# ABD piyasaları: Türkiye'de yerleşik swing trader için pratik koşullar ve güncel rejim (6 Kasım 2026)

Ajan: ABD-PRATİK. Kapsam: erişim, vergi, ABD piyasa rejimi, USD eşiği, araçlar.
Yöntem: Birincil kaynaklar doğrudan okundu: FINRA RN 26-10, FOMC metni, ABD–Türkiye vergi anlaşması, IRS, GİB 2026 rehberleri, FRED serileri, IBKR/Midas/Garanti/TradeMaster fiyat sayfaları, FactSet, Cboe, Renaissance. Hesaplar FRED verisiyle yeniden yapıldı.
**Kısıt:** Çalışmanın ortasında oturumun ortak web arama kotası doldu. Sonraki her şey doğrudan sayfa okumasıyla doğrulandı. Doğrulanamayan maddeler §7'de listeli.
Yatırım tavsiyesi değildir.

---

## 0. Yönetici özeti (rakamlarla)

1. **TL eşiği, kullanıcının sandığı gibi "reel %40–50" değil.**
   - Nominal brüt: 32 gün vadeli mevduat ~%39,6. PPF aylık ~%3,0, yıllıklandırılmış brüt ~%42,9.
   - Stopaj sonrası net (bileşik): mevduat ~%38, PPF ~%34.
   - Ekim TÜFE %29,77'ye göre reel net getiri **~%3,6–6,3**. Ex-post reel politika faizi %4,8.
   - Kısacası eşik nominal **~%34–38 net**, reel ise tek hanelidir.
2. **Vergi asimetrisi büyük.**
   - BIST payları, pay/endeks VİOP ve TEFAS'taki hisse yoğun fonlar: %0 stopaj, beyan yok.
   - ABD hisse/opsiyon kazancı: TL bazında, **kur farkı dahil**, %15–40 artan oranlı tarifeyle yıllık beyan.
   - Swing vadesinde Yİ-ÜFE endekslemesi pratikte hiç devreye girmez. Bunun için ~6 ay elde tutma gerekir.
   - Zarar sonraki yıla devredilmez.
3. **Sonuç: ABD'de bir stratejinin TL nakdi yenmesi için gereken vergi öncesi USD getirisi.**
   - Varsayımlar: yıllık kur artışı %20, marjinal vergi %35, tam yatırımda kalma.
   - Gereken getiri **~%28/yıl**. Vergisiz hesapta bu %12,5 olurdu.
   - Kur artışı %25 ise ~%23, %15 ise ~%34.
   - Verginin ertesi yılın Mart/Temmuz ayında ödenmesinin bugünkü değer etkisi ve %60 yatırımda kalma oranıyla ~%20'ye iner.
   - ABD T-bill getirisi ~%4,0. Yani ABD stratejisinin T-bill'in **~16–30 puan** üstünde olması gerekir.
4. **ABD rejimi (5 Kasım kapanışı).**
   - S&P 500 7.353,73: rekordan (6 Ekim, 7.818,93) −%5,95, yılbaşından beri +%7,4. 200 günlük ortalamanın (~7.323) yalnızca %0,4 üstünde.
   - Nasdaq 24.315: rekordan −%11,9 (düzeltme) ve 200 günlüğün ~%3 altında.
   - VIX 28,18. Bu, 2026 ortalamasının (18,1) çok üstünde; yılın günlerinin yalnızca %6,4'ünde VIX 25'in üstündeydi.
   - Momentum faktöründe iki büyük çözülme yaşandı: Temmuz (MTUM 20 günlük göreli −%15,5, tarihinin en kötüsü) ve Ekim (−%8,7, dördüncü en kötü).
   - Fed 16.09'da faiz artırdı, 28.10'da 3,75–4,00'te tuttu (10–2; iki üye artırım istedi). Aralık artırımı ~%66–70 olasılıkla fiyatlanıyor.
   - Breakout ve momentum swing için **kötü olasılıklı bir rejim**. Trend filtresi ve volatiliteye göre pozisyon boyutu şart.
5. **Erişim.**
   - IBKR, Türkiye'yi hesap açılabilen ülkeler listesinde gösteriyor.
   - IBKR Pro'nun yanında Türk aracı kurumlar maliyette çok geride:
     - Garanti BBVA Yatırım %0,30, İş Yatırım/TradeMaster %0,25 (min. 1 $). 20 bin $'lık bir işlemde gidiş-dönüş ~50–63 baz puan.
     - IBKR ~2 baz puan, Midas ~1,5 baz puan (işlem başına 1,5 $).
   - Midas ABD opsiyonu sunuyor: kontrat başına 1,5 $, sayfada yalnızca alım (call/put long) anlatılıyor.
   - FINRA'nın PDT (25 bin $) kuralı kaldırıldı: SEC onayı 14.04.2026, yürürlük 04.06.2026, aracı kurumlar için geçiş 20.10.2027'ye kadar. Swing trader için pratik önemi küçük.

---

## 1. Erişim

### 1.1 Türk aracı kurumların yurt dışı hizmetleri

| Kurum | ABD hisse komisyonu | ABD opsiyon | Kredi/açığa satış (ABD) | Kaynak (tür, tarih) |
|---|---|---|---|---|
| **Midas** | İşlem başına sabit **1,5 $**. 1 $ altı hisselerde 300 adet üstüne +0,005 $/adet. ACATS ile dışarı transfer 25 $, DTC transferi 5 $/hisse. ADR saklama 0,01–0,03 $/hisse. | **Var.** Ayda 0–500 kontrata **1,50 $/kontrat**. 500 üstünde, primi 0,10 $ altı kontratta 0,25 $, diğerlerinde 0,50 $. Sayfa yalnızca call/put **alımını** anlatıyor. Kapalı pozisyon (covered), spread ve çıplak yazım belirtilmemiş. Alım gücü yetmezse vade günü kapanıştan 30 dk önce otomatik satış. | ABD için kredi/açığa satış sayfada yok. BIST kredi faizi yıllık %48,5–66,5 (bakiyeye göre). | https://www.getmidas.com/ucretler/ ; https://www.getmidas.com/abd-opsiyonlari/ (kurum sayfası, Kasım 2026'da okundu) |
| **İş Yatırım (TradeMaster International / İşCep)** | **%0,25, min. 1 $.** Sayfadaki örnekler 0,95 $ min. gösteriyor (çelişki). Komisyon üzerine %5 BSMV. | Sayfada yok (doğrulanamadı) | Sayfada yok | https://trademaster.com.tr/yurtdisi/uluslararasi-piyasalar-islem-komisyonlari (kurum sayfası) |
| **Garanti BBVA Yatırım** | **%0,30 (binde 3), minimum yok.** Örnek: 1.000 $'lık işlemde 3 $. Yurt dışı hesap için yurt içi pay hesabı şart. | Sayfada yok. Ürünler: hisse, ETF, yabancı hisse fonu. | Sayfada yok | https://www.garantibbvayatirim.com.tr/urunlerimiz/yurt-disi-hisse-pay-senedi (kurum sayfası) |
| **Gedik** | Resmi tarife bulunamadı. Üçüncü taraf kaynağa göre 15 ülkede 32 piyasa. | Doğrulanamadı | Doğrulanamadı | VT Markets karşılaştırması (ikincil, düşük güven) |

**Çıkarım (swing maliyeti, tek pozisyon 20.000 $):**
- Garanti: tek yön ~63 $ (BSMV dahil, varsayım), gidiş-dönüş **~63 baz puan**.
- İş/TradeMaster: gidiş-dönüş **~52 baz puan**.
- Midas: **~1,5 baz puan**.
- IBKR Pro Fixed (400 adet × 50 $): gidiş-dönüş **~2 baz puan**.

