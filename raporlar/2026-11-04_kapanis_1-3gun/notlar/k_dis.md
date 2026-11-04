# k_dis — Dış sürücüler, kapanıştan kapanışa (1–3 gün) yeniden test

_03.11.2026 · veri 30.10.2026'ya kadar · kod: out/code_k_dis/ · sonuç tabloları: out/code_k_dis/res/ · yatırım tavsiyesi değildir_

## Kullanıcı kuralı (tüm testlerde)
- Karar BIST kapanışında (18:00–18:15 TSİ = 15:00–15:15 UTC). Giriş ve çıkış VİOP ön vade **uzlaşma** fiyatı (aynı kontrat ln(settle/prev_settle); vadeye <2 iş günü kala bir sonraki vadeye geçiş). Tutma h = 1, 2, 3 (kıyas 5) iş günü.
- Sinyal yalnız t kapanışında bilinen bilgiyle kuruldu: saatlik sürücüde 15:00 UTC'de **bilinen** son fiyat (bitmiş barın kapanışı ya da başlamış barın açılışı; ABD hisselerinde bu fiyat fiilen 14:30 UTC'ye ait); günlükte Asya (TSE/ASX/KRX) aynı gün t, Avrupa/ABD/emtia **t-1 tam gün** (shift 1); VİOP USDTRY/XAUUSD uzlaşması ve DİBS (BAP) aynı gün t.
- İşlem kuralı: sinyal / geçmiş 250 günlük std (saatlikte 120) = z; |z|>1 → yön(z), h gün tut; pozisyondayken yeni sinyal alınmaz (örtüşmeyen işlemler). Maliyet gidiş-dönüş 8 ve 15 bps (hedge'li işlemde +3 bps XU030 bacağı); ayrıca hisse bazlı y_viop_likidite rt_cost_small.
- Örneklemler: DF = VİOP vadeli 2017-03 → 2026-10 (IS 2017–2021 / OOS 2022–2026); DS = spot kapanış 2014 → 2026 (IS 2014–2020 / OOS 2021–2026); H = saatlik 15:00 UTC, 2023-12 (ES/Brent/altın 2024-06) → 2026-10 (yarılar: 2025-05 öncesi/sonrası).
- "raw" = hisse vadelisi tek bacak; "hedged" = hisse − β × F_XU030 (β geçmiş 250 gün).

## Test sayısı ve FDR
- (a) emsal ayrışması: 19.552 satır × 3 test (D, P|Ds, olay ortalaması) = 58.656 + 15.768 işlem-kuralı satırı. (b) çok günlük sürücü: 25.344 satır × 2 = 50.688. (c) kredi notu 189. (d) ABD makro 882. (e) akşam seansı 25. Sağlamlık 434. **Toplam ≈126.600 test.**
- (a)+(b) 109.344 birincil p-değeri üzerinde küresel BH-FDR (q=0,05): 393 geçen. Bunların ~250'si spot DS modunda D sinyalinin içindeki hissenin **kendi** kısa vadeli dönüşü (TCELL, ENKAI; hangi sepet konursa konsun geçiyor → sürücü değil, kapanış müzayedesi gürültüsü; vadelide yok). Sürücüye özgü olup küresel FDR'den geçenler: VİOP USDTRY 3–5g → THYAO/VESTL (q 0,004–0,03), ABD rafinerileri t-1 → TUPRS (q 0,008–0,03), altın (15:00) → TRMET h1 (q 0,016), Avrupa savunma (15:00) → ASELS h3 (q 0,043). Sınırda: FMG/BHP → EREGL (q 0,051), VİOP altın → TRALT (q 0,097; önceden kaydedilmiş hedef ailesinde q 0,028).
- Önceden kaydedilmiş hedef çift ailesi (sepet → kendi hissesi; mod başına 240–256 test): H 9, DF 9, DS 15 test FDR'den geçti; hepsi REF_US→TUPRS, MINERS_AU→EREGL/KRDMD, GOLD/GOLD_V→TRALT/TRMET, DEF_EU→ASELS, AIR_US→THYAO/TAVHL, AIRPORT→TAVHL.

## Ana sonuç
Önceki çalışmadaki "sektöre özgü yabancı emsal bilgisi gün içinde yavaş fiyatlanıyor" bulgusunun **kapanıştan kapanışa taşınan** bir kalıntısı var ama genel değil: hedef çiftlerin tamamı birlikte işlenince (|z|>1, 8 bps) net DF h3 hedged +11,7 bps (t 1,5), H h3 raw +26 (t 1,4); hedef dışı çiftler (plasebo) net −10…−12 (brüt ≈0). Yani bilginin çoğu t günü içinde fiyatlanıyor; t uzlaşmasından sonra yalnız 3–4 çiftte maliyeti aşan bir kalıntı kalıyor. **"Emsal − hisse ayrışması" (D) tek değişken olarak işe yaramıyor** (hissenin kendi artığının etkisi emsal etkisini götürüyor); çalışan şey emsal artığının kendisi (P), hissenin kendi hareketi kontrol edildiğinde de.

## Kullanılabilir adaylar (kapanıştan kapanışa)

| # | Kural | Hedef | 1/2/3 gün net (8 bps) | IS / OOS | Güven | Uygunluk |
|---|---|---|---|---|---|---|
| 1 | ABD rafineri sepeti (VLO, MPC, PSX, PBF) **dünkü** artığı (− β·S&P 500), |z|>1 | F_TUPRS | +13,6 (t 1,5) / +41,8 (t 2,9) / +55,3 (t 2,7); 15 bps: +6,6 / +34,8 / +48,3 | DF h2: +32,6 (t 1,75) / +50,7 (t 2,3); spot h2: +20,8 (t 1,4) / +57,0 (t 2,8) | ORTA | UYGUN |
| 2 | ASX demir cevheri (FMG, BHP) **bugünkü** artığı (− β·ASX200), |z|>1 | F_EREGL (hedge'li daha istikrarlı) | hedged +10,6 (t 1,4) / +28,1 (t 2,5) / +46,9 (t 3,2); raw h3 +51,7 (t 2,6) | DF h3 hedged: +73,6 (t 3,7) / +22,3 (t 1,0); spot h2 hedged: +31,7 (t 2,7) / +18,7 (t 1,25) | ORTA | UYGUN |
| 3 | VİOP altın (XAUUSD) uzlaşmasının **bugünkü** değişimi, |z|>1 | F_TRALT − β·F_XU030 (TRMET ikincil) | +25,9 (t 2,4) / +51,8 (t 3,2) / +54,4 (t 2,3); 15 bps: +18,9 / +44,8 / +47,4 | h2: +47,4 (t 2,0) / +54,2 (t 2,6) (VİOP TRALT 2018-12+) | ORTA | UYGUN |
| 4 | VİOP USDTRY uzlaşması 5 günlük kümülatif değişim, |z|>1 | F_THYAO (VESTL, ihracatçılar) | raw +26,6 (t 2,6) / +55,4 (t 3,1) / +96,3 (t 3,9); 15 bps h3 +89,3 | h3: +88,4 (t 2,5) / +105,3 (t 3,0) | ORTA | KOŞULLU |
| 5 | Avrupa savunma (RHM, BAE, LDO, SAAB) 15:00 UTC'ye kadarki artık | F_ASELS | saatlik raw h2 +93,8 (t 2,85), h3 +100 (t 2,4) | 2017–21 negatif, 2022+ pozitif | DÜŞÜK | KOŞULLU |
| 6 | Kredi notu kademe kararı: tepki günü uzlaşmasında ters yön, 2 gün | F_XU030 | h1 +61 / h2 +156 (t 3,0, bootstrap p 0,016) / h3 +180; n=16 | 2017–21 +160 (n=7) / 2022–26 +152 (n=9) | DÜŞÜK | KOŞULLU |

Ayrıntılar:

**1. ABD rafinerileri → TUPRS.** İşlem/yıl ≈53 (h2), 43 (h3); yıllar h2: 2017 −12, 2018 +20, 2019 −39, 2020 +121, 2021 +19, 2022 +75, 2023 +70, 2024 +54, 2025 +36, 2026 +23 (8/10 pozitif). Spot 2014–26 h2 +37,1 (t 3,0), 10/13 yıl. Hedge'li h2 +31,2 (t 2,6), h3 +42,2 (t 2,6). Regresyonda (hissenin kendi artığı kontrollü) t 3,3–4,5; 47 hisse içinde 1. sırada (DF ve DS); birini-dışarıda-bırak t 2,8–4,1; kriz günleri çıkarılınca t 3,9; bir gün daha eski sinyal de t 3,0 (yavaş, çok günlü sönüm). Basit β=1 sürüm (sepet − S&P 500) h3 +53,1 (t 2,6), 2025–26 +25,8 (raw) / +52,4 (hedged). Zayıf yanlar: IS'de işlem kuralı anlamlı değil (t 0,6–1,8); işlem kuralı PBF çıkarılınca t ~1'e düşüyor; saatlik 15:00 sürümü işlem kuralında ~0 (h2). KCHOL (Tüpraş payı) da aynı sinyale tepki veriyor (saatlik h3 hedged t 4,6). Brent tek başına daha zayıf (DF h3 +38, t 1,7).

**2. FMG/BHP → EREGL.** ASX BIST açılmadan kapanır; sinyal sabah biliniyor ama t uzlaşmasından sonra da 2–3 gün etkili. İşlem/yıl ≈50 (h2), 43 (h3). Yıllar (DF h3 hedged): 2017 +50, 2018 +69, 2019 +64, 2020 +121, 2021 +52, 2022 −37, 2023 −14, 2024 +3, 2025 +73, 2026 +89. Basit sürüm (FMG+BHP − ASX200) raw h3 +60,6 (t 2,9), 15 bps +53,6 (t 2,6), IS +67,6 (t 2,5) / OOS +53,9 (t 1,7), 9/10 yıl, 2025–26 +105,9. Bağımlılık: etki büyük ölçüde FMG'den (FMG çıkarılınca t≈0); bir gün eski sinyal etkisiz (hızlı sönüm); OOS IS'den zayıf; 2022–24 sönük. KRDMD'de yalnız OOS'ta (IS ≈0) → DÜŞÜK.

**3. VİOP altın → TRALT.** Hedge'li sürüm ham sürümden iyi (ham h2 +41,6, t 2,3). Yıllar h2 hedged: 2019 +48, 2020 +113, 2021 −44, 2022 −8, 2023 +43, 2024 +41, 2025 +64, 2026 +154. Saatlik (COMEX altın 15:00) TRALT h2 hedged +74 (t 2,1); TRMET saatlik h1 regresyon t 4,3. TRMET VİOP hedged h2 +45,6 (t 2,4), OOS +34,3 (t 1,4). Not: sinyal (XAUUSD uzlaşması) giriş fiyatıyla aynı 10 dakikada oluşur; pratikte 18:00–18:05 TSİ spot altın değişimi kullanılmalı. Önceki çalışmadaki uyarı geçerli: 2023Y2–2024Y2'de altın–TRALT bağı yoktu.

**4. VİOP USDTRY → THYAO.** Yıllar h3: 2017 −16, 2018 +83, 2019 −46, 2020 +88, 2021 +291, 2022 +314, 2023 +223, 2024 +112, 2025 +71, 2026 +34. Regresyon t 5,2 (küresel FDR q 0,004). Kriz pencereleri (2018-08/09, 2020-03/04, 2021-11/2022-01, 2023-05/06, 2025-03/04, 2026-09/10) çıkarılınca h3 +54,9 (t 2,2). 2024+ regresyon t 1,2. Kazancın çoğu "kur yükseldi → al" tarafında (brüt +187 vs "kur düştü → sat" +55). XU030'da yok (t 0,5–0,9) → ihracatçıya özgü (VESTL h2 +114, t 4,6; ihracatçı sepeti hedge'li t 3,7–4,7). Spot kurla (Yahoo t-1, saatlik 15:00) aynı sonuç çıkmıyor (t ≈0–1,6): etkinin bir kısmı vadeli USDTRY'nin baz/faiz bileşeninden ve kur şoku günlerinden geliyor. Kullanım: TL şoku dönemlerinde ihracatçı vadelisi; sakin yönetilen kur döneminde küçük.

**5. Avrupa savunma → ASELS.** Saatlik (2023-12+) yıllar h2: 2024 +38, 2025 +182, 2026 +55. Günlük vekil (t-1) 2014–21 sıfır/negatif, 2022+ pozitif (DS raw h2 2022 +79, 2023 −72, 2024 +57, 2025 +125, 2026 +58). Savunma temasının yaşandığı rejime bağlı.

**6. Kredi notu.** 2026 güncellemesi (web): kademe değişikliği yok. Görünüm: Fitch 23.01.2026 pozitif (eklenmişti; h2 −130), Fitch 10.04.2026 pozitiften durağana (eklendi; h2 +61). Moody's 23.01 ve 24.07.2026 Ba3 durağan (aksiyon yok), S&P 17.04 ve 16.10.2026 BB- durağan (aksiyon yok). Kademe + görünüm n=25 +115 (t 3,0, p 0,025); yalnız görünüm n=9 +44 (t 0,9). Düşürmelerde +190 (n=10), yükseltmelerde +99 (n=6). Son iki kademe kararı kayıp (S&P 2024-11 −217, Moody's 2025-07 −53). Spot XU030 2014+ kademe n=19 h2 +164 (t 3,5). 47 hissede medyan h2 +102 bps, 141 testte FDR 5 (PGSUS, SASA). Yılda ~1,5 olay; önceki çalışmadaki 2000–13 ve diğer ülke testleri genellemiyor → DÜŞÜK.

