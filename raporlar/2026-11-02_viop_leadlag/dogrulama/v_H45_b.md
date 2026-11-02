# v_H45_b — 2. aşama ÇÜRÜTME: H45 (KCHOL açılış NAV ayrışması; ENKAI–TUR_{t-1}; ENKAI–USDTRY_{t-1})
Tarih 02.11.2026. Veri sonu 30.10.2026.
- Kod: `out/code_v_H45_b/` (`blib.py`, `01_repro.py` … `07_extra.py`; loglar `log01–08`; `res_kchol.csv`, `res_sector_placebo.csv`, `res_scan47.csv`, `viop_ssf.parquet`).
- ll.py ve 1. aşamanın vlib.py'si import EDİLMEDİ; hizalama, temizlik ve Newey-West t sıfırdan yazıldı.
- Temizlik: fiyat marjı rejimine bağlı (2020-03-13 öncesi ±%20,5, sonrası ±%10,5). Karşılaştırma için "legacy" ±%10,5 de çalıştırıldı; sonuçlar neredeyse aynı.
- IS = 2014–2020, OOS = 2021–2026. NW(5) t.
- **Yeni veri:** VİOP günlük bülteninden (2017-03 … 2026-10, 2.424 gün) KCHOL, ENKAI ve XU030 vadelilerinin gerçek açılış, VWAP, kapanış ve uzlaşma fiyatları, hacim ve işlem sayısı.

## 0. Hüküm özeti
| | İstatistik gerçek mi? | Gap-fade/bid-ask mekaniği mi? | Gerçek enstrümanla işlenebilir mi? | Güven (istatistik / işlem) |
|---|---|---|---|---|
| (a) KCHOL NAV ayrışması | EVET. Sektör-eşleşmeli 400 plasebonun hepsini, hisse-bazlı piyasa kontrolünü ve her iştirak tek tek testini geçiyor. AMA 2020'den beri sönüyor (2014–19 t 5,1; 2023-06+ t 1,5) | Kısmen. NAVgap tek başına sıfır (t 0,8); güç tamamen "fark"tan ve KCHOL'un kendi müzayede fiyatının sapmasından geliyor. Eşzamanlı müzayedeler arası mikro-yapı etkisi | **HAYIR.** Gerçek KCHOL vadelisinde VWAP girişi → uzlaşma corr −0,006; 8 bps backtest OOS −6,4 bps. Spot 07:30 sonrası sıfır | ORTA (sönen) / ÇOK DÜŞÜK |
| (b) ENKAI–TUR_{t-1} | Yalnız **2020–2023 rejiminde**: 2014–19 t −1,5 (anlamsız), 2024–25 ≈0. Kuyruk günlerine bağımlı: %1 uç atılınca t −5,1 → −2,4 | HAYIR: Egap, Egap², büyük-gap kuklası ve piyasa gap'i kontrolünde t −4,6; küçük-gap günlerinde t −3,0 | z>1: HAYIR (vadeli VWAP OOS −3,4 bps). ENKAI vadelisi **31.05.2021–14.04.2023 arasında bültende hiç yok**; OOS kârının yoğunlaştığı dönem. z>2: vadeli VWAP OOS +58 bps (n 33), ama eşik sonradan seçildi | DÜŞÜK / DÜŞÜK |
| (c) ENKAI–USD_{t-1} | 2014–2022'de gerçek (2014–19 t 4,4), **2023-06'dan beri yok** (corr +0,006). 2021–22 hariç 2023+ t 0,4 | HAYIR: gap kontrolleri ve FX momentum kontrolü (USD_t) sonrası t 3,9–4,4 | HAYIR: vadeli VWAP z>1 OOS +10 bps (t 0,9); XU030 hedge'li −8 bps; ileriye dönük etki yok | DÜŞÜK / ÇOK DÜŞÜK |

**Genel hüküm: DÜZELT.** Güven: DÜŞÜK.
- Rakamlar birebir üretildi. İddianın "mekanik değil" kısmı (b) ve (c) için doğru. (a) için yarı doğru: NAV bileşeni gerçek, ama tek başına bilgi taşımıyor.
- İddianın işlenebilirlik çerçevesi ise yanlış:
  - (a) gerçek enstrümanda sıfır.
  - (b)'nin OOS kârı, ENKAI vadelisinin VİOP'ta bulunmadığı döneme denk geliyor.
  - (c) 2023 ortodoks dönüşünden sonra yok.

