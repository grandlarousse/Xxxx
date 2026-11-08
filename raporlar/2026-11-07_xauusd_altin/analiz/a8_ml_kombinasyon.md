# a8 — Çok değişkenli birleştirme ve makine öğrenmesi: VİOP F_XAUUSD, 1/3/5 gün, uzlaşmadan uzlaşmaya

Ajan anahtarı: `a8_ml_kombinasyon`. Tarih: 2026-11-08. Bütün kod ve çıktılar bu dizinde (`run_all.sh` hepsini sırayla yeniden üretir, ≈40 dk tek çekirdek).

## 0. Özet

1. **Ana sonuç: hiçbir model, örneklem dışında rastgele yürüyüşü (sıfır getiri tahmini) ya da tarihsel ortalamayı anlamlı biçimde yenmiyor.** Denenen modeller, üç ufukta: ridge, lasso, elastic net, HistGradientBoosting, random forest, bunların eşit ağırlıklı topluluğu, önceden belirlenmiş basit sinyallerin z-skoru birleşimi (C1) ve IC işaretli birleşimler (C2).
2. VİOP panelinde eğitilen modeller (V1, 103 öznitelik, ilk eğitim 2017-03..2019-12) 2022+ OOS'ta 27 model×ufuk kombinasyonunun **hiçbirinde** pozitif Campbell–Thompson R² (tarihsel ortalamaya karşı) vermedi. En iyisi −%0,02 (C1). Clark–West t hiçbir kombinasyonda 1,645'i geçmedi (en yüksek 1,17).
3. 2011'den beri spot panelde eğitilen modeller (V2) 2022+'da 13/27 pozitif R² verdi; en yüksek +%0,46 (HGB h=1, CW t 1,69). Aynı modeller 2020–21 doğrulama döneminde negatif R² verdi; en iyisi +%0,04, HGB h=1'de −%3,2. Zamanlama Sharpe'ları VAL'de −1,1..−1,6. İstikrarsızlar.
4. Erken dönem tekrarında (V3: eğitim 2011–12, test 2013–16, spot) 27 kombinasyondan yalnız 1'i pozitif R² verdi (ridge h=5, +%0,01).
5. Doğrulama döneminde (2020–21) en iyi modeli seçip OOS'ta bir kez değerlendirdik. Seçilen modellerin 2022+ sonuçları:
   - h=1 lasso: R² −%0,22, Sharpe −0,91;
   - h=3 ridge: R² −%1,20, Sharpe −0,18;
   - h=5 C2: R² −%0,52, Sharpe −0,46.
6. Ambargolu iç doğrulama çoğu yeniden eğitimde ridge cezasını ızgaranın üst ucuna (1e4–3e5) itti. Lasso h=1'de aylık eğitimlerin %64'ünde (V1) ve %90'ında (V2) hiç öznitelik seçmedi. Veri, tahmini tarihsel ortalamaya büzmeyi tercih ediyor.
7. Tek değişkenli tarama 103 öznitelik × 3 ufuk = 309 test yaptı. |t|≥2 çıkan test sayısı 15; şansla beklenen 14,1. |t|≥3 olan tek bir test var (2s10s eğim değişimi). 2011–2016 erken dönemde 12 adayın 9'unda işaret tersine döndü ya da etki sıfırlandı.
8. En tutarlı tek değişkenli bulgu `rt_nom2_d5`: ABD 2 yıllık getirisinin t-6→t-1 değişimi, ters işaretle, h=1. Spot 2011–2026'da t=−2,61 ve 16 yılın 12'sinde aynı işaret. VİOP'ta tam dönem t=−2,36, OOS t=−2,48, ama IS t=−0,26. Güven DÜŞÜK.
9. Önceden belirlenmiş C1 birleşiminin bileşenleri: r20, r250, −ΔDXY5, −Δreal10_5, +ΔŞanghay primi5, −COT z. C1 2020+'da zamanlama Sharpe'ı 0,74 verdi; demeaned 0,65, buy & hold 0,50.
   - Ayrıştırma bu kazancın **yıl düzeyindeki trendi yakalamaktan** geldiğini gösteriyor, 1–5 günlük öngörüden değil.
   - Her yılın kendi ortalaması çıkarılınca Sharpe 0,25'e düşüyor.
   - 2017–19'da Sharpe −0,76; IC t=1,06; yılların yalnız 2/9'unda aynı işaret.
   - Güven DÜŞÜK.
10. Permütasyon önemi: OOS R² negatif olduğu için önemin ekonomik anlamı yok. Fiyat ve COT grupları ağaç modellerinde OOS'ta zarar veriyor (karıştırınca MSE düşüyor). Pozitif katkılar MSE'nin ≲%1'i.
11. Sağlamlık kontrolleri sonucu değiştirmedi; uç dönemler (Mart 2020, Ocak–Şubat 2026) dışarıda bırakılınca kalan küçük pozitiflikler zayıflıyor. Ayrıca bakılanlar: roll ve COT gecikme dışlamaları, 10 bps maliyet, örtüşmesiz alt örneklem, placebo. İleriye bakma izi yok.
12. **Toplam kayıtlı hipotez testi: 522** (`out/registry/a8_ml_kombinasyon.csv`). Bunların 518'inde t tanımlı. |t|≥2: 18 (bağımsızlık altında beklenen ≈23,6). Bu ajanın kendi testleri içinde BH-FDR en küçük q = 0,77. **Hiçbir test çoklu test düzeltmesinden sağ çıkmıyor.**

