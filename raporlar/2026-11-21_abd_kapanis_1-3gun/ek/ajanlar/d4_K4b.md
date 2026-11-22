# K4b · backtest

araç: 19/40

Sınanan kural × varyant: 124 · IS adayı: 1 · OOS'tan geçen: 0

## Özet

Ne sınandı: 31 kural varyantı, her biri h = 1, 2, 3 ve "kapanışta gir, ertesi açılışta çık" ile; toplam 124 test. Kurallar:
- R3-01: |SPY| ≥ %2 günden sonra ters yön; GEX(t−1) < 0, > 0 ve 252 günlük alt %20 ayrımı; hedef SPY ve QQQ.
- R3-02: kapanış konumu (IBS: kapanışın günün aralığındaki yeri) vekili ve kontrol sürümü; SPY, QQQ.
- R3-03: kendi getirisi |r| ≥ %1/2/3/4 olunca ters yön; SPY, QQQ. R8-11 bunun SPY %2 satırıyla aynı kural.
- R3-04: NVDA, TSLA, MSTR, COIN, AMD, PLTR'de ±%6 dönüşü, "yeni yapı" hattında.
- Yöntem denetçisi ekleri: VIX(t−1) − 20 günlük gerçekleşen oynaklık z-skoru (4 varyant), VIXY sıçraması ≥ +%10 / +%20, evren genişliği (<%10, <%20 ve hisselerin %90'ının düştüğü gün), büyük gün + uç IBS (SPY, QQQ ve 4 tek hisse; tek hisseler yeni yapı hattında).
- R3-11 ve R8-10 betimsel olarak ölçüldü.

IS (2010–2019) eleme: yalnız 1 aday çıktı. R3-02 kontrol sürümü (SPY |r| ≥ %1,5 ve IBS 0,3–0,7, h = 3): 18 işlem, +110 bps, t_olcekli 2,17. Bu aday OOS'ta geçemedi: 22 işlem, +45 bps, t 0,79, p_bootstrap 0,53. OOS'tan geçen kural yok. "Hiçbiri geçmedi" bulgusu budur. Aday üstelik kontrol varyantı; asıl hipotez varyantı (uç IBS) IS'te negatif. Yani mekanizmayı desteklemiyor.

Eşiğe en yakın elenenler:
- Genişlik < %20 → SPY uzun (h = 2 ve 3): t_olcekli 2,06 ve 2,37. Ama tek yönlü kural şartı olan t_anormal ≥ 2'yi sağlamadı (1,39 ve 1,31). Kazancın çoğu SPY'nin kendi yükseliş eğilimi.
- VIXY ≥ +%10, h = 3: t 1,69.

Tek hisse ±%6 dönüşü (R3-04) iki dönemde de zarar ediyor (IS2 h=1 net −20, h=3 −83 bps). Kısa bacak çok kötü: yükselişler devam ediyor. "Devam" kuralı önceden yazılı olmadığı için sınanmadı.

R3-11: IS'teki bütün kural × h için kapanış girişi ile ertesi açılış girişi farkı ortalama +0,6 bps (medyan +0,6, %54 pozitif). Endeks dönüş kurallarında fark birkaç bps. Tek hisse kurallarında açılış girişi 17–24 bps daha iyi: gece hareketi aleyhte devam ediyor.

R8-10: 3x ETF'nin 1–3 günlük sapması (oynaklık aşınması ve maliyet), kaldıraç × dayanak getirisine göre:
- h = 1'de −2 ile −5 bps.
- VIX(t−1) > 30'da h = 3: UPRO/SPXL −21, TQQQ −27, SOXL −33 bps; ters 3x ürünlerde SPXU −34, SQQQ −41, SOXS −88 bps.
- SPY ≤ −%3 günlerinden sonra h = 3: TQQQ −90, SOXL −97, SOXS −189 bps.
- "Dayanak %3 düşerse çık" kuralı her üç üründe kazancı azalttı.

En önemli çekince: 20 Kasım kapanışında bu ailenin ham sinyallerinin neredeyse hepsi "uzun" yanıyor (SPY −%3,64, IBS 0,10; VIXY +%13,4; genişlik %9,3). Hiçbiri doğrulanmadı. Bu sinyalleri gerçek parayla kullanma gerekçesi yok.

## Tablo

| kural_id | ad | hedef | yon | h | giris | korunma | is_net_bps | oos_net_bps | oos_n | oos_t | oos_p | son_net_bps | son_t | girisA_oos_net_bps | basabas_bps | vix30 | sinif | gerekce |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R3-02.SPY.kontrol | SPY /r/>=%1,5 ve IBS 0,3-0,7 (kontrol) -> ters | SPY | iki | 3 | K | yok | 110.4 | 44.6 | 22 | 0.79 | 0.53 | 133.7 | 2.25 | 61.7 | 27.6 | 8 bölüm, %38 aynı işaret (destekli değil) | DÜŞÜK | Tek aday kontrol varyantı. IS ve OOS aynı yönde ama OOS t 0,79 ve p 0,53; az işlem var, asıl hipotez varyantı negatif. |
| K4b-b.ma20 | 20g ort. üstündeki hisse payı < %20 -> SPY uzun | SPY | uzun | 3 | K | yok | 52 |  |  |  |  |  |  |  | 29.8 |  | ELENDİ | IS t_olcekli 2,37 ama t_anormal 1,31 < 2: kazanç SPY'nin kendi yükseliş eğiliminden; tek yönlü kural şartı sağlanmadı. |
| K4b-b.ma20 | 20g ort. üstündeki hisse payı < %20 -> SPY uzun | SPY | uzun | 2 | K | yok | 38.1 |  |  |  |  |  |  |  | 22.6 |  | ELENDİ | IS t_olcekli 2,06, t_anormal 1,39 < 2. |
| K4b-a2.vixy10 | VIXY günlük >= +%10 -> SPY uzun | SPY | uzun | 3 | K | yok | 66.4 |  |  |  |  |  |  |  | 36.6 |  | ELENDİ | IS t_olcekli 1,69 < 2 (t_anormal 1,80); 42 işlem. |
| K4b-b.ma10 | 20g ort. üstündeki hisse payı < %10 -> SPY uzun | SPY | uzun | 3 | K | yok | 82.7 |  |  |  |  |  |  |  | 45.4 |  | ELENDİ | IS t_olcekli 1,57, t_anormal 1,42; 45 işlem. |
| K4b-b.dus90 | Evrenin >= %90'ı düştü -> SPY uzun | SPY | uzun | 3 | K | yok | 31.4 |  |  |  |  |  |  |  | 19.1 |  | ELENDİ | IS t_olcekli 1,70, t_anormal 0,92. |
| R3-03.SPY.e2/R8-11 | SPY /r/>=%2 -> ters yön | SPY | iki | 1 | K | yok | -2.6 |  |  |  |  |  |  |  | 2.2 |  | ELENDİ | IS net negatif (115 işlem, t −0,84); h=2 −16, h=3 +2, gece −5 bps. |
| R3-03.SPY.e3 | SPY /r/>=%3 -> ters yön | SPY | iki | 1 | K | yok | 0 |  |  |  |  |  |  |  | 4 |  | ELENDİ | IS net 0 bps (33 işlem); uzun bacak +13, kısa bacak −19 bps. |
| R3-03.SPY.e4 | SPY /r/>=%4 -> ters yön | SPY | iki | 1 | K | yok | 94.4 |  |  |  |  |  |  |  | 51.9 |  | ELENDİ | 11 işlem, t 1,38; h=2 ve 3 negatif. |
| R3-03.QQQ.e2 | QQQ /r/>=%2 -> ters yön | QQQ | iki | 1 | K | yok | 3.1 |  |  |  |  |  |  |  | 4.8 |  | ELENDİ | IS t 0,00; h=3 +16 bps, t 0,70. |
| R3-03.QQQ.e3 | QQQ /r/>=%3 -> ters yön | QQQ | iki | 1 | K | yok | 19 |  |  |  |  |  |  |  | 13.2 |  | ELENDİ | IS t 0,33 (53 işlem). |
| R3-01.SPY.gex<0 | /SPY/>=%2 ters yön, GEX(t-1)<0 | SPY | iki | 1 | K | yok | 34.2 |  |  |  |  |  |  |  | 20.9 |  | ELENDİ | IS t 0,42 (34 işlem). GEX<0'da daha güçlü dönüş hipotezi yönce tutuyor ama anlamsız; GEX>0'da −15 bps. |
| R3-01.QQQ.gex<0 | /SPY/>=%2 ters yön, GEX(t-1)<0 -> QQQ | QQQ | iki | 1 | K | yok | 55.1 |  |  |  |  |  |  |  | 31.4 |  | ELENDİ | IS t 0,95; kazanç uzun bacakta (+136), kısa bacak −9 bps. |
| R3-02.SPY.ana | SPY /r/>=%1,5 ve IBS uçta -> ters | SPY | iki | 1 | K | yok | -4.2 |  |  |  |  |  |  |  | 1.3 |  | ELENDİ | Asıl kapanış konumu hipotezi IS'te negatif (h=1..3: −4, −22, −16 bps). |
| R3-02.QQQ.ana | QQQ /r/>=%1,5 ve IBS uçta -> ters | QQQ | iki | 3 | K | yok | 16.1 |  |  |  |  |  |  |  | 11.3 |  | ELENDİ | IS t 1,20 < 2. |
| K4b-c1.QQQ | QQQ /r/>=%2 ve IBS uçta -> ters | QQQ | iki | 1 | K | yok | 7.6 |  |  |  |  |  |  |  | 7.1 |  | ELENDİ | IS t 0,09. |
| K4b-c1.SPY | SPY /r/>=%2 ve IBS uçta -> ters | SPY | iki | 1 | K | yok | -5.8 |  |  |  |  |  |  |  | 0.7 |  | ELENDİ | IS net negatif. |
| R3-04.COK6 | Tek hisse ±%6 -> ters (yeni yapı) | COK(6) | iki | 1 | K | yok | -19.6 |  |  |  |  |  |  |  | -4.6 |  | ELENDİ | IS2 (2020–2023) net negatif (t_kume −0,70); h=3 −83 bps; kısa bacak −47…−158 bps: yükselişler devam ediyor. ETF öncesi IS'te de negatif. |
| K4b-c2.COK4 | NVDA,TSLA,MSTR,COIN /r/>=%2 + IBS uç -> ters (yeni yapı) | COK(4) | iki | 1 | K | yok | -17.8 |  |  |  |  |  |  |  | -4.8 |  | ELENDİ | IS2 net negatif; h=3 −67 bps. |
| K4b-a1.w250.z2 | VIX(t-1)-RV20(t-1) z(250)>2 uzun / <-2 kısa | SPY | iki | 3 | K | yok | 20.6 |  |  |  |  |  |  |  | 13.8 |  | ELENDİ | IS t 1,11; öteki 3 varyant sıfır civarı ya da negatif. |

## Elenenler

IS'te (2010–2019; yeni yapıda 2020–2023) eleme sonucu:
- 31 varyantın 30'u ve 124 testin 123'ü IS'te aday olamadı.
- Tek aday R3-02.SPY.kontrol, h=3 (18 işlem). OOS'ta t 0,79 ve p 0,53 ile düştü; sınıfı DÜŞÜK.

Elenme nedenleri:
- R3-01 (6 varyant): |SPY| ≥ %2 dönüşü GEX(t−1)'e göre ayrıldı. GEX<0'da yön hipotezle uyumlu (SPY h=1 +34, QQQ +55 bps) ama t ≤ 1,3. GEX>0'da negatif.
- R3-02 asıl varyant (uç IBS, SPY ve QQQ): IS'te negatif ya da t ≤ 1,2. Gün sonu baskısının günlük vekili çalışmıyor.
- R3-03 / R8-11 (8 varyant, eşik %1–4): hiçbir eşikte t ≥ 2 yok. SPY %2 h=1 −2,6 bps; %4'te 11 işlem.
- R3-04 ve K4b-c2 (tek hisse, yeni yapı): IS2'de belirgin negatif. Dönüş yerine devam görünüyor; devam kuralı önceden yazılı değildi, sınanmadı.
- VIX − RV (4 varyant): t ≤ 1,1. Gece varyantlarında t −2,6 ile −3,0 (negatif yönde).
- VIXY sıçraması: ≥ +%10'da t 1,69 (h=3). ≥ +%20'de yalnız 4 işlem.
- Genişlik (3 varyant): <%20 h=2 ve 3'te t_olcekli ≥ 2. Ama t_anormal 1,3–1,4 < 2: tek yönlü kural şartı sağlanmadı, kazanç SPY'nin kendi eğilimi. <%10 ve %90 düşüş gününde t < 2.
- Büyük gün + IBS (SPY, QQQ): t ≤ 0,1.

## Bugünkü durum

OOS'tan geçen kural yok; işlem yapılacak doğrulanmış bir sinyal yok.

20 Kasım 2026 kapanış durumu:
- SPY 689,81 (−%3,64, IBS 0,097), QQQ 608,45 (−%5,67, IBS 0,060).
- VIXY +%13,4 (kapanış 25,95). VIX(19.11) 28,44.
- GEX(19.11) −0,90 milyar, GEX(20.11) −2,16 milyar.
- 20 günlük ortalamasının üstündeki hisse payı %9,3; düşen hisse payı %85,3.

Bu yüzden ham sinyallerin hepsi uzun yanıyor: R3-01 GEX<0 ve alt%20, R3-02 ana (SPY ve QQQ), R3-03 SPY e1–e3 ve QQQ e1–e4, R3-04 altı hisse, VIXY ≥ %10, genişlik <%10 ve <%20, c1 (SPY, QQQ), c2 dört hisse. Hiçbiri doğrulanmadı; kullanılmamalı.

Tek aday (R3-02.SPY.kontrol, DÜŞÜK) 20.11'de kapalı (IBS uçta). 23 Kasım kapanışında tetiklenme koşulu:
- Uzun: SPY ≤ 679,46 (−%1,5) ve kapanış günün aralığının %30–70'inde.
- Kısa: SPY ≥ 700,16 (+%1,5), aynı IBS koşuluyla.
Bu kural OOS'ta t 0,79; VIX > 30 bölümlerinde %38 aynı işaret: "bugün kullanma".

Bilgi için R3-03 SPY %2 düzeyleri: ≤ 676,01 ya da ≥ 703,61 (doğrulanmamış).

## Sapmalar

1) R3-01'de kuralın istediği "t günü GEX" yerine GEX(t−1) kullanıldı. GEX kapanıştan sonra yayımlanıyor; t günü değeri ancak Giriş A ile kullanılabilirdi. GEX(t) + Giriş A varyantı sınanmadı. R3-01'de QQQ hedefi de SPY'nin getirisiyle tetiklenir (kural metni böyle). R3-03'te her hedef kendi getirisiyle tetiklenir.
2) Bütün kurallar h=1,2,3 ve gece varyantıyla sınandı. R3-03/R8-11 kuralı yalnız h=1, R3-04 h=1 ve 3 diyordu; fazladan testler sayıya dahil (124).
3) R3-04'te benzer oynaklıktaki, kaldıraçlı ETF'i olmayan hisselerden kontrol grubu kurulmadı: hangi hisselerin ürünü olmadığı veriyle doğrulanamıyor. AMD ve PLTR'nin kaldıraçlı ürünleri panelde yok. Fark-içinde-fark yerine ETF öncesi dönem (IS 2010–2019) bilgi satırı olarak verildi.
4) Genişlik kuralında STRES (2005–2009) için 2010 dönem başı evreni kullanıldı. Yalnız STRES, TUM ve bölüm satırlarını etkiler; karar satırlarını etkilemez.
5) VIX − RV'de iki taraf da t−1 değeri: VIX(t−1) − RV20(t−1), zaman uyumu için.
6) R8-11'in VIX ≥ 30 alt kümesi ve R3-03'ün 2006–2011 / 2012–2026 alt dönemleri raporlanmadı. Kural IS'te aday olmadığı için tarama rejimsiz yapıldı; OOS'a bakmamak için alt dönem kırılımı çıkarılmadı. SH panelde yok.
7) R8-10 betimseldir: maliyetsiz, ETF ile kaldıraç × dayanak arasındaki brüt sapma. K1/K3/K4 olay günleri bu ölçüm için burada yeniden tanımlandı: K3 = VIX(t−1) ≥ 35, K4 = VIX(t−1) ≥ 30 ve |SPY| ≥ %1,5. %3 durdurma kuralı yalnız K1 günlerinde, h=3, brüt olarak hesaplandı. SOXL/SOXX endeks farkı (2021 öncesi) sapmaya karışıyor.
8) OOS'tan geçen kural olmadığı için 15:30 testi, ters/kaldıraçlı ETF uygulama satırları, komşu parametre testi ve korunmalı satırlar üretilmedi. kapanis1530_K4b.csv boş; komsu_K4b.csv yazılmadı.

