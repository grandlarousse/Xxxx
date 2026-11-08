# Midas'ta ABD ETF'leriyle 1-3 günlük alım-satım: stratejiler, izleme listesi ve lead-lag (07.11.2026)

*Veri: 06.11.2026 kapanışına kadar. Yatırım tavsiyesi değildir. Geçmiş performans geleceği garanti etmez.*

## 0. Kısa cevap

**Ne yapıldı?**
- 9 aileye ayrılan 313 ABD ETF'i 10 yıllık günlük veriyle (2016-11 → 2026-11) tarandı. Aileler: ABD endeks ve kaldıraçlı/ters, sektör ve tematik, tek hisse kaldıraçlı, enerji/doğalgaz/tarım, altın/gümüş/metal/madenci, tahvil ve döviz, VIX, kripto, ülke ETF'leri.
- Genel kütüphanede 31 sinyal, 3 giriş zamanı ve 1/2/3 günlük tutuş birlikte denendi; bu 92.664 test demek. Giriş zamanları: t kapanışı (C0), ertesi açılış (O1), ertesi kapanış (C1). Buna aile başına binlerce özel test eklendi: FOMC, CPI, EIA, roll, ihale, VIX vade yapısı, BTC 7/24...
- Her aday stratejiyi bağımsız bir denetçi kendi koduyla yeniden üretti ve çürütmeye çalıştı. Ardından ana ajan, dağıtım verisi düzeltilmiş veride ortak bir motorla hepsini yeniden hesapladı. Son olarak iki eleştirmen rapor ve kartları denetledi.

**Sonuç sert:** Midas'ın 1,5 $ komisyonu ve makaslar düşüldükten sonra denetimden geçen yalnız **2 kural** var. İkisi de aynı mekanizmaya dayanıyor: teknoloji ve yarı iletken ETF'i günün dibinde kapanınca sonraki 1-3 günde toparlanıyor. Rakamlar 2.500 $ pozisyon içindir.

| Kod | Kural | Araç | Tutuş | Net / işlem (backtest) | Denetçinin gerçekçi tahmini | Kazanma | İşlem/yıl | En kötü işlem | Çoklu test |
|---|---|---|---|---|---|---|---|---|---|
| **A1** | **QQQ:** IBS < 0,10 **ve** düşüş günü → ertesi gün kapanışta gir | QQQ | 3 gün | +68 bp (t 3,5) | **+45-55 bp** | %60 | ~18 | −%8,3 | sınırda (p ≈ 0,03-0,06) |
| **A2** | **SMH:** IBS < 0,20 → kapanışta / after-hours'ta gir | SMH (kopyası SOXX) | 1 gün | +42 bp (t 3,7) | **+31-36 bp** | %58 | ~50 | −%10,7 | sınırda |

**IBS (internal bar strength):** IBS = (kapanış − günün düşüğü) / (günün yükseği − günün düşüğü). 0'a yakın değer, kapanışın günün dibinde olduğu anlamına gelir.

> **Şu anki rejim (06.11.2026 kapanışı): çok yüksek oynaklık.**
> - **Endeksler ve oynaklık:** VIX 25,6; VIX/VIX3M 1,04, yani ters (backwardation) vade yapısı.
> - **SMH:** 20 günlük oynaklık %62. Bu, 10 yılın %97'lik dilimi demek. SMH zirvesinden −%31 aşağıda; günlük 1 standart sapmalık hareket ≈ 390 bp.
> - **QQQ:** oynaklık %33 (%90'lık dilim), zirveden −%14.
> - **Diğerleri:** EWY'nin oynaklığı %71 (%97'lik dilim); SOXL 52 haftalık zirvesinden −%85 aşağıda.
>
> **Bu ne demek?** A2'nin beklentisi işlem başına ~+35 bp; bu rejimde tek bir günün olağan hareketi bunun ~10 katı.
> - Tarihsel olarak A2 yüksek oynaklıkta daha iyi çalıştı: yüksek oynaklık dönemlerinde +65 bp (t 2,7), 2026'da +109 bp (n=38).
> - A1 yüksek oynaklıkta getiri başına daha fazla risk taşıdı: +70 bp ama standart sapma 319 bp. 2026'da 10 işlemde yalnız +5 bp.
>
> **Öneri:**
> - **Boyut:** Pozisyonu oynaklığa göre küçült: normal tutar × (10 yıllık medyan oynaklık / şu anki oynaklık). Bu da şu an QQQ ve SMH'de yaklaşık **yarı boyut** demek.
> - **Kaldıraç:** Kaldıraçlı araçlara (TQQQ, SOXL, NVDL, TSLL, KORU) bu rejimde girme.

**Bunların dışındaki her şey:**
- **Zayıf kanıtlılar (Kademe B):** 10 kural (B1-B10). Bunlara 1 filtre (F, strateji değil) eşlik ediyor. Kağıt üstünde izlenebilir ya da çok küçük boyutla denenebilir.
- **Çalışmayanlar:** Doğalgaz, petrol, altın-gümüş, VIX, kripto, döviz, tarım, sektör rotasyonu, takvim etkileri (FOMC, CPI, ay sonu…) ve kırılım stratejileri. "Millet doğalgaz, altın trade ediyor" ama bu ürünlerde 1-3 günlük, maliyeti yenen, sağlam bir giriş kuralı bulunamadı.

**Lead-lag:**
- 1-3 günlük ufukta, maliyet sonrası işe yarayan **doğrulanmış gecikmeli öncü yok.** 286 hedef ETF × 48 öncü, kendi-çiftler hariç 13.694 çift tarandı. Dokuz ailenin dokuzunda denetçi de bunu teyit etti. Gecikme testinde FDR'yi geçen 43 bayrağın çoğu döviz ETF'lerinde (1 sd başına 5-9 bp, maliyetin altında); kalanlar IGV/SKYY/KWEB'de negatif gecikmeler (yalnız 'alma' filtresi).
- İlk taramada FDR'yi geçen 1 günlük "yetişme" bayraklarının çoğu dağıtım verisindeki bir hatadan doğmuştu. Hata düzeltilince sayı 288'den 2'ye indi. 3 günlükte 110 bayrak kaldı; bunlar ETF'in kendi ortalamaya dönüşünü yansıtıyor ve maliyeti karşılamıyor.
- Doğru kullanım:
  1. **Aynı gün sürücüler:** ETF'yi neyin hareket ettirdiğini gösterir; öncü değildir.
  2. **Gerçek zamanlı izleme:** ETF kapalıyken işleyen vadeli, kripto ve döviz fiyatları ertesi açılış boşluğunu önceden gösterir.
