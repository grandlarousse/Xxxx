# L4 · Takvim ve olay etkileri (1-3 gün, kapanıştan kapanışa)

## Özet

Beklenti kısmen doğru, kısmen yanlış. **Bilanço çevresi etkileri ABD'de artık sağlam değil**: büyük şirketlerde bilanço sonrası sürüklenme (PEAD) 2006'dan beri yok (Martineau 2022), bilanço duyuru primi 2004 sonrası büyük ölçüde kayboldu (Heitz vd. 2020). Endeks ekleme etkisi %7,6'dan (1990'lar) %0,8'e indi (Greenwood ve Sammon 2022). **Klasik ay dönümü ([0:+3]) 2015'ten beri ABD ETF'lerinde anlamsız**; geniş pencere ([-3:+3], Etula vd. 2020) zayıflayarak sürüyor, 2024-2026'da bizim testte negatif. Mayıs 2024'teki T+1 takas geçişi pencereyi bir gün kaydırdı. **FOMC öncesi sürüklenme** 2016-2019'da düz, sonra yeniden pozitif (blog düzeyinde kanıt); yüksek VIX'te güçlü, düşük VIX'te sıfıra yakın. **Tatil öncesi gün** bizim testte 2015 sonrası da pozitif (+8 ile +26 bps/gün, t 1-1,8; gözlem az). **Opsiyon vadesi haftası** literatürün tersine endeks ETF'lerinde 2015 sonrası negatif (SPY 2020-2026 −16 bps/gün fark, t −2,3), vade sonrası hafta pozitif. Hiçbir takvim etkisi tek başına çoklu test düzeltmesini geçecek güçte değil; en iyi kullanım filtre ve konum boyutu ayarıdır. Bugün (21 Kasım 2026): 23-30 Kasım ay dönümü ile Şükran Günü tatil öncesi (25 Kasım) çakışıyor; 18 Aralık üç aylık vade (triple witching) cuması.

## Etki tablosu

Bizim test: `kod/l4_takvim_test.py`, adjclose, 2000-2026-11-20, çıktı `ek/literatur/l4_takvim_hizli_test.csv`. "Fark" = pencere günlerinin ortalama günlük getirisi eksi diğer günler; Welch t.

