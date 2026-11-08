# e3_etf_akis_prim — ETF akışları, prim/iskonto ve kaldıraçlı ETF dengelemesi (Midas cephesi)

Ufuk: 1, 3, 5 NYSE iş günü, ABD kapanışından kapanışına (16:00 ET). Karar anı (kesim): gün t 15:00 ET (yaz 19:00 UTC, kış 20:00 UTC).
IS = 2008–2017, OOS = 2018–2026-11, ayrıca 2022+ alt dönemi. VİOP hedefinde VİOP'un kendi bölünmesi (IS 2017-03..2021-12) kullanıldı.
Toplam kayıtlı test: **455** (`out/registry/e3_etf_akis_prim.csv`; başarısızlar, tanı testleri ve strateji ızgarası dahil).

## 0. Sonuç (önce)

| # | Bulgu | Güven |
|---|---|---|
| 1 | **Altının gün t 15:00 ET'ye kadarki hareketi (16:00 ET t-1 → 15:00 ET t, spot) GDXJ'nin ertesi gün getirisini ters yönde öngörüyor.** IC −0,077, t −5,30 (IS −4,80, OOS −2,77, 2022+ −2,21), 18 yılın 15'inde aynı işaret. Yalnız uzun kural (altın düştüyse GDXJ'yi kapanışta al, 1 gün tut, yoksa nakit): OOS net Sharpe 0,72 (10 bps), 0,51 (20 bps). GDXJ'yi sürekli tutmanın OOS Sharpe'ı 0,54. Drift çıkarılınca (demeaned) 0,53 / 0,32. | **YUKSEK** (maliyete duyarlı) |
| 2 | Aynı etki GDX'te ve geniş madenci evreninde de var (GDX t −3,82; JNUG −4,01; NUGT −3,40; AEM −3,24; RING −2,46). GDX'te OOS t −1,87 (h=1), −2,49 (h=5). IS'te seçilen GDX kuralı OOS'ta çalışmıyor. | ORTA |
| 3 | PHYS (Sprott fiziki altın tröstü) / GLD oranının 60 günlük medyandan sapması (t-1) sonraki 5 günde PHYS−GLD farkını ters yönde öngörüyor: IC −0,155, t −6,40 (IS −4,31, OOS −4,87), 17 yılın 17'sinde aynı işaret. Ekonomik büyüklük küçük: \|z\|>2'de 5 günde ±19–22 bps. Bu, iki bacaklı 20 bps geçiş maliyetini karşılamıyor. Yalnız zaten altın alacaksanız hangi aracı seçeceğinize karar verirken (ek maliyetsiz) işe yarar. | ORTA |
| 4 | CEF (Sprott altın+gümüş tröstü) için geçmiş β ile GLD+SLV karmasına göre artık sapma da aynı şekilde dönüyor (z60, h=5: t −6,70, OOS −4,41). IS'te seçilen geçiş kuralı OOS'ta IR 0,07. | ORTA |
| 5 | BIST altın BYF'si GLDTR'nin 17:30 TSİ'deki spot gram altına göre primi ertesi gün GLDTR − gram altın farkını ters yönde öngörüyor (IC −0,158, t −3,85, n=668, yalnız 2023-12+). Prim en üst %20 dilimdeyken (ort. +150 bps) BYF, gram altının 1 günde 18, 5 günde 55 bps altında kalıyor. ZGOLD zayıf, ISGLK'de etki yok. | DUSUK (kısa örneklem, fondan fona istikrarsız) |
| 6 | GLD/GLDM akışları getiriyi **öngörmüyor**. Tersine, akışlar geçmiş getiriyi takip ediyor: aynı gün t=12, önceki gün t=9,4, önceki 2–5 gün t=8,6. VİOP hedefi için de akış etkisi yok. | YOK |

Diğer olumsuz sonuçlar: GLD primi (std 3–5 bps) maliyetin altında kalıyor. Hacim şoklarında etki yok. GLD'nin kendisinde kaldıraçlı ETF dengeleme dönüşü yok. Ters ETF'li (GLL/DUST/JDST) sürümlerin kısa bacağı hiçbir yerde kalıcı değer üretmiyor. Bkz. §8.

## 1. Veri, kapsama ve zamanlama

