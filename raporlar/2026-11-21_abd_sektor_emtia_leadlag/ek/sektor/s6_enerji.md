# S6 Enerji (hisse tarafı)

## Özet

2026 enerji yılı, 28 Şubat'ta başlayan ABD-İran savaşı ve Hormuz Boğazı'ndaki kesintiyle şekillendi: USO yılbaşından beri +%102, BNO +%108, XLE +%38, rafineriler (MPC +%129, PBF +%132, VLO +%108) en büyük kazananlar. Son bir ayda tablo döndü: USO -%14, rafineriler -%15 ile -%28, XOP -%15. Nükleer/güç (CEG -%32, VST -%28) ve güneş (FSLR -%47, ENPH -%39) yılı ağır kayıpla geçiriyor; uranyum hisseleri spot fiyattan bağımsız düştü. 1-3 günlük vadede en güçlü test adayı **3-2-1 crack değişimi -> rafineriler (özellikle PBF, VLO)**; kendi hızlı taramamızda 2016 sonrası t ≈ 3. Petrol -> E&P/hizmet bir gün gecikmesi yalnız 2023 sonrasında pozitif (t ≈ 2), 2016+ örnekleminde yok: rejime bağlı. Lider rafineri -> küçük rafineri, UNG -> gaz üreticileri, SRUUF -> uranyum madencileri için günlük öncülük bulunmadı; bunlar ya sıfır ya ters işaretli.

## Araç tablosu

Sayılar ozet_istatistik.csv'den: sigma1g = günlük oynaklık %, hacim = 20 günlük ortalama, milyon $.

| Alt sektör | Ana ETF | Kaldıraçlı/ters | Öncü hisseler (likit) | Yüksek betalı takipçiler | Not |
|---|---|---|---|---|---|
| Geniş enerji | XLE (hacim 2.374, σ 1,48), VDE (89) | ERX 2x / ERY -2x (IXE; gider 0,91 / 0,99 net); ERY hacmi 201, ERX 51 | XOM (2.564), CVX (1.860), COP (1.048) | — | XLE'nin %24'ü XOM, %18'i CVX: iki hissenin ETF'i gibi davranır |
| Entegre ve arama-üretim | XOP (571, σ 1,90); IEO (16, eşik altı) | GUSH 2x / DRIP -2x (S&P O&G E&P Select; hacim 22 / 49, eşiğin altında-sınırda) | XOM, CVX, COP, OXY (635), EOG (524), DVN (554), FANG (419) | APA (σ 2,82, ytd +89), CVE (2,37), EQNR (2,56), PBR (2,47), SU, KOS (σ 5,6 ama hacim 44, likit değil) | ABD betası negatif (XOM -0,53, COP -0,63): piyasa düşüşünde koruyucu, ama bu 2026 savaş rejiminin ürünü |
| Petrol hizmetleri ve sondaj | OIH (110, σ 1,97); XES (11) ve IEZ (27) zayıf likit | Yok (OIH için likit kaldıraçlı ürün yok) | SLB (582), BKR (546), HAL (308), FTI (221) | RIG (σ 3,28, hacim 235), VAL (3,87), NE (2,75), PTEN (3,32), LBRT (3,97), HP (2,84), NOV | BKR'nin yarısı LNG/gaz teknolojisi; saf hizmet teması için SLB/HAL/RIG |
| Rafineri | CRAK (41, eşik altı, σ 1,41) | Yok | VLO (1.196), MPC (1.031), PSX (943), DINO (267) | PBF (σ 4,15, hacim 177), DK (3,56, 94), CVI (3,71, 106), PARR (3,63, 60) | En yüksek ytd ve son 1 ayda en sert düzeltme; PBF crack'e en duyarlı |
| Boru hattı ve LNG | AMLP (69, σ 0,85, K-1 yok, MLP) | Yok | LNG (721), WMB (616), KMI (418), TRGP (391), OKE (286), ENB (251) | ET, EPD (düşük σ ~1,1-1,2; takipçi değil) | 1-3 günlük işlem için oynaklık düşük; temada en yüksek σ LNG (2,01) |
| Doğal gaz üreticileri | FCG (26, eşik sınırında) | BOIL 2x / KOLD -2x (Henry Hub vadeli, hisse değil; σ ~6,9) | EQT (506), RRC (332), EXE (262), AR (169), CNX (67) | AR (σ 2,35), RRC (2,34) | RRC artık EQT birleşme arbitrajı (0,987 EQT hissesi): bağımsız hedef değil |
| Kömür | Yok (KOL kapandı; likit ETF yok) | Yok | HCC (57), BTU (55), CNR (51), AMR (36) | BTU (σ 3,56), AMR (3,59) | Tüm isimler likidite eşiğinde; tek hisse riski yüksek |
| Uranyum ve nükleer | URA (164, σ 3,21); URNM (39), NLR (51) | Likit kaldıraçlı yok | CCJ (314), GEV (3.625), CEG (1.015), VST (845), TLN (392), BWXT (176) | LEU (σ 5,52), UEC (4,94), NXE (3,45), UUUU (5,26), DNN, OKLO/SMR (σ ~6, beta ~3,6) | GEV, BE, ETN, PWR bu grupta ama sürücüleri yapay zekâ ve elektrik altyapısı, uranyum değil |
| Güneş ve temiz enerji | TAN (99, σ 2,46), ICLN (106, σ 1,95); PBW (10, eşik altı) | Yok | FSLR (636), NXT (326), ENPH (236), BE (3.353) | ENPH (σ 5,30), SEDG (5,92), RUN (4,93), ARRY (5,14), PLUG ve FCEL (fiyat $1 ve $7 civarı, sıçrama riski) | SPY betası 1,5-2,6: enerji değil, yüksek betalı büyüme hissesi gibi davranır |