- Her izleme ETF'i için bunlar TradingView kodlarıyla `kartlar/<SYM>.md` dosyalarında. Kodların tamamı sembol sayfası okunarak doğrulandı.

**Kuralların gerçek getirisi (10.000 $ portföy simülasyonu, §6):**
- A1 sermayenin yarısıyla, A2 dörtte biriyle uygulansaydı (2017-2026) yıllık bileşik getiri **%13,3**, en büyük düşüş **−%8,8** olurdu. Hesap günlerin %37'sinde piyasadaydı.
- Aynı dönemde QQQ'yu al-tut %19,3 getirdi ama −%35 düşüş yaşattı.
- Yani bu kurallar boğa döneminde al-tut'u **getiride geçmiyor** (A1 tek başına %100 ağırlıkla bile %14,6). Sağladıkları şey çok daha düşük düşüş ve piyasa maruziyeti.

**Midas'a özgü üç pratik kural:**
1. **Pozisyon en az ~2.500 $ olsun.** 1.000 $'da komisyon gidiş-dönüş 30 bp eder; SMH ve SPY kenarını yer. A1 + A2 birlikte için ≥ 5.000 $ gerekir. Daha küçük hesapta yalnız A1 (QQQ).
2. **"Kapanışta al" iki yolla yapılır.** Midas'ta MOC/LOC (kapanışta piyasa emri) yok.
   - (a) Kapanıştan ~5-10 dk önce emir: kışın TR 23:50, yazın 22:50.
   - (b) Daha temiz yol: kapanıştan sonra after-hours'ta (kış TR 00:00-01:00 tercih) kapanış fiyatına yakın **limit** emir, tam adet.
3. **PTP/K-1 yapısındaki fonlara dikkat.** Satışta %10 brüt kesinti riski var. Uygulamada "PTP" ibaresini ve kesintiyi teyit etmeden kısa vadeli işlem yapma. Hangi fonların bu yapıda olduğu §1'de.

## 1. Midas koşulları ve saatler

Kaynak: `notlar/midas_kosullari.md`; kaynaklı ve tarihli, `.json` sürümü de var.

| Konu | Durum |
|---|---|
| Komisyon | Emir başına 1,5 $ (gidiş-dönüş 3 $). 1.000 $'da 30 bp, 2.500 $'da 12 bp, 10.000 $'da 3 bp |
| Açığa satış / kredi | Yok. Kısa yön ancak ters ETF ile; ters ETF'li varyantların neredeyse tamamı testlerde net negatif çıktı |
| Seans (TR saati) | Kış (1 Kas 2026 – 14 Mar 2027): 17:30-00:00. Yaz: 16:30-23:00 |
| Pre-market / after-hours | Kış 12:00-17:30 / 00:00-04:00. Yaz 11:00-16:30 / 23:00-03:00. **Yalnız limit emir.** Kesirli emir uzatılmış saatte kabul edilmeyebilir; tam adet kullanın |
| Emir tipleri | Piyasa, limit, stop, stop-limit, kâr al/zarar durdur. **MOC/LOC yok**, takip eden stop yok |
| Kesirli alım | Var (ETF'lerde de; uzatılmış saatte belirsiz) |
| Takas | T+1. Aynı gece sat-al yaparken kullanılabilir bakiyeyi kontrol edin |
| Ürün bulunurluğu | Midas resmî sembol listesi yayımlamıyor. **1x ETF'ler (QQQ, SPY, SMH…) dahil hiçbir ETF için bulunurluk resmî olarak doğrulanamadı.** Kanıtlar: GBTC ve ETHE'nin sembol sayfası var; UNG'de işlem yapılmış (2023); TQQQ için kullanıcı beyanı var. Uygulamada sembolü arayarak teyit edin |
| PTP/K-1 yapısı | USCF: UNG, USO, BNO, USL, UNL, UGA, CPER · ProShares Trust II: BOIL, KOLD, UCO, SCO, UVXY, SVXY, VIXY, UGL, GLL, AGQ, ZSL, YCS, YCL, EUO, ULE · Invesco DB: DBA, DBB, DBC, DBO, UUP, UDN · Teucrium: CORN, WEAT, SOYB, CANE · ayrıca GSG, SVIX, UVIX. Uygulamadaki "PTP" ibaresi ve %10 kesinti yalnız UNG için belgelenmiş (09.2024, kullanıcı beyanı; kesinti 1-1,5 hafta sonra kaldırılmış). Diğerleri fon yapısından çıkarımdır |
| Vergi | ABD temettü stopajı %20 (W-8BEN). Türkiye'de yurt dışı alım-satım kazancı tutar ne olursa olsun yıllık beyan edilir (2026 kazançları Mart 2027'de); zarar yalnız aynı yıl içinde mahsup edilir |
| Yarım günler | 27.11.2026 ve 24.12.2026: kapanış 13:00 ET = **TR 21:00**. `kod/sinyal.py` bunu uyarır |

## 2. Uygulanabilir kurallar (Kademe A)

### A1 — QQQ "zayıf kapanış" dönüşü, 3 gün

**Sinyal (t günü kapanışı):**
- Grafik: `NASDAQ:QQQ` günlük mum.
- Koşul: IBS < 0,10 **ve** kapanış < önceki kapanış. Yani gün düşüşle ve günün dibine çok yakın kapanmış.
- TradingView göstergesi `kod/tradingview/ibs_dip.pine` QQQ'da otomatik olarak C1, 3 gün ayarına geçer.

