# ABD piyasalarında swing ufkunda (birkaç gün – ~3 ay) kenarlar: yayın sonrası ve örneklem dışı kanıt

Tarih: 2026-11-06 · Hazırlayan: araştırma ajanı (ABD swing kenarları)

## 0. Yöntem ve güvenilirlik notu

- **Kendi hesaplarım (birincil veri, tekrar üretilebilir):**
  - Ken French Data Library (CRSP 202609 sürümü, veri 2026-09'a kadar): UMD, STR, günlük piyasa, 49 sektör. https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
  - Chen-Zimmermann Open Source Asset Pricing, Ekim 2026 sürümü (212 predictor, veri 2025-12'ye kadar; opsiyon bazlı sinyaller 2022-12'de bitiyor). https://huggingface.co/datasets/OpenSourceAP/CrossSection
  - AQR Time Series Momentum faktörleri (veri 2026-05'e kadar). https://www.aqr.com/Insights/Datasets/Time-Series-Momentum-Factors-Monthly
  - FRED: NASDAQ100 (yalnız fiyat, 1986 – 2026-11-05), VIXCLS, DTB3, DFEDTARU.
  - Scriptler: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/abd_swing/py/`
- **Literatür:** Rakamlar birincil kaynaktan (PDF, NBER, IDEAS) ya da arama özetinden doğrulandı. Oturumun ortak web-arama kotası rapor yazılırken doldu. Bu yüzden bazı rakamlar **[H] = hafızadan, bu oturumda doğrulanmadı** etiketi taşıyor; doğrulayıcı önce bunlara baksın.
- **Getiri birimleri:**
  - "LS" = decile long-short, maliyet öncesi ("gross"), aylık %.
  - "liq" = Chen-Zimmermann'ın piyasa değeri > NYSE 20. persentil filtresi. Mikrocap'ler hariç tutulur; yani gerçekçi işlem yapılabilir evren budur.
  - "p10" = 2010–2025 dönemi.
- **Engel oranları (hurdle):**
  - USD: 3 aylık T-bill %4,03 (FRED DTB3, 2026-11-04), Fed üst bandı %4,00 (DFEDTARU). Ortak bağlamdaki 3,75–4,00 bandıyla tutarlı.
  - TL carry'nin USD karşılığı (ortak bağlam varsayımıyla; politika faizi %36, stopaj, kurda ~%20 değer kaybı): (1+0,36×0,825)/1,20−1 ≈ **%8 – %13 USD**, devalüasyon kuyruk riskiyle birlikte.
  - Pratik sonuç: ABD'de bir stratejinin anlamlı olması için net **> %15 – %20 USD** gerekir.

---

## 1. Yönetici özeti (10 madde)

1. **Anomali hayvanat bahçesi büyük ölçüde çöktü.** Chen-Zimmermann'ın 165 "clear" sinyalinde ortalama LS getiri (kendi hesabım) şöyle geriliyor:

   | Dönem / evren | Aylık ortalama LS |
   |---|---|
   | Orijinal örneklem | %0,745 |
   | Yayın sonrası | %0,318 |
   | 2010–2025 | %0,295 |
   | 2010–2025, likit evren | **%0,201 (≈ %2,4/yıl)** |

   Likit evrende 2010 sonrası t > 1,96 olan sinyallerin payı yalnızca **%16**. Bu tablo McLean-Pontiff (−%26 örneklem dışı, −%58 yayın sonrası) ve Chen-Velikov (maliyet ve yayın sonrası net ≈ 4 bp/ay) ile uyumlu.
2. **Klasik 12-1 hisse momentumu ABD'de büyük ölçüde öldü** (Fama-French UMD):

   | Dönem | CAGR | SR | MDD |
   |---|---|---|---|
   | 1927–1993 | %7,6 | 0,55 | |
   | 1994–2009 | %3,6 | 0,28 | |
   | 2010–2026/09 | %2,6 | 0,26 | |
   | Tüm tarih | | | −%78 |

   2009'da tek yılda −%52,8. Volatiliteye göre ölçeklenmiş momentum (Barroso-Santa-Clara replikasyonum) SR'yi 2010 sonrası 0,26'dan 0,47'ye çıkarıyor. Yine de getiri ancak tek hane.
3. **Sektör momentumu hâlâ yaşıyor ve senin "stratejik kümelenme" tarzına en çok uyan kanıt bu.**
   - Kurulum: 49 VW sektör, 12-1 sıralama, top5 − bottom5.
   - 2010–2026: **LS %9,6/yıl, SR 0,56, MDD −%38.**
   - Yalnız long top-5 sektör: **%16,7/yıl**. Karşılaştırma: tüm sektörler eşit ağırlıkla %12,7, piyasa %14,2.
   - 2000–2009'da LS −%4,6 idi. Rejime bağımlı.
4. **Earnings ailesi küçüldü ama tamamen ölmedi.**
   - SUE tabanlı PEAD büyük hisselerde 2006'dan, mikrocap'lerde 2016'dan beri yok (Martineau 2022).
   - Fiyat tepkisi tabanlı sinyaller (announcement return ≈ "earnings gap"), gelir sürprizi, earnings streak ve REV6 2010 sonrası likit evrende hâlâ aylık **%0,24 – %0,43 LS**, t ≈ 1,9 – 2,6.
   - Yani "gap" fikrinin akademik çekirdeği yaşıyor. Konsantre "gap-and-go / episodic pivot" versiyonu ise hakemli kanıtı olmayan, survivorship'li bir anekdot.
5. **Opsiyon-implied kesit sinyalleri, ölçtüğüm hayatta kalanların en güçlüsü** (veri 2022 sonuna kadar):
   - SmileSlope (Yan 2011): 2010–2022 %0,89/ay, t = 6,3; likit evrende %0,65, t = 5,0; MDD −%11.
   - CPVolSpread ve dCPVolSpread de t ≈ 2,3 – 4,1.
   - Ancak düşük volatiliteli LS ürünleri bunlar (opsiyon kompoziti: %4,5/yıl, vol %3,2). Swing trader için **filtre** olarak değerli, tek başına getiri motoru değil.
6. **Takvim ve akış anomalileri bitmiş.**
   - Kısa vadeli reversal: 2010–2026 %−0,5/yıl.
   - Ay dönümü: 2010 sonrası TOM günleri 7,6 bp, diğer günler 5,5 bp. TOM-only strateji %4,6, buy-and-hold %14,2.
   - Pre-FOMC drift: 2015 sonrası yok.
   - S&P 500'e ekleme etkisi: 1990'larda %7,4, son on yılda < %1.
   - Spin-off: 2010 sonrası ≈ 0.
   - Buyback: 2002 sonrası uzun vadeli alfa yok.
   - Bunlar 20 – 40 % hedefine katkı vermez.
7. **Kaldıraçlı trend (200-DMA filtreli 2x/3x) yüksek CAGR'ın tek sistematik yolu, ama bedeli ağır.**
   - 3x Nasdaq-100, 200-DMA filtreli (kendi backtest'im, fiyat endeksi, maliyetli):

     | Dönem | CAGR | MDD |
     |---|---|---|
     | 1987–2026 | %17,0 | **−%97** |
     | 2000–2009 | **−%19,8/yıl** | |
     | 2010–2026 | %24,6 | −%55 |
     | 2016–2026 (yayın sonrası) | %30,3 | −%55 |

   - 2016–2026'da 3x buy-and-hold %30,7, MDD −%82 idi. Filtre getiri katmıyor, drawdown'ı kesiyor.
   - Uzun vadeli CRSP proxy, 3x 200-DMA: 1928–2026 %21,2, MDD −%78.
8. **Variance risk premium gerçek ama "high reward" değil.**
   - VIX ile sonraki 21 günlük gerçekleşen vol arasındaki fark: 1990–2026 ortalama +4,0 vol puanı. Günlerin %15'inde negatif, en kötü −70 puan (2020-02-20).
   - CBOE PUT endeksi: 1986–2015 %10,13 (S&P %9,85), vol %10 (S&P %15).
   - Kaldıraçlı short-vol 2018 ve 2020'de fonları sildi.
9. **Tematik/anlatı momentumu: ortalama pozitif, kuyruğu kalın.**
   - Kendi Greenwood-Shleifer-You replikasyonum: 2 yılda +%100 (hem ham hem piyasaya göre) koşan sektörlerde (n = 128, 1928–2026), sonraki 12 ay ortalama +%9,4 (medyan +%4,1, piyasaya göre +%5,0).
   - Ama 24 ay içinde **≥ %40 drawdown olasılığı %40.**
   - Temalı ETF'ler lansmandan sonraki 5 yılda riske göre ≈ −%30 (Ben-David ve ark.).
   - Şu an Hardware (24 ay +%149) ve Gold miners (+%124) bu "balon" eşiğinde.
10. **Gerçekçi beklenti.** Bireysel, ABD-dışı bir swing trader için iyi kurulmuş bir kombinasyon (kaldıraçlı trend çekirdeği + sektör/tema momentumu + earnings-event filtresi + vol yönetimi):
    - Döngü boyunca net **%15 – %25 USD CAGR** ve **−%35 / −%55 MDD**.
    - **%40+** yalnız elverişli rejim yıllarında (2020, 2023-24 gibi) mümkün; sürdürülebilir ortalama değil.
    - Monte Carlo: SR 0,8'de %24 medyan CAGR almak için vol ≈ %35 gerekir. Bu düzeyde 10 yıllık medyan MDD −%51 ve P(MDD < −%50) = %54.

---

## 2. Genel çerçeve: yayın sonrası çürüme ve replikasyon

| Çalışma | Kaynak türü | Örneklem | Bulgu |
|---|---|---|---|
| McLean & Pontiff (2016, JF) | Hakemli | 97 predictor | Getiriler örneklem dışı %26, yayın sonrası %58 daha düşük. Farkın %32'si "yayından öğrenen arbitraj". https://ivey.uwo.ca/media/3775549/pontiff.pdf |
| Hou, Xue & Zhang (2020, RFS) | Hakemli | 452 anomali | NYSE breakpoint + VW ile %65'i \|t\| ≥ 1,96'yı geçemiyor; t ≥ 2,78 eşiğinde %82. Trading-frictions kategorisinin %96'sı başarısız. https://ideas.repec.org/a/oup/rfinst/v33y2020i5p2019-2133..html |
| Jensen, Kelly & Pedersen (2023, JF) | Hakemli | 153 faktör, 93 ülke | Bayesçi çerçevede faktörlerin çoğu (≈ %82 – 85) replike oluyor; 13 temanın 10'unda > %75. Zayıf temalar seasonality, leverage, size. Uyarı: "replike olmak" ile "maliyet sonrası bireyde para kazandırmak" farklı şeyler. https://nber.org/system/files/working_papers/w28432/w28432.pdf |
| Chen & Velikov (2023, JFQA) | Hakemli | 204 anomali | Spread maliyeti + yayın sonrası + 2005 sonrası: ortalama anomali **4 bp/ay** net. En iyileri ≈ 10 bp, kombinasyonlar ≈ 20 bp. https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/zeroing-in-on-the-expected-returns-of-anomalies/945133D5A3ECEEAF466AEE91551FD225 |
| **Kendi hesabım: Chen-Zimmermann 2026.10** | Açık veri | 165 "clear" predictor | Aylık LS: in-sample %0,745 → in-sample sonrası/yayın öncesi %0,459 → yayın sonrası %0,318 → 2010–2025 %0,295 → **likit evren 2010–2025 %0,201**. Medyan: %0,64 → %0,26 → %0,21. Likit evrende 2010 sonrası t > 1,96 olanlar %16. |

**Yorum.**
- Yayınlanmış sinyalleri çeşitlendirilmiş LS portföy olarak oynamak 2010 sonrası brüt yaklaşık %2 – %5/yıl getirir.
- Bunu 15% vol'e kaldıraçlasan bile, kendi kompozit testimde (momentum + earnings + opsiyon sinyalleri, likit evren) sonuç şöyle:
  - 2010–2025 kompozit: %4,7/yıl, vol %5,9, SR 0,80, MDD −%8.
  - 2,7x kaldıraçla (2010–2022): **%13,1 excess**, MDD −%21, maliyet öncesi.
- Bireyin yüzlerce isimde LS ve short maliyeti ödediğini düşününce net ≈ %8 – %12 + T-bill kalır. **"Quant factor investing" senin hedefin için yetersiz.** Büyük getiri ya kaldıraçlı beta zamanlamasından, ya konsantre sağ-kuyruk yakalamaktan (tema liderleri, event'ler), ya da opsiyon konveksitesinden gelir.

---

## 3. Momentum ailesi

### 3.1 Özet tablo

| Sinyal | Orijinal kanıt | Yayın sonrası / 2010 sonrası (kendi hesabım) | Crash riski | Bireysel uygulanabilirlik |
|---|---|---|---|---|
| **Kesitsel 12-1** (Jegadeesh-Titman 1993) | CZ in-sample %1,28/ay (t = 4,3) | CZ Mom12m p10 %1,51 (t = 3,0), **liq %0,73 (t = 1,96)**, MDD −%54. FF UMD (VW, 30/70): 2010–26 CAGR %2,6, SR 0,26. Yıllık: 2022 +%20, 2023 −%20,5, 2024 +%18,5, 2025 −%2,2, 2026/09 +%11. | 1932 Tem-Ağu, 2009 Mar-May, 2001 Oca. FF UMD en kötü aylar: −%52,6 (1932-08), −%34,4 (2009-04). | Long-only top-decile mümkün. Short bacak (kaybedenler) pahalı ve kalabalık. |
| **Sektör momentumu** (Moskowitz-Grinblatt 1999, JF) | | Kendi 49-sektör 12-1 top5−bottom5: 1927–99 %10,0/yıl; 2000–09 **−%4,6**; **2010–26 %9,6, SR 0,56, MDD −%38**. Long top-5: 2010–26 **%16,7**, SR 0,86, MDD −%28,6. CZ IndMom (6-6, hisse düzeyi, EW): p10 %0,07, yani ölü. | 2000–09 tipi rotasyon kırılmaları. | ETF/hisse sepeti ile kolay. Ayda bir rebalans, düşük maliyet. |
| **52 haftalık zirve** (George-Hwang 2004, JF) | CZ'de "likely", in-sample %0,42 (t = 1,6) | p10 %0,38 (t = 1,07), liq %0,10 (t = 0,37) | | Sinyal zayıf. "Zirveye yakın + breakout" pratiğinin tek başına istatistiksel desteği yok. |
| **Residual momentum** (Blitz-Huij-Martens 2011) | in-sample %0,99 (t = 8,7) | p10 %0,33 (t = 1,5), liq %0,15 (t = 0,7) | Düşük | Faktör regresyonu gerekir. Kenar küçük. |
| **Intermediate momentum** (Novy-Marx 2012) | %1,26 (t = 6,1) | p10 %0,73 (t = 1,4), liq %0,16 | | Zayıf |
| **Hacimli momentum** (Lee-Swaminathan 2000) | %1,63 | p10 %2,05 (t = 3,2), liq %1,04 (t = 1,99) | MDD −%52 | Genç ve küçük isimlerde. |
| **Firma yaşı – momentum** (Zhang 2006) | %2,22 | p10 %0,96, liq %0,83 (t = 2,26) | | Genç firmalarda momentum güçlü. Tema hisseleriyle örtüşüyor. |
| **Momentum, sezonsuz** (Heston-Sadka 2008) | %1,29 | p10 %1,62 (t = 3,2), **liq %1,08 (t = 2,94)** | MDD −%40 | Kolay: 12-1 getiriden aynı takvim ayını çıkar. |
| **Return seasonality** (Heston-Sadka) | %0,82 (t = 5,9) | p10 **−%0,06** | | Öldü. |
| **Frog-in-the-pan** (Da-Gurun-Warachka 2014, RFS) | 6 aylık: sürekli bilgiyle momentum %5,94, kesikli bilgiyle −%2,07 | Yayın sonrası bağımsız test bulamadım (CZ'de yok). Yalnız Alpha Architect gibi uygulayıcı kanıt var. | | Kolay: ID = sign(PRET)×(%neg gün − %poz gün). Momentum içinde kalite filtresi olarak mantıklı. https://www3.nd.edu/~zda/Frog.pdf |
| **Time-series momentum** (Moskowitz-Ooi-Pedersen 2012, JFE) | AQR TSMOM 1985–2009: %17,4/yıl excess, SR **1,41**, MDD −%15 | **2010–2026/05: %4,5, SR 0,40, MDD −%28**. 2022: +%24,7. 2023–26: %3,3. Yalnız hisse endeksi bacağı: 2010 sonrası SR 0,09, MDD −%80. Hepsi ücret öncesi. | Trend dönüşleri (2009, 2016, 2023) | Vadeli işlemle bireysel olarak mümkün (CME micro). Ama 58 enstrümanda vol-hedefli uygulama sermaye ister. |

Daniel-Moskowitz (2016, JFE), https://www.nber.org/papers/w20439:
- Mart–Mayıs 2009'da geçmiş kaybedenler decile'ı **+%163**, kazananlar +%8.
- Temmuz–Ağustos 1932'de kaybedenler +%232, kazananlar +%32.
- Crash'ler "panik" durumlarında oluşuyor: piyasa düşüşü + yüksek vol, ardından sert ralli. Kaybeden decile'ın betası 3'ün üstüne çıkıyor.
- Dinamik (ortalama/varyans tahminli) strateji alfa ve SR'yi yaklaşık ikiye katlıyor.

Barroso & Santa-Clara (2015, JFE; https://econpapers.repec.org/RePEc:eee:jfinec:v:116:y:2015:i:1:p:111-120):
- Working paper'a göre SR 0,53'ten 0,97'ye, en kötü kayıp −%97'den −%45'e iniyor (CXO özeti).
- **Kendi replikasyonum** (hedef vol %12, 126 günlük realized vol, bir ay gecikmeli):

  | Dönem | UMD ham | UMD vol-ölçekli |
  |---|---|---|
  | 1927–2009 | %6,8, SR 0,49, MDD −%78 | **%16,7, SR 0,94, MDD −%43** |
  | 2010–2026 | %2,6, SR 0,26, MDD −%25 | **%4,7, SR 0,47, MDD −%19** |

  - Ortalama kaldıraç 1,55x.
  - Sonuç: risk yönetimi faydası yayın sonrası da sürüyor, ama mutlak getiri küçük.

Lou-Polk-Skouras (2019, JFE; https://personal.lse.ac.uk/polk/research/TugOfWar.pdf):
- Momentum kârının tamamına yakını **overnight** oluşuyor (uygulayıcı özeti: ≈ %0,95/ay overnight, %0,11 intraday).
- Diğer birçok anomali intraday'de çalışıyor ve işaretler ters. Etki büyük ve yüksek fiyatlı hisselerde daha güçlü.
- **Uygulama:** Overnight-only al-sat maliyeti kenarı yer; 2 işlem/gün olur. Pratik çıkarım: momentum isimlerine **kapanışta (MOC) gir**, gün içinde kovalamaktan kaçın.

**Momentum sonuç.**
- Hisse-düzeyi 12-1'in ABD'deki brüt LS kenarı likit evrende ≈ %0,7/ay. Konsantre long-only versiyonda da piyasa üstü getiri ≈ %3 – %6/yıl.
- Swing trader için asıl değer, **sektör/tema düzeyinde** momentum ve onun üstüne **vol-yönetimi**:
  - Panik-ralli rejimlerinde (VIX yüksek + piyasa son 12 ay negatif) momentum pozisyonunu küçült.
  - 2009 tipi tersine dönüşte kaybedenlerin alfa betası patlar.

---

## 4. Earnings ailesi

| Sinyal | Orijinal | 2010 sonrası (CZ, kendi hesabım) | Not |
|---|---|---|---|
| **SUE-PEAD** (Foster-Olsen-Shevlin 1984; Bernard-Thomas 1989) | in-sample %1,16/ay | p10 %0,20 (t = 1,6), **liq %0,04 (t = 0,3)** | **Martineau (2022, CFR)**: analist sürprizleri büyük (mikrocap dışı) hisselerde 2006'dan, mikrocap'lerde 2016'dan beri 60 günlük getiriyi öngörmüyor. Random-walk sürprizinde mikrocap drift'i ≤ 5 gün. https://cfr.ivo-welch.info/published/papers/martineau2021rest.pdf. Subrahmanyam (2025, WP), 2001–2024: tüm hisseler t = 2,18, mikrocap hariç **t = 1,43** (UCLA Anderson Review özeti). |
| **Announcement return / EAR** (Chan-Jegadeesh-Lakonishok 1996; Brandt ve ark. 2008) | %1,14 (t = 12,5) | **p10 %0,59 (t = 4,1)**, liq %0,24 (t = 2,1). MDD −%13,8, SR 1,03 | Fiyat tepkisi sürprizden daha iyi bilgi taşıyor. "Gap" fikrinin akademik çekirdeği bu. |
| **Revenue surprise** (Jegadeesh-Livnat 2006) | %0,73 | p10 %0,43 (t = 3,2), liq %0,26 (t = 1,9) | SUE + SURGE birlikte daha güçlü (orijinal). |
| **Earnings streak** (Loh-Warachka 2012) | %1,09 | **p10 %0,62 (t = 4,8)**, liq %0,37 (t = 2,6). MDD −%9 | Art arda pozitif sürprizler. Hayatta kalanların en iyilerinden. |
| **Analyst revision** (Hawkins ve ark. 1984) | %0,96 | p10 %0,15, liq %0,14 | Basit 1 aylık revizyon öldü. |
| **REV6** (CJL 1996, 6 aylık revizyon) | %1,13 | p10 %0,61 (t = 3,0), liq %0,43 (t = 2,25) | Yaşıyor. |
| **Recommendation change** (Jegadeesh ve ark. 2004) | %1,03 | p10 %0,26 (t = 2,3), liq %0,13 | Zayıf. |
| **Earnings announcement premium** (Frazzini-Lamont 2007; Barber ve ark. 2013, JFE) | Duyuru beklenen hisseleri al, beklenmeyenleri sat: > 60 bp/ay (F-L, yıllık %7 – %18). Global: 66,8 bp/ay (%8/yıl). | 2010 sonrası bağımsız güncel test bulamadım. | Aylık ≈ %100 turnover, maliyet yüksek. Earnings öncesi long tutmanın neden pozitif beklentili olduğunu açıklar. https://www.nber.org/system/files/working_papers/w13090/w13090.pdf |
| **Pre-earnings run-up** (Aboody-Lehavy-Trueman 2010) [H] | Geçmiş 12 ayın büyük kazananları duyuru öncesi ≈ 5 günde pozitif anormal getiri, duyuru sonrası kısmi geri dönüş [H] | Doğrulanmadı | Swing trader için: güçlü momentum isminde duyuruya 3–5 gün kala girip duyurudan önce çıkmak test edilmeye değer. |

### 4.1 "Gap-and-go / episodic pivot" (EP)

- **Hakemli doğrudan kanıt:** Bulamadım. En yakınları şunlar:
  - Announcement-return drift (yukarıda).
  - Anormal hacim primi: Gervais-Kaniel-Mingelgrin 2001 [H]; Garfinkel-Sokobin 2006, JAR, https://www.biz.uiowa.edu/faculty/jgarfinkel/pubs/drift_JAR.pdf; Gerard 2012, FAJ, Avrupa 1997–2010: yüksek anormal hacimli earnings hisseleri 90 güne kadar daha iyi.
- **Anekdot:** Qullamaggie (Kristjan Kullamägi), Minervini, Oliver Kell ve US Investing Championship kazananları. Hiçbiri denetlenmiş track record değil [H]. Klasik survivorship: aynı setup'ı kaybedenler yarışmayı kaybeder ya da yayın yapmaz.
- **Kantitatif tahmin:** Likit evrende EAR LS yaklaşık %0,24/ay. Yani kenar, çeşitlendirilmiş bir LS portföyde yıllık birkaç yüzde. Konsantre EP trader'ın yüksek getirisi kenardan değil, **sağ kuyruk konveksitesinden** gelir: dar stop (gap-günü düşüğü) ve trailing exit ile, düşük isabet oranı (%30 – %40) ve 3R – 10R kazananlar.
- **Önerilen test protokolü** (VİOP lead-lag çalışmasındaki disiplinle):
  - Olay: earnings sonrası açılış gap'i ≥ +%7, hacim ≥ 3x 50 günlük ortalama, kapanış günün üst %30'unda. Opsiyonel: SUE > 0 ve revenue surprise > 0.
  - Giriş: gün-1 kapanışı veya gün-2'de gün-1 high'ı kırılınca.
  - Stop: gün-1 low.
  - Çıkış: 10/20 EMA trailing veya 20/40/60 gün.
  - Ölçüm: işlem başına R, isabet oranı, beklenti, yıl yıl dağılım. Eşleştirilmiş kontrol: aynı gap'te hacimsiz olaylar.
  - Örneklem: 2012–2019 in-sample, 2020–2026 out-of-sample. Maliyet: spread + 10 bp slippage.
  - Kabul kriteri: OOS'ta işlem başına beklenti > +0,3R ve yıllık işlem sayısı ≥ 40.

### 4.2 Earnings IV crush ve straddle fiyatlaması

- **Gao, Xing & Zhang (2018, JFQA), "Anticipating Uncertainty: Straddles around Earnings Announcements" [H]:** Duyurudan birkaç gün önce alınıp duyurudan hemen önce kapatılan straddle'lar, implied vol'ün duyuruya doğru artması sayesinde anlamlı pozitif getiri veriyor. Kesin rakamı doğrulayamadım.
- **Dubinsky, Johannes, Kaeck & Seeger (2019, RFS) [H]:** Opsiyon fiyatları earnings jump riskini ayrıca fiyatlıyor. Implied earnings-move ortalamada gerçekleşenle uyumlu ya da biraz yüksek. Bu yüzden duyuru boyunca long straddle ortalamada hafif negatif, short straddle hafif pozitif ama kuyruk riskli.
- **Swing trader için çıkarım:**
  - Earnings'i yön için oynayacaksan, ham opsiyon değil **dikey spread** kullan (IV crush'ı nötrler).
  - Duyuru boyunca naked long opsiyon ortalamada "crush vergisi" öder.
  - Duyuru öncesi IV run-up'ı ayrı ve kısa bir trade.

---

## 5. Kısa vadeli reversal, overnight ve takvim etkileri

| Etki | Orijinal | 2010 sonrası (kendi hesabım) | Karar |
|---|---|---|---|
| **1 aylık reversal** (Jegadeesh 1990) | FF STR 1927–93 %10,2/yıl, SR 0,89 | 1994–2009 %3,2; **2010–26 %−0,5, SR 0,01; 2021–26 %−5,6/yıl**, MDD −%40. CZ STreversal liq %0,08. | Öldü. |
| **Reversal × stres** (Nagel 2012, RFS "Evaporating liquidity") | Reversal getirisi = likidite sağlama primi, VIX ile artıyor | Önceki ay sonu VIX > 25 olan aylarda STR 2010–26 **+%0,55/ay** (n = 29), diğerlerinde −%0,08. 1990–2009: +%0,76 ve +%0,09. | Yalnız panik dönemlerinde (VIX > 25) aşırı satılmış kaliteli isimleri alan, kriz-koşullu swing taktiği olarak yaşıyor. |
| **Overnight vs intraday** (Lou-Polk-Skouras 2019) | Momentum overnight, diğerleri intraday | Uygulama maliyetli | Bkz. §3 |
| **Pre-FOMC drift** (Lucca-Moench 2015, JF) | 1994–2011: S&P 500 duyurudan önceki 24 saatte ortalama **+49 bp** (t > 4,5); yıllık toplam getirinin önemli bölümü. https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf | Kurov-Wolfe-Gilbert (2021, FRL): **2015 sonrası esasen yok** (örneklem Aralık 2019'a kadar). https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html | Öldü. |
| **Ay dönümü (TOM)** (Ariel 1987; Lakonishok-Smidt 1988; Etula ve ark. 2020, RFS) | Son gün + ilk 3 gün | Kendi CRSP VW hesabım: 1927–87 TOM 16,3 bp/gün, diğer 1,2 (getirinin %75'i günlerin %18'inde). 1988–2009: 12,0 ve 2,5. **2010–26: 7,6 ve 5,5** (getirinin %24'ü günlerin %19'unda). TOM-only CAGR %4,6, buy-and-hold %14,2. | Öldü. Choi-Hong-Lou ancak EW bazında kalıntı buluyor. |
| **Bayram öncesi** (Ariel 1990) | | 1927–87 33,7 bp; 1988–2009 14,2 bp; **2010–26 13,0 bp** (n = 156; ortalama gün 5,9 bp). Toplam katkı ≈ %0,7/yıl. | Önemsiz. |

---

## 6. Event-driven ve akış sinyalleri

| Sinyal | Orijinal kanıt | Güncel / yayın sonrası | Uygulama ve risk |
|---|---|---|---|
| **İçeriden alım: opportunistic insiders** (Cohen-Malloy-Pomorski 2012, JF) | Rutin olmayan işlemlerden kurulan VW portföy **82 bp/ay anormal**; rutin işlemler ≈ 0 (1986–2007). https://www.nber.org/digest/apr11/decoding-inside-information | 2016 sonrası bağımsız test bulamadım. Lakonishok-Lee 2001: etki küçük firmalarda yoğun [H]. | SEC Form 4 iki iş günü içinde EDGAR'da ücretsiz. Rutin ayrımı: son 3 yılda aynı takvim ayında işlem yapanlar rutindir. 10b5-1 planlı işlemlerin bilgi değeri ≈ 0. |
| **Küme alımları** (Alldredge-Blank 2019, J. Financial Research) | 1986–2016: kümelenmiş alımlardan sonraki ay > %2 anormal; bir özete göre 21 günde %3,8 (tekil alımlarda %2) | Yayın sonrası test yok | En temiz swing-ufku event sinyallerinden. Kapasite küçük (small/mid cap). Kendi event study'nle doğrula. |
| **13D aktivizm** (Brav-Jiang-Partnoy-Thomas 2008, JF) | [−20, +20] gün ≈ %7 anormal, sonraki yılda geri dönüş yok. Fiyat ve hacim artışı dosyalamadan 1–10 gün önce başlıyor. | SEC, 13D süresini 10 iş gününden 5 iş gününe indirdi (2023 kuralı, 2024'te yürürlük) [H]. Böylece dosyalama öncesi sızıntı kısalır, dosyalama günü tepkisi artabilir. Dosyalama **sonrası** alınabilir kısım muhtemelen birkaç yüzde [H]. | EDGAR'dan izlenebilir. Gün-0 açılışında girmek gerekir. |
| **Spin-off** (Cusatis-Miles-Woolridge 1993) | in-sample %0,39/ay (VW) | CZ p10 **−%0,06**, liq −%0,04, MDD −%66. CSD ETF'i 2016 endeks değişikliğinden sonra karışık. | Sistematik kenar yok. Tekil analizle hikâye trade'i olabilir. |
| **S&P 500'e ekleme** (Shleifer 1986) | Greenwood-Sammon (2025, JF): ekleme anormal getirisi 1980'ler %3,4 → 1990'lar **%7,4** → son on yıl **< %1**. Çıkarma: 1990'lar −%16,1 → 2010–20 −%0,6. Neden: MidCap'ten göç (%50 → > %70). https://www.nber.org/system/files/working_papers/w30748/w30748.pdf | | Öldü. Kalıntı: S&P 400/600 → 500 geçişinde değil, "hiç endekste olmayan" büyük isim ilk girişinde (ör. yeni IPO dev). Tekil event olarak izlenir. |
| **Buyback duyurusu** (Ikenberry-Lakonishok-Vermaelen 1995) | 4 yılda ≈ %12 anormal [H] | Fu-Huang (Management Science): uzun vadeli anormal getiri 2002 sonrası olaylarda yok. CZ ShareRepurchase p10 %0,45 (t = 2,6, EW), liq %0,18 (t = 1,65). | Swing ufkunda değil, yıllar ufkunda. Zayıf. |
| **Short interest / days-to-cover** (Dechow ve ark. 2001; Hong ve ark. 2016) | DTC LS 1988–2012 **%1,19/ay** EW (short ratio %0,71). VW daha zayıf. https://www.nber.org/papers/w21166.pdf | CZ ShortInterest p10 %0,95 (t = 3,2) **ama liq %0,27 (t = 0,9)**. IO_ShortInterest p10 %6,8/ay, MDD **−%90**: tamamen illikit, ödünç alınamayan isimler. | Kenar short bacakta ve küçük hisselerde: borrow fee, recall, squeeze riski. Bireysel uygulanabilirlik düşük. **Long filtre** olarak kullan: yüksek DTC'li isimleri long tarafında tutma. |
| **Short squeeze** | GME Ocak 2021 (≈ $17 → intraday $483) [H] | Sistematik öngörü kanıtı yok. Squeeze'ler nadir, pozitif-çarpık ve öngörülmesi zor. | Opsiyonla küçük konveks bahis dışında strateji değil. |
| **Retail attention / Robinhood herding** (Barber-Huang-Odean-Schwarz 2022, JF) | En çok alınan hisselerde 20 günlük anormal getiri **−%4,7**, aşırı herding'de **−%19,6**. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3715077 | | "Fade" kenarı gerçek ama short'u pahalı ve squeeze'e açık. Uygulama: put spread ya da en azından bu isimlerde long'dan kaçınmak. |
| **IPO'lar** | Ritter 1991: uzun vadeli zayıflık. CZ IndIPO p10 %0,46 (t = 2,1), liq %0,45 (t = 1,9). Lockup bitişi ≈ −%1 / −%3 (Field-Hanka 2001) [H]. Quiet-period bitişi ≈ +%4 (Bradley-Jordan-Ritter 2003; sonradan küçüldü) [H]. | | İlk gün primi bireye tahsis edilmez. Swing için: IPO base breakout (O'Neil) anekdot; lockup öncesi short/put event'i küçük kenarlı. |

---

## 7. Opsiyon tabanlı kenarlar

### 7.1 Variance risk premium (VRP)

- **Kendi hesabım** (VIX ve CRSP VW ile sonraki 21 günlük realized vol, 1990–2026):
  - VIX ortalaması 19,4, gerçekleşen 15,4: **+4,0 vol puanı** fark. 2010 sonrası +3,2.
  - Fark günlerin %15 – %17'sinde negatif. En kötü −69,9 puan (2020-02-20'de satılan 1 aylık vol).
  - Varyans biriminde medyan +1,2, en kötü −78,5: tipik kazancın ~65 katı tek olay kaybı.
- **CBOE PUT endeksi** (Bondarenko 2016, Cboe sponsorlu; bağımsız değil):
  - 1986–2015: %10,13/yıl (S&P %9,85), vol %10,2 (S&P %15,3).
  - 2006–2015 MDD: −%32,7 (S&P −%50,9).
  - Ağustos 2023'e kadar: %9,40 (S&P %9,91).
  - https://www.cboe.com/insights/posts/generating-income-and-managing-risk-cash-secured-put-writing-in-a-low-equity-return-environment
- **Kaldıraçlı short-vol çöküşleri [H]:** 5 Şubat 2018 "Volmageddon" (XIV ≈ −%90+ ve kapandı; LJM ve benzeri fonlar ağır kayıp), Mart 2020 (Malachite vb.).
- **Sonuç:** VRP ≈ hisse benzeri getiri ve daha düşük vol verir; **%20 – %40 hedefi ancak kaldıraçla mümkün, o da ölümcül kuyruk demek.** Swing trader için doğru kullanım: teminat üzerinde muhafazakâr kısmi put satışı ya da cash-secured put ile **giriş fiyatı almak**. Getiri motoru değil.

### 7.2 Dealer gamma, 0DTE, kaldıraçlı ETF rebalansı

- **0DTE:** Beckmeyer-Branger-Gayda (2023, SSRN 4404704): perakende 0DTE SPX'te Şubat 2021 – Şubat 2023 arasında günde ortalama $184 bin, günlük vadeler başladıktan (Mayıs 2022) sonra **$358 bin/gün** kaybetti. Kaybın büyük bölümü işlem maliyeti. https://www.bloomberg.com/news/articles/2023-04-21/day-traders-lose-358-000-per-day-gambling-on-zero-day-options
- **Dealer gamma:**
  - Baltussen-Da-Lammers-Martens (2021, JFE): "intraday momentum", son 30 dakika, negatif gamma hedge akışına bağlanıyor [H].
  - Dim-Eraker-Vilkov (2024, WP): 0DTE kaynaklı dealer gamma çoğunlukla pozitif, piyasayı istikrarsızlaştırdığına kanıt yok [H].
  - Swing ufkunda yön kanıtı yok. Negatif gamma rejimi yalnız **vol** öngörür. GEX gibi uygulayıcı metrikleri pozisyon boyutu ayarı için kullan, yön sinyali olarak değil.
- **Kaldıraçlı ETF rebalansı** (Cheng-Madhavan 2009 [H]): akış kapanışa yakın ve gün içi. Swing ile ilgisiz.

### 7.3 Opsiyon-implied kesit sinyalleri (hayatta kalanların en güçlüsü)

| Sinyal | Orijinal | 2010–2022 (CZ, kendi hesabım) |
|---|---|---|
| **SmileSlope** (Yan 2011; OTM put − call IV eğimi) | in-sample %1,83/ay (t = 8,2) | **%0,89 (t = 6,3); liq %0,65 (t = 5,0); MDD −%11; SR 1,73** |
| **CPVolSpread** (Bali-Hovakimian 2009; Cremers-Weinbaum ailesi) | %0,98 | %0,47 (t = 3,3); liq %0,37 (t = 2,95) |
| **dCPVolSpread** (An-Ang-Bali-Cakici 2014) | %1,36 | %0,58 (t = 4,1); liq %0,32 (t = 2,3) |
| **skew1** (Xing-Zhang-Zhao 2010, JFQA) | in-sample %0,63 (t = 3,1). Orijinal: en dik smirk'e sahip hisseler riske göre yıllık ≈ %10,9 düşük [H] | %0,21 (t = 1,45); liq %0,20 (t = 1,4). Zayıfladı. |
| **Put-call parity sapması** (Cremers-Weinbaum 2010, JFQA) | Görece pahalı call'u olan hisseler pahalı put'lulardan haftada ≈ 50 bp fazla getiri; 1996–2005 içinde azalan [H] | CZ CPVolSpread benzer: yukarıda |

- **Opsiyon kompoziti (likit):** %4,5/yıl, vol %3,2, SR 1,39, MDD −%2,6. Düşük vollü, düşük getirili ama tutarlı.
- **Uygulama:**
  - IBKR'den hisse başına put/call IV çekilebilir. 500 isimde haftalık tarama bireysel olarak yapılabilir.
  - **Filtre olarak kullan:** long adayların put skew'i dik değilse, call IV put IV'den yüksekse (bilgili alım) ve IV değişimi call lehineyse tut. Tersini ele.
  - Not: OptionMetrics 2024 metodoloji revizyonu nedeniyle CZ verisi 2022'de kesik. Güncel performans doğrulanmadı.

---

## 8. Kaldıraçlı trend ve volatilite hedefleme

### 8.1 200-DMA filtreli 2x/3x (Gayed-Bilello 2016, "Leverage for the Long Run")

Orijinal makale SSRN'de (2741701 [H]); SSRN erişimimi engelledi (403), rakamlarını doğrulayamadım. Bu yüzden **kendim replike ettim.**

- **Kurallar:**
  - Kapanış > 200-DMA ise ertesi gün L-kat pozisyon, değilse T-bill.
  - Kaldıraç maliyeti: (L−1)×(RF + %0,5), ETF gideri %0,85 – %0,90, günlük rebalans (vol decay dahil), geçiş başına %0,10.
  - Yılda ≈ 5,5 (CRSP) – 7 (NDX) geçiş.
- **Veri:** CRSP VW toplam getiri (S&P proxy) ve FRED NASDAQ100 (yalnız fiyat; temettü yok, yani CAGR'lar ≈ L×%0,7 eksik).

| Strateji | 1928/1987 – 2026 | 2000–2009 | 2010–2026 | 2016–2026 (yayın sonrası) | 2022 yılı |
|---|---|---|---|---|---|
| CRSP 1x BH | %9,6, MDD −%84 | −%0,4 | %14,2, MDD −%34 | %15,0 | −%20 |
| CRSP 3x BH | %11,1, MDD −%99,9 | −%21,0 | %29,1, MDD −%77 | %28,4 | −%60 |
| **CRSP 3x 200-DMA** | **%21,2, MDD −%78** | −%4,1 | %19,5, MDD −%55 | %24,6, MDD −%49 | −%35 |
| CRSP 2x 200-DMA | %16,0, MDD −%60 | −%1,0 | %14,6, MDD −%41 | %18,1 | −%25 |
| NDX 1x BH | %14,1, MDD −%83 | −%6,7 | %17,2, MDD −%36 | %17,6 | −%33 |
| NDX 3x BH | %11,2, MDD −%100 | **−%48,8/yıl** | %34,1, MDD −%82 | %30,7 | −%79 |
| **NDX 3x 200-DMA** | **%17,0, MDD −%97,2** | **−%19,8/yıl** | **%24,6, MDD −%55** | **%30,3, MDD −%55** | −%45 |
| NDX 2x 200-DMA | %15,7, MDD −%87 | −%9,7 | %19,1, MDD −%40 | %23,4, MDD −%40 | −%33 |

**Yorum.**
1. Filtre, uzun dönemde kaldıraçlı buy-and-hold'u yıkımdan kurtarıyor: CRSP 3x'te CAGR %11'den %21'e, MDD −%99,9'dan −%78'e.
2. Ama 2010 sonrası boğada **getiri kesiyor** (NDX 3x: %34 → %24,6). Asıl katkı MDD'yi −%82'den −%55'e indirmek.
3. **Rejim riski çok büyük.** 2000–2009'da filtreli 3x NDX bile yıllık −%19,8 ve MDD −%97: whipsaw + 2000-02 düşüşü. Bu, tek bir stratejiye 10 yıl kilitlenmenin ne demek olduğunu gösteriyor.
4. **Şu anki durum:**
   - NDX 2026-11-05'te 26.630. Bu, 200-DMA'nın (27.977) **%4,8 altı** ve 6 Ekim 2026 zirvesinin (31.225) **−%14,7 altı**.
   - 5 Kasım'da tek gün **−%6,4** (2020'den beri 4. en büyük günlük düşüş; nedenini doğrulayamadım).
   - Kural şu an "nakit" diyor. Aynı gün 3x pozisyon ≈ −%19 olurdu: kaldıraçlı stratejinin gap riskinin canlı örneği.
5. **Bireysel uygulama:**
   - TQQQ/UPRO ABD domisilli. ABD dışı kişiler için $60 bin üstü ABD varlıklarında **ABD veraset vergisi riski** var [H, vergi danışmanıyla doğrula].
   - Alternatif: CME micro vadeli (MNQ/MES). Finansman fiyata gömülü, ETF gideri yok, kaldıraç esnek.

### 8.2 Volatilite hedefleme

- **Kendi hesabım** (piyasa, hedef %15 vol, 21 günlük RV, 2x tavan):

  | Dönem | Strateji | Buy-and-hold |
  |---|---|---|
  | 1928–2026 | CAGR %10,4, MDD −%66,7 | %9,6, −%84 |
  | 2010–2026 | **%12,75**, MDD −%22 | **%14,2**, −%34 |

- Cederburg-O'Doherty-Wang-Yan (2020, JFE) [H]: Moreira-Muir (2017, JF) tipi vol-yönetimi örneklem dışında sistematik olarak üstün değil. Benim bulgum da öyle: **getiri motoru değil, drawdown kesici.**
- **İstisna: momentum.** Vol-ölçekli UMD, 2010 sonrası da SR'yi yaklaşık ikiye katlıyor (§3).

---

## 9. Sektör/tema rotasyonu, anlatı momentumu (AI, nükleer, kuantum, kripto bağlantılı) ve IPO'lar

**Kanıt 1: sektör momentumu** (§3.1). Long top-5 sektör 2010–2026 %16,7/yıl, EW-tüm sektörler %12,7. Rejime bağlı: 2000–09'da LS negatif.

**Kanıt 2: balon / koşu sonrası davranış.** Greenwood-Shleifer-You (2019, JFE, "Bubbles for Fama") [H] bulgusu: büyük koşular düşük **ortalama** getiri öngörmüyor ama crash olasılığını belirgin artırıyor. Koşunun özellikleri crash'i kısmen öngörüyor: vol artışı, turnover, yeni hisse ihracı, yaşlı firmalardan çok genç firmaların koşması, ivmelenen fiyat yolu.

Kendi replikasyonum (49 FF sektörü, 24 aylık ham ve piyasaya göre getiri > +%100, 24 aylık soğuma, 1928–2026):

| Ölçüt | Değer |
|---|---|
| Olay sayısı | 130 (128'inde ileri veri var) |
| Sonraki 12 ay ortalama / medyan | +%9,4 / +%4,1 |
| Sonraki 12 ay, piyasaya göre | +%5,0 (isabet %54) |
| Sonraki 24 ay ortalama | +%18,8 |
| **24 ay içinde ≥ %40 drawdown olasılığı** | **%40** (1990 sonrası %36, n = 45) |
| Medyan MDD (24 ay) | −%34 |

Örnekler: Hardw 1999-11 → 24 ay −%51, MDD −%81. Chips 1999-12 → −%53, MDD −%73. Coal 2022-02 → +%119. Gold 2002-10 → +%97.

**Kanıt 3: temalı ürünler.** Ben-David, Franzoni, Kim, Moussawi (2023, RFS): uzmanlaşmış/temalı ETF'ler ilk 5 yılda riske göre **≈ −%30** kaybediyor. Neden ücret değil, lansman anındaki aşırı değerleme; sağlayıcılar ekstrapolatif talebe ürün çıkarıyor. https://www.nber.org/papers/w28369 → **Tema ETF'i lansmanda alınmaz.** Kenar, tema erken iken likit liderlerde ve sektör momentumunun ilk 6–12 ayında.

**2022–2026 liderlik** (FF 49 VW, kendi hesabım; 2026 Eylül'e kadar):

| Yıl | Liderler |
|---|---|
| 2022 | Coal +%100, Oil +%65 |
| 2023 | Autos +%72, Construction +%70, Chips +%64, Software +%60 |
| 2024 | Chips +%55, Fun +%49, Autos +%49 |
| 2025 | **Gold +%184**, Steel +%57, Aero +%44 |
| 2026 YTD | **Hardware +%84**, Oil +%43, Machinery +%42, Chips +%36 |

- Son 24 ay: Hardware +%149, Gold +%124, Chips +%91, Electrical Equipment +%78.
- Hardware (2026-05) ve Gold (2025-09) GSY "balon" eşiğini geçti. Tarihsel baz oranla 24 ay içinde %36 – %40 crash olasılığı. Bu, "çık" değil, **trailing stop ve pozisyon küçültme** sinyali.
- **Kuantum, nükleer/SMR ve kripto bağlantılı hisseler (2024–2026) [H]:**
  - Kuantum isimleri Kasım–Aralık 2024'te yüzlerce yüzde koştu, Ocak 2025'te tek günde ≈ −%40 düştü.
  - Nükleer/SMR ve kripto-hazine şirketleri benzer "anlatı" döngüleri yaşadı.
  - Spesifik rakamları bu oturumda doğrulayamadım. Yapısal ders: anlatı hisselerinde **sağ kuyruk büyük, sol kuyruk da büyük**. Bunlar ancak kurala bağlı giriş-çıkışla oynanır (sektör/tema momentumu + vol stop).

**Genel kanıt [H]:** Bessembinder (2018, JFE): 1926–2016'da ABD hisselerinin ≈ %4'ü net servet yaratımının tamamını üretti. Yani getiri dağılımı aşırı çarpık. Konsantre momentum/tema trader'ının mantıklı tarafı bu; ama aynı çarpıklık "ortalama hisse T-bill'i yenemez" demek.

---

## 10. ABD'de kazananlar gerçekte nasıl kazanıyor (bulguların sentezi)

1. **Yapısal kazananlar (bireyin kopyalayamayacağı):**
   - Market maker'lar ve HFT (spread + rebate).
   - 0DTE/opsiyon akışının karşı tarafı: perakende 0DTE'de günde $358 bin kaybediyor.
   - Endeks ve akış bilgisine erken erişen kurumlar.
2. **Sistematik prim toplayıcılar:**
   - VRP satıcıları: risk yönetimiyle hisse benzeri getiri.
   - CTA/trend: 2022'de +%25. 2010 sonrası SR ≈ 0,4.
   - Factor fonları: 2010 sonrası brüt %2 – %5 LS.
3. **Kaldıraçlı beta zamanlayıcıları:** 2010–2026 ABD boğasında 2x – 3x endeks + trend filtresi %19 – %30 CAGR verdi. Bunun büyük kısmı **rejim şansı** (2000–09'da aynı kural −%20/yıl).
4. **Konsantre momentum/event trader'ları** (Minervini, Qullamaggie, USIC kazananları):
   - Kanıt anekdot ve denetimsiz. Survivorship ağır.
   - Mekanizma tutarlı: sektör liderliği, earnings tepkisi (EAR), yüksek hacimli kırılım, dar stop, sağ-kuyruk konveksitesi.
   - Ölçülebilir akademik çekirdek (EAR, revenue surprise, streak, sektör momentumu) küçük ama gerçek. Gerisi uygulama, pozisyon boyutu ve rejim.
5. **Baz oranlar (bireysel aktif trader) [H]:**
   - Tayvan gün içi trader'larının < %1'i öngörülebilir biçimde net kârlı (Barber-Lee-Liu-Odean).
   - Brezilya'da 300+ gün devam eden gün içi trader'ların %97'si zarar etti (Chague-De-Losso-Giovannetti 2019).
   - Swing ufku için benzer büyük-örneklem kanıtı yok; ama yüksek turnover'lı hesapların piyasanın altında kaldığı bulgusu tutarlı (Barber-Odean 2000).

---

## 11. Getiri, risk ve drawdown matematiği (Monte Carlo, normal dağılım, 10 yıl, 2000 yol)

| SR | Vol | Beklenen excess | Medyan CAGR (excess) | Medyan MDD | P(MDD < −%50) | P(10 yıl CAGR < 0) |
|---|---|---|---|---|---|---|
| 0,5 | %25 | %12,5 | %9,4 | −%46 | %39 | %12 |
| 0,5 | %35 | %17,5 | %11,5 | −%59 | %78 | %15 |
| 0,8 | %25 | %20,0 | %18,3 | −%40 | %17 | %2 |
| 0,8 | %35 | %28,0 | %24,4 | −%51 | %54 | %2 |
| 0,8 | %50 | %40,0 | %32,0 | −%66 | %93 | %4 |
| 1,0 | %25 | %25,0 | %24,1 | −%36 | %9 | %0 |
| 1,0 | %35 | %35,0 | %33,6 | −%47 | %40 | %0 |

- Gerçek getiriler kalın kuyruklu olduğu için drawdown'lar bundan kötü olur.
- **Çıkarım:** Net SR 0,6 – 0,8 gerçekçi üst sınır; bunu tutarlı yakalamak bile istisnai. Bu SR'lerde %20 – %30 hedefi %30 – %40 vol ve −%45 / −%60 drawdown kabulü demek. **%40+ sürekli hedef matematiksel olarak ya SR > 1 (kanıtlanmamış) ya da yıkım riski (P(MDD < −%50) > %90) ister.**

---

## 12. Sonuç: > %20 – %40 USD arayan swing trader için sıralı liste

Notlar: Beklentiler net, USD, bireysel, ABD dışı yatırımcı için. Aralık "kötü – iyi uygulama". T-bill (%4) dahil.

| Sıra | Yaklaşım | Kanıt kalitesi | Gerçekçi net CAGR | Beklenen MDD (döngü) | Kapasite | Uygulama |
|---|---|---|---|---|---|---|
| **1** | **Sektör/tema momentumu kümesi.** 49 sektör veya ~30 tema sepeti; 12-1 + 6 aylık sıralama; top 3–5 küme; aylık rebalans; vol-ölçekli boyut; panik-ralli rejiminde azaltma. Senin "stratejik kümelenme" tarzının sistematik versiyonu. | Orta-yüksek: 2010–26 long top-5 %16,7 brüt, LS SR 0,56 | **%13 – %20**; 1,3 – 1,5x kaldıraçla %17 – %25 | −%30 / −%45 | Yüksek | ETF ve liderler; kolay |
| **2** | **Kaldıraçlı trend çekirdeği.** 2x NDX/SPX (MNQ/MES micro vadeli), 200-DMA (+ opsiyonel %2 bant / 2 gün teyit) | Orta: uzun tarih var ama rejime aşırı bağımlı; 2016 sonrası kanıt güçlü, 2000–09 felaket | **%12 – %22** | −%40 / −%60 (3x'te −%55 / −%97) | Çok yüksek | Kolay; disiplin ve gap riski |
| **3** | **Earnings-event swing.** EAR/gap + anormal hacim + revenue surprise + streak (+ REV6); 5–60 gün tutma; dar stop; küme içi liderlerde | Düşük-orta: çeşitlendirilmiş LS çekirdeği yaşıyor (%0,24 – %0,6/ay); konsantre EP'nin hakemli kanıtı yok | **−%10 ile +%40 arası, çok geniş**; ancak kendi OOS testi geçerse | −%25 / −%40 | Orta (mid/small) | Veri + event study şart (§4.1 protokolü) |
| **4** | **Momentum için vol-yönetimi overlay** (Barroso-Santa-Clara / Daniel-Moskowitz) | Yüksek | Getiriye +%1 – %3; SR'ye +0,2 | MDD'yi ≈ %25 – %45 azaltır | | Kolay |
| **5** | **Opsiyon-implied filtreler** (SmileSlope, CPVolSpread, dCPVol) ve **short-interest/DTC filtresi** (long tarafında yüksek DTC'den kaçın) | Yüksek (2022'ye kadar) | Seçime +%2 – %4 | | Orta | IV verisi (IBKR) |
| **6** | **İnsider küme alımları** (opportunistic, Form 4) | Orta (2016'ya kadar) | Tek başına %5 – %15 brüt, küçük kapasite | −%30 | Düşük | EDGAR ücretsiz |
| **7** | **Konveksite:** tema/event bahislerinde hisse yerine call spread; earnings'te dikey spread | Teorik + IV crush bulguları | Kenar değil, risk şekillendirme | Prim kaybı sınırlı | | Orta |
| **8** | **Kriz-koşullu reversal** (VIX > 25'te aşırı satılmış kalite) | Orta (Nagel 2012; 2010 sonrası +%0,55/ay) | Fırsatçı; yılda birkaç ay | Kriz derinleşirse | | Kolay |
| **9** | **VRP:** cash-secured put ile giriş | Yüksek ama düşük getiri | ≈ endeks getirisi | −%30 / −%35 (kaldıraçsız) | | Kolay; kaldıraç yasak |

**Bırak (2010 sonrası kanıt yok ya da maliyet sonrası negatif):**
- Kısa vadeli reversal (koşulsuz), ay dönümü, bayram öncesi, pre-FOMC.
- S&P ekleme/çıkarma, spin-off endeksi, buyback (swing ufkunda).
- Büyük hisselerde SUE-PEAD, 1 aylık analist revizyonu, return seasonality, 52 haftalık zirve tek başına.
- 0DTE/gamma yön tahmini, kaldıraçlı ETF rebalans front-running.
- Temalı ETF'i lansmanda almak, kaldıraçlı short-vol.

**Önerilen kombinasyon ve gerçekçi beklenti:**
- Dağılım: %50 risk bütçesi sektör/tema momentumu (1), %30 kaldıraçlı trend (2, 2x), %20 earnings-event (3).
- Hepsine (4) ve (5) filtreleri uygulanıyor, event bahislerinde (7) kullanılıyor.
- Kaba beklenti: **net %15 – %25 USD CAGR, döngü MDD −%35 / −%50, yılların ≈ %20 – %25'i negatif.**
- 2023-24 tipi tema yıllarında +%40 – %70 mümkün. 2000–02 / 2008 / 2022 tipi yıllarda −%25 / −%45 beklenmeli.
- %40'ı ortalama hedef yapmak bu kanıt setiyle desteklenmiyor.

**Bireysel (Türkiye'de yerleşik) uygulama notları [H, doğrula]:**
- IBKR üzerinden ABD hisse, opsiyon ve CME vadeli erişimi mümkün.
- ABD, yerleşik olmayan kişiden hisse sermaye kazancı vergisi almaz. Temettü stopajı ABD-Türkiye anlaşmasıyla ≈ %20.
- Türkiye'de yurt dışı menkul kazancı yıllık beyanla gelir vergisine tabi.
- ABD domisilli ETF'lerde $60 bin üstü veraset vergisi riski var. Vadeli işlemler bunu ve ETF giderini azaltır.
- Short ve borrow maliyetleri, kenarı küçük hisse short bacağında olan sinyalleri (DTC, IO_SI, retail-fade) bireysel olarak uygulanamaz kılıyor.

---

## Ek A — Kaynakça (birincil URL'ler)

- McLean-Pontiff 2016: https://ivey.uwo.ca/media/3775549/pontiff.pdf
- Hou-Xue-Zhang 2020: https://ideas.repec.org/a/oup/rfinst/v33y2020i5p2019-2133..html
- Jensen-Kelly-Pedersen 2023: https://nber.org/system/files/working_papers/w28432/w28432.pdf
- Chen-Velikov 2023: https://www.federalreserve.gov/econres/feds/zeroing-in-on-the-expected-returns-of-anomalies.htm
- Chen-Zimmermann veri: https://huggingface.co/datasets/OpenSourceAP/CrossSection
- Daniel-Moskowitz 2016: https://www.nber.org/papers/w20439
- Barroso-Santa-Clara 2015: https://econpapers.repec.org/RePEc:eee:jfinec:v:116:y:2015:i:1:p:111-120
- Da-Gurun-Warachka 2014: https://www3.nd.edu/~zda/Frog.pdf
- Moskowitz-Ooi-Pedersen ve AQR veri: https://www.aqr.com/Insights/Datasets/Time-Series-Momentum-Factors-Monthly
- Lou-Polk-Skouras 2019: https://personal.lse.ac.uk/polk/research/TugOfWar.pdf
- Martineau 2022: https://cfr.ivo-welch.info/published/papers/martineau2021rest.pdf
- PEAD tartışması (Subrahmanyam 2025 özeti): https://anderson-review.ucla.edu/is-post-earnings-announcement-drift-a-thing-again
- Frazzini-Lamont 2007: https://www.nber.org/system/files/working_papers/w13090/w13090.pdf
- Barber ve ark. 2013 (EA premium): https://econpapers.repec.org/RePEc:eee:jfinec:v:108:y:2013:i:1:p:118-138
- Garfinkel-Sokobin 2006: https://www.biz.uiowa.edu/faculty/jgarfinkel/pubs/drift_JAR.pdf
- Lucca-Moench: https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf
- Kurov-Wolfe-Gilbert 2021: https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html
- Cohen-Malloy-Pomorski 2012: https://www.nber.org/digest/apr11/decoding-inside-information
- Greenwood-Sammon 2025: https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
- Brav ve ark. 2008: https://corpgov.law.harvard.edu/wp-content/uploads/2008/03/hedge_fund_activism-final.pdf
- Hong ve ark. DTC: https://www.nber.org/papers/w21166.pdf
- Barber-Huang-Odean-Schwarz 2022: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3715077
- Fu-Huang (buyback): https://ink.library.smu.edu.sg/lkcsb_research/3531
- Bondarenko / Cboe PUT: https://www.cboe.com/insights/posts/generating-income-and-managing-risk-cash-secured-put-writing-in-a-low-equity-return-environment
- 0DTE perakende kayıpları: https://www.bloomberg.com/news/articles/2023-04-21/day-traders-lose-358-000-per-day-gambling-on-zero-day-options
- Ben-David ve ark. ETF: https://www.nber.org/papers/w28369
- Ken French veri: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- FRED NASDAQ100 / VIX / DTB3: https://fred.stlouisfed.org/series/NASDAQ100

## Ek B — [H] etiketli, öncelikle doğrulanması gerekenler

1. Gayed-Bilello 2016 orijinal sonuçları (SSRN 2741701).
2. Xing-Zhang-Zhao "%10,9/yıl".
3. Cremers-Weinbaum "50 bp/hafta".
4. Gao-Xing-Zhang straddle getirisi.
5. Dubinsky ve ark. 2019.
6. Aboody-Lehavy-Trueman pre-earnings run-up.
7. SEC 13D 5 iş günü kuralı.
8. Field-Hanka lockup ve Bradley-Jordan-Ritter quiet-period büyüklükleri.
9. Cederburg ve ark. 2020.
10. Bessembinder 2018 "%4".
11. Barber-Lee-Liu-Odean ve Chague ve ark. baz oranları.
12. XIV/Volmageddon ayrıntıları; GME fiyatları.
13. Kuantum/nükleer/kripto hisse rakamları.
14. ABD veraset vergisi ve stopaj oranları.