- Ana panel `panel/panel_etf.parquet` (NYSE günleri 2008-01-02 → 2026-11-06). Kapanışlar `c_*` hedef ve giriş fiyatı olarak kullanıldı. Sinyalde gün t kapanışı hiç kullanılmadı.
- SSGA GLD/GLDM NAV ve pay sayısı: `etf_gld_navhist.parquet` (2004+) ve `etf_gldm_navhist.parquet` (2018-06+). Paneldeki `flow_gld_shares` ile kendi as-of hizalamam %100 uyumlu.
- Dukascopy saatlik XAUUSD 2008+ (fiyat anı = bar başı + 1 saat). LBMA PM anı (15:00 Londra; BST'de 14:00, GMT'de 15:00 UTC) ile hesaplanan NAV/spot oranının günlük oynaklığı kışın 15:00 UTC'de (0,26%), yazın 14:00 UTC'de (0,35%) en düşük. Bu, NAV'ın LBMA PM'den hesaplandığını doğruluyor.
- **BIST BYF'leri:** Yahoo günlük geçmişi YOK (GLDTR/ZGOLD/ISGLK/GMSTR için yalnız 1 gün). İş Yatırım ve Stooq erişilemedi. Yahoo saatlik (730 gün) indirildi (`dl_bist_byf/`, ayrıştırma `parse_bist_byf.py`). GLDTR ve ZGOLD 2023-12+, ISGLK 2024-07+ (tamamı OOS). GMSTR gümüş fonu, kapsam dışı.
- Saatlik ETF (son ~2 yıl) ve 5 dakikalık (son 60 gün) veri. Gün-içi ayrıştırmada temettü düzeltmesiz kapanış kullanıldı. Düzeltmeli kapanış ilk denemede GDXJ/DUST'ta sahte −0,5 korelasyon üretti. Hata düzeltildi.

### Öngörücülerin bilgi zamanı

| Öngörücü | Tanım | Bilgi anı (ET) | Bilgi anı (UTC) | Kullanıldığı gün |
|---|---|---|---|---|
| GLD/GLDM akış f1/f5/f20, z | Δln(pay) 1/5/20 SSGA günü; z = /geçmiş 250g std | SSGA günü D akşamı (~17–20 ET) | ~21–01 UTC | lag1: t=D+1; lag2: t=D+2 |
| Akış → VİOP | aynı | D akşamı ABD | ≤ D+1 01 UTC | VİOP günü t>D, karar 15:00 UTC |
| GLD primi prem_{t-1} | ln(c_GLD / (ons/pay_med × spot 16:00 ET)), ons/pay = NAV/spot(LBMA PM), 20g medyan | t-1 16:00 ET + NAV akşamı | t-1 20/21 UTC + akşam | t |
| GLD gün-içi primi | GLD 14:30 ET (saatlik) / [ons/pay_{t-1} × spot 14:30 ET ara değer]; 5 dk: 15:00 ET | 14:30 / 15:00 ET | 18:30–20:00 UTC | t |
| PHYS/PSLV/CEF sapma z | ln(PHYS/GLD), ln(PSLV/SLV), CEF artığı; − k günlük medyan; / 250g std | t-1 16:00 ET | t-1 20/21 UTC | t |
| m_t (madenci dönüşü) | ln(spot_15:00ET,t / spot_16:00ET,t-1), z = /σ60 (t-1'e kadar) | **15:00 ET t** | **19:00 (yaz) / 20:00 (kış) UTC** | t |
| m14_t | aynı, 14:00 ET spot | 14:00 ET t | 18:00/19:00 UTC | t |
| BIST BYF primi | BYF (başı ≤13:30 UTC olan son saatlik bar) / (gram/birim_med_{t-1} × XAUUSD×USDTRY/31,1035 aynı an) | — | ≤14:30 UTC (17:30 TSİ) | t (giriş BIST kapanışı 15:10 UTC) |
| Hacim şoku vz | ln hacim_{t-1} − geçmiş 60g ort. / std | t-1 16:00 ET | t-1 20/21 UTC | t |

İleriye bakma kontrolü (`placebo_lead`): bütün ana öngörücülerde sinyal geriye kaydırıldıkça (daha eski bilgi) IC yumuşakça sönüyor. Yalnız ileri kaydırma (yasak bilgi) IC'yi büyütüyor. Örnek: m_t → GDXJ, kaydırma 0: −0,077; +1: −0,021; +2: −0,008; −1: +0,736 (aynı günün hareketi, beklenen). PHYS z20: 0: −0,060; +1: −0,042; +2: −0,033. ABD yarım günleri (erken kapanış) çıkarılınca ana bulgu değişmiyor (IC −0,074, t −5,10).

### Yöntem
- IC = Spearman; t = Newey-West (lag = max(h,5)) (`lib_altin.split_stats`). Olay testleri: olay kukla değişkenine NW regresyonu (fark bps).
- Parametreler (eşik, k, h) yalnız IS'te seçildi. OOS bir kez raporlandı. Kademeli h günlük tutuş (her gün sermayenin 1/h'i).
- Strateji getirileri basit getiri. Maliyet her bacakta |Δnominal| × gidiş-dönüş/2. GLD/IAU/GDX/GDXJ/SLV/PHYS 10 bps (stres 20). Kaldıraçlı ve ters ETF'ler 20 bps (stres 40). Fon değiştirme (GLD→PHYS) iki bacak, 20 bps (stres 40).
- Ters ETF sürümü: kısa sinyalde nominal = |pos|/L ters ETF (GLL, ZSL L=2; DUST/JDST 2020-04 öncesi L=3, sonrası L=2), yani yaklaşık −1× hedef maruziyet.
- Her stratejide şunlar raporlandı: B&H Sharpe, demeaned Sharpe, uzun ve kısa bacak, 2022+, uç dönem PnL'i (2008, 2013-04, 2020-03, 2026-01/02) ve uç dönemler hariç Sharpe.