## İşlenemeyen / zayıf (olumsuz bulgular)
- **Havayolu sepetleri → THYAO/PGSUS/TAVHL:** saatlik raw h2 THYAO +55,6 (t 2,2), PGSUS +63,1 (t 2,3) ama günlük vekillerde net 8 bps'te +5…+20 (t <1,5), hedge'li ≈0; 2026 negatif. DÜŞÜK. Önceki gün-içi etki t günü içinde tükeniyor.
- **TKC → TCELL:** kapanıştan kapanışa işaret ters (DF hedged h2 −37,4 bps, t −3,0): TCELL'in kendi dönüşü, emsal bilgisi değil (P katsayısı hisse artığı kontrolünde ≈0). Saatlik parite sinyali +8 bps (t 0,5). ÇOK DÜŞÜK.
- **Küresel bira → AEFES:** DF hedged h1 +18,3 (t 1,5), saatlik negatif. DÜŞÜK. (BIRA sepeti hedef dışı PGSUS'u FDR'de öngörüyor — mekanizma yok, sahte kabul edildi.)
- **Avrupa/ABD/Japon çeliği → EREGL/KRDMD/BRSAN:** t ≈0–1,9; Japon çeliği EREGL'de ters. ABD çeliği/OCTG → BRSAN saatlik +20–43 bps/σ, t 1,6–2,1, VİOP BRSAN 2024-04+ (kısa). DÜŞÜK.
- **Altın madencileri (GDX, NEM…) → TRALT/TRMET:** VİOP altının kendisinden zayıf.
- **(b) Çok günlük ES, EEM, Brent, COMEX altın, TUR, DİBS 2y/10y → 47 hisse + F_XU030:** 50.688 testte sürücüye özgü FDR'den geçen yok (VİOP USDTRY hariç). TUR 2–3 günlük (t-1) → XU030 h1–h3 t 2,0–2,5 hem VİOP hem spotta, FDR yok → DÜŞÜK. "Sürücü − hisse ayrışması" biçimi (div) sürücüden bağımsız olarak hissenin kendi 2–3 günlük momentumunu/dönüşünü ölçüyor (XU030'da kısa vadeli momentum t −1,4…−2,1 işaretli div katsayısı).
- **(d) FOMC / NFP / CPI risk:** F_XU030 1/2/3 günlük std oranı (olay/diğer) FOMC 1,03 / 1,07 / 1,19 (bootstrap p 0,74 / 0,47 / 0,21); NFP 0,84 / 1,06 / 0,99; CPI 0,86 / 0,73 / 0,89 (n=34, 2023-12+). 47 hissede medyan 0,91–1,05; 441 std testinde FDR 4 (rastgele hisseler). Olay pencerelerinde pozisyonu yarıya indirmek oynaklığı %28,7 → %25,7–28,3 düşürüyor, Sharpe 0,21 → 0,12–0,20 → getiri kaybı risk azalmasından büyük. FOMC ertesi F_XU030 +44,9 bps (t 2,1, n=77), spot XU100 +54 (t 3,4, n=102) ama 2014–20 +7 (t 0,4), 2021–26 +109 (t 4,4); 2025 −7 → rejim, alfa değil. Pratik: bu günlerde pozisyon küçültmeye istatistiksel gerekçe yok.
- **(e) Akşam seansı (ES vekili, 2024-06 → 2026-10, n=592):** F_XU030 uzlaşma→ertesi uzlaşma varyansının yalnız %2,8'i akşam seansı süresince (ES 15:15→20:00 UTC), %7,4'ü gece (20:00→06:00), %7,1'i ertesi gün ES hareketiyle açıklanıyor (R² 0,15; ES dışı TR'ye özgü bilgi baskın). ES akşam hareketinin ertesi uzlaşmaya geçişi 0,34 (t 2,9), gün-içi eşzamanlı beta 0,37. Akşam stop (ES akşam −%0,25'ten kötüyse akşam seansında kapat; akşam fiyatı modelle): günlük std 176 → 157 bps (−%11), %5 kuyruk −264 → −231, ortalama −8,8 → −7,8 (değişmiyor). Akşamda ES yönünde giriş +3…+24 bps, t ≤1,1 → alfa yok. Akşam fiyatı bültende yok → DÜŞÜK; yalnız endeks vadelisi için risk aracı (pay vadelisi akşam seansında yok).

## Riskler ve sınırlamalar
- Seçim yanlılığı: adaylar 1. turdan biliniyordu; sepetler önceden kaydedildi ama "hangi biçim (raw/hedged, h)" seçimi sonuçlara bakarak yapıldı. Önerilen h=2–3 ve |z|>1 tüm adaylarda ortak; eşik 0,5'te net etki yarıya iniyor, 1,5–2'de gürültü artıyor.
- Saatlik örneklem 2,9 yıl; günlük vekiller Avrupa/ABD için t-1 bilgisini kullanıyor (t günü 15:00'e kadarki kısım dışarıda), yani muhafazakâr.
- VİOP uzlaşma fiyatından dolum varsayıldı; uzlaşma son 10 dk VWAP olduğu için kapanış müzayedesine yakın işlemle gerçekleştirilebilir ama kayma olabilir. Hisse vadesi maliyeti y_viop_likidite'den: TUPRS 6,2 / EREGL 7,2 / TRALT 6,5 / THYAO 5,9 / ASELS 6,1 bps (küçük emir), 1 mn TL emirde 9–16 bps.
- Rejim: TL şokları, altın rallisi (2025–26), savunma teması (2022+) etkileri büyütüyor. Korelasyon nedensellik değildir.

## Dosyalar
- res/a_peers_{H,DF,DS}.csv (emsal regresyon testleri), res/a2_trades_summary.csv (işlem kuralı), res/a2_pooled.csv, res/r_robust_peers.csv, res/r_simple.csv (basit kurallar)
- res/b_multiday_{F,S,H}.csv, res/r_robust_usd.csv
- res/c_rating_events.csv, res/c_rating_summary.csv, res/c_rating_47.csv
- res/d_macro.csv, res/d_halfrule.csv · res/e_evening.csv · res/global_bh_ab.csv
