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

# 1) Playwright: περιμένει να τελειώσει το Paged.js (data-paged="done" από το template) και τυπώνει με τα @page του CSS
if command -v npm >/dev/null 2>&1 && command -v node >/dev/null 2>&1; then
  echo "[1/3] Προσπάθεια με Playwright chromium..."
  WORK="$(mktemp -d)"
  cat > "$WORK/pdf.js" <<'JS'
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto(process.env.PDF_URL, { waitUntil: 'networkidle' });
  // όχι απλώς .pagedjs_pages: αυτό εμφανίζεται στην αρχή της σελιδοποίησης και το PDF έβγαινε κομμένο
  try {
    await p.waitForFunction(() => ['done', 'error'].includes(document.documentElement.dataset.paged), null, { timeout: 180000 });
  } catch (e) { console.error('  Η σελιδοποίηση δεν τελείωσε σε 3 λεπτά.'); process.exit(3); }
  if (await p.evaluate(() => document.documentElement.dataset.paged) !== 'done') {
    console.error('  Το Paged.js απέτυχε· άνοιξε το dist/index.html και δες την κονσόλα του browser.'); process.exit(3);
  }
  await p.waitForTimeout(500);
  const pages = await p.evaluate(() => document.querySelectorAll('.pagedjs_page').length);
  console.log('  σελίδες: ' + pages);
  await p.pdf({ path: process.env.PDF_OUT, preferCSSPageSize: true, printBackground: true });
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
JS
  (cd "$WORK" && npm init -y >/dev/null 2>&1 && npm install playwright --silent >/dev/null 2>&1 \
        && npx playwright install chromium >/dev/null 2>&1 \
        && PDF_URL="$URL" PDF_OUT="$OUT" node pdf.js); rc=$?
  rm -rf "$WORK"
  if [[ $rc -eq 0 && -s "$OUT" ]]; then echo "OK (playwright): $OUT"; exit 0; fi
  # 3 = η σελιδοποίηση απέτυχε ή δεν τελείωσε: σταματάμε αντί να βγει μισό PDF από άλλη μέθοδο
  if [[ $rc -eq 3 ]]; then rm -f "$OUT"; echo "ΑΠΟΤΥΧΙΑ: δεν βγήκε PDF." >&2; exit 3; fi
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