## Notlar

- Motor ve veri: motorda hata bulmadım; motor.py ve yukle.py'ye dokunulmadı. 31 sinyal fonksiyonunun hepsi bakis_testi'ni temiz geçti. bakis_testi dış dosyadan gelen GEX'i göremez; GEX yapı gereği 1 gün geciktirildi.
- Yalnız bu ailenin içindeki BH: tek aday, p 0,53. Birleşik BH için aday p'si 0,53; başka aday yok.
- Kapanış ile ertesi açılış girişi farkı (R3-11; IS, bütün kural × h, net, K − A): ortalama +0,6 bps, medyan +0,6, %54 pozitif. Gruplara göre ortalama:
  - Endeks dönüş kuralları: R3-03 +6,0 ve R3-01 +5,2 (geniş dağılım). R3-02 +13,8; bunu kontrol varyantı (+43…+47, n ≈ 19) şişiriyor, asıl varyant −1…−6.
  - Tek hisse kuralları negatif: R3-04 −23, c2 −17; yani açılış girişi daha iyi.
  - Sonuç: dönüş sinyallerinde kapanış girişinin kayması kenarın belirleyici kısmı değil; zaten kenar yok.
- Kaldıraçlı ETF yolu (R8-10): ortalama sapma, VIX(t−1) kovasına göre (h=3, bps):
  - VIX < 20: UPRO −6,3, TQQQ −6,1, SOXL −6,5, SPXU +6,7.
  - VIX 20–30: UPRO −5,9, TQQQ −6,9, SOXL −14,3.
  - VIX > 30: UPRO −20,6, SPXL −20,8, TQQQ −26,5, SOXL −32,5, SPXU −34,3, SQQQ −40,5, SOXS −87,5.
  - SPY ≤ −%3 günlerinden sonra (46 olay, h=3): TQQQ −90, UPRO −68, SOXL −97, SQQQ −97, SOXS −189. Medyanlar daha küçük (−10…−56), yani kuyruk etkisi var. p05: SOXS −1.070 bps.
  - Bugünkü rejimde 3x ürünle 3 gün tutmak, dayanak tahmini doğru olsa bile 20–90 bps götürür.
  - %3 durdurma kuralı kazancı düşürdü (K1, h=3, brüt): UPRO −37 → −63, TQQQ +66 → −27, SOXL +257 → +136 bps; olayların %20–30'unda tetikleniyor.
