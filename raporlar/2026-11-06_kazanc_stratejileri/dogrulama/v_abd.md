# ABD raporlarının çekişmeli doğrulaması (v_abd)

Tarih: 2026-11-06. Doğrulanan raporlar (`ajanlar/` altında):
- `abd_kim_kazaniyor.md` (K)
- `abd_swing_kenarlar.md` (S)
- `abd_test.md` (T) ve kodu `hesaplar/abd_test/`

## 0. Yöntem ve sınırlar

- **Web araması kullanılamadı.** Oturumun ortak WebSearch kotası (200) bu ajan başlamadan dolmuştu; ilk üç arama reddedildi. Kural gereği arama motorlarını başka yoldan sorgulamadım.
- **Yerine üç yol kullandım:**
  1. Bildiğim birincil kaynak URL'lerini doğrudan okudum (WebFetch, varsayılan başlıklar). Bunlar SEC EDGAR 10-K, federalreserve.gov, tcmb.gov.tr, NBER/IDEAS özetleri, makale PDF'leri, organizatör verisi, AAII ve IRS.
  2. Raporların ham verisinden (Ken French, FRED, Chen-Zimmermann 2026.10) temel sonuçları **kendi bağımsız kodumla** yeniden hesapladım.
  3. Analitik kontroller yaptım: ardışık kayıp olasılığı (DP) ve Monte Carlo.
