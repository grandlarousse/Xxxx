# BIST/VİOP net liste: neyi işle, neyi izle, neyden kaç (06.11 kapanışı → Pazartesi 9.11)

Profil: Karar BIST kapanışında (18:00–18:15 TSİ), VİOP'ta 1–3 gün kapanıştan kapanışa; gün içi ekran yok. Daha uzun swing'e açık.
Kaynak önceliği: doğrulama dosyaları > plan > araştırma raporu. Her sayı kaynağıyla verildi; "(hesap)" yazanlar benim hesabımdır.

Kısaltmalar:
- [PL] `2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md`; [RT] aynı klasördeki `risk_ve_boyut_tablosu.csv`; [KDC] `notlar/k_dis-suruculer_curut.md`; [KYC] `notlar/k_yurtici-takvim_curut.md`
- [RH-T] / [RH-K] / [RH-A]: `rehber/tuprs|koza|altin/REHBER_*.md`
- [PB] `uygulama/PLAN_BIST.md`; [SİN] `uygulama/tarama/bist_sinyal_20261106.md`; [VB] `dogrulama/v_bist.md`
- [LL] `2026-11-02_viop_leadlag/RAPOR.md`; [KART] `hisse_kartlari/<KOD>.md`; [TV] `tradingview_kodlari.csv`

Boy notasyonu: [RT] sütunu `kontrat_1mn_1pct_1sigma_3g`, yani 1 mn TL hesapta %1 risk (10 bin TL) = 3 günlük 1σ için kontrat sayısı (03.11 fiyatlarıyla). Planın boyu bunun altındadır ve ayrıca yazıldı.

## 0. Tek bakışta hüküm

| Grup | Kalem | Hüküm | Tek cümle |
|---|---|---|---|
| 1–3G | XU030 vadeli kapanış bazı sıçraması | **1-3G TRADE (mini)**; Kural 0 cevabına kadar kâğıt | En ucuz araç, aynı akşam 18:10–18:15 canlı ekran şart; kenar küçük ve sönüyor |
| 1–3G | ABD rafinerileri → TUPRS | **1-3G TRADE (mini)**; Kural 0 cevabına kadar kâğıt | Profile en uygun sinyal: sabah bilinir, kapanışta girilir; 2024–26'da t 1,0 |
| 1–3G | SAHOL/AKBNK 1–3 gün | **HAYIR** | Emekliye ayrıldı, yerine K1 (20 gün) geldi [PB K1] |
| 1–3G | Koza göreli momentum (TRMET/TRALT) | **IZLE** (kâğıt) | 2024–26 net ≈0 [RH-K §3]; tetik \|z3\| > 1,5 |
| 1–3G | Altın → TRALT | **IZLE** (kâğıt) | DÜŞÜK, rejime bağlı; ≥ ~700 bin TL hesap ister; tetik \|z\| > 1 |
| 1–3G | ASX FMG/BHP → EREGL | **HAYIR** | OOS t 0,92, 2022–23 negatif |
| 1–3G | Kredi notu kararı sonrası ters | **IZLE** (olay günü) | n=16, son iki karar kayıp |
| 1–3G | Ay dönümü | **HAYIR** | Kazanç yalnız 2020–23 |
| 1–3G | VİOP USDTRY → THYAO | **HAYIR** | Kur carry'si; drift düzeltmesiyle t 0,82 |
| 1–3G | Yürütme ipucu | **HAYIR** (strateji olarak) | Her VİOP emrinde yürütme kuralı olarak uygula |
| Kırılım | ENJSA | **IZLE → SWING K4** | Kapanış > 127,00; bilançosu geldi, en erken giriş 10.11 |
| Kırılım | ENERY / AHGAZ (tek isim) | **IZLE → SWING K4** | 14,60 / 48,70; bilanço 9.11; en erken 16.11 |
| Kırılım | KCHOL | **IZLE → SWING K4** | 225,50 ve SMA50 üstü; bilanço 9.11 |
| Kırılım | RYSAS | **IZLE → SWING K4** | 30,28; bilanço 9.11; en erken 16.11 |
| Kırılım | BRSAN | **IZLE → SWING K4** | 769,50; stop %25 |
| Kırılım | TRGYO, GLYHO | **HAYIR** | K4 evreni dışı (likidite sırası 85 / 96 > 75) |
| VİOP | SAHOL, AKBNK | **SWING TRADE (K1)** | Tek doğrulanmış piyasa-nötr kol; bugün z −0,54 |
| VİOP | GARAN, YKBNK, THYAO, BIMAS, EREGL | **HAYIR** | İşlenebilir öncülük yok; yönlü işlem için rejim KAPALI |
| VİOP | TUPRS | **1-3G TRADE (mini)** | Yukarıdaki rafineri kuralı |
| VİOP | TRMET, TRALT | **IZLE** | Koza ve altın kuralları kâğıtta |
| VİOP | KCHOL, ENJSA | **IZLE** | K4 tetikleri; K2 kâğıt |
| Küme | RAFİNERİ, KOZA_ALTIN, ÇELİK | **IZLE** | Yalnız içindeki tekil kurallar (TUPRS; Koza/altın; BRSAN) |
| Küme | HOLDİNG, PERAKENDE, BANKA, GYO | **HAYIR** | Küme beta kolu K7 kapalı; 3 aylık TL getirileri nakdin altında |

## 1. 1–3 günlük kurallar ([PL] §1)

**Ortak:** Eski dört lead-lag sinyali planda kâğıtta. Canlı yürütülecekse hepsinin toplam açık riski ≤ %0,5 ve bu, K4 sonda bütçesinden düşülür [PB §3.11]. [PL] gerçek paradan önce 2–3 ay ileriye dönük kâğıt izleme istiyor. **Kural 0:** VİOP teminatı faiz kazanmıyorsa ve PPF/DİBS teminata kabul edilmiyorsa hiçbir VİOP kolu açılmaz; aracı kurumun yazılı cevabı gelene kadar yalnız spot kollar açılabilir [PB §6.1]. Sorular Pazartesi gönderildiği için 9.11'de bu kurallar yalnız kâğıtta [PAZARTESI_OZET]. Gün içi stop hiçbirinde test edilmedi; koruma boyuttur. Limit emir kullanılır, piyasa emri yok.