## 1. Bağımsız yeniden üretim (01_repro.py)
- (a) sig = NAVgap − KCHOLgap → KCHOL intra:
  - Rejim temizliğiyle corr +0,104, t 5,63 (IS 5,44 / OOS 2,50). Legacy temizlikle t 5,38 / 5,08 / 2,50. İddia: 5,0 / 5,0 / 2,1.
  - Regresyon katsayıları: NAV +0,325 (t 4,5), Kgap −0,293.
  - Yılların 13/13'ünde pozitif (2025 +0,015, 2026 +0,104).
- (b) TUR_{t-1} → ENKAI intra: −0,108, t −5,14 (IS −2,48 / OOS −5,07). Aynı sinyal ENKAI gap'ini +0,129 (t 4,9) öngörüyor.
- (c) USD_{t-1} → ENKAI intra:
  - Ham: +0,110, t 4,42 (IS 5,19 / OOS 2,46).
  - 12σ kırpma ile: 3,43 / 4,07 / 1,49. Kırpılan günler (BIST tarihi): 13.08.2018, 21.12.2021, 08.06.2023, 20.03.2025. İddiadaki 3,3 / 1,4 bu kırpmaya bağlı.
- Zaman denetimi:
  - TRY=X günlük kapanış ile h1 00:00 UTC arasındaki medyan fark 2,9 bps; 15:00 UTC ile 4,6 bps. 00:00 konvansiyonu doğrulandı.
  - TUR günlük açılışı, h1 ilk bar açılışıyla birebir eşleşiyor.

## 2. (a) KCHOL — çürütme testleri (03_kchol.py, 04_auction.py, 06_bt.py, 07_extra.py)
**Bileşen ayrıştırması (kritik):**
- NAVgap tek başına → KCHOL intra: corr +0,021 (t 0,8; OOS 0,2).
- −Kgap tek başına: +0,047 (t 2,1; OOS 0,9).
- Fark (sig): t 5,6.
- (X30gap − Kgap): t 3,9. (NAVgap − X30gap): t 2,1.
- Yorum: Bilgi iştiraklerin açılışında değil, KCHOL müzayede fiyatının iştiraklerin eşzamanlı müzayede fiyatlarından **sapmasında**.

**Plasebolar (seçim yanlılığı / ortak faktör):**
- 400 sektör-eşleşmeli Koç-dışı sepet. Her iştirakin yerine aynı sektörden rastgele akran (bankalar, otomotiv, enerji, beyaz eşya), aynı ağırlıklar:
  - t_sig: medyan 2,21, %99 3,98, en yüksek 4,10. Gerçek 5,63.
  - Kgap + X30gap kontrollü sepet t'si: en yüksek 2,07. Gerçek 4,79.
  - OOS t: en yüksek 1,21. Gerçek 2,50.
  - Gerçek sepet dört ölçütte de 100. yüzdelikte. Saf sektör sepetleri (bankalar t 0,9, otomotiv −0,6, enerji 0,8) NAV'ı söndürmüyor.
- Her iştirak tek başına (Kgap kontrollü): TUPRS t 3,7, YKBNK 3,5, ARCLK 3,3, FROTO 2,1, TOASO 1,9. Tek bir bileşen artefaktı değil.
- Diğer holding: SAHOL NAV ayrışması t 1,1 (IS 2,6 / OOS 0,2). İki holdingden biri çalışıyor; seçim yanlılığı hafif.

**Piyasa kontrolü ve endeks açılışı tuzağı (yeni):**
- Yahoo XU030/XU100 günlük açılışı **2014–2015'te bayat**:
  - Endeks gap'inin 20 hissenin müzayede gap ortalamasıyla korelasyonu 0,54–0,73 (2016+ yıllarında 0,89–0,99).
  - Fark, endeksin gün-içi getirisini corr 0,62–0,68 ile öngörüyor. 2021–22'de kısmen yine bozuk (0,20–0,25).
  - Son 60 günde günlük o = m5 06:55 barının kapanışı, yani artık doğru.
