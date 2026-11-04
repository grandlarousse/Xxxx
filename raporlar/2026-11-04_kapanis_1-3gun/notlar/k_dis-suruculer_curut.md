# k_dis-suruculer_curut — dış sürücü adaylarını çürütme denemesi (bağımsız kod)

_03.11.2026 · veri 30.10.2026'ya kadar · kod: out/code_k_dis-suruculer_curut/ · sonuçlar: out/code_k_dis-suruculer_curut/res/ · yatırım tavsiyesi değildir_

## Ne yapıldı
Tarayıcının (k_dis) yalnız UYGUN ve KOŞULLU adayları sıfırdan yeniden hesaplandı. Tarayıcının `klib` ve `ll` kodları import edilmedi; ham parquet dosyaları doğrudan okundu.

- **VİOP ön vade:** vadeye en az 3 BIST işlem günü kalan en yakın standart kontrat (N1 ve mini kontratlar hariç; tarayıcı ≥2 iş günü kullanıyor). Getiri = aynı kontratta ln(settle/prev_settle). Hisse vadelisinde limit bandı dışı günler ve spottan (adj) %8'den fazla ayrışan günler atıldı. 2 ve 5 günlük roll kuralıyla da denendi; sonuçlar ±1 bps değişti.
- **Temettü:** Bültendeki prev_settle her zaman bir önceki uzlaşmaya eşit. Temettü günlerinde vadeli getirisi spot adj getirisine yakın, yani bülten fiyatları düzeltilmiş (TUPRS 11, EREGL 9 hak kullanım günü kontrol edildi). Temettü gününü kapsayan işlem sayısı 1–5; sonuca etkisi yok.
- **Sinyal eşlemesi:**
  - BIST kapanışından sonra kapanan piyasalar (ABD, Avrupa, COMEX): yalnız tarihi t'den önce olan günler kullanıldı. BIST tatillerinde arada kalan günler toplandı.
  - BIST kapanışından önce kapanan piyasalar (ASX): t_önceki < tarih ≤ t.
  - Saatlik veride: bitiş zamanı 15:00 UTC'ye kadar olan son barın kapanışı.
- **İşlem kuralı:** z = sinyal / geçmiş 250 günlük std (saatlikte 120), |z|>1 → yön(z), h gün tut. İşlemler örtüşmüyor.
- **Maliyet:** 8 ve 15 bps; hedge'li işlemde +3 bps. Ayrıca y_viop_likidite'deki küçük emir ve 1 mn TL maliyeti; roll içeren işlemde bir maliyet daha eklendi.
- **Sağlamlık testleri:**
  - (i) 24 varyantlık ızgara: h 1/2/3/5 × eşik 0,5/1/1,5 × raw/hedge'li.
  - (ii) Dairesel kaydırma null'u: sinyal takvimde ≥250 gün kaydırıldı, ızgaranın en yüksek t'si alındı. Varyant seçimi düzeltilmiş p; ana dört aday için 2.000, diğerlerinde 300 tekrar.
  - (iii) Plasebo: aynı sinyal diğer VİOP hisselerine uygulandı.
  - (iv) Rejim drifti düzeltmesi: aynı takvim yılının koşulsuz t→t+h ortalaması × yön çıkarıldı.
  - (v) En iyi 10 işlem çıkarıldı.
  - (vi) Alt dönemler: 2017–19, 2020–21, 2022–23, 2024–26 ve fon krizi (Eylül–Ekim 2026).
  - (vii) Dolum: uzlaşma yerine son işlem fiyatı.

