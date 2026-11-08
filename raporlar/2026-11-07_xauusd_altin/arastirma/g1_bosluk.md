# g1_bosluk — VİOP F_XAUUSD'nin yerel primi (fazla baz): ölçüm, nedenler, 1-3-5 günlük P&L etkisi

Tarih: 08.11.2026. Kapsam: Borsa İstanbul VİOP Dolar/Ons Altın vadelisi (F_XAUUSD), 06.03.2017–06.11.2026.
Kod ve çıktılar: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/g1_viop_prim/` (yeniden üretim: `run_all.sh`).
Test kaydı: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/registry/g1_viop_prim.csv` (81 satır; BH q değerleri `registry_with_q.csv`).

Not: Bu turda web arama bütçesi (200 arama) başka ajanlarca tüketilmişti. Bu yüzden yeni arama yapamadım. Yalnız adresini bildiğim birincil sayfaları doğrudan okudum (BIST, TCMB, GZT). "VİOP ons altın prim Ocak/Mart 2026" konulu Türkçe basın taraması **yapılamadı**.

---

## 0. Kısa sonuç

1. **Prim gerçek, veri yapaylığı değil.** Mart 2026'da fazla baz (eb) aylık medyanı dört farklı spot ölçüsüyle 124–136 bp. En yüksek değer 03.03.2026'da 366–405 bp. Ölçüler: Dukascopy 15:00, Dukascopy dakikalık 15:00–15:10 VWAP, GLD NAV'dan türetilen LBMA PM ve EFP'si düşülmüş COMEX GC.
2. Prim günlerinin %84'ünde (Kas 2025–Nis 2026, eb>50 bp, 56 gün) VİOP'un **gün içi en düşük işlem fiyatı** bile uzlaşma anındaki spotun üstünde kaldı. Normal günlerde bu oran %42. Kapanış fiyatı da uzlaşmadan yalnız medyan 2 bp ayrılıyor.
3. **Bir yapaylık bulundu:** 19.03.2026 yarım gündü. O gün uzlaşma ~09:30 UTC'de oluşuyor, 15:00 spotuyla kıyaslanınca eb 320 bp çıkıyor. Doğru saatle (09:20–09:30) değer 82 bp. Yarım günler eb serisinden çıkarılmalı.
4. **Tek tanımlı taşıma tablosu** (2017–2026, aylık) kuruldu. Vadeler arası ima oranının 3 aylık UST üstündeki fazlası 2017–2021'de 0,2–1,1 puan, 2022–2025'te 0,5–1,6 puan. 2026'da 2,9 puana çıktı. Aylık zirve Nisan 2026: 6,0 puan (%9,7'ye karşı %3,7).
5. **Önceki rakamlar uzlaştırıldı:** r6'nın %5,25'i (06.11.2026) birebir çıktı. r4'ün %7,2'si tanım farkı: aktif→sonraki vade ortalaması %7,13, medyanı %6,93. r1'in %4,7–4,8'i Ekim 2026 dağılımının alt ucunda; 1226'nın Ekim medyanı %5,34. Doğrulayıcının 29,6–102,6 USD aralığı 2026 aralığımızla aynı. Tek istisna yarım gün 28.10.2026'daki 16,4 USD.
6. **Primin sürücüleri yurt içi:** VİOP açık pozisyonu (aylık Spearman 0,68), BIST KMKTP altın işlem miktarı (0,59), altın oynaklığı (0,55). USDTRY değişimiyle ilişki yok (günlük korelasyon 0,02–0,05). VİOP içi gram–sentetik farkı (tr_prem_matched) ≈ 0, yani gram altın vadelisi de aynı primi taşıyor.
7. **Arbitraj kapanmıyor:** Yabancı banka kökenli aracı kurumların VİOP USD kıymetli maden hacmindeki payı Ocak–Mart 2026'da %0,65–0,93. Endeks vadelide bu pay %10,6–12,5. Teminat oranı (PSR) 17.02.2026'da %6,7'ye, 02.03.2026'da %10'a çıktı (r1, Takasbank GM 2126). Yol riski de büyük: eb>100 iken açılan "VİOP kısa + spot uzun" vadede ortalama +165 bp kazandırdı, ama ara zarar 160 bp'ye kadar indi.
8. **Mutlak VİOP getirisini prim öngörmüyor.** eb_{t-1} → VİOP fwd1/3/5 için t 1,34 / 1,64 / 1,43; yüksek rejimde 0,86 / 0,41 / 0,24.
9. **Göreli getiriyi öngörüyor.** "VİOP uzun − fonlanmış spot uzun" için eb_{t-1} > 50 bp iken 1/3/5 günde ortalama −6,6 / −16,1 / −21,1 bp (NW t −2,4 / −3,2 / −3,3; OOS −7,4 / −17,6 / −24,1). Normal rejimde −0,4 / −1,5 / −2,8 bp. eb_{t-1} > 100 bp iken −14,7 / −26,9 / −37,0 bp (n=28).
10. Prim kapanış anında dakikalık spotla canlı ölçülürse çözülme daha hızlı: eğim 1 günde −0,20, 3 günde −0,50, 5 günde −0,55. eb>100 iken −29 / −85 / −102 bp (NW t −2,6 / −3,5 / −4,5). Ama bu yalnız bir dönem (Kas 2025–Nis 2026) ve örneklem içi.
11. **Roll ve yakınsama maliyeti:** Uzun pozisyonun son 5 işlem gününde ön vadede kalması fonlanmış spota göre ortalama −10,8 bp (medyan −8,2) kaybettirdi. 2026 rolleri fazla takvim farkı olarak ödendi: Şubat (0226→0426) 116 bp, Nisan (0426→0626) 112 bp, Haziran 51, Ağustos 17, Ekim 29 bp.
12. **Pratik kural (§6).** eb'yi 18:00–18:10 TSİ'de canlı ölçün. eb ≤ 50 bp ise VİOP uzunu sorun değil (~0,5–1 bp/gün ek taşıma). eb 50–100 bp ise 5 günlük beklenen geri kalma ≈ 17–19 bp. eb > 100 bp ise VİOP uzunu pahalı, spot benzeri araç düşünün; kısa yön görüşü için VİOP avantajlı. Roll'u vadeye 5–10 iş günü kala yapın. Fazla takvim farkı > ~50 bp ise roll etmek yerine çıkmayı düşünün. Gram altın vadelisi (F_XAUTRYM) aynı primi taşıdığı için alternatif değildir.

---

## 1. Tanım

- **eb_t** = [ln(F_t / S_t) − r_{t-1} × dte_t / 365] × 10⁴ (bp).
  - F_t: aktif kontratın uzlaşması. Aktif kontrat, önceki günün açık pozisyonu en büyük vade. Uzlaşma = 15:00–15:10 UTC'deki son 10 dakikanın miktar ağırlıklı ortalaması (r1, Prosedür).
  - S_t: spot XAUUSD. Ana seri Dukascopy BID 15:00 UTC; kalibrasyon için dakikalık VWAP.
  - r: 3 aylık ABD Hazine par getirisi (t−1). dte: vadeye kalan takvim günü.
  - Yarım günler ve dte<3 günler çıkarıldı (`eb_daily.parquet`).
