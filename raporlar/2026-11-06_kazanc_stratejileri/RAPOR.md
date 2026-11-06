# Borsa İstanbul ve ABD'de kazananlar nasıl kazanıyor, sen nasıl kazanırsın? (06.11.2026)

_Veri 05–06.11.2026'ya kadar · yatırım tavsiyesi değildir · kaldıraçlı ürünlerde sermayenin tamamı kaybedilebilir_

İki soruya cevap: (1) Borsa İstanbul ve VİOP'ta para kazananlar nasıl kazanıyor, sen nasıl kazanırsın? (2) ABD borsalarında aynı soru. Ufuk: swing (birkaç gün ile birkaç ay arası), gün içi yok, al-unut yok. Ölçüt: TL'de risksiz getirinin, dolarda T-bill'in ve TL'de kalmanın fırsat maliyetinin üstü.

Yöntem: 7 araştırma iş akışı, ~25 ajan. Her iş akışının sonunda ayrı bir doğrulayıcı ajan iddiaları birincil kaynaktan ya da ham veriden yeniden hesapladı. Kendi backtest'lerimiz: BIST'te 485 hisse ve 49 endeks (2010–2026), ABD'de Ken French, Chen-Zimmermann, FRED ve AQR verileri. Olay çalışmaları: bedelsiz, halka arz, geri alım, içeriden alım, yabancı akışı, faiz döngüsü. Doğrulama raporları ana raporların üstündedir; burada yalnız doğrulamadan geçen ya da düzeltilmiş rakamlar var. Uygulama planları ayrı dosyalarda: `uygulama/PLAN_BIST.md`, `uygulama/PLAN_ABD.md`.

---

## 0. Önce bir düzeltme: aşman gereken çıta

**"Reel faiz %40–50" doğru değil.** Politika faizi %36 (22.10.2026), Ekim TÜFE yıllık %29,77. Reel faiz geçmiş enflasyona göre ~%4,8, beklentiye göre ~%5–8. %40–50 olan nominal faiz; 2024'te PPF'nin brüt bileşik getirisi %53–61'di, algı oradan geliyor.

| Araç | Bireyde vergi | Çıta (12 ay, net) |
|---|---|---|
| Mevduat, para piyasası fonu (PPF) | %17,5 stopaj | Faiz %36'da kalırsa ~%35–38; anketteki yolda (12 ayda ~%29) ~%31–33. Son 12 ayın PPF medyanı brüt %45,5 → net ~%37,5 |
| BIST'te pay alım-satımı, pay/endeks VİOP | %0 stopaj | Vergi avantajı çıtayı fiilen ~5–7 puan düşürür |
| VİOP USDTRY ve diğer pay dışı sözleşmeler | %10 stopaj | |
| ABD hisse/opsiyon kazancı | TL bazında (kur farkı dahil) beyan, %15–40 artan oran; zarar yalnız aynı yıl mahsup | TL'de kalmayı geçmek için vergi öncesi **~%20–28 USD/yıl** |

- **"Risksiz" de risksiz değil.** Tasfiyedeki 15 PPF'den 4'ü %95–99,9 kaybetti. Çıtayı banka PPF'si, TLREF ya da DİBS ile ölç.
- **TL'de kalmanın dolar karşılığı.** İleriye dönük net ~%13–15. Ama bu bir carry işlemi: 2010–2026'da USD bazında yılda −%7,2, en büyük düşüş −%85. Short F_USDTRY Temmuz 2023'ten beri yılda +%20,8 USD getirdi, 2018–2026 toplamı ise yalnız +%4,3 (2021'de −%30).
- **Profesyoneller de bu çıtayı aşamadı.** Son 3 yılda 91 hisse yoğun fondan yalnız 1'i PPF medyanını geçti ve o da şimdi tasfiyede. Üç alt dönemin üçünde de PPF'yi yenen yönetici yok. Bunun büyük kısmı beceri eksikliği değil: hisse betası yüksek reel faize yenildi.

Sonuç: BIST'te bir stratejinin işe yaraması için yılda ~%31–36 net TL'nin üstüne çıkması gerekiyor. Son üç yılda bunu tutarlı yapan kimse yok. ABD'de dolar bazında vergi öncesi %20–28.

---

## 1. Borsa İstanbul'da kazananlar nasıl kazanıyor?

### 1.1 Kim kaybediyor (taban oran)

- **Bireyler.** MKK hesap verisiyle 20.000 bireysel yatırımcı (2011–12) endeksin haftada %0,281 gerisinde kaldı, yılda ~14,6 puan. En çok işlem yapanlar haftada −%0,538, yılda ~28 puan geride. Yatırımcıların ~%70'i endeksi yenemedi. (Erdem vd. 2014; CAPM alfası anlamlı değil, yön net.)
- **Kaldıraçlı FX müşterileri.** 41 çeyrekte zararda hesap oranının ortalaması %67, 2026/06'da %74,4 (TSPB verisinden yeniden hesaplandı).
- **Kredili işlem yapanlar.** Aracı kurumların 2025 müşteri faiz geliri 53,1 mlr TL, komisyon gelirleri (32,3 mlr TL) toplamından büyük. Örtük kredi maliyeti ~%60.
- **Halka arzda seri bittikten sonra alanlar.** 53 arzın ~50'si seri sonundan sonra düştü, medyan −%55. 2026 arzlarının 36'sından 27'si arz fiyatının altında.

