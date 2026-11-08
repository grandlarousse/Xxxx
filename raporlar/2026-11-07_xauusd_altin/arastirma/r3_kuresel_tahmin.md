# r3 — Küresel altın fiyatını ne belirliyor, nasıl tahmin edilir? (7 Kasım 2026)

Kapsam: Dünya ons altın fiyatının (XAU/USD) yapısal sürücüleri, akademik literatürde örneklem dışı tahmin kanıtı, kurumların (Goldman Sachs, JPMorgan, UBS, Citi, WGC) modelleri ve isabetleri, Kasım 2026 itibarıyla güncel durum ve katalizörler, 1–5 gün / 1–3 ay / 6–12 ay için pratik çerçeve. Borsa İstanbul VİOP F_XAUUSD sözleşmesi bu fiyatı neredeyse birebir izler (6 Kasım 2026 F_XAUUSD1226 uzlaşma 4.078,8 USD; aynı gün spot ~4.071–4.077 USD, COMEX Aralık ~4.081 USD), bu yüzden burada anlatılan her şey doğrudan F_XAUUSD için de geçerlidir.

Yöntem notu: İddialar birincil kaynaklardan (Fed, BLS, WGC, Goldman Sachs PDF'i, akademik makale PDF/özetleri, Borsa İstanbul duyurusu) ve Reuters/Kitco haberlerinden teyit edildi. Ayrıca FRED (DFII10, DGS10, T10YIE, T5YIFR, DTWEXBGS, DCOILBRENTEU, VIXCLS, GVZCLS, CPIAUCNS, DFF), Yahoo Finance GC=F (COMEX sürekli vadeli; vade geçişlerinde küçük sıçramalar içerir) ve Caldara–Iacoviello günlük GPR verisiyle kendi hesaplarımı yaptım ("Kendi hesabım" diye işaretli). Hesap betikleri: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/scripts_r3/an1.py` … `an6.py`.

---

## 0. Kısa özet

1. **Seviye:** 6 Kasım 2026'da spot altın ~4.070–4.077 USD/ons, haftalık +%5 (Reuters). 2026 zirvesi 29 Ocak: LBMA PM 5.405,00 USD, spot gün içi 5.595,47 USD (WGC). 30 Ekim'de spot yıllık dip 3.869,85 USD; LBMA PM 3.913,25 USD. 2025 sonu LBMA ~4.310 USD idi; yani yılbaşından beri yaklaşık **-%5**, zirveden yaklaşık **-%25**.
2. **2026'nın hikâyesi "reel faiz geri döndü":** İran savaşı (Mart 2026 başı) petrolü 71 → 118 USD'ye (Brent, 27 Şubat → 18 Mart) taşıdı, enflasyon beklentisi Fed'i faiz artırımına itti (16 Eylül: +25 bp, 3,75–4,00%; 28 Ekim: sabit, 2 üye artırım istedi). Altın jeopolitik riske rağmen düştü: güvenli liman, enflasyonist şokta çalışmadı.
3. **Kendi hesabım:** Altının haftalık getirisinin 10 yıllık TIPS reel faiz değişimine duyarlılığı 2024–2025'te sıfırdı (beta +1,1%/puan, R² 0,00), 2026'da yeniden sertleşti (beta -16%/puan, korelasyon -0,37). Altın–Brent haftalık korelasyonu 2006–2021'de +0,19 iken 2026'da **-0,31**'e döndü.
4. **Seviye modeli çöktü:** 2006–2021 verisiyle kurulan "log(altın) = 7,283 - 0,288·reel faiz" modeli, bugünkü 2,60% reel faizle ~690 USD öngörüyor; fiyat bunun ~5,7 katı. Reel faiz artık *seviyeyi* değil, olsa olsa *değişimi* açıklıyor.
5. **Merkez bankaları yapısal taban:** WGC verisiyle 2022–2024 her yıl >1.000 t, 2025'te 863 t, 2026'nın ilk 9 ayında 675 t (Ç3: 321 t, yıllık +%42). Goldman'ın "nowcast"ı ayda ~85 t; tahmini 2026–27 için ayda 60 t.
6. **ETF'ler geri geldi:** 2026 Ç3'te +211 t, Ekim'de +19 t (+2,7 milyar USD) ile toplam rekor 4.275 t. Ama Kuzey Amerika fonları Ekim'de -512 milyon USD verdi. COMEX net uzunlar Ekim'de 94 t düşüp 560 t'ye indi.
7. **Akademik sonuç net:** Günlük–haftalık ufukta altın getirisini örneklem dışında rastgele yürüyüşten anlamlı biçimde daha iyi tahmin eden makro değişken bulunamadı. Pierdzioch–Risse–Rohloff çalışmaları "biraz öngörü gücü var ama işlem maliyeti sonrası al-tut'u geçmiyor" diyor. Kendi testlerimde 1, 3 ve 5 günlük OOS R² değerleri -%1,4 ile +%0,65 arasında.
8. **Kurum tahminleri fiyatı kovaladı:** Goldman'ın 2026 sonu hedefi 4.900 → 5.400 (22 Ocak) → 4.900 (19 Haziran) → 4.650 (Eylül) → **4.150** (5 Kasım) oldu; 2027 sonu hedefi 5.400 → **4.800**. JPMorgan 9 Haziran'da yıl sonu için 6.000 derken 3 Temmuz'da Ç4 için 4.500'e indi.
9. **Konsensüs (Reuters anketi, 27 Ekim 2026, 30 analist):** 2026 ortalaması 4.495 USD, 2027 ortalaması 4.650 USD. UBS 2027 Eylül için 5.400, Goldman 2027 sonu için 4.800 öngörüyor.
10. **Yaklaşan katalizörler:** ABD Ekim TÜFE (10 Kasım, 16:30 TSİ), Kasım istihdamı (4 Aralık, 16:30 TSİ), FOMC (8–9 Aralık; karar 9 Aralık 22:00 TSİ, yani VİOP gündüz uzlaşmasından sonra), Kasım TÜFE (10 Aralık). 5–6 Kasım'da piyasa Aralık artırımına %64–81 olasılık veriyordu.
11. **Volatilite rejimi:** 2026'da gerçekleşen yıllık volatilite %29,4; 2015–2024 ortalaması %14,8 (kendi hesabım). GVZ 25,8 (5 Kasım), uzun dönem ortalaması 15,9. 2026'da tipik 1 günlük hareketin standart sapması %1,9, 5 günlük %3,9. Pozisyon boyutu buna göre ayarlanmalı.
12. **Pratik ders:** 1–5 günde "tahmin" değil "olay ve rejim yönetimi" yapılır: veri ve Fed takvimi, sürprizin yönü, aynı gündeki reel faiz/dolar/petrol hareketi, pozisyon sıkışması ve marj artışları. 1–3 ayda Fed yolu, reel faiz, dolar ve ETF akışları önemli. 6–12 ayda merkez bankası alım hızı ve Fed döngüsünün dönüşü belirleyici.

---

## 1. Güncel durum (7 Kasım 2026)

### 1.1 Fiyat yolu

| Tarih | Ölçü | Değer (USD/ons) | Kaynak |
|---|---|---|---|
| 2025 son işlem günü | LBMA (sabah fixingi) | ~4.310 (2025: +%65,0) | BullionVault |
| 22 Ocak 2026 | Spot zirve (o gün) | 4.887,82 | Reuters/Daily Star |
| 29 Ocak 2026 | LBMA PM zirvesi | 5.405,00 | WGC Mid-Year Outlook |
| 29 Ocak 2026 | Spot gün içi zirve | 5.595,47 | WGC Mid-Year Outlook |
| 30 Ocak 2026 | Tarihin en büyük tek günlük düşüşü (vadeli >%11) | — | Reuters/Bloomberg özetleri |
| 24–25 Haziran 2026 | Spot gün içi dip 3.959,33 / LBMA PM dip 4.001,80 | — | WGC |
| 2026 Ç3 ortalaması | — | 4.262 | WGC GDT Ç3 |
| 30 Ekim 2026 | LBMA PM 3.913,25; spot yıllık dip 3.869,85 | — | Bernama; Reuters/Kitco |
| 5 Kasım 2026 | Spot 4.117,69 (13:16 GMT), gün içi yüksek 4.146,63 | — | Reuters/Kitco |
| 6 Kasım 2026 | Spot ~4.070–4.077, haftalık +%5 | — | Reuters/Kitco |
| 6 Kasım 2026 | F_XAUUSD1226 uzlaşma 4.078,8 | — | VİOP bülteni (görev bağlamı) |

Ekim ayında COMEX sürekli vadeli kapanışı 4.186,7'den (30 Eylül) 3.898,9'a (30 Ekim) indi: **-%6,9** (kendi hesabım, Yahoo GC=F).

### 1.2 Son 3 ayın anahtar olayları

- **16 Eylül 2026, Fed artırımı:** FOMC politika faizini 25 bp artırarak %3,75–4,00 aralığına çekti; oy 12–0, karşı oy yok; açıklamada "Inflation remains elevated" ifadesi var ([Fed](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm)). Bu, 2023'ten beri ilk artırımdı. 30 Eylül'de 10 yıllık getiri %5,29'a, 10 yıllık TIPS %2,93'e çıktı (FRED).
- **Eylül sonu, Goldman revizyonu:** 2026 sonu "adil değer" 4.900'den 4.650'ye indirildi, 2027 sonu 5.400 korundu ([investingLive, 23 Eyl 2026](https://investinglive.com/commodities/icymi-goldman-trims-end-2026-gold-forecast-to-4-650-but-holds-5-400-target-for-2027/)).
- **Ekim:** Altın ~%7 düştü. ABD teknoloji hisselerindeki satış (yapay zekâ yatırım harcaması kaygısı) Kuzey Amerika ETF'lerinde likidite amaçlı satışı tetikledi; çok yıllık zirvedeki Hazine getirileri de para çekti ([WGC ETF Ekim 2026](https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/11)).
- **28 Ekim 2026, FOMC sabit:** %3,75–4,00 korundu; oy 10–2, Lisa Cook ve Beth Hammack 25 bp artırım istedi ([Fed](https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm)).
- **3 Kasım 2026, WGC Ç3 talep raporu:** Merkez bankaları 321 t, ETF'ler +211 t, mücevher 313 t (-%17, en zayıf Ç3) ([WGC](https://gold.org/news-and-events/press-releases/central-bank-buying-and-etf-inflows-support-gold-demand-q3)).
- **3–5 Kasım, ABD ara seçimi:** Demokratlar Kongre'de büyük kazanç elde etti. Piyasa bunu "kilitlenme, mali genişleme sınırlanır" diye okudu. Dolar ve getiriler düştü, Brent bir günde ~%9 geriledi, altın 4 Kasım'da ~%3 artışla 4.046'ya, 5 Kasım'da 4.146'ya çıktı ([Reuters/Kitco](https://www.kitco.com/news/off-the-wire/2026-11-05/gold-hits-2-week-high-dollar-yields-oil-fall-after-us-midterms); [investingLive](https://investinglive.com/commodities/gold-surges-past-4-000-as-us-midterm-fallout-shakes-up-markets/)).
- **5 Kasım, Goldman revizyonu:** 2026 sonu hedefi 4.650'den 4.150'ye, 2027 sonu 5.400'den 4.800'e indirildi ([Investing.com/Yahoo, 6 Kas 2026](https://finance.yahoo.com/markets/commodities/articles/goldman-lowers-end-gold-price-081423381.html)).
- **6 Kasım, istihdam verisi:** Tarım dışı istihdam +165 bin (beklenti ~65 bin), işsizlik %4,1, saatlik ücret aylık +%0,4. 2 yıllık getiri ~6 bp artarak %4,53'e çıktı, altın ~%0,9 düştü (~4.051) ([Kitco](https://www.kitco.com/news/article/2026-11-06/gold-falls-us-payrolls-surge-165000-strengthening-december-fed-hike-case)).

### 1.3 Makro gösterge panosu (FRED, son değerler)

| Gösterge | Son değer | Tarih |
|---|---|---|
| 10y TIPS reel getiri (DFII10) | %2,60 | 5 Kas 2026 |
| 10y nominal getiri (DGS10) | %4,84 | 5 Kas 2026 |
| 10y başabaş enflasyon (T10YIE) | %2,24 | 5 Kas 2026 |
| 5y5y enflasyon beklentisi (T5YIFR) | %2,17 | 6 Kas 2026 |
| Efektif fed funds (DFF) | %3,88 | 5 Kas 2026 |
| Geniş dolar endeksi (DTWEXBGS) | 121,67 | 30 Eki 2026 |
| Brent (DCOILBRENTEU) | 107,03 USD | 3 Kas 2026 |
| VIX | 28,18 | 5 Kas 2026 |
| GVZ (altın örtük volatilite) | 25,83 | 5 Kas 2026 |
| ABD TÜFE (NSA) yıllık | %3,7 | Eylül 2026 |

### 1.4 Kurum tahminleri ve konsensüs (tarihli)

| Kurum | Tarih | Tahmin | Not / kaynak |
|---|---|---|---|
| Goldman Sachs | 5 Kas 2026 | 2026 sonu 4.150 (önce 4.650); 2027 sonu 4.800 (önce 5.400). Aşağı senaryo (Mart 2027'de ek artırım veya gecikmeli indirim): 2027 sonu 4.660 | Temel senaryo Aralık artırımını varsayıyor; MB alımı 2026–27 için ayda 60 t; "2022'ye benziyor" ([Yahoo/Investing](https://finance.yahoo.com/markets/commodities/articles/goldman-lowers-end-gold-price-081423381.html)) |
| UBS | ~9 Eki 2026 notu | Ara 2026: 4.600; Mar 2027: 5.000; Haz 2027: 5.200; Eyl 2027: 5.400; aşağı risk 4.000 | 2026'da bir artırım daha, 2027'de iki indirim varsayımı; MB alımı yılda 750–1.000 t ([Canadian Mining Report, 12 Eki 2026](https://www.canadianminingreport.com/blog/ubs-projects-gold-at-5-400-by-september-2027-could-4-000-come-first); ikincil kaynak) |
| JPMorgan | 3 Tem 2026 | Ç3 2026: 4.300; Ç4 2026: 4.500; riskler aşağı yönlü; 2027'de toparlanma olabilir (rakam yok) | 9 Haziran'da yıl sonu için 6.000 diyordu ([Reuters/Kitco](https://www.kitco.com/news/off-the-wire/2026-07-06/jpmorgan-sees-4500-gold-price-fourth-quarter-says-risks-downside)). Daha yeni JPM hedefi **bulunamadı**. |
| Citi | 9 Haz 2026 | 0–3 ay 4.000 (önce 4.300); 6–12 ay 4.500 | [Kitco](https://www.kitco.com/news/article/2026-06-09/citi-cuts-near-term-gold-price-target-4300-4000-warns-limited-upside). 24 Ağustos'ta 0–3 ayı 4.800'e çıkardığı ve 6–12 ayı 5.000'de tuttuğu yalnızca ikincil kaynakta geçiyor ([Golden Ark](https://goldenarkreserve.com/insights/gold-price-forecast-september-2026/)); Ekim–Kasım Citi notu **bulunamadı**. |
| WGC | 1 Tem 2026 | 2026 2. yarısı: ~4.100 USD ±%5 (makro konsensüs senaryosu); 3.860 kritik teknik seviye | [WGC Mid-Year Outlook 2026](https://www.gold.org/goldhub/research/gold-mid-year-outlook-2026) |
| Reuters anketi (30 analist) | 27 Eki 2026 | 2026 ortalaması 4.495 (önce 4.509); 2027 ortalaması 4.650 (önce 4.610) | [Reuters/WHTC](http://whtc.com/2026/10/27/strong-dollar-high-yields-drag-on-gold-outlook-but-central-bank-demand-lends-support/) |

### 1.5 Yaklaşan katalizörler (TSİ = UTC+3; ABD 1 Kasım'da kış saatine geçti)

| Tarih | Olay | Saat (TSİ) | VİOP günlük uzlaşmaya göre |
|---|---|---|---|
| 10 Kas 2026 | ABD Ekim TÜFE ([BLS](https://www.bls.gov/schedule/news_release/cpi.htm)) | 16:30 | Uzlaşmadan önce, aynı güne yansır |
| 4 Ara 2026 | ABD Kasım istihdamı ([BLS](https://www.bls.gov/schedule/news_release/empsit.htm)) | 16:30 | Aynı gün |
| 8–9 Ara 2026 | FOMC + SEP/dot plot ([Fed takvimi](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)) | Karar 9 Ara 22:00 | Gündüz uzlaşmasından sonra, akşam seansında (19:00–23:00); **10 Aralık uzlaşmasına** yansır |
| 10 Ara 2026 | ABD Kasım TÜFE | 16:30 | Aynı gün (FOMC'den sonraki gün) |
| 2027 FOMC | 26–27 Oca, 16–17 Mar, 27–28 Nis, 8–9 Haz, 27–28 Tem, 14–15 Eyl, 26–27 Eki, 7–8 Ara (geçici) | | Fed takvimi |

Diğer etkenler: İran savaşı ve petrol (Brent ~100 USD civarı), ara seçim sonrası mali politika ("kilitlenme"), merkez bankası aylık verileri (WGC, ~1 ay gecikmeli), Çin'in PBoC rezerv açıklamaları (her ayın 7'si civarı), Hindistan'da düğün sezonu talebi.

---

## 2. Yapısal sürücüler: mekanizma, kanıt ve 2026'da ne oldu

### 2.1 ABD reel faizleri (10y TIPS) ve 2022 sonrası kırılma

**Teori:** Altın faiz getirmez; reel faiz, onu tutmanın fırsat maliyetidir. Barsky & Summers (1988, *JPE* 96(3): 528–550), altın standardı döneminde altının reel fiyatıyla reel faiz arasındaki negatif dengeyi Gibson paradoksunun açıklaması olarak modelledi ([EconPapers](https://econpapers.repec.org/RePEc:ucp:jpolec:v:96:y:1988:i:3:p:528-50); [NBER WP 1680](https://www.nber.org/system/files/working_papers/w1680/w1680.pdf)). Bu bir *denge* ilişkisi; tahmin modeli değil.

**Kendi hesabım: haftalık altın getirisi (GC=F) ~ Δ10y TIPS ve Δ geniş dolar**

| Dönem | n (hafta) | korr(altın, ΔTIPS) | korr(altın, Δ$) | Beta (TIPS, %/1 puan) | R² (yalnız TIPS) | R² (TIPS + $) |
|---|---|---|---|---|---|---|
| 2006–2012 | 364 | -0,15 | -0,45 | -3,6 | 0,02 | 0,20 |
| 2013–2021 | 470 | **-0,50** | -0,49 | **-11,0** | **0,25** | 0,36 |
| 2022–2023 | 104 | -0,43 | -0,48 | -5,6 | 0,18 | 0,30 |
| 2024–2025 | 104 | **+0,05** | -0,37 | **+1,1** | **0,00** | 0,14 |
| 2026 (5 Kas'a kadar) | 44 | -0,37 | -0,38 | **-16,1** | 0,14 | 0,19 |

Yorum:
- Reel faiz–altın ilişkisi en güçlü 2013–2021'de. 2024–2025'te tamamen kayboldu: merkez bankası alımları ve "değer kaybı" (debasement) işlemi baskın geldi.
- 2026'da **geri döndü**: Fed artırım döngüsü ve İran savaşının petrol → enflasyon → faiz zinciri. Goldman de 5 Kasım notunda tabloyu "giderek 2022'ye benziyor" diye tanımlıyor: güçlü merkez bankası alımı var, ama yüksek faiz yatırımcı pozisyonlarını eziyor.
- Dolar, alt dönemlerin hepsinde -0,37 ile -0,49 arasında, reel faizden daha istikrarlı bir eşzamanlı açıklayıcı.
- Kırılmanın boyutu: 2006–2021 aylık verisiyle tahmin ettiğim seviye modeli log(altın) = 7,283 − 0,288·TIPS (R² 0,85; iki trendli seri olduğu için sahte regresyon riski yüksek), Ekim 2026 sonu için **~689 USD** veriyor; gerçekleşen fiyat 3.899 USD, açık **+%466**. Açık 2021 sonunda -%7, 2022 sonunda +%98, 2024 sonunda +%246 idi.
- WGC'nin GRAM modeli de 2026 ilk yarısında altın oynaklığının yalnızca **%3**'ünü "faiz" bileşenine bağladı. Momentum %24, risk/belirsizlik %17, kur %14, ekonomik büyüme %12; modelin açıklayamadığı kısım (merkez bankası alımları dahil) %30 ([WGC Mid-Year Outlook](https://www.gold.org/goldhub/research/gold-mid-year-outlook-2026)).

### 2.2 Dolar

Altının dolar karşısındaki eşzamanlı haftalık korelasyonu her dönemde -0,4 civarında (kendi hesabım). Aye, Gupta, Hammoudeh & Kim (2015, *IRFA* 41: 257–266) aylık veride (1992:02–2013:11; örneklem dışı 1999:10–2013:11; ufuk 1, 3, 6, 9, 12 ay) dinamik model seçiminde **döviz kuru faktörünü** en güçlü öngörücü buldu ([UP deposu](https://repository.up.ac.za/handle/2263/45456)). 2026'da dolar, İran savaşında güvenli liman işlevi gördü ve altını baskıladı ([Caixin, 12 Mar 2026](https://www.caixinglobal.com/2026-03-12/analysis-iran-war-cements-dollars-safe-haven-status-as-gold-loses-luster-102422146.html)). Ara seçim sonrası dolarda yaşanan düşüş ise altını 2 haftanın zirvesine taşıdı.

### 2.3 Enflasyon ve enflasyon beklentisi

Erb & Harvey, "The Golden Dilemma" (*FAJ* 2013, 69(4): 10–42), 1975–2012 verisinde şunları buldu: altın/TÜFE oranı ortalama ~3,2 (en düşük 1,46, Mart 2001; en yüksek 8,73, Ocak 1980; Mart 2012: 7,3). Reel fiyat yaklaşık 10 yıllık ufukta ortalamaya dönüyor. Geleceğin enflasyonunu mükemmel bilmek bile altın getirisini tahmin etmeye yetmiyor. Yani altın kısa vadede zayıf bir enflasyon koruması ([Duke PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P113_The_golden_dilemma.pdf)). 2012'deki yüksek reel fiyat "10 yıl boyunca yıllık yaklaşık -%10 reel getiri" ima ediyordu, ama yazarlar bunu "bilinen bir bilinmeyen" diye niteledi.

- Yayın sonrası performans: Altın Mart 2012'deki ~1.665 USD'den Aralık 2015'te ~1.050 USD'ye düştü (kısa vadede işe yaradı), sonra çok aştı. **Bugünkü oran = 4.078,8 / 336,94 (Eylül 2026 TÜFE) ≈ 12,1** (kendi hesabım; Ocak 2026 LBMA zirvesinde ~16,6). Bu, 1980 zirvesinin bile üstünde. Erb & Harvey 2024'te konuyu yeniden ele aldı (SSRN 4807895, 7 Mayıs 2024). Değerleme 10 yıllık ufukta bir uyarı işareti, 1–5 günlük işlem için bilgi taşımaz.
- 2026'da ironik bir tablo oluştu: enflasyon yükseldi (TÜFE %3,7), ama Fed artırım yaptığı için altın düştü. Altın **beklenmeyen enflasyonu değil, reel faiz baskısını** fiyatladı.

### 2.4 Merkez bankası alımları (WGC verisi)

| Yıl / dönem | Net alım (ton) | Kaynak |
|---|---|---|
| 2022 | İlk açıklama 1.136; revize ~1.082 (1950'den beri rekor) | [Kitco/WGC 2023](https://www.kitco.com/news/off-the-wire/2023-01-31/corrected-official-central-banks-bought-most-gold-record-last-year-wgc); [BullionStar](https://www.bullionstar.com/blogs/ronan-manly/central-bank-gold-buying-latest-trends-and-developments/) |
| 2023 | >1.000 (WGC: "üç yıl üst üste 1.000 t üzeri"); kesin rakam birincil kaynakta doğrulanamadı | WGC FY2025 basın bülteni |
| 2024 | 1.045 | [ThePrint/PTI](https://theprint.in/economy/buying-by-central-banks-leads-to-record-global-gold-demand-jewellery-demand-down-by-11-pc-in-2024-wgc/2480430) |
| 2025 | 863 (Ç4: 230) | [WGC, 29 Oca 2026](https://www.gold.org/news-and-events/press-releases/gold-investment-rockets-2025-setting-new-high-uncertainty-bites) |
| 2026 Ç1 | 57 (revize) | [WGC Ç2 bülteni](https://www.gold.org/news-and-events/press-releases/gold-market-shows-resilience-price-momentum-cools-q2) |
| 2026 Ç2 | 289 (Ç2 için rekor) | aynı |
| 2026 Ç3 | 321 (yıllık +%42; Ç4 2024'ten beri en yüksek); yılbaşından beri 675 (+%6) | [WGC, 3 Kas 2026](https://gold.org/news-and-events/press-releases/central-bank-buying-and-etf-inflows-support-gold-demand-q3) |
| Eylül 2026 | 61 (2026'nın en büyük aylık rakamı; Polonya ve Çin önde) | [WGC Goldhub Kasım 2026](https://www.gold.org/goldhub/gold-focus/2026/11) |

Ek bilgiler:
- WGC'ye göre Ç3 tahmininin yaklaşık üçte ikisi merkez bankalarınca **açıklanmayan** alımlardan oluşuyor.
- Fiyat hassasiyeti: WGC, diğer her şey sabitken 20–30 t ek rezerv alımının fiyatı yaklaşık %1 oynattığını söylüyor (Mid-Year Outlook 2026). Goldman 2022 öncesi ortalamayı ayda 17 t olarak veriyor; 2026 nowcast'ı ayda ~85 t (mevsimsellikten arındırılmış, 3 aylık).
- Neden alıyorlar: Arslanalp, Eichengreen & Simpson-Bell (IMF WP 2023/014; *JIE* 145, 2023), ABD, Birleşik Krallık, AB ve Japonya'nın finansal yaptırımlarının rezervlerde altın payını artırdığını buldu; payını ≥5 puan artıran 14 "aktif çeşitlendirici" ülkenin hepsi gelişmekte olan ekonomi ([EconPapers](https://econpapers.repec.org/RePEc:imf:imfwpa:2023/014)).
- WGC'nin 2026 merkez bankası anketinde (16 Haziran 2026) katılımcıların %89'u küresel resmî altın rezervlerinin 12 ayda artacağını bekliyor (2025'te %95); kendi rezervini artırmayı planlayanlar rekor %45 ([Kitco](https://www.kitco.com/news/article/2026-06-16/record-45-central-banks-plan-increase-gold-holdings-wgc-survey-finds)).
- De-dolarizasyon göstergesi: ECB'nin Haziran 2026 raporuna göre 2025 sonunda altın küresel resmî rezervlerin %27'si; ABD tahvili %22, euro %15. ECB bunun "büyük ölçüde değerleme etkisi" olduğunu söylüyor: 2023 sonu fiyatlarıyla altın ve euro ~%16, tahvil ~%26 ([UBS CIO, 3 Haz 2026](https://www.ubs.com/global/en/wealthmanagement/insights/chief-investment-office/house-view/daily/2026/latest-03062026.html)). Dolar FX rezervlerinin hâlâ ~%57'si.

Tahmin açısından sorun şu: Aylık merkez bankası verisi gecikmeli geliyor, çoğu açıklanmıyor ve WGC tahmini çeyreklik. Bu yüzden 1–5 günlük işlemde kullanılamaz; 6–12 ay için ise yön belirleyici bir değişken.

### 2.5 ETF akışları

- 2025: +801 t (ikinci en güçlü yıl). 2026: Mart ayında tarihin en büyük aylık çıkışı (~12 milyar USD, ikincil kaynak), Haziran'da -74 t (-8,9 milyar USD) ([Kitco, 8 Tem 2026](https://www.kitco.com/news/article/2026-07-08/investors-flee-gold-etfs-june-hawkish-fed-expectations-drive-liquidation)), ilk yarı toplam yalnızca +18 t (Ç2: -45 t).
- Ç3 2026: +211 t; toplam rekor 4.256 t. Ekim: +2,7 milyar USD, +19 t, toplam **4.275 t**. İlk 10 ayda +41 milyar USD (tarihteki 3. en güçlü), +246 t. Bölgesel Ekim akışı: Avrupa +1,8 milyar, Asya +1,3 milyar (Çin önde), Kuzey Amerika -512 milyon USD ([WGC](https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/11)).
- Goldman çerçevesinde Batılı ETF yatırımcısı Fed politika faizine duyarlı "inançlı alıcı" (aşağıda 4.1). Ekim'deki Kuzey Amerika çıkışı, likidite ihtiyacı ve yüksek Hazine getirisinin cazibesiyle açıklandı.
- Öngörü gücü: ETF akışları büyük ölçüde fiyatı **izliyor** (trend takibi). Pozisyonlama literatüründe de benzer sonuç var: 2013 tarihli bir PolyU tezi, CFTC "managed money" pozisyonlarının değerli metal fiyatlarını sürüklemediğini, aksine getirilere tepki verdiğini (pozitif geri besleme) buldu ([PolyU](https://theses.lib.polyu.edu.hk/handle/200/7971); zayıf kaynak). Aşırı pozisyonların "kontraryan sinyal" olduğu iddiası pratisyen yorumu; örneklem dışı akademik test **bulunamadı**.

### 2.6 Çin ve Hindistan

- **Çin:** PBoC Eylül 2026'da 23 t ekledi, Ekim 2023'ten beri en büyük aylık alım (WGC Çin güncellemesi). Goldman'a göre Ağustos itibarıyla 22 ay üst üste alım yapıldı. Çin primi Ağustos 2026'da 6 yılın zirvesine çıktı (WGC Goldhub başlığı). Ekim 2026 primi için birincil veri **bulunamadı**.
- **Şanghay priminin öngörü gücü zayıf:** Meader (Metals Focus), LBMA *Alchemist* 83. sayıda 2005–2015 günlük verisini inceledi. Gecikmeli korelasyonlar pozitif ama çok düşük ve istatistiksel olarak anlamsız. Dolar kontrollü regresyonda etki "mütevazı ama pozitif ve anlamlı". Olay çalışmasında boğa döneminde ≥%1 primden 1 ay sonra ortalama +33 USD; düşüş döneminde ≥%1 primden sonraki 10 günde -1 USD, >%0,2 iskontodan sonra -14 USD ([LBMA](https://www.lbma.org.uk/alchemist/issue-83/links-between-the-chinese-and-international-gold-prices)).
- **Hindistan:** Eylül 2026 ithalatı 1,8 milyar USD (aylık -%22, yıllık -%81; Mart 2024'ten beri en düşük). Yurt içi iskonto Eylül ortalamasında 66 USD/ons'tan 16 Ekim'de 8 USD'ye daraldı. Yatırım fonları 16 Ekim'den itibaren altın fon sepeti fonlarına yeni girişi geçici olarak durdurdu ([Upstox/WGC](https://upstox.com/news/personal-finance/commodities/pre-diwali-2026-5-key-trends-in-the-gold-market-according-to-wgc/article-202346/)). Ekim ortasında 3 aydan sonra ilk kez prim oluştu ([Money Metals](https://www.moneymetals.com/news/2026/10/19/india-gold-market-flips-to-premium-as-demand-improves-and-supplies-tighten-005302)).
- **Fiyat esnekliği:** Yüksek fiyatta Asya hane talebi düşüyor (2026 Ç3 mücevher -%17), ama fiyat düşünce "fırsatçı alıcı" olarak devreye giriyor. Goldman ve WGC bu tabanı "alt sınırı sınırlayan" etken olarak modelliyor.

### 2.7 Jeopolitik risk (GPR)

- **Endeks:** Caldara & Iacoviello (2022), *AER* 112(4): 1194–1225, gazete metinlerinden üretilen GPR endeksi; 1985–2019 ortalaması 100 ([veri](https://www.matteoiacoviello.com/gpr.htm)).
- **WGC:** GRAM modeline GPR eklendiğinde GPR'deki 100 puanlık artış altın getirisine ~**+%2,5** katkıyla ilişkili (5% düzeyinde anlamlı). Ancak R² yalnızca 0,635'ten 0,645'e çıkıyor ve etkinin bir kısmı petrol üzerinden geliyor ([WGC 2023](https://www.gold.org/goldhub/gold-focus/2023/10/you-asked-we-answered-whats-impact-of-geopolitics-on-gold)).
- **Baur & Smales (2020), *JBF* 117:** Değerli metaller jeopolitik riske karşı koruma sağlıyor; etki fiili olaylardan çok **tehditlerde** güçlü. Aşırı olaylarda tutarlı güvenli liman davranışı yalnızca altın ve gümüşte görülüyor ([EconPapers](https://econpapers.repec.org/RePEc:eee:jbfina:v:117:y:2020:i:c:s037842662030090x)).
- **Gupta, Karmakar & Pierdzioch (2024), *Computational Economics* 64: 487–513:** Aylık 1915–2021 verisinde ülke düzeyindeki GPR, özellikle random forest ile altın getiri ve volatilite tahminlerini iyileştiriyor.
- **2026 doğal deneyi (kendi hesabım + haberler):** Günlük GPR 2 Mart 2026'da 501'e fırladı (Mart ortalaması 325). Altın ilk gün +%1,2 yükseldi (GC=F 5.247,9 → 5.311,6), sonra Brent 71 → 118 USD'ye çıkarken 20 Mart'a kadar -%14 düştü (4.574,9). Haberlerin ortak açıklaması "petrol → enflasyon → indirim beklentisi bitti → dolar ve getiri yükseldi → altın düştü"; marj çağrıları satışı hızlandırdı ([Euronews, 30 Mar 2026](https://www.euronews.com/2026/03/30/gold-and-silver-prices-plunge-why-has-safe-haven-demand-faded-amid-iran-war)).
- **Kendi hesabım, GPR sıçraması sonrası getiriler:** En yüksek %5'lik GPR günlerinden sonra:
  - 2006–2021 (n=202): ertesi gün -%0,08 ve 5 gün -%0,35; tüm günlerin ortalaması +%0,03 ve +%0,15.
  - 2022–2026 (n=61): -%0,25 ve -%0,62; ortalama +%0,07 ve +%0,33.

  Anlamlılık testi yapılmadı ve 5 günlük pencereler örtüşüyor, yani zayıf kanıt. Yine de "GPR sıçradı, altın al" kuralı 1–5 günde işe yaramıyor. Tersine dönüş (fade) bir hipotez olarak test edilmeli.

### 2.8 ABD maliyesi, borç ve "değer kaybı" işlemi

Goldman 2025–26'daki yükselişin bir kısmını yapısal, taktik olmayan "debasement trade"e bağlıyor. Kasım 2026 notunda yukarı yönlü riski "mali sürdürülebilirlik kaygılarının korunma talebini canlandırması" olarak tanımlıyor. Ara seçim sonrası "kilitlenme, mali genişleme sınırlanır" yorumu getirileri düşürdü ve altını yükseltti; bu, mali politikanın altına **faiz kanalıyla** da etki ettiğini gösteriyor. ABD borç/açık düzeyini altın getirisine bağlayan, örneklem dışında test edilmiş bir çalışma **bulunamadı**; değişken anlatı düzeyinde güçlü, nicel tahmin düzeyinde zayıf.

### 2.9 Fed politika döngüsü

- 2026 akışı: indirim beklentileri önce Haziran ve Aralık 2027'ye kaydı (Goldman, 19 Haziran 2026), sonra 16 Eylül'de artırım geldi, Ekim'de 2 üye artırım istedi, Aralık artırımı %64–81 olasılıkla fiyatlanıyor.
- Goldman temel senaryosu: Aralık artırımı, indirimler 2027 ikinci yarısında. UBS: bir artırım daha, sonra 2027'de 2 indirim; piyasa 2027'ye kadar 75 bp'den biraz fazla artırım fiyatlıyor, UBS'e göre bu fazla şahin.
- Kurumların ortak tezi şu: "Sıkılaşma varış noktasını değil zamanlamayı değiştirir" (Goldman'ın Eylül notu). Fed indirimlere geçtiğinde ETF girişleri ve reel faiz düşüşü altını destekler. Bu tezin 6–12 aylık ufukta test edilmesi gerekiyor (aşağıda kendi bulgum).

### 2.10 Risk iştahı, petrol, likidite

- **Risk iştahı:** Altın–VIX haftalık korelasyonu tarihsel olarak ~0, 2026'da -0,14 (kendi hesabım). Baur & Lucey (2010, *Financial Review* 45(2): 217–229) altını ortalamada hisselere karşı koruma, aşırı düşüşlerde güvenli liman buldu, ancak etki kısa ömürlü: çalışma makalesi versiyonunda ~15 işlem günü ([EconPapers](https://econpapers.repec.org/RePEc:bla:finrev:v:45:y:2010:i:2:p:217-229)). 2026'nın Mart ve Ekim aylarında altın hisselerle birlikte düştü (likidite satışı).
- **Petrol:** Altın–Brent haftalık korelasyonu 2006–2021'de +0,19, 2022–2023'te +0,27, 2024–2025'te +0,13, **2026'da -0,31** (kendi hesabım). UBS'ten Staunovo da petrol, enflasyon ve altın arasında şu an "son derece güçlü korelasyon" olduğunu söylüyor (Reuters, 6 Kasım). 2026 rejiminde petrol yükselişi altın için **olumsuz**.
- **Likidite ve marj:** 30 Ocak 2026'daki rekor düşüş (vadeli >%11) borsaların marj artışları ve kalabalık pozisyonların çözülmesiyle bağlantılı; aynı dönemde Trump'ın Kevin Warsh'ı Fed başkanlığına aday göstermesi doları güçlendirdi. Mart 2026'da da marj kaynaklı tasfiye görüldü. 1–5 günlük riskin ana kaynağı bu tür zorunlu satışlar.

---

## 3. Akademik literatür: altın getirisi tahmin edilebilir mi?

### 3.1 Temel çalışmalar

| Çalışma | Örneklem / sıklık | Bulgu (etki büyüklüğü) | Örneklem dışı / yayın sonrası | Zayıflık |
|---|---|---|---|---|
| Hassani, Silva, Gupta & Segnon (2015), *Applied Economics* 47(39): 4141–4152 | Aylık altın; 17 yöntem (ARIMA, ETS, TBATS, AR, VAR, BVAR…) | Çalışma makalesi versiyonunda 1 ve 9 adım ileride **hiçbir yöntem rastgele yürüyüşü yenemiyor**; ortalamada en iyisi üstel düzleştirme; 24 aylık ufukta tek değişkenli modeller BVAR'ı yeniyor | Tamamen OOS | Tek değişkenli, makro bilgi yok ([EconPapers](https://econpapers.repec.org/RePEc:taf:applec:v:47:y:2015:i:39:p:4141-4152)) |
| Aye, Gupta, Hammoudeh & Kim (2015), *IRFA* 41: 257–266 | Aylık 1992:02–2013:11; OOS 1999:10–2013:11; h = 1, 3, 6, 9, 12 ay; 6 küresel faktör + 2 belirsizlik endeksi | DMS tüm ufuklarda en iyi; rastgele yürüyüşü ve BMA'yı yeniyor; döviz kuru faktörü baskın | Evet | Öngörücü seti ve parametreler zamanla değişiyor; işlem maliyeti yok ([UP](https://repository.up.ac.za/handle/2263/45456)) |
| Pierdzioch, Risse & Rohloff (2014), *QREF* 54(2): 292–305 | G7 çıktı açıkları, gerçek zamanlı | "Bir miktar" öngörü gücü var; işlem maliyeti sonrası basit kural **al-tut'u geçemiyor** | Gerçek zamanlı OOS | ([EconPapers](https://econpapers.repec.org/RePEc:eee:quaeco:v:54:y:2014:i:2:p:292-305)) |
| Pierdzioch, Risse & Rohloff (2015), *Applied Economics Letters* 22(1): 46–50 | Boosting; enflasyon, kur, hisse getirisi, faiz | Öngörücüler bir miktar güç taşıyor; işlem kuralı al-tut'u geçemiyor | Gerçek zamanlı OOS | ([EconPapers](https://econpapers.repec.org/RePEc:taf:apeclt:v:22:y:2015:i:1:p:46-50)) |
| Pierdzioch, Risse & Rohloff (2016), *NAJEF* 35: 38–55 | Kantil boosting | Kayıp fonksiyonuna (iyimser/kötümser yatırımcı) göre performans değişiyor | OOS | ([IDEAS](https://ideas.repec.org/a/eee/ecofin/v35y2016icp38-55.html)) |
| Risse (2019), *IJF* 35(2): 601–615 | Dalgacık ayrıştırması + SVR; küçük makro set | Zaman-frekans ayrıştırması tahmini iyileştiriyor; bileşenlerin önemi zamanla istikrarsız | OOS + işlem stratejisi | Özet sıklığı belirtmiyor; ML aşırı uyum riski ([EconPapers](https://econpapers.repec.org/RePEc:eee:intfor:v:35:y:2019:i:2:p:601-615)) |
| Gupta, Karmakar & Pierdzioch (2024), *Comput. Econ.* 64: 487–513 | Aylık 1915–2021 | Ülke düzeyindeki GPR, random forest ile tahmini iyileştiriyor | OOS | Aylık; işlem testi yok |
| Erb & Harvey (2013), *FAJ* 69(4): 10–42 | Aylık 1975–2012 | Reel fiyat ~10 yılda ortalamaya dönüyor; 2012 seviyesi yıllık ~-%10 reel getiri ima ediyordu | 2012–2015'te -%37 (doğru), sonra tamamen ters | Az sayıda bağımsız 10 yıllık gözlem |
| Baur & Lucey (2010), *Fin. Review* 45(2) | ABD, Birleşik Krallık, Almanya; günlük | Hisseler aşırı düştüğünde güvenli liman, ~15 gün | — | 2026'nın enflasyonist şokunda çalışmadı |
| Baur & Smales (2020), *JBF* 117 | GPR, günlük/aylık | Tehdit > fiili olay | — | Tahmin değil, koruma testi |
| Moskowitz, Ooi & Pedersen (2012), *JFE* 104(2): 228–250 | 58 vadeli (1984–), aylık | 1–12 ay zaman serisi momentumu, uzun vadede kısmen geri dönüyor | Yayın sonrası CTA'lar kalabalıklaştı | Altına özel sonuç makalede ayrıca raporlanmamış ([EconPapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:104:y:2012:i:2:p:228-250)) |
| Elder, Miao & Ramchander (2012), *JBF* 36(1): 51–65 | Gün içi altın/gümüş/bakır vadelileri | ABD makro sürprizlerine (özellikle 8:30 ET istihdam, dayanıklı mallar) hızlı ve anlamlı tepki | — | Tahmin değil, tepki: sürprizi bilmek gerekiyor ([EconPapers](https://econpapers.repec.org/RePEc:eee:jbfina:v:36:y:2012:i:1:p:51-65)) |
| Meader, LBMA *Alchemist* 83 (~2016) | Günlük 2005–2015 | Şanghay primi "mütevazı" öngörücü | — | Sektör analizi, hakemli değil |

**Ortak sonuçlar:**
1. Günlük ve haftalık ufukta makro değişkenlerin gecikmeli değerleri işlem maliyeti sonrası istikrarlı bir kazanç sağlamıyor.
2. Aylık ufukta bazı modeller (döviz faktörü, DMA/DMS, GPR + random forest) rastgele yürüyüşü yenebiliyor, ama öngörücü seti zamanla değişiyor. 2022 sonrası reel faiz kırılması bunun en çarpıcı örneği.
3. Uzun ufukta (5–10 yıl) değerleme ve ortalamaya dönüş "bir şey söylüyor", ama yapısal kırılma (yükselen piyasa merkez bankaları, ETF'ler) çok uzun sürebiliyor.
4. **Seviyeye karşı değişim:** Seviye modelleri (altın ~ reel faiz) eşbütünleşmeye dayanır ve kırılgandır; eşzamanlı değişim modelleri (Δaltın ~ Δreel faiz, Δ$) daha sağlamdır ama *tahmin* değil *açıklama* yapar, çünkü sağ taraftaki değişkeni bilmek gerekir. Pratikte işlemci sağ taraftaki değişkeni tahmin etmek zorunda (Fed, veri sürprizi), yani asıl iş makro tahmin.

### 3.2 Kendi örneklem dışı testlerim

**(a) Günlük, h = 1, 3, 5 gün** (GC=F 2006–2026; özyinelemeli OLS, 2016'dan itibaren her 5. günde tahmin, benchmark tarihsel ortalama):

| Öngörücü | OOS R² h=1 | h=3 | h=5 |
|---|---|---|---|
| Altın momentum 1g / 5g / 20g / 60g / 250g | -%0,03 / -%0,05 / -%0,17 / +%0,04 / -%0,07 | -%0,18 / -%0,09 / -%0,26 / +%0,06 / -%0,27 | -%0,15 / +%0,47 / -%0,10 / -%0,11 / -%0,18 |
| ΔTIPS 5g | +%0,65 | -%0,01 | -%1,44 |
| ΔTIPS 1g | +%0,27 (IS korr -0,077) | +%0,10 | +%0,09 |
| Δ$ 5g / Brent 5g / VIX seviyesi | +%0,04 / -%0,12 / -%0,01 | -%0,09 / -%0,95 / -%0,18 | -%0,22 / -%0,38 / +%0,01 |

Sonuç: 1–5 günde makro değişkenlerin gecikmeli değerleri pratikte sıfır öngörü gücü taşıyor. ΔTIPS(t)'nin ertesi gün altın getirisiyle küçük negatif ilişkisi (-0,077) büyük olasılıkla **kapanış saatleri arasındaki asenkronluktan** kaynaklanıyor: COMEX uzlaşması 13:30 ET, Hazine reel getiri eğrisi daha geç ölçülüyor. Bu durum VİOP için önemli, çünkü F_XAUUSD 18:10 TSİ'de (15:10 UTC) kapanıyor ve ABD öğleden sonrasının hareketi ertesi günün getirisine kayıyor. Lead-lag'in kaynağı bu; ayrıntısı ayrı ajanda.

**(b) Aylık, h = 1, 3, 6, 12 ay** (2001–2026; OOS 2012'den itibaren):

| Öngörücü | OOS R² 1 ay | 3 ay | 6 ay | 12 ay |
|---|---|---|---|---|
| TSMOM 12 ay | -%5,1 | -%11,6 | -%18,1 | -%21,7 |
| Momentum 3 ay / 1 ay | -%4,4 / -%4,2 | -%3,8 / -%2,1 | -%5,0 / -%1,8 | -%7,4 / -%1,9 |
| ΔTIPS 3 ay | -%1,1 | -%4,4 | -%4,0 | -%1,9 |
| Δ$ 3 ay | +%0,4 | +%0,1 | -%1,1 | -%1,3 |
| Reel fiyat (log altın/TÜFE) | %0,0 | -%0,7 | -%2,8 | -%12,2 |
| **TIPS seviyesi** | **+%3,9** | **+%12,3** | **+%24,1** | **+%35,4** |

- Şaşırtıcı bulgu: 10 yıllık TIPS **seviyesi** yüksekken sonraki aylarda altın getirisi daha yüksek; işaret naif teorinin tersi. 1 aylık ufukta alt örneklemlerde de pozitif (2012–2021: OOS R² +%5,1; 2022–2026: +%2,2).
- Olası mekanizma: reel faiz zirveleri Fed sıkılaşmasının sonuna denk geliyor (2008 sonu, 2018 sonu, 2023 Ekim) ve ardından gelen gevşeme altını yükseltiyor. 2013 "taper" dönemi bu kurala uymuyor.
- **Uyarı:** 12 aylık örtüşen pencerelerde yalnızca ~14 bağımsız gözlem var; bu bulgu kanıt değil, hipotez. Bugün TIPS %2,60, yani tarihsel olarak yüksek; hipoteze göre 6–12 ay için olumlu sinyal. Goldman, UBS ve JPMorgan'ın "2027 toparlanması" tezleriyle uyumlu, ama aynı zamanda 2022 benzeri bir senaryoda yanlış çıkabilir.
- TSMOM (12 ay > 0 ise al, değilse nakit) al-tut'a göre getiriyi artırmadı, volatiliteyi düşürdü:

  | Dönem | TSMOM yıllık getiri / vol | Al-tut yıllık getiri / vol |
  |---|---|---|
  | 2002–2011 | %17,1 / %18,4 | %18,2 / %18,8 |
  | 2012–2021 | %0,4 / %9,9 | %0,3 / %14,3 |
  | 2022–2026 | %12,0 / %16,3 | %17,0 / %17,3 |

---

## 4. Kurumların modelleri ve isabetleri

### 4.1 Goldman Sachs: "inançlı alıcılar / fırsatçı alıcılar" çerçevesi

- **Kurgu (18 Aralık 2025 tarihli 2026 Emtia Görünümü, birincil PDF):** İnançlı alıcılar (ETF'ler, merkez bankaları, spekülatörler) fiyattan bağımsız olarak makro ya da korunma görüşüyle alıyor; fırsatçı alıcılar (yükselen piyasalardaki haneler) fiyat uygun olunca devreye giriyor. Model, inançlı alıcıların net alımından fiyat ima ediyor; "yapışkan" versiyonu yalnızca merkez bankaları ve ETF'leri kapsıyor ([GS PDF](https://www.goldmansachs.com/pdfs/insights/goldman-sachs-research/2026-outlooks/CommoditiesOutlook2026.pdf)).
- **Parametreler:** Eylül 2025 tarihli GS makalesine göre inançlı alıcıların 100 t net alımı fiyatı ~**%1,7** artırıyor (yalnızca arama özetinden doğrulandı). ABD özel finansal portföylerinde altın payındaki her 1 bp artış (fiyat etkisi değil, yeni alım) fiyatı ~**%1,4** artırıyor; ETF'ler ABD özel portföylerinin %0,17'si, 2012 zirvesinin 6 bp altında (GS PDF). Merkez bankası alımı varsayımı Aralık 2025'te ayda 70 t'ydi ve 2026 sonuna kadar beklenen artışa ~14 puan katkı yapıyordu.
- **Varsayımların oynaklığı:** Merkez bankası alımı varsayımı Aralık 2025'te ayda 70 t, Ocak 2026'da 60 t, Haziran 2026'da 50 t (2027: 40 t), Kasım 2026'da 60 t oldu. Nowcast Eylül'de ~90 t, Kasım'da 85 t.
- **İsabet (2026 sonu hedefinin evrimi):**

  | Tarih | 2026 sonu hedefi | O günkü spot |
  |---|---|---|
  | Ekim–Aralık 2025 | 4.900 | — |
  | 22 Ocak 2026 | 5.400 | ~4.888 (spot zirve o gün) |
  | 19 Haziran 2026 | 4.900 | ~4.200–4.250 (GC=F 18 ve 22 Haziran kapanışları) |
  | ~19 Eylül 2026 | 4.650 | ~4.350 (Reuters); GC=F ~4.425 |
  | 5 Kasım 2026 | 4.150 | ~4.080–4.118 |

  Hedef her revizyonda fiyatın yaklaşık %1–16 üstünde kaldı ve fiyat düştükçe aşağı çekildi (ör. 5.400/4.888 ≈ +%10; 4.900/4.225 ≈ +%16; 4.650/4.350 ≈ +%7; 4.150/4.100 ≈ +%1). Model *yön* açısından yapısal talebi doğru yakaladı, ama *zamanlama* (Fed, ETF, spekülatif pozisyon) açısından başarısız oldu.

### 4.2 JPMorgan

Talep modelini çeyreklik ortalamalar üzerinden kuruyor. Ekim 2025'te 2026 Ç4 ortalaması için 5.055 USD öngördü ([Kitco/Reuters](https://www.kitco.com/news/off-the-wire/2025-10-23/jp-morgan-sees-gold-prices-averaging-5055-ounce-late-2026)). 9 Haziran 2026'da yıl sonu 6.000 USD dedi; 3 Temmuz 2026'da Ç3 4.300, Ç4 4.500'e indirdi ve riskleri aşağı yönlü gördü. Temmuz'dan sonraki revizyon **bulunamadı**. İsabet: Ç3 2026 ortalaması 4.262 (WGC), Temmuz tahmini 4.300'e çok yakın; Haziran tahmini ise tamamen yanlış.

### 4.3 UBS

Merkez bankası alımı (yılda 750–1.000 t), reel faiz ve dolar varsayımlarına dayalı bir çeyreklik hedef yolu kuruyor. Şubat 2026'da Mart çeyreği için 6.200 hedefliyordu ([Motley Fool AU](https://www.fool.com.au/2026/02/09/ubs-raises-gold-price-target-to-us6200-per-ounce-for-this-quarter)), Haziran 2026'da 1. yarı 2027 için 5.500 ([UBS CIO](https://www.ubs.com/global/en/wealthmanagement/insights/chief-investment-office/house-view/daily/2026/latest-03062026.html)). Ekim 2026 yolu Aralık 2026 için 4.600. İsabet: Mart çeyreği hedefi 6.200 iken gerçekleşen 4.6xx (GC=F Mart sonu 4.647,6).

### 4.4 Citi

0–3 ay ve 6–12 ay ufuklarına "taktik" hedefler veriyor. Haziran 2025'te 6–12 ay için 2.800 USD'lik ayı senaryosu açıkladı ([Kitco](https://www.kitco.com/news/article/2025-06-19/citi-sees-gold-prices-falling-below-3000-end-year)); 12 ay sonra fiyat 4.000 USD'nin üstündeydi, yani en büyük ıskalardan biri. 2026'da 0–3 ay hedefini 5.000 (Ocak), 4.300 (Nisan), 4.000 (9 Haziran) olarak verdi; 6–12 ay hedefi 4.500–5.000 aralığında.

### 4.5 World Gold Council: GRAM ve GVF/Qaurum

- **GRAM (Gold Return Attribution Model):** Haftalık ve aylık altın getirisinin ~15 açıklayıcı değişkenle çoklu regresyonu. Dört tema var: ekonomik büyüme, risk ve belirsizlik, fırsat maliyeti (kur ve faiz), momentum. Spot XAU kullanılıyor. Açıklanamayan kısım (residual) merkez bankası alımları ve olay primleri olarak yorumlanıyor; çünkü güvenilir aylık merkez bankası serisi yok ([GRAM aracı](https://www.gold.org/goldhub/tools/gold-return-attribution-model)). Bir **atfetme** (attribution) aracı, tahmin aracı değil. 2026 1. yarısında oynaklığın %30'u modelin dışında kaldı.
- **GVF / Qaurum (Ocak 2020):** Talep ve arz dengesinden "ima edilen" altın getirisini Oxford Economics makro senaryolarıyla hesaplıyor; ufuk 5 yıl ve 30 yıl. WGC kendisi "altın fiyatını tahmin etmez, eğitim amaçlıdır" diyor ([WGC](https://www.gold.org/goldhub/portfolio-tools/gold-valuation-framework)). İsabet ölçümü yayımlanmamış.
- **WGC senaryo tahmini:** Mid-Year Outlook 2026'da 2. yarı için ~4.100 ±%5, yani 3.895–4.305 aralığı. Gerçekleşen yol: Temmuz–Kasım 2026 GC=F kapanışları 3.899–4.697 aralığında (Ağustos zirvesi 4.697,8). Ağustos ve Eylül başında üst bant aşıldı; Kasım başı fiyat banda geri döndü. Tahmin isabetli, ama bandın %10 genişliğinde olduğunu unutmamak gerekiyor.

---

## 5. Pratik tahmin çerçevesi

### 5.1 1–5 gün (VİOP F_XAUUSD, kapanıştan kapanışa ~18:10 TSİ)

Gerçekçi beklenti: Gecikmeli makro değişkenlerle yön tahmini neredeyse imkânsız (bölüm 3). Bu ufukta para kazananlar şunları yapıyor:
1. **Olay ve sürpriz yönetimi:**
   - ABD verileri (8:30 ET = kışın 16:30 TSİ, yazın 15:30 TSİ) **uzlaşmadan önce** geliyor ve aynı günün getirisine yansıyor.
   - FOMC (14:00 ET = kışın 22:00 TSİ, yazın 21:00 TSİ) **uzlaşmadan sonra** geliyor ve ertesi günün getirisine yansıyor.
   - 2026 rejiminde ilişki şöyle: güçlü istihdam ya da enflasyon → Aralık artırımı olasılığı artar → 2 yıllık getiri ve dolar yükselir → altın düşer (6 Kasım örneği: istihdam +165 bin, beklenti ~65 bin; altın -%0,9, 2y +6 bp).
   - Elder ve ark. (2012) bu tepkinin dakikalar içinde gerçekleştiğini gösteriyor. Avantaj tepkiyi tahmin etmekte değil, sürprizin yönünü ya da pozisyon riskini yönetmekte.
2. **Eşzamanlı sürücüleri izlemek:** Aynı gün ΔTIPS, Δ2y, ΔDXY ve 2026'da Brent (negatif işaretli). Bunlar getiriyi "açıklar"; izlemenin yararı yanlış fiyatlamayı (ör. VİOP–spot farkı) yakalamak ve kapanış sonrası ABD seansının taşıdığı bilgiyi okumak.
3. **Saat farkı ve asenkronluk (BIST'e özgü):**
   - LBMA PM fixingi 15:00 Londra saatinde: kışın 18:00 TSİ, yazın 17:00 TSİ. Kışın VİOP uzlaşma penceresiyle (son 10 dakikanın hacim ağırlıklı ortalaması) neredeyse çakışıyor.
   - COMEX uzlaşması kışın 21:30 TSİ, yazın 20:30 TSİ.
   - 18:10'dan sonraki ABD hareketi ertesi günün VİOP getirisinin bir parçası; lead-lag fırsatı burada aranmalı.
4. **Pozisyon ve marj riski:** COMEX net uzunlar (WGC aylık; CFTC her Cuma), ETF akışları ve borsaların marj değişiklikleri. 30 Ocak ve Mart 2026 örnekleri 1–5 günlük kuyruk riskinin kaynağı.
5. **Volatiliteye göre pozisyon:** 2026'da 1 günlük hareketin standart sapması %1,9, 3 günlük %3,1, 5 günlük %3,9 (2015–2024'te %0,9 / %1,6 / %2,1). GVZ ~26. Aynı risk için pozisyon boyutu, 2015–2024 normallerine göre yaklaşık yarıya inmeli.
6. **Jeopolitik başlık:** GPR sıçramalarında 1–5 gün içinde ortalama getiri negatif çıktı (kendi hesabım, zayıf kanıt). Petrol üzerinden enflasyon kanalı çalışıyorsa altın düşüyor (Mart 2026).

### 5.2 1–3 ay

| Gösterge | Beklenen yön | Kanıt gücü | Nereden izlenir |
|---|---|---|---|
| Fed yolu (FedWatch, dot plot, Fed konuşmaları) | Daha şahin → altın aşağı | Güçlü (2026'da açık) | CME FedWatch; Fed |
| 10y TIPS **değişimi** | Yükselirse altın aşağı (2026 betası ~-%16 / 1 puan) | Orta (rejime bağlı) | FRED DFII10 |
| Dolar (DXY, geniş endeks) | Güçlenirse altın aşağı | Güçlü ve istikrarlı (korr ~-0,4) | FRED DTWEXBGS |
| ETF akış trendi | Giriş → destek | Orta (fiyatı izliyor) | WGC aylık ve haftalık |
| Merkez bankası aylık alımları | Hızlanırsa destek | Orta (gecikmeli veri) | WGC; PBoC |
| Petrol ve enflasyon beklentisi | 2026'da petrol yükselişi altın için olumsuz | Orta (yeni rejim) | Brent; T10YIE |
| Çin primi ve Hindistan iskontosu | Prim ya da iskonto daralması → fiziksel destek | Zayıf–orta | SGE/LBMA; WGC Hindistan |
| TSMOM 3–12 ay | Getiriyi değil volatiliteyi azaltıyor | Orta | Kendi hesabım |

### 5.3 6–12 ay

1. **Merkez bankası alım hızı:** Ayda 60 t ve üstü yapısal taban (Goldman; WGC: 20–30 t ≈ %1).
2. **Fed döngüsünün dönüşü:** İndirime geçiş ETF girişlerini ve reel faiz düşüşünü getirir. Kendi bulgum: yüksek TIPS seviyesinden sonraki 6–12 ay getirisi tarihsel olarak yüksek (hipotez).
3. **Mali ve de-dolarizasyon anlatısı:** Altının rezerv payı (ECB), yaptırımlar (IMF).
4. **Özel yatırımcı çeşitlendirmesi:** ETF'lerin ABD portföyündeki payı %0,17; her 1 bp ≈ +%1,4 (Goldman).
5. **Değerleme:** Reel fiyat oranı 12,1, 1975–2012 ortalaması 3,2'nin yaklaşık 4 katı (Erb–Harvey). 10 yıllık ufukta düşük getiri riski; 6–12 ayda zamanlama aracı değil.
6. **Senaryo bantları:** Goldman 2027 sonu 4.800 (aşağı 4.660), konsensüs 2027 ortalaması 4.650, UBS 2027 Eylül 5.400, WGC 3.860 teknik seviyesi.

### 5.4 Türkiye fiyatına köprü (kısaca)

Gram altın (TL) ≈ XAU/USD × USD/TRY / 31,1035. 6 Kasım'da F_XAUTRYM1226 6.855,7 TL ve F_XAUUSD1226 4.078,8 USD verildiğine göre ima edilen Aralık USD/TRY ≈ 6.855,7 × 31,1035 / 4.078,8 ≈ **52,28** (kendi hesabım). Yani TL altın = küresel ons + kur; küresel kısmın tahmini bu raporda, kur kısmı ayrı raporda.

### 5.5 VİOP doğrulaması

Borsa İstanbul duyurusu 30572 (Sayı E-18454353-100.04.02-30572, 19.11.2024) aslında **bakır** vadelisinin işleme açılmasıyla ilgili. Ekindeki VİOP Prosedürü değişikliğinin "7. Akşam Seansına Dahil Olan Sözleşmeler" maddesinde Dolar/Ons Altın vadeli sözleşmeleri akşam seansı listesinde yer alıyor. Aynı ekte bakır için şu kurallar yazıyor: günlük uzlaşma fiyatı seans bitiminden önceki son 10 dakikadaki işlemlerin hacim ağırlıklı ortalaması; akşam seansının baz fiyatı normal seans sonunda hesaplanan uzlaşma fiyatı ([Borsa İstanbul PDF](https://borsaistanbul.com/files/duyuru-30572-TR.pdf)). Akşam seansı saati (19:00–23:00) ve ons altının bu seansta işlem gördüğü aracı kurum ve basın kaynaklarında tutarlı ([Capital](https://www.capital.com.tr/haberler/tum-haberler/borsada-dolarons-altin-sozlesmeleri-aksam-seansinda-da-islem-gorecek)). Ancak 19:00–23:00 saatleri 30572'nin metninde geçmiyor. Normal seans bitişi kaynaklarda 18:10 ve 18:15 olarak farklı veriliyor; güncel BIST prosedüründen teyit edilmeli.

---

## 6. Test edilecek hipotezler (bizim veride)

1. **H1 (asenkron kapanış):** F_XAUUSD'nin t günü uzlaşma getirisi (18:10 → 18:10), t-1 günü 18:10 TSİ'den sonra gerçekleşen spot XAU hareketiyle (ör. 18:10 → 23:00 akşam seansı kapanışı ya da COMEX 21:30 TSİ uzlaşması) pozitif ilişkilidir. Kendi FRED/COMEX testimde ΔTIPS(t)'nin ertesi gün getirisiyle korelasyonu -0,077.
2. **H2:** Gündüz uzlaşmasından sonra gelen ABD 10y TIPS ve 2y getiri değişimi, ertesi günün F_XAUUSD getirisini negatif yönde öngörür.
3. **H3 (2026 rejimi):** Brent getirisi ile F_XAUUSD getirisi arasındaki korelasyon 2026'da negatif, 2022 öncesinde pozitif. Rejim değişkeni olarak "Fed artırım olasılığı" eklenmeli.
4. **H4:** GPR'nin en yüksek %5'lik günlerinden sonraki 1, 3 ve 5 günlük F_XAUUSD getirisi ortalamanın altında (tersine dönüş).
5. **H5:** 10y TIPS seviyesi yüksekken sonraki 1–3 aylık (21–63 iş günü) getiri daha yüksek. Bu bir Fed döngüsü dönüm noktası etkisi mi, alt örneklemlerle test edilmeli.
6. **H6:** ABD istihdam ve TÜFE günlerinde sürprizin yönü (gerçekleşen − beklenti) aynı günün F_XAUUSD getirisiyle 2026'da negatif ilişkili.
7. **H7:** FOMC kararlarından sonraki ilk VİOP uzlaşma günü mutlak getirisi, olağan günlerden büyük. Karar akşam seansına denk geliyor.
8. **H8:** 3 ve 12 aylık TSMOM işaretine göre 5 günlük tutma, al-tut'a göre getiriyi değil volatiliteyi azaltır, Sharpe oranını hafif artırır.
9. **H9:** Haftalık CFTC managed money net pozisyon değişimi sonraki haftanın getirisini öngörmez (pozitif geri besleme). Aşırı pozisyon yüzdelikleri (üst ve alt %10) sonrası getiriler ayrıca test edilmeli.
10. **H10:** Şanghay primindeki (SGE Au9999 − LBMA, USD) günlük değişim ertesi günün getirisine zayıf pozitif katkı yapar.
11. **H11:** 2026'da getirinin Asya saatlerinde kazanılıp ABD saatlerinde kaybedildiği iddiası (12,9% Asya-saati kazancı rakamı yalnızca bir arama özetinde geçiyor, doğrulanamadı). VİOP gündüz seansı (06:30–15:10 UTC) Asya öğleden sonrası ile Londra'yı kapsıyor; gece ve gündüz getirisi ayrıştırılarak test edilmeli.

---

## 7. Bulunamayanlar ve belirsizlikler

- JPMorgan'ın Temmuz 2026 sonrası ve Citi'nin Eylül 2026 sonrası gold hedefleri için birincil kaynak **bulunamadı**.
- Goldman'ın "100 t = %1,7" kuralı yalnızca GS sitesinin arama özetinden geldi; makale 403 hatası verdi. Aralık 2025 PDF'indeki %1,4/bp kuralı ise doğrudan okundu.
- 2023 merkez bankası alımının kesin tonajı birincil WGC kaynağında doğrulanamadı.
- Ekim 2026 Şanghay primi ve Hindistan Ekim ithalatı **bulunamadı**.
- İran savaşının kesin başlangıç tarihi birincil kaynakta doğrulanmadı. GPR günlük verisi 2 Mart 2026'daki sıçramayı (501) gösteriyor; Euronews'in 26 Mart başlığı savaşı "yaklaşık bir aylık" diye tanımlıyor.
- 2026 tepe fiyatı kaynaklara göre değişiyor: spot gün içi 5.589–5.608 USD (WGC 5.595,47; CBS 5.589,38; Reuters 5.594,82). LBMA PM 5.405,00 (WGC).
- Aralık FOMC'si için artırım olasılığı 5–6 Kasım'da farklı Reuters haberlerinde %64, %70 ve %81 olarak geçiyor.
- Kendi hesaplarımda GC=F sürekli vadeli serisi kullanıldı; vade geçiş sıçramaları ve Yahoo'nun kapanış tanımı (uzlaşma ya da son fiyat) küçük hatalar yaratabilir. FRED serileri ABD Hazine/Fed kapanış saatlerine göre ölçülüyor.

---

## 8. Kaynaklar (seçilmiş)

- Fed açıklamaları: [16 Eyl 2026](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm), [28 Eki 2026](https://www.federalreserve.gov/newsevents/pressreleases/monetary20261028a.htm), [FOMC takvimi](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)
- BLS: [TÜFE takvimi](https://www.bls.gov/schedule/news_release/cpi.htm), [istihdam takvimi](https://www.bls.gov/schedule/news_release/empsit.htm)
- WGC: [GDT Ç3 2026](https://gold.org/news-and-events/press-releases/central-bank-buying-and-etf-inflows-support-gold-demand-q3), [GDT Ç2 2026](https://www.gold.org/news-and-events/press-releases/gold-market-shows-resilience-price-momentum-cools-q2), [FY2025](https://www.gold.org/news-and-events/press-releases/gold-investment-rockets-2025-setting-new-high-uncertainty-bites), [Mid-Year Outlook 2026](https://www.gold.org/goldhub/research/gold-mid-year-outlook-2026), [ETF Ekim 2026](https://www.gold.org/goldhub/research/gold-etfs-holdings-and-flows/2026/11), [GRAM](https://www.gold.org/goldhub/tools/gold-return-attribution-model), [GPR analizi](https://www.gold.org/goldhub/gold-focus/2023/10/you-asked-we-answered-whats-impact-of-geopolitics-on-gold), [GVF](https://www.gold.org/goldhub/portfolio-tools/gold-valuation-framework), [Goldhub Kasım 2026](https://www.gold.org/goldhub/gold-focus/2026/11)
- Goldman Sachs: [2026 Emtia Görünümü PDF (18 Ara 2025)](https://www.goldmansachs.com/pdfs/insights/goldman-sachs-research/2026-outlooks/CommoditiesOutlook2026.pdf); [5 Kas 2026 revizyonu](https://finance.yahoo.com/markets/commodities/articles/goldman-lowers-end-gold-price-081423381.html); [Eylül 2026 revizyonu](https://investinglive.com/commodities/icymi-goldman-trims-end-2026-gold-forecast-to-4-650-but-holds-5-400-target-for-2027/); [Haziran 2026 revizyonu](https://www.mining.com/goldman-cuts-gold-price-forecast-down-to-4900/); [Ocak 2026 revizyonu](https://www.engineeringnews.co.za/article/goldman-sachs-raises-2026-end-gold-price-forecast-2026-01-22)
- Reuters/Kitco: [5 Kas](https://www.kitco.com/news/off-the-wire/2026-11-05/gold-hits-2-week-high-dollar-yields-oil-fall-after-us-midterms), [6 Kas](http://www.kitco.com/news/off-the-wire/2026-11-06/gold-drops-stays-track-best-week-over-two-months), [6 Kas istihdam](https://www.kitco.com/news/article/2026-11-06/gold-falls-us-payrolls-surge-165000-strengthening-december-fed-hike-case), [JPM 6 Tem](https://www.kitco.com/news/off-the-wire/2026-07-06/jpmorgan-sees-4500-gold-price-fourth-quarter-says-risks-downside), [Citi 9 Haz](https://www.kitco.com/news/article/2026-06-09/citi-cuts-near-term-gold-price-target-4300-4000-warns-limited-upside), [Reuters anketi 27 Eki](http://whtc.com/2026/10/27/strong-dollar-high-yields-drag-on-gold-outlook-but-central-bank-demand-lends-support/)
- Akademik: Barsky & Summers 1988 ([EconPapers](https://econpapers.repec.org/RePEc:ucp:jpolec:v:96:y:1988:i:3:p:528-50)); Erb & Harvey 2013 ([PDF](https://people.duke.edu/~charvey/Research/Published_Papers/P113_The_golden_dilemma.pdf)); Baur & Lucey 2010 ([EconPapers](https://econpapers.repec.org/RePEc:bla:finrev:v:45:y:2010:i:2:p:217-229)); Baur & Smales 2020 ([EconPapers](https://econpapers.repec.org/RePEc:eee:jbfina:v:117:y:2020:i:c:s037842662030090x)); Caldara & Iacoviello 2022 ([AER](https://www.aeaweb.org/doi/10.1257/aer.20191823)); Aye ve ark. 2015 ([UP](https://repository.up.ac.za/handle/2263/45456)); Hassani ve ark. 2015 ([EconPapers](https://econpapers.repec.org/RePEc:taf:applec:v:47:y:2015:i:39:p:4141-4152)); Pierdzioch ve ark. 2014/2015/2016 ([1](https://econpapers.repec.org/RePEc:eee:quaeco:v:54:y:2014:i:2:p:292-305), [2](https://econpapers.repec.org/RePEc:taf:apeclt:v:22:y:2015:i:1:p:46-50), [3](https://ideas.repec.org/a/eee/ecofin/v35y2016icp38-55.html)); Risse 2019 ([EconPapers](https://econpapers.repec.org/RePEc:eee:intfor:v:35:y:2019:i:2:p:601-615)); Moskowitz, Ooi & Pedersen 2012 ([EconPapers](https://econpapers.repec.org/RePEc:eee:jfinec:v:104:y:2012:i:2:p:228-250)); Elder, Miao & Ramchander 2012 ([EconPapers](https://econpapers.repec.org/RePEc:eee:jbfina:v:36:y:2012:i:1:p:51-65)); Arslanalp, Eichengreen & Simpson-Bell 2023 ([EconPapers](https://econpapers.repec.org/RePEc:imf:imfwpa:2023/014)); LBMA Alchemist 83 ([LBMA](https://www.lbma.org.uk/alchemist/issue-83/links-between-the-chinese-and-international-gold-prices))
- Veri: FRED (fred.stlouisfed.org), Yahoo Finance GC=F, GPR ([matteoiacoviello.com/gpr.htm](https://www.matteoiacoviello.com/gpr.htm))
- Borsa İstanbul: [Duyuru 30572](https://borsaistanbul.com/files/duyuru-30572-TR.pdf)
