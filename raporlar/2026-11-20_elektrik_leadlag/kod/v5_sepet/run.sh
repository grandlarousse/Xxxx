#!/usr/bin/env bash
# V5 — sektör sepeti uygulama betimlemesi. Kullanım: ./run.sh <panel_full> [ek_klasoru]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PANEL="${1:?panel_full klasörü gerekli}"
EK="${2:-$HERE/../../ek}"
python3 -I "$HERE/v5.py" "$PANEL" "$EK"
python3 -I "$HERE/ozet.py" "$EK/v5_sepet.csv"
