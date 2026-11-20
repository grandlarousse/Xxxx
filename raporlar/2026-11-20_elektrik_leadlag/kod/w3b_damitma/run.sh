#!/usr/bin/env bash
# W3-B damıtma — baştan sona: A8 üst dilim tanısı → sıralama taraması → adaylar → dondurulmuş kurallar + CSV.
# Kullanım: bash run.sh <panel_dev klasörü> [çıktı_csv]     (panel_full / raw / kasa verisi KULLANILMAZ)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PANEL="${1:?kullanım: run.sh <panel_dev klasörü> [çıktı_csv]}"
CSV="${2:-$HERE/../../ek/w3b_damitma_sonuc.csv}"
mkdir -p "$HERE/out"
python3 -I "$HERE/s1_tani.py" "$PANEL" > "$HERE/out/s1_log.txt" 2>&1
python3 -I "$HERE/s2_tarama.py" "$PANEL" > "$HERE/out/s2_log.txt" 2>&1
python3 -I "$HERE/s3_aday.py" "$PANEL" > "$HERE/out/s3_log.txt" 2>&1
python3 -I "$HERE/s4_son.py" "$PANEL" "$CSV" 2>&1 | tee "$HERE/out/s4_log.txt"
