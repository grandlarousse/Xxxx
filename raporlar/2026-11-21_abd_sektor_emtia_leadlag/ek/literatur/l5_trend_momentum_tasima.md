# L5 · Trend, momentum, rotasyon ve taşıma (carry): kanıt ve 1-3 günlük kapanış alımına uygunluk

Hazırlanış: 21.11.2026. Kaynaklar bu oturumda açıldı; açılamayanlar "doğrulanmadı (bellek)" diye işaretli. Ön hesap: `ek/literatur/l5_on_hesap.py`, sonuç: `ek/literatur/l5_on_hesap_sonuc.txt` (Yahoo paneli 2005-2026; AQR TSMOM verisi 1985-05/2026). Ön hesapta işlem maliyeti ve çoklu test düzeltmesi yok.

## Özet

Akademik trend ve momentum etkileri aylık ufukta bulunmuş, getirinin büyük kısmı 2010 öncesinde kalmıştır. AQR'nin güncel TSMOM (zaman serisi momentumu: son 12 ay getirisi pozitifse al, negatifse sat) faktörünün Sharpe oranı 1985-2009'da 1,41, 2010-2014'te 0,83, 2015-05/2026'da 0,24'tür (t = 0,80). Huang vd. (2020) varlık bazında etkinin zaten zayıf olduğunu gösterir. 9 SPDR sektör ETF'inde 1, 5, 20, 60, 120 ve 252 günlük sıralamayla "en iyi 3 sektörü al, 1 gün tut" rotasyonu iki dönemde de anlamlı değildir. 200 günlük ortalama filtresi getiriyi artırmıyor, yalnız oynaklığı düşürüyor: 2015 sonrasında sektör ETF'leri ortalamanın altındayken ertesi gün ortalaması daha yüksek (9,5 bp, üstündeyken 3,3 bp), ama oynaklık iki katı. Aynı gün ETF'ler arası korelasyon hesaba katılınca hiçbir trend filtresinin t değeri 2,5'i geçmiyor. Emtia ETF'lerinde trend en anlamlı yön filtresi olarak kalıyor (52 hafta zirvesine yakınken 3 günlük ortalama +20,5 bp, kümelenmeli t = 2,15), yine de Harvey-Liu-Zhu'nun t > 3 eşiğinin altında. Taşıma (carry) güçlü bir faktör (çapraz varlık Sharpe 1,1), ama aylık ve vadeli eğrisi verisi gerektiriyor; Yahoo'da en iyi vekili USO/USL ve UNG/UNL farkıdır. Bireysel işlemci kanıtı karamsar: Tayvan'da gün içi işlemcilerin 10'da 8'inden fazlası tipik 6 ayda para kaybediyor. Sonuç: bu yöntemler 1-3 günlük işlemde kâr kaynağı değil, risk ve rejim filtresi olarak kullanılmalı.

## Etki tablosu