### 1.2 Kim kazanıyor ve nasıl: dört katman

| Katman | Kim | Mekanizma | Getiri büyüklüğü | Senin için |
|---|---|---|---|---|
| **a) Yapıyı işletenler** | Aracı kurumlar, DMA/algo masaları, piyasa yapıcılar | Kredi faizi, komisyon, spread, hız. DMA pay hacminin %28'i, vadelinin %33'ü; DMA pay işlemlerinin %93'ü iki kurumda. Vadeli hacimde yabancı kurum payı %47. | Kurum ölçeğinde sürekli | Kopyalanamaz. Tek ders: bu gişeye ödediğin bedeli (kredi faizi, piyasa emri, sık işlem) küçült. |
| **a′) Manipülasyon ve fon döngüsü** | 2026 krizindeki fonlar ve grupları | Serbest dolaşımı düşük hisselerde dolaşımın üstünde pay toplamak, alarak fiyatı yükseltmek, grup kâğıtlarıyla değerleme. Tera Yatırım 2025'te aracı kurum sektör kârının %35'ini yaptı. TLY fonu 3 yılda +%71.787 getiri gösterdi, oynaklık %21, en derin düşüş −%4,2. Grup hisseleri 16.09'dan beri −%95/−%98. | Kâğıt üstünde sınırsız, sonra sıfır | Yasa dışı ve sonu belli. Ayrıca kendi backtest'imizde kırılım stratejisinin en büyük kârları bu hisselerden geldi (KTLEV, ODINE, HEDEF, PEKGY). Bu hisselerden uzak durmak bir kural olmalı. |
| **b) Faiz/carry** | Mevduat ve PPF sahipleri, TL carry yapanlar | Pozitif reel faiz | Net ~%31–38 TL. Son 3 yılda hisseyi ezdi. | Çekirdek. Ama bu "kazanmak" değil, çıtanın kendisi. |
| **c) Rejim kırılmasında yoğun makro bahis** | Yabancı kurumlar, iyi makrocular | Rejim dönerken ilgili kümeye yoğunlaşmak, kaldıraçla. | Bkz. tablo 1.3 | **Büyük para burada.** VİOP ile uygulanabilir. İsabet düşük, sonradan seçme yanlılığı yüksek. |
| **d) Davranış/akış kenarları** | Disiplinli bireyler, kurumsal masalar | Kırılım ve 52 haftalık zirve, olay öncesi akış (temettü, bedelsiz), çiftler, zorunlu satıcılar | İşlem başına 1–5%, çoğu çıtanın çevresinde | Uydu katman. Senin önceki 15–70 bps'lik kenarların burada ama en küçük ucunda. |

### 1.3 BIST'te büyük para nereden çıktı (2018–2026, dolar bazında, VİOP vadelilerinden hesaplandı)

| Dönem | İşlem | Getiri | Önceden görülebilen sinyal |
|---|---|---|---|
| Ağu 2018 – Oca 2019 | Long bankalar (GARAN) | +%91 | Kur krizinden sonra sert faiz artışı, reel faiz pozitife döndü |
| Ekim 2020 – Şub 2021 | Long bankalar | +%52 | Ekonomi yönetimi değişikliği, faiz artışı |
| 2022 | Long XU030 / bankalar (derin negatif reel faiz) | XU030 +%110, YKBNK +%149 | Reel faiz −%50'ye yakın, hisse enflasyon kalkanı |
| Ara 2017 – Ağu 2018, Ağu – Ara 2021 | Long USD (ortodoks olmayan şok) | +%74, +%121 | Faiz indirimi ve kur baskısı birlikte |
| May – Ağu 2023, Ara 2023 – Haz 2024 | Long bankalar | +%45, +%73 | Seçim sonrası ortodoks dönüş, faiz artışlarının sonu |
| Tem 2023 – Eki 2026 | TL carry (short F_USDTRY) | Yılda +%20,8 USD | Pozitif reel faiz, yönetilen kur |
| 08/2025 – 02/2026 | Koza/altın kümesi | XU100'e göre +%88–100 | Altın rekorları |
| 05/2023 – 02/2024, 02 – 06/2025 | Savunma kümesi | Göreli +%100, +%45 | Savunma bütçesi, halka arzlar |
| 06 – 10/2026 | Rafineri | Göreli +%56 (XU100 −%27) | Petrol 100 $ üstü |

Ortak nokta: getiri **küme** düzeyinde, **rejim** dönüşünde ve **yoğunlaşmayla** geldi. Ortodoks dönemde 6 aylık pencerelerin yalnız %26'sında XU030 dolar bazında carry'yi geçti. Yani koşulsuz "BIST al" çıtayı geçmiyor. Kazanan, ne zaman long olacağını bilen.

