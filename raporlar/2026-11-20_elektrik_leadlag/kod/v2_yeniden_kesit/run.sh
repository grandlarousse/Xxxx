#!/usr/bin/env bash
# V2 bagimsiz yeniden uretim (T2, K1, K2) + T1 denetimi. Kullanim: bash run.sh <VERI_KLASORU> [CALISMA_KLASORU]
# <VERI_KLASORU>: raw/d1 ve (yalniz sondaki karsilastirma icin) panel_full, panel_dev klasorlerini iceren dizin.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
DATA="${1:?veri klasoru}"
WORK="${2:-$DATA/../v2k_work}"
RAPOR="$(cd "$HERE/../.." && pwd)"
mkdir -p "$WORK"
python3 -I "$HERE/01_kurallar.py" "$DATA/raw/d1" "$RAPOR/ek" "$WORK"                     # ham veriden panel + kurallar + fark tablosu
python3 -I "$HERE/02_indir_dogrula.py" "$DATA/raw/d1" "$WORK/yeniden_indirme"             # 8 hisse Is Yatirim'dan yeniden (ag gerekir)
python3 -I "$HERE/03_panel_karsilastir.py" "$WORK" "$DATA/panel_full"                     # yalniz karsilastirma
python3 -I "$HERE/04_T1_denetim.py" "$WORK" "$DATA/panel_full" "$RAPOR/kod" "$RAPOR/ek" "$DATA/panel_dev"   # T1: kesme sinamasi + kiyas duyarliligi
