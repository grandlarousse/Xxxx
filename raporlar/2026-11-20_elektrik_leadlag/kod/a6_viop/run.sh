#!/usr/bin/env bash
# A6 (VİOP) — baştan sona. Kullanım: bash run.sh <panel_is klasörü>   (yalnız IS paneli; kör protokol)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PANEL="${1:?panel_is klasörü gerekli}"
EK="$(cd "$HERE/../../ek" && pwd)"
python3 -I "$HERE/01_betimle.py" "$PANEL" "$EK/a6_viop_likidite.csv" > "$HERE/_betimle.txt"
python3 -I "$HERE/02_tara.py" "$PANEL" "$EK/a6_viop_sonuc.csv" | tee "$HERE/_tarama.txt"
python3 -I "$HERE/03_tanilar.py" "$PANEL" > /dev/null
python3 -I "$HERE/04_ozdenetim.py" "$PANEL" | tee "$HERE/_ozdenetim.txt"