### 1.4 Swing ufkunda ne işe yarıyor, ne yaramıyor (kendi testlerimiz, doğrulamadan sonra)

**İşe yarayanlar (ama çoğu son 3 yılda çıtanın altında):**

| Yaklaşım | Sonuç | Çekince |
|---|---|---|
| **52 haftalık zirve kırılımı + trend şablonu + %15 iz süren stop** | İşlem başına aynı gün rastgele likit hisseye göre +%5,3 (t 5,1, 2.073 işlem, 17 yılın 15'i pozitif). İsabet %45, ortalama kazanç ortalama kaybın 3,3 katı. 10 slotlu portföyde medyan yılda %34,8 TL. | En iyi %5 işlem kârın ~%70'i, çoğu sonradan çöken pump hisseleri. Düzeltilmiş risksiz faizle 2024–26'da çıtanın 2–8 puan altında. Tavan/taban dolum varsayımıyla en büyük düşüş −%45/−%61. |
| **Sektör endeksi rotasyonu** (15 büyük sektör, her ay en güçlü 2–3) | Yılda ~%29,6 TL, uzun dönemde risksizin +11 puan üstü, MaxDD −%34. Hayatta kalan yanlılığı yok. | 2024, 2025, 2026'nın her birinde risksizin altında. Sektör endeksi doğrudan alınamıyor, sepetle kopyalanıyor. |
| **Küme rotasyonu** (12 aylık göreli güce göre ilk 3 küme) | Yanlılık düzeltilince eşit ağırlıklı kümelerin yılda ~+5 puan üstü, MaxDD −%40/−%48 | Bu rejimde çıtayı geçmiyor; getiri motoru değil, **küme seçme filtresi**. |
| **52 haftalık zirveye yakınlık sıralaması** | t 2,2–3,7 | 2022 çıkarılınca zayıf (t 0,85–1,5) |
| **Temettü hak kullanımından önceki 5 gün** (spot) | +%1,2 (t 6,5–7,8, n=1.109) | VİOP temettüyü fiyatlıyor; yalnız spotta |
| **Yüksek verimli nakit temettü (duyuruda verim ≥%5)** | Duyurunun ertesi kapanışında al, hak kullanımından önceki gün kapanışta sat. Aynı evrenin eşit ağırlıklı toplam getirisine göre +%6,5 (medyan +%4,1, t 6,5, ~27 işlem günü). 12 yılın 12'si pozitif, 2024–26'da +%13,5. Likit hisselerde de var. | Bu çalışmanın en güçlü yeni kenarı, bağımsız veriyle yeniden üretildi. Girişlerin %81'i Şubat–Mart'ta, yılda 14–25 olay. Hedgelenirse getiri ≈ TL faizi + %6–7. |
| **Bedelsiz** (601 olay) | Hak gününden sonraki 10 günde −%3,3 (t −5,5). Bu yüzden hak gününden önce satmak geçerli bir çıkış kuralı. | Alım tarafı **işe yaramıyor**: duyuru etkisi tavan kilitli günlerde, "onayda al, bölünmeye sat" net −%0,07, duyuruda alıp 5 gün tutmak −%1,6. |
| **Halka arz katılımı** | Gün içinde tavan ilk bozulduğunda satan katılımcı medyan +%33 | Hesap başına yılda 8–22 bin TL, ölçeklenmiyor. Seri bitince almak zarar: 21 günde medyan −%11, 2024–26'da −%17. |
| **Çiftler: SAHOL↔AKBNK, KCHOL↔iştirak sepeti** (\|z\|≥2) | Gerçekçi 1 gün gecikmeyle işlem başına +128–310 bps, t 2,1–2,8 | Önceki çalışmadaki SAHOL/AKBNK kenarının daha geniş bantlı hali. Kurumsal olay riski. |
| **12 aylık zaman serisi momentumu (XU100)** | 2019–26'da long/nakit yılda %48 (nakit %25) | Zayıf istatistik. Şu an kapalı: XU100 12 ayda +%3,3, nakit +%37. |

**İşe yaramayanlar:**
- Klasik 12-1 kesitsel momentum: risksizin altında.
- Kısa vadeli reversal: yılda −%17,9. Haftanın kaybedenleri kaybetmeye devam ediyor.
- Endekste SMA200 ve 50/200 kuralları.
- Bedelsizde alım tarafı, halka arzda seri bittikten sonra almak.
- Geri alım ve içeriden alım: eşleştirilmiş kontrollerle kalıcı bir kenar yok.
- Yabancı akımı: fiyatı izliyor, öngörmüyor.
- AKD/takas takibi: bilgili işlem ölçüleri getiri öngörmüyor.
- Ramazan etkisi, A/B pay oranları.

**Faiz döngüsü ve bankalar:** Faiz indiriminden sonraki 63 günde bankalar XU100'ün gerisinde kaldı; 6 döngünün 6'sında, ortalama −%6,3 (t −4,2). İndirimden önceki 63 günde ise +%3,2 önde. Bankalar son 63 günde +%26 koştu ve 10.12 PPK'da anket indirim bekliyor. Bağımsız gözlem yalnız 6 döngü; bu bir işlem kuralı değil, boyut eğilimi.

### 1.5 Kazananların BIST'teki gerçek formülü

1. **Çekirdek çıtada dursun.** Paranın çoğu net ~%31–38 TL'de. En verimli araç vergiye göre seçilir: banka PPF'si, mevduat, DİBS ya da XU030 nakit-taşıma (spot long + vadeli short; iki bacak da %0 stopaj, ima edilen faiz ~%29).
2. **Risk sermayesi rejim döndüğünde kümeye yoğunlaşsın.** Tetikler: rezerv artışı, aylık TÜFE %2'nin altına inmesi, yabancı alımı, CDS 230'un altı, faiz indirim döngüsü. O zaman bankalar ve VİOP üzerinden kaldıraç.
3. **Rejim kapalıyken uydular.** Çiftler, temettü öncesi spot, zorunlu satıcı olayları. Kırılımları da yalnız likit, VİOP'u olan ve fon tasfiyesi baskısı taşımayan hisselerde, küçük boyutla dene.
4. **Pump ve tasfiye baskısındaki hisselerden uzak dur.** Fon payı/serbest dolaşım oranı %20'nin üstünde olanlar ve SPK suç duyurusu yapılan 13 hisse. Liste uygulama planında.

Bu dört madde, önceki çalışmalarındaki "çok sayıda küçük istatistiksel kenar" yaklaşımından farklı: getiriyi az sayıda büyük, pozitif çarpık bahis üretiyor, geri kalan zaman sermaye çıtada bekliyor.

---

## 2. Sen Borsa İstanbul'da nasıl kazanırsın? (9 Kasım için)

Ayrıntılı kurallar `uygulama/PLAN_BIST.md` dosyasında, akşam rutini `uygulama/BIST_GUNLUK_RUTIN.md`'de, günlük sayılar `uygulama/kod/bist_sinyal.py` çıktısında. Plan şöyle hazırlandı:
1. Üç bağımsız taslak yazıldı: trend/lider, rejim ve carry, önce risk.
2. Üç hakem puanladı; "önce risk" taslağı iskelet seçildi.
3. Öteki iki taslağın iyi fikirleri eklendi ve plan iki çürütme incelemesinden geçti.

**Rejim anahtarı (her kapanıştan sonra hesaplanır, ertesi gün geçerli):**

| Durum | Tanım | Ne açılır |
|---|---|---|
| AÇIK | XU100 kapanışı 200 günlük ortalamanın (bugün 13.572) üstünde | Kırılım motoru tam boy (işlem başı risk %0,75), endeks/küme beta kolu (12 aylık momentum da açıksa) |
| GEÇİŞ | XU100 5 kapanış üst üste 50 günlüğün (12.691) üstünde **ve** net rezerv 3 hafta üst üste artıyor **ve** şu üçünden biri: 2 ay üst üste aylık TÜFE <%2, CDS <230 ve düşüyor, XBANK 200 günlüğünün üstünde | Kırılım yarım boy (risk %0,5) |
| KAPALI | Diğer her durum. **Bugün: 7 göstergenin 0'ı açık.** | Kırılımda en çok 2 küçük deneme (%0,25 risk). Rejimden bağımsız kollar açık. |
| KRİZ kesicisi | 5 günde XU100 ≤−%8, kur ivmesi, CDS >300, net rezerv 2 hafta üst üste ≤−5 mlr $, F_USDTRY ima faizi politika faizi +5 puanın üstünde ya da MSCI sınıflandırma danışması | 5 gün yeni giriş yok, açık pozisyonların stopu sıkılaşır |

GEÇİŞ için en erken gerçekçi tarih 26.11 kapanışı. 12.11'deki rezerv verisi bir hafta daha −5 mlr $ ya da daha kötüsünü gösterirse KRİZ kesicisi tetiklenir.

**Kollar:**

| Kol | Kural (özet) | Durum |
|---|---|---|
| Çekirdek | Pazartesi hesabın %15'i bankada 32 günlük mevduata, %85'i banka iştiraki PPF'ye. Hedef %60 mevduat / %40 PPF; dilimler 9, 16, 23 ve 30.11'de. | **Pazartesi yapılacak tek finansal işlem** |
| K1 SAHOL↔AKBNK | 20 günlük oran z-skoru \|z\|≥2 olunca VİOP'ta ters spread, ertesi kapanışta giriş | Rejimden bağımsız. Şart: teminat faiz kazanmalı, komisyon bacak başına ≤5 bps. |
| K3 Temettü öncesi 5 gün | Spotta hak kullanımından 6 gün önce al, bir önceki gün kapanışta sat; temettü alınmaz | Rejimden bağımsız; küçük kenar (+%0,2–0,5) |
| K3b Yüksek verimli temettü | Duyuruda verimi ≥%5 olanı duyurunun ertesi kapanışında al, hak kullanımından önceki gün sat, XU030 vadelisiyle hedgele | En güçlü yeni kenar: denetimden sonra +%6–7 fazla getiri, ~27 işlem günü. Sezonu Şubat–Mayıs; 01.02.2027'den yarım boylu pilot. |
| K4 Kırılım motoru | 52 haftalık kapanış zirvesi + trend şablonu + %15 iz süren stop; giriş kapanış seansında | Boyut rejime bağlı. En yakın tetikler: ENJSA 127,00; AHGAZ 48,70 / ENERY 14,60 (tek isim sayılır); RYSAS 30,28. |
| K5 Özel durumlar | Zorunlu pay alım teklifi, satma ve ayrılma hakları | Yalnız KAP teyidiyle. AKCNS teklifi kapanmış, listeden çıktı. |
| K6 TL carry | Short F_USDTRY, %10 stopaj | Kapalı; brüt rezerv kapısı 160 mlr $ (şu an 158,1) |
| K7 Endeks/küme beta | 12 aylık momentum açıkken | Kapalı |
| K8 Halka arz katılımı | Tavan gün içinde ilk bozulduğunda sat; seri bitince alma | İsteğe bağlı. Hesap başına yılda 8–22 bin TL, ölçeklenmiyor. |
| K9 Serbest kol | Plan dışı her fikir yalnız buradan, %0,25 risk | Birikimli −%1,5'te 6 ay kapanır |

**Kaçınma takvimi:**
- 11–13.11 kapanışlarında K3, K4, K5 ve K9'da yeni giriş yok.
- Kredili işlem esnekliği 13.11'de uzatılmazsa:
  - kırılım girişleri 23.11'e kadar yok;
  - VİOP-47 dışında long 30.11'e kadar yok.
- MSCI'ın çıkardığı ya da ağırlığını düşürdüğü hisseler, değişiklik yürürlüğe girene kadar alınmaz.
- 10.12 PPK sürprizsiz bir indirimse, ~15.03.2027'ye kadar bankalarda yarım boy. Gerekçe: indirimden sonraki 63 günde bankalar 6 döngünün 6'sında XU100'ün gerisinde kaldı.
- Dışlama listesindeki hisseler (fon tasfiyesi baskısı, SPK suç duyurusu) hiçbir kolda alınmaz.

**Dürüst beklenti (12 ay, vergi sonrası, çıtaya göre):**
- Merkez **+1…+2 puan**; %80 aralık −2…+5,5. Toplam net nominal getiri ~%33–37.
- Rejim 1–3 ayda dönerse kırılım ve endeks kollarından +3…+8 puan, kârın çoğu birkaç işlemden.
- Bu rejimde +10–20 puan hedeflemek bu planın 3–5 katı açık risk ve çıtaya göre −%25…−%40 düşüş toleransı ister. Kanıt bunu desteklemiyor.
- Yüksek getiri, rejim döndüğü anda hazır olmaktan gelir. Plan bunun için var.

---

## 3. ABD borsalarında kazananlar nasıl kazanıyor?

### 3.1 Yapıyı işletenler

- **Market maker'lar (2025):**
  - Jane Street ~39,6 mlr $ net işlem geliri (basın).
  - Virtu 2,44 mlr $ (+%33,7, 10-K).
  - Citadel Securities ~12,2 mlr $ (doğrulanamadı).
  - Bireyin tercih ettiği opsiyonlarda ortalama spread %12,6.
- **Pod fonları (2025):**
  - Getiriler: Point72 %17,5, Balyasny %16,7, Millennium %10,5, Citadel Wellington %10,2. Çoğu S&P 500'ün (+%16,4) altında.
  - Ürettikleri şey yüksek getiri değil, yüksek Sharpe. Arkasında 12x brüt kaldıraç ve pod başına %5–10'da mekanik risk kesme var.
- **Medallion ve RIEF.** 2020'de Medallion +%76, aynı firmanın dışarıya açık fonu RIEF −%22,6. Kısa ufuklu sinyaller kapasiteyle ölüyor. Senin BIST mikro kenarların bu türden.
- **CTA/trend fonları.** SG Trend 2022'de +%27,3, sonra en kötü 12 ayını yaşadı (−%18'in üstünde). 2000'den beri yıllık %5,2.