Pratik anlamı: kapanıştan kapanışa 1–5 günlük VİOP ons altın işlemi için, karar anında bilinen 103 öznitelikten makine öğrenmesiyle ya da doğrusal birleştirmeyle çıkarılabilecek, maliyet sonrası güvenilir bir yön kenarı **bulunamadı**. Görülen pozitif Sharpe'ların çoğu altının 2020–2026 boğa piyasasında uzun kalmaktan geliyor (drift tuzağı).

---

## 1. Kurulum

- **Hedef:** `fwd{h}`, yani VİOP aktif kontrat uzlaşma log getirilerinin t+1..t+h toplamı. Giriş gün t uzlaşması (≈15:05–15:15 UTC VWAP), çıkış t+h uzlaşması. Spot panelde (V2, V3) eğitim hedefi `sfwd{h}` (15:00→15:00 UTC spot). V2'nin tahminleri yine VİOP `fwd{h}` ile değerlendirildi.
- **Karar anı:** gün t 15:00 UTC. Bütün öznitelikler bu andan önce ya da tam 15:00'te kapanan saatlik barla bilinir (§2).
- **Dönemler:**
  - takvim IS = 2017-03..2021-12, OOS = 2022-01..2026-11;
  - ML testleri 2020-01'de başlıyor;
  - 2020–21 = **doğrulama (VAL)**; takvim olarak IS'te, model seçimi yalnız burada yapıldı;
  - 2022+ = OOS, tek sefer değerlendirildi;
  - erken dönem: V3 2013–2016.
- **Maliyet:** 5 bps gidiş-dönüş (stres 10 bps). `lib_altin.backtest` kademeli (örtüşen h alt portföy) uygulamasıyla.
- **Drift kontrolü:** her strateji için buy & hold Sharpe, demeaned Sharpe (getiriden dönem ortalaması çıkarılır), uzun ve kısa bacak ayrı. C1 için ayrıca **yıl-içi demeaned** Sharpe: her yılın kendi ortalaması çıkarılır. Bu yalnız atıf tanısıdır, işlem kuralı değildir.

## 2. Öznitelikler ve bilgi zamanı (UTC)

103 öznitelik (`oznitelik_bilgi_zamani.csv`). Spot türevli olanlar 2010'dan başlayan spot endeksinde hesaplandı ve VİOP günlerine as-of (yalnız geçmişe dönük ffill) taşındı.

Bilgi zamanı doğrulaması (`bilgi_zamani_kontrol.csv`):
- Kullanılan bütün Yahoo serilerinde `_avail` damgası satır satır kontrol edildi ve hepsi gün t 15:00'ten önce.
- En kısa önde olma süresi 14 saat (FX/kripto t-1 24:00 bar sonu); hisse ve ETF'lerde 17–18 saat.
- COT (rapor tarihi + 3 gün 21:00) ve SHFE (tarih ≤ t, 07:00 UTC) %100 cutoff öncesi.

| Grup | Öznitelikler | Kaynak | Bilgi zamanı (UTC) | Set |
|---|---|---|---|---|
| fiyat (24) | px_r{1,2,3,5,10,20,60,120,250}, px_vol20/60, volratio, r1z, r5z, px_ma{5..200} uzaklık, RSI2/14, dd250, hi20 | `xau_p15` | gün t 15:00 (Dukascopy bar 14:00–15:00 kapanışı) | A |
| seans (10) | seg_uspm_prev (t-1 15→20), seg_eve (t-1 20→t 00), seg_asia (00→07), seg_london (07→12), seg_nyam (12→15), seg_last1h (14→15); Asya/ABD 5 ve 20 günlük toplamlar | `xau_pHH` | en geç t 15:00 | A |
| çapraz Yahoo (23) | DXY, S&P 500, gümüş (SI=F), GDX, petrol (CL=F), bakır (HG=F), TLT, EEM, AUD 1 ve 5 günlük log değişim; GDX−GLD göreli; GLD/SLV oranı sapması; BTC (set B) | `y_*` | ABD kapanışı t-1 (≈20:00–21:15 t-1); FX/BTC t-1 24:00 | A (BTC B) |
| oynaklık (5) | VIX, GVZ: 1 günlük değişim, 60 günlük ortalamadan sapma; GVZ − gerçekleşen oynaklık | `y__VIX`, `y__GVZ` | t-1 16:15 ET | A |
| faiz (9) | nom10, real10, be10, nom2: 1 ve 5 günlük değişim; 2s10s eğim 5 günlük değişim | `ust_*` | t-1 22:00 | A |
| COT (4) | mm_net/oi seviye, 52 haftalık z, 1 haftalık değişim; swap z | `cot_gold_*` | Cuma 21:00 (rapor Salı) | A |
| Şanghay (3) | prim (AU0×31,1035/USDCNH07 vs xau_p07): 20 günlük sapma, 1 ve 5 günlük değişim; SHFE kapalıysa boş | `shfe_AU0_c`, `dk_USDCNH_p07` (2016 öncesi `y_CNY_X`) | t 07:00 | A |
| takvim (7) | Pazartesi–Perşembe kuklası, ay dönümü (son gün + ilk 3 gün), ay sin/cos | takvim | önceden bilinir | A |
| GPR (1) | log(MA7/MA30); **panelde sabit, kullanılamadı** | `gpr_*` | D+1 23:00 | A |
| dk 15:00 (10) | DXY, EUR, JPY, T-bond, S&P, gümüş, bakır, BTC, CNH, TRY: 24 saatlik (t-1 15:00→t 15:00) değişim | `dk_*_p15` | t 15:00 | B |
| VİOP t-1 (7) | vade gün sayısı, roll günü, hacim ve AP değişimi (t-1), baz (t-1 uzlaşma − t-1 15:00 spot), gram altın primi sapması (t-1), VİOP USDTRY getirisi (t-1) | `v_*`, `vo_*`, `tr_prem_matched` | t-1 15:10–15:15 ya da önceden bilinir | B |

