# Koza göreli momentum (TRMET1! / TRALT1!) — uygulama rehberi

*Hazırlanma: 04.11.2026 (12:15 TSİ). Veri: VİOP bülteni 03.11.2026'ya kadar, Yahoo günlük 03.11.2026 kapanışına kadar. Yatırım tavsiyesi değildir.*

*Bağımsız denetim: 04.11.2026 (~13:00 TSİ). Sinyal ve pratik kural backtest'i ayrı kodla birebir yeniden üretildi; betikte 2 hata, Pine'da 1 sağlamlık sorunu düzeltildi; varyant tablosu kilit kuralına göre ayrıştırıldı. Ayrıntı §14.*

**Durum:** KOŞULLU. Güven: **DÜŞÜK**. 2019–2026'da istatistiksel olarak anlamlı. Ama son 3 yılda maliyet sonrası kenar sıfıra yakın, 2026 negatif. Küçük boyutla ve kuralı bozmadan uygulanmalı.

---

## 0. Kısaca

- **Sinyal:** TRMET'in son 3 gündeki grup-göreli artığı. Grup = TRALT ile TRENJ'in ortalaması.
- **İşlem:** Artık eşiği aşınca aynı yönde işlem açılır. z3 > +1,5 ise TRMET1! AL ve yaklaşık 2 katı adet TRALT1! SAT. z3 < −1,5 ise tersi.
- **Süre ve fiyat:** Giriş ve çıkış VİOP uzlaşma fiyatına yakın yapılır (18:00–18:10). Pozisyon 2 iş günü tutulur. Sinyal aynı yönde sürüyorsa 2'şer gün uzatılır, en fazla 6 gün.
- **Klasik lead-lag DEĞİL.** TRALT bugün yükselince TRMET ertesi gün yükselmiyor, tersi de olmuyor (bkz. §9.5). Kazanç TRMET'in kendi göreli hareketinin 1–4 gün devam etmesinden geliyor. TRALT bacağı "takipçi" değil, hedge. Kazancın bir kısmı da VİOP uzlaşma fiyatının spot kapanışı geç izlemesinden geliyor.

---

## 1. Kesin kural

### 1.1 Sinyal (araştırma `c2_koza.py` ile birebir aynı)

Her BIST günü t'nin kapanışında hesaplanır.

| Adım | Tanım |
|---|---|
| Getiri | Günlük log getiri r. Yahoo `adj` (temettü + bölünme düzeltmeli). |
| Bayat gün | Hacim ≤ 0 ya da yüksek = düşük ise fiyat yok sayılır. Ertesi günün getirisi son geçerli fiyata göre hesaplanır. |
| Veri hatası | \|r\| günlük limiti aşarsa NaN. Limit: 13.03.2020 sonrası %10,5, öncesi %20,5. |
| grp | ort(r_TRALT, r_TRENJ). Biri eksikse NaN. |
| β_g | 250 günlük cov(r_TRMET, grp) / var(grp). En az 120 gözlem. **Dünkü bilgiye kadar** (shift 1). [0,2; 2,0] aralığına kırpılır. |
| u | r_TRMET − β_g · grp |
| z3 | (u_t + u_t−1 + u_t−2) / (σ60(u) · √3). σ60 için en az 40 gözlem gerekir. |
| β_TA | 250 günlük β(r_TRMET, r_TRALT), shift 1, [0,3; 2,0]. Hedge oranıdır. |

Son değerler: β_g 0,88, β_TA 0,69, σ60 ≈ 194 bps. Eşik ±1,5 olduğu için 3 günlük toplam artık yaklaşık ±505 bps olmalı.

### 1.2 Pratik işlem kuralı (örtüşmesiz; backtest'i §9.2)

1. **Pozisyon yokken |z3| > 1,5 ise gir.**
   - z3 > +1,5: TRMET1! AL + TRALT1! SAT.
   - z3 < −1,5: TRMET1! SAT + TRALT1! AL.
   - Oran: TRALT nominali = β_TA × TRMET nominali. Kontrat oranı ≈ β_TA × P_TRMET / P_TRALT; bugün **1 TRMET1! : 2 TRALT1!**.
2. **Giriş fiyatı:** t günü VİOP uzlaşma fiyatı. Pratikte 18:00–18:10 arasında, uzlaşmaya yakın doldurulur.
3. **Planlanan çıkış:** t+2 iş günü uzlaşması.
4. **Çıkış gününde z3'ü yeniden hesapla:**
   - **Aynı yönde hâlâ \|z3\| > 1,5** ise 2 iş günü uzat. Toplam tutma en fazla 6 iş günü.
   - **Ters yönde \|z3\| > 1,5** ise çık ve aynı uzlaşmada ters pozisyonu aç.
   - **Sinyal yoksa** çık.
5. **6 gün dolduğunda** sinyal hâlâ aynı yöndeyse çık. Aynı yöne yeniden girmek için önce z3'ün bant içine (\|z3\| ≤ 1,5) dönmesini bekle.
6. **Ara günlerde** (t+1, t+3, t+5) çıkan sinyaller yok sayılır. Pozisyon büyütülmez.
7. **Kilit günü girilmez.** Giriş günü TRMET1! ya da TRALT1! günlük fiyat limitine (±%10) dayanmış ve kilitliyse o gün girme. Ertesi gün sinyal hâlâ aktifse gir. Backtest vekili: ön vade uzlaşma değişimi \|r\| > %9,5.
8. **Vade:** Vadesi planlanan çıkış gününden **sonra** olan en yakın vade seçilir (§6). Uzatmada vade yetmiyorsa devredilir.

---

## 2. Saat saat uygulama

Her işlem günü aynı akış izlenir. Arife (yarım gün) günlerinde aynı adımlar seans sonundan 15–20 dk önceye kaydırılır.

