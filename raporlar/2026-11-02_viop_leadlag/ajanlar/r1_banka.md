# r1_banka — BIST bankaları (AKBNK, GARAN, YKBNK, ISCTR, HALKB, VAKBN, TSKB; bağlam XBANK/XLBNK) dış sürücüler
Ajan: banka · Veri: 30.10.2026 kapanışına kadar · Panel: 14:38/14:39 UTC sürümü (simetrik ±%10,5 temizlik + ll.FX_FIX) · Tüm betikler bu sürümle bir kez yeniden çalıştırıldı.
Kod: `out/code_banka/` (bk.py, 01_hyp … 08_findings) · Ham sonuçlar: `out/code_banka/res/` · Bulgular: `out/f_banka.csv` (613 satır).

## 0. Önce veri uyarısı (tüm ajanları etkiler)
Yahoo `=X` kur serilerinde ldate=t günlük kapanışı, aslında **t gününün ~00:00 UTC fiyatı** (saatlik ile doğrulandı: seviye farkı medyanı 00:00 UTC'de 2–3 bp, 15:00 UTC'de 20–40 bp). Düzeltme yapılmazsa FX'in "lag0" değeri gerçekte lag1 olur ve "BIST → FX" ters yön sahte çıkar (GARAN_{t-1}→TRY_t t=−11). Koordinatöre bildirildi, ll.py düzeltildi (FX_FIX). DX-Y.NYB, GC=F ve ^MOVE etkilenmiyor (^MOVE için lag0 en güçlüsü, hizalama doğru).

## 1. Net bulgular tablosu
| # | İlişki | Rakamlar | Güven |
|---|---|---|---|
| 1 | **TUR'un BIST kapanışı sonrası ABD seansı hareketi → ertesi gün banka gap'i** (saatlik, 15:30 UTC→ABD kapanışı) | XBANK corr 0,35, t=7,3, beta 0,91, n=696; iki yarı 0,34/0,36. GARAN 0,37 (t 8,8), AKBNK 0,33, HALKB 0,24 | YÜKSEK (ama spot'ta **işlenemez**) |
| 2 | Aynı sinyal → ertesi gün **gün-içi** (açılış→kapanış) | XBANK corr −0,000 (t −0,01); BT1h 10 bps sonrası −2,5 bps/gün | OLUMSUZ: açılışta tamamen fiyatlanıyor |
| 3 | ES gece hareketi (15:00→06:00 UTC) → gap | XBANK corr 0,49 (t 7,2), gün-içi 0,003 | YÜKSEK (gap) / OLUMSUZ (gün-içi) |
| 4 | **USDTRY → bankaya özgü negatif maruziyet** (senkron, XU100 kontrollü) | XBANK pc −0,16 (IS −0,18 / OOS −0,15); yılların %100'ünde ham corr negatif; tarama FDR'den geçti | YÜKSEK (tam dönem); 2025-03 sonrası DÜŞÜK |
| 5 | USDTRY rejim yapısı | pc: 2018-08 kriz −0,34; 2019-20 −0,19; 2021Ç4 −0,32; 2023-06..2025-03 carry −0,30; 2022-23H1 (KKM) −0,02; 2025-03..2026-10 −0,04. **İşaret hiçbir rejimde pozitife dönmüyor**; büyüklük çöküyor (TRY günlük sd 12 bp) | ORTA |
| 6 | USDTRY gece (15:00→06:00) → gap | XBANK corr −0,13 (t −3,0); 2. yarı daha güçlü (−0,19) | ORTA (işlenemez) |
| 7 | **2026 rejim kayması**: bankalar XU100'ün ötesinde küresel faktöre bağlandı | 2025-11..2026-10 XBANK kısmi corr: BZ=F −0,29, SAN.MC +0,28, EMB +0,26, BBVA.MC +0,23, EUFN +0,22, ^TNX −0,21, ^VIX −0,20. 2021–24'te hepsi ≈0. Winsorize ve en büyük 10 Brent günü çıkarılınca da sürüyor (Brent −0,25) | DÜŞÜK (kısa örneklem; izlenmeli) |
| 8 | TUR senkron (bankaya özgü kısım) | XBANK corr 0,69, pc 0,13 (IS 0,20 / OOS 0,10) | ORTA |
| 9 | BBVA ↔ GARAN | Ham corr 0,26 ama **GARAN~BBVA.MC \| XU100 pc 0,02** → GARAN'a özgü bağ yok. Ters yön (BBVA'nın Garanti'ye duyarlılığı, Avrupa bankaları kontrollü): pc IS 0,16 → OOS 0,05 → son 3y 0,01 | DÜŞÜK, zayıflıyor |
| 10 | HALKB ABD davası olayları | Zarrab itirafçı (28.11.2017) AR −4,7% (t −4,2); iddianame (16.10.2019) −3,3% (t −2,1); 2. Daire (23.10.2024) −4,1% (t −1,8); DOJ ertelenmiş kovuşturma anlaşması (09.03.2026) **+9,4% (t 3,8)**; Yüksek Mahkeme reddi (07.10.2025) 0,0% | DÜŞÜK–ORTA (olay bazlı) |

### Önemli olumsuz bulgular
- **Avrupa/Yunan/CEE/EM bankaları senkron ilişkisi tamamen piyasa kanalından**: XBANK ham corr 0,13–0,29, XU100 kontrollü pc 0,00–0,04 (SAN, UCG, ISP, BNP, DBK, PKO, PEO, OTP, ETE, EUROB, TPEIR, SBK, FSR, ITUB, BBD, KBE, KRE). (İstisna: 2026, bulgu 7.)
- **Altın**: USD bazlı pc ≈0 (−0,01…+0,02; son 3y HALKB 0,06 en yüksek); TL bazlı pc −0,06…−0,09 sadece TRY etkisi (TRY kontrol edilince 0). Altın mevduatı hipotezi **desteklenmiyor**.
- **İşlenebilir öncülük yok**: 7 test ailesinde 8.728'er test. FDR'den geçen intra 0, banka-özgü intra_x 0, gap_pc (XU100 gap kontrollü) yalnız 2. Gap'i öngören her şey (VIX t −7,0, MXN −6,3, TUR +6,1, EMB, HYG, CEW…) piyasa gap'i üzerinden çalışıyor (gap|XU100gap pc ≈0).
- **Backtestlerin tamamı 10 bps sonrası başarısız** (aşağıda).
- Kamu–özel spread'i (HALKB+VAKBN − AKBNK/GARAN/YKBNK/ISCTR) için dış sürücü yok (|t|<3); sadece ^TNX +0,05 (t 2,9) ve OOS'ta TUR −0,07 (t −2,8; yabancı akımı özel bankaları seçiyor olabilir) — DÜŞÜK.
- AKBTY/TKGBY ADR: senkron pc 0,42/0,35 (aynı varlık) ve "BIST→ADR" ters yön t≈4,3 = **illikit OTC ADR'nin bayat fiyatı** (TKGBY günlerin %20'sinde sıfır getiri). İşlenebilir değil.