### 1.1 XU030 vadelisi kapanış bazı sıçraması: **1-3G TRADE (mini)**
- **Kural:** 18:10'da spot kapanış çıkınca b = ln(F_XU030 son fiyat / XU030 spot kapanış), Δb = b − dünkü b (aynı vade). |Δb| > 1 × std120(Δb) (~50 bps) ise ters yön: vadeli ucuz kapandıysa AL, pahalıysa SAT. Giriş 18:10–18:15 limitli, çıkış **ertesi gün uzlaşma**sında [PL #1].
- **Araç ve vade:** F_XU0301226 (endeks vadelisi yalnız çift aylarda; vade 31.12). Δb aynı vadeyle hesaplanır, devir günü sinyal yok.
- **Boy:** 1 mn TL'de en çok 1 kontrat (kendi önerim; dosyalarda boy kuralı yok). Nominal ≈ 14.878 × 10 ≈ 149 bin TL (hesap; uzlaşma [SİN §5], çarpan [RH-A §2]).
- **Kanıt:** ~65 işlem/yıl. Son fiyattan brüt +25, uzlaşmadan +19; ~5 bps maliyetle net **+14…+20 bps/işlem**. IS +24 / OOS +25 (t 1,85); 2024–26 +17 (t 1,1); eğim −0,76 → −0,27, sönüyor [KYC #1]. Yalnız alım tarafı +28,5 (t 2,9) [KYC #1 ek kontroller]. Bir gün geç giriş (E2) −2,5 bps [KYC #1] → aynı akşam yapılmazsa hiç yapılmaz. Güven ORTA.
- **TradingView:** Lead-lag değil, kapanış mikroyapısı. Grafik `BIST:XU030DZ2026/BIST:XU030` (vade kodu kalıbı [TV]'nin XU030D1! satırında), bağlam `BIST:XU030D1!`. **Pine yok.** TradingView ücretsiz hesapta BIST 15 dk gecikmeli [LL] → sinyal aracı kurumun canlı ekranından hesaplanır.
- **06.11 durumu:** Δb dosyalarda yok.

### 1.2 ABD rafinerileri → TUPRS: **1-3G TRADE (mini)**
- **Kural [RH-T §2]:**
  - r_i = ln(adj_t / adj_t−1), i ∈ {VLO, MPC, PSX, PBF}.
  - β_i = 250 ABD günlük cov(r_i, r_SPX) / var(r_SPX), o gün hariç.
  - P = ort(r_i − β_i·r_SPX), en az 3 hisse dolu olmalı.
  - z = P / std(P, önceki 250 BIST günü).
- **Ne zaman bilinir:** ABD kapanışı 00:00 TSİ'de (kış saati 01.11.2026–14.03.2027) sinyal kesinleşir; sabah 08:30–10:00 `sinyal_tuprs.py` çalıştırılır.
- **İşlem:** |z| > 1 → F_TUPRS'ta z yönünde, aynı gün 18:00–18:10 uzlaşma penceresinde limitli giriş. t+2 sabahı z yeniden hesaplanır:
  - aynı yönde |z| > 1 → UZAT
  - ters yönde → ÇEVİR
  - aksi halde 18:00–18:10'da KAPAT
- **Boy:** [RH-T §4]: 1 mn TL'de %0,5 risk = 2 kontrat. [RT]: 7,7 kontrat. Ortak %0,5 bütçe yüzünden 1–2 kontrat. **XU030 hedge'i yok;** TUPRS'ta işe yaramıyor [PL §3].
- **Vade (rehber ile plan çelişiyor):**
  - Rehber [RH-T §6]: vadeye ≥ 3 BIST günü kalan en yakın kontrat; test bu kuralla yapıldı. Buna göre 25.11'e kadar F_TUPRS1126, 26.11'den itibaren F_TUPRS1226 (hesap).
  - Plan [PB §3.10 A10, "bütün kollar"]: Kasım pay vadelisi yeni pozisyonda kullanılmaz; açık Kasım bacakları en geç 25.11'de kapanır. A10 yalnız 20 günlük kollar için değil.
  - Plana uyulursa F_TUPRS1226 kullanılır: 06.11 hacmi 106 mn TL, açık pozisyon 3.403; Kasım'da 2.168 mn TL / 94.540 [SİN §5]. Rehber de ön vade dışı ayların ince olduğunu söylüyor [RH-T §6]. Kasım'la girmek plandan sapmadır ve günlüğe yazılır.
- **Ne zaman yapılmaz:**
  - 27.11'de sinyal yok (Şükran Günü).
  - İşlem yönünde limit kilidi varsa girilmez.
  - Giriş penceresi kaçırıldıysa ertesi gün girilmez.
  - Sepete hisse eklenmez, sepetten hisse çıkarılmaz.
- **Kanıt:**
  - ~53 işlem/yıl. Net **+42 bps** (8 bps maliyetle, t 2,72); 15 bps maliyetle +35. IS +34,5 / OOS +48,8 (t 2,12) [KDC].
  - 2024–26 +26 (t 1,0). En iyi 10 işlem çıkınca t 1,45.
  - Tem–Eki 2026 en derin düşüş dönemi; fon krizinde 8 pozisyon ortalaması −165 bps. PBF çıkarılınca t 1,7 [RH-T §7, §12].
  - En kötü tek pozisyon −%16,9 (04.08.2026 kısa).
  - Güven: sinyal ORTA, kârlılık DÜŞÜK–ORTA.
- **TradingView lead-lag (işlenebilir, kapanıştan kapanışa):**
  - Liderler: `NYSE:VLO`, `NYSE:MPC`, `NYSE:PSX`, `NYSE:PBF`; piyasa `SP:SPX`. Yalnız **önceki** ABD gününün kapanışı kullanılır. Aynı gün ABD hareketiyle sinyal üretme; 15:00 UTC sürümü ≈0 verdi [RH-T §3].
  - Pine: `/home/user/Xxxx/raporlar/2026-11-04_kapanis_1-3gun/rehber/tuprs/tuprs.pine`, `BIST:TUPRS1!` günlük grafiğinde. Derlenmedi; son 10–20 günü betikle karşılaştır, fark > 0,05 ise betik esastır.
  - Son 250 günde betalar negatif (ortalama −0,48): S&P yükselince uzun eşiği düşer [RH-T §5].
  - Bağlam (sinyal değil): `AMEX:CRAK`, `AMEX:XLE`, `ICEEUR:BRN1!` (Brent senkron; pc 0,16, son 1 yılda 0,45 [KART TUPRS]).
  - [KART TUPRS] aynı sürücünün **gün içi** sürümünü "sınırda, işlem DÜŞÜK" sayıyor (açılış seansı gerektirir). Kapanıştan kapanışa sürüm [PL]'de ayakta kalan tek yayılma sinyali.
- **Diğer:** K4 tetiği 409,90 (05.11, +%23,6 uzakta) [PB §4.4]. Temettü K3/K3b sezonu ilkbahar.
- **06.11 durumu:** 03.11'de kısa pozisyon açıldı (z −1,47); 05.11 çıkış günüydü [RH-T §5]. Sonrası dosyalarda yok → Pazartesi sabahı betiği çalıştır. 6.11 akşamı planlanan bilançoyu KAP'ta teyit et.

### 1.3 SAHOL/AKBNK 1–3 gün (z60 ±1,5): **HAYIR**
- Aynı çiftte iki sinyal çalıştırılmaz. 1–3 günlük sürüm emekliye ayrıldı, yerine K1 geldi [PB K1 "Eski sürüm"].
- Eski sürümün gerçekçi beklentisi +30–50 bps/işlemdi. 3 güne zorla sınırlamak sonucu bozuyordu [PL #2]. K1 için §3'e bak.

### 1.4 Koza göreli momentum (TRMET1! / TRALT1!): **IZLE (kâğıt)**
- **Kural [RH-K §1]:**
  - u = r_TRMET − β_g·ort(r_TRALT, r_TRENJ); β_g 250 gün, bir gün gecikmeli.
  - z3 = (u_t + u_t−1 + u_t−2) / (σ60·√3).
  - z3 > +1,5 → TRMET1! AL + TRALT1! SAT; z3 < −1,5 → tersi. TRALT nominali = β_TA (≈0,69) × TRMET nominali, yani bugün ≈ 1 TRMET1! : 2 TRALT1!.
  - 17:50–17:55'te canlı fiyatla hesaplanır, 18:00–18:10'da iki bacak birlikte girilir. Tutma 2 gün; aynı yönde sinyal sürerse uzatılır, en çok 6 gün.
- **Yapılmaz:** kilit günü, kurumsal olay günü ve ertesi günü, tek bacakla. Kümülatif −800 bps'te kural durdurulur.
- **Kanıt:**
  - Uzlaşmadan girişle h2 +45 (t 4,05); ertesi gün girişle +30 (t 2,6), 8/8 yıl. 2024–26 +21 (t 1,2) [PL #3].
  - Rehber [RH-K §3]: %0,75 riskte net ≈ +28,8 bps/işlem, ~18 işlem/yıl ≈ +19 bin TL/yıl (1 mn TL), **2024–26 net beklenti ≈ 0**. 2026 toplamı −458 bps [RH-K §8].
  - Kurumsal olay riski (TMSF, birleşme). Güven: [PL] KOŞULLU/ORTA, denetimli rehber **DÜŞÜK** [RH-K başlık] → kâğıt.
- **Boy (canlıya geçilirse):** %0,5 risk = 14 TRMET1! + 28 TRALT1! [RH-K §3]. [RT]: TRMET 19,0, TRALT 51,8.
- **TradingView:**
  - **Klasik lead-lag yok** [RH-K §9.5]: TRALT(t−1) → TRMET katsayısı 2022–26'da −0,13 (t −2,4), yani ters. Kazanç TRMET'e özgü momentumdan geliyor.
  - Pine: `/home/user/Xxxx/raporlar/2026-11-04_kapanis_1-3gun/rehber/koza/koza.pine`, `BIST:XU030` günlük grafiğine. Girdiler `BIST:TRMET`, `BIST:TRALT`, `BIST:TRENJ`; işlem `BIST:TRMET1!`, `BIST:TRALT1!`; bağlam `BIST:XMADN`, `COMEX:GC1!`.
  - Kapanıştan kapanışa işlenebilir.
- **06.11 durumu:** 03.11'de z3 +0,49; 04.11 gün içinde ~+1,5 ile eşikteydi [RH-K §10]. 06.11 z3 dosyalarda yok. TRALT/TRMET bilançosu tarihsiz [PB A1] → **9.11 kapanışında girme.**

### 1.5 Altın → TRALT: **IZLE (kâğıt)**
- **Kural [RH-A §1]:** g = ln(TVC:GOLD 17:55 / önceki BIST günü 17:55), z = g / σ250. Bugün σ ≈ %1,70, yani eşik ≈ ±%1,70.
  - z > +1 → TRALT1! AL + XU030D1! SAT; z < −1 → tersi.
  - Oran: 1 XU030D'ye karşı N = yuvarla(10·XU030 / (β·100·TRALT)). β, TRALT/XU030'un 250 günlük betası (03.11'de 1,29 → N ≈ 30–32).
  - Giriş 18:00–18:15; 2 BIST günü sonra aynı pencerede çıkış. Aynı yönde sinyal gelirse 2 gün uzatılır, ters sinyalde çevrilir.
  - Arife günü yeni pozisyon açılmaz.
- **Kanıt [RH-A §8]:**
  - 8+3 bps maliyetle net +35,5 (t 2,20). 2024–26 +54 (t 1,96). En iyi 10 işlem çıkınca t 0,94.
  - Yıllar: 2021 −48, 2023 0. Fon krizinde −82.
  - DÜŞÜK; yalnız altın rallisi rejimlerinde çalışıyor [PL].
- **Boy:** 1 birim = 1 XU030D + ~30–32 TRALT1!. 1 mn TL'de 1 birim; ~700 bin TL altında yapılmaz, çünkü hedge'siz sürüm zayıf [RH-A §5].
- **TradingView:**
  - Sinyal `TVC:GOLD` (yedek `OANDA:XAUUSD`); bağlam `BIST:XAUUSD1!`. İşlem `BIST:TRALT1!` + `BIST:XU030D1!`.
  - Pine: `/home/user/Xxxx/raporlar/2026-11-04_kapanis_1-3gun/rehber/altin/altin.pine`.
  - `COMEX:GC1!` sinyal için kullanılmaz (vade geçişinde sıçrıyor).
  - Klasik lead-lag değil: TRALT altına aynı gün eksik tepki veriyor (altın katsayısı t 2,84; TRALT'ın kendi hareketi t 0,29) [RH-A §9]. Kapanıştan kapanışa işlenebilir.
  - [KART TRALT] #2: `AMEX:GDX` t−1 → gün içi "sınırda", 09:30 açılış ister → bu profil için değil.
- **06.11 durumu:** 04.11'de AL adayıydı (z +1,47) [RH-A §10]; sonrası dosyalarda yok. 9.11 bilanço gecesi olabilir → girme.

### 1.6 ASX FMG/BHP → EREGL: **HAYIR**
- **Kural (bilgi için) [KDC; c2_asx.py]:** P = ort(r_FMG − β250·r_ASX200, r_BHP − β250·r_ASX200), z = P / std250. |z| > 1 → F_EREGL z yönünde + β × F_XU030 ters; 3 gün. ASX 05:10 UTC'de kapanır [KART EREGL], yani 08:10 TSİ (hesap; AU yaz saati).
- **Kanıt:** h3 hedge'li net +46,3 (t 2,95). Ama OOS 2022–26 +19,7 (t 0,92), 2022–23 −50, vade profili tutarsız (h5 +12). Yalnız FMG ya da yalnız BHP ile t ≤ 1,1. 2024–26 +59 (t 2,2) [KDC §2]. DÜŞÜK.
- **TradingView:** `ASX:FMG`, `ASX:BHP`. ASX 200 endeksinin kodu [TV]'de yok → **teyit et.** [KART EREGL] #1: "maliyet sonrası ≈0". Pine yok.

### 1.7 Kredi notu kademe kararı sonrası ters: **IZLE (olay günü)**
- **Kural:** Not kademesi değiştiğinde, tepki gününün F_XU030 uzlaşmasında kararın tersine girilir; 2 gün tutulur [PL]. 1 kontrat ya da kâğıt.
- **Kanıt:** n=16; 8 bps maliyetle net h2 +142 (t 2,93), isabet %75. En iyi 3 olay çıkınca +94 (t 1,87). Son iki karar kaybettirdi: S&P 2024-11 −217, Moody's 2025-07 −53. Bonferroni sonrası p ≈ 0,14 [KDC §6]. DÜŞÜK.
- Karar takvimi dosyalarda yok → teyit et. TV: `BIST:XU030D1!`.

### 1.8 Ay dönümü: **HAYIR**
- XU030D1! ayın son VİOP günü uzlaşmada al, ertesi gün sat: h1 +44 (t 2,42), n=115. FDR'den geçmedi; kazanç yalnız 2020–23 rejiminde [KYC #7]. Kasım'ın son günü (30.11) zaten vade günü.

### 1.9 VİOP USDTRY 5 günlük değişim → THYAO: **HAYIR**
- Kazanç vadeli kurun carry eğiliminden geliyor; strateji fiilen sürekli THYAO kısa. Drift düzeltmesiyle 2024–26 +28,7 (t 0,82) [KDC §4]. ÇOK DÜŞÜK.

### 1.10 Yürütme ipucu: **HAYIR (strateji olarak), yürütmede UYGULA**
- Pay vadelisi kapanışta spota göre pahalıysa satışı öne al, alışı ertele; ucuzsa tersi. Getirisi ~5–10 bps [PL]. Tek bacak strateji olarak tekrar etmedi: +12,5 (t 0,95) [KYC #3].

## 2. Kırılım bekleme listesi ([SİN] §2; kural [PB] K4)

**K4 kuralı (hepsi için aynı):**
- **Sinyal (t kapanışı):** kapanış > önceki 252 günün en yüksek kapanışı + trend şablonu + RS ≥ 80.
- **Giriş:** t+1 kapanış seansında 18:01–18:05, limit = min(t kapanışı × 1,06; P_son × 1,03), spot.
- **Çıkış:**
  - Ana çıkış iz-stop: kapanış ≤ girişten beri en yüksek kapanış × 0,85 olursa ertesi kapanışta risk azaltan satış.
  - Süre 120 gün.
  - Kâr +%100'e ulaşırsa iz-stop %10'a iner.
  - Oranı ≥ %500 bedelsizde hak −1'de satılır.
- **Boy (KAPALI rejim):** risk %0,25 / stop %15 → nominal hesabın %1,67'si. VİOP-47 dışı × 0,75. En çok 2 sonda, aynı kümeden en çok 1.
- **Kanıt:** Aynı gün rastgele hisseye göre +%5,3 (t 5,1); isabet %45; kazanç/kayıp 3,3. En iyi %5 işlem kârın ~%70'i.
- **Zayıf yanlar:** 2024–26'da engelin 2–8 puan altında. VİOP-47'de 2024 sonrası rf'ye göre −%3,3/işlem. KAPALI rejimde katkı ≈0 [PB K4].
- **Ufuk:** 1–3 günlük bir işlem değil, haftalar-aylar.
- **Takvim:**
  - 9.11'de bilançosu çıkmamış isimde giriş yok (A1).
  - 11.11'de hiçbir kolda giriş yok; 11–13.11'de K4 girişi yok (A2).
  - Kredili esneklik uzatılırsa ilk giriş 16.11; uzatılmazsa K4 girişi 23.11'den, VİOP-47 dışı long (ENERY, AHGAZ, RYSAS) 30.11'den önce yok (A4).
- **TradingView:** Kapanış alarmı, ör. "`BIST:ENJSA` kapanış > 127,00, bar kapanışında bir kez" [PB §6.3].

| Hisse | Hüküm | Tetik (kapanış >) / gereken | Boy, 1 mn TL (hesap) | En erken giriş | TradingView / lead-lag | Not |
|---|---|---|---|---|---|---|
| ENJSA | IZLE → K4, kümede öncelikli | 127,00 / +%4,1; şablon 5/5, RS 94 | 16.667 TL ≈ 131 lot | 9.11 sinyali → 10.11 kapanışı. 10.11 sinyali → 11.11 yasak → 16.11/23.11 | `BIST:ENJSA`. [KART]: küresel sürücü yok; kapanış müzayedesi dönüşü VİOP'ta uygulanamıyor → **işlenebilir lead-lag yok** | Spot: Kasım vadelisinin ima faizi −%6,2 → KAP'ta temettü/sermaye işlemi ara (K3/A6) [PB §1.5]. [RT] 23,9 kontrat, β 0,60 |
| ENERY | IZLE → K4 | 14,60 / +%3,9; RS 97 | × 0,75 → 12.500 TL ≈ 856 lot | Bilanço 9.11 akşamı → ilk karar 10.11 → giriş en erken 16.11 | `BIST:ENERY`. Kart yok (VİOP dışı) → **lead-lag çalışılmadı** | AHGAZ ile tek isim; aktif ihraççı geri alımı yalnız bayrak, kenar değil [PB §3.11] |
| AHGAZ | IZLE → K4 | 48,70 / +%4,0; RS 99 | 12.500 TL ≈ 256 lot | ENERY ile aynı | `BIST:AHGAZ` [TV]'de yok → **teyit et**; kart yok → lead-lag yok | ENJSA, ENERY ve AHGAZ'dan en çok 1 pozisyon |
| KCHOL | IZLE → K4 | 225,50 / +%9,4. Ayrıca kapanış > SMA50 (210,94) şart; şablon 4/5 | 16.667 TL ≈ 73 lot | Bilanço 9.11 → ilk karar 10.11 → giriş en erken 16.11 | `BIST:KCHOL`. [KART]: NAV sinyalleri VİOP'ta DÜŞÜK, THYAO_t−1 sınırda/hayır → **yok** | Blok 1. K2 kâğıt (§3) |
| RYSAS | IZLE → K4 | 30,28 / +%10,8; RS 96 | 12.500 TL ≈ 412 lot | Bilanço 9.11 → en erken 16.11 | `BIST:RYSAS` [TV]'de yok → **teyit et**; kart yok | Test evreninde yoktu [PB §4.4] |
| BRSAN | IZLE → K4 | 769,50 / +%12,8; dizilim ✗ | Stop %25 → 10.000 TL ≈ 12 lot | 6.11 bilançosu teyit edilince | `BIST:BRSAN`. [KART]: öncülükler gün içi/açılış (metal akranları, gap fade) → **kapanıştan kapanışa yok** | Sık limit günü (3 yılda 20) [RT] |
| TRGYO | HAYIR | (101,70 / +%12,5) | — | Likidite sırası 85 > 75 | `BIST:TRGYO` [TV]'de yok → teyit et; kart yok | Sıra ≤ 75'e girerse yeniden bak |
| GLYHO | HAYIR | (18,73 / +%14,6) | — | Likidite sırası 96 > 75 | `BIST:GLYHO`; kart yok | HOLDİNG, Blok 1 |

## 3. VİOP pay vadelileri (hisse bazında)

### SAHOL ↔ AKBNK, K1: **SWING TRADE** (rejimden bağımsız, piyasa-nötr)
- **Sinyal:** x = ln(SAHOL) − ln(AKBNK), z = (x − ort60) / std60, bugün dahil.
  - z ≥ +2 → F_SAHOL SAT + F_AKBNK AL; z ≤ −2 → tersi. TL nominaller eşit.
  - 18:15 sonrası hesaplanır, **ertesi gün** girilir [PB K1].
- **Giriş (t+1):**
  - 17:50: bir bacak gün içinde ±%9'un ötesindeyse o gün giriş yok.
  - 17:55: iki bacak limitli, karşı en iyi fiyat ± %0,3. 18:05'te dolmayan bacak ± %0,6'ya çekilir.
  - 18:08'de hâlâ tek bacak varsa β × nominal kadar ters F_XU030 açılır; ertesi gün ikisi birlikte kapatılır.
- **Çıkış:**
  - Ana kural: 20. işlem günü, z ne olursa olsun.
  - Felaket stopu: çift K/Z bacak nominalinin ≤ −%8'i.
  - Sabancı/Akbank pay yapısında olay olursa ertesi gün çıkılır.
- **Vade:** 20 gün 30.11'i aştığı için doğrudan **Aralık** kontratı (makas ≤ %0,3). Aralık bacakları en geç 23.12'de Ocak/Şubat'a devredilir ya da kapanır.
- **Boy:** Bacak başına hesabın %7,5'i. 1 mn TL'de 75 bin TL/bacak ≈ **8 F_SAHOL1226 + 10 F_AKBNK1226** (hesap; 06.11 uzlaşma 91,41 / 71,77). Stop riski ≈ %0,6.
- **Kapılar:** Kural 0 (teminat faiz kazanmalı), komisyon ≤ 5 bps/bacak/yön, çift teminatı aracı kurumdan yazılı.
- **Kanıt:**
  - 1 gün gecikmeyle **+160 / +310 bps/işlem** (2010–18 / 2019–26), t 2,4 / 2,8; 20 bps maliyetle ~+140 / +290 [VB #25]. Seçim yanlılığı var.
  - Plan beklentisi: net +80…+180 bps/işlem, isabet %60–70, ~5 işlem/yıl, katkı +0,4 puan/yıl.
  - Güven: ilişki YÜKSEK, işlem ORTA [LL].
- **TradingView:**
  - Oran grafiği `BIST:SAHOL/BIST:AKBNK` [KART SAHOL #4]; işlem `BIST:SAHOLZ2026`, `BIST:AKBNKZ2026` (vade kalıbı [TV]).
  - Pine: `/home/user/Xxxx/raporlar/2026-11-04_kapanis_1-3gun/kod/sahol_akbnk_z.pine`; varsayılan giriş eşiği eski sürümün 1,5'i, girdiyi **2,0**'a çek; z penceresi 60. Derlenmedi. β250 kullandığı için K1'in β=1 z'sinden farklı çıkar → yalnız alarm; karar `bist_sinyal.py`'den. 20 günlük çıkış takvimden sayılır.
  - Pine'sız yaklaşık yol (kendi önerim): oran grafiğine Bollinger (60, 2); kapanış bant dışındaysa ≈ |z| ≥ 2.
- **Lead-lag:** [KART SAHOL #4] oran dönüşü "evet (2021–26, VİOP)". Bu bir ortalamaya dönüş, lead-lag değil. Gerçek lead-lag adayları işlenebilir değil:
  - AKBNK_t−1 → SAHOL gün içi: "maliyeti karşılamıyor".
  - ES/NQ, TUR, VIX, Nikkei: açılış gap'i.
- **Diğer:**
  - A9: 29.01–05.02.2027 arasında yeni K1 girişi yok.
  - A3 MSCI: listeden çıkarılan hisse yürürlüğe kadar yalnız short bacak olabilir.
- **06.11:** z **−0,54**, sinyal yok. Tam tetikler (öbür bacak sabitken) [SİN §4]:
  - z = +2: SAHOL ≥ 93,06 ya da AKBNK ≤ 64,40.
  - z = −2: SAHOL ≤ 84,09 ya da AKBNK ≥ 71,27.

### Hisse tablosu

| Hisse | Hüküm | Kural / kol | [RT] 3g kontrat · β · maliyet | TradingView lead-lag (kartın "işlenebilir" sütunu) | Diğer yöntemler / 06.11 |
|---|---|---|---|---|---|
| SAHOL | **SWING (K1)** | Yukarıda | 28,4 · 1,05 · 5,7 bps; XU030 hedge'i iyi | Yalnız oran dönüşü "evet"; gece sürücüleri "hayır (gap)" | Temettü K3 sezonu Mart–Haziran. 87,30; F_SAHOL1226 91,41 |
| AKBNK | **SWING (yalnız K1 bacağı)**; yönlü HAYIR | K1 | 30,9 · 1,13 · 5,6 bps | ES gece → gap 0,47 ama "Hayır (işlenemez)"; gece→gün içi OOS +3,3 bps/gün; TUR: hayır | Rejim KAPALI, Blok 1, A7 PPK kuralı. 68,65; F_AKBNK1226 71,77 |
| GARAN | **HAYIR** | K4 şablonu 3/7 → kırsa bile giriş yok [PB §4.4] | 17,6 · 0,99 · 7,9 bps | Yok: ES gece gap 0,53 işlenemez (gece→gün içi OOS −15,8 bps/gün); BBVA bağı 0,02 | Banka çiftleri maliyet sonrası ≈0 [PL §2]. 144,30 |
| YKBNK | **HAYIR** | K2 sepet üyesi (kâğıt) | 54,2 · 1,15 · 6,9 bps | Yok; banka çiftleri "sınırda, ~30 işlem/çift, t < 2" | 37,24 |
| KCHOL | **IZLE** | K4 (§2). K2 KCHOL↔sepet kâğıt: z 1,56, 03.11 kesişimi bayat; yalnız yeni \|z\| ≥ 2 kesişiminde, ≥ 5 mn TL ve ≤ 8 bps komisyonla; beklenti +40…+90 bps [PB K2] | 13,4 · 0,93 · 6,7 bps; hedge'i iyi | Yok: NAV iskontosu VİOP fiyatlarıyla t 1,0–1,5; açılış NAV ayrışması OOS −6 bps | Bilanço 9.11. 206,10 |
| ENJSA | **IZLE** | K4 (§2), spot | 23,9 · 0,60 · 8,6 bps; likidite C | Yok (küresel bağ yok) | Vadeli ima anormal → temettü kontrolü. 122,00 |
| TUPRS | **1-3G TRADE (mini)** | §1.2 | 7,7 · 0,43 · 6,2 bps; XU030 hedge'i işe yaramaz | ABD rafinerileri: kapanıştan kapanışa işlenebilir (§1.2); Brent senkron | K4 uzak. 337,50; F_TUPRS1126 344,55 |
| THYAO | **HAYIR** | — | 11,1 · 0,84 · 5,9 bps | Avrupa+ABD havayolu artık sepeti t−1 (`XETR:LHA`, `LSE:IAG`, `LSE:EZJ`, `NASDAQ:RYAAY`, `NYSE:DAL`…) → gün içi: "sınırda, işlem DÜŞÜK"; 10:30 girişte net 8,5 bps (t 1,2) → açılış ister, bu profil için değil | HAVACILIK 126 günlük RS kırılımı → yalnız K9 (%0,25 risk) [PB K9]. USDTRY→THYAO HAYIR |
| BIMAS | **HAYIR** (şimdilik) | K4 tetiği 433,75 (05.11, +%17,5) uzak | 7,0 · 0,75 · 6,4 bps | Sağlam küresel sürücü yok; kapanış müzayedesi dönüşü VİOP'la uygulanamıyor | Bilanço 9.11; temettü K3 (KAP). 371,75 |
| TRMET | **IZLE** | Koza §1.4 | 19,0 · 1,03 · 8,1 bps; likidite B | Klasik lead-lag yok; grup içi ters dönüş (t −4,6) yalnız gün içi, maliyetle test edilmedi | Bilanço tarihsiz (9.11) |
| TRALT | **IZLE** | Koza hedge bacağı + altın §1.5 | 51,8 · 1,17 · 6,5 bps | Altın senkron "hayır"; GDX t−1 "sınırda" (açılış); 17:55 altın kuralı kapanıştan kapanışa ama DÜŞÜK | Bilanço tarihsiz (9.11) |
| EREGL | **HAYIR** | §1.6 | 82,7 · 0,92 · 7,2 bps | FMG: "sınırda/hayır", yalnız 09:30 açılışta otomatik emirle; Japon çeliği aynı | ÇELİK; bilanço tarihsiz (9.11) |

## 4. Kümeler ([SİN] §3; kurallar [PB] K7, §4.3)

Küme beta kolu K7 kapalı (T2 = 0). 12 aylık RS'de ilk üç küme RAFİNERİ, HOLDİNG ve KOZA_ALTIN, ama üçünün de 3 aylık TL getirisi nakdin (+%9,4) altında → filtre nakitte. Küme sırası yalnız K4 slot önceliği ve yoğunlaşma sınırı (KAPALI'da küme başına 1 yönlü pozisyon) için kullanılır.

| Küme | Hüküm | 06.11 (RS 12a / TL 3a / R÷MA50 / RS zirvesinden gün) | Ne yapılır | Lead-lag (TradingView) |
|---|---|---|---|---|
| RAFİNERİ | IZLE (yalnız TUPRS kuralı) | +%24,0 / −%8,1 / −%4,5 / 5 | Ayrıştırıcı küme (bankayla korelasyon −0,42). XU030 hedge'i yok | `NYSE:VLO`/`MPC`/`PSX`/`PBF` − β·`SP:SPX` → TUPRS: işlenebilir (§1.2) |
| HOLDİNG | HAYIR (küme) | +%22,0 / −%8,4 / +%4,4 / 18 | SAHOL yalnız K1'de, KCHOL K4 alarmı; Blok 1 | Yok: holding ve bankalarda sektör emsal etkisi yok [LL §3] |
| KOZA_ALTIN | IZLE (kâğıt) | +%21,6 / −%24,6 / −%6,4 / 29 | Koza (§1.4) ve altın (§1.5) kâğıtta | `TVC:GOLD` 17:55 → TRALT (DÜŞÜK); `AMEX:GDX` yalnız gün içi |
| PERAKENDE | HAYIR | +%14,7 / −%15,7 / −%3,9 / 16 | BIMAS ve SOKM bilançosu 9.11 | Yok (BIMAS, SOKM: sağlam küresel sürücü yok [LL §4]) |
| ÇELİK | IZLE (yalnız BRSAN K4) | +%6,7 / −%19,6 / −%1,5 / 50 | EREGL ve KRDMD'de kural yok | `ASX:FMG`, `TSE:5411`, `TSE:5401` → EREGL/KRDMD: işlem DÜŞÜK, açılış ister |
| BANKA | HAYIR (yönlü) | +%3,9 / +%5,4 / +%9,4 / **0 (kırılım)** | Cazip görünüyor ama Blok 1. Bugün yalnız K9 (%0,25). XBANK 16.398, SMA200 16.948'in altında. PPK: indirim sonrası 63 günde bankalar 6/6 döngüde geride (−%6,3, t −4,2); 10.12 sürprizsiz indirimse ~15.03.2027'ye kadar yarım boy (A7) | Yok: ES/TUR gece bilgisi açılışta fiyatlanıyor |
| GYO | HAYIR | −%2,4 / −%7,8 / +%4,1 / 21 | TRGYO K4 evreni dışı | EKGYO: DİBS 2 yıllık t−1 → gün içi yalnız OOS'ta pozitif (DÜŞÜK); `TVC:TR02Y` bağlam |

## 5. Bütün satırlara uygulanan olay ve kaçınma kuralları ([PB] §3.10, §3.11)

**Takvim ve kaçınma:**
- **A1, bilanço:** 9.11 18:00'den önce bilançosu çıkmamış isimde 9.11 gecesi pozisyon taşınmaz, yeni giriş yapılmaz.
- **A2:** 11.11'de hiçbir kolda giriş yok; 11–13.11'de K3, K4, K5 ve K9'da yeni giriş yok.
- **A3, MSCI:** Duyuru 12.11 01:00. Çıkarılan ya da ağırlığı düşen hisse 30.11'e kadar alınmaz.
- **A4, kredili işlem esnekliği:** 13.11'de bitiyor. Uzatılmazsa K4 girişi 23.11'e, VİOP-47 dışı long 30.11'e kadar yok.
- **A5, bedelsiz:** Hak günü dahil 10 gün alış yok (oran ≥ %500'de 20 gün). Duyuruda ya da onayda da alış yok.
- **A6, yüksek verimli temettü (≥ %5):** Hak günü dahil 5 gün alış yok.
- **A7, PPK:** Banka kümesinde yarım boy kuralı (§4 BANKA satırı).
- **A10, vade:** Kasım pay vadelisi yeni pozisyonda kullanılmaz. Açık Kasım bacakları en geç 25.11'de, Aralık bacakları en geç 23.12'de devredilir ya da kapanır. Vade gününe pozisyon taşınmaz.

**Olay kolları:**
- **K3, temettü öncesi 5 gün (yalnız spot):** Verim %2–5, ilk 100 likit hisse. Gün −6'da al, gün −1'de sat. Olay başına +%0,2…+%0,5. Kasım–Aralık'ta olay az.
- **K3b, yüksek verimli temettü (≥ %5):** Bildirimden sonraki ilk kapanışta al, hak −1'de sat. Muhafazakâr kıyasla +%6,5 [PB K3b]. Pilot 01.02.2027'de başlıyor; o zamana kadar kâğıt.
- **K8, halka arz:** Yalnız eşit dağıtımlı arzlar; tavan serisi bozulduğu günün kapanışında satılır. 3 Eylül'den beri onay yok. Seri bittikten sonra **asla** alınmaz.

**Kullanılmayanlar:**
- **Opsiyon:** Alım ve satım ikisi de yok (test edilmedi; uzlaşmalar işlem fiyatlarının ~%30 üstünde) [PB §3.11].
- **Kural 0:** Teminat faiz kazanmıyorsa ve PPF/DİBS teminata kabul edilmiyorsa VİOP kolu yok. Cevap gelene kadar yalnız spot kollar açılabilir [PB §6.1].

## 6. Hangi satırı hangi betik hesaplıyor (otomatik günlük liste için)

| Satır | Betik | Saat |
|---|---|---|
| Rejim, KRİZ, K4 bekleme listesi ve tetikleri, küme RS, K1/K2 z, VİOP ima oranları | `uygulama/kod/bist_sinyal.py` | 18:15 sonrası; bülten için 20:45 sonrası |
| TUPRS ← ABD rafinerileri | `rehber/tuprs/sinyal_tuprs.py` | Sabah |
| Koza | `rehber/koza/sinyal_koza.py` | 17:50 canlı, 18:30 sonrası kesin |
| Altın → TRALT | `rehber/altin/sinyal_altin.py` | Sabah ve 17:55 |

- **Günlük betiği olmayanlar:** XU030 baz sıçraması, kredi notu kuralı ve ASX → EREGL. `kod/` klasörlerinde yalnız araştırma kodları var (kendi kontrolüm).
- **Hiçbir betiğin taramadığı veriler:** KAP olayları (temettü, bedelsiz, bilanço tarihi, ZPAT) ve MSCI listeleri [SİN §6].

## (a) Pazartesi 9.11 için kısa liste
1. **Alarm (kapanış):** `BIST:ENJSA` > 127,00 · `BIST:ENERY` > 14,60 · AHGAZ > 48,70 · `BIST:KCHOL` > 225,50 · RYSAS > 30,28 · `BIST:BRSAN` > 769,50 · K1: `BIST:SAHOL` ≥ 93,06 / ≤ 84,09, `BIST:AKBNK` ≤ 64,40 / ≥ 71,27 · `BIST:XU100` 12.630 / 13.566 · `BIST:XBANK` 16.948.
2. **08:30–10:00** `sinyal_tuprs.py`: |z| > 1 ise sinyali **kâğıda yaz** (z yönünde 1–2 kontrat, hedge'siz, 18:00–18:10). Pazartesi canlı VİOP yok: Kural 0 cevabı yok [PAZARTESI_OZET; PB §6.1]. Canlıya geçince kontrat F_TUPRS1226 (A10; çelişki §1.2). Betik açık pozisyon gösterirse (05.11 UZAT) kendi çıkış kuralıyla kapanır [PB K9]. TUPRS bilançosunu KAP'ta teyit et.
3. **18:10–18:15** XU030 Δb ~50 bps'i aşarsa ters yönde 1 kontrat F_XU0301226, Salı uzlaşmasında çıkış: **kâğıtta** (Kural 0). Canlıda da yalnız aracı kurumun canlı ekranıyla; ekran yoksa yapma.
4. **Pazartesi 9.11 kapanışında tetiklenirse, giriş Salı 10.11:** ENJSA 9.11 kapanışı > 127,00 (şablon ve RS ≥ 80 sürüyorsa) → 10.11 18:01–18:05 spot K4 sondası (%0,25 risk); K1 |z| ≥ 2 → 10.11 17:55 Aralık kontratları, yalnız Kural 0 yazılı cevabı ve ≤ 5 bps komisyonla.
5. **Kâğıda yaz:** Koza z3 (17:50) ve TVC:GOLD 17:55 değişimi (eşik ±%1,70); 9.11 bilanço gecesi nedeniyle ikisinde de canlı giriş yok. KAP'ta K3/K3b bildirimleri.
6. **Kaçın:** 9.11 akşamı bilanço açıklayanlarda (KCHOL, BIMAS, AHGAZ, ENERY, RYSAS, TRALT, TRMET, EREGL…) kapanışta yeni pozisyon ya da taşıma; 11.11'de her giriş; 11–13.11 K3/K4/K5/K9; MSCI 12.11 01:00; dışlama listesi.
7. **HAYIR:** GARAN/YKBNK/THYAO/BIMAS/EREGL yönlü; banka ve havacılık RS kırılımı (yalnız K9, %0,25); ay dönümü; USDTRY → THYAO; ASX → EREGL.
8. **Gece "lead-lag"ini (ABD vadelileri, TUR, Brent, gece altını) sinyal sayma:** açılış gap'idir, kapanıştan kapanışa işlenemez [LL §2].

## (b) Dürüst not: 1–3 günlük işlem gerçekte ne getirir?
1. **Kenarlar küçük ve sönüyor:** Ayakta kalan 1–3 günlük kenarlar işlem başına 15–50 bps. Dördü de 2024–26'da t 1,0–1,2'ye indi [PL §1, §5; PB §3.11]. Bireysel komisyonla (bacak başına ~22 bps) SAHOL/AKBNK ve TUPRS kenarının yarısı gider [PL §5].
2. **TL çıtası karşısında:** Örnek: TUPRS'ta 2 kontrat, 53 işlem/yıl ve 2024–26 ortalaması +26 bps ≈ 1 mn TL'de +9,6 bin TL/yıl, yani ~%1 (hesap). Koza'nın rehber beklentisi ~%1,9, ama 2024–26'da ≈0 [RH-K §3]. Çıta net ~%31–38 TL [`kazanc_stratejileri/RAPOR.md` §0]; bu kenarlar ancak çekirdek getirinin üstüne ek olur.
3. **En güçlü uzun ufuklu kenarlar:** SAHOL/AKBNK'yı 20 gün tutmak 1 gün gecikmeyle bile ~+140 / +290 bps/işlem veriyor (2010–18 / 2019–26, 20 bps maliyet sonrası) [VB #25; PB K1]. VB #25'teki 88–290 aralığının alt ucu KCHOL↔sepet kolunun (K2) rakamı. Yüksek verimli temettü +%6–7 [PB K3b]. 1–3 günlük kurallar (§6'daki betiklerle) mini boyda ölçüm aracı olarak kalsın.
