#!/bin/bash
# e1_etf_zaman_takvim — tüm analizleri sırayla yeniden üretir (kayıt dosyası aile ön ekine göre temizlenip yeniden yazılır)
D=/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim
set -e
for s in a_ts a_strat a_os b_night b2_gap c_cal d_lev e_etf f_final g_perm g_placebo; do echo "== $s"; python3 -W ignore $D/$s.py > $D/log_$s.txt 2>&1; done
echo bitti
