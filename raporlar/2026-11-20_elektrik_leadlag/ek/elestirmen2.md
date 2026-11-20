araç: 18/25

# Eleştirmen 2 — kullanıcı gözüyle (uygulanabilirlik, anlaşılırlık)

Biçim: **Yer** (kısa alıntı) · **Sorun** · **Öneri** (hazır metin). RAPOR.md değiştirilmedi.

## KRİTİK

1. **Yer:** 1. bölüm, "sinyalleri 'ne zaman alınır, ne alınmaz' süzgeci olarak kullan" + 2.2'nin tam işlem akışı + 2.6 "gerçek paradan önce".
   **Sorun:** Üç mesaj yan yana duruyor: "kâra dönüşmüyor", "şu saatte şu emri gir", "bir yıl kâğıt üstünde izle". Okur yarın ne yapacağını bilmiyor. "Süzgeç" neyi süzüyor, yazılmamış: başka bir alım nedeni olmayan kişi için süzülecek bir şey yok.
   **Öneri (1. bölümün ilk maddesi olarak):** "Yarın için net öneri: bu sinyallerle şimdilik gerçek parayla işlem yapma. (a) Elektrik hissesini zaten başka bir nedenle alacaksan alımı S1 ya da S2 gününe denk getir ve kaçınma listesindeki hisseyi alma. (b) Sinyalin kendisiyle işlem yapmak istiyorsan önce 2.6'daki gibi kâğıt üstünde izle. (c) Komisyonun gidiş-dönüş %0,25'ten yüksekse hiç başlama. 2.2'deki akış, (a) ve (b) için 'nasıl yapılır' tarifidir; 'yap' demek değildir."

2. **Yer:** 2.2 adım 1, "17:30: hisselere bak. Tabana değmiş, sektörün 5 puan gerisinde…" ve 2.3 "güncel listeyi `araclar/sinyal.py` verir".
   **Sorun:** Bu adım araçlarla yapılamıyor. `sinyal.py --gunici` yalnız endeks sinyalini günceller; hisse listeleri dünkü kapanışa aittir (sinyal.py satır 432–433: "kaçınma ve T2 listeleri bugün için geçerli değildir"; KULLANIM.md satır 31). Kesin liste 18:10'dan sonra, yani emir penceresi kapandıktan sonra çıkıyor. Rapor bunu söylemiyor.
   **Öneri:** "17:30'da kaçınma listesini araç vermez; elle bak: TradingView izleme listesini 'Değişim %' sütununa göre sırala. XELKT'nin günlük yüzdesinden 5 puan çıkar (XELKT −%1 ise sınır −%6); bunun altındaki hisseyi alma. Günün en düşüğü −%10'a inmiş hisseyi alma. +%7'nin üstündekini alma. `sinyal.py`'nin kaçınma ve sepet listesi ancak 18:10'dan sonra kesinleşir; o liste ertesi günün kaydı içindir."

3. **Yer:** 2.1 "K Kaçınma: tabana değdi ya da ≥ 5 puan geride" ve "Kaçınma listesinde MAGEN var"; 4. bölüm "'en kötü beşte birlik' … geri çekildi"; 3.2 "3'ü en sıkı düzeltmeden geçti (… 'en kötü beşte birlik')".
   **Sorun:** Araç başka bir şey söylüyor. ornek_cikti satır 65–68 "bu hisseleri bugün kapanışta ALMA" başlığı altında "günün en kötü beşte birliği" diye 8 hisse sayıyor (AKSEN, BESTE, IZENR, MOGAN dahil); KULLANIM.md satır 24 "Sinyal olsa da bunları almayın" diyor; sinyal.py satır 10 "K1 … (ALMA)". Bu kural her gün sepetin beşte birini yasaklar; doğrulanan sürüm ise tam sepettir. Önerilen 15'lik listedeki BESTE, IZENR, MOGAN bugün bu etiketi taşıyor. Rapor kendi içinde de çelişiyor (3.2 "geçti", 4 "geri çekildi").
   **Öneri:** Rapora: "Araç çıktısındaki 'en kötü 1/5' etiketi geri çekilen bir kuraldır; dikkate alma. Kaçınma yalnız iki koşuldur: tabana değme ve 5 puan geride kapanma (çıktıda 'KAÇIN-5' ve 'taban')." 3.2'ye: "'En kötü beşte birlik' en sıkı düzeltmeden geçmişti; yeniden üretimde geri çekildi (4. bölüm)." Araç tarafı: sinyal.py satır 452–457 ve KULLANIM.md satır 24'te bu satır "bilgi; kural değil" diye ayrılmalı.

