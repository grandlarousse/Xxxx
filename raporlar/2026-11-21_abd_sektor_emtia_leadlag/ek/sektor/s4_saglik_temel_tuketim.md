# S4 Sağlık ve temel tüketim

## Özet

2026'da XLV (+%15,9) ve XLP (+%18,7) SPY'ı (+%1,9) yendi; ama bu iki ayrı hikâye: sağlıkta getiri LLY, JNJ, ABBV, MRK, AMGN, GILD (+%26 ile +%38) gibi büyük ilaçlardan ve Ağustos'taki MRNA sıçramasından geldi; cihaz (BSX -%56, ISRG -%30) ve sigortacılar (UNH +%5, son 5 gün -%17) zayıf. Temel tüketimde KO (+%41), MO (+%36), CL (+%28) önde; paketli gıda (GIS -%18, CAG -%8) geride. Son ayda SPY -%9,7 ve XLK -%18 düşerken XLP +%0,5: klasik savunmacı rotasyon sürüyor. 1-3 günlük öncüler için kendi hızlı testimizde tek sağlam aday **soya yağı (ZL=F) -> BG, ADM** (2019 sonrası t ≈ 2,1-2,3, 2024 sonrası t ≈ 2; 2018 öncesi etkisiz). Kakao -> HSY, kahve -> SBUX, buğday -> GIS, LLY -> NVO ve IWM -> XBI (pozitif) hipotezleri günlük veride **çalışmıyor**. Sektörlerde baskın desen öncülük değil, günlük ters dönüştür ve 2024 sonrası zayıfladı.

## Araç tablosu

Sayılar ozet_istatistik.csv'den: σ = günlük oynaklık (%), hacim = 20 günlük ortalama günlük işlem (milyon $). Gider oranları ihraççı sayfalarından (defter).

| Alt sektör | Ana ETF | Kaldıraçlı/ters | Öncü hisseler (likit) | Yüksek betalı takipçiler | Not |
|---|---|---|---|---|---|
| Büyük ilaç | XLV (hacim 2.383, σ 1,08; gider 0,08) | Evrende yok; CURE 3x (Direxion, gider %0,94) / RXL 2x (ProShares, ~%0,95, ihraççıdan doğrulanmadı) var | LLY (4.397), JNJ (2.164), ABBV (1.547), MRK (1.371), AMGN (1.266), PFE (1.111), GILD (1.080), BMY (639) | NVO (σ 2,86), ALNY (3,45), INSM (4,19), ZTS (2,42), HIMS (5,89) | XLV'nin %16,8'i LLY: XLV büyük ölçüde LLY+JNJ+ABBV. XPH (15) ve PJP (4,9) çok ince |
| Biyoteknoloji | XBI (1.344, σ 1,92; eşit ağırlığa yakın, gider 0,35), IBB (455, σ 1,50; gider 0,44) | LABU 3x / LABD -3x (gider 0,96 / 1,07 net); hacim LABD 193, LABU 79 | REGN (972), VRTX (850), AMGN, GILD, BIIB (291), ARGX (320) | MRNA (σ 12,3), CRSP (3,65), NTLA (4,81), BEAM (4,58), VKTX (4,39), BNTX (2,94) | ARKG (241, σ 3,0) tema karışık. NTLA, BEAM, CRSP hacmi 60-95: eşikte |
| Medikal cihaz ve araçlar | IHI (174, σ 1,40; gider 0,37) | Yok | TMO (1.354), ISRG (1.101), SYK (1.043), BSX (883), ABT (867), DHR (775), MDT (742) | NTRA (σ 3,35), ILMN (3,10), IQV (2,57), DXCM (2,38) | XHE (2,3) işlem yapılamaz. BSX -%56 yılbaşından beri, ISRG -%30 |
| Sağlık sigortası ve hizmetleri | IHF (80, σ 1,32) | Yok | UNH (2.581), CVS (1.110), HUM (738), HCA (730), ELV (624), CI (555) | HUM (σ 3,03), CNC (2,96), CVS (2,18) | Tek haber günü -%10 ile -%21 (bkz. Tuzaklar) |
| Gıda ve içecek | XLP (1.897, σ 1,00; gider 0,08) | Evrende yok | KO (1.848), PEP (1.389), MDLZ (572), MNST (491), KHC (368), HSY (377), STZ (318), GIS (295) | CELH (σ 3,60), CAG (2,08), STZ (2,01) | Düşük σ: 1-3 günde beklenen hareket ±%2 |
| Tütün | XLP (PM %5,9 + MO %4,5) | Yok | PM (1.079), MO (656) | — | MO SPY betası -0,41: en savunmacı |
| Ev ve kişisel bakım | XLP | Yok | PG (1.609), CL (540), KMB (828) | EL (σ 3,03, beta 1,25) | EL temadan çok Çin/turizm hikâyesi |
| Gıda perakendesi ve tarım işleme | XLP (WMT %11,4, COST %9,8); DBA (27) | Yok | WMT (2.982), COST (2.709), TGT (745), KR (376), DG (292), DLTR (303), ADM (277), BG (171), TSN (264) | DLTR (σ 2,74), DG (2,48), CTVA (2,56) | ADM, BG, TSN için soya, mısır ve hayvan vadelileri doğrudan öncü |

