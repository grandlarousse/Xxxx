# v_YR1_a: YR1 için bağımsız doğrulama (SAHOL/AKBNK oranı + KCHOL NAV iskontosu)

Kod `out/code_v_YR1_a/` altında, 01'den 11'e sırayla çalışır. `vlib.py` kendi temizlik ve hizalama kodum, ll.py'yi import etmiyor. `fut.py` VİOP bülteninden sürekli vadeli serisi kuruyor. Ara sonuçlar `res_*.csv` dosyalarında.
Temizlik: bayat gün = v<=0 ve h==l. Kurumsal işlem eşiği rejime bağlı: 2020-03-13 öncesi ±%20,5, sonrası ±%10,5. 2014 öncesinin açılış verisi atıldı. cc getirisi adj üzerinden, gün içi getiri log(c/o). Son veri günü 30.10.2026.
Muhasebe: pozisyon t kapanışında belirleniyor. Açılışla girişte pnl_t = pos_{t-2}·gap_t + pos_{t-1}·intra_t. Maliyet nominal ağırlıklı alınıyor: (1+|β|)·bps/2, her yön değişiminde. t değerleri Newey-West (5 gecikme) ve tüm günlerin pnl serisinden hesaplandı.

## Sonuç: DÜZELT
| | İddia | Bağımsız sonuç | Hüküm |
|---|---|---|---|
| SAHOL/AKBNK z60>1,5, giriş t+1 açılış, 8 bps | IS +18 (t 3,1), OOS +27 (t 3,5) | Kaynağın muhasebesiyle IS +19,7 (t 3,39), OOS +28,1 (t 3,46): **yeniden üretildi**. Doğru muhasebeyle (çıkış günü gap'i ve çıkış maliyeti dahil) IS +13,9 (t 3,17), OOS +22,1 (t 3,64) | Etki gerçek. "bps/aktif gün" rakamı %20–30 şişik, t değerleri doğru |
| 15 bps'te OOS | +25 | +19,7 (t 3,28). 30 bps'te +14,5 (t 2,46). 15 bps + tik maliyetiyle +18,1 (t 3,03) | Kabul |
| 13 yılın 12'si pozitif | 12/13 | 12/13 (yalnız 2015 −2,5) | Kabul |
| 6 parametre setinde t 2,5–4,3 | | Bu 6 set tekrarlandı. Ancak 24'lük ızgarada OOS t 0,47–3,64, yalnız %58'i t>2. w=250'de OOS t 0,5–1,2 | Seçilmiş aralık, düzelt |
| 19 grup dışı çiftte ortalama t 0,24 | | 47 hissenin 2.070 yönlü çiftinde ortalama OOS t −0,46. corr≥0,6 olan 66 çiftte 0,11. SAHOL/AKBNK min(IS,OOS) t'ye göre **1/2070**. BH-FDR'den (2.070 test) yalnız SAHOL/AKBNK (t 4,67) ve AKBNK/SAHOL (4,21) geçiyor | Güçlü biçimde kabul |
| KCHOL NAV, OOS 2021–26 | +19 bps (t 3,0) | Kaynak muhasebesiyle +13,4 (t 2,17). Doğru muhasebeyle +10,8 (t 1,97). 15 bps'te t 1,73, 30 bps'te 1,21 | **Zayıf, düzelt** |
| KCHOL NAV, IS 2014–20 | t 1,9 | t 1,21 (kaynak muhasebesiyle 1,52) | Anlamsız |
| 12 kombinasyonda OOS t 1,7–3,7 | | Aynı 12 kombinasyonda 1,37–3,29, hepsi pozitif. 16'lık ızgarada 0,26–3,29, %25'i t>2 | Düzelt |
| NAV plasebosu t≈0 | | REL (KCHOL−β·XU030) z'si: OOS t −0,36…0,57. Koç dışı 300 rastgele 8'li sepet: OOS t ortalama −0,20 (sd 0,51), hiçbiri ≥1,97 değil | Kabul |

## SAHOL/AKBNK ayrıntı
- **İşlem profili** (8 bps): IS'te 125 işlem, OOS'ta 107. Ortalama tutma süresi 4,8 gün, günlerin %34–35'inde pozisyon açık. İşlem başına net getiri IS'te 67 bps (isabet %73), OOS'ta 104 bps (isabet %77). En iyi 5 işlem toplam getirinin %26–28'i. Yıllık getiri IS %12 (Sharpe 1,05), OOS %19 (Sharpe 1,39).
- **Yıllık (bps/maruz gün)**: 2014 29 · 2015 −2,5 · 2016 16 · 2017 6,8 · 2018 27 · 2019 11 · 2020 13 · 2021 10 · 2022 20 · 2023 29 · 2024 13 · 2025 19 · 2026 51.
  - 2026 hariç 2021–25: +18,7 (t 2,93).
  - 2014–17: +11,0 (t 2,07). 2018–20: +17,0 (t 2,42).
- **Zamanlama ve dolum** (8 bps):
  - Aynı gün kapanışta giriş (iyimser): IS t 3,65, OOS 3,43.
  - Bir gün gecikmeyle t+1 kapanışında giriş: IS 13,7 (t 2,17), OOS 25,3 (t 2,79).
  - İki gün gecikmeyle: IS t 1,54, OOS 2,59. Sinyal yavaş, sadece açılışa bağlı değil.
  - **10:30 TSİ'de giriş** (h1 dönemi, 2023-12…2026-10): 25,5 bps (t 2,90). Aynı günlerde açılış girişi 24,8 bps (t 2,87). Kayıp yok.
- **Bid-ask sıçraması**:
  - Sinyal kapanış yerine tipik fiyattan, (h+l+c)/3, üretilince: IS 14,7 (t 3,45), OOS 23,2 (t 3,42).
  - Sinyal 17:30 TSİ saatlik fiyattan üretilince: aynı gün kapanışta giriş 26,4 (t 2,30), t+1 10:30 girişi 22,8 (t 2,63).
  - Brüt kârın yalnız %25–31'i giriş gününün gün içinden geliyor, kalanı sonraki günlerde.
  - Sonuç: etki kapanış seansı gürültüsü değil.
- **VİOP vadeli fiyatlarıyla** (bülten uzlaşma fiyatları, sürekli vadeli; taşıma maliyeti fiyata dahil):
  - 2021–26, 8 bps: uzlaşma t girişi 21,5 (t 2,79), uzlaşma t+1 girişi 21,9 (t 2,65), vadelinin t+1 ilk işlemi 17,6 (t 3,10).
  - 2021–26, 15 bps: t 2,25–2,70. 30 bps: t 1,40–1,82.
  - **2017–2020: t 0,5–1,9**, 30 bps'te negatif.
  - Sinyal vadeli fiyatından üretilince 2021–26: t 2,01.
- **IS işlenebilirliği zayıf**:
  - SAHOL vadelisinin medyan günlük hacmi 2017'de 0,3, 2018'de 0,5, 2019'da 2,9 mn TL. 2021'de 68, 2026'da 1.315 mn TL.
  - Fiyatların 5–10 TL olduğu 2014–21'de tik/fiyat maliyeti iki bacak için gidiş-dönüş 17–23 bps. Bu dönemde 15 bps + tikle IS t 1,70.
  - "İki bacak VİOP'ta" ifadesi IS için değil, yalnız 2021 sonrası için geçerli.
- **Mekanizma ve ayrıştırma**:
  - Etkiyi büyük ölçüde SAHOL bacağı taşıyor. SAHOL−β·XU030 bacağı: OOS brüt 20,3 (t 3,71). AKBNK bacağı: 7,4 (t 1,56).
  - SAHOL'ün XU030 ve XU100'e göre kendi MR'ı ≈0. SAHOL/XBANK kısmen çalışıyor (OOS t 1,2–2,2). AKBNK/XBANK ≈0.
  - Diğer holding–ana iştirak çiftleri çalışmıyor: KCHOL/TUPRS, KCHOL/YKBNK, AGHOL/AEFES ≈0 ya da negatif. Etki genel bir "holding–iştirak" olgusu değil, SAHOL/AKBNK'ya özgü.
- **Alternatif tanımlar**:
  - β=1 log fiyat oranı: IS t 4,58, OOS 2,53.
  - Histerezisli çıkış (z=0'da çık): β250 ile IS 1,62 / OOS 2,78. β=1 ile 2,50 / 3,48. z=0,5'te çıkış: 2,86 / 3,13.

## KCHOL NAV ayrıntı
- **Yeniden üretim farkı**: Kaynağın kendi z serisini benim motorumda çalıştırınca IS 5,7 (t 1,65), OOS 18,9 (t 2,98) çıkıyor, yani motor uyumlu. Fark NAV inşasından geliyor. Güncel rejim temizliğiyle z korelasyonu 0,96, pozisyon uyumu %89. Bu kadar küçük bir farkla OOS t 3,0'dan 2,0'a düşüyor. **Kırılgan.**
- **NAV varyantları** (OOS t):
  - Eski ±%10,5 temizliği 2,24. AYGAZ hariç 2,21.
  - Al-tut başlangıcı 2014: 2,82; 2012: 2,76.
  - Yıllık yeniden dengeleme 1,48. Eşit ağırlık 1,76.
  - Yalnız TUPRS/FROTO/YKBNK 2,54. YKBNK ağırlığı 0,12 iken 1,99.
  - Ağırlıklar ±%30 rastgele bozulunca (30 çekiliş): OOS 1,60–2,62, IS 0,56–2,35.
- **Zamanlama**:
  - t+1 kapanışında giriş: OOS t 1,50.
  - 10:30 girişi (2023-12+): 8,45 bps (t 1,22), açılış girişiyle aynı.
  - **VİOP vadelileriyle (KCHOL ve XU030) 2021–26: t 1,02–1,46.** 2017–20: ≈0.
  - XU030 bacağı 3 bps'le maliyetlenince: OOS t 2,05 (8 bps) / 1,94 (15 bps) / 1,70 (30 bps).
- **Yıllık (bps/maruz gün)**: 2014 −7 · 2015 10 · 2016 8,5 · 2017 1,2 · 2018 −1 · 2019 4,9 · 2020 5,8 · 2021 12 · 2022 19 · 2023 −5,8 · 2024 13 · 2025 6 · 2026 16. Toplam 10/13 pozitif. Tutma süresi 11–14 gün, günlerin %45–62'sinde pozisyon açık.
- **Veri tuzağı**: AYGAZ'ın Yahoo adj serisi temettü günlerinde (2012–2019) yaklaşık 2 kat fazla düzeltilmiş. Fiyat −%7…−11 düşerken adj +%7…+16 gösteriyor. Rejim temizliğinin ±%20,5 penceresi 2020 öncesinde bunları yakalamıyor. Ağırlığı 0,03 olduğu için etkisi küçük.

## Güven
- **SAHOL/AKBNK: YÜKSEK** (istatistik ve OOS 2021–26, VİOP'ta işlenebilir). IS 2014–2020'nin VİOP'ta işlenebilirliği DÜŞÜK; spot açığa satışla mümkün olabilir ama açığa satış yasakları ve tik maliyeti var.
- **KCHOL NAV: DÜŞÜK.** Mekanizma makul ve plasebo temiz. Ancak IS anlamsız, OOS t sınırda (≈2), vadeliyle t 1,0–1,5, sonuç NAV inşasına duyarlı.

TradingView: BIST:SAHOL, BIST:AKBNK, oran grafiği için `BIST:SAHOL/BIST:AKBNK`; BIST:KCHOL, BIST:XU030. VİOP sürekli vadelileri için TV kodları doğrulanmadı (?).
