# Midas'ta ABD ETF'leriyle 1-3 günlük alım-satım: stratejiler, izleme listesi ve lead-lag (07.11.2026)

*Veri: 06.11.2026 kapanışına kadar. Yatırım tavsiyesi değildir. Geçmiş performans geleceği garanti etmez.*

## 0. Kısa cevap

**Ne yapıldı?**
- 9 aileye ayrılan 313 ABD ETF'i 10 yıllık günlük veriyle (2016-11 → 2026-11) tarandı. Aileler: ABD endeks, sektör, tek hisse kaldıraçlı, enerji/tarım, metal/madenci, tahvil/döviz, VIX, kripto ve ülke ETF'leri.
- Genel kütüphanede 31 sinyal, 3 giriş zamanı (kapanış, ertesi açılış, ertesi kapanış) ve 1/2/3 günlük tutuş birlikte denendi; bu 92.664 test demek. Buna aile başına binlerce özel test eklendi (FOMC, CPI, EIA, roll, ihale, VIX vade yapısı, BTC 7/24...).
- Her aday stratejiyi bağımsız bir denetçi kendi koduyla yeniden üretti. Denetçi ayrıca çoklu test, parametre komşuluğu, permütasyon, yıl yıl sonuçlar ve en iyi işlemler çıkarılınca ne kaldığı açısından çürütmeye çalıştı. Ardından ana ajan, dağıtım (temettü) verisi düzeltilmiş veride ortak bir motorla hepsini yeniden hesapladı.

**Sonuç sert:** Midas'ın 1,5 $ komisyonu ve makaslar düşüldükten sonra denetimden geçen yalnız **2 kural** var. İkisi de aynı mekanizmaya dayanıyor: teknoloji ve yarı iletken ETF'i günün dibinde kapanınca sonraki 1-3 günde toparlanıyor.

| Kod | Kural | Araç | Tutuş | Net beklenti (2.500 $) | Güven |
|---|---|---|---|---|---|
| **A1** | **QQQ:** IBS < 0,10 **ve** düşüş günü | QQQ (2x QLD / 3x TQQQ yalnız küçük payla) | 3 gün | denetçi gerçekçi tahmini **+45-55 bp/işlem**; backtest +68 bp (t 3,5) | orta |
| **A2** | **SMH:** IBS < 0,20 | SMH (ya da kopyası SOXX) | 1 gün | denetçi gerçekçi tahmini **+31-36 bp/işlem**; backtest +42 bp (t 3,7) | orta |

**IBS (internal bar strength):** IBS = (kapanış − günün düşüğü) / (günün yükseği − günün düşüğü). 0'a yakın değer, kapanışın günün dibinde olduğu anlamına gelir.

**Bunların dışındaki her şey:**
- **"Zayıf" kanıtlılar (Kademe B, 12 kural):** Kağıt üstünde izlenebilir ya da çok küçük boyutla denenebilir.
- **Çalışmayanlar:** Doğalgaz, petrol, altın-gümüş, VIX, kripto, sektör rotasyonu ve takvim etkileri (FOMC, CPI, ay sonu…) bunların çoğunu oluşturuyor. "Millet doğalgaz, altın trade ediyor" ama bu ürünlerde 1-3 günlük, maliyeti yenen, sağlam bir giriş kuralı bulunamadı.

**Lead-lag:**
- 1-3 günlük ufukta, maliyet sonrası işe yarayan **doğrulanmış gecikmeli öncü yok**. 313 ETF × 45 öncü = 13.694 çift tarandı.
- İlk taramada "anlamlı" görünen yüzlerce "yetişme" sinyali dağıtım verisindeki hatadan doğmuştu. Hata düzeltilince 288'den 2'ye indi.
- Doğru kullanım şu:
  1. **Aynı gün sürücüler:** ETF'yi neyin hareket ettirdiğini gösterir; öncü değildir.
  2. **Gerçek zamanlı izleme:** ETF kapalıyken işleyen vadeli, kripto ve döviz fiyatları ertesi açılış boşluğunu önceden gösterir.
- Her izleme ETF'i için bunlar TradingView kodlarıyla `kartlar/<SYM>.md` dosyalarında. Kodların tamamı sembol sayfası okunarak doğrulandı.

**Midas'a özgü üç pratik kural:**
1. **Pozisyon en az ~2.500 $ olsun.** 1.000 $'da komisyon gidiş-dönüş 30 bp eder ve SMH/SPY kenarını yer.
2. **"Kapanışta al" iki yolla yapılır.** Midas'ta MOC/LOC (kapanışta piyasa emri) yok. Seçenekler: kapanıştan ~5-10 dk önce emir (kışın TR 23:50, yazın 22:50) ya da kapanıştan sonra after-hours'ta (kış 00:00-04:00) kapanış fiyatına yakın **limit** emir.
3. **PTP/K-1 ürünlerine dikkat.** UNG, USO, BOIL, KOLD, UCO, SCO, UVXY, SVXY gibi ürünlerde satışta %10 brüt kesinti riski var. Midas'ta teyit etmeden bu ürünlerle kısa vadeli işlem yapma.