## 2. (a) GLD ve GLDM akışları

| Öngörücü → hedef | n | IC | t | t_IS | t_OOS | t_22+ | aynı işaretli yıl |
|---|---|---|---|---|---|---|---|
| zf1 lag1 → GLD h1 | 4742 | −0,011 | −0,77 | +0,47 | −1,30 | −1,39 | 11/19 |
| zf5 lag1 → GLD h5 | 4738 | −0,001 | −0,02 | −0,22 | +0,13 | −0,43 | 13/19 |
| zf20 lag1 → GLD h1 | 4742 | +0,021 | +1,49 | −0,38 | +2,55 | +1,47 | 9/19 |
| zf1 lag2 → GLD h1 | 4742 | +0,026 | +1,77 | +0,03 | +2,51 | +2,30 | 11/19 |
| zf20 lag2 → GLD h5 | 4738 | +0,014 | +0,51 | −1,02 | +1,86 | +0,82 | 8/19 |
| f5 en üst %10 → GLD h5 (bps) | 249 olay | −29 | −1,04 | 0,00 | −1,52 | −0,70 | 11/15 |
| f5 en alt %10 → GLD h5 (bps) | 496 olay | +7 | +0,30 | −0,44 | +1,36 | +0,92 | 14/19 |
| GLDM zf1 lag2 → GLD h1 (2018+) | 1982 | +0,053 | +2,33 | — | +2,33 | +1,78 | 6/8 |
| GLD+GLDM $ akış z5 → GLD h1 | 4742 | +0,008 | +0,55 | −0,08 | +0,85 | +0,09 | 9/19 |
| zf20 lag1 → VİOP h1 | 2426 | +0,039 | +1,84 | +1,22 | +1,37 | +1,37 | 6/10 |
| zf1 lag1 → VİOP h1 | 2426 | −0,001 | −0,05 | +1,53 | −1,33 | −1,33 | 6/10 |

- 60 GLD testinin (6 öngörücü × 2 gecikme × 4 ufuk + IAU) hiçbiri IS ve OOS'ta aynı işaretle anlamlı değil. IS'te en güçlüsü f20 → GLD h10 (t_IS −1,26). OOS'ta işaret dönüyor (+1,89).
- GLDM akışlarında IS yok (tamamı 2018+). Tek anlamlı görünen (zf1 lag2, t 2,33) 18 GLDM testinin içinde. Çoklu test sonrası anlamsız.
- **Ters yön** (SSGA günü D, standartlaştırılmış β): f1_D ~ r_D 0,16 (t 6,0), r_{D-1} 0,11 (t 6,9), r_{D-5..D-2} 0,08 (t 3,8), r_{D-20..D-6} 0,07 (t 3,9), f1_{D-1} 0,18 (t 6,6). Üç alt dönemde de (2005–12, 2013–19, 2020–26) aynı. **Akış fiyatı takip ediyor, öncülük etmiyor.** Bu, literatürdeki Deutsche Bank Granger bulgusuyla uyumlu.
- **Pay sayısının güncellenme günü:** corr(f1_D, prem_{D−1}) = 0,186 > corr(f1_D, prem_D) = 0,139. Gün D'de raporlanan pay değişimi büyük olasılıkla D−1'deki prime verilen yaratma emirlerini yansıtıyor (T+1). Yine de lag2 sürümü de bir şey öngörmüyor.
- Strateji (IS seçimi: f20 z-skoru, IS işaretine göre karşıt; h=10 seçimi 5 güne kısıtlandı): yalnız uzun OOS 0,21 (B&H 0,81, demeaned −0,23). Ters ETF'li OOS −0,47. → **YOK.**

## 3. (b) GLD prim/iskontosu

- ons/pay günlük log değişim std'si: ham 31 bps (LBMA anı ölçüm gürültüsü), 20 günlük medyanla 1 bps. Prim ortalaması yıllara göre −2 ile +8 bps arası. Std 3–5 bps (2008: 8,5; 2020: 7,4). AC(1) 0,57, AC(5) 0,46.
- Tanı (işlem dışı, prim gün t kapanışında ölçülüyor): prem_t → (GLD − spot) t+1 IC −0,376 (t −26). Bu, ölçüm hatası ve kapanış gürültüsünün mekanik dönüşü. prem_t → GLD'nin kendi getirisi IC −0,015 (t −1,0). Dönüşü spot "yapıyor", GLD değil.
- Uygulanabilir: prem_{t-1} → GLD h1 IC −0,015 (t −1,02; IS +0,52, OOS −2,02). z-prim → GLD h1 −0,006 (t −0,43). Δprim → GLD h1 −0,019 (t −1,21; OOS −0,38).
- Gün-içi prim: 14:30 ET (saatlik, ara değerli, 698 gün, std 12 bps) → GLD h1 IC −0,054 (t −1,31). 15:00 ET (5 dk, 59 gün, std yalnız 2,5 bps) → GLD h1 +0,004.
- Strateji (karşıt, \|z\|>1): IS'te demeaned Sharpe negatif (−0,08). OOS ham Sharpe 0,61 B&H'nin (0,81) altında. → **YOK.** GLD primi 10 bps maliyetin altında. Midas'ta GLD ile IAU/GLDM arasında prime göre seçim yapmanın anlamı yok.

