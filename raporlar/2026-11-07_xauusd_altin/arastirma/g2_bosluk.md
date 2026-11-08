# g2_bosluk — "Kapanıştan kapanışa" hangi fiyat? Uygulanabilirlik ve lead-lag'lerin bu fiyatla sağlamlığı

Tarih: 2026-11-08. Sözleşme: VİOP F_XAUUSD (Dolar/Ons Altın vadeli). Kod ve çıktılar: `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/g2_kapanis/` (`run_all.sh` hepsini baştan üretir). Bu dosyanın aynısı `out/g2_kapanis/RAPOR.md`.

Veri: BIST ana bültenleri 2017-03-06 → 2026-11-06 (panel), BIST akşam bültenleri `viop_as_bul_YYYYMMDD.csv` 2020-09-18 → 2026-11-06 (1.541 gün denendi, 1.518 dosyada XAUUSD satırı var, 23 gün 404), Dukascopy XAUUSD BID dakikalık mumları 590 gün (2017-01 → 2026-11; 2023-01-02 → 2023-04-28 arası her iş günü, 2022-10 → 2023-06 yoğun).

Not: Bu turda web arama kotası baştan dolmuştu (WebSearch "limit doldu" döndü). Bu yüzden birincil kaynakları bilinen adreslerden doğrudan çektim (BIST prosedür ve revizyon PDF'leri, BIST duyuru PDF'leri, TradingView sayfaları, aracı kurum tarife sayfaları). Arama gerektiren bazı noktalar "bulunamadı" olarak kaldı.

---

## 0. Kısa sonuç

1. **"Kapanış" = günlük uzlaşma fiyatı**: seans sonundan önceki son 10 dakikanın miktar ağırlıklı ortalaması (VWAP). Pencerenin saati 2017'den beri **bir kez** değişti:
   - **10.02.2023'e kadar:** seans 18:15 TSİ'de bitiyordu. Pencere **18:05–18:15 TSİ = 15:05–15:15 UTC**. Yarım günlerde 12:35–12:45 TSİ.
   - **13.02.2023'ten beri:** seans 18:10 TSİ'de bitiyor. Pencere **18:00–18:10 TSİ = 15:00–15:10 UTC**. Yarım günlerde 12:30–12:40 TSİ.
   - Belge: Prosedür revizyon karşılaştırma tablosu, rev. 54 (06.03.2023 tarihli 15626 sayılı duyuru). Bu duyuru, değişikliğin 14.02.2023 tarihli 15151 sayılı duyuruyla devreye alındığını söylüyor. 15151'in metni bulunamadı (404).
   - Ampirik kırılma: son işlem fiyatına göre son 18:15 günü 10.02.2023, ilk 18:10 günü 13.02.2023.
2. **23.09.2022'de açılış seansı başladı** (09:20 emir toplama, 09:25 eşleştirme, 09:30 sürekli işlem; duyuru 11326). Seans sonu o tarihte değişmedi (18:15).
3. **Ana bülten yalnız normal seansı içerir.** Önceki akşamı da, aynı akşamı da içermez.
   - "AÇILIŞ FİYATI" 23.09.2022'den beri açılış seansının tek fiyatıdır (os_price ile 1.601 satırın %100'ünde eşit). Öncesinde normal seansın 09:30'daki ilk işlemidir. Akşam açılışıyla eşitliği %0,5.
   - Önceki akşamın fiyat aralığı ana bülten aralığının dışına günlerin %58'inde (2020-09 → 2022-09) ve %71'inde (2022-09 → 2026) taşıyor. Ana bülten önceki akşamı içerseydi bu oran %0 olurdu.
   - DATA_README'deki "AÇILIŞ = akşamın ilk işlemi" ve a1'deki "yüksek/düşük önceki akşam dahil" varsayımları **yanlış**.
4. **TradingView BIST:XAUUSD1! günlük çubuğu:** "Settlement as close" ayarı açıkken (varsayılan) kapanış = **uzlaşma**. 06.11.2026'da TV fiyatı 4.078,8 = uzlaşma. Normal seans son işlemi 4.079,3, akşam kapanışı 4.092 idi.
   - TV günlük hacmi = normal seans + **aynı takvim gününün** akşamı (06.11.2026: 18.465 + 2.555 = 21.020 = TV "21,02 K").
   - Ayar kapatılırsa kapanış, akşam seansının son işlemi olur (23:00 TSİ).
5. **VİOP'ta uzlaşma fiyatından emir (TAS/MOC) yok.** Prosedürdeki emir yöntemleri yalnız Limit, Piyasa ve Piyasadan Limite. Perakende yatırımcı uzlaşmayı 18:00:00–18:09:59 arasına eşit dilimlere bölünmüş emirle yakalayabilir.
   - Spot vekiliyle ölçtüm (2023-02-13 → 2026-11-06, 318 gün). 5 dilim, pencere VWAP'ından medyan 0,58 bps sapıyor (p90 1,81). 10 dilim 0,27 bps (p90 1,19). Seans sonunda tek emir 4,78 bps (p90 13,39).
6. **Kayma vekili:** 2026'da ön vadede |KAPANIŞ − UZLAŞMA| medyan 4,54 bps, ortalama 6,64, p90 12,99, p95 20,55, en büyük 58,66 bps (28.01.2026). 212 gün. 2017–2025'te yıllık medyan 2,0–3,9 bps.
7. **Piyasa yapıcı azami spread (Prosedür rev. 69, 23.02.2026):**
   - Normal seans: vadeye <30 gün 2,80 USD (≈6,9 bps), <60 gün 3,20, <90 gün 3,60, ≥90 gün 4,00 USD.
   - Akşam seansı: 5,60 / 6,40 / 7,20 / 8,00 USD.
   - İkisinde de asgari emir 20 sözleşme, piyasada bulunma süresi en az %70, en yakın 2 vade.
8. **Aracı kurum komisyonları (2026):** Ata onbinde 0,9; Strateji internet binde 0,20; İş Bankası onbinde 10'dan 5'e kademeli; Info binde 2'ye kadar. Hepsine %5 BSMV eklenir. Borsa payı yüzbinde 3 ve Takasbank yüzbinde 1 de taraf başı ayrıca alınır. Gidiş-dönüş maliyet ≈ 2,7 / 5,0 / 21,8–11,3 / 42,8 bps (spread hariç).
9. **Sağlamlık (giriş/çıkış fiyatı değişince):** Uzlaşma yerine bülten KAPANIŞ kullanmak sonucu neredeyse hiç değiştirmiyor. İki serinin günlük getiri korelasyonu 0,9958, Sharpe farkı ±0,1.
   - Akşam kapanışında (23:00 TSİ) işlem yapınca LOWMOM ve a6 hafif iyileşiyor. a5 C1 ve a3 NFP h3 kötüleşiyor: tam dönemde 0,48 → 0,31 ve 0,68 → 0,62, 2020-09+ döneminde 0,83 → 0,62.
