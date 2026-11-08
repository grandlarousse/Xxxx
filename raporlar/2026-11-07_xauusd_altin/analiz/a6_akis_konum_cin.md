# a6 — Konumlanma, akış, Asya/Çin → VİOP Ons Altın (F_XAUUSD) 1/3/5 gün lead-lag

Ajan anahtarı: `a6_akis_konum_cin`. Çalışma dizini: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a6_akis_konum_cin/`.
Tam yeniden üretim: `python3 run_all.py`. Bu betik kayıt dosyasını sıfırlar ve a→i betiklerini sırayla çalıştırır (~40 sn). Otomatik tablo eki: `tablolar.md`.

## 1. Kısa sonuç

- **Kayıtlı test sayısı 542** (`out/registry/a6_akis_konum_cin.csv`). Bunların **220'si birincil test**: 55 öngörücü × h ∈ {1,3,5,10}. Kalanlar sağlamlık, 2010–2016 erken dönem, aynı gün ve kural varyantları.
- Birincil testlerin 27'sinde |t| ≥ 2 çıktı. Yalnız şansla ≈10 beklenirdi, ama testler birbirine bağımlı (aynı sinyal farklı ufuklarda). Yerel BH-FDR'de en küçük q ≈ 0,17, yani **%10 FDR'de anlamlı tek bir bulgu yok.**
- **En iyi aday (ORTA): Çin altın hisselerinin artık getirisi.** 600547.SS, 1818.HK ve 2899.HK'nin altın ve yerel endeks betası çıkarılmış günlük getirilerinin ortalaması, sonraki 3–5 günün VİOP getirisini pozitif öngörüyor.
  - h=5: IC 0,065, t_tam 2,83, t_IS 0,37, t_OOS 3,40, 9 yılın 8'inde aynı işaret.
  - İşaret kuralı (h=5, kademeli, net 5 bps): OOS Sharpe 1,41, drift çıkarılmış 1,40. 10 bps stres altında 1,27. Aynı OOS'ta buy & hold Sharpe'ı 0,53.
  - **Ancak IS'te (2018–2021) kural Sharpe'ı −0,27 ve 2010–2016 spot tekrarında etki yok (t 0,45).** Etki büyük ölçüde 2022 sonrasına, yani Çin kaynaklı altın talebi dönemine ait.
- DÜŞÜK güvenli, istikrarsız adaylar:
  - Hang Seng gün t getirisi (h=1/3 pozitif). 2010–2016'da h=1'de ters işaretli.
  - VİOP OI 5g değişimi × 5g getiri işareti (negatif). IS'te güçlü, OOS'ta zayıf, spot getiri kontrolüyle kayboluyor.
  - GPR 250g z (negatif). Yayın zamanlaması belirsiz.
- **YOK:**
  - CFTC COT: seviye, z, akış, uç kural, swap ve üretici. Kapanma dönemleri dahil de olsa, hariç de olsa sonuç aynı.
  - SHFE AU0 ve 518880.SS Şanghay primi: seviye, değişim, z, hacim.
  - SHFE AG0 gümüş primi: ham t −2,5, ama spot getiri kontrolüyle t −0,33.
  - Diğer Asya endeksleri, spot Asya seansı getirisi, GPR şokları, VİOP OI ve hacim şokları, gram altın OI ("yerli kalabalık").
- **Veri hatası (diğer ajanlar için kritik):** `panel_viop/panel_spot` içindeki `gpr_*` sütunları **sabit** (97,67), çünkü panel kurucudaki tarih dönüşümü bozuk. Bu çalışmada GPR ham dosyadan yeniden kuruldu (`d_gpr.py`).

## 2. Veri, bilgi zamanı (UTC) ve ileriye bakma kontrolü

| Öngörücü | Kaynak | Bilgi zamanı (gün t) | 15:00 UTC'ye pay |
|---|---|---|---|
| CFTC COT (Salı pozisyonu) | ham CFTC zip, `cot_gold_reportdate` as-of | Cuma 19:30/20:30 UTC yayın → Pazartesi kullanımı | ≥ 2,5 gün |
| SHFE AU0/AG0 gündüz kapanışı | Sina (`data/misc/sina_*.txt`) | 15:00 CST = 07:00 UTC | 8 saat |
| Spot XAU/XAG, USDCNH | Dukascopy saatlik, 07:00 UTC | 07:00 UTC | 8 saat |
| 518880.SS, 600547.SS, 000001.SS | Yahoo, SHH kapanışı | 07:00 UTC | 8 saat (`c_avail_check.csv`: min 8,0 sa) |
| 1818.HK, 2899.HK, ^HSI | Yahoo, HKEX | 08:10 UTC | 6,8 saat |
| ^N225, ^KS11, ^AXJO | Yahoo | 05:10–06:30 UTC | ≥ 8,5 saat |
| GPR günlük | `data/misc/gpr_daily.xls` | D ≤ t−2 (D+1 23:00 UTC varsayımı) | belirsiz → DÜŞÜK |
| VİOP OI/hacim (XAUUSD, XAUTRYM) | `viop_long.parquet` | **t−1 bülteni** (gün t'nin OI/hacmi 15:15 UTC sonrası kesinleşir) | ~23 saat |

- **Aynı gün VİOP sürümleri** (`*_sameday`, 24 test) "kapanışta/kapanış sonrası hesaplanan, uygulanamaz" diye işaretlendi. Hiçbiri t−1 sürümünden daha iyi değil.
- **Yahoo tarih hizası doğrulandı.** 600547.SS ile SHFE AU0 aynı gün getiri korelasyonu 0,59; t+1 ile 0,04, t−1 ile −0,004. 1818.HK için 0,55 / 0,06 / −0,03. Bir günlük kayma yok.
- **Placebo** (`f_deep_placebo.csv`): Ana adayda x'i 1 gün eskitince IC 0,063 (h=5), 2 gün eskitince 0,017. Gelecek bilgisi (−1) eklenince IC 0,088'e çıkıyor; pencere örtüştüğü için bu beklenen bir sonuç. Sızıntı izi yok. Sızıntı olsaydı etki h=1'de yoğunlaşırdı, ama h=1'de IC yalnızca 0,017.
- **SHFE AU0 roll temizliği.** Sina AU0 ana kontrat değiştiğinde fiyat carry kadar sıçrıyor (50–165 bps). İki kural kullanıldı:
  - Sina OI sütununda |Δlog OI| > log 1,25 (53 gün).
  - Roll aylarında (4, 5, 10, 11, 12) ≥ 60 bps'lik pozitif ve kalıcı basamak (15 gün). Örnekler: 2016-05-04, 2016-11-09, 2017-05-02, 2017-11-10, 2018-05-03, 2018-11-08, 2019-05-13, 2020-05-18.
  - Bu günlerde Δprem = 0 alındı. Kontrat değişimi gerçek zamanlı kamuya açık bir bilgi; basamağın kalıcılığı yalnız roll gününü etiketlemek için kullanıldı.
  - Roll'dan bağımsız kontrol olarak 518880.SS (SGE Au99.99 izleyen ETF) primi kullanıldı. İki seri arasında Δprem korelasyonu 0,42.
- **USDCNH.** Dukascopy 07:00 UTC (2016+). 2010–2015 erken tekrarında Yahoo CNY=X'in t−1 kapanışı kullanıldı. Bu, yönetilen kur nedeniyle küçük bir hatadır ve yalnız erken dönemi etkiler.
- **COT kapanma dönemleri** (2018-12-21..2019-03-08 ve 2025-10-01..2026-01-23) ana sürümde NaN. "Kapanma dahil" ve "yalnız rapor sonrası ilk gün" sürümleri ayrıca verildi (`a_cot_robust.csv`). Sonuç değişmiyor.
- **Sıfır hacimli VİOP günü yok** (v_volume min 600). 61 roll günü var (`v_code` değişimi). Roll ±1 gün ve uç dönemler (Mart–Nisan 2020, Ocak–Şubat 2026) dışlanarak bütün adaylar yeniden test edildi.

## 3. Yöntem

- **Hedef:** `fwd{h}` = VİOP aktif kontrat uzlaşmadan uzlaşmaya log getiri, t+1..t+h (h = 1, 3, 5; ek olarak 10).
- **IC:** Spearman. t istatistiği rank sonrası OLS'ten, Newey–West lag = max(h, 5). Kod: `lib_altin.split_stats`.
- **Örneklem:** IS 2017-03..2021-12, OOS 2022-01..2026-11, yıl yıl işaret. Erken tekrar spot panelde (`sfwd{h}`, 15:00→15:00 UTC) 2010–2016.
- **Kural yönü** yalnız IS IC işaretinden alındı. Kurallar:
  - (i) `sign`: pos = IS_işareti × sign(x). Parametresiz.
  - (ii) `tercile_IS`: IS'in 1/3 ve 2/3 kantillerinin dışında ±1, arada 0.
  - Uygulama kademeli (`backtest`, h alt portföy). Net 5 bps, stres 10 bps. Uzun ve kısa bacak ayrı. Drift çıkarılmış (demeaned) Sharpe ve buy & hold ayrıca raporlandı.
- **Kontrollü regresyon** (`f_deep.py`): fwd_h ~ z(x) + spot r(15→15, t) + spot r(5g) + spot r(07→15, t) + VİOP r(t−1). Çin hisseleri için ayrıca spot r(07→07). NW lag h.
- **Aday seçimi.** İlk taramada |t| ≥ 2 olan ve mekanizması olan sinyaller derin analize alındı. Bunların yanına karşı örnek olarak COT swap eklendi.

## 4. Aile sonuçları (birincil IC t-değerleri; tam tablo `tablolar.md`)

### (a) CFTC COT — YOK

| Öngörücü | t(h1) | t(h3) | t(h5) | t(h10) | t_IS(h5) | t_OOS(h5) | yıl(h5) | t 2010–16 (h5) |
|---|---|---|---|---|---|---|---|---|
| MM net/OI 52h z | −0,45 | −0,59 | −0,57 | −0,64 | −0,45 | −0,25 | 3/10 | −1,63 |
| MM net/OI 156h z | 0,84 | 0,59 | 0,72 | 0,54 | −0,56 | 1,29 | 5/10 | −0,98 |
| MM net haftalık Δ/OI z | −1,49 | −0,54 | −0,06 | −1,05 | 0,59 | −0,61 | 6/10 | 0,75 |
| MM 4h Δ z | −1,57 | −1,06 | −0,50 | −0,49 | −0,83 | 0,13 | 3/10 | −0,14 |
| MM long Δ z / MM short Δ z | −1,28 / 1,26 | −0,71 / 0,49 | −0,42 / −0,14 | −1,51 / −0,05 | | | | |
| swap net/OI z52 | 0,87 | 1,34 | 1,51 | 1,83 | −0,11 | 2,11 | 6/10 | 1,49 |
| üretici net/OI z52 | −1,27 | −1,40 | −1,76 | −1,84 | −0,34 | −2,15 | 6/10 | **+2,01** |
| OI Δ × sign(ΔMM) | 1,66 | 1,52 | 1,45 | 2,48 | 1,07 | 1,09 | 5/10 | −1,00 |
| gümüş MM net/OI z / Δ z | 0,08 / −0,14 | | −0,33 / 0,10 | | | | | |

- Literatür kuralı (r2 §3.9, 156h z > +2 kısa, z < −2 uzun, h=5): aktif günlerin %7,8'inde pozisyon var. LS net Sharpe tam −0,10, OOS −0,17; kısa bacak OOS −0,78. 52h z ±1,5 kuralı: LS −0,04.
- COT swap ve üretici yalnız OOS'ta |t| ≈ 2; IS ≈ 0 ve erken dönemde üretici ters işaretli. IS yönüyle kurulan kural OOS'ta Sharpe −0,83 kaybettiriyor. Klasik "yalnız OOS'ta görünen" tuzak.

### (b) Şanghay primi / SHFE / 518880 — YOK (AG0 için ham sonuç spot getirisinin yansıması)

| Öngörücü | t(h1) | t(h3) | t(h5) | t(h10) | t_IS(h5) | t_OOS(h5) | t 2010–16 (h5) |
|---|---|---|---|---|---|---|---|
| SHFE AU0 prim Δ1 (roll temiz) = SHFE 07→07 getirisi − spot 07→07 − CNH | 0,78 | 1,70 | 0,24 | −0,20 | −0,13 | 0,36 | 0,18 |
| SHFE AU0 prim Δ5 | −0,06 | −0,94 | −1,99 | −1,82 | −0,55 | −2,03 | 0,11 |
| SHFE AU0 prim − 20g ort. | −0,28 | −0,37 | −0,98 | −0,88 | −0,36 | −0,93 | 0,48 |
| SHFE AU0 prim z250 | −0,05 | 0,21 | 0,14 | 0,21 | 0,68 | −0,30 | 0,92 |
| SHFE AU0 getirisi (07→07) | 0,89 | 0,61 | −0,56 | 0,24 | −1,35 | 0,31 | −0,21 |
| SHFE AG0 gümüş prim Δ1 | **−2,50** | −1,80 | −1,75 | −2,43 | 0,61 | −2,68 | — |
| 518880.SS prim Δ1 | 1,35 | 1,69 | 0,10 | 0,66 | −0,58 | 0,67 | −0,97 |
| 518880.SS anormal hacim / × sign(getiri) | 0,48 / −1,10 | 0,80 / 0,31 | 0,66 / −0,24 | | | | |

- AG0 prim Δ1 (h=1) spot getiri kontrolleri eklenince t −2,50'den **−0,33**'e düşüyor (IS −0,65, OOS 0,07). Sinyal bağımsız değil, spot fiyat hareketinin yansıması. İşaret kuralı net Sharpe: tam 0,10, 10 bps'de OOS 0,08. Sonuç: YOK.
- Roll temizliği yapılmamış ham AU0 Δprem de sonuçsuz (h1 t 0,35).

### (c) Asya / Çin hisseleri — ana aday burada

| Öngörücü | t(h1) | t(h3) | t(h5) | t(h10) | t_IS(h5) | t_OOS(h5) | yıl(h5) | t 2010–16 (h5) |
|---|---|---|---|---|---|---|---|---|
| **Çin altın hisseleri artık bileşik** | 0,69 | 2,33 | **2,83** | 2,73 | 0,37 | 3,40 | 8/9 | 0,45 |
| 600547.SS artık | 0,61 | 2,31 | **3,02** | 2,99 | 0,86 | 3,08 | 8/9 | −0,15 |
| 1818.HK artık | 1,28 | 2,06 | 2,87 | 2,73 | 0,57 | 3,29 | 7/9 | 0,61 |
| 2899.HK artık (Zijin, bakır ağırlıklı) | −0,22 | 1,11 | 0,60 | 1,22 | −0,33 | 1,08 | 5/9 | −0,07 |
| 600547 / 1818 / 2899 ham getiri | 0,78 / 2,12 / 1,49 | 1,76 / 2,71 / 2,67 | 0,89 / 1,75 / 0,49 | | | | | |
| Hang Seng getiri | **2,48** | **3,06** | 1,44 | 0,91 | 1,20 | 1,03 | 6/10 | 0,97 (h1: **−2,22**) |
| Şanghay Bileşik | 1,65 | 1,59 | −0,50 | 0,05 | 0,03 | −0,70 | 6/10 | −0,46 |
| Nikkei | 0,88 | −0,50 | −1,74 | −2,16 | −1,10 | −1,37 | 7/10 | −0,10 |
| KOSPI / ASX200 / Asya bileşik | 0,31 / 0,41 / 1,58 | | −0,83 / 0,13 / −0,10 | | | | | |
| Spot Asya seansı 00→07 UTC | −0,05 | 1,29 | −0,05 | −0,53 | 0,11 | −0,12 | 6/10 | 0,99 |

### (d) GPR — DÜŞÜK / YOK

- GPR log seviye z250: t(h1, h3, h5, h10) = −1,87 / −2,05 / −2,16 / −2,43. IS −1,86, OOS −1,63 (h5); 2010–16'da −0,80.
- Şok, değişim, tehdit ve eylem alt endeksleri: |t| < 2 (h ≤ 5).
- Uç olay kuralı (GPR şoku > IS %95 → uzun; 95 gün): h=5'te ortalama +21,6 bps, t 0,74. Drift çıkarılınca +6,1 bps, t 0,21. Sonuç: YOK.
- Mekanizma "söylentide al, haberde sat" olabilir. Ancak GPR gerçek zamanlı yayın tarihi ve revizyonları bilinmiyor, bu yüzden DÜŞÜK.

### (e) VİOP yerel konumlanma (t−1) — DÜŞÜK / YOK

| Öngörücü | t(h1) | t(h3) | t(h5) | t(h10) | t_IS(h5) | t_OOS(h5) | yıl(h5) |
|---|---|---|---|---|---|---|---|
| OI Δ1 / Δ5 | −0,15 / −0,07 | −0,35 / 0,46 | 0,46 / 0,89 | 1,10 / 0,92 | | 1,19 / 1,41 | |
| OI Δ1 × sign(r1) | 0,76 | −0,95 | −0,60 | −0,20 | −0,87 | 0,02 | 6/10 |
| **OI Δ5 × sign(r5)** | −2,28 | −2,26 | **−2,77** | −1,70 | **−3,61** | −0,62 | 10/10 |
| OI seviye z250 | 1,82 | 1,28 | 1,12 | 0,79 | 1,22 | 0,78 | 4/9 |
| hacim şoku / × sign(r) | 0,15 / 1,18 | 0,18 / 1,37 | 0,38 / 0,65 | | | | |
| XAUTRYM OI Δ5 / hacim şoku | 0,15 / −0,22 | | 0,20 / 0,29 | | | | |
| XAUTRYM OI z250 ("yerli kalabalık") | −1,28 | −1,45 | −1,45 | −1,46 | **+0,62** | **−2,20** | 6/9 |
| XAUTRYM OI Δ5 × sign(gram r5) | 0,41 | 0,08 | −1,14 | −2,31 | −1,08 | −0,50 | 6/10 |
| log(XAUTRYM OI / XAUUSD OI) Δ5 | 0,10 | −0,77 | −1,14 | −0,78 | −0,16 | −1,48 | 6/10 |

- **OI Δ5 × sign(r5).** Fiyatla aynı yönde yeni pozisyon birikimi tersine dönüyor; OI düşerken oluşan hareket ise devam ediyor.
  - Spot getiri kontrolleri eklenince h=5 t'si −2,77'den −1,21'e, OOS t'si −0,09'a düşüyor. Etki büyük ölçüde kısa vadeli fiyat dönüşünün yansıması.
  - İşaret kuralı (h=5): IS Sharpe 1,33, OOS 0,38, OOS 10 bps'de 0,26. 2024–2025'te negatif. Sonuç: DÜŞÜK.
- **"Yerli kalabalık" (gram altın OI seviyesi):** İşaret IS ile OOS arasında değişiyor. Sonuç: YOK.

## 5. Ana aday ayrıntısı — Çin altın hisseleri artık getirisi (ORTA)

**Tanım.** Gün t'de (SSE 07:00 UTC, HKEX 08:10 UTC kapanışından sonra) her hisse için şu hesaplanır:
- e = r_hisse − b₀ − b₁·r_altın(aynı pencere) − b₂·r_yerel_endeks.
- Altın penceresi, hissenin önceki kapanış anından bu kapanış anına kadar Dukascopy spot.
- Endeks: 600547 için 000001.SS, HK hisseleri için ^HSI.
- Betalar 250 günlük kayan OLS'ten ve **yalnız t−1'e kadarki veriyle** tahmin ediliyor.
- Bileşik = 600547.SS, 1818.HK ve 2899.HK artıklarının ortalaması (en az 2 hisse).

**Kural.** pos_t = sign(bileşik_t). Giriş gün t VİOP uzlaşması (≈15:10 UTC), tutuş h=5 iş günü. Kademeli uygulama: her gün sermayenin 1/5'i. Sinyal yönü yılda ≈121 kez değişiyor; yıllık ciro ≈44.

**Mekanizma.** Çinli yatırımcılar altın hisselerini altın talebinin vekili olarak alıp satıyor. Hissenin altın ve yerel endeksin ötesindeki hareketi, yerli talep (PBoC alımları, perakende/sigorta talebi, ETF akımı) hakkında bilgiyi küresel fiyattan önce yansıtıyor olabilir. Destekleyen iki gözlem:
- Artık, gün t'nin 07→15 UTC spot hareketiyle aynı gün 0,10 korelasyonlu (işlem yapılamaz, ama yön tutarlı).
- 5 günlük birikimli artık h=1'i bile öngörüyor (t 3,35). Bu yavaş yayılan bir bilgiye işaret ediyor. Bu varyant sonuçlara bakıldıktan sonra seçildi (post-hoc):
  - h=1 işaret kuralı: net Sharpe tam 0,60, IS 0,06, OOS 0,97; OOS demeaned 0,97, 10 bps'de 0,82; sinyal değişimi ≈50/yıl.
  - 2010–2016 tekrarı: t −0,05. Etki yok.

| Ölçüt | h=3 | h=5 |
|---|---|---|
| IC (tam) / t | 0,055 / 2,33 | 0,065 / 2,83 |
| t_IS / t_OOS | 0,26 / 2,89 | 0,37 / 3,40 |
| Yıllar aynı işaret | 7/9 | 8/9 |
| Kontrollü NW t (tam / IS / OOS) | 2,18 / −0,60 / 2,99 | 3,10 / −0,19 / 3,91 |
| Roll ±1 ve uç dönem hariç t (tam / OOS) | 2,15 / 2,75 | 2,28 / 3,18 |
| Kural pos×fwd ortalaması (bps), t; drift çıkarılmış | 8,1, 1,81; 8,3 | 15,5, 2,90; 15,8 |
| Net 5 bps Sharpe tam / IS / OOS | 0,41 / −0,72 / 1,10 | 0,77 / −0,27 / 1,41 |
| OOS demeaned / 10 bps | 1,09 / 0,92 | 1,40 / 1,27 |
| Uzun bacak OOS (dm) / kısa bacak OOS (dm) | 1,09 (0,63) / 0,18 (0,56) | 1,14 (0,64) / 0,19 (0,60) |
| Buy & hold OOS Sharpe | 0,53 | 0,53 |
| Spot hedef (15:00→15:00) t / OOS t | 2,28 / 2,97 | 2,41 / 3,06 |
| OOS 2022–2025 (2026 hariç) IC, t | 0,080, 2,50 | 0,087, 2,58 |
| 2010–2016 spot tekrar t | 0,86 | 0,45 |

- **Yıllık net Sharpe** (h=5, işaret kuralı): 2018 −1,00 | 2019 1,17 | 2020 −0,78 | 2021 −0,36 | 2022 1,37 | 2023 0,33 | 2024 0,84 | 2025 1,55 | 2026 2,49.
- **Uç dönemler hariç OOS Sharpe 1,52.** Yani sonuç Ocak–Şubat 2026'dan gelmiyor.
- **Beşli dilim ortalaması fwd5 (bps).** OOS: Q1 −17,7, Q2 8,4, Q3 −16,4, Q4 32,9, Q5 76,7 (kuyrukta belirgin). IS: 6,0 / −4,3 / 35,9 / −7,4 / 26,7 (monoton değil).
- **Varyantlar** (`g_cn_variants.csv`): yalnız altın betası, 120/500g pencere, 3g/5g toplam. Hepsinde h=5 t 2,4–2,95, OOS t 2,85–3,5 ve IS t ≤ 1,04. Etki beta tanımına duyarlı değil, ama **her varyantta IS zayıf.**
- **Tek hisse 600547.SS h=5** mekanik YÜKSEK eşiklerini geçiyor: t_tam 3,02, IS ile OOS aynı işaret, OOS t 3,08, yılların 8/9'u aynı işaret, OOS net Sharpe 1,02 ve demeaned 1,07. Yine de ORTA'ya indirildi. Gerekçeler:
  - (i) 3 hisse + bileşik × 4 ufuk arasından seçilmiş bir sonuç.
  - (ii) IS t 0,86; kural IS Sharpe'ı 0,27.
  - (iii) 2010–2016'da etki yok (−0,15).
  - (iv) Yerel BH-FDR q = 0,17.
- **Etiket: ORTA.** Mekanizma var, |t_tam| ≥ 2 ve OOS aynı işaretli. Ama rejime bağlı: etki 2022 sonrasına, yani Çin'in fiyat belirleyici olduğu döneme özgü olabilir. Gerçek para riski almadan önce ileriye dönük (2026-11 sonrası) izleme önerilir.

## 6. Test edilip tutmayan hipotezler (NEGATİF bulgular)

1. **COT yönetilen para net/OI seviyesi** (52h, 156h z), kontraryen ve trend: t ≤ |0,9|, yıllar 3–5/10. Literatür kuralı (156h z ±2) LS net Sharpe −0,10. YOK.
2. **COT haftalık akış** (ΔMM, ΔMM long/short, 4 haftalık): YOK. "Yalnız rapor sonrası ilk gün" sürümü de YOK. Kapanma dönemleri dahil/hariç fark yok.
3. **COT swap/üretici net z52:** yalnız OOS'ta |t| ≈ 2; IS ~0, erken dönemde ters işaret. IS-yönlü kural OOS Sharpe −0,83. YOK.
4. **COT gümüş** (seviye, değişim) ve **OI Δ × sign(ΔMM)**: h ≤ 5'te |t| < 1,7; h=10'daki 2,48 erken dönemde ters işaretli (−1,00). YOK.
5. **SHFE AU0 Şanghay primi** (Δ1, Δ5, 20g sapma, z250, SHFE getirisi): h ≤ 5'te en iyi |t| 1,99 (Δ5, h5; IS −0,55, erken +0,11). YOK. Meader'in prim/iskonto rejim etkisi 1–5 gün ufkunda görülmedi.
6. **518880.SS** (SGE ETF) prim değişimi, sapma, anormal hacim, işaretli hacim (Çin ETF akış vekili): YOK. En iyi t 1,69.
7. **SHFE AG0 gümüş primi Δ1:** ham t −2,50, spot getiri kontrolüyle −0,33. YOK.
8. **Asya endeksleri:** Nikkei, KOSPI, ASX200, Şanghay Bileşik ve vol-ölçekli Asya bileşiği h ≤ 5'te |t| < 1,8. YOK. Hang Seng ayrı (DÜŞÜK).
9. **Spot altın Asya seansı getirisi (00→07 UTC):** YOK.
10. **Ham Çin altın hisse getirileri:** h=3'te t 1,8–2,7 ama IS işareti karışık; bilgi artıkta. 2899.HK artığı (Zijin, bakır ağırlıklı) YOK.
11. **GPR şoku** (MA30'a göre), günlük değişim, MA7/MA30, tehdit/eylem şokları ve uç olay uzun kuralı: YOK. z250 DÜŞÜK.
12. **VİOP XAUUSD OI** Δ1/Δ5, OI seviyesi, hacim şoku, işaretli hacim şoku: YOK.
13. **VİOP XAUTRYM** (gram altın) OI Δ5, hacim şoku, OI × trend, XAUTRYM/XAUUSD OI oranı, "yerli kalabalık" OI z250 (işaret değiştiriyor): YOK.
14. **Aynı gün (kapanış sonrası) VİOP OI/hacim sürümleri:** t−1 sürümünden daha iyi değil. Uygulanamaz zaten.
15. **Çin talebi bileşiği** (hisse artığı + 518880 prim Δ + SHFE prim Δ): h=3'te t 2,56 (IS 0,69, OOS 2,82), h=5'te 1,34. Artık bileşiğe bilgi eklemiyor, primler gürültü ekliyor. DÜŞÜK.

## 7. Çoklu test

- Toplam kayıt 542. Dağılım:

| Aile | Test |
|---|---|
| asia | 60 |
| asia_early | 59 |
| viop_pos | 48 |
| cot | 44 |
| cot_early | 44 |
| shfe | 44 |
| shfe_early | 36 |
| asia_robust | 35 |
| viop_pos_robust | 28 |
| cot_robust | 24 |
| gpr | 24 |
| gpr_early | 24 |
| viop_pos_sameday | 24 |
| asia_rule | 18 |
| gpr_rule | 10 |
| shfe_robust | 6 |
| cot_rule | 4 |
| viop_pos_rule | 4 |
| gpr_robust | 4 |
| shfe_rule | 2 |

- Birincil testler 220. Bunların 27'sinde |t| ≥ 2; bağımsızlık varsayımıyla ≈10 beklenirdi.
- En iyi p'ler: HSI h3 0,0022; 600547 artık h5 0,0026; 1818 artık h5 0,0041; bileşik artık h5 0,0046; OI×trend h5 0,0055. BH q ≈ 0,17–0,18.
- **Sonuç: bu ailede FDR %10'u geçen bulgu yok.** Ana aday "olası ama kanıtlanmamış". Kayıt dosyası `out/registry/a6_akis_konum_cin.csv`; q değerli kopyaları `registry_with_q.csv` ve `registry_primary_q.csv`.

## 8. Uyarılar

- **Panel GPR hatası:** `gpr_*` sütunları sabit. GPR kullanan her ajan ham dosyadan yeniden kurmalı (`d_gpr.py` içindeki `gpr_asof`).
- **SHFE roll etiketlemesinde** basamak kuralı ileriye bakan bir kalıcılık ölçüsü kullanıyor. Yalnız 15 günü etiketliyor ve kontrat değişimi gerçek zamanlı biliniyor. Etiketsiz ham sürüm de sonuçsuz.
- **COT:** CFTC 2026 sonunda haftada iki yayına geçiyor (r2). İleride bilgi zamanı değişir.
- **Çin hisseleri:** Yahoo adjclose temettü düzeltmeli. HK 08:10 UTC kapanışı spot 08:00 ile eşleştirildi (≤10 dk fark).

## 9. Kod ve çıktı dosyaları

- `common.py`: ortak test (`T`, `T_early`), backtest bacakları (`legs_table`), `rule_stats`, `snap_h`.
- `a_cot.py` → `a_cot_ic.csv`, `a_cot_robust.csv`, `a_cot_early.csv`, `a_cot_rules.csv`, `cot_weekly_features.csv`.
- `b_shfe.py` → `b_shfe_ic.csv`, `b_shfe_early.csv`, `b_shfe_robust.csv`, `b_shfe_au_prem.csv` (roll etiketli prim), `b_etf518880.csv`.
- `c_asia.py` → `c_asia_ic.csv`, `c_asia_early.csv`, `c_asia_features.csv`, `c_avail_check.csv`.
- `d_gpr.py` → `d_gpr_ic.csv`, `d_gpr_early.csv`, `d_gpr_rule.csv`.
- `e_viop_pos.py` → `e_viop_ic.csv`, `e_viop_ic_sameday.csv`, `e_viop_robust.csv`.
- `f_deep.py` → `f_deep_summary.csv`, `f_deep_backtests.csv`, `f_deep_yearly_sharpe.csv`, `f_deep_placebo.csv`.
- `g_cn_robust.py` → `g_cn_variants.csv`, `g_cn_quintiles.csv`, `g_cn_sum5_backtests.csv`.
- `h_fdr.py` (yerel BH-FDR), `i_tables.py` → `tablolar.md`, `run_all.py` (hepsi).