4. **Yer:** 2.7 "gösterge (S1, S2, S3 işaretleri, alarm…)"; KULLANIM.md satır 8 "Alarm … Çubuk kapanışında bir kez".
   **Sorun:** Günlük çubuk kapanışında çalan alarm, kapanış seansından sonra gelir; o saatte alım yapılamaz. Rapor ayrıca "sinyali kaçırıp ertesi gün girme" diyor (2.4). Alarm bu hâliyle işlem için kullanılamaz, yalnız kayıt içindir. İkinci engel: TradingView'da BIST verisi gerçek zamanlı paket ya da aracı kurum bağlantısı yoksa 15 dakika gecikmelidir (TradingView destek sayfası: "you will receive BIST data with a 15 minute delay"; güncel koşul doğrulanmadı). 17:50'de görülen değer 17:35'in değeri olabilir.
   **Öneri:** "Alarm kapanıştan sonra çalar; işlem kararı için geç kalır, yalnız kayıt tutmaya yarar. 17:50 kararı için: bir gece önce yazılan tetik düzeyini (bugün için S1 571,59; S2 548,31) not al, 17:50'de XELKT'yi bununla kıyasla; hesap gerekmez. İstersen bu düzeye TradingView'da fiyat alarmı kur; gün içinde çalarsa 17:50'de yeniden bak. TradingView'da BIST verin gecikmeliyse (grafikte 'D' işareti) 17:50 değerini aracı kurum uygulamasından oku."

5. **Yer:** 2.1 tablo, S3 satırı: "Ne alınır: AKSEN, ENJSA, ODAS spot, 3 gün · Güven: Düşük; izleme".
   **Sorun:** "Al" mı "izle" mi belli değil. Aynı raporda "AKSEN, ENJSA, ODAS'ta sektör sinyali çalışmıyor" (1), "yalnız AKSEN, ENJSA ya da ODAS alma" (2.4) ve 3.3'te tek artıdaki satır S3 (+100) var. Araçlar ise doğrudan "AL" diyor: sinyal.py satır 7 ve 420 ("AKSEN, ENJSA, ODAS (spot) bugün kapanışta AL"), elektrik_sinyal.pine satır 8 ve 112 ("spot: kapanışta giriş, 3 gün"). S1 ve S2 için de aynı (sinyal.py satır 412, 416; pine satır 6–7, 110–111).
   **Öneri:** Tabloda "Ne alınır" hücresi: "Şimdilik alma; kâğıt üstünde izle (izlenecek: AKSEN, ENJSA, ODAS spot, 3 gün)". Altına: "S3 ile S1/S2 ayrı şeylerdir: S1/S2 günü bu üç hisseyi tek başına alma (çalışmıyor); S3 günü bu üçlü geçmişte iyi getirdi ama kazanç birkaç güne bağlı ve son dönemde doğrulanmadı." Araç metinleri: "AL … SAT" yerine "sinyal var; rapor 2.2'ye göre karar ver. S3: yalnız izleme".

