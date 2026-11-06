# Borsa İstanbul ve ABD'de kazananlar nasıl kazanıyor, sen nasıl kazanırsın? (06.11.2026)

_Veri 05–06.11.2026'ya kadar · yatırım tavsiyesi değildir · kaldıraçlı ürünlerde sermayenin tamamı kaybedilebilir_

İki soruya cevap: (1) Borsa İstanbul ve VİOP'ta para kazananlar nasıl kazanıyor, sen nasıl kazanırsın? (2) ABD borsalarında aynı soru. Ufuk: swing (birkaç gün ile birkaç ay arası), gün içi yok, al-unut yok. Ölçüt: TL'de risksiz getirinin, dolarda T-bill'in ve TL'de kalmanın fırsat maliyetinin üstü.

Yöntem: 16 araştırma raporu ve bunların hepsini kapsayan 6 doğrulama raporu; planlar için ayrıca 6 taslak, 6 hakem ve 4 kırmızı takım incelemesi. Doğrulayıcılar iddiaları birincil kaynaktan ya da ham veriden yeniden hesapladı. Kendi backtest'lerimiz: BIST'te 485 hisse ve 33 endeks (2010–2026), ABD'de Ken French, Chen-Zimmermann, FRED ve AQR verileri (AQR'ninki doğrulamada yeniden hesaplanamadı). Olay çalışmaları: bedelsiz, halka arz, geri alım, içeriden alım, yabancı akışı, faiz döngüsü. Doğrulama raporları ana raporların üstündedir; burada rakamların çoğu doğrulamadan geçti ya da düzeltildi, doğrulanamayanlar ayrıca işaretli. Uygulama planları ayrı dosyalarda: `uygulama/PLAN_BIST.md`, `uygulama/PLAN_ABD.md`.

---

## 0. Önce bir düzeltme: aşman gereken çıta

**"Reel faiz %40–50" doğru değil.** Politika faizi %36 (22.10.2026), Ekim TÜFE yıllık %29,77. Reel faiz geçmiş enflasyona göre ~%4,8, beklentiye göre ~%5–8. %40–50, 2024–25'in nominal faizi ve PPF'nin brüt bileşik getirisiydi (2024'te %53–61), algı oradan geliyor. İleriye dönük brüt bileşik PPF ~%37–42.

| Araç | Bireyde vergi | Çıta (12 ay, net) |
|---|---|---|
| Mevduat, para piyasası fonu (PPF) | %17,5 stopaj | Faiz %36'da kalırsa ~%36–38 (32 günlük mevduat aylık roll ~%37,9; PPF'de 12 ay ~%34–35); anketteki yolda (12 ayda ~%29) ~%31–33. Son 12 ayın PPF medyanı brüt %45,5 → net ~%37,5 |
| BIST'te pay alım-satımı, pay/endeks VİOP | %0 stopaj | Kazanç vergisiz; doğrudan net çıtayla kıyaslanır. Brüt faize göre ~5–7 puanlık avantaj net çıtada zaten var, ayrıca düşülmez |
| VİOP USDTRY ve diğer pay dışı sözleşmeler | %10 stopaj | |
| ABD hisse kazancı (opsiyon/vadeli kazancının vergi niteliği belirsiz, özelge yok) | TL bazında (kur farkı dahil) beyan, %15–40 artan oran; zarar yalnız aynı yıl mahsup | TL'de kalmayı geçmek için vergi öncesi **~%20–28 USD/yıl** (doğrulanmış çapa). Planda hesap büyüklüğü ve maruziyete göre: sermayenin pozisyonda kalma payı u≈0,3'te %12,7–25,9, tam yatırımda ~%17–34 |

- **"Risksiz" de risksiz değil.** Tasfiyedeki 15 PPF'den 4'ü %95–99,9 kaybetti. Çıtayı banka PPF'si, TLREF ya da DİBS ile ölç.
- **2027 stopajı.** Mevduat/PPF'deki %17,5 oran ve DİBS muafiyeti 31.12.2026'da bitiyor; indirim haberi tek ikincil kaynakta. İndirim gelirse net çıta ~1–3 puan yükselir. Çekirdek Aralık'ın son haftasında yeniden seçilir.
- **TL'de kalmanın dolar karşılığı.** İleriye dönük net ~%13–15. Ama bu bir carry işlemi: 2010–2026'da USD bazında yılda −%7,2, en büyük düşüş −%85. Short F_USDTRY Temmuz 2023'ten beri yılda +%20,8 USD getirdi (brüt; USD teminatın T-bill kazandığı varsayımıyla; Türk aracı kurumda teminat ~%0 kazanır, yılda 3,7–5 puan eksik; %10 stopaj hariç), 2018–2026 toplamı ise yalnız +%4,3 (2021'de −%30).
- **Profesyoneller de bu çıtayı aşamadı.** Son 3 yılda, 3 yıllık verisi olan 91 yurt içi hisse senedi yoğun fondan yalnız 1'i (tasfiyedeki Pardus'un BIH'i; getirisi güvenilmez) PPF medyanını geçti. Serbest şemsiyedeki DDF ve %81 hisseli TTL de geçiyor; vergi sonrası kıyasta 108 hisse fonundan 4'ü geçiyor. Üç alt dönemin üçünde de PPF'yi yenen hisse, serbest ya da değişken fon yok. Bunun büyük kısmı beceri eksikliği değil: hisse betası yüksek reel faize yenildi. Medyan aktif hisse fonu endeks fonunu 3 yılda ~22 puan geçti; 5 yılda ise 75 hisse fonunun 72'si PPF'yi geçti (5 yıllık medyan +%838'e karşı PPF +%447). Seçim becerisi var, belirleyici olan rejim.

Sonuç: BIST'te bir stratejinin işe yaraması için yılda ~%31–38 net TL'nin üstüne çıkması gerekiyor. Son üç yılda bunu tutarlı yapan kimse yok. ABD'de dolar bazında vergi öncesi %20–28.

---

## 1. Borsa İstanbul'da kazananlar nasıl kazanıyor?

### 1.1 Kim kaybediyor (taban oran)

