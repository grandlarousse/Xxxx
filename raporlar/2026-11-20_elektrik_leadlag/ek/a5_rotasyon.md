# A5 — XELKT / XU030 rotasyonu ve sektör zamanlaması (IS: 2010-01-04 → 2022-12-30)

**Taranan.** 96 tarih sinyali (S1 24, S2 6, S3 4, S4 8, S5 6, S6 48) × 3 hedef (sepet, likit10, VİOP üçlüsü) × h 1–3, AL; üçlüde ayrıca vadeli SAT. **1.152 ızgara testi** + yaklaşık 95 keşif testi. Ölçü: `own`, dolabilir.

**Bulgular**
- BH-FDR (q = 0,10): AL testlerinin hiçbiri geçmiyor. Aile düzeyi kaydırma testi: en iyi sonucun (zirve20 → üçlü h3) şansla çıkma olasılığı 0,082. Hüküm OOS'ta.
- Otokorelasyon (gecikme 1): XELKT 0,066, likit10 0,084, üçlü 0,048: likit sepette kaybolmuyor. Regresyon: XELKT(t−1) +0,10 (t 3,3), XU030(t−1) −0,06 (t −2,1). Tablo: `a5_rotasyon_otokor.csv`.
- Göreli güç: 1 günlük devam zayıf (t 1,9), 5–10 günlük dönüş yok; S5'te net pozitif satır yok. h = 1'de S1–S5 maliyeti geçmiyor; etki 2–3 güne yayılıyor.
- Piyasa-nötr (β × XU030 SAT; sinyal günü − bütün günler): zirve20 üçlü +85 (t 4,5), sepet +55 (3,6); mom1 sepet +52 (3,7).

**Ortak tanımlar.** z(x) = x(t) / std(x; t−60…t−1). Giriş t kapanışı, çıkış t+h kapanışı. Sepet = o gün dolabilir bütün XELKT üyeleri (≥ 5), eşit ağırlık; likit10 = adv60 sırasına göre en likit 10 dolabilir üye; üçlü = AKSEN, ENJSA, ODAS. Rakam sırası: fazla bps (t) | net temel | ≤2019 / 2020–22 | en iyi 10 gün hariç | t+1 kapanış girişi.

### DONDURULMUŞ KURAL 1 (birincil): A5_zirve20_viop3_h3
XELKT kapanışı(t) ≥ son 20 kapanışın (t dâhil) en yükseği → üçlü spot AL, h = 3. 547 gün (266 bağımsız): 69 (3,5) | +31 | 73 / 63 | 25 | 64. Pencere 10/40/60: 62/67/68. Vadeli fiyatıyla 70 (2,1). Mekanizma: kırılım sonrası alım 2–3 gün sürüyor. Zayıflık: ODAS ağırlıklı (114; AKSEN 49; ENJSA 24); 2021 negatif.

### DONDURULMUŞ KURAL 2 (birincil): A5_zirve20_sepet_h3
Aynı sinyal → sepet AL, h = 3: 46 (2,9) | +20 | 33 / 65 | 11 | 34.

### DONDURULMUŞ KURAL 3 (birincil): A5_mom1_sepet_h3
z(XELKT r_cc(t)) ≥ 1 → sepet AL, h = 3. 428 gün: 60 (3,5) | +27 | 81 / 18 | 23 | 26. Komşular: eşik 1,5 → 57; h2 → 41. Mekanizma: haberin yavaş yayılması, kısmen bayat fiyat. Zayıflık: 2020 ve 2021 negatif; 2020–22 brütü maliyetin altında.

### DONDURULMUŞ KURAL 4–5 (ikincil): A5_zirve20_likit10_h3, A5_mom1_likit10_h3
Aynı sinyaller → likit10 AL, h = 3. Zirve20: 50 (2,9) | +9 | 35 / 72 | 10 | 39. Mom1: 57 (3,1) | +18 | 78 / 15 | 16 | 26.

### DONDURULMUŞ KURAL 6 (ikincil): A5_gecikme1_viop3_h3
z(XU030 r_cc) ≥ 1 ve z(XELKT r_cc) < 0,5 → üçlü AL, h = 3. 140 gün: 80 (2,9) | +60 | 62 / 131 | 26 | 63. Zayıflık: piyasa-nötr fark 36 (t 1,5); sepette gecikme koşulu bilgi eklemiyor: piyasa momentumu.

### DONDURULMUŞ KURAL 7–8 (ikincil): A5_gunsonu1617_sepet_h1, A5_gunsonu1617_viop3_h3
x = XELKT(17:00)/XELKT(16:00) − XU030(17:00)/XU030(16:00); z(x) ≥ 1,5 (saatlik `h1_isy`; 17:00 değeri = 16:00 damgalı bar). 85 gün (2017+). Sepet h1: 50 (2,4) | +17 | 54 / 44 | 9 | 9; t+1 açılışından girişte 48. Üçlü h3: 121 (2,4) | +95 | 154 / 80 | 21 | 101. Zayıflık: 576 S6 testinden biri; 16:00 → kapanış sürümü doğrulamıyor; 2021 negatif.

### DONDURULMUŞ KURAL 9 (ikincil): A5_gunsonu1417_asagi_viop3_sat_h1
14:00 → 17:00 göreli getiri z ≤ −1,5 → üçlü vadeli SAT, h = 1 (`arac=viop`). 60 gün (%70'i ENJSA): 58 (2,0) | +25; vadeli fiyatıyla 55 (1,6); en iyi 10 gün hariç −13: yalnız izleme. Aynı günlerde sepet AL −59 (t −2,9): AL'dan kaçınma süzgeci.

**Elenenler.** S1 ve S5'in tamamı, dip ve aşağı yön sinyalleri, h = 1–2 sürümleri, diğer S6 pencereleri; gerekçeler CSV'nin `not` sütununda.

**Zayıflıklar.** Kurallar bağımlı (mom günlerinin %51'i zirve günü). Sinyal kapanış değeriyle kurulur: 17:00'de kapanış sinyalinin %89'u (zirve), %73'ü (mom) görülüyor. Birincillerde muhafazakâr maliyetle net −5…+6 bps. Hayatta kalma yanlılığı. S6 `h1_isy` yoksa sinyal üretmez. Sepet kuralları `min_n = 5` taşır.

**Öz-denetim.** `self_check_causal`: 9 kuralın hepsi 0,0. `build()` 0,1 sn, deterministik; `eval_rule` çıktısı tarama satırlarıyla aynı.
