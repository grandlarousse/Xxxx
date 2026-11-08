# r2 — Altında 1–5 günlük tutuşla "para kazandırdığı" söylenen stratejiler: kanıt derlemesi ve VİOP F_XAUUSD test planı

Tarih: 2026-11-07. Kapsam: VİOP "Dolar/Ons Altın" vadeli (F_XAUUSD), günlük uzlaşma fiyatından uzlaşma fiyatına (kapanıştan kapanışa) 1, 3 ve 5 iş günü tutuş.

Okuma kuralı: Her iddianın yanında kaynak var. "Bulunamadı" yazan yerde birincil kaynağa ulaşamadım; o boşluğu tahminle doldurmadım. Akademik kanıtların çoğu COMEX vadelisi, LBMA fiksingi veya GLD üzerinden. VİOP kapanışına (≈15:15 UTC) uyarlanmış yayımlanmış bir test bulamadım. Bu yüzden her aile için "bizim veride nasıl test edilir" kısmı ayrıca yazıldı.

---

## 0. Tek bakışta sonuç

| Aile | Altına özgü kanıt | 1–5 gün ufkunda yön | Yayın sonrası / örneklem dışı | Maliyet sonrası beklenti (VİOP, 1–5 gün) |
|---|---|---|---|---|
| Zaman serisi momentumu / trend (MA, Donchian, 52 hafta) | Orta (çoklu emtia, aylık); altına özgü ve günlük kanıt zayıf | Pozitif ama küçük | Altında 200 günlük ortalama sinyali 1990 sonrası çalışmıyor (CXO) | Sinyal yavaş değiştiği için maliyet düşük; işlem başına kenar küçük |
| Kısa vadeli dönüş (1–5 gün, RSI(2), Bollinger) | Zayıf / yok | Belirsiz | Altın için yayımlanmış test bulunamadı | Günlük devirde maliyet kenarı yer |
| >2σ gün sonrası | Zayıf | Ertesi gün hafif ters yön, istatistiksel olarak anlamsız | Caporale ve Plastun: t = 1,36 ve 0,73 | Sıfıra yakın |
| Oynaklık rejimi / hedefleme / GVZ | Hedefleme: emtiada Sharpe iyileşmesi yok; GVZ: kanıt yok | Riski düzeltir, getiriyi değil | Harvey ve diğ. 2018 | Risk yönetimi aracı, alfa kaynağı değil |
| Takvim (haftanın günü, ay dönümü, ay mevsimselliği, festival, Ramazan) | Zayıf–orta, kararsız | Pazartesi zayıf, Ocak/Eylül/Kasım güçlü iddiaları | Sonbahar etkisi tersine dönmüş (2024 replikasyonu) | Çoğu filtre olarak kullanılabilir |
| Seans (gece pozitif, gündüz negatif; "Asya'da yükselir, NY'de düşer") | Orta (COMEX 1985–2012) | VİOP kapanıştan kapanışa ile doğrudan yakalanamaz | Asimetri "belirgin şekilde zayıfladı" | VİOP'ta uygulanabilirliği düşük |
| Olay (FOMC, CPI, NFP, jeopolitik) | Dakikalık tepki güçlü; çok günlük sürüklenme kanıtı yok | FOMC tepkisi VİOP'ta ertesi günün getirisine düşer | Hisse senedinde FOMC öncesi sürüklenme zayıfladı | Volatilite yüksek, yön kenarı kanıtsız |
| COMEX opsiyon vadesi / roll / endeks roll / ay sonu | Altına özgü hakemli kanıt yok | Pratisyen iddiası: vade öncesi baskı | Goldman roll ön-alımı (2000–2010) yayımlandı | Test edilmeli |
| COT uçları, ETF akışı, Google Trends | Zayıf; çoğunlukla fiyat akışı/ilgiyi önden yönlendiriyor | Akış ve ilgi fiyatı takip ediyor | — | Kanıt zayıf |
| Şanghay primi | Zayıf (sektör analizi) | Prim yüksekken bir ay sonra +33 $ (boğa dönemi), etki "mütevazı" | — | Test edilmeli |
| Altın/gümüş oranı, madenci sapması, reel faiz/dolar artığı, carry | Zayıf / yok | Madenciler altını önden göstermiyor; altın madencileri önden gösteriyor | — | Göreli değer VİOP tek bacakla zor |
| Risk kapalı (VIX sıçraması) | Orta (aylık–haftalık güvenli liman) | ABD/Avrupa hisse çöküşünde altın tutunur, 15 iş günü | Aşırı oynaklıkta altın da satılabiliyor | Koşullu filtre |
| Perakende teknik (RSI, MACD, Fibonacci, destek-direnç, ICT) | Yok / zayıf | — | Veri madenciliği düzeltmesinden sonra çoğu kural kazandırmıyor | Negatif (maliyet) |

---

## 1. VİOP F_XAUUSD: zamanlama ve maliyet gerçekleri (doğrulanmış)

### 1.1 Seanslar ve uzlaşma fiyatı
- **Normal seans 09:30–18:15 TSİ (06:30–15:15 UTC), akşam seansı 19:00–23:00 TSİ (16:00–20:00 UTC).** İş Bankası'nın 22.02.2024 tarihli VİOP eğitim dokümanındaki "Kıymetli Madenler Vadeli İşlem Sözleşmeleri" bölümünde böyle yazıyor. 18:10 kapanışı pay vadelileri için geçerli. Görev metnindeki "~18:10" ons altın için değil, pay vadelileri için doğru. https://www.isbank.com.tr/contentmanagement/Documents/sozlesme-ve-formlar/2024/iscep-viop-egitimi-22.02.2024.pdf
- **Günlük uzlaşma fiyatı = seans bitmeden önceki son 10 dakikadaki işlemlerin miktar ağırlıklı ortalaması.** Son 10 dakikada 10'dan az işlem varsa son 10 işlemin ortalaması kullanılır. Daha az işlem varsa tüm işlemlerin ortalaması alınır. Hiç işlem yoksa önceki günün uzlaşması geçerlidir. Uzlaşma Fiyatı Komitesi müdahale edebilir (aynı İşbank dokümanı; aynı kural BIST duyurusu 30572'de metal sözleşmesi için açıkça yazıyor). Pratikte bu, **18:05–18:15 TSİ = 15:05–15:15 UTC VWAP** demek. https://borsaistanbul.com/files/duyuru-30572-TR.pdf
- **Duyuru 30572 doğrulaması.** Sayı E-18454353-100.04.02-30572, tarih 19.11.2024. Asıl konusu bakır vadelisinin işleme açılması (06.12.2024). VİOP Prosedürü madde 7'nin mevcut metni ("Akşam seansında BIST 30 …, **Dolar/Ons Altın**, Dolar/Ons Gümüş, Dolar/Ons Platin ve Dolar/Ons Paladyum Vadeli İşlem Sözleşmeleri işlem görür") ons altının akşam seansında olduğunu teyit ediyor. Aynı ekte "Akşam seansında işlem gören sözleşmelerin baz fiyatı, normal seans sonunda hesaplanan uzlaşma fiyatıdır" ifadesi ve ±%10 günlük limit bakır için yazılı. https://borsaistanbul.com/files/duyuru-30572-TR.pdf
- **Akşam seansı ons altında 18 Eylül 2020'de başladı** (BIST duyurusu 12590, 17.09.2020). https://borsaistanbul.com/duyuru/12590/usdtry-vadeli-islem-sozlesmelerinde-esnek-sozlesme-olusturma-ozelliginin-devreye-alinmasi-dolarons-altin-vadeli-islem-sozlesmelerinin-aksam-seansinda-islem-gormesi-ve-viop-proseduru
- **Vade sonu uzlaşma fiyatı = son işlem günündeki LBMA Gold Price PM** (BIST duyurusu 11834, 17.04.2015). https://borsaistanbul.com/duyuru/11834/viopta-altina-dayali-sozlesmelerde-vade-sonu-uzlasma-fiyatina-iliskin-guncelleme-yapilmistir
- **Sözleşme 1 ons. Vade ayları Şubat, Nisan, Haziran, Ağustos, Ekim, Aralık** (İşbank 2024 dokümanı). Minimum fiyat adımını GCM 0,05 olarak veriyor, eski bir arama özeti 0,10 diyordu. Güncel değeri sözleşme unsurlarından kontrol edin. https://www.gcmyatirim.com.tr/egitim/makaleler/ons-altin-usd-ons-xauusd-vadeli-islem-sozlesmesinde-islem-nasil-yapilir

