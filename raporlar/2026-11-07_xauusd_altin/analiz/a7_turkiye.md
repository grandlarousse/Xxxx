# a7_turkiye — Türkiye'ye özgü bilgi, Türkiye altın fiyatı ve VİOP Ons Altın (F_XAUUSD)

Tarih: 2026-11-07. Ajan anahtarı: `a7_turkiye`. Kod ve çıktılar: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye/` (`run_all.sh` hepsini yeniden üretir).
**Toplam kayıtlı hipotez testi: 162.** Bunların 120'si XAUUSD hedefli, 42'si gram altın, USDTRY ya da tanı testi (`registry/a7_turkiye.csv`, FDR'li kopya `registry_with_fdr.csv`).

## 0. Kısa sonuç

1. **Türkiye'ye özgü hiçbir değişken ons altını (VİOP XAUUSD) 1, 3 ya da 5 günlük ufukta güvenilir biçimde öngörmüyor.** 120 XAUUSD hedefli testin 9'unda p<0,05 çıktı. Şansla beklenen sayı 6. En küçük BH-q değeri 0,65. Yalnız IS'e bakılarak seçilen en iyi 3 kuralın OOS Sharpe'ı +0,16, −0,34 ve −0,94 (5 bps). Aynı dönemde buy & hold 0,53.
2. Bunun mekanizması basit. VİOP ons altın uzlaşması dünya spotunu çok yakından izliyor: günlük getiri korelasyonu 0,977, beta 0,98. TL şoku, BIST çöküşü ya da gram altın primi bu kontratta yerel bir fiyat sapması yaratmıyor. TL şoku günlerinde ortalama mutlak baz sapması 9,6 bps, normal günlerde 12,2 bps.
3. **Türkiye altın fiyatını (gram TL) öngörmenin işe yarayan tek parçası kur bileşeni.** Yönetilen kur döneminde (2023-06 sonrası) USDTRY spotunun sürüklenmesi geçmiş 20 günlük ortalamayla öngörülebiliyor. Rastgele yürüyüşe göre R² h=1'de %8, h=3'te %14, h=5'te %16. VİOP USDTRY vadeli fiyatı bu sürüklenmeyi fazlasıyla fiyatlıyor. Bu yüzden 2023-06'dan beri USDTRY vadelisinde **kısa** pozisyon yıllık ≈%10, 2025-03'ten beri ≈%16 kazandırdı (TL carry).
4. **USDTRY vadeli "sürüklenme − ima taşıma" sinyali** (t-1 bilgisiyle) USDTRY vadeli getirisini öngörüyor. IC t=4,35, IS t=3,2, OOS t=2,5, yılların 8/10'unda aynı işaret. ±1 kuralının 5 bps sonrası OOS Sharpe'ı 1,19 (demeaned 0,88). Ama bu bir **altın** sinyali değil. 2024–2026'daki kârın neredeyse tamamı sürekli kısa durmaktan, yani carry'den geliyor; o yıllarda yıl içi demeaned Sharpe ≈0 ya da negatif. Bir de 21.12.2021 KKM günü −%35'lik tek günlük kuyruk riski var. Güven: ORTA.
5. Gram altın vadelisinin sentetik primi (`tr_prem_matched`) güçlü biçimde ortalamaya dönüyor. Yarı ömür ≈1,4 gün (AR1) ile ≈3,9 gün (5 gecikmeli) arasında. Sapma, ileri prim değişimini h=5'te IC −0,18 (t −6,9) ile öngörüyor ve bu 10/10 yılda tutuyor. Ama 3 bacaklı (15 bps) göreli değer işlemi t-1 bilgisiyle **zarar** ediyor (OOS net Sharpe −0,77). Yalnız "kapanışta hesaplanan" sürüm net Sharpe 0,5 veriyor, uygulanabilirliği şüpheli. Prim fiziki Kapalıçarşı primi değil: vade sonunda LBMA PM × TCMB kuruna zorunlu olarak yakınsıyor.
6. Kur ve ons payları yıldan yıla çok değişiyor. Gram altın TL getirisinin varyansında kur payı 2018'de %91, 2021'de %94 idi. 2024'te %10'a, 2025'te %8'e, 2026'da ≈%0'a düştü. 2024'ten beri gram altını öngörmek fiilen ons altını öngörmek demek.
7. **Yöntem uyarısı (bütün proje için):** VİOP'ta 21 yarım gün var (bayram arifeleri ve 28 Ekim). Bu günlerde uzlaşma ~09:40 UTC'de oluşuyor. 15:00 UTC bilgisiyle kurulan her sinyal bu günlerde ileriye bakar. Örneğin xau 07→15 UTC momentumunun fwd1 ile korelasyonu yarım günlerde +0,55, normal günlerde +0,05. Tam örneklemdeki etkisi küçük (t'de +0,15–0,24), ama bu günler dışlanmalı ya da sinyal 09:30 UTC'de kesilmeli.

## 1. Veri, zaman kuralları ve bilgi zamanları

Hedef `fwd{h}` şöyle tanımlı: VİOP aktif kontratın t uzlaşmasından (~15:10 UTC) t+h uzlaşmasına log getirisi. Karar anı t günü 15:00 UTC.

| Öngörücü (kod adı) | Kaynak | Bilgi zamanı (UTC) | Not |
|---|---|---|---|
| `usd_fut_l1`, `usd_fut_5_l1` | VİOP USDTRY uzlaşma getirisi | t-1 15:10 | temiz |
| `usd_fut_K` | VİOP USDTRY, t | t 15:10 | **K = kapanışta hesaplanan** |
| `usd_spot_1`, `usd_spot_5`, `usd_intra` | Dukascopy USDTRY 15:00 / 07:00 | t 15:00 | 15:00 spot sürümü; placebo temiz |
| `itl_l1`, `ditl_5_l1` | ima TL faizi = ln(F_USDTRY/S)·365/dte + ABD 3a faizi | t-1 15:10 | |
| `xu_l1`, `xu_5_l1`, `xuusd_l1` | VİOP XU030 | t-1 15:10 | |
| `xu_K` | VİOP XU030, t | t 15:10 | K |
| `xu_intra_1430` | Yahoo saatlik XU030: t-1 kapanış → t 14:30 | t 14:30 | yalnız 2023-12+ |
| `prem_l1`, `dprem_l1`, `dprem5_l1`, `premz_l1` | `tr_prem_matched` | t-1 15:10 | |
| `prem`, `dprem_K`, `premz_K` | `tr_prem_matched`, t | t 15:10 | K |
| `gvolz_l1`, `goi_d1_l1`, `goi_d5_l1`, `gvol_ratio_z_l1` | VİOP XAUTRYM hacim/OI | t-1 | |
| `xbasis_dev_l1` / `xbasis_dev_K` | ln(v_settle/xau_p15) − taşıma (önceki 20 gün baz/dte medyanı × dte) | t-1 / t 15:10 | K |
| `y_XU030_IS`, `y_USDTRY_X` (erken dönem) | Yahoo kapanışları | t-1 | |

Kontroller (`a7_01_audit.py`, log `a7_01_audit.log`):
- VİOP USDTRY getirisi ile Dukascopy 15:00 değişiminin korelasyonu gecikme 0'da 0,957, ±1'de ≈0,03. Zaman damgası tutarlı. VİOP XAUUSD getirisi ile spot 15:00 getirisinin korelasyonu 0,977.
- Roll günü sayısı 60. Roll günü v_ret standart sapması 99 bps, diğer günler 100 bps (v_ret aynı kontrat içinde ölçülüyor). Sıfır hacimli gün yok (XAUUSD, XAUTRYM, USDTRY).
- Dukascopy USDTRY 2026-10-30'da bitiyor (32 eksik gün).
- `tr_prem_matched` 6 günde |%2|'yi aşıyor: 2018 Ağustos–Eylül ve 2022-05-27 (+%5,85, şüpheli). Prim testleri |prem|<2% filtresiyle de tekrarlandı.
- **Yarım günler (21):** Ramazan/Kurban arifeleri ve 28 Ekim. Takvim ve veriyle doğrulandı: uzlaşma 09:40 UTC spotuna yakın, 15:00'e uzak (ör. 2026-03-19'da sapma 09:40'a göre 26 bps, 15:00'e göre 235 bps). Liste `c5_half_days.csv`'de.
- **Yurt içi tatiller:** VİOP kapalıyken dünya açık olan 70 tatil sonrası ilk gün var (53 tek gün, 8 iki gün, 7 üç gün, 2 dört gün). Liste `c_post_holiday_days.csv`'de.

## 2. (a) XAUUSD'yi Türkiye bilgisiyle öngörme — `a7_02_predict_xau.py`, `a_ic_table.csv`

26 öngörücü × 3 ufuk = 78 test. IC Spearman, t Newey-West (lag = max(h,5)) ile hesaplandı. IS 2017-03..2021-12, OOS 2022-01..

| öngörücü | h | IC | t tam | t IS | t OOS | yıl aynı işaret |
|---|---|---|---|---|---|---|
| goi_d1_l1 (XAUTRY OI 1g Δ) | 3 | +0,047 | +2,11 | +0,38 | +2,62 | 6/10 |
| usd_fut_l1 (VİOP USDTRY t-1) | 3 | −0,042 | −2,08 | −1,56 | −1,45 | 8/10 |
| xu_intra_1430 (yalnız 2023-12+) | 3 | −0,071 | −2,02 | — | −2,02 | 3/3 |
| goi_d1_l1 | 1 | +0,038 | +1,97 | +1,25 | +1,74 | 8/10 |
| usd_spot_1 (USDTRY 15:00) | 1 | −0,034 | −1,75 | −0,12 | −2,12 | 7/10 |
| premz_l1 | 3 | +0,039 | +1,42 | +0,92 | +1,04 | 6/10 |
| diğer 72 test | | |t|<1,75 | | | | |

- 78 testin 3'ünde |t|≥2 var; şansla beklenen ≈4. Prim seviyesi, değişimi ve z'si (hem t-1 hem K), ima TL faizi, XU030 (TL ve USD bazlı), XAUTRY hacmi ve hacim oranı, VİOP baz sapması: hepsi |t|<1,8.
- **Dışlama testleri** (`a7_06_robust.py` R2):
  - `usd_fut_l1` h=3: TL kriz dönemleri (2018-08/09, 2021-11..2022-01) çıkınca t −1,34'e, roll pencereleri çıkınca −1,75'e iniyor.
  - `goi_d1_l1` h=3: roll çıkınca t +1,57, tatil/yarım gün çıkınca +1,64.
  - İkisi de kırılgan.
- **Erken dönem** (spot panel 2010–2016, Yahoo XU030/USDTRY t-1): bütün IC'ler |t|<1,5. `usdtry_1g` h=3: IC −0,014.
- **IS seçimli kurallar (R1):** IS |t|'ye göre en iyi 3 kombinasyon `ditl_5_l1` h5, `xuusd_l1` h3 ve `xu_l1` h1 çıktı. Bunların OOS IC'leri +0,007, −0,035 ve −0,021, yani hepsi çöktü. OOS net Sharpe 5 bps'te +0,16 / −0,34 / −0,94, 10 bps'te +0,04 / −0,55 / −1,30. Buy & hold OOS 0,53.
- Kapanışta hesaplanan (K) USDTRY ve XU030 getirisi (t 15:10) de öngörmüyor: |t|≤1,4.
- Kural backtest'i (`a7_07_claims.py`, C4): "dün USDTRY yükseldiyse 3 gün kısa ons" kuralı. OOS Sharpe 0,21, demeaned −0,01. Uzun bacak 0,41, kısa bacak −0,45. Kâr yalnız uzun bacakta (drift); kısa bacak para kaybediyor. **YOK / DÜŞÜK.**
- Kural C4b: "XAUTRY OI dün arttıysa 3 gün uzun, azaldıysa kısa". IS Sharpe −0,10, OOS 0,28 (demeaned 0,29). Kısa bacak OOS'ta −0,28. **DÜŞÜK.**

## 3. (b) Türkiye altın fiyatının yordanması — `a7_03_tr_gold.py`

### 3.1 Ayrıştırma (gram TL getirisi ≈ ons + kur + prim)
VİOP gram vadeli günlük getirisi = ons vadeli + USDTRY vadeli + kalıntı. Kalıntının standart sapması 24,8 bps ve Δprim ile korelasyonu 0,81. Kovaryans tabanlı varyans payları (toplam = %100) aşağıda; ayrıntı `b1_var_shares_futures.csv` ve `b1_var_shares_spot.csv`'de.

| dönem | h | ons % | kur % | prim % |
|---|---|---|---|---|
| 2017–2021 | 1 | 16,6 | 82,4 | 0,9 |
| 2022–2026 | 1 | 72,8 | 23,5 | 3,8 |
| 2023-06+ (yönetilen kur) | 1 | 87,8 | 10,8 | 1,4 |
| 2018 / 2021 | 1 | 6 / 6 | 91 / 94 | ≈2 / 0,5 |
| 2024 / 2025 / 2026 | 1 | 88 / 90 / 100 | 10 / 8 / 0 | 2 / 2 / 0 |

Yıllık getiri katkısı (spot, log %; `b1_annual_contrib.csv`):

| yıl | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (yılbaşından bugüne) |
|---|---|---|---|---|---|---|---|---|---|
| ons | −3,4 | 16,0 | 20,1 | −4,1 | −1,6 | 12,9 | 22,0 | 43,6 | −10,4 |
| kur | 33,4 | 11,3 | 21,8 | 56,5 | 34,4 | 45,1 | 18,8 | 17,4 | 14,8 |
| gram | 30,0 | 27,3 | 42,0 | 52,4 | 32,9 | 58,0 | 40,8 | 61,0 | 4,4 |

Gram altın yatırımcısının 2018–2023'teki TL kazancının çoğu kurdan geldi. 2024–2025'te ons baskın oldu. Kurun **getiriye** katkısı sürüyor (yıllık ≈%15–19). Ama oynaklığa katkısı artık çok küçük.

### 3.2 USDTRY sürüklenmesi (yönetilen kur) — `b2_fx_drift_forecast.csv`
Hedef: USDTRY spotunun (15:00 UTC) h günlük log değişimi. Tablodaki değerler rastgele yürüyüşe göre R² (%).

| dönem | model | h=1 | h=3 | h=5 |
|---|---|---|---|---|
| 2017-03..2023-05 | geçmiş 20g sürüklenme | −4,3 | −11,4 | −18,1 |
| 2017-03..2023-05 | VİOP bazı (t-1) | +0,2 | +1,3 | +2,2 |
| 2023-06+ | geçmiş 20g sürüklenme | +8,0 | +14,3 | +15,6 |
| 2023-06+ | VİOP bazı (t-1) | +1,5 | +11,6 | +15,4 |
| 2025-04+ | geçmiş 60g sürüklenme | +31,5 | +71,1 | +85,5 |
| 2025-04+ | VİOP bazı (t-1) | −50,8 | +13,3 | +30,0 |

- Serbest kur döneminde geçmiş sürüklenme işe yaramıyor, hatta zarar veriyor. Yönetilen dönemde güçlü.
- VİOP bazından ima edilen kayma 2025-04'ten beri gerçekleşeni sistematik olarak aşıyor. 5 günde tahmin 56 bps, gerçekleşen 35 bps. Bu fark TL carry primi.
- IC (yalnız 2023-06+, n≈750): `fx_trail20` h=1/3/5 için +0,12 / +0,17 / +0,21, t +2,6 / +2,6 / +2,7.
- **USDTRY vadeli ortalama getirisi (uzun):** 2017–2021 yıllık +%11,9 (oynaklık %26). 2023-06+ yıllık −%10,4 (oynaklık %7,1; kısanın Sharpe'ı 1,48). 2025-03+ yıllık −%15,7 (oynaklık %4,2; kısanın Sharpe'ı 3,71). Bu dönemde en kötü gün +%4,2 (2025-03-19).

### 3.3 Carry zamanlaması (USDTRY vadeli hedefi) — `a7_06_robust.py` R6, `a7_07_claims.py` C1
Kural: `sig = ort(Δln USDTRY_15:00, son 20 gün, t-1'e kadar) − 1,4 × ln(F_USDTRY,t-1 / S_t-1) / dte_t-1`. Uzlaşmada `pos = sign(sig)` alınır, 1 gün tutulur.

- IC h=1/3/5: +0,114 / +0,149 / +0,179, t tam 4,35 / 4,08 / 4,14. IS t 3,2 / 3,0 / 2,9; OOS t 2,5 / 2,6 / 2,2. Yıllar 8/10, 10/10, 9/10.
- Dışlamalar (h=1): TL krizleri hariç IC 0,10 (t 4,0); uç dönemler hariç t 4,0; USDTRY roll pencereleri hariç t 3,5; yalnız 2017–2021 t 3,2; yalnız 2023-06+ t 3,2.
- Placebo: kaydırmayla yavaş azalan profil (0,114 → 0,096). Kalıcı bir rejim sinyaline uyuyor, sızıntı izi yok.
- Backtest (h=1): tam Sharpe 0,90 (demeaned 0,92), IS 0,88, OOS 1,19 (demeaned 0,88). 10 bps'te OOS 1,08. Uzun bacak OOS 0,50, kısa bacak OOS 1,18. Buy & hold (uzun USDTRY) 0,14. Pozisyon yılda ≈20 kez değişiyor. Yıllık Sharpe 10/10 yıl pozitif.
- **Uyarılar:**
  1. 2024–2026'da pozisyon zamanın %89–92'sinde kısa. Yıl içi demeaned Sharpe 2024'te 0,11, 2025'te −0,60, 2026'da −1,64. Yani bu yıllardaki kâr carry'den geliyor; zamanlamanın katkısı yok. Zamanlamanın gerçek katkısı 2018, 2021–2023 rejim geçişlerinde.
  2. 21.12.2021'de (KKM) sinyal uzundu ve tek günde −%35 kaybettirdi. KKM haftası hariç Sharpe 1,2.
  3. Bileşenler ayrı ayrı: sürüklenme tek başına IS'te çalışıyor (t 3,2), OOS'ta çalışmıyor (0,8). −taşıma tek başına OOS'ta çalışıyor (2,8), IS'te çalışmıyor (0,7).
  4. Bu sinyal ons altını öngörmüyor: XAUUSD fwd1/3/5 için t −0,8 / −0,6 / −1,2.
- Güven: ORTA. Biçimsel YÜKSEK eşikleri sağlanıyor, ama rejim bağımlılığı ve kuyruk riski yüzünden bir kademe düşürüldü.

### 3.4 Gram altın primi — ortalamaya dönüş — `b3_prem_ar.csv`
`tr_prem_matched`'in tam dönem ortalaması 11,7 bps, standart sapması 27,8 bps. Yıllık ortalamalar: 2018'de 21 bps, 2022'de 32, 2024'te −6, 2025–2026'da ≈2 bps.

| | φ1 | yarı ömür (gün) | φ (5 gecikmeden) | yarı ömür (gün) |
|---|---|---|---|---|
| tam | 0,61 | 1,4 | 0,84 | 3,9 |
| IS | 0,72 | 2,1 | 0,85 | 4,4 |
| OOS | 0,50 | 1,0 | 0,81 | 3,3 |
| |prem|<2% | 0,68 | 1,8 | 0,86 | 4,5 |

- t-1 sapması (prem − 60g ortalama) ileri Δprim'i öngörüyor. h=1/3/5 için IC −0,07 / −0,15 / −0,18, t −3,7 / −6,1 / −6,9. IS ve OOS aynı işaret, 10/10 yıl. Global FDR sonrası da anlamlı (q<0,01).
- **Hangi bacak düzeltiyor:** gram, ons ve USDTRY bacaklarının her birinde t<0,7. Düzeltme gürültü içinde dağılıyor.
- **Mekanizma:** VİOP gram altının vade sonu uzlaşması LBMA PM × TCMB kuru ÷ 31,1035 (r1_viop_kontrat, Prosedür Ek-1 Q). Prim vade sonunda yakınsamak zorunda; arbitraj da onu sınırlıyor. **Bu, fiziki (Kapalıçarşı) primi değil.** Metals Focus'un 2023–2024 için bildirdiği 20–50 $/ons'luk fiziki prim bu veride yok.
- **İşlem:** 3 bacak, 15 bps.

| sürüm | k | h | brüt Sharpe | net Sharpe | OOS net Sharpe |
|---|---|---|---|---|---|
| t-1 (temiz) | z>1 | 3 | 0,85 | −0,76 | −0,77 |
| K (z_t, kapanışta) | z>1 | 3 | 2,09 | 0,51 | 0,53 |
| K | z>2 | 5 | 0,94 | 0,59 | 0,79 (maruziyet %5) |

  Kârlılık neredeyse tamamen ilk günkü (t→t+1) dönüşten geliyor. Üç bacağın uzlaşma VWAP'ında aynı anda işlem yapılmasını ve sinyalin o anda bilinmesini varsayıyor. Uygulanabilirlik şüpheli. **DÜŞÜK.**

### 3.5 Gram vadeli tahmin modeli — `b4_gram_model.csv`
Model: ons = 0 + kur vadeli beklenen getiri (geçmiş sürüklenme − ima taşıma, t-1) + prim dönüşü (katsayı IS'te). Kıyas 0, yani ons×kur rastgele yürüyüş.

- IS IC 0,10–0,16 (t ≈3). OOS IC 0,02–0,04 (t<1).
- OOS R² 0'a göre: prim bileşeni −0,08..+0,01 %, kur bileşeni −0,3..−6,7 %.
- **Rastgele yürüyüşe katkı yok.** Sebep: 2022'den beri gram vadeli varyansının %73–100'ü ons'tan geliyor. Kur bileşeninin öngörülebilir kısmı vadeli fiyata zaten gömülü.
- Spot gram altında (fiziki/banka) kur sürüklenmesi 2023-06+ döneminde R²'yi h=1/3/5 için %1,4 / %3,9 / %5,8 artırıyor. 2023-05 öncesinde negatif (`a7_03_tr_gold.log` B6).

## 4. (c) Yurt içi tatiller ve yarım günler — `a7_04_holidays.py`

- **Tatil sonrası ilk gün:** VİOP getirisi tatil boyunca spot hareketini yansıtıyor. Beta 1,04, R² 0,915; normal günde 0,98 ve 0,962. İzleme farkının standart sapması 43 bps, normal günde 19 bps. Baz sapması ortalama −7 bps (normal +0,5).
- **Pozisyon riski:** tatili kapsayan getirinin standart sapması 1 günlük tatilde 141 bps, 2 günlük tatilde 168 bps. Bu √(k+1) beklentisine uyuyor (139 ve 170). |getiri|>%2 olasılığı %13, normal günde %5. Tatile pozisyonla girmek 2–3 günlük risk taşımak demek.
- **Ortalama getiri yok:** tatil boyunca uzun pozisyonun drift-düzeltilmiş fazla getirisi −18 bps (t −1,06, n=70). Tatil öncesi son günün fazla getirisi −7 bps (t −0,66). Fabozzi tipi tatil etkisi bulunamadı.
- **Tatil hareketinden sonra:** h=5'te dönüş eğilimi var: b −0,30, t −2,24, Spearman −0,19 (p 0,11), n=70. "Tatil hareketinin tersine 5 gün" kuralının Sharpe'ı tam dönemde 0,00, IS'te −0,23, OOS'ta +0,20. **YOK.**
- **Yarım günler:** bkz. §0 madde 7. Uzlaşma 09:40 UTC'de. Yarım günden sonraki gün (tatil sonrası) getirisinin standart sapması 197 bps.

## 5. (d) Yurt içi kriz günleri — `a7_05_crisis.py`, `d1_event_table.csv`

| olay | gün | USDTRY 1g % | XU030 % | ons baz sapması bps | prim bps | prim 5g Δ bps | fwd1 % | fwd3 % | fwd5 % |
|---|---|---|---|---|---|---|---|---|---|
| TL krizi (Brunson) | 2018-08-10 | +14,8 | −2,8 | −8 | 23 | +168 | −1,62 | −3,01 | −3,11 |
| TCMB başkanı görevden alındı | 2021-03-22 | +9,0 | −10,5 | −17 | 9 | −8 | −0,44 | +0,09 | −1,39 |
| TL çöküşü | 2021-11-23 | +11,9 | +1,7 | −10 | 5 | −2 | −0,48 | +0,66 | +1,00 |
| KKM dönüşü | 2021-12-21 | −35,4 | −10,5 | −4 | 1 | +9 | +0,06 | +1,00 | +1,29 |
| Deprem | 2023-02-07 | 0,0 | −7,4 | −14 | 29 | −9 | +0,15 | −0,34 | −0,44 |
| İthalat kotası / prim | 2023-03-01 | 0,0 | +1,8 | +16 | 39 | −24 | −0,23 | +0,42 | −1,22 |
| Seçim | 2023-05-15 | +0,3 | −10,5 | +16 | 37 | −15 | −0,92 | −3,14 | −2,52 |
| Seçim sonrası devalüasyon | 2023-06-07 | +7,5 | +4,2 | +10 | 60 | −16 | +0,53 | −0,16 | −0,28 |
| İmamoğlu gözaltısı | 2025-03-19 | +3,3 | −10,5 | +9 | 4 | +10 | +0,24 | −0,89 | −0,64 |
| XU030 −%7,6 | 2026-09-16 | 0,0 | −7,6 | −5 | −1 | +1 | −0,01 | −0,17 | −1,44 |

- Olay günü ons baz sapmaları 4–17 bps; normal günlerde mutlak sapmanın medyanı 7,8 bps. **Yurt içi krizler VİOP ons altında belirgin bir yerel prim ya da iskonto yaratmıyor.** Yerel talep gram altın primine yansıyor (2018 Ağustos'ta 5 günde +168 bps).
- 10 olayın fwd1/3/5 ortalaması −0,27 / −0,55 / −0,87 %. Koşulsuz ortalama +0,03 / +0,09 / +0,16 %.
- **Sistematik tanım:** t günü 15:00'te |USDTRY 1g| > %2,5 ya da t-1 VİOP XU030 < −%5 (81 gün). h=3'te fazla getiri −48 bps, naif t −2,73. Ama olaylar kümeleniyor. 32 epizoda indirgeyince t −1,55 (h=3) ve −1,46 (h=5), negatif epizot oranı %56–59.
- Erken dönem (2010–2016, Yahoo TL şoku, n=11): h=3'te +36 bps, yani **ters işaret**.
- Kural "şok gününde kısa, 3 gün": Sharpe 0,5, demeaned 0,63, ama maruziyet yalnız %3 (t 1,54).
- Olası açıklama: Türkiye krizlerinin bir kısmı küresel dolar güçlenmesiyle çakıştı (2018 Ağustos EM krizi, 2021 Kasım Fed dönüşü). Yerel bir kanal görünmüyor. **DÜŞÜK.**
- Kriz penceresinde baz sapmasının (t-1) öngörü gücü: h=3'te IC +0,086, t 1,84. Anlamsız.

## 6. Sağlamlık özeti
- **Roll:** v_ret kontrat içi ölçüldüğü için roll sıçraması yok. Roll penceresi dışlaması aday ilişkileri zayıflattı: `goi_d1_l1` t 2,1'den 1,6'ya, `usd_fut_l1` −2,1'den −1,75'e.
- **Sıfır hacim:** yok. v_ret=0 olan 7 gün var, etkisiz.
- **Uç dönemler** (2020-03..04, 2026-01..02): dışlansalar da sonuçlar değişmiyor (R2 tablosu).
- **Yarım günler / tatiller:** dışlanınca `goi_d1_l1` h1 t 1,97'den 0,79'a düşüyor. Bu ilişki kısmen tatil ve yarım gün artefaktı.
- **Maliyet:** temel 5 bps, stres 10 bps; prim RV için 3 bacak 15 bps.
- **Erken dönem:** Türkiye değişkenleri için 2010–2016'da da ilişki yok.

## 7. NEGATİF bulgular (test edildi, tutmadı)
- USDTRY vadeli/spot getirisi (t-1, 5 günlük, 15:00 spot, gün içi 07→15, K) → XAUUSD: yok. En iyisi h=3'te t −2,08; kırılgan, erken dönemde yok.
- İma TL faizi seviyesi ve 5 günlük değişimi → XAUUSD: yok. IS'te t −2,5 olan sürüm OOS'ta çöktü (+0,16).
- XU030 (TL, USD bazlı, 5 günlük, K) → XAUUSD: yok. IS'te +2 çıkan sürümler OOS'ta ters işaret aldı.
- XU030 gün içi (t-1 kapanış → t 14:30, 2023-12+): h=3'te t −2,0. Tek dönem, IS yok. DÜŞÜK / YOK.
- Gram altın primi (seviye, Δ, 5g Δ, z; t-1 ve K) → XAUUSD: yok (|t|<1,5).
- XAUTRY hacim z'si, hacim oranı, OI 5g değişimi → XAUUSD: yok. OI 1g değişimi h=3'te t 2,1, ama IS'te t 0,4 ve roll ile tatil dışlanınca kayboluyor.
- VİOP XAUUSD baz sapması (t-1 ve K) → fwd: yok (t≤1,3).
- Tatil öncesi / tatil boyunca uzun pozisyon getirisi: yok. Tatil hareketine karşı işlem: yok.
- Kriz/şok günleri sonrası kısa ons: epizot kümeli t −1,5; erken dönem ters işaret.
- Prim RV (t-1, 15 bps): zarar.
- Gram vadeli tahmin modeli (ons 0 + kur + prim): OOS'ta rastgele yürüyüşe katkısı yok.
- USDTRY carry sinyali → ons altın: yok.

## 8. Pratik çıkarımlar (1-3-5 günlük F_XAUUSD işlemcisi için)
1. F_XAUUSD'nin yönünü küresel değişkenlerle tahmin edin (diğer ajanların aileleri). Türkiye verisi bu kontratın yönüne bilgi katmıyor.
2. Türkiye'ye özgü **riskler** gerçek, ama yönsüz. Tatil öncesi pozisyon 2–3 günlük oynaklık taşır; >%2 hareket olasılığı 2,6 kat. Yarım günlerde uzlaşma 09:40 UTC'dedir. 1/3/5 günü VİOP iş günü olarak sayın.
3. Gram altın vadelisi alan biri, ons vadeli + USDTRY vadeli uzun pozisyonu alıyor demektir. 2023-06'dan beri USDTRY vadeli uzun bacak yıllık ≈−%10 getirdi. TL bazında altın pozisyonu isteyen için ons vadeli ile gram vadeli arasındaki seçim, bu carry'yi ödeyip ödememek demek.
4. "Milletin para kazandığı" Türkiye'ye özgü kanallar şunlar:
   - (i) TL carry: USDTRY vadeli kısa; 2023-06+ Sharpe ≈1,5, ama nadir ve büyük sıçrama riski var.
   - (ii) Gram altında kur sürüklenmesinden gelen TL getirisi (2018–2023'te gram getirisinin çoğu).
   - (iii) Fiziki prim, ithalat kotası ve arbitraj: kurumsal bir kanal; VİOP verisiyle ölçülemez.
   Bunların hiçbiri ons altının 1–5 günlük yönünü öngörmüyor.

## 9. Dosyalar
- Kod: `a7_common.py` (öngörücüler, yarım gün ve tatil tespiti), `a7_01_audit.py`, `a7_02_predict_xau.py`, `a7_03_tr_gold.py`, `a7_04_holidays.py`, `a7_05_crisis.py`, `a7_06_robust.py`, `a7_07_claims.py`, `a7_08_fdr.py`, `run_all.sh`.
- Çıktılar: `a_ic_table.csv`, `b1_*.csv`, `b2_fx_drift_forecast.csv`, `b3_prem_ar.csv`, `b4_gram_model.csv`, `c1_post_holiday_tracking.csv`, `c5_half_days.csv`, `c_post_holiday_days.csv`, `d1_event_table.csv`, `claims_bt.json`, `registry_with_fdr.csv`, `*.log`, `features.parquet`.