**Gün t'de `v_*`/`vo_*` (15:10 değeri) hiçbir sinyalde kullanılmadı.** Bütün VİOP öznitelikleri t-1'e kaydırılmış sürümler. Set A = 2010'dan beri mevcut olanlar (V2, V3). Set B = A + dk + VİOP t-1 + BTC (V1).

## 3. Yöntem

- **Genişleyen pencere, ayda bir yeniden eğitim.** Test ayı M'nin ilk günü T0 için eğitim etiketleri yalnızca t+h ≤ T0−1 olan satırlar. Bu h günlük ambargo örtüşen etiket sızıntısını engeller (`02_walkforward.py`).
- **Standardizasyon** yalnız eğitim penceresinin ortalama ve standart sapmasıyla yapıldı; ±5σ kırpma uygulandı.
  - Eğitim penceresinde %50'den az dolu ya da sabit sütunlar düşürüldü.
  - Eksik değerler z=0 (eğitim ortalaması) ile dolduruldu; HGB eksikleri yerel olarak işler.
- **Hedef** eğitimde %1/%99 winsorize edildi (önceden sabit). CT tarihsel ortalama kıyası ham eğitim ortalamasıyla yapıldı.
- **Modeller** (hiperparametreler önceden sabit; `models.py`):
  - **ridge:** α ızgarası 10^0..10^5,5.
  - **lasso (l1=1) ve elastic net (l1=0,5):** α_max×10^(−2,5..0).
  - Ridge/lasso/EN cezaları eğitim penceresinin son %25'inde, h günlük boşlukla iç doğrulamayla seçildi.
  - **HGB:** 150 iterasyon, öğrenme hızı 0,03, derinlik 3, yaprak ≥50, L2=1.
  - **RF:** 200 ağaç, derinlik 5, yaprak ≥50, max_features 0,33, n_jobs=1.
  - **Topluluk (ens_ml):** beş ML modelinin ortalaması.
  - **C1 (a priori):** +px_r20, +px_r250, −xa_dxy_d5, −rt_real10_d5, +sh_prem_d5, −cot_mm_z52. İşaretler literatür ve mekanizmadan seçildi, veriden değil. Eğitim penceresinde z-skoru alınıp ±3'te kırpıldı ve eşit ağırlıkla birleştirildi.
  - **C2:** bütün özniteliklerin eğitim penceresi Spearman IC işaretiyle eşit ağırlık (all) ya da yalnız |IC|·√(n/h) > 2 olanlar (sel).
- **Sinyaller:**
  - "Ham" pozisyon = sign(ŷ). Boğa piyasasında neredeyse hep uzun olduğu için drift'i taşır.
  - "Zamanlama" pozisyonu = sign(ŷ − modelin kendi taban tahmini, yani winsorize eğitim ortalaması). Sıfır öznitelikli model pozisyon almaz.
  - C1/C2'de zamanlama = sign(skor).
  - Raporlanan Sharpe'lar zamanlama Sharpe'ıdır.
- **Ölçütler** (`common.py`):
  - Campbell–Thompson OOS R², tarihsel ortalama kıyasıyla (R²_hm) ve sıfır kıyasıyla (R²_0, rastgele yürüyüş) ayrı ayrı;
  - Clark–West t (NW lag ≥ max(h,5));
  - yön isabeti ve "hep uzun" temel isabeti;
  - Spearman IC ve NW t;
  - 5 ve 10 bps sonrası Sharpe (ham ve demeaned), uzun ve kısa bacak, buy & hold;
  - yıl yıl Sharpe ve IC.
- **Varyantlar:**
  - V1: VİOP paneli, set B, eğitim 2017-03'ten.
  - V2: spot paneli, set A, eğitim 2011-01'den, tahmin VİOP günlerinde.
  - V3: spot, set A, eğitim 2011–12, test 2013–16.

## 4. Bulgular

### 4.1 Tek değişkenli tarama (309 test; `01_univariate.py`, `univariate_viop.csv`)

|t|≥2 olan 15 test var; şansla 14,1 beklenir. |t|≥3 olan 1 test var; şansla 0,8 beklenir. En yüksek |t| değerleri ve bağımsız 2011–2016 spot tekrarı:

| öznitelik | h | IC | t (VİOP 2017+) | t IS | t OOS | yıl aynı işaret | t 2011–16 spot | t 2011–26 spot (yıl) |
|---|---|---|---|---|---|---|---|---|
| rt_curve_2s10s_d5 (+) | 1 | 0,063 | 3,03 | 1,50 | 2,53 | 6/10 | **−1,31** | 1,30 (10/16) |
| xa_gdx_rel1 (+) | 3 | 0,055 | 2,68 | 1,99 | 1,96 | 8/10 | −0,08 | 1,89 (11/16) |
| xa_aud_d5 (−) | 1 | −0,055 | −2,68 | −2,03 | −1,79 | 8/10 | **+1,72** | −0,41 (9/16) |
| seg_last1h (+) | 5 | 0,055 | 2,54 | 1,32 | 2,05 | 7/10 | 1,16 | 2,51 (13/16) |
| rt_nom2_d5 (−) | 1 | −0,049 | −2,36 | −0,26 | −2,48 | 6/10 | −1,61 | **−2,61 (12/16)** |
| cal_mcos | 3 | 0,070 | 2,34 | −0,02 | 3,23 | 6/10 | −0,49 | — |
| cot_mm_z52 (−) | 5 | −0,032 | −0,85 | — | — | 4/10 | −1,33 | −1,28 (9/16) |

Tek değişkenli sinyallerin işlem karşılığı (`08_univ_bt.py`; pos = sign(işaret×x), net 5 bps):

| sinyal | h | Sharpe 2017+ | demeaned | uzun / kısa | IS | OOS | OOS dm | OOS 10bps | B&H | spot 2011–16 |
|---|---|---|---|---|---|---|---|---|---|---|
| −rt_nom2_d5 | 1 | 0,37 | 0,41 | 0,45 / 0,05 | −0,06 | 0,66 | 0,71 | 0,51 | 0,49 | 0,30 |
| +rt_curve_2s10s_d5 | 1 | 0,51 | 0,55 | 0,65 / 0,08 | 0,07 | 0,85 | 0,88 | 0,68 | 0,49 | −0,69 |
| +seg_last1h | 5 | 0,52 | 0,49 | 0,66 / −0,24 | 0,38 | 0,63 | 0,57 | 0,48 | 0,49 | 0,21 |
| +xa_gdx_rel1 | 3 | 0,54 | 0,55 | 0,76 / −0,13 | 0,59 | 0,53 | 0,53 | 0,33 | 0,49 | −0,20 |
| −xa_aud_d5 | 3 | 0,62 | 0,63 | 0,83 / 0,02 | 1,02 | 0,32 | 0,35 | 0,21 | 0,49 | −0,63 |

Bütün sinyallerde kısa bacak sıfıra yakın ya da negatif; kazancın büyük kısmı uzun bacaktan geliyor. Faiz sinyalleri (2y, 2s10s) yalnız 2022+ Fed döngüsünde çalışıyor; 2017–21'de etkileri sıfır.

### 4.2 Walk-forward ML (`02_walkforward.py`, `03_evaluate.py`, `eval_all.csv`, `compact_tables.md`, `tablolar.md`)

Özet sayılar:

| varyant | dönem | R²_hm>0 | en yüksek R²_hm | CW t>1,645 | en yüksek CW t | zamanlama Sharpe>0 | demeaned Sharpe>0,3 |
|---|---|---|---|---|---|---|---|
| V1 (VİOP, set B) | VAL 2020–21 | 4/27 | +%1,25 (C2-sel h5) | 0 | 1,08 | 16/27 | 6/27 |
| V1 | **OOS 2022+** | **0/27** | −%0,02 (C1 h1) | **0** | 1,17 | 7/27 | 3/27 |
| V2 (spot 2011+, set A) | VAL 2020–21 | 8/27 | +%0,04 | 0 | 0,48 | 4/27 | 1/27 |
| V2 | **OOS 2022+** | 13/27 | +%0,46 (HGB h1) | 2 (HGB h1 1,69; ens h1 1,67) | 1,69 | 22/27 | 15/27 |
| V3 (erken) | 2013–16 | 1/27 | +%0,01 (ridge h5) | 0 | 1,11 | — | — |

Buy & hold Sharpe: VAL 0,47, OOS 0,53 (2020+ 0,50).

Seçilmiş satırlar (R² yüzde; zamanlama Sharpe net 5 bps):

| V | model | h | R²_hm VAL | R²_hm OOS | R²_0 OOS | CW t OOS | IC t VAL | IC t OOS | Sharpe VAL | Sharpe OOS | dm OOS | uzun / kısa OOS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| V1 | ridge | 1 | −0,14 | −0,09 | −0,03 | −1,00 | 0,35 | −0,41 | 0,40 | −0,17 | −0,17 | 0,25 / −0,49 |
| V1 | ridge | 3 | 0,08 | −1,20 | −1,02 | 0,67 | 0,93 | 0,15 | 0,11 | −0,18 | −0,16 | 0,31 / −0,47 |
| V1 | hgb | 5 | −4,07 | −10,26 | −9,95 | −0,79 | 0,15 | −1,22 | 0,21 | −0,49 | −0,46 | 0,10 / −0,67 |
| V1 | rf | 3 | −1,32 | −2,15 | −1,97 | −1,05 | −0,72 | −1,35 | −0,68 | −0,62 | −0,59 | −0,02 / −0,75 |
| V1 | ens_ml | 1 | −0,32 | −0,08 | −0,02 | 0,26 | −0,54 | −0,32 | 0,15 | −0,55 | −0,56 | −0,02 / −0,76 |
| V1 | c1_apriori | 1 | −0,03 | −0,02 | 0,04 | −0,60 | −0,18 | 1,82 | 0,36 | 0,90 | 0,82 | 0,87 / 0,32 |
| V2 | hgb | 1 | −3,24 | 0,46 | 0,51 | 1,69 | −2,27 | 1,71 | −1,14 | 0,30 | 0,30 | 0,64 / −0,14 |
| V2 | rf | 3 | −1,16 | 0,14 | 0,32 | 0,84 | −0,92 | 2,11 | −1,32 | 0,80 | 0,84 | 1,04 / 0,13 |
| V2 | ridge | 5 | −0,04 | 0,10 | 0,39 | 0,94 | −0,80 | 2,10 | −0,38 | 0,34 | 0,45 | 0,69 / −0,18 |
| V2 | ens_ml | 1 | −0,72 | 0,40 | 0,46 | 1,67 | −2,60 | 1,78 | −1,61 | 0,63 | 0,65 | 0,90 / 0,06 |

