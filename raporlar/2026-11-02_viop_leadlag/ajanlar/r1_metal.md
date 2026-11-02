# R1 — METAL / ÇELİK / MADENCİLİK / ALTIN (ajan: metal) — TAM KAPSAM
Hisseler: EREGL, KRDMD, TRALT (eski KOZAL), TRMET (eski KOZAA), BRSAN. Veri 30.10.2026 kapanışına kadar. Hesaplar FX_FIX ve simetrik ±%10,5 temizlik sonrası yapıldı.

**Dosyalar**
- Bulgular CSV: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/f_metal.csv` (559 satır; hiçbir hipotez elenmedi).
- Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_metal/`. Çalıştırma sırası: a1_hyp → a2_scan → a3_hourly → a4_bt → a6_extra → a5_csv → a7_update. Ara sonuçlar `res/` altında.

## 1. Net bulgular tablosu (önem sırasıyla)
| # | Hisse | Sürücü (Yahoo → TradingView) | İlişki | Rakam | Güven |
|---|---|---|---|---|---|
| 1 | EREGL | ISDMR.IS, KRDMD.IS (BIST:ISDMR, BIST:KRDMD) | sync | corr 0,65 / 0,62; XU100 kontrollü kısmi corr 0,45 / 0,34; yılların %100'ünde aynı işaret; IS 0,46 → OOS 0,76 | YÜKSEK |
| 2 | TRMET | TRALT.IS, TRENJ.IS (BIST:TRALT, BIST:TRENJ) | sync | kısmi corr 0,62 / 0,75; TRMET~TRALT haftalık corr 2026'da 0,85 | YÜKSEK |
| 3 | EREGL | Küresel çelik **aylık**: SLX, MT.AS, STLD, NUE, VALE (AMEX:SLX, EURONEXT:MT, NASDAQ:STLD, NYSE:NUE, NYSE:VALE) | sync (aylık) | aylık kısmi corr 0,41 / 0,41 / 0,37 / 0,33 / 0,30 (t 4,7–6,7). SLX için IS 0,56 / OOS 0,56. Günlükte aynı ilişki sadece 0,07–0,12 | YÜKSEK |
| 4 | TRALT | GC=F, SI=F (COMEX:GC1!, COMEX:SI1!) | sync | günlük kısmi corr 0,22 (son 1y 0,42); aylık kısmi 0,42 (t 6,5), IS 0,49 / OOS 0,27; 30 dk gün-içi senkron 0,415 (t 15). Rejime bağlı: haftalık 2023'te −0,11, 2026'da 0,49 | YÜKSEK |
| 5 | KRDMD, EREGL | FMG.AX (ASX:FMG). ASX 05–06 UTC'de, yani BIST açılışından önce kapanıyor | lead_intra | KRDMD gün-içi t=4,38 (IS 2,61 / OOS 3,78), EREGL t=3,87 (2,36 / 3,26). Kârlı yıl %77–85. XU100 hedge'li t 3,1 / 2,4. SLX, ES, MT.AS t-1 ve gap kontrolüyle t 3,2 / 2,7. **Çin ajanının bulgusu bağımsız doğrulandı** | YÜKSEK (istatistik) / işlem değeri DÜŞÜK–ORTA |
| 6 | EREGL, KRDMD | Japon çelik/makine + Avustralya madencileri z-kompoziti (TSE:5411, TSE:5401, TSE:6301, ASX:FMG, ASX:BHP) | lead_intra | Sadece \|z\|>1 günleri, 15 bps maliyet: OOS EREGL +27,7 bps (t 2,34), KRDMD +32,1 bps (t 2,18). Hedge'li t 1,3–1,6. 2024–2026'da zayıfladı | ORTA |
| 7 | TRALT, TRMET | Altının gece hareketi (saatlik, 15:00 UTC → 06:55 UTC) | lead_gap | TRALT gap corr 0,37, XU100'den arındırılmış 0,42 (t 6,1). Gün-içi t 0,5 | ORTA. İşlenebilir değil; VİOP pay vadelisinde akşam seansı yok |
| 8 | KRDMD | SHFE HRC (Çin borsası, TV'de açılmaz → alternatif ASX:FMG) | lead_intra | Kendi roll'suz serimle t=3,37 (IS 0,59 / OOS 3,78). lag1'de etki yok. FMG ile birlikte modelde HC t=2,47 | ORTA (zamanlama sınırda: 07:00 UTC) |
| 9 | KRDMD | Küresel çelik/metal **aylık** (SLX, MT.AS, VALE, HG=F, TIO=F) | sync (aylık) | aylık kısmi corr 0,22–0,26 (t 3,1–4,0) | YÜKSEK / ORTA |
| 10 | EREGL | Avrupa çelik (MT.AS, SSAB-A.ST, VOE.VI) günlük | sync | kısmi corr 0,12, haftalık kısmi 0,25, yılların %100'ünde aynı işaret, FDR'den geçiyor | ORTA |
| 11 | TRALT/TRMET | Olay: kayyum ataması 28.10.2015 | event | XU100'e göre 20 günlük birikimli fazla getiri (CAR) −%35,8 / −%40,8 (z −2,7 / −3,5) | ORTA |
| 12 | TRALT/TRMET | Olay: İmamoğlu/TL şoku 19.03.2025 | event | CAR[0,+20] +%23 / +%28 (z 2,2 / 2,5) | ORTA (tek olay) |
| 13 | BRSAN | ABD 232 vergisinin Türkiye'ye uygulanan oranı | event | %25'e indirilmesi (16.05.2019): CAR[-1,+1] +%10,1 (z 2,9). %50'ye çıkarılması (10.08.2018): −%8,5 (z −2,5; kur kriziyle iç içe) | DÜŞÜK |
| 14 | TRMET | GC=F | sync | günlük kısmi corr 0,13, aylık 0,30. Altın etkisi TRALT payı üzerinden dolaylı | ORTA |

## 2. Önemli olumsuz bulgular
- **BRSAN'ın küresel boru/petrol sürücüsü yok.** Günlük kısmi corr ≈0. Aylıkta da yok: TS −0,04, OIH −0,02, HRC=F 0,00, CL=F −0,02. BRSAN~TS haftalık corr 2004–2011'de 0,3–0,5 iken 2023–2026'da ≈0. TS t-1 → BRSAN backtest'i negatif. BRSAN'ın ABD operasyonları hisse getirisine günlük ve aylık frekansta yansımıyor. Hisseyi yurtiçi ya da şirkete özgü faktörler ve vergi olayları sürüyor.
- **Altın t-1 → TRALT gün-içi:** 15 bps maliyetle IS −12,5 / OOS −18,4 bps, kârlı yıl 2/13. Saatlik gece sinyaliyle de OOS t 0,96. Gap geri dönüş stratejileri negatif.
- **ABD çeliği (SLX; NUE, STLD, CLF, MT) t-1 → EREGL gün-içi:** 8 bps'te OOS −1,9 / −4,8 bps. Lag-1 etkisi gap'te (t≈5–6), yani eşzamansız kapanıştan geliyor.
- **TIO=F (TV: COMEX:TIO1!) günlük olarak bozuk bir seri.** Bu bir aylık ortalama kontrat. Ay sonunun son 3 gününde oynaklık 34 bps (ay ortası 115 bps). Ayın ilk 2 gününde (roll) oynaklık 418 bps ve günlerin %12'sinde 4σ üstü sıçrama var. VALE ile korelasyon ay ortasında 0,32, roll ve ay sonunda 0,09. Ay ortası alt-örneklemde EREGL kısmi corr 0,075'ten 0,106'ya çıkıyor. Öneri: TIO2!/FEF2! (2. ay) ya da FMG/VALE kullanılmalı.
- **HRC=F ve BUS=F günlük sinyal vermiyor.** Seriler bayat (%50–68 sıfır getiri). Aylıkta EREGL kısmi corr 0,17'ye çıkıyor ama HRC=F'te IS +0,25 / OOS −0,11 işaret değiştiriyor → DÜŞÜK.
- **"Türk altın madencisi" ortak faktörü yok.** EGO ve SSRM'nin TUR ETF'ine yüklenmesi ≈0 (EGO t 0,5; sadece OOS'ta t 2,0). TRALT (USD) haftalık kısmi corr, EGO ve SSRM'ye karşı ≈0. Çöpler heyelanı (13.02.2024) TRALT'ı etkilemedi (CAR[0,10] −%4, z −0,4).
- **h1 "hisse önde" sonuçları artefakt.** BIST barları :30'da, sürücü barları :00'da bitiyor. m5 ile 30 dakikalık tam hizalı ölçümde ne hisse ne sürücü önde. Örnek: TRALT~GC=F senkron t 15, iki yönde öncülük t −0,5 / −1,3. EREGL~Avrupa çelik 30 dk senkron bile ≈0; HG=F 0,15.
- **Muhtemel sahte bulgular (FDR'den geçse de):** KOSPI/Samsung → TRMET gün-içi, PKR=X → TRALT, ALB → BRSAN, IDR=X → EREGL, TUR t-1 → EREGL gün-içi (negatif; muhtemelen piyasa geneli geri dönüş).

## 3. Çin ajanının bulgularının bağımsız kontrolü
- **FMG.AX → KRDMD / EREGL / BRSAN gün-içi:** benim değerlerim t 4,38 / 3,87 / 3,51, Çin ajanınınki 4,39 / 3,87 / 3,51. Aynı veri olduğu için bu tek başına bağımsızlık sayılmaz. Bağımsız eklerim şunlar:
  - IS ve OOS ayrı ayrı anlamlı.
  - XU100 hedge'li testte de anlamlı.
  - SLX, ES, MT.AS t-1 ve gap_t kontrolünden sonra da anlamlı.
  - TRALT ve TRMET'te yok (t 1,0 / 1,7) → plasebo testi geçiyor.
  - XU100'de de var (t 2,7) → etkinin bir kısmı piyasa geneli.
  - Ekonomik değer marjinal. 15 bps işaret stratejisinde IS negatif; KRDMD OOS +9 bps (t 1,26). \|z\|>1'de KRDMD OOS +22 bps (t 1,58).
- **SHFE HRC → KRDMD:** Sina kontrat dosyalarından kendi "en yüksek açık pozisyonlu kontrat" serimi kurdum. Sonuç t=3,37 (Çin ajanı 3,33). Ama IS (2018-12…2020, kısa örneklem) t 0,59, ve lag1 sürümünde (tam işlenebilir) etki yok (t 0,85). Gün seansı 07:00 UTC'de, yani BIST sürekli işlem açılışında bitiyor → işlenebilirlik sınırda. → ORTA. EREGL'de DÜŞÜK (t 2,09).

## 4. Backtestler (IS 2014–2020 / OOS 2021–2026; maliyet 8 ve 15 bps gidiş-dönüş)
| Test | Mod | IS bps (t) | OOS bps (t) | OOS Sharpe | Kârlı yıl |
|---|---|---|---|---|---|
| JP/AU kompozit → EREGL gün-içi | \|z\|>1, 15 bps | +12,1 (1,47) | +27,7 (2,34) | 1,02 | 10/13 |
| JP/AU kompozit → KRDMD gün-içi | \|z\|>1, 15 bps | +26,3 (2,33) | +32,1 (2,18) | 0,96 | 12/13 |
| FMG.AX → KRDMD gün-içi | işaret, 15 bps | −7,9 (−1,28) | +9,2 (1,26) | 0,53 | 8/13 |
| FMG.AX → KRDMD gün-içi | \|z\|>1, 15 bps | +5,0 (0,40) | +22,4 (1,58) | 0,67 | 9/13 |
| SHFE HRC → KRDMD gün-içi | \|z\|>1, 15 bps | −23,8 (−0,97; n=117) | +31,0 (2,26) | 0,92 | 8/9 |
| Avrupa çelik t-1 → EREGL gün-içi | işaret, 8 bps | +1,0 | +0,7 | 0,04 | — |
| SLX t-1 → EREGL gün-içi | işaret, 8 bps | +3,5 | −1,9 | −0,13 | — |
| GC=F t-1 → TRALT gün-içi | işaret, 15 bps | −12,5 (−2,0) | −18,4 (−2,35) | −0,98 | 2/13 |
| TS t-1 → BRSAN gün-içi | işaret, 15 bps | −11,3 | −6,8 | −0,32 | 3/13 |
| TIO=F t-1 → EREGL gün-içi | işaret, 15 bps | −8,7 | −12,8 | −0,86 | 2/13 |
| Gece altın (saatlik) → TRALT gün-içi | işaret, 15 bps | −4,4 (2024-06…2025-07) | +17,7 (0,96) | — | — |

**Yıllara göre (bps/işlem):**
- JP/AU → EREGL: 2021 +45, 2022 +73, 2023 +27, 2024 −10, 2025 +12, 2026 +16.
- JP/AU → KRDMD: 2022 +99, 2024 +4, 2025 +7, 2026 −29.
- **Getiri büyük ölçüde 2021–2023'te; etki son iki yılda azalıyor.**

Not: işaret modundaki negatif t'lerin çoğu maliyetten geliyor; brüt getiri ≈0.

## 5. Yöntem
- **a1:** 5 hisse × 86 sürücü, TL ve USD bazında. Hesaplananlar: senkron corr (tam/3y/1y), XU100 kontrollü kısmi corr, beta, haftalık corr, IS/OOS, yıllık işaret tutarlılığı, lag1 → gap/gün-içi (NW-t), ters yön, 4 günlük sürüklenme.
- **a2:** 28.440 test (tüm panel × 5 hisse × 6 test). Her aile için Benjamini-Hochberg FDR (q=0,05) uygulandı.
- **a3:** saatlik gece ayrıştırması.
- **a4 / a6:** backtestler; FMG/SHFE kontrolü; TIO=F ay sonu analizi; aylık frekans; Türkiye madenci faktörü; 232 vergisi ve Çöpler olayları; m5 ile 30 dk hizalama; gece altın backtest'i.
- **a7:** CSV birleştirme.

## 6. Şirket gerçekleri (WebSearch)
- **KRDMD — brifingdeki varsayım düzeltildi:** Kardemir hurda bazlı EAF değil. Karabük'te yüksek fırınlı, **entegre (cevher + kok)** uzun ürün üreticisi (ray, inşaat demiri, profil).
- **EREGL:** Erdemir + İsdemir, entegre yüksek fırın, yassı ağırlıklı.
- **TRMET → TRALT:** TR Anadolu İnşaat (%99 bağlı ortaklık) üzerinden ~%47–48 dolaylı pay (Eylül 2025 konsolide tablo). 2026'da karşılıklı doğrudan alımlar ~%3,6 (tek kaynak). Kod değişikliği 24.11.2025. Yönetim 2016'dan beri TMSF'de. 2026'da satış/devir teyit edilmedi. Kaymaz için ÇED yürütmeyi durdurma kararı var. Çukuralan için ~104 bin ons tahmini (İş Yatırım).
- **BRSAN:** Baytown/Houston ERW OCTG tesisi (2014+) ve Berg Pipe (2023) ile ABD kapasitesi ~1 Mt. ABD'nin ciro payı yüzdesi **doğrulanamadı**.
- **VİOP:** pay vadelileri sadece 09:30–18:10 TSİ normal seansta işlem görüyor. Akşam seansı (19:00–23:00) endeks ve kıymetli maden/döviz için. Resmi listeden teyit edilmeli.

## 7. Karşı argümanlar ve öz-eleştiri
- **Kompozit sinyal (bulgu 6):** bileşenler FDR'den geçen semboller arasından seçildi → seçim yanlılığı var. FMG.AX tek başına önceden belirlenmiş bir hipotezdi, bu yüzden daha güvenilir. Etki büyük günlerde toplanıyor ve son yıllarda zayıflıyor. Tokyo kapanışı Kasım 2024'te 06:30 UTC'ye kaydı.
- **TRALT:** altın üreticisi ile Koza grubu olay/yönetim hissesinin melezi. Grup faktörü (kısmi 0,6–0,75) altından (0,22) baskın. Altın bağı aylıkta güçlü (0,42) ama yıllara göre oynak.
- **Frekans etkisi:** günlük ve aylık kısmi corr arasındaki büyük fark, günlük korelasyonun eşzamansızlık ve gürültüyle bastırıldığını gösteriyor. Portföy riski için aylık değerler, işlem için günlük değerler esas alınmalı.

## 8. Yapılmadı / sınırlamalar
- SGX:FEF (demir cevheri) ve LME hurda verisi yok; Türk hurda ithal fiyatı ve koklaşabilir kömür test edilemedi (ÇOK DÜŞÜK hipotez).
- ABD sondaj kulesi sayısı test edilmedi (Yahoo'da yok).
- m5 verisi sadece ~60 gün; TRALT saatlik verisi 11 ay.
- Olay tarihleri yaklaşık; 2018-08 olayı kur kriziyle iç içe.
- TradingView ticker'ları aday, ayrı ajan doğruluyor. Çin borsası ticker'ı verilmedi; HKEX için "açılmayabilir" notu var.
