# Midas: ABD piyasası işlem koşulları (1-3 günlük ETF işlemcisi gözüyle)

Hazırlanma: 07.11.2026 (Cumartesi). Kaynakların tamamı 07.11.2026'da erişildi. Midas destek sayfalarında yayın/güncelleme tarihi yazmıyor; "erişim tarihi" esas alınmalı.
Ham sayfalar: `ham_sayfalar/` (midas, midas_destek_abd, midas_destek_diger, midas_akademi, midas_sozlesme, midas_sitemap, midas_sembol, ptp, vergi, ucuncu_taraf). Betikler: `kod/faz1/fetch_pages.py`, `kod/faz1/fetch_binary.py`, `kod/faz1/extract_destek.py` (User-Agent "etf-research-script/1.0", `python -I`).

Kanıt düzeyi etiketleri:
- **[R]** Midas'ın resmi web sayfası (getmidas.com: ücretler, destek, akademi)
- **[S]** Midas'ın yayımladığı sözleşme / form (webcdn.getmidas.com PDF)
- **[3]** Üçüncü taraf kurumsal kaynak (ihraççı, banka, TradingView, haber)
- **[K]** Kullanıcı beyanı (forum, Şikayetvar, uygulama yorumları). Tek başına kesin kabul edilmedi.
- **(türetilmiş)**: kaynaktaki bilgiden hesapla çıkarıldı.

---

## 0. Hızlı özet