- Sonuç: 1. aşamanın ve diğer ajanların "XU030 gap kontrolü" ve "XU030 gap/gün-içi" bulguları 2014–15 ile 2021–22'de kısmen veri artefaktı.
- Hisse-bazlı (Koç dışı 30 VİOP hissesi) piyasa gap'i kontrolüyle NAV katsayısı:
  - +0,36 (t 3,8; IS 2,2 / OOS 3,0).
  - Eşzamanlı hisse-bazlı piyasa gün-içi de eklenince +0,25 (t 3,3; OOS 3,6). İstatistik ayakta.
- Hedge'li versiyonlar:
  - KCHOL − β·XU030 intra: t 5,1.
  - KCHOL − NAV intra (çift): t 5,9.
  - sig → NAV intra: −0,01. Yakınsama tek taraflı; yalnız KCHOL hareket ediyor.

**Uç değer / alt dönem:**
- Spearman 0,107 (IS 0,139 / OOS 0,070).
- |sig| q99, q95 ve q90'da kesilince t 5,4 / 4,8 / 4,2. Yıl jackknife t 4,9–5,7. Kuyruk bağımlı değil.
- Kendi gap'i sıfır olan 32 gün yok sayılabilir. |Kgap| < %0,5 günlerinde t 5,0.
- Sönme:
  - 2014–19 t 5,13. 2020–23 t 2,25. 2023-06+ t 1,53. 2024+ t 1,82.
  - 2 yıllık bloklar: 2014–15 3,8; 16–17 2,1; 18–19 3,6; 20–21 1,6; 22–23 1,6; 24–25 0,8; 2026 1,9.

**İşlenebilirlik — gerçek VİOP KCHOL vadelisi (bu doğrulamanın ana katkısı):**
- Hedef ln(uzlaşma/VWAP) ile korelasyon:
  - 2017+: −0,006 (t −0,3). 2020+: −0,014. 2023-11+: +0,008. Aynı günlerde spot müzayede → kapanış +0,093 (t 4,2).
- Backtest 2020+ (z>0,5):
  - Spot müzayede girişi 8 bps: OOS +9,1 (t 1,0). Bu dolum erişilemez.
  - Vadeli VWAP → uzlaşma: brüt OOS +1,6, 8 bps ile **−6,4 (t −1,2)**; IS −5,7.
- Vadelinin ilk işleminden (06:30, sinyalden ÖNCE) kapanışa: corr −0,066 (t −2,8), katsayı −0,30. Vadeli müzayededen önce zaten fiyatlıyor; ters yönlü bir uyum var.
- Spot müzayede fiyatının vadeli-ima fiyatından sapması (dev):
  - corr(dev, sig) −0,43.
  - Ama −dev spot gün-içini öngörmüyor (t −0,3); sig, dev kontrolünde t 2,3 kalıyor. Basit spot-vadeli baz yanlış fiyatlaması değil.
- Spot h1 (2023-11+):
  - Müzayede → 07:30: +0,182 (t 2,3). 07:30 → kapanış: −0,010.
  - VWAP(07:30+) → kapanış: +0,006.
- m5 (60 gün): giriş 07:00'da +0,14, 07:05'te +0,11, 07:15'te +0,02, 07:30'da 0,00. Etki ilk ~15 dakikada kapanıyor.
- Likidite: KCHOL vadelisinin medyan günlük hacmi 2017/18/19'da 0,1 / 0,7 / 2,7 mn TL; 2021+ döneminde 99–1.715 mn TL. IS (2014–20) kârı vadeliyle hiçbir zaman işlenemezdi.
- Türev hipotez (benim üretimim, veri madenciliği riski):
  - sigF = NAVgap − KCHOL vadeli ilk işlem gap'i → vadeli VWAP → uzlaşma, 8 bps: IS −17,0 (t −1,7), OOS +8,5 (t 1,7).
  - İşaret dönüyor ve VWAP, 06:30–07:00 sinyal-öncesi işlemleri içerdiği için iyimser yanlı. ÇOK DÜŞÜK.

