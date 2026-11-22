# E1 · Enerji emtiaları (WTI, Brent, benzin, dizel, doğal gaz, kömür, uranyum, karbon, elektrik)

## Özet

2026'nın enerji anlatısı ABD-İran savaşı ve Hormuz Boğazı'nın tıkanmasıdır. Savaş Şubat sonunda başladı, Brent Nisan başında zirve yaptı (vadelide 138 $ civarı, fiziki Dated Brent 144 $ üstü). Ekim'de yeniden yükseldi, Kasım'da yaklaşık beşte bir düştü. 20 Kasım'da Brent 92,57 $, WTI Aralık 83,98 $ kapattı. Ana tema arz toparlanması ve 2027 fazlası. Beklenen fiyatlar: EIA 4Ç27 için 77 $, Goldman 2027 için 88 $. Doğal gazda tablo ters: ABD'de Henry Hub 3,1–3,4 $, Avrupa'da TTF ve Asya'da JKM yaklaşık 28–30 $/MMBtu. LNG ihracatı rekor ama ılık hava fiyatı baskılıyor.

1–3 günlük vadede emtia ETF'lerinin kendi yapısı (roll, kaldıraç erimesi, iskonto) çoğu öncülük sinyalinden büyük. Hızlı yerel taramada en tutarlı bulgu şu: UNG Perşembe (depolama raporu günü) ortalamada negatif. Emtia→hisse günlük öncülüğü 2024 sonrasında büyük ölçüde kayboluyor.

## Araç tablosu

Likidite = 20 günlük ortalama günlük işlem hacmi (mn $, ozet_istatistik.csv). "(b)" = bellekten, bu oturumda doğrulanmadı.

