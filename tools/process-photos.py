#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pipeline φωτογραφιών kit (catalogue look).

Χρήση:
  python3 tools/process-photos.py <raw.jpg> <out.jpg> --kind component|board|wide
         [--rotate N] [--pad 0.12] [--region x0,y0,x1,y1] [--box x0,y0,x1,y1]

Βήματα: EXIF auto-rotate -> autocontrast(0.5) -> ουδέτερο φόντο (per-channel gain
από 4 γωνίες 5%, φόντο -> ~246, τα highlights πάνω από το φόντο συμπιέζονται, όχι clip)
-> --region (κλάσματα της εικόνας μετά το EXIF) -> --rotate N (μοίρες αριστερόστροφα)
-> ανίχνευση υποκειμένου -> crop -> unsharp(1.2, 80) -> JPEG q85, χωρίς EXIF, sRGB.
  component : τετράγωνο 1200x1200, pad 12%
  board     : ίδιο aspect, 2000px πλάτος, pad 6%
  wide      : 4:3, 2000px πλάτος (όχι upscale πάνω από το φυσικό μέγεθος), pad 6%,
              χωρίς κανονικοποίηση φόντου (σκούρο γραφείο)
Απαιτεί Pillow + numpy. Τα raw ΔΕΝ μπαίνουν στο repo.
"""
import argparse
import io
import sys

import numpy as np
from PIL import Image, ImageCms, ImageFilter, ImageOps

TARGET = 246


def corners(arr, frac=0.05):
    h, w = arr.shape[:2]
    n = max(2, int(w * frac))
    m = max(2, int(h * frac))
    ps = [arr[:m, :n], arr[:m, -n:], arr[-m:, :n], arr[-m:, -n:]]
    return np.mean([p.reshape(-1, 3).mean(0) for p in ps], axis=0)


def trim_dark_edges(im, maxfrac=0.08, ratio=0.9):
    """Κόβει σκοτεινές ταινίες/βινιέτα στις άκρες (artefact της κάμερας)."""
    g = np.asarray(im.convert("L")).astype(np.float32)
    h, w = g.shape
    out = []
    for prof, n in ((g.mean(0), w), (g.mean(1), h)):
        ref = np.median(prof[n // 4: 3 * n // 4])
        lim = int(n * maxfrac)
        lo = next((i for i in range(lim) if prof[i] >= ratio * ref), lim)
        hi = next((i for i in range(lim) if prof[n - 1 - i] >= ratio * ref), lim)
        out.append((lo + (4 if lo else 0), hi + (4 if hi else 0)))
    (l, r), (t, b) = out
    return im.crop((l, t, im.width - r, im.height - b))


def _feat(x, y):
    return np.stack([np.ones_like(x), x, y, x * x, x * y, y * y], -1)


def bg_model(im, tol=16, iters=5):
    """Εύρωστο fit δευτεροβάθμιου επιπέδου ανά κανάλι στο φόντο (ξεκινά από το περίγραμμα).
    Επιστρέφει (model_small[h,w,3], inlier_mask_small)."""
    sm = im.resize((160, max(8, round(160 * im.height / im.width))), Image.BILINEAR)
    a = np.asarray(sm).astype(np.float32)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    F = _feat(xx / w * 2 - 1, yy / h * 2 - 1).reshape(-1, 6)
    flat = a.reshape(-1, 3)
    m = np.zeros((h, w), bool)
    k = max(2, int(0.06 * w))
    m[:k] = m[-k:] = True
    m[:, :k] = m[:, -k:] = True
    m = m.ravel()
    for _ in range(iters):
        coef = np.stack([np.linalg.lstsq(F[m], flat[m, c], rcond=None)[0] for c in range(3)], 1)
        mod = F @ coef
        m = np.abs(flat - mod).max(1) < tol
    return mod.reshape(h, w, 3), m.reshape(h, w)


def normalise(im):
    """Flat-field + ουδέτερο φόντο: φόντο -> TARGET σε όλη την εικόνα (χωρίς gradient),
    highlights πάνω από το φόντο συμπιέζονται (όχι clip), μετά autocontrast 0.5 στις σκιές."""
    mod, _ = bg_model(im)
    big = np.stack([np.asarray(Image.fromarray(mod[..., c]).resize(im.size, Image.BICUBIC)) for c in range(3)], -1)
    big = np.clip(big, 20, 254)
    a = np.asarray(im).astype(np.float32)
    out = np.where(a <= big, a * TARGET / big, TARGET + (a - big) * (255 - TARGET) / (255 - big))
    out = Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8))
    # autocontrast μόνο προς τις σκιές: το λευκό σημείο μένει στο 255, το φόντο στο TARGET
    lut = []
    for c in range(3):
        hist = np.asarray(out.getchannel(c).histogram()).cumsum()
        lo = int(np.searchsorted(hist, 0.005 * hist[-1]))
        lut += [int(round(max(0, (v - lo) * TARGET / (TARGET - lo)))) if v <= TARGET else v for v in range(256)]
    return out.point(lut)


def subject_bbox(im, tol=16):
    _, inl = bg_model(im, tol=tol)
    mask = ~inl
    m = Image.fromarray((mask * 255).astype(np.uint8))
    m = m.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5))
    ys, xs = np.where(np.asarray(m) > 0)
    if len(xs) == 0:
        return (0, 0, im.width, im.height)
    s = im.width / mask.shape[1]
    return tuple(int(v * s) for v in (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def crop_pad(im, box, bgcol, aspect, pad, square_by_max=True):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w, h = x1 - x0, y1 - y0
    if aspect == 1:
        w = h = max(w, h) * (1 + 2 * pad)
    else:
        w, h = w * (1 + 2 * pad), h * (1 + 2 * pad)
        if aspect:
            if w / h < aspect:
                w = h * aspect
            else:
                h = w / aspect
    w, h = int(round(w)), int(round(h))
    left, top = int(round(cx - w / 2)), int(round(cy - h / 2))
    if bgcol is None:  # wide: θολό γέμισμα από την ίδια φωτογραφία
        canvas = im.resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(w, h) // 25))
    else:
        canvas = Image.new("RGB", (w, h), tuple(bgcol))
    canvas.paste(im, (-left, -top))  # PIL clips automatically
    return canvas


def to_srgb(im):
    icc = im.info.get("icc_profile")
    if icc:
        try:
            return ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(icc)),
                                             ImageCms.createProfile("sRGB"), outputMode="RGB")
        except Exception:
            pass
    return im


def process(src, dst, kind="component", rotate=0, pad=None, region=None, box=None):
    im = to_srgb(ImageOps.exif_transpose(Image.open(src))).convert("RGB")
    wide = kind == "wide"
    if wide:
        im = ImageOps.autocontrast(im, cutoff=0.5)
    else:
        im = normalise(trim_dark_edges(im))
    if region:
        x0, y0, x1, y1 = region
        W, H = im.size
        im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    if rotate:
        im = im.rotate(rotate, expand=True, resample=Image.BICUBIC, fillcolor=(TARGET,) * 3)
    bgcol = (TARGET,) * 3
    if wide:
        a = np.asarray(im.resize((700, int(700 * im.height / im.width)))).astype(np.int16)
        bgcol = tuple(int(v) for v in np.median(a.reshape(-1, 3), 0))
        # υποκείμενο = ό,τι ΔΕΝ είναι το σκούρο γραφείο: το κουτί/υλικά είναι πιο φωτεινά
        lum = a.mean(2)
        mask = lum > 90
        m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(7)).filter(ImageFilter.MaxFilter(15))
        ys, xs = np.where(np.asarray(m) > 0)
        s = im.width / 700
        box = tuple(int(v * s) for v in (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)) if len(xs) else (0, 0, im.width, im.height)
        out = crop_pad(im, box, None, 4 / 3, 0.06 if pad is None else pad)
        outw = min(2000, out.width)
        out = out.resize((outw, round(outw * 3 / 4)), Image.LANCZOS)
    elif kind == "board":
        if box:  # λευκή πλακέτα σε λευκό φόντο: χειροκίνητο box (κλάσματα) αντί ανίχνευσης
            box = (int(box[0] * im.width), int(box[1] * im.height), int(box[2] * im.width), int(box[3] * im.height))
        else:
            box = subject_bbox(im)
        out = crop_pad(im, box, bgcol, None, 0.06 if pad is None else pad)
        out = out.resize((2000, round(out.height * 2000 / out.width)), Image.LANCZOS)
    else:
        box = subject_bbox(im)
        out = crop_pad(im, box, bgcol, 1, 0.12 if pad is None else pad)
        out = out.resize((1200, 1200), Image.LANCZOS)
    out = out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=80, threshold=2))
    clean = Image.new("RGB", out.size)
    clean.paste(out)
    clean.save(dst, "JPEG", quality=85, optimize=True, exif=b"")
    return clean


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("raw")
    ap.add_argument("out")
    ap.add_argument("--kind", choices=["component", "board", "wide"], default="component")
    ap.add_argument("--rotate", type=float, default=0, help="μοίρες αριστερόστροφα (μετά το EXIF)")
    ap.add_argument("--pad", type=float)
    ap.add_argument("--region", help="x0,y0,x1,y1 ως κλάσματα 0-1 (μετά το EXIF, πριν το rotate)")
    ap.add_argument("--box", help="x0,y0,x1,y1 κλάσματα του υποκειμένου (μόνο board, μετά το rotate)")
    a = ap.parse_args()
    box = tuple(float(v) for v in a.box.split(",")) if a.box else None
    region = tuple(float(v) for v in a.region.split(",")) if a.region else None
    im = process(a.raw, a.out, a.kind, a.rotate, a.pad, region, box)
    msg = "%s %dx%d" % (a.out, im.width, im.height)
    if a.kind != "wide":
        c = corners(np.asarray(im).astype(np.float32))
        msg += " corners=(%.0f,%.0f,%.0f) spread=%.1f" % (*c, c.max() - c.min())
    print(msg)


if __name__ == "__main__":
    sys.exit(main())