## 1-3 günlük sürücüler ve öncü göstergeler

Kendi taramamız (kod/s4_hizli_tarama.py, kod/s4_islem_testi.py; sonuçlar ek/hipotez/s4_hizli_tarama.csv ve s4_islem_testi.csv). Giriş t kapanışı, çıkış t+1 ya da t+3 kapanışı, 5 bp maliyet. Yaklaşık 40 öncü-hedef çifti ve 3 dönem tarandı: t ≈ 2 olan tek sonuçlar çoklu test düzeltmesinden geçemeyebilir; ana ajanın tam testine aday olarak verildi.

- **Tarım işleyiciler (en güçlü aday):** ZL=F (soya yağı) 60 günlük z-skoru |z|>1 olduğunda yönünde BG: OOS (2019+) 608 işlem, +18 bp net, t 2,26; 2024+ +25 bp, t 2,05; plasebolar |t|<1,5. ADM benzer (t 2,1). Yıl yıl BG: 2017-18 negatif, 2021'den beri her yıl pozitif (2026: 74 işlem, +41 bp). 2018 öncesi yok: etki biyoyakıt politikasının soya yağını belirleyici yaptığı dönemle sınırlı olabilir (mekanizma doğrulanmadı). ZS=F de BG'yi t 2,4 (OOS) ile öngörüyor. CBOT 14:20 ET kapandığı için 16:00'da bilinir.
- **Paketli gıda ve girdi emtiaları:** kakao -> HSY/MDLZ, kahve -> SBUX, buğday -> GIS/KHC/CAG hipotezleri 1-3 günde **çalışmıyor** (|t|<1,8, işaret döneme göre değişiyor). Maliyet etkisi bilanço ve fiyat artışı duyurularıyla, haftalar içinde fiyatlanıyor.
- **Dolar:** UUP artışı ertesi gün PM, PG, KO, CL, XLP'yi düşürüyordu (2019-26 t -2,5 ile -4,0) ama 2024-26'da kayboldu.
- **Faiz -> biyotek ve savunmacılar:** ^TNX artışı ertesi gün XLP/XLV/IBB'yi düşürüyordu (2019-26 t ≈ -3), 2024-26'da işaret döndü. 10 yıllık faiz -> XBI hipotezi günlük vadede kanıtlanmadı.
- **Risk iştahı (IWM) -> XBI:** hipotezin tersi. IWM'nin sert düştüğü gün (z<-1,5) XBI almak ertesi gün OOS +46 bp (t 1,7), 3 günde 2024+ +95 bp (t 1,4): öncülük değil, birlikte aşırı satış ve geri dönüş.
- **Sektör içi ters dönüş:** XLV, XLP, PG, XBI kendi günlük getirileriyle ertesi gün negatif ilişkili (2019-26 corr t -3,5 ile -6,0). Ancak eşikli al sinyali (z<-1,5) net kâr üretmiyor ve 2024-26'da etki yarıya indi: bu kısmen 2020 dalgalanmasından geliyor.
- **Lider -> takipçi:** UNH -> HUM/ELV/CVS, LLY -> NVO/VKTX/HIMS, TMO -> DHR/IQV için ertesi gün pozitif yayılma yok; ortak haber aynı gün fiyatlanıyor. WMT/COST yükselişi ertesi gün DLTR'yi düşürüyor (t -3,2; 2024+ -2,1).
- **Yurt dışı seans:** Novo Nordisk Kopenhag (11:00 ET kapanış) -> NVO ADR t 1,6-1,7: zayıf; ADR o bilgiyi 16:00'ya kadar zaten fiyatlıyor.
- **Olay takvimi (günlük öncü değil, risk filtresi):** CMS Medicare Advantage ön oran bildirimi (Ocak sonu-Şubat başı) ve kesin oran (Nisan başı, kapanıştan sonra); FDA PDUFA tarihleri; bilanço; ASCO/ASH gibi kongreler. Veride: 27 Ocak 2026'da UNH -%19,6, HUM -%21,1, CVS -%14,2; 7 Nisan'da UNH +%9,4, CVS +%6,7. Doğrulandı: 26 Ocak akşamı CMS 2027 ön oran bildirimi (ortalama +%0,09; yatırımcı beklentisi ~%5) 27 Ocak düşüşünü; 6 Nisan akşamı kesin oran (+%2,48, risk skoru dahil +%4,98) 7 Nisan yükselişini getirdi. 18 Kasım düşüşü (UNH -%10,2, HUM -%13,0) CMS'nin 16 Kasım'da önerdiği dolandırıcılık kuralından (CRUSH; geçmiş ödemelere geriye dönük denetim) geldi; yorum süresi 19 Ocak 2027'de bitiyor.

