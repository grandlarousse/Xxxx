# Bedelsiz sermaye artırımı olay çalışması: BIST, 2015–2026 (ajan: olay_bedelsiz)

06.11.2026. Bilgi amaçlıdır, yatırım tavsiyesi değildir. Bütün getiriler kapanıştan kapanışa, TL, Is Yatırım düzeltilmiş (temettü dahil toplam getiri) fiyatlarıyla. AR (anormal getiri) = hisse − XU100. t değerleri olay gününe (t0) göre kümelenmiştir. Maliyet: gidiş-dönüş 25 bp.

## 0. Hüküm

| Soru | Veri ne diyor | Hüküm |
|---|---|---|
| YK (ilk) duyurusunda al | Duyuru günü AR +2,4% (t=10,4). Ama bunun tamamı **tavan kilitli** açılışlardan geliyor: t0 kilitsiz olaylarda CAR[0,1] **+0,1%** (t=0,3); kilitli olaylarda +13,4%. İlk dolabilir kapanışta alıp 5 gün tutmak: BHAR **−1,8%** (t=−4,9), 10 gün −2,2%. | **Yaramaz** |
| "SPK onayında al, bölünmeye sat" | Onay SPK bülteninde akşam çıkıyor (%97'si 18:00 sonrası). Getiri ertesi sabah **açılış boşluğunda** oluşuyor (AR[0] +1,4%), gün içinde geri veriliyor (AOF'tan kapanışa −0,8%). Onay t0 kapanışı → hak−1 kapanışı: BHAR **+0,18%** (t=0,5), net −0,07%. 2024–26: −0,2%. | **Yaramaz** |
| "Bölünme sonrası küçük yatırımcı rallisi" | Tersi. Hak günü kapanışından sonra 5 günde −2,8% (t=−6,7), 10 günde −3,3% (t=−6,1). Bu düşüş %500 ve üstü oranlarda daha derin (10 günde −6,1%). Ancak 2024–26'da zayıflamış: 10 günde −1,2% (t=−1,3). | **Yaramaz** (al tarafı). Pratikte bir **çıkış kuralı**: hak gününden önce sat. |
| Başvuruda al, hak−1'de sat (≈47 işlem günü) | Ortalama BHAR +5,2% (t=3,0), ama medyan +0,3%. Getiri 2020–23'teki birkaç çok büyük kazançtan geliyor. 2024–26: ortalama +0,4%, medyan −2,9%. Takvim-zamanı portföyü: tüm dönem +15%/yıl XU100 fazlası (t=1,6), 2024–26 **−24%/yıl**. 2024–26'da işlemlerin yalnız %33'ü %40 TL engelini geçiyor. | **Yaramaz** (2024–26), en iyi ihtimalle piyango |
| Sızıntı | İlk duyurudan önceki 60 günde CAR +9,8% (medyan +4,3%). Aynı hisselerin koşulsuz 60 günlük ortalaması +3,8%, yani fazlası ≈ +6%. Koşulsuz taban düşüldüğünde [−20,+1] birikiminin ≈%65'i, [−60,+1] birikiminin ≈%72'si duyurudan önce gerçekleşiyor. Duyurudan önceki 5 günde hacim medyan 1,37×; olayların %32'sinde 2×'in üstünde. | Sızıntı **ve** "fiyat yükselince bedelsiz kararı" seçilimi birlikte; ayırt edilemez |
| Bedelli (rüçhan) | İlk duyuru: CAR[0,1] **−2,8%** (t=−4,6). Hak günü ve sonrasında anlamlı ve tutarlı bir drift yok. | Yaramaz (olsa olsa kaçınma sinyali) |
| **Temettü (yüksek verim)** | Duyuru verimi ≥%5 (N=400): duyuru t0 kapanışında alıp hak−1 kapanışında satmak (temettü alınmaz): BHAR **+8,5%**, medyan +6,5%, t=11,1, isabet %74, medyan süre 28 işlem günü. 2024–26'da +14,4% (t=7,6, N=67). 12 yılın 12'sinde de pozitif. Takvim-zamanı: net +56%/yıl XU100 fazlası (t=5,1). Hak gününden sonra 5 günde −2,1% (t=−7,7). | **Güçlü aday, koşullu.** Bu bir "hızlı bakış"; aşağıdaki uyarılarla ayrıca doğrulanmalı (§8). |

Kısacası bedelsiz folklorunun hiçbir kolu, işlenebilir ve net olarak %36–40 TL engelini geçmiyor. Sağlam iki bulgu var:

- Bedelsiz ve yüksek verimli temettüde hak gününden sonra sistematik bir düşüş var. Bu bir **kaçınma/çıkış** kuralıdır.
- Yüksek verimli nakit temettülerde duyurudan hak gününe güçlü bir yükseliş var.

## 1. Veri ve olay tarihleri (yalnız kamuya açık kaynaklar, varsayılan HTTP başlıkları)

