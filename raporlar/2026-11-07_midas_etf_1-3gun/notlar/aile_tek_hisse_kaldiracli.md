# Aile: tek hisse kaldıraçlı ETF'ler (1-3 gün, Midas)

Hazırlanma: 07.11.2026. Veri son günü 06.11.2026. Kod `kod/ajan_tek_hisse_kaldiracli/`, tablolar `sonuclar/aile_tek_hisse_kaldiracli/`, JSON `sonuclar/aile_tek_hisse_kaldiracli/sonuc.json`.
ETF'ler (12): NVDL, NVDU, NVDS (NVDA); TSLL, TSLQ (TSLA); MSTU (MSTR); CONL (COIN); AAPU, AMZU, METU, MSFU, GGLL.

## 0. Kısa sonuç

* **Eşiği geçen tek aday: S1 = ön-kayıtlı TH03.** Sinyal hissenin kendi verisinden: hisse RSI(2) < 10 ve hisse > SMA(200) olunca o hissenin 2x ETF'ini al. Hisse kapanışı SMA(5)'in üstüne çıktığı ilk gün kapanışta, en geç 3. gün kapanışta sat. 7 mega-cap havuzunda (NVDA, TSLA, AAPL, AMZN, META, MSFT, GOOGL; sentetik kalibre 2x, 2016-11..2026-11):
  * C0: n=605 işlem / 419 sinyal günü, brüt +128 bp, net +111 bp, t=3,13. IS +104 bp (t=2,01), OOS +117 bp (t=2,40). Yılların %80'i pozitif.
  * O1: +101 bp (t=2,93). C1: +76 bp (t=2,14).
  * Gerçek ETF verisi (2022+, sinyal hisseden, işlem ETF fiyatından): C0 +128 bp (t=2,65, n=261), O1 +108 bp (t=2,38).
  * **Güven: düşük.** Kabul eşiklerini geçiyor ama birleşik FDR'yi (7.310 test) geçmiyor; yalnız ön-kayıtlı hipotez ailesinde geçiyor. Zamanlama kenarı (koşulsuz sürüklenme düşülmüş) yaklaşık +75 bp, t≈2,1. Bunun önemli kısmı tutuşunda bilanço olan 24 işlemden (%4) geliyor. Bilanço işlemleri hariç: net +84 bp (t=2,44), kenar +47 bp (t=1,35). Dayanaklar sonradan kazanan hisseler (seçim yanlılığı). Kuyruk büyük: en kötü işlem -%45 (TSLA 2x).
* **Kripto (MSTU, CONL) ve ters ürünler (TSLQ, NVDS) için doğrulanmış strateji yok.** Ters ETF almak her testte zarar ettirdi. Büyük NVDA yükselişinden sonra NVDS almak C0 h2'de -254 bp (t=-3,05; FDR'de anlamlı zarar).
* **Doğrulanmış gecikmeli öncü yok.** BTC@16:00 ET → MSTR/COIN ertesi gün: yok. SMH → NVDA: yok. Piyasa (SPY/QQQ) → hisse ertesi gün: negatif işaretli zayıf bir ilişki var (piyasa-geri dönüşü). Bu ilişki yalnız ek lead-lag ailesinde FDR'den geçiyor; OOS'ta zayıf ve kurala çevrilince maliyet sonrası doğrulanmıyor.
* **Oynaklık kaybı (TH01):** 1-3 günlük tutuşta 2x ETF'in 2x hisseye göre ortalama geri kalışı mega-cap'lerde 9-14 bp (3 gün). MSTU'da 57 bp, CONL'de 25 bp. Bu sapma basit getiride oynaklıktan değil, ücret ve swap finansmanından geliyor. Log getiride (L²−L)/2·h·σ² formülü tutuyor.
* **Midas:** bu ürünlerin Midas'ta bulunurluğu resmî olarak doğrulanamadı. Hepsi Nasdaq/Cboe'de listeli ve swap kullanan yatırım fonları. Vadeli emtia havuzu olmadıkları için PTP/K-1 olmaları beklenmez. Bu, ihraççı belgeleriyle bu çalışmada teyit edilmedi; işlemden önce Midas uygulamasında 'PTP' ibaresi olup olmadığına bakılmalı. Uzatılmış saatlerde yalnız limit emir, MOC/LOC yok.