## Zamanlama denetimi
- **VİOP XAUUSD uzlaşması** 15:00 UTC altınıyla örtüşüyor: günlük değişimin saatlik GC=F snap'iyle korelasyonu 14:00'te 0,90, 15:00'te **0,97**, 16:00'te 0,90 (2024-07+). Sinyal girişle aynı dakikalarda oluşuyor. 18:00 TSİ altını pratik bir vekil: |z|>1 günlerinde işaret uyumu %100, eşik uyumu %84.
- **VİOP USDTRY uzlaşması** saatlik TRY=X ile en yüksek korelasyonu 15:00'te veriyor (0,79; Yahoo TRY saatlik verisi gürültülü).
- **Yahoo TRY=X günlük kapanışı** (ldate) VİOP USDTRY'nin hem aynı gününe (0,54) hem ertesi gününe (0,47) yayılıyor. Zaman damgası güvenilmez, spot kur sinyali için kullanılamaz.
- **ABD günlük kapanışı** (VLO) saatlik 21:00 UTC snap'iyle 0,99 örtüşüyor. ASX günlük kapanışı (FMG) 06:00 UTC snap'iyle 0,99. İkisinin eşlemesi de doğru.

## Sonuç tablosu (benim hesabım, VİOP uzlaşma → uzlaşma)

| Aday | Ana varyant | n, işlem/yıl | net 8 bps (t) | net 15 / 1 mn TL+roll | IS / OOS | Izgara-düzeltmeli p | En iyi 10 çıkınca | 2024–26 | Hüküm |
|---|---|---|---|---|---|---|---|---|---|
| ABD rafineri t-1 → TUPRS | h2 raw | 492, 53 | +42,0 (2,72) | +35,0 / +37,3 | +34,5 (1,71) / +48,8 (2,12) | 0,0035 (2.000) | +20,4 (1,45) | +26,3 (1,02) | KOŞULLU, ORTA |
| FMG/BHP bugün → EREGL | h3 hedge'li | 373, 43 | +46,3 (2,95) | +39,3 / +39,2 | +80,7 (3,54) / +19,7 (0,92) | 0,005 (2.000) | +21,6 (1,55) | +59,2 (2,21) | KOŞULLU, DÜŞÜK |
| VİOP altın bugün → TRALT | h2 hedge'li | 405, 55 | +42,9 (2,54) | +35,9 / +34,0 | +44,1 (1,82) / +42,3 (1,89) | 0,024 (2.000) | +20,7 (1,31) | +69,7 (2,44) | KOŞULLU, DÜŞÜK |
| VİOP USDTRY 5g → THYAO | h3 raw | 282, 31 | +99,3 (3,79) | +92,3 / +97,1 | +87,6 (2,19) / +112,1 (3,37) | <0,0005 (2.000) | +59,3 (2,50) | +73,7 (2,12); drift düzeltmeli +28,7 (0,82) | KOŞULLU, DÜŞÜK |
| Avrupa savunma 15:00 → ASELS | h2 raw | 120, 48 | +62,8 (1,74) | +55,8 / +58,2 | yarılar +76 / +52 | 0,19 (300) | −2,1 (−0,06) | (tamamı 2024-04+) | UYGUN DEĞİL |
| Kredi notu kademe → XU030 ters | h2 | 16, 1,6 | +142 (2,93) | +135 | brüt 2017–21 +146 (n=7) / 2022–26 +152 (n=9) | aynı yıl rastgele tarih p 0,009 | en iyi 3 çıkınca +94 (1,87) | n=6, +99; son ikisi kayıp | KOŞULLU, DÜŞÜK |
| FOMC/NFP/CPI risk | std oranı | 77/34/34 | — | — | — | std oranı p 0,09–0,92 | — | — | KOŞULLU (yalnız bilgi), DÜŞÜK |
| Akşam seansı (ES) | — | 587 | — | — | — | — | — | R² %1,5 | UYGUN DEĞİL |

## Aday ayrıntıları

