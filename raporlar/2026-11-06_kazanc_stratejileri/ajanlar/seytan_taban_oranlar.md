# Şeytanın avukatı: taban oranlar, kenar çürümesi ve yüksek getirinin matematiği (06.11.2026)

Ajan raporu. Yatırım tavsiyesi değildir.

**Yöntem ve etiketler.** Web arama kotası (tüm ajanlarla paylaşılan 200 arama) bu ajan başladığında dolmuştu, bu yüzden tek bir arama bile yapılamadı. Kanıtlar üç yoldan toplandı: bilinen birincil URL'lerin doğrudan okunması (PDF'ler `pdftotext` ile açıldı), kardeş ajan raporlarındaki kaynaklar ve kendi simülasyonlarım. Her iddianın yanında etiketi var:
- **[D]** bu oturumda birincil kaynaktan okundu.
- **[A]** kardeş ajan raporundan alındı (`abd_kim_kazaniyor.md`, `abd_swing_kenarlar.md`, `bist_kim_kazaniyor.md`); kaynak orada.
- **[EB]** eğitim bilgim; bu oturumda doğrulanmadı.
- **[H]** kendi hesabım veya simülasyonum.

Betikler (repoya yazılmadı): `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/sim/math_target.py`, `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/sim/math_extra.py`, `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/sim/dd_fix.py`, `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/sim/sprt.py`. Çıktılar aynı klasörde `out_math.txt` ve `out_extra.txt` olarak duruyor.

---

## 0. Kısa cevap

1. **Taban oran acımasız ve her ülkede aynı.** Aktif bireysel trader'ların bir yılda kâr edenleri %10-15 civarında. Bu yüzde kâr edenleri sayıyor; risksiz faizi yenenler daha az. Bir sonraki yıl da öngörülebilir biçimde kazananlar **%1'in altında**. Rakamlar şöyle:
   - Tayvan: 360 bin day trader'ın %13-15'i kâr ediyor, **<%1'i** kalıcı [D].
   - Brezilya: en az 300 gün devam edenlerin **%97'si** zarar etti; banka gişe memuru maaşını geçen **%0,4** [D].
   - Hindistan (FY26): **%87,7** zararda [D].
   - Türkiye kaldıraçlı FX: 41 çeyrekte ortalama **%67** zararda [D, kendi hesabım].
   - ESMA CFD: **%74-89** zararda [D].
2. **Kalıcılık asimetrik. Kaybetmek, kazanmaktan çok daha kalıcı.** SEBI verisinde iki yıl üst üste kaybedip devam edenlerin **%90'ı** üçüncü yıl da kaybediyor; deneyim kârlılığı artırmıyor [D]. Tayvan'da önceki yılın en iyi 500'ü ertesi yıl day-trade portföyünde günde 28,1 bps net kazanıyor. Ama toplam portföy alfası yalnız **2,0 bps/gün (≈ %5/yıl)** [D].
3. **Yayınlanmış anomaliler büyük ölçüde ya yok ya da küçük.**
   - 447 anomalinin %64'ü %5 düzeyinde, %85'i t < 3 eşiğinde anlamsız (Hou-Xue-Zhang) [D].
   - Maliyet ve yayın etkisinden sonra ortalama anomali ayda **8 bps** getiriyor (Chen-Velikov, FEDS); yayınlanmış sürümde 4 bps [D/A].
   - Yayın sonrası düşüş McLean-Pontiff'te %35 (çalışma kâğıdı) [D], yayınlanmış sürümde %58 [EB/A].
   - Çürüme en çok **büyük, likit, düşük idiosenkratik riskli** hisselerde görülüyor [D]. Kullanıcının BIST30 ağırlıklı lead-lag kenarları tam bu sınıfta.
4. **Kullanıcının 1,1 milyon testi tek başına "kenar" üretir.** Sıfır gerçek kenarda 6 yıllık veriyle 1,1 milyon bağımsız denemenin en iyisinin beklenen yıllık Sharpe'ı **≈ 2,0**. Bonferroni eşiği **z ≈ 5,47** [H]. Hayatta kalan 3-4 kenarın 2024-26'da zayıflaması bu istatistikle tutarlı.
5. **Hedefin matematiği.** Sürdürülebilir maksimum log-büyüme fazlası **SR²/2**; bu tam Kelly'de, volatilite = SR iken elde ediliyor.
   - SR 0,5'te fazla en çok **%12,5/yıl** olur. Bunun için %50 volatilite gerekir ve 5 yılda %50+ düşüş olasılığı %86 [H].
   - ABD'de %20-40 dolar getiri, T-bill üstünde 16-36 puan demek. Yarım Kelly'de bunun için **SR ≥ 0,65-0,98** gerekiyor [H].
   - SR 1'lik bir stratejiyi %40 volatiliteyle 5 yıl koşmanın tipik bedeli: medyan en büyük düşüş **%45**, p90 %62, %50'yi aşan düşüş olasılığı **~%34** [H].
6. **Kelly'nin gizli tuzağı.** Tahmini SR'ye göre tam Kelly oynanır ve gerçek SR tahminin yarısıysa, beklenen fazla büyüme **sıfır** olur. Bu sonuç SR'nin büyüklüğünden bağımsız [H]. Literatürdeki tipik yayın sonrası kayıp (%26-58) bunu gerçekçi bir senaryo yapıyor.
7. **Kenarı şanstan ayırmak yıllar alır.** t = 2 için gereken süre SR 0,5'te **16 yıl**, SR 1'de **4 yıl**, SR 2'de 1 yıl. t = 3 için 36 / 9 / 2,25 yıl [H]. %30 isabetli ve +0,2R beklentili bir breakout sistemini sıralı testle (SPRT) doğrulamak medyan **~390 işlem** istiyor [H]. Kullanıcının 30 bps / 300 bps'lik tipik kenarı için t = 2'ye **400 işlem** gerekiyor. Yılda 60 işlemle bu 6,7 yıl eder. 1,5-3 yıllık yarı ömürle o noktada kenarın yalnız %5-21'i kalmış olur [H].
8. **Efsaneler büyük ölçüde örneklem seçimi.**
   - Sıfır kenarlı 700 kişilik bir yarışmada, %100 volatiliteyle kazananın medyan getirisi **+%1.239** [H].
   - USIC'te kârda kalanlar: 2022'de %8, 2026 ilk yarısında %17, 2026 dokuz ayda %11,9 [A]. Aynı dönemlerde rastgele ve sıfır alfalı trader'lar %24-25 ve %41-50 oranında kârda olurdu [H]. Yani medyan katılımcı rastgeleden **kötü**.
   - Tek yıllık %300-1000 beceri kanıtı değil. Asıl sinyal çok yıllık kalıcılık.
9. **Türkiye'de denetlenmiş bir bireysel trader sicili yok** [A]. SPK yaptırımları hızla artıyor:
   - 2025'te 481 kişi hakkında suç duyurusu (2024'te 275), 208 kişiye işlem yasağı (73), 127 piyasa dolandırıcılığı denetimi [D].
   - 2025'in en çok kazandıran fonu (%4.233) manipülasyon ürünüydü [A].
10. **Engel oranı düzeltmesi.**
    - Ekim 2026 brüt mevduat faizi %43,79; %17,5 stopajdan sonra net **%36,1**; Eylül TÜFE'sine göre reel **≈ %4,9** [D/H]. Kullanıcının "%40-50 reel" dediği rakam nominal.
    - **Yapısal not:** VİOP'ta teminat nemalandırılıyorsa ya da faizli enstrümanla verilebiliyorsa, stratejinin aşması gereken engel %36 değil. Engel, maliyet ve vergi sonrası **sıfırın üstünde fazla getiri** olur [EB; aracı kurumla teyit edilmeli].
    - Dolar tarafında bir Türk mukim için fırsat maliyeti T-bill (%3,75-4,00 bandı) [D] artı TL carry primi. Bu prim sakin dönemde yılda ≈ %10-17 dolar, şoklarda −%19 ile −%31 [A/H].
11. **En savunulabilir yol** sırayla şöyle: (0) muhasebe yapısı, (1) vol hedefli çok varlıklı trend/rejim kümesi, (2) önceden görülebilen zorunlu akış olayları, (3) yalnız stres rejiminde koşullu likidite sağlama (kullanıcının mevcut reversal kenarları), (4) ABD'de rejim filtreli lider momentum, küçük riskle, (5) boyutu sınırlandırılmış negatif çarpık primler. Her biri için öldürme kriterleri ve ölçüm protokolü §5'te.

---

