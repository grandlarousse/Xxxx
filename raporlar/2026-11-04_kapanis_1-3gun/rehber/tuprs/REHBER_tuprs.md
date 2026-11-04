# TUPRS ← ABD rafinerileri: uygulama rehberi

_04.11.2026 · veri: Yahoo günlük 03.11.2026 ABD kapanışına kadar, VİOP bülteni 03.11.2026'ya kadar · etiket: rehber_tuprs_kur, denetim: rehber_tuprs_denetim (bkz. §13) · yatırım tavsiyesi değildir_

## 1. Tek paragrafta
Dört ABD rafinerisi (VLO, MPC, PSX, PBF), bir önceki ABD gününde S&P 500'den bağımsız olarak belirgin biçimde yükseldiyse ya da düştüyse, TUPRS vadelisi sonraki iki BIST gününde aynı yöne kayma eğiliminde. Strateji bu farkı kullanıyor. Sinyal yalnız **önceki gecenin ABD kapanışlarından** hesaplanıyor; ABD kapanışından sonra (kışın 00:00, yazın 23:00 TSİ) kesindir. BIST fiyatı sinyale girmez, bu yüzden TradingView'ın 15 dakikalık gecikmesi sinyali etkilemez. Gecikme yalnız emir fiyatını etkiler; emir fiyatını aracı kurum ekranından alın. İşlem TUPRS pay vadelisinde, uzlaşma penceresinde (18:00–18:10) açılıp kapatılıyor; tutma süresi 2 BIST günü.

**Güven: ORTA (sinyalin varlığı), kârlılık için DÜŞÜK–ORTA.**
- 2017–26 tam dönem: pozisyon başına net +49 bps, t 2,5.
- 2024–26: net +30 bps, t 0,9 (anlamlı değil).
- Strateji şu anda 2024–26'nın en derin düşüşünde (Temmuz–Ekim 2026).
- Bağımsız denetim (§13): bps sonuçları birebir tekrarlandı. TL sonuçları aşağı düzeltildi (ort. +94 TL/kontrat, 2024–26 +40 TL). Eşik 0,75–1,25 ve tutma 1–3 gün varyantlarının dokuzu da 2024–26'da pozitif (+14 ile +45 bps), ama hiçbiri anlamlı değil. Tutma 1 gün zayıf.

## 2. Kesin kural (araştırma `c1_ref.py` ile birebir)
1. **Getiriler:** her ABD günü için r_i = ln(adj_t / adj_t−1). i = VLO, MPC, PSX, PBF; adj temettü düzeltmeli kapanış.
2. **Beta:** β_i, son 250 ABD gününde r_i'nin S&P 500 getirisine regresyon betası (cov/var). En az 100 gözlem gerekir; o günün kendisi dahil edilmez.
3. **Sepet artığı:** artık_i = r_i − β_i · r_SPX. P = dört artığın ortalaması; en az 3 hisse dolu olmalı.
4. **ABD günlerini BIST günlerine eşleme:** BIST günü t'ye, tarihi önceki BIST günü ≤ d < t olan ABD günleri atanır.
   - BIST tatilinde arada kalan ABD günleri toplanır.
   - t'den önceki ABD günü tatilse P boştur → **sinyal yok.**
5. **z skoru:** z_t = P_t / std(P, önceki 250 BIST günü; en az 100 dolu).
6. **Açılış:** pozisyon yokken |z_t| > 1 ise yön(z_t) ile açılır (z > 0 → uzun, z < 0 → kısa). Kontrat, t günü vadeye **en az 3 BIST işlem günü** kalan en yakın TUPRS vadelisidir. Giriş t günü 18:00–18:10'da (uzlaşma).
7. **Çıkış günü** t+2. BIST günüdür. O sabah z yeniden hesaplanır:
   - |z| > 1 ve aynı yön → **UZAT.** Hiç işlem yapılmaz, yeni çıkış günü 2 BIST günü sonrası. Kontratın vadesine <3 iş günü kaldıysa o gün sonraki vadeye roll yapılır.
   - |z| > 1 ve ters yön → **ÇEVİR.** Mevcut pozisyon kapanır, ters yönde yenisi açılır. Kontrat aynıysa bu tek emirdir (pozisyonun 2 katı ters emir). Tutulan kontratın vadesine <3 iş günü kaldıysa iki ayrı emir gerekir: eski kontratı kapat, yeni ön vadede ters aç (27.10.2026 örneği, §5).
   - Aksi halde → **KAPAT** (18:00–18:10).
