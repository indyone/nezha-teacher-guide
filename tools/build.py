#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — Οδηγός Δασκάλου: σημασιολογικό markdown (pandoc fenced divs) -> ένα HTML έτοιμο για Paged.js.

Χρήση (από τη ρίζα του repo):  python3 tools/build.py [content] [dist]
  * 1ο όρισμα: φάκελος με τα .md (default content/)
  * 2ο όρισμα: φάκελος εξόδου (default dist/)· γράφεται dist/index.html και
    αντιγράφονται τα assets/img -> dist/img και assets/vendor -> dist/assets/vendor
    (αν το όρισμα τελειώνει σε .html, γράφεται ακριβώς εκεί το αρχείο)
  * template/css από design/, εικόνες από assets/img/ (στο markdown: img/<όνομα>.jpg)
  * έκδοση: αρχείο VERSION, με προτεραιότητα στο `git describe --tags --always`
Μόνο stdlib + pandoc 2.x.
"""
import html as htmllib
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # ρίζα του repo
DESIGN = ROOT / "design"
IMG_DIR = ROOT / "assets" / "img"
VENDOR_DIR = ROOT / "assets" / "vendor"


def img_exists(src):
    """«img/x.jpg» στο markdown -> assets/img/x.jpg στο repo."""
    if not src or not src.startswith("img/"):
        return False
    return (IMG_DIR / src[len("img/"):]).is_file()


def get_version():
    """git describe --tags --always αν υπάρχει, αλλιώς το αρχείο VERSION."""
    try:
        v = subprocess.run(["git", "describe", "--tags", "--always"], cwd=ROOT, capture_output=True,
                           text=True, timeout=10)
        if v.returncode == 0 and v.stdout.strip():
            return v.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        return (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    except OSError:
        return "dev"

# ----------------------------------------------------------------------------
# Μίνι DOM (stdlib μόνο)
# ----------------------------------------------------------------------------
VOID = {"img", "br", "hr", "input", "col", "meta", "link", "source", "wbr"}


class Raw(str):
    """Κείμενο που βγαίνει ως έχει (έτοιμο HTML)."""


class El:
    def __init__(self, tag, attrs=None, kids=None):
        self.tag = tag
        self.attrs = dict(attrs or {})
        self.kids = list(kids or [])

    @property
    def classes(self):
        return set((self.attrs.get("class") or "").split())

    def a(self, key, default=None):
        """attribute, με fallback στο data-<key> (έτσι τα γράφει ο pandoc)."""
        if key in self.attrs:
            return self.attrs[key]
        return self.attrs.get("data-" + key, default)


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = El("root")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        el = El(tag, {k: ("" if v is None else v) for k, v in attrs})
        self.stack[-1].kids.append(el)
        if tag not in VOID:
            self.stack.append(el)

    def handle_startendtag(self, tag, attrs):
        el = El(tag, {k: ("" if v is None else v) for k, v in attrs})
        self.stack[-1].kids.append(el)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].kids.append(data)


def frag(html):
    p = _Parser()
    p.feed(html)
    p.close()
    return p.root.kids


def ser(n):
    if isinstance(n, Raw):
        return str(n)
    if isinstance(n, str):
        return htmllib.escape(n, quote=False)
    attrs = "".join(
        ' %s="%s"' % (k, htmllib.escape(str(v), quote=True)) for k, v in n.attrs.items()
    )
    if n.tag in VOID:
        return "<%s%s />" % (n.tag, attrs)
    return "<%s%s>%s</%s>" % (n.tag, attrs, "".join(ser(k) for k in n.kids), n.tag)


def inner(el):
    return "".join(ser(k) for k in el.kids)


def text_of(n):
    if isinstance(n, str):
        return str(n)
    return "".join(text_of(k) for k in n.kids)


def walk(n):
    yield n
    if isinstance(n, El):
        for k in n.kids:
            yield from walk(k)


def mk(tag, cls=None, kids=None, **attrs):
    d = {}
    if cls:
        d["class"] = cls
    for k, v in attrs.items():
        d[k.replace("_", "-")] = v
    return El(tag, d, kids)


def R(html):
    return Raw(html)


def flat(li_or_el):
    """inner html χωρίς <p> (loose lists)."""
    s = inner(li_or_el)
    s = re.sub(r"</p>\s*<p>", " ", s)
    s = re.sub(r"</?p>", "", s)
    return s.strip()


def esc(s):
    return htmllib.escape(s, quote=True)


# ----------------------------------------------------------------------------
# Εικονίδια (24x24 line-art)
# ----------------------------------------------------------------------------
ICONS = {
    "led": '<path d="M12 3a5 5 0 0 0-5 5v5h10V8a5 5 0 0 0-5-5zM9 13v4M15 13v4M7 17h10"/>',
    "cable": '<path d="M3 15c4 0 4-6 9-6s5 6 9 6M3 15v3M21 15v3M2 18h4M18 18h4"/>',
    "board": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 18v2M12 18v2M17 18v2M7 10h3v4H7zM13 10h4"/>',
    "bricks": '<rect x="4" y="4" width="7" height="7" rx="1"/><rect x="13" y="4" width="7" height="7" rx="1"/><rect x="4" y="13" width="16" height="7" rx="1"/>',
    "motor": '<circle cx="10" cy="12" r="6"/><circle cx="10" cy="12" r="1.5"/><path d="M16 12h5M10 3v3M10 18v3"/>',
    "servo": '<rect x="3" y="8" width="14" height="9" rx="1.5"/><path d="M17 12h3a2 2 0 0 0 0-4h-3M7 8V5M12 8V5"/>',
    "sensor": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "extra": '<path d="M4 8l8-4 8 4v8l-8 4-8-4zM4 8l8 4 8-4M12 12v8"/>',
    "check": '<path d="M5 12l4 4 10-10"/>',
    "tip": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "warn": '<path d="M12 3l10 18H2zM12 10v5M12 18v.5"/>',
    "safety": '<path d="M12 3l8 3v6c0 4.5-3.4 7.7-8 9-4.6-1.3-8-4.5-8-9V6z"/><path d="M12 8v5M12 16v.5"/>',
    "note": '<path d="M4 20l4-1 11-11-3-3L5 16z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.5"/>',
    "smile": '<circle cx="12" cy="12" r="9"/><path d="M8 14c1 2.4 7 2.4 8 0M9 9.5v.5M15 9.5v.5"/>',
    "bubble": '<path d="M4 5h16v11H9l-5 4z"/>',
    "wrench": '<path d="M14 6a4 4 0 0 0 5 5l-9 9a2 2 0 0 1-3-3l9-9a4 4 0 0 1-2-2z"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.5 7.5L20 18M8.5 16.5L20 6"/>',
}


def icon(name, cls="ico", stroke="#22303C", sw="1.6"):
    return R(
        '<svg class="%s" viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="%s" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
        % (cls, stroke, sw, ICONS[name])
    )


# ----------------------------------------------------------------------------
# Ελάχιστος κωδικοποιητής QR (byte mode, EC level L, εκδόσεις 1–10, ≤271 bytes)
# ----------------------------------------------------------------------------
# έκδοση: (σύνολο data cw, ec cw ανά block, [(πλήθος blocks, data cw ανά block), ...])
_QR_L = {
    1: (19, 7, [(1, 19)]), 2: (34, 10, [(1, 34)]), 3: (55, 15, [(1, 55)]),
    4: (80, 20, [(1, 80)]), 5: (108, 26, [(1, 108)]), 6: (136, 18, [(2, 68)]),
    7: (156, 20, [(2, 78)]), 8: (194, 24, [(2, 97)]), 9: (232, 30, [(2, 116)]),
    10: (274, 18, [(2, 68), (2, 69)]),
}
_QR_ALIGN = {1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30], 6: [6, 34],
             7: [6, 22, 38], 8: [6, 24, 42], 9: [6, 26, 46], 10: [6, 28, 50]}


def _gf_mul(x, y):
    z = 0
    for i in range(7, -1, -1):
        z = (z << 1) ^ ((z >> 7) * 0x11D)
        z ^= ((y >> i) & 1) * x
    return z


def _rs_gen(deg):
    r = [0] * (deg - 1) + [1]
    root = 1
    for _ in range(deg):
        for j in range(deg):
            r[j] = _gf_mul(r[j], root)
            if j + 1 < deg:
                r[j] ^= r[j + 1]
        root = _gf_mul(root, 2)
    return r


def _rs_rem(data, gen):
    res = [0] * len(gen)
    for b in data:
        f = b ^ res.pop(0)
        res.append(0)
        for i, c in enumerate(gen):
            res[i] ^= _gf_mul(c, f)
    return res


def qr_matrix(text):
    data = text.encode("utf-8")
    ver = None
    for v in range(1, 11):
        cap = _QR_L[v][0] - (2 if v < 10 else 3)
        if len(data) <= cap:
            ver = v
            break
    if ver is None:
        return None
    total_data, ec_len, groups = _QR_L[ver]
    # bit stream
    bits = [0, 1, 0, 0]
    cc = 8 if ver < 10 else 16
    bits += [(len(data) >> i) & 1 for i in range(cc - 1, -1, -1)]
    for b in data:
        bits += [(b >> i) & 1 for i in range(7, -1, -1)]
    cap_bits = total_data * 8
    bits += [0] * min(4, cap_bits - len(bits))
    bits += [0] * (-len(bits) % 8)
    cws = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
    pad = 0xEC
    while len(cws) < total_data:
        cws.append(pad)
        pad ^= 0xEC ^ 0x11
    # blocks
    blocks, pos = [], 0
    gen = _rs_gen(ec_len)
    for n, dl in groups:
        for _ in range(n):
            d = cws[pos:pos + dl]
            pos += dl
            blocks.append((d, _rs_rem(d, gen)))
    out = []
    for i in range(max(len(b[0]) for b in blocks)):
        for d, _ in blocks:
            if i < len(d):
                out.append(d[i])
    for i in range(ec_len):
        for _, e in blocks:
            out.append(e[i])
    allbits = []
    for b in out:
        allbits += [(b >> i) & 1 for i in range(7, -1, -1)]

    size = ver * 4 + 17
    M = [[False] * size for _ in range(size)]
    F = [[False] * size for _ in range(size)]

    def setf(x, y, dark):
        if 0 <= x < size and 0 <= y < size:
            M[y][x] = bool(dark)
            F[y][x] = True

    for i in range(size):  # timing
        setf(6, i, i % 2 == 0)
        setf(i, 6, i % 2 == 0)
    for cx, cy in ((3, 3), (size - 4, 3), (3, size - 4)):  # finders
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                setf(cx + dx, cy + dy, max(abs(dx), abs(dy)) not in (2, 4))
    pos_list = _QR_ALIGN[ver]
    for i, ax in enumerate(pos_list):  # alignment
        for j, ay in enumerate(pos_list):
            if (i == 0 and j == 0) or (i == 0 and j == len(pos_list) - 1) or (i == len(pos_list) - 1 and j == 0):
                continue
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    setf(ax + dx, ay + dy, max(abs(dx), abs(dy)) != 1)

    def fmt_bits(mask):
        d = (1 << 3) | mask  # EC level L = 01
        r = d
        for _ in range(10):
            r = (r << 1) ^ ((r >> 9) * 0x537)
        return ((d << 10) | r) ^ 0x5412

    def draw_format(mask):
        b = fmt_bits(mask)
        g = lambda i: (b >> i) & 1
        for i in range(6):
            setf(8, i, g(i))
        setf(8, 7, g(6)); setf(8, 8, g(7)); setf(7, 8, g(8))
        for i in range(9, 15):
            setf(14 - i, 8, g(i))
        for i in range(8):
            setf(size - 1 - i, 8, g(i))
        for i in range(8, 15):
            setf(8, size - 15 + i, g(i))
        setf(8, size - 8, True)

    draw_format(0)
    if ver >= 7:
        r = ver
        for _ in range(12):
            r = (r << 1) ^ ((r >> 11) * 0x1F25)
        vb = (ver << 12) | r
        for i in range(18):
            bit = (vb >> i) & 1
            a, b2 = size - 11 + i % 3, i // 3
            setf(a, b2, bit)
            setf(b2, a, bit)
    # data
    i = 0
    right = size - 1
    while right >= 1:
        if right == 6:
            right = 5
        for vert in range(size):
            for j in range(2):
                x = right - j
                up = ((right + 1) & 2) == 0
                y = size - 1 - vert if up else vert
                if not F[y][x] and i < len(allbits):
                    M[y][x] = bool(allbits[i])
                    i += 1
        right -= 2

    masks = [
        lambda x, y: (x + y) % 2 == 0, lambda x, y: y % 2 == 0, lambda x, y: x % 3 == 0,
        lambda x, y: (x + y) % 3 == 0, lambda x, y: (x // 3 + y // 2) % 2 == 0,
        lambda x, y: x * y % 2 + x * y % 3 == 0, lambda x, y: (x * y % 2 + x * y % 3) % 2 == 0,
        lambda x, y: ((x + y) % 2 + x * y % 3) % 2 == 0,
    ]

    def penalty(g):
        p = 0
        for rows in (g, [list(c) for c in zip(*g)]):
            for row in rows:
                run, prev = 0, None
                for v in row:
                    if v == prev:
                        run += 1
                        if run == 5:
                            p += 3
                        elif run > 5:
                            p += 1
                    else:
                        prev, run = v, 1
                s = "".join("1" if v else "0" for v in row)
                p += 40 * (s.count("10111010000") + s.count("00001011101"))
        for y in range(size - 1):
            for x in range(size - 1):
                if g[y][x] == g[y][x + 1] == g[y + 1][x] == g[y + 1][x + 1]:
                    p += 3
        dark = sum(sum(r) for r in g)
        p += (abs(dark * 20 - size * size * 10) // (size * size)) * 10
        return p

    best = None
    for m in range(8):
        for y in range(size):
            for x in range(size):
                if not F[y][x] and masks[m](x, y):
                    M[y][x] = not M[y][x]
        draw_format(m)
        pen = penalty(M)
        if best is None or pen < best[0]:
            best = (pen, m, [r[:] for r in M])
        for y in range(size):
            for x in range(size):
                if not F[y][x] and masks[m](x, y):
                    M[y][x] = not M[y][x]
    return best[2]


def qr_svg(url, cls="qr"):
    m = qr_matrix(url)
    if m is None:
        return None
    n, q = len(m), 2
    d = "".join("M%d %dh1v1h-1z" % (x + q, y + q) for y in range(n) for x in range(n) if m[y][x])
    return R(
        '<svg class="%s" viewBox="0 0 %d %d" shape-rendering="crispEdges" role="img" '
        'aria-label="QR: %s"><rect width="100%%" height="100%%" fill="#fff"/><path d="%s" fill="#22303C"/></svg>'
        % (cls, n + 2 * q, n + 2 * q, esc(url), d)
    )


# ----------------------------------------------------------------------------
# Μετασχηματισμοί components
# ----------------------------------------------------------------------------
PRODUCED = set()
STATS = {"qr_fallback": 0, "placeholders": 0, "plain_tables": 0, "fig_counter": 0}
LEVEL_NAMES = {}
CHIP_RE = re.compile(r"^[JMSP]\d{1,2}$")


def placeholder(label, cls="box"):
    STATS["placeholders"] += 1
    return mk("div", cls, [mk("span", "ph", ["[ΕΙΚΟΝΑ: %s]" % label])])


def img_or_placeholder(src, label, box_cls="box"):
    if img_exists(src):
        return mk("img", "pic", src=src, alt=label, loading="eager")
    return placeholder(label, box_cls)


def dots(n):
    try:
        n = max(0, min(5, int(n)))
    except (TypeError, ValueError):
        n = 0
    return R('<span class="dots">%s</span>' % ("<i class='on'></i>" * n + "<i></i>" * (5 - n)))


def h_glance(el):
    lvl = el.a("level", "")
    lines = []
    for k in el.kids:
        if isinstance(k, El) and k.tag == "p":
            s = inner(k).replace("<br />", "\n")
            lines += [l.strip() for l in s.split("\n")]
    goal, notes = [], {}
    concept_line = None
    for l in lines:
        if not l:
            continue
        m = re.match(r"^(?:<strong>)?(ΔΔ|Δ[ΜM])\s*:\s*(?:</strong>)?\s*(.*)$", l)
        if m:
            notes["ΔΔ" if m.group(1) == "ΔΔ" else "ΔΜ"] = re.sub(r"^[●○◐\s]+", "", m.group(2))
            continue
        m = re.match(r"^(?:<strong>)?Προαπαιτούμενα\s*:\s*(?:</strong>)?\s*(.*)$", l)
        if m:
            notes["pre"] = m.group(1)
            continue
        m = re.match(r"^(?:<strong>)?Νέ(α|ες)\s+έννοι(?:α|ες)\s*:\s*(?:</strong>)?\s*(.*)$", l)
        if m:
            concept_line = ("Νέα έννοια" if m.group(1) == "α" else "Νέες έννοιες", m.group(2))
            continue
        goal.append(l)
    if concept_line is None and el.a("concept"):
        c = el.a("concept")
        concept_line = ("Νέες έννοιες" if "," in c else "Νέα έννοια", esc(c))
    card = mk("div", "glance-card lv%s" % lvl if lvl else "glance-card")
    card.kids.append(R('<span class="chip level">ΕΠΙΠΕΔΟ %s</span>' % esc(lvl)))
    card.kids.append(R('<p class="goal">%s</p>' % " ".join(goal)))
    clock = ser(icon("clock", "ico-s", "currentColor", "2"))
    cells = [
        ("ΔΔ", ser(dots(el.a("dd")))),
        ("ΔΜ", ser(dots(el.a("dm")))),
        ("ΔΙΑΡΚΕΙΑ", '<span class="val">%s %s\'</span>' % (clock, esc(el.a("time", "–")))),
        ("ΤΑΞΗ", '<span class="val">%s</span>' % esc(el.a("grades", "–"))),
    ]
    card.kids.append(R('<div class="glance-cells">%s</div>' % "".join(
        '<div class="cell"><span class="lbl">%s</span>%s</div>' % c for c in cells)))
    n = []
    if concept_line:
        n.append('<p class="concept"><b>%s:</b> %s</p>' % concept_line)
    if "ΔΔ" in notes:
        n.append("<p><b>ΔΔ:</b> %s</p>" % notes["ΔΔ"])
    if "ΔΜ" in notes:
        n.append("<p><b>ΔΜ:</b> %s</p>" % notes["ΔΜ"])
    n.append("<p><b>Προαπαιτούμενα:</b> %s</p>" % notes.get("pre", "κανένα"))
    card.kids.append(R('<div class="glance-notes">%s</div>' % "".join(n)))
    return card


MAT_ICONS = [
    (r"εκτός\s*kit", "extra"), (r"\bled\b", "led"), (r"καλώδ|\busb\b|rj11", "cable"),
    (r"micro:bit|πλακέτ|nezha", "board"), (r"κινητήρ|motor", "motor"), (r"servo", "servo"),
    (r"αισθητήρ|sensor|sonar|trimpot|ποτενσ", "sensor"), (r"τουβλ|τούβλ|brick", "bricks"),
]


def h_materials(el):
    ul = next((k for k in el.kids if isinstance(k, El) and k.tag == "ul"), None)
    out = mk("ul", "materials")
    if ul is None:
        return el
    for li in [k for k in ul.kids if isinstance(k, El) and k.tag == "li"]:
        body = flat(li)
        plain = text_of(li).lower()
        ic = "check"
        for pat, name in MAT_ICONS:
            if re.search(pat, plain):
                ic = name
                break
        m = re.match(r"^(\d+)\s+(.*)$", body, re.S)
        qty = '<span class="qty">%s</span>' % m.group(1) if m else ""
        body = m.group(2) if m else body
        out.kids.append(R('<li class="%s">%s<span>%s%s</span></li>' % (
            "extra" if ic == "extra" else "", ser(icon(ic, "mi")), qty, body)))
    return out


def h_timeline(el):
    ul = next((k for k in el.kids if isinstance(k, El) and k.tag in ("ul", "ol")), None)
    out = mk("ol", "timeline")
    if ul is None:
        return el
    for li in [k for k in ul.kids if isinstance(k, El) and k.tag == "li"]:
        s = flat(li)
        m = re.match(r"^<strong>(.*?)</strong>\s*(.*)$", s, re.S)
        if m:
            out.kids.append(R('<li><span class="min">%s</span>%s</li>' % (m.group(1), m.group(2))))
        else:
            out.kids.append(R("<li>%s</li>" % s))
    return out


def h_codefig(el):
    src, cap, link = el.a("src"), el.a("caption", ""), el.a("link")
    fid = el.attrs.get("id", "")
    m = re.match(r"^fig-(.+)$", fid)
    if m:
        num = m.group(1).replace("-", ".")
    else:
        STATS["fig_counter"] += 1
        num = str(STATS["fig_counter"])
    fig = mk("figure", "code-figure", **({"id": fid} if fid else {}))
    row = mk("div", "cf-row")
    main = mk("div", "cf-main")
    main.kids.append(img_or_placeholder(src, cap or "Κώδικας"))
    row.kids.append(main)
    if link:
        qr = qr_svg(link)
        side = mk("div", "cf-link")
        if qr is not None:
            side.kids.append(qr)
            side.kids.append(R('<a href="%s">Άνοιξε τον κώδικα</a>' % esc(link)))
        else:
            STATS["qr_fallback"] += 1
            side.kids.append(R('<a href="%s">Άνοιξε τον κώδικα</a><span class="url">%s</span>' % (esc(link), esc(link))))
        row.kids.append(side)
    fig.kids.append(row)
    fig.kids.append(R("<figcaption><b>Εικόνα %s</b> – %s</figcaption>" % (esc(num), esc(cap))))
    return fig


def h_steps(el):
    ol = next((k for k in el.kids if isinstance(k, El) and k.tag in ("ol", "ul")), None)
    out = mk("ol", "steps")
    if ol is None:
        return el
    i = 0
    for li in [k for k in ol.kids if isinstance(k, El) and k.tag == "li"]:
        i += 1
        out.kids.append(R('<li><span class="marker inline">%d</span><div>%s</div></li>' % (i, flat(li))))
    return out


TROUBLE_RE = re.compile(
    r"^<strong>(.*?)</strong>\s*[—–-]*\s*Γιατί\s*:\s*(.*?)\s*Κάνε\s*:\s*(.*)$", re.S)


def h_trouble(el):
    ul = next((k for k in el.kids if isinstance(k, El) and k.tag in ("ul", "ol")), None)
    out = mk("div", "trouble")
    if ul is None:
        return el
    for li in [k for k in ul.kids if isinstance(k, El) and k.tag == "li"]:
        s = flat(li)
        m = TROUBLE_RE.match(s)
        if m:
            out.kids.append(R(
                '<div class="trouble-card"><div class="tc-sym">%s</div>'
                '<div class="tc-row"><b>Γιατί:</b> %s</div><div class="tc-row"><b>Κάνε:</b> %s</div></div>'
                % m.groups()))
        else:
            out.kids.append(R('<div class="trouble-card"><div class="tc-row">%s</div></div>' % s))
    return out


CALLOUTS = {"tip": "Συμβουλή", "warn": "Προσοχή", "safety": "Ασφάλεια", "note": "Σημείωση δασκάλου"}


def make_callout(kind):
    def h(el):
        label = CALLOUTS[kind]
        if el.attrs.get("title"):
            label += " · " + el.attrs["title"]
        c = mk("div", "callout " + kind)
        c.kids += [icon(kind), R('<span class="label">%s</span>' % esc(label))]
        c.kids += el.kids
        return c
    return h


def h_aside(el):
    c = mk("div", "aside")
    c.kids.append(icon("info"))
    c.kids.append(R('<span class="label">%s</span>' % esc(el.attrs.get("title") or "Στο περιθώριο")))
    c.kids += el.kids
    return c


def h_humor(el):
    c = mk("div", "aside humor")
    c.kids.append(icon("smile"))
    c.kids.append(R('<span class="label">%s</span>' % esc(el.attrs.get("title") or "Μικρή παρατήρηση")))
    c.kids += el.kids
    return c


def h_challenge(el):
    c = mk("div", "challenge-card")
    c.kids.append(icon("scissors", "scissors", "currentColor", "1.6"))
    c.kids.append(R('<span class="ct">%s</span>' % esc(el.attrs.get("title") or "Κάρτα Πρόκλησης")))
    c.kids += el.kids
    return c


def _lis(el):
    ul = next((k for k in el.kids if isinstance(k, El) and k.tag in ("ul", "ol")), None)
    return [k for k in (ul.kids if ul else []) if isinstance(k, El) and k.tag == "li"]


def h_diff(el):
    out = mk("div", "diff")
    for li in _lis(el):
        s = flat(li)
        m = re.match(r"^<strong>(.*?)</strong>\s*(.*)$", s, re.S)
        if m:
            out.kids.append(R('<div class="diff-card"><div class="dh">%s</div><div>%s</div></div>' % m.groups()))
        else:
            out.kids.append(R('<div class="diff-card"><div>%s</div></div>' % s))
    return out


def h_discuss(el):
    out = mk("ul", "discuss")
    for li in _lis(el):
        out.kids.append(R("<li>%s<span>%s</span></li>" % (ser(icon("bubble", "bi")), flat(li))))
    return out


def h_build(el):
    url = el.a("url")
    out = mk("div", "build")
    head = '<div class="bh">%s<span class="label">Σημειώσεις κατασκευής</span></div>' % ser(icon("wrench"))
    out.kids.append(R(head))
    if url:
        qr = qr_svg(url, "qr qr-s")
        short = re.sub(r"^https?://", "", url)
        body = '<div class="b-link"><div><a href="%s">Οδηγίες βήμα-βήμα στο wiki</a><span class="url">%s</span></div>%s</div>' % (
            esc(url), esc(short), ser(qr) if qr is not None else "")
        if qr is None:
            STATS["qr_fallback"] += 1
        out.kids.append(R(body))
    out.kids += el.kids
    return out


def h_component(el):
    name = el.a("name", "")
    img = el.a("img")
    card = mk("div", "component-card")
    ph = img_or_placeholder(img, name, "photo")
    if isinstance(ph, El) and ph.tag == "img":
        ph = mk("div", "photo", [ph])
    card.kids.append(ph)
    facts = mk("div", "facts")
    facts.kids.append(R('<div class="cc-kicker">Εξάρτημα</div><div class="cc-title">%s</div>' % esc(name)))
    dl = "<dl>"
    for li in _lis(el):
        s = flat(li)
        m = re.match(r"^<strong>(.*?)</strong>\s*(.*)$", s, re.S)
        dl += "<dt>%s</dt><dd>%s</dd>" % m.groups() if m else "<dd>%s</dd>" % s
    facts.kids.append(R(dl + "</dl>"))
    card.kids.append(facts)
    return card


def h_cards(el):
    cols = el.a("cols", "3")
    out = mk("div", "cards cols-%s" % re.sub(r"\D", "", cols or "3"))
    out.kids = el.kids
    return out


def h_card(el):
    c = mk("div", "card")
    if el.attrs.get("title"):
        c.kids.append(R('<div class="card-title">%s</div>' % esc(el.attrs["title"])))
    c.kids += el.kids
    return c


def h_pagebreak(el):
    return mk("div", "pb")


def h_passclass(cls):
    def h(el):
        STATS["plain_tables"] -= sum(1 for n in walk(el) if isinstance(n, El) and n.tag == "table")
        el.attrs = {"class": cls}
        return el
    return h


def h_figure(el):
    """pandoc <div class=figure><img><p class=caption> ή <figure>."""
    img = next((n for n in walk(el) if isinstance(n, El) and n.tag == "img"), None)
    cap = next((n for n in walk(el) if isinstance(n, El) and (n.tag == "figcaption" or "caption" in n.classes)), None)
    capt = flat(cap) if cap is not None else (img.attrs.get("alt", "") if img else "")
    f = mk("figure", "fig")
    f.kids.append(img_or_placeholder(img.attrs.get("src") if img else None, text_of(cap) if cap is not None else capt))
    if capt:
        f.kids.append(R("<figcaption>%s</figcaption>" % capt))
    return f


HANDLERS = {
    "glance": h_glance, "materials": h_materials, "timeline": h_timeline,
    "code-figure": h_codefig, "steps": h_steps, "trouble": h_trouble,
    "tip": make_callout("tip"), "warn": make_callout("warn"),
    "safety": make_callout("safety"), "note": make_callout("note"),
    "aside": h_aside, "humor": h_humor, "challenge": h_challenge, "diff": h_diff,
    "discuss": h_discuss, "build": h_build, "component": h_component,
    "cards": h_cards, "card": h_card, "page-break": h_pagebreak,
    "figure": h_figure,
    "table-lessons": h_passclass("table-lessons"),
    "table-glossary": h_passclass("table-glossary"),
    "table-schedule": h_passclass("table-schedule"),
}


def tx(n):
    """Αναδρομικός μετασχηματισμός (πρώτα τα παιδιά)."""
    if not isinstance(n, El):
        return n
    if n.tag == "figure" or (n.tag == "div" and "figure" in n.classes):
        return h_figure(n)  # πριν τα παιδιά: χρειάζεται το αρχικό <img>
    newkids = []
    for k in n.kids:
        if isinstance(k, str) and "___" in k:  # πεδία συμπλήρωσης
            parts = re.split(r"_{3,}", k)
            for i, ptxt in enumerate(parts):
                if ptxt:
                    newkids.append(ptxt)
                if i < len(parts) - 1:
                    newkids.append(R('<span class="fill"></span>'))
        else:
            newkids.append(tx(k))
    n.kids = newkids
    if n.tag == "code" and CHIP_RE.match(text_of(n).strip()):
        return El("span", {"class": "chip"}, n.kids)
    if n.tag == "input" and n.attrs.get("type") == "checkbox":
        return mk("span", "cb on" if "checked" in n.attrs else "cb")
    if n.tag == "li" and any(isinstance(k, El) and k.tag == "span" and "cb" in k.classes for k in n.kids[:1]):
        n.attrs["class"] = (n.attrs.get("class", "") + " task").strip()
    if n.tag == "table":
        STATS["plain_tables"] += 1
        return mk("div", "tbl", [n])
    if n.tag == "div":
        for c in sorted(n.classes):
            if c in HANDLERS and c != "figure":
                out = HANDLERS[c](n)
                PRODUCED.add(id(out))
                return out
    if n.tag == "img" and not img_exists(n.attrs.get("src", "")):
        return placeholder(n.attrs.get("alt", ""), "box inline-ph")
    return n


# ----------------------------------------------------------------------------
# Σελιδοποίηση σε sections, TOC, εξώφυλλο
# ----------------------------------------------------------------------------
DEFAULT_LEVEL_NAMES = {
    "1": "Μόνο micro:bit", "2": "Ένας αισθητήρας, μία έξοδος", "3": "Αισθητήρες και αποφάσεις",
    "4": "Κινητήρες και οχήματα", "5": "Ελεύθερο project",
}


def pandoc(md_path):
    r = subprocess.run(
        ["pandoc", "-f", "markdown+fenced_divs+task_lists+pipe_tables+smart-auto_identifiers",
         "-t", "html5", "--wrap=none", str(md_path)],
        capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("pandoc απέτυχε στο %s:\n%s" % (md_path, r.stderr))
    return r.stdout


def build_sections(nodes):
    secs, cur = [], None
    for n in nodes:
        if isinstance(n, str):
            if not n.strip():
                continue
        if isinstance(n, El) and n.tag == "h1":
            cur = {"h1": n, "body": []}
            secs.append(cur)
        else:
            if cur is None:
                cur = {"h1": None, "body": []}
                secs.append(cur)
            cur["body"].append(n)
    return secs


def wrap_printables(body):
    """## … {.printable} + ό,τι ακολουθεί μέχρι το επόμενο h2 -> ένα section.printable-page."""
    out, cur = [], None
    for n in body:
        if isinstance(n, El) and n.tag == "h2":
            cur = None
            if "printable" in n.classes:
                cur = mk("section", "printable-page", [n])
                out.append(cur)
                continue
        if cur is not None:
            cur.kids.append(n)
        else:
            out.append(n)
    return out


