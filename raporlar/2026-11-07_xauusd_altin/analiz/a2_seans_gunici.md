# a2_seans_gunici: gün içi seans yapısı ve VİOP mikro yapısı (F_XAUUSD)

**Soru.** Gün t uzlaşmasında (≈15:10 UTC) girip t+h uzlaşmasında (h = 1, 3, 5 iş günü) çıkan bir VİOP ons altın işlemi için gün içi seans getirileri, VİOP–spot bazı, LBMA PM fiksingi, hafta sonu boşluğu ve VİOP hacim/açık pozisyon verisi işe yarar bir öncü (lead-lag) sinyal veriyor mu?

**Kısa cevap.** Hayır. Kapanıştan kapanışa VİOP getirisini çoklu test düzeltmesinden sağ çıkacak biçimde öngören bir seans ya da mikro yapı sinyali **bulunamadı**. 192 testin hiçbiri bunu sağlamadı. İki sağlam bulgu var ama ikisi de 1-3-5 günlük kapanıştan kapanışa işlemde para kazandırmıyor:

1. **Takvim düzenliliği (lead-lag değil).** Spot altın UTC 20:00 ile 00:00 arasında (VİOP kapalıyken; Asya açılışı ve CME günlük yeniden açılışı) ortalama +2,9 bps/gün getiriyor. t = 6,6, 17 yılın 15'inde pozitif ve her alt dönemde anlamlı. Bu saatlerde VİOP kapalı. Akşam seansı kapanışında (23:00 TSİ) alıp sabah açılışında (09:30 TSİ) satan bir kural brüt Sharpe 1,5 veriyor, ama 5 bps maliyetle 0,25'e, 10 bps'te −1'e düşüyor.
2. **VİOP–spot baz ortalamaya dönüşü.** Dünkü aşırı baz, sonraki 3-5 günde VİOP'un spota göre göreli getirisini ters yönde öngörüyor (t ≈ −4,3 ile −5,0, OOS t −2,5 ile −3,4). Ama bu göreli bir ilişki (VİOP eksi spot). Brüt kazanç günde ~0,6–0,8 bps; iki bacağın maliyetinden sonra sıfır ya da negatif. Çıplak VİOP yönünü öngörmüyor.

Ölçütleri ancak kâğıt üzerinde ORTA sınırına yaklaşan tek yön sinyali (kış aylarında 14:00→15:00 UTC saatinin getirisi → ertesi gün VİOP) erken dönem (2010–2016) tekrarında tutmadı. Bu yüzden DÜŞÜK etiketli.

---

## 1. Veri, zaman kuralları, segmentler

