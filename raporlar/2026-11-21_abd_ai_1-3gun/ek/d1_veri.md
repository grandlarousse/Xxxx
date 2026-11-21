araç: 26/40

# D1 veri altyapısı ve betimleyici risk tablosu (21 Kasım 2026)

**Kapsam.** 140 kodun günlük verisi (2010-01-01 → 2026-11-20; Close ve Adj Close birlikte, O/H/L çarpanla düzeltildi) `veri/gunluk/`; 95 hedef+ETF kodunun 1 saatlik barları (çoğunda 2023-12-26'dan, yeni halka arzlarda 2024-11-22'den) `veri/saatlik/`. Kapsam dosyaları: `veri/kapsam_*.csv`, `ek/saatlik_kapsam.csv`. Birim testleri geçti (bilinen sinyal bulunuyor; 1 gün kaydırınca kayboluyor; tatilde NaN; BH = statsmodels).

**Sorunlu kodlar.**
- **PSTG → P:** Pure Storage adı Everpure, Inc. oldu; Yahoo'da PSTG boş, yeni kod `P` (günlük 2015'ten; saatlik yalnızca ~152 gün). Betikte takma ad.
- **SNDK 2026-11-20:** Yahoo o gün 8:1 bölünme gösteriyor; Close/Adj Close NaN, O/H/L/hacim dolu. Kapanış aynı günün saatlik son barından yamandı (79,30; −%16,0), `yama` sütununda işaretli; ileri doldurma yok.
- **^VIX** ABD tatillerinde de değer veriyor; takvim SPY'den.
- **Saatlik:** yarım günlerde son bar 11:30'da kesik; 2026-01-30'da çoğu kodda 3 bar. `saatlik_gunluk_ozet()` bu günlerde 15:30 fiyatını NaN bırakır. Tam günlerde saatlik son bar ile resmi kapanış farkı medyan ~2 bps.
- Kısa geçmiş: CRWV, SNDK (2025), NBIS, GEV, ALAB, AMDL, MUU, SMCX, PLTU (2024). WULF'un 2021 öncesi başka şirket.
- BTC/ETH, vadeli, döviz ve VIX ailesi ABD kapanışından sonra kapanıyor; `hizala` bunlara otomatik 1 gün gecikme uygular.

