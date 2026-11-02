# v_duyarlilik — Temizlik sürümü duyarlılığı (ll v3 → v4; ek olarak v1/v2)
Tarih: 02.11.2026 · Veri sonu: 30.10.2026 · Kod: `out/code_v_duyarlilik/` (d0…d5) · Tablo: `out/v_duyarlilik.csv` (953 satır; v1–v4 sütunları, `fark_v4_v3`, ajan raporundaki değer, etiket v3/v4)

## 0. Hüküm (özet tablo)

| # | Başlık | v3 → v4 | Değişen | Sonuç / güven etiketi |
|---|---|---|---|---|
| 1a | 47 hissenin XU100 betası | 46 hissede 3y/1y/OOS **aynı**. Tam dönem (2010+) ortalama \|Δβ\| 0,014, en çok 0,05. IS (2014–20) ortalama 0,024, en çok +0,13 (VESTL 0,98→1,11; TRMET 0,91→1,01; TRALT 0,77→0,87; BRSAN 0,89→0,96; DOAS 1,03→1,10) | Yalnız 2020 öncesi; **SASA hariç** | Değişmez (SASA için bkz. 5) |
| 1b | 10 çift (corr / kısmi corr / beta) | 8 çiftte corr/pc \|Δ\| ≤ 0,01 (beta ≤ 0,012). **EREGL–ISDMR:** corr 0,639→0,580, pc 0,446→0,394, pc IS 0,283→0,229, beta 0,614→0,505. **TRALT–GC=F:** pc IS 0,193→0,159, beta 0,588→0,612. Tüm çiftlerde 3y/1y aynı | 2020 öncesi gerçek %10,5–20 hareketleri | **10/10 etiket aynı** (mekanik kural: 9 YÜKSEK, EREGL–MT.AS ORTA) |
| 2 | XBANK–USDTRY kısmi corr (XU100 kontrollü) | v3 = v4: 2014–20 **−0,183**, 2021–26 **−0,148**, tam −0,161, son 1y −0,036. Tek tek bankalarda \|Δ\| ≤ 0,01 | v3→v4 değiştirmiyor. **v1 (FX kayması) değiştiriyor:** −0,030 / −0,048 | Etiket aynı. v1 ile çalışan biri ilişkiyi "yok" bulurdu |
| 3 | ES=F_{t−1} → 47 hisse gap / gün-içi (medyan corr) | Gap: IS 0,068→0,080 (Spearman 0,136→0,137), OOS 0,146→0,145. Gün-içi: IS −0,021→−0,021, OOS −0,014→−0,013 (Spearman ≈0). XU030 aynı | Pearson IS'te küçük artış (aykırı günler) | Değişmez: "açılışta fiyatlanır, gün-içi kalıntı yok" |
| 4 | \|gap\|>%1 fade, açılış girişi (brüt bps/işlem) | **IS portföy 28,0 (t 7,0) → 22,3 (t 5,3)**; IS hisse medyanı 12,4→9,6; IS'te t≥2 hisse 15→10. **OOS 16,5 (t 2,8) → 16,6 (t 2,8)**; OOS medyanı 17,8→17,8 | IS düşüyor, OOS sabit. v3'ün IS'i **sonuca koşullanma yanlılığı** taşıyordu (bkz. §4) | 47-portföy ORTA kalır. **OYAKC fade YÜKSEK→ORTA** (IS +47 (t 2,6) → +27 (t 1,4)). CIMSA aynı (IS +41, t 3,2) |
| 5 | SASA başlık rakamları | **Son 1y XU100 betası 0,28 → 1,29**, corr 0,23→0,58. 3y beta 0,77→1,17. HEKTS 1y corr 0,28→0,64. Saatlik veriyle bağımsız kontrol: beta 1,19, corr 0,52 (v4 doğru) | v3'te son 1y'nin %55'i (136/248 gün) **sıfır getiri** | SASA–HEKTS YÜKSEK, KMPUR/SMRTG ORTA etiketleri aynı. Ama v3 tabanlı SASA 1y/3y sayıları (beta, varyans payı, "en yerli hisse") **geçersiz** |