8. **Ara günler:** pozisyon açıkken çıkış günü dışındaki günlerde yeni sinyale bakılmaz. Kapattığınız günün ertesinden itibaren yeniden sinyal aranır.
9. **Uzatma sınırı** yok. Geçmişte en uzun pozisyon 8 BIST günü sürdü.

## 3. Saat saat uygulama (TSİ)

| Ne zaman | Ne yapılır |
|---|---|
| **Gece 00:00 (kış) / 23:00 (yaz)** | ABD kapanışı. 01.11.2026'dan 14.03.2027'ye kadar ABD kış saatinde, kapanış 00:00 TSİ. Sinyal bu andan itibaren kesindir. |
| **Sabah 08:30–10:00** | `python3 sinyal_tuprs.py --sermaye <TL> --risk 0.5` çalıştırılır. Çıktıda şunlar bulunur: kullanılan ABD günleri, z, SİNYAL, kurala göre pozisyon bağlamı (AÇ / TUT / UZAT / ÇEVİR / KAPAT), işlem kontratı ve uzlaşması, kontrat sayısı, ertesi seansın tetik seviyesi. "ABD verisi eksik" uyarısı çıkarsa işlem yapılmaz. İsterseniz TradingView'da `tuprs.pine` göstergesine de bakın; yalnız teyit içindir, betik esastır. |
| **Gün içi** | Bir şey yapılmaz. Gün içi stop ya da kâr al yoktur; bunlar test edilmedi. |
| **17:45** | Aracı kurum ekranında işlem kontratının (ör. F_TUPRS1126) alış/satış kademelerini, son fiyatını ve limite yakınlığını kontrol edin. TradingView'daki BIST:TUPRS1! fiyatı ücretsiz hesapta 15 dk gecikmelidir; emir fiyatı için kullanılmaz. |
| **17:55** | Emir hazırlanır. Adet betiğin hesabından alınır. ÇEVİR gününde emir adedi 2 katıdır (kontrat değişiyorsa iki ayrı emir: kapat + yeni vadede aç). |
| **18:00–18:10** | Uzlaşma penceresi; uzlaşma ≈ son 10 dakikanın ağırlıklı ortalaması. Pay vadelisi 18:10'da kapanır (endeks vadelisi 18:15; isteğe bağlı XU030 hedge'i kullanılırsa onun penceresi ≈18:05–18:15). Emir 18:00–18:09 arasında, karşı kademeye limit emirle gönderilir; 3+ kontratta 2–3 parçaya bölünebilir. Bu saatlerde spot pay piyasası kapanış müzayedesindedir; vadelide kademeler incelebilir. Son saniyeye bırakılmaz. |
| **Ertesi gün (t+1)** | Pozisyon tutulur. Betiğin "TUT" demesi beklenir. |
| **t+2 sabahı** | Betik o günün z'sine göre UZAT, ÇEVİR ya da KAPAT der. 18:00–18:10'da uygulanır. |

**Zamanlama ölçümü.** Pratik kuralın 85 pozisyonu (2024-04 → 2026-10) spot TUPRS üzerinde iki dolum zamanıyla karşılaştırıldı. Fark küçük: zamanlama sonucu değiştirmiyor, yeter ki 17:30 ile 18:10 arasında işlem yapılsın.

| Dolum zamanı | Brüt (bps) |
|---|---|
| 18:00 öncesi son fiyat (Yahoo saatlik 17:30 barının kapanışı) | +36,8 |
| Kapanış müzayedesi | +37,0 |
| Fark (ortalama) | −0,2 (std 52 bps) |
| ~17:30 fiyatı (16:30 barının kapanışı) | +39,8 |

VİOP'ta uzlaşma yerine son işlem fiyatıyla dolum: net +50,5 bps (uzlaşmayla +49,2).

**17:45–17:55 fiyatıyla sinyal hesaplamanın farkı sıfırdır.** Sinyal BIST fiyatı kullanmaz; betiğin z'si araştırma z'siyle 685 günde (2024+) 6·10⁻¹⁵ farkla aynı.

**Yapılmaması gereken:** BIST seansı sırasında ABD'nin o günkü hareketine bakıp sinyal üretmek. ABD 17:30'da (kış) açılıyor. Araştırmada ABD saatlik 15:00 UTC sürümü işlem kuralında ≈0 verdi. Aynı gün ABD kapanışı ise BIST kapanışından sonra oluştuğu için kullanılamaz.

## 4. Kontrat sayısı (1 kontrat = 100 pay)
Formül: kontrat = taban( sermaye × risk% / (100 × fiyat × L) ).
- L = 2 günlük %95 kötü hareket ≈ 1,65 · σ60 · √2. σ60, TUPRS'un 60 günlük günlük oynaklığı; L için taban %4.
- Geçmişte pozisyonların %5'lik kötü getiri dilimi −5,2% (2024–26'da −5,5%). L ile uyumlu.

