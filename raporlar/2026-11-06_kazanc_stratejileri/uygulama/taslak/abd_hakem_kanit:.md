# ABD planları A / B / C: KANIT hakemi kararı

**Tarih:** 06.11.2026, ~14:00 TSİ.
**Lens:** Kanıta sadakat ve istatistiksel dürüstlük. Sorular: her kural doğrulanmış bir bulgudan çıkıyor mu, beklenti aralıkları destekleniyor mu?

**Okunanlar:**
- Taslaklar: `uygulama/taslak/abd_A.md`, `abd_B.md`, `abd_C.md` (tamamı).
- Doğrulama dosyaları: `dogrulama/v_abd.md`, `v_capraz.md`, `v_dalga.md`, `v_profesyonel.md`.
- Atıfların kontrol edildiği bölümler:
  - `ajanlar/abd_test.md` §0, §3.1, §6.4
  - `abd_swing_kenarlar.md` §3–§6
  - `abd_profesyonel.md` §1.3–§1.4, §3.3, §3.5
  - `abd_kim_kazaniyor.md` §5.2–§5.4
  - `seytan_taban_oranlar.md` §3.7, §5
  - `abd_pratik.md` §1.2, §2.5
  - `dalga_abd.md`
  - `uygulama/abd_hafta_hazirlik.md` §1.2–§1.3, §2.1, §3

**Yöntem notu:**
- Yeni veri çekilmedi.
- Taslakların kendi backtest'leri (A'nın MC'si, B'nin BT-B'si, C'nin C-TEST'i) yeniden koşulmadı. Yalnız iç tutarlılık ve aritmetik kontrol edildi.
- **[H]** etiketi bu dosyadaki kendi kaba hesaplarımı gösterir.

---

## 1. Puan tablosu (0–10)

| Ölçüt | A (lider swing, EOD) | B (rejim çekirdeği + uydu) | C (önce risk, kanıt minimalizmi) |
|---|---|---|---|
| Kanıta sadakat | 7 | 5 | **8** |
| Pazartesi uygulanabilirlik (gün içi yok, erişim, emir tipleri) | **8** | 6 | 7 |
| Risk kontrolü ve en kötü durum | 8 | 5 | **9** |
| Beklenti gerçekçiliği (engel + TR vergisi) | 7 | 7 | **9** |
| Profile uyum (swing, yüksek ödül, kümeler) | **8** | 4 | 6 |
| **Toplam (50)** | **38** | **27** | **39** |

**Kazanan: C (iskelet olarak), A'nın işlem mekaniği aşılanarak.**
- A çok yakın ikinci. Kullanıcı profiline daha iyi uyuyor; çıkış ve emir mekaniği en ayrıntılı taslak.
- B iskelet olarak önerilmez. Vergi tablosu ve kademeli transfer fikri alınmalı.

---

## 2. Kazanan ve gerekçe

C şu dört konuda üç taslağın en dürüstü.