10. **Maliyet belirleyici.**
    - 5 bps'te bütün adaylar pozitif.
    - 22–25 bps'te (varsayılan perakende) yalnız **A1-LOWMOM h5** sağlam: tam dönem drift çıkarılmış Sharpe 0,53–0,70, OOS 1,36–1,52 (t 3,0–3,3).
    - a6 Çin bileşiği h5 ve a3 NFP h3 sınırda: OOS 0,50–0,92, t 1,1–2,0; tam dönem 0,02–0,30.
    - a4 GDXJ artığı, a5 C1 ve h=1 kuralları 22–25 bps'te sıfır ya da negatif.
11. **Uygulama tamponu kalmadı:** 13.02.2023'ten beri uzlaşma penceresi tam 15:00:00 UTC'de başlıyor. Panel kuralı "karar anı = 15:00 UTC" ile pencere arasında artık 0 dakika var (öncesinde 5 dakika vardı). 15:00 spotuyla kurulan sinyal ya 17:59 TSİ'de hesaplanıp 18:00–18:10'a dilimli emir olarak girilmeli ya da KAPANIŞ veya akşam fiyatıyla uygulanmalı. Bu üç yolun Sharpe'ı birbirine yakın (madde 9).

---

## 1. Uzlaşma penceresinin tarihçesi

### 1.1 Belgeler

Günlük uzlaşma kuralı Prosedür Ek-1 R'de yazıyor (rev. 70, 01.07.2026). Seans sona ermeden önceki son 10 dakikadaki tüm işlemlerin miktar ağırlıklı ortalaması alınıyor. 10'dan az işlem varsa geriye doğru son 10 işlem, seansta 10'dan az işlem varsa bütün işlemler, hiç işlem yoksa önceki uzlaşma kullanılıyor. Fiyat en yakın 0,10 adımına yuvarlanıyor ve özel işlem bildirimleri hesaba girmiyor. Bu kural 2017'den beri aynı. Değişen tek şey "seans sonu" saati.

| Dönem (yürürlük) | Ons altın normal seans (TSİ) | Uzlaşma penceresi TSİ / UTC | Yarım gün (TSİ) | Kaynak |
|---|---|---|---|---|
| 2017-03 → 2022-09-22 | 09:30–18:15 ("Diğer Türev Pazarları") | 18:05–18:15 / **15:05–15:15** | 09:30–12:45 (pencere 12:35–12:45 = 09:35–09:45 UTC) | Revizyon karşılaştırma tablosu, 2017/44 (06.04.2017) Ek-3: eski ve yeni metinde "Diğer Türev Pazarları 09:30-18:15", "Pay Türev Pazarı 09:30-18:10" |
| 18.09.2020 → | Akşam seansı eklendi: 19:00–23:00 TSİ (16:00–20:00 UTC) | Uzlaşmaya girmez | Yarım günde akşam yok | 17.09.2020 tarihli 2020/57 sayılı duyuru ("Dolar/Ons altın vadeli işlem sözleşmelerinin akşam seansında işlem görmesi"); ilk akşam bülteni 2020-09-18 |
| 31.12.2020 → | Yılın son işlem gününde akşam seansı yok | — | — | 17.12.2020 tarihli 2020/79 sayılı duyuru |
| 23.09.2022 → | Açılış seansı: emir toplama 09:20, eşleştirme 09:25 (+30 sn içinde rassal), sürekli işlem 09:30–18:15 | 18:05–18:15 / 15:05–15:15 (değişmedi) | 09:20–12:45 | Duyuru 11326 (21.09.2022), rev. 51. Aynı tarihte pay vadelileri 18:10'dan 18:15'e alındı ("diğer sözleşmelerde olduğu gibi") |
| **13.02.2023 →** (ampirik; belge 14.02.2023) | 09:20–18:10 & 19:00–23:00 | **18:00–18:10 / 15:00–15:10** | 09:20–12:40 (pencere 12:30–12:40 = 09:30–09:40 UTC) | Rev. 54 karşılaştırma tablosu: Ek-3 A ve B'de "09:20-18:15 / 09:20-12:45" → "09:20-18:10 / 09:20-12:40", "VIOP_SEANS_SONU 18:15:00 / 12:45:00" → "18:10:00 / 12:40:00". Duyuru 15626 (06.03.2023, rev. 54 yürürlüğü 10.03.2023), "14/02/2023 tarihli ve 15151 sayılı Duyurumuz ile devreye alınan uygulama değişikliklerine ilişkin" güncellemeyi yapıyor |
| 01.07.2026 (rev. 70, güncel) | 09:20–18:10 & 19:00–23:00 | 18:00–18:10 / 15:00–15:10 | 09:20–12:40 | Prosedür Ek-3 B: VIOP_SEANS_SONU 18:10:00 / 12:40:00, UF ilanı 18:45+, akşam öncesi 18:50, akşam 19:00–23:00, akşam gün sonu 23:15 |

- 15151 sayılı duyurunun metnine ulaşamadım. `duyuru-15151-tr.pdf` ve `-TR.pdf` 404 döndü. Belgenin tam yürürlük tarihi bu yüzden **bulunamadı**. Ampirik kırılma (§1.2) 13.02.2023 Pazartesi'yi gösteriyor. Duyuru tarihi 14.02.2023 ve "devreye alınan" ifadesi geçmiş zamanlı. Bu, duyurunun uygulamadan bir gün sonra yayımlanmış olabileceğini düşündürüyor (06.02.2023 depremi sonrası dönem). Bu yorum benim çıkarımım.
- Revizyon karşılaştırma tablosunda 2017–2026 arasında başka bir seans sonu değişikliği **yok**. Ons altın için seans saatine değen değişiklikler yalnız şunlar: 2020/57 (akşam seansı), 2020/79 (yıl sonu akşamı yok), 11326 (açılış seansı) ve rev. 54 (18:10).
- İşbank'ın eğitim dokümanı (görev metnine göre 22.02.2024 tarihli; tarihi PDF'ten ayrıca doğrulamadım) kıymetli madenler için "Normal Seans İşlemleri 09:30-18:15" yazıyor. Bu, değişiklikten bir yıl sonra bile **eskimiş** bir bilgi. Aynı dokümanda yalnız pay vadelileri 18:10.
- BIST duyuru 30572 (19.11.2024) bakır vadelisinin işleme açılmasıyla ilgili (rev. 63). Seans saatiyle ilgisi yok. Ons altının akşam seansında olduğu Prosedür md. 7'den doğrulanıyor: "Akşam seansında … Dolar/Ons Altın, Dolar/Ons Gümüş, Dolar/Ons Platin, Dolar/Ons Paladyum ve Dolar/Ton Bakır Vadeli İşlem Sözleşmeleri işlem görür".