## 1-3 günlük sürücüler ve öncü göstergeler

**Zamanlama kuralı.** Yahoo'daki CL=F, RB=F, HO=F, NG=F günlük kapanışları NYMEX uzlaşma fiyatıdır (petrol 14:30 ET). Uzlaşma 16:00'dan önce bilinir, yani sinyal olarak kullanılabilir. Ama 14:30-16:00 arasında petrol hareket etmeye devam eder. Hızlı taramada USO ile CL=F'nin aynı gün farkı ertesi gün CL=F'yi tahmin ediyor (2016+ t=2,5; 2023+ t=3,2). Bu bir senkron kayma artefaktıdır, gerçek öncülük değildir. Test ederken hisse hedefleri için öncü olarak 16:00'da kapanan USO/BNO/UNG kullanılmalı; vadeli kapanışla yapılan testte görülen "öncülük" saat farkından gelebilir.

**Hızlı tarama (veri/ham, günlük log getiri, öncü t günü, hedef t+1; t ≈ korelasyon×√n; çoklu test düzeltmesi yok):**
- 3-2-1 crack % değişimi -> PBF t+1: 2016+ c=0,064 (t 3,3), 2023+ c=0,049, 3 günlük c=0,109. VLO t+1: 2016+ t 3,1, 2023+ sıfır. Mekanizma: rafineri hisseleri marj değişimini gecikmeli fiyatlıyor. En güçlü aday.
- USO -> XLE/XOP/OIH t+1: 2023+ pozitif (t 1,9-2,3), 2016+ sıfır ya da negatif. Akademik literatür (Driesprong vd. 2008 izinde) petrol etkisinin aylık frekansta ve çoğunlukla petrol dışı sektörlerde olduğunu söyler; günlük enerji hissesi için kanıt zayıf.
- Lider rafineri (VLO, MPC) -> küçük rafineri (PBF, DK, PARR, CVI) t+1: 2016+ **negatif** (t -1,9 ile -3,9), 2023+ sıfır. Yani ABD içinde rafineriler arası pozitif öncülük yok; tersine kısa vadeli dönüş var. Türk rafinerisine öncülük saat farkından (İstanbul seansı ABD'den önce kapanır) geliyor; ABD içinde bu fark yok.
- UNG/NG=F -> EQT, AR, CNX t+1: sıfır ya da 2023+ hafif negatif (t -1,8 ile -2,1). Gaz hisseleri gazı aynı gün fiyatlıyor.
- SRUUF -> CCJ, UEC: sıfır. CCJ -> UEC, NXE: sıfır.
- ^OVX (petrol oynaklık endeksi) artışı -> XOP t+1: 2016+ c=0,043 (t 2,2): korku sonrası kısmi dönüş.
- XLE ve XOP kendi gecikmesi 2016+ negatif (t -2,0 / -2,5): günlük kısa vadeli dönüş; 2023+ hafif pozitif. Rejim değişiyor.
- ^TNX -> TAN/ENPH: anlamlı değil.

**Veri açıklamaları (hepsi 16:00'dan önce):** EIA haftalık petrol raporu Çarşamba 10:30 ET (tatil haftası Perşembe 12:00); EIA gaz depolama Perşembe 10:30 ET; Baker Hughes kule sayısı Cuma 13:00 ET (öğlen Central). Kule sayısı haftalık ve yavaş değişir; 1-3 günlük sinyal olarak önsel değeri düşük. OPEC+ toplantıları çoğunlukla Pazar günü: Cuma kapanışında alınan pozisyon hafta sonu boşluk riskini taşır.

**Diğer sürücüler:** Brent-WTI farkı (BZ=F - CL=F) ihracatçı ve kıyı rafinerileri için; Avrupa gazı (TTF) LNG için (Avrupa seansı ABD kapanışından önce biter); yapay zekâ veri merkezi haberleri ve PJM düzenlemesi CEG/VST/TLN için; şirket sonuçları (FSLR 3. çeyrek sonrası 7 günde -%24) güneş için.

## 2026 durumu ve takvim

- **Savaş ve petrol:** Dünya Bankası'na göre Mart sonuna kadar Brent yaklaşık %65 (46 $/varil) yükseldi, Mart'ta küresel arz 10,1 mb/g düştü; Nisan başında geçici ateşkes geldi. Ekim ortasında petrol yeniden 100 $'ı aştı (Reuters/BOE Report), 17 Kasım'da Brent ~93 $, Hormuz'da tanker saldırıları sürüyor. ozet_istatistik ile tutarlı: USO ytd +%102 ama son 1 ay -%14.
- **Rafineriler:** dizel crack'i Ağustos'ta rekor (247wallst); bizim hesapladığımız 3-2-1 crack 2026 zirvesi 75,3 $/varil (28 Ağustos), şimdi 41,0 $ (2016+ ortalaması 24,2 $). Marj hâlâ tarihsel olarak yüksek ama zirvenin yarısı: rafineri düzeltmesi bununla uyumlu.
- **OPEC+:** 1 Kasım'da Aralık üretim hedefleri sabit bırakıldı; **29 Kasım** toplantısı 2027 çerçevesini belirleyecek (Pazar: 30 Kasım Pazartesi açılış boşluğu riski).
- **Doğal gaz:** Aralık Henry Hub 11 Kasım'da 3,22 $; LNG besleme gazı 7 Kasım'da günlük rekor; EIA 2027 Henry Hub tahminini 3 $'ın altına indirdi. EQT, Range'i 26 Ekim'de hisse takasıyla alma kararı verdi (kapanış 2027 1. çeyrek).
- **Güç ve nükleer:** Kasım ara seçimlerinde Demokratların iki meclisi alması ve Teksas valiliği sonrası VST bir günde ~%15, CEG ~%9 düştü; PJM'de maliyet düzenlemesi baskısı sürüyor.
- **Uranyum:** spot 80'lerin ortasında (doğrulanmadı, tarih belirsiz), uzun vadeli kontrat fiyatı yılbaşından beri ~%12 yukarıda; CCJ 9 aylık sonuç ve daraltılmış rehberlik sonrası düştü.
- **Güneş:** FSLR 3. çeyrek satışları ~%23 düştü, 2026 gelir tahmini indirildi, 7 günlük kayıp serisi %24 (Trefis, tek kaynak).
- **Yakın takvim:** EIA petrol 25 Kasım Çarşamba 10:30 (Şükran Günü haftası istisna listesinde yok, normal gün); gaz depolama ve Baker Hughes Şükran Günü haftasında muhtemelen 25 Kasım Çarşamba (geçmiş yıllardan çıkarım, 2026 için doğrulanmadı); 26 Kasım borsa kapalı, 27 Kasım yarım gün; 29 Kasım OPEC+; ardından her Çarşamba/Perşembe EIA.

## Tuzaklar

- **Kaldıraçlı erime:** ERX/ERY, GUSH/DRIP günlük 2x hedefler; ihraççı "periods greater than a day" için 2x beklenmemeli diyor. 1-3 günlük tutuşta erime küçüktür ama σ1g ~3-4 olan GUSH/DRIP'te dalgalı günlerde belirgindir. GUSH (22) ve DRIP (49) hacim eşiğinin sınırında; ERX (51) de zayıf. Bunun yerine XOP/XLE ya da tek hisse tercih edilmeli. BOIL/KOLD vadeli kontrat devri (contango) taşır ve σ ~7'dir.
- **Likidite:** CRAK, XES, IEO, IEZ, FCG, URNM, PBW, kömür hisseleri, KOS, PARR, CQP eşik altında ya da sınırda; kapanış emrinde kayma maliyeti beklenenden yüksek olabilir.
- **Tek hisse ve olay riski:** sonuç açıklamaları (FSLR -%13,6 tek gün), birleşme (RRC artık EQT'yi izliyor), seçim ve düzenleme (VST -%15), OPEC+ hafta sonu kararları, Hormuz haberleri (gece boşluğu). Uranyum küçükleri (UUUU, LEU, UEC) 1 yılda -%70 ile -%82 düştü.
- **Rejim riski:** enerjinin negatif SPY betası ve petrol öncülüğünün 2023+ pozitif oluşu savaş dönemine özgü olabilir; 2016+ örnekleminde kaybolup tersine dönüyor. Örneklem dışı ve rejim ayrımı şart.
- **Saat farkı artefaktı:** vadeli uzlaşma (14:30) ile hisse kapanışı (16:00) arasındaki fark sahte öncülük üretir.
- **Akademik aykırı kanıt:** ABD/Kanada firma düzeyinde hisselerin petrole "without delay" tepki verdiğini bulan çalışma var; petrol vadeli değişiminin sektör getirisini tahmin gücü zayıf (Jahan-Parvar vd.).

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| Hormuz kesintisi tarihteki en büyük petrol şoku | https://blogs.worldbank.org/en/opendata/strait-of-hormuz-disruption-sends-oil-prices-surging | "triggered the largest oil market shock in history" | yüksek |
| Brent Mart sonuna kadar %65 yükseldi | aynı | "By the end of March, the Brent price had increased by about 65 percent ($46/bbl)" | yüksek |
| Mart'ta küresel arz 10,1 mb/g düştü | aynı | "Global oil supply crashed by 10.1 mb/d in March" | yüksek |
| Nisan başında geçici ateşkes | aynı | "Prices eased somewhat in early April after the announcement of a temporary ceasefire" | yüksek |
| Savaş 28 Şubat'ta başladı | https://www.iea.org/topics/the-middle-east-and-global-energy-markets (403, arama özeti) | "the war in the region that began on 28 February" | orta |
| Ekim ortasında petrol 100 $ üstü, enerji hisseleri yükseldi | https://boereport.com/2026/10/16/us-energy-stocks-gain-as-oil-tops-100-on-supply-fears/amp/ | başlık: "US energy stocks gain as oil tops $100 on supply fears" (arama özeti) | orta |
| 17 Kasım Brent ~93 $, Hormuz tanker saldırıları | https://oilprice.com/Energy/Energy-General/Brent-Stuck-Near-93-as-Hormuz-Tanker-Attacks-Offset-Gulf-Export-Surge.html | "Brent Stuck Near $93 as Hormuz Tanker Attacks Offset Gulf Export Surge" (başlık) | orta |
| OPEC+ Aralık hedeflerini sabit tuttu; sonraki toplantı 29 Kasım | https://www.opec.org/pr-detail/2033620-1-november-2026.html | "The next meeting will be held on 29 November 2026" (arama özeti) | orta |
| Dizel crack Ağustos'ta rekor | https://247wallst.com/investing/2026/08/18/diesel-prices-are-breaking-records-3-refiners-turning-the-crisis-into-record-profits/ | "$102.20 a barrel" (arama özeti) | orta |
| ERX/ERY günlük ±2x, IXE endeksi, gider oranı | https://www.direxion.com/uploads/ERX-ERY-Fact-Sheet.pdf | "Daily Target 200% -200% ... Net Expense Ratio* 0.91% 0.99%" | yüksek |
| Kaldıraçlı ETF birden uzun dönemde 2x vermez | aynı | "should not be expected to provide two times ... for periods greater than a day" | yüksek |
| XLE yoğunlaşması | aynı | "Exxon 24.12 Chevron Texaco 18.12" (%; 30.09.2026) | yüksek |
| GUSH/DRIP endeksi | https://direxion.com/product/daily-sp-oil-gas-exp-prod-bull-bear-2x-etfs | "S&P Oil & Gas Exploration & Production Select Industry Index" (arama özeti) | orta |
| Petrol spot değişimi sektörlerin ~beşte birini tahmin ediyor, vadeli zayıf | https://mpra.ub.uni-muenchen.de/15670/1/MPRA_paper_15670.pdf | "significant prediction power for slightly under one fifth of industry returns ... Oil future prices have weak prediction power" | yüksek |
| Yatırımcılar petrolün kazanca etkisini yavaş işliyor (aylık/çeyreklik) | https://ideas.repec.org/a/oup/rasset/v14y2024i2p274-309..html | "equity investors are slow to process information ... annualized Sharpe ratio of 0.50" | yüksek |
| Aykırı: firma düzeyinde gecikmesiz tepki | https://economics.ecu.edu/wp-content/pv-uploads/sites/165/2019/07/ECU0912.pdf | "respond to oil market movement without delay" (arama özeti) | orta |
| EIA petrol raporu Çarşamba 10:30; 2026 istisnaları Şükran Günü içermiyor | https://www.eia.gov/petroleum/supply/weekly/schedule.php | "10:30 a.m. eastern time on Wednesday with the following exceptions" | yüksek |
| Baker Hughes: iş haftasının son günü öğlen Central | https://rigcount.bakerhughes.com/rig-count-overview/ | "published weekly at noon Central Time on the last day of the work week" (arama özeti) | orta |
| Şükran Günü haftası gaz depolama Çarşamba 12:00 (2025) | https://ir.eia.gov/ngs/schedule.html | "11/26/2025 Wednesday 12:00 p.m." (arama özeti; 2026 satırı görülmedi) | orta |
| Aralık Henry Hub 11 Kasım'da 3,22 $ | https://www.aga.org/research-policy/resource-library/natural-gas-market-indicators-november-12-2026/ | "settled at $3.22 per MMBtu on November 11" (arama özeti) | orta |
| EQT, Range'i hisse takasıyla alıyor | https://finviz.com/news/407513/eqt-announces-strategic-acquisition-of-range-resources-creating-americas-undisputed-natural-gas-champion | "0.987 shares of EQT common stock" (arama özeti) | orta |
| Seçim sonrası VST -%15, CEG -%9 | https://stocktwits.com/news-articles/markets/equity/vst-ceg-stocks-drop-as-election-outcome-hits-merchant-power-generators/cNGLkduR93x | "Vistra traded 15% lower ... Constellation declined 9%" (arama özeti) | orta |
| FSLR 7 günde -%24, 3. çeyrek satış düşüşü | https://www.trefis.com/stock/fslr/articles/626088/first-solar-stock-extends-a-7-day-losing-streak-to-a-24-loss/2026-11-18 | "7-Day Losing Streak To A 24% Loss" (başlık) | orta |
| Uranyum spot 80'lerin ortası, hisseler düşerken | https://www.xtb.com/cy/market-analysis/news-and-research/uranium-stocks-after-the-selloff-uranium-energy-corp-tumbles-50-from-its-highs | "mid-$80 per pound range" (arama özeti, tarih belirsiz) | düşük |
| Rafineri marjı mevsimsel: Ekim-Şubat genişleme | https://www.wealthmanagement.com/etfs/tis-season-oil-refiners | "widened, on average, by 76 percent" (arama özeti, eski) | düşük |
| 3-2-1 crack -> PBF t+1 (kendi taramamız) | veri/ham (RB_eq_F, HO_eq_F, CL_eq_F, PBF) | 2016+ c=0,064, t≈3,3; 2023+ c=0,049 | orta (düzeltme yok) |
| VLO/MPC -> küçük rafineri t+1 negatif | veri/ham | MPC->PBF 2016+ c=-0,075, t≈-3,9 | orta |
| USO -> OIH t+1 yalnız 2023+ pozitif | veri/ham | 2023+ c=0,086 (t 2,3); 2016+ c=-0,003 | orta |
| CL=F uzlaşma artefaktı | veri/ham | USO-CL farkı -> CL=F t+1: 2023+ c=0,118 (t 3,2) | yüksek |
