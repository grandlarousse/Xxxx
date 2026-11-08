# r1_viop_kontrat — VİOP Dolar/Ons Altın (F_XAUUSD) vadeli sözleşmesinin işlem mekaniği

Tarih: 2026-11-07. Türkiye saati (TSİ) = UTC+3, yaz/kış değişikliği yok.
Ana birincil kaynak: **Borsa İstanbul VİOP Prosedürü, revizyon 70, revizyon tarihi 01/07/2026** (aşağıda "Prosedür"). PDF: https://borsaistanbul.com/files/borsa-istanbul-as-vadeli-islem-ve-opsiyon-piyasasi-proseduru.pdf
Kendi veri kontrollerim Borsa İstanbul'un günlük bülten CSV'lerine (`https://www.borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv`, akşam seansı için `viop_as_bul_YYYYMMDD.csv`) ve Dukascopy saatlik XAUUSD spot verisine dayanıyor.

---

## 0. Kısa özet (lead-lag için en kritik 8 nokta)

1. **"Kapanış" = günlük uzlaşma fiyatı**: normal seans bitmeden önceki **son 10 dakikadaki tüm işlemlerin miktar ağırlıklı ortalaması**. Tam iş gününde bu pencere **18:00:00–18:10:00 TSİ = 15:00–15:10 UTC**; yarım günde **12:30–12:40 TSİ = 09:30–09:40 UTC**. Akşam seansı uzlaşmaya girmez.
2. Kendi kontrolüm: Ekim 2026'da ön vade uzlaşma fiyatı, spot altının **15:00 UTC** değerine taşıma maliyeti kadar yakın (−0,5 ile +9,2 USD fark). 28.10.2026 yarım gününde ise uzlaşma 4054,4, spot 09:00–10:00 UTC bandı 4049,7–4055,8. Yani zaman damgası veriyle de doğrulanıyor.
3. **Akşam seansı 19:00–23:00 TSİ (16:00–20:00 UTC)**. Prosedüre göre akşam işlemleri "bir sonraki normal seans işlemi" sayılır (takas ve teminat T+1 günü sonunda). Borsa akşam seansı istatistiklerini **ayrı bir bültende, akşamın takvim tarihiyle** yayınlıyor. Ana bülten yalnızca normal seansı içeriyor.
4. **TradingView günlük çubuğu = normal seans + aynı günün akşam seansı.** 06.11.2026'da TV hacmi 21,02 bin. Bu, ana bülten (18.465) ile akşam bülteni (2.555) toplamına eşit. TV'de "settlement as close" ayarı kapalıysa günlük kapanış 23:00 TSİ'deki son işlem olabilir. Uzlaşmayla karıştırmayın.
5. **Vade sonu uzlaşma = LBMA Gold Price PM** (15:00 Londra). Kışın 18:00 TSİ, yazın 17:00 TSİ'ye denk gelir. **F_XAUUSD1226'nın son işlem günü 31.12.2026.** LBMA 2021–2025 arasında her yıl 31 Aralık'ta PM ihalesi yapmadı. Tekrarlanırsa sözleşme gereği **sabah (AM, 10:30 Londra) fiyatı** kullanılır. 2026 duyurusu henüz bulunamadı.
6. COMEX GC uzlaşması **13:29–13:30 ET** (kışın 21:29 TSİ, yazın 20:29 TSİ) ve FOMC gibi ABD öğleden sonra olayları VİOP uzlaşmasından **sonra** gelir. Bu yüzden "yabancı kapanış(T) → VİOP(T+1)" yönünde mekanik bir senkronsuzluk ilişkisi oluşur. Gerçek lead-lag için yabancı serileri **15:00–15:10 UTC'de** örnekleyin.
7. Maliyet: borsa payı yüzbinde 3 + Takasbank yüzbinde 1 (taraf başı). Aracı kurum komisyonu tarifelerde onbinde 0,9–binde 2 arası, üstüne %5 BSMV. Vergi: yerleşik gerçek kişi için **%10 stopaj** (pay/endeks dışı VİOP), üç aylık netleştirme, zarar devri sadece aynı takvim yılı içinde.
8. Likidite (2026'da 39 pazartesi, normal seans): tüm XAUUSD vadeleri için günlük hacim medyanı **43.343 sözleşme (≈43 bin ons)**, açık pozisyon medyanı **139.824**, işlem sayısı medyanı 9.523, ön vadenin payı medyan %86. Açık pozisyon vadeye 3–4 iş günü kala yeni vadeye geçiyor (Ağustos ve Ekim 2026). Hacim ön vadede son 1–2 güne kadar baskın.

---

## 1. Sözleşme künyesi (Prosedür Ek-1/R ve BIST ürün sayfası)

| Unsur | Değer | Kaynak |
|---|---|---|
| Dayanak | Saf altın | Prosedür Ek-1 R |
| Sözleşme büyüklüğü | **1 ons** altın | Prosedür Ek-1 R; BIST kıymetli maden VİS sayfası |
| Kotasyon | 1 ons altının USD değeri, virgülden sonra 2 hane (ör. 2.450,10) | Prosedür |
| Min. fiyat adımı / tik değeri | **0,10 USD**. Bir adımın değeri 0,10 USD. TL karşılığı ≈ 0,10 × TCMB USD alış (06.11.2026 için ≈5 TL) | Prosedür |
| Vade ayları | Şubat, Nisan, Haziran, Ağustos, Ekim, Aralık. Aynı anda en yakın 3 vade işlem görür (06.11.2026: 1226, 0227, 0427) | Prosedür; 06.11.2026 bülteni |
| Son işlem günü / vade sonu | Vade ayının **son iş günü**. O gün yurt içinde resmi tatil nedeniyle yarım gün ise bir önceki iş günü | Prosedür |
| Uzlaşma şekli | **Nakdi** | Prosedür |
| Takas süresi | T+1. Zararlar T günü sonunda tahsil edilir, kârlar T günü sonunda aktarılır | Prosedür |
| Kod yapısı | `F_XAUUSDAAYY` (ör. F_XAUUSD1226). Vadeler arası strateji kodu `F_XAUUSDM2-M1` | Prosedür 5.3, Ek-17 |
| ISIN (Ara 2026) | TRVXIST05OK7 (TradingView sayfası) | TradingView |
| Emir büyüklüğü | Min 1, **maks 1.250** sözleşme | Prosedür Tablo 7 |
| Özel işlem bildirimi | Min 1.250, maks 2.500 sözleşme; fiyat limitler içinde olmalı | Prosedür Ek-4 |

Not: Bazı aracı kurum sayfaları hâlâ "0,05 fiyat adımı" ve "09:30–18:15" yazıyor (ör. GCM eğitim makalesi). Bunlar eski bilgi. Güncel Prosedür 0,10 ve 18:10 diyor.

## 2. Seanslar ve "kapanış"ın UTC zamanı

Prosedür Ek-3(B), "akşam seansına dahil olan sözleşmeler" (Dolar/Ons Altın bunlardan biri, Prosedür md. 7):

| Bölüm | TSİ | UTC |
|---|---|---|
| Sistem / seans öncesi | 07:30 | 04:30 |
| Açılış seansı emir toplama | 09:20–09:25 (+0–30 sn rassal) | 06:20–06:25 |
| Açılış eşleştirme (tek fiyat) | ~09:25 | ~06:25 |
| Normal seans (sürekli işlem) | 09:30–18:10 | 06:30–15:10 |
| **Günlük uzlaşma penceresi** | **18:00:00–18:10:00** | **15:00–15:10** |
| Uzlaşma fiyatı ilanı | 18:45+ | 15:45+ |
| Gün sonu (normal) | 18:46+ | 15:46+ |
| Akşam seansı öncesi (emir girilemez) | 18:50 | 15:50 |
| **Akşam seansı** | **19:00–23:00** | **16:00–20:00** |
| Akşam gün sonu | 23:15 | 20:15 |
| **Yarım gün**: normal seans | 09:30–12:40 (uzlaşma penceresi 12:30–12:40) | 06:30–09:40 (09:30–09:40) |

- Normal seans içinde seans arası **yok**. 18:10–19:00 arası işlem yok.
- **Yarım iş günlerinde ve takvim yılının son işlem gününde akşam seansı yapılmaz** (Prosedür Ek-3; BIST işlem saatleri görseli). Doğrulama: 28.10.2026 yarım günü için akşam bülteni 404 döndü.
- Akşam seansında piyasa emri, piyasadan limite emri, iptale kadar geçerli ve tarihli emir **kullanılamaz**. Vadeler arası strateji emri de **kullanılamaz** (Prosedür md. 26).
- Altın akşam seansı 18.09.2020'de başladı (BIST duyuru 12590).
- **BIST duyuru 30572 (19.11.2024)** aslında bakır vadelisinin işleme açılmasıyla ilgili. Ekindeki Prosedür md. 7 değişiklik tablosu Dolar/Ons Altın'ın akşam seansı listesinde olduğunu teyit ediyor. Yani "akşam seansı var" bilgisi doğru, ama 30572 altına özgü bir duyuru değil.
- Normal seans ve akşam seansı **ayrı piyasa yapıcılık programlarıyla** işler (Prosedür 45.1).

**Kendi doğrulamam (zaman damgası).** Ekim 2026'da 9 tam iş gününde ön vade (F_XAUUSD1026) uzlaşmasını, Dukascopy spot XAUUSD'nin 15:00 UTC saat açılışıyla karşılaştırdım. Farklar 8 Eki +9,2; 15 Eki +3,8; 19 Eki +6,8; 20 Eki +4,0; 21 Eki +2,1; 22 Eki +2,7; 23 Eki −0,5; 26 Eki +2,0; 27 Eki +4,7 USD. Bunlar kalan vadeye göre ~%4 yıllık taşıma maliyetiyle uyumlu. Yarım gün (28 Eki) uzlaşması 4054,4 oldu ve 09:30–09:40 UTC spot seviyesine (~4053–4055) oturdu, 15:00 UTC spotuna (4041,4) değil.

**Yaz saati eşlemesi (2026–27).** İngiltere 29.03.2026'da BST'ye geçti, 25.10.2026'da GMT'ye döndü, 28.03.2027'de tekrar BST'ye geçecek. ABD 08.03.2026'da EDT'ye geçti, 01.11.2026'da EST'ye döndü, 14.03.2027'de EDT'ye geçecek (2027 tarihleri "Mart'ın son pazarı / ikinci pazarı" kuralından hesaplandı).

| Olay | Kış (UK GMT + US EST) | Yaz (BST + EDT) |
|---|---|---|
| LBMA Gold AM (10:30 Londra) | 10:30 UTC = 13:30 TSİ | 09:30 UTC = 12:30 TSİ |
| ABD 08:30 ET verileri | 13:30 UTC = 16:30 TSİ | 12:30 UTC = 15:30 TSİ |
| **LBMA Gold PM (15:00 Londra)** | **15:00 UTC = 18:00 TSİ (VİOP uzlaşma penceresinin başlangıcıyla aynı an)** | 14:00 UTC = 17:00 TSİ (uzlaşmadan 1 saat önce) |
| **VİOP uzlaşma** | 15:00–15:10 UTC | 15:00–15:10 UTC (değişmez) |
| COMEX GC uzlaşma (13:29–13:30 ET) | 18:29–18:30 UTC = 21:29 TSİ | 17:29–17:30 UTC = 20:29 TSİ |
| VİOP akşam seansı sonu | 20:00 UTC | 20:00 UTC |

Uyumsuz pencereler: 8–29 Mart ve 25 Ekim–1 Kasım. Bu haftalarda LBMA PM ile COMEX uzlaşması arasındaki fark 1 saat kayar.

## 3. Günlük uzlaşma fiyatı: yöntem ve veri kaynağı

Prosedür Ek-1 R (birebir yöntem). Sonuç en yakın fiyat adımına yuvarlanır:
- a) Seans sona ermeden önceki **son 10 dakikadaki tüm işlemlerin miktar ağırlıklı ortalaması**.
- b) Son 10 dakikada 10'dan az işlem varsa seanstaki son 10 işlemin ağırlıklı ortalaması.
- c) Seansta 10'dan az işlem varsa tüm işlemlerin ağırlıklı ortalaması.
- d) Hiç işlem yoksa önceki günün uzlaşma fiyatı.
- Hesaplanamazsa ya da piyasayı yansıtmıyorsa: seans sonu en iyi alış ve satış ortalaması, ya da spot fiyat ve diğer vadelerden "teorik" fiyat.
- Özel işlem bildirimleri hesaba girmez. Uzlaşma Fiyatı Komitesi fiyatı değiştirebilir.

