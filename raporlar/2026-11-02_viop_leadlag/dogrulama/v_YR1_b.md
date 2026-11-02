# v_YR1_b: YR1'i çürütme denemesi (2. aşama). SAHOL/AKBNK oranı ve KCHOL NAV iskontosu

Kod `out/code_v_YR1_b/` altında, 01'den 10'a sırayla çalışır. `vb.py` bağımsız yazıldı; ll.py'yi ve 1. aşamanın vlib.py'sini import etmiyor.
Ara sonuçlar: `res_*.csv`, `res_*.parquet`, `res_factor.txt`.

**Temizlik**
- Bayat gün: v<=0 ve h==l.
- Eşik fiyat bazında ve rejime bağlı: 2020-03-13 öncesi |basit getiri|>%20,5, sonrası >%10,5. Taban günleri (−%10) korunuyor.
- Getiriler adj ile tutarlı: f=adj/c, gap=log(o·f/adj₋₁), intra=log(c/o).
- 2014 öncesi açılış kullanılmadı.

**Muhasebe**
- pnl_t = pos_{t−2}·gap + pos_{t−1}·intra.
- Maliyet: (1+|β|)·c/2·|Δpos|.
- Getiri, "maruz gün" başına veriliyor; çıkış gününün gap'i dahil.
- t değerleri Newey-West (5 gecikme), tüm günler üzerinden.

## Hüküm: DÜZELT
SAHOL/AKBNK çürütülemedi. Etki gerçek ve bu çifte özgü, ancak büyüklük ve sağlamlık iddiası şişik. KCHOL NAV DÜŞÜK güvende kalıyor.

## 1. Temel tekrar (β250, z60>1,5, t+1 açılış)
| maliyet | 2014–17 | 2018–20 | 2021–23 | 2024–26 | IS | OOS |
|---|---|---|---|---|---|---|
| 0 | 13,5 (t 2,52) | 20,0 (2,81) | 19,4 (2,47) | 27,6 (3,07) | 16,6 (3,76) | 22,7 (3,82) |
| 8 | 10,8 (2,04) | 17,2 (2,45) | 16,7 (2,14) | 24,8 (2,80) | **13,9 (3,19)** | **20,0 (3,40)** |
| 15 | 8,3 (1,61) | 14,7 (2,13) | 14,4 (1,86) | 22,3 (2,55) | 11,4 (2,66) | 17,6 (3,02) |
| 30 | 3,2 (0,63) | 9,5 (1,41) | 9,3 (1,22) | 17,1 (1,99) | 6,2 (1,49) | 12,4 (2,17) |

Birim: bps/maruz gün (t).

- İddiadaki rakamlar kaynağın muhasebesiyle ortaya çıkıyor: Pi≠0 günlerinin ortalaması IS 20,5, OOS 26,4.
  - Doğru muhasebeyle 13,9 / 20,0. İddia (18 / 27) yaklaşık %30 şişik; t değerleri doğru.
  - "15 bps'te OOS +25" yerine +17,6 (t 3,0).
- Yıllar 12/13 pozitif; yalnız 2015 −2,4.
  - Tek tek yıllar zayıf: yalnız 2014, 2018, 2023 ve 2026'da t>2.
  - 2024–25 tek başına 16,3 bps (t 1,63). 2026 tek başına 51 bps (t 2,75).
  - 2026 hariç OOS: 16,6 (t 2,69).
- İşlemler: IS 128, OOS 113; ortalama 4,7 gün; isabet %72 / %78. İşlem bazında t: IS 4,2, OOS 4,4.

## 2. Çürütme testleri (SAHOL/AKBNK)
**Plasebo** (8 bps; gerçek değerler IS t 3,19 / OOS t 3,40):
- Dairesel kaydırma (400 çekiliş): t ort. −0,69 / −0,45, sd 0,95 / 0,89. p=0.
- İşlem bazında rastgele yön (400): −0,62 / −0,49. p=0.
- Rastgele tarih + yön, süre profili korunarak (300): −0,66 / −0,49. p=0.

**Bayatlatılmış sinyal** (karar k gün gecikmeli; OOS t):

| k | 0 | 1 | 2 | 3 | 5 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|---|---|
| OOS t | 3,40 | 2,12 | 2,10 | 0,42 | −0,37 | −1,15 | −0,53 | −0,71 |

IS'te k=2'de t 0,89'a iniyor. Doğal bir 1–3 günlük sönüm var, uzak gecikmelerde sahte yapı görünmüyor.

