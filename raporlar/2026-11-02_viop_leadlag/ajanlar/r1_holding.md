# R1 — HOLDİNG / İNŞAAT / GYO ajanı (KCHOL, SAHOL, DOHOL, ALARK, ENKAI, EKGYO)
Veri: 30.10.2026 kapanışına kadar. Bütün sonuçlar koordinatörün iki düzeltmesinden sonra yeniden hesaplandı: FX_FIX (Yahoo '=X' serileri bir gün kaymış geliyordu; bu ajan da 01.11'de ayrıca tespit edip bildirdi) ve simetrik ±%10,5 temizliği. Senkron analizler 2010+, gap/gün-içi analizler 2014+. IS = 2014–2020, OOS = 2021–2026. t değerleri Newey-West(5).
Kod: `out/code_holding/` (01_hyp → 06_findings sırasıyla çalışır). Bulgular: `out/f_holding.csv` (53 satır).

## 1. Net bulgular tablosu (önem sırasına göre)
| # | Hisse | Sürücü (TV) | İlişki | Rakamlar | Güven |
|---|---|---|---|---|---|
| 1 | SAHOL | AKBNK (BIST:AKBNK) | senkron, iştirak | corr 0,71; XU100 kontrollü kısmi korelasyon (pc) 0,24 (t 10,7); IS 0,25 / OOS 0,34 | YÜKSEK (yurt içi) |
| 2 | KCHOL | ARCLK / FROTO / YKBNK / TOASO / TUPRS | senkron, iştirak | pc 0,15 / 0,15 / 0,12 / 0,12 / 0,11; yılların %71–100'ünde aynı işaret. TUPRS'un son 1 yıllık corr'u 0,24'e düştü | YÜKSEK (yurt içi) |
| 3 | ENKAI | USDTRY (FX:USDTRY) | senkron, XU100'e göre göreli hedge | ham corr ≈0 (−0,02), pc +0,10 (t 5,4); IS 0,10 / OOS 0,11; yılların %76'sında aynı işaret. EURTRY de pc 0,10. USD bazında beta ≈ −1,04 | ORTA |
| 4 | SAHOL | USDTRY / EURTRY | senkron, negatif | pc −0,08 (t −3,7) / −0,08 (t −4,1); IS ve OOS aynı işaret | ORTA |
| 5 | SAHOL | EM bankaları (JSE:SBK, JSE:FSR, ABG, NED) | senkron | SBK pc 0,07 (t 4,2), yılların %100'ünde aynı işaret, OOS 0,11; tarama FDR'den geçer | ORTA |
| 6 | KCHOL | iştirak sepeti açılış ayrışması | lead_intra (açılıştan sonra bilinir) | corr 0,10 (t 5,0; IS 5,0 / OOS 2,1); yılların %100'ünde aynı işaret; kendi gap'i kontrol edilince NAV katsayısı 0,31 (t 4,0). Backtest (8 bps): IS +24 bps/işlem, Sharpe 1,6; OOS +6 bps (t 0,7). 15 bps maliyette OOS ≈0 | ORTA (istatistik); OOS'ta ekonomik olarak zayıf |
| 7 | ENKAI | TUR ETF_{t−1} (AMEX:TUR) | lead_intra, negatif (açılış aşırı tepkisi geri döner) | gap'te +0,12, gün içinde −0,11 (t −5,0; IS −2,5 / OOS −4,9); tarama FDR'den geçer. Backtest OOS +17 bps (t 1,3), IS ≈0 | ORTA (istatistik) / DÜŞÜK (işlem) |
| 8 | SAHOL | Akbank ADR (OTC:AKBTY) | senkron | pc 0,10 (t 5,2) | ORTA |
| 9 | KCHOL | Ford (NYSE:F), Whirlpool, EURUSD | lead_gap | F_{t−1}→gap t 4,3, gün içi ≈0. Eşzamansız kapanıştan kaynaklanıyor, işlenemez | ORTA (işlenemez) |
| 10 | ENKAI | USDTRY_{t−1} | lead_intra | t 3,3 (IS 4,2 / OOS 1,4). Backtest OOS +29 bps (t 1,5; 188 işlem) | DÜŞÜK |
| 11 | KCHOL | 5 günlük NAV ayrışması | lead_multiday (iskonto dönüşü) | t 2,25 (IS 2,2 / OOS 2,2). Backtest (kapanışta giriş) OOS +11 bps (t 1,0) | DÜŞÜK |
| 12 | KCHOL | iştirak sepeti, saatlik (h1) | intraday_minutes | NAV_{h−1}→KCHOL_h pc 0,045 (t 3,0); ters yön ≈0. 5 dakikalıkta etki iki yönlü | DÜŞÜK |
| 13 | EKGYO | CRAK (rafineri ETF'i) | senkron, negatif | pc −0,06 (t −3,2), IS ve OOS aynı işaret, FDR'den geçer; mekanizma dolaylı (petrol → TR enflasyon/faiz) | DÜŞÜK |
| 14 | KCHOL | MRL.MC / AENA.MC (İspanya) | senkron | pc 0,08, FDR'den geçer; mekanizma şüpheli (Avrupa çevre ülke risk faktörü?) | DÜŞÜK |

Önemli olumsuz bulgular (hepsi ÇOK DÜŞÜK, listede tutuldu):
- KCHOL–Brent, crack, Stellantis: pc ≈0.
- ALARK–MTF (kömür), TTF, Brent ve Avrupa müteahhitleri (ACS, FER, HOT, SKA, VIE, STR): pc ≈0. MTF–gün içi backtesti de boş.
- DOHOL–altın, gümüş, BTC: pc ≈0.
- EKGYO–XHB, ITB, ^TNX, VNA, VNQ: pc ≈0. Yalnızca eşzamansız gap var. ^TNX backtestinde IS ve OOS ters işaretli.
- ENKAI–Brent, TTF, ^TNX: pc ≈0.
- ENKAI–RUB: FX hizası düzeltilince senkron ≈0 çıktı. Eski hizada görülen pc −0,08 sahteydi.

## 2. Yöntem
- 01_hyp: Önceden belirlenmiş 6 hisse × ~25 sürücü. Hesaplananlar: corr (tam / 3y / 1y), pc (XU100 kontrollü), beta, yıllık işaret tutarlılığı, IS/OOS ayrımı, lag1 cc/gap/intra, gün içi pc (XU100 gün içi kontrollü), t+1..t+4 sürüklenme, ters yön. Ayrıca USD bazlı versiyon.
- 02_scan: 6 hisse × 1.092 panel sembolü (n≥750, sıfır oranı <0,3) = 6.546 çift. Aileler: pc, lag1-gap, lag1-intra, lag1-intra (XU100 kontrollü), Asya lag0→intra, ters yön. Her aile içinde Benjamini-Hochberg q=0,05 uygulandı.
  - FDR'den geçenler: pc 258 (yabancı 33), gap1 2.301 (eşzamansız kapanış, beklenen), intra1 1, ipc1 5, Asya lag0 0.
- 03_subs / 04_intraday: holding–iştirak ilişkileri.
  - Günlük çapraz gecikmeler, kendi gecikmesi ve XU100 gecikmesi kontrollü.
  - NAV sepeti, sabit ağırlıklı (Koç NAV payı: TUPRS .33, FROTO .20, YKBNK .24, ARCLK .07, TOASO .04, AYGAZ .03, OTKAR .02, TTRAK .03; Sabancı: AKBNK .45, ENJSA .10, CIMSA/BRISA/KORDS/AKGRT .03). Bir de 250 günlük kayan regresyon sepeti (look-ahead yok).
  - Ayrışma sinyalleri: açılış (gap) ayrışması ve kapanış ayrışması.
  - Dış sürücünün "yansıma oranı": holdingin gap betası / NAV'dan beklenen gap betası.
  - Saatlik (2023-11+) ve 5 dakikalık (son ~60 gün) lead-lag.
- 05_bt: 14 backtest kurgusu × 2 maliyet (8 ve 15 bps). Sinyal z-skoru geçmiş 250 güne göre hesaplandı.

## 3. Kanıt ve yorum
**Holding → iştirak yayılımı (kullanıcının "iştirak_t → holding_{t+1}" sorusu):**
- Günlük düzeyde yok. Ham lag1 korelasyonları pozitif (0,04–0,065) ama bu piyasa momentumu. Holdingin kendi gecikmesi ve XU100 gecikmesi kontrol edilince sub→hold pc aralığı −3,2…+0,25 t; anlamlı pozitif değer yok.
- Tek istisna: AKBNK_{t−1} → SAHOL gün içi (kontrollü t 3,5). Ancak backtesti OOS'ta anlamsız (+3,8 bps, t 0,3).
- Gerçek gecikme aynı gün açılışta. KCHOL'un açılış gap'i, iştirak sepetinin açılış gap'inden saptığında fark gün içinde kapanıyor. Bunun kendi-gap dönüşü (KCHOL intra~gap −0,10, t −2,4) olmadığı test edildi: NAV gap katsayısı kendi gap kontrollüyken de 0,31 (t 4,0).
- Ancak OOS'ta etki yaklaşık yarıya iniyor ve 2025–2026'da sıfır/negatif. Muhtemel neden: piyasa bu farkı arbitrajla kapatmaya başladı.
- SAHOL'da aynı etki ham veride yok (t 0,9); backtest kaybettiriyor.

**Dış sürücüler önce iştiraklere mi, holdinge mi yansıyor?**
- Hayır, ikisi aynı anda yansıyor. KCHOL'un gap betası NAV'dan beklenenin 0,76–1,35 katı (Brent 0,76, Ford 0,96, ES 1,16). Holdingin gün içi tepkisi ≈0 (|t|<1,3).
- SAHOL dış şoklara sepetinin 1,4–1,9 katı tepki veriyor. Gerekçe: yabancı akım ağırlığı ve sepette olmayan, halka açık olmayan Enerjisa Üretim. Bu da gecikmeli değil, eşzamanlı.

**ENKAI:**
- Bilanço: USD sunum para birimi, net nakit ~5,0–5,6 mlr USD (4Ç25), Moskova kira portföyü, Türkiye'de gaz santralleri.
- Bunun izi yalnızca göreli olarak görünüyor. TL değer kaybettiği günlerde ENKAI XU100'den belirgin daha az düşüyor (pc +0,10, IS ve OOS aynı).
- TL fiyatı kura günlük bazda yansımıyor: TL beta ≈0, USD bazında beta ≈ −1. Kur geçişi ya gecikmeli ya da daha uzun vadeli. Günlük getiriler bunu yakalamıyor; seviye/eşbütünleşme analizi yapılmadı.
- TUR_{t−1} sinyali: ABD seansındaki Türkiye riski ENKAI'nin açılış gap'ine fazla yansıyor ve gün içinde geri dönüyor. Etki 2021–22 TL krizinde yoğun (yıllık +76 / +88 bps), 2025–26'da negatif. Rejime bağımlı.

**SAHOL:**
- Kur şokunda piyasadan daha kötü performans gösteriyor (banka ağırlığı).
- EM ve Avrupa banka/risk faktörü XU100'ün ötesinde etkili (JSE bankaları, STOXX, IBEX, AENA, WIZZ; pc 0,05–0,09). Etki OOS'ta daha güçlü.
- Düzeltme: AKSA Sabancı iştiraki değil (Akkök Grubu). Sabancı'nın iştiraki Kordsa. KORDS/BRISA/AKSA'nın SAHOL'la XU100 kontrollü korelasyonu negatif çıkıyor; bunun sebebi banka-sanayi faktörü.

**ALARK, DOHOL, EKGYO:**
- Hiçbir dış sürücü XU100'ün ötesinde bilgi taşımıyor.
- ALARK'ın Cenal kömür santrali gelirin ~%72'si, FAVÖK'ün ~%97'si olmasına rağmen MTF/TTF ile ilişki yok. Muhtemel nedenler: Türkiye elektrik fiyatı (PTF) tavanı ve regülasyon, kömür-elektrik spread'inin doğal hedge'i, MTF verisinin bayatlığı (%19 sıfır getiri).

## 4. Karşı argümanlar ve sınırlamalar
- Kısmi korelasyonların çoğu 0,15'in altında; "YÜKSEK" etiketi yalnızca yurt içi iştirak ilişkilerinde var.
- NAV ağırlıkları sabit ve 2025 NAV dağılımına dayalı yaklaşık değerler; tarihsel ağırlıklar farklıydı. Kayan regresyon sepeti benzer sonuç verdi (açılış ayrışması t 4,4).
- Açılış ayrışması stratejisi açılış seansı fiyatının hemen ardından işlem yapmayı varsayıyor. Kayma/derinlik maliyeti 8–15 bps'i aşabilir. OOS'ta zaten kârsız sayılır.
- Saatlik test 3 yıllık, 5 dakikalık test ~60 günlük örneklem; çoklu test düzeltmesi yapılmadı.
- FX zamanlaması: Yahoo günlük FX "kapanışı" t günü 00:00 UTC fiyatıydı. Düzeltildi; eski ENKAI–RUB ve "BIST_{t−1}→FX_t" ters-yön bulguları bu hatanın ürünüydü. Tarama ters-yön ailesinde kalan 677 FDR geçişinin büyük kısmı Asya piyasaları; bunlar ters yön değil, eşzamanlı örtüşme.
- PKR=X (sabit kur), SMRTG, BA.L gibi FDR'den geçen sonuçlar mekanizmasız/sahte sayıldı.

## 5. Yapılmadı
- ENKAI–USDTRY seviye/eşbütünleşme ve aylık vadeli kur geçişi.
- Olay çalışmaları: Mart 2025 ve Eylül–Ekim 2026 fon krizi.
- Holding NAV iskontosunun seviye zaman serisi (yalnızca getiri ayrışması kullanıldı).
- EKGYO–Brent doğrudan testi ve yurt içi faiz verisi (Yahoo'da TR tahvili yok).
- DOHOL'un diğer iştirakleri (Hepiyi, Doğan Trend) halka açık olmadığı için test edilemedi.
- Ters yönde KCHOL_{t−1}→VIX_t pozitif sonucu (t 4,5) incelenmedi.

## Kaynaklar (şirket yapısı)
[Koç 2025 finansal sonuç sunumu (NAV: enerji %38, otomotiv %29, finans %24)](https://cdn.koc.com.tr/cmscontainer/kocholding/media/koc/03yatirimci-iliskileri/sunumlar-ve-bultenler/finansal-sonuc-sunumlari-en/koc-holding-fy25-earnings-presentation.pdf?ext=.pdf) · [Sabancı Ekim 2025 NAV tablosu](https://yatirimciiliskileri.sabanci.com/en/images/pdf/local-brokerage-and-asset-management-companies-meeting-october-3-2025.pdf) · [Alarko yatırımcı sunumu](https://alarko.com.tr/media/w4jpv5gu/alark-investor-presentation.pdf) · [Alarko 3Ç25 bülteni](https://alarko.com.tr/media/jgenxxc0/alarko-holding-3q-2025-earnings-release.pdf) · [ENKA 1Ç25 IAS raporu (USD)](https://www.enka.com/wp-content/uploads/2025/05/ENKAI_CONDENSED_IAS_REPORT_31.03.2025.pdf) · [GCM ENKAI 4Ç25 analizi (net nakit)](https://www.gcmyatirim.com.tr/arastirma-analiz/ozel-raporlar/2026-03-05-enka-insaat-enkai-2025-4-ceyrek-bilanco-analizi) · [Doğan Holding 4Ç25 bülteni](https://www.doganholding.com.tr/media/3uvp1uzn/dohol_4q25-earnings-release.pdf)
