# v_C4C5_b — 2. aşama ÇÜRÜTME: Çin/HK sürücüleri → TRALT / KRDMD
Kod: `out/code_v_C4C5_b/` (vb.py: kendi hizalama/temizlik + kendi SHFE roll serisi; ll.py ve vlib.py import edilmedi). Loglar `log_s01..s14.txt`.
Yeni veri: VİOP bülteninden (data/viop, 2017-03 → 2026-10) TRALT/KOZAL ve KRDMD pay vadelisi satırları → `viop_ssf_sel.parquet`. Aktif kontratı önceki günün en yüksek açık pozisyonuna göre seçtim. Böylece **gerçek enstrüman** olan VİOP vadelisinin açılış→kapanış getirisiyle test yapılabildi.

## Hüküm: DÜZELT
İddialar sayısal olarak birebir üretildi. Ancak (a)'nın orijinal hali ileriye bakıyor, (b) yalnızca belli bir dönemde var, (c) yanlış sütundan okunmuş. Güven:
- (a) istatistiksel bağ: ORTA
- (a) ve (b) işlenebilirlik: DÜŞÜK
- (c) "SHFE üstünlüğü": RED

## 1. Yeniden üretim (s01)
- 1787.HK D_t → TRALT gün-içi: r=0,095, t=4,14, n=2010. Net 10 bps maliyetle IS +19,8 bps (Sharpe 1,38), OOS +10,7 bps (Sharpe 0,55).
- 2899.HK: t=3,84. 600547.SS: t=3,34. 601899.SS: t=2,93.
- SHFE HC (kendi roll serim, 2018-05+) → KRDMD gün-içi: t=3,36, OOS +11,7 bps (Sharpe 0,65). IS +1,7 bps; 1. aşama farklı başlangıç tarihi ve roll kuralıyla −10,5 bps bulmuştu. Her iki durumda da IS pozitif değil.

## 2. Zamanlama ve açılış fiyatı
**Yahoo günlük açılışı gerçek açılış müzayedesi fiyatı (s02).** m5 06:55 barıyla 60/60 gün birebir; h1 06:30 barıyla %99,6 eşleşiyor. Açılıştan sonraki ilk 5 dakikada medyan |hareket| TRALT'ta 56 bps. Yani giriş anı önemli.

**HK kapanışı 08:00–08:10 UTC, BIST açılışı 07:00 UTC.** Orijinal 1787 sinyalinde ileriye bakma doğrulandı. Uzun dönem ayrıştırmada (s04):
- 1787 gap'i (önceki kapanış → 01:30 açılış): t=1,97
- 1787 gün-içi (01:30→08:10, örtüşmeli): t=3,62
- 2899 gap'i: t=0,13

**SSE kapanışı 07:00 UTC, müzayede 06:55–07:00 UTC.** 2023-11+ döneminde 600547 için P(06:30) ve P(07:00) aynı sonucu veriyor (r=0,099 / 0,099). Yani 600547 kapanış sinyali pratikte açılıştan önce biliniyor. **En temiz uzun dönem sinyal bu** (s05).

**HK h1 verisinin güvenilirliği.** h1 son bar kapanışı ile günlük kapanış arasındaki fark 2024-Q3 öncesinde 1787 için %90'lık dilimde 160–250 bps, 2899 için medyanda 50–80 bps. 2024-Q4'ten itibaren sıfır. Bu yüzden HK anlık testlerini yalnızca 2024-09+ için yaptım (s05).

**Açılış öncesi HK anlık fiyatı → TRALT spot gün-içi (2024-09+, n=541).**

| Sinyal | r | t | net 10 bps | net 15 bps |
|---|---|---|---|---|
| 2899 P(06:30) | 0,129 | 2,77 | +19,4 (BT t 1,44) | +14,4 |
| 2899 yalnız Asya seansı (01:30→06:30) | 0,152 | 3,74 | — | — |
| 1787 P(06:30) | 0,110 | 2,42 | +8,5 | +3,5 |
| 600547 P(06:30) | 0,082 | 1,67 | ≈0 | — |

**Ortak faktör kontrolü (s06, s13):**
- Gece COMEX altını (GC 15:00 t-1 → 06:30 t) TRALT gün-içini tahmin etmiyor: t=0,49.
- 2899, ABD t-1 sinyalleriyle (GDX, GC, EEM), TRALT'ın kendi gecikmesi ve gap'iyle birlikte regresyona girince t=2,0–2,2'ye düşüyor. 1787 bu kontrollerle t=1,9.
- 2899 ile GDX_{t-1} arasındaki korelasyon 0,43; bilginin bir kısmı ABD'den taşınıyor.
- 2024-09+ döneminde TRALT gün-içini GDX_{t-1} (t=2,69) ve EEM_{t-1} (t=2,65) de tahmin ediyor. Bu rejime özgü bir altın momentumuna işaret ediyor.
- Yarıyıllık r: 0,04 / 0,19 / 0,03 / 0,10 / 0,28. İstikrarsız.