**Giriş ve çıkış:** İki yoldan **yalnız birini** seç.
- **C1 (ana yol, akşam kontrolüne uygun):** Sinyali gece kesin kapanışla gör. Ertesi işlem günü kapanıştan ~5-10 dk önce (kış TR ~23:50) al. 3 işlem günü sonra kapanışa yakın sat.
- **O1 (erken akşam profili):** Sinyali gece gör, ertesi gün açılışta (kış TR 17:30) al, 3. gün kapanışa yakın sat. Biraz daha zayıf: +56 bp, t 3,1.
- **C0:** Sinyal günü kapanışında gir (+77 bp, t 3,9). IBS'yi kapanış öncesi tahmin etmek gerektiği için hata payı var.

Stop yok; backtest stopsuz yapıldı. Pozisyondayken gelen yeni sinyal yok sayılır.

**Rakamlar (son kontrol, dağıtım düzeltmeli veri):**
- C1: n=177, +68 bp, kazanma %60, ~18 işlem/yıl.
- IS +71 / OOS +66 bp; yılların %100'ü pozitif.
- En iyi 5 işlem çıkarılınca t 2,7; 2020 ve 2022 çıkarılınca t 3,3.
- 1.000 $'da +50 bp.

**Denetçi değerlendirmesi:**
- Karar: **doğrulandı**, güven orta. Gerçekçi beklenti +45-55 bp.
- Seçim düzeltmeli p = 0,025-0,055; çoklu testte sınırda.
- Net kenar VIX < 20'de +47 bp, VIX ≥ 20'de +91 bp.

**Oynaklık rejimine göre (sinyal günü 20 günlük oynaklık, üçe bölünmüş):**

| Rejim | Net (bp) | t | İşlem başı std (bp) |
|---|---|---|---|
| Düşük oynaklık | +63 | 2,7 | 140 |
| Orta | +70 | 2,3 | 240 |
| Yüksek | +70 | 1,9 | 319 |
| 2026 | +5 (n=10) | — | — |

**Kaldıraçlı araçlar (C1, son kontrol):**
- QLD (2x): +141 bp, en kötü işlem −%19,6.
- TQQQ (3x): +214 bp, en kötü işlem **−%31** (Mart 2020).
- Kullanılacaksa dayanak eşdeğeri tutarın 1/2-1/3'ü kadar. Şu anki rejimde önerilmez.

**Riskler:**
- Örneklem 2016-2026'nın güçlü teknoloji dönemi; uzun bir ayı piyasası test edilmedi.
- B1 (SPY) ile sinyallerin %73'ü aynı gün.

### A2 — SMH gün sonu zayıflığı dönüşü, 1 gün

**Sinyal (t kapanışı):**
- Grafik: `NASDAQ:SMH` günlük mum.
- Koşul: IBS < 0,20. Düşüş şartı yok, filtre yok.

**Giriş:** Yalnız **C0**, iki yoldan biriyle:
- **(a) Ana yol, denetçi düzeltmesi:** Resmî kapanıştan sonra kesin IBS'yi gör. After-hours'ta (kış **TR 00:00-01:00**, yaz 23:00-00:00) resmî kapanış fiyatı **+ 2-5 sent limit** emirle, **tam adet** al. Denetçinin ölçümüne göre bu yolun maliyeti ~6 bp.
- **(b) İkinci yol:** Kapanıştan dakikalar önce (kış TR 23:45-23:58) anlık IBS ile piyasa ya da agresif limit emir. Kapanış öncesi IBS'yi yanlış sınıflama riski yüzünden maliyeti ~15-20 bp.

**Ertesi açılışta girme:** O1'de kenar +17 bp'ye, C1'de +2 bp'ye düşüyor. Kenarın tamamı ilk gecede.

**Çıkış:** Ertesi işlem günü kapanışa yakın, ya da after-hours limitle. Ertesi gün de IBS < 0,20 olacaksa satma, bir gün daha tut; komisyondan tasarruf edersin.

**Rakamlar (son kontrol):**
- C0: n=483, +42 bp (t 3,7), kazanma %58, ~50 işlem/yıl, en kötü işlem −%10,7.
- 1.000 $'da +24 bp.
- Denetçinin gerçekçi tahmini: 2.500 $'da 31-36 bp; 1.000 $'da eşik altı.
- SOXX (kopya): +44 bp.
- SOXL (3x, A2-3x, zayıf): +148 bp ama maxDD −%53; SOXL şu an 52 haftalık zirvesinin −%85 altında.

**Oynaklık rejimine göre:**

| Rejim | Net (bp) | t |
|---|---|---|
| Düşük | +14 | 1,1 |
| Orta | +38 | 2,4 |
| Yüksek | +65 | 2,7 |
| 2026 | +109 (n=38) | — |

Kenar sakin dönemlerde neredeyse yok.

**Yakın olay riski:** NVDA bilançosu 17.11.2026 kapanış sonrası (Nasdaq/Zacks tahmini tarih; teyit edin). 17.11'de alınan A2 pozisyonu ya da açık bir A1 pozisyonu bilanço gecesinin boşluğunu taşır; o gece girmemeyi düşün.

### A1 ve A2 birlikte

İkisi aynı risk faktörü: A1 sinyallerinin ~%90'ı A2 sinyal günlerine düşüyor (A2 sinyallerinin ise ~üçte biri A1 ile aynı gün); pozisyondaki günlük getiri korelasyonu 0,27. Kural: **A1 ana kural; A2 yalnız A1'de pozisyon yokken tam boyutla, varsa yarım boyutla.**

## 3. Zayıf kanıtlı kurallar (Kademe B: kağıt üstünde izle ya da çok küçük boyut)

B4 dışındakiler kabul eşiğini biçimsel olarak geçiyor ama denetçinin sağlamlık testlerinden tam geçemiyor. Rakamlar ana ajanın son kontrolünden (2.500 $, ana giriş modu).