**Genel sonuç:** v4 temizliği iki yerde gerçek bir fark yaratıyor:
1. SASA'nın son 1–3 yılı (tek etkilenen hisse).
2. 2020-03-13 öncesi (IS) dönem: gap fade IS getirisi, EREGL–ISDMR ve birkaç illikit hisse.

2021+ (OOS) sonuçları, sabit kurlu (FX) bulgular ve uluslararası çiftlerin büyük kısmı v3 ile v4'te aynı. Yurt içi turun tüm çıktıları v3 ile üretilmiş (§1). Düzeltilmesi gereken etiketler: OYAKC gap fade ve hisse ajanının YKBNK–KCHOL çifti (§6). SASA'ya dair her 1y/3y ifade de yeniden yazılmalı.

## 1. Hangi çıktı hangi sürümle üretildi (kanıt)
- **Sürüm zamanları:** `ll_v1_backup.py` 01.11 14:32, `ll_v2_backup.py` 14:38, `ll_v3_backup.py` ve v4 `ll.py` 02.11 **12:01** UTC. Paneller (`panel_ret_bistcal`, `panel_decomp_bist`) 12:02'de v4 ile yeniden üretildi (`log_panel_v5`).
- **Yurt içi tur v3 ile üretildi.** Tüm `ry_*.md` / `f_y_*.csv` dosyaları 11:53–12:01 arasında yazıldı. v3 yeniden üretimim ajan rakamlarıyla birebir aynı:
  - gunici_y gap fade: 28,0 / 16,5 bps; medyan 12,4 / 17,8; likit 3,1; illikit 26,9.
  - hisse ajanının 138 senkron çiftinde kısmi korelasyon farkı her çiftte < 0,005.
  - SASA–HEKTS 0,474 / 0,643 / 0,547 / pc 0,301.
  - 1. tur rakamlarının çoğu da v3 ile aynı: TUPRS–CRAK, TRALT–GC=F, TCELL–TKC, SAHOL–AKBNK; SASA–BZ=F 1y −0,154.
- **Kodun içine eski kuralı gömen betikler.** Bunlar v4 `ll.py` ile yeniden çalıştırılsa bile v3 gibi davranır:
  - `code_y_gunici_y/c_common.py:118`: h1 paneli `v>0` filtresi.
  - `code_y_akis/c_calendar.py:48` ve `d_index.py:10`: `ll.LIM_UP/LIM_DN`, yani her tarihte simetrik ±%10,5.
  - `code_olay/olib.py`: kendi v3 kuralları.
  - 18 doğrulayıcı kod dizini (`code_v_A4_a`, `code_v_K1_a`, `code_v_M4_a`, `code_v_H45_a` …): sabit ±%10,5 ve çoğu `v>0`.
  - Bu çıktıların 2014–2020 ve SASA kısımları aşağıdaki duyarlılığa tabi.