### 1.2 Kapanışın küresel saatlere göre yeri (Kasım 2026 kış saati; ABD yaz saati 1 Kasım 2026'da, İngiltere 25 Ekim 2026'da bitti)
- **LBMA Gold Price PM** saat 15:00 Londra'da. Kışın 15:00 UTC'ye, yazın 14:00 UTC'ye denk geliyor. Yani VİOP uzlaşma penceresi (15:05–15:15 UTC) kışın PM fiyatından **5–15 dakika sonra**, yazın 65–75 dakika sonra açılıyor. Saat 15:00'in kaynağı BIST duyurusu 11834 ve IBA'nın PM fiyat tanımı.
- **ABD 08:30 ET verileri (NFP, CPI, PCE, başvurular)** kışın 13:30 UTC'de, yazın 12:30 UTC'de geliyor. Hepsi **aynı günün** VİOP kapanıştan kapanışa getirisine düşüyor ve VİOP kapanışına 1 saat 45 dakika ile 2 saat 45 dakika kalmış oluyor.
- **FOMC kararı (14:00 ET)** kışın 19:00 UTC'de, yazın 18:00 UTC'de açıklanıyor. Bu, VİOP normal seansı kapandıktan sonraya, akşam seansının içine denk geliyor. FOMC tepkisi **ertesi günün** uzlaşmadan uzlaşmaya getirisinde görünür.
- **CME GC günlük settlement** 13:29:00–13:30:00 ET VWAP. Bu kışın 18:29–18:30 UTC, yazın 17:29–17:30 UTC demek; VİOP uzlaşmasından 2 saat 15 dakika ile 3 saat 15 dakika sonra (CME müşteri wiki'si). VİOP ile COMEX "kapanışları" farklı anlarda. https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457088147/Gold
- **Şanghay Altın Borsası (SGE).** Gündüz seansı 09:00–15:30 Pekin (01:00–07:30 UTC), gece seansı 20:00–02:30 Pekin (12:00–18:30 UTC). Benchmark fiyatları 10:15 ve 14:15 Pekin (02:15 ve 06:15 UTC). SGE gündüz kapanışı ve PM benchmark, VİOP uzlaşmasından **önce** geliyor. https://en.sge.com.cn/eng_trading_ProductsIntroduce , https://www.kitco.com/price/fixes/shanghai-benchmark
- **CFTC COT** genellikle Cuma 15:30 ET'de yayımlanıyor ve önceki Salı'nın verisini içeriyor. Bu kışın 20:30 UTC demek. İlk kullanılabilir VİOP uzlaşması Pazartesi'ninki. CFTC 2026 sonuna kadar haftada iki yayına (Çarşamba ve Cuma) geçmeyi duyurdu. https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm , https://www.cftc.gov/PressRoom/PressReleases/9316-26

### 1.3 İşlem maliyeti (bir yön)
- **BIST borsa payı:** "Diğer Vadeli İşlem Sözleşmeleri" için işlem hacminin **0,3 bps'i (yüz binde 3 = %0,003)**. Altın/döviz sözleşmelerinde emir iptal ücreti 0 (Borsa İstanbul Ücretlendirme Tablosu). https://borsaistanbul.com/files/borsa-istanbul-ucretlendirme-tablosu.pdf
- **Takasbank:** Bir aracı kurum tarifesine göre diğer vadeli işlemlerde hacmin **yüz binde 1'i** alınıyor. Tarifenin tarihi net değil. https://www.denizyatirim.com/asset/CustomLinkPdf/1707831057.pdf
- **Aracı kurum komisyonu** en büyük kalem ve kişiye göre değişiyor. Arama özetine göre İş Bankası'nın 01.01.2024'ten geçerli hacim skalasında en düşük kademe (0–80.000) **on binde 10 (%0,10)**. Üstüne BSMV eklenir. https://www.isbank.com.tr/viop
- **Kaba hesap.** Varsayımlar: borsa payı 2 × 0,3 bps, takas 2 × 0,1 bps, yarım spread her yönde 0,5–1,5 bps.
  - Pazarlık edilmiş bir komisyonla (bir yön on binde 1–2) gidiş-dönüş toplamı yaklaşık **4–8 bps** ediyor.
  - Perakende varsayılan komisyonla (on binde 10, BSMV dahil) yaklaşık **22–25 bps**.
  - Spread ölçülmedi, bizim veriden ölçülmeli.
- **Ölçek.** Altının günlük standart sapması 2002–2008'de %1,23'tü (Elder ve diğ. 2012, Tablo 1). Yıllık Sharpe'ı 0,5 olan bir sinyal, yıllık %18 oynaklıkta günde ~3,6 bps, 5 günde ~18 bps getirir. **Her gün açılıp kapanan 1 günlük bir strateji perakende komisyonla açıkça zarar eder.** 5 günlük tutuş bile ancak düşük komisyonla anlamlı olur.

---

## 2. Beklentiyi kalibre eden genel kanıtlar

- **McLean ve Pontiff (2016, Journal of Finance):** 97 hisse senedi getiri öngörücüsünün getirisi örneklem dışında %26, yayımdan sonra %58 düşük. Yayımlanmış bir anomaliden beklentiyi kabaca yarıya indirin. https://counterpointfunds.com/wp-content/uploads/2017/07/PredictabilityMcleanPontiff.pdf
- **Park ve Irwin (2010, Journal of Futures Markets):** 17 ABD vadeli piyasası, 1985–2004. White Reality Check ve Hansen SPA ile veri madenciliği düzeltildikten sonra en iyi teknik kural yalnızca **17 piyasanın 2'sinde** anlamlı ekonomik kâr üretiyor. Önceki çalışma 1978–1984 kârlarının 1985–2003'te kaybolduğunu buldu. https://econpapers.repec.org/RePEc:wly:jfutmk:v:30:y:2010:i:7:p:633-659
- **Park ve Irwin (2007, Journal of Economic Surveys) taraması:** Teknik kurallar "en azından 1990'ların başına kadar" çeşitli piyasalarda kâr üretmiş. Veri madenciliği, kuralın sonradan seçilmesi, risk ve maliyet tahmini sorunları var. Görev metninde geçen "95 çalışmanın 56'sı pozitif" sayısını kaynakta doğrulayamadım. https://econpapers.repec.org/RePEc:bla:jecsur:v:21:y:2007:i:4:p:786-826
- **Marshall, Cahan ve Cahan (2008, Journal of Banking & Finance)** emtia vadelilerinde nicel zamanlama kurallarını test ediyor. Özetine erişemedim, bulgusunu yazmıyorum. https://econpapers.repec.org/RePEc:eee:jbfina:v:32:y:2008:i:9:p:1810-1819

---

## 3. Strateji aileleri

Her alt başlıkta sırayla mekanizma, kanıt, yayın sonrası durum, VİOP uygulanabilirliği, maliyet sonrası beklenti ve **kesin test kuralı** var. Test kurallarındaki notasyon:
- P_t: t günündeki VİOP F_XAUUSD uzlaşma fiyatı. En yakın vade kullanılır; vade geçişinde ölçek kopmasın diye ratio-adjust uygulanır (geri dönük oranlama).
- r_t = ln(P_t / P_{t-1}).
- İleri getiri: R_{t→t+h} = ln(P_{t+h} / P_t), h ∈ {1, 3, 5}.
- Sinyal t günü 15:15 UTC'den önce bilinen veriyle hesaplanır, pozisyon P_t'de açılır.
- Her kural için raporlanacaklar: koşullu ortalama, Newey-West t (h−1 gecikme), isabet oranı, işlem sayısı, gidiş-dönüş 8 bps ve 20 bps maliyetle net Sharpe.

### 3.1 Zaman serisi momentumu ve trend (hareketli ortalama kesişimi, Donchian kanalı, 52 hafta zirvesi)

**Mekanizma.** Yatırımcılar habere geç tepki verir, sonra aşırı tepki verir. CTA'lar ve riskten kaçınma akışları trendi besler.

**Kanıt.**
- **Moskowitz, Ooi ve Pedersen (2012, JFE):** 58 vadeli kontrat, 1985–2009. Getiriler **1–12 ay** sürüyor, daha uzun ufukta kısmen tersine dönüyor. Çeşitlendirilmiş portföyün Sharpe'ı 1'in üzerinde. Veri aylık, 1–5 günlük tutuşu doğrudan test etmiyor. https://fairmodel.econ.yale.edu/ec439/jpde.pdf
- **Szakmary, Shen ve Sharma (2010, JBF):** 28 emtia, 48 yıllık aylık veri. Çift hareketli ortalama ve kanal kurallarının tüm parametrelerinde 28 piyasanın en az 22'sinde maliyet sonrası pozitif getiri var. https://econpapers.repec.org/RePEc:eee:jbfina:v:34:y:2010:i:2:p:409-426
- **Han, Hu ve Yang (2016, JBF):** Emtia portföylerinde basit hareketli ortalama zamanlaması, maliyet, açığa satış kısıtı ve veri madenciliği kontrolünden sonra al-tut stratejisini yeniyor. Getiri resesyonda daha güçlü. https://econpapers.repec.org/RePEc:eee:jbfina:v:70:y:2016:i:c:p:214-234
- **Baltas ve Kosowski (2012, EFMA):** 71 kontrat, 1974–2012, aylık, haftalık ve günlük frekans. Sharpe 1,20'nin üzerinde (çok piyasalı portföy). https://efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2012-Barcelona/papers/BK_MOMF_Full.pdf
- **Altına özgü günlük kanıt (zayıf):**
  - CXO Advisory'nin 1973–2016 spot altın analizi: 200 günlük ortalamaya göre konum, rejimi tüm örneklemde ayırıyor ama bu "tamamen ilk dönem verisinden" geliyor. **1990 ve 2000 sonrasında 200 günlük ortalama ortalama getiri rejimlerini ayırmıyor.** https://www.cxoadvisory.com/?p=15805
  - Batten, Lucey, McGroarty, Peat ve Urquhart (2018, JIFMIM): Gün içi hareketli ortalama kurallarının altında "bir miktar" öngörü gücü var, gümüşte yok. Çalışma makalesi versiyonu kayda değer kâr olmadığını söylüyor. https://econpapers.repec.org/RePEc:eee:intfin:v:52:y:2018:i:c:p:102-113
  - Urquhart (2017, European Journal of Finance): 1987–2014 günlük veri. Değerli metallerde öngörülebilirlik zamanla açılıp kapanıyor (uyarlanabilir piyasa hipotezi). https://centaur.reading.ac.uk/79177
- **52 hafta zirvesi:** Emtia çalışmalarında anchoring kanıtı var. Bianchi, Fan ve Forster-Wright'ın 2018 çalışma makalesi ve Laubsch, Smales ve Vo (2025) zirvede ticaretin yavaşladığını, ticari katılımcıların karşıt davrandığını buluyor. **Altına özgü sonuç bulunamadı.** https://econpapers.repec.org/RePEc:taf:hbhfxx:v:26:y:2025:i:3:p:391-405
- **Uyarı örneği:** Singha ve diğ. (arXiv 2511.08571, Kasım 2025, hakemsiz) 2015–2025 altın vadelisinde örneklem dışı Sharpe 2,88, maksimum düşüş %0,52, yıllık %43 getiri bildiriyor. %15 oynaklık hedefiyle %0,52 düşüş inanılması güç. Bunu kanıt olarak almayın. https://arxiv.org/abs/2511.08571

**Yayın sonrası.** Çok piyasalı trend takibi 2010'larda zayıfladı, sonra güçlendi. Altına özgü kısa pencereli sinyalin 1990 sonrası işlediğine dair hakemli kanıt bulunamadı.

**VİOP uygulanabilirliği.** Uzlaşma serisiyle doğrudan hesaplanabilir. Uzun bakış pencereli sinyaller (60–250 gün) yavaş değişir, devir düşük olur. Ama kullanıcı 1–5 günde çıkmaya zorlanırsa her çıkışta maliyet ödenir. Doğru kurgu "sinyal aynıysa pozisyonu yenile, maliyeti yalnızca sinyal döndüğünde öde" şeklinde.

**Maliyet sonrası beklenti.** Pozitif ama küçük, çok piyasalı portföy Sharpe'ının çok altında.

**Test kuralları.**
- **TSMOM:** s_t = sign(ln(P_t / P_{t-k})), k ∈ {5, 10, 20, 60, 120, 250}. Pozisyon s_t, çıkış t+h'de. Ayrıca sürekli versiyonu: s_t / σ_{20,t}.
- **MA kesişimi:** (hızlı, yavaş) ∈ {(5,20), (10,50), (20,100), (50,200)}. P'nin basit ortalamaları üzerinden; hızlı > yavaş ise uzun, değilse kısa ya da nakit.
- **Donchian:** P_t > max(P_{t-N..t-1}) ise uzun, P_t < min(...) ise kısa, N ∈ {20, 55}. Ters kırılım veya h gün sonunda çıkış.
- **52 hafta:** x_t = P_t / max(P_{t-250..t}). x_t ≥ 0,98 ise uzun, h gün tut. Karşılaştırma: x_t ≤ 0,85.
- Tüm parametreler için çoklu test düzeltmesi yapılır (White RC / Hansen SPA). Eğitim 2012–2020, test 2021–2026.

### 3.2 Kısa vadeli dönüş (1–5 gün getirisinin tersi, RSI(2)/Connors, Bollinger)

**Mekanizma.** Likidite sağlayıcılar geçici fiyat baskısının tersine pozisyon alır.

**Kanıt.**
- **Wang ve Yu (2004, JBF):** 24 ABD vadeli piyasasında, kesitsel karşıt portföyle **haftalık getiri dönüşleri** güçlü. Kâr, gecikmeli hacim değişimiyle ilişkili. Tek tek altın sonucu özetlerde yok. https://econpapers.repec.org/RePEc:eee:jbfina:v:28:y:2004:i:6:p:1337-1361
- **Bianchi, Drew ve Fan (2015, JBF):** Emtiada saf dönüş stratejileri "tutarlı biçimde kârsız" (Zhang ve Urquhart 2020'nin aktarımı). Momentum ve dönüşü birleştiren çift sıralama yılda %20,24 getiriyor (aylık, kesitsel). https://econpapers.repec.org/RePEc:eee:jbfina:v:59:y:2015:i:c:p:423-444
- **Spekülatör akışı:** Bir Lingnan seminer özetine göre emtiada kısa vadeli dönüşü geçmiş fiyat değil, spekülatörlerin pozisyon akışı (COT) açıklıyor. Akış bileşeni ertesi haftayı negatif, artık bileşen pozitif öngörüyor. Makalenin tamamına erişemedim. https://lingnan.sysu.edu.cn/en/node/3656
- **Haber aşırı tepkisi:** Smales (2015, JIFMIM) altın vadelisinde katılımcıların planlanmamış haberlere önce aşırı tepki verip sonra geri aldığını buluyor. Ufuk özette yok. https://econpapers.repec.org/RePEc:eee:intfin:v:34:y:2015:i:c:p:161-172
- **RSI(2) / Connors:** Kurallar Connors ve Alvarez (2008) kaynaklı ve testler ağırlıkla hisse ETF'lerinde. **Altın için hakemli ya da güvenilir pratisyen testi bulunamadı.** GLD üzerine dolaşan "işlem başına %1,5" gibi iddialar kural tanımsız ve doğrulanamadı.
- **Bollinger:** Altına özgü kanıt bulunamadı.

**VİOP.** Uygulanabilir, fakat 1 günlük dönüş stratejisinin devri çok yüksek.

**Maliyet sonrası.** Kanıt zayıf, devir yüksek. Beklenti sıfır veya negatif.

**Test kuralları.**
- **R1:** pozisyon = −sign(r_t), h = 1, 3, 5.
- **R2:** pozisyon = −sign(ln(P_t / P_{t-5})).
- **RSI(2):** Wilder RSI(2) < 10 ve P_t > SMA200 ise uzun. Çıkış P > SMA5 veya 5 gün dolunca. Simetrik kısa: RSI(2) > 90 ve P < SMA200.
- **Bollinger(20, 2):** P_t alt bandın altında kapatırsa uzun, h gün tut.
- **Çakışma kontrolü:** R1'i TSMOM sinyali ile koşullandır (trend yönünde geri çekilme alımı).

### 3.3 Büyük hareket sonrası (>2σ günler)

**Kanıt.**
- **Caporale ve Plastun (CESifo WP 8445, 2020; FMPM 2021).** Veri 01.01.2009–31.03.2020, MetaQuotes, GMT+3, açılıştan kapanışa getiri. Eşik ortalama ± 2σ.
  - Altında anormal günün **ertesi günü karşıt etki** var, petrolde momentum.
  - Ertesi gün karşıt strateji, pozitif şok sonrası: 59 işlem, %59 isabet, işlem başına %0,07, t = 1,36. Negatif şok sonrası: 74 işlem, %58,1 isabet, işlem başına %0,15, t = 0,73. **İkisi de rastgeleden istatistiksel olarak farklı değil.** Maliyet dahil değil.
  - Aynı gün momentum stratejisi (86% / 72% isabet) günün "anormal" olacağının gün içinde anlaşılmasına dayanıyor ve tam örneklem eşiği kullanıyor. **İleriye bakma riski yüksek.**
  - https://www.ifo.de/DocDL/cesifo1_wp8445.pdf
- **Baur ve Lucey (2010, Financial Review) / IIIS DP 198:** Aşırı bir hisse şokundan sonra altın **yalnızca 15 iş günü** güvenli liman. https://econpapers.repec.org/RePEc:iis:dispap:iiisdp198

**VİOP.** Günlük fiyat limiti ±%10 (bakır sözleşme unsurlarında yazılı; ons altın için aynı varsayılıyor). Limit, 2σ hareketlerini kısıtlamaz.

**Maliyet sonrası.** Sıfıra yakın.

**Test kuralları.**
- z_t = r_t / σ_{20,t-1}.
- |z_t| > 2 olan günlerde R_{t→t+h} koşullu ortalaması, z > 2 ve z < −2 ayrı.
- Ayrıca 3σ eşiği ve "şok gününün ABD verisi/FOMC günü olup olmadığı" alt kırılımı.

### 3.4 Oynaklık kırılımı, oynaklık rejimi, GVZ, oynaklık hedefleme

**Kanıt.**
- **Harvey, Hoyle, Korgaonkar, Rattray, Sargaison ve Van Hemert (2018, JPM):** 60'tan fazla varlık, 1926–2017 günlük veri. Oynaklık hedefleme Sharpe'ı **yalnızca riskli varlıklarda (hisse, kredi)** iyileştiriyor. Emtia dahil diğerlerinde iyileştirme yok, ama uç kayıpları tüm sınıflarda azaltıyor. https://quantpedia.com/the-impact-of-volatility-targeting-on-equities-bonds-commodities-and-currencies
- **Ters asimetrik oynaklık:** Altında pozitif şoklar oynaklığı daha çok artırıyor (Todorova 2017, Economics Letters, 13,5 yıllık gün içi veri; Baur 2012, JAI). Yani altında oynaklık sıçraması tek başına "düşüş" sinyali sayılmamalı. https://ideas.repec.org/a/eee/ecolet/v150y2017icp138-141.html
- **GVZ:** GVZ'nin altın getirisini öngördüğüne dair **hakemli çalışma bulunamadı.** Bir Comillas çalışması GVZ'nin ana belirleyicisinin VIX olduğunu buluyor. QuantSeeker'ın Ocak 2026 yazısı ücretli, sonucu görülemedi. https://repositorio.comillas.edu/xmlui/handle/11531/95045?show=full
- **Oynaklık risk primi:** Prokopczuk, Symeonidis ve Wese Simen (2017, JBF): 21 emtianın neredeyse tamamında varyans risk primi anlamlı negatif. Eşit ağırlıklı kısa varyans swap portföyünün yıllık Sharpe'ı ~0,40. Bu, opsiyon satıcılarının para kazanma kanalı. VİOP vadelisiyle uygulanamaz. https://econpapers.repec.org/RePEc:eee:jbfina:v:81:y:2017:i:c:p:136-149
- **Oynaklık kırılımı (ATR, açılış aralığı kırılımı):** Altına özgü yayımlanmış test bulunamadı.

**VİOP ve beklenti.** Bunu yön kenarı olarak değil, **pozisyon boyutlandırma** aracı olarak kullanın.

**Test kuralları.**
- **Rejim ayrıştırması:** 20 günlük gerçekleşen oynaklığın 1 yıllık yüzdeliğine göre üç rejim (<%33, orta, >%67). TSMOM ve dönüş kurallarının her rejimdeki getirisi.
- **Oynaklık hedefleme:** Pozisyon büyüklüğü 0,15 / σ_{20,t}·√252, en fazla 2 kat. Sharpe ve maksimum düşüş hedefsiz versiyonla karşılaştırılır.
- **GVZ:** ΔGVZ_t (VİOP kapanışında bilinen son değer, yani bir önceki ABD kapanışı) en üst %10'da ise R_{t→t+h}.
- **Kırılım:** |r_t| > 1,5·ATR14 olan günden sonra kırılım yönünde h gün tutuş. Bu kural 3.3 ile çakıştığı için birlikte raporlanmalı.

### 3.5 Takvim etkileri

**Haftanın günü.**
- Ball, Torous ve Tschoegl (1982, JFM): 1975–1979 London fixing. Ortalama getiriler güne göre ve gece/gündüz ayrımına göre değişiyor, gece değişimleri daha az oynak. https://econpapers.repec.org/RePEc:wly:jfutmk:v:2:y:1982:i:2:p:175-182
- Lucey ve Tully (2006, Applied Financial Economics): COMEX 1982–2002. Ortalamada günlük mevsimsellik kanıtı zayıf, varyansta güçlü. Altın ve gümüşte **negatif Pazartesi etkisi** var. https://www.tcd.ie/triss/assets/PDFs/iiis/iiisdp57.pdf
- Blose ve Gondhalekar (2013, Accounting & Finance), "Weekend gold returns in bull and bear markets": özete erişilemedi.
- LME 1995–2015: haftanın günü etkisi yok, altında hafta sonu etkisi var. https://econjournals.sgh.waw.pl/JMFS/article/view/740
- Incrementum (In Gold We Trust; sektör yayını, hakemsiz): GLD 11/2004–12/2023 ortalama günlük getiri Pazartesi −%0,01 (tek negatif gün), Cuma +%0,11. https://ingoldwetrust.report/nuggets/calendar-anomalies-and-the-gold-market/?lang=en
- **BIST VİOP altın vadelisi:** Karataş Elçiçek (2023, BERJ), 02.09.2013–30.11.2022, ARMA-GARCH. Perşembe hariç günlerde pozitif getiri var. Sözleşme tipi özette belirtilmemiş. TL bazlı (gram) sözleşmeyse kur kaymasını içerir. https://econpapers.repec.org/RePEc:ris:buecrj:0643

**Ay dönümü.** Incrementum'a göre GLD, GDX ve GDXJ'de ayın ilk günü getirisi belirgin yüksek, son gün ve 2. gün de ortalamanın üstünde. Pencere tanımına çok duyarlı. **Hakemli altın çalışması bulunamadı.**

**Tatil öncesi.** Fabozzi, Ma ve Briley (1994, JF): genel vadelilerde tatil öncesi getiri yüksek. Güney Afrika altın vadelisinde anlamlı tatil etkisi yok (Smit ve Smit). https://econpapers.repec.org/RePEc:bla:jfinan:v:49:y:1994:i:1:p:307-24 , https://sajbm.org/index.php/sajbm/article/view/777

**Ay mevsimselliği.**
- Baur (2013, RIBAF), 1980–2010: **Eylül ve Kasım** pozitif ve anlamlı getirisi olan tek aylar. Açıklama olarak Hindistan düğün sezonu, Halloween öncesi hedge ve kısa günler öneriliyor. CXO'nun 1981–2010 özetine göre Eylül ortalaması %2,2, Kasım %1,8. https://econpapers.repec.org/RePEc:eee:riibaf:v:27:y:2013:i:1:p:1-11 , https://cxoadvisory.com/calendar-effects/gold-seasonality-drivers
- **Yayın sonrası:** Potrykus ve Augustynowicz (2024, IJME) replikasyonu: **sonbahar etkisi tersine dönmüş, yerini kış etkisi almış.** https://mostwiedzy.pl/pl/publication/the-autumn-effect-in-the-gold-market-does-it-contradict-the-adaptive-market-hypothesis,162800-1
- WGC (Artigas, 20.12.2023): Ocak ortalaması 1971'den beri %1,79 (uzun dönem aylık ortalama %0,63). Zamanın yaklaşık %60'ında, 2000'den beri yaklaşık %70'inde pozitif, %90 güvenle. Ocak 2021 ve 2022 negatifti. https://www.gold.org/goldhub/gold-focus/2023/12/you-asked-we-answered-is-there-a-january-effect-for-gold
- Gulseven (arXiv 2003.11027): Ocak en yüksek, Temmuz anlamlı negatif. https://arxiv.org/abs/2003.11027

**Festivaller ve dini günler.**
- **Hindistan (Diwali/Dhanteras, Akshaya Tritiya):** Akademik olay çalışması bulunamadı, yalnızca basın yorumu var.
- **Çin Yeni Yılı:** WGC, Ocak gücünü Ay Yeni Yılı öncesi stok yenilemeye "olası katkı" olarak bağlıyor, kanıtlamıyor. CME'nin Şanghay primi mevsimselliği yazısına erişilemedi.
- **Ramazan:** Ozkan (2019, JIABR), BIST altın endeksi 04.03.2003–30.09.2016: Ramazan etkisi var, ama yönü özette yok. https://econpapers.repec.org/RePEc:eme:jiabrp:jiabr-04-2017-0054
- **Kurban Bayramı:** Altına özgü çalışma bulunamadı. Not: Türkiye tatillerinde VİOP kapalıyken küresel altın işlem görür. Tatil dönüşü getirisi çok günlük bir sıçrama içerir.

**VİOP.** VİOP Pazartesi getirisi (Cuma 15:15 UTC → Pazartesi 15:15 UTC) Cuma ABD öğleden sonrasını, hafta sonunu ve Pazartesi Asya-Avrupa'yı kapsar. Bu, COMEX'in "Pazartesi"siyle aynı şey değil.

**Test kuralları.**
- r_t'yi gün kuklalarına regres et (HAC).
- **Ay dönümü:** son 1 iş günü ile ilk 3 iş günü uzun, kalan günler nakit.
- **Ay kuklaları:** Ocak, Eylül, Kasım; 2012–2019 ile 2020–2026 ayrı.
- **ABD tatil öncesi:** NYSE/COMEX tatilinden önceki VİOP günü.
- **TR tatil sonrası:** tatil sonrası ilk VİOP günü getirisi, tatil gün sayısına bölünerek.
- **Çin Yeni Yılı:** CNY'den önceki 10 iş günü toplam getirisi, aynı uzunlukta rastgele pencerelere karşı.
- **Hindistan:** Dhanteras ve Akshaya Tritiya'dan önceki 5 gün ile sonraki 5 gün.
- **Hicri:** Ramazan ayı, Kurban öncesi 5 gün.
- Takvim kurallarının çoğu yılda 12–30 gözlem verir. Bonferroni zorunlu.

### 3.6 Seans ve gün içi ayrışım

**Kanıt.**
- **Blose ve Gondhalekar (2014, AEL):** COMEX ön ay kontratı, 1985–2012. **Gece getirileri anlamlı pozitif, gündüz getirileri anlamlı negatif.** GLD'de de gece getirisi gündüzden yüksek. "Asimetri belirgin şekilde zayıfladı ama hâlâ var." https://econpapers.repec.org/RePEc:taf:apeclt:v:21:y:2014:i:18:p:1269-1272
- Blose, Gondhalekar ve Kort (2018, JEF): Aynı desen London fix, madenci hisseleri, kapalı uçlu fonlar ve ETF'lerde de var. https://ideas.repec.org/a/spr/jecfin/v42y2018i3d10.1007_s12197-017-9403-0.html
- **Veri yanılsaması uyarısı:** Quantpedia (Dujava, 14.02.2025), GDX. OHLC açılış fiyatıyla gece sürüklenmesi yılda ~%30, gün içi ~−%25 görünüyor. Gerçekçi 09:31 dolumuyla gece getirisi yılda %8,58'e iniyor. Açılış fiyatı ilk işlemden geliyor ve gerçekçi bir dolum değil. https://quantpedia.com/dangers-of-relying-on-ohlc-prices-the-case-of-overnight-drift-in-gdx-etf/
- **"Altın Asya'da yükselir, New York'ta düşer":** Hakemli bir çalışma bulunamadı. 2026 tarihli bir FXStreet/Money Metals köşe yazısı 2026'nın ilk yarısı için Asya saatlerinde +%12,9, Kuzey Amerika saatlerinde −%15, Avrupa'da −%1,3 iddia ediyor. Bu bir görüş yazısı, verisi doğrulanamadı (sayfa 403 verdi). Bloomberg (23.04.2024) rekor rallinin Çinli talebinde, ABD verilerinin geldiği gece seansında yoğunlaşan Şanghay işlemlerinde kökü olabileceğini yazdı. https://www.bloomberg.com/news/articles/2024-04-23/gold-s-record-setting-rally-may-have-its-roots-in-chinese-frenzy
- **Fiyat keşfi:** Hauptfleisch, Putniņš ve Lucey (2016, JFM), 17 yıllık gün içi veri: New York vadelisinin hacmi Londra spotunun onda birinden az olmasına rağmen fiyat keşfinde ortalamada daha büyük rol oynuyor. https://econpapers.repec.org/RePEc:wly:jfutmk:v:36:y:2016:i:6:p:564-586
- **LBMA fix:** Caminschi ve Heaney (2014, JFM) eski telefonlu fiksingi (2015 öncesi) inceledi. 15:01'de hacim önceki 20 dakikanın %47,8 üzerinde. Vadelinin yönü fiks sonucuyla 15:01'den itibaren %69,9, 5 dakika içinde %80 oranında örtüşüyor; bu bilgi sızıntısına işaret ediyor. Mart 2015 sonrası IBA elektronik müzayedesi için kalıcı bir sürüklenme kanıtı bulunamadı. https://econpapers.repec.org/RePEc:wly:jfutmk:v:34:y:2014:i:11:p:1003-1039

**VİOP uygulanabilirliği: düşük.** Kapanıştan kapanışa bir pozisyon gece ve gündüz bileşenlerini birlikte taşır. VİOP uzlaşması (15:05–15:15 UTC) COMEX gündüz seansının ortasına düşer. Seans etkisini VİOP'ta ancak akşam seansı (16:00–20:00 UTC) ile oynamak mümkün, bu da bu çalışmanın kapsamı dışında. Seans getirileri yine de **özellik** olarak kullanılabilir.

**Test kuralları.**
- **Ayrıştırma:** XAUUSD spot veya GC saatlik verisiyle her VİOP günü getirisini üçe böl: Asya (15:15 UTC'den 07:00 UTC'ye), Londra (07:00–12:30), NY sabahı (12:30–15:15).
- **Kalıcılık:** Her bileşenin işaretinin R_{t→t+h}'yi öngörüp öngörmediğini test et. Örnek: dünkü Asya bileşeni pozitifse ve NY bileşeni negatifse sonraki getiri ne olur?
- **Kış/yaz kontrolü:** Kış ve yaz saatinde LBMA PM ile VİOP uzlaşması arasındaki fark (5 dakika ile 65 dakika) etkileri değiştiriyor mu?

### 3.7 Olay odaklı (FOMC, CPI, NFP, PCE, başvurular, Powell, jeopolitik)

**Kanıt.**
- **FOMC öncesi sürüklenme:** Lucca ve Moench (2015, JF) bunu hisse senetlerinde buldu. Hazine tahvilleri, diğer sabit getirili araçlar ve **döviz kurlarında bulmadılar**. **Altın için sonuç bulunamadı.** Kurov, Wolfe ve Gilbert hisse senedi sürüklenmesinin azaldığını gösteriyor. https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf , https://www.skidmore.edu/economics/documents/KurovWolfeGilbert-TheDisappearingPre-FOMC-Announce-Drift-200914.pdf
- **FOMC tepkisi:** Awartani, Hussain ve Virk (2024, IRFA): Altın getirisi ve oynaklığı FOMC'den 5 dakika sonra **gevşek yönlü sürprizlere daha duyarlı**. Ayarlama 5 dakikadan uzun sürüyor. https://pure.kfupm.edu.sa/en/publications/how-do-the-gold-intra-day-returns-and-volatility-react-to-monetar/
- Pratisyen (Sunshine Profits/FXEmpire, 2017'den beri 33–36 toplantı): toplantı öncesi düşüş, sonra 10 günde ortalama +%0,5–0,8. İstatistiksel test yok ve sonuçlar Mart 2020'ye bağımlı.
- WGC: Son dört artırım döngüsünde (1994, 1999, 2004, 2015) altın ilk artırımdan önceki 6 ayda ~−%6,8, sonraki 6 ayda ~+%11,3. Ufuk aylık, 1–5 günle ilgisi yok. https://www.gold.org/goldhub/research/outlook-2022
- **Makro veriler:** Elder, Miao ve Ramchander (2012, JBF), 2002–2008 tick verisi.
  - 08:30 açıklamaları en etkili. Tarım dışı istihdam (NFP), altında 5 dakikalık getirinin %35'ini açıklıyor (düzeltilmiş R²).
  - Dayanıklı mallarda 1σ sürpriz altını 5 dakikada yaklaşık %0,06 düşürüyor. Ekonomik iyileşme sürprizleri altını düşürüyor.
  - **Etki çok çabuk sönüyor**, çok günlük sürüklenme kanıtı yok.
  - https://mountainscholar.org/handle/10217/206884
- **Haber duyarlılığı:** Smales (2014, JBF), 2003–2012 Thomson Reuters News Analytics: negatif haberin eşzamanlı etkisi daha büyük. https://econpapers.repec.org/RePEc:eee:jbfina:v:49:y:2014:i:c:p:275-286
- **Jeopolitik:** Baur ve Smales (2020, JBF): Değerli metaller jeopolitik riske, özellikle **tehditlere** (eylemlere değil) karşı hedge. Uç sıçramalarda yalnızca altın ve gümüş güvenli liman. GPR'ye dayalı saf uzun stratejiler pozitif getiriyor ama nominal olarak S&P 500'ün altında kalıyor. https://econpapers.repec.org/RePEc:eee:jbfina:v:117:y:2020:i:c:s037842662030090x
- **Powell konuşmaları, PCE, işsizlik başvuruları:** Altına özgü çok günlük çalışma bulunamadı.

**VİOP.**
- ABD 08:30 verileri **aynı günün** VİOP getirisine düşer. Veri gününden önceki VİOP kapanışında pozisyon almak verinin riskini taşımak demektir.
- FOMC **ertesi günün** getirisine düşer. "FOMC günü VİOP kapanışında al, ertesi gün kapanışta sat" kuralı kararı ve ilk tepkiyi taşır.
- Akşam seansı FOMC'yi canlı yakalar (kışın 19:00 UTC, akşam seansı 20:00 UTC'de bitiyor).

**Maliyet sonrası.** Yön kenarına dair kanıt yok. Bu günler büyük ölçüde oynaklık olayı.

**Test kuralları.**
- **FOMC (t = FOMC günü):** R_{t-1→t} (öncesi), R_{t→t+1} (karar ve tepki), R_{t+1→t+5} (sonrası). Hepsi FOMC dışı günlerle karşılaştırılır. Ayrıca R_{t-5→t-1} sürüklenmesi.
- **CPI, NFP, PCE, işsizlik başvuruları (t = veri günü):** R_{t-1→t} mutlak getirisi FOMC dışı günlere göre ve işaret ortalaması. Sürpriz verisi varsa sign(sürpriz)·R_{t→t+h} ile çok günlük sürüklenme testi.
- **Jeopolitik:** Caldara–Iacoviello GPR günlük endeksinin 30 günlük z-skoru 2'yi aşarsa R_{t→t+h}.

### 3.8 COMEX opsiyon vadesi, vadeli roll, endeks roll'ü, ay sonu ve çeyrek sonu

**Kanıt.**
- **COMEX altın opsiyonları (OG)** kontrat ayından önceki ayın sonundan 4 iş günü önce sona eriyor (CME gold fact card; Micro Gold için rulebook aynı mantığı açıkça yazıyor). https://www.cmegroup.com/content/dam/cmegroup/market-regulation/files/gold-futures-and-options-fact-card.pdf , https://cmegroup.com/markets/metals/precious/e-micro-gold.contractSpecs.options.html
- **Pinning (fiyatın kullanım fiyatına yapışması):** Hisse senetlerinde kanıtı var. **Altın için hakemli çalışma bulunamadı.** Aralık 2024 ve Mart 2025 vadelerindeki sert düşüşler bir bülten tarafından anekdot olarak aktarılıyor.
- **Endeks roll'ü:** Mou'nun Goldman roll ön-alımı stratejisi 2000 – Mart 2010'da Sharpe'ı 4,39'a kadar çıkarıyor. Endeks yatırımcıları yılda ortalama %3,6 getiriden vazgeçmiş. Altının örneklemde olup olmadığını doğrulayamadım. https://papers.ssrn.com/abstract=1716841
- **BCOM roll'ü** genellikle ayın 6–10. iş günü. Ocak 2026 yıllık ağırlık sıfırlamasının 5 günlük pencerede 6 milyar doları aşan altın vadeli satışı tetikleyeceği haberi çıktı (SMM, Ocak 2026). https://www.bloomberg.com/professional/products/indices/quote/BCOM:IND , https://news.metal.com/newscontent/103713376
- **Ay sonu ve çeyrek sonu yeniden dengelemesi:** Altına özgü çalışma bulunamadı.

**VİOP.**
- VİOP'un vade sonu uzlaşması LBMA PM. VİOP ile COMEX vade takvimleri farklı: COMEX GC ilk bildirim günü kontrat ayından önceki ayın son iş günü, VİOP'ta son işlem günü vade ayının sonu (doğrulanmalı).
- VİOP vade geçişi haftasında likidite yakın vadeden bir sonrakine kayar. Roll günlerinde spread ve gürültü artabilir.

**Test kuralları.**
- **Opsiyon vadesi (t_OE = OG vade günü):** R_{t_OE-5→t_OE} ve R_{t_OE→t_OE+3}.
- **Roll:** GC ilk bildirim gününden önceki 5 iş günü; BCOM 6–10. iş günleri; Ocak BCOM/GSCI yeniden ağırlıklandırma penceresi.
- **Ay sonu:** son 2 iş günü ile ilk 2 iş günü (3.5'teki ay dönümüyle birlikte).
- **VİOP kendi vadesi:** vade bitimine 5 gün kala ve son gün.

### 3.9 Pozisyonlanma ve akış (CFTC COT, ETF akışları, Google Trends, Şanghay primi)

**COT.**
- Altında COT uçlarının karşıt bir öngörücü olduğuna dair **hakemli, örneklem dışı ve maliyet sonrası kanıt bulunamadı.**
- Bir Aalto tezi, uç COT pozisyonlamasına dayalı karşıt stratejinin döviz ve enerjide istatistiksel olarak anlamsız, marjinal pozitif getiri verdiğini buluyor.
- Bir PolyU tezi değerli metallerde yatırımcıların trendi takip ettiğini, pozisyonların fiyatla eşzamanlı hareket ettiğini ve nedenselliğin fiyattan pozisyona doğru olabileceğini buluyor.
- Basu, Oomen ve Stremme (2008)'in zamanlama kazançları kısa bir örneklemden geliyor ve sürtünmeyi yok sayıyor.
- https://aaltodoc.aalto.fi/items/b84b07d6-3bd2-4040-bbcf-052b938b1f74 , https://theses.lib.polyu.edu.hk/handle/200/7971

**ETF akışları.**
- Deutsche Bank'ın Granger testi (Tickmill üzerinden aktarılıyor) **fiyatın akışa öncülük ettiğini** buluyor.
- Aalto tezi (2007–2014): yalnızca kriz sonrasında zayıf nedensellik var, tam örneklemde yok.
- https://www.tickmill.com/blog/institutional-insights-deutsche-bank-who-drives-gold-prices , https://epub.lib.aalto.fi/en/ethesis/id/14319

**Google Trends.** Baur ve Dimpfl (2016, Resources Policy): Aramalar oynaklıkla ve özellikle negatif fiyat hareketleriyle artıyor. Yani ilgi fiyatı takip ediyor. Öngörü gücü bulan çalışmalar küçük ve zayıf. https://econpapers.repec.org/RePEc:eee:jrpoli:v:50:y:2016:i:c:p:306-311

**Şanghay primi.** Meader (Metals Focus, LBMA Alchemist sayı 83), Ocak 2005 – Ağustos 2016:
- Boğa döneminde (2005 – Eylül 2011) en az %1 prim sonrası bir ayda LBMA AM ortalama +33 $, en az %0,2 iskonto sonrası +2 $.
- Düşüş döneminde (Eylül 2011 – 2015) prim sonrası 10 günde −1 $, iskonto sonrası −14 $.
- Gözlem sayısı verilmemiş. Yazar etkiyi "mütevazı" diyor.
- https://www.lbma.org.uk/alchemist/issue-83/links-between-the-chinese-and-international-gold-prices

**Test kuralları.**
- **COT:** Yönetilen para (managed money) net pozisyonu / açık pozisyon oranının 156 haftalık z-skoru. z > +2 ise kısa, z < −2 ise uzun, giriş Pazartesi VİOP uzlaşmasında, h = 5.
- **ETF akışı:** GLD tonaj değişimi (t−1 ABD gün sonu) en üst %10'da ise R_{t→t+h}, ve tersi. Ayrıca R_{t-5→t}'nin akışı öngörüp öngörmediği (nedensellik yönü).
- **Google Trends:** Haftalık "gold" araması 52 haftalık ortalamanın 2σ üstündeyse sonraki 5 gün.
- **Şanghay primi:** prim_t = SGE Au99.99 (PM benchmark, 06:15 UTC) ÷ (USDCNY × 31,1035) ÷ LBMA AM − 1. prim > %1 veya iskonto < −%0,2 ise R_{t→t+h}.

### 3.10 Göreli değer ve model artığı (altın/gümüş oranı, madenciler, reel faiz/dolar, carry/baz)

**Altın/gümüş oranı.** Örneklem dışı test içeren hakemli bir çift işlem çalışması **bulunamadı**. Kaynaklar pratisyen yazıları ve aracı kurum pazarlaması. VİOP'ta F_XAGUSD (10 ons) ile iki bacaklı kurulabilir.

**Madenciler.**
- Lucey ve O'Connor ("Are Gold Bugs Coherent?", AEL 2017), 1998–2015 günlük veri. **Altın vadelisi madenci hisselerine en az bir hafta öncülük ediyor.** Çok kısa aralıklarda madenci getirilerini altın dışı faktörler belirliyor.
- "Madenciler altını önden gösterir" iddiası desteklenmiyor.
- https://research.ucc.ie/en/publications/are-gold-bugs-coherent/ , https://www.cxoadvisory.com/gold/gold-futures-vs-gold-miner-stocks/

**Reel faiz/dolar artığı.**
- Erb ve Harvey (2013, FAJ, "The Golden Dilemma"): 1997'den beri 10 yıllık TIPS reel getirisi ile reel altın fiyatı arasındaki korelasyon −0,82 (ikincil özet; başka bir özette −0,74). Yazarlar bunu mekanik bir neden-sonuç olarak görmüyor. https://www.nber.org/papers/w18706
- 2022'den beri altın, TIPS modelinin öngördüğünün çok üzerinde seyrediyor (Goldmoney). https://www.goldmoney.com/research/have-central-banks-lost-control-over-the-gold-price
- **Model artığının 1–5 günde ortalamaya döndüğüne dair hakemli kanıt bulunamadı.**

**Carry ve baz.**
- Koijen, Moskowitz, Pedersen ve Vrugt (2018, JFE): carry, emtia dahil varlık sınıflarında bağımsız bir getiri öngörücüsü. Altında carry yaklaşık olarak −(faiz − kiralama oranı), yani küçük ve istikrarlı. https://econpapers.repec.org/RePEc:eee:jfinec:v:127:y:2018:i:2:p:197-225
- Barone-Adesi, Geman ve Theal: Altının convenience yield'i en iyi kiralama oranıyla yakalanıyor. Spekülasyon vadeli getirileriyle ilişkili. https://econpapers.repec.org/RePEc:chf:rpseri:rp0907
- 1–5 günlük bir sinyal için kanıt bulunamadı.

**Test kuralları.**
- **Altın/gümüş:** GSR = P_XAU / P_XAG, 60 günlük z-skoru. |z| > 2 ise oranın tersine (altın kısa + gümüş uzun ya da tersi), dolar nötr, h = 5.
- **Madenciler:** e_t = r_GDX,t − β·r_XAU,t (β 60 günlük). Kümülatif 5 günlük e en uç %10'da ise R_XAU,t→t+h.
- **Artık:** r_XAU,t = a + b·ΔDXY_t + c·ΔTIPS10_t + u_t (250 günlük kayan pencere). Σu_{t-4..t} > 2σ ise altında kısa.
- **Baz:** baz_t = P_VİOP,t / spot_t − 1 − teorik carry. z > 2 ise R_{t→t+h}. Bu bir lead-lag/arbitraj testi.

### 3.11 Risk kapalı günler (VIX sıçraması)

**Kanıt.**
- Baur ve McDermott (2010, JBF), 1979–2009: Altın ABD ve büyük Avrupa borsaları için hem hedge hem güvenli liman. Avustralya, Kanada, Japonya ve BRIC için değil. Etki çok uç koşullarda günlük ve haftalık getiride en güçlü. **Aşırı oynaklıkta altın hisselerle birlikte hareket edebiliyor.** https://econpapers.repec.org/RePEc:eee:jbfina:v:34:y:2010:i:8:p:1886-1898
- Baur ve Lucey: güvenli liman özelliği 15 iş günü sürüyor (3.3).

**Test kuralları.**
- ΔVIX_t (bir önceki ABD kapanışı) > +%20 veya VIX > 30 ise R_{t→t+h}.
- S&P 500 −%3 günlerinden sonra R_{t→t+h}; bu sinyal VİOP kapanışında bilinen son ABD kapanışından alınır.

### 3.12 Popüler perakende stratejileri

- **RSI, MACD:** Altın vadelisinde veri madenciliği düzeltmeli (White RC / SPA) yapılmış bir RSI veya MACD testi **bulunamadı.** Genel vadeli piyasalarda Park ve Irwin (2010) sonucu geçerli: 17 piyasanın 2'si. **Etiket: kanıt zayıf.**
- **Fibonacci:** City University çalışmasına (FT, 02.10.2006) göre tepe-dip oranları Fibonacci oranlarına rastgeleden **daha az** yakın düşüyor (ikincil kaynak). G10 döviz testinde Fibonacci seviyelerinde fiyat davranışı yakın seviyelerden farksız (forexop). **Etiket: kanıt yok.** https://forexop.com/strategy/fibonacci-fact-or-fiction/
- **Destek-direnç:** Osler (2000, FRBNY Economic Policy Review), döviz: Altı firmanın yayımladığı seviyeler gün içi trend kesilmelerini 10.000 rastgele seviye setinden daha iyi öngörüyor. Rastgele seviyelerde sekme oranı %56,2. Öngörü gücü en az 5 iş günü sürüyor. Firmalar ve kurlar arasında değişkenlik var. Mekanizma emir kümelenmesi (stop/take-profit). Altına özgü değil. **Etiket: dövizde gün içi kanıt orta; altında kanıt yok.** https://www.newyorkfed.org/medialibrary/media/research/epr/00v06n2/0007osle.pdf
- **ICT / "smart money concepts":** Akademik test **bulunamadı. Etiket: kanıt yok.**
- **Bu stratejileri kullananların sonucu:**
  - ESMA (27.03.2018): perakende CFD hesaplarının %74–89'u para kaybediyor, müşteri başına ortalama kayıp 1.600–29.000 €. https://www.esma.europa.eu/node/84933
  - SPK Başkanı (Aralık 2015): forekste 100 kişiden 87–88'i kaybediyor. 2017'de kaldıraç 1:10'a indirilince kâr/zarar oranı 23/77'den 32/68'e çıktı (yatırımcı sayısına göre; basın aktarımı). https://www.memurlar.net/haber/645699/
  - Chague, De-Losso ve Giovannetti (FGV WP 525): 2013–2015'te Brezilya mini endeks vadelisinde gün içi işleme başlayan 19.646 kişiden 300 günden fazla devam eden 1.551 kişinin yalnızca %3,0'ı net pozitif, %1,1'i asgari ücretten fazla kazandı. Öğrenme kanıtı yok. https://www.cxoadvisory.com/investing-expertise/day-trading-a-bust/

---

## 4. "Millet altın trade'inden nasıl para kazanıyor?" (kanıta dayalı yanıt)

1. **Piyasa yapıcılar ve spread toplayanlar.** BIST'te piyasa yapıcı hesapların borsa payı 0 bps (Ücretlendirme Tablosu). Kâr kaynağı yön değil, spread ve hacim.
2. **Arbitrajcılar.** VİOP, spot ve COMEX arasındaki farklar ile vade sonunda LBMA PM'e yakınsama. Kâr kaynağı lead-lag ve baz (3.10 son madde ile lead-lag çalışması).
3. **Çok piyasalı trend takipçileri (CTA).** Haftalar ile aylar arası tutuşla Sharpe ~1 portföy düzeyinde (MOP 2012, Baltas ve Kosowski). Tek başına altında ve 1–5 günde bu performans görülmüyor.
4. **Opsiyon ve volatilite satıcıları.** Emtiada negatif varyans risk primi var, kısa varyans portföyünün Sharpe'ı ~0,4 (Prokopczuk ve diğ. 2017).
5. **Uzun vadeli tutanlar (beta).** 2023–2026 rallisinde kazancın büyük kısmı kısa vadeli zamanlamadan değil, yön pozisyonundan geldi (VİOP 06.11.2026 uzlaşması 4.078,8 USD).
6. **Haber/HFT.** Makro sürprizlerde kenar dakikalar içinde tükeniyor (Elder ve diğ. 2012; Awartani ve diğ. 2024).
7. **Perakende kısa vadeli işlemciler.** Ortalamada kaybediyor (ESMA, SPK, Chague ve diğ.).

---

## 5. Bizim veride test protokolü (zorunlu)

1. **Veri.** VİOP F_XAUUSD günlük uzlaşma serisi, en yakın vade, geri dönük oranlamalı birleşik seri. Kontrol için aynı günlerde 15:15 UTC spot XAUUSD (uzlaşma VWAP'ı 15:05–15:15 UTC). Akşam seansı fiyatları ayrı tutulur, sinyalde kullanılmaz.
2. **Bilgi kesimi.** Sinyal yalnızca t günü 15:05 UTC'den önce yayımlanmış veriyle hesaplanır.
   - ABD kapanış verileri (VIX, GVZ, S&P 500, GLD tonajı) t−1 değeriyle girer.
   - COT, Cuma 20:30 UTC'den (kış) sonra yayımlandığı için en erken Pazartesi kullanılır.
   - SGE PM benchmark (06:15 UTC) ve LBMA AM aynı gün kullanılabilir. LBMA PM kışın 15:00 UTC'de çıkıyor, uzlaşma penceresine çok yakın, sinyalde kullanılmamalı.
3. **Getiri.** R_{t→t+h} = ln(P_{t+h} / P_t), h = 1, 3, 5. Çakışan pencereler için Newey-West (h−1 gecikme) veya bağımsız örnekleme kullanılır (her h günde bir giriş).
4. **Maliyet.** Gidiş-dönüş 4, 8 ve 20 bps senaryoları. Rapor her biri için net Sharpe ve başa baş maliyet (kenar / işlem sayısı) içerir.
5. **Çoklu test.** Toplam yaklaşık 60 kural × 3 ufuk. White RC / Hansen SPA veya en azından Bonferroni (α = 0,05/180 ≈ 0,0003; t ≈ 3,6). Harvey-Liu-Zhu'nun t > 3 kuralı alt sınır kabul edilir.
6. **Örneklem bölme.** Eğitim 2012–2020, doğrulama 2021–2023, test 2024–2026. Test dönemi parametre seçiminde **hiç** kullanılmaz.
7. **Kabul eşiği.** Test döneminde net (8 bps) Sharpe > 0,5, en az 100 işlem, eğitim ve test işaretleri aynı.
8. **Rejim ayrıştırması.** Altının yüksek ve düşük oynaklık dönemleri, faiz artırım ve indirim döngüleri, merkez bankası alımının yoğun olduğu 2022+ dönemi.

---

## 6. Bulunamayan veya doğrulanamayan kalemler

- Blose ve Gondhalekar (2013) hafta sonu bulgusu: özete erişilemedi.
- Marshall, Cahan ve Cahan (2008) sonuç sayıları: özete erişilemedi.
- Park ve Irwin (2007) "95 çalışma / 56 pozitif" sayıları: kaynakta doğrulanamadı.
- Altına özgü FOMC öncesi sürüklenme testi: bulunamadı.
- GVZ'nin altın getirisini öngördüğüne dair hakemli çalışma: bulunamadı.
- Hindistan festivalleri, Kurban, Çin Yeni Yılı için altın getirisi olay çalışması: bulunamadı.
- COMEX opsiyon vadesinde altın pinning'i: bulunamadı.
- Altın/gümüş oranı çift işleminin örneklem dışı hakemli testi: bulunamadı.
- Reel faiz/dolar artığının kısa vadede ortalamaya dönüşü: bulunamadı.
- Ozkan (2019) Ramazan etkisinin yönü: özette yok.
- VİOP F_XAUUSD güncel minimum fiyat adımı (0,05 mi 0,10 mu): çelişkili, BIST sözleşme unsurlarından teyit edilmeli.
- VİOP F_XAUUSD son işlem günü kuralı: altın için açık metin bulunamadı (bakırda "vade ayının son iş günü").
- 2026 seans bazlı getiri iddiası (Asya +%12,9, Kuzey Amerika −%15): köşe yazısı, doğrulanamadı.
