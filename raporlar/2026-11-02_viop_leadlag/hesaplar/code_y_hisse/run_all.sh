#!/bin/bash
# hisse ajanı — yeniden üretim sırası (nice -n 10, tek iş parçacığı BLAS). Toplam ~30–40 dk (paylaşılan 4 çekirdekte).
set -e; cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
N="nice -n 10 python3"
$N hdata.py            # veri önbelleği (cc/gap/intra, TL hacim, likidite)
$N hreg.py             # NW toplu regresyon doğrulaması (statsmodels ile)
$N s1_sync.py          # senkron yapı: artık korelasyon, kümeler, PCA, istikrar
$N s2_leadlag.py main; $N s2_leadlag.py vol; $N s2_leadlag.py null   # ana tarama + hacim filtresi + 20 kaydırma null
$N s3_fdr.py           # BH-FDR, null, IS/OOS/PRE replikasyonu, asimetri -> out/y_hisse_matrix.parquet
$N s2b_rel.py; $N s3b_rel.py   # piyasa-göreli (çifte özgü) tarama + null; matrise eklenir
$N s4_pairs.py         # ekonomik çiftler
$N s5_bt.py; $N s5b_gapfade.py # backtestler + gap-fade ayrıştırması / gecikmeli giriş
$N s6_viopliq.py       # VİOP pay vadelisi likiditesi (data/viop bültenleri)
$N s7_hourly.py        # saatlik lead-lag
$N s8_market.py        # piyasa düzeyi lider (THYAO) ve küçük/bireysel faktör
$N s9_csv.py           # out/f_y_hisse.csv
