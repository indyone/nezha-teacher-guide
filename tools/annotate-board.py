#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Σχολιασμός πλακέτας: ετικέτες-pills + γραμμές callout πάνω στο nezha-board-ports.jpg.
Χρήση: python3 tools/annotate-board.py [board.jpg] [out.jpg]
Οι συντεταγμένες είναι σε px της εικόνας 2000x1566 (έξοδος του process-photos.py --kind board
με το --box του tools/process-all.sh). Αν αλλάξει το crop, ξαναμέτρησε τα ANCHORS."""
import sys

from PIL import Image, ImageDraw, ImageFont

SRC = sys.argv[1] if len(sys.argv) > 1 else "assets/img/nezha-board-ports.jpg"
DST = sys.argv[2] if len(sys.argv) > 2 else "assets/img/nezha-board-annotated.jpg"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
INK = (20, 30, 50)
TOP, RIGHT, BOTTOM = 150, 640, 260


def main():
    board = Image.open(SRC).convert("RGB")
    assert board.size == (2000, 1566), "αναμένεται 2000x1566, βρέθηκε %s" % (board.size,)
    W, H = board.size
    canvas = Image.new("RGB", (W + RIGHT, H + TOP + BOTTOM), (246, 246, 246))
    canvas.paste(board, (0, TOP))
    font = ImageFont.truetype(FONT, 28)
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    def pt(x, y):
        return (x, y + TOP)

    def line(a, b):
        d.line([a, b], fill=INK + (235,), width=4)
        d.ellipse([b[0] - 9, b[1] - 9, b[0] + 9, b[1] + 9], fill=INK + (235,), outline=(255, 255, 255, 255), width=2)

    pills = []

    def pill(x, y, text, anchor="l"):
        """Επιστρέφει το (x,y) κέντρο-άκρων για σύνδεση. x,y = πάνω-αριστερά (anchor l) ή κέντρο (anchor c)."""
        lines = text.split("\n")
        w = max(d.textlength(t, font=font) for t in lines) + 40
        h = 46 * len(lines) + 4
        if anchor == "c":
            x -= w / 2
        pills.append((x, y, w, h, lines))
        return x, y, w, h

    # --- ετικέτες (πρώτα θέσεις, μετά γραμμές κάτω από τα pills) ---
    iic = pill(560, 40, "IIC (δεν χρησιμοποιείται)")
    power = pill(1290, 40, "Τροφοδοσία ⚡ (μην το αγγίζεις)")
    motors = pill(20, 40, "Κινητήρες M1–M4")
    ports = pill(1000, TOP + H + 40, "Θύρες αισθητήρων 1–4 (J1–J4)", "c")
    analog = pill(1000, TOP + H + 40 + 52, "● = και αναλογικά (μόνο 1–2)", "c")
    servo = pill(W + 30, TOP + 450, "Servo S1–S4")
    button = pill(W + 30, TOP + 690, "Κουμπί λειτουργίας")
    fischer = pill(W + 30, TOP + 920, "Υποδοχές Fischertechnik\n(δεν χρησιμοποιούνται)")

    # --- γραμμές ---
    for x in (550, 850, 1140):  # IIC
        line((min(max(x, iic[0] + 25), iic[0] + iic[2] - 25), iic[1] + iic[3]), pt(x, 85))
    line((power[0] + 120, power[1] + power[3]), pt(1430, 120))
    # motors: αγκύλη στην αριστερή πλευρά + 4 βελάκια
    bx = 50
    d.line([(bx, pt(0, 420)[1]), (bx, pt(0, 1130)[1])], fill=INK + (235,), width=4)
    d.line([(motors[0] + 60, motors[1] + motors[3]), (bx, pt(0, 420)[1])], fill=INK + (235,), width=4)
    for y in (430, 670, 880, 1100):
        line((bx, pt(0, y)[1]), pt(170, y))
    for x in (550, 850, 1140, 1420):  # θύρες 1–4
        line((ports[0] + ports[2] / 2 + (x - 985) * 0.25, ports[1]), pt(x, 1440))
    line((servo[0], servo[1] + servo[3] / 2), pt(1090, 590))
    line((button[0], button[1] + button[3] / 2), pt(1590, 790))
    line((fischer[0], fischer[1] + fischer[3] / 2), pt(735, 1010))

    # --- pills (ημιδιαφανές σκούρο, λευκό κείμενο) ---
    for x, y, w, h, lines in pills:
        d.rounded_rectangle([x, y, x + w, y + h], radius=h // 2 if len(lines) == 1 else 26, fill=INK + (215,))
        for i, t in enumerate(lines):
            d.text((x + w / 2, y + 25 + 46 * i), t, font=font, fill=(255, 255, 255, 255), anchor="mm")
    out = Image.alpha_composite(canvas.convert("RGBA"), ov).convert("RGB")
    out.save(DST, "JPEG", quality=85, optimize=True, exif=b"")
    print(DST, out.size)


if __name__ == "__main__":
    main()