Ön vadede günde ~4–9 bin işlem var (≈ dakikada 8–17). Bu yüzden pratikte (a) kuralı işler. Dakika bazında doğrulamadım.

**Bülten yapısı (kendi kontrolüm):**
- `viop_YYYYMMDD.csv` (ana bülten) yalnız **normal seansı** içerir. "AÇILIŞ FİYATI" açılış seansı tek fiyatıdır (06.11.2026: 4085, açılış seansında 5 sözleşme). "KAPANIŞ FİYATI" normal seanstaki son işlemdir. "UZLAŞMA FİYATI" ise 18:00–18:10 VWAP'ıdır. Kanıt: 22 ve 23 Ekim'de önceki akşamın başlangıç seviyesi (~4131 ve ~4052) o günün yüksek fiyatının (4104,5 ve 4038,3) üzerinde kaldı. Yani önceki akşam ana bültene yazılmamış.
- `viop_as_bul_YYYYMMDD.csv` (akşam bülteni) **aynı takvim gününün** 19:00–23:00 işlemlerini verir. Uzlaşma ve açık pozisyon alanları boştur. Örnek: 06.11.2026 akşamında F_XAUUSD1226 açılış 4080,5, kapanış 4092, hacim 2.555.
- Gram altın (XAUTRY) akşam bülteninde **yok**. Akşam seansı yalnız XAUUSD, XAGUSD, XPTUSD, XPDUSD, XCUUSD ve endekslerde var.
- **Kapanış ile uzlaşma farkı** (2026, 56 gün, ön vade): mutlak fark medyanı 4,1 bp, ortalaması 5,9 bp, %90'lık dilimi 11,7 bp, en büyüğü 35,6 bp (16,1 USD).
- **Akşam seansının etkisi** (67 gün): akşam hacmi toplamın medyan %7,3'ü (aralık %1,2–21,6). Akşam kapanışı (23:00 TSİ) aynı günün uzlaşmasından mutlak olarak medyan 33 bp, ortalama 42 bp sapıyor. Ertesi günün uzlaşmadan uzlaşmaya getirisinin anlamlı kısmı 15:10–20:00 UTC aralığında oluşuyor.