## 2026 durumu ve takvim

Aylık (yüzde, ortak veri): Ocak-Şubat XLP +7,5 / +7,8 ile yılın kazancının çoğunu yaptı; Nisan-Mayıs teknoloji rallisinde (XLK +20 / +20) geride kaldı; Ekim'de XLV +9,8, XLP +10,9 iken SPY -0,9, XLK -8,3; Kasım'da (20'sine kadar) XLK -17, SPY -8,7, XLP +1,2, XLV -4,1. Yani 2026 güçlülüğü büyük ölçüde iki savunmacı dalgadan (Ocak-Şubat, Ekim-Kasım) geliyor; sürdürülebilirliği teknoloji satışının sürmesine bağlı. XLV'nin yükü LLY'de (%16,8, 3 yılda +%134). Sağlıkta son haftanın ayrışması: UNH -%16,6 ve HUM -%13,3 (5 gün; 18 Kasım'da -%10,2 / -%13,0), INSM +%16,6. MRNA'nın 19 Ağustos'ta +%177 ve ertesi gün -%23,5 yapması yılın en büyük tek olayı: Merck ile geliştirilen kişiye özel mRNA kanser aşısı (intismeran autogene) melanomda Faz 3'te başarılı oldu. Cihazda BSX: 4 Şubat'ta temkinli 2026 kılavuzu ve zayıf elektrofizyoloji (-%17,6), 27 Mayıs'ta Watchman satışlarının durgunlaşabileceği açıklaması (-%10 üstü). ISRG: Temmuz'da ABD da Vinci işlem büyümesinin %14'ten %12'ye yavaşlaması, kılavuzun yükseltilmemesi ve yüksek değerlemenin daralması. XLP gücü: teknoloji/yapay zekâ değerleme kaygısı ve tarifelerle savunmacı rotasyon; Barclays'e göre sektör 1990'dan beri en güçlü yıl başlangıcını yaptı (ilk 30 işlem gününde +%15,6). XLV için ayrı neden kaynağı bulunamadı; yük LLY ve büyük ilaçta.

Önümüzdeki haftalar: 26 Kasım Şükran Günü kapalı, 27 Kasım 13:00 ET erken kapanış (NYSE); 10 Aralık 12:00 ET USDA WASDE; 12-15 Aralık ASH hematoloji kongresi (New Orleans); 11-14 Ocak 2027 J.P. Morgan sağlık konferansı (San Francisco; biyotek için yılın en yoğun haber haftası); 19 Ocak 2027 CRUSH kuralı yorum süresinin sonu. Doğrulanmadı (bellek): GIS (Aralık ortası), KR, COST bilanço tarihleri; CMS 2028 ön oran bildirimi Ocak sonu-Şubat başı (son yılın deseni: 26 Ocak 2026).

## Tuzaklar

