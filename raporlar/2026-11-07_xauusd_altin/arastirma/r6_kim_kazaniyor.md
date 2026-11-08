# r6_kim_kazaniyor — Altını kısa vadede kim trade ediyor, kim nasıl para kazanıyor?

Tarih: 07.11.2026. Kapsam: 1–5 günlük altın ticareti (VİOP F_XAUUSD odaklı). Önce kazanan grupların gelir kaynakları, sonra perakende sonuçları, sonra Türkiye'ye özgü yapı, kaybettiren hatalar ve bireysel ölçekte gerçekçi "edge" listesi.

**Yöntem ve sınırlar.**
- Bu ajan çalışırken oturumun **web arama bütçesi (200 arama) tükenmişti**. Bu yüzden arama yapılamadı. Bilinen birincil URL'ler doğrudan açıldı (WebFetch). Açılamayanlar "bulunamadı / açılamadı" diye işaretlendi.
- Boşlukları kendi ölçümlerimle doldurdum. Veriler: Dukascopy saatlik ve tick XAUUSD, Yahoo GC=F ve ^GVZ, CFTC COT disaggregated dosyaları, TSPB kaldıraçlı işlem kâr/zarar tablosu, BIST üye bazında hacim dosyaları.
  - Kod: `$S/out/r6_kim_kazaniyor/` (`r6_calc.py`, `cot_small.py`, `tspb_parse.py`, `ticks_spread.py`). Çıktılar: `*_out.txt`, `*.csv`.
- Önceki ajan raporlarındaki (r1, r2, r4) kaynaklı bulgular "(r1)" gibi işaretlendi. Kaynakları o raporlarda.
- `$S` = `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad`

---

## 0. Kısa özet (yük taşıyan bulgular)

1. **Kısa vadeli altın ticareti, maliyetler düşülünce sıfırdan küçük toplamlı bir oyun.** Sistematik kazananlar dört grup:
   - Likidite sağlayanlar: spread ve rebate kazanır.
   - Risk primini taşıyanlar: oynaklık satıcıları, carry ve kira geliri alanlar.
   - Bilanço ve lojistik avantajı olanlar: EFP ve bölgeler arası arbitraj yapan bankalar ve rafineriler.
   - Yavaş trend takipçileri.
   Perakende çoğunlukla bunların karşı tarafında ve maliyeti öder.
2. **Perakende hesapların çoğu zarar ediyor.** Rakamlar:
   - ESMA (27.03.2018): perakende CFD hesaplarının **%74–89**'u zarar ediyor. Müşteri başı ortalama zarar **1.600–29.000 €**.
   - FCA (06.12.2016): **%82**.
   - IG UK sayfası (Kasım 2026): **%70**.
3. **Türkiye: TSPB tablosu** (36 aracı kurum, 2016Ç2–2026Ç3, 42 çeyrek, 1.339 kurum-çeyrek; kendi hesabım):
   - Kârda olan hesapların ortalama payı **%33,1** (medyan %32,0).
   - Kurum-çeyreklerin **%92,7**'sinde zarar edenler kâr edenlerden fazla.
   - Kâr eden payı yalnızca **%6,3**'ünde %50'yi aştı.
   - SPK'nın 10.02.2017 kaldıraç kısıtından (100:1 → 10:1, asgari 50.000 TL) önce ortalama %31,1, sonra %33,4. **Zarar eden payı neredeyse değişmedi.**
4. **Kurum bazında son çeyrek (2026Ç3):**
   - GCM: **%30,12 kâr / %69,88 zarar.**
   - Ahlatcı: **%42 / %58.** Ahlatcı'da 40 çeyreğin **39**'unda zarar edenler fazla.
5. **Akademik kanıt:**
   - Heimer ve Simsek (2019, JFE): ABD 2010 kaldıraç sınırı işlem hacmini **%23** azalttı, yüksek kaldıraçlı traderların zararlarını **%40** hafifletti.
   - Barber, Lee, Liu ve Odean (2014): Tayvan 1992–2006 verisinde günlük traderların **%1'inden azı** ücret sonrası öngörülebilir biçimde kâr ediyor.
6. **COMEX altında piyasa yapıcılık otomatik ve yön almıyor** (CFTC, Haynes ve Roberts 2019; Kasım 2016–Ekim 2018):
   - Altın vadeli hacminin **%67,6**'sı otomatik.
   - Büyük otomatik traderlar hacmin **%50,4**'ünü yapıyor.
   - Bu traderların hacminin **%81,9**'u gün içinde, **%52,9**'u 1 dakika içinde netleşiyor.
   - Yani kazançları yönden değil, spread ve hızdan geliyor.
7. **VİOP F_XAUUSD'nin 7 resmî piyasa yapıcısı var:** İş, Gedik, Vakıf, QNB, Garanti BBVA (banka), Osmanlı, Yatırım Finansman (BIST).
   - Ekim 2026'da USD kıymetli maden vadelilerinde hacim payları: QNB **%22,6**, İş **%19,3**, Yapı Kredi **%17,8**. İlk üç **%59,7**.
   - Yedi piyasa yapıcının toplam payı **%53,2** (BIST aylık üye dosyası).
8. **Trend takipçileri (CTA vekili)** ortalamada kazanıyor ama dalgalı yıllarda kaybediyor. Kendi altın trend vekilim (20/60/120/250 gün işaret ortalaması, %10 oynaklık hedefi, 2,5 bps/yön maliyet):
   - Aralık 2010–Ekim 2026 Sharpe **0,49** (drift çıkarılmış 0,37), yılda ≈ %4.
   - Güçlü yıllar: 2013 (+%11,9, altın −%32,7 iken), 2019, 2024 ve 2025 (+%29,9).
   - Kötü yıllar: 2012, 2015–2017 ve 2021 (−%9,3).
   - SG Trend Index'in altın katkısı **bulunamadı** (SG sayfası 403).
9. **Yönetilen para (managed money) fiyatı takip ediyor, öngörmüyor** (CFTC COT, 2010–2026, 879 hafta):
   - Pozisyon değişimi ile aynı haftanın getirisi: korelasyon **0,49**. Sonraki haftanın getirisi: **−0,002**.
   - Swap dealer'lar (bankalar) yapısal olarak net kısa: ortalama açık pozisyonun **−%21,6**'sı. Ters yönde işlem yapıyorlar (−0,39).
   - Küçük (raporlanmayan) traderlar haftaların **%95,2**'sinde net uzun. Pozisyon değişimlerinin öngörü gücü yok (sonraki hafta −0,02).
10. **EFP kopuşları gerçekten büyük** (kendi ölçümüm, GC=F − Dukascopy spot):
    - 24.03.2020: uzlaşma saatinde ≈ **+31–37 $/ons**. Haziran 2019–Şubat 2020 ay medyanları −2,1 ile +0,7 $.
    - 31.01.2025: **48 $** (günlük medyan).
    - 08.08.2025: **93,4 $**. Aynı Aralık kontratının taşıma tabanı ≈ 53 $, yani ≈ **40 $ ek**.
    - Bu fırsatı kasaya, rafineriye ve uçak kapasitesine erişimi olan banka ve tüccarlar kullanabiliyor. Bireyin erişimi yok.
11. **Oynaklık satıcılarının primi gerçek, ama kuyruğu kalın.** GVZ ile sonraki 21 günde gerçekleşen oynaklığı karşılaştırdım (2010–2026, 4.213 gün):
    - Ortalama **+2,70 puan**. Günlerin **%80,8**'inde GVZ daha yüksekti.
    - En kötü durum **−27,4 puan** (Mart–Nisan 2013 çöküşü).
    - 2025'te prim +0,61, 2026'da +1,19 puana daraldı.
    - **VİOP'ta altın opsiyonu yok** (r1, Prosedür Ek-1). Bu kanal yurt içinde kapalı.
12. **VİOP'ta long taraf carry öder** (06.11.2026 bülteni):
    - F_XAUUSD Şub27/Ara26 yayılımının ima ettiği yıllık carry **%5,25**. Fed aralığı %3,75–4,00. Yani ≈ 1,3–1,5 puan fazla.
    - Gram altın (F_XAUTRYM) yayılımı **%34,47**.
    - Bu fazlayı vadeli satıp spot tutanlar (piyasa yapıcılar, kuyumcular, nakit-taşıma yapanlar) kazanır.
