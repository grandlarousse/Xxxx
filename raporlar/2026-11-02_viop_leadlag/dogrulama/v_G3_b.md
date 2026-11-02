# v_G3_b — 2. aşama çürütme: G3 (XU030 gece pozitif / gün-içi negatif, "açılışta sat, kapanışta kapat")
Tarih: 02.11.2026 · Doğrulayıcı: v_G3_b. `ll.py` ve `code_v_G3_a` import edilmedi. Yükleme, temizlik ve VİOP ayrıştırması kendi kodumda: `out/code_v_G3_b/bc.py`.
**Yeni veri kaynağı:** İş Yatırım saatlik endeks serisi (`data/isy/h1`, 2015–2026). Bu seri 1. aşamada kullanılmadı ve 2023 öncesinin saatlik ayrıştırmasını ilk kez mümkün kılıyor.
Etiket anlamını doğruladım: "HH:00" etiketi saatin son fiyatı, yani (HH+1):00 UTC anındaki değer. Yahoo m5 ile 30 günün %97–100'ünde birebir aynı. Her yılda değerlerin %100'ü Yahoo günlük [düşük, yüksek] aralığında.

## 0. Hüküm: DÜZELT · güven ORTA (düzeltilmiş "öğleden sonra düşüşü" ve vadeliyle 11:00 kısa işlemi); iddianın harfiyen hâli ("vadeliyle açılışta sat") DÜŞÜK–ORTA

**Özet:**
1. **Spot olgu sağlam.** Gap 13/13 yıl pozitif. Gün-içi XU030'da 10/13, XU100'de 11/13 yıl negatif.
2. **Açılış artefaktı değil.** 2017–2022'de açılış→11:00 arası spot **yükseliyor**: +4,1 bps (t 2,6). Açılışın gap'e göre geri dönüşü yok (eğim ≈ 0). Negatif kayma sürekli seansta, **11:00→kapanış** arasında: −11,2 bps/gün (t 4,7), 2015–2026'da 12 yılın 11'inde negatif.
3. **v_G3_a'nın VİOP sonucu 2017–2022 için GEÇERSİZ.** Bültendeki ACILIS FIYATI, açılış seansı başlamadan önce (2022 sonu) **bayat bir ilk baskı**: gece bilgisinin ancak %13–25'ini içeriyor. Dolayısıyla "spot–vadeli farkı +10,4 bps (t 6) = spot açılış müzayedesi aşırılığı" yorumu yanlış. Fark, vadeli açılışının bayatlığından kaynaklanıyor. Bayatlığın önemsiz olduğu küçük-gap günlerinde vadeli ile spot gün-içi aynı.
4. **Vadeli, spotun 11:00 sonrası hareketini birebir izliyor** (β 1,05; sabit −1,8 bps). Bu yüzden desenin işlenebilir hâli "XU030 vadelisini ~11:00'da sat, 18:10'da kapat". Spot vekili: 2017–2026 brüt +11,1 bps (t 4,2); OOS 2021–2026 +11,5 (t 3,1). 2 bps sonrası +9,1 (SR 1,1), 4 bps sonrası +7,1 (SR 0,86), 8 bps sonrası +3,1.
   - Uyarılar: Vadelinin 2017–2022'deki gün-içi fiyatı doğrudan gözlenmedi; sonuç regresyon kanıtına dayanıyor. 11:00 girişi bu analizde ortaya çıktı, önceden belirlenmedi (ama 11:00–17:00 arasındaki tüm girişler benzer sonuç veriyor). Son 250 gün zayıf: +5,0 (t 0,7).

## 1. İddianın parçaları