| etki | kural | kaynak | dönem | büyüklük | 1-3 güne uygunluk | bugünkü durum |
|---|---|---|---|---|---|---|
| Ay dönümü, klasik | T (ayın son işlem günü) .. T+3 uzun | Lakonishok ve Smidt 1988 (RFS); McConnell ve Xu 2008 (FAJ) | 1897-1986; 1987-2005 | ~12 bps/gün (Quantseeker özeti) | Uygun: T-1 kapanışında al, T+3 kapanışında sat (4 gün; 3+1 bölünebilir) | **Kayboldu.** Quantseeker 2025: 2015 sonrası ABD ETF'lerinde anlamsız. Bizim: SPY 2015-26 +0,4 bps fark, t 0,08 |
| Ay dönümü, geniş ("dash for cash") | T-3..T+3 uzun; T-8..T-4 satış baskısı | Etula, Rinne, Suominen, Vaittinen 2020, RFS 33(1) | 1980-2013 (ABD 1995-2013 ana) | S&P 500: T-8..T-4 −0,04%/gün; T-3..T-1 +0,11%; T+1..T+3 +0,13%; ort. gün 0,04%. İki pencere korelasyonu −0,38. Ay sonu cuma ise dönüş 2-3 kat | Uygun: T-4 kapanışında al, T-1'de sat (3 gün); T kapanışında al, T+3'te sat | **Zayıfladı.** Quantseeker: 5-12 bps/gün fark, anlamlı ama son 10 yılda düşüş. Bizim SPY: 2015-26 +3,5 bps t 0,83; 2024-26 −5,9 t −0,79 |
| T+1 takas kayması | 28 Mayıs 2024'ten beri satış baskısı bir gün geç biter: dönüş T-2'de başlar | Nathan, Suominen, Tasa 2026 (çalışma makalesi; Alpha Architect özeti) | 1980-2025 | Kaybeden hisse satışı "exactly one trading day closer to month-end" | Uygun: kuralı T-3 kapanışında al olarak güncelle | Yeni; bağımsız test yok |
| Ay içi momentum döngüsü | Kaybedenler ay sonundan 4 gün önce biten 6 günde düşer | Nathan, Suominen, Tasa 2026 | 1980-2025 | WML yalnız 6 günde $1→$18,78; ayın geri kalanında $2,37 | Kısmen: uzun-kısa gerektirir; uzun tarafta filtre olarak (kaybedenleri T-9..T-4'te alma) | Yeni; yayın sonrası veri yok |
| FOMC öncesi sürüklenme | Toplantıdan önceki kapanışta al, karar günü kapanışında sat | Lucca ve Moench 2015, JF 70(1) | Eyl 1994-Mar 2011, 131 toplantı | 2pm-2pm: 49 bps, t>4,5, Sharpe 1,14. Kapanıştan kapanışa: 33 bps, Sharpe 0,84. İki gün önceki kapanıştan 14:00'e: 54 bps | Uygun ama karar sonrası öğleden sonra gürültüsü dahil | **Tartışmalı.** Kurov, Wolfe, Gilbert 2021 (FRL): 2015 sonrası kayboldu (2019'a kadar). Quantseeker (blog, 1993-2024): SPY Sharpe 0,5-0,6, 2016-2019 düz, sonra canlandı; VIX yüksek çeyrekte güçlü, düşükte ~0 |
| FOMC günü -1 baskısı | Toplantı öncesi gün getirisi ertesi gün tamamen geri döner | Arif, Da, Lin 2025 (çalışma makalesi) | 1996-2021 | Gün −1 ort. 0,05%, gün 0 ort. 0,25% | Uygun (1 gün) | Test edilmedi |
| Makro duyuru günü primi | CPI, PPI, istihdam, FOMC günleri uzun | Savor ve Wilson 2013, JFQA 48(2) | 1958-2009 | 11,4 bps vs 1,1 bps; plansız FOMC günleri −89,2 bps (2001-2009, 15 gün) | Uygun: CPI/NFP 08:30 ET; önceki kapanışta al | **Tartışmalı.** Ernst, Gilbert, Hrdlicka 2021: ayın günü etkisi kontrol edilince olağandışı değil (yalnız arama özeti). NFP ayın ilk cuması → ay dönümüyle karışık |
| Tatil öncesi gün | Tatilden önceki son işlem gününün getirisi (bir önceki kapanışta al, 1 gün) | Ariel 1990, JF | 1963-1982 | doğrulanmadı (bellek) | Tam uygun (1 gün) | **Sürüyor (zayıf t).** Bizim: SPY 2015-26 +7,5 bps t 0,98; 2020-26 +15,7 t 1,84; IWM 2015-26 +18,2 t 1,84; XLF +15,2 t 1,44. Yılda ~9 gözlem |
| Opsiyon vadesi haftası | 3. cumayla biten haftada uzun | Stivers ve Sun 2013, JBF 37(11) | 1988-2010; ana: 28 hisse 1996-2008 | Yüksek opsiyon aktivitesi: alt dönemlerde haftalık fark 67,9 ve 70,7 bps (Quantpedia) | Uygun (haftalık) | **Endekste ters.** Bizim: SPY vade haftası 2015-26 −7,7 bps t −1,67; 2020-26 −16,1 t −2,30; XLE 2015-26 −19,7 t −2,58. Vade sonrası hafta pozitif (SPY 2020-26 +7,7 t 1,1) |
| Bilanço duyuru primi | Bilanço açıklayacak hisseyi duyuru haftası/ayı uzun | Frazzini ve Lamont 2007 (NBER w13090); Barber vd. 2013, JFE 108(1) | 1927-2004; 46 ülke | 61 bps/ay uzun-kısa, t>5, Sharpe 0,94 | Uygun (tarih kapanışta biliniyor) | **ABD'de kayboldu.** Heitz vd. 2020: 2004 öncesi haftalık 32,6 bps, sonrası 23,9 bps daha düşük; ABD dışında sürüyor (UK 88 bps) |
| Bilanço sonrası sürüklenme (PEAD) | Pozitif sürprizi al, 60 gün tut | Bernard ve Thomas 1989; Martineau 2022, CFR 11(3-4) | 1984-2019 | Büyük hisselerde 2006'dan beri yok; mikro hisselerde 2016'dan beri yok | Ufuk uymaz (60 gün) ve büyük hissede etki yok | **Kayboldu.** Karşı görüş: Chan ve Marsh 2024 gece getirisinde sürüklenme (yalnız arama özeti) |
| Emsallere bilgi aktarımı | Erken açıklayanın tepkisi geç açıklayan emsali fiyatlar | Foster 1981; Ramnath 2002; Thomas ve Zhang 2008 | — | doğrulanmadı (bellek): Thomas-Zhang'e göre emsal tepkisi aşırı, kendi duyurusunda geri döner | Uygun ama yön dönüş olabilir | Kaynak açılamadı (arama kotası) |
| S&P 500 ekleme/çıkarma | Ekleme duyurusu sonrası uzun | Greenwood ve Sammon 2022 (NBER w30748) | 1980-2020 | Ekleme: %3,4 (1980'ler), %7,6 (1990'lar), %0,8 (son 10 yıl); çıkarma 2010-2020 −%0,6 | Uygun ama etki küçük | **Kayboldu.** Kanıt zayıf |
| Russell yeniden yapılandırması, çeyrek sonu dengeleme | Haziran son cuması; çeyrek sonu hisse/tahvil dengelemesi | — | — | doğrulanmadı (bellek) | Uygun | Kaynak açılamadı; hipotez olarak test |

