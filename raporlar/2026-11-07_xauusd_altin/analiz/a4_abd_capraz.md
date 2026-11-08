# a4_abd_capraz — ABD/küresel çapraz varlıkların gecikmeli bilgisi → VİOP F_XAUUSD (1/3/5 gün, uzlaşmadan uzlaşmaya)

Tarih: 2026-11-07. Örneklem: VİOP 2017-03-06 → 2026-11-06 (2.427 gün). IS = 2017-03..2021-12, OOS = 2022-01..2026-11. Erken dönem tekrarı: spot panel 2010–2016 (hedef 15:00→15:00 UTC spot).
Kod: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz/` (`run_all.sh` hepsini sırayla yeniden üretir, ~1 dk).

## 0. Kısa sonuç

1. **Toplam 1.213 test kaydedildi** (`out/registry/a4_abd_capraz.csv`). Bunların 1.071'i birincil hipotez testi, kalanı sağlamlık ve tanı varyantı.
2. **Gecikmeli ABD kapanış değişimlerinin altını 1–5 gün öngördüğüne dair kanıt yok.** 35 varlık ve 6 faiz serisinde 1 ve 5 günlük z-ölçekli değişimlerle 240 IC testi yapıldı. Bunların yalnız %2,1'inde |t|≥2 çıktı; sıfır hipotezinde beklenen oran ≈%4,6. Dolar, 10 yıllık nominal/reel faiz, başabaş, S&P, Nasdaq, VIX, GVZ, MOVE, HY, petrol, bakır, gümüş, platin, BTC, EEM, FXI, TUR ve TLT/TIP'in hepsi bu sınıfta.
3. **Büyük hareket asimetrisinde de bir şey yok.** |z|>1,5 olay testlerinin 240'ında |t|≥2 oranı %5,4, yani şans düzeyi.
4. **18 saatlik emilim doğrulandı.** Dolar t-1 ABD kapanışında yükseldiyse altın [t-1 20:00 → t 15:00 UTC] penceresinde kısmen geri alıyor (DXY IC +0,058, t=2,76). Bu düzeltme VİOP girişinden önce bitiyor; t→t+h getirisine bir şey kalmıyor.
5. **Tek tutarlı bulgu: "madenciler altından güçlüyse altın izliyor".** GDXJ'nin GLD'ye göre 1 günlük beta-artığı (t-1 ABD kapanışları) VİOP 3 günlük getirisini öngörüyor: IC 0,068, t=3,53, IS t=2,53, OOS t=2,63, 10 yılın 9'unda aynı işaret. IS'te |t|≥2 ile seçilen 33 kuraldan OOS'ta aynı işaretle |t|≥2 veren yalnız madenci-artık kurallarıydı (GDX, GDXJ, RING; h=3).
6. **Madenci bulgusunun zayıf yanları da var.** 2010–2016 spot dönemde neredeyse sıfır (IC 0,016, t=0,63). Pearson (doğrusal) IS t'si yalnız 0,74. Birincil 1.071 test üzerinde BH-FDR q=0,43, yani global çoklu testi geçmiyor; yalnız kendi ailesi içinde geçiyor (q=0,013). Etiket: **ORTA**.
7. **Eğri dikleşmesi (Δ5 10y−2y → ertesi gün altın ↑) DÜŞÜK.** Tam dönemde t=3,15 ama IS'te t=1,87, yani ilişki tam örneklemde bulundu. 2010–2016'da işaret ters (IC −0,039; backtest Sharpe −0,72).
8. **Diğer adaylar çapraz varlık bilgisi taşımıyor.** "Dolar-sapması" kuralı aslında altının kendi gece momentumu; altının kendi getirisi kontrol edilince t=−0,72. Reel faiz + dolar modeli artığının OOS getirisi drift'ten geliyor (OOS demeaned Sharpe 0,06).
9. Altın/gümüş oranı z-skoru, GLD hacim şokları, madenci büyük olayları ve saatlik pencere sapmaları (11 Dukascopy varlığı × 3 pencere) için de **YOK / DÜŞÜK**.

---

## 1. Veri ve bilgi zamanı (ileriye bakma kontrolü)

Karar anı gün t 15:00 UTC. Giriş t uzlaşması (≈15:05–15:15 UTC VWAP), çıkış t+h uzlaşması. Hedef panelin `fwd{h}` sütunu, yani aynı kontrat içi uzlaşma log getirilerinin toplamı.

| Öngörücü grubu | Kaynak | Bilgi zamanı (UTC) | Kontrol |
|---|---|---|---|
| ABD hisse/ETF, madenciler, GLD, TLT, TIP, EEM, FXI, TUR (`y_*`) | Yahoo adjclose | t-1 20:00/21:00 (16:00 ET) | `y_*_avail` < t 15:00: **0 ihlal**, medyan 19 saat önce (`s1_bilgi_zamani.csv`) |
| Vadeliler (GC, SI, PL, PA, HG, CL, BZ, ES), DXY | Yahoo | t-1 21:00/22:00 (17:00 ET varsayımı) | 0 ihlal, medyan 18 saat |
| VIX, GVZ, MOVE | Yahoo | t-1 21:15 | 0 ihlal |
| BTC | Yahoo | t 00:59 | 0 ihlal, 14 saat |
| `ust_*` (nom2, nom10, real10, be10) | ABD Hazinesi | t-1 22:00 | panel as-of (t-1 değeri) |
| `xau_p15`, `dk_*_p15` | Dukascopy | t 15:00 (dahil) | Dukascopy saatlik ile birebir (max fark 0) |
| Saatlik pencereler A/B/C | Dukascopy BID, fiyat anı = bar başı + 1 saat | en geç t 15:00 | — |
| GLD hacmi | Yahoo GLD.parquet | gün D kapanışı (D = `y_GLD_avail` günü) | assert avail < t 15:00 |

- Sinyallerde **`v_*` / `vo_*` sütunu kullanılmadı.** Bu sütunlar yalnız getiri hesabında var, yani "kapanışta hesaplanan" sinyal yok.
- Kurlarda Yahoo `=X` kullanılmadı; Dukascopy saatlik kullanıldı.
- `y_GOLD` hariç tutuldu. Yahoo'da "GOLD" kodu 2025'te Barrick'ten başka bir şirkete geçti; GDX ile çeyreklik korelasyonu 0,02–0,70 arasında oynuyor. Barrick'in tarihi `y_B`'de (GDX ile çeyreklik korelasyon 0,75–0,99).
- `placebo_lead` ana adaylarda yapıldı (bkz. §5). Sinyal t'den daha eski bilgiye kaydırıldığında IC düzgünce azalıyor. Geleceğe kaydırınca (shift −1) değerin yükselmesi beklenen bir şey, çünkü x_{t+1} hedef pencerenin ilk gününü içeriyor.

## 2. Yöntem

- **Öngörücü dönüşümü.** Fiyatlarda log değişim, faizlerde seviye farkı (yüzde puanı). Her biri geçmiş 120 günün std'sine bölündü: z = r_t / std(r_{t−120..t−1}). Pencere w = 1 ve 5 gün.
- **Testler:**
  - (a) Spearman IC, Newey-West t (lag = max(h,5)); `split_stats` ile tam dönem, IS, OOS ve yıl yıl.
  - (b) Kısmi regresyon: altının kendi 15:00→15:00 getirileri (1 ve 5 gün) kontrol.
  - (c) Büyük hareket kuklaları z>+1,5 ve z<−1,5: olay sonrası ortalama fark (bps), NW t.
  - (d) Emilim tanısı: x(t-1 ABD kapanışı) → altın [t-1 20:00 → t 15:00]. Bu pencerede işlem yapılamaz; amaç bilginin VİOP girişinden önce fiyatlanıp fiyatlanmadığını görmek.
- **Göreli değer:**
  - Madenci/altın oranı değişimi ve beta-artığı: e = r_M − β60·r_GLD, β geçmiş 60 gün, `shift(1)`.
  - Altın/gümüş oranı (15:00 UTC) z-skoru, 20/60/120/250 gün.
  - Reel faiz + dolar seviye modeli: katsayılar **yalnız [t−W, t−1]** penceresinden, artık pencere dışı. İki sürüm var: ABD kapanışı ve 15:00 UTC.
  - Değişim modeli artığı.
  - GLD hacim şoku: log hacim − önceki 20 gün ortalaması, işaretsiz ve r_GLD işaretiyle.
- **Saatlik pencereler (Dukascopy).**
  - Pencereler: A = [t-1 15:00, t-1 20:00] ABD öğleden sonrası; B = [t-1 15:00, t 15:00]; C = [t-1 20:00, t 15:00].
  - Ölçüler: ham z(x) ve sapma = β·x − altın. β, aynı penceredeki geçmiş 250 günlük regresyondan.
  - Varlıklar (11): DXY, UST bond, S&P500 CFD, XAG, Brent, bakır, VIX CFD, EURUSD, USDJPY, USDCNH, BTC.
- **Backtest (`lib_altin.backtest`).**
  - Kademeli h-günlük tutuş; maliyet 5 bps gidiş-dönüş, stres 10 bps.
  - Sinyal → pozisyon eşlemesi IS'te üç seçenek arasından seçildi: işaret, z/2 kırpılmış, |z|>0,43 (≈ üst/alt üçte bir). Yön IS IC işaretinden.
  - Raporlananlar: buy&hold kıyası, demeaned Sharpe, uzun ve kısa bacaklar ayrı.
- **Sağlamlık:**
  - Roll günleri dışlandı: v_code(t) ≠ v_code(t+h) olan pencereler.
  - Düşük hacim dışlandı: t-1 hacmi, önceki 250 günün %10 diliminin altındaysa. Sıfır hacimli gün yok; en düşük hacim 600 kontrat.
  - Uç dönemler dışlandı: Mart–Nisan 2020 ve Ocak–Şubat 2026.
  - Hedef %1/%99 winsorize edildi; ayrıca Pearson ve sıra-tabanlı kısmi regresyon.
- **Çoklu test.** Kayıt üzerinde BH-FDR, global ve aile içi. Varyantlar BH'yi yapay biçimde gevşetebildiği için ayrıca "birincil evren" (s1–s3, tanılar hariç, 1.071 test) üzerinde de hesaplandı.

## 3. Tek değişkenli gecikmeli ABD kapanışları (s1, 760 test)

| Test ailesi | n | \|t\|≥2 oranı | Sıfır beklentisi |
|---|---|---|---|
| IC (35 varlık + 6 faiz × w{1,5} × h{1,3,5}) | 240 | **%2,1** | ≈%4,6 |
| Kısmi (altın öz-getirisi kontrollü) | 240 | %2,9 | ≈%4,6 |
| Büyük hareket (z>+1,5 / z<−1,5) | 240 | %5,4 | ≈%4,6 |

Tam dönemde |t|≥2 çıkan beş IC aşağıda. Hiçbiri IS'te |t|≥2 değil, yani hepsi tam örneklemde bulunmuş.

| Öngörücü | h | IC | t | t_IS | t_OOS | yıl |
|---|---|---|---|---|---|---|
| Δ5(10y−2y) | 1 | +0,065 | 3,16 | 1,88 | 2,58 | 7/10 |
| Δ5(10y−2y) | 3 | +0,062 | 2,16 | 0,81 | 2,16 | 6/10 |
| Δ5 nom2 | 1 | −0,050 | −2,47 | −1,10 | −2,32 | 5/10 |
| Δ1 paladyum | 3 | +0,042 | 2,12 | 0,32 | 2,46 | 7/10 |
| Δ5 GVZ | 1 | +0,044 | 2,03 | 0,51 | 2,18 | 6/10 |

**IS'te seçilip OOS'ta çöken kurallar (drift/aşırı uyum örnekleri):**

| Kural | IS t | OOS t |
|---|---|---|
| Δ5 DXY → h=5 | +2,75 | −0,85 |
| Δ5 UUP → h=5 | +2,60 | −0,82 |
| Δ1 TUR → h=3 | +2,70 | −0,86 |
| Δ5 platin → h=3 | −2,17 | −0,16 |
| Δ5 GLD → h=3 | −2,04 | +0,63 |

**Büyük hareketlerde** tam dönem |t|≥2 çıkanlar şunlar:

| Olay | h | Sonraki fark | t | t_IS | t_OOS |
|---|---|---|---|---|---|
| RGLD büyük yükseliş | 3 | +42 bps | 2,87 | 1,75 | 2,25 |
| GDXJ büyük yükseliş | 3 | +38 bps | 2,48 | — | — |
| NEM büyük yükseliş | 3 | +30 bps | 2,01 | — | — |
| Eğri büyük düşüş | 3 | −40 bps | −2,55 | −1,22 | −2,42 |
| EEM, FXI, TUR büyük düşüş | 1–3 | −21 ile −45 bps | 2–2,4 | — | — |

- **Madenci olayları** madenci-artık bulgusuyla aynı yönde. Ancak IS'te tek başına anlamlı değiller.
- **EEM, FXI ve TUR düşüşleri** IS ve OOS'ta tutarsız.

**Emilim tanısı (18 saat).** Hedef, altının [t-1 20:00 → t 15:00] hareketi; bu pencerede işlem yapılamaz.

| Öngörücü | IC | t | t_IS | t_OOS |
|---|---|---|---|---|
| Δ1 DXY | +0,058 | 2,76 | 1,61 | 2,23 |
| Δ1 UUP | +0,055 | 2,66 | 1,72 | 2,00 |

- Diğer bütün varlıklarda |t|<2.
- **Yorum:** ABD seansında doların sürüklediği altın hareketi gece ve Asya–Avrupa saatlerinde kısmen geri alınıyor. VİOP girişinden (t 15:10) sonrasına öngörü kalmıyor; dolar → fwd1 IC −0,018, t=−0,95.

## 4. Göreli değer (s2, 144 test) ve saatlik pencereler (s3, 229 test)

**Madenci/altın: beta-artığı (1 günlük), h=3**

| Madenci | IC | t | t_IS | t_OOS | yıl |
|---|---|---|---|---|---|
| GDX | 0,063 | 3,31 | 2,12 | 2,61 | 8/10 |
| **GDXJ** | **0,068** | **3,53** | **2,53** | **2,63** | **9/10** |
| RING | 0,063 | 3,18 | 2,14 | 2,39 | 8/10 |
| SIL (gümüş madencileri) | 0,041 | 2,02 | 1,15 | 1,77 | 9/10 |
| Sepet (NEM, AEM, B, KGC, FNV, WPM, RGLD) | 0,053 | 2,63 | 1,73 | 2,01 | 8/10 |

- **Madenci/altın:**
  - Ham oran değişimi Δ1 log(M/GLD), h=3, aynı resmi veriyor: t 2,2–2,8.
  - 5 günlük artık ve oran zayıf (|t| ≤ 2,2; IS'te hiçbiri |t|≥2 değil).
  - Madencinin tek başına getirisi zayıf: Δ1 GDXJ → h3 t=1,83. Yani bilgi madencinin altına göre ayrışmasında.
  - Artık büyük olayları (|z|>1,5) anlamlı değil: en iyi RING yükseliş h5 t=2,18, IS 0,99. Düşüş olaylarında hiçbir şey yok.
- **Altın/gümüş oranı z-skoru: YOK.**
  - W=120/250, h=5 IS'te t 2,4–2,5 verdi ama OOS'ta −0,21/+0,16.
  - Δ5 oran h=1 tam dönem −2,06, ancak IS'te −0,27.
- **Reel faiz + dolar seviye modeli: YOK.**
  - Tam dönem en iyisi 15:00 sürümü W=120, h=1: t=2,34, IS 1,62, OOS 1,70.
  - İşaret pozitif: artık momentumu var, ortalamaya dönüş yok.
  - Altının kendi getirileri kontrol edilince kısmi t=0,76; OOS demeaned Sharpe 0,06.
  - Değişim modeli artığı: |t|<1,7.
- **GLD hacim şoku: YOK.** İşaretli şok h=1'de IS t=2,11, OOS t=0,67. Büyük hacim olaylarında (n≈40–46) hiçbir şey yok.
- **Saatlik pencereler (198 test):**
  - |t|≥2 oranı %4,5; sıfır beklentisi %4,6.
  - IS'te |t|≥2 olan 11 kuraldan 8'inin işareti OOS'ta tersine döndü: S&P-A sapması (h1 ve h3), bakır-A (h1 ve h3), EURUSD-A, USDJPY-A, BTC-A ve XAG-A ham.
  - "DXY sapması C penceresi" için §5 C3'e bakın.
  - Altının kendi pencere getirileri: C penceresinde t=1,58, B'de t=1,66; zayıf pozitif momentum.

**IS → OOS aktarımı (s6).** IS'te |t|≥2 ile seçilen 33 kuraldan:
- %42'si OOS'ta aynı işaretli; bu yazı-tura düzeyi.
- Yalnız %9'u (3 kural: GDX, GDXJ ve RING artığı, h=3) OOS'ta aynı işaretle |t|≥2.

## 5. Adayların derin kontrolü (s4, s5, s7)

### C1 — GDXJ/GLD beta-artığı → 3 gün (ORTA)

**Kural:**
1. t-1 ABD kapanışında (≤21:00 UTC t-1) e = r_GDXJ − β·r_GLD hesaplanır; r = log adjclose değişimi (t-2 → t-1 kapanış), β = önceki 60 günün cov/var değeri.
2. z = e / std(e, önceki 120 gün).
3. z > +0,43 ise t uzlaşmasında uzun, z < −0,43 ise kısa açılır; 1/3 birim, 3 gün tutulur (kademeli).

| | Tam | IS | OOS |
|---|---|---|---|
| IC (Spearman), NW t | 0,068 / 3,53 | 0,067 / 2,53 | 0,072 / 2,63 |
| Net Sharpe 5 bps | 0,53 | 0,24 | **0,72** |
| Demeaned Sharpe 5 bps | 0,56 | 0,27 | **0,76** |
| Net Sharpe 10 bps | 0,31 | −0,04 | 0,53 |
| Yıllık getiri (5 bps) | %4,0 | %1,4 | %6,7 |
| Buy&hold Sharpe / yıllık getiri | 0,49 / %7,7 | 0,47 / %6,2 | 0,53 / %9,5 |
| Uzun bacak Sharpe (demeaned) | 0,73 (0,37) | 0,56 (0,22) | 0,87 (0,48) |
| Kısa bacak Sharpe (demeaned) | −0,03 (0,28) | −0,22 (0,08) | 0,09 (0,42) |

- **Yıl yıl strateji ve buy&hold (%):**

  | Yıl | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | Strateji | 4,9 | −4,7 | 5,8 | 1,6 | −1,0 | 4,4 | 11,0 | 8,1 | 0,8 | 8,0 |
  | Buy&hold | 4,5 | −4,2 | 14,1 | 20,6 | −5,0 | −4,6 | 4,2 | 16,3 | 44,9 | −15,8 |

  Strateji 2022'de ve 2026'da, yani altının düştüğü yıllarda da pozitif.
- **İşlem sıklığı.** Sinyal günü ≈143/yıl (her biri 1/3 birim, 3 gün tutuş); pozisyon taşınan gün ≈214/yıl; devir 68/yıl.
- **Sağlamlık (IC t; tam / IS / OOS):**

  | Kontrol | Tam | IS | OOS |
  |---|---|---|---|
  | Roll pencereleri hariç | 3,16 | 1,96 | 2,59 |
  | Uç dönemler hariç | 3,26 | 2,20 | 2,55 |
  | Winsor | 3,52 | 2,52 | 2,62 |
  | Düşük hacim hariç | 3,84 | 2,81 | 2,80 |
  | Sıra-tabanlı kısmi (g1, g5, S&P, VIX, r_GLD kontrollü) | 3,42 | 2,05 | 2,68 |
  | β=120 | 3,86 | — | — |
  | β=250 | 3,75 | — | — |
  | 2 faktör (GLD + S&P) | 3,60 | — | — |
  | GC=F kıyaslı | 2,65 | — | — |

- **Zayıf noktalar:**
  - **Pearson** IC t: tam 2,11, IS **0,74**. Etki sıralamada var, doğrusal büyüklükte zayıf. Pearson-tabanlı kısmi IS t −0,15.
  - **2010–2016 spot** IC 0,016, t=0,63; yıllar 2010: +0,06 … 2012: −0,19. Aynı kuralın backtest Sharpe'ı 0,15. Aynı sinyal 2017–2026 spot'ta t=3,26. Etki dönemsel olabilir.
  - **IS backtest Sharpe** yalnız 0,24, 10 bps'te negatif.
  - **Global FDR:** birincil 1.071 test üzerinde q=0,43; aile içi q=0,013.
- **İleri gün profili.** Günlük IC: t+1 0,041; t+2 0,032; t+3 0,029; t+4 0,000; t+5 0,017. Bilgi 2–3 güne yayılarak fiyatlanıyor. Emilim testi: e → altın [t-1 20:00 → t 15:00] IC 0,008, t=0,37. Yani gece fiyatlanmıyor.
- **Placebo.** IC kaydırmaya göre: shift +1: 0,036; +2: 0,018; +3: 0,005; −1: 0,058 (mekanik). Eski bilgiye doğru düzgün azalıyor.
- **Mekanizma (olası).** Madenci hisselerinde, özellikle küçük ve orta ölçekli GDXJ'de, altın beklentisi hisse yatırımcıları ve opsiyon akışıyla önden fiyatlanıyor olabilir. Literatür bunun tersini söylüyor: Lucey ve O'Connor 2017, 1998–2015 verisiyle "altın madencilere öncülük eder" buluyor. Bizim 2010–2016 erken dönem sonucumuz literatürle uyumlu, yani etki yok. Bu çelişki etiketi YÜKSEK'ten ORTA'ya indirmemin ana nedeni.
- **Etiket notu.** Kural sayısal YÜKSEK eşiklerinin hepsini 2017–2026 VİOP örnekleminde geçiyor: |t_full|≥3, IS/OOS aynı işaret, OOS t≥2, yılların %90'ı aynı işaret, OOS Sharpe ve demeaned Sharpe 0,3'ün üstünde. Ancak erken dönem tekrarı başarısız, Pearson IS'te zayıf ve global FDR geçilmiyor. Bu yüzden **ORTA**.

**C1b — madenci kompoziti (seçim yanlılığını azaltmak için).** z(e)'nin GDX, GDXJ, RING ve 7'li sepet üzerinden ortalaması; h=3; IS'te seçilen eşleme işaret.

| | Tam | IS | OOS |
|---|---|---|---|
| IC, NW t | 0,064 / 3,26 | 2,27 | 2,43 |
| Net Sharpe 5 bps | 0,40 | 0,47 | 0,38 |
| Demeaned Sharpe | 0,44 | — | 0,43 |
| Net Sharpe 10 bps | — | — | 0,19 |

- Yılların 8/10'unda aynı işaret.
- 2010–2016 spot: IC 0,003, t=0,13. **ORTA/DÜŞÜK.**

### C2 — Eğri dikleşmesi Δ5(10y−2y) → 1 gün (DÜŞÜK)

**Kural:** z = Δ5(nom10 − nom2) / std (t-1 22:00 UTC değerleri); pozisyon = clip(z/2, −1, 1); h=1.

| | Tam | IS | OOS |
|---|---|---|---|
| IC, NW t | 0,065 / 3,15 | 1,87 | 2,58 |
| Net Sharpe 5 bps | 0,59 | 0,52 | 0,65 |
| Demeaned Sharpe | 0,60 | — | 0,66 |
| Net Sharpe 10 bps | — | — | 0,47 |

- **Diğer kontroller:**
  - Sıra-tabanlı kısmi t: 2,96 (IS 1,21).
  - Yıl yıl: 7/10 aynı işaret.
  - Sonuçlar 2020, 2025 ve 2026'ya yoğunlaşıyor: +15,6 / +17,0 / +22,5%. 2019 ve 2023'te −8%.
- **2010–2016 spot'ta ters işaret:** IC −0,039 (t −1,6), backtest Sharpe −0,72 (t −1,93).
- IS t'si 2'nin altında, yani ilişki tam örneklemde bulundu.
- **Mekanizma:** Fed indirimlerinin fiyatlanması (boğa dikleşmesi, 2y'nin düşmesi) altına olumlu. Rejime bağlı; 2025–2026 indirim döngüsünde güçlü.

### C3 — DXY sapması, C penceresi → 1 gün (DÜŞÜK; çapraz varlık bilgisi değil)

- **Kural:** gap = β·r_DXY − r_XAU, [t-1 20:00 → t 15:00]; yön IS'ten: gap'in tersi.
- **IC:** −0,059, t=−2,62, IS −2,17, OOS −1,65; 7/9 yıl.
- **Çapraz varlık bilgisi yok.** Altının kendi C-penceresi getirisi kontrol edilince kısmi t=−0,72. Kural aslında altının kendi gece momentumunu ölçüyor.
- **Backtest:** OOS Sharpe 0,27, demeaned 0,23; 10 bps'te −0,04; devir 103/yıl.

### C4 — Reel faiz + dolar seviye modeli artığı → 1 gün (YOK)

- t=2,34, IS 1,62, OOS 1,70; kısmi t 0,76.
- OOS Sharpe 0,36 ama demeaned **0,06**: getiri drift'ten geliyor; uzun ağırlıklı pozisyon, maruziyet 0,59.

## 6. Çoklu test özeti

- **Kayıtlı test sayısı.** Toplam 1.213:
  - s1: 760 (IC 240, kısmi 240, büyük hareket 240, emilim 40)
  - s2: 144
  - s3: 229 (pencere 198, emilim 22, altın öz 9)
  - s4: 38
  - s5: 38
  - s6: 2
  - s7: 2
- **Birincil evren (1.071 test).**
  - Bonferroni eşiği p < 4,7e-5; geçen test yok.
  - BH en küçük q = 0,43 (GDXJ artığı h3).
  - `kayit_fdr.csv` içindeki global q (0,07–0,10), sağlamlık varyantlarının aynı hipotezi tekrar tekrar kaydetmesinden yapay olarak düşük. Bu sayıyı kanıt olarak kullanmayın.
- **Aile içi BH** (madenci-artık ailesi, 30 test): GDXJ h3 q=0,013, GDX h3 0,014, RING h3 0,015.

## 7. Negatif bulgular (test edildi, tutmadı)

1. **Dolar** (DXY, UUP) 1/5 günlük değişim → 1/3/5 gün: YOK. Δ5 h3/h5 IS'te t 2,5–2,75, OOS'ta −0,7/−0,85.
2. **ABD 10y nominal, 10y reel, başabaş, ^TNX** değişimleri: YOK (|t|<2). 2y Δ5 h1 t=−2,47 tam dönem, IS'te −1,10; DÜŞÜK.
3. **S&P 500, ES, Nasdaq, HYG, EEM, FXI, TUR:** YOK. Büyük düşüş olaylarında IS/OOS tutarsız.
4. **VIX, GVZ, MOVE** (log değişim ve büyük sıçrama): YOK. GVZ Δ5 h1 t=2,03, IS 0,51.
5. **Emtialar:**
   - Petrol (BZ, CL), bakır: YOK.
   - Gümüş, platin: YOK. Platin Δ5 IS'te −2,1/−2,2, OOS'ta ≈0.
   - Paladyum: YOK. Δ1 h3 t=2,12, IS'te 0,32.
6. **Tahvil ETF'leri ve kripto:** TLT, TIP, BTC: YOK.
7. **GLD fiyatı** (Δ1, Δ5): YOK. GLD hacim şoku (işaretsiz, işaretli, büyük olay): YOK.
8. **Altın/gümüş oranı** z-skoru (20/60/120/250) ve Δ1/Δ5: YOK.
9. **Reel faiz + dolar** seviye ve değişim modeli artığı (ABD ve 15:00 sürümleri; W 120/250/500): YOK. Drift ve momentum içeriyor; ortalamaya dönüş kanıtı yok.
10. **Saatlik pencereler:** ABD öğleden sonrası (A), 24 saat (B) ve gece (C) için ham ve sapma ölçüleri, 11 varlık × 3 pencere × 3 ufuk. Şans düzeyi; IS'te seçilenlerin yarısının işareti OOS'ta döndü.
11. **Madenci büyük artık olayları** (|z|>1,5, üst/alt %10): anlamlı değil. Yükseliş olaylarında pozitif eğilim var (h5 t≈1,4–2,2), düşüş olaylarında hiçbir şey yok.
12. **Madenci 5 günlük artık/oran** → 1/3/5 gün: zayıf, IS'te anlamsız.
13. **Eğri dikleşmesi** (C2): 2010–2016'da ters işaret; DÜŞÜK.
14. **Emilim:** ABD kapanışı sonrası 18 saatte dolar etkisi fiyatlanıyor. VİOP girişinden sonrasına bilgi kalmıyor.

## 8. Uygulama notu (C1)

- **Hesap saati.** Sinyal t-1 ABD kapanışından sonra (21:00 UTC) hesaplanabilir; VİOP girişine kadar 18 saat var.
- **Giriş ve maliyet.** Giriş t uzlaşması: 18:05–18:15 TSİ VWAP. Uzlaşma fiyatına yakın dolum için emir bu 10 dakikaya yayılmalı. 5 bps gidiş-dönüş varsayımı VİOP spread'i ve komisyonuna duyarlı. 10 bps'te OOS Sharpe 0,53'e, IS Sharpe −0,04'e düşüyor.
- **Neyi kazandığı.** Getirinin büyük kısmı uzun bacakta. Kısa bacak ham olarak ≈0, drift arındırınca pozitif. Yani kural, altın düşerken de pozitif katkı veriyor (2022: +4,4%; 2026: +8,0%), ancak mutlak getiri buy&hold'dan düşük.
- **Kullanım önerisi.** Bağımsız bir strateji olarak değil, mevcut altın pozisyonuna **zamanlama/eğim filtresi** olarak düşünülmeli. 2010–2016'da bu etki yoktu; kalıcı olduğu varsayılmamalı.

## 9. Dosyalar

- Betikler:
  - `s1_tek_degisken.py`
  - `s2_goreli_deger.py`
  - `s3_saatlik_pencere.py`
  - `s4_adaylar.py`
  - `s5_c1_tani.py`
  - `s6_ozet.py`
  - `s7_kural.py`
  - `a4_common.py`
  - `run_all.sh`
- Çıktılar:
  - `s1_tek_degisken.csv`
  - `s1_bilgi_zamani.csv`
  - `s2_goreli_deger.csv`
  - `s3_saatlik_pencere.csv`
  - `s4_adaylar.json`
  - `s4_pnl_*.parquet`
  - `s5_c1_tani.csv`
  - `s6_ozet.json`
  - `s7_kural.json`
  - `kayit_fdr.csv`
  - `kayit_fdr_birincil.csv`
  - `*_log.txt`
- Kayıt: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/registry/a4_abd_capraz.csv` (1.213 satır).
