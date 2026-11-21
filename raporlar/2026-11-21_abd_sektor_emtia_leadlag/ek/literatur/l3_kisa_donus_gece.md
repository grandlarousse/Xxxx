# L3 · Aracın kendi fiyatına dayalı kısa vadeli sinyaller (dönüş, IBS, RSI(2), düşüş serisi, gece/gün içi)

Hazırlayan: alt ajan L3 · 21.11.2026 · Profil: 16:00 ET kapanışta karar ve giriş, 1-3 gün tut, kapanışta çık.

## Özet

- **Endeks ETF'lerinde kısa vadeli dönüş (mean reversion) gerçek ve kalıcı.** Endeks getirilerinin günlük otokorelasyonu 2000'lerden beri 20 endeksin çoğunda negatif. Bunu "endekse karşı işlem" stratejisiyle ölçen çalışma, 1999 sonrası S&P 500 için yıllık Sharpe 0,67 buluyor (Baltussen, van Bekkum, Da 2018). IBS, RSI(2) ve "3 gün düşüş" bu etkinin uygulayıcı biçimleri.
- **Kendi Yahoo verimizle hızlı kontrol (brüt, maliyet öncesi):** QQQ'da IBS<0,2 sinyalinden sonraki günün getirisi 2015-23'te +26 bp (t 3,1), 2024-26'da +23 bp (t 1,4). Aynı dönemlerde koşulsuz günlük ortalama +7 bp. SPY'da sonuç daha zayıf: +12 bp (t 1,7) ve +13 bp (t 1,3). Etki sürüyor ama son 3 yılda istatistiksel olarak zayıf.
- **VIX yüksekken etki büyüyor** (Nagel 2012). Bizim verimizde QQQ için IBS<0,2 ve VIX>25 koşulu birlikteyken getiri 2015-23'te +67 bp (t 2,6). Ancak 2024-26'da bu koşulu sağlayan gün sayısı yalnızca 15.
- **"Kazancın çoğu gecede oluşur" beklentisi kısmen yanlış.** Aylık dönüş stratejisi kârının tamamını gecede kazanıyor (Lou, Polk, Skouras 2019). Günlük IBS sinyalinde ise 2005-23'te kazanç gece ve gün içi arasında bölünüyor; VIX yüksekken çoğunlukla gün içinde oluşuyor. Yalnız 2024-26'da kazanç ağırlıkla gecede.
- **Kaybolan ya da profile uymayan etkiler:** Avrupa açılışındaki gece sürüklenmesi (overnight drift) 2021-25'te sıfıra indi. Gün sonu momentumu ve gün sonu dönüşü son 30 dakikada gerçekleşiyor, bu profille yakalanamaz. Tek hisse dönüşü maliyet sonrası çok küçük (Avramov, Chordia, Goyal 2006). Emtia ve tahvil ETF'lerinde (XLE, GLD, TLT) RSI(2) çalışmıyor.

## Etki tablosu