6. **Yer:** 2.2 adım 3–4, "18:00 değerini bekle … 18:01–18:04: kapanış seansına emir gir"; 2.3 "Elle 40 emir zor".
   **Sorun:** Bekleme kuralı uygulanınca 15–40 emir için 4 dakika kalıyor; telefondan elle girilemez. Emir başına adet hesabı (tutar ÷ fiyat) da o 4 dakikaya sığmaz. Asgari komisyon ve toplu emir olanağı kontrol edilmedi (v5_sepet.md satır 43); rapor bunu yalnız 4. bölümde, komisyon başlığında söylüyor. Tek lotu pahalı hisse de yazılmamış: 100 bin TL'de hisse başına 2.381 TL düşer, LYDYE (2.902,50 TL) alınamaz (v5 madde 4); rapor "100 bin TL'lik sepet sorunsuz" diyor.
   **Öneri:** 2.2'ye: "Hazırlık 17:30'da yapılır: hisse başına tutarı ve adedi (tutar ÷ fiyat, aşağı yuvarla) önceden yaz. Aracı kurumunda 'sepet/toplu emir' ya da 'emir taslağı' varsa onu kullan; yoksa 4 dakikada elle 40 emir girilemez, 12–15 hisseyle sınırla. Kurumuna sor: emir başına asgari komisyon var mı? Varsa hisse başına tutar küçüldükçe maliyet varsayımı bozulur. Hisse başına tutar tek lot fiyatının altındaysa o hisse alınamaz (bugün LYDYE 2.902 TL)." 2.3'te "sorunsuz" yerine: "100 bin TL'de kapanış seansı hacmi sorun değil; LYDYE dışında bütün hisseler alınabilir."

## ÖNEMLİ

7. **Yer:** 1. bölüm, "70–85 bps fazla getirdi … yaklaşık 30–35 bps işlem maliyeti ve … faizi (32–44 bps) düşünce ortalama sıfıra yakın".
   **Sorun:** Okur 70–85'ten 62–79 çıkarıp "+5…+20 kalıyor" diye okur; oysa hesap fazla getiriyle değil ham getiriyle (74) yapılıyor. İki ölçü aynı cümlede karışıyor. bps telefonda zor okunuyor.
   **Öneri:** "Sinyal günü alınan sepet 3 günde ortalama %0,74 kazandırdı (sıradan günlerden %0,7–0,85 fazla). Komisyon ve fiyat farkı %0,30–0,35, aynı paranın 3 günde faizde kazanacağı %0,32–0,44. Elde kalan: yaklaşık sıfır."

8. **Yer:** 3.3, "Faiz, paranın o 3 gün boyunca nakitte kazanacağı getiridir."
   **Sorun:** Faiz kalemi herkese aynı uygulanmış. Parası hesapta boş duran kişi için bu kalem sıfırdır (S1 kalanı yaklaşık +40); parası para piyasası fonunda olan için geçerlidir ve net (stopaj sonrası) oran alınmalıdır. Karar buna göre değişiyor; rapor okura hangisi olduğunu sormuyor.
   **Öneri:** "Bu kalem senin durumuna bağlı: işlem parası zaten para piyasası fonunda ya da repoda duruyorsa faizi düş (net oranını kullan). Para hesapta boş bekliyorsa bu kalem sıfırdır ve S1'de elde kalan yaklaşık %0,4 olur; yine de bu ortalama birkaç iyi dalgadan geliyor (3.5)."

