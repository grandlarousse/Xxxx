# Denetim: abd_endeks ailesi (bağımsız denetçi)

Hazırlanma: 07.11.2026. Veri sonu: 06.11.2026.

* Denetim kodu: `kod/denetim_abd_endeks/`. Betikler `dt.py` (kendi motorum) ve `01`-`07`.
* Tablolar: `sonuclar/aile_abd_endeks/denetim/`. JSON: `sonuclar/aile_abd_endeks/denetim.json`.
* İşlem simülasyonunu `lib.trades`, `lib.evaluate` ve `ae.full_eval` kullanmadan kendim yazdım (`dt.sim`).
  Fiyatları yalnız `lib.load` ile okudum, IBS'i ham parquet'ten ayrıca hesapladım. Maliyet: 2×1,5 $ + `tarama.csv` makası.
* Bu bir geçmiş veri testi denetimidir. Yatırım tavsiyesi değildir.

## 0. Hüküm

| Strateji | Ajan | Denetim | Tek cümle |
|---|---|---|---|
| **S2 QQQ IBS<0,10 + düşüş, 3 gün** | orta güven | **DOĞRULANDI (orta güven, beklenti aşağı çekilmeli)** | Ailede sağlamlık testlerinin hepsinden geçen tek kural. Tam çoklu test düzeltmesinde ise sınırda. |
| **S1 SPY IBS<0,10 + düşüş, 3 gün** | orta güven | **ZAYIF** | Başlık sayısı (C1 h=3, 56 bp, t=2,79) 9 hücrenin en iyisi ve sivri bir tepe. Seçim düzeltmeli p=0,20, en iyi 5 işlem çıkınca t=1,93. |
| **S3 SPY 3 ardışık düşüş, ilk yükselişte çık** | düşük güven | **ÇÜRÜTÜLDÜ** | Yalnız tek bir kombinasyonda çalışıyor (C0 + erken çıkış + k=3). IS 2017-2019 yılları negatif, en iyi 5 işlem çıkınca t=1,33. |
| Lead-lag: "doğrulanmış gecikmeli öncü yok" | | **DOĞRULANDI** | En güçlü adaylar (QQQ←TIP/DFII10 h3) OOS'ta t≈1,5 ve etkileri maliyet düzeyinde. |

**Kod hatası ya da ileriye bakış bulmadım.** Ajanın sayıları birebir yeniden üretiliyor; düzeltilmesi gereken yorum ve seçim.

## 1. Mercek A: kod ve zamanlama

* **Yeniden üretim.** Kendi motorumla tüm sayılar birebir tuttu (2.500 $):

  | Strateji | Mod | n | Brüt | Net | t | IS net (t) | OOS net (t) | Yıl+ | maxDD | En kötü |
  |---|---|---|---|---|---|---|---|---|---|---|
  | S1 SPY | C0 | 170 | 48,9 | 35,9 | 1,98 | 17,2 (0,60) | 49,6 (2,11) | 0,8 | −%19 | −965 |
  | S1 SPY | O1 | 170 | 37,8 | 24,8 | 1,35 | 4,4 (0,14) | 39,9 (1,82) | 0,7 | −%21 | −1.296 |
  | S1 SPY | **C1** | **155** | **68,7** | **55,7** | **2,79** | **78,1 (2,09)** | **40,3 (1,85)** | **1,0** | **−%12** | **−675** |
  | S1 SPY | C2 (ek) | 144 | 32,0 | 19,0 | 0,97 | 50,9 | −3,7 | 0,7 | −%18 | −1.271 |
  | S2 QQQ | C0 | 181 | 89,2 | 76,2 | 3,68 | 82,2 (3,14) | 71,3 (2,29) | 1,0 | −%19 | −798 |
  | S2 QQQ | O1 | 181 | 68,3 | 55,3 | 2,94 | 63,4 (2,74) | 48,6 (1,70) | 0,8 | −%16 | −617 |
  | S2 QQQ | **C1** | **169** | **83,6** | **70,6** | **3,46** | **76,2 (2,57)** | **65,9 (2,33)** | **1,0** | **−%9** | **−831** |
  | S2 QQQ | C2 (ek) | 156 | 67,1 | 54,1 | 2,65 | 93,5 | 21,2 | 0,9 | −%25 | −1.071 |
  | S3 SPY | **C0** | **127** | **46,8** | **33,8** | **2,32** | **13,6 (0,48)** | **46,2 (2,88)** | **0,7** | **−%15** | **−786** |
  | S3 SPY | O1 | 127 | 30,0 | 17,0 | 1,21 | −7,2 | 31,8 | 0,6 | | |
  | S3 SPY | C1 | 122 | 37,1 | 24,1 | 1,52 | −16,3 | 48,6 | 0,6 | | |
  | S3 SPY | C2 (ek) | 116 | 15,8 | 2,8 | 0,21 | −9,0 | 10,2 | 0,7 | | |

  (C2: t+2 kapanışında giriş. Sinyal gecikmesine duyarlılık için ek mod.)