## 1. Yöntem

* **Zamanlama:** `kod/lib.py` sözleşmesi. Sinyal yalnız t kapanışına kadarki bilgiyle. Modlar: C0 (t kapanışı), O1 (t+1 açılışı), C1 (t+1 kapanışı). Çakışmayan işlemler. Maliyet: 2×1,5 USD / pozisyon + `tarama.csv` makas tahmini. 2.500$'da ETF'e göre 16-23 bp (CONL 48 bp, NVDS 27 bp).
* **Dayanak testi:** ETF geçmişleri 2022+ olduğu için kurallar dayanak hisselerde 2016-11..2026-11 boyunca sentetik 2x ETF ile test edildi (`thk.synth_letf`). Günlük sıfırlamalı yapı: açılış, yüksek ve düşük önceki kapanışa göre L katı ölçeklenir. Gider oranı %1,05, (L−1)×(3 aylık faiz + %0,5 swap marjı) ve kalibre ek sürükleme düşülür. Ek sürükleme, gerçek ETF'in 2x döneminde sentetiğe göre ortalama geri kalışıdır: NVDA 2,8, TSLA 2,7, MSTR 13,0, COIN 5,1, AAPL 1,3, AMZN 2,1, META 1,8, MSFT 1,1, GOOGL 1,6 bp/gün. Sentetik ile gerçek ETF günlük getiri korelasyonu 0,999+.
* **Gerçek kaldıraç (önemli):** Direxion (TSLL, AAPU, AMZU, MSFU, GGLL, NVDU) ve GraniteShares (NVDL, CONL) ürünleri **2024 başına kadar 1,5x** idi. Geçiş NVDL/CONL için Ocak 2024, Direxion için Nisan 2024. TSLQ 2024-07'ye kadar -1x, sonra -2x (`tarama.csv`'deki lev=-1 eski). NVDS -1,25x'ten -1,5x'e geçti. METU ve MSTU baştan 2x. Bkz. `kaldirac_yillik.csv`. Bu yüzden genel_tum'daki 2022-2024 ETF sonuçları kısmen 1,5x ürünle ölçülmüştür.
* **Bağımsız kanıt birimi = dayanak hisse.** NVDL/NVDU/NVDS aynı dayanaktır, TSLL/TSLQ da öyle. MSTR ve COIN birbirine yakındır (corr 0,81). Havuz istatistiği **tarih kümelemeli**: aynı sinyal günündeki işlemlerin ortalaması tek gözlem sayılır. Bu, piyasa geneli düşüşlerde kümelenen sinyallerin t'yi şişirmesini önler.
* **Zamanlama kenarı:** her işlemin brüt getirisinden, aynı tutuş süresi ve giriş yapısındaki koşulsuz ortalama düşülür. Bu, 2016-2026 mega-cap yükselişinin (hayatta kalma yanlılığı) payını ayırmak içindir.
* **Bilanço tarihleri:** Nasdaq takvim API'si (`/api/calendar/earnings?date=`) dürüst istemci adıyla, önbellekli kullanıldı (`b0_bilanco.py`, `b0b_bilanco_pencere.py`). Hacim+boşluk adaylarının bir önceki günü ve beklenen pencere sorgulandı. Bulunamayanlar hacim+boşluk sıçramasından "tahmini" işaretlendi. Bu 9 şirket duyuruyu seans sonrası yapar: duyuru günü E = t, tepki günü R = t+1.

## 2. İşlenebilirlik ve kopya grupları (`islenebilirlik.csv`)