| Aşama | Kaynak | Kapsam (hak günü 2015–2026, N=601) | Zaman damgası |
|---|---|---|---|
| Hak (bölünme) günü ve oran | Is Yatırım şirket kartı "Sermaye Artırımları" AJAX tablosu (`GetSermayeArttirimlari`, yıl yıl, tüm hisseler) | 601/601 | gün |
| P1: ilk duyuru (YK kararı / temettü teklifi) | KAP bildirim sorgusu (`api/disclosure/members/byCriteria`): "Sermaye Artırımı/Azaltımı" konusunda 7.750 bildirim, "Kar Payı Dağıtımı" konusunda 11.930 bildirim. Belirsiz özetler için 1.638 bildirim detayı okundu (YK karar tarihi, SPK başvuru ve onay tarihi, oran alanları). | 596 (450 KAP-CA, 151 KAP-KPD [bedelsiz temettü]) | dakika |
| P2: SPK başvurusu duyurusu | KAP özet/detay ("başvuru"), ayrıca 2014–17 bültenlerindeki "Yeni Başvurular" tablosu | 573 | dakika |
| P3: SPK onayı | 786 SPK haftalık bülteni (2014/1–2026/78) indirildi, PDF→metin. "Onaylanan" pay ihracı tablosunda şirket unvanı eşlendi. KAP onay bildirimi bültenden en fazla 3 gün önceyse onun zamanı alındı. | 599 (586 bülten) | 2022+ bülten yükleme saati (%98'i 18:00 sonrası); önceki yıllarda 18:30 varsayıldı |
| Fiyat | Is Yatırım `HisseTekil` (düzeltilmiş ve düzeltilmemiş kapanış, en yüksek/en düşük, AOF, piyasa değeri, hacim) ve `ChartData` (XU100, XUTUM, XYUZO, temettü-only hisseler) | 331 hisse (bedelsiz), toplam 614 | gün |

Doğrulamalar:

- **Bülten eşlemesi:** KAP detayındaki "SPK Onay Tarihi" ile bülten tarihi arasındaki fark medyan 0 gün; olayların %99,6'sında ≤7 gün (N=522).
- **KAP onay bildirimi:** Bültenden medyan 0,96 gün sonra yayımlanıyor; yalnız %8'i bültenden önce.
- **P1 ile son YK karar tarihi:** CA olaylarının %73'ünde fark ≤1 gün; %22'sinde P1 daha erken. Bu ikinci grup sonradan revize edilen kararlar (ör. AEFES, ARSAN, DESA). İlk kamu bilgisi P1 olduğu için doğru seçim P1.
- **Bölünme düzeltmesi:** Ham kapanışın hak günündeki medyan sıçraması −53%, düzeltilmiş temiz getirinin medyanı +0,2%. Hiçbir olayda |temiz getiri| %20'yi aşmıyor. Saf bedelsiz olaylarda gözlenen düzeltme çarpanı, teorik 1+oran ile **%99'unda %1 içinde**. Örnekler (hak günü ham → temiz getiri): SASA 2024 %700 (−87,4% → +0,9%), KORDS 2026 %1.800 (−94,8% → −1,6%), ADEL 2024 %1.000 (−90,2% → +7,6%), ACSEL 2015 %889 (−90,5% → −5,5%), SASA 2023 %130 (−52,8% → +8,6%).
- **İki fiyat kaynağı:** HisseTekil düzeltilmiş kapanışı ile ChartData kapanışı arasında getiri korelasyonu 0,9999 (THYAO, KORDS).
- **Dışlananlar:** ISATR ve ISBTR (4 olay; işlem görmeyen pay grupları, düzeltme yok).

Getirinin kendisi: Düzeltilmiş seri 4 ondalığa yuvarlandığı için çok bölünmüş hisselerde gürültülü. Bu yüzden getiri ham kapanıştan hesaplandı ve yalnız düzeltme çarpanının kırıldığı günlerde parça-medyan çarpanla düzeltildi.

Tradability kuralları:

- **t0:** Bilginin kamuya çıktığı andan sonraki ilk kapanış. 18:00'den önce yayımlanan bilgi için aynı gün (kapanış seansında alım mümkün), değilse ertesi işlem günü. P1'lerin %63'ü 18:00 sonrası, P3'lerin %97'si 18:00 sonrası yayımlanıyor.
- **Tavan/taban kilidi:** Günlük getiri ≥+%9 ve kapanış = gün içi en yüksek fiyat ise "tavan kilitli" sayıldı; kapanışta alım dolmaz varsayıldı (simetrik olarak taban kilidinde satış dolmaz).
- **"Dolabilir" varyant:** Giriş ilk kilitsiz kapanışa kaydırıldı.
- **"Kilitli hariç" varyant:** Kilitli girişler atıldı.
- **AOF varyantı:** t0 gününün ağırlıklı ortalama fiyatından giriş.

## 2. Örneklem

| Yıl | N | P1 | P2 | P3 | bülten | medyan oran | ≥%100 | ≥%500 |
|---|---|---|---|---|---|---|---|---|
| 2015 | 32 | 29 | 14 | 31 | 31 | 17% | 5 | 1 |
| 2016 | 32 | 32 | 29 | 31 | 29 | 36% | 6 | 2 |
| 2017 | 26 | 25 | 25 | 26 | 25 | 25% | 3 | 0 |
| 2018 | 39 | 39 | 38 | 39 | 38 | 50% | 14 | 2 |
| 2019 | 21 | 21 | 21 | 21 | 20 | 37% | 7 | 0 |
| 2020 | 30 | 30 | 30 | 30 | 30 | 77% | 11 | 3 |
| 2021 | 46 | 45 | 44 | 46 | 46 | 84% | 22 | 4 |
| 2022 | 56 | 56 | 55 | 56 | 56 | 122% | 36 | 4 |
| 2023 | 74 | 74 | 73 | 74 | 72 | 150% | 58 | 9 |
| 2024 | 96 | 96 | 96 | 96 | 93 | 291% | 88 | 27 |
| 2025 | 92 | 92 | 91 | 92 | 90 | 320% | 84 | 30 |
| 2026 | 57 | 57 | 57 | 57 | 56 | 238% | 47 | 17 |
| **Toplam** | **601** | 596 | 573 | 599 | 586 | 125% | 381 | 99 |

Tip dağılımı: iç kaynak 426, bedelsiz temettü 156, bedelli+bedelsiz 17, bedelsiz+nakit 2.

Aşamalar arası süre (işlem günü, medyan; parantezde %25–%75):

| Dönem | P1→P2 | P2→P3 | P3→hak | P1→hak |
|---|---|---|---|---|
| Tümü | 13 (4–34) | 40 (23–69) | 4 (3–7) | 69 (50–92) |
| 2015–19 | 29 | 26 | 5 | 62 |
| 2020–23 | 17 | 30 | 4 | 65 |
| 2024–26 | 8 | 64 | 4 | 85 |

2024–26'da SPK onay süresi iki katına çıkmış (64 gün). Onaydan hak gününe ise yalnız 3–4 işlem günü var.

## 3. Tam ızgara: aşama × pencere (pencereler önceden sabitlendi)

CAR = hisse − XU100 toplamı. "β" sütunu beta-düzeltilmiş modeli (α=0) gösterir, "α+β" sütunu tahmin edilmiş piyasa modelini. İkisinin tahmin penceresi P1'den önce [−220,−21] işlem günüdür.

| Aşama | Pencere | N | ort | med | t | isabet | p5 | p95 | β | α+β |
|---|---|---|---|---|---|---|---|---|---|---|
| P1 YK | [−60,−1] | 582 | +9,78% | +4,25% | 6,70 | 59% | −32,1% | +72,8% | +12,51% | +2,63% |
| P1 YK | [−20,−1] | 587 | +5,37% | +2,36% | 6,89 | 58% | −17,1% | +37,1% | +5,91% | +2,65% |
| P1 YK | [−5,−1] | 589 | +1,92% | +0,69% | 5,45 | 56% | −9,9% | +17,1% | +1,95% | +1,14% |
| P1 YK | [0,0] | 590 | +2,41% | +1,22% | 10,39 | 62% | −5,2% | +11,1% | +2,41% | +2,25% |
| P1 YK | [0,1] | 590 | +2,47% | +0,92% | 7,18 | 59% | −8,0% | +19,4% | +2,51% | +2,19% |
| P1 YK | [1,5] | 590 | −0,81% | −1,53% | −1,74 | 38% | −14,5% | +13,2% | −0,54% | −1,35% |
| P1 YK | [1,10] | 590 | −1,11% | −2,47% | −1,78 | 38% | −18,7% | +19,7% | −0,76% | −2,39% |
| P1 YK | [1,20] | 590 | −1,40% | −2,50% | −1,72 | 40% | −24,6% | +25,7% | −0,75% | −3,99% |
| P1 YK | [1,60] | 590 | −1,14% | −3,05% | −0,86 | 44% | −43,7% | +47,1% | +0,56% | −9,18% |
| P2 başvuru | [−20,−1] | 564 | +2,77% | +1,13% | 3,39 | 54% | −20,0% | +34,2% | +3,57% | +0,24% |
| P2 başvuru | [−5,−1] | 565 | +0,44% | −0,13% | 1,10 | 49% | −9,6% | +14,7% | +0,63% | −0,20% |
| P2 başvuru | [0,0] | 565 | +0,91% | +0,43% | 5,17 | 57% | −4,7% | +9,4% | +0,94% | +0,77% |
| P2 başvuru | [0,1] | 565 | +0,83% | +0,41% | 3,23 | 53% | −6,9% | +10,6% | +0,88% | +0,55% |
| P2 başvuru | [1,5] | 565 | −0,83% | −1,26% | −2,07 | 42% | −13,6% | +11,8% | −0,73% | −1,56% |
| P2 başvuru | [1,10] | 565 | −0,69% | −0,85% | −1,26 | 46% | −18,9% | +16,2% | −0,52% | −2,18% |
| P2 başvuru | [1,20] | 565 | −0,99% | −1,39% | −1,30 | 45% | −24,4% | +24,0% | −0,52% | −3,84% |
| P3 SPK onayı | [−20,−1] | 593 | +1,61% | +0,97% | 2,42 | 53% | −17,6% | +26,6% | +2,28% | −0,93% |
| P3 SPK onayı | [−5,−1] | 593 | +1,24% | +0,91% | 3,54 | 57% | −10,0% | +13,6% | +1,37% | +0,57% |
| P3 SPK onayı | [0,0] | 593 | +1,36% | +0,62% | 6,66 | 62% | −5,6% | +9,9% | +1,45% | +1,29% |
| P3 SPK onayı | [0,1] | 593 | +1,28% | +0,54% | 4,56 | 55% | −7,5% | +13,5% | +1,45% | +1,13% |
| P3 SPK onayı | [1,3] | 593 | +0,03% | −0,36% | 0,07 | 48% | −11,4% | +13,7% | +0,09% | −0,39% |
| P3 SPK onayı | [1,5] | 593 | −0,15% | −0,26% | −0,31 | 48% | −15,0% | +15,0% | +0,03% | −0,77% |
| P3 SPK onayı | [1,10] | 593 | −1,26% | −1,54% | −1,92 | 41% | −21,8% | +23,8% | −0,88% | −2,48% |
| P3 SPK onayı | [1,20] | 592 | −2,19% | −2,07% | −2,48 | 43% | −30,0% | +28,9% | −1,46% | −4,68% |
| Hak günü | [−20,−1] | 595 | +3,21% | +2,62% | 4,66 | 57% | −17,6% | +31,6% | +3,98% | +0,77% |
| Hak günü | [−5,−1] | 595 | +2,33% | +1,57% | 5,91 | 61% | −8,9% | +17,0% | +2,48% | +1,68% |
| Hak günü | [−1,−1] | 595 | +0,74% | +0,53% | 4,13 | 58% | −5,0% | +8,3% | +0,76% | +0,60% |
| Hak günü | [0,0] | 595 | +0,40% | −0,18% | 1,89 | 48% | −7,1% | +9,9% | +0,42% | +0,26% |
| Hak günü | [1,5] | 594 | −2,40% | −2,50% | −5,88 | 34% | −17,2% | +13,6% | −2,22% | −3,02% |
| Hak günü | [1,10] | 594 | −3,19% | −3,16% | −5,64 | 36% | −22,9% | +18,7% | −2,89% | −4,49% |
| Hak günü | [1,20] | 594 | −3,30% | −3,94% | −4,04 | 41% | −30,3% | +27,8% | −2,72% | −5,93% |
| Hak günü | [1,60] | 579 | −3,64% | −4,07% | −2,50 | 42% | −46,3% | +45,4% | −1,10% | −10,80% |

Okuma notları:

- **α+β modeli:** Olay öncesindeki yükseliş tahmin penceresine girdiği için α yukarı çıkıyor; bu da sonrasındaki CAR'ı yapay olarak daha negatif yapıyor. Bu yüzden ana ölçü piyasa-düzeltilmiş model, sağlamlık ölçüsü β-düzeltilmiş model.
- **Koşulsuz taban:** Olay hisselerinin 2015–26 koşulsuz ortalama günlük AR'si +0,065%; bu, 20 günde +1,3%, 60 günde +3,9% ediyor. Medyan ise negatif. Dolayısıyla negatif post-olay ortalamaları tabana göre daha da negatif.
- **Kıyas endeksinden bağımsızlık:** XUTUM ve XYUZO (BIST 100 dışı) kıyasıyla sonuçlar aynı: hak [1,10] −3,2% (t=−5,8 / −5,7), P1 [0,1] +2,5%, P3 [1,5] ≈0.

## 4. Sızıntı: duyuru öncesi birikim

| Ön pencere | N | ön CAR ort | [0,1] ort | ön pay (ort) | ön medyan | [0,1] medyan | ön CAR >10% olan |
|---|---|---|---|---|---|---|---|
| [−60,−1] | 582 | +9,78% | +2,45% | 80% | +4,25% | +0,91% | 42% |
| [−20,−1] | 582 | +5,46% | +2,45% | 69% | +2,40% | +0,91% | 31% |
| [−5,−1] | 582 | +1,94% | +2,45% | 44% | +0,71% | +0,91% | 13% |

Koşulsuz taban düşüldüğünde: 20 günlük ön fazla ≈ +4,2%, 60 günlük ≈ +6,0%; duyuru [0,1] ≈ +2,3%. Bu durumda ön pay ≈%65 (20 gün) ve ≈%72 (60 gün).

Anormal hacim (TL hacim / [−120,−21] medyanı) medyanları: P1 öncesi 5 gün 1,37×, P1 t0 2,12×; hak öncesi 5 gün 1,52×. P1 öncesi 5 günde hacmi 2×'i aşan olay payı %32.

| Alt grup | [−60,−1] | [−20,−1] ort / medyan | [0,1] ort / medyan | ön20 payı |
|---|---|---|---|---|
| oran <%100 (N=212) | +6,8% | +2,8% / +0,7% | +1,7% / +0,4% | 62% |
| oran %100–499 (275) | +10,7% | +6,8% / +4,3% | +1,7% / +0,9% | 80% |
| oran ≥%500 (95) | +13,9% | +7,4% / +5,3% | +6,4% / +5,0% | 54% |
| küçük (194) | +6,6% | +3,4% / −0,1% | +3,2% / +1,7% | 52% |
| büyük (190) | +11,8% | +6,2% / +5,4% | +2,1% / +0,4% | 74% |
| 2015–19 (141) | +5,8% | +2,1% / +0,4% | +3,0% / +0,9% | 42% |
| 2020–23 (198) | +13,6% | +6,4% / +3,4% | +2,1% / +0,6% | 76% |
| 2024–26 (243) | +8,9% | +6,6% / +3,8% | +2,5% / +1,5% | 73% |

Yorum: 2020 sonrasında birikimin ¾'ü duyurudan önce gerçekleşiyor. Büyük oranlı ve büyük ölçekli hisselerde ön yükseliş daha belirgin. Hacim artışı sızıntıyla uyumlu. Ama yönetimlerin bedelsizi fiyat yükseldikten sonra ilan etmesi (seçilim) de aynı izi bırakır. Bu ayrım fiyat verisiyle yapılamaz. İşlem açısından sonuç değişmiyor: bilgi kamuya çıktığında fiyatın büyük kısmı zaten içeride.

## 5. Kilit ve işlenebilirlik

t0 günü tavan kilitli olan olay payı: P1 %18 (oran ≥%500'de **%44**), P2 %7, P3 %11 (≥%500'de %21), hak günü %8. 2024–26'da P1'de %23.

| Pencere | t0 kilitsiz (N≈484–547) | t0 tavan kilitli (N≈48–106) |
|---|---|---|
| P1 [0,1] | +0,1% (t=0,3) | +13,4% (t=15,3) |
| P1 [1,20] | −1,6% (t=−2,1) | −0,5% (medyan −5,4%) |
| P3 [0,1] | +0,1% (t=0,4) | +10,6% (t=12,9) |
| hak [0,0] | −0,5% (t=−2,6) | +10,4% |
| hak [1,10] | −2,8% (t=−5,1) | −7,8% (t=−2,6) |

Duyuru etkisinin tamamı, kapanışta alınamayan kilitli günlerde. Kilit açıldıktan sonra giriş (medyan 1, en çok 7 gün gecikme) 5 günde BHAR −1,8% veriyor.

## 6. İşlem simülasyonları (dolabilir giriş/çıkış, BHAR = hisse − XU100 bileşik)

| Kural | N | medyan gün | kilitli giriş | BHAR ort | BHAR med | t | isabet | net BHAR | kilitli hariç ort (t) |
|---|---|---|---|---|---|---|---|---|---|
| YK t0 → +1g | 589 | 1 | 18% | −0,95% | −0,83% | −4,53 | 38% | −1,20% | −0,58% (−3,5) |
| YK t0 → +5g | 589 | 5 | 18% | −1,80% | −1,93% | −4,87 | 35% | −2,05% | −1,19% (−3,2) |
| YK t0 → +20g | 589 | 20 | 18% | −2,09% | −3,25% | −2,86 | 37% | −2,34% | −1,30% (−1,7) |
| YK t0 → hak−1 | 589 | 68 | 18% | +5,09% | −1,61% | 2,73 | 46% | +4,84% | +5,90% (3,1) |
| Başvuru t0 → onay t0 | 509 | 46 | 7% | +4,74% | −0,52% | 2,74 | 48% | +4,49% | +5,20% (2,9) |
| Başvuru t0 → hak−1 | 538 | 47 | 7% | +5,17% | +0,30% | 3,05 | 51% | +4,92% | +5,62% (3,2) |
| Onay t0 → hak−1 | 562 | 3 | 12% | +0,18% | −0,11% | 0,53 | 49% | −0,07% | +0,30% (1,0) |
| Onay t0 → hak | 588 | 4 | 11% | +0,52% | +0,12% | 1,27 | 51% | +0,27% | +0,81% (2,3) |
| Onay t0 AOF → hak−1 | 526 | 3 | — | −0,53% | −0,51% | −1,62 | 44% | −0,78% | |
| Onay t0 AOF → t0 kapanış | 526 | 0 | — | −0,83% | −0,59% | −9,46 | 33% | −1,08% | |
| Hak−1 → hak | 571 | 1 | 4% | +0,35% | −0,15% | 1,50 | 49% | +0,10% | +0,46% (2,2) |
| Hak → hak+5 | 593 | 5 | 8% | −2,78% | −2,72% | −6,69 | 32% | −3,03% | −2,15% (−5,4) |
| Hak → hak+10 | 594 | 10 | 8% | −3,30% | −3,45% | −6,14 | 33% | −3,55% | −2,61% (−5,0) |
| Hak → hak+20 | 594 | 20 | 8% | −3,11% | −4,54% | −3,88 | 38% | −3,36% | −2,22% (−2,9) |
| Onay t0 → hak+10 | 592 | 14 | 11% | −2,36% | −3,34% | −3,44 | 38% | −2,61% | −1,66% (−2,4) |

Takvim-zamanı portföyü: eşit ağırlık, açık pozisyonlar, XU100 fazlası, Newey-West t, net (her girişte 25 bp).

| Kural | aktif gün | ort. pozisyon | yıllık net fazla | t (net) | 2024–26 yıllık net | t |
|---|---|---|---|---|---|---|
| YK t0 → +5g | 1.506 | 2,0 | −99% | −4,6 | −117% | −2,8 |
| YK t0 → hak−1 | 3.166 | 14,3 | +5% | 0,6 | −33% | −2,0 |
| Başvuru t0 → hak−1 | 3.035 | 10,2 | +15% | 1,6 | −24% | −1,7 |
| Onay t0 → hak | 1.693 | 1,8 | +8% | 0,4 | −51% | −1,2 |
| Hak → hak+5 | 1.597 | 1,8 | −191% | −7,5 | −82% | −1,9 |
| Hak → hak+10 | 2.167 | 2,7 | −115% | −6,2 | −45% | −1,5 |

TL engeli karşılaştırması: işlem başına ham getiri − 25 bp − %40/yıl pro-rata.

| Kural | dönem | ham net ort / medyan | engel ort | engeli geçen | (ham net − engel) medyan |
|---|---|---|---|---|---|
| YK t0 → hak−1 | tümü | +12,8% / +2,4% | 11,0% | 40% | −6,5% |
| YK t0 → hak−1 | 2024–26 | +5,2% / −2,7% | 13,0% | 34% | −12,4% |
| Başvuru t0 → hak−1 | 2024–26 | +4,5% / −3,2% | 11,1% | 33% | −10,0% |
| Onay t0 → hak | 2024–26 | −0,6% / −0,7% | 0,6% | 41% | −1,2% |
| Hak → hak+10 | 2024–26 | −1,6% / −1,6% | 1,3% | 37% | −3,0% |

Uzun tutmalı "başvuru/YK → hak−1" sonuçlarının ortalaması pozitif ama medyanı ≈0 veya negatif. Bu sağa çarpık bir piyango profili ve 2020–23'e bağlı: o dönemde başvuru → hak−1 ortalaması +12,4%, 2024–26'da +0,4% (medyan −2,9%). Hak sonrası düşüşü kısa pozisyonla kullanmak ancak VIOP pay vadelisi olan 47 hisseyle mümkün. Bu hisselerde yalnız 31 olay var ve hak [1,10] −1,1% (t=−0,8). Kanıt yok.

## 7. Alt gruplar (ort (t) [medyan])

| Pencere | oran <%100 (N≈220) | %100–499 (≈279) | ≥%500 (≈96) |
|---|---|---|---|
| P1 [−20,−1] | +2,9 (2,5) [+0,7] | +6,6 (5,3) [+3,6] | +7,4 (4,5) [+5,3] |
| P1 [0,1] | +1,7 (4,5) [+0,4] | +1,7 (3,3) [+0,9] | +6,4 (5,5) [+5,1] (%44 kilitli) |
| P1 [1,20] | +1,1 (1,3) [−0,5] | −4,0 (−3,4) [−4,3] | +0,4 (0,1) [−4,1] |
| P3 [−5,−1] | +1,3 (2,7) [+1,1] | +0,5 (0,9) [+0,4] | +3,3 (3,9) [+1,9] |
| P3 [1,5] | +0,2 (0,5) [+0,2] | −0,4 (−0,5) [−1,0] | −0,2 (−0,2) [−0,8] |
| hak [−5,−1] | +1,9 (4,0) [+1,1] | +2,5 (3,9) [+1,8] | +2,8 (2,5) [+1,6] |
| hak [1,10] | −2,3 (−3,0) [−2,6] | −2,9 (−3,4) [−3,4] | **−6,1 (−3,3) [−6,1]** |
| hak [1,20] | −1,6 (−1,2) [−2,4] | −3,3 (−2,9) [−4,6] | −7,2 (−3,0) [−6,5] |

Büyüklük, XU100 seviyesine göre enflasyondan arındırılmış piyasa değeri tertillerine göre (her grup ≈198 olay):

| Pencere | küçük | orta | büyük |
|---|---|---|---|
| P1 [0,1] | +3,2 (5,4) [+1,8] | +2,0 (3,5) [+0,8] | +2,2 (3,7) [+0,5] |
| P3 [0,1] | +2,5 (5,3) [+1,4] | +0,5 (1,1) [+0,3] | +0,8 (1,7) [+0,0] |
| hak [1,10] | −2,8 (−2,9) [−3,5] | −4,3 (−4,6) [−3,6] | −2,5 (−2,5) [−2,2] |

| Pencere | 2015–19 (N≈148) | 2020–23 (≈204) | **2024–26 (≈243)** |
|---|---|---|---|
| P1 [−20,−1] | +2,2 (2,2) | +6,1 (4,2) | +6,6 (5,1) [+3,8] |
| P1 [0,1] | +3,0 (4,2) | +2,1 (3,7) | +2,5 (4,5) [+1,5] |
| P1 [1,20] | +1,1 (0,6) | −1,5 (−1,1) | −2,8 (−2,3) [−3,3] |
| P3 [0,1] | +0,6 (1,4) | +2,3 (4,1) | +0,8 (2,0) [+0,3] |
| P3 [1,5] | +0,2 (0,3) | −0,5 (−0,5) | −0,1 (−0,1) [−0,9] |
| hak [−5,−1] | +1,5 (2,2) | +3,9 (4,8) | +1,5 (2,8) [+1,3] |
| hak [1,10] | −4,4 (−4,9) | −4,7 (−4,4) | −1,2 (−1,3) [−1,9] |

Yıllık hak [1,10] ortalaması 12 yılın 12'sinde de negatif (−0,4% ile −5,7% arası; 2024 −0,5%, 2025 −0,4%, 2026 −3,6%). P1 [0,1] her yıl pozitif (+0,5% ile +4,1%). İkisi de tutarlı, ama ilki kısa pozisyon ister, ikincisi kilit nedeniyle alınamaz.

## 8. Hızlı bakış: bedelli ve nakit temettü

**Bedelli (rüçhan hakkı), N=290** (P1 yalnız KAP özetinden, 268 olay):

| Pencere | ort | med | t | isabet |
|---|---|---|---|---|
| P1 [−5,−1] | +1,4% | −0,3% | 2,4 | 47% |
| P1 [0,0] | −2,3% | −3,1% | −5,9 | 29% |
| P1 [0,1] | −2,8% | −4,1% | −4,6 | 28% |
| P1 [1,20] | −0,3% | −4,2% | −0,2 | 39% |
| hak [0,0] | +1,4% | −0,3% | 2,5 | 48% |
| hak [1,10] | +1,1% | −0,3% | 1,0 | 49% |

Duyuru negatif, 2024–26'da da aynı (−2,7%). Hak günü ve sonrasında anlamlı ve tutarlı bir drift yok.

**Nakit temettü, N=2.134** (P1 = ilk KAP "Kar Payı Dağıtımı" bildirimi, 1.859 olay).

Duyuru verimi = brüt temettü / duyurudan önceki kapanış (ileriye bakış yok).

| Kural | verim | dönem | N | medyan gün | BHAR ort | BHAR med | t | isabet | net |
|---|---|---|---|---|---|---|---|---|---|
| Duyuru t0 → hak−1 | <%2 | tümü | 829 | 40 | +3,4% | −2,0% | 2,6 | 44% | +3,2% |
| Duyuru t0 → hak−1 | %2–5 | tümü | 597 | 30 | +5,0% | +1,5% | 5,0 | 56% | +4,7% |
| Duyuru t0 → hak−1 | **≥%5** | tümü | 400 | 28 | **+8,5%** | +6,5% | 11,1 | 74% | +8,2% |
| Duyuru t0 → hak−1 | ≥%5 | 2024–26 | 67 | 22 | **+14,4%** | +11,7% | 7,6 | 85% | +14,1% |
| Duyuru t0+5 → hak−1 | ≥%5 | tümü | 400 | — | +7,3% | +5,2% | 10,4 | 76% | |
| Duyuru t0 → hak−3 | ≥%5 | 2024–26 | 67 | — | +11,9% | +9,2% | 6,9 | 81% | |
| hak−10 → hak−1 | ≥%5 | tümü | 422 | 9 | +3,5% | +2,7% | 8,7 | 68% | +3,2% |
| hak → hak+5 | ≥%5 | tümü | 421 | 5 | −2,1% | −2,1% | −7,7 | 33% | −2,4% |

Sağlamlık (verim ≥%5, t0 → hak−1):

- **Yıllar:** Her yıl pozitif. 2015 +4,3%, 2019 +6,7%, 2023 +13,8%, 2025 +17,0%, 2026 +14,3%.
- **Kıyas endeksi:** XUTUM kıyasıyla +8,2%, XYUZO kıyasıyla +7,6%.
- **Büyüklük:** küçük +9,7%, orta +7,1%, büyük +7,5% (medyan +7,4%).
- **Kilit bilgisi:** Kilit bilgisi olan hisselerde +8,1%, yalnız ChartData olanlarda +9,1%.
- **Verim eşiği:** Eşik ≥%3'te +7,3%, ≥%8'de +10,7%.
- **Takvim-zamanı:** Net +56%/yıl XU100 fazlası (t=5,1); 2024–26'da +91%/yıl (t=4,1). Ortalama 7 eşzamanlı pozisyon; aktif gün oranı %70; Şubat–Mayıs yoğunlaşması var.
- **Ham fiyat kontrolü:** TTRAK 2025'te ham kapanış 660 → 816,5 (XU100 −2%); NUHCM 2026'da 219 → 328 (düzeltilmiş). Etki düzeltme hatası değil.

Uyarılar:

- Temettü listesi gerçekleşmiş ödemelerden oluşuyor; iptal edilen teklifler örnekte yok (hafif hayatta kalan yanlılığı).
- Teklif edilen tutar genel kurulda değişebilir.
- Duyuru çoğu zaman yıllık sonuçlarla aynı dönemde; etki bir kısmen kazanç sürprizi olabilir.
- Hisselerin %29'unda tavan kilidi bilgisi yok.
- Likidite ve kalabalıklaşma riski var.
- Hak−1'de satıldığında stopaj meselesi yok. Hak gününden sonra 5 günde −2,1% düştüğü için tutmak da kötü.

**Öneri:** Bu kural ayrı bir ajanca bağımsız veriyle yeniden test edilmeli: KAP teklif metninden temettü tutarı, sektör ve kazanç kontrolü, işlem hacmi filtresi. Bu ajanın görev kapsamı dışında kalan en güçlü bulgu bu.

## 9. Literatürle uyum (kısa)

- Türkçe çalışmalar 2012–17 döneminde duyuru günü pozitif AR ve SPK onayından 2–5 gün sonra negatif AR buluyor ([DergiPark 452850](https://dergipark.org.tr/en/download/article-file/452850), [MAKÜ İİBF 439219](https://dergipark.org.tr/en/pub/makuiibf/article/439219)).
- 2015–17 için duyuru sonrası anormal getiri elde edilemediğini söyleyen bir tez de var ([Yaşar Üniv.](https://gcris.yasar.edu.tr/handle/123456789/234)).
- Bu çalışma 2015–26 için bu bulguları çok daha büyük bir örneklemle (N≈595) teyit ediyor. Ek olarak tavan kilidinin duyuru etkisini nasıl işlenemez kıldığını ve hak sonrası düşüşü gösteriyor.

## 10. Sınırlamalar

1. **Yalnız kapanış ve AOF var.** Açılış fiyatı yok. Akşam yayımlanan bilgide açılış boşluğu ölçülemedi; t0 AOF girişi gün içi en iyi yaklaşım.
2. **Tavan kilidi bir yaklaşım:** getiri ≥%9 ve kapanış = en yüksek fiyat. Kısmi dolumlar ve fiyat adımı etkileri yok sayıldı.
3. **Bülten yayım saati:** 2014–21 bültenlerinin saati bilinmiyor; 18:30 varsayıldı. 2022+ verisine göre %98'i 18:00 sonrası, yani muhafazakâr bir varsayım.
4. **Toplam getiri ile fiyat endeksi:** Getiri temettü dahil, XU100 ise fiyat endeksi. XU100 temettü verimi, 20 günde yaklaşık +0,3% yukarı yanlılık demek.
5. **P2 tanımı:** Bazı olaylarda YK kararı ile başvuru aynı bildirimde (P1 = P2).
6. **P1 seçimi:** P1 ilk kamu bilgisi. Sonradan revize edilen kararlarda ilk plan farklı olabilir; olayların %22'sinde P1 son YK tarihinden önce.
7. **KAP detay kapsamı:** 2.382 aday detayın 1.638'i okundu (önce belirsiz olanlar). Kalanlar yalnız özetle sınıflandı. KAP 1 sn aralıklı isteklere 429 verdi; tempo 2,5–3 sn'ye düşürüldü.
8. **Büyüklük:** Göreli büyüklük log(piyasa değeri / XU100); TL enflasyonuna karşı kaba bir arındırma.
9. **Kalabalıklaşma:** 2024–26'da bedelsiz sayısı ve oranları rekor seviyede; kalabalıklaşma ve SPK süresinin uzaması etkileri değiştirmiş olabilir.

## 11. Dosyalar ve yeniden üretim

Kod: `hesaplar/olay_bedelsiz/`. Önbellek repoda değil, `scratchpad/data/bedelsiz/` altında. Sıra şöyle:

- `f01_isy_sermaye.py`: Is Yatırım sermaye artırımı tabloları
- `f02_kap_meta.py`: KAP aylık metadata (CA, KPD)
- `f03_fiyat.py`: HisseTekil ve ChartData fiyatları
- `f04_kap_detay.py`: KAP detay sayfaları
- `f05_spk_bulten.py` → `f06_spk_parse.py`: SPK bültenleri
- `f07_olaylar.py`: olay listesi
- `f08_bedelli_temettu.py`: bedelli ve temettü olay listeleri
- `f09_dogrula_duzeltme.py`: bölünme düzeltmesi doğrulaması
- `f10_panel.py`, `f20_es.py`: getiri paneli ve olay çalışması motoru
- `f30_analiz.py`, `f31_calistir.py`: CAR ızgarası
- `f32_islemler.py`: işlem simülasyonları
- `f33_ek.py`: örneklem, süreler, sızıntı, sağlamlık
- `f40`/`f41`/`f42`: bedelli ve temettü

Türetilmiş olay listesi (601 olay; P1/P2/P3/hak zamanları, kaynak, bülten no): `hesaplar/olay_bedelsiz/olaylar_bedelsiz.csv`. Otomatik tablolar: `scratchpad/data/bedelsiz/sonuc/*.md`.
