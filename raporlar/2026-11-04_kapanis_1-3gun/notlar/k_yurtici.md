# k_yurtici — Yurt içi, takvim, olay ve çift sinyalleri: kapanıştan kapanışa 1–3 gün (VİOP uzlaşmasından)

**Tarih:** 03.11.2026 · **Veri sonu:** 30.10.2026 · **Kod:** `out/code_k_yurtici/` (klib.py, k1–k9) · **Tüm testler:** `out/code_k_yurtici/res/tests_all.csv`
**Test sayısı:** 2.494 (BH-FDR q=0,05 tüm aile: eşik |t| ≥ 2,73; 316 test geçti, çoğu aynı ailenin birbirine çok yakın varyantları)
SAHOL/AKBNK tekrar edilmedi. Yatırım tavsiyesi değildir.

## Kurallar (kullanıcı profili)
- Giriş **E0** = VİOP uzlaşması_t; çıkış uzlaşma_{t+h}; h = 1, 2, 3 iş günü (kıyas 5).
- **E1** = vadeli son işlem fiyatı_t (XU030'da 18:15; pay vadelisinde 23.09.2022'den beri 18:10).
- **E2** = sinyal t, giriş uzlaşma_{t+1}. Bu bir plasebo/sağlamlık testi: ileriye bakma ve kapanış anı mikro yapısı ayıklanıyor.
- Sözleşme: ön vade. Vade, çıkıştan önce doluyorsa 2. vade kullanıldı. Tutma süresince roll yok.
- Getiri: aynı sözleşmenin günlük uzlaşma zinciri.
  - Bedelsiz düzeltme günleri NaN.
  - Vadeli temettüde düşmüyor. Ex-günü vadeli − düzeltilmiş spot medyanı −25 bps, vadeli − fiyat spot medyanı +235 bps.
- Maliyet: pay vadelisi bacak başına gidiş-dönüş 8 / 15 bps, XU030 vadelisi 3 bps.
  - Çiftlerde getiri sermaye başınadır: (A − β·B)/(1+β). Net = brüt − c.
- t istatistiği: işlem ağırlıklı ortalama; tarih kümelemeli ve NW(h) (aynı gün ve örtüşen işlemler bağımlı).
- IS/OOS: VİOP 2017–2021 / 2022–2026; spot 2014–2020 / 2021–2026.
  - Limit bloğu yalnız ±%10 rejimi (2020-03+).
  - Müzayede bloğu 2023-11+ (h1): IS 2023-11..2024-12 / OOS 2025–26.

## Ana sonuç (tek cümle)
Kapanıştan kapanışa VİOP kullanıcısı için işe yarayan bilgi büyük ölçüde **kapanış anındaki fiyat bozulmasından** geliyor: vadeli uzlaşması, spot kapanış müzayedesini yarı yarıya izliyor ve fark ertesi gün kapanıyor. Bunun dışında yalnız iki göreli sinyal VİOP'ta 1 gün gecikmeli girişle de ayakta kalıyor:
- Koza grubu momentumu
- TCELL–TTKOM dönüşü (zayıf)

## Özet tablo