| Alt iddia | Benim sonucum | Durum |
|---|---|---|
| XU030 gap 13/13 yıl > 0 | 13/13 (+9,3…+28,6 bps/gün) | DOĞRU |
| Gün-içi 11/13 yıl < 0 | XU030 10/13 (2017 +1,4, 2021 +3,4, 2022 +14,3); XU100 11/13 | Kırılgan (2021 ≈ 0) |
| Aç-sat brüt +11 (t 2,2) | 2014–2026 +7,9 (t 3,06; NW 3,12; medyan +9,3); IS 2014–2020 +10,4 (t 3,45); **OOS 2021–2026 +4,9 (t 1,10)**; +11,1 (t 2,06) yalnız 2023-12..2026-10 | Dönem yanlış etiketlenmiş |
| 8 bps sonrası +3 | Yalnız h1 penceresinde | — |
| Endeks vadelisiyle 2–4 bps'de anlamlı | Açılıştan giriş 2023–2026: +11,3 (t 2,0), 2/4 bps sonrası +9,3/+7,3 (SR 0,83/0,65). 2017–2022 **test edilemez** (bayat ACILIS). **11:00 girişli vadeli (spot vekili) 2017–2026 +11,1 (t 4,2)** | Değiştirilmiş hâli daha güçlü |
| 47 hisse gap > 0 / gün-içi < 0 | Doğru ama tek bir piyasa faktörü. Etkin bağımsız sayı ≈ 2,9. Piyasa artığı medyanı −1,4 bps; t<−2 10/47, t>+2 2/47 | Ayrı kanıt değil |

## 2. Çürütme testleri

### 2.1 Açılış fiyatı gerçekçiliği / artefakt (İş Yatırım saatlik, XU030, bps/gün, kısa yönlü, parantezde t)

| Dönem | Aç-sat | Açılış→11:00 | 11:00→kapanış | 11:00→18:00 | 18:00→kapanış (müzayede) |
|---|---|---|---|---|---|
| 2015–2016 | +11,9 (2,2) | −1,0 (−0,6) | +12,9 (2,5) | +12,9 | +0,1 |
| 2017–2022 | +4,6 (1,3) | **−4,1 (−2,6)** | **+8,7 (2,7)** | +7,6 | +1,1 (3,2) |
| 2021–2022 | −9,0 (−1,2) | **−16,0 (−4,8)** | +7,0 (1,1) | +6,3 | +0,6 |
| 2023–2026 | +12,0 (2,2) | −2,3 (−1,0) | **+14,3 (3,0)** | +14,5 | +0,7 |
| 2015–2026 | +8,2 (3,0) | −3,0 (−2,6) | **+11,2 (4,7)** | +10,7 | +0,8 (3,5) |

- Açılış müzayedesinin gap'e aşırı tepkisi yok: s(açılış→11) ~ s_gap eğimi yıllara göre −0,24…+0,18. Sadece 2018'de anlamlı negatif.
- 2021–2022'de "aç-sat"ı bozan şey sabah rallisi (açılış→11:00 yükselişi 2021'de +8,7, 2022'de +22,8). Öğleden sonra düşüşü o yıllarda da sürdü (+5,3 / +8,5).
- Saat ızgarası, 2017–2026 kısa (`res/s4_grid.log`):
  - 11:00, 12:00, 13:00 ve 14:00 girişlerinden kapanışa +10,4…+10,9 (t 3,8–4,6).
  - 15:00, 16:00 ve 17:00 girişlerinden +5,9…+7,6.
  - En güçlü tek saat 17→18: +5,0 (t 4,1).
  - Seçilmiş tek bir hücre değil; 11:00 sonrası tüm girişlerde aynı işaret.
- Diğer endeksler (11→kapanış kısa, 2016-11+):
  - XU100: +11,7 (t 4,7), 10/11 yıl.
  - XBANK: +15,2 (t 4,1), 11/11 yıl.
  - XUSIN: +11,9 (t 4,8), 10/11 yıl. Yani yalnız bankalarda değil.

### 2.2 VİOP ACILIS bayatlığı (kendi ayrıştırmam: 2.422 bülten, 2.392 ortak gün)

| Yıl | f_gapc~s_gap eğimi | ACILIS = önceki kapanış (tam) | ±1 tik içinde | Medyan \|f_gapc\| / \|s_gap\| (bps) | \|s_gap\|>%1 günlerinde ACILIS gün dibi/tepesi: vadeli / spot | β(S&P_{T−1}): f_gapc / s_gap |
|---|---|---|---|---|---|---|
| 2017 | 0,13 | %12 | %28 | 7 / 27 | %67 / %0 | 0,04 / 0,22 |
| 2018 | 0,22 | %7 | %13 | 13 / 36 | %45 / %18 | 0,05 / 0,19 |
| 2019 | 0,15 | %13 | %25 | 8 / 29 | %71 / %18 | 0,03 / 0,11 |
| 2020 | ~0,25* | %2 | %6 | 14 / 39 | %51 / %10 | — |
| 2021 | 0,25 | %3 | %9 | 14 / 27 | %14 / %19 | 0,09 / 0,10 |
| 2022 | 0,41 | %1 | %3 | 20 / 38 | %30 / %7 | 0,09 / 0,13 |
| 2023 | 0,66 | %2 | %5 | 26 / 35 | %14 / %17 | 0,15 / 0,22 |
| 2025 | 0,78 | %4 | %6 | 21 / 30 | %4 / %9 | 0,26 / 0,22 |
| 2026 | 0,84 | %1 | %2 | 29 / 33 | %6 / %6 | 0,28 / 0,19 |

