# Literatür taraması: ABD ETF'lerinde 1-3 işlem günlük getiri etkileri

Hazırlanma tarihi: 7 Kasım 2026 · Faz 1 (literatür ve pratik) · Hedef kullanıcı: Midas üzerinden akşamdan akşama (TR saatiyle ABD kapanışı civarında) kontrol eden bireysel yatırımcı.

Bu not; akademik makaleleri (SSRN, dergiler), uygulayıcı araştırmalarını (Quantpedia, Alpha Architect, CXO, Cboe, CME, ihraççı dokümanları) ve güvenilir blogları özetler. Her etki için tanım, kural, varlık, raporlanan büyüklük ve dönem, yayın sonrası kanıt ve kaynak verilmiştir. Bulunamayan bilgi "bulunamadı" diye yazılmıştır. Bir kaynağın yalnızca özeti ya da ikincil anlatımı okunduysa bu ayrıca belirtilmiştir.

- Test edilebilir hipotezler: `notlar/hipotezler.csv` (aile başına en az 4).
- İndirilen ham sayfalar ve PDF metinleri: `ham_sayfalar/literatur/` (dizin: `index.tsv`, HTTP durum kodlarıyla). 403, 404 ve 503 dönen sayfalar indirilmedi. Bot koruması aşılmaya çalışılmadı.
- İndirme betiği: `kod/faz1/lit_indir.py`, URL listesi: `kod/faz1/lit_urls.txt` (`python3 -I` ile çalıştırıldı).

---

## 0. Ön koşullar ve genel uyarılar

### 0.1 Yayın sonrası zayıflama (genel taban oranı)
- McLean & Pontiff (2016, *Journal of Finance*) 97 kesitsel getiri öngörücüsünü inceliyor. Portföy getirisi örneklem dışında %26, yayından sonra ise %58 düşüyor. Aradaki farkın (%58 − %26 = %32) "yayından öğrenen işlemlerden" kaynaklandığı tahmin ediliyor. Kaynak (PDF): https://counterpointfunds.com/wp-content/uploads/2017/07/PredictabilityMcleanPontiff.pdf
- Pratik sonuç: aşağıdaki etkilerin raporlanan büyüklükleri **üst sınır** sayılmalı. Varsayılan beklenti, yayın sonrası büyüklüğün yarıya inmesidir. Takvim ve olay etkileri bu çalışmanın örneğinde yok (çalışma kesitsel hisse öngörücülerini kapsıyor). Yine de aşağıda görüleceği gibi pre-FOMC, pre-holiday ve PEAD gibi etkilerde benzer ya da daha sert erimeler belgelenmiştir.

### 0.2 Saat eşlemesi (ABD Doğu saati → TR, UTC+3)
TR saati kışın (EST) ET + 8 saat, yazın (EDT) ET + 7 saattir.

| Olay | ET | TR (kış / yaz) | Not |
|---|---|---|---|
| ABD kapanış (ETF) | 16:00 | 00:00 / 23:00 | "t kapanışı" |
| ABD açılış | 09:30 | 17:30 / 16:30 | |
| CPI, NFP (BLS) | 08:30 | 16:30 / 15:30 | açılıştan önce |
| EIA petrol stokları (WPSR), Çarşamba | 10:30 | 18:30 / 17:30 | tatil haftasında kayar. https://ir.eia.gov/ |
| EIA doğalgaz depolama, Perşembe | 10:30 | 18:30 / 17:30 | tatil haftasında kayar |
| FOMC bildirisi | 14:00 | 22:00 / 21:00 | basın toplantısı 14:30 ET |
| Hazine ihale sonuçları (2/3/5/7/10/20/30 yıl) | 13:00 | 21:00 / 20:00 | takvim önceden ilan edilir |
| WM/Reuters Londra 16:00 fix | 11:00 (Londra 16:00) | 19:00 / 18:00 | Londra ve ABD yaz saatine farklı tarihlerde geçer |
| Cboe VIX kapanışı | 16:15 | 00:15 / 23:15 | ETF kapanışından 15 dk sonra |

"t kapanışında bilinen veri" ilkesi: VIX, VIX3M ve OVX'in resmi kapanışı ETF kapanışından 15 dakika sonra (16:15 ET) gelir. Bu yüzden canlı kullanımda 15:55-16:00 ET (TR 23:55 kış) anlık değeri alınmalı, backtestte bu küçük ileri bakış not edilmelidir. Ülke ETF'lerinin resmi NAV'ı ve spot BTC ETF akım verileri kapanıştan sonra yayımlanır. Bu yüzden kurallar t−1 değerlerini ya da gün içi gösterge değeri (iNAV) kullanır.

### 0.3 Gerçekleştirme (Midas'a özgü pratik)
- Akademik "kapanışta gir" kurallarının çoğu MOC (kapanış emri) varsayar. Kullanıcı TR 23:30-00:00 (kış) aralığında kapanışa yakın limit veya piyasa emri vermelidir. Pandey & Joshi (2023), IBS stratejisinde kapanışta girmenin önemini vurgular: kapanıştan kapanışa kurulan sürüm belirgin biçimde daha kötü çıkmıştır (bkz. §a).
- Quantpedia'nın GDX çalışması, resmi açılış fiyatının (ilk işlem) yanıltıcı olabileceğini gösteriyor. 09:31 fiyatıyla gerçekçi yürütmede "gece getirisi" yaklaşık %30'dan yaklaşık %8,6'ya (yıllık) iniyor (bkz. §c). Açılışta işlem yapan kuralların backtesti için 1 dakikalık veri gerekir.

---

## (a) IBS, RSI(2) / Connors tipi ortalamaya dönüş, ardışık düşüş günleri

