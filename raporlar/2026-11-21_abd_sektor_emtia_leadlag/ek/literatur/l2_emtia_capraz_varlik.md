# L2 · Emtia ve diğer varlık sınıflarından ABD sektörlerine kısa vadeli öncülük

Hazırlanış: 21.11.2026. Profil: kapanışta al, 1-3 gün taşı, kapanışta sat. Kaynakların çoğu yalnız özet sayfasından okundu; tam metin açılamayanlar defterde belirtildi. "Ön hesap" satırları bu oturumda `kod/ortak.py` ile yapılmış tek seferlik korelasyon ve regresyonlardır; backtest değildir.

## Özet

Beklenti büyük ölçüde doğrulandı. Emtia ve çapraz varlık öncülüğünün akademik kanıtı neredeyse tamamen aylık (petrol: Driesprong ve ark. 2008; sanayi metalleri: Jacobsen ve ark. 2019; ABD'den diğer ülkelere: Rapach ve ark. 2013; endüstriler: Hong ve ark. 2007). Günlük ufukta ölçülen gecikme petrolde 7-8 işlem günü, yani tek günlük bir sinyal değil, birkaç haftaya yayılan küçük bir kaymadır. Petrol etkisinin işareti 2008 ortasında tersine döndü (Brigida 2018). Endüstri öncülüğü yeniden incelemede çoğunlukla kayboldu (Tse 2015). Sektör ETF'leri SPY'a öncülük etmiyor (CXO 2021). Kredi ile hisse arasında günlük öncülük yönü hisseden krediye; tersi yalnız olumsuz haberde ve özel bilgiyle var.

Günlük ufukta kanıtı en sağlam olanlar opsiyon akışı (Pan ve Poteshman 2006: ertesi gün 40 bps'nin üstünde), ancak sinyal kamuya açık değil. Kamuya açık sürümü yalnız 1-2 gün öngörüyor, sonra tersine dönüyor. Bu sinyal Yahoo verisiyle test edilemez.

Ön hesabın sonucu da aynı yönde. 2019 sonrasında USO→XLE, GLD→GDX, CPER→COPX, BTC→COIN/MSTR/MARA için ertesi gün korelasyonu sıfıra yakın ya da hafif negatif çıktı. HYG→SPY ve VIX→SPY'daki görünür etki, hedefin kendi geri dönüşü kontrol edilince kayboluyor. Bu iki sinyalin yeni bilgi taşımadığı, yalnızca SPY'ın kısa vadeli geri dönüşünü yakaladığı anlaşılıyor. Kalan adaylar şunlar: VIX vadeli yapısının ters dönmesi (karşıt "al" sinyali), TLT→XLU (IS'de anlamlı, OOS'ta zayıf) ve kripto hafta sonu düşüşünden Pazartesi'ye geçiş. Bu son etki profile uymuyor.

## Etki tablosu

| etki | kural | kaynak | dönem | büyüklük | 1-3 güne uygunluk | bugünkü durum |
|---|---|---|---|---|---|---|
| Petrol → hisse (negatif, gecikmeli tepki) | Aylık petrol getirisi ↑ → gelecek ay hisse ↓ | Driesprong, Jacobsen, Maat 2008, JFE 89(2) | ~30 yıl, aylık, 18 gelişmiş ülke | 18 ülkenin 12'sinde anlamlı (2003 WP özeti); sayısal getiri bu oturumda görülmedi | Düşük: etki ~1 aya yayılıyor, günlük tek gün sinyali değil | 2008 ortasında işaret döndü (Brigida 2018); ön hesap USO→SPY OOS t≈-1.7, SON t≈+1.6 (işaret kararsız) |
| Petrol → ABD endüstrileri | Spot petrol değişimi → endüstri getirisi | Fan ve Jahan-Parvar 2012 (WP 2009) | 49 endüstri, aylık | Endüstrilerin ~1/5'inde anlamlı; gecikme 7-8 işlem günü; vadeli fiyatla zayıf | Düşük-orta: gecikme 1-3 günden uzun | Yayın sonrası test görülmedi; ön hesap USO→XLE/XOP kısmi regresyon OOS t≈+0.5 |
| Petrol → şirket (rejim, büyüklük) | Gecikmeli petrol getirisi → hisse | Narayan ve Sharma 2011, JBF 35(12) | 560 NYSE şirketi | "strong evidence of a lagged effect"; 14 sektörün 5'inde rejime bağlı | Belirsiz (veri sıklığı görülmedi) | doğrulanmadı |
| Sanayi metalleri → piyasa (rejime bağlı) | Aylık metal getirisi 1 sd ↑ → genişlemede hisse ↓, resesyonda ↑ | Jacobsen, Marshall, Visaltanachoti 2019, Mgmt Sci 65(7) | aylık | genişlemede -%1.5/ay, resesyonda +%0.5/ay | Düşük: aylık; rejim etiketi gerekiyor | Ön hesap CPER→FCX OOS t≈-1.9 (negatif); günlük kanıt yok |
| Altın → madenciler | GLD getirisi → GDX ertesi gün | Uygulayıcı ve wavelet çalışmaları (CXO özeti) | — | Kısa vadede ilişki zayıf; öncülük en az ~1 hafta | Düşük | Ön hesap GLD→GDX: IS t≈-0.5, OOS t≈+0.1 (kısmi) → **kanıt zayıf** |
| ABD → diğer ülkeler | ABD'nin geçen ay getirisi → diğer ülkelerin bu ayı | Rapach, Strauss, Zhou 2013, JF 68(4) | 11 ülke, 1980-2010 aylık | Tersi (yabancı → ABD) sınırlı | ABD hedefi için yok | Avrupa'yı genişleten tezde ABD öncülüğü kayboldu (2017) |
| Endüstriler → piyasa | Endüstri getirisi → piyasa (2 aya kadar) | Hong, Torous, Valkanov 2007 JFE; Tse 2015 JEF | 1946-2013 aylık | Tse: 48 endüstrinin yalnız 1-7'si anlamlı | Düşük | **Kaybolmuş / zayıf** |
| Sektör ETF'leri ↔ SPY | Gecikmeli korelasyon | CXO Advisory 2021 | 1998-2021 aylık | Yalnız XLU'nun 1 ay gecikmesi ihtimali | Düşük | Kanıt yok |
| Kredi (CDS) → hisse | CDS'in kendine özgü yeniliği → hisse getirisi | Acharya ve Johnson 2007, JFE 84 | 79 ABD şirketi, 2001-2004 günlük | Yalnız olumsuz haber ve çok bankalı şirketlerde | Orta, ama CDS verisi Yahoo'da yok | Şeffaflık reformlarından sonra zayıfladı (izleyen çalışmalar) |
| Hisse → kredi (ters yön) | Hisse getirisi → CDS getirisi | Hilscher, Pollet, Wilson 2015, JFQA 50(3) | günlük ve haftalık | Hisse öncülük ediyor, CDS etmiyor | Hisse hedefi için yok | Sağlam |
| HYG/LQD → SPY | Bono ETF getirisi → SPY | CXO 2018; Tolikas 2018 | 2007-2018 | Günlükte eşzamanlı; aylıkta LQD < -%1 ise nakit: CAGR %11.1 (SPY %7.3) | Günlükte yok | Ön hesap: HYG→SPY ham t≈-4.3 (OOS); SPY'ın kendi gecikmesi kontrol edilince t≈+0.7 → **etki SPY geri dönüşü** |
| Opsiyon hacmi (özel) | Açılış alımlı put/call oranı düşük − yüksek | Pan ve Poteshman 2006, RFS 19(3) | 1990-2001 günlük kesit | >40 bps ertesi gün, >%1 hafta | Yüksek, ama veri kamuya kapalı | Kamuya açık sürüm yalnız 1-2 gün öngörüyor, sonra tersine dönüyor |
| Put-call parite sapması | Pahalı call − pahalı put hisseleri | Cremers ve Weinbaum 2010, JFQA 45(2) | — | 50 bps/hafta | Orta (opsiyon IV verisi gerekli) | Yazarlar zamanla azaldığını yazıyor |
| IV değişimi kesiti | Geçen ay call IV ↑ al, put IV ↑ sat | An, Ang, Bali, Cakici 2014, JF 69(5) | aylık | ~%1/ay ondalık farkı, 6 aya kadar | Düşük (aylık) | 2008-09'da sürdü (WP) |
| VIX vadeli yapısı (eğim) | Eğim (PC2) → varyans primi | Johnson 2017, JFQA 52(6) | — | Hisse için: WP'de çeyreklik R² %5.2 | Hisse için düşük | Asıl hedefi varyans swapları |
| VIX vadeli yapısı ters (karşıt) | Eğim < 0 (backwardation) → S&P ↑ | Fassas ve Hourvouliades 2019, JRFM 12(3) | 2010-2017 günlük | Slope⁻ katsayısı günlükte -0.1687, 4 ufkun 3'ünde anlamlı; contango anlamsız | Orta-yüksek: bilgi 16:15'te kesinleşir; ^VIX/^VIX3M kapanışta yakın bilinir | Ön hesap VIX/VIX3M → SPY ertesi gün: SON t≈+2.3, OOS t≈+1.7 |
| VIX değişimi → SPY | ΔlogVIX ↑ → SPY ertesi gün ↑ | Ön hesap | 2005-2026 | Ham t≈+2.5 (OOS); SPY gecikmesi kontrol edilince t≈-2.35 | — | **Bağımsız bilgi yok**; geri dönüşün yansıması |
| Kripto hafta sonu → Pazartesi | Hafta sonu kripto ↓ → Pazartesi hisse ↓ | Mourey, Shahrour, Şoiman 2025, FRL 86 | 20 kripto | Asimetrik: yalnız düşüş öngörüyor; LUNA'dan (05/2022) sonra güçlendi | **Uymuyor**: bilgi Cuma kapanışında yok, Pazartesi açılışında fiyatlanıyor | — |
| BTC → kripto hisseleri | BTC dünkü getirisi → COIN/MSTR/MARA | Ön hesap; arXiv 2505.14655 (transfer entropi) | 2019-2026 | Ön hesap: t -0.9 ile +0.9 arası | Düşük | **Kanıt zayıf** (eşzamanlı, gecikmeli değil) |
| Lead-lag ağ kümelemesi | Öncü kümenin dünkü getirisi → takipçi küme | Bennett, Cucuringu, Reinert 2022, Machine Learning | ABD hisseleri, 2000'ler-2019 günlük | Sharpe 0.62 (maliyetsiz), 2.4 bps/gün | Yüksek | 2012 sonrası bozulma; maliyetler dahil değil |

## Test edilecek sinyal tanımları

Hepsi kapanıştan kapanışa, h = 1, 2 ve 3 gün. Her biri ham olarak ve hedefin kendi gecikmeli getirisi kontrol edilerek test edilir. Ön hesap, bu kontrol olmadan çapraz varlık etkisinin geri dönüşle karıştığını gösterdi.

1. **VIX ters yapı:** `^VIX/^VIX3M > 1` (ya da > 1.05) iken SPY/IWM/QQQ al. Değişkenler: VIX9D/VIX ve eşik. Örtüşen olaylar kümelenir.
2. **VIX sıçraması, kısmi:** `zskor(ΔlogVIX) > 2` ve SPY'ın kendi getirisi < -1 sd. Hedeflenen soru: VIX bilgisi geri dönüşe bir şey ekliyor mu?
3. **Petrol şoku, gecikmeli pencere:** 5 ve 10 günlük USO getirisi z > 2 → XLE, XOP ve SPY'ın 1-3 gün ilerisi. Driesprong'daki 7-8 günlük gecikme, tek günlük getiriyle değil birikimli getiriyle aranmalı. 2008 öncesi ve sonrası ayrı ayrı test edilir.
4. **Faiz → faize duyarlı sektörler:** TLT ve ^TNX değişimi → XLU, XLRE, KRE, ITB. IS'de t≈2.2 çıktı, OOS'ta doğrulanmadı.
5. **Metal rejimi:** 21 günlük HG=F/CPER getirisi × rejim (örn. HYG 200 gün ortalamasının altında) → SPY, XLI, FCX.
6. **Kredi kuyruğu:** HYG'nin günlük getirisi < -2 sd iken SPY ve IWM. CXO'nun aylık "sol kuyruk" bulgusunun günlük karşılığı. Kontrol: SPY'ın kendi getirisi.
7. **Petrol ile rafineri farkı:** CL=F ile RB=F/HO=F arasındaki crack değişimi → CRAK, VLO, MPC (önsel).
8. **Kripto, hafta içi:** BTC'nin 15:00-16:00 sonrası hareketi ölçülemez. Bunun yerine BTC'nin geçen 24 saatlik getirisi büyükse (z > 2) COIN, MSTR ve MARA'nın ertesi günü test edilir. Ön hesap negatif, bu yüzden "kanıt zayıf" ön kabulüyle.
9. **Zamanlama kuralı:** CL=F, GC=F ve HG=F'nin Yahoo "close" değeri 16:00 ET'den önce oluşan settlement fiyatı olabilir. Bu doğrulanmadı. 16:00 hizası için USO, GLD ve CPER gibi ETF'ler kullanılmalı. Asya ve Avrupa kapanışları 16:00'da biliniyor, ancak ABD fiyatlarına aynı gün yansımış durumda.

## Çalışmayan ya da kaybolanlar

- **Petrol → piyasa (negatif):** 2008 ortasında işaret değişti, sonrasında risk primiyle tutarlı (Brigida 2018). Ön hesapta 2024 sonrası işaret pozitif ama anlamsız.
- **Endüstri öncülüğü (Hong ve ark. 2007):** Tse 2015'te büyük ölçüde kayboldu.
- **Sektör ETF'leri → SPY:** kanıt yok.
- **HYG/LQD → SPY (günlük):** eşzamanlı. Ön hesaptaki görünür etki SPY'ın kendi geri dönüşünden geliyor.
- **Altın → madenciler, bakır → madenciler, BTC → kripto hisseleri (ertesi gün):** ön hesapta sıfır ya da negatif. Popüler ama **kanıt zayıf**.
- **CBOE hisse put/call oranı ile piyasa zamanlaması:** CXO testinde R² 0.006. Kanıt zayıf, üstelik veri Yahoo'da yok.
- **Lead-lag ağ sinyali:** 2012'den sonra bozuldu. Ortalama 2.4 bps/gün, 5 bps maliyetin altında.
- **Opsiyon akışı sinyalleri:** kanıt güçlü, ancak veri ücretli ya da kamuya kapalı. Kamuya açık sürüm tersine dönüyor.

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| Petrol değişimi dünya hisse getirisini öngörür | https://econpapers.repec.org/RePEc:eee:jfinec:v:89:y:2008:i:2:p:307-327 | "Changes in oil prices predict stock market returns worldwide" | yüksek (özet) |
| 18 ülkenin 12'sinde anlamlı (2003 WP) | https://repub.eur.nl/pub/1017 | "significant predictability in 12 out of the 18 countries" | orta (arama özeti) |
| ABD endüstrilerinin ~1/5'i öngörülebilir; vadeli fiyatla zayıf | https://economics.ecu.edu/wp-content/pv-uploads/sites/165/2019/07/ECU0912.pdf | "statistical support for predictability based on changes in oil future prices is weak" | yüksek |
| Petrolde gecikme 7-8 işlem günü | aynı | "between seven and eight trading days" | yüksek |
| Petrol öngörüsü 2008 ortasında işaret değiştirdi | https://ideas.repec.org/a/eme/sefpps/sef-01-2017-0020.html | "After mid-2008, the predictive relationship switched signs" | yüksek |
| Metal 1 sd ↑ → genişlemede -%1.5/ay | https://pubsonline.informs.org/doi/pdf/10.1287/mnsc.2017.2933 | "price drop of one and a half percent in monthly stock market returns in expansions" | orta (arama özeti) |
| Yabancı → ABD öngörüsü sınırlı | https://econpapers.repec.org/RePEc:bla:jfinan:v:68:y:2013:i:4:p:1633-1662 | "Lagged non-U.S. returns display limited predictive ability with respect to U.S. returns" | orta (arama özeti) |
| Endüstri öncülüğü yeniden incelemede zayıf | https://ideas.repec.org/a/eee/empfin/v34y2015icp195-203.html | "only one to seven industries have significant predictive ability" | orta (arama özeti) |
| Sektör ETF'leri öncülük etmiyor | https://www.cxoadvisory.com/economic-indicators/do-any-sector-etfs-reliably-lead-or-lag-the-market/ | "little evidence that any equity sector ETFs reliably lead or lag" | yüksek |
| Bono ve hisse ETF'leri günlükte eşzamanlı | https://www.cxoadvisory.com/equity-premium/bond-and-stock-etfs-lead-lag/ | "relationships appear unexploitably coincident" | yüksek |
| LQD aylık filtre: CAGR %11.1 / SPY %7.3 | aynı | "7.3%, 8.6% and 11.1%, respectively" | yüksek (IS) |
| Hisse CDS'e öncülük eder, tersi yok | https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/are-credit-default-swaps-a-sideshow-evidence-that-information-flows-from-equity-to-cds-markets/F7CCD2FFB20AAEACE1E093D12EEF7A31 | equity returns lead credit protection returns at daily and weekly frequencies | orta (arama özeti) |
| CDS bilgisi yalnız olumsuz haberde | https://timothyjohnson.web.illinois.edu/papers/JFE_2007.pdf | information revelation occurs only for negative credit news | orta (arama özeti) |
| Put/call: ertesi gün >40 bps | https://nber.org/system/files/working_papers/w10925/w10925.pdf | "by more than 40 basis points on the next day and more than 1% over the next week" | yüksek |
| Kamuya açık opsiyon sinyali yalnız 1-2 gün, sonra geri döner | aynı | "able to predict stock returns for only the next 1 or 2 trade days. Moreover, the stock prices subsequently reverse" | yüksek |
| Put-call parite sapması 50 bps/hafta | https://ideas.repec.org/a/cup/jfinqa/v45y2010i02p335-367_00.html | 50 basis points per week; gradual reduction of the mispricing over time | orta (arama özeti) |
| IV kesiti ~%1/ay | https://www.nber.org/papers/w19590.pdf | spreads in average returns of approximately 1% per month | orta (arama özeti) |
| VIX eğimi hisse için çeyreklik R² %5.2 (WP) | https://www.bauer.uh.edu/departments/finance/documents/seminars/Johnson_020712.pdf | 5.2% adjusted R2 next-quarter | düşük (arama özeti) |
| VIX ters yapısı sonrası S&P pozitif; contango sinyalsiz | https://mdpi-res.com/d_attachment/jrfm/jrfm-12-00113/article_deploy/jrfm-12-00113-v2.pdf | "−0.1687 for daily returns vs. −1.1809 for quarterly returns" | yüksek |
| Contango anlamsız | aynı | "Slope+t was not statistically significant in any instance" | yüksek |
| Kripto hafta sonu düşüşü Pazartesi hisse düşüşünü öngörür | https://ideas.repec.org/p/hal/journl/hal-05415054.html | "negative weekend returns significantly predict Monday equity declines, while positive returns have no effect" | yüksek (özet) |
| Lead-lag küme sinyali Sharpe 0.62, 2.4 bps/gün, maliyetsiz | https://arxiv.org/pdf/2201.08283 | "annualised Sharpe Ratio of 0.62"; "mean daily return of the trading signal is 2.4 basis points" | yüksek |
| Bu sinyal 2012 sonrası bozuldu | aynı | "decay in the performance of the signal after 2012" | yüksek |
| Altın madencileri kısa vadede altına zayıf bağlı | https://www.cxoadvisory.com/gold/gold-futures-vs-gold-miner-stocks/ | gold futures lead miner returns by at least a week | düşük (arama özeti) |
| CBOE hisse put/call → SPY R² 0.006 | https://www.cxoadvisory.com/sentiment-indicators/predictive-power-of-put-call-ratios | R-squared 0.006 | düşük (arama özeti) |
| Ön hesap: HYG→SPY etkisi SPY geri dönüşü | ek/literatur/l2_on_hesap.py | OOS ham corr -0.097; kısmi b_HYG t=+0.69, b_SPY t=-2.13 | orta (tek seferlik) |
| Ön hesap: VIX/VIX3M → SPY ertesi gün | aynı | SON n=725 corr +0.087 t≈+2.3; OOS +0.038 | orta (tek seferlik) |
| Ön hesap: GLD→GDX, USO→XLE ertesi gün yok | aynı | kısmi OOS t: GLD→GDX +0.08, USO→XLE +0.54 | orta (tek seferlik) |
| Driesprong stratejisi makul maliyetle kâr | ECU0912.pdf (Fan ve Jahan-Parvar'ın aktarımı) | "gains from an oil-based active trading strategy in the presence of reasonable trading costs" | orta (ikincil) |
