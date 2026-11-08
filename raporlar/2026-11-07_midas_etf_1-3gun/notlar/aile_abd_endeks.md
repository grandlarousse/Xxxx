# Aile: abd_endeks (ABD geniş endeks, kaldıraçlı/ters, faktör ve temettü ETF'leri)

Hazırlanma: 07.11.2026. Veri: 2016-11-07..2026-11-06 (IS = 2016-11..2021, OOS = 2022..2026-11). Kod: `kod/ajan_abd_endeks/`,
tablolar: `sonuclar/aile_abd_endeks/`, makine okunur sonuç: `sonuclar/aile_abd_endeks/sonuc.json`.
Bu bir geçmiş veri testidir (backtest). Geçmiş sonuç gelecekteki getiriyi garanti etmez; yatırım tavsiyesi değildir.

## 0. Kısa sonuç

* **Eşiği geçen ve aile genelinde tutarlı tek etki: "zayıf kapanış dönüşü".** Kural: gün düşüşle kapanır ve kapanış günün dibine
  çok yakındır (IBS = (kapanış−düşük)/(yüksek−düşük) < 0,10). Sonra 3 işlem günü long tutulur.
  * **S1, SPY** (C1: t+1 kapanışında al, t+4 kapanışında sat): n=155, brüt 69 bp, net 56 bp (2.500 $ pozisyonla), t=2,79,
    IS 78 / OOS 40 bp, yılların %100'ü pozitif, maxDD −%12, en kötü işlem −%6,8.
  * **S2, QQQ** (aynı kural): n=169, net 71 bp, t=3,46, IS 76 / OOS 66 bp, C0/O1/C1 modlarının üçünde de t>2,9.
  * SPY ve QQQ sinyallerinin %73'ü aynı gün geliyor. S1 ile S2 iki ayrı fırsat değil, aynı fırsat kümesinin iki aracı.
* **Güven "orta".** İki yönlü birleşik BH-FDR'yi geçiyor. Katı tek yönlü BH'de ise (17.391 test, yalnız "net>0" hipotezi)
  hiçbir satır geçmiyor; odaklı hipotez setimde (1.056 test) yalnız QQQ satırları geçiyor. Kanıtın ağırlığı tek bir testte değil,
  aile içindeki tutarlılıkta. 19 grup temsilcisinin 19'unda net pozitif, üç giriş modunun hepsinde brüt pozitif, komşu IBS
  eşiklerinde (0,05-0,30) hem IS hem OOS pozitif.
* **Etki piyasa geneli zayıf kapanışlarda yoğunlaşıyor.** 19 temsilcinin en az 10'u aynı gün sinyal verdiğinde gün ortalaması
  net 94 bp (t=3,55). Yalnız 1-10 ETF sinyal verdiğinde sonuç ≈0. Bu yüzden sinyal SPY'dan (ya da QQQ'dan) alınmalı,
  faktör ETF'lerinin tek başına verdiği sinyaller işlenmemeli.
* **S3 (düşük güven, kapanışa bağımlı).** Kural: 3 ardışık düşen kapanıştan sonra al, ilk yükselen kapanışta sat (en çok 3 gün).
  SPY'da C0 modunda net 34 bp, t=2,32. Yalnız SPY ve QQQ'da çalışıyor. IS döneminde zayıf (t=0,48), birleşik FDR'yi geçmiyor.
* Pre-FOMC, CPI/NFP günü, OPEX haftası, ay dönümü, tatil öncesi, Turnaround Tuesday, VIX sıçraması, IWM'in SPY'ı yetişmesi,
  faktör çifti göreli dönüşü ve ters ETF ile kısa yön: hepsi eşik altında ya da net negatif.
* **Doğrulanmış gecikmeli öncü yok.** Ailenin 2.636 hedef×öncü satırında BH-FDR'yi geçen 0. ES1!/NQ1!/RTY1! vadelileri
  öncü değil, gerçek zamanlı izleme aracıdır: ETF kapalıyken işler ve açılış boşluğunu önceden gösterir.
* **Kaldıraçlı ETF'ler aynı sinyalle çalışıyor.** Sabit komisyonda (emir başına 1,5 $) tek avantajları sermaye verimliliği.
  Kuyruk riski 2-3 kat. S1/S2 işlemlerinde tek işlemde SPXL'de −%23, TQQQ'da −%31 kayıp yaşandı.
  **Ters ETF'ler yalnız koruma amaçlı kullanılabilir.**