- Hedef `fwd{h}`: VİOP aktif kontrat uzlaşma getirilerinin t+1..t+h toplamı (panel_viop, 2017-03-06 → 2026-11-06, 2.427 gün). Erken dönem tekrarı için spot panel (`sfwd{h}`, 15:00→15:00 UTC, 2010–2016).
- Saatlik spot: Dukascopy BID, **fiyat anı = bar başlangıcı + 1 saat**. Ekim–Kasım 2026 dakikalık yaması panel kurucuyla aynı yöntemle eklendi (`a2_common.hourly_bars`). Panel anlık görüntüleriyle birebir tuttuğu doğrulandı.
- **Segmentler** (gün t satırı; t−1 = endeksteki önceki gün; hepsi gün t 15:00 UTC'de ya da önce kapanır):

| Segment | Pencere (UTC) | Anlamı | Bilgi zamanı |
|---|---|---|---|
| S1_eve | t−1 15:00 → t−1 20:00 | VİOP akşam seansı / NY öğleden sonra | t−1 20:00 |
| S2_late | t−1 20:00 → t 00:00 | NY kapanışı, CME bakım arası, Asya açılışı | t 00:00 |
| S3_asia | 00:00 → 07:00 | Asya (Şanghay gündüz seansı) | t 07:00 |
| S4_lon | 07:00 → 12:00 | Londra | t 12:00 |
| S5_nyam | 12:00 → 15:00 | NY sabahı, ABD veri saatleri (12:30/13:30) | t 15:00 |
| C_full = S1+…+S5 | t−1 15:00 → t 15:00 | spot gün getirisi | t 15:00 |

  Kombinasyonlar: C_post = S1+S2, C_night = S2+S3, C_on = S1+S2+S3, C_day = S4+S5, C_pre = S3+S4+S5, D_asia_ny = S3−S5. Ayrıca 5 ve 20 günlük toplamlar.
- `v_*` sütunları (uzlaşma, hacim, OI) gün t 15:10 UTC'de ya da seans sonunda bilinir. Sinyalde yalnız t−1 sürümleri kullanıldı. Tek istisna baz testindeki eb_t; bu **"kapanışta hesaplanan"** diye işaretli ve t−1 sürümü de verildi.
- Yöntem (`lib_altin`): Spearman IC + Newey-West t (lag = max(h,5)). IS 2017-03..2021-12, OOS 2022-01..2026-11. Yıl yıl işaret tutarlılığı. Parametre ve eşikler (tercil, q90) yalnız IS'te seçildi. Backtest kademeli (örtüşen h alt portföy). Maliyet 5 bps gidiş-dönüş, stres 10 bps. Göreli değer işlemlerinde iki bacak için 10/20 bps. Her stratejide buy&hold, demeaned Sharpe ve uzun/kısa bacak ayrımı var.
- **Test sayısı: 192** (`out/registry/a2_seans_gunici.csv`; q değerleriyle `registry_with_q.csv`). Bonferroni %5 eşiği |t| ≥ 3,65.

## 2. (a) Segment getirileri 1/3/5 günlük VİOP getirisini öngörüyor mu?

Test kapsamı:
- 12 segment ve kombinasyon × 3 ufuk.
- 4 adet 5 günlük toplam × 3 ufuk.
- 2 adet 20 günlük toplam ("tug of war") × 3 ufuk.
- Büyük NY-sabahı hareketleri (|S5| > IS q90) × 3 ufuk.
- Bunların hepsinin spot panelde 2010–2016 tekrarı.

Sonuç:
- **57 VİOP testinin hiçbiri |t| ≥ 3 değil.** En yüksekleri:
  - C_pre (00→15 UTC) → fwd3: IC 0,048, t 2,37 (IS 1,10, OOS 2,11). Erken dönem IC −0,001.
  - S4_lon 5 günlük toplam → fwd3/fwd5: OOS t 2,9 ama IS işareti ters (IS −1,3).
  - |S5| büyük hareket → fwd5: IC 0,12, t 2,14, OOS 2,33, IS 0,33. Erken dönem IC −0,03. İşaret kuralı (h = 5, yılda ~31 sinyal): IS Sharpe 0,00, OOS 0,77 (demeaned 0,78). IS'te sıfır, erken dönemde ters → DÜŞÜK.
- **IS'te seçilen kural OOS'ta tersine döndü.** IS'te en yüksek |t| S1_eve → fwd3'te (IS t +2,49). OOS t −2,12 çıktı. İşaret kuralı IS Sharpe 0,60 → OOS −0,71 (demeaned −0,72). Seans getirilerindeki IS ilişkilerinin örneklem gürültüsü olduğunu gösteren tipik bir örnek.
- C_pre işaret kuralı (h = 3): tam dönem Sharpe 0,33, OOS 0,30. Demeaned değerler sırasıyla 0,26 ve 0,22. Uzun bacak demeaned 0,12, yani getirinin çoğu altının yükseliş eğiliminden geliyor. Erken dönemde yok. Etiket: DÜŞÜK.
- Spot hedefle (2017+) ve VİOP hedefle IC'ler hemen hemen aynı. Sorun hedefte değil, sinyal yok.

Tablo: Ek A.

## 3. (b) "Gece/Asya pozitif, NY negatif" anomalisi (2010–2026)

Segment ortalama getirileri (bps/gün, spot; tam tablo Ek B1–B2):

| Segment | 2010–16 | IS 2017–21 | OOS 2022–26 | Tam (t) | Pozitif yıl |
|---|---|---|---|---|---|
| S1 15→20 | 1,15 | 0,29 | −0,97 | 0,37 (0,50) | 10/17 |
| **S2 20→00** | **2,15 (t 3,4)** | **2,46 (t 3,6)** | **4,64 (t 4,6)** | **2,93 (6,59)** | **15/17** |
| S3 Asya 00→07 | 3,64 (t 3,6) | 0,06 | 1,61 | 2,04 (2,99) | 12/17 |
| S4 Londra 07→12 | −4,23 (t −4,4) | 0,43 | 1,33 | −1,21 (−1,92) | 9/17 |
| S5 NY 12→15 | −2,08 | 0,28 | −0,22 | −0,84 (−1,01) | 6/17 |

**Drift'ten arındırılmış fazla.** Fazla = segment − (segmentin yıllık varyans payı × günlük ortalama). S2 için +2,67 bps (t 6,0), S4 için −1,81 (t −2,9), S5 için −1,92 (t −2,3).

**Yorum.**
- Literatürdeki "Asya'da yükselir, Londra/NY'de düşer" deseni 2010–2016'da açıkça var: Asya +3,6 bps, Londra −4,2 bps, ikisi de t > 3,5. **2017'den sonra Asya ve Londra etkisi kayboldu** (IS'te ikisi de ≈ 0).
- Kalıcı olan tek parça **S2: t−1 20:00 → t 00:00 UTC.** Saat saat bakınca (Pazartesi–Perşembe akşamlarından ertesi güne uzanan geceler): 20→22 −2,2 bps (t −7,5), 22→00 +4,4 bps (t 12,2), net +2,1 bps (t 4,3). Yani gün sonu bakım arası (CME 17:00–18:00 ET) öncesinde düşüş, Asya/Globex yeniden açılışında yükseliş var.
- **Kote (BID) yanılsaması kontrolü.** Dukascopy BID kotası, makas bakım arasında açılıp sonra kapanınca yapay bir düşüş-yükseliş yaratabilir. Bu yüzden 2024-06..2026-11 arasında COMEX GC=F saatlik işlem fiyatlarıyla karşılaştırdım. GC'de S2 +4,9 bps, Dukascopy'de +6,0 bps, korelasyon 0,987. Etkinin büyük kısmı gerçek. ~1 bps kadarı kote yapısı olabilir.
- S2'nin sağlamlığı:

| Kontrol | S2 ortalaması | t |
|---|---|---|
| Pazartesi hariç | 2,16 bps | 4,5 |
| Uç dönemler hariç (Mart 2020, Ocak–Şubat 2026) | 2,52 bps | 6,3 |
| Winsor %1–99 | 2,82 bps | 7,6 |
| ABD yaz saati | 2,28 bps | – |
| ABD kış saati | 4,21 bps | – |

  Medyan 1,14 bps, günlerin %53,5'i pozitif.
- **VİOP-yerel kontrol.** VİOP işlem fiyatlarıyla gece (uzlaşma t−1 → normal seans açılışı t ≈ 06:30 UTC) ortalaması 1,11 bps (t 0,92), gündüz (açılış → uzlaşma) 1,97 bps (t 1,26). Fark yok. Bunun iki nedeni olabilir: VİOP'un gece penceresi S1'i de içeriyor, ve açılış fiyatı tek işlemlik, gürültülü bir fiyat. Ayrıca VİOP fiyatı vade sonuna doğru spota yaklaştıkça günde ~1,5–1,9 bps aşınıyor (taşıma maliyetinin erimesi).

**Alternatif giriş/çıkış saatleri.** Bunlar VİOP akşam seansıyla (18.09.2020+) uygulanabilir ama **kapanıştan kapanışa değil.** Değerler Sharpe; spot vekil fiyatla hesaplandı (Ek B4–B5):

| Kural | Brüt 2020-09+ | 5 bps | 10 bps | OOS 5 bps |
|---|---|---|---|---|
| 23:00 TSİ akşam kapanışında al → ertesi 09:30 TSİ açılışta sat (S2+S3) | 1,48 | 0,25 | −0,97 | 0,28 |
| 23:00 TSİ al → ertesi uzlaşmada sat (S2..S5) | 0,91 | 0,11 | −0,70 | 0,37 |
| Uzlaşmada al → 23:00 TSİ akşam kapanışında sat (S1) | −0,25 | −1,86 | −3,47 | −1,82 |
| Sabah açılışta al → uzlaşmada sat (S4+S5) | −0,08 | −1,12 | −2,16 | −0,80 |
| Gece uzun + gündüz kısa | 1,01 | −0,56 | −2,13 | −0,72 |
| Buy&hold 15:00→15:00 (maliyetsiz) | 0,70 | – | – | 0,88 |

Notlar:
- Gece-uzun kuralının drift'ten arındırılmış hali (segment − yıllık varyans payı × günlük ortalama): OOS brüt Sharpe 1,08, 5 bps sonrası −0,05.
- Gece-uzun kuralı her gün bir gidiş-dönüş demek (yılda ~252). 5 bps maliyet yılda ~%12,6 ediyor ve brüt getirinin neredeyse tamamını siliyor.
- **Akşam seansı kalibrasyonu** (2026 akşam bültenleri, n = 58 gün): VİOP akşam kapanışı, (spot 20:00 + o günün bazı)'ndan medyan 5,2 bps pahalı, MAD 7,8 bps. Akşam hacmi günlük hacmin medyan %7,7'si. Piyasa yapıcı makas sınırı normal seansın 2 katı.
- Bu yüzden gerçekçi maliyet 10 bps'e yakın. Bu düzeyde hiçbir saat kuralı kâr etmiyor.
- **Pratik çıkarım:** Zaten uzun pozisyon taşıyacak biri için en iyi pencere gece. Kapanıştan kapanışa tutan zaten bunu taşıyor. Kısa pozisyon taşıyan, 20:00–00:00 UTC'nin pozitif eğilimine karşı oynuyor.

## 4. (c) VİOP'a özgü fiyatlama hatası: excess_basis

Tanım: eb_t = log(v_settle_t / xau_p15_t) − r·dte/365, r = ust_nom3m/100 (t−1 değeri).

**Dakikalık kalibrasyon** (210 örnek gün; dakika endeksi bar başlangıcı, 14:59 barı saatlik 15:00 fiyatıyla birebir tutuyor):

| Karşılaştırma | Medyan (taşıma sonrası) | MAD | std |
|---|---|---|---|
| Uzlaşma vs spot 15:00 | +7,8 bps | 8,5 bps | 27,2 bps |
| Uzlaşma vs spot VWAP 15:05–15:15 | +8,7 bps | **6,6 bps** | 27,1 bps |
| Uzlaşma vs spot 15:10 | – | 6,9 bps | – |
| Uzlaşma vs spot 15:20 | – | 9,1 bps | – |

- Uzlaşma en iyi 15:05–15:15 VWAP ile örtüşüyor.
- Spot 15:00 ile 15:05–15:15 VWAP'ı arasındaki zaman farkı gürültüsü: std 15,4 bps, MAD 7,1 bps. Kış/yaz farkı küçük: 15:00→15:10 std yazın 13,1, kışın 18,8 bps.
- eb(p15) ile eb(VWAP) korelasyonu 0,84. eb'nin günlük varyansının kabaca %15–30'u zaman gürültüsü, kalanı kalıcı.

**Tanımlayıcı.**
- eb ortalaması 15,9 bps, medyan 11 bps, AC1 0,62.
- eb vadeye kalan gün sayısıyla artıyor: IS eğimi 0,21 bps/gün. VİOP USD altın, T-bill faizinin ~%0,8/yıl üstünde bir taşıma maliyetiyle fiyatlanıyor.
- 2026'da std 59 bps; uç değerler Ocak–Şubat 2026'da.

**Testler** (Ek C):

| Öngörücü → hedef | h = 1 | h = 3 | h = 5 | Not |
|---|---|---|---|---|
| eb_t (kapanışta hesaplanan) → VİOP fwd | t 0,82 | 1,33 | 1,29 | yok |
| eb_{t−1} → VİOP fwd | t 1,76 | 1,87 | 1,66 | pozitif ve zayıf; winsor Pearson t 0,08 / 0,18 → yok |
| **eb_{t−1} → VİOP − spot (göreli)** | **t −2,36** | **−4,33** (OOS −2,91) | **−4,05** (OOS −2,47) | baz ortalamaya dönüyor |
| **eb_{t−1} dte'den arındırılmış → göreli** | t −2,40 | **−4,84** (OOS −3,41, 8/10 yıl) | **−4,97** (OOS −3,08, 9/10 yıl) | IS t −1,9 |
| eb_t → göreli | t −25 | | | **MEKANİK**: eb_t'deki 15:00/15:10 gürültüsü hedefte −eb_t olarak geri geliyor. Kanıt sayılmaz. |

- Göreli ilişki sağlamlık kontrollerinde (roll penceresi hariç, uç dönemler hariç, dte > 5, winsor) t −3,6 ile −4,9 arasında kalıyor.
- Ortalamaya dönüş katsayısı: h = 1'de −0,10, h = 5'te −0,23. Dünkü baz sapmasının ~%23'ü 5 günde kapanıyor.
- **Ekonomik değer yok.** Göreli değer kuralı: eb_{t−1} > IS üst tercil ise VİOP kısa / spot uzun, alt tercil ise tersi.
  - Brüt kazanç 0,6–0,8 bps/gün.
  - Gidiş-dönüş maliyeti iki bacak için 10 bps olduğunda h = 5 tam dönem Sharpe −0,10, OOS +0,39. Ama OOS demeaned −0,32: OOS'taki pozitif değer, göreli getirinin taşıma kaynaklı −1,85 bps/gün eğiliminden geliyor.
  - 20 bps'te OOS −0,23.
- Çıplak VİOP kuralı ("pahalıyken kısa"): her ufukta negatif Sharpe (−0,4 ile −0,9). Ters yöndeki kural ("pahalıyken uzun"): OOS Sharpe 0,19–0,27, demeaned ≈ 0.

## 5. (d) LBMA PM fiksingi (15:00 Londra = kışın 15:00, yazın 14:00 UTC)

Fiks fiyatı yerine spotun o saatteki fiyatı kullanıldı. IBA/LBMA verisi Cloudflare engeline takıldı (`dl4/gold_pm.json` bir hata sayfası).

- **Fiks öncesi saat** ortalama −1,39 bps (t −2,72, 17 yılın 14'ünde negatif). Ama etki 2010–2016'da yoğun (−2,5, t −3,1). IS −0,8 (t −1,0), OOS −0,4 (t −0,4). **Zayıflamış**; eski telefonlu fiksinge özgü baskı Mart 2015 sonrası elektronik müzayedeyle büyük ölçüde gitmiş görünüyor.
- Fiks sonrası saat +0,59 (t 1,15). Gün içi fiks dönüşü (fiks öncesi saat → fiks sonrası saat): IC −0,018, t −1,18 → yok.
- Fiks öncesi saat → VİOP fwd1/3/5: t 1,81 / 1,21 / 1,72 → yok. Yaz aylarında fiks (14:00) → 15:00 → fwd: IS t 2,42, OOS −0,62 → yok.
- **Kış alt örneklemi** (fiks öncesi saat = 14:00→15:00 UTC, uzlaşmadan hemen önce) → fwd1:
  - IC 0,090, t 2,76 (IS 1,63, OOS 2,08, 7/10 yıl). Winsor Pearson t 4,28. Roll penceresi hariç t 2,81, uç dönemler hariç t 1,95.
  - İşaret kuralı OOS Sharpe 1,02 (demeaned 1,00, 10 bps'te 0,83). Uzun bacak OOS 1,24, kısa bacak 0,19.
  - Ama: IS Sharpe yalnız 0,13. **Erken dönem (2010–2016) tekrarı IC 0,036, t 0,97, 4/7 yıl.** Yaz ayları (aynı UTC saati, fiks sonrası) IC 0,005. Ayrıca bu, anlamsız çıkan genel bir testin alt kırılımı.
  - Etiket: **DÜŞÜK.** 192 test içinde Bonferroni ve BH-FDR'dan geçmiyor (q = 0,08).
- Vade sonu uzlaşması (= LBMA PM) aktif seride çok seyrek: dte ≤ 0 olan 9 gün var, çünkü aktif kontrat OI'ye göre vade sonundan 3–4 gün önce değişiyor.

## 6. (e) Hafta sonu boşluğu ve Pazartesi

- Boşluk = Cuma son spot barının kapanışı (~21:00 UTC) → Pazar ilk barın açılışı (~22:00/23:00 UTC). 960 hafta sonu. Ortalama +1,33 bps (t 1,34), std 25,7 bps.
- Boşluk → Pazartesi uzlaşmasından fwd1/3/5: t 0,75 / −0,86 / −0,56. Cuma 15:00 → Pazartesi 00:00 → fwd: t 0,53 / 0,11 / −0,27. **Yok.**
- Erken dönemde boşluk → sfwd1 için IC −0,12, t −2,45 çıktı, ama VİOP döneminde işaret +. Tutarsız.
- Gün içi: boşluk → Pazartesi 07→15 (VİOP sabah açılışından uzlaşmaya): IC 0,039, t 1,05. Cuma öğleden sonrası → boşluk: t −1,06. Yok.
- **Haftanın günü** (VİOP v_ret, gün etkisi = o günün ortalaması − genel ortalama): Pazartesi −6,6 bps (t −1,51), Çarşamba +5,4 (t 1,26). Diğerleri ≈ 0. 2010–2016 spot döneminde Pazartesi tersine +10,3 bps (t 1,86). **Kararlı bir gün etkisi yok.**
- "Cuma uzlaşmada al → Pazartesi uzlaşmada sat": Sharpe −0,42 (demeaned −0,62).

## 7. (f) VİOP mikro yapısı (t−1 bülteni)

Hacim şoku (20 günlük log z), getiri × hacim şoku, toplam OI değişimi (roll'dan etkilenmez) ve getiri yönü × OI değişimi → fwd1/3/5. **12 testin hepsi |t| < 1,3.** Yok.

## 8. Sağlamlık özeti (zorunlu kontroller)

- **Roll günleri** (t+1..t+h içinde v_code değişimi): baz göreli testi değişmiyor (t −4,8 / −4,9). Kış 14→15 testi t 2,81. Seans IC'leri zaten sıfıra yakın.
- **Sıfır hacim:** aktif kontratta sıfır hacimli gün yok. v_ret = 0 olan 7 gün var. Etkisi ihmal edilebilir.
- **Uç dönemler** (Mart 2020, Ocak–Şubat 2026): S2 2,52 bps (t 6,3), baz göreli t −3,8 / −3,9, kış 14→15 t 1,95 (zayıflıyor).
- **İleriye bakma:**
  - Bütün segment öngörücüleri t 15:00 UTC'de ya da önce kapanıyor.
  - placebo_lead (kış 14→15): shift −1'de IC 0,27. Bu beklenen bir sonuç, çünkü t+1'in 14→15 saati fwd1'in içinde. shift 0'da 0,09, shift +1'de −0,01, yani tutarlı.
  - eb için shift −1'de IC 0,06 (gelecek uzlaşma hedefte). shift 0 / +1'de 0,018 / 0,040.
- **Çoklu test:** 192 test.
  - BH-FDR q < 0,05'i geçenler: S2 ortalaması ve fazlası; baz göreli testleri (h = 3, 5); S3 Asya ortalaması (q 0,045, yalnız 2010–2016 kaynaklı); eb_t mekanik testleri; maliyet yüzünden negatif çıkan iki saat kuralı.
  - **Kapanıştan kapanışa çıplak VİOP yön öngörüsünün hiçbiri FDR'ı geçmiyor.**

## 9. Kullanıcı için pratik sonuçlar

1. 1-3-5 günlük kapanıştan kapanışa VİOP ons altın işleminde, gün içi seans getirilerinden (Asya, Londra, NY sabahı, akşam seansı), fiks saatinden, hafta sonu boşluğundan ya da VİOP hacim/OI'sinden **güvenilir bir yön sinyali çıkmıyor.** Bu ailede "işe yarayan lead-lag" bulunamadı.
2. Altının gece 23:00–03:00 TSİ (20:00–00:00 UTC) yükselme eğilimi gerçek ve kalıcı. Ama VİOP o saatlerde kapalı. Akşam seansıyla yakalamaya çalışmak (23:00'te al, 09:30'da sat) maliyet ve akşam makası yüzünden kâr bırakmıyor.
3. VİOP fiyatı spota göre ~11 bps (medyan) pahalı. Bu fark gün içinde açılıp birkaç günde kısmen kapanıyor. Bilgi olarak faydalı: gün sonunda VİOP spota göre çok pahalıysa yeni bir **uzun** pozisyonu VİOP'ta değil, başka bir araçta açmak ya da ertelemek giriş maliyetini birkaç bps azaltabilir. Ama kendi başına işlem stratejisi değil.
4. "Altın Asya'da çıkar, Londra/NY'de iner" eski literatür deseni 2017 sonrasında yok. Buna göre gün içi pozisyon açmak, verilere göre maliyetten başka bir şey kazandırmıyor.

## 10. Negatif bulgular (test edildi, tutmadı)

- Her segment ve kombinasyon → fwd1/3/5 (36 test). Hepsi |t| < 2,4. IS'te seçilen kural (S1_eve, h = 3) OOS'ta tersine döndü.
- 5 günlük ve 20 günlük segment toplamları (gece/gündüz "tug of war"): yok. Londra 5 günlük toplamının OOS'taki gücü IS ile ters işaretli.
- Büyük NY-sabahı (ABD veri saati) hareketlerinin devamı: OOS t 2,3, ama IS 0,3 ve erken dönem negatif.
- Asya pozitif / Londra negatif segment ortalamaları: yalnız 2010–2016'da var.
- Gece-uzun / gündüz-kısa ve diğer saat kuralları: maliyet sonrası negatif.
- Fiks öncesi saat → fwd: yok. Kış alt örneklemi DÜŞÜK.
- Fiks öncesi/sonrası gün içi dönüş: yok.
- eb (kapanışta ya da t−1) → çıplak VİOP fwd: yok (winsor sonrası t ≈ 0).
- Hafta sonu boşluğu → fwd1/3/5 ve → Pazartesi gün içi: yok. Haftanın günü etkisi yok. Cuma al / Pazartesi sat: negatif.
- VİOP hacim şoku, OI değişimi ve etkileşimleri: yok.
- VİOP-yerel gece/gündüz ayrışması (uzlaşma → açılış → uzlaşma): fark yok.

## 11. Dosyalar

Kod (tek başına çalışır; `run_all.sh` hepsini sırayla çalıştırır):
- `a2_common.py`
- `a_segments.py`
- `b_segmeans.py`
- `c_basis.py`
- `d_fix.py`
- `e_weekend.py`
- `f_micro.py`
- `g_robust.py`
- `h_tables.py`

Çıktılar: `*.csv`, `log_*.txt`, `tables.md`, `registry_with_q.csv`. Kayıt: `out/registry/a2_seans_gunici.csv` (192 satır).

---

# Ekler (CSV çıktılarından otomatik üretilmiş tablolar)

### A: segment IC tablosu
| predictor | h | n | ic | t | t_is | t_oos | yrs | ic_1016 | t_1016 | yrs_1016 |
|---|---|---|---|---|---|---|---|---|---|---|
| S1_eve | 1 | 2379 | -0.0111 | -0.54 | 1.76 | -2.15 | 5/10 | 0.0071 | 0.3 | 4/7 |
| S2_late | 1 | 2359 | 0.0237 | 1.15 | 0.25 | 1.29 | 7/10 | -0.0633 | -2.61 | 6/7 |
| S3_asia | 1 | 2406 | -0.001 | -0.05 | -0.24 | 0.19 | 6/10 | 0.0151 | 0.63 | 3/7 |
| S4_lon | 1 | 2406 | 0.0168 | 0.82 | 0.98 | 0.31 | 5/10 | 0.0155 | 0.63 | 5/7 |
| S5_nyam | 1 | 2406 | 0.0256 | 1.22 | 1.68 | 0.22 | 7/10 | -0.0228 | -1.01 | 5/7 |
| C_full | 1 | 2386 | 0.0267 | 1.33 | 1.85 | 0.13 | 6/10 | -0.0145 | -0.67 | 5/7 |
| C_post | 1 | 2359 | -0.0076 | -0.35 | 1.3 | -1.36 | 5/10 | -0.028 | -1.18 | 5/7 |
| C_night | 1 | 2359 | 0.0248 | 1.21 | 0.43 | 1.18 | 5/10 | -0.0279 | -1.24 | 6/7 |
| C_on | 1 | 2359 | 0.0095 | 0.47 | 1.49 | -0.53 | 6/10 | -0.0104 | -0.47 | 4/7 |
| C_day | 1 | 2406 | 0.0286 | 1.35 | 1.57 | 0.5 | 8/10 | -0.0184 | -0.79 | 4/7 |
| C_pre | 1 | 2406 | 0.0235 | 1.13 | 1.1 | 0.55 | 8/10 | -0.0025 | -0.11 | 4/7 |
| D_asia_ny | 1 | 2406 | -0.0157 | -0.75 | -1.71 | 0.31 | 5/10 | 0.0334 | 1.32 | 5/7 |
| S1_eve_cum5 | 1 | 2187 | -0.0294 | -1.32 | 0.58 | -1.9 | 7/10 | -0.0161 | -0.67 | 4/7 |
| C_night_cum5 | 1 | 2168 | -0.001 | -0.04 | -0.65 | 0.44 | 5/10 | -0.0005 | -0.02 | 4/7 |
| S4_lon_cum5 | 1 | 2322 | 0.0155 | 0.72 | -1.02 | 1.84 | 7/10 | 0.0019 | 0.09 | 3/7 |
| S5_nyam_cum5 | 1 | 2322 | 0.0188 | 0.85 | -0.53 | 1.43 | 6/10 | -0.0063 | -0.26 | 3/7 |
| S1_eve | 3 | 2377 | -0.0043 | -0.21 | 2.49 | -2.12 | 5/10 | -0.0276 | -1.14 | 4/7 |
| S2_late | 3 | 2357 | -0.004 | -0.19 | -0.91 | 0.44 | 6/10 | -0.0363 | -1.44 | 5/7 |
| S3_asia | 3 | 2404 | 0.0266 | 1.29 | 1.26 | 0.64 | 7/10 | 0.0144 | 0.62 | 3/7 |
| S4_lon | 3 | 2404 | 0.042 | 1.96 | 0.38 | 2.2 | 7/10 | 0.0117 | 0.51 | 3/7 |
| S5_nyam | 3 | 2404 | 0.0104 | 0.5 | 0.16 | 0.47 | 5/10 | -0.0059 | -0.25 | 5/7 |
| C_full | 3 | 2384 | 0.0278 | 1.36 | 1.23 | 0.72 | 7/10 | -0.0149 | -0.66 | 4/7 |
| C_post | 3 | 2357 | -0.0164 | -0.75 | 1.7 | -2.03 | 7/10 | -0.0424 | -1.75 | 6/7 |
| C_night | 3 | 2357 | 0.0185 | 0.92 | 0.31 | 0.8 | 5/10 | -0.0166 | -0.7 | 6/7 |
| C_on | 3 | 2357 | 0.0079 | 0.39 | 1.86 | -0.83 | 4/10 | -0.0222 | -0.97 | 4/7 |
| C_day | 3 | 2404 | 0.0292 | 1.45 | 0.11 | 1.77 | 7/10 | -0.0108 | -0.48 | 5/7 |
| C_pre | 3 | 2404 | 0.0484 | 2.37 | 1.1 | 2.11 | 7/10 | -0.001 | -0.04 | 4/7 |
| D_asia_ny | 3 | 2404 | 0.0163 | 0.8 | 0.96 | 0.23 | 9/10 | 0.0195 | 0.83 | 4/7 |
| S1_eve_cum5 | 3 | 2185 | -0.0547 | -1.78 | -0.49 | -1.79 | 7/10 | -0.0287 | -0.79 | 5/7 |
| C_night_cum5 | 3 | 2166 | -0.0126 | -0.37 | -0.82 | 0.05 | 5/10 | 0.0214 | 0.6 | 4/7 |
| S4_lon_cum5 | 3 | 2320 | 0.041 | 1.34 | -1.3 | 2.94 | 7/10 | -0.0214 | -0.65 | 4/7 |
| S5_nyam_cum5 | 3 | 2320 | 0.0013 | 0.04 | -1.5 | 1.23 | 6/10 | 0.0088 | 0.25 | 4/7 |
| S1_eve | 5 | 2375 | -0.0213 | -1.03 | 0.63 | -1.76 | 7/10 | -0.0158 | -0.68 | 4/7 |
| S2_late | 5 | 2355 | -0.0301 | -1.39 | -1.26 | -0.93 | 7/10 | -0.0042 | -0.17 | 4/7 |
| S3_asia | 5 | 2402 | -0.0011 | -0.05 | 0.11 | -0.12 | 6/10 | 0.025 | 0.99 | 5/7 |
| S4_lon | 5 | 2402 | 0.0172 | 0.78 | -1.19 | 1.94 | 6/10 | -0.0043 | -0.19 | 5/7 |
| S5_nyam | 5 | 2402 | 0.0312 | 1.49 | 0.31 | 1.56 | 8/10 | 0.0153 | 0.66 | 5/7 |
| C_full | 5 | 2382 | 0.0019 | 0.09 | -0.52 | 0.51 | 5/10 | 0.0044 | 0.2 | 4/7 |
| C_post | 5 | 2355 | -0.0328 | -1.57 | 0.29 | -2.08 | 6/10 | -0.032 | -1.39 | 4/7 |
| C_night | 5 | 2355 | -0.0119 | -0.57 | -0.91 | -0.12 | 5/10 | 0.0022 | 0.08 | 3/7 |
| C_on | 5 | 2355 | -0.0232 | -1.11 | -0.34 | -1.11 | 7/10 | -0.0142 | -0.62 | 6/7 |
| C_day | 5 | 2402 | 0.0229 | 1.08 | -0.84 | 2.01 | 5/10 | -0.0016 | -0.07 | 4/7 |
| C_pre | 5 | 2402 | 0.0288 | 1.42 | 0.03 | 1.77 | 6/10 | 0.0124 | 0.55 | 3/7 |
| D_asia_ny | 5 | 2402 | -0.0158 | -0.74 | 0.24 | -1.06 | 5/10 | 0.0099 | 0.42 | 3/7 |
| S1_eve_cum5 | 5 | 2183 | -0.0602 | -1.79 | -0.76 | -1.67 | 7/10 | -0.0434 | -1.07 | 5/7 |
| C_night_cum5 | 5 | 2164 | -0.0238 | -0.65 | -0.7 | -0.41 | 6/10 | 0.0425 | 1.07 | 4/7 |
| S4_lon_cum5 | 5 | 2318 | 0.0572 | 1.64 | -0.62 | 2.78 | 8/10 | -0.0327 | -0.88 | 5/7 |
| S5_nyam_cum5 | 5 | 2318 | -0.0113 | -0.33 | -1.69 | 0.83 | 4/10 | 0.0193 | 0.49 | 3/7 |
| C_on_cum20 | 1 | 2412 | 0.0044 | 0.2 | 0.13 | 0.02 | 4/10 | -0.0057 | -0.24 | 5/7 |
| C_day_cum20 | 1 | 2412 | -0.0013 | -0.06 | -1.07 | 0.78 | 7/10 | -0.0191 | -0.83 | 6/7 |
| S5_nyam |>q90_IS| | 1 | 304 | 0.1102 | 1.98 | 1.65 | 1.26 | 6/7 | -0.0851 | -1.05 | 4/5 |
| C_on_cum20 | 3 | 2410 | -0.0002 | -0.01 | -0.89 | 0.29 | 6/10 | -0.0246 | -0.67 | 6/7 |
| C_day_cum20 | 3 | 2410 | -0.0061 | -0.18 | -1.12 | 0.6 | 5/10 | -0.0124 | -0.34 | 5/7 |
| S5_nyam |>q90_IS| | 3 | 304 | 0.1007 | 1.81 | 0.6 | 1.81 | 5/7 | -0.0252 | -0.33 | 4/5 |
| C_on_cum20 | 5 | 2408 | -0.0054 | -0.14 | -0.92 | 0.17 | 6/10 | -0.0331 | -0.77 | 6/7 |
| C_day_cum20 | 5 | 2408 | -0.0146 | -0.38 | -1.1 | 0.35 | 7/10 | -0.0149 | -0.34 | 5/7 |
| S5_nyam |>q90_IS| | 5 | 302 | 0.1247 | 2.14 | 0.33 | 2.33 | 6/7 | -0.0266 | -0.35 | 3/5 |

### B1: segment ort. yıl yıl (bps/gün)
| date | S1_eve | S2_late | S3_asia | S4_lon | S5_nyam | DAY | n |
|---|---|---|---|---|---|---|---|
| 2010.0 | 4.97 | 1.38 | 5.05 | -0.13 | -2.35 | 8.93 | 260.0 |
| 2011.0 | 2.02 | 5.47 | 2.97 | -2.67 | -3.68 | 4.11 | 259.0 |
| 2012.0 | 1.45 | 0.98 | 1.81 | -4.37 | 1.75 | 1.61 | 258.0 |
| 2013.0 | -0.65 | 4.58 | 2.54 | -13.84 | -4.76 | -12.13 | 251.0 |
| 2014.0 | 0.88 | -1.3 | 3.23 | 0.16 | -1.09 | 1.89 | 252.0 |
| 2015.0 | -0.11 | 2.02 | 4.75 | -8.07 | -2.08 | -3.49 | 253.0 |
| 2016.0 | -0.61 | 1.92 | 5.1 | -0.96 | -2.43 | 3.03 | 255.0 |
| 2017.0 | 2.29 | 0.44 | 0.4 | 0.82 | 0.59 | 4.53 | 251.0 |
| 2018.0 | -2.18 | 3.24 | -2.45 | 1.62 | -0.59 | -0.36 | 254.0 |
| 2019.0 | 1.74 | 2.61 | -0.07 | 1.92 | 0.37 | 6.58 | 255.0 |
| 2020.0 | 1.17 | 5.51 | -1.75 | 2.26 | 2.59 | 9.77 | 253.0 |
| 2021.0 | -0.1 | -0.12 | 4.85 | -3.79 | -1.51 | -0.67 | 252.0 |
| 2022.0 | -1.71 | 3.17 | -1.38 | -1.72 | 1.6 | -0.03 | 257.0 |
| 2023.0 | 0.62 | 3.8 | 0.49 | 1.27 | -1.41 | 4.77 | 255.0 |
| 2024.0 | 1.65 | 3.64 | 2.78 | 2.94 | -1.87 | 9.14 | 259.0 |
| 2025.0 | 3.15 | 5.15 | 6.06 | 3.36 | 2.23 | 19.96 | 257.0 |
| 2026.0 | -9.94 | 7.92 | -0.22 | 0.69 | -1.9 | -3.44 | 218.0 |

### B2: segment testleri
| seg | kind | 2010-16_bps | 2010-16_t | IS17-21_bps | IS17-21_t | OOS22-26_bps | OOS22-26_t | full_bps | full_t | yrs_pos |
|---|---|---|---|---|---|---|---|---|---|---|
| S1_eve | mean | 1.15 | 0.93 | 0.29 | 0.25 | -0.97 | -0.69 | 0.37 | 0.5 | 10/17 |
| S1_eve | excess | 0.78 | 0.63 | -0.86 | -0.74 | -2.34 | -1.69 | -0.52 | -0.71 | 8/17 |
| S2_late | mean | 2.15 | 3.37 | 2.46 | 3.6 | 4.64 | 4.57 | 2.93 | 6.59 | 15/17 |
| S2_late | excess | 2.05 | 3.21 | 2.1 | 3.09 | 4.26 | 4.18 | 2.67 | 6.01 | 15/17 |
| S3_asia | mean | 3.64 | 3.62 | 0.06 | 0.06 | 1.61 | 1.0 | 2.04 | 2.99 | 12/17 |
| S3_asia | excess | 3.44 | 3.42 | -0.71 | -0.79 | 0.38 | 0.24 | 1.37 | 2.01 | 11/17 |
| S4_lon | mean | -4.23 | -4.37 | 0.43 | 0.41 | 1.33 | 1.07 | -1.21 | -1.92 | 9/17 |
| S4_lon | excess | -4.36 | -4.57 | -0.39 | -0.37 | 0.26 | 0.21 | -1.81 | -2.91 | 6/17 |
| S5_nyam | mean | -2.08 | -1.53 | 0.28 | 0.21 | -0.22 | -0.13 | -0.84 | -1.01 | 6/17 |
| S5_nyam | excess | -2.31 | -1.7 | -1.13 | -0.84 | -2.17 | -1.31 | -1.92 | -2.29 | 2/17 |

### B3: saatlik
| index | 2010-16 | 2017-21 | 2022-26 | t_all |
|---|---|---|---|---|
| 23->00 | 2.11 | 1.71 | 0.73 | 6.32 |
| 00->01 | 0.1 | -0.61 | 0.33 | -0.17 |
| 01->02 | 0.59 | 0.98 | 1.02 | 2.38 |
| 02->03 | 1.51 | 0.38 | 0.05 | 2.96 |
| 03->04 | -0.18 | -0.6 | 0.07 | -1.14 |
| 04->05 | -0.24 | -0.28 | -0.14 | -1.28 |
| 05->06 | 1.62 | 0.5 | -1.01 | 2.01 |
| 06->07 | -0.03 | -0.06 | 1.25 | 1.19 |
| 07->08 | -0.87 | 0.08 | 0.25 | -0.85 |
| 08->09 | -1.19 | 0.77 | -0.16 | -1.08 |
| 09->10 | -1.5 | 0.01 | 0.08 | -2.33 |
| 10->11 | -0.8 | -0.1 | 0.3 | -1.03 |
| 11->12 | 0.12 | -0.41 | 0.87 | 0.61 |
| 12->13 | 0.12 | 0.1 | 0.22 | 0.31 |
| 13->14 | -1.21 | -0.2 | -0.94 | -1.69 |
| 14->15 | -1.17 | -0.01 | 0.51 | -0.68 |
| 15->16 | 1.19 | 0.49 | -1.39 | 0.54 |
| 16->17 | 0.01 | -0.12 | 0.76 | 0.57 |
| 17->18 | 0.19 | 0.14 | -0.77 | -0.33 |
| 18->19 | -0.13 | -0.3 | 0.5 | 0.0 |
| 19->20 | -0.2 | 0.43 | -0.04 | 0.1 |
| 20->21 | -0.78 | -2.36 | -0.01 | -4.51 |
| 21->22 | -1.24 | -1.35 | -0.03 | -4.59 |
| 22->23 | 1.54 | -0.6 |  | 3.08 |

### B4: alternatif giriş Sharpe
| strat | cost | 2010-16 | IS17-21 | OOS22-26 | VIOPeve20.09+ |
|---|---|---|---|---|---|
| ALT_20_to_settle | 0 | -0.1 | 0.72 | 1.15 | 0.91 |
| ALT_20_to_settle | 5 | -1.01 | -0.4 | 0.37 | 0.11 |
| ALT_20_to_settle | 10 | -1.93 | -1.52 | -0.41 | -0.7 |
| ALT_LN_SD | 0 | 2.15 | 0.4 | 0.76 | 1.01 |
| ALT_LN_SD | 5 | 0.38 | -1.84 | -0.72 | -0.56 |
| ALT_LN_SD | 10 | -1.4 | -4.08 | -2.2 | -2.13 |
| ALT_day_long | 0 | -1.38 | 0.19 | 0.23 | -0.08 |
| ALT_day_long | 5 | -2.47 | -1.14 | -0.8 | -1.12 |
| ALT_day_long | 10 | -3.56 | -2.46 | -1.82 | -2.16 |
| ALT_eve_long | 0 | 0.33 | 0.11 | -0.3 | -0.25 |
| ALT_eve_long | 5 | -1.08 | -1.84 | -1.82 | -1.86 |
| ALT_eve_long | 10 | -2.49 | -3.8 | -3.35 | -3.47 |
| ALT_night_long | 0 | 1.87 | 1.06 | 1.41 | 1.48 |
| ALT_night_long | 5 | 0.26 | -1.05 | 0.28 | 0.25 |
| ALT_night_long | 10 | -1.36 | -3.15 | -0.85 | -0.97 |
| BH_15_15 | 0 | 0.09 | 0.69 | 0.88 | 0.7 |
| BH_15_15 | 5 | 0.09 | 0.69 | 0.88 | 0.7 |
| BH_15_15 | 10 | 0.09 | 0.69 | 0.88 | 0.7 |

### B5: alt yıl yıl
| date | ALT_eve_long | ALT_night_long | ALT_day_long | ALT_20_to_settle | ALT_LN_SD | BH_15_15 |
|---|---|---|---|---|---|---|
| 2010.0 | -0.1 | 3.6 | -18.8 | -2.6 | -2.7 | 22.5 |
| 2011.0 | -7.5 | 8.7 | -28.6 | -7.3 | 12.1 | 10.4 |
| 2012.0 | -8.9 | -5.6 | -19.2 | -12.2 | -11.6 | 4.1 |
| 2013.0 | -14.2 | 5.3 | -59.5 | -41.5 | 39.6 | -30.6 |
| 2014.0 | -10.4 | -7.7 | -14.9 | -10.1 | -18.0 | 4.8 |
| 2015.0 | -12.9 | 4.5 | -38.2 | -21.1 | 17.5 | -8.8 |
| 2016.0 | -14.1 | 5.1 | -21.1 | -3.4 | 1.0 | 7.6 |
| 2017.0 | -6.8 | -10.5 | -9.0 | -6.9 | -26.6 | 11.4 |
| 2018.0 | -18.1 | -10.6 | -10.0 | -8.0 | -25.8 | -0.9 |
| 2019.0 | -8.2 | -6.2 | -6.8 | -0.4 | -24.6 | 16.6 |
| 2020.0 | -9.7 | -3.1 | -0.4 | 9.1 | -28.0 | 24.6 |
| 2021.0 | -12.9 | -0.7 | -26.0 | -14.0 | 0.1 | -1.7 |
| 2022.0 | -16.9 | -8.1 | -12.9 | -8.4 | -20.4 | -0.1 |
| 2023.0 | -11.0 | -1.8 | -13.0 | -2.1 | -14.0 | 12.0 |
| 2024.0 | -8.4 | 3.6 | -9.9 | 6.3 | -11.7 | 23.0 |
| 2025.0 | -4.7 | 15.7 | 1.5 | 29.8 | -11.0 | 50.3 |
| 2026.0 | -37.6 | 6.8 | -15.6 | 3.8 | -2.7 | -8.7 |

### C: baz
| predictor | h | n | ic | t | t_is | t_oos | yrs |
|---|---|---|---|---|---|---|---|
| eb_t (kapanışta) | 1 | 2406 | 0.018 | 0.82 | 0.94 | 0.33 | 6/10 |
| eb_t-1 | 1 | 2405 | 0.0397 | 1.76 | 1.47 | 1.08 | 7/10 |
| ebres_t-1 (dte-düz.) | 1 | 2405 | 0.0388 | 1.7 | 1.41 | 0.93 | 6/10 |
| eb_t-1 -> VİOP-spot | 1 | 2365 | -0.0449 | -2.36 | -0.86 | -1.93 | 6/10 |
| ebres_t-1 -> VİOP-spot | 1 | 2365 | -0.0462 | -2.4 | -0.69 | -2.12 | 7/10 |
| eb_t -> VİOP-spot (mekanik) | 1 | 2386 | -0.5042 | -25.14 | -23.9 | -15.23 | 10/10 |
| eb_t (kapanışta) | 3 | 2404 | 0.0373 | 1.33 | 1.64 | 0.55 | 7/10 |
| eb_t-1 | 3 | 2403 | 0.0518 | 1.87 | 2.05 | 0.87 | 7/10 |
| ebres_t-1 (dte-düz.) | 3 | 2403 | 0.0426 | 1.57 | 1.91 | 0.53 | 6/10 |
| eb_t-1 -> VİOP-spot | 3 | 2323 | -0.0977 | -4.33 | -1.7 | -2.91 | 6/10 |
| ebres_t-1 -> VİOP-spot | 3 | 2323 | -0.109 | -4.84 | -1.94 | -3.41 | 8/10 |
| eb_t -> VİOP-spot (mekanik) | 3 | 2344 | -0.5285 | -25.06 | -23.97 | -14.48 | 10/10 |
| eb_t (kapanışta) | 5 | 2402 | 0.0403 | 1.29 | 1.17 | 0.76 | 7/10 |
| eb_t-1 | 5 | 2401 | 0.0519 | 1.66 | 1.6 | 0.91 | 7/10 |
| ebres_t-1 (dte-düz.) | 5 | 2401 | 0.0432 | 1.42 | 1.6 | 0.55 | 6/10 |
| eb_t-1 -> VİOP-spot | 5 | 2283 | -0.1092 | -4.05 | -1.15 | -2.47 | 8/10 |
| ebres_t-1 -> VİOP-spot | 5 | 2283 | -0.1314 | -4.97 | -1.9 | -3.08 | 9/10 |
| eb_t -> VİOP-spot (mekanik) | 5 | 2303 | -0.5129 | -22.17 | -21.82 | -12.25 | 10/10 |

### C2: rv
| h | cost_bps_2leg | full_sharpe | is_sharpe | oos_sharpe | full_ann_pct | is_ann_pct | oos_ann_pct | turn |
|---|---|---|---|---|---|---|---|---|
| 1.0 | 10.0 | -1.9 | -2.72 | -1.28 | -6.05 | -7.65 | -4.49 | 162.1 |
| 1.0 | 20.0 | -4.25 | -5.58 | -3.23 | -14.15 | -16.59 | -11.77 | 162.1 |
| 3.0 | 10.0 | -0.5 | -1.44 | 0.03 | -1.17 | -2.48 | 0.09 | 59.1 |
| 3.0 | 20.0 | -1.73 | -3.23 | -0.92 | -4.13 | -5.71 | -2.61 | 59.1 |
| 5.0 | 10.0 | -0.1 | -1.01 | 0.39 | -0.23 | -1.54 | 1.03 | 35.8 |
| 5.0 | 20.0 | -0.92 | -2.25 | -0.23 | -2.01 | -3.47 | -0.61 | 35.8 |

### D
| predictor | h | n | ic | t | t_is | t_oos | yrs |
|---|---|---|---|---|---|---|---|
| r_pre (fiks-1s->fiks) | 1 | 2406 | 0.0385 | 1.81 | 0.45 | 1.75 | 6/10 |
| yaz: fiks(14)->15:00 | 1 | 1432 | 0.0229 | 0.83 | 2.42 | -0.62 | 6/10 |
| r_pre (fiks-1s->fiks) | 3 | 2404 | 0.0265 | 1.21 | -1.09 | 2.09 | 5/10 |
| yaz: fiks(14)->15:00 | 3 | 1432 | 0.0393 | 1.48 | 1.31 | 0.71 | 6/10 |
| r_pre (fiks-1s->fiks) | 5 | 2402 | 0.0382 | 1.72 | 0.15 | 1.92 | 5/10 |
| yaz: fiks(14)->15:00 | 5 | 1432 | 0.0283 | 1.05 | 0.46 | 0.91 | 5/10 |
| r_pre kis | 1 | 974 | 0.0898 | 2.76 | 1.63 | 2.08 | 7/10 |
| r_pre yaz | 1 | 1432 | 0.0046 | 0.17 | -0.64 | 0.43 | 6/10 |
| r_pre->r_post (gün içi) | 0 | 4354 | -0.0183 | -1.18 | -1.41 | -0.21 | 11/17 |

### D2
| date | pre2(fiks-2->-1) | pre(fiks-1->fiks) | post(fiks->+1) |
|---|---|---|---|
| 2010.0 | -1.06 | -4.28 | 2.22 |
| 2011.0 | -0.16 | -4.73 | 0.89 |
| 2012.0 | 0.56 | 0.19 | 4.27 |
| 2013.0 | -1.18 | -4.11 | 1.25 |
| 2014.0 | 0.82 | -1.36 | -0.21 |
| 2015.0 | -2.1 | -0.2 | -0.98 |
| 2016.0 | 1.38 | -2.87 | -0.11 |
| 2017.0 | -0.06 | -1.22 | 2.71 |
| 2018.0 | 0.0 | -0.44 | 0.65 |
| 2019.0 | -0.53 | -0.37 | 1.63 |
| 2020.0 | 1.58 | 0.8 | -1.14 |
| 2021.0 | -0.12 | -2.69 | 0.45 |
| 2022.0 | 0.13 | 2.2 | 0.97 |
| 2023.0 | -0.75 | -1.58 | -0.55 |
| 2024.0 | -0.02 | -1.08 | -0.34 |
| 2025.0 | 0.16 | -1.57 | 2.48 |
| 2026.0 | -2.18 | -0.04 | -4.98 |

### E
| predictor | h | n | ic | t | t_is | t_oos | yrs |
|---|---|---|---|---|---|---|---|
| gap (Pzt satırı) | 1 | 468 | 0.036 | 0.75 | 1.16 | 0.44 | 5/10 |
| Cuma15->Pzt00 | 1 | 464 | 0.0314 | 0.53 | 1.54 | -0.32 | 6/10 |
| gap (Pzt satırı) | 3 | 468 | -0.0403 | -0.86 | -0.79 | -0.27 | 4/10 |
| Cuma15->Pzt00 | 3 | 464 | 0.0058 | 0.11 | 0.92 | -0.63 | 6/10 |
| gap (Pzt satırı) | 5 | 467 | -0.0282 | -0.56 | 0.06 | -0.69 | 8/10 |
| Cuma15->Pzt00 | 5 | 463 | -0.0137 | -0.27 | 0.98 | -1.03 | 5/10 |
| gap -> Pzt 07->15 (gün içi, spot 2010+) | 0 | 850 | 0.0385 | 1.05 | 0.35 | 1.22 | 9/17 |
| Cuma 15-20 -> gap (spot 2010+) | 0 | 844 | -0.0413 | -1.06 | -2.2 | 0.86 | 11/17 |

### E2
| gun | ort_bps | t_ham | fark_bps | t_fark | t_is | t_oos | yil_ayni | spot1016_fark_bps | spot1016_t | n |
|---|---|---|---|---|---|---|---|---|---|---|
| Pzt | -3.56 | -0.81 | -6.64 | -1.51 | -0.38 | -1.58 | 7/10 | 10.34 | 1.86 | 485 |
| Sal | 2.64 | 0.64 | -0.44 | -0.11 | -0.64 | 0.37 | 5/10 | 0.05 | 0.01 | 485 |
| Çar | 8.47 | 1.98 | 5.38 | 1.26 | -0.14 | 1.57 | 8/10 | -6.05 | -1.19 | 485 |
| Per | 1.9 | 0.42 | -1.19 | -0.26 | -0.11 | -0.25 | 6/10 | -6.88 | -1.14 | 489 |
| Cum | 5.99 | 1.52 | 2.91 | 0.74 | 0.76 | 0.38 | 7/10 | 2.59 | 0.46 | 483 |

### F
| predictor | h | n | ic | t | t_is | t_oos | yrs |
|---|---|---|---|---|---|---|---|
| volz_t-1 | 1 | 2405 | -0.0023 | -0.11 | -0.76 | 0.59 | 6/10 |
| ret_x_volz_t-1 | 1 | 2405 | 0.015 | 0.72 | 1.04 | -0.15 | 6/10 |
| dOI_t-1 | 1 | 2424 | -0.0091 | -0.43 | -0.47 | -0.0 | 7/10 |
| sign_ret_x_dOI_t-1 | 1 | 2424 | 0.0187 | 0.91 | 0.46 | 0.64 | 8/10 |
| volz_t-1 | 3 | 2403 | -0.0001 | -0.0 | -0.77 | 0.63 | 6/10 |
| ret_x_volz_t-1 | 3 | 2403 | 0.0139 | 0.64 | 0.25 | 0.5 | 6/10 |
| dOI_t-1 | 3 | 2422 | -0.0073 | -0.36 | -0.87 | 0.55 | 6/10 |
| sign_ret_x_dOI_t-1 | 3 | 2422 | -0.0166 | -0.79 | -0.19 | -1.21 | 7/10 |
| volz_t-1 | 5 | 2401 | 0.0065 | 0.23 | -0.24 | 0.61 | 4/10 |
| ret_x_volz_t-1 | 5 | 2401 | 0.0074 | 0.35 | -0.45 | 0.59 | 6/10 |
| dOI_t-1 | 5 | 2420 | 0.0185 | 0.87 | 0.12 | 1.26 | 5/10 |
| sign_ret_x_dOI_t-1 | 5 | 2420 | -0.0161 | -0.77 | -0.81 | -0.39 | 6/10 |

### F2
| date | gece_uzl->acilis | gunduz_acilis->uzl | n |
|---|---|---|---|
| 2017.0 | 2.98 | -0.83 | 208.0 |
| 2018.0 | -2.05 | 0.37 | 251.0 |
| 2019.0 | -0.49 | 6.13 | 249.0 |
| 2020.0 | 0.66 | 7.51 | 252.0 |
| 2021.0 | 1.46 | -3.47 | 249.0 |
| 2022.0 | -1.18 | -0.65 | 252.0 |
| 2023.0 | 1.35 | 0.33 | 253.0 |
| 2024.0 | 4.99 | 1.52 | 250.0 |
| 2025.0 | 9.14 | 8.73 | 251.0 |
| 2026.0 | -6.6 | -0.87 | 212.0 |

### R: kayıt (p<0.05)
| family | test_id | h | ic | t | t_is | t_oos | yrs_same_sign | yrs | p | q_bh |
|---|---|---|---|---|---|---|---|---|---|---|
| c_basis | c_eb_t_rel_h1 | 1 | -0.5042 | -25.1419 | -23.8999 | -15.2287 | 10.0 | 10.0 | 0.0 | 0.0 |
| c_basis | c_eb_t_rel_h3 | 3 | -0.5285 | -25.0618 | -23.971 | -14.4781 | 10.0 | 10.0 | 0.0 | 0.0 |
| c_basis | c_eb_t_rel_h5 | 5 | -0.5129 | -22.1747 | -21.8205 | -12.2499 | 10.0 | 10.0 | 0.0 | 0.0 |
| b_segmean | b_mean_S2_late | 0 | 0.0003 | 6.5884 | 3.5974 | 4.5669 | 15.0 | 17.0 | 0.0 | 0.0 |
| b_altentry | b_ALT_day_long | 0 | -0.0007 | -6.5414 | -2.5202 | -1.8138 | 16.0 | 17.0 | 0.0 | 0.0 |
| b_altentry | b_ALT_eve_long | 0 | -0.0005 | -6.2803 | -4.0544 | -4.2553 | 17.0 | 17.0 | 0.0 | 0.0 |
| b_segexcess | b_excess_S2_late | 0 | 0.0003 | 6.0083 | 3.0892 | 4.1834 | 15.0 | 17.0 | 0.0 | 0.0 |
| c_basis | c_ebr_tm1_rel_h5 | 5 | -0.1314 | -4.9702 | -1.8992 | -3.0781 | 9.0 | 10.0 | 0.0 | 0.0 |
| c_basis | c_ebr_tm1_rel_h3 | 3 | -0.109 | -4.8439 | -1.9431 | -3.4051 | 8.0 | 10.0 | 0.0 | 0.0 |
| c_basis | c_eb_tm1_rel_h3 | 3 | -0.0977 | -4.3327 | -1.6991 | -2.9073 | 6.0 | 10.0 | 0.0 | 0.0003 |
| c_basis | c_eb_tm1_rel_h5 | 5 | -0.1092 | -4.048 | -1.1537 | -2.469 | 8.0 | 10.0 | 0.0001 | 0.0009 |
| b_segmean | b_mean_S3_asia | 0 | 0.0002 | 2.9903 | 0.0633 | 0.9998 | 12.0 | 17.0 | 0.0028 | 0.0446 |
| b_segexcess | b_excess_S4_lon | 0 | -0.0002 | -2.911 | -0.3689 | 0.2103 | 11.0 | 17.0 | 0.0036 | 0.0532 |
| d_fix | d_rpre_kis_h1 | 1 | 0.0898 | 2.7598 | 1.6294 | 2.0792 | 7.0 | 10.0 | 0.0058 | 0.0793 |
| d_fix | d_mean_r_pre | 0 | -0.0001 | -2.7245 | -1.0326 | -0.3924 | 14.0 | 17.0 | 0.0064 | 0.0824 |
| a_early | a_early_S2_late_h1 | 1 | -0.0633 | -2.6083 |  |  | 6.0 | 7.0 | 0.0091 | 0.1092 |
| e_weekend | e_early_gap_h1 | 1 | -0.1207 | -2.4528 |  |  |  |  | 0.0142 | 0.1601 |
| c_basis | c_ebr_tm1_rel_h1 | 1 | -0.0462 | -2.4036 | -0.6904 | -2.1244 | 7.0 | 10.0 | 0.0162 | 0.1732 |
| a_segment | a_C_pre_h3 | 3 | 0.0484 | 2.3696 | 1.101 | 2.1111 | 7.0 | 10.0 | 0.0178 | 0.1767 |
| c_basis | c_eb_tm1_rel_h1 | 1 | -0.0449 | -2.3573 | -0.8637 | -1.9299 | 6.0 | 10.0 | 0.0184 | 0.1767 |
| b_segexcess | b_excess_S5_nyam | 0 | -0.0002 | -2.2858 | -0.8403 | -1.3052 | 15.0 | 17.0 | 0.0223 | 0.2036 |
| b_altentry | b_ALT_LN_SD | 0 | -0.0003 | -2.2093 | -4.174 | -1.7537 | 12.0 | 17.0 | 0.0272 | 0.237 |
| a_bigmove | a_S5big_h5 | 5 | 0.1247 | 2.1447 | 0.334 | 2.3251 | 6.0 | 7.0 | 0.032 | 0.2669 |
| g_is_selected | g_is_best_S1_eve_h3 | 3 | -0.0626 | -2.12 | 2.49 | -2.12 |  |  | 0.034 | 0.272 |
| b_segexcess | b_excess_S3_asia | 0 | 0.0001 | 2.0139 | -0.791 | 0.2353 | 11.0 | 17.0 | 0.044 | 0.3381 |
| a_bigmove | a_S5big_h1 | 1 | 0.1102 | 1.9767 | 1.6532 | 1.2555 | 6.0 | 7.0 | 0.0481 | 0.355 |
