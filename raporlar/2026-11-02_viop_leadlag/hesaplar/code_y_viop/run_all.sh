#!/bin/bash
# Tüm hattı sırayla çalıştırır (nice). Kullanım: bash run_all.sh
set -e
cd "$(dirname "$0")"
S=/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad
for s in 02_parse.py 03_build.py 05_liquidity.py; do echo "== $s"; nice -n 10 python3 -I $s; done
cp results/liquidity_raw.csv $S/out/y_viop_likidite.csv
for s in 04_evening.py 06_basis.py 06b_basis_tests.py 07_oi.py 08_openclose.py 09_backtest.py; do echo "== $s"; nice -n 10 python3 -I $s; done
echo ALLDONE
