# L1 · ABD hisselerinde günlük çapraz öncülük (lead-lag)

Hazırlanma: 21.11.2026. Kapsam: günlük frekansta "A'nın bugünkü getirisi B'nin yarınki getirisini öngörür mü" etkileri; profil = kapanışta al, 1-3 gün tut, kapanışta sat. Web arama kotası 16. çağrıdan sonra doldu (oturum sınırı); sonraki bulgular açılan PDF'lerden ve evrendeki Yahoo verisiyle yapılan **ön testten** (`kod/l1_leadlag_hizli.py`, çıktılar `ek/backtest/l1_hizli_*.csv`) geliyor. Ön test resmi backtest değildir: hayatta kalma yanlılığı var (evren bugünkü hisseler), çok adımlı ufuklarda t değerleri örtüşen getirilerle şişkin.

## Özet

Klasik "büyük hisse küçüğe öncülük eder" etkisi (Lo-MacKinlay 1990, Chordia-Swaminathan 2000) günlük ölçekte 2000'lerin başında büyük ölçüde kayboldu: Tóth-Kertész NYSE'de "lead-lag ... vanished in less than twenty years" diyor. ETF düzeyinde ön testimiz daha da ileri gidiyor: SPY/QQQ'nun bugünkü getirisi IWM ve IJR'ın yarınki getirisini **ters** yönde öngörüyor (2020-26: t = -4,7), bu da endeks ürünleriyle gelen negatif seri bağımlılıkla (Baltussen-van Bekkum-Da 2019) uyumlu. Yani "SPY yükseldi, yarın IWM yetişir" kuralı bugün çalışmıyor.

Hâlâ iz bırakan tek aile **grup (sektör) içi yayılım**: hissenin kendi grubu (kendisi hariç) bugün ne yaptıysa hisse yarın kısmen yetişiyor (Hou 2007 mekanizması). Ön testte 594 ABD hissesinde "geride kalan" uzun-kısa kantil yayılımı günde 13 bp (2005-09) → 10 → 7 → 2,6 bp (2020-26, t = 1,2) düştü; etkinin neredeyse tamamı **ertesi gecede** (kapanıştan açılışa) oluşuyor, gün içi payı sıfır ya da negatif. Bu, kapanışta alan profile uygun, ama günde %100'e yakın devir ve 2×(2-5) bp maliyetle 2020 sonrası net kazanç sıfıra yakın. Ağ/makine öğrenmesi yöntemleri (Bennett vd. 2022, Cartea-Cucuringu-Jin 2023) maliyet öncesi Sharpe 0,6-2 raporluyor, ama ilki 2012 sonrası bozulma, ikincisi ilişkilerin 6 ayda değiştiğini söylüyor. Tek başına işlem sinyali olarak zayıf; ek filtre (bilanço günü, büyük lider hareketi, küçük/az takip edilen hisse) ile test edilmeli.

## Etki tablosu

