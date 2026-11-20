#!/usr/bin/env bash
# V4 çürütme (S3, T1/T2, K1/K2). Kullanım: bash run.sh <panel_full klasörü>   (kasa AÇIK; yalnız betimleme, kural dondurmaz)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
DATA="${1:?panel_full klasörünü ver}"
mkdir -p "$HERE/out"
python3 -I "$HERE/s3.py" "$DATA" > "$HERE/out/s3_log.txt"
python3 -I "$HERE/tk.py" "$DATA" > "$HERE/out/tk_log.txt"
python3 -I "$HERE/birlestir.py" "$ROOT/ek/v4_curutme_diger.csv"
echo "tamam: $ROOT/ek/v4_curutme_diger.csv; günlükler: $HERE/out/s3_log.txt, $HERE/out/tk_log.txt"