## 4. Vade sonu uzlaşma fiyatı

Prosedür Ek-1 R ve BIST vade sonu uzlaşma sayfası:
- **Son işlem günü Londra'da öğleden sonra oluşan altın USD/ons fiyatı**: ICE Benchmark Administration'ın açıkladığı **LBMA Gold Price P.M.** İhale 15:00 Londra saatinde başlar (LBMA).
- PM ihalesi yapılmazsa **sabah (AM) fiyatı** kullanılır.
- Resmi tatil vb. nedenle fiyat açıklanmazsa **uluslararası spot piyasada 17:00 TSİ'deki (14:00 UTC) alış ve satış ortalaması** kullanılır. Sonuç fiyat adımına yuvarlanır.
- Tarihçe: 2015'te London Gold Market Fixing Ltd. feshedildiği için referans "LBMA Gold Price P.M. (IBA)" olarak güncellendi (BIST duyuru 11834, 17.04.2015).
- **Aralık vadesi riski:** LBMA 24 ve 31 Aralık 2025'te altın, platin ve paladyum için PM ihalesi yapılmayacağını duyurdu (LBMA, 15.12.2025). 2021'de de 24 ve 31 Aralık'ta yalnız AM ihalesi yapıldı. 31.12.2026 için LBMA duyurusu **bulunamadı**. Aynı uygulama sürerse F_XAUUSD1226 son işlem günü fiyatı **AM ihalesine (13:30 TSİ)** göre belirlenir. Ayrıca 31.12.2026 yılın son işlem günü olduğundan **o akşam akşam seansı da olmaz**.
- Kendi kontrolüm: 30.10.2026'da F_XAUUSD1026 uzlaşması 3913,3. Dukascopy spot 15:00 UTC saat açılışı 3917,5. LBMA PM o gün 15:00 GMT'deydi ve fark makul. LBMA verisini doğrudan çekemedim (403).
- Prosedür, son işlem gününde vadesi dolan sözleşmenin işlem saatine özel bir hüküm koymuyor. Vadesi dolan sözleşmenin o gün akşam seansında işlem görüp görmediği için birincil kaynak **bulunamadı**. Aracı kurum (GCM) "vade sonu gelen sözleşmeler için akşam seansı düzenlenmez" diyor.

## 5. TL'ye çevirme ve nakit akışı

- Prosedür Ek-1 R "Dolar Kuru": USD değerlerin TL'ye çevrilmesinde **TCMB'nin saat 15:30 itibarıyla açıkladığı gösterge niteliğindeki ABD Doları ALIŞ kuru** esas alınır. Borsa gerekli görürse ya da TCMB kur açıklamazsa spot piyasa kurlarıyla güncellenebilir.
- TCMB gösterge kuru nasıl oluşur: 10:00, 11:00, 12:00, 13:00, 14:00 ve 15:00'te bankalararası USD/TRY alım-satım ortalamaları alınır. Bu 6 değerin ortalaması orta kuru verir. Orta kura iskonto ve prim uygulanarak alış ve satış kuru bulunur, **15:30'da** belirlenir. **Resmi tatil, hafta sonu ve yarım günlerde gösterge kur belirlenmez** (TCMB). Yarım günlerde Borsa spot kur kullanır.
- Akış: Günlük USD kâr/zarar, **o günün** 15:30 TCMB alış kuruyla TL'ye çevrilir ve T günü sonunda hesaba yansır (T+1 takas tanımı). Akşam seansında açılıp kapanan pozisyonun kâr/zararı bir sonraki iş günü sonunda yansır (Prosedür 9.5; GCM).
- Sonuç: Pozisyonun USD getirisi kurdan bağımsız. TL karşılığını ise her gün o günün kuru belirler. Teminat TL olduğu için teminat ihtiyacı USDTRY ile birlikte artar.
- Gram altın (XAUTRY) vade sonu farklı: LBMA PM × TCMB 15:30 **alış ve satış ortalaması** ÷ 31,1035 (Prosedür Ek-1 Q).