| etki | kural | kaynak | dönem | büyüklük | 1-3 güne uygunluk | bugünkü durum |
|---|---|---|---|---|---|---|
| Büyükten küçüğe (boyut) | Büyük hisse portföyü t getirisi → küçük portföy t+1 | Lo-MacKinlay 1990 (RFS; NBER w2977); Chordia-Swaminathan 2000 (JF, hacim) | 1962-87 haftalık; 1963-96 günlük/haftalık | Büyüklük sayısı açılan metinde yok (doğrulanmadı) | Bilgi 16:00'da biliniyor | **Kayboldu**: Tóth-Kertész günlük korelasyon 0,15-0,2'den hata düzeyine (1980'ler→1990 sonu). Ön test SPY→IWM 2020-26 b = -0,29 (t -4,7), ters işaret |
| Hacim/spread kanalı | Büyük hisse spread'i yüksekken büyüklerin sipariş akışı küçükleri öngörür | Chordia-Sarkar-Subrahmanyam 2007 (NY Fed SR 303; sonra RFS 2011) | 1988-2002 dolayı (doğrulanmadı) | Nitel | Günlük veriyle spread yok; hacim vekil olabilir | Ölçülmedi; ETF düzeyinde ters işaret baskın |
| Sektör içi yayılım (Hou) | Sektör içi büyükler → küçükler; kötü haberde daha yavaş | Hou 2007 (RFS 20(4)) | 1963-2001 haftalık (doğrulanmadı) | "predominantly intra-industry" (özet) | Uygun; ön testte kazanç ertesi gece | **Zayıfladı**: ön test L/S 13 → 2,6 bp/gün; FM katsayısı t 3,7/5,6/2,0/1,8; 2024-26 t 0,05 |
| Sektör → piyasa | Bazı sektörler piyasaya 1-2 ay öncülük eder | Hong-Torous-Valkanov 2007 (JFE) | 1946-2002 aylık | 34 sektörden 13'ü 1 ay öncülük | **Aylık**, günlük kanıt yok | Kanıt zayıf (günlük için) |
| Granger liderleri | Her hisse için t>2 lider seti, lider sinyali → takipçi | Scherbina-Schlusche (RF 2020) | 1929-2011 aylık/haftalık | Aylık L/S %0,61 (t 6,2) EW, %0,45 (t 3,4) VW | Haftalık sürümü 5 güne yakın; günlük sürüm yok | Değerli ağırlıkta zayıf; yayın sonrası bilinmiyor |
| Ekonomik bağlar | Müşteri/tedarikçi, ortak analist, teknoloji, coğrafya | Cohen-Frazzini 2008 (JF) ve diğerleri | 1980-2004 aylık | Aylık %1,5 dolayı (doğrulanmadı, bellek) | **Aylık**; günlük veriyle bağ verisi yok | 1-3 gün için kanıt yok |
| Kümelenmiş lead-lag ağı | 500 likit NYSE hissesi, öncü küme → takipçi küme | Bennett-Cucuringu-Reinert 2022 (Machine Learning 111) | 2000-2019 günlük | Sharpe 0,62, günlük 2,4 bp, **maliyet hariç** | Uygun (kapanış verisi) | **2012 sonrası bozulma** (yazarlar) |
| Lévy-alanı lider/takipçi | İkili Lévy alanı + korelasyonla sıralama, liderlerin geçmiş getirisiyle takipçide pozisyon | Cartea-Cucuringu-Jin 2023 (SSRN 4599565; Jin 2025 tez) | Dönem açılmadı; en büyük %25 (~550) hisse | Yıllık >%20, Sharpe >2; "after accounting for industry standard transaction costs" | Haftalık portföy; ilişki 6 ayda bozuluyor | Bağımsız tekrar yok; yeni ve tekrar edilmemiş |
| Endeks seri bağımlılığı | Endeks getirisi negatif oto-korelasyon (çapraz değil) | Baltussen-van Bekkum-Da 2019 (JFE) | 20 endeks, 1951-2016 | AR(1) ~+0,05 → 2000'lerde negatif; MAC(5) ters strateji Sharpe 0,63-0,67 | Uygun; ETF'te de geçerli | Lead-lag'in yerini aldı: ETF çiftlerinde ters işaret bunu yansıtıyor |
| Ön test: ETF çiftleri | Öncü ETF t → takipçi ETF t+1 (takipçinin kendi t kontrol) | Bu çalışma | 2005-2026 | 14 çiftte 2020-26'da pozitif anlamlı yok; SPY→IWM, QQQ→IWM, SPY→IJR, XLF→KRE, SPY→XBI negatif (t -3,3…-4,7) | — | Klasik "+" yön çalışmıyor |
| Ön test: grup içi "geride kalan" | gap = grup ort. (kendisi hariç) − kendi getiri; üst %20 al, alt %20 sat | Bu çalışma (594 hisse, 49 grup) | 2005-2026 | t+1: 13,0/9,9/7,2/2,6 bp; t+3 toplam: 28/17/11/9 bp | Kazancın çoğu gece (2005-19 gece payı %48-71) | Maliyet sonrası 2020+ ~0 |

## Test edilecek sinyal tanımları

Hepsi `ortak.py` kurallarıyla: t kapanışında sinyal, t kapanışında giriş, h = 1/2/3 çıkış; IS ≤ 2018, OOS ≥ 2019, SON ≥ 2024. Maliyet: likit ETF 2 bp, büyük hisse 3-5 bp, küçük hisse 10 bp tek yön.

1. **Grup içi geride kalan (G1).** `gap_i = mean(r_j, j∈grup, j≠i) − r_i`. Kesitte üst kantili al. Varyant: yalnız gruplar içinde sıralama (sektör nötr); gece (açılış/önceki kapanış) ve gün içi ayrı raporla. Not: bu sinyal tek hisse kısa vadeli dönüşü de içerir; FM regresyonunda `r_i,t` kontrolüyle saf grup katsayısını ayrıca raporla.
2. **Lider bilançosu yayılımı (G2).** `veri/bilanco_takvimi.csv` ile: grubun en yüksek dolar hacimli hissesi bilanço açıkladığında tepki günü t'deki lider getirisi; aynı gruptaki diğerlerinin t+1..t+3 getirisi (Hou'nun mekanizması). Bilanço çoğunlukla kapanış sonrası açıklandığından tepki günü ertesi seanstır; t kapanışında bilinir.
3. **Büyük lider hareketi koşulu (G3).** G1'i yalnız `|grup_haric_t| > 2 × 60 günlük σ` günlerinde uygula. Yayılımın haber günlerinde yoğunlaştığı varsayımı.
4. **Kötü haber asimetrisi (G4).** G1'in yalnız negatif kolu (grup sert düştü, hisse düşmedi → kaçın/sat). Hou: yavaş uyum "negative information" kaynaklı.
5. **Az likit yarı (G5).** G1'i grup içinde 60 günlük dolar hacmi medyanının altındaki hisselerle sınırla. Ön test: 13,1 → 4,2 bp (2020-26, t 1,0).
6. **ETF → küçük bileşen (G6).** SMH → AMKR, ACLS, FORM, AEHR, ONTO, CAMT; KRE → ZION, WAL, KEY, CFG; XOP → AR, RRC, APA. Kural: `ETF_t − beta × hisse_t > 1σ` ise hisseyi al.
7. **ETF çiftleri (E1).** Ters yönlü hipotez: büyük ETF'in sert günü küçük ETF'te ertesi gün dönüş (SPY→IWM, SPY→IJR, XLF→KRE). Çok test düzeltmesi zorunlu (14 çift × 4 dönem × 3 ufuk).
8. **Madenci-altın göreli yakınsama (E2).** `sign(GLD_t − GDXJ_t)` yönünde GDXJ−GLD göreli pozisyon; ön test 2015-26'da günde 9-14 bp göreli. Lead-lag değil çift yakınsaması; e2 (değerli metal) notuyla çakışabilir.

