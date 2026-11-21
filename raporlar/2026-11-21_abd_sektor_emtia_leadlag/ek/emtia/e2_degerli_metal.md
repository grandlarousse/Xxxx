# E2 · Değerli metaller (altın, gümüş, platin, paladyum)

## Özet

Dört metal 2026'da aynı döngüyü yaşadı: Ocak sonunda zirve (altın ~5.590 $, gümüş 121,65 $), 30 Ocak–2 Şubat'ta çöküş (CME teminat artışı, Warsh'ın Fed başkanlığına aday gösterilmesi), sonra yıl boyu düşüş. Kasım 2026'da ana anlatı, Fed'in Aralık'ta faiz **artıracağı** beklentisi (olasılık %90'ın üstünde), güçlü dolar ve yüksek reel faiz. Yılbaşından beri getiriler (ozet_istatistik.csv): GLD -18,5, SLV -42,6, PPLT -37,0, PALL -44,3, GDX -20,3. Talep tarafı hâlâ güçlü (3. çeyrekte merkez bankaları 321 t, ETF girişi 211 t).
1-3 günlük işlem için kullanılabilir yön şudur: altın ve gümüşteki hareket ABD seansında satış, Asya seansında alım şeklinde ayrışıyor. GLD'nin 3 yıllık ortalama gece getirisi günde +9,7 bps, gün içi getirisi -1,4 bps. Altından madencilere ya da altından gümüşe giden günlük öncülük kanıtı zayıf. Yerel ön hesapta altın getirisi ertesi günkü madenci getirisiyle hafif **negatif** ilişkili (tersine dönme).

## Araç tablosu

| Emtia | Ana ETF/ETN | Yapı ve maliyet | Kaldıraçlı/ters | İlgili hisseler | Not |
|---|---|---|---|---|---|
| Altın | GLD (3.668 mn $/gün), IAU (441), GLDM (395), SGOL (113); vadeli GC=F | Hepsi fiziki külçe trast. Gider oranı: GLD %0,40, IAU %0,25, SGOL %0,17, GLDM %0,10. Roll maliyeti ve contango yok. K-1 yok; ABD mukimi için "collectible" vergisi (en çok %28, bellek). | UGL 2x / GLL -2x (ProShares, Bloomberg Gold Subindex; vadeli + swap; **K-1 çıkarır**). Madenci: NUGT/DUST 2x/-2x GDX, JNUG/JDST 2x/-2x GDXJ | GDX (2.197 mn $), GDXJ (560), RING, GOAU; NEM (844), AEM, B, AU, KGC, GFI, WPM, FNV, RGLD (royalty: düşük beta) | Kısa vade için en likit araç GLD. Taşıma maliyeti öncelikliyse GLDM. Gümüşte 1-3 gün için de UGL'nin vadeli olmasından gelen roll etkisi küçük. |
| Gümüş | SLV (963), SIVR (115); SI=F | Fiziki. SLV %0,50, SIVR %0,30. K-1 yok, collectible vergisi. | AGQ 2x (173 mn $) / ZSL -2x (92); vadeli + swap, **K-1** | SIL, SILJ, SLVP; PAAS, HL, CDE, AG, EXK, SSRM, WPM | Oynaklık altının yaklaşık 1,7 katı (60 günlük yıllık oynaklık %42,5, AGQ %86). Kaldıraç kaybı (volatility decay) yüksek; 1-3 günde küçük, haftalarda büyük. |
| Platin | PPLT (30 mn $); PL=F (Ocak 27 kontratı) | Fiziki, %0,60. K-1 yok. | **UPLT** 2x (ProShares, 21 Nisan 2026'da açıldı, **K-1'siz, 1099**, LBMA Platinum PM endeksi, toplam gider %1,04). Ters ürün yok. | SBSW (52 mn $), PLG (mikro, 1,2 mn $: işlem dışı); Implats/Northam ABD'de OTC | Likidite düşük: PPLT'de spread maliyeti dikkate alınmalı. UPLT evrende yok. |
| Paladyum | PALL (22 mn $); PA=F | Fiziki, %0,60 (tek kaynak). K-1 yok. | **UPAL** 2x (ProShares, 21 Nisan 2026, K-1'siz). Ters ürün yok. | SBSW (Stillwater, ABD'de üretim) | Rusya'dan ithal ham paladyuma ABD'de damping soruşturmasında kesin olumlu karar çıktı (Mayıs 2026). Vergi oranı görülmedi. |

Kapanan ürünler: eski iPath ETN'leri (JJP/PGM gibi platin ve paladyum ETN'leri) ile DB/PowerShares kaldıraçlı değerli metal ETN'leri (DGP/DZZ) artık işlem görmüyor (bellek, doğrulanmadı). Yerlerine geçenler: platin ve paladyumda UPLT/UPAL, altında UGL/GLL. Evrende olmayan fiziki alternatifler: AAAU, BAR, OUNZ; Sprott PHYS/PSLV/SPPP (kapalı uçlu, NAV'a primle ya da iskontoyla işlem görür).