Yorum:

- **V1: model karmaşıklaştıkça OOS kötüleşiyor.** HGB/RF OOS R²'si −%0,3..−%10,3, doğrusal modellerinki −%0,09..−%5,6. Ridge ve lasso cezayı neredeyse tamamen artırıp tarihsel ortalamaya yaklaştığında R² sıfıra yaklaşıyor; daha iyisi yok.
- **V2'nin OOS pozitifliği doğrulama döneminde tam tersine dönüyor.** VAL'de HGB h=1 CW t −1,84, RF h=1 −1,88, topluluk h=1 −1,90; zamanlama Sharpe'ları −1,1..−1,6. OOS'ta aynı modeller +1,3..+1,7.
- V2 RF h=3'ün yıllık IC'si: 2020 −0,19, 2021 0,09, 2022 −0,02, 2023 0,24, 2024 0,03, 2025 0,09, 2026 0,08. Kazanç 2023'e yığılıyor (yıllık Sharpe 2,1).
- **Rastgele yürüyüş kıyası (R²_0):** V2 OOS'ta 17/27 pozitif. Bunun nedeni tahminlerin pozitif ortalamayı (drift) içermesi. R²_0 ile R²_hm arasındaki farkın tamamı tarihsel ortalamanın kendisinden geliyor. Tarihsel ortalamaya karşı (R²_hm) kazanç ya yok ya da anlamsız.
- **"Ham" pozisyonlar** (sign ŷ) çoğunlukla uzun. Doğrusal modellerde ve C1'de ham OOS Sharpe 0,0–0,9 aralığında; demeaned karşılıkları 0,3–0,5 puan daha düşük, çoğunlukla 0'a yakın. Örnek: V1 C1 ham OOS 0,52, demeaned 0,01 (`eval_all.csv`, sütun `raw_*`). Bu, drift tuzağının doğrudan kanıtı.

**Doğrulamada seçim → OOS tek değerlendirme** (`selection_val_to_oos.csv`; ölçüt VAL CW t, V1+V2 içinden):

| h | seçilen | VAL CW t | VAL R²_hm | OOS R²_hm | OOS R²_0 | OOS CW t | OOS IC t | OOS Sharpe (dm) | B&H OOS |
|---|---|---|---|---|---|---|---|---|---|
| 1 | V1 lasso | 0,59 | −%0,23 | −%0,22 | −%0,16 | −1,19 | −1,47 | −0,91 (−0,93) | 0,53 |
| 3 | V1 ridge | 0,91 | +%0,08 | −%1,20 | −%1,02 | 0,67 | 0,15 | −0,18 (−0,16) | 0,53 |
| 5 | V1 C2-sel | 1,08 | +%1,25 | −%0,52 | −%0,24 | −1,49 | −1,41 | −0,46 (−0,53) | 0,53 |

**Erken dönem (V3, 2013–2016):**
- 26/27 kombinasyonda R²_hm < 0 (−%9,1..+%0,01).
- CW t en fazla 1,11 (HGB h5; R² −%6,1).
- Bu dönemde altın düşüyordu (B&H −0,57) ve zamanlama Sharpe'ları çoğunlukla negatif.
- İstisna C1: Sharpe 0,66 / 0,34 / 0,27. Trend izleme düşüş yıllarında kısa pozisyonda kalıyor.

### 4.3 Önceden belirlenmiş birleşik C1: neden "çalışıyor gibi" görünüyor? (`06_c1_decomp.py`, `c1_decomp.csv`)

| ölçüt (h=1) | C1 sabit (genişleyen z) | yalnız hızlı 4 bileşen | yalnız yavaş (r20+r250) |
|---|---|---|---|
| IC t (VİOP 2017+), IS / OOS | 1,06; −0,65 / 1,85 | −0,62 | 1,61 |
| yıllar aynı işaret | 2/9 | 5/9 | 2/9 |
| Sharpe 2020+ (demeaned) | 0,76 (0,66) | −0,12 (−0,09) | 0,45 (0,30) |
| Sharpe 2020+ yıl-içi demeaned | **0,25** | −0,25 | −0,20 |
| Sharpe 2017-03..2019-12 (B&H 0,49) | **−0,76** | −1,24 | 0,29 |
| spot 2011–2019 Sharpe / yıl-içi dm (B&H 0,05) | 0,24 / 0,05 (IC t 0,14) | — | — |

