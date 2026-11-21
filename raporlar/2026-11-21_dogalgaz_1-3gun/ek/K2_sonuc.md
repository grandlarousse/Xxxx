# K2 — Bağımsız yeniden hesap ve çürütme

Betik: `kod/02_bagimsiz_kontrol.py <veri> [çıktı.txt]` (K1 kodu okunmadan yazıldı; tek komut, ~1 dk). Tanımlar: basit getiri, z = r / σ60 (σ t−1'e kadar), t kapanışında giriş, t+h kapanışında çıkış; t: günlük strateji P&L serisi, Newey–West gecikme h. Ana hesap **basit getiriyle z**; K1 **log getiriyle z** kullanmış (A5 ve A8'de log-z ile K1 sayıları birebir çıktı).

## A. Yeniden üretim (K1 | K2 | fark | uyuyor mu)
| # | ölçü | K1 | K2 | fark | uyum |
|---|---|---|---|---|---|
| 1 | UNG / BOIL / KOLD 2012-21 bps (t) | -4.7 (-0.86) / -13.3 (-1.30) / 9.5 (0.93) | -4.7 (-0.88) / -13.3 (-1.32) / 9.5 (0.94) | 0 | evet |
| 1 | aynı, 2022-26 | -4.8 / -18.2 / 14.0 | -4.8 / -18.2 / 14.0 | 0 | evet |
| 1 | kış 2012-21 UNG/BOIL/KOLD | -18.6 / -42.1 / 36.5 | -18.6 / -42.1 / 36.5 | 0 | evet (yaz ve 2022-26 kış/yaz da birebir) |
| 2 | BOIL − 2×UNG h=1 / h=3 | -5.4 / -16.0 | -5.4 / -17.5 (faz 0); -16.0 (faz 1) | 0 / -1.5 | evet (h=3 pencere fazına bağlı) |
| 2 | KOLD + 2×UNG h=1 / h=3 | 1.47 / 3.59 | 1.5 / -1.9 (faz 0); 3.6 (faz 1); 1.5 (faz 2) | 0 / -5.5 | kısmen: h=3 işareti faza göre değişiyor, sıfırdan ayırt edilemez |
| 3 | beta / R² son250 ve 2022+ (EQT, AR, CRK, EXE, RRC, CNX, LNG, BOIL, KOLD) | ör. EQT 0.26/0.24, 0.34/0.28 | EQT 0.25/0.25, 0.34/0.28; diğer 8 satır birebir | ≤0.01 | evet |
| 4 | KOLD Perşembe IS / OOS / 24-26 bps (t); OOS net | 43.7 (1.86) / 70.7 (1.68) / 90.3 (2.04); 55.7 | aynı | 0 | evet |
| 5 | gece boşluğu z>1 → KOLD h=1 IS / OOS / 24-26 | 44.0 (1.54) / 129.1 (2.02) / 118.4 (1.41), n 381/162 | basit-z: 43.1 (1.53) / 121.0 (1.92) / 115.3 (1.40), n 387/165; log-z: 44.0 (1.54) / 129.1 (2.02) | OOS -8 bps, t -0.10 | evet (tanım farkı) |
| 6 | TTF z>2 → UNG h=3 IS / OOS (t), n | 162 (1.30) / 391 (2.16), 29/22 | 81 (0.75) / 220 (1.45), 36/30 | OOS -170 bps | **hayır** |
| 6 | TTF z>2 → BOIL h=3 IS / OOS | 357 (1.47) / 782 (2.30) | 190 (0.89) / 454 (1.54) | OOS -328 bps | **hayır** |
| 6 | en yakın varyant (yalnız 60g hacim>0 oranı >%90 olan günler) UNG / BOIL OOS | — | 299 (1.58) / 645 (1.80), n 30/21 | | K1'in n'i bu kuralla tutuyor, ortalama tutmuyor |
| 7 | UNG z>1 → gaz sepeti h=1 IS / OOS | 6.3 (0.49) / -3.4 (-0.18) [IS 2007+, hacim filtreli] | 18.5 (1.21) / 0.3 (0.09) [IS 2011-10+, filtresiz] | | evet: ikisi de boş |
| 8 | UNG z>2 → ertesi gün UNG IS / OOS, n | 9.2 (0.23) / -280.3 (-2.32), 90/32 | basit-z: 5.5 (0.14) / -239.4 (-2.23), 93/36; log-z: birebir | OOS +41 | evet (tanım farkı) |

