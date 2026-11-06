# ABD'de profesyonel swing pratiği, opsiyon yapıları ve "stratejik küme" risk mühendisliği (6 Kasım 2026)

Görev anahtarı: `abd_profesyonel`. Soru: Doğrulanmış kazananlar ve profesyonel diskresyoner trader'lar işlemi gerçekte nasıl kuruyor? Opsiyonlar asimetrik swing getirisi için ne zaman işe yarıyor? Tematik kümelerde risk nasıl yönetiliyor?

**Kaynak etiketleri**
- [YAR] USIC, aracı kurum ekstresiyle doğrulanmış yarışma sonucu. Denetimli composite değil.
- [VRG] Vergi beyannamesi veya basının gördüğü kayıt.
- [KİT] Schwager ve benzeri kitaplar (yazar kaydı gördüğünü söylüyor; denetim raporu yayımlanmadı).
- [RÖP] Röportaj, podcast, blog (kişinin kendi beyanı).
- [İKİ] İkincil özet ya da blog (zayıf).
- [AK] Hakemli akademik çalışma.
- [RD] Resmî veya regülatör belgesi.
- [VERİ] Borsa veya veri sağlayıcı verisi.
- [H] Benim hesabım. Betikler oturum scratchpad'inde; repoya yazılmadı.

**Diğer dosyalarla örtüşme**
- Kişi kartları, USIC paydası ve survivorship: `abd_kim_kazaniyor.md`.
- Akademik kenarlar, IV crush ve vol hedefleme: `abd_swing_kenarlar.md`.
- Erişim, komisyon ve vergi: `abd_pratik.md`.

Bu dosya işlemin mekaniğine odaklanıyor: giriş, stop, boyut, piramit, çıkış, rejim, opsiyon yapısı ve ısı/küme limitleri.

---

## 0. Yönetici özeti

1. **Doğrulanmış kazananların ortak işletim sistemi:**
   - İşlem başına risk %0,25–1. Minervini'de %1,25–2,5'e kadar çıkıyor.
   - Stop yapısal ve dar: günün dibi ya da baz altı, en fazla ~1 ATR veya %7–10.
   - Kazanana ekleme var, maliyet düşürme yok.
   - Kâr güçlü yükselişte kısmen alınıyor: 3–5 günde 1/3–1/2. Kalan pozisyon 10/20 GHO ile trail ediliyor.
   - Endeks rejim anahtarı kullanılıyor ve kazanırken boyut büyüyor, kaybederken küçülüyor.
   - Edge seçim değil, payoff asimetrisi ve boyut disiplini.
2. **İki arketip var, ikisinin beklentisi benzer, +0,4–0,6R/işlem:**
   - (A) Minervini: isabet %44–63, ortalama kazanç = 2,15 × ortalama kayıp. Kaynak: 2021 için kendi beyanı.
   - (B) Kullamägi/Luk: isabet ~%25, kazanan ~5R ve üzeri.
   - Brandt (vadeli): 60–70 bps risk, işlem başı 20–30 bps hedef beklenti, yani ~+0,3–0,5R.
3. **Doğrulama zayıf, survivorship güçlü.** USIC sonuçları ekstreyle doğrulanıyor ama tek yıllık. Kullamägi'nin rakamları kitap düzeyinde (Coyle inceledi). Minervini'nin 1994–2000 serisi kitap düzeyinde.
   - Mekanik kopyalar mütevazı: Kullamägi tipi breakout backtest'i 2008–2025'te CAGR %19, MDD −%21 [İKİ].
   - FFTY 2022'de −%51 (`abd_kim_kazaniyor.md`).
4. **Şu an (5.11.2026 kapanışı) bu trader'ların kendi kuralları "yeni long yok" diyor.**
   - NDX 26.630; 10 GHO (28.672) < 20 GHO (29.286) < 50 GHO (29.686). 10<20 durumu 19.10'dan beri sürüyor. NDX 6.10 zirvesinden −%14,7.
   - VIX 28,2. Vade yapısı ters: VIX9D 32,7 > VIX3M 25,6.
   - SMH 52 hafta zirvesinden −%30, URA −%49,6, IBIT −%28,8.
   - Kullamägi'nin 10/20 filtresi, IBD'nin "correction" durumu ve Weinstein'ın Stage 3/4 okuması aynı şeyi söylüyor: 9.11.2026 tam boyutla başlama günü değil. İzleme listesi ve pilot (≤%0,25 risk) yalnızca follow-through veya 10>20 dönüşüyle açılır [H, VERİ].
5. **Opsiyon kanıtı koşulsuz olarak alıcının aleyhine.**
   - S&P zero-beta ATM straddle ≈ −%3/hafta (Coval-Shumway).
   - Yüksek çarpıklıklı 7 günlük tekil call'lar ≈ −%35/hafta, brüt, mid fiyatla (Boyer-Vorkink, çalışma kâğıdı).
   - Gömülü kaldıraç arttıkça riske göre getiri düşüyor (Frazzini-Pedersen).
   - Retail Kasım 2019–Haziran 2021'de ~2,1 milyar $ kaybetti; maliyetler bunun üstüne ~4,1 milyar $ (Bryzgalova et al.).
6. **Opsiyon ancak "bir edge'e kaldıraç" olarak ve IV ucuzken anlamlı.**
   - IV−RV sinyali (Goyal-Saretto) yarım-spread maliyeti düşüldükten sonra bile ~%5,3/ay long-short getiri veriyor.
   - Benim BS hesabım: ATM 45 günlük call, hisseyle aynı stop-R'de, +%20/15 günde 3,9R getiriyor (hisse 2,5R). Yatayda −0,34R. −%20 gap'te −1,56R (hisse −2,5R).
   - IV 15 puan düşerse avantaj kayboluyor.
   - Deep ITM LEAPS'in örtük yıllık maliyeti IV %45'te ~%7–9, IV %60'ta %11–14. Yüksek vol'lü tema hissesinde margin'den pahalı [H].
7. **TR mukimi için uygun alt küme:**
   - Çekirdek pozisyon hisse + yapısal stop.
   - Opsiyon yalnızca üç durumda: (i) düşük IV'li ve earnings içermeyen breakout'ta 45–90 günlük, 0,55–0,70 delta call; (ii) earnings veya yüksek IV'de debit spread; (iii) tema hedge'i için kısa vadeli put spread veya mikro vadeli short.
   - Kaçınılacaklar: <30 günlük OTM, çıplak short, IV >%45 isimde LEAPS.
   - 871(m) dividend-equivalent kuralı non-delta-one işlemlere 2028 sonuna kadar uygulanmıyor (Notice 2026-61).
8. **VİOP XU030 opsiyonu dar bir araç (5.11.2026 bülteni).**
   - 151 serinin yalnızca 36'sı işlem gördü. 665 işlem, prim 24,7 mn TL (~0,5 mn $). Nominal, BIST30 vadeli hacminin %2,3'ü.
   - Pay opsiyonlarında 2.257 seriden 289'u işlem gördü.
   - Kullanım alanı endeks olay hedge'i ve tanımlı riskli endeks görüşü. Tekil swing kaldıracı için değil.
9. **Küme riski gerçek ve ölçülebilir.**
   - 2024–Eylül 2026'da Chips/Hardware/Electrical Equipment endüstri portföylerinin ortalama korelasyonu 0,69. Beş pozisyon ≈ 1,33 bağımsız bahis.
   - 2026'da piyasadan arındırılmış korelasyon 0,37–0,50; 2015–19'da ~0.
   - Chips'in −%4'ten kötü olduğu 17 günde Hardware −%4,4, ElcEq −%4,0 [H, Ken French].
   - Aynı beklentiyle Monte Carlo: dörtlü tema kümelenmesi %1 riskte %5 olasılıklı kötü MDD'yi −%23,9'dan −%32,3'e çıkarıyor [H].
10. **Drawdown merdiveninin değeri sınırlı ama gerçek.**
    - Zirveden −%5'te ×0,5, −%10'da ×0,25 kuralı %5 olasılıklı kötü MDD'yi yarıya indiriyor (−%40,6 → −%18,9). Bedeli medyan getiriden ~17 puan.
    - Kaminski-Lo'nun teorisiyle uyumlu: değer yalnızca performans rejime bağlıysa doğar. Rejimsiz dünyada bu kural yalnızca "daha küçük oynamak"tır [H].
    - Önerilen tavanlar: küme ısısı ≤%1,5, toplam ısı ≤%3/%5/%6 (rejime göre), gap-ayarlı ısı, Elder'in aylık %6 devre kesicisi.

---

## 1. Profesyoneller işlemi nasıl kuruyor?

### 1.1 Trader matrisi (giriş, stop, risk, boyut, piramit, çıkış, rejim, istatistik)

