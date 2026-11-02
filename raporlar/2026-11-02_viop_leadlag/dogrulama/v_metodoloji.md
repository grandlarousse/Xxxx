# v_metodoloji — Metodoloji şeytanın avukatı (sistemik hatalar)

Kod: `out/code_v_metodoloji/` (t01–t23, bağımsız yükleyici `vm.py`; **ll.py import edilmedi**, hizalama/temizlik ham parquet'ten yeniden yazıldı). Tüm testler `nice -n 10`.

## 0. Özet karar tablosu

| # | Sorun | Ciddiyet | Kanıt (test) | Etkilenen iddialar | Düzeltme |
|---|---|---|---|---|---|
| M1 | **FX_FIX 2010-09 öncesinde look-ahead üretiyor.** Yahoo `=X` günlük kapanışı 2010-09'a kadar gün SONU, sonra ldate 00:00 UTC. ll.daily tüm geçmişi 1 gün kaydırıyor (ortak panel de öyle). | **KRİTİK** (2005/2010 başlangıçlı FX analizleri için) | t16/t17: EURUSD~FXE aynı gün corr 2006–09: 0,94–0,96, önceki gün ≈0. 2011+ tersi (0,83–0,96). Geçiş ~22.09.2010. XU100 cc_t ~ TRY_fix_{t−1}: 2005–10 **−0,487**, 2011–26 **−0,021**. 2005+ tam dönem −0,173'ün ~%90'ı look-ahead. XBANK: −0,470 / −0,068. | FX sürücülü tüm lag-1 cc testleri ve 2005/2010 başlangıçlı tam dönem senkron/kısmi korelasyonlar (186 FX satırı n>3.800). Panel taramaları (r1_tarama 'tam' penceresi, USDTRY kontrollü pc_xt). gap/intra (2014+) ve IS/OOS etkilenmez. | `if FX_FIX and ldate>=2010-09-22: shift(-1)` (öncesine dokunma) ya da FX analizlerini 2011+ başlat. |
| M2 | **12σ filtresi gerçek şokları siliyor.** | **ORTA–KRİTİK** (TL kuru bulguları) | t05: 1.047 BIST-dışı sembolde 576 gün silinmiş (328 sembol). %86'sı ertesi gün geri dönmüyor (gerçek şok). TRY=X: **10.08.2018 (+%20,5), 20.12.2021 KKM (−%20,9), 07.06.2023 (+%6,0), 19.03.2025 İmamoğlu (+%3,5)**. EURTRY/GBPTRY aynı. BZ=F/CL=F 09.03.2020, CHF 15.01.2015, ES=F 05.02.2018, HG=F 31.07.2025 (−%25), SI=F 30.01.2026 (−%37,6). | t06: XBANK~TRY β −0,40 → −0,36. TRY_{t−1}→gün-içi: XU100 +0,030→+0,062, **TUPRS +0,008→+0,070**, FROTO +0,024→+0,058. AKBNK TRY_{t−1}→gap −0,166→−0,206. ENKAI–TRY intra t 3,3↔4,3 (v_H45_a ile aynı). Brifingin rejim günlerinin kendisi siliniyor. | Silme yerine: yalnız ertesi gün geri dönen sıçramaları sil (roll/hata). Sonuçları hem kırpılmış (winsorize %0,5) hem ham raporla. Etkisi tek güne bağlı bulguyu ORTA'dan yukarı etiketleme. |
| M3 | **Kış aylarında saatlik BIST'te son 30 dk + kapanış seansı YOK.** `snap_daily(BIST,'15:00')` kışın 14:30 fiyatını verir. | **ORTA** (kapanış/son saat analizleri) | t11 + ek: kış (Kas–Mar) 297/721 günde son bar 13:30 (14:30'da biter). Son bar–resmi kapanış farkı medyan 24–35 bp (yaz 7–15 bp). Kış günlerinin %12–18'inde günlük yüksek h1 maksimumunun üstünde. 15:00 kapanış seansı barı pratikte hiç yok. ABD nakit ETF/ADR'lerde (TUR, SPY, JETS, TKC, EEM) 15:00 UTC snap'i Ara–Şub'da %0, Kas'ta %3 → kışın NaN. | **ry_akis #14 (vade sonu kapanış seansı)** — bkz. M4. savunma 03_defense H=14 "lead" kışın 0 (snap 15:10 = snap 14:30). y_akis b2/b3 "15:15" kışın 14:30. ry_gunici_y bunu doğru ele almış (CA yalnız yaz). | Kış günlerini kapanış/son saat testlerinden çıkar ya da yalnız yaz günleriyle raporla. snap_daily'ye `max_age` parametresi (BIST için 15 dk). |
| M4 | ry_akis kapanış seansı hesabı (`auc = log(C / snap15:00)`) kış/yaz karışımı. | **ORTA** (tek iddia, ama sonuç tersine dönüyor) | t12 (47 hisse, 2023-11+): **Yaz (gerçek müzayede): |auc| 21,3 bps, ertesi cc eğimi −0,300. Kış (14:30→C): 46,8 bps, eğim +0,070.** Normal günler yaz: −0,314 / vade sonu yaz: −0,283. | "Vade sonu −0,37 vs normal 0,00" karşıtlığı **artefakt**. Geri dönüş her gün var (ry_gunici_y #10 ile tutarlı). Vade sonunda büyük olan yalnız |auc| (yaz 37,9 vs 20,5). | Yalnız yaz günleriyle yeniden hesapla. "Vade sonuna özgü geri dönüş" iddiasını kaldır. |
| M5 | **ll.py başlığındaki "Asya lag0 = BIST'e göre zaten önde" notu HK/SG/Hindistan/Körfez için yanlış.** Bu piyasalar BIST açılış müzayedesinden (06:55 UTC) SONRA kapanıyor. | **KRİTİK** (lag0→gün-içi aileleri) | t22: lag0→gün-içi 199 satır; kapanışı ölçülebilen 116'nın 75'inde sürücü 06:55 UTC'den sonra kapanıyor. HK 08:00–08:10, SSE/SZSE 07:00 (müzayededen 5 dk sonra), Suudi ~12:00, Hindistan ~10:00. **4 YÜKSEK (cin: TRALT~1787.HK, 2899.HK, 600547.SS; TRMET~2899.HK) + 3 ORTA** etkileniyor (v_C4C5_b 1787 için doğruladı). | cin lead_intra lag0 aileleri, r1_holding "Asya lag0→intra" ailesi, tarama `intra_l0`. | Kütüphane notunu düzelt. lag0 yalnız kapanışı ≤06:30 UTC olan piyasalarda (Tokyo, Seul, Tayvan, Avustralya). Diğerlerinde hedefi sürücü kapanışından sonra başlat (ör. 08:30 UTC→kapanış). |
| M6 | **ll sürüm kayması (v3→v4).** v4 12:01'de yazıldı. Tüm r1 (09:30–11:23) ve ry_ag/akis/grup/gunici_y/hisse (11:53–12:01) v3 ile çalıştı. y_endeks v4 ile yeniden koştu. | **ORTA** | t18: v3, 2020-03-13 öncesindeki gerçek ±%10,5–20,5 günleri siliyordu (47 hisse: 2008: 193, 2013: 62, 2015: 45, 2016: 35, 2018: 39 gün). Gap-fade IS (brüt, açılıştan): **OYAKC 47,5 → 26,7 bps**, SASA 20,6 → 12,2, HEKTS 4,1 → 9,9, CIMSA 37,9 → 40,9. v3 SASA'nın 2024+ günlerinin %21,5'ini (hacim=0) siliyordu. | IS (2014–2020) istatistikleri: gap-fade (r1_kimya #5, ry_gunici_y #6/#7). Uç günlü olay/rejim analizleri. Ajanlar arası karşılaştırmalar. | Kritik iddiaları v4 ile yeniden koştur. CSV'ye `ll_version` sütunu ekle. |
| M7 | **Tatil sonrası lag-1 penceresi yanlış** (BIST tatilinde ABD işlem görmüşse). | DÜŞÜK (muhafazakâr) | t03/t04: 2010+ BIST günlerinin %2,4'ü (100 gün) ABD'nin işlem gördüğü BIST tatilinden sonra geliyor (29'unda ≥2 ABD günü), +99 ertesi gün → yılda ~11,6 gün. Doğru pencereyle gap korelasyonu artıyor: ES→XU100 0,141→**0,155**, ^GSPC 0,162→0,176, ES→THYAO 0,096→0,114. Etkilenen günlerde 0,07 vs 0,25. Gün-içi değişmiyor. | Tüm lead_gap: büyüklük ~%10 eksik. Sahte pozitif yok. Senkron lag0'a tatil hareketi karışıyor. | Sinyal = P(son kapanış ≤ t−1 takvim günü) − P(son kapanış ≤ önceki BIST günü − 1). |
| M8 | Eksik FX barında `shift(-1)` look-ahead (2011+ dahil). | DÜŞÜK | t02: lag-1 FX sinyalinin BIST t açılışından sonra bittiği gün: TRY=X 15 (%0,27), EURTRY 13, EURUSD/GBPTRY/JPY 29, **RUB=X 121 (%2,2)**. | RUB/TRY lag-1 testleri (küçük etki; RUB'da dikkat). | Kaydırmadan sonra sonraki barın tarihi > t+1 (hafta sonu hariç) ise NaN. |
| M9 | `bist_cal()`: XU100 hacim filtresi + Yahoo eksikleri. | DÜŞÜK | t03: 25 XU100 barı v=0 diye atılmış (24'ü 2002–2008, 1'i 2019; o günlerde ≥20 VİOP hissesi işlem görmüş). 13 gerçek BIST günü Yahoo XU100'de yok (25 Aralık 2017–2020, 02.04.2021…). | 2014+ sonuçlara etkisi ihmal edilebilir. | Takvim = XU100 ∪ (≥20 hissenin işlem gördüğü gün). |
| M10 | `backtest()` maliyeti her aktif gün |pos|×maliyet. | DÜŞÜK (muhafazakâr), ama ajanlar arası tutarsız | t23: z-modunda look-ahead YOK (bilgisiz trend sinyali +1,3 bps, gürültü). Sürekli long'da ll 32.000 bps keser, |Δpos| tabanlı gerçek ≈4 bps. **Çağıran hatası riski:** ABD sinyali kaydırılmazsa XU030 gün-içi −1 bps brüt yerine **+18 bps brüt** (net +10,4) sahte kâr. | Kalıcı pozisyonlu (cc) stratejiler net getiriyi olduğundan kötü gösteriyor. y_grup yalnız pozisyon değişiminde maliyet alıyor → net bps'ler karşılaştırılamaz. | `cost_mode='turnover'` ekle. Sinyal zaman damgasını assert eden bir kontrol (sinyal_bitiş < pozisyon_giriş). |
| M11 | Saatlik/5 dk 'c' temettü düzeltmesiz. | DÜŞÜK–ORTA | t07: Yahoo adj doğru günde (gap_0 eğimi −0,92, t −34,7; t−1/t+1 ≈0). h1 döneminde 49 olay k>%2, 13 olay k>%5 (DOAS 24.04 %11,1 / 25.05 %12,7; TOASO, TUPRS, ULKER %5–8). | snap tabanlı günlük/gece getirileri (h1 'c'). Gece penceresi testlerinde −%5…−%15 sahte hareket. | Gece/çok günlü h1 getirisinde günlük adj/c oranıyla düzelt ya da ex-günlerini NaN yap. |
| M12 | Açılış fiyatı = müzayede fiyatı. "Kendi gap'i → gün-içi geri dönüş" kısmen mikroyapı. | ORTA (işlenebilirlik) | t23b (h1, 47 hisse medyanı): corr(gap, açılış→07:30) −0,045 (%74'ünde negatif); 07:30 sonrası ≈ −0,012. Fade brüt: açılıştan **15,6 bps → 07:30 girişte 7,9**. Hisse açılışları h1 ile %99,7 birebir (veri hatası değil). o==önceki c oranı 2014+ %15 (tik adımı). Endekslerde h1 ilk bar açılışı bozuk (%27,5'i önceki kapanış). | r1_kimya #5, ry_gunici_y #6–#8, K1 doğrulamaları. | Getirinin yarısı ilk 30 dk'da. İşlenebilirliği açılış seansı derinliğiyle sınırla, gecikmeli girişle raporla. |

Diğer veri notu (y_endeks bulgusu, burada teyit edildi): Yahoo'da XU030/XU100/XBANK/XUSIN dışındaki BIST endekslerinin (XHOLD, XLBNK…) günlük geçmişi **tek satır**. Bu endeksleri Yahoo panelinden kullanan r1 satırları boş (sahte değil, eksik).

## 1. Kütüphane (ll.py) satır satır

- **daily()**
  - FX_FIX (M1, M8). Yöntem: EURUSD/JPY günlük c, ldate 00:00 UTC h1 fiyatıyla getiri bazında 0,999 korelasyonlu (t01b). Yani 2011+ için düzeltme doğru.
  - ffill ile BIST takvimi (M7, M9).
  - Bayat filtresi: v4'te yalnız (v=0 & h==l). Makul.
- **ret()**
  - BIST ±%10,5 / 2020 öncesi ±%20,5: v4 doğru. 2020 sonrası taban günleri (ln0,9 = −0,1054) korunuyor. Sayımım (t18 ek) bu günleri yanlışlıkla aykırı saydı, düzeltildi.
  - 12σ (M2).
  - Not: BIST endekslerine de ±%10,5 uygulanıyor. Endeks ±%10'u aşamayacağı için zararsız.
- **decomp()**
  - gap = cc(adj) − intra, temettü gününde toplam getiri gap'idir; doğru (t07).
  - Bedelsiz: Yahoo meta 47 hissede **0 split olayı** veriyor. Bedelsiz etkisi adj içinde (SASA 29.05.2017: ham gap −%18, cc −%5,4) ya da düzeltilmeden kalıyor.
  - ±%10,5 filtresinden kaçan küçük (<%10) düzeltilmemiş bedelsiz kalıntısı otomatik ayrılamadı (t21: adayların çoğu 08.02.2023 durdurma günü gibi gerçek olay). Kalıntı risk: DÜŞÜK.
  - bad_open koşulu (h==l & o==önceki c) çok dar ama zararsız: o==önceki c günleri gerçek (h1 ile %100 tutarlı).
- **snap_daily()**
  - Bar sonu varsayımları m5 ile doğrulandı. BIST 06:30 barı 07:30'da, 14:30 barı 15:00'te bitiyor.
  - Eksik: kış saati (M3). 6 saatlik bayatlık eşiği BIST için çok gevşek (kışın 14:30 fiyatı 15:00 snap'i sayılıyor).
- **backtest()** (M10). z-modu temiz.
- **Başlık notu** (M5): "HK 08:00 UTC BIST'ten önce/başında" ifadesi yanlış. HK BIST sürekli işleminin 1. saatinin sonunda kapanır.

## 2. Ajanlar arası tutarsızlıklar (t10)

- **Senkron satırlar:** ≥2 ajanın raporladığı 223 çift var. Bunların 13'ünde corr farkı >0,10, 92'sinde güven etiketi farklı, 12'si aynı anda hem YÜKSEK hem DÜŞÜK.
  - Neden 1 — frekans/para birimi aynı `sync` etiketiyle karışıyor. Örnek: EREGL~SLX günlük TL 0,22–0,25, haftalık 0,42, **aylık USD 0,55 (n=226) → YÜKSEK**. TRALT~SI=F için 0,20 vs 0,44, KRDMD~HG=F için 0,15 vs 0,37.
  - ABD kapanışlı sürücülerde günlük senkron korelasyon eşzamansız kapanış yüzünden olduğundan düşük (lag0+lag1 Dimson toplamı gerekir). |corr|≥0,30 eşiği ABD/Avrupa sürücülerini Asya'ya göre sistematik olarak cezalandırıyor.
  - Neden 2 — mekanik içerme. AEFES/BIMAS/MGROS/SOKM/ULKER~XU030'u tuketim DÜŞÜK, y_endeks YÜKSEK etiketlemiş (ham R² vs hisse-hariç).
- **Öncülük satırları:** işaret çelişkisi yok (9 ortak çift). Ama t yöntemi farklı: XU030~ES=F lead_gap aynı corr (0,2394) ile tarama t=3,98, y_viop t=9,78 (HC0 / NW / HC1 / FM karışık).
- **Kapanış müzayedesi:** ry_akis ile ry_gunici_y çelişiyor. Neden M4.
- **Maliyet modeli:** ll |pos| günlük, y_grup |Δpos|. Net bps'ler aynı ölçekte değil.
- **Sürüm:** v3 ile v4 karışık (M6).
- **Düzeltme:** CSV'ye `freq`, `ccy`, `t_method`, `ll_version`, `sample_start` sütunları ekle. Etiketleme günlükte Dimson korelasyonuyla yapılmalı.

## 3. Çoklu test ve çatallanan yollar (t14)

- Raporlanan birincil test toplamı **≈1,12 milyon**. Dönem kırılımlarıyla (IS/OOS/3y/1y) ≈3–4 milyon korelasyon eder. Örnekler: r1_tarama ≈481 bin, ry_hisse ≈240 bin, ry_ag ≈82 bin, r1_banka ≈61 bin.
- Küresel Bonferroni eşiği (α=0,05): **|t| ≥ 5,47**. Bağımsız test sayısı ≈10–50 bin varsayılırsa eşik 4,6–4,9.
- Serbestlik dereceleri (tek çift için): lag 1–5 × cc/gap/intra × TL/USD × günlük/haftalık/aylık × 4 pencere × 3 kontrol seti × eşik (|z|>1, |gap|>%1/%2) × giriş zamanı (E0/E2/E3) × maliyet × likit/illikit × 12σ açık/kapalı × v3/v4. Bu kabaca 10⁴–10⁵ varyant demek. Aile içi BH bunu kapsamaz. OOS sonuçları spesifikasyon seçiminden sonra görüldüğü için tam anlamıyla "saklı" değil.
- **YÜKSEK/ORTA etiketli 2.536 satırın |t|≥5,47 geçişi:**

  | İlişki | Geçen / toplam |
  |---|---|
  | sync YÜKSEK | 429/555 |
  | lead_gap YÜKSEK | 88/140 |
  | variance_share YÜKSEK | 84/133 |
  | **lead_intra YÜKSEK** | **2/8** |
  | **lead_intra ORTA** | **0/46** |
  | lead_hourly ORTA | 4/30 |
  | granger YÜKSEK | 2/24 |

  İşlenebilir türde (lead_intra/hourly/5m/auction/multiday/event/flow) YÜKSEK/ORTA olup |t|<3 olan 52 satır var.
- **Buna rağmen ayakta kalanlar:**
  1. Yurt içi senkron kümeler ve hisse-hariç sektör faktörü (pc 0,4–0,76).
  2. ABD/küresel t−1 → BIST **gap** (t 6–25; işlenemez).
  3. Olumsuz bulgular: gün-içi/saatlik öncülük yok (yüz binlerce testte FDR ≈0, null düzeyinde replikasyon). Bunlar çoklu teste karşı en sağlam sonuçlar.
  4. y_viop baz anomalisi → vadeli gün-içi (t −7,3; IS −5,1 / OOS −5,4) ve çok günlük (t −11,5). İşlem kapasitesi düşük.
  5. y_akis tavan/taban olgu iddiaları (t 6–44). Dolum varsayımına duyarlı.
  6. Temettü ex-günü etkileri (t 6–7,5).
  7. Kendi gap'i fade portföyü (IS t 7,0 / OOS t 2,8). Ama M6 ve M12 nedeniyle IS şişik, yarısı ilk 30 dk'da.
- **Eşiğin altında kalan "işlenebilir" iddialar** ORTA'dan DÜŞÜK'e inmeli: Avrupa/ABD havayolu→gün-içi t 2,6–3,0; Çin/HK lag0 (M5); FMG.AX→EREGL/KRDMD t 2,2–4,4; HEKTS hacim t 2,0; SAHOL–AKBNK t 3,5 (OOS t 3,5 ön-kayıtlı tek test olarak makul, ORTA kalabilir).

## 4. Yapısal kırılmalar (t19)

- **Kur rejimi:**
  - USDTRY günlük oynaklığı: 2018'de 194 bp, 2021'de 233 bp; **2024'te 32, 2025'te 25, 2026'da 10 bp**. |r|<5 bp gün oranı 2025–26'da %38–43.
  - Yönetilen kurda TRY varyansı yok. TRY'li ilişkilerin OOS/1y'de çökmesi çürütme değil, ölçülemezlik.
  - corr_1y / corr_3y TRY satırları bilgi taşımaz. TRY bulguları rejim koşullu etiketlenmeli ("serbest kur dönemlerinde").
- **TL vs USD, rejim yılları:** XU100~EEM (Dimson) TL bazında 2021'de 0,11, 2023'te 0,04. Diğer yıllar 0,4–0,6, 2026'da 0,61 (fon krizi + küresel). OOS (2021–26) iki "kopuk" yıl içeriyor. IS/OOS büyüklük kıyasları bu yüzden yanıltıcı, işaret tutarlılığı daha anlamlı.
- **Uç günlere bağımlılık:**
  - En uç %1 gün kovaryansın %29–47'sini taşıyor (TUPRS~BZ %47).
  - Ama Spearman ≈ Pearson (ör. XU100~EEM 0,300 vs 0,318). 6 kriz penceresi (2018-08, 2021-12, 2023-06, 2020 COVID, 2025-03, 2026 Eyl–Eki) çıkarılınca korelasyonlar korunuyor. XBANK~TRY krizsiz daha da güçlü (−0,233 → −0,295).
  - Yani senkron korelasyonlar kriz artefaktı DEĞİL. Lead/gün-içi bulgularsa tek günlere duyarlı (M2).
- **Nominal TL / enflasyon:**
  - XU100 gap ortalaması 2014–2026 her yıl pozitif (10–30 bps/gün; 2026'da 4,1). Gün-içi 11/13 yıl negatif.
  - Spot gap'in pozitifliği büyük ölçüde TL taşıma maliyetini (faiz/enflasyon) yansıtıyor. Vadelide bu fiyatta: y_viop XU030 vadeli gece long yalnız +5 bps.
  - İşaret stratejilerinde sürüklenme payı küçük (sign(EEM_{t−1})→gap: 9,4 bps'in ~1 bps'i).
- **Fon krizi (Eyl–Eki 2026):** 1y penceresinin son 2 ayı. corr_1y değerleri (özellikle küçük/illikit hisse kümeleri) bu ayrışmadan etkilenir; 1y değerleri tek başına etiket gerekçesi olmamalı.

## 5. "İşlenemez ama gerçek" gap bulgularının pratik anlamı (t20 + ry_viop)

- **Akşam seansı ne görüyor?** XU030 spot gap'i ~ ES=F gece pencereleri (2024-06+, n=558):
  - Toplam R² 0,268.
  - Akşam seansı kapanışında (20:00 UTC = 23:00 TSİ) bilinen pencereler (W1 15–16 + W2 16–20 UTC) R² 0,065 açıklıyor. Bu, açıklanabilir kısmın yalnız **~%24**'ü (ABD yaz saatinde %22, kışta %42).
  - Betalar: W1 0,26, W2 0,29, seans sonrası W3 (20:00–06:30) 0,66.
  - Bilginin çoğu akşam seansı kapandıktan sonra geliyor (ABD'nin kışta son saati, ABD vadelilerinin gecesi, Asya).
  - ry_viop vadeli gece getirisinde akşam penceresi payını ~%44 buldu (farklı hedef). İkisi birlikte: akşam seansı gecenin bilgisinin **dörtte biri ile yarısı** arasını görüyor, kalanını göremiyor.
- **Kullanıcı için anlamı:**
  1. ABD lag-1 → gap ilişkisi alfa değil, **risk ve beklenti bilgisi**.
  2. Spot/SSF pozisyonunu 18:10'da taşıyan biri ABD seansının riskini yalnız endeks düzeyinde ve kısmen hedge edebilir: akşam seansında XU030/XLBNK vadelisi, 23:00'e kadar. Pay vadelilerinde ve USD/TRY'de akşam seansı yok → hisseye özgü risk hedge edilemez.
  3. Açılış müzayedesinde (09:40–09:55 TSİ) teorik açılış fiyatı yayımlandığı için ABD hareketi müzayedede zaten fiyatlanır. ABD kapanışına bakarak müzayedeye emir vermek bir kenar sağlamaz, yalnız beklenen açılışı tahmin edip limit fiyatı/stop seviyesini ayarlamaya yarar (icra kalitesi).
  4. Pay vadelisi 09:20–09:30 açılış seansında spot gap'inin β≈0,64'ünü zaten fiyatlıyor (ry_viop #8). Spot müzayede öncesi "erken giriş" de kenar vermiyor.
  5. Gün-içinde kalan tek aday, açılış müzayedesi aşırı tepkisinin geri dönüşü (kendi gap'i fade). Bunun yarısı ilk 30 dk'da ve açılış seansı derinliği sığ (ry_viop: açılış seansı hacmi toplamın onbinde 1–7'si).
- **Likidite bağlamı (t13):** brifingdeki "VİOP pay vadelilerinin çoğu illikit" ifadesi 2025-11..2026-10 için doğru değil. 47 SSF'nin tamamı her gün işlem görüyor. Medyan günlük değer AKBNK 4.028 mn TL … DOAS 69 mn TL, medyan işlem 1.870–47.970. Sorun gün geneli değil, açılış/kapanış müzayedesi derinliği.

## 6. Öncelikli düzeltme listesi (koordinatöre)

1. FX_FIX'i 2010-09-22'den itibaren uygula ve paneli yeniden üret. 2005/2010 başlangıçlı FX satırlarını yeniden hesapla (M1).
2. 12σ'yı "geri dönen sıçrama" kuralıyla değiştir. TRY bulgularını şoklu ve şoksuz raporla (M2).
3. lag0→gün-içi satırlarını sürücü kapanış saatine göre filtrele. cin'in 4 YÜKSEK satırını düşür (M5). ll başlık notunu düzelt.
4. ry_akis #14'ü yaz günleriyle yeniden hesapla (M4). Kış günlerini h1 kapanış analizlerinden çıkar (M3).
5. Kritik IS istatistiklerini (gap-fade) v4 ile tekrarla (M6).
6. CSV şemasına freq/ccy/t_method/ll_version/sample_start ekle. Güven etiketini küresel |t|≥5,5 (ya da OOS ön-kayıtlı tek test) ile ilişkilendir (§3).