- **Bireyler.** MKK hesap verisiyle 20.000 bireysel yatırımcı (2011–12) endeksin haftada ~%0,29 gerisinde kaldı (piyasaya göre düzeltilmiş −%0,286), yılda ~15 puan. En çok işlem yapanlar haftada −%0,538, yılda ~28 puan geride. Yatırımcıların ~%70'i endeksi yenemedi. (Erdem vd. 2014; CAPM alfası anlamlı değil, yön net.)
- **Kaldıraçlı FX müşterileri.** 41 çeyrekte zararda hesap oranının ortalaması %67, 2026/06'da %74,4 (TSPB verisinden yeniden hesaplandı).
- **Kredili işlem yapanlar.** Aracı kurumların 2025 müşteri faiz geliri 53,1 mlr TL, komisyon gelirleri (32,3 mlr TL) toplamından büyük. Örtük kredi maliyeti ~%60.
- **Halka arzda seri bittikten sonra alanlar.** 2025–26'daki 53 arzın 50–51'i seri sonundan sonra düştü, medyan −%55 (bedelsize göre düzeltilmemiş). 2026 arzlarının 36'sından ~26–27'si arz fiyatının altında.

### 1.2 Kim kazanıyor ve nasıl: dört katman

| Katman | Kim | Mekanizma | Getiri büyüklüğü | Senin için |
|---|---|---|---|---|
| **a) Yapıyı işletenler** | Aracı kurumlar, DMA/algo masaları, piyasa yapıcılar | Kredi faizi, komisyon, spread, hız. DMA pay hacminin %28'i, vadelinin %33'ü; DMA pay işlemlerinin %93'ü iki kurumda. Vadeli hacimde yabancı kurum payı %47. | Kurum ölçeğinde sürekli | Kopyalanamaz. Tek ders: bu gişeye ödediğin bedeli (kredi faizi, piyasa emri, sık işlem) küçült. |
| **a′) Manipülasyon ve fon döngüsü** | 2026 krizindeki fonlar ve grupları | Serbest dolaşımı düşük hisselerde dolaşımın üstünde pay toplamak, alarak fiyatı yükseltmek, grup kâğıtlarıyla değerleme. Tera Yatırım 2025'te aracı kurum sektör kârının %35'ini yaptı. TLY fonu 3 yılda +%71.787 getiri gösterdi, oynaklık %21, en derin düşüş −%4,2. Grup hisseleri 16.09'dan beri −%95/−%98. | Kâğıt üstünde sınırsız, sonra sıfır | Yasa dışı ve sonu belli. Ayrıca kendi backtest'imizde kırılım stratejisinin en büyük kârları bu hisselerden geldi (KTLEV, ODINE, HEDEF, PEKGY). Bu hisselerden uzak durmak bir kural olmalı. |
| **b) Faiz/carry** | Mevduat ve PPF sahipleri, TL carry yapanlar | Pozitif reel faiz | Net ~%31–38 TL. Son 3 yılda hisseyi ezdi. | Çekirdek. Ama bu "kazanmak" değil, çıtanın kendisi. |
| **c) Rejim kırılmasında yoğun makro bahis** | Yabancı kurumlar, iyi makrocular | Rejim dönerken ilgili kümeye yoğunlaşmak, kaldıraçla. | Bkz. tablo 1.3 | **Büyük para burada.** VİOP ile uygulanabilir. İsabet düşük, sonradan seçme yanlılığı yüksek. |
| **d) Davranış/akış kenarları** | Disiplinli bireyler, kurumsal masalar | Kırılım ve 52 haftalık zirve, olay öncesi akış (temettü, bedelsiz), çiftler, zorunlu satıcılar | İşlem başına %1–7, çoğu çıtanın çevresinde | Uydu katman. Senin önceki 15–70 bps'lik kenarların burada ama en küçük ucunda. |

### 1.3 BIST'te büyük para nereden çıktı (Ara 2017–2026, dolar bazında)

Bankalar, XU030 ve carry satırları VİOP uzlaşmalarından, long USD satırları spot kurdan hesaplandı. Son üç satır XU100'e göre göreli ve ex post dip-tepe ölçüsü; gerçekleştirilebilir getiri değil.