**Evren** (47 hissenin 2.070 geçerli yönlü çifti, aynı kural):
- Null dağılım: IS t ort. −0,20 (sd 1,26), OOS t −0,64 (sd 0,90).
- SAHOL/AKBNK min(IS, OOS) t'ye göre **1/2070**.
- IS ve OOS'ta t≥3 olan tek çift bu. İkisinde de ≥2 olan 2 çift var, ikisi de aynı ekonomik çift (ters yönü dahil); bağımsızlık altında beklenen 0,16.
- Korelasyonu eşlenmiş 42 çift (corr 0,72±0,1): OOS t ort. 0,00.
- Grup çiftleri tutmuyor: KCHOL/YKBNK 0,37, KCHOL/TUPRS 0,38, SAHOL/ENJSA 0,22, ISCTR/SISE −0,94 vb.

**Ortak faktör.** SAHOL/AKBNK pnl'i şu faktörlerle regres edildi: SAHOL/XU030, AKBNK/XBANK, XBANK/XU030 ve KCHOL/XU030 aynı kurallı strateji pnl'leri; 47 hisselik kesitsel 5 günlük dönüş faktörü; XU100; |XU100| (demean edilmiş).
- Alfa IS 4,4 bps/gün (t 3,11), OOS 8,2 (t 3,56). Ham ortalamalar 4,8 / 7,3.
- Genel faktörler etkiyi açıklamıyor.
- SAHOL/XBANK, SAHOL/GARAN ve SAHOL/YKBNK varyantları da eklenince OOS alfa yine t 3,63. OOS'ta etki diğer bankalara değil AKBNK'ya özgü.
- IS'te SAHOL her bankaya karşı dönüyordu (banka b'leri ortalama IS t 2,1), OOS'ta yalnız AKBNK'ya karşı (diğer bankalar OOS t 0,3). Bu, "SAHOL NAV'ı ≈ AKBNK" mekanizmasıyla uyumlu.
- Bacaklar: SAHOL bacağı IS t 2,84 / OOS 3,78, AKBNK bacağı 1,72 / 1,37.
- Sapmanın kaynağı: AKBNK'nın hareket ettiği (SAHOL'ün geride kaldığı) ve SAHOL'ün kendi hareket ettiği girişler IS ve OOS'ta ikisi de kârlı (işlem t 2,5–3,9).

**Uç değer**
- En iyi 10 işlem çıkarılınca işlem t: IS 2,80, OOS 2,96 (en iyi 5 hariç 3,46 / 3,67).
- %2,5 winsorize: OOS t 4,38.
- Kriz pencereleri çıkarılınca (2018-08/09, 2020-03/04, 2021-11…2022-01, deprem, 2023 seçimi, 2025-03/04, 2026-09/10): IS t 2,93, OOS 2,49. 2021–23 bu durumda t 1,29.
- Limit (±%9,5) günleri pnl'de sıfırlanınca OOS t 3,50; etkisi yok.
- Temettü pencereleri [−2, +5] sıfırlanınca IS 2,99, OOS 2,96.

**Mekanik bid-ask ve dolum**
- Brüt kârın %25–26'sı giriş günü gün içinden, %74–75'i sonraki günlerden geliyor.
- 2023-12+ döneminde 10:30 TSİ giriş + 10:30 çıkış 24,8 bps (t 2,84); açılış girişi 24,1 (2,76). Açılış iyimserliği yok.
- 482 açılış işleminden yalnız 1'inde açılış tavan/taban kilitli (2023-05-16). Ertelenince değişiklik yok.
- Not: Yahoo açılışı günlerin ~%10'unda önceki kapanışa eşit. Ancak h1 ilk bar açılışıyla %99,9 aynı ve 10:30 testi bunu nötrlüyor.

