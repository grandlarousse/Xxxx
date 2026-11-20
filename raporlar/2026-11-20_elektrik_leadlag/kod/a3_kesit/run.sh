#!/usr/bin/env bash
# A3 kesit ailesi — baştan sona. Kullanım: bash run.sh <panel_is klasörü> [ara çıktı klasörü]
# Yalnız IS paneliyle çalıştırılır (kör protokol). Çıktılar: ../../ek/a3_kesit_sonuc.csv, a3_kesit_regresyon.csv, a3_kesit_tanilama.txt
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PANEL="${1:?kullanım: run.sh <panel_is klasörü> [ara çıktı klasörü]}"
OUT="${2:-${TMPDIR:-/tmp}/a3_kesit_out}"
EK="$(cd "$HERE/../../ek" && pwd)"
mkdir -p "$OUT"
python3 -I -W ignore "$HERE/scan.py" "$PANEL" "$OUT"
python3 -I -W ignore "$HERE/scan2.py" "$PANEL" "$OUT" > "$OUT/scan2.log"
python3 -I -W ignore "$HERE/finalize.py" "$PANEL" "$OUT" "$EK"