- **Erişilemeyenler:** SSRN (403), Bloomberg (paywall), BusinessWire (403). Bunlara dayanan iddialar DOGRULANAMADI. Bellekten teyit ettiklerim "(bellek)" etiketli.
- Hesap dosyaları: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/v_abd/spot.py` ve aynı klasördeki çıkarılmış PDF metinleri.

## 1. Hüküm tablosu: karar için en önemli iddialar

| # | İddia (rapor) | Hüküm | Düzeltme / not | Kaynak |
|---|---|---|---|---|
| 1 | Jane Street 2025 net trading revenue 39,6 mlr $ (K) | DOGRU (BAS) | Reuters, "belgeleri görmüş" (24.04.2026); resmî rakam değil. 2024'ün 20,5 mlr $'ı bu kaynakta yok → DOGRULANAMADI | https://www.marketscreener.com/news/jane-street-s-40-billion-trading-haul-tops-rivals-sources-say-ce7f59dfdf8ff52d |
| 2 | Citadel Securities 2025 12,2 mlr $ (K) | DOGRULANAMADI | Paywall. URL başlığı "record $12 billion" diyor; büyüklük tutarlı | bloomberg.com (erişilemedi) |
| 3 | Virtu trading income 2.436,7 mn $ (+%33,7), net kâr 912 mn $ (K) | DOGRU (REG) | 10-K: 2.436.707 / 1.822.437 bin $ | https://www.sec.gov/Archives/edgar/data/1592386/000159238626000009/virt-20251231.htm |
| 4 | Optiver NTI 4,556 mlr €, net kâr 1,769 mlr € (K) | DOGRU | 2024: 3,494 / 1,369 | https://www.optiver.com/about-us/financial-results/ |
| 5 | Pod getirileri, 2025 ve Ekim 2026 (K) | DOGRU (BAS) | 2025: Point72 %17,5, Balyasny %16,7, Millennium %10,5, Wellington %10,2. Ekim 2026: Millennium −%2,3, Wellington +%1,7 (YTD +%15,3), Quantedge YTD +%60. **Ek bağlam:** aynı kaynakta S&P 2025'te +%16,4; pod'ların çoğu endeksin altında. "Yüksek getiri değil yüksek Sharpe" tezi güçleniyor | https://finance.yahoo.com/news/2025-returns-hedge-funds-rolling-234728986.html ; https://hedgeweek.com/news/major-hedge-funds-suffer-october-losses-as-market-volatility-hits-multiple-strategies |
| 6 | Medallion 2020 +%76, RIEF −%19 (K) | KISMEN | Atıf yapılan II makalesi: RIEF **−%22,62**, RIDA −%33,58 (25 Aralık'a kadar). Yıl sonu −%19 teyit edilemedi | https://www.institutionalinvestor.com/article/b1q3fndg77d0tg/Renaissance-s-Medallion-Fund-Surged-76-in-2020-But-Funds-Open-to-Outsiders-Tanked |
| 7 | CTA/trend: SG Trend 2022 +%27,3, SG CTA +%20,2; 12 ay (Nisan 2025) −%18,7, "25 yılın en kötüsü" (K) | KISMEN | SG CTA **+%20,1**. TTU Nisan 2025: "12 aylık kayıp −%18'i aşıyor". "En kötü" ifadesi doğrulanamadı. **Önemli ek:** SG Trend 2000'den beri CAGR **%5,23**, tüm tarih MaxDD %20,61 (Ekim 2025). Trend tek başına high-reward değil | https://alpha-week.com/2022-cta-index-performance-review ; https://www.toptradersunplugged.com/trend-following-performance-report-april-2025/ ; https://www.toptradersunplugged.com/trend-following-performance-report-october-2025/ |
| 8 | Tayvan day trader'ları, 1992–2006 (K) | DOGRU (PR) | Yılda 360 bin trader; ~%13'ü net kârlı. ~1.000 kişi (<%1) öngörülebilir şekilde kazanıyor. En iyi 500: 49,5 bps brüt / 28,1 bps net. Toplam portföy alfası 2,0 bps/gün. Aktifler +13,1 bps brüt / −6,8 bps net | https://faculty.haas.berkeley.edu/odean/papers/day%20traders/Day%20Trading%20Skill%20110523.pdf |
| 9 | Brezilya: 300+ seans devam edenlerin %97'si zararda; %1,1'i asgari ücretin, %0,5'i gişe memuru maaşının üstünde (K) | KISMEN | %97 doğru. Güncel özette: "yalnız **%0,4**'ü gişe memurundan ($54/gün) fazla kazandı". Asgari ücret rakamı bu sürümde yok | https://econpapers.repec.org/RePEc:spa:wpaper:2019wpecon47 |
| 10 | Retail opsiyon: hacmin >%60'ı, spread %12,6, ortalamada kayıp (K) | DOGRU (PR, JF 2023) | "1,14 + 4,13 mlr $" basın rakamı doğrulanamadı | https://lbsresearch.london.edu/id/eprint/2827 |
| 11 | 0DTE retail günde −358 bin $ (K, S) | DOGRU, bağlamı eksik | Günlük vadeler başladıktan (Mayıs 2022) sonra 358 bin $, öncesi 184 bin $. Ocak 2021–Şubat 2023 toplamı ~70 mn $; piyasa ölçeğinde küçük | https://cxoadvisory.com/individual-investing/retail-0dte-option-trader-performance |
| 12 | Robinhood herding. K: ~1 ay −%5 / −%9. S: 20 gün −%4,7, aşırıda −%19,6 | KISMEN, raporlar çelişiyor | Kasım 2020 taslağı: 5 günlük BHAR −%3,5, aşırıda −%6,4. 20 günlük −%4,7 yayımlanmış özetle (bellek) tutarlı ama SSRN 403. **−%19,6 DOGRULANAMADI, muhtemelen hatalı** | https://www.smallake.kr/wp-content/uploads/2020/12/SSRN-id3715077.pdf |
| 13 | USIC: Luk 2024 +%283,1 / 2025 +%969,8 / 2026'nın 9 ayı +%785,8; 712 katılımcının 85'i kârda (K) | DOGRU (YAR) | Organizatör bülteni. Aracı kurum ekstresiyle kontrol ediliyor; denetimli composite değil, time-weighted | https://finance.yahoo.com/markets/stocks/articles/united-states-investing-championship-nine-121500218.html |
| 14 | USIC paydası ve geri vermeler (K) | DOGRU (organizatör verisi, CTE derlemesi) | 2022'nin 10 ayı: 26/316. 2026 ilk yarısı: 115/688. Luk zirve +%1.358,2 → +%969,8; Mikulka +%960,4 → +%409,6. Sean Ryan 7/7 yıl, +%6.232. Minervini 2021 +%334,8; J Law +%353,9 / +%252,3; Kell 2020 +%941,1 | https://completetradersedge.com/wp-content/uploads/2026/09/CTE-Research-Sheet-US-Investing-Championship-2.pdf ; https://www.bowdoin.edu/news/2021/03/oliver-kell-10-wins-national-investment-contest-posting-nearly-tenfold-returns.html |
| 15 | Luk'un işlem istatistikleri: 104 kazanç / 319 kayıp, ~%0,5 risk, ortalama +%15 / −%3 (K §5.2 EV hesabının girdisi) | **DOGRULANAMADI** | Atıf yapılan sayfada bu sayılar yok. Sayfada yalnız "stoplar çoğunlukla %1–4" ve örnek işlemler var. §5.2'deki +0,48R ve "+%283 ile tutarlı" aritmetiği doğrulanmamış girdiye dayanıyor | https://www.financialwisdomtv.com/post/martin-luk-s-pullback-trading-strategy-how-the-2025-u-s-investing-champion-finds-low-risk-high-re |
| 16 | Kullamägi (K) | DOGRU (beyan düzeyinde, C) | İddialar: 105 mn $ (Kasım 2021) → ~45 mn $ (2022 ortası), risk ≤%0,5 (tavan %1), isabet %25–30. Ekstreleri Coyle incelemiş; CTE görmemiş; denetim yok. "Filtreye uysaydım kaybın %90'ından kaçardım" kendi karşı-olgusal iddiası | https://completetradersedge.com/kristjan-kullamagi-qullamaggie/ |
| 17 | FFTY: 2022 −%51,0; kuruluştan Mart 2025'e yıllık %1,24; 1 yıl −%18,8 (K) | KISMEN | 2022 ve 1 yıl doğru. 5 yıl −%7,3/yıl, 10 yıl +%4,6/yıl. "%1,24" sayfada yok → DOGRULANAMADI | https://www.aaii.com/etf/ticker/FFTY |
| 18 | Tekil hissede trend takibi, Zarattini-Pagani-Wilcox (K) | DOGRU (WP, uygulayıcı yazarlar) | Survivorship-free veri, 66 bin+ işlem; işlemlerin <%7'si kârın çoğunu üretiyor. CAGR %15,19 **brüt** (1991–2024), alfa %6,18, OOS 2005–2024. Maliyet varsayımı açıklanmamış; <1 mn $'da uygulaması zor | https://concretumgroup.com/does-trend-following-still-work-on-stocks/ |
| 19 | McLean-Pontiff: OOS −%26, yayın sonrası −%58, 97 sinyal (S, T) | DOGRU (JF 2016, bellek), kaynak hatalı | Atıf yapılan ivey PDF'i Mayıs 2013 taslağı: 82 sinyal, OOS ~%10, yayın sonrası ~%35. URL yayımlanmış sürümle değiştirilmeli | https://ivey.uwo.ca/media/3775549/pontiff.pdf |
| 20 | Hou-Xue-Zhang: 452 anomalinin %65'i elenir, t ≥ 2,78'de %82 (S) | DOGRU | | https://ideas.repec.org/a/oup/rfinst/v33y2020i5p2019-2133..html |
| 21 | Chen-Velikov: ortalama anomali net 4 bp/ay (S) | KISMEN | JFQA özetinde 4 bp; FEDS WP sürümünde 8 bp. Özet "en güçlüler 10–20 bp" diyor; S'nin "en iyi ≈ 10, kombinasyon ≈ 20" ayrımı özette yok | https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/zeroing-in-on-the-expected-returns-of-anomalies/945133D5A3ECEEAF466AEE91551FD225 ; https://www.federalreserve.gov/econres/feds/zeroing-in-on-the-expected-returns-of-anomalies.htm |
| 22 | Chen-Zimmermann 165 clear sinyal: aylık 0,745 → 0,318 → 0,295 → likit 0,201; anlamlı pay %16 (S) | DOGRU (yeniden hesapladım) | 0,745 / 0,319 / 0,295 / 0,201; t > 1,96 payı %16,4 | https://huggingface.co/datasets/OpenSourceAP/CrossSection |
| 23 | Martineau: PEAD büyük hissede 2006'dan, mikrocap'te 2016'dan beri yok (S, K) | DOGRU (PR) | Analist sürprizi, 60 günlük ufuk | https://cfr.ivo-welch.org/published/papers/martineau2021rest.pdf |
| 24 | Greenwood-Sammon: S&P 500'e ekleme etkisi 1990'larda %7,4, son on yılda <%1; çıkarma −%16,1 → −%0,6 (S) | KISMEN | NBER özeti: 1980'ler %3,4, **1990'lar %7,6**, son on yıl **%0,8**. Çıkarma 2010–2020'de −%0,6. −%16,1 doğrulanamadı | https://www.nber.org/papers/w30748 |
| 25 | Pre-FOMC drift: 1994–2011'de +49 bp; 2015 sonrası yok (S) | DOGRU | Kurov ve ark. örneklemi Aralık 2019'a kadar | https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf ; https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html |
| 26 | Opportunistic insider alımları: VW 82 bp/ay, 1986–2007 (K, S) | DOGRU (PR) | Yayın sonrası bağımsız test yok | https://www.nber.org/papers/w16454 ; https://www.nber.org/digest/apr11/decoding-inside-information |
| 27 | Daniel-Moskowitz: 2009'da kaybeden decile +%163, kazanan +%8; 1932'de +%232 / +%32 (S) | DOGRU | Makale metni. French VW desilleriyle kontrol: +%158,5 / +%7,2 ve +%239 / +%31 | https://www.nber.org/papers/w20439 |
| 28 | Temalı/uzmanlaşmış ETF'ler ilk 5 yılda riske göre ≈ −%30 (S) | DOGRU | | https://www.nber.org/papers/w28369 |
| 29 | Bessembinder: hisselerin %4'ü tüm net servet yaratımını açıklıyor (K, S) | DOGRU | | https://wpcarey.asu.edu/sites/default/files/2021-10/do-stocks-outperform-treasury-bills.pdf |
| 30 | Fed 16.09.2026'da +25 bp, bant %3,75–4,00, 12–0 (K, T) | DOGRU (REG) | DFF %3,88, DTB3 %4,03 (4.11.2026) | https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm |
| 31 | 5.11.2026 kapanışları (K, S, T) | DOGRU | Nasdaq Composite −%5,52 → 24.315; S&P −%4,36 → 7.353,73; 10 yıllık %4,90. NDX −%6,36 → 26.629,8; FRED'de 2020'den beri 4. en kötü gün; 200-DMA'nın −%4,8 altında, zirvenin −%14,7 altında | https://www.fool.com/coverage/stock-market-today/2026/11/05/stock-market-today-nov-5-nasdaq-suffers-worst-day-in-18-months-as-ai-trade-comes-under-fire/ ; https://fred.stlouisfed.org/series/NASDAQ100 |
| 32 | T §9.6: "S&P 500 200-DMA'nın %5,0 üstünde, zirveden −%1,7, YTD +%12,3" | **YANLIS (eskimiş)** | 4.11 verisi kullanılmış. 5.11 kapanışıyla S&P 200-DMA'nın yalnız **~%0,4 üstünde**, zirveden −%5,9, YTD ~+%7,4 | FRED SP500 + 7.353,73 |
| 33 | TCMB politika faizi %36 (K: "Ekim kararı bulunamadı") | DOGRU | 23.10.2026'da %37 → %36. 2025–26 patikası: %45 → … → %38 → %37 (23.01.2026) → %36 | https://www.tcmb.gov.tr/wps/wcm/connect/EN/TCMB+EN/Main+Menu/Core+Functions/Monetary+Policy/Central+Bank+Interest+Rates/1+Week+Repo |
| 34 | TL carry'nin USD engeli: K %15,7 brüt / %10,4 net; T son 12 ay +%22,5 brüt, net ~%16–18; S %8–13 | KISMEN | USD/TRY 12 aylık değişim %17,7 (FRED aylık ortalama, Eylül/Eylül), K'nın %17,5'i doğru. **Ama** K basit faiz kullanmış, bileşiği atlamış; T ise geriye dönük. İleriye dönük tahmin: %36 bileşik (~%42–43 brüt), %17,5 stopaj, %17,5–20 kur kaybı → **net ~%13–15,5 USD**. Anketteki faiz indirimi (12 ayda ~%29) gerçekleşir ya da kur hızlanırsa %6–12. 2010–2026 USD carry'si −%7,2/yıl, MaxDD −%85 (FRED ile yeniden üretilebilir) | https://fred.stlouisfed.org/series/CCUSMA02TRM618N ; https://fred.stlouisfed.org/series/IRSTCI01TRM156N |
| 35 | Sentetik 3x NDX 2022 −%79 ≈ TQQQ (T) | DOGRU (model) | Bağımsız hesabım −%78,9. Analitik karşılığı 3·ln(0,67) − 3σ² ≈ −%79. TQQQ'nun gerçek takvim yılı getirisi harici kaynaktan teyit edilemedi; ProShares sayfası yıllık getiri vermiyor. TQQQ gider oranı brüt %0,94 / net %0,78 | https://www.proshares.com/our-etfs/leveraged-and-inverse/tqqq |
| 36 | ABD gayrimukim veraset vergisi: 60 bin $ üstü (S, T) | DOGRU | ABD hisseleri US-situs varlık sayılıyor | https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-us-assets-must-file-estate-tax-returns |
| 37 | Kayıp serisi ve Monte Carlo (K §5.3, S §11) | DOGRU | %25 isabet, 200 işlem: P(≥10 / 12 / 15 / 17 ardışık kayıp) = %96,1 / 81,6 / 48,6 / 30,4 (analitik DP). SR 0,8, vol %35: medyan CAGR %24,9, medyan MDD −%50,9, P(MDD < −%50) %53 (benim simülasyonum) | yerel hesap |
| 38 | Aktivizm: ~%7 [−20, +20], "getirinin çoğu dosyalamadan önce" (K) | KISMEN | ~%7 doğru (bellek, JF 2008). "Çoğu önce" aşırı iddia: makale fiyat ve hacmin 10 gün önce yükseldiğini, dosyalama gününde de sıçrama olduğunu raporluyor | https://law.duke.edu/sites/default/files/centers/gfmc/session_3/2_brav_et_al-hedge_fund_activism-2008.pdf (okunmadı) |
| 39 | AQR TSMOM Sharpe: 1985–2009'da 1,41 → 2010–2026'da 0,40 (S) | DOGRULANAMADI | Ham AQR dosyası diskte yok, yeniden hesaplanmadı | https://www.aqr.com/Insights/Datasets/Time-Series-Momentum-Factors-Monthly |
| 40 | TÜFE Ekim %29,77; stopaj %17,5 (K, T) | DOGRULANAMADI (bağımsız) | Başka bir ajan (`tr_makro_engel.md`) resmî kaynakla raporlamış; ben arama yapamadığım için teyit edemedim | — |

## 2. Backtest denetimi

### 2.1 `abd_test` (ortak.py, test1–7)

**Look-ahead: yok.**
- Kaldıraçlı trend: sinyal t kapanışında oluşuyor, t+1 getirisine uygulanıyor (`sig.shift(1+lag)`). lag0, MOC emriyle uygulanabilir ama iyimser; lag1 ayrıca raporlanmış.
- 10 aylık SMA: ay sonu kararı doğru kaydırılmış.
- Vol-yönetimli UMD: ağırlık, t−1 ay sonundaki 126 günlük vol ile hesaplanıyor (doğru).
- Endüstri momentumu: seçim t ay sonunda, tutma t+1'de. Tek küçük sızıntı: `valid.loc[dn]` filtresi yalnız bir sonraki ayda verisi olan endüstrileri seçiyor (etkisi önemsiz).

**Survivorship.** Hisse düzeyinde yok; endeks ve portföy verisi kullanılmış. Ama **hindsight seçimi** var:
- NDX, sonradan en iyi çıkan endeks.
- 200-DMA kuralı literatürden önceden biliniyor.
- 2010–2026, tarihin en güçlü teknoloji boğası.

**Fiyat ve toplam getiri.**
- MKT (CRSP) toplam getiri; doğru.
- NDX fiyat endeksi + sabit %0,7 temettü; makul yaklaşım.
- S'nin `lev.py`'si NDX'e temettü eklememiş; CAGR ~L×%0,7 düşük, yani muhafazakâr.
- MKT'nin MA sinyali toplam getiri endeksinden hesaplanmış; çok küçük yanlılık.

**Finansman ve gider.** Formül L·r − (L−1)(rf+%1) − %0,9. Makul ve hafif muhafazakâr (TQQQ net gideri %0,78). Micro vadeli işlemde örtük finansman daha düşük olabilir.

**YENİ HATA: yıllıklaştırma.**
- `ortak.stats` yıl sayısını "gözlem / 252" ile hesaplıyor. French günlük verisi 1953 öncesinde Cumartesi seanslarını içeriyor: 1927–1952'de yılda 281–302 gözlem var.
- Sonuç olarak 1926/27 başlangıçlı **tüm günlük tam-dönem CAGR'lar düşük çıkıyor**:

  | Seri | Rapordaki | Takvim yılıyla |
  |---|---|---|
  | Piyasa 1x BH | %9,7 | %10,2 (aylık veriyle T'nin kendi tablosu %10,3) |
  | 3x 200DMA, lag0 | %20,8 | %21,7 |
  | 3x 200DMA, lag1 | %17,9 | %18,7 |

- Aynı hata 1953 öncesinde spread ve ER'yi ~%19 fazla tahsil ediyor; "200 gün" de o yıllarda ~0,67 takvim yılına karşılık geliyor.
- Yön muhafazakâr; sonuçları değiştirmiyor. 1950+ ve 2010+ tabloları etkilenmiyor.

**Bağımsız yeniden üretim.** Kendi kodumla (`v_abd/spot.py`) şunları aldım:

| Seri | Sonuç |
|---|---|
| NDX 3x 200DMA, lag0, tam dönem | CAGR %17,8 / MDD −%97,1 |
| NDX 3x 200DMA, lag0, 2010+ | %25,7 / −%55,2 |
| NDX 3x 200DMA, lag1, tam dönem | %18,8 / −%87,8 |
| NDX 3x 200DMA, 2000–02 penceresi, lag0 | −%89,3 |
| MKT 3x BH, 2010+ | %27,8 |
| MKT 3x 200DMA, 2010+ | %18,5 |
| NDX 2x 200DMA, lag1, 2010+ | %19,0 / −%41 |

Rapordaki sayılarla birebir aynı.

**Kırılganlık, raporda eksik.** 2000–02 penceresi lag1 ile **−%75,3** (lag0'da −%89). Tek günlük gecikme hem pencereyi hem tam dönem MaxDD'yi (−97 → −88) oynatıyor. Backtest MaxDD'leri nokta tahmin değil, tek bir yolun örneği.

**Kayan pencereler (test7).** Aylık adımla örtüşen 5 yıllık pencereler kullanılmış. 1990+ döneminde yaklaşık 7 bağımsız 5 yıllık gözlem var; P10 ve ">%15 olasılığı" sahte bir kesinlik veriyor.

**TL carry (test6a).** Üç zayıflık var:
- Aylık **ortalama** kur kullanılmış, ay sonu değil; bu vol ve MaxDD'yi hafif küçültür.
- Gecelik interbank faizi bireyin PPF ya da mevduat getirisiyle aynı değil.
- Vergi yok.

**Modellenmeyenler.** Vergi; kur çevrim maliyeti; yılda 5–7 sinyal geçişinin vergi olayı yaratması; seans arası gap'te LETF kapanış dışı yürütme.

### 2.2 `abd_swing` scriptleri (ff.py, lev.py)

**`ff.py` (sektör momentumu).**
- Formasyon t−12…t−2, tutma t. Look-ahead yok.
- **Maliyet sıfır.** Ayrıca 49 FF endüstrisinin bir kısmı yatırılabilir değil.
- Yeniden çalıştırdım: 2010–2026'da top-5 long %16,68, SR 0,86, MDD −%28,6. Aynı dönemde piyasa %14,15, **SR 0,97**. Yani **risk-ayarlı olarak piyasanın altında.**
- Parametreye duyarlı: 6 aylık sıralamayla %15,2. T'nin 24 kombinasyonlu ızgarası (10 bp maliyetle) medyan %14,2, piyasa %14,1.

**`lev.py`.** lag0, ER %0,85, spread %0,5, NDX temettüsüz. Sonuçlar T ile tutarlı.

**CZ hesapları.** 165 clear sinyal yeniden üretildi (tablo #22).

## 3. Raporlar arası çelişkiler

1. **Sektör/tema momentumu.**
   - S bunu 1 numaralı yaklaşım yapıyor: net %13–20, 1,3–1,5x kaldıraçla %17–25.
   - T'nin ızgarası 2010–26'da piyasaya göre +0,1 puan buluyor; benim hesabımda Sharpe piyasanın altında.
   - Kanıt "risk-ayarlı alfa ≈ 0, kötü sektörden uzak durma disiplini" düzeyinde. S'nin aralığı tek bir parametre seçimine ve sıfır maliyete dayanıyor.
2. **Engel oranı.** Üç rapor üç rakam veriyor: K %10,4, S %8–13, T %16–18 net USD. Düzeltilmiş ileriye dönük tahmin ~%13–15,5 net (#34). Kuyruk senaryosunda değer çok daha düşük.
3. **Robinhood rakamları** çelişiyor (#12).
4. **K'nın arketip B'si** ("pod-lite", kaldıraçsız +%15–40, Sharpe ~1) kanıtsız bir tahmin. T §6.4'e göre earnings sinyallerinin long-only üst portföyü 2010–25'te VW piyasayı geçmiyor (AnnouncementReturn −%1,4/yıl).
5. **Rejim okuması.** T S&P'yi "trend içinde" okuyor (eski veri). 5.11 sonrası S&P 200-DMA'ya %0,4 mesafede; NDX ise dışarıda.

## 4. Önemli eksikler

1. **Vergi asimetrisi.**
   - TL PPF ve mevduatta %17,5 **nihai** stopaj var.
   - ABD kazancı ise yıllık beyanla **%15–40 artan oranla** vergileniyor. Kazanç TL bazında hesaplanıyor, yani kur artışı da vergiye giriyor; Yİ-ÜFE endekslemesi koşullu.
   - Hiçbir rapor vergi sonrası karşılaştırma yapmadı. Vergi sonrası eşitlik için ABD tarafında gereken brüt USD getirisi muhtemelen %20–25+ (doğrulanmadı, mali müşavir şart).
2. **Kullanıcının tarzına en yakın test hiç yapılmadı.** Hisse düzeyinde EP, earnings-gap, breakout ve pullback setup'ları (Luk/Kullamägi ailesi) test edilmedi. Survivorship-free günlük hisse verisi gerekiyor; T'nin Test 4'ü veri engeliyle düştü.
3. **Korelasyon.** Önerilen bileşenler aynı riski taşıyor: sektör momentumu, 2x/3x NDX trend ve lider/earnings swing aynı teknoloji/büyüme betası. 2022'de üçü birlikte kaybeder. S'nin kombinasyon beklentisi (%15–25, MDD −35/−50) bir backtest'e değil tahmine dayanıyor.
4. **İleriye dönük hisse primi.** Kaldıraçlı-beta getirisi doğrudan hisse primine bağlı. 2010–2026 olağanüstü bir dönemdi; değerleme ve faiz (%4,9'luk 10 yıllık) altında beklenen prim tartışılmadı.
5. **USIC getiri dağılımı yok.** Yalnız "kâr eden oranı" var; medyan getiri ve sonraki yıl kalıcılığı sistematik değil. Luk'un işlem istatistikleri doğrulanmamış (#15).
6. **Opsiyonla konveksite** (call spread, LEAPS ile tema bahsi) maliyet sonrası test edilmedi.
7. **TR mukimi için uygulama** doğrulanmadı:
   - ABD-domisilli ETF erişimi (PRIIPs yalnız AB/AEA mukimine uygulanır; bellek).
   - CME micro vadeli işlem izinleri.
   - Temettü stopajı (ABD–TR anlaşması %20/%15; bellek).
8. **Şu anki tema riski.** S'nin "Hardware / Gold balon eşiği" bulgusu ile K'nın "lider kırılması" gözlemi birleştirilmedi. Mevcut rejimde (NDX 200-DMA altında, momentum unwind) üç yaklaşımın da kuralı düşük maruziyet söylüyor.

## 5. Karar için net çıkarım

Ana sonuçlar doğrulama sonrası ayakta:
- Kamuya açık ABD anomalileri kaldıraçsız, maliyet sonrası %15–20 USD vermiyor. CZ, McLean-Pontiff, HXZ, Chen-Velikov ve Martineau tutarlı.
- Yüksek getiri iki yerden geliyor:
  - Kaldıraçlı beta + trend filtresi: −%40 ile −%97 arası drawdown ve rejim şansı pahasına.
  - Doğrulanmış ama küçük bir sağ kuyruk: konsantre momentum swing trader'ları. Payda kötü: %8–17 kârlı.
- Düzeltilmesi gerekenler:
  - Engel oranı (net ~%13–15,5 USD, vergi asimetrisi hariç).
  - S&P rejim okuması (eskimiş).
  - S'deki sektör momentumu sıralaması (abartılı).
  - K'daki Luk EV aritmetiğinin girdileri (doğrulanmamış).
  - Küçük rakam hataları: RIEF −%22,6; Greenwood-Sammon %7,6 / %0,8; SG CTA %20,1; McLean-Pontiff kaynak URL'si.