### 1.2 Ampirik doğrulama (dakikalık spot)

**Yöntem A (seans sonu, keskin):** Bülten KAPANIŞ fiyatı seansın son işlemi. Seansın bittiği ana denk gelmesi beklenir.
- Her gün ön vadenin KAPANIŞ fiyatını taşıma düzeltmesiyle spota çevirdim: C* = C · exp(−c·T1). c, en yakın iki vadenin uzlaşma farkından çıkan günlük taşıma oranının ±10 iş günü medyanı. T1, vadeye kalan takvim günü.
- C*'ı τ = 15:00…15:25 UTC anındaki Dukascopy spot fiyatıyla (τ−1 dakikasının kapanışı) karşılaştırdım.
- Ölçüt, ardışık günlerde farkın değişiminin MAD'ı. Bu fark, günden güne yavaş değişen taban ve BID/mid hatasını iptal eder.

| Dönem | n (gün çifti) | MAD τ=15:10 | MAD τ=15:14 | MAD τ=15:15 | En iyi τ |
|---|---|---|---|---|---|
| 2017-03 → 2023-02-12 | 145 | 8,47 | 4,76 | **4,57** | **15:15** (= 18:15 TSİ) |
| 2023-02-15 → 2023-03-31 | 31 | **5,45** | 8,51 | 7,93 | **15:10** (= 18:10 TSİ) |
| 2023-04-01 → 2026-11-06 | 236 | **5,92** | 11,80 | 13,48 | **15:10** |

- **Kırılma tarihi.** 2022-10 → 2023-06 yoğun blokta toplam kaybı en aza indiren ayrım: son 18:15 günü **10.02.2023**, ilk 18:10 günü **13.02.2023**. Sıradaki adaylar 14.02 ve 10.02, kayıp farkları küçük.
- Aylık skor |Δ(15:10)| − |Δ(15:15)| (pozitif = 18:15 rejimi):
  - 2022-10: +5,67; 2022-11: +4,92; 2022-12: +8,24; 2023-01: +5,38.
  - 2023-02: −0,75 (karışık ay); 2023-03: −2,30; 2023-04: −3,46; 2023-05: −3,06; 2023-06: −2,98.
- Gün gün yerel ofset düzeltmeli seviye: 23.01–10.02.2023 arasında 15 günün 14'ünde 15:15 daha yakın. 13.02–10.03.2023 arasında 20 günün 17'sinde 15:10 daha yakın; 13–23 Şubat'ın 9 gününün hepsinde 15:10.
- Yıl bazında seviye yöntemi (medyan etrafı MAD): 2018–2022 ve 2023 Ocak–12 Şubat'ın her birinde MAD(15:15) < MAD(15:10). 2024, 2025 ve 2026'da tersi geçerli. 2026: 9,33'e karşı 14,98. 2017 (n=27) gürültülü, en iyi τ 15:22. 2023'ün 13 Şubat–Aralık bölümünde seviye yöntemi gürültülü (MAD ≈11, iki τ ayrışmıyor). Bu dilim için ardışık gün yöntemi esas alınmalı.

**Yöntem B (uzlaşma penceresi):** Taşıma düzeltmeli uzlaşmayı, tik hacmi ağırlıklı (o+c)/2 spot ortalamasıyla karşılaştırdım. Pencereler 10 dakikalık [a, a+10), a = 14:40…15:20 UTC.

| Dönem | n | Ardışık fark MAD: 15:00–15:10 | 15:01–15:11 | 15:05–15:15 | En iyi | Seviye MAD: 15:00–15:10 / 15:05–15:15 |
|---|---|---|---|---|---|---|
| 2017-03 → 2023-02-14 | 133 çift / 248 gün | 8,58 | 7,27 | **3,99** | **15:05–15:15** | 5,72 / **4,14** (en iyi 15:06–15:16, 4,07) |
| 2023-02-15 → 2026-11 | 266 çift / 309 gün | 5,25 | **4,99** | 7,50 | **15:01–15:11** | 12,08 / 11,79 (gürültülü; en iyi 15:02–15:12) |

- Sonuç belgeyle uyumlu: önce 15:05–15:15 UTC, sonra 15:00–15:10 UTC. 2023 sonrası en iyi pencere 1 dakika geç çıkıyor (15:01). Bunun nedeni Dukascopy dakika damgası ya da VİOP'un spotu ~1 dakika gecikmeyle izlemesi olabilir. 1 dakikalık fark yorum değiştirmiyor.
- Dosyalar: `log_03_pencere.txt`, `log_05_kirilma.txt`, `log_06_sonislem.txt`, `log_08_yillik.txt`, `pencere_gunluk.csv`, `sonislem_ardisik_fark.csv`.

**Analizlere etkisi.**
- Panelde hedef `v_ret` uzlaşmadan uzlaşmaya ölçülüyor ve doğru. Ancak zaman damgası 2017-03 → 2023-02-10'da ≈15:10 UTC (pencere ortası), 2023-02-13'ten sonra ≈15:05 UTC.
- "Karar anı 15:00 UTC" kuralı ileriye bakma üretmiyor: sinyal pencere başlamadan biliniyor. Ama 2023-02-13'ten beri uygulama tamponu sıfır (önceden 5 dakika).
- 15:00–15:10 UTC arasında yayımlanan bir bilgi (ör. ABD 10:00 ET verileri yazın 14:00 UTC'de; kışın 15:00 UTC'de) 2023 sonrasında uzlaşmanın içine düşer. ISM, JOLTS ve tüketici güveni kışın tam 15:00:00 UTC'de çıkıyor. Bu günlerde uzlaşma, verinin ilk 10 dakikalık tepkisini kısmen içeriyor.

---

## 2. Bülten alanlarının anlamı

### 2.1 Ana bülten (`viop_YYYYMMDD.csv`)

