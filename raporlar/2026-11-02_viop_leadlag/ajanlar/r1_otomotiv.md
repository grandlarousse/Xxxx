# R1 — Otomotiv, dayanıklı tüketim ve elektrik ekipmanı (ajan: otomotiv)

**Kapsam.** Hisseler: FROTO, TOASO, DOAS, ARCLK, VESTL, ASTOR. Veri 30.10.2026 kapanışına kadar.

**Veri düzeltmeleri.** Koordinatörün iki düzeltmesi uygulandı:
- FX_FIX: Yahoo '=X' serileri 1 gün kaydırıldı.
- Temizlik simetrik hale getirildi: ±%10,5'i aşan günler artık her iki yönde çıkarılıyor.

Tüm sonuçlar bu düzeltmelerden sonra yeniden hesaplandı.

**Dosyalar.**
- Bulgu tablosu: `f_otomotiv.csv` (69 satır).
- Kod: `code_otomotiv/`. Sıra 01_hyp → 02_scan → 03_asia → 04_bt → 06_hourly → 07_regime → 08_extra → 09_mech → 05_findings → 10_findings_add. Ara sonuçlar `code_otomotiv/res/` altında.

**Genel sonuç.** 49 backtest varyantı denendi. Hiçbiri 8 bps maliyetten sonra OOS'ta t>2 ile pozitif değil. Senkron ilişkiler gerçek, ama yabancı emsallerle sektöre özgü bağ küçük. En güçlü ilişkiler yurtiçi tema ve grup etkileri. Tek belirgin yapısal değişim, ASTOR'un küresel şebeke temasına bağlanması.

## 1. Net bulgular

| # | Hisse | Sürücü (TV kodu) | İlişki | Kanıt | Güven |
|---|---|---|---|---|---|
| 1 | ASTOR | EUPWR (BIST:EUPWR), GESAN (BIST:GESAN) | senkron | XU100 kontrollü kısmi korelasyon (pc) 0,37 / 0,31 (IS 0,45 → OOS 0,29). 250 günlük kayan korelasyon hiç 0,39'un altına inmedi. Bağ zayıflıyor (z = −2,8). | YÜKSEK |
| 2 | FROTO↔TOASO; FROTO, TOASO, ARCLK↔KCHOL; ARCLK↔VESTL | BIST:… | senkron | FROTO–TOASO pc 0,31; 250 günlük korelasyon en az 0,20, tüm yıllarda pozitif. KCHOL ile ≈0,15. ARCLK–VESTL pc 0,09–0,21 (son yıllarda artıyor). | YÜKSEK |
| 3 | ASTOR | Küresel şebeke sepeti (EURONEXT:SU, SIX:ABBN, NYSE:ETN, XETR:SIE, KRX:267260, KRX:298040) | rejim | Korelasyon 2023–24'te −0,01, 2025–26'da 0,26 (Fisher z = 4,2). SU ile pc −0,13'ten +0,13'e çıktı (z = 4,0). Kayan korelasyonun son değeri 0,32 ve bu tarihi en yüksek seviye. | ORTA |
| 4 | TOASO | STLA (NYSE:STLA), saatlik hizalı | senkron | 15:00 UTC hizalı korelasyon 0,24; günlük lag0 ile 0,15. pc 0,13 (2023-11 sonrası). | ORTA |
| 5 | TOASO | XETR:EXV5, EURONEXT:RNO, MIL:STLAM | senkron | Ham korelasyon 0,21–0,28, pc 0,07–0,10. 2014–2026 arasında 13 yılın 10'unda pc pozitif. OOS zayıflıyor. | ORTA |
| 6 | FROTO | XETR:EXV5, XETR:VOW3 | senkron | Ham 0,21–0,24, pc 0,06–0,07. NYSE:F ile pc yalnız 0,03. | ORTA |
| 7 | TOASO | Stellantis Türkiye devri (olay) | event | Piyasa modeline göre anormal getiri: 25.10.2024 (Rekabet Kurulu reddi) −%6,4 (z −3,5); 18.04.2025 (onay) +%7,0 (z 3,3); 21.04.2025 +%9,6 (z 4,5). | ORTA |
| 8 | İhracatçılar ile DOAS arasındaki kur farkı | FX:USDTRY | senkron | pc FROTO +0,06, TOASO +0,04, DOAS −0,06. Ham korelasyon DOAS −0,15, FROTO −0,06. Yön mekanizmayla tutarlı, büyüklük küçük. 2024 sonrası TL rejiminde işaretler oynak. | ORTA |
| 9 | FROTO | NYSE:F büyük hareket günleri (\|z\|>2) | lead_intra | 8 bps maliyetten sonra IS +41,9 bps, OOS +43,2 bps (t 1,35 / 1,84). Tüm dönem t = 2,02. 13 yılın 10'unda pozitif. 15 bps maliyette OOS +36 bps. | DÜŞÜK (en iyi işlenebilir aday) |
| 10 | FROTO, TOASO | Asya lag0: TWSE:TAIEX?, KRX:KOSPI?, KRX:005930 | lead_intra | 174 Asya testinden 5'i FDR'den geçti (t 3,6–3,9). OOS t ≈ 2. \|z\|>1 varyantında tüm dönem t = 2,44, OOS +14,5 bps (t 1,3). Etki BIST geneline yayılıyor: TWII için 47 hissenin 13'ünde t>2. XU100'de OOS'ta kayboldu. | DÜŞÜK |