**(i) Engel hesabı.**
- C, engeli hesap büyüklüğüne ve yatırımda kalma oranına (u) göre hesaplıyor. Pozisyon içindeki kur artışının sıfır USD getiride bile vergi doğurduğunu ("hayalet vergi") sayısallaştırıyor (`abd_C` §1.2).
- Tam yatırım satırı (250 bin $, u=1: %22,1–30,5) doğrulanmış çapayla tutarlı: ~%20–28 (`v_capraz` #22).

**(ii) Ölçek kapıları.**
- Kapılar t-istatistiğine bağlı (Faz 2: t ≥ 1,0; Faz 3: t ≥ 1,65 ve 12 aylık engel geçilmiş).
- Hipotez kartında denenen varyant sayısı (N) yazılıyor (`seytan_taban_oranlar` §5.3 #1).
- Ayrıca "kaçan sinyaller" sekmesi ve beta-sızıntısı öldürme kuralı (K8) var.

**(iii) Uydurma kenar yok.**
- Hangi kolun yayın sonrası kanıtı olmadığını açıkça yazıyor: S2 insider (`v_abd` #26), S1'in EOD uyarlaması (`v_abd` §4.2).
- Bilanço filtresinin "alfa değil, eleme" olduğunu `abd_test` §6.4'teki sadece-uzun sonuçlarla gerekçelendiriyor.

**(iv) En sıkı kuyruk kontrolü.**
- Hesap toplam sermayenin %10'u (en çok %15'i).
- Faz 1'de toplam ısı %1–3, aylık devre kesici %3.
- −%15'te plan duruyor. En kötü durumda kayıp toplam servetin ~%1,5–2,25'i.

Bu dört nokta A'daki karşılıklarından daha kanıta dayalı. A'nın beklenti tablosu ise kalibre edilmemiş bir MC'ye ve öznel senaryo ağırlıklarına dayanıyor (§3.1).

C'nin zayıf yanları:
- Profil uyumu düşük: episodic pivot kolu yok, yüksek ödül yıllarca erteleniyor.
- S3 (VIX çözülmesi) kolu örneklem içi bir teste dayanıyor ve fazla büyük boyutlandırılmış (§3.3).

Önerim: bu iki zayıflık A'dan ve kendi düzeltmelerinden aşılanarak giderilir (§5).

---

## 3. Taslak bazında bulgular

### 3.1 A: ölümcül kusur yok; üç ciddi sorun

**A1. Beklenti tablosu kanıttan çok varsayım (§8).**
- Senaryo olasılıkları öznel. "USIC tipi kenar" (+0,45R/işlem) satırı, Luk'un **doğrulanamayan** 104/319 istatistiğinden türetilmiş +0,48R aritmetiğine çok yakın (`v_abd` #15; `abd_kim_kazaniyor` §5.2).
- Bu senaryoya %10–15 olasılık vermek cömert:
  - USIC'te katılımcıların yalnız %8–17'si **yılı kârla** kapatıyor (`v_abd` #14). Kâr etmek +0,45R kenar anlamına gelmez.
  - EOD uyarlaması kazanç R'ını düşürür (`v_profesyonel` A12, eksik #8).
  - Bu yüzden "P(>%20) ≈ %5–10" büyük olasılıkla üst sınır.
- "Kanıt sonrası" tablosu (%1 riskte medyan +%48, p90 +%187, %5 kötü MDD −%21) desteklenmiyor. A bunu kendisi de söylüyor (§8 madde 4).
  - Savunulabilir referans, `abd_profesyonel` §3.3 Model B: %1 risk ve kural yokken medyan %37,6 / %5 kötü MDD −%40,6; merdivenle %20,6 / −%18,9.
  - Bu model de kalibre edilmemiş (`v_profesyonel` eksik #11).

**A2. R1 rejimi doğrulanmış anahtardan gevşek.**
- R1 yeni long'a izin veriyor ama ne NDX/S&P 10>20 GHO arıyor ne de FTD.
- Çelişki:
  - `abd_profesyonel` §3.5 #6: "Kapalıyken yeni long yok"; pilot ancak FTD ya da 10>20 ile (§1.4).
  - `seytan_taban_oranlar` §5.1 satır 4: "yalnız endeks kısa GHO'ların üstündeyken".
- Hazırlık dosyası FTD öncesi %25–50 boyuta izin veriyor (`abd_hafta_hazirlik` §0, §6). Kanıt karışık, ama R1 kendi başına test edilmemiş bir tasarım.
- Ek sorun: R1'i yeniden açan ana bileşen VIX/VIX3M < 1. `v_profesyonel` A11 bu terslik argümanını "zayıf, tek günlük sıçrama" diyor; rejim hükmünü geçerli kılan NDX 10<20. VIX bir günde normale dönerse A, NDX hâlâ kırıkken pilot açabilir.

**A3. Boştaki USD.**
- C3 kuralı boştaki USD için "IBKR nakdi ya da T-bill" diyor.
- `abd_pratik` §2.5'e göre dövizin kur kazancı vergisiz, menkul kıymet içindeki kur kazancı vergili. T-bill bir menkul kıymet olduğu için A kendi hurdle formülündeki u etkisini burada bozuyor. B ve C bunu doğru ele alıyor.

**Küçük notlar:**
- L1 kapısı (50 işlem, E[R] ≥ +0,2R, t şartı yok) sıfır kenarlı bir sistemde ~%28 olasılıkla geçilir [H: sd 2,5R, SE 0,35R, z 0,57]. Riski iki katına çıkarmanın bedeli küçük, ama istatistik olarak gürültü.
- CPI günü "vadeli −%1'den fazla düşükse iptal" kuralı [Ö]; kanıtı yok. Etiketli olduğu için sorun değil.

### 3.2 B: bu kullanıcı için ölümcül iki kusur

**B1 (ölümcül, profil).**
- Hesabın %50'si (B-Agresif'te %70'i) S&P'de kapılı, oynaklık ölçekli, en çok 2x kaldıraçlı bir trend pozisyonu.
- Kapı 1% bantla yıllarca açık kalabilir. Bu fiilen zamanlı al-tut.
- Kullanıcının iki açık şartıyla çelişiyor: "al-tut yok" ve "en fazla birkaç ay".

**B2 (ölümcül, kanıt ve ödül).** Çekirdek kenar değil, beta.
- B'nin kendi testinde hiçbir filtre Sharpe'ı artırmıyor (1928+ SR 0,60–0,64; Ek A).
- N25'in 2010–26 getirisi %13,8. Bu, 1x al-tutun altında (`abd_test` §3.1: MKT 1x BH 2010–26 %14,1).
- Doğrulanmış çapa da aynısını söylüyor: filtre 2010 sonrası getiriyi kesti (`abd_test` §0 #1; `v_abd` §2.1).
- Sonuç olarak B'nin tıraşlı merkezi ~%10. Bu, TL engelinin 8–18 puan altında; B bunu kendisi kabul ediyor (§1.2, §8.3).
- Yani plan, "yüksek ödül" sorusuna kanıtlı bir yol önermiyor. Riskini ise artırıyor:
  - B-Standart MaxDD −%20…−%35.
  - B-Agresif −%30…−%45.
  - 1987 tipi gap'te çekirdek −%35 (BT-B).
  - Toplam brüt %155'e kadar çıkabiliyor.

**B3. Doğrulanmamış kendi testleri.**
- BT-B ~30 varyanttan seçilmiş ve hiçbir doğrulama turundan geçmemiş.
- B, 2–3 puan tıraş uyguluyor. İyi bir refleks, ama tıraşın büyüklüğü keyfi.
- Uydu-R kuralı `dalga_abd`'deki ızgaranın en iyilerinden (L12s0; 140 kuralın 3.'sü). `v_dalga` §3.2'ye göre k≥3 kuralların 2015+ medyanı (%12,2) piyasanın (%13,5) altında. B'nin "piyasa ± 4 puan" beklentisi bununla tutarlı, ama 30'luk ağırlık için gerekçe zayıf.
- Uydu-R'nin haftalık 50 GHO zamanlaması ve %12 GTC stopu test edilmedi; B bunu kendisi yazıyor.

**B4. Erişim ve vergi belirsizliği çekirdeğin tam ortasında.**
- Teyit edilmemiş üç nokta (B kendisi de işaretliyor):
  - TR mukimi için CME micro vadeli izni (`v_abd` §4 #7).
  - Yurt dışı vadeli kazancının vergi niteliği (`v_capraz` eksik #9).
  - IBIE/PRIIPs nedeniyle ABD ETF erişimi.

**B5. Sermaye kapısında istatistik eksik.**
- H/W payını artırma kapısı tek bir yılın vergi sonrası getirisine bağlı: USD nakit + 3 puan.
- Oysa B'nin kendi 12 aylık dağılımı P10 −%2 ile P90 +%26 arasında ve B kendisi "ilk yıl yöntem hakkında az şey söyler" diyor.

**Küçük atıf hataları:**
- "Kaldıraçlı al-tut 2x %23,9 (T §0.1)" rakamı `abd_test`'te yok. §3.1'de MKT 2x BH 2010–26 %22,3.
- "%20,8 / −%78" lag0 ve 252 gözlem/yıl yanlılığıyla hesaplanmış. Takvim yılı düzeltmesiyle %21,7, lag1 ile %18,7 / −%88 (`v_abd` §2.1).
- Vergi sonrası beklenti iki yerde iki farklı rakam: özet §0 #12'de "%1–6", §8.3'te "%3,0–4,3".

### 3.3 C: ölümcül kusur yok; üç ciddi sorun

**C1. S3 (VIX çözülmesi) örneklem içi ve fazla boyutlu.**
- Başlıktaki t=3,69, 40 günlük fazla getirinin **sıfıra** göre t'si. Ama koşulsuz 40 günlük piyasa getirisi zaten ~+%2,1 (C bunu da yazıyor).
- Asıl artımsal kenar ~+1,8 puan. Kaba t'si ≈ 1,7 [H: olay başına σ ≈ 3,94·5/3,69 ≈ %5,3; SE ≈ %1,07].
- 2 tanım denendi, örneklem 2009–26 boğası, n=25.
- %50 tıraştan sonra kalan kenar ≈ +%0,9/olay. Bunun t'si ~1, yani bilgi yok.
- Buna rağmen S3'te işlem riski S1'in iki katı (%0,5) ve pozisyon E'nin %25'ine kadar çıkabiliyor.
- Öneri: S3 yalnız rejim girdisi olarak kalsın. İşlem olarak açılacaksa %0,25 risk ve gölge kayıtla, örneklem dışı 5+ olaydan sonra yeniden değerlendirilsin.

**C2. S2 (insider küme alımı) bugün uygulanamıyor.**
- Kanıtın tamamı 1986–2007 (`v_abd` #26). Yayın sonrası bağımsız test yok.
- 21 günde %3,8 rakamını hiçbir doğrulayıcı teyit etmedi (C bunu yazıyor).
- Veri kaynağı 06.11'de 503 verdi. "Rutin değil" filtresi 3 yıllık Form 4 geçmişi istiyor. Bu, gün içi ekransız ama ağır bir manuel iş.
- C kolu "ölçüm" diye etiketliyor. Doğru etiket, ama Faz 1'de canlı risk almak yerine gölge kayıt daha tutarlı olur.

**C3. Rejim ve kural metni çelişkileri.**
- KIRMIZI'nın tek tetiği VIX/VIX3M ≥ 1. `v_profesyonel` A11 bu göstergeyi zayıf sayıyor.
- SARI, NDX 10<20 iken bile pilot S1 girişine izin veriyor. Bu, A2 ile aynı sapma.
- §7.3'te "12 ay ve 100 işlemden önce yalnız öldürme kararı verilebilir (SEY §5.3 #4)" yazıyor. Aynı tablo Faz 2'yi (risk ×2) 50 işlem ve 4 ayda açıyor. Bu bir iç çelişki: A ve B bu sapmayı açıkça adlandırıyor, C bir cümlede reddederken tabloda uyguluyor.

**Küçük notlar:**
- Engel tablosunun d=%32,9 sütunu bir kur tahmini değil. Bu oran faiz paritesinin (CIP) sonucu ve uzak vadeler likit değil (`v_capraz` #5). Anketin 12 aylık kur beklentisi 59,26, yani ~%18,4 (`v_capraz` #3). Özetteki "~%0–9 yetiyor" cümlesi senaryo olarak okunmalı.
- Engel "%13–26" düşük görünüyor, çünkü u ≈ 0,3 (E'nin çoğu nakitte). Doğrulanmış çapa (%20–28) tam yatırım içindir. İkisi çelişmiyor, ama karşılaştırma yapılırken u belirtilmeli.
- İlk yıl beklentisine giren +%2,4 nakit faizi için teyit gerekiyor [bellek, doğrulanmadı]. IBKR'nin boş nakit faizi küçük hesaplarda ilk 10 bin $'a ödenmeyebilir ve 100 bin $ altında orantılı düşebilir. 50 bin $'lık E'de bu katkı belirgin küçülebilir.

---

## 4. Doğrulanmış gerçeklerle çelişkiler ve sapmalar

| # | Konu | Taslak | Doğrulanmış olgu | Hüküm |
|---|---|---|---|---|
| 1 | NVDA bilanço tarihi | A, B, C: 17.11 AMC (teyit notuyla) | Görev notu "~19.11 (verify)". `abd_hafta_hazirlik` §2.1 NVIDIA IR bağlantısıyla 17.11 diyor | Çelişki görev notunda. Üç taslak doğru davranıyor |
| 2 | Filtre 2010 sonrası getiriyi kesti | B çekirdeği getiri kaynağı gibi konumluyor (%50–70 ağırlık) | `abd_test` §0 #1, §3.1; `v_abd` §2.1 | B kendi rakamlarıyla teyit ediyor (13,8 < 14,1). Konumlandırma çelişkili |
| 3 | Sektör momentumu 2010 sonrası risk-ayarlı olarak piyasa düzeyinde | A ve C filtre diyor; B %30 ağırlık, "piyasa ± 4" | `v_abd` §2.2; `v_dalga` U4, U7 | Hepsi uyumlu; B'nin ağırlığı gerekçesiz |
| 4 | Sıkı rejim anahtarı (10>20, FTD) | A R1 ve C SARI 10<20'de pilot açıyor; B FTD istiyor | `abd_profesyonel` §1.4, §3.5 #6; `seytan_taban_oranlar` §5.1 #4; hazırlık §0 FTD öncesi %25–50 | A ve C sapıyor (küçük boyutla). B en sadık |
| 5 | VIX terslik argümanı zayıf | A ve C'de R0/KIRMIZI'nın ana tetiği | `v_profesyonel` A11 | Kural olarak meşru, ama yeniden açılış bu göstergeye bağlanmamalı |
| 6 | 12 ay ve 100 işlemden önce boyut büyütme yok | Üçü de 50 işlemde riski %0,25'ten %0,5'e çıkarıyor | `seytan_taban_oranlar` §5.3 #4 | A ve B sapmayı adlandırıyor; C kendi metniyle çelişiyor |
| 7 | Boştaki USD ve kur farkı vergisi | A: T-bill de olur. B ve C: nakit | `abd_pratik` §2.5 (teyit gerek); `v_capraz` #10 | A tutarsız |
| 8 | Luk ve Minervini istatistikleri doğrulanamadı | A'nın "USIC tipi" senaryosu bu girdiye yakın | `v_abd` #15; `v_profesyonel` A3 | A etiketliyor, ama olasılık ağırlığı cömert |
| 9 | Opsiyon alımı ortalamada kaybettiriyor | A: R3 ve IV ucuzken. B: ilk 6 ay yok. C: Faz ≥2, YEŞİL, IV rank ≤30 ve IV ≤ HV20 | `v_profesyonel` A6, A8 | Üçü uyumlu; C en sıkı |
| 10 | Midas: yalnız call/put alımı; stop, GTC, MOO desteği bilinmiyor | Üçü de teyit şartı koyuyor | `abd_hafta_hazirlik` §1.2 | Uyumlu |
| 11 | IBKR ile gerçekçi ilk işlem 11–13.11 | Üçü de kabul ediyor | `abd_hafta_hazirlik` §1.3 | Uyumlu |
| 12 | 2026 zararı 2027'ye devretmez | A C5, B §6.5, C §6.4 | `v_capraz` #10 | Uyumlu |
| 13 | Yüzdesel komisyon | A: %3 stopta 0,17–0,2R. C: %6 stopta 0,08R | `abd_pratik` §1.1 | İkisi de doğru; oran stop mesafesine bağlı |
| 14 | 2x ve 3x kaldıraç rakamları | B: "2x %23,9 (T §0.1)" | `abd_test` §3.1: %22,3 | B'de atıf hatası |

---

## 5. Aşılanacak en iyi fikirler (öncelik sırasıyla)

1. **Sermaye kararı: C §1.2 ve B §8.3 birlikte.**
   - Engel, hesap büyüklüğüne ve u'ya göre hesaplanır; "hayalet vergi" ayrıca gösterilir.
   - Vergi öncesi R'den vergi sonrası USD'ye geçiş tablosu (50k / 250k / 1m) karar ekranına konur.
   - Tam yatırım satırı doğrulanmış %20–28 çapasına göre denetlenir.
2. **Boştaki USD aracı kurumda nakit tutulur, T-bill'e ya da para piyasası ETF'ine konmaz.** Gerekçe `abd_pratik` §2.5; mali müşavir teyidi şart.
   - B §1.3'teki kademeli transfer de eklenir: gerekmeyen pay TL'de bekler, rejim tetiği gelince taşınır.
   - A C2'nin "rejimin izin verdiği brüt kadar çevir" kuralı aynı fikrin hisse koluna uyarlanmış hâli.
3. **İstatistik kapıları: C §7.**
   - Hipotez kartında N yazılır.
   - Faz 2: t ≥ 1,0. Faz 3: t ≥ 1,65, 12 ay ve engel geçilmiş.
   - "Kaçan sinyaller" sekmesi tutulur; K8 beta-sızıntısı öldürme kuralı uygulanır.
   - A K6 eklenir: 12 ayda "rejim açıkken RSP, değilse T-bill" kuralını geçemeyen kol durur (`seytan_taban_oranlar` §5.3 #6).
   - SEY §5.3 #4'ten sapma açıkça yazılır: 50 işlemde yalnız işlem riski artar, sermaye artmaz.
4. **EOD çıkış mekaniği: A §2.4 ve §2.7.**
   - Kısmi satış: kapanış ≥ +2R ya da 4. seans ≥ +1R → ertesi açılışta MOO. Ardından stop başabaşa.
   - İz süren çıkış: kapanış 10/20 GHO altına inerse ertesi açılışta MOO.
   - 10 seanslık zaman stopu; ilk 3 seansta başarısız kırılım kuralı.
   - **OCA "orantılı küçült" uyarısı:** kısmi limit dolunca stop tüm adedi satıp açığa satış doğurmasın.
   - Koruyucu stop stop-limit değil, piyasa stopu olur.
5. **Rejimin yeniden açılması doğrulanmış bileşene bağlanır.**
   - Pilot için FTD **ya da** NDX/S&P 10>20 şartı aranır (`abd_profesyonel` §1.4; B §3.2).
   - VIX/VIX3M < 1 gerekli koşul olarak kalır, ama tek başına yetmez (`v_profesyonel` A11).
6. **Gap-ayarlı ısı ve maliyetin R cinsinden ölçülmesi.**
   - Gap-ayarlı ısı = adet × max(stop, 1,5 ATR); bilanço penceresinde 2 × implied move (`abd_profesyonel` §3.5 #5).
   - Komisyon R cinsinden tablolanır (C §5.3). Yüzdesel komisyonlu Türk kurumları lider kolundan çıkarılır.
7. **Düşüş merdiveni.**
   - C §5.2'deki gibi kayıp serisi matematiğine göre kalibre edilir: %0,25 riskte −%4 = 16R (`abd_kim_kazaniyor` §5.3).
   - B §5.3'teki bulgu da alınır: merdiven yalnız rejime bağlı kolda değer katar, sistematik kolda yalnız getiri alır. Bu `abd_profesyonel` §3.3 ile tutarlı.
8. **AI kümesine dönüş kuralı: A §4.5** (`dalga_abd` §7.4 ile tutarlı).
   - Pilot için: SMH 10 seans 50 GHO üstünde, SMH/SPY oranı 3 aylık zirvede, hissede yeni Stage 2 bazı. Bu aşamada yarım küme ısısı.
   - Tam ısı ancak 12 aylık RS zirvesiyle.
   - Ölçülene kadar sağlık alt kümeleri tek küme sayılır.
9. **Episodic pivot (A S2) gölge kolda başlar.**
   - Canlıda değil, gölge günlükte (A §7.4) koşulur. Gerekçe: konsantre EP'nin hakemli kanıtı yok, sadece-uzun earnings portföyleri VW'yi geçmiyor (`abd_swing_kenarlar` §4.1; `abd_test` §6.4).
   - EOD testi geçerse canlıya alınır. Bu, C'nin dışlaması ile A'nın kapsaması arasında kanıta uygun orta yol ve profilin sağ kuyruk kaynağını açık tutuyor.
10. **Vergi takvimi.**
    - 9.11–31.12.2026 ayrı bir vergi yılı; küçük boyutta kalınır (A C5).
    - Aralık başında vergi kontrolü yapılır, ama yalnız vergi için çıkış yapılmaz (C §6.4).

---

## 6. Beklenti aralıkları: hangisi destekli?

| Taslak ve rakam | Dayanak | Hüküm |
|---|---|---|
| A, 1. yıl: medyan −%3…+%19, senaryo ağırlıklı ~%0–5 | Kendi MC'si [H] ve öznel ağırlıklar; "USIC tipi" girdisi doğrulanmamış | **Kısmen.** "Kenar yok" senaryosu taban oranlarla uyumlu. Üst senaryonun ağırlığı cömert |
| A, kanıt sonrası: %1 riskte medyan %40–48 | Aynı MC; düşüşler iyimser (A kabul ediyor) | **Desteklenmiyor.** Referans: `abd_profesyonel` §3.3 Model B (%20,6 / −%18,9, merdivenle) |
| B, çekirdek: %8–12, MaxDD −%25…−%45 | BT-B (doğrulanmamış, ~30 varyant); `abd_test` §3.1 ile yön tutarlı | **Kısmen.** Getiri tarafı muhtemelen üst uçta; DD aralığı makul |
| B, Uydu-R: piyasa ± 4 puan | `v_dalga` U4, U5 | **Destekli** |
| B, toplam: %6–14, merkez %10 | Yukarıdakilerin bileşimi | **Kısmen.** TL engelinin altında kaldığını dürüstçe söylüyor |
| C, 1. yıl: −%8…+%15, merkez +%2–6 | Şeffaf aritmetik (işlem sayısı × risk × E[R] + nakit) | **Destekli.** Nakit faizi katkısı küçük hesapta teyit edilmeli |
| C, S3: olay başına +0,25…+0,5R | Kendi örneklem içi testi, n=25 | **Zayıf.** Artımsal t ≈ 1,7 [H], tıraştan sonra ~1 |
| C, S2: −0,1…+0,25R | 1986–2007 kanıtı | **Tahmin.** Kanıt yayın sonrasına taşınmamış |
| C, Faz 3: medyan +%17…+%30 | +0,25–0,35R kenar şartına bağlı aritmetik | **Koşullu.** Kenarın kendisi doğrulanmamış |

**Ortak sonuç.** Üç taslak da 1. yılda TL'den gelen parayı yenmeyi beklemiyor. Bu, doğrulanmış bulgularla tutarlı:
- Anomaliler çürüdü (`v_abd` #22).
- USIC'te kârda olan pay %8–17 (`v_abd` #14).
- EOD uyarlaması hiç test edilmedi (`v_abd` §4.2).

Bu dürüstlüğü en tutarlı ve sayısal biçimde taşıyan taslak C.

---

## 7. Birleşik plan için teyit listesi

1. Midas: buy stop-limit, GTC stop ve MOO desteği (1 adetle test). Desteklemiyorsa lider kolu IBKR'yi bekler.
2. IBKR: bağlanılacak kuruluş (IB LLC mi IBIE mi), ABD ETF erişimi, MOO/MOC son giriş saati, küçük hesapta nakit faizi kademeleri.
3. Vergi:
   - Elde tutulan USD'nin kur farkının vergisizliği.
   - Hangi TCMB kurunun kullanılacağı.
   - 2026 tarifesi (`v_capraz` #11'e göre doğrulanamadı).
   - "Ticari kazanç" riski.
   - Yurt dışı vadelinin vergi niteliği (yalnız B'ye özgü bir çekirdek kurulursa).
4. NVDA tarihi (17.11), BRK-B ve MDT bilanço tarihleri.
5. EOD S1/S2 kurallarının hayatta kalma yanlılığından arınmış veriyle geriye dönük testi: örneklem içi 2012–19, dışı 2020–26 (A §7.4). Bu test yapılmadan riskin %0,5'in üstüne çıkarılmaması önerilir.
