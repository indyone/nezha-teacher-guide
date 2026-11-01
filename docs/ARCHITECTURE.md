# Αρχιτεκτονική: από markdown σε PDF

```
content/*.md ──pandoc──► HTML fragments ──tools/build.py──► dist/index.html ──Paged.js (browser)──► PDF
   (components)            (fenced divs → <div class>)      (components, TOC, QR,        (σελιδοποίηση A4)
                                                              template + CSS inline)
```

## 1. Πηγή: `content/*.md`
Pandoc markdown με *fenced divs* (`::: {.timeline}` κ.ά.). Τα αρχεία διαβάζονται ταξινομημένα κατά όνομα (`10-…`, `20-…`). Η σύνταξη ορίζεται στο
[`design/COMPONENT_SPEC.md`](../design/COMPONENT_SPEC.md). Ύφος: [`content/STYLE_BRIEF.md`](../content/STYLE_BRIEF.md).

## 2. Pandoc
Το `build.py` καλεί `pandoc` (2.x) ανά αρχείο και παίρνει HTML όπου κάθε fenced div είναι `<div class="…" data-…>`. Οι πίνακες και οι εικόνες περνούν ως έχουν.

## 3. `tools/build.py`
- Διαβάζει το HTML με μικρό DOM parser (μόνο stdlib) και εφαρμόζει *handlers* ανά class: κάρτα «με μια ματιά», χρονογραμμή, κάρτες θυρών/εξαρτημάτων, πλαίσια, διαφοροποίηση κ.ά.
- Χτίζει sections ανά `#` (Μέρος / Μάθημα / Παράρτημα), TOC με placeholders αριθμών σελίδας, QR σε SVG για συνδέσμους, ονομασμένες σελίδες ανά επίπεδο (χρωματική ταινία στο περιθώριο).
- Εικόνες: `img/x.jpg` → `assets/img/x.jpg`. Αν λείπει, βγαίνει διακεκομμένο placeholder με τη λεζάντα.
- Βάζει τα `design/tokens.css`, `design/print.css` και τα παραγόμενα `@page` rules μέσα στο `design/template.html` και γράφει `dist/index.html`. Αντιγράφει `assets/img` → `dist/img` και `assets/vendor` → `dist/assets/vendor`, ώστε το `dist/` να είναι αυτόνομο.
- Έκδοση: το `VERSION`, αλλιώς το τελευταίο git tag (μπαίνει σε εξώφυλλο, υποσέλιδο και `<meta name="generator">`· το `make-pdf.sh` τη χρησιμοποιεί και στο όνομα του PDF).
- Στο τέλος τυπώνει στατιστικά και «Μη μετασχηματισμένα components: N» (πρέπει 0· ελέγχεται από `make check`).

## 4. Paged.js → PDF
Το `template.html` φορτώνει πρώτα το `assets/vendor/paged.polyfill.js` και, αν λείπει, μία αλυσίδα CDN (unpkg → jsDelivr → cdnjs). Το `PagedConfig.auto=false`
ώστε η σελιδοποίηση να ξεκινά αφού φορτώσουν οι γραμματοσειρές. Οι γραμματοσειρές ορίζονται με `@font-face` σε τοπικά αρχεία `assets/vendor/fonts/` (αν λείπουν, το build αφαιρεί τα
`@font-face` και μένει το Google Fonts `<link>`). Το PDF παράγεται από `tools/make-pdf.sh`: Playwright chromium → τοπικό Chrome headless → οδηγίες για χειροκίνητη εκτύπωση.

## 5. Εκδόσεις και CI
- `.github/workflows/build.yml`: σε push/PR χτίζει `assets → check → html → pdf` και ανεβάζει το `dist/` ως artifact.
- `.github/workflows/release-please.yml`: ανοίγει Release PR από τα Conventional Commits· στο release χτίζει και επισυνάπτει PDF/HTML στο GitHub Release.
- `make changelog` (git-cliff, προαιρετικό) δείχνει τι θα μπει στην επόμενη έκδοση, χωρίς να γράψει το `CHANGELOG.md`. Στο «Ιστορικό εκδόσεων» μπαίνουν μόνο `feat`/`fix` (και `feat(assets)`)· τα υπόλοιπα types μένουν έξω και στο release-please.

## Πού είναι τι
Τοπικό build: `make assets && make html && make pdf`. Αλλαγή εμφάνισης: `design/`. Νέο component: handler στο `tools/build.py` + CSS στο `design/print.css` + περιγραφή στο `COMPONENT_SPEC.md`.