**Diğer düşük güvenli bulgular:**
- ABD otomotiv yarı iletken ve döngüsel ailesi (ON, NXPI, STM, BWA, APTV, SOX) → FROTO gün-içi: 12 sürücünün 12'si pozitif. ON, NXPI ve IFX kontrolünden sonra da t = 4,4. Yine de sinyal maliyet sonrası para kazandırmıyor.
- XHB / ITB / XLY → DOAS gün-içi: SPX, IWM, EEM ve TNX kontrolünden sonra t = 3,4. Faiz kanalı değil (TNX, TLT, ZN ≈ 0). XU100 gün-içinde etki yok, DOAS'a özgü.
- STLAM'ın BIST kapanışından sonraki hareketi → TOASO gün-içi: r = 0,16, t = 2,9. Gap'te görülmüyor, ama 138 saatlik testte FDR'den geçmiyor.
- Kore şebeke sepeti → ASTOR gün-içi: \|z\|>1 varyantında ikinci yarı +47 bps net (t 1,3); ilk yarı ile işaret tutarsız. Yıllar: 2023 −0, 2024 +12, 2025 +18, 2026 +67 bps.

## 2. Önemli olumsuz bulgular (elenmedi, etiketlendi)

**Backtest sonuçları**
- 49 backtest varyantının 22'si OOS'ta net pozitif, ama hiçbiri t>2 değil. Çok sayıda varyant denendiği için tablodaki 9. bulgu dahil hepsi seçim yanlılığına açık.
- Basit işaret sinyalleri (F / STLA / EXV5 / WHR / LG / Samsung / LG Display) → gün-içi: hepsi maliyet sonrası negatif.
- Hedge'li varyantlarda (hisse − XU100 gün-içi) de sonuç yok.