Yıllık 40 işlem yapan bir swing trader için oransal tarifeler **~20–25 puanlık** bir sürtünme demektir. Bu tek başına edge'in tamamını yiyebilir.

### 1.2 Interactive Brokers (IBKR)

- **Erişim:** IBKR'nin "Available Countries and Territories" sayfasında **Turkey** listede (sayfa 6.11.2026'da okundu): https://www.interactivebrokers.com/en/accounts/open-account-country-list.php (kurum sayfası).
  - Taranan ikincil kaynaklarda 2025–26'da Türk yerleşiklere yönelik bir kısıtlama haberi çıkmadı.
  - SPK'nın erişim engelleri lisanssız forex, CFD ve kripto sitelerine yönelik. Bu bulgu ikincil kaynaklara dayanıyor.
  - IBKR'nin SPK lisansı yok, dolayısıyla yerel başvuru veya koruma mekanizması da yok. Yatırımcı koruması, hesabın bağlı olduğu IBKR kuruluşuna göre değişir. Türk müşterilere hangi kuruluşun atandığı doğrulanamadı.
- **Komisyon (IBKR Pro):**
  - Fixed: **0,005 $/adet, min. 1 $, en fazla işlem değerinin %1'i.**
  - Tiered: 0,0035 $/adet (≤300 bin adet/ay), min. 0,35 $ + borsa/takas ücretleri.
  - IBKR Lite (0 $ komisyon) **yalnızca ABD yerleşiklerine** açık.
  - Kaynak: https://www.interactivebrokers.com/en/pricing/commissions-stocks.php (kurum sayfası).
- **Opsiyon:** **0,65 $/kontrat** (prim ≥0,10 $), emir başına min. 1 $. Doğrudan yönlendirilen emirde 1 $/kontrat. https://www.interactivebrokers.com/en/pricing/commissions-options.php
- **Kredi (margin) faizi:**
  - USD, 0–100 bin $ dilimi: **%5,38 (BM + %1,5)** Pro, %6,38 Lite.
  - 100 bin–1 mn $ dilimi: %4,88 (BM + %1). Benchmark örtük olarak ~%3,88, bu da efektif fed funds ile tutarlı.
  - Boş nakde **%3,38** faiz ödeniyor.
  - Kaynak: https://www.interactivebrokers.com/en/trading/margin-rates.php (kurum sayfası).
  - TL kredisiyle karşılaştırma: Midas'ta BIST kredi faizi %48,5–66,5. USD kaldıraç TL'ye göre ~10 kat ucuz. Ancak Türk vergisinde **kredi faizi kazançtan düşülemez** (Yapı Kredi notu, aşağıda).
- **Piyasa verisi:** "US Securities Snapshot and Futures Value Bundle" **ayda 10 $** (non-pro). Opsiyon (OPRA) ve akış paketleri ayrıca ücretli. https://www.interactivebrokers.com/en/pricing/market-data-pricing.php
- **Tereke (estate) vergisi riski:** ABD dışında yerleşik ve ABD vatandaşı olmayan biri öldüğünde, **ABD'de bulunan varlıkları 60.000 $'ı aşıyorsa** Form 706-NA verilmesi gerekir. ABD hisseleri ABD varlığı sayılır.
  - Kaynak: https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-us-assets-must-file-estate-tax-returns (resmi).
  - Türkiye–ABD arasında tereke vergisi anlaşması yok (bilgim bu yönde; IRS listesinden ayrıca teyit edin).
  - Swing trader için pozisyon sürekli açık olmadığından risk düşük. Yine de nakdin ve pozisyonların ABD'de durduğu unutulmamalı.

### 1.3 W-8BEN ve temettü stopajı

- ABD–Türkiye çifte vergilendirmeyi önleme anlaşması, Madde 10/2:
  - Portföy temettülerinde (oy hakkının %10'undan az pay) kaynakta en fazla **%20**.
  - Oy hakkının ≥%10'una sahip **şirket** pay sahiplerinde **%15**.
  - Kaynak: https://www.irs.gov/pub/irs-trty/turkey.pdf (resmi anlaşma metni).
  - W-8BEN verilmezse stopaj %30.
- W-8BEN imzalandığı yıldan sonraki 3. takvim yılının sonuna kadar geçerlidir (IRS form talimatı; genel bilgi).
- Sermaye kazancı ABD'de vergilenmez (Madde 13; ABD'de 183 günden az bulunan yerleşik olmayan kişi).
- Açığa satışta temettü yerine yapılan "substitute payment" ödemelerinde de stopaj kesilir.
- Türkiye tarafı (§2.1):
  - Yabancı temettü 2026'da **22.000 TL'yi aşarsa tamamı** beyan edilir. Yurt içi temettüdeki %50 istisna yabancı temettüye uygulanmaz.
  - ABD'de kesilen %20, GVK 123'e göre mahsup edilebilir. Bunun için mahallinde tasdikli belge gerekir.
  - Kaynak: https://www.yapikredi.com.tr/medium/file/yabanci-hisse-senedi-gelirlerinde-2026-yili-vergi-durumu_71999/view (banka yayını, 01.01.2026 mevzuatı).
  - **Swing trader için temettü önemsizdir.** Asıl konu sermaye kazancıdır.

### 1.4 Opsiyon onayı, margin, PDT, açığa satış, takas

- **Opsiyon onayı:** IBKR'de opsiyon izni, beyan edilen bilgi/deneyim ve hesap tipine bağlıdır.
  - Spread ve yazım için margin hesabı gerekir. Çıplak call yazımı en üst seviyedir.
  - Kesin eşikler bu çalışmada kaynakla doğrulanmadı.
  - Türk aracı kurumlarda ABD opsiyonunu belgeli olarak yalnızca Midas sunuyor ve sayfada yalnızca uzun (long) pozisyon görünüyor.
- **Margin (Reg T):** Başlangıç teminatı %50, sürdürme teminatı genelde %25. IBKR volatil hisselerde daha yüksek oran uygular.
  - Portföy marjini için IBKR ~110 bin $ özsermaye ister (IBKR kuralı, bu çalışmada teyit edilmedi).
  - FINRA notuna göre 5 mn $ altındaki portföy marjini hesaplarında gün içi risk için de gün sonuna benzer teminat tutulmalı.
- **PDT kuralı (FINRA Rule 4210):**
  - SEC onayı: **14.04.2026** (Release No. 34-105226, 91 FR 20731, dosya SR-FINRA-2025-017).
  - **Yürürlük: 04.06.2026.** Aracı kurumlar **20.10.2027'ye kadar** geçiş yapabilir.
  - Gün içi işlem sayımı, "pattern day trader" sınıflandırması ve **25.000 $ asgari özsermaye kaldırıldı.** Yerine risk bazlı "intraday margin deficit" rejimi geldi.
  - Bu açık en geç 15. iş günü kapanışına kadar kapatılmalı. Alışkanlık haline getiren müşteriye 90 gün dondurma uygulanır. Özsermayenin %5'ini veya 1.000 $'ı (hangisi küçükse) aşmayan açıklar hariç.
  - Kaynak: https://www.finra.org/rules-guidance/notices/26-10 (düzenleyici, 20.04.2026).
  - **Bu kullanıcı için anlamı:** Gün içi işlem yapmadığı için PDT zaten bağlayıcı değildi. Küçük hesapta aynı gün stop olup yeniden girişi kolaylaştırır, o kadar. Bazı aracı kurumlar eski kuralı 2027'ye kadar uygulayabilir.