### 3.2 Bireyler: taban oran ve sağ kuyruk

- **Medyan birey kaybediyor:**
  - Tayvan: day trader'ların %13'ü kârlı, kalıcı kazananlar %1'in altında.
  - Brezilya: 300 seanstan fazla devam edenlerin %97'si zararda.
  - 0DTE opsiyonda bireyler günde ~358 bin $ kaybediyor.
  - Hindistan (SEBI FY26): %87,7 zararda.
- **Beceri gerçek ama küçük ve ölçeklenmiyor.** Tayvan'da önceki yılın en iyi 500'ü ertesi yıl günde 28 bps kazanıyor, ama toplam portföy alfası yılda ~%5.
- **Doğrulanmış sağ kuyruk:** ABD Yatırım Şampiyonası (USIC), aracı kurum ekstreleriyle:
  - Martin Luk 2024 +%283, 2025 +%970, 2026'nın 9 ayında +%786.
  - J Law 1 mn $ üstü hesapta 2024 +%354, 2025 +%252.
  - Minervini 2021 +%335. Oliver Kell 2020 +%941. Sean Ryan 7 yılın 7'si kârlı, yılda ~%81.
- **Ama payda kötü.** Kârda biten katılımcı oranı 2022'de %8, 2026'da %12–17. Zirveden yıl sonuna geri vermeler büyük: Luk −%27, bir başkası −%52. Kullamägi 105 mn $'dan ~45 mn $'a indi (−%57, kendi beyanı).
  - Sıfır kenarlı 700 kişilik bir yarışmada, %100 volatiliteyle bile kazananın medyan getirisi +%1.239 çıkar. Tek yıllık şampiyonluk beceri kanıtı değil; üç yıllık kalıcılık (Luk) daha anlamlı.
