# ry_viop: VİOP bülten geçmişi, işlenebilirlik/likidite ve VİOP kaynaklı lead-lag (ajan: viop)

Tarih 02.11.2026. Veri: Borsa İstanbul günlük VİOP bülteni, **2017-03-06 → 2026-10-30, 2.422 işlem günü, eksik gün yok**. 2017-03 öncesi sunucuda 404. 102 hafta içi gün 404 döndü; bunlar tatil. Spot taraf ll.py v4 (02.11 12:02 rejim/bayat-gün düzeltmesi) ile tam yeniden üretildi.
Kod: `out/code_y_viop/` (`run_all.sh` hattı baştan çalıştırır). Bulgular: `out/f_y_viop.csv` (234 satır). Likidite tablosu: `out/y_viop_likidite.csv` (53 dayanak).

**Diğer ajanlar için ortak veri**
- `data/viop/viop_YYYYMMDD.csv`: ham bülten.
- `data/viop_panel.parquet`: tüm vadeli seriler, 531 bin satır. Sütunlar: date, code, root, und (KOZAL→TRALT, KOZAA→TRMET), expiry, settle, prev_settle, open, low, high, close, vwap, value_tl, qty, trades, oi, oi_chg, os_* (açılış seansı, 23.09.2022+), mult.
- `data/viop_opt_agg.parquet`: opsiyonlar dayanak × gün × C/P bazında.
- `out/code_y_viop/results/rates.parquet`: USDTRY takvim yayılımından örtük TL faizi.
- `results/daily_all.parquet`: ön vade, 2. vade ve t-1 AP'ye göre seçilmiş "L" sözleşmesi; spot ile birleşik.

## 0. Net bulgular