- **Açığa satış:** ABD'de Reg SHO kapsamında ödünç bulma (locate) zorunlu. IBKR margin hesabında açığa satış var; ödünç ücreti hisseye göre değişir ve zor bulunan hisselerde çok yüksek olabilir.
  - Türk aracı kurumlarda ABD açığa satışı belgelenemedi. Fiilen IBKR'ye özgü bir imkân.
  - Swing short alternatifi: put alımı (Midas'ta da mümkün) veya ters ETF.
- **Takas:** ABD hisselerinde **T+1, 28.05.2024'ten beri.** SEC kararı 15.02.2023: https://www.sec.gov/news/press-release/2023-29 (resmi; tarih genel bilgi).
  - Nakit hesapta "good faith violation" riski T+1 ile azaldı. Satış parası ertesi gün kullanılabilir.

### 1.5 Seans saatleri (TSİ)

- ABD'de yaz saati 1 Kasım 2026'da bitti. Kış döneminde NYSE/Nasdaq normal seansı **17:30–24:00 TSİ**.
- Kapanış sonrası bilanço açıklamaları TSİ 00:05'ten sonra gelir.
- Pratikte giriş-çıkış kararları gece yarısına kayar. Bu, uyku ve disiplin maliyeti yaratır. Kapanışa yakın emir veya gün sonu (MOC) tipi emirlerle yönetilmeli.

---

## 2. Türkiye'de vergilendirme (bireysel, 2026)

### 2.1 Yurt dışı menkul kıymet kazancı (ABD hisse, ETF, opsiyon)

- **Nitelik:** Değer artışı kazancı (GVK mükerrer 80). Yurt dışı borsadaki alım-satım kazancı **tutarı ne olursa olsun** yıllık beyannameyle bildirilir. İstisna ve beyan sınırı yoktur.
  - GİB örneği: 2025'te yurt dışı hisseden 225.000 TL kazanç → beyan.
  - Kaynak: GİB "Diğer Kazanç ve İratlar 2026" rehberi, https://intvrg.gib.gov.tr/hazirbeyan/assets/pdf/DUYURU_UNIVERSAL_2026_Diger_Kazanc_ve_Iratlar_2026.pdf (resmi, 2026).
- **Hesaplama:** Alış ve satış bedeli o günlerin kurlarıyla TL'ye çevrilir. **Kur farkı vergiye tabidir.** USD bazında zarar edilse bile TL bazında kâr varsa vergi doğar (Yapı Kredi notu, banka yayını).
- **Endeksleme:** Alış ayı dahil, satış ayı hariç Yİ-ÜFE artışı **≥%10** ise maliyet endekslenir (GİB rehberi §1.2.1, GVK mükerrer 81).
  - Ekim 2026 Yİ-ÜFE: aylık %1,65, yıllık %27,41. %10 eşiği için **~6 ay** elde tutmak gerekir.
  - **Birkaç günden birkaç haftaya swing pozisyonlarda endeksleme pratikte hiç uygulanmaz.** Kur artışının tamamı vergilenir.
  - TÜFE/Yİ-ÜFE kaynağı: haber derlemesi (cumhuriyet.com.tr, aa.com.tr, 3.11.2026).
- **Zarar mahsubu:**
  - Aynı yıl içinde yabancı para menkul kıymet kâr ve zararları netleşir: yabancı hisse, yatırım fonu, Eurobond. Kanunda açık hüküm yok; Maliye basın açıklamasına dayanır (Yapı Kredi notu, dipnot 4; GİB rehberi örnek 16).
  - Zarar, kira ve serbest meslek gibi diğer gelir unsurlarından düşülemez (GVK 88).
  - **Net zarar sonraki yıla devredilemez** (uygulayıcı yazıları, muhasebetr.com; GİB rehberi "diğer kazanç ve iratlardan doğan zararlar diğer gelir unsurlarından mahsup edilemez"). Kötü bir yıl, önceki iyi yılın vergisini geri getirmez.
- **İndirilebilir giderler:** Komisyon ve saklama gibi doğrudan giderler indirilebilir. **Kredi (margin) faizi indirilemez** (Yapı Kredi notu).
- **Tarife (2026 kazancı, Mart 2027'de beyan, ücret dışı gelir):**

  | Dilim | Oran |
  |---|---|
  | 190.000 TL'ye kadar | %15 |
  | 190.000–400.000 TL | %20 |
  | 400.000–1.000.000 TL | %27 |
  | 1.000.000–5.300.000 TL | %35 |
  | 5.300.000 TL üstü | %40 |

  - 332 Seri No.lu GV Genel Tebliği, RG 31.12.2025. Kaynak: https://www.alomaliye.com/2025/12/31/2026-yili-vergi-dilimleri/ (ikincil mevzuat derlemesi; kümülatif tutarlar yeniden hesaplanıp tutarlı bulundu).
- **Ödeme:** Beyan Mart'ta. Vergi Mart ve Temmuz'da iki taksit. Değer artışında geçici vergi yok. Kazanç yıl içine yayılmışsa ortalama gecikme ~11 aydır. %35 TL faizle bugünkü değer çarpanı **~0,76**: vergi TL cinsinden sabitlenir ve enflasyonla erir.
- **Risk:** İşlem sıklığı ve organizasyon "ticari kazanç" iddiasına dayanak olabilir. Bu durumda defter tutma ve geçici vergi gündeme gelir. Bu çalışmada bunun aracı kurum üzerinden işlem yapan bireylere uygulandığına dair bir örnek bulunmadı. Belirsizlik olarak not edildi.
- **Vadeli/opsiyon (yurt dışı):** Genel yorum değer artışı yönünde. Kur farkı ve beyan aynı mantıkla işler. Bu çalışmada özelgeyle doğrulanmadı.

### 2.2 BIST payları

- **Bireyin BIST pay alım-satım kazancı:** Geçici 67 kapsamında **%0 stopaj** (2008/14272 BKK). Yıllık veya münferit beyan **yok.**
  - Bir yıldan uzun elde tutulan paylarda tevkifat da yok, mükerrer 80 de uygulanmaz.
  - Menkul kıymet yatırım ortaklığı (MKYO) payları hariç.
  - Kaynak: GİB "Geçici 67 Uygulama Rehberi 2026", https://cdn.gib.gov.tr/api/gibportal-file/file/getFileResources?objectKey=arsiv%2Ffileadmin%2Fbeyannamerehberi%2F2026%2F2026_Gecici67.pdf, §12.2 (resmi, 2026).
- **Geçici 67'nin süresi:** 11.12.2025 tarihli Cumhurbaşkanı Kararı ile **31.12.2030'a uzatıldı.** Kaynaklar: https://www.stb-cpaturkey.com/gelir-vergisi-kanunu-gecici-67-madde-11-aralik-2025/ ve Grant Thornton sirküleri (ikincil, profesyonel).
- **Stopaj/işlem vergisi teklifi:**
  - 27.07.2026'da "borsa kazancına vergi" söylentisi piyasayı oynattı. Hazine ve Maliye Bakanlığı resmi bir yalanlama yapmadı.
  - Cumhurbaşkanının %0'ı %40'a kadar çıkarma yetkisi var, ancak bu yetkiyi kullanan bir karar bulunamadı.
  - Kaynak: https://www.malumatfurus.org/borsa-vergi/ (doğrulama sitesi, ikincil).
  - Ekim 2026 tarihli bir rehbere göre **yürürlükte bir işlem vergisi yok** (ikincil).
  - **Durum:** %0 sürüyor. Kuyruk riski: tek bir Cumhurbaşkanı Kararı.

### 2.3 VİOP

- **Pay ve pay endeksine dayalı** vadeli ve opsiyonlar: **%0.**
- **Diğerleri:** döviz (F_USDTRY), altın, emtia, faiz vb. **%10 nihai stopaj** (2009/14580 BKK). Tam ve dar mükellef gerçek kişiler için geçerli.
- Kaynak: GİB Geçici 67 Rehberi 2026, §19 (resmi).
- **Komite raporundaki açık soruya cevap:** Short F_USDTRY carry kazancı **%10 stopaja tabidir.** Yıllık ~10–16 puanlık carry net ~9–14 puana iner.

### 2.4 Fonlar, mevduat, DİBS

- **TL mevduat:** Vadesiz ve 6 aya kadar **%17,5**, 1 yıla kadar %15, 1 yıldan uzun %10.
  - 10041 sayılı Karar (9.7.2025). Süresi 11444 sayılı Kararla (RG 20.06.2026, sayı 33286) **31.12.2026'ya** uzatıldı.
  - Kaynaklar: GİB Geçici 67 Rehberi; https://parafomo.com/blog/stopaj-nedir-2026-stopaj-oranlari/ (ikincil, 15.10.2026).
  - **Yıl sonunda oranlar değişebilir. Takvim riski var.**
- **Yatırım fonları (PPF dahil):** 9.7.2025'ten sonra alınan paylarda **%17,5** (10041). 1.2–8.7.2025 arası alımlarda %15 (GİB rehberi §20).
  - **Hisse yoğun fon (TEFAS'ta işlem gören): %0.**
  - TEFAS dışı serbest hisse yoğun fon: 27.03.2026'dan itibaren alınan paylarda %17,5 (11107).
- **11734 sayılı Karar (RG 5.9.2026):** PPF ve unvanında "para piyasası" geçen serbest fonlarda **kurumlar** ve kurumsal yatırımcılar için oran %0'dan %10'a çıktı. **Gerçek kişileri kapsamıyor.**
  - Kaynak: https://t24.com.tr/yazarlar/murat-bati/para-piyasasi-fonlarina-yuzde-10-stopaj-geldi,58885 ve https://www.kardemymm.com.tr/... (profesyonel, ikincil).
  - Uyarı: Bazı haber siteleri bu kararı "PPF stopajı %10 oldu" diye yanlış genelliyor.
- **DİBS ve hazine bonosu:** %0 (indirimli oran 31.12.2026'ya uzatıldı).
- **Önemli çıkarım (yüksek gelirli birey için):**
  - TEFAS'taki **yabancı hisse fonları** %17,5 nihai stopajla vergilenir. Doğrudan ABD hissesi ise %35–40 marjinal oran ve kur farkı vergisi öder.
  - Pasif ABD maruziyeti için fon yolu vergi açısından üstün. **Tekil hisse swing'inde bu yol yok.**

### 2.5 Döviz alımı

- **Kambiyo BSMV: binde 2 (%0,2)** döviz alımında alınır, satışta alınmaz. Kaynaklar: https://www.hangikredi.com/bilgi-merkezi/kambiyo-vergisi-nedir/ ve faturaport (ikincil).
- "17.03.2026'da değişti mi" sorusu çelişkili kaldı. Oran 2020'den beri binde 2 görünüyor.
- TL→USD dönüşümünde tek seferlik 20 baz puan.
- **Bireyin elinde tuttuğu dövizin kur kazancı vergilenmez.** Döviz menkul kıymet değildir. Menkul kıymet içindeki kur kazancı ise vergilenir (§2.1).

### 2.6 Vergi öncesi gerekli getiri: venue karşılaştırması

**TL tarafı (6.11.2026):**
- 32 gün vadeli 100 bin TL için banka ortalaması: yıllık brüt %39,58 (yatirimci.ai, 28.10.2026, ikincil).
- Net (%17,5 stopaj): basit %32,65, aylık yenilemeyle **efektif ~%38,0.**
- PPF: Ekim brüt aylık %3,02 (İş Portföy PPF, kurum sayfası https://www.isportfoy.com.tr/getiri-ve-fiyatlar).
  - Yıllıklandırılmış brüt %42,9, %17,5 sonrası net **~%34,4.**
  - Bu rakam "fiyat brüt mü" sorusunu açık bırakıyor. TEFAS fiyatı fon giderleri sonrası, stopaj öncesidir.
- **Reel karşılıklar** (Ekim TÜFE %29,77): politika ex-post %4,8, PPF net ~%3,6, mevduat net ~%6,3.
- **Merkezi TL eşiği h ≈ %35 net.**

| Venue / araç | Vergi | Gereken vergi öncesi getiri (h=%35 net'i yenmek için) |
|---|---|---|
| BIST spot pay | %0 | **≥%35 TL nominal** + işlem maliyeti. USD cinsinden, kur artışı d=%20 iken ≥%12,5. |
| VİOP pay/endeks vadeli | %0 | Vadeli fiyatı TL faizini içerir (baz). Teminat getiri kazanıyorsa (PPF/DİBS teminatı; aracı kurumdan teyit) eşik **sıfırın üstünde fazla getiri (excess return)**. Teminat nakitte bekliyorsa eşik teminat × h. |
| VİOP döviz/emtia | %10 | Brüt kazanç ≥ net hedef / 0,90 |
| TEFAS yabancı hisse fonu | %17,5 | ≥%42,4 TL nominal (=0,35/0,825) |
| **Doğrudan ABD hisse/opsiyon** | %15–40 (artan oranlı) + kur farkı vergisi | Aşağıdaki tablo |

**Doğrudan ABD için formül.**
Tanımlar:
- R: vergi öncesi USD getirisi
- d: yıllık USDTRY artışı
- u: yatırımda kalma oranı (pozisyonların açık kaldığı zamanın payı)
- t: efektif vergi oranı
- pv: verginin bugünkü değer çarpanı

Formül: R = (1+h − t·pv) / ((1+d) − t·pv·(1+d)^u) − 1

h = %35 için gereken R:

| d | Vergisiz | t=%27 | **t=%35** | t=%40 | t=%35, u=0,6 | t=%35, pv=0,76 | t=%35, u=0,6, pv=0,76 |
|---|---|---|---|---|---|---|---|
| %15 | %17,4 | %28,6 | **%33,8** | %37,7 | %30,0 | %28,4 | %25,9 |
| %20 | %12,5 | %23,3 | **%28,2** | %31,9 | %23,5 | %23,1 | %20,0 |
| %25 | %8,0 | %18,4 | **%23,1** | %26,7 | %17,7 | %18,1 | %14,6 |
| %30 | %3,8 | %13,8 | **%18,3** | %21,8 | %12,3 | %13,6 | %9,6 |

**Somut örnek (2026 tarifesi, başka gelir yok):**
- Varsayım: 100.000 $ sermaye, kur 50,05, R = +%30 USD, d = %20, tam yatırımda.
- TL kazanç: 2,80 mn TL. Vergi: 863 bin TL (ortalama %30,8) = yıl sonu kuruyla **14.377 $.**
- Bu, **USD kârının %47,9'u** eder. Sebebi kur farkının da vergilenmesidir.
- Vergi sonrası: 115,6 bin $ = **TL bazında +%38,7.** Ertelemenin bugünkü değeriyle +%42,9.
- Kıyas: TL nakit net ~%34–38.
- **Sonuç: Yılda +%30 USD kazandıran bir ABD swing stratejisi, TL nakdi ancak başa baş ile birkaç puan arasında geçiyor.** Vergisiz "%12,5 yeter" hesabı yanıltıcı.
- Not: Hesap, BSMV, komisyon ve kayıp yıllarında zararın devredilememesi etkilerini içermiyor. Bunlar eşiği yükseltir.

---

## 3. ABD piyasasının durumu (5–6 Kasım 2026)

### 3.1 Seviyeler

Kaynaklar:
- Kapanış verileri: https://cappnotes.substack.com/p/closing-look-thursday-november-5 (bülten, ikincil) ve https://www.stocktitan.net/articles/stock-market-today-live-november-5-2026 (haber).
- Seriler: FRED SP500, NASDAQCOM, VIXCLS, DTB3, DGS2, DGS10 (resmi istatistik): https://fred.stlouisfed.org/
- 2025 kapanışı: S&P 6.845,50, Nasdaq 23.241,99 (marketscreener ve HL, haber).

| Gösterge | Değer |
|---|---|
| S&P 500, 5.11 | **7.353,73** (−%4,36; Nisan 2025'ten beri en kötü gün) |
| S&P yılbaşından beri / rekordan | **+%7,4** / **−%5,95** (rekor 7.818,93, 6.10.2026; 2026'nın 28. rekor kapanışı) |
| S&P 50 / 200 günlük ortalama | ~7.687 / **~7.323** (fiyat 200 günlüğün %0,4 üstünde) |
| S&P Ekim ayı | −%0,9 (7.651,54 → 7.580,07). Nasdaq Ekim: −%5,3 |
| 2026 maksimum düşüş | −%9,1 (dip 30.03.2026, 6.343,72; İran savaşı/petrol dönemi) |
| Nasdaq Comp. | **24.315** (−%5,52), rekordan **−%11,9**, 200 günlüğün ~%3 altında. Nisan'dan beri ilk kez 200 günlüğün altı. Yılbaşından beri +%4,6. |
| Nasdaq-100 / SMH / Russell 2000 | 26.629,81 (−%6,36) / −%11,2 / 2.729,89 (−%4,45) |
| Genişlik, 5.11 | S&P'de 71 yükselen / 431 düşen. Eşit ağırlıklı RSP −%2,89 (endeksten iyi) |
| VIX | **28,18** (+%69,7). 2026 ortalaması 18,1, medyanı 17,2. VIX>20 günlerin %18,3'ü, >25 %6,4'ü, >30 %0,9'u. Yıl zirvesi 31,05 (27.03). |
| Gerçekleşen volatilite (S&P, 2026) | Yıllık %13,0. Mutlak değeri %2'yi aşan gün sayısı yalnızca 4 (5.11 öncesi) |
| Getiri eğrisi (4–5.11) | 4 hafta 3,85, 3 ay **4,03**, 6 ay 4,14 (iskonto bazı). 2 yıl 4,46–4,58, 10 yıl 4,84–4,90. 2s10s ~+38 baz puan. |
| Emtia/kur | Brent 98,29 $ (5.11, +%3,8; önceki gün −%8). Ekim sonunda 115 $'ın üstündeydi. Altın ~4.098 $. DXY 101,6 |

**Tetikleyici (4–5 Kasım):**
- Ara seçimlerde Demokratlar Kongre'yi kazandı.
- Veri merkezi düzenlemesi korkusu ve zayıf çip bilançoları ortaya çıktı.
- Düşüşler: Micron −%17,5, AMD −%17,3, Marvell −%16,4, Arm −%13,1, NVDA −%9,3.
- Kazananlar: AppLovin +%31 (bilanço), Cloudflare seans sonrası +%17, Airbnb seans sonrası +%7.

### 3.2 Fed, enflasyon, büyüme

- **FOMC 28.10.2026:** Hedef aralık **3,75–4,00** sabit. Oylama **10–2.** Cook ve Hammack 25 baz puan **artırım** istedi.
  - Metin: "Economic activity is expanding at a strong pace … Inflation remains elevated … The Committee will deliver price stability."
  - Rezerv faizi (IORB) %3,90, ON RRP %3,75, SRF %4,0.
  - Kaynak: https://www.federalreserve.gov/monetarypolicy/files/monetary20261028a1.pdf (resmi).
- 16–17.09.2026'da 25 baz puan artırım yapılmıştı (ikincil haber; FOMC metni aralığın değişmediğini teyit ediyor).
- Başkan Kevin Warsh. Aralık artırım olasılığı 28.10'da %82,6'ydı, 5.11'de ~%66–70'e indi (CME FedWatch, haber üzerinden). Sonraki karar 9.12.2026.
- **Eylül TÜFE (ABD):** manşet %3,7, çekirdek %2,6 (aylık +0,3). Benzin endeksi aylık +%9,1 (İran savaşı).
  - Kaynak: https://www.cnbc.com/2026/10/14/cpi-inflation-breakdown-september-2026.html (haber). Ekim TÜFE 10.11.2026'da açıklanacak.
- 3. çeyrek verimlilik +%3,6 (yıllıklandırılmış), birim işgücü maliyeti −%0,7. Haftalık işsizlik başvurusu 189 bin. Ekim istihdam beklentisi +65 bin, işsizlik %4,2 (cappnotes).
- **Rejim özeti:** Arz şoku kaynaklı manşet enflasyon ve güçlü yatırım/verimlilik var. Fed "şahin bekle" modunda. Uzun faiz ~%4,9 hisse değerlemesini sınırlıyor.

### 3.3 Bilanço sezonu ve değerleme

Kaynak: FactSet Earnings Insight, 30.10.2026, https://insight.factset.com/sp-500-earnings-season-update-october-30-2026 (endüstri veri sağlayıcı).

- Şirketlerin %60'ı açıkladı. **%82'si beklentiyi aştı** (5 yıllık ortalama %78).
- **Sürprizin büyüklüğü yalnızca %1,9.** 5 yıllık ortalama %7,5. Gerçekleşirse Q4 2022'den beri en düşük.
- Q3 harmanlanmış kâr büyümesi **+%30,2**: üst üste üçüncü çeyrek %25'in üstünde. Gelir büyümesi +%13,4.
- 2026 yılı kâr büyümesi beklentisi %32,9, Q4 beklentisi %28,4.
- 11 sektörün hepsi büyüyor. Kâr büyümesinde önde: enerji, bilgi teknolojileri, malzeme.
- **İleri 12 ay F/K 18,7.** 5 yıllık ortalama 19,8, 10 yıllık 19,1, 30.09'da 19,0. Kâr çok hızlı büyüdüğü için çarpan ortalamanın altında. Rallinin dayanağı kâr, çarpan genişlemesi değil.
- **Swing için anlamı:**
  - Beklentiyi aşmak artık fiyatlanmış durumda. Sürpriz küçük olduğu için "aşma ama sat" asimetrisi var: Arm, Qualcomm; seans sonrası Atlassian −%16, Axon −%14.
  - Gelir büyümesini ve yönlendirmeyi (guidance) belirgin aşan isimlerde gap-up sonrası sürüklenme hâlâ en temiz ayrışma kaynağı: APP, NET.

### 3.4 Liderlik, momentum çözülmeleri, kalabalık pozisyonlar

- **Temmuz 2026:**
  - MTUM'un S&P'ye göre 20 günlük göreli düşüşü **−%15,5**: fonun tarihindeki en büyük.
  - Momentum ile yarı iletken fazla getirisi arasındaki korelasyon Ağustos başında **0,95** (Mart'ta ~0,5).
  - BofA fon yöneticisi anketinde "long küresel yarı iletken" rekor **%82.**
  - Kaynak: https://www.lighthouse-canton.com/insights/momentum-interrupted-market-commentary/ (varlık yöneticisi yorumu, 27.10.2026).
  - Aynı dönem (RIA, 18.07.2026, uygulayıcı blogu): Goldman yüksek beta momentum sepeti Temmuz'un ilk yarısında −%24 (Nisan 2009'dan beri en kötü). Morgan Stanley teknoloji momentum endeksinde 17 günlük değişim −%35 (27 yılın en kötüsü). Asya'daki 2x tek hisse ETF'leri (SK Hynix) zorunlu satış yaptı. https://realinvestmentadvice.com/resources/blog/momentum-meltdown-catches-traders-by-surprise/
- **Ekim 2026 (23.10'a kadar):**
  - MTUM 20 günlük göreli **−%8,7** (tarihin dördüncü en büyüğü). SPMO/RSP −%12,1. SMH/SPY −%13,1.
  - **XLE/SPY +%13,1.** 22.10'da yarı iletken endeksi −%6,7 ve 30 hissenin hepsi düştü. 2008'den beri en uzun düşüş serisi: 8 seans.
  - Goldman prime brokerage portföyünde teknoloji payı %23,5 (5 yılın 90. yüzdeliği). Kalabalık işlem oranı %82'den %45'e indi.
  - Fiyatlar sabit kalırsa **enerji 2 ay içinde 12-1 momentumda yarı iletkenleri geçer** (Lighthouse).
- **Tarihsel istatistik:** 2013'ten beri momentum 20 günde S&P'nin ≥5 puan gerisinde kaldığı 10 epizottan yalnızca 3'ünde sonraki 3 ayda öne geçti (Temmuz 2026, Aralık 2021, Ocak 2023).
  - Goldman notu (RIA üzerinden, ikincil): momentum faktörü bir ayda >%20 düştükten sonra medyan getiri sonraki hafta ~+%4, sonraki ay ~+%6.
  - Birlikte okunduğunda: **kısa vadeli tepki sıçraması olası, ama liderliğin geri gelmesi olası değil.**
- **Akademik dayanak:**
  - Daniel & Moskowitz (2016), "Momentum crashes", *JFE* 122(2): Momentum çöküşleri **piyasa düşüşü ve yüksek volatilite sonrasındaki "panik" durumlarında**, piyasa toparlanırken kaybedenlerin sert yükselmesiyle olur. Dinamik ağırlıklandırma Sharpe oranını ~2 katına çıkarır. https://doi.org/10.1016/j.jfineco.2015.12.002 (hakemli).
  - Barroso & Santa-Clara (2015), "Momentum has its moments", *JFE* 116(1): Volatiliteye göre ölçeklenen momentumda Sharpe ~0,53'ten ~0,97'ye çıkar, çöküş riski düşer. https://doi.org/10.1016/j.jfineco.2014.11.010 (hakemli).

### 3.5 Bireysel yatırımcı katılımı ve IPO

- **Opsiyon hacmi:**
  - Q2 2026 günlük ortalama hacim **72,8 mn kontrat** (yıllık +%19).
  - Vadesi aynı gün dolan (0DTE) opsiyon hacmi yılbaşından beri +%46,2, günde 20 mn kontratın üstünde.
  - Tek hisse opsiyon hacmi yılbaşından beri +%6. NVDA ve TSLA'nın her biri tek hisse hacminin %9'u.
  - Kaynak: https://www.cboe.com/insights/posts/state-of-the-options-industry-options-market-continued-to-break-records-in-q-2-2026 (borsa verisi, 21.07.2026).
  - OCC verisiyle Ocak–Eylül 2026 ortalaması 70,6 mn/gün (+%20,6) (ikincil).
  - Citadel Securities: bireysel opsiyon platformunda "kayıtlardaki en yoğun Ekim" (ikincil; sayfa 403 verdi).
- **IPO (Renaissance Capital):**
  - 23.10'a kadar 118 IPO (−%34 adet), **148,3 mlr $** (+%362). Bu, 2021 rekorunu (142,4 mlr $) geçiyor. Ağırlık SpaceX'in ~75 mlr $'lık Haziran halka arzında.
  - **Ekim zayıf:** 8 IPO, 1,2 mlr $ (10 yıllık Ekim ortalaması 22 IPO, 5,1 mlr $). Renaissance IPO Endeksi Ekim'de **−%10** (S&P −%1). Ekim IPO'larının ~2/3'ü halka arz fiyatının altında.
  - Gündem: Anthropic'in IPO başvurusu (Renaissance tahmini ~75 mlr $, Kasım ortası bekleniyor).
  - Kaynak: https://www.renaissancecapital.com/IPO-Center/News/122531/renaissance-capital%E2%80%99s-october-ipo-market-update (endüstri verisi).

### 3.6 Bu rejim momentum ve breakout swing için ne anlama geliyor?

1. **Breakout'un temel koşulu (endeks yükseliş trendinde) bozuldu.**
   - Nasdaq 200 günlüğün altında ve düzeltmede. S&P 200 günlüğün tam üstünde. VIX 28 (yılın en üst ~%5'lik dilimi).
   - O'Neil/CAN SLIM tipi sistemlerin kendi kuralı bu koşulda yeni alımı durdurmaktır.
   - Lighthouse'un hipotetik trend katmanı son 4 büyük satışta MTUM düşüşlerini **5–11 puan** azaltmış.
   - **Kural:** Endeks 50 günlüğün altında ve VIX>25 iken brüt pozisyonu yarıya indir. Yeni breakout'u ancak endeksin trend toparlanmasını teyit eden bir gün sonrasında al.
2. **Liderlik el değiştiriyor.**
   - Yarı iletken ve yapay zeka altyapısı (bellek, optik, güç) 12-1 momentumda hâlâ 1. sırada. 3 aylık momentumda ise 9. sırada.
   - Enerji her iki ölçüde de yükseliyor (İran/Hormuz, Brent 90–115 $ bandı).
   - Kümelenme yapan bir trader için açık sonuç: **"AI çip kümesi"ni lider küme saymak gecikmeli bir sinyal.** 3 ay ile 12-1 ay momentum sıralamasını birlikte izle.
   - 5.11'de en az düşenler: enerji dışı defansifler (temel tüketim −%0,75, kamu hizmetleri −%0,71, iletişim −%0,59).
3. **Volatiliteye göre pozisyon boyutu zorunlu.**
   - Endeksin gerçekleşen volatilitesi 2026'da %13. Ama tek hisse kuyrukları yüksek: tek günde −%17 (MU, AMD), −%55 (MNTN).
   - Hedef: pozisyon başına risk = sermaye × %0,5–1, stop = 1,5–2 × ATR. VIX 28'de bu, 2026 ortalamasına (18) göre ~%35 daha küçük pozisyon demektir (yaklaşık oran 18/28).
4. **Bilanço sezonunun asimetrisi:** Beklentiyi aşma oranı yüksek, sürpriz küçük. Bilanço öncesi pozisyon taşımak negatif çarpıklıkta. Bilanço sonrası gelir ve yönlendirmeyi belirgin aşan isimlerde gap-up sürüklenmesi daha savunulabilir.
5. **Faiz:** 10 yıllık ~%4,9, Fed artırım eğilimli. Uzun vadeli (long-duration) büyüme hisselerinde çarpan baskısı var. Seçim sonrası düzenleme belirsizliği veri merkezi ve güç zincirinde (GEV, VST, FIX, CRWV) kalıcı bir risk primi yaratabilir.
6. **Mevsimsellik ve ara seçim istatistiği:** Ara seçim yıllarında Ekim kapanışından sonraki 12 ay 1950'den beri 19/19 pozitif (TradingView verisi, haber üzerinden). n=19, gözlemler bağımsız değil. **İşlem sinyali değil**, en fazla bir eğilim (bias).
7. **IPO tabanları:** Ekim'de yeni halka arzlar zayıftı. Anthropic IPO'su gibi büyük bir arz likiditeyi emebilir. IPO breakout stratejisi ancak bu arz başarılı olursa yeniden canlanır.

---

## 4. Bu kullanıcı için USD eşiği

### 4.1 Bileşenler

- **ABD risksiz:**
  - 3 aylık T-bill %4,03 (iskonto). Tahvil eşdeğer getirisi ~%4,1. 4 hafta %3,85, 6 ay %4,14 (FRED DTB3/DTB4WK/DTB6, 4.11.2026).
  - IBKR boş nakit faizi %3,38.
  - T-bill faizi Türkiye'de menkul sermaye iradı olarak beyana tabidir.
- **TL carry fırsat maliyeti:**
  - Sakin rejimde TL net h ≈ %35. Beklenen kur artışı d ≈ %20.
    - 2026 gerçekleşen hız ~%19–20 (komite raporu).
    - Ekim TCMB anketi yıl sonu kur beklentisi 51,55. 5.11 kuru 50,05'e göre +%3,0 (8 hafta, yıllık ~%21).
  - TL'de kalmanın USD getirisi: 1,35/1,20 − 1 ≈ **%12,5.** T-bill'e göre fazla getiri ~**8,5 puan.**
  - Komite tarihsel ölçümü: ortodoks dönemlerde 64 günde ortalama +%2,6 (yıllık ~%15,8), pencerelerin %88'i pozitif. 2018/2021/2023 şoklarında −%19 ile −%31.
  - Komite raporu: /home/user/Xxxx/raporlar/2026-10-28_viop_komite_raporu.md (iç kaynak).
  - Vadeli kur (F_USDTRY1226, 27.10): 52,516/49,76 → 64 günde +%5,54, basit yıllık ~%31,6. Piyasa, beklenen ~%20'nin üzerinde değer kaybını fiyatlıyor. Bu fark carry primidir.
- **USD stratejisinin eşiği (§2.6):**
  - Sakin rejim ve %35 dilim: **vergi öncesi ~%23–28 USD/yıl.**
  - Erteleme ve kısmi yatırımda kalmayla: **~%20.**
  - T-bill'in **+16 ile +24 puan** üstü.
  - Kullanıcının "%10 USD kabul edilemez" sezgisi doğru, ama gerekçesi farklı: reel faiz değil, **vergi ve kur farkı vergisi.**

### 4.2 TL devalüasyon kuyruğuna karşı USD maruziyetinin değeri

Senaryo: Sakin yılda d=%20, şok yılında d=%45 veya %60.

| Durum | TL'de kal (h=%35) | USD nakit/T-bill (%4), TL bazında |
|---|---|---|
| Sakin yıl (d=%20) | +%35 | +%24,8 → TL ~10,2 puan önde |
| Şok yılı (d=%45) | +%35 | +%50,8 → USD ~15,8 puan önde |
| Ağır şok (d=%60) | +%35 | +%66,4 → USD ~31,4 puan önde |

- **Başa baş şok olasılığı:** d=%45 için ~%39/yıl, d=%60 için ~%25/yıl.
- Son 8 yılda 3 büyük şok (2018, 2021, 2023) ve bir kontrol edilen şok (Mart 2025) yaşandı. Kaba sıklık **~%35–50/yıl.**
- **Yorum:** USD maruziyeti **kabaca adil fiyatlı bir sigorta.** Bedava değil, pahalı da değil. Dolayısıyla ABD stratejisinin sigorta değerini "ek getiri" sayıp eşiği düşürmek ancak kısmen meşrudur.
- **Vergi inceliği:** Bireyin elindeki dövizin kur kazancı vergisizdir. Menkul kıymet içindeki kur kazancı vergilidir. **Sigorta en verimli şekilde pozisyonlar arasında USD nakitte tutularak** elde edilir.
- Pratik sonuç: ABD hesabında boşta bekleyen nakit, hem sigorta hem %3,4–4 getiri sağlar. Hisse pozisyonunda tutulan süre boyunca oluşan kur artışı ise vergilenir.
- **Korelasyon:** TL şoklarında BIST/VİOP kümeleri genelde USD bazında çöker (Ekim 2026'daki −%22 gibi). ABD kümeleri ise TL'den bağımsızdır. ABD bacağının asıl katkısı bu **çeşitlendirme**, beklenen getiri değil.

---

## 5. ABD swing trader araçları ve maliyetleri (6.11.2026'da kurum sayfalarından)

| Araç | Ne için | Fiyat | Kaynak |
|---|---|---|---|
| **Finviz Elite** | Tarayıcı, gerçek zamanlı fiyat, seans öncesi/sonrası, backtest, uyarılar | **39,50 $/ay** veya **299,50 $/yıl** (yıllıkta ~24,96 $/ay). Ücretsiz sürüm gecikmeli. | https://finviz.com/elite |
| **TradingView** | Grafik, Pine, uyarılar. Kullanıcının mevcut altyapısıyla uyumlu (Pine göstergeleri). | Yıllık faturalamada aylık: Essential **12,95 $**, Plus **29,95 $**, Premium **59,95 $**, Ultimate **199,95 $**. Aylık faturalama daha pahalı (14,95/34,95/69,95 $). Borsa veri ücretleri ayrı. | https://www.tradingview.com/pricing/ |
| **MarketSurge** (eski MarketSmith, IBD) | RS sıralaması, CAN SLIM tabanları, kurumsal sahiplik | **149,95 $/ay** veya **1.499 $/yıl**. 30 gün deneme 24,95 $. | https://marketsmith.investors.com/ |
| **IBD Digital** | Liste ve "market pulse" (dağıtım günleri, endeks trend sinyali) | 34,95–49,99 $/ay (plana göre), **379 $/yıl**. İlk 2 ay 20 $. | https://www.investors.com/ibd-digital/ |
| **IBKR verisi** | Gerçek zamanlı ABD fiyatı | Snapshot ve vadeli paketi **10 $/ay**. OPRA ve akış paketleri ek. | https://www.interactivebrokers.com/en/pricing/market-data-pricing.php |
| Ücretsiz | Bilanço takvimi ve implied move, makro, faiz olasılıkları | Earnings Whispers, Nasdaq bilanço takvimi, SEC EDGAR (8-K/10-Q), FRED, CME FedWatch, FINRA açığa satış verisi (ayda iki kez) | (genel bilgi) |

- **Asgari ciddi set:** TradingView Plus/Premium + Finviz Elite + IBKR veri: **~80–110 $/ay** (~1.000–1.300 $/yıl). 100 bin $ sermayede bu ~1–1,3 puanlık sürtünme demektir.
- MarketSurge eklenirse **+1.500 $/yıl.**

---

## 6. Kaynak listesi (tür, tarih)

| # | Kaynak | Tür | Tarih |
|---|---|---|---|
| 1 | FINRA Regulatory Notice 26-10, https://www.finra.org/rules-guidance/notices/26-10 | Düzenleyici | 20.04.2026 |
| 2 | FOMC açıklaması, https://www.federalreserve.gov/monetarypolicy/files/monetary20261028a1.pdf | Resmi | 28.10.2026 |
| 3 | ABD–Türkiye vergi anlaşması, https://www.irs.gov/pub/irs-trty/turkey.pdf | Resmi (anlaşma) | 1996 (yürürlükte) |
| 4 | IRS yerleşik olmayanlar için tereke vergisi sayfası, https://www.irs.gov/individuals/international-taxpayers/some-nonresidents-with-us-assets-must-file-estate-tax-returns | Resmi | Güncel |
| 5 | GİB Diğer Kazanç ve İratlar Rehberi 2026, https://intvrg.gib.gov.tr/hazirbeyan/assets/pdf/DUYURU_UNIVERSAL_2026_Diger_Kazanc_ve_Iratlar_2026.pdf | Resmi | 2026 |
| 6 | GİB Geçici 67 Rehberi 2026, https://cdn.gib.gov.tr/api/gibportal-file/file/getFileResources?objectKey=arsiv%2Ffileadmin%2Fbeyannamerehberi%2F2026%2F2026_Gecici67.pdf | Resmi | 2026 |
| 7 | Yapı Kredi, "Yabancı hisse senedi gelirlerinde 2026 yılı vergi durumu", https://www.yapikredi.com.tr/medium/file/yabanci-hisse-senedi-gelirlerinde-2026-yili-vergi-durumu_71999/view | Banka yayını | 01.01.2026 mevzuatı |
| 8 | 2026 tarife (332 Seri No.lu Tebliğ), https://www.alomaliye.com/2025/12/31/2026-yili-vergi-dilimleri/ | İkincil mevzuat | 31.12.2025 |
| 9 | 11444 ve 11107 kararları, stopaj tablosu, https://parafomo.com/blog/stopaj-nedir-2026-stopaj-oranlari/ | İkincil | 15.10.2026 |
| 10 | 11734 kararı (PPF, kurumlar), https://t24.com.tr/yazarlar/murat-bati/para-piyasasi-fonlarina-yuzde-10-stopaj-geldi,58885 | Profesyonel yorum | Eylül 2026 |
| 11 | Geçici 67'nin 2030'a uzatılması, https://www.stb-cpaturkey.com/gelir-vergisi-kanunu-gecici-67-madde-11-aralik-2025/ | Profesyonel | Aralık 2025 |
| 12 | Borsa vergisi söylentisi, https://www.malumatfurus.org/borsa-vergi/ | Doğrulama sitesi | Temmuz 2026 |
| 13 | Kambiyo BSMV, https://www.hangikredi.com/bilgi-merkezi/kambiyo-vergisi-nedir/ | İkincil | 2026 |
| 14 | Midas ücretleri ve ABD opsiyonları, https://www.getmidas.com/ucretler/ ; https://www.getmidas.com/abd-opsiyonlari/ | Kurum sayfası | Kasım 2026 |
| 15 | TradeMaster komisyonları, https://trademaster.com.tr/yurtdisi/uluslararasi-piyasalar-islem-komisyonlari | Kurum sayfası | Kasım 2026 |
| 16 | Garanti BBVA Yatırım yurt dışı hisse, https://www.garantibbvayatirim.com.tr/urunlerimiz/yurt-disi-hisse-pay-senedi | Kurum sayfası | Kasım 2026 |
| 17 | IBKR ülke listesi, hisse/opsiyon komisyonu, margin faizi, veri sayfaları (bkz. §1.2) | Kurum sayfası | 6.11.2026 |
| 18 | FactSet Earnings Insight, https://insight.factset.com/sp-500-earnings-season-update-october-30-2026 | Endüstri verisi | 30.10.2026 |
| 19 | FRED (SP500, NASDAQCOM, VIXCLS, DTB3, DTB4WK, DTB6, DGS2, DGS10), https://fred.stlouisfed.org/ | Resmi istatistik | 4–5.11.2026 |
| 20 | 5.11 kapanışı, https://cappnotes.substack.com/p/closing-look-thursday-november-5 ; https://www.stocktitan.net/articles/stock-market-today-live-november-5-2026 | Bülten/haber | 5.11.2026 |
| 21 | Lighthouse Canton, "Momentum interrupted", https://www.lighthouse-canton.com/insights/momentum-interrupted-market-commentary/ | Varlık yöneticisi yorumu | 27.10.2026 |
| 22 | RIA, "Momentum meltdown…", https://realinvestmentadvice.com/resources/blog/momentum-meltdown-catches-traders-by-surprise/ | Uygulayıcı blogu | 18.07.2026 |
| 23 | Cboe, Q2 2026 opsiyon sektörü raporu, https://www.cboe.com/insights/posts/state-of-the-options-industry-options-market-continued-to-break-records-in-q-2-2026 | Borsa verisi | 21.07.2026 |
| 24 | Renaissance Capital, Ekim IPO raporu, https://www.renaissancecapital.com/IPO-Center/News/122531/renaissance-capital%E2%80%99s-october-ipo-market-update | Endüstri verisi | Kasım 2026 |
| 25 | CNBC, Eylül ABD TÜFE, https://www.cnbc.com/2026/10/14/cpi-inflation-breakdown-september-2026.html | Haber | 14.10.2026 |
| 26 | Daniel & Moskowitz (2016) JFE, https://doi.org/10.1016/j.jfineco.2015.12.002 ; Barroso & Santa-Clara (2015) JFE, https://doi.org/10.1016/j.jfineco.2014.11.010 | Hakemli | 2015–16 |
| 27 | TCMB 15:30 gösterge kuru 5.11.2026 (USD satış 50,0489), https://www.ensondakika.com.tr/tcmb-doviz-kurlari-5-kasim-2026/734815/ | Haber (TCMB verisi) | 5.11.2026 |
| 28 | Ekim TÜFE %29,77 / aylık %2,58, Yİ-ÜFE %27,41, https://www.aa.com.tr/tr/ekonomi/enflasyon-rakamlari-aciklandi/4109355 | Haber (TÜİK verisi) | 3.11.2026 |
| 29 | Mevduat ve PPF karşılaştırması, https://yatirimci.ai/fon/para-piyasasi-fonu-mu-mevduat-mi ; İş Portföy, https://www.isportfoy.com.tr/getiri-ve-fiyatlar | İkincil / kurum | 28.10–5.11.2026 |

---

## 7. Doğrulanamayanlar ve belirsizlikler

Web arama kotası çalışma sırasında doldu. Aşağıdakiler açık kaldı:

- İş Yatırım, Garanti, Gedik ve diğer kurumlarda ABD opsiyon, ABD kredisi ve açığa satış imkânı. Midas'ta opsiyon yazımı ve spread.
- Midas ve diğer kurumların döviz dönüşüm makası.
- Türk yerleşiklere atanan IBKR kuruluşu ve buna bağlı yatırımcı koruması. IBKR opsiyon izin seviyeleri. Portföy marjini eşiği.
- Yurt dışı vadeli/opsiyon kazançlarının vergi niteliği (özelge). Sık işlemde "ticari kazanç" iddiası riski.
- Kambiyo BSMV'nin 17.03.2026'da değişip değişmediği.
- Mevduat stopajının 01.01.2027 sonrası oranları (11444'ün süresi 31.12.2026'da doluyor).
- 6.11.2026 ABD istihdam verisi ve sonraki seans. Kasım ortası bilanço takvimi (NVDA vb.).
- ABD genişlik verileri çelişkili: 200 günlüğün üstündeki hisse oranı 4.11 için %68,9 (StreetStats), 21.10 için %54,7 (MacroMicro).
- Brent: komite tarihinde (Ekim sonu) >115 $, 5.11'de 98,29 $. Rakamlar farklı tarihlere ait.