- **Mekanik kopyası çalışmıyor.** IBD 50 ETF'i (FFTY) 10 yılda yılda %4,6 getirdi, 2022'de −%51.

### 3.3 Kazananların ortak yöntemi

- İşlem başına risk sermayenin %0,25–1'i. Stop yapısal ve dar: 1 ATR ya da %7–10.
- İsabet %22–45, ortalama kazanç ortalama kaybın 2–5 katı. İşlem başına beklenti +0,4–0,6R.
- Giriş: göreli gücü en yüksek tema liderlerinde taban kırılımı, kazanç sonrası boşluk, yükselen 10/20 günlük ortalamaya ilk geri çekilme.
- Kâr alma: 3–5 günde 1/3–1/2 satış, kalan kısım 10/20 günlük ortalamayla taşınıyor.
- Yalnız kazanana ekleme. Kazanırken pozisyon büyüyor, kaybederken küçülüyor.
- **Katı piyasa rejimi anahtarı.** Kullamägi kendi filtresine uysaydı 2022 kaybının ~%90'ından kaçacağını söylüyor.
- 4–8 pozisyon, tema yoğunlaşması.

Akademik destek bileşenlerde var: haber destekli fiyat şokları sürüyor, 52 haftalık zirveye yakınlık ve sektör momentumu getiri öngörüyor. Bessembinder'e göre hisselerin %4'ü bütün net servet yaratımını açıklıyor. Tekil hisse trend takibinin akademik testi yılda ~%15 brüt; işlemlerin %7'sinden azı kârın çoğunu üretiyor.

