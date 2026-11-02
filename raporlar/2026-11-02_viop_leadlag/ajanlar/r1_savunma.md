# R1 — SAVUNMA-TELEKOM ajanı (ASELS, TCELL, TTKOM)
Tarih: 02.11.2026 · Veri: 30.10.2026 kapanışına kadar · Paneller ikinci düzeltmeden (FX kaydırması + simetrik ±%10,5 temizlik) sonra yeniden üretildi; tüm betikler yeni süreçte bir kez daha çalıştırıldı.
Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_savunma/` (01–07 betikleri, `res/` sonuçları, `logs/` çıktıları). Bulgular: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/f_savunma.csv` (47 satır).

## 1. Net bulgular tablosu

| # | Hisse | Sürücü (TV) | İlişki | Rakamlar | Güven |
|---|---|---|---|---|---|
| 1 | TCELL | TKC (NYSE:TKC) | senkron | corr 0,74 / 3y 0,84 / 1y 0,89; XU100 kontrollü kısmi 0,61 (IS 0,62, OOS 0,62); yılların %100'ünde aynı işaret | YÜKSEK (aynı varlık; işlem sinyali değil) |
| 2 | TCELL | TKC t-1 → TCELL gap | lead_gap | corr 0,11, t 4,3. Saatlik: TKC 15:30→ABD kapanışı → gap β 0,20 (t 2,9); ES=F kontrolüyle t 1,3 | ORTA, **İŞLENEMEZ** |
| 3 | TCELL | Parite sapması D → TCELL gün-içi | lead_intra | intra_t ~ D_(t-1) + gap_t: b_D 0,13 (t 2,8); IS 0,09 (t 2,2), OOS 0,15 (t 2,4). BT \|U\|>50 bps: OOS +19 bps/işlem, t 2,5, Sharpe 1,07 (8 bps); IS ≈ 0 | ORTA (maliyete çok duyarlı) |
| 4 | TCELL | TKC kapanış sonrası (saatlik) → ertesi gün 07:30 UTC→kapanış | intraday_minutes | β 0,30, t 2,75 (n 694); BT \|tk_post\|>50 bps OOS +20 bps, Sharpe 1,14 (8 bps) / 0,75 (15 bps), n 282 | DÜŞÜK (yalnız 2023-12 sonrası) |
| 5 | TCELL↔TKC | Prim kapanması | reverse | dP_(t+1) ~ D_t β −0,43 (t −12,5); kapanmanın ~2/3'ü TKC/kur tarafında | ORTA |
| 6 | TCELL/TTKOM | Karşılıklı | senkron | kısmi 0,29 (IS 0,19 → OOS 0,40) | YÜKSEK |
| 7 | TTKOM | TKC | senkron | corr 0,48, kısmi 0,21 (OOS 0,29); TKC sapması TTKOM gün-içini tahmin etmiyor | YÜKSEK (sektör) |
| 8 | ASELS | Avrupa savunma sepeti | rejim | kısmi 2014–21 0,02 → 2022–26 0,13 (XU100+STOXX kontrolüyle 0,15); tam dönem 0,06 | ORTA |
| 9 | ASELS | Yeniden silahlanma haber günleri (n=6) | olay | AR0 ort. +357 bps (t 3,3), işaret uyumu %100, CAR0–5 +769 bps | ORTA (n küçük) |
| 10 | ASELS | EU savunma şok günleri (\|z\|>3) | olay/senkron | 2022–26: yukarı n=13 AR0 +284 bps, aşağı n=10 −181 bps; 2010–21 yok denecek kadar az. Ertesi gün etkisi yok | ORTA (senkron, işlenemez) |
| 11 | ASELS | XBANK (BIST:XBANK) | senkron | kısmi −0,16 (yurt içi banka/savunma rotasyonu) | ORTA (iç faktör) |
| 12 | ASELS | OTKAR (BIST:OTKAR) | senkron | kısmi 0,11 (IS 0,14 → OOS 0,06) | ORTA |
| 13 | TTKOM | USDTRY (FX:USDTRY) | senkron | kısmi −0,04 (IS −0,10, OOS −0,05; yılların %76'sında negatif) | DÜŞÜK |
| 14 | TTKOM | İmtiyaz uzatımı (KAP 27.08.2025) | olay | AR: 27.08 +48, 28.08 −388, 29.08 −419 bps; CAR(27.08–03.09) −710 bps; TCELL de −290/−204 bps | DÜŞÜK (tek olay) |

TradingView sepet bileşenleri: XETR:RHM, LSE:BA., MIL:LDO, EURONEXT:HO, OMXSTO:SAAB_B, OSL:KOG, XETR:HAG, XETR:R3NK. Kore: KRX:012450, KRX:064350, KRX:079550, KRX:047810. ABD: NYSE:LMT/NOC/RTX/GD/LHX, AMEX:XAR, AMEX:PPA, ITA '?'. EUAD '?'. Çin borsası ticker'ı kullanılmadı.

## 2. Önemli olumsuz bulgular
- **TKC → TCELL, beklenen "en güçlü lead" zayıf çıktı.** TKC'nin BIST kapanışından sonraki hareketinin yalnızca ~%20'si TCELL açılışına geçiyor. Bu kısım da büyük ölçüde ABD piyasa hareketi (ES=F kontrolüyle t 1,3). Geri kalanın bir bölümü ertesi gün TKC'de geri dönüyor, yani gürültü (β −0,17). Bir bölümü de TCELL'de gün içinde fiyatlanıyor (bulgu 3–4).
- **Gap işlenemez.** VİOP pay vadelileri akşam seansında işlem görmüyor. Akşam seansı (19:00–23:00) yalnızca endeks, döviz ve kıymetli maden sözleşmelerine açık. Kaynaklar: https://www.borsaistanbul.com/sss/viop , https://www.getmidas.com/blog/viop-islem-saatleri , https://www.yatirimx.com.tr/piyasa/viop-islem-saatleri-2025-gunduz-ve-aksam-seanslari-ne-zaman/11132 (güncel resmi duyuruyla teyit önerilir).
- **ASELS için işlenebilir dış öncülük yok.**
  - EU_DEF_(t-1) → gün-içi: OOS Sharpe −0,52.
  - Kore lag0 → gün-içi: KS11 kontrolüyle t 1,6; BT OOS Sharpe 0,33.
  - Avrupa post-close → gün-içi: Sharpe 0,49, t 0,8.
  - Şok günü ertesi: Sharpe 0,09.
  - Saatlik veride gün-içi öncülük: t<1,8.
- **Tam panel taraması** (13.662 test, BH-FDR q=0,05): gün-içi lag1'de ASELS ve TTKOM için FDR'den geçen dış sürücü sıfır. TCELL'de geçen tek sürücü LISN.SW (Lindt). Mekanizması yok, BT OOS Sharpe 0,17 ve XU100'de de etkisi var; büyük olasılıkla sahte → ÇOK DÜŞÜK. Gap lag1'de FDR'den geçenler TUR, NDX, SOX, VIX, AUDUSD gibi ABD/risk vekilleri: eşzamansız kapanış.
- **Savaş günleri karışık.** 24.02.2022'de ASELS −%10,5 ile taban oldu (XU100 −%8,5; AR −302 bps). Sonraki 5 günde CAR +1.295 bps. Türkiye risk primi gün 0'da savunma temasını bastırabiliyor.
- **Barış günleri** (n=9): ASELS AR0 −85 bps (t −1,9); CAR0–5 +200 bps, yani etki kalıcı değil.
- **Diğer zayıf ilişkiler** (kısmi korelasyon ~0–0,08, DÜŞÜK/ÇOK DÜŞÜK): EM/Avrupa telekom (VOD, MTN, DTE, ORA, TEF, OPL), VEON, KYIV, ABD savunma, ESLT. TTKOM için dış sürücü beklentisi düşüktü; bu doğrulandı.

## 3. Yöntem
- **Getiriler:** BIST takvimine oturtulmuş log getiriler kullanıldı. Senkron analiz 2010+, gap/gün-içi 2014+. IS 2014–2020, OOS 2021–2026. t değerleri Newey-West (5 gecikme).
- **Parite primi:** P = ln(TKC × USDTRY / (2,5 × TCELL)). ADR oranı SEC 20-F'e göre 2 ADS = 5 hisse; veride yıllık medyan oran 2,47–2,59 ile doğrulandı. Sapma D = P − önceki 20 günün ortalaması (adj fiyatlarla). Kur, ~00:00 UTC t+1'e hizalı.
- **Saatlik analiz:** TKC 15:30 UTC snap (kışın ABD 14:30'da açıldığı için 15:00 snap yok). Kur için 15:00/21:00 snap.
- **Olay çalışması:** AR = r − β·XU100, β önceki 250 günden. Olay günlerinde temizlenmemiş getiri kullanıldı. Haber tarihleri WebSearch ile orta/düşük güvenle belirlendi; liste `code_savunma/events.csv` içinde.
- **Backtest:** `ll.backtest` ile, 8 ve 15 bps maliyetle.

## 4. Veri tuzağı (ekip geneli)
Yahoo `=X` günlük kapanışı aslında D günü 00:00 UTC fiyatı. Bunu bağımsız olarak tespit ettim (TUR~TRY=X: 2011'den itibaren lag −1 baskın). Koordinatör ll.py'de düzeltti. Benim `sv.fx_aligned` fonksiyonum ham veriden tek kaydırma yapıyor; düzeltilmiş ll ile korelasyonu 0,999, yani çift kaydırma yok.

## 5. Şirket gerçekleri (doğrulama)
- **Turkcell ADR:** 2 ADS = 5 adi hisse (SEC 20-F FY2022: https://www.sec.gov/Archives/edgar/data/1071321/000110465923051268/tkc-20221231x20f.htm).
- **Aselsan ihracatı:** teslimatlardaki payı 2024'te %19, 2025'te %25. 2024 satış bazında ~%14. 2025'te 2 mrd USD'yi aşan ihracat sözleşmesi imzalandı (https://www.dailysabah.com/business/defense/turkiyes-defense-giant-aselsan-to-end-2025-with-record-exports-deals/amp , https://hurriyetdailynews.com/aselsans-net-income-surged-45-percent-last-year-206265).
- **Türk Telekom imtiyazı:** 28.02.2050'ye uzatıldı. Bedel 2,5 mrd USD + KDV, 2026'dan başlayarak 10 yılda ödenecek. KAP tarihi 27.08.2025 (https://ttinvestorrelations.com/en-us/announcements-disclosures/pages/ir-news , https://www.bloomberght.com/turk-telekom-un-imtiyaz-sozlesmesi-25-yil-uzatildi-3755808).
- **ReArm Europe:** 04.03.2025 (https://fortune.com/europe/2025/03/04/europe-announces-unprecedented-840-billion-rearmament-plan-tackle-grave-threats-defense-giants-bae-thales-rheinmetall).
- **Barış günleri:** Kasım 2025 haberleri (https://www.pravda.com.ua/eng/news/2025/11/19/8008065 , https://en.ain.ua/2025/11/24/rheinmetall-shares-fell-by-almost-5/).

## 6. Karşı argümanlar ve sınırlamalar
- **Bulgu 3:** Regresyon IS ve OOS'ta anlamlı, ancak işlem başına beklenen kazanç (~10–20 bps) maliyet düzeyinde. Açılış fiyatından giriş varsayımı iyimser. IS backtest'i ≈0.
- **Bulgu 4:** Yalnız ~2,9 yıllık saatlik veriye dayanıyor.
- **Olay çalışmaları:** n küçük (6–9), olaylar 2025'e yığılmış. Mart 2025 İmamoğlu şoku (19.03) Bundestag oylamasına bitişik.
- **2022 rejimi:** ASELS'in kendi kampanyaları (KAAN, Çelik Kubbe, ihracat sözleşmeleri) Avrupa temasıyla aynı döneme denk geliyor, bu yüzden nedensellik kanıtlanmış değil.
- **Prim kapanması** (bulgu 5) için IS/OOS ayrı hesaplanmadı.
- **2026 dışı:** 2026'daki barış/savaş haber günleri doğrulanamadı (WebSearch sonuç vermedi). Yerine veri güdümlü şok günleri kullanıldı.
