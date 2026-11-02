# r1 — HAVACILIK / TURİZM ajanı: THYAO, PGSUS, TAVHL dış sürücüleri

Son veri 30.10.2026. Tüm sonuçlar, koordinatörün iki veri düzeltmesinden sonra (FX_FIX: '=X' serileri 1 gün kaydırıldı; simetrik ±%10,5 temizlik) **yeni bir Python sürecinde bir kez yeniden çalıştırıldı**. Kod: `out/code_havacilik/` (çalıştırma sırası: a1_pairs → a2_scan → a3_multi → a4_hourly → a5_backtest → a5b_attrib → a6_events_intraday → a7_findings). Ara sonuçlar: `out/code_havacilik/res/`. Bulgular: `out/f_havacilik.csv` (77 satır).

## 1. Net bulgular tablosu

| # | İlişki | Sayılar | Güven |
|---|---|---|---|
| 1 | **Avrupa havayolları ↔ THYAO/PGSUS (senkron, hisseye özgü)** | XU100-kontrollü kısmi corr: THYAO–LHA 0,182 (IS 0,143 / OOS 0,243; yılların %94'ünde aynı işaret), THYAO–EZJ 0,162, THYAO–IAG 0,154; PGSUS–EZJ 0,171 (IS 0,147 / OOS 0,209), PGSUS–IAG 0,154. Ham corr 0,26–0,31 (son 1y 0,43–0,45). 16.365 testlik taramada (BH-FDR) her üç hissenin en yüksek kısmi korelasyonları havacılık sembolleri. | **YÜKSEK** |
| 2 | **THYAO ↔ PGSUS senkron** | kısmi corr 0,507, ham 0,72; 2013'ten beri tüm yıllar pozitif. TAVHL–PGSUS kısmi 0,287. | **YÜKSEK** |
| 3 | **TAVHL ↔ havalimanı emsalleri** | ADP.PA kısmi 0,134 (IS 0,120 / OOS 0,187; %88 yıl). IAG 0,130, FRA.DE 0,127, AENA 0,124. Eşik (0,15) altında. ADP, TAV'ın %46,12 ortağı ve TAV'ı konsolide ediyor. | ORTA |
| 4 | **Havayolu sepeti t-1 → BIST gün-içi t (işlenebilir öncülük)** | Avrupa+ABD havayolu sepeti, STOXX/SPX'e göre artık (kayan beta, look-ahead yok); \|z\|>1 olunca yön al; 8 bps maliyet. THYAO: IS 17,6 bps/işlem (t 2,33, SR 0,92), OOS 20,3 bps (t 2,77, SR 0,98). PGSUS: IS 22,0 (t 2,24), OOS 24,5 (t 2,78, SR 1,10). TAVHL: IS 9,0 (t 1,0), OOS 20,8 (t 2,3). Aynı sinyal XU100/XU030 gün-içinde ≈0 → etki havacılığa özgü. Plasebo: sinyal 1 gün bayatlarsa (t-2) etki yok. THYAO 13 yılın 11'inde pozitif. | ORTA |
| 5 | **TUR (ABD'de işlem gören Türkiye ETF'i) t-1 → THYAO gün-içi: TERS işaret** | corr −0,110 (t −4,6; IS t −2,9 / OOS t −3,9; FDR geçer). TUR, THYAO gap'ini +0,126 (t 4,2) etkiliyor; sonra gün içinde geri dönüyor (gap aşırı tepkisi). Tek başına backtest zayıf: IS 24 bps (t 2,3), OOS 16,6 bps (t 1,15). PGSUS ve TAVHL'de zayıf. | ORTA |
| 6 | COMBO = havayolu sepeti − TUR | THYAO: IS 23,2 bps (t 3,27, SR 1,28), OOS 25,8 bps (t 3,66, SR 1,29). PGSUS OOS 25,5 bps (t 2,95). **Ancak** TUR bacağı tam dönem bulgusu görüldükten sonra eklendi, yani gerçek bir holdout değil. XU030 hedge'li hali (16–24 bps maliyet) kârsız. | ORTA (iyimser) |
| 7 | **Brent rejimi** | Tam dönem kısmi corr zayıf: THYAO −0,094, PGSUS −0,082, TAVHL −0,048. Son 1 yıl corr −0,41 / −0,45 / −0,47. 2026'da kısmi ≈ −0,36…−0,45 (savaş öncesi 2026 Ç1'de de negatif). corr(XU100, Brent) 2026'da −0,25: petrol Türkiye/bölge risk faktörüne dönüştü. 2020–21'de işaret pozitifti (yeniden açılış talebi). THYAO/PGSUS'ta işaret 2011–2019 arası istikrarlı biçimde negatif. | ORTA (rejime bağlı); TAVHL DÜŞÜK |
| 8 | **Gece Brent hareketi → açılış gap'i (saatlik, 2024-06+)** | Brent BIST kapanışı (15:00) → açılış (07:00 UTC): gap ile corr THYAO −0,43, PGSUS −0,35, TAVHL −0,41 (ES ile +0,36…+0,43). Nakitte işlenemez. Gün-içi devamı yalnız TAVHL'de var (−0,097, t −2,3). Gece \|Brent\|>%1 ise ters yön: TAVHL 2026'da 58,7 bps (t 3,4), 2024–25'te 10 bps (t 0,6) → savaş rejimine bağlı. | DÜŞÜK |
| 9 | ABD havayolu/JETS t-1 → gap (eşzamansız kapanış) | JETS→gap: THYAO 0,094 (t 3,3), PGSUS 0,150 (t 5,0), TAVHL 0,122 (t 4,7). Avrupa havayollarında gap etkisi yok. BIST kapanışından sonraki Avrupa 15:00→kapanış penceresi de gap'i açıklamıyor (≈0). | ORTA (gerçek, ama işlenemez) |
| 10 | Olay çalışması (piyasa modeli artığı) | Orta Doğu tırmanması havayollarında −%3 civarı: 02.03.2026 savaş/Hormuz THYAO −%3,4, PGSUS −%2,9 (TAVHL +%0,6); 13.06.2025 İsrail-İran THYAO −%3,5, PGSUS −%3,4. Gerginliğin azalması: 24.06.2025 ateşkes +%5,1 / +%6,1 / +%4,4. Atatürk Havalimanı saldırısı TAVHL −%6,3 (CAR0–5 −%10,6). Pfizer aşısı +%5–6. | DÜŞÜK (her biri tek olay) |