| ETF | Dayanak | Medyan hacim (mn$) | Maliyet 2.500$ (bp) | 1g oynaklık (bp) | Maliyet/oynaklık | Kaldıraç (son 1y) | 1y getiri | Karar |
|---|---|---|---|---|---|---|---|---|
| NVDL | NVDA | 626 | 16,2 | 479 | 0,034 | 1,98 | -%23 | kabul (S1) |
| NVDU | NVDA | 49 | 20,0 | 479 | 0,042 | 1,98 | -%23 | yedek (NVDL kopyası) |
| NVDS | NVDA | 7,6 | 27,0 | 362 | 0,075 | -1,50 | -%17 | red |
| TSLL | TSLA | 969 | 23,4 | 575 | 0,041 | 1,99 | -%54 | kabul (S1) |
| TSLQ | TSLA | 189 | 17,7 | 576 | 0,031 | -2,00 | -%10 | red |
| MSTU | MSTR | 176 | 16,0 | 1.026 | 0,016 | 1,98 | -%89 | yedek (yalnız BTC ile izleme) |
| CONL | COIN | 111 | 47,8 | 906 | 0,053 | 1,99 | -%90 | red |
| AAPU | AAPL | 54 | 16,0 | 312 | 0,051 | 1,99 | +%39 | kabul (S1) |
| AMZU | AMZN | 83 | 16,0 | 424 | 0,038 | 1,99 | -%8 | kabul (S1) |
| METU | META | 100 | 16,7 | 521 | 0,032 | 2,00 | -%26 | kabul (S1) |
| MSFU | MSFT | 116 | 16,0 | 422 | 0,038 | 1,98 | -%5 | kabul (S1) |
| GGLL | GOOGL | 141 | 16,0 | 428 | 0,037 | 2,01 | -%19 | kabul (S1) |

Hepsinin hacmi 20 mn$'ın üstünde, yalnız NVDS altında. 1-3 günlük hareket maliyetin 20-60 katı. Kopya grupları: {NVDL, NVDU} (corr 1,00; NVDL seçildi). NVDS ve TSLQ, NVDL ve TSLL'nin aynasıdır (corr -1,00). MSTU-CONL 0,81, AMZU-GGLL 0,61, diğer çiftler 0,05-0,47.

## 3. Genel kütüphane (`genel_aile_tutarlilik.csv`, `dayanak_genel_havuz.csv`)

**(a) genel_tum.csv, gerçek ETF verisi (2022+):** aile 3.564 satır. Aile içi BH-FDR'yi geçen 0. Tüm evren FDR'sinde aile satırlarından 156 geçiyor, 55'i pozitif ve hepsi tek ETF satırı (NVDL/NVDU RSI2, GGLL RSI2<5 vb.). Burada IS boştur (ETF'ler 2022+). 9 bağımsız birincil ETF'te en tutarlı satırlar şunlar: VX_vix_sicrama15 O1 h1 (9/9 pozitif, Stouffer 4,3), haftanın günü (CA_cum, CA_per), MR_rsi2_lt10 C1 h3 (8/9). Bu dönemde (2023-2025) tek hisse 2x'lerin koşulsuz sürüklenmesi çok yüksekti. **Not:** genel kütüphanede RSI2/SMA200 ETF'nin kendi fiyatından hesaplanıyor. Böyle hesaplanınca TH03 zayıf: MR_rsi2_lt10_ust200 C0 h3 erken çıkışlı, 9 ETF ortalaması +12 bp. Kaldıraçlı ETF'nin SMA200'ü sürüklenme ve 1,5x→2x geçişi yüzünden bozuk bir filtredir. **Sinyal hisseden hesaplanmalı.**

**(b) Aynı 31 sinyal dayanakta (2016+, sentetik 2x, 9 hisse):** 2.673 hisse satırı, 297 havuz satırı. Havuz düzeyinde FDR'yi geçen 0 (en küçük p=0,0006). Ön eleme (net>0, havuz t≥2,5, IS>0, OOS>0, yıl≥%60) 12 satır. Bunlar iki kümede toplanıyor:
* RSI(2)<10 dibi (h=3, C0/O1/C1, erken çıkışlı ya da sabit): ör. C1 h3 +140 bp t=3,44, C0 h3 erken çıkışlı +102 bp t=3,04. Zamanlama kenarı t 1,7-2,2.
* Cuma/Perşembe sinyalli haftanın günü etkisi: CA_cum O1 h3 +99 bp t=3,34, 9/9 pozitif. Ancak QQQ/TQQQ/XLK'de de var: piyasa geneli Nasdaq takvim etkisi, mekanizması yok. abd_endeks ailesi de eledi. **Elendi.**
* IBS<0,10 ve düşüş günü: C0 h1 +44 bp t=2,04, 9/9 pozitif. O1'de +3 bp, C1'de negatif: kapanışa bağımlı, eşik altı.
* 20 gün zirvesi, z>2 devamı ve VIX sıçraması dayanakta zamanlama değeri taşımıyor.

## 4. Aileye özel hipotezler (`hipotez_testleri.csv`; 105 havuz + 279 hisse satırı)

