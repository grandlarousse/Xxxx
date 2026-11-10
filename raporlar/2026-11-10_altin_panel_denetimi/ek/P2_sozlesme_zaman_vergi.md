araç: 28/32

# P2: VİOP sözleşme, maliyet, vergi, TradingView referansı (10.11.2026)

Genel uyarı: Bulduğum resmî sözleşme belgeleri eski (2014 ve 2012 tarihli Borsa İstanbul kılavuzları). 2026 için güncel Borsa İstanbul sözleşme sayfasına ya da prosedüre ulaşamadım. Aşağıdakiler "eski belge + ikincil kaynak" düzeyindedir.

## Özet

F_XAUUSD (dolar/ons altın vadelisi):
- Büyüklük 1 ons, kotasyon USD/ons, fiyat adımı 0,05 USD (2014 kılavuzu ve GCM). Bir arama özeti 0,10 yazıyor; çelişki çözülmedi.
- Nakdi uzlaşma. Vade ayları Şubat, Nisan, Haziran, Ağustos, Ekim, Aralık. Vade sonu fiyatı: son işlem günü Londra öğleden sonra altın fiyatı (LBMA PM; 2014 metni "London Gold Fixing P.M.").
- Günlük uzlaşma: seans sonundan önceki son 10 dakikadaki işlemlerin miktar ağırlıklı ortalaması (10'dan az işlem varsa son 10 işlem). Yani kapanış fiyatı değil, uzlaşma farklı bir sayıdır.
- TL çevrimi: 2014 metnine göre TCMB 15:30 gösterge ABD Doları alış kuru. Güncelliği doğrulanmadı. (Kâr/zarar TL hesapta tahsil edilir; USD notional kur riski yaratır.)
- Günlük fiyat limiti ±%10 (2014 kılavuzu; baz fiyat önceki uzlaşma).
- Normal seans: aracı kurum kaynakları 09:30–18:15. Akşam seansı 19:00–23:00 ve Dolar/Ons Altın kapsamda (GCM rehberi; Borsa İstanbul 2024 duyurusu alıntısı arama özetinde). Akşam seansında ayrı uzlaşma fiyatı yok, fiyatlar normal seans uzlaşmasının ±%3'üyle sınırlı, kâr/zarar ertesi günün normal seans uzlaşmasına göre hesaplanır. Yarım günde, yılın son iş gününde ve vade sonunda akşam seansı yok.
- Başlangıç teminatı: SPAN ile belirlenir, sabit oran yok; GCM "yaklaşık 1:16 kaldıraç" diyor (yani kabaca %6, 2020 tarihli, değişir). Güncel teminat Takasbank'tan doğrulanmadı.
- Takas T+1: zarar T gün sonu tahsil, kâr T+1.

F_TRALT (Türk Altın İşletmeleri pay vadelisi; Darphane ya da altın sertifikası DEĞİL, bir hisse senedi):
- Çarpan 100 (Ekofin). Kasım 2026 vadesi 30.11.2026 (ayın son iş günü). Fiziki teslimat, T+3 (2014 kılavuzu). Vade sonu fiyatı: spot piyasada kapanış seansı fiyatı. Seans 09:30–18:10 (Borsa İstanbul broşürü, çelişkili kaynak 09:20). Günlük limit: 2022 işleyiş esaslarına göre ±%20 (2014'te de %20); benim ±%10 adayım kanıtlanmadı. Akşam seansı: pay vadelisi için akşam seansı kanıtı bulunmadı (GCM listesi yalnızca endeks ve kıymetli maden/bakır sayıyor). Pay vadelisi teminat oranı doğrulanmadı.
- Önemli: TRALT bir hisse. Altın ons fiyatına duyarlı ama şirkete özgü risk, temettü/pay işlemleri, BIST pay piyasası saatleri ve kendi kapanış seansı vardır; altın paneliyle günlük % değişimi uyuşmaması doğaldır.

Maliyet:
- Aracı kurum komisyonu: Borsa İstanbul alt ve üst sınır koyar, kademeli. Bir kurumun 2025 tarifesi (Strateji Yatırım): VİOP sabit binde 0,30, internet binde 0,20, borsa payı ilave. Fon bildirimlerinde onbinde 2 + BSMV görülüyor, yani aracı kurum başına çok değişken. Birden fazla kurum tarifesini doğrulayamadım (yalnız 1 kurum tarifesi, diğeri fon bildirimi).
- Borsa payı: pay endeksi vadelilerinde %0,004 (yüz binde 4) + BSMV yazılı bir banka belgesinde; kıymetli maden ve pay vadelisi oranı doğrulanmadı. Tarife dosyası (borsa-payi-ve-diger-ucretler-tarifesi.pdf) açılmadı.
- Gidiş-dönüş bps: kesin hesaplanamaz. Yalnız komisyon: binde 0,20 ila onbinde 2 taraf başına ise gidiş-dönüş yaklaşık 0,4 ila 4 bps + borsa payı + BSMV. Bu aralık kaba, onaylı değil. Asıl maliyet bid-ask ve uzlaşma-kapanış farkıdır.

Vergi:
- Pay/pay endeksi dışı VİOP sözleşmeleri (altın dahil): stopaj %10, nihai vergi (Borsa İstanbul vergilendirme sayfası, Akbank, Gedik 16.01.2024, Burgan). Pay ve pay endeksine dayalı (F_TRALT dahil): %0.
- Düzeltme: 9 Temmuz 2025 (10041 sayılı) kararıyla %15'ten %17,5'e çıkan oran VİOP işlem kazancına değil, teminat nema faizine ait. İşlem kazancı için %10 görünüyor. Ancak 12.11.2025 tarihli kaynak ve 2026 sonrası bir karar kontrol edilmedi; Kasım 2026 için %10 "büyük olasılıkla, resmî Resmî Gazete teyidi yok".
- Zarar mahsubu: Burgan, "Geçici 67/1 kapsamında" mahsup mümkün diyor; ayrıntı doğrulanmadı.

Saatler ve TradingView:
- ABD kış saati, NYSE/Arca TSİ saatleri, COMEX 13:30 ET uzlaşma, BIST pay kapanış seansı saatleri: DOĞRULANMADI (arama yapılmadı).
- Watchlist, Details ve Screener futures için her zaman uzlaşma (settlement) fiyatını kullanır; grafikte ise varsayılan seçenek "settlement as close" (günlük çubukta uzlaşmayı kapanış yap) ya da son işlem fiyatı olabilir (TradingView yardım sayfası). Bu, aynı sembolde bile grafikle liste arasında fark yaratabilir. Blog (13.03.2024) BIST için seçeneğin varsayılan olmadığını söylüyor, yardım sayfası ise varsayılan olarak açık diyor: çelişki.
- Günlük % değişim formülü için resmî TradingView sayfası bulunamadı (destek URL'si 404). GLD/GDX/GDXJ/PHYS için "önceki ABD seans kapanışı" adayım kanıtlanmadı. Gecikme süreleri (15 dk BIST, 10 dk CME) doğrulanmadı.
- Panelde değişim % tutmamasının doğrulanmış nedenleri: (1) uzlaşma ve son fiyat farklı referanslar, (2) VİOP uzlaşması son 10 dk ortalaması, (3) akşam seansı uzlaşmaya girmez ama fiyat hareketi gün içi görünür, (4) farklı seans saatleri, (5) PHYS kapalı uçlu fon, NAV'a göre prim/iskonto (Sprott: 7 Ağustos 2026'da -%2,33), GLD ETF yaratma/itfa mekanizmalı.
- GDXJ ile GDX farkı (küçük madenciler ve daha geniş sepet): aramada kaynak bulmadım; kendi bilgimdir, doğrulanmadı.

## İddia defteri

iddia | kaynak URL | alıntı/sayı | güven
Sözleşme 1 ons, kotasyon USD, adım 0,05 | https://www.borsaistanbul.com/files/viop-ozet-bilgiler-dokumani.pdf | "Minimum fiyat adımı 0,05'dır." (Kasım 2014) | orta (eski)
Adım 0,05 (aracı kurum) | https://www.gcmyatirim.com.tr/egitim/makaleler/ons-altin-usd-ons-xauusd-vadeli-islem-sozlesmesinde-islem-nasil-yapilir | "Minimum fiyat adımı 0,05'dir." | orta
Nakdi uzlaşma, vade ayları Şub-Nis-Haz-Ağu-Eki-Ara | https://www.borsaistanbul.com/files/viop-ozet-bilgiler-dokumani.pdf | "Şubat, Nisan, Haziran, Ağustos, Ekim ve Aralık" | orta (eski)
Vade sonu: Londra PM fiyatı | https://www.borsaistanbul.com/files/viop-ozet-bilgiler-dokumani.pdf | "The London Gold Fixing P.M." | orta (eski)
Günlük uzlaşma son 10 dk ağırlıklı ortalama | https://www.borsaistanbul.com/files/viop-ozet-bilgiler-dokumani.pdf | "son 10 dakika içerisinde gerçekleştirilen tüm işlemlerin miktar ağırlıklı ortalama fiyatı" | orta (eski)
Dolar kuru: TCMB 15:30 gösterge alış | https://www.borsaistanbul.com/files/viop-ozet-bilgiler-dokumani.pdf | "TCMB tarafından saat 15:30 itibarıyla açıklanan gösterge niteliğindeki ABD Doları Alış Kuru" | orta-düşük (2014)
Günlük limit ±%10 (altın) | https://www.borsaistanbul.com/files/viop-ozet-bilgiler-dokumani.pdf | "baz fiyatın ±%10'udur" | orta-düşük (2014)
Teminat SPAN | https://www.borsaistanbul.com/files/viop-ozet-bilgiler-dokumani.pdf | "SPAN portföy bazında teminatlandırma" | orta
Akşam seansı 19:00–23:00, altın kapsamda, ayrı uzlaşma yok, ±%3 | https://www.gcmyatirim.com.tr/egitim/makaleler/viop-aksam-seansi-rehberi | "Akşam seansında gerçekleştirilen işlemler için ayrı bir günlük uzlaşma fiyatı belirlenmez" | orta
Normal seans 09:30–18:15 | arama özeti (gcmyatirim.com.tr, isbank.com.tr eğitim) | "09:30-18:15" | orta
Teminat ~1:16 kaldıraç | GCM ons altın sayfası (yukarıdaki) | "kaldıraç oranının yaklaşık 1:16" | düşük (2020)
Stopaj hisse dışı %10, hisse/endeks %0 | https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/vergilendirme | "Pay ve pay endeksi dışındaki sözleşmeler %10" (sütun eşleşmesi belirsiz) | orta
Gedik %10 tevkifat, nihai | https://gedik.com/yazilar/vergilendirme/viop-kontrat-gelirlerinin-vergilendirilmesi | "%10 oranında tevkifat uygulanır" (16.01.2024) | orta (eski)
%17,5 nema faizine ait | https://www.muhasebetr.com/yazarlarimiz/huseyinergut/077 | "TPP, BPP ve VÖP nema faizi %17,50 (önceki oran %15)" (12.11.2025) | orta
Zarar mahsubu Geçici 67/1 | arama özeti (burgan.com.tr hisse-senedi-viop) | "Geçici 67/1" | düşük
TRALT çarpan 100, vade 30.11.2026 | https://ekofin.net/viop/F_TRALT1126 | "30 Kas 26", çarpan 100 | orta
Pay vadeli fiziki teslim, vade ayın son iş günü, ±%20 | https://www.borsaistanbul.com/files/viop-ozet-bilgiler-dokumani.pdf | "Fiziki teslimat"; "Her vade ayının son iş günü"; "±%20" (2014) | orta-düşük
Pay vadeli 09:30–18:10 | arama özeti (Borsa İstanbul broşürü) | "09:30 – 18:10" | düşük
Komisyon örneği binde 0,30 sabit / 0,20 internet | https://strateji.com.tr/wp-content/uploads/2025/12/Ucret-Masraf-ve-Komisyon-Bilgilendirilmesi-2025-12-04.pdf | "binde 0,30", "binde 0,20" (arama özeti) | orta
Borsa payı endeks vadeli %0,004 | arama özeti (banka dokümanı) | "%0,004" | düşük
TradingView: liste/Details/Screener uzlaşma kullanır | https://www.tradingview.com/support/solutions/43000685268-can-i-switch-settlement-and-last-prices-as-close-for-futures/ | "Watchlist, Details, and Screener always use settlement prices" (arama özeti) | orta
PHYS iskonto -%2,33 (7.8.2026) | https://sprott.com/investment-strategies/exchange-listed-products/physical-bullion-funds/gold/ | "-2.33%" (arama özeti) | orta

## Listemde olmayan önemli bulgu
- F_TRALT bir hisse vadelisi: %0 stopaj ve fiziki teslim buna bağlı. Altın duyarlılığı dolaylı.
- Akşam seansında ayrı uzlaşma yok ve ±%3 limit var; 17:55 TSİ giriş kararı ile 18:15 sonrası/akşam hareketi aynı uzlaşmaya girmez.
- Borsa İstanbul akşam seansı ve uzlaşma sayfası 2024 duyurusuna atıf yapıyor; sözleşme listesi değişebilir.

## Listemle çelişen kanıt
- %17,5 (Temmuz 2025) VİOP kazanç stopajı değil, nema faizi stopajı.
- Adım 0,05 vs 0,10: bir arama özeti 0,10 yazıyor.
- Pay vadeli limit ±%20 çıktı (aday ±%10/±%20 ikilisinden %20).
- Pay vadeli seans 09:30–18:10 ve altın 09:30–18:15 görünüyor; normal seans kapanışı kaynaklar arası çelişkili (09:20–18:10 de geçiyor).
- Arama özetinde "Ocak 2026 limit %20" iddiası çıktı; açtığım kaynak 27.10.2022 gram altın/döviz için tek günlük artış. Ons altın için kanıt değil.

## Açık kalanlar
- Güncel (2026) Borsa İstanbul sözleşme şartnamesi: adım, limit, seans, TL çevrim kuru.
- Takasbank güncel teminat (F_XAUUSD, F_TRALT).
- Borsa payı oranları (kıymetli maden ve pay vadeli) ve en az 2 kurum tarifesi; gidiş-dönüş bps.
- 2026'da stopaj oranı ve 10154 sayılı karar sonrası değişiklik; zarar mahsubu ayrıntısı.
- ABD kış saati, NYSE/Arca TSİ saatleri, COMEX 13:30 ET uzlaşma, BIST pay kapanış seansı.
- TradingView günlük % değişim formülü (GLD, GDX, GDXJ, PHYS, TVC:GOLD, COMEX:GC, VİOP) ve ücretsiz gecikme süreleri.
- GDXJ-GDX farkı kaynağı.
