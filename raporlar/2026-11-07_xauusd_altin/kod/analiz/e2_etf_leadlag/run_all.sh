#!/bin/bash
# e2_etf_leadlag tam yeniden çalıştırma (kayıt dosyası sıfırlanır)
S=/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad
cd $S/out/e2_etf_leadlag
rm -f $S/out/registry/e2_etf_leadlag.csv
for f in s0_veri_kaldirac s1_madenci_artik s2_gunici_rv s3_capraz_gecikmeli s4_viop_cot_akis s5_derin_a s5b_kismi_rank s7_asya_madenci_kombin s6_strateji s10_ayristirma s8_ozet s9_grid_oos; do
  echo "=== $f"; python3 -W ignore $f.py > log_$f.txt 2>&1 || { echo "HATA $f"; tail -20 log_$f.txt; exit 1; }
done
echo bitti