### 3.4 Kamuya açık anomaliler büyük ölçüde bitti (kendi hesaplarımız)

| Kenar | 2010 sonrası |
|---|---|
| 212 yayımlanmış anomali (Chen-Zimmermann) | Medyan uzun-kısa getiri yayın öncesi %0,60/ay → yayın sonrası %0,24 → 2010–25 likit evrende %0,13. Anlamlı kalan pay %16. |
| 12-1 hisse momentumu (UMD) | Yılda %2,6–4, Sharpe 0,26 |
| PEAD | Büyük hisselerde 2006'dan, mikrocap'lerde 2016'dan beri yok |
| Kısa vadeli reversal | ~%0 (yalnız VIX>25 aylarında pozitif) |
| Pre-FOMC, S&P 500'e ekleme, spin-off, ay dönümü | Bitti ya da çok küçüldü |
| Sektör momentumu | Uzun dönemde gerçek. 2010 sonrası risk ayarlı olarak piyasa düzeyinde, 2015 sonrası belirsiz. |
| Opsiyon almak | Koşulsuz zarar: straddle haftada ~−%3, piyango call'ları haftada −%35 |
| Hayatta kalan tek güçlü sinyal grubu | Opsiyon fiyatlarından çıkan sinyaller (skew; t 5–6), analist revizyonu, ardışık kazanç sürprizi. Hisse seçme filtresi olarak değerli, tek başına getiri motoru değil. |

**%15–25 USD bandı yalnız kaldıraçlı betayla görülüyor.** 2x/3x Nasdaq-100 + 200 günlük ortalama filtresi 2010–26'da yılda %18–26 getirdi. Bedeli: en büyük düşüş −%55 ile −%97 arası; 2000–02'de 3x versiyon −%89. Filtre 2010–26'da getiriyi artırmadı, yalnız düşüşü kesti. Bu alfa değil, kaldıraçlı hisse primi.

---

## 4. Sen ABD borsalarında nasıl kazanırsın? (9 Kasım için)

Ayrıntılı kurallar `uygulama/PLAN_ABD.md` dosyasında, akşam rutini `uygulama/ABD_GUNLUK_RUTIN.md`'de, rejim ve trend şablonu göstergesi `uygulama/kod/abd_rejim_ve_sablon.pine` dosyasında (TradingView'da derlenmedi). Plan BIST planıyla aynı süreçten geçti: üç bağımsız taslak, üç hakem, iki çürütme incelemesi. İskelet "önce risk" taslağından, işlem mekaniği "lider momentumu" taslağından alındı. Kaldıraçlı endeks çekirdeği reddedildi: fiilen kaldıraçlı al-tut, ve 2010 sonrasında filtre getiriyi de kesti.