| Hipotez | Ön-kayıtlı varyant | n | Net (bp) | t | IS / OOS net | Sonuç |
|---|---|---|---|---|---|---|
| TH03 RSI2<10 & >SMA200, SMA5 çıkış (7 mega-cap) | C0 h≤3 | 605 | +111 | 3,13 | +104 / +117 | **Aday S1** (hipotez ailesinde FDR ✓) |
| TH03, aynı kural MSTR+COIN | C0 h≤3 | 99 | +99 | 0,70 | +149 / +74 | Zayıf, COIN negatif |
| TH02a büyük düşüş (≤-2,5σ20) → 2x long (NVDA/TSLA/MSTR/COIN) | C0 h2 | 134 | +200 | 1,45 | +139 / +267 | Eşik altı. Diğer 5 hissede -39 bp, OOS -148 |
| TH02b büyük yükseliş → 2x long (dönüş beklentisi) | C0 h2 | 165 | +178 | 1,74 | | Dönüş yok, devam var |
| TH02c büyük yükseliş → ters ETF (NVDS sentetik) | C0 h2 | 41 | -254 | -3,05 | -328 / -149 | Anlamlı **zarar** |
| TH02c, TSLQ sentetik | C0 h2 | 49 | -253 | -1,40 | | Zarar |
| TH05 opex haftası (Cuma → OE Çarşamba), NVDA/TSLA/AAPL | C0 | 351 | +159 | 2,13 | +183 / +134 | Zamanlama kenarı +23 bp, t=0,30: yalnız sürüklenme |
| TH06 BTC 16:00 artığı ≥2sd → MSTR/COIN 2x | C0 h1 | 45 | +213 | 0,85 | IS yok | Öncülük yok |
| TH01 kuralı (σ yüksekse 1 gün) S1 üzerinde | C0 | 755 | +84 | 2,49 | | S1'i kötüleştiriyor |
| TH07 (ek) RSI2>90 & <SMA200 → ters ETF (TSLA/NVDA) | C0 h2 | 64 / 39 | -44 / -32 | -0,30 / -0,32 | | Yok |
| SMH yetişme ≥2sd → NVDA 2x | C0 h1 | 51 | +68 | 0,55 | +102 / +35 | Öncü değil |

**TH01, oynaklık kaybı (`th01_oynaklik_kaybi.csv`, gerçek ETF, kaldıraç geçişinden sonra):** ETF getirisi − L×hisse getirisi, çakışmayan pencereler, bp:

| | NVDL | TSLL | MSTU | CONL | AAPU | AMZU | METU | MSFU | GGLL | TSLQ | NVDS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 gün | -5,2 | -5,1 | -15,5 | -7,5 | -3,6 | -4,5 | -4,1 | -3,4 | -3,9 | +2,8 | +1,8 |
| 3 gün | -13,5 | -14,4 | -57,0 | -25,3 | -9,5 | -12,1 | -12,5 | -9,2 | -11,6 | -3,0 | +8,9 |
| 3 gün log sapma | -42 | -56 | -126 | -92 | -20 | -26 | -30 | -19 | -24 | -121 | -43 |
| formül (L²−L)/2·3·σ² | -28 | -43 | -88 | -73 | -9 | -13 | -18 | -9 | -12 | -128 | -49 |

Basit getiride (dolar kâr/zarar) beklenen sapma oynaklık kovasına göre artmıyor. Bu, finansman, ücret ve swap maliyetidir. Oynaklık, sapmanın dağılımını büyütür: MSTU'da 3 günlük std 141 bp. Log getiride formül tutar. Pratik sonuç: 1-3 günlük işlemde maliyete 2x ürün için 3-5 bp/gün, MSTU için ~19 bp/gün ekle. TH01'in "yüksek σ'da 1 gün tut" kuralı S1'e zarar verdi.

**TH04, bilanço (`bilanco_tarihleri.csv`, `bilanco_olaylar.csv`, `bilanco_testleri.csv`; 28 test).** 342 duyuru bulundu. 334'ü Nasdaq takviminden doğrulandı, 8'i hacim+boşluktan tahmin (COIN 3, MSTR 3, TSLA 2). Tepki günü ortalama |hareket| normal günün 2,5-5 katı: META 820 bp, TSLA 743, NVDA 596 (normal 120-390 bp). Ölçümler sentetik 2x üzerinde, net:

