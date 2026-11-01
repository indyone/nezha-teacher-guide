#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Επεξεργασία φωτογραφιών kit: EXIF autorotate, autocontrast, ήπιο white balance,
sharpen, resize, αφαίρεση ΟΛΩΝ των EXIF, JPEG q82.

Χρήση:
  python3 tools/process-photos.py <raw-dir-ή-αρχείο> assets/img/ --name sonar
  python3 tools/process-photos.py raw/IMG_1.jpg assets/img/ --name board --max 2000
Με --name και πολλές εικόνες προκύπτουν name.jpg, name-2.jpg, ... (σε σειρά ονόματος).
Χωρίς --name κρατιέται το όνομα του αρχείου (slug). Ονόματα που περιέχουν
"board" ή "box" χρησιμοποιούν αυτόματα μέγιστη πλευρά 2000px, τα υπόλοιπα 1600px.
Απαιτεί Pillow. Τα raw ΔΕΝ μπαίνουν στο repo.
"""
import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps

EXTS = {".jpg", ".jpeg", ".png", ".heic", ".webp"}


def gray_world(im, strength=0.5):
    """Ήπιο white balance (gray-world, μερική διόρθωση, όρια ±15%)."""
    avg = list(im.resize((1, 1), Image.BOX).getpixel((0, 0)))
    mean = sum(avg) / 3
    gains = [1 + strength * (mean / a - 1) if a else 1 for a in avg]
    gains = [min(1.15, max(0.85, g)) for g in gains]
    r, g, b = im.split()
    return Image.merge("RGB", [c.point(lambda v, k=k: min(255, int(v * k))) for c, k in zip((r, g, b), gains)])


def process(src, dst, longest):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im = ImageOps.autocontrast(im, cutoff=1)
    im = gray_world(im)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=3))
    im.thumbnail((longest, longest), Image.LANCZOS)
    clean = Image.new("RGB", im.size)  # καθαρό αντίγραφο: καμία μεταδεδομένη
    clean.paste(im)
    clean.save(dst, "JPEG", quality=82, optimize=True, exif=b"")
    return clean.size


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "img"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("raw")
    ap.add_argument("out")
    ap.add_argument("--name")
    ap.add_argument("--max", type=int)
    a = ap.parse_args()
    raw = Path(a.raw)
    files = [raw] if raw.is_file() else sorted(p for p in raw.iterdir() if p.suffix.lower() in EXTS)
    if not files:
        sys.exit("Δεν βρέθηκαν εικόνες στο %s" % raw)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for i, f in enumerate(files):
        base = slug(a.name) if a.name else slug(f.stem)
        if a.name and i:
            base += "-%d" % (i + 1)
        longest = a.max or (2000 if ("board" in base or "box" in base) else 1600)
        dst = out / (base + ".jpg")
        size = process(f, dst, longest)
        print("%s -> %s %dx%d %d KB" % (f.name, dst, size[0], size[1], dst.stat().st_size // 1024))


if __name__ == "__main__":
    main()