**FX ile ilgili sahte bulgular**
- FX düzeltmesinden önce USDTRY_{t−1} → ihracatçı gün-içi t ≈ 4,7 çıkıyordu (FDR'den geçiyordu). Bu sahteydi; düzeltmeden sonra OOS −17 bps.
- KRW=X lag0 düzeltmeden sonra look-ahead içeriyor; geçersiz.
- Düzeltmeden sonra EURUSD ve EURTRY → ihracatçı backtest'lerinin hepsi negatif.

**Çin emsalleri**
- Çin beyaz eşya ve TV şirketleri: Haier 6690.HK / 600690.SS, Midea 0300.HK / 000333.SZ, Gree 000651.SZ, TCL 1070.HK, Hisense 0921.HK. ABD alternatifleri: FXI, KWEB, MCHI, HSHCY. Hepsinde pc ≈ 0.
- FXI ve KWEB'deki ham korelasyon (0,07–0,13) tamamen küresel risk faktörü.
- **Önerilebilecek, test edilmiş bir Çin alternatifi yok.**

**Sektör kanalları**
- VESTL ile panel fiyatı proxy'leri arasında ilişki yok: LG Display (KRX ve NYSE LPL), AUO, Innolux, BOE için pc −0,04 ile 0,01 arası. Samsung ve Sony de aynı.
- ARCLK'da çelik maliyeti kanalı görünmüyor: HRC=F korelasyonu −0,04 (seri %50 bayat). MT'de ham +0,16 risk-on etkisi, pc 0.
- ASTOR'da bakır (HG=F, pc −0,05) ve BTC (pc −0,01) ile bağ yok.

**Olay sonrası kırılımlar**
- Beko Europe sonrası ARCLK'nın WHR ve ELUX ile bağı değişmedi (p > 0,4).
- TOASO'da birleşme sonrası STLAM bağı arttı ama anlamlı değil (p = 0,10). USDTRY korelasyonu +0,12'den −0,02'ye döndü (p = 0,03; ithalatçı yönüne kayış). Kısmi korelasyon farkı anlamlı değil.

## 3. Şirket gerçekleri (WebSearch ile)
- **Ford Otosan:** 2025 ihracatı 602.842 adet (toptan satışın yaklaşık %83'ü). Ford'un Avrupa ticari araç satışlarının %79'unu sağlıyor. Ford ile Koç eşit ortak; %41 kaynakta net teyit edilemedi.
- **Tofaş:** Rekabet Kurulu 24.10.2024'te reddetti, 18.04.2025'te şartlı onay verdi. Stellantis Türkiye (Fiat, Peugeot, Citroën, Opel, Jeep, DS, Alfa) 400 milyon €'ya devralındı. 256 milyon € yatırımla yeni platform üretimi 2026 3. çeyrekte başlıyor.
- **Doğuş Otomotiv:** VW, Audi, SEAT, Cupra, Porsche, Bentley, Lamborghini ve VW Ticari'nin distribütörü. Škoda %50 iştiraki Yüce Auto üzerinden. 2025'te 208 bin adet.
- **Arçelik:** Whirlpool Avrupa işinin devri 17.01.2023'te duyuruldu (anormal getiri +%7,9). Beko Europe (Arçelik %75, Whirlpool %25) 02.04.2024'te kapandı (anormal getiri +%4,5).
- **Vestel:** İhracat yaklaşık 2,2–2,3 milyar $, ağırlıklı Avrupa. 2025 satışları reel olarak %26 düştü.
- **Astor:** İhracatın gelirdeki payı yaklaşık %45–46. Mart 2026'da ABD'li şirketlerle 768,9 milyon $ trafo sözleşmesi imzaladı; bu, 3. bulgudaki rejim değişimiyle tutarlı.

## 4. Yöntem

**Getiriler.**
- ll.ret (BIST takvimi). BIST dışı sürücülerde tatil ffill'inden gelen tam sıfırlar NaN yapıldı.
- Senkron analiz 2010 sonrası; gap ve gün-içi 2014 sonrası (ll.decomp).
- IS/OOS ayrımı 2014–2020 / 2021–2026. ASTOR, GEV ve DTG gibi kısa serilerde örneklem ortası kullanıldı.

**Öncülük gecikmesi (L).**
- Kore, Japonya, Tayvan: L = 0. Kapanışlar 05:30–06:30 UTC; BIST açılışı yaklaşık 07:00 UTC.
- HK, Hindistan, Çin: BIST seansıyla çakıştığı için lag0 işlenebilir değil.
- ABD, Avrupa, FX (düzeltme sonrası), kripto ve BIST sürücüleri: L = 1.

**Senkron metrikler.** Korelasyon (tam / 3y / 1y), XU100 kontrollü pc, XU100+USDTRY kontrollü pc, USD bazlı korelasyon, beta, yıllık işaret tutarlılığı, ters yön.

**Öncülük testleri.** sürücü_{t−L} → gap_t (işlenemez), → intra_t (işlenebilir), → açılış bilgisi kontrollü intra_t (XU100 gap_t, kendi gap_t, ^GSPC_{t−1}), → t+1..t+4 sürüklenme.

**Veri güdümlü tarama (02_scan).**
- 6 hisse × 1.174 sembol × 5 aile = 35.220 test.
- Her ailede ayrı Benjamini-Hochberg (q = 0,05).
- FDR'den geçen sayıları: sync_pc 712, lead_intra 5, lead_intra_pc 22.
- Sürprizlere mekanizma testi uygulandı (08_extra / 09_mech):
  - CSG.AS: 2026-01'den beri yalnız 188 gün veri, sahte.
  - GWLLY: fiyatın %38'i bayat (OTC), sahte.
  - KRDMB → ARCLK: kontrollerle OOS'ta kayboluyor.
  - EREGL → FROTO: yalnız OOS'ta görülüyor, BIST içi tersine dönüş.
  - ON → FROTO ve XHB → DOAS: aile/kanal testi yapıldı (yukarıda).

**Asya (03_asia).** 29 Asya sembolü × 6 hisse = 174 test. KOSPI / N225 / TWII kontrolüyle "emsal mi, piyasa mı?" ayrımı yapıldı. Ayrıca saatlik ilk saat / günün geri kalanı ayrımı (2023-11 sonrası): ilk saatte 84 testin 5'i, gün geri kalanında 8'i |t|>2, yani şans düzeyi.

**Saatlik hizalama (06_hourly).** r_in = 15:00 UTC'den 15:00 UTC'ye (gerçek senkron). r_ovn = BIST kapanışından ertesi gün 06:30 UTC'ye kadar.
- r_ovn → gap medyan t = 1,7; ES=F → FROTO gap t = 5,3.
- r_ovn → gün-içi: 138 testin 9'u |t|>2.

**Rejim (07_regime).** Yıllık pc, 9 rejim penceresi, 250 günlük kayan korelasyon özeti, olay öncesi/sonrası Fisher z ve olay günü anormal getiri.

**Backtest.** ll.backtest; işaret ve z-skor (geçmiş penceresi, look-ahead yok); 0 / 8 / 15 bps maliyet; yıllara göre kırılım (`res/*bt*.csv`).

## 5. Rejim pencereleri (pc|XU100; ayrıntı `res/regime_windows.csv`)
- **Ağustos 2018 kur krizi ve Aralık 2021 kur şoku:** İhracatçı–USDTRY pc negatife döndü (ARCLK −0,24 / −0,20). Ani TL şokunda, ihracatçılar da genel risk satışından kaçamıyor; kur kalkanı kısa vadede çalışmıyor. DOAS −0,17 / −0,33 (ithalatçı, daha sert).
- **Mart 2025 (İmamoğlu şoku) sonrası:** FROTO–VOW3 pc −0,16, FROTO–EXV5 −0,07. Yurtiçi şok dönemlerinde yabancı emsal bağı kopuyor.
- **Eylül–Ekim 2026 fon krizi:** ASTOR–şebeke sepeti pc 0,34, ARCLK–WHR 0,26, DOAS–VOW3 0,19 yükseldi. Kısa pencere (~40 gün), düşük güven.

## 6. Karşı argümanlar ve sınırlamalar
- **XU100 kontrolü** FROTO, TOASO ve ARCLK'nın kendisini (Koç ağırlığı) içerdiği için pc'yi aşağı çekebilir. Ham korelasyonlar `f_otomotiv.csv` içinde.
- **9. ve 10. bulgu çoklu varyant denemesinden geliyor** (49 backtest). Tüm dönem t ≈ 2 olduğu için seçim yanlılığı göz ardı edilemez. Canlıya almadan önce ileriye dönük test gerekir.
- **ASTOR rejim bulgusu** yalnız ~450 günlük "sonra" penceresine dayanıyor. Sebep (ABD sözleşmeleri mi, küresel AI/veri merkezi teması mı, yabancı yatırımcı girişi mi) ayrıştırılamadı.
- **Saatlik veri yalnız 2023-11 sonrasını kapsıyor.** Kesin senkron korelasyonlar kısa örneklemden.
- **Tarama p-değerleri iid varsayımlı.** FDR'den geçenler için Newey-West t ayrıca hesaplandı.
- **VİOP pay vadelilerinin akşam seansında işlem görüp görmediği doğrulanmadı.** Görüyorsa ABD seansı (lag0) bilgisi kısmen işlenebilir olabilir.
- **TradingView kodları aday:**
  - '?' olanlar doğrulanmalı: KRX:KOSPI?, TWSE:TAIEX?, OTC:GWLLY?, EURONEXT:CSG?.
  - HKEX kodları kullanıcıda açılmayabilir.
  - Çin borsası kodu verilmedi; SS/SZ serileri yalnız test amaçlı kullanıldı.