**Örnek (04.11.2026 betik çıktısı):**
- Fiyat 346,75 TL (F_TUPRS1126, 03.11 uzlaşması) → 1 kontrat = 34.675 TL; teminat (~%15) ≈ 5.200 TL.
- σ60 = %2,54 → L = %5,9 → kontrat başı risk ≈ 2.057 TL.

| Sermaye 1.000.000 TL | Risk %0,5 (5.000 TL) | Risk %1 (10.000 TL) |
|---|---|---|
| Kontrat | 2 | 4 |
| Nominal | 69.350 TL (%6,9) | 138.700 TL (%13,9) |
| Teminat | ≈10.400 TL | ≈20.800 TL |
| Geçmişin en kötü pozisyonu (fiyatta −%16,9 + maliyet) olsaydı | ≈ −11.800 TL (%1,2) | ≈ −23.600 TL (%2,4) |
| Tam dönem en büyük düşüş (−37,6 nominal puan) | ≈ −%2,6 sermaye | ≈ −%5,2 sermaye |

- En kötü gerçekleşen kayıp (04.08.2026 kısa: log −%15,7 = fiyatta −%16,9), "risk" ölçüsünün yaklaşık 2,9 katıdır. Boyutu buna göre düşünün.
- Teminat (~%15) ≈ 5.200 TL/kontrat; Takasbank oranı %13–17 aralığında değişebilir, aracı kurum ek marj isteyebilir. Limit günlerinde (±%10) teminat çağrısı aynı gün gelebilir; hesapta en az 2–3 kat teminat kadar serbest nakit tutun.
- Oran: **tek bacak** (yalnız TUPRS). Hedge'li sürüm araştırmada ana kural değil: bağımsız hesapta h2 hedge'li net8 +29 bps (t 2,4), hedge'siz +42 (t 2,7). Ayrıca 1 XU030 vadelisi ≈ 144.000 TL olduğundan bu boyutlarda hedge yuvarlanamıyor.

## 5. Örnek işlemler (pratik kural, gerçek VİOP uzlaşmaları)
- **Kazanç, uzatmalı:**
  - 27.02.2026: z +1,17 → F_TUPRS0326 uzun, 211,60.
  - 03.03 (z +2,68) ve 05.03 (z +2,09) → UZAT.
  - 09.03: z +0,09 → KAPAT, 245,65.
  - Net +1.479 bps, kontrat başı +3.378 TL.
- **Kayıp, çevirmeli:**
  - 23.10.2026: z −1,08 → F_TUPRS1026 kısa, 362,45.
  - 27.10 (çıkış günü): z +1,30 → ÇEVİR. Kısa 359,75'ten kapandı (+64 bps); uzun F_TUPRS1126'dan 367,55'te açıldı. F_TUPRS1026'nın vadesine 2 iş günü kaldığı için sonraki vade kullanıldı.
  - 30.10: z +0,27 → KAPAT, 353,00.
  - Kısa bacak net +64 bps (+231 TL/kontrat), uzun bacak net −415 bps (−1.494 TL/kontrat); iki pozisyonun toplamı ≈ −1.263 TL/kontrat.
