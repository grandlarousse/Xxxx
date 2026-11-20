#!/bin/bash
# V6 — karar anı ve dolum gerçekçiliği. Kullanım: run.sh <panel_full> [ek_klasoru] [ara_klasor]
# İsteğe bağlı: XU030_M5_RAW=<raw/d2/isy/m5/XU030.parquet> (04_isy_endeks.py SABIRLI ile tamamlanan ham 5 dk dosyası)
set -e
K=$(cd "$(dirname "$0")" && pwd)
P=${1:?panel_full klasoru}
O=${2:-$K/../../ek}
A=${3:-${TMPDIR:-/tmp}/v6_zamanlama_ara}
mkdir -p "$A"
python3 -I "$K/t1_endeks.py" "$P" "$A/t1_endeks.csv" $XU030_M5_RAW > "$A/t1.log"   # iş 1–2 (≈ 1 dk)
python3 -I "$K/t3_dolum.py"  "$P" "$A/t3_dolum.csv"  > "$A/t3.log"                  # iş 3 (≈ 1 dk)
python3 -I "$K/t5_hisse.py"  "$P" "$A/t5_hisse.csv"  > "$A/t5.log"                  # iş 5 (mod=tam; ≈ 25 dk)
python3 -I "$K/birlestir.py" "$A" "$O/v6_zamanlama.csv"