\* 2020'de endeks bölünme günü dışlanmış çeyreklik ortalama: 0,23–0,27.

- Açılış seansı fiyatı alanı 2022'de günlerin %28'inde, 2023+ %100 dolu. Dolu günlerde ACILIS = açılış seansı fiyatı (%100).
- **Regresyon (2017–2022):** f_gün-içi = −1,8 bps (t −1,5) + 0,72·s_gap + 0,93·s(açılış→11) + 1,05·s(11→kapanış). Yani vadeli, spot gap'in %72'sini açılışından sonra fiyatlıyor ve 11:00 sonrası spot hareketini birebir izliyor.
- **2023–2026:** sabit −5,1 (t −3,1), gap katsayısı 0,32. Vadeli gün-içi, spot ile açıklanandan ~5 bps düşük; muhtemelen gün-içi taşıma (baz) erimesi. Bu fark kısa pozisyonun lehine.
- **Küçük-gap plasebosu** (|s_gap|<%0,25; bayatlık önemsiz):
  - 2017–2022: vadeli aç-sat +2,8, spot +2,3, fark −0,5 (t −0,3).
  - 2023–2026: +23,1 / +18,7.
  - v_G3_a'nın "+10,4 bps fark" bulgusu bayatlığın gap ile orantılı ortalamasıdır. Spot açılış artefaktı değildir.
- **Sonuçlar:**
  - v_G3_a'nın "vadeli aç-sat 2017–2026 +1,0 bps (t 0,3)" sonucu 2017–2022 için geçersiz. Vadeli gece getirisi (+5,1) ve buna dayalı carry ayrıştırması da 2017–2022'de çarpık (gece düşük ölçülmüş).
  - SSF'lerde (pay vadelileri) de aynı sorun var: 2017–2022 medyan eğim 0,44; |gap|>%2 günlerinde ACILIS %27 gün dibi/tepesi. Bu yüzden "SSF'de gün-içi<0 sadece 29/47" sonucu da kirli. Küçük-gap günlerinde SSF aç-sat medyanı +5,3 (vadeli), spotta +2,4.

### 2.3 Uç değer bağımlılığı

| Test | Aç-sat (XU030, 2014–2026) | 11→kapanış kısa (2017–2026) |
|---|---|---|
| Ortalama / medyan | +7,9 / +9,3 | +10,9 / +10,3 |
| En iyi 20 gün çıkarılınca | +3,9 (t 1,6) | +6,3 (t 2,5) |
| En iyi 50 gün (%2) çıkarılınca | +0,0 | +2,1 (t 0,9) |
| Simetrik 50/50 kırpma | +6,8 (t 3,1) | +10,1 (t 4,7) |
| Winsor %2,5 | +6,8 (t 3,0) | +10,0 (t 4,3) |
| Yıl-blok bootstrap %95 GA | [+2,4, +13,0] | [+6,1, +15,2] |

- Getiri sağa çarpık: kısa pozisyon çöküş günlerinde çok kazanıyor, en iyi %1'lik günler toplamın %70'i.
- Ama merkez eğilimi de pozitif: medyan ≈ ortalama, simetrik kırpma sağlam. Ortalamanın uç günlere bağımlı olduğu doğru, deseni sadece uç günlerin yarattığı doğru değil.

### 2.4 Alt dönem istikrarı / rejim
- 11→kapanış kısa, yıllık (bps/gün):

  | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  | +21,7 | +4,0 | −1,2 | +13,8 | +7,6 | +18,0 | +5,3 | +8,5 | +25,8 | +15,5 | +11,5 | +2,6 |

  - 250 günlük kayan ortalama günlerin %97'sinde > 0.
  - Son 250 gün +5,0 (t 0,7): 2026 Ocak–Ağustos ≈ 0, Eylül–Ekim +11,8. **Zayıflama işareti var.**