| Dönem | İşlem | Getiri | Önceden görülebilen sinyal |
|---|---|---|---|
| Ağu 2018 – Oca 2019 | Long bankalar (GARAN) | +%91 (doğrulanamadı) | Kur krizinden sonra sert faiz artışı, reel faiz pozitife döndü |
| Ekim 2020 – Şub 2021 | Long bankalar | +%52 (doğrulanamadı) | Ekonomi yönetimi değişikliği, faiz artışı |
| 2022 | Long XU030 / bankalar | XU030 +%110; YKBNK +%149 (YKBNK doğrulanamadı) | Derin negatif reel faiz (politika %14→%9, TÜFE %78,6+), KKM; hisse enflasyon kalkanı |
| Ara 2017 – Ağu 2018, Ağu – Ara 2021 | Long USD (ortodoks olmayan şok) | +%74, +%121 (spot kur; 2021'de tepeye kadar) | Faiz indirimi ve kur baskısı birlikte |
| May – Ağu 2023, Ara 2023 – Haz 2024 | Long bankalar | +%45, +%73 (doğrulanamadı) | Seçim sonrası ortodoks dönüş, faiz artışlarının sonu |
| Tem 2023 – Eki 2026 | TL carry (short F_USDTRY) | Yılda +%20,8 USD (brüt; T-bill kazanan USD teminat varsayımıyla, Türk aracı kurumda yılda 3,7–5 puan eksik; %10 stopaj hariç) | Pozitif reel faiz, yönetilen kur |
| 08/2025 – 02/2026 | Koza/altın kümesi | XU100'e göre +%88–100 | Altın rekorları |
| 05/2023 – 02/2024, 02 – 06/2025 | Savunma kümesi | Göreli +%100, +%45 | Savunma bütçesi, halka arzlar |
| 06 – 10/2026 | Rafineri | Göreli +%56 (XU100 −%27) | Petrol 100 $ üstü |

"Önceden görülebilen sinyal" sütunu sonradan okuma; bankaların rejim dönüşündeki kazancı n=4.

Ortak nokta: getiri **küme** düzeyinde, **rejim** dönüşünde ve **yoğunlaşmayla** geldi. Ortodoks dönemde 6 aylık pencerelerin yalnız %26'sında XU030 dolar bazında carry'yi geçti (tr_makro_engel; doğrulanamadı). Yani koşulsuz "BIST al" çıtayı geçmiyor. Kazanan, ne zaman long olacağını bilen.

Bireyin erişebildiği meşru büyük kazançlar 2025–26'da hisse seçiminden değil, emtia rejim bahislerinden geldi: gümüş fon sepetleri 2025'te +%195–202 TL, petrol BYF sepeti 2026'da +%115 TL (ajan derlemesi, doğrulamada kontrol edilmedi); 5 yılın en iyi fon kategorisi kıymetli madenler (+%982). Eylül–Ekim çöküşünde kazananlar nakit, döviz, petrol ve VİOP'ta kısa taşıyanlardı (XU030 kısası ≈+%25, n=1).

### 1.4 Swing ufkunda ne işe yarıyor, ne yaramıyor (kendi testlerimiz, doğrulamadan sonra)

**İşe yarayanlar (ama çoğu son 3 yılda çıtanın altında):**

| Yaklaşım | Sonuç | Çekince |
|---|---|---|
| **52 haftalık zirve kırılımı + trend şablonu + %15 iz süren stop** | İşlem başına aynı gün rastgele likit hisseye göre +%5,3 (t 5,1, 2.073 işlem, 17 yılın 15'i pozitif). İsabet %45, ortalama kazanç ortalama kaybın 3,3 katı. 10 slotlu portföyde 36 varyantın medyanı yılda %34,8 TL (bu kuralın gerçekçi dolumlu sürümü %36,2). | En iyi %5 işlem kârın ~%70'i, çoğu sonradan çöken pump hisseleri. Düzeltilmiş risksiz faizle 2024–26'da çıtanın 2–8 puan altında. Gerçekçi tavan/taban dolumuyla en büyük düşüş −%45 (şablonsuz S1'de −%61); dolum modeli 2020 öncesi limiti yanlış modelliyor. |
| **Sektör endeksi rotasyonu** (15 büyük sektör, her ay en güçlü 2–3) | Yılda ~%29,6 TL, uzun dönemde (düşük hesaplanmış) risksizin +11 puan üstü, MaxDD −%34. Hayatta kalan yanlılığı yok. | 2024–26'da risksizin yılda 6–19 puan gerisinde. Sektör endeksi doğrudan alınamıyor, sepetle kopyalanıyor. |
| **Küme rotasyonu** (12 aylık göreli güce göre ilk 3 küme) | Yanlılık düzeltilince eşit ağırlıklı kümelerin yılda ~+5 puan üstü, MaxDD −%40/−%48 | Bu rejimde çıtayı geçmiyor; getiri motoru değil, **küme seçme filtresi**. |
| **52 haftalık zirveye yakınlık sıralaması** | t 2,2–3,7 | 2022 çıkarılınca zayıf (t 0,85–1,5) |
| **Temettü hak kullanımından önceki 5 gün** (spot) | Ham +%1,2 (t 6,5–7,8, n=1.109); piyasaya ve maliyete göre olay başına +%0,2–0,5 | VİOP temettüyü fiyatlıyor; yalnız spotta |
| **Yüksek verimli nakit temettü (duyuruda verim ≥%5)** | Duyurudan sonraki ilk kapanışta al (bildirim 17:00'den önceyse aynı gün), hak kullanımından önceki gün kapanışta sat. Aynı evrenin eşit ağırlıklı toplam getirisine göre +%6,5 (medyan +%4,1, t 6,5, ~27 işlem günü). XU100 kıyasında 12 yılın 12'si pozitif (olay_bedelsiz); 2024–26'da +%13,5. Likit hisselerde de var. | Bu çalışmanın en güçlü yeni kenarı, bağımsız veriyle yeniden üretildi. Açık riskler: iptal edilen teklifler örnekte yok, etkinin bir kısmı kazanç açıklaması olabilir, test önceden kayıtlı değil. Girişlerin %81'i Şubat–Mart'ta, yılda 14–25 olay. Hedgelenirse getiri ≈ TL faizi + %6–7; plan bunun yarısını bekliyor. |
| **Bedelsiz** (601 olay) | Hak gününden sonraki 10 günde −%3,3 (t −5,5); 2024–26'da zayıf (−%1,45, t −1,5). Bu yüzden hak gününden önce satmak geçerli bir çıkış kuralı. | Alım tarafı **işe yaramıyor**: duyuru etkisi tavan kilitli günlerde, "onayda al, bölünmeye sat" net −%0,07, duyuruda alıp 5 gün tutmak −%1,6. |
| **Halka arz katılımı** | Gün içinde tavan ilk bozulduğunda satan katılımcı medyan +%33; seri bozulduğu günün kapanışında satan +%38 (planın kuralı) | Hesap başına yılda 8–22 bin TL, ölçeklenmiyor. Seri bitince almak zarar: 21 günde medyan −%11, 2024–26'da −%17. |
| **Çiftler: SAHOL↔AKBNK, KCHOL↔iştirak sepeti** (\|z\|≥2) | Gerçekçi 1 gün gecikmeyle işlem başına +128–310 bps (t 2,1–2,8, maliyet öncesi; maliyet sonrası +88–290 bps) | Önceki çalışmadaki 1–3 günlük SAHOL/AKBNK kenarının 20 günlük karşılığı; çift o çalışmadan seçildi (seçim yanlılığı). Kurumsal olay riski. |
| **12 aylık zaman serisi momentumu (XU100)** | 2019–26'da long/nakit yılda %48 (nakit %25, düşük hesaplanmış seri) | Zayıf istatistik. Şu an kapalı: XU100 12 ayda +%3,8, nakit ~%37 (test serisi; gerçekleşen brüt PPF ~%45,5). |

**İşe yaramayanlar:**
- Klasik 12-1 kesitsel momentum: risksizin altında.
- Kısa vadeli reversal: eşit ağırlıklı evrene göre yılda −%17,9. Haftanın kaybedenleri kaybetmeye devam ediyor.
- Endekste SMA200 ve 50/200 kuralları.
- Bedelsizde alım tarafı, halka arzda seri bittikten sonra almak.
- Geri alım ve içeriden alım: eşleştirilmiş kontrollerle kalıcı bir kenar yok.
- Yabancı akımı: fiyatı izliyor; ileri getiriyi ancak zayıf öngörüyor (2024–26 t 1,1), işlem sinyali değil.
- AKD/takas takibi: bilgili işlem ölçüleri getiri öngörmüyor.
- Ramazan etkisi, A/B pay oranları.

**Faiz döngüsü ve bankalar:** Faiz indiriminden sonraki 63 günde bankalar XU100'ün gerisinde kaldı; 6 döngünün 6'sında, ortalama −%6,3 (t −4,2). İndirimden önceki 63 günde ise +%3,2 önde. Bankalar son 63 günde XU100'e göre +%26 koştu (mutlak değil; XU100 21.08'den bu yana −%22) ve 10.12 PPK'da anket indirim bekliyor. Bağımsız gözlem yalnız 6 döngü; bu bir işlem kuralı değil, boyut eğilimi.

### 1.5 Kazananların BIST'teki gerçek formülü

1. **Çekirdek çıtada dursun.** Paranın çoğu net ~%31–38 TL'de. En verimli araç vergiye göre seçilir: banka PPF'si, mevduat, DİBS ya da XU030 nakit-taşıma (spot long + vadeli short; iki bacak da %0 stopaj, ima edilen basit faiz ~%29,3; bugün kapalı, açılış eşiği %35,6).
2. **Risk sermayesi rejim döndüğünde kümeye yoğunlaşsın.** Tetikler §2'deki rejim anahtarıdır: XU100'ün 50 ve 200 günlük ortalamaların üstüne dönmesi, swap hariç net rezervin 3 hafta üst üste artması, 2 ay üst üste aylık TÜFE <%2, CDS <230 ve düşüyor, XBANK 200 günlüğünün üstünde. Yabancı alımı tetik değil, fiyatı izliyor. Faiz indirimi bankalar için alım tetiği değil, uyarı: indirimden sonraki 63 günde bankalar 6 döngünün 6'sında geride kaldı; sürprizsiz indirimden sonra bankalarda yarım boy. Araç kaldıraç değil, rejimle büyüyen boy: kırılım motoru tam boy ve endeks/küme kolu; kredili işlem hiç yok, endeks kolu en çok 1x, AÇIK'ta net endeks betası ≤ +%40.
3. **Rejim kapalıyken uydular.** Çiftler, temettü öncesi spot, KAP teyitli özel durumlar (ZPAT, satma hakkı). Kırılımları likit ilk 75 hissede (VİOP-47 öncelikli, diğerleri 0,75 boyla), fon tasfiyesi baskısı taşımayanlarda, küçük boyutla dene.
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
| GEÇİŞ | XU100 5 kapanış üst üste 50 günlüğün (12.691) üstünde **ve** swap hariç net rezerv 3 hafta üst üste artıyor **ve** şu üçünden biri: 2 ay üst üste aylık TÜFE <%2, CDS <230 ve düşüyor, XBANK 200 günlüğünün üstünde | Kırılım yarım boy (risk %0,5) |
| KAPALI | Diğer her durum. **Bugün: 7 göstergenin 0'ı açık.** | Kırılımda en çok 2 küçük deneme (%0,25 risk). Rejimden bağımsız kollar açık. |
| KRİZ kesicisi | 5 günde XU100 ≤−%8, kur ivmesi, teyitli CDS >300, swap hariç net rezerv 2 hafta üst üste ≤−5 mlr $ ya da seviye <0, F_USDTRY ima faizi politika faizi +5 puanın üstünde ya da MSCI sınıflandırma danışması | 5 gün yeni giriş yok; K6 ve hedgesiz K3/K3b kapanır; K4, K5, K9 stopu KRİZ günü kapanışının en çok %10 altına çekilir; K1 sürer |

GEÇİŞ için en erken gerçekçi tarih 26.11 kapanışı. 12.11'deki rezerv verisi bir hafta daha −5 mlr $ ya da daha kötüsünü gösterirse KRİZ kesicisi tetiklenir. Aynı veri ABD planındaki döviz anahtarının birinci tetiğini de tamamlar (§4).

**Kollar:**

| Kol | Kural (özet) | Durum |
|---|---|---|
| Çekirdek | Pazartesi hesabın %15'i bankada 32 günlük mevduata, %85'i banka iştiraki PPF'ye. Hedef %60 mevduat / %40 PPF; dilimler 9, 16, 23 ve 30.11'de. | **BIST hesabında Pazartesi yapılacak tek finansal işlem** (ABD tarafındaki SWIFT için §4) |
| K1 SAHOL↔AKBNK | 60 günlük oran z-skoru \|z\|≥2 olunca VİOP'ta ters spread, ertesi kapanışta giriş, 20 işlem günü tutulur; çiftin K/Z'si bacak nominalinin −%8'ine inerse felaket stopu | Rejimden bağımsız. Şart: teminat faiz kazanmalı, komisyon bacak ve yön başına ≤5 bps. |
| K3 Temettü öncesi 5 gün | Spotta hak kullanımından 6 gün önce al, bir önceki gün kapanışta sat; temettü alınmaz | Rejimden bağımsız; küçük kenar (piyasa ve maliyet sonrası olay başına +%0,2–0,5) |
| K3b Yüksek verimli temettü | Verimi ≥%5 ve hacmi ≥20 mn TL olanı ilk bildirimden sonraki ilk kapanış seansında al (17:00'den önceyse aynı gün), hak kullanımından önceki gün sat; Kural 0 sağlanır ve tutar yeterse XU030 vadelisiyle hedgele (1 mn TL hesapta genelde hedgesiz) | En güçlü yeni kenar: denetimde muhafazakâr kıyasla +%6–7 fazla getiri, ~27 işlem günü; plan beklentisi bunun yarısı, olay başına +%3…+%3,5. Sezonu Şubat–Mayıs; 01.02.2027'den yarım boylu pilot (olay başına %1,25). |
| K4 Kırılım motoru | 52 haftalık kapanış zirvesi + trend şablonu + %15 iz süren stop; giriş kapanış seansında | Boyut rejime bağlı. En yakın tetikler: ENJSA 127,00; AHGAZ 48,70 / ENERY 14,60 (tek isim sayılır); RYSAS 30,28. |
| K5 Özel durumlar | Zorunlu pay alım teklifi, satma ve ayrılma hakları | Yalnız KAP teyidiyle. Zorunlu teklifte kayıt tarihi kuralı varsayılır: sonradan alınan pay teklife verilemez, işlem yok. Kalan gönüllü teklif ve satma hakkı; katkı ~0. AKCNS teklifi kapanmış, listeden çıktı. |
| K6 TL carry | Short F_USDTRY, %10 stopaj | Kapalı: 6 kapı koşulundan 3'ü sağlanmıyor (net rezerv düşüşü, yabancı DİBS çıkışı, brüt rezerv 158,1 < 160 mlr $); en erken 19.11 |
| K7 Endeks/küme beta | 12 aylık momentum açıkken | Kapalı |
| K8 Halka arz katılımı | Yalnız eşit dağıtımlı arza katıl; 18:00'de son fiyat tavan değilse o günün kapanış seansında sat (gün içi izleme yok; medyan +%38); seri bitince asla alma | İsteğe bağlı, risk bütçesi dışında. Hesap başına yılda 8–22 bin TL. 3 Eylül'den beri onay yok. |
| K9 Serbest kol | Plan dışı her fikir yalnız buradan, %0,25 risk | Birikimli −%1,5'te 6 ay kapanır |

**Kaçınma takvimi:**
- 9.11'de bilançosunu 18:00'e kadar açıklamamış hisselere giriş yok.
- 11.11 kapanışında hiçbir kolda, 11–13.11 kapanışlarında K3, K4, K5 ve K9'da yeni giriş yok.
- Kredili işlem esnekliği 13.11'de uzatılmazsa:
  - kırılım girişleri 23.11'e kadar yok;
  - VİOP-47 dışında long 30.11'e kadar yok.
- MSCI'ın çıkardığı ya da ağırlığını düşürdüğü hisseler, değişiklik yürürlüğe girene kadar alınmaz. MSCI'da yalnız artışlar dondu, azaltma ve çıkarmalar sürüyor; sınıflandırma danışması açılırsa KRİZ.
- Bedelsizde hak günü dahil 10 işlem günü (oran ≥%500'de 20), yüksek verimli temettüde (verim ≥%5) hak günü dahil 5 işlem günü yeni alış yok.
- 10.12 PPK sürprizsiz bir indirimse, ~15.03.2027'ye kadar bankalarda yarım boy. Gerekçe: indirimden sonraki 63 günde bankalar 6 döngünün 6'sında XU100'ün gerisinde kaldı.
- Dışlama listesindeki hisseler (fon tasfiyesi baskısı, SPK suç duyurusu) hiçbir kolda alınmaz.

**Dürüst beklenti (12 ay, vergi sonrası, çıtaya göre):**
- Merkez **+1…+2 puan**; %80 aralık −2…+5,5. Toplam net nominal getiri ~%33–37 (reel ~%3–7); KAPALI sürerse yalnız +0,5…+1,5 puan. 12 ayda çıtanın altında kalma olasılığı ~%35–45.
- USD bazında ağırlıklı ~+%10 (çok belirsiz); kur kırılmasında (öznel %10) şok anında −%10…−%21. Plan bunu BIST hesabının içinde korumasız kabul ediyor; servet düzeyindeki kur kontrolü ABD planının döviz anahtarı (§4). Ölçü birimini (TL ya da USD) Pazartesiden önce yazılı seç.
- Senaryo olasılıkları (öznel): sönümlenme %35, yatay kanama %40, kontrollü kur hızlanması %15, kırılma %10.
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
  - Ürettikleri şey yüksek getiri değil, yüksek Sharpe. Arkasında sektörde ~12x brüt (~4,5x net) kaldıraç ve pod başına ~%5 düşüşte risk kesme, %7,5–10'da tasfiye kuralı var (doğrulamada kontrol edilmedi).
- **Medallion ve RIEF.** 2020'de Medallion +%76, aynı firmanın dışarıya açık fonu RIEF −%22,6 (25 Aralık'a kadar). Kısa ufuklu sinyaller kapasiteyle ölüyor. Senin BIST mikro kenarların bu türden.
- **CTA/trend fonları.** SG Trend 2022'de +%27,3; Nisan 2025'te 12 aylık kaybı −%18'i aştı ("en kötü 12 ay" ifadesi doğrulanamadı). 2000'den beri yıllık %5,2.

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

- İşlem başına risk sermayenin %0,25–1'i. Stop yapısal ve dar (1 ATR ya da %7–10), ama giriş ve stop çoğunlukla gün içi (açılış aralığı tepesi, günün dibi). Kapanış bazlı kopyada 1 ATR altı stop kötü sonuç verdi; plan 1–2 ATR ve ≤%8 kullanıyor.
- İsabet %22–35, ortalama kazanç ortalama kaybın 3–5 katı. Minervini'ye atfedilen daha yüksek isabet (%44–63) ve 2,15× oran doğrulanamadı. İşlem başına +0,4–0,6R beklentisi bu girdilerden türetilmiş bir tahmin ve zayıf kanıta dayanıyor (Luk ve Minervini'nin işlem istatistikleri doğrulanamadı). Senin gün sonu uyarlaman hiç test edilmedi; planın beklentisi +0,1R (−0,2…+0,4R), öznel %50–60 olasılıkla sıfır ya da altı.
- Giriş: göreli gücü en yüksek tema liderlerinde taban kırılımı, kazanç sonrası boşluk, yükselen 10/20 günlük ortalamaya ilk geri çekilme.
- Kâr alma: 3–5 günde 1/3–1/2 satış, kalan kısım 10/20 günlük ortalamayla taşınıyor.
- Yalnız kazanana ekleme. Kazanırken pozisyon büyüyor, kaybederken küçülüyor.
- **Katı piyasa rejimi anahtarı.** Kullamägi kendi filtresine uysaydı 2022 kaybının ~%90'ından kaçacağını söylüyor.
- 4–8 pozisyon, tema yoğunlaşması.

Akademik destek bileşenlerde var: haber destekli fiyat şokları sürüyor, 52 haftalık zirveye yakınlık ve sektör momentumu getiri öngörüyor. Bessembinder'e göre hisselerin %4'ü bütün net servet yaratımını açıklıyor. Tekil hisse trend takibinin uygulayıcı yazarlı çalışma kâğıdı (Zarattini-Pagani-Wilcox) yılda ~%15 brüt buluyor; işlemlerin %7'sinden azı kârın çoğunu üretiyor.

### 3.4 Kamuya açık anomaliler büyük ölçüde bitti (kendi hesaplarımız ve literatür)

| Kenar | 2010 sonrası |
|---|---|
| 165 net yayımlanmış anomali (Chen-Zimmermann) | Ortalama uzun-kısa getiri yayın öncesi %0,75/ay → yayın sonrası %0,32 → 2010 sonrası %0,30 → likit evrende %0,20. Anlamlı kalan pay %16. |
| 12-1 hisse momentumu (UMD) | Yılda %2,6–4, Sharpe 0,26 |
| PEAD | Büyük hisselerde 2006'dan, mikrocap'lerde 2016'dan beri yok |
| Kısa vadeli reversal | ~%0 (yalnız VIX>25 aylarında pozitif) |
| Pre-FOMC, S&P 500'e ekleme, spin-off, ay dönümü | Bitti ya da çok küçüldü |
| Sektör momentumu | Uzun dönemde gerçek. 2010 sonrası risk ayarlı olarak piyasanın biraz altında (Sharpe 0,86'ya karşı 0,97), 2015 sonrası belirsiz. |
| Opsiyon almak | Koşulsuz zarar: straddle haftada ~−%3, piyango call'ları haftada −%35 |
| Hayatta kalan tek güçlü sinyal grubu | Opsiyon fiyatlarından çıkan sinyaller (skew; t 5–6), analist revizyonu, ardışık kazanç sürprizi. Hisse seçme filtresi olarak değerli, tek başına getiri motoru değil. |

**%15–25 USD bandı yalnız kaldıraçlı betayla görülüyor.** 2x/3x Nasdaq-100 + 200 günlük ortalama filtresi 2010–26'da yılda %18–26 getirdi. Bedeli: en büyük düşüş −%41 (2x) ile −%97 (3x, tam dönem) arası; 2000–02'de 3x versiyon −%89. Filtre 2010–26'da getiriyi düşürdü (3x NDX'te %35,6'dan %24–26'ya), yalnız düşüşü kesti. Bu alfa değil, kaldıraçlı hisse primi.

---

## 4. Sen ABD borsalarında nasıl kazanırsın? (9 Kasım için)

Ayrıntılı kurallar `uygulama/PLAN_ABD.md` dosyasında, akşam rutini `uygulama/ABD_GUNLUK_RUTIN.md`'de, rejim ve trend şablonu göstergesi `uygulama/kod/abd_rejim_ve_sablon.pine` dosyasında (TradingView'da derlenmedi). Plan BIST planıyla aynı süreçten geçti: üç bağımsız taslak, üç hakem, iki çürütme incelemesi. İskelet "önce risk" taslağından, işlem mekaniği "lider momentumu" taslağından alındı. Kaldıraçlı endeks çekirdeği reddedildi: fiilen kaldıraçlı al-tut, ve 2010 sonrasında filtre getiriyi de kesti.

