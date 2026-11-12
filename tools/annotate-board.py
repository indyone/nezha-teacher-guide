#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Σχολιασμός πλακέτας: ετικέτες-pills + γραμμές callout γύρω από το nezha-board-ports.jpg.
Χρήση: python3 tools/annotate-board.py [board.jpg] [out.jpg]
Οι συντεταγμένες (ANCHORS) είναι σε px της φωτογραφίας 2000x1498, με την πλακέτα όρθια:
τροφοδοσία και IIC αριστερά, θύρες 1–4 δεξιά, servo S1–S4 στη μέση, κινητήρες M1–M4 κάτω.
Αν αλλάξει η φωτογραφία ή το crop, ξαναμέτρησε τα ANCHORS."""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

SRC = sys.argv[1] if len(sys.argv) > 1 else "assets/img/nezha-board-ports.jpg"
DST = sys.argv[2] if len(sys.argv) > 2 else "assets/img/nezha-board-annotated.jpg"
FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]
INK = (20, 30, 50)
SIZE = (2000, 1498)
LEFT, RIGHT, TOP, BOTTOM = 560, 600, 150, 190

# σημεία πάνω στη φωτογραφία (px της 2000x1498)
POWER = (488, 425)                                   # αριστερή άκρη του ⚡
IIC = [(472, 640), (468, 855), (464, 1075)]          # αριστερή άκρη των IIC
PORTS = [(1455, 430), (1455, 640), (1452, 855), (1452, 1075)]  # δεξιά άκρη θυρών 1–4
SERVO = (845, 690)                                   # πάνω από το S1
BUTTON = (970, 300)                                  # πάνω άκρη του κουμπιού
FISCHER = (785, 1100)                                # κάτω αριστερή υποδοχή
MOTORS = [(710, 1365), (880, 1365), (1050, 1365), (1220, 1365)]  # κάτω άκρη M1–M4


def font(size):
    for f in FONTS:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    sys.exit("Δεν βρέθηκε γραμματοσειρά με Ελληνικά (δες FONTS)")


def main():
    board = Image.open(SRC).convert("RGB")
    assert board.size == SIZE, "αναμένεται %sx%s, βρέθηκε %s" % (SIZE + (board.size,))
    W, H = board.size
    # φόντο = το χρώμα των γωνιών της φωτογραφίας, ώστε να μη φαίνεται «κουτί»
    cs = [board.getpixel((x, y)) for x in (5, W - 6) for y in (5, H - 6)]
    bg = tuple(sum(c[i] for c in cs) // len(cs) for i in range(3))
    canvas = Image.new("RGB", (LEFT + W + RIGHT, TOP + H + BOTTOM), bg)
    # απαλό σβήσιμο των άκρων της φωτογραφίας (120 px) για να μη φαίνεται το όριό της
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rectangle([120, 120, W - 121, H - 121], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(50))
    canvas.paste(board, (LEFT, TOP), mask)
    fnt = font(30)
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    def pt(p):
        return (p[0] + LEFT, p[1] + TOP)

    def line(a, b):
        d.line([a, b], fill=INK + (235,), width=4)
        d.ellipse([b[0] - 9, b[1] - 9, b[0] + 9, b[1] + 9], fill=INK + (235,), outline=(255, 255, 255, 255), width=2)

    pills = []

    def pill(x, y, text, anchor="l"):
        """x,y = πάνω-αριστερά (l), πάνω-δεξιά (r) ή πάνω-κέντρο (c). Επιστρέφει x, y, w, h."""
        lines = text.split("\n")
        w = max(d.textlength(t, font=fnt) for t in lines) + 44
        h = 48 * len(lines) + 6
        if anchor == "c":
            x -= w / 2
        elif anchor == "r":
            x -= w
        pills.append((x, y, w, h, lines))
        return x, y, w, h

    def right_mid(p):
        return (p[0] + p[2], p[1] + p[3] / 2)

    def left_mid(p):
        return (p[0], p[1] + p[3] / 2)

    # --- ετικέτες ---
    power = pill(LEFT - 40, TOP + 300, "Τροφοδοσία\n(μην την αγγίζεις)", "r")
    iic = pill(LEFT - 40, TOP + 790, "IIC\n(δεν χρησιμοποιούνται)", "r")
    ports = pill(LEFT + W + 50, TOP + 640, "Θύρες αισθητήρων\n1–4 (J1–J4)\n● = και αναλογικά\n(μόνο 1, 2)")
    servo = pill(LEFT + 700, 30, "Servo S1–S4", "c")   # η γραμμή περνά αριστερά από το LED
    button = pill(LEFT + 1250, 30, "Κουμπί λειτουργίας", "c")
    fischer = pill(LEFT - 40, TOP + H + 40, "Υποδοχές Fischertechnik\n(δεν χρησιμοποιούνται)", "r")
    motors = pill(LEFT + 965, TOP + H + 50, "Κινητήρες M1–M4", "c")

    # --- γραμμές ---
    line(right_mid(power), pt(POWER))
    for p in IIC:
        line(right_mid(iic), pt(p))
    for p in PORTS:
        line(left_mid(ports), pt(p))
    line((servo[0] + servo[2] / 2, servo[1] + servo[3]), pt(SERVO))
    line((button[0] + button[2] / 2, button[1] + button[3]), pt(BUTTON))
    line((fischer[0] + fischer[2], fischer[1] + 20), pt(FISCHER))
    for i, p in enumerate(MOTORS):
        line((motors[0] + motors[2] * (i + 1) / 5, motors[1]), pt(p))

    # --- pills (ημιδιαφανές σκούρο, λευκό κείμενο) ---
    for x, y, w, h, lines in pills:
        d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2 if len(lines) == 1 else 26, fill=INK + (215,))
        for i, t in enumerate(lines):
            d.text((x + w / 2, y + 27 + 48 * i), t, font=fnt, fill=(255, 255, 255, 255), anchor="mm")
    out = Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")
    out.save(DST, "JPEG", quality=85, optimize=True, exif=b"")
    print(DST, out.size)


if __name__ == "__main__":
    main()