## 1. Yöntem

* **Zamanlama.** `kod/lib.py` sözleşmesine uyuldu. Sinyal t kapanışına kadar bilinen veriyle hesaplanıyor. Olay takvimleri
  önceden bilindiği için kullanıldı. Giriş modları:
  * C0: t kapanışı. Pratikte kapanıştan dakikalar önce emir verilir; sinyal kapanış fiyatına dayandığı için hafif iyimser.
  * O1: t+1 açılışı.
  * C1: t+1 kapanışı. En temiz mod.
  * Çıkış: girişten h işlem günü sonraki kapanış. İşlemler çakışmıyor: pozisyondayken gelen sinyal yok sayılıyor.
  * Tüm hesaplar toplam getiri (temettü dahil) düzeltmeli fiyatlarla yapıldı.
* **Maliyet.** `lib.cost_bp`: 2 × 1,5 $ komisyon + likidite kademesine göre makas. Çekirdek ETF'lerde 2.500 $ pozisyonda
  13-14 bp. Duyarlılık için 1.000 $ (30 bp + makas) ve 10.000 $ (3 bp + makas) da hesaplandı.
* **Kopya grupları.** 2022-06..2026-11 günlük getiri korelasyonu |r|>0,97 olan çiftler (`kopya_ciftleri.csv`, 139 çift)
  kullanıldı. Sonuçta 55 ETF 27 gruba ayrıldı (`ae.GROUPS`).
  * Aile içi tutarlılık yalnız grup temsilcilerinde sayıldı: 6 çekirdek (SPY, QQQ, IWM, DIA, RSP, MDY) ve 13 faktör/temettü
    (IWF, IWD, SCHD, SPLV, SPHB, MTUM, QUAL, VLUE, IWO, IWN, COWZ, JEPI, QYLD).
  * VOO/IVV/VTI ile SPY, QQQM ile QQQ ve kaldıraçlı kopyalar bağımsız kanıt sayılmadı.
  * Faktör ETF'leri de SPY ile 0,8-0,97 korelasyonlu. Etkin bağımsız dayanak sayısı en fazla 3-4: büyük ölçek, teknoloji,
    küçük ölçek, değer/defansif.
* **Test sayısı.** Toplam 18.127 test:
  * genel kütüphanenin aile satırları: 16.335;
  * `03_hipotezler.py`: 1.056;
  * lead-lag: kontrollü yetişme 616, yetişme backtest'i 80, reel faiz 16, TIP 24.
  * Ayrıca 144 sağlamlık yeniden değerlendirmesi yapıldı (komşu parametreler ve kaldıraçlı araçlar) ve 10 adet sonradan bakılan
    "SPY sinyaliyle diğer ETF" satırı eklendi. Bunlar yeni hipotez değil.
* **FDR.**
  * İki yönlü BH (q=0,10), birleşik küme: eşik p≤0,0102, 1.846 satır geçiyor. Geçenlerin çoğu NEGATİF satır: ters ETF'ler,
    kapalı alım fonları ve dar hareketli ETF'lerde maliyet nedeniyle anlamlı zarar. Bu satırlar eşiği gevşetiyor.
  * Bu yüzden ek olarak katı tek yönlü BH uygulandı ("net>0" hipotezi). Sonuçlar Bölüm 0'da.
* **Kabul eşiği:** görev tanımındaki eşik uygulandı (net>0, t≥2, IS ve OOS>0, yılların ≥%60'ı pozitif, n≥40, O1 ya da C1'de
  brüt>0). Parametre taraması yapılmadı. Komşu parametreler yalnız kararlılık göstermek için raporlandı.

## 2. İşlenebilirlik (tablo: `islenebilirlik.csv`)

