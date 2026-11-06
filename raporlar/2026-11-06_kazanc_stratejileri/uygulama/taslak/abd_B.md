# ABD swing planı B: "Rejim çekirdeği + uydu" (9.11.2026'dan itibaren)

**Hazırlanma:** Cuma 06.11.2026, ~14:00 TSİ. Son kapanış 05.11.2026. Bugünkü NFP (16:30 TSİ) bu planın rejim tablosuna henüz girmedi; §3.3 tablosu Cuma kapanışından sonra (Cumartesi 00:15 TSİ) yeniden hesaplanmalı.
**Kullanıcı:** TR mukimi, deneyimli BIST/VİOP trader'ı. Swing ufku (günler–haftalar, en fazla birkaç ay). Gün içi ekran işlemi yok. Al-tut yok. "Stratejik küme" tarzı.
**Kapsam:** Bağımsız ve tam bir plan. Kol yapısı: kuralı sabit bir endeks çekirdeği (yalnız rejim açıkken ve oynaklık düşükken kaldıraçlı, kapalıyken nakit) ve iki uydu (12 aylık sektör/tema rotasyonu + seçici liderler).
**Yatırım tavsiyesi değildir.** Vergi satırları mevzuat özetidir; mali müşavirle teyit edilmeli.

**Kaynak kısaltmaları** (hepsi `raporlar/2026-11-06_kazanc_stratejileri/` altında). Doğrulama dosyaları raporlarla çeliştiğinde doğrulama esas alındı.

