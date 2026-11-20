#!/bin/bash
# D1 bastan sona: bash run.sh <VERI_KLASORU> [SON_TARIH=2026-11-20] [DEV_KESIM=2025-06-30]
# Uretir: <VERI>/raw/d1 (ham), <VERI>/panel_full, <VERI>/panel_dev. Betikler veri klasorunun disinda durur; python -I ile calisir.
set -euo pipefail
D="${1:?veri klasoru}"; END="${2:-2026-11-20}"; CUT="${3:-2025-06-30}"
K="$(cd "$(dirname "$0")" && pwd)"
cd /
python3 -I "$K/01_indir.py" "$D/raw/d1" END="$END"
python3 -I "$K/02_panel.py" "$D/raw/d1" "$D/panel_full" CUT="$END"
python3 -I "$K/02_panel.py" "$D/raw/d1" "$D/panel_dev" CUT="$CUT"
python3 -I "$K/03_dogrula.py" "$D/raw/d1" "$D/panel_full" "$D/panel_dev" DEV_CUT="$CUT"