| Emtia | Ana ETF/ETN | Yapı ve maliyet | Kaldıraçlı/ters | İlgili hisseler | Not |
|---|---|---|---|---|---|
| WTI | USO (733), DBO (17,5), USL (0,6; 12 ay merdiven); vadeli CL=F | Vadeli tabanlı LP'ler, **K-1 çıkarır**. USO yönetim ücreti ilk 1 mlr $ için %0,60. DBO toplam %0,81, net %0,75 (Invesco; feragat 31.08.2026'ya kadar yazıyor, güncel olmayabilir). 2026 backwardation (vadeli eğrinin aşağı eğimli olması) roll'u kazanca çevirdi: USO 3 yılda +%95,7, CL=F sürekli serisi +%9,5 | UCO 2x / SCO -2x (ProShares; gider %0,95; Bloomberg WTI swapları; K-1). UCO yılbaşından beri +154,6, SCO -73,8. Kaldıraçlı hisse: ERX/ERY, GUSH/DRIP | E&P: COP, OXY, DVN, FANG, APA; hizmet: SLB, HAL, OIH; XLE, XOP | Eğri contango'ya dönerse (yakın vade ucuz, uzak vade pahalı) USO/UCO yine erir. USL eğriye daha az duyarlı |
| Brent | BNO (114); BZ=F | Vadeli LP, K-1, gider ~%1 (b; ihraççı sayfası değeri JS ile yüklüyor, bulunamadı) | Doğrudan 2x Brent ETF yok (b) | XOM, CVX, SHEL, BP, TTE; tanker: FRO, DHT, INSW, TNK, STNG | Brent-WTI farkı 2026'da geniş. ABD ihracatını ve tanker ton-milini (taşınan ton × mesafe) sürüyor (EIA) |
| Benzin (RBOB) | UGA (5,3); RB=F | Vadeli LP, K-1, ~%0,97 (b). Hacim düşük | Yok | VLO, MPC, PSX, PBF, DINO, DK, PARR, CVI; CRAK | Yaz/kış kalite geçişi Şubat–Nisan güçlü, Eylül–Kasım zayıf (aşağıda) |
| Isıtma yağı/dizel | Tekil ABD ETF'i yok (UHN kapandı, b); HO=F; DBE (2,3) çoklu enerji | DBE: Invesco, K-1, toplam %0,80, net %0,75 (Invesco; feragat tarihi geçmiş olabilir) | Yok | Rafineriler (dizel ağırlıklı: DINO, PBF, VLO); havayolları ters yönde (JETS, UAL, DAL) | EIA 2026 dizel perakende 5,25 $/gal; ürün crack'leri 2027'ye kadar geniş bekleniyor |
| Doğal gaz (Henry Hub) | UNG (212), UNL (0,4; 12 ay); NG=F | Vadeli LP, K-1. UNG toplam ~%1,24 (ETFdb ve etfcentral; AAII %1,17), yönetim ücreti ilk 1 mlr $ için %0,60 (USCF). UNL ~%1,57–1,65, USL ~%1,02 (aracı siteler). Contango kaybı ağır: UNG 3 yılda -59,8, NG=F +6,9 | BOIL 2x / KOLD -2x (ProShares; %0,95; Ocak 27 NG vadelisi ~%200). BOIL 1 yılda -71,9, UNG -28,2 | EQT, EXE, AR, RRC, CNX, FCG; LNG ihracatçı: LNG, CQP, FLNG | UNG ve BOIL'u 1–3 günden uzun taşımak yapısal olarak pahalı |
| TTF / JKM | ABD'de doğrudan ETF yok; TTF=F (Yahoo) evrende yok | — | — | LNG, CQP, EQT, EXE (ihracat marjı) | AB depoları 15 Kasım'da %70,5 dolu (5 yıllık ortalama %89). 1 Ocak'ta Rus LNG yasağı başlıyor |
| Kömür | ABD'de kömür ETF'i yok: **KOL (VanEck) 2020'de tasfiye edildi (b; bu oturumda kaynak bulunamadı)**; Rotterdam vadelisi MTF=F (evrende) | — | — | Termal: BTU, ARLP, CNR; metalurjik: HCC, AMR | Metalurjik kömür çelik döngüsüne bağlı. Hızlı taramada doğal gazdan kömüre günlük öncülük yok |
| Uranyum | SRUUF (OTC, 10,1); asıl kote: TSX U.UN/U.U (SPUT); URA (164; %0,69), URNM (38,5; %0,75) | SPUT fiziki U3O8 tutar, MER %0,71, **PFIC** (pasif yabancı yatırım şirketi; ABD'de ayrı vergi formu). 20.11'de NAV'a **%20,3 iskontolu**; 3. çeyrekte 63 günün hepsi iskontoda. NAV yılbaşından beri +%9,1, SRUUF -%11,6 | Kaldıraçlı uranyum ETF'i yok (b) | CCJ, NXE, UEC, DNN, UUUU, LEU; reaktör: CEG, VST, TLN, BWXT, SMR, OKLO | URA ve URNM fiziki değil, madenci hissesidir (beta 2,2–2,4). Spot fiyat günlük bir bileşiktir (TradeTech, UxC, Platts, Numerco); borsada işlem görmez |
| Karbon izni | KRBN (0,5); KraneShares'in KEUA ve KCCA fonları (b) | Vadeli tabanlı, 1099 (K-1 yok); gider %0,91. Ağırlıklar: EUA ~%52, CCA ~%27 | Yok | ICLN, TAN (zayıf bağ) | Hacim çok düşük (günde 5–27 bin pay). Gece/gün içi ayrışması aşırı: gece -22,9, gün içi +24,0 bps/gün. **Kontrol edildi:** CSV'de bölünme, sıfır hacim ya da sıçrama yok (yalnız Aralık 2022 dağıtımı); yani klasik veri hatası değil. Ama işaret dönemle tersine dönüyor (2020–21 gece +36, gün içi −8 ile −18; 2024–26 gece −31, gün içi +24–27) ve günlerin %18,5'inde açılış = gün dibi: ince işlemde açılış fiyatının alış kotasyonundan basılmasına bağlı mikro yapı etkisi. Sinyal olarak kullanılamaz |
| Elektrik | ABD'de elektrik fiyatı izleyen ETF/ETN yok (b) | — | — | Bağımsız üreticiler: VST, CEG, NRG, TLN; XLU | Yaygın vekil doğal gaz fiyatıdır (üretimin %40'ı gaz). UNG→VST bağı hızlı taramada zayıf |