**TRALT h1 (2025-11+, n=230).** 2899 06:30 sinyalinin etkisi gün içine yayılmış: açılış→07:30 r=0,097, 07:30→kapanış r=0,107 (t=1,56). 07:30 girişte net 10 bps maliyetle +7,4 bps.

## 3. Plasebo, seçim yanlılığı, uç değer, alt dönem — (a) 600547 → TRALT (s03, s04, s14)
**Plasebo matrisi:** 27 Asya sinyali × 48 BIST gün-içi hedefi.
- Altın dışı 20 Asya sinyalinin TRALT için t ortalaması −0,17 (aralık −1,5…+1,3).
- Altın sinyalleri altın dışı hisseleri tahmin etmiyor. Örneğin 600547 için diğer 45 hissede t>2 olan hisse sayısı 0.
- Sonuç: ilişki altına özgü; genel bir Asya etkisi ya da açılış artefaktı değil.

**İstatistiksel sağlamlık:**
- Dairesel kaydırma null'u (500): gerçek t=3,34, null %99 eşiği 2,98, p=0,002.
- Winsorize %1: t=3,43. Winsorize %5: t=4,22. Spearman 0,085 > Pearson 0,064. Uç değere bağlı değil.
- Çin uzun tatil sonrası günler çıkarılınca t=3,15.
- Bayat açılış (o == önceki c) günlerinde r=0,20 (n=250), normal günlerde r=0,052 (t=2,74).