| # | Bulgu | Rakam | İşlenebilir mi? | Güven |
|---|---|---|---|---|
| 1 | **Bülten fiyatları akşam seansını İÇERMİYOR.** Açılış = 09:30 açılış seansı (2026'da %100 eşit), yüksek/düşük/kapanış ise gündüz seansı. | XU030 "yüksek fazlası"nın ES akşam yoluna (16–20 UTC) eğimi 0,08 (t 1,7). Akşam seansı olmayan THYAO'da 0,18 (t 2,9), yani XU030'da fazladan etki yok. Kapanış−uzlaşma farkının ES akşamıyla korelasyonu 0,003. Bülten 19:45–20:55 TSİ'de üretiliyor. | Akşam seansı getirisi bültenle **ölçülemez** | YÜKSEK |
| 2 | Akşam seansının görebildiği bilgi payı (ES vekili, 2024-06+) | XU030 vadeli gece getirisi (uzlaşma→09:30): ES_akşam β 0,42 (t 9,8), ES_gece β 0,59 (t 7,4). R²: yalnız akşam 0,167, yalnız gece 0,208, ikisi birlikte 0,379. Akşam ES → ertesi vadeli gün-içi β −0,10 (t −0,6). | Akşam penceresi açıklanan gece varyansının ~%44'ünü endeks vadelisinde akşam seansında işlenebilir kılıyor. Ertesi güne kalan öngörü YOK. | ORTA |
| 3 | **Baz anomalisi → ertesi spot açılış gap'i** (kesitsel FM, kontrollü) | +5,2 bps/sd (t 12,6). IS 5,4 (t 9,4), OOS 4,8 (t 8,7). Hisselerin %90'ında işaret pozitif. 9 hisse YÜKSEK (DOHOL, SAHOL, BIMAS, ASELS, TCELL…). | HAYIR: gap'te fiyatlanıyor | YÜKSEK (bilgi) |
| 4 | **Baz anomalisi → ertesi vadeli gün-içi** (pahalı vadeli ucuzluyor) | −7,2 bps/sd (t −7,3). IS −7,2 (t −5,1), OOS −7,2 (t −5,4). A/B likit −6,1 (t −5,5). Uzlaşma→uzlaşma −12,9 (t −11,5). | Yalnız açılış fiyatından girilirse (bkz. BT1) | YÜKSEK (ilişki) / DÜŞÜK (işlem) |
| 5 | BT1: baz anomalisi L/S (üst/alt %20), vadeli 09:30 açılış → kapanış | BRÜT +24,2 bps/gün (t 9,1), 10/10 yıl pozitif. NET +6,4 (t 2,4): IS +8,2, OOS +3,6 (t 1,0, Sharpe 0,5). Muhafazakâr maliyetle +0,4. **VWAP(t+1)→VWAP(t+2) girişte brüt +6,7, net −11.** Kenarın çoğu açılış basılı fiyatında. Açılış seansı medyan hacmi THYAO 0,56 mn TL, DOAS 41 bin TL. | Kapasite çok düşük. Net, maliyet varsayımına çok duyarlı. | DÜŞÜK |
| 6 | Pay vadelisi **hacim sürprizi** → ertesi gün: açılışta devam, gün içinde dönüş | Spot gün-içi −4,6 bps/sd (t −5,7; IS t −4,1, OOS t −4,1). Gap +2,2 (t 6,1). BT2 L/S brüt +10,4 bps/gün (t 4,1, 10/10 yıl). NET −7,8. | Maliyet (~18 bps L+S) kenarı aşıyor | ORTA (ilişki) / DÜŞÜK (işlem) |
| 7 | **AP değişimi** → ertesi vadeli getiri | −3,2 bps/sd (t −3,9; IS −2,7, OOS −3,0). "AP↑+fiyat↑ = yeni long → devam" kuralı DESTEKLENMİYOR (r×dOI t 0,1). Hisse bazında 1.444 testten 2'si FDR'den geçiyor. | Hayır (BT2b net −8) | ORTA (zayıf etki) |
| 8 | Vadeli 09:30 açılışı → spot 09:55/10:00 açılış gap'i | β medyan 0,64, R² medyan 0,31 (0,16–0,66). XU030 β 1,02, R² 0,47. Kalıntı → spot gün-içi: medyan t −1,2, hisselerin %17'sinde t<−2. BT4 net negatif. | Spot açılışı vadeliyi zaten fiyatlıyor; gün-içi kalıntı ~0 | YÜKSEK (öncülük) / ÇOK DÜŞÜK (işlem) |
| 9 | XU030 vadeli 18:15 son fiyatı (spot 18:10'dan 5 dk sonra) → ertesi spot gap | β 0,45 (t 2,8) | Vadeli gece getirisine etkisi yok (t −1,1), yani işlenemez | ORTA |
| 10 | XU030 vadeli gece/gün-içi ayrışması (gerçek vadeli fiyatlarıyla) | Gece long (18:15→09:30) brüt +5,0 bps (t 5,2; 9/10 yıl; IS +3,4, OOS +7,4). Gün-içi short brüt yalnız +2,7 (t 0,8). Spottaki "gün-içi<0" (1. tur) vadelide büyük ölçüde yok. | NET ≈ 0 (maliyet 4,8 bps/işlem) | DÜŞÜK |
| 11 | Temettü beklentisi bazda tam fiyatlanmış | Örtük temettü ~ gerçekleşen: eğim 1,02 (t 31,5), R² 0,86, n 3.230, 41 hisse. Temettüsüz günlerde (r·τ − baz) medyan −0,5 bps. | Bilgi (USDTRY örtük faizi taşımayı iyi açıklıyor) | YÜKSEK |
| 12 | Vade sonu yakınsaması | Anomali sapması günde %40 kapanıyor (hisse, yarı ömür ~1,4 gün). XU030 %18 (~3,5 gün). Pay vadelisi vade sonu uzlaşması = spot kapanış, 2021+ %100 birebir. | — | YÜKSEK |

## 1. Likidite / işlenebilirlik (`y_viop_likidite.csv`)
**Doğrulanan sözleşme özellikleri.** Bültendeki hacim/(adet×VWAP) çarpanından ölçüldü ve kaynaklarla teyit edildi:
- Pay vadelisi **100 pay** ([BIST tanıtım kitapçığı](https://borsaistanbul.com/files/VIOP_Tanitim_Kitapcigi_Vadeli_Islem_Sozlesmeleri.pdf)).
- Endeks vadelisi 10 TL × endeks. 27.07.2020 öncesi fiyat endeks/1000 idi; panelde ×100 ile ölçeklendi.
- USDTRY 1.000 USD, gram altın 1 gr.

**Tik büyüklüğü (koordinatör sorusu).** "0,01 TL" bugün **yalnız 100 TL altı paylar** için doğru. 02.12.2024'ten beri pay vadelisinde bantlı tik var: <100 TL: 0,01; 100–500: 0,05; 500–1000: 0,1; 1000–2500: 0,25; ≥2500: 0,5. Endeks tiki 0,25'ten 1,00'a, USD/TL tiki 0,001'e, gram altın tiki 0,10'a çıktı ([Halk Yatırım genelgesi, BIST duyurusuna atıf](https://halkyatirim.com.tr/download/viop2911.pdf)).
- **Bültenle ampirik teyit:** 02.12.2024 öncesi fiyatların %100'ü 0,01 ızgarasında. Sonrasında 100–500 TL bandındaki fiyatların %100'ü 0,05 katı (öncesinde bu oran %40'tı). XU030 fiyatlarının 2024-12 sonrası %100'ü tam sayı.
- Tikin bps karşılığı fiyatla değişiyor. Son fiyatla: SASA 1,45 TL → **69 bps**, HEKTS 1,60 → 62,5, ODAS 4,25 → 23,5, TSKB 11,2, ISCTR 8,6. 12 ay medyan fiyatla: 39 / 32 / 16 / 8,3 / 7,1 bps. gunici_y'nin 63/58/21 değerleri bu ikisinin arasında, yani dönem farkından kaynaklanıyor.
- Ayrıca **100 TL'nin hemen üstünde** tik 0,05'e çıkıyor (~5 bps). TCELL 12 ay medyanı 4,5 bps, şu an (90 TL) 1,1 bps.

**Maliyet yöntemi.** Günlük H-L tahmincileri likit sözleşmelerde oynaklıktan şişiyor (Corwin–Schultz 50–120 bps, Abdi–Ranaldo çoğunlukla 0, Roll gürültülü). Bu yüzden yalnız karşılaştırma sütunu olarak tutuldu.
- Spread = max(1 tik, σ_gün/√N_işlem). Bu, Wyart–Bouchaud vd. (2008) spread–oynaklık yasası. Muhafazakâr sürüm: max(1,5 tik, 2σ/√N).
- Komisyon: kurumsal onbinde 2 + %5 BSMV ≈ 2,1 bps/yön (borsa payı dahil varsayıldı). Bireysel tarife (onbinde 10) ayrı sütunda.
- Piyasa etkisi (1 mn TL): 2 × 0,5 σ √(Q/ADV).

**Özet (son 252 gün)**
- **A sınıfı (≥1 mlr TL/gün):**
  - XU030: 43,6 mlr TL, 97,6 bin işlem, gidiş-dönüş (RT) **4,8 bps**.
  - USDTRY: 16,8 mlr TL, 4,4 bps.
  - AKBNK: 4,0 mlr TL, 5,6 bps.
  - THYAO: 3,7 mlr TL, 5,9 bps.
  - ASELS 3,4 mlr; YKBNK 3,0 mlr; ISCTR 2,8 mlr (tik nedeniyle 11,3 bps); ASTOR, TUPRS, KCHOL, GARAN (7,9), TRALT, EREGL, SAHOL, BIMAS, EKGYO, TCELL.
- **B sınıfı (19 hisse, 250 mn–1 mlr TL):** RT 6,6–9,8 bps.
- **C sınıfı (13 hisse):**
  - DOAS 70 mn TL/gün, 1.887 işlem, RT 9,3 bps.
  - Tik cezalı düşük fiyatlı paylar: SASA RT 43, HEKTS 36, ODAS 20 bps.
- **D sınıfı:** X10XB günde 3,4 mn TL / 10 işlem (RT ~56 bps). XSD25'te 12 ayda **hiç işlem yok**. XLBNK 712 mn TL/gün, RT 9,6 bps (B).
- **47 hisse geneli:** küçük emirde RT medyanı **7,3 bps** (çeyrekler arası 6,7–8,7). 1 mn TL emirde medyan 18,7 bps. Bireysel komisyonla medyan 24 bps.
- **Brifingdeki 8–15 bps varsayımı:** A/B için biraz muhafazakâr kalıyor. C sınıfı ve 1 mn TL+ emirlerde ise iyimser.

**En likit vade ve geçiş.**
- Günlerin %95'inde en likit vade ön vade. Hacmin ~%80'i ön vadede.
- Geçiş son 1–2 günde oluyor. Ön vadenin hacim payı 5 iş günü kala ~%85, 1 gün kala ~%60, vade günü ~%44.
- USDTRY'de hacim aylara dağınık (ön vade payı %52).
- Açılış seansı hacmi toplam hacmin yaklaşık onbinde 1–7'si. Açılış fiyatından işlem kapasitesi buna göre küçük.

## 2. Yöntem notları
- **Faiz:** r_TL = ln(F2/F1)/(τ2−τ1) + r_USD (^IRX). F1/F2 aynı bültenin USDTRY ön ve 2. vade uzlaşmaları; 5 günlük medyan alındı. Yıllık ortalamalar: 2017 %11,6 → 2024 %44,7 → 2026 %34,8. TLREF1M vadeli uzlaşmaları işlemsiz ve sabit (36,49), bu yüzden kullanılmadı.
- **Baz:** b = ln(F_L,uzlaşma / S_kapanış). Yahoo bölünme düzeltmeli spotun ölçeği vade sonu günlerinde kalibre edildi (pay vadelisi vade sonu uzlaşması = spot kapanış).
- **Teorik baz:** b* = r·τ − Σ temettü. Temettü, Yahoo adj/c sıçramasıyla (vade+7 gün içinde) belirlendi.
- **Anomali:** (b − b*) eksi kendi geçmiş 60 gün medyanı (t hariç). "nodiv" sürümünde temettü penceresi dışlandı; sonuçlar aynı.
- **AP:** dOI = Σoi_chg / Σ(oi − oi_chg). Yalnız t'de listelenen seriler sayıldı, böylece vade dolumu mekanik düşüş yaratmıyor; vade günleri dışlandı.
- **Hedefler:** spot gap / gün-içi / cc (ll.decomp; endekslerde tam takvim) ve vadeli uzlaşma, kapanış, gün-içi (aynı sözleşme).
- **Testler:**
  - Fama-MacBeth: günlük kesit OLS, sinyaller sıra-normalize; eğimlerin NW t'si.
  - Kontroller: spot r_t ve vadeli r_t (baz için); r_t (AP için).
  - Hisse bazında TS-OLS (NW-5) + BH-FDR. Baz: 1.152 test, 201 geçti (çoğu mekanik kapanış sıçraması içeren anom_close sürümü). AP/hacim: 1.444 test, 2 geçti.
- **IS / OOS:** IS 2017-04…2022-12, OOS 2023-01…2026-10. Yön IS işaretinden seçildi.
- **Liste tarihleri:** 20 hisse 2017'den beri listeli. BRSAN 2024-04, CIMSA/DOAS 2024-02, ASTOR 2023-07 (kısa örneklem, güven bir kademe düşürüldü).

## 3. Kanıt ayrıntısı
**Akşam seansı.** Kural metinleri: akşam seansı işlemleri ertesi işlem gününün takasına giriyor ve uzlaşma hesabına girmiyor; baz fiyat, gündüz seansı uzlaşması ([BIST duyuru 30572](https://borsaistanbul.com/files/duyuru-30572-TR.pdf)). Seans saatleri ([duyuru 05.05.2022](https://www.borsaistanbul.com/files/viop-acilis-seansi-ve-pay-vis-ops-seans-sonu-deg-hk-duyuru.pdf)):
- Açılış seansı 09:20–09:30.
- Pay vadelisi normal seans 18:10'da, diğer sözleşmeler 18:15'te bitiyor (23.09.2022'den beri).

Testler (04_evening.py):
- (i) Vadeli gece getirisi hem akşam hem gece ES'ine yükleniyor; pay vadelisi kontrolüyle aynı desen.
- (ii) Yüksek/düşük fazlasında akşam yolu etkisi yok.
- (iii) Aynı gün bülteninde akşamın ilk 2 saati de yok (korelasyon −0,16 / −0,01).

Sonuç: "akşam seansı getirisi → ertesi açılış" doğrudan test edilemedi. Bunun için TradingView BIST:XU030D1! gün-içi verisi gerekiyor.

**Baz bulgusunun yorumu.** Pahalı vadelide (pozitif anomali) ertesi gün spot gap'le yükseliyor, vadeli ise uzlaşmadan uzlaşmaya ve gün içinde ucuzluyor. Bu, iki taraflı yakınsama demek.
- Kaynağı büyük olasılıkla spot kapanış müzayedesi ile vadelinin son 10 dk VWAP'ı arasındaki geçici fiyat baskısı.
- Yahoo kapanışı hatası değil: 2021+ vade günlerinin %100'ünde Yahoo kapanışı = resmi uzlaşma. 2018–2020'de bu oran ~%20.
- Spot gün-içi etkisi zayıf: +1,8 bps/sd, IS t 0,6, OOS t 2,6.
- Vadeli gün-içi etkisinin açılış seansı fiyatına bağlı olması, açılış fiyatının da "pahalı" başladığını ve gün içinde düzeldiğini gösteriyor.

**Backtest özetleri** (`results/backtests.csv`; maliyet hisse bazlı RT; L+S iki bacak)
- **BT1 (q=0,1):** net +12,0 bps/gün (t 3,0). OOS +5,1 (t 1,0).
- **BT1, yıllara göre net:** 2017 +9,8 · 2018 +11,0 · 2019 +7,2 · 2020 +4,8 · 2021 +5,6 · 2022 +11,6 · 2023 +9,7 · 2024 +3,8 · **2025 −2,8** · 2026 +3,6. Bozulmanın bir kısmı 02.12.2024 tik genişlemesinden.
- **BT5 (XU030 baz anomalisi → XU030 vadeli gün-içi):** net +7,9 bps (t 2,1). IS t 1,5, OOS t 1,6; yılların %50'si pozitif. DÜŞÜK.
- **BT2 (vsur, AP), BT3 (XU030 gece/gün-içi), BT4 (açılış gap fade):** net ≤ 0.

## 4. Karşı argümanlar ve sınırlamalar
- **Spread tahmini model bazlı.** Emir defteri verisi yok; σ/√N yasası BIST VİOP için kalibre edilmedi. Likitlerde alt sınır 1 tik, gerçek spread zaman zaman 2+ tik olabilir; muhafazakâr sütun bunu kapsıyor. Komisyon kuruma göre onbinde 0,5–10 arasında değişiyor.
- **BT1'de açılış fiyatından dolum iyimser.** Açılış seansı derinliği çok sığ. 2022-09 öncesinde açılış = ilk sürekli işlem. VWAP sürümü net negatif.
- **Örtük faiz gürültüsü.** USDTRY takvim yayılımından gelen faiz τ ile çarpılınca XU030 zaman serisi anomalisine ~85 bps sd gürültü ekliyor. Kesitsel testte bu gürültü ortak olduğu için düşüyor.
- **Temettü kaynağı.** Gerçekleşen temettü kullanıldı (hafif look-ahead). "nodiv" sürümü aynı sonucu verdiği için sinyal bundan etkilenmiyor.
- **Kayıp alanlar.** XU030 için yabancı/yerli kırılımı bültende yok. Opsiyon AP özeti üretildi (`viop_opt_agg.parquet`) ama put/call sinyali test edilmedi.
- **Rejim kırılımları:** 2018, 2021-12, 2023-06, 2025-03, 2026-09/10 için ayrı kırılım yapılmadı. Yalnız yıllık kırılım var.

## 5. Açık sorular
1. XU030D1! gün-içi (akşam seansı 23:00 fiyatı) → ertesi spot açılış/gün-içi. TradingView verisiyle ölçülmeli.
2. Açılış seansı emir defteri / denge fiyatı derinliği (BT1 kapasitesi).
3. Gerçek komisyon tarifesi ve piyasa yapıcı spread'leri (B grubu sözleşmeler).
4. Baz anomalisinin spot kapanış müzayedesi dengesizliği verisiyle (BIST kapanış seansı) ayrıştırılması.

TradingView: BIST:<KOD>1! (sürekli pay vadelisi), BIST:XU030D1!, BIST:XLBNKD1! (?), BIST:X10XBD1! (?), BIST:XSD25D1! (?), BIST:USDTRY1!, BIST:XAUTRY1!, belirli vade için BIST:XU030DZ2026 biçimi; CME_MINI:ES1!.