## 1. Midas koşulları ve saatler

Kaynak: `notlar/midas_kosullari.md`; kaynaklı ve tarihli, `.json` sürümü de var. Özet:

| Konu | Durum |
|---|---|
| Komisyon | Emir başına 1,5 $ (gidiş-dönüş 3 $). 1.000 $'da 30 bp, 2.500 $'da 12 bp, 10.000 $'da 3 bp |
| Açığa satış / kredi | Yok. Kısa yön ancak ters ETF ile, ve ters ETF'ler testlerde neredeyse her yerde zarar ettirdi |
| Seans (TR saati) | Kış (1 Kas 2026 – 14 Mar 2027): 17:30-00:00. Yaz: 16:30-23:00 |
| Pre-market / after-hours | Kış 12:00-17:30 / 00:00-04:00. Yaz 11:00-16:30 / 23:00-03:00. **Yalnız limit emir** |
| Emir tipleri | Piyasa, limit, stop, stop-limit, kâr al/zarar durdur. **MOC/LOC yok**, takip eden stop yok |
| Kesirli alım | Var (ETF'lerde de) |
| Ürün bulunurluğu | Kaldıraçlı/ters/VIX/tek hisse kaldıraçlı ETF'ler resmî olarak **doğrulanamadı** (TQQQ "muhtemel"). GBTC ve ETHE sembol sayfası doğrulanmış. Uygulamada sembolü arayarak teyit edin |
| PTP/K-1 | UNG, USO, BOIL, KOLD, UCO, SCO, UVXY, SVXY: uygulamada "PTP" ibaresi var. 2024'te UNG satışında geçici %10 brüt kesinti bildirilmiş |
| Vergi | ABD temettü stopajı %20 (W-8BEN). Türkiye'de yurt dışı alım-satım kazancı tutar ne olursa olsun yıllık beyan; zarar yalnız aynı yıl içinde mahsup edilebilir |
| Yarım günler | 27.11.2026 ve 24.12.2026: kapanış 13:00 ET = TR 21:00 |

## 2. Uygulanabilir kurallar (Kademe A)

### A1 — QQQ "zayıf kapanış" dönüşü, 3 gün

**Sinyal (t günü kapanışı):**
- Grafik: `NASDAQ:QQQ` günlük mum.
- Koşul: IBS < 0,10 **ve** kapanış < önceki gün kapanışı. Yani gün düşüşle ve günün dibine çok yakın kapanmış.
- TradingView göstergesi: `kod/tradingview/ibs_dip.pine` (eşik 0,10, düşüş şartı açık, tutuş 3).

**Giriş:**
- **Ana yol (C1):** Sinyali gece gör. Ertesi işlem günü kapanıştan ~5-10 dk önce al: kış TR ~23:50, yaz ~22:50.
- **Alternatif (C0):** Sinyal günü kapanışa yakın, ya da kapanış sonrası after-hours'ta limit emirle gir.

**Çıkış:** Girişten 3 işlem günü sonra, kapanışa yakın sat. Stop yok; backtest stopsuz yapıldı. Pozisyondayken gelen yeni sinyal yok sayılır.

**Rakamlar (2.500 $, işlem başı net):**

| Kaynak | Sonuç |
|---|---|
| Aile ajanı | C1 +71 bp, t 3,46, n=169. IS +76 / OOS +66 bp. Yılların %100'ü pozitif |
| Ana ajan son kontrolü (dağıtım düzeltmeli veri) | C0 **+77** (t 3,9) · O1 **+56** (t 3,1) · C1 **+68** (t 3,5). En iyi 5 işlem çıkarılınca t 2,7; 2020 ve 2022 çıkarılınca t 3,3. 1.000 $'da +50 bp (t 2,6) |
| Denetçi | **"doğrulandı"**, ancak gerçekçi beklenti **+45-55 bp**. Seçim düzeltmeli p = 0,025-0,055 (yani sınırda). Kâr VIX ≥ 20 günlerinde daha yüksek: brüt 91 bp, VIX < 20'de 47 bp |
| Kaldıraçlı araçlar (C1) | QLD +145 bp, en kötü işlem −%19,6. TQQQ +220 bp, en kötü işlem **−%31** (Mart 2020). Kaldıraçlı kullanacaksan dayanak eşdeğeri tutarın 1/2-1/3'ü kadar |

**Riskler:**
- Örneklem 2016-2026'nın güçlü teknoloji dönemi; uzun bir ayı piyasası test edilmedi.
- 2024+ alt döneminde n=43 ve t 1,6.
- SPY'ın aynı kuralı (B1) ile sinyallerin %73'ü aynı gün. İkisini birlikte almak çeşitlendirme değil, riski ikiye katlar.

### A2 — SMH gün sonu zayıflığı dönüşü, 1 gün

**Sinyal (t kapanışı):**
- Grafik: `NASDAQ:SMH` günlük mum.
- Koşul: IBS < 0,20. Düşüş şartı yok, 200 günlük ortalama filtresi yok.

**Giriş:** Yalnız **C0**: sinyal günü kapanışında. Bunu yapmanın iki yolu var:
- (a) Kapanıştan dakikalar önce anlık IBS'yi hesaplayıp piyasa ya da agresif limit emirle gir (kış TR 23:45-23:58).
- (b) Daha temiz yol: resmi kapanıştan sonra kesin IBS'yi gör ve after-hours'ta (kış 00:00-04:00) kapanış fiyatına yakın **limit** emirle gir. Denetçi bu yolun maliyetini ~6 bp, kapanış öncesi tahminle girmenin maliyetini ~15-20 bp ölçtü.

**Çıkış:** Ertesi işlem günü kapanışa yakın. Ertesi gün de IBS < 0,20 olursa pozisyonu bir gün daha tut; bu, komisyon tasarrufu sağlar.

**Rakamlar:**
- Son kontrol, 2.500 $: C0 **+42 bp** (t 3,7, n=483). O1 +17 bp. **C1 +2 bp.**
- Kenar neredeyse tamamen ilk gecede; kapanışta girmezsen yok.
- 1.000 $'da +24 bp. Denetçinin gerçekçi tahmini 2.500 $'da 31-36 bp; 1.000 $'da eşiğin altında.
- SOXX (kopya ETF): +44 bp.
- SOXL (3x): +148 bp ama Midas'ta doğrulanmadı ve maxDD −%53. SOXL Haziran 2026'dan beri −%82'de. "Zayıf" sayıldı.

**Riskler:** A1 ile aynı bahis: sinyallerin ~%70'i QQQ IBS < 0,20 ile aynı gün, pozisyondaki günlük getirilerin korelasyonu 0,27. Kenar oynaklık rejimine bağlı; sakin dönemlerde ~0.

**A1 ile A2 birlikte:** Toplam riski tek bütçe say. Pratik öneri: A1'i ana kural, A2'yi yalnız A1'de pozisyon yokken ya da yarım boyutla kullan.

## 3. Zayıf kanıtlı kurallar (Kademe B — kağıt üstünde izle ya da çok küçük boyut)

Hepsi "kabul eşiğini biçimsel olarak geçen ama denetçinin sağlamlık testlerinden tam geçemeyen" kurallar. Rakamlar ana ajanın son kontrolünden (2.500 $, ana giriş modu).

| Kod | Kural | Araç | Giriş · tutuş | Net bp (t) · C0/O1/C1 | Neden zayıf |
|---|---|---|---|---|---|
| B1 | SPY IBS < 0,10 + düşüş | SPY (SSO/SPXL) | C1 · 3 gün | +54 (2,9) · 37/26/54 | En iyi hücre "sivri tepe"; seçim düzeltmeli p = 0,20. VIX < 20'de 1.000 $'da negatif. QQQ ile aynı günler |
| B2 | GDXJ IBS < 0,10 + düşüş | GDXJ (JNUG) | C0 · 3 gün | +102 (3,4) · 102/68/24 | Madenci havuzunda IS kanıtı yok (t 0,5); eşik komşuluğunda IS çöküyor; kapanışa bağımlı; maxDD −%26 |
| B3 | Ay sonu: son işlem günü kapanışı → 3. gün kapanışı | GDX (ya da GLD) | C0 · 3 gün | GDX +74 (2,0); GLD +34 (2,2) | En iyi 5 işlem çıkarılınca t < 1,2; son 3 yıla bağımlı. GDX ve GLD aynı bahis |
| B4 | SPY ≤ −%1,5 olan günde SPY'dan çok düşen Asya ETF'lerini al | EWJ, EWY, EWT, FXI, EWA, EWH | C0 · 1 gün | +57 (3,2) · 57/−3/29 | Basit t (Newey-West'siz) 1,99; en iyi 5 gün çıkarılınca t 0,8; kenar gece boşluğunda. Ertesi açılışta girmek zararlı |
| B5 | EWY IBS < 0,10 + düşüş | EWY (KORU) | C0 · 1 gün | +42 (3,1) · 42/6/−9 | Taramadan seçildi; 2026'nın aşırı oynaklık rejimine bağlı |
| B6 | 10Y Hazine ihalesinden 3 iş günü önce al, ihaleden 1 gün önce sat | TMV (tercihen TBT) | C0 · 2 gün | TMV +102 (3,1); TBT +61 (2,8) | 2002-2016'da çalışmıyor; global FDR yok; −3x ters ürün; Midas doğrulanmadı |
| B7 | EIA doğalgaz raporundan önceki gün (yalnız Kasım-Mart) | KOLD ⚠PTP | C0 · 1 gün | +118 (2,5) · 118/79/−27 | Mevsim ayrımı sonradan yapıldı; en iyi 10 işlem çıkarılınca t 0,6; PTP; tek işlemde −%16 |
| B8 | USO alt Bollinger (20, 2) kırılımı → 1 gün bekle, 2 gün tut | USO ⚠PTP | C1 · 2 gün | +108 (2,8) · −35/−4/108 | Genel taramadan seçildi; yalnız 1 gün gecikmeli girişte çalışıyor; evrende tekrar etmiyor |
| B9 | SVXY RSI(2) < 10 ve SVXY > SMA200 | SVXY ⚠PTP | C0 · 2 gün | +157 (3,2) · 157/108/−28 | IS kanıtı yalnız 2021; 2010-2018 vekilinde kenar 0; Şubat 2018 tipi kuyruk |
| B10 | Mega-cap hisse RSI(2) < 10 ve hisse > SMA200 → aynı hissenin 2x ETF'i; hisse > SMA5 olunca ya da en geç 3 gün sonra çık | NVDL, TSLL, AMZU, MSFU, GGLL (AAPU, METU yedek) | C0 · ≤ 3 gün | ETF sepeti +120 (2,7) · 120/104/98 | Sonradan seçilmiş kazanan hisseler: aynı kural önceden seçilmiş 47 hissede çalışmıyor (+12 bp, t 0,8). 2020 ve 2024'e bağlı |
| — | IBIT trend filtresi (C > SMA10 > SMA50) | IBIT | C0 · 3 gün | +30 (0,6) | Strateji değil. IBIT döneminde anlamsız; en fazla "BTC trend yukarı mı" filtresi |

Takvimli B kurallarının yakın tarihleri:
- **Ay sonu GDX/GLD:** giriş 30.11.2026 kapanışı (TR 01.12 00:00), çıkış 03.12.2026 kapanışı.
- **10Y ihale (TMV/TBT):** 10.11.2026 ihalesinin giriş günü (05.11) geçti; açık pozisyon 09.11 kapanışında kapanır. Sonraki ihale 08.12.2026, giriş 03.12 kapanışı.
- **EIA doğalgaz (KOLD):** raporlar 13.11, 19.11 ve 25.11. Girişler bir gün önce kapanışta.

`kod/sinyal.py` bunları her akşam hesaplar.

## 4. Popüler ama çalışmayanlar

Ayrıntı: `notlar/aile_*.md` ve `notlar/denetim_*.md`.

**Doğalgaz (UNG, BOIL, KOLD):**
- Hiçbir long kural maliyeti aşmıyor.
- BOIL'ün koşulsuz bozulması günde −36 bp, UNG'ninki −10 bp.
- EIA günü (Perşembe 10:30 ET = kış TR 18:30) UNG brüt −28 bp; 2018-2026'da her yıl negatif.
- Kontango (UNG/UNL) ve roll pencereleri kırılgan çıktı.
- **Tek sağlam kural bir kaçınma kuralı:** UNG/BOIL long pozisyonunu EIA raporuna taşıma. Elinde BOIL varsa raporun olduğu günden önce çık.

**Petrol (USO, UCO, XLE, XOP):**
- EIA petrol raporu günü, OVX, Brent-WTI farkı ve enerji hissesi-petrol yetişmesi testlerinden hiçbiri işe yaramadı.
- **OVX yalnız boyut bilgisi taşıyor:** OVX ≥ 1,25 × SMA20 olduktan sonraki 3 günde USO'nun mutlak hareketi 2,3 kat. Bu durumda pozisyonu küçült.
- UCO artık tam 2x USO gibi davranmıyor; 2026'da betası 1,13.

**Altın ve gümüş (GLD, SLV):**
- Reel faiz ve dolar sinyalleri, FOMC sonrası (işaret tersine), altın/gümüş oranı, GVZ ve RSI(2) testleri işe yaramadı.
- Altının getirisi gece oluşuyor: kapanış → açılış ortalama +5 bp/gün, t 3,2; gün içi ≈ 0. Ama her gün işlem yapınca maliyet bunu yiyor.
- Altın için ancak zayıf ay sonu etkisi (B3) kaldı.

**VIX ürünleri (VXX, UVXY, UVIX):**
- 1-3 günlük hiçbir long kural pozitif değil. Koşulsuz kayıp günde VXX −9,6 bp, UVXY −18 bp, UVIX −35 bp.
- Kontango taşıma kuralı 2022 sonrasında negatif.
- VIX sıçramasından sonra uzun vol almak kaybettiriyor.
- Kısa vol tarafında yalnız B9 kaldı.

**Kripto (IBIT, ETHA, BITX…):**
- Perşembe etkisi çürütüldü.
- Hafta sonu etkisi, gece primi, momentum ve dönüş testleri maliyet sonrası çalışmadı.
- Kaldıraçlı BTC ürünleri 2×IBIT'e göre günde ~11 bp kaybediyor.

**Sektör rotasyonu:**
- "Aşırı satılan sektörü al" testi ters çıktı: geride kalan sektör ertesi gün de geride kaldı (−14 bp, t −2,2).
- 1-3 günlük sektör momentumu ve sektör çiftleri yok.
- Sektörlerin "33/34'ünde pozitif" görünen IBS sonucu tek bir piyasa etkisi (etkin N ≈ 2,6).

**Takvim etkileri:** FOMC öncesi drift (2015 sonrası yok), CPI/NFP öncesi, OPEX haftası, ay dönümü (endekslerde), tatil öncesi ve Turnaround Tuesday maliyet sonrası ya eşik altında ya da negatif.

**Kırılım ve momentum:** 20 günlük zirve kırılımı neredeyse her ailede **negatif**. 1-3 günde trend takibi değil, ortalamaya dönüş çalışıyor.

**Ters ETF'lerle kısa yön:** SQQQ, SPXU, TSLQ, NVDS gibi ürünlerde bütün varyantlar kalıcı negatif net verdi.

**Ülke ETF'lerinde "NAV'dan sapma düzeltmesi":** SPY'a göre kalıntı vekiliyle test edildi; maliyet sonrası yok. Yalnız B4'ün dar sürümü kaldı.

## 5. İzleme listesi

**Kapsam:** 77 ETF.
- **Kabul (22):** A 2, B 13, C 7.
- **Yedek (55):** A 3 (QLD, TQQQ, SOXX), B 17, C 35.

Tam tablo: **`IZLEME_LISTESI.md`**. ETF başına kart: **`kartlar/<SYM>.md`**.

**TradingView'a içe aktarma:** `izleme_listeleri/TUM_ETF_bolumlu.txt` dosyasında aile bazında bölümler var: ETF'ler, sürücüler/öncüler, gerçek zamanlı izleme. TradingView'da İzleme listesi → "Listeyi içe aktar" ile yüklenir; aile bazında ayrı dosyalar da var.

Çekirdek liste (kabul), kademe sırasıyla:

| Kademe | ETF (TradingView) | Not |
|---|---|---|
| A | `NASDAQ:QQQ`, `NASDAQ:SMH` | Doğrulanmış kurallar (A1, A2). Araçlar: `AMEX:QLD`, `NASDAQ:TQQQ`, `NASDAQ:SOXX` (yedek) |
| B | `AMEX:SPY`, `AMEX:GDXJ`, `AMEX:GDX`, `AMEX:GLD`, `AMEX:EWY`, `AMEX:EWT`, `AMEX:FXI`, `CBOE:SVXY`⚠, `NASDAQ:NVDL`, `NASDAQ:TSLL`, `NASDAQ:AMZU`, `NASDAQ:MSFU`, `NASDAQ:GGLL` | Zayıf kurallar (B1-B5, B9, B10). TMV/TBT ile KOLD⚠ ve USO⚠ yedekte |
| C | `AMEX:XLE`, `AMEX:XOP`, `NASDAQ:TLT`, `NASDAQ:IBIT`, `AMEX:GBTC`, `NASDAQ:ETHA`, `AMEX:ETHE` | Kural yok. Likit, popüler; sürücüleriyle takip |

Doğalgaz (UNG⚠, KOLD⚠), petrol (USO⚠, UCO⚠, SCO⚠, BNO⚠), gümüş (SLV), bakır (COPX), VIX (VXX) ve küçük şirket (IWM) gibi popüler ürünler **yedek** olarak kartlarda. Hepsinin sürücüsü ve gerçek zamanlı izleme kodu orada.

## 6. Lead-lag: ne bulduk, nasıl kullanılır

**Yöntem (`kod/leadlag_sweep.py`, `sonuclar/leadlag_sweep.csv`):**
- Her hedef ETF (n ≥ 500 gün, ≥ 2 mn $/gün) için 45 öncü kullanıldı: ETF'ler; VIX, OVX, GVZ ve VVIX; VIX vade yapısı; BTC/ETH'nin 16:00 ET fiyatı; Hazine faizleri.
- **Gecikmeli test:** r_öncü(t) → r_hedef(t+1…t+3); hedefin kendi gecikmesi kontrol edildi, Newey-West kullanıldı.
- **Yetişme testi:** beta·r_öncü(t) − r_hedef(t) → ileri getiri.
- Kontroller: BH-FDR, IS/OOS işaret tutarlılığı, ekonomik büyüklüğün maliyetle karşılaştırılması.
- Aile ajanları ek kontrol yaptı, denetçiler yeniden hesapladı.

**Bulgular:**

1. **Doğrulanmış, işlenebilir gecikmeli öncü yok.** Dokuz ailenin dokuzunda bu sonuç denetçi tarafından da teyit edildi.
2. **Bulunan gecikmeli ilişkiler gerçek ama işlenemez.** Örnek: "ABD hisseleri dün yükseldiyse döviz ETF'i (FXE, FXF, FXY) bugün yükselir" (t ≈ 4-5). Büyüklük 1 sd başına 5-9 bp, maliyet ise 20-47 bp.
3. **Yalnız "alma" filtresi olarak kullanılabilecekler:** EEM güçlü yükseldiği günün ertesinde KWEB zayıf; QQQ/SPY'dan sonra IGV için de benzer bir ilişki var ama zayıf.
4. **İlk taramadaki "yetişme" sinyallerinin çoğu artefakt.** Nasdaq API'si NYSE Arca ve Cboe listeli 267 ETF'in dağıtımlarını vermiyordu. Bu, ex-date'lerde sahte düşüşler yarattı. Yahoo dağıtımlarıyla düzeltildi (`kod/temettu_yahoo.py`) ve FDR'yi geçen 1 günlük yetişme bayrakları 288'den 2'ye düştü.
5. **Pratik kullanım:**
   - (a) **Aynı gün sürücüler** ETF'nin neye göre hareket ettiğini gösterir. Örnek: QQQ ↔ `CME_MINI:NQ1!`, `AMEX:XLK`; GLD ↔ `COMEX:GC1!`; UNG ↔ `NYMEX:NG1!`.
   - (b) **Gerçek zamanlı izleme:** ETF kapalıyken işleyen enstrümanlar ertesi açılış boşluğunu önceden gösterir. Örnek: `COINBASE:BTCUSD` IBIT'in açılış boşluğunun **%96'sını** açıklıyor; QQQ varyansının ~%42'si gece oluşuyor.
   - Bu yüzden O1 (açılışta) giriş düşünüyorsan ilgili vadeliye bakarak boşluğu önceden gör. A1/A2 gibi kapanış kurallarında ise kapanış öncesi son dakikalardaki vadeli/ETF fiyatı yeterli.

Aile bazında başlıca gerçek zamanlı kodlar (tamamı doğrulanmış):

| Aile | Gerçek zamanlı izleme (TradingView) |
|---|---|
| ABD endeks | `CME_MINI:ES1!`, `CME_MINI:NQ1!`, `CME_MINI:RTY1!`, `CBOE:VX1!`, `TVC:US10Y` |
| Yarı iletken / sektör | `CME_MINI:NQ1!`, `NASDAQ:NVDA` (pre-market), `KRX:KOSPI`, `CBOT:ZN1!` |
| Enerji | `NYMEX:CL1!`, `ICEEUR:BRN1!`, `NYMEX:NG1!`, `NYMEX:NG2!`, `ICEENDEX:TFM1!`, `CBOE:OVX` |
| Metal | `COMEX:GC1!`, `COMEX:SI1!`, `COMEX:HG1!`, `NYMEX:PL1!`, `FX_IDC:XAUUSD`, `CBOE:GVZ` |
| Tahvil / döviz | `CBOT:ZN1!`, `CBOT:ZB1!`, `CBOT:UB1!`, `TVC:US10Y`, `TVC:US02Y`, `TVC:DXY`, `FX_IDC:USDJPY` |
| VIX | `CBOE:VIX`, `CBOE:VIX3M`, `CBOE:VIX9D`, `CBOE:VX1!`, `CBOE:VVIX`, `CME_MINI:ES1!` |
| Kripto | `COINBASE:BTCUSD`, `COINBASE:ETHUSD`, `CME:BTC1!`, `CME_MINI:NQ1!` |
| Ülke ETF'leri | `OSE:NK2251!`, `HKEX:HSI1!`, `KRX:KOSPI`, `TWSE:IX0001`, `EUREX:FDAX1!`, `FX_IDC:USDJPY` |

## 7. Akşam rutini (TR saati, kış saatine göre; yazın 1 saat erken)

1. **~17:30, ABD açılışı (isteğe bağlı):** `CME_MINI:NQ1!`, `CME_MINI:ES1!` ve `COINBASE:BTCUSD`'ye bakarak gece boşluğunu gör. Açık pozisyonun varsa panik yapma; kurallar stopsuz test edildi.
2. **~23:40-23:55, kapanışa 10-20 dk kala:**
   - `python3 -I kod/sinyal.py --canli` çalıştır, ya da TradingView'da `ibs_dip.pine` göstergesine bak.
   - QQQ IBS < 0,10 + düşüş varsa A1'i C0 olarak hemen, C1 olarak ertesi akşam uygula.
   - SMH IBS < 0,20 ise A2'yi uygula. Çıkış günü olan pozisyonları bu saatte sat.
3. **00:00 sonrası, kapanış sonrası:** `python3 -I kod/sinyal.py` çalıştır. Kesin kapanış verisiyle sinyalleri ve açık pozisyon çıkışlarını teyit et. A2 için after-hours (00:00-04:00) limit emir seçeneği burada.
4. **Haftalık kontrol:** Takvimli B kuralları (ay sonu, 10Y ihale, EIA) ve önemli veriler. CPI ve NFP TR 16:30'da; FOMC kararı kışın TR 22:00'de.

Örnek çıktı (06.11.2026 kapanışı): `sonuclar/sinyal_ornek_2026-11-06.txt`.
- QQQ'da 02.11 ve 05.11'de sinyal var. C1 pozisyonu 06.11 kapanışında kapandı; C0 sürümünde 05.11 girişi 10.11'de kapanır.
- SMH'nin 05.11 sinyali 06.11'de kapandı.
- Bugün yeni A sinyali yok.

## 8. Risk ve pozisyon kuralları

- **Boyut:** A kuralı başına sermayenin en fazla %20-25'i (1x araçla). 2x araçta bunun yarısı, 3x araçta üçte biri.
- **Kuyruk riski:** QQQ 3 günlük işlemde en kötü −%8,3; TQQQ −%31. Stop test edilmedi. Stop koyacaksan geniş tut, ama kenarı değiştirebileceğini bil.
- **Aynı anda en çok bir teknoloji pozisyonu:** A1, A2, B1 ve B10 aynı risk faktörü; B10'da aynı gün en çok 7 hisse sinyali görüldü.
- **PTP ürünleri** (⚠): Midas'ta "PTP" ibaresi ve %10 brüt kesinti uygulanmadığını teyit etmeden kısa vadeli işlem yapma. %10 kesinti işlem başına ~1.000 bp demek; hiçbir kural bunu karşılamaz.
- **Ürün bulunurluğu:** Kaldıraçlı, ters, VIX ve tek hisse kaldıraçlı ETF'leri Midas uygulamasında arayıp gör. Yoksa 1x araçla devam et; kurallar 1x'te de geçerli.
- **Olay günleri:** CPI, NFP ve FOMC günleri büyük boşluk yaratabilir. Kurallar bu günleri dışlamıyor; kendi tercihin.
- **Kur ve vergi:** USD bakiye tutulabiliyor; TL çevriminde makas yayımlanmıyor. Kâr/zarar TL bazında vergilenir; zarar ertesi yıla devretmez.

## 9. Yöntem, veri ve sınırlamalar

**Veri:**
- Nasdaq API: 10 yıllık günlük OHLCV, bölünme düzeltmeli. 318 ETF'den 313'ü indi.
- Yahoo: dağıtım ve bölünme olayları. Yahoo'nun bölünme bazı Nasdaq fiyatlarıyla birebir eşleşiyor (`sonuclar/yahoo_nasdaq_fiyat_orani.csv`).
- Cboe: VIX, VIX9D, VIX3M, VIX6M, VVIX, OVX, GVZ (1990+).
- Coinbase: BTC/ETH günlük ve saatlik veri.
- ABD Hazinesi: nominal ve reel getiri eğrileri. FRED proxy üzerinden erişilemedi.
- Dayanak hisseler: Nasdaq.
- Olay takvimleri (`data/events/`): FOMC, CPI, NFP, EIA doğalgaz/petrol, OPEX, NYSE tatilleri, NG/CL/VIX vadeleri, UNG/USO/BOIL-KOLD roll pencereleri, 10Y/30Y ihaleleri. Kaynaklı; kuraldan hesaplananlar işaretli.

**Veri düzeltmeleri:**
- Nasdaq'ın NYSE Arca ve Cboe ETF'lerinde dağıtım vermemesi Yahoo ile giderildi.
- Bölünmeye göre ölçeklenmemiş Nasdaq temettüleri (NVDL, SOXX…) Yahoo ile değiştirildi.
- Hatalı barlar çıkarıldı: DFEN 2024-06-03, IAU 2021-03-08.
- Tröst dönemleri çıkarıldı: GBTC 2024-01 öncesi, ETHE 2024-07 öncesi. USHY 2019-04 öncesi çıkarıldı.
- Gerçek aşırı hareketler korundu: Mart 2020, 05.08.2024, 09.04.2025, 30.01.2026 gümüş, 02.02.2026 doğalgaz (`sonuclar/veri_kalitesi.csv`).

**Zamanlama sözleşmesi** (`kod/lib.py`):
- Sinyal yalnız t kapanışına kadar bilinen veriyle hesaplandı.
- C0 = t kapanışında giriş. Kapanış fiyatıyla hesaplanan sinyalde hafif iyimserdir; bu yüzden O1 ve C1 de raporlandı.
- VIX'in kapanışı 16:15 ET; BTC günlük mumu 00:00 UTC'de kapanıyor. Bunun yerine 16:00 ET saatlik fiyat kullanıldı.

**Maliyet:** 2 × 1,5 $ komisyon + likidite kademesine göre makas. Makas en az 1 sentlik fiyat adımı kadar alındı; bu yüzden 10 $'lık ETF'de en az ~10 bp.

**Çoklu test:**
- Genel kütüphanede 92.664 test var. **Tek yönlü katı BH-FDR'de hiçbir test geçmiyor.**
- A1 ve A2'nin dayanağı tek bir testin t'si değil. Dayanaklar şunlar: önceden belirlenmiş literatür hipotezi (IBS etkisi), aile genelinde tutarlılık, parametre platosu, permütasyon testleri ve üç giriş modunda sağlamlık. Seçim düzeltmeli p ≈ 0,03-0,06 olduğu için güven **orta**, yüksek değil.

**Sınırlamalar:**
- Veri 10 yılla sınırlı (2016-2026); uzun bir ayı piyasası yok. Gün içi veri yok; kapanış öncesi giriş maliyeti tahmini.
- Kaldıraçlı ETF'lerin kaldıracı dönem içinde değişti: NUGT/JNUG 2020'de 3x'ten 2x'e, Direxion tek hisse ETF'leri 2024'e kadar 1,5x, SVXY 2018'de −1x'ten −0,5x'e indi.
- Midas'ta ürün bulunurluğu ve PTP uygulaması resmî olarak doğrulanamadı.
- Literatürdeki IBS/RSI(2) etkilerinin yayın sonrasında zayıfladığı biliniyor. Gerçek performans backtestin altında olabilir; denetçilerin "gerçekçi beklenti" aralıkları bunu yansıtıyor.

## 10. Dosyalar

| Yol | İçerik |
|---|---|
| `RAPOR.md` | Bu rapor |
| `IZLEME_LISTESI.md` | 77 ETF'lik izleme listesi tablosu (kademe, TV kodu, maliyet, kural, sürücü, gerçek zamanlı) |
| `kartlar/<SYM>.md` | ETF başına kart: kurallar, rakamlar (ajan + denetçi + son kontrol), sürücüler, öncüler, gerçek zamanlı izleme, takvim riskleri |
| `izleme_listeleri/*.txt` | TradingView içe aktarma dosyaları (aile bazında ve tümü) |
| `kod/sinyal.py` | Akşam kontrol betiği (`--canli` ile kapanış öncesi) |
| `kod/tradingview/ibs_dip.pine`, `rsi2_dip.pine` | TradingView göstergeleri (Pine v5, derlenmedi) |
| `notlar/aile_<aile>.md`, `notlar/denetim_<aile>.md` | Aile ajanlarının ve denetçilerin ayrıntılı notları |
| `notlar/midas_kosullari.md`, `literatur.md`, `hipotezler.csv`, `takvim_notlari.md` | Midas koşulları, literatür, önceden kayıtlı hipotezler, takvim notları |
| `sonuclar/son_kontrol*.csv` | Ana ajanın düzeltilmiş veriyle son kontrolü (3 mod × 3 pozisyon boyutu, yıllık, korelasyon) |
| `sonuclar/genel_tum.csv.gz`, `leadlag_sweep.csv`, `tarama.csv` | Genel kütüphane, lead-lag taraması, işlenebilirlik |
| `sonuclar/izleme_son.csv`, `kart_indeksi.csv` | Uzlaştırılmış izleme kararları (ajan → denetçi → nihai) |
| `sonuclar/tv_etf.csv`, `tv_dogrulama.csv` | TradingView kod doğrulaması (sayfa okunarak) |
| `kod/` | Veri indirme (`dl.py`, `temettu_yahoo.py`), ortak kütüphane (`lib.py`), genel kütüphane (`strategies.py`, `run_generic.py`), tarama, lead-lag, kart üretici, aile ve denetim betikleri |

Ham veri (`data/`, olay takvimleri hariç) ve indirilen sayfalar (`ham_sayfalar/`) repoya eklenmedi; `kod/dl.py all` ve `kod/temettu_yahoo.py` ile yeniden indirilir.