**Betimleyici bulgular.**
- **En oynak 10 (60g):** SOXS, AMDL, SOXL (~%11/gün), SMCX, MUU, CIFR %7,6, AAOI, IREN, CRDO, NBIS.
- **En likit 10 (60g medyan $ hacim):** SPY 33 mr, NVDA 26, QQQ 25, MU 24, AAPL, TSLA, SNDK, AMD, META, MSFT (~11-13 mr).
- **Gece/gün içi (2023'ten beri):** hisselerin %82'sinde gece ortalaması gün içinden büyük (medyan +17'ye +6 bps/gün; SMH 15,9'a 1,1). Neocloud ve kaldıraçlı ürünlerde gün içi negatif (CRWV −15,7). Oynaklığın ~%40'ı gece. Test değil, betimleme.
- **Kümeler (Ward, son 1 yıl, 15):** çekirdek yarı iletken + SMH/SOXL (28), bellek/disk (MU SNDK WDC STX; iç korelasyon 0,79), optik (COHR LITE CIEN AAOI FN), neocloud+madenciler+ORCL+BE+OKLO, sunucu/depolama (P NTAP DELL HPE), NVDA tek başına, yazılım, enerji, geniş piyasa, ters ETF'ler.
- **Son durum:** SMH için 20 Kasım (−%10,6) 2023'ten beri en kötü 2. gün (1.: 5 Kasım −%11,2). 52 hafta zirvesinden SMH −%40, MU −%51, NVDA −%48, SNDK −%73, SOXL −%90. ATR14: SMH %7,3, SOXL %37.

## Kısa tablo (25 araç; yüzdeler günlük; kuyruklar 2023'ten beri; β ve R² son 1 yıl)

| Kod | Hacim60g $mn | Vol60g % | Vol1y % | β SMH | R² SMH | q5 1g % | q1 3g % | En kötü % | Tarih | Zirveden % | YTD % | Gece bps | Gün içi bps | ATR14 % | Küme |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SMH | 4396 | 3.19 | 2.79 | 1.00 | 1.00 | -3.62 | -9.89 | -11.2 | 2026-11-05 | -40.2 | 11.1 | 15.9 | 1.07 | 7.30 | 3:AMD |
| SOXX | 4447 | 3.63 | 3.22 | 1.14 | 0.98 | -3.94 | -10.4 | -12.1 | 2026-11-05 | -43.4 | 23.1 | 12.5 | 2.66 | 8.01 | 3:AMD |
| QQQ | 25382 | 1.71 | 1.41 | 0.46 | 0.84 | -1.97 | -5.01 | -6.49 | 2026-11-05 | -19.9 | -0.62 | 6.77 | 2.80 | 3.47 | 9:SPY |
| SOXL | 9589 | 11.0 | 9.55 | 3.38 | 0.98 | -11.6 | -29.3 | -38.7 | 2026-11-05 | -89.7 | -26.5 | 34.2 | 5.17 | 37.3 | 3:AMD |
| TQQQ | 4114 | 4.99 | 4.17 | 1.37 | 0.84 | -5.96 | -14.8 | -18.9 | 2026-11-05 | -52.6 | -21.4 | 16.4 | 7.99 | 12.6 | 9:SPY |
| USD | 51.5 | 6.35 | 5.35 | 1.85 | 0.94 | -7.55 | -21.8 | -27.5 | 2025-01-27 | -69.1 | -33.1 | 31.9 | 3.28 | 20.7 | 3:AMD |
| NVDL | 352 | 5.99 | 5.15 | 1.32 | 0.51 | -8.23 | -24.9 | -33.8 | 2025-01-27 | -76.0 | -64.8 | 42.6 | 0.09 | 29.0 | 7:NVDA |
| NVDA | 26119 | 3.03 | 2.59 | 0.67 | 0.51 | -4.24 | -12.5 | -17.0 | 2025-01-27 | -47.5 | -32.5 | 23.4 | 3.68 | 10.2 | 7:NVDA |
| AMD | 12115 | 5.51 | 4.73 | 1.41 | 0.69 | -5.53 | -14.6 | -17.3 | 2026-02-04 | -34.7 | 98.2 | 18.1 | 8.05 | 12.4 | 3:AMD |
| AVGO | 8458 | 3.49 | 3.17 | 0.83 | 0.53 | -4.16 | -11.7 | -17.4 | 2025-01-27 | -36.6 | -11.6 | 23.0 | -0.54 | 7.65 | 3:AMD |
| TSM | 4576 | 3.04 | 2.74 | 0.85 | 0.75 | -3.57 | -9.97 | -13.3 | 2025-01-27 | -34.4 | 5.70 | 20.1 | -1.31 | 6.83 | 3:AMD |
| MU | 23784 | 4.79 | 5.38 | 1.59 | 0.68 | -5.32 | -16.8 | -17.5 | 2026-11-05 | -51.0 | 108 | 26.4 | 6.43 | 11.5 | 2:MU |
| SNDK | 12500 | 6.14 | 7.24 | 1.88 | 0.53 | -8.95 | -26.1 | -22.3 | 2026-11-05 | -72.8 | 167 | 42.4 | 43.7 | 16.7 | 2:MU |
| WDC | 2855 | 4.97 | 5.29 | 1.37 | 0.53 | -5.27 | -15.4 | -18.3 | 2025-04-03 | -65.0 | 51.7 | 20.4 | 11.0 | 10.5 | 2:MU |
| STX | 3094 | 5.06 | 4.91 | 1.23 | 0.49 | -4.69 | -14.5 | -16.4 | 2025-04-03 | -58.2 | 66.5 | 17.5 | 11.7 | 10.7 | 2:MU |
| LRCX | 2593 | 4.68 | 4.40 | 1.42 | 0.81 | -5.02 | -14.7 | -16.4 | 2026-11-05 | -57.7 | 7.38 | 18.2 | 2.75 | 9.51 | 3:AMD |
| ANET | 1043 | 4.09 | 3.68 | 0.85 | 0.41 | -4.77 | -14.9 | -22.4 | 2025-01-27 | -22.7 | 27.9 | 15.9 | 6.57 | 8.77 | 3:AMD |
| CRDO | 1349 | 6.75 | 6.25 | 1.50 | 0.45 | -7.98 | -22.7 | -46.8 | 2023-02-15 | -67.0 | -30.6 | 23.8 | 12.0 | 15.1 | 3:AMD |
| ALAB | 1185 | 6.56 | 6.45 | 1.65 | 0.51 | -8.86 | -21.8 | -28.0 | 2025-01-27 | -62.7 | 8.41 | 24.4 | 11.8 | 13.4 | 3:AMD |
| LITE | 3908 | 6.53 | 6.42 | 1.49 | 0.42 | -7.28 | -20.9 | -22.5 | 2025-01-27 | -59.4 | 24.9 | 26.0 | 6.92 | 14.1 | 1:LITE |
| VRT | 1272 | 5.13 | 4.53 | 1.18 | 0.53 | -6.01 | -17.6 | -29.9 | 2025-01-27 | -55.8 | 2.68 | 32.0 | 2.86 | 11.4 | 3:AMD |
| CRWV | 2757 | 6.58 | 6.37 | 1.33 | 0.34 | -9.65 | -21.5 | -20.8 | 2025-08-13 | -71.4 | -44.8 | 39.5 | -15.7 | 16.2 | 4:ORCL |
| NBIS | 3350 | 6.73 | 7.24 | 1.60 | 0.38 | -10.1 | -23.1 | -37.4 | 2025-01-27 | -71.6 | -2.86 | 49.4 | 10.4 | 21.6 | 4:ORCL |
| IREN | 1521 | 6.83 | 6.97 | 1.60 | 0.41 | -9.81 | -23.2 | -24.2 | 2025-01-27 | -82.6 | -68.7 | 44.6 | 6.35 | 22.1 | 4:ORCL |
| PLTR | 4052 | 3.20 | 3.81 | 0.38 | 0.08 | -5.57 | -14.6 | -15.1 | 2024-05-07 | -31.4 | -19.3 | 16.5 | 23.7 | 6.85 | 12:PLTR |

Tam tablo: ek/risk_tablosu.csv (95 satır, 36 sütun); korelasyon: ek/korelasyon.csv; kümeler: ek/kumeler.csv.