- **relf** (VİOP uzun − fonlanmış spot uzun) = Σ [v_ret − s_ret + r × takvim günü / 365]. Bu yaklaşık Δeb'dir. Spot bacağının USD fonlama maliyeti dahildir. Kontrat t'de sabitlenir; roll günlerinde aynı kontrat içi getiri kullanılır.
- **Rejim:** yüksek = eb_{t-1} > 50 bp (136 gün: IS 29, OOS 107; 2026'da 58, 2023'te 27, 2020'de 18). Normal = eb_{t-1} ≤ 50 bp.
- Yeniden üretilen ön hesap (aylık medyan/maks, bp): Kas 2025 33/60, Ara 22/83, Oca 2026 81/265, Şub 61/133, Mar 128/389, Nis 18/84, May 21/52, Haz 16/80, Tem 12/36, Ağu 4/27, Eyl 6/28, Eki 2/45, Kas 4/12. Görevdeki rakamlarla aynı.
- **a2'nin "eb ortalaması 15,9 bp" özeti** tüm dönem için doğru: bizde ortalama 16,0, medyan 11,3. Ama rejimi gizliyor: 2026 ortalaması 37,9, Ocak–Mart 2026 ortalaması **102,8**, Ağustos–Kasım 2026 ortalaması 5,0 bp.

## 2. Veri kalitesi: zirve Dukascopy yapaylığı mı? Hayır.

Kod: `code/g1_01_quality.py`. Dakikalık Dukascopy XAUUSD BID verisi, 03.11.2025–30.04.2026 arasındaki tüm iş günleri ve 01–02.10.2025 için indirildi (131 dosya; önceki 210 örnek günle birlikte 334 dakikalık gün; `dl_m/`, kaynak `https://datafeed.dukascopy.com/datafeed/XAUUSD/YYYY/MM-1/DD/BID_candles_min_1.bi5`).

**Dört bağımsız spot ölçüsü:**
- (a) Dukascopy 15:00 UTC.
- (b) Dukascopy dakikalık 15:00–15:10 VWAP, yani uzlaşma penceresinin kendisi.
- (c) GLD NAV ÷ pay başına ons. Pay başına ons, 58 vade gününde VİOP vade sonu uzlaşmasından (= LBMA PM, BIST duyurusu 11834) kalibre edildi ve aradaki günler doğrusal ara değerle bulundu. Ara değer hatasının medyanı 0,07 bp. Beş çapa >5 bp sapma verdiği için dışlandı; biri 31.08.2026 (Birleşik Krallık banka tatili). Kışın LBMA PM 15:00 UTC'dir, yani 18:00 TSİ.
- (d) Yahoo GC=F saatlik 15:00 UTC fiyatından, önceki 10 günün (GC − spot) medyanı (EFP) düşülerek.

**Zirve günleri** (eb, bp; tam tablo `q_peak_days.csv`):

| Gün | Kontrat | Uzlaşma | VİOP gün içi en düşük | Spot 15:00 | Spot VWAP 15:00–10 | eb (a) | eb (b) | eb (c) LBMA PM | eb (d) GC−EFP |
|---|---|---|---|---|---|---|---|---|---|
| 28.01.2026 | 0226 | 5.334,8 | 5.293,4 | 5.285,9 | 5.276,7 | 62 | 79 | 22 | 4 |
| 29.01.2026 | 0226 | 5.619,9 | 5.540,0 | 5.496,0 | 5.441,7 | 194 | 293 | 360 | 145 |
| 30.01.2026 | 0226 | 5.181,5 | 5.116,0 | 5.031,8 | 4.999,9 | 265 | 329 | 365 | 212 |
| 02.02.2026 | 0226 | 4.791,2 | 4.470,1 | 4.716,0 | 4.721,4 | 133 | 122 | 136 | – |
| 23.02.2026 | 0226 | 5.243,9 | 5.156,7 | 5.192,2 | 5.189,6 | 95 | 100 | 97 | 97 |
| 02.03.2026 | 0426 | 5.504,4 | 5.456,0 | 5.331,6 | 5.329,1 | 260 | 264 | 293 | 269 |
| 03.03.2026 | 0426 | 5.268,5 | 5.205,1 | 5.037,8 | 5.049,0 | 389 | 367 | 397 | 405 |
| 04.03.2026 | 0426 | 5.297,7 | 5.263,1 | 5.145,9 | 5.152,8 | 233 | 219 | 228 | 250 |
| 10.03.2026 | 0426 | 5.338,9 | 5.262,5 | 5.206,5 | 5.213,2 | 199 | 186 | 193 | 205 |
| 19.03.2026 (yarım gün) | 0426 | 4.771,5 | 4.741,5 | 4.601,6 | – | 320 | **82 (09:20–09:30)** | – | – |
| 23.03.2026 | 0426 | 4.528,0 | 4.157,8 | 4.461,7 | 4.475,9 | 109 | 77 | 99 | 116 |
| 24.03.2026 | 0426 | 4.459,4 | 4.398,7 | 4.415,6 | 4.409,8 | 61 | 74 | 66 | 69 |

- 29–30.01.2026'da spot uzlaşma penceresinde çöktü. Dukascopy 14:59'da 5.496, 15:08'de 5.418, 15:14'te 5.383; GC 15:00 barı 5.525'ten açılıp 5.211'den kapandı. Bu yüzden 15:00 ölçüsü primi **küçük** gösteriyor. Pencere VWAP'ı ve LBMA PM ile prim 293–365 bp.
- **Aylık medyan, dört ölçüyle (bp; yarım günler hariç):** Ocak 2026: 81 / 77 / 80 / 97. Şubat: 61 / 53 / 61 / 56. Mart: 124 / 127 / 132 / 131. Nisan: 18 / 25 / 29 / 19. Mart maksimumu 389 / 366 / 397 / 405.
- **Vade günü kontrolü** (58 vade günü, 2017–2026): VİOP vade sonu uzlaşması (LBMA PM) ile Dukascopy (PM saati) farkının medyanı −1,8 bp, ortalaması −3,8, std 17,6.
  - 27.02.2026: 0226 = 5.222,3, Dukascopy 15:00 = 5.223,4, fark −2,1 bp.
  - Aynı gün 0426 = 5.420,7. Bu, eb = ln(5.420,7 / 5.223,4) − 0,0368 × 62 / 365 = 370,8 − 62,5 = **308 bp** demek. O gün 0426'da 141.078 sözleşme işlem gördü (roll günü).
  - Büyük sapma 31.12.2025'te (−86,8 bp). LBMA yılın son gününde PM ihalesi yapmıyor, uzlaşma AM fiyatına göre (r1).
- **GLD-ima LBMA PM − Dukascopy** (2.372 gün): medyan −1,1 bp, çeyrekler arası −7,4 / +3,6 bp. 2026'da medyan mutlak fark 6,2 bp. Dukascopy seviyesi sistematik olarak kaymıyor. Dukascopy BID kotasyonu orta fiyattan ~1 bp aşağıda olabilir; eb'yi en çok ~1 bp şişirir.
- **15:00 ile 15:00–15:10 VWAP arasındaki eb farkı** (321 dakikalık gün): medyan −0,2 bp, MAD 6,2 bp. Zirve günlerinde medyan +3,9 bp, uç değerler yalnız 29–30.01 çöküşünde.
- **VİOP'un kendi fiyatları:** Kas 2025–Nis 2026'da eb>50 olan günlerin %84'ünde (47/56) VİOP gün içi en düşüğü, uzlaşma penceresi spot VWAP'ının üstünde. Bu en düşük fiyat önceki akşam seansını da kapsar. Normal günlerde oran %42. Kapanış−uzlaşma farkı prim günlerinde medyan +2,3 bp, std 16,6. Yani uzlaşma fiyatında hesap hatası yok; VİOP gerçekten spotun üstünde işlem gördü.

**Sonuç:** Zirve gerçek. Tek düzeltme yarım günleri çıkarmak. Ayrıca 29–30.01 gibi pencere içi çöküşlerde 15:00 ölçüsü primi **olduğundan küçük** gösteriyor.

## 3. Tek tanımla taşıma tablosu (2017–2026)

Kod: `code/g1_02_carry.py`. Günlük tablo `carry_daily.parquet`, aylık tablo `carry_monthly.csv` (117 ay), yıllık tablo `carry_yearly.csv`.

**Tanımlar:**
- M1 = vadeye ≥3 takvim günü kalan en yakın vade, M2 = sonraki vade.
- b1 = ln(F1/S15). r1_imp = b1 × 365 / dte1 (spot–ön vade ima oranı).
- r12 = ln(F2/F1) × 365 / (dte2 − dte1) (vadeler arası ima oranı).
- Fazla oran x12 = r12 − UST 3 ay.
- SOFR: NY Fed API (`https://markets.newyorkfed.org/api/rates/secured/sofr/search.json`). DTB3: FRED (`https://fred.stlouisfed.org/graph/fredgraph.csv?id=SOFR,DTB3,TB3MS`).

**Yıllık özet** (oranlar %, eb bp):

| Yıl | r1_imp medyan | r12 medyan | r12 ort. | UST 3a | SOFR | x12 (r12−UST) | eb_act ort. | eb_act medyan | F2−F1 min–maks (USD) |
|---|---|---|---|---|---|---|---|---|---|
| 2017 | 1,71 | 1,33 | 1,33 | 1,03 | – | 0,29 | 5,6 | 5,0 | −2,0 – 9,0 |
| 2018 | 2,71 | 2,40 | 2,44 | 1,97 | 1,98 | 0,44 | 6,8 | 7,3 | −1,9 – 13,4 |
| 2019 | 3,33 | 2,34 | 2,35 | 2,10 | 2,20 | 0,24 | 11,1 | 10,1 | 1,0 – 8,3 |
| 2020 | 2,50 | 1,50 | 1,57 | 0,38 | 0,38 | 1,12 | 21,6 | 18,3 | −3,2 – 10,2 |
| 2021 | 1,24 | 0,84 | 0,90 | 0,05 | 0,04 | 0,79 | 11,5 | 9,9 | −0,1 – 11,4 |
| 2022 | 4,04 | 3,67 | 3,84 | 2,09 | 1,65 | 1,58 | 17,0 | 15,7 | 2,3 – 26,1 |
| 2023 | 7,39 | 6,47 | 6,52 | 5,27 | 5,00 | 1,20 | 21,5 | 15,4 | 13,5 – 37,0 |
| 2024 | 6,75 | 5,70 | 5,76 | 5,17 | 5,14 | 0,52 | 15,4 | 13,7 | 7,1 – 33,8 |
| 2025 | 5,52 | 4,78 | 4,68 | 4,20 | 4,24 | 0,57 | 11,3 | 10,9 | 10,7 – 56,6 |
| 2026 (06.11'e kadar) | 5,77 | 6,70 | 6,98 | 3,84 | 3,68 | **2,86** | **38,8** | 17,1 | 16,4 – 102,6 |

**Son 15 ay** (aylık medyan; eb bp, oranlar %):

| Ay | eb_act medyan / maks | r1_imp | F2−F1 medyan (min–maks) USD | r12 medyan / maks | UST 3a | SOFR | x12 UST / SOFR |
|---|---|---|---|---|---|---|---|
| 2025-09 | 22 / 39 | 5,9 | 28,5 (25,9–32,4) | 4,7 / 5,3 | 4,1 | 4,3 | 0,6 / 0,4 |
| 2025-10 | 13 / 80 | 5,9 | 30,4 (26,5–53,1) | 4,4 / 8,1 | 4,0 | 4,2 | 0,4 / 0,2 |
| 2025-11 | 33 / 60 | 6,7 | 35,9 (32,2–39,3) | 5,4 / 6,0 | 3,9 | 4,0 | 1,5 / 1,4 |
| 2025-12 | 22 / 83 | 8,6 | 41,8 (33,8–56,6) | 6,0 / 7,5 | 3,7 | 3,8 | 2,3 / 2,2 |
| 2026-01 | 81 / 265 | 11,3 | 59,0 (48,0–80,3) | 7,4 / 8,4 | 3,7 | 3,7 | 3,7 / 3,7 |
| 2026-02 | 61 / 133 | 17,1 | 68,8 (53,2–102,6) | 8,1 / 11,5 | 3,7 | 3,7 | 4,4 / 4,4 |
| 2026-03 | 128 / 389 | 14,0 | 73,1 (56,4–82,8) | 8,8 / 10,1 | 3,7 | 3,6 | 5,1 / 5,2 |
| 2026-04 | 18 / 84 | 6,8 | 76,6 (62,5–90,7) | **9,7** / 11,1 | 3,7 | 3,6 | **6,0 / 6,0** |
| 2026-05 | 21 / 52 | 5,6 | 62,7 (48,6–70,7) | 7,8 / 8,9 | 3,7 | 3,6 | 4,2 / 4,3 |
| 2026-06 | 16 / 80 | 4,6 | 59,0 (39,1–67,8) | 8,0 / 9,1 | 3,8 | 3,6 | 4,2 / 4,4 |
| 2026-07 | 12 / 36 | 4,7 | 38,6 (31,7–46,2) | 5,7 / 6,7 | 3,9 | 3,6 | 1,8 / 2,1 |
| 2026-08 | 4 / 27 | 4,4 | 33,3 (29,6–40,6) | 4,7 / 5,3 | 3,9 | 3,6 | 0,8 / 1,0 |
| 2026-09 | 6 / 28 | 4,6 | 38,3 (34,1–45,1) | 5,2 / 6,3 | 4,1 | 3,7 | 1,1 / 1,5 |
| 2026-10 | 2 / 45 | 4,6 | 40,2 (16,4*–45,6) | 5,6 / 7,4 | 4,2 | 3,9 | 1,4 / 1,8 |
| 2026-11 (5 gün) | 4 / 12 | 4,5 | 35,1 (32,7–41,9) | 5,5 / 6,4 | 4,2 | 3,9 | 1,3 / 1,6 |

\* 28.10.2026 yarım gün; geri vadenin uzlaşması güvenilmez.

**Önemli gözlem:** Ön vadenin primi Nisan 2026'da normale döndü (medyan 18 bp). Ama vadeler arası fazla oran Nisan–Haziran'da en yüksek düzeyde kaldı (4,2–6,0 puan). Yani prim önce **geri vadelere** taşındı ve oradan yavaş eridi. eb2 (M2'nin fazla bazı) aylık medyanı: Ocak 139, Şubat 137, Mart 207, Nisan 120, Mayıs 93, Haziran 92 bp.

**Uzlaştırma:**
- **r6 (%5,25, 06.11.2026, Şub27/Ara26):** ln(4.112,4 / 4.078,8) × 365 / 57 = **%5,253**. Birebir aynı. Aynı gün UST 3 ay %4,17, SOFR %3,92. Fazla oran UST'ye göre 1,1 puan, SOFR'a göre 1,3 puan.
- **r4 (%7,2, 2026 takvim yayılımı medyanı):** Aktif→sonraki vade (OI'ye göre) tanımıyla 2026 medyanı %6,93, ortalaması %7,13. En yakın iki vade tanımıyla medyan %6,70, ortalama %6,98. r4'ün %7,18'i ortalama/medyan ve kontrat seçimi farkından geliyor; ±0,5 puan tanım farkı.
- **r1 (%4,7–4,8, Ekim 2026, 1226):** 1226'nın Ekim 2026 spot ima oranı (M2 iken, 19 gün): medyan %5,34, %10–%90 aralığı %4,94–5,77. 30.10.2026'da (M1 iken) %4,70. r1'in rakamı dağılımın alt ucu ya da ay sonu değeri. Medyan ≈ %5,3.
- **Doğrulayıcı (takvim farkı 29,6–102,6 USD; %5,2–6,1):** 2026'da F2−F1 en yüksek 102,6 USD (Şubat), yarım gün 28.10 hariç en düşük 29,6 USD (19.08.2026). Aralık birebir aynı. %5,2–6,1 aralığı bizim tabloda Temmuz–Kasım 2026 aylık r12 medyanlarına (4,7–5,7) ve 1226'nın Ekim spot ima oranına (%4,9–5,8) karşılık geliyor. Yılın ilk yarısını (7,4–9,7) kapsamıyor.
- **r1'in "1,5–2 bp/gün taşıma" varsayımı:** VİOP − spot (fonlamasız) günlük ortalama, 2017–2026 boyunca −1,85 bp/işlem günü. Varsayım tüm dönem için doğru. Ama yıllara göre değişiyor: 2023 −3,44, 2024 −3,00, 2025 −2,29, **2026 −4,10 bp/gün**. Yüksek rejimde fonlanmış göreli kayıp 1. gün −6,6 bp. Fonlama eklenmezse ~1–1,5 bp/gün daha kötü. Yani 1,5–2 bp/gün 2026 için yarı yarıya düşük, prim rejiminde 4–5 kat düşük.

## 4. Sürücüler

Kod: `code/g1_03_tests.py` (C ailesi + eşzamanlı tablo `t_contemp.csv`) ve `code/g1_05_monthly.py` (`monthly_drivers.csv`).

### 4.1 Türkiye fiziki primi
- **GZT, 25.02.2026:** "1 kilo altında iki piyasa arasındaki fark 12.500 dolara kadar açılmıştı... Bugün ise bu makas yaklaşık 5.000 dolar seviyesine gerilemiş durumda."
  - Tarih "geçtiğimiz ay" (Ocak 2026) diye geçiyor; kesin gün yok. **Reuters'a atıf yok.** Görevdeki "Reuters'ın verdiği 12.500 $" kaynağı **bulunamadı**.
  - Çeviri: 12.500 $/kg = 388,8 $/ons. Ons 5.000–5.500 $ iken bu %7,1–7,8. 5.000 $/kg = 155,5 $/ons, 25.02 spotunda (5.190,9) %3,0.
  - Bu "makas" alış-satış farkını da içerebilir (r4).
  - Kaynak: https://www.gzt.com/ekonomi/25-subat-2026-altin-fiyatlari-gram-altin-fiyati-bugun-ne-kadar-iste-kapalicarsi-rakamlari-4019837
- Aynı günlerde VİOP primi daha düşük. 29–30.01.2026'da eb 194–365 bp (%2–3,7). 25.02.2026'da aktif 0226 (vadeye 2 gün) 26 bp, 0426 147 bp (%1,5). **VİOP, fiziki yerel prim ile uluslararası fiyat arasında bir yerde fiyatlandı.**
- **BIST KMKTP altın işlem miktarı** (BIST Ekim 2026 aylık piyasa raporu):
  - Mart 2026: **55.007 kg**. Mart 2025'te 21.414 kg, yani +%157.
  - Diğer aylar: Oca 2026 33.584, Şub 32.719, Nis 35.827, May 19.635, Haz 37.175, Tem 26.166, Ağu 18.696, Eyl 11.541, Eki 13.572 kg.
  - Mart 2026'da işlem sayısı 4.386 (+%398), TL hacmi 376.431 milyon TL (+%397).
  - Aylık eb medyanı ile Spearman korelasyonu 0,59 (Kas 2024–Eki 2026, n=24).
  - İthalat ile ilişki zayıf (0,14). İthalat Mart 2026'da 8.512 kg, Ekim 2026'da 2.871 kg.
  - Kaynak: https://borsaistanbul.com/files/aylik-piyasa-raporu-ekim-2026.pdf
- **tr_prem_matched** (VİOP gram vs XAUUSD×USDTRY vadelileri):
  - 2026 ortalaması +2 bp, std 8 bp (r4). Zirve günlerinde ±27 bp.
  - Bu, VİOP içi tutarlılığı gösteriyor: **F_XAUTRYM de aynı ons primini taşıyor**.
  - Öngörü gücü yok. tr_prem_{t-1} → relf1/3/5 için t −0,03 / −0,13 / 0,88; Δtr_prem için |t| < 0,31.
- Günlük Kapalıçarşı/KMKTP prim serisi **bulunamadı**. BIST KMTP sayfasındaki günlük fiyat tabloları dinamik; XML bağlantıları "#". Bu yüzden fiziki prim → Δeb günlük lead-lag'i test **edilemedi**.

### 4.2 USDTRY şokları
- Eşzamanlı korelasyonlar zayıf. Δeb ile ΔUSDTRY (Dukascopy 15:00): 2017–2025.10'da 0,02, Kas 2025–Nis 2026'da 0,05. Aylık eb ile aylık USDTRY değişimi −0,42; kur sabit hızla kaydığı için bu bilgi taşımıyor.
- Öngörü testleri:
  - ΔUSDTRY_t → relf1: IC 0,045, t 2,38 (IS 1,85, OOS 1,87), q = 0,062. h=3 ve 5'te t 0,71 ve 0,56.
  - VİOP USDTRY getirisi (t−1) → relf: t −1,44 / −1,11 / −0,56.
- **Sonuç:** Kur şoku primi açıklamıyor. Mart 2026'da kur kontrollüydü (r4: VİOP USDTRY günlük getirisi −%0,54 ile +%0,24 arası).

### 4.3 TCMB adımları
- TCMB **01.03.2026 (Pazar)** tarihinde iki duyuru yayımladı:
  - **DUY2026-11:** "1 hafta vadeli repo ihalelerine bir süreliğine ara verilmesi kararlaştırılmıştır." (https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Duyurular/Basin/2026/DUY2026-11)
  - **DUY2026-10:** TCMB nezdinde TL uzlaşmalı vadeli döviz satım işlemlerine başlandı. Duyuruda tutar, vade ve faiz yok. (https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Duyurular/Basin/2026/DUY2026-10)
  - İkisini de doğrudan okudum.
- Ertesi iş günleri eb: 02.03.2026'da **260 bp**, 03.03.2026'da **389 bp** (dönemin zirvesi).
- Diğer adımlar (r4 ve r7'den; bu çalışmada yeniden doğrulanmadı):
  - Fonlama fiilen O/N %40'tan yapıldı. İhaleler 23.08.2026'da yeniden başladı (DUY2026-35).
  - TCMB'nin Mart 2026'da ~60 t altın satıp swapladığı haberleri var (ikincil, orta güven).
- **Nedensellik kanıtlanmadı.** İran savaşı 28.02.2026'da başladı (r4). Altın oynaklığı ve yurt içi talep aynı günlerde sıçradı. TCMB etkisini ayrıştıracak bir test kurulamadı.

### 4.4 VİOP açık pozisyon ve hacim
- **Aylık:** eb medyanı ile VİOP XAUUSD toplam OI medyanı arasında Spearman 0,68, hacim medyanıyla 0,53 (n=24).
  - Toplam OI Kas 2025–Nis 2026'da 193–233 bin sözleşme (≈ 193–233 bin ons; 5.000 $'dan ≈ 1,0–1,2 milyar $).
  - Temmuz–Ekim 2026'da 67–99 bin sözleşme.
- **Günlük, eşzamanlı:** Δeb ile ΔlogOI korelasyonu Kas 2025–Nis 2026'da 0,28, öncesinde 0,14. Yeni uzun pozisyon girişi primi açıyor.
- **Öngörü yok:** ΔlogOI_{t-1} → relf5 için t −1,68 (OOS −2,39); hacim z_{t-1} → relf5 için t −0,90.

### 4.5 Oynaklık ve teminat
- eb seviyesi spot oynaklığıyla birlikte hareket ediyor:
  - Günlük: eb ile 5 günlük spot oynaklığı arasındaki korelasyon Kas 2025–Nis 2026'da 0,49, 2017–2025.10'da 0,20.
  - Aylık Spearman 0,55 (n=24). 2017–2026'nın 117 ayında 0,40.
- spot vol5_t → relf1 için t −3,09 (OOS −2,63, q=0,011). Bu büyük olasılıkla eb seviyesini temsil ediyor (eb ile korelasyonu 0,38).
- **Takasbank GM 2126 (12.02.2026; r1):** XAUUSD PSR 17.02.2026'dan %6,7, 02.03.2026'dan %10,0. Arbitrajcının sözleşme başına teminatı primin zirvesinde %50 arttı. Kaynak (aracı kurum barındırması, bu çalışmada yeniden okunmadı): https://www.ahlatciyatirim.com.tr/medya/icerik/dosyalar/RISK_PARAMETRELERI_12.02.2026.pdf
- Aracı kurum kuralları: QNB Invest teminatın en az %50'sinin TL olmasını istiyor ve XAUUSD için kendi PSR'ı %20 (r1; https://www.qnbinvest.com.tr/viop-teminatlari). VİOP USD kâr/zararı her gün TCMB 15:30 alış kuruyla TL'ye çevriliyor (r1, Prosedür).

### 4.6 Yatırımcı tipi ve aracı kurum dağılımı
- **BIST "İşlem Hacmi Yerli/Yabancı Dağılımı"** (https://www.borsaistanbul.com/data/vadeli/viopyyishac202610.zip) yalnız **VİOP toplamı** için yayımlanıyor.
  - Yabancı payı: 2025'te %42,0. 2026'da Ocak %43,5, Şubat %44,3, Mart %45,7, Ekim %45,9.
  - **XAUUSD özelinde yatırımcı tipi istatistiği bulunamadı.** Dosya dizini (https://www.borsaistanbul.com/files/datafilepaths_viop.zip) sözleşme bazında yerli/yabancı veya bireysel/kurumsal dosyası listelemiyor.
- **Vekil ölçü: üye bazında aylık hacim** (`viopaylikishacYYYYMM.zip`, sayfa "KIYM MAD VİS-PREC MET FUT_USD").
  - Yabancı banka kökenli üyelerin (Bank of America Yatırım Bank, HSBC Yatırım, ING Yatırım) toplam payı:
    - Kıymetli maden USD vadelileri: Eki 2025 %1,54, Oca 2026 %0,78, Şub %0,65, Mar %0,93, May %2,87, Ağu %3,45, Eki 2026 %0,87.
    - Endeks vadelileri: Oca %10,6, Mar %12,5, Eki %9,4.
    - TL döviz vadelileri: Oca %13,9, Mar %6,3, Eki %10,9.
  - Mart 2026'da kıymetli maden USD vadelilerinde ilk 5 üye: Yapı Kredi Yatırım %27,3, İş Yatırım %14,8, QNB Yatırım %10,8, Ak Yatırım %8,6, Garanti BBVA %8,1.
  - Kıymetli maden USD vadelileri toplam hacmi: Oca 2026 1.320 milyar TL, Mar 969, May 369, Ekim 519 milyar TL.
  - **Yorum:** Uluslararası arbitraj sermayesinin doğrudan kanalı neredeyse yok. Yabancılar başka aracılar üzerinden işlem yapabildiği için bu vekil ölçü kesin değil.

### 4.7 Pozisyon limitleri ve piyasa yapıcı kapasitesi
- XAUUSD için hesap bazında sayısal pozisyon limiti **bulunamadı** (r1; BIST sayfası Takasbank MKT mevzuatına atıf yapıyor). Emir başına üst sınır 1.250 sözleşme.
- Piyasa yapıcı yükümlülüğü yalnız azami spread (normal seans 2,80–4,00 USD) ve piyasada bulunma oranı (%70) içeriyor (r1, Prosedür Ek-10/12). Fiyat **seviyesine** dair bir yükümlülük yok. Spread yükümlülüğü 300 bp'lik seviye primini engellemez.
- XAUUSD'deki piyasa yapıcı sayısı ve bilanço kapasitesi **bulunamadı**.

### 4.8 Arbitraj neden kapanmadı (kanıtların özeti)
1. **Sermaye ve kanal:** Arbitrajcı VİOP'u satıp yurt dışında spot almalı, ya da yurt içinde ithal edilebilir fiziki tutmalı. Yabancı banka kökenli üyelerin altın vadeli payı %1'in altında. Kapatılması gereken uzun pozisyon 1–1,2 milyar $ büyüklüğündeydi.
2. **Yol riski:** eb>100 iken (28 gün, 2020–2026) açılan "M1 kısa + fonlanmış spot uzun, vadeye kadar tut" işlemi ortalama 32 iş gününde +165 bp kazandırdı (en az +75, en çok +376). Ama ara dönemde en kötü değerleme zararı −160 bp. Örnek: 12.01 ve 21.01.2026 girişlerinde eb 105–107 bp'den 30.01'de 265 bp'ye açıldı. Kod: `g1_04_roll.py`, çıktı `arb_path.csv`.
3. **Teminat:** PSR %6,7 → %10 (Şubat–Mart 2026). Teminatın bir kısmı TL olmalı ve TL likiditesi Mart 2026'da daraltıldı (DUY2026-11).
4. **Zamanlama:** Prim oynaklık sıçramalarında açılıyor. Risk sermayesinin en kıt olduğu an bu.
5. **İkame:** Fiziki yerel prim daha yüksekti (Ocak 2026'da %7'ye kadar, GZT). Yurt içi alıcı için VİOP uzunu fizikiden ucuzdu. Talep VİOP'a kaydı.

## 5. Testler

Kurallar: `lib_altin` (`split_stats`, NW lag ≥ max(h,5)), IS = 2017-03..2021-12, OOS = 2022-01..2026-11. Sinyal eb_{t-1} t−1 15:10'da biliniyor, giriş t uzlaşması. 81 test kayda geçti (72'si p değerli). Ajan içi BH: q<0,05 olan 17, q<0,10 olan 21 test (`registry_with_q.csv`). Plasebo: eb_{t-1} → relf3 için IC −0,086. Bir gün daha eski bilgiyle −0,083, iki gün −0,049. Yani ilişki gecikmeye dayanıklı.

### 5.1 Mutlak VİOP getirisi (A ailesi): yok
| Öngörücü | h=1 t | h=3 t | h=5 t | OOS t (h=3) |
|---|---|---|---|---|
| eb_{t-1} (tümü) | 1,34 | 1,64 | 1,43 | 0,85 |
| eb_{t-1} \| eb>50 | 0,86 | 0,41 | 0,24 | 0,28 |
| eb_{t-1} \| eb≤50 | 1,35 | 1,75 | 1,61 | 0,92 |
| Δeb_{t-1} | 0,71 | 0,90 | 1,24 | 0,70 |

Prim, altının yönünü söylemiyor. Yüksek rejimde VİOP mutlak getiri ortalaması gürültülü: eb 100–200 kovasında fwd5 −180 bp, n=23, tek dönem.

### 5.2 Göreli getiri (B ve D aileleri): var
- eb_{t-1} → relf (tümü): IC −0,039 / −0,086 / −0,096, t −2,05 / −3,67 / −3,52. OOS t −1,97 / −3,23 / −2,82. h=5'te 10 yılın 8'inde aynı işaret.
- Yüksek rejim içinde: IC −0,20 / −0,25 / −0,32, t −2,80 / −2,96 / −4,01 (OOS −2,93 / −2,14 / −3,37). q = 0,022 / 0,015 / 0,001.

**eb_{t-1} kovasına göre ortalama relf** (VİOP uzun − fonlanmış spot, bp; tüm dönem / OOS):

| eb_{t-1} | n | 1 gün | 3 gün | 5 gün | 5 gün OOS (n) |
|---|---|---|---|---|---|
| ≤ 0 | 343 | +1,1 | +0,9 | +0,5 | −1,3 (149) |
| 0–25 | 1.475 | −0,6 | −1,8 | −3,2 (t −6,0) | −4,3 (646) |
| 25–50 | 344 | −1,2 | −2,6 | −4,2 (t −3,6) | −4,0 (218) |
| 50–100 | 106 | −4,5 | −13,2 | −16,7 (t −2,7) | −18,9 (79) |
| 100–200 | 23 | −8,9 | −19,8 | −25,5 (t −2,0) | −28,2 (18) |
| > 200 | 5 | −41 | −59 | −90 | – |

| Eşik | n | 1 gün | 3 gün | 5 gün | eşik üstü ort. eb |
|---|---|---|---|---|---|
| eb_{t-1} > 25 | 482 | −2,7 | −6,4 | −8,9 | 49 |
| > 50 | 136 | −6,6 (t −2,4) | −16,1 (t −3,2) | −21,1 (t −3,3) | 86 |
| > 75 | 56 | −9,6 | −20,5 | −27,8 | 124 |
| > 100 | 28 | −14,7 | −26,9 | −37,0 | 162 |
| > 150 | 13 | −43,7 | −44,5 | −93,4 | 214 |

- IS'te (2017–2021) 50–100 kovası −4,7 / −10,1 / −8,7 bp (n=24, t −1,1 / −1,5 / −1,5). İşaret aynı ama zayıf.
- Normal rejimde (eb ≤ 50) sabit bir sızıntı var: 5 günde −2,8 bp (t −5,2), OOS −3,8 bp. Yani VİOP uzunu, UST'ye göre fazla taşıma nedeniyle günde ~0,5–0,8 bp geride kalıyor.
- AR(1): eb için ρ = 0,67 (tümü), Kas 2025–Nis 2026'da 0,78. Zaman gürültüsü ρ'yu aşağı çekiyor. Göreli kayıp oranı, eb_{t-1}'in 5 günde ~%20–25'inin çözüldüğünü gösteriyor.

### 5.3 Kapanış anında canlı ölçülen prim (G ailesi; dakikalık spot, Kas 2025–Nis 2026)
Giriş: t uzlaşması. Prim t'de 15:00–15:10 spot VWAP ile ölçülür; bu, işlem yapan kişinin ekranında gördüğü değerdir. Çıkışta da aynı pencere kullanılır.

| Rejim (eb_t) | n (h=1/3/5) | 1 gün | 3 gün | 5 gün |
|---|---|---|---|---|
| ≤ 50 | 62 / 62 / 58 | −0,2 | −1,9 | −2,5 |
| > 50 | 54 / 52 / 50 | −7,1 (t −1,5) | −21,0 (t −1,7) | −29,0 (t −1,7) |
| > 100 | 16 / 15 / 14 | **−29,0 (t −2,6)** | **−85,4 (t −3,5)** | **−101,6 (t −4,5)** |

- Eğim (relf_h ~ eb_t): −0,20 / −0,50 / −0,55. Primin yarısı 3 günde çözülüyor.
- Spearman IC −0,30 / −0,39 / −0,38, t −2,8 / −4,3 / −5,4.
- **Zayıflık:** Tek bir dönem (Ocak–Mart 2026), örtüşen pencereler, örneklem içi. OOS yok.

### 5.4 Türkiye lead-lag'i (C ailesi): yok ya da zayıf
Öngörücü → relf, h=1/3/5 için t değerleri:
- tr_prem_{t-1}: −0,03 / −0,13 / 0,88. Δtr_prem_{t-1}: −0,31 / −0,19 / −0,23.
- ΔUSDTRY_t: **2,38** / 0,71 / 0,56. |ΔUSDTRY_t|: 1,73 / 1,81 / 1,93 (OOS ≈ 0).
- VİOP USDTRY ret_{t-1}: −1,44 / −1,11 / −0,56.
- ΔlogOI_{t-1}: −1,12 / −0,54 / −1,68. Hacim z_{t-1}: −0,72 / −0,19 / −0,90.
- Spot vol5_t: **−3,09** / −2,48 / −1,49. Spot ret5_t: 1,18 / 1,11 / 2,13. Spot ret1_t: 1,99 / 1,33 / 1,44.

Kayda değer tek bulgu spot vol5 (q=0,011). O da eb seviyesinin vekili. Türkiye'ye özgü değişkenlerin (kur, gram–sentetik fark, OI) Δeb üzerinde öncül gücü yok.

### 5.5 İşlem kuralları (E ailesi; maliyet 5 bp, göreli için 10 bp)

| Kural | h | Tam dönem Sharpe | OOS Sharpe | OOS drift'siz Sharpe | Maruziyet |
|---|---|---|---|---|---|
| Her zaman uzun (buy&hold) | – | 0,49 | – | – | 1,00 |
| eb_{t-1} > 50 iken VİOP uzun yok, aksi halde uzun | 1 / 3 / 5 | 0,53 / 0,56 / 0,55 | 0,61 / 0,63 / 0,61 | 0,07 / 0,08 / 0,05 | 0,94 |
| eb_{t-1} > 50 iken VİOP kısa, aksi halde düz | 1 / 3 / 5 | −0,02 / 0,00 / −0,04 | 0,00 / 0,04 / −0,03 | 0,09 / 0,13 / 0,06 | 0,06 |
| eb_{t-1} > 50 iken VİOP kısa + spot uzun | 1 / 3 / 5 | 0,18 / 0,35 / 0,28 | 0,34 / 0,45 / 0,37 | 0,22 / 0,32 / 0,23 | 0,06–0,09 |

- Prim filtresi mutlak getiride bağımsız bir kazanç (alfa) üretmiyor; drift'siz Sharpe ≈ 0. Yalnızca pahalı 6% günde uzun olmamayı sağlıyor.
- Göreli işlem pozitif ama küçük: yıllık getiri %0,3–1,0, düşük maruziyet. İki bacaklı işlem bireysel yatırımcı için zor; spot bacak yurt içinde kaldıraçlı XAUUSD ile kurulabilir, ama swap maliyeti test edilmedi.

### 5.6 Roll ve vade yakınsaması (F ailesi; `g1_04_roll.py`)
- **Vade yakınsaması:** Vade günü uzlaşması LBMA PM'dir. Spot ile farkın medyanı −1,8 bp, yani prim sıfıra yakınsıyor. M1 uzunu fonlanmış spota göre ortalama şöyle kaybetti:
  - son 1 günde −9,4 bp (medyan −4,8),
  - son 5 günde −10,8 bp (−8,2),
  - son 10 günde −11,8 bp (−9,3),
  - son 20 günde −23,4 bp (−13,7).
- Örnekler:
  - 0226: son 20 günde −267 bp, son 5 günde −63 bp.
  - 1225: son 5 günde −104 bp (31.12'de AM fiyatı etkisi dahil).
  - 1025: son 5 günde −67 bp.
- **Roll anında ödenen fazla takvim farkı**, ln(F2/F1) − UST3a × Δgün / 365, vadeye 5 iş günü kala (bp):
  - Yıllık ortalamalar: 2017 6,5; 2018 4,9; 2019 10,1; 2020 15,6; 2021 10,2; 2022 25,7; 2023 42,5; 2024 27,2; 2025 16,0; **2026 64,9**.
  - 2026 rolleri: 0226→0426 (20.02) **116,1**, 0426→0626 (22.04) **111,7**, 0626→0826 50,9, 0826→1026 16,7, 1026→1226 29,0. 1225→0226 (24.12.2025) 46,6.
- **Erken mi geç mi?** Son k günde M1'de kalmak ile M2'ye geçmek arasındaki fark (uzun için, bp; negatif = erken geçmek daha iyi): k=5 −16,8 (medyan −10,6), k=10 −22,2, k=20 −26,4.
  - İstisnalar: 0426 (k=5'te +64) ve 0626 (+24). O dönemde geri vadenin primi eriyordu, erken geçen kaybetti.
- **Yüksek rejimde M2 mi M1 mi?** 5 günlük relf M1'de −19,7, M2'de −13,5 bp (fark +3,3; t 1,54, anlamsız).

## 6. Pratik kural (1-3-5 gün, kapanıştan kapanışa)

**Ölçüm (her gün 18:00–18:10 TSİ):**
- eb = ln(VİOP aktif vade fiyatı / spot XAUUSD) × 10⁴ − UST3a × vadeye kalan takvim günü / 365 × 10⁴.
- 06.11.2026 örneği: 1226 = 4.078,8, vadeye 55 gün, UST3a %4,17 → taşıma 62,8 bp. Kasım 2026 eb medyanı 4 bp (normal).
- Yarım günlerde uzlaşma 12:30–12:40 TSİ'de oluşur; o saatin spotunu kullanın.

| eb (bp) | VİOP uzunu, fonlanmış spota göre beklenen geri kalma (1 / 3 / 5 gün) | Ne yapmalı |
|---|---|---|
| ≤ 25 | ≈ 0,6 / 1,8 / 3,2 bp (eb ≤ 0 iken ≈ 0) | Normal. VİOP uzun kullanılabilir |
| 25–50 | ≈ 1,2 / 2,6 / 4,2 bp | Normal. Maliyet gidiş-dönüş komisyonunun altında |
| 50–100 | ≈ 4,5 / 13 / 17 bp (OOS 4,5 / 14 / 19) | Uzun boyutunu küçültün ya da spot benzeri araçla alın. Kısa görüş için VİOP avantajlı |
| > 100 | ≈ 15 / 27 / 37 bp (eb_{t-1}). Canlı ölçümle 29 / 85 / 102 bp (tek dönem) | **VİOP uzunu pahalı.** Yeni uzun pozisyonu spot benzeri araçla kurun; mevcut uzunu tutmanın maliyetini hesaba katın. VİOP kısa, prim çözülmesinden ek kazanç sağlar |

**Alternatif araçlar:**
- **F_XAUTRYM (gram altın vadeli) alternatif değil.** tr_prem_matched ≈ 0 olduğu için aynı primi taşır.
- Spot benzeri araçlar:
  - Yurt içi kaldıraçlı XAUUSD: SPK, 10:1, asgari 50.000 TL (r1). Swap maliyeti ve vergisi bu çalışmada doğrulanmadı.
  - ABD seansında GLD/IAU (Midas, ~10 bp gidiş-dönüş varsayımı). Saat uyumsuzluğu var; ABD kapanışı 23:00/00:00 TSİ.
  - M2 (geri vade) primi genellikle daha yüksektir (Mart 2026 eb2 medyanı 207 bp). Yüksek rejimde M2 uzunu M1'den yalnız ~3 bp/5 gün daha az kaybetti. Gerçek bir alternatif değil.

**Roll:**
- Uzun pozisyonu vadeye **5–10 iş günü kala** F_XAUUSDM2-M1 strateji emriyle taşıyın. M1'in son 5 gündeki yakınsama kaybı ortalama −10,8 bp; erken geçiş tarihsel olarak 17–26 bp daha iyi.
- Roll anında fazla takvim farkı > ~50 bp ise, yani r12 − UST3a ≳ 3 puan (2026'da Şubat, Nisan ve Haziran rolleri), roll etmek primi kilitlemek demektir. Pozisyonu kapatıp spot benzeri araca geçmeyi, ya da roll'u prim düşene kadar ertelemeyi değerlendirin.
- Vade günü (son işlem günü) uzlaşması LBMA PM'dir; 31 Aralık'ta AM fiyatı olabilir. Primle aldığınız kontratı vadeye kadar tutarsanız primin tamamını kaybedersiniz. 0226'da son 20 günde bu −267 bp idi.

## 7. Zayıflıklar ve bulunamayanlar

- Yüksek rejimin 136 gününün 58'i 2026'da, büyük kısmı Ocak–Mart 2026'daki tek bir dönemde. Bağımsız dönem sayısı az (2020, 2023, 2026). Canlı ölçüm testi (5.3) yalnız bu dönemi kapsıyor.
- Fazla baz, UST 3 aya göre ölçüldü. Türk karşı tarafların gerçek USD fonlama maliyeti (SOFR + kredi primi) ve altın kira oranı ölçülmedi. Normal dönemdeki 0,5–1,5 puanlık fazla oranın bir kısmı bunlar olabilir; bu hipotez test edilmedi.
- Dukascopy BID kotasyonu orta fiyattan ~1 bp aşağıda. 15:00 ile 15:10 arasındaki zaman gürültüsü MAD 6 bp.
- **Bulunamadı:**
  - XAUUSD'ye özgü yatırımcı tipi (yerli/yabancı, bireysel/kurumsal) istatistiği.
  - Hesap bazında pozisyon limiti.
  - XAUUSD piyasa yapıcı sayısı ve kapasitesi.
  - Günlük Kapalıçarşı/KMKTP prim serisi.
  - 12.500 $/kg için Reuters kaynağı (yalnız GZT bulundu).
  - "VİOP ons altın prim" konulu Türkçe basın açıklamaları (arama bütçesi tükendi).
  - TCMB'nin Mart 2026 altın swap/satış rakamlarının birincil kaynağı.

## 8. Kaynaklar

Birincil (bu çalışmada okundu ya da indirildi):
- BIST VİOP günlük bülteni (kontrat bazında uzlaşma, OHLC, OI): https://www.borsaistanbul.com/data/vadeli/viop_YYYYAAGG.csv (panel `viop_long.parquet`)
- BIST veri dosya dizini: https://www.borsaistanbul.com/files/datafilepaths_viop.zip
- BIST VİOP yerli/yabancı dağılımı: https://www.borsaistanbul.com/data/vadeli/viopyyishac202610.zip, https://www.borsaistanbul.com/data/vadeli/viopyyishac202512.zip
- BIST VİOP aylık üye bazında hacim: https://www.borsaistanbul.com/data/vadeli/viopaylikishac202601.zip (ve 202510, 202602, 202603, 202605, 202608, 202610)
- BIST KMTP aylık piyasa raporları: https://borsaistanbul.com/files/aylik-piyasa-raporu-ekim-2026.pdf, https://www.borsaistanbul.com/files/aylik-piyasa-raporu-mart-2026.pdf, https://www.borsaistanbul.com/files/aylik-piyasa-raporu-ocak-2026.pdf
- BIST KMKT veri sayfası: https://borsaistanbul.com/veriler/kiymetli-madenler-ve-kiymetli-taslar-piyasasi
- BIST duyuru 12590 (17.09.2020; ons altın akşam seansı 18.09.2020'den itibaren): https://borsaistanbul.com/duyuru/12590/usdtry-vadeli-islem-sozlesmelerinde-esnek-sozlesme-olusturma-ozelliginin-devreye-alinmasi-dolarons-altin-vadeli-islem-sozlesmelerinin-aksam-seansinda-islem-gormesi-ve-viop-proseduru
- BIST duyuru 30572 (19.11.2024; konu bakır vadelisi). Eki Prosedür md.7 "Akşam Seansına Dahil Olan Sözleşmeler" listesinde Dolar/Ons Altın var: https://borsaistanbul.com/files/duyuru-30572-TR.pdf
- BIST duyuru 11834 (vade sonu uzlaşma = LBMA PM): https://borsaistanbul.com/duyuru/11834/viopta-altina-dayali-sozlesmelerde-vade-sonu-uzlasma-fiyatina-iliskin-guncelleme-yapilmistir
- TCMB DUY2026-10 ve DUY2026-11 (01.03.2026): https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Duyurular/Basin/2026/DUY2026-10 , https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Duyurular/Basin/2026/DUY2026-11
- NY Fed SOFR: https://markets.newyorkfed.org/api/rates/secured/sofr/search.json?startDate=2018-04-02&endDate=2026-11-07 ; FRED DTB3: https://fred.stlouisfed.org/graph/fredgraph.csv?id=SOFR,DTB3,TB3MS
- Dukascopy dakikalık: https://datafeed.dukascopy.com/datafeed/XAUUSD/2026/00/29/BID_candles_min_1.bi5 (örnek gün)
- SPDR Gold Trust NAV geçmişi (LBMA PM tabanlı NAV): https://www.spdrgoldshares.com/usa/historical-data (panel `etf_gld_navhist.parquet`)
- Yahoo GC=F saatlik: https://query1.finance.yahoo.com/v8/finance/chart/GC=F?range=730d&interval=1h

İkincil ya da önceki raporlardan devralınan (bu çalışmada yeniden okunmadı):
- r1 (Prosedür rev. 70, Takasbank GM 2126/2150, QNB teminat): `research/r1_viop_kontrat.md`
- r4 (TCMB Mart 2026, WGC, kur): `research/r4_turkiye_altin.md`; r7 (TCMB olay takvimi): `research/r7_olay_takvimi.md`
- GZT 25.02.2026 (bu çalışmada okundu): https://www.gzt.com/ekonomi/25-subat-2026-altin-fiyatlari-gram-altin-fiyati-bugun-ne-kadar-iste-kapalicarsi-rakamlari-4019837

## 9. Dosyalar

Hepsi `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/g1_viop_prim/` altında:
- Kod (`code/`): `dl_duka_min_g1.py`, `g1_00_parse_min.py`, `g1_01_quality.py`, `g1_02_carry.py`, `g1_03_tests.py`, `g1_04_roll.py`, `g1_05_monthly.py`, `g1_06_sameday.py`, `g1_07_fdr.py`; hepsini `run_all.sh` çalıştırır.
- Tablolar:
  - Taşıma: `carry_daily.parquet`, `carry_monthly.csv`, `carry_yearly.csv`.
  - Veri kalitesi: `q_daily.parquet`, `q_peak_days.csv`, `q_gld_anchors.csv`.
  - Testler: `eb_daily.parquet`, `t_tests_all.csv`, `t_bucket_relf.csv`, `t_backtests.csv`, `t_contemp.csv`, `sameday_minute.csv`, `sameday_minute_summary.csv`.
  - Roll: `roll_convergence.csv`, `roll_cost.csv`, `roll_early_late.csv`, `m1_vs_m2.csv`, `arb_path.csv`.
  - Sürücüler: `monthly_drivers.csv`, `member_precmet_usd.csv`.
  - Kayıt: `registry_with_q.csv`.
- Loglar: `log_g1_0*.txt`. Ham indirmeler: `dl_m/` (Dukascopy), `dl_web/` (SOFR, FRED), `dl_bist/` (BIST zip/xlsx/pdf).
