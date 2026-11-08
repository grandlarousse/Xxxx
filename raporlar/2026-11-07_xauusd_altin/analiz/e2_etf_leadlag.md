# e2_etf_leadlag — ABD altın ETF'leri (Midas cephesi): öncü bilgiler ve 1/3/5 günlük stratejiler

**Özet.** Bu cephede tek sağlam öncü ilişki **madencilerden altına** gidiyor. GDX ya da GDXJ, altına (GLD) ve hisse piyasasına (SPY) göre beklenenden iyi gidince sonraki 3–5 günde altın ve madenciler yükseliyor. Kötü gidince tersi oluyor. İşaret 19 yılın 15'inde aynı. Beta penceresini, dönemi (60/120/250/500 gün), GDX ya da GDXJ'yi, ABD ya da Asya madencilerini değiştirince ve gün içi sürümde de işaret aynı kalıyor. Ayrıştırma testi (s10) bir şeyi netleştiriyor: sinyal madencinin *kendine özgü* ileri getirisini öngörmüyor, **altının** ileri getirisini öngörüyor. GDX ve GDXJ, altına yaklaşık 2 kat beta taşıdıkları için aynı bilgiyi daha yüksek oynaklıkla taşıyor.

Diğer bütün aileler OOS'ta tutmadı:
- gün içi makro göreli değer artığı,
- gecikmeli dolar, faiz, VIX, petrol, BTC ve Avrupa/Asya kapanışları,
- Şanghay primi,
- VİOP bazı ve gram altın primi,
- COT,
- GLD pay akışı.

Bu aileler ya hiç işe yaramadı ya da yalnız IS'te çalıştı. **Ters ETF'li (GLL/DUST/JDST/ZSL) sürümler neredeyse her stratejide yalnız-uzun sürümden kötü.** Bunun iki nedeni var: kısa bacağın sinyali zayıf ve DUST/JDST/ZSL yılda %35–50 log aşınma taşıyor. Midas için pratik sonuç: kısa sinyali "nakitte kal" diye kullanın.

Toplam kayıtlı hipotez testi: **1.030** (`out/registry/e2_etf_leadlag.csv`). Ajan içi BH-FDR sonucu: q<0,05 olan 67, q<0,10 olan 120 test. Testler yüksek korelasyonlu; pozitiflerin büyük kısmı aynı "madenci artığı" kümesinin varyantları.

---

## 1. Yöntem

**Zaman çizelgesi (ET / UTC).** Giriş gün t ABD kapanışında (16:00 ET; yazın 20:00, kışın 21:00 UTC), çıkış t+h kapanışında (h=1,3,5 NYSE günü). Karar anı gün t 15:00 ET (19:00/20:00 UTC). Hedef `log(c_T,t+h / c_T,t)`, adjclose (temettü dahil). `c_*` sütunları sinyalde kullanılmadı; ABD varlıklarında yalnız t-1 kapanışı (`shift(1)` ya da `y_*`) kullanıldı. `y_*_avail < cut_utc` her gün ve her sütun için denetlendi, **ihlal 0** (`s0_avail_ihlal.json`).

**Bilgi zamanları:**

| Öngörücü | Bilgi anı | ET | UTC |
|---|---|---|---|
| GDX/GDXJ/GLD/SLV/SIL/SPY kapanış artıkları (aile a) | t-1 kapanış | t-1 16:00 | t-1 20:00/21:00 |
| Asya madencileri 2899.HK, 1818.HK | gün t HK kapanışı | t 03:10/04:10 | t 08:10 |
| Asya madencisi 600547.SS, SHFE AU0, `xau_07utc`, `dk_USDCNH_p07` | gün t Şanghay kapanışı | t 02:00/03:00 | t 07:00 |
| Spot altın `xau_cut`, Dukascopy `dk_*_cut` (aile b1) | cutoff | t 15:00 | t 19:00/20:00 |
| ETF saatlik fiyatı, son 730 gün (aile b2): 13:30 barının kapanışı | — | t 14:30 | t 18:30/19:30 |
| ABD vadelileri ve DXY (Yahoo) | t-1 kapanış (17:00 ET varsayımı) | t-1 17:00 | t-1 21:00/22:00 |
| VIX/GVZ/OVX | t-1 kapanış | t-1 16:15 | — |
| BTC | t-1 UTC günü sonu | — | t 01:00 |
| `ust_*` | t-1 değeri | — | t-1 22:00 |
| Avrupa kapanışları | gün t | t 11:30 | 15:30/16:30 |
| VİOP uzlaşması | gün t | — | ≈15:05–15:15 |
| COT | Cuma yayını; Pazartesi'den itibaren kullanılır | — | Cuma 21:00 |
| GLD pay sayısı | t-1 (ayrıca t-2 gecikmesi test edildi) | — | t-1 23:00 |