| etki | kural | kaynak | dönem | büyüklük | 1-3 güne uygunluk | bugünkü durum |
|---|---|---|---|---|---|---|
| Zaman serisi momentumu (TSMOM) | 12 ay getirisi > 0 ise al, < 0 ise sat; 1 ay tut; oynaklıkla ölçekle | Moskowitz, Ooi, Pedersen 2012, JFE 104 | 58 vadeli, 1985-2009 | Çeşitlendirilmiş portföy "Sharpe ratio greater than one"; AQR verisiyle 1985-2009 SR 1,41 (t 7,06) | Bilgi kapanışta biliniyor; ama ufuk aylık. 1-3 günde yalnız yön filtresi | 2015-05/2026 SR 0,24 (t 0,80); emtia alt faktörü SR 0,15; 2020-2026 emtia SR 0,52 (t 1,32). **Zayıfladı** |
| TSMOM'a itiraz | Varlık bazında regresyon ve bootstrap | Huang, Li, Wang, Zhou 2020, JFE 135 | 55 varlık, 1985-2015 | 55 varlığın 47'sinde t < 1,65; TSMOM ile "tarihsel ortalama" stratejisi aynı getiri | — | Etkinin varlığı tartışmalı; **kanıt zayıf** |
| Sektör (endüstri) momentumu | Geçmiş 1-12 ay endüstri getirisine göre sırala, kazananı al | Moskowitz, Grinblatt 1999, JF 54 | ABD hisseleri, 1963-1995 | 1 aylık ufukta en güçlü (sayı açılmadı) | Aylık. Kendi testimizde 9 SPDR, 1 gün tutma: hiçbir pencerede anlamlı değil | 9 SPDR'de 2015-2026 en iyi 3 - EW: L=20 için 0,53 bp/gün, t 0,58. **Çalışmıyor** (bu evrende) |
| Faktör momentumu | Faktörleri geçmiş 1 ay (ya da 12 ay) getirisiyle sırala ya da işaretiyle al | Arnott, Clements, Kalesnik, Linnainmaa 2018; Ehsani, Linnainmaa 2019/2022 | 51 ve 20 faktör, ABD | 1 ay sıralama: yıllık %10,5, t 5,01; TS faktör momentumu yıllık %4,2, t 7,04; kazançlı yıl sonrası ayda 53 bp, kayıplı yıl sonrası 1 bp | Aylık, uzun-kısa portföy. ETF'lerle (MTUM, QUAL, USMV, VLUE, IWD/IWF) ancak kaba vekil | Endüstri momentumunu kapsıyor. Yayın sonrası ETF düzeyinde test edilmedi |
| 52 hafta zirvesi | Fiyat / 52 hafta zirvesi oranı yüksek olanı al | George, Hwang 2004, JF | ABD hisseleri | (6,6) stratejisi ayda %0,45; Ocak hariç %1,23 | Bilgi kapanışta biliniyor. Kendi testimiz: emtia ETF zirveye %2 yakınken 3 gün +20,5 bp (kümelenmeli t 2,15, 2015-2026); sektör ETF'de 3 gün +5,1 bp, havuz t 1,80 | Emtiada orta, sektörde zayıf |
| Hareketli ortalama filtresi (Faber) | Aylık kapanış 10 ay ortalamasının üstündeyse tut, altındaysa nakit | Faber 2007, J. Wealth Mgmt (2013 güncelleme) | Varlık sınıfları, 1900'ler-2012 | Yazar: "equity like returns with bond like volatility and drawdowns" | Risk filtresi. Kendi testimiz: SPY 2015-2026 SMA200 üstü gün ortalaması 4,7 bp (SR 0,90), altı 8,5 bp (SR 0,68) | **Getiriyi değil oynaklığı ve düşüşü azaltır**; ortalama getiri altta daha yüksek |
| Trend filtresi, sektör ETF | Fiyat > SMA200 ise al | Kendi ön hesap | 9 SPDR, 2005-2026 | 2015-2026 üstü 3,3 bp/gün, altı 9,5 bp/gün (havuz); kümelenmeli t 2,32 / 1,80 | Bilgi kapanışta. Üstündeyken getiri tamamen gece (4,3 bp, gün içi −0,3 bp) | Yön belirleyici değil. Altta ortalama dönüş eğilimi (L3 ile örtüşür) |
| Trend filtresi, emtia ETF | SMA50 > SMA200 ise al | Kendi ön hesap; Erb, Harvey 2006 FAJ | 8 emtia ETF, 2005-2026 | 2015-2026 üstü 4,4 bp/gün, altı −0,4 bp; uzun-kısa SR 0,19 (t 0,66); 2005-2014 SR 0,36 | Bilgi kapanışta; bazı ETF'lerde bayat kapanış (CPER, DBA) | Yön filtresi olarak en iyi aday ama istatistiksel olarak zayıf |
| Emtia taşıma (carry) / vade yapısı | Backwardation'da (vadeli < spot) al, contango'da sat | Koijen, Moskowitz, Pedersen, Vrugt 2018 JFE; Szymanowska vd. 2014 JF; Erb, Harvey 2006 | Çapraz varlık 1980'ler-2012; emtia 1986-2010 | Varlık sınıfı içi ortalama SR 0,74, çeşitlendirilmiş 1,10; baz sıralı spot primi yılda %5-14, vade primi %1-3 | Aylık sinyal, yavaş değişir; 1-3 günde yalnız eğim yönü filtresi. Yahoo'da eğri yok: USO-USL, UNG-UNL, BNO-USO farkı vekil | 2015 sonrası test edilmedi (bu oturumda) |
| Uzun vadeli emtia primi | Eşit ağırlıklı emtia vadeli sepeti | Gorton, Rouwenhorst 2006 FAJ; Erb, Harvey 2006 | 1959-2004 | "same return and Sharpe ratio as equities"; Erb-Harvey: eşit ağırlıklı sepet son 25 yılda "approximately a zero excess return" | Pasif prim, 1-3 günle ilgisiz | İki kaynak çelişiyor; ağırlıklandırmaya bağlı |
| Gece/gün içi ayrışması | Momentum kârları gecede, gün içi zıt | Lou, Polk, Skouras 2019 JFE 134 | ABD hisseleri, 1993-2013 | 14 stratejide kâr ya "entirely overnight" ya "entirely intraday" | Kapanış alımı geceyi yakalar; bu profil için olumlu | Kendi testimiz: SMA200 üstü sektör getirisinin tamamı gece (t 9,5 havuz). Gece kayması zayıflıyor olabilir (L3'e bakın) |
| Kaldıraçlı ETF erimesi | L kat günlük ETF, uzun tutma | Cheng, Madhavan 2009; Avellaneda, Zhang 2010 — **doğrulanmadı (bellek)** | — | Teori: yaklaşık −(L²−L)/2·σ²·T. Kendi ölçüm 2011-2025: NUGT/GDX yılda −15,4 puan, ERX/XLE −8,1, SOXL/SOXX −8,5 (L × taban yıllık getirisine göre) | 1-3 günde erime küçük (σ² × gün); asıl risk 3 kat oynaklık | Geçerli |
| Kaldıraçta 200 gün kuralı | Taban > SMA200 ise kaldıraçlı ETF tut | Gayed vd. "Leverage for the Long Run" — **doğrulanmadı (bellek)**, SSRN açılmıyor | 1928-2015 | Açılmadı | Risk filtresi; erimeyi yüksek oynaklık dönemlerinden kaçarak azaltır | Test edilmeli (hipotez 10) |
| Yayın sonrası zayıflama | — | McLean, Pontiff 2016 JF — **doğrulanmadı (bellek)**: örneklem dışı ~%26, yayın sonrası ~%58 düşüş; Harvey, Liu, Zhu 2016 RFS | 97 anomali; 313 makale | HLZ: yeni faktör için "t-ratio greater than 3.0" | Tüm sinyallere uygulanacak eşik | Trend/momentum için gözlenen düşüş bununla tutarlı |
| Bireysel işlemci sonuçları | — | Barber, Odean 2000 JF; Barber, Lee, Liu, Odean (Tayvan gün içi); Chague vd. 2020 — **doğrulanmadı (bellek)**: Brezilya'da %97 kayıp | ABD 1991-96; Tayvan 1995-99 | En çok işlem yapan hane yılda %11,4, piyasa %17,9; Tayvan'da 10'da 8'den fazlası 6 ayda kaybediyor; küçük bir grup günde 62 bp fark | "Ciddi kazanç" beklentisi çoğunluk için gerçekleşmiyor | Geçerli |

## Test edilecek sinyal tanımları

Tümü t günü 16:00 ET kapanışıyla hesaplanır, t kapanışında girilir, t+1/t+2/t+3 kapanışında çıkılır. Raporlanacak: işlem başına ortalama bp, isabet, **gün kümelenmeli t** (aynı gün sinyal veren ETF'lerin ortalaması tek gözlem), 2005-2014 ve 2015-2026 ayrı, gece ve gün içi pay, gidiş-dönüş 2-5 bp maliyet sonrası, sinyalsiz koşulsuz ortalamaya göre fark.

1. **Rejim filtresi (SPY > SMA200):** sektör ETF'lerinde alım yalnız bu koşulda. Ölçüt getiri değil: oynaklık, en kötü %5 gün, en büyük düşüş.
2. **Emtia trendi:** GLD, SLV, USO, UNG, DBA, DBC, DBB, CPER için SMA50 > SMA200 ve 12 ay getirisi > 0 → al. Uzun-kısa ve yalnız uzun ayrı.
3. **Emtia 52 hafta zirvesi:** kapanış ≥ 0,98 × 252 gün en yüksek → 3 gün tut.
4. **Taşıma vekili:** USO'nun 20 günlük getirisi − USL'nin 20 günlük getirisi > 0 (eğri backwardation'a dönüyor) → USO/XLE/XOP al. Aynı kural UNG−UNL ve BNO−USO için.
5. **Emtia kesitsel momentumu:** 8 emtia ETF'ini 63 gün getirisiyle sırala, en iyi 2'yi al, 3 gün tut.
6. **İnce endüstri momentumu:** SMH, XBI, KRE, ITB, XME, XOP, OIH, IGV, XRT, IYT, KIE, TAN, URA, JETS, XHB, KBE'yi 21 gün getirisiyle sırala, en iyi beşte biri al (9 SPDR'de çalışmadı; ince endüstride ayrıca sına).
7. **Faktör ETF momentumu:** MTUM, QUAL, USMV, VLUE, IWD, IWF, IWN, IWO, SPHB, SPLV, RSP, COWZ; 21 gün getirisi en yüksek 3 → al.
8. **Gece momentumu (Lou-Polk-Skouras):** sektör ETF'lerinde son 20 günün gece getirisi toplamı en yüksek 3 → kapanışta al. Gece ve gün içi pay ayrıca.
9. **Trend altında ortalama dönüş:** sektör ETF fiyat < SMA200 ve günü negatif kapattı → al (2015 sonrası gün içi pozitif bileşen; L3 ile çakışma kontrolü).
10. **Kaldıraç filtresi:** SOXL, TQQQ, UPRO, ERX yalnız taban > SMA200 iken; taban altında ise nakit. Aynı sinyal taban ETF ile karşılaştırılır.

## Çalışmayan ya da kaybolanlar

- **TSMOM 2015 sonrası:** AQR'nin kendi güncel faktörü SR 0,24; hisse endeksi bileşeni negatif (−0,02). Emtia bileşeni 2020-2026'da toparlanıyor (SR 0,52) ama t 1,32.
- **9 SPDR sektör rotasyonu (1 gün tutma):** 1-252 gün tüm pencerelerde 2015-2026 t < 1. 2005-2014'te 1 günlük sıralamada ters yön vardı (dünün kazananı −3,2 bp/gün, t −3,26); 2015 sonrası kayboldu.
- **"Altın kesişim" ve SMA200'ü getiri artırıcı sanmak:** sektör ETF'lerinde 2015 sonrası ortalama altında daha yüksek. Popüler; getiri için **kanıt zayıf**, risk için geçerli.
- **12 ay momentum filtresi sektörde:** 2015-2026'da 12 ay getirisi negatif sektörler ertesi gün daha iyi (11,6 bp'ye 3,0 bp havuz; kümelenmeli t 1,48). Yön filtresi olarak tersine dönmüş.
- **Popüler ama test edilmemiş kurallar:** RSI, MACD, "dual momentum" gibi kurallar için bu oturumda hakemli ve yayın sonrası kanıt bulunmadı; **kanıt zayıf** sayılmalı ve yalnız ön kayıtlı testle kullanılmalı.
- **Kaldıraçlı ETF'yi trendde uzun tutmak:** güçlü yükseliş yıllarında L × tabandan iyi olabilir (bileşik etki), oynak yıllarda belirgin geride. 15 yılın 11-12'sinde UPRO, ERX, NUGT ve UCO L × tabanın gerisinde kaldı.

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| TSMOM çeşitlendirilmiş portföy Sharpe > 1 | https://pages.stern.nyu.edu/~lpederse/papers/TimeSeriesMomentum.pdf | "yielding a Sharpe ratio greater than one on an annual basis, or roughly 2.5 times the Sharpe ratio for the equity market" | yüksek |
| TSMOM 1-12 ay sürer, sonra döner | https://pages.stern.nyu.edu/~lpederse/papers/TimeSeriesMomentum.pdf | "The positive t-statistics for the first 12 months indicate significant return continuation or trends." | yüksek |
| AQR TSMOM 2015-05/2026 SR 0,24 | https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Time-Series-Momentum-Factors-Monthly.xlsx | Kendi hesap: 1985-2009 SR 1,41 (t 7,06); 2010-14 0,83; 2015-26 0,24 (t 0,80) | yüksek |
| TSMOM varlık bazında zayıf | https://alphaarchitect.com/2020/03/an-empirical-challenge-for-trend-following/ | "47 of the 55 assets have a t -statistic of less than 1.65" | yüksek |
| TSMOM ile tarihsel ortalama stratejisi aynı | https://alphaarchitect.com/2020/03/an-empirical-challenge-for-trend-following/ | "TSM and TSH perform virtually the same" | yüksek |
| Endüstri momentumu 1 ayda en güçlü | https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2018/03/Juhani.pdf | "this predictability is at its strongest at the one-month horizon (Moskowitz and Grinblatt 1999)" | yüksek |
| Faktör momentumu 1 ay sıralama | https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2018/03/Juhani.pdf | "annualized average return of 10.5% with a t-value of 5.01" | yüksek |
| Faktör momentumu kazançlı/kayıplı yıl sonrası | https://www.nber.org/system/files/working_papers/w25551/w25551.pdf | "1 basis point following a year of losses and 53 basis points following a positive year" | yüksek |
| TS faktör momentumu getirisi | https://www.nber.org/system/files/working_papers/w25551/w25551.pdf | "annualized return of 4.2% ( t-value = 7.04)" | yüksek |
| 52 hafta zirvesi stratejisi büyüklüğü | https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf | "all around 0.45% per month"; Ocak hariç "from 0.45 to 1.23%" | yüksek |
| Momentum kârı gecede oluşuyor | https://personal.lse.ac.uk/polk/research/TugOfWar.pdf | "profits are either earned entirely overnight (for reversal and a variety of momentum strategies) or entirely intraday" | yüksek |
| Carry, varlık sınıfı içi ve çeşitlendirilmiş Sharpe | https://www.nber.org/system/files/working_papers/w19325/w19325.pdf | "annualized Sharpe ratio of 0.7 on average ... diversified across all asset classes earns a Sharpe ratio of 1.1" | yüksek |
| Emtia baz sıralı primler | https://econpapers.repec.org/RePEc:bla:jfinan:v:69:y:2014:i:1:p:453-482 | "spot premia between 5% and 14% per annum and term premia between 1% and 3% per annum" | yüksek |
| Emtia vadeli = hisse getirisi ve Sharpe | https://www.nber.org/system/files/working_papers/w10595/w10595.pdf | "Fully-collateralized commodity futures have historically offered the same return and Sharpe ratio as equities" | yüksek |
| Eşit ağırlıklı emtia sepeti sıfıra yakın | https://www.nber.org/system/files/working_papers/w11222/w11222.pdf | "equally weighted long-only portfolio of commodity futures returns has approximately a zero excess return over the past 25 years" | yüksek |
| Momentum + vade yapısı taktiği daha iyi | https://www.nber.org/system/files/working_papers/w11222/w11222.pdf | "tactical strategies provide higher average returns and lower risk than a long-only commodity futures exposure" | yüksek |
| Faber modeli: risk azaltır | https://mebfaber.com/wp-content/uploads/2016/05/SSRN-id962461.pdf | "achieving equity like returns with bond like volatility and drawdowns" | yüksek |
| Yeni faktör için t > 3 | https://www.nber.org/system/files/working_papers/w20592/w20592.pdf | "a newly discovered factor needs to clear a much higher hurdle, with a t-ratio greater than 3.0" | yüksek |
| Anomali yayın sonrası zayıflar (%26 / %58) | McLean, Pontiff 2016 JF (sayfa açılamadı) | örneklem dışı ~%26, yayın sonrası ~%58 düşüş | doğrulanmadı (bellek) |
| Çok işlem yapan hane geride | https://econpapers.repec.org/RePEc:bla:jfinan:v:55:y:2000:i:2:p:773-806 | "those that trade most earn an annual return of 11.4 percent, while the market returns 17.9 percent" | yüksek |
| Gün içi işlemcilerin çoğu kaybeder | https://faculty.haas.berkeley.edu/odean/papers/Day%20Traders/Day%20Trade%20040330.pdf | "in the typical six month period, more than eight out of ten day traders lose money" | yüksek |
| Küçük bir yetenekli grup var | https://faculty.haas.berkeley.edu/odean/papers/Day%20Traders/Day%20Trade%20040330.pdf | "stocks they buy outperform those they sell by 62 basis points per day" | yüksek |
| Brezilya gün içi işlemcilerin %97'si kaybetti | Chague, De-Losso, Giovannetti 2020 (SSRN, açılmadı) | %97 | doğrulanmadı (bellek) |
| Sektör SMA200 altı ertesi gün daha yüksek (2015-26) | ek/literatur/l5_on_hesap_sonuc.txt | üstü 3,3 bp (t 4,37 havuz), altı 9,5 bp (t 4,11 havuz); kümelenmeli t 2,32 / 1,80 | orta (ön hesap) |
| 9 SPDR rotasyonu 1 gün tutmada sonuçsuz | ek/literatur/l5_on_hesap_sonuc.txt | 2015-26 L=20 en iyi3−EW 0,53 bp/gün, t 0,58; L=252 t 0,29 | orta (ön hesap) |
| Emtia ETF 52 hafta zirvesi 3 gün | ek/literatur/l5_on_hesap_sonuc.txt | 2015-26 +20,5 bp, kümelenmeli t 2,15 | orta (ön hesap) |
| Emtia trend uzun-kısa zayıf | ek/literatur/l5_on_hesap_sonuc.txt | SMA50>200 uzun−kısa SR 0,36 (2005-14), 0,19 (2015-26), t 0,66 | orta (ön hesap) |
| SPY SMA200: getiri değil oynaklık | ek/literatur/l5_on_hesap_sonuc.txt | 2015-26 üstü 4,7 bp, sd 82 bp; altı 8,5 bp, sd 199 bp | orta (ön hesap) |
| Kaldıraçlı ETF erimesi ölçümü | ek/literatur/l5_on_hesap_sonuc.txt | NUGT/GDX −15,4 puan/yıl; 12/15 yıl L×tabanın gerisinde | orta (ön hesap) |