| Test (9 hisse) | n | Net (bp) | t | IS / OOS | Yorum |
|---|---|---|---|---|---|
| Duyuruyu taşı (C_E → C_R) | 342 | +24 | 0,28 | +30 / +18 | Kumar: std 1.560 bp, en kötü -5.334 bp |
| Sonrası C_R → C_R+2 (TH04: PEAD yok) | 342 | +17 | 0,33 | +59 / -21 | Beklendiği gibi ~0. corr(tepki, sonraki 2 gün) 0,06 |
| Olumlu tepki sonrası (mega-cap 7) | 136 | +146 | 2,05 | +214 / +72 (t 0,73) | OOS'ta zayıflıyor, FDR yok |
| Duyuru öncesi 3 gün (mega-cap 7) | 279 | +76 | 1,92 | t 2,81 / 0,37 | OOS'ta yok |
| Tepki günü açılışta al → kapanış, olumlu boşluk | 182 | **-142** | -2,55 | -209 / -74 | Boşluğu kovalamak zarar |
| Tepki günü açılışta al → kapanış, olumsuz boşluk | 159 | **-161** | -2,77 | -153 / -167 | Dipten almak da zarar |

Strateji yok. İki pratik sonuç çıkıyor. (1) Bilanço sabahı 2x ETF'e açılışta girmek (TR kış 17:30) her iki yönde de ortalama ~1,5% kaybettirmiş. Tepki günü açılışından sonraki gün içi hareket ters gidiyor; bilanço aile içinde FDR'den geçiyor. (2) TH04 kuralı, yani duyurudan önce kapatmak, beklenen getiriyi değil riski azaltır. S1'de bilanço taşıyan 24 işlem (%4) ortalama +569 bp (t=1,80) getirmiş. Bunlar çıkarılınca S1 C0 +84 bp (t=2,44). IS +88 (t=1,68), OOS +80 (t=1,77). Zamanlama kenarı 47 bp (t=1,35) olur (§5). Yani S1'in sürüklenme dışı kenarının önemli kısmı az sayıda bilanço öncesi dip işleminden geliyor.

## 5. Aday strateji S1 (`aday_S1.py`, `aday_S1_cikti.txt`, `aday_S1_ozet.csv`, `aday_S1_hisse_etf.csv`)

**Kural (TradingView):** günlük grafikte NASDAQ:NVDA / TSLA / AAPL / AMZN / META / MSFT / GOOGL. Göstergeler kapanıştan: RSI(2), SMA(200), SMA(5). Sinyal t: RSI(2) < 10 ve kapanış > SMA(200). İşlem aracı: NVDL / TSLL / AAPU / AMZU / METU / MSFU / GGLL. Çıkış: girişten sonra hisse kapanışı > SMA(5) olan ilk günün kapanışı, en geç t+3 kapanışı. Pozisyondayken aynı hissede yeni sinyal yok sayılır. Stop yok.

**Giriş/çıkış saatleri:** C0 için TR kış 23:45-23:58 (yaz 22:45-22:58), canlı fiyatla kontrol edilir. Midas'ta MOC/LOC yok, normal seansta emir verilir. O1 için ertesi gün açılış, TR kış 17:30 (yaz 16:30); pre-market TR kış 12:00-17:30 yalnız limit emir.

| | n | Brüt | Net | t | IS net (t) | OOS net (t) | Kazanma | PF | Yıl+ | Zamanlama kenarı (t) |
|---|---|---|---|---|---|---|---|---|---|---|
| Dayanak C0 | 605 | 128 | 111 | 3,13 | 104 (2,01) | 117 (2,40) | 0,64 | 1,48 | 0,80 | 74 (2,06) |
| Dayanak O1 | 605 | 118 | 101 | 2,93 | 101 (1,88) | 102 (2,25) | 0,63 | 1,45 | 0,80 | 76 (2,18) |
| Dayanak C1 | 564 | 93 | 76 | 2,14 | 65 (1,35) | 85 (1,66) | 0,61 | 1,22 | 0,80 | 47 (1,30) |
| Gerçek ETF C0 (2022+) | 261 | 145 | 128 | 2,65 | — | 128 | 0,64 | 1,60 | 0,80 | 94 (1,94) |
| Gerçek ETF O1 | 261 | 125 | 108 | 2,38 | — | 108 | 0,62 | 1,56 | 0,80 | 90 (1,98) |
| Gerçek ETF C0, yalnız 2x dönemi | 190 | 166 | 149 | 2,44 | — | | 0,64 | 1,68 | 0,67 | |

