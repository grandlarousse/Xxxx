# v_M4_a — Bağımsız doğrulama: JP/AU çelik-madenci z-kompoziti (t) → EREGL/KRDMD gün-içi (t)
Doğrulayıcı: v_M4_a · Tarih 02.11.2026 · Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_M4_a/` (v.py = kendi yardımcı modülüm; ll.py/mh.py import EDİLMEDİ, ham parquet'ten okundu). Sonuç dosyaları aynı dizinde `res_s*.csv`.

## KARAR: DÜZELT — rakamlar birebir tekrarlanıyor, zamanlamada ileriye bakma yok. Ama işlem iddiası şişirilmiş. Yeni güven: işlem için DÜŞÜK; istatistiksel ilişki için ORTA.

### 1. Yeniden üretim (s1)
Tanımlar kaynak koddan alındı (a4_bt.py):
- Her bileşen için BIST takvimli log getiri hesaplandı. Sıfır getiriler NaN yapıldı. 12σ sıçrama temizliği uygulandı.
- Bileşen z-skoru, geçmiş 250 günle hesaplandı (shift 1). Kompozit = z'lerin ortalaması.
- Kompozit, hedefle birleştirildikten sonra tekrar 250 günlük geçmiş z'ye çevrildi. |z|>1 ise pozisyon = işaret.
- Hedef: intra = log(c/o), 2014 ve sonrası. Fiyat bazında ±%10,5 dışı ve gap dışı günler atıldı.

| | IS bps (t) | OOS bps (t) | OOS Sharpe | Kaynak |
|---|---|---|---|---|
| EREGL, \|z\|>1, 15 bps | +12,1 (1,47) | **+27,7 (2,34)** | 1,02 | aynı |
| KRDMD, \|z\|>1, 15 bps | +26,3 (2,33) | **+32,1 (2,18)** | 0,96 | aynı |
| EREGL hedge (tam-örneklem beta), 15 bps | −0,8 | +14,3 (1,61) | | aynı |
| KRDMD hedge, 15 bps | +12,5 | +15,5 (1,33) | | aynı |
| FMG.AX(t)→intra korelasyonu: KRDMD / EREGL / BRSAN | r 0,081 / 0,067 / 0,056; t 4,38 / 3,87 / 3,51 (OOS t 3,78 / 3,26 / 2,48) | | | aynı |

Değerlendirme:
- Kendi hizalamam ll ile aynı sonucu verdi. Kütüphane hatası bulunmadı.
- FX bu iddiada kullanılmıyor, yani FX kayması burada etkili değil.

### 2. Zamanlama / ileriye bakma denetimi (s3, h1 verisi indirildi: 5411.T, 5401.T, 6301.T, BHP.AX)
Kapanış saatleri:
- **Tokyo:** son h1 barı 06:00 UTC'de başlıyor.
  - 2024-11-05 öncesinde günlük c, son barın kapanışına %99–100 eşit. Yani kapanış 06:00 UTC.
  - 2024-11-05 sonrasında eşitlik %15–19'a düşüyor. Günlük c artık 15:30 JST kapanış müzayedesi, yani **06:30 UTC**.
- **ASX:** Avustralya yaz saatinde (Eki–Nis) son bar 05:00 UTC, kışında 06:00 UTC. Günlük c, son bar kapanışına %95–100 eşit. Kapanış müzayedesi yaklaşık **05:10 / 06:10 UTC**.

BIST açılışı:
- m5 verisinde açılış müzayedesi barı 06:55 UTC'de. Emir toplama yaklaşık 06:40–06:55 UTC.
- Günlük `o`, h1 ilk bar açılışına %99,3–99,5 eşit (2023-12 ve sonrası). Yani `o` açılış müzayedesi fiyatı.

Sonuç: Tüm bileşenler BIST açılış müzayedesinden ÖNCE kapanıyor. **İleriye bakma yok.** Ancak marj dar:
- 2016 öncesinde TR yaz saatinde Tokyo/ASX ile marj yaklaşık 15–40 dk.
- 2024-11 ve sonrasında Tokyo ile marj yaklaşık 25 dk.
- Sinyal hesabı ve emir girişi otomatik olmalı.

Plasebo (kompozit t−1 → intra t): EREGL OOS +8 (t 0,7), KRDMD +3 (t 0,2). Etki aynı güne özgü.

Mevsim kırılımı (15 bps):
- Kas–Mar: EREGL +32 (t 2,85), KRDMD +42 (t 2,87).
- May–Eyl: EREGL +6 (t 0,56), KRDMD +10 (t 0,72).
- Marjın geniş olduğu aylarda etki daha güçlü. Bu bir ileriye bakma işareti değil.

**Alternatif giriş: h1 ilk bar kapanışı (06:30–07:30 barı, yaklaşık 07:30 UTC = 10:30 TSİ) → günlük kapanış.** Pencere 2023-12…2026-10, |z|>1, 197 işlem:

| Hisse | açılış girişi brüt / 15 bps net | 07:30 girişi brüt / 15 bps net | ilk 30 dk (o→07:30) brüt |
|---|---|---|---|
| EREGL | 23,4 / +8,4 (t 0,53) | 13,2 / **−1,8** (t −0,13) | 10,2 |
| KRDMD | 12,8 / −2,2 (t −0,13) | 10,4 / **−4,6** (t −0,28) | 2,4 |
| BRSAN | 31,1 / +16,1 | 0,1 / −14,9 | 31,1 (tamamı ilk 30 dk'da) |

Değerlendirme:
- Kısa pencerede açılış girişi bile maliyet sonrası yaklaşık sıfır.
- 07:30 girişinde net getiri negatif.
- Örneklem küçük (197 işlem), güç düşük.

### 3. Sağlamlık (s4, s5, s6, s7) — 15 bps, |z|>1, OOS bps (t)
**Seçim yanlılığı (kritik).** Kaynak ajan bileşenleri 2014–2026 TAM örneklem taramasından seçti (intra0_preopen, FDR; 72 Asya sembolü). Dolayısıyla OOS kirli.
- Aynı 72'lik evrende **yalnız IS (2014–2020) korelasyonuyla** seçilen ilk-5 ile OOS sonucu:
  - **EREGL +3,9 (t 0,35)**, KRDMD +19,0 (t 1,34).
  - İlk-3: EREGL +16,1 (1,26), KRDMD +6,5 (0,54). İlk-10: +10,4 / +7,5.
- Rastgele 5'li kompozit null'u (2000 çekiliş): OOS medyanı ≈0 bps, %95'lik dilim 15 / 20 bps.
  - JP_AU kompoziti OOS'ta %99,8 / %99,6. Bu yüksek persentil kısmen seçimin sonucu.
  - IS persentili %90 / %98.

**Bileşen bağımlılığı:**

| Varyant | EREGL OOS bps (t) | KRDMD OOS bps (t) |
|---|---|---|
| Tek bileşenler | +2,5 … +11,6 (t ≤ 1,04) | −5,5 … +19,8 |
| Komatsu (6301.T) çıkarılınca | +14,1 (1,26); IS +1,4 | +22,2 (1,57); IS +7,4 |
| A-priori çelik+cevher (5411, 5401, POSCO, Hyundai Steel, FMG, BHP, RIO; Komatsu yok) | +19,2 (1,59); IS +7,1 | **+36,1 (2,40)**; IS +14,2 |
| Geniş Asya endeksleri (N225, AXJO, KS11) | ≈0 | ≈0 |
| Japon çelik-dışı (MUFG, NTT, Toyota, Sony, SoftBank) | −13 | −14 |

Geniş endekslerde ve çelik-dışı Japon hisselerinde etki olmaması iyi haber: etki genel bir Asya risk iştahı faktörü değil, sektöre özgü.

**Eşik duyarlılığı (EREGL):**
- |z|>0,5: +4,2 (0,52).
- |z|>1,5: +30,7 (1,67), ama IS +0,1.
- KRDMD daha tutarlı: sırasıyla +16,6 / +37,8.

**Hedge (geçmiş 250 günlük beta, ileriye bakmasız; XU100):**
- EREGL OOS +12,3 (1,40), IS +3,3 (0,42).
- KRDMD OOS +16,6 (1,42), IS +16,3 (1,77).
- XU030 hedge'i benzer sonuç veriyor.

**Regresyon kontrolleri** (intra_t ~ kompozit_t + gap_t + kendi intra/cc_{t−1} + XU100 intra_{t−1} + SPX_{t−1} + SLX_{t−1}; NW t):
- Kompozit t: EREGL tam 4,08 / OOS 2,10; KRDMD tam 4,05 / OOS 2,41.
- N225 z_t eklenince OOS t: EREGL 1,67, KRDMD 2,32.
- Korelasyon düzeyinde ilişki kontrollere dayanıklı.

**Genişlik (47 VİOP hissesi, BH-FDR):** Geçenler KRDMD, EREGL, BRSAN ve AEFES. AEFES'te etki yalnız IS'te var, OOS'ta negatif. XUSIN t 4,5; XU100 t 2,2. Diğer hisselerde ≈0. Bu tablo çelik mekanizmasıyla tutarlı.

**Yoğunlaşma:**
- OOS kârının %71 (EREGL) / %81'i (KRDMD) en iyi 10 işlem gününden geliyor. Bu 10 gün hariç ortalama +10 / +12 bps.
- Kâr ağırlıkla short tarafında. OOS short: +49 / +56 bps; long: +6 / +8 bps.

**Yıllar (15 bps net, bps/işlem, yılda ~52–83 işlem):**
- EREGL: 2014 −6, 2015 +22, 2016 +7, 2017 +43, 2018 −3, 2019 +11, 2020 +11, 2021 +45, 2022 +73, 2023 +27, 2024 −10, 2025 +12, 2026 +16.
- KRDMD: 2014 +1, 2015 +19, 2016 +37, 2017 +39, 2018 +22, 2019 +44, 2020 +26, 2021 +53, 2022 +99, 2023 +47, 2024 +4, 2025 +7, 2026 −29.

Tokyo'nun 06:30 kapanış döneminde (2024-11 ve sonrası): EREGL +14,6 (t 0,72), KRDMD −11,4 (t −0,54). **Getirinin çoğu 2021–2023'te; etki zayıflıyor.**

### 4. Maliyet
- 8 bps'te OOS: EREGL +34,7 (2,93), KRDMD +39,1 (2,66).
- 25 bps'te OOS: +17,7 / +22,1 (t 1,50).
- OOS başabaş maliyeti: brüt EREGL 42,7, KRDMD 47,1 bps.

VİOP likiditesi (bülten 30.10.2026): EREGL ön iki vadede günlük ~0,9 + 0,9 milyar TL, KRDMD ~0,6 + 0,5 milyar TL. Bugün 0,01 TL'lik tik ≈ 2,7–3 bps; 8–15 bps varsayımı 2023 ve sonrası için makul.

**Ancak IS dönemi gerçekçi değil:** Yahoo'nun bedelsiz düzeltmeli fiyatlarıyla 0,01 TL tik, 2014–2020'de KRDMD için 25–78 bps, EREGL için 19–52 bps ediyor. Gerçek fiyat daha yüksekti, bu bir üst sınır. Yine de IS'teki "+26 bps net" KRDMD için uygulanabilir değildi. 2021'de tik ~11–14 bps.

### 5. Düzeltilmiş iddia
Aynı gün JP/AU çelik-madenci getirisi, EREGL/KRDMD gün-içi getirisini öngörüyor:
- Korelasyon r ≈ 0,08–0,09, NW t 4,6–4,9; IS t 3,6–3,7, OOS t 2,8–3,4.
- Gap ve ABD t−1 kontrolüyle de anlamlı.
- Sektöre özgü (geniş Asya endekslerinde yok), zamanlama temiz.

İşlem değeri ise iddia edilenden zayıf:
- Raporlanan OOS +27,7 / +32,1 bps, OOS dönemini de kapsayan tam örneklem bileşen seçimi içeriyor.
- Dürüst (yalnız IS) seçimle: EREGL +4 (t 0,35), KRDMD +19 (t 1,34).
- A-priori kompozitle: EREGL +19 (t 1,6), KRDMD +36 (t 2,4).
- Kâr birkaç büyük short gününde toplanıyor.
- 2024–2026'da sonuç ≈0 veya negatif.
- 07:30 girişinde 2023-12 ve sonrasında net negatif.

En savunulabilir sürüm: KRDMD, a-priori çelik+cevher kompoziti, yalnızca short ağırlıklı büyük |z| günleri. Bu da DÜŞÜK–ORTA güvende.

### 6. TradingView
- Bileşenler: TSE:5411, TSE:5401, TSE:6301, ASX:FMG, ASX:BHP.
- A-priori ekler: KRX:005490, KRX:004020, ASX:RIO.
- Hedefler: BIST:EREGL, BIST:KRDMD, BIST:BRSAN.
- VİOP sürekli kontrat kodu: '?' (doğrulanmadı).