**Yöntem: doğrulanmış şampiyonların yöntemi, gün içi ekransız.**
- Tek canlı kol: rejim filtreli lider swing. İki kurulum var:
  - **S1 baz kırılımı:** pivot üstüne al-stop limit.
  - **S2 yükselen 10/20 günlük ortalamaya geri çekilme.**
- Girişler 16:45–17:15 TSİ arasında, bekleyen emirle: BUY STOP-LIMIT ve ekli, iyi-iptal SELL STOP.
- Çıkışlar ve stop düzeltmeleri gece 00:30–01:00 ya da sabah 08:00–09:00 arasında, kapanışa göre.
- 17:30–00:00 arasında ekrana bakılmaz.
- Kâr alma: +2R'de ya da 4. seansta ≥+1R ise 1/3–1/2 satılır, kalan 10/20 günlük ortalamayla taşınır.
- Bilanço gap'i ve VIX çözülmesi kurulumları önce yalnız kâğıt üzerinde (gölge) kaydediliyor. Opsiyon, margin, açığa satış ve kaldıraçlı ETF ilk fazda yok.

**Rejim bugün KIRMIZI:**
- Nasdaq düzeltmede.
- S&P 500 200 günlüğün ancak %0,4 üstünde.
- VIX/VIX3M 1,10.
- S&P ve Nasdaq'ta 10 günlük ortalama 20 günlüğün altında.
- Dip teyit günü (FTD) yok.

Sarıya geçmek için şartların 3 kapanış üst üste sağlanması gerekiyor. Bu yüzden **Pazartesi canlı işlem yok; ilk canlı deneme en erken 16.11**, tek pozisyonla ve AI dışı bir kümeden.

