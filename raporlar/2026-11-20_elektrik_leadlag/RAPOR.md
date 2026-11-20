# BIST elektrik hisselerinde 1–3 günlük öncülük sinyalleri

*20.11.2026 · Seviye L+ · Yatırım tavsiyesi değildir. Bütün rakamlar geçmiş veriye dayanır.*

Sözlük: **bps** = baz puan, %0,01 (100 bps = %1). **t** = etkinin kendi belirsizliğine oranı; kabaca 2'nin üstü "şans olma olasılığı düşük" demektir. **XELKT** = BIST Elektrik endeksi (42 hisse). **Sepet** = o gün alınabilir durumdaki elektrik hisseleri, eşit tutarla. **Ham getiri** = pozisyonun kendi getirisi. **Fazla getiri** = sinyal günleri ile aynı dönemin sıradan günleri arasındaki fark.

## 1. Kısa yanıt

- Aradığın türden öncülük ("X bugün hareket etti, Y yarın izler") elektrik hisselerinde kullanılabilir biçimde **yok**: hisse çiftleri, XU030 → sektör, büyük → küçük ve VİOP baz/hacim sinyalleri sınandı; kalıcı ve maliyeti aşan bağ çıkmadı.
- Var olan şey **momentum**: XELKT 20 günlük zirve yaptığında ya da sert yükseldiğinde sektör sepeti sonraki 3 günde sıradan günlerden 70–85 bps fazla getirdi (2023 → Kasım 2026).
- Bu fark kâra dönüşmüyor: yaklaşık 30–35 bps işlem maliyeti ve 3 günlük TL faizi (yaklaşık 32–44 bps) düşünce ortalama sıfıra yakın. Kazanç birkaç yükseliş dalgasından geliyor.
- Bu yüzden sinyalleri **"ne zaman alınır, ne alınmaz" süzgeci** olarak kullan; tek başına para kazandıran strateji olarak değil.
- AKSEN, ENJSA, ODAS'ta sektör sinyali çalışmıyor. Doğrulanan VİOP satış sinyali yok. Alımlar vadelide değil spotta yapılmalı.
- En işe yarar bulgu bir kaçınma kuralı: o gün tabana değmiş ya da sektörün 5 puan gerisinde kapanmış hisse kapanışta alınmaz.

## 2. Ne yapmalıyım

### 2.1 Sinyaller ve TradingView kodları

| Sinyal | Koşul (gün sonunda) | Ne alınır | Güven |
|---|---|---|---|
| **S1 Zirve** | `BIST:XELKT` kapanışı son 20 işlem gününün en yüksek kapanışı | Sepet, 3 gün | Orta; yalnız zamanlama süzgeci |
| **S2 Güçlü gün** | `BIST:XELKT` günlük artışı ≥ önceki 60 günün günlük oynaklığı (bugün %2,1) | Sepet, 3 gün | Orta-düşük |
| **S3 Piyasa önde** | `BIST:XU030` artışı ≥ kendi 60 günlük oynaklığı (bugün %1,9) **ve** XELKT artışı bunun yarısından az (bugün < %1,05) | `BIST:AKSEN`, `BIST:ENJSA`, `BIST:ODAS` spot, 3 gün | Düşük; izleme |
| **K Kaçınma** | Hisse o gün tabana değdi ya da sektör ortalamasının ≥ 5 puan gerisinde kapandı | O hisseyi o gün alma | Orta |
| **D Sakin hisse** | 20 günlük oynaklığı sektörün alt yarısında | Seçerken öncelik ver | Düşük; günde 5–12 bps |

- "Oynaklık" = günlük getirilerin standart sapması. Göstergede **z** olarak görünür: günlük getiri ÷ oynaklık. S2 "z ≥ 1" demektir.
- S1 ve S2 aynı gün gelirse geçmişte etki daha büyüktü (+125 bps, 54 gün). Bu sonradan bakılmış bir kesittir, doğrulanmadı.
- Vadeli kodları: `BIST:AKSEN1!`, `BIST:ENJSA1!`, `BIST:ODAS1!`, `BIST:XU030D1!`. Bunlar yalnız izleme içindir; aşağıdaki alımların hiçbiri vadelide yapılmaz.

