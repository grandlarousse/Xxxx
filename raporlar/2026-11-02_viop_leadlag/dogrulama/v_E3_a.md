# v_E3_a — Bağımsız doğrulama: ABD rafineri sepeti (VLO, MPC, PSX, PBF) t-1 → TUPRS gün-içi (t)

Doğrulayıcı: v_E3_a (1. aşama: bağımsız yeniden üretim ve zamanlama denetimi). Tarih: 02.11.2026.
Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_a/` (vlib.py, 01_replicate.py, 02_timing.py, 03_robust.py, 04_misc.py, 05_hedge_cost.py; çıktılar res/ altında).
ll.py ve elib.py import edilmedi. Hizalama ve temizlik ham parquet'ten yeniden yazıldı. Kullanılan kurallar: BIST'te fiyat bazlı simetrik ±%10,5 eşiği, ABD tarafında 12σ temizliği, ABD tarafında yerel tarih ≤ t olan son kapanış.

## Karar: DÜZELT. İlişki istatistiksel olarak gerçek (ORTA). Maliyet sonrası işlenebilirlik zayıf (DÜŞÜK).

| İddia | Benim sonucum | Durum |
|---|---|---|
| Hedge'li gün-içi t=4,5 (ES ve BZ lag1 kontrollü) | ALL t=4,52 (n=3199). **IS t=1,96, OOS t=3,91.** Tek değişkenli NW t: IS 3,11, OOS 4,35 | Birebir tuttu. Ama 4,5 tam dönem rakamı; IS'de kontrollü t yalnızca ≈2 |
| VLO tek başına IS t=3,8 / OOS t=4,5 | Hedef y_h (TUPRS−XU100 gün-içi), NW t: IS 3,76, OOS 4,48. Hedef ham TUPRS gün-içi olunca IS 2,44, OOS 3,16 | Tuttu. İddia hedge'li hedefe ait |
| Hareketin ~%62'si gün-içinde | Gap betası 0,035 (t 3,8), gün-içi betası 0,056 (t 4,0); oran IS, OOS ve tüm dönemde 0,62 | Tuttu, ama mekanizma yorumu düzeltilmeli (aşağıda) |
| BT \|z\|>1 brüt: IS 17,7 bps (t 2,4), OOS 25,6 bps (t 2,3) | IS 17,74 (t 2,37, n=483), OOS 25,57 (t 2,28, n=363) | Birebir |
| Net Sharpe, 8 bps: IS 0,44 / OOS 0,62. 15 bps: 0,12 / 0,37 | 0,44 / 0,62 ve 0,12 / 0,37 | Birebir. Ama net t değerleri IS 1,30 / OOS 1,56 (8 bps) ve 0,37 / 0,94 (15 bps): anlamlı değil |

## (b) Zamanlama ve ileriye bakma denetimi: TEMİZ
- ABD günlük `ldate` gerçekten ABD işlem tarihi. Günlük kapanış, aynı tarihin saatlik son bar kapanışıyla %94 eşleşiyor; bir sonraki günle eşleşme %3. FX'teki türden bir kayma yok.
- VLO kapanışı 20:00 UTC (yaz) / 21:00 UTC (kış). ES=F günlük kapanışı ağırlıkla 20:00–21:00 UTC; BZ=F daha erken. Hepsi BIST açılış müzayedesinden (06:55–07:00 UTC; 2016 öncesi kışın 07:55) en az ~10 saat önce.
- Sinyal penceresinin bitişi ≥ BIST günü t olan gün sayısı: **0 / 6.686**. İleriye bakma yok.
- BIST tatilinden sonraki 80 günde sinyal, açılışta bilinen son ABD kapanışını kaçırıyor (bayat sinyal, ileriye bakma değil). "Taze" sinyal tanımı (sigB) sonucu biraz zayıflatıyor: Z1 brüt IS 15,2 / OOS 22,2 bps.
- Asya kuralı bu iddiada geçerli değil, çünkü sinyal ABD kaynaklı.
- Yahoo BIST açılışı: 2023-11 sonrasında günlük `o` = saatlik ilk bar açılışı (%99,9) ve 5 dk 06:55 müzayede barı (60/60 gün). Yani `o` açılış müzayedesi fiyatı. 2014–2023 için doğrudan doğrulama yapılamadı. `o` == önceki kapanış olan günlerin oranı yıllara göre %3–18; bu günlerde getiri farklı değil (27 bps, diğer günlerde 21 bps).

## (c) Alternatif giriş: kazancın yaklaşık yarısı ilk 30 dakikada
Ortak örneklem 2023-11-30 → 2026-10-30, 722 gün, Z1 ile 205 işlem. z-skoru 2014'ten beri hesaplanan sinyalden alındı. Çıkış günlük kapanışta.

| Giriş | Brüt bps/işlem | t | Net 8 bps | Net 15 bps |
|---|---|---|---|---|
| E0: açılış müzayedesi | 26,9 | 1,94 | 18,9 | 11,9 |
| E1: saatlik ilk bar kapanışı (10:30 TSİ) | **15,3** | 1,37 | 7,3 | **0,3** |
| E2: 11:30 TSİ | 13,1 | 1,21 | 5,1 | −1,9 |
| XU030 hedge'li E0 / E1 / E2 (2 bacak, 8 / 15 bps × 2) | 40,7 / 22,6 / 20,1 | 3,48 / 2,31 / 2,17 | 24,7 / 6,6 / 4,1 | 10,7 / −7,4 / −9,9 |

- Açılıştan 10:30'a kadarki ilk dilim tek başına 11,6 bps. Getirinin ~%43'ü açılışın hemen ardından geliyor. Geç girişte 15 bps maliyetle kazanç sıfıra iniyor.
- VİOP F_TUPRS bülteni, en yüksek hacimli vade (417 gün): vadeli açılış→kapanış ile spot açılış→kapanış korelasyonu 0,92; spot 10:30→kapanış ile korelasyon 0,785. Vadeli açılış fiyatı = açılış seansı fiyatı (fark medyanı 0). Yani vadelide açılış seansıyla spot açılışına yakın bir anda girmek mümkün. Bu 97 işlemde vadeli açılış→kapanış 35,6 bps, spot 33,5 bps (t ~1,2).
- Likidite: F_TUPRS ön vadesinde medyan günlük işlem değeri ~957 mn TL, ~13 bin işlem. En likit pay vadelilerinden biri, bu yüzden 8 bps makul. Ama açılış seansı hacmi küçük (ör. 30.10.2026'da 6 işlem, 213 bin TL). Büyük emirde açılış dolumu iyimser bir varsayım.

## Mekanizma düzeltmesi ("gece eksik tepki" değil, yavaş yayılma)
VLO saatlik verisiyle sinyali ikiye böldüm (2024-03 → 2026-10, n=465):
- (i) ABD kapanışı t-2 → 15:00 UTC t-1: BIST seansı t-1 sırasında zaten biliniyor.
- (ii) 15:00 UTC t-1 → ABD kapanışı t-1: BIST kapanışından sonra gelen kısım.

Sonuçlar:
- Gap: (ii) b=0,157, t 3,72; (i) t 0,75. BIST kapanışı sonrası bilgi açılışta fiyatlanıyor.
- Gün-içi: (i) b=0,072, t 1,66; (ii) b=0,029, t 0,45.

Yani gün-içi öngörü, ABD rafinerilerinin BIST seansı t-1 sırasında ve öncesinde yaptığı hareketten geliyor. TUPRS bu bilgiye yaklaşık bir gün geç tepki veriyor (sektör bilgisinin yavaş yayılması). "ABD gece hareketine açılışta eksik tepki" yorumu desteklenmiyor. Örneklem küçük, t ~1,7; bu ayrıştırma bir gösterge, kanıt değil. TUPRS cc_{t-1}, XU100 cc_{t-1}, gap_t ve XU100 gap_t kontrol edildiğinde US_REF t değerleri: ALL 4,43, IS 1,93, OOS 3,91.

## (d) Stabilite
- Yıllık corr(US_t-1, y_h): 13 yılın 11'inde pozitif (%85); negatif yıllar 2016 (−0,002) ve 2017 (−0,07). 250 günlük kayan korelasyon günlerin %81'inde > 0.
- Z1 brüt bps yıllara göre: 2014 30, 2015 7, 2016 6, **2017 −34**, 2018 32, 2019 19, 2020 41, **2021 −8**, 2022 26, 2023 55, 2024 29, 2025 30, 2026 19.
- 8 bps net 13 yılın 9'unda pozitif; 15 bps netinde de 9/13. Ama 15 bps netinde pozitif yıllar küçük.
- Alt dönemler: 2014–16 12 bps (t 1,55), 2017–20 22 (1,91), 2021–23 25 (1,36), 2024–26 26 (1,88). Hiçbir alt dönem tek başına t>2 değil.
- Dairesel kaydırma null testi (2000 tekrar): ALL p<0,001, IS p=0,008, OOS p=0,012. Şans eseri olması zor.
- Gecikme profili: etki yalnızca k=1'de (y_h t 5,3). k=2 t 0,9; k=3..6 t 1,2–2,7 (küçük, dağınık). Lag2'nin ek katkısı yok.
- Kesitsel plasebo: aynı sinyal 48 VİOP hissesinin hedge'li gün-içi getirisinde denendi. **TUPRS 1. sırada (t 5,3); 2. sırada AYGAZ (t 3,7)**, ki Koç grubu üzerinden Tüpraş'a dolaylı ortak. |t|>2 olan 6 hisse var, şansla beklenen ~2,4. Sinyal TUPRS'a özgü, genel bir piyasa etkisi değil.
- Sektör özgüllüğü: OOS'ta rafineriler (VLO, PBF, PSX, MPC, CRAK; Z1 OOS 17–34 bps) entegre devlerden (XLE 3, XOM −3, CVX 8 bps) belirgin şekilde iyi. IS'de fark yok. "US_REF − XLE" spread'i: IS t 1,87, OOS t 3,58.

## Kırılganlık (karşı kanıt)
- Eşiğe duyarlı. Filtresiz işaret stratejisinde 8 bps net IS Sharpe −0,21 (OOS 0,90). Eşik |z|>0,5'te 8 bps net IS Sharpe dört z penceresinin hepsinde negatif (−0,21 ile −0,43 arası). 12 pencere×eşik kombinasyonunda 8 bps net Sharpe > 0 oranı IS'de %67, OOS'ta %100.
- En iyi 10 işlem çıkarılınca IS 10,4 bps (t 1,50). 2020 çıkarılınca IS t 1,63.
- Blok bootstrap %95 güven aralığı alt sınırları: IS 3,3 bps, OOS 6,1 bps. İkisi de 8 bps maliyetin altında, yani net kârlılık istatistiksel olarak kanıtlanmış değil. ALL [8,8, 33,2].
- XU030 vadelisiyle hedge (pay vadelisi 8 bps + endeks vadelisi 3 bps): IS Sharpe 0,40 (t 0,99), OOS 1,07 (t 2,90). 15+3 bps'de 0,04 / 0,79. Hedge OOS'ta yardımcı oluyor, IS'de olmuyor.
- Seçim yanlılığı: sinyal, 1.085 sembollük taramanın en iyisinden (VLO) türetildi. Sepet sektörel olarak önceden tanımlı. VLO dışarıda bırakılınca IS t 2,83, OOS 4,22; MPC ve PSX tek başına da anlamlı. Bu yüzden risk sınırlı.

## Düzeltilmiş iddia
ABD rafineri sepetinin t-1 getirisi TUPRS'un t günündeki gün-içi getirisini öngörüyor. Bu ilişki TUPRS'a özgü (48 hisse içinde 1.), k=1'e özgü ve istatistiksel olarak gerçek: hedge'li NW t tam dönem 5,3, IS 3,1, OOS 4,35; ES ve BZ kontrollü t ALL 4,5, IS 2,0, OOS 3,9. Yılların %85'inde işaret pozitif.

İşlenebilirlik zayıf:
- |z|>1 tek bacak brüt IS 17,7 / OOS 25,6 bps. 8 bps net t IS 1,3 / OOS 1,6; 15 bps net Sharpe 0,12 / 0,37. Bootstrap alt sınırları maliyetin altında.
- Getirinin ~%43'ü açılışın ilk 30 dakikasında geliyor. 10:30 girişinde (2023-11+) brüt 15 bps; 15 bps maliyetle sıfır.
- İşlemek için girişin VİOP F_TUPRS açılış seansında ya da hemen sonrasında yapılması gerekiyor.

Mekanizma: gece hareketine eksik tepki değil, BIST seansı t-1 sırasındaki ABD rafineri hareketine gecikmeli tepki (yavaş yayılma).

Güven: ilişki için ORTA; maliyet sonrası strateji için DÜŞÜK.

## TradingView
NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF (alternatif AMEX:CRAK), hedef BIST:TUPRS. VİOP vadelileri: TUPRS pay vadelisi ve hedge için XU030 vadelisi; TradingView sembolleri doğrulanmadı ('?').
