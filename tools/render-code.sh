#!/usr/bin/env bash
# tools/code/*.ts -> assets/img/code-*.png μέσω του MakeCode (θέλει internet)
# Χρήση: bash tools/render-code.sh [code-2-1 ...]
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
command -v npm >/dev/null 2>&1 && command -v node >/dev/null 2>&1 \
  || { echo "Χρειάζονται node και npm (https://nodejs.org)." >&2; exit 1; }

# το playwright σε προσωρινό φάκελο, όπως στο make-pdf
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
(cd "$WORK" && npm init -y >/dev/null 2>&1 && npm install playwright --silent >/dev/null 2>&1 \
      && npx playwright install chromium >/dev/null 2>&1) \
  || { echo "Το playwright δεν εγκαταστάθηκε." >&2; exit 1; }

echo "Εικόνες κώδικα από το MakeCode:"
NODE_PATH="$WORK/node_modules" node "$ROOT/tools/render-code.js" "$@"