## 2. v3→v4 hangi günleri değiştiriyor (d0_diag, d3_limits)
- **Bayat gün kuralı (hacim 0 VE h==l).**
  - Son 1 yılda yalnız **SASA** etkileniyor: 129 gün; 3 yılda 151.
  - SASA'daki hacim boşluğu 2025-08'de başlıyor, brifingdeki 2025-06 değil. Aylık dağılım: 2025-08'de 7 gün, 2026-02'de 15, 2026-09'da 18.
  - Diğer hisselerde hacim0 & h≠l günü 2008/2010'da birkaç tane (ARCLK, PETKM, SISE, TSKB) ve tek tük.
  - XU030/XBANK'ta 2000–2009'un **tamamı** hacim0. v3 bu yılları siliyordu (seriler 2010'da başlıyordu), v4 tutuyor. 2010+ analizleri bundan etkilenmiyor.
- **SASA'nın hacim0 günleri gerçek işlem günü.**
  - Günlük h/l saatlik uçlarla %98 / %94 eşleşiyor; normal günlerde oran %97 / %96.
  - Günlük açılış m5 açılış müzayedesi fiyatıyla %100 aynı (32 gün).
  - Saatlik hacim bu günlerin tamamında > 0.
  - Yani v3 bu günleri atarak hatalı davranıyordu; v4 doğru.
- **Rejime bağlı eşik.**
  - 2020-03-13 öncesinde %10,5–20,5 bandında 1.331 hisse-günü var; 239'u 2014–2020'de (TRMET 36, VESTL 21, SASA 20, TRALT 20, ISDMR 15, DOHOL 14, ODAS 12, DOAS 11, BRSAN 10).
  - Veri bu rejimi doğruluyor (tüm BIST hisseleri, ham kapanış): 2016H1–2020-03-12 arasında her yarıyılda %19,5–20,5'te 20–68 limit kümelenmesi var; 2020-03-13'ten sonra 0.
  - 2008–2015'te %10'da duvar yok; yarıyılda 43–441 adet %10,5–19,5 hareket var. v3 bu dönemde gerçek hareketleri siliyordu.
- **v4'ün kalıntı riskleri:**
  - (a) 2020 öncesi %10–20 bedelsizler (−%9…−%17) yakalanmıyor. "Piyasa sakin + hareketin tamamı gap" sezgisiyle 2010–2020'de 47 hissede yaklaşık 17 şüpheli gün var (BRSAN 2010–12'de 4 gün, MGROS 2011-04-14 −%20,9, DOHOL 2012-04-12, ULKER 2012-06-06, TKFEN 2013-08-23, ALARK 2013-12-18, ODAS 2019-11-07). Koza günleri (2015-09-01, 2015-10-27) gerçek haber. Etkileri küçük.
  - (b) 2020 öncesi uç açılış müzayedesi fiyatları artık tutuluyor (bkz. §4).
  - (c) `bist_cal()` hâlâ XU100 `v>0` kullanıyor. 2019-04-19 (gerçek işlem günü) iki sürümde de takvimden düşüyor; ihmal edilebilir.

## 3. Madde madde sonuçlar (v3 / v4)

### (1) XU100 betası (seçmeler; 47 hissenin tamamı CSV'de, `1_beta_XU100`)
| Hisse | Tam 2010+ | IS 2014–20 | 3y | 1y |
|---|---|---|---|---|
| SASA | 0,867 / 0,972 | 0,787 / 0,852 | 0,765 / **1,168** | 0,275 / **1,289** |
| VESTL | 0,970 / 1,021 | 0,979 / 1,105 | 1,097 / 1,097 | 0,967 / 0,967 |
| TRMET | 0,971 / 1,018 | 0,908 / 1,013 | aynı | aynı |
| TRALT | 0,860 / 0,897 | 0,773 / 0,871 | aynı | aynı |
| Diğer 43 | \|Δ\| ≤ 0,045 (DOAS 0,043) | \|Δ\| ≤ 0,07 | aynı | aynı |

Çiftler, v3 / v4. Tam dönem 2010+; pc = XU100 kontrollü kısmi korelasyon:

| Çift | corr tam | corr 3y | corr 1y | pc tam | pc IS | pc OOS | beta | etiket |
|---|---|---|---|---|---|---|---|---|
| THYAO–LHA.DE | 0,310/0,316 | 0,303 | 0,424 | 0,180/0,184 | 0,183/0,188 | 0,241 | 0,322/0,333 | YÜKSEK = |
| PGSUS–EZJ.L | 0,255/0,259 | 0,218 | 0,303 | 0,169/0,169 | 0,159/0,157 | 0,206 | 0,256/0,262 | YÜKSEK = |
| TUPRS–CRAK | 0,300 | 0,284 | 0,342 | 0,172 | 0,145 | 0,221 | 0,480 | YÜKSEK = |
| TUPRS–BZ=F | 0,166 | 0,222 | 0,341 | 0,158 | 0,101 | 0,258 | 0,157 | YÜKSEK = |
| TRALT–GC=F | 0,218/0,217 | 0,270 | 0,413 | 0,214/0,209 | **0,193/0,159** | 0,191 | 0,588/0,612 | YÜKSEK = |
| EREGL–MT.AS | 0,283 | 0,223 | 0,187 | 0,118 | 0,109 | 0,140 | 0,230 | ORTA = |
| TCELL–TKC | 0,739/0,740 | 0,836 | 0,890 | 0,610/0,609 | 0,618/0,616 | 0,621 | 0,690/0,693 | YÜKSEK = |
| AEFES–CCOLA | 0,406/0,414 | 0,521 | 0,498 | 0,222/0,223 | 0,200/0,205 | 0,264 | 0,405/0,417 | YÜKSEK = |
| SAHOL–AKBNK | 0,707/0,708 | 0,727 | 0,794 | 0,238/0,237 | 0,245 | 0,342 | 0,623/0,625 | YÜKSEK = |
| EREGL–ISDMR | **0,639/0,580** | 0,722 | 0,647 | **0,446/0,394** | **0,283/0,229** | 0,578 | **0,614/0,505** | YÜKSEK = |

