#!/bin/bash
# Bağımsız yeniden üretim (lib_altin ve analist kodu kullanılmaz). Sıra önemli.
cd "$(dirname "$0")"
python3 -W ignore r0_data.py      > log_r0.txt
python3 -W ignore r1_calendars.py > log_r1.txt
python3 -W ignore r2_claims.py    > log_r2.txt
python3 -W ignore r3_bh.py        > log_r3.txt
python3 -W ignore r4_extra.py     > log_r4.txt
