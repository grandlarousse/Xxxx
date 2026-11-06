# Hakem raporu (UYGULAMA merceği): ABD planları A, B, C

**Tarih:** Cuma 06.11.2026, ~14:00 TSİ. Son kapanış 05.11; NFP sonrası Cuma kapanışı bu değerlendirmede yok.
**Mercek:** Bu kullanıcının Pazartesi 09.11'de planı uygulayıp uygulayamayacağı ve riski. Bakılan noktalar: aracı kurum erişimi, gün içi ekran olmadan uyarlama, emir tipleri, boyut hesabı, gap riski, en kötü hafta.
**Okunanlar:**
- Üç taslak (`taslak/abd_A.md`, `abd_B.md`, `abd_C.md`).
- `abd_hafta_hazirlik.md`.
- Doğrulama dosyaları: `v_abd`, `v_capraz`, `v_profesyonel`, `v_dalga`.
- `abd_profesyonel` §3.5, `abd_pratik` §2.5–2.6 ve `seytan_taban_oranlar` §5.

**Bağımsız kontroller** (hakem betikleri; scratchpad'de, repoya yazılmadı):
- `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/hakem_uyg/n25_check.py`: B'nin çekirdek backtest'ini Ken French günlük verisiyle yeniden ürettim.
- `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/hakem_uyg/vix_check.py`: C'nin S3 (VIX çözülme) testini, koşulsuz piyasa getirisine göre yeniden ölçtüm.

Bu bir yatırım tavsiyesi değildir. Vergi kalemleri mali müşavirle teyit edilmelidir.

---

## 1. Puan tablosu (0–10)

| Ölçüt | A | B | C |
|---|---|---|---|
| Kanıta sadakat | 7 | 7 | 6 |
| Pazartesi uygulanabilirliği (ekransız, erişim, emir tipi) | 8 | 5 | 8 |
| Risk kontrolü ve en kötü durum | 8 | 6 | 9 |
| Beklenen değerin engel karşısında gerçekçiliği (TR vergisi dahil) | 8 | 9 | 8 |
| Profile uyum (swing, yüksek ödül, küme) | 9 | 4 | 7 |
| **Toplam / 50** | **40** | **31** | **38** |

**Kazanan: A. C yakın ikinci.**
- A temel alınmalı, risk kabuğu C'den alınmalı (§4).
- B'nin çekirdeği bu kullanıcı için reddedilmeli. B'den yalnız uygulama ve vergi parçaları alınmalı.

**Gerekçe.**
- Üç plan da Pazartesi için doğru sonuca varıyor: canlı lider işlemi yok.
- A, kullanıcının istediği tarzı (lider swing, küme, kanıt gelirse yüksek ödül) en iyi emir mekaniğiyle kuruyor:
  - Korumada stop-market kullanıyor, stop-limit değil.
  - Stoplar yalnız normal seansta (RTH) tetikleniyor.
  - Kısmi satışta OCA tuzağına karşı uyarı var.
  - MOO son giriş saatini hesaba katıyor.
  - Midas'ı emir tipi şartına bağlıyor.
- C riskte en sıkı plan. Ama S3'ün kanıtını abartıyor ve kısmi satış emrinde operasyonel bir tuzak var (§3).
- B'nin en büyük risk bileşeni, kaldıraçlı ve rejim kapılı bir endeks betası. Bu bileşen kullanıcının "al-tut yok" ve swing ufku şartlarıyla çelişiyor.

---

## 2. Uygulama denetimi: kalem kalem

### 2.1 Erişim (Pazartesi gerçeği)

**Pazartesi neye erişilebilir?**
- IBKR'de ilk işlem gerçekçi olarak 11–13.11 (`hazırlık` §1.3).
- Midas onayı 1–2 gün sürüyor (üçüncü taraf kaynağı). Midas'ta stop-limit, GTC ve MOO desteği **bilinmiyor** (`hazırlık` §1.2, §7).
- IBKR'de Türk müşterinin bağlanacağı kuruluş (IB LLC mi IBIE mi) ve buna bağlı ABD ETF erişimi doğrulanmadı (`hazırlık` §1.2; `v_abd` §4 #7, bellek).

**Bu belirsizliklere karşı planların dayanıklılığı:**

| | A | B | C |
|---|---|---|---|
| ABD ETF'ine bağımlılık | Yok; ETF yalnız ölçüt olarak kullanılıyor | **Yüksek.** Çekirdek SPY/SSO ya da MES; Uydu-R tamamen ETF | Düşük. Yalnız S3 SPY kullanıyor; CSPX yedeği var |
| Midas'ta emir tipi bilinmezliği | "STP LMT ve GTC yoksa Midas kullanılmaz" | Pazartesi XLV için **MOO + GTC stop varsayıyor**; SSO'nun Midas'ta olup olmadığı da bilinmiyor | Midas yalnız limit emirli kollarda; S1 IBKR'yi bekliyor |
| Yüzdesel komisyonun maliyeti (R cinsinden) | Var: %3 stopta 0,17–0,2R | Kısmen var | En net hali: %6 stopta 0,08R (doğru hesap) |
| 50k hesapta en zayıf halka | Veri maliyeti (bunu ele alıyor) | MES için çekirdek ≥ 75k gerekiyor. ETF engellenirse **çekirdek 50k'da uygulanamıyor** | Veri maliyeti |

### 2.2 Ekransız uyarlama ve emir tipleri

- Üç plan da aynı iskeleti kullanıyor ve iskelet doğru:
  - Seans öncesinde DAY buy-stop-limit giriş.
  - GTC sell-stop koruma, yalnız RTH'de tetiklenir.
  - Çıkış kararı kapanışa göre verilir, ertesi açılışta MOO ile uygulanır.
- **A en ayrıntılı plan:**
  - Neden stop-limit değil stop-market kullandığını açıklıyor: gap'te stop-limit dolmayabilir.
  - "17:25'ten sonra MOO yok" kuralı var.
  - Kısmi satışta OCA "orantılı küçült" uyarısı var.
  - Başarısız kırılım ve 10 seanslık zaman stopu var.
  - Haftalık acil stop yükseltmesi var.
- **C'nin tek emir penceresi (16:45–17:15)** sabah 16:30'daki ABD verisinden sonra açılıyor. Her gün aynı ritim; bu kullanıcı için en temiz uygulama.
- **C'de kısmi satış tuzağı var.** 1/3'lük +2R GTC limit, tam adetli stopla OCA'da tutuluyor ve C margin tipi hesap öneriyor.
  - OCA azaltma davranışı yanlış kurulursa limit dolduktan sonra stop tüm adedi satar. Sonuç istenmeyen açığa satış olur.
  - A bu riski açıkça yazıyor.
  - B'nin "iki ayrı bracket" yöntemi (1/3 için kendi limiti ve stopu, 2/3 için kendi stopu) riski tamamen ortadan kaldırıyor.
- **Boyut tetik fiyatına göre hesaplanıyor (üç planda da).** Gap'te dolum limit fiyatından olabilir.
  - A'nın örneğinde (stop %5,6, limit +%1,5) gerçekleşen risk ~1,27R'ye çıkar.
  - Düzeltme: adet = risk $ / (limit − stop).
- **Stop alt sınırı EOD kanıtıyla çelişiyor.**
  - `v_profesyonel` A12: kapanış bazlı mekanik kopyada 1 ATR stop kötü sonuç verdi.
  - A'nın S1 bandı 0,6–1,5 ATR, C'ninki 0,75–2 ATR. B'de alt sınır hiç yok.
  - Üçü de <1 ATR stopa izin veriyor. EOD uyarlamada taban **≥ 1,0 ATR** olmalı [hakem önerisi, Ö].

### 2.3 Boyut hesapları (yeniden hesaplandı)

- **A, Örnek 1 (stop 5,60 $):** 22 / 111 / 446 adet. Tutar 2.202 / 11.111 / 44.645 $. Gap-ayarlı ısı %0,33. **Doğru.**
- **A, Örnek 2 (stop 1,65 $):** 75 / 378 / 1.515 adet. Gap-ayarlı ısı %0,27. **Doğru.**
- **C (stop 6 $):** 20 / 104 / 416 adet. IBKR gidiş-dönüş 2 / 2 / 4,16 $, yani 0,016 / 0,003 / 0,002R. İş TMI ~0,08R. **Doğru.**
- **B:**
  - Dilim ısısı %7 × %12 = %0,84; üç dilimle %2,5. **Doğru.**
  - 1 MES ≈ 5 $ × 7.354 ≈ 36,8k $ nominal. **Doğru** (çarpan bellekten, teyit gerekiyor).

### 2.4 Gap riski ve en kötü hafta [hakem hesabı]

**Stres varsayımı.** Korele bir gecede gap −%15. Dayanak: 5.11'de SOXX −%12, MU −%17,5, AMD −%17,3 (`hazırlık` §0, §6).

**Pazartesi haftası (9–13.11), hesap fonlanmış varsayımıyla:**

| Plan | Bu hafta açılabilecek risk | En kötü hafta |
|---|---|---|
| A | R0: sıfır. R1: ≤2 pilot, brüt ≤ ~%15 | ≤ −%2,3 (A kolu) |
| B | XLV dilimi %7 (üç dilim geçerse %21); ETF haftalık −%8 | −%0,6 (−%1,7) (H) |
| C | Sıfır, yalnız 1 adetlik testler. S3 tetiklenirse SPY %12,5 × −%10 | −%1,25 (E) |

**Tavanlar açıldığında, en kötü hafta:**

| Plan | Hesap bazında | Toplam servete etkisi |
|---|---|---|
| A, R3/L3 (brüt ≤ %100, 8 pozisyon) | ~−%15. Isı tavanı %5'in 3 katı | Kol servetin %10–20'siyse −%1,5 ile −%3 |
| B, YEŞİL+ (brüt %155) | ~−%18 ile −%25 (H). Ayrıntı aşağıda | H servetin %15–25'iyse **−%3 ile −%6** |
| C, Faz 1 YEŞİL | −%6 ile −%7,5 (E) | E servetin %10'uysa −%0,6 ile −%0,75 |
| C, Faz 3 (≤1,3x marj) | ~−%20'ye kadar (E) | — |

- **B'nin en kötü haftası, çekirdek ayrıntısıyla:**
  - N25'in en kötü 5 günü −%34,5 (Ekim 1987) ve 2000 sonrasında −%19,5 (Şubat 2020; hakem yeniden üretimi).
  - Çekirdek H'nin %50'si olduğu için bu, H'de −%17 / −%10 eder.
  - Uydu ve lider kollarının %55 brütüne −%15 eklenince toplam ~−%18 ile −%25 olur.
- **Sonuç.** En kötü hafta sıralaması C < A < B. B'de kuyruk yapısal: oynaklık hedefi Şubat 2020'de geç kaldı. Sakin dönemde L≈2'ye çıkılmıştı.

### 2.5 Olay günleri (CPI 10.11, AMAT/CSCO 12.11, NVDA 17.11)

| | CPI günü kuralı | Değerlendirme |
|---|---|---|
| A | 16:30'dan önce yeni emir yok. Vadeli −%1'in altındaysa giriş iptal | Asimetrik ama işe yarıyor: yukarı gap'te limit zaten dolumu engelliyor |
| B | 16:45'ten önce emir yok | Yeterli |
| C | 16:45'ten önce emir yok. Vadeli ±%1,5 oynarsa o gün giriş yok | En temiz kural |

- **NVDA:** Üç plan da 17.11 AMC'yi (01:00 TSİ, 18.11) kullanıyor. Bu tarih `hazırlık` §2.1'deki NVIDIA IR kaynağından. Görev notundaki "~19.11" eski bilgi; çelişki planlarda değil, notta. Yine de IR sayfasından teyit edilmeli.

---

## 3. Ölümcül ya da kritik kusurlar

### A (ölümcül kusur yok, düzeltilmesi gereken üç nokta)
1. **S1 stop tabanı 0,6 ATR.** EOD'de <1 ATR stopun kötü sonuç verdiği tek kanıtla çelişiyor (`v_profesyonel` A12). Taban ≥ 1,0 ATR olmalı.
2. **S2 (bilanço gap'i, 2.–5. gün) canlı kol olarak zayıf.** PEAD büyük hissede yok (`v_abd` #23). Earnings sinyallerinin long-only üst portföyü VW piyasayı geçmiyor (`abd_test` §6.4). EOD uyarlaması test edilmedi. İlk 30 işlemde yalnız gölge günlükte kalmalı.
3. **Boyut tetik fiyatına göre.** Limit fiyatına göre hesaplanmalı (§2.2).
   - **Ek not:** R0'dayken de A kolunun %50'si USD'ye çevriliyor. A'nın kendi hesabıyla bu, boşta duran kısımda ayda ~%0,8–0,9 carry kaybı demek. B'nin kademeli transferi daha iyi.

### B
1. **Çekirdek profile aykırı ve en büyük risk kaynağı.**
   - H'nin %50'si, kaldıraçla rejim kapılı bir endeks betası. Aylar ya da yıllarca açık kalabilir; bu fiilen kaldıraçlı al-tut.
   - En kötü 5 gün: 1987'de −%34,5, Şubat 2020'de −%19,5. H bazında −%17 / −%10.
   - Doğrulanmış çapa da aynı yönde: 2010 sonrası filtre getiriyi kesti (`v_abd` §2.1). B bunu kabul ediyor ("sigorta, motor değil"). Ama kullanıcının aradığı şey bu değil.
2. **Uygulama, doğrulanmamış erişime bağlı.**
   - Midas'ta MOO, GTC ve SSO.
   - IBIE/PRIIPs ETF engeli.
   - MES için ≥ 75k çekirdek ve vadeli izni.
   - Yurt dışı vadeli kazancının vergi niteliği belirsiz.
   - ETF engellenirse 50k hesapta çekirdeğin uygulanacak aracı kalmıyor.
3. **Pazartesi XLV alımı kendi kuralından sapıyor.**
   - Ay sonu takvimi dışında yapılıyor.
   - 12 aylık veri yok; yaklaşık olarak YTD kullanılıyor.
   - VIX vade yapısı tersken (1,10) MOO ile yeni risk alınıyor. "Sıkı rejim anahtarı" çapasıyla çelişiyor.
   - Risk küçük, ama bu kural gevşekliği kalıcı olur.
4. **Sistematik kollarda merdiven yok.** Yalnız −%20 / −%25 / −%30 frenleri var. Plan H'de −%30'a kadar düşüşü tolere ediyor.
5. **Küçük hata.** "1950 sonrası günlerin ~%27'si σ̂ ≤ %12,5" deniyor. Hakem hesabıyla bu oran 1950 sonrası ~%52, 2000 sonrası ~%30.
   - Buna karşılık B'nin ana sayıları birebir tekrarlandı: N25 1928+ %13,8 / −%44,3; 2000+ %10,5 / −%25,4; 2010+ %13,8 / −%24,1.

### C
1. **S3'ün kanıtı abartılı.**
   - "40 gün, t = 3,69" sonucu T-bill'e göre fazla getiriyi ölçüyor; bu çoğunlukla hisse primi.
   - Koşulsuz 40 günlük piyasaya göre (+%2,1) fark +1,8 puan, **t ≈ 1,71**. Rastgele tarih testinde p ≈ 0,05 (hakem `vix_check.py`). İki tanım denendi, test örneklem içi.
   - Nagel atfı kısa vadeli reversal faktörü için, SPY zamanlaması için değil.
   - Bu yüzden §2.0'daki "kalan üç kolun her biri doğrulamadan geçmiş bir bulguya dayanıyor" iddiası S3 için yanlış. S2 için de yanlış: yayın sonrası testi yok, %3,8 rakamı teyitsiz.
2. **Kısmi satış emrinde OCA miktar tuzağı** (margin tipi hesapta istenmeyen açığa satış). B'nin iki ayrı bracket yöntemine geçilmeli.
3. **S2 Pazartesi uygulanamıyor.**
   - openinsider 503 veriyor.
   - "Rutin insider" ayıklaması için EDGAR Form 4'ü 3 yıl geriye elle taramak gerekiyor. İş yükü yüksek.
   - Kol ertelenmeli.
4. **S1 iş yükü yüksek.** Her hafta her aday için dört maddelik bilanço filtresi elle toplanıyor (Nasdaq, Yahoo). C'nin kendi notuna göre filtre alfa üretmiyor (0 ile +2 puan). İlk ayda sadeleştirilebilir.

---

## 4. Aşılanacak en iyi fikirler (öncelik sırasıyla)

1. **(A + C) Pazartesi canlı lider işlemi yok.** Fonlanan hesapta 1 adetle emir testi yapılır: GTC stop (RTH), buy-stop-limit (DAY), MOO, bracket. Testi geçmeyen platform o emir tipi için kullanılmaz (A §6.1; C §2.5).
2. **(C) Tek emir penceresi 16:45–17:15 TSİ ve simetrik veri kuralı.** CPI/PPI sonrası vadeli ±%1,5'ten fazla oynarsa o gün yeni giriş yok (C §3.4).
3. **(B) Kısmi satış için iki ayrı bracket.** 1/3 kendi +2R GTC limiti ve stopuyla, 2/3 kendi GTC stopuyla; OCA miktar oyunu yok. Varsayılan seçenek A'nınki: kapanışta karar, MOO ile uygulama (B §2.4; A §2.7).
4. **(Hakem) Boyut ve stop düzeltmesi.**
   - Adet = risk $ / (limit − stop).
   - Stop 1,0–2,0 ATR ve ≤ %8.
   - Gap-ayarlı ısı = adet × max(stop, 1,5 ATR); bilanço penceresinde 2 × implied move.
   - Dayanak: `v_profesyonel` A12; `abd_profesyonel` §3.5 #5.
5. **(C) Faz 1 risk kabuğu, A'nın tavanlarının yerine.**
   - Toplam ısı KIRMIZI/SARI/YEŞİL: %1 / %2 / %3.
   - Küme ısısı %0,75; sağlık tek küme.
   - Aylık kesici min(%6; 12R) = %3.
   - Merdiven −%4 / −%7 / −%10 / −%15 (C §5).
6. **(Hakem) En kötü hafta tavanı, yeni bir kural.** Σ pozisyon × max(stop %, %15) ≤ kolun %6'sı (Faz 1) [Ö]. Yalnız ısıya bakmak gap'te 2–3 kat yanıltıyor (§2.4).
7. **(B) TL'den USD'ye kademeli geçiş.**
   - Yalnız rejimin kullanabileceği kısım taşınır, kalanı banka PPF'sinde ya da mevduatta bekler.
   - Boştaki USD T-bill'de değil aracı kurum nakdinde durur ("hayalet vergi": C §1.2; B §6.5; `abd_pratik` §2.5). Bu, mali müşavir teyidine bağlı.
8. **(C) Maliyeti R cinsinden ölç.**
   - Türk aracı kurumlarında komisyon %6 stopta ~0,08R, %3 stopta 0,17–0,2R. Bu yüzden ana platform IBKR.
   - Maliyet + kayma > 0,15R olursa yöntem değiştirilir (A K3; `seytan_taban_oranlar` §5.2 #3).
9. **(B, C) Hesap büyüklüğüne göre vergi sonrası tablo.**
   - B §8.3: 50k / 250k / 1m'de vergi sonrası USD; R = 0'da bile −%3 civarı.
   - C §1.2: boyuta göre engel.
   - Kullanıcıya gösterilecek ana tablo bu olmalı.
10. **(C) TR'ye özgü döviz anahtarı ve "kaçan sinyal" sekmesi.**
    - Döviz anahtarı işlem kenarından bağımsız. İlk kontrol: Perşembe 12.11 rezerv verisi.
    - Kaçan sinyal sekmesi, ekransız ve limitli girişin bedelini ölçer (C §1.3, §7.2).

---

## 5. Doğrulanmış bilgilerle çelişkiler

| Konu | Taslak | Doğrulanmış bilgi | Hüküm |
|---|---|---|---|
| EOD stop tabanı | A 0,6 ATR; C 0,75 ATR; B taban yok | `v_profesyonel` A12: kapanış bazlı 1 ATR stop kötü sonuç verdi | Çelişki. ≥ 1 ATR olmalı |
| S3 kanıtı | C "t = 3,69", "doğrulanmış bulgu" | Hakem: koşulsuz piyasaya göre t ≈ 1,71, örneklem içi; Nagel STR için | Abartı |
| Insider %3,8 / 21 gün | C kullanıyor ve "teyitsiz" diye işaretliyor | `v_abd` #26: yalnız 82 bp/ay (1986–2007) doğru; yayın sonrası test yok | Uyarı yeterli, ama kol kanıtsız |
| Sektör/tema rotasyonu | B'de H'nin %30'u | `v_abd` §2.2, `v_dalga` U4/U7: risk-ayarlı ≈ piyasa; 2015+ bilgi yok | B dürüst ("piyasa ± 4"). Ama kenarı olmayan bir kola %30 sermaye |
| Kaldıraçlı trend | B çekirdeği | `v_abd` §2.1: 2010+ filtre getiriyi kesti; MaxDD −%55/−%97 (2x/3x NDX) | B'nin vol hedefli S&P sürümü daha yumuşak (−%25/−%44), çapayla uyumlu. Profile aykırı |
| FTD eşiği | A: S&P +%1,25 / NDX +%1,5. B: +%1,25. C: +%1,5 | `hazırlık` §3: +%1,5, artan hacim | A ve B'de küçük sapma. Tek eşikte birleştirilmeli |
| σ̂ ≤ %12,5 gün oranı | B "1950+ ~%27" | Hakem: 1950+ ~%52, 2000+ ~%30 | Küçük hata |
| NVDA tarihi | A, B, C: 17.11 AMC | `hazırlık` §2.1 (NVIDIA IR) | Planlar doğru. Görevdeki "~19.11" eski |
| Midas emir tipleri | B varsayıyor; A ve C koşula bağlıyor | `hazırlık` §7: bilinmiyor | B riskli |
| IBKR kuruluşu ve ETF erişimi | B'de kritik; C'de S3 için | `hazırlık` §1.2; `v_abd` §4 #7: doğrulanmadı | B için kırılma noktası |
| TL engeli | A ve B ~%20–28; C boyuta göre %12,7–25,9 (u=0,3) | `v_capraz` #22: ~%28 cebir doğru; `abd_pratik` §2.6: u=0,6'da %23,5 | C'nin düşük rakamları düşük u'ya ve "dövizin kur kazancı vergisiz" varsayımına (`abd_pratik` §2.5, teyitsiz) dayanıyor. Ölçek büyüyünce (u → 1) %22–30'a döner |
| 2026 tarifesi, BSMV | Hepsi "doğrulanamadı" diyor | `v_capraz` #11 ve eksikler listesi | Tutarlı |

---

## 6. Pazartesi için birleşik karar (A tabanı + aşılar)

- **Cumartesi:** Cuma kapanışıyla rejim tablosu doldurulur.
  - VIX/VIX3M ≥ 1 ise canlı lider işlemi yok.
  - < 1 ise de en erken FTD Çarşamba 11.11.
- **Pazartesi:**
  - Fonlanan hesapta 1 adetle emir tipi testleri (§4 #1).
  - İzleme listesinde her aday için pivot, limit, 1–2 ATR stop, adet (limit fiyatına göre) ve bilanço tarihi yazılır.
  - IBKR'de kuruluş ve ETF erişimi **yazılı** sorulur.
  - Canlı risk: sıfır.
- **Salı (CPI):** 16:45'ten önce emir yok. Vadeli ±%1,5'ten fazla oynarsa yeni giriş yok.
- **Rejim SARI/R1'e dönerse:** en çok 2 pilot. Koşullar:
  - %0,25 risk, farklı ve AI dışı kümeler.
  - Gap-ayarlı ısı ≤ %1–2.
  - En kötü hafta tavanı ≤ kolun %6'sı.
- **Beklenti (dürüst):** 1. yıl vergi öncesi USD medyanı kabaca −%3 ile +%6, kenar yoksa negatif (A §8; C §8.1). TL kökenli parada engelin altında kalır. Bu bir ölçüm bedelidir. Sermaye ancak 100 işlem, 12 ay ve önceden yazılmış kapılar geçilirse büyür.