* **Maliyet duyarlılığı (dayanak C0):** 1.000$ +93 bp (t=2,62), 2.500$ +111 bp, 10.000$ +120 bp (t=3,38). O1: +83 / +101 / +110.
* **Hisse başına (dayanak C0):** NVDA +201 (t=1,98), TSLA +163 (0,94), AAPL +54 (0,93), AMZN +84 (1,33), META +45 (0,66), MSFT +141 (2,28), GOOGL +104 (1,84). 7/7 pozitif ama tek başına anlamlı olan yok gibi (yalnız MSFT t>2). Kanıt havuzdan geliyor; tek hisse seçme.
* **Gerçek ETF (C0):** NVDL +362 (t=2,75), TSLL +103, AAPU +35, AMZU +85, METU -45 (n=21), MSFU +70, GGLL +100. NVDU (kopya) +338.
* **Komşu parametreler (yalnız rapor, seçim yok):** RSI<5 ve trend filtresiz varyantlar benzer ya da daha iyi (ör. trend filtresiz, SMA5 çıkış C0 +115 bp t=3,57; IS 2,75, OOS 2,39). RSI<15 ve sabit 1 gün tutuş zayıf. Kenar 2-3 günlük tutuşta.
* **Yıllar (sinyal günü başına ort. net, bp toplamı):** 2017 +1.201, 2018 +1.027, 2019 +634, 2020 +10.530, 2021 +6.636, 2022 -1.166, 2023 +1.996, 2024 +19.353, 2025 -2.606, 2026 +8.897. Ayı yıllarında (2022) ve sert düşüşlerde (Mart-Nisan 2025) dip alımı tekrar tekrar zarar yazıyor.
* **Risk:** en kötü işlem -4.457 bp (TSLA 2x). Hisse başına maxDD %18 (MSFT) ile %72 (TSLA) arası. 1/7 sermayeli kaba portföy maxDD -%11,5. Eşzamanlı açık pozisyon medyan 2, en çok 7. Sinyaller piyasa düşüşlerinde kümelenir, sermaye buna göre bölünmeli.
* **Ayna:** aynı sinyalle ters ETF almak NVDS'te -324 bp (t=-3,33), TSLQ'da -194 bp. Beklenen yönde.
* **Güncel durum (06.11.2026 kapanışı):** 7 hissenin hiçbirinde sinyal yok. NVDA (186,64 < SMA200 204,67) ve TSLA (358,22 < 383,87) SMA200 altında olduğu için filtre şu an kapalı. Yaklaşan: NVDA bilançosu 17.11.2026 seans sonrası (Nasdaq/Zacks tahmini; tepki 18.11 açılışında, TR 17:30). Diğerleri Ocak sonu-Şubat 2027.
* **Bilanço ayrımı:** bilanço taşıyan 24 işlem çıkarılınca C0 +84 bp (t=2,44; IS 88 t=1,68, OOS 80 t=1,77), O1 +74 bp (t=2,25), gerçek ETF C0 +93 bp (t=2,13). Maliyet: 1.000$'da +66 bp (t=1,92), 10.000$'da +93 bp. Zamanlama kenarı +47 bp (t=1,35). Tarih ağırlıklı yıllık toplamlarda pozitif yıl oranı %50; işlem ağırlıklıda %80. Muhafazakâr kullanım: tutuş içinde seans sonrası bilanço duyurusu varsa girme ya da duyuru günü kapanıştan önce çık.
* **FDR:** birleşik test kümesinde (bkz. §7) geçmiyor (C0 p=0,0019, eşik ~4e-5). Ön-kayıtlı hipotez havuzunda (105 test) C0 ve O1 geçiyor. Kabul eşiklerinin hepsi sağlanıyor. Ama sürüklenme dışı kenar zayıf ve az sayıda bilanço işlemine bağlı: **güven düşük**.