- **EREGL–ISDMR'deki düşüşün kaynağı:** ISDMR'nin 2016–2018'deki 15 gerçek tavan/taban günü (2016-03-29…04-01 arası art arda +%18; illikit spekülatif ralli).
  - Sıra tabanlı (Spearman) kısmi korelasyon değişmiyor: 0,455 / 0,451. %1 winsorize ile 0,449 / 0,426.
  - Yani bağ ~0,45 düzeyinde. Pearson'daki düşüş birkaç uç günden geliyor.
  - TRALT–GC=F'de de aynı tablo: IS Spearman 0,193 / 0,187.

### (2) Bankalar–USDTRY (XU100 kontrollü kısmi korelasyon)
| | v1 | v2 | v3 | v4 |
|---|---|---|---|---|
| XBANK 2014–20 | −0,030 | −0,180 | −0,183 | −0,183 |
| XBANK 2021–26 | −0,048 | −0,148 | −0,148 | −0,148 |
| XBANK son 1y | −0,024 | −0,036 | −0,036 | −0,036 |

- 7 bankada v3→v4 farkı en çok 0,01 (GARAN IS −0,152→−0,160; YKBNK −0,130→−0,141).
- Banka ajanının raporu (−0,16; IS −0,18 / OOS −0,15) v2+ ile tutarlı.

### (3) ES=F_{t−1} → gap / gün-içi (47 hisse medyanı)
| | gap IS | gap OOS | gün-içi IS | gün-içi OOS |
|---|---|---|---|---|
| Pearson v3 / v4 | 0,068 / 0,080 | 0,146 / 0,145 | −0,021 / −0,021 | −0,014 / −0,013 |
| Spearman v3 / v4 | 0,136 / 0,137 | 0,150 / 0,150 | −0,004 / −0,003 | −0,001 / −0,000 |

- Pozitif gap korelasyonu payı IS %98, OOS %100; her iki sürümde aynı.
- Pearson ile Spearman arasındaki IS farkı uç gap günlerinden geliyor; bu sürümden bağımsız bir aykırı değer duyarlılığı.

### (4) Gap fade (|gap|>%1, açılış girişi E0, brüt bps/işlem)
| | IS v3 | IS v4 | OOS v3 | OOS v4 |
|---|---|---|---|---|
| Portföy 47 (t) | 28,0 (7,0) | **22,3 (5,3)** | 16,5 (2,8) | 16,6 (2,8) |
| Hisse medyanı | 12,4 | 9,6 | 17,8 | 17,8 |
| Likit 23 / illikit 24 | 12,9 / 33,2 | 10,7 / 26,3 | 3,1 / 26,9 | 3,5 / 26,9 |
| t≥2 hisse sayısı | 15 | 10 | 5 | 5 |
| 8 bps sonrası portföy | 20,0 | 14,3 | 8,5 | 8,6 |

- **IS farkının kaynağı (d2):** v4 IS'e 211 işlem ekliyor; bunların ortalaması −185 bps.
  - **154'ünde \|cc\|>%10,5.** Bunlar gap'in gün içinde sürdüğü günler; ortalama −755 bps.
  - v3 bu günleri cc'ye bakarak siliyordu. cc gün-içi sonucu içerdiği için bu **sonuca koşullanma (look-ahead seçim) yanlılığıdır**. 2014–20'de \|gap\|>%1 olup \|cc\|>%10,5 olan 203 günde fade ortalaması −470 bps; isabet oranı %19.
  - Ters yönde, 55 işlemlik bir grup var: uç gap'li ve gün içinde dönen şok/devre kesici günleri (2016-06-24, 2016-07-18, 2018-06-25, 2018-08-10, 2020-02-28). Ortalaması +881 bps. Açılış müzayedesinden dolum bu günlerde gerçekçi değil.
  - \|gap\|>%10,5 hariç tutulursa v4 IS portföyü 21,5 bps (t 5,1); hisse medyanı **4,5 bps**.