* **IBS çapraz kontrolü.** Ham OHLC ile düzeltilmiş OHLC'den hesaplanan IBS arasındaki fark en fazla 7e-14. SPY'da 217'ye karşı 218
  sinyal var; tek fark 11.07.2024 ve `lib.load`'un h/l temizliğinden geliyor. QQQ'da fark yok.
* **İleriye bakış.** Sinyal yalnız t günü OHLC'sini ve t−1 kapanışını kullanıyor. VIX, BTC ve Hazine verisi kullanılmıyor.
  * Girişler doğru günde: C0'da c[t], O1'de o[t+1], C1'de c[t+1]. Çıkış t+h ya da t+1+h kapanışında.
  * Çakışma yok. Maliyet her işlemde bir kez düşülüyor. Isınma süresi 200 gün.
  * Çekirdek ETF'lerde `veri_duzeltmeleri.csv` satırı yok.
* **En büyük 5 kazanç** (S1 SPY C1):
  * 20.03.2020 sinyali: +1.716 bp (Mart 2020 dönüşü);
  * 03.04.2025: +858 bp (09.04.2025 gümrük ertelemesi günü, `veri_kalitesi.csv`'de gerçek olay);
  * 11.03.2022: +577 bp;
  * 21.12.2018: +572 bp;
  * 12.05.2020: +476 bp.

  Veri hatası yok, olaylar gerçek. Ancak dördü kriz dönüşü. Bu 5 işlem ortalamanın ~27 bp'sini taşıyor.
  * S2 QQQ C1'de de ilk üç işlem aynı olaylar.
  * S3'ün en büyük kazancı 07.04.2025 → 09.04.2025 (+877 bp, tek olay).
* **Kaldıraçlı araçlar** (C1, sinyal dayanaktan) birebir tuttu:

  | Araç | Net | t | En kötü işlem |
  |---|---|---|---|
  | SSO | 121 bp | 3,00 | −%13,8 |
  | SPXL | 183 bp | 2,99 | −%22,8 |
  | QLD | 145 bp | 3,50 | −%19,6 |
  | TQQQ | 220 bp | 3,50 | −%31,0 |

* **C0'nun uygulanabilirliği.** Midas'ta MOC yok; karar kapanıştan ~10 dk önce, son fiyatla verilir.
  * IBS 0,08-0,12 aralığındaki ve |r|<%0,1 olan sınır günleri çıkarıldı.
  * QQQ C0: 76 → 56 bp (t 3,68 → 2,43). Sınırdaki işlemler ortalamanın üstünde kazandırmış, yani C0 sonucu son dakika
    sınıflamasına duyarlı.
  * SPY C0: 36 → 39 bp. Etkilenmiyor.
  * C1 bu sorundan bağımsız; sinyal tamamen bilinir.

## 2. Mercek B: istatistiksel sağlamlık

### 2.1 Çoklu test

* Ajanın iddiası doğru:
  * Aile satırları (genel 16.335 + hipotez 1.056) üzerinde iki yönlü BH'de 1.822 satır geçiyor (eşik p≤0,0105). Bunların
    yalnız 97'si pozitif, yani geçişler çoğunlukla ters ETF ve kapalı alım fonlarındaki negatif satırlar.
  * Tek yönlü BH'de ("net>0") geçen yok.
  * Bonferroni eşiği t≈4,5; etkin 7.533 testle t≈4,4. Hiçbir satır geçmiyor.
* **Seçim düzeltmeli permütasyon** (benim testim). Genel kütüphanenin 31 sinyali × 3 mod × 3 tutuş = 279 hücrede en yüksek
  net t alındı. Null: tüm sinyallere aynı dairesel kaydırma (400 tekrar). Bu null sinyal kümelenmesini ve piyasa eğilimini korur.
  * **SPY:** gözlenen en iyi hücre S1 C1 h3 (t=2,79). Null altında en yüksek t'nin medyanı 2,29, %95'i 3,22 → **p=0,20**.
    SPY'da S1, kütüphane içinden seçilmiş olmasıyla açıklanabilir.
  * **QQQ:** en iyi hücre S1 C0 h3 (t=3,68), **p=0,025**. C1 için p=0,055.
* **Aile düzeyi.** 19 temsilcinin ortalama t'si 279 hücrenin her birinde hesaplandı; tüm ETF'lere aynı kaydırma
  uygulandı (300 tekrar).
  * Gözlenen en yüksek değer S1 C1 h3'te: 2,28. Null'ın %95'i 2,44 → **p=0,09**.
  * C0 için p=0,44, O1 için p=0,78.
  * "19/19 temsilcide pozitif" bulgusu tek başına anlamlı (null'da olasılığı 0,001). Ancak bu hücre 279 hücre içinden
    seçildi. Seçim düzeltmesiyle kanıt %10 düzeyinde sınırda.
  * 6 çekirdek ETF için "6/6 pozitif" null'da %17 olasılıkla görülüyor. Pozitif eğilimli piyasada "hepsi pozitif" zayıf bir kanıt.

### 2.2 Tek test permütasyonları (2.000 tekrar, aynı çakışmasız simülasyon, ortalama brüt)

| Vaka | Gözlenen | Rastgele gün (p) | Düşüş günü + VIX beşte biri eşleşmeli (null ort., p) | Dairesel kaydırma (p) |
|---|---|---|---|---|
| S1 SPY C1 | 68,7 | 0,0005 | 26,5 / 0,002 | 0,0005 |
| S1 SPY C0 | 48,9 | 0,005 | 24,3 / 0,042 | 0,011 |
| S2 QQQ C1 | 83,6 | 0,0005 | 36,6 / 0,004 | 0,0005 |
| S2 QQQ C0 | 89,2 | 0,0005 | 39,7 / 0,0005 | 0,0005 |
| S2 QQQ O1 | 68,3 | 0,001 | 32,8 / 0,012 | 0,001 |
| S3 SPY C0 | 46,8 | 0,0005 | 22,0 / 0,008 | 0,0015 |

* IBS'in katkısı gerçek. SPY C1'de "düşüş günü & IBS≥0,30" net 5 bp, tüm düşüş günleri 7 bp, IBS<0,10 ise 56 bp.
* VIX≥20 içinde IBS<0,10 84 bp, IBS≥0,30 38 bp. Yani etki yalnız oynaklık rejimi değil.
* Ancak bu p'ler seçimden önceki p'ler. Seçim düzeltmesi Bölüm 2.1'de.

### 2.3 Parametre komşuluğu

Ağ: IBS eşiği 0,05 / 0,075 / 0,10 / 0,125 / 0,15 / 0,20, tutuş h=1-5, modlar C0 / O1 / C1
(`komsu_parametre.csv`). Özet için eşik 0,05-0,20 × h=2-4 × 3 mod = 54 hücreye bakıldı.

| ETF | Medyan net | t≥2 hücre oranı | IS>0 & OOS>0 oranı | Yorum |
|---|---|---|---|---|
| **QQQ** | 57 bp | %78 | %96 | **plato** |
| **SPY** | 27,5 bp | %30 | %94 | işaret tutarlı, anlamlılık değil |
| **IWM** | 17 bp | %20 | %59 | gürültü |

* SPY C1 satırı h=1-4: 13 / 22 / **56** / 45 bp; t 1,1 / 1,3 / **2,8** / 1,9. C1 h=3 sivri bir tepe.
  Mod ekseninde de öyle: C0 / C1 / C2 = 36 / 56 / 19 bp.
* IWM'de kendi sinyaliyle C1 satırı h=2-4: −4 / **+39** / −1 bp. Ajanın IWM gerekçesindeki "39 bp (t=1,9)" gürültü.
* **Takvim zamanlı (örtüşmeli, yol bağımsız) sürüm.** Her sinyal kendi penceresinde tutulur.
  * SPY: C0 18,2 bp/gün (t=2,66), C1 18,3 (t=2,70), C2 7,6 (t=1,14).
  * QQQ: C0 30,9 (t=4,06), C1 26,1 (t=3,52).
  * Sonuç: SPY'da C1'in C0'dan "daha iyi" görünmesi, çakışmasızlık kuralının yarattığı bir yol artefaktı.
    "Yeni sinyalde süreyi uzat" varyantıyla SPY C0 net 52 bp (t=2,73), C1 54 bp (t=2,33).
  * OOS günlük getiri: SPY C1 12,5 bp/gün (koşulsuz 5,5), QQQ C1 20,5 bp/gün.

### 2.4 Dönem ve işlem dışlamaları (2.500 $ net)

| Vaka | Tümü | 2020 hariç | 2022 hariç | 2020+2022 hariç | En iyi 5 hariç | 2024+ |
|---|---|---|---|---|---|---|
| S1 SPY C1 | 55,7 / 2,79 | 47,2 / 2,79 | 64,1 / 2,92 | 55,4 / 3,08 | **30,0 / 1,93** | 50,6 / 1,54 (n=44) |
| S1 SPY C0 | 35,9 / 1,98 | 37,1 / 2,13 | 37,3 / 2,04 | 39,1 / 2,42 | **20,1 / 1,17** | 47,2 / 1,69 |
| S2 QQQ C1 | 70,6 / 3,46 | 61,5 / 3,03 | 80,1 / 3,68 | 71,0 / 3,30 | **47,2 / 2,65** | 69,8 / 1,62 (n=43) |
| S2 QQQ C0 | 76,2 / 3,68 | 71,5 / 3,16 | 89,2 / 4,52 | 85,8 / 3,97 | 57,6 / 2,95 | 74,6 / 1,93 |
| S3 SPY C0 | 33,8 / 2,32 | 33,4 / 2,55 | 34,2 / 2,10 | 33,6 / 2,39 | **16,2 / 1,33** | 53,7 / 2,29 |

S3'ün yıllık net toplamları (bp): 2017 −11, 2018 −124, 2019 −222, 2020 +393, 2021 +616. IS'in ilk üç yılı negatif.

### 2.5 Maliyet ve rejim

* Net bp, pozisyon 1.000 / 2.500 / 10.000 $:
  * S1 SPY C1: 38 / 56 / 65.
  * S2 QQQ C1: 53 / 71 / 80.
  * S3 SPY C0: 16 / 34 / 43.
* **SPY'da etki VIX≥20 günlerine bağlı:**
  * VIX<20 (n=72): brüt 25,8 bp; net 2.500 $'da 12,8, **1.000 $'da −5,2**.
  * VIX≥20 (n=83): brüt 106 bp.
* **QQQ iki rejimde de çalışıyor:** VIX<20'de net 47 bp (brüt t=2,74), VIX≥20'de 91 bp.

### 2.6 S3 komşuları (SPY)

| Varyant | C0 net / t | IS net |
|---|---|---|
| 2 ardışık düşüş | 9 / 0,88 | |
| **3 düşüş + ilk yükselişte çık** | **34 / 2,32** | |
| 3 düşüş, sabit 3 gün | 25 / 1,32 | −9 |
| 4 düşüş | 53 / 1,88 (n=54) | −22 |

* C1'de tüm varyantlar ≤24 bp.
* IWM, DIA, RSP ve MDY'de yok. QQQ'da yalnız C0 + erken çıkışta var (C1 9 bp).
* Tek bir kombinasyonda görünen bir tepe → çürütüldü.

## 3. Lead-lag

* `leadlag_sweep.csv`'de aile hedeflerinin 2.636 satırında `fdr10_lag_t_h1` ve `fdr10_lag_t_h3` bayrağı 0. Teyit edildi.
* Bağımsız yeniden tahmin: kendi gecikmesi kontrollü, Newey-West, 6 hedef × 6 öncü × h1/h3 = 70 test (`leadlag_yeniden.csv`).

  | Öncü → hedef | Tüm dönem t | IS t | OOS t | OOS etki (1 sd başına, 3 gün) |
  |---|---|---|---|---|
  | TIP → QQQ h3 | 3,06 | 3,33 | 1,54 | 11,6 bp |
  | DFII10 → QQQ h3 | −3,03 | −2,91 | −1,75 | −14,1 bp |

  * Bu iki satır, benim seçtiğim küçük kümede BH'yi geçiyor. Ancak tam taramada geçmiyor; OOS'ta zayıflıyor ve OOS etkisi
    2.500 $ maliyeti (13 bp) düzeyinde.
  * DFII10 (Hazine reel getiri eğrisi) ABD kapanışında bilinmez; yalnız O1/C1 için kullanılabilir.
  * Sonuç: **gecikmeli öncü değil, izleme bilgisi.**
* **IWM←SPY h1 (t=−2,73).** Göreli getiri (IWM−SPY) ile test edilince t=−1,61 (h1) ve −0,35 (h3). Etki büyük ölçüde SPY'ın kendi
  negatif otokorelasyonundan (−0,13) geliyor; çapraz öncülük değil. Midas'ta açığa satış da yok.
* **T10YIE yetişme.** Yeniden hesapladım: SPY h3 tüm dönem t=3,75, 2020 hariç 0,75, OOS 0,42. Ajanın "yalnız 2020" tespiti doğru.
* **Bayat fiyat.** XYLD ve QYLD'nin kendi otokorelasyonu −0,21 / −0,20 (SPY −0,13). Ajanın QYLD "yetişme" bulgusunu artefakt
  sayması doğru.
* **TradingView kodları.** Lead-lag ve izleme kodlarının tamamı `tv_dogrulama.csv` / `tv_etf.csv`'de "dogrulandi" ya da
  "dogrulandi_kanonik". Örnekler: CME_MINI:ES1!, NQ1!, RTY1!, CBOT_MINI:YM1!, CBOE:VX1!, OSE:NK2251!, EUREX:FDAX1!,
  FX_IDC:USDJPY, TVC:US10Y, TVC:US02Y, NASDAQ:NVDA, CBOE:VIX, CBOE:VIX3M.
* **Küçük düzeltme (OSE seans saatleri).** 05.11.2024 sonrası OSE türev seansları gündüz 08:45-15:45 JST (TR 02:45-09:45),
  gece 17:00-06:00 JST (TR 11:00-00:00). Ajan "TR 02:45-09:15" ve "gece TR 10:30-00:00" yazmış; eski saatler gibi görünüyor.
  Doğrulanmalı.

## 4. İzleme listesine itirazlar

* **SPY (kabul).** Araç ve sinyal kaynağı olarak uygun. Ancak SPY'ın kendi S1 beklentisi düşük: komşu medyanı ~28 bp net,
  VIX<20'de 1.000 $'da negatif. Aynı SPY sinyaliyle QQQ'da işlem: C1 74 bp (t=3,34), C0 57 (t=2,65), O1 45 (t=2,08).
  Ana araç QQQ olmalı.
* **IWM (yedek).** Gerekçe yanıltıcı. Kendi sinyaliyle C1 h=2/3/4 = −4 / 39 / −1 bp; C0 t=0,8; komşu hücrelerin %20'sinde t≥2.
  Doğrulanabilir strateji yok. Yedek kalacaksa gerekçesi "yalnız SPY sinyaliyle, likit küçük ölçek aracı (RTY1! ile izlenir)"
  olmalı.
* **DIA, RSP (yedek).**
  * SPY ile 0,84-0,87 korelasyonlu. S1 sonucu SPY'daki gibi yalnız C1 h=3'te: RSP C0 t=1,8, C2 10 bp; DIA C0 t=1,87, C2 10 bp.
    Bağımsız değer katmıyor.
  * Maliyet/oynaklık oranı SPY'dan iyi değil: DIA 0,15, RSP 0,17.
  * Öneri: red, ya da "yalnız SPY yerine". MDY de benzer (C2 13 bp), ama IWM'e alternatif olarak yedek kalabilir.
* **SPXL ve SSO (yedek).** SPY sinyaliyle SPXL C0 t=2,18, O1 t=1,71. Kırılganlık SPY ile aynı, kuyruk riski 3 kat:
  en kötü işlem −%22,8 (C1), −%29,9 (C0), −%36,9 (O1).
* **TQQQ ve QLD.** Uygun. TQQQ'nun Midas bulunurluğu "muhtemel", QLD'ninki doğrulanmadı.
  * TQQQ'da 60 günlük en kötü işlem kümesi −%17 (Nisan 2019).
  * Kaldıraçlı araçta pozisyon büyüklüğü dayanağa göre 1/3 alınmazsa risk 3 kat olur.

## 5. Ajanın kaçırdıkları

1. **Mod ve çakışma kuralı yanılgısı.**
   * Ajan SPY'da C1'i "en temiz ve en iyi" diye ana mod yapmış. Takvim zamanlı sürümde ise C0 ile C1 aynı:
     t 2,66'ya karşı 2,70. Fark çakışmasızlık kuralından geliyor; "uzatmalı" kuralla SPY C0 52 bp (t=2,73).
   * Kullanıcı için anlamı: pozisyondayken yeni sinyal gelirse ne yapılacağı (yok say ya da süreyi uzat) sonucu modu
     seçmekten daha çok etkiliyor. Başlık sayısı bu ayrıntıya duyarlı.
   * Güncel örnek: 05.11.2026 sinyali katı kuralda yok sayıldı. Uzatmalı kural pozisyonu 11.11'e kadar taşırdı; araya 10.11 CPI
     (TR 16:30) girerdi.
2. **Rejim bağımlılığı ve küçük hesap.**
   * SPY S1'in kârı VIX≥20 günlerinde. VIX<20'de 1.000 $ pozisyonla işlem başına −5 bp.
   * QQQ'da VIX<20'de bile 1.000 $'da +29 bp.
   * Midas'ın sabit 1,5 $ komisyonuyla küçük hesap için doğru araç QQQ (ya da SPY sinyaliyle QQQ). Bu, filtre önerisi değil;
     araç seçimi.
3. **Test edilemeyen risk.** Veri 2016'da başlıyor: 2018, 2020, 2022 ve 2025 düşüşleri hızlı V dönüşleriyle bitti. Uzun ayı
   piyasasında (2000-2002, 2008 tipi) ardışık sinyallerde birikimli kayıp test edilmedi. En büyük kazançların dördü kriz dönüşü.
   Strateji "kapitülasyon alımı" niteliğinde.

Betikler (hepsi `python3 -I` ile, tek süreç):

* `kod/denetim_abd_endeks/01_yeniden_uretim.py`
* `02_saglamlik.py`
* `03_secim_duzeltme.py`
* `04_aile_maxstat.py`
* `05_leadlag.py`
* `06_s3_ve_esik.py`
* `07_kacirilan.py`