| Grup | En iyi araç | Medyan $ hacim | Maliyet (2.500 $) | 1 günlük σ | Maliyet/σ | Not |
|---|---|---|---|---|---|---|
| S&P 500 | SPY | 41,6 mlr | 13 bp | 85 bp | 0,15 | VOO/IVV/VTI kopya |
| Nasdaq-100 | QQQ | 30,1 mlr | 13 bp | 134 bp | 0,10 | QQQM kopya |
| Russell 2000 | IWM | 7,8 mlr | 13 bp | 117 bp | 0,11 | |
| 3x S&P | SPXL | 526 mn | 14 bp | 256 bp | 0,055 | UPRO kopya; 3 günde ~7 bp kaldıraç kaybı |
| 3x NDX | TQQQ | 4,7 mlr | 14 bp | 396 bp | 0,035 | 3 günde ~16 bp kaldıraç kaybı |
| 3x R2K | TNA | 405 mn | 14 bp | 349 bp | 0,040 | URTY kopya |
| Ters (−1x..−3x) | SH, PSQ, SQQQ, SPXU, TZA… | 53 mn-2,6 mlr | 14-18 bp | | | −3x'te 3 günde 13-33 bp kayıp |
| Temettü / düşük vol / kapalı alım | SCHD, SPLV, USMV, JEPI, XYLD… | 27-680 mn | 14-20 bp | 54-80 bp | 0,20-0,37 | 1-3 gün için dar |

Kaldıraç kaybı formülü (L²−L)/2·σ²; σ olarak dayanağın son 1 yıllık oynaklığı kullanıldı.

**PTP/K-1 riski.** Bu ailede PTP/K-1 ürünü yok. Kaldıraçlı ve ters ürünler (ProShares, Direxion) 1940 Yasası kapsamındaki ETF'ler.
Buna karşın bu ürünlerin Midas'ta bulunurluğu resmî olarak doğrulanamadı: TQQQ "muhtemel" (`notlar/midas_kosullari.md`).

## 3. Genel kütüphane: aile içi tutarlılık (`genel_aile_tutarlilik.csv`)

Ölçüt: 19 temsilcide kaç ETF'te net>0 ve IS ile OOS>0. Satırlar aile içi BH sayısına göre sıralandı.

* `MR_ibs_lt01_dusus` C1 h=3: 19/19 net>0, 18/19 IS ve OOS>0, 13'ünde t≥2. Medyan net 49 bp, medyan t 2,56.
  Aile FDR'sinde 16 ETF'te (kopyalar dahil) pozitif geçiyor.
* Aynı sinyal C0 h=3: 18/19 pozitif, medyan t 1,59. O1 h=3: 18/19 pozitif, medyan t 1,38.
* `VX_backwardation` C1 h=2: 19/19 pozitif ama medyan t≈1, hiçbir ETF'te t≥2 yok.
* `CA_tatil_oncesi` C1 h=3 (tatil sonrası 2.-4. gün): 19/19 pozitif, medyan t 1,54. Tatil türüne göre çok dağınık
  (Bölüm 6) → elendi.
* `MR_3gun_dusus` C0 erken çıkışlı: aile FDR'sinde 12 ETF'te pozitif. Bunların hepsi NDX/büyüme ve S&P kaldıraçlı kopyaları;
  IWM/DIA/RSP/MDY'de t<1,3 → S3 (düşük güven).
* `CA_cum`, `CA_per` (haftanın günü): yalnız NDX/büyüme kümesinde geçiyor → elendi.
* 20 gün zirve kırılımı ve momentum sinyalleri: net ≤0.

## 4. Aday stratejiler

Betik: `python3 -I kod/ajan_abd_endeks/05_adaylar.py`. Tüm sayıları basar ve `aday_*.csv` dosyalarını yazar.

### S1: zayıf kapanış dönüşü, SPY (abd_endeks_S1, güven: orta)

**TradingView'da uygulama:**
* Günlük grafik `AMEX:SPY`, temettü düzeltmesi (ADJ) açık.
* Pine: `ibs=(close-low)/(high-low)`, `sinyal = ibs<0.10 and close<close[1]`.
* İşlem: SPY long. Alternatif araç `AMEX:SSO` (2x) ya da `AMEX:SPXL` (3x); sinyal yine SPY'dan alınır.

**Zamanlama (TR saati):**
* Sinyal t günü ABD kapanışında oluşur (kış saatinde TR 00:00, yaz saatinde 23:00).
* Ana mod C1: ertesi işlem günü kapanıştan 5-10 dk önce al (kış TR ~23:50, yaz ~22:50). Midas'ta MOC/LOC emri olmadığı için
  piyasa emri ya da agresif limit emri kullanılır.
