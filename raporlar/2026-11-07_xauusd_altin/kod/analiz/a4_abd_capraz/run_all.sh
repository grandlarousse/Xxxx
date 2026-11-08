#!/bin/bash
# a4_abd_capraz — tüm analizleri sırayla yeniden üretir.
# Kayıt dosyası (out/registry/a4_abd_capraz.csv) her betikte kendi önekine göre temizlenip yeniden yazılır (yinelenme olmaz).
set -e
D=/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz
for s in s1_tek_degisken s2_goreli_deger s3_saatlik_pencere s4_adaylar s5_c1_tani s7_kural s6_ozet; do
  echo "== $s"
  python3 -W ignore "$D/$s.py" > "$D/${s%%_*}_log.txt" 2>&1
done
echo tamam
