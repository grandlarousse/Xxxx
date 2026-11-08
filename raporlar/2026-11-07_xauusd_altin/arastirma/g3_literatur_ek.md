# g3_literatur_ek — Tablolar (Türkiye literatürü, künye doğrulaması, pratik iddialar)

Tarih: 2026-11-08. Ana rapor ve yöntem notları: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/research/g3_bosluk.md`. Web arama bütçesi bittiği için anahtar kelime araması yapılmadı. Türkçe literatür yalnız atıf zinciri ve DergiPark içindekiler listeleriyle tarandı.

## 2. (A) Türkçe ve Türkiye literatürü

### 2.1 Tablo

| # | Çalışma | Künye / DOI | Sözleşme / piyasa | Örneklem, sıklık | Ufuk | Bulgu (sayılarla) | OOS / maliyet | Zayıflık | Bizim veriyle ilişki |
|---|---|---|---|---|---|---|---|---|---|
| A1 | Karataş Elçiçek (2023) | BERJ 14(3): 369–387, DOI 10.20409/berj.2023.422 | BIST-VİOP "gold futures", kapanış fiyatı (datastore.borsaistanbul.com). Tip yazılmamış; istatistikler **TL gram** ile tutarlı (§2.2) | 02.09.2013–30.11.2022, 2.317 günlük gözlem | 1 gün (takvim kuklaları) | ARMA(2,2)-GARCH(1,1). Perşembeye göre Pzt +0,271% (t 4,20), Sal +0,127% (t 1,81), Çar +0,136% (t 1,89), Cum +0,146% (t 2,08). Kasım'a göre Ocak +0,254% (t 2,56), Mart +0,233% (t 2,61). Sonbahara göre ilkbahar +0,094% (t 2,41), kış +0,099% (t 2,26), yaz anlamsız | Yok / yok | TL serisi kur kaymasını içeriyor. Sürekli seri ve roll yöntemi anlatılmamış. Çoklu test düzeltmesi yok | F_XAUUSD'de Pazartesi getirisi (Cuma girişi) t −1,08, Ocak t +2,03 (IS 0,72, 2026 hariç t 1,07), Mart t −0,03 → **taşınamaz** |
| A2 | Özdemir (2020) | GUSBEED 11(2): 474–483, DOI 10.36362/gumus.683714 | Spot: TCMB "saf altın". Vadeli: investing.com "saf altın vadeli". Birim yok; büyük olasılıkla VİOP TL/gram | 15.03.2013–31.05.2018, günlük. İngilizce özette "02.01.2009" yazıyor; metinle çelişiyor | Günlük gecikmeli VECM | Johansen: 1 eşbütünleşme vektörü. ECM: spot −0,202 (t −5,11), vadeli +0,000132 (t 2,57). Granger: vadeli→spot χ² 143,05 (p 0,0000); spot→vadeli χ² 8,59 (p 0,072). Makale "çift yönlü" diyor | Yok / yok | Eşzamansız fiyatlar (TCMB saati makalede yok). Metin Tablo 6'yı ters okumuş | Bizim baz dönüşü testinde **VİOP spota yakınsıyor** (a2_c2, OOS t −3,08). Yön zıt; araç farklı (ons, Dukascopy 15:00 UTC) |
| A3 | Aksoy (2013) | Muhasebe ve Finansman Dergisi 57: 149–164 (DergiPark üst verisi 149–152 diyor). https://dergipark.org.tr/tr/pub/mufad/article/396163 | İstanbul Altın Borsası altın ve gümüş referans fiyatları. Birim belirtilmemiş | Ağu 2008–Ara 2011, günlük, 853 gözlem | 1 gün | Salıya göre GARCH: Pzt −0,240 (p 0,022), Cum −0,170 (p 0,093). EGARCH: Cum −0,263 (p 0,010). Salı ortalaması +%0,356 | Yok / yok | 3,4 yıl. Kriz dönemi | İlgisiz (spot, 2011 öncesi) |
| A4 | Kırlıoğlu ve Tuna (2013) | Muhasebe ve Denetime Bakış 39: 27–40 | Türkiye altın fiyatları (KE 2023 özetine göre) | Oca 1978–Haz 2012 | Ay / mevsim | Ay ve mevsim etkisi var (ikincil: KE 2023) | ? | **Tam metin erişilemedi** | — |
| A5 | Gümüş ve Durmuşkaya (2015) | Niğde Üniv. İİBF Dergisi 8(1): 43–52 | VOB vadelileri; sözleşme listesi erişilemedi | 2005–2011 | 1 gün | Haftanın günü etkisi yok, hafta sonu etkisi var (ikincil: Özer–Ece 2016) | ? | **Erişilemedi.** DergiPark arşivinde 2015 sayısı ilk iki sayfada yok | — |
| A6 | Özer ve Ece (2016) | Nevşehir HBV Üniv. SBE Dergisi 6(2): 1–14. https://dergipark.org.tr/tr/pub/nevsosbilen/article/260058 | BIST-100 endeks vadeli (altın değil) | Şub 2005–Ağu 2013, 2.143 gün | 1 gün | Cuma ve Çarşamba +, Pazartesi −; Ocak etkisi yok | Yok | — | İlgisiz (altın değil). Türkiye'de vadeli takvim etkisi literatürünün dar olduğunu doğruluyor |
| A7 | Özarı ve Turan (2016) | Uluslararası Sosyal Araştırmalar Dergisi 9(42): 1604–1619 | "VIOB ve BIST" | ? | 1 gün | Haftanın günü ve Ocak | ? | **Erişilemedi** (DergiPark'ta değil) | — |
| A8 | Baklacı, Süer ve Yelkenci (2016) | Emerging Markets Finance and Trade 52(1): 1–9, DOI 10.1080/1540496X.2015.1062292 | Çin, Hindistan, Japonya, Tayvan, **Türkiye**, ABD altın vadelileri | Örneklem ve sıklık **erişilemedi** | — | Örneklemdeki ülkelerin çoğunda oynaklık aktarımı var. Çin görece yalıtılmış. Çeşitlendirme imkânı sınırlı | ? | Türkiye sözleşmesi ve yönü özette yok | "Ons işin %97'si" ile uyumlu |
| A9 | Baklacı, Süer ve Yelkenci (2018; çevrimiçi 2016) | Singapore Economic Review 63(05): 1345–1365, DOI 10.1142/S021759081650020X | 8 gelişmekte olan ülke (Türkiye dahil) + ABD, Japonya | **Erişilemedi** | Johansen/VECM | Uzun dönem fiyat bağımlılığı var. Çin ve Rusya en yalıtılmış | ? | Kısa ufuk bulgusu yok | Uyumlu (VİOP dünya fiyatını izliyor) |
| A10 | Uzuner (2025) | UBEYAD 8(2): 117–152, DOI 10.52736/ubeyad.1783124 | BIST KMP altın, TL/kg ve USD/ons kapanış | 03.01.2017–31.01.2025, günlük, ≈2.014 gözlem | 1–4 gün otokorelasyon | Koşu testi TL/kg: 6 koşu, beklenen 936,14, Z −44,65; USD/ons: 24 koşu, beklenen 1.000,13, Z −485,3; "P değeri 2". ρ1 TL +0,031, USD **−0,140**. USD ρ3 = 0,019 iken t 9,57 yazılmış | Yok | **İç tutarsızlık:** 2.014 gözlemde 6 koşu fiziksel olarak imkânsız; ρ = 0,019 için t ≈ 0,85 olmalı. **Kullanılamaz** | USD/ons ρ1 −0,14 doğruysa KMP kapanışında bayat fiyat ya da alış-satış sıçraması olabilir (§7, H-G3-4) |
| A11 | Cingöz ve Kendirli (2019) | FESA 4(4): 545–554, DOI 10.29106/fesa.649254 | BIST Altın Endeksi, BIST100, USD/TL | 2006:01–2018:06, **aylık ortalama** | Ay | Uzun dönemde eşbütünleşme var; kısa dönemde Granger nedensellik yok | Yok | Aylık ortalama fiyat | İlgisiz (aylık) |
| A12 | Başaran (2026) | Hitit Sosyal Bilimler Dergisi 19(2): 897–918, DOI 10.17218/hititsbd.1863280 | Spekülatif pozisyonlar ↔ reel faiz (küresel) | — | — | CRQA ile doğrusal olmayan bilgi aktarımı | — | Türkiye'ye özgü değil | İlgisiz |

### 2.2 Karataş Elçiçek (2023): sözleşme tipinin kanıtı

Makale sözleşmenin ons/USD mı yoksa gram/TL mi olduğunu yazmıyor. Metinde "gram", "TL", "USD", "ounce" ya da "lira" hiç geçmiyor; yalnız "gold futures contracts traded in BIST-VIOP" deniyor. Tanımlayıcı istatistikler ise ayırt edici:

| Ölçü | Makale (Şekil 1) | TL gram, bizim hesap | Ons/USD, bizim hesap |
|---|---|---|---|
| Ortalama günlük log getiri | **0,001060** | (0,2324 + 2,2231)/2.317 = **0,001060** | 0,2324/2.317 = 0,000100 |
| En düşük günlük | −0,3485 | VİOP XAUTRYM (2017-03–2022-11): −0,356 (21.12.2021) | VİOP XAUUSD: −0,046 (16.03.2020) |
| En yüksek günlük | +0,1451 | +0,148 (10.08.2018) | +0,054 (24.03.2020) |
| Std | 0,0158 | 0,0174 (2017–2022) | 0,0084 |

- **Hesap girdileri:**
  - Ons: Dukascopy XAUUSD 15:00 UTC, 1.392,59 (02.09.2013) → 1.756,87 (30.11.2022); log 0,2324.
  - Kur: TCMB USD döviz alış, 2,0160 → 18,6194; log 2,2231. Kaynak: https://www.tcmb.gov.tr/kurlar/201309/02092013.xml , https://www.tcmb.gov.tr/kurlar/202211/30112022.xml
- **Sonuç:** Örneklemi TL cinsinden gram altın vadeli serisi (yüksek güven). Ons sözleşmesi olsaydı ortalama 10 kat küçük olurdu ve −%35'lik gün olmazdı.
- **Pratik anlam:** Pazartesi, Ocak ve Mart bulguları ons yönünü değil, ons + USDTRY + TL taşıma bileşimini ölçüyor. F_XAUUSD kullanıcısı için **ilgisiz.**
- **Hipotez (test edilmedi):** Pazartesi katsayısı +0,27% üç takvim gününün kur kaymasını ve TL faiz taşımasını yansıtıyor olabilir.

### 2.3 Taranamayan konular (bulunamadı ≠ yok)

Bu konular için atıf zincirinde Türkiye çalışmasına rastlanmadı:

- "Ons altın volatilite yayılımı Borsa İstanbul" (VİOP özelinde)
- "Kıymetli Madenler Piyasası fiyat keşfi"
- "Gram altın Kapalıçarşı primi"
- "VİOP bireysel yatırımcı performansı"
- "VİOP takvim etkisi, ons altın"

Anahtar kelime araması yapılamadığı için yokluk kanıtlanmış değil. Yalnız Türkiye bağlantılı iki not var:

- Karataş Elçiçek'in literatür özeti "Türkçe literatürde altın vadeli getirisinde takvim anomalisine odaklanan çalışma yok" diyor. 2023'e kadar bu boşluğu teyit ediyor.
- Özdemir (2020) "Türkiye altın spot ve vadeli ilişkisini inceleyen çalışmaya rastlanmamıştır" diyor. 2020'ye kadar teyit ediyor.

---

---

## 3. (B) Künye ve bulgu doğrulaması

Durum sütunu: **D** = önceki raporlardaki iddia doğru; **Dz** = düzeltme gerekiyor; **DY** = doğrulanamadı.

| Çalışma | Doğrulanmış künye ve DOI | Örneklem, sıklık | Ufuk | OOS? | Maliyet sonrası? | Bulgunun yönü (özete göre) | Önceki raporlardaki iddia → durum |
|---|---|---|---|---|---|---|---|
| Cai, Cheung ve Wong (2001) | "What moves the gold market?" JFM 21(3): 257–278. DOI 10.1002/1096-9934(200103)21:3<257::AID-FUT4>3.0.CO;2-W | COMEX altın vadeli, gün içi. Dönem özette yok | Gün içi oynaklık | Uygulanamaz (açıklayıcı) | Hayır | 23 ABD duyurusu içinde en büyük oynaklık etkisi: istihdam, GSYH, TÜFE, kişisel gelir. Gün içi desenler arındırılınca uzun hafıza | r5 → **D** |
| Christie-David, Chaudhry ve Koch (2000) | "Do macroeconomics news releases affect gold and silver prices?" J. Economics and Business 52(5): 405–421. DOI 10.1016/S0148-6195(00)00029-1 | **Erişilemedi** | — | — | — | Özet erişilemedi (ScienceDirect 403; Crossref ve Semantic Scholar'da özet yok) | r5 "özet erişilemedi" → **D** |
| Aggarwal ve Lucey (2007) | "Psychological barriers in gold prices?" Review of Financial Economics 16(2): 217–230. DOI 10.1016/j.rfe.2006.04.001. WP: IIIS DP 53 (2005) | Londra AM fix 02.01.1980–31.12.2000 (5.478 gün); COMEX spot ve vadeli 02.01.1982–28.11.2002 (5.255); UBS 15 dakikalık 28.08.2001–09.01.2003 (12.938) | Günlük ve 15 dk | Hayır | Hayır | 100 $'lık seviyelerde (200, 300…) bariyer var. Varyans değişimi "çok güçlü", koşullu ortalama değişimi "bir miktar". Yüksek frekansta kanıt zayıf | Daha önce raporlanmamıştı. Bizim kayıtta **test yok** |
| Pierdzioch, Risse ve Rohloff (2014a) | "On the efficiency of the gold market: Results of a real-time forecasting approach" IRFA 32: 95–108. DOI 10.1016/j.irfa.2014.01.012 | **Özet erişilemedi** | — | (başlığa göre gerçek zamanlı) | ? | — | Görevdeki "IRFA 2014" künyesi **var**; içerik **DY** |
| Pierdzioch, Risse ve Rohloff (2014b) | "The international business cycle and gold-price fluctuations" QREF 54(2): 292–305. DOI 10.1016/j.qref.2014.01.002 | G7 çıktı açıkları | Aylık (özette yok) | Evet, gerçek zamanlı | **Evet** | "Bir miktar" öngörü gücü var. Maliyet sonrası basit kural al-tut'u geçmiyor | r3 → **D** |
| Pierdzioch, Risse ve Rohloff (2015) | "Forecasting gold-price fluctuations: a real-time boosting approach" AEL 22(1): 46–50. DOI 10.1080/13504851.2014.925040 | Enflasyon, kur, hisse getirisi, faiz | — | Evet | Ekonomik değer testi | Öngörücüler güç taşıyor. Ekonomik katkı kuralı al-tut'un üstüne çıkarmaya yetmiyor | r3 → **D** |
| Pierdzioch, Risse ve Rohloff (2016) | "A quantile-boosting approach to forecasting gold returns" NAJEF 35: 38–55. DOI 10.1016/j.najef.2015.10.015 | — | — | Evet | Kural performansı | Kural performansı yatırımcı tipine (iyimser/kötümser kayıp fonksiyonu) göre değişiyor | r3 → **D** |
| Baur (2013) | "The autumn effect of gold" RIBAF 27(1): 1–11. DOI 10.1016/j.ribaf.2012.05.001 | 1980–2010, aylık | Ay | Hayır | Hayır | Pozitif ve anlamlı tek aylar Eylül ve Kasım. Koşulsuz ve risk faktörleri koşullu geçerli. Oynaklık da daha yüksek | r2 → **D** |
| Potrykus ve Augustynowicz (2024) | "The 'autumn effect' in the gold market—does it contradict the Adaptive Market Hypothesis?" IJME 60(3): 157–172. DOI 10.2478/ijme-2024-0011 | Dönem ve sıklık **erişilemedi** | Ay | Yayın sonrası replikasyon | Hayır | "Sonbahar etkisi tersine dönmüş, yerini kış etkisi almış." Platin ve paladyumda Ocak artışı | r2 → **D** (künye ilk kez teyit edildi) |
| Caminschi ve Heaney (2014) | "Fixing a Leaky Fixing: Short-Term Market Reactions to the London PM Gold Price Fixing" JFM 34(11): 1003–1039. DOI 10.1002/fut.21636 | GC vadeli ve GLD, dakikalık. Eski telefonlu fiks | Dakika | Hayır | "Ekonomik getiri var" deniyor | Fiks başladıktan sonraki 4 dakikada bilgili işlemcilere getiri avantajı. Açılış dakikalarındaki işlemler fiks yönünü "bazı durumlarda %90'ın üzerinde" öngörüyor. Sonuç yayımından sonra etki yok | r2'nin %47,8 / %69,9 / %80 sayıları özette yok → **DY** (r5 de not etmişti) |
| Hauptfleisch, Putniņš ve Lucey (2016) | "Who Sets the Price of Gold? London or New York" JFM 36(6): 564–586. DOI 10.1002/fut.21775 | 17 yıl, gün içi | Gün içi | Uygulanamaz | Hayır | İki piyasa da katkı yapıyor; NY vadeli **ortalamada** daha büyük pay alıyor. NY hacmi Londra spotunun onda birinden az. Pay gün içinde ve yıllar arasında değişiyor. Platform yükseltmesi gürültüyü azaltmış | r2/r5 → **D**. Sayısal paylar **DY** |
| Blose ve Gondhalekar (2014) | **"Overnight gold returns"** AEL 21(18): 1269–1272. DOI 10.1080/13504851.2014.922661 | COMEX ön ay 1985–2012; GLD | Gece / gündüz | Hayır | Hayır | Gece getirisi anlamlı pozitif, gündüz anlamlı negatif. GLD'de gece > gündüz. Asimetri "belirgin şekilde zayıflamış ama sürüyor" | r2/r5 → **D** (başlık eklendi) |
| Pavabutr ve Chaihetphon (2010) | "Price discovery in the Indian gold futures market" J. Economics and Finance 34(4): 455–467 (çevrimiçi 14.11.2008). DOI 10.1007/s12197-008-9068-9 | MCX. Anahtar kelimeler: Gold Futures, Price Discovery, Information Share | — | — | — | **Özet erişilemedi** (Springer kimlik duvarı) | r5 → **D** (erişilemedi) |
| Xu ve Fung (2005) | "Cross-market linkages between U.S. and Japanese precious metals futures trading" JIFMIM 15(2): 107–124. DOI 10.1016/j.intfin.2004.03.002 | ABD–TOCOM | — | — | — | **Özet erişilemedi** | r5 → **D** (erişilemedi) |
| Hassani, Silva, Gupta ve Segnon (2015) | "Forecasting the price of gold" Applied Economics 47(39): 4141–4152. DOI 10.1080/00036846.2015.1026580 | Aylık; 17 yöntem, 9'u raporlanmış | 1, 9 adım; 24 ay | Evet | Hayır | 1 ve 9 adım ileride **hiçbir yöntem rastgele yürüyüşü yenmiyor**. 24 aylık ufukta ortalamada en iyisi üstel düzleştirme. Tek değişkenli modeller BAR/BVAR'ı yeniyor | r3 → **D** (artık dergi özetiyle) |
| Aye, Gupta, Hammoudeh ve Kim (2015) | "Forecasting the price of gold using dynamic model averaging" IRFA 41: 257–266. DOI 10.1016/j.irfa.2015.03.010 | Aylık; IS 1992:02–1999:09, OOS 1999:10–2013:11 | 1–12 ay | Evet | Hayır | DMA/DMS rastgele yürüyüşü ve BMA'yı yeniyor; DMS en iyisi. **Döviz kuru faktörü** en baskın; KC Fed stres endeksi de güçlü | r3 → **D** |
| Gupta, Karmakar ve Pierdzioch (2024) | "Safe Havens, Machine Learning, and the Sources of Geopolitical Risk: A Forecasting Analysis Using Over a Century of Data" Comput. Econ. 64(1): 487–513 (çevrimiçi 17.08.2023). DOI 10.1007/s10614-023-10452-w | 1915–2021, aylık; 39 ülke kaynağı | Aylık | Evet | Hayır | Ülke düzeyinde jeopolitik risk **sonraki altın oynaklığının** tahminini iyileştiriyor, özellikle random forest ile. **Getiri değil** | r3 "getiri ve volatilite" → **Dz: yalnız oynaklık** |
| Lucey ve O'Connor (2017; çevrimiçi 2016) | "Are gold bugs coherent?" AEL 24(2): 90–94. DOI 10.1080/13504851.2016.1164813 | CXO'ya göre: Oca 1998–Kas 2015, günlük, NYSE Arca Gold Bugs (HUI) ve COMEX 100 ons vadeli | Dalgacık ölçekleri | Hayır | İşlem testi yok | Kısa vadede az ilişki, uzun vadede anlamlı ve kalıcı. "Altın, madenci hisselerine öncülük ediyor gibi". CXO: "çoğunlukla en az bir hafta önde"; bir yıl ve üzeri ölçekte daha güvenilir | r2'deki "en az bir hafta" → **D, ama yalnız ikincil kaynakta**. Özet bunu söylemiyor |
| Caporale ve Plastun (2020 WP; 2021) | CESifo WP 8445 (Temmuz 2020); FMPM 35(3): 353–368 (2021). DOI 10.1007/s11408-021-00380-w | 01.01.2009–31.03.2020, günlük ve saatlik, MetaQuotes, GMT+3 | 1 gün | Hayır (tam örneklem eşiği) | Hayır | **Getiri tanımı açılıştan kapanışa:** R = (Close/Open − 1)×100. Anormal gün eşiği: ortalama + k×σ (dinamik tetik). Aynı gün momentum (Strateji 1): pozitif şokta t 5,61 (59 işlem, %86 isabet), negatif şokta t 8,17 (74 işlem, %72). Ertesi gün karşıt (Strateji 2): t 1,36 ve 0,73, anlamsız | r2 → **D**. Strateji 1 gün içi tespite dayanıyor; uzlaşmadan uzlaşmaya taşınamaz |

**Rastlantısal bulgu (okunmadı):** Smales, O'Grady ve Yang (2015), "Examining the impact of macroeconomic announcements on gold futures in a VAR-GARCH framework", AEL 22(9): 710–716, DOI 10.1080/13504851.2014.972538. r5'teki "Smales (2015) aşırı tepki" atfı bu makale olabilir; doğrulanmadı.

---

---

## 4. (C) Türkiye'de dolaşan pratik iddialar ve bizim testler

Etiket, bizim ana bulgularımıza göre veriliyor: LOWMOM, GDXJ artığı, NFP, S2 gece etkisi, baz dönüşü. "destekler" = iddia bulgumuzla aynı yönde; "çelişir" = ters ya da kenar yok; "ilgisiz" = farklı araç ya da ölçek; "test edilmedi".

| # | İddia | Kaynak | Bizim test (kayıt) ve sayı | Etiket | Not |
|---|---|---|---|---|---|
| C1 | Kısa hareketli ortalamalar (5/10/20/50 gün), RSI, Stoch, MACD, CCI tabloları ALIM/SATIM veriyor. Pivot destek/direnç seviyeleri. Örnek 04.11.2026, XAU/USD: dört HO de SATIM, RSI SATIM, StochS ALIM, MACD SATIM, CCI ALIM. F_XAUUSD1226: D1 3.919,80 / Pivot 3.959,90 / R1 3.992,90 | Gedik VİOP Günlük Bülten 04.11.2026 | A1-TREND-MA50 (P > SMA50 uzun, 1 gün): IS t −0,72, OOS +1,82. Yıl ortalaması çıkarınca Sharpe 0,03 → YOK. rsi14_lo\|vt1\|h5: t 2,93 (IS 1,63, OOS 2,66; son listede yok). Pivot: kayıtta yok | **çelişir** (koşulsuz trend). LOWMOM ile **kısmen ilgili** | LOWMOM yalnız düşük oynaklıkta 5 günlük momentum. Koşulsuz HO sinyalinin kenarı yok. Pivot test edilmedi |
| C2 | "Olası oynaklığa karşı aktif kâr al / zarar durdur"; takvim: ECB/BoE kararları, ABD TÜFE, haftalık işsizlik başvuruları, Fed konuşmaları | Gedik VİOP gün ortası 18.12.2025 (gram altın) | Sentez risk_stop: VİOP 2σ stop, 1 gün nakit: Sharpe 0,60 (al-tut 0,57). 3σ, 1 gün: 0,67, yıllık +1,47 puan. 2σ, 5 gün: 0,50. A3 NFP tepkisi: NFP_cond_13to15_h1 t 3,68 (IS 1,41, OOS 3,93); CPI_pre_h1 t 2,56 (IS 4,25, OOS 0,35) | NFP için **destekler** (olay günü bilgi var). Stop için **ilgisiz/zayıf** | Stop kuralı ±1–2 puan yıllık; kenar değil, risk aracı |
| C3 | Akşam seansında (19:00–23:00 TSİ) FOMC'ye ve ABD öğleden sonrasına canlı tepki | r1 §, r6 §4.4; BIST 30572 | a3 FOMC_post_F+1_h3 t −1,50; FOMC_pre_F-5_h5 t −1,77; FOMC_cond_close_h1 t −1,77 → yön YOK. VOL_FOMC t 4,23 (oynaklık ↑). a2_c1_S2_gece: akşam kapanışında uzun, sabah çık; ~3 bp/gün brüt, IS t 3,6, OOS t 4,57, gerçekçi maliyetle ≈ 0 | Yön için **çelişir**. Oynaklık ve S2 drift için **destekler**, ama ekonomik değil | Akşam seansı bir risk ayarlama aracı; kâr kaynağı değil |
| C4 | Gram–ons makası (yurt içi sentetik prim) açılınca kapanır | Kuyumcu/arbitraj pratiği (r4 §5, §7); Özdemir 2020'nin dolaylı sonucu | a7_C3_gram_prim_donus: prim_sapma_t-1 → 5 günlük Δprim t −6,85 (IS −4,19, OOS −5,59), 3 gün t −6,10. Kural (z > 1, 3 bacak, 15 bp): IS t −2,93, OOS −5,79, OOS Sharpe −0,77 | Baz dönüşüyle **destekler** (istatistik). Net kâr için **çelişir** | Dönüş gerçek; makas ve üç bacak maliyeti kazancı yiyor. Fırsat piyasa yapıcıların |
| C5 | Bayram öncesi altın al / bayram sonrası düzeltme | Yaygın perakende söylem (birincil aracı kurum notu **bulunamadı**) | a3 BAYRAM_post_h5, düzeltilmiş (2017-03-06 sahte olay çıkarılmış): 20 olay, fark −94,6 bp, t_NW −2,94 (IS −2,10, OOS −2,08), isabet %30, 8/10 yıl aynı işaret. 2010–2016 spotta +70,3 bp (t 1,53), **ters**. BAYRAM_pre_h5 −62,2 bp (t −1,24). Son karar: YOK | **çelişir** (alım iddiasına). Kısa tarafı istikrarsız | 20 olay, mekanizma yok. Erken dönemde ters işaret |
| C6 | Kapalıçarşı makası/primi: iskontoda fiziki al, primde sat | r4 §7 (WGC, basın) | Test **yok**: Kapalıçarşı zaman serisi elimizde değil | **test edilmedi** | r4: makas ≈ %3,5 (Mayıs 2026, düşük güven) |
| C7 | Altın sertifikası / BYF primi yüksekken alma | Gedik "Altın sertifikası tavsiye raporu" (22.04.2025, 23.09.2025; PDF **erişilemedi**). QNB KAP 02.02.2026 GLDTR NAV uyarısı (m1) | E3-5_GLDTR_prim: prim üst %20'deyken BYF yerine VİOP/ETF seç; h1 −18 bp, OOS t −3,85. Veri kusurlu (kış barları eksik), 3 yıl, IS yok | **ilgisiz** (F_XAUUSD'ye değil, araç seçimine dair). Yönü destekler | Uygulama: GLDTR'de NAV'a bak, VİOP'ta prim sorunu yok |
| C8 | Haftanın günü: Pazartesi kazandırır (KE 2023); Pazartesi kaybettirir (Aksoy 2013, Lucey–Tully) | Akademik, Türkiye | DOW_entry_Cum_h1 (Pazartesi getirisi) t −1,08 (IS −0,91, OOS −0,71). DOW_entry_Pzt_h1 t −0,26. a2 e_dow_Pzt t −1,51 | **ilgisiz/çelişir** | F_XAUUSD'de haftanın günü etkisi yok |
| C9 | Ocak ve Mart pozitif (KE 2023); Eylül ve Kasım pozitif (Baur 2013); kış pozitif (Potrykus–Augustynowicz 2024) | Akademik | MONTH_Oca_h1 t 2,03 (IS 0,72, OOS 2,00; 2026 hariç 1,07). MONTH_Mar t −0,03. MONTH_SepNov t −1,48 (IS −2,57, OOS 0,13). MONTH_Winter t 1,58 (IS 0,86, OOS 1,33). MONTH_Haz t −2,20 | Ocak ve kış için **zayıf destek**. Baur ve Mart için **çelişir** | 12 ay × 1 test; FDR'de hiçbiri geçmiyor |
| C10 | TL şoku/kriz günlerinde ons al (ya da sat) | Perakende söylem | a7_C5_TR_sok: TL şoku ya da XU030 < −%5 gününde ons kısa, 3 gün: −48 bp/olay, IS t −2,29, OOS t −1,48. Kümelemeden sonra anlamsız, ≈30 bağımsız epizot | **ilgisiz** | Ons, TL şokuna kalıcı tepki vermiyor |
| C11 | "VİOP vadeli spotun önünden gider" (fiyat keşfi vadelide) | Özdemir 2020 (TL gram–TCMB) | a5_yetisme_YOK (makroya eksik tepki → yetişme): IS t −2,21, OOS −0,98, işaret ters. a2_c2_baz_donus: eb üst tercil → VİOP kısa + spot uzun, h5; IS t −1,9, OOS t −3,08; fonlama sonrası ≈ 0 | **çelişir** | Bizde VİOP, 15:00 UTC spota yakınsıyor; VİOP bilgi üretmiyor |
| C12 | Altın madencileri altını izler (madenciye altından bak) | Lucey–O'Connor 2017 (uluslararası) | A4-C1_GDXJ_artik_h3: GDXJ artığı → VİOP 3 gün; IS t 2,53, OOS t 2,63; kural P&L tam t 1,64. E2-C1 madenci öncü → GLD h5: IS 3,46, OOS 1,94 | Kısa ölçekte **çelişir** (bizde madenci artığı öncü) | Farklı ölçek. L–O'C kısa vadede ilişki az diyor |
| C13 | Gece (Asya/akşam) altın yükselir, gündüz düşer | Blose–Gondhalekar 2014 | a2 b_mean_S2_late t 6,59 (IS 3,60, OOS 4,57). e1 GDXJ gece–gün içi t 5,42 | **destekler** (S2 gece etkisi). Ekonomik değil | Maliyet ≈ 5 bp; kenar ≈ 3 bp |

---

---

## 9. Kaynaklar

**Türkiye**
- Karataş Elçiçek 2023: https://econpapers.repec.org/RePEc:ris:buecrj:0643 ; PDF https://www.berjournal.com/?file_id=883 ; DOI 10.20409/berj.2023.422
- Özdemir 2020: https://dergipark.org.tr/tr/pub/gumus/article/683714 ; PDF https://dergipark.org.tr/tr/download/article-file/1171668 ; DOI 10.36362/gumus.683714
- Aksoy 2013: https://dergipark.org.tr/tr/pub/mufad/article/396163 ; PDF https://dergipark.org.tr/tr/download/article-file/427032
- Özer ve Ece 2016: https://dergipark.org.tr/tr/pub/nevsosbilen/article/260058
- Cingöz ve Kendirli 2019: https://dergipark.org.tr/tr/pub/fesa/article/649254 ; DOI 10.29106/fesa.649254
- Uzuner 2025: https://dergipark.org.tr/tr/pub/ubeyad/article/1783124 ; DOI 10.52736/ubeyad.1783124
- Başaran 2026: https://dergipark.org.tr/tr/pub/hititsbd/article/1863280 ; DOI 10.17218/hititsbd.1863280
- Baklacı, Süer ve Yelkenci 2016: https://econpapers.repec.org/RePEc:mes:emfitr:v:52:y:2016:i:1:p:1-9 ; DOI 10.1080/1540496X.2015.1062292
- Baklacı, Süer ve Yelkenci 2018: https://econpapers.repec.org/RePEc:wsi:serxxx:v:63:y:2018:i:05:n:s021759081650020x ; DOI 10.1142/S021759081650020X
- Korkmaz, Çevik ve Uygurtürk 2017 (altın değil, BIST30): https://dergipark.org.tr/tr/pub/hititsosbil/article/305741
- TCMB kurları: https://www.tcmb.gov.tr/kurlar/201309/02092013.xml ; https://www.tcmb.gov.tr/kurlar/202211/30112022.xml

**Uluslararası** (EconPapers sayfası ve DOI)
- Cai vd. 2001: https://econpapers.repec.org/RePEc:wly:jfutmk:v:21:y:2001:i:3:p:257-278
- Christie-David vd. 2000: https://econpapers.repec.org/RePEc:eee:jebusi:v:52:y:2000:i:5:p:405-421 ; DOI 10.1016/S0148-6195(00)00029-1
- Aggarwal ve Lucey 2007: https://econpapers.repec.org/RePEc:wly:revfec:v:16:y:2007:i:2:p:217-230 ; WP https://www.tcd.ie/triss/assets/PDFs/iiis/iiisdp53.pdf ; DOI 10.1016/j.rfe.2006.04.001
- Pierdzioch vd.: IRFA 2014 DOI 10.1016/j.irfa.2014.01.012 ; QREF 2014 https://econpapers.repec.org/RePEc:eee:quaeco:v:54:y:2014:i:2:p:292-305 ; AEL 2015 https://econpapers.repec.org/RePEc:taf:apeclt:v:22:y:2015:i:1:p:46-50 ; NAJEF 2016 https://econpapers.repec.org/RePEc:eee:ecofin:v:35:y:2016:i:c:p:38-55 ; yazar listesi https://econpapers.repec.org/RAS/ppi123.htm
- Baur 2013: https://econpapers.repec.org/RePEc:eee:riibaf:v:27:y:2013:i:1:p:1-11 ; DOI 10.1016/j.ribaf.2012.05.001
- Potrykus ve Augustynowicz 2024: DOI 10.2478/ijme-2024-0011 (Crossref özeti) ; https://reference-global.com/article/10.2478/ijme-2024-0011
- Caminschi ve Heaney 2014: https://econpapers.repec.org/RePEc:wly:jfutmk:v:34:y:2014:i:11:p:1003-1039 ; DOI 10.1002/fut.21636
- Hauptfleisch vd. 2016: https://econpapers.repec.org/RePEc:wly:jfutmk:v:36:y:2016:i:6:p:564-586 ; DOI 10.1002/fut.21775
- Blose ve Gondhalekar 2014: https://econpapers.repec.org/RePEc:taf:apeclt:v:21:y:2014:i:18:p:1269-1272 ; DOI 10.1080/13504851.2014.922661
- Pavabutr ve Chaihetphon 2010: https://econpapers.repec.org/RePEc:spr:jecfin:v:34:y:2010:i:4:p:455-467 ; DOI 10.1007/s12197-008-9068-9
- Xu ve Fung 2005: https://econpapers.repec.org/RePEc:eee:intfin:v:15:y:2005:i:2:p:107-124 ; DOI 10.1016/j.intfin.2004.03.002
- Hassani vd. 2015: https://econpapers.repec.org/RePEc:taf:applec:v:47:y:2015:i:39:p:4141-4152 ; DOI 10.1080/00036846.2015.1026580
- Aye vd. 2015: https://econpapers.repec.org/RePEc:eee:finana:v:41:y:2015:i:c:p:257-266 ; DOI 10.1016/j.irfa.2015.03.010
- Gupta, Karmakar ve Pierdzioch 2024: DOI 10.1007/s10614-023-10452-w (Crossref özeti)
- Lucey ve O'Connor 2017: https://econpapers.repec.org/RePEc:taf:apeclt:v:24:y:2017:i:2:p:90-94 ; DOI 10.1080/13504851.2016.1164813 ; ikincil https://www.cxoadvisory.com/gold/gold-futures-vs-gold-miner-stocks/
- Caporale ve Plastun: https://econpapers.repec.org/RePEc:ces:ceswps:_8445 ; PDF https://www.ifo.de/DocDL/cesifo1_wp8445.pdf ; FMPM DOI 10.1007/s11408-021-00380-w
- Smales, O'Grady ve Yang 2015 (okunmadı): DOI 10.1080/13504851.2014.972538

**Pratik / aracı kurum**
- Gedik VİOP Günlük Bülten 04.11.2026: https://cdn.gedik.com/cdn/bulletin/2026/11/04/VIOP_Bulten_04112026_c2ab774d.pdf
- Gedik VİOP gün ortası 18.12.2025: https://cdn.gedik.com/media/media/ttljweyg/viopgunortasi_18122025.pdf
- Gedik altın sayfası: https://gedik.com/altin ; tavsiye raporu sayfası (PDF erişilemedi): https://gedik.com/yurt-ici-piyasa-bultenleri/makro-gorunum-raporlari/makro-not-altin-sertifikasi-tavsiye-raporu-23092025
- BIST duyurusu 30572: https://borsaistanbul.com/files/duyuru-30572-TR.pdf
- Bizim kayıt: `out/registry/*.csv`, `out/sentez/sinyal_tablosu.csv`, `out/sentez/risk_stop.csv`, `out/a3_takvim_olay_adv/log_adv3_diger.txt` (BAYRAM düzeltmesi), `out/a3_takvim_olay_rep/log_r2.txt`
