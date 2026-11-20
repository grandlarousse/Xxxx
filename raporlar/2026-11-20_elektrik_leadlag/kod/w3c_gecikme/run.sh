#!/usr/bin/env bash
# W3-C: XU030 → elektrik gecikmesi çürütme taraması. Kullanım: bash run.sh <panel_dev klasörü>
# panel_full / raw klasörleri KULLANILMAZ (kasa dönemi).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
DATA="${1:?panel_dev klasörünü ver}"
case "$DATA" in *panel_full*|*raw*) echo "kasa verisi kullanılamaz" >&2; exit 2;; esac
python3 -I "$HERE/tara.py" "$DATA" "$ROOT/ek/w3c_gecikme_sonuc.csv" "$ROOT/ek/oos1_sonuc.csv" > "$HERE/tara_log.txt"
python3 -I "$HERE/denetim.py" "$DATA" > "$HERE/denetim_log.txt"
echo "tamam: $ROOT/ek/w3c_gecikme_sonuc.csv; günlükler: $HERE/tara_log.txt, $HERE/denetim_log.txt"