**İstatistik.** `lib_altin.split_stats` kullanıldı. Ölçüt Spearman IC; t değeri rank-OLS üzerinde Newey-West, lag = max(h,5) ile hesaplandı. Dönemler IS = 2008–2017 (`lib_altin.IS_END=2017-12-31`), OOS = 2018–2026-11, ayrıca 2022+ alt dönemi.
- Dukascopy çapraz varlıkları 2016/2018'de başladığı için **b1 ailesinde** sözde-IS 2018–2021, OOS 2022+ alındı.
- VİOP verisi 2017-03'te başladığı için **d ailesinde** de 2017-03..2021 / 2022+ ayrımı kullanıldı.
- Saatlik **b2 ailesinde** (723 gün) ilk ve ikinci yarı karşılaştırıldı. Bu aile yalnız keşif amaçlı.

Kısmi testler rank-gauss dönüşümlü NW-OLS ile yapıldı (s5b). İleriye bakma denetimi için `placebo_lead` kullanıldı.

**Strateji.**
- Eşikler yalnız IS dağılımından alındı: sinyal IS q-kantilinin üstündeyse ±1, (1−q)-kantilinin altındaysa ∓1. İşaret IS IC'sinden geliyor.
- Parametre ızgarası (k formasyon, h tutuş, q) IS'te taranıp en iyi IS net Sharpe seçildi. OOS bir kez değerlendirildi. Izgaranın tamamının OOS'u yalnız şeffaflık için `s9_grid_oos.csv`'de.
- Uygulama kademeli (h alt portföy), `lib_altin.backtest` ile yapıldı.
- Üç sürüm var:
  1. *ideal* ±1 dayanak (açığa satış varsayımsal, sinyal kalitesi ölçüsü),
  2. *yalnız uzun* (değilse nakit, nakit getirisi 0),
  3. *uzun + ters ETF* (kısa yönde GLL/DUST/JDST/ZSL; ağırlık = 1/|geçmiş 60 günlük beta|, yani ≈ −1x maruziyet).
- Maliyet gidiş-dönüş: dayanak ETF'te 10 bps (stres 20), ters ETF'te 20 bps (stres 40).
- Her sürümün drift çıkarılmış (demeaned) Sharpe'ı ve buy & hold kıyası raporlandı.

**Güven etiketi.** Görevdeki kural uygulandı, üzerine bir drift koruması eklendi. YUKSEK için ayrıca yalnız-uzun OOS Sharpe'ın B&H'yi geçmesi ya da demeaned yalnız-uzun Sharpe'ın 0,2'den büyük olması, ve ideal OOS net Sharpe'ın 0,3'ten büyük olması istendi.

---

## 2. Temel: buy & hold ve ters ETF'lerin gerçekleşen kaldıracı

| ETF | IS 2008–17 yıllık / Sharpe | OOS 2018+ yıllık / Sharpe | 2022+ Sharpe |
|---|---|---|---|
| GLD | %3,8 / 0,20 | %12,5 / 0,73 | 0,83 |
| GDX | −%6,9 / −0,16 | %16,0 / 0,41 | 0,56 |
| GDXJ | −%10,5 / −0,22 | %14,2 / 0,31 | 0,47 |
| SLV | %0,5 / 0,02 | %12,2 / 0,35 | 0,41 |

OOS'ta güçlü bir drift var; uzun ağırlıklı her kural iyi görünür. Bu yüzden demeaned Sharpe kritik.

**Ters ETF'ler.** 3 günlük örtüşmeyen getirilerde beta ve log aşınma (β × dayanak getirisine göre, yıllık):

| Ters ETF | 2008–2019 | 2020-04+ | 2022+ |
|---|---|---|---|
| GLL | β=−2,00, aşınma −%9,5 | β=−1,99, −%2,0 | −%1,1 |
| DUST | β=−2,94 (3x dönemi), −%91 | β=−2,01, −%35 | −%34 |
| JDST | β=−3,07, −%157 | β=−2,00, −%49 | −%47 |
| ZSL | β=−1,95, −%32 | −%40 | −%39 |