| Trader / sistem | Doğrulama (tür) | Giriş tetiği | İlk stop | Risk/işlem, boyut | Piramit | Kâr alma / trail | Rejim anahtarı | Kazanç/kayıpta boyut | İsabet, payoff |
|---|---|---|---|---|---|---|---|---|---|
| **Mark Minervini** (SEPA/VCP) | USIC 1997 +%155 (250 bin $ öz para), 2021 $1M+ +%334,8 [YAR]. 1994–2000 ~%220/yıl, tek kayıplı çeyrek [KİT] | Trend Template (fiyat 150/200 GHO üstünde, 200 GHO yükselen, RS yüksek, zirveye yakın). VCP'de daralan düzeltmeler sonrası pivot kırılımı | Maksimum %10, ortalama kayıp hedefi %5–6 [İKİ] | %1,25–2,5 özsermaye [İKİ]. En iyi 4–5 isme %20–25, toplam ≤10–12 [İKİ] | Yalnızca kazanana. "Progressive exposure": %25 → %50 → %75 → %100 [İKİ] | Güce satış. Kâr riskin birkaç katına çıkınca kısmi satış ve stop başabaşa (kesin eşik doğrulanamadı) | Birincil gösterge kendi işlem sonuçları: "piyasa çalışırken büyük, çalışmazken küçük" | Pilotla başla, yastık oluşunca büyüt, kayıpta küçült | 2021: isabet **%44–63**, ort. kazanç **2,15×** ort. kayıp, 550+ hisse, "massive leverage but sparingly" [RÖP, X, 20.01.2022]. Genel: %45–50, iyi piyasada %60–65 [İKİ] |
| **O'Neil / IBD / David Ryan** (CANSLIM) | Ryan 1985 +%161, 1986 ~+%160, 1987 iki yıllık 43 bin $ → 295 bin $ [YAR/KİT, B–C] | Baz (cup-handle vb.) pivot kırılımı, ortalama üstü hacim. IBD "buy zone": pivot +%5 [İKİ] | **%7–8** (IBD kuralı) | Klasik: 4–6 lider (genel IBD öğüdü) | %50 başlangıç, +%2–2,5'te %30, bir +%2–2,5 daha yükselince %20 [İKİ, IBD yeniden basımı] | %20–25'te sat. İstisna: kırılımdan sonra 3 hafta içinde +%20 → en az 8 hafta tut | Follow-through day (rally denemesinin 4.+ günü, artan hacimle güçlü artış), distribution day sayımı (25 gün). FTD sonrası önerilen maruziyet %40–60; %80–100 yalnızca oturmuş trendde [İKİ] | Piyasa maruziyet kademesi ile | Mekanik versiyon (FFTY) 2022'de −%51 |
| **Kristjan Kullamägi** | Coyle ekstreleri inceledi (*Market Wizards: The Next Generation*, 2026) [KİT, "orta"]. FAQ: 2013–19 CAGR %268, en büyük DD %50 (2014) [RÖP] | (1) Breakout: önceki 1–3 ayda %30–100+ koşu, 2 hafta–2 ay daralan baz, 10/20 GHO üstünde; açılış aralığı tepesinden (1/5/60 dk) giriş. (2) EP: haber/earnings ile %10+ gap ve dev hacim. (3) Parabolic short | **Günün dibi; mesafe ≤1 ADR/ATR** | Çoğunlukla %0,25–1 (blog), %0,3–0,5 (FAQ), maksimum %1. Pozisyon %10–20 (FAQ: %5–25, çoğu %10–15). **Tek hissede gece >%30 yok** | Yok denecek kadar az. Edge giriş kalitesi ve trail'de | **3–5 günde 1/3–1/2 sat, stop başabaşa**, kalanı 10/20 GHO'da ilk kapanışla. İyi piyasada 10–20R+ | Nasdaq/SPY'de 10 GHO > 20 GHO ve ikisi yükseliyorsa long, 10<20'de temkin. Öz-tahmin: ~%80 isabetli | İyi giderken zamanın en az yarısında marjin. Zirvede ~150 mn $ long / 105 mn $ özsermaye ≈ 1,43x. Nakitten tam marjine geçiş haftalar–aylar sürüyor. Günlük kayıp limiti yok | İsabet **%25** (2019), %25–30. 2021 beklentisi ~1,16R (ikincil, çelişkili). 105 mn $ (Kasım 2021) → ~45 mn $ (2022 ortası). Kendi tahmini: filtreye uysaydı kayıpların ~%90'ı önlenirdi |
| **Martin Luk** | USIC 2024 +%283,1, 2025 +%969,8, 2026'nın 9 ayında +%785,8 [YAR] | Pullback-öncelikli: yükselen EMA'lara veya anchored VWAP'a ilk geri çekilme | <%2,5, çoğunlukla %1–1,5 | ~%0,5 | – | Trail | – | – | 2024: 104 kazanç / 319 kayıp (**%24,6**). Ort. kazanç ~%15, ort. kayıp ~%3 → ~5R [RÖP, ikincil] |
| **Oliver Kell** | USIC 2020 +%941,1 [YAR] | "Cycle of price action": reversal extension → wedge pop → EMA crossback → base n' break → exhaustion extension → wedge drop (10/20 EMA) | Kademeli: 10 ve 20 EMA altlarına | Earnings öncesi **"earnings size"**: boyut düşürülüyor [İKİ] | Crossback'lerde ekleme | Exhaustion extension'da güce satış, 20 EMA ihlalinde çıkış | Döngüdeki konum | Earnings'e küçük gir | – |
| **Stan Weinstein** (Stage analysis) | Denetimli kayıt yok (bülten) | Stage 2 kırılımı: direnç üstü kapanış, 30 haftalık GHO yukarı dönüyor, belirgin hacim (bir kaynak: önceki 3–4 haftanın 2×'i), Mansfield RS pozitif veya pozitife dönüyor | Baz altı. Sonra 30 haftalık GHO altında trail [İKİ] | – | – | Stage 3'te azalt, Stage 4'te çık | Endeks ve sektör "stage"i | – | – (ufuk: haftalar–aylar; stop geniş, boyut küçük) |
| **Linda Raschke** | CTA 1992, fon 2002–2015, BarclayHedge 5 yıllık sıralamada 4.500 içinde 17. (kendi sitesi) [RÖP]. Denetimli rakam yayımlanmamış | 2–5 günlük kısa vadeli teknik. Holy Grail: ADX(14) >30 ve yükselen, 20 GHO/ÜGHO'ya geri çekilme, sinyal barı tepesinin üstünden giriş. Turtle Soup: 20 günlük kırılım fake'ine karşı | Swing dibi [İKİ] | – | – | Önceki swing tepesi | Trend gücü (ADX) | – | – (trend içinde mean-reversion. Kullanıcının önceki 1–3 günlük bulgularına en yakın akraba) |
| **Peter Brandt** (vadeli, klasik formasyon) | *Unknown Market Wizards*: 27 yılda **%58/yıl**, Gain-to-Pain 2,81 [KİT]. Kendi ifadesi: yıllık vol ~%53 (agresif) | Formasyon kırılımı; teyit 30 günlük ATR'nin %50'si ötesinde stop emriyle | Formasyon karşı tarafı, koşullu stop | **60–70 bps**, her işlemde aynı dolar riski. Aynı anda 3–4 piyasa | **Piramit yapmaz** | 1–2 hafta içinde kısmi kâr. 8 günlük GHO üstünde kaldıkça taşır. **Cuma kuralı:** zarardaki işlem hafta sonuna taşınmaz | – | Boyut sabit (dolar risk) | Son 12 yılda isabet ~%54. Kitap döneminde %30–35 (235 işlemin 75'i kârlı). Hedef: 20–30 bps/işlem beklenti, 100 işlemde profit factor 3,0, DD <%15 [RÖP, 5.8.2026] |
| **Turtle kuralları** (sistematik referans) | Yayımlanmış kural seti (Faith, 2003) | 20/55 günlük kanal kırılımı | **2N** (N = ATR20) = %2 risk | 1 birim: 1N hareket = özsermayenin %1'i | Her ½N'de 1 birim, piyasa başına maksimum 4 | Kanal çıkışları | – | **Her −%10'da nominal hesap −%20**, yıl başı seviyesi geri gelene kadar | – (düşük isabet, büyük kazanç) |
| **Dan Zanger** | Fortune (Aralık 2000) 1999 vergi beyannamesini gördü: 14,23 mn $ sermaye kazancı. ~10.775 $ → ~18 mn $ (6/1998–12/1999) [VRG] | Chart pattern breakout'ları (cup-handle, flag) | Doğrulanamadı | Yüksek kaldıraç, balon rejimi | – | – | – | – | Tek dönem. Sonrasında denetimli kayıt yok: survivorship örneği |

Kaynaklar (tür, tarih):
- Minervini 2021 istatistiği: kendi X paylaşımı [RÖP]. Tweet kimliğinden çözülen tarih 20.01.2022; sayfa artık önbellekte "silinmiş" görünüyor. https://twitter.com/markminervini/status/1484178830889738240
- Minervini, 2021 USIC: https://www.businesswire.com/news/home/20220124005241/en/2021-United-States-Investing-Championship-Winners-%E2%80%94-Minervini-Smashes-Record
- Minervini, boyutlama özeti [İKİ]: https://juliachencoding.blogspot.com/2025/03/mark-minervinis-position-sizing.html ve https://www.tradingreviewers.com/think-and-trade-like-a-champion-review/
- Minervini, FinTwit 2022: https://benzinga.com/news/22/05/27210421/exclusive-know-when-to-be-a-pig-and-when-to-be-a-chicken-mark-minervini-at-2022-fintwit-conference
- Kullamägi: https://qullamaggie.com/my-3-timeless-setups-that-have-made-me-tens-of-millions/ ; https://qullamaggie.com/faq/ ; https://completetradersedge.com/kristjan-kullamagi-qullamaggie/
- USIC tabloları: https://completetradersedge.com/?p=234478
- Brandt: https://chatwithtraders.com/episode/329-peter-brandt (5.8.2026) ; https://www.panmacmillan.com/authors/jack-d-schwager/unknown-market-wizards/9780857198716 ; https://www.elitetrader.com/et/threads/market-wizard-peter-brandt-interview.374288 ; https://www.financialwisdomtv.com/post/diary-of-a-professional-trader-by-peter-brandt
- Turtle kuralları: https://turtletradersystem.blogspot.com/2009/01/original-turtle-trading-rules-chapter-3.html ; https://turtletradersystem.blogspot.com/2009/01/original-turtle-trading-rules-chapter-5.html
- IBD: https://inkl.com/news/how-to-invest-8-week-hold-rule-helps-latch-on-to-big-winners ; https://www.moomoo.com/my/learn/when-to-sell-stock-the-7-8-sell-rule ; https://inkl.com/news/when-to-buy-growth-stocks-how-pyramiding-up-can-be-as-easy-as-a-cup-of-coffee ; https://inkl.com/news/how-to-handle-changing-stock-market-trends
- Kell: https://traderlion.com/technical-analysis/chart-patterns/cycle-of-price-action-by-oliver-kell/ ; https://traderlion.com/profile/oliver-kell/mu-wedge-pop/
- Weinstein: https://picklespicksthestockmarket.blogspot.com/p/blog-page_28.html ; https://www.luxalgo.com/library/concept/weinstein-stage-analysis/
- Raschke: https://lindaraschke.net/bio-linda/ ; https://therighttrader.com/learn/trading-strategies/holy-grail-setup
- Luk: https://www.financialwisdomtv.com/post/martin-luk-s-pullback-trading-strategy-how-the-2025-u-s-investing-champion-finds-low-risk-high-re
- Zanger: https://money.cnn.com/magazines/fortune/fortune_archive/2000/12/18/293117/index.htm

### 1.2 Beklenti aritmetiği: farklı yollar, aynı sonuç

| Profil | İsabet p | Ort. kazanç / ort. kayıp b | Beklenti (R) = p·b − (1−p) | Başabaş b* = (1−p)/p | Tam Kelly f* = p − (1−p)/b | Gerçek risk/işlem |
|---|---|---|---|---|---|---|
| Minervini 2021 (alt uç) | 0,44 | 2,15 | **+0,39** | 1,27 | %18 | %1,25–2,5 → Kelly'nin ~1/7–1/15'i |
| Minervini 2021 (orta) | 0,50 | 2,15 | **+0,58** | 1,00 | %27 | aynı |
| Kullamägi / Luk | 0,25 | 5 | **+0,50** | 3,00 | %10 | %0,25–0,5 → ~1/20–1/40 |
| Brandt (hedef) | ~0,50 | – | **+0,3–0,45** (20–30 bps / 60–70 bps) | – | – | %0,6–0,7 |
| Benim varsayımım (MC, §3.3) | 0,27 | ~4 (sağa çarpık) | +0,45 | 2,7 | %9 | %0,25–1 test edildi |

**Neden herkes Kelly'nin çok altında?** Bunlar benim çıkarımlarım.
1. p ve b tahminleri gürültülü. 100 işlemde isabetin standart hatası ~±4,4 puan.
2. Aynı anda 4–8 pozisyon açık ve pozisyonlar ilişkili. Kelly payı tek bahis için hesaplanır; eşzamanlı ve ilişkili bahislerde bölünmesi gerekir.
3. Gap riski 1R'yi 2–3R yapabilir: Intel 30.10'da −%30, AMD 5.11'de −%17,3 (`abd_kim_kazaniyor.md`).
4. Yarım Kelly, büyüme hızının %75'ini varyansın 1/4'üyle verir (log-normal yaklaşımında g(f) = fμ − f²σ²/2). Kesirli Kelly'nin bedeli düşük, sağladığı koruma yüksek (MacLean-Thorp-Ziemba 2010). https://www.stat.berkeley.edu/~aldous/157/Papers/Good_Bad_Kelly.pdf

**Kapasite ve işlem sayısı çarpanı.**
- Luk 2024: 423 işlem × +0,48R × %0,5 ≈ %100 aritmetik. Progresif boyut ve bileşik getiriyle gerçekleşen +%283.
- Brandt: 125–150 işlem × ~0,35R × %0,65 ≈ %30 aritmetik. Gerçekleşen tarihî %58/yıl ancak çok daha yüksek kaldıraçla geldi (vol %53).
- Sonuç: **yüksek ödülün kaynağı yüksek işlem sayısı × pozitif R × rejimde progresif boyut.** Tek tek "büyük vuruşlar" değil.

### 1.3 Ortak işletim sistemi: sayısallaştırılmış 12 kural

1. **Evren:** RS liderleri. Son 1/3/6 ayın en iyi %1–2'si (Kullamägi) ya da Trend Template (Minervini). Tema liderliği şart: Moskowitz-Grinblatt industry momentum (`abd_kim_kazaniyor.md` §5).
2. **Giriş:** Sıkışmadan kırılım ya da trend içinde ilk geri çekilme. Tetik intraday (opening range high) veya kapanış. Kovalamaca sınırı: pivot +%5 (IBD) ya da stop mesafesi ≤1 ATR/ADR (Kullamägi).
3. **İlk stop yapısal:** günün dibi, baz altı ya da swing dibi. Tavan: ≤1 ATR (Kullamägi), ≤%7–8 (IBD), ≤%10 (Minervini). Ortalama kayıp tavanın yarısı civarında: Minervini %5–6, Luk %3.
4. **Boyut stoptan türetilir:** adet = (özsermaye × risk%) / (giriş − stop). Bu yüzden dar stop büyük pozisyon demektir ve tek pozisyon tavanı gerekir: Kullamägi gece %30, Minervini %20–25.
5. **Risk/işlem:** %0,25–0,5 normal, %1 tavan. Minervini %1,25–2,5 ama 4–6 pozisyon ve %5–6 ortalama kayıpla.
6. **Piramit:** Yalnızca kazanana ve küçülen dilimlerle (IBD %50/30/20, Turtle ½N'de bir). Brandt hiç yapmıyor; bu da meşru bir seçim.
7. **Kısmi kâr:** 3–5 günde 1/3–1/2 (Kullamägi), 1–2 haftada kısmi (Brandt), %20–25 (IBD). Ardından stop başabaşa. İşlem "bedava" hale gelir ve psikolojik sermaye korunur.
8. **Trail:** Hızlı hisselerde 10 GHO, olağan hızda 20 GHO, pozisyon hissesinde 50 GHO veya 30 haftalık GHO (Weinstein). Kapanış bazlı.
9. **Earnings:** Küçült ("earnings size", Kell) ya da yalnızca kâr yastığı varken taşı (Minervini). Yoksa çık.
10. **Rejim anahtarı:** Endeks 10>20 GHO (Kullamägi), FTD ve distribution sayımı (IBD), Stage (Weinstein). Kötü rejimde maruziyet ~0, "işlem yapmamak da pozisyondur".
11. **Kazanırken büyüt, kaybederken küçült:** Minervini "progressive exposure", Turtle −%10 → −%20. Kullamägi nakitten marjine haftalar–aylar içinde geçiyor.
12. **Ölçüm:** Her işlem R ile kaydedilir. İzlenenler: isabet, ortalama kazanç/kayıp, en uzun kayıp serisi, setup başına beklenti. Brandt hedefi: 100 işlemde PF 3,0.

### 1.4 Bu kurallar bugün (6.11.2026) ne diyor?

| Gösterge (5.11 kapanış) | Değer | Kurala göre |
|---|---|---|
| NDX ve 10/20/50 GHO | 26.629,8 / 28.672 / 29.286 / 29.686. 10<20 19.10'dan beri, iki ortalama da düşüyor. Zirveden −%14,7 (6.10: 31.224,7) | Kullamägi: yeni long yok. IBD: correction, FTD bekle |
| S&P 500 | 7.353,7. 200 GHO 7.322,7, yani hemen üstünde. 50 GHO 7.686,5 | Geniş piyasa sınırda, teknoloji liderliği kırık |
| VIX vade yapısı | VIX 28,18 < VIX9D 32,66; VIX3M 25,55 (ters) | Kısa vadeli stres. Opsiyon almak pahalı |
| Tema ETF'leri (52 hafta zirvesinden) | SMH −%30,0 (50 GHO'nun %16,9 altında), URA −%49,6, TAN −%40,3, IBIT −%28,8, XLK −%18,0 | AI donanım, nükleer ve kripto kümeleri Stage 3/4'te |
| Genişlik | NYSE yükselen/düşen 416/2.344 | Dağıtım günü |

Kaynak: FRED NASDAQ100/SP500 serileri ve Cboe VIX CSV'leri (kardeş ajanın 6.11 snapshot'ı, scratchpad), ETF tablosu (aynı snapshot) [VERİ, H]. https://fred.stlouisfed.org/series/NASDAQ100 ; https://www.cboe.com/tradable_products/vix/vix_historical_data/

**Pratik çıkarım (9.11.2026 Pazartesi):**
- Profesyonellerin kendi kural setleri bu tabloda **tam boyutlu yeni long'a izin vermiyor**.
- Yapılacaklar:
  - Endeks düşerken 50 GHO üstünde kalan ve RS çizgisi zirvede olan isimlerden izleme listesi kurmak (O'Neil/Minervini gözlemi; akademik teyidi yok).
  - FTD (rally denemesinin 4.+ günü, artan hacim, ≥~%1,25 artış) ya da 10>20 kesişimiyle **pilot** açmak: ≤%0,25 risk, toplam ısı ≤%2.
  - Short tarafında parabolic short ve başarısız kırılım short'u düşünülebilir, ama küçük boyutla. Daniel-Moskowitz: ayı rallileri short'ları ezer.
- BIST tarafında aynı rejim kontrolü XU100/XU030 için yapılmalı. TL'de nakit %36–40 nominal kazandırdığı için **"nakitte bekle" kararının TL'deki fırsat maliyeti ABD'dekinden çok daha düşük.**

### 1.5 Şüpheci notlar

- **Survivorship ve yarışma teşviki:** USIC'te katılımcıların yalnızca %8–17'si yılı kârla kapatıyor (`abd_kim_kazaniyor.md` §4.1). Yarışma ödülü konveks olduğu için aşırı kaldıracı ödüllendiriyor. Tek yıllık %500+ getiri beceri kanıtı değil; asıl sinyal kalıcılık.
- **Öz beyan:** Kullamägi'nin FAQ'ı denetim veya ekstre içermiyor. "Filtreye uysaydım kayıpların %90'ı önlenirdi" bir hindsight tahmini. Minervini'nin 2021 istatistiği silinmiş bir tweet.
- **Ticari çıkar:** Minervini (seminer, Private Access) ve TraderLion (Kell/Luk içerikleri) eğitim satıyor.
- **Mekanik test mütevazı:** Kullamägi breakout'unun kural tabanlı kopyası (SPY >140 EMA filtresi, MA trail) 2008–2025'te 2.382 işlemde **CAGR %19, MDD −%21** verdi. 3 günlük çıkış ve 1 ATR stop kötü sonuç verdi. Rakam overfit'e ve survivorship'e açık, maliyet raporlanmadı [İKİ]. https://stonkscapital.substack.com/p/modeling-kullamagi-part-2-momentum
- Kendi yöntemini 82 işlemle deneyen bir taklitçi kâra geçemedi. Tek günde 16 işlemin 13'ü kayıptı, yani korelasyon tuzağı [İKİ]. https://valuefund.substack.com/p/how-does-one-trader-turn-9100-into
- **Kural uyumu:** Minervini ve Kullamägi'yi mekanik kopyadan ayıran kısım seçim kalitesi ve rejimde boyut değişimi. Bu kısım ölçülemiyor ve devredilemiyor.

---

## 2. Asimetrik swing için opsiyonlar

### 2.1 Kanıt: sistematik opsiyon alımı vs edge'e kaldıraç

| Çalışma | Bulgu | Not |
|---|---|---|
| Coval & Shumway (2001, JF) [AK] | S&P 500'de zero-beta ATM straddle ≈ **−%3/hafta**. Call'lar beta'nın öngördüğünden az kazandırıyor | Endeks. Vol risk primi (VRP) alıcıdan satıcıya akıyor. https://econpapers.repec.org/RePEc:bla:jfinan:v:56:y:2001:i:3:p:983-1009 |
| Boyer & Vorkink (2014, JF) [AK] | Ex-ante çarpıklığa göre sıralanan portföylerde haftalık getiri farkı %10–50. Çalışma kâğıdında 7 günlük yüksek çarpıklıklı call'lar **−%35,4/hafta**, düşük çarpıklıklılar +%1,4 (1996–2009, mid, vadeye kadar tutma) | OTM ve kısa vade = piyango primi. Spread'ler çarpıklıkla açılıyor, satıcı da primin hepsini alamıyor. https://ideas.repec.org/a/bla/jfinan/v69y2014i4p1485-1527.html ; https://www.cxoadvisory.com/equity-options/sell-lottery-tickets-for-their-fun-and-your-profit |
| Frazzini & Pedersen (2022, RAPS) [AK] | Gömülü kaldıraç arttıkça riske göre getiri düşüyor. Low-minus-high leverage t-stat: hisse opsiyonu 8,6, endeks opsiyonu 6,3. Hisse opsiyonu kaldıracı 2–20× | Kaldıraç kısıtlı yatırımcı kaldıraca prim ödüyor. https://econpapers.repec.org/RePEc:oup:rasset:v:12:y:2022:i:1:p:1-52. |
| Cao & Han (2013, JFE) [AK] | Delta-hedged hisse opsiyonu getirisi idiosenkratik vol ile monoton olarak düşüyor | **Sıcak tema hisselerinde opsiyon yapısal olarak pahalı.** https://econpapers.repec.org/RePEc:eee:jfinec:v:108:y:2013:i:1:p:231-249 |
| Goyal & Saretto (2009, JFE) [AK] | RV−IV farkına göre long/short straddle ekonomik ve istatistiksel olarak anlamlı. Effective spread = yarım kotasyon varsayımıyla **~%5,3/ay**; tam kotasyonla bir bacak ~%4,1/ay | Opsiyonu **IV, RV'ye göre ucuzken** al. https://ideas.repec.org/a/eee/jfinec/v94y2009i2p310-326.html ; https://www.cxoadvisory.com/volatility-effects/making-money-with-options-based-on-superior-volatility-forecasts |
| Bryzgalova, Pavlova & Sikorskaya (2023, JF) [AK] | Retail Kasım 2019–Haziran 2021'de ~**2,1 milyar $** kaybetti (JF versiyonu). Basın: maliyetlerle ~4,1 milyar $ daha. Retail'in sevdiği opsiyonlarda ortalama spread %12,6 | Kısa vadeli ucuz OTM tercih ediliyor. https://lbsresearch.london.edu/id/eprint/2827 |
| de Silva, Smith & So (2025, RoF) [AK] | Retail, beklenen duyuru vol'ü yüksek earnings'lerden önce opsiyon alıyor, realize vol'e göre fazla ödüyor, duyurudan sonra geç kapatıyor. Çift haneli yüzde kayıp | Earnings boyunca çıplak long = "crush vergisi". https://www.gsb.stanford.edu/faculty-research/publications/losing-optional-retail-option-trading-expected-announcement |
| Gao, Xing & Zhang (2018, JFQA) [AK] | ATM straddle, duyurudan 3 gün önceden duyuru gününe kadar **+%3,34** (brüt) | Duyuru öncesi IV run-up ayrı ve kısa bir işlem. Spread sonrası marj ince. https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/anticipating-uncertainty-straddles-around-earnings-announcements/7B34877AD5E06304BA3C55FBA3219FDD |
| EarningsWatcher (2026, ticari) [İKİ] | 2023–2026'da 28.898 ABD earnings: implied ±%9,18, gerçekleşen ±%6,32. Raporların yalnızca %25,2'si implied'ın dışında kapandı | Yöntem doğrulanmadı. Akademik bulgularla aynı yönde. https://earnings-watcher.com/wiki/options-implied-move-vs-actual-earnings-study-2026 |
| Muravyev & Pearson (2020, RFS) [AK] | Zamanlama yapan trader'ların effective spread'i geleneksel ölçünün <%40'ı. Ortalama düzeltilmiş spread geleneksel ölçünün ~2/3'ü, kotasyonun ~yarısı | Limit emir ve zamanlama maliyeti ciddi düşürüyor. https://ideas.repec.org/a/oup/rfinst/v33y2020i11p4973-5014..html |
| Israelov (2019, JAI / AQR) [AK] | Koruyucu put, drawdown'ı azaltmada statik maruziyet düşürmekten kötü. Cboe %5 put-protection endeksinin aşırı getirisi = %36,5 S&P + %63,5 nakit | Hedge = önce brüt maruziyeti azalt. https://www.aqr.com/insights/research/white-papers/pathetic-protection-the-elusive-benefits-of-protective-puts |
| Cboe PUT endeksi (Ennis Knupp 2009; Bondarenko 2019) [İKİ, Cboe destekli] | 1986–2008: PUT %10,32/yıl, vol %9,91 (S&P vol %15,39). 1990–2018: vol %9,95 vs %14,93, beta 0,56 | Endeks düzeyinde put satımı VRP topluyor. Tekil hissede spread ve kuyruk riski yüksek. https://www.cboe.com/insights/posts/white-paper-shows-volatility-risk-premium-facilitated-higher-risk-adjusted-returns-for-put-index |

**Sentez:**
- Koşulsuz olarak opsiyon alıcısı **ödeyen taraf**: VRP, piyango primi ve spread.
- Opsiyon yalnızca üç koşul birlikte sağlanınca "edge'e kaldıraç" olur:
  1. Koşullu dağılımın sağ kuyruğu IV'nin fiyatladığından kalın olmalı (bilgi edge'i ya da rejim edge'i).
  2. IV kendi geçmişine ve RV'ye göre ucuz olmalı.
  3. Spread ve zamanlama maliyeti kontrol edilmeli.
- **Belgelenmiş örnek:**
  - Chris Camillo: Schwager'ın doğruladığı rakama göre 2006–2020'de ~%77/yıl.
  - Opsiyonları ATM/ITM ve katalizör penceresini kapsayan vadeyle, yüksek inançlı bilgi asimetrisinde kullanıyor; uzak OTM'den kaçınıyor [İKİ].
  - Kullamägi opsiyonu denemiş, "bana göre değil" demiş [İKİ]. Minervini, Luk ve Ryan'ın kayıtları ağırlıkla hisse ve marjin.
  - Kaynaklar: https://www.ibtimes.co.uk/chris-camillo-10-million-stock-success-1798668 ; https://www.forex.in.rs/social-arb-playbook ; https://retailtradersrepository.substack.com/p/kristjan-kullamagi-qullamaggie-stream-d8c

### 2.2 Kendi hesabım: breakout'ta hisse vs opsiyon yapıları (Black-Scholes)

**Varsayımlar:**
- S = 100, r = %4, temettü yok.
- 1R = hisse 3. günde 92'ye düşüp stop olduğunda yaşanan kayıp. Opsiyon pozisyonları da **dayanak fiyatına bağlı aynı stopla** çıkıyor ve aynı 1R'ye boyutlanıyor.
- Stop senaryosunda IV +5 puan, gap senaryosunda +15 puan.
- Yarım spread: ATM/ITM %3, spread %5, LEAPS %2, OTM %8 (retail ortalama tam spread %12,6 ile uyumlu).
- Skew ve VRP yok, yani BS iyimser.

**IV %45: enstrüman özellikleri ve R cinsinden K/Z**

| Enstrüman | Prim | Delta | Theta/gün (primin %'si) | Stop 92 (3. gün) | Yatay 100 (10. gün) | +%10 (10. gün) | +%20 (15. gün) | +%35 (25. gün) | Gap −%20 (1. gün) | +%10, IV −15 puan | Maks. kayıp (tüm prim), R |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Hisse, stop −%8 | – | 1,00 | – | −1,00 | 0,00 | +1,25 | +2,50 | +4,38 | **−2,50** | +1,25 | – |
| ATM call 45g K100 | 6,53 | 0,54 | −1,15 | −1,00 | −0,34 | +1,55 | **+3,91** | **+7,97** | −1,56 | +1,17 | 1,95 |
| ITM call 60g K90 | 13,43 | 0,76 | −0,40 | −1,00 | −0,24 | +1,23 | +2,84 | +5,39 | −1,73 | +1,10 | 2,47 |
| Call spread 45g 100/120 | 5,40 | 0,40 | −0,62 | −1,00 | −0,31 | +1,23 | +2,77 | +4,30 (tavan) | −1,56 | +1,32 | 1,95 |
| Deep ITM LEAPS 365g K60 | 44,15 | 0,93 | −0,03 | −1,00 | −0,23 | +0,90 | +2,06 | +3,82 | −1,97 | +0,78 | 5,55 |
| OTM call 21g K110 | 1,22 | 0,21 | **−6,27** | −1,00 | **−0,84** | +1,77 | +7,59 | +20,25 | −1,18 | +0,79 | 1,23 |

IV %60'ta yön aynı, büyüklük daha zayıf. Örnekler: ATM 45g +%20'de +3,14R, yatayda −0,39R, "+%10 ve IV −15 puan"da +0,82R. LEAPS K60'ta delta 0,89, extrinsic %6,7.

**Okuma:**
1. Hisseyle aynı stop-R'de ATM 45–90 günlük call, büyük hareketlerde (+%20 ve üzeri) **1,5–1,8×** R üretiyor. Yatayda −0,3/−0,4R kaybediyor, küçük kazançlarda (+%5) hisseden geride.
2. Gap-down'da opsiyonun kaybı primle sınırlı: −1,6R, hissede −2,5R. **Bu, TR mukimi için gerçek bir avantaj.** Premarket 11:00 TSİ'de başlıyor ve haber gap'leri uyurken geliyor.
3. **IV crush avantajı siliyor:** +%10 ve IV −15 puanda ATM call +1,17R, hisse +1,25R.
4. Call spread sağ kuyruğu kesiyor. Trend DNA'sında kârın çoğunu işlemlerin <%7'si üretiyor (Zarattini et al., `abd_kim_kazaniyor.md`). Spread bu yüzden **ana araç değil**; earnings veya yüksek IV için.
5. OTM 21 günlük call'da theta primin %6'sı/gün. Tabloda +%35'te +20R görünüyor, ama bu BS'nin "IV = gerçek dağılım" varsayımının ürünü. Ampirik olarak bu kova en pahalı kova (Boyer-Vorkink, Cao-Han).
6. **Dar stoplu (LOD, ≤1 ATR) Kullamägi girişine opsiyon uymuyor:** spread ve delta küçük R'yi yiyor. Opsiyon daha çok geniş stoplu ve haftalarca tutulan Minervini/Weinstein tipi pozisyona uyuyor.

**Varsayımsal dağılımla beklenti** (hassasiyet amaçlı; olasılıklar bana ait)
- İyi rejim: stop %58, scratch %15, +%10 %10, +%20 %8, +%35 %4, +%60 %3, gap %2. İsabet %25.
- Zayıf rejim: stop %66, scratch %14, +%10 %8, +%20 %4, +%35 %2, +%60 %0,5, gap %5,5.

| IV / rejim | Hisse | ATM 45g | ATM 90g | ITM 60g | Spread 100/120 | LEAPS K60 |
|---|---|---|---|---|---|---|
| %45, iyi | +0,10R | **+0,57R** | +0,44R | +0,21R | 0,00R | −0,04R |
| %45, zayıf | −0,47R | −0,28R | −0,34R | −0,42R | −0,47R | −0,54R |
| %60, iyi | +0,10R | +0,35R | +0,25R | +0,14R | −0,08R | −0,05R |
| %60, zayıf | −0,47R | −0,39R | −0,43R | −0,46R | −0,53R | −0,54R |

**Sonuç:**
- Opsiyon edge'i yaratmıyor; edge'in sağ kuyruğunu büyütüyor.
- Zayıf rejimde her yapı negatif. Opsiyonun tek kazancı gap koruması.
- IV yüksekken (%60) avantaj yarıya iniyor.
- **Karar değişkeni opsiyon değil, rejim ve IV seviyesi.**

**Deep ITM LEAPS'in örtük maliyeti** (365 gün; extrinsic ≈ put değeri + finansman; yıllık maliyet = extrinsic / K)

| IV | K50 (delta) | K60 | K70 | K80 |
|---|---|---|---|---|
| %35 | %4,2 (0,99) | %5,0 (0,96) | %6,5 (0,90) | %8,9 (0,82) |
| %45 | %5,3 (0,97) | %6,9 (0,93) | %9,3 (0,87) | %12,3 (0,79) |
| %60 | %8,3 (0,94) | %11,1 (0,89) | %14,4 (0,83) | %17,9 (0,77) |

- LEAPS = margin kredisi + koruyucu put. Düşük vol'lü liderde (IV ≤%35) maliyet margin faizine yakın (Fed bandı %3,75–4,00 + broker marjı; IBKR oranı `abd_pratik.md`).
- Tema hissesinde (IV %45–60) yılda %7–14 maliyet çıkıyor. "Stock replacement" orada pahalı. Getirisi: margin call yok ve gap'te tavan kayıp.

Betikler: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/abd_prof/opt_compare.py` ve `.../ev_mix2.py` [H].

### 2.3 Yapı yapı karar tablosu

| Yapı | Ne zaman | Parametreler | Kanıt | Ne zaman değil |
|---|---|---|---|---|
| **Long call (breakout'ta hisse yerine)** | IV kendi 1 yıllık geçmişinin alt ~%30–40'ında ve IV ≤ RV20 (Goyal-Saretto yönü); tutma penceresinde earnings yok; hızlı ve büyük hareket beklentisi | 45–90 gün, delta 0,55–0,70. Prim ≤1,5–2R. Çıkış dayanak fiyatına bağlı koşullu emirle | §2.1, §2.2 | IV yüksek (bugünkü VIX 28 ve 5.11 sonrası tekil IV'ler), earnings içeren pencere, dar LOD stopu |
| **Call debit spread** | Earnings veya event, yüksek IV, hedef fiyat net | ATM al, +%10–20 OTM sat, 30–60 gün | OTM bacak pahalı "piyango"yu satıyor (Boyer-Vorkink). Vega ve crush nötre yakın | Trend taşıma pozisyonu: sağ kuyruğu kesiyor |
| **Deep ITM LEAPS** (delta 0,8–0,9) | Düşük IV'li lider, aylarca tutma, margin kullanmak istememe | 6–12 ay, K ≈ S × 0,6–0,7 | §2.2 maliyet tablosu | IV >%45 olan tema hissesi. Maliyet %7–14/yıl |
| **Risk reversal** (OTM call al / OTM put sat) | Hisseyi K_put'tan zaten almaya hazırsan ve put skew'i pahalıysa | Margin onayı gerekir | Put satışı VRP topluyor (endeks düzeyinde kanıt) | Stop tabanlı trader için: put altında sınırsız gap riski. 5.11 tipi −%17 gün |
| **Put satarak girme** | Pullback ile girme stili (Luk/Kell EMA crossback): "o seviyeden zaten alırım" | Cash-secured, 30–45 gün, delta 0,25–0,35 | PUT endeksi: hisse benzeri getiri, ~2/3 vol (endeks) | Breakout stili: düşüşte dolarsın (ters seçim), kırılımı kaçırırsın |
| **Endeks/tema put hedge'i** | Kısa ve tanımlı olay riski | Önce brüt maruziyeti azalt (Israelov). Sonra MES/MNQ mikro vadeli short ya da kısa vadeli put **spread** (SMH/QQQ) | Israelov: put, maruziyet düşürmekten kötü | Sürekli rulolanan put. Bugün VIX ters yapıda, koruma en pahalı anında |
| **Duyuru öncesi straddle** | Earnings'ten 3 gün önce al, duyurudan önce sat | Likit isim, ATM | +%3,34 brüt (GXZ 2018) | Spread >%5 ise beklenti ~0 |

### 2.4 Likidite ve uygulama kuralları (pratisyen konvansiyonu [İKİ] + kanıt)

- **Spread / mid:**
  - ATM'de ≤%5 ideal, ≤%10 kabul; >%20 ise edge spread'den sağ çıkmaz.
  - ATM'de %5 spread, 10-delta'da genellikle %20+ demek.
  - Kaynak: https://flashalpha.com/concepts/liquidity [İKİ].
- **Open interest:** Kontratta ≥500–1.000. Emir ≤ OI'nin %5–10'u. Günlük hacim yüzlerle ölçülmeli. OI destekleyici kanıt; belirleyici olan dar spread.
- **Emir:**
  - Mid'den limit, gerekirse 1 tick yürüt. **Asla piyasa emri yok.**
  - Açılışın ilk 30–60 dakikasında spread geniş; Muravyev-Pearson'a göre zamanlama effective maliyeti ~1/3 düşürüyor.
- **Stop:** Opsiyon primine stop konmaz. Kural "dayanak X'i kırarsa opsiyonu sat" (IBKR koşullu emir).
- **Vade:** Haftalık ve 0DTE yok. Tutma süresi × 2'den uzun vade seçilir (Camillo: katalizör penceresi + yedek pencere).
- **Earnings takvimi:** Pencereye düşüyorsa ya çık, ya spread'e çevir, ya da boyutu "earnings size"a indir.
- **Maliyet:** IBKR 0,65 $/kontrat, Midas 1,5 $/kontrat (yalnızca long). Ayrıntı: `abd_pratik.md` §1.

### 2.5 TR mukimi için uygunluk

- **Erişim:** IBKR (opsiyon onayı beyan edilen deneyime bağlı) ve Midas (yalnızca call/put alımı). Ayrıntı: `abd_pratik.md` §1.2–1.4.
- **Vergi:** Yurt dışı türev kazancı %15–40 artan oranlı ve kur farkı dahil (`abd_pratik.md` §2.1, özelgeyle doğrulanmadı). VİOP pay ve endeks türevlerinde stopaj %0 (`abd_pratik.md` §2.3).
- **871(m):**
  - Notice 2026-61 (21.09.2026), non-delta-one işlemlerin muafiyetini 2028 sonuna kadar uzattı.
  - Delta ≥0,8 deep ITM opsiyonların dividend-equivalent stopajı en erken 2029'da gündeme gelir. Büyüme hisselerinin çoğu zaten temettü ödemiyor.
  - Kaynaklar [RD]: https://www.irs.gov/pub/irs-drop/n-26-61.pdf ; https://www.mayerbrown.com/en/insights/publications/2026/09/section-871m-phase-in-extended-two-more-years
- **Saat:** Normal seans 17:30–00:00 TSİ (yaz saati 1.11'de bitti). Opsiyonlar yalnızca normal seansta işlem görüyor. Hisse stopları premarket gap'lerinde kayıyor; opsiyonun tavan kaybı burada değer kazanıyor.
- **Önerilen alt küme:**
  - (i) Çekirdek: hisse + yapısal stop + rejim anahtarı.
  - (ii) Uygun koşulda (düşük IV, earnings yok) ATM/ITM 45–90 günlük call. Primle sınırlı kayıp, R'nin 1,5–2 katını geçmesin.
  - (iii) Earnings ve yüksek IV'de debit spread.
  - (iv) Hedge önce maruziyet azaltımı, sonra mikro vadeli veya put spread.
  - Kaçınılacaklar: <30 günlük OTM, çıplak short (marjin ve gap), IV >%45 isimde LEAPS.

### 2.6 VİOP XU030 opsiyonları: likidite gerçeği (5.11.2026 bülteni) [VERİ, H]

| Ürün (5.11.2026) | Seri | İşlem gören seri | İşlem sayısı | Prim (mn TL) | Nominal (mn TL) | Açık pozisyon |
|---|---|---|---|---|---|---|
| BIST30 vadeli | 3 | 3 | 107.146 | – | **51.791** | 451.434 |
| BIST30 opsiyon | 151 | **36** | **665** | **24,7** | 1.188 (vadelinin **%2,3**'ü) | 133.994 |
| – Aralık 2026 vadesi | 63 | – | 582 | 21,8 | – | 130.236 |
| – Şubat 2027 vadesi | 58 | – | 83 | 2,9 | – | 3.684 |
| – Nisan 2027 vadesi | 30 | – | **0** | 0 | – | 74 |
| Pay opsiyonları (tümü) | 2.257 | **289** | 2.036 | 36,1 | 1.037 | 863.709 |

4.11'de BIST30 opsiyonunda 997 işlem, prim 44,2 mn TL, nominal vadelinin %2,7'si. Ekim'in son haftasında (önceki çalışma, `ajanlar/r1_opsiyon.md`) nominal vadelinin %5–14'ü idi.

- **Yoğunlaşma:** Hacim Aralık ATM ±1.000 puanda. En çok işlem gören seriler P15500 (69 işlem, 8,5 mn TL), P15000 (111 işlem) ve P14500 (100 işlem). Akış put ağırlıklı, yani hedge talebi.
- **Fiyat güvenilirliği:** Uzlaşma ile son işlem arasında büyük fark var. Örnek P14500: kapanış 194, uzlaşma 291,5. Uzlaşma fiyatları model fiyatı gibi davranıyor; ekran fiyatı ve bülten fiyatı aynı şey değil. Önceki çalışmanın ekran gözlemine göre kanatlar tek taraflı, ATM makası tahminen %5–15, emir başına uygulanabilir boyut 10–50 kontrat.
- **Pay opsiyonları:** Seri başına günde ortalama <1 işlem. En likit örnek THYAO Kasım C300: 79 işlem, 3,2 mn TL. **Pratikte tekil swing kaldıracı olarak kullanılamaz.**
- **TL taşıma:** Opsiyon vadeliden fiyatlanıyor ve vadeli %36–40 TL faizini içeriyor. Long call ve call spread başabaşına taşıma ekleniyor. Önceki çalışmada call spread başabaşındaki +%6,4'ün %4,9'u yalnızca taşımaydı.
- **Uygun kullanım:**
  - (i) TCMB, siyasi takvim ve kur şoku gibi olaylarda endeks put spread'i ile BIST hisse kümesini hedge etmek.
  - (ii) Tanımlı riskli endeks görüşü (call/put spread, Aralık vadesi).
  - (iii) Asıl hedge aracı likit XU030 vadelisi; günde 51,8 milyar TL.
- Kaynaklar: https://www.borsaistanbul.com/data/vadeli/viop_20261105.csv ; https://www.borsaistanbul.com/data/vadeli/viop_20261104.csv
- Ayrıştırıcı: `raporlar/hesaplar/opsiyon/viop_parse.py`. Zincir istatistiği scratchpad'de: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/viop_chain_stats.py`.

---

## 3. Risk mühendisliği: "stratejik kümeler"

### 3.1 Profesyonellerin ısı ve maruziyet kuralları

| Kaynak | Kural | Tür |
|---|---|---|
| Turtle | 1 birim = 1N için %1. Tek piyasa ≤4 birim, **yakın ilişkili piyasalar ≤6**, gevşek ilişkili ≤10, tek yön ≤12. Her −%10'da nominal −%20 | Yayımlanmış kural |
| Alexander Elder | İşlem başı ≤%2. **Ayın realize zararı + açık risk ≥%6 → ay sonuna kadar yeni işlem yok.** Öneri: ≥%0,5 maliyet payı | Kitap. https://www.incrediblecharts.com/trading/6_percent_rule.php |
| Kullamägi | Risk ≤%0,5 (tavan %1). Pozisyon %10–20. **Tek hissede gece ≤%30.** Marjine kademeli geçiş. Günlük kayıp limiti yok | RÖP/KİT |
| Minervini | %1,25–2,5 risk. En iyi 4–5 isimde %20–25. Toplam ≤10–12. Progresif maruziyet | İKİ |
| Brandt | 60–70 bps risk. Aynı anda 3–4 piyasa ve 2–3 bekleyen emir. İlişkili riski yönetiyor ama sayısal tavan vermiyor. Yıllık DD'yi çok düşük tutmayı hedefliyor (podcast özetinde <%1, olağan %2–3; özet hatası olabilir) | RÖP (2026) |
| IBD | Piyasa durumuna göre maruziyet: FTD sonrası %40–60, oturmuş trendde %80–100 | İKİ |
| Kell | Earnings'e "earnings size" ile girme | İKİ |

**Turtle'ın 6/10/12 yapısını hisse kümelerine çevirince:**
- %0,5 risk/işlemde aynı tema ≤3 pozisyon, yani ≤%1,5 ısı.
- İlişkili temalar toplamı ≤%2,5–3.
- Tek yön toplamı ≤%5–6. Bu, Elder'in %6 tavanıyla örtüşüyor.

### 3.2 Veri: kümeler birleşiyor (Ken French 49 endüstri, günlük, değer ağırlıklı) [H, VERİ]

| Dönem | ρ(Chips, Hardw) | ρ(Chips, ElcEq) | ρ(Chips, Softw) | ρ(Chips, Util) | Piyasadan arındırılmış ρ(Chips, ElcEq) / (Hardw, ElcEq) | Beta ElcEq / Chips | Yıllık vol ElcEq |
|---|---|---|---|---|---|---|---|
| 2015–2019 | 0,77 | 0,70 | 0,79 | 0,28 | 0,00 / 0,02 | 1,14 / 1,21 | %18,7 |
| 2022 | 0,87 | 0,82 | 0,91 | 0,54 | −0,13 / −0,10 | 1,27 / 1,35 | %35,9 |
| 2024–Eylül 2026 | 0,73 | 0,64 | 0,64 | 0,15 | 0,12 / 0,38 | 1,55 / 1,62 | %34,5 |
| **2026 (Ocak–Eylül)** | 0,66 | **0,72** | **0,31** | −0,06 | **0,43 / 0,50** | **2,18** / 1,65 | **%44,5** |

**Okuma:**
1. 2026'da **"AI donanım" tek risk kümesi:** yarı iletken + bellek/donanım + elektrik ekipmanı/güç. Piyasa etkisi çıkarıldıktan sonra bile korelasyon 0,4–0,5; 2015–19'da sıfırdı. Kullanıcının "AI semis" ve "power" kümeleri **ayrı tema sayılmamalı.**
2. Yazılım 2026'da bu kümeye karşı negatif artık korelasyonda (−0,49/−0,50). Doğal hedge adayı, ama 2022'de herkes birlikte düştü (ρ 0,82–0,91).
3. 2024–Eylül 2026'da Chips'in −%4'ten kötü olduğu 17 günde Hardw ortalama −%4,40, ElcEq −%4,04, Softw −%2,67, Util −%0,67. Bu günlerin %71–76'sında ElcEq ve Hardw de −%3'ten kötü kapandı.
4. Ortalama ρ = 0,69 ile etkin bahis sayısı n/(1+(n−1)ρ): 3 pozisyon → 1,26, 5 → 1,33, 8 → 1,37. Kümede pozisyon sayısını artırmak çeşitlendirme sağlamıyor.
5. Uyarı: endüstri portföyleri tekil hisse korelasyonunu düşük gösterir. Tekil hissede idiosenkratik gürültü ikili korelasyonu düşürür, ama çöküş günlerinde birlikte hareket artar. Kripto hisseleri (COIN/MSTR/miner'lar) bu veride yok; IBIT'in −%28,8 düşüşü kümenin BTC'ye bağlı olduğunu gösteriyor.

Betikler: `.../scratchpad/abd_prof/ff_corr.py`, `ff_tail.py`. Veri: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html (Eylül 2026 sürümü).

### 3.3 Monte Carlo: kümelenme ve drawdown kuralları [H]

**Model A (aynı beklenti, bağımsız vs kümeli):**
- Yılda 160 işlem: 40 dalga × 4 eşzamanlı pozisyon.
- İsabet %27. Kazanç 0,5 + Exp(3,5)R (ortalama ~4R). Scratch %13. Kayıpların %5'i gap'li (−2R).
- Beklenti +0,45R/işlem.
- Kümeli versiyon: dalgaların %30'unda tema bozuluyor ve 4 pozisyon birlikte stop oluyor. Toplam beklenti sabit tutuluyor.
- 20.000 yol.

| Risk/işlem | Bağımsız: medyan getiri | MDD medyan | **MDD %5 kötü** | P(MDD < −%20) | Kümeli: medyan getiri | MDD medyan | **MDD %5 kötü** | P(MDD < −%20) |
|---|---|---|---|---|---|---|---|---|
| %0,25 | %18,9 | −%3,3 | −%6,4 | %0,0 | %18,7 | −%4,6 | −%9,0 | %0,0 |
| %0,50 | %40,1 | −%6,6 | −%12,7 | %0,2 | %39,1 | −%9,1 | **−%17,4** | %2,0 |
| %1,00 | %90,4 | −%12,9 | −%23,9 | %12,5 | %86,6 | −%17,6 | **−%32,3** | **%37,0** |
| %2,00 | %220,9 | −%24,5 | −%43,4 | %72,9 | %199,7 | −%32,7 | −%54,9 | %93,6 |

**Model B (rejimli):**
- İyi rejim: beklenti +0,48R, tema bozulması %15.
- Kötü rejim: beklenti −0,25R, bozulma %30.
- Kalıcılık: iyi rejimde kalma olasılığı %90, kötüde %80. Kötü rejim payı ~%33.
- Genel beklenti ≈ +0,24R, isabet ~%23.

| Risk | Kural | Medyan getiri | Ortalama | MDD medyan | MDD %5 kötü | P(yıl < −%10) |
|---|---|---|---|---|---|---|
| %0,5 | Yok | %19,7 | %22,8 | −%11,1 | −%22,7 | %7,1 |
| %0,5 | Turtle (her −%10'da −%20) | %19,4 | %22,9 | −%11,2 | −%21,7 | %8,1 |
| %0,5 | **Merdiven (−%5: ×0,5, −%10: ×0,25)** | %14,5 | %19,3 | −%8,9 | **−%12,9** | %3,6 |
| %1,0 | Yok | %37,6 | %50,9 | −%21,5 | −%40,6 | %13,1 |
| %1,0 | Turtle | %37,1 | %50,7 | −%21,2 | −%37,0 | %14,9 |
| %1,0 | **Merdiven** | %20,6 | %34,5 | −%13,2 | **−%18,9** | %9,7 |

Kontrol için aynı beklentili ama rejimsiz (iid) bir versiyon koştum. %1 riskte merdiven: medyan %36,2 → %15,8, MDD %5 kötü −%36,6 → −%17,6. %0,5 risk ve kuralsız: %18,4 / −%19,9.

**Okuma:**
1. **Kümelenme, beklenti aynı kalsa bile kuyruk riskini ~%35–40 büyütüyor.** %1 riskte −%20'lik DD olasılığı 3 kat artıyor (%12,5 → %37). Kümeli bir kitapta "işlem başı %1" aslında işlem başı %1,5–2 gibi davranıyor.
2. **Turtle kuralı bir yıllık ufukta pek tetiklenmiyor.** Etkisi küçük; başlangıç sermayesine göre ölçtüğü için yavaş.
3. **Merdiven** %5 kötü MDD'yi yaklaşık yarıya indiriyor ama medyan getiriden ~17 puan alıyor.
   - Rejimli dünyada "%1 + merdiven" (medyan %20,6, %5 kötü −%18,9), "%0,5 sabit"e (%19,7 / −%22,7) göre biraz daha iyi.
   - Rejimsiz dünyada ise daha kötü (%15,8 / −%17,6 vs %18,4 / −%19,9).
   - Yani drawdown kuralı **yalnızca performans rejime bağlıysa** değer katıyor. Kaminski-Lo'nun teorik sonucuyla birebir uyumlu.
4. Momentum ve tema swing'inde performans güçlü biçimde rejime bağlı: 2022'de FFTY −%51, Kullamägi −%57. Merdiven bu yüzden **ikincil emniyet kemeri olarak** savunulabilir. **Birincil araç doğrudan rejim filtresi.**

Betikler: `.../scratchpad/abd_prof/mc_heat2.py`, `mc_ddrule2.py`.

### 3.4 Volatilite hedefleme ve drawdown kontrolü kanıtı

| Çalışma | Bulgu | Kullanıcı için anlamı |
|---|---|---|
| Moreira & Muir (2017, JF) [AK] | Vol yüksekken risk azaltma: piyasada alfa %4,9, Sharpe +%25 (çalışma kâğıdı). Faktörlerde Sharpe +%50–100 | Teori güçlü. https://www.nber.org/papers/w22208 |
| Cederburg, O'Doherty, Wang & Yan (2020, JFE) [AK] | 103 stratejide gerçek zamanlı uygulamada vol yönetimi sistematik olarak üstün değil. **İstisnalar: MOM, ROE, BAB** | Momentum benzeri swing'de vol ölçekleme savunulabilir. https://econpapers.repec.org/RePEc:eee:jfinec:v:138:y:2020:i:1:p:95-117 |
| Barroso & Santa-Clara (2015, JFE) [AK] | Riski yönetilen momentumda Sharpe 0,53 → ~0,97, çöküşler neredeyse yok | ATR/vol'e göre boyut doğru yaklaşım. https://econpapers.repec.org/RePEc:eee:jfinec:v:116:y:2015:i:1:p:111-120 |
| Harvey et al. (2018, JPM) [AK] | ABD hissede Sharpe 0,40 → 0,48–0,51. Vol-of-vol %4,6 → %1,8. Sol kuyruk hafifliyor | Getiri motoru değil, kuyruk kesici. https://quantpedia.com/the-impact-of-volatility-targeting-on-equities-bonds-commodities-and-currencies |
| Daniel & Moskowitz (2016, JFE) [AK] | Momentum çöküşleri ayı sonrası toparlanmalarda geliyor. Dinamik ölçekleme Sharpe'ı ~2 katına çıkarıyor | Dipten sert rallide short ve pair'leri küçült. https://www.nber.org/papers/w20439 |
| Han, Zhou & Zhu (2016) [AK, çalışma kâğıdı] | Momentumda hisse bazlı %10 stop-loss: eşit ağırlıklı en kötü aylık kayıp −%49,79 → −%11,36 (1926–2013). Sharpe ~0,17 → ~0,37. Brüt | Stop'un gap'te stop fiyatından dolduğu varsayımına ve maliyete duyarlı. Alpha Architect'in replikasyon yazısı var (bu oturumda okunamadı). https://www.cxoadvisory.com/technical-trading/stop-losses-to-avoid-stock-momentum-crashes/ |
| Kaminski & Lo (2014, JFM) [AK] | Rastgele yürüyüşte stop-loss beklenen getiriyi **daima düşürür**. Momentum veya rejim geçişi varsa değer katabilir. Çalışma kâğıdı: stop-out dönemlerinde 50–100 bps/ay | §3.3 MC ile aynı sonuç. https://dspace.mit.edu/handle/1721.1/114876 |
| Vol hedefleme, kendi hesabı (`abd_swing_kenarlar.md` §8.2) | 2010–2026'da piyasada CAGR %12,75 (B&H %14,2), MDD −%22 (B&H −%34) | Drawdown kesici, getiri motoru değil |

### 3.5 Önerilen kural seti (kullanıcının "stratejik kümeleri" için; BIST ve ABD ortak)

**1. Risk/işlem**
- İlk 50 işlem: **%0,25**.
- 50 işlemde R-beklentisi ≥ +0,2 ise: **%0,5**.
- Onaylı trend ve yıl içi kâr yastığı ≥%10 ise: **%0,75–1**.
- 100 işlemde beklenti <0 olursa %0,25'e dönülür.

**2. Küme tanımı**
- Aynı anlatıya bağlı ya da 60 günlük getiri korelasyonu ≥0,6 olan isimler tek kümedir.
- 2026 için kümeler:
  - (a) AI donanım = yarı iletken + bellek + elektrik ekipmanı/güç/data-center altyapısı (§3.2).
  - (b) Kripto hisseleri (BTC'ye bağlı).
  - (c) Nükleer/uranyum.
  - (d) Kuantum/spekülatif.
  - (e) BIST'te bankalar (XBANK) ve holdingler (önceki lead-lag çalışmasıyla tutarlı).

**3. Küme tavanları**
- Isı ≤**%1,5**; güçlü rejimde ≤%2.
- Brüt maruziyet ≤ özsermayenin %40'ı.
- Tek hisse ≤%20–25 (Kullamägi tavanı %30).

**4. Toplam ısı (açık pozisyonlarda stop'a kadar risk toplamı)**
- Zayıf/temkin: ≤%2–3. Normal: ≤%5. Onaylı trend ve yastık varken: ≤%6 (Elder).
- Kümeli kitapta MC'ye göre %1 risk ~%1,5–2 gibi davrandığı için %6 mutlak tavan.

**5. Gap-ayarlı ısı**
- Pozisyon riski = pozisyon × max(stop mesafesi, 1,5×ATR14). Earnings penceresinde: 2× implied move.
- Earnings'e taşınan pozisyon, 2× implied move gap'i ≤1R zarar ettirecek boyuta indirilir ("earnings size").

**6. Rejim anahtarı**
- Gösterge: NDX (ABD) / XU100 (BIST) 10 GHO > 20 GHO ve ikisi yükseliyor. Ek teyit: IBD FTD veya distribution sayımı.
- Kapalıyken: yeni long yok, mevcutlar trail'de.
- İlk açılışta: pilot, toplam ısı ≤%2.
- 3–6 hafta içinde kademeli genişleme. Kullamägi'nin "nakitten marjine haftalar–aylar" kuralı.

**7. Drawdown merdiveni (zirveden)**
- −%5 → risk ×0,5. −%10 → ×0,25 ve yalnızca A+ setup. −%15 → 2 hafta işlem yok, kayıt incelemesi.
- Geri yükleme: kaybın yarısı geri gelince bir kademe yukarı.

**8. Aylık devre kesici**
- Ayın realize zararı + açık risk ≥%6 → ay sonuna kadar yeni işlem yok (Elder). Daha sıkı tercih: %4.

**9. Kâr yönetimi**
- 3–5 günde veya ≥2R'de 1/3–1/2 sat, stop başabaşa.
- Kalan pozisyon 10 GHO (hızlı) veya 20 GHO ile trail. Bu, ısıyı serbest bırakıp yeni işleme yer açar (Elder'in notu).

**10. Opsiyon ısısı**
- Opsiyonun riski = ödenen prim (tavan) ve dayanak stopundaki kayıp; ikisi de ısı tavanına sayılır.
- Spread kullanılıyorsa net debit sayılır.

**11. Ölçüm ve yeniden kalibrasyon**
- Her işlemde R, setup, küme, rejim ve earnings bayrağı kaydedilir.
- 50 işlemde bir: isabet, ortalama kazanç/kayıp, en uzun kayıp serisi (%25 isabette 200 işlemde ≥15'li seri olasılığı ~%49, `abd_kim_kazaniyor.md` §5.3), küme başına beklenti.

**Beklenti çerçevesi** (MC, rejimli, kümeli): %0,5 risk ve merdivenle medyan ~%15–20/yıl, %5 kötü MDD ~−%13. Bu, kullanıcının USD eşiği (%3,75–4 T-bill + TL taşıma fırsat maliyeti) ve TL eşiği (%36–40) için iyi rejimde aşılabilir, kötü rejimde aşılamaz bir profildir. "Yüksek ödül" (%50+) ancak iyi rejimde %1 risk, işlem sayısı ve progresif boyutla, yani −%30–40'lık kuyruğu kabul ederek gelir.

---

## 4. KİLİT İDDİALAR (doğrulayıcı için)

1. **Kullamägi kuralları:**
   - Risk "çoğunlukla %0,25–1" (blog) ve "%0,3–0,5" (FAQ). Stop günün dibi, mesafe ≤1 ADR/ATR.
   - 3–5 günde 1/3–1/2 sat, kalanı 10/20 GHO ile trail. Tek hissede gece >%30 yok.
   - 2019 isabeti %25. 2013–2019 CAGR %268 ve en büyük DD %50 (öz beyan).
   - https://qullamaggie.com/my-3-timeless-setups-that-have-made-me-tens-of-millions/ ; https://qullamaggie.com/faq/
2. **Kullamägi rejim filtresi ve 2022:**
   - Filtre: Nasdaq/SPY'de 10 GHO > 20 GHO ve ikisi yükseliyor. Zirvede ~150 mn $ long / 105 mn $ özsermaye.
   - 2022 ortasında ~45 mn $. Kendi tahmini: filtreye uysaydı kayıpların ~%90'ı önlenirdi (Schwager-Coyle 2026; CTE notu "orta/zayıf").
   - https://completetradersedge.com/kristjan-kullamagi-qullamaggie/
3. **Minervini 2021:**
   - İsabet %44–63, ortalama kazanç 2,15× ortalama kayıp, 550+ hisse. Kaynak: kendi X paylaşımı, ID'den çözülen tarih 20.01.2022.
   - Aynı yıl USIC $1M+ +%334,8.
   - https://twitter.com/markminervini/status/1484178830889738240 ; https://www.businesswire.com/news/home/20220124005241/en/2021-United-States-Investing-Championship-Winners-%E2%80%94-Minervini-Smashes-Record
4. **Brandt (5.8.2026 podcast):**
   - İşlem başı 60–70 bps risk, piramit yok, yılda 125–150 işlem. Son 12 yılda isabet ~%54. Hedef: işlem başı 20–30 bps beklenti, 100 işlemde PF 3,0.
   - Schwager: 27 yılda %58/yıl, Gain-to-Pain 2,81.
   - https://chatwithtraders.com/episode/329-peter-brandt ; https://www.panmacmillan.com/authors/jack-d-schwager/unknown-market-wizards/9780857198716
5. **Turtle limitleri:**
   - 1N = %1, stop 2N. Birim limitleri: tek piyasa 4, yakın ilişkili 6, gevşek ilişkili 10, tek yön 12.
   - Her −%10'da nominal hesap −%20.
   - https://turtletradersystem.blogspot.com/2009/01/original-turtle-trading-rules-chapter-3.html
6. **Opsiyon alıcısının dezavantajı:**
   - Coval-Shumway: S&P zero-beta ATM straddle ≈ −%3/hafta.
   - Boyer-Vorkink: çarpıklık kovaları arasında haftalık %10–50 fark; çalışma kâğıdında 7 günlük yüksek çarpıklıklı call'lar −%35,4/hafta.
   - https://econpapers.repec.org/RePEc:bla:jfinan:v:56:y:2001:i:3:p:983-1009 ; https://www.cxoadvisory.com/equity-options/sell-lottery-tickets-for-their-fun-and-your-profit
7. **Retail opsiyon zararı ve gömülü kaldıraç:**
   - Retail Kasım 2019–Haziran 2021'de ~2,1 milyar $ kaybetti (Bryzgalova et al., JF 2023).
   - Gömülü kaldıraç arttıkça riske göre getiri düşüyor (Frazzini-Pedersen; t = 8,6 hisse opsiyonu).
   - https://lbsresearch.london.edu/id/eprint/2827 ; https://econpapers.repec.org/RePEc:oup:rasset:v:12:y:2022:i:1:p:1-52.
8. **Opsiyon IV ucuzken anlamlı:**
   - Goyal-Saretto: RV−IV long/short straddle yarım-spread maliyetle bile ~%5,3/ay.
   - Gao-Xing-Zhang: duyurudan 3 gün önceki ATM straddle +%3,34 (brüt).
   - https://www.cxoadvisory.com/volatility-effects/making-money-with-options-based-on-superior-volatility-forecasts ; https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/anticipating-uncertainty-straddles-around-earnings-announcements/7B34877AD5E06304BA3C55FBA3219FDD
9. **871(m):** Notice 2026-61 (21.09.2026), non-delta-one işlemlerin muafiyetini 2028 sonuna uzattı. https://www.irs.gov/pub/irs-drop/n-26-61.pdf ; https://www.mayerbrown.com/en/insights/publications/2026/09/section-871m-phase-in-extended-two-more-years
10. **VİOP 5.11.2026:**
    - BIST30 opsiyonu: 151 serinin 36'sı işlem gördü. 665 işlem, prim 24,7 mn TL, nominal 1.188 mn TL (vadeli 51.791 mn TL'nin %2,3'ü). Nisan 2027 vadesinde işlem yok.
    - Pay opsiyonları: 2.257 seriden 289'u işlem gördü, toplam 2.036 işlem.
    - https://www.borsaistanbul.com/data/vadeli/viop_20261105.csv
11. **Kümelenme (Ken French 49 endüstri, kendi hesabım):**
    - 2026'da Chips–ElcEq korelasyonu 0,72, piyasadan arındırılmış 0,43. ElcEq beta 2,18.
    - 2024–Eylül 2026'da Chips/Hardw/ElcEq ortalama ρ 0,69, beş pozisyon ≈ 1,33 bağımsız bahis.
    - Chips'in −%4'ten kötü 17 gününde Hardw −%4,4, ElcEq −%4,0.
    - https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
12. **Vol ve drawdown kontrolü kanıtı:**
    - Cederburg et al.: vol yönetimi 103 stratejide gerçek zamanlı üstün değil; momentum istisna.
    - Kaminski-Lo: stop-loss yalnızca momentum veya rejim geçişi varken değer katar.
    - Benim MC'm: kümelenme %1 riskte %5 kötü MDD'yi −%23,9 → −%32,3 yapıyor. Merdiven −%40,6'yı −%18,9'a indiriyor, bedeli medyandan ~17 puan.
    - https://econpapers.repec.org/RePEc:eee:jfinec:v:138:y:2020:i:1:p:95-117 ; https://dspace.mit.edu/handle/1721.1/114876

---

## 5. Boşluklar ve uyarılar

- Minervini'nin sayısal boyut kuralları (%1,25–2,5, 4–6 veya 10–12 pozisyon, progresif maruziyet adımları) ikincil özetlerden geliyor; kitap metniyle birebir doğrulanmadı. "Kâr 3× risk olunca stop başabaşa" kuralı doğrulanamadı.
- David Ryan'ın Market Wizards'taki stop ve pozisyon sayısı ayrıntıları bulunamadı. CANSLIM'in genel %7–8 kuralı kullanıldı.
- Raschke ve Weinstein için denetimli performans yok. Kurallar ikincil kaynaklı.
- Kullamägi'nin 2021 beklentisi (1,16R vs 0,16R) ikincil kaynakta çelişkili.
- Goyal-Saretto'nun brüt ana rakamı okunamadı (PDF erişimi TLS hatası verdi); yalnızca maliyet sonrası ikincil rakamlar kullanıldı.
- Han-Zhou-Zhu'ya yönelik Alpha Architect replikasyon eleştirisi okunamadı (403).
- Tekil hisse fiyat verisi (Yahoo 429, Stooq bot kontrolü) alınamadı. Küme korelasyonları endüstri portföyü düzeyinde. Kripto kümesi ölçülemedi.
- Opsiyon karşılaştırması BS ile yapıldı: skew, VRP ve IV dinamiği yok. Dağılım karışımları bana ait varsayımlar. Sonuçlar yön göstergesi, kesin değer değil.
- Monte Carlo parametreleri (isabet, kazanç dağılımı, tema bozulma olasılığı, rejim kalıcılığı) kalibre edilmedi, makul varsayımlar. Asıl değer, modeller arasındaki göreli farklarda.
- VİOP opsiyon makasları bültende yok. Ekran makası önceki çalışmanın tek gözlemine dayanıyor.

Yatırım tavsiyesi değildir.
