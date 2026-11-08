#!/bin/bash
# a8_ml_kombinasyon — bütün adımları sırayla yeniden üret (≈35-40 dk tek çekirdek; 02 adımı V1/V2/V3 paralel çalıştırılabilir)
set -e
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
python3 -W ignore features.py
python3 -W ignore 01_univariate.py
for v in V1 V2 V3; do python3 -W ignore 02_walkforward.py $v; done
python3 -W ignore 02b_ybar_w.py   # (02 zaten ybar_w yazar; doğrulama amaçlı)
python3 -W ignore 03_evaluate.py
python3 -W ignore 04_permimp.py
python3 -W ignore 05_robust.py
python3 -W ignore 06_c1_decomp.py
python3 -W ignore 07_placebo.py
python3 -W ignore 08_univ_bt.py
python3 -W ignore 09_longspot.py
python3 -W ignore 10_tables.py
