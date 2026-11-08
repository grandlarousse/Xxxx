#!/bin/bash
# a7_turkiye: tüm analizleri sırayla yeniden üret (kayıt dosyası aile bazında sıfırlanır)
cd "$(dirname "$0")"
for s in a7_01_audit a7_02_predict_xau a7_03_tr_gold a7_04_holidays a7_05_crisis a7_06_robust a7_07_claims a7_08_fdr; do
  python3 -W ignore $s.py > ${s}.log 2>&1 || echo "HATA: $s"
done
