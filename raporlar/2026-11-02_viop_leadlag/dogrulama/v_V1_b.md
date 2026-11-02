# v_V1_b: İkinci bağımsız doğrulama (çürütme aşaması). Kredi notu değişikliği sonrası kontraryen strateji
Doğrulayıcı: V1_b · 02.11.2026 · Kod: `out/code_v_V1_b/` (vb.py, b1_core.py … b6_checks.py; loglar log_b1..b6.txt; olay listeleri events_b.csv, events_xc.csv)
Bağımsızlık: ll.py, olib.py ve 1. aşama kodu import edilmedi. Ham parquet dosyaları `ldate` ile indekslendi. BIST takvimi XU100'den alındı. FX düzeltmesi kendi kodumda (bar t+1'in c değeri). VİOP bültenleri kendi ayrıştırıcımla okundu.

## 0. Hüküm: DÜZELT. Güven ORTA'dan DÜŞÜK'e iniyor
- **Örneklem içi rakamlar doğru.** Ondalığına kadar tekrar edildi: 20 olay, XU100 +207,9 bps, t 3,77.
- **Örneklem içi sağlamlık güçlü.** Plasebolar, yerel taban, faktör kontrolü (TL), VİOP ve madencilik düzeltmeli max-t testini (p=0,014) geçiyor.
- **Ama iddianın ileriye dönük geçerliliğini destekleyen bağımsız kanıt yok:**
  1. **Gerçek örneklem dışı, Türkiye 2000–2013 (n=21):** Etki sıfır (+8 bps net, t 0,10; plasebo p=0,48). Olay öncesinde fiyat not yönünde güçlü hareket etmiş (351 bps, t 2,75), ama geri dönüş yok.
  2. **Dış geçerlilik, takvimli Cuma not değişiklikleri (Güney Afrika + Yunanistan + İtalya, n=39):** −36 bps (t −0,7). Volatiliteye göre ölçeklenince −0,11 SD; Türkiye +0,84 SD. Türkiye büyüklüğünde bir etki z=4,5 ile reddediliyor. İtalya'da ters yönde: −201 bps, t −2,2.
  3. **Ortak faktör:** Aynı tarihlerde, Türkiye'nin not yönüyle işaretlenmiş EEM +105 bps (t 3,3; tarih plasebosu p=0,005). Türkiye EEM'in yaklaşık %1'i olduğundan bu hareket Türkiye'nin notundan kaynaklanamaz; büyük olasılıkla tesadüf ya da bulaşma.
     - USD bazında Türkiye'ye özgü kısım: TUR−β·EEM = +97 bps (t 1,74). IS +81 (t 1,0), OOS +113 (t 1,35); ikisi de anlamsız.
  4. **Mekanizma desteklenmiyor:** Görünüm değişikliklerinde etki yok (+11, t 0,16). Takvim dışı 3 olay negatif. Olay öncesi 5 günlük hareket anlamsız (t 1,4–1,9) ve geri dönüşü öngörmüyor.
  5. **Aile düzeyinde çoklu test:** 1. tur yaklaşık 10 olay ailesini taradı ve bu sonucu en iyi bulgu olarak seçti. Izgara düzeltmeli p=0,014'e aile düzeyinde Bonferroni uygulanınca p ≈ 0,14.

**Sonuç:** Bu bulgu bir "anomali" değil, örneklem içi bir olgu; ileriye dönük beklenti ihtiyatlı olmalı. Kâğıt üstünde ileri test önerilir (yılda ~2 olay; ilk anlamlı sonuç için yıllar gerekir).

