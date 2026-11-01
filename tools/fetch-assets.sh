#!/usr/bin/env bash
# Κατεβάζει (μέσω npm) τις γραμματοσειρές και το Paged.js στο assets/vendor/.
# Idempotent: ό,τι υπάρχει ήδη δεν ξανακατεβαίνει. Απαιτεί node/npm και internet.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR="$ROOT/assets/vendor"
FONTS="$VENDOR/fonts"
PAGEDJS_VERSION="0.4.3"
mkdir -p "$FONTS"

if ! command -v npm >/dev/null 2>&1; then
  echo "Δεν βρέθηκε το npm. Εγκατάστησε Node 20+ (https://nodejs.org) και ξανατρέξε." >&2
  exit 1
fi

# πακέτο | αρχεία (χωρίς subset/επέκταση): weight-style
FONT_SPECS=(
  "commissioner|600-normal 800-normal"
  "source-sans-3|400-normal 400-italic 600-normal"
  "jetbrains-mono|400-normal"
)
SUBSETS="greek latin"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
fetched=0; skipped=0

for spec in "${FONT_SPECS[@]}"; do
  pkg="${spec%%|*}"; variants="${spec#*|}"
  need=0
  for v in $variants; do for s in $SUBSETS; do
    [[ -f "$FONTS/$pkg-$s-$v.woff2" ]] || need=1
  done; done
  if [[ $need -eq 0 ]]; then
    echo "= @fontsource/$pkg: υπάρχει ήδη"; skipped=$((skipped+1)); continue
  fi
  echo "+ @fontsource/$pkg: λήψη..."
  (cd "$TMP" && npm pack "@fontsource/$pkg" --silent >/dev/null && mkdir -p "x-$pkg" && tar -xzf fontsource-"$pkg"-*.tgz -C "x-$pkg")
  for v in $variants; do for s in $SUBSETS; do
    for ext in woff2 woff; do
      f="$TMP/x-$pkg/package/files/$pkg-$s-$v.$ext"
      if [[ -f "$f" ]]; then cp "$f" "$FONTS/"; else echo "  ! λείπει $pkg-$s-$v.$ext" >&2; fi
    done
  done; done
  fetched=$((fetched+1))
done

if [[ -f "$VENDOR/paged.polyfill.js" ]]; then
  echo "= pagedjs: υπάρχει ήδη"; skipped=$((skipped+1))
else
  echo "+ pagedjs@$PAGEDJS_VERSION: λήψη..."
  (cd "$TMP" && npm pack "pagedjs@$PAGEDJS_VERSION" --silent >/dev/null && mkdir -p x-pagedjs && tar -xzf pagedjs-*.tgz -C x-pagedjs)
  cp "$TMP/x-pagedjs/package/dist/paged.polyfill.js" "$VENDOR/paged.polyfill.js"
  fetched=$((fetched+1))
fi

echo "Τέλος: $fetched πακέτα κατέβηκαν, $skipped υπήρχαν ήδη. Αρχεία στο assets/vendor/:"
ls -1 "$VENDOR" "$FONTS" | sed 's/^/  /'