**Kapanmış ürünler:** UGAZ/DGAZ (3x gaz, Credit Suisse) son işlem günü 10 Temmuz 2020, borsa kaydı 12 Temmuz 2020'de silindi (doğrulandı). UWT/DWT'nin öncülleri UWTI/DWTI 2016'da kapandı; UWT/DWT'nin 2020'de kapandığı doğrulanmadı (bellek). iPath OIL ve GAZ, KOL ve UHN için kapanış yılı bulunamadı (bellek). Yerlerine geçenler: UCO/SCO ve BOIL/KOLD (2x). KOL'un doğrudan halefi yok. UHN'nin yerine HO=F ya da DBE kullanılır.

## İşlem saatleri ve 16:00 ET'de bilinen bilgi

| Kontrat | Günlük uzlaşma | Elektronik seans | 16:00 ET'de durum |
|---|---|---|---|
| CL (WTI) | 14:28–14:30 ET VWAP (hacim ağırlıklı ortalama fiyat). Vade günü 14:00–14:30 | Globex Pazar 18:00 – Cuma 17:00 ET, her gün 17:00–18:00 arası ara (b) | Uzlaşma kesin. 14:30–16:00 arası hareket USO'da var, CL uzlaşmasında yok |
| RB, HO, NG | 14:28–14:30 ET VWAP; vade günü 14:00–14:30 (CME) | Aynı | Kesin |
| ICE Brent | 19:28'den itibaren 2 dakikalık ortalama (Londra saati). Yılın çoğunda 14:28 ET; ABD ve İngiltere yaz saati arasındaki ~3 haftada 15:28 ET | New York 20:00 – 18:00 (ertesi gün) | Kesin |
| Uranyum spot | Günlük bileşik fiyat, borsa dışı | SPUT TSX'te 16:00 ET'de kapanır | SPUT/SRUUF fiyatı biliniyor; spot genelde günün sonunda yayınlanır (b) |
| EUA (ICE Endex) | ~17:00–18:00 CET, yani 11:00–12:00 ET (b) | — | Kesin. KRBN'in 16:00 değeri Avrupa'ya göre "bayat" kalabilir |
| Şanghay INE ham petrol | Gündüz seansı 15:00 Pekin, gece seansı 02:30 Pekin (b) | — | Önceki Asya seansı tamamen biliniyor |

Yahoo'daki `=F` serilerinin kapanışı uzlaşma fiyatı olmayabilir. Hizalama testine göre CL=F ile USO aynı gün korelasyonu 0,89, NG=F ile UNG 0,83. Sürekli seri vade geçişinde sıçrar (WTI Aralık kontratı 20 Kasım civarında sona erdi). Proje kodunda `=F` serileri SUPHELI_VADELI listesinde.

**Bu haftanın tatil düzeni:** NYSE 26 Kasım'da kapalı, 27 Kasım'da 13:00'te kapanıyor. CME 27 Kasım'da enerji TAS emirlerini (uzlaşma fiyatından işlem) normal saatte kapatıyor. 27 Kasım'da ETF'ler 13:00'te kapanırken vadeliler 14:30 sonrasına kadar işlem görüyor. Bu yüzden o gün emtia ile ETF arasında hizalama bozulur.

## 1-3 günlük sürücüler ve veri takvimi

