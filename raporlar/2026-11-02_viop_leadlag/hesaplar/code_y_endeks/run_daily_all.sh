#!/bin/bash
# Günlük boru hattı (ll v4 temizlik kuralıyla yeniden üretim). Her betik yeni Python sürecinde.
cd "$(dirname "$0")"
for s in s0_weights s1_sync s1b_best s1c_years s2_daily_lead s2b_summary s3_lomac s5_backtest s6_regime s7_extra s7b_thyao_robust; do
  echo "== $s $(date +%H:%M:%S)"; nice -n 10 python3 $s.py > results/log_$s.txt 2>&1 || echo "FAIL $s"
done
echo "== done $(date +%H:%M:%S)"