## 3. (b) ENKAI–TUR_{t-1} — çürütme testleri (05_enkai.py, 06_bt.py, 07_extra.py)
- **Gap-fade değil:**
  - Egap + Egap² + |Egap|>%1 kuklası + hisse-bazlı piyasa gap'i kontrolünde TUR −0,090 (t −4,6; OOS −4,6).
  - Yalnız |Egap| < %0,5 günlerinde −0,100 (t −3,0).
  - Kendi gap fade'i ayrıca var (t 4,3), ama TUR'u açıklamıyor.
- **Plasebolar:**
  - EWZ, EZA, EWW, EEM'nin t-1 getirileri → ENKAI intra: |t| ≤ 2,4. TUR hepsinin kontrolünde t −4,4…−5,1 kalıyor. Genel EM faktörü değil.
  - TUR_{t-2}: +0,02 (t 1,2). Gelecekteki TUR_t: +0,27 (doğal; sağlık kontrolü).
- **Ayrıştırma:**
  - TUR'un ABD seansı parçası (o→c, ağırlıklı olarak BIST kapanışı sonrası) t −2,3.
  - "Gece" parçası (önceki ABD kapanışı → ABD açılışı; BIST t-1 seansını içerir) t −3,4.
  - İkisi de X100cc_{t-1} ve Ecc_{t-1} kontrolünde kalıyor. Yalnız "BIST kapanışından sonraki haber" değil; dünkü TL-bazlı hareketin tamamına gün-içi ters tepki.
- **Rejim (en önemli düzeltme):**
  - 2014–2019 t −1,5 (n 1.501; 2019 +0,15 ters işaretli). 2020–2023 t −5,7. 2024 −0,001, 2025 −0,04. 2026 −0,135 (n 207).
  - İddiadaki "IS −2,5" yalnız 2020'yi içerdiği için anlamlı çıkıyor.
- **Uç değer:** |TUR| ≤ q99 iken t −2,4; ≤ q95 iken −1,9. Spearman −0,064.
- **Ortak faktör:**
  - 47 hisse taramasında ENKAI 1. sırada (t −5,1). Ama THYAO −4,4, SISE −3,7, FROTO −3,6, TKFEN −3,6, EREGL −3,3, ALARK −3,2.
  - Bu bir USD-gelirli / ihracatçı faktörü: ihracatçı sepeti intra t −3,9; ihracatçı − iç talep t −3,1.
  - ENKAI, eşzamanlı ihracatçı ve iç talep gün-içi kontrolünde de −0,06 (t −4,0) koruyor; ENKAI'ye özgü bir pay var.
- **(c) ile aynı kanal:**
  - TUR + USD + gap + gecikme kontrollerinde TUR'un tam dönem t'si −1,3. IS'te **+1,8 (ters işaret)**, OOS'ta −3,8.
  - 2014–21'de TL serbest dalgalanırken bilgi USD'de; KKM / yönetilen kur döneminde (2021–23) TUR'da.
- **İşlenebilirlik:**
  - ENKAI pay vadelisi VİOP bülteninde 31.05.2021 → 14.04.2023 arasında yok. Aynı dönemde KCHOL vb. pay vadelilerinin satırları var; yani veri eksikliği değil, kontrat yok. 2019-11 öncesinde de yok.
  - z>1, 8 bps:
    - Spot OOS +21,5 (t 1,6). En iyi 10 gün OOS toplam kârın %122'si.
    - Yıllar: 2021 +77, 2022 +88; 2023 +7, 2024 −5, 2025 +13, 2026 −23.
    - Vadeli VWAP → uzlaşma (mevcut günler) OOS −3,4 (t −0,4), brüt +4,6. Vadeli Fo→Fc (2024-11-19+; pay vadelisi akşam seansı yok) −1,7 (n 112).
  - z>2, 8 bps:
    - Spot OOS +130 (t 4,5, n 57). Vadeli VWAP OOS +57,7 (t 2,1, n 33). Vadeli Fo→Fc 2024-11-19+ +169 (t 2,5, n 20).
    - XU030 vadeli VWAP (3 bps): IS +26 (t 2,0), OOS +30 (t 1,5).
    - Uyarılar: eşik sonradan seçildi ve n küçük. Etki piyasa geneli; büyük TUR hareketinden sonra endekste de gün-içi dönüş var. Long bacak baskın (OOS +138 / short +121).