## B1. Perşembe / EIA günü
Takvim: Perşembe; Perşembe tatilse (32 hafta: 19 Şükran, 3 Noel, 3 Yılbaşı, 3 Temmuz 4, Juneteenth 2025, 11 Kasım 2010 ve 2021) rapor Çarşamba'ya kaydırıldı (varsayım; gerçek EIA takvimi yok). "hariç" = bu haftaların Çar ve Per günleri iki gruptan da çıkarıldı. Fark t = Welch.

Yıl yıl, EIA günü − diğer günler (bps): UNG EIA / diğer / fark (t); KOLD ve BOIL fark (t). Parantezli "har" = kayma haftaları hariç UNG farkı.
| yıl | UNG EIA | UNG diğer | UNG fark (t) | har | KOLD fark (t) | BOIL fark (t) |
|---|---|---|---|---|---|---|
| 2007 | -24.9 | -12.6 | -12.4 (-0.27) | -14.0 | | |
| 2008 | -99.4 | 9.7 | -109.1 (-2.25) | -120.1 | | |
| 2009 | 9.8 | -36.0 | 45.7 (0.64) | 34.0 | | |
| 2010 | -52.4 | -8.6 | -43.8 (-0.95) | -41.8 | | |
| 2011 | -46.2 | -16.3 | -29.9 (-0.86) | -35.3 | | |
| 2012 | -26.6 | -3.3 | -23.4 (-0.43) | -27.9 | 56.1 (0.56) | -59.4 (-0.59) |
| 2013 | 7.7 | 4.6 | 3.0 (0.08) | 2.2 | -4.6 (-0.07) | -8.4 (-0.12) |
| 2014 | -46.1 | -0.6 | -45.5 (-1.07) | -24.4 | 101.1 (1.29) | -93.3 (-1.20) |
| 2015 | -64.0 | -6.1 | -57.9 (-1.40) | -57.7 | 94.4 (1.20) | -94.4 (-1.23) |
| 2016 | 28.2 | 1.1 | 27.1 (0.60) | 22.0 | -69.1 (-0.85) | 78.2 (0.96) |
| 2017 | 19.3 | -25.9 | 45.1 (1.40) | 48.7 | -87.6 (-1.42) | 74.7 (1.22) |
| 2018 | -47.5 | 20.8 | -68.3 (-1.41) | -67.2 | 143.7 (1.45) | -142.7 (-1.52) |
| 2019 | -11.9 | -12.9 | 1.0 (0.03) | -0.3 | 1.6 (0.03) | 1.5 (0.03) |
| 2020 | -82.4 | -0.3 | -82.2 (-1.54) | -87.8 | 172.9 (1.86) | -181.4 (-1.94) |
| 2021 | -17.2 | 26.5 | -43.6 (-0.94) | -39.7 | 87.0 (0.99) | -80.6 (-0.90) |
| 2022 | -39.8 | 31.0 | -70.8 (-0.92) | -77.3 | 121.7 (0.85) | -133.8 (-0.91) |
| 2023 | -8.5 | -40.5 | 32.1 (0.56) | 28.9 | -75.6 (-0.71) | 65.8 (0.61) |
| 2024 | -57.4 | 14.8 | -72.2 (-1.24) | -56.9 | 176.4 (1.80) | -181.6 (-1.88) |
| 2025 | -58.1 | 7.4 | -65.5 (-1.34) | -60.7 | 105.1 (1.20) | -105.8 (-1.21) |
| 2026 | -11.0 | 2.8 | -13.8 (-0.29) | -13.8 | 43.2 (0.48) | -43.9 (-0.49) |
UNG farkı 20 yılın 14'ünde negatif; KOLD farkı 15 yılın 11'inde pozitif. Hiçbir tek yıl |t| ≥ 2 değil (2008 hariç).

