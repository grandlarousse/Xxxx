# v_cin_gunici_olay_tarama — Bağımsız doğrulama (Çin vekilleri, gün-içi, olay, tarama)

Doğrulayıcı: v_cin_gunici_olay_tarama · Tarih 02.11.2026 · Veri sonu 30.10.2026
Kod: `out/code_v_cin_gunici_olay_tarama/` (vcore.py, v0_timing, v1_cin, v2_gunici, v2b_tur_robust, v3_olay, v3b_fomc_placebo, v3c_fomc_h1, v3d_weekday_spx, v4_tarama, v4b_ks_timing). Loglar ve CSV'ler: `res/`.
ll.py / olib / tlib / cin_lib IMPORT EDİLMEDİ. Ham parquet'ten kendi hizalamamı yazdım:
- FX '=X' için ldate=t kapanışı t günü 00:00 UTC'dir. h1 ile doğruladım: TRY=X günlük_t ile h1 00:00 r=0,85, düzeltme sonrası 23:00 r=0,84. Bu yüzden shift(-1) uyguladım.
- BIST hisseleri: fiyat bazında ±%10,5 simetrik temizlik, hacmi 0 olan günler atıldı, 2014 öncesi gap/intra NaN.
- Sürücüler BIST takvimine "yerel tarih ≤ t olan son kapanış" kuralıyla oturtuldu.
- Kısmi korelasyonda her iki seri ortak örneklemde kontrollere göre OLS artığı alındı. t değerleri HC0.
- Zamanlama kontrolleri (`v0_timing.log`):
  - XU030 günlük 'o' = m5 06:55 açılış müzayedesi barının 'c'si (%100).
  - ^KS11 günlük_t ile h1_t arasında r=0,975, günlük_t ile h1_{t±1} arasında ≈−0,06. Kore etiketi doğru, kapanış ~06:30 UTC.
  - XU030 h1 son barı kışın 13:30 (14:30 barı eksik).

## 0. Karar özeti