| Kod | Kural | Araç | Giriş · tutuş | Net bp (t) · C0/O1/C1 | Neden zayıf |
|---|---|---|---|---|---|
| B1 | SPY IBS < 0,10 + düşüş | SPY (SSO / SPXL) | C1 · 3 gün | +54 (2,9) · 37/26/54 | Seçilmiş "sivri tepe"; seçim düzeltmeli p = 0,20. VIX < 20'de 1.000 $'da negatif. QQQ ile aynı gün sinyal verirse yalnız A1 |
| B2 | GDXJ IBS < 0,10 + düşüş | GDXJ (JNUG) | C0 · 3 gün | +102 (3,4) · 102/68/24 | Madenci havuzunda IS kanıtı yok (t 0,5); eşik komşuluğunda IS çöküyor. Kapanışa bağımlı: kapanış kaçarsa atla. maxDD −%25 |
| B3a / B3b | Ay sonu: son işlem günü kapanışı → yeni ayın 3. işlem günü kapanışı | GDX (B3a) ya da GLD (B3b) | C0 · 3 gün | GDX +74 (2,0); GLD +34 (2,2) | En iyi 5 işlem çıkarılınca t < 1,2; son yıllara bağımlı. İkisi aynı bahis |
| B4 | SPY ≤ −%1,5 olan günde SPY'dan çok düşen Asya ETF'leri | EWJ, EWY, EWT, FXI, EWA, EWH | C0 · 1 gün | +57 (işlem bazında t 3,2; **gün kümeli t 1,9**) · 57/−3/29 | Aynı gün açılan işlemler bağımsız değil: gün bazında t 1,9, eşik altı. En iyi 5 gün çıkarılınca t 0,8. Ertesi açılışta girmek zararlı |
| B5 | EWY IBS < 0,10 + düşüş | EWY (KORU) | C0 · 1 gün | +42 (3,1) · 42/6/−9 | Taramadan seçildi; 2026'nın aşırı oynaklık rejimine bağlı |
| B6 | 10Y Hazine ihalesinden 3 iş günü önce kapanışta al, ihaleden 1 gün önce kapanışta sat | TBT (tercih) ya da TMV | C0 · 2 gün | TBT +61 (2,8); TMV +102 (3,1) | 2002-2016'da çalışmıyor; global FDR yok; ters kaldıraçlı ürün; Midas doğrulanmadı |
| B7 | EIA doğalgaz raporundan önceki gün kapanışta al, rapor günü kapanışında sat (yalnız Kasım-Mart) | KOLD ⚠ | C0 · 1 gün | +118 (2,5) · 118/79/−27 | Mevsim ayrımı sonradan yapıldı; en iyi 10 işlem çıkarılınca t 0,6; PTP; tek işlemde −%17 |
| B8 | USO alt Bollinger (20, 2) kırılımı → ertesi gün kapanışta al, 2 gün tut | USO ⚠ | C1 · 2 gün | +108 (2,8) · −35/−4/108 | Genel taramadan seçildi; yalnız gecikmeli girişte çalışıyor; evrende tekrar etmiyor. TradingView'da StdDev **2,05** girin (popülasyon std farkı) |
| B9 | SVXY RSI(2) < 10 ve SVXY > SMA200 | SVXY ⚠; PTP teyidi yoksa aynı sinyalle **QQQ / QLD** | C0 · 2 gün | +157 (3,2) · 157/108/−28 | IS kanıtı yalnız 2021; 2010-2018 vekilinde kenar 0; Şubat 2018 tipi kuyruk riski. SVIX elendi |
| B10 | Mega-cap hisse RSI(2) < 10 ve hisse > SMA200; hisse > SMA5 kapanınca ya da en geç 3 gün sonra çık | 2x ETF: NVDL, TSLL, AMZU, MSFU, GGLL (AAPU, METU yedek). Kaldıraçlı ETF yoksa ya da yüksek oynaklık rejiminde (şu an) **hissenin kendisi** | C0 · ≤ 3 gün | ETF sepeti +120 (2,7; gün kümeli 2,65) · 120/104/98 | Sonradan seçilmiş kazanan hisseler: aynı kural önceden seçilmiş 47 hissede çalışmıyor (+12 bp, t 0,8). 2020 ve 2024'e bağlı. Test edilen hâl: her sinyale eşit pay (aynı anda medyan 2, en çok 7 hisse); sermaye kısıtlıysa en düşük RSI(2)'li 2 hisse seçimi test edilmedi |
| F | IBIT/BTC kapanış > SMA10 > SMA50 | (filtre) | — | IBIT +30 (0,6) | **Strateji değil**; en fazla "BTC trendi yukarı mı" filtresi |

**Takvimli B kurallarının yakın tarihleri** (`kod/sinyal.py` her akşam hesaplar):
- **Ay sonu (B3):** giriş 30.11.2026 kapanışı (TR 01.12 00:00), çıkış 03.12.2026 kapanışı.
- **10Y ihale (B6):** 10.11.2026 ihalesinin pozisyonu 09.11 kapanışında kapanır. Sonraki ihale 08.12.2026; giriş 03.12 kapanışı.
- **EIA doğalgaz (B7):** raporlar 13.11, 19.11, 25.11; girişler birer gün önce kapanışta.

**Takvim dosyaları sınırlı:** EIA takvimi 31.12.2026'da, 10Y ihale takvimi 08.12.2026'da bitiyor. Bitince betik uyarır. EIA için kural tabanlı Perşembe tarihleri üretir. Güncelleme kaynakları:
- ir.eia.gov/ngs/schedule.html
- TreasuryDirect "Tentative Auction Schedule"
- Hazine fiscaldata "upcoming auctions" API'si (betik bunu da sorgular)

## 4. Popüler ama çalışmayanlar

Ayrıntı: `notlar/aile_*.md` ve `notlar/denetim_*.md`.

**Doğalgaz (UNG, BOIL, KOLD):**
- Hiçbir long kural maliyeti aşmıyor.
- BOIL'ün koşulsuz bozulması günde −36 bp, UNG'ninki −10 bp.
- EIA günü (Perşembe 10:30 ET = kış TR 18:30) UNG brüt −28 bp; 2018-2026'da her yıl negatif.
- Kontango (UNG/UNL), roll pencereleri, vade günü, mevsim ve büyük gün sonrası devam/dönüş testleri ya kırılgan çıktı ya da IS/OOS'ta işaret değiştirdi.
- **Tek sağlam kural bir kaçınma kuralı:** UNG/BOIL long pozisyonunu EIA raporuna taşıma.

