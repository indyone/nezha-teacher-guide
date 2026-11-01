#!/bin/sh
# Επαναδημιουργία όλων των φωτογραφιών από φάκελο raw (εκτός repo, π.χ. photos_raw/).
# Χρήση: sh tools/process-all.sh [raw-dir] [map-file]
#   raw-dir  default: photos_raw   (gitignored)
#   map-file default: tools/photo-map.txt  (μορφή: δες την κεφαλίδα του αρχείου)
set -e
R=${1:-photos_raw}; M=${2:-tools/photo-map.txt}; O=assets/img
[ -f "$M" ] || { echo "Λείπει ο χάρτης $M" >&2; exit 1; }
[ -d "$R" ] || { echo "Λείπει ο φάκελος $R" >&2; exit 1; }
python3 -I - "$R" "$M" "$O" <<'PY'
import shlex, subprocess, sys
R, M, O = sys.argv[1:4]
n = 0
for no, line in enumerate(open(M, encoding="utf-8"), 1):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    f = shlex.split(line)
    if len(f) < 3 or f[2] not in ("component", "board", "wide"):
        sys.exit("%s:%d: αναμένεται <raw> <target> <component|board|wide> [επιλογές]" % (M, no))
    raw, target, kind, rest = f[0], f[1], f[2], f[3:]
    subprocess.run(["python3", "tools/process-photos.py", "%s/%s" % (R, raw), "%s/%s.jpg" % (O, target),
                    "--kind", kind] + rest, check=True)
    n += 1
print("Επεξεργάστηκαν %d φωτογραφίες" % n)
PY
