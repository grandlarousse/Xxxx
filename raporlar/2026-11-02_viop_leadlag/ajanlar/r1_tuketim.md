# r1 — TÜKETİM / PERAKENDE / GIDA-İÇECEK (BIMAS, MGROS, SOKM, ULKER, AEFES)
Ajan: tuketim · Veri: 30.10.2026 kapanışı · Örneklem 2014-01-02 → 2026-10-30 (SOKM 2018+) · IS 2014–2020 / OOS 2021–2026
Veri düzeltmeleri uygulandı: FX_FIX (Yahoo '=X' 1 gün kayması) + simetrik ±%10,5 temizlik (taban günleri artık dahil). Tüm a1–a5, a7 sonuçları düzeltilmiş panelle YENİDEN üretildi.

## 0. Ana sonuç (tek paragraf)
Beklendiği gibi bu grup **ağırlıklı yurt içi**: 172 yabancı hisse/emtia/FX sürücüsünde XU100 kontrollü kısmi korelasyon medyanı |pc| = **0,019**; %91'inde |pc| < 0,05; hiçbirinde |pc| ≥ 0,10 değil. Lag-1 → gün-içi (işlenebilir) öncülükte veri güdümlü taramada **0/5.620** test FDR'den geçti (gün-içi artıkta da 0/5.620). Dışarıdan anlamlı tek istisna **AEFES** (CCOLA iştiraki + küresel bira emsalleri + küresel/EM faktörü). Grubun gerçek ortak sürücüsü **yurt içi gıda-perakende faktörü** (hisseler arası artık korelasyonları 0,17–0,37 ve OOS'ta güçleniyor) ve **banka rotasyonunun tersi** (XBANK ile negatif kısmi korelasyon). "Defansiflik" = düşük beta; koşullu alfa yok ve kuyruk günlerinde beta ~1'e çıkıyor. Kakao → ULKER hipotezi **çürüdü** (işaret bile ters).

## 1. Net bulgular tablosu
| # | Hisse | Sürücü (Yahoo → TV) | İlişki | Rakam | IS / OOS | Güven |
|---|---|---|---|---|---|---|
| 1 | AEFES | CCOLA.IS → BIST:CCOLA | senkron | corr 0,44; pc\|XU100 0,233; yılların 12/13'ünde + (yalnız 2022 ≈0) | 0,200 / 0,264 | **YÜKSEK** |
| 2 | AEFES | CCOLA (60m) | gün-içi senkron | corr 0,437; XU100-artık 0,218 (t=11,3); artık lag1 0,001 | – | **YÜKSEK** (öncülük YOK) |
| 3 | BIMAS/MGROS/SOKM/ULKER | birbirleri (BIST:…) | senkron, XU100 artığı | MGROS–SOKM 0,314; SOKM–BIMAS 0,248; BIMAS–MGROS 0,222; ULKER–SOKM 0,193; ULKER–MGROS 0,167 | MGROS–SOKM .22/.37; BIMAS–MGROS .07/.37 | **YÜKSEK** (BIST-içi) |
| 4 | AEFES | CARL-B.CO, HEIA.AS, ABI.BR, CCH.L, BUD → OMXCOP:CARL_B, EURONEXT:HEIA, EURONEXT:ABI, LSE:CCH, NYSE:BUD | senkron | pc\|XU100+STOXX/SPX 0,07–0,09; plasebo (diğer 4 hisse) \|pc\|<0,04 | CARL .090/.091, CCH .105/.092, HEIA .050/.101 | ORTA |
| 5 | AEFES | küresel/EM faktör (EEM → AMEX:EEM) | senkron | FDR geçen 37 yabancı sürücünün 34'ü +; EEM pc 0,044 | aynı işaret | ORTA |
| 6 | BIMAS, SOKM, ULKER (MGROS, AEFES zayıf) | XBANK → BIST:XBANK | senkron (rotasyon) | pc: BIMAS −0,164, SOKM −0,125, ULKER −0,093 | BIMAS −.30/−.07; SOKM −.19/−.10 | ORTA |
| 7 | Hepsi | XU100 kuyruk | rejim | XU100≤−%2 günlerinde beta 0,88–1,08 (tam dönem 0,70–0,88); MGROS/SOKM/ULKER/CCOLA aşağı beta > yukarı (t −2,0…−3,5) | – | ORTA (olumsuz) |
| 8 | Hepsi | XU100≤−%3 günleri (n=88) | olay | ham göreli +21…+145 bps, beta-düzeltmeli ≈0 veya − (ULKER −55, AEFES −41, CCOLA −42) | B2c IS −79 / OOS +92 bps → işaret değişiyor | ORTA (olumsuz) |
| 9 | AEFES | Rusya olayları | olay | 24.02.2022 CAR t0..t4 −2.133 bps; 01.03.2022 −1.178; 17.10.2023 geçici yönetim t0..t2 −560 | tekil | ORTA |
| 10 | Hepsi | ^VIX, USDTRY_{t-1} | lead_gap (işlenemez) | VIX→gap −0,10…−0,12 (t≈−5); USDTRY_{t-1}→MGROS gap −0,155 (t −4,3) | gün-içine taşma yok | ORTA (işlenemez) |
| 11 | AEFES | KE=F (arpa/malt proxy) → CBOT:KE1! | senkron | pc −0,063 (t −3,2) | −0,068 / −0,053 | ORTA-DÜŞÜK (büyüklük çok küçük) |
| 12 | BIMAS/MGROS/ULKER | SX5E≤−%2 (senkron Avrupa risk-off) → TVC:SX5E | olay | β-adj +37…+46 bps | BIMAS IS +69 / OOS −1; MGROS +28/+55; ULKER +21/+74 | DÜŞÜK (işlenemez) |
| 13 | ULKER | USDTRY aylık → FX:USDTRY | rejim | pc −0,156; OOS β_rel −0,44 (t −3,5) | −0,08 / −0,23 | DÜŞÜK (2021+ rejimi; ORTA adayı) |
| 14 | BIMAS / MGROS | TL şok günü (USDTRY ≥ +%1,5) | olay | BIMAS +30 bps (t 1,9); MGROS −38 bps (t −2,4) | BIMAS +32/+27; MGROS −52/−8 | DÜŞÜK |
| 15 | ULKER | CC=F kakao → ICEUS:CC1! | senkron/öncülük/aylık | günlük pc 0,015; lag1 gün-içi t −1,05; aylık lag0–6 anlamsız; yıllık corr **+0,20 (yanlış işaret)** | backtest OOS Sharpe −0,12 | **ÇOK DÜŞÜK** |
| 16 | BIMAS/MGROS/SOKM | yabancı perakende (JMT.LS, DNP.WA, CA.PA, AD.AS, WMT, COST, SHP.JO…) | senkron | hepsi \|pc\| < 0,04 | – | ÇOK DÜŞÜK (olumsuz) |
| 17 | Hepsi | ABD risk-off_{t-1} → defansif rotasyon | lead_intra (backtest B2a) | IS −16,9 bps / OOS −3,6 bps (16 bps maliyet) | OOS Sharpe −0,13 | ÇOK DÜŞÜK |
| 18 | Hepsi | 22.480 testlik tarama | lead_intra | FDR(aile) 0 geçiş; en iyi t≈3,6–4,0 (Çin A-hisseleri, 0001.HK, COALINDIA.NS) | – | ÇOK DÜŞÜK (sahte pozitif) |

Ayrıntılı tüm satırlar (214 çift + 30 özel bulgu): `f_tuketim.csv`.

## 2. Şirket gerçekleri (WebSearch, kısa doğrulama)
- **AEFES**: CCI'da ~%50,3 pay, 2013'ten beri tam konsolidasyon. Rusya bira (AB InBev Efes) Ekim 2023'te Rus devletinin "geçici yönetimi"ne alındı; AB InBev payının Efes'e devri (Ara-2023) Rus makamlarınca reddedildi (Ağu-2024), Eki-2024'te Rusya-Efes / Ukrayna-AB InBev bölünmesi planlandı; **1.1.2025'ten itibaren Rusya bira konsolidasyon dışı, "finansal yatırım"**; 2025 ortasında yeni başvuru da reddedildi. Kaynaklar: [just-drinks](https://www.just-drinks.com/newsletters/russia-again-rejects-efes-proposal), [inside.beer](https://www.inside.beer/news/detail/russian-authorities-block-ab-inbevs-sale-of-joint-venture-stake-to-anadolu-efes), [Belga](https://belganewsagency.eu/ab-inbev-exits-russian-joint-venture-ab-inbev-efes), [KAP](https://kap.org.tr/tr/api/file/download/4028328c9f52dc40019ff20542a74483). 2026 durumu doğrulanamadı.
- **BİM**: Fas (2009, %65 pay, 2025 sonu 933 mağaza) ve Mısır (2013/14, %100, 445 mağaza); yurt dışı ciro payı Fas ~%5, Mısır ~%1. [Morocco World News](https://www.moroccoworldnews.com/2026/03/284641/bim-nears-1000-stores-in-morocco-following-record-expansion-in-2025/), [Fintables](https://fintables.com/arastirma/yazilar/ne-is-yapiyor/bim-ne-is-yapiyor/pdf).
- **Ülker**: 2025 ciro 111,9 mlr TL, yurt dışı 21,3 mlr TL (~%19); kakao/şeker/fındıkta proaktif alım ve hedge. [Yıldız Holding](https://www.medyamerkezi.yildizholding.com.tr/en/press-releases/ulker-announces-its-2025-full-year-financial-results), [İnfo Yatırım](https://cdn.infoyatirim.com/Content/Analysis/ULKER%202025-12%20Finansal%20De%C4%9Ferlendirme%20Raporu.pdf).
Bu gerçekler istatistikle uyumlu: BİM'in Mısır/Fas maruziyeti istatistiksel olarak görünmeyecek kadar küçük (EGP=X pc 0,018, MAD=X 0,016); Ülker'in hedge politikası kakao fiyatının hisseye geçmemesini açıklıyor; AEFES'in Rusya kanalı kurdan olay riskine dönüştü.

## 3. Yöntem
- Getiriler: log, BIST takvimi (ll.ret), BIST dışı sürücüde tatil-ffill sıfırları NaN. Senkron: corr tam/3y/1y; XU100 kontrollü kısmi korelasyon (ek: XU100+USDTRY, USD bazlı r_TL−r_USDTRY); beta; yıllara göre kısmi korelasyon işareti (NaN yıllar hariç); IS/OOS.
- Öncülük: sürücü_{t−1} → hisse cc, **gap**, **gün-içi**, gün-içi artığı (XU100 gün-içine göre), t+1..t+4 sürüklenme; ters yön hisse_{t−1} → sürücü_t. Newey-West(5) t.
- Defansiflik (a2): olay günlerinde hisse−XU100 (cc/gap/intra) ve beta-düzeltmeli göreli getiri; yukarı/aşağı beta, kuyruk betası; olay sonrası 5 gün.
- Veri güdümlü tarama (a3): 5 hisse × panel_ret_bistcal'deki tüm semboller (+MAD/PKR/UZS/IQD) × {senkron kısmi, lag1 gap, lag1 intra, lag1 intra-artık} = **22.480 test**; aile bazında BH-FDR q=0,05 (birincil). Havuzlanmış FDR ayrıca hesaplandı ama yanıltıcı (güçlü gap/senkron p'leri eşiği gevşetiyor → 13 "geçiş" artefakt).
- Özel testler (a4): kakao aylık/yıllık/rejim/büyük hareket; AEFES yıllara göre RUB/KZT/CCOLA/bira; Avrupa endeksi kontrollü emsal + plasebo; olay çalışmaları (Rusya, EGP devalüasyonları, kakao zirveleri); TÜFE günleri; XBANK rotasyonu; artık korelasyon matrisi. Saatlik (a6): AEFES–CCOLA, ULKER–kakao, ES=F. Aylık FX (a7).
- Backtest (a5): look-ahead yok; sinyal t−1 ABD/vadeli kapanışında bilinir → BIST açılışında gir; maliyet gidiş-dönüş 8 ve 15 bps (çift bacakta ×2).

## 4. Kanıt
### 4.1 Senkron — dış sürücüler zayıf (olumsuz bulgu, rakamla)
- 172 yabancı/emtia/FX çiftinde medyan \|corr_full\| 0,058, medyan \|pc\| 0,019. Ham korelasyonlar (ör. BIMAS–^GSPC 0,14) tamamen XU100 kanalından geliyor (pc ≈ 0).
- ULKER: CC=F 0,015, SB=F ~0,02, ZW=F −0,01, ZL=F 0,01, MDLZ/HSY/NESN/BARN/LISN \|pc\|<0,03 → hiçbiri anlamlı değil.
- Perakende: JMT.LS, DNP.WA, CA.PA, AD.AS, TSCO.L, WMT, COST, SHP.JO, CPALL.BK… hepsi \|pc\|<0,04.
- AEFES istisna: bira emsalleri 0,07–0,10 (Avrupa/ABD endeksi kontrolünden sonra da 0,07–0,09; IS ve OOS aynı); plasebo (aynı emsaller × diğer 4 hisse) ≈0 → AEFES'e özgü sektör faktörü. KO/PEP/KOF zayıf (0,02–0,05).
- BIST-içi küçük FX satırları (BIMAS~TRY=X pc 0,063; MGROS~EURTRY −0,086, IS'de −0,15, OOS −0,02) otomatik kuralla ORTA çıktı ama büyüklük çok küçük; ekonomik önemi düşük kabul edin.

### 4.2 Öncülük
- Gap kanalında çok sayıda "anlamlı" sonuç var (FDR aile: 1.337) ama bunlar eşzamansız kapanış (VIX, TUR, ABD endeksleri, USDTRY akşamı) ve piyasa geneli; açılışta fiyatlanır → **işlenemez**.
- Gün-içi: 172 seçilmiş sürücüde \|t\|≥2,5 olan yok; taramada 0/5.620 FDR. Saatlikte AEFES–CCOLA senkron 0,44 ama lag1 öncülük yok (artık 0,001).
- Ters yön: düzeltilmiş FX ile BIST_{t−1}→USDTRY_t korelasyonu 0,013 (önceki −0,17 artefaktı ortadan kalktı).

### 4.3 Defansiflik (koşullu beta)
- Tam dönem beta: BIMAS 0,70, CCOLA 0,75, AEFES 0,79, SOKM 0,80, ULKER 0,83, MGROS 0,88.
- XU100≤−%3 günleri: ham göreli pozitif (BIMAS +145 bps, t 5,9) ama **beta-düzeltmeli** BIMAS +6,5, SOKM +9,3, MGROS −33, ULKER −55, AEFES −41, CCOLA −42 → defansiflik tamamen düşük betadan. Kuyruk betası 0,88–1,08 → panik günlerinde koruma zayıflıyor. Simetrik temizlikten önce (taban günleri silinince) bu tablo daha "defansif" görünüyordu.
- ABD risk-off_{t−1} (SPX≤−%2, n=104) → gün-içi göreli anlamsız (\|t\|<1,3). VIX sıçraması da anlamsız.
- Senkron Avrupa risk-off: BIMAS/MGROS/ULKER β-adj +37…+46 bps (t 1,7–2,5) ama BIMAS'ta yalnız IS'de; AEFES/CCOLA defansif değil (−22 bps). Senkron olduğu için işlenemez.

### 4.4 FX / enflasyon hedge
- Aylık: ULKER TL değer kaybı aylarında XU100'ün gerisinde (pc −0,156; OOS β_rel −0,44, t −3,5; IS ≈0) → 2021+ rejimi (YP borç/ithal girdi hipotezi). AEFES'in aylık "hedge" görüntüsü FX_FIX sonrası kayboldu (pc 0,04; OOS −0,07). BIMAS/MGROS/SOKM anlamsız.
- Günlük TL şok günleri: BIMAS +30 bps (fiyatlama gücü?), MGROS −38 bps (yalnız IS).

### 4.5 Emtia
- Kakao→ULKER: 2023–24'te kakao +%150 (log) iken ULKER−XU100 +%41; 2025–26'da kakao −%76 iken ULKER−XU100 −%42 → maliyet hipotezinin **tersi** (yıllık corr +0,20, n=19, anlamsız). Muhtemel açıklama: hedge + güçlü fiyat geçişi + kakao rallisinin TL enflasyon dönemine denk gelmesi. Kakao ≥+%8 günü sonrası 5 gün −179 bps (t −3,3, n=18) → küçük örneklem, eşik seçimi riski → DÜŞÜK.
- Palm yağı (Yahoo'da yok; ZL=F proxy ≈0), fındık (veri yok), arpa (yok; KE=F proxy AEFES pc −0,063 beklenen işaret) → hipotez/DÜŞÜK.
- Alüminyum ALI=F→AEFES pc −0,03 (seri %19 sıfır, illikit) → ÇOK DÜŞÜK.

### 4.6 Olaylar
- AEFES Rusya: işgal haftası −21%/−12% (t0..t4), geçici yönetim kararnamesi −5,6% (t0..t2); devir/yeniden yapılandırma haberleri + (+1,8%/+4,8%).
- BIMAS Mısır devalüasyonları: 5/5 olayda t0..t4 CAR pozitif (+51…+556 bps) — mekanizma ters (Mısır ciro ~%1) → muhtemel tesadüf, DÜŞÜK.
- TÜFE günleri: yalnız AEFES +41 bps (t 2,2; 7 test) → ÇOK DÜŞÜK.

### 4.7 Backtestler (OOS 2021–2026, net)
| Strateji | Maliyet | IS ort. bps (t) | OOS ort. bps (t) | OOS Sharpe |
|---|---|---|---|---|
| B1a kakao_{t−1} → ULKER gün-içi | 8 | −11,0 (−2,4) | −1,9 (−0,3) | −0,12 |
| B1b kakao → ULKER−XU030 gün-içi | 16 | −13,8 | −10,5 (−1,8) | −0,76 |
| B1c kakao 5g → ULKER göreli 5g (haftalık) | 16 | −10,8 | −14,2 | −0,43 |
| B2a ABD risk-off → defansif−XU030 gün-içi | 16 | −16,9 (−1,6) | −3,6 (−0,3) | −0,13 |
| B2b aynı, t..t+4 | 16 | −1,6 | −34,6 (−1,0) | −0,49 |
| B2c XU100≤−%3 → defansif short t+1..t+5 | 16 | −78,9 (−1,4) | +92,1 (+1,4) | +0,70 (IS ters işaret) |
| B3a CCOLA_{t−1} → AEFES gün-içi | 8 | +2,2 (0,5) | −5,2 (−0,8) | −0,33 |
| B3b AEFES−βCCOLA spread geri dönüşü | 16 | −5,9 | −7,7 | −0,27 |
| REF koşulsuz defansif−XU030 gün-içi | 16 | −14,2 (brüt ≈+2) | −18,4 (brüt ≈−2) | −2,18 |
Hiçbir strateji IS ve OOS'ta birlikte pozitif değil; 15 bps'de hepsi daha kötü.

## 5. Karşı argümanlar / kendi bulgumun eleştirisi
- BIST-içi küme (#3) ve XBANK rotasyonu (#6) kısmen **endeks bileşimi mekaniği**: XU100'den artık alınca sektör dışı ağırlıklar ters işaretli kısmi korelasyon üretir. Gerçek ekonomik faktör olduğu argümanı: OOS'ta güçlenme ve tutarlı yıllık işaret.
- AEFES–bira emsalleri: aynı gün Avrupa kapanışı BIST kapanışından 0,5–1,5 saat sonra; küçük bir "sonra" bileşeni var. Saatlik kontrol yapılmadı.
- Kakao rejim gözlemi tek bir büyük döngüye (2023–2025) dayanıyor; "yanlış işaret" de nedensel değil.
- Olay tarihleri (Ağu/Eki-2024, JV 2018) yaklaşık; tek olaylarda t-istatistiği anlamlı değil.
- Defansiflik analizinde XU100'ün kendisi bu hisseleri içeriyor (~%10 ağırlık) → beta hafifçe yukarı yanlı.

## 6. Sınırlamalar
Yahoo verisi (bedelsiz/bölünme sıçramaları temizlendi, ±%10,5), arpa/palm/fındık verisi yok, TÜFE beklenti verisi yok, CCOLA saatlik ~2023-11+, SOKM 2018+. VİOP evening session (19:00–23:00 TSİ) ile ABD kapanışına yakın pozisyon açma test edilmedi. Çin A-hisseleri taramada göründü ama TV'de açılmaz; zaten mekanizmasız.

## 7. TradingView ticker adayları
BIST:AEFES, BIST:CCOLA, BIST:BIMAS, BIST:MGROS, BIST:SOKM, BIST:ULKER, BIST:XU100, BIST:XU030, BIST:XBANK; OMXCOP:CARL_B, EURONEXT:HEIA, EURONEXT:ABI, LSE:CCH, NYSE:BUD, NYSE:KO, NYSE:KOF; AMEX:EEM, TVC:SX5E, SP:SPX, CBOE:VIX, FX:USDTRY, FX_IDC:USDRUB, FX_IDC:USDEGP, FX_IDC:USDMAD?, ICEUS:CC1!, ICEUS:SB1!, CBOT:ZW1!, CBOT:KE1!, CBOT:ZL1!, COMEX:ALI1!, MYX:FCPO1!? (palm, Malezya — Çin DCE yerine). '?' işaretliler ayrıca doğrulanmalı.

## 8. Açık sorular
1. ULKER'in 2021+ USDTRY duyarlılığı bilançodaki net YP pozisyonuyla örtüşüyor mu (çeyreklik)?
2. AEFES'in Rusya varlığının değerlemesi/satış haberi gelecekte hangi olay riskini taşıyor (2026 durumu belirsiz)?
3. Gıda-perakende kümesi: TÜFE gıda sürprizi / asgari ücret / Rekabet Kurumu olay seti ile açıklanabilir mi?
4. VİOP akşam seansında ABD risk-off'a göre defansif-XU030 pozisyonu (gap'i yakalamak) işlenebilir mi?

## Dosyalar
Kod: `code_tuketim/` (common.py, a1_curated.py, a2_defensive.py, a3_scan.py, a4_specific.py, a5_backtests.py, a6_hourly.py, a7_fx_checks.py, build_outputs.py) ve ara çıktılar (a1_curated.csv, a2_*.csv, a3_scan.csv, a4_*.csv, a5_backtests.csv, a6_hourly.csv, a7_fx.csv).