* Çıkış: 3 işlem günü sonra aynı saatte sat. Erken kapanış günlerinde (27 Kas ve 24 Ara 2026) kapanış TR 21:00.
* Akşam kontrol eden yatırımcıya uygun: sinyali bir akşam görür, ertesi akşam kapanışta işlem yapar.

| Mod | n | Brüt | Net (2.500 $) | t | IS net / t | OOS net / t | Yıl+ | maxDD | En kötü |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 170 | 49 | 36 | 1,98 | 17 / 0,60 | 50 / 2,11 | 0,8 | −%19 | −%9,7 |
| O1 | 170 | 38 | 25 | 1,35 | 4 / 0,14 | 40 / 1,82 | 0,7 | −%21 | −%13,0 |
| **C1** | **155** | **69** | **56** | **2,79** | **78 / 2,09** | **40 / 1,85** | **1,0** | **−%12** | **−%6,8** |

* **Maliyet duyarlılığı (C1).** Net 1.000 $'da 38 bp, 2.500 $'da 56 bp, 10.000 $'da 65 bp. Kazanma oranı %63, PF 1,93.
* **Kenar.** Koşulsuz 3 günlük getiri 16 bp; kenar 53 bp (t=2,64).
* **Dönem kontrolleri.** 2020 hariç net 47 bp (t=2,79). 2024 sonrası net 51 bp (t=1,54, n=44).
* **Yıllık bileşik net (C1, bp):**

  | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
  |---|---|---|---|---|---|---|---|---|---|
  | +114 | +246 | +502 | +2.266 | +1.915 | +172 | +1.291 | +1.270 | +697 | +256 |

* **Olay çalışması.** Sinyalden sonraki 1., 2., 3. ve 4. günlerin her biri koşulsuz ortalamanın üstünde
  (SPY: 18 / 23 / 11 / 24 bp/gün; koşulsuz 5,6). 5. gün negatif (−11). Bu yüzden C0 ile C1 aynı pencereyi yakalıyor ve 3 günden
  uzun tutmanın faydası yok.
* **Komşu parametreler** (`aday_S1_komsu_parametre.csv`, C1 h=3). IBS eşikleri 0,05 / 0,10 / 0,15 / 0,20 / 0,30, düşüş şartlı
  ve şartsız: 6 çekirdek ETF'in hepsinde hem IS hem OOS net>0. Eşik büyüdükçe etki küçülüyor (0,30'da 3-49 bp); bu da
  mekanizmayla tutarlı.