**Sermaye:**
- Para TL'deyse ABD strateji sermayesi likit servetin **%10'u** (en çok %15'i). Bunun şimdilik %40'ı USD'ye çevrilip IBKR nakit hesabına gider, kalanı TL'de mevduat ve PPF'de bekler.
- Para zaten USD'deyse servetin en çok %20'si.

**Risk (ilk 50 işlem):**
- İşlem başı risk %0,25, tek pozisyon ≤%7,5.
- Küme ısısı ≤%0,75. Toplam açık risk sarıda %1,25, yeşilde %2,5.
- Aylık devre kesici %3. Strateji sermayesinde −%8'de plan durur.
- Kritik bir kural ihlalinde (stop indirmek, zarara eklemek, rejim dışı giriş) 10 seans işlem yok; ikinci ihlalde plan durur.

**Erişim:**
- Ana platform IBKR Pro. Türkiye'den açılabiliyor, ~0,005 $/adet; gerçekçi ilk işlem 11–13.11.
- Midas yalnız ≤500 $ ile test için: stop/GTC desteği teyit edilmeli, yalnız opsiyon alımı var.
- PDT kuralı (25 bin $) kalktı.

**Vergi:** Kazanç TL bazında, kur farkı dahil, beyanla vergilenir; zarar yalnız aynı yıl içinde mahsup edilir. Her işlemi TCMB kuruyla kaydet. Aralıkta zarar realize ederek vergi düşürme ancak müşavir onayıyla.

**Dürüst beklenti:**
- İlk faz bir ispat dönemi. Medyan beklenti kenara göre −%2,5 ile +%6,5 arası; TL'de kalmayı geçme olasılığı %5'in altında.
- Yüksek getiri ancak kenar ispatlandıktan sonra gelir: 100 işlem, 12 ay ve t ≥1,65 gerekiyor. O noktada risk işlem başına %0,5–1'e çıkar. Doğrulanmış üst dilimde yılda %40+ görülüyor, medyan trader'da görülmüyor.

---

## 5. Ortak sonuç: senin için gerçekten işe yarayan yol

1. **Mikro kenarlardan büyük, az sayıda, pozitif çarpık bahse geç.** İşlem başına 15–70 bps'lik kenarlar senin elinde maliyet, gecikme ve sönümle yeniliyor. Kenarın %35–58'i yayından sonra kayboluyor; senin BIST30 kenarların tam da en hızlı sönen sınıfta. Sermayeyi büyüten şey ise az sayıda büyük kazanç. Hem BIST kırılım testinde hem ABD şampiyonlarında kârın çoğu en iyi %5–10'luk işlemlerden geliyor.
2. **Sermayenin çoğu çıtada, risk sermayesi rejim açıkken çalışsın.** BIST'te çıta net ~%31–38 TL; ABD'de TL'de kalmayı geçmek için vergi öncesi ~%20–28 USD. Rejim kapalıyken (bugün iki piyasada da) agresif olmamak bir kenardır, tembellik değil.
3. **Kümelemeyi risk birimi yap.** Bankalar+holding+havacılık BIST'te tek bahis (korelasyon 0,77–0,79). ABD'de yarı iletken ve elektrik ekipmanı tek bahis (0,72). Küme başına risk ≤%1,5, toplam açık risk rejime göre %3/%5/%6. Ay içi zarar ile açık risk toplamı %6'ya ulaşınca o ay yeni işlem yok.
4. **Zorunlu satıcıların karşısında dur, ama hemen değil.** MSCI kararları, kredili tasfiyeler, fon tasfiye takvimi, satış yasaklarının bitişi. Stres anında likidite sağlamanın primi var (reversal getirisi VIX ile artıyor). Yalnız akış bittikten sonra ve likit hisselerde.
5. **Ölç, yoksa bırak.** İşlem başına +0,2R'lik bir sistemin şanstan ayrılması ~390 işlem ister; Sharpe 1'lik bir stratejinin t=2'ye ulaşması 4 yıl sürer. Bu yüzden:
   - Kenarı R-çarpanıyla ölç.
   - İlk 30–50 işlem küçük boyutla.
   - Önceden yazılmış öldürme kriterlerine uy.
   Planlarda sayısal olarak var.

---

## 6. Ne düzeltildi, ne bilinmiyor

**Doğrulamada düzeltilenler (hepsi stratejilerin aleyhine):**
- **BIST backtest'leri.** Risksiz faiz basit faizle hesaplanmıştı. Düzeltince 2024–26 sonuçları çıtanın 2–8 puan altına indi.
- **SAHOL/AKBNK ve KCHOL çiftleri.** Sinyal kapanışında girildiği varsayılmıştı. 1 gün gecikmeyle kenar %30–45 küçüldü.
- **VİOP baz hesabı.** Tarama, BIST30 vadelisindeki ima faizi %23,3 bulmuştu. Resmi uzlaşmayla doğrusu ~%29,3.
- **ABD.** Sektör momentumunun "1 numaralı" sıralaması abartılı bulundu. S&P'nin 200 günlüğe uzaklığı eski veriydi.
- **BIST küme rotasyonu.** Kenarın yaklaşık yarısı, kümelerin bugün kazandığı bilinen hisselerle kurulmasından doğuyordu; bu sonradan seçme yanlılığı çıkarıldı.

**Sınırlar:**
- **Web araması.** Alt ajanların ortak web arama kotası (200) iş ortasında doldu. Doğrulayıcılar birincil kaynakları doğrudan indirerek çalıştı; erişemedikleri iddiaları "doğrulanamadı" diye işaretlediler.
- **Veri erişimi.** Yahoo istek sınırı koydu, Stooq bot doğrulaması istedi, TEFAS otomatik erişimi reddetti; bunların hiçbiri aşılmaya çalışılmadı. Bu yüzden ABD'de hisse düzeyinde earnings-gap/kırılım testi yapılamadı. ABD planındaki aday listesi kaynaklı web derlemesi ve senin çalıştıracağın tarama ayarları.
- **Halka arz verisinde bir istisna.** halkarz.com betikle yapılan isteklere 403 verdi. Ajan taramayı durdurdu ama detay sayfalarını sonra başka bir araçla (WebFetch) tek tek okudu. Denetçi bunu "engelin başka bir istemciyle aşılması" sayılabilir diye işaretledi.
  - Arz listesi ve fiyatlar başka kaynaklarla (İş Yatırım birincil halka arz listesi ve fiyat serileri) doğrulanıyor.
  - Katılımcı sayısı ve lot alanları ise yalnız o sayfalardan geliyor. Bu alanlar KAP'taki satış sonuçları bildirimlerinden yeniden alınmalı.
  - Ham veri repoda yok.
- **Hayatta kalan yanlılığı.** BIST hisse evreni bugün işlem gören hisselerden kurulu; bu sonuçları yukarı çarpıtıyor.
- **Öznel tahminler.** Rejim senaryolarının olasılıkları öznel.

## Dosyalar

- `ajanlar/`: 14 araştırma raporu.
  - BIST: `bist_kim_kazaniyor`, `bist_swing_kenarlar`, `bist_test`, `dalga_bist`, `olay_*`, `tr_profesyonel`.
  - ABD: `abd_kim_kazaniyor`, `abd_swing_kenarlar`, `abd_test`, `dalga_abd`, `abd_profesyonel`, `abd_pratik`.
  - Çapraz: `tr_makro_engel`, `seytan_taban_oranlar`.
- `dogrulama/`: bağımsız doğrulama ve denetim raporları. Ana raporlarla çeliştiklerinde bunlar geçerli.
- `uygulama/`:
  - Planlar: `PLAN_BIST.md`, `PLAN_ABD.md`.
  - Günlük rutinler: `BIST_GUNLUK_RUTIN.md`, `ABD_GUNLUK_RUTIN.md`.
  - Hafta hazırlıkları: `bist_hafta_hazirlik.md`, `abd_hafta_hazirlik.md`.
  - `kod/`: tarama ve sinyal betikleri, TradingView göstergesi (derlenmedi).
  - `tarama/`: güncel çıktılar.
  - `taslak/`: taslaklar, hakem ve çürütme notları.
- `hesaplar/`: backtest ve olay çalışması kodları ile özet çıktılar. Ham veri repoda yok.