## Çalışmayan ya da kaybolanlar

- **Büyükten küçüğe günlük lead-lag (ETF düzeyinde): kayboldu, işaret döndü.** Tóth-Kertész 1990'ların sonunda; ön testte 2020-26'da 5 çiftte anlamlı negatif. "SPY yükseldi, IWM yarın yetişir" popüler ama **kanıt zayıf / ters**.
- **Sektör → piyasa günlük:** kanıt aylık; günlük için **kanıt zayıf**.
- **Ekonomik bağ (müşteri-tedarikçi vb.) 1-3 gün:** kanıt aylık, bağ verisi Yahoo'da yok; **kanıt zayıf**.
- **Bennett vd. küme sinyali:** maliyet hariç 2,4 bp/gün ve 2012 sonrası bozulma; maliyet sonrası muhtemelen sıfır.
- **Grup içi yayılım 2024-26:** FM katsayısı 0,001 (t 0,05), saf grup L/S −2,8 bp. Son dönemde yok sayılacak kadar zayıf.
- Genel uyarı: makine öğrenmesi lead-lag makaleleri (Cartea vd.) yüksek Sharpe raporluyor ama bağımsız tekrar yok; ilişkiler 6 ayda değişiyor, yani her ay yeniden tahmin gerekiyor ve aşırı uyum riski yüksek.

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| Günlük lead-lag NYSE'de kayboldu | https://arxiv.org/pdf/physics/0506071 | "lead-lag relationships between daily returns of stocks vanished in less than twenty years" | yüksek |
| Büyük→küçük günlük korelasyon hata düzeyine indi | https://arxiv.org/pdf/physics/0506071 | "From about 0.15–0.2 it decreased under the error-level by the end of the nineties" | yüksek |
| Tóth-Kertész verisi | https://arxiv.org/pdf/physics/0506071 | "daily closing prices of 116 large stocks from NYSE" 1982-2000 | yüksek |
| Endeks seri bağımlılığı negatife döndü | https://personal.eur.nl/vanbekkum/2018%20JFE%20BaltussenVanBekkumDa.pdf | "While many studies find serial dependence to be positive until the 1990s, it switches to negative since the 2000s." | yüksek |
| Değişim endeks ürünleriyle bağlantılı | https://personal.eur.nl/vanbekkum/2018%20JFE%20BaltussenVanBekkumDa.pdf | "the decline in serial dependence links to the increasing popularity of index products" | yüksek |
| Ters MAC(5) stratejisi Sharpe | https://personal.eur.nl/vanbekkum/2018%20JFE%20BaltussenVanBekkumDa.pdf | "annual Sharpe ratio of 0.63 (0.67) after March 2, 1999" | yüksek |
| Lo-MacKinlay: çapraz kovaryans kontrarian kârı açıklar | https://www.nber.org/system/files/working_papers/w2977/w2977.pdf | "show the presence of important lead—lag relations across securities" | yüksek |
| Chordia-Swaminathan: yüksek hacim düşüğe öncülük | https://econpapers.repec.org/RePEc:bla:jfinan:v:55:y:2000:i:2:p:913-935 | "Daily and weekly returns on high volume portfolios lead returns on low volume portfolios, controlling for firm size" (arama özeti) | orta |
| Büyük hisse spread'i yüksekken lead-lag artar | https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr303.pdf | "The lead-lag relation between large and small stocks increases with lagged spreads of large stocks." | yüksek |
| Hou: lead-lag esas olarak sektör içi | https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html | "predominantly intra-industry"; "sluggish adjustment to negative information" (arama özeti) | orta |
| Hong-Torous-Valkanov: sektörler piyasaya öncülük (aylık) | https://escholarship.org/content/qt6x49x543/qt6x49x543.pdf?t=krnr78 | "industries such as retail, services, commercial real estate, metal, and petroleum lead the stock market by up to two months" | yüksek |
| Scherbina-Schlusche L/S büyüklüğü (aylık) | https://escholarship.org/content/qt9pc1b5j5/qt9pc1b5j5.pdf?t=old1k2 | "0.61% with a t-statistic of 6.20, and 0.45% with a t-statistic of 3.39" | yüksek |
| Scherbina-Schlusche: değer ağırlıklı daha zayıf | https://escholarship.org/content/qt9pc1b5j5/qt9pc1b5j5.pdf?t=old1k2 | "value-weighted portfolios generate lower return differentials than equal-weighted portfolios" | yüksek |
| Bennett vd. Sharpe ve günlük getiri | https://arxiv.org/pdf/2201.08283 | "annualised Sharpe Ratio of 0.62"; "mean daily return of the trading signal is 2.4 basis points" | yüksek |
| Bennett vd. 2012 sonrası bozulma | https://arxiv.org/pdf/2201.08283 | "there is a decay in the performance of the signal after 2012" | yüksek |
| Bennett vd. maliyet hariç | https://arxiv.org/pdf/2201.08283 | "we do not take into account transaction costs when calculating the profit of our signal" | yüksek |
| Bennett vd. örneklem | https://arxiv.org/pdf/2201.08283 | "5325 NYSE equities spanning from 04-01-2000 to 31-12-2019"; en hacimli 500 | yüksek |
| Cartea-Cucuringu-Jin performansı | https://ora.ox.ac.uk/objects/uuid:173a88b2-f00c-4346-8868-aabbd97ec8d7/files/dt722h970m | "annualized returns ... over 20% and the Sharpe ratio of the portfolios are above 2" | orta (tez özeti, makale açılmadı) |
| Cartea vd. ilişkiler kısa ömürlü | https://ora.ox.ac.uk/objects/uuid:173a88b2-f00c-4346-8868-aabbd97ec8d7/files/dt722h970m | "rarely remains profitable after 6 months because the lead-lag relationship changes" | orta |
| Cartea vd. maliyet sonrası | https://ora.ox.ac.uk/objects/uuid:173a88b2-f00c-4346-8868-aabbd97ec8d7/files/dt722h970m | "economically significant after accounting for industry standard transaction costs" | orta |
| Ön test: SPY→IWM 2020-26 ters işaret | ek/backtest/l1_hizli_etf_cift.csv | b = -0,285, t = -4,67 (n = 1731 gün) | orta (yerel ön test) |
| Ön test: 14 ETF çiftinde 2020-26 pozitif anlamlı yok | ek/backtest/l1_hizli_etf_cift.csv | en yüksek t_F1 = 1,23 (ITB→XHB) | orta |
| Ön test: grup içi FM katsayısı düşüşü | ek/backtest/l1_hizli_grup_ici.csv | b_grup t: 3,66 / 5,58 / 1,96 / 1,80 / 0,05 (2024-26) | orta |
| Ön test: geride kalan L/S t+1 | ek/backtest/l1_hizli_grup_ici.csv | 12,99 / 9,92 / 7,21 / 2,62 bp/gün (t 1,21 son dönem) | orta |
| Ön test: kazanç gecede | ek/backtest/l1_hizli_grup_ici.csv | grup katsayısı gece t 4,90, gün içi t −1,43 (2020-26) | orta |
| Ön test: az likit yarıda daha güçlü | ek/backtest/l1_hizli_grup_ici.csv | 13,06 → 4,16 bp (küçük); büyük yarı 0,30 bp (2020-26) | orta |
| Hou 2007 örneklem ve haftalık frekans | — | 1963-2001 haftalık | doğrulanmadı (bellek) |
| Cohen-Frazzini müşteri momentumu | — | aylık ~%1,5 L/S, 1981-2004 | doğrulanmadı (bellek) |