## Test edilecek sinyal tanımları

Hepsi KENDI tipi takvim sinyalidir; giriş ve çıkış kapanışta. Uygulanacak dönemler: IS ≤2018, OOS ≥2019, SON ≥2024. Çoklu test: bu dosyada 20'den fazla kural var, Bonferroni ya da Holm ile t eşiği ~3 alınmalı.

1. **TOM7-a:** T-4 kapanışında al, T-1 kapanışında sat. **TOM7-b:** T kapanışında al (T'ye kadar tutuyorsan devam), T+3 kapanışında sat. Ayrıca T cuma ise ayrı raporla.
2. **TOM T+1 düzeltmeli:** 2024-05-28 sonrası T-3 kapanışında al, T kapanışında sat; öncesiyle karşılaştır.
3. **Ay ortası kaçınma filtresi:** T-8..T-4 günlerini diğer sinyallerden çıkar; sinyal getirisinin artıp artmadığına bak.
4. **Tatil öncesi:** NYSE tatilinden önceki son işlem gününün getirisi (bir önceki kapanışta al). Yarım gün (Şükran Günü sonrası cuma, 24 Aralık) ayrı.
5. **FOMC:** ilk toplantı gününden önceki kapanışta al, karar günü kapanışında sat. VIX (^VIX) giriş günü üst yarı/çeyrek koşullu sürüm. Tarihler için federalreserve.gov FOMC takvimi gerekir; veride yok.
6. **Vade sonrası:** 3. cuma kapanışında al, 1/2/3 gün tut. **Vade haftası kaçınma:** 3. cumadan önceki pazartesi-cuma günleri uzun pozisyon açma.
7. **Makro gün:** CPI ve NFP gününden önceki kapanışta al, o günün kapanışında sat; ay dönümüyle çakışanları ayır.
8. **Bilanço:** veri/bilanco_takvimi.csv yalnız 2008-01-03..2011-08-16 arasını kapsıyor ve saat bilgisi yok ("time-not-supplied"); bilanço sinyalleri bugünkü veriyle test edilemez.

## Çalışmayan ya da kaybolanlar

- **Klasik ay dönümü [0:+3]:** 2015 sonrası ABD'de anlamsız (Quantseeker; bizim t 0,08). Kanıt zayıf.
- **PEAD (büyük şirketler):** 2006'dan beri yok (Martineau). Kullanıcının evreni büyük hisse ve ETF; kullanılamaz.
- **Bilanço duyuru primi (ABD):** 2004 sonrası büyük ölçüde kayboldu (Heitz vd.).
- **Endeks ekleme:** %0,8'e indi; işlem maliyeti ve rekabetle birlikte pratikte yok.
- **Opsiyon vadesi haftası uzun:** endeks ETF'lerinde 2015 sonrası işaret tersine döndü. Stivers-Sun bulgusu yalnızca yüksek opsiyon aktivitesi olan büyük hisseler için ve 2008'e kadar.
- **FOMC öncesi:** kalıcı değil; 2016-2019 kesintisi var. Düşük VIX'te sıfıra yakın.
- **Makro duyuru primi:** ayın günü etkisiyle karışık olabilir (Ernst vd. 2021; yalnız özet görüldü).

## İddia defteri

| iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|
| FOMC öncesi 24 saatte S&P 500 +49 bps, 1994-2011 | https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf | "the S&P500 index has on average increased 49 basis points in the 24 hours before scheduled FOMC announcements" | yüksek |
| t istatistiği ve örneklem | aynı | "49 basis points, with a t-statistic of more than 4.5"; "131 scheduled FOMC meetings from September 1994 to March 2011" | yüksek |
| Kapanıştan kapanışa FOMC günü 33 bps, Sharpe 0,84 | aynı | "somewhat lower at about 33 basis points"; "annualized Sharpe Ratio of 0.84" | yüksek |
| 2pm-2pm strateji Sharpe 1,14 | aynı | "would have earned a large annualized Sharpe ratio of 1.14" | yüksek |
| FOMC öncesi sürüklenme 2015 sonrası kayboldu (2019'a kadar) | https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html | Arama özeti: drift "essentially disappeared after 2015" (PDF 404 verdi) | orta |
| FOMC stratejisi 1993-2024: Sharpe 0,5-0,6, 2016-19 düz | https://www.quantseeker.com/p/trading-the-fed-the-pre-fomc-drift | "experienced a flat period between 2016 and 2019 before gaining momentum again in recent years" | orta (blog) |
| FOMC etkisi düşük VIX'te sıfıra yakın | aynı | "significantly stronger during periods of high market volatility while remaining close to zero in low-volatility environments" | orta (blog) |
| FOMC öncesi gün baskısı ertesi gün geri döner | https://www3.nd.edu/~zda/FOMC.pdf | "the day before recent FOMC meetings, while completely reverted the next day" | orta |
| Ay dönümü ABD S&P 500 günlük ortalamaları 1995-2013 | https://acris.aalto.fi/ws/portalfiles/portal/40965155/hhz054.pdf | T-8..T-4 −0.04%; T-3..T-1 0.11%; T −0.04%; T+1..T+3 0.13%; ort. 0.04% | yüksek |
| Ay sonu cuma ise dönüş 2-3 kat | aynı | "two to three times larger whenever the last trading day of the month is a Friday" | yüksek |
| Satış baskısı ve dönüş korelasyonu | aynı | S&P 500 (1995-): −0.38 | yüksek |
| Klasik TOM 2015 sonrası kayboldu | https://www.quantseeker.com/p/turn-of-the-month-strategies-do-they | "has largely disappeared over the past decade, with TOM returns now indistinguishable from returns on other days" | orta (blog) |
| Geniş TOM 5-12 bps fark ama düşüşte | aynı | "approximately 5–12 basis points higher than on other days"; "declined substantially over the past decade" | orta (blog) |
| T+1 takas satış baskısını bir gün kaydırdı | https://alphaarchitect.com/momentum-cycle/ | "shifted exactly one trading day closer to month-end" | orta |
| Momentum 6 günde yoğun | aynı | "$1 into $18.78 over 1980–2025, compared with $2.37 during the rest of the month" | orta |
| Makro duyuru günü 11,4 vs 1,1 bps | https://faculty.wharton.upenn.edu/wp-content/uploads/2012/04/Draft20111128p_edited.pdf | "average announcement day excess return from 1958 to 2009 is 11.4 basis points versus 1.1 basis points" | yüksek |
| Plansız FOMC günleri negatif | aynı | "strongly negative (-89.2 bps for 15 such days between 2001 and 2009)" | yüksek |
| Makro primi ayın günü etkisiyle açıklanır | (arama özeti, Ernst, Gilbert, Hrdlicka 2021; sayfa açılmadı) | "nothing unusual about macroeconomic announcement days" | düşük |
| Bilanço primi 61 bps/ay, t>5 | https://pages.stern.nyu.edu/~afrazzin/pdf/The%20earnings%20announcement%20premium%20and%20trading%20volume%20-%20Frazzini%20and%20Lamont.pdf | "returns of 61 basis points per month (or about 7% per year) with a t-statistic over 5" | yüksek |
| Bilanço primi Sharpe 0,94 | aynı | "annual Sharpe ratio of 0.94" | yüksek |
| Bilanço primi ABD'de 2004 sonrası kayboldu | https://www.iimb.ac.in/ARC2020/Papers/The_Disappearing_Earnings_Announcement_Premium.pdf | "weekly 32.6 bps ... prior to 2004"; "23.9 bps ... lower in the period after 2004" | yüksek |
| Bilanço primi ABD dışında sürüyor | aynı | "after 2004 in the UK, the market-adjusted premium ... remains economically large at 88 bps" | yüksek |
| PEAD büyük hisselerde 2006'dan beri yok | https://cfr.ivo-welch.info/published/papers/martineau2021rest.pdf | "For large stocks, PEAD have been non-existent since 2006 but has only disappeared recently for microcap stocks" | yüksek |
| Kısa ufukta da PEAD yok | aynı | "PEAD is not present for the smallest 'all-but-microcap' stocks and at shorter horizon" | yüksek |
| Vade haftası etkisi alt dönemlerde sürer (1996-2008) | https://quantpedia.com/strategies/option-expiration-week-effect | "average return spreads remain positive at 67.9 and 70.7 basis points" | orta |
| Endeks ekleme etkisi küçüldü | https://www.nber.org/system/files/working_papers/w30748/w30748.pdf | "fallen from an average of 3.4% in the 1980s and 7.6% in the 1990s to 0.8% over the past decade" | yüksek |
| Endeks çıkarma 2010-2020 | aynı | "only -0.6% between 2010 and 2020" | yüksek |
| Vade haftası SPY 2020-2026 negatif | kod/l4_takvim_test.py (bu oturum) | fark −16,1 bps/gün, t −2,30, n=403 | orta (tek test, çoklu test düzeltmesiz) |
| Tatil öncesi SPY 2020-2026 pozitif | kod/l4_takvim_test.py | fark +15,7 bps, t 1,84, n=65 | orta |
| Tatil öncesi etki (Ariel 1990) | — | doğrulanmadı (bellek) | doğrulanmadı (bellek) |