**Petrol (USO, UCO, XLE, XOP):**
- EIA petrol raporu günü, OVX, Brent-WTI farkı ve enerji hissesi-petrol yetişmesi testleri işe yaramadı.
- **OVX yalnız boyut bilgisi taşıyor:** OVX ≥ 1,25 × SMA20 olduktan sonraki 3 günde USO'nun mutlak hareketi 2,3 kat. Bu durumda pozisyonu küçült.
- UCO artık tam 2x USO gibi davranmıyor; 2026 betası 1,13.
- PTP'siz enerji aracı XLE ya da XOP (40 Act fonu).

**Altın ve gümüş (GLD, SLV):**
- Reel faiz ve dolar sinyalleri, FOMC sonrası (işaret tersine), altın/gümüş oranı, GVZ ve RSI(2) testleri işe yaramadı.
- Altının getirisi gece oluşuyor (kapanış → açılış +5 bp/gün, t 3,2; gün içi ≈ 0). Ama her gün işlem yapınca maliyet bunu yiyor.
- Kalan tek kural ay sonu (B3b, zayıf).
- Kaldıraçlı metal ürünleri (UGL, AGQ, ZSL, GLL) PTP yapısında.

**VIX ürünleri (VXX, UVXY, UVIX):**
- 1-3 günlük hiçbir long kural pozitif değil. Koşulsuz kayıp günde VXX −9,6 bp, UVXY −18 bp, UVIX −35 bp.
- Kontango taşıma kuralı 2022 sonrasında negatif. VIX sıçramasından sonra uzun vol almak kaybettiriyor.

**Kripto (IBIT, ETHA, BITX…):**
- Perşembe etkisi çürütüldü. Hafta sonu etkisi, gece primi, momentum ve dönüş testleri maliyet sonrası çalışmadı.
- Kaldıraçlı BTC ürünleri 2×IBIT'e göre günde ~11 bp kaybediyor.
- `COINBASE:BTCUSD`, IBIT'in açılış boşluğunun %96'sını açıklıyor; öncü değil, izleme aracı.

**Döviz (UUP, FXE, FXY, FXB, YCS…):**
- Günlük hareketler küçük, maliyet ise yüksek. UUP: 35 bp oynaklığa 20 bp maliyet. FXE ve FXY: ~34-51 bp oynaklığa 27 bp maliyet; ikisi de ~10 mn $/gün likiditede.
- FOMC günü (net −22..−41 bp), FXY güvenli liman (−39 bp), ay sonu USD dengelemesi (−24 bp) ve yen-faiz farkı kuralları net negatif.
- "ABD hisseleri dün yükseldiyse döviz bugün yükselir" gecikmesi gerçek (t ≈ 4-5) ama 1 sd başına 5-9 bp; işlenemez.
- UUP ve UDN Invesco DB yapısında (K-1).
- İzleme kodları: `TVC:DXY`, `FX_IDC:EURUSD`, `FX_IDC:USDJPY`.

**Tarım (DBA, CORN, WEAT, SOYB, CANE):**
- 8 küme temsilcisinin hiçbirinde tutarlı sinyal yok.
- Likidite düşük (CORN 4,7 mn $, SOYB 1,8 mn $/gün), maliyet 20-47 bp. Hepsi K-1 yapısında (Invesco DB, Teucrium).
- İzleme kodları: `CBOT:ZC1!`, `CBOT:ZW1!`, `CBOT:ZS1!`, `ICEUS:SB1!`.

**Sektör rotasyonu:**
- "Aşırı satılan sektörü al" testi ters çıktı: geride kalan sektör ertesi gün de geride kaldı (−14 bp, t −2,2).
- 1-3 günlük sektör momentumu ve sektör çiftleri yok.
- Sektörlerin "33/34'ünde pozitif" görünen IBS sonucu tek bir piyasa etkisi (etkin N ≈ 2,6).

**Takvim etkileri:** FOMC öncesi drift (2015 sonrası yok), CPI/NFP duyuru günleri, OPEX haftası, endekslerde ay dönümü, tatil öncesi ve Turnaround Tuesday maliyet sonrası ya eşik altında ya da negatif.

**Kırılım ve momentum:** 20 günlük zirve kırılımı neredeyse her ailede **negatif**. 1-3 günde trend takibi değil, ortalamaya dönüş çalışıyor.

**Ters ETF'lerle kısa yön:** SQQQ, SPXU, SOXS, TSLQ, NVDS gibi ürünlerde varyantların neredeyse tamamı net negatif. Yalnız koruma amaçlı kullanılabilir.

**Ülke ETF'lerinde "NAV'dan sapma düzeltmesi":** SPY'a göre kalıntı vekiliyle test edildi; maliyet sonrası yok. Kalan tek şey B4'ün dar sürümü (eşik altı).

**Kapsam dışı kalanlar:**
- Evrende olmayanlar: MSTX (2x MSTR) ve SOL/XRP gibi yeni spot kripto ETF'leri.
- Verisi indirilemeyenler: EGPT, FM, GXG, PAK, SPLG.
- 10 mn $/gün altındaki 26 ülke ETF'i maliyet nedeniyle elendi (TUR dahil: 6,8 mn $/gün, 27 bp).

## 5. İzleme listesi

**Kapsam:** 77 ETF.
- **Kabul (22):** A 2, B 13, C 7.
- **Yedek (55):** A 3 (QLD, TQQQ, SOXX), B 18, C 34.

Tam tablo: **`IZLEME_LISTESI.md`**; kural kodları, araç rolleri, sürücüler ve gerçek zamanlı kodlarla. Altında "popüler ama alınmayanlar, neden?" bölümü var. ETF başına kart: **`kartlar/<SYM>.md`**.

