# ABD Planı A: Lider hisse momentumu (USIC tarzı), gün sonu kararlı swing

**Başlangıç:** Pazartesi 9.11.2026. ABD seansı 17:30–24:00 TSİ (ABD 1.11'den beri kış saatinde; TSİ = ET + 8).
**Hazırlanma:** Cuma 6.11.2026, ~14:00 TSİ. Son kapanış verisi Perşembe 5.11. Ekim NFP bugün 16:30 TSİ'de açıklanacak; Cuma kapanışı bu dosyada **yok**. Pazartesi kararı §3.3'teki tabloyla Cuma kapanışından hesaplanır.
**Durum:** Taslak, bağımsız plan. Yatırım tavsiyesi değildir; vergi kısımları mali müşavirle teyit edilmelidir.

**Atıf biçimi.** Her kuralın yanında dayanağı yazılı: `dosya.md §bölüm`. Doğrulama dosyaları raporlarla çeliştiğinde doğrulama esas alındı.
- `v_abd`, `v_capraz`, `v_dalga`, `v_profesyonel` → `dogrulama/`
- `abd_hafta_hazirlik` (kısaca `hazırlık`) → `uygulama/`
- Diğerleri → `ajanlar/`

**Etiketler.**
- **[A]** Hakemli veya resmî kaynak.
- **[P]** Uygulayıcı kuralı (USIC kazananları, IBD, Minervini, Kullamägi, Luk, Kell). Öz beyandır; akademik testi yoktur.
- **[H]** Benim hesabım. Betik: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/abdA/mc.py` (oturum scratchpad'i, kalıcı değil).
- **[Ö]** Tasarım seçimi veya öznel tahmin. İleri ölçümle kalibre edilecek.

---

## 0. Tek paragrafta plan

Doğrulanmış yüksek getiri ABD'de gerçek ama nadir:
- USIC'te aracı kurum ekstresiyle doğrulanan sonuçlar var: Luk 2024 +%283, 2025 +%970; Minervini 2021 +%334,8; Kell 2020 +%941.
- Aynı yarışmada katılımcıların yalnız **%8–17'si** yılı kârla kapatıyor (`v_abd` #13–14).
- Bu yöntemin gün sonu (EOD) uyarlaması **hiç test edilmedi** (`v_abd` §4.2; `abd_test` §8; `v_profesyonel` eksik #8).
- Rejim bugün düşmanca: Nasdaq düzeltmede, VIX vade yapısı ters.

Bu yüzden plan şöyle kurulu:

1. **Küçük ve ayrı bir ABD hesabı** açılır: likit sermayenin **%10–20'si**. Bu tutarın yalnız rejimin izin verdiği kısmı USD'ye çevrilir.
2. **İşlem başı risk %0,25** ile başlanır.
3. Üç kurulum kullanılır: **kırılım, katalizör gap'i, 10/20 GHO'ya geri çekilme**. Girişler seans öncesi bırakılan **buy-stop-limit**, korumalar **GTC stop** emirleriyle yapılır. Çıkış kararları **kapanışa göre** verilir.
4. Altı göstergeli bir **rejim anahtarı** yeni işlemlere izin verip vermediğine karar verir.
5. İlk 100 işlem **ölçüm**tür. Sermaye ancak kanıt gelirse büyür.

İlk 12 ayda dürüst beklenti: ABD hesabında **medyan −%3 ile +%19** (senaryoya göre). Bu, TL'de kalmanın engelini (**vergi öncesi %20–28 USD**) büyük olasılıkla geçmez. Yüksek ödül ancak 2. yıldan sonra, kenar kanıtlanmış ve rejim elverişliyse gelebilir (§8).

---

## 1. Sermaye ve engel kararı

### 1.1 Engel rakamları (doğrulanmış)

| Kalem | Değer | Dayanak |
|---|---|---|
| TL'de kalmanın net nominal getirisi | Faiz sabit kalırsa ~%36–38; anket patikasında ~%31–33 | `v_capraz` #4 |
| TL'de kalmanın USD karşılığı, ileriye dönük | Net ~%13–15,5. Faiz indirimi gelir ya da kur hızlanırsa %6–12 | `v_abd` #34 |
| TL carry'nin geçmişi | 2010–26'da USD bazında −%7,2/yıl, MaxDD −%85 | `abd_test` §2; `v_abd` #34 |
| TL'den gelen sermaye için gereken **vergi öncesi USD getirisi** | ~%28 (h=%35, d=%20, t=%35). Vergi ertelemesi ve %60 yatırımda kalmayla ~%20 | `abd_pratik` §2.6; `v_capraz` #22 (cebir DOĞRU) |
| Örnek | +%30 USD kazanan strateji, vergi sonrası TL bazında +%38,7. TL nakdi ancak başa baş geçer | `abd_pratik` §2.6 |
| USD'de bekleyen sermaye için alternatif | 3 aylık T-bill %4,03 (iskonto) / %4,10 (kupon eşdeğeri) | `v_capraz` #13 |
| Türkiye vergisi | ABD kazancı TL bazında, kur farkı dahil, %15–40 artan oranla beyan edilir. Zarar yalnız aynı yıl içinde mahsup edilir. Yİ-ÜFE endekslemesi yalnız ≥%10 artışta (~6 ay elde tutma) | `v_capraz` #10 |

**USD'de duran sermaye için engel, benim yaklaşığım [H].**
- Strateji pozisyonlarındaki kur artışı vergilenir. Elde tutulan dövizin kur kazancı vergilenmez (`abd_pratik` §2.5, §4.2).
- Yaklaşık formül: gereken R ≈ i + u·t·d / ((1+d)(1−t)).
  - i = T-bill getirisi, u = yatırımda kalma oranı, t = vergi oranı, d = kur artışı.
- i=%4, t=%35, d=%20 ile: tam yatırımda (u=1) **~%13**, u=0,5 ile **~%8,5**.
- T-bill faizinin kendisi de beyana tabidir (`abd_pratik` §4.1). Bu yüzden rakam yaklaşık bir değerdir.

### 1.2 Karar kuralları

**C1. A kolu büyüklüğü.**
- Kural: A kolu ≤ toplam likit yatırım sermayesinin **%20'si** ve ≤ şu tutar: "A kolu × %20 öldürme eşiği ≤ toplam sermayenin %4'ü". İki koşul pratikte aynı sınırı verir.
- Sermaye TL'den geliyorsa ve ayrıca USD ihtiyacın yoksa: **%10**.
- Zaten USD tutuyorsan ya da USD çeşitlendirmesi istiyorsan: **%20**.
- **Dayanak:**
  - Taban oranlar kötü: USIC'te %8–17 kârlı, medyan katılımcı rastgeleden kötü (`v_abd` #14; `seytan_taban_oranlar` §0 #8).
  - +0,2–0,3R'lik bir kenarı şanstan ayırmak 280–450 işlem, yani 2–4 yıl ister (`seytan_taban_oranlar` §3.7).

**C2. USD'ye çevirme.** Rejime göre kademeli çevrilir.
- Çevrilecek tutar = A kolu × (rejimin brüt maruziyet tavanı + %10 tampon).
  - R1'de bu %50, R2'de %80, R3'te %100'dür (§5). R0'da da R1'e hazır olmak için %50 çevrilir; daha azı da olur.
- Çevrilmeyen kısım TL'de banka mevduatında, banka PPF'sinde ya da TLREF/DİBS'te kalır.
- **Gerekçe:** Boşta bekleyen her USD ayı, beklenen değerde ~%0,8–0,9 carry kaybıdır (%13–15,5 / 12 eksi T-bill). Ama carry'nin sol kuyruğu kalındır (−%85 MaxDD).
- **Uyarı:** PPF risksiz değildir (`v_profesyonel` eksik #2).

**C3. A kolunun nakdi.** Pozisyon dışındaki USD, IBKR nakit faizi (%3,38) ya da 3 aylık T-bill (~%4) ile tutulur (`abd_pratik` §4.1).
- Veraset vergisi: ABD hisseleri ve ABD menşeli fonlar 60 bin $ üstünde "US-situs" sayılır (`v_abd` #36).
- 250 bin $ ve 1 mn $ hesapta bu ciddi bir risktir. Hangi nakit aracının bu kapsamda olduğunu uzmana sor. Bellekten bilgi: doğrudan T-bill muaftır; bu bilgi doğrulanmadı.

**C4. Sermaye eklememe kuralı.** A koluna şu koşulların hepsi sağlanmadan para eklenmez:
- **100 işlem**
- **12 ay**
- E[R] ≥ +0,3R ve %80 güven aralığının alt sınırı > 0
- Kural ihlali < %5

Bu koşullar sağlanınca A kolu ×1,5 büyütülebilir (toplam sermayenin en fazla %30'u). %50'ye çıkmak için 250+ işlem ve 2 yıl gerekir (§7.2).
- **Dayanak:** `seytan_taban_oranlar` §5.3 #4: "12 ay ve 100 işlemden önce boyut artırılmaz."

**C5. Vergi yılı.** 9.11–31.12.2026 ayrı bir vergi yılıdır. 2026 net zararı 2027'ye devredilmez (`v_capraz` #10).
- Bu 7 haftada küçük boyutta kalmak hem risk hem vergi açısından doğru.
- Ölçüm yılı fiilen 1.1.2027'de başlar; Kasım–Aralık ölçüme dahildir.

### 1.3 Çalışılmış örnekler (A kolu büyüklüğü olarak)

| | **50 bin $** | **250 bin $** | **1 mn $** |
|---|---|---|---|
| İma ettiği toplam likit sermaye (%10–20) | 250–500 bin $ | 1,25–2,5 mn $ | 5–10 mn $ |
| R0/R1'de USD'ye çevrilecek (%50) | 25 bin $ | 125 bin $ | 500 bin $ |
| İşlem başı risk %0,25 | 125 $ | 625 $ | 2.500 $ |
| İşlem başı risk %0,5 (≥50 işlem ve E[R] ≥ +0,2R) | 250 $ | 1.250 $ | 5.000 $ |
| R1 toplam ısı tavanı %1,5 | 750 $ | 3.750 $ | 15.000 $ |
| R1 tek pozisyon tavanı %12,5 | 6.250 $ | 31.250 $ | 125.000 $ |
| Aylık devre kesici (ilk 100 işlem: %4) | 2.000 $ | 10.000 $ | 40.000 $ |
| Öldürme eşiği (zirveden −%20) | 10.000 $ | 50.000 $ | 200.000 $ |
| Toplam sermayeye etkisi (öldürmede) | −%2 ile −%4 | −%2 ile −%4 | −%2 ile −%4 |
| Veri ve yazılım maliyeti, yıllık ~1.000–1.300 $ (`abd_pratik` §5) | **%2–2,6** (çok yüksek; asgari set kullan, aşağıda) | %0,4–0,5 | %0,1 |
| 60 bin $ veraset eşiği (`v_abd` #36) | Pozisyonlar dolunca aşılabilir | Aşılır | Aşılır |

**50 bin $ hesap için.** Yalnız TradingView Essential veya Plus (12,95–29,95 $/ay) ve ücretsiz finviz yeter. Sürtünme yılda ~%0,3–0,7 olur.

### 1.4 Neden bu kadar küçük?

- Senaryo ağırlıklarıyla ilk yılın beklenen sonucu kabaca T-bill düzeyindedir, ~%0–5 (§8). TL'den gelen sermaye için beklenen fırsat maliyeti, A kolunun yılda ~%10–13'ü eder; toplam sermayenin %1–2,6'sı. Kötü senaryoda öldürme kaybı toplam sermayenin %2–4'ü.
- Karşılığında alınan şey bir **opsiyon**: kenar gerçekse 2. yıldan itibaren riski ve sermayeyi büyütme hakkı.
- Ek fayda, TL şokuna karşı çeşitlendirme (`abd_pratik` §4.2). Ama bu sigortanın "adil fiyatlı" olduğu doğrulanmadı. 2018–26'da USD T-bill carry'yi yendi; sonuç rejime bağlı (`v_capraz` #21).

---

## 2. Strateji kolları ve işlem kuralları

### 2.0 Ortak tanımlar

| Terim | Tanım |
|---|---|
| GHO | Günlük basit hareketli ortalama (SMA) |
| ATR14 | 14 günlük ortalama gerçek aralık |
| ADR%20 | 100 × (20 günlük ortalama (yüksek/düşük) − 1) |
| RS çizgisi | Hisse kapanışı / S&P 500 kapanışı. "RS/52H" = RS çizgisinin 252 günlük zirvesine oranı (`hazırlık` §5a Pine betiği) |
| TT (trend şablonu) | Kapanış > 50 > 150 > 200 GHO; 200 GHO bugün > 21 gün önce; kapanış ≥ 1,3 × 52 hafta dibi ve ≥ 0,75 × 52 hafta zirvesi (`hazırlık` §5a; Minervini [P]) |
| R | Başlangıç riski = (dolum − ilk stop) × adet. Gerçekleşen R = net kâr/zarar (komisyon dahil) / başlangıç riski |
| Isı | Açık pozisyonların stoplarına kadar toplam riski. **Gap-ayarlı ısı** = adet × max(stop mesafesi, 1,5 × ATR14) (`abd_profesyonel` §3.5 #5) |
| Küme | Aynı anlatıya bağlı ya da 60 günlük getiri korelasyonu ≥ 0,6 olan isimler (`abd_profesyonel` §3.5 #2) |

**Evren filtresi (her kurulum için).**
- Fiyat ≥ 20 $, piyasa değeri ≥ 2 mlr $ (`hazırlık` §4–5).
- 50 günlük ortalama dolar hacmi ≥ 20 mn $; 1 mn $ hesapta ≥ 50 mn $ [Ö]. Pozisyon ≤ günlük ortalama dolar hacminin %1'i [Ö].
- ADR%20 ≥ %2 [Ö].
  - Pozitif çarpıklık büyük hareket edebilen hisse ister. Kullamägi'nin evreni çok daha oynak [P].
  - Su şirketi gibi düşük ADR'li savunmacılarda hedeflenen R küçük kalır.
- Satın alma/birleşme arbitrajı profili (aylık oynaklık < %2) dışarıda (`hazırlık` §4).
- Dışlanan kümeler §4.5'te.

**Kanıtın genel çerçevesi.**
- Bileşenlerin akademik çekirdeği var:
  - Tekil hissede trend takibi: işlemlerin <%7'si kârın çoğunu üretiyor. CAGR %15,19 brüt (`v_abd` #18).
  - Bessembinder: hisselerin %4'ü tüm net servet yaratımını açıklıyor (`v_abd` #29).
  - Earnings tepkisi (EAR), likit evrende LS %0,24/ay (`abd_swing_kenarlar` §4).
- Ama zayıflıklar da var:
  - 52 hafta zirvesi tek başına 2010 sonrası anlamsız (likit evrende t=0,37; `abd_swing_kenarlar` §3.1).
  - Sadece-uzun earnings üst portföyleri 2010–25'te VW piyasayı geçmiyor (`abd_test` §6.4).
  - IBD'nin mekanik sürümü FFTY: 2022'de −%51, 10 yılda +%4,6/yıl (`v_abd` #17).
- Kenar, varsa, **çıkış asimetrisi + rejim + boyut** disiplinindedir (`abd_kim_kazaniyor` §5.1, §7.2).

### 2.1 S1: Baz kırılımı (VCP / düz baz), gün sonu uyarlaması

| Adım | Kural | Dayanak |
|---|---|---|
| Ön koşul | TT = 1. RS/52H ≥ 0,97. Kapanış 52 hafta zirvesinin ≤ %10 altında (pivot ≤ %5 tercih edilir). Son 1 aylık getiri < +%25; daha fazlaysa "uzamış" sayılır, yalnız S3 ile girilir | `hazırlık` §5a; dalga_abd §4.4 (sektör düzeyinde 3 ayda +%40 sonrası 1–3 ay medyan −%4/−%6; hisse düzeyinde test yok) [Ö] |
| Baz | En az 15 seans. Derinlik (baz tepesi → dibi): R1/R2'de ≤ %15, R3'te ≤ %25. Son daralma ≤ %10 ve ≤ 2,5 × ATR14. Son 5 seansın toplam aralığı ≤ 2 × ATR14. 10 günlük ortalama hacim < 50 günlük ortalama hacim | Minervini VCP, IBD baz [P] (`abd_profesyonel` §1.1) |
| Pivot | Son daralmanın en yüksek seviyesi (genelde son 5–15 seansın tepesi) | [P] |
| Giriş emri | Kapanıştan sonra (00:00–17:25 TSİ) **BUY STOP-LIMIT**: tetik = pivot + %0,1, limit = tetik + %1,5. DAY emri; her gün yeniden değerlendirilir, en fazla 5 seans. Gap tetiğin %1,5'inden fazla üstünde açarsa dolmaz; bu kovalamayı engeller | IBD alım bölgesi pivot +%5 [P]. Daha sıkı tutuldu, çünkü ekran yok [Ö] |
| İlk stop | Emirle birlikte **GTC SELL STOP (piyasa)**, yalnız normal seansta tetiklenir. Seviye = son daralmanın dibi − %0,1. Koşullar: tetikten uzaklık **0,6–1,5 × ATR14** ve **≤ %8**. Koşul sağlanmıyorsa işlem yapılmaz | Kullamägi ≤1 ATR/ADR; IBD %7–8; Minervini ≤%10 (`abd_profesyonel` §1.3 #3). Mekanik 1 ATR stop ve 3 günlük çıkış kötü sonuç verdi; stop yapısal olmalı (`v_profesyonel` A12) |
| Başarısız kırılım | Dolumdan sonraki ilk 3 seansta kapanış < pivot − 0,5 × ATR14 ise ertesi açılışta **MOO** ile tamamen çık | Minervini'de ortalama kayıp tavanın yarısı [P] (`abd_profesyonel` §1.3 #3) [Ö] |

**Dürüst beklenti (S1, EOD uyarlaması, maliyet sonrası) [Ö]:**
- İsabet %25–40. Ortalama kazanç 2–4R. E[R] **−0,1 ile +0,4R**.
- Belirsizlik **yüksek.** Uyarlama test edilmedi. Benzer mekanik kopya: 2008–25 CAGR %19, MDD −%21, brüt, survivorship'e açık [İKİ] (`v_profesyonel` A12 KISMEN).

### 2.2 S2: Katalizör gap'i (episodic pivot), 2.–5. gün girişi

| Adım | Kural | Dayanak |
|---|---|---|
| Olay günü (1. gün) | Gün sonu verisiyle kontrol edilir: **earnings** ya da büyük haber (kılavuz yükseltme, onay, sözleşme) ile önceki kapanışa göre açılış gap'i ≥ **+%8**. Hacim ≥ **3 ×** 50 günlük ortalama. Gün dolar hacmi ≥ 50 mn $. Kapanış gün aralığının üst yarısında ve ≥ açılış × 0,98 | `hazırlık` §5b; `abd_swing_kenarlar` §4.1 test protokolü (gap ≥%7, hacim ≥3×) |
| Kalite | Gelir beklentiyi aşmış ve kılavuz yükselmiş (basın bülteni). Gap öncesi 3 aylık getiri ≤ +%30 ("ihmal edilmiş hisse") | Savor (2012): analist bilgisiyle desteklenen şok drift ediyor, bilgisiz şok tersine dönüyor [A] (`abd_kim_kazaniyor` §5.1). Kullamägi'nin "neglected" vurgusu [P] |
| Giriş emri | 2.–5. seans **BUY STOP-LIMIT**: tetik = olaydan bu yana en yüksek + %0,1, limit = tetik + %1,5. Kapanış 1. gün dibinin altına inerse kurulum iptal | `abd_swing_kenarlar` §4.1 ("gün-2'de gün-1 high'ı kırılınca") |
| İlk stop | GTC SELL STOP = 1. gün dibi − %0,1. Uzaklık ≤ **%10** ve ≤ 2 × ATR14 (ATR olay gününü içerir). Daha genişse işlem yapılmaz | `abd_swing_kenarlar` §4.1; Minervini ≤%10 [P] |
| Bilanço | Bir sonraki bilanço ~3 ay uzakta. Sorun yok | — |

**Dürüst beklenti (S2) [Ö]:**
- İsabet %30–45. Kazanç 2–5R. E[R] **−0,1 ile +0,3R**.
- Akademik çekirdek yaşıyor ama küçük (EAR LS %0,24/ay, t≈2,1).
- Sadece-uzun büyük hisse versiyonu VW'yi geçmiyor (−%1,4/yıl; `abd_test` §6.4). PEAD büyük hisselerde 2006'dan beri yok (`v_abd` #23).
- Kenar küçük/orta ölçekte ve ihmal edilmiş hissede. Konsantre EP'nin hakemli kanıtı yok (`abd_swing_kenarlar` §4.1). Hisse düzeyinde test yapılamadı (`abd_test` §8).

### 2.3 S3: Yükselen 10/20 GHO'ya geri çekilme (Luk ve Kell ailesi)

| Adım | Kural | Dayanak |
|---|---|---|
| Lider | TT = 1. RS/52H ≥ 0,95. Son 20–40 seansta ≥ +%20 itki ya da son 6 haftada bir S1/S2 olayı. 10 GHO > 20 GHO > 50 GHO. 20 GHO bugün > 5 seans önce | Luk: yükselen ortalamaya ilk geri çekilme; Kell: EMA crossback [P] (`abd_profesyonel` §1.1) |
| Geri çekilme | Son tepeden 2–8 seans. Derinlik %5–15 ve ≤ 2,5 × ATR14. Geri çekilme günlerinde hacim 50 günlük ortalamanın altında | [P] |
| Sinyal günü | Gün dibi ≤ 10 GHO + 0,25 × ATR (10 veya 20 GHO bölgesine değmiş). Kapanış ≥ 20 GHO ve ≥ gün ortası | Raschke "Holy Grail": sinyal barı tepesi üstünden giriş [P] (`abd_profesyonel` §1.1) |
| Giriş emri | Ertesi seans **BUY STOP-LIMIT**: tetik = sinyal günü tepesi + %0,1, limit = tetik + %1. 2 seans geçerli | [P] |
| İlk stop | GTC SELL STOP = min(sinyal günü dibi, 20 GHO − 0,25 × ATR) − %0,1. Uzaklık ≤ 1,5 × ATR14 ve ≤ %7 | Luk: stop <%2,5, çoğunlukla %1–1,5 (gün içi). EOD uyarlamasında daha geniş [P] |

**Dürüst beklenti (S3) [Ö]:**
- İsabet %30–45. Kazanç 2–3R. E[R] **−0,1 ile +0,3R**.
- Luk'un 104/319 işlem istatistiği **DOĞRULANAMADI** (`v_abd` #15). Gün içi stop yerine EOD stop kullanıldığı için kazanç R'ı düşer.

### 2.4 Ortak çıkış kuralları (bütün kollar)

| Kural | Uygulama (EOD) | Dayanak |
|---|---|---|
| **Kısmi kâr** | İlk gerçekleşen koşulda: (a) kapanış ≥ giriş + 2R, ya da (b) 4. seans kapanışı ≥ giriş + 1R. Ertesi açılışta **MOO** ile R1/R2'de pozisyonun **1/2**'si, R3'te **1/3**'ü satılır | Kullamägi: 3–5 günde 1/3–1/2 [P] (`v_profesyonel` A1 DOĞRU, öz beyan) |
| **Başabaş** | Kısmi satıştan sonra ya da kapanış ≥ +1,5R olunca GTC stop giriş fiyatına çekilir | [P] (`abd_profesyonel` §1.3 #7) |
| **İz süren çıkış** | Kalan pozisyon için ilk **kapanış < 10 GHO** (hızlı hisse: ADR%20 ≥ %4 ya da girişten sonraki 10 seansta ≥ +3R) ya da **kapanış < 20 GHO** (diğerleri). Ertesi açılışta MOO | Kullamägi 10/20 GHO [P]. Momentum getirisinin çoğu gece oluşuyor; ertesi açılışta satmak bunu korur (Lou-Polk-Skouras [A], `abd_swing_kenarlar` §3.1) |
| **Acil stop** | Her Cuma kapanışından sonra GTC stop son 10 seansın en düşük dibinin %0,5 altına yükseltilir. Asla düşürülmez | [Ö] |
| **Zaman stopu** | 10 seans sonunda kâr < +1R ve girişten beri yeni kapanış zirvesi yoksa ertesi açılışta çık | [Ö] Isıyı boşaltır (`abd_profesyonel` §3.5 #9) |
| **Bilanço** | S1/S3'te bilançoya ≤ 10 seans kalmışsa yeni giriş yok. Açık pozisyonda: kısmi satış yapılmış ve yastık ≥ +3R ise kalan pozisyon, 2 × implied move'luk bir gap'te ≤ 1R kaybedecek boyuta indirilerek taşınabilir. Aksi halde bilanço günü (AMC ise) MOC ile, BMO ise önceki gün MOC ile çıkılır | Kell "earnings size"; `abd_profesyonel` §3.5 #5 [P] |
| **Aşırı koşu** | Pozisyon girişten +%100'e ulaştıysa ya da hissenin 24 aylık koşusu ≥ +%100 ise iz süren çıkış 10 GHO'ya ve %10'luk tepeden düşüş stopuna sıkılaştırılır | GSY replikasyonu: %10–15'lik iz süren stop en kötü sonucu −%69'dan −%22'ye çekiyor [H/A] (`dalga_abd` §5; `v_dalga` U8 DOĞRU) |
| **Yeniden giriş** | Stop olan hisseye yeni pivot oluşursa yeniden girilebilir. Aynı bazda en fazla 2 deneme | [Ö] |

### 2.5 Boyut formülü ve örnekler

- **Adet** = (A kolu özsermayesi × risk%) / (tetik fiyatı − stop).
- **Tavanlar:**
  - Pozisyon tutarı ≤ rejim tavanı: R1 %12,5, R2 %15, R3 %20. Mutlak tavan %25.
  - Gap-ayarlı ısı, rejimin küme ve toplam ısı tavanlarının içinde kalmalı (§5).
  - Dar stop büyük pozisyon demektir. Tek hisse tavanı bu yüzden şart: Kullamägi gece ≤%30, Minervini %20–25 (`abd_profesyonel` §1.3 #4).

**Risk% merdiveni (ilerleyici maruziyet).**
- Kullanılacak risk = min(rejim bandı, kanıt seviyesi) × düşüş çarpanı.
- **Kanıt seviyesi** (`abd_profesyonel` §3.5 #1; Minervini %25→%50→%75→%100 [P]):

| Seviye | Koşul | Azami risk |
|---|---|---|
| L0 | 0–49 işlem | %0,25 |
| L1 | ≥ 50 işlem ve E[R] ≥ +0,2R | %0,5 |
| L2 | ≥ 100 işlem, ≥ 6 ay, E[R] ≥ +0,3R | %0,75 |
| L3 | ≥ 200 işlem, ≥ 12 ay, E[R] ≥ +0,3R ve %80 GA alt sınırı > 0 | %1,0. **Hiçbir koşulda %1 aşılmaz** |

- %1'in üstünde bu DNA matematiksel olarak kırılır: %25 isabette 200 işlemde ≥ 15 ardışık kayıp olasılığı ~%49 (`v_abd` #37; `abd_kim_kazaniyor` §5.3).
- **Rejim bandı:** R1 %0,25. R2 %0,25–0,5. R3 %0,5–1,0.
  - Bant içinde üst uç yalnız özsermaye son 20 seansta yeni zirve yaptıysa kullanılır; aksi halde alt uç. Bu, "kazanırken büyüt, kaybederken küçült" kuralıdır [P].
- **Düşüş çarpanı:** §5'teki merdiven.
- **L1 eşiği ile C4 farkı:** L1'deki %0,5 risk, `seytan_taban_oranlar`'ın "12 ay/100 işlemden önce büyütme yok" kuralıyla çelişir. Çözüm: hesap içindeki işlem riski 50 işlemde artabilir, ama **A kolunun sermayesi** C4 sağlanmadan artmaz. Küçük bir hesapta %0,5, toplam sermayenin ≤ %0,1'i eder.

**Örnek 1 (S1).**
- Pivot 100,00 $ → tetik 100,10, limit 101,60.
- Stop 94,50 (%5,6). ATR14 5,0 $, yani 1,12 ATR. Hisse başı risk 5,60 $.

| %0,25 risk | 50 bin $ | 250 bin $ | 1 mn $ |
|---|---|---|---|
| Adet | 22 | 111 | 446 |
| Tutar (hesabın %'si) | 2.202 $ (%4,4) | 11.111 $ (%4,4) | 44.645 $ (%4,5) |
| Gap-ayarlı ısı (1,5 ATR = 7,5 $) | 165 $ = %0,33 | 833 $ = %0,33 | 3.345 $ = %0,33 |
| +2R kısmi satış seviyesi | 111,30 $ | 111,30 $ | 111,30 $ |

**Örnek 2 (S3, dar stop).**
- Tetik 50,05, stop 48,40 (%3,3). ATR 1,2 $, yani 1,38 ATR. Hisse başı risk 1,65 $.
- Adet: 75 / 378 / 1.515.
- Tutar: 3.754 / 18.919 / 75.826 $, hesabın %7,5–7,6'sı.
- Gap-ayarlı ısı: max(1,65 ; 1,8) × adet ≈ %0,27.

### 2.6 Piramit (yalnız kazanana)

| Kural | Değer | Dayanak |
|---|---|---|
| Ön koşullar | Rejim ≥ R2. Pozisyonun kapanış kârı ≥ +1,5R. Yeni bir geçerli S3 sinyali (10/20 GHO'ya geri çekilme) ya da yeni S1 bazı. Bilançoya > 10 seans var | IBD %50/30/20; Turtle ½N [P] (`abd_profesyonel` §1.3 #6) |
| Ek boyutu | 1. ek: başlangıç riskinin **0,5**'i. 2. ek: **0,33**'ü. En fazla 2 ek | [P] |
| Stop | Ekin kendi S1/S3 stopu. Orijinal lotun stopu en az başabaşa çekilir. Ek sonrası toplam pozisyonun gap-ayarlı ısısı ≤ 1R (başlangıç riski) olmalı | [Ö] |
| Yasak | Maliyet düşürme (zarardaki pozisyona ekleme). R1'de ekleme | Bütün doğrulanmış kazananlarda ortak (`abd_profesyonel` §0 #1) |
| Kayıt | Her ek ayrı işlem satırı olarak kaydedilir (kendi R'ı, ana işlem kimliğiyle) | §7 |

Brandt hiç piramit yapmıyor; bu da meşru bir seçim (`abd_profesyonel` §1.3 #6). İlk 50 işlemde piramit **isteğe bağlı**. Ölçüm temiz kalsın diye ayrı etiketlenir.

### 2.7 Emir tipleri ve günlük iş akışı (TSİ, ekran başında işlem yok)

| Zaman (TSİ) | İş | Emir tipi |
|---|---|---|
| 00:00 (isteğe bağlı) ya da ertesi sabah 08:00–12:00 | Gün sonu rutini: rejim skoru (§3), taramalar (§4), açık pozisyonların çıkış kontrolü (kapanış GHO altında mı, kısmi koşulu, zaman stopu, başarısız kırılım), yeni adaylar için pivot ve stop çizimi. AMC bilançolar 00:05'ten sonra gelir; sabah bilinir | — |
| 12:00–17:25 | Emir girişi. Yeni giriş: BUY STOP-LIMIT (DAY), ekli GTC SELL STOP. Çıkış kararları: MOO (açılışta piyasa). Stop yükseltmeleri | STP LMT, STP (GTC), MOO |
| Makro veri günü 16:30 | Veri sonrası 16:35–17:25 arasında emirler gözden geçirilir (§3.4) | İptal/teyit |
| 17:30–24:00 | **Ekrana bakılmaz.** Emirler kendi kendine çalışır | — |
| Cuma kapanışından sonra (Cumartesi) | Haftalık rapor: rejim, ısı, günlük metrikleri, acil stop yükseltmeleri | GTC değişikliği |

**Emir ayarları.**
- Stoplar **"yalnız normal seans" (RTH)** tetiklenir. IBKR'de "outside RTH" kapalı bırakılır.
- Koruyucu stop **STOP (piyasa)** olur, stop-limit değil. Gap'te stop-limit dolmayabilir.
- Girişler **STOP-LIMIT** olur. Limit, kovalamayı keser.
- Pazar emri yalnız MOO/MOC çıkışlarında kullanılır. Opsiyonda asla (`abd_profesyonel` §2.4).
- MOO/MOC son giriş saatleri borsaya göre değişir. Bellekten: NYSE/Nasdaq'ta açılış 09:28 ET, kapanış 15:50 ET. IBKR'de teyit et. **17:25 TSİ'den sonra MOO verme.**
- **Kısmi satış emri.** Kısmi satış için +2R'de dinlenen bir limit satış emri kullanılacaksa, IBKR'de stop ile aynı OCA grubunda **"diğer emirleri orantılı küçült"** seçilmeli. Yoksa limit dolduktan sonra stop tüm adedi satar ve marj hesabında açığa satış doğar. Varsayılan yöntem: kısmi satış kararı gün sonunda verilir ve MOO ile uygulanır.
- **Kapanış teyitli giriş (S1-B).** IBKR koşullu emirle "15:45 ET'de fiyat ≥ pivot ise MOC al" kurulabilir. Momentum gece getirisini yakalar (Lou-Polk-Skouras, `abd_swing_kenarlar` §3.1). İlk 50 işlemde **yalnız gölge günlükte** test edilir (§7.4).

### 2.8 Bu planda kullanılmayanlar (ve neden)

- **Opsiyon alımı** (şimdilik). Sistematik alım ortalamada kaybettiriyor:
  - Straddle ~−%3/hafta.
  - Yüksek çarpıklıklı 7 günlük call −%35/hafta (`v_profesyonel` A6 DOĞRU).
  - VIX 28 iken IV pahalı.
  - Ancak R3'te, IV kendi geçmişinin alt %30–40'ında, IV ≤ RV20 ve pencerede bilanço yokken 45–90 günlük, 0,55–0,70 deltalı call bir hissenin yerine geçebilir. Prim ≤ 1,5–2R (`abd_profesyonel` §2.3).
  - İlk 100 işlemde yok; ölçüm temiz kalsın.
- **Açığa satış ve parabolik short.** Locate, ödünç ücreti, squeeze riski. Daniel-Moskowitz: ayı rallileri short'ları ezer (`v_abd` #27; `abd_kim_kazaniyor` §5.4).
- **Marj.** İlk 12 ayda yok. Marj faizi %5,38 (`v_capraz` #16) ve Türkiye'de kredi faizi indirilemez (`abd_pratik` §2.1).
- **Kaldıraçlı ETF ve AI dip alımı.** 3x NDX + 200 GHO bile 2000–02'de −%89 (`abd_test` §0 #2). AI kümesi kırık (§4.5).
- **Koşulsuz kısa vadeli reversal.** 2010 sonrası öldü (`abd_test` §7).

---

## 3. Rejim anahtarı

### 3.1 Göstergeler, eşikler ve bugünkü değerler (5.11 kapanışı)

| # | Gösterge | Eşik | 5.11 değeri | Puan | Dayanak |
|---|---|---|---|---|---|
| a | S&P 500 kapanış > 200 GHO | > | 7.353,73 > **7.322,7** (+%0,4). 200 GHO günde ~+4 puan yükseliyor; Pazartesi ~7.330 | **1** | `hazırlık` §3; `v_abd` #32 |
| b | S&P 500 10 GHO > 20 GHO | > | 7.622 < 7.680 | 0 | [H] FRED SP500 + 7.353,73 |
| c | NDX 10 GHO > 20 GHO ve ikisi de 5 seans öncesinden yüksek | > | 28.672 < 29.286; ikisi de düşüyor (19.10'dan beri 10<20) | 0 | `v_profesyonel` A11 DOĞRU; Kullamägi filtresi [P] |
| d | NDX kapanış > 50 GHO | > | 26.629,8 < **29.685,7** (200 GHO 27.976,5; −%4,8) | 0 | `hazırlık` §3 |
| e | VIX/VIX3M < 1,00 ve VIX < 25 | < | 28,18 / 25,55 = **1,10** | 0 | `hazırlık` §3. 4.11'de VIX 16,61 idi; tek günlük sıçrama (`v_profesyonel` A11) |
| f | Genişlik: S5FI ≥ 50 ve Nasdaq 52 hafta zirve − dip (MAHQ − MALQ) > 0 | ≥ / > | S5FI 62,5 (önbellek, karışık zaman damgası); 150 − 490 = **−340** | 0 | `hazırlık` §3, §5d |
| | **Skor** | | | **1/6** | |

Ek göstergeler:
- **FTD (takip günü).** Ralli denemesinin 4. veya sonraki günü S&P ≥ +%1,25 ya da NDX ≥ +%1,5 kapanış. Hacim SPY/QQQ'da önceki günden yüksek.
  - Ralli denemesinin 1. günü, düzeltmenin en düşük kapanışından sonraki ilk artı kapanıştır. Endeks o dibin altında kapanırsa sayım sıfırlanır.
  - Dayanak: IBD [P] (`abd_profesyonel` §1.1, §1.4); `hazırlık` §3.
- **RSP > 50 GHO.** 5.11'de +%0,7 üstünde (`hazırlık` §3).

### 3.2 Rejim seviyeleri ve izinler

| Seviye | Koşul (her kapanışta yeniden) | Yeni işlem izni | Risk/işlem | Azami pozisyon | Küme ısısı | Toplam ısı | Brüt tavan |
|---|---|---|---|---|---|---|---|
| **R0 KAPALI** | R1 koşulları sağlanmıyor. Tipik nedenler: (a) yok, VIX/VIX3M ≥ 1,00, RSP < 50 GHO ile birlikte S5FI < 50, ya da aylık devre kesici aktif | **Yok.** Yalnız gölge günlük (§7.4) | — | Mevcutlar | — | Mevcut ≤ %1 | %0–20 |
| **R1 PİLOT** | (a) var **ve** VIX/VIX3M < 1,00 **ve** (RSP > 50 GHO **ya da** S5FI ≥ 50); büyüme tarafı kırık olabilir | S1, S2, S3. Yalnız AI dışı kümeler. Kümede tek pozisyon | %0,25 | 3 | %0,5 | **%1,5** | %40 |
| **R2 TEYİT** | R1 **ve** VIX < 25 **ve** [FTD **ya da** (c)] | Hepsi. Piramit izinli | %0,25–0,5 | 5 | %1,0 | **%3** | %70 |
| **R3 TREND** | R2 **ve** (b), (c), (d) **ve** NDX 10 > 20 > 50 GHO **ve** VIX < 20 **ve** (f) **ve** S5FI ≥ 60 | Hepsi | %0,5–1,0 | 8 | %1,5 (yıl içi yastık ≥ %10 ise %2) | **%5** (yastıkla %6) | %100, marj yok |

**Geçiş kuralları.**
- Seviye düşüşü kapanışta hesaplanır ve ertesi günden geçerlidir.
- Yeni seviyede ısı ve pozisyon sayısı fazlaysa yeni giriş yapılmaz. Fazla ısı zorla kapatılmaz; R0 hariç.
  - **R0'a düşüşte** bütün iz süren çıkışlar 10 GHO'ya sıkılaştırılır. Toplam ısı 5 seans içinde ≤ %1'e indirilir: önce en zayıf RS'li pozisyonlar satılır.
- S&P 2 ardışık kapanış < 200 GHO olursa: R0, iz süren çıkışlar 10 GHO'ya, toplam ısı ≤ %1.
- FTD'ye dayalı R2 iki durumda düşer: endeks ralli denemesinin dibinin altında kapanırsa ya da 15 seans içinde (c) gerçekleşmezse.

**Dayanaklar.**
- Kullamägi 10/20 filtresi, IBD FTD, Weinstein Stage [P] (`abd_profesyonel` §1.3 #10, §3.5 #6).
- Kullamägi'nin iddiası: filtreye uysaydı 2022 kayıplarının ~%90'ı önlenirdi. Bu, kendi hindsight tahmini (`v_abd` #16).
- Daniel-Moskowitz: dinamik ölçekleme momentum Sharpe'ını ~2 katına çıkarıyor [A] (`v_abd` #27).
- "Endeks 50 GHO altında ve VIX > 25 iken brüt pozisyonu yarıya indir" (`abd_pratik` §3.6).
- Isı tavanları %3/%5/%6 (`abd_profesyonel` §3.5 #4; Elder %6 [P]).

**Rejim filtresinin beklenen etkisi.**
- Getiri motoru değil, sol kuyruk kesici.
- Monte Carlo'da drawdown kuralları yalnız performans rejime bağlıysa değer katıyor (Kaminski-Lo [A]; `abd_profesyonel` §3.3–3.4). Momentum swing'de bağlılık güçlü: FFTY 2022 −%51, Kullamägi −%57.
- **Bedel:** Dipten çıkışın ilk %5–10'u kaçırılır.

**TradingView rejim göstergesi** (Pine v6; kağıt üzerinde doğrula, semboller `hazırlık` §5d'de teyitli):

```pine
//@version=6
indicator("A_Rejim", overlay=false)
ftd = input.bool(false, "FTD geldi mi? (elle)")
[spx, spx10, spx20, spx50, spx200, spx1, spx200_1] = request.security("SP:SPX", "D", [close, ta.sma(close,10), ta.sma(close,20), ta.sma(close,50), ta.sma(close,200), close[1], ta.sma(close,200)[1]])
[ndx, ndx10, ndx20, ndx50, ndx10p, ndx20p] = request.security("NASDAQ:NDX", "D", [close, ta.sma(close,10), ta.sma(close,20), ta.sma(close,50), ta.sma(close,10)[5], ta.sma(close,20)[5]])
[rsp, rsp50] = request.security("AMEX:RSP", "D", [close, ta.sma(close,50)])
vix  = request.security("CBOE:VIX", "D", close)
vix3 = request.security("CBOE:VIX3M", "D", close)
s5fi = request.security("INDEX:S5FI", "D", close)
hq   = request.security("INDEX:MAHQ", "D", close)
lq   = request.security("INDEX:MALQ", "D", close)
a = spx > spx200
b = spx10 > spx20
c = ndx10 > ndx20 and ndx10 > ndx10p and ndx20 > ndx20p
d = ndx > ndx50
e = vix / vix3 < 1.0 and vix < 25
f = s5fi >= 50 and hq - lq > 0
score = (a?1:0) + (b?1:0) + (c?1:0) + (d?1:0) + (e?1:0) + (f?1:0)
r1 = a and vix / vix3 < 1.0 and (rsp > rsp50 or s5fi >= 50)
r2 = r1 and vix < 25 and (ftd or c)
r3 = r2 and b and c and d and ndx10 > ndx20 and ndx20 > ndx50 and vix < 20 and f and s5fi >= 60
lvl = r3 ? 3 : r2 ? 2 : r1 ? 1 : 0
twoBelow = spx < spx200 and spx1 < spx200_1
plot(score, "Skor 0-6", color=color.gray, style=plot.style_stepline)
plot(lvl, "Rejim R0-R3", color=color.blue, linewidth=3, style=plot.style_stepline)
plot(vix / vix3, "VIX/VIX3M", color=color.red)
plotshape(twoBelow, "S&P 2 kapanis 200 GHO alti", shape.xcross, location.top, color.red)
hline(1.0)
```

### 3.3 Bugün ne diyor, Pazartesi neye göre karar verilir

- **5.11 kapanışıyla: R0.** VIX/VIX3M 1,10 ≥ 1,00. Skor 1/6. Yeni canlı işlem yok.
- **Pazartesi 9.11'de R2 ve R3 imkânsız.**
  - FTD için en az 4 günlük ralli denemesi gerekir. Cuma 1. gün olsa bile en erken FTD Çarşamba 11.11'dir.
  - NDX 10 < 20 GHO farkı ~600 puan; birkaç seansta kapanmaz.

**Cuma 6.11 kapanışından sonra (Cumartesi sabahı) bakılacak tablo:**

| Cuma kapanışı | Pazartesi rejimi | Pazartesi ne yapılır |
|---|---|---|
| VIX/VIX3M ≥ 1,00 ya da S&P ≤ 200 GHO (~7.327) | **R0** | Canlı giriş yok. Hesap kurulumu, izleme listesi, gölge emirler (§7.4) |
| VIX/VIX3M < 1,00, S&P > 200 GHO, RSP > 50 GHO (ya da S5FI ≥ 50) | **R1** | Hesap hazırsa en fazla **2** canlı giriş emri: %0,25 risk, farklı AI dışı kümeler, yalnız tam geçerli S1/S2/S3. Toplam ısı ≤ %1,5 |
| S&P > 200 GHO ama RSP < 50 GHO ve S5FI < 50 | **R0** | Savunmacı liderlik de çözülüyor demektir (`hazırlık` §5d okuma kuralı). Nakit |

### 3.4 Pazartesi, Salı (CPI) ve haftanın geri kalanı

| Gün | Olay (TSİ) | Kural |
|---|---|---|
| **Pt 9.11** | 16:40 Bowman/Barkin. 21:00 3 yıllık tahvil ihalesi. BMO: CEG, MNDY, NRG (AI güç; dışlanmış). AMC: RKLB, TTWO, ZETA, ASTS, HIMS, MARA, PLUG. BRK-B bilançosu 9.11 olabilir, teyit et (`hazırlık` §2.1, §4) | R0: gölge emirler. R1: en fazla 2 giriş emri 12:00–17:25 arasında. BRK-B'ye bilanço öncesi giriş yok |
| **Sa 10.11** | **16:30 Ekim CPI.** Cleveland nowcast: manşet %0,24 aylık; çekirdek %0,21. 21:00 10 yıllık ihale. AMC: CRWV (AI turnusolu, yalnız bilgi). BMO: ONON, SE, QBTS | **16:30'dan önce yeni giriş emri bırakılmaz.** 16:35–17:25 arasında S&P vadelisi önceki kapanışa göre **−%1'den fazla düşükse** o günün yeni giriş emirleri iptal edilir; değilse emirler girilir. Açık pozisyona dokunulmaz, GTC stoplar çalışır [Ö] |
| **Ça 11.11** | Gaziler Günü: hisse piyasası açık, tahvil piyasası kapalı. Hacim düşük olabilir. MSCI Kasım duyurusu gece (BIST için) | O gün dolan S1'de başarısız kırılım kuralı sıkı uygulanır. Hacim 50 günlük ortalamanın altındaysa kırılım "teyitsiz" etiketlenir. En erken FTD günü |
| **Pe 12.11** | 16:30 işsizlik başvuruları. 21:00 30 yıllık ihale. AMC: **CSCO, AMAT** (çip ekipmanı) ve CBRS (Cerebras); BMO: NBIS | AI kümesinde işlem yok. AMAT'ın sert tepkisi Cuma geneli etkileyebilir; GTC stoplar yeterli |
| **Cu 13.11** | 16:30 PPI. 18:00 UMich | CPI günü kuralı aynen uygulanır. Kapanıştan sonra **haftalık rapor**: rejim, ısı, gölge ve canlı işlemler |
| Sonraki hafta | **NVDA 17.11 AMC** (çağrı 01:00 TSİ, 18.11). Görevdeki "~19.11" notu `hazırlık` §2.1'deki NVIDIA IR kaynağıyla çelişiyor; IR'den teyit et. HD 17.11; TGT/TJX/LOW 18.11; **FOMC tutanakları 18.11 22:00**; WMT 19.11; **aylık opsiyon vadesi 20.11**; BJ 20.11 BMO | Endeksi hareketlendiren olay (NVDA, FOMC) öncesindeki son seansta yeni giriş emri yok. Temel tüketim/perakende kümesindeysen WMT/TGT öncesi o kümeye yeni giriş yok [Ö] |
| Ay sonu | **26.11 Şükran Günü kapalı. 27.11 erken kapanış 21:00 TSİ** (yeni giriş yok). 30.11 ay sonu küme sıralaması (§4.2). 4.12 NFP. **9.12 FOMC 22:00 TSİ** (artırım olasılığı ~%67–70). 11.12 bütçe finansman süresi doluyor | FOMC günü yeni giriş yok. 11.12'ye doğru kapanma riski haberleri izlenir |

---

## 4. Evren, kümeler, izleme listesi

### 4.1 Taramalar (ayarlar `hazırlık` §5'ten)

| Tarama | Ne zaman | Ayar |
|---|---|---|
| **(a) Trend şablonu + RS** | Her gün sonu | `hazırlık` §5a Pine betiği `TT_RS_EP_Screen`. Filtreler: `TT = 1`, `RS line / 52w max ≥ 0,97`, `Dist to 52wH ≥ −10`, `50d $Vol ≥ 20`; sıralama `RS raw`. Finviz sıkı sürüm (52H'ye %0–5, 6.11'de 86 sonuç) ve geniş sürüm (412 sonuç): URL'ler `hazırlık` §5a'da. Ek kolonlar: ADR%, bilanço tarihi |
| **(b) EP / gap** | Her sabah 09:00–12:00 (önceki günün olayları) | `hazırlık` §5b: `Gap % ≥ 8`, `RVOL ≥ 3`, `50d $Vol ≥ 20`, kapanış üst yarıda. Finviz `earningsdate_yesterdayafter` / `todaybefore` URL'leri. Gün içi 17:45–18:30 taraması bu planda **yok**; gün sonu verisiyle ertesi sabah bakılır |
| **(c) Küme/ETF sıralaması** | Ay sonu (ilki 30.11) ve her Cuma göz atma | `hazırlık` §5c skoru: 0,2·(1A − SPY) + 0,4·(3A − SPY) + 0,4·(6A − SPY), fiyat > 50 GHO |
| **(d) Yeni liderlik avı** | Her Cuma | finviz endüstri grupları 3A sıralaması (`hazırlık` §3). İlk 10'a yeni giren ve 1A'sı pozitif grup aday kümedir. İçinde TT = 1 ve RS çizgisi yeni zirvede olan hisseler aranır. "Düzeltmede RS çizgisi fiyattan önce zirve yapan" isimler (O'Neil/Minervini gözlemi [P]; akademik teyidi yok, `abd_kim_kazaniyor` §6) |

**Önemli dürüstlük notu.** Küme sıralaması bir **filtre**dir, kenar değil.
- Sektör momentumu 2010 sonrası risk-ayarlı olarak piyasanın altında kalıyor (`v_abd` §2.2, §3.1).
- 2015 sonrası fark istatistiksel olarak belirsiz (`v_dalga` U1, U4).
- Swing ufkunda sektör düzeyinde kenar yok: 40 varyantın 40'ı negatif (`v_dalga` U7).
- Kümenin işi **kötü temadan uzak tutmak**. Getiri, küme içindeki hisse kurulumlarından gelmek zorunda.

### 4.2 Küme tanımları (Kasım 2026 başlangıç haritası)

**Kural.**
- Aynı anlatı ya da 60 günlük getiri korelasyonu ≥ 0,6 ise aynı küme (`abd_profesyonel` §3.5 #2).
- Korelasyonu TradingView "Correlation Coefficient" (60) ile ölç ve her ay sonu güncelle.
- Ölçülene kadar K1–K3 (sağlık) **tek küme** sayılır.
- Gerekçe: ρ = 0,6–0,8 ile 5 pozisyon 1,19–1,47 bağımsız bahis eder (`seytan_taban_oranlar` §3.6). Kümelenme %1 riskte %5 olasılıklı kötü MDD'yi −%23,9'dan −%32,3'e çıkarıyor (`abd_profesyonel` §3.3; kalibre edilmemiş MC, `v_profesyonel` #11).

| Küme | İsimler (`hazırlık` §4 listesinden) | ETF ölçüt | Durum |
|---|---|---|---|
| K1 Medtech / araçlar | MDT, EW, BDX, GEHC, TMO, IDXX | IHI (#2) | Lider (XLV skor #1) |
| K2 İlaç / biyotek | LLY, REGN, RPRX | PPH, IBB | Lider |
| K3 Sağlık hizmetleri | CNC, EHC | IHF | Lider |
| K4 Borsalar / finansal veri | CBOE, CME, TW | XLF | Lider. CBOE oynaklıktan fayda sağlıyor; VIX düşerse geride kalabilir |
| K5 Sigorta / broker | AJG, MRSH, ACGL, BRK-B | — | Lider. K4 ile ρ'yu ölç |
| K6 Temel tüketim / indirim | KDP, BJ | XLP | Lider (savunmacı) |
| K7 Atık / su | RSG, VLTO, AWK | — | Lider, ama ADR düşük olabilir; filtreyi kontrol et |
| K8 Konaklama / tüketici | MAR, HLT, SN, HAS, EBAY | XRT | Lider |
| K9 Dikey yazılım / bilanço sonrası | ROP, MANH, U, GEN | IGV (zayıf) | Karışık. Tekil EP'ler |
| K10 REIT | CCI, PSA | XLRE | Faize duyarlı; CPI riski |
| K11 Mega-cap teknoloji | AAPL | QQQ | NDX rejimine bağlı; ≥ R2 bekle |

**Faktör uyarısı.** R1'de açılacak her pozisyon büyük olasılıkla savunmacı ve düşük betalı olacak. Bu da kendi başına bir kümedir.
- Büyümeye sert geri dönüşte savunmacılar geride kalabilir ya da düşebilir. Daniel-Moskowitz'te 2009'da kazananlar +%8, kaybedenler +%163 yaptı (`v_abd` #27).
- Sınır: toplam ısı tavanı. R1'de %1,5.

### 4.3 Küme başına 3–5 isim nasıl seçilir

1. (a) taramasının sonuçları kümelere dağıtılır.
2. Küme içinde `RS raw`'a göre sıralanır. Evren filtresini (likidite, ADR ≥ %2, bilanço > 15 seans ya da yeni açıklanmış) geçen **ilk 5** izleme listesine girer.
3. Her isme kurulum etiketi verilir: S1 (baz hazır, pivot ≤ %3 uzakta), S2 (olay penceresi açık), S3 (geri çekilme sürüyor) ya da "uzamış, bekle".
4. Her isme pivot, stop, stop %, stop/ATR ve bilanço tarihi yazılır. Stop koşulunu (S1 0,6–1,5 ATR ve ≤ %8) sağlamayan isim kurulum listesine girmez.
5. Öncelik: RS sırası → sıkılık (son 5 seans aralığı / ATR) → pivota yakınlık.
6. Tetiklenince işlem sayısı: R1'de kümenin yalnız **1.**'si, R2'de ilk 2'si, R3'te ilk 3'ü. Diğerleri yedektir.

### 4.4 Güncel adaylar (5.11 verisiyle; grafik görülmeden yapılmış ön sınıflama)

Fiyatlar 5.11 kapanışıdır (finviz). "52H ≈" = fiyat / (1 + uzaklık), yani `hazırlık` §4'ten türetildi [H]. Gerçek pivotu grafikte çiz.

| Durum | İsim (52H ≈, $) | Not |
|---|---|---|
| **S1 adayı: pivotu çiz, rejim R1 olunca emir** | BDX (214,9), EHC (143,4), TW (129,0), AWK (153,7)*, PSA (346,0)*, RSG (254,5)*, RPRX (69,8), ACGL (113,6), VLTO (119,1)*, MANH (263,6), HLT (381,2), MAR (433,3), SN (225,6), EBAY (127,8), KDP (37,8)*, TMO (712,1), CME (322,7) | 52H'ye %1–5 uzaklık; son bilanço ≥ 1 hafta önce. *Düşük oynaklık olabilir: ADR%20 < %2 ise dışarı. BDX 5.11'de bilanço açıklayıp çöküş gününde zirve yakınında kaldı (`hazırlık` §4); 5.11 gap'i ≥ %8 ise S2 olarak da değerlendirilir |
| **S2 penceresi: 1. gün kriterlerini teyit et** | U (5.11 BMO; "haftada +%35"), EW (4.11 AMC → 5.11 tepki), SN (4.11 BMO) | U için 5.11 1. gün, 9.11 3. gün, 11.11 5. gün (son). Gap ≥ %8, hacim ≥ 3×, kapanış üst yarıda değilse S1/S3'e düşer |
| **Uzamış: yalnız S3 (geri çekilme) bekle** | AJG (1A +%26,9), CBOE (1A +%25,4), GEHC (1A +%29,5; 52H'ye −%6,7), HAS (1A +%31,7), ROP (1A +%36,9), GEN (1A +%36,7), CCI (1A +%31,8), MRSH (1A +%20,6; sınırda), CNC (YTD +%78,5; 4.11'de tek günde +%12,6) | Kovalanmaz (`dalga_abd` §4.4 sektör bulgusunun hisseye uyarlanması [Ö]) |
| **S3 adayı (EP sonrası ilk geri çekilme)** | IDXX (2.11 EP +%21,9; 2.–5. gün penceresi 6.11'de kapandı) | 1. gün dibi üstünde sıkışma ve 10/20 GHO dokunuşu bekle |
| **Bilanço bekle** | MDT (Kasım ortası/sonu, teyit), BRK-B (9.11 olabilir, teyit), BJ (20.11 BMO) | Bilançodan sonra S2 adayı olabilir |
| **Bekle: baz yok / olay riski** | REGN (52H'ye −%9,8), LLY (−%7,1; ObesityWeek 14–17.11, 6.11 fiyat anlaşması; `dalga_abd` §6.2) | Yeni baz kurulursa S1 |
| **≥ R2 bekle** | AAPL | NDX'e bağlı mega-cap |
| **Dışarıda** | AI çip/bellek/donanım/güç/veri merkezi (NVDA, AMD, MU, SNDK, MRVL, VRT, GEV, VST, CEG...), neocloud/madenciler (CRWV, NBIS, IREN), nükleer/SMR, kuantum, kripto, drone/uzay, enerji (50 GHO kırıldı), altın madencileri, APP (200 GHO altında), NET (52H'ye −%24,7) | `hazırlık` §4 "bilinçli dışarıda"; `dalga_abd` §6.2, §7 #4 |

### 4.5 Kırık temalara dönüş kuralı (AI kompleksi)

- **Tek küme.** Yarı iletken + bellek/donanım + elektrik ekipmanı/güç + veri merkezi altyapısı + neocloud ve AI'a dönen madenciler.
  - 2026'da Chips–ElcEq korelasyonu 0,72, piyasadan arındırılmış 0,43 (`abd_profesyonel` §3.2). Bu, ajanın kendi hesabı; tekrarlanmadı (`v_profesyonel` A14). Yön makul.
- **Pilot dönüş koşulu (R2 ve sonrası).**
  - SMH 10 seans boyunca 50 GHO'nun üstünde kapanmalı.
  - SMH/SPY oranı 3 aylık zirve yapmalı.
  - Hisse yeni bir Stage 2 bazından (≥ 5 hafta) S1 vermeli.
  - Küme ısısı yarı tavanda tutulur.
- **Tam küme ısısı.** SMH/SPY'nin **12 aylık RS zirvesi** yeniden görülmeli (`dalga_abd` §6.2, §7 #4).
- **Hardw canlı GSY olayı.** Tarihsel çöküş olasılığı %42–53 (`dalga_abd` §5). Bu kümeye dönüşte stop %10'luk tepeden düşüşe sıkılaştırılır.

---

## 5. Risk limitleri (özet tablo)

| Limit | Değer | Dayanak |
|---|---|---|
| İşlem başı risk | %0,25 (L0) → %0,5 (L1) → %0,75 (L2) → **%1 mutlak tavan** (L3), rejim bandıyla sınırlı | `abd_profesyonel` §3.5 #1; `v_abd` #37 |
| Tek pozisyon tutarı | R1 %12,5 / R2 %15 / R3 %20; mutlak %25. Günlük ortalama dolar hacminin ≤ %1'i | Kullamägi ≤%30, Minervini %20–25 [P] |
| Gap-ayarlı risk | adet × max(stop, 1,5 × ATR14); bilanço penceresinde 2 × implied move | `abd_profesyonel` §3.5 #5 |
| Küme ısısı | R1 %0,5 / R2 %1,0 / R3 %1,5 (yastıkla %2). Ölçülmüş ρ ≥ 0,6 olan kümeler birleşir | `abd_profesyonel` §3.1, §3.5 #3 |
| Toplam açık ısı | R0 ≤ %1 (yalnız mevcutlar) / R1 %1,5 / R2 %3 / R3 %5 (yastıkla %6) | `abd_profesyonel` §3.5 #4; Elder [P] |
| Brüt maruziyet | R0 %0–20 / R1 %40 / R2 %70 / R3 %100. İlk 12 ay marj yok | `abd_pratik` §3.6; [Ö] |
| Pozisyon sayısı | R1 3 / R2 5 / R3 8 | Kullamägi/Minervini 4–8 [P] |
| **Aylık devre kesici** | Ayın gerçekleşen zararı + açık ısı ≥ **%4** (ilk 100 işlem) / **%6** (sonrası) → ay sonuna kadar yeni işlem yok | Elder %6 [P] (`abd_profesyonel` §3.5 #8) |
| **Düşüş merdiveni** (A kolu özsermaye zirvesinden) | −%5 → risk × 0,5. −%10 → × 0,25, yalnız R3'te S1/S2. −%15 → 2 hafta işlem yok, günlük incelemesi. −%20 → **öldürme** (§7.3 K1). Kaybın yarısı geri gelince bir basamak yukarı | `abd_profesyonel` §3.3 Model B: %1 riskte merdiven %5 kötü MDD'yi −%40,6'dan −%18,9'a indiriyor, medyandan ~17 puan alıyor [H, kalibre edilmemiş] |
| Kayıp serisi | 8 ardışık kayıpta risk × 0,5, bir sonraki ≥ +2R kazanca kadar. **Seri tek başına öldürme nedeni değildir** | %25 isabette 200 işlemde ≥ 10'lu seri olasılığı %96, ≥ 15'li %49 (`v_abd` #37) |
| Bilanço | S1/S3'te ≤ 10 seans kala giriş yok; taşıma yalnız §2.4 koşuluyla | Kell [P] |
| Olay günleri | CPI/PPI kuralı (§3.4). FOMC ve NVDA öncesi son seansta giriş yok. 27.11 erken kapanışta giriş yok | [Ö] |

---

## 6. Erişim ve uygulama

### 6.1 Aracı kurum seçimi

| Kurum | Kullanım | Maliyet (gidiş-dönüş) ve R karşılığı | Dayanak |
|---|---|---|---|
| **IBKR Pro (ana hesap)** | Bütün emir tipleri: STP LMT, GTC STP, OCA, MOO/MOC, koşullu emir. Nakit faizi. İleride marj ve opsiyon | 0,005 $/adet, min 1 $/emir. Örnek 1'de 50 bin $ hesapta 2 $ ≈ **0,016R**, 1 mn $ hesapta ~4,5 $ ≈ 0,002R | `v_capraz` #16 DOĞRU; `hazırlık` §1.2 |
| **Midas (köprü)** | Onay 1–2 gün; Pazartesi'ye en olası hesap. **Koşul:** uygulamada buy-stop-limit ve GTC stop emri olmalı. Yoksa bu plan için **kullanılmaz** (ekran gerektirir) | 1,5 $/işlem. 50 bin $ hesapta 3 $ ≈ 0,024R. Kur makası yayınlanmıyor; küçük tutarla ölç | `v_capraz` #16; `hazırlık` §1.2, §7 |
| İş Yatırım TMI %0,25 / Garanti %0,30 (+%0,50 kur) | Yalnız hesap zaten açıksa ve IBKR beklenirken | Maliyet / R = %0,5–0,6 / stop%. %3 stopta **0,17–0,2R**, %6 stopta 0,08–0,1R. +0,3R'lik kenarın %25–60'ını yer. Bu plan için uygun değil | `abd_pratik` §0 #5 |

**IBKR adımları.**
- Hesap açılışı 1–3 iş günü, SWIFT 1–2 iş günü. Gerçekçi ilk işlem **11–13.11** (`hazırlık` §1.3).
- Başvuruda VİOP tecrübesini türev deneyimi olarak beyan et.
- Hangi IBKR kuruluşuna (IB LLC / IBIE) bağlanacağını **yazılı** sor; ETF erişimi buna bağlı. Bu plan ETF almaz, ama küme ölçütlerinde ETF kullanılır.
- W-8BEN formunu doldur. Temettüde %20 stopaj uygulanır (`v_capraz` #12).

**İlk gün operasyon testi.** Hesap fonlanınca 1 adet likit hisse için şunları dene ve kaydet:
- STP LMT alış, GTC STP satış, MOO satış.
- Kur çevirme maliyeti: BSMV binde 2 (`abd_pratik` §2.5; `v_capraz` doğrulayamadı) ve banka makası.

Bu bir strateji işlemi değil; günlükte "ops" olarak işaretlenir.

**PDT.** 25 bin $ şartı kaldırıldı. Yürürlük 4.6.2026; aracı kurumların geçişi 20.10.2027'ye kadar sürebilir. Bu plan gün içi işlem yapmadığı için bağlayıcı değil. Nakit hesapta Reg T ve free-riding kuralları sürüyor (`v_capraz` #15).

### 6.2 Vergi ve kayıt (beyanname için)

Mali müşavirle teyit edilmeli.

- **Her kapanan lot için tutulacaklar:**
  - Alış tarihi, alış USD, alış günü TCMB kuru (hangi kur: döviz alışı mı, müşavirle netleştir) → TL maliyet.
  - Satış tarihi, satış USD, satış günü kuru → TL bedel.
  - Komisyon (indirilebilir gider; `abd_pratik` §2.1).
  - TL kâr/zarar.
- Maliyet yöntemini (FIFO ya da ortalama) müşavirle seç ve bütün yıl aynı uygula.
- **Kur farkı vergilenir.** USD'de zararlı bir işlem TL'de kârlı olabilir. Swing ufkunda Yİ-ÜFE endekslemesi pratikte hiç devreye girmez (`v_capraz` #10).
- **Zarar** yalnız aynı yıl içinde, yabancı para menkul kıymet kazançlarıyla mahsup edilir; devretmez.
  - 2026 kısa bir yıl: 9.11–31.12.
- **Tarife ve yük.**
  - 2026 tarifesi %15/20/27/35/40 (190 bin / 400 bin / 1 mn / 5,3 mn TL). Bu dilimler DOĞRULANAMADI (`v_capraz` #11).
  - Örnek: +%30 USD kârın %47,9'u vergi olabilir (`abd_pratik` §2.6).
- **Ödeme takvimi.** Beyan Mart 2027'de; ödeme Mart ve Temmuz taksitleriyle. Geçici vergi yok.
- **Faiz ve temettü.**
  - T-bill/nakit faizi menkul sermaye iradıdır, beyan edilir (`abd_pratik` §4.1).
  - Temettüde ABD stopajı %20; Türkiye'de beyan sınırı 22.000 TL (`v_capraz` #10). Form 1042-S saklanır.
- **Belge seti:**
  - IBKR aylık ve yıllık Activity Statement (CSV + PDF).
  - İşlem teyitleri.
  - SWIFT ve döviz alım dekontları.
  - TCMB günlük kur tablosu: işlem günleri için kaydet.
  - W-8BEN kopyası.
- **Risk.** Sık işlem "ticari kazanç" iddiasına dayanak olabilir. Belirsiz; müşavire sor (`abd_pratik` §2.1).

---

## 7. Öldürme kriterleri ve ileri ölçüm protokolü

### 7.1 Günlük alanları (her işlem bir satır; piramit ekleri ayrı satır)

| Grup | Alanlar |
|---|---|
| Kimlik | İşlem no, ana işlem no (ek için), canlı / gölge / ops, hipotez kartı no |
| Bağlam | Tarih, rejim seviyesi ve skoru, VIX/VIX3M, küme, kümenin ay sonu sırası, kurulum (S1/S2/S3/S1-B), bilançoya kalan seans |
| Plan | Pivot / tetik / limit, ilk stop, stop %, stop/ATR, ATR14, ADR%20, adet, tutar (% hesap), risk $ (R), gap-ayarlı ısı, giriş anında küme ve toplam ısı |
| Uygulama | Dolum fiyatı ve saati, tetiğe göre kayma (bps), komisyon, emir tipi |
| Yönetim | Kısmi satış (tarih, fiyat, R), stop değişiklikleri, ekler |
| Sonuç | Çıkış nedeni (stop / başarısız kırılım / iz süren / zaman / bilanço / rejim / öldürme), çıkış fiyatı, **gerçekleşen R**, MAE (R), MFE (R), tutma süresi (seans) |
| Vergi | Alış ve satış günü TCMB kuru, TL maliyet, TL bedel, TL kâr/zarar |
| Disiplin | Kural ihlali var mı, hangisi; grafik ekran görüntüsü linki |

### 7.2 Ölçüm takvimi ve ölçekleme eşikleri

**Her 25 işlemde hesaplananlar:**
- E[R] ve bootstrap %80/%90 güven aralığı; t = ort(R) / (sd(R)/√n).
- İsabet, ortalama kazanç/kayıp, profit factor.
- En uzun kayıp serisi.
- Net kârın en iyi %10 işlemden gelen payı. Pozitif çarpık sistemde %100'ün üstünde olması normal.
- Kurulum ve rejim bazında E[R].
- Ortalama kayma + maliyet (R cinsinden).
- Kural ihlali oranı.

**İstatistiksel gerçek.**
- sd(R) ≈ 2,5R (pozitif çarpık) ve E[R] = +0,3R ise t = 2 için **~280 işlem** gerekir [H].
- 100 işlem yalnız ipucu verir (t ≈ 1,2).
- +0,2R'lik sistemde sıralı test medyan ~390 işlem ister (`seytan_taban_oranlar` §3.7).

**Ölçekleme eşikleri:**

| Eşik | Koşul | Ne değişir |
|---|---|---|
| L1 | 50 işlem, E[R] ≥ +0,2R, ihlal < %10 | Risk %0,5'e kadar (rejim izin verirse). Sermaye aynı |
| L2 | 100 işlem, ≥ 6 ay, E[R] ≥ +0,3R | Risk %0,75'e kadar |
| C4 | 100 işlem, **12 ay**, E[R] ≥ +0,3R, %80 GA alt sınırı > 0, MDD simülasyon bandında, ihlal < %5 | A kolu × 1,5 (toplamın en fazla %30'u) |
| L3 | 200 işlem, 12 ay, aynı koşullar | Risk %1'e kadar (yalnız R3) |
| Kanıt | ≥ 280 işlem ve t ≥ 2 ya da SPRT H1 kabulü, ve en az bir stres rejimi atlatılmış | A kolu toplamın en fazla %50'si |

### 7.3 Öldürme kriterleri (önceden yazılı, sayısal)

| # | Tetik | Eylem | Dayanak |
|---|---|---|---|
| K1 | A kolu zirveden **−%20** | Yeni işlem durur. Açıklar stoplarla yönetilir. 4 hafta ara ve yazılı inceleme. Yeniden başlarsa %0,25 riskle ve sermaye eklemeden. **İkinci −%20 → kalıcı kapanış** | `seytan_taban_oranlar` §5.1 satır 4 ("kol düzeyinde düşüş > %20 ise dur") |
| K2a | 50 işlemde E[R] < 0 | L0'da kal; kurulum bazında kural incelemesi | `seytan_taban_oranlar` §5.2 #4 |
| K2b | **100 işlemde E[R] < 0** | Kol durur | `seytan_taban_oranlar` §5.2 #4 |
| K2c | **150 işlemde E[R]'nin %80 GA üst sınırı < 0** | Öldür | `seytan_taban_oranlar` §5.1 |
| K3 | 50 işlemlik ortalama kayma + maliyet > **0,15R/işlem** | Aracı kurumu ya da emir yöntemini değiştir. Düzelmezse dur | `seytan_taban_oranlar` §5.2 #3 |
| K4 | Herhangi 20 işlemlik blokta **≥ 3 kural ihlali** (stopu indirmek, boyut aşımı, rejim dışı giriş) | 2 hafta dur | [Ö] |
| K5 | R3 rejiminde biriken ≥ 3 ay ve ≥ 40 işlemde E[R] ≤ 0 | En elverişli ortamda bile kenar yok: öldür | Rejim bağımlılığı (`abd_profesyonel` §3.3) |
| K6 | 12 ayda A kolu, vergi öncesi ve aynı ortalama maruziyetle "rejim ≥ R2 iken RSP, değilse T-bill" basit kuralını geçemiyor | Seçim değer katmıyor: basit kurala geç ya da dur | `seytan_taban_oranlar` §5.3 #6 (kıyas) |
| K7 | 12 ay ve 100 işlemden sonra vergi sonrası TL getirisi < TL nakdin net getirisi **ve** E[R] < +0,3R | Ölçekleme yok. Sürdürülecekse yalnız L0/L1 ile | §1.1 engeli |

### 7.4 Gölge (kağıt) günlük

- R0 günlerinde ve S1-B gibi varyantlar için bütün kurallar kağıt üzerinde uygulanır.
- Kullanılan veri: gün sonu dolum varsayımı. Tetik dolumu = max(tetik, açılış). Limit aşıldıysa "dolmadı" yazılır.
- Gölge işlemler **canlı eşiklere sayılmaz.** Kural kalibrasyonu ve "R0'da beklemenin bedeli" ölçümü için kullanılır.
- Ayrı olarak, mümkünse survivorship'siz günlük veriyle (CRSP/WRDS ya da meşru ücretli sağlayıcı) S1/S2/S3'ün EOD sürümü geriye dönük test edilmeli (`abd_test` §8; `abd_swing_kenarlar` §4.1 protokolü):
  - Örneklem içi 2012–19, örneklem dışı 2020–26.
  - Maliyet: spread + 10 bp.
  - Kabul: OOS'ta E[R] > +0,3R ve yılda ≥ 40 işlem.
  - Bu test geçilmeden L2'ye çıkılmaz [Ö].

---

## 8. Beklenen sonuç aralıkları ve engel karşılaştırması

**İlk 12 ay.** Varsayımlar:
- Kanıt merdiveni L0 → L1. İşlem başı risk %0,25–0,5. Yılda 90–150 işlem.
- Pozisyon dışındaki nakit %4 faiz alıyor (~%2,5 katkı).
- İşlemler 3'lü dalgalar halinde. Dalgaların %30'unda tema bozuluyor ve hepsi birlikte stop oluyor. %8 gap'li kayıp −2R, normal kayıp −1,05R.
- Düşüş merdiveni uygulanıyor.
- Vergi öncesi, USD [H].

| Senaryo | E[R]/işlem (maliyet sonrası) | Öznel olasılık [Ö] | Medyan yıllık | p10 / p90 | MDD medyan / %5 kötü | P(> %20) / P(> %28) |
|---|---|---|---|---|---|---|
| **Kenar yok** (medyan USIC katılımcısına benzer) | −0,15R | %50–60 | **−%2 ile −%3** | −%8 / +%7 | −%7 ile −%9 / −%10 ile −%12 | ~%1–2 / ~%0–1 |
| **Küçük kenar** | +0,15R | %25–35 | **+%3 ile +%6** | −%4 / +%17 ile +%33 | −%6 ile −%9 / −%9 ile −%12 | %6–19 / %2–12 |
| **USIC tipi kenar** (Luk ailesinin DNA'sı) | +0,45R | %10–15 | **+%11 ile +%19** | −%1 ile 0 / +%29 ile +%77 | −%6 ile −%10 / −%8 ile −%13 | %25–49 / %11–40 |

**Kanıt sonrası (2. yıl ve sonrası; 200 işlem, sabit risk) [H]:**

| Senaryo | Risk %0,5 | Risk %0,75 | Risk %1,0 |
|---|---|---|---|
| Küçük kenar: medyan / p10 / p90 / %5 kötü MDD | +%7 / −%9 / +%44 / −%15 | +%8 / −%11 / +%59 / −%20 | +%9 / −%13 / +%71 / −%24 |
| USIC tipi: medyan / p10 / p90 / %5 kötü MDD | +%33 / −%2 / +%100 / −%14 | +%40 / −%3 / +%149 / −%18 | +%48 / −%4 / +%187 / −%21 |

**Okuma.**
1. **İlk yıl, TL'den gelen sermaye için engeli (vergi öncesi %20–28) büyük olasılıkla geçmez.**
   - Senaryo ağırlıklarıyla P(> %20) kabaca %5–10.
   - Gerçek bir +0,45R kenar olsa bile %0,25 riskte medyan ~%11–17 kalır.
   - Yüksek ödülün kaynağı yüksek işlem sayısı × pozitif R × iyi rejimde ilerleyici boyut (`abd_profesyonel` §1.2).
2. **USD'de duran sermaye için engel (~%8–13, §1.1).** Yalnız USIC tipi senaryoda medyanda aşılır. Küçük kenarda aşılmaz.
3. **Kanıt sonrası tablo** "yüksek ödül"ün nereden geldiğini gösteriyor.
   - USIC tipi kenarda %0,75–1 riskle medyan %40–48. %5 kötü MDD −%18/−%21; gerçekte daha kötü olabilir.
   - Kenar küçükse aynı risk medyanda yalnız +%8–9 getirir ve −%20/−%24 düşüş verir.
   - Bu yüzden riski **kanıtsız büyütmek**, kötü senaryonun bedelini katlar.
4. **Benim simülasyonum düşüşleri iyimser gösteriyor.** Merdiven var, küme etkisi 3'lü dalgalarla sınırlı, rejim kalıcılığı yok. Daha kalın kuyruklu referanslar:
   - Rejimli Model B'de %1 risk ve kural yokken medyan %37,6, %5 kötü MDD −%40,6 (`abd_profesyonel` §3.3).
   - SR 0,8 ve %35 vol ile 10 yıllık medyan MDD −%51 (`abd_swing_kenarlar` §11; `v_abd` #37).
   - Arketip A'nın raporlardaki aralığı (tahmin): iyi tema yılında +%40–150, kötü yılda −%10–25, yatay yılda 0–15 (`abd_kim_kazaniyor` §7.1).
5. **Vergi sonrası.** +%30 USD bile TL nakdi ancak başa baş geçer (`abd_pratik` §2.6). Vergi sonrası eşitlik için %20–25+ brüt gerektiği doğrulanmadı; mali müşavir şart (`v_abd` §4 #1).
6. **Belirsizliğin kaynağı.**
   - Senaryo olasılıkları öznel.
   - EOD uyarlaması test edilmedi.
   - Taban oranlar day trade, opsiyon ve CFD verisinden geliyor; swing için doğrudan ölçüm yok (`v_capraz` eksik #10).
   - Rejim şu an düşmanca. Bu, ilk 1–3 ayda işlem sayısını ve dolayısıyla öğrenme hızını düşürür.

---

## 9. Pazartesi 9.11 kontrol listesi (tek sayfa)

**Hafta sonu (7–8.11)**
- [ ] Cuma kapanışıyla rejim tablosunu doldur (§3.1; Pine `A_Rejim`). Not et: S&P vs 200 GHO (~7.327), VIX/VIX3M, RSP vs 50 GHO, S5FI, MAHQ − MALQ. Seviye: R0 mı, R1 mi?
- [ ] NFP sonucu, İran/Hürmüz haberleri, Senato kesin sonuçları (`hazırlık` §6.1).
- [ ] Hesap durumu: Midas onayı? IBKR başvurusu gönderildi mi? Midas'ta STP LMT ve GTC STP emri var mı?
- [ ] (a) ve (b) taramalarını çalıştır. Kümelere ayır (§4.2). Küme başına ilk 5'i seç (§4.3).
- [ ] Her aday için yaz: kurulum, pivot/tetik/limit, stop, stop %, stop/ATR, ADR%, bilanço tarihi. Stop koşulunu sağlamayanı ele.
- [ ] Teyit et: BRK-B (9.11?) ve MDT bilanço tarihleri; NVDA 17.11; U/EW/SN'de 1. gün S2 kriterleri.
- [ ] Günlük şablonunu aç (§7.1); hipotez kartları S1, S2, S3 (değiştirilemez, tarihli).

**Pazartesi 08:00–12:00 TSİ**
- [ ] Gece haberleri ve AMC bilançoları; pre-market 12:00'den itibaren.
- [ ] Rejim R0 ise: **canlı emir yok.** Gölge emirleri günlüğe yaz. Bitti.

**Pazartesi 12:00–17:25 TSİ (yalnız R1 ve hesap hazırsa)**
- [ ] En fazla **2** giriş emri, farklı ve AI dışı kümelerden; kümenin 1. sırasındaki isim.
- [ ] Boyut: adet = hesap × %0,25 / (tetik − stop). Pozisyon ≤ %12,5. Gap-ayarlı toplam ısı ≤ %1,5.
- [ ] Emir: BUY STOP-LIMIT (tetik = pivot + %0,1; limit = tetik + %1,5; DAY) ve ekli GTC SELL STOP (RTH, piyasa).
- [ ] 17:25'ten sonra emir değiştirme yok. **17:30–24:00 arası ekrana bakma.**

**Salı 10.11 (CPI 16:30)**
- [ ] 16:30'dan önce yeni giriş emri yok. 16:35–17:25 arası: S&P vadelisi < −%1 ise yeni girişleri iptal et, değilse gir.

**Her gün sonu / ertesi sabah**
- [ ] Rejim skoru → seviye.
- [ ] Açık pozisyonlar: başarısız kırılım (ilk 3 seans), kısmi koşulu (+2R ya da 4. seans ≥ +1R), kapanış < 10/20 GHO, zaman stopu (10 seans). Gerekirse MOO çıkış emri.
- [ ] Isı (gap-ayarlı), küme ısısı, aylık zarar + ısı < %4.
- [ ] Günlüğü doldur: R, MAE/MFE, kayma, TCMB kuru.

**Cuma 13.11 kapanışından sonra**
- [ ] Haftalık rapor: rejim, işlem sayısı, E[R], ihlaller. GTC acil stopları yükselt.

**Asla**
- [ ] AI çip/güç dip alımı · bilanço öncesi yeni giriş · zarardaki pozisyona ekleme · stopu aşağı çekme · %1'in üstünde risk · 30 günden kısa OTM opsiyon · marj (ilk 12 ay).

---

## 10. Doğrulanmamış ve açık noktalar

1. **Hiç test edilmedi:** S1/S2/S3'ün EOD uyarlaması ve beklentisi (`v_abd` §4.2; `v_profesyonel` eksik #8). Plan bir hipotezdir; §7 bunun ölçümüdür.
2. **Doğrulanmamış uygulayıcı istatistikleri:**
   - Luk'un isabet ve R rakamları (`v_abd` #15).
   - Minervini'nin isabeti ve 2,15× oranı (`v_profesyonel` A3).
   - Kullamägi'nin bütün rakamları öz beyan (`v_profesyonel` A1–A2).
3. **Ajanın kendi hesabı, tekrarlanmadı:** küme korelasyonu 0,72 (`v_profesyonel` A14). Monte Carlo'lar kalibre edilmemiş varsayımlara dayanıyor (`v_profesyonel` #11). Bu dosyadaki MC de öyle.
4. **Midas:** emir tipleri, kur makası, marj ve pre/post-market erişimi kamuya açık sayfalarda yok (`hazırlık` §7).
5. **IBKR:** hangi kuruluşa bağlanılacağı ve buna bağlı ETF erişimi. MOO/MOC son giriş saatleri (bellek; teyit et). Koşullu MOC kurulumunu kağıt hesapta dene.
6. **Vergi:**
   - 2026 dilimleri (`v_capraz` #11) ve kambiyo BSMV.
   - Hangi TCMB kurunun kullanılacağı ve maliyet yöntemi.
   - "Ticari kazanç" riski.
   - Veraset vergisi açısından nakit aracının konumu.
7. **Takvim:** NVDA tarihi (17.11 IR'ye göre, görev notu ~19.11), BRK-B ve MDT bilanço tarihleri, perakende satış verisinin tarihi (`hazırlık` §7).
8. **Genişlik verisi:** S5FI ve benzerleri TradingView önbelleğinden, zaman damgaları karışık (`hazırlık` §7). Pazartesi kendi grafiğinde teyit et.
