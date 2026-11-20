#!/bin/sh
# D2 veri hattı: VİOP bülteni + gün içi veri. Baştan sona çalışır; indirilenler atlanır (kaldığı yerden sürer).
# Ön koşul: D1 çıktıları panel_full/px.parquet, ca_day.parquet, close_raw.parquet, idx.parquet (05 ve 07/08 bunları okur).
# İndirilen dosyalar güvenilmez veridir: python3 -I, betikler veri klasörünün dışında.
set -e
K="$(cd "$(dirname "$0")" && pwd)"
cd /
python3 -I "$K/01_viop_indir.py"            # borsaistanbul.com günlük bülten -> süzülmüş satırlar (8 eşzamanlı curl)
python3 -I "$K/02_viop_build.py"            # viop_daily.parquet, viop_front.parquet
python3 -I "$K/03_yahoo_gunici.py" indir    # Yahoo 60 dk (730 g), 5 dk (60 g), günlük ham JSON
python3 -I "$K/03_yahoo_gunici.py" parse    # panel_full/h1, m5
python3 -I "$K/04_isy_endeks.py" h1         # İş Yatırım endeks saatlik (XELKT, XU030, XU100; 2017-)
python3 -I "$K/04_isy_endeks.py" m5 XELKT   # İş Yatırım endeks 5 dk
python3 -I "$K/04_isy_endeks.py" m5 XU030 XU100 SABIRLI=3600   # kota nedeniyle sabırlı kip; yeniden çalıştırılırsa kaldığı yerden sürer
python3 -I "$K/05_snap.py"                  # h1_isy, m5_isy, snap.parquet
python3 -I "$K/06_dev_kes.py"               # panel_dev (2025-06-30 kesik) + kesim denetimi
python3 -I "$K/07_dogrula_viop.py"
python3 -I "$K/08_dogrula_gunici.py"