| Etki | Tanım ve kural | Varlık | Büyüklük ve dönem | Yayın sonrası | Kaynak |
|---|---|---|---|---|---|
| **IBS etkisi** | IBS = (Kapanış − Düşük)/(Yüksek − Düşük). IBS < 0,20 → ertesi gün yükseliş, IBS > 0,80 → düşüş. 1 günlük tutuş | Hisse endeksi ETF'leri (SPY, QQQ, ülke ETF'leri) | Pagonidis (2013): ETF'lerin kuruluşundan 12.5.2013'e kadar. İkincil aktarım: IBS < 0,2 sonrası ortalama +%0,35, IBS > 0,8 sonrası −%0,13. Etki yüksek aralıklı ve yüksek hacimli günlerde, en çok Pazartesi → Salı arasında güçlü (Kinlay özeti) | Pandey & Joshi (2023) 2009-2019 ülke ETF'lerinde etkiyi doğruluyor. Tek ETF eşik stratejisinde Sharpe: PIN 2,17, EWJ 1,59, EWI 1,48, FXI 1,05, EWZ 0,48, **IVV 0,20**, EWC −0,45. Yükseliş olasılığı: EWJ IBS < 0,2'de %60,6, IVV %56,6. Kesitsel "min-max" (en düşük IBS'li ülkeyi al, en yükseği aç sat) Sharpe 2,91. **İşlem maliyeti yok**. 2 günlük tutuşta ve 2 günlük IBS hesabında performans düşüyor | Pagonidis'in birincil metni **bulunamadı**. Pandey & Joshi: https://arxiv.org/abs/2306.12434 (PDF indirildi). Kinlay özeti: https://jonathankinlay.com/?p=2199. +%0,35 / −%0,13 rakamları ikincil özetlerden: https://therighttrader.com/learn/trading-strategies/internal-bar-strength · https://www.quantconnect.com/forum/discussion/5675/mean-reversion-effect-in-etf-price-series/ |
| **RSI(2) (Connors)** | Yaygın aktarılan kural: Kapanış > SMA200 ve RSI(2) < 10 (sıkı sürümü < 5) → kapanışta al. Kapanış > SMA5 → sat. Birincil kitap (Connors & Alvarez 2008, *Short Term Trading Strategies That Work*) okunmadı, kural ikincil kaynaktan | SPY, QQQ, endeks ETF'leri | Bağımsız ve hakemli bir büyüklük ölçümü **bulunamadı**. Oxford Strat bağımsız testi (5 endeks vadelisi, 1980-2016): RSI(2) avantajı var, RSI(14)'te yok | Connors'un kendi raporu (çıkar çatışması): "RSI 25" kuralı (C > SMA200, RSI(4) < 25 al, RSI(4) < 20 ekle, RSI(4) > 55 sat) SPY'da 1993-2008 %88,2 isabet, **yayın sonrası 2009-2017 %96,8 isabet** (62 işlem). Quantified Strategies: 2009 sonrası "biraz daha az etkili". Hakemli bir yayın sonrası test **bulunamadı** | Connors Research Traders Journal: https://tradingmarkets.com/?p=1593757 (indirildi). Oxford Strat: https://oxfordstrat.com/?p=16240 |
| **Ardışık düşüş günleri** | N gün art arda düşen kapanış (çoğunlukla N=3), trend filtresiyle (C > SMA200) → al, 1-5 gün tut | SPY, QQQ, sektör ETF'leri | Akademik ve kesin parametreli birincil kaynak **bulunamadı**. Connors: ortalamaya dönüşün "tatlı noktası" 3-7 gün | Dolaylı kanıt: endeks günlük otokorelasyonu 1998 civarında pozitiften negatife döndü (blog, 250 günlük pencere) | Connors (yukarıda). Otokorelasyon: https://advisoranalyst.com/?p=40530. Lewellen'in otokorelasyon çalışmasına (Dartmouth) erişilemedi (404) |
| **Turnaround Tuesday** | Pazartesi SPX ≤ −%1,5 → Salı al-tut | SPY | Schaeffer's (2010 sonrası): Salı ortalama +%0,9, yaklaşık %70'i pozitif. Bespoke (2009 sonrası): Pazartesi ≤ −%2 sonrası 15 vakanın 12'sinde ertesi gün yükseliş, ortalama yaklaşık +%1 | Küçük örneklem. Yayın sonrası test **bulunamadı** | https://www.schaeffersresearch.com/content/analysis/2021/09/22/is-turnaround-thursday-a-real-thing · https://weissratings.com/en/pivotal-point/sharp-rebound-to-monday-smackdown-was-ingeniously-forecast |

Yorum: IBS ve RSI(2) tipi etkiler ABD büyük endeks ETF'sinde (IVV, SPY) daha zayıf (Sharpe 0,2). Ülke ve sektör ETF'lerinde daha güçlü görünüyor. Kanıtların büyük kısmı ya maliyetsiz ya da strateji satıcısı kaynaklı. Kendi örneklem dışı testimiz şart.

---

## (b) Takvim ve olay etkileri

| Etki | Kural | Büyüklük ve dönem | Yayın sonrası | Kaynak |
|---|---|---|---|---|
| **Ay dönümü (TOM)** | Ayın son işlem günü ile yeni ayın ilk 3 işlem günü (4 günlük pencere) | McConnell & Xu (2008, FAJ), CRSP 1926-2005: pencere içinde günlük ortalama değer ağırlıklı (VW) %0,15, eşit ağırlıklı (EW) %0,22. 35 ülkenin 31'inde var. Hacim ve fon akımı açıklamıyor | Quantpedia SPY sürümü: ay sonundan 1 gün önce al, yeni ayın 3. işlem günü kapanışında sat. 2024 sponsorlu blog (1980-2024 S&P): hâlâ işliyor, yazın zayıf. SPY ile 2010 sonrasını kapsayan bağımsız ve hakemli test **bulunamadı** | https://econpapers.repec.org/RePEc:taf:ufajxx:v:64:y:2008:i:2:p:49-64 · https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes · https://www.etftrends.com/etf-strategist-channel/turn-month-effect/ |
| **Tatil öncesi** | NYSE tatilinden önceki son işlem günü | Ariel (1990): tatil öncesi getiri normal günün 9-14 katı (1963-1982) | **Zayıfladı.** Ko & Yang (2021, *Critical Finance Review*), 1983-2019: etki artık yalnızca küçük şirketlerde. Büyük şirketlerde 1990 sonrası anlamsız | https://cfr.ivo-welch.info/published/papers/ko2021pre.pdf (indirildi) |
| **Haftanın günü** | French (1980): Pazartesi negatif | Klasik | ABD hisselerinde büyük ölçüde kayboldu (Caporale & Plastun özetindeki literatür). Kriptoda ters yönde (Pazartesi pozitif), bkz. §k | https://cesifo.org/DocDL/cesifo1_wp6716.pdf |
| **Pre-FOMC drift** | Planlı FOMC bildirisinden önceki 24 saat (14:00 → 14:00 ET) | Lucca & Moench (2015, JF), 1994-2011: S&P 500 ortalama **+49 bp**. Diğer uluslararası endekslerde benzer, Hazine kâğıtlarında yok. Eğri düzken ve VIX yüksekken daha büyük | **Büyük ölçüde kayboldu.** Kurov, Wolfe & Gilbert (2021, FRL): 2011'den sonra yalnızca basın toplantılı toplantılarda kalıyor, **2015'ten sonra fiilen yok**. Ben Dor & Rosa: 2011/04-2017/12 arasında drift yok. Durum bağımlı yorum: drift yüksek belirsizlik dönemlerinde yoğunlaşıyor (Quantpedia özeti) | NY Fed SR 512 (indirildi): https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf · Kurov ve diğ.: https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html · VoxEU: https://cepr.org/voxeu/columns/predictable-movements-asset-prices-around-fomc-meetings |
| **FOMC döngüsü "çift haftalar"** | FOMC'den sonraki 0., 2., 4. ve 6. haftalar (0. hafta: gün −1 ile +3 arası) | Cieslak, Morse & Vissing-Jorgensen (2019, JF), 1994 sonrası yaklaşık 160 toplantı. 5 günlük ortalama aşırı getiri: hafta 0 %0,57, hafta 2 %0,30, hafta 4 %0,42, hafta 6 %0,61. Tek haftalar yaklaşık 0. Yüksek getirinin yaklaşık yarısı büyük düşüşlerden sonraki dönüşten geliyor | Yayın sonrası test **bulunamadı** | https://stern.nyu.edu/sites/default/files/assets/documents/cycle_paper_cieslak_morse_vissingjorgensen.pdf (indirildi) |
| **FOMC basın toplantısı** | Basın toplantılı toplantı günleri | Boguth, Grégoire & Martineau (2019, JFQA): piyasa risk primi basın toplantılı günlerde daha büyük. 2019'dan beri her toplantıda basın toplantısı var (bu ayrım artık yok) | — | https://ideas.repec.org/a/cup/jfinqa/v54y2019i6p2327-2353_2.html |
| **Makro duyuru günleri (CPI, PPI, istihdam, FOMC)** | Planlı duyuru günü (kapanıştan kapanışa) | Savor & Wilson (2013, JFQA), 1958-2009: duyuru günü ortalama aşırı getiri **11,4 bp**, diğer günler 1,1 bp. Yıllık primin %60'ından fazlası günlerin %13'ünde. Hazine kâğıtlarında da (1961-2009) geçerli | Bespoke: 2000 sonrası CPI günü medyan mutlak hareket %0,55 ile tüm günlerle aynı. Kasım 2021 sonrası CPI günü %0,95, tüm günler %0,88. 2022-2023'te dağılım genişledi, yön kanıtı yok (FS Investments) | Wharton taslağı (indirildi): https://faculty.wharton.upenn.edu/wp-content/uploads/2012/04/Draft20111128p_edited.pdf · https://www.bespokepremium.com/?p=172399 · https://fsinvestments.com/?p=23115 |
| **Opsiyon vade haftası (OE)** | Ayın 3. Cuma'sını içeren hafta boyunca opsiyonu aktif büyük hisseleri tut | Stivers & Sun (2013, JBF), S&P 100: OE haftası getirisi yüksek, 4. Cuma haftası hafif düşük. Quantpedia: OE haftası ortalama haftalık getiri %0,528, Sharpe 0,61. Mekanizma: piyasa yapıcıların delta hedge çözülmesi. Opsiyon/hisse hacim oranı en yüksek %7,5'lik haftalarda %0,83 (CXO, 1996-2008). Sonraki haftada kısmi dönüş | QuantConnect OEF ile 2007-2018 backtesti var, sonucu okunmadı. Bağımsız yayın sonrası test **bulunamadı** | https://quantpedia.com/strategies/option-expiration-week-effect (indirildi) · https://ideas.repec.org/a/eee/jbfina/v37y2013i11p4226-4240.html |

---

## (c) Gece (overnight) ve gün içi getiri ayrışması

| Etki | Bulgu | Dönem | Yayın sonrası | Kaynak |
|---|---|---|---|---|
| ABD hisse endeksleri gece > gün içi | Cliff, Cooper & Gulen (2008, SSRN 1004081) ve Kelly & Clark (2011, JAM): getirinin büyük kısmı kapanıştan açılışa kadar olan bölümde. Price Action Lab: SPY getirisinin %93'ünden fazlası gece (ikincil) | 1993-2000'ler | NightShares 500 ve 2000 ETF'leri (NSPY, NIWM) Haziran 2022'de açıldı, Temmuz 2023'te kapandı. NSPY kuruluştan bu yana −%6,9, S&P 500 +%22. Morningstar: maliyetler etkiyi yiyor | https://ideas.repec.org/a/pal/assmgt/v12y2011i2d10.1057_jam.2011.2.html · https://www.wealthmanagement.com/etfs/-night-effect-etfs-to-shut-down-with-overnight-stock-returns-elusive (indirildi) |
| Hisse düzeyinde "çekişme" | Lou, Polk & Skouras (2019, JFE): momentum kârları tamamen gece, ters dönüş (reversal) kârları ise gün içinde kazanılıyor. İki bileşen ters işaretli | 1993-2013 | Yayın sonrası test **bulunamadı** | https://personal.lse.ac.uk/polk/research/TugOfWar.pdf (indirildi) |
| E-mini S&P 24 saat | Bondarenko & Muravyev ("Market Return Around the Clock: A Puzzle", JFQA): Avrupa açılışı civarındaki 4 saat ortalama getirinin tamamını açıklıyor. Benzer bulgu: Boyarchenko, Larsen & Whelan, "The Overnight Drift" (2023): ABD hisse getirisi Avrupa piyasalarının açılış saatlerinde belirgin pozitif | — | — | https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/abs/market-return-around-the-clock-a-puzzle/089E33AC0B4D3B9A02CBA31EDF6505B3 |
| **Altın** | Blose, Gondhalekar & Kort (2018, *J. Econ. Finance*): COMEX altın, Londra fix, madenci hisseleri ve altın ETF'lerinde gece getirisi anlamlı pozitif, gündüz getirisi anlamlı negatif. Aynı yazarlar (2014, COMEX 1985-2012): fark daraldı ama kaybolmadı. Quantpedia: GLD'nin gün içi performansı son 20 yılda "ihmal edilebilir". WGC (Caixin aktarımı) 2026 ilk yarı: Asya saatleri **+%12,97**, Avrupa −%1,32, ABD saatleri **−%15,08** | 1985-2026 | 2026'da da sürüyor (WGC) | https://ideas.repec.org/a/spr/jecfin/v42y2018i3d10.1007_s12197-017-9403-0.html · https://www.caixinglobal.com/2026-07-03/analysis-gold-caught-in-a-tug-of-war-between-asian-bulls-and-a-hawkish-fed-102460438.html (indirildi) · CBS tezi (2019, doğu saatlerinde yükseliş): https://research.cbs.dk/en/studentProjects/gold-price-dynamics-around-the-clock/ |
| **GDX** | Resmi OHLC ile gece +%30/yıl, gün içi −%25/yıl ("gerçek olamayacak kadar iyi"). 09:31 fiyatıyla gece stratejisi yıllık %8,58, MDD −%40,7 | yaklaşık 20 yıl | Ölçüm artefaktı uyarısı | https://quantpedia.com/dangers-of-relying-on-ohlc-prices-the-case-of-overnight-drift-in-gdx-etf/ (indirildi) |
| **Ham petrol (USO)** | Doğrudan gece/gün içi getiri ayrıştırması **bulunamadı**. Energy Economics (2023, USO 2008-2022): haber ve uç şoklar gece seanslarını daha çok etkiliyor | 2008-2022 | — | https://ideas.repec.org/p/hal/journl/halshs-04250313.html |
| **Bitcoin/IBIT** | Bloomberg/Bespoke: IBIT'in Ocak 2024'ten bu yana birikimli gece getirisi yaklaşık +%200, al-tut yaklaşık +%40 (aradaki fark gün içinin negatif olduğunu ima ediyor). Promotör beyanı: "IBIT kazançlarının tamamı gece" | 2024-2026 | Bu gözlem üzerine NGHT adlı "gece BTC, gündüz hazine bonosu" ETF'si önerildi | https://www.marketscreener.com/news/why-is-an-etf-seeking-to-capture-bitcoin-s-night-premium-ce7e50dedc8bf221 · https://www.thedailyupside.com/etf/thematics-sectors/morgan-stanleys-bitcoin-etf-launches-as-a-new-vampire-fund-rises-from-the-crypto |

1-3 günlük kapanıştan kapanışa tutuş için çıkarım: gece/gün içi ayrışması tutuşu bozmaz, aksine gece primini toplar. Altın ve IBIT'te "kapanışta al, açılışta sat" yaklaşımının kapanıştan kapanışa göre üstün olup olmadığı ayrıca test edilmeli. Açılış fiyatı ölçüm sorunu bu testte de geçerlidir.

---

## (d) Kaldıraçlı ETF'ler: gün sonu yeniden dengeleme ve oynaklık kaybı

**Mekanizma.** Günlük L kat hedefleyen fon, endeks gün içinde r kadar hareket ettiğinde kapanışta yaklaşık L(L−1)·r·NAV tutarında, aynı yönde işlem yapar. Kayıp formülü (standart türetim, Cheng & Madhavan 2009): log büyüme yaklaşık L·μ − L²σ²/2 iken endeksin L katı L·μ − Lσ²/2'dir. Gün başına ek kayıp ≈ **(L² − L)/2 · σ²_günlük**.
- 3x, σ_g = %1,5 (QQQ benzeri) → 6,75 bp/gün, 3 günde yaklaşık 20 bp.
- 2x tek hisse, σ_g = %4 (MSTR veya TSLA benzeri) → 16 bp/gün, 3 günde yaklaşık 48 bp.
- −1x ters ETF, σ_g = %1,5 → (1+1)/2 · σ² = 2,25 bp/gün.

| Kaynak | Bulgu | Dönem | Yayın sonrası / tartışma |
|---|---|---|---|
| Cheng & Madhavan (2009, JOIM) | Yeniden dengeleme talebi kapanışa doğru oynaklığı artırabilir. %1'lik piyasa hareketi MOC talebini %17, %5'lik hareket %50 artırır (FPA aktarımı) | 2009 | https://joim.com/dynamics-leveraged-inverse-exchange-traded-funds |
| Tuzun (2013, Fed FEDS 2013-48) | %1'lik endeks hareketi yaklaşık 1,04 milyar $ yeniden dengeleme akışı doğurur (Aralık 2011 itibarıyla 20,14 milyar $ AUM). Portföy sigortasına benziyor | 2006-2011 | https://www.federalreserve.gov/pubs/feds/2013/201348/ (indirildi) |
| Shum, Hejazi, Haryanto & Rodier (2016, RoF) | Gün sonu oynaklık, olası yeniden dengeleme/hacim oranıyla anlamlı ilişkili, en çok çok oynak günlerde. Çalışma taslağı (CXO): yeniden dengeleme son saat oynaklığının yaklaşık 1/3'ünü, ≥%3'lük günlerde %50'den fazlasını açıklıyor. Strateji: piyasa 14:45 ET'ye kadar ≥ %2 hareket ettiyse SSO/SDS'i 14:45'te al, kapanışta sat. İşlem başı brüt %0,60, birikimli %104 (2006/06-2011/07), ancak kârın çoğu 2008 sonundaki 2,5 ayda; 2006 ve 2011'de hiç işlem yok | 2006-2011 | https://ideas.repec.org/a/oup/revfin/v20y2016i6p2379-2409..html · https://www.cxoadvisory.com/volatility-effects/front-running-leveraged-etfs-at-the-end-of-the-day (indirildi) |
| Baltussen, Da, Lammers & Martens (2021, JFE) | 60'tan fazla vadeli işlemde (1974-2020) son 30 dakikanın getirisi günün geri kalanının getirisiyle pozitif öngörülüyor. Etki negatif net gamma günlerinde güçlü. **Sonraki günlerde geri dönüyor** (1-3 günlük tutuş için önemli: büyük ve trendli günlerin ertesinde kısmi dönüş) | 1974-2020 | https://www3.nd.edu/~zda/intramom.pdf (indirildi) |
| Barbon, Beckmeyer, Buraschi & Moerke (SSRN 3925725) | Kaldıraçlı ETF ve opsiyon delta hedge akışları gün sonunda momentum ve ardından ortalamaya dönüş yaratıyor. Tesla vakası. Kaldıraçlı ETF etkisi zamanla azalmış ve hızla geri dönüyor (arama özetinden, SSRN 403 döndü) | — | https://papers.ssrn.com/abstract=3925725 |
| Lenkey (2024, *QFE* derlemesi) | İstatistiksel ilişkiler tutarlı biçimde raporlanıyor, ancak çoğu makalede ciddi yöntem hatası olabilir ve **ekonomik etki anlamsız görünüyor**. Politika endişeleri genel kanıtla desteklenmiyor | 2024 | https://www.aimspress.com/article/doi/10.3934/QFE.2024031 (indirildi) |
| Bianchi & Goldberg (2026, arXiv 2604.27287) | 3.1.2022-29.12.2023: S&P 500 +%0,076, **SSO −%11,09, UPRO −%28,24**. Farkın yaklaşık 2/3'ü bileşik getiri ve oynaklık, kalanı kaldıraç sapmasının endeks getirisiyle negatif kovaryansı | 2022-2023 | https://arxiv.org/abs/2604.27287 (indirildi) |
| Zhao (2026, arXiv 2608.03703) | Kore 2026: kaldıraçlı ETF'lerin kapanış dengelemesine karşı konumlanan spekülatörler oynaklığı büyütüyor. Kaldıraçlı ETF'lerde tutulan hisseler, ABD kaynaklı açılış öncesi haberlere verdikleri ilk tepkinin **yaklaşık %75'ini ertesi kapanışa kadar geri veriyor** ve birkaç gün salınıyor. SK Hynix oynaklığı %100'den %136,7'ye çıktı. Bireysel yatırımcı maliyeti %17,6 | 2026 | https://arxiv.org/abs/2608.03703 (indirildi) |
| Tek hisse kaldıraçlı ETF'ler (MSTR) | JPMorgan (Benzinga aktarımı): Kasım 2024'te kaldıraçlı MSTR ETF'lerinin günlük yeniden dengeleme akışı zaman zaman 2 milyar $'ı aştı. Fiyata duyarsız akışlar gün sonu oynaklığını büyütüyor. Birincil JPM notu **bulunamadı** | 2024 | https://benzinga.com/24/12/42344345/how-microstrategy-etfs-are-powering-the-bitcoin-surge |
| Düzenleyici | SEC ve FINRA (2009) uyarısı: günlük sıfırlamalı ürünler bir günden uzun tutulduğunda hedeften sapar. FINRA RN 09-31: bir seanstan uzun tutacak bireysel yatırımcı için genellikle uygun değil | 2009 | https://www.investor.gov/news-alerts/investor-alerts/sec-finra-investor-alert-leveraged-inverse-etfs (indirildi) |

1-3 günlük çıkarım: (i) Kaldıraçlı araçla 1-3 gün tutuşun beklenen ek maliyeti yukarıdaki formülle hesaplanabilir. Yüksek oynaklıkta (σ_g ≥ %3) tek hisse 2x için 3 günlük kayıp 25-50 bp civarındadır. (ii) Büyük hareketli günlerin ertesinde kısmi dönüş beklentisi (Baltussen ve diğ., Zhao) dayanak kaynaklardaki en güçlü 1-3 günlük sinyaldir. Ancak ABD endekslerinde ekonomik büyüklüğü tartışmalı (Lenkey). (iii) Kaldıraçlı ETF'ler sinyal aracı değil, uygulama aracı olarak düşünülmeli.

---

## (e) VIX vade yapısı: VXX, UVXY, SVXY ve VIX sıçraması sonrası hisse getirisi

| Etki | Kural | Büyüklük ve dönem | Yayın sonrası | Kaynak |
|---|---|---|---|---|
| **VIX vadeli basis** (Simon & Campasano) | Günlük roll = (en yakın VIX vadelisi − VIX) / uzlaşmaya kalan iş günü. Kontango ve roll > 0,10 → VIX vadelisi aç sat. Backwardation ve roll < −0,10 → al. 5 gün tut. E-mini ile hedge | 2006/2007-2011: "yüksek kârlı", maliyet ve örneklem dışı hedge oranına dayanıklı | **Quantpedia: örneklem dışı backtest hafif negatif, alfa bozuluyor** | https://quantpedia.com/strategies/exploiting-term-structure-of-vix-futures (indirildi) |
| **VIX primi** (Cheng, "The Expected Return of Fear", SSRN 2495414; sonradan RFS 2019'da "The VIX Premium" adıyla yayımlandı) | Uzun VIX vadeli yatırımcısı ayda ortalama yaklaşık %4 kaybediyor. Vade eğrisi aşağı eğimliyken (backwardation) sonraki vadeli getiriler sıfıra yakın ya da pozitif. Kural: kısa VIX vadelisi taşı, eğri aşağı eğimliyse nakde geç → aylık 4 faktör alfası %3,4, Sharpe 0,36 | Dönem özette belirtilmemiş | Yayın sonrası test **bulunamadı** | Quantpedia sayfasında "Other papers" altında özet (indirildi) · http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2495414 |
| **VXX ve kısa vadeli vadeli işlem endeksi kaybı** | Al-tut | Whaley (2013): S&P VIX kısa vadeli toplam getiri endeksi Mart 2012'ye kadarki 6 yılda yaklaşık −%94, VXX tipi ürünlerin zamanla para kaybetmesi "neredeyse kesin". Orta vadeli ürünler aynı dönemde +%5,9 | Kontango kalıcı: Cboe'ya göre 2010'dan beri vakitlerin %80'inden fazlası kontango | https://www.cxoadvisory.com/volatility-effects/buying-and-holding-exchange-traded-products-based-on-vix-futures (indirildi) · Cboe: https://www.cboe.com/insights/posts/inside-volatility-trading-is-vix-backwardation-necessarily-a-sign-of-a-future-down-market |
| **Kısa vol kuyruk riski** | — | 5-6 Şubat 2018 "Volmageddon". ProShares 27.2.2018'de **SVXY'yi −1x'ten −0,5x'e, UVXY'yi 2x'ten 1,5x'e** indirdi | Yapısal değişiklik: 2018 öncesi SVXY verisi bugünkü ürünü temsil etmez | https://www.etfstrategy.com/proshares-reduces-vix-etfs-exposures-following-volatility-blow-up-65487/ · SEC 8-K (indirilemedi, 403): https://www.sec.gov/Archives/edgar/data/0001415311/000119312518059052/d503117dex991.htm |
| **VIX/VIX3M oranı** | VIX3M = 93 günlük S&P 500 örtük oynaklığı (Eylül 2017'ye kadar ticker VXV). VIX/VIX3M > 1 → backwardation (stres) | — | Uygulayıcılar oran eşiklerini kullanıyor (ör. kontangoda SVIX, backwardation'da VXX). Aynı uygulayıcı bunun "olduğu gibi uygulanırsa genelde geride kaldığını" belirtiyor. Hakemli SVXY ve VIX/VIX3M backtesti **bulunamadı** | https://tradingvolatility.substack.com/p/three-strategies-for-trading-volatility · Cboe: https://cboe.com/products/vix-index-volatility/volatility-on-stock-indexes/cboe-3-month-volatility-index-vxv · https://www.macroption.com/vix3m/ |
| **Backwardation sonrası hisse getirisi** | VIX vadeli eğrisi negatif eğimli → sonraki S&P 500 getirisi | Fassas & Hourvouliades (2019, JRFM): negatif eğim katsayısı anlamlı → **backwardation sonrası pozitif S&P getirisi**. Kontangoda sinyal yok | Fassas'ın 2012 çalışması (2004-2010) zayıf ve örneklem içi | https://mdpi.com/1911-8074/12/3/113 (403) · Macrosynergy özeti: https://macrosynergy.com/?p=41000 |
| **VIX sıçraması sonrası S&P** | VIX > SMA10 · 1,20 (Schaeffer's tetikleyicisi, yılda 3-4 kez). %30 eşiğinde 22,5 yılda 21 olay | Sonraki ileri getiri ortalama %7,85, rastgele alımda %2,06 (ufuk yazıda belirsiz, büyük olasılıkla birkaç ay). Man Group: en büyük 20 sıçramada getiri çoğunlukla ilk hafta. Bandelli & Wang (2018, CXO): yalnızca 2 yıllık VIX zirvesi istismar edilebilir; örtüşen pencereler anlamlılığı şişiriyor | New Frontier (2014-2024 güncellemesi): VIX sıçramasında piyasadan çıkmak net zarar ettiriyor | https://www.schaeffersresearch.com/content/analysis/2015/08/24/what-to-make-of-the-latest-overbought-vix-signal · https://www.man.com/insights/views-from-the-floor-2021-dec-14 · https://www.cxoadvisory.com/?p=31176 |

---

## (f) Doğalgaz (UNG, BOIL, KOLD)

| Etki | Kural | Büyüklük ve dönem | Yayın sonrası | Kaynak |
|---|---|---|---|---|
| **EIA depolama raporu günü** (Perşembe 10:30 ET) | Duyuru günü getirisi ile diğer günler | Prokopczuk, Wese Simen & Wichmann (2021, *Energy Journal*), NG vadelisi 03/2003-12/2018: yıllık ortalama getiri −%31,65. Duyuru günü ortalaması **−%0,37**, diğer günler −%0,09. Negatif yıllık getirinin %50'den fazlası duyuru günlerinde. Getiri duyuru öncesi (%49,4) ve sonrası (%50,6) arasında eşit bölünüyor. Duyuru öncesi parça yalnızca depolama beklentiyi aştığında görülüyor. Strateji: duyurudan 90 dk önce aç sat, 30 dk sonra kapat → maliyet ve fonlama sonrası yıllık %12, Sharpe 1,76 | **Alt dönem 2014-2018'de etki yok** (makale ek tablosu A.3). Yazarlar stratejinin arbitrajla zayıflamış olabileceğini belirtiyor | https://centaur.reading.ac.uk/90003/1/NG_paper_final_round.pdf (indirildi) · https://econpapers.repec.org/RePEc:sae:enejou:v:42:y:2021:i:2:p:91-112 |
| Rapor oynaklığı | Linn & Zhu (2004, JFM), 1999-2002: rapor anında oynaklık sıçraması, yaklaşık 30 dk sürüyor | 1999-2002 | AGA'dan EIA'ya geçişten sonra da sürüyor | https://ou.edu/content/dam/price/Management/Energy%20Institute/docs/Linn%20and%20Zhu%20JFM%202004.pdf (indirildi) |
| Ölçüm hatası | Halova, Kurov & Kucher (2014, JFM): EKK, stok sürprizinin fiyat etkisini olduğundan küçük tahmin ediyor. Gerçek etki daha büyük | — | — | https://ideas.repec.org/a/wly/jfutmk/v34y2014i10p911-933.html |
| **Kontango ve roll getirisi (UNG)** | UNG her ay ön ay pozisyonunu 4 iş gününde, vadeden yaklaşık 2 hafta önce bir sonraki aya taşıyor (ikincil kaynak). Kontangoda sistematik kayıp | UNG yaklaşık 10 yılda yaklaşık −%90 (yaklaşık 108 $ → 11 $, 247wallst 2026, görüş yazısı) | Kalıcı | https://247wallst.com/investing/2026/05/28/ung-holds-front-month-natural-gas-futures-and-contango-has-cost-holders-90-percent-over-a-decade-without-a-single-price-drop/ · güncel roll takvimi için USCF sitesi (bu çalışmada **indirilmedi / bulunamadı**) |
| **UNG roll'unun önden koşulması** | Roll günlerinde fiyat baskısı | UNG'ye özgü akademik çalışma **bulunamadı**. USO için Bessembinder ve diğ.: önden koşma yok, likidite artıyor (bkz. §g). 2009'da Citi, UNG'nin ön ayı "desteklediğini" söylemişti | — | https://www.naturalgasintel.com/?p=66634 |
| **Mevsimsellik** | Takvim ayına göre UNG ve NG getirisi | Akademik büyüklük ölçümü **bulunamadı**. Sentimentrader: mevsimsellik dönüş noktası sinyali verebilir ama kontango yüzünden UNG ile işlemi önermiyor | — | https://sentimentrader.com/blog/seasonality-a-potential-ray-of-hope-for-plummeting-natural-gas |
| **Hava durumu** | HDD/CDD tahmin revizyonları | Piyasa haberlerinde fiyatın tahmin revizyonuyla oynadığı sıkça yazılıyor (NGI). Tahmin revizyonu ile getiri öngörüsü üzerine hakemli çalışma **bulunamadı**. Sıcaklık şoku ve stok sürprizi etkisi üzerine bir makale var, detayı okunmadı | — | https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4122141/ |

---

## (g) Ham petrol (USO, UCO, SCO, BNO)

| Etki | Bulgu | Kaynak |
|---|---|---|
| **EIA WPSR** (Çarşamba 10:30 ET, API Salı akşamı) | Rousse & Sévi (2019, *Energy Journal*): stok rakamı beklentiyi aştığında açıklamadan önceki 2 saatte alıcı kaynaklı emirler anlamlı biçimde artıyor, fiyat açıklama öncesi ortalama yaklaşık −%0,25 hareket ediyor (bilgili işlem). Asimetrik tepki ve sonraki saatlerde kısmen düzelen **aşırı tepki**. Kapanıştan kapanışa duyuru günü getiri primine dair çalışma **bulunamadı** | https://hal.archives-ouvertes.fr/hal-02024317 · https://ideas.repec.org/p/ags/feemes/249788.html |
| EIA ölçüm hatası | Halova ve diğ. (2014): stok sürprizi etkisi EKK ile küçük tahmin ediliyor. Alturki & Kurov (2022, JFM): ardışık API ve EIA duyurularında ham petrol vadelisi ve hisse piyasasında verimsizlik kanıtı | https://econpapers.repec.org/RePEc:wly:jfutmk:v:42:y:2022:i:1:p:172-188 |
| **USO roll** | Bessembinder, Carrion, Tuttle & Venkataraman (2016, JFE): roll günlerinde spread daralıyor, derinlik artıyor, likidite sağlayan hesap sayısı artıyor. **Sistematik önden koşma yok** ("sunshine trading"). USO roll başına gidiş-dönüş yaklaşık 25 bp etkin maliyet ödüyor (CFTC taslağı 2014). Örneklem döneminde ham petrol ETF AUM'unun %95'i USO'daydı | https://www.cftc.gov/idc/groups/public/@economicanalysis/documents/file/oce_predatorysunshine0314.pdf (indirildi) · https://econpapers.repec.org/RePEc:eee:jfinec:v:121:y:2016:i:1:p:142-166 |
| USO 2020 yapı değişikliği | Nisan 2020'den itibaren pozisyon birden fazla vadeye dağıtıldı. Roll süresi 4 günden 10 güne uzadı. 2020 öncesi USO verisi bugünkü fonu temsil etmez | https://www.etf.com/sections/news/biggest-oil-etf-shakes-structure |
| **OVX** | Chen, Liu & Li (2018): OVX, WTI ve Brent spot oynaklığını örneklem içi ve dışında öngörüyor (5 ve 20 gün dahil). Yön öngörüsü kantile ve rejime bağlı (yüksek OVX kantilinde var). USO'ya özgü test **bulunamadı** | https://econpapers.repec.org/RePEc:eee:phsmap:v:492:y:2018:i:c:p:837-850 |
| Petrol → hisse | Bkz. §n (Driesprong ve diğ. 2008) | |

---

## (h) Altın ve gümüş (GLD, IAU, SLV, GDX, GDXJ)

| Etki | Bulgu | Kaynak |
|---|---|---|
| Gece/Asya seansı | §c: gece pozitif, ABD seansı negatif (1985-2026). 2026 ilk yarısında Asya +%13, ABD −%15 | §c kaynakları |
| **Madencilerin gecikmeli tepkisi** | Kısa vadede GLD → GDX gecikmesini test eden akademik çalışma **bulunamadı**. Uzun vadeli kanıt: Baur, Trench & Tay ("Gold Shares Underperform Gold Bullion"). Quantpedia: 2006-2025'te GDX yıllık %1,2, GLD %8,1 (birikimli 350 puan fark), fark ayı piyasalarında ve hisse krizlerinde büyük. Kısa vadeli gecikme iddiaları anekdot düzeyinde (Zeal LLC, Kasım 2023: altın 8 günde +%5,6 iken GDX yatay) | https://quantpedia.com/golds-rally-and-the-gold-mining-stocks-trap/ (indirildi) · https://www.zealllc.com/2023/gdstklag.htm |
| **Reel faiz** | Erb & Harvey (2013, NBER w18706 / FAJ): 10 yıllık TIPS reel getirisi ile reel altın fiyatı arasında korelasyon −0,82 (1997-2012, aylık düzeyler). Yazarlar nedenselliğe itiraz edilebileceğini vurguluyor. **2022'de ilişki koptu** (reel getiriler +250 bp yükselirken altın düşmedi, ikincil kaynaklar). Günlük ve 1-3 günlük öngörü testi **bulunamadı** | https://www.nber.org/papers/w18706.pdf (indirildi) · https://www.longtermtrends.net/gold-vs-real-yields/ |
| Dolar | Altın-dolar kısa vade öncü-ardıl ilişkisine dair hakemli çalışma **bulunamadı** (aynı anlı negatif ilişki yaygın biliniyor) | — |
| **FOMC ve altın** | Altında pre-FOMC drift'i test eden hakemli çalışma **bulunamadı**. Lucca & Moench slaytlarında altın portföyü var, sonucu görülmedi. Gayriresmî analiz (Yahoo/Sunshine Profits, 2017 sonrası 41 toplantı): altın toplantıdan önce genelde düştü, sonra yükseldi, 10 gün sonra ortalama +%0,67 | https://www.bostonfed.org/economic/conf/Macro-Finance-2012/presentations/lucca.pdf · https://ca.finance.yahoo.com/news/daily-gold-news-wednesday-jan-124820478.html |

---

## (i) Uzun vadeli tahvil (TLT, TMF, TBT)

| Etki | Kural | Büyüklük ve dönem | Yayın sonrası | Kaynak |
|---|---|---|---|---|
| **Ay sonu (endeks uzatma ve yeniden dengeleme)** | Ayın son 3-5 iş günü uzun Hazine | Hartley & Schwarz (2019): 1990-2018. 10 yıllık tahvilde son 3 gün ortalama aşırı getiri **%0,25/ay** (yıllık yaklaşık 3 puan), Sharpe yaklaşık 1. Vade uzadıkça büyüyor. Diğer günler sıfırdan farksız. Hayat sigortacıları endeks yeniden dengeleme günlerinde net alıcı. Etki geçici | 2015-2018 alt dönemi daha zayıf ama anlamlı (CXO). **CXO: TLT'de 2002 ortasından beri ay dönümü bulguları makaleyi desteklemiyor** (farklı pencere) | https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2019/12/17-19.Schwarz.pdf (indirildi) · https://www.cxoadvisory.com/bonds/term-premium-end-of-month-effect/ |
| **İhale döngüsü** | İhaleden önceki birkaç gün fiyat düşer, sonra toparlanır | Lou, Yan & Zhang (2013, RFS): ikincil piyasa fiyatları ihale öncesi günlerde anlamlı düşüyor ve kısa sürede toparlanıyor. Hazine'ye gizli maliyet ihale büyüklüğünün 9-18 bp'si. Robeco (2025): ihale öncesi vadeliler ortalama 6 bp düşüyor, sonraki saatlerde toparlanıyor | TradeMachine (satıcı): TLT ihale haftası, yılda yaklaşık 5 işlem, ortalama 3 gün tutuş (ücretli, doğrulanamadı) | https://eprints.lse.ac.uk/46329/ (indirildi) · https://www.robeco.com/en-sg/insights/2025/03/quant-chart-us-treasuries-up-for-auction (403) |
| **FOMC çevresi** | FOMC'nin −1, 0, +1 günleri | Hillenbrand (2025, RFS): 1980-2017 arasında uzun vadeli getirilerdeki seküler düşüşün **tamamı** FOMC etrafındaki 3 günlük pencerede (10 yıllık %10,1 → %2,4). Pan & Peng: uzun vadeli tahvillerde FOMC'den **bir gün önce** pozitif drift (AFA slaytı: 10 yıllık sıfır kuponlu getiri FOMC[−1]'de −0,79 bp). Brooks, Katz & Lustig (2018, NBER 25127): fed funds hedef değişikliklerinden sonra uzun vadeli getirilerde **FOMC sonrası drift** (tahvil fonu akımları kaynaklı) | 2022 sıkılaşmasında yönün tersine dönüp dönmediği **bulunamadı** | https://quantpedia.com/secular-decline-in-yields-around-fomc-meetings/ (indirildi) · https://en.saif.sjtu.edu.cn/junpan/slide_FOMC_AFA.pdf · https://www.nber.org/papers/w25127 |
| **CPI ve istihdam günleri** | Duyuru günü uzun tahvil getirisi | Savor & Wilson (2013): Hazine kâğıtlarında da duyuru günü aşırı getirisi yüksek (1961-2009) | Yayın sonrası test **bulunamadı** | §b |
| **Bakır/altın → 10 yıllık getiri** | Bakır/altın oranı yükselirse getiri yükselir | Gundlach'ın iddiası (CNBC 2017, Bloomberg 2019) | Bloomberg 2020: ilişki "kırık". CFA Enterprising Investor 2023: rejim değişince zayıflıyor. Örneklem dışı test **bulunamadı** | https://www.cnbc.com/2017/08/08/jeff-gundlach-obscure-chart-tells-him-yields-to-rise-stocks-to-fall.html · https://www.bloombergquint.com/markets/gundlach-s-favored-metals-ratio-breaks-from-yields-in-new-normal · https://rpc.cfainstitute.org/blogs/enterprising-investor/2023/is-the-copper-gold-ratio-a-leading-indicator-on-rates |

---

## (j) Döviz ETF'leri (UUP, UDN, FXE, FXY, FXA, FXF)

| Etki | Bulgu | Kaynak |
|---|---|---|
| **UUP ve FXY'ye özgü kısa vadeli momentum/dönüş** | 1-3 günlük ufukta döviz ETF'lerine özgü hakemli çalışma **bulunamadı**. Döviz momentumu literatürü (Menkhoff ve diğ. 2012) aylık ufukta | — |
| Günün saati | Ranaldo (2009, JBF): yerel para **yerel çalışma saatlerinde değer kaybediyor**, yabancı saatlerde değer kazanıyor (yıllar boyunca, takvim etkileri kontrol edildikten sonra da). Krohn, Mueller & Whelan (2024, JF): USD büyük fix'lerden (Tokyo 9:55, ECB 14:15 CET, Londra 16:00) önce değer kazanıyor, sonra kaybediyor ("W" deseni). 1999-2019, G9: "dolar portföyü" (USD'ye karşı eşit ağırlıklı yabancı paralar) NY kapanışından Tokyo fix'ine kadar yıllık −%5,0 (USD değer kazanıyor), sonrasında +%5,3. Avrupa açılışından ECB fix'ine kadar −%4,2, **Londra fix'inden (11:00 ET) NY gün sonuna kadar +%4,6** (yani ABD öğleden sonrasında USD değer kaybediyor). t-istatistikleri 4,5 ile 11,7 arasında | https://snb.ch/en/mmr/papers/id/working_paper_2007_03 · https://www.bankofcanada.ca/wp-content/uploads/2021/10/swp2021-48.pdf (indirildi) |
| **FOMC günleri** | Mueller, Tahbaz-Salehi & Vedolin (2017, JF): FOMC günlerinde USD karşısında yüksek faizli döviz portföyü **+16,83 bp**, diğer günler +1,66 bp. Düşük faizli portföy 5,71 bp, diğer günler −0,55 bp. Belirsizlik ve faiz indirimiyle artıyor. Örnek: AUD duyuru günü 21,76 bp | https://www.fmg.ac.uk/sites/default/files/publications/dp-54.pdf (indirildi) |
| **Ay sonu hedge dengelemesi** | Melvin & Prins (2015, JFM): ay içindeki hisse yükselişi, ay sonu fix'inden önce para biriminin değer kaybını öngörüyor (hedge işlemleri). Uygulayıcı yorumu: ABD hisseleri ay içinde güçlü yükseldiyse ay sonuna doğru USD satış baskısı (Barclays ay sonu modeli) | https://ideas.repec.org/a/eee/finmar/v22y2015icp50-72.html · https://www.newsquawk.com/headlines/barclays-month-end-moderate-usd-selling |
| **Güvenli liman** | Ranaldo & Söderlind (2010, RoF): ABD hisseleri düşüp tahviller yükseldiğinde ve döviz oynaklığı arttığında CHF ve JPY USD'ye karşı değer kazanıyor. Etki birkaç saatten birkaç güne kadar, krizlerde güçlü. Son çalışmalar yenin güvenli liman niteliğinin BoJ politikasıyla zayıfladığını söylüyor | https://www.snb.ch/en/mmr/papers/id/working_paper_2007_17 |

---

## (k) Kripto (IBIT, FBTC, BITO, ETHA, BITX)

| Etki | Bulgu | Yayın sonrası ve uyarı | Kaynak |
|---|---|---|---|
| Haftanın günü | Caporale & Plastun (2019, FRL), 2013-2017: dört kriptodan yalnızca BTC'de Pazartesi getirisi anlamlı yüksek. Dergi sürümünde işlem simülasyonu rastgeleden anlamlı farklı değil | Hafta sonu ve CME boşluğu etkisinin zayıfladığı yönünde yorumlar var (Weiss 2025, CoinMarketCap), hakemli değil | https://cesifo.org/DocDL/cesifo1_wp6716.pdf (indirildi) |
| Saat etkisi | Quantpedia (Gemini, 10/2015-02/2022): en güçlü saatler 22:00 ve 23:00 UTC. Kural: 21:00 UTC'de al, 23:00'te sat → yıllık %33, oynaklık %20,9, MDD −%22,5. NYSE açık günlerde getiriyi "gece" bileşeni (16:00 → 10:00 NY) belirliyor. NYSE kapalı günlerde "gün içi" bileşen | 2022-2023'te düşüş yaşandı (Quantpedia güncellemesi) | https://quantpedia.com/are-there-seasonal-intraday-or-overnight-anomalies-in-bitcoin/ (indirildi) |
| ABD seansı ve Asya | Amberdata (2018-2023): en yüksek ortalama getiri ABD saatlerinde, en çok negatif saat Asya'da. NYDIG (2020-2021): Kuzey Amerika saatleri en güçlü. 2017 zirvesine kadar Asya saatleri baskın. K33: ABD saatleri +%30, Asya +%21, Avrupa +%17 | Dönem bağımlı. IBIT "gece" bulgusuyla (§c) gerilim var, çünkü tanımlar farklı | https://blog.amberdata.io/trading-between-hours-volatility-dispersion-across-multiple-regions · https://nydig.com/research/a-look-at-geographic-drivers-of-returns |
| **Spot ETF akımları → fiyat** | FalconX (2024): Granger p = 0,004, VAR'da önceki gün akımı bugünün getirisini pozitif etkiliyor (katsayı 0,027), korelasyon 0,30, etki yaklaşık %1,2 tepe. DWF Labs (2026): akımlar geçmiş hareketi izliyor (önceki hafta korelasyonu 0,54), ertesi gün 0,09, 1 hafta 0,03 | Zayıf ve kararsız | https://falconx.io/newsroom/what-can-spot-etf-flows-tell-us-about-the-trajectory-of-bitcoin-prices-a-preliminary-statistical-investigation (indirildi) · https://forklog.com/en/news/dwf-labs-questions-whether-etf-flows-predict-bitcoins-future-price-moves |
| Zaman serisi momentumu | Liu & Tsyvinski (2021, RFS): günlük ve haftalık frekansta anlamlı zaman serisi momentumu. BTC'de geçen haftanın en üst %20'lik dilimi sonrası ortalama +%11,2, en alt dilim +%2,6 (2011-2018) | Örneklem içi, veri madenciliği uyarısı (CXO) | https://www.nber.org/system/files/working_papers/w24877/w24877.pdf · https://www.cxoadvisory.com/currency-trading/crypto-asset-risks-and-returns/ |
| BTC'nin gece hareketleri ve IBIT | §c: IBIT gece +%200, al-tut +%40 (Ocak 2024-2026) | Promotör kaynaklı | §c |

---

## (l) Ülke ETF'leri: eşzamansız fiyatlama, NAV primi ve ertesi gün düzeltmesi

| Etki | Bulgu | Kaynak |
|---|---|---|
| **ABD saatlerinde S&P'ye aşırı tepki** | Levy & Lieberman (2013, JBF): eşzamanlı saatlerde ETF fiyatını NAV getirisi, eşzamansız saatlerde S&P 500 belirliyor. S&P'nin ETF üzerindeki etkisi yabancı endeks üzerindeki etkisinden büyük → **ABD'ye aşırı tepki**. Gecikmeli prim ve iskontonun ABD açılışında güçlü **negatif** etkisi var (prim ve iskonto açılışta tersine düzeliyor) | https://econ.biu.ac.il/sites/econ/files/shared/riedp_1-13.pdf (indirildi) |
| Fiyat keşfi mi aşırı tepki mi | Asya-Pasifik ülke ETF'leri (2006-2020): yerel işlem saatleri öngörü gücünü belirliyor. Yazarlara göre aşırı tepkiden çok kısa vadeli beklenti (fiyat keşfi) | https://www.informahealthcare.com/doi/abs/10.1080/10293523.2023.2208904 |
| ETF → yerel endeks | Atilgan, Demirtas, Gunaydin & Oztekin (2022, *Applied Economics*): 18 ülkenin 14'ünde ABD'deki ETF getirisi yerel endeksin **ertesi gün** getirisini öngörüyor. Eşzamansızlık kontrol edildikten sonra da geçerli, yüksek oynaklıkta güçlü. Kore istisna (negatif). Not: bu, ETF'nin kendisinde değil yerel piyasada işlem fırsatı | https://ideas.repec.org/a/taf/applec/v54y2022i47p5476-5496.html |
| **Prim ve iskontonun ortalamaya dönüşü** | Petajisto (2017, FAJ), 2007-2014, 1.813 fon: fiyat ve NAV sapması yaklaşık ±200 bp bantta, uluslararası ve likit olmayan fonlarda büyük. Benzer ETF grubuyla düzeltilince bant yaklaşık 100 bp. Göreli prim stratejisi maliyet öncesi yaklaşık %7 anormal getiri (maliyet düşülmemiş). "Kısa vadeli ortalamaya dönüşün kanıtı" | https://rpc.cfainstitute.org/research/financial-analysts-journal/2017/inefficiencies-in-the-pricing-of-exchange-traded-funds · Alpha Architect özeti: https://alphaarchitect.com/academic-research-insight-digging-into-etf-trading-spreads/ |
| Ülke ETF'lerinde IBS | §a: Pandey & Joshi (2009-2019): EWJ, PIN, EWI, EIS, EZA ve FXI'de IBS eşiği Sharpe ≥ 1 (maliyetsiz). Kesitsel min-max Sharpe 2,9 | §a |

---

## (m) Sektör ETF'leri: kısa vadeli göreli dönüş ve endüstri momentumu

| Etki | Bulgu | Kaynak |
|---|---|---|
| **Endüstri momentumu** | Moskowitz & Grinblatt (1999, JF): endüstri momentumu en güçlü **1 aylık** ufukta. 1 aydan kısa ufukta endüstri ve hisse momentumunun işaretleri **tamamen zıt** (hisselerde kısa vadeli dönüş, endüstrilerde devam). Grundy & Martin (2001): alış-satış sıçraması ve 1 ay gecikmeye dayanıklı değil | https://econpapers.repec.org/RePEc:bla:jfinan:v:54:y:1999:i:4:p:1249-1290 |
| Haftalık endüstri | Du (2008): haftalık endüstri momentumu büyük ölçüde seri korelasyondan kaynaklanıyor, her zaman dönmüyor. CXO: 1 aylık oluşum ile tutuş arasında 1 hafta atlanınca hisselerde kısa vadeli dönüş kayboluyor, endüstri gruplarında kaybolmuyor. Birleşik "dönüş ve endüstri momentumu" brüt aylık %4,08 (1931-2010) | https://experts.nau.edu/en/publications/momentum-and-reversals-in-industry-portfolio-returns/ · https://www.cxoadvisory.com/momentum-investing/short-term-reversal-by-industry |
| Endeks vadelilerinde haftalık dönüş | Quantpedia: 7 Avrupa endeks vadelisi, son 5 güne göre zayıfları al, güçlüleri aç sat, haftalık → yıllık %29,6 (1993-2002) | https://theideafarm.com/alternative-investment/short-term-reversal-in-equity-index-futures/ |
| **SPDR sektör ETF'lerinde günlük göreli dönüş** | 1-3 günlük ufukta hakemli çalışma **bulunamadı**. Concretum (Temmuz 2026) 11 SPDR sektöründe ortalamaya dönüş modeli yayımladı (ücretli, içerik okunmadı) | https://concretumgroup.substack.com/p/a-mean-reversion-model-for-us-sectors |
| Niş ETF'lerde dönüş | Quantpedia: likiditesi düşük alternatif ETF'lerde kısa pencereli dönüş daha iyi çalışıyor | https://quantpedia.com/evaluating-reversal-potential-in-niche-alternative-etfs/ |

Çıkarım: sektör düzeyinde 1-3 günlük ufukta yön önceden belli değil. Hisse literatürü dönüş, endüstri literatürü devam öneriyor. İki yönlü test gerekir.

---

## (n) Öncü-ardıl (lead-lag) ilişkileri

| İlişki | Bulgu | Ufuk | Kaynak |
|---|---|---|---|
| Büyük → küçük şirketler | Lo & MacKinlay (1990, RFS): büyük hisse getirisi küçük hisseleri öncüler (haftalık), tersi zayıf. Hou (2007, RFS): etki ağırlıklı olarak **endüstri içi**, yavaş bilgi yayılımı, küçük ve az izlenen endüstrilerde güçlü | haftalık | https://web.mit.edu/~alo/www/Papers/lo-mackinlay-90b.html · https://ideas.repec.org/a/oup/rfinst/v20y2007i4p1113-1138.html |
| Endüstri → piyasa | Hong, Torous & Valkanov (2007, JFE): perakende, hizmetler, ticari gayrimenkul, **metal ve petrol** endüstri getirileri piyasayı 2 aya kadar öncülüyor. Piyasa ise az sayıda endüstriyi öncülüyor | aylık | https://cxoadvisory.com/economic-indicators/market-leading-industries |
| Petrol → hisse | Driesprong, Jacobsen & Maat (2008, JFE): petrol fiyatı artışı gelecekteki hisse getirisini **düşürüyor** (gelişmiş ve gelişmekte olan piyasalar). Birkaç işlem günü gecikme eklenince ilişki güçleniyor (yatırımcıların gecikmeli tepkisi) | günler-aylık | https://econpapers.repec.org/RePEc:eee:jfinec:v:89:y:2008:i:2:p:307-327 |
| Sanayi metalleri → hisse | Jacobsen, Marshall & Visaltanachoti (2019, *Management Science*): metal getirisi hisseyi öngörüyor, işaret konjonktüre bağlı. Genişlemede 1 SS metal artışı → aylık yaklaşık −%1,5, resesyonda +%0,5 | aylık | https://econpapers.repec.org/RePEc:inm:ormnsc:v:65:y:2019:i:7:p:3026-3042 |
| Bakır/altın → faiz | §i (zayıf ve kırılgan) | — | §i |
| Emtia → üretici hisseler (GLD → GDX, CL → XLE/XOP) | Günlük ufukta hakemli çalışma **bulunamadı** (madenciler için §h) | — | — |
| BTC → MSTR/COIN | Güçlü **eşanlı** birlikte hareket (arXiv 2505.14655: Strategy dahil 12 şirkette BTC betası > 1). Ertesi gün öncülüğü **bulunamadı** | günlük | https://arxiv.org/html/2505.14655 |
| ABD ETF → yabancı endeks | §l (Atilgan ve diğ. 2022) | ertesi gün | §l |
| Hazine ihalesi/FOMC → TLT | §i | gün | §i |

---

## Tek hisse ve tek hisse kaldıraçlı ETF'lere özgü ek bulgular (NVDL, TSLL, MSTU, CONL…)

| Etki | Bulgu | Kaynak |
|---|---|---|
| Kazanç duyurusu primi | Barber, De George, Lehavy & Trueman (2013, JFE), 46 ülke, 1990-2009: duyuru ayında getiri yüksek, en çok küçük hisselerde. Sürücü belirsizlik ve dikkat | https://econpapers.repec.org/RePEc:eee:jfinec:v:108:y:2013:i:1:p:118-138 |
| PEAD | Martineau (2022, CFR): modern piyasada fiyat sürprizi duyuru günü tamamen yansıtıyor. **Büyük hisselerde 2006'dan beri PEAD yok**, mikro hisselerde de son dönemde kayboldu. 2025'te karşıt iki makale var (UCLA Anderson özeti) | https://cfr.ivo-welch.info/published/papers/martineau2021rest.pdf (indirildi) · https://anderson-review.ucla.edu/is-post-earnings-announcement-drift-a-thing-again/ |
| Opsiyonu aktif büyük hisseler, OE haftası | §b Stivers & Sun (S&P 100). NVDA, TSLA ve AAPL gibi opsiyon hacmi çok yüksek hisseler bu tanıma uyar (çıkarım) | §b |
| Gece/gün içi | §c Lou, Polk & Skouras: hisse düzeyinde momentum gece, dönüş gün içinde | §c |
| Kaldıraçlı ETF dengelemesi ve kayıp | §d (Zhao 2026, MSTR 2024 akımları, formül) | §d |

---

## Bulunamayanlar (açıkça)
- Pagonidis (2013) IBS makalesinin birincil metni (yalnızca ikincil aktarım).
- Connors RSI(2) ve ardışık düşüş kurallarının bağımsız ve hakemli yayın sonrası testi.
- SPY ile 2010 sonrasını kapsayan bağımsız ay dönümü testi. TLT'de Hartley & Schwarz kuralının (son 3 gün) bağımsız ETF testi (CXO yalnızca ay dönümü penceresine bakmış).
- UNG roll önden koşmasına dair akademik veya düzenleyici çalışma. UNG'nin güncel (2026) roll takvimi (USCF sayfası indirilmedi).
- Doğalgazda hava tahmini revizyonu → getiri öngörüsü çalışması. Doğalgaz mevsimselliğinin akademik büyüklüğü.
- EIA WPSR günü kapanıştan kapanışa getiri primi (yalnızca gün içi ve bilgili işlem bulguları var).
- USO'nun gece/gün içi ayrıştırması. OVX → USO yön testi.
- GLD → GDX günlük gecikme testi. Altında pre-FOMC drift'i (hakemli). Altın ve dolar kısa vadeli öncü-ardıl ilişkisi.
- UUP ve FXY'de 1-3 günlük momentum veya dönüş çalışması.
- SPDR sektör ETF'lerinde günlük göreli dönüş üzerine hakemli çalışma.
- BTC → MSTR/COIN ertesi gün öncülüğü.
- SVXY ve VIX/VIX3M eşikli stratejinin hakemli backtesti (2018 sonrası ürün yapısıyla).
- Tek hisse kaldıraçlı ETF'lerin (NVDL, TSLL) gün sonu etkisine özgü hakemli çalışma.

## İndirilemeyen (erişim reddi veya hata) kaynaklar
SSRN abstract sayfaları (403), SEC EDGAR (403), MDPI (403), Robeco (403), escholarship (403), core.ac.uk (403), EFMA PDF'leri (503), Dartmouth (404), CFA blog eski URL'si (404), Skidmore KSSW (404). Ayrıntı: `ham_sayfalar/literatur/index.tsv`.
