# ABD planları A / B / C: hakem raporu, DEĞER merceği

**Tarih:** Cuma 06.11.2026, ~14:00 TSİ. Son kapanış 05.11 (NFP öncesi).
**Mercek:** Maliyet ve Türkiye vergisi sonrası beklenen değer. Kıyas iki engelle yapıldı: TL'de kalmak (TL carry) ve USD nakit/T-bill. Ayrıca iki soru soruldu: "yüksek ödül" hedefi dürüstçe karşılanıyor mu, ve hangi getiri/düşüş dağılımı beklenmeli?
**Okunanlar:** `taslak/abd_A.md`, `abd_B.md`, `abd_C.md`. Kontrol için `dogrulama/v_abd.md`, `v_capraz.md`, `v_dalga.md`, `v_profesyonel.md`, `ajanlar/abd_pratik.md` §2–4, `abd_profesyonel.md` §3.3, `tr_makro_engel.md` §5.1 ve `uygulama/abd_hafta_hazirlik.md` (kısaca `hazırlık`) kullanıldı.
**Etiketler:** [H] benim hesabım (betikler §8'de), [Ö] öznel tahmin. Vergi hesapları 2026 tarifesini varsayıyor. Bu tarife doğrulanamadı (`v_capraz` #11).

---

## 0. Kısa hüküm

- **Kazanan: C**, A ve B'den aşılarla (§6). C riski en iyi sınırlıyor, vergiyi en doğru modelliyor ve en az kanıtsız kural taşıyor. Ama "yüksek ödül" kısmında iki hesap hatası var (§3.3).
- **Hiçbir plan TL'den gelen sermaye için ilk yılda engeli geçmiyor. Üçü de bunu açıkça yazıyor.** İlk yılda vergi sonrası USD getirisi kabaca şöyle [H, §2.2]:
  - A ve C: ~%0–2,5. Bu, USD nakdin vergi sonrası %2,4–2,9'u kadar ya da biraz altında.
  - B: ~%1–6.
  - TL'de kalmanın USD karşılığı ise %9–14.
  - Toplam servete maliyet yılda ~%1–2,5. Proje TL carry'ye göre beklenen değerde negatif. Gerekçesi bilgi edinmek (kenarı ölçmek) ve TL şokuna karşı çeşitlendirme, getiri değil.
- **B'nin çekirdeği bu kullanıcı için ölümcül kusurlu.** Kaldıraçlı endeks betası yıllarca açık kalabiliyor ve bu "al-tut yok" profiliyle çelişiyor. Üstelik vergi sonrası USD nakdin ancak ~0–1 puan üstünde getiri için −%25/−%45'lik bir düşüş bütçesi harcıyor.
- **Asıl değer kaldıracı ABD kurulumu değil, TL tarafı.** Servetin %75–90'ı TL'de kalıyor. TL carry 2010–26'da USD bazında yılda −%7,2 kaybettirdi, en büyük düşüşü −%85 (`v_abd` #34). Bu riski yöneten tek kural C'nin döviz anahtarı (§6, aşı 4).

---

## 1. Puan tablosu (0–10)

| Ölçüt | A | B | C | Kısa gerekçe |
|---|---|---|---|---|
| Kanıta sadakat | 7 | 7 | **8** | A, doğrulama "gitti" dediği EP/gap kolunu canlı tutuyor. B kendi testini (BT-B, ~30 varyant, örneklem içi) açıkça ifşa ediyor. C yalnız doğrulamadan sağ çıkan kuralları kullanıyor, ama S3'ün t=3,69 başlığı yanıltıcı |
| Pazartesi uygulanabilirliği (gün içi yok, erişim, emir tipi) | 7 | 6 | **8** | A: R0 ise kayıt, R1 ise 2 pilot. B'nin tek eylemi ABD ETF'i MOO; bu da PRIIPs/IBIE, Midas MOO ve IBKR'nin 11–13.11'e hazır olmasına bağlı. C: emir testleri, S3 kurulu, saatler net |
| Risk kontrolü ve en kötü durum | 8 | 5 | **9** | Toplam servete en kötü kayıp: A ~−%2/−4. B ~−%4,5/−7,5 (H −%30'a kadar sürüyor; çekirdek 1987'de −%35). C ~−%1,5/−2,3 |
| Engele göre beklenen değerin gerçekçiliği (TR vergisi dahil) | 7 | 7 | 7 | A dağılımı en iyi raporluyor, ama vergi modeli kaba. B'nin vergi tablosu iyi, merkez tahmini iyimser. C'nin vergi modeli en iyisi, ama Faz 3'te iki kat iyimser ve hesabın tamamını hemen çeviriyor |
| Profile uyum (swing, yüksek ödül, kümeler) | **8** | 4 | 7 | A, USIC yöntemiyle en uyumlu ve kümeli. B'nin çekirdeği swing değil, küme de değil. C uyumlu, ama S2/S3 küme dışı ve işlem sayısı düşük |
| **Toplam / 50** | **37** | **29** | **39** | |

---

## 2. Değer muhasebesi: ortak çerçeve [H]

### 2.1 Engeller

**Model.** C'nin modeli (`abd_C` §1.2) kullanıldı ve `abd_pratik` §2.6 ile tutarlı bulundu. Vergilenebilir TL kazancı ≈ E × kur × [R(1+d) + u·d].
- E: ABD hesabı (USD), R: vergi öncesi USD getirisi, d: yıllık kur artışı, u: yatırımda kalma oranı.
- Kur 50,05, d = %20. Tarife 2026 (doğrulanmadı).
- Elde tutulan USD nakdin kur kazancı vergisiz kabul edildi (`abd_pratik` §2.5, §4.2; mali müşavirle teyit edilmeli).

**TL'de kalmanın USD karşılığı:** h=%31 → %9,2; h=%35 → %12,5; h=%37 → %14,2. Doğrulanmış çapa: %13–15,5, faiz indirimi ya da kur şoku kuyruğunda %6–12 (`v_abd` #34).

| E | USD nakit (IBKR %3,38), vergi sonrası | TL'yi yenmek için gereken R, u=0,3 (h %31 / %37) | Aynısı, u=0,6 |
|---|---|---|---|
| 50 bin $ | %2,9 | %12,7 / %19,5 | %14,5 / %21,4 |
| 250 bin $ | %2,7 | %15,6 / %23,3 | %18,3 / %26,0 |
| 1 mn $ | %2,4 | %17,5 / %25,9 | %20,9 / %29,2 |

**Okuma:**
- Engel, maruziyet arttıkça yükseliyor, çünkü pozisyondaki sermayenin kur farkı vergileniyor (hayalet vergi). Hesap büyüdükçe de yükseliyor, çünkü vergi dilimi artıyor.
- A'nın düz "%20–28"i ancak u ≈ 1'de doğru.
- **USD'den gelen sermaye için engel**, R ≈ T-bill + u × ~%9 (vergi sürüklemesi). u=0,3'te ~%6–7, u=1'de ~%13.
  - A'nın "%8,5–13"ü (u=0,5–1) kendi maruziyetinden (R0–R1'de %0–40) yüksek.
  - C'nin "~%5–8"i doğru.