**Bugünkü durum (20.11.2026 kapanışı):** üç sinyal de yok. XELKT 537,06, XU030 13.957,13. Bir sonraki işlem günü için tetikler: S1 XELKT ≥ 571,59; S2 XELKT ≥ 548,31; S3 XU030 ≥ 14.220,17 ve XELKT < 542,68. Kaçınma listesinde MAGEN var.

### 2.2 Günlük akış

1. **17:30:** hisselere bak. Tabana değmiş, sektörün 5 puan gerisinde ya da +%7'nin üstünde olanları (tavanda kapanma olasılığı yüksek) listeden çıkar.
2. **17:50:** XELKT'ye bak. S1 ve S2 bu saatte büyük ölçüde belli: 17:50 değeri kapanış sinyalinin S1'de %95'ini, S2'de %87'sini yakalıyor.
3. **17:55–18:00:** XELKT eşiğe çok yakınsa (zirvenin ±%0,15'i) 18:00 değerini bekle. S3'e yalnız 18:00'de bak; 17:00'de sinyalin ancak yarısı görünüyor.
4. **18:01–18:04:** kapanış seansına emir gir (son fiyatın 1–2 adım üstünde limit ya da piyasa emri). Fiyat 18:05'te belirlenir.
5. **18:08–18:10:** dolmayan kısım için yalnız kapanış fiyatından emir girilebilir; karşıda satıcı bekliyorsa dolar.
6. **3. işlem günü:** kapanış seansında sat. Pozisyondayken yeni sinyal gelirse sat-al yapma; çıkışı son sinyalden 3 gün sonraya ertele.

### 2.3 Sepet nasıl kurulur

- **Doğrulanan sürüm:** tavanda kapanmayan bütün elektrik hisseleri (bugün 40), eşit tutar. Elle 40 emir zor.
- **Küçültme:** rastgele 12 hisse almak ortalamayı değiştirmiyor, oynaklığı az artırıyor. 3–5 hisseyle sonuç şansa kalıyor.
- **En likit hisselere daraltma.** En likit 5 hissede etki yarıdan aza iniyor; AKSEN/ENJSA/ODAS üçlüsünde yok.
- **Pratik seçenek (sonradan türetildi, doğrulanmadı):** 60 günlük hacim sırasında 6.–20. olan 15 hisse. Bugün: AHGAZ, ODAS, CANTE, METEN, HUNER, AKFYE, MASFN, BESTE, VEYAS, SMRTG, IZENR, ZOREN, MOGAN, BIOEN, KLYPV. Sıra değişir; güncel listeyi `araclar/sinyal.py` verir.
- **Büyüklük:** 100 bin TL'lik sepet sorunsuz. Tam sepette yaklaşık 610 bin TL'nin üstünde küçük hisselerde kapanış seansı hacminin %10'u aşılıyor (hacim tahmini dolaylıdır).
- **Fon kullanılamaz:** XELKT'yi izleyen yatırım fonunda (TEFAS kodu GNS) emirler 13:30'a kadar veriliyor ve sonraki günlerin fiyatıyla gerçekleşiyor; 1–3 günlük işleme uymuyor.

### 2.4 Yapma listesi

- Sektör sinyaliyle yalnız AKSEN, ENJSA ya da ODAS alma: 2023 sonrasında fazla getiri +16 bps (t 0,5), kasada eksi.
- Alımı vadelide yapma: vadeli, 3 günde spotun 48–54 bps gerisinde kalıyor (taşıma maliyeti günde 14–15 bps). ODAS'ta tek fiyat adımı 23 bps.
- VİOP'ta bu çalışmadaki hiçbir satış kuralını uygulama: hiçbiri doğrulanmadı.
- "Bugün geride kalan yarın yetişir" diye alma: tersi doğru, geride kalan geride kalmaya devam ediyor.
- "Bir hisse tavan yaptı, benzerini alayım" deme: etki yok (+10 bps, maliyet sonrası eksi).
- Sinyali kaçırıp ertesi gün kapanışta girme: fazla getiri 78'den 46'ya düşüyor (t 1,3).
- 1 günlük tutmayla al-sat yapma: hiçbir sinyalde maliyeti geçmiyor.

### 2.5 Boyut, risk ve beklenti

- **Beklenti (S1, 2023 sonrası):** işlem başına ham ortalama +74 bps, medyan +62, işlemlerin %59'u artıda. Maliyet sonrası yaklaşık +40; faiz de düşülünce sıfıra yakın.
- **Kötü sonuçlar:** olayların en kötü %5'i −%4 ve altı; en kötü olay −%8,9 (17.03.2025). S2'de en kötü −%10,4 (20.10.2026). Art arda 7 zararlı sinyal günü görüldü.
- **Taban kilidi:** işlemlerin yaklaşık %1'inde çıkış günü hisse tabanda kilitliydi ve ortalama kayıp %15 oldu. Sepeti dar tutmamak için asıl neden bu.
- **Boyut örneği:** kötü bir olayda (en kötü %5) toplam sermayenin en çok %1'ini kaybetmek istiyorsan pozisyon sermayenin dörtte birini geçmemeli.
- XU030 vadelisiyle koruma önerilmez: oynaklığı yalnız %16 azaltıyor, bir kontrat yaklaşık 149 bin TL.

### 2.6 Gerçek paradan önce

- En az 10 sinyal dalgası (yaklaşık bir yıl) ya da 20 işlem boyunca kâğıt üstünde izle. Her işlemde üç şeyi yaz: ham getiri, kendi komisyonun, aynı günlerde nakdin getirisi.
- **Vazgeçme ölçütü:** 20 işlem sonunda komisyon ve faiz sonrası ortalama eksiyse bırak.
- **Senin komisyonun belirleyici.** Hesaplar gidiş-dönüş 25 bps komisyon ve yarım fiyat adımı varsayıyor. Banka tarifesiyle (gidiş-dönüş 50 bps ve üstü) S1 ve S2'de geriye bir şey kalmıyor.

### 2.7 Araçlar (`araclar/` klasörü)

- `sinyal.py`: her akşam çalıştırılır; sinyalleri, yarının tetik düzeylerini, sepet ve kaçınma listesini yazar. 17:50'de endeks değerini elle girip sinyali önceden hesaplama seçeneği var. Son 400 işlem gününde araştırma koduyla birebir aynı sonucu verdi.
- `elektrik_sinyal.pine`: `BIST:XELKT` günlük grafiğine eklenen gösterge (S1, S2, S3 işaretleri, alarm, yarının tetik çizgisi). `hisse_sektor_fark.pine`: hisse grafiğinde kaçınma işareti.
- **Uyarı:** Pine kodları TradingView'da derlenip denenmedi. İlk kullanımda işaretleri `sinyal.py` çıktısıyla karşılaştır (beklenen son sinyaller: S2 12.11, S1 13.11 ve 16.11).
- `izleme_listesi.txt`: TradingView'a içe aktarılacak liste (3 endeks, 4 vadeli, 42 hisse).
- Göstergedeki kaçınma işareti kıyas olarak XELKT'yi kullanır; araştırmadaki kıyas hisselerin eşit ağırlıklı ortalamasıdır. İkisi yarım puan ayrışabilir; eşiğe yakın günlerde `sinyal.py` listesi esastır.

## 3. Gerekçe ve kanıt

### 3.1 Nasıl sınandı

- **Veri:** 42 XELKT hissesi ve 4 komşu hisse, 2010 → 20.11.2026, İş Yatırım. VİOP bültenleri 2017'den, saatlik veri 2023 sonundan.
- **Üç dönem:** keşif (2010–2022), sınama (2023 → Haziran 2025), kasa (Temmuz 2025 → Kasım 2026). Kasa en sona kadar açılmadı.
- **Kör protokol:** yedi ayrı ekip sekiz sinyal ailesini yalnız keşif verisiyle taradı (yaklaşık 21 bin test) ve 41 kuralı kod olarak dondurdu. Sonraki dönemleri görmediler.
- **Giriş ve çıkış:** sinyal günü kapanışında giriş, 1–3 gün sonra kapanışta çıkış. Tavanda kapanan hisse alınamaz sayıldı; çıkış günü tabanda kilitli hisse satılamaz sayıldı.
- **Bağımsız denetim:** iki ekip sonuçları ortak kütüphaneyi kullanmadan ham veriden yeniden üretti; iki ekip de çürütmeye çalıştı.

### 3.2 Üç dönemde sonuç

Fazla getiri, bps, maliyet öncesi; parantez içinde t.

| Kural | 2010–2022 | 2023 → 2025/6 | Kasa | 2023 sonrası toplam |
|---|---|---|---|---|
| S1 Zirve → sepet | +44 (2,8) | +85 (1,8) | +86 (2,5) | +83 (2,8) |
| S2 Güçlü gün → sepet | +53 (3,2) | +53 (1,2) | +95 (2,3) | +70 (2,2) |
| S3 Piyasa önde → üçlü | +64 (2,4) | +221 (3,0) | +41 (0,8) | +157 (3,0) |
| S1, üçlüye uygulanırsa | +75 (3,8) | +44 (0,9) | −25 (−0,6) | +16 (0,5) |
| K Kaçınma (temiz kıyas) | −17 (−0,7) | −70 (−2,7) | −67 (−2,5) | −69 (−3,6) |

- S1 ve S2 kasada, önceden kayda geçirilen ölçüyle ve çoklu test düzeltmesiyle doğrulandı. S3 kasada tek başına yetersiz kaldı (14 olay).
- **Çöküş hisseleri etkisi:** kasa döneminde BIGEN 29, LYDYE 14, MAGEN 13 gün art arda tabanda kapandı. Bu üç hisse çıkarılınca S1 kasada +59 (t 1,7), 2023 sonrasında +67 (t 2,2); S2 +82 (t 2,1) ve +62 (t 2,0). Etki kaybolmuyor ama kasadaki büyüklüğün yaklaşık üçte biri buradan geliyordu.
- **Seçim yapılmadan bakıldığında:** keşifte artıda olan 40 kuralın %75'i 2023 sonrasında da artıda; ortalama etki 63 bps'den 30 bps'ye düştü. 41 kuralın 10'u hafif düzeltmeden, 3'ü en sıkı düzeltmeden geçti (S3, birleşik model ve "en kötü beşte birlik").

### 3.3 Kazanç gerçekte ne kadar

Sinyal günü alıp 3 gün tutan birinin eline geçen, bps:

| | Ham getiri | Maliyet | 3 günlük faiz | Kalan |
|---|---|---|---|---|
| S1, 2023 sonrası | +74 | 30–35 | 32–44 | yaklaşık +6 |
| S1, kasa | +48 | 30–35 | 32–44 | yaklaşık −18 |
| S2, 2023 sonrası | +63 | 30–35 | 32–44 | yaklaşık −4 |
| S2, kasa | +57 | 30–35 | 32–44 | yaklaşık −6 |
| S3, 2023 sonrası | +177 | 35 | 32–44 | yaklaşık +100 |
| S3, kasa | +86 | 35 | 32–44 | yaklaşık +13 |

- Faiz, paranın o 3 gün boyunca nakitte kazanacağı getiridir. Yıllık %27–37 varsayıldı; bu oran XU030 vadelisinin fiyat farkından türetildi ve başka bir kaynakla doğrulanmadı. Gerçek oran daha yüksekse S1 de ekside kalır.
- S3'teki "+100" yanıltıcı olabilir: 45 sinyal gününün en iyi 2'si (26.05.2023 ve 04.04.2024, seçim haftaları) çıkarılınca fazla getiri 157'den 106'ya, en iyi 10'u çıkarılınca 25'e düşüyor.

### 3.4 Yıllara göre ham getiri

Sinyal günü kapanışta alıp 3 gün tutmanın ortalama ham getirisi, bps, maliyet öncesi:

| Yıl | S1 | S2 | S3 | Sıradan gün (sepet) |
|---|---|---|---|---|
| 2023 | +168 | +110 | +193 | +2 |
| 2024 | +99 | +10 | +209 | +27 |
| 2025 | +39 | +86 | +224 | +18 |
| 2026 | +7 | +38 | +70 | −68 |

- Göreli üstünlük her yıl var; mutlak kâr yok. Sektörün düştüğü 2026'da S1 sıradan günden 75 bps iyi, ama ham getirisi +7.
- Nakde göre yıllık sonuç (S1, yaklaşık hesap): 2023 +16 puan, 2024 −1,5, 2025 +2,8, 2026 −7. S2: −3,5, −11, +11,4, −5,2.

### 3.5 Çürütme turunun bulguları

- **Kazanç birkaç dalgada.** S1'de 2023 sonrasındaki 40 yükseliş dalgasının 18'i artıda; en iyi 3 dalga fazla getirinin %83'ü. Onlar çıkınca +19 bps kalıyor.
- **Kazanç sağ kuyruktan.** Sonraki 3 günde tavan yapan işlemler (işlemlerin %5,7'si) fazla getirinin %91'ini taşıyor. Sepeti geniş tutmanın nedeni bu: o hisseleri önceden seçemezsin.
- **Elektriğe özgü değil.** Aynı devam etkisi sanayi endeksinde de var (+72, t 3,0), XU030'da yok (−5). Orta ve küçük hisselere özgü bir olgu.
- **S3 gecikme değil, piyasa momentumu.** 2023 sonrasında "XELKT geride" koşulu olmadan da aynı sonuç çıkıyor (+98, t 2,7). XU030'a karşı korunmuş hâli kasada +11 (t 0,2).
- **Çürütülemeyenler:** etki en likit üçte birlikte de var (+66); ertesi sabah açılıştan girişte de sürüyor (+64); parametreye duyarlı değil (zirve penceresi 10–60 gün arasında +78…+96); aylık trend yapaylığı değil.

### 3.6 Çalışmayanlar

| Aile | Ne sınandı | Sonuç |
|---|---|---|
| Hisse → hisse | 420 sıralı çift | Düzeltmeden geçen tek bağ AYEN → ZOREN; dönemin iki yarısında tekrarlanan bağ yok. Aynı gruptaki hisselerde (NATEN–ESEN–MAGEN, ODAS–CANTE) de yok |
| XU030 → sektör | Ertesi gün gecikme | Yok (katsayı −0,05, t −1,6) |
| Geride kalan yetişir mi | Sert yükseliş günü hareket etmeyen hisse | +10 bps, maliyet sonrası −22 |
| Büyük → küçük | Likit hisseler sığ hisseleri öncüler mi | Yok (katsayı 0,04, t 1,1) |
| Tavan bulaşması | Bir hisse tavan yaptı, diğerleri | +10 bps (t 1,0); bulaşma değil sektör momentumu |
| Tavana değip kapanamayan | Ertesi gün düşer mi | Keşifte ve sınamada evet; kasada −37 (t −0,7), doğrulanmadı |
| VİOP baz, hacim, açık pozisyon | Vadeli tarafındaki bilgi | Kullanılabilir sinyal yok |
| VİOP satış kuralları | 6 kural | Vadeli fiyatıyla hiçbiri anlamlı değil (t −0,7 … +1,0) |
| Birleşik model | Makine öğrenmesiyle sıralama | Sıralama gücü gerçek ama küçük: temiz kıyasla günde +13…+22 bps, maliyetin altında |
| Sade seçim kuralı | "Sakin ve güçlü hisse" | Kasada temiz kıyasla +10 (t 1,6): doğrulanmadı; işe yarayan tek parçası düşük oynaklık |

### 3.7 Karar anı ve dolum

- 17:50'de karar verenin getiri kaybı küçük: S1'de −3 bps, S2'de −6 bps (2017 sonrası). Eşiğe tampon eklemek gerekmiyor.
- S3'te 18:00 değeriyle bile getiri 157'den 90'a düşüyor (2023 sonrası); kaçan günler en iyi günler.
- Sinyal günü sepet hisselerinin %4–6'sı tavanda kapanıyor ve alınamıyor; bunların dörtte biri 17:30'dan sonra tavana kilitleniyor.
- 17:50–17:59'da sürekli işlemde almanın kapanış seansına göre ortalama fiyat üstünlüğü yok.

### 3.8 Düzeltilen varsayımlar

- **Öncülük varsayımı:** elektrik hisseleri arasında ve BIST 30 ile sektör arasında günlük ufukta işlenebilir bir öncülük ilişkisi bulunmadı. Bulunan şey sektörün (ve genel olarak orta-küçük hisselerin) kendi momentumu.
- **VİOP ile uygulama:** XELKT'nin vadelisi yok. Elektrik hisselerinden yalnız AKSEN, ENJSA ve ODAS'ın pay vadelisi var. Pay vadelileri 18:10'da kapanır ve akşam seansında işlem görmez. Vadelide alım taşıma maliyeti yüzünden spottan kötü.
- **Önceki çalışmamdaki ölçü:** hisselerin "olağan getirisi"ni son 250 günün ortalamasıyla ölçmek 2022 rallisinden sonra yanlı çıktı ("her gün al" bile −54 bps görünüyordu). Dönem içi ortalamaya göre ölçen kıyasa geçildi; iki tablo da ekte duruyor.

## 4. Emin olunmayanlar ve doğrulama kapsamı

**Doğrulananlar**
- **Hesaplar:** altı kural (S1, S2, S3, sade seçim, iki kaçınma kuralı) ham İş Yatırım verisinden bağımsız kodla yeniden üretildi. İşaret farkı yok; en büyük fark kasada 8 bps. Sinyal tarihleri S1 ve S3'te %100, S2'de %99,5 örtüşüyor.
- **Piyasa kuralları:** 17 iddia Borsa İstanbul'un güncel prosedürlerinden (Pay Piyasası rev. 54, VİOP rev. 70) kontrol edildi; 17'si doğrulandı, düzeltilen yok.
- **Endeks, fon ve literatür:** 15 iddia kontrol edildi; 15'i doğrulandı. Dört akademik kaynak yalnız özetinden görüldü.
- **TradingView kodları:** 57 kodun 57'sinin sayfası açılıyor.
- **Araç:** `sinyal.py` son 400 işlem gününde araştırma koduyla birebir aynı.
- **Çürütme:** iki ekip; bulguları 3.5'te ve hükümlere işlendi.

**Protokolden sapmalar**
- Kıyas ölçüsü sınama sonuçları görüldükten sonra değiştirildi (gerekçesi 3.8'de). Kasa bu değişiklikten sonra açıldı.
- Sade seçim kuralı ve "en kötü beşte birlik" kasada önceden kayıtlı ölçüyle "doğrulandı" çıkmıştı; yeniden üretim, kıyasın çöküş hisseleriyle kirlendiğini gösterdi ve ikisi geri çekildi.
- 15 hisselik sepet, "sinyal sürdükçe tut" ve S1 ile S2'nin birlikteliği sonradan türetildi; doğrulanmış kural değildir.

**Bilinen sınırlar**
- **Komisyon varsayımdır.** Aracı kurum komisyonları ve asgari komisyon birincil kaynaktan doğrulanmadı.
- **Faiz oranı varsayımdır** (3.3).
- **Kapanış seansı derinliği ölçülemedi.** Hacim payı (günlük hacmin yaklaşık %2,5–4,5'i) dolaylı tahmindir. Kırk emrin dört dakikada elle girilip girilemeyeceği sınanmadı.
- **Tedbirli hisseler:** brüt takas gibi tedbirler altındaki hisselerde 1 günlük çıkış yapılamayabilir; tedbir tarihleri veride yok.
- **Evren bugünkü 42 üyeden oluşuyor.** Son üç yılda endeksten çıkan hisse bulunmadı ama resmi kaynaktan kesinleştirilmedi.
- **Hisselerde gerçek 17:50 fiyatı** yalnız son 60 gün için var; öncesi 17:30 fiyatıyla ölçüldü.
- **Kütüphane sapması:** çıkış kaydırması 5 günle sınırlı (yöntem "ilk kilitsiz kapanış" diyordu). Momentum rakamlarını 7–8 bps temkinli tarafa çekiyor.
- **Veri kaynağı:** İş Yatırım'ın günlük endeks servisi son gün için tutarsız değer döndürebiliyor; betik saatlik seriyle düzeltiyor.
- **Keşif dönemi dar:** 2019'a kadar yalnız yaklaşık 10 elektrik hissesi işlem görüyordu. 2015 sonu öncesindeki tavan/taban bayrakları güvenilmez.

## 5. Kaynaklar

- Borsa İstanbul, Pay Piyasası Prosedürü (rev. 54, 21.09.2026): https://borsaistanbul.com/files/pay-piyasasi-proseduru.pdf
- Borsa İstanbul, VİOP Prosedürü (rev. 70, 01.07.2026): https://borsaistanbul.com/files/borsa-istanbul-as-vadeli-islem-ve-opsiyon-piyasasi-proseduru.pdf
- Borsa İstanbul, Pay Piyasası işleyişi: https://borsaistanbul.com/piyasalar/pay-piyasasi/piyasa-isleyisi
- Borsa İstanbul, VİOP dayanak varlıklar: https://borsaistanbul.com/piyasalar/viop/sozlesme-ozellikleri/dayanak-varliklar
- Borsa İstanbul, pay endeksleri kural seti (Ekim 2026): https://www.borsaistanbul.com/files/bist-pd-agirlikli-pay-endeksleri-ks-tr-2026-ekim-temiz.pdf
- Borsa İstanbul, VİOP günlük bülteni (örnek gün; her iş günü için ayrı dosya): https://www.borsaistanbul.com/data/vadeli/viop_20261119.csv
- KAP, endeks üyeleri: https://www.kap.org.tr/tr/Endeksler
- KAP, GNS fonu: https://kap.org.tr/tr/fon-bilgileri/genel/gns-garanti-portfoy-enerji-sirketleri-hisse-senedi-tl-fonu-hisse-senedi-yogun-fon
- İş Yatırım, hisse ve endeks verisi: https://www.isyatirim.com.tr
- TradingView, XELKT: https://www.tradingview.com/symbols/BIST-XELKT/
- Hou (2007), sektör içi bilgi yayılımı: https://econpapers.repec.org/RePEc:oup:rfinst:v:20:y:2007:i:4:p:1113-1138
- DeMiguel, Nogales, Uppal (2014), işlem maliyeti eşiği: https://lbsresearch.london.edu/id/eprint/4
- Chen ve ark., Çin'de tavan sonrası devam: https://www.nber.org/papers/w24014.pdf

**Ek dosyalar** (bu klasörde):
- `YONTEM.md`, `ek/YONTEM_EK.md`: yöntem ve hesaptan önce yazılan kurallar.
- `ek/oos1_sonuc.csv`, `ek/oos1_sonuc_donem_notr.csv`, `ek/kasa_sonuc.csv`, `ek/tum_oos_sonuc.csv`: sonuç tabloları.
- `ek/v1_…` – `ek/v7_…`: yeniden üretim, çürütme, sepet, zamanlama ve araç notları.
- `ek/a1_…` – `ek/a8_…`, `ek/w3a_…` – `ek/w3c_…`: sinyal ailelerinin notları ve tabloları.
- `ek/dogrulama_piyasa_kurallari.md`, `ek/dogrulama_xelkt_literatur.md`: kaynak doğrulaması.
- `kod/`: bütün kod; `araclar/`: günlük kullanım araçları.

## 6. Devam notu

- **Bulunan:** elektrik hisselerinde işlenebilir öncülük yok; sektör momentumu (S1, S2) istatistiksel olarak üç dönemde de var ama maliyet ve faiz sonrası sıfıra yakın; S3 piyasa momentumu ve kuyruğa bağımlı; kaçınma kuralı sağlam; VİOP satış sinyali yok.
- **Dosyalar:** bu rapor, `ek/kasa_sonuc.csv`, `ek/tum_oos_sonuc.csv`, `ek/v3_curutme_momentum.md`, `ek/v5_sepet.md`, `araclar/sinyal.py`.
- **Veri depoda yok** (yeniden indirilebilir): `kod/d1_veri/run.sh` ve `kod/d2_veri/run.sh`; paneller `kod/ortak/elib.py` ile okunur.
- **Açık işler:** Pine kodlarını TradingView'da derleyip denemek; kendi komisyonunla ve gerçek TL faiziyle 3.3'ü yeniden hesaplamak; kapanış seansı dolumunu küçük tutarla denemek.
- **İleriye dönük sınama:** 21.11.2026 sonrasındaki her S1, S2, S3 günü yeni veridir; `sinyal.py --gecmis` ile kayıt tutulabilir.

*Maliyet özeti: Seviye L+ · 28 Fable alt ajan (1. dalga 6, 2. dalga 8, kasa öncesi 3, doğrulama ve uygulama 7, kaynak doğrulayıcı 2, eleştirmen 2) + 7. dakikada durdurulan 2 sonnet · 3 üretim dalgası + doğrulama · kontrol noktasını geçenler: literatür ve piyasa kuralları araştırmacıları (51/35; eksik sayı ve tarihleri tamamlamak için), VİOP veri ajanı (41/40) · model ataması kullanıcı isteğiyle protokolden farklı (bütün alt ajanlar Fable).*