13. **Spread en çok tam yanlış anlarda açılıyor** (Dukascopy tick, Ekim–Kasım 2026):
    - Normal (05.11.2026, 15:00 UTC saati): medyan **0,54 $** (1,32 bps), maksimum 1,19 $.
    - Pazar açılışı (01.11.2026, 23:00 UTC): maksimum **14,96 $** (38,6 bps), ilk dakika medyanı 1,93 $.
    - FOMC sonrası saat (28.10.2026, 19:00 UTC): p90 1,62 $, maksimum 2,80 $.
    - VİOP akşam seansında piyasa yapıcının izin verilen azami spread'i normal seansın 2 katı (2,80 → 5,60 $; r1).
14. **Kaldıraçla yaşanan gerçek risk:**
    - 2026'da 15:00→15:00 UTC günlük getirilerin std'si **%1,80**. Günlerin **%22,3**'ünde |getiri| > %2, **4** günde > %5.
    - En kötü gün 30.01.2026, **−%8,82**.
    - Takasbank PSR %10 ≈ 10 kat kaldıraç. Bu kaldıraçla o gün teminatın ≈ %88'i tek günde gider.
15. **VİOP kapalıyken risk:** Cuma 20:00 → Pazartesi 07:00 UTC getirisinin std'si %0,726. Hafta içi gece aynı saatlerde %0,474. |getiri| > %1 olasılığı **%8,7**'ye karşı %3,9.
16. **Bireysel ölçekte gerçekçi edge kaynakları:**
    - Maliyet disiplini: pazarlıklı komisyonla gidiş-dönüş ≈ 5 bps, varsayılan perakende ≈ 22–25 bps (r1, r2).
    - Yavaş trend ve oynaklıkla boyutlandırma.
    - Carry farkındalığı: F_XAUUSD mi, gram mı?
    - Olay ve kapanış boşluklarında pozisyon küçültme.
    - Fiziki altın tutanlar için nakit-taşıma.
    Hız, EFP lojistiği, Şanghay ithalat lisansı, kira (lease) piyasası ve opsiyon satışı bireye kapalı.

---

## 1. Para nereden nereye akıyor? (çerçeve)

Kısa vadeli vadeli işlemde fiyat değişiminden gelen kâr/zarar, karşı taraflar arasında sıfır toplamlı. Bu toplamdan şunlar çıkar:
- borsa ve takas ücretleri,
- aracı kurum komisyonu ve BSMV,
- spread,
- vergi (VİOP altında %10 stopaj; r1).

Sistematik kazananlar kazançlarını üç kaynaktan alır:
1. **Hizmet bedeli:** spread ve rebate. Piyasa yapıcılar ve HFT.
2. **Risk primi:** oynaklık primi, carry ve kira geliri, trend primi. Bu kazanç uç olaylarda geri ödenir.
3. **Kıt kaynak rantı:** fiziki lojistik, kasa ve rafineri erişimi, ithalat lisansı, bilanço. Arbitrajcılar ve banka bullion masaları.

**Bireysel trader'ın hesabı** (VİOP, 1 sözleşme = 1 ons, 06.11.2026, r1):
- Borsa ve takas taraf başı yüzbinde 4 tutuyor.
- Onbinde 2 komisyon + BSMV ile gidiş-dönüş ≈ 102 TL ≈ **5 bps ≈ 2 $/ons** ediyor.
- Varsayılan perakende komisyonla (onbinde 10) ≈ **22–25 bps** (r2).
- Her gün açıp kapatan biri pazarlıklı tarifeyle yılda nominalin ≈ %12,5'ini (250 × 5 bps), varsayılan tarifeyle ≈ %55'ini maliyete öder. 10 kat kaldıraçta bu, öz sermayenin yılda **%125–550**'si demek.
- Karşılaştırma: yayımlanmış en sağlam trend stratejileri %10 oynaklıkta yılda birkaç puan getiri üretiyor (§2.2).

---

## 2. Kazananlar ve gelir kaynakları

### 2.1 Piyasa yapıcılar ve HFT: spread, rebate, hız

**Kanıt (COMEX altın, CFTC).** Haynes ve Roberts, "Automated Trading in Futures Markets — Update #2", CFTC Baş Ekonomist Ofisi, 26.03.2019. CME işlem verisi; dönemler Kasım 2014–Ekim 2016 ve Kasım 2016–Ekim 2018. https://www.cftc.gov/sites/default/files/2019-04/ATS_2yr_Update_Final_2018_ada.pdf

