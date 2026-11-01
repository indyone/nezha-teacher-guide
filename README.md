# Οδηγός Δασκάλου – Ρομποτική & STEM με το Nezha Inventor's Kit

![Άδεια περιεχομένου: CC BY-SA 4.0](https://img.shields.io/badge/content-CC%20BY--SA%204.0-lightgrey.svg)
![Άδεια κώδικα: MIT](https://img.shields.io/badge/code-MIT-blue.svg)
![Έκδοση](https://img.shields.io/badge/version-0.0.0%20draft-orange.svg)

Ένας οδηγός για δασκάλους δημοτικού χωρίς καμία εμπειρία προγραμματισμού: 5 κεφάλαια, 16 μαθήματα σε 5 επίπεδα δυσκολίας,
με το micro:bit V2, την πλακέτα Nezha V1 και το MakeCode. Το κείμενο γράφεται σε markdown (`content/`), μετατρέπεται σε HTML
και σελιδοποιείται σε PDF A4 με Paged.js.

## Γρήγορη εκκίνηση

Απαιτούνται `git`, `python3` (3.9+), `pandoc` 2.x και, για γραμματοσειρές/PDF, Node 20+.

```bash
git clone <url-του-repo> nezha-teacher-guide && cd nezha-teacher-guide
make assets      # γραμματοσειρές + Paged.js στο assets/vendor/ (μία φορά, χρειάζεται internet)
make html        # content/*.md -> dist/index.html
open dist/index.html   # (Linux: xdg-open) — περίμενε να τελειώσει η σελιδοποίηση
make pdf         # dist/odigos-daskalou-<έκδοση>.pdf (Playwright ή τοπικό Chrome)
```

Αν δεν τρέξεις `make assets`, το HTML δουλεύει με CDN (Paged.js, Google Fonts) όταν υπάρχει internet.
Άλλοι στόχοι: `make check` (έλεγχος πριν από commit), `make version`, `make changelog`, `make clean`.

### Χειροκίνητο PDF από τον browser
Άνοιξε το `dist/index.html` στο Chrome, περίμενε τη σελιδοποίηση, Cmd/Ctrl+P → «Αποθήκευση ως PDF» → A4 → Περιθώρια: Κανένα →
ενεργά τα «Γραφικά παρασκηνίου», ανενεργές οι κεφαλίδες/υποσέλιδα.

### Εικόνες
Οι φωτογραφίες βρίσκονται στο `assets/img/` και στο markdown γράφονται ως `img/<όνομα>.jpg`. Όσες λείπουν εμφανίζονται ως
διακεκομμένο πλαίσιο με τη λεζάντα. Νέες φωτογραφίες περνούν από `python3 tools/process-photos.py <raw-dir> assets/img/ --name <slug>`
(αυτόματη περιστροφή, διόρθωση, αφαίρεση EXIF). Τα raw αρχεία δεν μπαίνουν στο repo.

## Χάρτης φακέλων

| Φάκελος / αρχείο | Τι είναι |
|---|---|
| `content/` | Η μοναδική πηγή αλήθειας: markdown σε σύνταξη components + `STYLE_BRIEF.md` |
| `design/` | `tokens.css`, `print.css`, `template.html`, `DESIGN_SYSTEM.md`, `COMPONENT_SPEC.md` |
| `tools/` | `build.py`, `fetch-assets.sh`, `make-pdf.sh`, `process-photos.py` |
| `assets/img/` | Επεξεργασμένες φωτογραφίες (χωρίς EXIF) |
| `assets/vendor/` | Γραμματοσειρές και Paged.js (γεμίζει με `make assets`, δεν γίνεται commit) |
| `docs/` | Πλάνο, έρευνα, αποφάσεις, `ARCHITECTURE.md`, `CONTENT_GUIDE.md` |
| `dist/` | Αποτέλεσμα του build (στο `.gitignore`) |
| `AGENTS.md` | Οδηγίες για AI agents |

## Εκδόσεις

- [Semantic Versioning](https://semver.org/lang/el/). **v0.0.0 = πρόχειρο (draft)**, **1.0.0 = η πρώτη τελική έκδοση**.
  Πριν το 1.0.0 τα `feat` ανεβάζουν το δεύτερο ψηφίο μόνο όπου χρειάζεται και τα `fix` το τρίτο· ρυθμίζεται στο `release-please-config.json`.
- Το [release-please](https://github.com/googleapis/release-please) ανοίγει αυτόματα Release PR με νέο `CHANGELOG.md` και νέο `VERSION`·
  με το merge δημιουργείται tag και GitHub Release με το PDF και το HTML.
- Η έκδοση που εμφανίζεται στο build είναι το `git describe --tags --always`, αλλιώς το αρχείο `VERSION`.

### Conventional Commits

Μορφή: `type(scope): περιγραφή` (Ελληνικά ή Αγγλικά, σώμα προαιρετικό).

| scope | Τι αλλάζει | Παράδειγμα |
|---|---|---|
| `content` | κείμενο μαθημάτων/κεφαλαίων | `feat(content): μάθημα 3.2 – Σύστημα συναγερμού` |
| `design` | CSS, template, design system | `fix(design): διόρθωση σπασίματος κάρτας στο τέλος σελίδας` |
| `build` | `tools/`, Makefile, CI | `build: ανίχνευση Chrome σε macOS στο make-pdf` |
| `docs` | `docs/`, README, AGENTS | `docs: ενημέρωση ανοιχτών σημείων` |
| `assets` | φωτογραφίες, γραμματοσειρές | `chore(assets): φωτογραφία αισθητήρα απόστασης` |

Types: `feat`, `fix`, `docs`, `build`, `chore`, `perf`, `refactor`. Breaking change: `!` μετά το scope ή `BREAKING CHANGE:` στο σώμα.

## Πώς συνεισφέρεις

1. Άνοιξε issue ή πρότεινε αλλαγή· για αλλαγές δομής (επίπεδα, κλίμακες δυσκολίας, τίτλος, άδειες) χρειάζεται απόφαση του συντηρητή.
2. Δημιούργησε branch, γράψε στα `content/*.md` με τη σύνταξη του [`design/COMPONENT_SPEC.md`](design/COMPONENT_SPEC.md) και τους κανόνες του
   [`content/STYLE_BRIEF.md`](content/STYLE_BRIEF.md). Οδηγός βήμα-βήμα: [`docs/CONTENT_GUIDE.md`](docs/CONTENT_GUIDE.md).
3. Τρέξε `make check` και δες το `dist/index.html`.
4. Commit με Conventional Commits, άνοιξε Pull Request. Το CI χτίζει HTML και PDF.

Δεν επεξεργαζόμαστε ποτέ το `dist/`. Φωτογραφίες: μόνο επεξεργασμένες, χωρίς EXIF και χωρίς πρόσωπα παιδιών.

## Άδειες και credits

- Περιεχόμενο (`content/`, `docs/`, `assets/`): [CC BY-SA 4.0](LICENSE-CONTENT.md).
- Κώδικας (`tools/`, `Makefile`, `.github/`, CSS/HTML του `design/`): [MIT](LICENSE).
- Γραμματοσειρές Commissioner, Source Sans 3, JetBrains Mono (SIL OFL 1.1, μέσω [fontsource](https://fontsource.org)) και [Paged.js](https://pagedjs.org) (MIT): κατεβαίνουν με `make assets`.
- Το υλικό βασίζεται στο kit Nezha Inventor's Kit της ELECFREAKS και στο MakeCode της Microsoft· τα ονόματα ανήκουν στους κατόχους τους.
- Συντελεστές: [CONTRIBUTORS.md](CONTRIBUTORS.md). Ιστορικό αλλαγών: [CHANGELOG.md](CHANGELOG.md).