### 2.2 Planların merkez tahmini, vergi sonrası USD (d=%20)

| Plan, merkez | R | u | 50k | 250k | 1m |
|---|---|---|---|---|---|
| A, 1. yıl (senaryo ağırlıklı ~%2) | %2 | 0,3 | %0,9 | %0,3 | −%0,3 |
| C, 1. yıl (merkez %2–6'nın ortası) | %4 | 0,3 | %2,5 | %1,6 | %1,0 |
| B-Standart, B'nin iddiası | %10 | 0,6 | %5,8 | %3,8 | %2,6 |
| B-Standart, benim gerçekçi tahminim* | %7 | 0,6 | %3,7 | %1,8 | %0,8 |
| B-Agresif | %13 | 0,7 | %7,6 | %5,1 | %3,8 |

\* Kaba ayrıştırma: ileriye dönük R ≈ rf (%4) + ortalama hisse betası (~0,6–0,7) × ileriye dönük hisse primi. Hisse primi için %3–5 varsaydım [Ö]. `v_abd` §4.4 bu primin tartışılmadığını not ediyor; ileri F/K 18,7 ve 10 yıllık getiri %4,84–4,90. B kendi tahminini 2–3 puan tıraşlamış; bence 3–5 puan gerekiyor.

**Okuma:**
- USD'den gelen sermayede B-Standart, USD nakdi **~0–1 puan** geçiyor. B "+1–2" diyor. Yani B'nin en büyük kolu vergi sonrası neredeyse sıfır fazla getiri için −%25/−%45 düşüş taşıyor (`abd_B` §8.2).
- A ve C ilk yıl USD nakit düzeyinde ya da biraz altında. Ama düşüşleri küçük: %5 olasılıklı kötü durum −%8/−12.

### 2.3 Gözden kaçan iki vergi etkisi

1. **Zarar devretmiyor, bu yüzden vergi dışbükey.** Kötü yılda vergi iadesi yok, iyi yılda tam vergi var (`v_capraz` #10, #22). Oynaklık arttıkça beklenen vergi sonrası getiri düşüyor. 250k hesapta simülasyon sonucu: A/C profilinde (σ≈%7) yılda −0,4 puan, B-Standart'ta (σ≈%15) −0,5, B-Agresif'te (σ≈%20) −0,7 [H]. Hiçbir plan bunu hesaba katmamış.
2. **Yİ-ÜFE endekslemesi uzun tutulan lotlarda hayalet vergiyi siliyor.** Kural: elden çıkarma ayı hariç Yİ-ÜFE artışı ≥%10 ise maliyet endekslenir; bu ~6 ay demek (`v_capraz` #10 DOĞRU).
   - Örnek: 12 ay tutulan bir lot, R=%10, d=%20, Yİ-ÜFE +%27,4. Dolar maliyet başına vergi matrahı 16,0 TL'den 2,3 TL'ye iniyor (−%86) [H].
   - Swing kuralları için bu bir şey değiştirmez; kural vergiden önce gelir.
   - Ama iki yerde önemli: aylarca iz süren büyük kazananların kalan lotu ve olası bir pasif beta bacağı.
   - B'nin vergi tablosu bunu yok sayıyor, yani B'nin çekirdeği için vergi aleyhine yanlı. Müşavirle teyit şart.

### 2.4 "Opsiyon değeri" kaba hesabı [H, Ö]

- Kullanıcının USIC tipi bir kenarı olma olasılığı %10–15 (A'nın ağırlığı; taban oranlar: USIC'te %8–17 kârlı, Tayvan'da %13; `v_abd` #8, #14). Kenar varsa Faz 3 kapısının geçilme olasılığı ~0,6–0,7. Sonuç: ~2 yıl sonra ölçeklenebilir bir kenar bulunma olasılığı **~%7–10**.
- Kenar bulunursa: kol servetin ~%30'una çıkar. Merdivenle medyan +%16–36 vergi öncesi (§4.2), engel %16–26. Yani yılda kabaca −%1,5 ile +%4,5 arası (W'nin). Beklenen getiri ≈ 0,08 × ~%3 × 3 yıl ≈ **W'nin +%0,7'si**.
- Maliyet: 1–2 yıl boyunca W'nin %1–2,5'i.
- **Sonuç:** Proje TL'deki temel senaryoya göre W'nin kabaca −%0,5 ile −%2'si eder. Savunması:
  - (i) TL şoku çeşitlendirmesi: 2018–26'da kurun ≥%45 arttığı yıllar 2/9 (`v_capraz` #21).
  - (ii) Sermaye zaten USD'deyse maliyet ~0.

---

## 3. Plan bazında değerlendirme

### 3.1 A: Lider momentumu (USIC tarzı), gün sonu uyarlaması

**Güçlü yanları:**
- Dağılım raporu en iyisi: senaryo ağırlıkları, p10/p90, MDD ve P(>%20)/P(>%28) (`abd_A` §8). Benim MC'm A'nın kanıt sonrası rakamlarıyla tutarlı (§4.2).
- Kademeli USD çevrimi (C2), rejim tavanları ve gap-ayarlı ısı var.
- Değere bağlı öldürme kriterleri: K6 ("rejim açıkken RSP, değilse T-bill" kıyası) ve K7 (vergi sonrası TL'ye karşı TL nakit).
- 50k hesapta veri maliyeti disiplini (%2–2,6 → ~%0,3–0,7).
- 2026'nın kısa vergi yılında küçük kalma kuralı (C5).
- Yılda 90–150 işlem. Bu daha hızlı öğrenme ve daha yüksek opsiyon değeri demek.

**Ölümcül kusur:** Yok.

**Ciddi kusurlar:**
1. **S2 (bilanço gap'i, 2.–5. gün) canlı kol.** Oysa doğrulama tersini söylüyor: büyük hissede PEAD 2006'dan beri yok (`v_abd` #23), sadece-uzun bilanço üst portföyleri VW piyasayı geçmiyor (`abd_test` §6.4). A'nın kendi E[R] aralığı −0,1/+0,3R. Bu kol gölge günlüğe alınmalı.
2. **R0'da bile kolun %50'si USD'ye çevriliyor.** Brüt tavan %0–20 iken boşta bekleyen USD'nin yıllık fırsat maliyeti ~9–12 puan (TL'nin USD karşılığı %12,5–14,2 eksi nakdin vergi sonrası %2,4–2,9).
3. **Nakit için "T-bill ~%4" öneriliyor (C3).** T-bill bir menkul kıymet; anaparadaki kur farkı vergilenebilir (`abd_pratik` §2.5, §4.2). Faiz farkı +0,65 puan, kur farkı vergisi riski ise %20 kurda ~%5–7. Varsayılan USD nakit olmalı.
4. USD'den gelen sermaye engeli (§2.1) ve düz %20–28 TL engeli hesap büyüklüğüne ve kolun maruziyetine göre ayarlanmamış.

### 3.2 B: Rejim çekirdeği + uydu

**Güçlü yanları:**
- Gerçek bir backtest yapılmış (Ken French 1926–2026), varyant sayısı ifşa edilmiş. Rotasyon beklentisi "piyasa ± 4 puan" doğrulamayla birebir tutarlı (`v_dalga` U4, U5, U7; `v_abd` §3.1).
- Hesap büyüklüğüne göre vergi sonrası tablo (`abd_B` §8.3) ve dürüst sonuç: "TL kökenli parada beklenen değer negatif".
- BT-B bulgusu: sistematik kollarda sıkı merdiven CAGR'den 2,3–2,8 puan alıyor, MaxDD'yi düşürmüyor. Bu, merdivenin yalnız kendi takdirle işlenen kola konmasını destekliyor (`abd_profesyonel` §3.3 ile tutarlı).
- Transfer tetiği (10 GHO > 20 GHO) sinyalden önce para yolda olsun diye kurulmuş; çekirdeğin payı o zamana kadar TL'de bekliyor.
- Kaldıracın meşruiyet koşulu açık: trend açık ve oynaklık düşük; 3x ve NDX kaldıracı yok. Pasif beta için TEFAS yabancı hisse fonu notu var (%17,5 nihai stopaj; `abd_pratik` §2.4).

**Ölümcül kusur (bu kullanıcı ve değer merceği için):**
- Çekirdek H'nin %50–70'i ve S&P'ye kapılı, 2x'e kadar kaldıraçlı. Kapı bir kez açıldı mı aylarca, hatta yıllarca açık kalabilir (2023–25 gibi).
- Bu, kaldıraçlı bir al-tut ve kullanıcının "al-tut yok, en fazla birkaç ay" sınırını çiğniyor.
- Değer tarafında: vergi sonrası USD nakde fazla getiri ~0–1 puan (§2.2), buna karşılık düşüş bütçesi −%25/−%45 (`abd_B` §8.2).
- Çekirdek ölünce geriye kalan uydu-R (piyasa ± 4) ve tavanlı lider kolu (risk ≤%0,75, ısı ≤%2, brüt ≤%25) var. Bu yapıyla "yüksek ödül" yapısal olarak erişilemez.

**Ciddi kusurlar:**
1. En kötü durum geniş: H −%30'a kadar plan sürüyor, çekirdek −%45'te ölüyor, 1987 tipi gap'te −%35.
2. Pazartesi'nin tek canlı eylemi XLV'ye MOO emri. Bu emir dört teyitsiz şeye bağlı:
   - ABD ETF erişimi: IBIE'ye bağlanırsa PRIIPs kısıtı olabilir (`hazırlık` §1.2).
   - Midas'ta MOO desteği.
   - IBKR'nin 11–13.11'den önce hazır olması (hazır değil).
   - 12 aylık sıralama verisi: elde yok, YTD vekili kullanılıyor.
3. Merkez tahmini (%10) muhtemelen 3–5 puan iyimser (§2.2).
4. MES ile yurt dışı vadeli kazancının vergi niteliği belirsiz (`v_capraz` §2 #9). B bunu işaretliyor, ama çekirdeğin büyük hesaptaki aracı bu.

### 3.3 C: Önce risk, kanıt minimalizmi

**Güçlü yanları:**
- En iyi vergi modeli: hesap büyüklüğüne ve u'ya bağlı engel, hayalet vergi (R=0'da E'nin %0,9/1,3/1,9'u; yeniden hesapladım, tutuyor).
- Boştaki USD aracı kurumda nakit tutuluyor.
- Döviz tahsis anahtarı işlem kenarından ayrı (`tr_makro_engel` §5.1'e sadık).
- Yüzdesel komisyonun R cinsinden maliyeti ölçülmüş (İş TMI 0,08R), bu yüzden ana platform IBKR.
- Sıkı en kötü durum (−%15'te plan durur) ve t istatistikli faz kapıları.
- "Kaçan sinyaller" sekmesi, beklemenin bedelini ölçmeye yarıyor.

**Ölümcül kusur:** Yok.

**Ciddi kusurlar:**
1. **Faz 3'teki "medyan +%17–30" iki kat iyimser.**
   - Rakam doğrusal aritmetikten geliyor (85 × %0,85 × 0,3) ve atıfı kalibre edilmemiş MC'ye (`abd_profesyonel` §3.3; `v_profesyonel` #11).
   - C'nin kendi −%4/−%7/−%10/−%15 merdivenini ve kümelenmeyi yok sayıyor.
   - Benim MC'mde +0,3R, 85 işlem, %0,75–1 risk: merdivensiz medyan %15–20, C merdiveniyle **%7,5–9** (+nakit ~%2) [H, §4.2].
   - Ayrıca %0,75 riskte −%4 yalnız 5,3R eder. Normal kayıp serileri merdiveni sürekli tetikler.
2. **E'nin tamamı hemen USD'ye çevriliyor (§6.2).** Oysa kendi hesabı boşta bekleyen ~%70'in yılda E'nin %7–8,5'i kadar fırsat maliyeti yarattığını söylüyor (§1.3). KIRMIZI'da brüt tavan %25, SARI'da %50; o kadarı çevrilmeli.
3. **S3'ün "t=3,69" başlığı yanıltıcı.** Bu t değeri sıfıra karşı hesaplanmış ve hisse primini içeriyor. Koşulsuz ortalamaya göre fark ~+1,8 puan (C de yazıyor). n=25, örneklem içi, 2009–26 boğası, iki tanım denenmiş. %50 tıraş doğru; başlık düzeltilmeli. S3'ün katkısı olay başına E'nin +%0,1–0,5'i; asıl işi rejime yeniden giriş sinyali.
4. **S2 (insider küme alımları).** Yayın sonrası kanıtı yok, %3,8'lik küme rakamı teyitsiz (`v_abd` #26). EV yılda ~0 ile +%0,5. Her gün EDGAR taraması gerektiriyor. Değer/zaman oranı en düşük kol; ertelenmeli.
5. **Yavaş öğrenme.** Yılda 40–70 işlemle Faz 3 (100 işlem) 1,5–2,5 yıl sürüyor; opsiyon değeri gecikiyor. A'nın geri çekilme kurulumu bunu hızlandırır.

---

## 4. Beklenen dağılım: dürüst rakamlar

### 4.1 1. yıl (Faz 1, %0,25 risk, ~80 işlem, u≈0,3; nakit +%2,4 dahil) [H]

| Kenar (E[R]) | Medyan | p10 / p90 | MDD medyan / %5 kötü |
|---|---|---|---|
| −0,1R (taban oranlara göre en olası) | −%0,4 | −%4,2 / +%7,9 | −%5,7 / −%8,3 |
| 0 | +%1,1 | −%3,7 / +%10,3 | −%5,5 / −%8,1 |
| +0,15R | +%3,8 | −%2,8 / +%15,3 | −%5,2 / −%7,8 |
| +0,3R | +%6,7 | −%2,0 / +%19,9 | −%5,0 / −%7,5 |
| +0,45R (USIC tipi) | +%9,1 | −%1,2 / +%25,0 | −%4,9 / −%7,4 |

- Ağırlıklı merkez vergi öncesi +%1–4, vergi sonrası ~%0–2,5. Bu, USD nakit düzeyi.
- TL engelini (§2.1) geçme olasılığı **< %5**.
- A'nın (−%3/+%19) ve C'nin (−%8/+%15) aralıkları bununla tutarlı. **Doğru beklenti: ilk yıl ölçüm yılıdır.**

### 4.2 Kanıt sonrası (riski artırılmış kol, yıllık) [H, kaba MC]

Model: isabet %30, kayıpların %10'u gap'li −2R, dalgaların %30'unda küme birlikte bozuluyor, toplam beklenti sabit.

| Kenar, işlem/yıl, risk | Merdivensiz: medyan / p10 / p90 / %5 kötü MDD | A merdiveni: medyan / %5 kötü MDD | C merdiveni: medyan / %5 kötü MDD |
|---|---|---|---|
| 0R, 85, %1 (şans) | −%4,7 / −%30 / +%36 / −%40 | −%4,5 / −%18 | −%4,3 / −%15 |
| +0,15R, 150, %1 | +%15 / −%31 / +%100 / −%49 | +%4 / −%20 | +%3,5 / −%15 |
| +0,3R, 85, %0,75–1 | +%15–20 / −%14…−21 / +%65–96 / −%29…−38 | +%8 / −%15…−17 | +%7,5–9 / −%14…−15 |
| +0,3R, 150, %1 | +%39 / −%19 / +%159 / −%46 | +%17 / −%20 | +%16 / −%15 |
| +0,45R, 150, %1 | +%72 / −%6 / +%232 / −%43 | +%36 / −%19 | +%29 / −%15 |

**Okuma:**
1. "Yüksek ödül" (medyan %40+) yalnız iki koşul birlikteyken geliyor: yılda ≥150 işlem ile ≥+0,3R kenar, **ve** merdivensiz, %5 olasılıklı kötü düşüşü −%45 civarında kabul etmek. Bu, doğrulanmış kazananların fiili profiliyle tutarlı (`v_abd` #37: SR 0,8, vol %35'te medyan MDD −%51).
2. Merdiven kötü kuyruğu ~−%15/−%20'ye çekiyor, ama medyanı yarıya indiriyor (`abd_profesyonel` §3.3 ile aynı yön).
3. Kenar yokken bile %10 olasılıkla +%24–36'lık bir yıl gelebiliyor. Faz kapıları bu yüzden t istatistiğine bağlı olmalı (C'nin yöntemi doğru).
4. Kanıt sonrası bile, C'nin işlem temposunda medyan TL engelinin (%16–26) altında ya da civarında. Engeli rahat geçmek için A'nın işlem sayısı gerekiyor (aşı 5).

---

## 5. Doğrulanmış gerçeklerle çelişkiler

| Taslak | Çelişki | Doğru olan |
|---|---|---|
| A | Bilanço gap'i (S2) canlı, eşit statüde | Büyük hissede PEAD yok (`v_abd` #23); sadece-uzun bilanço üst portföyleri VW'yi geçmiyor (`abd_test` §6.4) |
| A | Nakit için T-bill önerisi | Dövizin kur kazancı vergisiz, menkul kıymetin içindeki vergili (`abd_pratik` §2.5, §4.2; teyit gerekli) |
| A, B | FTD eşiği +%1,25 | `hazırlık` §3: +%1,5. Küçük fark, ama tutarlı olmalı |
| B | Merkez %10, 2010–26 temposunda | `v_abd` §4.4: 2010–26 olağanüstüydü; ileriye dönük hisse primi düşük (ileri F/K 18,7, 10 yıllık %4,84–4,90) |
| B | Çekirdek ve uydu ABD ETF'ine dayanıyor | IBKR kuruluşu (IB LLC / IBIE) doğrulanmadı; IBIE'de PRIIPs kısıtı olabilir (`hazırlık` §1.2; `v_abd` §4 #7) |
| C | "CDS 5 yıl 248" güncel veri gibi yazılmış | `v_capraz` §1: DOĞRULANAMADI |
| C | Kur vadelisinin %32,9'u engel senaryosu olarak kullanılmış ("%0–9 yetiyor") | Bu bir tahmin değil, faiz paritesinin (CIP) sonucu; uzak vadeler likit değil (`v_capraz` #5). C "carry bahsi" diye doğru çerçeveliyor, ama bu satır karar ağırlığı taşımamalı |
| C | Faz 3 medyanı kalibre edilmemiş MC'ye dayanıyor | `v_profesyonel` #11: rakamlar yalnız göreli fark olarak okunmalı |
| C | S3, Nagel'in kısa vadeli reversal bulgusundan endeks zamanlamasına geçiyor | Nagel'in bulgusu hisseler arası (kesitsel) bir etki; koşulsuz kısa vadeli reversal 2010'dan beri ~0 (`abd_test` §7). S3 kendi örneklem içi testine dayanıyor |
| Üçü de | — | NVDA tarihi 17.11 (AMC, NVIDIA IR; `hazırlık` §2.1); görev notundaki "~19.11" aykırı. Üçü de doğru tarihi kullanıp teyit istiyor. 2026 tarifesi ve Midas emir tipleri teyitsiz; üçü de işaretliyor |

---

## 6. Aşılanacak en iyi fikirler (değer sırasıyla)

1. **Hesap büyüklüğüne ve u'ya bağlı engel ve hayalet vergi tablosu** (C §1.2). A'nın düz %20–28'inin ve B'nin u=0,6'sının yerine, planın gerçek maruziyetiyle kullanılmalı. Her ay sonu raporuna "vergi sonrası USD, USD nakit ve TL USD karşılığı" satırı eklenmeli (B §7.2 biçimi).
2. **Boştaki USD aracı kurumda nakit tutulur; T-bill, SGOV ve BIL kullanılmaz** (C §6.2, B §6.5; `abd_pratik` §2.5, §4.2). Müşavirle teyit edilmeli. Kazanç: %20 kurda T-bill pozisyonunun ~%5–7'si kadar kur farkı vergisinden kaçınılırken kaybedilen faiz yalnız 0,65 puan.
3. **Kademeli çevrim** (B §1.3 + A C2). Yalnız rejimin brüt tavanı + %10 tampon USD'ye çevrilir: C'de KIRMIZI'da E'nin %25'i, SARI'da %50'si. Kalanı banka mevduatında ya da DİBS'te bekler; stresli PPF'de değil (`v_profesyonel` eksik #2). Rejim yükselince transfer yapılır. Kazanç [H]: KIRMIZI'da E'nin %75'i TL'de kalırsa, boşta bekleyen USD'nin yıllık fırsat maliyeti E'nin kabaca %7'si kadar azalır (bekleme süresine orantılı).
4. **Döviz tahsis anahtarı, işlem kenarından bağımsız** (C §1.3; `tr_makro_engel` §5.1). Beş tetikten ikisi oluşursa USD nakit payı servetin %25–35'ine çıkar; işlem riski aynı kalır. Servetin %75–90'ı TL'de olduğu için toplam değer ve risk üzerinde en etkili kural bu. CDS'yi doğrulanmış bir kaynakla güncelleyin.
5. **A'nın geri çekilme kurulumu C'nin S1'ine eklenir** (yükselen 10/20 GHO'ya geri çekilme, A §2.3; Luk/Kell). Ayrı etiketlenir. Amaç işlem sayısını 40–70'ten ~90–120'ye çıkarıp faz kapılarına daha hızlı ulaşmak. Bilanço gap'i (A S2) ise **gölgede** kalır.
6. **A'nın dağılım tablosu ve değere bağlı öldürme kriterleri C'ye eklenir.** Senaryo × p10/p90 × MDD × P(>engel) tablosu (A §8). K6: 12 ayda aynı maruziyetle "rejim açıkken RSP, değilse T-bill"i geçememek. K7: vergi sonrası TL getirisinin TL nakdin altında kalması.
7. **Merdiven R cinsinden ve yalnız takdirli kolda** (B §5.3 BT-B; `abd_profesyonel` §3.3). C'nin −%4/−%7 eşikleri Faz 2–3'te R'ye çevrilmeli: örneğin −12R'de ×0,5, −20R'de daralt, −%15'te dur. Faz 3 beklentisi bu merdivenle yeniden hesaplanmalı (§4.2: +0,3R'de merkez ~%8–16).
8. **Kısa vergi yılı 2026** (A C5, C §6.4). 9.11–31.12 arasında Faz 1 boyutunda kalınır, çünkü zarar 2027'ye devretmiyor. Aralık kontrolünde yalnız vergi için çıkış yapılmaz.
9. **Komisyon ve veri maliyeti R cinsinden** (C §5.3, A §1.3, B §6.4). Yüzdesel komisyonlu kurumlar 0,08–0,2R yiyor, bu yüzden IBKR zorunlu. Midas yalnız stop ve GTC emirleri 1 adetle teyit edilirse kullanılır. 50k hesapta veri seti ≤%0,7.
10. **Pasif beta için vergi kaldıraçları (araştırma maddesi, kural değil)** (B §6.5; `abd_pratik` §2.4; `v_capraz` #10). Kullanıcı bir gün endeks betası isterse doğrudan kaldıraçlı trendden önce iki seçenek değerlendirilmeli:
    - (a) TEFAS yabancı hisse fonu, %17,5 nihai stopaj.
    - (b) Lotları ≥6 ay tutup Yİ-ÜFE endekslemesinden yararlanmak. Örnekte matrah −%86 düşüyor (§2.3).

    Müşavir teyidi şart.

---

## 7. Kazanan ve kazananın düzeltilmesi gerekenler

**Kazanan: C.** Gerekçe, değer merceğiyle:
- (i) İlk yılın beklenen kaybını en küçük ve en sınırlı tutuyor. Toplam servete en kötü kayıp ~−%1,5/−2,3.
- (ii) Türkiye vergisini en doğru modelliyor: hesap büyüklüğü, u, hayalet vergi, nakit-T-bill ayrımı.
- (iii) Yüksek ödülü kanıt kapısına bağlıyor ve kapıyı t istatistiğiyle ölçüyor.
- (iv) Servetin büyük kısmının durduğu TL tarafını yöneten tek kural onda.

A çok yakın ikinci. Profile uyumu ve işlem temposu daha iyi; birleşik planın S1 iskeleti A'dan alınmalı. B'nin çekirdeği bu kullanıcı için reddedilmeli. B'nin vergi tablosu, transfer tetiği ve merdiven bulgusu ise alınmalı.

**C'de zorunlu düzeltmeler:**
1. §8.2'deki Faz 3 rakamı (+%17–30) merdiven ve kümelenmeyle yeniden hesaplanmalı. Dürüst merkez yaklaşık +%8–16, ancak +0,45R ve ≥150 işlemde %30+.
2. §6.2: E'nin tamamı yerine rejimin brüt tavanı + %10 çevrilir (aşı 3).
3. §2.3: S3'ün başlık t değeri yerine koşulsuz ortalamaya göre fark (+1,8 puan, n=25, örneklem içi) yazılmalı.
4. S2 ertelenir. Geri çekilme kurulumu eklenir (aşı 5).
5. Aylık rapora vergi sonrası satırı ve K6/K7 eklenir (aşı 1, 6).
6. CDS ve diğer teyitsiz makro girdiler işaretlenir.

**Kullanıcıya tek cümlelik dürüst beklenti:**
- İlk yıl vergi sonrası USD'de ~%0–2,5 (USD nakit düzeyi), düşüş −%5/−%8.
- TL'de kalmaya göre servete yıllık ~%1–2,5 maliyet. Bunun karşılığı ~%7–10 olasılıkla 2. yıldan itibaren ölçeklenebilir bir kenar.
- Gerçek "yüksek ödül" (medyan %40+) ancak kanıtlanmış ≥+0,3R kenar, ≥150 işlem/yıl ve −%45'e varan kötü kuyruğu kabul etmekle gelir.

---

## 8. Hesap betikleri (scratchpad, repoya yazılmadı)

- Engel ve vergi sonrası tablo, vergi dışbükeyliği, endeksleme örneği: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/hakem_deger/ev.py`
- Kanıt sonrası ve 1. yıl Monte Carlo (kümelenme, merdivenler; beklenti kümelenmeye göre kalibre): `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/hakem_deger/mc3.py`
  - `mc.py` hatalı ilk sürüm: kümelenme beklentiyi düşürüyordu.
  - `mc2.py` kalibre edildi, ama merdiven kalıcı durduruyordu.
  - Sonuçlar `mc3.py`'den.
- MC sınırları: isabet sabit %30, kazançlar 0,5 + üstel dağılım (R), kayıpların %10'u −2R gap. Rejim kalıcılığı yok. Merdivenin ara duraklaması "×0,25 ile devam" diye yaklaşıklandı. Rakamlar yalnız göreli büyüklük olarak okunmalı.