| İddia | Yeniden üretim (benim rakamım) | Karar | Güven (iddia → benim) |
|---|---|---|---|
| C1 CSI300/SSE → ASHR/KBA/CNYA haftalık r 0,83–0,89 | CSI300: ASHR 0,87 / KBA 0,82 / CNYA 0,87 (bağımsız haftalandırma); ortak-gün ile 0,91 / 0,86 / 0,92. Sina–Yahoo SSE günlük r 0,99998 | KABUL (KBA notu) | YÜKSEK → YÜKSEK (ASHR, CNYA); KBA SSE için ORTA |
| C2 HSI → FXI/MCHI/EWH haftalık 0,84–0,89 | 0,88 / 0,87 / 0,85. EWH: son 1y 0,68, 2026 0,65; HSCEI–EWH 0,75 | DÜZELT | YÜKSEK → FXI, MCHI YÜKSEK; EWH ORTA |
| C6 TIO1! aylık ortalama, ay sonu oynaklık çöküşü | |r| ay başı %1,96 → ay sonu %0,23 (DCE düz %1,6). Ayın 1. işlem günü |r| %4,5 (roll sıçraması). TIO2!/FEF2! test edilemedi (Yahoo kontrat ayları 404) | KABUL | (ORTA) → teşhis YÜKSEK, öneri ÇOK DÜŞÜK (test yok) |
| G1 ES gece → XU030 gap 0,45; 47 medyanı 0,36 | 0,47 (HC t 8,8); IS 0,49 / OOS 0,44; 3/3 yıl. Medyan 0,354. Açılış öncesi (06:00) ES ile de 0,47. Uzun örneklem ES_{t-1}→gap 13/13 yıl + | KABUL | YÜKSEK → YÜKSEK (işlenemez) |
| G4 TUR | ES pc 0,15 | 0,149 (HC t 2,0); IS 0,12 (t 0,9) / OOS 0,18 (t 3,1); yıllar −0,03 / +0,30 / +0,06; winsor 0,20 (t 3,7); etkili 10 gün çıkınca 0,06 | KABUL (kırılgan) | ORTA → ORTA (sınırda DÜŞÜK) |
| G5 5 dk ES→XU030 lag1 ≈0 | lag0 0,19, lag1 0,002; Σβ1..6 t 0,10; ABD açılışında lag1 −0,01; 47 hissenin 1'inde t>2 | KABUL | ÇOK DÜŞÜK (ilişki yok) |
| V2 FOMC gecesi gap β 0,22 vs 0,09 | Rakam aynen çıkıyor, ama FOMC dışı Çarşamba gecelerinde β 0,20; Perşembe içinde fark Δβ 0,05 (t 0,6); OOS 0,17 vs 0,22; h1 kesin gece penceresiyle FOMC 0,34 vs diğer 0,40. |gap| büyümesi gerçek: 1,38x (Perşembeye göre), MW p<0,001, IS ve OOS | DÜZELT | ORTA → β: DÜŞÜK; |gap| (oynaklık): ORTA |
| V3 negatif siyasi şok XU100 gap −215 bps (n 18) | −215 bps (t −3,23), medyan −188, 14/18 negatif; XBANK cc −399 (t −3,29). Seans dışı n 13: −264. IS −239 / OOS −196. dir=+1: +233 bps (8/8) | DÜZELT (yöntem) | ORTA → ORTA (betimleyici, işlenemez) |
| V5 XAUTRY pc: TRALT 0,29, TRMET 0,25, GUBRF 0,26 | Bu değerler yalnız 2023-12+ eşzamanlı (15:00 UTC) örneklemde çıkıyor: 0,31 / 0,25 / 0,27. Tam 2014–26 (XU100 kontrollü): 0,15 / 0,10 / 0,05. GUBRF IS −0,04, 2014–23 yılları ≈0 | DÜZELT | TRALT YÜKSEK; TRMET ORTA (rejim); GUBRF DÜŞÜK |
| TR1 ^KS11_{t-1} → XU030 gün-içi r 0,071 | r 0,071 (t 3,57), 11/13 yıl. Kore lag0 (Kore t seansı, BIST açılışından önce biter) r 0,017. Asya-3 ortalaması 0,073; KS11 \| N225, TWII 0,038 (OOS t 1,1); makro gecikme kontrollü 0,040 | DÜZELT | DÜŞÜK → DÜŞÜK (Kore'ye özgü değil) |
| TR2 USD XU100 EEM Dimson β 0,85 / 0,15 / 0,60 | 0,85 / 0,15 / 0,60 aynen; haftalık β 0,91 / −0,00 / 0,63; 15:00 eşzamanlı USDTRY ile de 0,49 / 0,29 / 0,64 (2024 / 25 / 26) | KABUL | ORTA → ORTA |
| TR3 20 hisse "küresel sürücüsü yok" | 992 sürücü × 2 lag: max \|pc\| 0,064–0,102; 39.360 testte 4 FDR geçişi, replike olan yok. Ancak USDTRY kontrol olduğu için görünmüyor: ENKAI +0,13 (t 5,4), VAKBN −0,16, ISCTR −0,12, HALKB −0,11. TCELL–TKC pc 0,66 ama ayna | DÜZELT (ifade) | → YÜKSEK ("XU100+USDTRY dışında, ayna hariç, ek küresel sürücü yok") |

## 1. C1 / C2: Çin ve HK vekil sadakati (v1_cin.py, res/c1c2_*.csv)
Dönem 2014+ (CNYA 2016-06+). Haftalık Cuma–Cuma getiri; ortak işlem günleri ve bağımsız haftalandırma ayrı ayrı hesaplandı.

| Orijinal–vekil | günlük | alt_t→orig_t+1 | 2g | haftalık (ortak gün / bağımsız) | IS / OOS / 3y / 1y (haftalık) | yıl-min | yıl ≥0,80 |
|---|---|---|---|---|---|---|---|
| CSI300–ASHR | 0,79 | 0,14 | 0,87 | 0,91 / 0,87 | 0,90 / 0,92 / 0,91 / 0,91 | 0,86 | 13/13 |
| CSI300–KBA | 0,76 | 0,13 | 0,82 | 0,86 / 0,82 | 0,92 / **0,78** / 0,86 / 0,82 | 0,64 (2022) | 12/13 |
| CSI300–CNYA | 0,77 | 0,11 | 0,88 | 0,92 / 0,87 | 0,92 / 0,92 / 0,91 / 0,89 | 0,82 | 11/11 |
| SSE–KBA | 0,73 | 0,15 | 0,78 | 0,82 / 0,79 | 0,90 / **0,71** / 0,78 / **0,66** | 0,59 | 10/13 |
| HSI–FXI | 0,65 | 0,27 | 0,79 | 0,88 / 0,87 | 0,87 / 0,90 / 0,88 / 0,82 | 0,80 | 12/13 |
| HSI–MCHI | 0,64 | 0,28 | 0,77 | 0,87 / 0,85 | 0,85 / 0,89 / 0,88 / 0,78 | 0,76 | 12/13 |
| HSI–EWH | 0,65 | 0,20 | 0,78 | 0,85 / 0,83 | 0,86 / 0,83 / 0,82 / **0,68** | 0,65 (2026) | 10/13 |
| HSCEI–FXI | 0,68 | 0,26 | 0,82 | 0,90 / 0,89 | 0,90 / 0,91 / 0,90 / 0,88 | 0,82 | 13/13 |
| HSCEI–EWH | 0,59 | 0,19 | 0,70 | 0,75 / 0,74 | — / — / 0,76 / **0,56** | 0,53 | 4/13 |

- İddia edilen aralık (0,83–0,89) iki haftalandırma yönteminin arasında kalıyor ve yeniden üretildi.
- **KBA OOS'ta zayıflıyor.** Endeks değişikliği olabilir (MSCI China A 50 Connect). Şanghay için son 1y 0,66, bu yüzden SSE için KBA ORTA.
- **EWH**, MSCI Hong Kong'u (yerel finans ve gayrimenkul) izliyor. Teknoloji ağırlıklı HSI ve HSCEI ile son yıllarda ayrışıyor: 2026'da 0,65, HSCEI ile 0,75. Bu yüzden EWH ORTA. FXI ve MCHI YÜKSEK.
- **BIST tarafı (iddianın parçası değil ama önemli)**:
  - XU100 haftalık korelasyonları: CSI300 0,18, ASHR 0,17, HSI 0,27, FXI 0,23, EWH 0,25. IS'ten OOS'a sert düşüş var: HSI 0,46 → 0,13.
  - **EEM + USDTRY kontrollü kısmi korelasyon**: CSI300 −0,01, HSI −0,01, ASHR −0,10, FXI −0,14, MCHI −0,16.
  - Yani Çin'e özgü faktör BIST için bilgi taşımıyor. Görünen bağ EM faktörü. ETF'ler EEM kontrolünden sonra negatife dönüyor, çünkü Çin ile EM-hariç-Çin ayrışmasını ölçüyorlar.
  - Günlük XU100 için ASHR_{t-1} r 0,03, CSI300_t r 0,08.
  - Vekil iyi bir vekil, ama BIST'i açıklayan bir sürücü değil.

## 2. C6: TIO1! (v1_cin.py C6; res/c6_*.csv)
DCE demir cevheri serisini Sina tekil kontratlarından kendim kurdum: önceki günün maksimum açık pozisyonu, yalnızca ileri vadeye roll, 2018-05 → 2026-10, 26 kontrat. Analiz 2019+.

| ayın günü | n | TIO \|r\| % | DCE \|r\| % | corr(TIO, DCE) |
|---|---|---|---|---|
| 1–7 | 354 | 1,96 | 1,59 | 0,52 |
| 8–14 | 448 | 0,87 | 1,71 | 0,75 |
| 15–21 | 432 | 0,47 | 1,56 | 0,56 |
| 22–31 | 567 | 0,23 | 1,59 | 0,44 |

- Ay sonuna sayımla: son 2–3 gün |r| %0,18, corr 0,35.
- **Ayın 1. işlem günü |r| %4,5**. Bu, Yahoo sürekli serisinin yeni ay kontratına geçişindeki roll sıçraması. Ek bir sorun olarak, TIO1! gibi sürekli seride getiri istatistiklerini kirletiyor.
- Haftalık TIO–DCE r 0,60, aylık 0,55. İddia doğrulandı. Mekanizma sözleşmeden geliyor (ön ay = ayın ortalama fiyatı, ilerledikçe sabitleniyor). Teşhis için güven YÜKSEK.
- TIO2! ve SGX:FEF2! önerisi mantıklı ama **test edilmedi**: Yahoo'da TIOX26.CMX, TIOZ26.CMX, TIOF27.CMX, TIOG27.CMX için HTTP 404 döndü. Öneri için güven ÇOK DÜŞÜK, ticker '?'.

## 3. G1 / G4 / G5: gece ve gün-içi (v2_gunici.py, v2b_tur_robust.py; res/g1_g4_stocks.csv, g5_stocks.csv)
Gece penceresi: ES h1 snapshot, önceki BIST günü 15:00 UTC → bugün 07:00 UTC (bar bitişine göre). 2024-06-11 → 2026-10-27, n=558. Yarım günler (7 adet) ve ertesi günler hariç.

**G1**
- XU030 gap ~ ES: r **0,472**, β 0,41, HC t 8,8 (OLS t 12,6; iddiadaki t 6,8 daha muhafazakâr).
- IS (≤06/2025) 0,49, OOS 0,44, son 1y 0,49. Yıllar: 2024 0,47, 2025 0,47, 2026 0,52.
- Açılış müzayedesi öncesi ES (15→06 UTC) ile r 0,468, yani 07:00 snapshot'ı sonucu şişirmiyor.
- Ortak faktör testi: USDTRY gecesi + EEM (15:30→kapanış) kontrolünden sonra 0,425.
- XU100 0,451. Winsor %1 ile 0,495. Spearman 0,41.
- 47 hisse medyanı **0,354**:
  - bankalar 0,44–0,52 (HALKB 0,33);
  - SASA 0,26, ENJSA 0,22, ASELS 0,26;
  - en düşük TUPRS 0,07.
- XU100 gap kontrolünden sonra hisseye özgü ES maruziyetinin medyanı 0,04. Bu bir piyasa faktörü.
- Gün-içi devam: r 0,03 (t 0,5).
- Uzun örneklem (günlük, 2014+): XU030 gap_t ~ ES_{t-1} r 0,148, ^GSPC_{t-1} 0,170, TUR_{t-1} 0,188. **13/13 yıl pozitif**, IS ve OOS ikisi de pozitif.
- Güven YÜKSEK, ama ilişki açılış müzayedesinde fiyatlanıyor; işlenemez.

**G4**
- TUR (t-1 günü 15:30 → ABD kapanışı) | ES: pc **0,149**, HC t 2,04.
- IS 0,117 (t 0,9), OOS 0,182 (t 3,1), 1y 0,09. Yıllar: 2024 −0,03, 2025 +0,30, 2026 +0,06.
- Etki olay günlerine bağlı:
  - en etkili 10 gün (2025-03-19 İmamoğlu, 2024-08-05, 2026-03-09/10 …) çıkarılınca 0,063 (t 1,5);
  - 17.03–30.04.2025 hariç 0,099;
  - winsor %1 ile 0,20 (t 3,7), rank-kısmi 0,16.
- ES + USDTRY + EEM kontrolüyle 0,26 (EEM | ES negatif, bastırıcı etki). Bu, Türkiye'ye özgü kapanış-sonrası haber kanalını destekliyor.
- Hisseler: pc(TUR | ES) medyanı 0,107, 28/47 hisse >0,10 (iddia: %51). Doğrulandı.
- TKC → TCELL gap r 0,151; TKC | ES, TUR −0,05. İddia (−0,02) doğrulandı.
- Güven ORTA (mekanizma güçlü, istatistik kırılgan).

**G5**
- m5, 2026-08-21..10-30, 49 gün, 4.245 bar; sürekli işlem 07:00–14:55 UTC.
- lag0 0,194, lag1 0,002, lag2 0,02. XU önde (XU_k → ES_{k+1}) −0,01. XU030'un kendi lag1'i 0,02.
- Regresyon XU ~ ES0..6 + XU1..6: β0 0,63 (t 12), Σβ1..6 0,014 (t 0,10), gecikmeli pay %2.
- ABD açılış penceresi: lag1 −0,01.
- 47 hisse: lag1 medyanı 0,002, 47 hissenin 1'inde Σβ1..6 t>2 (şansla beklenen ~1).
- Olumsuz bulgu sağlam. Sınırlama: yalnız yaz aylarını ve fon krizi dönemini kapsıyor.

## 4. V2 FOMC (v3_olay.py, v3b/v3c/v3d)
- FOMC tarih listem (planlı toplantıların 2. günü, 102 karar 2014–2026; 2020'deki 2 olağanüstü toplantı hariç) kaynak listeyle **birebir aynı**.
- Tepki günü = karardan sonraki ilk BIST günü (29 Ekim / 1 Mayıs tatilleri doğru atlanmış).
- Yeniden üretim, XU100 gap_t+1 ~ ES günlük_t:
  - FOMC β **0,223** (r 0,353, n 102), normal β **0,096** (r 0,147). İddia aynen çıkıyor.
  - Etkileşim farkı tam dönemde t 1,72 (anlamsız). IS'te 0,30 (t 2,8), **OOS'ta 0,03 (t 0,4)**.
  - Yıllara göre 10/13 yılda FOMC β > normal β, ama 2022, 2025 ve 2026'da FOMC β ≤0.
- **Plasebo bu iddiayı bozuyor.** FOMC dışı Çarşamba gecelerinde (Perşembe tepki günleri) β **0,200** (r 0,34, n 549).
  - Perşembe günleri içinde FOMC farkı Δβ 0,047 (t 0,58).
  - Haftanın gününe göre β (FOMC dışı): Pazartesi 0,11, Salı −0,04, Çarşamba 0,09, Perşembe 0,20, Cuma 0,16. ^GSPC_{t-1} ile aynı desen çıkıyor, yani ES verisine özgü bir hata değil.
  - FOMC tutanak geceleri (karardan +21 gün sonraki Çarşamba): β 0,27, r 0,60.
  - Sebep: günlük ES getirisinin BIST kapanışından (15:00 UTC) sonraki payı güne ve olaya göre değişiyor. Regresyon payı 2024+ döneminde Pazartesi 0,16, Çarşamba 0,81. Gap betası bu bileşimi ölçüyor.
- Kesin gece penceresiyle (h1 ES 15→07 UTC, 2024-06+): FOMC β 0,34 (n 20), diğer günler 0,40. FOMC'ye özgü yükseliş yok.
- **Gerçek olan kısım oynaklık.**
  - |gap| FOMC sonrası 59 bps, FOMC dışı Perşembe 43 bps; oran 1,38, Mann–Whitney p<0,001.
  - IS 1,46, OOS 1,29. |intra| oranı 1,12. XBANK 1,38x.
- Düzeltilmiş iddia: "FOMC gecesi BIST gap'i daha oynak (|gap| ≈1,3–1,4x; ORTA). Gap'in ES'e betası FOMC'ye özgü değil, Çarşamba gecesi bileşim etkisi (DÜŞÜK)." İşlenemez.

## 5. V3 siyasi şoklar (v3_olay.py; res/v3_political.csv)
- Kaynak listedeki dir=−1 olan 18 olay: XU100 gap **−215 bps** (t −3,23), medyan −188, 14/18 negatif. XBANK cc −399 (t −3,29). İddia aynen çıktı.
- Kesit (hisse − XU100 cc) doğrulandı:
  - bankalar: VAKBN −140 (t −3,2), HALKB −131, YKBNK −129, GARAN −123, ISCTR −120;
  - döviz gelirliler: TAVHL +223 (t 3,2), ENKAI +210 (t 3,4), TKFEN +177, TUPRS +150, TRALT +144, CIMSA +124.
- t+1..5 sürüklenme: +101 bps (t 0,9), anlamsız. 20.000 rastgele 18 günlük permütasyonda p<0,0001.
- **Sorunlar:**
  1. 5 olay "in_session" (2016-05-05, 2018-05-23, 2018-08-10, 2021-11-23, 2026-09-16). Bu günlerde gap olaydan ÖNCE oluşuyor (ort. −88 bps). Doğru ölçüt seans dışı alt küme: n 13, **−264 bps** (t −3,0), 10/13 negatif.
  2. Yön etiketleri kısmen geriye dönük. dir=+1 olan 8 olayın gap'i +233 bps (8/8 pozitif). Bazı etiketler tartışmalı: 2026-09-17 SPK tasfiye kararı "−1" etiketli ama XU100 cc +291, XBANK +851. 2022-02-24 (Rusya) ve 2023-02-06 (deprem) siyasi olay değil.
  3. Sonucu birkaç olay taşıyor: 2015-06-08 (−850), 2025-03-19 (−711), 2023-05-15 (−659). En büyük 2 olay çıkarılınca −145 (t −2,8).
  4. 2021-03-22'de gap −245 / gün-içi −785 ayrışması, o günkü sert açılış düşüşüyle uyumsuz görünüyor. Yahoo endeks açılış verisi 2023 öncesi için doğrulanamıyor.
  5. IS (n 8) −239, OOS (n 10) −196. İşaret aynı.
- Güven ORTA (betimleyici: olay riski ve korunma kesiti). Önceden belirlenmiş olay seçimi olmadığı için öngörü değeri yok.

## 6. V5 XAUTRY (v3_olay.py V5)
XAUTRY = GC=F × USDTRY (düzeltilmiş) günlük kapanış; eşzamanlı versiyon h1 15:00 UTC.

| hisse | pc \| XU100 tam / IS / OOS / 3y / 1y | yıllar | pc \| XU100+USD+EEM tam / IS / OOS | GC \| XU100+USD | 15:00 eşzamanlı (2023-12+) |
|---|---|---|---|---|---|
| TRALT | 0,149 / 0,110 / 0,170 / 0,256 / 0,337 | 12/13 | 0,190 / 0,191 / 0,187 (13/13) | 0,193 | **0,305** |
| TRMET | 0,097 / 0,032 / 0,154 / 0,236 / 0,289 | 8/13 | 0,123 / 0,072 / 0,172 (12/13) | 0,126 | **0,248** |
| GUBRF | 0,047 / **−0,036** / 0,113 / 0,197 / 0,383 | 7/13 | 0,072 / 0,005 / 0,116 (6/13) | 0,073 | **0,270** |

- İddiadaki 0,29 / 0,25 / 0,26 yalnızca son ~3 yılın (2023-12+) değerleri. Tam dönem için bu değerler abartılı.
- "Gram altın" ayrı bir sürücü değil. GC | XU100+USD ile XAUTRY | XU100+USD+EEM aynı sonucu veriyor; USDTRY tek başına TRALT için ~0. TV önerisi: COMEX:GC1! (+FX:USDTRY).
- GUBRF:
  - 2014–2023 arası yıllık pc ≈0 / negatif (2018 −0,25);
  - 2024 0,10, 2025 0,15, 2026 0,40.
  - Bu bir rejim etkisi ya da 2026 altın rallisi ile bireysel yatırımcı ortak hareketi. Ekonomik mekanizma şüpheli, güven DÜŞÜK.
- TRMET'te güç 2020 sonrası geliyor (Koza grubu kayyum dönemi?), güven ORTA.
- TRALT: pc ≥0,15, 13/13 yıl, IS ve OOS anlamlı, güven YÜKSEK.
- XBANK "ikame" etkisi (−0,11, XU100 kontrollü) USDTRY eklenince 0,01'e iniyor. Yani bu tamamen kur etkisi.

## 7. TR1 Kore (v4_tarama.py, v4b_ks_timing.py)
- **Tanım kontrolü:**
  - KS11_t = Kore seansı t. KS11 06:30 UTC'de, BIST açılışından (07:00) önce kapanır. Yani KS11 lag0 zaten öncü ve işlenebilir; gün-içi r **0,017** (t 0,9), yani yok.
  - Taramadaki "lag1" = KS11_{t-1} = bir önceki Kore seansı (BIST t açılışından ~24,5 saat önce biter). İddia bu tanımla aynen çıkıyor: r **0,071** (t 3,57), IS 0,075 / OOS 0,071 / 1y 0,161, 11/13 yıl.
- **Kore'ye özgü değil:**
  - N225_{t-1} 0,055, TWII_{t-1} 0,058, AXJO_{t-1} 0,041, Asya-3 ortalaması_{t-1} 0,073.
  - KS11 | N225, TWII_{t-1}: 0,038 (OOS t 1,1).
  - XU030'un kendi gecikmeleri + gap_t + KS11_t + ES_{t-1,t-2} kontrolüyle: 0,062 (t 3,2).
  - Bunlara EEM_{t-1}, USDTRY_{t-1}, XU100_{t-1}, N225_{t-1} eklenince: 0,040 (OOS t 1,5; 3y 0,02; 1y 0,01).
  - ES_{t-2} → intra_t 0,043.
  - corr(KS11_{t-1}, XU030 gap_{t-1}) = 0,32: Kore t-1 bilgisi BIST'e zaten bir gün önceki gap'te giriyor.
- Mekanizma şüpheli (iki günlük gecikme, lag0 sıfır). Taramanın tüm intra_l1 ailesinde 0 FDR geçişi var.
- Backtest XU030 gün-içi, z>1:
  - 8 bps maliyetle OOS +12,7 bps/işlem (t 1,5, Sharpe 0,63, n 422); 15 bps maliyetle t 0,7;
  - sign modu 8 bps maliyetle negatif.
- Güven DÜŞÜK. İddianın "Kore" çerçevesi düzeltilmeli: "Asya t-1 seansı ortak faktörü".

## 8. TR2 küresel beta rejimi (res/tr2_beta.csv)
USD bazlı XU100 (r_XU100 − r_USDTRY düzeltilmiş) ~ EEM_t + EEM_{t-1}. Dimson β:
- 2014–17: 0,85 (se 0,06)
- 2018: 0,68
- 2019–20: 0,74
- 2021: 0,57
- 2022–May23: 0,41
- Haz23–Mar25: 0,46
- 2023 yılı: **0,15** (se 0,20)
- Mar–Ara 2025: 0,17
- 2026 Oca–Ağu: **0,60**
- Eyl–Eki 2026: 0,72 (n 42)
- 2026 yılı: 0,63

İddiayla aynı. Sağlamlık kontrolleri:
- Haftalık β (asenkronluk yok): 0,91 / 2023 −0,00 / 2026 Oca–Ağu 0,63. Bu, deseni doğruluyor.
- 15:00 UTC eşzamanlı USDTRY ile: 2024 0,49, 2025 0,29, 2026 0,64.
- Eyl–Eki 2026 haftalık β 0,04 (n 9). Fon krizi tahmini güvenilmez.

Güven ORTA (betimleyici rejim; kısa pencerelerde se 0,1–0,2).

## 9. TR3 "küresel sürücüsü olmayan 20 hisse" (res/tr3_scan.csv)
Bağımsız tarama: XU100 + USDTRY kontrollü. 992 BIST-dışı sürücü (n ≥1000, sıfır oranı ≤0,3), lag0 ve lag1, TR aynaları (TUR, TKC, AKBTY, TKGBY, *TRY=X) hariç. Toplam 39.360 test.

- 20 hissenin max \|pc\| değerleri 0,064–0,102:
  - SISE–KRBN (karbon ETF'i) 0,101 (IS 0,13 / OOS 0,10; AB ETS maliyeti kanalı makul, izlenebilir);
  - TSKB–FORTUM 0,102;
  - HALKB–9863.HK 0,094 (kısa örneklem);
  - TTKOM–KRBN_{L1} −0,09.
- BH-FDR'den 4 çift geçiyor; hiçbiri IS ve OOS'ta sağlam biçimde replike değil.
- "İlk 5 bile \|pc\| ≤0,08" ifadesi küçük aşımlarla (≤0,10) doğru. Liste genel olarak doğrulandı.
- **Çelişki kontrolü:**
  - TCELL–TKC: pc | XU100+USD **0,66** (13/13 yıl). TKC aynı şirketin ADR'si; taramada bilerek "ayna" olarak dışlanmış. Öncülük bilgisi yok: TKC_{t-1} → TCELL gap | XU100 gap 0,047 (t 1,7), TUR eklenince 0,039, gün-içi −0,005. Ekonomik çelişki değil, ama listenin "TR aynaları hariç" diye belirtilmesi gerekiyor.
  - ENKAI–USDTRY: pc | XU100 **+0,128** (t 5,4; IS 0,10 / OOS 0,11; 11/13 yıl; ama 3y 0,00 ve 1y 0,05, sönüyor). USDTRY kontrol değişkeni olduğu için tanım gereği listede görünemez.
  - USDTRY maruziyeti anlamlı olan diğer hisseler: VAKBN −0,157 (t −6,9), ISCTR −0,116, HALKB −0,113, SISE +0,080, TKFEN +0,062, BIMAS +0,061, DOHOL +0,059, TTKOM −0,059.
  - Sonuç: liste "küresel sürücü yok" değil, "XU100 ve USDTRY dışında ek küresel sürücü yok (ayna hariç)" diye yazılmalı. ENKAI ve kamu bankaları için USDTRY anlamlı bir makro sürücü.

## 10. Genel notlar ve sınırlamalar
- h1 ve m5 iddiaları (G1, G4, G5) 2,4 yıl ile 49 gün arası verilere dayanıyor; IS 2014–2020 penceresi uygulanamadı. G1 günlük uzun örneklemle teyit edildi. G4 ve G5 edilemedi.
- Yahoo endeks açılışı (XU100/XU030 'o') 2023 öncesinde doğrulanamadı. Gap ve gün-içi ayrıştırması olay günlerinde hatalı olabilir (bkz. 2021-03-22).
- TIO2!, FEF2!, KRX:KOSPI ve FX_IDC:XAUTRY ticker'ları doğrulanmadı.
- Tüm bulgular korelasyondur; nedensellik iddiası yok. İşlenebilir olanlar yalnız TR1'in zayıf z>1 versiyonu (DÜŞÜK); diğerleri gap'te fiyatlanıyor ya da betimleyici.

Yeniden üretim:
```
cd out/code_v_cin_gunici_olay_tarama
nice -n 10 python3 v0_timing.py
python3 v1_cin.py
python3 v2_gunici.py
python3 v2b_tur_robust.py
python3 v3_olay.py
python3 v3b_fomc_placebo.py
python3 v3c_fomc_h1.py
python3 v3d_weekday_spx.py
python3 v4_tarama.py
python3 v4b_ks_timing.py
```
