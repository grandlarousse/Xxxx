#!/bin/bash
# a1_zaman_serisi: tüm analizi baştan üretir (kayıt dosyası a1_main.py'de sıfırlanır)
set -e
D=/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a1_zaman_serisi
cd $D
python3 -W ignore a1_main.py
python3 -W ignore a1_deep.py
python3 -W ignore a1_volreg.py > volreg_stdout.txt
python3 -W ignore a1_final.py
python3 -W ignore a1_tables.py && cat RAPOR_govde.md tables.md > RAPOR.md