Dönemler (dahil; hariç fark parantezde):
| dönem | UNG EIA / diğer / fark (t) | KOLD fark (t) | BOIL fark (t) |
|---|---|---|---|
| 2007-2018 (makale dönemine en yakın) | -28.8 / -5.9 / -22.8 (-1.69) [har -23.6] | | |
| 2014-2018 | -22.1 / -2.1 / -20.0 (-1.05) [har -15.7] | 36.7 (1.01) | -35.7 (-1.01) |
| IS 2011-10..2021 | -22.4 / -1.3 / -21.1 (-1.56) | 44.0 (1.73) [har 42.6 (1.64)] | -44.5 (-1.75) |
| OOS 2022-2026 | -35.5 / 3.2 / -38.7 (-1.46) | 75.0 (1.56) [har 72.2 (1.49)] | -80.8 (-1.67) |
| 2024-2026 | -43.4 / 8.6 / -52.0 (-1.73) | 110.8 (2.09) [har 99.4 (1.89)] | -113.1 (-2.15) |
Makale karşılaştırması: 2007-2018 UNG'de yön aynı (EIA -29 / diğer -6; makale -37 / -9). 2014-2018'de makale "etki yok, EIA günü diğerlerinden iyi" diyor; UNG'de fark -20 bps ama anlamsız (t -1.05): "anlamlı etki yok" kısmı tutuyor, işaret tutmuyor (UNG 16:00 kapanışı, makale uzlaşma fiyatı).

Haftanın günleri (bps, t): KOLD IS Pzt 5.9 · Sal -17.4 · Çar 10.6 · **Per 43.7 (1.9)** · Cum 15.3; OOS Pzt -26.5 · Sal 41.2 · Çar -41.4 · **Per 70.7 (1.7)** · Cum 23.7. UNG IS Per -21.0 (-1.7), OOS -33.0 (-1.4). Perşembe iki dönemde de en uç gün.
Düzeltme (hafta içi etiket permütasyonu, 2000 tekrar; skor = min(IS t, OOS t), gün-diğer farkı; 5 gün × 2 yön arasından en iyisi): KOLD skor 1.47, p = 0.045; UNG skor 1.33, p = 0.095. Ama bu yalnız 10 hücrelik ailenin düzeltmesi; K1'in 398 testlik taramasından seçildiği hesaba katılmıyor.

Saatlik (2023-12+, 148 EIA günü; bps, EIA / diğer, Welch t):
| ürün | Çar 16:00→Per 09:30 | 09:30→10:30 | 10:30→11:30 | 11:30→16:00 | toplam |
|---|---|---|---|---|---|
| KOLD | 16.7 / 13.0 (0.11) | 1.7 / 13.3 (-0.85) | **36.3 / -14.5 (2.08)** | **37.7 / -23.5 (2.06)** | 93.2 / -8.5 (1.92) |
| UNG | -2.1 / -1.1 (-0.05) | -0.1 / -7.8 (1.05) | -16.6 / 5.2 (-1.56) | -19.4 / 11.9 (-2.00) | -37.8 / 8.3 (-1.53) |
| BOIL | -14.0 / -9.9 | -4.8 / -11.6 | -36.2 / 11.3 (-1.93) | -38.3 / 18.0 (-1.94) | -95.4 / 9.0 (-1.99) |
Getiri gece ve açılışta değil, 10:30 duyurusundan sonra oluşuyor (mekanizmayla tutarlı); yarısı 11:30 sonrasında (makaledeki "+30 dk'da biter" bulgusundan farklı).