| Açıklama | Gün / saat (ET) | 16:00'a göre |
|---|---|---|
| API haftalık stoklar | Salı ~16:30; Pazartesi (ya da Salı) tatilse Çarşamba. Perşembe tatili etkilemez, 24 Kasım normal (API) | **Sonra.** Çarşamba açılışında gap yapar, kapanış sinyaline girmez |
| EIA haftalık petrol (WPSR) | Çarşamba 10:30. Tatil haftasında Perşembe 12:00 (2026'da 12 Kasım) | Önce |
| EIA doğal gaz depolama | Perşembe 10:30. **25 Kasım 2026 Çarşamba 12:00** (Şükran Günü) | Önce |
| Baker Hughes sondaj kulesi sayısı | Haftanın son iş günü, öğlen Central saati = 13:00 ET | Önce |
| CFTC COT pozisyon raporu | Cuma 15:30, Salı verisi (b) | Önce, ama 3 gün bayat |
| Hava modelleri | GFS/ECMWF 00z ve 12z koşuları; NOAA 6-10/8-14 gün görünümü ~15:00 (b) | Hafta sonu güncellemeleri Pazartesi gap'i yaratır |
| EIA STEO aylık raporu | Ayın ilk yarısı (b) | Önce |
| OPEC+ | **29 Kasım Pazar**: 2027 kotaları | Pazartesi açılışında gap |
| Dolar, faiz, jeopolitik | Sürekli. Hormuz'daki tanker olayları 2026'nın ana şok kaynağı | — |

## 2026 durumu

- **Petrol:** EIA'ya göre Brent spot Ekim'de ortalama 124 $ oldu (Temmuz 2022'den beri en yüksek). 4 Kasım'da 100 $'ın altına indi. Orta Doğu üretim kesintileri Mayıs'taki 10,9 mn varil/gün zirvesinden Ekim'de 2,5 mn varil/güne geriledi. ABD ticari stokları Ekim sonunda 410 mn varil, 2014'ten beri en düşük ekim sonu seviyesi. Spot (Dated) ile vadeli arasındaki büyük fark sürüyor: EIA spotu ~100 $ bekliyor, ICE vadelisi 92,57 $. IEA dördüncü çeyrekte fazla görüyor.
- **Doğal gaz:** EIA kış ortalamasını (Kasım–Mart) %16 düşürerek 2,87 $'a indirdi. Depolama 3.862 Bcf (milyar fit küp; 6 Kasım), 5 yıllık ortalamanın %2 üstünde. LNG besleme gazı rekor 21,8 Bcf/gün. Spekülatif net kısa pozisyon 227 bin kontrat; ani soğuk havada short squeeze (kısa pozisyonların zorunlu kapanışıyla sert yükseliş) riski var.
- **Uranyum:** Spot yılbaşından beri yaklaşık +%13,7 (Ekim sonu itibarıyla). 16 Kasım gösterge spot ~91,50 $/lb, 52 haftalık zirve 93,42 $ (30 Ocak; MeltValue). ABD uranyum vadelisi Kasım başında 91 $ üstü, Şubat'tan beri en yüksek (Trading Economics). Hisse ve ETF tarafı çöktü: URA -37,3, CCJ -36,6, UEC -54,6. SPUT %20 iskontoda.
- **Kömür:** BTU yılbaşından beri −%48 (CSV: 29,70 → 15,47). Nedeni ağırlıkla şirkete özgü: Avustralya Centurion madeninde devreye alma sorunları (1Ç satış beklentisi ~700 bin tondan ~250 bin tona), 2Ç zararı beklentiden geniş (hisse başı −0,74 $, beklenti −0,42 $), üretim rehberi yıl içinde üç kez düşürüldü. Ilık kış ve ucuz doğal gaz da ABD termal kömür talebini zayıflatıyor.
- **Hürmüz (Kasım):** Ağustos sonunda ABD uluslararası geçiş şeritlerindeki mayınları temizledi, ama trafik savaş öncesinin çok altında kaldı; Eylül ortasında da "substantially below normal". Kasım'a ait ön gemi takip verisi geçişlerin aydan aya düştüğünü gösteriyor ve körfezde yeni çatışma haberleri var; kesin Kasım geçiş sayısı bulunamadı. EIA 3Ç26 Hürmüz akışını 9,1 mn varil/gün veriyor, rakamları sık revize ediyor.
- **Takvim:** 24 Kasım API, 25 Kasım EIA petrol (10:30) ve gaz (12:00) aynı gün, 26 Kasım kapalı, 27 Kasım yarım gün, 29 Kasım OPEC+, 1 Ocak AB'nin Rus LNG yasağı.

## Tuzaklar

1. **Roll ve kaldıraç erimesi:** UNG ve BOIL için 1–3 gün sorun değil, haftalar sorun. Backtest'te NG=F yerine UNG ya da BOIL getirisi kullanılmalı.
2. **14:30–16:00 boşluğu:** Vadeli uzlaşma ile ETF kapanışı arasındaki fark, ertesi gün ters dönüş gibi görünen sahte sinyal üretebilir. Hızlı taramada 2024 sonrası NG=F→UNG t+1 korelasyonu -0,11 (t≈-3,1). Büyük olasılıkla hizalama etkisi.
3. **Rejim:** Petrol→tanker ertesi gün negatif ilişkisi 2019+ döneminde t≈-5. 2020 çıkarılınca t≈-1,8, 2024 sonrasında sıfır. Petrol→havayolu öncülüğü hiç yok (t≈0).
4. **Mevsimsellik varsayımı yanlış:** "Kış öncesi doğal gaz yükselir" UNG'de tutmuyor. 2008–2026 aylık ortalamada Ekim -4,7, Kasım -1,1, Aralık -8,5. Nedeni contango ve ılık kış riski.
5. **SPUT iskontosu:** SRUUF spot uranyumu izlemiyor (2026'da 20 puan ayrıştı).
6. Bütün ABD emtia LP'leri K-1 çıkarır. Düzenli kısa vadeli işlemde vergi işi ağırlaşır.

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| CL günlük uzlaşma penceresi | https://www.cmegroup.com/confluence/display/EPICSANDBOX/NYMEX+Crude+Oil | "14:28:00 to 14:30:00 ET for the Active Month" | yüksek |
| CL vade günü uzlaşması | aynı | "VWAP of the outright CME Globex trades executed between 14:00:00 and 14:30:00 ET" | yüksek |
| ICE Brent uzlaşma saati | https://www.ice.com/products/219/Brent-Crude-Futures | "two minute settlement period from 19:28:00, London time" | yüksek |
| ICE Brent işlem saatleri | aynı | "NEW YORK 8:00 PM - 6:00 PM*" | yüksek |
| EIA WPSR standart saat | https://www.eia.gov/petroleum/supply/weekly/schedule.php | "10:30 a.m. eastern time on Wednesday" | yüksek |
| Gaz depolama Şükran Günü kayması | https://ir.eia.gov/ngs/schedule.html | "November 25, 2026 Wednesday 12:00 p.m. Thanksgiving Day" | yüksek |
| Baker Hughes yayın saati | https://rigcount.bakerhughes.com/ | "released weekly at noon Central Time on the last day of the work week" | yüksek |
| NYSE 27 Kasım erken kapanış | https://www.nyse.com/markets/hours-calendars | "close early at 1:00 p.m. ... on Friday, November 27, 2026" | yüksek |
| UCO gider, NAV saati | https://www.proshares.com/our-etfs/leveraged-and-inverse/uco | "Expense Ratio 0.95% NAV Calculation Time 2:30 p.m. ET" | yüksek |
| BOIL 2x, Ocak 27 NG | https://www.proshares.com/our-etfs/leveraged-and-inverse/boil | "199.96% -- NATURAL GAS FUTR JAN27" | yüksek |
| USO yönetim ücreti | https://www.uscfinvestments.com/uso | "Management fee for first $1,000,000,000 is 0.60% of NAV" | yüksek |
| URA %0,69, URNM %0,75 | https://www.etfcentral.com/compare-etfs/URA-vs-URNM | URA TER 0.69%, URNM 0.75% (arama özeti) | orta |
| KRBN gider %0,91, K-1 yok | https://etfdb.com/etf/KRBN/ | 0.90–0.91%; "Distributes K1 No" (arama özeti) | orta |
| SPUT iskonto ve NAV | https://sprott.com/investment-strategies/physical-commodity-funds/uranium/ | "NAV YTD Change 9.11% ... Premium / Discount -20.27%" | yüksek |
| SPUT PFIC, MER | aynı | "all Sprott Physical Trusts are considered PFICs"; MER 0.71% | yüksek |
| Brent Ekim ortalaması 124 $ | https://www.eia.gov/outlooks/steo/pdf/steo_full.pdf | "increased to an average of $124 per barrel (b) in October" | yüksek |
| Brent 4Ç27 tahmini | aynı | "gradually fall to an average of $77/b in the fourth quarter of 2027" | yüksek |
| ABD stokları 2014'ten beri en düşük | aynı | "fell to 410 million barrels at the end of October, the lowest end-of-October level since 2014" | yüksek |
| Kesintiler zirveden geriledi | aynı | "averaged 2.5 million barrels per day (b/d) in October, down from 10.9 million b/d at the peak in May" | yüksek |
| Kış Henry Hub tahmini | aynı | "average $2.87 per million British thermal units from November through March, 16% lower" | yüksek |
| Brent 20.11 uzlaşması, OPEC+ 29.11 | https://financefeeds.com/brent-crude-oil-price-92-57-saturday-week-ahead-opec-plus-29-november-bull-96-bear-89/ | "Brent settle: $92.57 on Friday 20 November"; "all members meet on 29 November" | yüksek |
| Brent Kasım'da beşte bir düştü | aynı | "Brent has fallen about a fifth in November as Middle East supply recovered" | orta |
| Savaş zirvesi | https://en.majalla.com/node/332465 | Brent "$138 a barrel on 7 April" (arama özeti) | orta |
| LNG besleme rekoru, net kısa pozisyon | https://www.tradingnews.com/news/december-natural-gas-holds-3-103-as-record-21-8-bcf-d-lng-meets-warm-weather-3-40-usd-in-play | "LNG feedgas at a record 21.8 Bcf/d and a speculative net short position of 227,227 contracts" | orta |
| AB depoları düşük, Rus LNG yasağı | https://theenergynewsbeat.substack.com/p/two-gas-markets-this-winter-about | "70.5 percent full on Nov. 15, against a five-year average of 89 percent" | orta |
| ABD depolama | aynı | "3,862 billion cubic feet in the week ending Nov. 6, 2.0 percent above the five-year average" | orta |
| Aykırı: vadeli petrolle öngörü zayıf | https://economics.ecu.edu/wp-content/pv-uploads/sites/165/2019/07/ECU0912.pdf | "statistical support for predictability based on changes in oil future prices is weak" | yüksek |
| Petrol etkisi 7–8 gün gecikmeli | aynı | "between seven and eight trading days" | yüksek |
| UNG Perşembe etkisi (yerel tarama) | veri/panel_adjclose.parquet (betik: scratchpad tara2.py) | Perşembe ort. bps: 2008-13 -40 (t-2,1), 2014-18 -18, 2019-23 -33, 2024+ -36 (t-1,4) | orta (yerel) |
| USO-USL eğim vekili → USO t+1 | aynı | 2019+ c=0,078 t=3,5; 2024+ t=0,5 | orta (yerel) |
| RB, HO, NG uzlaşması 14:28–14:30 ET | https://www.cmegroup.com/trading/energy/files/NYMEX_Energy_Futures_Daily_Settlement_Procedure.pdf | "VWAP ... executed between 14:28:00 and 14:30:00 ET" (arama özeti; belge 2015–19) | yüksek |
| API Salı ~16:30 ET | https://www.api.org/energy-insights/statistics/wsb | "every Tuesday afternoon at approximately 4:30 pm Eastern" (arama özeti) | yüksek |
| API Pazartesi tatilinde Çarşamba | aynı | "If Monday is a Federal holiday, the reports are scheduled for release on Wednesday afternoon" | yüksek |
| DBO %0,81/0,75, DBE %0,80/0,75 | https://www.invesco.com/us/en/solutions/invesco-etfs/commodity-investing.html | DBE 0.80% total, 0.75% net; DBO 0.81% / 0.75% (arama özeti) | orta |
| UNG ~%1,24; UNL %1,57; USL %1,02 | https://www.etfcentral.com/compare-etfs/UNG-vs-UNL ; https://www.etfcentral.com/compare-etfs/UNG-vs-USL | UNG 1.24%, UNL 1.57%, USL TER 1.02% (aracı site; AAII UNG 1.17%) | orta |
| UNG yönetim ücreti %0,60 | https://www.uscfinvestments.com/ung | "Management fee for first $1,000,000,000 is 0.60% of NAV" | yüksek |
| UGAZ/DGAZ son işlem 10.07.2020 | https://seekingalpha.com/article/4355199-goodbye-ugaz-and-dgaz-interesting-ride | "last day of trading set to occur on July 10th, 2020" (arama özeti) | yüksek |
| Uranyum gösterge spot ~91,50 $/lb (16.11) | https://meltvalue.com/uranium-price | "At $91.50 on Nov 16, 2026 ... 52-week high of $93.42, set Jan 30" (arama özeti) | orta |
| BTU: Centurion üretim kesintisi | https://stocktwits.com/news-articles/markets/equity/btu-stock-tumbles-australian-mine-production-cut/cZERwYxRIN1 | 1Ç satış ~250K ton vs ~700K beklenti (arama özeti) | orta |
| BTU: rehber üç kez düşürüldü; 18.11 kapanış 16,99 $ | https://fool.com/investing/2026/11/18/why-peabody-energy-stock-slumped-today | "production outlook ... cut three times so far this year" (arama özeti) | orta |
| BTU YBB −%48 | yerel: veri/ham/BTU.csv | 31.12.2025 29,70 → 20.11.2026 15,47 | yüksek |
| Hürmüz: mayınlar temizlendi, trafik savaş öncesinin altında (Ağustos) | https://news.usni.org/2026/08/28/strait-of-hormuz-tanker-transits-up-but-still-below-pre-war-levels | "remains a shadow of what it was prior to the U.S.-Iran war" (arama özeti) | orta |
| Hürmüz: Eylül ortası normalin çok altında | https://gulfnews.com/business/energy/hormuz-tanker-traffic-shows-signs-of-recovery-but-gulf-oil-flows-remain-far-below-normal-1.500674751 | "substantially below normal levels" (arama özeti) | orta |
| Hürmüz: Kasım'da geçişler aydan aya düşüyor (ön veri) | https://www.energyconnects.com/news/oil/2026/november/oil-edges-lower-despite-gulf-flare-ups-as-traders-shun-risk/ | "showing signs of falling month-on-month, preliminary vessel-tracking data" (arama özeti; kaynağı kesin eşleşmedi) | düşük |
| KRBN gece/gün içi ayrışması mikro yapı etkisi | yerel: veri/ham/KRBN.csv | 2020–21 gece +36 bps; 2024–26 gece −31; açılış=dip 294/1586 gün | orta |

## Boşluk kapatma (22.11.2026)
- Doğrulandı: RB/HO/NG uzlaşması 14:28–14:30 ET (CME); API Salı ~16:30 ET, Pazartesi tatilinde Çarşamba; UGAZ/DGAZ Temmuz 2020'de kapandı.
- Düzeltildi: DBO ~%0,77 → %0,81 toplam/%0,75 net; DBE ~%0,77 → %0,80/%0,75; UNG ~%1,06 → ~%1,24 (aracı site). USL ~%1,02, UNL ~%1,57 eklendi.
- Eklendi: uranyum spot ~91,50 $/lb (16.11); BTU −%48'in nedeni (Centurion üretim sorunları, zarar, rehber kesintileri); Hürmüz Kasım durumu (trafik hâlâ normalin altında, kesin sayı yok).
- KRBN: veri hatası değil, ince işlemde açılış fiyatı kaynaklı mikro yapı etkisi; işareti dönemle değişiyor, kullanılamaz.
- Bulunamadı: BNO ve UGA gideri, iPath OIL/GAZ, KOL, UHN ve UWT/DWT kapanış yılları.
