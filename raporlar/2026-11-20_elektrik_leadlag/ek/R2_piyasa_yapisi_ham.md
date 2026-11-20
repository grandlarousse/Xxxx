araç: 51/35 (devam nedeni: 35'te açığa satış yasağı tarihleri ve komisyon aralıkları doğrulanmamıştı; sonraki çağrılar 2026 yasağı, 22/09/2026 yukarı adım kuralı ve tarife verisi getirdi)

## Özet

Ana kaynaklar bu oturumda indirildi: Pay Piyasası Prosedürü rev. 54 (21/09/2026) ve VİOP Prosedürü rev. 70 (01/07/2026). Maliyet tablosu yazıldı: `/home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/maliyet.md`.

**Düzeltilen varsayımlar**
- VİOP normal seansı 18:15'te değil **18:10**'da biter. Pay vadelileri akşam seansında işlem görmez (yalnız endeks, metal, kıymetli maden).
- Pay vadelisi fiyat adımı spot tablosundan farklıdır: 100 TL altı 0,01; 100–500 TL 0,05.
- Kalıcı marj kuralı Yıldız ±%20, Ana ±%15'tir. Fiilen 2020/20 sayılı duyuruyla ±%10 uygulanıyor ve Eylül 2026 metninde hâlâ yürürlükte. Pay vadelisinde de limit ±%10.
- Açığa satışta yeni dönemler var: 02/03–26/06/2026 tam yasak; 22/09/2026'dan beri BIST 50'de yukarı adım kuralı.

**Soruların yanıtı**
1. Kapanış akışı: 18:00–18:01 marj yayını, 18:01–18:05 emir toplama, 18:05 (+30 sn rastlantısal) fiyat belirleme, 18:07–18:08 marj yayını, 18:08–18:10 kapanış fiyatından işlemler. Son aşamada yeni emir yalnız kapanış fiyatından girilir ve aynı fiyatta karşı pasif emir varsa eşleşir; yoksa bekler. Garantili dolum yok.
2. Tavanda kapanış (kurallardan çıkarım): fiyat üst sınırı aşamaz, bekleyen alışlar fiyat-zaman önceliğiyle sıralıdır, satıcı az olur. 18:01 sonrası girilen alış kuyruğun sonundadır; 18:08–18:10'da karşı satış emri kalmaz. Backtest'te tavan kapanışlı günlerde giriş "dolmadı" sayılmalı.
3. Spot kapanış ~18:05'te belli olur; pay vadelisi 18:10'a kadar sürekli işlem görür. Yani yaklaşık 4–5 dakikalık pencere var; 18:10 sonrası işlem yok. Günlük uzlaşma: son 10 dakikanın (18:00–18:10) miktar ağırlıklı ortalaması; 10'dan az işlemde geriye dönük son 10 işlem.
4. Marj: ±%10 (12/03/2020 duyurusu); kapanış seansında son fiyat ±%3.
5. Adım tabloları defterde.
6. Maliyet (gidiş-dönüş): spot düşük 4–5 bp, temel 18–25 bp, banka tarifesi 50+ bp; VİOP 6–10 / 15–30 / 45+ bp. VİOP rakamları alış-satış farkı ölçülmeden yazıldı.
7. Yasaklar: 2020 (28/02 ve 02/03 kararları; BIST-30'da 01/07/2020'de kalktı), 06/02/2023–01/01/2025 (02/01/2025'te yalnız BIST 50'de kalktı), 24/03–29/08/2025, 02/03–26/06/2026.

**Listede olmayan bulgular:** 46 pay dayanağı var; elektrik tarafında AKSEN, ENJSA, ODAS (ayrıca ASTOR, ekipman üreticisi). ELCBAS listede. Devre kesici 01/09/2025'te değişti (emir toplama 10 dk; yukarı adım eşiği BIST 100 −%2). Vadeli fiziki teslimatlı.

**Aykırı kanıt araması:** 2025–2026'da spot seans saatlerinde ve marjda değişiklik bulunmadı; değişenler devre kesici, açığa satış ve emir/işlem oranı.

## İddia defteri

iddia | kaynak | alıntı/sayı | güven
---|---|---|---
Pay Piyasası Prosedürü güncel sürüm | https://borsaistanbul.com/files/pay-piyasasi-proseduru.pdf | "Revizyon Tarihi 21/09/2026 Revizyon Numarası 54" | yüksek
Açılış emir toplama 09:40–09:55, sürekli 10:00–18:00 | aynı (Ek-10) | "Emir Toplama Süreci 09:40 – 09:55 … Sürekli İşlem Bölümü 10:00 – 18:00" | yüksek
Kapanış emir toplama 18:01–18:05 | aynı | "Kapanış Marj Yayını 18:00 – 18:01 … Emir Toplama 18:01 – 18:05" | yüksek
Kapanış fiyatı 18:05'te (+30 sn) | aynı | "Kapanış Fiyatının Belirlenmesi 18:05 (+)**" | yüksek
Kapanış fiyatından işlemler 18:08–18:10 | aynı | "Kapanış Fiyatından / Tek Fiyattan İşlemler 18:08 – 18:10" | yüksek
Son aşamada emir yalnız kapanış fiyatından | aynı (5.2) | "yeni alış ve satış emirleri sadece belirlenmiş kapanış/son işlem fiyatından olabilir" | yüksek
Eşleşme karşı pasif emre bağlı | aynı | "aynı fiyattaki bir pasif emir ile karşılaşması hâlinde öncelik sırasına göre işleme dönüşür" | yüksek
Kapanış seansı marjı ±%3 | aynı | "son normal emir işlem fiyatının ±%3'ünden daha fazla farklı olamaz" | yüksek
Kalıcı marj kuralı pazara göre | aynı (5.1.11) | "Yıldız Pazar'da±%20'den, Ana Pazar'da ±%15'ten; Alt Pazar, YİP ve PÖİP'te ±%10'dan" | yüksek
Fiilen ±%10 uygulanıyor | https://borsaistanbul.com/piyasalar/pay-piyasasi/piyasa-isleyisi | "Fiyat marjı Yıldız Pazar, Ana Pazar, borsa yatırım fonları … %10'dur" | yüksek
Geçici kurallar hâlâ yürürlükte | Pay Piyasası Prosedürü dipnot 10 | "ikinci bir duyuruya kadar geçerli olduğu ilan edilen duyurularda (2020/20, 2020/21, 2020/50, 2025/38860)" | yüksek
Spot fiyat adımı tablosu | aynı (Tablo-7) | 0,01–19,999: 0,01; 20–49,999: 0,02; 50–99,999: 0,05; 100–249,999: 0,10; 250–499,999: 0,25; 500–999,999: 0,50; 1000–2499,999: 1; üstü 2,5 | yüksek
Spot borsa payı | aynı (Ek-20) | "Pay Piyasasındaki tüm pazarlarda … gerçekleştirilen işlemler 0,25" (bps) | yüksek
Devre kesici değişikliği 01/09/2025 | aynı (duyuru listesi) | "01/09/2025 Pay Bazında Devre Kesicilerde … Duyuru 2025/38860" | yüksek
Yukarı adım eşiği BIST 100 −%2 | aynı (5.8.2) | "%2 veya üzerinde düşmesi durumunda … yukarı adım kuralı seans sonuna kadar otomatik" | yüksek
VİOP Prosedürü güncel sürüm | https://borsaistanbul.com/files/borsa-istanbul-as-vadeli-islem-ve-opsiyon-piyasasi-proseduru.pdf | "Revizyon Tarihi 01/07/2026 Revizyon Numarası 70" | yüksek
VİOP normal seans 09:30–18:10 | aynı (Ek-3) | "VIOP_SUREKLI_MZYD 09:30:00 … VIOP_SEANS_SONU 18:10:00 / 12:40:00" | yüksek
Akşam seansı kapsamı; pay vadelisi yok | https://borsaistanbul.com/file/2025-07/viop-islem-saatleri-pazarlar-10-11-12.png | "Akşam Seansı (endeks, metal ve döviz cinsinden işlem gören kıymetli madenler vadeli işlem sözleşmeleri) 19:00-23:00" | yüksek
Pay vadelisi günlük uzlaşma | VİOP Prosedürü Ek-1/B | "son 10 dakika içerisinde gerçekleştirilen tüm işlemlerin miktar ağırlıklı ortalama fiyatı" | yüksek
Az işlemde yedek kural | aynı | "son 10 dakika içerisinde 10'dan az işlem yapıldıysa … son 10 işlemin miktar ağırlıklı ortalama fiyatı" | yüksek
Sözleşme büyüklüğü, uzlaşma şekli | aynı | "dayanak varlığa ait 100 adet payı temsil eder" ; "Uzlaşma Şekli Fiziki teslimat" | yüksek
Pay vadelisi adım tablosu | aynı | 0,01–99,99: 0,01; 100–499,99: 0,05; 500–999,99: 0,10; 1000–2499,99: 0,25; 2500+: 0,50 | yüksek
Pay vadelisi günlük limit ±%10 | aynı (dipnot) | "günlük fiyat değişim limitleri ikinci bir duyuruya kadar geçerli olmak üzere ±%10" | yüksek
VİOP borsa payı (pay vadelisi) | aynı (Ek-5) | "Diğer Tüm Vadeli İşlem Sözleşmeleri İşlem Hacmi 0,00003 (Yüzbinde 3)" | yüksek
Dayanaklar: AKSEN, ENJSA, ODAS, ELCBAS | https://borsaistanbul.com/piyasalar/viop/sozlesme-ozellikleri/dayanak-varliklar | "Aksa Enerji Üretim A.Ş. AKSEN … Enerjisa Enerji A.Ş. ENJSA … Odaş Elektrik Üretim … ODAS"; 46 pay | yüksek
2023 yasağı ve BIST 50 istisnası | https://borsaistanbul.com/piyasalar/pay-piyasasi/piyasa-isleyisi | "açığa satış yasağı … 02/01/2025 tarihinden itibaren … BIST 50 endeksinde yer alan pay piyasaları ile sınırlı olarak kaldırılmıştır" | yüksek
2020 yasağı BIST-30'da 01/07/2020'de kalktı | https://spk.gov.tr/duyurular/basin-duyurulari/2020/basin-aciklamasi-30-06-2020 | "BIST-30 Endeksinde yer alan pay piyasalarında kaldırılmasına" | orta (özet model aracılığıyla)
2025 yasağı 29/08/2025'e kadar | https://www.bloomberght.com/borsada-aciga-satis-yasaginin-uzatilmasi-planlanmiyor-3755623 | "29 Ağustos seans sonuna kadar uzatılmış"; haber 25/08/2025 | orta (ikincil; bitiş "planlanmıyor" haberi)
2026 yasağı 02/03–26/06/2026 | https://www.qnbinvest.com.tr/investodak/qnbarastirma/borsa-istanbulda-aciga-satis-yasagi-yeniden-uzatilmadi | "26 Haziran 2026 tarihinde alınan kararla bu geçici tedbirlerin süresi tamamlandı" | orta (ikincil)
22/09/2026'dan beri BIST 50'de yukarı adım | https://kap.org.tr/en/api/BildirimPdf/1666369 (açılmadı); https://www.cnbce.com/borsa/borsa-istanbul-duyurdu-bist-50-endeksinde-aciga-satisa-yukari-adim-sarti-getirildi-h37772 | arama özeti: 22 Eylül 2026 işlemlerinden itibaren, yeni duyuruya kadar | orta (yalnız arama özeti)
Komisyon veri noktaları | https://infoyatirim.com/hakkimizda/ucretler ; https://www.karekod.org/blog/hisse-senedi-komisyon-oranlari/ | "Binde2 + BSMV" (pay ve VİOP tavanı, 12/01/2026); liste on binde 1–8, banka binde 2 (Mart 2025) | orta-düşük

## açık kalanlar

- AKSEN/ENJSA/ODAS vadelilerinde gerçek alış-satış farkı, derinlik ve hacim ölçülmedi; VİOP maliyet senaryoları bu yüzden varsayımdır. VİOP bülten verisiyle kontrol edilmeli.
- Pay vadelisi başlangıç teminatı doğrulanamadı (Takasbank tablosuna ulaşılamadı; arama özeti fiyat tarama aralığını AKSEN %21,45, ODAS %21,15 olarak veriyor, tarih 04/05/2026, doğrulanmadı).
- BSMV oranı (%5) ve yüksek hacimli müşteri komisyonu (1–2 bp) bu oturumda birincil kaynakla doğrulanmadı.
- AKSEN, ENJSA, ODAS'ın BIST 50 üyeliği kontrol edilmedi; açığa satış yalnız BIST 50'de serbest olduğundan kısa bacak için belirleyici.
- 2020 yasağının BIST-30 dışı paylarda kalkış tarihi ve 2025 yasağının ara uzatmaları (25/04–27/06/2025) eksik; 22/09/2026 KAP duyurusu ve SPK 2025/2026 kararlarının asıl metinleri açılmadı.
- Tavanda dolmama (soru 2) kurallardan çıkarımdır; emir defteri verisiyle sınanmadı.
- Hisse fiyat düzeyleri (AKSEN ~67, ENJSA ~120, ODAS ~9 TL) arama özetinden, tarihleri farklı; adım/bp hesabı yaklaşık.
- VİOP seans sonunun 18:10'a alınma tarihi (arama özeti: 23/09/2022) duyuru metninden doğrulanmadı.