**Yöntem: doğrulanmış şampiyonların yönteminin gün sonu uyarlaması, gün içi ekransız.** Doğrulanan yöntem değil, şampiyonların sonuçları; yöntemin bu uyarlaması hiç test edilmedi.
- Tek canlı kol: rejim filtreli lider swing. İki kurulum var:
  - **S1 baz kırılımı:** pivot üstüne al-stop limit.
  - **S2 yükselen 10/20 günlük ortalamaya geri çekilme.**
- Girişler 16:45–17:15 TSİ arasında, bekleyen emirle: BUY STOP-LIMIT ve ekli, iyi-iptal SELL STOP.
- Çıkışlar ve stop düzeltmeleri gece 00:30–01:00 ya da sabah 08:00–09:00 arasında, kapanışa göre.
- 17:30–00:00 arasında ekrana bakılmaz.
- Kâr alma: +2R'de ya da 4. seansta ≥+1R ise 1/3–1/2 satılır, kalan 10/20 günlük ortalamayla taşınır.
- Bilanço gap'i ve VIX çözülmesi kurulumları önce yalnız kâğıt üzerinde (gölge) kaydediliyor. Opsiyon, margin, açığa satış ve kaldıraçlı ETF ilk fazda yok.

**Rejim bugün KIRMIZI:**
- KIRMIZI'yı tek başına VIX/VIX3M 1,10 (≥1,00) tetikliyor. Bu zayıf bir gösterge: 4.11'de VIX 16,61'di, terslik tek günlük bir sıçrama.
- VIX düzelse de SARI tetiği yok: S&P ve Nasdaq'ta 10 günlük ortalama 20 günlüğün altında, dip teyit günü (FTD) yok. Hüküm bu yüzden geçerli.
- Nasdaq düzeltmede (zirveden −%14,7). S&P 500 200 günlüğün ancak %0,4 üstünde.

