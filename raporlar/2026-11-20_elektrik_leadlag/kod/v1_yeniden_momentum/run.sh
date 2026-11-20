#!/usr/bin/env bash
# V1 — S1/S2/S3 bağımsız yeniden üretim. Kullanım:
#   bash run.sh <veri_klasoru> <rapor_klasoru> [cikti_klasoru] [indir]
#   <veri_klasoru>: raw/d1 ve panel_full'u içeren klasör (panel_full yalnız son karşılaştırma adımında açılır)
#   4. bağımsız değişken "indir" ise 8 hisse + 3 endeks İş Yatırım'dan yeniden indirilir ve ham dosyalarla karşılaştırılır.
set -euo pipefail
VERI="$1"; RAPOR="$2"; CIKTI="${3:-$(dirname "$VERI")/v1out}"; MOD="${4:-}"
KOD="$(cd "$(dirname "$0")" && pwd)"
if [ "$MOD" = "indir" ]; then
  DL="$CIKTI/../v1dl"; mkdir -p "$DL"
  B="https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/"
  for s in AKSEN ENJSA ODAS ZOREN BIGEN AYDEM LYDYE MAGEN; do
    curl -s -m 120 -A "Mozilla/5.0" -o "$DL/$s.json" "${B}Data.aspx/HisseTekil?hisse=$s&startdate=01-01-2000&enddate=20-11-2026"; done
  for s in XELKT XU030 XU100; do
    curl -s -m 120 -A "Mozilla/5.0" -o "$DL/IDX_$s.json" "${B}ChartData.aspx/IndexHistoricalAll?period=1440&from=20000101000000&to=20261120235959&endeks=$s"; done
  python3 -I "$KOD/00_indir_dogrula.py" "$VERI/raw/d1" "$DL"
fi
python3 -I "$KOD/01_main.py" "$VERI/raw/d1" "$CIKTI" > "$CIKTI.log" 2>&1 || { tail -20 "$CIKTI.log"; exit 1; }
python3 -I "$KOD/02_karsilastir.py" "$CIKTI" "$VERI/panel_full" "$RAPOR"