- **Rejim değişkeni:** vadeli bazından ima edilen TL taşıması.
  - 11→kapanış kısa taşıma tercillerine göre 11,6 / 10,6 / 10,7. Aylık eğim 0,05 (t 0,3). Desen faiz rejimiyle açıklanmıyor.
  - Rejime bağlı olan sabah saati: yüksek taşımada ilk saat kısa −7,1.
- Haftanın günü (11→kapanış): Salı +19, Çarşamba +20, Perşembe +12, Pazartesi 0, Cuma +2,5 (post-hoc, yorumlanmadı). Aç-sat'ta ay son iş günü +26,6 (n 154).
- Gap koşulu (aç-sat, 2014–2026): etkinin tamamı |gap|<%0,5 günlerinde: 0…+%0,5 aralığında +14,8 (t 4,4). |gap|>%0,5 günlerinde −4…+1.

### 2.5 Plasebo / dış geçerlilik (aynı Yahoo o/c ayrıştırması, 2014–2026, bayat açılışsız 27 yabancı endeks)
- Aç-sat t>2 sadece 4 endekste: BSESN +8,9 (t 5,9), NSEI +6,4, KS11 +4,6, HSI +4,7. Ayrıca JKSE (açılışı %10 bayat). t<−2 olan yok; medyan 0,0.
- Genel bir Yahoo açılış artefaktı değil. Bazı gelişen piyasalarda (Hindistan, Kore, HK) ve TR'de görülen bir olgu; literatürdeki "gece–gündüz / tug of war" desenine uygun.
- İşaret permütasyonu (11→kapanış): p < 0,0002.

### 2.6 Ortak faktör / seçim yanlılığı
- 47 hissenin gün-içi getirileri arasındaki ortalama ikili korelasyon 0,33. Etkin bağımsız sayı ≈ 2,9; "45/47 negatif" sayımı 47 ayrı kanıt değil.
- Piyasa artığı (gün-içi − β·XU030 gün-içi; medyan β 0,80): medyan −1,4 bps; t<−2 10/47, t>+2 2/47. EW47 − XU030: −1,3 (t −1,2).
- Seçim: iddia r1_gunici'deki 8 backtestten biri (BT5). XU030 için tek, doğal bir hipotez. 11:00 girişi bu doğrulamada ortaya çıktı, ama 45 hücrelik ızgarada 11:00 sonrası girişlerin hepsi aynı işaretli ve benzer büyüklükte.

### 2.7 Likidite / maliyet
- F_XU030 günlük medyan işlem sayısı 27 bin (2017) → 96 bin (2026); hacim 1,9 → 43 milyar TL. 11:00'da sürekli seansta küçük–orta pozisyon için sorun yok.
- Açılış seansı medyanı 28–58 işlem, 4–29 milyon TL. Açılıştan dolum küçük boyut için mümkün.
- Fiyat adımı:
  - 2017–2020: 0,025 (≈2 bps)
  - 2021: 0,25 (1,6 bps)
  - 2022: 0,9 bps
  - 2023–2024: 0,2–0,35 bps
  - 2025–2026: 1 puan (0,6–0,8 bps)
- 2017–2020'de 1 tik ≈ 2 bps olduğu için 2 bps toplam maliyet o yıllar için iyimser; 3–4 bps daha gerçekçi.
- ln(KAPANIS/UZLAŞMA) ortalaması +0,5 bps: uzlaşma fiyatıyla çıkış aynı sonucu verir.

| Strateji (bps/gün) | Brüt (t) | 2 bps | 4 bps | 8 bps |
|---|---|---|---|---|
| Vadeli 11:00 kısa → kapanış (spot vekili), 2017–2026 | 11,1 (4,2) | 9,1 (SR 1,10) | 7,1 (0,86) | 3,1 (0,38) |
| Aynı, OOS 2021–2026 | 11,5 (3,1) | 9,5 (1,07) | 7,5 (0,84) | 3,5 (0,39) |
| Aynı, 2023–2026 | 14,9 (3,2) | 12,9 (1,43) | 10,9 (1,21) | 6,9 (0,77) |
| Vadeli açılış seansında sat → kapanış, 2023–2026 (doğrudan) | 11,3 (2,0) | 9,3 (0,83) | 7,3 (0,65) | 3,3 (0,29) |