**TradingView'a içe aktarma:** İzleme listesi menüsünden "Listeyi içe aktar" ile yüklenir.
- `izleme_listeleri/TUM_ETF_bolumlu.txt`: tekrarsız 150 sembol. Önce aile bazında ETF bölümleri gelir, sonra "Ortak sürücüler" ve "Gerçek zamanlı izleme" bölümleri.
- Ayrıca aile bazında ayrı dosyalar var: `<aile>.txt`.

Çekirdek liste (kabul):

| Kademe | ETF (TradingView) | Not |
|---|---|---|
| A | `NASDAQ:QQQ` (A1), `NASDAQ:SMH` (A2) | Doğrulanmış kurallar. Araçlar (yedek): `AMEX:QLD`, `NASDAQ:TQQQ` (A1), `NASDAQ:SOXX` (A2) |
| B | `AMEX:SPY` (B1), `AMEX:GDXJ` (B2), `AMEX:GDX` (B3a), `AMEX:GLD` (B3b), `AMEX:EWY` (B4, B5), `AMEX:EWT` ve `AMEX:FXI` (B4), `CBOE:SVXY`⚠ (B9), `NASDAQ:NVDL`, `NASDAQ:TSLL`, `NASDAQ:AMZU`, `NASDAQ:MSFU`, `NASDAQ:GGLL` (B10) | Zayıf kurallar. TBT ve TMV (B6), KOLD⚠ (B7), USO⚠ (B8) yedekte |
| C | `AMEX:XLE`, `AMEX:XOP`, `NASDAQ:TLT`, `NASDAQ:IBIT`, `AMEX:GBTC`, `NASDAQ:ETHA`, `AMEX:ETHE` | Kural yok; likit ve popüler, sürücüleriyle takip. IBIT/GBTC/ETHA için F yalnız filtre |

Doğalgaz (UNG⚠, KOLD⚠), petrol (USO⚠, UCO⚠, SCO⚠, BNO⚠), gümüş (SLV), bakır (COPX), VIX (VXX) ve küçük şirket (IWM) gibi popüler ürünler **yedek** olarak kartlarda. BOIL, UVXY, SQQQ, SOXS, AGQ, TUR ve UUP gibi ürünlerin neden listede olmadığı `IZLEME_LISTESI.md` sonunda.

## 6. Portföy simülasyonu (10.000 $, A1 + A2)

`kod/ek_analiz.py`, `sonuclar/ek_portfoy*.csv`. Varsayımlar:
- Komisyon 1,5 $/emir, makas yarı yarıya giriş ve çıkışta.
- Günlük kapanışla değerleme, nakit faizsiz, vergi öncesi.
- A2 C0 kapanış fiyatıyla; gerçekçi after-hours girişi bunu işlem başına ~6 bp düşürür.

| Ağırlık (özsermayenin) | Yıllık bileşik | Yıllık oynaklık | En büyük düşüş | İşlem/yıl | Piyasada gün |
|---|---|---|---|---|---|
| **A1 %50 + A2 %25** | **%13,3** | %8,8 | **−%8,8** (08.04.2025) | ~68 | %37 |
| A1 %100 | %14,6 | %12,8 | −%12,1 (16.03.2020) | ~18 | %22 |
| A2 %100 | %28,0 | %18,1 | −%16,8 (14.10.2022) | ~50 | %20 |
| A1 %25 + A2 %25 | %9,2 | %6,2 | −%6,7 | ~68 | %37 |
| *Karşılaştırma: QQQ al-tut* | *%19,3* | — | *−%35,1* | — | *%100* |

- **Yıllık getiriler (A1 %50 + A2 %25):** 2017 +5,3 · 2018 +8,8 · 2019 +7,4 · 2020 +38,0 · 2021 +7,8 · 2022 +4,5 · 2023 +21,3 · 2024 +14,8 · 2025 +10,6 · 2026 +14,2 (%; önceki yıl sonuna göre). Kayıplı yıl yok, ama getirinin büyük kısmı kriz yıllarında (2020) geliyor.
- **Not:** A1 %100 tek başına %14,6 getiriyor; A1 %50 + A2 %25 bileşimi getiriden biraz feragat edip oynaklığı ve düşüşü azaltıyor.
- **A2'nin %100 sonucu iyimser.** Kapanış fiyatıyla giriş varsayıyor ve A2 tek bir bağımsız kümeye dayanıyor. Bunu hedef değil, üst sınır olarak okuyun.
- **Vergi:** Türkiye'de kazanç TL bazında beyan edilir (2026 tarifesi %15-40); net getiri buna göre düşer.

## 7. Akşam rutini (TR saati; kış saatine göre, yazın 1 saat erken)

**Kurulum (bir kez):**
- TradingView'da `kod/tradingview/ibs_dip.pine` ve `rsi2_dip.pine` göstergelerini Pine düzenleyiciye yapıştırıp grafiğe ekle (derlenmedi; hata çıkarsa bildir).
- Alarmları "**Bar kapanışında bir kez**" ile kur; kış saatinde TR 00:00'da (resmî kapanışta) tetiklenir. Üç alarm var: "IBS sinyali" (C0 kurallarında şimdi after-hours limitle al; C1'de bir şey yapma), "Yarın al (C1)" (ertesi gün kapanıştan ~10 dk önce al) ve "Yarın sat" (ertesi gün kapanışa yakın sat). SOXX grafiğinde sinyal SMH'den hesaplanır.
- Python kullanacaksan: `python3 -m venv .venv` ve `.venv/bin/pip install requests numpy pandas tzdata`. Sonra `.venv/bin/python kod/sinyal.py` (Windows: `py -m venv .venv`, `.venv\Scripts\python kod\sinyal.py`).

**Yalnız TradingView ile izlenebilenler:**
- A1, A2, B1, B2, B5: `ibs_dip.pine`.
- B9, B10: `rsi2_dip.pine`.
- B8: Bollinger Bantları (20, StdDev 2,05).

**Elle kontrol edilenler:**
- B3: ayın son işlem günü.
- B4: SPY günlük ≤ −%1,5 mi? Öyleyse Asya ETF'lerinin günlük değişimini SPY'ınkiyle karşılaştır.
- B6: TreasuryDirect'te 10Y ihale tarihi.
- B7: EIA takvimi.

