#!/usr/bin/env bash
# A7 — gün içi zamanlama ve dolum doğrulaması (aday üretmez; T3 bulguları "keşif").
# Kullanım: bash run.sh <panel_klasoru> [ek_klasoru]
#   T1 → ek/a7_vekil_tablosu.csv      (17:30 / 18:00 / 17:50 vekili: korelasyon, kesinlik, yakalama)
#   T2 → ek/a7_kapanis_sapma.csv, a7_kilit_gecis.csv, a7_kilit_riski.csv, a7_kapanis_hacim.csv
#   T3 → ek/a7_kesif.csv              (keşif)
#   araç sınaması → ek/a7_vekil_ornek.csv (örnek kurallar, yalnız örtüşme: --kor)
# 3. dalga için: python3 -I vekil.py <panel_full> ../<ajan>/rules.py --bas 2025-07-01 --cikti <csv>
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PANEL="${1:?panel klasörü gerekli (ör. .../panel_dev)}"
EK="${2:-$HERE/../../ek}"
python3 -I "$HERE/t1_vekil_tablosu.py" "$PANEL" "$EK/a7_vekil_tablosu.csv"
python3 -I "$HERE/t2_kapanis.py" "$PANEL" "$EK"
python3 -I "$HERE/t3_kesif.py" "$PANEL" "$EK/a7_kesif.csv"
python3 -I "$HERE/vekil.py" "$PANEL" "$HERE/ornek_rules.py" --kor --cikti "$EK/a7_vekil_ornek.csv"
python3 -I "$HERE/vekil.py" "$PANEL" "$HERE/ornek_rules.py" --kor --nokta p_close --hacim-payi 1   # öz-denetim: hepsi 1,0 olmalı
