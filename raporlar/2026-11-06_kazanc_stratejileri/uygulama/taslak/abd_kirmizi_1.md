# ABD planı, kırmızı takım 1: pre-mortem

**Hedef:** `uygulama/PLAN_ABD.md` (06.11.2026, ~14:00 TSİ).
**Mercek:** Plan önümüzdeki 3 ayda (9.11.2026 – ~5.2.2027) ABD hesabının **%15–25'ini** kaybetti. En olası yollar hangileri? Hangi kural bu yolları kesiyor, hangisi kesemiyor? Her açık için somut kural düzeltmesi.

Kısaltmalar PLAN_ABD.md ile aynıdır (KIM, KEN, TEST, PRA, PROF, DLG, SEY, TRM, VA, VC, VD, VP, HAZ, HU). "NLV" = IBKR hesabının net likidasyon değeri, yani gerçekten ABD'de duran para.

**Etiketler:** [D] doğrulanmış, [K] kısmen, [P] uygulayıcı kuralı, [H] bu dosyanın hesabı (kalibre değil, yalnız göreli büyüklük), [Ö] tasarım seçimi.

---

## 0. Özet

**Ana sonuç:**
- **Kurallara uyulursa pre-mortem neredeyse olmaz.** Düşmanca bir rejim varsayan hesabımda [H] P(3 ayda NLV'nin ≥%15'i kaybı) ≈ %0–0,4.
- **Pre-mortem'i üreten yollar dört tane:**
  - (1) Planın kendi durdurma eşiği bu kaybı serbest bırakıyor (payda yanılgısı).
  - (2) Davranış ihlalleri. Erken dönemde bunları fren yok.
  - (3) Emir mekaniği: margin hesapta birlikte tetiklenen bekleyen emirler.
  - (4) 200 GHO çevresinde rejim whipsaw'u ve tek isim gap'i.
- Vergi ve kur kaybı büyütmüyor, ama algıyı ve net sonucu ~1–4 puan kötüleştiriyor.

| # | Ciddiyet | Yol | Düzeltme (kısa) |
|---|---|---|---|
| 1 | **KRİTİK** | Limitler E'nin yüzdesi; ama ABD'de yalnız E'nin %40'ı var. −%15 E durdurması = **NLV'nin −%37,5'i**. Pre-mortem bandı (NLV −%15…−25 = E'nin −%6…−10'u) planı Kademe 1–3'te bırakıyor, durdurmuyor. −%15, planın kendi 1 yıllık p95 düşüşünün (−%7,4…−8,3) ~2 katı | Merdiven −%3 / −%5 / −%6,5 / **−%8 E'de dur**. Her limit E ve NLV birimiyle yazılır |
| 2 | **KRİTİK** | Davranış: risk artırma, Midas'ta call, AI dip alımı. K6 ilk 20 işlemde fiilen tetiklenmiyor. İhlal senaryosunda P(NLV ≥ −%15) ≈ %38 [H] | Kritik ihlal listesi: ilk ihlalde 10 seans dur, ikincide plan durur. Teknik kilitler: opsiyon izni yok, emir değeri tavanı, Midas'ta test parası dışında bakiye yok |
| 3 | ÖNEMLİ | Rejim whipsaw: S&P 200 GHO'nun +%0,4 üstünde. Bu bölgede başlayan SARI bölümlerinin %59'u 10 seanstan kısa sürdü (2017–26) [H] | SARI 3 kapanış üst üste. Pilot-başarısızlık freni. 200 GHO × 1,02 altında tek pilot |
| 4 | ÖNEMLİ | 6 izinli kümede 6 bekleyen buy-stop aynı ralli gününde dolabilir. Margin tipi hesap fazlasını borçla finanse eder | Canlı giriş emri sayısı ≤ boş hak; fazla aday OCA grubunda. IBKR **nakit hesap** |
| 5 | ÖNEMLİ | Tek isim gap'i / ikili olay. Tek pozisyon tavanı %15 E = NLV'nin %37,5'i. Bilanço dışı olay (FDA, CMS, kongre verisi) taranmıyor | Faz 1–2'de tek pozisyon ≤ %7,5 E. Yasak listesine ikili olaylar. Yönetilen sağlık evren dışı |
| 6 | ÖNEMLİ | 2026 kısa vergi yılı: Kasım–Aralık zararı 2027'ye devretmez | Aralık'ta "kazanç hasadı" istisnası (müşavir teyidiyle) |
| 7 | ÖNEMLİ | Döviz anahtarının getirdiği USD "aracı kurumda nakit" olabiliyor. Sonuç: boyut karışıklığı, teyitsiz IBKR kuruluşunda yoğunlaşma | Anahtar USD'si işlem hesabına girmez |
| 8 | KÜÇÜK | SARI'yı NDX 10>20 açabiliyor, oysa izinli evren savunmacı. K6, K7 ve K10 aynı faiz faktörünü taşıyor | Savunmacı kümede tetik S&P/FTD olmalı. K6+K7+K10 tek küme. Korelasyon ilk girişten önce ölçülür |
| 9 | KÜÇÜK | Tek emir penceresi (16:45–17:15) BIST/VİOP seansıyla çakışıyor. Pencere kaçarsa çıkışlar da kaçar | Çıkışlar ve stop düzeltmeleri sabah 08:00–09:00'a. Sabah stop mutabakatı |
| 10 | KÜÇÜK | Kısmi MOO reddedilirse pozisyonun yarısı stopsuz kalır | İki alt lot, her birine ayrı ekli stop; kısmi satış OCA içinde |
| 11 | KÜÇÜK | 22:00 TSİ olay günleri (18.11 FOMC tutanakları) ve 8–11.12 olay kümesi | O günlerde giriş emri 21:55'te düşer (GTD). Makro olay için gap-ayarlı ısı |
| 12 | KÜÇÜK | TL algısı: işlem sonucu sıfır olsa bile ABD'deki boş USD, TL mevduata göre çeyrekte ~2,7 puan geride | Çeyrek içinde TL kıyasıyla karar verilmez. Rapor iki birimle yazılır |