### 1. ABD rafineri sepeti (VLO, MPC, PSX, PBF − β·S&P 500), t-1 → F_TUPRS
- **Doğrulandı:** h2 raw +42,0 bps (tarayıcı +41,8). Regresyonda hissenin kendi artığı ve XU030 kontrol edildiğinde z katsayısının t'si 3,6 (h2) ve 4,1 (h3).
- **Plasebo:** TUPRS 44 hisse içinde 1. sırada. Diğer hisselerin t ortalaması −0,25; hiçbirinde t>2 yok.
- **Dairesel null:** tek varyant p<0,003; 24 varyantın en iyisi düzeltmesiyle p = 0,0035 (2.000).
- **Sağlamlık:** dolum (son işlem fiyatı +40,8) ve roll kuralına duyarsız. 2020 sonrası +59,7 (t 3,15).
- **Zayıf yanlar:**
  - Tarayıcının h3 rakamı abartılı: benim hesabımda +41,6 (t 1,93), tarayıcıda +55,3 (t 2,7).
  - Kazanç birkaç işlemde yoğunlaşıyor; en iyi 10 işlem (%2) çıkınca h2 +20,4 (t 1,45), h3 +11,5 (t 0,58).
  - Alt dönemler: 2017–19 −9,4; 2020–21 +86; 2022–23 +88; 2024–26 +26,3 (t 1,02); 2026 +11; fon krizi −142 (n=9). Rejim drifti düzeltmesiyle 2024–26 +21,4 (t 0,84).
  - Sepet PBF'ye bağımlı: PBF çıkarılınca t 1,67; yalnız PBF ile t 4,0; yalnız PSX ile ≈0.
  - Bir gün eski sinyal de çalışıyor (t 2,19), yani sönüm yavaş ve gecikmeli uygulamaya dayanıklı.
- **Hüküm:** Sinyal gerçek ama büyüklüğü abartılı. Bugünkü beklenti net +20–25 bps/işlem civarı. UYGUN değil KOŞULLU: yalnız h2, küçük pozisyon. ORTA güven.

### 2. FMG/BHP (ASX) bugünkü artığı → F_EREGL
- **Doğrulandı:** h3 hedge'li +46,3 bps (tarayıcı +46,9). Ana varyantın dairesel null'u p<0,003; ızgara düzeltmeli 0,005 (2.000). Plasebo 1/44. Ancak HEKTS gibi ilgisiz bir hisse de t 2,6–3,1 veriyor.
- **Çürütmeye yakın bulgular:**
  - OOS 2022–26 +19,7 (t 0,92); 2022–23 −50 (t −1,45).
  - Vade profili tutarsız: h1 +13, h2 +28, h3 +46, h5 +12 (t 0,46). 4. ve 5. günlerde etki geri dönüyor.
  - Bir gün eski ASX sinyali etkisiz (t 0,6). Yalnız FMG ya da yalnız BHP ile h2 t ≤1,1.
  - En iyi 10 işlem çıkınca t 1,55.
- **Olumlu taraf:** 2024–26 +59 (t 2,2), fon krizinde de pozitif.
- **Hüküm:** KOŞULLU, DÜŞÜK. Yalnız h3, hedge'li ve küçük pozisyon. KRDMD'de IS ≈0 olduğu için kullanılmamalı.

### 3. VİOP altın (XAUUSD uzlaşması) bugünkü değişimi → F_TRALT − β·F_XU030
- **Doğrulandı:** h2 hedge'li +42,9 bps, t 2,54 (tarayıcı +51,8, t 3,2). Izgara düzeltmeli p = 0,024 (2.000); plasebo 1/44.
- **Zayıf yanlar:**
  - Hedge'siz raw sürüm t 1,53; raw'da en iyi 10 işlem çıkınca t 0,31. Hedge'li sürümde en iyi 10 çıkınca t 1,31.
  - Rejime bağlı: z katsayısının t'si 2019–20'de 3,4, 2021–22'de 0,0, 2023–24'te 0,9, 2025–26'da 1,7.
  - Dünkü COMEX altını (t-1) etkisiz (t 0,07), dünkü VİOP altını da etkisiz (t 0,5). Bilgi yalnız aynı günün 18:00 altınında.
  - Pratik 15:00 UTC sürümü (2024-07+) h2 +64 (t 1,8); uzlaşmalı sürüm aynı dönemde +84 (t 2,56).
