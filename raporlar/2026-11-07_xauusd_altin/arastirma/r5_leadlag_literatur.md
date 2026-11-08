# r5_leadlag_literatur — Altında öncülük-gecikme (lead-lag) ve fiyat keşfi literatürü, VİOP F_XAUUSD için test edilecek hipotezler

Tarih: 2026-11-07. Türkiye kalıcı UTC+3 (TSİ). Hedef: VİOP F_XAUUSD günlük uzlaşmasından (15:00–15:10 UTC VWAP) sonraki 1, 3 ve 5 günlük uzlaşmadan uzlaşmaya getiri.

**Yöntem ve sınırlama (önce okuyun).** Bu ajan başladığında oturumun ortak web arama bütçesi (200 arama) tükenmişti. Bu yüzden **hiç anahtar kelime araması yapılamadı.** Literatür şu yollarla doğrulandı:
- (a) Bilinen makalelerin birincil bibliyografik sayfaları doğrudan WebFetch ile okundu: EconPapers/RePEc, IDEAS, NBER, Crossref DOI kaydı, yazar kurum deposu. Yalnız özet (abstract) düzeyinde doğrulama yapıldı. Özetinde olmayan sayı yazılmadı.
- (b) Aynı oturumdaki önceki raporlar (r1–r4) ve analiz ajanlarının kayıtları (`out/registry/*.csv`) kullanıldı. Bunlardan alınan iddialar "(r1)", "(r2)" vb. ile işaretlendi.
- (c) Senkronsuzluk tuzağının büyüklüğünü kendi kısa hesabımla ölçtüm: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/r5_leadlag_literatur/nonsync_demo.py`.

Özeti okunamayan makaleler "özet erişilemedi" diye işaretlendi; bulgu uydurulmadı. Türk akademik literatürü (DergiPark) arama yapılamadığı için **taranamadı.**

---

## 0. Kısa özet

1. **Fiyat keşfi Londra–New York:** Hauptfleisch, Putniņš ve Lucey (2016, JFM 36(6): 564–586) 17 yıllık gün içi veriyle iki piyasanın da fiyat keşfine katkı yaptığını buluyor. New York vadelisinin hacmi Londra spotunun onda birinden az, ama payı **ortalamada** daha büyük. Pay gün içinde ve yıllar arasında değişiyor; değişimi likidite, gün ışığı saatleri ve makro duyurular açıklıyor. Lucey, Larkin ve O'Connor (2013, AEL 20(8)) 25 yılı 4 aylık pencerelerle inceliyor; liderlik iki piyasa arasında el değiştiriyor ve "hiçbiri baskın değil".
2. **Çin:** Jin, Li, Wang ve Yang (2018, JFM 38(10)): Çin içinde fiyat keşfi ağırlıkla **vadeli piyasada** (SHFE) oluyor. Bu sonuç bilgi payı, bileşen payı ve bilgi liderliği payı ölçülerinin üçünde de ve üç seansın hepsinde geçerli. Fiyat keşfi gece seansında daha güçlü. Lucey, Larkin ve O'Connor (2014, AEL 21(13)) Diebold–Yılmaz yayılım endeksiyle Şanghay'ı "yalıtılmış" buluyor; en güçlü bağlı çift Londra spot ile COMEX.
3. **ETF:** Ivanov (2013, JEF 37(3)) gün içi veriyle, altın ve gümüşte fiyat keşfinin ETF'lerin gelişiyle **ETF piyasasına kaydığını** buluyor. Petrolde fiyat keşfi hâlâ vadelide.
4. **Hindistan (MCX) ve Tokyo (TOCOM):** Pavabutr ve Chaihetphon (2010, JEF 34(4)) ile Xu ve Fung (2005, JIFMIM 15(2)) mevcut, ama özetlerine erişilemedi. Bulguları **raporlanmıyor.**
5. **VİOP:** VİOP ile spot/uluslararası fiyat arasında fiyat keşfi çalışan bir yayın **bulunamadı** (arama yapılamadı). Bizim veri VİOP'un saf bir **fiyat alıcısı (uydu piyasa)** olduğunu gösteriyor:
   - Günlük getiri korelasyonu 0,977, beta 0,98 (a7).
   - Uzlaşma, spotun 15:00 UTC değerine yalnız taşıma maliyeti kadar uzak (r1).
   - VİOP–spot baz sapması ertesi gün mekanik olarak kapanıyor: t ≈ −25 (a2).
6. **Varlıklar arası, ana ilke:** Ferraro, Rogoff ve Rossi (2015, JIMF 54) günlük sıklıkta emtia–kur ilişkisinin **eşzamanlı** değişimle sağlam olduğunu buluyor. **Gecikmeli** değişimle öngörü gücü "geçici" ve ancak istikrarsızlık modellenince görülüyor. Altında da tablo aynı: dolar, reel faiz, hisse, petrol ve gümüş ilişkileri eşzamanlı olarak güçlü, günlük gecikmeli olarak zayıf ya da yok.
7. **Gümüş:** Baur ve Tran (2014, Empirical Economics 47(4)), 1970–2011: altın ile gümüş eşbütünleşik ve **ilişkiyi altın sürüyor**. Gümüşün altına öncülük ettiğine dair kanıt yok.
8. **Madenciler:** Lucey ve O'Connor (2017, AEL 24(2)) dalgacık analiziyle kısa vadede zayıf, uzun vadede güçlü ilişki buluyor ve **altın madencilere öncülük ediyor.** Bizim kayıtta ters yönde bir iz var: GDXJ'nin GLD'ye göre beta-artığı VİOP 3 günlük getirisini öngörüyor (IC 0,068, t 3,53, IS t 2,53, OOS t 2,63; global FDR'ı geçmiyor, q 0,43; a4).
9. **Dolar:** Reboredo (2013, JBF 37(8)) kopula modeliyle altın ile dolar değer kaybı arasında ortalamada pozitif ve anlamlı, kuyruklarda simetrik bağımlılık buluyor. Pukthuanthong ve Roll (2011, JBF 35(8)): altın her para biriminde o paranın değer kaybıyla ilişkili. Sjaastad (2008): altın piyasasına dolar bloku hâkim. Bunların hiçbiri günlük gecikmeli öngörü değil.
10. **Emtia paraları:** Chen, Rogoff ve Rossi (2010, QJE 125(3)): emtia ihracatçısı ülkelerin kurları **küresel emtia fiyat endekslerini** örneklem içi ve dışında öngörüyor. Ters yön daha zayıf. Apergis (2014, IREF 29), 2000–2012 günlük nominal veride yön tersine: **altın AUD'yi** örneklem dışında öngörüyor.
11. **Petrol:** Zhang ve Wei (2010, Resources Policy 35(3)), Ocak 2000–Mart 2008:
    - Petrol değişimleri altın oynaklığını doğrusal olarak Granger-nedenliyor, tersi yok.
    - Fiyat keşfi payı PT modelinde petrol %86,50 / altın %13,50, IS modelinde %50,28 / %49,72.
    - Seviye korelasyonu 0,9295.
    - 2026'da haftalık altın–Brent korelasyonu −0,31'e döndü (r3), yani ilişki rejime bağlı.
12. **Hisse/VIX:** Baur ve Lucey (2010): altın uç hisse düşüşlerinde güvenli liman, ama yalnız ~15 işlem günü (r3). Hood ve Malik (2013, RFE 22(2)), Kasım 1995–Kasım 2010 günlük ABD verisi: altın zayıf bir güvenli liman. Oynaklığın çok düşük ya da çok yüksek olduğu dönemlerde altın–hisse korelasyonu negatif değil. Bu dönemde VIX daha iyi bir hedge.
13. **Bitcoin:** Klein, Pham Thu ve Walther (2018, IRFA 59): Bitcoin düşen piyasalarla pozitif korelasyonlu, altının tersi. Bouri ve ark. (2018), 17.07.2010–02.02.2017 günlük veri: altın ve emtia endeksi **Bitcoin'i** öngörüyor (asimetrik, kantile bağlı). Bitcoin'den altına öncülük kanıtı **bulunamadı.**
14. **Akış ve konum:**
    - ETF akışları büyük ölçüde fiyatı **izliyor**. Deutsche Bank'ın Granger testi (ikincil aktarım) ve bir Aalto tezi böyle diyor (r2).
    - COT pozisyonları için de aynı: bir PolyU tezine göre pozisyonlar getiriye tepki veriyor (r3).
    - Altın için COT'un hakemli, örneklem dışı ve maliyet sonrası öngörü gücü **bulunamadı.**
    - Şanghay primi "mütevazı" öngörücü (Meader, LBMA Alchemist 83; r2/r3).
15. **Gün içi zaman yapısı:**
    - Blose ve Gondhalekar (2014, AEL 21(18)), COMEX 1985–2012: gece getirisi anlamlı pozitif, gündüz anlamlı negatif. Asimetri zamanla "belirgin şekilde zayıflamış ama sürüyor".
    - Caminschi ve Heaney (2014, JFM 34(11)): eski telefonlu LBMA PM fiksinginde bilgi sızıntısı. Fiksing başladıktan sonraki 4 dakikada bilgili işlemciler anlamlı getiri elde ediyor; açılış dakikalarındaki işlemler fiksingin yönünü bazı durumlarda %90'ın üzerinde isabetle öngörüyor. Sonuç yayımlandıktan sonra etki yok.
    - Bizim veride t-1 20:00 → t 00:00 UTC penceresinin ortalaması günde +2,9 bps (t 6,6; IS t 3,6; OOS t 4,6; 17 yılın 15'inde pozitif; a2).
16. **Senkronsuzluk tuzağı (kendi ölçümüm, 2017–2026, n = 2.358):** Uzlaşmadan **sonra** oluşan bilgiyi "önceki gün" diye etiketlemek sahte öncülük üretiyor.
    - Gün t'nin 15:00→20:00 UTC spot hareketi ile t→t+1 uzlaşma getirisi arasında korelasyon **0,424** (R² %18, beta 0,92).
    - COMEX'in aynı gün kapanıştan kapanışa getirisi için korelasyon **0,191**.
    - ABD 10 yıllık getirisinin aynı gün değişimi için **−0,089**.
    - Doğru gecikmeli sürümlerde değerler −0,028 / −0,014 civarına iniyor.
    - Bu "öncülükler" uzlaşmada işlemle **kullanılamaz.**
17. **Sonuç:** Literatürde VİOP'un 15:10 UTC kapanışından sonraki 1–5 günü güçlü biçimde öngören gecikmeli bir değişken yok. Test edilmeye değer adaylar şunlar:
    - ABD kapanışı sonrası ve Asya açılışı penceresinin pozitif sürüklenmesi.
    - Madenci göreli gücü.
    - Düşük oynaklıkta momentum.
    - Uzlaşmadan önce gelen ABD verisi günlerinde 13:00–15:00 UTC hareketinin devamı.
    - Şanghay primi.
    - Asya hisse kapanışları.
    - Uzlaşmadan sonraki olaylar (FOMC) ile oynaklık koşullu kurallar.

    Bölüm 9'da 36 somut hipotez ve 3 plasebo kontrolü var.

---

## 1. VİOP zaman çizelgesi ve seans doğrulaması

**Seans ve uzlaşma (r1, Borsa İstanbul VİOP Prosedürü rev. 70, 01/07/2026):**
- Normal seans 09:30–18:10 TSİ (06:30–15:10 UTC).
- Günlük uzlaşma = seans bitmeden önceki son 10 dakikanın miktar ağırlıklı ortalaması, yani **15:00–15:10 UTC**.
- Yarım günlerde 09:30–09:40 UTC. Yarım günlerde 15:00 UTC bilgisiyle kurulan her sinyal ileriye bakar; xau 07→15 momentumunun fwd1 ile korelasyonu yarım günlerde +0,55 (a7). Yarım günler dışlanmalı.
- Ortak `DATA_README.md` eski kaynağa (İşbank 2024) dayanarak 18:15 / 15:05–15:15 UTC yazıyor. Güncel Prosedür 18:10 diyor. Fark 5 dakika, sonuçları değiştirmez.

**Akşam seansı: DOĞRULANDI.**
- Borsa İstanbul duyurusu 30572 (19.11.2024) aslında **bakır** vadelisinin işleme açılmasıyla ilgili.
- Ekindeki VİOP Prosedürü md. 7 "Akşam Seansına Dahil Olan Sözleşmeler" hem mevcut hem revize metinde "Dolar/Ons Altın" diyor. Aynı ekte "Akşam seansında işlem gören sözleşmelerin baz fiyatı, normal seans sonunda hesaplanan uzlaşma fiyatıdır" ifadesi var. Bunları yerel kopyadan kendim okudum: `research/pdf_bist/d30572.pdf`. https://borsaistanbul.com/files/duyuru-30572-TR.pdf
- Saat **19:00–23:00 TSİ (16:00–20:00 UTC)** 30572'nin metninde geçmiyor. Kaynağı Prosedür Ek-3(B) (r1).
- Ons altında akşam seansı 18.09.2020'de başladı (BIST duyuru 12590; r2).
- Akşam seansı uzlaşmaya girmez (r1).

**Uzlaşmaya göre olay saatleri (UTC; r1, r2, r3):**

| Olay | Kış (GMT/EST) | Yaz (BST/EDT) | VİOP uzlaşmasına göre |
|---|---|---|---|
| SGE gündüz seansı / benchmark | 01:00–07:30 / 02:15 ve 06:15 | aynı (Çin'de yaz saati yok) | Önce |
| SHFE gündüz kapanışı | 07:00 | 07:00 | Önce |
| Nikkei, KOSPI / Şanghay / Hang Seng / NSE kapanışı | 06:30 / 07:00 / 08:10 / 10:00 | aynı | Önce |
| LBMA Gold AM (10:30 Londra) | 10:30 | 09:30 | Önce |
| SGE/SHFE gece seansı başlangıcı | 12:00 / 13:00 | aynı | Uzlaşmayla örtüşür ve sonrasına taşar |
| ABD 08:30 ET verileri | 13:30 | 12:30 | Önce |
| **LBMA Gold PM (15:00 Londra)** | **15:00 = uzlaşma penceresinin başı** | 14:00 | Kışın eşzamanlı, yazın 1 saat önce |
| **VİOP uzlaşması** | **15:00–15:10** | **15:00–15:10** | — |
| VİOP akşam seansı | 16:00–20:00 | 16:00–20:00 | Sonra |
| COMEX GC uzlaşması (13:29–13:30 ET) | 18:29–18:30 | 17:29–17:30 | Sonra |
| FOMC kararı (14:00 ET) | 19:00 | 18:00 | Sonra |
| ABD hisse kapanışı (16:00 ET) | 21:00 | 20:00 | Sonra |
| CFTC COT (Cuma 15:30 ET, Salı verisi) | 20:30 | 19:30 | Sonra; ilk kullanılabilir uzlaşma Pazartesi |

---

## 2. Yöntem literatürü: fiyat keşfi nasıl ölçülür, nerede yanıltır

- **Hasbrouck (1995), "One Security, Many Markets", JF 50(4): 1175–1199.**
  - Bir piyasanın "bilgi payı" (IS), tüm piyasalarda ortak olan gözlenemeyen etkin fiyatın yeniliklerine yaptığı oransal katkı.
  - Dow 30 hisselerinde NYSE'nin medyan IS'i %92,7.
  - https://econpapers.repec.org/RePEc:bla:jfinan:v:50:y:1995:i:4:p:1175-99
- **Gonzalo ve Granger (1995), JBES 13(1): 27–35.** Eşbütünleşik sistemlerde ortak I(1) faktörlerin tahmini. Bileşen payı (CS / PT) ölçüsünün temeli bu. https://econpapers.repec.org/RePEc:bes:jnlbes:v:13:y:1995:i:1:p:27-35
- **Putniņš (2013), "What do price discovery metrics really measure?", J. Empirical Finance 23: 68–83.**
  - IS ve CS, "yeni bilgiyi ilk yansıtan piyasa" tanımına yalnız iki serinin gürültüsü eşitse uyuyor.
  - Gürültüler farklıysa iki ölçü, bilgi liderliğini "gürültüden kaçınma" ile karıştırıyor.
  - Önerilen **bilgi liderliği payı (ILS)** gürültü farkına dayanıklı.
  - Dört ampirik çalışmada ölçü seçimi "kim öncü" sonucunu esaslı biçimde değiştiriyor.
  - https://econpapers.repec.org/RePEc:eee:empfin:v:23:y:2013:i:c:p:68-83
  - **VİOP'a çıkarım:** VİOP uzlaşması 10 dakikalık VWAP. Spot ise anlık kotasyon. Gürültü yapısı çok farklı olduğundan VİOP için IS/CS yerine ILS ya da doğrudan gecikmeli regresyon kullanılmalı.
- **Lo ve MacKinlay (1990), "An econometric analysis of nonsynchronous trading", J. Econometrics 45: 181–211 (NBER WP 2960).**
  - İşlem yapılmaması getirilerin varyansını, otokorelasyonunu ve **çapraz otokorelasyonunu** (öncülük-gecikmenin kanalı) değiştiriyor.
  - Yazarlar bunun rastgele yürüyüş reddinin önemli bir kaynağı olduğunu savunuyor.
  - https://econpapers.repec.org/RePEc:eee:econom:v:45:y:1990:i:1-2:p:181-211 , https://www.nber.org/papers/w2960
- **Scholes ve Williams (1977), JFE 5(3): 309–327** (senkron olmayan veriden beta tahmini) ve **Martens ve Poon (2001), JBF 25(10): 1805–1827** (uluslararası piyasalarda senkronize getiri ve günlük korelasyon). İkisinin de özetine erişilemedi, bulgu raporlanmıyor.
  - https://econpapers.repec.org/RePEc:eee:jfinec:v:5:y:1977:i:3:p:309-327
  - https://econpapers.repec.org/RePEc:eee:jbfina:v:25:y:2001:i:10:p:1805-1827

---

## 3. Fiyat keşfi: hangi altın piyasası önden gidiyor?

| Çalışma | Piyasalar / örneklem / sıklık | Bulgu | Zayıflık |
|---|---|---|---|
| Hauptfleisch, Putniņš ve Lucey (2016), JFM 36(6): 564–586 (DOI 10.1002/fut.21775) | Londra spot ve NY (COMEX) vadeli, 17 yıl, gün içi | İkisi de katkı yapıyor, NY **ortalamada** daha büyük. NY hacmi Londra spotunun < 1/10'u. Pay gün içinde ve yıllar arasında değişiyor (likidite, gün ışığı saatleri, makro duyurular). NY platform yükseltmesi göreli gürültüyü ve gün ışığının etkisini azaltmış, ama bilginin fiyata yansıma hızını belirgin biçimde artırmamış | Sayısal paylar özette yok; yıllar sayfada belirtilmemiş. https://econpapers.repec.org/RePEc:wly:jfutmk:v:36:y:2016:i:6:p:564-586 |
| Lucey, Larkin ve O'Connor (2013), AEL 20(8): 813–817 | Londra ve NY, 25 yıl, örtüşmeyen 4 aylık pencerelerde IS | "Neither London nor New York is dominant". Liderlik el değiştiriyor ve makro/siyasi olaylarla açıkça eşleşmiyor | Kısa not; IS yöntemi Putniņš eleştirisine açık. https://econpapers.repec.org/RePEc:taf:apeclt:v:20:y:2013:i:8:p:813-817 |
| Lucey, Larkin ve O'Connor (2014), AEL 21(13): 887–892 | Londra, NY, Tokyo, Şanghay; Diebold–Yılmaz yayılım endeksi | Şanghay getiri ve oynaklıkta "yalıtılmış". En güçlü bağlı çift Londra spot–COMEX. Getiri yayılımı oynaklık yayılımından güçlü; zamanla değişiyor | Örneklem dönemi sayfada yok; 2014 öncesi veri, SHFE/SGE gece seansları ve 2024–26 Çin talebi öncesi. https://econpapers.repec.org/RePEc:taf:apeclt:v:21:y:2014:i:13:p:887-892 |
| Jin, Li, Wang ve Yang (2018), JFM 38(10): 1262–1281 | Çin içi: SHFE vadeli ve SGE spot | Fiyat keşfi ağırlıkla vadelide (IS, CS, ILS üçünde de); üç seansın hepsinde vadeli baskın; gece seansında fiyat keşfi her iki piyasada daha güçlü | Çin–Londra/NY arası ilişkiyi ölçmüyor. https://econpapers.repec.org/RePEc:wly:jfutmk:v:38:y:2018:i:10:p:1262-1281 |
| Ivanov (2013), JEF 37(3): 453–462 | Altın, gümüş, petrol ETF'leri; vadeli ve dayanak; gün içi | ETF'ler dayanağı yakından izliyor. **Altın ve gümüşte fiyat keşfi ETF piyasasına kaymış**, petrolde hâlâ vadelide | Yalnız ABD seansı; tek yazar. https://econpapers.repec.org/RePEc:spr:jecfin:v:37:y:2013:i:3:p:453-462 |
| Caminschi ve Heaney (2014), JFM 34(11): 1003–1039 | LBMA PM fiksingi (eski telefonlu yöntem) → GC vadeli ve GLD | Fiksing başladıktan hemen sonra hacim ve oynaklık anlamlı yüksek. İlk 4 dakikada bilgili işlemciler anlamlı getiri elde ediyor. Açılış dakikalarındaki işlemler fiks yönünü bazı durumlarda %90'ın üzerinde isabetle öngörüyor. Sonuç yayımlandıktan sonra etki yok | Mart 2015 öncesi; IBA elektronik ihalesi için geçerliliği bilinmiyor. https://econpapers.repec.org/RePEc:wly:jfutmk:v:34:y:2014:i:11:p:1003-1039 . (r2'deki "%47,8 hacim artışı, %69,9 / %80 yön uyumu" sayıları özette yok; tam metinden doğrulanmadı) |
| Pavabutr ve Chaihetphon (2010), JEF 34(4): 455–467 | Hindistan altın vadelisi (MCX), IS | **Özet erişilemedi** (EconPapers, IDEAS ve Crossref'te yok; Springer giriş istiyor) | https://econpapers.repec.org/RePEc:spr:jecfin:v:34:y:2010:i:4:p:455-467 |
| Xu ve Fung (2005), JIFMIM 15(2): 107–124 | ABD ve Japonya (TOCOM) kıymetli metal vadelileri | **Özet erişilemedi** (EconPapers ve IDEAS'ta "abstract yok"; ScienceDirect 403) | https://econpapers.repec.org/RePEc:eee:intfin:v:15:y:2005:i:2:p:107-124 |
| Meader (Metals Focus), LBMA *Alchemist* 83 | Şanghay primi, 2005–2016, günlük | Gecikmeli korelasyonlar pozitif ama çok düşük ve anlamsız. Dolar kontrollü regresyonda etki "mütevazı ama pozitif ve anlamlı". Boğa döneminde ≥%1 primden 1 ay sonra ortalama +33 USD (r2, r3) | Sektör analizi, hakemsiz; gözlem sayısı yok. https://www.lbma.org.uk/alchemist/issue-83/links-between-the-chinese-and-international-gold-prices |

**VİOP ve Türkiye.**
- VİOP altın sözleşmeleri ile spot/uluslararası fiyat arasında fiyat keşfi (IS/CS, Granger, VECM) çalışan Türkçe ya da İngilizce yayın **bulunamadı.** Arama bütçesi tükendiği için DergiPark ve ULAKBİM taranamadı; bu, "yok" demek değil, "aranamadı" demek.
- Bulunan tek VİOP altın çalışması Karataş Elçiçek (2023, BERJ): 02.09.2013–30.11.2022, ARMA-GARCH, haftanın günü etkisi. Fiyat keşfi değil; sözleşme tipi özette belirtilmemiş (r2). https://econpapers.repec.org/RePEc:ris:buecrj:0643
- **Bizim verideki kanıt** VİOP'un uydu piyasa olduğunu gösteriyor:
  - VİOP–spot günlük getiri korelasyonu 0,977, beta 0,98 (a7).
  - Ekim 2026'da uzlaşma–spot(15:00 UTC) farkı −0,5 ile +9,2 USD arasında, yani taşıma maliyeti kadar (r1).
  - VİOP–spot baz sapması ertesi gün kapanıyor (IC −0,50, t −25,1; IS t −23,9, OOS t −15,2; a2). Bu, VİOP'un kendine özgü gürültüsünün spot tarafından düzeltildiğini, yani bilginin spottan VİOP'a aktığını gösteriyor.
  - Hacim de küçük: tüm XAUUSD vadeleri 2026 pazartesi medyanı ≈ 43 bin ons/gün (r1).
- **Pratik sonuç:** VİOP için "öncü piyasa" aramak yerine küresel fiyatın kendisi için öngörücü aranmalı. VİOP'a özgü tek bilgi, uzlaşma VWAP'ının spottan sapmasıdır. Bu sapma t'de 15:00 itibarıyla kısmen gözlenebilir, ama pratikte bir mikro-gürültü.

---

## 4. Varlıklar arası ilişkiler: eşzamanlı mı, öngörücü mü?

### 4.1 Genel ilke (döviz–emtia literatürü)
- **Chen, Rogoff ve Rossi (2010), QJE 125(3): 1145–1194 (NBER WP 13901).**
  - "Emtia parası" kurları küresel emtia fiyatlarını "şaşırtıcı derecede sağlam" biçimde öngörüyor; örneklem içi ve dışı, birçok alternatif benchmark'a karşı.
  - Ters yön (emtia → kur) "belirgin şekilde daha az sağlam".
  - Açıklama: kurlar ileriye bakan varlık fiyatları, emtia fiyatları ise kısa vadeli talep dengesizliklerine tepki veriyor.
  - Sıklık ve ülke listesi erişilen sayfalarda **belirtilmemiş**. Hedef değişken altın değil, toplu emtia endeksleri.
  - https://econpapers.repec.org/RePEc:oup:qjecon:v:125:y:2010:i:3:p:1145-1194 , https://www.nber.org/papers/w13901
- **Ferraro, Rogoff ve Rossi (2015), JIMF 54: 116–141.**
  - **Günlük** sıklıkta emtia fiyatı ile kur arasında çok kısa vadeli bir bağ var.
  - Bağ **eşzamanlı** gerçekleşen değişimlerle sağlam.
  - **Gecikmeli** değişimlerle öngörü gücü "geçici" ve çoğunlukla ancak istikrarsızlık modellenince ortaya çıkıyor.
  - https://econpapers.repec.org/RePEc:eee:jimfin:v:54:y:2015:i:c:p:116-141
  - **Bu çalışmanın temel önsel bilgisi bu:** günlük veride güçlü ilişkiler eşzamanlıdır. 15:00 UTC'de senkron örneklenmiş bir çapraz varlığın t-1→t değişiminin fwd1'i öngörmesi beklenmez.

### 4.2 Gümüş
- **Baur ve Tran (2014), Empirical Economics 47(4): 1525–1541**, 1970–2011. Altın ile gümüş arasında açık eşbütünleşme var ve **ilişkiyi altın fiyatı sürüyor.** Balon benzeri dönemler ve finansal krizler sonucu etkiliyor. Escribano ve Granger'ın (1998) uzantısı. https://econpapers.repec.org/RePEc:spr:empeco:v:47:y:2014:i:4:p:1525-1541
- Escribano ve Granger (1998), J. Forecasting 17(2): sayfası 404 verdi, doğrulanamadı.
- Bizim kayıt (a5):
  - Altın/gümüş oran z-skorları: YOK.
  - "Altın son 5 günde gümüşü geçtiyse ertesi gün altın zayıf": tam dönem t −2,49, ama IS t −0,68, OOS t −2,82. DÜŞÜK.
- **Önsel:** Gümüşün altına öncülük etmesi beklenmez. Göreli hareketin altında ortalamaya dönüş yaratması zayıf bir aday.

### 4.3 Madenci hisseleri (GDX/GDXJ)
- **Lucey ve O'Connor (2017), "Are gold bugs coherent?", AEL 24(2): 90–94.** Dalgacık modelleri: kısa vadede madenci hisseleri ile altın arasında az ilişki, uzun vadede anlamlı ve kalıcı ilişki. "Gold prices appear to lead gold miner stock prices." https://research.ucc.ie/en/publications/are-gold-bugs-coherent/
  - r2 bu çalışmanın örneklemini 1998–2015 günlük ve öncülüğü "en az bir hafta" olarak aktardı. Bu ayrıntılar okuduğum özette **yok.**
- **Blose, Gondhalekar ve Kort (2018), JEF 42(3):** gece pozitif / gündüz negatif getiri deseni London fix, madenci hisseleri, kapalı uçlu fonlar ve ETF'lerde de var (r2). https://ideas.repec.org/a/spr/jecfin/v42y2018i3d10.1007_s12197-017-9403-0.html
- Tufano (1998, JF) madenci hisselerinin altın duyarlılığı: EconPapers ve IDEAS sayfaları 404 verdi, doğrulanamadı.
- **Bizim kayıt, literatürle ters yönde ilk iz (a4):**
  - GDXJ'nin GLD'ye göre 1 günlük beta-artığı (t-1 ABD kapanışları, 60 günlük beta) → VİOP fwd3: IC 0,068, t 3,53, IS t 2,53, OOS t 2,63; 10 yılın 9'unda aynı işaret.
  - GDX ve RING'de benzer sonuç.
  - 2010–2016 spot döneminde ≈0 (IC 0,016).
  - Global BH-FDR q = 0,43, yani geçmiyor; etiket ORTA.
  - Mekanizma adayı: hisse yatırımcısının altın görüşünü kaldıraçlı araçla önce ifade etmesi. Literatürün "altın madenciye öncülük eder" bulgusuyla çelişiyor. Sağlamlık ve çürütme testi gerekli.

### 4.4 Dolar / DXY
- **Capie, Mills ve Wood (2005), JIFMIM 15(4): 343–352:** özet erişilemedi. https://econpapers.repec.org/RePEc:eee:intfin:v:15:y:2005:i:4:p:343-352
- **Reboredo (2013), JBF 37(8): 2665–2676:** kopula. Altın ile dolar değer kaybı arasında pozitif ve anlamlı ortalama bağımlılık var (hedge). Kuyruk bağımlılığı simetrik (uç dolar hareketlerinde güvenli liman). Dönem ve sıklık özette yok. https://econpapers.repec.org/RePEc:eee:jbfina:v:37:y:2013:i:8:p:2665-2676
- **Pukthuanthong ve Roll (2011), JBF 35(8): 2070–2083:** altının her para birimindeki fiyatı o paranın değer kaybıyla ilişkili olabilir; dolar, euro, sterlin ve yen için de geçerli. Anahtar kelimelerde Granger nedenselliği var, ama yön özette yok. https://econpapers.repec.org/RePEc:eee:jbfina:v:35:y:2011:i:8:p:2070-2083
- **Sjaastad (2008), Resources Policy 33(2): 118–124:** Bretton Woods sonrası majör kurlar arasındaki dalgalanma altın piyasasında büyük bir fiyat istikrarsızlığı kaynağı. Altın piyasası "dolar bloku hâkimiyetinde". https://econpapers.repec.org/RePEc:eee:jrpoli:v:33:y:2008:i:2:p:118-124
- Bizim veri ve önceki raporlar:
  - Haftalık eşzamanlı altın–dolar korelasyonu her alt dönemde −0,37 ile −0,49 arasında (r3).
  - Gecikmeli günlük DXY değişimi → VİOP fwd: YOK (a4, t −0,95).
  - "18 saatlik emilim": dolar t-1 ABD kapanışında yükseldiyse altın [t-1 20:00 → t 15:00 UTC] penceresinde kısmen geri alıyor (IC +0,058, t 2,76). Ama bu VİOP girişinden önce bitiyor (a4).

### 4.5 Emtia paraları (AUD, ZAR), EM paraları, CNH, JPY/CHF
- **Apergis (2014), IREF 29: 75–82:** ECM. Nominal AUD için günlük, reel kur için çeyreklik veri, 2000–2012. **Altın fiyatları AUD/USD'yi** örneklem dışında "güçlü ve sağlam" biçimde öngörüyor. Yön altından kura. https://econpapers.repec.org/RePEc:eee:reveco:v:29:y:2014:i:c:p:75-82
- AUD/ZAR'ın günlük sıklıkta **altını** öngördüğüne dair altına özgü çalışma **bulunamadı.** Chen–Rogoff–Rossi toplu endeks içindir ve sıklığı doğrulanamadı.
- CNH ve Çin hisseleri → altın: hakemli çalışma **bulunamadı.** Bizim kayıtta Hang Seng'in t günü getirisi (08:10 UTC kapanış) → fwd3: IC 0,061, t 3,06, IS t 2,37, OOS t 2,11 (a6). Ama 2010–2016 spot döneminde işaret **ters** (h=1 IC −0,054, t −2,22). Çin altın hisseleri (600547.SS, 1818.HK) artıkları h=5'te OOS t ≈ 3, ama IS t < 1.
- JPY/CHF: güvenli liman kurlarının altına öncülük ettiğine dair çalışma bulunamadı. Pukthuanthong ve Roll yen için de değer kaybı–altın bağını belirtiyor.

### 4.6 Reel faiz / TIPS / ABD 10 yıllık
- Seviye ilişkisi: Erb ve Harvey (2013, FAJ) 1997'den beri 10 yıllık TIPS ile reel altın fiyatı arasında güçlü negatif korelasyon buluyor. Barsky ve Summers (1988) Gibson paradoksu (r2, r3).
- 2024–2025'te ilişki koptu; haftalık beta +1,1%/puan, R² 0,00. 2026'da geri döndü; beta −16%/puan (r3).
- Günlük gecikmeli öngörü: r3'ün OOS testlerinde ΔTIPS için h=1/3/5 OOS R² +%0,27 / +%0,10 / +%0,09 (1 gün). COMEX'e karşı görülen −0,077'lik ertesi gün korelasyonu büyük olasılıkla kapanış saatleri arasındaki asenkronluktan kaynaklanıyor (r3).
- a4: nominal ve reel 10y, 2y ve başabaş değişimleri → VİOP fwd: YOK. Eğri dikleşmesi (Δ5 10y−2y) tam dönem t 3,15, ama IS t 1,87 ve 2010–2016'da işaret ters. DÜŞÜK.

### 4.7 S&P 500, VIX, kriz anları
- **Baur ve Lucey (2010), Financial Review 45(2): 217–229:** altın ortalamada hisselere karşı hedge, uç düşüşlerde güvenli liman. Güvenli liman etkisi kısa ömürlü, ~15 işlem günü (r3). https://econpapers.repec.org/RePEc:bla:finrev:v:45:y:2010:i:2:p:217-229
- **Baur ve McDermott (2010), JBF 34(8):** ABD ve büyük Avrupa borsaları için hedge ve güvenli liman. Aşırı oynaklıkta altın hisselerle birlikte hareket edebiliyor (r2). https://econpapers.repec.org/RePEc:eee:jbfina:v:34:y:2010:i:8:p:1886-1898
- **Hood ve Malik (2013), RFE 22(2): 47–52**, Kasım 1995–Kasım 2010 günlük:
  - Altın ABD hisseleri için hedge ve **zayıf** güvenli liman.
  - Diğer kıymetli metaller bu rolü oynamıyor.
  - Oynaklık çok düşük ya da çok yüksek olduğunda altın–hisse korelasyonu negatif değil.
  - VIX daha güçlü bir hedge ve güvenli liman.
  - https://econpapers.repec.org/RePEc:eee:revfin:v:22:y:2013:i:2:p:47-52
- 2026 deneyimi: Mart ve Ekim'de altın hisselerle birlikte düştü (likidite satışı, marj; r3). Kriz anında yön rejime bağlı.

### 4.8 Bitcoin
- Klein, Pham Thu ve Walther (2018), IRFA 59: 105–116: Bitcoin altından farklı. Düşen piyasalarla pozitif korelasyonlu, istikrarlı hedge özelliği yok. https://econpapers.repec.org/RePEc:eee:finana:v:59:y:2018:i:c:p:105-116
- Dyhrberg (2016), FRL 16: 85–92: GARCH. Bitcoin oynaklık özellikleriyle altın ile dolar arasında bir yerde. https://econpapers.repec.org/RePEc:eee:finlet:v:16:y:2016:i:c:p:85-92
- Bouri, Gupta, Lahiani ve Shahbaz (2018), Resources Policy 57: 224–235: 17.07.2010–02.02.2017 günlük, NARDL ve kantil ARDL. Emtia endeksi ve **altın, Bitcoin fiyatını** öngörüyor; ilişki asimetrik, doğrusal değil ve kantile bağlı. https://econpapers.repec.org/RePEc:eee:jrpoli:v:57:y:2018:i:c:p:224-235
- Bitcoin → altın öncülüğü: **bulunamadı.** a4 ve a5: BTC değişimleri ve BTC artığı → VİOP fwd: YOK; IS'te seçilen BTC artığı OOS'ta işaret değiştirdi.

### 4.9 Petrol ve bakır
- **Zhang ve Wei (2010), Resources Policy 35(3): 168–177**, Ocak 2000–Mart 2008:
  - Seviye korelasyonu 0,9295, eşbütünleşme var.
  - Petrol değişimleri altın oynaklığını doğrusal olarak Granger-nedenliyor; tersi yok; doğrusal olmayan nedensellik yok.
  - Fiyat keşfi: PT modelinde petrol %86,50, altın %13,50; IS modelinde %50,28 / %49,72.
  - https://econpapers.repec.org/RePEc:eee:jrpoli:v:35:y:2010:i:3:p:168-177
- **Narayan, Narayan ve Zheng (2010), Applied Energy 87(10): 3299–3303:** farklı vadelerde altın ve petrol vadelileri eşbütünleşik. "Petrol piyasası altını öngörmekte kullanılabilir, tersi de" denince iki piyasa birlikte etkin değil. Dönem özette yok. https://econpapers.repec.org/RePEc:eee:appene:v:87:y:2010:i:10:p:3299-3303
- Uyarı: Her iki çalışma da seviyede eşbütünleşme kuruyor. 2026'da korelasyonun işareti değişti (r3: haftalık −0,31). Günlük gecikmeli Brent → VİOP: YOK (a4).
- Bakır/altın oranı → altın: hakemli çalışma **bulunamadı**; a4'te YOK.

---

## 5. Akış ve konumlanma

| Konu | Kanıt | Kaynak | Öngörü yönü |
|---|---|---|---|
| ETF akışları | Deutsche Bank Granger testi: fiyat akışa öncülük ediyor (ikincil aktarım). Aalto tezi (2007–2014): yalnız kriz sonrası zayıf nedensellik | r2: https://www.tickmill.com/blog/institutional-insights-deutsche-bank-who-drives-gold-prices , https://epub.lib.aalto.fi/en/ethesis/id/14319 | Akış fiyatı izliyor; öngörü zayıf |
| ETF fiyat keşfi | Gün içinde altın fiyat keşfi ETF'e kaymış | Ivanov (2013) | Saniye–dakika ölçeği, günlük değil |
| COT (CFTC) | Değerli metallerde pozisyonlar getiriye tepki veriyor (pozitif geri besleme). Lingnan semineri: spekülatör akış bileşeni ertesi haftayı negatif öngörüyor (tam metin yok). Altında COT uçlarının karşıt öngörücü olduğuna dair hakemli, OOS ve maliyet sonrası kanıt **yok** | r3: https://theses.lib.polyu.edu.hk/handle/200/7971 ; r2: https://lingnan.sysu.edu.cn/en/node/3656 | Zayıf ve tartışmalı |
| COT, bizim kayıt (a6) | Kontraryen z±2 kuralları ≈0. "Üretici net/OI z52 → fwd5" OOS t −2,15, ama IS t −0,34. "Swap net/OI z52 → fwd10" OOS t 2,31, IS t 0,20 | `out/registry/a6_akis_konum_cin.csv` | IS–OOS tutarsız |
| Merkez bankası alımları | Diğer her şey sabitken 20–30 t ek alım ≈ %1 fiyat (WGC). Aylık ve gecikmeli veri; Ç3 2026 tahmininin ~2/3'ü açıklanmayan alım | r3 (WGC Mid-Year Outlook 2026) | 1–5 günde kullanılamaz; PBoC açıklama günü (~ayın 7'si) olay olarak test edilebilir |
| Şanghay primi | Mütevazı pozitif (Meader). a6: SHFE AU0 1g prim değişimi → VİOP fwd1 ≈0 (uç dönemler hariç sağlamlık sürümünde t 0,69; roll temizliği olmadan t 0,35); 5g değişim → fwd5 t −1,99 (IS −0,55, OOS −2,03) | LBMA Alchemist 83; a6 | Zayıf |
| Hindistan primi/iskontosu | Eylül 2026 iskontosu 66 USD → 16 Ekim 8 USD, sonra prim (r3). Öngörü testi yapılmamış; zaman serisi elimizde yok | r3 | Veri yok |

---

## 6. Gün içi zaman yapısı ve saat etkileri

- **Blose ve Gondhalekar (2014), AEL 21(18): 1269–1272:** COMEX ön ay 1985–2012. Gece getirisi anlamlı pozitif, gündüz getirisi anlamlı negatif. GLD'de gece getirisi gündüzden anlamlı yüksek. Asimetri "belirgin biçimde zayıflamış ama mevcut". Büyüklük özette yok. https://econpapers.repec.org/RePEc:taf:apeclt:v:21:y:2014:i:18:p:1269-1272
- **Cai, Cheung ve Wong (2001), JFM 21(3): 257–278:** COMEX gün içi. Gün içi desenler oynaklığı derinden etkiliyor. 23 ABD duyurusu içinde en büyük etkiyi istihdam, GSYH, TÜFE ve kişisel gelir yapıyor. Desenler arındırılınca uzun hafıza var. https://econpapers.repec.org/RePEc:wly:jfutmk:v:21:y:2001:i:3:p:257-278
- **Elder, Miao ve Ramchander (2012), JBF 36(1):** altın, gümüş ve bakır vadelileri ABD makro sürprizlerine dakikalar içinde tepki veriyor (r3). https://econpapers.repec.org/RePEc:eee:jbfina:v:36:y:2012:i:1:p:51-65
- **Smales (2015), JIFMIM 34:** planlanmamış haberlere önce aşırı tepki, sonra geri alma (r2). https://econpapers.repec.org/RePEc:eee:intfin:v:34:y:2015:i:c:p:161-172
- **Christie-David, Chaudhry ve Koch (2000), JEB 52(5):** özet erişilemedi. https://econpapers.repec.org/RePEc:eee:jebusi:v:52:y:2000:i:5:p:405-421
- **Lucca ve Moench (2015):** FOMC öncesi sürüklenme hisselerde var, Hazine tahvilleri ve kurlarda yok. Altın için sonuç bulunamadı (r2). https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf
- **LBMA fiksingi:** Caminschi ve Heaney (2014; bölüm 3). Kışın PM ihalesi (15:00 UTC) VİOP uzlaşma penceresiyle aynı anda başlıyor. Yazın 1 saat önce bitiyor. Bu, VİOP uzlaşmasının içerdiği gürültünün mevsime göre değişebileceği anlamına geliyor (hipotez H30).
- **Asya / Şanghay:**
  - Bloomberg (23.04.2024): rekor rallinin kökü, ABD verilerinin geldiği gece seansında yoğunlaşan Şanghay işlemlerinde olabilir (r2).
  - Jin ve ark. (2018): Çin'de fiyat keşfi gece seansında daha güçlü.
  - Not: SHFE/SGE gece seansı 12:00/13:00–18:30 UTC. Yani uzlaşmamızla örtüşüyor ve çoğu uzlaşmadan **sonra.**
- **Bizim veri (a2; segment ortalamaları, spot, bps/gün, 2010–2026):**
  - S2_late (t-1 20:00 → t 00:00 UTC; NY kapanışı, CME bakım arası, Asya açılışı): **+2,93** (t 6,59; IS t 3,60; OOS t 4,57; 17 yılın 15'inde pozitif). Drift arındırılmış fazla +2,67 (t 6,0).
  - S3_asia (00–07 UTC): +2,04 (t 2,99), ama IS t 0,06, OOS t 1,00.
  - S4_lon: −1,21. S5_nyam: −0,84. Asya pozitif / Londra negatif deseni yalnız 2010–2016'da var.
  - Segment getirilerinin kendisi fwd1/3/5'i öngörmüyor: 36 testin hepsinde |t| < 2,4; IS'te seçilen kural OOS'ta tersine döndü (a2).
  - Kapanıştan kapanışa işlem yapan biri gece sürüklenmesini ayrıştıramaz; bu yalnız seans içi giriş ve çıkışla kullanılabilir.

---

## 7. Senkron olmayan işlem (non-synchronous trading) tuzağı: ölçülmüş büyüklük

**Neden:** VİOP uzlaşması 15:05 UTC civarında. Yabancı piyasaların "günlük kapanışları" bundan sonra:
- COMEX uzlaşması 18:30 UTC (kış).
- ABD hisseleri 21:00 UTC.
- ABD Hazine getirileri gün sonu.
- Yahoo `=X` kurları 24:00 UTC.

Bu kapanışlar, VİOP'un **ertesi** uzlaşmaya kadar fiyatlayacağı bilgiyi içeriyor. "Yabancı(t) → VİOP(t+1)" regresyonu bu yüzden mekanik bir pozitif ilişki bulur. Lo ve MacKinlay (1990) bunu çapraz otokorelasyon kanalı olarak modelliyor.

**Kendi ölçümüm** (panel_viop, 2017-03 → 2026-11, n = 2.358; hedef fwd1 = uzlaşma(t) → uzlaşma(t+1); betik `out/r5_leadlag_literatur/nonsync_demo.py`):

| Öngörücü | Bilgi zamanı | corr(fwd1) | ≈t | 2017–21 | 2022–26 |
|---|---|---|---|---|---|
| Spot XAU 15:00→20:00 UTC, gün t (uzlaşmadan sonra) | 20:00 t → **ileriye bakar** | **+0,424** (R² %18, beta 0,92) | 20,6 | +0,437 | +0,417 |
| COMEX GC kapanıştan kapanışa, gün t (t-1 → t) | ~21:00 t → **ileriye bakar** | **+0,191** | 9,3 | +0,193 | +0,191 |
| ABD 10y getirisi (^TNX) değişimi, gün t | 21:00 t → **ileriye bakar** | **−0,089** | −4,3 | −0,199 | −0,035 |
| S&P 500 değişimi, gün t | 21:00 t → **ileriye bakar** | +0,025 | 1,2 | — | — |
| COMEX GC t-2 → t-1 (doğru gecikmeli) | t-1 akşamı | −0,028 | −1,3 | +0,049 | −0,069 |
| ^TNX t-2 → t-1 (doğru gecikmeli) | t-1 akşamı | −0,014 | −0,7 | −0,043 | −0,001 |
| S&P t-2 → t-1 (doğru gecikmeli) | t-1 akşamı | +0,046 | 2,3 | — | — |
| Spot XAU 15:00(t-1) → 15:00(t) (senkron) | 15:00 t | +0,042 | 2,1 | — | — |

**Kurallar:**
1. Yabancı serileri **15:00 UTC'de** örnekleyin (Dukascopy `dk_*_p15`, `xau_p15`). Ya da yalnız t-1'de kapanmış veriyi kullanın.
2. TradingView günlük çubuğu normal seansı ve aynı günün akşam seansını içeriyor. Kapanışı 20:00 UTC'deki son işlem olabilir (r1). Uzlaşma yerine bu kapanış kullanılırsa tuzak tersine kurulur.
3. Yarım günler (uzlaşma ~09:35 UTC) dışlanmalı (a7).
4. Her aday için `placebo_lead` yapılmalı. Öngörücü bir gün geleceğe kaydırılınca korelasyonun sıçraması beklenir; bir gün geçmişe kaydırılınca düzgünce sönmesi gerekir.
5. Uzlaşma–kapanış farkı gibi "kapanışta hesaplanan" sinyaller de ileriye bakar. Bülten kapanışı 15:15–15:20 UTC'de oluşuyor; fwd1'e karşı t −2,92 olan ilişki temiz t-1 sürümünde t 0,14 (a1).

---

## 8. Hangi ilişkiler günlük kapanıştan kapanışa ÖNGÖRÜ gücü gösteriyor?

| İlişki | Eşzamanlı güç | Günlük gecikmeli öngörü (literatür) | Bizim veride ilk iz (FDR öncesi) | Önsel |
|---|---|---|---|---|
| Dolar (DXY) | Güçlü (haftalık −0,4) | Ferraro ve ark.: geçici | YOK (a4 t −0,95); 18 saatlik emilim girişten önce bitiyor | Çok düşük |
| Reel faiz / 10y | Rejime bağlı (2024–25: 0; 2026: −0,37 haftalık) | r3: OOS R² ≈ 0 | YOK; eğri dikleşmesi DÜŞÜK | Çok düşük |
| Gümüş | Çok güçlü | Altın gümüşü sürüyor (Baur–Tran) | Oranlar YOK; 5g göreli hareket DÜŞÜK | Düşük |
| Madenciler | Güçlü (yüksek beta) | Altın madencilere öncülük ediyor (Lucey–O'Connor) | Madenci artığı → fwd3 ORTA (t 3,5) | Düşük–orta |
| Petrol | Rejime bağlı | 2000–08 petrol → altın oynaklığı (Zhang–Wei) | YOK | Düşük |
| S&P / VIX | Krizde değişken | Güvenli liman ~15 gün (Baur–Lucey) | YOK | Düşük |
| Bitcoin | Zayıf | Altın → BTC (Bouri ve ark.) | YOK | Çok düşük |
| Emtia paraları | Eşzamanlı | Kur → emtia endeksi (CRR); altın → AUD (Apergis) | Test edilmedi (Yahoo `=X` güvenilmez) | Düşük |
| Asya hisseleri | — | Literatür yok | HSI → fwd3 t 3,06, ama 2010–16'da ters | Düşük |
| Şanghay primi | — | Mütevazı (Meader) | ≈0 | Düşük |
| COT | — | Pozisyon fiyatı izliyor | IS–OOS tutarsız | Düşük |
| ETF akışları | — | Akış fiyatı izliyor | (e3 ajanında) | Düşük |
| Gece/ABD sonrası segment | Ortalama getiri | Gece pozitif, gündüz negatif (Blose–Gondhalekar) | +2,9 bps/gün (t 6,6); ama kapanıştan kapanışa ayrıştırılamaz | Yüksek (ortalama), uygulanabilirlik düşük |
| Kendi momentum, düşük oynaklık | — | TSMOM aylık (Moskowitz ve ark.) | LOWMOM drift arındırılmış Sharpe ~1 (t ≈ 3); 2026'da pasif (a1) | Orta |
| Veri günü 13:00–15:00 UTC hareketi | — | Aşırı tepki → dönüş (Smales) ile hızlı tepki (Elder) | NFP günü işaret → fwd1 IC 0,27, t 3,68; IS t 1,41, OOS t 3,93 (a3; yılda ~12 olay) | Orta–düşük |
| Gün içi makro artığı | — | — | C1: tam dönem t 2,95, IS t 2,10, OOS t 1,93 (a5) | Düşük–orta |

**Etki büyüklüğü beklentisi.** Literatür ve kayıt birlikte okunduğunda gerçekçi bir günlük öngörücünün |IC| değeri 0,03–0,07 bandında (R² ≈ %0,1–0,5). Bunun üstündeki değerler ya olay koşullu (az gözlem) ya da senkronsuzluk ürünü. Karşılaştırma için sahte "öncü" korelasyonlar 0,19–0,42.

---

## 9. Test edilecek aday hipotezler (VİOP F_XAUUSD, giriş t uzlaşması 15:00–15:10 UTC, çıkış t+h uzlaşması, h = 1/3/5)

"15:00 önce?" sütunu: **E** = sinyal 15:00 UTC'den önce tamamen bilinir. **H** = bilinmez (yalnız t-1 sürümü kullanılabilir). **K** = kısmen (bileşenin bir kısmı sonra). Panel sütunları `DATA_README.md`'ye göredir. "Kayıt" sütunundaki ilk izler BH-FDR öncesidir.

### A. Plasebo ve kontrol (önce bunlar çalıştırılmalı)

| # | Öngörücü | Sinyal zamanı (UTC) | 15:00 önce? | Beklenen | Amaç / kaynak |
|---|---|---|---|---|---|
| P1 | Spot 15:00→20:00 UTC (gün t) → fwd1 | 20:00 t | H | + (≈0,42) | Senkronsuzluk ölçeği; Lo–MacKinlay (1990); bölüm 7 |
| P2 | COMEX GC aynı gün kapanıştan kapanışa (t-1→t) → fwd1 | ~21:00 t | H | + (≈0,19) | Yanlış etiketlenmiş "COMEX öncülüğü" |
| P3 | Uzlaşma(t) − bülten kapanışı(t) → fwd1 | 15:20 t | H | − (t −2,9) | "Kapanışta hesaplanan" sinyal tuzağı (a1) |

### B. Seans, saat ve senkronsuzluk

| # | Öngörücü | Sinyal zamanı (UTC) | 15:00 önce? | Beklenen işaret | Mekanizma | Kaynak / kayıt |
|---|---|---|---|---|---|---|
| H1 | VİOP–spot baz sapması 15:00'te: VİOP son fiyatı (15:00) − spot 15:00 − teorik taşıma → fwd1 | 15:00 t | E (VİOP 15:00 fiyatı dakikalık veri gerektirir) | − | Uydu piyasa; VİOP gürültüsü spota yakınsar | Putniņš (2013); a2 mekanik sürüm t −25 (uzlaşma bazlı, 15:10'da bilinir) |
| H2 | Akşam seansı kapanışı (t-1 20:00 UTC) − aynı günün uzlaşması → fwd1 (t → t+1) | 20:00 t-1 | E | 0 (bilgi t uzlaşmasına zaten yansımış) | Akşam seansındaki yerel fiyat baskısı ertesi güne taşınıyor mu? | r1 (akşam seansı uzlaşmadan medyan 33 bp sapıyor) |
| H3 | S2_late getirisi (t-1 20:00 → t 00:00) → fwd1/3 | 00:00 t | E | + (zayıf) | Gece talebi (Asya) sürüyor mu? | Blose–Gondhalekar (2014); a2 segment ortalaması + ama öngörü yok |
| H4 | Asya getirisi (00:00 → 07:00 t; Şanghay gündüz) → fwd1/3 | 07:00 t | E | + | Çin talebi kalıcı; Şanghay gece seansında fiyat keşfi | Jin ve ark. (2018); Bloomberg (2024; r2) |
| H5 | Londra sabah getirisi (07:00 → 12:00 t) → fwd1 | 12:00 t | E | − | Gündüz satışı / geri dönüş | Blose–Gondhalekar (2014) |
| H6 | Yaz–kış ayrımı: kış haftalarında (PM ihalesi uzlaşma penceresiyle eşzamanlı) \|fwd1\| ve uzlaşma–spot sapması daha büyük | Takvim | E | Oynaklık + / yön 0 | Fiksing anındaki hacim ve oynaklık sıçraması | Caminschi–Heaney (2014); r1 saat tablosu |
| H7 | Yaz aylarında PM fiks (14:00 UTC) → uzlaşma (15:05) arası spot hareketi → fwd1 | 15:00 t | E | − | Fiks sonrası kısa vadeli geri dönüş | Caminschi–Heaney (sonuç yayımı sonrası etki yok → beklenen ≈0) |

### C. Fiyat keşfi ve Asya piyasaları

| # | Öngörücü | Sinyal zamanı (UTC) | 15:00 önce? | Beklenen | Mekanizma | Kaynak / kayıt |
|---|---|---|---|---|---|---|
| H8 | SHFE AU0 primi 1 günlük değişim (07:00 UTC; log(AU0·31,1035/USDCNH) − log(xau_p07)) → fwd1 | 07:00 t | E | + | Çin yerel talebi küresel fiyata yayılır | Meader (LBMA Alchemist 83); a6 ≈0 |
| H9 | Şanghay primi seviyesi > %1 (boğa) / iskonto < −%0,2 → fwd5 | 07:00 t | E | Prim +, iskonto − | Fiziki arbitraj ve ithalat talebi | Meader; r2 test kuralı |
| H10 | SGE PM benchmark (06:15 UTC) − aynı anda spot → fwd1 | 06:15 t | E | + | Benchmark talebi | r2 (SGE saatleri); literatür yok. Veri gerektirir |
| H11 | Hang Seng getirisi (t, 08:10 UTC) → fwd3 | 08:10 t | E | + | Çin risk iştahı ve likidite | Literatür yok; a6 t 3,06, ama 2010–16'da ters |
| H12 | Çin altın madencileri (2899.HK Zijin, 1818.HK, 600547.SS) altın+endeks artığı → fwd5 | 07:00–08:10 t | E | + | Çinli yatırımcının altın görüşü önce hisseye yansır | Literatür yok; a6 OOS t ≈ 3, IS t < 1 |
| H13 | Çin tatili (Altın Hafta 1–7 Ekim, Bahar Bayramı) haftaları → Asya segmenti ve fwd5 | Takvim | E | − (Asya alıcısı yok) | Şanghay kapalı, gece talebi kesilir | Jin ve ark.; Lucey ve ark. (2014) Şanghay yalıtılmış (eski örneklem) |
| H14 | Hindistan primi/iskontosu değişimi (haftalık) → fwd5 | Haftalık haber | K | + | Fiziki talep | r3; veri yok |

### D. Varlıklar arası (senkron 15:00 UTC ya da t-1)

| # | Öngörücü | Sinyal zamanı (UTC) | 15:00 önce? | Beklenen | Mekanizma | Kaynak / kayıt |
|---|---|---|---|---|---|---|
| H15 | GDXJ (ve GDX, RING) 1 günlük beta-artığı e = r_M − β60·r_GLD (t-1 ABD kapanışı) → fwd3 | 20:00/21:00 t-1 | E | + | Hisse yatırımcısının kaldıraçlı bilgisi altına sızar (literatürle ters yön) | Lucey–O'Connor (2017) ters yön; a4 t 3,53 (ORTA, FDR geçmez) |
| H16 | GDX/GLD 5 ve 20 günlük göreli momentum → fwd5 | t-1 | E | + | Aynı mekanizma, daha yavaş | Lucey–O'Connor uzun vade ilişkisi |
| H17 | Gümüş/altın 5 günlük göreli getiri (15:00 UTC) → fwd1 | 15:00 t | E | Altın gümüşü geçtiyse − | Göreli değerde ortalamaya dönüş | Baur–Tran (2014) (altın sürüyor → beklenen zayıf); a5 DÜŞÜK |
| H18 | Platin/altın ve bakır/altın oranı değişimi (15:00 UTC) → fwd3 | 15:00 t | E | − (büyüme ↑ → faiz ↑ → altın ↓) | Döngüsel–parasal ayrışma | Literatür yok |
| H19 | DXY 15:00(t-1) → 15:00(t) değişimi → fwd1 | 15:00 t | E | 0 (eşzamanlı ilişki, gecikmeli yok) | Etkin piyasa sıfır testi | Ferraro ve ark. (2015); a4 YOK |
| H20 | t-1 ABD kapanışında büyük dolar hareketi (\|z\| > 1,5) → fwd1 | 21:00 t-1 | E | 0 (emilim girişten önce bitiyor) | 18 saatlik emilim | a4 (IC +0,058 penceresi girişten önce) |
| H21 | AUD/USD ve USD/ZAR 15:00 UTC değişimi (Dukascopy) → fwd1/5 | 15:00 t | E | AUD↑ / ZAR↑ (USDZAR↓) → + | İleriye bakan emtia paraları | Chen–Rogoff–Rossi (2010; toplu endeks); Apergis (2014) ters yön |
| H22 | USDCNH 15:00 UTC 1 ve 5 günlük değişim → fwd5 | 15:00 t | E | Belirsiz (CNH değer kaybı → Çin korunma talebi +; dolar gücü −) | Çin kur kanalı | Literatür yok; a4 saatlik YOK |
| H23 | USDJPY ve EURCHF sert güvenli liman hareketi (\|z\| > 2) → fwd1/5 | 15:00 t | E | JPY/CHF değer kazancı → + | Güvenli liman akışının yayılması | Pukthuanthong–Roll (2011); Reboredo (2013) kuyruk bağımlılığı |
| H24 | 10y TIPS değişimi (t-1 gün sonu) → fwd1 | t-1 akşamı | E | − (rejime bağlı) | Fırsat maliyeti | Erb–Harvey; r3 OOS ≈ 0 |
| H25 | 2026 rejim koşulu: Fed artırım olasılığı yüksekken (t-1) Δ2y → fwd1 | t-1 | E | − | Şahin rejimde faiz duyarlılığı artar | r3 (2026 betası −%16/puan) |
| H26 | S&P 500'de t-1'de uç düşüş (< −2,5% ya da \|z\| > 2) → fwd1/3/5 | 21:00 t-1 | E | 1–5 günde + ya da 0; 15 gün sonra − | Güvenli liman kısa ömürlü; likidite satışında ters | Baur–Lucey (2010); Hood–Malik (2013); 2026 Mart/Ekim deneyimi (r3) |
| H27 | VIX (15:00 UTC CFD) sıçrama > 90. yüzdelik → fwd5 | 15:00 t | E | Düşük ya da yüksek oynaklık uçlarında 0 / − | Uç oynaklıkta altın–hisse korelasyonu negatif değil | Hood–Malik (2013) |
| H28 | Brent 15:00 UTC 1 ve 5 günlük getiri → fwd1/5; 2022 öncesi ve 2026 ayrı | 15:00 t | E | 2026: −; 2000–2021: + (zayıf) | Petrol → enflasyon → faiz kanalı | Zhang–Wei (2010); Narayan ve ark. (2010); r3 |
| H29 | BTC 15:00 UTC getirisi → fwd1 | 15:00 t | E | 0 / zayıf + | "Değer kaybı" anlatısı ortak faktör | Klein ve ark. (2018); Bouri ve ark. (2018) ters yön |

### E. Akış, konum, olay

| # | Öngörücü | Sinyal zamanı (UTC) | 15:00 önce? | Beklenen | Mekanizma | Kaynak / kayıt |
|---|---|---|---|---|---|---|
| H30 | GLD+IAU+SGOL ton değişimi (t-1 ABD gün sonu yayını) en üst / alt %10 → fwd5 | t-1 akşamı | E | Akış fiyatı izliyorsa 0; aşırı girişte − (kontraryen) | Akış fiyat takipçisi | DB Granger (ikincil), Aalto tezi; Ivanov (2013) |
| H31 | Fiyat → akış ters testi: R(t-5 → t) → GLD akışı(t+1..t+5) | — | — | + | Nedensellik yönü kontrolü; öngörücü değil, tanı | r2 test kuralı |
| H32 | COMEX managed money net/OI 52 ve 156 haftalık z-skoru (Salı verisi, Cuma 20:30 UTC yayını) > +2 / < −2 → Pazartesi girişli fwd5 | Cuma akşamı | E (Pazartesi uzlaşması için) | − (kontraryen) | Kalabalık pozisyonun çözülmesi | PolyU tezi (pozisyon getiriyi izler); a6 ≈0 |
| H33 | COT haftalık MM değişimi (akış bileşeni) → ertesi hafta | Cuma akşamı | E | − | Spekülatör akışının fiyat baskısı geri döner | Lingnan semineri (r2) |
| H34 | PBoC rezerv açıklama günü (~ayın 7'si) altın artışı / durması → fwd1/3 | Açıklama saati (Pekin sabahı) | E (genelde 15:00 öncesi) | Artış +, durma − | Resmî talep sinyali | r3 (PBoC 22 ay üst üste alım; Eylül 2026 +23 t) |
| H35 | NFP/TÜFE günleri: spot 13:00 (kış) / 12:00 (yaz) → 15:00 UTC işareti → fwd1/3 | 15:00 t | E | + (devam) / − (Smales aşırı tepki) | Haberin fiyata tam yansıması saatler sürüyor mu? | Elder ve ark. (2012); Cai ve ark. (2001); Smales (2015); a3 NFP IC 0,27 (t 3,7; IS t 1,4) |
| H36 | FOMC kararı uzlaşmadan sonra (19:00/18:00 UTC): FOMC günü uzlaşmasında pozisyon → fwd1 \|getiri\| (oynaklık) ve yön | Takvim | E | \|fwd1\| ↑; yön: FOMC öncesi sürüklenme? (bilinmiyor) | Kararın tamamı fwd1'e düşüyor | Lucca–Moench (2015) (tahvil/kurda yok, altında bilinmiyor); r3 |

**Ek (oynaklık koşullu kendi momentum, literatür köprüsü):** H36b. 20 günlük gerçekleşen oynaklık alt üçte birdeyse son 5 günün işaretinde pozisyon → fwd1/5. Kaynak: TSMOM (Moskowitz, Ooi ve Pedersen 2012, aylık) ve a1 LOWMOM (t ≈ 3,0; 2010–16 t ≈ 1,5; 2026'da pasif). Beklenen işaret +.

**Test önceliği (önsel güce göre):**
1. P1–P3 (tuzak ölçümü).
2. H15–H16 (madenci), H35 (veri günü), H36b (düşük oynaklık momentumu), H3–H4 (gece/Asya).
3. H8–H13 (Çin).
4. H26–H28 (rejime bağlı kriz ve petrol).
5. Geri kalanlar, ağırlıkla "sıfır beklenen" doğrulama testleri.

Toplam: 36 hipotez + 3 plasebo + 1 ek. Global FDR için hepsi kaydedilmeli.

---

## 10. Bulunamayanlar ve belirsizlikler

- **Türk akademik literatürü:** VİOP (eski VOB) altın vadelileri ile spot ya da uluslararası fiyat arasında fiyat keşfi çalışmaları (DergiPark) **taranamadı**, çünkü arama bütçesi tükenmişti. Bulunan tek VİOP altın çalışması Karataş Elçiçek (2023), haftanın günü etkisi üzerine.
- **MCX (Pavabutr–Chaihetphon 2010) ve TOCOM (Xu–Fung 2005):** özetler erişilemedi, bulgu yok.
- **Hauptfleisch ve ark. (2016):** sayısal bilgi payları ve dönem yılları özette yok.
- **Caminschi–Heaney:** r2'deki %47,8 / %69,9 / %80 sayıları özette yok; doğrulanmadı.
- **Lucey–O'Connor (2017):** örneklem dönemi ve "en az bir hafta" öncülük süresi okuduğum özette yok.
- **ETF akışı → getiri** ve **COT → getiri:** altına özgü hakemli, OOS kanıt bulunamadı. Mevcut kanıt tez ve ikincil aktarım düzeyinde.
- **Altın–CNH, altın–bakır, altın–GVZ, Bitcoin → altın:** hakemli öngörü çalışması bulunamadı.
- **Martens–Poon (2001), Scholes–Williams (1977), Capie–Mills–Wood (2005), Christie-David ve ark. (2000):** özetler erişilemedi.
- **Tufano (1998)** ve **Escribano–Granger (1998):** EconPapers sayfaları 404 verdi.
- **Chen–Rogoff–Rossi (2010):** veri sıklığı ve ülke listesi erişilen sayfalarda yok.
- **Kendi ölçümüm:** Yahoo GC=F ve ^TNX günlük kapanış zamanları panel varsayımına dayanıyor (17:00 ET / 16:00 ET). Ölçülen korelasyonlar bu varsayıma bağlı.

---

## 11. Kaynaklar

**Borsa İstanbul / piyasa yapısı**
- BIST duyuru 30572 (19.11.2024, Prosedür md. 7, akşam seansı listesi): https://borsaistanbul.com/files/duyuru-30572-TR.pdf (yerel: `research/pdf_bist/d30572.pdf`)
- VİOP Prosedürü rev. 70 (r1): https://borsaistanbul.com/files/borsa-istanbul-as-vadeli-islem-ve-opsiyon-piyasasi-proseduru.pdf
- BIST duyuru 12590 (akşam seansı 18.09.2020; r2): https://borsaistanbul.com/duyuru/12590/usdtry-vadeli-islem-sozlesmelerinde-esnek-sozlesme-olusturma-ozelliginin-devreye-alinmasi-dolarons-altin-vadeli-islem-sozlesmelerinin-aksam-seansinda-islem-gormesi-ve-viop-proseduru
- CME GC uzlaşma (r2): https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457088147/Gold
- SGE seansları (r2): https://en.sge.com.cn/eng_trading_ProductsIntroduce

**Fiyat keşfi ve yöntem**
- Hasbrouck (1995): https://econpapers.repec.org/RePEc:bla:jfinan:v:50:y:1995:i:4:p:1175-99
- Gonzalo–Granger (1995): https://econpapers.repec.org/RePEc:bes:jnlbes:v:13:y:1995:i:1:p:27-35
- Putniņš (2013): https://econpapers.repec.org/RePEc:eee:empfin:v:23:y:2013:i:c:p:68-83
- Hauptfleisch, Putniņš ve Lucey (2016): https://econpapers.repec.org/RePEc:wly:jfutmk:v:36:y:2016:i:6:p:564-586 ; https://api.crossref.org/works/10.1002/fut.21775
- Lucey, Larkin ve O'Connor (2013): https://econpapers.repec.org/RePEc:taf:apeclt:v:20:y:2013:i:8:p:813-817
- Lucey, Larkin ve O'Connor (2014): https://econpapers.repec.org/RePEc:taf:apeclt:v:21:y:2014:i:13:p:887-892
- Jin, Li, Wang ve Yang (2018): https://econpapers.repec.org/RePEc:wly:jfutmk:v:38:y:2018:i:10:p:1262-1281
- Ivanov (2013): https://econpapers.repec.org/RePEc:spr:jecfin:v:37:y:2013:i:3:p:453-462
- Pavabutr ve Chaihetphon (2010): https://econpapers.repec.org/RePEc:spr:jecfin:v:34:y:2010:i:4:p:455-467
- Xu ve Fung (2005): https://econpapers.repec.org/RePEc:eee:intfin:v:15:y:2005:i:2:p:107-124
- Caminschi ve Heaney (2014): https://econpapers.repec.org/RePEc:wly:jfutmk:v:34:y:2014:i:11:p:1003-1039
- Meader, LBMA Alchemist 83: https://www.lbma.org.uk/alchemist/issue-83/links-between-the-chinese-and-international-gold-prices
- Karataş Elçiçek (2023): https://econpapers.repec.org/RePEc:ris:buecrj:0643

**Senkronsuzluk**
- Lo ve MacKinlay (1990): https://econpapers.repec.org/RePEc:eee:econom:v:45:y:1990:i:1-2:p:181-211 ; https://www.nber.org/papers/w2960
- Scholes ve Williams (1977): https://econpapers.repec.org/RePEc:eee:jfinec:v:5:y:1977:i:3:p:309-327
- Martens ve Poon (2001): https://econpapers.repec.org/RePEc:eee:jbfina:v:25:y:2001:i:10:p:1805-1827

**Varlıklar arası**
- Chen, Rogoff ve Rossi (2010): https://econpapers.repec.org/RePEc:oup:qjecon:v:125:y:2010:i:3:p:1145-1194 ; https://www.nber.org/papers/w13901
- Ferraro, Rogoff ve Rossi (2015): https://econpapers.repec.org/RePEc:eee:jimfin:v:54:y:2015:i:c:p:116-141
- Apergis (2014): https://econpapers.repec.org/RePEc:eee:reveco:v:29:y:2014:i:c:p:75-82
- Baur ve Tran (2014): https://econpapers.repec.org/RePEc:spr:empeco:v:47:y:2014:i:4:p:1525-1541
- Lucey ve O'Connor (2017): https://research.ucc.ie/en/publications/are-gold-bugs-coherent/
- Blose, Gondhalekar ve Kort (2018): https://ideas.repec.org/a/spr/jecfin/v42y2018i3d10.1007_s12197-017-9403-0.html
- Reboredo (2013): https://econpapers.repec.org/RePEc:eee:jbfina:v:37:y:2013:i:8:p:2665-2676
- Capie, Mills ve Wood (2005): https://econpapers.repec.org/RePEc:eee:intfin:v:15:y:2005:i:4:p:343-352
- Pukthuanthong ve Roll (2011): https://econpapers.repec.org/RePEc:eee:jbfina:v:35:y:2011:i:8:p:2070-2083
- Sjaastad (2008): https://econpapers.repec.org/RePEc:eee:jrpoli:v:33:y:2008:i:2:p:118-124
- Zhang ve Wei (2010): https://econpapers.repec.org/RePEc:eee:jrpoli:v:35:y:2010:i:3:p:168-177
- Narayan, Narayan ve Zheng (2010): https://econpapers.repec.org/RePEc:eee:appene:v:87:y:2010:i:10:p:3299-3303
- Baur ve Lucey (2010): https://econpapers.repec.org/RePEc:bla:finrev:v:45:y:2010:i:2:p:217-229
- Baur ve McDermott (2010): https://econpapers.repec.org/RePEc:eee:jbfina:v:34:y:2010:i:8:p:1886-1898
- Hood ve Malik (2013): https://econpapers.repec.org/RePEc:eee:revfin:v:22:y:2013:i:2:p:47-52
- Klein, Pham Thu ve Walther (2018): https://econpapers.repec.org/RePEc:eee:finana:v:59:y:2018:i:c:p:105-116
- Dyhrberg (2016): https://econpapers.repec.org/RePEc:eee:finlet:v:16:y:2016:i:c:p:85-92
- Bouri, Gupta, Lahiani ve Shahbaz (2018): https://econpapers.repec.org/RePEc:eee:jrpoli:v:57:y:2018:i:c:p:224-235

**Gün içi, olay, akış**
- Blose ve Gondhalekar (2014): https://econpapers.repec.org/RePEc:taf:apeclt:v:21:y:2014:i:18:p:1269-1272
- Cai, Cheung ve Wong (2001): https://econpapers.repec.org/RePEc:wly:jfutmk:v:21:y:2001:i:3:p:257-278
- Elder, Miao ve Ramchander (2012): https://econpapers.repec.org/RePEc:eee:jbfina:v:36:y:2012:i:1:p:51-65
- Smales (2015): https://econpapers.repec.org/RePEc:eee:intfin:v:34:y:2015:i:c:p:161-172
- Christie-David, Chaudhry ve Koch (2000): https://econpapers.repec.org/RePEc:eee:jebusi:v:52:y:2000:i:5:p:405-421
- Lucca ve Moench (2015): https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf
- Deutsche Bank ETF Granger (ikincil): https://www.tickmill.com/blog/institutional-insights-deutsche-bank-who-drives-gold-prices
- Aalto tezi (ETF): https://epub.lib.aalto.fi/en/ethesis/id/14319 ; PolyU tezi (COT): https://theses.lib.polyu.edu.hk/handle/200/7971 ; Lingnan: https://lingnan.sysu.edu.cn/en/node/3656

**Bu oturumun iç kaynakları**
- `research/r1_viop_kontrat.md`, `r2_kisa_vade_strateji.md`, `r3_kuresel_tahmin.md`, `r4_turkiye_altin.md`
- `out/registry/a1…a8*.csv`, `out/a4_abd_capraz/RAPOR.md`, `out/a5_esz_artik/RAPOR.md`, `out/a7_turkiye/RAPOR.md`, `out/a2_seans_gunici/RAPOR.md`
- Kendi betiğim: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/r5_leadlag_literatur/nonsync_demo.py`