## 6. Lead-lag (`leadlag_aile_sweep.csv`, `leadlag_suruculer.csv`, `leadlag_ek_regresyon.csv`, `th06_btc_regresyon.csv`, `smh_nvda_regresyon.csv`, `btc_gece_acilis.csv`, `oncu_kural_testleri.csv`)

* **Genel tarama:** aile hedefleri × 48 öncü = 576 satır, FDR bayrağı 0. En yüksek (geçmeyen) t'ler NVDS ← faiz/IEF yetişmesidir; düşük korelasyonlu öncüde yetişme, NVDS'nin kendi geri dönüşüdür.
* **Eşzamanlı sürücüler (öncü DEĞİL):** her ETF'te dayanak hisse (corr 0,998-0,999, beta ~2 / -2 / -1,5). Sonra NVDL/TSLL için XLK, SMH, QQQ (0,55-0,75); MSTU/CONL için IBIT ve BTC (0,80-0,86); AAPU/AMZU/METU/MSFU/GGLL için SPY/QQQ (0,32-0,56).
* **Ek test (dayanak 2016+, kendi gecikmesi kontrollü, Newey-West; 152 test):** 13'ü FDR'den geçiyor. Hepsi **negatif işaretli piyasa-geri dönüşü**: SPY/QQQ/XLK bugün yükselirse hisse ertesi gün piyasa kısmını kısmen geri veriyor. Örnekler: AMZN ← SPY t=-3,31 (IS -2,65, OOS -2,05); GOOGL ← SPY t=-3,25 (OOS -1,58); NVDA ← SPY t=-2,65 (OOS -0,39). 1 sd'lik etki 2x ETF'te 40-80 bp, maliyet 16 bp. Ancak OOS'ta çoğu zayıf ve birleşik FDR'de geçmiyor. **Kurala çevrilince** (piyasa z<-2 → 2x long, 9 hisse) yalnız QQQ O1 h1 +109 bp (t=2,44). C0, C1 ve h2-3 anlamsız; gerçek ETF'de C0 negatif. **İşlem için doğrulanmış gecikmeli öncü yok.**
* **BTC → MSTR/COIN (TH06, 2023-06+):** BTC 16:00 ET getirisi → MSTR t+1 t=-1,26. TH06 artığı t=-0,98, yetişme boşluğu t=-0,89. COIN için t -1,0 ile -1,1. Öncülük yok. Gerçek zamanlı izleme gücü ise yüksek: BTC'nin 16:00 → ertesi 09:00 ET hareketi MSTR açılış boşluğuyla corr 0,88 (beta 1,22, R² 0,78), COIN ile 0,78. MSTU kapalıyken COINBASE:BTCUSD açılışı büyük ölçüde önceden gösterir. Bu bir öncü değil, izleme aracıdır.
* **SMH → NVDA (NVDL):** SMH getirisi → NVDA t+1 t=-1,72 (IS -2,69, OOS +0,30). Yetişme t=-2,08 (IS -2,79, OOS -0,13). İşaret negatif ve OOS'ta sıfır. Kural +68 bp t=0,55. Öncü değil.
* **Gerçek zamanlı izlenecekler (ETF kapalıyken):** hissenin kendi uzatılmış seansı (NASDAQ:NVDA vb.; pre-market TR kış 12:00-17:30, after-hours TR kış 00:00-04:00; bilanço tepkisi burada görülür), CME_MINI:NQ1!, CME_MINI:ES1!. MSTU için COINBASE:BTCUSD ve CME:BTC1!. NVDL için ek bağlam OSE:NK2251!.

## 7. Test sayısı ve FDR (`fdr_tum_testler.csv`, `t6_fdr.py`)

Birleşik BH-FDR (q=0,10) için **7.310 test** kullanıldı (`fdr_tum_testler.csv`). Eşik p ≤ 4,1e-05; geçen 4 test var, hepsi tek hisse satırı ve pozitif (MSFT IBS<0,2 varyantları, AAPL CA_cum O1 h3). Bunlar tek hisse seçimi olduğu için strateji yapılmadı. Gruplar:

| Grup | Test | FDR geçen |
|---|---|---|
| genel_tum aile ETF satırları (2022+) | 3.500 | 0 |
| Dayanak genel kütüphane, hisse satırı | 2.673 | 4 |
| Dayanak genel kütüphane, havuz | 297 | 0 |
| Aile hipotezleri (TH01-TH07, SMH; hisse+havuz) | 384 | 0 |
| Öncü kural testleri (LL1/LL2) | 180 | 0 |
| Ek lead-lag regresyonları | 152 | 0 |
| BTC / SMH regresyonları | 22 | 0 |
| Bilanço testleri | 28 | 0 |
| S1 komşu/maliyet/gerçek ETF kontrolleri | 74 | 0 |

Daha dar aileler içinde ayrı BH de hesaplandı. Hipotez havuzunda (105 test) 5 test geçiyor: TH03 C0 ve O1 (S1), ayrıca TH02c NVDS'in 3 negatif varyantı. Ek lead-lag ailesinde (152) 13 test geçiyor, hepsi negatif işaretli. Bilanço ailesinde (28) 5 test geçiyor, hepsi negatif (tepki günü gün içi). genel_tum'un tüm evren FDR'sinde aile satırlarından 156 geçiyor, 55'i pozitif ve tek ETF.

## 8. Elenenler (özet)

TH02a/b/c, TH04 (strateji olarak), TH05, TH06, TH07, TH01 kuralı, SMH yetişmesi, haftanın günü (CA_cum O1 h3), IBS<0,10 kapanış dönüşü, z>2/20 gün zirvesi momentumu, piyasa düşüşü → 2x kuralı, kripto ve ters ETF'lerde S1. Gerekçeler sonuc.json "elenen" alanında.

## 9. Sınırlamalar

* **Seçim/hayatta kalma yanlılığı:** dayanaklar, tek hisse kaldıraçlı ETF'i olacak kadar popülerleşmiş, yani 2016-2026'nın kazananları. Koşulsuz 2x getiri çok yüksek. Zamanlama kenarı ayrıca raporlandı (S1: ~75 bp, t≈2,1).
* Sentetik 2x gerçek ETF'i iyi izliyor (corr 0,999), ama 2020 gibi stres dönemlerinde swap maliyeti ve kapanış dengeleme etkileri farklı olabilirdi. Ürünlerin kapanma riski (fon tasfiyesi), ters bölünme (CONL 2,79$) ve ihraççı riski modellenmedi.
* Bilanço tarihlerinin bir kısmı tahmindir (§4). Duyuru saati seans sonrası varsayıldı.
* C0 girişi kapanış fiyatıyla hesaplanıyor. RSI(2) son dakikalarda eşiği geçip dönebilir. O1 bu yüzden yedek giriş.
* Maliyet modeli kaba: makas kademesi tahmini. Yüksek oynaklık günlerinde (sinyal günleri) makas daha geniş olabilir. BSMV belirsizliği `notlar/midas_kosullari.md`'de.
* Midas'ta sembol bazında bulunurluk doğrulanamadı. Kaldıraçlı ETF'ler için ek risk bildirimi/uygunluk testi gerekebilir.

## 10. Tekrar üretim

```
python3 -I kod/ajan_tek_hisse_kaldiracli/t1_islenebilirlik.py
python3 -I kod/ajan_tek_hisse_kaldiracli/t2_genel_aile.py
python3 -I kod/ajan_tek_hisse_kaldiracli/t3_dayanak_genel.py
python3 -I kod/ajan_tek_hisse_kaldiracli/t4_hipotez.py
python3 -I kod/ajan_tek_hisse_kaldiracli/b0_bilanco.py          # ağ (Nasdaq takvimi), önbellekli
python3 -I kod/ajan_tek_hisse_kaldiracli/b0b_bilanco_pencere.py # ağ, önbellekli
python3 -I kod/ajan_tek_hisse_kaldiracli/b1_gelecek_bilanco.py  # ağ: yaklaşan bilanço tarihleri
python3 -I kod/ajan_tek_hisse_kaldiracli/t5_leadlag.py
python3 -I kod/ajan_tek_hisse_kaldiracli/t5b_oncu_kural.py
python3 -I kod/ajan_tek_hisse_kaldiracli/t7_bilanco.py
python3 -I kod/ajan_tek_hisse_kaldiracli/aday_S1.py     # S1'in tüm sayıları (aday_S1_cikti.txt)
python3 -I kod/ajan_tek_hisse_kaldiracli/t6_fdr.py
python3 -I kod/ajan_tek_hisse_kaldiracli/t8_sonuc.py    # sonuc.json
```