**IS ve OOS:**
- IS (2014–20): r=0,055, t=2,17. OOS (2021–26): r=0,070, t=2,61.
- Yıllık korelasyon 13 yılın 11'inde pozitif (2015 ve 2022 negatif).
- Kontroller (kendi gap'i ve gecikmesi, XU100, GC_{t-1}, GDX_{t-1}) sonrası t=2,99.
- At yarışında 600547 (t=2,03) SSE altın ETF'ini (518880, t=1,11) geçiyor. 518880'in kendisinde IS t=4,00 ama OOS t=0,79: bilgi altın fiyatında değil, Çin altın hissesinde.

**Ekonomik büyüklük:** brüt 18,6 bps/işlem. Net: 8 bps maliyetle +10,6, 10 bps'te +8,6 (BT t 1,59), 15 bps'te +3,6. OOS net 10 bps'te +6,6 (BT t 0,79).
- En iyi 10 işlem çıkarılınca +5,3 bps.
- Eşik |s|>%1 ile OOS +33,7 bps (t=3,06) çıkıyor. Ancak 4 eşik denendi ve seçim sonradan yapıldı; kanıt sayılmaz.

## 4. Gerçek enstrüman: VİOP pay vadelisi (s09–s12)
**Likidite yeterli.** Yıllık medyan günlük işlem hacmi:
- TRALT: 2024'te 474 mn TL, 2025'te 556 mn TL, 2026'da 1,4 mlr TL (14–26 bin işlem).
- KRDMD: 467–771 mn TL.
- 2018–20'de çok illikit: KOZAL 0,2–16 mn TL.
- VİOP açılış seansı ise ince: medyan 40–280 bin TL, birkaç işlem.

**Vadeli gün-içi ile spot gün-içi korelasyonu 0,93.** Vadeli 06:30 UTC'de (09:30 TSİ) açılıyor, spot müzayededen önce.

**Açılıştan önce bilinen sinyallerle vadeli sonuçları (2024-09+):**

| Sinyal → vadeli | r | t | net 10 bps | net 15 bps |
|---|---|---|---|---|
| 2899 P(06:30) → TRALT vadeli | 0,173 | 3,87 | +24,8 (BT t 1,88) | +19,8 |
| 1787 P(06:30) → TRALT vadeli | 0,114 | 2,39 | +8,2 | — |
| 600547 P(06:30) → TRALT vadeli | 0,095 | 1,88 | ≈0 | — |
| HC P(06:15) → KRDMD vadeli | 0,087 | 2,43 | +13,8 (BT t 1,32) | +8,8 |

**Vadeli sonuçları spottan iyi görünüyor; bunun bir kısmı vadeli açılış fiyatının bayatlığından geliyor:**
- KRDMD'de vadelinin spota göre fazlasını (fint−sint) ABD t-1 sinyalleri tahmin ediyor: SLX t=3,21, ES t=3,41. Bu genel bir açılış bayatlığı.
- TRALT'ta spot gap'i vadeli gün-içini tahmin ediyor (t=2,25). 2899 sinyali vadeli fazlasını da tahmin ediyor (t=2,2–2,6).
- Bu fazla ancak ince açılış seansında dolum olursa yakalanabilir; iyimser bir varsayım.
- Gerçekçi tahmin olarak spot müzayede sonuçlarını kullanmak gerekir.

## 5. (b) SHFE HC → KRDMD (s07, s10, s14)
- **İstatistik sağlam:** dairesel null p=0,002; en büyük %1 |gün-içi| günleri çıkarılınca t=3,97.
- **Çeliğe özgü:** diğer hedefler arasında yalnızca EREGL anlamlı (t=2,69); 47 hissenin medyan t'si −0,16.
- Asya ve çelik kontrolleri eklenince (FMG, Baosteel, Shenhua, CMOC, SSE, kendi gap'i ve gecikmesi) HC t=2,38'de kalıyor.
- **Ama KRDMD gün-içi genel olarak "Asya duyarlı":** 27 Asya sinyalinin medyan t'si 2,09.
- **Bayat açılış etkisi yok:** normal açılış günlerinde t=3,26. Göreli tik büyüklüğü 2018+ döneminde sorun değil.
- **Alt dönemler:** 2018–20 r=0,025 (t 0,63) · 2021–23 r=0,113 (t 3,53) · 2024–26 r=0,046 (t 1,37). IS t=0,59, OOS t=3,77.
- 2021–23'te gapD (gece seansı açılış gap'i, 07:00–13:00 UTC t-1, yani BIST t-1 seansı sırasında) t=2,94 iken 2024–26'da −1,34. İşaret istikrarsız.
- **Temiz sinyal (P 06:15 UTC, 60 dk, 2023-08+):** spot t≈1,45. Bu dönem zaten zayıf olduğu için 2021–23'teki etkinin zamanlamasını doğrulamak mümkün değil.
- **Maliyet sonrası:** net 10 bps'te +8,5, 15 bps'te +3,5. En iyi 20 işlem çıkarılınca negatif.

## 6. (c) Haftalık altın (s08; kendi AU roll serim, ortak örneklem 2018-11+)
- bist_pairs.csv'de AU haftalık r=0,286, kısmi 0,317. GC haftalık r=0,268, kısmi 0,242 (farklı örneklem). Rapordaki 0,29/0,11 rakamları gap_corr sütunundan okunmuş (0,290 / 0,113).
- XU100 kontrollü kısmi korelasyon (AU / GC) ve at yarışı t'leri, çapaya göre:

| Çapa | AU kısmi | GC kısmi | Fark [%95 GA] | t_AU | t_GC |
|---|---|---|---|---|---|
| Pzt | 0,218 | 0,228 | −0,010 [−0,06; +0,04] | 1,28 | 1,95 |
| Sal | 0,276 | 0,289 | −0,013 [−0,08; +0,05] | 1,37 | 2,11 |
| Çar | 0,322 | 0,313 | +0,009 [−0,06; +0,07] | 2,14 | 1,52 |
| Per | 0,392 | 0,350 | +0,041 [+0,002; +0,085] | 3,96 | 1,07 |
| Cum | 0,324 | 0,219 | +0,105 [+0,03; +0,20] | 4,78 | −0,47 |

- Çin primi (AU−GC−CNH) kısmi korelasyonu Pzt'de 0,05, Cum'da 0,22: çapaya bağlı.
- Günlük: GC 0,229 > AU 0,174. BIST t seansını kapsayan AU_{t+1} penceresi, GC'ye ek bilgi taşımıyor (t=−0,26).
- 2021–23'te bağ zayıf (Cuma çapasında AU 0,11 / GC −0,03).
- Sonuç: senkron altın bağı gerçek. "SHFE > COMEX" iddiası 5 çapadan 2'sine özgü; COMEX:GC1! yeterli vekil.

## Sınırlamalar
- Bu oturumda yaklaşık 200 tanı amaçlı varyant çalıştırıldı (plasebo matrisi hariç); FDR uygulanmadı. 2899 h1 bulgusu sonradan yapılan arama sonucu bulundu; Bonferroni ile (~20 varyant) spot t=2,77 anlamlılığını yitiriyor.
- VİOP gün-içi tik verisi yok; vadeli açılış saati ve dolum varsayılarak hesaplandı.
- TRALT h1 yalnızca 2025-11+ (KOZAL h1 Yahoo'da 404). HK h1 yalnızca 2024-09+ güvenilir.
