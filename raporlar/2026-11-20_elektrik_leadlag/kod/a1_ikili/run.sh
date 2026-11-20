#!/usr/bin/env bash
# A1 (hisse -> hisse ikili öncülük) — baştan sona. Kullanım: bash run.sh <panel_is klasörü>
# KÖR PROTOKOL: yalnız panel_is verilir (son tarih 2022-12-30); betikler daha uzun paneli reddeder.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PANEL="${1:?kullanım: bash run.sh <panel_is klasörü>}"
OUT="$HERE/out"; mkdir -p "$OUT"
python3 -I "$HERE/scan.py"  "$PANEL" "$OUT" > "$OUT/scan_log.txt"      # T1/T2 taraması, BH, sıfır dağılımı, kalıcılık, hipotezler
python3 -I "$HERE/grid.py"  "$PANEL" "$OUT" "$HERE/../../ek/a1_ikili_sonuc.csv" > "$OUT/grid_log.txt"   # kural ızgarası (elib.evaluate) + öz-denetim
python3 -I "$HERE/check.py" "$PANEL" "$OUT" > "$OUT/check_log.txt"     # aday kurallar için ek denetimler
tail -n 6 "$OUT/grid_log.txt"
