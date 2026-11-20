# BIST elektrik hisselerinde 1–3 günlük öncülük sinyalleri

*20.11.2026 · Seviye L+ · Yatırım tavsiyesi değildir. Bütün rakamlar geçmiş veriye dayanır.*

**Sözlük**
- **bps** = baz puan, %0,01 (100 bps = %1).
- **t** = etkinin kendi belirsizliğine oranı; kabaca 2'nin üstü "şans olma olasılığı düşük" demektir.
- **XELKT** = BIST Elektrik endeksi (42 hisse). **Üçlü** = AKSEN, ENJSA, ODAS (VİOP'ta pay vadelisi olan elektrik hisseleri). **Spot** = hissenin kendisi (vadeli değil).
- **Sepet** = o gün alınabilir durumdaki elektrik hisseleri, eşit tutarla.
- **Tavan / taban** = bir hissenin gün içinde en çok ±%10 oynayabilmesi. Tavanda kapanan hisse alınamaz, tabanda kapanan satılamaz sayıldı.
- **Ham getiri** = pozisyonun kendi getirisi. **Fazla getiri** = sinyal günleri ile aynı dönemin sıradan günleri arasındaki fark.
- **Dalga** = art arda gelen sinyal günleri. **Gidiş-dönüş** = alış ve satış birlikte. **Medyan** = ortadaki değer.
- **Kasa** = en sona kadar hiç bakılmayan son dönem (Temmuz 2025 → Kasım 2026); bir kuralın gerçek sınavı.
- **Adım** = fiyatın oynayabileceği en küçük miktar (20 TL altında 1 kuruş, 20–50 TL arasında 2 kuruş).

## 1. Kısa yanıt

- **Net öneri:** bu sinyallerle şimdilik gerçek parayla işlem yapma; kâğıt üstünde izle. Elektrik hissesini zaten başka bir nedenle alacaksan alımı aşağıdaki S1 gününe denk getir ve kaçınma kuralına uy.
- Aradığın türden öncülük ("X bugün hareket etti, Y yarın izler") **yok**: hisse çiftleri, XU030 → sektör, büyük → küçük ve VİOP baz/hacim sinyalleri sınandı; kalıcı ve maliyeti aşan bağ çıkmadı.
- Var olan şey **momentum**: XELKT 20 günlük zirve yaptığı ya da sert yükseldiği gün alınan sepet 3 günde ortalama %0,65–0,75 kazandırdı; bu, sıradan günlerden %0,7–0,8 fazla.
- Bu kâra dönüşmüyor: komisyon ve fiyat farkı %0,30–0,35, aynı paranın 3 günlük faizi %0,32–0,44. Elde kalan yaklaşık sıfır ve kazanç birkaç yükseliş dalgasından geliyor.
- AKSEN, ENJSA, ODAS'ta sektör sinyali çalışmıyor. Doğrulanan VİOP satış sinyali yok. Alım yapılacaksa vadelide değil spotta.
- Tek hisse seçen için işe yarar bir kaçınma kuralı var: o gün tabana değmiş ya da sektörün 5 puan gerisinde kapanmış hisse kapanışta alınmaz.

## 2. Ne yapmalıyım

Bu bölüm "nasıl yapılır" tarifidir; "yap" demek değildir. Sırası: (a) hisseyi zaten alacaksan zamanlama ve kaçınma için kullan, (b) sinyalin kendisiyle işlem yapmak istiyorsan önce 2.6'daki gibi kâğıt üstünde izle, (c) komisyonun gidiş-dönüş %0,25'ten yüksekse hiç başlama.

### 2.1 Sinyaller ve TradingView kodları

**S1 Zirve**
- Koşul: `BIST:XELKT` kapanışı son 20 işlem gününün en yüksek kapanışı.
- Hedef: sepet, 3 işlem günü.
- Güven: istatistiksel etki orta, kâr yok. Yalnız zamanlama süzgeci.

**S2 Güçlü gün**
- Koşul: `BIST:XELKT` günlük artışı, önceki 60 günün günlük oynaklığına eşit ya da büyük (bugün %2,1).
- Hedef: sepet, 3 işlem günü.
- Güven: düşük. S1 olmayan günlerde etkisi zayıf (+35 bps, t 0,9).

**S3 Piyasa güçlü günü (yalnız izleme)**
- Koşul: `BIST:XU030` artışı kendi 60 günlük oynaklığına eşit ya da büyük (bugün %1,9) **ve** XELKT artışı kendi oynaklığının yarısından az (bugün %1,05'ten az).
- İzlenecek: `BIST:AKSEN`, `BIST:ENJSA`, `BIST:ODAS` spot, 3 işlem günü. Şimdilik alma; kâğıt üstünde kaydet.
- Güven: düşük. Ad yanıltmasın: bu bir öncülük değil, piyasanın güçlü gününden sonraki genel devam etkisi.

**K Kaçınma**
- Koşul: hisse o gün tabana değdi ya da sektör ortalamasının 5 puan ve daha fazla gerisinde kapandı.
- Ne yapılır: o hisse o gün alınmaz (1 günlük).
- Güven: orta. Tek hisse seçen için işe yarar; sepete katkısı küçüktür.

Notlar:
- "Oynaklık" = günlük getirilerin standart sapması. Göstergede **z** olarak görünür: günlük getiri ÷ oynaklık. S2 "z en az 1" demektir.
- S1/S2 günü üçlüyü tek başına alma (çalışmıyor). S3 ayrı bir şeydir ve yalnız izlenir.
- Seçim yapacaksan oynaklığı düşük hisseyi yeğle; etki küçük (günde %0,05–0,12).
- Vadeli kodları (`BIST:AKSEN1!`, `BIST:ENJSA1!`, `BIST:ODAS1!`, `BIST:XU030D1!`) yalnız izleme içindir.

**Bugünkü durum (20.11.2026 kapanışı):** üç sinyal de yok. XELKT 537,06, XU030 13.957,13. Bir sonraki işlem günü için tetikler: S1 XELKT 571,59 ve üstü; S2 XELKT 548,31 ve üstü; S3 XU030 14.220,17 ve üstü, XELKT 542,68'in altı. Kaçınma listesinde MAGEN var. Bugün XELKT sert düştü (z −1,1); böyle günlerden sonra sepet 2023 sonrasında ertesi gün ortalama −48 bps getirdi (kasada −109). Bu doğrulanmış bir kural değil, ama bugün alım için bir neden de yok.

### 2.2 Günlük akış

1. **Bir gece önce:** yarının tetik düzeylerini not al (yukarıdaki gibi; `sinyal.py` yazar). İstersen bu düzeye TradingView'da fiyat alarmı kur.
2. **17:30, hisseler (elle):** TradingView izleme listesini "Değişim %" sütununa göre sırala.
   - XELKT'nin günlük yüzdesinden 5 puan çıkar (XELKT −%1 ise sınır −%6); bunun altındaki hisseyi alma.
   - Günün en düşüğü −%10'a inmiş hisseyi alma.
   - +%7'nin üstündeki hisseyi alma (tavanda kapanma olasılığı yüksek).
   - Hisse başına tutarı ve adedi (tutar ÷ fiyat, aşağı yuvarla) şimdi hazırla.
3. **17:50, endeks:** XELKT'yi tetik düzeyiyle kıyasla. 17:50 değeri kapanış sinyalinin S1'de %95'ini, S2'de %87'sini yakalıyor.
4. **17:55–18:00:** eşiğe çok yakınsa (S1: zirvenin ±%0,15'i; S2: z 0,9–1,1 arası) 18:00 değerini bekle. S3'e yalnız 18:00'de bak; 17:00'de sinyalin ancak yarısı görünüyor.
5. **18:01–18:04, emir:** kapanış seansına limit ya da piyasa emri gir.
   - Kapanış seansında herkes aynı fiyattan (18:05'te belirlenen kapanış fiyatı) işlem yapar. Yazdığın limit ödeyeceğin fiyat değil, razı olduğun en yüksek fiyattır; son fiyatın 1–2 adım üstünü yaz.
   - Limit kapanış fiyatının altında kalırsa emir dolmaz; piyasa emri karşılık bulamazsa iptal edilir. Emir fiyatı son işlem fiyatının %3'ünden uzak olamaz.
6. **18:08–18:10:** dolmayan kısım için yalnız kapanış fiyatından emir girilebilir; karşıda satıcı bekliyorsa dolar.
7. **Çıkış:** sinyal günü 0 sayılır; 3. işlem günü kapanış seansında sat (pazartesi sinyal → perşembe; perşembe sinyal → salı).
   - Pozisyondayken gelen yeni sinyali yok say.
   - Çıkış günü hisse tabanda kilitliyse satış emrini her gün kapanış seansında yinele.
8. **Yapma:** resmî tatil öncesi yarım günlerde işlem yapma; saatler farklı ve araçlar o günlerde sınanmadı.

Uyarılar:
- TradingView'da gerçek zamanlı BIST paketin yoksa veri 15 dakika gecikmelidir; 17:50 değerini aracı kurum uygulamasından oku.
- Göstergenin "çubuk kapanışında" çalan alarmı kapanış seansından sonra gelir; işlem için geç kalır, yalnız kayıt tutmaya yarar.

### 2.3 Sepet nasıl kurulur

- **Doğrulanan sürüm:** tavanda kapanmayan bütün elektrik hisseleri (bugün 40), eşit tutar.
- **Emir sayısı:** dört dakikada elle 40 emir girilemez. Aracı kurumunda "sepet" ya da "toplu emir" varsa onu kullan; yoksa 12–15 hisseyle sınırla.
- **Küçültme:** rastgele 12 hisse almak ortalamayı değiştirmiyor, oynaklığı az artırıyor. 3–5 hisseyle sonuç şansa kalıyor.
- **En likit 5 hisseyle yetinme:** etki yarıdan aza iniyor; üçlüde yok.
- **Pratik seçenek (sonradan türetildi, doğrulanmadı):** `sinyal.py` sepet tablosunun 6.–20. satırları. Bugün: AHGAZ, ODAS, CANTE, METEN, HUNER, MASFN, AKFYE, BESTE, IZENR, SMRTG, VEYAS, ZOREN, BIOEN, MOGAN, TATEN. Sıra değişir.
- **Adımı kaba hisseyi çıkar:** tablodaki "adım" sütunu 50'nin üstündeyse (bugün CANTE ve ZOREN) fiyatın tek adım oynaması %0,5–1 demektir; çıkarıp sıradakini al.
- ODAS burada sepetin 15'te biri olarak yer alır; tek başına alınmaz.
- **Büyüklük:** 100 bin TL'de kapanış seansı hacmi sorun değil; hisse başına 2.381 TL düştüğü için LYDYE (2.902 TL) alınamaz. Tam sepette yaklaşık 610 bin TL'nin üstünde küçük hisselerde kapanış seansı hacminin %10'u aşılıyor (hacim tahmini dolaylıdır).
- **Aracı kurumuna sor:** emir başına asgari komisyon var mı? Varsa hisse başına tutar küçüldükçe maliyet varsayımı bozulur.
- **Fon kullanılamaz:** XELKT'yi izleyen yatırım fonunda (TEFAS kodu GNS) emirler 13:30'a kadar veriliyor ve sonraki günlerin fiyatıyla gerçekleşiyor.

### 2.4 Yapma listesi

- Sektör sinyaliyle yalnız AKSEN, ENJSA ya da ODAS alma: 2023 sonrasında fazla getiri +16 bps (t 0,5), kasada eksi.
- Alımı vadelide yapma: vadeli, 3 günde spotun 48–54 bps gerisinde kalıyor (taşıma maliyeti günde 14–15 bps). ODAS'ta tek fiyat adımı 23 bps.
- VİOP'ta bu çalışmadaki hiçbir satış kuralını uygulama: hiçbiri doğrulanmadı.
- "Bugün geride kalan yarın yetişir" diye alma: yetişme yok; sert geride kalanlar (taban, 5 puan) ertesi gün de zayıf.
- "Bir hisse tavan yaptı, benzerini alayım" deme: etki yok (+10 bps, maliyet sonrası eksi).
- Sinyali kaçırıp ertesi gün kapanışta girme: fazla getiri aynı ölçüyle 78'den 46'ya düşüyor (t 1,3).
- 1 günlük tutmayla al-sat yapma: hiçbir sinyalde maliyeti geçmiyor.
- "Sinyal sürdükçe tut" deme: bakıldı; giriş sayısı azalıyor ama girişlerin %55–58'i zararla kapanıyor, medyan −44 bps. Önerilmez.

### 2.5 Beklenti ve risk

- **Beklenti (S1, 2023 sonrası, 82 örtüşmeyen işlem):** ham ortalama +73 bps, medyan +62; işlemlerin %59'u artıda (maliyet sonrası %57).
- **Kötü sonuçlar:** olayların en kötü %5'i −%4 ve altı; en kötü olay −%8,9 (17.03.2025). S2'de en kötü −%10,4 (20.10.2026). Art arda 7 zararlı sinyal günü görüldü.
- **TL karşılığı:** 100 bin TL'lik pozisyonda her 20 işlemden birinde 4 bin TL ve üstü, görülen en kötü olayda 8.900 TL (S2'de 10.400 TL) kayıp.
- **Taban kilidi:** işlemlerin yaklaşık %1'inde çıkış günü hisse tabanda kilitliydi; ortalama kayıp %15. Kasa döneminde durum ağırlaştı: her dört sinyal gününün birinde sepette çıkışı kilitli en az bir hisse vardı; bu işlemlerin ortalama kaybı %21, en kötüsü %32. Sepeti dar tutmamanın asıl nedeni bu.
- **Zarar-kes:** sınama zarar-kes emri olmadan yapıldı; kullanırsan bu rakamlar geçerli olmaz. Taban günü zarar-kes emri de dolmaz.
- **Boyut örneği:** kötü bir olayda (en kötü %5) toplam sermayenin en çok %1'ini kaybetmek istiyorsan pozisyon sermayenin dörtte birini geçmemeli.
- XU030 vadelisiyle koruma önerilmez: oynaklığı yalnız %16 azaltıyor, bir kontrat yaklaşık 149 bin TL.

### 2.6 Gerçek paradan önce

- Kâğıt üstü izlemenin amacı stratejiyi kanıtlamak değil; kendi maliyetini ve emirlerin dolup dolmadığını görmek. 20 işlem, kazancın gerçek olup olmadığını ayırt etmeye yetmez (ortalamadaki belirsizlik yaklaşık ±%1,4).
- Her işlemde üç şeyi yaz: ham getiri, gerçekleşen maliyet (komisyon ve fiyat farkı), emirlerin kaçının dolduğu.
- **Bırakma ölçütü:** gerçekleşen maliyet işlem başına %0,35'i aşıyorsa ya da emirlerin beşte biri dolmuyorsa bırak.
- **Senin komisyonun belirleyici.** Hesaplar gidiş-dönüş 25 bps komisyon ve yarım fiyat adımı varsayıyor. Banka tarifesiyle (gidiş-dönüş 50 bps ve üstü) S1 ve S2'de geriye bir şey kalmıyor.

### 2.7 Araçlar (`araclar/` klasörü)

- `sinyal.py`: her akşam çalıştırılır; sinyalleri, yarının tetik düzeylerini, sepet ve kaçınma listesini yazar. Son 400 işlem gününde araştırma koduyla birebir aynı sonucu verdi. Hisse listeleri ancak 18:10'dan sonra kesinleşir; o liste kayıt içindir, 17:30 kontrolünü elle yaparsın.
- Çıktıdaki "günün en kötü beşte birliği" satırı ve "T2 sakin ve güçlü" listesi kural değildir; dikkate alma.
- `elektrik_sinyal.pine`: `BIST:XELKT` günlük grafiğine eklenen gösterge (S1, S2, S3 işaretleri, yarının tetik çizgisi). `hisse_sektor_fark.pine`: hisse grafiğinde kaçınma işareti.
- **Uyarı:** Pine kodları TradingView'da derlenip denenmedi. İlk kullanımda işaretleri `sinyal.py --gecmis 20` çıktısıyla karşılaştır (beklenen son sinyaller: S2 12.11, S1 13.11 ve 16.11).
- Göstergedeki kaçınma işareti kıyas olarak XELKT'yi kullanır; araştırmadaki kıyas hisselerin eşit ağırlıklı ortalamasıdır. İkisi yarım puan ve daha fazla ayrışabilir.
- `izleme_listesi.txt`: TradingView'a içe aktarılacak liste (3 endeks, 4 vadeli, 42 hisse). `KULLANIM.md`: kurulum ve günlük akış.
- **Bilgisayarın yoksa:** S1 ve S2 için betik şart değil. S1 = XELKT kapanışı son 20 günün en yükseği (grafikte gözle görülür). S2 = XELKT'nin günlük artışı yaklaşık %2 ve üstü (kesin eşik bugün %2,1). Sepet ve kaçınma için TradingView izleme listesi yeter.

## 3. Gerekçe ve kanıt

### 3.1 Nasıl sınandı

- **Veri:** 42 XELKT hissesi ve 4 komşu hisse, 2010 → 20.11.2026, İş Yatırım. VİOP bültenleri 2017'den, saatlik veri 2023 sonundan.
- **Üç dönem:** keşif (2010–2022), sınama (2023 → Haziran 2025), kasa (Temmuz 2025 → Kasım 2026).
- **Kör protokol:** yedi ekip yedi sinyal ailesini yalnız keşif verisiyle taradı (yaklaşık 21 bin test) ve 41 kuralı kod olarak dondurdu (ikisi aynı kural, yani 40 ayrı kural). Sonraki dönemleri görmediler. Sekizinci ekip (gün içi zamanlama) kural dondurmadı.
- **Giriş ve çıkış:** sinyal günü kapanışında giriş, 1–3 gün sonra kapanışta çıkış.
- **Bağımsız denetim:** iki ekip sonuçları ortak kütüphaneyi kullanmadan ham veriden yeniden üretti; iki ekip çürütmeye çalıştı; iki eleştirmen bu raporu denetledi.

### 3.2 Üç dönemde sonuç

Fazla getiri, bps, maliyet öncesi; parantez içinde t. İlk üç satır 3 günlük, son satır 1 günlüktür.

| Kural | 2023 sonrası toplam | Kasa | 2023 → 2025/6 | 2010–2022 |
|---|---|---|---|---|
| S1 Zirve → sepet | +83 (2,8) | +86 (2,5) | +85 (1,8) | +44 (2,8) |
| S2 Güçlü gün → sepet | +70 (2,2) | +95 (2,3) | +53 (1,2) | +53 (3,2) |
| S3 → üçlü | +157 (3,0) | +41 (0,8) | +221 (3,0) | +64 (2,4) |
| S1, üçlüye uygulanırsa | +16 (0,5) | −25 (−0,6) | +44 (0,9) | +75 (3,8) |
| K, tabana değmeyenler | −69 (−3,6) | −67 (−2,5) | −70 (−2,7) | −17 (−0,7) |

- K satırında eksi sayı, kaçınılan hissenin ertesi gün sektörden o kadar kötü getirdiğini gösterir; eksi olması kuralın çalıştığı anlamına gelir. Bu etki 2010–2022'de yok. Göstergenin kullandığı XELKT kıyasıyla kasada −38 (t −1,5).
- Ara sütundaki rakamlar son panelden; kasa açılmadan önceki tabloda biraz farklıydı (S1 +87, S2 +52, S3 +209). İşaretler aynı.
- **S1 ve S2 kasada, önceden kayda geçirilen ölçüyle ve çoklu test düzeltmesiyle (Holm, alfa 0,10; on kural) geçti.** S3 kasada tek başına yetersiz kaldı (14 olay).
- **Bu sonuç sağlamlık sınamalarında zayıfladı:**
  - Kasa döneminde BIGEN 29, LYDYE 14, MAGEN 13 gün art arda tabanda kapandı. Bu üç hisse çıkarılınca S1 kasada 86 → 56 (t 1,6), S2 95 → 77 (t 2,0) oluyor ve aynı eşik geçilmiyor. S1'de büyüklüğün üçte biri, S2'de beşte biri bu hisselerin sıradan günlerdeki zararından geliyordu.
  - Sektörün ve piyasanın son haftalardaki yönü kontrol edilince S1'in kendi katkısı 2023 sonrasında +45 (t 1,2), kasada +20 (t 0,4): zirve koşulu, "sektör zaten yükseliyor" bilgisinin üstüne az şey ekliyor. S2'de +69 (t 2,2).
  - 2023 sonrasının tamamında S1 ve S2 yalnız hafif düzeltmeden geçti, en sıkısından geçmedi.
- **Seçim yapılmadan bakıldığında:** keşifte artıda olan 40 kuralın %75'i 2023 sonrasında da artıda; ortalama etki 63 bps'den 30 bps'ye düştü. Hafif düzeltmeden 9 ayrı kural, en sıkısından 3 kural geçti (S3, birleşik model, "en kötü beşte birlik"). Son ikisi yeniden üretimde zayıfladı (3.6).

### 3.3 Kazanç gerçekte ne kadar

Sinyal günü alıp 3 gün tutan birinin eline geçen, bps:

| | Ham getiri | Maliyet | 3 günlük faiz | Kalan |
|---|---|---|---|---|
| S1, 2023 sonrası | +75 | 30–35 | 32–44 | +2 … +6 |
| S1, kasa | +48 | 30–35 | 32–44 | −23 … −18 |
| S2, 2023 sonrası | +64 | 30–35 | 32–44 | −9 … −4 |
| S2, kasa | +59 | 30–35 | 32–44 | −11 … −6 |
| S3, 2023 sonrası | +177 | 35 | 32–44 | yaklaşık +100 (*) |
| S3, kasa | +86 | 35 | 32–44 | yaklaşık +13 (*) |

- **Faiz kalemi senin durumuna bağlı.** İşlem paran para piyasası fonunda ya da repoda duruyorsa faizi düş (kendi net oranınla). Para hesapta boş bekliyorsa bu kalem sıfırdır ve S1'de elde kalan yaklaşık %0,4 olur; yine de bu ortalama birkaç iyi dalgadan geliyor (3.5).
- Faiz yıllık %27–37 varsayıldı; bu oran XU030 vadelisinin fiyat farkından türetildi ve başka bir kaynakla doğrulanmadı.
- **(*) S3 satırları yanıltıcı olabilir:**
  - Rakamlar kapanış değeriyle kurulan sinyale ait. En erken 18:00'de karar verilebildiği için uygulanabilir sürümde fazla getiri 157'den 90'a (kasada 41'den 11'e) düşüyor; kalan yaklaşık +35, kasada yaklaşık −15 olur.
  - 45 sinyal gününün en iyi 2'si (26.05.2023 ve 04.04.2024, seçim haftaları) çıkarılınca fazla getiri 157'den 106'ya, en iyi 10'u çıkarılınca 25'e düşüyor.
  - Çürütme ekibinin beklentisi olay başına net 0 … +40 bps, yılda yaklaşık 10 olay.

### 3.4 Yıllara göre ham getiri

Sinyal günü kapanışta alıp 3 gün tutmanın ortalama ham getirisi, bps, maliyet öncesi:

| Yıl | S1 | S2 | S3 | Sıradan gün (sepet) |
|---|---|---|---|---|
| 2023 | +168 | +110 | +193 | +2 |
| 2024 | +99 | +10 | +209 | +27 |
| 2025 | +39 | +86 | +224 | +18 |
| 2026 | +7 | +38 | +70 | −68 |

- S1 her yıl sıradan günden iyi, ama fark yalnız 2023'te anlamlı (t 2,2; sonraki yıllarda t 0,5–1,4). S2 2024'te sıradan günün 18 bps altında kaldı.
- Sektörün düştüğü 2026'da S1 sıradan günden 75 bps iyi, ama ham getirisi yalnız +7.
- Nakde göre yıllık sonuç (yaklaşık hesap): S1 2023 +16 puan, 2024 −1,5, 2025 +2,8, 2026 −7. S2: −3,5, −11, +11,4, −5,2.

### 3.5 Çürütme turunun bulguları

- **Kazanç birkaç dalgada.** S1'de 2023 sonrasındaki 40 yükseliş dalgasının 18'i artıda; en iyi 3 dalga fazla getirinin %83'ü. Onlar çıkınca +19 bps kalıyor.
- **Kazanç sağ uçtan.** Sonraki 3 günde tavan yapan işlemler (işlemlerin %5,7'si) fazla getirinin %91'ini taşıyor. O hisseleri önceden seçemezsin; sepeti geniş tutmanın nedeni bu.
- **Elektriğe özgü değil.** Aynı devam etkisi sanayi endeksinde de var (+72, t 3,0), XU030'da yok (−5). Orta ve küçük hisselere özgü bir olgu.
- **S3 gecikme değil, piyasa momentumu.** 2023 sonrasında "XELKT geride" koşulu olmadan da üçlü +98 (t 2,7) getiriyor; koşulun ek katkısı anlamsız (kasada −6). XU030'a karşı korunmuş hâli kasada +11 (t 0,2).
- **S1 ve S2 aynı gün gelirse** geçmişte etki daha büyüktü (+125, 54 gün). Sonradan bakılan bir kesittir; ek sinyal sayılmaz.
- **Çürütülemeyenler:** etki en likit üçte birlikte de var (+66); ertesi sabah açılıştan girişte de sürüyor (+64); parametreye duyarlı değil (zirve penceresi 10–60 gün arasında +78 … +96).

### 3.6 Çalışmayanlar

- **Hisse → hisse (420 sıralı çift):** düzeltmeden geçen tek bağ AYEN → ZOREN; dönemin iki yarısında tekrarlanan bağ yok. Aynı gruptaki hisselerde (NATEN–ESEN–MAGEN, ODAS–CANTE) de yok.
- **XU030 → sektör:** ertesi gün gecikme yok (katsayı −0,05, t −1,6).
- **Geride kalan yetişir mi:** sert yükseliş günü hareket etmeyen hisse ertesi gün +10 bps, maliyet sonrası −22.
- **Büyük → küçük:** likit hisseler sığ hisseleri öncülemiyor (katsayı 0,04, t 1,1).
- **Tavan bulaşması:** bir hisse tavan yaptığında diğerleri +10 bps (t 1,0); bulaşma değil, sektör momentumu.
- **Tavana değip kapanamayan:** keşifte ve sınamada ertesi gün düşüyordu; kasada −37 (t −0,7), doğrulanmadı.
- **VİOP baz, hacim, açık pozisyon:** doğrulanmış sinyal yok. Bir baz kuralı (vadeli bazı yukarı sıçrayınca üçlüde spot alım, 3 gün) 2023 sonrasında +75 (t 2,1) verdi ama en sıkı düzeltmeden geçmedi ve kasada ayrıca sınanmadı; izleme.
- **VİOP satış kuralları (5 kural):** vadeli fiyatıyla hiçbiri anlamlı değil (t −0,7 … +1,0).
- **Birleşik model (makine öğrenmesi):** sıralama gücü gerçek ama küçük; temiz kıyasla günde +13 … +22 bps, maliyetin altında.
- **Sade seçim kuralı ("sakin ve güçlü hisse"):** kasada temiz kıyasla +10 (t 1,6), doğrulanmadı. İşe yarayan tek parçası düşük oynaklık.
- **"Günün en kötü beşte birliği":** tabanda kapananlar çıkarılınca kasada −3 (t −0,5); bağımsız bir bulgu değil, taban serilerinin gölgesi.

"Temiz kıyas": sektör ortalaması hesaplanırken tabanda kapanan hisselerin dışarıda bırakılması. Kasa döneminde çöküş serileri sektör ortalamasını günde 30 bps aşağı çektiği için ilk rakamlar şişkindi.

### 3.7 Karar anı ve dolum

- 17:50'de karar verenin getiri kaybı küçük: S1'de −3 bps, S2'de −6 bps (2017 sonrası); kasada −10 ve −12. Eşiğe tampon eklemek gerekmiyor.
- S3'te kaçan günler en iyi günler; bu yüzden 18:00 kararıyla getiri belirgin düşüyor (3.3).
- Sinyal günü sepet hisselerinin %4–6'sı tavanda kapanıyor ve alınamıyor; bunların dörtte biri 17:30'dan sonra tavana kilitleniyor.
- 17:50–17:59'da sürekli işlemde almanın kapanış seansına göre ortalama fiyat üstünlüğü yok.

### 3.8 Düzeltilen varsayımlar

- **Öncülük varsayımı:** elektrik hisseleri arasında ve BIST 30 ile sektör arasında günlük ufukta işlenebilir bir öncülük ilişkisi bulunmadı. Bulunan şey sektörün (ve genel olarak orta-küçük hisselerin) kendi momentumu.
- **VİOP ile uygulama:** XELKT'nin vadelisi yok. Elektrik üretim ve dağıtım şirketlerinden yalnız AKSEN, ENJSA ve ODAS'ın pay vadelisi var. Pay vadelileri 18:10'da kapanır ve akşam seansında işlem görmez. Vadelide alım, taşıma maliyeti yüzünden spottan kötü.
- **Ölçü düzeltmesi:** çalışmanın başında hisselerin "olağan getirisi" son 250 günün ortalamasıyla ölçülüyordu. Bu ölçü 2022 rallisinden sonra yanlı çıktı ("her gün al" bile 3 günde −54 bps görünüyordu) ve dönem içi ortalamaya göre ölçen kıyasa geçildi. İlk ölçüyle S1 ve S2 sınamada ve kasada anlamsızdı (t 0,1–0,7). Yani bulgu, ölçü düzeltmesinin doğru olduğu kabulüne dayanır; iki tablo da ekte duruyor.

## 4. Emin olunmayanlar ve doğrulama kapsamı

**Doğrulananlar**
- **Hesaplar:** altı kural (S1, S2, S3, sade seçim, iki kaçınma kuralı) ham İş Yatırım verisinden bağımsız kodla yeniden üretildi. İşaret farkı yok; en büyük fark kasada 8 bps. Sinyal tarihleri S1 ve S3'te %100, S2'de %99,5 örtüşüyor.
- **Rapordaki sayılar:** bir eleştirmen 1.–3. bölümlerdeki yaklaşık 257 sayıyı kaynak dosyalarla karşılaştırdı: 251 doğru, 5 küçük farkla yanlış, 1'inin kaynağı bulunamadı. Altısı da düzeltildi. Çıkarımla ilgili 13 itirazın tamamı bu sürüme işlendi.
- **Piyasa kuralları:** 17 iddia Borsa İstanbul'un güncel prosedürlerinden (Pay Piyasası rev. 54, VİOP rev. 70) kontrol edildi; 17'si doğrulandı, düzeltilen yok.
- **Endeks, fon ve literatür:** 15 iddia kontrol edildi; 15'i doğrulandı. Dört akademik kaynak yalnız özetinden görüldü.
- **TradingView kodları:** 57 kodun 57'sinin sayfası açılıyor.
- **Araç:** `sinyal.py` son 400 işlem gününde araştırma koduyla birebir aynı.

**Protokolden sapmalar**
- Kıyas ölçüsü sınama sonuçları görüldükten sonra değiştirildi (3.8). Kasa bu değişiklikten sonra açıldı.
- Sade seçim kuralı ve "en kötü beşte birlik" kasada önceden kayıtlı ölçüyle geçmişti; yeniden üretim kıyasın çöküş hisseleriyle kirlendiğini gösterdi ve ikisi geri çekildi.
- 15 hisselik sepet ve S1 ile S2'nin birlikteliği sonradan türetildi; doğrulanmış kural değildir.

**Bilinen sınırlar**
- **Komisyon varsayımdır.** Aracı kurum komisyonları, asgari komisyon ve toplu emir olanağı doğrulanmadı.
- **Faiz oranı varsayımdır** (3.3).
- **Kapanış seansı derinliği ölçülemedi.** Hacim payı (günlük hacmin yaklaşık %2,5–4,5'i) dolaylı tahmindir.
- **TradingView veri gecikmesi** (15 dakika) bu çalışmada yeniden doğrulanmadı; hesabında kontrol et.
- **Tedbirli hisseler:** brüt takas gibi tedbirler altındaki hisselerde 1 günlük çıkış yapılamayabilir; tedbir tarihleri veride yok.
- **Evren bugünkü 42 üyeden oluşuyor.** Son üç yılda endeksten çıkan hisse bulunmadı ama resmi kaynaktan kesinleştirilmedi.
- **Hisselerde gerçek 17:50 fiyatı** yalnız son 60 gün için var; öncesi 17:30 fiyatıyla ölçüldü.
- **Kütüphane sapması:** çıkış kaydırması 5 günle sınırlı (yöntem "ilk kilitsiz kapanış" diyordu). Momentum rakamlarını 7–8 bps temkinli tarafa çekiyor; kasa dönemindeki seçim ve kaçınma rakamlarını ise şişirdiği için o rakamlar temiz kıyasla verildi.
- **Veri kaynağı:** İş Yatırım'ın günlük endeks servisi son gün için tutarsız değer döndürebiliyor; betik saatlik seriyle düzeltiyor.
- **Keşif dönemi dar:** 2019'a kadar yalnız yaklaşık 10 elektrik hissesi işlem görüyordu. 2015 sonu öncesindeki tavan/taban bayrakları güvenilmez.
- **Pine kodları derlenmedi.**

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
- `ek/dogrulama_piyasa_kurallari.md`, `ek/dogrulama_xelkt_literatur.md`: kaynak doğrulaması. `ek/elestirmen1.md`, `ek/elestirmen2.md`: eleştirmen notları.
- `kod/`: bütün kod; `araclar/`: günlük kullanım araçları.

## 6. Devam notu

- **Bulunan:** elektrik hisselerinde işlenebilir öncülük yok. Sektör momentumu (S1, S2) kasada kayıtlı ölçüyle geçti ama sağlamlık sınamalarında zayıfladı ve maliyet ile faiz sonrası sıfıra yakın. S3 piyasa momentumu ve birkaç güne bağımlı. Kaçınma kuralı 2023 sonrasında tutarlı. VİOP satış sinyali yok.
- **Dosyalar:** bu rapor, `ek/kasa_sonuc.csv`, `ek/tum_oos_sonuc.csv`, `ek/v3_curutme_momentum.md`, `ek/v5_sepet.md`, `ek/elestirmen1.md`, `araclar/sinyal.py`.
- **Veri depoda yok** (yeniden indirilebilir): `kod/d1_veri/run.sh` ve `kod/d2_veri/run.sh`; paneller `kod/ortak/elib.py` ile okunur.
- **Açık işler:** Pine kodlarını TradingView'da derleyip denemek; kendi komisyonunla ve gerçek TL faiziyle 3.3'ü yeniden hesaplamak; kapanış seansı dolumunu küçük tutarla denemek.
- **İleriye dönük sınama:** 21.11.2026 sonrasındaki her S1, S2, S3 günü yeni veridir; `sinyal.py --gecmis` ile kayıt tutulabilir.

*Maliyet özeti: Seviye L+ · 28 Fable alt ajan (1. dalga 6, 2. dalga 8, kasa öncesi 3, doğrulama ve uygulama 7, kaynak doğrulayıcı 2, eleştirmen 2) + 7. dakikada durdurulan 2 sonnet · 3 üretim dalgası + doğrulama · kontrol noktasını geçenler: literatür ve piyasa kuralları araştırmacıları (51/35; eksik sayı ve tarihleri tamamlamak için), VİOP veri ajanı (41/40) · model ataması kullanıcı isteğiyle protokolden farklı (bütün alt ajanlar Fable).*
