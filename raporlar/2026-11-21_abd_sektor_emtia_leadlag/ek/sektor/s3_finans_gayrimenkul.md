# S3 Finans ve gayrimenkul

## Özet

Grup son haftada sert satış yedi: XLF 5 günde -%7,0, KRE -%6,1, GS -%13,7, MS -%13,1; VIX 35,9 (5 günde +%86). Yıl içinde kazananlar sigorta (TRV +%37, ALL +%30, CB +%20), CBOE (+%44) ve sağlık/veri merkezi GYO'ları (WELL +%31, EQIX +%29); kaybedenler kripto zinciri (BTC -%33, COIN -%55, MSTR -%49, IREN -%69), alternatif yöneticiler (KKR -%30, BX -%25, CG -%37) ve mortgage GYO'ları (AGNC -%19). Fed'in 8-9 Aralık'ta faiz artırması bekleniyor; ^TNX 4,91 (YTD +%18).

1-3 günlük vadede en sağlam aday bir öncü değil, **koşullu dönüş**: XLF/KRE/KIE'de IBS < 0,2 ve VIX > 25 iken kapanışta al, 3 gün taşı (2005-14 ve 2015-23'te ayrı ayrı pozitif; şu an koşul açık). Çapraz öncülerin çoğu (BTC -> madenci, kredi -> alternatif yönetici, getiri eğrisi -> bölgesel banka) bizim taramamızda sıfır ya da ters çıktı. Madenciler artık BTC'den çok yapay zekâ bulut hisseleriyle (CRWV) birlikte hareket ediyor.

## Araç tablosu

Sayılar ozet_istatistik.csv'den: h = 20 günlük ortalama hacim (milyon $), σ = günlük oynaklık %, β = SPY betası.

| Alt sektör | Ana ETF | Kaldıraçlı/ters | Öncü hisseler | Yüksek betalı takipçiler | Not |
|---|---|---|---|---|---|
| Büyük banka ve yatırım bankası | XLF (h 2.255, σ 0,98) | FAS 3x / FAZ -3x (h 63 / 64; net gider %0,88 / %1,03) | JPM (2.353, σ 1,46), BAC (1.762), GS (2.013, σ 2,12), MS (1.181), C (1.215), WFC (1.031) | GS (β 1,69), MS (1,47), C (1,31), COF (σ 1,95), IBKR (σ 2,55, β 1,94) | XLF'nin ~%26'sı yalnız üç banka dışı adda (BRK-B %12,3, V %8,2, MA %5,9); bankalar endeksin %28'i: saf banka teması değil. Banka için hisse sepeti ya da KBE daha temiz |
| Bölgesel banka | KRE (h 1.084, σ 1,28), KBE (133) | DPST 3x (h 24,9, gider %0,92, eşit ağırlıklı S&P Regional Banks); likit ters ETF yok | PNC (384), USB (377), TFC (369), FITB (314), KEY (296), HBAN (293), RF (288), CFG (240) | WAL (h 68, σ 2,03, β 1,09), ZION (98), FLG (64, σ 1,80), CFG (β 0,89) | DPST hacmi sınırda; 3x ve dar hacim birlikte kayma riski. KRE 2023+ döneminde XLF'den bağımsız dönüş vermiyor |
| Aracı kurum, borsa, alternatif yönetici | IAI (h 13,6: likit değil) | yok | SCHW (843), BLK (783), CME (598), BX (596), ICE (582), KKR (458), APO (452), CBOE (415), IBKR (397) | ARES (σ 2,78), BX (2,44), KKR (2,42), CG (2,40), LPLA (2,48), HOOD | CME (β -0,25) ve CBOE (β -0,42) piyasa düşerken kazanan oynaklık hisseleri; alternatif yöneticilerle aynı sepete konmamalı |
| Sigorta | KIE (h 82, σ 1,08) | yok | TRV (604), CB (576), PGR (551), ALL (424), MET (331), AIG (297), PRU (226) | MET (β 0,64), PRU (0,66); P&C betaları negatif | Düşük oynaklık: 1-3 günde getiri küçük. Ama dönüş sinyalleri en istikrarlı burada (aşağıda) |
| Fintech ve kripto | IBIT (h 2.088, σ 2,83), BITO (572), WGMI (24, σ 5,43); BLOK (10,9) ve BITQ (3,6) likit değil | BITX 2x BTC (h 93, σ 5,61); CONL 2x COIN (h 55, σ 9,03, YTD -%89); ters BTC ETF evrende yok | MSTR (2.223), HOOD (1.723), COIN (1.232), SOFI (942), PYPL (624), XYZ (556) | IREN (σ 6,99), CIFR (7,23), HUT (7,00), APLD (6,69), CLSK (6,05), WULF (5,99), RIOT (5,70), MARA (5,58), CORZ (4,89), UPST (4,08) | Madenciler 2026'da yapay zekâ barındırma hisselerine dönüştü: son 6 ayda CORZ-CRWV korelasyonu 0,78, CORZ-IBIT 0,31. BTC teması için COIN (0,80) ve MSTR (0,84) |
| GYO ve mortgage GYO | IYR (h 546), VNQ (380), XLRE (343; σ ~0,9) | 3x GYO (DRN/DRV) evrende yok; REM (h 15,7) likit değil | WELL (804), EQIX (770), AMT (531), DLR (524), PLD (472), O (387), PSA (372), CCI (381) | IRM (β 1,32, σ 2,16), CBRE (2,20), CCI (2,27), SBAC (2,34), DLR (β 0,99); mREIT: AGNC (223), NLY (221) | GYO'lar düşük oynaklık; 1-3 günde faiz duyarlılığı baskın. Veri merkezi GYO'ları (EQIX, DLR, IRM) teknoloji betası taşır |

