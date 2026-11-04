# k_yurtici-takvim_curut — 'yurtici-takvim' taramasını çürütme denemesi

**Tarih:** 03.11.2026 · **Veri sonu:** 30.10.2026 · **Kod:** `out/code_k_yurtici-takvim_curut/` (curlib.py, c0–c7; tarayıcının klib.py'si import edilmedi) · **Testler:** `res/tests_all_curut.csv` (q sütunu)
**Test sayısı:** 433 kayıtlı test, hepsine BH-FDR (q=0,05, eşik |t| ≈ 2,47; 120 test geçti, çoğu aynı ailenin varyantı). Ayrıca plasebo evreni olarak VİOP47'nin 2.162 sıralı çifti tarandı; bunlar hipotez değil, plasebo dağılımıdır. Yatırım tavsiyesi değildir.

## Bağımsız kurgu (tarayıcıdan farkları)
- **Sözleşme kimliği:** (dayanak, vade). N1 (bedelsiz düzeltmeli) kodlar aynı vadenin devamı sayıldı. Bültende prev_settle = dünkü uzlaşma; düzeltme günlerinde N1 kodunun prev_settle değeri düzeltilmiş.
- **Vade seçimi:** vade > çıkış günü (kesin büyük). Tarayıcı ≥ kullanmıştı; burada daha katı.
- **Giriş/çıkış:**
  - E0 = uzlaşma_t.
  - E1 = son işlem_t (işlem > 0 olan günlerde).
  - E2 = uzlaşma_{t+1}.
  - Çıkış uzlaşma_{t+h}.
- **XU030 kotasyonu:** 27.07.2020 öncesi vadeli /10 kotasyonlu (endeksten iki sıfır atıldı). Tarayıcının hazır baz panelini kullanmadım, ölçeği kendim düzelttim.
- **Saat kontrolü:** Borsa İstanbul dokümanına göre pay vadelisi 18:10'da, endeks vadelisi dahil diğer türevler 18:15'te kapanıyor. XU030 için "spot kapanışı (≈18:05–18:10) biliniyor, vadeli 18:15'e kadar açık" varsayımı geçerli.
- **Saatlik ızgara:** Yahoo .IS saatlik verisinde yalnız yaz ızgarasında 14:30 barı 18:00 TSİ'de bitiyor (müzayede öncesi). Kışın son bar 13:30. Müzayede hareketi (CA) yalnız yaz günlerinde ölçülebiliyor.
- **Uzlaşma = VWAP:** Sinyal uzlaşma fiyatından kuruluyor ve aynı uzlaşmadan giriliyorsa bu ileriye bakmadır. Tarayıcının çift testinde (k6) VİOP sinyali vadeli uzlaşma getirilerinden kurulmuş ve E0'da aynı uzlaşmadan girilmiş. TCELL–TTKOM'da bunu ayrıca test ettim.

## Aday bazında hüküm

| # | Aday | Tarayıcı | Bağımsız sonuç (ana kural) | Çürütme testleri | Hüküm |
|---|---|---|---|---|---|
| 1 | XU030 kapanış bazı sıçraması (h1) | UYGUN / ORTA | E1 +24,7 bps (t 2,87), n=607; E0 +19,2 (t 2,27); E2 −2,5 | Simetrik budama ±10: +23,0 (t 3,32). Rastgele tarih plasebosu %99 = +17,5 (p<0,001). Izgara 12/12 pozitif (E1 t 2,4–3,1). q=0,024. Dönemler: 17–19 +38 (t 3,3) · 20–21 +9 · 22–23 +42 · 24–26 +17 (t 1,1). Eğim −0,76 → −0,36 → −0,27 | **UYGUN / ORTA** (etki küçülüyor) |
| 2 | Koza grubu göreli momentum | KOŞULLU / ORTA | E0 h2 +44,6 (t 4,05); E2 h2 +29,9 (t 2,59), 8/8 yıl | Ayrıntılar aşağıda | **KOŞULLU / ORTA** (küçük boyut) |
| 3 | Pay vadelisi baz sapması | KOŞULLU / ORTA | Kesitsel, 2022-09+ A sınıfı: E1 h1 +11,7 (t 3,8), E0 +5,7 (t 1,9), net ≈ +5 / −1 bps | Tek bacak \|z\|>1,5 tekrar etmiyor: +12,5 (t 0,95), E0 +5,9, E2 −5,3 (tarayıcı +39,6, t 2,6) | **Strateji olarak UYGUN DEĞİL.** Yalnız yürütme ipucu: KOŞULLU / DÜŞÜK |
| 4 | TCELL–TTKOM göreli dönüş | KOŞULLU / DÜŞÜK | Tarayıcı kurgusu (vadeli sinyal) E0 h3 +39,5 (t 2,67), E2 +27,3 (t 1,67). Spot sinyal E0 +34,7 (t 2,25), E2 +23,5 (t 1,44) | Ayrıntılar aşağıda | **UYGUN DEĞİL / DÜŞÜK** |
| 5 | KCHOL NAV sapması | KOŞULLU / DÜŞÜK | E0 h3 +11,4 (t 2,36); E2 +7,9 (t 1,62); 2017–21 −1 (t −0,2) | Sinyal günlerin %56'sında açık. Maliyet sermaye başına ~6 bps, net E0 ~+5, E2 ~+2. Spot da 2017–21'de ≈0 | **UYGUN DEĞİL / DÜŞÜK** (tek başına) |
| 6 | Temettü öncesi (spot) | KOŞULLU / ORTA | VİOP verim ≥ %4: +5 (t 0,09); tümü −4 | Spot yüksek verim 2010+: +73 (t 2,9); 2017+: +75 (t 2,1), en iyi 10 çıkınca +1. Profilde spot kapanış müzayedesi dolumu geçersiz | **UYGUN DEĞİL** |
| 7 | Ay dönümü XU030D1! | KOŞULLU / DÜŞÜK | E0 h1 +44,2 (t 2,42), n=115; E2 +8 | Ayrıntılar aşağıda | **KOŞULLU / DÜŞÜK** |

### Aday 1 — XU030 kapanış bazı sıçraması: ek kontroller
- **Ayrıştırma:** y1 ≈ −0,37·r_F + 0,37·r_S, yani etkiyi taşıyan baz değişimi.
- **2023-11+ yaz günleri:** y1 ~ Δb −0,50 + CA +1,0. Spot müzayede hareketini vadeli ertesi gün tam yakalıyor; mekanizma tutarlı.
- **Yalnız AL:** +28,5 (t 2,9), budamada da sağlam.
- **Maliyet:** 4,8 bps ile net ≈ +20 bps.

### Aday 2 — Koza grubu göreli momentum: çürütme testleri
- **Simetrik budama ±10:**
  - E0 h2: +43,6 (t 5,3).
  - E2 h2: +31,7 (t 3,5).
- **Kilitli günler:** limitte kilitli günler çıkarılınca E0 h2 +41,8 (t 3,8). Sinyal günlerinin yalnız %3,9'u kilitli.
- **Bağımsız olaylar:** 283 sinyal günü, 120 bağımsız olay. Yalnız olayın ilk günü girilirse:
  - E0 h2: +33,9 (t 3,1).
  - E2 h2: +25,3 (t 1,8).
- **Rastgele tarih plasebosu:** p<0,001.
- **Plasebo evreni (2.162 çift, tek hedge):**
  - TRMET/TRALT E0'da en üst %0,1'de.
  - E2'de en üst %8'de.
  - Genel E2 momentumu bütün çiftlerde ortalama +8 bps.
- **Spot uzun geçmiş:** 2010–16 ters işaretli. Momentum yalnız 2017'den beri var.
- **Dönemler (E0 h2):** 2019 +102 · 20–21 +43 · 22–23 +52 · 24–26 +21 (t 1,2).
- **Maliyet:** sermaye başına küçük emirde 7,4, ihtiyatlı 10,4, 1 mn TL'de 21 bps.

### Aday 4 — TCELL–TTKOM: çürütme testleri
- **Getiri tek döneme yığılı:** kazanç 2020–21'de (+93…+120). 2017–19 ve 2022–23 sıfır ya da negatif.
- **Budama:** E2 simetrik budamada t 1,9–2,2.
- **Kurguya duyarlılık:**
  - Kaldıraçlı log-fiyat yayılımı ≈ 0.
  - Z60 / β=1 varyantı güçlü görünüyor ama sonradan seçilmiş.
- **q:** E2 h3 için 0,17–0,24.
- **İleriye bakma payı:** vadeli sinyalle E0 girişindeki ileriye bakma etkisi küçük (spot sinyalli E0 benzer).

### Aday 7 — Ay dönümü: çürütme testleri
- **Rastgele gün plasebosu:** p=0,006.
- **Budama:**
  - Simetrik budama +37 (t 3,1).
  - Yalnız en iyi 10 çıkınca +7 (t 0,5).
- **Dönemler:** 17–19 −7 · 20–21 +82 · 22–23 +104 · 24–26 +26 (t 0,8).
- **Komşu gün:** ME−1 −21 (t −1,6).
- **Spot XU100 2005–20:** +12 (t 0,9).
- **FDR:** q=0,052, geçmiyor.

## UYGUN DEĞİL (tarayıcının listesi) — yeniden hesaplanmadı, gerekçeyle onaylandı
- **Tavan/taban:** kârlı yön dolmuyor; dolan yön kaybettiriyor. Yalnız bir risk kuralı olarak kullanılabilir.
- **Hisse bazında kapanış müzayedesi dönüşü:** VİOP'ta dönüş yok. Dönüş yalnız spotta var ve açığa satış ile kapanış dolumu gerektiriyor.
- **Genel çift dönüşü:** havuzda dönüş yok. Plasebo evreninde ortalama dönüş E0'da −16, E2'de −9 bps; yani 1–3 günde genel bir dönüş yok, tersine hafif momentum var.
- **Bayram ve endeks değişikliği:** bayram etkisi yok; BIST30 değişikliğinde n=18.

## Dosyalar
- **Kod:**
  - `curlib.py`
  - `c0_cache.py` (ileri getiri önbelleği)
  - `c1_xu030.py`
  - `c2_koza.py`
  - `c3_evren_plasebo.py`
  - `c4_tcell_kchol.py`, `c4b_tcell_fut_signal.py`
  - `c5_ay_temettu.py`
  - `c6_baz.py`
  - `c7_ozet.py`
- **Kayıtlar:** `log_c*.txt`
- **Sonuçlar:** `res/tests_*.csv`, `res/tests_all_curut.csv`, `res/evren_plasebo.csv`