- **Yıllar:** 2016 40,7→24,0; 2019 36,9→22,5; 2015 5,5→0,3; 2021+ aynı (yalnız 2025, SASA nedeniyle 5,3→8,3). 13 yılın 11'inde pozitif (2015 sıfıra yakın).
- **Hisseler (IS):**
  - OYAKC 47,5 (t 2,64) → 26,7 (t 1,37). Fark 4 gerçek gün-içi devam gününden geliyor: 2016-02-04, 2016-09-05, 2019-10-07, 2019-10-08; −700…−1.700 bps.
  - TRMET 38,6 (2,6) → 17,0 (1,0); VESTL 30,1 (2,3) → 14,9 (0,9).
  - CIMSA 38,0 (3,5) → 41,0 (3,2).
  - Hiçbir hissede OOS değişmiyor; SASA hariç.
- **Gerçekçi giriş (h1, 2023-12+; açılış gürültüsü / bid-ask ayrıştırması):**
  - E0 açılış 24,2→24,5.
  - E2 (ilk saat barı (h+l+c)/3) 20,5→20,9.
  - E3 (10:30 TSİ fiyatı) 15,4→15,9.
  - Sürümden bağımsız. Etkinin ~%35'i açılış fiyatının kendisinde.
  - Uyarı: HEKTS'in 2024-09 h1 fiyatları bölünmeye göre düzeltilmemiş (~2,78 kat). \|O→07:30\|>%12 filtresi olmadan E2 portföyü yanlışlıkla 42 bps çıkıyor.
- **v1/v2 notu:** v2→v3 (taban günlerinin korunması) OOS portföyü 19,5'ten 16,5'e indirmişti. v1/v2 ile çalışan bir rapor OOS'u ~3 bps şişik verir.

### (5) SASA
| Metrik | v3 | v4 | Not |
|---|---|---|---|
| Son 1y sıfır getiri günü (ll.ret) | 136/248 (%55) | 12/251 | 2021+ payı %12,2 → %2,3 (ag ajanının "SASA %12" değeri v3 artefaktı) |
| 1y yıllık oynaklık | %29,6 | %53,6 | |
| XU100 betası tam / 3y / 1y | 0,87 / 0,77 / 0,28 | 0,97 / 1,17 / **1,29** | h1 kontrolü: 1y 1,19; 2023-12+ 1,17 |
| XU100 corr 1y | 0,23 | 0,58 | h1: 0,52 |
| XU100 R² 1y (ret / decomp-cc yolu) | 0,051 / 0,167 | 0,338 / 0,339 | ag ajanı varyans payı 1y 0,017 (v3) |
| Küresel-8 (t, t−1) düz. R² 1y / 2024–26 | 0,006 / 0,025 | 0,029 / 0,026 | 2024–26 "en yerli hisse" sonucu ayakta; 1y değeri değil |
| corr 1y: HEKTS / KMPUR / SMRTG | 0,28 / 0,24 / 0,12 | 0,64 / 0,43 / 0,35 | decomp-cc yolu (hisse ajanı): 0,547→0,642; 0,406→0,431; 0,207→0,348 |
| pc 1y: HEKTS | 0,19 | 0,45 | pc tam (2014+, decomp-cc) 0,301→0,288: YÜKSEK aynı |
| corr 1y: PETKM / AKSA / KORDS | 0,09 / 0,12 / 0,21 | 0,36 / 0,42 / 0,22 | KORDS pc 1y 0,13→−0,04 |
| corr 1y: BZ=F / CL=F / IVL.BK / 1326.TW / CT=F | −0,154 / −0,117 / −0,012 / −0,075 / 0,109 | −0,131 / −0,126 / 0,122 / 0,009 / 0,188 | 1. tur değerleri v3 ile birebir; tam dönem rakamlarında değişim ≤0,02, etiketler (DÜŞÜK / ÇOK DÜŞÜK) aynı |
| ES=F_{t−1} → gap IS / OOS | 0,069 / 0,154 | 0,098 / 0,143 | gün-içi ≈0 (aynı) |
| Kendi gap fade'i IS / OOS (bps) | +20,3 / −1,7 | +12,0 / −16,2 | h1 E2: +19,6 → −14,5 (işaret dönüyor; t<1) |

