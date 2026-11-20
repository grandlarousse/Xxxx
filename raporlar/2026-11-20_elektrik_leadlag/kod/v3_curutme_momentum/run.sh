#!/bin/bash
# V3 — çürütme: S1 (A5_zirve20_sepet_h3) ve S2 (A2_xelkt_z1_tum_h3). Kullanım: bash run.sh <panel_full klasörü> [ek klasörü]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PANEL="${1:?panel_full klasörü gerekli}"
EK="${2:-$HERE/../../ek}"
python3 -I "$HERE/v3.py" "$PANEL" "$EK/v3_curutme_momentum.csv" "$EK/a7_kapanis_hacim.csv"
