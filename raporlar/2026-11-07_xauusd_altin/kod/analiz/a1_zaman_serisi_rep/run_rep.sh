#!/bin/bash
# Bağımsız yeniden üretim (lib_altin ve analist kodu kullanılmaz). Sırayla çalıştır.
set -e
D=/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a1_zaman_serisi_rep
cd /tmp
python3 -W ignore $D/r1_build.py
python3 -W ignore $D/r2_timing.py > $D/r2_timing.txt
python3 -W ignore $D/r2b_timing.py > $D/r2b_timing.txt
python3 -W ignore $D/r2c_minute_by_period.py > $D/r2c_minute.txt
python3 -W ignore $D/r3_lowmom.py > $D/r3_lowmom.txt
python3 -W ignore $D/r4_others.py > $D/r4_others.txt
python3 -W ignore $D/r5_extra.py > $D/r5_extra.txt
python3 -W ignore $D/r6_nwcheck.py > $D/r6_nwcheck.txt
