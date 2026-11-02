# ry_gunici_y — Yurt içi gün-içi lead-lag (ajan: gunici_y)
Tarih: 02.11.2026 · Hedef: 47 VİOP pay vadelisi dayanağı
Veri:
- **m5:** 07.08–30.10.2026 (60 gün). Tamamı AB yaz saatinde ve Eyl–Eki 2026 fon krizini içeriyor.
- **h1:** 30.11.2023–30.10.2026 (729 gün). 425'i 14:30 barının bulunduğu yaz günü.
- **Günlük:** 2014–2026.

Kod: `out/code_y_gunici_y/` (`c_common.py`, `a0_checks` … `a9_idio_fade`, `z_build_csv.py`; ara sonuçlar `res/`).
Bulgular: `out/f_y_gunici_y.csv` (1.680 satır: lead_5m 742 = 741 çift + 1 özet; lead_hourly 741; lead_auction 145 = 47 gap fade + 47 sektör + 48 kapanış + 3 portföy; intraday_momentum 51; event 1).
Çalıştırma sırası (`nice -n 10 python3 …`, dizin `code_y_gunici_y`): a0 → a1 → a1b → a3 → a4 → a4b → a5 → a6 → a7 → a8 → a9 → z_build_csv (a6/a7 a0, a1 ve a3 çıktılarını okur).
1. turun (uluslararası) sonuçlarını tekrar etmiyorum; burada yalnız BIST içi ilişkiler var.

## 0. Net bulgular tablosu