Walk-forward C1 (V1) zamanlama Sharpe'ları:

| h | 2020+ | OOS (dm) | 10 bps OOS | uzun / kısa OOS |
|---|---|---|---|---|
| 1 | 0,74 | 0,90 (0,82) | 0,80 | 0,87 / 0,32 |
| 3 | 0,73 | 0,88 | — | — |
| 5 | 0,61 | 0,76 | — | — |

Sonuç: C1'in 2020–26 performansı büyük ölçüde **yıl düzeyinde trend yakalamaktan** geliyor.
- Yıl içinde öngörü gücü küçük: yıl-içi demeaned Sharpe 0,25.
- Yıllık IC karışık: 2020 −0,13, 2025 −0,13; ama 2025 Sharpe 2,2.
- Hızlı makro bileşenler (dolar, reel faiz, Şanghay primi değişimi) tek başlarına sıfır ya da negatif.
- Kural 2017–19'da belirgin zarar etti.

Bu, uzun vadeli trend izlemenin bilinen bir özelliği; 1–5 günlük lead-lag değil. Tek tek bileşenlerin hiçbiri |t|≥1,7'yi geçmiyor (`c1_decomp.csv`). COT kontrarian bileşeni 2020+'da 0,27–0,34 Sharpe verdi, ama IC t<0,9. Aynı bileşen 2017–19 VİOP'ta Sharpe −0,14..−0,20, 2011–16 spotta +0,11..+0,24 verdi.

### 4.4 Permütasyon önemi (`04_permimp.py`, `permimp_*.csv`)

Statik modeller 2017-03..2021-12'de eğitildi (h günlük ambargo) ve 2022+ üzerinde değerlendirildi. Temel OOS R²_hm değerlerinin hepsi negatif:

| model | OOS R²_hm |
|---|---|
| ridge | −%0,05..−%0,12 |
| EN | −%0,09..−%0,84 |
| HGB | −%0,8..−%11,9 |
| RF | −%0,04..−%2,5 |

Grup permütasyonu 10 tekrarla yapıldı. MSE değişimi ×1e-6 cinsinden; karşılaştırma için h=1 MSE ≈ 100×1e-6, h=5 MSE ≈ 500×1e-6.

- **Fiyat grubu:** HGB'de −0,4 / −7,5 / −27,2, RF'de −0,2 / −0,6 / −1,8. Karıştırınca OOS iyileşiyor; fiyat öznitelikleri aşırı öğrenme kaynağı.
- **COT:** HGB h5 −14,1, RF h5 −5,6. Bu grup da zarar veriyor.
- **En büyük pozitif katkılar** hep R²'si −%12 olan HGB h5 modelinde: Şanghay +2,9, VİOP t-1 +2,8, oynaklık +2,7. Ridge h5'te seans +1,0.
- **Öznitelik düzeyinde ridge'in ilk sıraları:** seg_last1h, rt_curve_2s10s_d5, xa_aud_d5, vp_basis_l1. Bunlar tek değişkenli taramanın da üst sıraları; büyüklükleri MSE'nin ≤%0,2'si.

Önem sıralaması ilginç ama ekonomik olarak sıfır: hiçbir grup modeli tarihsel ortalamanın üstüne çıkarmıyor.

### 4.5 Sağlamlık (`05_robust.py`, `robust.csv`)

- **Sıfır hacimli aktif kontrat günü yok** (0 gün). Roll günü sayısı 61.
- **Roll içeren girişler sıfırlandı** (t+1..t+h içinde v_code değişimi). Sonuçların yönü değişmedi: V1 ridge h3 2020+ R² −%0,84 → −%1,35; C1 h3 OOS Sharpe 0,88 → 0,98; V2 RF h3 OOS 0,80 → 0,67.
- **Uç dönemler dışarıda** (Mart 2020, Ocak–Şubat 2026):
  - V1 ridge h3 R² −%0,84 → −%1,68;
  - V2 RF h1 Sharpe 2020+ −0,07 → −0,35, OOS 0,36 → 0,05;
  - C1 h1 OOS 0,90 → 0,78.
  V2'nin h=1 OOS kazancının çoğu uç günlerden geliyor.
- **COT gecikmeli yayın** (01.10–31.12.2025) dışarıda bırakılınca anlamlı değişiklik yok: C1 h1 OOS 0,90 → 0,82; V2 RF h3 0,80 → 0,91.
- **Örtüşmesiz alt örneklem** (her h günde bir giriş, h ofsetleri ortalaması): V1 ridge h3 R²_hm −%0,85, V2 RF h3 −%0,22, V2 ridge h3 +%0,24. Anlamlılık yok.
- **10 bps maliyet:** OOS zamanlama Sharpe'ları 0,07–0,30 düşüyor. Örnekler: C1 h1 0,90 → 0,80; V2 RF h3 0,80 → 0,73; V2 topluluk h1 0,63 → 0,38; V2 HGB h1 0,30 → 0,05. HGB/RF h=1 yılda ≈165–195 birim devirle maliyete en duyarlı modeller.
- **Ceza seçimi:** ridge cezası çoğu ayda ızgaranın üst ucunda (1e4–3e5). Lasso ve EN h=1'de aylık eğitimlerin %64'ünde (V1) ve %90'ında (V2) sıfır öznitelik seçti (`diag_*.csv`). İç doğrulama "sinyal yok" diyor.