| Altın vadeli (GC) | 2014–16 | 2016–18 |
|---|---|---|
| Toplam hacim (milyon kontrat, 2 yıl) | 162 | 153 |
| Otomatik (ATS) payı | %65,0 | **%67,6** |
| İki tarafı da otomatik işlemler | %46,1 | %50,2 |
| Bir taraf otomatik, bir taraf manuel | %37,8 | %34,8 |
| Büyük otomatik traderların hacim payı (günlük hacmin ≥ %0,5'i) | %33,7 | **%50,4** |
| Küçük manuel traderların payı | %26,4 | %19,3 |
| Büyük otomatik traderların gün içinde netleşen (yönsüz) hacmi | %64,8 | **%81,9** |
| … 1 dakika içinde netleşen | %34,2 | **%52,9** |
| Büyük trader sayısı değişimi | — | **−%32** (ürünler içindeki en büyük düşüş) |

**Yorum.** Altın vadelisinde büyük otomatik hesaplar hacmin yarısını yapıyor. Hacimlerinin %82'si gün sonunda sıfırlanıyor. Bu, yön almayan piyasa yapıcılık ve arbitraj demek. Gelirleri:
- alış-satış farkı,
- borsa teşvikleri ve rebate,
- kısa ömürlü bilgi (diğer piyasadan önce fiyatı güncellemek).

Baron, Brogaard, Hagströmer ve Kirilenko (2019, JFQA, "Risk and Return in High-Frequency Trading") HFT firmaları arasındaki performans farklarının büyük kısmını göreli gecikmenin (latency) açıkladığını buluyor. Colocation yükseltmeleri performansı artırıyor. Hız avantajı piyasa yapıcılık ve piyasalar arası arbitraj stratejilerine yarıyor. https://econpapers.repec.org/RePEc:cup:jfinqa:v:54:y:2019:i:03:p:993-1024_00
- Özette altına özgü kârlılık sayısı yok. Çalışma ağırlıkla hisse vadelisi üzerine.

**Spread'in zaman profili** (kendi ölçümüm, Dukascopy XAUUSD tick, perakende ECN kotasyonu; `ticks_spread_out.txt`):

| An | Tick | Medyan spread | p90 | Maks |
|---|---|---|---|---|
| 05.11.2026 15:00–16:00 UTC (VİOP uzlaşma saati, Londra–NY örtüşmesi) | 45.959 | **0,54 $ (1,32 bps)** | 0,63 $ | 1,19 $ |
| 28.10.2026 19:00–20:00 UTC (FOMC kararından sonraki saat; karar 18:00 UTC) | 16.128 | 0,74 $ | 1,62 $ | 2,80 $ |
| 25.10.2026 22:00–23:00 UTC (Pazar açılışı, ABD yaz saati) | 3.595 | 0,94 $ | 1,32 $ | 5,82 $ (14,6 bps) |
| 01.11.2026 23:00–24:00 UTC (Pazar açılışı, ABD kış saati) | 15.983 | 0,68 $ (ilk dakika 1,93 $) | 1,22 $ | **14,96 $ (38,6 bps)** |

- NFP ve sakin saat karşılaştırması için indirmeler hız sınırına (HTTP 429) takıldı, bu yüzden yapılamadı. Elde dört saat var.

**VİOP'taki karşılığı** (r1, Prosedür Ek-10/12):
- F_XAUUSD A Grubu sözleşme. Normal ve akşam seansı için ayrı piyasa yapıcılık programları var.
- Azami spread, vadeye 30 günden az kala normal seansta **2,80 $**, akşam seansında **5,60 $**. 90 gün ve üzerinde 4,00 / 8,00 $.
- Asgari kotasyon 20 sözleşme. Piyasada bulunma oranı süresinin %70'i.
- Gerçekleşen tipik spread için birincil veri **bulunamadı** (r1).
- Piyasa yapıcılara özel borsa payı indirimi BIST borsa payı sayfasında **yok**. Prosedür'deki "haklar" ekinin ayrıntısı bu çalışmada okunmadı. https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/borsa-payi

### 2.2 CTA'lar ve trend takipçileri

**Akademik zemin** (r2'de kaynaklı):
- Moskowitz, Ooi ve Pedersen (2012, JFE): 58 vadeli kontrat, 1985–2009. 1–12 aylık zaman serisi momentumu; çeşitlendirilmiş portföyde Sharpe > 1. Altına özgü sonuç makale metninde ayrıca verilmiyor (yerel metin taraması). https://econpapers.repec.org/RePEc:eee:jfinec:v:104:y:2012:i:2:p:228-250
- Altına özgü günlük trend kanıtı zayıf (r2 §3.1).

**SG Trend Index ve altının katkısı:** Société Générale sayfası 403 verdi, veri **bulunamadı**.

**Kendi vekilim: SG Trend benzeri, yalnız altın** (`r6_calc.py` [4]). Kurgu:
- Sinyal: 20, 60, 120 ve 250 günlük getiri işaretlerinin ortalaması.
- Hedef oynaklık %10 (60 günlük σ ile). Pozisyon ±2 ile sınırlı.
- 15:00 UTC spot, bir gün gecikmeli. Maliyet 2,5 bps × |Δpozisyon|.

| Yıl | Trend net (log %) | Al-tut (log %) | Ort. pozisyon |
|---|---|---|---|
| 2011 | +11,5 | +10,7 | +0,44 |
| 2012 | −6,9 | +5,6 | +0,09 |
| **2013** | **+11,9** | **−32,7** | −0,37 |
| 2014 | −1,2 | −0,4 | −0,28 |
| 2015 | −3,6 | −11,7 | −0,43 |
| 2016 | −2,0 | +8,8 | +0,24 |
| 2017 | −4,9 | +11,5 | +0,18 |
| 2018 | +2,0 | −1,6 | −0,06 |
| 2019 | +12,3 | +17,1 | +0,44 |
| 2020 | +9,0 | +22,0 | +0,49 |
| 2021 | **−9,3** | −3,8 | −0,10 |
| 2022 | +0,7 | −0,2 | −0,06 |
| 2023 | +1,3 | +12,6 | +0,36 |
| 2024 | +12,1 | +23,7 | +0,58 |
| **2025** | **+29,9** | +50,8 | +0,55 |
| 2026 (Kas. 6'ya kadar) | +2,1 | −7,1 | +0,05 |

- Tüm dönem Sharpe 0,49, drift çıkarılmış 0,37, yıllık ortalama ≈ %4,05. Yıllık devir 18,2 kat, ortalama |pozisyon| 0,44.
- Sonuç: trend takipçisi altında **uzun ve kesintisiz trendlerde** (2013 düşüşü, 2019–20 ve 2024–25 yükselişleri) kazanıyor. **Dalgalı ve yön değiştiren yıllarda** (2012, 2015–17, 2021) kaybediyor.
- 1–5 günlük tutuş için anlamı: sinyal yavaş değişir. Kazanç günlük işlem yapmaktan değil, pozisyonu taşımaktan gelir.

**CTA ve yönetilen paranın davranışı** (CFTC COT, COMEX altın 088691, 05.01.2010–03.11.2026, 879 hafta; `cot_small_out.txt`). Ortalama net pozisyon (açık pozisyona oranla):

| Grup | Ortalama net | Δ ile aynı hafta getirisi | Δ ile sonraki hafta getirisi | Seviye ile önceki 13 hafta getirisi |
|---|---|---|---|---|
| Managed money (CTA, makro fon) | +%21,3 | **+0,49** | −0,002 | +0,48 |
| Swap dealer (banka) | **−%21,6** | −0,39 | +0,03 | −0,32 |
| Producer/merchant | −%17,9 | −0,36 | −0,03 | −0,19 |
| Other reportable | +%13,0 | −0,20 | +0,01 | −0,01 |
| Raporlanmayan (küçük) | +%5,1 | +0,17 | −0,02 | +0,37 |

- **Yönetilen para fiyatın peşinden gidiyor.** Hem aynı hafta hem geçmiş 13 haftayla güçlü pozitif ilişki var. Sonraki haftayı öngörmüyor.
- Swap dealer'lar, üreticiler ve diğerleri karşı taraf. Bu yapı, trend takipçilerinin likiditeyi tükettiğini, bankaların ve fiziki oyuncuların sağladığını gösteriyor.
- WGC (Ocak 2025 piyasa yorumu): "COMEX managed money net longs added US$64bn (150t)". https://www.gold.org/goldhub/research/gold-market-commentary-january-2025

### 2.3 Makro fonlar

Makro fonların altın işlemlerine özgü performans verisi **bulunamadı**. COT'ta CTA'larla aynı "managed money" kategorisindeler (§2.2). Kazanç kanalı orta vadeli sürücülerdir (reel faiz, dolar, merkez bankası talebi; r3). 1–5 gün ufkunda ayrıca bir kanıt yok.

### 2.4 Banka bullion masaları: müşteri akışı, kira, EFP, fiziki lojistik

**Yapı.**
- Swap dealer kategorisi COMEX altında yapısal olarak net kısa: ortalama açık pozisyonun %21,6'sı, haftaların %93,4'ünde net kısa (`cot_small_out.txt`).
- Bunun nedeni, müşterilere ve üreticilere sattıkları OTC forward, opsiyon ve hesap altını pozisyonlarını borsada hedge etmeleri.
- Gelir kalemleri: müşteri spread'i, metal kiralama (lease) geliri, Londra–New York EFP ve bar dönüşümü, kasa hizmetleri.
- Lease oranlarının 2020 ve 2025 seviyelerine ait birincil veri **bulunamadı**.

**EFP kopuşları: kendi ölçümüm** (`efp_proxy_daily_2024_2026.csv`, `r6_calc_out.txt` [1a–1b]). Ölçü: GC=F (Yahoo, sürekli ön kontrat) eksi Dukascopy spot.
- Ön ay kontratına kadarki taşıma maliyetini (faiz − kira) içerir. Yahoo kontrat değiştirdiğinde (roll) sıçrar. Bu yüzden "olağan taban" ile karşılaştırılmalı.

| Olay | Ölçüm | Olağan taban | Fazlalık |
|---|---|---|---|
| Mart 2020 (pandemi, rafineri ve uçuş kesintisi) | 24.03.2020: **+36,7 $** (13:30 ET varsayımı) / +30,6 $ (17:00 ET). 23–26.03.2020: 13–37 $ | 2019-06 → 2020-02 ay medyanları −2,1 ile +0,7 $ (iki saat varsayımı); Nisan 2020 kontratı vadeye çok yakın | ≈ **30–37 $/ons** |
| Aralık 2024 – Şubat 2025 (gümrük vergisi korkusu, COMEX'e akış) | 11.12.2024: 36,1 $; 19–20.01.2025: 40–42 $; **31.01.2025: 48,2 $**; 02.02.2025: 41,6 $ | Aynı kontratta (Şubat 2025) Aralık–Ocak tabanı ≈ 12–23 $ | ≈ 20–35 $ |
| Ağustos 2025 (külçe sınıflandırma ve gümrük vergisi belirsizliği) | 07.08.2025: 69,0 $; **08.08.2025: 93,4 $**; 10.08.2025: 64,7 $; 12.08.2025: 50,5 $ | Aralık 2025 kontratına geçişten sonra (30.07–06.08.2025) 52–55 $ | ≈ **40 $** |
| Ağustos 2026 | 55–60 $, sıçrama yok | Aralık 2026 kontratının taşıma maliyeti | ≈ 0 |

- Saatlik karşılaştırma 2024-06 → 2026-10 için. Mart 2020 günlük, yani gün içi sapma gürültüsü taşıyor.
- WGC Şubat 2025 yorumu (06.03.2025): altının Şubat'taki gücünü "continued flows of gold into COMEX inventories, driven by continued tariff uncertainty" ile açıklıyor. Ton verisi yok. https://www.gold.org/goldhub/research/gold-market-commentary-february-2025
- Basında geçen "EFP gün içinde 70 $'ı aştı", "Bank of England kasa kuyruğu" gibi ayrıntıların birincil kaynağı bu çalışmada **açılamadı**.

**Kim kazandı?**
- Londra'da 400 onsluk külçeyi alıp İsviçre'de 1 kg veya 100 ons bara döktürebilenler.
- Uçakla New York'a taşıyabilenler.
- Pahalı COMEX vadelisini satıp teslim edebilenler.
Bu, rafineri kapasitesi, kasa, sigorta, kredi limiti ve borsa teslim yetkisi gerektirir. **Bireyin erişimi yok.** Bireyin bu olaylardaki tek ilişkisi şu: VİOP vade sonu LBMA PM'ye bağlı (r1), yani EFP kopuşu VİOP ile COMEX arasındaki farkı da oynatır.

**Emir defteri manipülasyonu da bir "gelir" kaynağıydı** (stop avı/spoofing riskinin kanıtı). CFTC 29.09.2020: JPMorgan, en az 2008–2016 arasında COMEX ve NYMEX altın, gümüş, platin ve paladyum vadelilerinde (ve Hazine vadelilerinde) "hundreds of thousands of spoof orders" verdi. Toplam **920,2 milyon $** ödedi:
- tazminat 311,7 milyon $,
- kazanç iadesi 172,0 milyon $,
- para cezası 436,4 milyon $.
https://www.cftc.gov/PressRoom/PressReleases/8260-20

### 2.5 Baz ve carry ticareti

- **Teori:** Altında vadeli fiyat ≈ spot × (1 + (USD faizi − kira oranı) × süre). Carry küçük ve istikrarlı (Koijen ve diğ. 2018, JFE; r2). https://econpapers.repec.org/RePEc:eee:jfinec:v:127:y:2018:i:2:p:197-225
- **VİOP'ta long taraf ABD faizinin üstünde carry ödüyor.**
  - 06.11.2026: F_XAUUSD0227 4.112,4 / F_XAUUSD1226 4.078,8, 57 gün → **%5,25 yıllık** (kendi hesabım, BIST bülteni). Aynı dönemde Fed hedef aralığı %3,75–4,00 (Fed, 16.09.2026; r3).
  - r4'ün 2026 takvim yayılımı medyanı %7,18. 3 aylık ABD Hazine bonosu ortalaması %3,84.
  - Long pozisyon spot sentetiğe göre seans başına ≈ −%0,034 geride kalıyor (5 seansta −%0,17; r4).
- **Gram altın (F_XAUTRYM):** Şub27/Ara26 yayılımı **%34,47**. VİOP USDTRY Ara26 52,281 / Kas26 51,008. Long pozisyon spot gram pariteye göre seans başına ≈ −%0,166 geride kalıyor (Nisan 2025–Ekim 2026; r4).
- **Kim kazanır?** Pahalı vadeliyi satıp ucuz spotu tutabilenler:
  - piyasa yapıcılar (yurt dışı spot veya forex hedge),
  - fiziki altını olan kuyumcu ve bankalar (nakit-taşıma, §4.3),
  - vadeler arası (takvim) yayılım tutanlar.
- Bireysel long trader bu farkı **öder**. 5 günlük ons long'da ≈ 0,17 puan, gram long'da ≈ 0,8 puan (r4).

### 2.6 Oynaklık satıcıları

**Kendi ölçümüm** (`r6_calc_out.txt` [2]): GVZ (CBOE 30 günlük altın ETF ima oynaklığı, Yahoo) ile sonraki 21 işlem gününde gerçekleşen oynaklık (spot 20:00 UTC, √252) karşılaştırması. 05.01.2010–08.10.2026, 4.213 gün.

| | Değer |
|---|---|
| Ortalama GVZ − RV | **+2,70 puan** (medyan +3,11) |
| GVZ > RV gün payı | **%80,8** |
| %5'lik dilim | −5,04 puan |
| En kötü | **−27,4 puan** (26.03–09.04.2013 başlangıçlı pencereler: GVZ ≈ 12–13, gerçekleşen ≈ 40) |
| 2025 / 2026 ortalaması | +0,61 / +1,19 puan; pozitif gün payı %67 / %63 |

- Akademik destek: Prokopczuk, Symeonidis ve Wese Simen (2017, JBF). 21 emtianın neredeyse tamamında varyans risk primi anlamlı negatif. Eşit ağırlıklı kısa varyans swap portföyünün yıllık Sharpe'ı ≈ 0,40 (r2). https://econpapers.repec.org/RePEc:eee:jbfina:v:81:y:2017:i:c:p:136-149
- **Mekanizma:** Opsiyon satıcısı çoğu ay küçük prim kazanır, çöküş haftalarında (Nisan 2013, Mart 2020, Ocak 2026) büyük öder. 2025–26'da gerçekleşen oynaklık arttığı için prim daraldı.
- **VİOP'ta altın opsiyonu yok** (r1, Prosedür Ek-1). Ekim 2026 BIST üye dosyasında da opsiyon sayfaları yalnız endeks, pay ve döviz için. Yurt içi bireysel trader bu kanalı kullanamaz. Yurt dışı (COMEX OG) erişimi aracı kurum ve vergi meselesi; bu çalışmada incelenmedi.

### 2.7 Olay traderları

- Elder, Miao ve Ramchander (2012, JBF), 2002–2008 tick verisi (r2):
  - ABD 08:30 ET verileri en etkili. NFP, altının 5 dakikalık getiri varyansının %35'ini açıklıyor.
  - Etki dakikalar içinde fiyatlanıyor. Çok günlük sürüklenme kanıtı yok.
  - https://econpapers.repec.org/RePEc:eee:jbfina:v:36:y:2012:i:1:p:51-65
- **Kazananlar:** İlk saniyeleri hız sahipleri alıyor (§2.1). Olaydan sonra "yön" kenarı kanıtsız. Kalan getiri oynaklık primi gibi davranıyor.
- **LBMA fiksing sızıntısı:** Caminschi ve Heaney (2014, JFM), eski telefonlu fiksingde (2015 öncesi) vadeli fiyatın fiks sonucunu dakikalar önce yansıttığını buluyor. Fiks yönüyle uyum 15:01'de %69,9, 5 dakika içinde %80. Mart 2015'ten beri IBA elektronik ihalesi var. Kalıcı sürüklenme kanıtı bulunamadı (r2). https://econpapers.repec.org/RePEc:wly:jfutmk:v:34:y:2014:i:11:p:1003-1039

### 2.8 Merkez bankası ve ETF akışını önden okuyanlar

- **ETF akışı:** Deutsche Bank'ın Granger testi fiyatın akışa öncülük ettiğini buluyor (r2). Akış verisi aylık ve gecikmeli (WGC). 1–5 günlük öngörü kanıtı **bulunamadı**.
- **Merkez bankaları:**
  - Q3 2026'da merkez bankaları **321 t** aldı (WGC, 03.11.2026; r3).
  - Bu veri çeyrek sonunda ve IMF verisiyle gecikmeli geliyor. Önden okuma kanıtı **bulunamadı**.
  - TCMB'nin Mart 2026 satış/swap haberleri ile onsun ≈ %17 düşüşü aynı haftalara denk geldi. Nedensellik kurulamadı (r4).
- **Kim kazanır?** Akış bilgisine erken erişen külçe bankaları (müşteri akışını görenler). Bunun ölçülebilir kanıtı yok. Bireysel düzeyde kanal yok.

### 2.9 Arbitrajcılar: COMEX – Londra – Şanghay – Dubai – İstanbul

| Hat | Mekanizma | Ölçek ve kanıt | Bireysel erişim |
|---|---|---|---|
| COMEX–Londra | EFP, bar dönüşümü, nakliye | §2.4: 2020'de ≈ 30–37 $, 2025'te ≈ 20–40 $ fazlalık | Yok |
| Şanghay–Londra | Çin ithalatı lisanslı; prim/iskonto ithalat kanalıyla kapanır | Meader (LBMA Alchemist 83), 2005–2016: boğa döneminde ≥ %1 prim sonrası 1 ayda LBMA AM ortalama +33 $. Yazar etkiyi "mütevazı" buluyor (r2). https://www.lbma.org.uk/alchemist/issue-83/links-between-the-chinese-and-international-gold-prices | Yok |
| Dubai | Hindistan/Afrika akışı, iskonto | Birincil veri **bulunamadı** | Yok |
| İstanbul–Londra | Kapalıçarşı/KMKTP primi; 07.08.2023'ten beri HMB ithalat kotası | Metals Focus: 2023'te prim zirvesi 150 $/ons, Mart 2024'te 200 $/ons. Kasım 2026'da toptan prim ≈ 0 (r4) | Fiziki al-sat ile kısmen, makas ≈ %3 |
| VİOP gram – VİOP ons × VİOP USDTRY | Üç bacaklı sentetik | 2025: ort. +%0,018 (std %0,084); 2026: ort. +%0,020 (std %0,081); %5–95 bandı −%0,107 / +%0,162 (r4) | Bant maliyetin içinde. Piyasa yapıcıların alanı |

Hauptfleisch, Putniņš ve Lucey (2016, JFM): New York vadelisi, Londra spot hacminin onda birinden az hacme rağmen fiyat keşfinde daha büyük rol oynuyor (r2). Yani bölgeler arası farkı ilk kapatanlar vadeli piyasadaki hızlı katılımcılar.

---

## 3. Perakende sonuçları

### 3.1 Avrupa ve İngiltere

- **ESMA (27.03.2018):**
  - Perakende CFD hesaplarının "**74-89%**"u zarar ediyor. Müşteri başı ortalama zarar 1.600–29.000 €.
  - Yeni kaldıraç sınırları: majör pariteler 30:1; **altın, majör olmayan pariteler ve majör endeksler 20:1**; diğer emtialar 10:1; tek hisseler 5:1; kripto 2:1.
  - Teminat %50'ye inince pozisyon kapatılır. Hesap bazında negatif bakiye koruması var.
  - https://www.esma.europa.eu/press-news/esma-news/esma-agrees-prohibit-binary-options-and-restrict-cfds-protect-retail-investors
- **FCA:**
  - 06.12.2016 (CP16/40 duyurusu): temsilî örneklemde müşterilerin **%82**'si zarar etti. https://www.fca.org.uk/news/press-releases/fca-proposes-stricter-rules-contract-difference-products
  - PS19/18 (Temmuz 2019): altında asgari teminat **%5 (20:1)**. CFD için yürürlük **01.08.2019**. Firmalar "X% of retail investor accounts lose money" uyarısını kendi güncel oranlarıyla yayımlamak zorunda. https://www.fca.org.uk/publication/policy/ps19-18.pdf
- **IG UK** (sayfa, Kasım 2026): "70% of retail investor accounts lose money when trading spread bets and CFDs with this provider." https://www.ig.com/uk
- **Altına özgü** perakende CFD zarar oranı **bulunamadı**. Raporlar tüm CFD'leri birlikte veriyor.

### 3.2 Türkiye: SPK düzenlemesi ve aracı kurum açıklamaları

- **SPK 10.02.2017 değişikliği** (III-37.1, RG 29975):
  - Forex'te azami kaldıraç **100:1'den 10:1'e** indi.
  - Pozisyon açmadan önce asgari **50.000 TL** veya karşılığı döviz teminat şartı geldi.
  - Mevcut pozisyonlara 45 gün uyum süresi verildi.
  - https://spk.gov.tr/duyurular/basin-duyurulari/2017/yatirim-hizmetleri-ve-faaliyetleri-ile-yan-hizmetlere-iliskin-esaslar-hakkinda-tebligde-iii-37-1-degisiklik-yapilmasina-dair-teblig-hakkinda
- **Güncel çerçeve:** SPK "Yatırım Hizmet ve Faaliyetleri ile Yatırım Kuruluşlarına İlişkin Rehber", son güncelleme i-SPK.37.8 (10.03.2026). Yerel kopya: `$S/dl_spk/rehber.txt`; spk.gov.tr'deki tam URL bu çalışmada **bulunamadı**. Rehber şunları söylüyor:
  - Aracı kurumlar internet sitesindeki "**Zarar Olasılığınız**" menüsünde kâr/zarar oranlarını çeyrek dönemler halinde (Ocak–Mart, Nisan–Haziran, Temmuz–Eylül, Ekim–Aralık) yayımlıyor.
  - Hesaplama "hesap bazında gerçekleşmiş kar/zarar dikkate alınarak" yapılıyor.
  - Müşteriden alınan beyandaki kâr/zarar dağılımı internet sitesindekiyle aynı olmalı.
  - Rehber ayrıca Tebliğ md. 27'ye atıfla 20.000 TL ve 30.000 TL teminat eşiklerinden söz ediyor. Bu eşiklerde kaldıraç "ikinci fıkradaki oranlara" yükseltilebiliyor. **Güncel madde metni ve oranları açılamadı** (mevzuat.gov.tr 404).
  - GCM ana sayfası "Forex işlemlerinde kaldıraç oranı 1:10 olarak belirlenmiştir" diyor (Kasım 2026).
- **TSPB toplu tablosu** (36 kurum; kendi hesabım: `tspb_parse.py`, `tspb_kar_zarar.csv`). Kaynak: https://tspb.org.tr/kaldiracli-islem-bildirimleri/ → https://tspb.org.tr/wp-content/uploads/2026/11/1_TSPB-Kar-Zarar-2026-3.xlsx

| | Değer |
|---|---|
| Kapsam | 2016Ç2–2026Ç3, 42 çeyrek, 1.339 kurum-çeyrek gözlemi |
| Kârda olan hesap payı (kurumlar arası basit ortalama) | **%33,1** (medyan %32,0) |
| Zarar eden > kâr eden olan kurum-çeyrek payı | **%92,7** |
| Kâr eden payı > %50 olan kurum-çeyrek payı | %6,3 |
| En iyi çeyrek (ortalama) | 2022Ç4: %48,0 |
| En kötü çeyrek | 2016Ç4: %20,0 |
| 2026Ç1 / Ç2 / Ç3 ortalaması | %29,7 / %25,6 / %37,1 |
| SPK kısıtı öncesi (2016Ç2–Ç4) / sonrası (2017Ç2–2026Ç3) | %31,1 / %33,4 |

  - Sınırlar: Kurumlar arası basit ortalama (hesap sayısı yok, ağırlıklandırılamadı). Altına özgü değil, tüm kaldıraçlı işlemler. "Gerçekleşmiş" kâr/zarar, açık pozisyon zararını dışarıda bırakabilir.
- **Kurum örnekleri (2026Ç3):**
  - GCM: kâr **%30,12**, zarar **%69,88**. https://www.gcmyatirim.com.tr/sirket-profili/yasal-bildirimler/zarar-olasiliginiz
  - Ahlatcı: kâr **%42**, zarar **%58**. 2016Ç4–2026Ç3 arasındaki 40 çeyreğin 39'unda zarar eden payı yüksek. En düşük kâr payı 2018Ç3 (%14,89), en yüksek 2024Ç4 (%53). 2026Ç2 %17, 2026Ç1 %28. Reddedilen emir payı (2026Ç3) %0,32. Fiyat sağlayıcıları: FXCM, Swissquote, Finalto, Infinox. https://www.ahlatciyatirim.com.tr/hakkimizda/zarar-olasiliginiz

### 3.3 Akademik kanıt (perakende kaldıraç ve günlük işlem)

- **Heimer ve Simsek (2019, JFE, "Should retail investors' leverage be limited?").** ABD perakende forex'te 2010 kaldıraç sınırının etkileri:
  - İşlem hacmi **−%23**.
  - Yüksek kaldıraçlı traderların zararları **%40** hafifledi.
  - Aracı kurumların faaliyet sermayesi **−%25**.
  - Aracı kurumların göreli alış-satış fiyatlamasında değişiklik yok.
  - https://econpapers.repec.org/RePEc:eee:jfinec:v:132:y:2019:i:3:p:1-21
  - Türkiye için anlamı: 2017 kısıtı zarar eden **hesap payını** pek değiştirmedi (TSPB, §3.2). Heimer ve Simsek'e göre asıl etki zararın **büyüklüğünde** beklenir. Türkiye için büyüklük verisi **bulunamadı**.
- **Barber, Lee, Liu ve Odean (2014, JFM).** Tayvan günlük traderları, 1992–2006:
  - Önceki yılın en iyi 500 trader'ı sonraki yıl ücret öncesi günde 61,3 bps, ücret sonrası **37,9 bps** kazanıyor.
  - En kötüler ücret sonrası −28,9 bps.
  - **%1'inden azı** "predictably and reliably" ücret sonrası pozitif anormal getiri elde ediyor.
  - https://econpapers.repec.org/RePEc:eee:finmar:v:18:y:2014:i:c:p:1-24
- Chague, De-Losso ve Giovannetti'nin Brezilya vadeli günlük trader çalışması (SSRN 3423101): sayfa 403 verdi, **teyit edilemedi**. Rakamları burada kullanmıyorum.

### 3.4 Prop firmaları

- **FTMO** (ana sayfa, Kasım 2026):
  - "4.5M+ Customers worldwide", "$650M+ Paid in rewards".
  - En önemlisi: "all accounts we provide to our clients are demo accounts with fictitious funds".
  - Yani "fonlanmış" trader gerçek piyasada işlem yapmıyor. Gelir modeli değerlendirme ücreti; ödüller simüle kâra göre ödeniyor.
  - Kaba ölçek: 650 milyon $ / 4,5 milyon müşteri ≈ **müşteri başı 144 $** toplam ödül. Bu üst sınır, çünkü müşteri ≠ hesap. Ücret gelirleri açıklanmadığı için net akış hesaplanamadı.
  - https://ftmo.com/en/
- Geçme oranı ve ödeme alan trader payı için birincil veri **bulunamadı**. CFTC'nin MyForexFunds basın duyurusu (8771-23) 403 verdi, **açılamadı**.
- Türkiye'de SPK lisanslı prop firması verisi **bulunamadı**.

### 3.5 Altın özelinde perakende davranışı (COMEX küçük traderlar)

- Raporlanmayan (küçük) traderlar 2010–2026 haftalarının **%95,2**'sinde net uzun. Ortalama net pozisyon açık pozisyonun +%5,1'i.
- Pozisyon değişimleri hafif trend takipçisi: aynı hafta getirisiyle +0,17, önceki 13 hafta getirisiyle +0,37.
- Sonraki haftayı öngörmüyor: −0,02. Net pozisyon seviyesi sonraki 4 haftayı da öngörmüyor: −0,03.
- Net işaret ile sonraki hafta yönü %54,8 oranında aynı. Bu, beceriden çok altının 2010–2026'daki yükseliş eğilimiyle uyumlu.
- Perakende CFD duyarlılık endekslerine (IG Client Sentiment vb.) dayalı akademik test **bulunamadı**.

---

## 4. Türkiye'ye özgü

### 4.1 VİOP altın piyasa yapıcıları ve hacim yoğunlaşması

- **Piyasa yapıcılar** (BIST, Kıymetli Madenler Vadeli): https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/piyasa-yapicilik

| Kurum | Dolar/Ons Altın | Gram Altın | Dolar/Ons Gümüş |
|---|---|---|---|
| İş Yatırım | ✓ | ✓ | ✓ |
| Gedik Yatırım | ✓ | | ✓ |
| Vakıf Yatırım | ✓ | | ✓ |
| QNB Yatırım | ✓ | ✓ | ✓ |
| Türkiye Garanti Bankası | ✓ | ✓ | |
| Osmanlı Yatırım | ✓ | ✓ | ✓ |
| Yatırım Finansman | ✓ | ✓ | |

- **Üye bazında hacim** (Ekim 2026, "Kıymetli Madenler Vadeli İşlem Sözleşmeleri USD": XAUUSD, XAGUSD, XPT, XPD). Toplam **519,2 milyar TL**, 53 üye. Kaynak: https://www.borsaistanbul.com/data/vadeli/viopaylikishac202610.zip (dizin listesi: https://www.borsaistanbul.com/files/datafilepaths_viop.zip)

| Üye | Pay |
|---|---|
| QNB Yatırım (PY) | **%22,6** |
| İş Yatırım (PY) | **%19,3** |
| Yapı Kredi Yatırım | %17,8 |
| Ak Yatırım | %6,8 |
| TEB Yatırım | %5,6 |
| GCM Yatırım | %5,2 |
| Garanti Bankası (PY) | %3,9 |
| Garanti Yatırım | %2,3 |
| Vakıf (PY) / Yatırım Finansman (PY) / Gedik (PY) / Osmanlı (PY) | %2,0 / %1,9 / %1,8 / %1,6 |

  - İlk üç üye %59,7. Yedi piyasa yapıcı toplam **%53,2**.
  - Üye hacmi kurumun müşteri işlemleriyle kendi hesabını birlikte içerir. Ayrıştırma **yapılamıyor**.
- **Yabancı payı** (tüm VİOP, ürün kırılımı yok): 2013'te %24,7, 2026 Ocak–Ekim'de **%44,1**, Ekim 2026'da %45,9. https://www.borsaistanbul.com/data/vadeli/viopyyishac202610.zip

### 4.2 VİOP–spot/forex arbitrajı

- **Uzlaşma ve vade sonu bağı:**
  - Günlük uzlaşma 15:00–15:10 UTC VWAP.
  - Vade sonu LBMA PM (r1). Ekim 2026'da ön vade uzlaşması 15:00 UTC spotun −0,5 ile +9,2 $ üstündeydi; bu, taşıma maliyetiyle tutarlı (r1).
- **Gram–sentetik bandı** 2025–26'da ±%0,15 (r4). Üç bacaklı işlemin komisyon, BSMV ve spread maliyetine yakın, yani **piyasa yapıcının alanı**.
- **Arbitrajcı ne kazanır?** VİOP ons'un ABD faizi üstündeki ek carry'si (06.11.2026'da ≈ 1,3–1,5 puan; r4'te 2026 medyanı ≈ +3,3 puan).
  - Bunu, VİOP'ta satıp yurt dışı spot veya forex'te alan kurum alır.
  - Bireysel trader için forex tarafındaki swap maliyeti ve kaldıraç kuralları bu farkı muhtemelen yer. Swap oranları bu çalışmada ölçülmedi.

### 4.3 Kuyumcuların ve bankaların hedge'i, TL carry'si

- **Nakit-taşıma (cash-and-carry):** Fiziki altın + VİOP gram short ≈ TL faizi. 2026'da yıllık carry ≈ %34–43 (06.11.2026 yayılımı %34,47; r4'te 2026 medyanı %43,4).
  - Kuyumcu stokunu ya da hane altınını "faizlendirmenin" yolu bu.
  - Riskleri: Kapalıçarşı primindeki değişim (baz), teminat, stopaj (r4).
  - Kuyumcuların VİOP'u ne ölçüde kullandığına dair birincil veri **bulunamadı**. Bu bölüm mekanizma ve r4 ölçümüne dayanıyor.
- **Bankalar:** Kıymetli maden depo hesapları ≈ 4,74 trilyon TL ≈ **717 t** altın eşdeğeri (r4, BIST KMKTP Eylül 2026). Bankalar bu yükümlülüğü TCMB zorunlu karşılığı, KMKTP, LBMA ve VİOP ile yönetiyor. Garanti Bankası doğrudan VİOP gram ve ons piyasa yapıcısı (§4.1).
- **Bireysel trader için sonuç:**
  - F_XAUTRYM long, ons long + yüksek carry'li USDTRY long demek. Kısa vadede kur katkısı ≈ +%0,07/gün, carry ≈ −%0,17/seans; net ≈ **−%0,1/seans** ters rüzgâr (r4).
  - 1–5 günlük yön işlemi için F_XAUUSD daha "temiz" araç: carry'si küçük, akşam seansı var.

### 4.4 Akşam seansı kullanımı

- Seans 19:00–23:00 TSİ (16:00–20:00 UTC). Altında 18.09.2020'de başladı (BIST duyurusu 12590).
- BIST duyurusu 30572 (19.11.2024) ekindeki Prosedür md. 7 Dolar/Ons Altın'ı akşam seansı listesinde sayıyor. **Teyit edildi**; duyurunun konusu bakır vadelisi. https://borsaistanbul.com/files/duyuru-30572-TR.pdf
- Akşam hacmi toplamın medyan **%7,3**'ü (r1).
- Akşam seansında piyasa emri yok. Piyasa yapıcının azami spread'i normal seansın 2 katı (5,60 $).
- Kullanım: FOMC (kışın 19:00 UTC) ve ABD öğleden sonra olaylarına canlı tepki. Uzlaşmadan uzlaşmaya getirinin anlamlı kısmı 15:10–20:00 UTC arasında oluşuyor (r1).
- Gram altın ve USDTRY akşam seansında **yok**.

---

## 5. Kaybettiren tipik hatalar (rakamlarla)

1. **Aşırı kaldıraç.**
   - 2026'da 15:00→15:00 UTC spot getirisinin std'si %1,80. Günlerin %22,3'ünde |r| > %2, %7,7'sinde > %3, 4 günde > %5. En kötü gün 30.01.2026, −%8,82 (`r6_calc_out.txt` [5c]).
   - 2010–2026 bütününde std %1,02.
   - Takasbank PSR %10 (r1) ≈ 10 kat. 10 kat kaldıraçta 2026'nın tipik günü öz sermayede ≈ ±%18, en kötü günü ≈ −%88 demek.
   - Heimer ve Simsek'e göre kaldıracı kısmak zararları %40 azaltıyor.
2. **Kapalı piyasa ve boşluklar.**
   - Dukascopy'de hafta sonu açılış boşluğu küçük (2010–2026, 859 hafta): ortalama |boşluk| %0,127, p99 %1,28, maksimum %2,45 (15.03.2020 açılışı). 13 haftada > %1, 2 haftada > %2.
   - VİOP trader'ının taşıdığı risk daha geniş: Cuma 20:00 → Pazartesi 07:00 UTC std'si %0,726, hafta içi gecede %0,474. > %1 hareket olasılığı %8,7'ye karşı %3,9.
   - Türkiye tatillerinde VİOP kapalıyken küresel piyasa açık. Tatil dönüşü getirisi çok günlük hareketi tek seferde yansıtır (r2).
3. **Maliyet ve aşırı işlem.**
   - Pazarlıklı gidiş-dönüş ≈ 5 bps, varsayılan ≈ 22–25 bps (r1, r2). Sharpe'ı 0,5 olan bir sinyal %18 oynaklıkta günde ≈ 3,6 bps getiriyor (r2).
   - Her gün dönen strateji varsayılan komisyonla kesin zarar eder.
   - Barber ve diğ.: günlük traderların %1'inden azı kalıcı kârlı.
4. **Haber anında spread genişlemesi.** Pazar açılışında spread normalin 28 katına (14,96 $ / 0,54 $) çıkabiliyor. FOMC sonrası saatte p90 3 kat (§2.1). Stop emirleri en kötü fiyattan dolar.
5. **Stop avı ve sahte emir.**
   - Büyük bankaların emir defterinde sahte emirle fiyatı ittiği belgelendi: JPMorgan, 2008–2016, 920,2 milyon $ (§2.4).
   - Bireysel düzeyde korunma: ince likiditede (akşam seansı, Pazar açılışı, Asya sabahı) bariz yuvarlak seviyelere stop koymamak, limit emir kullanmak.
6. **Yanlış enstrüman ve carry.** Gram altın long'unu 5 gün taşımak spot pariteye göre ≈ 0,8 puan kaybettirir (r4). Ons long'da bu ≈ 0,17 puan. Bu kayıp yön tahmini doğru olsa bile yaşanır.
7. **Trend aleyhine "ucuzladı" alımı (anchoring).** Küçük traderlar haftaların %95'inde net uzun. Pozisyonları sonraki haftayı öngörmüyor (§3.5).

---

## 6. Bireysel trader için gerçekçi "edge" kaynakları

| Kaynak | Kim kazanıyor | Bireysel erişim | Beklenen büyüklük ve not |
|---|---|---|---|
| Spread, rebate, hız (HFT) | Otomatik piyasa yapıcılar | **Yok** | Latency rekabeti (Baron ve diğ. 2019) |
| EFP / bar dönüşümü / nakliye | Banka, rafineri, tüccar | **Yok** | 2020: ≈ 30–37 $; 2025: ≈ 20–40 $/ons fazlalık, kısa sürer |
| Şanghay / İstanbul ithalat primi | Lisanslı ithalatçı | **Yok** (ancak fiziki prim ticareti, %3 makas) | Prim tavanı kotaya bağlı (r4) |
| Opsiyon satışı (VRP) | Opsiyon satıcıları | VİOP'ta altın opsiyonu **yok** | +2,7 vol puanı ortalama, −27 puan kuyruk |
| Kira (lease) / metal ödünç | Merkez bankaları, bankalar | **Yok** | Veri bulunamadı |
| VİOP ons ek carry'si (short VİOP, long spot) | Piyasa yapıcı, kurum | Kısmen (forex swap maliyeti belirsiz) | ≈ 1,3–3,3 puan/yıl |
| Nakit-taşıma (fiziki + VİOP gram short) | Kuyumcu, banka, fiziki altını olan hane | **Var** (fiziki altını olan için) | ≈ TL faizi − baz riski (2026 ≈ %34–43 brüt) |
| Yavaş trend + oynaklık hedefi | CTA'lar | **Var** | Altın vekilinde Sharpe ≈ 0,4–0,5. Dalgalı yıllarda zarar. Devir yılda ≈ 18 kat, maliyet duyarlı |
| Maliyet minimizasyonu | Herkes | **Var** | 22 → 5 bps, işlem başına ≈ 17 bps kazanç |
| Olay/oynaklık rejimine göre boyutlandırma | Risk yöneticileri | **Var** | Getiri değil, kuyruk zararını azaltır (Harvey ve diğ. 2018; r2) |
| Kapanış/tatil boşluğu yönetimi | — | **Var** | Cuma→Pazartesi riski hafta içi gecenin ≈ 1,5 katı (std) |
| Akış takvimi (BCOM roll, COMEX opsiyon vadesi, ay sonu) | Pratisyenler | Var | Altına özgü hakemli kanıt yok (r2) |

**Sonuç.** Bireysel trader için "para kazandıran" şey çoğunlukla **kaybettiren davranışlardan kaçınmak**: düşük kaldıraç, düşük maliyet, carry farkındalığı, olay ve boşluk yönetimi. Bunun üstüne yavaş, oynaklıkla ölçeklenmiş bir trend bileşeni eklenebilir. Kazanan grupların çoğunun (hız, lojistik, lisans, opsiyon satışı) kaynağına erişim yok.

---

## 7. Test edilmesi gereken hipotezler (bizim veride)

1. **Trend vekili VİOP'ta:** 20/60/120/250 gün işaret ortalaması ve %10 oynaklık hedefiyle, VİOP uzlaşma serisinde 1/3/5 günlük kademeli tutuş. IS 2017–2021, OOS 2022–2026. 5 ve 10 bps maliyet, drift çıkarılmış Sharpe. Beklenti: OOS Sharpe 0,2–0,5, 2026'da ≈ 0.
2. **COT managed money Δ** (Salı, Cuma yayın) sonraki 1/3/5 VİOP gününü öngörmez (beklenen IC ≈ 0). Yalnız aşırı uçlarda (z > 2) zayıf karşıt etki olabilir.
3. **GVZ − son 21 gün RV** (oynaklık primi) ve GVZ seviyesi, VİOP'ta sonraki 5 günün |getiri|'sini öngörür (oynaklık tahmini). Yönü öngörmez.
4. **EFP vekili** (GC=F − spot − olağan taban) sıçradığında, sonraki 1–5 günde VİOP ile spot arasındaki fark veya VİOP getirisi değişir mi?
5. **VİOP ons ek carry'si** (takvim yayılımı − ABD 3 aylık bono) yükseldiğinde (yurt içi long talebi), sonraki 5–20 günde VİOP getirisi düşük mü? r4'ün ilk testi anlamsızdı (OOS t = −1,44).
6. **Akşam seansı ters dönüşü:** Akşam seansı (16:00–20:00 UTC) hareketi büyükse (|r| > 1σ), ertesi günün uzlaşma getirisi kısmen tersine döner mi? İnce likidite ve 2 kat spread hipotezi.
7. **Pazartesi / tatil dönüşü:** VİOP Pazartesi ve tatil sonrası günlerinin getiri varyansı diğer günlerden yüksek mi? Cuma pozisyonunu yarıya indirme kuralı Sharpe'ı korurken maksimum düşüşü azaltır mı?
8. **ABD 13:30 UTC veri günleri:** Uzlaşma getirisinin mutlak büyüklüğü artar. "Veriden önce pozisyon almak" ile "uzlaşmada girmek" arasında yön kenarı farkı yoktur.

---

## 8. Bulunamayanlar ve açılamayan kaynaklar

- SG Trend Index ve SG CTA Index'in yıllık getirileri ve altın katkısı (403).
- Lease oranı serileri, 2020 ve 2025 EFP'nin gün içi zirvesi, Bank of England kasa kuyruğu (birincil kaynak açılamadı).
- Dubai iskontosu.
- Altına özgü perakende CFD zarar oranı. Türk aracı kurumlarında hesap sayısı ağırlıklı kâr/zarar ve zarar büyüklüğü.
- Prop firmalarında geçme ve ödeme oranları. CFTC MyForexFunds duyurusu (403).
- Chague ve diğ. Brezilya günlük trader makalesi (SSRN 403).
- Kuyumcuların VİOP hedge kullanımına dair birincil veri.
- VİOP piyasa yapıcılarının hakları ve teşvik ayrıntısı (Prosedür eki okunmadı).
- Gerçekleşen VİOP spread'i.
- Barclays/LBMA fiksing cezası (FCA sayfası 404).
- SPK Tebliğ md. 27'nin güncel kaldıraç oranları (mevzuat.gov.tr 404).
- NFP saati tick spread'i (Dukascopy 429).

## 9. Kaynaklar

**Birincil (kurum / düzenleyici):**
- ESMA, 27.03.2018: https://www.esma.europa.eu/press-news/esma-news/esma-agrees-prohibit-binary-options-and-restrict-cfds-protect-retail-investors
- FCA CP16/40 duyurusu, 06.12.2016: https://www.fca.org.uk/news/press-releases/fca-proposes-stricter-rules-contract-difference-products
- FCA PS19/18, Temmuz 2019: https://www.fca.org.uk/publication/policy/ps19-18.pdf
- SPK basın duyurusu, 10.02.2017: https://spk.gov.tr/duyurular/basin-duyurulari/2017/yatirim-hizmetleri-ve-faaliyetleri-ile-yan-hizmetlere-iliskin-esaslar-hakkinda-tebligde-iii-37-1-degisiklik-yapilmasina-dair-teblig-hakkinda
- SPK Rehber (i-SPK.37.8, 10.03.2026): yerel kopya `$S/dl_spk/rehber.txt`
- TSPB kaldıraçlı işlem bildirimleri: https://tspb.org.tr/kaldiracli-islem-bildirimleri/ ; https://tspb.org.tr/wp-content/uploads/2026/11/1_TSPB-Kar-Zarar-2026-3.xlsx
- GCM "Zarar Olasılığınız": https://www.gcmyatirim.com.tr/sirket-profili/yasal-bildirimler/zarar-olasiliginiz
- Ahlatcı "Zarar Olasılığınız": https://www.ahlatciyatirim.com.tr/hakkimizda/zarar-olasiliginiz
- IG UK: https://www.ig.com/uk
- CFTC, Haynes ve Roberts (26.03.2019): https://www.cftc.gov/sites/default/files/2019-04/ATS_2yr_Update_Final_2018_ada.pdf
- CFTC, JPMorgan (29.09.2020): https://www.cftc.gov/PressRoom/PressReleases/8260-20
- CFTC COT disaggregated geçmiş dosyaları (`fut_disagg_txt_YYYY.zip`): https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm
- BIST piyasa yapıcılık: https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/piyasa-yapicilik
- BIST borsa payı: https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/borsa-payi
- BIST üye bazında aylık hacim (Ekim 2026): https://www.borsaistanbul.com/data/vadeli/viopaylikishac202610.zip ; yerli/yabancı: https://www.borsaistanbul.com/data/vadeli/viopyyishac202610.zip ; dizin: https://www.borsaistanbul.com/files/datafilepaths_viop.zip
- BIST günlük bülten 06.11.2026: https://www.borsaistanbul.com/data/vadeli/viop_20261106.csv
- BIST duyuru 30572: https://borsaistanbul.com/files/duyuru-30572-TR.pdf ; VİOP Prosedürü: https://borsaistanbul.com/files/borsa-istanbul-as-vadeli-islem-ve-opsiyon-piyasasi-proseduru.pdf
- WGC piyasa yorumları: https://www.gold.org/goldhub/research/gold-market-commentary-january-2025 ; https://www.gold.org/goldhub/research/gold-market-commentary-february-2025
- FTMO: https://ftmo.com/en/
- Dukascopy tick verisi (örnek yol, ay 0 tabanlı): https://datafeed.dukascopy.com/datafeed/XAUUSD/2026/10/05/15h_ticks.bi5

**Akademik:**
- Heimer ve Simsek (2019): https://econpapers.repec.org/RePEc:eee:jfinec:v:132:y:2019:i:3:p:1-21
- Barber, Lee, Liu ve Odean (2014): https://econpapers.repec.org/RePEc:eee:finmar:v:18:y:2014:i:c:p:1-24
- Baron, Brogaard, Hagströmer ve Kirilenko (2019): https://econpapers.repec.org/RePEc:cup:jfinqa:v:54:y:2019:i:03:p:993-1024_00
- Moskowitz, Ooi ve Pedersen (2012): https://econpapers.repec.org/RePEc:eee:jfinec:v:104:y:2012:i:2:p:228-250
- Koijen, Moskowitz, Pedersen ve Vrugt (2018): https://econpapers.repec.org/RePEc:eee:jfinec:v:127:y:2018:i:2:p:197-225
- Prokopczuk, Symeonidis ve Wese Simen (2017): https://econpapers.repec.org/RePEc:eee:jbfina:v:81:y:2017:i:c:p:136-149
- Elder, Miao ve Ramchander (2012): https://econpapers.repec.org/RePEc:eee:jbfina:v:36:y:2012:i:1:p:51-65
- Caminschi ve Heaney (2014): https://econpapers.repec.org/RePEc:wly:jfutmk:v:34:y:2014:i:11:p:1003-1039
- Hauptfleisch, Putniņš ve Lucey (2016): https://econpapers.repec.org/RePEc:wly:jfutmk:v:36:y:2016:i:6:p:564-586
- Meader, LBMA Alchemist 83: https://www.lbma.org.uk/alchemist/issue-83/links-between-the-chinese-and-international-gold-prices

**Önceki ajan raporları:** `$S/research/r1_viop_kontrat.md`, `r2_kisa_vade_strateji.md`, `r3_kuresel_tahmin.md`, `r4_turkiye_altin.md`.

**Kendi hesaplarım:** `$S/out/r6_kim_kazaniyor/` (`r6_calc.py` + `r6_calc_out.txt`, `cot_small.py` + `cot_small_out.txt` + `cot_gold_groups.csv`, `tspb_parse.py` + `tspb_kar_zarar.csv`, `ticks_spread.py` + `ticks_spread_out.txt`, `efp_proxy_daily_2024_2026.csv`, `trend_vekili_yillik.csv`).