---

## 1. Pre-mortem çerçevesi: "ABD hesabının %15–25'i" planda ne demek?

PLAN §1.3–1.4 ve §5.1 bütün yüzdeleri **E** üzerinden tanımlıyor. E, ABD hesabı ile TL'de bekleyen payın toplamı. Aşama 1'de ABD'deki USD, E'nin %40'ı. Bu yüzden her limitin NLV'deki karşılığı **2,5 kat** büyük.

| Limit (Faz 1) | E'nin %'si (plan) | NLV'nin %'si (aşama 1, %40) | 50k / 250k / 1m $ E'de $ |
|---|---|---|---|
| İşlem başı risk | %0,25 | %0,625 | 125 / 625 / 2.500 |
| Aylık devre kesici | %3 | %7,5 | 1.500 / 7.500 / 30.000 |
| En kötü hafta, SARI (brüt %30 × −%15) | %4,5 | %11,25 | 2.250 / 11.250 / 45.000 |
| Merdiven −%4 / −%7 / −%10 | aynı | −%10 / −%17,5 / **−%25** | 2k/3,5k/5k · 10k/17,5k/25k · 40k/70k/100k |
| **Dur (K5) −%15** | −%15 | **−%37,5** | 7.500 / 37.500 / 150.000 |
| Tek pozisyon tavanı %15 | %15 | %37,5 | 7,5k / 37,5k / 150k |

**Okuma:**
1. Pre-mortem bandı NLV'nin −%15…−25'i, yani E'nin **−%6…−10'u**. Plan bu noktada Kademe 1 ile 3 arasında. Risk yarıya iniyor, en kötü durumda 10 seans duruluyor, ama **plan durmuyor**.
2. Üç aylık devre kesici art arda tetiklense bile toplam ~%9 E eder. Bu NLV'nin %22,5'i: pre-mortem'in üst ucu kuralların içinde kalıyor.
3. Kullanıcı IBKR ekstresinde −%25 görür, plan ise "devam" der. Bu ayrım hem terk etmeyi hem intikam işlemini besler (bkz. bulgu 2).

---

## 2. En olası yollar: üç aylık Monte Carlo [H]

