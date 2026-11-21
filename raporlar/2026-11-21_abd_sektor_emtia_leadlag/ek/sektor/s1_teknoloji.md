# S1 · Teknoloji (yarıiletken, donanım/yapay zekâ altyapısı, yazılım, siber güvenlik)

Sayılar `ozet_istatistik.csv` (son veri 20 Kasım 2026) ve `veri/panel_*.parquet` dosyalarından. σ1g = günlük oynaklık (%), hacim = 20 günlük ortalama günlük işlem hacmi (milyon $).

## Özet

Teknoloji 6 Ekim'den bu yana çöküş içinde: SOX zirveden -%42.5, XLK son 1 ayda -%18.3, NVDA -%40.8. Tetikleyiciler sırayla: yapay zekâ harcaması ve değerleme kaygısı, 5 Kasım ara seçim sonrası SOX -%12.2 (2020'den beri en kötü gün), 12 Kasım Jensen Huang'ın istifası, güçlü NVDA bilançosunun (17 Kasım) fiyatı tutamaması, 20 Kasım'da SEC muhasebe soruşturması haberiyle NVDA -%14. VXN 45'te. En likit ve en temiz araçlar: SMH/SOXX (yarıiletken), SOXL/SOXS (3x), XLK + TECL/TECS, IGV (yazılım), CIBR (siber). Siber güvenlik grubun içinde en dirençli kol (CRWD, PANW, OKTA 1 ayda düz ya da pozitif). Kendi 3 yıllık ön testimde basit günlük lead-lag ilişkilerinin hiçbiri |t|>2 değil; en umut verici yön liderden takipçiye yayılma değil, aşırı günlerden sonra kısa vadeli geri dönüş.

## Araç tablosu

