# r1_gunici — Gün-içi, zaman dilimi ve VİOP akşam seansı (ajan: gunici)
Tarih: 02.11.2026 · Veri: h1 2023-12…2026-10 (ES/NQ/BZ/GC h1 2024-06'dan, BTC h1 2024-11'den), m5 son 60 BIST günü (ES m5 ~50 gün: 21.08–30.10.2026)
Kod: `out/code_gunici/` (g_common.py, t1_overnight.py, t1b_drift.py, t2_m5_leadlag.py, t46_asia_weekend.py, z_build_csv.py; ara sonuçlar `results/`). Bulgular: `out/f_gunici.csv` (1.934 satır).

## 0. Net bulgular tablosu

| # | Bulgu | Rakam | İşlenebilir mi? | Güven |
|---|---|---|---|---|
| 1 | Gece ES=F (15:00→07:00 UTC) → BIST açılış gap'i | XU030 corr 0,45 (t 6,8), β 0,43; IS 0,45 / OOS 0,44. 47 hisse medyan 0,36 (bankalar 0,45–0,50; SASA/ENJSA/ASELS ~0,2) | HAYIR: açılış müzayedesinde fiyatlanıyor | YÜKSEK (ilişki) |
| 2 | Gece sürücü sepeti (ES, BZ, GC, TRY, TUR, DAX-kalan) gap'in ne kadarını açıklıyor | R² XU030 0,28, XBANK 0,39, GARAN 0,40, AKBNK/YKBNK 0,39; düşük: SASA 0,07, ENJSA/DOAS/AKSEN ~0,09; +BTC ile R² +0,01…0,09 | HAYIR | YÜKSEK/ORTA |
| 3 | Gap açıldıktan sonra devam/dönüş (07:30→kapanış) | 612 (hisse×sürücü) gün-içi testinin **0'ı** FDR'den geçiyor. Tahmini gap → 07:30-kapanış medyan corr 0,03; XU030 0,09 (t 1,8) | Maliyet sonrası YOK | ÇOK DÜŞÜK |
| 4 | Gap'in açıklanamayan kalıntısı ilk 30 dk'da kısmen dönüyor | corr(açılış→07:30, kalıntı) medyan −0,10; hisselerin %23'ünde açılış→kapanış t<−2; 07:30 sonrası medyan −0,03 | Sadece açılış müzayedesi fiyatıyla; 8 bps sonrası ~0 | DÜŞÜK |
| 5 | Gece/gün-içi ayrışması: ortalama gap > 0, gün-içi < 0 | XU030 2014–2026 gap 13/13 yıl pozitif (ort. +10…+31 bps/gün), gün-içi 11/13 yıl negatif (−2…−22 bps). 2024–26'da hisselerin %87–94'ünde gün-içi negatif | XU030 "açılışta sat/kapanışta kapat": brüt +11 bps/gün (t 2,2), 8 bps sonrası +3; endeks vadelisinde (~2–4 bps) belki | ORTA (endeks), DÜŞÜK (hisse) |
| 6 | TUR (BIST kapanışı sonrası 15:30→ABD kapanışı) → gap; ES'e EK bilgi | corr(XU030) 0,32 (t 6,1); kısmi(TUR\|ES) 0,15 XU030, hisselerde medyan 0,10 (%51'inde >0,10). TUR→XU030 gün-içi t 2,5 (FDR'den geçmiyor) | HAYIR (pay); endeks vadelisi akşam seansında kısmen | ORTA |
| 7 | TKC ADR → TCELL gap | corr 0,15 (t 2,8) vs ES 0,45; kısmi(TKC\|ES,TUR) −0,02 | HAYIR, ek bilgi yok | DÜŞÜK |
| 8 | DAX/Stoxx 15:00→Avrupa kapanışı → gap | XU030 corr 0,05 (t 1,1); kısmi(DAX\|ES) −0,06 | — ES zaten kapsıyor | ÇOK DÜŞÜK |
| 9 | Brent gece → BIST gap: rejim değişimi | Tam −0,23; IS (≤06/2025) +0,03, OOS −0,45 (XBANK OOS −0,57) | HAYIR | DÜŞÜK (rejim; istikrarsız) |
| 10 | Akşam seansı pencereleri: ES'in 20:00–07:00 UTC kısmı (VİOP kapalıyken) gap'i en çok açıklayan kısım | XU030 β: 15–16 UTC 0,28 (t 3,5), 16–20 UTC 0,29 (t 8,1), 20–07 UTC 0,63 (t 4,7). R²: 15–20 UTC tek başına 0,067; 20–07 UTC 0,196 | Akşam seansı bilginin ~1/4'ünü görebilir, kalanı yine açılışta | ORTA |
| 11 | 5 dk lead-lag ES/NQ/BZ/GC/TRY/DAX → XU030 ve 47 hisse | XU030–ES lag0 0,17, lag1 0,00; gecikmeli pay (Σβ1..6/Σβ) 0,08 (t 0,4). Hisselerin %0'ında Σβ1..6 t>2. ABD açılışı penceresinde de (13:30–14:55) lag1 −0,01 | YOK: ES şoku sonrası brüt 0–2 bps/işlem, maliyet 3–15 bps | ÇOK DÜŞÜK (olumsuz bulgu, ~50 gün) |
| 12 | Asya: N225/KOSPI/Şanghay gün getirisi → gap | XU030: N225 0,42 (t 4,7), KS11 0,33, SSE 0,18 (hepsi açılıştan önce bilinir) | HAYIR (gap) | ORTA |
| 13 | Asya'nın BIST açılışından SONRAKİ kısmı: HSI 07:30→kapanış → BIST 08:30→kapanış | XU030 corr 0,04 (t 1,1); kısmi(\|ES 07:00–08:30) 0,006; OOS brüt +10 bps (t 1,6) | Hayır/zayıf | ÇOK DÜŞÜK |
| 14 | BTC hafta sonu → Pazartesi gap (bireysel ağırlıklı) | Uzun örneklem 2015+: TRALT 0,19 (t 3,3), ASTOR 0,21 (t 2,8, n 189), HEKTS 0,11 (t 2,5), SASA 0,07, ODAS 0,06, PETKM 0,04; 2021+ daha güçlü (0,12–0,29). Hafta sonu c ≈ hafta içi gece c (h1: 47 hisse medyan 0,22 vs 0,22) → hafta sonuna özgü değil | HAYIR (gap); Pazartesi gün-içi devam yok | DÜŞÜK |
| 15 | VİOP akşam seansı (19:00–23:00 TSİ = 16:00–20:00 UTC): PAY VADELİLERİ YOK | Birincil kaynak: Borsa İstanbul duyuru 30572 (19.11.2024) | Kapanış sonrası bilgi pay vadelisinde açılışa kadar işlenemez | YÜKSEK (kaynaklı) |

## 1. VİOP akşam seansı (Görev 5) — birincil kaynaklar
- **Saatler:** Akşam seansına dahil sözleşmelerde günlük akış "09:20-18:10 & 19:00-23:00" (açılış seansı 09:20, sürekli müzayede 09:30, normal seans sonu 18:10, AS öncesi 18:50, AS sürekli müzayede 19:00, AS sonu 23:00). Yarım günlerde ve takvim yılının son işlem gününde akşam seansı yapılmaz. Kaynak: [Duyuru 15626, 06.03.2023 (Ek-3)](https://borsaistanbul.com/files/duyuru-15626-tr.pdf); önceki hâli [Duyuru 11326, 21.09.2022](https://www.borsaistanbul.com/files/duyuru-11326-TR.pdf) — burada "Pay Türev Pazarı 09:30-18:10" açıkça **"Akşam Seansına Dahil Olmayan Sözleşmeler"** tablosunda.
- **Kapsam (güncel prosedür md. 7, aynen):** "Akşam seansında BIST 30 Endeks, BIST Likit Banka Endeks, BIST Banka Dışı Likit 10 Endeks, BIST Sürdürülebilirlik 25 Endeks, Dolar/Ons Altın, Dolar/Ons Gümüş, Dolar/Ons Platin, Dolar/Ons Paladyum ve Dolar/Ton Bakır Vadeli İşlem Sözleşmeleri işlem görür." — [Duyuru 30572, 19.11.2024](https://borsaistanbul.com/files/duyuru-30572-TR.pdf). **Pay vadelisi yok; USD/TL, EUR/TL ve TL/gram altın vadelisi de listede yok.**
- **Başlangıç:** Planlama duyurusu 2019/73 ([18.11.2019](https://borsaistanbul.com/duyuru/11414/viopta-devreye-alinmasi-planlanan-aksam-seansi-uygulamasi-duyurusu)); uygulama 17.01.2020'de, ilk etapta yalnız endeks vadelileriyle başladı (ikincil: [Ekonomist](https://www.ekonomist.com.tr/borsa/borsa-istanbul-viopta-yeni-donem-uygulama-bu-aksam-basliyor-8612)). Ons metaller sonra eklendi, bakır 06.12.2024'te.
- 2025–2026 VİOP duyurularında (41504 28.11.2025, 42281 23.12.2025, 47594 22.05.2026) pay vadelisinin akşam seansına eklendiğine dair bir ifade bulamadım. Prosedürler sayfası (borsaistanbul.com/tr/sayfa/146) erişim sırasında 503 verdi, yani güncel prosedürün tam metni ayrıca kontrol edilmeli. Savunma ajanının bulgusuyla uyumlu.
- **Sonuç:** 47 pay vadelisi için ABD seansı bilgisi (BIST kapanışı 15:10 UTC sonrası) **sadece ertesi sabah** işlenebilir. VİOP pay vadelisi 09:30 TSİ'de, yani spot (10:00) piyasadan 30 dk önce açılır. Bu yarım saat spot açılış müzayedesine karşı "ilk fiyatlayan" piyasadır (bu veriyle test edilemedi). XU030/XLBNK endeks vadelileri 16:00–20:00 UTC (yaz) penceresinde işlem görür. Kışın ABD kapanışı 21:00 UTC olduğu için son ABD saati bunun dışında kalır.
- **Rakamla anlamı (Bulgu 10):** XU030 gap'inin ES ile açıklanan kısmının yaklaşık %25–30'u akşam seansının görebildiği pencerede (15:00–20:00 UTC; R² 0,067), %70'i 20:00–07:00 UTC'de oluşuyor (R² 0,196). Kısmen kış ABD son saati, kısmen Asya seansı. Akşam seansı endeks vadelisi bilginin bir kısmını gece fiyatlar, gerisi her durumda açılışa kalır.

## 2. Yöntem
- **Bar yapısı (kendim doğruladım):** BIST h1 06:30 barı = 06:55 açılış müzayedesi + 07:00–07:30; 14:30 barı 30 dk; 15:00 kapanış müzayedesi barı sadece son günde var. **Kış aylarında (AB yaz saati dışında) h1 verisinde 14:30 barı yok**, 14:30–15:10 arası eksik. Kanıt: kışın son bar ile kapanış arasındaki medyan fark %0,30, yazın 14:30 fiyatı ile kapanış arasındaki fark %0,27. Bu yüzden ABD açılışı örtüşmesi için h1 kullanılmadı, m5 kullanıldı (m5'in tamamı yaz). **Endekslerde h1 ilk bar 'o' = önceki kapanış**, açılış değil. Açılış günlük 'o'dan alındı (m5 06:55 barının 'c'si ile aynı). Hisselerde h1 ilk 'o' = günlük 'o'.
- **Gece penceresi:** önceki BIST günü 15:00 UTC → bugün 07:00 UTC (h1 snapshot; bar bitiş zamanına göre). ABD ETF'leri (TUR/TKC/EEM) için 15:30 UTC → ABD kapanışı, Avrupa için 15:00 → Avrupa kapanışı. Yarım günler ve sonraki günler hariç. Gap = ll.decomp (temettü düzeltmeli).
- **Gün parçaları:** r30 = açılış→07:30, r1 = açılış→08:30, rest = 08:30→kapanış, r_0730_close.
- **Devam/dönüş:** genişleyen pencereli OLS ile tahmini gap (look-ahead yok, en az 120 gözlem). Kalıntı = gap − tahmin.
- **Backtestler** (IS < 2025-07-01 ≤ OOS; maliyet 0/8/15 bps gidiş-dönüş):
  - BT1 sign(tahmini gap), giriş 07:30;
  - BT2 −sign(kalıntı), giriş açılış (iyimser) veya 07:30;
  - BT3 sign(ES gece), giriş 07:30;
  - BT4 −sign(gap);
  - BT5 açılışta sat/kapanışta kapat;
  - BT6 5 dk ES şoku (z = 1/2/3 σ, h = 1/3/6 bar, örtüşmesiz; 1. ve 2. yarı);
  - BT7 HSI-late → 08:30-kapanış;
  - BT8 sign(BTC hafta sonu) × Pazartesi gün-içi.
- **Çoklu test:** gap 612 testin 382'si BH-FDR'den geçiyor; gün-içi 612 testin 0'ı geçiyor.

## 3. Kanıt ayrıntıları
**BT1–BT5 (47 hisse medyanı, 8 bps sonrası; OOS):**
- BT1 tahmini gap ile devam: IS +16,9, OOS −6,6 bps.
- BT2 kalıntı dönüşü (07:30): OOS −7,9 bps. Açılıştan girişte, 0,5σ eşikle OOS +14,3 bps (t 0,7). Bu, açılış müzayedesi fiyatından işlem varsayar ve anlamlı değil.
- BT3 ES gece devamı: OOS −1,8 (0,5σ eşikle +3,4) bps.
- BT4 gap dönüşü: OOS −1,1 bps.
- BT5 açılışta sat: hisselerde OOS +7,4 bps (t 0,6).
- XU030 tarafında:
  - BT3 IS +9,2 / OOS −2,8 bps;
  - BT1 IS +22,8 / OOS −6,6 bps;
  - BT5 brüt IS +14,1 / OOS +7,5 bps (8 bps sonrası ≈0; endeks vadelisi maliyetiyle ~+4).

Kısacası IS'teki devam sinyali OOS'ta kayboluyor.

**5 dk (Görev 2):** 5 dk getiri oynaklığı XU030 15,5 bps, hisse medyanı 23 bps. ES şoku (z=3, h=3) sonrası XU030 brüt +4,8 bps (t 1,5, n 75), hisse medyanı +3,8 bps. Endeks vadelisi maliyeti (~2–4 bps) ile bile sınırda, SSF maliyetiyle (8–15 bps) negatif. preUS z=3 h=6 +19,8 bps (n 18) aşırı küçük örneklem. Not: XU030 spot endeksi son işlem fiyatlarından hesaplanıyor. Endekste görülecek bir gecikme bile vadeliye aktarılamayabilir, ama zaten gecikme yok.

**Spread:** Gün-içi 5–30 dk'lık stratejilerde beklenen brüt kazanç 0–5 bps. Bu, SSF yarım spread'inin (likit hisselerde ~2–5 bps, illikitlerde 10+ bps) altında. Gece/gün-içi stratejilerde 8 bps maliyet brüt kazancın tamamını yiyor.

## 4. Karşı argümanlar / öz-eleştiri
- **Bulgu 5:** Açılış fiyatı müzayede fiyatıdır. Gerçek işlem 10:00'da SSF fiyatından yapılır ve SSF bazı/açılış primi farklı olabilir (VİOP verisi yok). Gün-içi negatif ortalama kısmen kapanış müzayedesinin etkisi ve 2023–2025 TL/likidite rejimi olabilir. 2017 ve 2022'de işaret ters döndü.
- **Bulgu 9 (Brent):** Brent'in işareti 2025 ortasında değişti. Bu, olay odaklı bir rejim (petrol arz şoku = TR için risk-off) olabilir ya da örneklem gürültüsü. Yıllara göre kırılım yapılmadı.
- **Gece R²:** ES'in başka bilgileri de taşıması (küresel risk, TL haberleri vb.) nedensellik kanıtı değildir.
- **Örneklem:** h1 sonuçları ~2,4–2,9 yıl, m5 ~50 gün. BTC h1 hafta sonu n ≈ 96. Bu yüzden m5 bulgularının tamamı en fazla DÜŞÜK güvende. "Lead-lag yok" sonucu ise güvenilir bir olumsuz sonuçtur: lag0 her yerde güçlü, lag1 sıfır.

## 5. Sınırlamalar / yapılmadı
- VİOP vadeli fiyat verisi (normal ve akşam seansı) yok. Akşam seansının gece bilgisini ne kadar fiyatladığı doğrudan ölçülemedi; ES alt pencereleriyle dolaylı ölçüldü.
- Kış h1 verisinde son 40 dk eksik. ABD açılışı örtüşmesinin kış (14:30 UTC) versiyonu test edilemedi (m5 tamamen yaz).
- Görev 4 ve 6 kısa tutuldu: yıllara göre kırılım, FDR ve gün-içi maliyet hassasiyeti yapılmadı. Brent rejiminin yıllara göre kırılımı da yapılmadı.
- TradingView kodları aday. HKEX (^HSI) açılmayabilir. Çin için önerilen alternatifler: FX:USDCNH (test edildi: 07:00–08:30 → BIST etkisi yok), AMEX:ASHR/FXI/MCHI (ABD saatinde işlem görür, gece sürücüsü olarak kullanılabilir; burada ayrıca test edilmedi), SGX:CN1! (A50 vadelisi, '?').
