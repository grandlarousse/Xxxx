#!/bin/bash
# a5_esz_artik: tüm adımları baştan çalıştırır (kayıt dosyası a5_02'de sıfırlanır)
cd "$(dirname "$0")"
for f in a5_01_signals.py a5_02_tests.py a5_03_robust.py a5_04_spotgrid.py a5_05_extra.py; do
  echo "=== $f"; python3 -W ignore $f > log_${f%.py}.txt 2>&1 || { echo "HATA $f"; exit 1; }
done
echo "kayıt satırı: $(($(wc -l < ../registry/a5_esz_artik.csv)-1))"
