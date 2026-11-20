#!/bin/bash
# A5 — XELKT/XU030 rotasyonu: baştan sona. Kullanım: bash run.sh <panel_is klasörü> [ek klasörü]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PANEL="${1:?panel_is klasörü gerekli}"
EK="${2:-$HERE/../../ek}"
python3 -I "$HERE/tara.py"  "$PANEL" "$EK/a5_rotasyon_sonuc.csv"          # ızgara taraması + seçim + öz-denetim
python3 -I "$HERE/kesif.py" "$PANEL" "$EK/a5_rotasyon_otokor.csv" tani    # otokorelasyon tablosu + tanılar
python3 -I "$HERE/aile.py"  "$PANEL" "$EK/a5_rotasyon_sonuc.csv"          # BH, aile düzeyi kaydırma testi, vadeli / XU030 korumalı