**Veri madenciliği** (105'lik ızgara: pencere 20–250 × eşik 1–2 × β ∈ {1, 120, 250}):
- IS t medyanı 3,26 (%95'i >2).
- **OOS t medyanı 1,96, yalnız %49'u >2** (%96'sı >0). OOS bps medyanı 14,4 (IQR 8,9–20,3). w=250'de OOS t ≈0–1,4.
- **Dürüst seçim:** IS'te en iyi spesifikasyon (β1, w30, eşik 1,25; IS t 5,08) OOS'ta 1,66 veriyor; IS'in ilk 5 spesifikasyonu OOS 1,66–2,76.
- 40 korelasyon-eşli plasebo çifti: ızgara-medyan OOS t ort. −0,18, en yüksek 0,95. IS-seçimli OOS ort. −0,11, en yüksek 2,09.
  - Yani SAHOL/AKBNK yüzeyinin tamamı yüksek, ama IS seçimiyle beklenen OOS t ~2, 3,4 değil.
  - En yüksek plasebo yüzeyleri de SAHOL–banka çiftleri.
- Histerezis alt ızgarası (32 spesifikasyon): OOS t 0,38–3,72.
- **Temizlik duyarlılığı:** −%10 taban günleri yanlışlıkla sinyalden de atılınca (log eşik hatası) OOS t 2,26'ya, 2021–23 t 0,94'e iniyor. 2021–23 katkısı büyük hareket günlerindeki sapmalara dayanıyor.

**VİOP vadelileri** (kendi sürekli serim: ön ay, vadeye ≤3 iş günü kala devir, **devir maliyeti dahil**; sinyal spot):
| dolum | maliyet | 2017–20 | 2021–23 | 2024–26 | OOS 2021–26 |
|---|---|---|---|---|---|
| t+1 ilk işlem | 8 | 1,55 | 1,83 | 2,29 | **2,75** (17,0 bps) |
| | 15 | 1,21 | 1,53 | 1,97 | 2,32 (14,3) |
| | 30 | 0,47 | 0,89 | 1,23 | 1,39 (8,5) |
| t+1 tüm gün VWAP | 8 / 15 / 30 | 1,65 / 1,23 / 0,31 | 1,57 / 1,26 / 0,59 | 2,83 / 2,52 / 1,81 | 2,85 / 2,41 / 1,47 |
| t+1 uzlaşma | 8 / 15 | 0,89 / 0,43 | 1,01 / 0,73 | 2,71 / 2,42 | 2,32 / 1,92 |

- Tik maliyeti eklenince (taban 6 + 1 tik/fiyat) vadeli OOS t 2,58. Taban 15 + tik ile 2,03; 2021–23 bu durumda 1,19.
- Tik/fiyat oranı: SAHOL 2014–21'de 10–12 bps, AKBNK 15–17 bps; 2024+ ikisi de 1–2 bps.
- Ön ay medyan günlük işlem değeri, SAHOL: 2017 0,3, 2019 2,5, 2021 65, 2024 636, 2026 1.309 mn TL.
- **2014–2020 VİOP'ta işlenebilir değil, 2021–23 vadeliyle zayıf** (t 1,0–1,9).

## 3. KCHOL NAV iskontosu (kendi NAV inşam; ağırlıklar kaynakla aynı, model girdisi)
- 8 bps: IS 2,95 bps/maruz gün (t 0,98), OOS 11,2 (t 2,04).
  - Alt dönemler: 2014–17 t 1,05, 2018–20 0,40, 2021–23 1,25, 2024–26 1,64. **Hiçbir alt dönem anlamlı değil.**
- Maliyet: 15 bps'te OOS t 1,79, 30 bps'te 1,26. XU030 bacağı 3 bps ile 2,13.
- 11/13 yıl pozitif, ama yıllık değerler küçük.
- Bayat sinyal OOS t: k=1 1,40, k=2 1,39, k=5 1,54, k=20 −0,09.
- Plasebo: dairesel kaydırmada OOS p 0,01, rastgele yönde 0,003 (OOS'ta yapı var). IS p 0,07.
- Uç değer: IS'te en iyi 3 işlem kârın %70'i; bunlar çıkınca IS işlem t 0,52. OOS'ta en iyi 3 hariç 2,14.
- Kriz hariç OOS t 2,64.
- 45'lik NAV × pencere × eşik ızgarası: OOS t medyanı 1,90 (%42'si >2), IS medyanı 1,66 (%20'si >2).
- 10:30 girişi (2023-12+): t 1,68; açılış girişi 1,43.
- 1. aşamanın vadeli testi 2021–26 için t 1,0–1,5 vermişti. **DÜŞÜK** güven teyit edildi. İddiadaki OOS +19 (t 3,0) tekrarlanmıyor; +11 (t 2,0).

## 4. Düzeltilmiş iddia
- **SAHOL/AKBNK [YÜKSEK, ilişki olarak]**
  - Oran, 60 günlük ortalamasından 1,5σ sapınca t+1 açılışta ters spread pozisyonu alınıyor (β250).
  - 8 bps'te IS 2014–20 +14 bps/maruz gün (t 3,2), OOS 2021–26 +20 (t 3,4); 15 bps'te +11 / +18.
  - Dört alt dönemin hepsi pozitif (t 2,0–2,8). Plasebo, evren (1/2070), genel faktör kontrolü, uç değer, 10:30 dolumu ve temettü testlerinden geçiyor.
  - **Işlenebilir beklenti daha düşük:** parametre-dürüst OOS t ~2 ve ~14 bps. VİOP'ta devir maliyeti dahil 2021–26 t 2,3–2,9 (8–15 bps), 30 bps'te 1,4.
  - 2014–20 VİOP'ta işlenemezdi. 2021–23 vadeliyle zayıf. 2026 en güçlü yıl.
- **KCHOL NAV [DÜŞÜK]:** OOS +11 bps (t 2,0), IS t 1,0. Hiçbir alt dönem anlamlı değil; vadeliyle t 1,0–1,5.