| Saat (TSİ) | Ne yapılır |
|---|---|
| **Sabah 09:30–10:00** | KAP'ta TRMET, TRALT ve TRENJ haberlerine bak: TVF/satış, birleşme, temettü, bedelsiz, tedbir, endeks değişikliği. Önemli kurumsal olay varsa **o gün yeni pozisyon açma** (§8). Açık pozisyon varsa planlanan çıkış gününü not et. Gece betiği çalıştırdıysan dünkü sinyal ve durum hazırdır. |
| **Gün içi** | İşlem yok. İstersen TradingView göstergesinde canlı z3'ü izle (15 dk gecikmeli). |
| **17:45** | Aracı kurum ekranından TRMET, TRALT ve TRENJ **spot** son fiyatlarını al. TRMET1! ve TRALT1! ön vade fiyatlarını da al. Hangisinin limite yakın olduğunu kontrol et. |
| **17:50–17:55** | `python3 sinyal_koza.py --canli TRMET=.. TRALT=.. TRENJ=.. --vadeli TRMET=.. TRALT=.. --sermaye ..` çalıştır. Betik z3'ü, yönü, kontrat adetlerini ve açık pozisyon durumunu yazar. Canlı ekran yoksa TV'nin 15 dk gecikmeli fiyatıyla (≈17:40) hesapla (fark §9.4). **Bir gün beklemek çok daha pahalı.** |
| **18:00–18:10** | Karar varsa her iki bacağı bu aralıkta, uzlaşma penceresinde doldur. Emri 2–3 parçaya böl (ör. 18:01, 18:05, 18:08). Önce daha az likit TRMET1! bacağını, hemen ardından TRALT1! bacağını gir. Limitli emri en iyi alış/satışa koy. Bir bacak dolmazsa diğerini de azalt; tek bacakla gece taşıma. Çıkış ve uzatma günlerinde de çıkış aynı pencerede yapılır. *İsteğe bağlı:* Spot kapanış seansı fiyatı ~18:05'te oluşur. Canlı ekranın varsa son parçadan önce (18:06–18:08) z3'ü kapanış fiyatıyla bir kez daha hesapla; sinyal kaybolduysa kalan parçayı girme. Bu, backtest'in kapanış varsayımına daha yakındır (seans saatlerini aracı kurumdan teyit et). |
| **Akşam (≥ 18:30)** | Betiği `--canli` olmadan çalıştır. Kapanışla kesinleşen z3, 17:55'teki z3'ten çok az farklı olabilir. Pozisyon zaten açılmışsa bu fark kuralı değiştirmez. Yahoo BIST verisi ~15 dk gecikmeli olduğu için betik bugünün barını **18:30'dan önce** kullanmaz (denetimde 18:15'ten düzeltildi). |
| **t+1** | Hiçbir şey yapma. Yeni sinyal yok sayılır. |
| **t+2 (çıkış günü) 17:50** | z3'ü yeniden hesapla. Aynı yönde > 1,5 ise uzat (çıkma). Değilse 18:00–18:10'da çık. Ters sinyal varsa çıkıp ters pozisyonu aç. |
| **t+4 / t+6** | Uzatıldıysa aynı kontrol yapılır. 6. günde koşulsuz çık. |

**Yapılmayacaklar**

- Sinyali ertesi sabah açılışta uygulamak. Kenarın büyük kısmı uzlaşma penceresinde oluşuyor.
- Tek bacak (yalnız TRMET1!) taşımak. Varyans 2 katına çıkar; bu kural için test edilmedi.
- Zarardaki pozisyona ekleme yapmak.
- Eşiği ya da süreyi "son dönemde daha iyi" görünen değere çekmek (ör. h3, eşik 2,0). §9.3'teki varyantlar yalnız bilgi içindir.
- Pozisyon açıkken ara gün sinyaline göre pozisyonu büyütmek.

---

## 3. Kontrat sayısı (1 mn TL sermaye)

Kuralın işlem başı brüt getiri standart sapması σ ≈ **%2,05**. Brüt nominal G aşağıdaki gibi hesaplanır:

G = sermaye × risk / σ ; TRMET nominali = G / (1 + β_TA) ; TRALT nominali = β_TA × TRMET nominali.

Bugünkü fiyatlar: TRMET1! 102,35, TRALT1! 34,94 (03.11 uzlaşma), β_TA 0,69, 1 kontrat = 100 pay.

| Risk / işlem | G (brüt nominal) | TRMET1! | TRALT1! | Teminat (~%15, iki bacak) | 1σ işlem | En kötü geçmiş işlem (−463 bps) |
|---|---|---|---|---|---|---|
| %0,5 | 243.902 TL | 14 adet (143.290 TL) | 28 adet (97.832 TL) | ≈ 36.000 TL | ±5.000 TL | ≈ −11.300 TL |
| %0,75 (betik varsayılanı) | 365.854 TL | 21 adet (214.935 TL) | 42 adet (146.748 TL) | ≈ 54.000 TL | ±7.500 TL | ≈ −16.900 TL |
| %1 | 487.805 TL | 28 adet (286.580 TL) | 57 adet (199.158 TL) | ≈ 73.000 TL | ±10.000 TL | ≈ −22.600 TL |