* **Aile içi (C1 h=3, ETF'in kendi sinyali; net bp ve t):**

  | Çekirdek | SPY | QQQ | IWM | DIA | RSP | MDY |
  |---|---|---|---|---|---|---|
  | Net bp / t | 56 / 2,8 | 71 / 3,5 | 39 / 1,9 | 42 / 2,1 | 57 / 3,0 | 47 / 2,5 |

  | Faktör | IWF | IWD | SCHD | SPLV | SPHB | MTUM | QUAL | VLUE | IWO | IWN | COWZ | JEPI | QYLD |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | Net bp / t | 59 / 2,9 | 56 / 3,4 | 31 / 1,8 | 4 / 0,3 | 76 / 2,7 | 55 / 2,6 | 53 / 2,9 | 49 / 2,8 | 52 / 2,6 | 39 / 1,9 | 37 / 2,1 | 10 / 0,8 | 22 / 1,0 |

* **Sepet t** (aynı giriş gününde açılan işlemler ortalanarak):

  | Mod | 6 çekirdek | SPY+QQQ+IWM |
  |---|---|---|
  | C1 | 2,44 | 2,77 |
  | C0 | 1,93 | 2,50 |
  | O1 | 1,23 | 1,69 |

  19 temsilcinin gün sepetinde t=1,23. Neden düşük olduğu bir sonraki maddede.
* **Genişlik** (önemli bulgu). Aynı gün sinyal veren temsilci sayısına göre gün ortalaması net:

  | Aynı gün sinyal veren temsilci | Gün sayısı | Net | t |
  |---|---|---|---|
  | 1 | 197 | −12 bp | |
  | 2-10 | 323 | ≈0 | |
  | ≥10 | 99 | +94 bp | 3,55 |

  Etki piyasa geneli zayıf kapanışlardan geliyor. ETF'in kendi sinyali SPY'ın da sinyal verdiği günlere denk geliyorsa güçlü;
  SPY'ın sinyal vermediği günlerde IWM/DIA/RSP/MDY'de ≈0. Sonradan bakılan bir kontrol: SPY sinyaliyle başka ETF'de işlem
  (C1) QQQ'da 74 bp (t=3,34), IWM'de 59 (2,40), MDY'de 56 (2,34), RSP'de 50 (2,34), DIA'da 45 (2,20).
  **Uygulama: sinyali SPY'dan al.**
* **VIX rejimi.** Bilgi amaçlı. 7 filtre denendi, ana kurala hiçbiri eklenmedi.
  * SPY C1: VIX≥20 iken 93 bp (t=2,75, n=83), VIX<20 iken 13 bp (t=0,75, n=72).
  * 200 günlük ortalama filtresi sonucu iyileştirmiyor (C>SMA200: medyan net 36 bp, filtresiz 52 bp).
* **Kaldıraçlı uygulama** (`aday_S1_kaldiracli.csv`, C1 h=3, sinyal dayanaktan):

  | Araç | Net | t | maxDD | En kötü işlem | Pozisyondayken en kötü gün |
  |---|---|---|---|---|---|
  | SSO (2x) | 121 bp | 3,0 | −%23 | −%13,8 | −%19 |
  | SPXL (3x) | 183 bp | 3,0 | −%35 | −%22,8 | −%29 |
  | QLD (2x) | 145 bp | 3,5 | −%20 | −%19,6 | −%24 |
  | TQQQ (3x) | 220 bp | 3,5 | −%32 | −%31,0 | −%34 |
  | TNA (3x) | 135 bp | 2,2 | −%40 | −%35,4 | −%32 |

  Kaldıraç başına brüt getiri dayanağa çok yakın: SPXL'de kaldıraç başına 66 bp, SPY'da 69 bp. Yani 3 günlük kaldıraç kaybı
  küçük. Sabit komisyonda 2.500 $ SPXL, 7.500 $ SPY maruziyeti verir ve bp maliyeti yaklaşık aynıdır (≈5 bp). Avantaj yalnız
  sermaye verimliliği; bedeli 3 kat kuyruk riski.
* **Son durum.** En son sinyal 5 Kas 2026 Perşembe (SPY, QQQ, IWM). Katı kuralda 2 Kas sinyaliyle açılan pozisyon 6 Kas'ta
  kapandığı için 5 Kas sinyali yok sayıldı. 2 Kas işlemi SPY'da −266 bp, QQQ'da −439 bp ile kapandı.

### S2: aynı kural, QQQ (abd_endeks_S2, güven: orta)

`NASDAQ:QQQ`, aynı Pine kodu. Alternatif araç `AMEX:QLD` (2x) ya da `NASDAQ:TQQQ` (3x). Zamanlama S1 ile aynı.

| Mod | n | Brüt | Net | t | IS net / t | OOS net / t | Yıl+ | maxDD |
|---|---|---|---|---|---|---|---|---|
| C0 | 181 | 89 | 76 | 3,68 | 82 / 3,14 | 71 / 2,29 | 1,0 | −%19 |
| O1 | 181 | 68 | 55 | 2,94 | 63 / 2,74 | 49 / 1,70 | 0,8 | −%16 |
| **C1** | **169** | **84** | **71** | **3,46** | **76 / 2,57** | **66 / 2,33** | **1,0** | **−%9** |

* Maliyet duyarlılığı (C1, net): 1.000 $'da 53 bp, 2.500 $'da 71 bp, 10.000 $'da 80 bp. Kenar 60 bp (t=2,95).
* 2020 hariç 62 bp (t=3,03). 2024 sonrası 70 bp (t=1,62).
* SPY'ın sinyal vermediği günlerdeki QQQ sinyalleri (yalnız teknoloji kaynaklı) C1'de zayıf (n=50, 42 bp, t=1,49),
  C0'da güçlü (n=54, 95 bp).
* Uyarı 1: QQQ'nun 2016-2026'daki güçlü teknoloji trendi sonucu şişirmiş olabilir. Aynı kural her endekste pozitif, ama en
  güçlü sonuç QQQ'da; seçim yanlılığı riski var.
* Uyarı 2: S1 ile S2'yi aynı anda almak riski ikiye katlar. Birini seç ya da pozisyonu böl.

### S3: 3 ardışık düşüş, ilk yükselen kapanışta çık (abd_endeks_S3, güven: düşük, kapanışa bağımlı)

**Kural:** `close<close[1] and close[1]<close[2] and close[2]<close[3]` ise SPY'ı t kapanışında al (C0, TR ~23:50).
İlk `close>close[1]` kapanışında, en geç 3. gün kapanışta sat.

| Mod | n | Net | t | IS net / t | OOS net / t |
|---|---|---|---|---|---|
| C0 | 127 | 34 bp | 2,32 | 14 / 0,48 | 46 / 2,88 |
| O1 | | 17 bp | 1,21 | | |
| C1 | | 24 bp | 1,52 | | |

* C0'da kazanma oranı %71, yılların %70'i pozitif.
* QQQ'da C0 net 52 bp, t=3,21. IWM/DIA/RSP/MDY'de t<1,3. 6 çekirdek sepeti C0'da t=1,95, O1'de 0,29, C1'de −0,14.
* S1 ile sinyal günlerinin yalnız ~%26'sı ortak.
* Eşiği SPY ve QQQ'da biçimsel olarak geçiyor, ama aile içinde tutarlı değil, IS'te zayıf ve SPY satırı birleşik FDR'yi geçmiyor.
* AE05'in SMA200 filtreli sürümü geçmedi.

## 5. Lead-lag (`leadlag_aile_ozet.csv`, `leadlag_catch_kontrollu.csv`, `leadlag_*_backtest.csv`)

* **Gecikmeli öncü (b): doğrulanmış öncü yok.**
  * `leadlag_sweep.csv`'deki 48 adayın hiçbiri aile hedeflerinde BH-FDR'yi geçmiyor (h1 ve h3). Aile alt kümesinde (2.636 satır)
    ve yalnız 6 çekirdek hedefte (284 satır) yeniden yapılan BH'de de geçen 0.
  * En güçlü FDR'siz satırlar faiz kanalından: TIP↑ / LQD↑ / DFII10 (reel faiz)↓ → 3 günde endeks↑. Örnek değerler:
    SPY ← TIP t=2,65 (IS 3,3 / OOS 1,3), QQQ ← DFII10 t=−2,99 (IS −2,9 / OOS −1,8); 1 sd başına ~20-26 bp.
  * Bu adaylar işlem kuralına çevrildi (z>1, h=3): SPY'da net 4-30 bp, t<1,6; yalnız QQQ C1'de t≈2,0-2,5. IWM ve DIA'da yok.
    Sonuç: izleme bilgisi, sinyal değil.
* **Yetişme testi (kendi getirisi kontrol edilerek).**
  * Kontrolsüz testte FDR'yi geçen 44 satırın 31'i QYLD'de. Bu, QYLD'nin kendi getirisindeki dönüşten kaynaklanan bir artefakt.
  * Kendi gecikmesi kontrol edilince h3'te yalnız T10YIE (başabaş enflasyon) 12 hedefte FDR'yi geçiyor. Ancak etki tamamen
    2020'den geliyor: 2020 hariç t=0,75, 2020 içinde t=5,5, OOS'ta t≈0,4 → öncü değil.
  * h1'de geçen tek satırlar SPLV←FXY ve SPLV←UUP. İkisi de OOS'ta zayıf.
* **IWM'in SPY'ı izlemesi (AE13).** İşaret ters çıktı. SPY'ın IWM'den 1 puan iyi olduğu günün ertesi IWM long: net −28 bp (h1),
  −89 bp (h3). z(gap)>1 kuralı: −21 bp (t=−2,1). Kontrollü katsayı IWM←SPY h1'de t=−2,78.
  Küçük ölçek büyükleri "yetişmiyor", ertesi gün bir miktar daha geri kalıyor.
* **Eşzamanlı sürücüler (a)** (corr_1y / beta_1y; öncü DEĞİL):
  * SPY: QQQ 0,93 / 0,59; VIX −0,86; XLK 0,85; DIA 0,84.
  * QQQ: XLK 0,96; SPY 0,93 / 1,45; SMH 0,91; EEM 0,84.
  * IWM: SPY 0,83 / 1,14; DIA 0,78; VIX −0,75; QQQ 0,74.
  * Kaldıraçlı araçlar: dayanakla korelasyon 1,00, beta ≈ kaldıraç.
* **Gerçek zamanlı izleme (c, d).** Hepsi doğrulanmış TradingView kodları:
  * `CME_MINI:ES1!` (SPY/RSP), `CME_MINI:NQ1!` (QQQ), `CME_MINI:RTY1!` (IWM/MDY), `CBOT_MINI:YM1!` (DIA).
    Globex'te ~23 saat işler. ABD kış saatinde TR 02:00'den ertesi gün 01:00'e açık; bakım arası TR 01:00-02:00.
  * Gece risk göstergeleri: `CBOE:VX1!`, `OSE:NK2251!`, `EUREX:FDAX1!`, `FX_IDC:USDJPY`.
  * Faiz: `TVC:US10Y`, `TVC:US02Y`.
  * QQQ için `NASDAQ:NVDA` pre-market hareketi.
  * Bu araçlar öncü değil: ETF kapalıyken işleyip açılış boşluğunu önceden gösterir. Gece hareketinin varyanstaki payı:
    SPY %40, QQQ %42. TR 12:00-17:30 arası pre-market'te Midas'ta yalnız limit emri geçer.

## 6. Elenen hipotezler (özet; ayrıntı `hipotez_ozet.csv`, `sonuc.json` → elenen)

| Hipotez | Sonuç |
|---|---|
| AE01 IBS<0,2, 1 gün | C0 medyan net −2 bp; O1 −10 bp. Literatürle uyumlu: IVV'de zayıf |
| AE02 IBS>0,8 → kısa (ters ETF) | C0 h1: SH −19 bp (t=−4,5), PSQ −18 bp (t=−3,5); −2x ve −3x araçlarda da net −18..−23 bp. Kısa yön kârsız |
| AE03 RSI2<10 & >SMA200 (≤3 gün) | Medyan net 2 bp |
| RSI2<10 C0 h1 (filtresiz) | SPY 24 bp t=2,0, QQQ t=2,1; ama O1/C1'de ≈0 ve diğer endekslerde yok |
| AE04 RSI4<25 (Connors) | C0 medyan net 13 bp, t 0,5; C1 negatif |
| AE05 3 düşüş & >SMA200 | Medyan net 2 bp (filtresiz sürüm S3) |
| AE06 Turnaround Tuesday | 6/6 pozitif (C0 medyan 90 bp) ama n≈31<40, medyan t 1,7 |
| AE07 Ay dönümü | Son gün→ilk 3 gün: O1 6/6 IS ve OOS pozitif ama medyan t 0,6 |
| AE08 Pre-FOMC | C0 medyan net −11 bp. Kurov ve diğ. (2021) ile uyumlu: drift yok |
| AE09 CPI / NFP günü | CPI −19 bp, NFP −6 bp, birleşik −13 bp. Duyuru primi yok |
| AE10 OPEX haftası | C0 medyan net −24 bp |
| AE11 Tatil öncesi | C0 medyan net 4 bp, t 0,4 |
| CA_tatil_oncesi C1 h3 (tatil sonrası 2.-4. gün) | SPY t=2,2, ama C0/O1 ≈0; tatil türüne göre dağınık (Good Friday +147, Yılbaşı +75, Noel −46, Juneteenth −26 bp; her tür ≤10 gözlem). Veri madenciliği |
| AE12 VIX ≥1,2×SMA10 & SPY>SMA200 | C0 12 bp, t 0,4; O1/C1 negatif |
| AE13 SPY→IWM yetişme | Ters işaret (Bölüm 5) |
| AE14 Gece/gün içi | Gece > gün içi (SPY 3,7 / 1,9 bp/gün) ama OOS'ta gece 2,2 bp (t=1,2). Kapanışta al-açılışta sat net −9 bp. Çıkarım: kapanışta işlem yap |
| AE15 Büyük düşüş günü → 2 gün | C0 medyan net −25 bp |
| VIX backwardation→kontango dönüşü | C1 h3 6/6 pozitif (medyan 55 bp) ama n≈45, medyan t 1,3 |
| Faktör çifti göreli dönüş (SPHB/SPLV, IWF/IWD, IWO/IWN, QQQ/IWM) | 16 varyantın yalnız biri (QQQ/IWM z1<−2 → QQQ C1 h3) FDR geçti; aynı fikrin diğer mod ve yönleri negatif |
| Aşırı alım → ters ETF (180 test) | Neredeyse tamamı net negatif (SPY RSI2>90 → SH C0 h1: −20 bp, t=−6) |
| Haftanın günü (CA_cum/CA_per) | Yalnız NDX/büyüme kümesinde; tek bağımsız küme |

## 7. İzleme listesi (55 ETF; ayrıntı `sonuc.json` → izleme)

* **Kabul:** SPY (S1, S3), QQQ (S2).
* **Yedek:**
  * IWM: kendi sinyali eşik altı; SPY sinyaliyle C1 net 59 bp.
  * RSP, DIA, MDY: S1 bu ETF'lerde de geçiyor, ama SPY ile yüksek korelasyonlu.
  * Kaldıraçlı araçlar (sinyal dayanaktan): SPXL ve SSO (SPY sinyaliyle), TQQQ ve QLD (QQQ sinyaliyle).
* **Red:**
  * Kopyalar: VOO, IVV, VTI, QQQM, UPRO, URTY, VUG, SCHG, MGK, VTV, VYM.
  * TNA ve UDOW: zayıf sinyal ya da aşırı kuyruk riski.
  * Tüm ters ETF'ler (10 adet): kısa sinyal yok, kalıcı negatif.
  * Dar hareketli temettü, düşük oynaklık ve kapalı alım fonları: maliyet/σ 0,20-0,37.
  * Faktör ETF'leri (IWF, IWD, SPHB, MTUM, QUAL, VLUE, IWO, IWN, AVUV, COWZ): SPY/QQQ ile örtüşüyor; tek başına verdikleri
    sinyaller piyasa geneli değil.

## 8. Sınırlamalar

* **Tek etki, tek dönem.** 2016-2026 güçlü boğa piyasası; dönüş stratejileri yükselen trendde daha iyi çalışır.
  OOS dönemi (2022-2026) 2022 ayı piyasasını içeriyor ve S1/S2 o yıl da pozitif. Yine de tek bir 10 yıllık örneklem var.
* **FDR.** Katı tek yönlü BH'de genel arama üzerinden hiçbir satır geçmiyor (Bölüm 1). Sonuçlar aile tutarlılığına dayanıyor
  ve aile, etkin olarak 3-4 bağımsız dayanaktan oluşuyor.
* **Kapanış fiyatı varsayımı.** C0/C1, kapanıştan 5-10 dk önce verilen emrin kapanış fiyatından dolduğunu varsayıyor. Midas'ta
  MOC/LOC yok, son dakikalardaki kayma modellenmedi. Çekirdek ETF'lerde makas ~1 bp; kaldıraçlıda 2-4 bp varsayıldı.
* **IBS hesabı.** TradingView varsayılan olarak düzeltilmemiş fiyat gösterir. IBS buna duyarsız; ama `close<close[1]` koşulu
  temettü günlerinde farklı çıkabilir. ADJ açık tutulmalı.
* **Vergi ve kur.** ABD temettü stopajı ve TL bazlı vergi hesabı modellenmedi. Backtest stopajsız toplam getiri kullanıyor.
* **Kaldıraçlı ürünler.** Midas'ta bulunurlukları resmî olarak doğrulanmadı. Mart 2020, 5 Ağu 2024 ve 9 Nis 2025 gibi olaylar
  gerçek. Tek işlemde −%20..−%35 kayıp mümkün.
* **Stop-loss.** Hiçbir stratejide stop yok. Stop eklemek sonucu değiştirir ve test edilmedi.

## 9. Tekrar üretim

```
python3 -I kod/ajan_abd_endeks/01_islenebilirlik.py   # işlenebilirlik + kopya çiftleri
python3 -I kod/ajan_abd_endeks/02_genel_aile.py       # genel kütüphane aile tutarlılığı + aile FDR
python3 -I kod/ajan_abd_endeks/03_hipotezler.py       # AE01-AE15 + yönlendirme testleri (1.056 test)
python3 -I kod/ajan_abd_endeks/04_leadlag.py          # lead-lag özet, kontrollü yetişme, kural backtest'leri
python3 -I kod/ajan_abd_endeks/05_adaylar.py          # S1/S2/S3 tüm istatistikler (sayıları basar)
python3 -I kod/ajan_abd_endeks/06_sonuc_json.py       # birleşik FDR + sonuc.json
```
Tek süreçte çalışır, multiprocessing yok. Her betik birkaç saniye sürer.