1/3/5 günde gerçekleşen kaldıraç nominale çok yakın (`s0_kaldirac.csv`). GLL kabul edilebilir. **DUST, JDST ve ZSL birkaç günden uzun tutmak için çok pahalı.**

---

## 3. Aile sonuçları (test sayısı; p<0,05 ve q<0,10 adedi)

### (a) Madenci–altın göreli artığı: 245 + 45 kısmi test (p<0,05: 92; q<0,10: 56)

e_t = r_Y,t − β_{t-1}·r_X,t. Yuvarlanan beta yalnız geçmişle hesaplandı: tek faktörlüde 120 gün, GLD+SPY iki faktörlüde 250 gün. Sinyal t-1'de biten k günlük toplam.

| Sinyal → hedef | IC | t tam | t IS | t OOS | t 2022+ | Yıl |
|---|---|---|---|---|---|---|
| GDX~GLD+SPY k10 → **GLD** h5 | 0,101 | 3,93 | 3,46 | 1,94 | 2,63 | 15/19 |
| GDX~GLD+SPY k3 → GLD h3 | 0,061 | 3,07 | 1,60 | 2,79 | 2,55 | 16/19 |
| GDXJ~GLD+SPY k1 → GLD h3 | 0,051 | 3,32 | 0,99 | 3,84 | 3,61 | 13/17 |
| GDX~GLD (SPY'siz) k10 → GLD h5 | 0,072 | 2,78 | 2,45 | 1,31 | 2,09 | 11/19 |
| GDX~GLD+SPY k3 → **GDX** h3 | 0,063 | 3,29 | 2,24 | 2,34 | 1,66 | 15/19 |
| GDXJ~GLD+SPY k1 → **GDXJ** h3 | 0,053 | 3,47 | 1,90 | 3,04 | 2,54 | 15/17 |
| SLV~GLD, SIL~SLV, GDXJ~GDX (her k ve h) | — | çoğunlukla \|t\|<2, OOS işaret dağınık | — | — | — | — |

- **SPY ayıklaması önemli.** Hisse piyasası betası çıkarılmazsa sinyal zayıflıyor.
- **Beta penceresi duyarlılığı** (k10 → GLD h5): W=60'ta t 4,24 (OOS 1,97), W=500'de t 3,81 (OOS 2,03). Sonuç pencereden bağımsız.
- **Uç dönemler dışlanınca** (2008 Eyl–Ara, 2013 Nis–Haz, 2020 Şub–Nis, 2026 Oca–Şub) t 3,51 (IS 3,10, OOS 1,74).
- **Kısmi test (s5b, rank).** GLD'nin kendi k günlük getirisi ve gün içi altın kontrol edildiğinde artık → GLD h5 için t 4,03, IS 3,40, OOS 2,12, 2022+ 2,50. GLD'nin kendi 5–10 günlük getirisi tek başına öngörü taşımıyor (t −0,5 ile −1,1). Yani bulgu altının kendi dönüşü değil; bilgi madencilerden geliyor.
  - Ham OLS sürümü (s5_derin_a P1–P2) artığın bileşenlerini kontrol olarak koyduğu için çoklu doğrusallıktan anlamsız. Kayıtta duruyor ama yorumlanmadı.
- **Ayrıştırma (s10).** Madenci artığı GDX'in ileri *artığını* öngörmüyor: OOS t −1,0 ile +0,5, 2022+ negatif. Öngördüğü şey ileri GLD getirisi (t ≈ 3). "Madenci artık momentumu" sektöre özgü bir momentum değil; altın kanalından geçen aynı öncülük.
- **Asya'da tekrar (s7).** Zijin (2899.HK), Zhaojin (1818.HK) ve Shandong (600547.SS) için gün t artığı, aynı penceredeki altın (07 UTC) ve yerel endekse göre hesaplandı. Sonuç → GLD h3: t 3,29, IS 2,08, OOS 2,48, 2022+ 3,27. → GDX h3: t 3,19, OOS 2,43. Bu bilgi cutoff'tan 11–12 saat önce biliniyor ve ABD madenci artığıyla kısmen örtüşüyor: kısmi testte Asya t 1,95 ve ABD t 2,54 (k5, h3).
- **Gecikmeli çapraz getiriler.** GLD'nin 5 günlük getirisi → GDX/GDXJ h5 negatif (t −3,2/−3,4). Bu, artığın "−β·GLD" bileşeni. Altın madencilerin onayı olmadan yükselirse geri veriyor.

### (b) Gün içi senkron göreli değer, cutoff 15:00 ET: 114 test (p<0,05: 17)

- **b1 (2016/2018+).** Altının [t-1 15:00 → t 15:00 ET] hareketi, aynı penceredeki DXY, T-bond, S&P, USDJPY, gümüş, BTC, bakır ve Brent'le yuvarlanan 250 günlük modele oturtuldu. Modelin artığı → GLD/GDX/SLV:
  - Sözde-IS 2018–21'de GDX h1 t 4,6 gibi değerler var.
  - **OOS 2022+'da çöküyor** (OOS t −2,0 ile +0,9; 72 testin hiçbiri OOS'ta \|t\|≥2 ve IS ile aynı işarette değil).
  - **Sonuç: YOK.**
