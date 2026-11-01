#!/usr/bin/env bash
# dist/index.html -> dist/odigos-daskalou-<έκδοση>.pdf
# Σειρά προσπαθειών: 1) npx playwright (chromium)  2) τοπικό Chrome/Chromium headless  3) οδηγίες.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
HTML="$ROOT/dist/index.html"
[[ -f "$HTML" ]] || { echo "Λείπει το dist/index.html — τρέξε πρώτα: make html" >&2; exit 1; }
# ίδια έκδοση με εξώφυλλο/υποσέλιδο (build.py): αρχείο VERSION, αλλιώς το τελευταίο git tag
VER="$(tr -d '[:space:]' < VERSION 2>/dev/null | sed 's/^v//')"
[[ -n "$VER" ]] || VER="$(git describe --tags --abbrev=0 2>/dev/null | sed 's/^v//')"
OUT="$ROOT/dist/odigos-daskalou-$VER.pdf"
URL="file://$HTML"

# 1) Playwright: περιμένει το Paged.js (έχει προσθέσει .pagedjs_pages) και τυπώνει με τα @page του CSS
if command -v npm >/dev/null 2>&1 && command -v node >/dev/null 2>&1; then
  echo "[1/3] Προσπάθεια με Playwright chromium..."
  WORK="$(mktemp -d)"
  cat > "$WORK/pdf.js" <<'JS'
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto(process.env.PDF_URL, { waitUntil: 'networkidle' });
  await p.waitForSelector('.pagedjs_pages', { timeout: 180000 });
  await p.waitForTimeout(2000);
  await p.pdf({ path: process.env.PDF_OUT, preferCSSPageSize: true, printBackground: true });
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
JS
  if (cd "$WORK" && npm init -y >/dev/null 2>&1 && npm install playwright --silent >/dev/null 2>&1 \
        && npx playwright install chromium >/dev/null 2>&1 \
        && PDF_URL="$URL" PDF_OUT="$OUT" node pdf.js) && [[ -s "$OUT" ]]; then
    rm -rf "$WORK"; echo "OK (playwright): $OUT"; exit 0
  fi
  rm -rf "$WORK"
  echo "  Το Playwright δεν δούλεψε, συνεχίζω..."
fi

# 2) Τοπικό Chrome/Chromium
for c in "google-chrome" "google-chrome-stable" "chromium" "chromium-browser" \
         "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
         "/Applications/Chromium.app/Contents/MacOS/Chromium" \
         "/c/Program Files/Google/Chrome/Application/chrome.exe"; do
  if command -v "$c" >/dev/null 2>&1 || [[ -x "$c" ]]; then
    echo "[2/3] Chrome headless: $c"
    if "$c" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=60000 \
            --run-all-compositor-stages-before-draw --print-to-pdf="$OUT" "$URL" >/dev/null 2>&1 && [[ -s "$OUT" ]]; then
      echo "OK (chrome): $OUT"; exit 0
    fi
  fi
done

# 3) Οδηγίες
cat <<MSG
[3/3] Δεν βρέθηκε Playwright ή Chrome/Chromium. Κάνε το PDF χειροκίνητα:
  1. Άνοιξε το dist/index.html στο Chrome (χρειάζεται internet ή τρέξε πρώτα: make assets).
  2. Περίμενε να τελειώσει η σελιδοποίηση (σελίδες A4 + αριθμοί στα Περιεχόμενα).
  3. Cmd/Ctrl+P → «Αποθήκευση ως PDF» → A4 → Περιθώρια: Κανένα → «Γραφικά παρασκηνίου» ΕΝΕΡΓΑ,
     κεφαλίδες/υποσέλιδα ΑΝΕΝΕΡΓΑ.
  4. Αποθήκευση ως dist/odigos-daskalou-$VER.pdf
MSG
exit 2
