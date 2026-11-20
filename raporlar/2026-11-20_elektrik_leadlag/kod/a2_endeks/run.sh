#!/usr/bin/env bash
# A2 (endeks <-> hisse) — baştan sona. Kullanım: bash run.sh <panel_is klasörü>
# KÖR PROTOKOL: yalnız IS paneli (son tarih 2022-12-30) verilir; betikler daha uzun paneli reddeder.
set -euo pipefail
PANEL=${1:?kullanım: bash run.sh <panel_is klasörü>}
HERE=$(cd "$(dirname "$0")" && pwd)
OUT="$HERE/out"; EK="$HERE/../../ek"
mkdir -p "$OUT"
python3 -I "$HERE/scan.py" "$PANEL" "$OUT"                        # önceden yazılı ızgara (T1–T4, bayat fiyat)
python3 -I "$HERE/checks.py" "$PANEL" "$OUT" | tee "$OUT/checks.txt"   # yer değiştirme, örtüşme, keşif
python3 -I "$HERE/secim.py" "$PANEL" "$OUT" "$EK" | tee "$OUT/secim.txt" # seçim etiketleri, dondurulmuş kurallar, öz-denetim
