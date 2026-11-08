#!/bin/bash
# a3_takvim_olay: tam yeniden üretim (registry sıfırlanır ve yeniden yazılır)
set -e
cd "$(dirname "$0")"
python3 -W ignore build_events.py > log_events.txt      # --download ile kaynak sayfaları yeniden indirir
python3 -W ignore a3_analiz.py   > log_analiz.txt
python3 -W ignore a3_derin.py    > log_derin.txt
python3 -W ignore a3_oynaklik.py > log_oynaklik.txt
python3 -W ignore a3_tablolar.py
tail -1 log_oynaklik.txt
