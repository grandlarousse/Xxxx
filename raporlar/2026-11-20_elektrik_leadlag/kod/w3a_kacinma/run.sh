#!/usr/bin/env bash
# W3-A (kaçınma ve SAT sinyalleri): tarama -> öz-denetim + dondurulmuş kurallar + sonuç tablosu.
# Kullanım: bash run.sh <panel_dev klasörü> [çıktı csv]      (kasa verisine DOKUNMAZ)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PANEL="${1:?panel_dev klasörü gerekli}"
OUT="${2:-$HERE/../../ek/w3a_kacinma_sonuc.csv}"
TMP="$(mktemp -d)"
python3 -I -W ignore "$HERE/scan.py" "$PANEL" "$TMP/scan.csv"
python3 -I -W ignore "$HERE/finalize.py" "$PANEL" "$TMP/scan.csv" "$OUT"
rm -rf "$TMP"