**Her akşam (karar ağacı):**
1. **~17:30, isteğe bağlı:** `CME_MINI:NQ1!`, `CME_MINI:ES1!`, `COINBASE:BTCUSD` ile gece boşluğunu gör.
   - Bekleyen bir **O1** girişin varsa açılışta emri ver.
   - Açık pozisyonda panik satışı yapma; kurallar stopsuz test edildi.
2. **~23:45, kapanışa 15 dk kala:** Bugün çıkış günü olan pozisyonları sat. **İstisna (A2):** SMH'de anlık IBS yine < 0,20 ise satma, bir gün daha tut. Yarım günlerde (27.11, 24.12) bu adım **TR 20:45**'te.
   - **A1'i C1 ile uyguluyorsan:** dün gece A1 sinyali geldiyse **şimdi al.**
   - **C0 kuralları (A2, B2, B5…) için** kapanış öncesi giriş istiyorsan: `sinyal.py --canli` ya da göstergedeki anlık IBS'ye bak (§2'deki 'ikinci yol').
3. **00:00 sonrası, resmî kapanış** (yarım günlerde 21:00 sonrası; after-hours penceresi 21:00-01:00): `python kod/sinyal.py` çalıştır ya da gelen alarmlara bak. Bu, kesin kapanışla değerlendirme. **Açık pozisyonun varken aynı kuraldan gelen yeni sinyal yok sayılır** (betik ve gösterge bunu 'YOK SAY' / gri üçgen olarak gösterir).
   - **A1 sinyali varsa:** C1 kullanıyorsan **bu gece bir şey yapma**; yarın 23:50'de al. C0 kullanıyorsan şimdi after-hours limitle al (ya da bir dahaki sefere kapanış öncesi tahminle, §2). **İkisini birden yapma.**
   - **A2 sinyali varsa:** şimdi (00:00-01:00) after-hours'ta kapanış + 2-5 sent limitle, tam adet al.
4. **Haftalık:** Takvimli B kuralları, önemli veriler ve bilançolar.
   - CPI ve NFP: TR 16:30. FOMC kararı: TR 22:00. EIA doğalgaz: Perşembe TR 18:30.
   - NVDA bilançosu 17.11 kapanış sonrası (tahmini tarih).

Örnek çıktı (06.11.2026 kapanışı): `sonuclar/sinyal_ornek_2026-11-06.txt`.
- QQQ'da 02.11 ve 05.11'de sinyal var. C1'de 02.11 sinyaliyle 03.11'de girildi, 06.11'de çıkıldı; 05.11 sinyali pozisyon açıkken geldiği için **yok sayıldı**. C0 kullananın 05.11 girişi 10.11'de kapanır.
- SMH'nin 05.11 sinyali 06.11'de kapandı.
- B10'da 04.11 TSLA sinyali var (pozisyon en geç 09.11'de kapanır). Yüksek oynaklık rejimi nedeniyle bu sinyalde araç TSLL değil **TSLA hissesinin kendisi** olmalıydı; betik artık bunu uyarıyor.
- Bugün yeni A sinyali yok.

## 8. Risk ve pozisyon kuralları