## 1. Taban oranlar: kim risksiz faizi yeniyor, ne kadar kalıcı?

### 1.1 Büyük örneklemli kanıt

| Pazar / çalışma | Örneklem | 1 yıl | Çok yıl / kalıcılık | Tür | Kaynak |
|---|---|---|---|---|---|
| **Tayvan**, Barber-Lee-Liu-Odean, "The Cross-Section of Speculator Skill" | Ortalama yılda 360.000 day trader (1992-2006, tüm TSE işlemleri) | Ücret ve vergi sonrası kâr eden: **≈ %13** (metin) / **≈ %15** (giriş ve sonuç) | Önceki yılın en kârlı ≈ 1.000'i (**<%1**) ertesi yıl öngörülebilir biçimde kazanıyor. En iyi 500: day-trade portföyünde günde 49,5 bps brüt / **28,1 bps net**. **Toplam portföy alfası 2,0 bps/gün (≈ %5/yıl)**. İlk 10.000'in altındakiler günde −5,7 bps (yılda −15 puandan fazla) | Hakemli (JFM 2014 [A]) | [D] https://faculty.haas.berkeley.edu/odean/papers/day%20traders/Day%20Trading%20Skill%20110523.pdf |
| **Brezilya**, Chague-De-Losso-Giovannetti, "Day trading for a living?" | 2013-15'te mini endeks vadelide day trade'e başlayıp **en az 300 gün** devam eden herkes | **%97 zarar**. Yalnız **%0,4**'ü gişe memurundan (54 $/gün) fazla kazandı. En iyi birey 310 $/gün, standart sapma 2.560 $ | "Öğrenme kanıtı yok" | Çalışma kâğıdı, FEA-USP 2019_47 | [D] https://econpapers.repec.org/RePEc:spa:wpaper:2019wpecon47 |
| **ABD**, Barber-Odean (2000) | 66.465 hane, 1991-96 | En çok işlem yapan beşte bir **%11,4**, piyasa %17,9. Ortalama hane %16,4; devir hızı %75/yıl | – | Hakemli (JF 55(2)) | [D] https://faculty.haas.berkeley.edu/odean/papers%20current%20versions/individual_investor_performance_final.pdf |
| **Hindistan**, SEBI hisse türevleri (FY25-FY26), en büyük 15 aracı kurum, bireylerin ≈ %90'ı | FY26: 78,6 lakh trader (FY25'te 98,1 lakh) | **%87,7 zarar**. Toplam net zarar ₹91.685 crore, kişi başı ₹1,17 lakh. Zararın %92'si opsiyondan. Prop trader'lar ₹44.000 crore brüt kâr yaptı; FPI ve prop kârının **%99'u "algo" kuruluşlarda** | İki yıl üst üste kaybedip devam edenlerin **≈ %90'ı** yine kaybediyor. Trader-çeyrek gözlemlerinin %85'i zararda. Kâr ve zararlı çeyrekleri olanların %79'unda ortalama kazanç ortalama kayıptan küçük. Bırakanların %86-89'u son çeyreğinde zarardaydı | Düzenleyici veri, PR 50/2026, 20.08.2026 | [D] https://www.sebi.gov.in/sebi_data/attachdocs/aug-2026/1787236407005.pdf |
| Hindistan, SEBI FY22-FY24 | >1 crore trader | 3 yılda **%93 zarar**, toplam ₹1,8 lakh crore üstü | 3 yıl boyunca kârda olan ≈ %7,2; maliyet sonrası ₹1 lakh üstü kazanan ≈ %1 | Düzenleyici | [EB] (Eylül 2024 basın bülteni; bu oturumda açılamadı) |
| **AB**, ESMA CFD ürün müdahalesi | Ulusal otoritelerin analizleri | Bireysel CFD hesaplarının **%74-89'u zararda**. Müşteri başı ortalama zarar 1.600-29.000 € | Kuruma özgü zarar oranını açıklamak zorunlu | Düzenleyici, 27.03.2018 | [D] https://www.esma.europa.eu/press-news/esma-news/esma-agrees-prohibit-binary-options-and-restrict-cfds-protect-retail-investors |
| **Türkiye**, kaldıraçlı işlemler (FX), SPK'nın zorunlu kıldığı kurum bildirimi (TSPB derlemesi) | 28-34 kurum × 41 çeyrek (2016/06-2026/06) | Çeyrek içinde zararda olan hesap oranı, ağırlıksız kurum ortalaması: **%67,0**. Çeyreklerin %90'ında %60'ın üstünde. Aralık %52,0 (2022/12) ile %80,0 (2016/12). **2026/06'da ortalama %74,4, medyan %77,0** | Kümülatif zarar oranı daha yüksek olmalı (çeyreklik anlık görüntü) | Düzenleyici veri | [D, Excel'den kendi hesabım] https://tspb.org.tr/wp-content/uploads/2026/07/1_TSPB-Kar-Zarar-2026-2.xlsx |
| **Türkiye**, pay piyasası, Erdem-Arık-Yüksel (Borsa İstanbul Araştırma) | 2011-12, MKK'dan 20.000 bireysel yatırımcı | Piyasaya göre ortalama **−%0,281/hafta** (≈ −14,6 puan/yıl). En yüksek devir hızlı dilim **−%0,538/hafta**. En büyük portföy dilimi −%0,104/hafta. Yatırımcıların ≈ %70'i endeksi yenemedi | – | Çalışma kâğıdı / hakemli dergi [A] | [D] https://mpra.ub.uni-muenchen.de/46804/1/MPRA_paper_46804.pdf |
| **USIC** (gerçek parayla, kendini seçen ABD yarışmacıları) | 316 / 688 / 712 katılımcı | Kâr eden: 2022'nin 10 ayında **%8** (26/316); 2026 ilk yarısında %17 (115/688); 2026'nın 9 ayında %11,9 (85/712) | §4 | Yarışma verisi | [A] https://completetradersedge.com/wp-content/uploads/2026/09/CTE-Research-Sheet-US-Investing-Championship-2.pdf ; https://finance.yahoo.com/markets/stocks/articles/united-states-investing-championship-nine-121500218.html |

**1 / 3 / 5 yıl sentezi [H, yukarıdaki satırlardan]:**
- **1 yıl:** Kâr eden %10-15. Örnekler: Tayvan %13-15, SEBI FY26 %12,3, USIC %8-17. Risksiz faizi yenen bundan az. TL'de ise %36 net engeli yenen oran çok daha az; Erdem ve diğ.'de ortalama birey endeksin bile 14,6 puan gerisinde.
- **3 yıl:** Kâr eden ≈ %3-7. Brezilya'da 300 günden fazla devam eden %3; SEBI FY22-24'te %7,2 [EB].
- **5 yıl ve kalıcı:** **<%1**. Tayvan'ın yıldan yıla öngörülebilir kazananları. Doğrudan 5 yıllık bir ölçüm bulamadım.

Fonlar için benzer bir sonuç var: Barras-Scaillet-Wermers (JF 2010), ABD fonlarının ≈ %0,6'sını maliyet sonrası "yetenekli" buluyor [EB].

### 1.2 Kazananlar kimler, neden kalıcı?
- **Tayvan'ın kazananları** likidite sağlayıcı değil. Agresif emir veriyorlar (en iyi 500'de emirlerin %71'i agresif), short yapmaya istekliler ve birkaç hissede yoğunlaşıyorlar [D]. Kenarları gerçek ama kapasiteye bağlı: day-trade portföyündeki 28 bps/gün toplam portföyde 2 bps/gün'e iniyor.
- **Hindistan'da** kârın sahibi prop ve FPI tarafındaki "algo" kuruluşları (%99) [D]. Bireyler arasında en kötü grup opsiyon alıcıları. Trader'ların ≈ %97'si ağırlıkla opsiyon alıyor; pozitif medyan getiri yalnız ağırlıkla opsiyon satanlarda (≈ %2) görülüyor [D]. Bu, negatif çarpık primin (volatilite primi) gerçek olduğunu, ama alanların bunu ödediğini gösteriyor.
- **Portföy büyüklüğü koruyucu.** SEBI'de zarar oranı hisse portföyü olmayanlarda %93, ₹10 crore üstündekilerde %58 [D]. BIST'te en büyük portföyler kabaca piyasa kadar kazandı [D].
- **Türkiye'de kim kazanıyor?** Kaldıraçlı FX karşı tarafı, kredili işlem faizi alan aracı kurumlar, DMA/HFT masaları ve içerdekiler [A]. Bireysel taraf için kamuya açık bir VİOP kâr/zarar istatistiği bulunamadı [A].

### 1.3 Bu kullanıcı için okuma
Kullanıcının canlı deneyimi ("3-4 kenar kaldı, sık sık sakat geliyor") taban oranın tam ortasında duruyor. Bu bir başarısızlık değil, beklenen sonuç. Kullanıcının üst %1'de olup olmadığını ancak ileri test söyleyebilir (§5.3). Önsel olasılık düşük olmalı: yeni bir bireysel swing kenarının gerçek olma olasılığı ≈ %10-20. Bu tahmin HXZ'deki %64-85'lik başarısızlık oranından ve taban oranlardan geliyor [H].

---

## 2. Kenar çürümesi: neden ölüyorlar, hangileri yaşıyor?

### 2.1 Literatür, sayılarla

| Çalışma | Bulgu | Tür | Kaynak |
|---|---|---|---|
| McLean-Pontiff, çalışma kâğıdı (2013) | 82 karakteristik. Örneklem dışı çürüme ≈ %10 (anlamsız), **yayın sonrası ≈ %35**. **Arbitraj maliyeti düşük portföylerde çürüme daha büyük**: büyük hisse, dar spread, yüksek hacim, düşük idiosenkratik volatilite, temettü ödeyen. Sharpe ve t-istatistiği çürümeyi açıklamıyor | Çalışma kâğıdı | [D] https://ivey.uwo.ca/media/3775549/pontiff.pdf |
| McLean-Pontiff, JF 71(1) 2016 | 97 öngörücü; **örneklem dışı −%26, yayın sonrası −%58**. Farkın ≈ %32'si yayından öğrenen arbitraj | Hakemli | [EB/A] (aynı URL'nin yayınlanmış sürümü) |
| Hou-Xue-Zhang, "Replicating Anomalies" (RFS 33(5) 2020) | 447 anomali. NYSE kırılımı ve değer ağırlıkla **286'sı (%64)** %5'te anlamsız. **102 likidite değişkeninin 95'i (%93)** anlamsız. t ≥ 3 eşiğinde **380'i (%85)** anlamsız. Anlamlı 161'in büyüklüğü de raporlanandan çok daha düşük | Hakemli | [D] https://www.nber.org/papers/w23394 |
| Harvey-Liu-Zhu (RFS 29(1) 2016) | Çoklu test çerçevesinde yeni faktör için **t > 3,0** gerekiyor; "çoğu iddia büyük olasılıkla yanlış" | Hakemli | [D] https://www.nber.org/papers/w20592 |
| Jensen-Kelly-Pedersen (JF 78(5) 2023) | Bayesçi çerçevede faktörlerin çoğu **replike ediliyor**; 13 temaya kümeleniyor; 93 ülkede örneklem dışında çalışıyor | Hakemli | [D] https://www.nber.org/papers/w28432 |
| Chen-Velikov, "Zeroing in on the expected returns of anomalies" | FEDS sürümü: 120 anomali, maliyet ve yayın sonrası ortalama **8 bps/ay**; en güçlüleri veri madenciliği düzeltmesiyle 10-20 bps. JFQA 2023: 204 anomali, **4 bps/ay** | Çalışma kâğıdı / hakemli | [D] https://www.federalreserve.gov/econres/feds/zeroing-in-on-the-expected-returns-of-anomalies.htm ; [A] JFQA |
| Novy-Marx-Velikov (RFS 29(1) 2016) | Aylık tek yönlü devir hızı **<%50** olan anomaliler maliyet sonrası çoğunlukla anlamlı kalıyor; yüksek devirlilerin azı hayatta kalıyor | Hakemli | [D] https://www.nber.org/papers/w20721 |
| Falck-Rej-Thesmar, "Why and how systematic strategies decay" | Yayın yılı tek başına Sharpe çürümesi varyansının ≈ %30'unu açıklıyor. Her yıl, yeni yayınlanan faktörlerin çürümesi **+5 puan** artıyor. Aşırı uyum göstergeleri (sinyal karmaşıklığı, uç değere duyarlılık) ≈ %15 ek açıklama sağlıyor | Çalışma kâğıdı (arXiv 2105.01380) | [D] https://arxiv.org/abs/2105.01380 |
| Chen-Zimmermann açık veri (Ekim 2026), kardeş ajanın hesabı | 165 "clear" sinyalin aylık LS getirisi: in-sample %0,745 → yayın sonrası %0,318 → **likit evren 2010-25 %0,201**. Likit evrende 2010 sonrası t > 1,96 olanlar **%16** | Açık veri, hesap | [A] https://huggingface.co/datasets/OpenSourceAP/CrossSection |
| AQR TSMOM, kardeş ajanın hesabı | 1985-2009: SR **1,41**. 2010-2026/05: **SR 0,40**, en büyük düşüş −%28 | Veri seti | [A] https://www.aqr.com/Insights/Datasets/Time-Series-Momentum-Factors-Monthly |