- **Kaldıraçlı erime:** LABU ve LABD, σ1g ≈ %5,7. LABD 3 yılda -%95, LABU 1 yılda XBI +%23 iken +%28 (3x değil). 1-3 gün taşımada erime küçüktür ama oynak günlerde yol bağımlılığı büyür; LABU hacmi (79) LABD'den (193) düşük. Gider 0,96 / 1,07.
- **Düşük likidite:** XPH, PJP, XHE, XHS günlük 2-15 milyon $; kapanışta alım için uygun değil. NTLA, BEAM, CRSP, VKTX eşikte.
- **Tek hisse olay riski:** biyotekte tek veri ya da FDA kararıyla ±%25-180 (MRNA +%177, ALNY -%28 ve -%25, HIMS +%41). Sigortada politika duyurusuyla -%20. Kapanışta alıp taşıyan biri için ertesi gün açılış boşluğu (gap) asıl risktir; bilinen olay günlerinden önceki kapanışta pozisyon açılmamalı.
- **Sığ beklenen hareket:** XLP ve KO, PG gibi hisselerde σ3g ≈ %2; 5-10 bp maliyet ve kayma, 1 günlük kenarın önemli bir kısmını yer.
- **Rejim kayması:** dolar, faiz ve ters dönüş sinyalleri 2019-23'te güçlü, 2024 sonrası zayıf. Soya yağı sinyali de 2018 öncesinde yoktu.
- **Konsantrasyon:** XLV = LLY + JNJ + ABBV ≈ %35; XLP = WMT + COST ≈ %21. "Sektör" işlemi aslında birkaç hissenin işlemi.

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| XLV gider oranı %0,08 | https://www.ssga.com/us/en/intermediary/etfs/the-health-care-select-sector-spdr-fund-xlv | "Gross Expense Ratio ... 0.08%" | yüksek |
| XLV'de LLY ağırlığı %16,8, JNJ %10, ABBV %7,8 | https://www.ssga.com/us/en/intermediary/etfs/the-health-care-select-sector-spdr-fund-xlv | "ELI LILLY + CO 5,801,972 16.81% JOHNSON + JOHNSON 17,474,334 10.01% ABBVIE INC ... 7.79%" | yüksek |
| XLV Ekim 2026 getirisi | https://www.ssga.com/us/en/intermediary/etfs/the-health-care-select-sector-spdr-fund-xlv | "Oct 31 2026 9.86% 9.86% 20.92%" (1 ay, QTD, YTD) | yüksek |
| XBI gider %0,35, değiştirilmiş eşit ağırlık | https://www.ssga.com/us/en/intermediary/etfs/spdr-sp-biotech-etf-xbi | "Gross Expense Ratio: 0.35%" ; "The Index is modified equal weighted." | yüksek |
| XBI varlığı | https://www.ssga.com/us/en/intermediary/etfs/spdr-sp-biotech-etf-xbi | "Assets Under Management $9,635.62 M as of Nov 19 2026" | yüksek |
| LABU/LABD 3x, giderler | https://www.direxion.com/product/daily-sp-biotech-bull-bear-3x-etfs | "seek daily investment results ... of 300%, or 300% of the inverse" ; "Expense Ratio (gross/net %) 0.96 / 0.96" ; LABD "1.08 / 1.07" | yüksek |
| IBB gider %0,44 | https://www.ishares.com/us/products/239699/ishares-nasdaq-biotechnology-etf | "Expense Ratio 0.44%" | yüksek |
| IHI gider %0,37, YTD -%9,5 | https://www.ishares.com/us/products/239516/ishares-us-medical-devices-etf | "Expense Ratio 0.37%" ; "YTD: Decrease -9.53%" | yüksek |
| XLP gider %0,08, WMT %11,4, COST %9,8 | https://www.ssga.com/us/en/intermediary/etfs/the-consumer-staples-select-sector-spdr-fund-xlp | "WALMART INC 13,442,987 11.37% COSTCO WHOLESALE CORP 1,337,731 9.82%" ; "Gross Expense Ratio: 0.08%" | yüksek |
| ZL=F -> BG yönlü sinyal | ek/hipotez/s4_islem_testi.csv (kendi testimiz) | OOS n 608, net +18,3 bp, t_anormal 2,26; 2024+ t 2,05; IS t -0,08 | orta |
| ZL=F -> ADM yönlü sinyal | ek/hipotez/s4_islem_testi.csv | OOS net +16,6 bp, t 2,12; 2024+ t 2,06 | orta |
| Kakao -> HSY çalışmıyor | ek/hipotez/s4_islem_testi.csv | CC z>1,5 sat HSY h=1: IS t -0,09, OOS 0,29, 2024+ 0,25 | orta |
| IWM düşüşü sonrası XBI geri dönüşü | ek/hipotez/s4_islem_testi.csv | IWM z<-1,5 al XBI h=1 OOS +45,6 bp, t 1,70 | orta |
| Savunmacı günlük ters dönüş zayıfladı | ek/hipotez/s4_hizli_tarama.csv | XLP_oto t: 2019-26 -6,0; 2024-26 -1,8 | orta |
| 27 Ocak 2026 sigortacı çöküşü | ortak veri (adjclose) | UNH -19,6%, HUM -21,1%, CVS -14,2% | yüksek |
| Nedeni CMS 2027 ön oran bildirimi | https://www.morningstar.com/markets/healthcare-managed-care-stocks-plunge-following-almost-flat-medicare-rate-proposal | ortalama +0.09%; Cantor: "investor base case expectations of 5%" | yüksek |
| 7 Nisan yükselişi: kesin oran +%2,48 | https://www.fiercehealthcare.com/regulatory/cms-gives-medicare-advantage-rates-248-bump-2027-plan-year-final-rule | "2.48%" ; risk skoru dahil "4.98%" | yüksek |
| 18 Kasım düşüşü: CMS CRUSH önerisi | https://www.trefis.com/stock/hum/articles/626885/why-is-humana-stock-falling/2026-11-19 | UNH -10.2%, HUM -13.0%; yorum süresi "until Jan. 19, 2027" | orta |
| MRNA 19 Ağustos 2026 sıçraması | ortak veri (adjclose) | +177,0%, ertesi gün -23,5% | yüksek |
| MRNA nedeni: melanom Faz 3 başarısı | https://abcnews.com/Health/wireStory/moderna-shares-surge-after-experimental-mrna-cancer-treatment-135776280 | kapanış $174.38, "up 176.97%"; intismeran autogene, Merck ile | yüksek |
| BSX düşüşü: kılavuz ve Watchman | https://www.fool.com/investing/2026/05/29/why-boston-scientific-stock-was-sliding-this-week/ | 4 Şubat -%17,6; 27 Mayıs "down over 10%" | orta |
| ISRG düşüşü: işlem büyümesi yavaşladı | https://www.fool.com/investing/2026/07/14/heres-exactly-why-intuitive-surgical-stock-is-flou/ | ABD da Vinci işlem büyümesi 12% (Q1 14%) | orta |
| CURE gider %0,94 | https://www.direxion.com/product/daily-healthcare-bull-3x-etf | gross/net 0.94% | yüksek |
| RXL gider ~%0,95 | https://etfdb.com/etf/RXL/ | 0.95% | orta (ihraççı değil) |
| XLP: 1990'dan beri en güçlü başlangıç | https://www.whalesbook.com/news/English/stock-investment-ideas/Barclays-Recommends-Defensive-Stocks-for-2026-Volatility/69cb9bd93f30946a72374612 | "strongest start to a year since 1990 with gains of 15.6% in the first 30 trading days" | orta |
| Takvim: WASDE 10 Aralık | https://www.usda.gov/wasde | "December 10" , 12:00 p.m. ET | yüksek |
| Takvim: ASH 12-15 Aralık; JPM 11-14 Ocak 2027 | https://www.hematology.org/meetings/annual-meeting ; https://www.biopharmadive.com/news/top-biotech-pharma-medical-conferences-2027/832075/ | "December 12–15, 2026" ; "Jan. 11-14" | yüksek |
| GIS, KR, COST bilanço tarihleri; CMS 2028 ön bildirim | — | — | doğrulanmadı (bellek) |

## Boşluk kapatma (22.11.2026)

Web aramasıyla kapatılanlar: MRNA +%177 (19 Ağustos) Merck ortaklı mRNA kanser aşısının melanom Faz 3 başarısı. Sigortacılar: 27 Ocak düşüşü CMS 2027 ön oran bildirimi (+%0,09), 7 Nisan yükselişi kesin oran (+%2,48), 18 Kasım düşüşü CMS'nin CRUSH dolandırıcılık kuralı önerisi. BSX: zayıf kılavuz (Şubat) ve Watchman durgunluğu (Mayıs). ISRG: işlem büyümesinde yavaşlama ve değerleme daralması. CURE (3x, %0,94) ve RXL (2x, ~%0,95) var. XLP gücü teknolojiden savunmacıya rotasyon. Takvim: WASDE 10 Aralık, ASH 12-15 Aralık, JPM konferansı 11-14 Ocak 2027, Şükran Günü tatili doğrulandı. Açık kalanlar: XLV gücüne özel neden kaynağı, GIS/KR/COST bilanço tarihleri, CMS 2028 ön bildirim tarihi, RXL'in ihraççıdan gider oranı.