| Kısa | Dosya |
|---|---|
| K | `ajanlar/abd_kim_kazaniyor.md` |
| S | `ajanlar/abd_swing_kenarlar.md` |
| T | `ajanlar/abd_test.md` |
| P | `ajanlar/abd_pratik.md` |
| PR | `ajanlar/abd_profesyonel.md` |
| D | `ajanlar/dalga_abd.md` |
| Ş | `ajanlar/seytan_taban_oranlar.md` |
| M | `ajanlar/tr_makro_engel.md` |
| VA / VC / VD / VP | `dogrulama/v_abd.md` / `v_capraz.md` / `v_dalga.md` / `v_profesyonel.md` |
| H | `uygulama/abd_hafta_hazirlik.md` |
| BT-B | Bu plan için yapılan bağımsız testler: Ken French günlük piyasa ve aylık 49 sektör verisi, 1926–09/2026 (yöntem Ek A'da) |

---

## 0. Özet: 12 madde

1. **Bu plan TL'deki parayı yenmeyi vaat etmiyor.** TL kökenli sermayede gereken vergi öncesi USD getirisi hesap büyüklüğüne göre **~%16–30** (§1.1). Planın sistematik kısmının tıraşlanmış beklentisi **%8–12** (B-Standart) ile **%11–15** (B-Agresif). Bu yüzden ABD'ye ayrılan pay sınırlı tutuluyor. Önerilen başlangıç: likit servetin **%15–25**'i, kademeli.
2. **Hesap (H) üç kola bölünüyor.**
   - **Çekirdek:** H'nin %50'si.
   - **Uydu-R** (12 aylık sektör/tema rotasyonu, ETF): H'nin %30'u.
   - **Uydu-L** (seçici liderler, hisse): brüt en fazla %25, ısı en fazla %2.
   - Boştaki para USD nakitte durur. Gerekçe: dövizin kur kazancı vergisiz, menkul kıymetin içindeki kur kazancı vergili (P §2.5, §4.2).
3. **Çekirdek kuralı (BT-B'de test edildi).**
   - S&P 500 kapanışı 200 GHO × 1,01'in üstünde **ve** 10 GHO > 20 GHO ise kapı açılır. Kapanış 200 GHO × 0,99'un altına inince kapanır.
   - Kapı açıkken kaldıraç **L = min(2; %25 / σ̂)**, burada σ̂ = max(RV20, RV60).
   - 1928–2026: CAGR %13,8, MaxDD −%44. 2000–2026: %10,5, −%25. 2010–2026: %13,8, −%24.
   - Karşılaştırma: 1x al-tut %10,0 / −%84; sabit 2x + 200 GHO %15,4 / −%67.
4. **Kaldıraç yalnız şu koşulda meşru:** trend açık **ve** gerçekleşen oynaklık düşük. 2x'e ancak σ̂ ≤ %12,5 iken çıkılır; 1950 sonrası günlerin ~%27'si böyle.
   - 3x yok, Nasdaq-100 kaldıracı yok. 3x NDX + 200 GHO, 2000–02'de −%89 verdi (T §3.5).
   - Kaldıraç tercihen MES micro vadeliyle yapılır. Küçük hesapta SPY+SSO kullanılır.
5. **Uydu-R kuralı.**
   - Ay sonunda 12 aylık getiriye göre ilk 3 **farklı** küme, küme başına 1 ETF. Mutlak filtre: 12 aylık getiri > T-bill.
   - Haftalık zamanlama kuralı var. Stop, girişten beri en yüksek kapanışın %12 altında (GTC).
   - Kanıt orta-zayıf. ETF'e yakın evrende 2000+ piyasanın +2,7 puan üstü; 2015+ belirsiz, %90 aralık [−7,2; +15,8] (VD U4–U5). Rotasyon bir alfa motoru sayılmamalı; işlevi kırık kümelerden uzak tutmak.
6. **Uydu-L kuralı.** Kullamägi/Minervini/Luk iskeleti gün içi ekransız çalışacak şekilde uyarlandı:
   - Seans öncesi konan buy-stop-limit giriş, GTC yapısal stop.
   - +2R'de 1/3 kâr alma, kalan pozisyon için kapanış bazlı 10/20 GHO trail.
   - Risk ilk 50 işlemde H'nin **%0,25**'i.
   - Bu kolun kenarı kanıtlanmadı. USIC'te katılımcıların yalnız %8–17'si kârlı (K §4.1).
7. **Rejim bugün (5.11): SARI.**
   - S&P 200 GHO'nun yalnız %0,42 üstünde (bant içinde). 10 GHO 20 GHO'nun altında. VIX 28,2, VIX/VIX3M 1,10. NDX 200 GHO'nun %4,8 altında.
   - Çekirdek **sıfırdan başladığı için kapalı (nakit)**. Uydu-R dilimleri %7. Uydu-L FTD'ye kadar işlem yapmıyor.
8. **Pazartesi 9.11'de çekirdek ve lider işlemi yok.** Hesap fonlandıysa yalnız Uydu-R ilk kurulumu yapılır: MOO emirleri 17:25 TSİ'ye kadar, zamanlama şartını geçen ETF'ler.
   - Salı (CPI 16:30): 16:45'ten önce yeni emir yok.
   - FTD en erken Çarşamba 11.11.
   - Çekirdeğin açılması için 10 > 20 gerekiyor. Bunun için S&P'nin kabaca 7 seans ≥ ~7.735'te kapanması lazım; yani bu hafta çekirdek büyük olasılıkla kapalı kalır.
9. **Risk limitleri.**
   - İşlem başı %0,25 (sonra %0,5, tavan %0,75).
   - Küme ısısı ≤ %1,5. Toplam ısı (uydu + lider) SARI/KIRMIZI'da ≤ %3, YEŞİL'de ≤ %5, YEŞİL+'da ≤ %6.
   - Aylık devre kesici: zarar + açık risk ≥ %6 (ilk 6 ay %4).
   - Merdiven: −%5 / −%10 / −%15'te lider kolu kısılır. Sistematik kollar için yalnız felaket frenleri: −%20 ve −%25. Hesap −%30'da durur.
10. **Portföy düzeyinde sıkı merdiven bu sistemde işe yaramıyor (BT-B).** −%10'da ×0,5, −%15'te ×0,25 kuralı CAGR'den 2,3–2,8 puan aldı, MaxDD'yi ise neredeyse hiç düşürmedi. Trend kapısı bu korumayı zaten sağlıyor. Merdiven bu yüzden lider koluna uygulanıyor (PR §3.3 ile tutarlı).
11. **Ölçme protokolü.**
    - R-defteri tutulur. 50 işlemden önce lider riski büyütülmez.
    - 100 işlemde E[R]'nin %90 güven aralığının üst sınırı < 0 ise lider kolu kapatılır.
    - Sermaye artışı en erken 12 ay sonra ve yalnız ölçülmüş performansla.
12. **Beklenti (vergi öncesi USD, tıraşlı).**

    | Sürüm | Medyan CAGR | Kötü 12 ay (P10) | MaxDD |
    |---|---|---|---|
    | B-Standart | %8–12 | −%4…−%8 | −%20…−%35 |
    | B-Agresif | %11–15 | −%7…−%12 | −%30…−%45 |

    - Lider kolu ilk yıl H'ye −%4 ile +%6 arası ekler.
    - Vergi sonrası (%35 dilim, kur +%20) B-Standart ≈ **USD'de %1–6**. USD nakdin vergi sonrası ~%2–3'ü ile karşılaştırılmalı.

---

## 1. Sermaye ve engel kararı

### 1.1 Engel: rakamlar

| Ölçü | Değer | Kaynak |
|---|---|---|
| TL'de kalmanın net nominal getirisi (birey, 12 ay) | Faiz sabit kalırsa ~%36–38 (mevduat roll). Anket patikasında ~%31–33 | VC #4 |
| Aynısının ileriye dönük USD karşılığı | **~%13–15,5**. Faiz indirimi ya da kur hızlanmasında %6–12 | VA #34 |
| TL carry'nin geçmişteki USD sonucu | 2010–2026: **−%7,2/yıl, MaxDD −%85** | T §2, VA #34 |
| ABD kazancının TR vergisi | TL bazında, kur farkı dahil, %15–40 artan oranlı. Zarar yalnız aynı yıl içinde mahsup edilir. Yİ-ÜFE endekslemesi yalnız artış ≥ %10 ise (~6 ay) | P §2.1, VC #10 |
| TL nakdi yenmek için gereken vergi öncesi USD getirisi | **~%20–28** (h=%35, d=%20, t=%35; erteleme ve kısmi yatırımda kalma ile ~%20) | P §2.6, VC #22 |
| Aynı hesap, hesap büyüklüğüne göre (bu plan; 2026 tarifesi doğrulanamadı, VC #11) | Vergi sonrası USD %9 / %13 / %15,5 hedefleri için: **50k $: %16 / %22 / %25**; **250k $: %18 / %24 / %27**; **1m $: %20 / %26 / %30** | BT-B §8.3 |
| Sermaye zaten USD'deyse engel | T-bill ~%4,0–4,1 (DTB3 %4,03). IBKR boş nakit %3,38. Vergi sonrası ~%2–3 USD | VC #13, P §1.2 |
| USD maruziyetinin "sigorta" değeri | Ortodoks rejimde pahalı. d ≥ %45 şok sıklığı 2018–26'da 2/9 ≈ %22; başabaş olasılığı %39 | VC #21 |

### 1.2 Planın beklentisi ve engelle karşılaştırma (ayrıntı §8)

- **B-Standart sistematik kısım (BT-B):**
  - 1930–2026: CAGR %13,1, MaxDD −%27,9.
  - 2000–2026: %10,7, −%16,4.
  - 5 yıllık kayan pencerede (1950+) medyan %13,4, P10 %7,0. 5 yıllık CAGR'nin %20'yi aşma olasılığı %11.
- **Tıraş:** Bu oturumda ~30 varyant denendi (Ek A). Değerlemeler yüksek (ileri F/K 18,7; VC #14). Bu yüzden ileriye dönük beklenti 2–3 puan düşük alınmalı: **%8–12**.
- **Sonuç:** TL kökenli parada beklenen değer engelin **8–18 puan altında**. Plan ancak üç durumda engeli geçer:
  - (i) güçlü trend ve düşük oynaklıklı bir yıl (çekirdek 2021'de +%37, 2024'te +%36; BT-B),
  - (ii) TL şoku,
  - (iii) lider kolunun sağ kuyruğu (kanıtsız).

### 1.3 Karar kuralı

**A. Sermaye TL kökenliyse:**
1. **Hedef H** = likit servetin (W) **%15–25**'i, varsayılan %20. Daha fazlasını "belki %20+ yapar" gerekçesiyle taşımak kanıtla desteklenmiyor. BT-B'de B-Standart'ın 12 aylık getirisinin %28'i aşma olasılığı 2000 sonrası %9.
2. **Şimdi taşınacak kısım: H'nin %40'ı.** Uydu-R (SARI'da 3 × %7 = %21) + lider pilotları + tampon.
3. **Çekirdek sermayesi (H'nin %50'si) şimdilik TL'de bekler.** PPF veya kısa vadeli mevduatta, 1–2 gün içinde çekilebilir şekilde.
   - Çekirdek kapalıyken bu paranın USD nakitte durmasının fırsat maliyeti yılda ~6–12 puan: TL'nin USD karşılığı %9–15,5, IBKR nakdi %3,4.
   - **Transfer tetiği:** S&P'de 10 GHO > 20 GHO kapanışı. Giriş için bundan başka "kapanış > 200 GHO × 1,01" de gerekiyor. Böylece SWIFT'in 1–2 günü, giriş sinyalinden önce tamamlanmış olur.
   - Tetikten sonra 15 işlem günü içinde giriş gelmezse para TL'ye geri dönebilir. Bu bir tercih; kur makası nedeniyle gidip gelmemek de makul.
4. **Ölçek büyütme** (H/W payını +%10 artırma) yalnız §7.3'teki kapılar geçilirse ve en erken 12 ay sonra.

**B. Sermaye zaten USD'deyse** (ya da USD'de tutulacaksa): H'nin tamamı ABD hesabına geçer, boştaki kısım USD nakitte bekler. Engel nakdin vergi sonrası ~%2–3'ü. B-Standart'ın vergi sonrası beklentisi bunun yaklaşık 1–4 puan üstünde (§8.3).

**Örnek: likit servet 1,25m $ karşılığı TL, hedef H = 250k $ (%20).**

| Adım | Şimdi | Transfer tetiği gelince |
|---|---|---|
| ABD'ye giden | 100k $ (H'nin %40'ı) | +125k $ (çekirdek) |
| TL'de kalan | 1,15m $ karşılığı | 1,025m $ karşılığı |

Kalan ~25k $'lık tampon, YEŞİL rejimde uydu dilimleri %10'a büyüdüğünde eklenir.

---

## 2. Kollar: giriş, çıkış, stop, boyut, piramit, emir tipi

### 2.0 Tanımlar

- **H:** ABD hesabının günlük piyasa değeri, USD.
- **SPX:** S&P 500 (TradingView `SP:SPX`). GHO = basit hareketli ortalama, kapanış bazlı.
- **σ̂:** max(RV20, RV60). RV, SPX günlük log getirilerinin standart sapması × √252.
- **Isı:** Stoplu pozisyonların stopa kadar toplam riski. Gap-ayarlı tanım §5.2'de.
- **Karar zamanı:** Her ABD kapanışından sonra (00:15–01:00 TSİ ya da ertesi sabah 07:30–09:00). **Emir zamanı:** 12:00–17:25 TSİ (seans öncesi). Gün içi ekran yok. Gün içinde yalnız önceden konmuş emirler çalışır.

### 2.1 Çekirdek (H'nin %50'si; B-Agresif'te %70)

**Kural** (BT-B'de "N25" adıyla test edildi):

1. **Kapı açılışı:** SPX kapanışı > 200 GHO × 1,01 **ve** 10 GHO > 20 GHO, aynı kapanışta.
2. **Kapı kapanışı:** SPX kapanışı < 200 GHO × 0,99. Ara bölgede önceki durum korunur (histerezis).
3. **Hedef kaldıraç:**
   - Kapı açıkken L* = min(2,0; 0,25 / σ̂).
   - Kapı kapalıyken L* = 0; para USD nakitte.
   - B-Agresif'te formül 0,30 / σ̂ (BT-B "N30").
4. **Ayar eşiği:** Fiili L, |L* − L| ≥ 0,25 olduğunda ya da L* = 0 olduğunda güncellenir. BT-B'ye göre yılda ~8–11 ayarlama.
5. **Sıfırdan başlangıç:** Sistem 9.11'de **kapalı** başlar. İlk giriş, 1. maddedeki açılış sinyalinin yeniden oluşmasını bekler.
   - Bu kural sinyali bant içindeyken yakalamamak için konuldu. Geçmişe dönük çalıştırılan tarih serisine göre bugün kapı açık olurdu ve L ≈ 1,24 hedeflenirdi.
   - Başlangıç kuralının maliyeti ayrıca test edilmedi. Sinyale göre en fazla ~%0,6 + 10>20 gecikmesi kadar geç giriş demek.
6. **Ek tavanlar** [Ö, test edilmedi; operasyonel güvenlik]:
   - İlk girişten sonraki ilk 20 işlem günü L ≤ 1,0 (uygulama hatası riski).
   - H zirveden −%10 → L ≤ 1,0. −%20 → L ≤ 0,5. −%25 → L ≤ 0,5 ve diğer kollar yarıya iner (§5.3).
7. **Uygulama: L'nin araca çevrilmesi**

   | Durum | Araç | Nasıl |
   |---|---|---|
   | Çekirdek sermayesi C ≥ ~75k $ (IBKR) | **MES** (micro E-mini S&P, çarpan 5 $ × endeks [bellek; CME'den teyit]) | Kontrat = yuvarla(L × C / (5 × SPX)). 7.354'te 1 MES ≈ 36,8k $ nominal. Teminat dışındaki para USD nakitte kalır |
   | C < 75k $ ya da Midas | **SPY + SSO** (2x S&P ETF) [SSO'nun Midas'ta varlığını teyit edin] | L ≤ 1: SPY = L × C. 1 < L ≤ 2: SSO = (L − 1) × C, SPY = (2 − L) × C. Örnek: L = 1,5 → %50 SPY + %50 SSO |
   | Marjinle SPY | Kullanılmaz | IBKR marj faizi %5,38 (BM + 1,5); TR'de gider yazılamaz (P §1.2, §2.1) |
   | 3x ürünler (UPRO, TQQQ) ve NDX kaldıracı | **Yasak** | 3x NDX + 200 GHO 2000–02'de −%89, tam dönem MaxDD −%97 (T §3.5, VA §2.1) |

8. **Emir tipleri ve saat:**
   - Karar t kapanışında verilir.
   - ETF'te t+1 günü **MOO** (Market-on-Open, 17:25 TSİ'ye kadar girilir).
   - MES'te 17:30–17:45 TSİ arasında limitli emir: SPX vadelinin son fiyatı ± %0,1.
   - Backtest lag1 kullandı: t kapanışındaki sinyal t+1 kapanışında uygulanıyor. Açılışta uygulamak bundan daha erken, yani test muhafazakâr.
   - Çekirdekte stop emri yok. Çıkış yalnız kapanış kuralıyla olur.

**Neden S&P, neden NDX değil?**
- 2026'da AI donanım/yarı iletken/güç tek bir risk kümesi (Chips–ElcEq korelasyonu 0,72; PR §3.2).
- Hardware sektöründe canlı GSY (Greenwood–Shleifer–You) "balon" bayrağı var (D §0.7).
- NDX'in 2010 sonrası üstünlüğü büyük ölçüde rejim şansı. Aynı kural 2000–09'da yılda −%19,8 kaybettirdi (S §8.1).

**Kanıt ve dürüst beklenti** (BT-B; vergi öncesi USD; lag1; finansman rf + %0,5; değişim başına 5 bp):

| Varyant | 1928–2026 CAGR / MaxDD | 2000–2026 | 2010–2026 | Kriz pencereleri (dönem getirisi / pencere içi MaxDD) |
|---|---|---|---|---|
| 1x al-tut | %10,0 / −%84 | %8,5 / −%55 | %14,2 / −%34 | 2000–02 −37/−49; 2008 −45/−55; 2020 −14/−34 |
| 1x 200 GHO, bant %1 | %10,1 / −%39 | %7,6 / −%25 | %10,1 / −%21 | 1987 −25/−29; 2020 −20/−21 |
| 2x 200 GHO, bant %1 | %15,4 / −%67 | %11,5 / −%51 | %17,1 / −%40 | 1987 −47/−53; 2000–02 −41/−51 |
| **N25 (çekirdek, B-Standart)** | **%13,8 / −%44** | **%10,5 / −%25** | **%13,8 / −%24** | 1929–32 −33/−36; **1987 −35/−42**; 2000–02 −15/−24; 2008 −9/−14; 2020 −20/−21; 2022 −14/−16 |
| N30 (B-Agresif) | %14,5 / −%46* (1930+) | %11,6 / −%24* | %15,4 / −%22* | – |
| Sabit 2x, aynı kapı (N2) | %16,0 / −%63 | %13,4 / −%39 | %18,6 / −%32 | 1987 −47/−53 |

\* Aylık toplulaştırılmış seri; günlük MaxDD birkaç puan daha kötüdür.

- **N25 yıllık getirileri:** 2018 −0,3; 2019 +23,7; 2020 +13,6; 2021 +37,4; 2022 −13,6; 2023 +7,7; 2024 +36,0; 2025 +9,9; 2026 (Eylül'e kadar) +4,4.
- **12 aylık kayan getiri (2000+):** P10 −%9,4, medyan %9,7, P90 %37,2. Kayıp yılı olasılığı ~%22–28.
- **Duyarlılık:** Finansman rf + %1,5 olursa CAGR −0,5 ile −0,7 puan. Gecikme 0 olursa +0,7 puan.
- **Belirsizlik:**
  - Kapı kuralı literatürden önceden biliniyor. Bant, eşik ve vol hedefi bu oturumda 20 civarı varyant arasından seçildi. Seçim yanlılığı için −1/−2 puan tıraş uygulayın.
  - 1987 tipi tek günlük çöküşte kapı geç kalır. N25 o pencerede −%35 kaybetti.
  - Filtre 2010 sonrasında getiriyi azalttı: kaldıraçlı al-tut 2x %23,9 iken kapılı sürüm daha düşük (T §0.1). Yani bu kural getiri motoru değil, sigorta.

### 2.2 Kaldıraç ne zaman meşru? (çekirdeğin kalbi)

| Koşul | Eşik | Gerekçe |
|---|---|---|
| Trend kapısı açık | §2.1 madde 1–2 | 200 GHO kuralı uzun dönemde kaldıraçlı al-tutu yıkımdan kurtardı: piyasa 3x %10,6/−%100 → %20,8/−%78 (T §0.1, §3.1) |
| Oynaklık düşük | L = 2 ancak σ̂ ≤ %12,5 iken. σ̂ = %16,7'de 1,5; %25'te 1,0 | Vol yönetimi getiri motoru değil, kuyruk kesici (S §8.2; PR §3.4: Moreira–Muir, Cederburg vd.). BT-B'de benzer oynaklıktaki (~%18) "kapı + trend koşullu 2x/1x" kuralına göre MaxDD daha iyi: 1928+ −%45'e karşı −%60, 2000+ −%30'a karşı −%37. CAGR benzer: 13,8'e karşı 13,0 |
| Hesap drawdown'da değil | H zirveden > −%10 | §5.3 |
| Araç uygun | MES ya da SSO. 3x yok, tekil hisse/tema kaldıracı yok | T §3.5; D §6.2 (SOXL'den kaçının) |
| Kısa vade uyumu | Giriş için 10 GHO > 20 GHO (yalnız açılışta aranır) | BT-B: N, M'ye göre 2000+ CAGR 10,5 vs 9,9, MaxDD −25 vs −30. Tek ek test; zayıf kanıt |

**Kaldıraç meşru değil:**
- VIX ≥ 22 ya da VIX/VIX3M ≥ 1 iken. Bu koşulda σ̂ zaten yüksek olduğu için formül de kaldıracı 1'in altına iter.
- Uydu kollarında.
- Opsiyon alımıyla. Opsiyon alımı ortalamada kaybettiriyor: straddle haftada ~−%3, piyango call'lar haftada −%35 (PR §0.5).

### 2.3 Uydu-R: 12 aylık sektör/tema rotasyonu (H'nin %30'u, 3 dilim)

**Evren** (yalnız hisse sektör/endüstri ETF'leri, ortalama günlük işlem hacmi ≥ 20 m $): XLB, XLC, XLE, XLF, XLI, XLK, XLP, XLRE, XLU, XLV, XLY, SMH, IGV, XBI, IBB, IHI, IHF, PPH, ITA, XAR, KRE, KBE, IAI, XOP, OIH, XHB, ITB, XRT, GDX, TAN, URA (H §5c listesinden; GLD, SLV, IBIT ve TLT hisse olmadığı için çıkarıldı).

**Kurallar:**

1. **Sıralama:** Ayın son işlem günü kapanışıyla 12 aylık toplam getiri, son ay atlanmadan (TradingView "Perf % 1Y").
   - D §4.2: L12 atlamasız (s0) 1930+ %16,7, atlamalı (s1) %14,0. k = 3–5 en sağlam bölge.
2. **Mutlak filtre:** 12 aylık getiri > 12 aylık T-bill (~%4). Geçmeyen dilim nakde gider.
   - D §4.2: C_abs, 1930+ %17,0 / MaxDD −%51; filtresiz −%66.
   - Piyasa filtresi kullanılmaz: 2015+ getiriyi %3,4'e düşürüyor.
3. **Küme başına 1 ETF, ilk 3 farklı küme** (küme haritası §4.2).
   - D §7.1: "aynı kümeden 3 hisse = 1 büyük pozisyon".
   - PR §3.2: ρ = 0,69'da 5 pozisyon yalnız 1,33 bağımsız bahis ediyor.
   - Küme içinde en yüksek 12 aylık getirili ETF seçilir. Getiri farkı < 5 puansa en geniş ve en likit olan (örneğin IHF yerine XLV).
4. **Giriş zamanlaması (haftalık)** [Ö; D §7.2 "seçim aylık, zamanlama haftalık", H §5c ek koşul]:
   - Seçilen ETF'in **Cuma kapanışı 50 GHO'nun (≈10 haftalık) üstündeyse** Pazartesi MOO ile girilir.
   - ETF 52 hafta zirvesinin ≥ %20 altındaysa ya da kümede GSY bayrağı varsa (24 ayda ham ve piyasaya göre ≥ +%100): ek olarak ETF/SPY RS çizgisi 52 haftalık zirvede olmalı (D §7.4, AI kümesi için).
   - Şart sağlanmayan dilim **nakitte bekler**. Yerine alt sıradaki konmaz. Bu "zamanlama" yorumu; ikame sürümü test edilmedi.
5. **Dikey sıçrama yasağı:** ETF son 3 ayda SPY'yi ≥ %40 geçtiyse yeni giriş yok. Konsolidasyondan sonra yeni RS zirvesi beklenir.
   - D §4.4: böyle bir sıçramadan sonraki 1–3 ayda göreli getiri medyanı −%4 ile −%6.
6. **Çıkış:**
   - (a) Ay sonu sıralamasında ilk 3 küme dışına düşerse: ertesi gün MOO.
   - (b) **GTC stop:** girişten beri en yüksek kapanışın %12 altı, GSY bayrağında %10. Her Cuma gece güncellenir (D §7.3: %12–15; GSY bayrağı sol kuyruğu −%69'dan −%22'ye çekti).
   - (c) Mutlak filtre bozulursa: ertesi gün MOO.
7. **Boyut:**
   - Dilim YEŞİL ve YEŞİL+'da H'nin %10'u; SARI ve KIRMIZI'da %7'si.
   - Dilim ısısı ≤ dilim × %12. Örnek: %7 × %12 = %0,84; 3 dilimde %2,5.
   - Piramit yok, dilimler sabit.
8. **Takvim:**
   - Ay sonu kararı ayın son işlem günü kapanışından sonra; emir ilk işlem günü MOO.
   - Kasım 2026: kapanış **30.11 Pazartesi**, emir **1.12 Salı**.

**Dürüst beklenti:**

| Seri | 1930+ | 2000+ | 2010+ | 2015+ |
|---|---|---|---|---|
| C_abs (FF49, BT-B; D ile birebir) | %17,0 / −51 | %14,6 / −47 | %15,6 / −27 | %15,5 / −23 |
| C_abs, ≥10 firmalı sektör-aylar (ETF'e daha yakın) | %15,2 / −53 | %11,2 / −43 | %13,3 / −31 | %12,6 / −31 |
| Aylık kontrollü %15 trail eklenmiş, ≥10 firma | %14,5 / −52 | %10,4 / −35 | %11,6 / −35 | %10,8 / −35 |
| Piyasa (VW) | %10,1 / −79 | %8,5 / −50 | %14,1 / −25 | %13,5 / −25 |

- **İstatistik:**
  - ≥10 firmalı evrende 2000+ kenar +4,3 puan, t = 1,38 (VD U5).
  - 2015+ nokta tahmin +3,4 puan, %90 aralık [−7,2; +15,8]: bilgi yok (VD U4).
  - 2010–26'da Sharpe piyasanın altında (VA §2.2, §3.1).
- **Kazanç birkaç büyük dalgadan geliyor.** En iyi %10'luk işlemlerin toplam kazanca katkısı %185–530 (D §4.1). İsabet %40–55. 2024'te kural −%11, piyasa +%25 (D §4.2).
- **Beklenti:** Piyasa ± 4 puan. Asıl katkısı kırık kümelerden uzak durmak ve çekirdekle düşük korelasyon (aylık ρ ≈ 0,45, 2000+).
- **Belirsizlik:**
  - ETF'ler FF49 ile birebir aynı değil.
  - Haftalık zamanlama ve günlük GTC stop test edilmedi. Aylık %15 trail getiriyi 1–2,5 puan düşürdü.

### 2.4 Uydu-L: seçici liderler (hisse; brüt ≤ H'nin %25'i, ısı ≤ %2)

**Ön koşullar:**
- Rejim YEŞİL ya da YEŞİL+ (§3.2). SARI'da yalnız FTD sonrası pilot.
- Hisse §4.3 filtresinden geçmiş.
- Önümüzdeki **10 işlem günü içinde bilanço yok.**

**Setup'lar** (PR §1.3: "Giriş sıkışmadan kırılım ya da trend içinde ilk geri çekilme"):
- **(S1) Baz kırılımı:** 2–8 haftalık daralan konsolidasyon. Pivot = baz tepesi.
- **(S2) İlk geri çekilme:** Yükselen 10/20 GHO'ya ilk geri çekilme. Pivot = önceki günün tepesi (Luk: pullback öncelikli; K §4.2).
- **(S3) Bilanço sonrası 2. gün:**
  - Gap ≥ %8, RVOL ≥ 3, kapanış gün aralığının üst yarısında, dolar hacmi ≥ 20 m $ (H §5b).
  - Pivot = gap günü tepesi.
  - Kanıt zayıf: S3'ün akademik çekirdeği long-only olarak piyasayı geçmiyor (T §6.4, §8). En fazla %0,25 risk.

**Giriş: gün içi ekransız uyarlama** [Ö; VP §3 madde 8: "kapanış bazlı uyarlama verilmemiş"]
- Emir: **BUY STOP LIMIT, DAY.** Her gün 12:00–17:25 TSİ arasında yeniden girilir.
  - Tetik = pivot × 1,001.
  - Limit = tetik × 1,015, ya da tetik + 0,5 × ATR14 (hangisi küçükse).
  - Açılış gap'i limiti aşarsa emir dolmaz; bu bilinçli, gap kovalanmaz (IBD alım bölgesi pivot + %5'i aşmıyoruz; PR §1.3 madde 2).
- **Makro günler** (CPI 10.11, PPI 13.11, FOMC tutanakları 18.11): yeni buy-stop yalnız 16:45 TSİ'den sonra girilir.
- **Başarısız kırılım** [Ö]: Giriş günü kapanışı pivotun %1'inden fazla altındaysa ertesi gün MOO ile çık.

**İlk stop:**
- Yapısal: baz dibi ya da S2/S3'te setup günü dibi.
- Mesafe ≤ min(%8; 1,5 × ATR14). Yapısal stop daha uzaksa **işlem yapılmaz.**
- Emir: **GTC SELL STOP**, giriş dolunca hemen konur (bracket child).
- Kanıt: Tavanlar ≤ 1 ATR (Kullamägi), %7–8 (IBD), %10 (Minervini) (PR §1.3 madde 3). Kapanış bazlı mekanik kopyada **1 ATR stop ve 3 günlük çıkış kötü sonuç verdi** (VP A12). Bu yüzden 1,5 ATR tavanı ve MA trail seçildi.

**Boyut:**
- Adet = (H × r) / (giriş − stop).
- r:
  - İlk 50 işlem **%0,25**.
  - 50 işlemde E[R] ≥ +0,2R ve rejim YEŞİL ise %0,5.
  - YEŞİL+, yıl içi kâr yastığı ≥ %10 ve 100 işlemde E[R] ≥ +0,3R ise en fazla %0,75 (PR §3.5 madde 1).
- **Tek pozisyon ≤ H'nin %10'u.** Uydu-R de küme maruziyeti taşıdığı için Kullamägi'nin %20–25'inin altında tutuldu.

**Kâr yönetimi** (PR §1.3 madde 7–8; Kullamägi: 3–5 günde 1/3–1/2, ardından stop başabaşa):
- Emri iki parçaya bölün:
  - **Parça A (1/3):** bracket; hedef GTC SELL LIMIT = giriş + 2R; stop = ilk stop.
  - **Parça B (2/3):** yalnız GTC stop.
- A dolunca ertesi sabah B'nin stopu **giriş fiyatına** çekilir.
- **Trail (B):**
  - Gece kontrolünde kapanış < 10 GHO (ADR% ≥ 4 olan hızlı hisse) ya da < 20 GHO (diğerleri) → ertesi gün **MOO sat.**
  - Ayrıca her yeni yüksek dipten sonra GTC stop o dibin altına çekilir (gap koruması).
- **Zaman:** 15 işlem günü içinde +1R görülmediyse 16. gün MOO ile çık [Ö, test edilmedi].

**Piramit** (PR §1.3 madde 6: yalnız kazanana, küçülen dilimlerle; IBD %50/30/20):
- Pozisyon ≥ +1,5R iken yükselen 10/20 GHO'ya geri çekilip dönerse: yeni buy-stop, ekleme = ilk adedin %50'si. Eklemenin stopu geri çekilme dibi.
- Eski stoplar yükseltilir; toplam pozisyon riski ≤ 1R (ilk risk).
- SARI'da ekleme yok. YEŞİL'de en fazla 2 ekleme. Maliyet düşürme (kaybedene ekleme) **asla.**

**Bilanço** (PR §1.3 madde 9, §3.5 madde 5; Kell "earnings size"):
- Bilançoya 2 işlem günü kala pozisyon < +2R ise bilançodan önceki gün MOO ile kapatılır.
- ≥ +2R ise pozisyon, 2 × implied move'luk bir gap'in kaybı ≤ 1R olacak boyuta indirilir.

**Dürüst beklenti:**
- Doğrulanmış kazananların profili: isabet %22–45, kazanan 2–5 × kaybeden (anchor). +0,4–0,6R/işlem (PR §0.2). Ancak bu sayıların bir kısmı doğrulanamadı: Luk'un istatistikleri (VA #15), Minervini'nin isabeti (VP A3).
- Taban oranlar: USIC katılımcılarının %8–17'si kârlı (K §4.1). Tayvan'da yıllık ~%13 kârlı, < %1 kalıcı (VA #8).
- Bu kullanıcıda kenar: −0,2R ile +0,3R arası; bilinmiyor.
- H'ye etkisi (%0,25 risk, yılda 60–100 işlem): **−%4 ile +%6/yıl.**
- %25–30 isabette 200 işlemde 12–17'li kayıp serisi normal: %25 isabette P(≥15) = %49 (K §5.3). %0,25 riskte 15 ardışık kayıp ≈ −%3,7. Böyle bir seri tek başına öldürme gerekçesi değil.

### 2.5 Bu planda bilinçli olarak olmayanlar

| Ne | Neden |
|---|---|
| 3x ETF, NDX kaldıracı | T §3.5, S §8.1 |
| Tekil hisse ya da tema kaldıracı | PR §3.3: kümelenme %1 riskte bile kuyruğu ~%35–40 büyütüyor |
| Opsiyon alımı (ilk 6 ay) | VIX 28 ve ters vade yapısı: primler pahalı (H §0 madde 10). Opsiyon ortalamada kaybettiriyor (PR §0.5). Midas'ta yalnız alım var |
| Kısa vadeli reversal, PEAD (büyük hisse), takvim etkileri | Öldü (T §0.8–9, S §1.6) |
| Kırık "anlatı" kümelerinde dip alımı (AI, nükleer, kuantum, kripto, drone/uzay) | D §6.2, §7.4 |
| Açığa satış | Locate ve borrow maliyeti; ayı rallisi riski (K §5.4, PR §1.4) |

---

## 3. Rejim anahtarı

### 3.1 Göstergeler (her ABD kapanışından sonra)

| Kod | Gösterge | Eşik | Kaynak |
|---|---|---|---|
| G | Çekirdek kapısı (latch) | Açılış: SPX > 200 GHO × 1,01 ve 10 > 20 GHO. Kapanış: SPX < 200 GHO × 0,99 | BT-B (N); T §3.4 bant ızgarası |
| K10 | SPX 10 GHO > 20 GHO | – | Kullamägi filtresi (PR §1.1, §1.3 madde 10) |
| S | Stres | VIX ≥ 22 **veya** VIX/VIX3M ≥ 1,00 | H §5d okuma kuralları; PR §1.4 |
| B | Genişlik | S5FI ≥ 50 ve S5TH ≥ 60 | H §5d |
| N | Büyüme | NDX > 200 GHO | T §3, H §3 |
| FTD | Takip günü | Ralli denemesinin 4. ya da sonraki günü, SPX veya NDX ≥ +%1,25, hacim önceki günden yüksek. Denemenin dibi kapanışla kırılırsa iptal | PR §1.4; H §3 (+%1,5 de kabul) |
| σ̂ | Oynaklık | §2.1 | BT-B |

### 3.2 Durumlar ve kol izinleri

| Durum | Tanım | Çekirdek | Uydu-R | Uydu-L | Toplam ısı (uydu + lider) |
|---|---|---|---|---|---|
| **KIRMIZI** | SPX < 200 GHO × 0,99 | 0 (nakit) | Dilim %7, kurallara göre giriş/çıkış | Yeni işlem yok; açıklar stop ve trail'de | ≤ %3 |
| **SARI** | KIRMIZI değil ve (G kapalı veya K10 yok veya S var veya B yok) | G açıksa formül, kapalıysa 0 | Dilim %7 | Yalnız **FTD'den sonra** pilot: ≤ 2 pozisyon, farklı kümelerden, r = %0,25, lider ısısı ≤ %0,5 | ≤ %3 |
| **YEŞİL** | G açık, K10 var, S yok, B var | Formül (L ≤ 2) | Dilim %10 | r = %0,25 (ilk 50 işlem), sonra %0,5. ≤ 5 pozisyon | ≤ %5 |
| **YEŞİL+** | YEŞİL + VIX < 18 + VIX/VIX3M < 0,90 + N + H zirveden > −%5 + ≥ 10 seanstır YEŞİL | Formül | Dilim %10 | r ≤ %0,75 (§2.4 koşulları) | ≤ %6 |

- Kanıt: Isı tavanları %3/%5/%6 (PR §3.5 madde 4, Elder). IBD FTD sonrası maruziyet %40–60 (PR §3.1). "Kötü rejimde maruziyet ~0" (PR §1.3 madde 10).
- **Dürüstlük notu:** Bu durum tablosu yalnız çekirdek ve uydu-R için test edildi. Lider kolu için pratisyen kuralıdır, test edilmedi. Kullamägi'nin "filtreye uysaydım kaybın %90'ından kaçardım" iddiası kendi karşı-olgusal tahmini (VA #16).

### 3.3 Bugün ne diyor (5.11 kapanışı, NFP öncesi)

| Gösterge | Değer | Eşik | Sonuç |
|---|---|---|---|
| SPX / 200 GHO | 7.353,73 / 7.322,7 (+%0,42) | Açılış ≥ 7.396; kapanış < 7.250 | Bant içi |
| 200 GHO eğimi (20 seans) | +%1,06 | – | Yükseliyor; 200 GHO günde ~3–4 puan artıyor. 13.11'e kadar eşikler ≈ 7.415 / 7.270 |
| SPX 10 / 20 / 50 GHO | 7.622 / 7.680 / 7.687 | 10 > 20 | **Yok.** Kabaca 7 seans ≥ 7.735'te ya da 10 seans ≥ 7.625'te kapanış gerekir (BT-B hesabı) |
| σ̂ = max(RV20, RV60) | max(%20,2; %14,0) = %20,2 | – | Kapı açılsaydı L* = 1,24 |
| VIX; VIX/VIX3M | 28,18; 1,10 | < 22; < 1,00 | **Stres var** (4.11'de VIX 16,61; tek günlük sıçrama; VP A11) |
| NDX / 200 GHO | 26.630 / 27.977 (−%4,8); zirveden −%14,7 | > | Yok |
| S5FI / S5TH | 62,5 / 66,1 (TradingView önbelleği, zaman damgası karışık; H §3) | ≥ 50 / ≥ 60 | Var (grafikte teyit edin) |
| FTD | Yok | En erken: 6.11 artıda kapanırsa 11.11; 6.11 yeni dip yaparsa 12.11 | – |
| **Durum** | | | **SARI.** Çekirdek: sıfırdan başlangıç → **0 (nakit)**. Uydu-R: dilim %7. Uydu-L: FTD bekleniyor |

### 3.4 Bu hafta ne yapılır?

Kur: Karar gece, emir 12:00–17:25 TSİ, ekran yok.

- **Cuma 6.11 gece (00:15 TSİ):** NFP günü kapanışıyla §3.3 tablosunu yenileyin.
  - SPX artıda kapandıysa ralli denemesinin 1. günü 6.11'dir.
  - SPX < 7.250 kapanırsa durum KIRMIZI: uydu dilimleri yine %7, lider yok, çekirdek nakit.
- **Pazartesi 9.11:**
  - Çekirdek işlemi yok (kapalı başlangıç).
  - Lider işlemi yok (FTD yok).
  - Hesap fonlandıysa **Uydu-R ilk kurulumu.** Hafta sonu 6.11 kapanışıyla 12 aylık sıralama yapılır. Zamanlamayı geçen kümeler için 17:25'e kadar **MOO** emirleri girilir, her biri H'nin %7'si. Dolumdan sonra GTC stop = dolum × 0,88.
  - Fonlanmadıysa ilk fonlanan günde aynısı yapılır. CPI günü 16:45'ten sonra MOO girilebilir; MOO 17:30'da çalışır.
- **Salı 10.11, CPI 16:30 TSİ:**
  - 16:30'dan önce yeni emir yok; mevcut GTC stoplar durur.
  - CPI sonrası kapanış FTD sayımını etkiler. 6.11 1. günse Salı 3. gündür, yani FTD olamaz.
  - Gece: CRWV bilançosu (AI kümesi için turnusol). İşlem yok, AI kümesi kapalı.
- **Çarşamba 11.11 (Gaziler Günü; hisse açık, tahvil kapalı):**
  - En erken FTD günü.
  - FTD gelirse Perşembe 12:00–17:25 arasında en fazla 2 pilot: farklı kümelerden, r = %0,25, buy-stop-limit + GTC stop.
  - Pilot sağlık kümesindeyse küme ısısı (uydu XLV dilimi dahil) ≤ %1,5 olmalı.
- **Perşembe 12.11:**
  - Pilot emirleri (FTD varsa).
  - Gece CSCO ve AMAT bilançoları: AI kümesinin açılma koşulu (SMH RS 52 hafta zirvesi) bu hafta beklenmiyor.
- **Cuma 13.11, PPI 16:30:**
  - 16:45'ten önce yeni buy-stop yok.
  - Gece **haftalık inceleme:** bekleyen uydu dilimlerinin zamanlama kontrolü (Pazartesi 16.11 MOO), ısı tablosu, R-defteri, çekirdek transfer tetiği (10 > 20 var mı?).
- **Sonraki hafta:**
  - NVDA bilançosu **17.11 kapanış sonrası, 01:00 TSİ** (H §2.1, NVIDIA IR). Görev notunda ~19.11 geçiyor; IR sayfasından teyit edin.
  - 18.11 22:00 FOMC tutanakları. 18–19.11 TGT/TJX/LOW/WMT bilançoları: perakende ve temel tüketim isimlerinde 10 günlük bilanço filtresi.
  - 20.11 aylık opsiyon vadesi. 25.11 PCE ve GSYH.
  - **26.11 kapalı. 27.11 erken kapanış 21:00 TSİ.**
  - **30.11 ay sonu sıralaması → 1.12 MOO.**

---

## 4. Evren, izleme listesi, kümeler

### 4.1 Tarama ayarları (H §5'ten, plan uyarlamasıyla)

- **Uydu-L ana tarama** (H §5a, finviz sıkı versiyon; 6.11'de 86 sonuç): `https://finviz.com/screener.ashx?v=152&f=cap_midover,sh_avgvol_o1000,sh_price_o20,ta_highlow52w_b0to5h,ta_sma200_pa,ta_sma50_pa,ta_volatility_mo2&o=-perf13w&c=1,2,4,6,42,43,44,47,51,53,54,57,63,65,68`
- **Pine Screener** (H §5a betiği):
  - `TT = 1`, `RS line / 52w max ≥ 0,97`, `50d $Vol ≥ 20`.
  - Plan ekleri: **`Dist to 52wH ≥ −5`** (SARI'da; YEŞİL'de −10). `RS raw` azalan sıralama.
- **S3 bilanço gap'i** (H §5b): `earningsdate_yesterdayafter`, `sh_relvol_o3`, `ta_gap_u8` URL'si. Plan, gap gününde değil **ertesi gün** buy-stop ile girer.
- **Elle kontrol:**
  - Sonraki bilanço tarihi (IR sayfası).
  - ADR% ve ATR14.
  - Ortalama hacim × fiyat ≥ 20 m $.
  - Satın alma/birleşme arbitrajı profili: `ta_volatility_mo2` bunları eler (H §4: SGRY, BRZE).
- **Uydu-R:** H §5c ETF listesi. Sütunlar: Perf 1Y / 3M / 6M, SMA50 uzaklığı, 52H uzaklığı. Oran grafiği `XLV/SPY` vb.

### 4.2 Küme tanımları (tek bahis birimi)

- **Tanım:** Aynı anlatı ya da 60 günlük getiri korelasyonu ≥ 0,6 olan isimler tek kümedir (PR §3.5 madde 2).
- **Küme ısısı** ≤ %1,5 (YEŞİL+'da %2); uydu dilimi + aynı kümedeki liderler toplamı. Küme brütü ≤ H'nin %25'i.

| Küme | ETF vekili | Hisse havuzu (H §4; öneri değil) | Durum 6.11 |
|---|---|---|---|
| S1 Sağlık (medtech, ilaç, hizmet, araç) | XLV, IHI, IHF, PPH, IBB, XBI | MDT, EW, BDX, GEHC, TMO, REGN, LLY, RPRX, CNC, EHC, IDXX | **Açık.** Lider küme (XLV 6 ayda +%27,7) |
| S2 Borsalar ve finansal veri | (IAI zayıf) | CBOE, CME, TW | Açık (hisse) |
| S3 Sigorta | (XLF kısmen) | AJG, MRSH, ACGL, BRK-B | Açık. BRK-B bilanço tarihini teyit edin |
| S4 Temel tüketim | XLP | KDP, BJ | Açık. BJ 20.11 bilanço |
| S5 Altyapı hizmeti (atık, su, kule, depolama) | XLU, XLRE | RSG, VLTO, AWK, CCI, PSA | Açık |
| S6 Konaklama ve tüketici | XLY, XRT | MAR, HLT, HAS, EBAY, SN | Açık |
| S7 Dikey yazılım | IGV | ROP, MANH, U, GEN | ETF bekle (IGV 50 GHO'nun −%5,6 altında). Hisseler tek tek değerlendirilir |
| S8 Finans/bankalar | XLF, KRE, KBE | – | İzle (XLF 3 ayda −%1) |
| S9 Malzeme ve konut | XLB, ITB, XHB | – | İzle |
| K1 **AI donanım, yarı iletken, güç, veri merkezi** | SMH, XLK | NVDA, AMD, MU, MRVL, AVGO, VRT, GEV, ETN, PWR, CEG, VST; AAPL (FF49'da Hardw) | **KAPALI.** Kırık (SMH 52H zirvesinin −%30 altında) + GSY bayrağı. Açılma: SMH/SPY RS 52 hafta zirvesi (D §7.4) |
| K2 Enerji | XLE, XOP, OIH | XOM, COP, MPC, VLO, PSX | **Bekle.** 50 GHO altında; İran haberi riski (H §4) |
| K3 Altın ve gümüş madencileri | GDX | NEM, AEM | Bekle. Balon sonrası, zirveden −%27 |
| K4 Nükleer/uranyum | URA | OKLO, SMR, LEU, CCJ | KAPALI (çöküş; D §6.2) |
| K5 Kuantum/spekülatif | – | IONQ, RGTI, QBTS | KAPALI |
| K6 Kripto | (IBIT) | COIN, MSTR, madenciler | KAPALI |
| K7 Savunma, drone, uzay | ITA, XAR | LMT, RTX…; KTOS, AVAV, RKLB | Bekle (ITA −%20,7) |

### 4.3 Küme başına 3–5 isim seçimi

1. **Küme açık mı?** §4.2 tablosu ve kümenin ETF vekili 50 GHO üstünde mi?
2. **Ön filtre** (§4.1): TT = 1, RS çizgisi zirveye ≤ %3 uzak, 52H'ye uzaklık ≤ %5 (SARI) ya da ≤ %10 (YEŞİL), dolar hacmi ≥ 20 m $, fiyat > 20 $.
3. **Bilanço filtresi:** önümüzdeki 10 işlem günü içinde rapor yok.
4. **Setup filtresi:** Tanımlı bir pivot olmalı ve stop mesafesi ≤ min(%8; 1,5 ATR). 10 GHO'nun 2 ATR'den fazla üstündeki hisse "uzamış" sayılır, alınmaz.
5. **Sıralama:** `RS raw` (H §5a Pine; IBD ağırlıklı ROC). Kümede ilk 3–5 isim izleme listesine girer.
6. **İşlem:** Kümeden **aynı anda en fazla 2 pozisyon.** ρ = 0,69'da 3 pozisyon yalnız 1,26 bağımsız bahis (PR §3.2). Küme ısısı tavanı bunu zaten zorlar.

### 4.4 Güncel adaylar (5.11 fiyatları, H §4; öneri değildir)

| Sınıf | İsimler | Neden |
|---|---|---|
| **Uygun: izleme listesi, pivot bekliyor** | S1: BDX (−%1,1), EHC (−%1,5), EW (−%3,2), RPRX (−%3,6), TMO (−%4,8). S2: TW (−%1,1), CME (−%4,8), CBOE (−%4,9). S3: MRSH (−%2,1), AJG (−%2,2), ACGL (−%2,7). S5: AWK (−%0,8), PSA (−%1,6), RSG (−%2,0), VLTO (−%2,7), CCI (−%4,3). S6: HLT (−%3,1), MAR (−%3,7), SN (−%3,6), HAS (−%3,6), EBAY (−%3,8). S7 (tek tek): U (−%2,3), ROP (−%3,2), MANH (−%3,2), GEN (−%3,3). S4: KDP (−%4,0) | Zirveye ≤ %5 uzak, 50 ve 200 GHO üstünde, son bilanço geride kalmış |
| **Bekle** | MDT ve BRK-B (bilanço tarihi yakın, teyit), BJ (20.11 bilanço), GEHC (−%6,7), LLY (−%7,1; ObesityWeek 14–17.11), REGN (−%9,8), CNC (tek günde +%12,6, baz yok), IDXX (EP sonrası zirveden −%12,9; bayrak ya da baz bekleyin) | SARI'da zirveye uzaklık > %5, bilanço riski ya da tanımlı baz yok |
| **Kapalı** | K1 tümü, AAPL dahil (Hardw kümesi, GSY bayrağı); K4–K6; enerji (K2), 50 GHO'ya dönene kadar | §4.2 |

**Kural:** SARI'da FTD gelse bile en fazla 2 pilot açılır. Önerilen kümeler: Uydu-R'de dilimi olmayan bir küme (S2, S3 ya da S5) ve S1. S1'de uydu XLV dilimi varsa küme ısısı limiti sağlık pilotunu ≤ %0,66 ısıyla sınırlar.

### 4.5 Uydu-R ön sıralaması: yaklaşık, yalnız fikir vermek için

12 aylık getiri elimizde yok. Aşağıdaki tablo H §5c ham verisinden alınan yılbaşından beri (YTD, ~10 ay) getirilerle yapıldı. Kesin sıralama hafta sonu "Perf % 1Y" ile yapılmalı.

| Küme | En iyi ETF (YTD) | 50 GHO'ya uzaklık | Zamanlama |
|---|---|---|---|
| K2 Enerji | XOP +%37,6 / XLE +%37,2 | −%9,3 / −%5,8 | **Geçmez → dilim nakitte** |
| K1 AI | SMH +%30,5 | −%16,9; 52H'nin −%30 altı | **Geçmez** (RS zirvesi de yok) |
| S1 Sağlık | IHF +%24,1 / IBB +%24,1 / XLV +%18,3 | +%3,5 / +%0,5 / +%5,7 | **Geçer** → XLV (en geniş; fark < 5 puan sayılırsa) |
| S4 Temel tüketim | XLP +%15,9 | +%5,8 | İlk 3 dışında kalabilir |
| S9 Malzeme | XLB +%15,4 | +%2,7 | İlk 3 dışında kalabilir |

**Muhtemel sonuç:**
- 12 aylık sıralama da YTD sırasına benzerse ilk 3 küme Enerji, AI ve Sağlık olur. Yalnız sağlık dilimi açılır: H'nin %7'si.
- Enerji 50 GHO'ya döndüğünde girilir. AI için RS zirvesi beklenir.
- İkame (XLP/XLB'yi koymak) bu planın kuralı değil.

---

## 5. Risk limitleri

### 5.1 Tablo (H'nin yüzdesi; dolar karşılıkları 50k / 250k / 1m $)

| Limit | Değer | 50k | 250k | 1m | Kaynak |
|---|---|---|---|---|---|
| Lider riski/işlem (ilk 50 işlem) | %0,25 | 125 $ | 625 $ | 2.500 $ | PR §3.5 madde 1 |
| Sonra / tavan | %0,5 / %0,75 | 250 / 375 | 1.250 / 1.875 | 5.000 / 7.500 | PR §3.5 |
| Tek hisse pozisyonu | ≤ %10 | 5k | 25k | 100k | Kullamägi %20–30 tavanından sıkı (PR §3.1) |
| Uydu dilimi SARI / YEŞİL | %7 / %10 | 3,5k / 5k | 17,5k / 25k | 70k / 100k | §2.3 |
| Küme ısısı | ≤ %1,5 (YEŞİL+ %2) | 750 $ | 3.750 $ | 15k $ | Anchor; PR §3.5 madde 3 |
| Küme brütü | ≤ %25 | 12,5k | 62,5k | 250k | PR §3.5 |
| Toplam ısı SARI–KIRMIZI / YEŞİL / YEŞİL+ | %3 / %5 / %6 | 1,5k / 2,5k / 3k | 7,5k / 12,5k / 15k | 30k / 50k / 60k | Anchor; Elder (PR §3.1) |
| Çekirdek nominal | ≤ L × C, L ≤ 2. Stres kaybı (nominal × %20) ≤ H'nin %20'si | ≤ 50k | ≤ 250k | ≤ 1m | §2.1; BT-B 1987 −%35 penceresi |
| Toplam brüt (YEŞİL+) | ≤ %155 (çekirdek %100 + uydu %30 + lider %25) | 77,5k | 387,5k | 1,55m | – |
| Aylık devre kesici | Ayın gerçekleşen zararı + açık risk ≥ %6 (ilk 6 ay %4) → ay sonuna kadar yeni uydu/lider girişi yok | 3k (2k) | 15k (10k) | 60k (40k) | Elder (PR §3.5 madde 8) |

Aylık devre kesicide çekirdek formülü çalışmaya devam eder.

### 5.2 Gap-ayarlı ısı ve bilanço

- **Pozisyon riski** = adet × max(giriş − stop; 1,5 × ATR14) (PR §3.5 madde 5). Örnekler: Intel −%30 tek günde, AMD −%17,3 (PR §1.2).
- **Bilanço penceresinde:** risk = 2 × implied move. Taşınacak pozisyonun boyutu buna göre küçültülür (§2.4).
- **Uydu dilimi ısısı** = dilim × (fiyat − GTC stop) / fiyat.

### 5.3 Drawdown merdiveni (H'nin zirvesinden, günlük piyasa değeriyle)

| Eşik | Eylem | Gerekçe |
|---|---|---|
| −%5 | Lider r × 0,5 | PR §3.5 madde 7 |
| −%10 | Lider yalnız A+ setup, r = %0,25. **Çekirdek L ≤ 1,0** | PR §3.5; kaldıraç meşruiyeti (§2.2) |
| −%15 | 2 hafta lider işlemi yok; R-defteri incelemesi | PR §3.5 |
| −%20 | Çekirdek L ≤ 0,5. Uydu dilimleri yarıya | Ş §5.2 madde 8 (engel bazlı −%25'te yarıya) |
| −%25 | Tüm kollar yarıya. Lider kolu kapanır | Ş §5.2 madde 8 |
| **−%30** | **Plan durur:** her şey nakde, tam inceleme (§7.4) | B-Standart'ın 1930+ backtest MaxDD'si −%28; bunu aşmak modelin dışına çıkıldığını gösterir |
| Geri yükleme | Kaybın yarısı geri gelince bir kademe yukarı | PR §3.5 |

**Kalibrasyon notu (BT-B):**
- Sıkı merdiven (−%10'da ×0,5, −%15'te ×0,25) sistematik B-Standart'a uygulandığında sonuçlar:

  | Dönem | Merdivensiz CAGR / MaxDD | Merdivenli CAGR / MaxDD |
  |---|---|---|
  | 1930+ | %13,1 / −%27,9 | %10,3 / −%27,2 |
  | 2000+ | %10,7 / −%16,4 | %8,4 / −%14,2 |

- Bu PR §3.3'ün "rejim filtresi birincil, merdiven ikincil" bulgusuyla ve Kaminski–Lo ile tutarlı. Sistematik kollara bu yüzden yalnız −%20 ve sonrasında fren uygulanıyor.

---

## 6. Erişim ve uygulama

### 6.1 Kurum seçimi

| Kurum | Rol | Neden | Kısıt |
|---|---|---|---|
| **IBKR Pro** (ana) | Tüm kollar. MES, bracket/GTC/MOO, hisse/ETF | 0,005 $/adet (min 1 $); marj %5,38; boş nakde %3,38; Türkiye listede (VC #16). Hesap 1–3 iş günü + SWIFT 1–2 gün → **ilk işlem gerçekçi olarak 11–13.11** (H §1.3) | Bağlı kuruluş (IB LLC mi IBIE mi) doğrulanamadı. IBIE'ye bağlanırsa PRIIPs nedeniyle ABD ETF'leri kısıtlanabilir (H §1.2). PRIIPs yalnız AB/AEA mukimine uygulanır (VA §4 madde 7, bellek). **Başvuruda yazılı teyit alın.** ETF kısıtı varsa: çekirdek MES, Uydu-R Midas'ta |
| **Midas** (köprü) | Pazartesi Uydu-R ve küçük hesapta SPY/SSO çekirdeği | Onay 1–2 gün; işlem başı 1,5 $ (H §1.2) | Yalnız call/put alımı; spread, yazım, marj, vadeli yok. **Stop-limit, GTC, MOO ve bracket desteği sayfalarda yok; uygulamada teyit edin.** Yoksa lider kolu yalnız IBKR'de. Kur makası yayınlanmıyor; küçük tutarla test edin |
| İş Yatırım TMI, Gedik, Garanti | Yalnız düşük devirli çekirdek/uydu için yedek | Mevcut hesapla hızlı | %0,25–0,30 komisyon; 20k $ pozisyonda gidiş-dönüş ~50–63 bp (P §1.1). Lider kolu için pahalı |

**IBKR başvurusu:**
- Marj hesabı. İzinler: ABD hisse, ETF, **ABD vadeli (CME)**; opsiyon seviye 2 sonra.
- VİOP tecrübesini "futures/options experience" olarak beyan edin (H §1.2).
- **W-8BEN** imzalayın: temettü stopajı %20; yoksa %30 (P §1.3).

### 6.2 Emir tipleri (kol bazında)

| Kol | Giriş | Çıkış | Zaman (TSİ) |
|---|---|---|---|
| Çekirdek ETF | MOO | MOO | Karar gece; emir ertesi gün 17:25'e kadar |
| Çekirdek MES | Limit (vadeli son fiyat ± %0,1) | Limit (aynı) | 17:30–17:45 |
| Uydu-R | MOO | Sıralama/filtre çıkışında MOO; stop için **GTC SELL STOP** | Haftalık: Cuma gece karar → Pazartesi MOO. Aylık: son işlem günü gecesi → ilk işlem günü MOO |
| Uydu-L | **BUY STOP LIMIT, DAY** (tetik pivot × 1,001; limit tetik × 1,015) | Parça A: GTC LIMIT (+2R) + GTC STOP. Parça B: GTC STOP; trail ihlalinde ertesi gün MOO | Emir 12:00–17:25. Makro günlerde 16:45'ten sonra |

**Notlar:**
- Gap'te stop emri piyasa emrine döner ve 1R'den fazla kayıp verebilir. Bu yüzden gap-ayarlı ısı kullanılıyor (§5.2).
- 27.11 erken kapanış (21:00 TSİ).

### 6.3 Rutin takvimi (TSİ)

| Ne zaman | İş | Süre |
|---|---|---|
| Her gece 00:15–01:00 ya da sabah 07:30–09:00 | Rejim tablosu (Ek B Pine), σ̂, L*, trail kontrolleri, 10 günlük bilanço takvimi, emir listesi | 20–30 dk |
| 12:00–17:25 | Emir girme ve değiştirme | 10 dk |
| Cuma gece / Cumartesi | Haftalık: uydu zamanlaması, ısı, R-defteri, kümeler, merdiven | 60 dk |
| Ay sonu hafta sonu | Uydu-R sıralaması, aylık rapor (§7.2) | 60–90 dk |

### 6.4 Maliyetler

- **Komisyon:**
  - IBKR: 0,005 $/adet. Örnek: 400 adet × 50 $ işlemde gidiş-dönüş ~2 bp (P §1.1).
  - MES komisyonu bu dosyalarda yok; platformdan alın.
  - Midas: işlem başı 1,5 $.
- **Kur dönüşümü:**
  - Kambiyo BSMV binde 2 (P §2.5; VC tarafından doğrulanamadı).
  - Banka makası ve Garanti'de %0,50.
  - Midas makası yayınlanmıyor.
- **Veri** (P §5): TradingView Plus/Premium + Finviz Elite + IBKR verisi ≈ 1.000–1.300 $/yıl.

  | Hesap | Tam setin H'ye oranı | Öneri |
  |---|---|---|
  | 50k $ | ~%2,4 (çok yüksek) | TradingView Essential (12,95 $/ay) + ücretsiz finviz, ~%0,6 |
  | 250k $ | ~%0,5 | Tam set |
  | 1m $ | ~%0,1 | Tam set |

- **SSO gideri:** ~%0,9 + gömülü finansman (bellek; T'de LETF varsayımı %0,9). MES'te gider yok; finansman fiyata gömülü (S §8.1).

### 6.5 Vergi ve kayıt (TR beyannamesi)

| Konu | Kural | Kaynak |
|---|---|---|
| Nitelik | Yurt dışı borsa kazancı = değer artışı. Tutar ne olursa olsun yıllık beyan (Mart). Ödeme Mart ve Temmuz | P §2.1; VC #10 |
| Hesap | Alış ve satış o günlerin kuruyla TL'ye çevrilir. **Kur farkı vergilidir.** USD'de zarar edilse bile TL'de kâr varsa vergi doğar | P §2.1 |
| Endeksleme | Yİ-ÜFE artışı ≥ %10 ise (alış ayı dahil, satış ayı hariç; ~6 ay). Çekirdekteki uzun pozisyonlarda gerçekleşebilir | P §2.1 |
| Zarar | Yalnız aynı takvim yılında, yabancı menkul kazançlarıyla mahsup. Devretmez. **Kasım–Aralık 2026 zararı 2027'ye taşınmaz** | VC #10 |
| Giderler | Komisyon ve saklama düşülür. **Marj faizi düşülmez** | P §2.1 |
| Temettü | ABD'de %20 stopaj (W-8BEN), TR'de mahsup için belge gerekir. 22.000 TL'yi aşarsa beyan | P §1.3; VC #12 |
| Faiz | IBKR nakit faizi ve T-bill faizi menkul sermaye iradı olarak beyan edilir | P §4.1 |
| **Boştaki para** | **USD nakit** (IBKR %3,38). Dövizin kendi kur kazancı vergisiz. T-bill ya da SGOV/BIL bir menkul kıymettir; anapara kur farkının vergilenmesi gri alan. Varsayılan USD nakit; T-bill'i müşavir onayıyla kullanın | P §2.5, §4.2 |
| Vadeli ve opsiyon | Yurt dışı vadeli kazancının niteliği belirsiz; özelge yok. MES'te kur farkı yalnız K/Z'ye mi uygulanır? **Teyit edin.** Doğruysa ETF'e göre vergi avantajı olur | VC §2 madde 9; P §2.1 |
| Ticari kazanç riski | Yüksek işlem sıklığı "ticari kazanç" iddiasına dayanak olabilir (defter ve geçici vergi). Lider kolunda yılda 60–100 işlem → müşavire sorun | P §2.1 |
| Tarife | 2026: 190k / 400k / 1m / 5,3m TL; %15 / 20 / 27 / 35 / 40 (P §2.1; **VC #11: doğrulanamadı**) | – |
| ABD veraset | ABD varlıkları 60k $'ı aşarsa Form 706-NA riski. 250k ve 1m hesapta geçerli. İrlanda domisilli UCITS alternatifi (bellek) ayrıca araştırılmalı | VA #36; P §1.2 |
| Pasif alternatif | TEFAS yabancı hisse fonu: %17,5 nihai stopaj, ücret %2,5–2,9, T+1/T+3 valör. Çekirdeğin 1x kısmı için yüksek dilimde vergi açısından daha iyi olabilir. Kaldıraç yok, gecikmeli, takip farkı var; test edilmedi | P §2.4; H §1.4 |

**Kayıt (her işlem):**
- Tarih, adet, USD fiyat, komisyon.
- **İşlem günü TCMB USD/TRY kuru** (hangi kur türü: müşavirle teyit) ve TL tutar.
- Alış ayının Yİ-ÜFE endeksi.
- Aracı kurum ekstreleri: IBKR Activity Statement, 1042-S.
- Maliyet yöntemi (FIFO ya da ortalama) müşavirle belirlenir.

---

## 7. Öldürme kriterleri ve ileri ölçüm protokolü

### 7.1 İşlem defteri alanları (her işlem; Excel/Sheets)

- **Kimlik:** ID; kol (Çekirdek / Uydu-R / Uydu-L); küme; setup (S1/S2/S3; rotasyon; çekirdek ayarı); işlem öncesi hipotez kartı numarası.
- **Rejim:** Girişteki durum (KIRMIZI/SARI/YEŞİL/YEŞİL+), σ̂, VIX, FTD var/yok.
- **Giriş:** Ticker; tetik; dolum; **kayma (bp ve R)**; ilk stop; R ($); adet; pozisyonun H'ye oranı; gap-ayarlı pozisyon ısısı; toplam ısı; küme ısısı; ATR14; ADR%; bilanço tarihi.
- **Çıkış:** Tarih ve fiyat; neden (stop / +2R / trail / başarısız kırılım / zaman / bilanço / rejim / sıralama); **R-katı**; MAE ve MFE (R); tutma günü; komisyon.
- **Vergi:** Alış ve satış TCMB kuru; TL maliyet ve satış bedeli; TL kazanç; Yİ-ÜFE (alış ve satış ayı).
- **Kural uyumu:** Sapma var/yok; varsa nedeni. Ekran görüntüsü bağlantısı.

### 7.2 Aylık rapor metrikleri (Ş §5.3 madde 5)

- **Lider kolu:** E[R] ve bootstrap %90 güven aralığı; isabet; ortalama kazanç/kayıp; profit factor; en uzun kayıp serisi; MAE/MFE; net kârın en iyi %10'luk işlemlere düşen payı (> %100 normal); kayma (bp); ısı kullanımı.
- **Çekirdek:** Modele uyum. Gerçekleşen L ile Ek B'deki L* farkı; ayarlama gecikmesi (gün); takip farkı (yıllık ≤ %1 hedef).
- **Uydu-R:** RSP ve SPY'ye göre fark; tutulan kümeler; stop sayısı.
- **Toplam:** H'nin USD getirisi, **vergi sonrası tahmini USD** (§8.3 formülü) ve TL karşılığı. USD nakde ve TL engeline (%31–38) göre fark. MaxDD ve merdiven kademesi. S&P ve USDTRY'ye beta ve korelasyon.

### 7.3 Ölçek büyütme kapıları

| Ne | Ne zaman | Koşul |
|---|---|---|
| Lider r: %0,25 → %0,5 | ≥ 50 işlem | E[R] ≥ +0,2R ve rejim YEŞİL (PR §3.5). Ş §5.3'ün "12 ay ve 100 işlemden önce büyütme yok" kuralı daha sıkı. Bu planda %0,5'e geçiş 50 işlemde izinli; %0,75 en erken 100 işlem ve 12 ayda |
| Lider r → %0,75 | ≥ 100 işlem ve ≥ 12 ay | E[R] ≥ +0,3R ve %80 güven aralığının alt sınırı > 0 |
| B-Standart → B-Agresif | ≥ 12 ay | Kural uyumu ≥ %95 (sapma oranı); çekirdekte ayarlama gecikmesi ≤ 1 gün; H zirveden −%15'i hiç görmemiş |
| **H/W payını +%10 artırma** | **≥ 12 ay** | (i) Kural uyumu ≥ %95. (ii) H'nin vergi sonrası USD getirisi ≥ USD nakit + 3 puan. (iii) Lider kolu açıksa n ≥ 100 ve E[R] ≥ +0,2R. Üçü birlikte gerekli |

### 7.4 Öldürme kriterleri (önceden yazılı)

| Kol | Kriter | Eylem | Kaynak |
|---|---|---|---|
| Uydu-L | 50 işlemde E[R] < 0 | r = %0,25'te kalır, hipotez kartı gözden geçirilir. 50 işlemde canlı < hedefin (+0,3R) yarısı → boyut yarıya | Ş §5.2 madde 4 |
| Uydu-L | **100 işlemde E[R]'nin bootstrap %90 güven aralığının üst sınırı < 0** | Kol kapanır | Ş §5.2 madde 2 |
| Uydu-L | 150 işlemde %80 güven aralığının üst sınırı < 0 ya da kol düzeyinde düşüş > %20 | Kol kapanır | Ş §5.1 satır 4 |
| Uydu-L | Ortalama kayma > 0,25R ya da > brüt kenarın %50'si | Emir tipi değişir; sürerse kol kapanır | Ş §5.2 madde 3 |
| Uydu-R | 36 ay sonunda RSP'ye göre fark < −5 puan/yıl **ve** SPY korelasyonu > 0,9 (beta sızıntısı) | Kol SPY veya RSP ile değiştirilir | Ş §5.2 madde 7 |
| Çekirdek | Kurala aykırı manuel müdahale (bir kez) | 1 ay lider kolu durur; kural yeniden okunur | – |
| Çekirdek | Kol düşüşü > −%45 (N25 simülasyonunun 1928+ MaxDD'sinin ötesi) | Kol durur; mekanizma incelemesi | Ş §5.2 madde 1 |
| Hepsi | Mekanizma değişirse (ör. FINRA/aracı kurum kuralı, vergi rejimi değişikliği, IBKR erişiminin kapanması) | t-istatistiğine bakılmadan ilgili kol durur | Ş §5.2 madde 5 |
| **Toplam** | H zirveden **−%25** → tüm kollar yarıya. **−%30** → plan durur | | Ş §5.2 madde 8; §5.3 |
| Toplam | 12 ay sonunda H vergi sonrası USD getirisi < USD nakit **ve** kural uyumu ≥ %95 | Plan çalıştı ama değer katmadı → H/W payı yarıya. TL kökenli sermaye TL'ye döner | §1.3 |

**Uyarı:** Kenarı şanstan ayırmak uzun sürer. +0,2R'lik bir sistemde t = 2 için ~450 işlem gerekir (Ş §3.7). Çekirdeğin 3 yıllık getirisi bile 2000 sonrası pencerelerin %8'inde negatif (BT-B). İlk yılın sonucu yöntem hakkında çok az şey söyler. Ölçülen asıl şey **kural uyumu ve maliyet.**

---

## 8. Beklenen sonuç aralıkları ve engel

### 8.1 Backtest (vergi öncesi USD; sistematik kollar; lider kolu dahil değil)

| Sürüm | Bileşim | 1930–2026 CAGR / MaxDD | 2000–2026 | 2010–2026 | 5 yıllık kayan (1950+) medyan / P10 / P90; P(> %20) | 12 aylık kayan (2000+) P10 / medyan / P90; P(< 0); P(> %28) |
|---|---|---|---|---|---|---|
| **B-Standart** | %50 N25 + %30 Uydu-R + %20 nakit | **%13,1 / −%27,9** | **%10,7 / −%16,4** | %12,5 / −%15,3 | %13,4 / %7,0 / %20,3; %11 | −%2,0 / %10,0 / %26,4; %14,6; %9,1 |
| B-Standart, ≥ 10 firma + trail | aynı | %12,3 / −%32,7 | %9,3 / −%15,0 | %11,2 / −%15,0 | %12,5 / %6,4 / %20,4; %12 | – |
| **B-Agresif** | %70 N30 + %30 Uydu-R | %15,7 / −%39,5 | %13,1 / −%20,9 | %16,0 / −%20,8 | %15,9 / %7,6 / –; %30 | −%4,3 / %11,6 / %38,2; %20,4; %19,4 |
| Kıyas: 1x al-tut | %100 piyasa | %10,0 / −%84 | %8,5 / −%55 | %14,2 / −%34 | %12,1 / %1,0 / %19,2 (T §3.6) | – |
| Kıyas: 2x 200 GHO (S §12 "çekirdek 2") | – | %15,4 / −%67 | %11,5 / −%51 | %17,1 / −%40 | %14,6 / %4,2 / %28,5; %31 | – |

**B-Standart yıllık getirileri (BT-B):** 2008 −7,4; 2009 +17,9; 2011 −0,9; 2013 +44,0; 2015 −5,7; 2018 −2,9; 2020 +28,6; 2021 +23,8; 2022 +8,0; 2023 +8,2; 2024 +14,4; 2025 +10,3; 2026 (9 ay) +7,1.

### 8.2 İleriye dönük, tıraşlı beklenti

**Tıraş gerekçeleri:**
- ~30 varyant denendi (seçim yanlılığı).
- FF49 sektörleri ile ETF'ler aynı değil.
- Değerlemeler yüksek: ileri F/K 18,7, 10 yıllık getiri %4,84–4,90. 2010–2026 olağanüstü bir dönemdi (VA §4 madde 4).

| Kol / sürüm | CAGR (vergi öncesi USD) | Kötü yıl | MaxDD (döngü) | Belirsizlik |
|---|---|---|---|---|
| Çekirdek N25 tek başına | %8–12 | −%10…−%16 | −%25…−%45 | 1987 tipi gap'te −%35 |
| Uydu-R tek başına | Piyasa ± 4 puan | −%12…−%25 | −%30…−%50 | 2015+ %90 aralık [−7; +16] puan |
| Uydu-L (r = %0,25) | H'ye −%4…+%6 | – | Kol −%10…−%20 | Kanıtsız; taban oranlar kötü |
| **B-Standart toplam** | **%6–14, merkez ~%10** | −%5…−%10 | **−%20…−%35** | Yılların ~%15–20'si negatif |
| **B-Agresif toplam** | **%9–17, merkez ~%13** | −%8…−%15 | **−%30…−%45** | Yılların ~%20–25'i negatif |

**İlk 1–2 ay** (rejim SARI, çekirdek nakit, uydu ~%7–21): H büyük ölçüde nakit. Beklenen getiri −%2 ile +%3 arası. "Pazartesi büyük başlangıç" bu planda yok. Bu, kuralların sonucu.

### 8.3 Vergi sonrası: 50k / 250k / 1m $ örnekleri

**Varsayımlar:**
- Kur bir yılda +%20 (50,05 → 60,06; anket ve 2026 hızı; M §1.4).
- Yatırımda kalma oranı u = 0,6. Boştaki USD nakdin kur kazancı vergisiz.
- Veri gideri 1.200 $/yıl.
- 2026 tarifesi (doğrulanamadı); başka gelir yok; vergi ertelemesinin bugünkü değeri katılmadı (katılırsa sonuç biraz iyileşir; P §2.6).

**Hesap:** Vergi öncesi USD getirisi R'den vergi sonrası USD getirisine geçiş.

| R (vergi öncesi) | 50k $ (efektif vergi) | 250k $ | 1m $ |
|---|---|---|---|
| %0 | −%3,6 (%15,7) | −%2,9 (%26,5) | −%3,3 (%33,3) |
| %10 (B-Standart merkez) | **+%4,3** (%19,5) | **+%3,8** (%30,8) | **+%3,0** (%36,6) |
| %13 (B-Agresif merkez) | +%6,6 (%20,6) | +%5,9 (%31,3) | +%4,9 (%37,1) |
| %16 | +%8,8 | +%7,9 | +%6,8 |
| %25 (iyi yıl) | +%15,6 | +%14,0 | +%12,4 |
| %40 (çok iyi yıl) | +%25,9 | +%23,5 | +%21,8 |
| −%10 | −%12,4 | −%10,5 | −%10,2 |

**Okuma:**
1. **USD getirisi sıfır olsa bile vergi doğar.** Pozisyonların içindeki kur artışı TL kazancı sayılır. Bu planın en sert gerçeği (P §2.6, VC #22).
2. **USD kökenli sermaye:** B-Standart vergi sonrası %3–4; USD nakit vergi sonrası ~%2–3. Avantaj +1–2 puan; B-Agresif'te +2–4 puan. Küçük ama pozitif.
3. **TL kökenli sermaye:** TL'de kalmanın USD karşılığı %13–15,5 (kuyrukla %6–12). Bunu yakalamak için gereken vergi öncesi R: 50k'da %22–25, 250k'da %24–27, 1m'de %26–30. B-Standart'ın merkezi %10 olduğundan **beklenen açık yılda ~8–12 puan USD.**
   - Plan bu açığı yalnız şu durumlarda kapatır: R ≥ %25 olan bir yıl (backtest'te 12 aylık pencerelerin %9–19'u), TL şoku (d ≥ %45: yıllık ~%11–22 olasılık; VC #21) ya da lider kolunun sağ kuyruğu.
4. **Küçük hesap vergi açısından avantajlı:** 50k'da efektif oran ~%20, 1m'de ~%37. Veri maliyeti ise 50k'da dezavantaj.

### 8.4 Dürüst sonuç

- Plan B, ABD'de **kanıtı en uzun olan iki yapıyı** birleştiriyor: kapılı ve oynaklık ölçekli endeks betası, 12 aylık sektör momentumu. Bunun üstüne kanıtı zayıf ama sağ kuyruğu olan bir lider kolu ekliyor.
- Yüksek getiri ancak kaldıraçla gelir. Kaldıraç ise yalnız sakin yükselişlerde açılır. Bu, drawdown'u −%67'den (sabit 2x) −%25/−%45 aralığına çeker, ama CAGR'yi de %15'ten %10–14'e indirir.
- **Engel karşısında:** TL kökenli parada beklenen değer negatif. Plan ancak "USD çeşitlendirme + 12 aylık ileri test" olarak, servetin %15–25'iyle ve çekirdek sermayesi gerekene kadar TL'de bekletilerek savunulabilir.

---

## 9. Pazartesi 9.11.2026: tek sayfa kontrol listesi

**Hafta sonu (6–8.11)**
- [ ] Cuma kapanışından sonra §3.3 tablosunu yenile (NFP etkisi). SPX < 7.250 → KIRMIZI; aksi halde SARI beklenir. Ralli denemesi gün sayımını başlat (6.11 artı kapanış = 1. gün).
- [ ] Midas başvurusu ve onayı. IBKR Pro marj hesabı: izinler hisse/ETF/ABD vadeli; W-8BEN; VİOP tecrübesi beyanı. **IBKR kuruluşu ve ABD ETF erişimini yazılı sor.**
- [ ] Sermaye kararı (§1.3): TL kökenliyse hedef H = W'nin %20'si. **Şimdi H'nin %40'ı** taşınır (50k → 20k, 250k → 100k, 1m → 400k). Çekirdek payı TL'de, transfer tetiği "SPX 10 GHO > 20 GHO".
- [ ] TradingView: Ek B Pine (çekirdek rejimi), H §5a Pine Screener, ETF listesi (§2.3), küme izleme listeleri (§4.2).
- [ ] **12 aylık ETF sıralaması** (Perf % 1Y; 6.11 kapanışı): mutlak filtre, küme başına 1, ilk 3 küme, 50 GHO zamanlaması. Hangi dilimler açılıyor? Tahmin: yalnız sağlık (XLV).
- [ ] Lider izleme listesi (§4.4 "uygun" satırı): her isim için pivot, yapısal stop, ATR14, adet (r = %0,25), sonraki bilanço tarihi.
- [ ] R-defteri şablonu (§7.1) ve hipotez kartları (kol başına bir sayfa: kural, beklenen E[R], öldürme kriteri).

**Pazartesi 12:00–17:25 TSİ**
- [ ] SWIFT'i sabah, banka kesim saatinden önce gönder. TL→USD dönüşümünü önce küçük tutarla test et (makası ölç).
- [ ] Vadeli endekslere bak. **Çekirdek: işlem yok** (kapalı başlangıç).
- [ ] Hesap fonlandıysa: zamanlamayı geçen Uydu-R dilimleri için **MOO** emri, her biri H'nin %7'si (50k: 3,5k; 250k: 17,5k; 1m: 70k). 17:25'ten önce gir.
- [ ] Dolumdan sonra (seans içinde ya da gece) **GTC SELL STOP = dolum × 0,88.**
- [ ] **Lider emri yok** (FTD yok). Opsiyon yok. AI, nükleer, kuantum, kripto ve enerji kümelerinde işlem yok.

**Pazartesi gece (00:15–01:00 TSİ)**
- [ ] Rejim tablosu: SPX vs 7.396/7.250 (güncel eşikleri hesapla), 10 vs 20 GHO, σ̂, VIX, VIX/VIX3M, S5FI, S5TH, ralli günü.
- [ ] Toplam ısı ≤ %3? Küme ısısı ≤ %1,5? Deftere işle.

**Salı 10.11 (CPI 16:30)**
- [ ] 16:30'dan önce yeni emir yok. Gerekirse 16:45–17:25 arası MOO.
- [ ] FTD Salı gelemez (en erken Çarşamba).

**Hafta boyunca**
- [ ] Çarşamba ya da Perşembe kapanışında **FTD** (≥ +%1,25, hacim artışı, 4. gün ve sonrası) varsa ertesi gün en fazla **2 pilot:** farklı kümelerden, r = %0,25, BUY STOP LIMIT (pivot × 1,001 / × 1,015) + GTC stop (≤ min(%8; 1,5 ATR)). Bilançosu 10 gün içinde olan isim yok.
- [ ] Perşembe gece CSCO/AMAT, gelecek hafta NVDA (17.11 AMC, teyit) → AI kümesi kapalı kalır. Okumak serbest, işlem yok.
- [ ] Cuma 13.11 gece haftalık inceleme: bekleyen uydu dilimleri (Pazartesi 16.11 MOO), çekirdek transfer tetiği, aylık devre kesici (ilk 6 ay %4).

**Asla:** gün içi ekran işlemi, stop genişletme, kaybedene ekleme, 3x ürün, kırık kümede dip alımı, kurala aykırı çekirdek müdahalesi.

---

## Ek A. Bu planın kendi testleri (BT-B): yöntem, sınırlar, kod

**Veri:**
- Ken French günlük piyasa getirisi (Mkt-RF + RF; CRSP VW; temettü dahil), 1926-07 → 2026-09-30.
- Aylık 49 sektör VW ve firma sayıları.
- Yerel kopya: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/french/`, `.../data/dalga_abd/`.
- Okuyucular: `hesaplar/abd_test/ortak.py`, `hesaplar/dalga_abd/ff_load.py`. Rotasyon: `hesaplar/dalga_abd/kurallar.py::rotation`.
- Güncel seviyeler: FRED SP500 / NASDAQ100 (`.../data/fred_*.csv`) ve H snapshot'ı (5.11 kapanışı eklendi).

**Çekirdek motoru:**
- Fiyat endeksi: toplam getiri birikimi. abd_test ile aynı; küçük bir yanlılık var (T §1).
- Sinyal t kapanışında; pozisyon t+2 getirisini alır (lag1).
- L > 1 kısmının finansmanı rf + %0,5 (duyarlılıkta + %1,5). L < 1 kısmı rf kazanır.
- Maliyet: kaldıraç değişiminin her birimi için 5 bp. Ayar eşiği 0,25.
- CAGR takvim günüyle yıllıklandırıldı. VA'nın 1953 öncesi "gözlem/252" düzeltmesi uygulandı.
- σ̂ = max(RV20, RV60) × √252.

```python
g = latch(on=(px > 1.01*sma200) & (sma10 > sma20), off=(px < 0.99*sma200))
L_target = g * np.minimum(2.0, 0.25 / np.maximum(rv20, rv60))   # N25 (B-Agresif: 0.30)
L = rebalance_threshold(L_target, 0.25).shift(2)                 # lag1
r = L*mkt + (1-L).clip(lower=0)*rf - (L-1).clip(lower=0)*(rf + 0.005/252) - 0.0005*L.diff().abs()
```

**Denenen çekirdek varyantları** (hepsi raporlandı, seçim yanlılığına dikkat):

| Ad | Tanım |
|---|---|
| A, B | 1x ve 2x 200 GHO, bant %1 |
| C | VT15, tavan 2 |
| D, E | Kademeli tavan, VT15 ve VT12 |
| H, I, J | Kapı + 10/20 ve 50/200 koşullu 2x/1x/0,5x |
| K, L, M | VT20 ve VT25 |
| M0 | Bantsız kapı |
| N, N1, N2 | 10 > 20 giriş şartı; 1x ve 2x |
| N25, N30, N35 | Seçilen aile |
| Kıyas | 1x ve 2x al-tut |

Yaklaşık 20 varyant ve 3 duyarlılık (finansman, lag0, lag1) denendi.

**Uydu:** C_abs, C_abs + %15 trail, ≥ 10 firma şartı, ikisi birlikte (4 varyant).
**Kombinasyonlar:** 6 ağırlık, 1 merdiven testi.

**Sonucu tek cümleyle:** Hiçbir filtre Sharpe'ı belirgin artırmadı (1928+ SR 0,60–0,64 bandı). Filtreler esas olarak riski ölçekliyor; seçim bu yüzden "aynı riskte daha az drawdown" ölçütüyle yapıldı.

**Sınırlar:**
- Kod repoya yazılmadı (yalnız bu dosya yazılabiliyordu). Yukarıdaki parçalar ve ortak modüllerle yeniden üretilebilir.
- CRSP VW, S&P 500 değil.
- Vadeli roll ve teminat ayrıntısı modellenmedi.
- Vergi yok (§8.3 ayrı hesap).
- Lider kolu test edilemedi: hayatta kalma yanlılığından arınmış günlük hisse verisi yok (T §8).

## Ek B. TradingView Pine: çekirdek rejimi (sıfırdan başlangıçlı)

```pine
//@version=6
indicator("B_Cekirdek_Rejim", overlay=false)
startT = input.time(timestamp("09 Nov 2026 00:00 +0000"), "Sistem baslangici")
tgt    = input.float(0.25, "Vol hedefi (0.25 Standart / 0.30 Agresif)")
spx  = request.security("SP:SPX", "D", close)
m10  = ta.sma(spx, 10)
m20  = ta.sma(spx, 20)
m200 = ta.sma(spx, 200)
r    = math.log(spx / spx[1])
sig  = math.max(ta.stdev(r, 20), ta.stdev(r, 60)) * math.sqrt(252)
onSig  = spx > m200 * 1.01 and m10 > m20
offSig = spx < m200 * 0.99
var float gate = 0.0
gate := time < startT ? 0.0 : (onSig ? 1.0 : (offSig ? 0.0 : gate))
Lt = gate * math.min(2.0, tgt / sig)
plot(Lt,   "Hedef kaldirac L*")
plot(gate, "Kapi (1=acik)")
plot((spx / m200 - 1) * 100, "SPX - 200GHO (%)")
plot(m200 * 1.01, "Acilis esigi", display=display.data_window)
plot(m200 * 0.99, "Kapanis esigi", display=display.data_window)
plot(sig * 100, "sigma_hat (%)")
```

Fiili L, |L* − L| ≥ 0,25 olduğunda ya da L* = 0 olduğunda değişir (§2.1 madde 4). Betik sözdizimi bu oturumda TradingView'de çalıştırılmadı; ilk kullanımda grafikte kontrol edin.

## Ek C. Teyit listesi (doğrulanamayanlar)

1. IBKR'de Türk müşterinin bağlı olduğu kuruluş ve ABD ETF erişimi (PRIIPs).
2. Midas'ta SSO, stop-limit, GTC, MOO ve bracket desteği; kur makası.
3. MES çarpanı, teminatı ve komisyonu (CME ve IBKR sayfaları; bellek).
4. Yurt dışı vadeli kazancının TR vergi niteliği; MES'te kur farkının hangi tabana uygulandığı; T-bill anapara kur farkı.
5. 2026 gelir vergisi tarifesi (VC #11).
6. Kambiyo BSMV (binde 2).
7. NVDA bilanço tarihi: 17.11 (H, IR) mi, ~19.11 mi?
8. BRK-B, MDT ve BJ bilanço tarihleri.
9. S5FI ve S5TH güncel değerleri (önbellek verisi).
10. 12 aylık ETF getirileri: elimizde yok; §4.5 YTD ile yaklaşık.
11. UCITS ETF'lerin ABD veraset vergisine etkisi (bellek; uzman teyidi).