## 4. (c) ENKAI–USDTRY_{t-1} — çürütme testleri
- **FX momentumu değil:** Eşzamanlı USD_t (seans t'yi kapsar) kontrolünde USD_{t-1} +0,205 (t 4,4). FX otokorelasyonu 0,10 (t 1,7). USD_t'nin ENKAI intra ile ilişkisi ≈0.
- **Gap-fade değil:** Gap kontrolleriyle +0,21 (t 3,9). Küçük-gap günlerinde t 3,9.
- **Rejim:**
  - 2014–19 t 4,4. 2020–23 t 3,0. 2023-06+ corr +0,006 (t 0,3). 2024+ −0,026.
  - Yıllık: 2023 +0,04, 2024 −0,10, 2025 +0,02, 2026 +0,06.
  - **Ortodoks dönüşten sonra yok.** 2021–22 hariç tutulunca 2023+ t 0,4.
- **Uç değer:** q99'da kesince t 5,0 (yükseliyor: KKM gibi en uçlar karışık işaretli); q95'te 2,7. Spearman 0,063. Orta-büyük hareketlere bağlı.
- **Plasebo FX:** ZAR=X_{t-1} → ENKAI intra t 3,3; EURTRY 3,35; BRL ve MXN ≈0. Kanalın bir kısmı küresel USD gücü / EM-FX.
- **İşlenebilirlik:**
  - z>1, 8 bps: spot OOS +50 (t 2,7), en iyi 10 gün kârın %97'si.
  - Vadeli VWAP → uzlaşma OOS +10 (t 0,9). ENKAI−XU030 hedge'li −8,3. Fo→Fc (2024-11-19+) +43 (t 1,4, n 55).
  - z>2: OOS +30 (t 0,7); eşikte tutarsız.

## 5. Yan bulgular (diğer ajanları etkiler)
1. **Yahoo endeks açılışı (XU030/XU100) 2014–2015'te bayat, 2021–22'de kısmen bozuk.** Hisse-bazlı müzayede gap ortalamasıyla yıllık korelasyon 0,54 / 0,73 (2014 / 15) ve 0,90 / 0,80 (2021 / 22); diğer yıllarda 0,89–0,99. Endeks gap/gün-içi ayrıştırması ve endeks-gap kontrolü bu yıllarda yanıltıcı; hisse-bazlı piyasa gap'i kullanılmalı.
2. **ENKAI pay vadelisi 31.05.2021–14.04.2023 arasında listede yok.** 2021–22 krizinde ENKAI üzerindeki her VİOP stratejisi işlenemezdi.
3. **Pay vadelisi likiditesi 2020 öncesinde çok düşük** (KCHOL 2017–19 medyan 0,1–2,7 mn TL/gün; ENKAI 2020 1,7 mn TL). IS dönemi backtestleri VİOP ile gerçekleştirilemezdi.
4. Vadeli ile spot müzayede fiyatı arasında, önceki günün bazına göre medyan 30–36 bps fark var. Spot müzayede fiyatı gürültülü.

## 6. TradingView
- Spot: BIST:KCHOL, BIST:ENKAI, BIST:TUPRS, BIST:YKBNK, BIST:FROTO, BIST:ARCLK, BIST:TOASO.
- Sürücüler: NASDAQ:TUR, FX:USDTRY.
- Hedge: BIST:XU030D1!.
- VİOP pay vadelisi TV kodları doğrulanmadı ('?').

## 7. Sınırlamalar
- Vadeli bülteninde gün-içi zaman damgası yok. VWAP gün boyu ortalama: (a) için sinyal-öncesi 06:30–07:00 işlemlerini içeriyor (iyimser yanlı); buna rağmen sıfır çıkıyor.
- 2024-11-19 öncesinde pay vadelisinde akşam seansı olup olmadığı bültenden kesin ayırt edilemedi. Bu yüzden Fo girişi yalnız 2024-11-19+ için kullanıldı.
- m5 yalnız 60 gün, h1 2023-11+. 2023 öncesinde (a)'nın dakika-düzeyi kapanması doğrudan değil, vadeli VWAP üzerinden dolaylı gösterildi.
- Spread ve derinlik ölçülmedi. 8 bps varsayımı, kârın yoğunlaştığı kriz günlerinde iyimser olabilir.