### 4.6 İleriye bakma kontrolü (`07_placebo.py`, `placebo_preds.csv`, `univariate_early_placebo.csv`)

- Model tahminleri kaydırılarak IC'ye bakıldı (shift −1/−2 = geleceğin tahmini).
  - Gerçek (shift 0) IC'ler küçük (|IC| ≤0,08).
  - Shift +1/+2 (daha eski bilgi) IC'leri shift 0'a benzer büyüklükte. Bu, özniteliklerin hedefi önceden içermediğini gösterir.
  - Shift −1 IC'leri yüksek (V1 ridge h1 0,47): yarının 15:00 fiyatı yarının getirisiyle örtüşüyor, bu beklenen durum.
- Tek değişkenli adaylarda da aynı desen var. Örnek rt_nom2_d5: shift −2 → −0,149, 0 → −0,049, +1 → −0,049.
- Gün t'de 15:10'da bilinen `v_*` değerleri kullanılmadı.
- Etiket örtüşmesine karşı h günlük ambargo uygulandı ve standardizasyon yalnız eğitim penceresinde yapıldı. Kayan z-skorları (COT 52 hafta, Şanghay 20 gün) yalnız geçmiş pencereyi kullanıyor.

## 5. Negatif bulgular (test edildi, tutmadı)

- **Modeller:**
  - Ridge, lasso, elastic net, HGB, RF ve topluluk V1 ve V3'te hiçbir ufukta tarihsel ortalamayı ya da sıfırı yenemiyor. V1 OOS'ta 0/27 pozitif R². V2'de yalnız 2022+'da pozitiflik var; VAL'de tersine dönüyor ve anlamsız.
  - Doğrulamada seçilen modellerin OOS'u negatif (h=1/3/5).
  - C2 (IC işaretli eşit ağırlık; bütün öznitelikler ya da seçilmişler): OOS R² negatif. C2-sel h3 VAL'de iyi görünüyor, OOS'ta IC t −2,05.
- **Makro ve akış sinyalleri:**
  - C1'in hızlı makro bileşenleri (−ΔDXY5, −Δreal10_5, +ΔŞanghay primi5) tek başlarına 2020+'da Sharpe ≈ −0,64..+0,07. Dolar 5 günlük değişimi IS'te ters işaretli (t_is −2,1..−3,1), OOS'ta a priori yönde; kararsız.
  - Şanghay primi değişimi: 2020+ Sharpe −0,10..−0,64, IC t ≈ −0,2..−1,5. A priori işaretin tersi; tutarsız.
  - COT kontrarian z-skoru: IC t<0,9; yılların 4/10'unda aynı işaret.
- **Seans:** Asya, Londra, NY sabahı ve 20 günlük Asya/ABD toplamlarında "Asya alır, NY satar" kalıcılığı yok. seg_london h3 t 2,07 (IS 0,46; 2011–16 t 0,70) zayıf. Tek istisna seg_last1h (DÜŞÜK güven, §6).
- **Erken dönemde tutmayan tek değişkenliler:**
  - AUD 5 günlük değişimi (ters): VİOP'ta t −2,68; 2011–16'da işaret tersine döndü (t +1,72).
  - 2s10s eğim değişimi: VİOP'taki tek |t|≥3; 2011–16'da ters işaret (t −1,31).
  - GDX−GLD göreli: 2011–16'da sıfır (t −0,08).
- **Takvim:** ay mevsimselliği (cal_mcos) IS'te t ≈0, yalnız OOS'ta var. Ay dönümü (cal_tom; t 0,36 / −0,57 / −0,66) ve haftanın günü etkileri |t|<2.
- **Çapraz varlık:** şu sinyallerin hepsi |t|<2:
  - oynaklık (VIX, GVZ, varyans primi; en yüksek vol_gvz_dev60 h1 t 1,62, IS −0,45);
  - petrol, bakır, BTC, gümüş, S&P ve TLT'nin t-1 değişimleri;
  - dk 15:00 24 saatlik değişimler (en yüksek dk_try_d1 t −1,57).
- **VİOP t-1:** hacim/AP değişimi ve yurt içi gram altın primi |t|<2. Sınırda, mekanizmasız iki sinyal: vp_basis_l1 h3 t 2,00 (IS 1,41, OOS 1,59) ve tr_usdtry_ret_l1 h3 t −2,08 (IS −1,56, OOS −1,45).
- **Veri sorunu:** paneldeki `gpr_*` (Caldara–Iacoviello) sütunları bütün satırlarda sabit (tek değer). Jeopolitik risk öznitelikleri test edilemedi ve standardizasyonda düştü. Panel kurucuda düzeltilmeli.

## 6. İddialar ve güven etiketleri

