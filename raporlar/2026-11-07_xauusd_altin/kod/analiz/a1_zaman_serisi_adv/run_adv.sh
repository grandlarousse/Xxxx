#!/bin/bash
# Hakem kontrolleri (a1_zaman_serisi): bağımsız yeniden kurulum + saldırılar. Her betik stdout'a yazar.
set -e
cd /tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a1_zaman_serisi_adv
for f in r1_replicate r2_decomp r4_arife r5_grid r6_drift r7_conc r8_regimes r9_spells r10_others r11_rev; do
  echo "===== $f"; python3 -W ignore $f.py
done