## 2. Önemli olumsuz bulgular
- **USDTRY / döviz geliri hipotezi günlük TL getirisinde desteklenmiyor.** FX düzeltmesinden sonra USDTRY ile XU100-kontrollü kısmi corr ≈0: THYAO −0,003 (47 hisse içinde 25.), PGSUS 33., TAVHL 0,053 (6.). Düzeltme öncesinde havayolları 3., 5. ve 6. sıradaydı; bu sıralama hizalama hatasının ürünüydü. USDTRY t-1 → THYAO gün-içi IS'te güçlü (t 4,0) ama OOS'ta yok (t 0,05); yıllık sonuçlar çok oynak (2022, 2024 ve 2025 negatif) → DÜŞÜK.
- **EURUSD → PGSUS** (gelirin %50'si EUR): kısmi 0,008 → ÇOK DÜŞÜK.
- **Jet crack ve HO=F** Brent'e ek bilgi katmıyor (senkron ≈0; PGSUS gün-içi −0,036, t −1,95) → DÜŞÜK.
- **Brent şoku backtest'i** (\|z\|>2 olunca ters yön, gün-içi): THYAO IS 38 bps (t 1,8) → OOS 12 bps (t 0,5); TAVHL IS −38 bps (t −2,7). Olay ortalaması işaret değiştiriyor: Brent-UP sonrası THYAO gün-içi 2014–20 −%0,83 (t −3,5, n=29), 2021–26 +%0,92 (n=15) → DÜŞÜK.
- **THYAO → PGSUS yurt içi lead-lag:** günlük THYAO_{t-1} → PGSUS gap t 3,1, gün-içi t 1,6. Çok değişkenli modelde havayolu sepetleri ve PGSUS'un kendi gecikmesi bu etkiyi emiyor. Saatlik ve 5 dakikalık barlarda lead yok (lag-1 bar corr ≈0). Backtest OOS SR 0,22 → DÜŞÜK. Ters yön (PGSUS→THYAO) yok.
- VIX, TA-125, El Al, Boeing/Airbus, AerCap, Booking/Expedia/Airbnb: kısmi corr ≤0,09; büyük ölçüde piyasa betası → DÜŞÜK / ÇOK DÜŞÜK.
- Taramadaki sürprizlerin mekanizması yok: Lotte Chemical (011170.KS) → THYAO gün-içi 0,081; 8TRA.DE, SGO.PA ve FSR.JO → PGSUS gün-içi → ÇOK DÜŞÜK. Bunlar, Avrupa döngüsel bilgisinin likiditesi daha düşük PGSUS'a yavaş yayıldığını gösterebilir.
- Hedge'li (hisse − β·XU030) gün-içi strateji maliyetten sonra kârsız. Sinyalin net kazancı piyasa yönü riski taşıyor.

## 3. Yöntem (özet)
- Getiriler: log, BIST takvimi (ll.ret / ll.decomp: cc = gap + intra, 2014+). Senkron (tam / 3y / 1y), XU100-kontrollü kısmi corr, beta (NW-t), IS 2010(14)–2020 / OOS 2021–2026, yıllara göre işaret istikrarı.
- Öncülük: sürücü_{t-1} → gap_t, intra_t, hisseye özgü intra (XU100 gün-içinden arındırılmış), t..t+4 sürüklenme; ters yön.
- Tarama (a2): panel_ret_bistcal'daki 1.091 sembol (zero_frac ≤0,30, n ≥750) × 3 hisse × 5 aile = **16.365 test**, aile başına BH-FDR q=0,05. FDR geçenler: sync_pc 584, gap_l1 1.475 (çoğu ABD eşzamansızlığı), intra_l1 156, xintra_l1 143, reverse 327.
- Saatlik (a4): ll.snap_daily ile sürücünün 15:00 (BIST kapanışı), 07:00 (açılış) ve 21:00 UTC fiyatları. ABD hisselerinde yalnız ABD seansı, Avrupa'da 15:00→kapanış.
- Backtest (a5, a5b): sinyal BIST açılışından önce biliniyor; pozisyon açılışta alınıp kapanışta kapatılıyor; maliyet 8 ve 15 bps (hedge'lide 16 ve 24). Sepet artıkları için kayan 250 günlük beta, z-skorlar geçmiş pencereden. Ek kontroller: atıf (bacak bacak), XU100/XU030 kıyası, plasebo (t-2, t-3), long/short ayrımı, yıllara göre kırılım.
- Olaylar (a6): beta [-260,-11] günlük pencereden; AR t0 ve CAR 0–5 / 0–20.

## 4. Şirket gerçekleri (WebSearch, kısa doğrulama)
- THY: USD fonksiyonel para birimi. 2026 yakıt hedge oranı ~%48 (2Ç26 özeti); savaş öncesi ~%40. 2025 geliri 24,1 mlr $. Gelirlerin döviz kırılımı bulunamadı.
- Pegasus: 2025 gelirinin ~%50'si EUR, %28'i USD, %20'si TL. 2026 hedge oranı ~%61–68, Brent 64–71 $ bandında.
- TAV: Groupe ADP payı %46,12 (2017'den beri tam konsolidasyon). Yeni Antalya imtiyazı 2027–2051, 7,25 mlr €; dış hat yolcu servis ücreti 17 €.
- 2026 Orta Doğu savaşı: 1–2 Mart 2026'da Hormuz trafiği neredeyse durdu, Brent 85–90 $'a çıktı; Nisan'da ~126 $ zirve; Temmuz'da tekrar 90 $ üstü. Veride Ekim sonu Brent ~113 $.

## 5. Karşı argümanlar ve sınırlamalar
- Bulgu 4–6 tek tek |t|<3 (COMBO hariç) ve 2020–21 (COVID haber akışı) katkısı orantısız (THYAO 66 ve 44 bps/işlem). Sepet bileşimi önceden seçildi, ancak hipotezlerin bir kısmı tam dönem bakılarak kuruldu → OOS iyimser olabilir.
- Gün-içi stratejinin uzun/kısa asimetrisi var: IS'te kısa bacak, OOS'ta uzun bacak güçlü. Ortalama gün-içi getiri negatif (gap pozitif) → kısa bacak sürüklenmeden kazanıyor olabilir.
- Brent ilişkisi rejime bağlı. 2026 tek bir savaş rejimi; 1y corr, kalıcı bir beta olarak okunmamalı.
- Saatlik örneklem ~560 gün ve savaş dönemi baskın.
- Olay çalışmasında, temizlik nedeniyle bazı t0 günleri bir sonraki seansa kaydı (2016-07-19; 2020-03 olayında THYAO 13.03'e, PGSUS/TAVHL 16.03'e). Tek olaylar istatistiksel kanıt değildir.
- ABD lag0 korelasyonları BIST kapanışından sonraki saatleri de içerir. Avrupa lag0'ı 0,5–1,5 saat sonrasını içerir.
- **Yapılmadı:** VİOP akşam seansı (gece Brent/JETS hareketini işlemek); aylık KAP/DHMİ trafik verisi; mevsimsellik; hisse→sürücü yönünün saatlik testi (sadece günlük); TUR'un yıllara göre kırılımı.

## 6. TradingView adayları
BIST:THYAO, BIST:PGSUS, BIST:TAVHL; XETR:LHA, EURONEXT:AF, LSE:IAG, LSE:EZJ, LSE:WIZZ, LSE:JET2, NASDAQ:RYAAY; NYSE:DAL, NASDAQ:UAL, NASDAQ:AAL, AMEX:JETS; EURONEXT:ADP, XETR:FRA, BME:AENA, SIX:FHZN; ICEEUR:BRN1! / TVC:UKOIL, NYMEX:HO1!, jet crack = NYMEX:HO1!*42−ICEEUR:BRN1!; TUR (NASDAQ:TUR ?), FX:USDTRY, FX:EURUSD, CBOE:VIX, TASE:TA125 ?. Çin borsası kullanılmadı.

Kaynaklar: [Quartr THYAO 2Ç26](https://quartr.com/events/t-rk-hava-yollari-anonim-ortakligi-thyao-q2-2026_F3EzEFvc), [Enterprise AM (Haz 2026)](https://enterpriseam.com/menaplus/2026/06/01/turkish-airlines-sets-sights-on-global-top-spot-amid-reshaped-regional-aviation/), [AGBI](https://www.agbi.com/aviation/2026/06/turkish-airlines-upbeat-despite-fuel-cost-surge-and-stock-price-slump/), [İş Yatırım PGSUS](https://www.isyatirim.com.tr/tr-tr/analiz/arastirma-raporlari/ArastirmaRaporlari/2_20260305092700200_1.pdf), [Info Yatırım PGSUS 2026-06](https://cdn.infoyatirim.com/Content/Analysis/PGSUS%202026-06%20Finansal%20De%C4%9Ferlendirme%20Raporu%20.pdf), [AMF ADP-TAV 2017](https://echanges.dila.gouv.fr/OPENDATA/AMF/CNS/2017/07/FCCNS156082_20170707.pdf), [haber.aero Antalya](https://mail.haber.aero/sivil-havacilik/antalya-havalimani-ihalesi-7-milyar-250-milyon-euroya-fraport-tavin), [Bloomberg Brent Mart 2026](https://www.bloomberg.com/news/articles/2026-03-06/latest-oil-market-news-and-analysis-for-march-6), [Ziraat Yatırım THYAO](https://ziraatyatirim.com.tr/documents/features/ZFG_YATIRIM_thyao-2023-05-05-1c23-pdf_159.pdf).
