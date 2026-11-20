#!/usr/bin/env bash
# A4 (olaylar): tarama -> seçim/not -> öz-denetim.  Kullanım: bash run.sh <panel_is klasörü> [çıktı csv]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PANEL="${1:?panel_is klasörü gerekli}"
OUT="${2:-$HERE/../../ek/a4_olay_sonuc.csv}"
TMP="$(mktemp -d)"
python3 -I "$HERE/scan.py" "$PANEL" "$TMP/scan.csv" > "$TMP/scan.log"
tail -1 "$TMP/scan.log"
python3 -I "$HERE/finalize.py" "$PANEL" "$TMP/scan.csv" "$OUT"
rm -rf "$TMP"
