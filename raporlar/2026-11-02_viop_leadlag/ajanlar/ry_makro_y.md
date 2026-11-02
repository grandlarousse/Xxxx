# ry_makro_y — Yurt içi makro/piyasa değişkenleri ↔ 47 VİOP hissesi (kur, gram altın, TL faizleri, risk primi)
Ajan: makro_y · Veri sonu 30.10.2026 · ll.py **v4** (rejime bağlı ±%20,5/±%10,5 temizlik + bayat gün = hacim 0 ve h==l) ile tüm betikler yeni süreçte yeniden çalıştırıldı.
Kod: `out/code_y_makro_y/` (00–09 + mlib.py) · Ham sonuçlar: `out/code_y_makro_y/res/` · Bulgular: `out/f_y_makro_y.csv` (2.005 satır).

## 0. Yeni veri (1. turda olmayan; ortak kullanıma açık)
| Veri | Kaynak | Dönem | Not |
|---|---|---|---|
| VİOP günlük bülteni (2.422 gün, eksiksiz) | borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv → `data/viop/` | 2017-03-06 … 2026-10-30 | 2017-03 öncesi 404. Döviz/altın/TLREF/XU030 vadelileri çıkarıldı: `res/viop_fx.parquet` |
| **DİBS getirileri** (BAP kesin alım-satım bülteni, ISIN bazında kapanış bileşik getiri) | borsaistanbul.com/data/ttb/YYYY/AA/ttbYYYYAAGG{2,3}.zip → `data/bap/` (yeni ortak dizin, 3.475 dosya) | 2013-06-03 … 2026-10-30 | 2019 öncesi XLS (oturum 2), sonrası CSV (oturum 3); 2018-07…12 için oturum 2 sadece para piyasası → oturum 3 ayrıca indirildi. `res/bap_bonds.parquet` |
| TLREF oranı + BIST TLREF endeksi (tam arşiv) | borsaistanbul.com/datum/TLREFORANI_D.zip, BISTTLREFENDEKSI_D.zip | 2018-12-28 … | UTF-16 CSV, `dl_makro_y/` |
| Aylık TÜFE (yıllık/aylık %) | TCMB "Tüketici Fiyatları" sayfası (anahtarsız HTML tablo) | 2013-06 … 2026-09 | `res/tufe_tcmb.csv` |
| Bulunamayan | Türkiye CDS (hiçbir anahtarsız kaynak), Yahoo'da DİBS/KYD endeksi (XKYD.IS, XDIBS.IS, DIBS.IS → 404), stooq (JS duvarı) | | CDS yerine EMB, TUR, TUR−EEM vekil |

**Türetilen seriler (BIST takvimi, `res/macro_daily.parquet`)** ve **bilgi anı (UTC)**:
- `y_*` Yahoo günlük FX (FX_FIX sonrası **~24:00 UTC**; BIST kapanışından 9 saat sonra) — USDTRY, EURTRY, sepet (0,5/0,5), gram altın = GC=F(~18:00) × TRY=X(~24:00).
- `v_*` VİOP ön ay (en yüksek açık pozisyon, vadeye >2 gün) **aynı kontratın** uzlaşma/önceki uzlaşma oranı → roll sıçraması yok. **Uzlaşma anı doğrulandı: ~15:00 UTC** (VİOP gram altın uzlaşma getirisi ile saatlik GC×TRY: 13:00 → 0,83; 14:00 → 0,90; **15:00 → 0,96**; 16:00 → 0,88; USDTRY: 15:00'te en yüksek 0,76). Yani BIST kapanışıyla hizalı.
- `h15_*` saatlik 15:00 UTC anlık (2024-01+; altın 2024-06+), `n_*` gece hareketi 15:00 UTC(t−1) → 06:00 UTC(t) (açılıştan önce bilinir).
- `d_ir12` **zımni TL faizi**: ln(F₂/F₁)·365/(T₂−T₁) (VİOP USDTRY 1. ve 2. vade) + ^IRX; aynı kontrat çiftinde günlük fark. Seviye makul (2026 ort. %34,7; TLREF %38,6; 2y DİBS %39,8).
- `d_dibs1/2/5/10` gösterge-benzeri DİBS: vade kovası (150–450 / 450–1000 / 1400–2200 / 2900–4000 gün) içinde **aynı ISIN'in** günlük getiri farkının hacim ağırlıklı medyanı (TÜFE'ye endeksli kağıtlar günün medyanının %60'ının altı → atıldı). BAP kapanışı ~14:00–14:30 UTC (BIST'ten ~30–60 dk önce).
- `d_tlref` TLREF günlük farkı (yayın ~13:00 UTC).