Sarıya geçmek için şartların 3 kapanış üst üste sağlanması gerekiyor. Bu yüzden **Pazartesi canlı işlem yok; ilk canlı deneme en erken 16.11**, tek pozisyonla ve AI dışı bir kümeden.

**Sermaye:**
- Para TL'deyse ABD strateji sermayesi (E) likit servetin **%10'u** (en çok %15'i). E'nin %40'ı (servetin ~%4'ü) **Pazartesi sabahı**, IBKR hesabı onaylandıysa, SWIFT'le IBKR nakit hesabına gider (önce küçük tutarla kur makası ölçülür); %10'u banka PPF'sinde, %50'si 32 günlük mevduatta bekler. Bu, Pazartesinin BIST çekirdeğinden sonraki ikinci finansal işlemi.
- Para zaten USD'deyse servetin en çok %20'si; çevrim yok.
- **Döviz anahtarı (servet düzeyi; PLAN_ABD §1.5).** Aşağıdaki beş tetikten ikisi oluşursa servetin USD nakit payı %25–35'e çıkar. Fazla USD IBKR'ye değil, Türk bankasında döviz mevduatına gider; E ve işlem riski değişmez. Tetikler (bugünkü değer):
  1. Swap hariç net rezerv <0 ya da 2 hafta üst üste haftalık düşüş >5 mlr $ (24,3 mlr $; son hafta −6,5: yarısı oluştu).
  2. Yabancı DİBS çıkışı 2 hafta üst üste >1 mlr $ (−750 mn $: yok).
  3. 5 yıllık CDS >300 (248, doğrulanamadı: yok).
  4. 1 aylık USDTRY vadelisinin zımni yıllık getirisi politika faizini 5 puan aşıyor (~%32–33; eşik %36 + 5 = %41: yok).
  5. Ex-ante reel faiz <%3 (%9,8; makul bant %5–8: yok).

  Kontrol her Perşembe TCMB rezerv verisiyle. 12.11 verisi bir hafta daha >5 mlr $ düşüş gösterirse 1. tetik tamamlanır; anahtar için bir tetik daha gerekir.
