# S5 · Sanayi ve kamu hizmetleri

## Özet

Grup Kasım 2026'da iki ayrı rejimde: (1) "yapay zekâ gücü ve altyapısı" (GEV, VRT, ETN, PWR, CAT, VST, CEG, BE, STRL) 5 Kasım'dan beri çip satışının sanayiye yayılmasıyla sert düşüşte (CAT 3 ayda -36,9%, STRL -50%, VRT -34,8%); (2) savunmacı kamu hizmetleri (XLU, DUK, SO, ED, AWK) zirveye yakın ve SPY ile korelasyonu sıfıra yakın. Tankerler İran/Hürmüz şokuyla yılbaşından beri +60–140% (FRO +138%). Savunma, 1,5 trilyon $ bütçe önerisine rağmen 3 ayda geriledi (ITA -14,8%, DFEN -42%). 1-3 günlük işlem için en temiz araçlar: XLI, XLU, ITA, PAVE, GRID ve likit hisseler. Denizcilik ETF'leri (SEA, BOAT, BDRY) çok sığ. En umut veren öncüler: NVDA/SMH -> güç sepeti, büyük -> küçük yüklenici, petrol -> tanker, doğal gaz -> IPP, faiz -> XLU. Literatür, gecikme etkilerinin işlem maliyetinden sonra çoğunlukla kaybolduğunu söylüyor. Bu yüzden her sinyal maliyet dahil test edilmeli.

## Araç tablosu

Sayılar `ozet_istatistik.csv` dosyasından alındı. h20 = 20 günlük ortalama işlem hacmi (milyon $), σ1g = günlük oynaklık (%), β = SPY betası.