- Şüpheli ya da dikkat:
  - Tek aday bir kontrol varyantı ve IS'te 18 işleme dayanıyor; IS p_bootstrap 0,11. Son dönemde +134 bps, t 2,25 (11 işlem) ama karar dışı.
  - Genişlik < %20'deki net t ≥ 2, anormal getiri şartıyla düştü; denetçinin uyarısıyla uyumlu.
  - R3-04'te kısa bacaktaki büyük zararlar, tek hisse kaldıraçlı ürünlerin dayanaklarında dönüş değil devam olduğunu düşündürüyor. Bu sonradan görülmüş bir gözlem; önceden yazılı kural olmadan sinyal sayılmamalı.
- Maliyet: IS 2010–2019'da AMD gibi düşük fiyatlı hisselerde 0,5 sent tabanı ve hisse başı komisyon maliyeti işlem başına yaklaşık 30 bps'ye çıkarıyor; R3-04 IS'te brüt −9, net −39 bps.
- Çalışma süresi: tek komut yaklaşık 50 saniye (python3 -I aile_K4b.py).

## Dosyalar

- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/aile_K4b.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/aday_K4b.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/sonuc_K4b.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/karar_K4b.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/kayma_K4b.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/yol_K4b.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/bugun_K4b.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/kapanis1530_K4b.csv