**Eşzamanlı pozisyon kuralı (tek kural):**
- **Teknoloji riski tek bütçe:** A1, A2, B1, B9 ve B10 aynı risk faktörü (ABD teknoloji / risk iştahı).
  - Aynı anda en fazla A1 tam (özsermayenin ~%50'si) + A2 yarım (~%25).
  - B1 sinyali A1 ile aynı gün gelirse yalnız A1. B10'da her sinyale eşit küçük pay (test edilen hâl); sermaye kısıtlıysa en çok 2 hisse (seçim kuralı test edilmedi).
- **Diğer B kuralları:** her biri en fazla ~%10-15, toplam en fazla 3 açık pozisyon.

**Minimum sermaye:**
- A1 için ≥ 2.500 $; A1 + A2 için ≥ 5.000 $.
- Daha küçük hesapta yalnız A1, 1x QQQ ile. 1.000 $'da A1 hâlâ +50 bp; A2 ise eşiğin altında kalıyor.

**Oynaklık ayarı:** Tutar = normal tutar × min(1, medyan oynaklık / şu anki 20 günlük oynaklık). Şu an QQQ ve SMH için ~0,5.

**Kaldıraç:**
- 2x araçta 1x tutarın yarısı, 3x araçta üçte biri.
- Yüksek oynaklık rejiminde kaldıraçlı araç yok.
- Kuyruk örnekleri: TQQQ −%31 (tek işlem), SOXL maxDD −%53, NVDL/TSLL tek işlemde −%28'e kadar.

**PTP (⚠):** Midas'ta "PTP" ibaresi ve %10 brüt kesinti olmadığı teyit edilmeden kısa vadeli işlem yapma. %10 kesinti işlem başına ~1.000 bp demek; hiçbir kural bunu karşılamaz.

**Ürün bulunurluğu:** Kaldıraçlı, ters, VIX ve tek hisse kaldıraçlı ETF'leri uygulamada arayıp gör. Yoksa 1x araçla devam et; kuralların sinyali 1x araçta da geçerli.

**Olay günleri:** CPI, NFP, FOMC ve büyük bilançolar gece boşluğu yaratabilir. Kurallar bu günleri dışlamıyor; dışlamak kendi tercihin.

**Stop:** Test edilmedi. Koyacaksan geniş tut, ama kenarı değiştirebileceğini bil.

## 9. Yöntem, veri ve sınırlamalar

**Veri:**
- Nasdaq API: 10 yıllık günlük OHLCV, bölünme düzeltmeli. 318 ETF'den 313'ü indi.
- Yahoo: dağıtım ve bölünme olayları. Yahoo'nun bölünme bazı Nasdaq fiyatlarıyla birebir eşleşiyor (`sonuclar/yahoo_nasdaq_fiyat_orani.csv`).
- Cboe: VIX, VIX9D, VIX3M, VIX6M, VVIX, OVX, GVZ (1990+).
- Coinbase: BTC/ETH günlük ve saatlik veri.
- ABD Hazinesi: nominal ve reel getiri eğrileri. FRED proxy üzerinden erişilemedi.
- Dayanak hisseler: Nasdaq.
- Olay takvimleri (`data/events/`): FOMC, CPI, NFP, EIA, OPEX, NYSE tatil/yarım gün, NG/CL/VIX vadeleri, UNG/USO/BOIL-KOLD roll pencereleri, 10Y/30Y ihaleleri. Kaynaklı; kuraldan hesaplananlar işaretli.

**Veri düzeltmeleri:**
- Nasdaq, NYSE Arca ve Cboe listeli 267 ETF'in dağıtımlarını vermiyor; Yahoo ile giderildi. Etkisi küçük değildi: ex-date'ler aşağı yanlıydı ve sahte "yetişme" sinyalleri doğuyordu.
- Bölünmeye göre ölçeklenmemiş Nasdaq temettüleri (NVDL, SOXX…) düzeltildi.
- Hatalı barlar çıkarıldı: DFEN 2024-06-03, IAU 2021-03-08.
- Tröst dönemleri çıkarıldı: GBTC 2024-01 öncesi, ETHE 2024-07 öncesi. USHY 2019-04 öncesi çıkarıldı.
- Gerçek aşırı hareketler korundu (`sonuclar/veri_kalitesi.csv`).

**Zamanlama:**
- Sinyal yalnız t kapanışına kadar bilinen veriyle hesaplandı (`kod/lib.py`).
- C0 kapanış fiyatıyla hesaplandığı için hafif iyimser; bu yüzden O1 ve C1 de raporlandı. Denetçi A2 için gün içi veriyle bu iyimserliği ölçtü.
- VIX'in kapanışı 16:15 ET; BTC günlük mumu 00:00 UTC'de kapanıyor. Bunun yerine 16:00 ET saatlik fiyat kullanıldı.

**Maliyet:** 2 × 1,5 $ komisyon + likidite kademesine göre makas. Makas en az 1 sentlik fiyat adımı kadar alındı.

**Çoklu test:**
- Genel kütüphanede 92.664 test var. **Tek yönlü katı BH-FDR'de hiçbir test geçmiyor.**
- A1 ve A2'nin dayanağı tek bir testin t'si değil. Dayanaklar şunlar: önceden kayıtlı literatür hipotezi (IBS etkisi), aile tutarlılığı, parametre platosu, permütasyon ve üç giriş modunda sağlamlık. Bu yüzden güven **orta**.
- Sepet kurallarında (B4, B10) gün kümeli t de verildi.

**Sınırlamalar:**
- Veri 10 yılla sınırlı (2016-2026); uzun bir ayı piyasası yok. Gün içi veri yok.
- Kaldıraçlı ETF'lerin kaldıracı dönem içinde değişti: NUGT/JNUG 2020'de 3x'ten 2x'e, Direxion tek hisse ETF'leri 2024'e kadar 1,5x, SVXY 2018'de −1x'ten −0,5x'e indi.
- Midas'ta ürün bulunurluğu ve PTP uygulaması resmî olarak doğrulanamadı.
- Literatürdeki IBS/RSI(2) etkilerinin yayın sonrasında zayıfladığı biliniyor. Gerçek performans backtestin altında olabilir; denetçilerin "gerçekçi beklenti" aralıkları bunu yansıtıyor.

## 10. Dosyalar

| Yol | İçerik |
|---|---|
| `RAPOR.md` | Bu rapor |
| `IZLEME_LISTESI.md` | 77 ETF'lik izleme listesi (kademe, TV kodu, maliyet, kural kodu ve rol, sürücüler, gerçek zamanlı kodlar) + popüler ama alınmayanlar |
| `kartlar/<SYM>.md` | ETF başına kart: kurallar (A1…B10 kodlarıyla; ajan, denetçi ve son kontrol rakamları), sürücüler, öncüler, gerçek zamanlı izleme, takvim riskleri |
| `izleme_listeleri/*.txt` | TradingView içe aktarma dosyaları (tümü tekrarsız; aile bazında ayrı) |
| `kod/sinyal.py` | Akşam kontrol betiği (`--canli` ile kapanış öncesi; yarım gün ve takvim uyarıları) |
| `kod/tradingview/ibs_dip.pine`, `rsi2_dip.pine` | TradingView göstergeleri (Pine v5; sembole göre otomatik ön ayar; derlenmedi) |
| `kod/kurallar.py` | Kural kataloğu (A1-B10, F): kartlar ve tablo bu tek kaynaktan üretilir |
| `notlar/aile_<aile>.md`, `notlar/denetim_<aile>.md` | Aile ajanlarının ve denetçilerin ayrıntılı notları |
| `notlar/midas_kosullari.md`, `literatur.md`, `hipotezler.csv`, `takvim_notlari.md` | Midas koşulları, literatür, önceden kayıtlı hipotezler, takvimler |
| `sonuclar/son_kontrol*.csv`, `ek_*.csv` | Ana ajanın düzeltilmiş veriyle son kontrolü (3 mod × 3 pozisyon boyutu, gün kümeli t, yıllık, korelasyon), rejim ve portföy analizleri |
| `sonuclar/genel_tum.csv.gz`, `leadlag_sweep.csv`, `tarama.csv` | Genel kütüphane, lead-lag taraması, işlenebilirlik |
| `sonuclar/izleme_son.csv`, `kart_indeksi.csv` | Uzlaştırılmış izleme kararları (ajan → denetçi → nihai) |
| `sonuclar/tv_etf.csv`, `tv_dogrulama.csv` | TradingView kod doğrulaması (sayfa okunarak) |
| `kod/` | Veri indirme (`dl.py`, `temettu_yahoo.py`), ortak kütüphane (`lib.py`), genel kütüphane (`strategies.py`, `run_generic.py`), tarama, lead-lag, son kontrol, ek analiz, kart üretici, aile ve denetim betikleri |

Ham veri (`data/`, olay takvimleri hariç) ve indirilen sayfalar (`ham_sayfalar/`) repoya eklenmedi; `kod/dl.py all` ve `kod/temettu_yahoo.py` ile yeniden indirilir.