Kod yolu kökü: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a8_ml_kombinasyon/`

| # | iddia | kural | h | t tam / IS / OOS | yıllar | OOS Sharpe (dm) | erken / uzun spot | etiket |
|---|---|---|---|---|---|---|---|---|
| 1 | ML ve çok değişkenli birleştirme RW'yi yenmiyor | 9 model × 3 h × 3 varyant | 1/3/5 | V1 OOS R²_hm ≤ −%0,02 (0/27 pozitif), CW ≤ 1,17 | — | seçilen modeller −0,91 / −0,18 / −0,46 | V3 1/27 pozitif (+%0,01) | **YOK** |
| 2 | 2 yıllık getiri 5 günde düştüyse ertesi gün altın artar | pos = −sign(nom2_{t-1} − nom2_{t-6}) | 1 | −2,36 / −0,26 / −2,48 | 6/10 (spot 12/16) | 0,66 (0,71) | 2011–16 t −1,61; 2011–26 t −2,61 | DÜŞÜK (ORTA ölçütlerini mekanik olarak karşılıyor; ama IS sıfır, 309 testten seçildi, q=0,77) |
| 3 | 14–15 UTC son saat getirisi 5 gün sürer | pos = sign(ln p15/p14) | 5 | 2,54 / 1,32 / 2,05 | 7/10 (spot 13/16) | 0,63 (0,57) | 2011–16 t 1,16; 2011–26 t 2,51 | DÜŞÜK (h=1 OOS t 0,74; kısa bacak −0,24) |
| 4 | 2s10s eğimi 5 günde dikleştiyse ertesi gün altın artar | pos = sign(Δ5(nom10 − nom2)) | 1 | 3,03 / 1,50 / 2,53 | 6/10 | 0,85 (0,88) | 2011–16 **t −1,31 (ters)**; 2011–26 t 1,30 | DÜŞÜK |
| 5 | C1 a priori birleşik zamanlama | sign(z-ort.: +r20, +r250, −ΔDXY5, −Δreal10_5, +ΔŞP5, −COTz) | 1 | IC 1,06 / −0,65 / 1,85 (sabit) | 2/9 | 0,90 (0,82) | 2017–19 Sharpe −0,76; yıl-içi dm 0,25 | DÜŞÜK (kazanç yavaş trendden) |
| 6 | V2 RF (spot 2011+ eğitim), h=3 | sign(ŷ − ȳ_w) | 3 | IC 1,54 / −0,92 / 2,11 | 5/7 | 0,80 (0,84) | V3 (2013–16) RF h3 IC t −0,81, Sharpe −0,22; OOS R² yalnız +%0,14 (CW 0,84) | DÜŞÜK |

## 7. Test sayısı ve çoklu test

`register()` ile **522 test** kaydedildi:

| aile | test sayısı |
|---|---|
| a8_univariate | 309 |
| a8_univariate_early | 12 |
| a8_univariate_longspot | 18 |
| a8_ml_V1 | 27 |
| a8_ml_V2 | 27 |
| a8_ml_V3 | 27 |
| a8_c1_components | 30 |
| a8_robust (ens_ml, C1, ridge, RF için uç / roll / COT dışlamaları; bağımlı yeniden testler) | 72 |

518 testte t tanımlı. |t|≥2: 18 (bağımsızlık altında beklenen ≈23,6). |t|≥3: 1. Bu ajanın kendi kaydında BH-FDR en küçük q = 0,77. Hiçbir bulgu %10 FDR'de sağ çıkmıyor.

## 8. Uygulama notu

- Bu veride 1–5 günlük VİOP ons altın işlemi için ML ya da çok değişkenli birleştirme, buy & hold'dan (Sharpe ≈0,5) daha iyi bir risk ayarlı getiri sağlamıyor.
- Uzun bacağı ağır basan her kural 2020–26'da iyi görünüyor. Drift çıkarılınca ya da 2017–19 ve 2013–16 dönemlerine bakılınca bu görünüm kayboluyor.
- Faiz değişimleri (2y, 2s10s) ve son saat momentumu izlemeye değer, ama tek başına işlem kuralı için yetersiz. Önce diğer ajanların yeniden üretimi ve global FDR beklenmeli.

## 9. Dosyalar

- **Betikler:** `features.py`, `common.py`, `models.py`, `01_univariate.py` … `10_tables.py`, `02b_ybar_w.py`, `run_all.sh`, `_report_numbers.py` (rapordaki sayıları yazdırır).
- **Bilgi zamanı:** `oznitelik_bilgi_zamani.csv`, `bilgi_zamani_kontrol.csv`.
- **Tahminler:** `preds_V1/V2/V3.parquet` (date, h, model, yhat, ybar, ybar_w), `diag_*.csv`.
- **Değerlendirme:** `eval_all.csv`, `eval_yearly.csv`, `selection_val_to_oos.csv`, `compact_tables.md`, `tablolar.md`.
- **Diğer:** `univariate_viop.csv`, `univariate_early_placebo.csv`, `univ_bt.csv`, `longspot.csv`, `c1_decomp.csv`, `permimp_*.csv`, `robust.csv`, `placebo_preds.csv`.
- **Düzeltme notları:**
  1. İlk değerlendirmede zamanlama sinyali sign(ŷ − ham ortalama) olarak alınmıştı. Bu, sıfır öznitelikli modellerde winsorize ile ham ortalama arasındaki farktan sahte bir sürekli uzun ya da kısa pozisyon üretiyordu. Sinyal sign(ŷ − winsorize ortalama) olarak düzeltildi.
  2. Ay dönümü özniteliği ilk sürümde hatalıydı (her gün 1); düzeltildi ve bütün hat yeniden çalıştırıldı.

  Raporlanan bütün sayılar düzeltilmiş son çalıştırmaya aittir.