## 6. Fiyat limitleri

- Baz fiyat: ilk gün Uzlaşma Fiyatı Komitesi belirler, sonraki günlerde **önceki günün uzlaşma fiyatıdır**. **Akşam seansının baz fiyatı, aynı günün normal seans uzlaşma fiyatıdır.**
- Limit: baz fiyatın **±%10**'u. Üst limit bir alt fiyat adımına, alt limit bir üst fiyat adımına yuvarlanır. XAUUSD için akşam seansında ayrı bir oran yok, endekslerdeki ±%3 kuralı burada geçmiyor (Prosedür).
- Vadeler arası strateji emri fiyat limiti sabiti (k): XAUUSD için **15,00 USD** (02.01.2026'dan itibaren, önceden 10). Kaynak: BIST duyuru 42281 (23.12.2025), Prosedür Ek-17.

## 7. Teminat (Takasbank, BISTECH marjin yöntemi)

- Prosedür: "İşlem teminatı esasları Takas Mevzuatı çerçevesinde belirlenir." Takasbank, risk parametresi olarak **Fiyat Değişim Aralığı (PSR, %)** yayınlıyor.
- **Takasbank Genel Mektup 2126 (12.02.2026)**: XAUUSD PSR 17.02.2026'dan itibaren **%6,7**, 02.03.2026'dan itibaren **%10,0**. Aynı mektupta XAUTRY %10,4 → %14,0; XAGUSD %13,9 → %20,0. Gerekçe "emtia piyasalarındaki dalgalanmalar".
- **Takasbank Genel Mektup 2150 (11.06.2026, 15.06.2026'dan geçerli)**: XAUUSD PSR **%10**, XAUTRY %14, XAGUSD %20. XAUUSD vadeler arası yayılma riski (intra-commodity spread charge) 305 USD. Aşırı hareket çarpanı 3, kapsama oranı %32 (GM 2126).
- Sonraki mektuplar (13.08.2026 GM 2163, 01.10.2026 GM 2171, 15.10 ve 02.11.2026 güncellemeleri) **XAUUSD PSR değeri için okunamadı** (isyatirim sunucusu 503 verdi). Arama özetine göre GM 2163'te XAUUSD yayılma riski 325 USD. Güncel PSR için Takasbank risk parametre dosyasına bakılmalı.
- Yaklaşık başlangıç teminatı (PSR %10 ise): 0,10 × 4078,8 ≈ **408 USD/sözleşme** ≈ 20,4 bin TL (06.11.2026). Bu Takasbank tabanıdır. Aracı kurumlar fazlasını isteyebilir: QNB Invest kendi PSR'ını XAUUSD için 02.06.2026'dan **%20**, 08.10.2026'dan **%20,0** uyguluyor. GCM 02.06.2026 tablosunda XAUUSD %10. Gedik 27.02.2026 duyurusunda XAUUSD için "yeni ek teminat oranı %11" yazıyor.
- Teminat çağrısı aracı kurumdan kuruma değişiyor. QNB: gün sonu oran başlangıç teminatının %100'ünün altına inerse çağrı yapılır, gün içi oranın en az %50 olması istenir, toplam teminatın en az %50'si TL olmalı. Takasbank'ın sabit bir "sürdürme %75" kuralı 2026 için **doğrulanamadı**.
- Kaldıraç karşılaştırması: PSR %10 yaklaşık 10 kat kaldıraç demek. Yurt içi forex için SPK sınırı da 10:1 (aşağıda).

## 8. Pozisyon limitleri

BIST sayfası yalnızca "Takasbank Merkezi Karşı Taraf Mevzuatı hükümleri uygulanır" diyor. XAUUSD için hesap bazında sayısal limit **bulunamadı**. Bireysel ölçekte bağlayıcı olması beklenmez. Emir başına 1.250 sözleşme üst sınırı ise kesin.

## 9. Piyasa yapıcılık

- Dolar/Ons Altın **A Grubu** sözleşme. Normal seans ve akşam seansı için **ayrı programlar** var (Prosedür 45.1).
- Yükümlülükler, en yakın 2 vade için (Prosedür Ek-10 ve Ek-12):

| Vadeye kalan gün | <30 | <60 | <90 | ≥90 |
|---|---|---|---|---|
| Normal seans azami spread (USD) | 2,80 | 3,20 | 3,60 | 4,00 |
| Akşam seansı azami spread (USD) | 5,60 | 6,40 | 7,20 | 8,00 |

- Her iki seansta min emir büyüklüğü 20 sözleşme, piyasada bulunma oranı açık sürenin %70'i.
- Bunlar üst sınırlar. Gerçekleşen tipik alış-satış farkı için birincil veri **bulunamadı**. Akşam seansında izin verilen spread normal seansın 2 katı.

## 10. Ücretler ve maliyet

- **Borsa payı**: pay endeksi dışı vadelilerde işlem hacminin **yüzbinde 3**'ü (0,00003), taraf başı (Prosedür Ek-5; BIST borsa payı sayfası).
- **Takasbank VİOP takas komisyonu**: diğer vadelilerde hacmin **yüzbinde 1**'i, asgari tutar yok (Takasbank VİOP ücret tarifesi, 30.01.2026).
- **Aracı kurum komisyonu** (pazarlığa açık, örnek tarifeler):
  - Ata Yatırım 2026: hacmin **onbinde 0,9**'u (vergiler hariç).
  - Strateji Menkul (04.12.2025): VİOP internet **binde 0,20**, sabit binde 0,30.
  - Info Yatırım (12.01.2026'dan): **binde 2 + BSMV**.
  - GCM: günlük asgari 5 TL.
  - Komisyona **%5 BSMV** eklenir (Ata örneği).
- İradi emir iptal ücreti altın sözleşmelerinde **uygulanmaz** (Prosedür 33).
- **Örnek** (06.11.2026, 1 sözleşme, nominal ≈ 4078,8 × 50,0 ≈ 204 bin TL):
  - Borsa ve Takasbank, taraf başı: yüzbinde 4 ≈ **8,2 TL**.
  - Onbinde 2 komisyon + BSMV: ≈ 42,8 TL.
  - Gidiş-dönüş toplam ≈ 102 TL ≈ **5 bp ≈ 2 USD/ons**.
  - 1 tik = 0,10 USD ≈ 0,25 bp.

## 11. Vergilendirme

**Yerleşik (tam mükellef) gerçek kişi:**
- Yasal dayanak GVK geçici 67. 2006/10731 sayılı BKK, 2009/14580 BKK ile değişti. **Pay ve pay endeksi dayalı VİOP %0, bunların dışındaki sözleşmeler (altın, döviz vb.) %10 tevkifat.** Bu oranlar tam ve dar mükellef gerçek kişiler için aynı (**GİB "GVK Geçici 67 Rehberi", Şubat 2026, Yayın No 598**, bölüm 19).
- Geçici 67'nin süresi **10680 sayılı Cumhurbaşkanı Kararı** ile **31.12.2030**'a kadar uzatıldı (RG 11.12.2025).
- Stopajı aracı kurum **takvim yılının üçer aylık dönemleri** itibarıyla keser. Aynı türden araçların dönem içi kâr ve zararları netleşir. Dönem zararı izleyen döneme devreder, ama **takvim yılını aşamaz**. Son çeyrek zararı devredemez (GİB rehberi bölüm 7; GVK geç. 67/1).
- Altın veya dövize dayalı araçlarda matrah işlem tarihindeki **TL karşılıklarıyla** hesaplanır (GVK geç. 67/1).
- Stopaj **nihai vergi**, beyan zorunlu değil (BIST vergilendirme rehberi).
- **İhtiyari beyan** mümkün: aynı türden araçlarda yıl içindeki zararların tamamı mahsup edilebilir. Beyanda "diğer kazançlar" için oran %10, kesilen stopaj mahsup ve iade edilir. Beyan dönemi 1–31 Mart (GİB rehberi).
- Sınıflandırma: menkul kıymete bağlı olmayan vadeli işlemler **III. grupta** ("diğer menkul kıymetler ve diğer sermaye piyasası araçları"). Altın vadelisi zararı hisse kazancıyla netleşmez.

**Kurumlar:**
- BIST vergilendirme sayfası: pay/endeks dışı sözleşmelerde kurumsal tam mükellef için %0, dipnotta "diğer tam ve dar mükellef kurumlar için %10".
- Gedik özeti: sermaye şirketleri %0, diğer kurumsal yatırımcılar %10. Kazanç kurum kazancına girer, stopaj kurumlar vergisinden mahsup edilir.
- GVK geç. 67'ye göre KVK 2/1 kapsamındaki mükellefler için oran %0.

## 12. Kodlar ve veri

| Platform | Kod |
|---|---|
| TradingView sürekli | **BIST:XAUUSD1!** ("Gold USD per ounce Futures") |
| TradingView vadeler | BIST:XAUUSDZ2026 (Ara 2026, vade 31.12.2026), BIST:XAUUSDG2027, BIST:XAUUSDJ2027. Ay harfleri G=Şub, J=Nis, M=Haz, Q=Ağu, V=Eki, Z=Ara |
| TradingView gram altın | BIST:XAUTRY1! (front XAUTRYZ2026). Borsadaki kod F_XAUTRYM1226 (M = mini) |
| Bloomberg | **XLTA Comdty** (gram altın XLA, gümüş STWA, platin PHWA, paladyum PCSA) |
| Reuters | **0#XAUUSD:** (strateji 0#XAUUSD-:) |

- TV sayfası (07.11.2026) fiyatı 4.078,8 gösteriyor (bu uzlaşma fiyatı), hacmi 21,02K (normal + akşam), açık pozisyonu 82,62K. Veri ICE Data Services'ten.
- TV'de "Use settlement as close on daily interval" ayarı ve **B-ADJ** (geri ayarlama) var (TV blog, 13.03.2024).
- TV sürekli kontratı (1!), bir sonraki vadenin hacmi önceki vadeyi geçtiğinde değiştirir. Geçiş tarihini her sembol için tarihsel ortalamaya göre sabitler (örnekte vadeye 6 iş günü kala). XAUUSD1! için kullanılan kural **bulunamadı**.
- TV'deki BIST VİOP verisinin gecikmeli mi gerçek zamanlı mı olduğu birincil kaynaktan **doğrulanamadı**. TV'de ücretli "BIST Futures" veri paketi var (2020 blog). Aracı kurum terminalleri genelde gerçek zamanlı.

## 13. İlgili VİOP kontratları (Prosedür Ek-1)

| Sözleşme | Büyüklük | Adım | Akşam seansı | Vade sonu uzlaşma |
|---|---|---|---|---|
| TL/Gram Altın (F_XAUTRYM) | 1 gram | 0,10 TL | **Yok** | LBMA PM × TCMB 15:30 (alış+satış)/2 ÷ 31,1035 |
| Dolar/Ons Gümüş (F_XAGUSD) | 10 ons | 0,010 USD (değeri 0,10 USD) | Var | LBMA Silver Price, yedek 17:00 spot |
| Dolar/Ons Platin (F_XPTUSD) | 1 ons | 0,10 USD | Var | Refinitiv XPT= orta fiyat, 17:00:00–17:00:59 TSİ |
| Dolar/Ons Paladyum (F_XPDUSD) | 1 ons | 0,10 USD | Var | Refinitiv XPD= orta fiyat, 17:00:00–17:00:59 TSİ |
| Dolar/Ton Bakır (F_XCUUSD) | 0,1 ton | 0,50 USD (değeri 0,05 USD) | Var | LME Official Settlement Price (06.12.2024'te açıldı) |

- **Altına dayalı opsiyon VİOP'ta yok.** Ek-1'deki opsiyonlar yalnız pay, BIST 30 ve USD/TL.
- Likidite (06.11.2026):
  - Gram altın 1226: 82.691 sözleşme (=82,7 kg), açık pozisyon 365.792.
  - Gümüş 1226: 332.964 sözleşme, açık pozisyon 191.920.
  - Platin, paladyum ve bakır çok sığ (günde 8–112 sözleşme).

## 14. Alternatif enstrümanlar

| Araç | Temel farklar |
|---|---|
| **VİOP F_XAUUSD** | 1 ons, USD fiyat, nakdi, TL takas. 09:30–18:10 ve 19:00–23:00 TSİ. Takasbank PSR %10. %10 stopaj. Maliyet yüzbinde 4 + komisyon |
| **VİOP gram altın** | TL fiyat, yani altın × USDTRY örtük. Akşam seansı yok. PSR %14 (Haz 2026) |
| **Yurt içi kaldıraçlı (forex/CFD) XAUUSD** | SPK 10.02.2017 değişikliği: azami kaldıraç **10:1**, asgari başlangıç teminatı **50.000 TL** veya karşılığı döviz. 7/24'e yakın spot, swap maliyeti var. GVK geç. 67'de "diğer sermaye piyasası aracı" sayılıyor. Uygulanan stopaj oranı bu çalışmada **teyit edilmedi** |
| **COMEX GC** | 100 troy ons, 0,10 USD adım = 10 USD. Fiziki teslim (Ch.113). Globex Pazar–Cuma 18:00–17:00 ET. Günlük uzlaşma 13:29–13:30 ET VWAP (12.01.2026'dan güncel prosedür) |
| **COMEX MGC (Micro)** | 10 ons, 0,10 USD = 1 USD |
| **COMEX 1OZ** | 1 ons, **nakdi** (aynı ayın GC uzlaşmasına göre), 0,25 USD adım. Şub/Nis/Haz/Ağu/Eki/Ara. İşlem, kontrat ayından önceki ayın sondan üçüncü iş gününde biter. 13.01.2025'te başladı |
| **LBMA spot / Londra** | Kurumsal OTC piyasa. Referans AM/PM ihaleleri 10:30 ve 15:00 Londra |
| **BIST Kıymetli Madenler Piyasası** | 16:10–23:45 / 08:00–16:00 (ertesi işlem günü). Teslim ve parasal yükümlülük son saati 17:00 (T+0). Yarım günlerde 13:00'te biter. Üye bazlı piyasa |
| **GLDTR (QNB Portföy Altın Katılım BYF)** | BIST KMP'de işlem gören 995/1000 fiziki altın. Yönetim ücreti %0,47/yıl (QNB sayfası, arama özeti). Pay piyasası saatleri. Vergi rejimi bu çalışmada teyit edilmedi |
| **Darphane Altın Sertifikası (ALTIN.S1)** | 1 sertifika = 0,01 gram (995). Pay Piyasası Emtia Pazarı'nda piyasa yapıcılı. GİB rehberi Darphane sertifikası kazancı için %0 (ihtiyari beyan bölümü) |
| **Banka altın hesabı** | Banka alış-satış makası geniş. Vergi ve BSMV ayrıntısı bu çalışmada teyit edilmedi |

## 15. Likidite ve roll pratiği (kendi bülten analizim)

**2026 pazartesi örneklemi (39 gün, 05.01–28.09.2026, yalnız normal seans):**

| | XAUUSD (tüm vadeler) | XAUTRY (gram) | XAGUSD |
|---|---|---|---|
| Günlük hacim medyanı (sözleşme) | **43.343** (ort. 52.149; min 11.732; maks 216.770) | 118.798 | 134.484 |
| İşlem değeri medyanı (TL) | 8,80 milyar | 0,82 milyar | 4,45 milyar |
| Açık pozisyon medyanı | **139.824** | 999.171 | 299.674 |
| İşlem sayısı medyanı | 9.523 | 6.128 | 13.480 |
| Ön vadenin hacim payı (medyan) | %86 | %91 | %90 |

- 06.11.2026 normal seansı: F_XAUUSD1226'da 18.465 sözleşme, 5.356 işlem, açık pozisyon 82.616, uzlaşma 4078,8, kapanış 4079,3. F_XAUUSD0227'de 1.695 sözleşme. F_XAUUSD0427'de 282 sözleşme. Aynı akşam 1226'da 2.555 sözleşme işlem gördü.

**Roll (açık pozisyon ve hacim kesişmeleri):**

| Vade | Son işlem günü | Açık pozisyon kesişmesi | Hacim kesişmesi |
|---|---|---|---|
| Haziran 2026 | 30.06 | 22.06'dan önce: o gün 0826 = 94.680, 0626 = 64.721 (≥6 iş günü kala) | 29.06 (0826 42.570 > 0626 36.405) |
| Ağustos 2026 | 31.08 | 24.08 → 25.08 arası (25.08'de 0826 = 46.229 < 1026 = 47.674), 4 iş günü kala | 31.08 (vade günü) |
| Ekim 2026 | 30.10 (28.10 yarım gün, 29.10 tatil) | 26.10 → 27.10 arası (27.10'da 1026 = 32.632 < 1226 = 74.605) | 30.10 (vade günü) |

- Vade günü ön vadede hâlâ önemli açık pozisyon nakit uzlaşmaya kalıyor. 30.10.2026'da F_XAUUSD1026 açık pozisyonu 23.470.
- **İki aylık takvim farkı** (2. vade − 1. vade uzlaşma): 2026'da **34–80 USD** (≈%0,8–1,7). Ocak–Nisan döneminde 51–80, Haziran–Kasım döneminde 34–41 USD. Spot ile ön vade arasındaki taşıma ≈ %4,7–4,8 yıllık (Ekim 2026'da 1226 vadesi için hesap).
- Pratik öneri: Pozisyonu vadeye **~5 iş günü** kala, tercihen **F_XAUUSDM2-M1 strateji emriyle** taşıyın. Strateji emri yalnız normal seansta kullanılabilir, fiyat limiti sabiti k=15 USD. Sürekli seriyi kendiniz kuracaksanız: sabit roll günü seçin (ör. vadeye 5 iş günü kala), takvim farkı kadar geri ayarlayın ve vade günü uzlaşmasını (LBMA PM) seriden çıkarın.

## 16. Lead-lag çalışması için çıkarımlar

1. **Zaman damgası:** VİOP günlük getirisini uzlaşma fiyatından uzlaşma fiyatına ölçün. Damga tam günlerde ~15:05 UTC, yarım günlerde ~09:35 UTC. Vade günü ön vade için damga LBMA PM zamanıdır.
2. **Yabancı serileri aynı anda örnekleyin.** Spot XAUUSD, DXY, ABD reel faizleri, COMEX gibi serilerin 15:00–15:10 UTC değerini kullanın. Kendi günlük kapanışlarını (COMEX 18:30 UTC, ABD hisse kapanışı 21:00 UTC kışın) kullanmayın. Kullanırsanız "yabancı(T) → VİOP(T+1)" yönünde yapay bir öncül ilişki çıkar. Bu ilişkinin büyüklüğüne fikir vermesi için: akşam kapanışı uzlaşmadan medyan 33 bp sapıyor.
3. **Uzlaşma sonrası olaylar** (ABD öğleden sonra seansı, COMEX uzlaşması, FOMC) T+1 uzlaşma getirisine düşer. Bunlar akşam seansında (19:00–23:00 TSİ) işlem görülebilir. Ama akşam hacmi düşük (medyan %7), yalnız limit emir var ve piyasa yapıcı spread izni 2 kat. Getiriyi yine T+1 uzlaşmasıyla ölçersiniz.
4. **Mevsimsellik:** Kışın LBMA PM ihalesi VİOP uzlaşma penceresiyle aynı anda başlıyor. Yazın 1 saat önce bitmiş oluyor. ABD verileri kışın 16:30, yazın 15:30 TSİ'de; ikisi de uzlaşmadan önce. Rejim değişim tarihlerini (Mart ve Ekim/Kasım) analizde dummy olarak işaretleyin.
5. **Yurt içi tatil ve yarım günler:** Dünya işlem görürken VİOP kapalı kalır. O günlerin getirisi çok günlük olur, yarım günlerde de zaman damgası kayar. 1-3-5 günlük ufukta takvim günü değil **VİOP iş günü** sayın ve bu günleri işaretleyin.
6. **Taşıma kayması:** Ön vade getirisi ≈ spot getirisi + (USD faizi − kira oranı)/252. Bu yaklaşık 1,5–2 bp/gün. 5 günlük ortalamalarda dikkate alın.
7. **TL getirisi** USD getirisinden farklı ise neden TCMB 15:30 alış kurudur (10:00–15:00 TSİ ortalaması). Gram altın vadelisi ise kur riskini gömülü taşır.

## 17. Bulunamayan veya teyit edilemeyenler

- 31.12.2026 için LBMA PM ihalesinin yapılıp yapılmayacağı (2025 ve 2021 notlarına göre büyük olasılıkla yapılmayacak).
- Takasbank'ın 15.06.2026 sonrasındaki XAUUSD PSR değeri (Ağustos, Ekim ve Kasım 2026 mektupları okunamadı).
- Hesap bazında pozisyon limiti rakamı.
- Gerçekleşen tipik bid-ask spreadi. Elimde yalnız piyasa yapıcı azami spread yükümlülüğü var.
- TradingView XAUUSD1! roll kuralı ve veri gecikmesi.
- Kaldıraçlı forex, GLDTR ve banka altın hesabı için güncel stopaj ve BSMV oranları.
- Vadesi dolan sözleşmenin son işlem günündeki işlem bitiş saati (Prosedürde özel hüküm yok).

## 18. Kaynaklar

- Borsa İstanbul VİOP Prosedürü rev. 70 (01/07/2026): https://borsaistanbul.com/files/borsa-istanbul-as-vadeli-islem-ve-opsiyon-piyasasi-proseduru.pdf
- BIST Kıymetli Maden VİS sayfası: https://borsaistanbul.com/piyasalar/viop/vadeli-islem-sozlesmeleri/kiymetli-maden-vadeli-islem-sozlesmeleri
- BIST VİOP işlem saatleri: https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/islem-saatleri (görsel: https://borsaistanbul.com/file/2025-07/viop-islem-saatleri-pazarlar-10-11-12.png)
- BIST günlük uzlaşma fiyatları: https://borsaistanbul.com/piyasalar/viop/sozlesme-ozellikleri/gunluk-uzlasma-fiyatlari
- BIST vade sonu uzlaşma: https://borsaistanbul.com/piyasalar/viop/sozlesme-ozellikleri/vade-sonu-uzlasma-fiyatlari
- BIST duyuru 30572 (19.11.2024, bakır, Prosedür md.7): https://borsaistanbul.com/files/duyuru-30572-TR.pdf
- BIST duyuru 12590 (altın akşam seansı, 18.09.2020): https://borsaistanbul.com/duyuru/12590/usdtry-vadeli-islem-sozlesmelerinde-esnek-sozlesme-olusturma-ozelliginin-devreye-alinmasi-dolarons-altin-vadeli-islem-sozlesmelerinin-aksam-seansinda-islem-gormesi-ve-viop-proseduru
- BIST duyuru 42281 (23.12.2025, k=15): https://www.borsaistanbul.com/files/duyuru-42281-TR.pdf
- BIST duyuru 11834 (2015, LBMA PM): https://borsaistanbul.com/duyuru/11834/viopta-altina-dayali-sozlesmelerde-vade-sonu-uzlasma-fiyatina-iliskin-guncelleme-yapilmistir
- BIST günlük bülten 06.11.2026: https://www.borsaistanbul.com/data/vadeli/viop_20261106.csv ; akşam bülteni: https://www.borsaistanbul.com/data/vadeli/viop_as_bul_20261106.csv ; veri sayfası: https://borsaistanbul.com/veriler/viop
- BIST borsa payı: https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/borsa-payi
- BIST pozisyon limitleri: https://borsaistanbul.com/piyasalar/viop/takas-ve-risk-yonetimi/pozisyon-limitleri
- BIST veri dağıtıcı kodları: https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/veri-dagitici-kuruluslarda-viop-sozlesmeleri
- BIST vergilendirme: https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/vergilendirme ; rehber: https://borsaistanbul.com/files/menkul-kiymet-vergilendirme-rehberi.pdf
- BIST KMP saatleri: https://borsaistanbul.com/piyasalar/kiymetli-madenler-ve-kiymetli-taslar-piyasasi/islem-saatleri
- Takasbank VİOP ücret tarifesi (30.01.2026): https://www.takasbank.com.tr/documents/mevzuat/viopucrettarifesi30_01_2026.pdf
- Takasbank GM 2126 (12.02.2026): https://www.ahlatciyatirim.com.tr/medya/icerik/dosyalar/RISK_PARAMETRELERI_12.02.2026.pdf
- Takasbank GM 2150 (11.06.2026): https://marbas.com.tr/assets/Takasbank-Genel-Mektup-2150.pdf
- QNB PSR (08.10.2026): https://www.qnbinvest.com.tr/duyuru/-viop-psr-oran-guncellemesi-08102026 ; QNB teminat: https://www.qnbinvest.com.tr/viop-teminatlari
- GCM teminat (26.05.2026): https://www.gcmyatirim.com.tr/duyurular/duyuru-viop-baslangic-teminat-degisikligi-hakkinda-26-05-2026
- Gedik teminat (27.02.2026): https://gedik.com/viop-duyurulari/teminat-degisiklikleri/viop-teminat-degisikligi-2702
- GİB GVK Geçici 67 Rehberi (Şubat 2026): https://cdn.gib.gov.tr/api/gibportal-file/file/getFileResources?objectKey=arsiv%2Ffileadmin%2Fbeyannamerehberi%2F2026%2F2026_Gecici67.pdf
- KPMG, 10680 sayılı CBK: https://kpmgvergi.com/yayinlar/mali-bultenler/vergi/gvk-gecici-67-nci-maddenin-yururluk-suresi-31-aralik-2030-tarihine-kadar-uzatildi/3312
- Gedik vergilendirme: https://gedik.com/yazilar/vergilendirme/viop-kontrat-gelirlerinin-vergilendirilmesi
- TCMB gösterge kurlar: https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb+tr/main+menu/temel+faaliyetler/doviz+efektif/doviz+ve+efektif+piyasalari/gosterge+niteligindeki+kurlar
- LBMA fiyat özeti: https://www.lbma.org.uk/lbma-prices-summary ; 2025 yılsonu: https://www.lbma.org.uk/articles/market-and-lbma-price-auction-closing-times-2025
- CME GC uzlaşma prosedürü: https://www.cmegroup.com/content/dam/cmegroup/notices/ser/2026/06/ser-9637r.pdf ; https://www.cmegroup.com/content/dam/cmegroup/market-regulation/rule-filings/2025/12/25-467.pdf ; GC kural kitabı: https://www.cmegroup.com/rulebook/COMEX/1a/113.pdf ; GC fact card: https://www.cmegroup.com/trading/metals/files/fact-card-gold-futures-options.pdf
- CME 1OZ: https://www.cmegroup.com/markets/metals/precious/1-ounce-gold.contractSpecs.html ; basın bülteni: https://www.cmegroup.com/media-room/press-releases/2024/12/05/cme_group_to_launch1-ouncegoldfuturestomeetsurgingretaildemand.html ; MGC: https://cmegroup.com/markets/metals/precious/e-micro-gold.html
- SPK 10.02.2017 basın duyurusu: https://spk.gov.tr/duyurular/basin-duyurulari/2017/yatirim-hizmetleri-ve-faaliyetleri-ile-yan-hizmetlere-iliskin-esaslar-hakkinda-tebligde-iii-37-1-degisiklik-yapilmasina-dair-teblig-hakkinda
- TradingView: https://www.tradingview.com/symbols/BIST-XAUUSD1!/ ; https://www.tradingview.com/symbols/BIST-XAUUSDZ2026/ ; https://www.tradingview.com/symbols/BIST-XAUTRY1!/ ; https://www.tradingview.com/blog/en/improved-bist-futures-settlement-price-back-adjustment-open-interest-43494 ; https://www.tradingview.com/support/solutions/43000691027-how-is-the-switching-date-of-contracts-determined-in-continuous-futures/
- Komisyon tarifeleri: https://atayatirim.com.tr/sss/ucret-ve-tarifeler ; https://infoyatirim.com/hakkimizda/ucretler ; https://strateji.com.tr/wp-content/uploads/2025/12/Ucret-Masraf-ve-Komisyon-Bilgilendirilmesi-2025-12-04.pdf ; https://www.gcmyatirim.com.tr/sirket-profili/yasal-bildirimler/ucret-ve-komisyonlar
- GCM akşam seansı: https://www.gcmyatirim.com.tr/egitim/makaleler/viop-aksam-seansi-hakkinda-bilinmesi-gerekenler
- GLDTR: https://www.qnbinvest.com.tr/GLDTR ; ALTIN.S1: https://www.gcmyatirim.com.tr/borsa/hisse/altins1-darphane-altin-sertifikasi
- Yaz saati 2026: https://www.timeanddate.com/news/time/europe-starts-dst-2026.html

Kod ve veri (yeniden üretim için):
- `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code_r1/` (chk.py, liq.py, sc.py, ev.py)
- Bültenler: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/dl3/` ve `dl4/`