| Alan | Anlamı | Kanıt |
|---|---|---|
| AÇILIŞ FİYATI | 23.09.2022'den beri açılış seansının tek fiyatı (denge fiyatı). Öncesinde normal seansın ilk işlemi (09:30 TSİ = 06:30 UTC) | os_price olan 1.601 satırın **%100'ünde** AÇILIŞ = ACILIS SEANSI FIYATI. Ön vadede os_price payı: 2022 %21,8, 2023 %84,6, 2024 %85,2, 2025 %96,8, 2026 %92,9. Açılış seansında işlem olmayan günlerde AÇILIŞ boş kalıyor ya da ilk sürekli işlem yazılıyor; bu ayrım test edilmedi. Spot karşılaştırması (taşıma düzeltmeli): AÇILIŞ'ın 06:30 UTC spotuna mutlak sapması medyan 13,6 / 14,8 / 12,2 bps (2017→2020-09 / 2020-09→2022-09 / 2022-09+). Önceki gün 16:00 UTC spotuna sapma 18,3 / 21,5 / 31,9 bps. Akşamın ilk işlemiyle eşitlik %0,6 / %0,5 |
| EN YÜKSEK / EN DÜŞÜK | Yalnız normal seans (açılış seansı dahil) | Önceki takvim gününün akşam aralığı (e_high > high ya da e_low < low) ana bülten aralığının dışına **%57,7** (2020-09 → 2022-09, 496 gün) ve **%70,9** (2022-09+, 1.021 gün) taşıyor. Aynı takvim gününün akşamı için %50,5. Kapsasaydı %0 olurdu |
| KAPANIŞ FİYATI | Normal seansın son işlemi. 18:15'e (≈15:15 UTC) kadar, 13.02.2023'ten beri 18:10'a (≈15:10 UTC) kadar | §1.2 Yöntem A. Akşam kapanışıyla eşitlik %0,4 |
| AĞIRLIKLI ORTALAMA, HACİM, İŞLEM SAYISI | Normal seans | 06.11.2026: ana 18.465 + akşam 2.555 = 21.020 = TradingView hacmi; ana + önceki akşam (3.561) = 22.026 ≠ TV |
| UZLAŞMA FİYATI | Son 10 dk VWAP (§1) | — |
| AÇIK POZİSYON | Gün sonu (akşam bülteninde boş) | Akşam bülteninde UZLAŞMA ve AÇIK POZİSYON alanları boş |

- Normal seansa ait istatistiklerin (OI, baz, uzlaşma, limitler ve kapanış hariç) akşam seansı öncesinde "temizlendiği" Prosedür Ek-3'te yazıyor (VIOP_AS_ONCESI açıklaması). Bu, akşamın kendi açılış/yüksek/düşük değerleriyle başladığını gösteriyor.
- **Etkilenen sinyaller.**
  - a1'deki `loc_v|mt` ve `loc_v|mt1` (uzlaşmanın gün aralığındaki yeri) "önceki akşam dahil" varsayımıyla tanımlanmış. Hesap aslında **normal seans aralığını** kullanıyor. Sonuçları zaten "YOK"tu (t ≤ 1,5); yorum değişiyor, sonuç değişmiyor.
  - a1'in `mt` bilgi zamanı tablosundaki "VİOP gün t yüksek/düşük (önceki akşam seansı dahil)" ifadesi düzeltilmeli.
  - a2'nin `f_micro.py` dosyası `v_open`'ı doğru biçimde "~06:30 UTC normal seans açılışı" olarak kullanmış.
  - Ayakta kalan adayların (§5) hiçbiri v_open, v_high ya da v_low kullanmıyor.

### 2.2 Akşam bülteni (`viop_as_bul_YYYYMMDD.csv`) ve md. 9.5

- Dosya tarihi D = akşamın **takvim günü**. İşlemler D günü 19:00–23:00 TSİ (16:00–20:00 UTC) arasında. Örnek: 06.11.2026 Cuma akşamı F_XAUUSD1226 açılış 4.080,5, kapanış 4.092, hacim 2.555.
- Prosedür md. 9.5: akşam işlemleri "bir sonraki normal seans işlemi olarak değerlendirilir". Takas, teminat ve kâr/zarar açısından D akşamının işlemleri **sonraki işlem günü** T = next_td(D) (Cuma akşamı için Pazartesi) uzlaşmasıyla hesaplanıyor. Akşamın baz fiyatı D'nin normal seans uzlaşması.
- **Veri hazırlığı:**
  1. Fiyat zaman damgası olarak akşam bülteni D → D günü 16:00–20:00 UTC kullanılmalı.
  2. Kâr/zarar ve takas günü olarak D akşamı → T = next_td(D) atanmalı.
  3. BIST tanımıyla işlem günü T hacmi = ana bülten(T) + akşam bülteni(önceki işlem günü). TradingView tanımıyla takvim günü D hacmi = ana(D) + akşam(D).
  4. Ana bülten T'nin OHLC'si önceki akşamı **içermez**. "T günü yüksek/düşük" ancak iki dosya birleştirilerek kurulabilir.
- Akşam seansı olmayan günler: yarım günler (28 Ekim, bayram arifeleri), yılın son işlem günü. Açıklanamayan iki gün daha var: 04.08.2023 ve 29.11.2024 (dosya 404, nedeni **bulunamadı**). 2020-09-21 → 2026-11-06 arasında ön vadede akşam kapanışı olan gün payı %98,2.

---

## 3. TradingView BIST:XAUUSD1! ve yerel veri sağlayıcıları