| # | Sinyal | VİOP sonucu (brüt bps / işlem) | 1 gün geç (E2) | FDR | Uygunluk | Güven |
|---|---|---|---|---|---|---|
| 1 | **XU030 kapanış bazı sıçraması** (Δ[ln(F_18:15/S_kapanış)] > 1σ ters yön, h1) | +25,0 (t 2,93), 65/yıl, net(3) +22. IS +22 (t 2,1) / OOS +28 (t 2,1), 9/10 yıl. Yalnız AL +28,6 (t 2,9) | −1,8 (t −0,2) | geçti (sınırda) | UYGUN (18:10–18:15 hızlı işlem) | ORTA |
| 2 | **TRMET grup-içi momentum** (3g artık TRMET − β·ort(TRALT,TRENJ) > 1,5σ yönünde; TRMET1! / β·TRALT1!) | h1 +26 (t 4,2), h2 +44 (t 4,0), h3 +55 (t 3,6); IS t 3,3 / OOS t 2,9; 7/8 yıl | h2 +29 (t 2,5), 8/8 yıl | geçti | KOŞULLU | ORTA |
| 3 | **Pay vadelisi kapanış baz sapması** (vadeli kapanış spot müzayedesine göre zengin/ucuz -> ters) | Kesitsel L/S üst/alt %20, E1 h1 +23–25 (t 17–18); 10/10 yıl. Hacimce ilk 15 + 2022-09 sonrası +16,5 (t 5,4), net15 +1,5. Tek bacak A sınıfı 2022-09+ \|z\|>1,5 +39,6 (t 2,6) | ≈0 (t 0,5–1,9) | geçti | KOŞULLU (giriş anı kritik; maliyetle başa baş) | İstatistik YÜKSEK / işlem DÜŞÜK-ORTA |
| 4 | **TCELL–TTKOM göreli dönüş** (Z20 > 2, 2–3 gün) | h2 +32 (t 2,8), h3 +41 (t 2,85); IS +54 / OOS +30 (t 1,5); spot 2014+ h3 +51 (t 4,7), 17/18 yıl | h2 +27 (t 2,3) | geçti (sınırda) | KOŞULLU | DÜŞÜK-ORTA |
| 5 | **KCHOL NAV sapması** (zdev > 0,5; KCHOL1! − β·XU030D1!) | h3 +14,8 (t 3,3); IS +1,9 (t 0,3) / OOS +29,9 (t 4,2); spot 2014+ +17,3 (t 5,3), 15/17 yıl | — | geçti | KOŞULLU (net küçük) | DÜŞÜK-ORTA |
| 6 | **Temettü öncesi yükseliş** (verim ≥ %4, E−4 kapanış -> E−1 kapanış) | VİOP +15 (t 0,3): YOK. Spot VİOP47 +74 (t 2,9), tüm evren +101 (t 4,9), 15/17 yıl | — | spot geçti | VİOP'ta UYGUN DEĞİL; spot KOŞULLU | Spot ORTA |
| 7 | Ay dönümü (ayın son günü uzlaşmasında al, ilk gün sat; XU030D1!) | +44 (t 2,4), 6/10 yıl (2021–22 ağırlıklı) | — | geçmedi | KOŞULLU | DÜŞÜK |
| 8 | Tavan/taban sonrası | Dolan yön (tavanda sat / tabanda al) kaybettiriyor: −99 / −252 bps (h1). Devam yönü yalnız olay günlerinin ~%15'inde dolabiliyor: +52 / +17 (t ≤1) | ≈0 | kayıplar geçti | UYGUN DEĞİL (risk kuralı) | YÜKSEK (olgu) |
| 9 | Kapanış müzayedesi dönüşü (hisse) | VİOP'ta dönüş yok; tersine hafif devam (yalnız piyasa bileşeni). Hisseye özgü CA_id ≈ 0. Spotta dönüş var (açığa satış gerekir) | ≈0 | — | UYGUN DEĞİL | ORTA |
| 10 | Çift dönüşü (12 çift + ASELS–KRDMD) | Havuzda yok, h1'de hafif ters (−3…−9). THYAO–PGSUS ve TRALT–TRMET göreli MOMENTUM gösteriyor | — | kısmen | UYGUN DEĞİL (4 hariç) | — |
| 11 | Bayram/tatil öncesi, BIST30 dönem değişikliği | Anlamlı ve tutarlı değil. BIST30/50 değişikliği n=18 (fade yönü −117…−325, 3 çeyrek) | — | n küçük | UYGUN DEĞİL | ÇOK DÜŞÜK |

## Ayrıntılar

### (a) Temettü (k1, 105 test)

**Vadeli temettüyü bazda fiyatlıyor; ex-günü vadeli düşmüyor.**