- SASA etkisi kullanılan yola bağlı:
  - `ll.ret` yolu (`summarize_pair`, 12:02 öncesi panel): v3 hacim0 günlerini **0 getiri** yapıp ertesi güne yığıyordu. Etki en ağır bu yolda.
  - `ll.decomp` yolu (hisse ajanı): bu günler NaN oluyordu; son 1y'de yalnız 119 gün kalıyordu.

## 4. Doğrulayıcı yorumu: hangisi doğru?
- **v4 daha doğru:**
  - SASA günleri saatlik ve 5 dakikalık veriyle gerçek işlem günü olarak doğrulandı (§2).
  - 2020 öncesi %10,5–20 hareketleri ±%20 marj rejiminde gerçek hareketler; limit kümelenmesi veride görülüyor.
  - v3'ün cc filtresi gap fade backtestinde sonuca koşullanma yanlılığı üretiyordu.
- **v4'ün de iki zayıflığı var:**
  - (i) 2020 öncesi küçük bedelsizleri yakalamıyor (az sayıda; §2).
  - (ii) Uç açılış müzayedesi günlerini tutuyor. Bu fiyatlar gerçek ama işlem için erişilemez (devre kesici). İşlem testlerinde \|gap\|>%10,5 ayrıca dışlanmalı.

## 5. Sınırlamalar
- "Mekanik etiket", brifingdeki ölçütün kural tabanlı yaklaşık bir uygulaması. Mekanizma yargısı içermiyor; ajanların kendi etiket kuralları biraz farklı olabilir.
- Pair taraması yalnız hisse ajanının 138 senkron çiftini kapsıyor. Öncülük (lead) testleri ve ağ (DY/Shapley) analizleri yeniden çalıştırılmadı. ag ajanının "alıcı: SASA" ve 1y paylarındaki SASA değerleri v3 artefaktı olabilir; 2024–26 küresel payı (≈%2,6) iki sürümde aynı.
- Kurumsal işlem takvimi (KAP) olmadığı için 2020 öncesi bedelsiz kalıntısı yalnız sezgisel olarak tahmin edildi.

## 6. Etiket değişiklikleri listesi (koordinatöre)
1. **OYAKC gap fade: YÜKSEK → ORTA.** IS v4'te anlamlı değil (t 1,37). OOS +50 (t 2,7) aynı. CIMSA YÜKSEK kalır.
2. **47-hisse gap fade:** ORTA kalır. Rapordaki IS rakamı 28,0'dan **22,3 (t 5,3)** olarak düzeltilmeli; IS medyanı 9,6 (uç gap'ler hariç 4,5). OOS aynı.
3. **YKBNK–KCHOL (f_y_hisse):** pc 0,152 → 0,136. Ajanın kendi kuralıyla (pc ≥ 0,15) YÜKSEK → ORTA.
   - 138 çiftin geri kalanında etiketi değiştiren fark yok. Medyan \|Δpc\| 0,003; IS'te en çok 0,069.
   - IS'te 0,15 eşiğini geçen çiftler: MGROS–AGHOL, ODAS–ZOREN, CLEBI–TAVHL, HEKTS–BAGFS (IS pc 0,15 altına iniyor), AGHOL–AEFES, PETKM–AYGAZ, DOAS–TOASO (çıkıyor). ISDMR–KRDMD tam pc 0,335→0,283.
4. **SASA:** 1y ve 3y'ye dayanan her ifade v4 ile yeniden yazılmalı: XU100 betası ≈1,2–1,3, 1y corr 0,52–0,58, akran korelasyonları yaklaşık 2 kat. Tam dönem etiketleri aynı kalıyor.
5. **v1 ile üretilmiş FX bulgusu varsa:** banka–USDTRY gibi ilişkiler ~0 görünür ve etiket yanlış olur. v2+ ile yeniden hesaplanmalı (banka ajanı zaten v2+).