**Bulunanlar (birincil):**
- **Kapanış:** TradingView 13.03.2024 blog notu, BIST vadelilerinde grafiğin günlük kapanış olarak "Settlement or Last" fiyatından birini gösterebildiğini yazıyor. Ayar: "Use settlement as close on daily interval" ya da grafiğin altındaki SET düğmesi. Aynı not, gün içi aralıklarda uzlaşmanın gösterilmediğini söylüyor. Varsayılanın açık olduğu bu notta yazmıyor.
- **Ampirik kontrol:** TV sembol sayfası (07–08.11.2026) "XAUUSD1! trades at 4,078.8 USD" gösteriyor. Bu, 06.11.2026 uzlaşması. Normal seans son işlemi 4.079,3, akşam kapanışı 4.092. Yani sayfa uzlaşmayı kapanış olarak gösteriyor.
- **Hacim** 21,02 K = normal seans 18.465 + aynı gün akşamı 2.555. Yani TV günlük çubuğu, akşamı **aynı takvim gününe** yazıyor (BIST'in takas mantığının tersine).
- Ayar kapalıyken günlük kapanış, akşamın son işlemi olur (23:00 TSİ). Bu, uzlaşmadan medyan 30,8 bps sapıyor (§5.1). Bunu doğrudan TV verisiyle **doğrulayamadım**, çıkarımdır.
- Sayfada veri sağlayıcı "ICE Data Services" ve açık pozisyon 82,62 K yazıyor.
- **Roll:** TV yardım sayfasına göre sürekli seri, "sonraki kontratın günlük hacmi mevcut kontratı aştığında" geçiyor. Kural sembol bazında, istatistiksel ortalamalarla belirleniyor ve tüm geçmişe uygulanıyor. GC örneğinde vadeden ≈6 iş günü önce geçiyor. Geri ayarlama isteğe bağlı (B-ADJ düğmesi / "Adjust for contract changes", 13.03.2024 notu).
  - VİOP ons altında hacim çok geç devrediyor: 2017–2026 vadelerinde sonraki vadenin hacmi ön vadeyi medyan **0 iş günü** önce (yani vade gününde) geçiyor. 2024+ için "ilk geçiş" medyanı 1 iş günü. Panel AP kuralı medyan 1–2 iş günü (`hacim_devri.csv`).
  - Bu yüzden XAUUSD1! büyük olasılıkla vade gününe kadar ön vadede kalıyor. Vade günü uzlaşması LBMA PM ile belirleniyor. Geri ayarlama kapalıysa roll günü 34–80 USD'lik takvim farkı kadar sıçrama oluyor.
  - BIST:XAUUSD1! için TV'nin kullandığı tam kural **bulunamadı**.
- **Gecikme:** TV sayfasında BIST vadelileri için gecikme süresi yazmıyor. **Bulunamadı.**
- **Matriks / İdeal:** Günlük çubuk konvansiyonu (uzlaşma mı son mu, akşam hangi güne yazılıyor) için birincil kaynak **bulunamadı** (arama kotası yok).

**Kullanıcının kendi kontrolü (adım adım):**
1. TV'de BIST:XAUUSD1! günlük grafiğini açın. Ayarlar → Sembol → "Use settlement as close on daily interval" kutusuna (ya da alttaki SET düğmesine) bakın.
2. Son bir günün kapanışını üç fiyatla karşılaştırın: borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv içindeki "UZLASMA FIYATI" ve "KAPANIS FIYATI", ve viop_as_bul_YYYYMMDD.csv içindeki "KAPANIS FIYATI". Ayarı açıp kapatarak hangisine eşit olduğunu görün.
3. Aynı günün TV hacmini ana bülten "ISLEM MIKTARI" + aynı tarihli akşam bülteni ile karşılaştırın. Bu, akşamın hangi güne yazıldığını gösterir.
4. Vade haftasında XAUUSD1! ile XAUUSDZ2026 ve XAUUSDG2027 grafiklerini üst üste koyun. Serinin hangi gün geçtiğini ve B-ADJ açıkken sıçramanın kalkıp kalkmadığını görün.
5. Gecikme için sembol adının yanındaki "D" (delayed) işaretine ya da TV hesap sayfasındaki borsa veri aboneliklerine bakın. Normal seans bitimi (18:10:00) ile çubuğun son güncellenme saatini karşılaştırın.
6. Sinyal ve getiri hesabında TV verisi yerine BIST bülteninin UZLAŞMA alanını kullanın. Gün içi spot karşılaştırması için 15:00–15:10 UTC'yi (13.02.2023 öncesinde 15:05–15:15 UTC) kullanın.

---

## 4. Uygulanabilir fiyat

### 4.1 Uzlaşmadan emir yok

- Prosedür md. 22'deki emir yöntemleri Limit, Piyasa ve Piyasadan Limite. Geçerlilik süreleri Gün, İptale Kadar Geçerli, Tarihli, Gerçekleşmezse İptal Et ve Kalanı İptal Et. Bunlara şarta bağlı emirler ekleniyor.
- "Uzlaşma fiyatından işlem" (TAS) ya da "kapanıştan" (MOC) emir türü **yok**.
- Akşam seansında piyasa emri, piyasadan limite emri, iptale kadar geçerli ve tarihli emir, ayrıca vadeler arası strateji emri kullanılamıyor (Prosedür md. 26, Ek-3).

### 4.2 Perakende yatırımcı uzlaşmayı nasıl yakalar?

- Uzlaşma penceresi 18:00:00–18:10:00 TSİ. Emri bu pencereye eşit zaman aralıklı dilimlere bölmek yeterli (TWAP).
- Spot dakika verisiyle vekil ölçüm, 2023-02-13 → 2026-11-06, 318 gün, |fiyat − pencere VWAP'ı|:

| Yöntem | Medyan bps | p90 bps |
|---|---|---|
| Pencerenin son anında tek emir (≈ KAPANIŞ) | 4,78 | 13,39 |
| 18:00:00'de tek emir | 5,40 | 19,00 |
| 2 dilim | 2,18 | 6,26 |
| 5 dilim (her 2 dk) | **0,58** | 1,81 |
| 10 dilim (her dk) | **0,27** | 1,19 |

- Vekilin geçerliliği: spot üzerindeki "son an − VWAP" sapması (4,78 / 13,39) gerçek VİOP |KAPANIŞ − UZLAŞMA| dağılımına (2026: 4,54 / 12,99) çok yakın.
- Dilim başına ayrıca yarım spread ödenir (§4.3). 1–4 sözleşmelik bir pozisyon tam bölünemiyor. Bu durumda dilim sayısı sözleşme sayısıyla sınırlı kalıyor.
- Pratik reçete: sinyali 17:58–17:59 TSİ'de hesaplayın (15:00 UTC spotu 18:00 TSİ'de oluşuyor; 17:59'daki fiyatla yaklaşık hesaplanabilir). 18:00–18:09 arasında her 1–2 dakikada bir, en iyi alış/satışa limit emir gönderin. Son dilimi 18:09:30'dan önce girin.

### 4.3 Piyasa yapıcı yükümlülükleri (F_XAUUSD, A Grubu)

| Seans | Vadeye <30 gün | <60 | <90 | ≥90 | Asgari emir | Piyasada bulunma | Sorumlu vadeler |
|---|---|---|---|---|---|---|---|
| Normal (Ek-10, rev. 69) | **2,80 USD** (≈6,9 bps @4.079) | 3,20 | 3,60 | 4,00 (≈9,8 bps) | 20 sözleşme | Açık sürenin %70'i | En yakın 2 vade |
| Akşam (Ek-12, rev. 69) | **5,60 USD** (≈13,7 bps) | 6,40 | 7,20 | 8,00 (≈19,6 bps) | 20 | %70 | En yakın 2 vade |

- Geçmiş değerler: rev. 67'ye (28.11.2025, duyuru 41504) kadar normal 1,30/1,50/1,70/2,00 ve akşam 2,60/3,00/3,40/4,00 USD. Rev. 67 ile 1,80/2,00/2,30/2,50 ve 3,60/4,00/4,60/5,00 oldu. Rev. 69 (23.02.2026, duyuru 44576) ile bugünkü değerlere çıktı.
- Normal seans ve akşam için ayrı program ve ayrı gelir paylaşımı var (Prosedür 45.1).
- Bunlar **üst sınır**. Gerçekleşen tipik spread için birincil veri **bulunamadı**. Azami spread ile işleme giren perakende emir taraf başı en çok ≈3,4 bps (normal) ve ≈6,9 bps (akşam) yarım spread öder.

### 4.4 Kayma vekili: son işlem − uzlaşma

| Yıl | n | Medyan |K−U| bps | p90 | Maks |
|---|---|---|---|---|
| 2017 | 208 | 2,75 | 7,06 | 43,26 |
| 2018 | 251 | 2,03 | 6,42 | 41,42 |
| 2019 | 249 | 2,03 | 6,60 | 17,34 |
| 2020 | 252 | 3,86 | 10,50 | 35,92 |
| 2021 | 249 | 2,96 | 7,31 | 39,33 |
| 2022 | 252 | 3,58 | 9,49 | 52,87 |
| 2023 | 253 | 3,08 | 9,25 | 24,75 |
| 2024 | 250 | 3,44 | 10,28 | 56,16 |
| 2025 | 251 | 3,33 | 10,55 | 26,87 |
| **2026** | **212** | **4,54** | **12,99** | **58,66 (28.01.2026)** |

- 2026 ayrıntısı: ortalama 6,64, p75 9,26, p95 20,55 bps. İşaretli ortalama −0,01 bps, yani yönsüz. Ön vade = günün en yüksek hacimli kontratı.
- Sağlamlık testinde "uzlaşma + kayma" senaryosu için taraf başı 4,5 bps (gidiş-dönüş +9 bps) ekledim.

### 4.5 Aracı kurum komisyonları (2026)

| Kurum | VİOP komisyonu | Kaynak / tarih | Gidiş-dönüş (komisyon×2×1,05 + 2×0,4 bps borsa+takas) |
|---|---|---|---|
| Ata Yatırım | %0,009 (onbinde 0,9), vergiler hariç | atayatirim.com.tr/sss/ucret-ve-tarifeler, "2026 yılı" | ≈2,7 bps |
| Strateji Menkul | İnternet binde 0,20, temsilci binde 0,30 | 04.12.2025 bilgilendirme PDF'i | ≈5,0 bps (internet) |
| İş Bankası (İşCep) | Günlük ort. hacme göre onbinde 10 / 8 / 7 / 6 / 5 (0–80 bin, …, >2 milyon TL) + BSMV | isbank.com.tr/viop, 01.01.2024'ten geçerli | ≈21,8 bps (ilk kademe) → ≈11,3 bps (son kademe) |
| Info Yatırım | Binde 2 + BSMV (azami; kanala göre değişir) | infoyatirim.com/hakkimizda/ucretler, 12.01.2026 | ≈42,8 bps |
| GCM Yatırım | Komisyon oranı sayfada **bulunamadı**. Borsa payı 0,00003, takas payı 0,00001 (pay endeksi hariç vadeli) aynen yansıtılıyor; günlük asgari 5 TL | gcmyatirim.com.tr ücret ve komisyonlar, Şubat 2025 | — |
| Midas | VİOP tablosu %0,05 / %0,02 / %0,01 (0–10 / 10–100 / >100 milyon TL). Ons altın vadelisinin Midas'ta işlem gördüğü **teyit edilemedi** (kardeş rapor m1: "yok") | getmidas.com/ucretler | (≈11,3 bps, eğer varsa) |

- Spread maliyeti bunlara eklenir. Pazarlıklı komisyonla toplam ≈5 bps varsayımı (panel `COST_BPS`) yalnız Ata ve Strateji internet düzeyinde gerçekçi. Varsayılan banka tarifesiyle 22–25 bps, Info azami tarifesiyle ≈43 bps.

---

## 5. Sağlamlık: aynı sinyaller, farklı giriş/çıkış fiyatı

**Kurulum.**
- Sinyaller değişmedi: hepsi gün t 15:00 UTC (a6'da Asya kapanışları, a4'te t-1 ABD kapanışı) bilgisiyle kuruldu.
- Aktif kontrat panel `v_code` (önceki gün en büyük AP). Getiri hep aynı kontrat içinde hesaplandı.
- Üç uygulama fiyatı:
  - **U** uzlaşma → uzlaşma (temel).
  - **K** bülten KAPANIŞ → KAPANIŞ (normal seans son işlemi).
  - **A** akşam kapanışı → akşam kapanışı (23:00 TSİ = 20:00 UTC). Akşam bülteni yoksa (2020-09 öncesi, yarım gün, yıl sonu) vekil kullandım: 20:00 UTC spot × exp(ln uzlaşma_t − ln spot15_t).
- Vekil kalitesi: gerçek akşam kapanışı ile vekil arasındaki fark medyan +0,95 bps, |fark| medyanı 8,3 bps, n = 1.513. Getiri korelasyonu 0,982.
- Yarım günlerde pozisyon sıfır.
- Kademeli h günlük tutuş (`lib_altin.backtest`). Maliyet gidiş-dönüş 5, 22 ve 25 bps; U için ayrıca 5+9 = 14 bps (kayma vekili).
- Temel sonuçlar önceki raporlarla birebir: LOWMOM h1 0,986, h5 0,955; a6 OOS 1,26; a3 NFP h3 OOS 1,07.
- U ile K günlük getirileri arasında korelasyon 0,9958, |fark| medyanı 4,6 bps. U ile A arasında korelasyon 0,825, |fark| medyanı 30,8 bps.

**Drift çıkarılmış net Sharpe (t) — tam dönem 2017-03 → 2026-11:**

| Aday | h | U 5 | K 5 | A 5 | U+kayma 14 | U 22 | K 22 | A 22 | U 25 | K 25 | A 25 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A1-LOWMOM | 1 | 0,98 (3,0) | 0,96 (3,0) | 1,11 (3,4) | 0,70 (2,2) | 0,45 (1,4) | 0,43 (1,3) | 0,60 (1,8) | 0,36 (1,1) | 0,34 (1,0) | 0,51 (1,6) |
| A1-LOWMOM | 5 | 0,96 (3,0) | 0,96 (3,0) | 1,05 (3,2) | 0,76 (2,4) | 0,59 (1,8) | 0,60 (1,9) | 0,70 (2,2) | 0,53 (1,6) | 0,54 (1,7) | 0,64 (2,0) |
| a4 C1 GDXJ/GLD artığı | 3 | 0,56 (1,7) | 0,56 (1,7) | 0,61 (1,9) | 0,16 (0,5) | −0,19 | −0,19 | −0,13 | −0,32 | −0,33 | −0,26 |
| a3 NFP işaret | 1 | 0,48 (1,5) | 0,39 (1,2) | 0,59 (1,8) | 0,15 | −0,14 | −0,23 | 0,03 | −0,25 | −0,34 | −0,07 |
| a3 NFP işaret | 3 | 0,68 (2,1) | 0,66 (2,1) | 0,62 (1,9) | 0,48 (1,5) | 0,30 | 0,28 | 0,28 | 0,24 | 0,22 | 0,22 |
| a5 C1 makro artığı | 3 | 0,48 (1,5) | 0,47 (1,5) | 0,31 (0,9) | 0,25 | 0,05 | 0,04 | −0,11 | −0,03 | −0,04 | −0,18 |
| a6 Çin altın hisseleri artığı | 5 | 0,74 (2,3) | 0,72 (2,2) | 0,83 (2,6) | 0,42 (1,3) | 0,15 | 0,12 | 0,27 | 0,04 | 0,02 | 0,17 |
| a6 Çin artık 5g toplamı | 1 | 0,67 (2,1) | 0,63 (2,0) | 0,80 (2,5) | 0,35 | 0,08 | 0,05 | 0,24 | −0,02 | −0,05 | 0,14 |

**OOS 2022-01 → 2026-11:**

| Aday | h | U 5 | K 5 | A 5 | U+kayma 14 | U 22 | K 22 | A 22 | U 25 | K 25 | A 25 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A1-LOWMOM | 1 | 1,29 (2,8) | 1,29 (2,8) | 1,56 (3,4) | 1,06 (2,3) | 0,86 (1,9) | 0,86 (1,9) | 1,14 (2,5) | 0,78 (1,7) | 0,79 (1,7) | 1,07 (2,3) |
| A1-LOWMOM | 5 | 1,63 (3,6) | 1,65 (3,6) | 1,76 (3,9) | 1,51 (3,3) | 1,40 (3,1) | 1,41 (3,1) | 1,52 (3,3) | 1,36 (3,0) | 1,37 (3,0) | 1,48 (3,3) |
| a4 C1 | 3 | 0,76 (1,7) | 0,75 (1,6) | 0,82 (1,8) | 0,42 | 0,11 | 0,09 | 0,17 | −0,01 | −0,02 | 0,05 |
| a3 NFP | 1 | 0,90 (2,0) | 0,81 (1,8) | 0,82 (1,8) | 0,60 | 0,32 | 0,23 | 0,32 | 0,22 | 0,12 | 0,23 |
| a3 NFP | 3 | 1,07 (2,4) | 1,07 (2,4) | 0,86 (1,9) | 0,89 (2,0) | 0,73 (1,6) | 0,73 (1,6) | 0,55 (1,2) | 0,67 (1,5) | 0,66 (1,5) | 0,50 (1,1) |
| a5 C1 | 3 | 0,57 (1,2) | 0,57 (1,3) | 0,38 (0,8) | 0,30 | 0,06 | 0,06 | −0,10 | −0,03 | −0,03 | −0,19 |
| a6 Çin bileşiği | 5 | 1,26 (2,8) | 1,25 (2,7) | 1,40 (3,1) | 1,00 (2,2) | 0,76 (1,7) | 0,75 (1,6) | 0,92 (2,0) | 0,68 (1,5) | 0,66 (1,4) | 0,84 (1,8) |
| a6 sum5 | 1 | 0,93 (2,0) | 0,90 (2,0) | 1,20 (2,6) | 0,66 | 0,41 | 0,39 | 0,70 | 0,32 | 0,29 | 0,61 |

**2020-09-21 → 2026-11, yalnız gerçek akşam fiyatı olan dönem (A sütunu %97 gerçek):**
- LOWMOM h1: U 1,00 / K 0,99 / A 1,23.
- LOWMOM h5: 1,33 / 1,34 / 1,43.
- a3 NFP h3: 0,83 / 0,83 / 0,62.
- a5 C1: 0,48 / 0,48 / 0,31.
- a6 bileşik: 0,99 / 0,98 / 1,13.
- Hepsi 5 bps'te. Tam tablo `saglamlik_tablo.md` ve `saglamlik_tum.csv`'de.

**Yorum.**
- **K ≈ U.** Normal seans son işlemiyle çalışmak sonuçları değiştirmiyor (en büyük fark a3 NFP h1'de: 0,48 → 0,39). Uzlaşmayı kaçıran ama 18:10'dan önce işlem yapan perakende yatırımcı aynı kenarı alıyor.
- **A neden bazılarında iyileşiyor?** Gün t'nin 15:10 → 20:00 UTC dilimi (uzlaşmadan akşam kapanışına) sinyal yönünde ortalama şöyle:
  - LOWMOM −0,93 bps (t −0,86); a6 bileşik −1,90 bps (t −2,12); a4 −0,51 (t −0,42); NFP −0,91 (t −0,25).
  - a5 C1 +4,49 bps (t 1,40); sum5 +0,31.
  - Akşamda giren yatırımcı a6 ve LOWMOM'da bu küçük ters hareketten kaçıyor. a5 C1'de ise ABD öğleden sonrasındaki devam hareketini kaçırıyor. Sharpe farkları 0,1–0,2 düzeyinde. 9,7 yıllık örneklemde Sharpe'ın standart hatası ≈0,32 olduğundan bu farklar istatistiksel olarak ayırt edilemez.
- **Maliyet her şeyi belirliyor.** 22–25 bps'te yalnız LOWMOM h5'in tam dönem t'si ≥1,6 ve OOS t'si ≥3,0. LOWMOM h1'in yıllık devri yüksek ve 25 bps'te tam dönem 0,34–0,51. a4 C1 (yılda ≈143 işlem) ve a5 C1 22 bps'te sıfırlanıyor.
- **Önceki uyarılar geçerli.** LOWMOM 2026'da pasif (rv20 ≈ %21, eşik ≈ %11,7). a6'nın IS'i boş. a3 NFP'nin IS'i zayıf. Bunlar bu testten bağımsız.

---

## 6. DATA_README için düzeltme listesi

1. "VİOP kıymetli maden normal seansı 09:30–18:15 TSİ (06:30–15:15 UTC)" → **10.02.2023'e kadar** 09:30–18:15 TSİ. **13.02.2023'ten beri** 09:30–18:10 TSİ (06:30–15:10 UTC). 23.09.2022'den beri önünde 09:20–09:30 açılış seansı var. Yarım gün 09:30–12:45 → 13.02.2023'ten beri 09:20–12:40.
2. "Günlük uzlaşma ≈ 15:05–15:15 UTC VWAP (İşbank 2024, BIST duyurusu 30572)" → 2017-03 → 2023-02-10 arası 15:05–15:15 UTC. 2023-02-13'ten beri **15:00–15:10 UTC**. Yarım günde 09:35–09:45 → 09:30–09:40 UTC. Kaynak: Prosedür rev. 54 karşılaştırma tablosu (duyuru 15626, 06.03.2023), ampirik kırılma 10/13.02.2023. İşbank dokümanı bu konuda eskimiş. 30572 bakır duyurusu, saatle ilgisi yok.
3. "uzlaşma–spot farkının sapması 15:10 UTC'de minimum (MAD 3,7)" → dönemlere ayrılmalı. Ardışık gün yöntemiyle en iyi pencere 2023 öncesinde 15:05–15:15 UTC (MAD 3,99), sonrasında 15:01–15:11 UTC (MAD 4,99).
4. "Bülten KAPANIŞ FİYATI (son işlem) ≈ 15:15–15:20 UTC" → son işlem 2023-02-10'a kadar ≈15:15 UTC, 2023-02-13'ten beri **≈15:10 UTC**.
5. "AÇILIŞ FİYATI büyük olasılıkla akşam seansının ilk işlemidir" → **yanlış.** 23.09.2022'den beri açılış seansı tek fiyatı (os_price ile %100 eşit, 1.601 satır). Öncesinde normal seansın ilk işlemi (09:30 TSİ). Akşam açılışıyla eşitlik %0,5.
6. "18.09.2020'den beri VİOP gün t'nin işlemleri önceki akşam başlar" → takas açısından doğru (md. 9.5). Ama **ana bülten t yalnız normal seansı içerir**: OHLC, VWAP, hacim ve işlem sayısı. Önceki akşamın aralığı ana bülten aralığının dışına %58 (2020-09 → 2022-09) / %71 (2022-09+) günde taşıyor. Akşam için `viop_as_bul_D` (D = akşamın takvim günü) ayrıca okunmalı ve takası next_td(D)'ye yazılmalı.
7. "Karar anı = gün t 15:00 UTC; giriş = gün t uzlaşması" → ileriye bakma yok. Ama 13.02.2023'ten beri pencere 15:00:00'da başlıyor, tampon 0 dakika (öncesinde 5 dk). Uygulanabilirlik için dilimli emir ya da KAPANIŞ/akşam fiyatı gerekir (§4.2, §5). ABD verisi 15:00 UTC'de (kışın 10:00 ET) çıkan günlerde uzlaşma bu verinin ilk 10 dakikalık tepkisini içeriyor.
8. a1 `mt` bilgi zamanı açıklaması "gün t yüksek/düşük (önceki akşam seansı dahil)" → "yalnız normal seans (09:20/09:30–18:10/18:15 TSİ)". `loc_v` = uzlaşmanın normal seans aralığındaki yeri.
9. Akşam seansı olmayan günler listeye eklenmeli: yarım günler, yılın son işlem günü (2020/79), ve nedeni bilinmeyen 04.08.2023 ile 29.11.2024 (akşam bülteni 404).
10. Maliyet: `COST_BPS = 5` yalnız pazarlıklı komisyon (Ata ≈2,7 bps, Strateji internet ≈5,0 bps + spread) için gerçekçi. Varsayılan banka tarifesi ≈22 bps, Info azami ≈43 bps. Stres testi 10 bps yerine **22–25 bps** olmalı. Kayma vekili: 2026 |KAPANIŞ − UZLAŞMA| medyan 4,54, p90 12,99, maks 58,66 bps.
11. TradingView notu eklenmeli: günlük kapanış = uzlaşma ("settlement as close" açıkken). Günlük hacim = normal + aynı takvim günü akşamı. Sürekli seri hacim kuralıyla, VİOP altında pratikte vade gününe yakın geçiyor; geri ayarlama isteğe bağlı.
12. Piyasa yapıcı azami spread (rev. 69): normal 2,80–4,00 USD, akşam 5,60–8,00 USD, asgari 20 sözleşme, %70 bulunma. Yalnız üst sınır; gerçekleşen spread bilinmiyor.

---

## 7. Bulunamayanlar

- 15151 sayılı BIST duyurusunun (14.02.2023) metni ve kesin yürürlük tarihi (PDF 404).
- TradingView'in BIST:XAUUSD1! için kullandığı tam roll günü kuralı, BIST vadelilerinde veri gecikmesi süresi ve "settlement as close" ayarının varsayılan değeri. Varsayılan için 13.03.2024 notu yalnız seçeneğin varlığını söylüyor; sembol sayfası uzlaşmayı gösteriyor.
- Matriks ve İdeal'in VİOP günlük çubuk konvansiyonu.
- F_XAUUSD'de gerçekleşen tipik alış-satış farkı (yalnız piyasa yapıcı üst sınırları var).
- 04.08.2023 ve 29.11.2024'te akşam seansının neden yapılmadığı.
- GCM'nin VİOP komisyon oranı; Midas'ta ons altın vadelisinin işlem görüp görmediği.

---

## 8. Kaynaklar

- Borsa İstanbul VİOP Prosedürü rev. 70 (01.07.2026): https://borsaistanbul.com/files/borsa-istanbul-as-vadeli-islem-ve-opsiyon-piyasasi-proseduru.pdf (md. 7, 9.5, 22–23, 26, 45.1, Ek-1 R, Ek-3, Ek-10, Ek-12)
- VİOP Prosedürü Revizyon Karşılaştırma Tablosu (01.07.2026, 306 s.): https://borsaistanbul.com/files/vadeli-islem-ve-opsiyon-piyasasi-proseduru-revizyon-karsilastirma-tablosu.pdf (2017/44, 2020/57, 2020/79, rev. 51, 54, 63, 67, 69)
- BIST prosedürler sayfası: https://borsaistanbul.com/kurumsal/mevzuat/prosedurler
- BIST duyuru 11326 (21.09.2022, açılış seansı, 23.09.2022): https://borsaistanbul.com/files/duyuru-11326-TR.pdf
- BIST duyuru 15626 (06.03.2023, rev. 54, 10.03.2023; 15151'e atıf): https://borsaistanbul.com/files/duyuru-15626-tr.pdf
- BIST duyuru 30572 (19.11.2024, bakır): https://borsaistanbul.com/files/duyuru-30572-TR.pdf
- BIST günlük bülten ve akşam bülteni: https://www.borsaistanbul.com/data/vadeli/viop_20261106.csv ; https://www.borsaistanbul.com/data/vadeli/viop_as_bul_20261106.csv
- İşCep VİOP eğitim dokümanı (İş Bankası, yerel kopya `pdfs/isbank.txt`): kıymetli madenler "09:30-18:15", pay "09:30-18:10"
- TradingView BIST:XAUUSD1!: https://www.tradingview.com/symbols/BIST-XAUUSD1!/
- TradingView blog (13.03.2024) BIST vadelilerinde uzlaşma, geri ayarlama, AP: https://www.tradingview.com/blog/en/improved-bist-futures-settlement-price-back-adjustment-open-interest-43494
- TradingView sürekli vadeli geçiş kuralı: https://www.tradingview.com/support/solutions/43000691027-how-is-the-switching-date-of-contracts-determined-in-continuous-futures/
- Ata Yatırım ücret ve tarifeler: https://atayatirim.com.tr/sss/ucret-ve-tarifeler
- Strateji Menkul (04.12.2025): https://strateji.com.tr/wp-content/uploads/2025/12/Ucret-Masraf-ve-Komisyon-Bilgilendirilmesi-2025-12-04.pdf
- İş Bankası VİOP: https://www.isbank.com.tr/viop
- Info Yatırım ücretler (12.01.2026): https://infoyatirim.com/hakkimizda/ucretler
- GCM Yatırım ücret ve komisyonlar: https://www.gcmyatirim.com.tr/sirket-profili/yasal-bildirimler/ucret-ve-komisyonlar
- Midas ücretler: https://www.getmidas.com/ucretler/
- Dukascopy XAUUSD dakikalık BID mumları: https://datafeed.dukascopy.com/datafeed/XAUUSD/YYYY/MM/DD/BID_candles_min_1.bi5