- Teminat oranı Takasbank'a göre pay vadelisinde ~%13–17. Tabloda netleştirme yok; aracı kurumun gerçek teminatına bakın.
- Kaldıracı 1× brüt nominalin üstüne çıkarmayın (betikte `--kaldirac` varsayılanı 1,0).
- TRMET1! B sınıfı likidite (12 ay medyan ~392 mn TL/gün). 200–300 bin TL'lik bacak uzlaşma penceresinde dolabilir. 1 mn TL üstü emirde etki ~25 bps.
- **Beklenti (gerçekçi):** %0,75 riskte net15+tik ≈ +28,8 bps/işlem, yani ≈ +1.050 TL/işlem. Yılda ~18 işlemle ≈ +19.000 TL/yıl (sermayenin ~%1,9'u). Tarihsel maks düşüş −791 bps × G ≈ −29.000 TL. 2024–26'da net beklenti ≈ 0.

---

## 4. Örnek işlemler (gerçek VİOP uzlaşmalarıyla, %0,75 risk)

**Örnek 1 — 23.09.2026, uzatmasız, kazanç**

- **22.09:** z3 +0,91. TRMET +%6,3; TRALT −%2,2; TRENJ +%0,8.
- **23.09 kapanış:** z3 = **+2,40**. Sinyal: TRMET1! AL / TRALT1! SAT; β_TA 0,65.
- **Vade seçimi:** Planlanan çıkış 25.09. Eylül vadesi 30.09 > 25.09, uygun.
- **Giriş (23.09 uzlaşma):** TRMET0926 140,00 / TRALT0926 50,43.
  - Adet: 365.854 / 1,65 = 221.400 TL → **16 TRMET1!**.
  - 0,65 × 16 × 140,00 / 50,43 → **29 TRALT1!**.
- **24.09:** z3 +3,18 ama pozisyondayız; yok sayılır.
- **25.09 (çıkış günü) 17:50:** z3 +0,76. Sinyal sönmüş, 18:00–18:10'da çık.
- **Çıkış (25.09 uzlaşma):** 140,45 / 49,85.
  - TRMET: 16 × 100 × (+0,45) = +720 TL.
  - TRALT (açığa): 29 × 100 × (50,43 − 49,85) = +1.682 TL.
  - **Brüt +2.402 TL (+65 bps).** Maliyet ~%0,17 (≈ 650 TL) sonrası ≈ +1.750 TL.

**Örnek 2 — 24.07.2026, uzatmalı, kayıp (kural her zaman kazanmaz)**

- **23.07:** z3 +2,51, ama TRMET o gün limitte (kilit vekili) → girilmedi.
- **24.07:** z3 +3,31 → giriş. TRMET0726 136,90 / TRALT0726 49,36; β 0,65; 16 + 29 adet.
- **28.07 (çıkış günü):** z3 +1,72, hâlâ > 1,5 → 30.07'ye uzatıldı. Temmuz vadesi 31.07 > 30.07, devir yok.
- **30.07:** z3 −0,12 → çıkış. 128,25 / 46,08.
  - TRMET −13.840 TL; TRALT +9.512 TL.
  - **Brüt ≈ −4.330 TL (−126 bps).**

---

## 5. Uzatma neden var?

- **İlk 2 günlük bölüm:** ortalama +26,7 bps.
- **Uzatma kararından sonraki 2 günlük bölümler:** +76,6 bps (t 3,07, n 46, isabet %70). Karar anında bilinen bilgiyle alındığı için ileriye bakma yok. 2024+'da bu bölümler +23,3 bps (n 16).
- **Uzatılmayan işlemler** ortalamada −12,8 bps. Kazanç, sinyali süren (momentumu devam eden) işlemlerden geliyor. Bu yüzden "küçük kâr görünce erken çık" yapılmamalı.

---

## 6. Vade devri

- **Pay vadelisi vade sonu:** ayın son iş günü.
- **Seçim kuralı:** Vade > planlanan çıkış günü (kesin büyük) olan en yakın vade.
  - Örnek: 26.11.2026 Perşembe giriş, çıkış 30.11 Pazartesi. Kasım vadesi 30.11'de bitiyor (30.11 > 30.11 değil) → **Aralık vadesi**.
- **TradingView:** `BIST:TRMET1!` sürekli ön vadedir. Belirli vade için tv_final notundaki biçim kullanılır: örn. `BIST:TRMETZ2026` (Aralık 2026). Diğer ay harflerini TV arama kutusunda kontrol edin.
- **Likidite:** Hacim vade gününe kadar ön vadede kalıyor (ön vade payı ~%85). Vadeye 1–2 gün kala sonraki vade daha sığ olur. Bu günlerde emri daha da bölün.
- **Uzatmada vade bitiyorsa:** Mevcut vade yeni çıkış gününden önce ya da o gün bitiyorsa, uzatma gününün uzlaşma penceresinde bir sonraki vadeye devret. İki bacak birlikte devredilir.
  - Ek maliyet = 1 gidiş-dönüş.
  - Backtest'te 141 işlemde 8 devir oldu; maliyetleri hesaba katıldı.
- **Bedelsiz / temettü:** Bu günlerde VİOP sözleşmesi düzeltilir (N1 kodu). Spot sinyali Yahoo `adj` ile düzeltilir; TradingView kapanışı temettüye göre düzeltilmez (§10).

---

## 7. Limit ve kilit günleri

- **Pay vadelisi günlük limiti ±%10.** 13.03.2020 öncesinde ±%20'ydi.
- **Kilit günü giriş yok.** Sinyal günü vadeli bacak limitte kilitliyse (alıcısız taban / satıcısız tavan) giriş yapılamaz. Ertesi gün sinyal hâlâ aktifse girilir. Backtest'te bu kural (P0L) ortalamayı +57,9'dan **+51,7 bps**'e düşürür; kilit günlerinde dolum varsayan P0 iyimserdir.
- **Bayat spot günü:** Spot o gün bütünüyle limitte kilitliyse (yüksek = düşük) o günün getirisi NaN olur ve z3 hesaplanamaz. Betik "SİNYAL YOK" yazar.
- **Pozisyon açıkken limit:** Bacaklardan biri aleyhe limite kilitlenirse çıkış ertesi güne kayabilir. Bu risk backtest'e yansımadı (uzlaşma fiyatıyla çıkış varsayıldı).
- **Bugünkü durum (04.11 gün içi, 12:36 Yahoo):** TRMET spot +%9,5 (109,50), tavan 110,00. Grubun bugünkü hareketiyle z3'ün +1,5'i geçmesi için TRMET'in ≈ 109,6 üstünde kapanması gerekiyor. Bu fiyat zaten tavana %0,4 uzaklıkta. Yani bugün sinyal oluşursa büyük olasılıkla bacaklar limitte ya da limite çok yakın olacak. TRMET1! tavanı ≈ 112,6 (03.11 uzlaşması 102,35 × 1,10). Kilitliyse girilmez. Kilit kontrolü 17:45'te yapılmalı.

---

## 8. Ne zaman yapılmaz

- **Kurumsal olaylar.** TRMET, TRALT ya da TRENJ'de önemli kurumsal olay günü ve ertesi günü. Örnekler: TVF satış/devir duyurusu, birleşme ya da iptal, sermaye artırımı, temettü/bedelsiz hak kullanımı, tedbir kararı. Momentum bu günlerde olayın kendisidir ve tersine dönebilir.
- **Eksik veri.** z3 hesaplanamıyorsa: TRENJ işlem görmediyse ya da bir hisse bütün gün limitteyse.
- **Bacak dolmuyorsa.** Tek bacakla kalınmaz.
- **Endeks dönemleri.** BIST 30/100 endeks dönemi değişikliği ve uzlaşmanın kayabileceği vade sonu günleri. Bu günlerde girilecekse vade kuralına özellikle dikkat edin.
- **Bütçe aşımı.** Sermaye/teminat 2 bacağı birlikte taşımaya yetmiyorsa.
- **Düşüş sınırı.** Kümülatif düşüş −800 bps'i aşarsa (geçmiş en kötü −791) stratejiyi durdurup yeniden değerlendirin. 2026'da kural şimdiye kadar −458 bps (net15+tik toplam).

---

## 9. Sonuçlar

### 9.1 Araştırmanın yeniden üretimi (birebir)

`kod/k1_repro.py`; araştırma önbelleği ve önbelleksiz `curlib.Fut` yeniden hesabı aynı sonucu veriyor.

| Kural (örtüşen; her sinyal günü bir işlem) | n | brüt bps | t |
|---|---|---|---|
| E0 h2 (t uzlaşmasında giriş) | 283 | **+44,6** | **4,05** |
| E1 h2 (son işlem fiyatı) | 283 | +42,1 | 3,77 |
| E2 h2 (t+1 uzlaşmasında giriş) | 283 | **+29,9** | **2,59** |
| E0 h2, 2024–26 | — | +21,1 | 1,21 |
| E0 h2, en iyi 10 hariç | — | +29,9 | 3,11 |
| Bağımsız olay sayısı | **120** | — | — |
| TERS (TRALT artığı), E0 h2 | 269 | +33,0 | 2,52 |
| TERS (TRALT artığı), E2 h2 | 269 | +18,8 | 1,50 |

Taze Yahoo verisiyle hesaplanan z3 araştırmanınkiyle aynı (maks fark 7·10⁻⁶; sinyal uyumu %100).

### 9.2 Pratik kural (P0L) — VİOP uzlaşma fiyatlarıyla, 2019-01 → 2026-11-03

`kod/k2_pratik.py`, işlem listesi `kod/islemler_P0L.csv`. Maliyet brüt sermaye başına gidiş-dönüş: 8 ya da 15 bps. "+tik" = bacak ve yön başına 1 fiyat adımı (0,01 TL; ortalama 7,0 bps, 2024+ 4,8 bps). Vade devrinde maliyet tekrarlanır.

| Ölçü | Değer |
|---|---|
| İşlem sayısı | 141 (18,3/yıl), ort. tutma 2,65 gün, %27'si uzatıldı, piyasada zaman %19 |
| Brüt / işlem | **+51,7 bps** (t 3,00), isabet %57, σ 205 bps |
| net8 / net15 | +43,2 / +35,8 |
| net8+tik / net15+tik | +36,2 / **+28,8** |
| IS 2019–21 / OOS 2022–26 | +61,0 (t 2,40, n 49) / +46,7 (t 2,05, n 92) |
| **2024–26** | **+21,7 (t 0,93, n 52); net15+tik +1,0** |
| En iyi 10 işlem hariç | +10,2 (t 0,87): kazanç büyük kazananlara yığılı |
| En kötü / en iyi işlem | −463 bps (09.01.2023) / +985 bps |
| Maks düşüş (işlem toplamı) | −763 bps (net8) / −791 bps (net15+tik); 22.12.2022 → 09.01.2023 |
| En uzun kayıp serisi | 4 işlem |
| 1 çift (1 TRMET1! + 2 TRALT1! ≈ 17.200 TL) | brüt +89 TL, net15+tik +50 TL / işlem; ≈ +900 TL / yıl / çift |

Yıllar (brüt bps / net15+tik bps, işlem sayısı):

| Yıl | Brüt | Net15+tik | n |
|---|---|---|---|
| 2019 | +104 | +74 | 15 |
| 2020 | +26 | +1 | 18 |
| 2021 | +60 | +37 | 16 |
| 2022 | +59 | +38 | 20 |
| 2023 | +99 | +77 | 20 |
| 2024 | +50 | +28 | 18 |
| 2025 | +23 | +1 | 18 |
| **2026** | **−11** | **−29** | 16 |

Brüt 7/8 yıl pozitif. Etki 2023'ten beri belirgin biçimde küçülüyor.

### 9.3 Varyantlar (yalnız bilgi; seçim için değil)

**Denetim notu:** Kurucunun ilk tablosunda P1, P1b, P2, P2b ve TERS satırları **kilit kuralı olmadan** hesaplanmıştı. Bu yüzden P0L ile değil P0 ile karşılaştırılmalılar. Aşağıda iki sürüm de var. Sayılar denetimin bağımsız koduyla birebir tekrarlandı (`kod/denetim/`).

| Varyant | Kilit kuralı | n | brüt | t | net15+tik | 2024–26 brüt (t) | en iyi 10 hariç |
|---|---|---|---|---|---|---|---|
| P0: uzatmalı | yok (iyimser) | 143 | +57,9 | 3,40 | +35,0 | +30,5 (1,34) | +17,5 |
| **P0L: ana pratik kural** | **var** | **141** | **+51,7** | **3,00** | **+28,8** | +21,7 (0,93) | +10,2 |
| P1: sabit h2, uzatmasız | yok | 145 | +33,4 | 2,94 | +11,7 | +22,9 (1,15) | +13,2 |
| P1L: sabit h2, uzatmasız | var | 143 | +25,2 | 2,22 | +3,4 | +13,8 (0,70) | +4,2 |
| P1b: sabit h3, uzatmasız | yok | 142 | +47,2 | 2,99 | +25,5 | +42,5 (1,70) | +17,7 |
| P1bL: sabit h3, uzatmasız | var | 141 | +40,5 | 2,52 | +18,7 | +28,2 (1,11) | +10,1 |
| **P2: GECİKMELİ** (dünkü kapanış sinyali, bugün uzlaşmada giriş) | yok | 143 | +38,8 | 2,30 | +15,8 | +26,8 (1,15) | +4,8 |
| P2L: gecikmeli, uzatmalı | var | 141 | +38,8 | 2,35 | +16,0 | +23,7 (1,05) | +6,1 |
| P2b: gecikmeli, sabit h2 | yok | 145 | +22,9 | 1,67 | +1,1 | +20,7 (0,94) | −0,5 |
| P2bL: gecikmeli, sabit h2 | var | 143 | +24,2 | 1,83 | +2,4 | +17,3 (0,80) | +2,5 |
| TERS P0 (TRALT artığı, TRALT1! − β·TRMET1!) | yok | 128 | +47,4 | 2,37 | +25,2 | +34,5 (0,91) | +0,3 |
| **TERS P0L** | var | 130 | **+30,4** | **1,83** | +8,2 | +15,8 (0,53) | −4,7 |
| TERS P2 (gecikmeli) | yok | 128 | +19,9 | 1,16 | −2,3 | +20,1 (0,64) | −17,8 |

- **Yol bağımlılığı:** Kilit kuralı yalnız 2–3 girişi bir gün kaydırıyor. Ama sonraki işlem dizisi değiştiği için ortalama 6–17 bps oynuyor (P1 −8, TERS −17). İşlem başı standart hata ≈ 17 bps (σ 205 / √141). Tek tek varyant farklarını sinyal saymayın.
- **TERS kural uygulanmaz.** Kilit kuralıyla brüt +30,4 (t 1,83), en iyi 10 hariç negatif. Gecikmeli girişte de kayboluyor.

#### 9.3b Parametre duyarlılığı (denetim; P0L kilit kuralıyla, 2019-01 → 2026-11-03)

Uzatmalı sürümde aynı yönde sinyal sürerse +h gün uzatılır, en fazla 3h gün. Sabit sürümde uzatma yok.

| Eşik | Tutma | Uzatmalı: n / brüt (t) / net15+tik / 2024–26 brüt | Sabit: brüt (t) / net15+tik |
|---|---|---|---|
| 1,25 | h1 | 207 / +40,7 (3,79) / +18,4 / +40,5 | +24,1 (3,41) / +2,3 |
| 1,25 | h2 | 196 / +50,6 (3,50) / +27,9 / +35,4 | +27,5 (2,84) / +5,8 |
| 1,25 | h3 | 189 / +51,4 (3,27) / +28,3 / +69,7 | +39,0 (2,95) / +17,2 |
| 1,50 | h1 | 149 / +38,9 (3,06) / +16,9 / +26,8 | +22,8 (2,76) / +1,1 |
| **1,50** | **h2** | **141 / +51,7 (3,00) / +28,8 / +21,7** | +25,2 (2,22) / +3,4 |
| 1,50 | h3 | 141 / +46,7 (2,65) / +24,5 / +30,7 | +40,5 (2,52) / +18,7 |
| 1,75 | h1 | 97 / +43,0 (2,73) / +20,8 / +67,6 | +15,5 (1,57) / −6,3 |
| 1,75 | h2 | 93 / +48,4 (2,35) / +25,9 / +56,9 | +24,1 (1,65) / +2,3 |
| 1,75 | h3 | 93 / +54,9 (2,50) / +32,4 / +62,4 | +54,6 (2,58) / +32,7 |

**Okuma:**
- Uzatmalı sürüm eşik ±0,25 ve h 1–3 arasında brüt +39…+55 bps bandında, t 2,3–3,8. Ana kural en iyi ya da en kötü köşe değil.
- Sabit tutmada (uzatmasız) maliyet sonrası çoğu hücre ≈ 0. **Kenarın çoğu "süren sinyalde tutmaya devam et" kuralından geliyor.**
- Eşik 1,75'te en iyi 10 işlem çıkınca ortalama ≈ 0 (h2 −0,4). Daha seçici eşik kazancı daha da az işleme yığıyor.
- 2024–26 hücreleri +14…+70 arasında oynuyor (n 50–70). Buradan parametre seçmeyin; ana kural (1,5 / h2 / uzatmalı) önceden belirlendi ve öyle kalmalı.

- **TERS kural uygulanmaz.** E0'da var gibi, ama gecikmeli girişte ve en iyi 10 işlem çıkınca kayboluyor.
- **XU030 hedge'li varyant** (araştırma): TRMET1! − β·XU030D1!, örtüşen E0 h2 +50,5 (t 3,46). Pratik kural olarak test edilmedi.

### 9.4 Sinyal kapanış yerine 17:30–17:55 fiyatıyla hesaplanırsa

`kod/k4_1755.py`. Yalnız bugünün getirisi değişir; önceki günler tam kapanışla bilinir.

| Ölçüm | Sonuç |
|---|---|
| m5 penceresi (12.08–03.11.2026, 58 gün): 17:40 / 17:50 / 17:55 fiyatıyla z3 | Kapanış z3'üyle korelasyon 0,972 / 0,982 / 0,986. Sinyal günü uyumu %100: pencerede 2 sinyal günü, 1 işlem; ikisi de aynı. |
| h1 penceresi (25.11.2025–03.11.2026, 232 gün): 17:30 fiyatı | Gün uyumu %94. 26 kapanış sinyalinin 9'u 17:30'da yok, 5 yeni sinyal var, ters yön 0. İşlem: 17 (kapanış) / 15 (17:30), 11 ortak. |
| **Tam geçmiş Monte Carlo** (P0L, 300 tekrar) | **17:55 fiyatı:** brüt +47,8 (%5–95: +39,3…+57,5), t ≈ 2,8, net15+tik +25,2. **17:40 (TV 15 dk gecikmeli):** +48,1, net15+tik +25,4. Kapanış tabanı: +51,7 / +28,8. |
| **Fark** | ≈ **−4 bps/işlem**. Karşılaştırma: bir gün beklemenin (P2) maliyeti ≈ −19 bps (ikisi de kilit kuralsız: P0 +57,9 → P2 +38,8). |

- **Monte Carlo varsayımı:** Kapanış müzayedesi hareketinin ileri getiriden bağımsız olduğu varsayılır. Ama pencerede ε_u ile ileri 2 günlük çift getirisi arasında +0,12 korelasyon var (n 58; zayıf). Gerçek fark −4 bps'ten biraz büyük olabilir.
- **Öneri:** 17:50–17:55'te canlı fiyatla hesapla. Canlı fiyat yoksa TV'nin gecikmeli fiyatıyla yine 17:55'te hesapla. Ertesi güne bırakma.

### 9.5 TRALT ↔ TRMET lead-lag var mı? (günlük, `kod/k3_leadlag.py`)

Regresyon: y_t ~ x_{t−1..3} + y_{t−1..3} + XU030_{t−1..3}, NW(5) t. Ayrıca XU030'dan arındırılmış getirilerle tekrarlandı.

| Soru | 2011–16 | 2017–21 | 2022–26 | 2024–26 |
|---|---|---|---|---|
| TRALT(t−1) → TRMET(t), b1 (t) | **+0,13 (2,9)** | −0,05 (−0,9) | −0,13 (−2,4) | −0,14 (−2,2) |
| TRALT(t−2) → TRMET(t), b2 (t) | +0,05 (1,1) | +0,08 (1,5) | +0,09 (1,5) | +0,21 (3,0) |
| TRALT(t−3) → TRMET(t), b3 (t) | +0,05 (1,2) | +0,03 (0,6) | −0,10 (−2,0) | −0,14 (−2,3) |
| TRMET(t−1) → TRALT(t), b1 (t) | −0,03 (−0,9) | −0,01 (−0,3) | −0,01 (−0,1) | +0,04 (0,6) |
| Eşzamanlı korelasyon | 0,64 | 0,74 | 0,81 | 0,77 |
| Yayılım öz-korelasyonu lag1, spot kapanış | 0,07 | 0,03 | 0,09 | 0,06 |
| Yayılım öz-korelasyonu lag1, VİOP uzlaşma | — | 0,05 | **0,14** | 0,14 |
| corr(VİOP yayılımı t+1, spot yayılımı t) | — | 0,08 | **0,15** | 0,14 |

**Okuma:**
- **2017'den beri klasik lead-lag yok.** Ne TRALT'tan TRMET'e ne de TRMET'ten TRALT'a tutarlı, aynı işaretli 1–3 gün öncülük var. Eski KOZAL → KOZAA öncülüğü (2011–16, t 2,9) 2017'de kayboldu. 2022–26'da TRALT(t−1) → TRMET katsayısı **negatif** (−0,13, t −2,4), lag-3 de negatif (−0,10, t −2,0), lag-2 pozitif (+0,09). Üç lag'ın toplamı −0,14. Yani TRALT'ın yükselişini TRMET ertesi günlerde izlemiyor; varsa zayıf bir ters ilişki var ve işareti dönemden döneme değişiyor (2017–21 toplamı +0,05). Denetim aynı regresyonu bağımsız kodla birebir buldu.
- **Sinyal günlerinde kazanç TRMET'ten.** Yön uygulanmış 2 günlük VİOP getirileri: TRMET1! +86 bps, TRALT1! +1,6 bps, XU030 −15. TRALT bacağı hareket etmiyor; TRMET kendi göreli hareketini sürdürüyor. TRMET'in yalnız XU030'a göre artığı da aynı şeyi veriyor: h2 +88 bps, t 3,0. Yani bu, **TRMET'e özgü kısa vadeli momentum**.
- **Zamanlama payı var.** VİOP uzlaşma yayılımının öz-korelasyonu (0,14) spot kapanışınkinden (0,09) yüksek. TRMET kartında da SSF uzlaşması kapanış müzayedesi hareketinin yalnız ~%41'ini izliyor. Kenarın bir kısmı, uzlaşmanın spot kapanışı ertesi gün yakalamasından geliyor. E0 (+44,6) ile E2 (+29,9) arasındaki fark bununla tutarlı. E2/P2'de kalan pozitif kısım gerçek devamdır.

---

## 10. Güncel durum

| | |
|---|---|
| Son kapanış | **03.11.2026**: TRMET 100,00 · TRALT 34,18 · TRENJ 69,05 |
| u_t / Σ3u / σ60 | +140 / +163 / 194 bps |
| **z3** | **+0,49** → **sinyal yok** |
| Kurala göre pozisyon | **Yok.** Son işlem 23–25.09.2026 (+65 bps). TERS z3 +0,33 (sinyal yok). |
| **04.11 kapanışı için tetik** | AL: u ≥ **+175 bps**; TRALT ve TRENJ yatay kalırsa TRMET kapanışı ≥ **101,76**. SAT: u ≤ **−835 bps**; TRMET ≤ **91,99**. |
| **04.11 gün içi (11:57, sinyal değil)** | TRMET 108,10 (+%7,8 log), TRALT 36,78, TRENJ 73,25 → u ≈ +196 bps, **z3 ≈ +1,55**. Eşiğin hemen üstünde. 17:50'de yeniden hesaplanmalı. |
| **04.11 gün içi (12:36, denetim; sinyal değil)** | TRMET 109,50 (+%9,5), TRALT 37,32, TRENJ 74,80 → u ≈ +168 bps, **z3 ≈ +1,48** (betik ve bağımsız kod aynı). Eşiğin hemen altında. Grup bu düzeyde kalırsa TRMET 109 → z3 +1,34; 110 (tavan) → +1,60. |
| Sinyal + kilit birlikte | Bugün sinyal ancak TRMET tavana çok yakınken oluşabiliyor. TRMET1! (tavan ≈ 112,6) ya da TRALT1! limitte kilitliyse kural gereği **girme**. Kilitli değilse ve 17:50'de z3 > +1,5 ise giriş, planlanan çıkış 06.11. |
| 04.11 kapanışında olası işlem | z3 > 1,5 kalır ve TRMET1!/TRALT1! limitte kilitli değilse TRMET1! AL / TRALT1! SAT. Örnek: 21 + 42 adet (%0,75 risk). Planlanan çıkış 06.11 uzlaşması. |
| Gün içi kilit riski | TRMET spot 12:36'da +%9,5 (tavan 110,00); limit kilidi riski yüksek. |

---

## 11. TradingView: izlenecek kodlar

Yalnız `tv_final.csv`'de doğrulanmış kodlar.

| Kod | Rol | Neden |
|---|---|---|
| `BIST:TRMET` | sinyal girdisi | u'nun hedefi (spot kapanış) |
| `BIST:TRALT` | sinyal girdisi | Grup ortalaması ve hedge betası (β_TA) |
| `BIST:TRENJ` | sinyal girdisi | Grup ortalaması (vadelisi yok) |
| `BIST:TRMET1!` | işlem aracı | Uzun/kısa bacak; limit kontrolü. 15 dk gecikmeli, akşam seansı yok. Vade kodu biçimi örn. `BIST:TRMETZ2026` |
| `BIST:TRALT1!` | işlem aracı / hedge | Hedge bacağı (A sınıfı likidite) |
| `BIST:XU030` | grafik takvimi + bağlam (senkron) | Pine göstergesini bu günlük grafiğe ekleyin; takvim araştırmayla aynı olur |
| `BIST:XU030D1!` | bağlam / alternatif hedge | Piyasa yönü; araştırmadaki TRMET − β·XU030 varyantı (kuralın parçası değil) |
| `BIST:XMADN` | bağlam (senkron) | Madencilik endeksi; grup dışı sektör hareketi |
| `COMEX:GC1!` (alt. `TVC:GOLD`) | bağlam (senkron) | TRALT'ın altın bağı. Sinyal değil; altın sert hareket ettiği günlerde TRALT bacağı oynak olur |
| `BIST:XAUTRY1!` | bağlam (senkron) | Gram altın (TL) |
| `FX:USDTRY` | bağlam | TL şoku günleri (seans dışı şoklarda grup birlikte gap yapar) |

TRMET ve TRALT için diğer sürücüler (kartlardan; bu stratejinin girdisi değil):

- **TRMET:** `BIST:TRALT` / `BIST:TRENJ` senkron. ABD gecesi (`CME_MINI:NQ1!`, `NASDAQ:TUR`) yalnız açılış gap'ini öngörüyor; kapanıştan kapanışa işlenemez.
- **TRALT:** Altın (`COMEX:GC1!`) senkron, rejime bağlı (2021–24'te bağ yok, 2025–26'da güçlü). `AMEX:GDX` gün içi öncü, ama işlem güveni DÜŞÜK. Altın → TRALT kuralı ayrı bir strateji (C); bu rehberin konusu değil.

**Pine göstergesi (`koza.pine`)**

- **Kurulum:**
  1. TradingView'da `BIST:XU030` ya da `BIST:TRMET` günlük grafiğini açın.
  2. Pine Editor'e yapıştırıp "Grafiğe ekle" deyin.
- **Çizdikleri:**
  - z3 çizgisi ve ±1,5 bantları.
  - Sinyal günlerinde yeşil/kırmızı arka plan.
  - Pratik kural işaretleri: ▲/▼ giriş, ◆ uzatma, ✕ çıkış, ● kilit şüphesi.
  - Sağ üst tablo: z3, sinyal, kural durumu, β_g/β_TA, σ60, bugünkü u, AL/SAT tetiği (u ve TRMET fiyatı olarak), kontrat oranı.
- **Canlı bar:** Gün içinde son bar onaylanmamıştır; z3 TV'nin 15 dk gecikmeli fiyatıyla "canlı" hesaplanır. Tetik satırı o zaman "bugünün kapanışı için" olur.
- **Doğrulama:**
  - **Gösterge burada derlenemedi.** Denetimde de derleyici yoktu; kod satır satır okundu. İlk kullanımda son 5–10 günün z3 değerini `sinyal_koza.py` çıktısıyla karşılaştırın. Örn. 03.11.2026 için +0,49 (TV kapanışıyla ≈ +0,48), 02.11 +0,11, 30.10 +0,38.
  - **Denetim düzeltmeleri:**
    - `indicator(..., max_bars_back=300)` eklendi. Fonksiyon içindeki `x[i]` döngüleri 250 bar geriye bakıyor; bu ayar çalışma anındaki "referencing length" hatasını önler.
    - "Temettü düzeltmeli veri" girdisi eklendi (varsayılan açık; `ticker.modify(..., adjustment = adjustment.dividends)`). Araştırmadaki Yahoo `adj` ile uyum içindir. Derleme ya da veri sorunu çıkarsa kapatın; fark 2.932 günde 2 sinyal günü.
    - Kilit vekilinin asimetrik olduğu not edildi: yukarıda ≈ +%9,5, aşağıda ≈ −%8,7. Gerçek karar aracı kurum ekranından verilir.
  - **Denetimde doğru bulunanlar:** İleriye bakma yok (yalnız BIST sembolleri; altın `close[1]` + `lookahead_on`). Bar yoksa `time_tradingday` eşleşmez ve değer na olur; tatil tekrarı oluşmaz. β için 250 bar; cov ortak geçerli çiftlerle, var x'in kendi gözlemleriyle hesaplanır (pandas ile aynı). `[1]` = shift(1). σ60 bugünü içerir (araştırma tanımı). Kural durum makinesi betikle aynı. Sözdizimi: `request.security` tuple, `ta`/`math`/`str` çağrıları, `hline` (input sabiti), `var`, `table` v5'e uygun görünüyor.
  - Algoritma Python'da bar bar öykünüldü (`kod/k5_pine_emul.py`). Yahoo `adj` ile araştırma z3'ü birebir tuttu (maks fark 0).
  - Temettüsüz kapanışla (TV'ye benzer) 2015+ 2.932 günün 2'sinde sinyal farklı çıktı (temettü günleri).
- **Altın satırı** (isteğe bağlı): `close[1]` + `lookahead_on` ile yalnız bir önceki tamamlanmış altın gününü gösterir. Tatilde tekrar eden değer boş bırakılır.

---

## 12. Dosyalar

| Dosya | İçerik |
|---|---|
| `sinyal_koza.py` | Günlük sinyal betiği (pandas/numpy/requests). `--canli`, `--vadeli`, `--sermaye`, `--risk`, `--ters` |
| `koza.pine` | TradingView Pine v5 göstergesi (derlenmedi) |
| `kod/kl.py` | Ortak yardımcılar. Ortak panel + 02–03.11 bültenleri; ortak dosyalar değiştirilmedi |
| `kod/k1_repro.py` | Araştırmanın birebir yeniden üretimi (`log_k1.txt`) |
| `kod/k2_pratik.py` | Pratik kural ve varyant backtest'i (`log_k2.txt`, `res_pratik.csv`, `islemler_*.csv`) |
| `kod/k3_leadlag.py` | Lead-lag ölçümü (`log_k3.txt`, `res_leadlag.csv`, `res_spread_ac.csv`) |
| `kod/k4_1755.py` | 17:30–17:55 fiyatıyla sinyal (`res_1755_*.csv`) |
| `kod/k5_pine_emul.py` | Pine algoritmasının öykünmesi (`log_k5.txt`) |
| `kod/ydl_koza.py` | Yahoo indirici kopyası (çıktı `dl_rehber_koza/`) |
| `kod/log_sinyal_20261104*.txt` | Betik çıktıları (kapanış ve gün içi canlı) |
| `kod/denetim/` | Bağımsız denetim kodu: `bag.py` (sinyal), `d1_esles.py` (eşleşme), `d2_bt.py` (pratik kural + duyarlılık), `d3_ek.py` (uzatma, 2026, replay, lead-lag), `d4_1755.py` (17:55 Monte Carlo); loglar `log_d*.txt`, işlem listesi `islemler_P0L_denetim.csv` |

---

## 13. Riskler

1. **Kenar küçülüyor.** 2024–26 brüt +21,7 (t 0,93); maliyet sonrası ≈ 0. 2026 negatif.
2. **Kazanç az sayıda büyük işlemde.** En iyi 10 işlem çıkınca t 0,87. Birkaç büyük kazananı kaçırmak (ör. bir uzatmayı atlamak) sonucu sıfırlar.
3. **Olay riski.** Koza grubu kurumsal olaylara çok açık: TVF satışı, birleşme/iptal, endeks girişleri, 2026 fon krizi. Momentum olay günlerinde tersine dönebilir; en kötü işlemler 2022-12 / 2023-01 olay kümesinde.
4. **Zamanlama.** Kenarın bir kısmı uzlaşma fiyatının spot kapanışı geç izlemesinden geliyor. Uzlaşma yöntemi ya da seans saatleri değişirse bu kısım kaybolur.
5. **Dolum.** Uzlaşma (VWAP) birebir dolum değildir. TRMET1! B sınıfı likidite; büyük emirde etki 25 bps'e çıkar. İki bacak senkron dolmazsa tek bacak riski oluşur.
6. **Limit kilidi.** Girişte kilit kuralı uygulandı; pozisyon açıkken aleyhe kilitlenme ve çıkışın gecikmesi modellenmedi.
7. **Sonradan bulunmuş sinyal.** Momentum yönü veriden geldi; çoklu test (~2.500 test) bağlamında bağımsız aday sayısı ~8–10. Spot 2010–16'da işaret tersti.
8. **Veri farkları.** TradingView kapanışı temettüye göre düzeltilmez. Ücretsiz hesapta veri 15 dk gecikmelidir. Yahoo verisi zaman zaman gecikir ya da düzeltilir.

---

## 14. Denetim (04.11.2026)

**(1) Sinyal eşleşmesi.** Bağımsız kod (`kod/denetim/bag.py`, betik ve curlib import edilmeden, numpy pencere döngüleriyle) son 300 BIST gününde (26.08.2025 → 03.11.2026) şunları buldu:
- Betikle: z3 maks fark 1,8·10⁻¹⁴, NaN günleri aynı, sinyal uyumu %100 (34/34 sinyal günü).
- Araştırma z3'üyle (30.10'a kadar): maks fark 2·10⁻¹⁴, uyum %100.
- Tam geçmişte (6.722 gün) maks fark 9·10⁻⁶; sinyal uyumu %100.
- Tarih hizalaması doğru:
  - Bütün girdiler BIST sembolü; ABD "after" kuralı gerekmiyor.
  - Yahoo'da BIST tatil barı yok (2025–26 tatilleri tek tek kontrol edildi).
  - İşlem görmeyen gün (ör. 24.11.2025, üç hisse de v = 0) NaN sayılıyor; z3 3 gün boyunca hesaplanmıyor; ertesi getiri son geçerli fiyata göre.
- Betiğin `replay()` fonksiyonu son ~400 günde P0L ile aynı 27 işlemi buldu.

**(2) Pratik kural backtest'i.** Bağımsız simülatör (`d2_bt.py`) P0L'i birebir verdi:
- 141 işlemin hepsi aynı giriş, çıkış ve yönde; brüt farkı 0,000.
- Brüt +51,7 (t 3,00); net15+tik +28,8; 2024–26 +21,7 (t 0,93); maks düşüş −791; 8 vade devri.
- 2019+ hiçbir işlem eksik veri yüzünden düşmüyor.
- Uzatma segmentleri +76,6 (n 46); 2024+'da +23,3 (n 16, t 0,68).
- 2026: 16 işlem, net15+tik toplamı −458 bps.
- Simetrik ±%9,5 kilit vekiliyle sonuç +52,2.
- Kurucunun kilitsiz varyantları da birebir tuttu. Ama tabloda kilitli ana kuralın yanında etiketsiz duruyorlardı; §9.3'te ayrıştırıldı. Kilitli TERS kural +30,4 (t 1,83).
- Duyarlılık için §9.3b'ye bakın.
- 17:55 fiyatıyla Monte Carlo (bağımsız, 150 tekrar): −3,7 bps; 17:40 fiyatıyla −4,0 bps. Kurucunun −4 bps bulgusu doğrulandı.

**(3) Betik düzeltmeleri** (`sinyal_koza.py`):
- (a) **Bugünün Yahoo barı 18:15 yerine 18:30'dan sonra kabul ediliyor.** Yahoo ~15 dk gecikmeli (denetimde 12:41'de son fiyat zamanı 12:25 idi). Eski sınırla 18:15–18:20 arası bir çalıştırma kapanış seansından önceki fiyatı "kapanış" sayabilirdi. Son fiyat zamanı 18:05'ten önceyse uyarı basılıyor.
- (b) **`--vadeli` verildiğinde tetik fiyatı yanlış hesaplanıyordu.** Vadeli fiyatına göre hesaplanıp "TRMET kapanışı" diye yazılıyordu; bugün 101,76 yerine ≈ 104,2 çıkardı. Artık tetik her zaman spot fiyata göre.
- (c) Hisselerin son Yahoo tarihleri farklıysa uyarı basılıyor (Yahoo'nun bir seriyi geç güncellemesi).
- (d) `--sermaye`, `--risk`, `--kaldirac` artık Türkçe yazımı kabul ediyor (ör. `--risk 0,0075`, `--sermaye 1.000.000`). Eskiden virgüllü değer hata veriyordu.

**(4) Pine:** §11'deki düzeltmelere bakın. Derleyici yok; ilk kullanımda betikle karşılaştırın.

**(5) Talimatların gerçekçiliği:**
- Pay vadelisi seansı 18:10'da kapanıyor; uzlaşma son dakikaların VWAP'ı. Rehberdeki 18:00–18:10 penceresi bununla uyumlu. Endeks vadelisi (18:15) bu kuralda kullanılmıyor.
- VİOP bültenlerinde 2020-04 sonrası pay vadelisi gün içi en yüksek ve en düşük fiyatları bir önceki günün uzlaşmasına göre tam ±%10'da sınırlanıyor. Yani ±%10 limit veride doğrulandı.
- Kontrat ve teminat tablosu yeniden hesaplandı, doğru: 1 mn TL ve %0,75 risk için 21 + 42 adet, ≈ 54 bin TL teminat.
- TradingView'ın 15 dk gecikmesi talimatta hesaba katılmış.
- Rehberdeki bütün TradingView kodları `tv_final.csv`'de doğrulanmış satırlarda var: BIST:TRMET, TRALT, TRENJ, TRMET1!, TRALT1!, XU030, XU030D1!, XMADN, XAUTRY1!; COMEX:GC1!; TVC:GOLD (alternatif); FX:USDTRY; CME_MINI:NQ1!; NASDAQ:TUR; AMEX:GDX. `BIST:TRMETZ2026` ise yalnız tv_final notundaki örnek biçim; TV arama kutusunda teyit edin.