| Konu | Bulgu | Kanıt |
|---|---|---|
| ABD işlem ücreti | Emir başına sabit **1,5 USD**; alt/üst limit yok. Kısmi dolum olsa da emir başına 1,5 USD | [R] M1, M2, M4, M17; [S] S1 |
| 1 USD altı hisse | İlk 300 adet 1,5 USD; 300 adedin üstündeki her adet için +0,005 USD | [R] M1, M17; [S] S1 |
| Hesap işletim / saklama | Ücretsiz (ADR'lerde hisse başına yıllık 0,01-0,03 USD ADR ücreti) | [R] M1 |
| TL↔USD makası | **Bulunamadı** (Midas oran yayımlamıyor; "avantajlı kur" diyor) | [R] M29; [3] T17 |
| USD bakiye | Tutulabiliyor; USD olarak çekilebiliyor; USD nema (faiz) seçeneği var | [R] M30, M31 |
| Saatler (şu an, kış/EST) | Pre 12:00-17:30, Normal 17:30-00:00, After 00:00-04:00, Gece 04:00-12:00 (TSİ) | [R] M7 |
| Uzatılmış saat / gece emir tipi | **Sadece limit** | [R] M8, M10 |
| Emir tipleri | Piyasa, Limit, Stop, Stop-Limit, Kâr al / Zarar durdur | [R] M3 |
| Takip eden stop, MOC/LOC | Midas listesinde **yok** (bulunamadı) | [R] M3 |
| Kesirli alım | Var (min 1 USD); her sembolde değil; ETF'lerde de var | [R] M6, M22 |
| Açığa satış / ABD'de kredi | **Yok** (kredili yatırım sadece BIST) | [R] M19; [S] S2; [K] T1 |
| PDT kuralı | 04.06.2026 itibarıyla kaldırıldı | [R] M13 |
| Takas | T+1, ertesi iş günü 12:00 (TSİ) | [R] M16 |
| Kaldıraçlı/ters ETF | Muhtemel (sembol bazında resmi doğrulama yok) | [S] S2; [K] T3 |
| Spot kripto ETF | **Var**: ETHE ve GBTC'nin getmidas.com sembol sayfası var; IBIT/FBTC/ETHA doğrulanamadı | [R] M38 |
| UNG | **Var** (Kasım 2023; Midas'ın resmi şikâyet yanıtı işlemin gerçekleştiğini teyit ediyor) | [K]+[R yanıtı] T4 |
| PTP (K-1) fonları | Uygulamada "PTP" etiketi var; 2024'te ~1-1,5 hafta %10 brüt satış stopajı uygulandığı bildirildi | [K] T5; [3] T7, T8 |
| Veri | ABD canlı veri **ücretsiz** (gecikmesiz) | [R] M1, M2 |
| Vergi | Alım-satım kazancı tutarı ne olursa olsun yıllık beyan; TL bazında hesap (kur farkı vergilenir); aynı yıl içinde zarar mahsubu var, sonraki yıla devir yok | [R] M25, M26; [3] T9, T10 |

---

## 1. Ücretler, komisyon, döviz

### 1.1 ABD işlem ücreti
- "Amerikan Borsası / İşlem Ücreti: **1,5 USD***" (piyasada 15 USD diye karşılaştırılıyor). [R] M1
- "Sadece 1,5 dolar işlem ücreti öde. Yatırımda alt limit/üst limit yok! Tutar fark etmeksizin sabit 1,5 dolar işlem ücreti." [R] M2
- Piyasa veya limit emri fark etmeksizin "her bir emir için yalnızca 1,5 dolar". Limit emir parça parça dolsa da emir başına ücret alınıyor. [R] M4
- TradingView üzerinden verilen emirlerde de aynı ücret: "Amerikan borsasında sabit işlem ücreti $1,5". [R] M17
- **1 USD altı hisse kuralı**: emir iletildiği andaki fiyat 1 USD'nin altındaysa ilk 300 adet için 1,5 USD sabit, 300 adedin üstündeki her adet için +0,005 USD. [R] M1, M17; [S] S1 (Ek-III)
- Sözleşme tarifesinde "Yukarıda belirtilen oranlar/işlemler **BSMV hariç** … BSMV, Takasbank, MKK ücretleri ile Borsa Payı … ayrıca tahsil edilecektir" ifadesi var. [S] S1. ABD işlemlerinde 1,5 USD'nin üstüne BSMV eklenip eklenmediği **doğrulanamadı** (web sayfaları BSMV'den bahsetmiyor).
- Ücretsiz işlem hakları (kampanya/doğum günü) varsa ABD hisse alım-satımında ücret alınmıyor; 1 USD altı hisselerde geçmiyor. [R] M35
- Opsiyon (bilgi için): 0-500 kontrat/ay için kontrat başına 1,50 USD. [R] M1

**1-3 gün işlemci için gidiş-dönüş maliyet (türetilmiş, 2 × 1,5 USD = 3 USD):**

| Pozisyon | Gidiş-dönüş komisyon | BSMV %5 eklenirse (varsayım) |
|---|---|---|
| 500 USD | %0,60 | %0,63 |
| 1.000 USD | %0,30 | %0,32 |
| 2.500 USD | %0,12 | %0,13 |
| 5.000 USD | %0,06 | %0,06 |
| 10.000 USD | %0,03 | %0,03 |

Spread, kayma ve kur makası bu tabloya dahil değil.

### 1.2 Saklama, hesap ve transfer ücretleri
- Hesap işletimi: ücretsiz. Hesaba para aktarma: ücretsiz. Canlı veri: ücretsiz. Hesap güvencesi (SIPC): var. [R] M1
- ADR'lerde saklama ücreti: hisse başına 0,01-0,03 USD (yılda 1-4 kez, ay sonunda toplu kesilir). ETF'leri ilgilendirmez. [R] M1, destek/ADR sayfası
- Para yatırma: Midas ücret almıyor; banka, SWIFT ve muhabir banka masrafları müşteriye ait. USD transferleri 1-2 iş gününde hesaba geçiyor. [R] M32, para-aktarma sayfaları
- USD çekim: 50 bin USD altı genelde birkaç dakika. ABD hesabından sadece USD çekilebiliyor. [R] M30, para-çekme sayfası
- Başka kuruma ABD hisse virmanı: ACATS 25 USD, DTC hisse başına 5 USD; Midas'a gelen virman ücretsiz. [R] M1

### 1.3 TL↔USD dönüşümü ve USD bakiye
- Döviz al-sat **7/24** yapılabiliyor (yarım günlerde saatler değişebilir). Pariteler USD/TL ve EUR/TL. Sadece nakit bakiye ile yapılabiliyor; alım gücü ile yapılamıyor. [R] M29
- **Makas/ücret oranı: bulunamadı.** Midas web sitesinde ve sözleşmede USD/TL alış-satış farkı yayımlanmıyor. App Store açıklaması yalnızca "avantajlı kur oranlarıyla dolar alım-satım" diyor. [3] T17. Gerçek makas uygulamada alış ve satış fiyatı karşılaştırılarak ölçülmeli.
- Sözleşmeye göre, alım emri başka para birimindeki nakitle verilirse nakit "Elektronik İşlem Platformu'nda yer alan **gün sonu kapanış fiyatları** üzerinden" müşteri onayı aranmadan çevrilebiliyor. [S] S1 md. (para birimi çevirimi). Kontrolsüz kur maliyeti oluşmaması için önce USD alıp sonra emir vermek daha öngörülebilir (türetilmiş).
- **USD bakiye tutulabiliyor**: "Midas yatırım hesabına dolar yollayarak ya da hesabındaki TL bakiyenle dolar alarak…" [R] M2. USD nema: her iş günü 18:45'teki nakit USD bakiyesi üzerinden (yıllık oran uygulamada gösteriliyor; örnekte %3), ödeme ertesi ayın ilk 5 iş gününde. Nakit bloke edilmiyor; hisse alımında kullanılabiliyor. [R] M31. İşlemler arası boşta kalan USD için önemli (türetilmiş).

### 1.4 Bakiye ve teminat kuralları (ücret değil, bloke)
- ABD alımında hesapta yatırım tutarından **en az %1 fazla** nakit bulunmalı (100 USD için 101 USD). [R] M33
- Piyasa kapalıyken verilen **piyasa emirlerinde %3**, **stop emirlerinde %2,5** marj (bloke) uygulanıyor. Hesaptan sadece gerçekleşen tutar düşüyor. [R] M5
- Piyasa emri adet ile verilirse fiyat kayması nedeniyle bakiye eksiye düşebiliyor. Tutarla verilen emirlerde düşmüyor. Limit emirde de düşmüyor. [R] M34

---

## 2. İşlem saatleri (TSİ)

Midas: "hafta içi her gün, 24 saat boyunca alım satım yapılabilir." [R] M7, M2

| Oturum | ABD saati (ET) | TSİ, **kış** (EST; ABD'de 01.11.2026'dan 14.03.2027'ye) | TSİ, **yaz** (EDT) | Kaynak |
|---|---|---|---|---|
| Piyasa öncesi (pre-market) | 04:00-09:30 | **12:00-17:30** | 11:00-16:30 | Kış [R] M7; yaz [R] M23 |
| Normal seans | 09:30-16:00 | **17:30-00:00** | 16:30-23:00 | [R] M7, M23 |
| Piyasa sonrası (after-hours) | 16:00-20:00 | **00:00-04:00** | 23:00-03:00 | Kış [R] M7; yaz [R] M23 |
| Gece piyasası (overnight) | 20:00-04:00 | **04:00-12:00** | 03:00-11:00 (türetilmiş) | Kış [R] M7, uzatılmış saatler sayfası |

- Midas'ın saat sayfası yaz/kış ayrımını yazmıyor. Verdiği saatler bugünkü (EST) duruma uyuyor. Yaz saatleri Midas Akademi sayfasından (pre 11:00-16:30, post 23:00-03:00, normal 16:30-23:00) alındı. Gece piyasasının yaz saati bir saat geriye kaydırılarak türetildi. [R] M7, M23
- ABD saat değişimleri (türetilmiş, takvim hesabı): kış saati 01.11.2026'da başladı; yaz saati **14.03.2027**'de başlayacak. Türkiye'de saat değişimi yok, bu yüzden TSİ seans saatleri bu tarihlerde 1 saat kayıyor.
- Tatiller (2026 kalanı): 26.11.2026 Perşembe kapalı (Şükran Günü); **27.11.2026 Cuma** ve **24.12.2026 Perşembe** yarım gün, işlemler TSİ **21:00**'e kadar; 25.12.2026 kapalı. [R] M12
- **ETF'ler uzatılmış saatlerde işlenebiliyor mu?** Pre/post için Midas genel olarak "hisse" diyor, ETF'leri dışlamıyor. Gece piyasasında "yaklaşık 2.000 farklı hisse ve **yatırım fonunda**" işlem yapılabiliyor; liste her gün güncelleniyor; uygulamada *Keşfet > Tarayıcı oluştur > (Amerikan Borsası) 24 Saat İşlem* ile görülüyor. [R] M11. Belirli bir ETF'in (ör. TQQQ, BOIL) gece listesinde olup olmadığı **doğrulanamadı**; uygulamada kontrol edilmeli.
- **Uzatılmış saatlerde ve gece piyasasında sadece limit emir** verilebiliyor. [R] M8, M10. Gece piyasasında hacim düşük, spread geniş; emir uzun süre dolmayabilir. [R] gece-piyasası SSS
- Bağlam [3] T14: Nasdaq 6 Aralık 2026'dan itibaren (SEC onayına tabi) günde ~23 saat işlem planlıyor; NYSE 22 saat için SEC onayı almış. Midas'ın gece piyasası altyapısının buna göre değişip değişmeyeceği **bulunamadı**.

---

## 3. Emir tipleri, geçerlilik, kesirli alım

### 3.1 Emir tipleri
"Amerikan borsasında … 5 farklı emir tipi: Piyasa emri, Limit emri, Stop emri, Stop-Limit emri, Kâr al-zarar durdur." [R] M3

- **Takip eden stop (trailing)**: Midas'ın emir tipi listesinde **yok**. Midas Akademi'deki "Emir tipleri" yazısı trailing'i genel kavram olarak anlatıyor, Midas'ta sunulduğunu söylemiyor. → **bulunamadı / muhtemelen yok**. [R] M3, akademi/emir-tipleri
- **MOC/LOC (kapanışta piyasa/limit)**: Midas'ta **bulunamadı** (listede yok). Kapanış fiyatına yakın işlem için normal seansın son dakikalarında (kışın 23:5x TSİ) limit/piyasa emri veya after-hours limit emri kullanılmalı (türetilmiş).
- **Kâr al / Zarar durdur (TP/SL)**:
  - Portföydeki pozisyon için "Sat" ekranından veriliyor; seviye oran veya tutar olarak giriliyor. [R] kar-al-zarar-durdur sayfaları
  - **Zarar durdur tetiklenince "Stop Limit emrine dönüşerek belirlenen fiyatın %2 altına kadar gerçekleşebilecek şekilde" borsaya iletiliyor.** [R] M14. Fiyat %2'den fazla boşluk yaparsa (gap) stop dolmayabilir; kaldıraçlı ETF'lerde bu ciddi risk (türetilmiş).
  - TP/SL emri **değiştirilemiyor**, sadece iptal edilip yeniden veriliyor. Birlikte verilen TP ve SL, birlikte iptal oluyor. [R] M15
  - Kâr/zarar oranı normal seansta anlık fiyattan, uzatılmış saatte uzatılmış saat fiyatından, piyasa kapalıyken kapanış fiyatından hesaplanıyor. [R] kar-al-zarar-durdur/belirledigim-kar…
- Alpaca sözleşmesinin Türkçe metninde piyasa, limit ve "sıralı" emirler maddesi var. [S] S2 md. 25

### 3.2 Emir geçerliliği (gün / GTC)
- **Limit**: "iptal edilene kadar" (en fazla **3 ay**, sonra otomatik iptal) veya "piyasa kapanışına kadar". Limit emir borsa açık ya da kapalıyken her an verilebiliyor. [R] M4
- **"Günlük" limit emir 04:00-04:00 arasında geçerli** (uzatılmış saatler sayfası). [R] M9. Limit emir sayfasındaki "verildiği gün borsa kapanışında iptal edilir" ifadesiyle **çelişiyor**. Daha özel ve 24 saat düzenine uygun olan 04:00-04:00 ifadesi muhtemelen günceldir; uygulamada teyit edilmeli.
- **Stop / Stop-limit için GTC**: Midas sayfalarında **bulunamadı**. TradingView'daki Midas kullanıcı yorumu: "Stop emirde iptale kadar geçerli seçeneği yok … Limit emirde var ama stop emirde yok." [K] T1 (tarihsiz). Doğruysa 1-3 günlük pozisyonda stop'un her gün yenilenmesi gerekir. **doğrulanamadı**.
- TradingView entegrasyonu kullanıcı yorumları [K] T1: TradingView panelinden TP/SL girilemiyor; "Limit order's are not possible on early and post market". **doğrulanamadı** (Midas uygulaması için uzatılmış saatte limit emir açıkça mümkün).
- Emirler "İletilecek" veya "Bekliyor" durumundayken iptal/düzenleme yapılabiliyor (Menü > İşlem geçmişi). [R] verdigim-emri-nasil-iptal…

### 3.3 Kesirli (fractional) alım
- Var. Tutar veya adet ile işlem; **en az 1 USD**. Parçalı alıma açık hisselerde limit emir tutar veya adet bazında, kapalı hisselerde **sadece adet** bazında. "Tutar bazlı işlem özelliği tüm hisseler için geçerli değildir." [R] M6
- Midas Akademi: ETF'leri de parçalı alıp satabiliyorsun; "Midas sayesinde yabancı borsa yatırım fonlarında da parçalı alım ve satım yapabilirsin." Aynı yazıda 2021 itibarıyla ~10 bin hissenin ~2.063'ünün (~%20) parçalı alıma uygun olduğu yazıyor (eski veri). [R] M22
- Alpaca sözleşmesi: kesirli emirler sadece NMS menkul kıymetlerinde stoktan karşılanıyor; 1 USD altı tutarlı emirler kabul edilmeyebilir. [S] S2 md. 27
- Belirli kaldıraçlı/ters ETF'lerin parçalı alıma açık olup olmadığı **doğrulanamadı** (uygulamadaki "parçalı" etiketiyle kontrol edilmeli).

---

## 4. Açığa satış ve kredili işlem (ABD)

- **Kredili işlem ABD için yok**: "Kredili yatırım, **sadece Borsa İstanbul hisse senedi alım işlemleri** için kullanılır." [R] M19. Akademi'deki marjin yazısı da sadece BIST'i anlatıyor. [R] akademi/marjin
- **Açığa satış ABD için yok (doğrulandı, dolaylı)**:
  - Alpaca müşteri sözleşmesinin Türkçe metni: açığa satış, "Hesap açma düzenlemelerim Alpaca'da kısa satış yapmaya izin veriyorsa" ve "yalnızca bir **kredi hesabında**" yapılabilir. Midas'ta ABD için kredi hesabı sunulmuyor. [S] S2 md. 10; [R] M19
  - Kullanıcı yorumu: "Short pozisyon işlemlerinin mümkün hale getirilmesi çok isabetli olur. **Sadece long** pozisyon işlemleri yapılması kısıtlayıcı." [K] T1
  - Midas sayfalarında açığa satışın mümkün olduğuna dair bir ifade **bulunamadı**. Eski bir BIST açığa satış SSS adresi 404 dönüyor.
- **Sonuç**: Düşüş yönlü işlem sadece **ters (inverse) ETF** ile (ör. SQQQ, SOXS, SPXU/SDS, TZA, KOLD, SCO, DUST, TMV; vol kısa için SVXY) veya opsiyon (put alımı) ile yapılabilir. Ters ETF'lerin Midas'taki bulunurluğu için bkz. §5.
- **PDT kuralı**: "4 Haziran 2026 itibarıyla PDT kuralı kapsamında uygulanan 25.000 USD portföy değeri şartı ve son 5 işlem gününde en fazla 3 günlük alım-satım işlemi yapma sınırı kaldırılmıştır." [R] M13
- **Takas**: ABD'de takas "bir sonraki iş günü saat 12:00'ye kadar" (T+1). Satış bedelinin çekilebilir olması takası bekliyor. [R] M16, satisini-yaptigim… sayfası. Satış gelirinin takas beklenmeden aynı gün yeni alımda kullanılıp kullanılamayacağı (good-faith kuralı) **bulunamadı**.

---

## 5. ETF bulunurluğu

### 5.1 Genel ifadeler
- "NASDAQ ve NYSE üzerinden işlem … popüler OTC hisselerine ve **çeşitli yabancı borsa yatırım fonlarına (ETF)** yatırım." [R] M20
- "Yaklaşık 10 bin hisse senedi ve fon." [R] M21
- App Store: "NASDAQ ve New York Stock Exchange üzerindeki hisselere ve borsa yatırım fonlarına (ETF) yatırım." [3] T17
- Akademi: "Midas'ta bulunan yatırım fonları aracılığıyla … petrol, buğday, uranyum ve doğal gaz…" ve "New York borsasında işlem gören borsa yatırım fonlarına Midas aracılığıyla yatırım…" [R] akademi/abd-borsalarinda-nelere…
- Alpaca müşteri sözleşmesi (Midas'ın yayımladığı TR metni) md. 34: "**Kaldıraçlı ve Ters ETF'ler** tüm yatırımcılar için uygun olmayabilir…" Ürün kapsamı içinde ele alınıyorlar, ama bu sembol bazında bir garanti değil. [S] S2
- Yurt dışı işlemlerde aracı/saklamacı: **Alpaca Securities LLC** (Nasdaq, NYSE Amex/Arca/MKT). [S] S1 Ek-I, Ek-II
- SPK, 20.08.2026 tarihli kararla Midas'a yurt dışında "paylar, diğer menkul kıymetler, türev araçlar" için **işlem aracılığı** izni verdi (emir iletimine aracılık izni zaten vardı). [S] S4

### 5.2 getmidas.com sembol sayfaları
- Sembol sayfası biçimi `https://www.getmidas.com/amerikan-borsasi/<sembol>-hisse/`.
- Site haritasında (midas-us-stock-sitemap1..9) **1.691** ABD sembol sayfası var. Bunlar hisse senedi. Klasik ETF'lerin (SPY, QQQ, TQQQ, GLD, UVXY, IBIT vb.) sayfası **yok**. `spy-hisse`, `tqqq-hisse` ve `spy-etf` 404 dönüyor. [R] M37
- İstisna: **ETHE** ("Grayscale Ethereum Staking ETF Shares") ve **GBTC** ("Grayscale Bitcoin Trust ETF") sayfaları var, "AL" butonuyla. [R] M38
- Sonuç: web sitesi ETF'ler için sembol bazında doğrulama kaynağı **değil**. Kesin doğrulama sadece uygulama içi aramayla (Keşfet > Pay ara) yapılabiliyor.

### 5.3 Sembol bazında değerlendirme

Değerler: **var** (somut kanıt), **muhtemel** (dolaylı/kullanıcı kanıtı), **doğrulanamadı** (kanıt bulunamadı ama aleyhte de bulgu yok). "yok" denecek hiçbir aleyhte kanıt bulunamadı.

| Sembol | Tür | Durum | Kanıt / not |
|---|---|---|---|
| TQQQ | 3x Nasdaq-100 | muhtemel | [K] T3 r10.net 18.03.2024: "Kaldıraçlı ETF'ler var … TQQQ … SPXL"; Alpaca'da işlenebildiğine dair [K] T6 (2022) |
| SQQQ | -3x Nasdaq-100 | doğrulanamadı | Akademi SQQQ'yu örnek veriyor ama bulunurluk söylemiyor [R] |
| SOXL / SOXS | ±3x yarı iletken | doğrulanamadı | — |
| UPRO | 3x S&P 500 | doğrulanamadı | (SPXL için [K] T3) |
| TNA | 3x Russell 2000 | doğrulanamadı | — |
| BOIL / KOLD | ±2x doğalgaz (ProShares Trust II, **PTP/K-1**) | doğrulanamadı | Şikayetvar kullanıcısı "ung ve buna benzer boil gibi fonlar" diyor [K] T4. PTP riski §5.4 |
| UCO / SCO | ±2x ham petrol (**PTP**) | doğrulanamadı | PTP riski §5.4 |
| NUGT / DUST | ±2x altın madencileri | doğrulanamadı | — |
| TMF / TMV | ±3x 20+ yıl hazine | doğrulanamadı | — |
| UVXY | 1,5x VIX vadeli (**PTP**) | doğrulanamadı | PTP riski §5.4 |
| SVXY | -0,5x VIX vadeli (**PTP**) | doğrulanamadı | PTP riski §5.4 |
| VXX | VIX vadeli **ETN** (PTP değil) | doğrulanamadı | ETN, ihraççı kredi riski |
| IBIT / FBTC / ETHA | Spot BTC/ETH | muhtemel | Aynı sınıftan ETHE ve GBTC'nin sembol sayfası var [R] M38 |
| BITO | BTC vadeli ETF | doğrulanamadı | Yüksek aylık dağıtım: ex-date'te %20 ABD stopajı riski (§6.3) |
| NVDL / TSLL / MSTU / CONL | Tek hisse 2x | doğrulanamadı | — |
| UNG | Doğalgaz vadeli (**PTP**) | **var** (2023-2024) | Kullanıcı Midas'tan UNG aldı; Midas'ın resmi yanıtı (30.11.2023): "27.11.2023 tarihinde Limit Emir ile işlemleriniz başarılı bir şekilde gerçekleşti" [K+R] T4; 09.2024'te uygulamada PTP ibaresi [K] T5 |
| USO | Ham petrol vadeli (**PTP**) | doğrulanamadı | PTP riski §5.4 |
| GLD | Altın (grantor trust) | muhtemel | Midas'ın Kulakları'nda GLD haberleri var; Akademi GLD'yi örnek veriyor [R] (bulunurluk ifadesi yok) |
| SLV | Gümüş (grantor trust) | doğrulanamadı | — |
| ETHE, GBTC | Spot ETH/BTC | **var** | Sembol sayfası [R] M38 |

### 5.4 PTP (K-1 veren ortaklık yapısındaki ETF'ler) ve %10 stopaj riski
- ABD vergi düzenlemesi 1446(f) (01.01.2023'ten beri): ABD dışı kişilerin PTP satışlarında aracı kurum **brüt satış tutarının %10'unu** stopaj olarak kesmek zorunda. PTP "10 percent exception" için "qualified notice" yayımlarsa kesinti yapılmıyor. [3] T7, T8
- **ProShares Trust II** (SVXY, UCO, BOIL, ULE, UGL, AGQ, UVXY, YCL, SCO, KOLD, EUO, GLL, ZSL, YCS, VIXM, VIXY) 26.02.2026 tarihli 92 günlük Qualified Notice'te "10 percent exception … applies" diyor. [3] T7. Sonraki bildirimler bu çalışmada kontrol edilmedi; 92 gün geçerli.
- **USCF** (USCI, USO, USL, BNO, **UNG**, UNL, UGA, CPER) 31.07.2026 tarihli 92 günlük Qualified Notice yayımlamış. [3] T8. Bu bildirimin 92 günü ~31.10.2026'da doldu; daha yenisi bu çalışmada **bulunamadı**.
- **Midas uygulaması**: Şikayetvar kullanıcısı (01.09.2024): UNG'yi alırken uygulamada "sağ üst köşesinde **ptp** diye belirtilmemişti … geç de olsa uyarı koymuşlar"; 12.09.2024: "Midas firması %10 vergiyi bu fondan 1 hafta 10 gün sonra kaldırmış olup bu durumun partner firmadan kaynaklandığını belirtmektedir." Başka bir kullanıcı: "ibare 3-4 gün önce eklendi. Şimdi kesinti yapılacağı söyleniyor." [K] T5
- **1-3 günlük işlemci için sonuç (türetilmiş)**: %10 brüt kesinti tek işlemde bütün avantajı yok eder. PTP etiketli ETF'lerde (UNG, USO, BNO, BOIL, KOLD, UCO, SCO, UVXY, SVXY, VIXY, UGL, AGQ, ZSL, GLL vb.) her işlemden önce uygulamadaki PTP ibaresi ve kesinti bilgisi kontrol edilmeli. Mümkünse PTP olmayan muadiller tercih edilmeli: altında GLD/IAU (grantor trust), gümüşte SLV, volatilitede VXX (ETN), endekslerde 1940 Kanunu fonları (TQQQ, SOXL vb.).

### 5.5 Uygunluk testi / karmaşık ürün onayı
- Yurt dışı işlemlere aracılık sözleşmesi: "Genel Müşteri" olarak sınıflandırılan gerçek kişilerin **Uygunluk Testi yapması zorunlu**. Hizmetler "Uygunluk Testi sonucuna göre … sunulacak ve/veya sunulması durdurulacak". Test sonucu ürünlere uygun değilse sözleşmenin ilgili hükümleri test güncellenince yürürlüğe giriyor. [S] S1 md. 2, 5, 16
- Kaldıraçlı/ters ETF'ler için **ayrı bir onay, ek test veya risk bildirimi bulunamadı**. Alpaca sözleşmesinde genel bir kaldıraçlı/ters ETF risk uyarısı var. [S] S2 md. 34. UNG şikâyetinde kullanıcı "hiç uyarmadınız" diyor (2023). [K] T4

---

## 6. Vergilendirme (kısa vadeli işlemciyi ilgilendiren özet)

Vergi danışmanlığı değildir. Kaynaklar arasındaki farklar ayrıca belirtildi.

### 6.1 ABD tarafı
- **W-8BEN**: Hesap açılışında W-8 beyanı imzalanıyor ("varsa vergi anlaşması avantajlarını talep etmek için bu formla birlikte geçerli W8 Formu'nu da iletiyorum"). [S] S3. Alpaca sözleşmesi: W-8 en az **her 36 ayda bir** yeniden tasdik edilmeli, yoksa hesap kısıtlanabilir. [S] S2 md. 1
- **Temettü stopajı**: ABD temettülerinde Türk vatandaşlarına **%20** (TR-ABD anlaşması); Midas tarafından ödenip net tutar yatırılıyor. [R] M24
- ABD'de NRA (ABD'de yerleşik olmayan) kişi için alım-satım kazancı genelde stopaja tabi değil; istisnası PTP'ler (§5.4).

### 6.2 Türkiye tarafı (alım-satım kazancı)
- "Yurt dışı hisse senedi alım-satım kazançları **tutarına bakılmaksızın** beyan edilmelidir." [R] M25. Yapı Kredi (01.01.2026 mevzuatı): "herhangi bir vergi istisna tutarı veya yıllık beyan haddi aşılması şartı yoktur." [3] T9
- Nitelik: değer artış kazancı (GVK Mük. 80, hesap Mük. 81). Midas beyan rehberi: "BEYAN EDİLECEK DİĞER KAZANÇ VE İRAT" bölümünde **GVK.M.Md.80.1.2**, kazanç sağlayan Midas Menkul Değerler A.Ş. (VKN 6210969430). [R] M26
- Hesaplama [3] T9: alış ve satış bedeli alım/satım tarihlerindeki kurlarla TL'ye çevriliyor. Vergi Merkezi "bir önceki günün TCMB döviz alış kuru" diyor. [3] T10 (küçük fark; mali müşavirle netleştirilmeli)
  - **Kur farkı vergilenir**: TL bazında kazanç varsa USD bazında zarar olsa bile vergi çıkabilir. [3] T9
  - **Yİ-ÜFE endekslemesi**: alım-satım arası Yİ-ÜFE artışı **≥%10** ise maliyet endekslenir; alındığı ay dahil, satıldığı ay hariç. [3] T9, T11. 1-3 günlük işlemlerde pratikte devreye girmez (türetilmiş).
  - Aracı kurum komisyonu (1,5 USD) gider olarak indirilebilir. [3] T9
- **Zarar mahsubu**: aynı yıl içindeki YP menkul kıymet satış zararları (Yapı Kredi'ye göre yurt dışı hisse, yatırım fonu, Eurobond) kazançlardan mahsup edilir. Kira, serbest meslek gibi başka gelirlerden mahsup edilemez (GVK 88). [3] T9. Vergi Merkezi'ne göre yıllık net zarar **sonraki yıla devredilemez**, hisse zararı Eurobond kârından mahsup edilemez. [3] T10 (kaynaklar Eurobond konusunda çelişiyor). Mahsubun yasal dayanağı Maliye Bakanlığı basın açıklaması. [3] T9
- **Oran**: ücret dışı gelir tarifesi. Midas'a göre 2025'te ücret geliri 4,3 milyon TL ve üzerindeyse bu kazançlara %40. [R] M27. 2026 dilimleri: 190.000 / 400.000 / 1.000.000 (ücretlilerde 3. dilim 1.500.000) / 5.300.000 TL; oranlar %15-%20-%27-%35-%40. [3] T13 ve arama özetleri (kaynaklarda küçük tutarsızlık var; GİB tarifesiyle teyit edilmeli)
- **Beyan dönemi**: 2026 kazançları **Mart 2027**'de beyan; ödeme Mart 2027 ve Temmuz 2027 olmak üzere iki taksit. Hazır Beyan Sistemi kullanılıyor. [R] M28, M26
- Midas stopaj kesmiyor veya beyan vermiyor; sorumluluk müşteride. [S] S1 Risk Bildirim; [3] T10
- Yeni düzenleme: 05.05.2026 kanun teklifindeki GVK Mük. 20/D "yurt dışı kazanç istisnası" sadece **son 3 takvim yılında Türkiye'de ikametgâhı ve mükellefiyeti olmayıp 01.01.2026'dan itibaren yerleşenlere** 20 yıl için öngörülüyor. Mevcut Türkiye yerleşiklerini kapsamıyor. [3] T12

### 6.3 Temettü/dağıtım (kısa vadeli işlemciye tuzak)
- Yabancı temettü + USD nema toplamı için beyan sınırı 2025'te 18.000 TL, **2026'da 22.000 TL**. Aşılırsa tamamı beyan edilir. [R] M25; [3] T9
- ABD'de kesilen %20, Türkiye'de bu gelire isabet eden vergiden mahsup edilebilir (GVK 123; belge gerekir, ör. 1042-S). [3] T9, T10
- **Türetilmiş uyarı**: Yüksek dağıtım yapan ETF'ler (ör. BITO, bazı kaldıraçlı ETF'lerin çeyreklik dağıtımları) ex-date üzerinde tutulursa fiyat dağıtım kadar düşer, ama dağıtımın %20'si ABD'de kesilir. 1-3 günlük pozisyonlarda ex-date'i taşımamak bu "vergi sızıntısını" önler.

---

## 7. Veri
- ABD için **canlı veri ücretsiz** ("Canlı Veri: Midas'ta Ücretsiz / Piyasada 150 TL"). [R] M1. "Herkes hisse ve fon fiyatlarını gecikmeli görürken sen borsalara dair canlı verilere anlık ve ücretsiz ulaşırsın." [R] M2
- Pre/post fiyatları hisse detay sayfasında güneş/ay sembolü yanında gösteriliyor. [R] M34
- TradingView entegrasyonunda veri **CBOE One** kaynaklı; Midas uygulamasındaki fiyattan farklı olabilir ("Midas daha kapsamlı piyasa verisi lisanslarına sahip"). [R] M18
- Midas Pro (aylık 1.200 TL): derinlik, aracı kurum dağılımı, takas analizi. Ağırlıkla BIST verisi; ABD için ek veri sağladığı **bulunamadı**. [R] M36, midas-pro-nedir
- BIST verileri için "en az 15 dakika gecikmeli" uyarı notu var (ABD'yi kapsamıyor). [S] Uyarı Notu

---

## 8. 1-3 günlük (akşamdan akşama) işlemci için pratik sonuçlar (türetilmiş)

1. **Kontrol saati**: Kışın TSİ 17:30-00:00 normal seans, akşam kontrolü seans içinde yapılabiliyor. Yazın seans 23:00'te kapanıyor. Akşam 23:00 sonrası kontrol yazın after-hours'a (sadece limit) denk geliyor.
2. **Kapanışa yakın giriş/çıkış**: MOC/LOC yok. Kışın 23:50-23:59 TSİ arasında limit (veya piyasa) emri ya da 00:00-04:00 after-hours limit emri kullanılmalı.
3. **Stop yönetimi**: Zarar durdur, tetik fiyatının %2 altına limitli stop-limit oluyor. Gece boşluklarında (gap) dolmayabilir. Stop'ta GTC olmadığı kullanıcı beyanı var; pozisyon taşınan her gün stop kontrol edilmeli. Trailing stop yok.
4. **Piyasa emri yerine limit**: Piyasa kapalıyken piyasa emri %3 bloke ile açılışta dolar. Uzatılmış saat ve gece piyasasında zaten sadece limit kabul ediliyor.
5. **Kısa yön**: Açığa satış yok. Düşüş için ters ETF veya put.
6. **Pozisyon büyüklüğü**: 1,5 USD sabit ücret yüzünden 1.000 USD altı pozisyonlarda gidiş-dönüş maliyeti %0,3'ü geçiyor. 2.500 USD üstünde %0,12'nin altına iniyor.
7. **PTP etiketli fonlar** (doğalgaz, petrol, VIX, ProShares Ultra emtia): her işlemden önce uygulamadaki PTP ibaresi ve %10 kesinti kontrol edilmeli. Altında GLD/IAU, VIX'te VXX gibi PTP olmayan muadiller tercih edilmeli.
8. **Kur**: TL'den USD'ye her girişte makas maliyeti var (oran bulunamadı). USD bakiyede kalıp USD nema almak daha verimli. Vergi TL bazında, kur artışı vergilenebilir kazanç yaratıyor.
9. **Ex-date**: Yüksek dağıtımlı ETF'lerde ex-date taşınmamalı (%20 ABD stopajı).
10. **Doğrulama listesi (uygulamada, her ETF için)**: (a) Keşfet > Pay ara ile sembol var mı, (b) "parçalı" etiketi, (c) "PTP" ibaresi, (d) Keşfet > Tarayıcı > 24 Saat İşlem listesinde mi, (e) emir ekranında stop/limit için geçerlilik seçenekleri.

---

## 9. Bulunamayanlar / açık sorular
- USD/TL döviz makası veya ücreti (yayımlanmıyor).
- 1,5 USD'ye BSMV eklenip eklenmediği (sözleşmede "BSMV hariç" ifadesi var).
- Trailing stop, MOC/LOC: Midas'ın listesinde yok; uygulamada gizli bir seçenek olup olmadığı doğrulanamadı.
- Stop emirlerinde GTC (sadece kullanıcı beyanı var: yok).
- Belirli ETF'lerin (TQQQ, SOXL, BOIL, UVXY, IBIT vb.) Midas'ta işlem görüp görmediği: resmi sembol listesi yok; uygulama içi kontrol gerekli.
- Kaldıraçlı/ters ETF için ayrıca karmaşık ürün onayı veya ek test: bulunamadı.
- Satış gelirinin takas öncesi yeni alımda kullanılması (cash account good-faith kuralı) Midas'ta nasıl uygulanıyor: bulunamadı.
- USCF'nin 31.07.2026 sonrası 1446(f) bildirimi: bulunamadı (92 gün dolmuş olabilir).
- Kesirli emirlerin uzatılmış saat ve gece piyasasında geçip geçmediği: bulunamadı.
- Midas'ın gece piyasası mekânı (ATS/borsa) ve Nasdaq'ın 6 Aralık 2026 gece seansı sonrası değişiklik: bulunamadı.

---

## 10. Kaynaklar (erişim: 07.11.2026)

**Midas resmi web [R]**
- M1 Ücretler: https://www.getmidas.com/ucretler/ (eski adres `…/destek/profil-ve-hesap-bilgileri/ucretler-ve-komisyon/komisyon-oranlari-nelerdir` buraya yönleniyor)
- M2 ABD borsaları: https://www.getmidas.com/abd-borsalari/
- M3 Emir tipleri: https://www.getmidas.com/destek/amerikan-borsasi/alim-satim-islemleri-ve-emirler/midasta-hangi-emir-tiplerini-kullanabilirim
- M4 Limit emir: https://www.getmidas.com/destek/amerikan-borsasi/alim-satim-islemleri-ve-emirler/limit-emir-nedir
- M5 Piyasa emri marj kuralı: https://www.getmidas.com/destek/amerikan-borsasi/alim-satim-islemleri-ve-emirler/amerikan-borsasi-piyasa-emirlerindeki-marj-kurali-nedir
- M6 Parça hisse: https://www.getmidas.com/destek/amerikan-borsasi/alim-satim-islemleri-ve-emirler/tutar-veya-adet-ile-parca-hisse-alim-satimi-nasil-yapilir
- M7 İşlem saatleri: https://www.getmidas.com/destek/amerikan-borsasi/amerikan-borsasi-piyasa-bilgileri/hangi-saatler-arasinda-emir-verebilirim
- M8 Uzatılmış saat emir tipi: https://www.getmidas.com/destek/amerikan-borsasi/uzatilmis-islem-saatleri/uzatilmis-islem-saatlerinde-hangi-emir-tiplerini-iletebilirim
- M9 Günlük limit geçerliliği: https://www.getmidas.com/destek/amerikan-borsasi/uzatilmis-islem-saatleri/limit-emirler-ne-zamana-kadar-gecerlidir
- (uzatılmış saat farkı) https://www.getmidas.com/destek/amerikan-borsasi/uzatilmis-islem-saatleri/uzatilmis-islem-saatleri-ile-piyasa-saatlerinin-farki-nedir
- M10 Gece piyasası emir tipi: https://www.getmidas.com/destek/amerikan-borsasi/gece-piyasasi/gece-piyasasinda-hangi-emir-turunu-kullanabilirim
- M11 Gece piyasası semboller: https://www.getmidas.com/destek/amerikan-borsasi/gece-piyasasi/gece-piyasasinda-hangi-hisselerde-islem-yapabilirim
- (24 saat) https://www.getmidas.com/destek/amerikan-borsasi/gece-piyasasi/amerikan-borsasinda-24-saat-islem-yapabilir-miyim
- M12 Tatiller: https://www.getmidas.com/destek/amerikan-borsasi/amerikan-borsasi-piyasa-bilgileri/amerikan-borsasinin-kapali-oldugu-ozel-gunler
- M13 PDT: https://www.getmidas.com/destek/amerikan-borsasi/gunluk-al-sat-limiti/gunluk-al-sat-islemlerinde-limit-var-mi
- M14 Zarar durdur: https://www.getmidas.com/destek/amerikan-borsasi/kar-al-zarar-durdur/zarar-durdur-emri-nedir
- M15 TP/SL değiştirme/iptal: https://www.getmidas.com/destek/amerikan-borsasi/kar-al-zarar-durdur/kar-al-zarar-durdur-emrini-nasil-degistirebilirim ; https://www.getmidas.com/destek/amerikan-borsasi/kar-al-zarar-durdur/kar-al-zarar-durdur-emrini-nasil-iptal-edebilirim
- M16 Takas: https://www.getmidas.com/destek/amerikan-borsasi/amerikan-borsasi-piyasa-bilgileri/amerikan-borsasinda-takas-suresi-ne-anlama-gelir
- M17 TradingView ücret: https://www.getmidas.com/destek/amerikan-borsasi/tradingview-entegrasyonu/tradingview-uzerinden-verecegim-emirlerin-islem-ucreti-ne-kadar
- M18 TradingView veri: https://www.getmidas.com/destek/amerikan-borsasi/tradingview-entegrasyonu/uygulamada-gordugum-fiyat-ile-tradingviewdaki-fiyat-arasinda-fark-var-neden
- M19 Kredili işlem (sadece BIST): https://www.getmidas.com/kredili-islem/
- M20 Hangi yatırımlar: https://www.getmidas.com/destek/midas-ile-yatirima-baslarken/midas-ile-neler-yapabilirim/midas-yatirim-hesabin-ile-hangi-yatirimlari-yapabilirsin
- M21 Avantajlar (~10 bin hisse ve fon): https://www.getmidas.com/destek/midas-ile-yatirima-baslarken/midas-ile-neler-yapabilirim/midasla-yatirim-yapmanin-avantajlari-neler
- M22 Parça hisse (ETF'lerde parçalı): https://www.getmidas.com/midas-akademi/parca-hisse-senedi-nedir/
- M23 Pre/Post saatleri (yaz/kış): https://www.getmidas.com/midas-akademi/abd-acilis-oncesi-islemler-ve-kapanis-sonrasi-pre-market-post-market-nedir/
- M24 Temettü %20: https://www.getmidas.com/destek/amerikan-borsasi/temettu/temettu-nedir
- M25 Beyan kapsamı: https://www.getmidas.com/destek/amerikan-borsasi/vergilendirme/amerikan-borsasindaki-hangi-kazanclarim-icin-vergi-beyaninda-bulunmaliyim
- M26 Beyanname: https://www.getmidas.com/destek/amerikan-borsasi/vergilendirme/beyanname-nasil-verilir
- M27 Vergi dilimleri: https://www.getmidas.com/destek/amerikan-borsasi/vergilendirme/vergi-dilimleri-nelerdir
- M28 Beyan dönemi: https://www.getmidas.com/destek/amerikan-borsasi/vergilendirme/vergi-beyani-donemi-ne-zaman
- M29 Döviz al-sat: https://www.getmidas.com/destek/para-transferi-ve-doviz-al-sat/doviz-al-sat/hangi-saatler-arasinda-doviz-al-sat-yapabilirim ; …/hangi-paritelerde-islem-yapabilirim ; …/alim-gucu-ile-islem-yapabilir-miyim
- M30 Çekim para birimi: https://www.getmidas.com/destek/para-transferi-ve-doviz-al-sat/para-cekme-islemi/hangi-para-birimlerinde-para-cekme-islemi-yapabilirim
- M31 USD nema: https://www.getmidas.com/destek/amerikan-borsasi/dolar-nema-getirisi/dolar-nema-getirimi-nasil-hesaplayabilirim (ve aynı kategorideki diğer sayfalar)
- M32 Para yatırma ücreti: https://www.getmidas.com/destek/para-transferi-ve-doviz-al-sat/para-aktarma-islemi/para-yatirma-ucreti-var-mi
- M33 %1 bakiye kuralı: https://www.getmidas.com/destek/midas-ile-yatirima-baslarken/midas-ile-neler-yapabilirim/nasil-alis-islemi-gerceklestirebilirsin
- M34 Eksi bakiye / pre-post fiyat: https://www.getmidas.com/destek/amerikan-borsasi/amerikan-borsasi-piyasa-bilgileri/hesap-bakiyemi-neden-ekside-goruyorum
- M35 Ücretsiz işlem: https://www.getmidas.com/destek/profil-ve-hesap-bilgileri/ucretler-ve-komisyon/ucretsiz-islem-nedir
- M36 Midas Pro ücreti: https://www.getmidas.com/destek/profil-ve-hesap-bilgileri/midas-pro/midas-pro-uyelik-ucreti-ne-kadar
- M37 Site haritası: https://www.getmidas.com/sitemap_index.xml ; https://www.getmidas.com/midas-us-stock-sitemap1.xml … sitemap9.xml
- M38 Sembol sayfaları: https://www.getmidas.com/amerikan-borsasi/ethe-hisse/ ; https://www.getmidas.com/amerikan-borsasi/gbtc-hisse/ (404: …/spy-hisse/, …/tqqq-hisse/)
- Akademi: https://www.getmidas.com/midas-akademi/emir-tipleri-nelerdir/ ; https://www.getmidas.com/midas-akademi/etf-nedir-nasil-alinir/ ; https://www.getmidas.com/midas-akademi/kisa-pozisyon-short-ve-uzun-pozisyon-long-nedir/ ; https://www.getmidas.com/midas-akademi/marjin-ne-demek-borsada-marjin-islem/ ; https://www.getmidas.com/midas-akademi/abd-borsalarinda-nelere-yatirim-yapabilirim/

**Midas sözleşme/form [S]** (liste: https://www.getmidas.com/yasal-duyurular-ve-sozlesmeler/)
- S1 Yurt Dışı İşlemlere Aracılık Sözleşmesi (+ Ek-I/II/III, Risk Bildirim Formu): https://webcdn.getmidas.com/uploads/2025/12/04160345/yurt-disi-islemlere-aracilik-sozlesmesi.pdf
- S2 Yurt Dışı Borsaları Kullanıcı Sözleşmesi (Alpaca Müşteri Sözleşmesi TR): https://webcdn.getmidas.com/uploads/2025/12/04155950/yurt-disi-borsalari-kullanici-sozlesmesi-1.pdf
- S3 W-8BEN Disclosure: https://webcdn.getmidas.com/uploads/2025/12/04160304/W8-BEN-Disclosure.docx.pdf
- S4 SPK yurt dışı işlem aracılığı izni (21.08.2026): https://webcdn.getmidas.com/uploads/2026/08/24134138/Yurt-Disinda-Islem-Araciligi-Faaliyet-Izni.pdf
- Uyarı Notu: https://webcdn.getmidas.com/uploads/2025/12/04155226/Uyari-Notu-2.docx-2.pdf

**Üçüncü taraf [3] / kullanıcı [K]**
- T1 [K] TradingView Midas broker sayfası, kullanıcı yorumları (tarihsiz): https://www.tradingview.com/broker/Midas/
- T2 [3] TradingView blog, Midas entegrasyonu: https://www.tradingview.com/blog/en/midas-joins-tradingview-ecosystem-51852/
- T3 [K] r10.net, 18.03.2024: https://www.r10.net/sorum-var/4027951-midas-ta-kaldiracli-islemler-var-mi.html
- T4 [K+Midas yanıtı] Şikayetvar UNG, 27-30.11.2023: https://www.sikayetvar.com/midas/midas-dogalgaz-fonlari-etf-yatirim-araci-degil-batirim-araci-ung
- T5 [K] Şikayetvar "UNG fonunda %10 vergi", 01-12.09.2024: https://www.sikayetvar.com/midas/midas-ung-fonunda-10-vergiyi-belirtmedi
- T6 [K] Alpaca forum, 09.12.2022: https://forum.alpaca.markets/t/leveraged-etf-trading-as-retail-client/11301
- T7 [3] ProShares Trust II 1446(f) Qualified Notice, 26.02.2026: https://www.proshares.com/globalassets/proshares/documents/qualified-reports/pst_ii_qualified_notice_02262026.pdf
- T8 [3] USCF 1446(f) Qualified Notice, 31.07.2026: https://secure.alpsinc.com/MarketingAPI/api/v1/Content/uscfinvestments/uscfinvestments-taxst-20260731.pdf
- T9 [3] Yapı Kredi, "Yabancı Hisse Senedi Gelirlerinde (2026 Yılı) Vergi Durumu" (01.01.2026 mevzuatı): https://www.yapikredi.com.tr/medium/file/yabanci-hisse-senedi-gelirlerinde-2026-yili-vergi-durumu_71999/view
- T10 [3] Vergi Merkezi, 2025 yurt dışı hisse vergi rehberi: https://vergimerkezi.com.tr/yurtdisi-hisse-senedi-vergilendirme-rehberi-2025/
- T11 [3] Gedik Yatırım, yurt dışı hisse vergilendirmesi: https://gedik.com/yazilar/vergilendirme/yurt-disi-hisse-senedi-gelirlerinin-vergilendirilmesi
- T12 [3] KPMG, 07.05.2026 kanun teklifi (GVK Mük. 20/D): https://kpmgvergi.com/yayinlar/mali-bultenler/vergi/vergi-kanunlarinda-onemli-degisiklikler-ongoren-kanun-teklifi-tbmm-ye-sunulmustur/4485
- T13 [3] Forbes Türkiye, 01.01.2026, 2026 tarifesi ve 22.000 TL sınırı: https://www.forbes.com.tr/ekonomi/2026-yili-gelir-vergisi-tarifesi-ve-istisna-tutarlari-belirlendi
- T14 [3] Euronews, 18.08.2026, Nasdaq 23 saat: https://tr.euronews.com/business/2026/08/18/nasdaq-araliktan-itibaren-23-saatlik-islem-icin-gece-seansini-onayladi
- T17 [3] App Store Midas sayfası: https://apps.apple.com/tr/app/midas-borsa-hisse-al%C4%B1m-sat%C4%B1m/id1554268946?l=tr
- Okunamadı: saygec.com forum konusu (bot doğrulama sayfası döndü, aşılmaya çalışılmadı): https://saygec.com/konu/midas-kaldiracli-islem-nasil-yapilir.73339/