**Model:** `kirmizi1/premortem_mc.py`, 40.000 yol.
- Faz 1, %0,25 risk. Çeyrekte ortalama 14 işlem (Poisson).
- İsabet %27; kazanç 0,5 + Üstel(2)R. Kayıpların %10'u gap'li (−2R).
- İşlemler 2'li dalgalarla geliyor. Dalgaların %30'unda hepsi birlikte stop oluyor (PROF §3.3 Model B'nin kötü rejimi).
- İşlem başı beklenti ≈ **−0,4R**. Bu bilinçli olarak düşmanca bir rejim varsayımı.
- Aylık devre kesici ve merdivenin 1. kademesi modelde var.
- "Felaket gap": işlem başına %1 olasılıkla pozisyonda −%30…−50.
- "İhlal" senaryosu iki davranış ekler: (a) E'nin −%2'sine inilince ya da 6 kayıplık seride risk %1'e çıkıyor; (b) 2. aydan itibaren ayda 2 kez E'nin %1'i kadar piyango tipi call alınıyor, ortalama kayıp ~%50 (%60 olasılıkla tamamı). Dayanak: VP A6, kısa vadeli call'larda −%35/hafta.

| Senaryo | Medyan (E / NLV) | %5 kötü (E / NLV) | P(NLV ≤ −%15) | P(NLV ≤ −%25) |
|---|---|---|---|---|
| Kurala uyum, felaket yok | −%1,6 / −%4,0 | −%4,0 / −%9,9 | ~%0 | ~%0 |
| Kurala uyum, felaket %1/işlem, tavan %15 | −%1,8 / −%4,5 | −%4,4 / −%11,0 | %0,4 | ~%0 |
| Aynısı, tavan %7,5 | −%1,8 / −%4,5 | −%4,4 / −%10,9 | %0,3 | ~%0 |
| **İhlal + felaket %1** | **−%4,6 / −%11,5** | **−%11,8 / −%29,6** | **%37,8** | **%11,6** |
| İhlal + felaket %1, tavan %7,5 | −%4,6 / −%11,4 | −%11,4 / −%28,5 | %37,2 | %10,3 |

**Sonuç:**
- İşlem kuralları (%0,25 risk, ısı, devre kesici) düşmanca rejimde bile kaybı NLV'nin ~%10'unda tutuyor.
- Pre-mortem'in baskın yolu **davranış**. KIM §6 da bunu söylüyor: "kuralın en çok ihlal edildiği an tam bu an"; Kullamägi 2022'de filtreye uymadı ve −%57 yaptı (VA #16).
- Rakamlar varsayıma bağlı; yalnız göreli büyüklük olarak okunmalı.

**En olası birleşik yol (anlatı):**
1. **11–12.11:** CPI'den sonraki ralli FTD verir. İki savunmacı pilot açılır. 17.11'de NVDA güçlü gelir, para büyümeye döner, iki pilot stop olur (−0,55% E).
2. **Kasım sonu:** S&P iki kapanış 200 GHO altında kalır (KIRMIZI). Aralık başında yine SARI olur; 4 pozisyon açılır. 9.12 FOMC'de faiz artırılır (olasılık %67–70, HAZ §2.2). Korele stoplar ve bir gap gelir (−1,2% E).
3. **Bu arada AI tarafı sert bir tepki rallisi yapar** (Daniel-Moskowitz: panik sonrası kaybedenler en sert yükselir; VA #27). Kullanıcı dışarıda kalmıştır. Midas'tan call alır, "kaybı kapatmak" için riski %1'e çıkarır (−4…−6% E).
4. **Sağlık kümesinde bilanço dışı bir haber** (CMS ya da ilaç fiyatı) büyük bir düşük oynaklıklı pozisyonu −%30 gap'le stopun altından açar (−2…−4% E).
5. **Toplam:** E'nin −%6…−10'u, yani NLV'nin **−%15…−25'i**. Vergide 2026 zararı boşa gider. TL mevduata göre ~3 puanlık fırsat maliyeti de eklenir.

---

## 3. Bulgular ve düzeltmeler

### Bulgu 1 (KRİTİK): Durdurma eşiği pre-mortem'i serbest bırakıyor; payda yanıltıcı

**Kuralın testi:**
- PLAN §5.2 ve §8.5 K5'te durdurma eşiği −%15 E.
- PLAN §9.1'in kendi modelinde 1. yıl en büyük düşüşün %5 kötü değeri −%7,4…−8,3 E. Bu, her kenar düzeyi için geçerli.
- SEY §5.2 #1 açık: "Gerçekleşen düşüş > simülasyonun p95'i ise kol durur."
- Plan K5'i SEY §5.2 #1'e dayandırıyor, ama eşiği p95'in ~2 katına koyuyor. Çelişki bu.
- Ayrıca §1 tablosu gösteriyor: −%15 E, NLV'nin −%37,5'i.

**Düzeltme (§5.2 ve §8.5 K5'in yerine):**

| Kademe | Tetik (E'nin %'si, zirveden; NLV karşılığı aşama 1'de) | Eylem |
|---|---|---|
| 1 | −%3 (NLV −%7,5) | Risk × 0,5 (en az %0,125). Piramit yok |
| 2 | −%5 (NLV −%12,5) | Yalnız en güçlü 2 küme. Toplam ısı rejim tavanının yarısı |
| 3 | −%6,5 (NLV −%16) **ya da iki ardışık ayda devre kesici** | 10 seans yeni işlem yok. Yazılı inceleme |
| **Dur** | **−%8 (NLV −%20)**: planın p95'i aşıldı, model yanlış | Plan durur. Yeniden başlamak için yeni hipotez kartı ve Faz 1 |

- $ karşılıkları (−%8 E): 4.000 / 20.000 / 80.000 $ (E = 50k / 250k / 1m).
- **Yazım kuralı:** §5.4'teki her satır ikinci bir sütunla yazılır: "NLV'nin %'si (bugünkü aşamada)". Aylık rapor da (§8.6) iki birimle yazılır.
- **Dayanak:** SEY §5.2 #1; PLAN §9.1 [H]; PROF §3.3 (merdiven ancak rejime bağlı performansta değer katar) [H].
- **Beklenen etki:** Pre-mortem bandının üst yarısı (NLV −%20…−25) kesilir.
- **Bedel:** Kenarı gerçekten +0,15–0,3R olan bir sistemin 1. yılda yanlışlıkla durdurulma olasılığı ~%3–5 [H; §9.1'in p95'inden]. Kalibre edilmemiş bir modelin p95'i olduğu için belirsizlik yüksek.

### Bulgu 2 (KRİTİK): Davranış yolu baskın; ilk 20 işlemde ihlal freni yok

**Kuralın testi:**
- K6 (§8.5) "n ≥ 20'de ihlal oranı > %20 ya da 20 işlemlik blokta ≥ 3 ihlal" diyor.
- İlk 3 ayda tahminen 10–20 işlem var (PLAN §9.6 #5: rejim düşmanca, işlem sayısı düşük). Yani K6 pre-mortem penceresinde fiilen çalışmıyor.
- "Asla" listesi (§10) teknik bir kilit değil. Midas'ta opsiyon alımı zaten açık (HAZ §1.2).
- §2 tablosu: İhlal senaryosu P(NLV ≤ −%15) ≈ %38, P(≤ −%25) ≈ %12 [H].

**Düzeltme:**
1. **Kritik ihlal listesi (n'den bağımsız):**
   - KIRMIZI/TURUNCU'da canlı giriş.
   - Gerçekleşen risk > 1,25 × planlanan 1R.
   - Stopu aşağı çekmek ya da iptal edip yeniden girmemek.
   - Zarardaki pozisyona ekleme.
   - Opsiyon, kaldıraçlı ETF, margin borcu ya da açığa satış.
   - AI kümesinde §4.6 dışında giriş.
   - 17:30–00:00 arası emir değiştirmek.
   - **Yaptırım:** 1. ihlal → 10 seans yeni işlem yok ve yazılı inceleme. 2. ihlal (12 ay içinde) → plan durur (K5).
2. **Teknik kilitler (Pazartesi):**
   - IBKR'de yalnız "Stocks – United States" işlem izni istenir. **Opsiyon izni Faz 2 kapısına kadar istenmez.** PLAN §6.1 ve HAZ §1.3 VİOP tecrübesinin beyan edilmesini öneriyor; beyan edilir, ama izin talep edilmez.
   - IBKR emir ön ayarlarında emir başı değer tavanı E'nin %7,5'i (bulgu 5) ve adet tavanı tanımlanır. Ayarın adı ve yeri 1 adetlik testte teyit edilir; bellekten yazıldı.
   - **Midas'a test için ≤ 500 $ dışında para gönderilmez.** Test bitince bakiye geri çekilir.
3. **Haftalık uyum satırı (Cumartesi):** İhlal sayısı, "dışarıda kalma" günleri ve G2 gölge sonucu yazılır. Fırsat kaçırma duygusu gölge günlüğüne yazılır, hesaba yansımaz.

**Dayanak:** KIM §6 ve §5.3 (risk %1'i aşınca DNA kırılır); VA #16; VP A6–A7 (bireysel opsiyon alıcısı ortalamada kaybeder) [D].
**Beklenen etki:** §2'deki %38'lik yolun büyük kısmı kapanır. Bedeli ~0. Belirsizlik: kilitlerin kendisi de aşılabilir; kural yalnızca sürtünme yaratır.

### Bulgu 3 (ÖNEMLİ): 200 GHO çevresinde rejim whipsaw'u

**Test:** `kirmizi1/rejim_whipsaw.py`, `rejim_var.py` [H].
- Veri: FRED SP500 ve NASDAQ100, Cboe VIX ve VIX3M. Dönem 23.08.2017 – 05.11.2026, 2.314 seans.
- PLAN §2.2'nin hesaplanabilir kısmı kullanıldı. S5FI/S5TH ve FTD yok; SARI tetiği yalnız "S&P veya NDX 10 > 20".

| Ölçü | Sonuç |
|---|---|
| SARI+ bölümü | Yılda 6,2. Yılda 1,9'u 10 seanstan kısa. Durum değişimi yılda 17 |
| **Başlangıçta S&P 200 GHO'nun ±%2 içinde** (bugün +%0,4) | 17 bölüm. **Medyan süre 9 seans; %59'u 10 seanstan kısa; %65'inde 10 seans içinde KIRMIZI.** Bölüm boyunca S&P medyan **−%1,1** |
| Başlangıçta ±%2 dışında | 40 bölüm. Medyan 20,5 seans; %18'i kısa; S&P medyan −%0,2 |
| Günlük durum değişimi | 200 GHO ±%2 içinde günlerin %22,7'si, dışında %4,8'i |
| Örnek | Şubat–Nisan 2022'de 5 kısa SARI bölümü (10.02, 15.02, 22.03, 24.03, 07.04) |
| S&P'nin ertesi gün getirisi, yıllıklandırılmış | SARI+ günlerinde +%10,7; diğer günlerde **+%19,1** |

**Okuma:**
- Endeks düzeyinde filtre, bu örneklemde getiri korumadı. Bu, TEST §0 ve VA §2.1'deki "2010 sonrası filtre getiriyi kesti" bulgusuyla ve Daniel-Moskowitz'in panik sonrası toparlanma bulgusuyla (VA #27) tutarlı.
- Filtrenin faydası ancak kırılım başarısızlık oranından gelebilir. O da ölçülmedi (VA §4.2).
- **Pilot turu başına maliyet:** 2 pilot × ~1,1R = ~%0,55 E (NLV %1,4). SARI'da 4 pozisyonla %1,1 E. Üç ayda 3–4 tur olursa E'nin −%1,7…−4,4'ü.

**Düzeltme (§2.2 ve §2.4'e ek):**
1. **SARI için şartlar 3 kapanış üst üste sağlanmalı.**
   - Önceden seçilmiş üç varyanttan biri. Kısa bölümleri yılda 1,9'dan 1,0'a indirdi; SARI gün payı %63'ten %58'e düştü.
   - Diğer iki varyant fayda vermedi, bu yüzden önerilmiyor: SARI için 200 GHO × 1,02 bandı (kısa bölüm 2,2/yıl) ve 50 GHO şartı (1,6/yıl).
2. **Pilot-başarısızlık freni:**
   - Bir SARI bölümünde açılan pilotların ≥ 2'si 10 seans içinde stop ya da başarısız kırılımla kapanırsa bir sonraki SARI için şart ağırlaşır.
   - Yeni bir ralli denemesinin FTD'si **ve** S&P > 50 GHO gerekir.
   - Dayanak: PROF §1.3 #11 ("kaybederken küçült"); IBD'de FTD sonrası %40–60 maruziyet (PROF §3.1).
3. **Yakın bölge kuralı:** S&P / 200 GHO < 1,02 iken SARI'da tek pilot ve toplam ısı ≤ %0,5.

**Belirsizlik:** n = 17 bölüm, örneklem içi; varyant seçimi tek örneklemde yapıldı. Beklenen etki, çeyrekte ~0,5–1,5% E'lik whipsaw kaybının yarıya inmesi [H].

### Bulgu 4 (ÖNEMLİ): Birlikte tetiklenen bekleyen emirler; margin tipi hesap hatayı borca çeviriyor

**Kuralın testi:**
- §4.4 #5: SARI'da her izinli kümenin 1. ismi tetik listesine giriyor. Bugün 6 izinli küme var (§4.3), yani 6 canlı BUY STP LMT olabilir.
- SARI izni ise günde 2 giriş, en çok 4 pozisyon, ısı %2 ve brüt %30.
- Geniş bir ralli günü (tam olarak FTD ya da CPI günü) altısını birden doldurabilir.
- §6.1'de hesap margin tipinde. IBKR fazlayı borçla finanse eder: %5,38 faiz, Türkiye'de indirilemez (VC #10, #16).
- FTD başarısız olursa 6 pozisyon birlikte stop olur: ~−6,6R = −%1,65 E = NLV −%4.

**Düzeltme (§6.2'ye ek):**
1. **Canlı giriş emri sayısı ≤ min(günlük kalan giriş hakkı; boş pozisyon yeri; ⌊kalan ısı / (1,25 × 1R)⌋).**
2. Daha fazla aday varsa adaylar bir **IBKR OCA grubunda** tutulur: biri dolunca diğerleri iptal olur ("with block"). 2 hak varsa iki ayrı OCA grubu kurulur.
3. Σ(bekleyen giriş tutarı + açık pozisyonlar) ≤ min(brüt tavan; yerleşmiş USD nakit).
4. **Hesap tipi: IBKR nakit hesap.**
   - Bu kullanıcı gün içi işlem yapmıyor ve T+1 takas geçerli; PRA §1.4'e göre good-faith ihlal riski azaldı.
   - Nakit hesapta fazla emir ve OCA miktar hatası **reddedilir**; borca ya da açığa satışa dönmez.
   - Opsiyon spread'i gerekecekse margin'e geçiş Faz 2 kapısında değerlendirilir.
   - Teyit: IBKR nakit hesapta yerleşmemiş satış bedeliyle alım kuralı (1 adetlik test).

**Dayanak:** PLAN §3.5 OCA tuzağı (HU §2.2); VC #15–16 [D]. Beklenen etki: kural dışı maruziyet olasılığı ~0'a iner. Bedel: dolmayan emirlerle kaçan sinyaller ("kaçan" sekmesinde ölçülür).

### Bulgu 5 (ÖNEMLİ): Tek isim gap'i ve ikili olaylar

**Kuralın testi:**
- §3.1 yalnız bilançoyu eliyor. Bugünün 1 numaralı izinli kümesi sağlık; FDA, CMS, ilaç fiyatı ve tıp kongresi verisi ikili olay üretiyor.
- Corpus'taki 2026 tek gün hareketleri: INTC −%30, AMD −%17,3, MU −%17,5, MNTN −%55 (KIM §6; PRA §3.6 #3). CNC 4.11'de tek günde +%12,6 (HAZ §4).
- Tek pozisyon tavanı %15 E = NLV'nin %37,5'i. Bu, Kullamägi'nin hesabın %30'u gece tavanının üstünde (PROF §3.1).
- ADR ≥ %2 şartıyla gerçekçi en büyük pozisyon %12,5 E. Bu pozisyonda −%40'lık bir gap = −%5 E = **NLV −%12,5**. Tek olay pre-mortem'in yarısını üretir.
- §3.4'teki gap-ayarlı risk (1,5 × ATR14) bu kuyruğu görmüyor.

**Düzeltme:**
1. **Faz 1–2'de tek pozisyon ≤ %7,5 E** (NLV'nin ~%19'u; Minervini'nin %20–25'iyle uyumlu, PROF §3.1). Faz 3'te ≤ %10.
   - Bağlayıcı olduğu yer yalnız stop < %3,3. Bu durumda işlem 1R'nin altında riskle açılır.
   - $ karşılığı: 3.750 / 18.750 / 75.000.
2. **§3.1'e ek:** önümüzdeki 10 seansta bilanço dışı ikili olay olan hisse elenir. Olaylar:
   - FDA PDUFA ya da danışma kurulu.
   - Büyük tıp kongresinde pivot veri (ör. LLY, ObesityWeek 14–17.11).
   - Yatırımcı günü ya da kılavuz toplantısı.
   - CMS oran duyurusu, mahkeme ya da düzenleyici karar.
3. **Yönetilen sağlık (CNC tipi) Faz 1'de evren dışı.**

**Dürüst not:** MC'de bu düzeltmenin etkisi küçük; P(NLV ≤ −%15) %0,4'ten %0,3'e iniyor, çünkü işlem başı olasılık düşük. Değeri kuyruğu kesmek; bedeli ~0.

### Bulgu 6 (ÖNEMLİ): Vergi; 2026 kısa yılında zarar boşa gidiyor

**Kuralın testi:**
- Zarar yalnız aynı yıl içinde mahsup ediliyor ve devretmiyor (VC #10 [D]).
- PLAN §6.5 "yalnız vergi için çıkış yapılmaz" diyor.
- Pre-mortem'de Kasım–Aralık'ta E'nin −%3'ü gerçekleşir, 2027 başında aynı büyüklükte kazanç gelir.
  - USD'de sonuç sıfırdır.
  - Ama 2027 kazancı %15–35 marjinal dilimden vergilenir: E'nin ~%0,45 / %0,6–0,8 / %1,05'i (50k / 250k / 1m) [H; 2026 tarifesi doğrulanmadı, VC #11].
- Ayrıca kur her ay ~%1,5 arttığı için USD'de zarar eden lotlar bile TL'de kâr gösterebilir (PRA §2.1).

**Düzeltme (§6.5, 1–4.12 kontrol noktası):**
- 2026'nın net gerçekleşen TL sonucu < 0 ise ve açık pozisyonlarda TL bazında gerçekleşmemiş kâr varsa, en çok zarar kadar kârı olan lotlar 30.12'ye kadar **MOC ile satılır ve ertesi seans MOO ile geri alınır**.
- Şart: geri alım anında kurulumun çıkış sinyali yok.
- Bedel: 2 komisyon (IBKR'de ~0,005R) ve bir gece piyasa dışında kalma.
- Ön koşul: Türkiye'de wash-sale benzeri bir kural olmadığı müşavirle teyit edilir.
- Bu, "yalnız vergi için çıkış yok" kuralının tek istisnası olur.

### Bulgu 7 (ÖNEMLİ): Döviz anahtarının USD'si işlem hesabına girmemeli

**Kuralın testi:**
- §1.5 tetiklenirse servetin USD payı %25–35'e çıkıyor ve "aracı kurumda nakit" kalabiliyor. Bu, E'nin 2,5–3,5 katı demek.
- Üç sonucu var:
  - (a) Risk NLV'ye göre hesaplanırsa 3–9 kat büyür.
  - (b) Servetin üçte biri, hangi kuruluşa bağlanacağı (IB LLC / IBIE) ve yatırımcı korumasının ne olduğu doğrulanmamış bir aracı kurumda toplanır (HAZ §1.2; VC §2 #9).
  - (c) Veraset riski artar: ABD hisseleri US-situs varlık (VA #36); nakdin durumu teyitsiz.

**Düzeltme:** Anahtarın USD'si Türk bankasında döviz mevduatında tutulur. Elde tutulan dövizin kur kazancı vergisizdir (PRA §2.5 [K]). İşlem hesabında yalnız §1.4 aşamasının USD'si durur.

### Bulgu 8 (KÜÇÜK): Tetik–evren uyumsuzluğu ve savunmacı faktör kümesi

**Kuralın testi:**
- SARI'yı "NDX 10 > 20" tek başına açabiliyor (§2.2). Oysa izinli evren savunmacı.
- Test (`kirmizi1/defansif_rotasyon.py`, FF49 VW günlük, 1986–2026/09) [H]:
  - Olay: NDX 252 günlük zirveden ≥ %10 düştükten sonra 10 GHO'nun 20 GHO'yu yukarı kesmesi.
  - Sepet: Hlth, MedEq, Drugs, Insur, Food, Util, Hshld eksi piyasa, sonraki 20 seans.
  - 113 olayda ortalama +%0,02; etki yok.
  - **2010 sonrası 35 olayda −%0,66, %60'ı negatif.** Zayıf ama yönü tutarlı.
- K6, K7 ve K10 (temel tüketim, su/atık, REIT) aynı faiz faktörünü taşıyor. 10.11 CPI ve %4,84–4,90'lık 10 yıllık getiri bu riski canlı tutuyor.
- Korelasyon ilk kez ay sonunda ölçülecek (§4.2); yani ilk girişlerden sonra.

**Düzeltme:**
1. Savunmacı kümelerde (K1, K4–K7, K10) SARI tetiği S&P 10 > 20 ya da FTD olmalı. NDX tek başına yalnız K9 ve K11'i açar.
2. Korelasyon ölçülene kadar K6 + K7 + K10 tek küme sayılır; ısı ≤ %0,75.
3. 60 günlük korelasyonlar 07–08.11'de ölçülür.

### Bulgu 9 (KÜÇÜK): Tek emir penceresi BIST seansıyla çakışıyor

**Kuralın testi:**
- 16:45–17:15 TSİ, BIST sürekli işleminin (kapanış 18:00, HAZ §1.1) ve VİOP'un içinde. Kullanıcı tam o saatte BIST/VİOP işlemi yapıyor olabilir.
- Pencere kaçarsa MOO çıkışları (başarısız kırılım, zaman stopu, trail) da kaçar. Kaybeden pozisyon ~−0,5R yerine tam stopa (−1R) gider.

**Düzeltme:**
- Çıkış emirleri (MOO) ve stop düzeltmeleri sabah **08:00–09:00** rutininde girilir. Kapanış verisi o saatte hazırdır; IBKR'nin seans dışında MOO kabul ettiği 1 adetlik testte teyit edilir.
- 16:45–17:15 penceresi yalnız girişler için kalır (veri günü kuralı korunur).
- **Sabah mutabakatı:** Her açık pozisyonun doğru adetli, canlı bir GTC stopu var mı? Yoksa hemen girilir.

### Bulgu 10 (KÜÇÜK): Kısmi satışta emir sırası

**Kuralın testi:** §3.5'te kısmi MOO ile stop adedinin düşürülmesi aynı pencerede yapılıyor. MOO reddedilir ya da ~17:28 TSİ sınırını kaçırırsa (teyitsiz), stop kalan adede inmiş olur. Pozisyonun yarısı ertesi sabaha kadar stopsuz kalır.

**Düzeltme:**
- Giriş iki alt lotla yapılır (1/2 + 1/2; YEŞİL'de 1/3 + 2/3). Her alt lotun kendi ekli stopu vardır.
- Kısmi satış = alt lot A için MOO, stop A ile aynı OCA grubunda ("cancel, with block").
- Dayanak: HU §2.2 (B'nin iki-bracket yöntemi riski tamamen kaldırıyor). Pazartesi 1 adetlik testlere eklenir.

### Bulgu 11 (KÜÇÜK): 22:00 TSİ olayları ve 8–11.12 olay kümesi

**Kuralın testi:**
- 18.11'de FOMC tutanakları 22:00'de; plan o gün "giriş serbest" diyor (§7.2). DAY buy-stop'lar 22:00 sıçramasında dolup ters dönebilir.
- 9.12 FOMC (artırım olasılığı %67–70), 10.12 CPI ve 11.12 bütçe süresi ardışık günler. Plan yalnız 9.12 için "yeni giriş yok" diyor; açık pozisyonlar üç olayı birden taşıyor.

**Düzeltme:**
1. 22:00 TSİ olayı olan günlerde giriş emirleri GTD olarak girilir, **21:55 TSİ'de (13:55 ET) düşer**. IBKR GTD saat seçeneği testte teyit edilir.
2. 8.12 kapanışında gap-ayarlı ısı yeniden hesaplanır: gap = max(1,5 × ATR14; 2 × S&P ima edilen hareketi × hisse betası). Toplam ≤ rejim tavanı olmalı.
   - Aşan kısım için en düşük R'li pozisyon 9.12 MOO ile kapatılır.
   - Dayanak: PROF §3.5 #5'in bilanço kuralının makro olaya uyarlanması [Ö].

### Bulgu 12 (KÜÇÜK): TL algısı ve 40 seans kuralı

**Hesap [H]:**
- TL mevduat net ~%37,9 (VC #4) → 3 ayda +%8,4.
- Kur yıllık %20 → 3 ayda +%4,7. Yani TL mevduatın USD karşılığı 3 ayda +%3,5.
- IBKR boş nakit faizi 3 ayda +%0,85.
- Fark: boş USD çeyrekte ~2,7 puan geride. Aşama 1'de (E'nin %40'ı) bu ~%1,1 E eder.
- İşlem sonucu −%10 NLV iken kullanıcı TL'ye göre ~−%13 algılar.

**Düzeltme:**
- Çeyrek içinde TL kıyasıyla karar verilmez. TL kıyası yalnız 12 aylık K10 kapısında kullanılır.
- Aylık rapor USD, NLV ve "TL mevduata göre" sütunlarıyla yazılır.
- 40 seans kuralının (§1.4) çevrim makası ilk transferde ölçülür (VC #16: ölçülmedi).

---

## 4. Kural–yol matrisi

| Plan kuralı | Whipsaw | Gap | Tema/faktör | CPI/FOMC | Kur | Vergi | Aracı kurum/uygulama | Davranış |
|---|---|---|---|---|---|---|---|---|
| %0,25 risk, ısı %2/%3 | Tutar | Kısmen | Tutar | Tutar | — | — | — | **Kırılır** (bulgu 2) |
| Rejim anahtarı | **Zayıf** (bulgu 3) | — | Uyumsuz (8) | Kısmen | — | — | — | Sıkılma üretir (2) |
| Devre kesici %3 / merdiven / K5 | Tutar | Tutar | Tutar | Tutar | — | — | — | **Gevşek** (1) |
| Gap-ayarlı ısı, en kötü hafta | — | Tek isim kuyruğunu görmez (5) | Tutar | Kısmen (11) | — | — | — | — |
| Bilanço yasağı | — | İkili olay yok (5) | — | — | — | — | — | — |
| Emir rutini, OCA hijyeni | — | — | — | 22:00 olayı (11) | — | — | **Fazla tetik (4), MOO sırası (10), pencere (9)** | — |
| Döviz anahtarı, kademeli çevrim | — | — | — | — | Tutar; USD yeri yanlış (7) | — | Yoğunlaşma (7) | Boyut karışıklığı (7) |
| Vergi kaydı | — | — | — | — | — | Zarar boşa gider (6) | — | — |
| K6 ihlal kriteri | — | — | — | — | — | — | — | **İlk 20 işlemde yok** (2) |

---

## 5. Hesaplar ve betikler (scratchpad; repoya yazılmadı)

| Betik | İçerik |
|---|---|
| `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/kirmizi1/premortem_mc.py` | 3 aylık pre-mortem MC (§2) |
| `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/kirmizi1/rejim_whipsaw.py` | Rejim bölümleri, 200 GHO yakınlığı (bulgu 3) |
| `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/kirmizi1/rejim_var.py` | Önceden seçilmiş üç histerezis varyantı (bulgu 3) |
| `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/kirmizi1/defansif_rotasyon.py` | Savunmacı sepet ve NDX toparlanma olayı (bulgu 8) |

**Veri:** `scratchpad/data/fred/SP500.csv` (2016–2026; 5.11 kapanışı 7.353,73 elle eklendi, VA #31), `fred/NASDAQ100.csv`, `cboe_VIX.csv`, `cboe_VIX3M.csv`, Ken French 49 endüstri günlük (Eylül 2026 sürümü).

## 6. Sınırlar

- **MC (§2):** Bütün parametreler öznel. Kötü rejim bilinçli olarak düşmanca seçildi (E ≈ −0,4R). İhlal davranışı bir varsayım; olasılıklar yalnız göreli okunmalı.
- **Rejim testi:** FTD ve genişlik koşulları yok; S&P serisi yalnız 2016'dan başlıyor; n küçük. Endeks getirisi, kırılım başarısını ölçmüyor.
- **Savunmacı sepet:** FF49 endüstri vekilleri, izin verilen hisseler değil. Tekil hissede kuyruk daha kalın (PROF §3.2 #5).
- **Teyitsiz uygulama ayrıntıları:** IBKR emir ön ayarları, nakit hesapta yerleşmemiş bedel kuralı, GTD saati, MOO'nun seans dışında kabulü ve OCA içinde MOO bellekten yazıldı. Hepsi Pazartesi 1 adetlik testte doğrulanmalı.
- **Vergi:** "Kazanç hasadı" istisnası ve wash-sale yokluğu müşavir teyidine bağlı. 2026 tarifesi doğrulanmadı (VC #11).