| # | Bulgu | Rakam | İşlenebilir mi? | Güven |
|---|---|---|---|---|
| 1 | **5 dk: XU030 → hisse, 1 bar (5 dk) gecikmeli tepki** (hedefin kendi 6 gecikmesi ve XU030 gecikmeleri kontrollü) | 46/47 hissede pozitif, 20/46'sı FDR'den geçiyor. En güçlüleri: HEKTS (std b 0,17, t 10,1; XU030'daki 1σ = 15,6 bps hareket başına +8,1 bps; tepkinin %90'ı 15 dk'da), SASA (+6,9 bps; 10 dk), ODAS (+3,0), TSKB (+2,7), TTKOM (+2,6), DOHOL (+2,5), ENJSA (+2,4; 10 dk), THYAO (+2,4), OYAKC (+2,2), GARAN (+1,9), CIMSA (+1,8). Diğerlerinde tepkinin ≥%90'ı en geç bir sonraki 5 dk barında, likit büyüklerde (GARAN, AKBNK, YKBNK, ISCTR, KCHOL) aynı barda tamamlanıyor. Hou–Moskowitz D1 medyanı 0,003 (en yüksek 0,046, HEKTS). | HAYIR. BT1 OOS medyanı brüt 0,4–1,5 bps/işlem; illikit hedeflerde 4–7 bps; maliyet 8–60+ bps | DÜŞÜK (60 gün) |
| 2 | **Gecikmenin yaklaşık yarısı bayat son fiyat ve tik ayrıklığından geliyor** | Hisse başına lag-1 katsayısının Spearman korelasyonu: fiyatı değişmeyen bar oranıyla +0,66, tik/fiyatla +0,46, ciroyla −0,39. İllikit yarıda önceki bar düşük hacimliyse b 0,105, aktifse 0,056. Önceki barda fiyat değişmemişse etki ~2 kat (ör. ALARK 0,20'ye karşı 0,05; BIMAS 0,19'a karşı 0,04). Getiri barın ilk işleminden ölçülünce (bar arası sıçrama hariç) katsayı ~%35–45 düşüyor (illikit 0,067 → 0,042). Ama aktif barlarda ve bar içinde de t 3–6 kalıyor | Kalan kısım gerçek ama ~5 dk süren bir yayılım | ORTA (açıklama olarak) |
| 3 | **Saatlik ölçekte BIST içi lead-lag YOK** | 16 lider × 47 hedef: 741 ileri ve 741 ters testin hiçbiri FDR'den geçmiyor (en küçük düzeltilmiş p 0,47). D1 medyanı 0,002 (en yüksek 0,012). IS/OOS işaretleri rastgele | — | YÜKSEK (olumsuz bulgu) |
| 4 | **Açılış penceresinde gecikme 2,7 kat güçlü** | Hedef barı 07:05–07:30 UTC olduğunda XU030_{t-1} katsayısı 0,158 (t 2,8); 07:30 sonrası 0,059 (t 7,9). Likit/illikit ayrımı benzer (0,178 / 0,138) | Hayır (maliyet) | DÜŞÜK |
| 5 | **Sektör içi 5 dk öncülük (bankalar, havayolu, perakende)** | XBANK/XLBNK/AKBNK/ISCTR → GARAN: b 0,10–0,17, t 4,1–5,7. YKBNK ↔ AKBNK 0,07–0,08. PGSUS/TOASO/ULKER → THYAO 0,055–0,067 (t 3,4–3,8). BIMAS → MGROS 0,065 (t 3,7). TUPRS → THYAO −0,072 (t −4,3) | HAYIR. BT1'de XBANK→GARAN IS +0,3…+11 bps, OOS −3…−8 bps; BIMAS→MGROS ≈0; TUPRS→THYAO işaret değiştiriyor | DÜŞÜK |
| 6 | **Gap fade, 47 hissede sistematik** (|gap|>%1 ise açılışta gap'in tersine pozisyon, kapanışta çıkış) | 2014–2026, açılıştan giriş (E0). Hisse medyanı: IS +12,4, OOS +17,8 bps/işlem; hisselerin %87'sinde OOS > 0; 10/47 FDR. |gap|>%2'de medyan OOS +67 bps, 21/47 FDR. Eşit ağırlıklı portföy: IS 28,0 bps (t 7,0), OOS 16,5 bps (t 2,8); illikit 24 hisse OOS 26,9 (t 3,9), likit 23 hisse OOS 3,1 (t 0,4). 13 yılın 11'inde pozitif (2014 −4,9 ve 2022 −6,3 hariç) | KISMEN. h1 döneminde ilk 30 dk VWAP vekiliyle giriş (E2) OOS 21,1 bps (t 1,9); 07:30 girişi (E3) 15,3 bps (t 1,5). Etki illikitlerde, maliyet de orada yüksek | ORTA |
| 7 | **CIMSA ve OYAKC gap fade** (1. tur bulgusu doğrulandı) | CIMSA: IS +38 (t 3,4), OOS +74 bps (t 3,8), E2 +78 bps (t 3,2, FDR). OYAKC: IS +48 (t 2,6), OOS +50 (t 2,7), E2 +48 (t 3,5, FDR). ALARK: E0 FDR, E2 +43 bps (t 2,3) | SSF tiki CIMSA 2,5 bps (~270 mn TL/gün), OYAKC 5,3 bps (~100 mn TL/gün). Gerçek spread bilinmiyor | YÜKSEK (ilişki); işlenebilirlik ORTA–DÜŞÜK |
| 8 | **Hisseye özgü gap fade, piyasa-nötr** (idio = gap − XU030 gap; XU030 vadelisiyle hedge) | Havuz regresyonu: hisseye özgü gap'in %11'i (2024+ %19, t −4,7) gün içinde dönüyor; piyasa gap'i dönmüyor (2024+ +0,03). Strateji (|idio|>%1): E0 IS 42,6 bps (t 10,7), OOS 24,2 (t 4,2), 2024+ 30,8 (t 3,6). E2 (h1): IS 20,1 (t 2,1), OOS 22,7 (t 2,3). Ağu–Eki 2026: −1,8 bps | 15 bps maliyet + hedge sonrası OOS ~5–8 bps | ORTA |
| 9 | **Sektör gap'inin yayılımı (yetişme)** | Kendi gap'i ve XU030 gap'i kontrollüyken akranların gap'i hissenin gün-içi getirisini pozitif tahmin ediyor: medyan b 0,09, %89 pozitif, 6/47 FDR (AKBNK, GARAN, VAKBN, BRSAN, CIMSA, OYAKC). h1'de etkinin tamamı ilk 30 dk'da (O→07:30 b 0,12; 07:30→kapanış −0,06). Portföy (|s|>%1, açılış→kapanış): IS 25,3 (t 7,6), OOS 23,4 (t 4,7) | HAYIR. E2→kapanış OOS 10,7 (t 1,2), E3→kapanış 6,6 (t 0,8); E0→07:30 15,9 (t 3,0) ama açılış müzayedesi fiyatı gerektiriyor | ORTA (ilişki) / DÜŞÜK (işlem) |
| 10 | **Kapanış müzayedesi hareketi ertesi sabah kısmen dönüyor** | CA = log(C / P15:00). Ertesi gap b −0,157 (t −3,7); ertesi O→07:30 b −0,192 (t −3,8). Müzayede hareketinin ~%35'i ertesi gün 10:30 TSİ'ye kadar geri dönüyor. Son 30 dk sürekli işlem (14:30–15:00 UTC) etkisiz (−0,02). Hisselerin %83'ünde negatif; FDR 7/47 (ENKAI, BIMAS, GARAN, VESTL, VAKBN, TRMET, ENJSA). Portföy (|CA|>25 bps, C→07:30): IS 11,7 (t 2,5), OOS 16,4 (t 4,1); yıllara göre 12,7 / 17,1 / 13,7. |CA|>50 bps'de OOS 25,7 (t 3,5). İllikit 18,7 (t 5,2), likit 7,7 (t 1,7). XU030'da yok (−0,10, t −0,4) | SPOT'ta 'kapanış fiyatından işlemler' (18:08–18:10 TSİ) ile C'den giriş gerekiyor; SSF ile birebir uygulanamıyor. 8–15 bps maliyet sonrası net +1…+10 bps | ORTA |
| 11 | **VİOP vade sonu (ayın son iş günü)** | SSF vade sonu uzlaşma fiyatı = spot kapanış fiyatı (30.10.2026 bülteninde 47/47 doğrulandı; fiziki teslim). Vade sonunda |CA| 37,7 bps, diğer günler 20,5 bps (×1,8). m5'te müzayede hacim payı %3,9'a karşı %2,9. CA dönüşü vade sonunda farklı değil (vade sonu hariç 14,4 bps, t 4,5). XU030 ay sonu cc −24 bps (t −2,0), ayın ilk günü +27 bps (t 1,9). Etki yalnız 2021+ döneminde (OOS −39 / +75 bps, t −2,1 / +3,3); IS'te yok | Takvim bilinir; endeks vadelisiyle işlenebilir, ama istikrarsız | DÜŞÜK |
| 12 | **Gün-içi momentum (Gao vd. 2018)** | XU030: r_first → r_last b 0,035 (t 1,6); IS 0,070 (t 2,5), OOS −0,008. İşaret stratejisi (14:30 → kapanış) brüt 4,0 bps (t 2,5; IS 4,1, OOS 3,9). Sinyal sign(O→07:30) ise 5,5 bps (t 3,5; IS 7,2, OOS 3,75, t 1,8). 47 hissede 0/47 FDR, havuz b ≈ 0 (t −0,02) | Endeks vadelisinde 2–4 bps maliyet sonrası ≈ 0–3 bps; hisselerde yok | DÜŞÜK (XU030) / ÇOK DÜŞÜK (hisse) |
| 13 | **Ters yön: hisse → endeks** | Hisse → XU030 5 dk öncülüğü yok (1/47 FDR: VESTL, negatif). Hisse → sektör endeksleri 8 FDR (küçük, çoğu negatif). TRMET → bankalar Σb −0,10…−0,15 (t −2,4…−3,6) | — | ÇOK DÜŞÜK / DÜŞÜK |

**Özet:** Endeks/lider bilgisi BIST hisselerine dakikalar içinde (çoğunda <5 dk) geçiyor. Saatlik ölçekte yayılım yok. İşlenebilir görünen yurt içi gün-içi etkiler lead-lag değil; müzayede kaynaklı fiyat baskısının geri dönüşü (açılış gap fade, kapanış müzayedesi dönüşü). İkisi de illikit hisselerde yoğunlaşıyor; maliyet de en çok orada.

---

## 1. Veri ve bar yapısı (bu ajan doğruladı, `a0_checks.py`)

**m5 barları:**
- 06:55 barı açılış müzayedesi. c'si günlük 'o' ile 60/60 gün aynı; hacmi 0.
- Sürekli işlem: 07:00–14:55 arası 96 bar.
- 15:00 kapanış müzayedesi barı yalnız son günde var. Bu yüzden kapanış günlük 'c'den alındı. 14:55 barının c'si günlük kapanıştan medyan 11–15 bps farklı; bu fark kapanış müzayedesinin etkisi.
- Bar 'o' değeri bardaki ilk işlem. Barların %62'sinde önceki barın c'sine eşit (tik ayrıklığı).
- Hisselerde sürekli işlemde hacmi 0 olan bar yok denecek kadar az (%0–0,2).
- Fiyatı değişmeyen bar oranı: KRDMD %9 … THYAO %28, SASA %51, HEKTS %49 (SASA/HEKTS 1,5–2,4 TL, tik 0,01 = 42–69 bps).

**h1 barları:**
- 06:30 barının c'si = 07:30 fiyatı. Yazın bu barın hacmi 0 görünüyor (Yahoo kusuru).
- **14:30 barı yalnız AB yaz saati aylarında var** (729 günün 425'i). Kışın son bar 13:30 (14:30'da bitiyor) ve 14:30–15:00 parçası eksik. Kanıt: kışın h1 hacim toplamı / günlük hacim 0,86, yazın 0,80; kışın son bar c'si kapanıştan %0,35, yazın 14:30 barının c'si kapanıştan %0,15 farklı.
- Bu nedenle yıl boyu tutarlı parçalar kullanıldı: O → 07:30 → saatlik … → 14:30 → C. Kapanış müzayedesi (CA) yalnız yaz günlerinde ayrıştırılabiliyor.
- h1 ile m5 kesişiminde P07:30, P08:30, P14:30 ve P15:00 değerlerinin farkı 0,0 bps.

**Eksik veriler:**
- XLBNK ve XHOLD: Yahoo'da günlük geçmiş yok (1 satır). h1'de yalnız r2…r8 parçaları, m5'te tam veri kullanıldı.
- TRALT ve TRMET: h1 verisi yalnız 25.11.2025'ten beri var (ticker değişimi); IS dönemi yok.

**Fiyat adımları:**
- Spot tik tablosu (0,01/0,02/0,05/0,10/0,25/0,50…) m5'teki en küçük fiyat değişimiyle ampirik olarak tutarlı.
- VİOP pay vadelisi tiki: bülten ondalıklarından çıkarımla 0,01 TL (47'nin 46'sında; BRSAN ≥0,05?). Bu, spot tikinden çok daha ince. Sözleşme dokümanından doğrulanmadı.

## 2. Yöntem

**5 dk lead-lag (`a1_m5_leadlag.py`):**
- Model: y_t = a + Σ_{k=1..6} b_k·L_{t−k} + Σ c_k·y_{t−k} + Σ d_k·XU030_{t−k} + e.
- Gecikmeler gün içinde; günün başından önceki gecikmeler 0. Hedef slotlar 07:05–14:55.
- Getiriler slot bazında standartlaştırıldı (her 5 dk dilimi eşit ağırlık); ham getiri ayrıca hesaplandı.
- Standart hatalar gün kümelenmiş. Testler: Wald(b1..6) ve Σb. BH-FDR 741 ileri ve 741 ters test üzerinden ayrı ayrı.
- Dayanıklılık:
  - açılış hariç (07:30 sonrası);
  - iki yarı (30/30 gün);
  - bayat fiyat varyantları: hedefin bar içi getirisi log(C_t/O_t), bar arası sıçrama log(O_t/C_{t−1}), önceki barda fiyat değişmiş/değişmemiş, önceki bar hacmi slot medyanının üstünde/altında.
- Gecikme süresi: lag0..6 dağıtılmış gecikme modelinde kümülatif tepkinin %90'a ulaştığı lag × 5 dk. Ek olarak Hou–Moskowitz D1.

**Saatlik (`a1b_h1_leadlag.py`):** Aynı model, parçalar r1..r9. IS ilk yarı (<15.05.2025), OOS ikinci yarı.

**Açılış (`a3_open.py`, `a7_extra.py`, `a9_idio_fade.py`):**
- Gap fade, eşikler 0 / 0,5% / 1% / 2% / z>1 / z>2.
- Girişler:
  - E0 = açılış müzayedesi fiyatı (iyimser);
  - E2 = h1 06:30 barının (h+l+c)/3 değeri, yani ilk 30 dk VWAP vekili;
  - E3 = 07:30 fiyatı;
  - m5'te E1 = ilk 5 dk tipik fiyat, E1b = 07:00–07:15 hacim ağırlıklı fiyat, E4 = 07:05.
- Sektör yayılımı: y ~ kendi gap + akran (kendisi hariç) gap ortalaması + XU030 gap.
- Açılış hızı: O→07:30 hareketinin ilk 5/10/15 dk'da gerçekleşen payı (ağırlıklı fiyat katkısı, WPC).

**Kapanış (`a4_close.py`, `a4b_eom.py`):**
- Değişkenler: CA, L30 = 14:30→15:00, DAY = O→14:30.
- Ertesi gün: gap, O→07:30, gün-içi, 07:30→kapanış.
- Vade sonu = ayın son BIST iş günü (bültende VADE TARIHI ile doğrulandı).

**Momentum (`a5_mom.py`):**
- r_first = önceki kapanış → 07:30 (Gao tanımı, gece gap'i dahil).
- r_last = 14:30 → kapanış.
- Ayrıca r_last_c = 14:30→15:00 (yaz) ve r_12 = 13:30→14:30.
- HAC(5) standart hatalar. Hisse bazında ve havuz (gün kümelenmiş, kesitsel arındırılmış).

**Backtest (`a6_bt.py`, `a8_regime.py`, `a9_idio_fade.py`):** Look-ahead yok. Sinyal pozisyondan önce biliniyor; z-skorlar önceki günlerden.

## 3. Kanıt

### 3.1 5 dk: XU030 → hisse (std katsayı; bps = XU030'daki 1σ 5 dk hareketi başına hedefin sonraki 5 dk tepkisi)

| Hedef | b1 (t) | bps/1σ | %90 tepki | bar içi b1 (t) | önceki bar düşük hacim / aktif | fiyatı değişmeyen bar | spot tik (bps) | ciro (mn TL/gün) |
|---|---|---|---|---|---|---|---|---|
| HEKTS | 0,174 (10,1) | 8,1 | 15 dk | 0,095 (6,2) | 0,168 / 0,152 | %49 | 42 | 566 |
| SASA | 0,133 (7,1) | 6,9 | 10 dk | 0,063 (4,0) | 0,124 / 0,114 | %51 | 44 | 4.903 |
| OYAKC | 0,102 (7,1) | 2,2 | 5 | 0,058 (3,7) | 0,154 / 0,083 | %24 | 9,5 | 249 |
| TSKB | 0,155 (7,0) | 2,7 | 5 | 0,090 (4,1) | 0,198 / 0,137 | %29 | 9,2 | 198 |
| ODAS | 0,103 (6,2) | 3,0 | 5 | 0,062 (4,3) | 0,145 / 0,089 | %30 | 14 | 279 |
| DOHOL | 0,098 (5,9) | 2,5 | 5 | 0,055 (3,3) | 0,090 / 0,112 | %21 | 9,7 | 175 |
| CIMSA | 0,088 (5,1) | 1,8 | 5 | 0,070 (3,9) | 0,093 / 0,095 | %14 | 4,6 | 284 |
| ENJSA | 0,085 (5,0) | 2,4 | 10 | 0,059 (3,9) | 0,151 / 0,064 | %24 | 8,9 | 372 |
| TTKOM | 0,106 (4,9) | 2,6 | 5 | 0,066 (3,2) | 0,160 / 0,089 | %22 | 9,4 | 1.417 |
| THYAO | 0,113 (4,4) | 2,4 | 5 | 0,059 (2,2) | 0,098 / 0,121 | %28 | 8,5 | 9.753 |
| GARAN | 0,097 (4,1) | 1,9 | 0 (aynı bar) | 0,059 (2,4) | 0,118 / 0,090 | %21 | 7,6 | 3.593 |
| Tepki vermeyenler | ASTOR −0,02, TUPRS 0,00, KRDMD 0,01, VAKBN 0,02, FROTO 0,03, SISE 0,04, ISCTR 0,04, ASELS 0,03, KCHOL 0,04 (t<2) | | | | | | | |

**Diğer liderler:**
- XBANK ve XLBNK medyan Σb ~0,09. AKBNK 11 FDR, ISCTR 7, XLBNK 8, XBANK 6, TUPRS 6 (negatif).
- XHOLD ve XUSIN zayıf (Σb ≈ 0).
- Gecikmeli pay medyanı 0,05–0,23.

### 3.2 Bayat fiyat mı, gerçek gecikme mi? (Görev 2)
Kanıtlar:
- Lag-1 katsayısı en çok fiyatın sık değişmediği, tiki büyük ve cirosu düşük hisselerde (Spearman +0,66 / +0,46 / −0,39).
- Bar arası sıçrama, yani önceki barın son işlemi ile bu barın ilk işlemi arasındaki fark, XU030 gecikmesiyle güçlü ilişkili. Medyan b 0,10–0,11 ve tüm hisselerde t>2. Bu, "ilk işlem önceki bilgiyi hemen yansıtıyor, son fiyat bayattı" demek.
- İllikit yarıda önceki bar düşük hacimliyse etki 0,105, aktifse 0,056.

Sonuç: gecikmenin ~%40–50'si mekanik. Kalan kısım bar içinde (ilk işlemden sonra) devam ediyor. İllikitlerde medyan 0,042, HEKTS 0,095 (t 6,2). Bu gerçek bir ~5 dk'lık yayılım; yine de 1σ XU030 hareketi başına 1–5 bps, yani işlenemez.

**BT1 (5 dk, XU030 → 47, örtüşmesiz):**
- |z|>1,5, 1 bar tutma: OOS medyan brüt +1,5 bps/işlem; giriş C_t yerine O_{t+1} (ilk işlem) olunca 1,5 bps.
- 3 bar tutma: 0,4 bps.
- |z|>2,5, 3 bar tutma: 5,4 bps (n 3.290).
- İllikit hedeflerde OOS +4…+7 bps (HEKTS h=1 +7,4, t 2,9; TSKB +4,6; OYAKC +4,1). Ama bu hisselerin SSF tiki 5–58 bps ve spread'i çok tik.

### 3.3 Saatlik: yok
- 741 ileri testten |t1|>3 olan yalnız 1, |tΣ|>3 olan 10 çift var; hiçbiri FDR'den geçmiyor.
- XU030 → hisse medyan b1 0,012 (IS 0,029, OOS −0,003).
- Bu güçlü bir olumsuz sonuç: BIST içinde "endeks/sektör/lider hisse bir saat önceden haber verir" diye bir şey yok. 5 dk'daki gecikme ilk 5–15 dk'da tükeniyor.

### 3.4 Açılış (Görev 3)

**Gap fade:**
- Eşiğe göre medyan OOS (bps/işlem): 0 → +2,1; 0,5% → +6,6; 1% → +17,8; 2% → +67; z>2 → +47,6.
- FDR'den geçen hisse sayısı: 5 / 12 / 10 / 21 / 14.
- Likit büyükler (TUPRS, SAHOL, PGSUS, KRDMD, YKBNK, AKBNK, ISCTR, GARAN, HALKB) ≈0 veya negatif.
- Havuz regresyonu: gün-içi getiri ~ gap, b −0,106 (t −4,2), yani gap'in ~%10'u gün içinde dönüyor. Bu tamamen hisseye özgü kısımdan geliyor: idio −0,113 (t −5,4), piyasa −0,085 (t −1,5); 2024+ idio −0,19, piyasa +0,03.

**Açılış dolumu gerçekçiliği** (|gap|>%1, h1 2023-12+; gap'in tersi yönde açılışa göre kayıp):
- İlk 30 dk VWAP vekili: −3,0 bps.
- 07:30: −10,1 bps.
- Toplam açılış → kapanış fade'i: 16,6 bps.
- m5'te ilk 5 dk tipik fiyat −2,4 bps, 15 dk VWAP −0,5 bps (60 gün).

Sonuç: Dönüşün çoğu ilk 30 dk'dan sonra oluşuyor. İlk 5–30 dk VWAP girişiyle etkinin %80'i korunuyor. 07:30'a kadar beklemek etkinin yarısını götürüyor. VİOP pay vadelisi 09:30 TSİ'de, spot müzayededen önce açıldığı için SSF'de 10:00 civarı giriş fiilen E1/E2'ye yakın. SSF gün-içi fiyat verisi olmadığı için test edilemedi.

**Rejim:**
- 2025 ≈ +4 bps (t 0,3); Mart 2025 (İmamoğlu şoku) −90 bps/gün.
- 2024 +37 bps (t 3,1); 2026 Ocak–Ağustos +37 bps.
- Eyl–Eki 2026 fon krizi: portföy +28 bps (t 0,8).
- Ağu–Eki 2026 işlem bazında −40 bps (Ekim −97 bps, 155 işlem). Toplu gap günlerinde gap'ler devam etti.
- Hisseye özgü E2 fade Ağu–Eki 2026'da −1,8 bps.

**Sektör yayılımı:** Yetişme ilk 30 dk'da gerçekleşiyor; 07:30'dan sonra etki yok, hatta hafif ters. Bankalarda katsayılar en büyük (b_sec 0,41–0,48), ama banka gap'leri çok korelasyonlu olduğundan bireysel katsayılar çoklu doğrusallık altında.

**Kim önce hareket ediyor (WPC, 60 gün, gürültülü):**
- 07:05'e kadar O→07:30 hareketinin medyan %44'ü gerçekleşiyor.
- En yavaşlar (%29–35): SOKM, EKGYO, OYAKC, BRSAN, TTKOM, BIMAS.
- En hızlılar (%53–64): AEFES, DOAS, ARCLK, TKFEN, ENKAI.
- XU030 %40. Endeks, bayat bileşenler yüzünden ilk 5 dk'da hisselerden yavaş.

### 3.5 Kapanış (Görev 4)
Havuz (yaz günleri, 47 hisse, ~19.000 gözlem, 423 gün):

| y (ertesi gün) | CA | L30 (14:30–15:00) | DAY (O→14:30) |
|---|---|---|---|
| gap_{t+1} | −0,157 (t −3,7) | −0,017 (−0,3) | +0,034 (+2,9) |
| O→07:30_{t+1} | −0,192 (−3,8) | −0,021 (−0,3) | +0,014 (0,9) |
| gün-içi_{t+1} | −0,169 (−1,6) | +0,065 (0,5) | −0,013 (−0,4) |
| 07:30→C_{t+1} | +0,027 (0,3) | +0,086 (0,9) | −0,025 (−1,2) |

- Dönüş ertesi gün 07:30'da (10:30 TSİ) tamamlanıyor.
- Yıl boyu ölçülebilen LH (14:30→C) etkisiz, çünkü müzayede ve sürekli işlem karışıyor. Çeyrek sonlarında (12 gün) LH → gap −0,25 (t −3,0).
- Günlük 2014+ ay sonu etkisi tablo 0 #11'de; yıllara göre XU030 ay sonu gün-içi 13 yılın 9'unda negatif.

### 3.6 Gün-içi momentum (Görev 5)
- XU030: etkinin işareti tutarlı (sign stratejisi IS 4,1 / OOS 3,9 bps), ama regresyon eğimi OOS'ta sıfır.
- Gao vd.'nin "yüksek oynaklık günlerinde güçlü" bulgusu BIST'te tersine: |r_first| üst tercilinde b 0,014 (t 0,6), orta tercilde 0,149 (t 2,7).
- Bileşenler: gece gap'i r_last'ı tahmin etmiyor (0,012); etki O→07:30 parçasında (0,082, t 2,0).
- Hisseler: 0/47 FDR. Kesitsel arındırılmış: göreli gap son 30 dk'da hafif dönüyor (−0,019, t −3,0; ekonomik olarak önemsiz).

### 3.7 Backtest özeti (maliyet: gidiş-dönüş, işlem başına)

| BT | Strateji | IS brüt bps (t) | OOS brüt bps (t) | OOS işlem sayısı | OOS net 8 / 15 bps | Not |
|---|---|---|---|---|---|---|
| BT1 | 5 dk XU030 → 47, |z|>1,5, h=1, giriş O_{t+1} | 1,3 (medyan) | 1,5 (medyan) | 14.805 (toplam) | −6,5 / −13,5 | İllikitlerde 4–7 bps; IS'te seçilen hisseler OOS'ta tutmuyor |
| BT1 | XBANK → GARAN, |z|>1,5, h=3 | +1,9 (0,6) | −8,6 (−3,1) | 197 | — | Çökme |
| BT2 | Gap fade |gap|>1%, 47 hisse, E0 (2014+) | 28,0 (7,0) | 16,5 (2,8) | 11.665 | +8,5 / +1,5 | İllikit24 OOS 26,9 (3,9); likit23 3,1 (0,4) |
| BT2 | aynı, IS'te t>2 olan 14 hisse → OOS | — | 25,6 (3,4) | 3.277 | +17,6 / +10,6 | Seçim yanlılığı yok (IS seçimi) |
| BT2 | h1 dönemi E0 / E2 / E3 (47) | 22,0 / 20,1 / 15,2 | 25,5 / 21,1 / 15,3 (t 1,9 / 1,9 / 1,5) | 2.628 | E2: +13 / +6 | Gerçekçi giriş etkiyi azaltıyor |
| BT2b | Hisseye özgü gap fade, piyasa-nötr, E0 | 42,6 (10,7) | 24,2 (4,2) | 6.420 | +16 / +9 | XU030 vadelisi hedge maliyeti (~2–4 bps) ayrıca düşülmeli |
| BT2b | aynı, E2 (h1) | 20,1 (2,1) | 22,7 (2,3) | 1.404 | +14,7 / +7,7 | Ağu–Eki 2026: −1,8 |
| BT3 | Sektör yetişmesi |s|>1%, E0→C (2014+) | 25,3 (7,6) | 23,4 (4,7) | 7.378 | +15 / +8 | E2→C OOS 10,7 (1,2); E3→C 6,6 (0,8) |
| BT4 | XU030 14:30→C, sign(O→07:30) | 7,2 (3,0) | 3,75 (1,8) | 365 | net 2 / 4 bps: +1,75 / −0,25 | Endeks vadelisi; yıllar 2024 5,2 / 2025 3,2 / 2026 6,3 |
| BT4 | XU030, sign(r_first) | 4,1 (1,6) | 3,85 (1,9) | 365 | +1,85 / −0,15 (2/4 bps) | |
| BT5 | Kapanış müzayedesi dönüşü |CA|>25 bps, C→07:30_{t+1} | 11,7 (2,5) | 16,4 (4,1) | 3.362 | +8,4 / +1,4 | Vade sonu hariç 14,4 (4,5); illikit 18,7 (5,2) |
| BT5 | aynı, |CA|>50 bps | 17,9 (2,1) | 25,7 (3,5) | 811 | +17,7 / +10,7 | 2024 18,7 / 2025 25,4 / 2026 23,4 |
| BT5 | |CA|>0, C→O_{t+1} | 4,5 (2,6) | 6,3 (3,5) | 9.668 | negatif | Eşiksiz işlenemez |

## 4. Maliyet: VİOP pay vadelisi tiki ve spread

**Spot tik (fiyat kademeli):**
- Bugünkü fiyatlarda 47 hissenin medyanı 6,7 bps.
- Büyük tikliler: SASA 44, HEKTS 42, ODAS 14, PETKM/MGROS/OYAKC/ASTOR ~9,5 bps.
- Bu tikler 5 dk getirilerde fiyatı değişmeyen barları ve bayat fiyat etkisini doğrudan üretiyor.

**SSF tiki 0,01 TL** (bülten çıkarımı):
- Yüksek fiyatlı hisselerde <1 bps (ASELS, THYAO, TUPRS, BIMAS, MGROS 0,2–0,4).
- Orta fiyatlılarda 1–3 bps.
- Düşük fiyatlılarda büyük: TSKB 11, ODAS 21, HEKTS 58, SASA 63 bps. SASA/HEKTS SSF'lerinde 1 tik bile tüm gün-içi etkilerden büyük.

**SSF likiditesi** (6 bülten medyanı, TL hacim/gün):
- AKBNK 6,3 mlr, ASELS 6,1, YKBNK 5,9, THYAO 5,5, ISCTR 4,0, SAHOL 3,8 …
- Etkilerin yoğunlaştığı hisseler ise: DOAS 64 mn, OYAKC 98, VESTL 124, DOHOL 151, ULKER 159, HEKTS 160, SOKM 184, ODAS 205, ENJSA 227, TSKB 233, ARCLK 249, CIMSA 267 mn.

**Kotasyon verisi yok:**
- Roll tahmincisi 5 dk'da çoğu hissede tanımsız (pozitif 5 dk otokorelasyonu: ASTOR, VAKBN, VESTL, ISCTR).
- Varsayım (doğrulanmadı):
  - likit SSF (>1 mlr TL/gün): gidiş-dönüş 5–10 bps;
  - orta (300 mn–1 mlr): 10–20 bps;
  - illikit (<300 mn): 20–40+ bps, artı piyasa etkisi;
  - SASA/HEKTS: ≥60–120 bps.
- **Kendi bulgumun eleştirisi:** Gap fade, kapanış müzayedesi dönüşü ve 5 dk gecikme tam da bu illikit grupta güçlü. Likit yarıda gap fade OOS 3,1 bps, kapanış dönüşü 7,7 bps. Yani brüt bulgular gerçek ama net getirinin varlığı spread'e bağlı ve bilinmiyor.
- Endeks vadelisi (XU030D1!) maliyeti ~2–4 bps. BT4 ancak bu maliyetle sıfırın biraz üstünde.

## 5. Karşı argümanlar ve öz-eleştiri

1. **Açılış fiyatı = müzayede fiyatı.** E0 bu fiyattan sınırsız dolum varsayıyor; müzayede hacmi günlük hacmin ~%1–3'ü. E2'nin (h+l+c)/3 vekili, fade yönünde h/l'nin uç değerlerini içerebildiği için hafif iyimser olabilir. E3 (kesin 07:30 fiyatı) muhafazakâr alt sınır: 47 hissede OOS 15 bps, t 1,5, yani anlamlılık sınırında.
2. **Kapanış dönüşünün bir kısmı bid-ask sıçraması olabilir.** P15:00 son işlemi alış ya da satış fiyatında olabilir. Ama dönüş ertesi açılışta, yani müzayede fiyatı C'den sonra ölçülüyor. C, adil fiyatsa sıçrama dönüşü beklenmez; ölçülen şey müzayede fiyatının kendisinin geçici baskıyla oluşması. Yine de illikitlerde güçlü olması likidite primi/fiyat baskısı yorumuyla tutarlı, bilgi yorumuyla değil.
3. **C'den giriş.** 'Kapanış fiyatından işlemler' penceresi kısa (18:08–18:10 TSİ; kaynaklar 18:07/18:08 başlangıcı veriyor) ve sığ. SSF normal seansı 18:10'da bitiyor; SSF ile C'den işlem yok. Dolum ve kapasite belirsiz.
4. **5 dk örneklemi 60 gün ve olağandışı** (fon krizi, yüksek oynaklık). Bu ölçekteki tüm sonuçlar en fazla DÜŞÜK. "Gecikme yok / işlenemez" olumsuz sonucu ise h1 ile tutarlı.
5. **Mekanik içerme.** XU030 hedefi içeriyor. Lag-1 etkisi diğer 29 bileşenden geliyor; hedefin XU030 ağırlığı senkron korelasyonu şişirir, gecikmeli katsayıyı şişirmez. XBANK → GARAN'da GARAN XBANK'ın içinde; ama AKBNK→GARAN ve ISCTR→GARAN da aynı yönde.
6. **Çoklu test.**
   - 5 dk: 1.482 Wald testi (ileri + ters). Ayrıca ~15 varyant, hisse başına değil özet olarak.
   - h1: 1.482 test.
   - Gap fade: 6 eşik × 47.
   - Sektör: 4 hedef × 47.
   - Kapanış: 8 × 47.
   - Momentum: 9 × 51.
   - BH-FDR her aile içinde ayrı uygulandı; aileler arası düzeltme yapılmadı.
   - Gap fade ve kapanış dönüşünde IS/OOS replikasyonu ve yıllık kırılım var. 5 dk sektör çiftleri OOS'ta çöktü (aşırı uyum uyarısı).
7. **Rejim bağımlılığı.** Gap fade 2025'te ≈0. Mart 2025 ve Ekim 2026 gibi toplu şok günlerinde gap'ler devam ediyor. Ay başı/ay sonu etkisi yalnız 2021+ döneminde (yüksek enflasyon, KKM, fon akımları); IS'te yok.

## 6. Sınırlamalar / yapılmadı / açık sorular
- VİOP pay vadelisi gün-içi fiyat ve kotasyon verisi yok. SSF'nin spot açılıştan önceki 30 dk'da (09:30–10:00) gap'i ne kadar fiyatladığı ve gerçek spread ölçülemedi. Bu, gap fade'in SSF'de uygulanabilirliği için kritik.
- Kış aylarında h1'de 14:30–15:00 eksik, bu yüzden CA ve son 30 dk testleri yalnız yaz günlerinde. m5'te kış verisi yok.
- Fiyatı değişmeyen bar dışında işlem sayısı / emir defteri yok. Bayat fiyat ayrıştırması dolaylı (bar içi getiri, hacim alt örneklemi).
- XLBNK ve XHOLD'un günlük Yahoo geçmişi yok; açılış/kapanış testlerinde kullanılmadı.
- Endeks dönem değişimi (çeyrek sonu) ile vade sonu çakışıyor. 12 çeyrek sonu günüyle ayrıştırma zayıf.
- Açık sorular:
  1. Gap fade ve kapanış dönüşü likit 10 SSF'de net kârlı mı? Gerçek kotasyon gerekiyor.
  2. Açılış müzayedesinde yayımlanan teorik fiyatla müzayede içi giriş (E0) ne kadar gerçekçi?
  3. Ay başı etkisi 2027'de sürecek mi (rejim)?

Kaynaklar (birincil/ikincil):
- Uzlaşma ve son işlem günü: [Borsa İstanbul VİOP pay vadeli duyurusu 20076](https://borsaistanbul.com/files/duyuru-20076-tr.pdf), [VİOP tanıtım kitapçığı](https://borsaistanbul.com/files/VIOP_Tanitim_Kitapcigi_Vadeli_Islem_Sozlesmeleri.pdf). Pay vadelisinde son işlem günü = ayın son iş günü, uzlaşma = spot kapanış seansı fiyatı; bülten ile 47/47 doğrulandı.
- Kapanış fiyatından işlemler penceresi: [Garanti BBVA BIST işlem saatleri](https://www.garantibbva.com.tr/borsa-hisse-senetleri/bist-islem-saatleri), [QNB Invest](https://www.qnbinvest.com.tr/hisse-senedi-islem-saatleri). İkincil kaynaklar; BIST'in güncel duyurusuyla teyit edilmeli.
- VİOP akşam seansı kapsamı: 1. tur `r1_gunici.md` (duyuru 30572).