**JKP ile HXZ çelişmiyor.** JKP'nin söylediği "işaret ve anlamlılık replike ediliyor". Bundan "maliyet sonrası bireyin para kazanacağı büyüklük var" sonucu çıkmıyor. Chen-Velikov'un 4-8 bps/ay'ı ve Novy-Marx-Velikov'un devir hızı eşiği ikincisini cevaplıyor. Yüksek devirli (1-3 günlük) kenarlarda net getiri sıfıra çok yakın.

### 2.2 Kullanıcının lead-lag kenarları neden çürüdü? Beş mekanizma
1. **Seçim yanlılığı, en büyük etken [H].** N bağımsız denemenin en iyisinin sıfır gerçek kenardaki beklenen yıllık Sharpe'ı (Bailey ve López de Prado yaklaşımı) şöyle:

   | N deneme | T = 3 yıl | T = 6 yıl | T = 10 yıl |
   |---|---|---|---|
   | 10 | 0,91 | 0,64 | 0,50 |
   | 1.000 | 1,88 | 1,33 | 1,03 |
   | **1.100.000** | **2,82** | **1,99** | **1,55** |

   Testler korelasyonlu olduğu için etkin N daha küçük. Ama etkin N = 1.000 bile alınsa, 6 yılda **SR ≈ 1,3 şansla** çıkıyor. %5 aile bazlı hata için Bonferroni eşiği **z = 5,47** (iki yönlü). Hayatta kalan kenarlar bu eşikle mi seçildi? Seçilmediyse in-sample büyüklük sistematik olarak şişkin, ve 2024-26'daki "zayıflama"nın bir kısmı ortalamaya dönüşten ibaret.
2. **Arbitraj maliyeti en düşük sınıf.** McLean-Pontiff'e göre çürüme en çok büyük, likit, düşük idiosenkratik riskli hisselerde [D]. XU030 baz sıçraması, SAHOL/AKBNK ve rafineriler → TUPRS tam bu sınıf. Rakipler de arttı: DMA vadeli hacmin %31-33'ü, yurtdışı kurumlar %43-47 [A]. Bu kenarlar en hızlı kapanan türden.
3. **Bilgi yayılımı kenarları HFT'nin ana yemi.** Lead-lag, yani bir piyasanın diğerini gecikmeli takip etmesi, ölçeklenebilir ve otomatikleştirilebilir. Yayın gerektirmeden kapanır, çünkü aynı korelasyonu herkes ölçebilir.
4. **Devir hızı ve maliyet.** 1-3 günlük tutuşta aylık devir %500'ün üstünde. Novy-Marx-Velikov eşiği %50 [D]. 15-70 bps'lik brüt kenardan 10-20 bps'lik gidiş-dönüş maliyeti ve kayma düşülünce net kenar, kenarın kendi standart sapmasının içinde kalıyor (§3.8).
5. **Rejim kırılması.** 2026 fon krizi, MSCI riski ve yabancı çıkışı korelasyon yapısını değiştirdi [A]. Lead-lag ilişkileri yapısal değil; akışın kimden geldiğine bağlı.

### 2.3 Hangi kenarlar yaşıyor?