## 1. Olay tarihleri (birincil/ikincil kaynak denetimi)
Ajansların kendi siteleri giriş duvarlı ya da JS ile yükleniyor. Bu yüzden ajans bültenlerini aktaran haberler (Bloomberg/Reuters başlıkları, AFP), Türk bankalarının KAP/IR duyuruları, CNN Türk not karnesi zaman çizelgesi, TradingEconomics S&P tablosu ve countryeconomy kullanıldı.
- **2014+ 20 tepki günü doğrulandı:** 17'si Cuma akşamı, 3'ü hafta içi takvim dışı (S&P Çar 20.07.2016, Moody's Çar gece 07.03.2018, S&P Sal 01.05.2018). Hepsi not kademesi değişikliği; görünüm değişikliği dahil değil. 17.08.2018'deki S&P ve Moody's kararları tek olay sayıldı.
- **1. aşama düzeltmeleri teyit edildi:** Fitch 11.02.2022 indirimi eklendi; 08.07.2022 kararı B+→B. Moody's 07.03.2018 için "late Wednesday, surprise" (intellinews, Reuters). S&P 01.05.2018 için "not part of regularly scheduled reviews" (Reuters).
- **2026'da not değişikliği yok:**
  - Moody's 23/24.01.2026 periyodik değerlendirmede işlem yapmadı (Hürriyet DN, ntv, cnbce).
  - S&P 17.04.2026'da BB-/durağanı teyit etti, 16.10.2026'da değerlendirme yayımlamadı (foreks).
  - Fitch 23.01.2026'da görünümü pozitife çevirdi, 10.04.2026'da durağana geri aldı.
- **2000–2013, 21 olay:** CNN Türk zaman çizelgesi ile TE S&P tablosu ve countryeconomy Fitch/Moody's satırları tutarlı. Ayrıca Bloomberg 16.05.2013, Al Arabiya 05.11.2012, invest.gov.tr 20.06.2012, Reuters/investing 08.01.2010 ve centralbanking 03.12.2009 haberleriyle doğrulandı.
  - Belirsiz kalanlar: Fitch 27.04.2000 (countryeconomy'de 21.09.2000) ve S&P 16/17.04.2001 (geç tarih kullanıldı).
  - Bu dönemde AB CRA takvimi yoktu ve açıklama saatleri bilinmiyor. Bu yüzden muhafazakâr giriş kuralı kullanıldı: ilan gününden sonraki ilk seansın kapanışı.

## 2. Bağımsız tekrar (b1)
| Küme (20 olay, açılış → t+2 kapanış, 15 bps) | Ortalama | Medyan | t | İsabet |
|---|---|---|---|---|
| XU100 | +207,9 | +160,7 | 3,77 | %85 |
| XU100 IS 2014–20 (n=10) | +182,5 | | 2,53 | %80 |
| XU100 OOS 2021–26 (n=10) | +233,3 | | 2,69 | %90 |
| XU030 | +211,8 | | 3,48 | %75 |
| XBANK | +302,5 | | 3,47 | %70 |
| Kapanış t0 → t+2 (işlenebilir, açılıştan bağımsız) | +146,7 | +171,6 | 3,55 | %80 |

- **Günlük profil (işaretli, brüt):**

  | Bileşen | bps | t |
  |---|---|---|
  | Pazartesi gap | −30 | −1,1 |
  | Pazartesi gün-içi | +61 | 1,4 |
  | t+1 | +71 | 2,96 |
  | t+2 | +91 | 2,77 |
  | t+3 | −1 | — |
  | t+4 | −6 | — |

- **Açılış fiyatı ve bid-ask sıçraması:**
  - corr(gap, gün-içi): olay günlerinde 0,05, 2014+ tüm günlerde −0,045. Mekanik negatif korelasyon yok.
  - Strateji yönünü gap belirlemiyor, not belirliyor; açılış gürültüsü yalnız varyans ekler.
  - Getirinin çoğu açılıştan bağımsız: kapanış girişi +147, VİOP uzlaşma +152.

## 3. Plasebo ve veri madenciliği (b1, b2)
- **İşaret çevirme:** p=0,00018. **Etiket permütasyonu:** p=0,001. **Bağımsız tarih kaydırma** (±3..52 hafta, aynı gün): p=0,00025 (plasebo ortalaması +19, sd 61).
- **Izgara max-t testi:** 33 varyant (giriş {açılış, kapanış} × vade {0,1,2,3,5,10} × endeks {XU100, XU030, XBANK}). Gerçek max|t| 4,04; plasebo %95'lik dilimi 3,33, %99'luk dilimi 4,17. **Madencilik düzeltmeli p=0,014.**
- **Sabit kaydırma profili (−26..+26 hafta):**
  - k≠0 ortalaması +22 bps; 52 kaydırmanın hiçbiri gerçek değere (+223) ulaşmıyor.
  - +2 ve +3 hafta kaydırmaları +106 ve +139 (t 2,0 ve 2,75): sınırlı bir rejim bileşeni var.
  - Yerel taban (±1..6 hafta aynı pencere) çıkarılınca +190..+203 bps (t 3,5–3,85). Rejim açıklaması çürüdü.
- **Kümeleme:** Yıl ortalamalarıyla t 3,58 (n=8); epizot ortalamalarıyla t 6,2 (n=5).
- **Uç değerler:**
  - En iyi 1 / 3 / 5 olay hariç: +174 / +137 / +105 (t 3,8 / 3,2 / 2,5).
  - %10 kırpılmış ortalama: +190 (t 4,65).
  - Wilcoxon p=0,0002.

## 4. Ortak faktör ve başka piyasa plasebosu (b3, b4, b6)
- **Türk tarihleri ve yönleri başka piyasalara uygulandı** (Pzt açılış → t+2, brüt):
  - ABD'de işlem gören USD ETF'leri: EEM +105 (t 3,33), EZA +128 (t 2,94), EWY +100 (t 2,63), GREK +94 (t 2,53), EWG +70 (t 2,0).
  - Yerel para birimli endeksler (^BVSP, ^MXX, ^J203.JO, ^STOXX50E, ^GDAXI, FTSEMIB): −14..+43, anlamsız.
  - Yani ortak bileşen büyük ölçüde USD/küresel GOP hareketi.
  - EEM tarih plasebosu: p=0,005. Olay öncesinde EEM'de not yönünde stres yok (+46, t 1,0). Genel bir "stres sonrası GOP geri dönüşü" açıklaması tutmuyor.
- **Faktör ayarlı XU100 (TL):**
  - Açılış → t+2 − β_Dimson(0,47)·EEM: +161 (t 3,14).
  - Kapanış → t+2, STOXX + EEM Dimson faktörleri: +104 (t 2,52); faktörün açıkladığı kısım +43 (t 2,58).
  - Olaylar arası regresyon: XU100 = 0,72·EEM + 147 (t 2,9).
- **USD, aynı saat:**
  - TUR −β(0,71)·EEM: +97 (t 1,74), medyan +55, isabet %60.
  - Sadece Cuma (n=17): +116 (t 2,04).
  - IS +81 (t 1,0), OOS +113 (t 1,35).
- **Değerlendirme:** Türkiye'ye özgü kalıntı pozitif, ama USD bazında istatistiksel olarak sınırda. Ham +208'in yaklaşık %25–45'i küresel faktörle çakışıyor.

## 5. Gerçek örneklem dışı test, Türkiye 2000–2013 (b3, b6)
21 olay (5 indirim, 16 artırım). Bu olaylar 1. turda hiç kullanılmadı. 2014 öncesi açılış verisi bozuk olduğundan kapanış girişleri kullanıldı.

| Kural (XU100, kontraryen) | Ortalama | t | n |
|---|---|---|---|
| A: c[t0] → c[t+2], net 15 bps (kesin işlenebilir) | +8 | 0,10 | 21 |
| A, yerel taban çıkarılmış (brüt) | +45 | 0,57 | 21 |
| A, ±60 gün trend çıkarılmış (brüt) | +39 | 0,46 | 21 |
| A, 2003–13 (2001 krizi hariç) | −11 | −0,13 | 15 |
| A, 2009–13 (n=7, hepsi artırım) | +71 | 0,77 | 7 |
| B: ilan günü kapanışı → +2 (saat bilinmiyor, ileriye bakma riski) | +75 | 1,32 | 21 |
| Tarih plasebosu, A | p=0,48 | | |
| Olay öncesi 5 gün (not yönünde) | 351 bps | 2,75 | 21 |

**Sonuç:** Takvimsiz dönemde olay öncesi fiyatlama var, ama sonrasında geri dönüş yok. "Önceden fiyatlanır, sonra haberle satılır" mekanizması bu dönemde çalışmıyor. Karşı argüman: dönem farklı (takvim yok, sürpriz kararlar, 2003–13 boğa piyasasında artırımlar). Bu nedenle bulguyu doğrudan çürütmüyor, ama genellemeyi desteklemiyor.

## 6. Dış geçerlilik: başka ülkelerin not değişiklikleri (b5, b6)
Olay listesi `events_xc.csv` (72 olay; countryeconomy + Bloomberg, AFP, BizNews ile doğrulama). Kural: ilandan sonraki ilk seansın açılışı → t+2 kapanış, kontraryen, 15 bps. ^J203.JO açılışı bozuk, yani fiilen önceki kapanış.

| Küme | n | Yerel endeks | USD ETF | ETF − β·EEM |
|---|---|---|---|---|
| Güney Afrika, takvimli | 8 | +82 (t 1,28) | +27 | +43 |
| Yunanistan, takvimli (22 artırım) | 23 | −20 (t −0,27) | +44 (t 0,76) | +26 |
| İtalya, takvimli | 8 | **−201 (t −2,23)** | −199 (t −3,1) | −97 (t −2,2) |
| **Havuz takvimli (GA+YU+İT)** | **39** | **−36 (t −0,72)** | −9 | +4 |
| Brezilya, takvim dışı | 12 | −8 | −3 | −1 |

- Volatilite ölçekli (sinyalli getiri / önceki 60 günün 3 günlük sd'si):
  - Türkiye +0,84 SD (t 4,05).
  - Havuz −0,11 SD (SE 0,21); fark z=4,5.
  - Test güçlü: Türkiye büyüklüğünde bir etki olsaydı yakalanırdı.
- İtalya tarihlerinde de EEM −162 (t −2,2) hareket etmiş. n≈10–20 olayda ±2–3 t'lik küresel faktör tesadüfleri olağandışı değil. Bu, Türkiye'deki EEM çakışmasının tesadüf olma ihtimalini makul kılıyor.

## 7. İşlenebilirlik (b4)
- **Kendi VİOP ayrıştırmam** (F_XU030 en aktif kontrat, t0 uzlaşma → t+2 uzlaşma, 4 bps): **+152 (t 3,10, n=17; 2016 olayları bülten öncesi)**. Sadece Cuma: +178 (t 3,67, n=15).
- **09:30 VİOP açılış seansı fiyatıyla giriş** (alan 2022-10'dan beri var, n=7): +376 (t 2,8). 2022-10-03 hariç ~+262. Gerçek bir müzayede dolumuyla da sonuç bozulmuyor.
- **Not:** Akşam seansı Pazartesi işlem gününe sayıldığından bülten "ACILIS FIYATI" Cuma akşamı ilandan önce olabilir. Bu yüzden kullanılmadı.
- **Saatlik ilk bar** (2024+, n=6, brüt): açılış girişi +186, ilk bar kapanışı (~10:30 TSİ) +149, 2. bar +136. Bir saat gecikme yaklaşık 40 bps kaybettiriyor.
- **Likidite:** Ön vade F_XU030 olay günlerinde 140 bin–600 bin sözleşme; 4 bps maliyet makul. F_XLBNK illikit (1. aşama).

## 8. Kalan sorunlar
1. **Örneklem dışı yok:** 2000–13 Türkiye (n=21) ve 3 başka ülke (n=39) ile tekrar etmiyor.
2. **Seçim yanlılığı:** Kontraryen yön, t+2 vadesi ve "takvimli / sadece Cuma" alt kümesi tam örneklem görüldükten sonra seçildi. Aile düzeyi p ≈ 0,14.
3. **Küresel faktör çakışması:** EEM +105 (p 0,005). USD bazlı Türkiye'ye özgü kısım t 1,7.
4. **Mekanizma desteklenmiyor:** Görünüm değişikliklerinde etki yok, takvim dışı olaylar negatif, olay öncesi hareket geri dönüşü öngörmüyor.
5. **Yoğunlaşma:** En iyi 5 olay ortalamanın ~yarısını veriyor. 2022-10-03 (TÜFE günü) tek başına +865.
6. **Olay seyrekliği:** 2026'da hiç not değişikliği olmadı. İleri test için yıllar gerekir.

## 9. TradingView
BIST:XU100, BIST:XU030, BIST:XBANK, BIST:XU0301! (? VİOP sürekli kontrat), NASDAQ:TUR, AMEX:EEM (faktör kontrolü).
