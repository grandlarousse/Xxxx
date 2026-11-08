#!/bin/bash
# Bağımsız yeniden üretim (lib_altin kullanılmaz). Ham Yahoo + exchange_calendars XNYS.
D=/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_rep
set -e
for s in r01_takvim_zaman r02_takvim r03_fiyat_kurallari r04_gece r05_ornek_disi r06_ek r07_ek2 r08_saatlik; do echo "== $s"; python3 -W ignore $D/$s.py > $D/log_$s.txt 2>&1; done