- **Ham gün içi altın** [t-1 16:00 → t 15:00 ET] → GDX h1: IC −0,055, t −3,84 (IS −3,41, OOS −1,86). GDX ertesi gün aynı gün altın hareketini geri veriyor; olası nedenler kaldıraçlı ETF yeniden dengelemesi ve aşırı tepki. Strateji olarak ise yılda 105 gidiş-dönüş gerektiriyor; ideal OOS Sharpe 0,12, stres maliyette −0,23. Rank kısmi testte t −2,2 (OOS −1,4). **DUSUK.**
- **b2 (son 723 gün, ETF saatlik, t 14:30 ET'ye kadar).** GDX~GLD+SPY gün içi artığı → GLD h5 t 2,74, GDX h5 t 2,36. GDXJ sürümü → GLD h5 t 3,19. SIL~SLV → SIL h1 t 2,30. İlk yarı güçlü, ikinci yarı zayıf (OOS t 0,5–0,9). Keşif amaçlı; aile (a) ile tutarlı.
- **C1 sinyaliyle birleşim (son 723 gün, h5).** C1 tek başına IC 0,188 (t 2,83), gün içi artık eklenince IC 0,206 (t 3,06). Gün içi güncelleme küçük bir katkı yapıyor.

### (c) Gecikmeli çapraz varlıklar: 504 test (p<0,05: 75; q<0,10: 25)

Değişkenler: dolar (DXY, UUP), faiz (UST 2/10, reel 10, başabaş, eğri), TLT, TIP, VIX, GVZ, OVX, MOVE, S&P, NDX, HYG, EEM, FXI, petrol, bakır, platin, BTC. Avrupa (DAX, STOXX, FTSE, Xetra-Gold, SGLN/PHAU). Asya (Nikkei, HSI, KOSPI, ASX, SSE, 518880.SS, 2840.HK, 1328.T ve Çinli madenciler). SHFE primi ve Çin ETF primi. Her biri 1 ve 5 günlük değişimle (VIX/GVZ'de seviye z ile) test edildi.

- **GLD hedefi.** 252 testin 19'u \|t\|≥2; IS ve OOS'ta birlikte \|t\|≥2 ve aynı işaretli tek test: UST2 5 günlük değişim → GLD h1, t −2,92 (IS −2,16, OOS −2,10, IC −0,044). Zayıf; **DUSUK**.
- **Avrupa ve Asya endeksleri, Asya altın ETF'leri, Xetra-Gold, Londra ETC'leri, SHFE primi ve Çin ETF primi → GLD: YOK.** \|t\|<2,6 ve OOS'ta tutarsız. Beklenen senkronsuzluk tuzağı doğrulandı: bu bilgi gün t 16:00 ET GLD kapanışına zaten giriyor.
- **GDX hedefi.** Çok sayıda 5 günlük "risk/emtia rallisi" değişkeninin IC'si negatif: platin, Japonya ve HK altın ETF'leri, FXI, EEM, Nikkei, HSI, WTI, SPY.
  - En güçlüsü **platin 5 günlük → GDX h3**: IC −0,085, t −4,18, IS −1,99, OOS −3,87, 14/19 yıl, q=0,009.
  - Rank kısmi testte (GLD5, GDX5, SPY5, gün içi altın ve madenci artığı kontrol edilince) t −2,9 ile −3,4 arasında, IS ise −1,3 ile −1,5.
  - 2013–2017'de işaret ters (IC −0,034); güçlü bir mekanizma bulunamadı. 500 testin en üstünde. **DUSUK** (veri madenciliği şüphesi).

### (d) VİOP bilgisi: 48 test (p<0,05: 4; q<0,10: 0)

Test edilenler: baz, fazla carry'nin 20 günlük sapması, baz değişimi, hacim z, toplam OI değişimi, gram altın primi (seviye z, d1, d5) → GLD/GDX. OOS'ta yalnız toplam OI d1 → GDX h3 t 2,69; IS'te 0,20 ve gram prim z → GDX h3 t 1,84. **Sonuç: YOK.** Yurt içi talep ve VİOP konumlanması ABD ETF'lerini öngörmüyor.

### (e) COT: 48 test (p<0,05: 0)

MM net/OI z (750 gün), haftalık değişim ve IS %10/%90 uçları → GLD/GDX, h=1,3,5,10. Hükümet kapanması dönemleri dahil de hariç de \|t\|≤2,25. IS işaretleri OOS'la çelişiyor. **YOK.**

### (f) GLD pay akışı, ek: 18 test (p<0,05: 0)

Pay değişimi (t-1 ve t-2 gecikmeli) ve 5 günlük toplam. \|t\|<1,7. **YOK.**

---

## 4. Adaylar: IS'te seçilen konfigürasyon, OOS tek seferde

IC istatistikleri (seçilen konfigürasyon):

| Kod | Sinyal → hedef (k, h, q) | IC | t tam | t IS | t OOS | t 22+ | Yıl | q_FDR |
|---|---|---|---|---|---|---|---|---|
| C1 | GDX~GLD+SPY k10 → GLD (h5, q0,8) | 0,101 | 3,93 | 3,46 | 1,94 | 2,63 | 15/19 | 0,010 |
| C1j | GDXJ~GLD+SPY k10 → GLD (h5, q0,7) | 0,088 | 3,30 | 3,49 | 1,07 | 2,53 | 10/17 | 0,026 |
| C2 | GDX~GLD+SPY k3 → GDX (h3, q0,7) | 0,063 | 3,29 | 2,24 | 2,34 | 1,66 | 15/19 | 0,026 |
| C2j | GDXJ~GLD+SPY k1 → GDXJ (h3, q0,7) | 0,053 | 3,47 | 1,90 | 3,04 | 2,54 | 15/17 | 0,021 |
| C5 | Asya madenci artığı k1 → GLD (h3, q0,7) | 0,051 | 3,29 | 2,08 | 2,48 | 3,27 | 12/19 | 0,026 |
| C4 | −Platin 5 günlük → GDX (h3, q0,8) | 0,085 | 4,18 | 1,99 | 3,87 | 1,82 | 14/19 | 0,009 |
| C3 | −gün içi altın → GDX (h1, q0,7) | 0,055 | 3,84 | 3,25 | 2,05 | 1,86 | 15/19 | 0,012 |

**Alt dönem IC (t):**

| Kod | 2008–12 | 2013–17 | 2018–21 | 2022–24 | 2025–26 |
|---|---|---|---|---|---|
| C1 | 0,063 (1,2) | 0,191 (4,0) | −0,017 (−0,3) | 0,026 (0,4) | 0,222 (2,7) |
| C2 | 0,015 (0,4) | 0,106 (2,8) | 0,065 (1,7) | 0,051 (1,1) | 0,059 (0,9) |
| C2j | −0,006 | 0,068 (2,4) | 0,055 (1,8) | 0,098 (2,9) | 0,028 (0,6) |
| C5 | 0,068 (2,1) | 0,023 (0,9) | −0,003 | 0,057 (1,6) | 0,149 (3,1) |

**C1 ve C5 yüksek oynaklık rejimlerinde çalışıyor** (2008, 2013–17, 2025–26); 2018–2024'te yaklaşık sıfır. **C2 ve C2j dönemlere daha eşit yayılmış.**

### Strateji sonuçları (OOS 2018–2026, net Sharpe)

Yalnız-uzun sürümler için demeaned Sharpe ayrı sütunda; maliyet temel, parantez içi stres.

| Kod | İdeal ±1 | İdeal demeaned | **Yalnız uzun** | Yalnız-uzun demeaned | **Uzun + ters ETF** | Kısa bacak (ters ETF) | B&H | Maruziyet | Yıllık işlem |
|---|---|---|---|---|---|---|---|---|---|
| C1 (GLD) | 0,53 (0,42) | 0,50 | **0,73 (0,65)** | 0,37 | 0,49 (0,38) | 0,01 | 0,72 | %19 | 11 |
| C1j (GLD) | 0,42 (0,30) | 0,38 | 0,61 (0,51) | 0,15 | 0,39 | −0,03 | 0,72 | %27 | 12 |
| C2 (GDX) | 0,56 (0,42) | 0,53 | **0,58 (0,47)** | 0,29 | 0,24 (0,10) | −0,20 | 0,41 | %31 | 34 |
| C2j (GDXJ) | 0,58 (0,41) | 0,56 | **0,64 (0,53)** | 0,40 | −0,09 (−0,22) | −0,50 | 0,31 | %28 | 33 |
| C5 (GLD) | 0,51 (0,06) | 0,47 | 0,84 (0,57) | 0,27 | 0,47 (0,02) | −0,29 | 0,72 | %33 | 35 |
| C4 (GDX) | 0,86 (0,75) | 0,87 | 0,69 (0,62) | 0,48 | 0,71 (0,61) | 0,26 | 0,41 | %26 | 23 |
| C3 (GDX) | 0,12 (−0,23) | 0,14 | 0,37 (0,13) | 0,17 | −0,19 | −0,59 | 0,41 | %26 | 105 |

**2022+ alt dönemi** (temel maliyet; yalnız uzun / uzun + ters / B&H):

| Kod | Yalnız uzun | Uzun + ters | B&H |
|---|---|---|---|
| C1 | 0,79 | 0,79 | 0,85 |
| C2 | 0,57 | 0,38 | 0,58 |
| C2j | 0,74 | 0,35 | 0,49 |
| C5 | 1,29 | 0,91 | 0,85 |
| C4 | 0,77 | 0,58 | 0,58 |

**IS dönemi** (2008–2017, seçim yapılan dönem; ideal / yalnız uzun):

| Kod | İdeal | Yalnız uzun |
|---|---|---|
| C1 | 0,79 | 0,78 |
| C2 | 0,39 | 0,30 |
| C2j | 0,70 | 0,47 |
| C5 | 0,27 | 0,26 |
| C4 | 0,40 | 0,26 |

**Izgara sağlamlığı** (`s9_grid_oos.csv`; 8 konfigürasyonun OOS ideal Sharpe medyanı):

| Kod | OOS medyan | IS medyan | Not |
|---|---|---|---|
| C1 | 0,40 | 0,68 | k10 varyantları k5'ten iyi |
| C2 | 0,50 | 0,01 | IS'te zayıf; h1 varyantları IS'te negatif |
| C2j | 0,53 | 0,33 | — |
| C5 | 0,64 | 0,09 | IS'te çok zayıf |

**"Uzun-varsayılan" kaplama** (GLD tut, yalnız C1 ayı sinyalinde nakit; maruziyet %84):

| Dönem | Sharpe | Yıllık getiri | Maks. düşüş |
|---|---|---|---|
| OOS | 0,90 (B&H 0,72) | %12,9 (B&H %12,4) | −%22,8 (B&H −%33,2) |
| 2022+ | 1,24 (B&H 0,85) | — | — |
| IS | 0,47 (B&H 0,19) | — | — |

Midas'ta GLD tutan biri için en pratik kullanım bu. Yine de 2018–2024'te katkısı küçük.

### Yıllık getiriler (%, temel maliyet)

C1 (GLD):

| | 2008 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ideal | 31,1 | −1,0 | 4,2 | −10,6 | 0,5 | 16,8 | 12,0 | 19,1 | −2,0 | 19,2 | −2,6 | −0,9 | 6,2 | −1,3 | −1,2 | −0,6 | −3,5 | 18,8 | 30,3 |
| uzun | 18,2 | 3,2 | 5,2 | −4,0 | 4,6 | −1,6 | 7,0 | 9,1 | 1,3 | 10,9 | −0,3 | 4,0 | 7,0 | 2,1 | −2,4 | −0,5 | 1,4 | 17,1 | 12,2 |
| B&H | 1,1 | 21,5 | 25,7 | 9,1 | 6,4 | −33,3 | −2,2 | −11,3 | 7,7 | 12,1 | −2,0 | 16,4 | 22,2 | −4,2 | −0,8 | 11,9 | 23,6 | 49,3 | −6,2 |

C2j (GDXJ):

| | 2010 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ideal | 4,0 | 17,6 | −29,2 | 42,4 | 18,4 | −10,6 | 30,2 | 46,9 | 4,8 | 5,4 | 13,4 | 9,7 | 20,6 | −1,6 | 33,2 | 4,2 | 12,9 |
| uzun | 10,6 | 12,9 | −11,7 | 5,1 | −5,6 | −5,4 | 33,0 | 34,7 | 11,7 | 3,9 | 11,7 | 5,1 | 7,3 | 0,9 | 16,5 | 34,6 | 2,9 |
| uzun+JDST | 10,6 | 12,9 | −11,7 | 2,6 | −11,1 | −26,2 | 10,0 | 39,1 | 1,9 | 1,6 | **−62,2** | 4,7 | 11,7 | −4,9 | 28,6 | −2,6 | −0,3 |
| B&H | 51,3 | −41,5 | −18,4 | −93,6 | −25,3 | −21,2 | 54,8 | 7,9 | −11,7 | 34,0 | 26,5 | −23,9 | −15,7 | 6,9 | 14,6 | 100,2 | −5,5 |

C2 (GDX), ideal: 2018 7,0 · 2019 −2,1 · 2020 32,6 · 2021 6,6 · 2022 −18,0 · 2023 −2,6 · 2024 31,3 · 2025 35,5 · 2026 26,1.

### Uç dönemler (pencere toplam getirisi, %)

| | 2008 GFC | 2013 Nis–Haz | 2020 Şub–Nis | 2026 Oca–Şub |
|---|---|---|---|---|
| C1 ideal / uzun / uzun+GLL / B&H | 14,4 / 10,2 / 10,2 / 5,7 | 13,4 / −2,1 / 12,3 / −26,0 | 3,4 / 1,1 / 1,6 / 4,5 | 12,2 / 11,2 / 10,5 / 19,9 |
| C2 (GDX) | 3,5 / 3,8 / 3,8 / −10,5 | −1,5 / −8,0 / −7,4 / −43,5 | 0,7 / 0,6 / **−22,8** / 8,1 | 33,7 / 26,9 / 30,4 / 30,1 |
| C2j (GDXJ) | — | 20,6 / −6,7 / −6,7 / −60,3 | 5,2 / −0,3 / **−64,3** / −8,7 | 23,4 / 21,3 / 18,1 / 31,7 |
| C5 (GLD) | 22,0 / 13,8 / 13,8 / 5,7 | −1,3 / −8,1 / −2,2 / −26,0 | 9,0 / 3,7 / 8,3 / 4,5 | 7,7 / 12,9 / 5,5 / 19,9 |

Uç dönemler yalnız-uzun ve ideal sürümleri bozmuyor. Ters ETF sürümü (özellikle Mart 2020'de JDST/DUST) felaket olabiliyor.

### Placebo (IC, sinyal s gün kaydırılmış; s<0 = gelecek bilgisi)

| Kod | s=−2 | s=−1 | s=0 | s=+1 | s=+2 | s=+3 |
|---|---|---|---|---|---|---|
| C1 | 0,117 | 0,107 | **0,101** | 0,098 | 0,087 | 0,074 |
| C2 | 0,206* | 0,050 | **0,063** | 0,044 | 0,023 | 0,014 |
| C2j | 0,325* | 0,019 | **0,053** | 0,047 | 0,027 | −0,001 |
| C5 | 0,044 | 0,086 | **0,051** | 0,024 | 0,008 | 0,004 |
| C3 | 0,001 | −0,751* | **0,055** | 0,011 | 0,009 | 0,019 |

\* Hedef penceresiyle mekanik örtüşme.

Sızıntı belirtisi yok. C1 yavaş sönüyor; bu, uzun ömürlü bir sinyale işaret ediyor ve giriş zamanlamasına duyarlı değil. C3 yalnız s=0'da var.

---

## 5. Güven etiketleri

| Kod | Etiket | Gerekçe |
|---|---|---|
| **C2j** madenci artığı (GDXJ) → GDXJ 3 gün, yalnız uzun | **YUKSEK** | Tüm kural maddeleri ve drift koruması sağlanıyor: \|t\|=3,47, OOS 3,04, 15/17 yıl, yalnız-uzun OOS 0,64 > B&H 0,31, demeaned 0,40, stres 0,53, 2022+ t 2,54. Uç dönemler hariç t 3,43. **Ters ETF (JDST) sürümü kullanılmamalı.** Mekanizma altın kanalı (ayrıştırma). |
| **C2** madenci artığı (GDX) → GDX 3 gün, yalnız uzun | **ORTA** | Sayısal kural YUKSEK'i karşılıyor (t 3,29 / IS 2,24 / OOS 2,34 / 15/19 / yalnız uzun 0,58 > B&H 0,41). Ama ızgara IS medyanı ≈0; 2022+ t 1,66 ve yalnız uzun 2022+'da B&H'yi geçmiyor; idiosenkratik bileşen yok. Bilerek bir kademe indirildi. |
| **C1** madenciler → GLD 5 gün | **ORTA** | t 3,93, IS 3,46, kısmi t 4,03; ama IS'te seçilen konfigürasyonun OOS t'si 1,94 (<2) ve 2018–2024'te IC ≈0. Kaplama sürümü pratikte faydalı. |
| **C5** Asya madencileri (gün t 07–08 UTC) → GLD 3 gün | **ORTA** | t 3,29, OOS 2,48, 2022+ 3,27; ama 12/19 yıl (<%70), stres maliyette ideal OOS 0,06 ve ızgara IS medyanı 0,09. C1 için bağımsız teyit değerinde. |
| C4 −platin 5 günlük → GDX | **DUSUK** | İstatistik güçlü (t 4,18, OOS 3,87); fakat mekanizma yok, 2013–17'de işaret ters, 500 testin en üstü. |
| C3 −gün içi altın → GDX ertesi gün | **DUSUK** | IC anlamlı ama maliyet sonrası işlem değeri yok: ideal stres −0,23, yalnız uzun < B&H. |
| UST2 5 günlük → GLD h1 | **DUSUK** | IS/OOS t ≈ −2,1; ekonomik büyüklük küçük. |
| Diğer her şey | **YOK** | b1 makro artık, VİOP, COT, akış, Avrupa/Asya endeksleri, SHFE primi. |

## 6. Midas kullanıcısı için pratik okuma

1. Her gün ABD kapanışından sonra GDX ve GDXJ'nin GLD ve SPY'ye göre artığını hesaplayın. Beta yuvarlanan 250 günlük ve yalnız geçmiş verilerle olmalı. Bu sinyal ertesi gün 15:00 ET'den yaklaşık 23 saat önce hazır olur; girişi ertesi gün kapanışa yakın yapın.
2. Kullanım:
   - (a) GDXJ'de 1 günlük artık IS %70 kantilinin üstündeyse 3 gün uzun tutun, değilse nakitte kalın (C2j).
   - (b) GLD tutuyorsanız 10 günlük GDX artığı IS %20 kantilinin altına inince nakite geçin (C1 kaplama).
3. **Kısa yön için DUST/JDST/ZSL kullanmayın.** Kısa bacakların OOS Sharpe'ı negatif ve aşınma çok yüksek. GLL kabul edilebilir ama C1'de kısa bacak OOS'ta katkı yapmadı (0,01).
4. Beklenti mütevazı tutulmalı. Kazanç yüksek oynaklık dönemlerinde yoğunlaşıyor; 2018–2024 benzeri sakin dönemlerde C1 sıfıra yakın.

## 7. Sınırlar

- Yahoo adjclose ve günlük kapanış kullanıldı. 15:00 ET karar anı muhafazakâr; gerçek uygulamada 15:45–15:55 ET.
- b2 sürümünde ETF fiyatı 14:30 ET'de alındı (saatlik bar sınırı). Gün içi altınla tam senkron ETF karşılaştırması yalnız son 723 gün için mümkündü.
- Nakit getirisi 0 varsayıldı; bu, yalnız-uzun sürümlerin Sharpe'ını bir miktar düşük gösterir.
- Kur makası, Midas'ın gerçek komisyon tarifesi ve ABD stopaj vergisi temel maliyet varsayımlarının içinde kabaca yer alıyor.
- C1, C2 ve C2j aynı fenomenin varyantları. Global FDR yapılırken bağımsız 3 bulgu olarak sayılmamalı.

## 8. Dosyalar

Kod: `out/e2_etf_leadlag/` altında. `run_all.sh` kayıt dosyasını sıfırlayıp hepsini yeniden üretir (~1 dakika).

| Dosya | İçerik |
|---|---|
| `e2_common.py` | Ortak yardımcılar; strateji ve ters ETF mantığı |
| `s0` | Veri denetimi, B&H, kaldıraç |
| `s1` | Madenci artıkları |
| `s2` | Gün içi göreli değer |
| `s3` | Çapraz gecikmeli |
| `s4` | VİOP / COT / akış |
| `s5`, `s5b` | Derin inceleme ve kısmi testler |
| `s6` | Stratejiler |
| `s7` | Asya madencileri ve birleşim |
| `s8` | FDR, etiketler, kaplama, placebo |
| `s9` | Izgara OOS |
| `s10` | Ayrıştırma |

Tablolar `*.csv` ve `*.json` dosyalarında. Kayıt: `out/registry/e2_etf_leadlag.csv` (1.030 satır) ve FDR'li kopyası `s8_kayit_fdr.csv`.