| Alt sektör | Ana ETF | Kaldıraçlı / ters | Öncü hisseler | Yüksek betalı takipçiler | Not |
|---|---|---|---|---|---|
| Havacılık ve savunma | ITA (h20 188, σ1g 1,53); XAR (74; eşit ağırlıklı, β 1,40); PPA (42) | DFEN 3x (h20 14,5; gider oranı 2017'de %0,95 net); likit ters ETF yok | GE (1570), BA (1838), RTX (1042), LMT (909), HWM (903), NOC (490), GD (459), LHX (497) | KTOS (σ1g 4,47), AVAV (4,94), AXON (4,08), BAH, LDOS, HII | Ana savunma şirketlerinin (LMT, NOC, GD) β'sı ~0: piyasadan bağımsız ve olaya duyarlı. DFEN eşiğin altında. |
| Taşımacılık | IYT (72); XTN (6,4, sığ) | Likit kaldıraçlı ETF yok | UNP (878), UPS (661), CSX (596), FDX (484), ODFL (396), NSC (386) | XPO (σ 2,60), SAIA (2,93), CHRW (2,78), KNX, JBHT | Demiryolları düşük β (0,3) ve düşük σ. Kamyonculukta oynaklık daha yüksek. |
| Denizcilik | Uygun ETF yok: SEA 0,6, BOAT 10,2, BDRY 0,5 (gider oranı %3,50) | Yok | FRO (190), DHT (117), STNG (77), INSW (75), MATX (74) | TNK (47), ZIM (40, σ 3,09), SBLK (39), DAC (25), GNK (18) | Kuru yük hisseleri (SBLK, GNK) eşiğin altında. Tanker teması en likit olanı. |
| Makine, inşaat, elektrifikasyon | XLI (1536, σ 1,17); PAVE (111); GRID (108) | DUSL 3x XLI (gider oranı %0,97), UXI 2x, SIJ -2x (üçü de evrende yok; likidite doğrulanmadı) | GEV (3625), CAT (2453), ETN (1177), PWR (982), FIX (886), DE (798), CMI (783), URI (593) | STRL (σ 5,96), PRIM (5,30), MTZ (3,66), DY (3,52), EME, VRT (4,53) | Yapay zekâ altyapısı alt grubu (GEV, VRT, PWR, STRL) NVDA ile birlikte hareket ediyor (β_qqq 1,2–2,3). |
| Kamu hizmetleri ve bağımsız elektrik üreticileri (IPP) | XLU (1071, σ 1,00, β 0,13) | UTSL 3x (net gider %0,97), SDP -2x (evrende yok) | NEE (1091), SO (805), XEL (755), DUK (668), AEP (550), CEG (1015), VST (845) | TLN (σ 3,68), NRG (3,32), BE (7,02), PCG (2,20), EIX (2,30) | İki ayrı kova: düzenlenmiş şirketler (β < 0,1) ve IPP'ler (β 1,3–1,8). Bunlar karıştırılmamalı. |
| Uzay ve tematik yüksek beta | UFO (9,7, sığ) | Yok | RKLB (1058), IONQ (681), ASTS (622), TEM (485), OKLO (252) | RGTI, QBTS, LUNR, SMR, JOBY, ACHR (σ1g 4,3–7,3) | Hepsi 1 yıllık zirvesinden -65% ile -85% aşağıda. SpaceX halka arzı sonrası fon bu hisselerden SpaceX'e kaydı. |

## 1-3 günlük sürücüler ve öncü göstergeler

Ayrıntı ve test tanımları için: `ek/hipotez/s5_sanayi_kamu.json` (22 hipotez).

- **Yapay zekâ gücü sepeti (GEV, VRT, ETN, PWR, VST, CEG, CAT):** Ana sürücü NVDA, SMH ve hiper ölçekli şirketlerin yatırım haberleri. 5 Kasım'da satış çip ve depolama hisselerinden (WDC -17%) VRT (-14%), PWR (-12%) ve CAT (-6%) hisselerine geçti. 9 Kasım'da CEG bilançosu sepeti birlikte yükseltti. Bilgi 16:00 ET'de biliniyor. Etkinin aynı gün mü yoksa t+1'de mi gerçekleştiği test edilmeli.
- **Büyük -> küçük öncülüğü:** GEV, ETN ve PWR'nin hareketi STRL, PRIM, MTZ ve DY'ye gecikmeli geçebilir. Uluslararası kanıta göre bu etki sürüyor ama tek yön işlem maliyeti 40 baz puanı aşınca anlamlılığını yitiriyor.
- **Bağımsız elektrik üreticileri (IPP):** Doğal gaz (NG=F) toptan elektrik fiyatını belirliyor. Spark spread (elektrik fiyatı ile gaz maliyeti arasındaki fark) TLN'nin kârını açıkça artırdı. PJM kapasite ihalesi üç kez fiyat tavanında (325 $/MW-gün) kapandı; 2029/30 ihalesi 9 Aralık 2026'da açılıyor. EIA gaz depolama raporu perşembe 10:30 ET'de çıkıyor (bellek).
- **Düzenlenmiş kamu hizmetleri:** 10 yıllık faiz (^TNX, şu an %4,91, yılbaşından beri +18%) ters yönde etkiliyor. Etki çoğunlukla aynı gün fiyatlanıyor; kalıntı t+1 etkisi zayıf olabilir. Volatilite artınca savunmacı rotasyon da XLU'yu destekliyor.
- **Tankerler:** Brent ve WTI ile Hürmüz haberleri. VLCC (çok büyük ham petrol tankeri) navlunu 2026'da günlük 470–600 bin $'a çıktı. Petrol 14:30 ET'de uzlaşıyor, yani kapanışta biliniyor.
- **Kuru yük:** Baltık endeksleri ve FFA değerlemeleri (Londra 17:30 = 12:30 ET) ABD kapanışından önce biliniyor. Kanıt zayıf ve aylık veriye dayanıyor: hakemli bir çalışma, kuru yük hisselerine Baltık endeksinin değil emtia fiyatlarının öncülük ettiğini buldu. Demir cevheri (TIO=F) ve Şanghay endeksi alternatif öncüler. Şanghay ABD açılışından önce kapanıyor.
- **Konteyner:** Maersk (Kopenhag 11:00 ET kapanış) -> ZIM, MATX, DAC.
- **Savunma:** Avrupa savunması (RHM.DE, Xetra 11:30 ET kapanış) Ukrayna ateşkes haberlerinde ilk ve en sert tepkiyi veriyor (ör. Nisan 2026: -5/6%). ABD'de ayrıca bütçe (NDAA) ve İran haberleri etkili. ABD'nin büyük savunma şirketlerinin piyasa β'sı ~0. Bu nedenle yalnızca habere tepki veren bir öncü arandığında anlamlılar.
- **Taşımacılık:** FDX/UPS bilançosu -> emsaller. Dizel (HO=F) kısa vadede kamyon marjına baskı yapıyor çünkü yakıt ek ücreti bir hafta gecikmeli. Dizel 2026 Mayıs'ında yıllık +58% ile 5,60 $/galona çıktı.
- **Makine (tarım ve madencilik):** Bakır (HG=F) -> CAT; mısır ve soya -> DE; güçlü dolar -> ihracatçılar ters yönde. Bunlar önsel ve öncelik 3.
- **Tematik yüksek beta:** Sert düşüş sonrası kısa vadeli dönüş mü, momentum mu: iki yön de test edilmeli. Faiz artışı (+8 bp üstü) nükleer hikâye hisselerine baskı yapıyor.

## 2026 durumu ve takvim

- **Yıl içinde:** Ocak'ta 1,5 trilyon $'lık savunma bütçesi çağrısı savunmayı yükseltti. Şubat sonu ABD-İran çatışması petrol, dizel ve tanker navlununu patlattı (CL=F yılbaşından beri +46%, HO=F +85%). Haziran'da SpaceX halka arzı küçük uzay hisselerinden fon çekti. Temmuz'da New York yeni büyük veri merkezlerine moratoryum koydu; yerel oylamaların 41'inden 40'ında veri merkezi sınırlaması kabul edildi. Ağustos–Ekim'de faiz kaygısıyla nükleer hikâye hisseleri çöktü (OKLO yılbaşından beri -72%). 28 Ekim'de GEV güçlü Ç3 açıkladı (sipariş +96%, birikmiş sipariş 197 milyar $) ama hisse düştü. 29 Ekim'de CAT -9% düştü. 5 Kasım'dan beri yapay zekâ altyapısında satış sürüyor.
- **Şu an (21 Kasım):** XLI 5 günde -7,4%, XLU -3,1% (görece güçlü). Düzenlenmiş kamu hizmetleri 1 yıllık zirvesine yakın (DUK -0,6%, ED -1,3%). Tankerler zirvenin ~20% altında. NG=F son 1 ayda +22%.
- **Takvim:** 26 Kasım Şükran Günü (borsa kapalı, 27 Kasım kısa seans; bellek); 1 Aralık ISM imalat (10:00 ET; bellek); 9 Aralık PJM 2029/30 ihalesi açılışı; Aralık ortası FOMC (tarih doğrulanmadı); 16 Aralık FDX bilançosu (doğrulanmadı); NDAA 2027 Kongre süreci; CAT ve GEV Ç4 bilançoları Ocak sonunda; PJM veri merkezi çerçeve kararı Mart 2027.

## Tuzaklar

- **Kaldıraçlı ETF:** DFEN yılbaşından beri -37,8%, 1 yıllık en büyük düşüş -59%. Günlük yeniden dengeleme yüksek oynaklıkta erimeye yol açıyor. DFEN, DUSL ve UTSL'nin likiditesi düşük; alım-satım farkı 1-3 günlük getiriyi yiyebilir. Bunun yerine likit ana ETF ya da hisse tercih edilmeli.
- **Düşük likidite:** SEA, BDRY, XTN, UFO ve BOAT 20 milyon $ eşiğinin altında. SBLK, GNK, DAC ve FLNG da sığ. BDRY'nin gider oranı %3,50 ve vadeli yapısında contango (vadeli fiyatın spot fiyattan yüksek olması) erimesi var.
- **Tek hisse ve olay riski:** Bilanço gecesi (GEV, CAT, FDX) ±6–10% gap'ler oluşabiliyor; 1-3 günlük pozisyon bilanço tarihini kapsamamalı. Savunmada ateşkes haberleri hafta sonu gelip pazartesi gap'i yaratıyor. Uzay ve kuantum hisselerinde günlük σ 6–7%; 3 günlük 1σ hareket ~11%. IPP'lerde PJM ve FERC kararları, uzayda fırlatma kazaları riskli.
- **Rejim kayması:** Yapay zekâ güç sepetinin NVDA ile bağı 2026'da çok güçlendi. Geçmiş veride bu bağ yoktu; 2023 öncesi dönemle yapılan testler yanıltıcı olabilir.
- **Gecikme etkisinin kaybolması:** Tedarik zinciri ve sektör gecikmeleri belgelenmiş olsa da işlem maliyetiyle çoğu kayboluyor. Müşteri momentumu 2004 sonrası dönemde 2–4 kat zayıfladı.
- **Gece / gün içi asimetrisi:** DFEN, NLR, URA ve VRT'de 3 yıllık getirinin tamamı gece (kapanıştan açılışa) oluşuyor: DFEN gece +51,6 bp/gün, gün içi -16,1 bp/gün. Kapanışta alıp kapanışta satmak her iki parçayı da taşır.

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| UTSL 3x XLU, gider %0,97 net | https://www.direxion.com/product/daily-utilities-bull-3x-etf | "0.98 / 0.97*" gross/net (Ekim 2026) | orta |
| DUSL 3x XLI, gider %0,97 | https://etfdb.com/etf/DUSL/ | 0.97% expense ratio | orta |
| DFEN 3x, Dow Jones U.S. Select Aerospace & Defense endeksi; gider 2017'de %0,95 net | https://www.etftrends.com/2017/05/direxion-launches-5-leveraged-etfs-to-capitalize-on-trump-policies/2/ | gross 1.09%, net 0.95% | orta (eski) |
| BDRY gider oranı %3,50, yakın vade kuru yük navlun vadelileri | https://amplifyetfs.com/bdry/ | "3.50%"; expense limitation may be terminated after December 31, 2026 | orta |
| Yapay zekâ satışı 5 Kasım 2026'da sanayiye yayıldı | https://www.tikr.com/blog/caterpillar-sinks-another-6-vertiv-down-14-quanta-down-12-as-ai-selloff-spreads-to-industrials | Caterpillar 6%, Vertiv 14%, Quanta 12%; WDC down 17% | orta |
| CEG Ç3 sonrası 9 Kasım'da güç sepeti yükseldi | https://www.trefis.com/articles/623883/vertiv-stock-at-200-is-the-power-trade-back/2026-11-10 | Constellation 10.5%, Vertiv 9.6%, Quanta 9.4%, Vistra 7.3% | orta |
| CAT Ç3 bilançosunda düştü; birikmiş sipariş rekor | https://www.thestandard.com.hk/finance/article/346968/Caterpillar-sticks-to-annual-sales-forecast-amid-cost-pressures-shares-dive | "Shares of the company sank 8%"; backlog $78 billion | orta |
| Veri merkezi sınırlaması: yerel oylamalar ve NY moratoryumu | https://247wallst.com/investing/2026/10/13/caterpillar-sinks-5-as-deere-edges-higher-is-the-data-center-power-premium-unwinding/ | data center limits in 40 of 41 local ballot measures | düşük |
| GEV Ç3 2026: sipariş +96%, birikmiş sipariş 197 milyar $ | https://www.sec.gov/Archives/edgar/data/0001996810/000199681026000162/gevpressrelease3q26.htm | orders of $29.3 billion, up 96% organically; backlog $197 billion | yüksek |
| PJM 2028/29 ihalesi fiyat tavanında kapandı | https://insidelines.pjm.com/pjm-capacity-auction-procures-138318-mw-of-generation-resources-as-work-continues-to-address-growing-electricity-demand/ | 138,318 MW; 6,831 MW short of reliability requirement; cap $325/MW-day | yüksek |
| PJM 2029/30 ihalesi 9 Aralık 2026'da açılıyor | https://www.pjm.com/-/media/DotCom/markets-ops/large-load/large-load-registry-and-byonc-schedule.pdf | 2029/30 BRA opening Dec. 9, 2026 | orta |
| IPP hisseleri Eylül 2026'ya kadar 12 ayda düştü | https://www.spglobal.com/market-intelligence/en/news-insights/articles/2026/10/pjm-auction-delay-complicates-independent-power-producers-stock-price-recovery-106494914 | Vistra, Constellation, NRG, Talen declined 30%, 22%, 41%, 28% | orta (sayfa 403, arama özeti) |
| PJM spark spread artışı TLN kârını destekledi | https://www.fool.com/earnings/call-transcripts/2026/02/26/talen-tln-q4-2025-earnings-call-transcript | PJM spark spreads for 2026 to 2028 increased by over 15% | orta |
| VLCC navlunu 2026'da rekor | https://www.seatrade-maritime.com/tankers/vlcc-rates-near-470-000-a-day-for-fixtures-through-hormuz | $469,000 per day loading in the Arabian Gulf | orta |
| Eylül'de VLCC 600 bin $/gün üstü | https://www.kpler.com/blog/crude-tanker-rates-hit-new-highs-as-hormuz-risk-escalates | $32/bbl, equivalent to earnings of $1.2m/day | düşük (dönem karışık) |
| Kuru yük hisselerine emtia fiyatları öncülük ediyor (aylık, 2005–2021) | https://jshippingandtrade.springeropen.com/articles/10.1186/s41072-024-00178-9 | "commodity prices, with the latter having a leading impact on the former" | yüksek |
| Aynı çalışmada piyasa endeksi kuru yük getirisini açıklamıyor | https://jshippingandtrade.springeropen.com/articles/10.1186/s41072-024-00178-9 | neither the contemporaneous nor the lagged value of the stock market index has a significant impact | yüksek |
| Gecikme ilişkileri sürüyor ama maliyetle kayboluyor (aykırı kanıt) | https://www.alexandria.unisg.ch/254105/ | insignificant for one-way transaction costs of more than 40 basis points | yüksek |
| Müşteri momentumu 2004 sonrası zayıfladı (aykırı kanıt) | https://arxiv.org/pdf/2301.11394 | magnitude of customer momentum decreases by a factor of 2-4 | orta (arama özeti) |
| Müşteri getirisi tedarikçiyi önceden gösteriyor | https://www.aqr.com/insights/research/journal-article/economic-links-and-predictable-returns | customer momentum ... slow information diffusion | orta (arama özeti) |
| Avrupa savunması ateşkes haberine sert tepki veriyor (Nisan 2026) | https://finance.yahoo.com/markets/stocks/articles/europe-defense-stocks-slide-russia-182944735.html | Rheinmetall fell around 5% to 6%, Leonardo declined roughly 5% | orta |
| ABD savunması İran saldırısı sonrası düştü | https://newsukraine.rbc.ua/news/defense-stocks-fall-in-europe-and-the-us-1777165613.html | began falling right after the US launched strikes on Iran in late February | düşük |
| 1,5 trilyon $ savunma bütçesi çağrısı | https://www.yahoo.com/news/articles/trump-says-us-military-budget-213020184.html | $1.5 trillion; $901 billion approved by Congress for 2026 | orta |
| Dizel 2026 Mayıs'ında 5,60 $/galon, yakıt ek ücreti gecikmeli | https://www.ccjdigital.com/business/finance/article/15827534/how-the-2026-diesel-surge-is-costing-trucking-fleets-hundreds-of-thousands | $5.60 per gallon by mid-May 2026—a 58.3% increase | orta |
| Nükleer hikâye hisseleri faiz kaygısıyla düştü | https://247wallst.com/investing/2026/10/12/nuscale-power-sinks-7-as-nuclear-names-give-back-a-month-of-ground-oklo-falls-6-centrus-energy-drops-4/ | NuScale 7%, Oklo 6%; NuScale down 53% year to date | orta |
| SpaceX halka arzı küçük uzay hisselerini vurdu | https://247wallst.com/investing/2026/06/12/virgin-galactic-craters-24-rocket-lab-drops-8-ast-spacemobile-falls-10-as-spacex-hype-triggers-a-space-stock-shakeout/ | Rocket Lab drops 8%, AST SpaceMobile falls 10% | orta |
| FDX Ç2 (mali 2027) bilançosu 16 Aralık 2026 | https://bullstory.io/en/stocks/fdx/earnings/2027-q2 | December 16, 2026 | düşük |
| FFA değerleme saati 17:30 Londra | https://www.balticexchange.com/en/data-services/market-information0/ | assessments submitted by leading FFA brokers at 1730 (London) | orta (arama özeti) |
| EIA gaz depolama perşembe 10:30 ET; Şükran Günü 26 Kasım 2026 | — | — | doğrulanmadı (bellek) |