## 1. Net bulgular
| # | İlişki | Rakam | İşlenebilir mi? | Güven |
|---|---|---|---|---|
| 1 | **TL faizi ↑ (DİBS 10y/5y/2y) ↔ BIST ↓, bankalar en çok** (senkron) | XU100 corr d_dibs10 **−0,30** (3y −0,39, 1y −0,39); XBANK −0,33 (1y −0,49); XU100 kontrollü kısmi: XBANK **−0,16** (IS −0,21 / OOS −0,13; yılların %85'i), AKBNK −0,15, ISCTR −0,15; 2y'de XBANK son 1y kısmi −0,38. Beta: 10y'de +1 yp → XBANK piyasaya göre −0,7%. Ters işaret: TUPRS +0,13, ENKAI/SISE/TKFEN +0,08 | Senkron | **YÜKSEK** (bankalar; FDR) |
| 2 | **Kur (VİOP USDTRY, 15:00 UTC hizalı) ↔ bankalar −, ihracatçılar +** | Kısmi: XBANK **−0,20** (IS −0,29 / OOS −0,14), YKBNK −0,18, GARAN −0,18; **SISE +0,17** (IS 0,17 / OOS 0,16, yılların %80'i), ENKAI +0,12, XUSIN +0,14, TUPRS/EREGL +0,10. Ham corr XU100: tam −0,21, **son 1y −0,46** | Senkron | **YÜKSEK** (YKBNK, ISCTR, SISE, sepet/EUR ile de); diğer bankalar ORTA–YÜKSEK |
| 3 | **Yönetilen kur döneminde VİOP USDTRY = faiz/risk göstergesi** | Son 1y: VİOP ön ay günlük sd 10 bp, bunun **baz (ileri puan) bileşeni 12 bp > spot 9 bp**; XU100 ile corr: spot (15:00) −0,08, baz −0,34, toplam −0,46; baz ~ d_ir12 corr 0,42. Yahoo `TRY=X` (24:00) ile son 1y corr sadece −0,08 | Ölçüm bulgusu | ORTA |
| 4 | **Kur duyarlılığı rejime bağlı** | Bankalar kısmi corr: düşük kur-vol rejimi −0,07…−0,09 → **yüksek −0,21…−0,27**; 2018 −0,33, 2021 −0,29, carry 2023H2–25Q1 −0,29 (beta ≈ −1!), KKM −0,09, **2025-03 sonrası −0,04**. ENKAI 0,05 → 0,19; XUSIN 0,09 → 0,19 | Risk yönetimi | ORTA |
| 5 | **Gram altın ↔ TRALT/TRMET** (aynı gün; öncülük yok) | VİOP gram altın kısmi: TRALT **0,20** (IS 0,18 / OOS 0,21, 1y 0,38); 15:00 hizalı (2024+): TRALT 0,30, TRMET 0,25, **GUBRF 0,27** (yeni, 2024+), PETKM −0,17. Gece altın → TRALT gap corr **0,40** (t 5,3) | Senkron / gap'te | YÜKSEK (TRALT) / DÜŞÜK (GUBRF: kısa örneklem) |
| 6 | **OLUMSUZ – 1. turdaki "gece altın → TRALT gün-içi negatif" yeni hizalamayla TEYİT EDİLMEDİ** | n_xau → TRALT gün-içi t **+0,82** (yarılar +1,21 / +0,55); ters-yön (fade) stratejisi H1 −14, H2 −37 bps; devam stratejisi H1 −2, H2 +21 bps (z-skorlu, 8 bps) — tutarsız | Hayır | ÇOK DÜŞÜK |
| 7 | DİBS 2y şoku_{t−1} → XU030/banka/EKGYO **gün-içi** (gap kontrollü) | XU030 t **−3,17** (IS −1,63 / OOS −2,80; 13 yılın 12'sinde negatif corr), XBANK −2,94, EKGYO −3,51, SAHOL (10y) −4,10 (FDR'den geçen tek faiz bağı). Büyüklük küçük: 1 yp → XU030 gün-içi −29 bp; tipik gün ±0,4 yp → ~±10 bp. Mekanizma büyük ölçüde getirinin kendi otokorelasyonu (+0,24) | Brüt 6–21 bps; **8 bps maliyetle IS negatif** (BT1b) | DÜŞÜK |
| 8 | BIST → faiz/kur (ters yön) | 1.071 ters-yön testinde **0 FDR**. En tutarlı: XBANK(XU100'e göre)_{t−1} → 1y DİBS_t t −2,76 (IS −2,61 / OOS −2,05: banka hisseleri kısa faizi bir gün önden fiyatlıyor olabilir); XU100_{t−1} → VİOP USDTRY_t t +3,1 (yalnız OOS, kur kısmi geri dönüşü) | Hayır | DÜŞÜK |
| 9 | **"Dolar hissesi" (USD bazlı/kur geçişkenliği)** | Çeyreklik TL getirisi ~ USDTRY: XU100 b=0,19 (kur 1 → BIST TL 0,19); XU100'e göre göreli: **SASA +0,80 (t 3,9)**, AKSEN +0,51, EREGL +0,35, HEKTS +0,35, SISE +0,31, THYAO +0,28, FROTO +0,24 (t 2,0); haftalık göreli **ENKAI +0,41 (t 6,1)**, EREGL +0,26 (t 3,6), TAVHL +0,26. TL riski: HALKB −0,38 (t −5,6), VAKBN −0,37, DOHOL −0,37, ULKER −0,49, SOKM −0,35, GARAN −0,29 | Uzun vade konumlama | ORTA (ENKAI, EREGL, SASA, HALKB, VAKBN) / DÜŞÜK diğerleri |
| 10 | **Kur geçişkenliği işaret değiştirdi** | Haftalık b: IS 2014–20 tüm gruplar negatif (bankalar −0,84, ihracatçılar −0,41: TL zayıflığı = risk-off), OOS 2021–26 ihracatçılar **+0,25**, bankalar −0,07. Kriz pencereleri (hisse TL getirisi / USDTRY değişimi): 2021-Q4'te EREGL/SISE/SASA/KRDMD/TKFEN 0,90–1,05, bankalar 0,18–0,65, XU100 0,60; 2018-08'de XBANK −0,54, ISCTR −0,72, PETKM +0,95, SISE +0,30 | Rejim | ORTA |
| 11 | **Nominal/reel ayrımı** | 2014–26 yıllık ort. log getiri: XU100 TL **%22,5** / USD **−%1,5** / reel (TÜFE) **+%0,2**. İhracatçı grubu TL 31,6 / USD 7,5 / reel 9,4; bankalar 21,1 / −3,0 / −1,6 | Bilgi | YÜKSEK (aritmetik) |
| 12 | USDTRY_{t−1} (24:00 UTC) → ENKAI gün-içi | t **3,75** (IS 3,94 / OOS 2,06, FDR, gap kontrollü 3,79) ama işaret-backtesti: |z|>1, 8 bps IS +9,7 (t 1,3) / OOS +23,7 (t 1,25), yıllar çok oynak | Zayıf | ORTA (elle YÜKSEK'ten indirildi) |
| 13 | Yahoo kur_{t−1} → gap (eşzamansız kapanış) **kayboldu** | XU100 gap t: IS **−7,4** / OOS **+1,0** (kur 2021 sonrası gece hareket etmiyor) | İşlenemez | ORTA (IS) |
| 14 | Saatlik / 5 dk | 1.140 saatlik testte 14 FDR (çoğu altın→TRALT/TRMET aynı/yarım saat). Gerçek ≥30 dk öncülük: yalnız sepet kur → ENKAI (j=2, t 3,6, corr 0,08). 5 dk (son 60 gün): altın → TRALT 5 dk gecikmeli corr 0,067 (t 4,2), 10 dk 0,032; USDTRY 5 dk'da hiçbir şey (yönetilen kur) | Spread'i aşmaz | DÜŞÜK |
| 15 | Zımni TL faizi (VİOP) değişimi | Gürültülü ama aynı yönde: XBANK kısmi −0,09 (IS −0,10 / OOS −0,09), 1y −0,20; öncülük yok (gün-içi t −0,7); BT1 tüm varyantlar IS'te negatif ya da anlamsız | Hayır | DÜŞÜK |
| 16 | TLREF değişimi | Bankalar kısmi −0,05 (FDR yok); gün-içi t −2,1 (XBANK), BT anlamsız. TLREF politika faizi adımlarıyla hareket eden bir seri — piyasa bilgisini DİBS/VİOP zaten içeriyor | Hayır | ÇOK DÜŞÜK |
| 17 | CDS vekilleri (EMB, TUR−EEM) | EMB_{t−1} → XU100 gap t 4,1 (eşzamansız), gün-içi 0; TUR−EEM → gün-içi **negatif** (XU100 −2,75; gap kontrollü EREGL −4,0, FROTO −3,7): ABD seansındaki Türkiye primi hareketi açılışta aşırı fiyatlanıp kısmen geri veriliyor (1. turdaki gap-fade'in özel hali) | Gap-fade ile aynı | ORTA |

**Çoklu test:** 21 değişken × 51 hedef = 1.071 test/aile; BH-FDR (q=0,05): senkron 387, gap 218, **gün-içi 6, hisseye özgü gün-içi 0, çok-günlük 0, ters yön 0**. Gece hareketi 255 test → gün-içi 0 FDR. Saatlik 1.140 → 14.

**TradingView:** USDTRY `FX:USDTRY` / `FX_IDC:USDTRY` (BIST kapanışı için 1s grafikte 18:00 TSİ barı); VİOP `BIST:USDTRY1!`, `BIST:EURTRY1!`; sepet `(FX:USDTRY+FX:EURTRY)/2`; **gram altın `FX_IDC:XAUTRYG` (doğrulandı: "GOLD / TURKISH LIRA GRAM")**, ons-TL `FX_IDC:XAUTRY`, VİOP gram altın `BIST:XAUTRY1!` (doğrulandı: "Gold TRY per gram Futures"); zımni faiz yerine `BIST:USDTRY2!/BIST:USDTRY1!` yayılımı (`BIST:USDTRY2!` doğrulandı); DİBS `TVC:TR02Y`, `TVC:TR05Y`, `TVC:TR10Y`; 1y `TVC:TR01Y` (?); TLREF (?) bulunamadı; EMB `NASDAQ:EMB`, TUR `NASDAQ:TUR`, TUR−EEM `NASDAQ:TUR/AMEX:EEM`. CDS: yok (?).

## 2. Önemli olumsuz bulgular
- **İşlenebilir (pozisyon bilgi sonrası alınabilen) yurt içi makro öncülüğü yok denecek kadar az.** Kur/altın/faizin t−1 bilgisi ya açılış gap'inde fiyatlanıyor (Yahoo FX, EMB, TUR) ya da hiç taşınmıyor (BIST kapanışıyla hizalı VİOP serilerinde gap ve gün-içi t'leri |t|<1,5).
- **Backtestler (res/bt.csv, 80+ varyant):** maliyet sonrası IS ve OOS'ta birlikte pozitif ve anlamlı **hiçbiri yok**. Özet (8 bps; çift bacakta 16):

| BT | IS (2014/17–20) net bps (t) | OOS (2021–26) net bps (t) | Brüt OOS | Sonuç |
|---|---|---|---|---|
| BT1 zımni faiz z>1 (t−1) → banka sepeti gün-içi short | −21,1 (−1,6) | +2,4 (0,2) | 10,4 | başarısız |
| BT1 zımni faiz z>2 → XBANK gün-içi | +24,1 (1,0; n=56) | +48,7 (1,4; n=70) | 56,7 | ÇOK DÜŞÜK (az işlem) |
| BT1b DİBS 2y z(t−1) → XU030 gün-içi (her gün) | −2,1 (−0,7) | +3,0 (0,6) | 11,0 | maliyet kadar |
| BT1b DİBS 2y \|z\|>1 → EKGYO gün-içi | −5,6 (−0,6) | +41,8 (2,3) | 49,8 | yalnız OOS → DÜŞÜK |
| BT1b DİBS 2y \|z\|>1 → banka sepeti | −0,9 (−0,1) | +25,5 (1,6) | 33,5 | yalnız OOS → DÜŞÜK |
| BT2 gece gram altın (z, 120g) → TRALT gün-içi devam (yarılar: 2024-06/2025-08/2026-10) | −1,8 (−0,1) | +21,3 (1,2) | 29,3 | tutarsız |
| BT2 aynı, geri dönüş (1. tur hipotezi) | −14,2 (−0,8) | −37,3 (−2,0) | — | **reddedildi** |
| BT2b Yahoo gram altın \|z\|>1 (t−1) → TRALT gün-içi devam | +24,6 (2,05) | +17,0 (1,0) | 25,0 | DÜŞÜK (iki dönem +, OOS anlamsız) |
| BT3 USDTRY z(t−1) → (ihracatçı − banka) gün-içi, tüm / yüksek vol / düşük vol | −15,8 / −17,9 / −13,8 | −9,3 / −8,8 / −9,4 | 6,7 | başarısız (rejim filtresi kurtarmıyor) |
| BT3 gece USDTRY z>1 → banka sepeti short (yarılar) | +30,5 (1,95; n=88) | +29,2 (1,3; n=67) | 37,2 | DÜŞÜK (kısa örneklem, 2024+) |
| BT3 gece USDTRY ham işaret → XU100 short | +16,8 (2,9) | +6,1 (0,9) | — | **artefakt**: kur her gece yükseldiği için "hep short" = bilinen negatif gün-içi sürüklenme; z-skorla −15 bps |
| BT4 VİOP USDTRY z(t−1) → (ihracatçı − banka) | −11,5 (−2,6) | −9,4 (−2,1) | 6,6 | başarısız |
| BT5 USDTRY z>1 → ENKAI gün-içi | +9,7 (1,3) | +23,8 (1,25) | 31,8 | DÜŞÜK |
- Rejim filtresi (yüksek kur-vol): senkron betaları 2–3 kat büyütüyor ama hiçbir öncülük stratejisini maliyet üstüne çıkarmıyor.
- TLREF ve zımni faiz günlük değişimleri, DİBS'e göre çok daha zayıf bilgi taşıyor (TLREF politika adımlı; zımni faiz 2. vade uzlaşmasının gürültüsünü taşıyor, sd 2,1 yp, 2021-12 / 2022-02 / 2023-05'te 20–37 yp sıçramalar; z-skor ve 5 sd kırpma uygulandı).
- "BIST kur/faizi öngörüyor mu?": FDR düzeyinde **hayır**; yalnız banka-göreli → kısa faiz (t −2,8) tutarlı.

## 3. Yöntem
- **Hedefler:** 47 VİOP hissesi + XU100, XU030, XBANK, XUSIN (XHOLD: Yahoo günlük verisi tek satır, kullanılamadı). Getiri = log, ll.ret/ll.decomp (v4). Faiz değişkenleri yüzde puan farkı. Her değişken 5 sd'de kırpıldı.
- **Senkron:** corr tam/3y/1y; XU100_t kontrollü kısmi corr (tam, IS 2014–20 / OOS 2021–26, 3y, 1y); yıl bazında kısmi corr işaret oranı; beta (XU100 kontrollü, HAC-NW t). XU100 hisseyi içerir → kısmi corr muhafazakârdır.
- **Öncülük:** y_t ∈ {cc, gap, gün-içi} ~ x_{t−1} + hisse_{t−1} + XU100_{t−1} (NW 5). Hisseye özgü gün-içi: + XU100 gün-içi_t. Çok-günlük: x_{t−1} → Σcc(t+1..t+4) (NW 8). Gece değişkenleri (n_*) için lag 0 → gün-içi (06:00 UTC'de bilinir).
- **Ters yön:** x_t ~ hisse_{t−1} + x_{t−1} + XU100_{t−1}. Not: XU030/XUSIN gibi endekslerde XU100 kontrolü katsayıyı "endeks − XU100" farkına çevirir (yüksek kollinerlik); yorum XU100 satırından yapıldı.
- **Saatlik:** BIST barı (T−60, T], T ∈ 08:30…14:30 UTC (açılış barı ve kapanış seansı hariç); sürücü penceresi (T−30−60j, T+30−60j]; j≥2 sürücü ≥30 dk önde, j≤−1 BIST önde; hisse_{k−1} ve XU100 aynı bar kontrolü. 5 dk: aynı ızgara, son ~60 gün.
- **Rejim:** USDTRY 20g vol (t−1'e kadar), genişleyen pencere tercilleri (look-ahead yok) + 7 tarihsel dönem.
- **USD/reel:** USD bazlı = r_TL − r_USDTRY; reel = r_TL − ln(1+aylık TÜFE)/ay içi gün. Geçişkenlik haftalık/aylık/çeyreklik; XU100'e göreli ve USD-XU100 kontrollü USD betası.
- **Backtest:** ll.backtest; yön mekanizmadan önceden sabit (IS'ten seçilmedi); z-skor geçmiş 250 (gece serilerinde 120) gün; maliyet 8/15 bps (çift bacak 16/30); saatlik tabanlı sinyallerde bölünme 2025-08-01 (iki yarı). Her BT için "pozisyonun long oranı" ve hedefin aynı günlerdeki ortalaması raporlandı (sürüklenme artefaktı kontrolü — BT3'teki artefakt böyle yakalandı).
- **İş modeli sınıfı** (07_usd_real.py, `GROUP`): ihracatçı/döviz gelirli (ENKAI, TUPRS, THYAO, PGSUS, FROTO, TOASO, BRSAN, EREGL, KRDMD, TRALT, TRMET, ARCLK, VESTL, SISE, CIMSA, ASTOR, TAVHL, TKFEN, AEFES, ASELS, PETKM, SASA), banka, yurt içi TL gelirli (BIMAS, MGROS, SOKM, ULKER, TCELL, TTKOM, EKGYO, ENJSA, AKSEN, ODAS, OYAKC), ithalatçı/döviz maliyetli (DOAS, HEKTS, GUBRF), holding. Kısa WebSearch: 2026/06 ihracat payı BRSAN %89, THYAO %88, FROTO %82; bilanço net döviz pozisyonu tabloları anahtarsız kaynakta bulunamadı (KAP dipnotu gerekir) → sınıflama iş modeline dayalı, ampirik geçişkenlik asıl ölçüt. Ampirik sonuç sınıflamayı kısmen düzeltiyor: DOAS/HEKTS çeyreklik geçişkenliği pozitif (ithalatçı beklentisi tutmadı), AKSEN (USD endeksli satışlar) ihracatçı gibi.

## 4. Ayrıntılı kanıt
**4.1 Kur.** Yahoo `TRY=X` (24:00 UTC) ile VİOP (15:00 UTC) arasında corr 0,67 (aynı gün) ve 0,33 (Yahoo t−1); yani Yahoo serisinin ~%40'ı BIST kapanışından sonraki saatler. Bu yüzden Yahoo kur_{t−1} → gap (IS t −7,4) "öncülük" değil eşzamansız kapanış; OOS'ta kur geceleri hareket etmediği için kayboluyor (+1,0). VİOP hizalı seride gap ve gün-içi öncülük yok (XU100 gap t 1,4, gün-içi 0,2). Haftalık USDTRY sd: 2021'de %5,7 → 2025'te %0,22 → 2026'da %0,09; 2025-03 sonrası betalar anlamsızlaşıyor (pc −0,04), ama BIST kapanışıyla hizalı VİOP serisinde ham corr son 1y'de −0,46'ya **yükseliyor** çünkü seri artık ileri puanı (TL faiz/risk primi) ölçüyor (§1-3).
**4.2 Faiz.** DİBS getirileri BIST'in en güçlü yurt içi makro faktörü: XU100 ile corr 10y −0,30, 2y −0,22, 1y −0,16 (USDTRY'den büyük). Banka-özgü kısmi corr 10y'de −0,15…−0,16, son 1y'de −0,33. Faiz ↑ günlerinde ihracatçılar (TUPRS, ENKAI, SISE, TKFEN, EREGL) piyasadan iyi: kur ve faiz aynı TR risk faktörünün iki yüzü. GYO (EKGYO) ham corr −0,25 ama kısmi sadece −0,07 (piyasa faktörü); holdinglerde SAHOL −0,12 (banka iştiraki), KCHOL 0,01. Lag: d_dibs2_{t−1} → gün-içi negatif ve gap pozitif (XU100 gap t +2,3, gün-içi −2,9); gap kontrolünde de sürüyor; ama örtük büyüklük getiri otokorelasyonu (0,24) × senkron beta ile açıklanıyor ve maliyeti karşılamıyor.
**4.3 Altın.** TRALT/TRMET senkron ve 5 dk içinde fiyatlıyor; saatlik j=1 (yarım örtüşme) t 7,1, j=2 t 0,4 → yarım saatten uzun gecikme yok. GUBRF'nin 2024+ altınla kısmi 0,27'si yeni ve 1y'de 0,36 (2026 jeopolitik/İran teması olabilir — mekanizma şüpheli). Gram altın-TL'nin bankalarla negatif kısmi corr'u (−0,09…−0,12) TRY bileşeninden; 15:00 hizalı (2024+) seride işaret pozitif (+0,03…+0,11).
**4.4 Dolar hissesi.** Kısa vadede (haftalık) TL zayıflığı tüm BIST için risk-off'tu (IS); 2021 sonrası ihracatçılar kuru TL fiyatına kısmen yansıtıyor (+0,25–0,48). Çeyreklik ufukta bile XU100 geçişkenliği 0,19 → BIST TL bazında "dolar endeksli" değil; uzun dönemde TL getirisi kur artışının (yıllık ~%24) gerisinde kaldı (USD −%1,5/yıl). En "dolar"lar (XU100'e göre çeyreklik): SASA, AKSEN, EREGL, HEKTS, SISE, THYAO, FROTO, TAVHL, ENKAI (haftalıkta en güçlü). USD-XU100 kontrollü haftalık USD betasında yalnız KRDMD (+0,42, t 4,2) pozitif-anlamlı (TRMET +0,18, t 1,6); DOAS (−0,35), TTKOM (−0,25), OYAKC (−0,21), BIMAS (−0,15) TL'ye en çok maruz.
**4.5 Değişen rakamlar (ll v4 sonrası):** korelasyon/kısmi korelasyonlar en fazla 0,02 değişti (medyan 0,001); gap/gün-içi t'leri medyan 0,1 değişti (en büyük: TUR → MGROS gap t 6,7 → 5,3). **TL/USD/reel yıllık getiriler belirgin değişti** (2020 öncesi %10,5–20 günler artık korunuyor): ör. TRMET TL %6,2 → %30,6, DOHOL %15,0 → %25,4, OYAKC %19,8 → %27,6. Eski sonuçlar: `code_y_makro_y/res_old_v3/`.

## 5. Karşı argümanlar ve sınırlamalar
- **Korelasyon ≠ nedensellik:** faiz–BIST ve kur–banka bağları ortak TR risk primi şokunu yansıtıyor; yön (faiz mi hisseyi, hisse mi faizi) senkron veride ayrıştırılamaz. Ters-yön testleri her iki yönde de zayıf.
- **DİBS serisi** gösterge-benzeri kovadır, resmi gösterge değil; BAP kapanışı BIST kapanışından ~30–60 dk önce → senkron ölçümde küçük zaman kayması; illikit kağıtlarda bayat kapanış otokorelasyon yaratabilir (bulgu 7'nin kaynağı olabilir). 2013–2016'da bazı günlerde kova başına 2–3 ISIN.
- **Zımni faiz** iki vadenin uzlaşmasına dayanır; 2. vade daha az likit (uzlaşma teorik olabilir); ABD faizi için ^IRX (t−1) kullanıldı.
- **VİOP uzlaşma anı** 15:00 UTC'ye en yakın (korelasyonla doğrulandı); kesin uzlaşma algoritması (son 10 dk ağırlıklı ort. vb.) bültende yok.
- **Saatlik/5 dk örneklemler kısa** (FX 2024-01+, altın 2024-06+, TRALT saatlik 2025-11+; 5 dk son 60 gün). Kur 2025-03 sonrası yönetildiği için saatlik kur testleri düşük güçte.
- **Eylül–Ekim 2026 fon krizi** ve **2025-03** son 1y korelasyonlarını şişirebilir (DİBS–banka 1y −0,49).
- **Bilanço FX pozisyonu** doğrudan ölçülmedi (KAP dipnotları); sınıflama iş modeline dayalı.
- **CDS** yok; EMB/TUR vekilleri küresel EM bileşeni ve (TUR'da) BIST hisselerinin kendisini içerir (mekanik).
