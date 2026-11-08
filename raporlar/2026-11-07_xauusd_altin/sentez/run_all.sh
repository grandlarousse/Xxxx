#!/bin/bash
# Sentez zinciri: sıra önemli (s02 tablosu s03 çıktısını, s07 hepsini okur). ~1 dk.
cd "$(dirname "$0")"
set -e
for f in s01_fdr s03_dogrula s04_ortusme_birlesim s05_bugun s06_risk s02_tablo s07_rapor; do
  python3 -W ignore $f.py > log_$f.txt 2>&1
done
echo tamam
