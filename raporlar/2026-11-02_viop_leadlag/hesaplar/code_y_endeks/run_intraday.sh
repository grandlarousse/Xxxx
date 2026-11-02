#!/bin/bash
cd "$(dirname "$0")"
while pgrep -f "^python3 -I isy_fetch.py h1" >/dev/null; do sleep 10; done
echo "== h1 indirildi $(grep -c 'h1 ok' log_h1.txt) $(date +%H:%M:%S)"
nice -n 10 python3 s4_intraday.py yh m5 > results/log_s4_yh_m5.txt 2>&1 && echo "== yh m5 ok $(date +%H:%M:%S)" || echo "FAIL yh m5"
nice -n 10 python3 s4b_tick.py yh_m5 > results/log_s4b.txt 2>&1 && echo "== tick ok" || echo "FAIL tick"
nice -n 10 python3 s8_m5_bt.py > results/log_s8.txt 2>&1 && echo "== m5 bt ok" || echo "FAIL m5bt"
nice -n 10 python3 s4_intraday.py isy h1 > results/log_s4_isy_h1.txt 2>&1 && echo "== isy h1 ok $(date +%H:%M:%S)" || echo "FAIL isy h1"
nice -n 10 python3 s4c_years.py > results/log_s4c.txt 2>&1 && echo "== years ok $(date +%H:%M:%S)" || echo "FAIL years"
echo "== intraday done"