9. **Yer:** 2.2 adım 6, "3. işlem günü: kapanış seansında sat. … çıkışı son sinyalden 3 gün sonraya ertele."
   **Sorun:** (a) "3. işlem günü" sinyal günü sayılarak mı, sayılmadan mı, belli değil. (b) Hafta sonu ve tatil taşıması, yarım gün (sürekli işlem 12:30'da biter; akıştaki saatler geçersiz; `sinyal.py` yarım günde sınanmadı) yok. (c) Erteleme kuralı doğrulanmış değil ve tutma süresini ortalama 7 güne çıkarıyor (v5: "~10 giriş, ortalama 7 gün"); kullanıcı 1–3 gün istemişti, 2.5'teki risk rakamları 3 günlük olaylar içindir. (d) Çıkış günü hisse tabandaysa ne yapılacağı yazılmamış.
   **Öneri:** "Sinyal günü 0 sayılır: pazartesi sinyal → perşembe kapanışında sat; perşembe sinyal → salı kapanışında sat (hafta sonu taşınır). Resmî tatil öncesi yarım günlerde işlem yapma: saatler farklı, araç sınanmadı. Erteleme kuralı sonradan türetildi; uygulanırsa pozisyon ortalama 7 gün açık kalır ve kayıp 2.5'teki rakamları aşabilir. Kesin 3 gün istiyorsan erteleme, yeni sinyali yok say. Çıkış günü hisse tabanda kilitliyse satış emrini her gün kapanış seansında yinele; bu durum işlemlerin %1'inde görüldü."

10. **Yer:** 1. bölüm, "En işe yarar bulgu bir kaçınma kuralı"; 6. bölüm "kaçınma kuralı sağlam"; 2.1'de güven "Orta".
    **Sorun:** Üç yerde üç ayrı güven düzeyi. Kural 1 günlük ve sektöre göre bir farktır (mutlak zarar değil). Sepete süzgeç olarak katkısı küçük: v5 madde 2 "K2 süzgeci: IS 0, OOS-1 +2'ye kadar, kasa +8 ile +16". 5 puan geride kalan hisse seyrek (bugün 40'ta 1). 3.2 tablosunda eksi sayının ne demek olduğu yazılmamış.
    **Öneri:** "Kaçınma kuralı tek hisse seçen için işe yarar: o gün sektörün 5 puan gerisinde kapanan hisse ertesi gün de sektörden ortalama %0,7 kötü kaldı. Sepete katkısı küçüktür (3 günde en çok %0,1–0,2). Güven: orta." 3.2 tablo altına: "K satırında eksi sayı, kaçınılan hissenin ertesi gün sektörden o kadar kötü getirdiğini gösterir; eksi olması kuralın çalıştığı anlamına gelir."

11. **Yer:** 2.3, "60 günlük hacim sırasında 6.–20. olan 15 hisse. Bugün: … MOGAN, BIOEN, KLYPV."
    **Sorun:** (a) Araç bu listeyi yazmıyor; okur 40 satırdan 6.–20. satırları kendisi sayacak. (b) Sayınca farklı çıkıyor: ornek_cikti satır 42–43'te 20. sıra TATEN, 21. sıra KLYPV (ikisi de 79 mn TL); raporda KLYPV var, TATEN yok. (c) İlk 5'in neden atlandığı bu maddede yazmıyor. (d) Listede adımı çok kaba hisseler var: CANTE'de bir fiyat adımı %1,08, ZOREN'de %0,72; tek adımlık kayma beklenen kazancı siler. (e) Listede ODAS var; okur "üçlüde çalışmıyor" cümlesiyle çelişki görür.
    **Öneri:** "Araç çıktısındaki sepet tablosunun 6.–20. satırlarını al (ilk 5 atlanır: en likit 5 hissede etki yarıdan az). Bugün: AHGAZ, ODAS, CANTE, METEN, HUNER, MASFN, AKFYE, BESTE, IZENR, SMRTG, VEYAS, ZOREN, BIOEN, MOGAN, TATEN. Tablodaki 'adım' sütunu 50'nin üstündeyse (bugün CANTE, ZOREN) o hissede fiyatın tek adım oynaması %0,5–1 demektir; listeden çıkarıp sıradakini al. ODAS burada sepetin 15'te biri olarak yer alır; tek başına alınmaz."

12. **Yer:** 2.2 adım 4, "son fiyatın 1–2 adım üstünde limit ya da piyasa emri".
    **Sorun:** "Adım" tanımsız (ilk açıklama yok). Limitin tavan fiyat olduğu, ödenecek fiyatın kapanış fiyatı olduğu yazılmamış; okur 2 adım fazla ödeyeceğini sanar. Piyasa emri eşleşmezse iptal olur, limit kapanış fiyatının altında kalırsa dolmaz, emir son fiyatın ±%3'ünü aşamaz (v6_zamanlama.md satır 28–30); raporda yok.
    **Öneri:** "Adım = fiyatın oynayabileceği en küçük miktar (20 TL altında 1 kuruş, 20–50 TL arasında 2 kuruş). Kapanış seansında herkes aynı fiyattan (18:05'te belirlenen kapanış fiyatı) işlem yapar; yazdığın limit ödeyeceğin fiyat değil, razı olduğun en yüksek fiyattır. Limit kapanış fiyatının altında kalırsa emir dolmaz; piyasa emri karşılık bulamazsa iptal edilir. Emir fiyatı son işlem fiyatının %3'ünden uzak olamaz."

13. **Yer:** 2.6, "En az 10 sinyal dalgası (yaklaşık bir yıl) ya da 20 işlem … 20 işlem sonunda … ortalama eksiyse bırak."
    **Sorun:** "Dalga" tanımsız; "işlem" her sinyal günü mü (yılda ~45), her giriş mi (yılda ~10), belli değil. 20 işlemin ortalaması bu stratejiyi sınamaya yetmez: olay başına oynaklık %3,1 (v5), 20 olayın ortalamasındaki belirsizlik yaklaşık ±%1,4; beklenen fark ise %0–0,4. Ölçüt okura yanlış güven ya da yanlış vazgeçme verir.
    **Öneri:** "Dalga = art arda gelen sinyal günleri (yılda yaklaşık 10). Kâğıt üstü izlemenin amacı stratejiyi kanıtlamak değil, kendi maliyetini ve emirlerin dolup dolmadığını görmektir: 20 işlem, kazancın gerçek olup olmadığını ayırt etmeye yetmez (ortalamadaki belirsizlik yaklaşık ±%1,4). Bırakma ölçütü: gerçekleşen maliyetin (komisyon + fiyat farkı) işlem başına %0,35'i aşıyorsa ya da emirlerin beşte biri dolmuyorsa bırak."

14. **Yer:** 2.1 "D Sakin hisse: 20 günlük oynaklığı sektörün alt yarısında"; araçta "T2 SAKİN VE GÜÇLÜ".
    **Sorun:** Ad ve tanım tutmuyor. Araçtaki T2 ayrıca "günlük getirisi en üst üçte birlikte" koşulunu arar (sinyal.py satır 8–9, ornek_cikti satır 70; KULLANIM.md satır 25). Rapor 3.6'da bu birleşik kuralı "doğrulanmadı" diyor, D'yi ise tabloya koyuyor. D'nin kendisi hiçbir araçta görünmüyor. Günde 5–12 bps maliyetin altında; tabloya beşinci satır olarak yük bindiriyor.
    **Öneri:** D satırını tablodan çıkar; altına tek cümle: "Seçim yapacaksan oynaklığı düşük hisseyi yeğle (etki küçük: günde %0,05–0,12). Araç çıktısındaki 'T2 sakin ve güçlü' listesi doğrulanmamış bir kuraldır; yalnız oynaklık sütununa bak."

15. **Yer:** KULLANIM.md satır 35, "S1 ve S2 temel maliyetten sonra yaklaşık +40 bps bırakıyor"; satır 14 "EVET çıkarsa … emri hazırlayın"; satır 12 "17:50: … XELKT ve XU030 değerini okuyun".
    **Sorun:** KULLANIM raporun sonucuyla uyumsuz: faiz düşülmemiş (+40 ↔ raporda "sıfıra yakın"), kâğıt üstü izleme ve "süzgeç" yok, S3 için 17:50 öneriliyor (rapor: "S3'e yalnız 18:00'de bak"), kaçınma listesinin 17:30'da elle bakılması yok.
    **Öneri (KULLANIM.md için):** Satır 35: "S1 ve S2 maliyetten sonra yaklaşık +40 bps, 3 günlük faiz de düşülünce sıfıra yakın bırakıyor (rapor 3.3). S3 yalnız izleme içindir." Satır 14: "EVET çıkarsa rapor 2.2'ye göre karar verin; rapor önce kâğıt üstünde izlemeyi öneriyor." Satır 12'ye: "S3 için XU030 değerini 18:00'de girin."

16. **Yer:** 2.4 "kasada eksi" (kasa 3.1'de tanımlanıyor); ayrıca "spot", "üçlü", "olay", "dalga", "temiz kıyas", "çoklu test düzeltmesi", "sağ kuyruk", "gidiş-dönüş", "baz", "medyan", "tavan/taban".
    **Sorun:** Terimler ilk geçtiği yerde açıklanmıyor; "kasa" tanımından 30 satır önce kullanılıyor. Tavan/taban oranı (±%10) raporda hiç yazmıyor.
    **Öneri (Sözlük'e ek):** "**Kasa** = en sona kadar hiç bakılmayan son dönem (Temmuz 2025 → Kasım 2026); bir kuralın gerçek sınavı. **Spot** = hissenin kendisi (vadeli değil). **Üçlü** = AKSEN, ENJSA, ODAS. **Tavan/taban** = bir hissenin günlük en çok ±%10 oynayabilmesi. **Olay** = bir sinyal günü. **Dalga** = art arda gelen sinyal günleri. **Gidiş-dönüş** = alış ve satış birlikte. **Medyan** = ortadaki değer. **Temiz kıyas** = (tanımı ana ajan yazmalı; rapordan anlaşılan: çöken üç hisse BIGEN, LYDYE, MAGEN çıkarılarak yapılan karşılaştırma)." "Dalga" tanımı da rapordan çıkarımdır; ana ajan doğrulamalı.

17. **Yer:** 2.5, "olayların en kötü %5'i −%4 ve altı; en kötü olay −%8,9".
    **Sorun:** Zarar-kes emri konusu yok; bireysel yatırımcının ilk soracağı şey. Sınama zarar-kessiz yapıldı. Rakamlar TL'ye çevrilmemiş.
    **Öneri:** "100 bin TL'lik pozisyonda: her 20 işlemden birinde 4 bin TL ve üstü, görülen en kötü olayda 8.900 TL (S2'de 10.400 TL) kayıp. Sınama zarar-kes emri olmadan yapıldı; zarar-kes kullanırsan buradaki rakamlar geçerli olmaz. Taban günü zarar-kes emri de dolmaz."

## KÜÇÜK

18. **Yer:** 2.3, "**En likit hisselere daraltma.** En likit 5 hissede etki yarıdan aza iniyor".
    **Sorun:** "Daraltma" Türkçede hem "daraltmak işi" hem "daraltma!" diye okunur; kalın yazıldığı için öneri sanılabilir.
    **Öneri:** "**En likit 5 hisseyle yetinme:** etki yarıdan aza iniyor; AKSEN/ENJSA/ODAS üçlüsünde yok."

19. **Yer:** 2.1 tablosu (4 sütun, uzun koşul hücreleri), 3.6 tablosu (uzun metin hücreleri), 3.2 (5 sütun).
    **Sorun:** Telefonda yatay kaydırma gerekir; 2.1 kararın dayandığı tablo ve en çok okunacak yer.
    **Öneri:** 2.1'i sinyal başına üç satırlık listeye çevir: "**S1 Zirve** — Koşul: … — Ne yapılır: … — Güven: …". 3.6'yı madde listesine çevir; 3.2'de "2023 sonrası toplam" sütununu başa al, "2010–2022" sütununu eke taşı.

20. **Yer:** 2.2 adım 3, "eşiğe çok yakınsa (zirvenin ±%0,15'i) 18:00 değerini bekle".
    **Sorun:** Yalnız S1 için ölçü var; S2 için yok (v6_zamanlama.md satır 36: "z 0,9–1,1").
    **Öneri:** "Eşiğe çok yakınsa (S1: zirvenin ±%0,15'i; S2: göstergede z 0,9–1,1 arası, yani tetik düzeyinin yaklaşık ±%0,2'si) 18:00 değerini bekle."

21. **Yer:** 2.5, "ham ortalama +74 bps, medyan +62, işlemlerin %59'u artıda".
    **Sorun:** v5_sepet.md aynı sepet için "ham ortalama, medyan 75, 78" ve "zarar olasılığı (net) %44" veriyor. Medyan 62 ↔ 78 farkının kaynağı raporda yok; hangisinin hangi ölçü olduğu (ham mı, net mi; olay mı, hisse-işlem mi) belirtilmeli.
    **Öneri:** Rakamı kaynağıyla eşle ve birimi yaz: "olay başına ham ortalama +74, medyan +… (v5 tablosu); maliyet sonrası olayların %44'ü zararda."

22. **Yer:** elektrik_sinyal.pine satır 100 "S3 gecikme", satır 8 "(sektör geride)"; rapor 3.5 "S3 gecikme değil, piyasa momentumu"; rapordaki ad "S3 Piyasa önde".
    **Sorun:** Araçtaki ad, raporun çürüttüğü yorumu taşıyor; rapordaki ad da öncülük çağrıştırıyor.
    **Öneri:** Üç yerde tek ad: "S3 Piyasa güçlü günü". Rapora: "Ad yanıltmasın: bu bir öncülük değil, piyasanın güçlü gününden sonraki genel devam etkisidir."

23. **Yer:** 2.1, "S1 ve S2 aynı gün gelirse geçmişte etki daha büyüktü (+125 bps, 54 gün). … doğrulanmadı."
    **Sorun:** Doğrulanmamış en büyük rakam, "Ne yapmalıyım" bölümünün başında duruyor; okuru en çok cesaretlendiren satır bu.
    **Öneri:** 3.5'e taşı ya da şu hâle getir: "S1 ve S2'nin aynı güne denk gelmesi ek bir sinyal sayılmaz; sonradan bakılan bu kesit doğrulanmadı."

24. **Yer:** 3.3 tablosu, "S3, 2023 sonrası … yaklaşık +100".
    **Sorun:** Tablodaki tek büyük artı; uyarı tablonun altında, ayrı maddede. Telefonda tabloyu görüp geçen okur yanlış sonuç çıkarır.
    **Öneri:** Hücreye dipnot işareti koy ve satırı şöyle yaz: "S3, 2023 sonrası | +177 | 35 | 32–44 | yaklaşık +100 (en iyi 10 gün çıkınca yaklaşık 0)".

25. **Yer:** 2.7, "`sinyal.py`: her akşam çalıştırılır"; KULLANIM.md satır 5 "Bilgisayar ya da bulut: Python 3.9+".
    **Sorun:** Okur telefonda; betiği telefondan çalıştıramaz. Rapor aracı olmayan okur için asgari yolu söylemiyor.
    **Öneri:** "Bilgisayarın yoksa: S1 ve S2 için gösterge ve betik şart değil. S1 = XELKT kapanışı son 20 günün en yükseği (grafikte gözle görülür). S2 = XELKT'nin günlük artışı yaklaşık %2 ve üstü (kesin eşik bugün %2,1; ayda bir güncelle). Sepet ve kaçınma listesi için TradingView izleme listesi yeter (2.2 adım 1)."

Kaynak (madde 4, TradingView gecikmesi): https://www.tradingview.com/blog/en/borsa-istanbul-live-data-22031 · https://ru.tradingview.com/support/solutions/43000725196 (ikincil; güncel abonelik koşulu doğrulanmadı).

## açık kalanlar

- `sinyal.py`'nin 500+ satırının tamamı okunmadı; yalnız başlık (satır 5–11), çıktı bölümü (392–436) ve anahtar sözcük eşleşmeleri görüldü.
- Madde 13'teki ±%1,4 ve madde 10'daki %0,7 kaba hesaptır (v5'teki 308 bps olay oynaklığından ve rapor 3.2'deki −69 bps'den).
- Aracı kurumlarda asgari komisyon ve toplu emir olanağı bu görevde de doğrulanmadı.