| Tür | Mekanizma (neden arbitrajla kapanmıyor) | Kanıt | Bedeli | Kullanıcıya uygunluk |
|---|---|---|---|---|
| **Kriz riskli risk primleri.** Momentum, trend, carry, volatilite primi | Prim, kötü durumda kaybetmenin ödülü. Kapanmaz, çünkü ödenen bir sigorta primi | Momentum çöküşleri kısmen öngörülebilir (panik dönemleri, piyasa toparlanması). Dinamik ölçekleme alfa ve Sharpe'ı **≈ 2 katına** çıkarıyor (Daniel-Moskowitz, JFE 2016) [D] https://www.nber.org/papers/w20439. Yüksek ve düşük faizli para birimleri arasındaki kur hareketleri **negatif çarpık**; ani carry çözülmeleri likidite kurumasıyla geliyor (Brunnermeier-Nagel-Pedersen) [D] https://www.nber.org/papers/w14473. TSMOM yayından sonra da pozitif ama SR 1,41'den 0,40'a indi [A] | Kuyruk riski. Carry ve vol satışında sol kuyruk; momentumda çöküş; trendde uzun kurak dönem (SG Trend 12 ayda −%18,7 [A]) | **Yüksek.** Rejim kümelenmesi bunun sezgisel hâli |
| **Arbitraj sınırıyla korunan davranışsal kenarlar** | Short maliyeti, idiosenkratik risk, sermaye kısıtı | Çürüme yüksek idiosenkratik riskli ve az likit hisselerde daha az (McLean-Pontiff) [D]. Retail sürü alımlarının ardından 1 ayda −%5 ile −%9, yalnız <1 milyar $ hisselerde (Barber-Huang-Odean-Schwarz) [A] | Short ve borç alma zorluğu, squeeze | Orta. BIST'te spot short yasağı riski var; VİOP'ta tekil hisse sayısı sınırlı |
| **Kapasite kısıtlı küçük ölçek kenarları** | Büyük para giremez, getiri ölçeklenmiyor | Tayvan'ın en iyi day trader'ları yoğunlaşıyor ama toplam portföy alfası küçük [D]. Kullamägi 105 milyon $'da kırıldı [A] | Likidite, kayma | Yüksek. Kullanıcının ölçeğinde kapasite bağlayıcı değil |
| **Bilgi işleme kenarları** | Karmaşık ve dağınık bilgiyi birleştirmek; dikkat sınırlı | "Fırsatçı" içeriden alımlardan kurulan portföy ayda **82 bps** anormal getiri veriyor; rutin içeriden işlemlerinki ≈ 0 (Cohen-Malloy-Pomorski, JF 2012) [D] https://www.nber.org/papers/w16454. Ekonomik bağlantılar ve "lazy prices" [EB] | Zaman ve uzmanlık | Yüksek. KAP, %5 bildirimleri ve fon portföy verileri |
| **Likidite sağlama ve zorunlu akış** | Zorunlu satıcının karşısında durmak; kriz anında sermaye kıtlaşıyor | Kısa vadeli reversal getirisi likidite sağlamanın bedeli; **VIX ile güçlü biçimde öngörülebilir**, 2007-09'da sıçradı (Nagel, RFS 2012) [D] https://www.nber.org/papers/w17653. Çıkış yaşayan fonların zorunlu satışlarının karşısında duranlar "yüksek anlamlı" getiri kazanıyor ve akış öngörülebilir (Coval-Stafford, JFE 2007) [D] https://www.nber.org/papers/w11357 | Krizde erken girip ezilmek (yakalanan bıçak) | **En yüksek.** Kullanıcının SAHOL/AKBNK ve baz sıçraması kenarları aslında likidite sağlama. Sabit boyutla değil, stres rejimine göre ölçeklenmeli. BIST'te 131 fon tasfiyede [A] |

---

## 3. Hedefin matematiği

### 3.1 Engel oranları (düzeltilmiş)

| Ölçü | Değer | Kaynak |
|---|---|---|
| TL mevduat, 3 aya kadar, brüt ortalama (2 Ekim 2026 haftası) | **%43,79** | [D] https://www.endeks24.com/bist-100-iki-ayda-yuzde-25-dustu |
| Stopaj: vadesiz ve 6 aya kadar mevduat, 9.7.2025 sonrası alınan para piyasası fonları | **%17,5**; BIST payında %0 | [D] https://parafomo.com/blog/stopaj-nedir-2026-stopaj-oranlari/ (15.10.2026) |
| Net nominal TL engeli | **%36,1** (22.10'daki %36'lık politika faizinden sonra mevduat faizleri düştüyse ≈ %30-33) | [H] |
| Reel net (Eylül TÜFE %29,73) | **≈ %4,9** (brüt %40'ta %2,5; brüt %37'de %0,6) | [H] |
| Fed fon faizi | **%3,75-4,00**: 16.09.2026'da +25 bps, 28.10.2026'da sabit | [D] https://www.stephens.com/uploads/shared/documents/PCG-Docs/FOMC-Updates/Fed-Update-9-16-26.pdf ; https://www.federalreserve.gov/monetarypolicy/files/monetary20261028a1.pdf |
| TL carry'nin dolar karşılığı | Komite: ortodoks dönemde short F_USDTRY 64 günde +%2,6 → **yıllık ≈ +%10,6**, pencerelerin %88'i pozitif; şoklarda −%19 ile −%31. 2026 yılbaşından beri ≈ +%15-17 USD | [A] komite raporu, `bist_kim_kazaniyor.md`; [H] yıllıklandırma |

**İki yapısal sonuç:**
1. **Doğru TL engeli nominal %36, reel ≈ %5.** "%40-50 reel" bir yanılgı. Doğru çerçeve şu: TL'de risksiz getiri, sermayenin reel değerini ancak koruyor.
2. **VİOP'ta engel, aşılması gereken getiri değil, bir muhasebe sorusu.** Vadeli fiyat taşıma maliyetini içeriyor (F ≈ S·e^{(r−q)T}), yani long vadeli zaten "TL faizi üstündeki" getiriyi veriyor. Teminat nemalandırılıyorsa ya da DİBS veya fon payıyla verilebiliyorsa, toplam getiri = risksiz getiri + overlay. Bu durumda stratejinin aşması gereken engel, **maliyet ve vergi sonrası fazla getirinin sıfırdan büyük olması**. Teminat nakit olarak boşta duruyorsa, teminat kısmının fırsat maliyeti yılda %36 olur.
   - Pay ve endeks vadelilerinde bireysel stopajın %0 olması, %17,5 stopajlı para piyasası fonuna göre ek avantaj sağlıyor. **Bu bilgi [EB]; Takasbank teminat listesi, aracı kurumun nemalandırma oranı ve GVK geçici 67 kapsamı ayrıca teyit edilmeli.** Takasbank ve GİB sayfaları bu oturumda okunamadı.
   - Spot kredili alım tersine çalışıyor: kredi maliyeti ≈ %45-50 olduğu için engel yükseliyor [A].

### 3.2 Sharpe, kaldıraç ve büyüme [H]
Fazla log-büyüme g = SR·σ − σ²/2. Bunun en büyük değeri **SR²/2**'dir ve tam Kelly'de (σ = SR) elde edilir. Yarım Kelly'de büyüme (3/8)·SR², volatilite SR/2.

| SR | Tam Kelly vol / fazla büyüme | Yarım Kelly vol / fazla büyüme |
|---|---|---|
| 0,3 | %30 / **%4,5** | %15 / %3,4 |
| 0,5 | %50 / **%12,5** | %25 / %9,4 |
| 0,75 | %75 / %28,1 | %38 / %21,1 |
| 1,0 | %100 / %50 | %50 / %37,5 |
| 1,5 | %150 / %112,5 | %75 / %84,4 |

Belirli bir fazla getiri hedefi için gereken SR (SR = E/σ + σ/2):