İşlenebilir kural (EIA'dan önceki kapanışta KOLD al, EIA kapanışında sat; net, bps):
| kesit | n | ort | medyan | geo | t | isabet | yıllık toplam | MDD | pozitif yıl |
|---|---|---|---|---|---|---|---|---|---|
| tüm 2011-10+ (15 bps) | 788 | 40.2 | 48.0 | 23.6 | 1.96 | 0.54 | %21.7 | -%68.2 | 0.73 |
| IS (15) | 534 | 31.5 | 37.6 | 17.6 | 1.37 | 0.54 | %17.7 | -%68.2 | 0.70 |
| OOS (15) | 254 | 58.5 | 56.0 | 36.3 | 1.40 | 0.54 | %29.7 | -%48.5 | 0.80 |
| 2024-26 (15) | 150 | 86.6 | 72.1 | 71.9 | 1.94 | 0.57 | %43.3 | -%28.1 | 1.00 |
| IS / OOS (30 bps) | 534 / 254 | 16.5 / 43.5 | | 2.6 / 21.3 | 0.72 / 1.04 | | %9.9 / %22.1 | -%74 / -%51 | 0.70 / 0.80 |
| kış IS / OOS (15) | 224 / 101 | 107.1 / 99.9 | | | 2.72 / 1.46 | 0.59 / 0.55 | | | |
| yaz IS / OOS (15) | 310 / 153 | -23.1 / 31.2 | | | -0.85 / 0.59 | | | -%74 (IS) | 0.40 / 0.80 |
| contango IS / OOS | 294 / 129 | 21.9 / 89.3 | | | 0.74 / 1.48 | | | | |
| contango değil IS / OOS | 240 / 125 | 43.2 / 26.6 | | | 1.19 / 0.46 | | | | |
| kayma haftaları hariç IS / OOS | 518 / 246 | 30.5 / 55.7 | | | 1.30 / 1.32 | | | | 0.70 / 1.00 |
En kötü 5 işlem (EIA günü, brüt): 2012-06-14 -%26.6 · 2022-07-07 -%25.6 · 2023-05-18 -%17.0 · 2022-01-27 -%16.5 · 2023-06-15 -%16.4. Kış farkı kısmen kışın zaten pozitif olan KOLD ortalamasından geliyor (kış 2012-21 koşulsuz +36.5 bps). Yaz IS negatif.
**Hüküm: İZLE.** Yön 2007'den beri tutarlı, getiri duyuru sonrasında oluşuyor, 10 hücrelik düzeltmede p ≈ 0.05-0.10. Ama IS t < 2 (fark t 1.73), OOS fark t 1.56, BH'yi geçmiyor, MDD IS'de -%68, 30 bps maliyette IS t 0.72. Tek başına para yatırılacak kural değil.

## B2. KOLD yapısal ortalama ve kuyruk
Yıl yıl ortalama günlük getiri bps (tüm / kış / yaz): KOLD 2012 18/107/-44 · 2013 -9/-60/26 · 2014 18/17/19 · 2015 32/32/33 · 2016 -15/8/-31 · 2017 30/35/26 · 2018 -8/9/-20 · 2019 33/51/21 · 2020 30/109/-26 · 2021 -34/56/-97 · 2022 -45/-51/-40 · 2023 74/201/-15 · 2024 17/13/19 · 2025 14/-41/52 · 2026 10/-46/39. BOIL yaklaşık ayna görüntüsü (2012 -22 · 2015 -38 · 2021 29 · 2022 28 · 2023 -77 · 2026 -11). KOLD 15 yılın 10'unda pozitif; kışın bile 2013, 2022, 2025, 2026'da negatif. Ortalama, UNG'nin negatif sürüklenmesinin -2 katı; ayrı bir avantaj değil (t 0.94 / 0.68).
| | en kötü 5 bir gün (%) | en kötü 5 üç gün (bitiş, %) | 3 günde ≤ -%20 |
|---|---|---|---|
| KOLD | 2026-01-20 -38.4 · 2018-11-14 -37.5 · 2020-08-03 -33.7 · 2012-06-14 -26.6 · 2022-07-07 -25.6 | 2026-01-21 -51.5 · 2018-11-14 -50.1 · 2020-08-05 -40.0 · 2021-09-27 -35.7 · 2022-01-31 -35.4 | günlerin %2.3'ü, 50 ayrı olay (yılda 3.3); 2022+ %4.6, yılda 6.2 |
| BOIL | 2026-02-02 -50.5 · 2018-11-15 -38.4 · 2022-06-14 -32.0 · 2022-06-30 -28.2 · 2022-05-09 -24.3 | 2026-02-04 -44.3 · 2022-12-06 -39.7 · 2022-02-07 -39.6 · 2021-12-01 -38.3 · 2022-06-14 -36.6 | %2.1, 49 olay (yılda 3.3); 2022+ %3.8, yılda 5.6 |

## B3. Gece boşluğu sonrası dönüş (A5)
| eşik | IS ort (t) n | OOS ort (t) n | 24-26 ort | OOS net | OOS ertesi gün gece / gün içi |
|---|---|---|---|---|---|
| 0.5 | 23.8 (1.28) 739 | 65.3 (1.49) 340 | 70.7 | 50.3 | 40.2 / 25.2 |
| 1 | 43.1 (1.53) 387 | 121.0 (1.92) 165 | 115.3 | 106.0 | 99.5 / 21.1 |
| 1.5 | 28.4 (0.64) 177 | 167.6 (1.71) 70 | 126.8 | 152.6 | 164.4 / 2.6 |
| 2 | -32.2 (-0.46) 94 | 300.2 (1.91) 32 | 307.3 | 285.2 | 216.2 / 84.4 |
Yıl yıl (eşik 1, brüt bps/n): 2012 132/35 · 2013 31/41 · 2014 88/41 · 2015 -62/34 · 2016 64/33 · 2017 -92/38 · 2018 129/46 · 2019 43/33 · 2020 57/40 · 2021 13/42 · 2022 158/38 · 2023 91/28 · 2024 12/36 · 2025 130/35 · 2026 229/28 (13/15 pozitif; ama KOLD'un koşulsuz ortalaması da pozitif: koşulsuza göre fazla IS 31.7 bps t 1.22, OOS 106.5 bps t 1.85).
Örtüşme: UNG kapanış z>2 olan 129 günün 102'si (%79) aynı zamanda gece z>1 günü. OOS'de etki z>1 kapanışlı günlerde (176 bps, t 1.98, n 94); yalnız gece boşluğu olan günlerde 48 bps (t 0.54, n 71). IS'de eşik arttıkça etki artmıyor (eşik 2'de negatif). OOS'de getirinin çoğu ertesi günün gece boşluğunda.
**Hüküm: İZLE.** A8 ile büyük ölçüde aynı olgu, bağımsız ikinci kanıt değil; IS zayıf ve eşikte monoton değil.

## B4. TTF sıçraması (A6)
OOS olayları (tarih TTF% UNG 3g%): 2022-02-24 51 -1.1 · 03-01 23 7.6 · 03-02 36 -0.4 · 06-14 16 -4.2 · 06-15 24 -8.8 · 07-26 13 -5.0 · 08-22 13 -4.4 · 11-14 16 5.5 · 2023-03-10 21 0.7 · 06-05 20 3.9 · 06-09 19 3.7 · 06-13 16 12.0 · 08-09 28 -5.6 · 10-09 15 -1.0 · 2024-04-11 8 -2.5 · 05-02 8 8.8 · 11-14 6 5.5 · 12-19 5 4.8 · 2025-01-13 7 9.4 · 01-21 7 2.2 · 01-29 6 5.3 · 02-27 9 10.8 · 06-20 6 -10.2 · 10-06 5 -4.2 · 2026-01-12 7 -7.9 · **01-16 11 30.0** · 01-21 9 8.7 · 03-02 39 0.4 · 03-03 22 3.8 · 08-10 9 -1.7.
UNG OOS 220 bps (t 1.45), medyan 147; en büyük olay çıkınca 125, en büyük 2 çıkınca 86. Bir yıl dışarıda: -2022 350 · -2023 219 · -2024 190 · -2025 220 · -2026 136. Toplam getiri payı: 2022 -%16 (8 olay), 2026 %51 (6 olay). Bir gün gecikmeli giriş: OOS 49 bps (t 0.32). 2022'de TTF'nin 185 günü hacim 0 (yalnız uzlaşma fiyatı); K1'in yüksek sonucu bu dönemi dışarıda bırakmaktan geliyor; 2022 olayları çoğunlukla negatif.
**Hüküm: KULLANILAMAZ.** Yeniden üretilemedi; OOS t veri temizliği seçimine göre 1.10-1.80 arasında, hiçbir varyantta IS t ≥ 2 yok; sonuç 2026 Ocak kümesine bağlı.

## B5. Büyük yukarı gün sonrası dönüş (A8)
Yıl yıl (UNG ertesi gün bps/n): 2007 -146/5 · 2008 -231/6 · 2009 -66/9 · 2010 34/4 · 2011 -28/5 · 2012 -116/6 · 2013 38/8 · 2014 -155/10 · 2015 62/8 · 2016 17/8 · 2017 -5/7 · 2018 103/16 · 2019 -52/6 · 2020 179/9 · 2021 -80/13 · 2022 -280/8 · 2023 43/6 · 2024 -482/7 · 2025 -179/5 · 2026 -237/10.
2007-2011.09 n 27, -98 bps; IS n 93, 5.5; OOS n 36, -239 (medyan -160; en iyi ve en kötü 3 çıkınca -180). IS-OOS fark t 2.21. z (2,3]: IS +53 / OOS -285; z>3: IS -147 / OOS -101. OOS'de UNG σ60 medyanı 373 bps (IS 228); z>2 gün oranı %3.6 → %2.9. KOLD ile OOS 342 bps (t 1.87).
**Hüküm: İZLE (yalnız OOS).** OOS'de birkaç uç olaya bağlı değil, ama 2012-2021'de 10 yılın 5'i negatif 5'i pozitif; rejim (yüksek oynaklık) açıklaması makul ama kanıtlanmadı. 36 olay ve 398 test içinden sonradan seçildi.

## B6. Risk tablosu 2022+ (%)
| | 1g sd | 1g %5 | 1g %1 | 1g en kötü | 3g sd | 3g %5 | 3g %1 | 3g en kötü |
|---|---|---|---|---|---|---|---|---|
| UNG | 3.94 | -6.27 | -9.31 | -24.85 | 6.69 | -10.24 | -15.15 | -21.47 |
| BOIL | 7.25 | -11.56 | -16.74 | -50.53 | 12.51 | -18.40 | -30.35 | -44.26 |
| KOLD | 7.26 | -11.66 | -16.98 | -38.35 | 12.38 | -19.67 | -27.76 | -51.47 |
| EQT | 2.55 | -3.98 | -7.05 | -11.48 | 4.48 | -6.89 | -11.97 | -15.06 |
| CRK | 3.64 | -5.92 | -9.39 | -16.65 | 6.51 | -10.37 | -15.80 | -22.03 |
| AR | 2.91 | -4.48 | -8.11 | -13.74 | 5.10 | -8.48 | -12.86 | -18.69 |
| EXE | 2.12 | -3.32 | -5.78 | -9.53 | 3.62 | -5.56 | -9.43 | -12.32 |
Gece payı (var(kapanış→açılış) / var(kapanış→kapanış)): UNG %57, BOIL %55, KOLD %55 (gece sd: UNG 2.99, BOIL 5.38, KOLD 5.41; gün içi 2.53 / 4.79 / 4.77). Kapanışta alan kişi riskin yarıdan fazlasını piyasa kapalıyken taşıyor; stop emri bu kısmı korumaz.

## K1 ile uyuşmayanlar ve açık kalanlar
- A6 (TTF) yeniden üretilemedi (OOS UNG 391 → 220; BOIL 782 → 454). Kaynak: hacmi 0 olan TTF günlerinin (2022'de 185) ele alınışı ve getiri tanımı. K1'in kesin varyantı (51 olay, 782 bps) bulunamadı.
- A2 KOLD h=3 işareti pencere fazına bağlı (-1.9 / 3.6 / 1.5); K1'in 3.59'u bir fazın sonucu.
- z tanımı: K1 log getiri, K2 basit getiri; A5 ve A8'de OOS t 2.02 → 1.92 ve -2.32 → -2.23 (eşik altına inme yok).
- Açık: gerçek EIA yayın takvimi (tatil kaymaları varsayım); T2 adayı (orta oynaklıkta yukarı gün → KOLD) ayrıca sınanmadı, ama A8 ile aynı günlere dayanıyor; TTF saat damgası K1/M1'e güvenilerek kabul edildi.
