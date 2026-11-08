#!/bin/bash
# Bagimsiz yeniden uretim (lib_altin / e2_common kullanilmaz). ~15 sn.
set -e
cd "$(dirname "$0")"
for s in r1_sinyal_zaman r2_ic r3_strateji r4_ek_kontroller r5_saglamlik; do
  python3 -W ignore $s.py > log_$s.txt 2>&1
done
echo ok