| Hedef fazla getiri E (risksizin üstü) | vol %15 | vol %25 | vol %35 | vol %50 | En az (tam / yarım Kelly) |
|---|---|---|---|---|---|
| +4 puan (TL'de ≈ %40) | 0,34 | 0,29 | 0,29 | 0,33 | 0,28 / 0,33 |
| +10 puan | 0,74 | 0,53 | 0,46 | 0,45 | 0,45 / 0,52 |
| +20 puan (USD'de ≈ %24) | 1,41 | 0,93 | 0,75 | 0,65 | 0,63 / 0,73 |
| +30 puan | 2,08 | 1,32 | 1,03 | 0,85 | 0,77 / 0,89 |
| +36 puan (USD'de ≈ %40) | – | – | – | – | 0,85 / 0,98 |

**Gerçekçi SR çapaları:**
- Çeşitlendirilmiş trend, 2010 sonrası ≈ 0,4 [A].
- Ortalama anomali maliyet sonrası ≈ 0,1-0,2 [D/H].
- Tayvan'ın en iyi 500 trader'ının toplam portföy alfası ≈ %5/yıl [D].
- Pod shop'lar yüksek Sharpe'ı düşük volatiliteyle üretiyor; 2025'te net %10-17,5 [A].

**Sonuç.** ABD'de %20-40 dolar getiri, yarım Kelly'de **SR 0,7-1,0** istiyor; bu, kurumların bile nadiren sürdürdüğü bir seviye. TL'de %36'yı +10 puan geçmek **SR ≈ 0,5** istiyor. Bu ulaşılabilir, ama tek bir kenarla değil.

### 3.3 Tahmin hatası Kelly'yi nasıl öldürür? [H]
Tahmini SR'ye göre tam Kelly oynanırsa (σ = SR̂), fazla büyüme g = h·SR̂² − SR̂²/2 olur; h, gerçek SR'nin tahmine oranı.
- **h = 0,5 iken g = 0.** Bu, SR̂ = 1, 1,5 ve 2 için de aynı. SR̂ 1 ve h = 0,3'te g = −%20/yıl; SR̂ 2 ve h = 0,3'te −%80/yıl.
- McLean-Pontiff'teki −%26 ile −%58 arası ve §2.2'deki seçim yanlılığı, h ≈ 0,4-0,75'i gerçekçi kılıyor.
- **Kural:** Önce SR'yi en az %50 tıraşla, sonra tıraşlanmış SR'nin ¼ ile ½ Kelly'siyle oyna.
- Kelly fraksiyonu c iken başlangıç servetinin x kesrine **hiç düşmeme** olasılığı 1 − x^(2/c − 1):
  - Tam Kelly: yarıya düşme olasılığı **%50**.
  - ½ Kelly: %12,5.
  - ¼ Kelly: %0,8.

### 3.4 Düşüş ve iflas riski, 5 yıl, günlük adım, 20.000 yol [H]
"Fazla" sütunu, risksiz getiri çıkarıldıktan sonraki serveti ölçüyor; yani engele göre düşüşü gösteriyor.

| Senaryo | Fazla getiride medyan / p90 düşüş | Fazla getiride P(düşüş > %50) | Nominal medyan düşüş | 5 yıllık CAGR, medyan (p10) | P(5 yıllık CAGR < risksiz) |
|---|---|---|---|---|---|
| USD, SR 0,5, vol %30 | %44 / %63 | %33 | %42 | %15,3 (−%2,7) | %22 |
| USD, SR 0,5, vol %40 | %55 / %75 | %64 | %53 | %16,7 (−%7,3) | %26 |
| USD, SR 1, vol %30 | %36 / %50 | %11 | %34 | %33,8 (%12,9) | %3 |
| **USD, SR 1, vol %40** | **%45 / %62** | **%34** | %44 | %43,3 (%14,2) | %4 |
| TL (r = %36), SR 0,5, vol %30 | %44 / %62 | %33 | %30 | %50,9 (%26,9) | %22 |
| TL, SR 1, vol %40 | %45 / %62 | %35 | %36 | %87,2 (%48,9) | %4 |

- Kalın kuyruklu getirilerde (t dağılımı, df = 4) SR 1 ve vol %40 için medyan düşüş %43, P(> %50) %29. Diffüzyona yılda 0,3 olasılıkla −%20'lik sıçramalar eklenince medyan %40, P(> %50) %20.
- **TL'de nominal düşüşü %36'lık taşıma yumuşatıyor; engele göre düşüş aynı kalıyor.**

İflas riski: 5 yıl içinde servetin başlangıcın %50'sine inme olasılığı, gerçek SR'ye göre.

| Kelly katı | SR 0,5 | SR 1 |
|---|---|---|
| ¼ | %0 | %1 |
| ½ | %6 | %11 |
| 1 | %35 | %46 |
| 1,5 | %59 | %71 |
| 2 | %74 | %87 |

Tam Kelly'de SR 1 ile bile 5 yılda %50'lik düşüş neredeyse kesin (%100).

### 3.5 Pozitif ve negatif çarpıklık [H]
**Pozitif çarpık sistem** (breakout ve momentum tipi): isabet %30, kazanç ortalama 3R (lognormal dağılımlı), kayıp −1R, beklenti **+0,20R**, sd 2,13R, çarpıklık +2,1.
- 200 işlemde en uzun kayıp serisi: medyan **12**, p90 17, en kötüsü 33.
- İşlem başı %0,5 riskle 200 işlem: medyan getiri yalnız **+%20**, medyan düşüş %9,2 (p90 %14,7). 200 işlem sonunda hâlâ zararda olma olasılığı %10.
- Net kârın **%177'si** en iyi %7'lik işlemlerden geliyor (medyan). Yani geri kalan işlemler toplamda zararda. Bu, Zarattini ve diğ.'nin "<%7" bulgusuyla tutarlı [A].
- **Gerçek bir kenarı erken öldürme riski:** ilk 50 işlemin toplamı %26 olasılıkla, ilk 100'ü %17 olasılıkla negatif.
- %0,5 risk ve +0,2R ile yılda +%50 imkânsız. Bunun için ya ≈ %1 risk ve yılda 250 işlem, ya da ≥ 0,4R beklenti gerekiyor. Şampiyonların yaptığı tam olarak bu: yoğunlaşma ve güçlü piyasada marjin [A].

**Negatif çarpık sistem** (TL carry'ye benzer): çeyrekte +%4 (olasılık 0,92), −%25 (olasılık 0,08). Yıllık ≈ +%6,9, gerçek **SR 0,43**, çarpıklık −3,1.
- 3 yıllık pencerelerin **%37'sinde hiç çöküş yok**. Bu pencerelerde ölçülen medyan SR **4,1**, yani gerçeğin yaklaşık 10 katı. Çöküşsüz 5 yıl olasılığı %19.
- **Çöküş yaşamadan raporlanan carry ve vol satışı sicili, SR hakkında hiçbir şey söylemez.** Komitenin "%88 pozitif pencere" bulgusu bununla aynı yapıda.
- Minimum sicil uzunluğu (Bailey ve López de Prado, %95 güven), SR 1 için:
  - normal dağılımda **2,9 yıl**,
  - çarpıklık −2, basıklık 12 ile **5,0 yıl**,
  - çarpıklık +1,5, basıklık 8 ile 2,0 yıl.

### 3.6 Konsantrasyon ve "stratejik küme" [H]
Etkin bağımsız bahis sayısı N/(1 + (N−1)ρ). SR çarpanı bunun karekökü.

| Pozisyon sayısı | ρ = 0 | ρ = 0,3 | ρ = 0,6 | ρ = 0,8 |
|---|---|---|---|---|
| 5 | 5,0 bahis (SR × 2,24) | 2,27 (× 1,51) | 1,47 (× 1,21) | **1,19 (× 1,09)** |
| 8 | 8,0 (× 2,83) | 2,58 (× 1,61) | 1,54 (× 1,24) | 1,21 (× 1,10) |

**Kullanıcının kümeleri tek bir bahis.** ρ = 0,6-0,8'lik 5 pozisyonluk bir küme SR'yi ancak %9-21 artırıyor. Risk bütçesi küme düzeyinde verilmeli, pozisyon düzeyinde değil. Kümeler arası korelasyon < 0,3 tutulursa ancak 2-3 küme gerçek çeşitlendirme sağlar. Konsantrasyonun faydası sağ kuyruğu (Bessembinder: hisselerin ≈ %4'ü tüm net servet yaratımını açıklıyor [A] https://wpcarey.asu.edu/sites/default/files/2021-10/do-stocks-outperform-treasury-bills.pdf) yakalamak; bedeli SR'yi değil, volatiliteyi artırması.

### 3.7 Kenarı şanstan ayırmak için ne kadar veri gerekir? [H]

| Gerçek yıllık SR | t = 2 için yıl | t = 3 için yıl (HLZ eşiği) | 5 yılda gerçekleşen SR'nin < 0 çıkma olasılığı |
|---|---|---|---|
| 0,5 | **16** | 36 | %13 |
| 1,0 | **4** | 9 | %1,3 |
| 2,0 | 1 | 2,25 | ≈ 0 |

İşlem bazında gereken işlem sayısı (işlem başı SR = ortalama / sd):

| Kenar | İşlem başı SR | t = 2 | t = 3 | 1,1 milyon test için Bonferroni (t ≈ 5,3) |
|---|---|---|---|---|
| 15 bps / 250 bps | 0,060 | 1.111 | 2.500 | 7.891 |
| **30 bps / 300 bps** | 0,100 | **400** | 900 | 2.841 |
| 50 bps / 350 bps | 0,143 | 196 | 441 | 1.392 |
| 70 bps / 350 bps | 0,200 | 100 | 225 | 710 |
| Breakout, +0,2R / 2,13R | 0,094 | 454 | 1.020 | – |

- **Sıralı test (Wald SPRT; H0: μ = 0, H1: μ = backtest değeri; α = 0,05, β = 0,20).**
  - +0,2R'lik bir sistemde kenar gerçekse beklenen örneklem 432 işlem; simülasyonda medyan 389 işlem, doğru kabul %83.
  - Kenar sıfırsa 304 işlem (simülasyonda medyan 228, doğru ret %96).
  - Gerçek kenar backtest'in yarısıysa (+0,1R) ≈ 1.700 işlem gerekiyor.
- **Çürüme ile tespit yarışı.** İşlem başı SR 0,10 ve yılda 60 işlemle t = 2'ye 6,7 yılda ulaşılıyor. Kenarın yarı ömrü 1,5 yılsa o noktada kenarın **%5'i**, 3 yılsa **%21'i** kalıyor. **Hızlı çürüyen mikro kenarlar istatistiksel olarak doğrulanamaz.** Onlara güvenmenin tek yolu mekanizmadır; t-istatistiği yetmez.

### 3.8 Kullanıcının kenarları overlay olarak [H]
Varsayım: işlemler bağımsız, teminat risksiz getiriyi kazanıyor, L = sermayeye göre nominal çarpan.

| Brüt kenar / maliyet / işlem sayısı / işlem sd | L = 1: fazla getiri, vol, SR | L = 2: log-büyüme | L = 3: log-büyüme |
|---|---|---|---|
| 30 / 12 bps, 60/yıl, 300 bps | +%10,8, %23, **0,46** | +%10,8 | +%8,1 |
| 50 / 15 bps, 40/yıl, 350 bps | +%14,0, %22, 0,63 | +%18,2 | +%19,9 |
| 20 / 12 bps, 100/yıl, 250 bps | +%8,0, %25, 0,32 | +%3,5 | **−%4,1** |
| 70 / 15 bps, 25/yıl, 350 bps | +%13,8, %17,5, 0,79 | +%21,4 | +%27,5 |

**Okuma.**
- Kenarlar gerçekse, teminat nemalandırılıyorsa ve maliyet ≤ 15 bps ise, TL risksiz getirinin üstüne **+%8-14** ekleyebilir. Bu da toplam ≈ %44-50 nominal eder. Yani "%36'yı geçmek" mümkün.
- Kaldıraç SR'yi artırmıyor. L ≥ 3'te zayıf kenarın (SR 0,32) büyümesi negatife dönüyor.
- §3.7'ye göre bu kenarların gerçek olduğunu kanıtlamak yıllar alır. Bu yüzden uygun rolleri çekirdek değil, uydu.

---

## 4. Survivorship: efsaneler ve gurular

### 4.1 Sayılar ne diyor? [H + A]

**Sıfır kenarlı ve maliyetsiz N trader'lık bir yarışmada yılın kazananı** (yıllık volatilite σ, 20.000 tekrar):

| N | σ = %60 | σ = %100 | σ = %150 |
|---|---|---|---|
| 316 | +%362 (p10 %263, p90 %545) | +%944 | +%2.231 |
| 700 | +%433 | **+%1.239** (p10 %819, p90 %2.152) | +%3.263 |

- Minervini'nin 1997'deki +%155'i [A], tek başına sıfır kenarla bile beklenen kazanan düzeyinin altında. Luk'un 2025'teki +%969,8'i, %100 volatiliteli rastgele bir kazananla aynı aralıkta.
- **Kalıcılık daha bilgilendirici.** Sıfır kenarla, %100 volatiliteyle 3 yıl üst üste +%250'nin üstünde kapatma olasılığı: 700 kişide ≈ %4,3, 7.000 kişi-kohortta ≈ %36. Volatilite %80'de bu oranlar %1,0 ve %10. Luk'un 3 yıllık serisi (2024 +%283,1, 2025 +%969,8, 2026 dokuz ayda +%785,8 [A]) şansa karşı anlamlı bir kanıt. Ama yarışmanın 40 yıllık geçmişi ve çok sayıda kategorisi var; bunlar arasında seçim yapmak kanıtı zayıflatıyor.
- **Rastgele trader bu oranda kârda olurdu, katılımcılar daha azında oldu.** Beta 1 ve sıfır alfayla:
  - 2026 ilk yarısı (S&P +%10): σ %60-100'de rastgele trader'ların **%41-50**'si kârda olurdu; USIC'te gözlenen %17.
  - 2022 benzeri 10 ay (piyasa −%20): rastgele %24-25; gözlenen %8.
  - **Medyan katılımcı yazı-turadan anlamlı ölçüde kötü.** Olası nedenler maliyet, aşırı işlem ve disposition etkisi; SEBI'deki %79'luk "kazanç < kayıp" asimetrisi bunun bir örneği.
- **Gidenler görünmüyor.** SEBI'de bırakanların %86-89'u son çeyreğinde zarardaydı [D]. USIC'te katılım isteğe bağlı ve kendini seçmiş; aylık liste yayımlanması da isteğe bağlı [A]. Görünen kuyruk olduğundan kalın.

### 4.2 Bireysel efsaneler (ayrıntı `abd_kim_kazaniyor.md` §4'te) [A]

| İsim | Doğrulanabilir olan | Doğrulanamayan / ters kanıt |
|---|---|---|
| Minervini | USIC 1997 +%155; 2021'de $1M+ kategoride +%334,8 (Business Wire) | 1994-2000 için "≈ %220/yıl" ve "%33.500" iddiaları denetlenmemiş; kurs ve seminer satıyor (ticari teşvik) |
| Kullamägi (Qullamaggie) | 2026 Market Wizards kitabı için Coyle kayıtları inceledi | Bağımsız denetim yok. Kasım 2021'deki ≈ 105 milyon $ zirveden 2022 ortasında ≈ 45 milyon $'a indi (**−%57**) |
| Zanger | Fortune 1999 vergi beyannamesini gördü: 14,23 milyon $ sermaye kazancı | Tek dönem (1998-99 balonu); sonrasında denetimli kayıt yok |
| Luk, J Law, Kell | USIC kayıtları, aracı kurum ekstresiyle | Rekorlar güçlü tematik boğalarda kırıldı. Zirveden yıl sonuna geri vermeler −%26,6 ile −%51,9 arası |

### 4.3 Türkiye: sinyal grupları, gurular ve SPK
- **Denetlenmiş ve kamuya açık bir bireysel Türk trader sicili yok** [A]. Doğrulanabilir tek sicil TEFAS NAV'ı. O da 2025'te manipülatif bir fonun (TLY) **+%4.233**'lük getirisini "resmî" olarak gösterdi [A].
- **SPK 2025 Faaliyet Raporu** [D] (https://spk.gov.tr/data/61e48f651b41c60d1404d687/2025%20Y%C4%B1l%C4%B1%20Faaliyet%20Raporu.pdf):
  - Suç duyurusu yapılan kişi sayısı **481** (2024'te 275).
  - İşlem yasağı getirilen kişi **208** (73).
  - Toplam yaptırım uygulanan kişi 697 (357).
  - Denetimler: piyasa dolandırıcılığı 127 (116), **izinsiz sermaye piyasası faaliyeti 101** (81).
  - 62 yazılı başvurunun 34'ü izinsiz faaliyet, 16'sı piyasa dolandırıcılığı hakkında. 2025'te ilk derecede sonuçlanan 70 ceza davasının 32'si mahkûmiyet, 9'u beraat, 13'ü HAGB.
  - 25 payda 55 kişiye SPKn m.101 kapsamında tedbir amaçlı geçici işlem yasağı getirildi.
  - Erişim engeli (SPKn m.99/3) yaptırım türleri arasında sayılıyor, ama raporda adet verilmiyor.
- **SPK bültenleri 2026/49-78 (30 bülten, kendi taramam)** [D/H]: 13 URL'ye erişim engeli kararı çıktı. Bunların hepsi sahte aracı kurum ya da izinsiz platform sitesi ve uygulamasıydı. Bu örneklemde "Telegram" veya "sosyal medya" geçen bir yaptırım metni bulamadım. Sosyal medya ve Telegram üzerinden "hisse önerisi + pump" vakalarına dair birincil kanıtı bu oturumda doğrulayamadım. Varlıklarını bilgi bazlı piyasa dolandırıcılığı (SPKn m.107/2) ve izinsiz yatırım danışmanlığı (m.109) çerçevesinde biliyorum [EB].
- **2026 kriz yaptırımları** [A]: SPK 16.09'da 38 kişi hakkında suç duyurusunda bulundu. TRHOL dosyasında 37 kişi ve Tera'ya 2 yıl işlem yasağı geldi. ALKLC ve ANELE dosyasında 48 kişi hakkında suç duyurusu yapıldı.
- **Guru ekonomisinin matematiği:** binlerce takipçi ve onlarca grup var; her ay "en iyi çağrı" ex post seçiliyor. §4.1'deki tablo grup sayısına aynen uygulanır. Ayrıca takipçi akışı, guruya kendi pozisyonundan çıkış likiditesi sağlar. Bu bir piyasa dolandırıcılığı mekanizmasıdır; taban oranı negatif.

---

## 5. Bütün bu şüpheden sonra en savunulabilir yol

### 5.1 Sıralı ve yanlışlanabilir cevap
Bu kullanıcı deneyimli, swing ufkunda işlem yapıyor, kümeleme alışkanlığı var, VİOP'a ve ABD vadelilerine erişimi var. Sıralama ölçütü: (kanıtın gücü) × (kullanıcıya uyum) × (çürümeye dayanıklılık) × (yanlışlanabilirlik).

| Sıra | Yol | Neden | Beklenti (dürüst) | Yanlışlama testi |
|---|---|---|---|---|
| **0** (ön koşul) | **Muhasebe yapısı.** Sermayenin çoğu para piyasası fonunda veya repoda (net ≈ %30-36). VİOP teminatı nemalandırılıyor ya da faizli enstrümanla veriliyor. Tüm performans "risksiz getiri üstü, vergi ve maliyet sonrası" ölçülüyor | Engeli %36'dan sıfır fazlaya çeviriyor (§3.1). Stopaj farkı lehte olabilir [EB] | Alfa değil, ama hata payını ortadan kaldırıyor | Aracı kurumdan teminat nemalandırma oranını yazılı al. Oran politika faizinin < %80'iyse yapıyı değiştir |
| **1** | **Vol hedefli, çok varlıklı trend ve rejim kümesi.** XU030, USDTRY, altın, banka endeksi vadelileri; ABD micro vadelileri (S&P, Nasdaq, 10Y, petrol, altın). Hedef portföy vol'ü %15-20 | Kriz riskli prim ve davranışsal gecikme. Yayından sonra yaşıyor ama küçüldü (SR 1,41 → 0,40 [A]). Pozitif çarpık, öldürme kuralına uygun. Kullanıcının kümeleme sezgisinin sistematik hâli | SR 0,3-0,6 → fazla getiri +%4-10/yıl; TL toplamı ≈ %40-46 nominal. Kurak yıllar −%10-20 | 3 yıllık SR < 0 ise ya da XU030 ile korelasyon > 0,7 ise (yani sadece beta) öldür |
| **2** | **Zorunlu akış ve olay kümesi.** MSCI Haziran 2027 sınıflandırma incelemesi, 131 fonun tasfiye satışları, 13.11'de biten özkaynak esnekliği, halka arz kilit bitişleri, endeks değişiklikleri, SPK kural değişiklikleri | Coval-Stafford: zorunlu satıcının karşısında durmak yüksek getirili ve akış öngörülebilir [D]. Kapasite kısıtlı ve bilgi işleme gerektiriyor, bu yüzden çürümeye dayanıklı. BIST 28.08-16.09 vakası (n = 1) [A] | Olay başına %5-25, yılda 5-15 olay. İsabet ≈ %50-60, kazanç/kayıp ≥ 1,5 | Her olay türü önceden kaydedilir (yön, giriş/çıkış, beklenen büyüklük). 20 olaydan sonra ortalama fazla getiri ≤ 0 ise o türü öldür |
| **3** | **Koşullu likidite sağlama.** Kullanıcının SAHOL/AKBNK z-skoru ve XU030 baz sıçraması reversal'ı yalnız stres rejiminde (BIST realize vol > 1 yıllık p70) ve boyut vol'e göre | Nagel: reversal getirisi VIX ile güçlü biçimde artıyor [D]. Şu an BIST stres rejiminde | Overlay SR 0,3-0,6; +%5-12/yıl. Ancak kenarlar zaten zayıfladı | 100 işlemden sonra ortalama ≤ maliyet ya da gerçekleşen kayma > backtest kenarının %50'si ise öldür |
| **4** | **ABD'de rejim filtreli lider momentum ve breakout.** İşlem başı risk %0,25-0,5; yalnız endeks kısa GHO'ların üstündeyken | Bileşenler hakemli (Bessembinder, momentum, 52 hafta zirvesi); sonuçlar anekdot. En yüksek sağ kuyruk, en kötü taban oran | İyi tema yılında +%40-150, kötü yılda −%10-25 [A]. Doğrulama 300-450 işlem, yani 2-4 yıl sürer | SPRT. 150 işlemden sonra E[R]'nin %80 güven aralığının üst sınırı < 0 ise öldür. Kol düzeyinde düşüş > %20 ise dur |
| **5** | **Boyutu sınırlı negatif çarpık primler.** TL carry (short F_USDTRY), seçici opsiyon satışı | Gerçek prim (SEBI'de pozitif medyanlı tek grup opsiyon satıcıları [D]). Ama çöküşsüz sicil yanıltır (§3.5) | Yıllık +%7-15 USD; −%25-30'luk şok | Stres kaybı (−%30 kur şoku) toplam sermayenin ≤ %5-10'u olacak şekilde boyutlandır. Tek seferde bu sınırı aşan bir kayıp gelirse öldür |

**Kanıtla elenenler:**
- Kısa vadeli opsiyon alımı (SEBI'de opsiyon alıcıları en kötü grup; 0DTE).
- Kaldıraçlı FX (zararda olanlar %67-74).
- Halka arz serisi bittikten sonra hisse almak (52/53 düştü [A]).
- Guru ve sinyal grupları.
- Toplu testten çıkan, mekanizması belirsiz mikro kenarlar (şansla SR ≈ 2,0).
- Spot kredili kaldıraç (≈ %50 faiz).

**Kullanıcının "yüksek getiri" sorusuna dürüst cevap.** Sürdürülebilir hedef şu: TL'de risksiz getirinin üstüne +%10-20 puan, dolar bazında yıllık %15-25. Bu ancak 2-3 düşük korelasyonlu kümeden gelen toplam SR ≈ 0,6-0,8 ile ve ½ Kelly'nin altında oynanarak tutturulabilir; beklenen medyan düşüş %30-45 (§3.4). Tek yıllık +%100'ler pozitif çarpık kolun (1, 2 ve 4) iyi yıllarında gelir; plan bunlara dayanamaz.

### 5.2 Öldürme kriterleri (önceden yazılı, sayısal)
1. **Düşüş bandı.** Her kol için beklenen düşüş dağılımı önceden simüle edilir (§3.4 yöntemiyle, haircut'lı SR kullanılarak). Gerçekleşen düşüş > simülasyonun p95'i ise kol durur. Yeniden açılması yalnız mekanizma incelemesiyle olur.
2. **Beklenti testi.** n ≥ 100 işlemde E[R]'nin bootstrap %90 güven aralığının üst sınırı < tahmini işlem maliyetiyse öldür.
3. **Uygulama farkı.** Gerçekleşen kayma ve maliyet > backtest brüt kenarının %50'si ise öldür. Mikro kenarlarda en sık ölüm nedeni bu.
4. **Canlı ile backtest farkı.** 50 işlemden sonra canlı ortalama < backtest'in %50'siyse boyutu yarıya indir. 100 işlemden sonra < 0 ise öldür.
5. **Rejim ve mekanizma.** Kenarın gerekçesi ortadan kalkarsa t-istatistiğine bakmadan öldür. Örnekler: piyasa yapıcı girişi, kural değişikliği, fiyatlamayı değiştiren endeks dahil olması.
6. **Negatif çarpık kol.** Tek bir kayıp, önceden tanımlı stres kaybını (sermayenin %5-10'u) aşarsa öldür.
7. **Beta sızıntısı.** 12 aylık korelasyon > 0,7 ve XU030 / S&P / USDTRY'ye göre kalıntı alfa ≤ 0 ise kol beta'dır. Onu ucuz endeks pozisyonuyla değiştir.
8. **Toplam sermaye.** Engele göre toplam düşüş > %25 ise bütün kollarda boyut yarıya iner. > %35 ise sistematik kollar dışında her şey kapanır.

### 5.3 Kenarın gerçek olup olmadığını ölçme protokolü
1. **Hipotez kartı (işlemden önce).**
   - Mekanizma: kim, neden zorla ya da hatalı işlem yapıyor; arbitraj neden kapatmıyor (§2.3'teki beş sınıftan hangisi).
   - Evren; giriş, çıkış ve boyut kuralları.
   - Beklenen E[R], isabet, kazanç/kayıp oranı, yıllık işlem sayısı.
   - **Denenen varyant sayısı N.** Deflated SR için zorunlu.
   - Kart tarihli ve değiştirilemez. Değişiklik yeni bir hipotez sayılır.
2. **Backtest kabul eşiği.**
   - Seçim yanlılığı: in-sample SR > E[max SR | N, T] + 2·SE (§2.2 tablosu).
   - Büyük N için t ≥ 3.
   - Maliyet: gerçek VİOP komisyonu, spread ve limit gün etkisiyle.
   - Canlı beklenti: backtest SR'nin %50'si.
3. **İleri test boyutu.** Tıraşlanmış SR'nin ≤ ¼ Kelly'si, ya da pozitif çarpık sistemlerde işlem başı %0,25 risk. Sermayenin büyük kısmı para piyasası fonunda kalır.
4. **Takvim.**
   - Her 25 işlemde SPRT log-olabilirlik oranı güncellenir.
   - **12 ay ve 100 işlemden önce boyut artırılmaz; yalnız öldürme kararı verilebilir.**
   - "Kanıtlandı" demek için ya SPRT'nin H1'i kabul etmesi gerekir (+0,2R sistemde ≈ 300-450 işlem), ya da kol bazında 3 yıl ve en az bir stres rejimi.
5. **Metrikler** (aylık rapor, hepsi risksiz getiri üstü, vergi ve maliyet sonrası):
   - R cinsinden E[R] ve bootstrap güven aralığı; t-istatistiği; isabet; kazanç/kayıp; profit factor.
   - MAE / MFE.
   - Uygulama farkı (sinyal fiyatına göre bps).
   - Net kârın en iyi %5-10 işleme düşen payı (pozitif çarpık sistemde > %100 normal).
   - Çarpıklık ve basıklık.
   - 6 ve 12 aylık yuvarlanan SR; deflated SR.
   - Düşüşün Monte Carlo bandına göre yeri.
   - XU030, USDTRY ve S&P'ye beta ve korelasyon.
   - Piyasada kalma süresi.
   - Rejime göre ayrışma (stres / normal).
6. **Kıyas.** Aynı volatiliteyle (a) para piyasası fonu, (b) XU030 vadelisi, (c) basit 12 aylık trend kuralı. Kol, (b) ve (c)'yi kalıntı alfa olarak geçemiyorsa yaşamayı hak etmez.

---

## 6. Kaynaklar

**Birincil kaynak, bu oturumda okundu [D]:**
- Barber, Lee, Liu, Odean, Cross-Section of Speculator Skill (PDF): https://faculty.haas.berkeley.edu/odean/papers/day%20traders/Day%20Trading%20Skill%20110523.pdf
- Chague, De-Losso, Giovannetti (2019), Day trading for a living?: https://econpapers.repec.org/RePEc:spa:wpaper:2019wpecon47
- Barber, Odean (2000), JF: https://faculty.haas.berkeley.edu/odean/papers%20current%20versions/individual_investor_performance_final.pdf
- SEBI PR 50/2026 (20.08.2026): https://www.sebi.gov.in/sebi_data/attachdocs/aug-2026/1787236407005.pdf ; sayfa: https://www.sebi.gov.in/media-and-notifications/press-releases/aug-2026/sebi-studies-indicate-key-trends-in-retail-participation-trading-behaviour-and-profitability-in-the-equity-derivatives_103838.html
- ESMA (27.03.2018): https://www.esma.europa.eu/press-news/esma-news/esma-agrees-prohibit-binary-options-and-restrict-cfds-protect-retail-investors
- TSPB kaldıraçlı kâr/zarar Excel'i: https://tspb.org.tr/wp-content/uploads/2026/07/1_TSPB-Kar-Zarar-2026-2.xlsx
- Erdem, Arık, Yüksel (MPRA 46804): https://mpra.ub.uni-muenchen.de/46804/1/MPRA_paper_46804.pdf
- McLean, Pontiff (2013 WP): https://ivey.uwo.ca/media/3775549/pontiff.pdf
- Hou, Xue, Zhang: https://www.nber.org/papers/w23394
- Harvey, Liu, Zhu: https://www.nber.org/papers/w20592
- Jensen, Kelly, Pedersen: https://www.nber.org/papers/w28432
- Chen, Velikov (FEDS): https://www.federalreserve.gov/econres/feds/zeroing-in-on-the-expected-returns-of-anomalies.htm
- Novy-Marx, Velikov: https://www.nber.org/papers/w20721
- Falck, Rej, Thesmar: https://arxiv.org/abs/2105.01380
- Daniel, Moskowitz: https://www.nber.org/papers/w20439
- Brunnermeier, Nagel, Pedersen: https://www.nber.org/papers/w14473
- Nagel (2012): https://www.nber.org/papers/w17653
- Coval, Stafford: https://www.nber.org/papers/w11357
- Cohen, Malloy, Pomorski: https://www.nber.org/papers/w16454
- SPK 2025 Faaliyet Raporu: https://spk.gov.tr/data/61e48f651b41c60d1404d687/2025%20Y%C4%B1l%C4%B1%20Faaliyet%20Raporu.pdf
- SPK bültenleri 2026/49-78 (liste): https://spk.gov.tr/spk-bultenleri/2026-yili-spk-bultenleri ; SPK 2025/50: https://spk.gov.tr/data/68d2e4d48f95db1b001b05b2/2025-50.pdf
- Mevduat faizi, Ekim 2026: https://www.endeks24.com/bist-100-iki-ayda-yuzde-25-dustu
- Stopaj oranları 2026: https://parafomo.com/blog/stopaj-nedir-2026-stopaj-oranlari/
- Fed (16.09 ve 28.10.2026): https://www.stephens.com/uploads/shared/documents/PCG-Docs/FOMC-Updates/Fed-Update-9-16-26.pdf ; https://www.federalreserve.gov/monetarypolicy/files/monetary20261028a1.pdf

**Kardeş ajanlardan [A]:**
- USIC: https://completetradersedge.com/wp-content/uploads/2026/09/CTE-Research-Sheet-US-Investing-Championship-2.pdf ; https://finance.yahoo.com/markets/stocks/articles/united-states-investing-championship-nine-121500218.html ; https://www.businesswire.com/news/home/20220124005241/en/2021-United-States-Investing-Championship-Winners-%E2%80%94-Minervini-Smashes-Record
- Kullamägi: https://completetradersedge.com/kristjan-kullamagi-qullamaggie/
- Zanger: https://money.cnn.com/magazines/fortune/fortune_archive/2000/12/18/293117/index.htm
- Bessembinder: https://wpcarey.asu.edu/sites/default/files/2021-10/do-stocks-outperform-treasury-bills.pdf
- Chen-Zimmermann: https://huggingface.co/datasets/OpenSourceAP/CrossSection
- AQR TSMOM: https://www.aqr.com/Insights/Datasets/Time-Series-Momentum-Factors-Monthly
- BIST kriz verileri ve yaptırımlar: `bist_kim_kazaniyor.md` §2.4

**Eğitim bilgisi [EB]:**
- McLean-Pontiff JF 2016 sayıları
- SEBI FY22-24 (%93)
- Barras-Scaillet-Wermers 2010
- Moskowitz-Ooi-Pedersen 2012
- Bailey ve López de Prado (deflated SR, MinTRL)
- VİOP stopajı ve teminat nemalandırma
- SPKn m.107/2 ve m.109 cezaları

## 7. Sınırlamalar
- Web araması hiç yapılamadı. SSRN 403 verdi; Takasbank, GİB ve mevzuat.gov.tr sayfaları zaman aşımına uğradı.
- Simülasyonlarda varsayımlar: GBM, bağımsız işlemler, sabit SR. Gerçekte SR zamanla değişir ve rejime bağlıdır; düşüşler büyük olasılıkla daha kötüdür.
- SEBI ve Tayvan verisi day trading ve opsiyon ağırlıklı. Swing ufku için büyük örneklemli taban oran yok. Yüksek devirli hesapların piyasanın altında kaldığı bulgusu (Barber-Odean, Erdem ve diğ.) yönü destekliyor.
- §5'teki beklenti aralıkları kalibre edilmiş tahminler, ölçüm değil. Yanlışlama testleri bu yüzden var.