**Spot (XU100'e göre fazla getiri), E−4 -> E−1:**
- Tüm evren: +62 bps (t 4,8), 16/17 yıl.
- VİOP47: +37 (t 2,8).
- 2017+ VİOP47: +26 (t 1,4).
- Yüksek verim (≥ %4): VİOP47 +74 (t 2,9; OOS +124), tüm evren +101 (t 4,9).

**VİOP uzlaşması aynı pencerede:**
- +5 (t 0,15).
- Hedge'li −7.
- Yüksek verimde +15 (t 0,3; IS −103 / OOS +114).

**Ex sonrası geri veriş:**
- VİOP'ta yok (−14…+10).
- Spotta ex-günü toplam getiri XU100'ün +40 bps üstünde (açılış primi). Ardından anlamlı geri veriş yok.

**Yorum:** Koşu, spotta temettü hakkına özgü bir talep primi; vadeli bu priminden pay almıyor. Arbitraj için spot açığa satış gerekir. VİOP kullanıcısı için işlenemez; spot hesapla (uzun + XU030 vadeli hedge) işlenebilir.

### (b) Tavan/taban (k2, 80 test; ±%10 rejimi, VİOP47 vadeli var: TC 594, BC 383 olay)

**Vadeli kilit oranları:**
- t günü vadeli uzlaşması limitte: tavanda %84, tabanda %86.
- t+1'de kilit: %12 / %20.

**Dolan yönler kaybettiriyor:**
- Tavanda vadeli sat -> h1 −99 bps (t −3,7), 2/7 yıl.
- Tabanda vadeli al -> h1 −252 (t −3,2), 0/7 yıl.

**Devam yönü:**
- Yalnız vadeli kilitsizken dolabiliyor. Tavan: n=92, +52 (t 1,0). Taban: n=53, +17; hedge'li +159 (t 2,5), IS n=9.
- t+1 uzlaşmasından giriş (E2): tavan devam ≈0; taban devam +45…+92 (t 0,4–1,1), hedge'li ≈0.

**Spot taban sürüklenmesi:** Tüm evrende +137…+270 bps (h2–h5) ama küçük hisseler ve 2026 fon krizi kaynaklı; VİOP47'de IS negatif.

**Pratik kural:** Limitte kapanan hissede kapanışta ters pozisyon açma.

### (c) Kapanış müzayedesi (k3, 142 test; 2023-11+, yaz günleri, 425 gün)

**Vadeli müzayedeyi kısmen izliyor:** Vadeli uzlaşma getirisi müzayede hareketinin ~%50'sini içeriyor.

**Vadeli devam (|CA| > 25 bps, E0 h1):**
- +14 (t 2,25).
- Likit üst 1/3: +30,6 (t 3,1); E1 ile +23,4 (t 2,4).
- E2: ≈0.
- Hisseye özgü CA_id (XU030 müzayedesi çıkarılmış): ≈0.

**Endeks düzeyi:** Etki piyasa geneli. XU030 spot müzayedesi -> XU030 vadelisi, |CA_x| > 10 bps: h1 +35,5 (t 2,5), E1 +33 (t 2,3), n=169.

**Spot dönüşü (açığa satış):** CA_id > 25 bps için h1 +24 (t 4,6). Önceki bulgu doğrulandı ama VİOP'ta çalışmıyor.

### (d) Takvim (k4, 125 test)

**Ay dönümü (ME kapanışı -> d1):**
- XU030D1! +44 (t 2,4); SSF sepeti +39 (t 2,3).
- Spot XU100 2005+: +18 (t 1,5); IS ≈0, OOS +65.
- Yıllar: 2021 +164, 2022 +161, diğerleri küçük. Rejime bağlı.

**ME−1 -> ME:** −25 (t −1,8).

**Tatil öncesi / bayram arifesi:** Tutarlı etki yok. "Diğer tatil öncesi −1" −38 (t −2,1). İşaret beklenenin tersi, OOS'a bağlı.

**XU030 vade ayları vs diğer aylar:** Fark anlamlı değil.

**BIST30/50 dönem değişikliği (VİOP47'de 19 olay, 6 çeyrek):**
- Tepki günü kapanışından sonra giren/çıkan yönünde tutmak kaybettiriyor (h3 hedge'li −117, t −3,8).
- Fade yönü pozitif ama n=18 ve 2026 fon krizi içeriyor: ÇOK DÜŞÜK.

### (e) Baz anomalisi (k5, k5b, k8; 382 test)

Pay vadelisi kesitsel L/S (üst %20 sat, alt %20 al):
- anom_close_dev, E1:
  - h1 +25,4 (t 18,2), h3 +29,0 (t 9,8); 10/10 yıl.
  - net8 +17, net15 +10.
- Likidite ve dönem filtreleri:
  - İşlem ≥ 1000: +21,6 (t 13,6).
  - Hacimce ilk 15: +20,2 (t 10,7).
  - 2022-09-23 sonrası: +22,5 (t 11,8).
  - 2022-09 sonrası + ilk 15: +16,5 (t 5,4), net15 +1,5; h3 +20,7, net15 +5,7.
- **E2 (bir gün sonra giriş):** +0,3…+7 (t ≤ 2,6), yani etki yalnız kapanış anında var.
- **Tek bacak, hisse bazında |z| > 1,5** (anom_close_dev / 120g std):
  - Tümü: +44 (t 4,7).
  - A sınıfı: +44 (t 4,2).
  - A sınıfı 2022-09+: +39,6 (t 2,6).
  - |z| > 2,5, A sınıfı 2022-09+: +23 (t 0,9).
  - E2 ≈ 0.
- **Uygulama zorluğu:** Pay vadelisi seansı 2022-09'dan beri spot müzayedesiyle aynı anda (18:10) bitiyor. Sinyal ancak müzayede gösterge fiyatıyla yaklaşık bilinebilir. Uzlaşma bir VWAP'tır, birebir dolum mümkün değildir.
- **En gerçekçi kullanım:** Zaten açılacak/kapatılacak pozisyonda yürütme filtresi. Vadeli spota göre pahalıysa satış tarafını öne al, alışı ertele.

XU030 vadelisi (k8, 54 test):
- **Sinyal:** Δb_c = günlük değişim, ln(F_son işlem 18:15 / S_kapanış). Aynı sözleşmede hesaplandı; vade geçişleri ayıklandı.
- **Ölçek:** σ ≈ 50 bps, yani |z| > 1 yaklaşık |Δb| > 50 bps.
- **Yön:** Vadeli spota göre dünkünden ucuz kapandıysa al, pahalı kapandıysa sat. Ertesi gün uzlaşmada kapat.
- **Sonuçlar:**
  - z120, |z| > 1: n=605, +25,0 (t 2,93), 9/10 yıl.
  - Taşıma düzeltmeli versiyon +25,8 (t 2,98).
  - Bütün pencere/eşik ızgarasında h1 t 2,4–3,0.
  - Sürekli eğim −0,37: farkın ~%37'si ertesi gün kapanıyor. Eğim zamanla azalıyor (2017–19 −0,74, 2020–22 −0,34, 2023–26 −0,29).
  - Arife günleri hariç tutulunca aynı sonuç.
  - Yalnız AL tarafı +28,6 (t 2,9); SAT tarafı +18,7 (t 1,2).
  - E2 (1 gün geç): −1,8.
  - XU030 müzayede hareketiyle korelasyon −0,27; (c) ile aynı mekanizma.
- h2–h3'te etki sönüyor (t 2,1–2,5, yalnız h1 güvenilir).

### (f) Çiftler (k6, 1.344 test)

**Seçim ve havuz:**
- ASELS ortağı IS döneminde kısmi korelasyonla seçildi: KRDMD (0,21). İlişki zayıf.
- Havuz (13 çift): hiçbir sinyalde dönüş yok.
  - VİOP E0 h1 −3…−9 bps (t −1,3…−3,4).
  - Spot ≈ 0…+9.

**VİOP'ta h1'de hafif ters işaret:** Bu, kapanış uzlaşmasının spotu geç izlemesinden kaynaklanıyor (bkz. c, e).

**Tek tek çiftler:**
- **TCELL–TTKOM:** Tek tutarlı dönüş çifti; ayrıntılar özet tabloda.
- **THYAO–PGSUS:** Göreli momentum. Z20 > 1,5, h2: −25 (t −3,3) dönüş yönünde; IS −42 / OOS −9 (t −1,2). Sönüyor: DÜŞÜK.
- **TRALT–TRMET:** Göreli momentum. REV3 > 2, h3: −88 (t −3,75), 0/8 yıl dönüş. E2 h2 −28 (t −2,5). (h) ile aynı olgu.
- **Banka çiftleri** (AKBNK–GARAN, YKBNK–ISCTR, VAKBN–HALKB):
  - E0 h1 dönüşü kaybettiriyor (−18…−21, t −3,5).
  - E2 ile 5 günlük ufukta pozitif: YKBNK–ISCTR REV3 > 2, h5 +78 (t 2,95, 10/10 yıl); AKBNK–GARAN Z60 > 1,5, h5 +41 (t 3,0).
  - 1–3 gün penceresinin dışında: DÜŞÜK.
- **Diğerleri** (EREGL–KRDMD, FROTO–TOASO, MGROS–SOKM, CIMSA–OYAKC, KCHOL–SAHOL, TUPRS–PETKM): VİOP'ta anlamlı ve maliyeti karşılayan dönüş yok. CIMSA–OYAKC'de n çok küçük.

### (g) KCHOL NAV (k7, 76 test)

- **Sinyal:** zdev = (D − MA60(D)) / std250. D = log KCHOL − log NAV sepeti.
- **Spot 2014+ (XU030 hedge'li):** h3 +17,3 (t 5,3), 15/17 yıl. h20'de +61 (t 3,3).
- **VİOP (KCHOL1! − β·XU030D1!):**
  - h3 +14,8 (t 3,3), ama IS 2017–21 ≈ 0 (t 0,3), OOS +30 (t 4,2).
  - Per birim brüt sermaye net ~+7 (8 bps) / ≈0 (15 bps). Gerçek maliyet ~4–5 bps (KCHOL 6,7 + XU030 3).
- **NAV sepeti vadelileriyle hedge'li:** Benzer sonuç (5 bacak, pratik değil).
- **Değerlendirme:** Öncekinden (DÜŞÜK) biraz daha güçlü. Pratik kazanç küçük.

### (h) Koza grubu (k7, 240 test)

**Kapanıştan kapanışa ilişki dönüş değil, MOMENTUM.** Önceki gün-içi bulgu (TRMET gün-içi dönüş, ORTA) gap ile birlikte düşünülünce tutarlı: grup-içi göreli hareket ertesi gün açılışta devam ediyor, gün içinde kısmen geri veriliyor, kapanıştan kapanışa net devam kalıyor.

**Sinyal tanımı:**
- u = r_TRMET − β·ort(r_TRALT, r_TRENJ); β 250g, son değer 0,88.
- z3 = Σ₃u / (σ60·√3). σ60 ≈ 166–194 bps, yani eşik |Σ₃u| ≈ 430 bps.

**Kural:** z3 > 1,5 -> TRMET1! al, 0,7·TRALT1! sat (hedge β son 0,69). z3 < −1,5 -> tersi.

**Sonuçlar:**

| Giriş | h1 | h2 | h3 | yıl |
|---|---|---|---|---|
| E0 | +26 | +44 | +55 | 7/8 |
| E2 | +18 | +29 | +34 | 8/8 |

- E0 net15: +11 / +29 / +40.
- E2 t: 2,6 / 2,5 / 2,3.
- XU030 hedge'li daha güçlü (h3 +63, t 3,2).
- Spot 2014+ zayıf (h3 +52, t 3,2, yalnız 17/22 yıl).
- TRALT'ın artığında da momentum var, yalnız TRMET'e hedge'li.

**Riskler:**
- Mekanizma belirsiz (çapraz iştirak NAV zinciri TRENJ -> TRMET -> TRALT; altın trendi).
- Grup kurumsal olaylara açık (TMSF, isim değişikliği, 2026Q4 BIST30 girişi, fon krizi).
- TRMET B sınıfı likidite (RT 8–12 bps; 1 mn TL emirde ~25 bps).

## Karşı argümanlar / sınırlamalar
- **Uzlaşma VWAP'tır.** E0 birebir dolum değildir. E1 (son işlem) ve E2 (ertesi gün) bu yüzden raporlandı. Kapanış anı sinyallerinin (1, 3) değeri E1'de korunuyor, E2'de sıfırlanıyor.
- **İllikit sözleşmelerde son işlem fiyatı bayat olabilir.** Likidite filtreleri (işlem ≥ 1000/3000, A sınıfı) kenarı küçültüyor ama sıfırlamıyor.
- **XU030 baz sıçraması FDR eşiğini ancak geçiyor** (q 0,03). En iyi parametre aramasından kaçınmak için z120 / |z| > 1 önerildi. Eğim yıllar içinde azalıyor (piyasa öğreniyor olabilir).
- **TRMET momentumu sonradan bulundu.** Hipotez dönüştü, iki yönlü test edildi, ama işaret veriden geldi. Kurumsal olaylara duyarlı; grup lehine/aleyhine haber günlerinde momentum doğal.
- **Temettü verimi gerçekleşen temettüden alındı.** İlan edilen temettüyle çok yakın ama birebir değil.
- **Çoklu test:** 2.494 test, FDR geçen 316'nın çoğu birbirine çok yakın varyantlar (baz ailesi, spot temettü, NAV, Koza). Bağımsız "aday" sayısı ~8–10.
- **Rejimler:** 2021–22 (KKM/yüksek enflasyon) ay dönümü ve bazı spot bulgularını şişiriyor. 2026 Eylül–Ekim fon krizi taban/çift sonuçlarını etkiliyor.

## TradingView
- `BIST:XU030D1!`
- `BIST:TRMET1!`, `BIST:TRALT1!`, `BIST:TRENJ` (sinyal için, vadelisi yok)
- `BIST:TCELL1!`, `BIST:TTKOM1!`
- `BIST:KCHOL1!`
- Spot temettü için `BIST:<KOD>`
- Pay vadelisi baz için `BIST:<KOD>1!` ve `BIST:<KOD>`

## Dosyalar

| Dosya | İçerik |
|---|---|
| `code_k_yurtici/klib.py` | Panel, ileri getiri (E0/E1), istatistik, BH |
| `k1_temettu.py` | (a) Temettü |
| `k2_limit.py` | (b) Tavan/taban |
| `k3_muzayede.py` | (c) Kapanış müzayedesi |
| `k4_takvim.py` | (d) Takvim |
| `k5_baz.py` | (e) Baz kesitsel L/S |
| `k5b_ts_liq.py` | (e) Baz, hisse bazında, likidite filtreli |
| `k6_cift.py` | (f) Çiftler |
| `k7_nav_koza.py` | (g) KCHOL NAV, (h) Koza grubu |
| `k8_xu030.py` | XU030 baz sıçraması sağlamlık |
| `k9_fdr.py` | Tüm testlerin birleştirilmesi ve BH-FDR |
| `res/tests_*.csv`, `res/tests_all.csv` (q_all, fdr_all) | Test sonuçları |
| `log_k*.txt` | Çalıştırma kayıtları |