- **TRMET:** ızgara düzeltmeli p 0,065, OOS t 1,33; 1 mn TL maliyetle t 1,31 → zayıf.
- **Hüküm:** KOŞULLU, DÜŞÜK. Altın trend rejiminde, iki bacakla (hedge'li).

### 4. VİOP USDTRY 5 günlük kümülatif değişim → F_THYAO
- **Doğrulandı:** h3 raw +99,3 bps (t 3,79); ızgara düzeltmeli <0,0005 (2.000). En iyi 10 işlem çıkınca da +59 (t 2,5). Dört aday içinde en sağlamı.
- **Ama kazancın kaynağı başka:**
  - **Carry/drift:** Vadeli USDTRY getirisi carry'yi içerir. 2024–26 carry rejiminde vadeli kur her gün düşüyor; sinyallerin uzun payı 2024'te %8, 2025'te %0, 2026'da %1. Strateji fiilen sürekli THYAO kısa pozisyonu tutuyor ve THYAO'nun aynı dönemdeki zayıflığından kazanıyor. Hep uzun kıyası 2024–26'da −49 bps. Yıl drifti düzeltmesiyle 2024–26 +28,7 (t 0,82).
  - **Spot kur tekrar etmiyor:**
    - Yahoo TRY=X 5g (t-1) → VİOP THYAO: +49 (t 1,32), OOS ≈0.
    - Spot THYAO 2014+: t 1,79; IS t 0,41; en iyi 10 işlem çıkınca ≈0.
    - Saatlik 15:00 TRY=X (2023-12+): −71 (t −2,27).
  - **Ortak faktör:** raw sürümde diğer hisselerin %23'ü t>2 veriyor (TL'nin nominal etkisi). Hedge'li sürümde bu oran %2.
- **Carry çıkarılmış (demeaned) sürüm:** h3 raw +96,5 (t 3,0); 2024–26'da n=49, +66 (t 1,27). Uzun sinyaller (kur şoku): +150 (t 3,3, n=106) ama en iyi 10 çıkınca t 1,53; 2024–26'da yalnız 4 uzun sinyal var.
- **Hüküm:** KOŞULLU, DÜŞÜK. Yalnız carry'si çıkarılmış sinyalle ve TL şoku dönemlerinde (z>1 uzun). Tarayıcının "+96 bps, ORTA" değerlendirmesi rejim driftini alfa sayıyor.

### 5. Avrupa savunma 15:00 → F_ASELS — UYGUN DEĞİL
- Saatlik veri 2023-12'de başlıyor; ısınma döneminden sonra işlemler 2024-04'ten itibaren. n=120.
- h2 raw +62,8 (t 1,74; tarayıcı +93,8, t 2,85). Hedge'li +32 (t 1,0).
- Izgara düzeltmeli p 0,19. En iyi 10 işlem çıkınca −2 bps.
- Yıllar: 2024 0, 2025 +166, 2026 +3. Tek yılın sonucu.
- Carry çıkarılmış sürüm t 1,0. Günlük t-1 vekilinde 2019–21 negatif.