| etki | kural | kaynak | dönem | büyüklük | 1-3 güne uygunluk | bugünkü durum |
|---|---|---|---|---|---|---|
| Endeks seviyesinde negatif seri bağımlılık | MAC(5): pozisyon = −(4r_t+3r_{t−1}+2r_{t−2}+r_{t−3}), her gün yenilenir | Baltussen, van Bekkum, Da, JFE 2018 | 20 endeks, 1999 sonrası | Yıllık Sharpe 0,63 (tüm endeksler), 0,67 (S&P 500). Yazarlar "maliyet sonrası çoğu yatırımcı için kullanılamayabilir" diyor | Yüksek: bilgi kapanışta biliniyor | Yayın 2018. Mekanizma (endeks ürünleri) büyüyor; bizim verimizde etki sürüyor |
| IBS etkisi (endeks ETF'leri) | IBS=(K−D)/(Y−D) <0,2 ise kapanışta al; ertesi kapanışta ya da IBS>0,8 olunca sat | Pagonidis 2013 (NAAIM), Kinlay özeti | ABD ve ülke ETF'leri, 1990'lar–2013 | IBS<0,2 sonrası ertesi gün ort. +0,35%, IBS>0,8 sonrası −0,13% (Kinlay'in aktarımı). SPY stratejisi 1999-2016 yıllık bileşik ~%13, maliyet hariç | Yüksek | Kinlay: 2015-16'da negatif. Bizim verimiz: QQQ 2024-26 +23 bp (t 1,4), SPY +13 bp (t 1,3), ikisi de brüt |
| IBS + yüksek VIX | IBS<0,2 ve VIX>25 | Nagel, RFS 2012 (mekanizma); kendi testimiz | 1998-2010; 2005-26 | Dönüş stratejisi getirisi kriz dönemlerinde günde ~%1'e çıkıyor (Nagel, hisse düzeyi). QQQ +67 bp (t 2,6), IWM 2005-14 +84 bp (t 3,7) | Yüksek. Kazanç büyük ölçüde ertesi gün içinde | Az sayıda gün var (2024-26'da 15 gün): en güçlü ama en seyrek sinyal |
| RSI(2) < 10 | Connors: 2 günlük RSI<10 ise al, çoğu sürümde kapanış SMA200 üzerindeyken | Connors (kitap), CXO Advisory örneklem dışı testi | SPY 2007-03/2009 | İşlem başına 0,69%, %83 isabet (CXO). CXO'ya göre örneklem dışı kanıt "karışık" | Yüksek | Kendi verimiz: SPY 2015-23 +24 bp (t 2,1), 2024-26 +40 bp (t 1,9). XLE, GLD ve JPM'de sıfır ya da negatif: **kanıt zayıf, araca bağlı** |
| 3 gün üst üste düşüş | Üç kapanış art arda düşükse al, 1-3 gün tut | Uygulayıcı kuralı; akademik kaynağı yok | – | Kendi verimiz: SPY 2015-23 +17,5 bp (t 1,7), QQQ +27 bp (t 2,1) | Yüksek | IBS ve RSI(2) ile büyük ölçüde örtüşüyor; ayrı bir etki değil. **Kanıt zayıf** |
| Hisse düzeyi kısa vadeli dönüş | Son 1 hafta / 1 ayın kaybedenini al, kazananını sat | Jegadeesh 1990, Lehmann 1990 (doğrulanmadı, bellek); Avramov-Chordia-Goyal, JF 2006 | 1960'lar-2000'ler | ACG: "profits are smaller than the likely transactions costs". Haftalık 30-50 bp net (EFMA 2011 çalışması, küçük hisseler hariç) | Orta: haftalık sıklıkta, çok hisse gerektiriyor | Ondalık fiyatlamadan (decimalization) sonra anomali kazançları zayıfladı. Bu profil için brüt olarak ancak marjinal |
| Kalıntı (residual) dönüş | Sektör ya da faktöre göre arındırılmış getiriyle dönüş | Da, Liu, Schaumburg, Mgmt Sci 2014 | 1982-2009 | Riske göre düzeltilmiş getiri standart dönüşün 4 katı | Orta | Tek hisse ve maliyet sorunu sürüyor |
| Kısa vadeli momentum (yüksek işlem hacmi) | 1 aylık getiri × işlem hacmi çift sıralama | Medhat ve Schmeling, RFS 2022 | ABD hisseleri | Düşük hacimli hisselerde dönüş, yüksek hacimlilerde momentum | Düşük: aylık ufuk | Uyarı: likit ve popüler hisselerde dönüş tersine işleyebilir |
| Gece/gün içi çekişmesi | Kârın hangi pencerede oluştuğu | Lou, Polk, Skouras, JFE 2019 | 1993-2013 | Momentum ve dönüş kârının "essentially all" kısmı gecede. CRSP piyasası aylık gün içi %0,38, gece %0,55 | Bilgi amaçlı (aylık ufuk) | Günlük sinyallerde bizim verimiz karışık sonuç veriyor (bkz. Özet) |
| Avrupa açılışında gece sürüklenmesi | ES vadelisi, 02:00-03:00 ET | Boyarchenko, Larsen, Whelan, RFS 2023 + Liberty Street 07/2026 | 1998-2020; 2021-25 | Yıllık 3,7% (günde 1,48 bp). 2021-25'te "close to zero" | Düşük: tek başına işlenemez, ama kapanıştan kapanışa tutulan pozisyon bu pencereyi de taşır | **Yayın sonrası kayboldu** |
| Gece primi (kapanışta al, açılışta sat) | SPY kapanış→açılış | Cliff, Cooper, Gulen 2008 (bellek); Alpha Architect 2020 | 1993-2020 | Kümülatif brüt: gece %717, al-tut %627, gün içi %12. Spread ve komisyon sonrası "low" sağlamlık | Profile uymuyor (açılışta çıkış gerekir) | Maliyet sonrası zayıf. Robot Wealth (2024): Yahoo SPY verisinde gece ağırlığı sürüyor |
| Piyasa gün içi momentumu | İlk yarım saat (ve günün geri kalanı) → son yarım saat | Gao, Han, Li, Zhou, JFE 2018; Baltussen vd., JFE 2021 | 1993-2013; 1974-2020 | R² ~1,6%. Sharpe 0,87-1,73 (varlık sınıfı düzeyi). Etki "reverts over the next days" | **Uymuyor** (giriş 15:30'da olmalı). Dolaylı ipucu: kapanışa doğru kaldıraçlı ETF ve gamma akışı ertesi gün tersine dönüyor | Gamma etkisi sürüyor, kaldıraçlı ETF etkisi azalıyor (Barbon vd.) |
| Gün sonu dönüşü (tek hisse) | Gün içi getiri → son 30 dk ters yönde | Baltussen, Da, Soebhag, çalışma metni 2026 | 1993- | Günde 3,55-6,15 bp (yıllık %8,9-15,4) | **Uymuyor** (gün içi) | Neredeyse her 5 yıllık pencerede anlamlı |
| Kaldıraçlı ETF dengelemesi | Büyük endeks hareketi olan günlerde kapanışa doğru aynı yönde akış | Barbon, Beckmeyer, Buraschi, Moerke 2021/22 | – | Etki "quickly revert at the next day's open" | Orta: kapanışta büyük |r| sinyali → ertesi gün kısmi dönüş | Kaldıraçlı ETF etkisi zamanla "decreasing significantly" |

### Kendi verimizle hızlı kontrol (brüt, ertesi gün kapanıştan kapanışa, bp; ON = gece, ID = gün içi)

| sembol · sinyal | 2005-14 | 2015-23 | 2024-26 | koşulsuz ort. 2015-23 / 2024-26 |
|---|---|---|---|---|
| SPY IBS<0,2 | 22,7 (t 3,2) ON 8,8 / ID 13,8 | 11,9 (t 1,7) ON 6,1 / ID 5,6 | 13,4 (t 1,3) ON 11,1 / ID 2,2 | 5,0 / 6,2 |
| QQQ IBS<0,2 | 19,4 (t 2,7) | 26,1 (t 3,1) ON 10,1 / ID 15,9 | 22,9 (t 1,4) ON 16,6 / ID 6,3 | 7,3 / 6,8 |
| IWM IBS<0,2 | 29,4 (t 3,5) | 11,0 (t 1,6) | 14,1 (t 1,1) | 3,8 / 4,8 |
| SPY RSI2<10 | 25,2 (t 2,1) | 24,3 (t 2,1) | 40,0 (t 1,9) ON 28,5 | 5,0 / 6,2 |
| QQQ IBS<0,2 & VIX>25 | 52,4 (t 2,5) ID 41,4 | 67,1 (t 2,6) ID 49,2 | n=15 | – |
| AAPL IBS<0,2 | – | 32,2 (t 3,5) | 14,9 (t 0,7) | 10,6 / 10,1 |
| MSFT IBS<0,2 | – | 48,9 (t 5,0) | 12,1 (t 0,7) | 11,3 / 5,4 |
| XLK IBS<0,2 | – | 30,9 (t 3,7) | 12,2 (t 0,7) | 8,3 / 8,1 |
| XLE IBS<0,2 / RSI2<10 | – | 13,7 (t 1,4) / 0,3 | −0,6 / −4,8 | 3,8 / 7,1 |
| GLD RSI2<10 | – | −2,8 | −4,0 | 2,7 / 8,3 |
| TLT IBS<0,2 | – | 6,1 (t 1,4) | −0,9 | 0,3 / −0,6 |

Not: Maliyet ve çoklu test düzeltmesi yok, sürüklenme çıkarılmadı (koşulsuz ortalama yanda verildi). 3 günlük tutuşta sinyaller örtüştüğü için t değerleri şişik olur, o yüzden tabloya alınmadı. Betik: `kod/l3_hizli_test.py`, ortak.oku() kullanıyor. Ana backtest'te ortak.py yöntemiyle yeniden çalıştırılmalı.

## Test edilecek sinyal tanımları

Hepsi günlük Yahoo verisiyle (açılış, yüksek, düşük, düzeltilmiş kapanış) t kapanışında hesaplanır. Giriş t kapanışında, çıkış t+1, t+2 ya da t+3 kapanışında. Açılış, yüksek ve düşük fiyatlar adjclose/close katsayısıyla düzeltilir (ortak.oku zaten yapıyor).

1. **IBS** = (K−D)/(Y−D); Y=D olan günler atılır. Giriş IBS<0,2. Çıkış: sabit 1/2/3 gün ya da IBS>0,8 olan ilk kapanış. Filtreler: (a) VIX>20/25, (b) hacim > 20 günlük ortalama (Pagonidis: ABD endeks ETF'lerinde etki yalnız yüksek hacimli günlerde var), (c) K>SMA200 ve K<SMA200 ayrı ayrı.
2. **RSI(2)**: Wilder ortalaması (alpha=1/2). Giriş RSI2<10 (ve <5). Çıkış RSI2>70 ya da K>SMA5.
3. **Düşüş serisi**: art arda 3 (ve 4) düşük kapanış.
4. **MAC(5) endeks dönüşü**: s_t = −(4r_t+3r_{t−1}+2r_{t−2}+r_{t−3}). s_t>0 ise uzun pozisyon. Pozisyon büyüklüğü s_t/σ² ile ölçeklenebilir.
5. **Sektörler arası dönüş**: 11 sektör SPDR'ı 5 günlük getiriye göre sıralanır, en kötü 2 alınır. VIX>25 koşullu ve koşulsuz test edilir (Nagel'in endüstri sonucu).
6. **Büyük hareket sonrası dönüş (kaldıraçlı ETF dengelemesi)**: |r_QQQ,t|>1,5% ise t+1 getirisi r_t'nin işaretine göre ayrıştırılır.
7. **Gece/gün içi ayrımı (her sinyal için tanı)**: ON = A_{t+1}/K_t − 1, ID = K_{t+1}/A_{t+1} − 1. Sinyal kazancının hangi pencerede oluştuğu raporlanır.
8. **Maliyet**: SPY, QQQ, IWM ve sektör SPDR'ları için gidiş-dönüş 2-4 bp, tek hisse için 5-10 bp varsayılır. Kapanış emri (MOC) kullanılır. Sürüklenme düzeltmesi zorunlu: sinyal getirisi eksi aynı dönemin koşulsuz getirisi.
9. **Dönemler**: IS ≤2018, OOS ≥2019, SON ≥2024. Yaklaşık 4 sinyal × 3 eşik × 3 ufuk × 15 sembol test edileceği için Bonferroni ya da White/Hansen benzeri bir çoklu test düzeltmesi gerekir.

## Çalışmayan ya da kaybolanlar

- **Avrupa açılışı gece sürüklenmesi**: yazarların kendisi 2021-25'te "averaged close to zero" diyor. Kapanış dengesizliğinin dağılımı yarıya indi.
- **Saf gece stratejisi (kapanışta al, açılışta sat)**: brüt olarak çarpıcı, ancak spread ve komisyon sonrası istatistiksel sağlamlık düşük (Alpha Architect 2020). Ayrıca bu profile uymuyor.
- **IBS 2015-16'da negatifti** (Kinlay). Bizim verimizde 2024-26'da SPY, IWM, AAPL, MSFT ve XLK'da t<1,5. Etki var ama son dönemde gürültüden zor ayrılıyor.
- **RSI(2) emtia, enerji ve tahvilde çalışmıyor**: XLE, GLD ve TLT'de ortalama sıfır ya da negatif. Connors kitabındaki testlerde veri madenciliği düzeltmesi yok (CXO).
- **Tek hisse kısa vadeli dönüşü**: maliyet sonrası küçük (ACG 2006). Likit, yüksek hacimli hisselerde tersine momentum görülebilir (Medhat-Schmeling 2022).
- **Gün içi momentum ve gün sonu dönüşü**: gerçek etkiler, ancak son 30 dakikada oluşuyor. Bu profil (16:00 ET kapanışta giriş) bunları yakalayamaz.
- **Kaldıraçlı ETF kapanış akışı**: etki zamanla azalıyor (Barbon vd.).

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| Endeks serisi bağımlılığı 2000'lerden beri negatif | https://personal.eur.nl/vanbekkum/2018%20JFE%20BaltussenVanBekkumDa.pdf | "While many studies find serial dependence to be positive until the 1990s, it switches to negative since the 2000s." | yüksek |
| MAC(5) karşıt strateji Sharpe değeri | aynı | "annualized Sharpe ratio of 0.63 (0.67) after March 2, 1999" | yüksek |
| Yazarlara göre maliyet sonrası uygulanabilirlik şüpheli | aynı | "the strategy perhaps is not exploitable to many investors after accounting for transaction costs" | yüksek |
| VIX dönüş getirisini öngörüyor | https://www.nber.org/papers/w17653.pdf | "highly predictable with the VIX index" | yüksek |
| Kriz dönemlerinde dönüş getirisi günde ~%1 | aynı | "close to 1% per day during the LTCM crisis in 1998 and the Nasdaq decline in 2000/01" | yüksek |
| Endüstri portföy dönüşü yalnız VIX yüksekken | aynı | "industry portfolios (which do not yield high returns unconditionally) produce high rates of return ... during times of high VIX" | yüksek |
| IBS<0,2 sonrası ertesi gün getirisi (Pagonidis, aktarım) | https://jonathankinlay.com/?p=2199 | "Average returns when IBS is below 0.20 are .35% ,while average returns when IBS is above 0.80 are -0.13%" | orta (ikincil kaynak) |
| IBS 2015-16'da negatife döndü | aynı | "strategy returns for SPY and EWS have diminished in recent years, turning negative in 2015 and 2016 YTD" | orta |
| IBS etkisi ABD endeks ETF'lerinde yalnız yüksek hacimli günlerde | aynı | "the IBS effect only appears to work on high-volume days" | orta |
| SPY IBS stratejisi yıllık bileşik getirisi, maliyet hariç | aynı | "of the order of 13% for SPY ... ignoring transaction costs" | orta |
| Dönüş ve momentum kârı gecede oluşuyor (aylık) | https://personal.lse.ac.uk/polk/research/TugOfWar.pdf | "essentially all of the abnormal returns on momentum and short-term reversal strategies occur overnight" | yüksek |
| CRSP piyasası gece/gün içi aylık getirisi | aynı | "intraday excess return of 0.38% and an average overnight return of 0.55%" | yüksek |
| Gece sürüklenmesi 2021 sonrası kayboldu | https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/ | "roughly 3.7 percent per annum has averaged close to zero since 2021" | yüksek |
| Kapanış dengesizliği ve gece getirisi bağı zayıfladı | aynı | "The Order-Imbalance–Overnight-Return Relationship Has Broken Down" | yüksek |
| Tek hisse dönüş kârı maliyetin altında | https://econpapers.repec.org/RePEc:bla:jfinan:v:61:y:2006:i:5:p:2365-2394 | "the contrarian trading strategy profits are smaller than the likely transactions costs" (arama özetinden) | orta |
| Kalıntı dönüş standart dönüşün 4 katı | https://ideas.repec.org/a/inm/ormnsc/v60y2014i3p658-674.html | "risk-adjusted return four times the size of the standard reversal strategy" (arama özetinden) | orta |
| Yüksek hacimli hisselerde kısa vadeli momentum | https://econpapers.repec.org/RePEc:oup:rfinst:v:35:y:2022:i:3:p:1480-1526. | "high-turnover stocks exhibit short-term momentum" (arama özetinden) | orta |
| RSI(2) SPY örneklem dışı testi | https://cxoadvisory.com/technical-trading/a-few-notes-on-short-term-trading-strategies-that-work | "0.69% per trade (83% win rate; Jan 2007–Mar 2009" (arama özetinden) | orta |
| Gün içi momentum: son 30 dk, sonraki günlerde tersine dönüyor | https://www3.nd.edu/~zda/intramom.pdf | "The return during the last 30 minutes before the market close is positively predicted by the return during the rest of the day" (arama özetinden) | orta |
| Gün sonu dönüşü günlük getirisi | https://www3.nd.edu/~zda/EOD.pdf | "3.55 to 6.15 basis points per day (8.9% to 15.4% annualized)" | yüksek |
| Kaldıraçlı ETF etkisi açılışta geri dönüyor ve azalıyor | https://ideas.repec.org/p/chf/rpseri/rp2240.html | "quickly revert at the next day's open"; "decreasing significantly over time" (arama özetinden) | orta |
| SPY gece stratejisi maliyet sonrası sağlam değil | https://alphaarchitect.com/trading-costs-wipe-out-the-overnight-return-anomaly/ | "the statistical robustness of any outperformance is low" | yüksek |
| SPY 1993-2020 kümülatif brüt getiri ayrışması | aynı | "717%, 627%, and 12% for the overnight, buy-and-hold, and intraday" | yüksek |
| Kendi verimiz: QQQ IBS<0,2, ertesi gün | yerel: veri/ham/QQQ.csv (l3_test.py) | 2015-23 +26,1 bp t 3,1; 2024-26 +22,9 bp t 1,4 (brüt) | yüksek (hesap), orta (yorum) |
| Kendi verimiz: SPY IBS<0,2, ertesi gün | yerel: veri/ham/SPY.csv | 2015-23 +11,9 bp t 1,7; 2024-26 +13,4 bp t 1,3; koşulsuz 5,0 / 6,2 | yüksek (hesap) |
| Kendi verimiz: VIX>25 iken kazanç gün içinde | yerel | QQQ 2015-23 IBS&VIX>25: toplam 67,1; ON 17,6; ID 49,2 bp | yüksek (hesap) |
| Kendi verimiz: XLE, GLD, TLT'de RSI2/IBS çalışmıyor | yerel | XLE RSI2 2015-23 +0,3 bp; GLD −2,8; TLT IBS 2024-26 −0,9 | yüksek (hesap) |
| Jegadeesh 1990 / Lehmann 1990 aylık ve haftalık dönüş | – | doğrulanmadı (bellek) | doğrulanmadı (bellek) |
| Cooper, Cliff, Gulen 2008: S&P 500 1993-2003 primi gecede | https://arxiv.org/html/2507.04481v1 (arama özeti) | "the equity risk premium is earned entirely overnight" | orta |
