# a5_esz_artik — 15:00 UTC'de aynı anda ölçülen göreli değer ve artık (idiosenkratik) altın hareketi
**Hedef:** VİOP F_XAUUSD, gün t uzlaşmasında gir (≈15:05–15:15 UTC VWAP), t+h uzlaşmasında çık, h = 1, 3, 5 iş günü.
**Soru:** Altının 15:00→15:00 getirisinin çapraz varlıklarla açıklanamayan kısmı (artık) ya da altın/gümüş, altın/platin gibi oranların sapması sonraki 1–5 günde dönüyor mu, sürüyor mu? Gün içinde dolar, T-bond ve S&P hareketine altının eksik tepkisi sonradan kapanıyor mu ("yetişme")?

---
## 0. Kısa sonuç

1. **Toplam 1.048 hipotez testi** `register(agent='a5_esz_artik')` ile kayda geçti (başarısızlar dahil). Dağılım: VİOP hedefi 483, spot hedefi 438, sağlamlık/kontrol/erken dönem 127.
2. **Ailenin büyük kısmı gürültü.** VİOP ızgarasında |t|>2 oranı %3,9, spot ızgarasında %2,7; ikisi de sıfır hipotezinin beklediği %5'in altında. A (15→15 artık) ve B (oran) ailelerinde IS→OOS işaret uyumu sırasıyla %37 ve %33, yani yazı turasından kötü. Her aile ve h için IS'te seçilen 18 spesifikasyondan yalnız 5'i OOS'ta işaretini korudu. OOS'ta hem aynı işarette kalıp hem |t|≥2 veren olmadı.
3. **"Eksik tepki → yetişme" hipotezi reddedildi.** β·x − altın kapanmıyor. Ölçülen işaret tam tersi: altının makro faktörlerle açıklanmayan **gün içi** hareketi zayıf biçimde **sürüyor**.
4. **Tek tutarlı aile gün içi artık sürmesi (C).** 54 testin %98'inde IC pozitif, IS→OOS işaret uyumu %85, |t|>2 oranı %17. Testler birbirine çok bağımlı olduğu için bu 54 bağımsız kanıt sayılmaz.
5. **En güçlü tek kural (C1, ORTA ama kırılgan).** Koşul: 12:00–15:00 UTC'de DXY+T-bond+S&P'nin altına ima ettiği hareket büyük olmalı (|fit/σ| > 1,096, IS'in 80. yüzdeliği). Kural: o pencerede altının artığının işaretinde 3 gün pozisyon. Sonuçlar:
   - rank-IC t: tam dönem 2,95, IS 2,10, OOS 1,93; spot hedefte OOS 2,65.
   - Net Sharpe (5 bps): OOS 0,60; demeaned 0,58.
   - Zayıf yanları: getiri ağırlıklı (Pearson) t 1,23, P&L t 1,64. IS kanıtı büyük ölçüde 2020'den geliyor (2020 hariç IS t 0,38). Kazancın çoğu uzun bacakta. Yılda ≈37 sinyal.
6. **Altın/gümüş 5 günlük göreli hareket (B1, DÜŞÜK).** Altın son 5 günde gümüşü geçtiyse ertesi gün altın zayıf:
   - t: tam dönem −2,49, IS −0,68, OOS −2,82.
   - Yalnız 2022 sonrasında ve 2010–2016'nın Yahoo vekilinde (h=3/5) görülüyor; 2017–2021'de yok.
7. **15→15 yuvarlanan-beta artığı (A ailesi, 11 model × 3 pencere × 3 k × 3 h): YOK.** IS'te seçilenler (EURUSD, BTC) OOS'ta işaret değiştirdi. Kanonik W120/k1 sürümünde (β·x − altın) hiçbir çiftte |t| 1,7'yi geçmiyor.
8. **Oran z-skorları (altın/gümüş 15:00; altın/platin Yahoo t-1), VİOP kapanışındaki altın/gümüş oranı: YOK** ya da IS–OOS işareti tutarsız.
9. **Pratik not (aile dışı).** VİOP vadeli 2023–2026'da spotun yıllık ≈%5,5–7,4 üzerinde (bazın yıllıklaştırılmış hali). Uzun pozisyon roll maliyeti bu kadar. Buy & hold VİOP Sharpe: IS 0,47, OOS 0,53.

---
## 1. Veri, bilgi zamanı ve ileriye bakma kontrolü

| Öngörücü | Kaynak | Bilgi zamanı (UTC) | ≤ 15:00 UTC? |
|---|---|---|---|
| `xau_p15`, `dk_<SYM>_p15` | Dukascopy BID saatlik, 14:00 mumunun kapanışı | gün t 14:59:59 | Evet. Saatlik mumla birebir doğrulandı (örn. 2023-01-10 XAU 1878,165 = 14:00 mum kapanışı) |
| `xau_p12`, 12:00 çapraz varlık (`a5_01.snap`) | Dukascopy saatlik, 11:00 mumunun kapanışı | gün t 11:59:59 | Evet |
| `xau_p07`, `dk_<SYM>_p07` | 06:00 mumunun kapanışı | gün t 06:59:59 | Evet |
| `y_GC_F`, `y_SI_F`, `y_PL_F` (Yahoo) | son bilinen ABD kapanışı | ≤ t−1 22:00 (paneldeki `*_avail − t` en çok −2 saat) | Evet ("t−1 sürümü") |
| Yuvarlanan beta, artık σ | yalnız [t−W, t−1] satırları | t−1 | Evet |
| `v_settle`, `vo_xag_settle` (E ailesi) | VİOP uzlaşması | t 15:10 | **Hayır. KAPANIŞTA HESAPLANAN** olarak işaretli; t−1 sürümü (`lag1`) ve 15:00 spot sürümü (B ailesi GSRD) ayrıca verildi |

- **Placebo (`placebo_lead`, `placebo.csv`).** Adayların IC'si sinyali 1–3 gün geri kaydırınca düzgün sönüyor. C1: 0,171 (kaydırmasız) → 0,095 (1 gün) → 0,010 (2 gün). B1: −0,052 → −0,024 → −0,010. Kaydırmasız değerde aşırı bir sıçrama yok. Sinyali ileri kaydırınca (yasak yön) IC büyüyor (0,3–0,8). Bunun nedeni t+1'in getirisinin hedefle çakışması; beklenen bir sonuç.
- **Spot görüntü gürültüsü.** `sfwd` hedefi aynı 15:00 görüntüsünden başlıyor. Bu yüzden adaylarda 1 saat atlamalı hedef de kullanıldı: log(p15_{t+h} / p16_t). VİOP hedefinde bu sorun yok, çünkü giriş fiyatı 15:05–15:15 VWAP ve 15:00 görüntüsünden bağımsız.
- **Veri temizliği.** Tek açık hatalı baskı NaN yapıldı: `dk_USTBONDTRUSD_p15` 2018-02-06 (141,1 → 129,9 → 142,6). Metal ve kriptodaki sert gidiş-dönüşler gerçek olaylar (Şubat 2021 gümüş sıkışması, Ocak–Şubat 2026) ve tutuldu.
- **Eksik veri.** XPTUSD Dukascopy verisi indirilememiş, platin yalnız Yahoo PL_F/GC_F t−1 kapanışlarıyla test edildi. Kapsama: XAG, SPX, USDJPY, EURUSD, USDCNH, COPPER 2016+; BTC 2017-05+; DXY 2017-12+; T-bond 2018-01+ (C1'in ilk sinyali 2019-08). VIX ve Brent CFD kısa olduğu için kullanılmadı.

## 2. Yöntem

- **Getiriler.** Altın g_t = log(xau_p15_t / xau_p15_{t−1}). Çapraz varlık x_t de aynı 15:00→15:00 penceresinden. Hesap spot (Dukascopy) takviminde yapıldı, sonra VİOP günlerine eşlendi.
- **Artık (A ailesi).** g_t = a + b'x_t + e_t. (a, b) yalnız t−W..t−1 günlerinden OLS ile tahmin edildi; en az 0,8W gözlem şartı var. W ∈ {60, 120, 250}. Sinyal z_k = Σ_{j<k} e_{t−j} / (σ_e,t √k), k ∈ {1, 3, 5}.
  - Modeller: tek faktör XAG, DXY, TBOND, SPX, USDJPY, USDCNH, BTC, EURUSD; çok faktör MACRO3 (DXY+TBOND+SPX), FX3 (EURUSD+USDJPY+USDCNH), ALL7 (XAG+DXY+TBOND+SPX+USDJPY+USDCNH+bakır).
  - Negatif IC dönüş ya da yetişme demek, pozitif IC sürme demek. "β·x − altın" = −e (k=1).
  - Ayrıştırma: fitted (b'x/σ) ve altının kendi getirisi ayrıca test edildi.
- **Oranlar (B ailesi).**
  - GSRZ_L: log(XAU15/XAG15)'in L ∈ {20, 60, 120} günlük z-skoru.
  - GSRD_k: oranın k günlük değişimi (β=1 artık), 120 günlük geçmiş σ ile standartlaştırılmış.
  - GPTZ / GPTD: altın/platin (Yahoo t−1). GSYD: altın/gümüş Yahoo t−1, erken dönem için.
  - Tanı testi: oran iki bacaklı spread'de dönüyor mu (altın − gümüş ileri getirisi)?
- **Gün içi (C ailesi).**
  - g12 = log(XAU 15:00/12:00), x12 = DXY, T-bond, S&P (ve MACRO3) aynı pencerede. Beta geçmiş W günden. Sinyal e/σ.
  - Koşullu sürüm: |fit/σ| > IS'in 80. yüzdeliği (önceden sabitlendi; q70 ve q90 duyarlılık için).
  - 07:00–15:00 (Londra+NY sabahı) MACRO3 sürümü ayrıca var.
- **E ailesi.** VİOP uzlaşmalarıyla altın/gümüş (2021+). Kapanışta hesaplanıyor; t−1 sürümü de var.
- **İstatistik.** `split_stats` ile Spearman IC, Newey-West t (lag = max(h, 5)), IS 2017-03..2021-12 (spot: 2016-01..2021-12), OOS 2022-01..2026-11, yıl yıl işaret. Adaylarda ayrıca Pearson IC ve kısmi regresyon.
- **Seçim kuralı.** Her aile ve her h için |t_IS| en büyük olan spesifikasyon (`is_selection.csv`). OOS bir kez okundu. Göze çarpan diğerleri **post-hoc** olarak işaretli.
- **Backtest (`legs_bt`).** Yön = IS IC işareti. Kurallar: "sign" (sürekli ±1; koşullu sinyalde yalnız koşul günleri) ve "thr1" (|z|>1; koşullu sinyalde |z|>0,5). Kademeli h günlük tutuş, 5 bps gidiş-dönüş (stres 10 bps), demeaned Sharpe, uzun ve kısa bacak ayrı, buy & hold kıyası. Getiri `v_ret`, yani aktif kontrat içinde, roll'dan bağımsız.
- **Sağlamlık.** Pencerede roll (`v_code` değişimi) olan günler hariç; Mart 2020 ve Ocak–Şubat 2026 hariç; IS 1/99 yüzdelikte winsorize; spot hedef; 1 saat atlamalı spot hedef; 2016-01..2017-03 spot alt dönemi. Aktif kontratta **sıfır hacimli gün yok** (`v_volume==0` sayısı 0), o yüzden ayrı kontrol gerekmedi.

## 3. Test sayısı ve aile düzeyinde teşhis

| Aile (VİOP hedefi) | n | |t|>2 | maks |t| | IC>0 oranı | IS→OOS aynı işaret |
|---|---|---|---|---|---|
| A_resid (15→15 artık) | 297 | 6 | 2,35 | 0,53 | 0,37 |
| A_fitted (faktörün ima ettiği hareket) | 33 | 1 | 2,10 | 0,45 | 0,48 |
| A_own (altının kendi getirisi, kontrol) | 9 | 0 | 1,58 | 0,67 | 0,22 |
| B_ratio (oran z / Δk, gümüş ve platin) | 36 | 1 | 2,49 | 0,47 | 0,33 |
| B_spread_diag (iki bacaklı spread tanısı) | 18 | 0 | 1,54 | 0,72 | 0,89 |
| C_intraday artık (12–15, 07–15, koşullu) | 54 | 9 | 2,95 | **0,98** | **0,85** |
| C_intraday fitted | 9 | 0 | — | 0,67 | 0,67 |
| E_viop_close (kapanışta hesaplanan) | 27 | 2 | 2,17 | 0,07 | 0,26 |

Spot ızgarası (438 test) VİOP ızgarasıyla t düzeyinde 0,93 korelasyonlu; işaret uyumu %88. Kayıt dökümü: A_resid 297, A_resid_spot 297, C 63+63, R_robust 59, B 36+36, A_fitted 33+33, X_extra 31, E 27, K_control 19, B_spread_diag 18, B_early 18, A_own 9+9. **Toplam 1.048.**

**IS seçimleri ve OOS (`is_selection.csv`):**

| Aile | h | IS'te seçilen | t_IS | t_OOS | Aynı işaret? |
|---|---|---|---|---|---|
| A_resid | 1 | EURUSD W60 k1 | 2,49 | −0,41 | hayır |
| A_resid | 3 | BTC W250 k5 | −2,71 | 1,58 | hayır |
| A_resid | 5 | BTC W250 k3 | −3,18 | 1,01 | hayır |
| B_ratio | 1/3/5 | GSRZ L120 | 1,30 / 1,57 / 2,11 | −1,30 / −0,75 / −0,17 | hayır |
| C_intraday | 1 | I12 koşullu MACRO3 W250 | 3,58 | −0,02 | hayır |
| **C_intraday** | **3** | **I12 koşullu MACRO3 W60 (C1)** | **2,10** | **1,93** | **evet** |
| C_intraday | 5 | I12 koşullu MACRO3 W250 | 1,30 | 1,47 | evet |
| E | 1/3/5 | VGSRD k1 lag1 / VGSRD k1 / VGSRZ L120 | 2,26 / 1,46 / 1,34 | −0,93 / −1,55 / 0,11 | hayır / hayır / evet |

## 4. Bulgular

### 4.1 15→15 artık ve "β·x − altın" (A ailesi): YOK
Kanonik W=120, k=1 için VİOP hedefinde t (h=1/3/5). Negatif t yetişme ya da dönüş demek.

| Çift | t h1 | t h3 | t h5 | t_IS h1 | t_OOS h1 |
|---|---|---|---|---|---|
| Gümüş (XAG) | 0,07 | −0,17 | −0,63 | 0,88 | −0,80 |
| DXY | 1,35 | 0,75 | −0,18 | 2,06 | 0,02 |
| T-bond | 1,44 | 0,99 | 0,17 | 1,74 | 0,58 |
| S&P (USA500) | 1,39 | 1,62 | 0,26 | 2,15 | −0,14 |
| USDJPY | 1,66 | 1,73 | −0,24 | 1,49 | 0,90 |
| USDCNH | 1,09 | 0,67 | −0,31 | 1,62 | −0,10 |
| BTC | 0,97 | 1,04 | −0,21 | 1,41 | −0,04 |
| EURUSD | 1,23 | 0,89 | −0,26 | 2,12 | −0,27 |
| MACRO3 | 1,65 | 1,62 | 0,65 | 1,74 | 0,75 |
| FX3 | 1,36 | 0,93 | −0,36 | 2,15 | −0,14 |
| ALL7 | 0,43 | 0,68 | −0,22 | 0,68 | −0,01 |

- Hiçbir çiftte yetişme (negatif ve anlamlı t) yok. Makro faktörlere göre artıkta IS'te hafif pozitif bir eğilim var (sürme), ama OOS'ta kayboluyor.
- Tam dönemde en iyi görünen post-hoc spesifikasyonlar 297 testin maksimumu, yani gürültüyle uyumlu:
  - USDJPY W60 k3 h1: t 2,35 (IS 1,02, OOS 2,22).
  - MACRO3 W250 k3 h1: t 2,29 (IS 1,14, OOS 1,90).
- **Kontroller.**
  - Altının kendi 15→15 getirisi: k=1,3,5 × h için hepsi |t| < 1,6 (`A_own`).
  - Faktörün ima ettiği hareket (fitted): yalnız gümüşte zayıf pozitif. Gümüş bugün yükseldiyse altın sonraki 3 günde yükseliyor: t 2,10, IS 1,79, OOS 1,18.
  - Ham gümüş getirisi: K_xag1 h3 t 1,63; K_xag5 h1 t 1,52 (IS −0,22, OOS 2,16). Hiçbiri kural olacak kadar sağlam değil.

### 4.2 Oranlar (B ailesi) ve kapanışta hesaplanan VİOP oranı (E): çoğu YOK
- **Altın/gümüş log oran z-skoru** (L=20/60/120): IS ve OOS işaretleri ters. IS'te en iyisi L120 (h5 t_IS 2,11), OOS'ta −0,17. **YOK.**
- **Altın/platin** (Yahoo t−1, z ve Δk; 18 test): maks |t| 1,07. **YOK.**
- **Altın/gümüş 3–5 günlük değişim (GSRD).** Negatif IC: altın gümüşü geçtiyse ertesi günlerde altın zayıf.
  - k5 h1: t −2,49, IS −0,68, OOS −2,82. Spot hedefte −3,06; 1 saat atlamalı hedefte −3,00 (OOS −3,25).
  - Yıllık IC: 2018, 2019 ve 2021'de pozitif, 2022–2026'nın hepsinde negatif. IS'te yok, OOS'ta var: rejime bağlı.
  - Kısmi regresyon (fwd ~ altın5 + gümüş5): iki bacak tek başına anlamlı değil, etki oranın kendisinde.
  - İki bacaklı spread tanısı: oran spread olarak 1–5 günde dönmüyor (18 test, maks |t| 1,54). Yani "gümüş yetişir" değil; tek bacakta altın zayıflıyor.
  - **DÜŞÜK.**
- **E ailesi (VİOP uzlaşmalarıyla, kapanışta hesaplanan).** VGSRD k5 h1 t −2,17 (IS +0,73, OOS −2,46); t−1 sürümü −1,36. B1 ile aynı OOS rejimi, IS'te ters. **YOK/DÜŞÜK.**

### 4.3 Gün içi eksik tepki (C ailesi): yetişme YOK, zayıf sürme VAR
- **Koşulsuz.** 12–15 UTC MACRO3 W60 artığı: h1 t 2,08 (IS 2,21, OOS 0,98). 07–15 UTC MACRO3 W60: h1 t 2,60 (IS 2,66, OOS 1,38). İşaret pozitif: altın makronun ima ettiğinden fazla yükseldiyse ertesi gün de yükselme eğiliminde. Yetişme hipotezinin (negatif IC) tam tersi.
- **Kontrol.** Altının kendi 12–15 getirisi (g12) h1 t 1,22, OOS 0,22; 07–15 (g07) h1 t 1,35. Rank IC'de artık kendi getirisinden güçlü. Pearson kısmi regresyonda ise koşulsuz artık g12'yi kontrol edince anlamsız (t 0,82).
- **Koşullu (büyük makro günleri, C1).**
  - 9 spesifikasyonun hepsi pozitif (VİOP t 0,86–2,95; spot 1,37–3,40).
  - Eşik yükseldikçe güçleniyor (h3): q70 t 3,27 (OOS 2,56); q80 t 2,95 (OOS 1,93); q90 t 4,02 (OOS 2,82; n=150).
  - Aynı günlerde altının kendi g12'si h3'te t 0,97: etki artıkta, kendi momentumda değil.
  - Altının kendisinin büyük hareket ettiği günlerle koşullayınca h3 t 0,23; sakin makro günlerinde h3 t −0,13. Etki makro günlerine özgü.
  - Tek faktörlü koşullu sürümler: S&P h3 t 2,60, DXY h1 2,24, T-bond anlamsız.

## 5. Aday sinyallerin sağlamlığı (VİOP hedefi; t değerleri)

| Aday | Seçim | h | n | t | t_IS | t_OOS | Yıl | Spot t (OOS) | Atlamalı t (OOS) | Roll hariç | Uç hariç | Pearson t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **C1** I12 koşullu MACRO3 W60 | IS | 3 | 272 | **2,95** | 2,10 | 1,93 | 6/7 | 3,43 (2,65) | 3,48 (2,94) | 2,74 | 2,69 | 1,23 (kırpılmış: 3,11) |
| C2 I12 koşullu MACRO3 W250 | IS | 1 | 297 | 1,74 | 3,58 | −0,02 | 4/6 | 1,96 (0,39) | 1,77 (0,71) | 1,28 | 1,49 | — |
| C3 I12 MACRO3 W60 | post-hoc | 1 | 1803 | 2,08 | 2,21 | 0,98 | 6/8 | 1,87 (1,08) | 1,76 (0,95) | 1,94 | 1,67 | — |
| C4 I07 MACRO3 W60 | post-hoc | 1 | 1819 | 2,60 | 2,66 | 1,38 | 6/8 | 2,03 (0,99) | 1,84 (0,78) | 2,49 | 2,07 | — |
| **B1** GSRD k5 | post-hoc | 1 | 2354 | **−2,49** | −0,68 | −2,82 | 7/10 | −3,06 (−2,88) | −3,00 (−3,25) | −2,36 | −2,63 | −1,34 |
| B2 GSRD k3 | post-hoc | 3 | 2358 | −1,84 | −0,25 | −2,37 | 6/10 | −2,25 (−2,54) | −2,28 (−2,67) | −1,58 | −1,84 | — |
| A1 MACRO3 W250 k3 | post-hoc | 1 | 1688 | 2,29 | 1,14 | 1,90 | 6/7 | 1,98 (1,60) | 1,72 (1,41) | 2,28 | 1,97 | — |
| A2 USDJPY W60 k3 | post-hoc | 1 | 2406 | 2,35 | 1,02 | 2,22 | 7/10 | 1,98 (1,56) | 1,44 (1,14) | 2,21 | 2,12 | 1,98 |
| A3 EURUSD W60 k1 | IS | 1 | 2402 | 1,36 | 2,49 | −0,41 | 6/10 | 1,16 (−0,90) | 0,92 (−1,26) | 1,31 | 1,13 | — |
| A4 BTC W250 k3 | IS | 5 | 2099 | −1,08 | −3,18 | 1,01 | 6/9 | −1,03 (1,08) | −0,97 (1,09) | −1,21 | −0,68 | — |

**C1'in kırılganlığı.**
- 2020 hariç tutulunca IS t 2,10'dan 0,38'e düşüyor; OOS 1,93 olarak kalıyor (`X_C1_ex2020_h3`).
- Ham Pearson IS t 0,28. Artık ±3σ'da kırpılınca 1,94. Çok büyük artıklar sürmüyor, işaret ve sıra sürüyor.
- Kısmi Pearson regresyonda (resid + fit) h3 t 1,34, h5 t 2,91.

### 5.1 Backtest (net 5 bps; yön = IS işareti; `backtests.csv`)

| Aday / kural | SR IS | SR OOS | SR OOS 10 bps | dm OOS | Uzun OOS (dm) | Kısa OOS (dm) | Yıllık getiri IS / OOS | Devir/yıl | Maruziyet | P&L t (tam) |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 sign | 0,47 | 0,60 | 0,45 | 0,58 | 0,93 (0,70) | −0,23 (0,01) | %1,6 / %1,9 | 17 | 0,09 | 1,64 |
| C1 \|z\|>0,5 | 0,47 | 0,73 | 0,61 | 0,72 | 1,00 (0,82) | −0,17 (0,05) | %1,4 / %2,1 | 12 | 0,07 | 1,85 |
| C3 \|z\|>1 | 0,94 | 0,27 | −0,02 | 0,28 | 0,23 (0,03) | 0,17 (0,33) | %5,9 / %2,9 | 93 | 0,21 | 1,56 |
| C4 \|z\|>1 | 0,82 | 0,88 | 0,60 | 0,87 | 0,76 (0,56) | 0,52 (0,67) | %5,6 / %9,7 | 93 | 0,22 | 2,58 |
| C4 sign | 0,55 | 0,04 | −0,29 | 0,02 | 0,36 (−0,02) | −0,28 (0,05) | %6,1 / %0,8 | 182 | 0,75 | 0,68 |
| B1 sign | 0,06 | 1,12 | 0,98 | 1,11 | 1,24 (0,86) | 0,35 (0,70) | %0,8 / %19,2 | 99 | 0,97 | 2,02 |
| B1 \|z\|>1 | −1,19 | 0,72 | 0,59 | 0,70 | 0,55 (0,36) | 0,46 (0,65) | −%9,8 / %7,8 | 52 | 0,29 | −0,31 |
| A2 sign | 0,15 | 0,65 | 0,47 | 0,63 | 0,80 (0,42) | 0,13 (0,47) | %2,0 / %11,8 | 138 | 0,99 | 1,33 |
| A3 sign (IS seçimi) | 0,54 | −0,81 | −1,17 | −0,81 | −0,25 | −0,91 | %7,0 / −%14,6 | 257 | 0,99 | −0,77 |
| A4 sign (IS seçimi) | 0,98 | −0,26 | −0,36 | −0,27 | 0,29 | −0,57 | %7,5 / −%3,2 | 46 | 0,45 | 0,66 |
| **Buy & hold VİOP** | **0,47** | **0,53** | | | | | | | 1,00 | |

**C1 yıl yıl (sign kuralı, `c1_trades_by_year.csv`).**

| Yıl | Sinyal sayısı | Net getiri | Ort. işlem (brüt) |
|---|---|---|---|
| 2019 | 39 | −%3,1 | −11 bps |
| 2020 | 34 | +%11,9 | +100 bps |
| 2021 | 48 | −%1,0 | −1 bps |
| 2022 | 29 | +%2,0 | +25 bps |
| 2023 | 55 | +%5,4 | +34 bps |
| 2024 | 24 | −%0,5 | −1 bps |
| 2025 | 11 | −%3,4 | −88 bps |
| 2026 | 32 | +%5,7 | +58 bps |

- İşlem başı 3 günlük brüt ortalama 23 bps: IS 24, OOS 23 bps. Koşulsuz 3 günlük drift 9,4 bps.
- Uzun işlemler ortalama 39 bps, kısa işlemler (kısa getirisi) 7 bps.
- P&L yılların yalnız 4/8'inde pozitif.

## 6. Erken dönem (2010–2017) tekrarı (`early.csv`)
- **C ve A adayları.** Dukascopy çapraz varlık saatlik verisi 2016 (DXY 2017-12, T-bond 2018) öncesinde yok, bu yüzden 2010–2016 tekrarı mümkün değil. 2016-01..2017-03 spot alt döneminde A2 için IC 0,01 (t 0,08, n=251), yani tekrar etmiyor.
- **B1 (altın/gümüş, Yahoo GC/SI t−1 vekili).** 2010-01..2017-03, spot hedef:

| Sinyal | h=1 t | h=3 t | h=5 t |
|---|---|---|---|
| k=5 | −1,16 | **−2,33** | **−2,46** |
| k=3 | 1,15 | −1,04 | −1,96 |
| k=1 | **+2,60** | 1,58 | −0,03 |

  - Yıllık IC (k5, h5) 8 yılın 6'sında negatif.
  - Aynı vekil 2017+ VİOP'ta: k5 h1 −1,35, k3 h1 −2,29.
  - 2016-01..2017-03 Dukascopy GSRD k5 h1: IC −0,10, t −1,39 (n=205).
  - Sonuç: 5 günlük göreli hareketin tersine dönmesi 2010–2016 ve 2022–2026'da var, 2017–2021'de yok. 1 günlük hareket erken dönemde tersine sürmüş. İstikrarsız.

## 7. Güven etiketleri ve gerekçe

| İddia | Etiket | Gerekçe |
|---|---|---|
| C1: büyük makro günlerinde 12–15 UTC altın artığı 3 gün sürer | **ORTA (kırılgan)** | Rubrikteki ORTA koşulları sağlanıyor: tam dönem rank-IC t 2,95, IS ve OOS aynı işaret, aile düzeyinde IS→OOS işaret uyumu %85, spot ve atlamalı hedefte OOS t 2,65 / 2,94. Kanıt yine de ince: VİOP OOS t 1,93 < 2, Pearson t 1,23, P&L t 1,64, IS kanıtı 2020'ye dayalı, ≈1.000 test içinde seçildi. Global FDR'den geçmesi beklenmez. |
| C4: 07–15 UTC artığı \|z\|>1 iken ertesi gün sürer | DÜŞÜK | Post-hoc. OOS IC t 1,38; spot OOS 0,99; atlamalı OOS 0,78. Backtest iyi (OOS SR 0,88) ama IC ile tutarsız. |
| B1: altın/gümüş 5 günlük göreli hareket tersine (tek bacak) | DÜŞÜK | ORTA eşiklerini biçimsel olarak karşılıyor (tam dönem t −2,49, OOS aynı işaret) ama post-hoc seçildi. IS t −0,68, IS backtest SR 0,06, rejime bağlı. B ailesinde IS→OOS işaret uyumu %33. |
| Yetişme (β·x − altın kapanır), gün içi ve 15→15 | YOK | İşaret ters ya da sıfır. |
| 15→15 yuvarlanan-beta artığında dönüş ya da sürme (11 model) | YOK | |t|>2 oranı %2, IS→OOS uyumu %37, IS seçimleri OOS'ta tersine döndü. A1/A2'nin OOS'taki pozitif görünümü 297 test içinde post-hoc. |
| Oran z-skorları (altın/gümüş, altın/platin), VİOP kapanış oranı | YOK | |

YÜKSEK etiketli bulgu yok.

## 8. Negatif bulgular (test edildi, tutmadı)
1. Yetişme / eksik tepki: 12–15 UTC'de dolar, T-bond ve S&P'ye beta altında tepki veren altın sonraki 1–5 günde yetişmiyor. 45 test, işaret hep ters (sürme).
2. [t−1 15:00 → t 15:00] çapraz varlık hareketinin altına yansımamış kısmı (β·x − altın) sonraki 1/3/5 günü öngörmüyor. Gümüş, platin, DXY, T-bond, USDJPY, USDCNH, BTC, S&P, EURUSD, MACRO3, FX3, ALL7 için W60/120/250, k1/3/5 denendi.
3. IS'te en iyi görünen A spesifikasyonları OOS'ta işaret değiştirdi: EURUSD artığı (IS t 2,49 → OOS −0,41; backtest OOS SR −0,81) ve BTC artığı (IS −3,18 → OOS +1,01).
4. Altın/gümüş log oran z-skoru (20/60/120 gün) seviye dönüşü yok. IS ve OOS işaretleri ters.
5. Altın/platin oranı (Yahoo t−1; z ve Δk, 18 test) için kanıt yok; maks |t| 1,07.
6. Altın/gümüş oranı iki bacaklı spread olarak 1–5 günde dönmüyor (18 test).
7. VİOP uzlaşmasıyla hesaplanan altın/gümüş (2021+) ve t−1 sürümü: IS–OOS işaretleri tutarsız.
8. Faktörün ima ettiği hareket (fitted) altının sonraki getirisini öngörmüyor (gümüş h3 t 2,10 hariç; IS 1,79, OOS 1,18, zayıf).
9. Altının kendi 15→15 getirisi (1/3/5 günlük toplam) 1/3/5 günü öngörmüyor (kontrol).
10. IS'te seçilen 12–15 koşullu W250 h1 (IS t 3,58) OOS'ta sıfır (−0,02).
11. 07–15 ve 12–15 koşulsuz artıkla "sign" kuralı (sürekli pozisyon) OOS'ta 5 bps sonrası sıfır ya da negatif Sharpe veriyor.

## 9. Trader için sonuç
- Bu ailede günlük işlem kuralı olarak önerilebilecek bir şey yok.
- En fazla şu kadarı söylenebilir: büyük ABD makro hareketi olan günlerde (12:00–15:00 UTC'de DXY, faiz ya da S&P büyük oynadığında) altın makronun ima ettiğinden ayrışmışsa ayrışma yönünde 3 günlük pozisyon tarihsel olarak hafif pozitif.
  - Bunu bağımsız bir kural olarak değil, başka bir sinyalin filtresi ya da teyidi olarak düşünün.
  - Yılda ≈37 sinyal, işlem başı brüt ≈23 bps.
  - "Altın makroya göre geride kaldı, yetişir" mantığı veride **yok**. Ters yönde işlem açmak tarihsel olarak zarar ettirmiş.
- Altın/gümüş 5 günlük göreli hareket 2022'den beri altın için ertesi gün ters işaret veriyor, ama 2017–2021'de vermedi. Rejime bağlı, izlenebilir ama güvenilmez.
- VİOP'ta uzun tutmanın roll maliyeti 2023–2026'da yıllık ≈%5,5–7,4 (vadeli primi). Uzun ağırlıklı her stratejiyi buna göre değerlendirin.

## 10. Dosyalar ve yeniden üretim
Dizin: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik/`. Hepsini sırayla çalıştırmak için `run_all.sh` (≈50 sn; kayıt dosyası a5_02'de sıfırlanır).

| Dosya | İçerik |
|---|---|
| `a5_lib.py` | Yuvarlanan geçmiş-yalnız OLS artığı (`roll_resid`), `cum_z`, bacak ayrımlı backtest (`legs_bt`) |
| `a5_01_signals.py` | Tüm sinyaller → `signals_spot.parquet`, `signals_meta.csv` |
| `a5_02_tests.py` | VİOP ızgarası (483 test) → `grid_viop.csv` |
| `a5_03_robust.py` | Kontroller, adayların sağlamlığı, placebo, backtest, erken dönem → `controls.csv`, `partials.csv`, `robust.csv`, `placebo.csv`, `backtests.csv`, `early.csv` |
| `a5_04_spotgrid.py` | Spot ızgarası (438 test) → `grid_spot.csv` |
| `a5_05_extra.py` | C1 çürütme testleri → `extra.csv`, `c1_partial.csv`, `c1_trades_by_year.csv` |
| `is_selection.csv`, `pair_canonical_W120_k1.csv`, `pair_summary.csv`, `log_summary.txt` | Özet tablolar |
| `../registry/a5_esz_artik.csv` | Kayıt: 1.048 satır |

**Not.** Çalışma sırasında başka bir süreç `panel/duka/*.parquet` saatlik dosyalarını güncelledi (23:30 UTC). Raporlanan rakamlar bu güncel veriyle yapılan son tam çalıştırmaya ait. Önceki çalıştırmayla farklar küçük: örneğin C1 t 3,00 → 2,95.