## İşlem saatleri ve 16:00 ET'de bilinen bilgi

| Olay | Saat (ET, kış) | 16:00 ET'de biliniyor mu |
|---|---|---|
| SGE gece seansı biter (02:30 Pekin) | ~13:30 ET, önceki gün | Evet |
| SGE gündüz seansı biter (15:30 Pekin) | ~02:30 ET | Evet |
| LBMA AM / PM altın müzayedesi (10:30 / 15:00 Londra) | 05:30 / 10:00 ET (ABD ile İngiltere'nin yaz saati farklı olduğu haftalarda 1 saat kayar) | Evet. Fiziki ETF'lerin NAV'ı LBMA PM'ye dayanır (bellek) |
| COMEX paladyum / platin uzlaşması | ~13:00 / ~13:05 ET (tatil takviminden çıkarım) | Evet |
| COMEX gümüş uzlaşması | 13:24–13:25 ET (eski CFTC belgesi) | Evet |
| COMEX altın uzlaşması | 13:29–13:30 ET (Ocak 2026'dan beri Ekim de aktif ay) | Evet |
| ABD hisse ve ETF kapanışı | 16:00 ET | Karar anı |
| Globex metal seansı biter | 17:00 ET | **Hayır**: 16:00–17:00 arası vadeli hareketi ertesi günün bilgisidir. Yahoo GC=F/SI=F/PL=F/PA=F çubukları 1 gün gecikmeli kullanılmalı (ortak.py böyle yapıyor) |

16:00 ET'de uzlaşma fiyatları ile Londra ve Şanghay'ın kapanış fiyatları kesinleşmiş olur. Vadeli piyasa 17:00'ye kadar işlem görmeye devam eder.

## 1-3 günlük sürücüler ve veri takvimi

- **Faiz ve Fed (en güçlü sürücü, Kasım 2026):** Aralık'ta artırım beklentisi, 10 yıllık getiri (^TNX), reel faiz (TIP). Yerel ön hesapta (2012 sonrası, maliyetsiz) TIP'in t günü getirisi ile metallerin ve madencilerin t+1 getirisi arasındaki korelasyon +0,05 ile +0,08 arasında. En tutarlı ön sinyal bu; testi gerekiyor.
- **Dolar:** DXY Nisan 2025'ten beri en güçlü seviyesinde. UUP 16:00'da biliniyor; DX-Y.NYB 1 gün gecikmeli.
- **Takvim (kapanıştan önce mi):** İstihdam raporu 4 Aralık 08:30, FOMC kararı **9 Aralık 14:00** (basın toplantısı 14:30), TÜFE 10 Aralık 08:30, ÜFE 15 Aralık 08:30. Hepsi kapanıştan **önce** açıklanır. CFTC COT raporu Cuma 15:30 ET'de çıkar (bellek; ertesi günün bilgisi sayılmalı). WGC Gold Demand Trends çeyreklik yayımlanır (3. çeyrek raporu 3 Kasım'da çıktı), WPIC Platinum Quarterly de çeyreklik.
- **Seans ayrışması:** StoneX'e göre Eylül başından bu yana altın Asya saatlerinde %2,7 yükseldi, ABD seansında %12,2 düştü. WGC'nin 1. yarı verisi de aynı yönde (Asya +%12,9, Kuzey Amerika -%15).
- **Risk iştahı ve likidasyon:** Kasım'da teknoloji hisselerindeki satış metalleri de aşağı çekti (corr_spy: GLD 0,39, GDX 0,50). Hisse satışında teminat çağrısıyla metal satışı geliyor.
- **Ticaret politikası:** Section 232 kritik mineral tarifesi Ocak 2026'da ertelendi; liste platin, paladyum ve gümüşü kapsıyor. COMEX stokları ile EFP primi (vadeli ile fiziki arasındaki fark) tarife haberlerine hızlı tepki veriyor.
- **Gümüş/altın oranı:** 16 Kasım'da tek seansta 79,7'den 82,2'ye çıktı. Gümüş hem yükselişte hem satışta altından sert hareket ediyor. Uzun vadede oran ortalamaya dönüyor (Silver Institute), ancak 1-3 günlük kanıt yok.

## 2026 durumu

- Altın: 28-29 Ocak'ta ~5.590 $ ile rekor kırdı. Mart'ta ~4.100 $'a geriledi ("43 yılın en kötü ayı"). 20 Kasım'da 3.558 $'a indi ("Mart'tan beri en kötü hafta"). Goldman yıl sonu hedefini 4.150 $'a düşürdü; JPMorgan 6.300 $ hedefini koruyor.
- Gümüş: rekordan yaklaşık %61 aşağıda. Silver Institute 2026 için üst üste altıncı yıl arz açığı öngörüyor.
- Platin ve paladyum: zirveden -53 ile -59 arası (csv). Rusya'ya yönelik damping kararı ABD'deki paladyum fiyatını destekleyen bir unsur.
- Talep: 3. çeyrekte merkez bankaları 321 t aldı (+%42), ETF'lere 211 t giriş oldu. Fiyat düşüşünü fiziki talep değil faiz yönlü vadeli ve kâğıt satış sürüyor.
- Önümüzdeki haftalar: 4 Aralık istihdam, 9 Aralık FOMC (artırım bekleniyor), 10 Aralık TÜFE. Aralık COMEX altın vadesi sona yaklaşıyor; aktif ay Şubat'a (G) geçiyor ve bu Yahoo'nun sürekli serisinde sıçrama yaratabilir. ^GVZ 34,8 (yılbaşından +%45): oynaklık yüksek.

## Tuzaklar

- Altından madencilere öncülük **aynı gün** gerçekleşir; ertesi güne taşan bir etki ön hesapta görülmedi (korelasyon -0,03 ile -0,06). Wavelet çalışması da kısa vadede ilişkinin zayıf olduğunu söylüyor.
- Altından gümüşe günlük Granger nedenselliği kanıtı karışık. Etki çift yönlü ya da eşzamanlı.
- GC=F gibi vadelilerin günlük çubuğu 17:00'de kapanır; aynı gün sinyali olarak kullanılırsa ileriye bakış hatası (look-ahead) olur.
- Yahoo'nun sürekli vadeli serisi roll günlerinde sıçrar. Getiri için ETF kullanılmalı.
- Kaldıraçlı ürünler: AGQ/UGL/GLL K-1 çıkarır, UPLT/UPAL çıkarmaz. 1-3 gün için kaldıraç kaybı küçük ama oynak günlerde sapma büyür.
- Fiziki ETF'ler ABD mukimi için collectible vergisine tabidir (kullanıcı mukim değilse farklı olabilir).
- PPLT, PALL ve SBSW'nin likiditesi düşük. Mikro hisseler (PLG) dışarıda bırakılmalı.
- Mevsimsellik (Ocak etkisi, Kasım–Şubat gücü) aylık bir olgu. 1-3 günlük işlem için zayıf ve oynak; WGC ve Perth Mint de zamanlama riskine karşı uyarıyor.
- FOMC sonrası 3 günde altın ETF'lerinin ortalama -%0,50 getirisi eski ve küçük bir örneklem (2014 sonrası, Kensho).

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| GLDM, SGOL, IAU ve GLD gider oranları | https://247wallst.com/investing/2026/07/05/gold-is-up-again-in-2026-and-after-reviewing-every-way-to-own-bullion-these-3-etfs-cover-the-trade-at-three-cost-levels/ | GLDM 0.10%, SGOL 0.17%, IAU 0.25%, GLD 0.40% (arama özeti) | orta |
| SIVR ve SLV gider oranı | https://www.etf.com/sections/etf-education-series/top-10-precious-metals-etfs-silver-and-platinum-shine | SIVR 0.30%; SLV 0.50% (arama özeti, fool.com ile uyumlu) | orta |
| PPLT ve PALL gider oranı | https://www.fool.com/coverage/etfs/2026/01/17/sivr-vs-pplt-riding-silver-and-platinum-s-explosive-2025-rally | PPLT 0.60%; PALL 0.6% (etfcentral, tek kaynak) | orta |
| AGQ 2x, vadeli + swap | https://www.proshares.com/our-etfs/leveraged-and-inverse/agq | "AGQ invests in futures and swap and does not directly invest in silver." | yüksek |
| UGL 2x Bloomberg Gold Subindex, vadeli + swap | https://www.proshares.com/our-etfs/leveraged-and-inverse/ugl | "two times (2x) the daily performance of the Bloomberg Gold Subindex" | yüksek |
| AGQ ve GLL K-1 çıkarır | https://www.proshares.com/resources/tax-and-filing-documents/k-1s-form-1065 | AGQ ve GLL K-1 üreten fonlar listesinde (arama özeti) | orta |
| UPLT/UPAL 2x, 21 Nisan 2026, K-1'siz | https://www.proshares.com/press-releases/proshares-launches-first-etfs-targeting-2x-daily-returns-of-platinum-and-palladium | "K-1 Free"; UPLT toplam gider 1.04% (etfcentral) | orta |
| COMEX altın uzlaşma penceresi | https://www.cmegroup.com/content/dam/cmegroup/notices/ser/2026/06/ser-9637r.pdf | "13:29:00 to 13:30:00 Eastern Time/ET for the active month" | yüksek |
| Altında Ekim de aktif ay (12 Ocak 2026'dan beri) | https://www.cmegroup.com/content/dam/cmegroup/notices/ser/2025/12/ser-9637.pdf | "add the October contract month as a lead month indicator" | yüksek |
| Gümüş uzlaşma penceresi | https://www.cftc.gov/filings/orgrules/rules0815235374.pdf | "between 13:24:00 and 13:25:00 Eastern Time" (eski belge, arama özeti) | orta |
| Platin ve paladyum uzlaşma saati | https://www.cmegroup.com/tools-information/holiday-calendar/files/2025/christmas-holiday-settlement-times-2025.pdf | Tatil: Palladium 12:00, Platinum 12:05; normal gün +1 saat çıkarımı | düşük |
| SGE seansları | https://en.sge.com.cn/eng_trading_ProductsIntroduce | gündüz 9:00–15:30, gece 20:00–2:30 (arama özeti) | orta |
| LBMA müzayede saatleri | https://www.lbma.org.uk/prices-and-data/about-lbma-daily-auction-prices | auction 10:30 and 15:00 London (arama özeti) | orta |
| Aralık 2026 BLS takvimi | https://www.bls.gov/schedule/2026/12_sched.htm | "Employment Situation November 2026 08:30 AM" 4 Ara; CPI 10 Ara 08:30; PPI 15 Ara | yüksek |
| FOMC 8-9 Aralık 2026 | https://www.federalreserve.gov/newsevents/2026-december.htm | December 8 - 9 (arama özeti; karar 14:00 ET) | orta |
| Aralık artırım olasılığı %90'ın üstünde, Fed başkanı Warsh | https://www.usagold.com/daily-precious-metals-market-report-november-16-2026/ | "CME FedWatch pricing puts the odds of a December hike above 90%" | yüksek |
| 16 Kasım'da oran 79,7'den 82,2'ye çıktı | https://www.usagold.com/daily-precious-metals-market-report-november-16-2026/ | "The gold-silver ratio jumped to 82.2 from 79.7" | yüksek |
| Gümüş rekoru 121,65 $ (26 Ocak) | https://www.usagold.com/daily-precious-metals-market-report-november-16-2026/ | "roughly 61% below its January 26 record of $121.65" | yüksek |
| 20 Kasım'da altın 3.558 $ | https://www.usagold.com/daily-precious-metals-market-report-november-16-2026/ | "Gold Slides to $3,558 as Fed Hike Bets Drive Worst Week Since March" | yüksek |
| Ocak sonu çöküşü: CME teminat artışı | https://aljazeera.com/economy/2026/2/3/gold-and-silver-prices-soared-then-plummeted-whats-going-on | CME margin 6% -> 8%; altın ~-10%, gümüş ~-28% (arama özeti) | orta |
| Asya alıyor, ABD satıyor (Eyl–Kas 2026) | https://www.stonex.com/en-gb/news-and-analysis/gold-outlook-asia-buys-the-dip-us-hammers-the-rip-2026-11-16/ | Asya +2.7%, Avrupa -2.5%, ABD seansı -12.2% (arama özeti; sayfa 403) | orta |
| WGC 1. yarı 2026 seans ayrışması | https://www.moneymetals.com/news/2026/07/12/a-strange-dichotomy-gold-up-on-the-year-in-asian-markets-down-big-in-the-west-005059 | Asya +12.9%, Kuzey Amerika -15% (arama özeti) | orta |
| 3. çeyrek: merkez bankası 321 t, ETF 211 t | https://www.gold.org/sites/default/files/downloads/2026-11/Gold-Demand-Trends-Q3-2026.pdf | 321t (+42% y/y); ETF inflows 211t (arama özeti) | orta |
| Rus paladyumuna damping kararı | https://www.federalregister.gov/documents/2026/05/01/2026-08487/unwrought-palladium-from-the-russian-federation-final-affirmative-determination-of-sales-at-less | "final affirmative determination of sales at less than fair value" | yüksek |
| Section 232 tarifesi ertelendi | https://www.thompsonhinesmartrade.com/2026/01/no-section-232-tariff-now-on-processed-critical-minerals-and-their-derivative-products/ | 14 Ocak 2026: tarife "for now" yok (arama özeti) | orta |
| Altın ile madenciler arasında kısa vadede ilişki zayıf (aykırı kanıt) | https://informahealthcare.com/doi/abs/10.1080/13504851.2016.1164813 | "little relationship in the short run"; uzun vadede altın öncü (arama özeti) | orta |
| Altın ile gümüş arasında nedensellik çift yönlü ya da eşzamanlı (aykırı kanıt) | https://www.doi.org/10.1016/j.resourpol.2017.12.008 | "bi-directional causality in mean and variance" (arama özeti) | orta |
| Altında Ocak etkisi | https://gold.org/goldhub/gold-focus/2023/12/you-asked-we-answered-is-there-a-january-effect-for-gold | Ocak ortalaması ~1.79% (1971'den beri) (arama özeti) | orta |
| FOMC sonrası 3 günde altın ETF'lerinde ortalama -%0,50 | https://ca.finance.yahoo.com/news/why-gold-yanked-around-fed-175313734.html | "negative by on average 0.50 percent in the three days after" (arama özeti) | düşük |
| Fiziki ETF'ler collectible vergisine tabi (en çok %28) | — | doğrulanmadı (bellek) | düşük |