## 1-3 günlük sürücüler ve öncü göstergeler

Kendi hızlı taramamız (kod: ortak.tarama ve islem_testi, kapanıştan kapanışa, öncü t günü 16:00 ET'de bilinen bilgi; dönemler 2010-26, 2016-22, 2023-26). Sonuçlar eleme amaçlıdır, çoklu test düzeltmesi yapılmadı.

**Çalışan ya da yakın olanlar**
- **Koşullu dönüş, VIX yüksekken.** IBS (kapanışın gün içi aralıktaki yeri) < 0,2 ve VIX > 25 iken kapanışta al: XLF 3 günlük ortalama 2005-14'te 139 bp (t 2,4), 2015-23'te 94 bp (t 2,5); KRE 187 / 99 bp; KIE 78 / 79 bp. Koşulsuz 3 günlük ortalama ~14-19 bp. 2024-26'da yalnız 11-18 işlem var, sınanamadı. Mekanizma Nagel'in (NBER w17653) bulgusu: likidite sağlamanın getirisi VIX ile artar. Not: 3 günlük t değerleri örtüşme düzeltmesiz; gerçek t daha düşük. Şu an VIX 35,9: koşul açık.
- **Sigortada sade dönüş.** KIE 5 günde -%3'ten fazla düştükten sonra 3 günlük ortalama 52 / 66 / 79 bp (üç dönemde t 1,5 / 2,0 / 2,5). Az ama istikrarlı.
- **TLT -> GYO, ertesi gün (+).** TLT bugünkü getirisi ile XLRE/VNQ/IYR yarınki getirisi: t ≈ 4 (2010-22), t ≈ 1 (2023+). Eşikli işlem testi (TLT z > 1) maliyet sonrası anlamlı değil (VNQ 10 bp, t 1,7). ^TNX değişimi -> AGNC 2023+ t -2,0: faiz şoku mREIT'e gecikmeli geçiyor.
- **KRE -> BAC (+), yalnız 2023+.** t 3,5; 2010-22'de ters (-2,7). Rejim değişimi; tek dönemlik, şüpheli.

**Çalışmayanlar (listedeki hipotezlerle çelişen kanıt)**
- **Büyük banka -> bölgesel banka.** JPM, XLF, SPY getirisi ertesi gün KRE'yi ters yönde öngörüyordu (2010-22 t -4 ile -6: kısa vadeli dönüş). 2023+ sıfıra yakın (t -1 ile -1,7). JPM z < -1,5 sonrası KRE alımı 2023+ net -6,5 bp.
- **Bitcoin -> COIN, MSTR, madenciler.** IBIT (16:00 kapanışı) ertesi gün MSTR'yi ters yönde (t -2,3), madencileri sıfır ya da ters öngörüyor. COIN sert yükselişi sonrası MARA ertesi gün düşme eğiliminde (COIN z > 1,5 iken MARA açığı 2023+ 133 bp, t 1,8, n 75). Yani öncülük yok; varsa aşırı tepkinin dönüşü.
- **Kripto zamanlama tuzağı.** BTC-USD Yahoo çubuğu UTC gece yarısı (ET 19:00/20:00) kapanır. Hizalama testimizde BTC-USD günlük getirisi IBIT'in ertesi gece getirisiyle 0,32 korelasyonlu: BTC-USD'nin "bugün"ü 16:00'da bilinmez. 16:00 bilgisi için IBIT/BITO kullan.
- **Kredi spreadi -> alternatif yönetici.** HYG, JNK, HYG-IEF -> BX/KKR/APO/ARES: t -2 ile +2 arasında, dönemler arası işaret değişiyor.
- **Getiri eğrisi -> bölgesel banka.** 10y-3a eğim değişimi -> KRE t -1,5 (beklenenin tersi işaret), 2023+ sıfır.
- **VIX -> borsalar.** dVIX -> CBOE/CME 2010-22 t +3,4 / +5,9; 2023+ t -3,3 / -1,9. İşaret döndü.

**Veri ve açıklama saatleri**: Fed H.8 (banka mevduat ve kredileri) her cuma 16:15 ET: kapanıştan sonra, etkisi pazartesi. FOMC kararları 14:00 ET: kapanıştan önce biliniyor. Bilanço: büyük bankalar açılış öncesi açıklar (JPM Q4 2026 sonuçları 14 Ocak 2027, yaklaşık 06:45 ET); alternatif yöneticiler ve sigortacıların bir kısmı kapanış sonrası.

## 2026 durumu ve takvim

- **Faiz.** Enflasyon enerjiyle hızlandı (Eylül TÜFE %3,7). Piyasa Aralık'ta 25 bp artış fiyatlıyor; Citi indirimin Haziran 2027'den önce gelmeyeceğini düşünüyor. ^TNX 4,91. Yükselen faiz mREIT'leri (AGNC 3 ayda -%27, NLY -%25) ve büyük GYO'lardan PLD'yi (-%14) vurdu. Sağlık ve depolama GYO'ları dirençli.
- **Kasım satışı.** SPY 5 günde -%8,6, VIX 35,9. Yatırım bankaları (GS, MS) ve alternatif yöneticiler en sert düşenler; sigorta ve CME/CBOE hafif. Alternatif yöneticilerdeki yıllık düşüş 2026 boyunca süren özel kredi kaygısıyla açıklanıyor: yazılım şirketlerine verilen kredilerde yapay zekâ riski, temerrüt artışı (Fitch: Ocak 2026'ya kadar %5,8) ve fonlarda rekor geri çekme talepleri. Kasım'daki son ayağın (GS, MS dahil) özel bir finans haberi bulunamadı; kaynaklar Kasım satışını yapay zekâ hisselerindeki çöküş ve Fed artış beklentisine bağlıyor.
- **Kripto.** BTC 58.799 $ (1 ayda -%28). Haberlere göre Temmuz'dan beri en düşük seviye; Fed artış beklentisi ve hisse satışıyla aynı anda. Kasım düşüşünde öne çıkan nedenler: spot BTC ETF'lerinden 5-13 Kasım arası yaklaşık 1,91 milyar $ çıkış, kaldıraçlı uzun pozisyon tasfiyeleri, faiz artışı beklentisi ve Strategy (MSTR) talebinin zayıflaması. Gider oranları: CONL %1,04-1,15 (kaynaklar farklı, ihraççıdan doğrulanmadı); BITX için kaynaklar %1,85 ile %2,75 arasında çelişiyor (ihraççıdan doğrulanmadı). DRN/DRV hâlâ işlemde (Direxion sayfası, gider %0,98 / %1,06 net) ama evrenimizde yok; DPST için 2026'da ters bölünme ya da kapanış haberi bulunamadı (son ters bölünme Haziran 2023, 1'e 10). CONL ve BITX gibi kaldıraçlı ürünler yılda -%67 ile -%89 kaybetti.
- **Takvim.** 26 Kasım Şükran Günü borsa kapalı, 27 Kasım 13:00 ET erken kapanış (NYSE takvimi); 24 Aralık da 13:00 erken kapanış. Her cuma 16:15 H.8. **8-9 Aralık FOMC** (projeksiyonlu): artış olasılığı yüksek. Kasım TÜFE **10 Aralık 08:30 ET** (FOMC'den sonra), Kasım ÜFE 15 Aralık, Aralık TÜFE 13 Ocak 2027 (BLS). Büyük banka Q4 bilançoları Ocak 2027 ortası: JPM 14 Ocak 2027 (diğer bankaların tarihi bulunamadı). Fed stres testi sonuçları yaz aylarında.

## Tuzaklar

- **Kaldıraç erimesi.** FAS ve FAZ'ın ikisi de 3 yılda kaybettirebilir; FAZ 3 yılda -%77. CONL 3 yılda -%90, BITX -%39. 1-3 gün taşımada erime küçük, ama yüksek VIX'te günlük yeniden dengelemenin maliyeti büyür. Sinyal ana ETF'de test edilip kaldıraçlıda uygulanırsa kayma ayrıca ölçülmeli.
- **Likidite.** IAI, BLOK, BITQ, REM, PHO pratikte işlenmez. DPST (25 milyon $) ve WGMI (24 milyon $) sınırda.
- **Tek hisse ve olay riski.** Bölgesel bankalarda tek bankanın kredi zararı açıklaması bütün grubu düşürür (2023 SVB tipi). MSTR bilançosu BTC'ye kaldıraçlı; COIN düzenleme haberleriyle sıçrar. Sigortada kasırga ve afet haberleri (sezon 30 Kasım'da biter). Bilanço günlerinde 1-3 günlük sinyal bilanço tepkisine boğulur: bilanço öncesi kapanışta yeni pozisyon açma.
- **Rejim değişimi.** Bu grupta 2010-22'de çalışan dönüş ve VIX ilişkileri 2023'ten sonra zayıfladı ya da işaret değiştirdi. Uzun örnekleme güvenme; her sinyal 2023+ alt döneminde ayrıca geçmeli.
- **Zaman uyumsuzluğu.** BTC-USD ve DX-Y.NYB gibi 16:00'dan sonra kapanan seriler bir gün kaydırılmadan öncü olarak kullanılırsa sahte öncülük üretir.

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| FAS 3x, FAZ -3x; net gider %0,88 / %1,03 | https://www.direxion.com/uploads/FAS-FAZ-Fact-Sheet.pdf | "Daily Target 300% -300% ... Net Expense Ratio* 0.88% 1.03%" | yüksek |
| XLF endeksinde ilk ağırlıklar banka dışı | https://www.direxion.com/uploads/FAS-FAZ-Fact-Sheet.pdf | "Berkshire Hathaway Class B 12.34 JP Morgan Chase 11.70 Visa Incorporation 8.15 Mastercard 5.93" | yüksek |
| XLF endeksi mortgage GYO'larını da içerir | https://www.direxion.com/uploads/FAS-FAZ-Fact-Sheet.pdf | "financial services; insurance; banks; capital markets; mortgage real estate invest[ment trusts]" | yüksek |
| DPST 3x, gider %0,92, eşit ağırlığa yakın bölgesel banka endeksi | https://www.direxion.com/uploads/DPST-Fact-Sheet.pdf | "Daily Target 300% Gross Expense Ratio 0.92% Net Expense Ratio* 0.92%" ; ilk 10 ağırlık ~%1,1-1,15 | yüksek |
| Fed H.8 cuma 16:15 ET'de yayımlanır | https://www.federalreserve.gov/releases/h8/ | "These data are released each Friday, generally at 4:15 p.m." | yüksek |
| 2026'nın son FOMC toplantısı 8-9 Aralık (projeksiyonlu) | https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm | "September 15-16* ... October 27-28 ... December 8-9*" | yüksek |
| Piyasa Aralık artışını fiyatlıyor; Citi 25 bp artış bekliyor | https://investinglive.com/central-banks/icymi-citi-now-expects-a-december-fed-rate-hike-after-hotter-september-us-inflation/ | "Markets price roughly a 94% chance of a December hike" (14.10.2026) | orta |
| Eylül 2026 TÜFE %3,7; indirim Haziran 2027'den önce yok (Citi) | aynı | "September CPI rose to 3.7% y/y from 3.4%" ; "cuts not starting until June 2027" | orta |
| BTC Temmuz'dan beri en düşükte, Fed artış beklentisiyle | aynı sayfa, başlık listesi | "Bitcoin hits lowest since July as Fed hike talk and a Wall Street rout collide" | orta (yalnız başlık) |
| Dönüş getirisi VIX ile öngörülebilir | https://www.nber.org/papers/w17653.pdf | "highly predictable with the VIX index" | yüksek |
| Aykırı: eski bir zamanlama anomalisi 2021 sonrası kayboldu | https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/ | "has averaged close to zero since 2021" | yüksek |
| XLF/KRE/KIE IBS<0,2 & VIX>25 -> 3 günlük getiri pozitif | kendi taraması (kod/l3_hizli_test.py) | XLF 139/94 bp, KRE 187/99 bp, KIE 78/79 bp (2005-14/2015-23) | orta (örtüşme düzeltmesiz t) |
| JPM/XLF -> KRE ertesi gün dönüşü 2023+ kayboldu | kendi taraması (ortak.tarama) | JPM->KRE t -6,2 (2010-26), -1,7 (2023-26) | orta |
| IBIT -> madenci öncülüğü yok; madenciler CRWV ile hareket ediyor | kendi hesabı (2026-05-20 sonrası korelasyon) | IBIT->MSTR t -2,3; CORZ-CRWV 0,78, CORZ-IBIT 0,31 | orta |
| BTC-USD çubuğu 16:00'dan sonra kapanıyor | ek/hizalama_testi.csv | BTC-USD -> IBIT ertesi gece farkı 0,315 | yüksek |
| Alternatif yönetici düşüşü özel kredi kaygısından (2026 geneli) | https://www.morningstar.com/stocks/why-alts-manager-stocks-are-getting-hit-hard | "Jitters about private credit markets" ; Fitch temerrüt %5,8 (Ocak 2026) | orta (Kasım'a özgü haber yok) |
| Özel kredi fonlarında rekor geri çekme talepleri | https://finance.yahoo.com/news/week-slump-asset-manager-stocks-133000629.html | "redemption requests in private credit funds hit record levels" | orta |
| BTC Kasım düşüşü: ETF çıkışı ve tasfiye | https://cointelegraph.com/news/bitcoin-four-month-low-62k-crypto-market-selloff | "Net outflows totaled approximately $1.91 billion between November 5 and November 13" | orta |
| CONL gider oranı | https://etfdb.com/etf/CONL/ | 1.04% (başka kaynaklar 1.10-1.15%) | düşük-orta |
| BITX gider oranı | https://www.theblock.co/etfs/bitcoin/bitx | "1.85% management fee ... total expense ratio of 2.75%" (SoFi 2.38%) | düşük (çelişkili) |
| DRN/DRV net gider %0,98 / %1,06 | https://www.direxion.com/product/daily-real-estate-bull-bear-3x-etfs | "0.98 / 0.98" ; "1.07 / 1.06" (gross/net) | yüksek |
| DPST'nin son ters bölünmesi 2023 | https://finance.yahoo.com/news/direxion-announces-reverse-split-dpst-203004684.html | 1-for-10, "after the close of the markets on June 2, 2023" | orta |
| Şükran Günü 26 Kasım kapalı, 27 Kasım 13:00 erken kapanış | https://www.nyse.com/trade/hours-calendars | "close early at 1:00 p.m. ... on Friday, November 27, 2026" | yüksek |
| Kasım 2026 TÜFE 10 Aralık | https://www.bls.gov/schedule/news_release/cpi.htm | "November 2026 Dec. 10, 2026 08:30 AM" | yüksek |
| JPM Q4 2026 sonuçları 14 Ocak 2027 | https://www.financialcontent.com/article/bizwire-2025-5-21-jpmorganchase-announces-conference-calls-to-review-first-quarter-second-quarter-third-quarter-and-fourth-quarter-2026-earnings | "Thursday, January 14, 2027 ... approximately 6:45 a.m. (Eastern)" | orta (Mayıs 2025 duyurusu) |

## Boşluk kapatma (22.11.2026)

Web aramasıyla kapatılanlar: Şükran Günü (26 Kasım kapalı, 27 Kasım 13:00 erken kapanış; NYSE). Kasım TÜFE tarihi 10 Aralık 08:30 (BLS), yani 8-9 Aralık FOMC'den sonra. JPM Q4 bilançosu 14 Ocak 2027, açılış öncesi. Alternatif yönetici düşüşü: 2026 boyunca özel kredi kaygısı (yazılım kredileri, temerrüt, geri çekme talepleri) kaynaklı; Kasım'a özgü finans haberi bulunamadı. BTC Kasım düşüşü: ETF çıkışı, kaldıraç tasfiyesi, faiz beklentisi. DRN/DRV gider oranları Direxion'dan eklendi; DPST için 2026'da bölünme/kapanış haberi yok. Açık kalanlar: CONL ve BITX gider oranları kaynaklar arasında çelişkili (ihraççı sayfası açılmadı); JPM dışındaki büyük bankaların bilanço tarihleri.