- **İki planın çelişkisi ve çözümü.** BIST planı kur korumasını reddediyor ("S4'teki USD kaybı bilinçli olarak kabul edilmiştir"). İki kural farklı katmanda: döviz anahtarı **toplam servete** uygulanan bir risk kontrolü; BIST planının "kur koruması yok" kuralı yalnız **BIST işlem hesabının içinde** geçerli (hesapta USDTRY call'ı ya da carry primi ödenerek koruma alınmaz). Bu okumada anahtar tetiklenirse BIST hesabının kolları ve kuralları değişmez. Planlar BIST hesabının servetteki payını ABD E'siyle bağlamıyor ve ek USD'nin servetin hangi TL kısmından çevrileceğini söylemiyor. Bu yorumu ve çevrimin kaynağını Pazartesiden önce yazılı teyit et.

**Risk (ilk 50 işlem):**
- İşlem başı risk %0,25, tek pozisyon ≤%7,5.
- Küme ısısı ≤%0,75. Toplam açık risk sarıda %1,25, yeşilde %2,5.
- Aylık devre kesici %3 (ay içi zarar + açık risk). Strateji sermayesinde −%8'de plan durur.
- Kritik bir kural ihlalinde (stop indirmek, zarara eklemek, rejim dışı giriş) 10 seans işlem yok; ikinci ihlalde plan durur.

**Erişim:**
- Ana platform IBKR Pro nakit hesap. Türkiye'den açılabiliyor, ~0,005 $/adet; gerçekçi ilk işlem 11–13.11.
- Midas yalnız ≤500 $ ile test için: ekli stop/GTC ve MOO desteği teyit edilmeli. Call/put alımı açık ve teknik kilit yok; bu yüzden test parası dışında bakiye tutulmaz.
- PDT kuralı (25 bin $) kalktı (aracı kurum geçişi 20.10.2027'ye kadar); nakit hesaba zaten uygulanmıyor, Reg T ve free-riding kısıtları sürüyor.

**Vergi:** Kazanç TL bazında, kur farkı dahil, beyanla vergilenir; zarar yalnız aynı yıl içinde mahsup edilir. Her işlemi TCMB kuruyla kaydet.
- Hayalet vergi: USD getirisi sıfır olsa da pozisyondaki sermayenin kur farkı vergilenir (u=0,3 ve kur +%20'de hesap büyüklüğüne göre E'nin ~%0,75–1,55'i).
- 9.11–31.12 kendi başına kısa bir vergi yılı; 2026 zararı 2027'ye devretmez. Bu yüzden 2026'da Faz 1 boyutunda kalınır.
- Aralık'ta yalnız vergi için çıkış yok. Tek istisna kazanç hasadı: 2026 net TL sonucu negatifse kârdaki lotlar en geç 30.12'de satılıp ertesi seans geri alınır (wash-sale benzeri kural olmadığının müşavirle yazılı teyidiyle).
- 60 bin $ üstü US-situs varlıkta ABD veraset vergisi riski var; E 250 bin $ ve üstündeyse gerçek. 2026 tarifesi doğrulanamadı.

**Dürüst beklenti:**
- İlk faz bir ispat dönemi. Medyan beklenti kenara göre −%2,5 ile +%6,5 arası; TL'de kalmayı geçme olasılığı %5'in altında.
- Ağırlıklı merkez vergi öncesi −%1,5…+%1,5, vergi sonrası −%2…+%1: USD nakdin altında. TL'de kalmaya göre servete maliyeti yılda ~%0,3–0,8; karşılığı, ~%7–10 olasılıkla ölçeklenebilir bir kenarı ucuza keşfetmek.
- Kapılar: 50 işlem, ≥4 ay, ≥+0,25R ve t ≥1,0 → risk %0,5 (sermaye aynı). 100 işlem, 12 ay, t ≥1,65, en az bir KIRMIZI→YEŞİL döngüsü ve hayatta kalma yanlılığından arındırılmış gün sonu backtest'i → %0,75 (en çok %1). O noktada da dürüst merkez yılda ~%8–16.
- Yılda %40+ ≥+0,3R kanıtlı kenar, yılda ≥150 işlem ve ~%5 olasılıkla −%45 düşüşü birlikte ister. Doğrulanmış üst dilimde görülüyor, medyan trader'da görülmüyor.

---

## 5. Ortak sonuç: senin için gerçekten işe yarayan yol

1. **Mikro kenarlardan büyük, az sayıda, pozitif çarpık bahse geç.** İşlem başına 15–70 bps'lik kenarlar senin elinde maliyet, gecikme ve sönümle yeniliyor. Kenarın %35–58'i yayından sonra kayboluyor; senin BIST30 kenarların tam da en hızlı sönen sınıfta. Sermayeyi büyüten şey ise az sayıda büyük kazanç. Hem BIST kırılım testinde (en iyi %5 işlem kârın ~%70'i) hem ABD tekil hisse trend testinde (işlemlerin <%7'si kârın çoğu) kâr az sayıda işlemden geliyor.
2. **Sermayenin çoğu çıtada, risk sermayesi rejim açıkken çalışsın.** BIST'te çıta net ~%31–38 TL; ABD'de TL'de kalmayı geçmek için vergi öncesi ~%20–28 USD. Rejim kapalıyken (bugün iki piyasada da) agresif olmamak tembellik değil, bir risk kontrolüdür. Rejim filtresi getiri kaynağı değil (ABD'de endeks düzeyinde getiriyi korumadı: SARI+ günlerinde yıllık +%10,7, diğer günlerde +%19,1); faydası çöküş yıllarında görünür (FFTY 2022'de −%51).
3. **Kümelemeyi risk birimi yap.** Bankalar+holding+havacılık BIST'te tek bahis (korelasyon 0,77–0,79). ABD'de yarı iletken ve elektrik ekipmanı tek bahis (0,72; ajan hesabı, doğrulanamadı). Makro düzeyde de aynı: TL carry ile banka uzun pozisyonu aynı şokta birlikte kaybeder (kırılma senaryosunda carry −%10/−%25, bankalar −%30/−%40). Bugün geçerli sınırlar planlardaki gibi:
   - BIST: küme başına yönlü pozisyon KAPALI'da 1, GEÇİŞ/AÇIK'ta 2; toplam açık stop riski KAPALI/GEÇİŞ/AÇIK'ta %2,5/%3,5/%5,5; stres tavanı %6/%8/%10; aylık uydu kaybı −%2,5'te (AÇIK'ta −%3) ay sonuna kadar yeni giriş yok.
   - ABD (ilk 50 işlem): küme ısısı ≤%0,75; toplam açık risk SARI %1,25 / YEŞİL %2,5; ay içi zarar + açık risk %3'te o ay yeni giriş yok.
   - Küme ≤%1,5, toplam %5–6 ve aylık %6 yalnız ABD'de Faz 2–3 kapılarından sonra.
4. **Zorunlu satıcının önünden çekil; karşısında durmayı henüz kenar sayma.** MSCI kararları (yalnız artışlar dondu, azaltma ve çıkarmalar sürüyor; Haziran 2027'ye kadar ilerleme yoksa Frontier/Standalone danışması, pasif akış net negatif), kredili esnekliğin bitişi (13.11), fon uyumu (31.01.2027) ve tasfiye takvimi (~17.03.2027) planlarda kaçınma kuralı: etkilenen hisse yürürlüğe ya da takvim sonuna kadar alınmaz, düşen hisse "dipten" alınmaz. Likidite primi ABD verisinde var (reversal yalnız VIX>25 aylarında pozitif, +%0,55/ay, n=29; planda yalnız gölge kayıt); BIST'te kısa vadeli reversal eşit ağırlıklı evrene göre yılda −%17,9 ve zorunlu akış tezi n=1. Denenecekse yalnız K9'dan, %0,25 riskle, yazılı fikir kartıyla.
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
- **Olay çalışmaları.** Yüksek verimli temettünün fazla getirisi muhafazakâr kıyasla +%8,5'ten +%6,5'e, halka arz katılımcı primi ileriye bakışsız kuralla medyan +%45'ten +%33–38'e indi.

**Sınırlar:**
- **Web araması.** Alt ajanların ortak web arama kotası (200) iş ortasında doldu. Doğrulayıcıların çoğu birincil kaynakları doğrudan indirerek çalıştı; erişemedikleri iddiaları "doğrulanamadı" diye işaretlediler.
- **Veri erişimi.** Yahoo istek sınırı koydu, Stooq bot doğrulaması istedi, TEFAS otomatik erişimi reddetti; bunların hiçbiri aşılmaya çalışılmadı. Bu yüzden ABD'de hisse düzeyinde earnings-gap/kırılım testi yapılamadı. ABD planındaki aday listesi kaynaklı web derlemesi ve senin çalıştıracağın tarama ayarları.
- **Halka arz verisinde bir istisna.** halkarz.com betikle yapılan isteklere 403 verdi. Ajan taramayı durdurdu ama detay sayfalarını sonra başka bir araçla (WebFetch) tek tek okudu. Denetçi bunu "engelin başka bir istemciyle aşılması" sayılabilir diye işaretledi.
  - Arz listesi ve fiyatlar başka kaynaklarla (İş Yatırım birincil halka arz listesi ve fiyat serileri) doğrulanıyor.
  - Katılımcı sayısı ve lot alanları ise yalnız o sayfalardan geliyor. Bu alanlar KAP'taki satış sonuçları bildirimlerinden yeniden alınmalı.
  - Ham veri repoda yok.
- **Değer faktörü test edilmedi.** Bütün testler fiyat tabanlı. Hakemli BIST kanıtında en güçlü faktör değer (yılda %14–19 prim); MSCI Türkiye ileri F/K 6,66, EM 9,72.
- **Backtest kör noktaları.** BIST dolum modeli Mart 2020 öncesi ±%20 fiyat limitini ±%9,5 sanıyor (hatanın yönü belirsiz). Çekilmeyen 99 kod arasında krizin iki ana pump hissesi OZATD ve TEHOL var. ABD kaldıraçlı testinde bir günlük gecikme 2000–02 düşüşünü −%89'dan −%75'e oynatıyor; NDX sonradan en iyi çıkan endeks.
- **Hayatta kalan yanlılığı.** BIST hisse evreni bugün işlem gören hisselerden kurulu; bu sonuçları yukarı çarpıtıyor.
- **Öznel tahminler.** Rejim senaryolarının olasılıkları (§2) ve planlardaki Monte Carlo sonuçları öznel, kalibre değil.

## Dosyalar

- `ajanlar/`: 16 araştırma raporu.
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
