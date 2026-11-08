#!/bin/bash
# a2_seans_gunici: bütün analizleri sırayla yeniden üretir (kayıt CSV'si aile bazında sıfırlanıp yeniden yazılır).
set -e
cd "$(dirname "$0")"
for f in a_segments.py b_segmeans.py c_basis.py d_fix.py e_weekend.py f_micro.py g_robust.py h_tables.py; do
  echo "== $f"; python3 -W ignore "$f" > "log_${f%.py}.txt"
done
echo bitti