## 4. (c) Kapalı uçlu ve fiziki tröstler: PHYS, PSLV, CEF

Referans aynı anda kapanan ETF (oran yöntemi, NAV'a gerek yok). Spread günlük std: PHYS−GLD 42 bps (AC1 −0,09), PSLV−SLV 60 bps (−0,11), CEF artığı 53 bps (−0,12).

| Sapma z (t-1) → spread | n | IC | t | t_IS | t_OOS | t_22+ | yıl |
|---|---|---|---|---|---|---|---|
| PHYS/GLD k=60, h1 | 4051 | −0,072 | −5,42 | −5,12 | −2,70 | −1,49 | 15/17 |
| PHYS/GLD k=60, h5 | 4047 | −0,155 | −6,40 | −4,31 | −4,87 | −3,76 | 17/17 |
| PHYS/GLD k=20, h5 | 4067 | −0,108 | −4,47 | −4,32 | −2,08 | −1,11 | 14/17 |
| PSLV/SLV k=60, h5 | 3876 | −0,090 | −3,32 | −2,60 | −2,35 | −2,32 | 14/16 |
| CEF artık k=60, h5 | 4338 | −0,165 | −6,70 | −5,15 | −4,41 | −3,57 | 17/18 |
| CEF artık k=20, h1 | 4362 | −0,061 | −4,54 | −3,66 | −2,90 | −2,08 | 17/18 |
| PHYS/GLD z → PHYS'in kendi getirisi h5 | 4047 | +0,001 | +0,04 | −0,62 | +0,66 | +1,43 | 6/17 |

Büyüklük (z dilimine göre 5 günlük ortalama spread, bps; IS / OOS):

| | z≤−2 | −2<z≤−1 | \|z\|<1 | 1<z≤2 | z>2 |
|---|---|---|---|---|---|
| PHYS−GLD (k60) | +21 / +19 | +15 / +6 | −2 / −2 | −13 / −7 | −19 / −22 |
| PSLV−SLV (k60) | +47 / +69 | +18 / −1 | −2 / −7 | −28 / −6 | −129 / −12 |
| CEF artık (k60) | +32 / +59 | +22 / +4 | +1 / −1 | −37 / −24 | −35 / −30 |

- Dönüş yalnız spread'de. Fonun kendi yönü öngörülmüyor, bu yüzden "iskontoluyken PHYS al, değilse nakit" kuralı anlamsız (yalnız uzun OOS 0,07, B&H 0,78; ters GLL sürümü −0,24).
- **Yalnız uzun uygulanabilir sürüm (araç değiştirme):** varsayılan GLD (SLV / GLD+SLV karması) tutulur. z<−eşik iken fona geçilir. IS seçimi (IR_IS'e göre):
  - PHYS: k=60, eşik=1, h=1, IR_IS 0,36 → OOS −0,29 (stres −0,99, brüt +0,48). Başarısız. (k=60, eşik=1,5, h=3 OOS IR 0,49 ama IS'te seçilmedi.)
  - PSLV: k=60, eşik=2, h=3, IR_IS 0,35 → OOS 0,53 (stres 0,39). Ama fazla getirinin önemli kısmı 2020-03'ten (+7,6%) ve 2026-01/02'den (+3,7%). Uç dönemler hariç IR 0,28, t_OOS 1,57. → DUSUK.
  - CEF: k=20, eşik=1,5, h=5, IR_IS 0,45 → OOS 0,07 (2022+ −0,19). Başarısız.
- Sonuç: istatistiksel ilişki sağlam (**ORTA**). Maliyet sonrası ayrı bir strateji olarak değeri yok. Pratik kullanım: zaten altın alacak birinin PHYS/GLD z'sine bakarak ucuz aracı seçmesi ek maliyetsiz. Bu seçim \|z\|>2'de 5 günde ~20 bps, −2<z≤−1'de 6–15 bps kazandırır.

## 5. (d) Kaldıraçlı ETF dengelemesi

### 5.1 Gerçekleşen kaldıraç ve aşınma (örtüşmesiz h-gün regresyonu)

| ETF | dönem | β h1 / h3 / h5 | yıllık aşınma (sabit terim, %) |
|---|---|---|---|
| GLL (−2× altın) | 2010–2019 / 2020-04+ | −1,99 / −2,00 / −2,00 ; −1,98 / −1,99 / −1,98 | −9,6 ; −1,7 |
| UGL (+2×) | | 2,00 / 2,01 / 2,02 ; 2,02 / 2,04 / 2,02 | −5,2 ; −10,3 |
| DUST (ters GDX) | (−3× 2020'ye kadar) | −2,82 / −2,88 / −2,93 ; −1,99 / −2,00 / −2,02 | −90 ; −35 |
| JDST (ters GDXJ) | | −2,90 / −3,06 / −2,97 ; −1,97 / −2,00 / −2,02 | −156 ; −48 |
| NUGT / JNUG | | ~2,9 → ~2,0 | −54 / −93 ; −20 / −24 |
| ZSL (−2× gümüş) | | −1,98 / −1,94 / −1,89 ; −1,95 | −32 ; −40 |

1–5 günde gerçekleşen kaldıraç nominale çok yakın. Ama madenci ters ETF'lerinin aşınması çok büyük: JDST'de 2020+ için yılda ~−48%, yani 5 günde ~−1%. Kısa yönü DUST/JDST ile almak pahalı. GLL'de aşınma küçük.

### 5.2 Mekanizma tanısı (işlem dışı: gün t kapanış getirisi)
- Ertesi gün getirisinin r_t'ye regresyonu (β): GDX'te NUGT/DUST öncesi (2006-05..2010-11) −0,001, sonrası −0,040 (t −1,8). GDXJ'de JNUG öncesi (2009-11..2013-09) +0,031, sonrası −0,056 (t −2,0). GLD'de öncesi −0,022, sonrası −0,014 (fark yok).
- \|r_t\|>2σ olaylarında ertesi gün işaretli getiri: GDXJ'de öncesi +84 bps (t 2,0), sonrası −9 bps (t −0,25). Devam eğilimi tersine dönmüş. GDX +23 → +10 bps (anlamsız). GLD +4 → 0.
- Son saat ve son 30 dakika momentumu: corr(m_t, spot 15→16 ET) = +0,076 (t 3,4, 19 yılın 12'si).
  - Saatlik veri (2 yıl), t-1 kapanış→14:30 ET ile 14:30→16:00 ET arası korelasyon: GLD +0,13 (t 3,3), IAU +0,11, GLL +0,09, UGL +0,09, GDXJ +0,10 (t 2,0), GDX +0,06.
  - 5 dk veri (60 gün), t-1 kapanış→15:30 ile son 30 dk arası: GLD +0,31 (t 2,5), IAU +0,32 (2,7), GDXJ +0,32 (2,1), GDX +0,23, NUGT +0,18, SLV +0,05.
  - Kapanışa doğru momentum var. Bu, kaldıraçlı ETF dengelemesiyle (ve gün-içi momentum literatürüyle) uyumlu.

### 5.3 Uygulanabilir sinyal: altının 15:00 ET'ye kadarki hareketi m_t

| m_t → hedef | n | IC | t | t_IS | t_OOS | t_22+ | yıl |
|---|---|---|---|---|---|---|---|
| **GDXJ h1** | 4239 | **−0,077** | **−5,30** | −4,80 | −2,77 | −2,21 | 15/18 |
| GDXJ h5 | 4235 | −0,068 | −4,49 | −3,13 | −3,27 | −1,23 | 16/18 |
| GDXJ h1, 14:00 ET kesim | 4235 | −0,081 | −5,59 | −4,89 | −3,08 | −2,36 | 16/18 |
| GDXJ − β·GLD h5 (göreli) | 4127 | −0,099 | −6,14 | −4,50 | −4,11 | −3,28 | 15/17 |
| GDX h1 | 4618 | −0,053 | −3,82 | −3,48 | −1,87 | −1,65 | 15/19 |
| GDX h5 | 4614 | −0,042 | −2,97 | −1,83 | −2,49 | −0,86 | 17/19 |
| GDX h1, 14:00 ET kesim | 4614 | −0,060 | −4,32 | −3,78 | −2,30 | −1,93 | 16/19 |
| JNUG h1 / NUGT h1 | 3272 / 3981 | −0,066 / −0,051 | −4,01 / −3,40 | −4,18 / −3,59 | −1,72 / −1,24 | | 11/14, 12/16 |
| AEM h1 / KGC h5 / RING h5 / SGDM h1 | | −0,046 / −0,041 / −0,033 / −0,044 | −3,24 / −2,83 / −2,08 / −2,61 | | | | |
| SLV h1 | 4618 | −0,025 | −1,69 | −0,47 | −1,98 | −1,81 | 11/19 |
| GLD h1 | 4618 | −0,026 | −1,74 | −1,52 | −0,96 | −1,18 | 14/19 |
| m_{t-1} (bir gün eski) → GDXJ h1 | 4238 | −0,021 | −1,37 | | | | |

- Etki madencilerde ve yeni bilgide yoğun. Bir gün eski hareket zayıf. Altının kendisinde küçük.
- Hem Asya-Avrupa kısmı (16:00 ET t-1 → 07:00 UTC t; GDXJ h1 t −2,7) hem ABD sabahı kısmı (07:00 UTC → 15:00 ET; t −3,8) katkı veriyor.
- Ayrıştırma (tanı): r_GDXJ,t+1 ~ m_t + madencinin gün t'deki kendine özgü getirisi. m_t katsayısı −0,151 (t −3,1), kendine özgü kısım +0,008 (t 0,2). Dönen, altın kaynaklı aşırı tepki. Madencinin kendi haberi dönmüyor.
- Kaldıraçlı ürün öncesi ve sonrası: GDX'te öncesi (2008-01..2010-12) IC −0,016 (t −0,4), sonrası −0,060 (t −4,0). GDXJ'de öncesi (2009-11..2013-10) −0,061 (t −2,0), sonrası −0,081 (t −5,0).
  - Alt dönem IC'leri: GDXJ 2013–16 −0,117; 2017–19 −0,094; 2020–21 −0,045; 2022+ −0,060.
  - Yıllara göre GDXJ IC: 2009 −0,24, 2010 −0,09, 2011 −0,06, 2012 +0,02, 2013 −0,15, 2014 −0,16, 2015 −0,16, 2016 −0,03, 2017 −0,17, 2018 −0,12, 2019 −0,01, 2020 −0,12, 2021 +0,05, 2022 −0,13, 2023 +0,03, 2024 −0,04, 2025 −0,10, 2026 −0,07.
  - Mekanizma kaldıraçlı ETF dengelemesiyle tutarlı ama tek açıklama değil. GDXJ'de kaldıraçlı ürün öncesinde de zayıf bir etki var.
- 2023–2024'te etki zayıfladı (IC +0,03 / −0,04). 2025–2026'da yeniden belirgin.

### 5.4 Stratejiler (IS'te seçim → OOS bir kez)

IS'te en güçlü uygulanabilir test m_t → GDXJ h1 (t_IS −4,80). Eşik ve h, yalnız uzun demeaned IS Sharpe'a göre seçildi: eşik=0, h=1.

| Kural | Sürüm | Maliyet | Sharpe IS | OOS | 2022+ | demeaned OOS | B&H OOS | uzun bacak OOS | kısa bacak OOS | uç dönem hariç | pozitif yıl |
|---|---|---|---|---|---|---|---|---|---|---|---|
| m_t<0 → GDXJ al, h=1 | yalnız uzun | 10 bps | 0,58 | **0,72** | 0,81 | 0,53 | 0,54 | 0,93 | — | 0,72 | 15/18 |
| | yalnız uzun | 20 bps | 0,39 | 0,51 | 0,59 | 0,32 | 0,54 | | | 0,50 | 14/18 |
| | yalnız uzun | 40 bps | 0,00 | 0,08 | 0,14 | | | | | | |
| m_t>0 → JDST | ters ETF'li | 10/20 bps | 1,03 | 0,41 | 0,41 | 0,46 | 0,54 | 0,93 | 0,05 | 0,75 | 11/14 |
| | ters ETF'li | 20/40 bps | 0,80 | 0,12 | 0,10 | 0,17 | | | | | |
| m_t<0 → GDX al, h=1 (IS seçimi değil) | yalnız uzun | 10 bps | 0,23 | 0,61 | 0,70 | 0,39 | 0,61 | 0,86 | | 0,58 | 14/19 |
| GDX IS seçimi (eşik 1,5, h=1) | yalnız uzun | 10 bps | 0,17 | 0,00 | 0,25 | −0,07 | 0,61 | | | | |
| m_t<0 → GLD al | yalnız uzun | 10 bps | −0,30 | 0,23 | 0,52 | −0,14 | 0,81 | | | | |
| m_t<0 → JNUG al (2×) | yalnız uzun | 20 bps | 0,84 | 0,43 | 0,61 | | 0,35 | | | | |

GDXJ yalnız uzun kuralının ayrıntıları:
- Maruziyet %47. Yılda ~66 gidiş-dönüş işlem.
- OOS başabaş maliyeti gidiş-dönüş ~44 bps (14:00 ET kesimle 40 bps).
- "Uzun gün" ortalama getirisi 18 yılın 17'sinde "nakit gün"den yüksek (`g_gdxj_yearly.csv`).
- Uç dönem PnL'i: 2013-04 −6,7%, 2020-03 −6,6%, 2026-01/02 +8,6%. 2008'de GDXJ yok. GDX'te 2008 IC +0,09, yani kriz yılında işaret ters.
- Strateji getirisinin kendi t'si (10 bps net): tam 2,70, IS 1,68, OOS 2,14.

Ters ETF (JDST) bacağı OOS'ta değer üretmiyor (Sharpe 0,05). Uç dönemlerde ağır kayıp veriyor (2020-03 −24,8%, 2026-01/02 −18,1%). Midas'ta yalnız uzun sürüm tercih edilmeli.

## 6. (e) BIST altın BYF'leri — gram altına göre prim

- BYF birim başına gram (20 günlük medyan): GLDTR ~0,086, ZGOLD ~0,107, ISGLK ~0,106. GLDTR'de oran 3 yılda ~0,089'dan 0,0834'e düştü (gider ve iç piyasa primi).
- Medyandan sapmanın sağlam std'si (MAD×1,48): GLDTR 81, ZGOLD 182, ISGLK 199 bps. AC1 0,84–0,91.
  - Sapma VİOP'tan ölçülen yurt içi gram primiyle ilişkili değil (corr −0,08 / −0,10 / −0,45).
  - 2026 Ocak–Şubat çöküşünde BYF'ler spotun +3 ile +8% üstünde fiyatlandı.

| Test (tamamı 2023-12+) | n | IC | t | yarı 1 / yarı 2 t (h1) |
|---|---|---|---|---|
| GLDTR prim 17:30 TSİ → GLDTR−gram h1 | 668 | −0,158 | −3,85 | −1,74 / −4,07 |
| GLDTR → h5 | 639 | −0,194 | −2,77 | (h5: −0,02 / −5,18) |
| GLDTR prim kapanış t-1 → h1 | 660 | −0,103 | −2,53 | |
| ZGOLD h1 / h5 | 668 / 639 | −0,069 / −0,137 | −1,77 / −2,09 | −0,47 / −2,35 |
| ISGLK h1 / h5 | 519 / 495 | −0,015 / −0,012 | −0,34 / −0,15 | |
| Prim → BYF'nin kendi getirisi (üçü) | | −0,02..+0,10 | ≤1,3 | |

Prim beşte birlik dilimlerine göre (GLDTR, bps): en düşük dilim (ort. −153) → göreli h1 +5, h5 +24. En yüksek dilim (ort. +150) → h1 −18, h5 −55. ZGOLD en yüksek dilim (+335) → h5 −82.

Dönüş göreli. BYF'nin kendi yönü öngörülmüyor. "İskontoda al" yalnız uzun kuralı yalnızca altın driftini taşıyor (Sharpe 0,77; GLDTR B&H 1,94). BIST'te ters altın BYF'si yok, ters ETF'li sürüm yapılamaz. → **DUSUK** (yalnız ~3 yıl, IS yok, üç fondan yalnız biri net). Pratik kullanım: BYF primi yüksekken (son 20 günün medyanına göre >+1%) BYF yerine VİOP gram/ons ya da ABD ETF'si seçmek.

## 7. (f) Hacim şokları

30 IC testi ve 12 olay testi yapıldı (GLD, GDX, GDXJ, SLV, IAU; vz ve vz×işaret(r_{t-1}); h 1/3/5). En güçlüleri:
- vz → GLD h1: IC +0,030, t 2,03 (OOS 0,94).
- vz → SLV h1: t 2,00 (IS 2,27, OOS 0,58).
- vz → IAU h5: t 0,84 (OOS 2,21, IS −0,82).

IS seçimi (SLV h1): yalnız uzun OOS 0,10 (B&H 0,53), ters ZSL'li 0,06. → **YOK.**

## 8. Olumsuz bulgular (test edildi, tutmadı)
1. GLD/GLDM pay akışları (1/5/20 gün, z, uçlar; t-1 ve t-2; GLD+GLDM $ akış) → GLD/IAU 1/3/5/10 gün: IS–OOS işaret dönüyor, çoklu test sonrası anlamsız.
2. Akış → VİOP fwd1/3/5 (VİOP 15:00 UTC'ye hizalı): en büyük \|t\| 1,93 (zf20 lag2 h1), IS ve OOS'ta anlamsız.
3. GLD primi: std 3–5 bps, maliyetin altında. prem_{t-1} ve gün-içi prim GLD'nin kendi getirisini öngörmüyor. Kapanış primindeki büyük "dönüş" ölçüm kaynaklı ve mekanik, ulaşılamaz.
4. Fon iskontosuna dayalı yönlü işlem (iskontoda PHYS/PSLV al, primde GLL/ZSL): OOS Sharpe 0,07 / −0,35. Ters sürümler negatif.
5. Araç değiştirme stratejisi (maliyet sonrası): PHYS ve CEF'te IS seçimi OOS'ta başarısız. PSLV uç dönemlere bağımlı.
6. GLD ve SLV'de kaldıraçlı ETF dengeleme dönüşü: m_t → GLD t −1,74 (OOS −0,96). Yalnız uzun GLD kuralı B&H'nin altında.
7. Büyük hareket olayları (\|z\|>2; gün t 15:00 ET ya da t-1 kapanış; GLD/GDX/GDXJ/SLV): hiçbiri IS ve OOS'ta birlikte anlamlı değil.
8. Ters ETF bacakları (GLL, DUST, JDST, ZSL): incelenen hiçbir stratejide OOS'ta kalıcı pozitif kısa bacak yok. DUST/JDST aşınması yılda −35..−50% (2020+).
9. Hacim şokları: yok.
10. BIST ISGLK primi: yok. ZGOLD zayıf.

## 9. Çoklu test
- Kayıtlı test: 455. Aileler: akış 119, prim 34, CEF 99 (54'ü strateji ızgarası), kaldıraçlı ETF ve madenci 121, BIST BYF 39, hacim 42, ana strateji 1.
- Ajan içi BH-FDR (`h_registry_with_fdr.csv`): 55 test q<0,05, 34 test Bonferroni (0,05/455) geçiyor. Bunların büyük kısmı tanı testi (ters yön, ulaşılamaz kapanış primi, gün-içi mekanik).
- Uygulanabilir olup Bonferroni geçen 23 test: m_t → GDXJ h1/h5; m14 → GDXJ h1/h5 ve GDX h1; göreli GDXJ h1/h5, GDX h5, RING h5; JNUG h1/h5; PHYS/GLD z20 ve z60 h1/h3/h5; CEF z20 ve z60 h1/h3/h5.
- GLDTR (q 0,0015) ve GDXJ strateji getirisinin kendisi (t 2,70, q 0,055) Bonferroni'yi geçmiyor. Global FDR orkestratörde yapılacak.

## 10. Midas için pratik özet
- **Tek uygulanabilir aday (YUKSEK, maliyete duyarlı):**
  - Gün t'de 15:00 ET'de (kışın 23:00, yazın 22:00 TSİ) spot altını dünkü 16:00 ET değeriyle karşılaştırın. 14:00 ET de aynı sonucu veriyor ve emre zaman bırakıyor.
  - Altın düşmüşse GDXJ'yi kapanışa yakın alın, ertesi gün kapanışa yakın satın. Ertesi gün altın yine düşmüşse pozisyonu koruyun.
  - Altın yükselmişse nakitte kalın. JDST ile kısa almayın.
  - Gidiş-dönüş toplam maliyet (komisyon + spread + kur) 20 bps'i geçerse avantaj hızla azalıyor. 40 bps'de yok oluyor.
  - Kapanış öncesi son 30 dakikada momentum olduğu için 15:45–15:55 ET'de girmek kapanış fiyatından biraz farklı sonuç verebilir.
- PHYS/GLD (ve CEF) iskontosu: ayrı strateji değil, giriş anında araç seçimi. PHYS/GLD z<−1,5 ise altın pozisyonunu PHYS ile açmak birkaç günde 6–20 bps avantaj sağlar.
- BIST BYF primi: BYF, spot gram altın değerinin belirgin üstündeyse (son 20 günün medyanına göre >+1%) BIST BYF yerine başka araç kullanın.
- GLD akışları, GLD primi ve hacim için izleme yapmaya gerek yok.

## 11. Sınırlamalar
- Giriş ve çıkış 16:00 ET kapanış fiyatıyla varsayıldı. Midas'ta MOC emri yoksa kayma maliyeti stres senaryosuna dahil sayılmalı.
- Dukascopy BID spotu ile LBMA ve borsa saatleri arasında saniye düzeyinde uyumsuzluklar var.
- BIST BYF verisi yalnız saatlik ve 3 yıllık. Kapanış seansı fiyatı son saatlik barın kapanışıyla yaklaşıklandı.
- GLDM'de IS yok.
- DUST/JDST'nin 2020'deki kaldıraç değişimi (3×→2×) ters ETF sürümünde zamana bağlı L ile işlendi.

## 12. Dosyalar (`out/e3_etf_akis_prim/`)
- Kod: `run_all.py` (hepsini yeniden çalıştırır, kayıt dosyasını sıfırlar), `common.py`, `a_flows.py`, `b_premium.py`, `c_cef.py`, `d_letf.py`, `d2_miners_robust.py`, `e_bist_byf.py`, `f_volume.py`, `g_main_claim.py`, `h_summary.py`, `parse_bist_byf.py`.
- Çıktılar: `*_tests.csv`, `*_strategies.csv`, `c_cef_magnitude.csv`, `c_cef_switch_strategies.csv`, `d_realized_leverage.csv`, `d_prepost_letf.csv`, `d_m_miner_subperiods.csv`, `d_intraday_lastseg.csv`, `e_bist_byf_quintiles.csv`, `g_gdxj_yearly.csv`, `g_main_claim.json`, `h_registry_with_fdr.csv`, `log_*.txt`, `bist_*_{1h,5m}.parquet`.