- SSF (8–15 bps): tek hisse bazında anlamlı bir net getiri kalmıyor; desen zaten piyasa faktörü. Endeks vadelisi doğru enstrüman.

## 3. Düzeltilmiş iddia
1. **Gece:** Spot XU030 gece (önceki kapanış → açılış) getirisi 2014–2026'da 13/13 yıl pozitif.
2. **Gün-içi:** Açılış→kapanış XU030'da 10/13, XU100'de 11/13 yıl negatif.
3. **Negatif kaymanın yeri:** Açılış müzayedesi değil, sürekli seans. 11:00→kapanış arası −11,2 bps/gün (t 4,7), 2015–2026'da 11/12 yıl; en güçlü tek saat 17→18. Açılış→11:00 arasında ise 2017–2022'de ortalama yükseliş var; 2021–2022'de bu yükseliş güçlü (KKM dönemi sabah rallisi) ve "açılışta sat"ı bozan şey bu.
4. **Spot "açılışta sat":** 2014–2026 +7,9 bps (t 3,1), OOS 2021–2026 +4,9 (t 1,1). "+11 (t 2,2)" rakamı yalnız 2023-12..2026-10 penceresine ait.
5. **İşlenebilir hâli:** XU030 vadelisi ~11:00'da açılan kısa pozisyon, 18:10'da kapanır. Spot vekili 2017–2026 +11,1 bps (t 4,2), IS +9,5 (t 2,7), OOS +11,8 (t 3,1). 2–4 bps sonrası +7…+9 (SR 0,9–1,1).
6. **Vadeli verisiyle doğrudan test:** Yalnız 2023+ mümkün (açılış seansı fiyatı): aç-sat +11,3 (t 2,0). 2017–2022 bülten ACILIS'i bayat olduğu için test edilemez.
7. **Faiz rejimi:** Desen faiz rejiminden bağımsız. Son 12 ay zayıf (+5, t 0,7).
8. **47 hisse:** Desen tek bir piyasa faktörü (etkin N ≈ 3); hisseye özgü kısım ≈ −1,4 bps.

**Güven:**
- Öğleden sonra düşüşü ve vadeli 11:00 kısa: ORTA. Mekanizma belirsiz; vadeli gün-içi 2017–2022'de doğrudan gözlenmedi; giriş saati post-hoc; getiri dağılımı sağa çarpık; son yıl zayıf.
- İddianın harfiyen hâli (açılışta sat): DÜŞÜK–ORTA.

## 4. Kod (`nice -n 10 python3 <script>`; dizin `out/code_v_G3_b/`, çıktılar `res/`)
- `bc.py`: yükleme, temizlik (±%10,5 simetrik), VİOP ayrıştırıcı (cp1254) → `res/viop_fut_b.parquet`, istatistik araçları (NW-t, blok bootstrap).
- `s1_spot.py`: yıllar, IS/OOS, uç değer, kriz hariç, haftanın günü, gap koşulu.
- `s2_isy.py`: İş Yatırım saatlik ayrıştırma (XU030, XU100, hisseler).
- `s3_viop.py`, `s3b_acilis.py`, `s3c_stale.py`: vadeli zamanlaması, bayatlık testleri, VWAP, regresyon.
- `s4_grid.py`: giriş/çıkış saat ızgarası, küçük-gap plasebosu, permütasyon.
- `s5_stocks.py`: piyasa artığı, etkin N, SSF bayatlığı.
- `s6_placebo_intl.py`: 37 yabancı endeks.
- `s7_regime_cost.py`: ima edilen taşıma rejimi, fiyat adımı, net getiri.
- `s8_combo.py`: kayan pencere, son 12 ay.
- `s9_other_idx.py`: XU100, XBANK, XUSIN.

TradingView: `BIST:XU030D1!` (işlem), `BIST:XU030`, `BIST:XU100`, `BIST:XBANK`, `BIST:XUSIN`. Hindistan karşılaştırması için `NSE:NIFTY`.