### 6. Kredi notu kademe kararı → tepki günü F_XU030 uzlaşmasında ters yön, 2 gün
- Kendi olay listemle (16 kademe kararı, 2018-03 → 2025-07) sonuç aynı çıktı: h2 +150 brüt (t 2,93), isabet %75.
- **Plasebo:** aynı yıldan rastgele tarih p 0,009; aynı yıldan rastgele Pazartesi p 0,007. Drift düzeltmesi sonucu değiştirmiyor.
- **Zayıf yanlar:**
  - Tepki günü kararın yönünde hareket olaylarda yalnız %31. Yani "tepkinin geri dönüşü" gerekçesi yanlış; olan şey, açıklama gününün ters hareketinin sürmesi.
  - En iyi 3 olay çıkınca +94 (t 1,87).
  - Son iki karar kayıp (S&P 2024-11 −217, Moody's 2025-07 −53).
  - Tarayıcı ~16 varyant denedi; kaba Bonferroni sonrası p ≈0,14.
- **Hüküm:** KOŞULLU, DÜŞÜK. Yılda 1–2 olay, taktik ve küçük pozisyon.

### 7. FOMC/NFP/CPI günleri risk
- F_XU030 std oranı:
  - FOMC h1/h2/h3: 1,03 / 1,07 / 1,18 (bootstrap p 0,36 / 0,26 / 0,09).
  - NFP: 0,88 / 1,13 / 0,95.
  - CPI: 0,91 / 0,75 / 0,92.
- Riskte artış yok, bu günlerde pozisyon küçültmeye gerek yok. Bu bir "bir şey yapma" bilgisidir.
- FOMC ertesi +45 bps (t 2,1): 2017–21 +0,8, 2022+ +88 → alfa değil, rejim.

### 8. Akşam seansı — UYGUN DEĞİL
- Çıkış uzlaşmada değil, akşam seansında (19:00–23:00 TSİ) oluyor; kullanıcı profilinin dışında.
- Akşam fiyatı bültende yok; tarayıcının sonucu modele dayalı.
- ES'nin akşam hareketi (15→20 UTC) ertesi XU030 uzlaşma getirisinin yalnız %1,5'ini açıklıyor (β 0,31). Alfa yok.

## Ortak bulgu: roll
Dört adayda da roll içeren işlemler negatif ya da zayıf. Net bps: TUPRS −12,6 (n=44), EREGL −12,2 (n=47), TRALT −25,4 (n=20), THYAO +17 (n=34); roll içermeyen işlemler +47…+111. Örneklem küçük ama işaret tutarlı. Pratik kural: vadeye 3 iş gününden az kalmışsa işleme bir sonraki vadeden girin, ya da roll'u kapsayan sinyali atlayın.

## Kontrat likiditesi (ön vade, medyan günlük işlem hacmi, mn TL)
- TUPRS: 2017 0,6 / 2018 1,7 / 2019 7 / 2020 44 / 2023 524 / 2026 1.794
- TRALT: 2018 0,2 / 2019 2,7 / 2020 15 / 2026 1.379
- ASELS 2026: 2.989
- 2017–19 uzlaşmaları ince işlemden oluşuyor. 2020 sonrası sonuçlar: TUPRS +59,7 (t 3,15), EREGL +37,9 (t 2,09), TRALT +42,7 (t 2,35), THYAO +128 (t 3,96).

## UYGUN DEĞİL (tarayıcının listesi, yeniden test edilmedi)
- Havayolu/havalimanı sepetleri: etki t günü içinde tükeniyor; günlük vekilde t <1,6, 15 bps maliyette sıfır.
- TKC → TCELL: işaret ters, hissenin kendi dönüşü.
- Brent, bira, çelik ve altın madencisi sepetleri: FDR yok; rafineri ve VİOP altınının zayıf kopyaları.
- Çok günlük ES/EEM/Brent/altın/TUR/DİBS: FDR yok.

## Test sayısı ve FDR
- Gerçek veride ≈780 istatistik hesaplandı.
- Null tarafında 4 × 2.000 × 24 ve 6 × 300 × 24 dairesel kaydırma simülasyonu yapıldı.
- Birincil hipotezler (8): BH-FDR q=0,05 → ızgara düzeltmeli p'lerle (USD <0,0005; REF 0,0035; ASX 0,005; not 0,0086; ASELS en iyi varyant 0,023; altın 0,024; TRMET 0,065; FOMC risk 0,085) 6 hipotez geçiyor. Not kararı için varyant düzeltmesi (≈0,14) ve ASELS'in ana varyantı (0,19) kullanılınca 4 hipotez geçiyor: USD, REF, ASX, altın. Bu p'ler aynı çift üzerindeki 24 varyantı düzeltiyor, ama 32 ön-kayıtlı hedef çift arasındaki seçimi düzeltmiyor. Kaba Bonferroni ×32 ile REF 0,11, ASX 0,16, altın 0,77; USDTRY'nin ailesi daha büyük (47 hisse × birçok sürücü). Plasebo sıralamasının 1/44 olması özgüllük açısından destek veriyor.

## Dosyalar
- res/c1_grid.csv, c1_robust.csv, c1_trades_h2raw.csv, c1_ref.json
- res/c2_*, c3_*, c4_*, c5_*, c6_rating.csv
- res/d_drift.csv, c7_rolldiv.csv, n_null.csv
