#!/usr/bin/env bash
# A8 birleşik model — baştan sona: tarama (IS) → tanı/keşif → öz-denetim + sonuç CSV'si.
# Kullanım: bash run.sh <panel_is klasörü> [çıktı_csv]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PANEL="${1:?kullanım: run.sh <panel_is klasörü> [çıktı_csv]}"
CSV="${2:-$HERE/../../ek/a8_model_sonuc.csv}"
mkdir -p "$HERE/out"
python3 -I "$HERE/scan.py" "$PANEL" > "$HERE/out/scan_log.txt" 2>&1
python3 -I "$HERE/diag.py" "$PANEL" > "$HERE/out/diag_log.txt" 2>&1
python3 -I "$HERE/final.py" "$PANEL" "$CSV"