## 2. Yöntem
- Getiri bazlı, BIST takvimi; gap/intra ayrıştırması (2014+). Senkron: tam/3y/1y corr, XU100 kontrollü kısmi corr, beta, yıl bazında işaret oranı, IS 2014–2020 / OOS 2021–2026. Öncülük: sürücü_{t-1} → cc/gap/intra (NW t), gap|XU100 gap ve intra|XU100 intra kısmi; ters yön; t+1..t+4 sürüklenme. (01_hyp.py: 8 hisse × 52 sürücü, TL ve USD bazlı.)
- Tarama (02_scan.py): 8 hisse × 1.091 sembol (n≥750, zero_frac<0,3), 7 test ailesi, White HC0 t, aile bazında BH-FDR q=0,05. Sayımlar: sync 7.915/8.728 FDR, sync_pc 542, gap 3.241, gap_pc 2, intra 0, intra_x 0, rev 9 (ADR'ler).
- Saatlik (04_hourly.py, 2023-12+): TUR/BBVA/EEM 15:30 UTC→ABD kapanışı; ES 15:00→06:00 UTC; USDTRY 15:00→06:00 UTC. Not: TUR saatlik barları :30'da başlıyor; 15:30 referansı BIST kapanış seansından ~20 dk sonrasını içeriyor (küçük kirlenme).
- Rejim (07_regime.py), olay çalışması (06_events.py: piyasa modeli, beta [−260,−20], kıyas HALKB/GARAN için XBANK, XBANK için XU100), çoklu beta ve altın (03_targeted.py).

## 3. Backtestler (05_bt.py; yön IS'ten seçildi; maliyet 0/8/10/15 bps, pair 0/16/20/30)
| Backtest | OOS (2021–26) medyan, 10 bps | Brüt (0 bps) | Sonuç |
|---|---|---|---|
| BT1 TUR_{t-1} → banka intra (8 seri) | −9,4 bps/gün, SR −0,5 | +0,6 bps | kenar yok |
| BT1h TUR_post (saatlik) → intra | −2,5 bps, SR −0,2 | +7,5 bps | kenar maliyet altında |
| BT5h ES gece → intra | −15,8 bps, SR −1,1 | −5,8 | başarısız |
| BT2 BBVA ADR_{t-1} → GARAN intra | −22,8 bps, SR −1,4 (IS'te seçilen yön OOS'ta ters) | −12,8 | başarısız |
| BT2 BBVA.MC_{t-1} → GARAN intra | −9,4 bps | +0,6 | başarısız |
| BT3 gap fade/continuation (\|z\|>1) | −23,4 bps | −13,4 | başarısız |
| BT3 + TRY-vol YÜKSEK rejim filtresi | +16,8 bps, SR 0,3 | +26,8 | ÇOK DÜŞÜK: banka başına 17–36 işlem, bankalar arasında işaret tutarsız (XBANK +, GARAN −) |
| BT3x banka-özgü fazla gap → fazla intra (pair) | brüt +8,5 bps; 2 bacak maliyetini karşılamıyor | | başarısız |
| BT4 ^MOVE_{t-1} → XBANK intra | +3,3 bps, SR 0,2 (IS net −6) | +13,3 | DÜŞÜK, FDR yok |

## 4. Diğer kanıtlar
- **Çoklu beta (OOS 2021+, XU100+TRY+GC+BZ+VIX+EMB)**: TRY betası −0,26…−0,33 (t −3,1…−4,7; en güçlü HALKB −4,7); Brent −0,03…−0,08 (AKBNK t −3,6, VAKBN −3,2); GC ≈0 (TSKB −0,09 t −2,1). Kamu bankalarında R² daha düşük (0,34–0,40, özellerde 0,43–0,50) → kamu bankaları daha çok yerel/politik bilgiyle hareket ediyor.
- TRY asimetrisi: TL değer kaybı b+ −0,195 (t −4,3), kazancı b− −0,261 (t −2,9); fark anlamlı değil.
- BBVA tarafı: XU100 <−%4 günlerinde BBVA.MC − Avrupa bankaları ort. −21 bps, >+%4 günlerinde +20 bps (n=148). Beklenen yön ama küçük.
- GARAN olayları: BBVA teklif duyurusu 15.11.2021 GARAN +9,5% ama XBANK de +9,3% (kıyas GARAN'ı içeriyor → AR küçümseniyor); fiyat artışı TL15 (25.04.2022) AR +2,8% (t 3,1). KKM 21.12.2021 XBANK − XU100 +7,0% (3 gün +15,8%). TCMB ortodoks dönüş 22.06.2023 XBANK −5,4% (XU100'e göre). 10.08.2018 −3,4%.
- Kısa doğrulama: BBVA'nın Garanti payı %85,97 (VTO 18.05.2022). Halkbank: iddianame Eki 2019; Yüksek Mahkeme 19.04.2023; 2. Daire 22.10.2024; Yüksek Mahkeme reddi 06.10.2025; DOJ ertelenmiş kovuşturma anlaşması 09.03.2026; dava düşürüldü ~17.06.2026. VİOP akşam seansı (19:00–23:00 TSİ) endeks vadelilerini kapsıyor (BIST Likit Banka dahil), pay vadelilerini kapsamıyor.

## 5. Karşı argümanlar / kendi bulgumun eleştirisi
- Bulgu 1–3 "öncülük" değil, eşzamansız kapanış. Gerçek fırsat ancak **VİOP XLBNK akşam seansı**nda olabilir; o seans aynı bilgiyi zaten fiyatlıyor olabilir (vadeli verisi olmadığı için test edilmedi).
- Bulgu 7 tek yıla ve muhtemelen tek temaya (2026 İran savaşı/petrol, ~Mar–Tem 2026) dayanıyor; XU100'ün banka dışı bileşenlerinin farklı tepki vermesi de kısmi corr'u şişirebilir.
- TRY bulgusu: düzeltilmiş FX getirisi 00:00→00:00 UTC; BIST seansından sonraki ~9 saati de içeriyor → senkron ölçüm hafif gürültülü (gerçek etki muhtemelen biraz daha büyük).
- Olay çalışması: tek günlük olaylar, sızıntı/zamanlama belirsiz (ABD akşamı haberleri ertesi BIST gününe atandı), çoklu test yok.
- USD bazlı banka getirileri (hyp_usd.csv) üretildi ama raporda ayrıca yorumlanmadı.

## 6. Yapılmadı / test edilemedi
- **Türkiye 5y CDS / TR 2y–10y faiz**: kamuya açık günlük seri bulunamadı (stooq JS duvarı, FRED sadece aylık OECD, EVDS API anahtarı gerekiyor). Proxy: TUR/EMB/USDTRY → ÇOK DÜŞÜK güven. TV adayları: TVC:TR02Y ?, TVC:TR10Y; CDS için TV ticker'ı bilinmiyor (?).
- TCMB PPK / enflasyon açıklama günlerinin sistematik olay çalışması (yalnız 22.06.2023 tek olay olarak).
- VİOP XLBNK akşam seansı backtest'i (veri yok). ALPHA.AT 2025-07 öncesi yok (ALBKY OTC ADR kullanıldı, illikit).
- Banka içi saatlik lead-lag (GARAN → diğerleri) ayrıca test edilmedi; günlük taramada BIST hisseleri arası intra öncülüğü FDR'den geçmedi.

## 7. TradingView
BIST:XBANK, BIST:XLBNK (vadeli: BIST:XLBNK1! ?), NASDAQ:TUR, NYSE:BBVA, BME:BBVA, OTC:AKBTY, OTC:TKGBY, FX:USDTRY, CME_MINI:ES1!, ICEEUR:BRN1!, BME:SAN, NASDAQ:EUFN, NASDAQ:EMB, TVC:US10Y, CBOE:VIX, COMEX:GC1!. Çin borsası ticker'ı kullanılmadı.