| Alt sektör | Ana ETF | Kaldıraçlı/ters | Öncü hisseler (hacim, σ1g) | Yüksek betalı takipçiler (σ1g) | Not |
|---|---|---|---|---|---|
| Yarıiletken – tasarım (GPU/ASIC/CPU) | SMH (6.096; σ 2.8), SOXX (6.406; σ 3.2), XSD (62; eşit ağırlık) | SOXL/SOXS 3x (12.920 / 5.670; σ 9.6/9.7); NVDL 2x NVDA (709) | NVDA (48.162; 2.6), AMD (21.082; 4.7), AVGO (10.002; 3.2), MRVL (5.437; 5.5), QCOM (2.476; 3.5), ARM (1.187; 5.3) | ALAB (6.5), CRDO (6.3), MTSI (4.4), SITM (5.6), RMBS (5.1) | NVDA tek başına SMH/XLK'nin büyük ağırlığı; şu an hukuki olay riski taşıyor |
| Yarıiletken – üretim/döküm/paketleme | SMH (TSM ağırlıklı) | SOXL/SOXS | TSM (6.441; 2.8), INTC (9.683; 5.4), ASX (430; 4.2) | UMC (4.4), GFS (4.0), AMKR (5.1) | TSM ADR'si ile 2330.TW arasındaki prim test edilebilir (TWD=X gerekir) |
| Yarıiletken – ekipman | SMH/SOXX (saf ekipman ETF'i likit değil) | SOXL/SOXS | ASML (2.746; 3.1), AMAT (3.093; 4.1), LRCX (2.975; 4.4), KLAC (2.207; 4.1), TER (1.138; 5.0) | ONTO (4.9), FORM (5.7), MKSI (4.0), ACMR (5.6), AEHR (8.3; hacim 170) | Ekipman 3 ayda -%37..-44; Japon eşleri (8035.T, 6857.T) ABD açılışından önce kapanır |
| Yarıiletken – bellek/depolama | (saf likit ETF yok; SMH içinde MU) | SOXL/SOXS dolaylı | MU (25.726; 5.4), SNDK (12.604; 7.1), WDC (2.525; 5.3), STX (3.387; 4.9) | SNDK (7.1), AAOI değil; NTAP (3.1, düşük beta) | MU yılbaşından +%108 ama 1 ayda -%31; DRAM sözleşme fiyatı hâlâ artıyor (4Ç26 +%10-15) |
| Yarıiletken – analog/MCU (savunmacı kol) | SOXX/XSD | – | TXN (2.636; 2.8), ADI (2.051; 2.5), NXPI (1.487; 3.2), MCHP (1.142; 3.4), ON (779; 4.1) | MPWR (3.8), LSCC (4.1), STM (4.0) | Beta düşük (QQQ'ya 1.2-1.5); çöküşte görece dirençli |
| Donanım, ağ, yapay zekâ altyapısı | XLK (2.565; σ 1.9), AIQ (101), SMH dolaylı | TECL/TECS 3x XLK (187 / 43 – TECS ince); TQQQ/SQQQ 3x NDX (5.678 / 2.855) | DELL (2.845; 5.2), ANET (1.643; 3.7), VRT (1.773; 4.5), CSCO (2.219; 2.4), APH (1.237; 3.1), GLW (1.271; 4.9), HPE (724; 3.9) | SMCI (5.9), CLS (5.1), CIEN (5.2), FN (5.2), FLEX (4.8), CRWV (6.4; 3.645), NBIS (7.2; 4.020) | Neocloud (CRWV, NBIS) 1 ayda -%29/-%49: yapay zekâ borç kaygısının en uç ifadesi |
| Optik/bağlantı (altyapı alt kolu) | – | – | LITE (4.270; 6.4), COHR (2.180; 5.8) | AAOI (9.3; 810), CRDO, ALAB, FN | En yüksek oynaklık; NVDA ile eşzamanlı korelasyon yüksek, gecikmeli ilişki yok |
| Yazılım ve bulut | IGV (973; σ 2.1), SKYY (52), FDN (52) | Likit kaldıraçlı yazılım ETF'i yok; TQQQ/SQQQ dolaylı | MSFT (15.691; 2.2), ORCL (5.216; 3.8), PLTR (4.257; 3.8), NOW (2.345; 4.1), APP (2.059; 5.1), CRM (1.567; 3.0), SNOW (1.271; 4.2), INTU (1.041; 3.3) | DDOG (4.4), TEAM (5.1), MDB (4.6), HUBS (4.7), TWLO (4.1), U (4.5) | Yazılım yıl boyu "yapay zekâ yazılımı yiyecek" anlatısıyla geride (IGV YTD -%13); ORCL YTD -%47 |
| Siber güvenlik | CIBR (240; σ 2.0), HACK (64) | – | PANW (2.678; 3.3), CRWD (2.185; 3.7), FTNT (904; 3.1), NET (1.271; 4.3), OKTA (979; 4.5), ZS (504; 4.4) | S (3.6; 240), OKTA, NET | Grubun en dirençlisi: CRWD YTD +%96, PANW +%86, CIBR 1 ay -%11 (XLK -%18) |

## 1-3 günlük sürücüler ve öncü göstergeler

Ayrıntı ve test tanımları: `ek/hipotez/s1_teknoloji.json` (24 hipotez).

**Zamanlama gerçeği.** Asya seansları (Tayvan, Kore, Japonya) ABD açılışından önce kapanır. Bu bilgi kapanışta bilinir ama ABD açılışında zaten fiyatlanmıştır; kapanışta alıp 1-3 gün tutan biri için taşıyıcı değildir. ABD kapanışından sonra gelen tek Asya bilgisi ertesi sabahki seanstır ve o karar anında bilinmez. Asya hipotezleri bu yüzden öncelik 3. TSMC aylık satışı (her ayın ~10'u) ve Kore 10/20 günlük ihracat verisi de ABD açılışından önce yayınlanır.

**Kendi ön testim (2023-11 → 2026-11, 752 gün, kapanış-kapanış, hedefin kendi getirisi kontrol edildi).** Lider_t → takipçi_t+1 katsayıları: NVDA→SMCI +0.08 (t 0.9), NVDA→CRDO −0.13 (t −1.6), NVDA→SOXX −0.08 (t −1.9), MU→STX +0.05 (t 1.1), MU→WDC +0.04 (t 0.9), SOX→QQQ +0.05 (t 1.2), 2330.TW→TSM −0.08 (t −1.5), ^TNX→IGV +0.05 (t 1.0). Sonuç: günlük frekansta lider→takipçi yayılması yok ya da ters işaretli. Bu, literatürle uyumlu: tedarik zinciri öngörülebilirliği aylık frekansta ve küçük tedarikçilerde bulunuyor; günlük frekansta lead-lag ilişkileri büyük ölçüde kayboluyor.

**Test etmeye değer sürücüler (öncelik 2):**
1. **Aşırı gün sonrası geri dönüş:** SOXX < −%5 günlerden sonra t+1..3 ort. +%1.02 (n=28, isabet %50; koşulsuz +%0.35). Kaldıraçlı ETF gün sonu dengelemesi (SOXL hacmi 12.9 milyar $/gün) bu etkiyi büyütebilir. VXN sıçraması ve VIX/VIX3M > 1 ile birlikte test et.
2. **NVDA'ya özgü şok → sektörde ters hareket:** NVDA'nın SMH'ye göre artık getirisi büyükse ertesi gün SOXX kısmen düzelir (ön test t −1.9).
3. **Olay tabanlı yayılma:** NVDA, MU, hiper ölçekleyici (MSFT, GOOGL, META, AMZN) ve CRWD/PANW bilançoları. Tepki ertesi gün kapanışında bilinir; takipçilerde t+1..3 sürüklenme test edilir. Örneklem küçük, Kasım 2026'da güçlü NVDA bilançosu bir gün bile tutmadı.
4. **Bellek içi yayılma:** MU → WDC/STX/SNDK (zayıf pozitif, iki yarıda tutarlı).
5. **Yapısal gece getirisi:** SMH 3 yılda gecede +19.3 bps/gün, gün içinde −4.0; SOXX +15.7/−1.8; NVDA +22.8/−4.9. Kapanışta alıp tutan profil bu primi doğal olarak yakalar. Açılışta satmak (gün içini atlamak) ayrıca test edilmeli.

**Faiz:** 10 yıllık getiri %4.9-5.3 bandında. Aralık'ta Fed faiz artırımı beklentisi var (Citi). Faiz yazılım değerlemesini eşzamanlı etkiler; gecikmeli etki ön testte görülmedi.

## 2026 durumu ve takvim

- **Yılın ilk 9 ayı:** Yapay zekâ donanımı ve bellek patlaması. MU YTD hâlâ +%108, SNDK +%218, DELL +%123. DRAM sözleşme fiyatı 1Ç26'da +%93-98 (çeyreklik) arttı. Yazılım ise yıl boyu geride kaldı (IGV −%13, ORCL −%47, INTU −%59).
- **6 Ekim → 20 Kasım:** SOX 13.218'den 8.409'a düştü (−%36). Kilometre taşları: 30 Ekim (QCOM −%11, SOX −%7.2), 5 Kasım (ara seçim sonrası SOX −%12.2, MU −%17.5), 12 Kasım (Huang istifa etti, CFO Colette Kress geçici CEO), 17 Kasım (NVDA 115.8 milyar $ gelir, 4Ç rehberi 130 milyar $; ertesi gün −%2.9), 19 Kasım (Anthropic halka arzı, 1.5 trilyon $ değerleme), 20 Kasım (Reuters: SEC muhasebe incelemesi; NVDA −%14, SOX −%10.7, Nasdaq −%5.3; S&P 500 ve Dow düzeltme bölgesinde). Bir gün önce Kaliforniya Başsavcısı NVDA'ya celp gönderdi. ABD 17 Kasım'da Malezya, Singapur ve diğer ülkeleri "kabul edilemez yönlendirme riski" listesine aldı.
- **Anlatı:** Temel veri hâlâ güçlü (TSMC Ekim satışı rekor, yıllık +%59.7; DRAM 4Ç26 +%10-15). Fiyat ise yönetişim, hukuk, yapay zekâ borcu ve faiz artırımı riskiyle değerleme sıkışması yaşıyor. Temel veri ile fiyat arasındaki bu kopukluk, olay tabanlı "iyi haber → alım" kurallarının şu an çalışmadığını gösteriyor.
- **Takvim (doğrula):** 26 Kasım Şükran Günü, piyasa kapalı; 27 Kasım yarım gün (bellekten). 1 Aralık CRWD bilançosu. Kore Kasım ihracatı 1 Aralık civarı (bellekten). 8-9 Aralık FOMC. 9 ya da 10 Aralık AVGO. 10 Aralık ORCL (teyitsiz) ve Kasım TÜFE (tek kaynak). ~10 Aralık TSMC Kasım satışı. 15 Aralık MU (teyitsiz). MRVL Aralık başı (bellekten, teyitsiz). NVDA SEC/celp süreci ve CEO araması gündemi yönetecek, tarihleri belirsiz.

## Tuzaklar

- **Kaldıraçlı ETF erimesi:** SOXL 1 yılda −%14 iken SOXX +%32; SOXL zirveden −%89.7. 3x ürün yüksek oynaklıkta (σ1g 9.6) 1-3 gün tutmada bile yolu sert bozar. VXN 45'te gidiş-dönüş erimesi en yüksek seviyede. TECS'in hacmi 43 milyon $; yayılma (alış-satış farkı) maliyeti dikkate alınmalı. NVDL 1 yılda −%66.
- **Tek hisse ve olay riski:** NVDA'da SEC, Kaliforniya Başsavcılığı, ihracat (Megaspeed/Singapur soruşturması) ve CEO araması aynı anda açık. Hafta sonu ya da gece haberi gap riski taşıyor; gece getirisi primi tam bu riskin bedeli. Bilanço gecesi taşıma riski: MU, AVGO, ORCL, CRWD Aralık'ta.
- **Rejim kayması:** Ön testin 3 yılı çoğunlukla boğa piyasası; mevcut çöküş rejiminde ilişkiler değişebilir. Aşırı gün sonrası geri dönüş, 2008/2022 tipi sürekli düşüşte art arda zarar verir (ör. 5 Kasım sonrası iki gün geri dönüş, sonra yeni dip).
- **Ölçek sorunu:** Hacmi 50 milyon $'ın altındaki takipçiler (CAMT, POWI, ACLS) ve 20 milyon $'ın altındaki ETF'ler (ROBO 10.5) bu profilde uygun değil.
- **Endeks yoğunlaşması:** XLK ve SMH'nin getirisi birkaç dev hisseye bağlı (doğrulanmadı, bellek: NVDA, AAPL, MSFT XLK'nin yarısına yakın). "Sektör" sinyali çoğu zaman NVDA sinyalidir.
- **Bayram/yarım gün:** 26-27 Kasım düşük likidite; 1-3 günlük pencere takvim günü değil işlem günüyle sayılmalı.

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| 5 Kasım'da SOX -%12.25, Mart 2020'den beri en büyük günlük kayıp | https://247wallst.com/investing/2026/11/06/chip-stocks-just-had-their-second-worst-day-on-record/ | "settled at 9,011.14, a loss of 1,257.52 points, or 12.25%" (arama özeti) | yüksek (panel ile tutarlı: -%12.2) |
| 5 Kasım satışı ara seçim ve QCOM zayıf rehberiyle ilişkilendirildi | https://digg.com/world-business/27a40eau | "Chip stocks sink after midterms as Qualcomm slides following earnings" | orta |
| Huang istifa etti, Kress geçici CEO | https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000082/nvidiaannouncesceotransiti.htm | "resignation of Jen-Hsun Huang, as NVIDIA's President, Chief Executive Officer and member of the Board, effective immediately" (arama özeti) | yüksek |
| NVDA 3Ç FY27 gelir 115.8 milyar $, 4Ç rehberi 130 milyar $ | https://www.guru3d.com/story/nvidia-q3-fy2027-usd-1158-billion-revenue-data-center-usd-1076-billion-usd-130-billion-q4/ | 115.8 milyar $ gelir; 4Ç 130.0 milyar $ ±%2 | yüksek |
| Güçlü bilançoya rağmen NVDA fiyatı tutmadı | https://www.fool.com/investing/2026/11/20/here-is-why-nvidia-stock-crashed-on-friday/ | "Nvidia's quarterly results released on Nov. 17 were impressive. Revenue rose 103% year over year" | yüksek |
| 20 Kasım NVDA -%14, SEC muhasebe incelemesi haberi | https://www.fool.com/investing/2026/11/20/here-is-why-nvidia-stock-crashed-on-friday/ | "plunged 14% on Friday following reports that the U.S. Securities and Exchange Commission (SEC) is investigating the tech titan's accounting practices" | yüksek |
| Kaliforniya Başsavcısı NVDA'ya celp gönderdi | https://www.fool.com/investing/2026/11/20/here-is-why-nvidia-stock-crashed-on-friday/ | "served an investigative subpoena on Nvidia" | yüksek |
| 20 Kasım Nasdaq -%5.28, S&P 500 -%3.7, Dow ve S&P düzeltmede | https://www.foxbusiness.com/markets/wall-street-suffers-historic-losses-dow-sp-500-plunge-correction-territory | "the S&P 500 dropped 3.7% and the tech-heavy Nasdaq Composite plunged 5.28%" | yüksek |
| Anthropic ikinci işlem gününde ~-%9 | https://www.foxbusiness.com/markets/wall-street-suffers-historic-losses-dow-sp-500-plunge-correction-territory | "Anthropic fell about 9% during its second trading session as a public company" | yüksek |
| Anthropic 19 Kasım'da 83 $'dan arz edildi, 1.5 trilyon $ değerleme | https://www.aljazeera.com/economy/2026/11/19/anthropic-starts-trading-in-the-us-after-blockbuster-ipo | "priced its IPO at $83 per share ... value the entire business at $1.5 trillion" (arama özeti) | orta |
| ABD, Malezya/Singapur vb. ülkeleri yönlendirme riski listesine aldı; Megaspeed cezai soruşturması | https://www.malaymail.com/news/money/2026/11/17/after-nvidia-scandal-us-targets-third-party-data-centres-in-malaysia-singapore-and-more/243588 | "unacceptable risk of diversion" (arama özeti) | orta |
| TSMC Ekim 2026 satışı rekor, yıllık +%59.7 | https://pr.tsmc.com/english/news/3349 | NT$586.89 milyar; yıllık +%59.7, aylık +%14.7 (arama özeti) | yüksek |
| TrendForce: 4Ç26 konvansiyonel DRAM sözleşme fiyatı +%10-15, NAND +%15-20 | https://www.trendforce.com/presscenter/news/20260930-13258.html | DRAM +%10-15 QoQ; NAND +%15-20 (arama özeti) | orta |
| 1Ç26'da DRAM sözleşme fiyatı +%93-98 | https://247wallst.com/technology-3/2026/07/17/micron-technology-record-dram-pricing-meets-a-stock-in-retreat/ | "rose an estimated 93-98% quarter-over-quarter in Q1 2026" (arama özeti) | orta |
| Citi Aralık'ta 25 bp Fed faiz artırımı bekliyor | https://investinglive.com/central-banks/icymi-citi-now-expects-a-december-fed-rate-hike-after-hotter-september-us-inflation/ | "expects the Fed to hike rates by 25bp in December" (arama özeti) | orta |
| FOMC 8-9 Aralık 2026; Kasım TÜFE 10 Aralık | https://streamlinefeed.co.ke/news/fed-signals-december-rate-hike-after-hot-october-inflation-data | "December 8-9"; TÜFE 10 Aralık (tek kaynak) | düşük |
| CRWD bilançosu 1 Aralık 17:00 ET; AVGO 9 Aralık | https://guptadeepak.com/earnings/calendar/ | CRWD 1 Aralık (teyitli); AVGO 9 Aralık (TipRanks: 10 Aralık) | orta |
| MU 15 Aralık 16:05 ET, ORCL 10 Aralık (teyitsiz) | https://www.financecalendar.com/events/category/earnings-season/2026-12/ | "to be confirmed" (arama özeti) | düşük |
| Tedarikçi fiyatları müşteri hareketine gecikmeli tepki verir (aylık) | https://ideas.repec.org/a/taf/ufajxx/v66y2010i3p60-77.html | müşteri endüstri getirileri tedarikçiyi 22 gelişmiş ülkede öncüler (arama özeti) | orta |
| Customer momentum'un bir kısmı basit lead-lag; büyüklük oranı kısıtı etkiyi 2-4 kat düşürür | https://arxiv.org/pdf/2301.11394 | "cuts the magnitude of customer momentum by a factor of 2-4" (arama özeti) | orta |
| Aykırı kanıt: lead-lag ilişkileri günlük ölçekte kaybolur | https://www.arxiv.org/pdf/1111.7103 | "on a daily time scale, the absence of lead/lag relationships thus seems to be quite reasonable" (arama özeti) | orta |
| Kaldıraçlı ETF ve opsiyon gamma dengesizliği gün sonu momentum/tersine dönüş yaratır | https://www.alexandria.unisg.ch/server/api/core/bitstreams/5a99db31-0d37-4f86-9502-8cb0f3bff4fe/content | büyük negatif gamma dengesizliği "end-of-day momentum" yaratır (arama özeti) | orta |
| SMH gider oranı %0.35, MVIS US Listed Semiconductor 25 endeksi | https://www.etfcentral.com/news/etf-comparison-vaneck-semiconductor-etf-smh-versus-ishares-semiconductor-etf-soxx | %0.35 (arama özeti) | orta |
| SOXL ve TECL toplam gider oranı ~%0.91 / %0.94 (Kasım 2026; kaynaklar arası çelişkili: %0.75-1.08) | https://www.etfcentral.com/compare-etfs/TECL-vs-SOXL | TECL %0.94, SOXL %0.91 | düşük |
| SOXX ICE Semiconductor Index'i izler (eski PHLX SOX); gider ~%0.34-0.35 | https://www.fool.com/investing/2026/06/14/smh-vs-soxx-vs-soxq-which-semiconductor-etf-best/ | ICE Semiconductor Index; SOXQ aynı endeks %0.19 (arama özeti) | orta |
| Kendi ön testi: günlük lider→takipçi lead-lag katsayılarının hiçbiri |t|>2 değil | veri/panel_adjclose.parquet (2023-11..2026-11) | NVDA→SOXX t −1.88; MU→STX t 1.14; SOX→QQQ t 1.24 | orta (tek dönem, çoklu test düzeltmesi yok) |
| Kendi ön testi: SOXX < −%5 günü sonrası t+1..3 ort. +%1.02 (n=28) | veri/panel_adjclose.parquet | koşulsuz +%0.35; isabet %50 | düşük (n küçük) |