- **Şu anki işlem:**
  - 03.11.2026: z −1,47 (P −3,88%; 02.11 ABD gününde VLO −4,7%, PBF −3,8%, MPC −3,3%, PSX −2,8%, S&P 500 −0,5%) → F_TUPRS1126 **kısa**, 346,75.
  - 04.11: z +0,38 → TUT; yeni sinyale bakılmaz.
  - **05.11 çıkış günü.** Tetik, 04.11 ABD gününün sepet artığına göre |P| > %2,65:
    - P ≤ −%2,65 → UZAT (kısa kalır).
    - P ≥ +%2,65 → ÇEVİR (4 kontrat alım = 2 kısa kapanır + 2 uzun açılır).
    - Arada kalırsa 18:00–18:10'da KAPAT.
  - Eşik S&P 500 sabitken dört hissenin eşit hareketi cinsinden:

    | Hisse | Uzun tetiği | Kısa tetiği |
    |---|---|---|
    | VLO | ≥ 398,07 | ≤ 377,50 |
    | MPC | ≥ 438,83 | ≤ 416,15 |
    | PSX | ≥ 279,25 | ≤ 264,82 |
    | PBF | ≥ 79,90 | ≤ 75,77 |

    Son 250 günde betalar negatif (04.11 ABD günü için, 03.11'e kadarki pencereyle: VLO −0,46, MPC −0,34, PSX −0,43, PBF −0,70; ort. −0,48). Bu yüzden S&P 500 yükselirse uzun eşiği düşer: S&P +%1 iken eşik, dört hissenin ortalaması +%2,17 (S&P −%1 iken +%3,13); kısa eşiği S&P +%1 iken −%3,13, S&P −%1 iken −%2,17.

## 6. Vade devri, limit, kilit
- **Vade:** TUPRS vadelileri ayın son iş günü sona erer. Girişte vadeye en az 3 BIST işlem günü yoksa (vade t, t+1 ya da t+2 ise) sonraki ayın kontratı kullanılır. Bu kuralla pozisyon vadeye taşınmaz.
- **Roll:** yalnız uzatma gününde kontratın <3 günü kaldıysa yapılır. 411 pozisyonun 3'ünde oldu; ortalaması −43 bps, örneklem küçük. Ön vade dışındaki aylar ince: 03.11'de Aralık 120 mn TL, Ocak 1 mn TL, Kasım 2.127 mn TL. Roll'u ön vadeye geçiş günü yapın.
- **Limit:** 2020-03'ten beri günlük limit ±%10. Veride en büyük günlük hareket ±%10,5 log, yani %10 fiyat.
  - 492 bloğun 4'ünde limit günü vardı; 3'ünde çıkış günü limit gününe denk geldi.
  - Çıkış günü kontrat limitte kilitliyse ve çıkamıyorsanız, bir sonraki seansın 18:00–18:10'unda çıkın. O gün yeni sinyal aramayın.
  - Giriş günü işlem yönünde kilit varsa (uzun açacakken limit yukarı) giriş atlanır.
- **Temettü/bedelsiz:** VİOP uzlaşmaları düzeltiliyor. Backtest, kontratın kendi uzlaşma/önceki uzlaşma oranlarını zincirleyerek hesaplandı.

## 7. Ne zaman yapılmaz
- **ABD tatili sonrası:** betik "ABD günü YOK → sinyal yok" der. Örnek: Şükran Günü 26.11.2026 → 27.11 BIST'te sinyal yok.
- **ABD verisi gecikmesi:** betik "beklenen ABD günü veride yok" uyarısı verirse işlem yapılmaz.
- **Giriş penceresi kaçırıldıysa:** ertesi gün girilmez. Ölçüm: girişi bir gün geç yapmak 2017–26'da net +37 bps (t 2,0), 2024–26'da +12 bps (t 0,4). 15 bps maliyetle sıfıra yakın.
- **BIST'te sistemik şok:** 2026 Eylül–Ekim fon krizinde 8 pozisyon ortalaması −165 bps. Kural bu dönemleri ayırt etmiyor; boyutu küçültmek sizin kararınız.
- **Sepeti değiştirmeyin:** DINO ya da CRAK eklemek, PBF'yi çıkarmak test edilmiş kural değildir. PBF çıkarılınca t 1,7'ye düşüyor, sinyal PBF'ye bağımlı.
- **Kuralı değiştirmeyin:** |z| büyükken boyut artırmak, stop eklemek, çok uzak vade kullanmak test edilmedi. |z| kovaları (yalnız bilgi; pozisyon başı net):

  | |z| | Net (bps) | n |
  |---|---|---|
  | 1–1,5 | +18 | 227 |
  | 1,5–2 | +52 | 113 |
  | 2–3 | +129 | 52 |
  | >3 | +187 | 19 |

  Eğilim tutarlı ama bu bir boyut kuralı değildir.

## 8. Backtest: TAM bu pratik kural (VİOP uzlaşma → uzlaşma, 2017-08 → 2026-11-03)
**Yöntem:**
- Tutulan kontratın kendi uzlaşmaları kullanıldı; pozisyon içinde ön vadeye geçiş yok.
- Gelecek bilgisiyle veri süzme yok.
- Maliyet: açılış+kapanış = 1 tur. Roll = +1 tur. Tik maliyeti tur başına 2 tik: 2025 öncesi 0,01 TL, 2025+ 0,05 TL; uzlaşma ondalıklarından çıkarıldı, bugünkü fiyatta ≈2,9 bps.

| | 8 bps + tik | 15 bps + tik |
|---|---|---|
| Pozisyon sayısı / yılda | 411 / 44,6 | 411 / 44,6 |
| Ort. tutma | 2,39 BIST günü (2 gün: 342, 4: 59, 6: 8, 8: 2) | aynı |
| Brüt / net (bps) | +59,7 / **+49,2** (t 2,53) | +59,7 / **+42,2** (t 2,17) |
| İsabet | %54,3 (ort. kazanç +297, kayıp −245 bps) | %53,3 |
| IS 2017–21 / OOS 2022–26 | +39,6 (t 1,56) / +58,2 (t 1,98) | +32,5 (1,28) / +51,1 (1,74) |
| 2017–19 / 2020–21 / 2022–23 / **2024–26** | −12,5 / +100,9 / +108,1 / **+30,5 (t 0,90, n 137)** | −19,7 / +93,9 / +101,1 / **+23,4 (t 0,69)** |
| Yıllar | 2017 +12, 2018 +10, 2019 −45, 2020 +147, 2021 +27, 2022 +123, 2023 +86, 2024 +42, 2025 +34, 2026 +15 | 2017 +5 … 2026 +8 |
| En iyi 10 çıkınca | +17,1 (t 1,02) | +10,0 (t 0,60) |
| Uzun / kısa | +60,5 (213) / +37,1 (198) | +53,4 / +30,1 |
| TL / pozisyon, 1 kontrat (tarihsel fiyatlarla, doğrusal vadeli K/Z) | ort. +94 TL; 2024–26 +40 TL | +82 / +26 TL |
| Bugünkü fiyatta (34.675 TL nominal) | ≈ +171 TL; 2024–26 oranıyla ≈ +106 TL | ≈ +146 / +81 TL |
| Maks. düşüş | 1× nominal toplam −3.762 bps (12.2018 → 04.2019); 1 kontrat −11.355 TL; 2024–26 −6.911 TL (24.07.2026 → 27.10.2026, **sürüyor**) | −3.892 bps; −11.619 TL; 2024–26 −7.248 TL |
| En kötü pozisyon | 04.08.2026 kısa, 4 gün: log −1.566 bps = fiyatta −%16,9 (doğrusal −1.693 bps), −5.029 TL/kontrat (TL olarak da en kötüsü) | −1.573 log bps; −5.050 TL |
| En uzun kayıp serisi | 8 pozisyon | 11 pozisyon |

_Denetim düzeltmesi (04.11.2026): önceki sürümde TL kâr/zararı kısa pozisyonlarda 100·S₀·(e^(−lr) − 1) ile hesaplanmıştı; vadeli K/Z fiyatta doğrusal olduğundan doğrusu 100·S₀·(1 − e^(lr)). Hata kısa pozisyonların TL sonucunu ortalama +28 TL şişiriyordu (ort. +108 → +94 TL, 2024–26 +54 → +40 TL, en kötü −4.310 → −5.029 TL). bps satırları (log, araştırma kuralı) değişmedi; doğrusal bps ile tam dönem net +49,2 (t 2,52), uzun +68 / kısa +29._

**Araştırmayla karşılaştırma (blok bazında, her 2 günlük blok tam maliyet ödüyor):**
- Yayımlanan rakamlar birebir tekrarlandı: 492 işlem, 53,4/yıl, net8 +42,0 (t 2,72), net15 +35,0, IS +34,5 / OOS +48,8, 2024–26 +26,3 (t 1,02), en iyi 10 çıkınca +20,4 (t 1,45).
- Pratik kural aynı 492 bloğu üretiyor; giriş tarihleri %100 aynı.
- Tutulan kontratla hesaplayınca blok başına fark ort. −0,2 bps; 44 blokta roll farkı var.
- 8 bps + tik ile blok bazında +39,5 (t 2,56), 15 bps + tik ile +32,5 (t 2,10).
- Pozisyon bazında rakam daha yüksek, çünkü uzatmada yeniden işlem maliyeti ödenmiyor.

**Dolum ve gecikme duyarlılığı:**

| Varyant | Net (bps) | t | 2024–26 |
|---|---|---|---|
| VİOP son işlem fiyatıyla dolum, 8 bps + tik | +50,5 | 2,57 | +25,4 |
| Bir gün geç giriş | +37,3 | 2,04 | +12,2 |

## 9. Bu bir lead-lag mı?
- **Kısmen gerçek bir yayılma, kısmen zaman farkı.** ABD kapanışı BIST kapanışından sonra oluşuyor. Bu yüzden ABD t−1 bilgisinin bir kısmı BIST t açılışında fiyatlanıyor; bu kısım bizim kullanamadığımız zaman farkı.
- Strateji BIST t gününün tamamı geçtikten sonra (t uzlaşması) giriyor ve t → t+2 kaymasını alıyor. Yani bilginin TUPRS'a yavaş ve eksik yayılmasını kullanıyor.
- **TUPRS'un kendi momentumu değil:** regresyonda hissenin kendi artığı ve XU030 kontrol edilince z'nin t'si 3,6–4,1. Plaseboda 44 hisse içinde 1. sırada.
- Bir gün eski sinyal de çalışıyor; sönüm yavaş.
- Büyüklük birkaç büyük işlemde yoğunlaşıyor ve PBF'ye bağımlı.

## 10. TradingView'da izlenecek kodlar (yalnız `tv_final.csv`'de doğrulanmış kodlar)

| Kod | Rol | Neden |
|---|---|---|
| NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF | sinyal girdisi | Sepetin dört üyesi; yalnız **önceki** ABD günü kapanışı kullanılır. |
| SP:SPX (alternatif TVC:SPX) | sinyal girdisi | β·S&P 500 çıkarımı (piyasa etkisini ayıklar). |
| BIST:TUPRS1! | işlem aracı | Ön vade sürekli kontrat. Emir, aracı kurumda o ayın kontratına (ör. F_TUPRS1126) verilir. Vade kodu biçimi BIST:TUPRSZ2026 (Aralık 2026). TV'de 15 dk gecikmeli; akşam seansı yok. |
| BIST:TUPRS | bağlam (senkron) | Spot; vadeli ile baz farkını görmek için. |
| BIST:XU030D1! | hedge (isteğe bağlı) / bağlam | Ana kural hedgesiz; piyasa geneli şok takibi. |
| BIST:XU030 | bağlam (senkron) | BIST 30 spot. |
| AMEX:CRAK | bağlam | ABD/küresel rafineri ETF'i; sepetin genel görünümü. Sinyalde kullanılmaz. |
| AMEX:XLE | bağlam | ABD enerji sektörü. |
| ICEEUR:BRN1! (alternatif TVC:UKOIL) | bağlam (senkron) | Brent TUPRS ile eşzamanlı hareket ediyor (kısmi korelasyon 0,16, son 1 yılda 0,45). Öncü değil, işlem sinyali değil. |
| NYMEX:HO1!*42-ICEEUR:BRN1! | bağlam | Dizel crack (formül). Günlük sürücü değil, çeyreklik frekansta görünüyor. |
| CME_MINI:ES1! | bağlam | BIST seansı sırasında ABD vadelisi. Sinyale **girmez**; aynı gün ABD hareketiyle sinyal üretmeyin. |
| BIST:KCHOL | bağlam | Tüpraş'ın ana ortağı, aynı sinyale tepki veriyor. Bu rehberdeki işlem kuralı KCHOL'da test edilmedi. |
| BIST:AYGAZ | bağlam (senkron) | Koç grubu kardeş şirket; eşzamanlı bağ. |

## 11. Dosyalar ve ilk kullanım kontrolü
- `sinyal_tuprs.py`: günlük betik (pandas/numpy/requests).
  - Yahoo'dan son 6 yıl alınır; VİOP bülteni borsaistanbul.com'dan çekilir (`--viop 0` ile kapatılır).
  - Hedef seans 18:10 TSİ'den önce bugündür, sonra ertesi BIST günüdür. `--tarih` ile değiştirilir.
  - BIST tatil listesi betiğin başındadır. 2021–2026 kısmı VİOP takviminden alındı. **2027 satırı tahmindir; Borsa İstanbul takviminden teyit edip güncelleyin.**
- `tuprs.pine`: Pine v5 göstergesi. z sütunları, ±eşik çizgileri, sinyal günü arka planı, AL/SAT/UZAT/ÇEVİR/KAPAT işaretleri ve durum tablosu içerir.
  - **DERLENMEDİ** (bu ortamda Pine derleyicisi yok). BIST:TUPRS1! ya da BIST:TUPRS günlük grafiğine ekleyin.
  - Denetimde beta/std hesabı kayan toplamlara (bar başına sabit iş) çevrildi; algoritma Python'da bar bar benzetildi (`denetim/kod/pine_sim.py`): 2024+ 686 günde bağımsız z ile fark ≤ 4·10⁻¹⁴, sinyal eşleşmesi %100; ABD barı ister önceki gün ister aynı tarih eşlensin sonuç aynı (ileriye bakma yok).
  - Ücretsiz TradingView'da ABD hisse verisi gerçek zamanlı olabilir ama günlük kapanış barı resmi kapanışla ertesi sabah kesinleşir; kararı sabah betikle verin.
  - Son 10–20 günün z değerlerini betik çıktısıyla karşılaştırın; fark 0,05'ten büyükse betiği esas alın.
  - Göstergenin bugünkü z'si, BIST'in bugünkü barı oluştuktan sonra görünür (seans açılışı).
- Backtest kodu: `kod/bt_pratik.py` (pratik kural), `kod/cl_t.py` (araştırma kütüphanesinin veri yolu değiştirilmiş kopyası), `kod/zaman_testi.py` (dolum zamanı), `kod/test_sinyal.py` (betik = araştırma z'si kontrolü).
- Sonuçlar: `sonuc/pratik_ozet.json`, `sonuc/pratik_pozisyonlar.csv`, `sonuc/pratik_bloklar.csv`, `sonuc/sinyal_cikti_20261104.txt`.

## 12. Riskler
- 2024–26 kârlılığı istatistiksel olarak anlamlı değil (t 0,9) ve strateji şu an düşüşte. Beklenti net +20–30 bps/işlem civarı; 15 bps maliyette daha da az.
- Kazanç az sayıda büyük işlemde: en iyi 10 pozisyon çıkınca t ≈ 1.
- Sepet PBF'ye bağımlı.
- 2017–19'da ve 2026 fon krizinde negatif. Rejime bağlı.
- Tek pozisyonda fiyatta −%17'ye varan kayıp oldu (04.08.2026 kısa, −5.029 TL/kontrat). Boyutu küçük tutun.
- Dolum kayması: uzlaşma VWAP olduğu için tek bir fiyattan tam uzlaşmayı yakalamak mümkün değil.
- Yahoo veri hatası, tatil listesi hatası (özellikle 2027) ve göstergenin derlenmemiş olması operasyonel risk.

## 13. Bağımsız denetim (rehber_tuprs_denetim, 04.11.2026)
Kod ve çıktılar: `denetim/kod/` (z_bagimsiz.py, karsilastir_z.py, bt_bagimsiz.py, pine_sim.py, ydl_d.py), `denetim/sonuc/`. Bağımsız kod günlük betiği, `cl.py` ya da `cl_t.py`'yi import etmez; Yahoo verisi 04.11.2026'da ayrı dizine yeniden indirildi.

**(1) Sinyal ve tarih hizalaması — doğru.**
- Son 300 BIST günü, bağımsız z ↔ günlük betik (canlı Yahoo): 290 dolu günün hepsi ortak, en büyük fark 6,7·10⁻⁶ (veri yuvarlaması), sinyal eşleşmesi %100. 10 boş gün iki tarafta da boş (ABD tatili ertesi).
- Bağımsız z ↔ araştırma z (30.10.2026'ya kadar): 287 ortak gün, sinyal eşleşmesi %100. Betik takvimi 2021+ VİOP takvimiyle birebir.
- 'after' kuralı örnekleri: 08.09.2026 (Labor Day ertesi), 27.11.2026 (Şükran Günü ertesi) → ABD günü yok, sinyal yok; 30.10.2026 → 28.10 + 29.10 ABD günleri toplanıyor (29.10 BIST tatili). Yahoo'nun bitmemiş günü betikte 16:20 New York süzgeciyle atılıyor; beklenen ABD günü eksikse uyarı veriliyor.
- Araştırma kodunda küçük artefakt: `cl.to_bist` takvim başlangıcından (06.03.2017) önceki 1.130 ABD gününü ilk BIST gününe topluyor. Bu yüzden 2017–18'de z en fazla 0,04 farklı, 3 sinyal günü değişiyor. Günlük betikte bu hata yok. Bağımsız z ile pratik backtest: 414 pozisyon, net8 +49,5 bps (t 2,56); kurucunun 411 / +49,2 (t 2,53) sonucuyla pratikte aynı.
- Betikte düzeltme: bir sonraki seans eşiğindeki ortalama beta artık son tamamlanmış ABD gününü de içeren pencereden hesaplanıyor (−0,46 → −0,48). Sinyalin kendisi değişmedi.

**(2) Pratik kuralın backtest'i — bps sonuçları doğrulandı, TL sonuçları düzeltildi.**
- Araştırma z'si ile bağımsız simülasyon: 411/411 pozisyonda giriş, çıkış ve yön aynı; brüt fark ≤ 0,005 bps.
- TL hatası düzeltildi (§8 notu). `kod/bt_pratik.py` düzeltilip yeniden çalıştırıldı; `sonuc/` dosyaları güncellendi.
- Duyarlılık (bağımsız z, VİOP uzlaşma, pozisyon bazında, 8 bps + tik; 15 bps sütunu ayrıca):

| Eşik | Tutma | n | Net8 (t) | Net15 (t) | IS 2017–21 (t) | OOS 2022–26 (t) | 2024–26 (t) | En iyi 10 hariç (t) |
|---|---|---|---|---|---|---|---|---|
| 0,75 | 1 | 707 | +24,0 (2,38) | +17,0 (1,68) | +8,1 (0,59) | +38,5 (2,62) | +28,0 (1,66) | +9,8 (1,07) |
| 0,75 | 2 | 515 | +48,6 (2,86) | +41,4 (2,44) | +33,7 (1,61) | +62,3 (2,37) | +34,8 (1,12) | +25,5 (1,63) |
| 0,75 | 3 | 388 | +63,3 (2,56) | +56,0 (2,26) | +53,6 (1,54) | +71,6 (2,05) | +34,1 (0,87) | +24,4 (1,12) |
| 1,00 | 1 | 532 | +15,3 (1,37) | +8,2 (0,74) | +12,1 (0,80) | +18,1 (1,12) | +14,3 (0,80) | −1,1 (−0,11) |
| **1,00** | **2** | **414** | **+49,5 (2,56)** | **+42,5 (2,20)** | **+40,4 (1,62)** | **+58,2 (1,98)** | **+30,5 (0,90)** | **+17,7 (1,06)** |
| 1,00 | 3 | 335 | +46,8 (1,75) | +39,6 (1,48) | +21,8 (0,60) | +68,4 (1,76) | +30,3 (0,74) | +3,4 (0,15) |
| 1,25 | 1 | 365 | +16,5 (1,25) | +9,5 (0,72) | +4,1 (0,22) | +27,3 (1,49) | +23,4 (1,10) | −5,7 (−0,50) |
| 1,25 | 2 | 309 | +50,5 (2,49) | +43,4 (2,14) | +30,2 (1,11) | +68,0 (2,31) | +22,1 (0,66) | +14,8 (0,86) |
| 1,25 | 3 | 269 | +78,4 (2,69) | +71,3 (2,45) | +16,3 (0,42) | +134,0 (3,16) | +45,3 (0,94) | +25,0 (1,03) |

- Okuma: tutma 2 günde eşik ±0,25 sonucu bozmuyor (t 2,5–2,9). Tutma 1 gün zayıf (t 1,3–2,4). Eşik 1'de tutma 3 gün t 1,75'e düşüyor ve en iyi 10 çıkınca sıfırlanıyor. **Hiçbir varyant 2024–26'da anlamlı değil** (en yüksek t 1,66). En iyi 10 işlem çıkınca hiçbir varyantta t 1,7'yi geçmiyor.

**(3) Pine.** İleriye bakma yok: aynı tarihli ABD barı time_close > kesim ile her durumda eleniyor. Tatil tekrarı yok (lastTc). Boşlar doğru işleniyor. Beta 250/100 (o gün hariç), std 250/100 (o bar hariç) araştırmayla aynı. Sözdiziminde bariz hata bulunmadı (request.security tuple + lookahead, ticker.new, array.*, plot/hline/plotshape, var). Tek değişiklik performans için yapıldı: bar başına 250'lik döngüler yerine kayan toplamlar. **Derleyici yok; derlenmedi.**

**(4) Talimat gerçekçiliği.**
- Seans saatleri (pay vadelisi 18:10, endeks vadelisi 18:15), uzlaşma penceresi, 15 dk TradingView gecikmesi doğru ele alınmış. Sinyal BIST fiyatı kullanmadığı için "17:45–17:55 fiyatıyla hesaplama" farkı tanım gereği 0; dolum zamanı farkı ölçüldü: 18:00 öncesi son fiyat ile kapanış arasında ort. −0,2 bps (std 52).
- Kontrat ve teminat hesabı doğru (34.675 TL nominal, ~%15 ≈ 5.200 TL; %0,5 riskte 2, %1 riskte 4 kontrat).
- ÇEVİR'de kontrat değişebileceği notu eklendi.
- Limit kilidi talimatı makul. Backtest kilitli girişleri ayıklamıyor; 492 bloğun yalnız 4'ünde limit günü var.
- Rehberdeki TradingView kodlarının tümü `tv_final.csv`'de var: TVC:UKOIL alternatif listesinde, BIST:TUPRSZ2026 ise TUPRS1! satırının notunda vade kodu örneği olarak geçiyor.

**(5) Güncel durum (bağımsız hesap).** 03.11 z −1,469 → kısa (F_TUPRS1126, 346,75); 04.11 z +0,377 → tut; 05.11 çıkış günü, tetik |P| > %2,653 (241 dolu gözlem). §5'teki fiyat tetikleri birebir doğrulandı.