def main():
    src_arg = sys.argv[1] if len(sys.argv) > 1 else "content"
    out_arg = sys.argv[2] if len(sys.argv) > 2 else "dist"
    src = None
    for cand in (Path(src_arg), ROOT / src_arg):
        if cand.is_dir():
            src = cand.resolve()
            break
    if src is None:
        sys.exit("Δεν βρέθηκε ο φάκελος πηγών: %s" % src_arg)
    out_arg_p = Path(out_arg) if Path(out_arg).is_absolute() else Path.cwd() / out_arg
    if out_arg_p.suffix.lower() == ".html":
        out_path, out_dir = out_arg_p, out_arg_p.parent
    else:
        out_dir, out_path = out_arg_p, out_arg_p / "index.html"
    out_dir.mkdir(parents=True, exist_ok=True)
    files = sorted(src.glob("[0-9]*.md"), key=lambda p: p.name)  # STYLE_BRIEF.md etc. δεν είναι κεφάλαια
    if not files:
        sys.exit("Κανένα [0-9]*.md στο %s" % src)

    nodes = []
    for f in files:
        nodes += frag(pandoc(f))
    nodes = [tx(n) for n in nodes]

    # sections ανά h1
    secs = build_sections(nodes)
    toc, uid, parts = [], [0], []
    sec_html = []

    def ensure_id(h):
        if not h.attrs.get("id"):
            uid[0] += 1
            h.attrs["id"] = "s%d" % uid[0]
        return h.attrs["id"]

    for s in secs:
        h1 = s["h1"]
        body = wrap_printables(s["body"])
        if h1 is None:
            sec_html.append("".join(ser(b) for b in body))
            continue
        title = text_of(h1).strip()
        classes = h1.classes
        lvl = h1.a("level")
        kind = "lesson" if "lesson" in classes else "level-intro" if "level-intro" in classes else (
            "part" if re.match(r"^Μέρος\b", title) else "chapter-other")
        if kind == "level-intro" and lvl:
            m = re.match(r"^Επίπεδο\s+\d+\s*[–—-]\s*(.*)$", title)
            if m:
                LEVEL_NAMES[lvl] = m.group(1).strip()
        sc = ["chapter", kind]
        if kind in ("lesson", "level-intro") and lvl:
            sc.append("lv" + lvl)
            h1.attrs["class"] = " ".join(sorted(classes))
        if kind == "lesson":
            m = re.match(r"^Μάθημα\s+([\d.]+)", title)
            h1.attrs["data-label"] = "Μάθημα %s · Επίπεδο %s" % (m.group(1) if m else "", lvl or "")
        hid = ensure_id(h1)
        toc.append((1, hid, title, lvl if kind in ("lesson", "level-intro") else None, kind))
        link_appx = re.match(r"^Παράρτημα\s+[ΕE]\b", title) is not None
        for b in body:
            if isinstance(b, El) and b.tag == "h2":
                hid2 = ensure_id(b)
                if kind != "lesson":
                    toc.append((2, hid2, text_of(b).strip(), None, kind))
        if link_appx:
            for b in body:
                for n in list(walk(b)):
                    if isinstance(n, El) and n.tag == "li":
                        a = next((k for k in n.kids if isinstance(k, El) and k.tag == "a"), None)
                        if a is not None and a.attrs.get("href", "").startswith("http"):
                            qr = qr_svg(a.attrs["href"], "qr qr-s")
                            if qr is not None:
                                n.attrs["class"] = "link-item"
                                n.kids = [mk("div", "li-text", n.kids), mk("div", "li-qr", [qr])]
        attrs = {"class": " ".join(sc)}
        if lvl and kind in ("lesson", "level-intro"):
            attrs["data-level"] = lvl
        sec = El("section", attrs, [h1] + body)
        sec_html.append(ser(sec))

    # TOC
    items = []
    for lev, hid, txt, lvl, kind in toc:
        dot = '<i class="tdot lv%s"></i>' % lvl if lvl else ""
        items.append('<li class="toc%d %s"><a href="#%s">%s%s</a></li>' % (lev, kind, hid, dot, esc(txt)))
    toc_html = '<ul class="toc-list">%s</ul>' % "".join(items)

    band = ""
    for i in "12345":
        band += '<div class="seg s%s"><span class="n">%s</span><span class="t">%s</span></div>' % (
            i, i, esc(LEVEL_NAMES.get(i, DEFAULT_LEVEL_NAMES[i])))

    tokens = (DESIGN / "tokens.css").read_text(encoding="utf-8")
    if not list((VENDOR_DIR / "fonts").glob("*.woff*")):  # δεν υπάρχουν τοπικά αρχεία: Google Fonts
        tokens = re.sub(r"@font-face\{.*?\}\s*", "", tokens, flags=re.S)
    printcss = (DESIGN / "print.css").read_text(encoding="utf-8")
    page_rules = ""
    for i in range(1, 6):
        page_rules += (
            "@page level-%d{@top-right-corner{content:\"\";background:linear-gradient(to left,var(--l%d) 6mm,transparent 6mm)}"
            "@right-middle{content:\"\";background:linear-gradient(to left,var(--l%d) 6mm,transparent 6mm)}"
            "@bottom-right-corner{content:\"\";background:linear-gradient(to left,var(--l%d) 6mm,transparent 6mm)}}\n"
            ".chapter.lv%d{page:level-%d}\n" % (i, i, i, i, i, i))
    page_rules += (
        "@page part{@top-right-corner{content:\"\";background:linear-gradient(to left,var(--note) 6mm,transparent 6mm)}"
        "@right-middle{content:\"\";background:linear-gradient(to left,var(--note) 6mm,transparent 6mm)}"
        "@bottom-right-corner{content:\"\";background:linear-gradient(to left,var(--note) 6mm,transparent 6mm)}}\n"
        ".chapter.part{page:part}\n")

    tpl = (DESIGN / "template.html").read_text(encoding="utf-8")
    doc = (tpl.replace("{{TOKENS_CSS}}", tokens).replace("{{PRINT_CSS}}", printcss)
           .replace("{{PAGE_RULES}}", page_rules).replace("{{LEVEL_BAND}}", band)
           .replace("{{VERSION}}", get_version()).replace("{{TOC}}", toc_html).replace("{{BODY}}", "\n".join(sec_html)))
    out_path.write_text(doc, encoding="utf-8")
    if IMG_DIR.is_dir():
        shutil.copytree(IMG_DIR, out_dir / "img", dirs_exist_ok=True)
    if VENDOR_DIR.is_dir():
        shutil.copytree(VENDOR_DIR, out_dir / "assets" / "vendor", dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(".gitkeep"))

    print("Πηγές: %d αρχεία από %s" % (len(files), src))
    print("Έκδοση: %s" % get_version())
    print("Γράφτηκε %s (%d KB)" % (out_path, out_path.stat().st_size // 1024))
    print("Sections: %d · TOC: %d εγγραφές (placeholders αριθμών σελίδας) · εικόνες-placeholder: %d · "
          "πίνακες (όχι κάρτες): %d · QR fallback σε URL: %d" % (
              len(secs), len(toc), STATS["placeholders"], STATS["plain_tables"], STATS["qr_fallback"]))
    left = sum(1 for b in nodes for n in walk(b) if isinstance(n, El) and n.tag == "div"
               and (n.classes & set(HANDLERS)) and id(n) not in PRODUCED and "tbl" not in n.classes
               and not (n.classes & {"table-lessons", "table-glossary", "table-schedule"}))
    left += doc.count('<div class="glance"')
    print("Μη μετασχηματισμένα components: %d" % left)


if __name__ == "__main__":
    main()
