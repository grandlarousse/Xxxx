# Olay çalışmaları: geri alım ve içeriden alım, yabancı akımı, faiz döngüsü ve bankalar (06.11.2026)

Ajan anahtarı: `akis_rejim`. Kod ve tam tablolar: `hesaplar/olay_akis_rejim/` (`cikti/A_tablolar.md`, `A_kontrol.md`, `A_dalga.md`, `B_tablolar.md`, `C_tablolar.md`). Ham veri repoda yok; önbellek: `scratchpad/data/akis_rejim/`.

## 0. Net hüküm

| Çalışma | Örneklem | Ana sayı (dürüst ölçü) | Hüküm |
|---|---|---|---|
| A1 Geri alım, yeni dalga (GA_YENI) | 674 olay, 303 hisse, 2018-2026 | Kontrollü AR: 5g +%0,9 (t 2,0); 20g +%1,4 (t 1,7, medyan −%0,6); 60g +%4,0 (t 1,3, medyan −%3,0, isabet %45) | **Kenar yok** (60g). Ham BHAR'daki +%8,9, eşit ağırlıklı küçük hisse primi ve çarpıklıktan geliyor. 2024-26'da 20g +%2,6 (t 2,6), ama en iyi %5 çıkarılınca +%0,1 |
| A2 Geri alım programı açıklaması (GA_PROG) | 299 olay; VİOP'lu 41 | Hepsi: 60g +%6,1 (t 1,3, medyan −%2,6). **VİOP'lu hisseler: 5g +%2,3 (t 2,9), 60g +%6,4 (t 2,0, medyan +%8,4, isabet %66)** | Tüm örneklemde kenar yok. VİOP'lu altkümede **zayıf aday** (n=41, 8'i BIMAS; ~126 hücreden biri, çoklu test riski) |
| A3 İçeriden alım (özeti açıkça "alım") | 242 olay; küme alımı 82 | Kontrollü 60g −%3,2 (t −1,7, medyan −%6,2); küme 60g ~0 | **Kenar yok**, işaret ters |
| A4 Piyasa çapında geri alım dalgası | 5 tamamlanmış dalga | 13 hafta XU100 ort. +%15, 4/5 pozitif | Anlatı için ilginç, istatistik yok (n=5) |
| B Yabancı haftalık hisse akımı (TCMB) | 1.086 hafta, 2006-2026 | Akım getiriyi **izliyor** (aynı hafta t 10,7; önceki hafta t 9,4). İleri getiri: 8 hafta z t≈2,5 tüm dönem, ama 2021-26 ve 2024-26'da anlamsız; 1 haftalık kural farkı t≈1 | **Ticari kenar yok.** Gecikmeyle yayımlanan bir takip göstergesi |
| C1 Faiz indirimleri ve bankalar | 37 indirim, 6 indirim döngüsü | İndirimden sonraki 63g XBANK/XU100: ort. −%5,9 (isabet %24). **Döngü düzeyinde 6/6 negatif, ort. −%6,3, t −4,2.** Karardan önceki 63g: +%3,2 | **En sağlam bulgu:** bankalar indirimden önce yükseliyor, sonra geride kalıyor ("söylentide al, kararda sat") |
| C2 İlk artırım (dönüş) | 5 olay | 63g XBANK/XU100 +%7,5, 5/5 pozitif, bootstrap p 0,05 | Yönü tutarlı, n çok küçük |
| C3 2Y DİBS getirisi öncü mü? | 2010-2026 günlük, kendi kurduğum 2Y | Geçmiş 60g ΔY2 +100bp → sonraki 63g XBANK/XU100 +%0,85 (örtüşmesiz t 2,4-5,2). Eşzamanlı ilişki ters (−0,43). Aylık kural: ayda ~+%0,5-1,6, t 0,7-2,2 (başlangıç günüyle değişiyor) | **Karşıt yönde öncü.** Yükselen 2Y'den sonra bankalar toparlanıyor. Kural olarak zayıf-orta |
| C4 İhracatçı ve yurt içi sepetleri | aynı olaylar | Dönüşlerde desen yok. Güvercin sürprizden sonra yurt içi öne geçiyor (63g −%4,4, p 0,01) | Kullanılabilir değil |

**Pazartesi 9.11.2026 için:**
1. **10 Aralık PPK'da beklenen −100bp (%35) bir "döngü içi, sürprizsiz indirim".** Tarihsel karşılığı (n=24): karardan sonraki 21/42/63 günde XBANK/XU100 sırasıyla −%2,3, −%4,8 ve −%6,6 (isabet %33, %17, %17). Bankalar 63 günde XU100'e karşı +%26 koştu (06.08'den 05.11'e, 79→100). Veri, banka göreli uzun pozisyonunu (XBANK-XU100) **10.12 sonrasına taşımamayı** destekliyor. Karar öncesi dönem için yalnız zayıf bir pozitif var (karar öncesi 63g ort. +%3,2, döngü düzeyinde 4/6). Bugün yeni banka-uzun pozisyonu için destek yok.
2. 2Y sinyali şu an nötr. ΔY2(60g) −81bp, eşik ±100bp. Y2 ≈ %40,0, AOFM %36 (+418bp).
3. Yabancı 5 haftadır net satıcı (seri −5, z4 −0,96). Tarihte 5. hafta epizotlarından sonra 8 haftada XU100 +%9,3 (kosulsuz +%3,2, t 1,4, n=21). Karşıt eğilim var ama işlem kuralı değil.
4. GARAN 04.11'de geri alım programı başlattı (KAP 03.11 19:54). Giriş günü (04.11) hisse +%6,8, XU100 +%4,1. SAHOL (16.10), GUBRF (26.10), TCELL (26.10), ODAS (26.10) de VİOP'lu yeni geri alım. A2'deki zayıf adaya göre bunlar izleme listesi, sinyal değil.

## 1. Veri ve yöntem

- **Fiyat:** İş Yatırım HisseTekil düzeltilmiş kapanış, gün içi yüksek ve düşük (kardeş ajan `bist_test` önbelleği; 496 bugün işlem gören hisse). Eksik 196 kodu (kote olmaktan çıkmış ya da XUTUM dışı) aynı uçtan kendim çektim: varsayılan başlıklar, sıralı, 0,7 sn bekleme. 111'i veri döndürdü, 85'i boş döndü; bunlar örneklem dışında. Endeksler ChartData IndexHistoricalAll'dan. **XBANK'ta 02.07.2010-31.12.2010 arası 1/100 ölçek hatası vardı, ×100 ile düzelttim.** 06.11 gün içi (kısmi) kapanış dışarıda bırakıldı.
- **Düzeltme doğrulaması:** Bilinen bedelsiz hak kullanım günlerinde ham ve düzeltilmiş getiri: SASA 23.05.2023 (%130) −%52,8 / +%8,6; ASELS 25.08.2023 (%100) −%48,9 / +%2,1; SASA 12.08.2024 (%700) −%87,4 / +%0,9; ADEL 04.09.2024 (%1000) −%90,2 / +%7,5; EREGL 27.11.2024 −%50,7 / −%1,4; FROTO 07.05.2025 (%900) −%90,1 / −%0,6; KORDS 14.09.2026 (%1800) −%94,8 / −%1,6. Kardeş ajanın 228 olaylık kontrolünde düzeltilmiş |getiri| > %20 olan olay yok. Olay pencerelerinde |günlük getiri| > %40 olan olay da yok (0/6.365).
- **Olay tarihleri:** KAP'ın kendi arama API'si (`api/disclosure/members/byCriteria`), konu bazında aylık sorgular, varsayılan başlıklar, 1,5 sn bekleme. "Payların Geri Alınmasına İlişkin Bildirim" için 11.493, "Pay Alım Satım Bildirimi" için 18.678 bildirim (2018-01 ile 2026-11 arası). Üç kez 429 alındı, beklenip tekrarlandı, eksik ay yok. TCMB: EVDS3 web arayüzünün herkese açık sorgu ucu (anahtar ve giriş yok; captcha yalnızca üyelikte), PPK sayfaları ve 1 hafta repo tablosu.
- **Giriş zamanı:** KAP yayını 17:00'den önce ve işlem günündeyse aynı gün kapanışında, aksi halde ertesi işlem günü kapanışında. PPK kararları 14:00'te açıklandığı için karar günü kapanışında giriş; akşam ve olağanüstü kararlarda ertesi gün. TCMB akım verisi Perşembe yayın günü kapanışında; Perşembe tatilse sonraki işlem günü.
- **Getiri ölçüleri:** BHAR (hisse alıp tutma eksi XU100 alıp tutma) ve piyasa modeli CAR (β [−250, −21]). Ana ölçü **eşleştirilmiş kontrol**: olay AR'sinden, aynı gün aynı [olay öncesi 20 günlük AR beşlisi × 60 günlük medyan TL hacim üçlüsü] kovasındaki diğer hisselerin ortalama AR'si çıkarılır. t'ler giriş haftasına göre kümelenmiş. Tavan kilidi: giriş günü getirisi ≥ %9,5 ve kapanış gün içi en yüksekte. Bu olaylar ana tablolardan çıkarıldı. Maliyet: 25bp gidiş-dönüş (A), 30bp (C kuralı).
- **Hayatta kalma yanlılığı:** Kontrol paneli yalnızca bugün işlem gören hisselerden oluşuyor. Olay hisselerinin bir kısmı da öyle (kote olmaktan çıkmış kodların bir kısmı İş Yatırım'da boş döndü). Bu durum kontrolü ve olayları aynı yönde etkiler. Eşleştirilmiş fark daha az etkilenir.

## 2. (A) Geri alım ve içeriden alım

### 2.1 Örneklem ve tanımlar (önceden belirlendi)

| Olay | Tanım | n (fiyatlı, tavan hariç) | Hisse | VİOP'lu |
|---|---|---|---|---|
| GA_YENI | Hissede 60 işlem günü sessizlikten sonra ilk geri alım bildirimi (program başlangıcı veya ilk alım) | 674 | 303 | 97 |
| GA_PROG | Özette program, karar, başlatma veya yetki geçen bildirim (sonlanma ve süre dolması hariç), 60 gün sessizlik | 299 | 244 | 41 |
| GA_ISLEM | Gerçekleşen alım bildirimi, 20 gün sessizlik (alım koşusunun başı) | 861 | 286 | 126 |
| PAS_ALIS | "Pay Alım Satım Bildirimi" konusunda özeti açıkça "alım" olan bildirim (satış kelimesi yok), 20 gün sessizlik | 242 | 107 | 43 |
| PAS_ALIS_KUME | 20 işlem günü içinde aynı hissede ≥ 3 alım bildirimi | 82 | 51 | 24 |
| PAS_SATIS | Özeti açıkça "satım/satış" olan | 330 | 127 | 37 |
| PAS_HEPSI | Yönü bilinmeyen tüm içeriden işlem bildirimleri (kontrol) | 3.262 | 616 | 425 |

Not: İçeriden işlem bildirimlerinin %84'ünün özeti "Pay Alım Satım Bildirimi". Yön KAP'ta PDF ekte kalıyor (örnek: ENKAI 671636). KAP detay sayfaları kardeş ajanda 3 sn aralıkla bile 429 verdi, bu yüzden yön yalnızca özetten alındı. Özeti açıkça "alım" olanlar ağırlıkla **ana ortakların bağlı şirket alımları** (Şişecam→Soda/Trakya Cam, İş Bankası grubu→GYO'lar, Koza, İpek, Vertu, Derhl). Yönetim kurulu üyesi alımları daha az temsil ediliyor. Belgelenmiş ve sınırlı bir örneklem.

### 2.2 Ham BHAR neden yanıltıcı

| Olay | Önceki 20g AR | Gün 0 ham (XU100 düzeltmeli) | Ham AR 20g | Ham AR 60g (medyan) | Piyasa modeli 60g | Kontrol kovası 60g |
|---|---|---|---|---|---|---|
| GA_YENI | −%4,9 (t −4,6) | +%1,8 (+%1,0) | +%2,25 | +%8,9 (+%1,55) | +%1,3 | +%4,9 |
| GA_PROG | −%5,9 (t −3,3) | +%3,0 (+%1,9; isabet %71) | +%1,9 | +%9,4 (+%0,7) | +%1,4 | +%3,3 |
| **PAS_SATIS (içeriden SATIŞ)** | +%6,3 | −0,2 | +%1,8 | **+%6,65 (t 3,05; medyan −%2,7)** | −%1,9 | +%8,5 |

İçeriden satışlarda bile ham 60 günlük BHAR +%6,65 (t 3,05). Bu, 2018-2023'te eşit ağırlıklı küçük ve orta hisselerin XU100'ü geçmesinden ve sağa çarpık dağılımdan (p95 +%55-78) kaynaklanıyor. Kontrol kovasının kendisi 60 günde +%5-8 kazanıyor. Geri alımlar −%5-6'lık düşüşten sonra geliyor; kısa vadeli geri dönüşü de kontrol yakalıyor.

### 2.3 Kontrol düzeltmeli sonuçlar (tavan kilitli girişler hariç)

| Olay / evren / dönem | n | k5 % (t) | k20 % (t) | medyan20 | k60 % (t) | medyan60 | isabet60 |
|---|---|---|---|---|---|---|---|
| GA_YENI hepsi 2018-26 | 674 | +0,89 (2,0) | +1,37 (1,7) | −0,59 | +4,02 (1,3) | −3,03 | %45 |
| GA_YENI hepsi 2024-26 | 380 | +1,84 (3,65) | +2,55 (2,6) | +0,36 | +5,59 (1,8) | −0,62 | %50 |
| GA_YENI VİOP | 97 | +0,36 (0,6) | −0,61 (−0,6) | −0,60 | −1,06 (−0,5) | −2,15 | %49 |
| GA_PROG hepsi | 299 | +1,23 (1,9) | +1,59 (1,5) | +0,10 | +6,07 (1,3) | −2,57 | %46 |
| **GA_PROG VİOP 2018-26** | **41** | **+2,28 (2,9)** | +2,65 (1,8) | +2,10 | **+6,38 (2,0)** | **+8,38** | **%66** |
| GA_PROG VİOP 2024-26 | 19 | +2,57 (2,3) | +3,13 (1,5) | +0,46 | +6,90 (1,6) | +5,14 | %69 |
| GA_ISLEM hepsi | 861 | +0,18 (0,6) | +0,98 (1,5) | −0,71 | +1,02 (0,4) | −3,47 | %43 |
| GA_ISLEM VİOP | 126 | +0,32 (0,75) | −0,73 (−0,9) | −0,52 | −2,70 (−1,3) | −2,45 | %45 |
| PAS_ALIS hepsi | 242 | +0,36 (0,5) | −0,02 (0,0) | −1,80 | −3,15 (−1,7) | −6,15 | %35 |
| PAS_ALIS VİOP | 43 | −0,82 | +3,16 (1,1) | +0,02 | +0,04 (0,0) | −4,07 | %39 |
| PAS_ALIS_KUME hepsi | 82 | −1,47 (−1,5) | −1,98 (−1,2) | +0,12 | −0,08 (0,0) | −7,93 | %36 |
| PAS_SATIS hepsi | 330 | −0,54 | −0,43 | −2,85 | −1,87 (−0,8) | −5,64 | %39 |
| PAS_HEPSI (yönsüz) | 3.262 | −0,63 (−4,0) | −0,78 (−2,1) | −2,63 | −1,31 (−1,6) | −6,17 | %38 |

Yıllara göre GA_YENI k60 (ort., %): 2018 +3,7 · 2019 +0,5 · **2020 +23,3 (medyan −17,7)** · 2021 −2,1 · 2022 −3,5 · 2023 −1,0 · 2024 −0,3 · **2025 +11,3** · 2026 +2,0 (kısmi). k20: 2025 +3,9, 2026 +2,8 (medyan +2,3). Pozitif ortalamayı 2020 Mart ve 2025 Mart dalgalarındaki birkaç uç kazanan taşıyor. Medyanlar neredeyse her yıl negatif.

**VİOP'lu GA_PROG olay olay (60 günlük k'si olan 38 olay):** En büyük katkılar EKGYO 04.2025 (+%57), BIMAS 07.2026 (+%42), BIMAS 02.2023 (+%40), GUBRF 10.2024 (+%35), YKBNK 02.2023 (+%34) ve SASA 11.2021 (+%30). En büyük kayıplar SASA 04.2025 (−%54), TAVHL 03.2020 (−%41) ve THYAO 03.2020 (−%21). **BIMAS tek başına 8 olay** (ort. +%14). En büyük olay çıkarılınca ort. +%5,0, en büyük iki olay çıkarılınca +%4,0, BIMAS hariç ≈ +%4,3. Aynı ayda en fazla 4 olay var (03.2020, 04.2025). Medyan (+%8,4) ve isabet (%66) de pozitif, yani sonuç tek bir uçtan gelmiyor. Ancak 126 hücrelik tabloda t ≈ 2 şansla beklenecek bir sonuç ve olayların bir kısmı aynı hissenin tekrarı. **Doğrulanmamış aday.**

### 2.4 Piyasa çapında geri alım dalgası (keşif)

Haftalık GA_YENI sayısı: ortalama 1,7, %90'lık dilim 4. Eşik ≥ 8 ve dalgalar arası ≥ 8 hafta ile 6 dalga: 03.2020 (13h XU100 +%31), 02.2023 deprem (−%12), 12.2023 (+%23), 03.2025 (+%11,5), 11.2025 (+%22,5), **09.2026 (15→28→28→11→13/hafta; ilk girişten (18.09) 4 haftada −%11,8)**. Tamamlanmış 5 dalganın 4'ü pozitif ama n=5. Şu anki dalga 2023 depreminden sonraki en büyüğü.

### 2.5 Hüküm (A)
- Geri alım ve içeriden alım haberinde **kapanışta alınabilir, maliyet sonrası kalıcı bir kenar yok.** Gün 0 tepkisi (XU100 düzeltmeli +%1,0 ile +%1,9) kapanış girişinde kaçırılıyor. Bildirimlerin %56-62'si 17:00'den sonra geliyor; tepki ertesi gün açılışta oluşuyor. Küçük hisselerde girişlerin %12-21'i tavan kilidinde.
- 2024-26'da GA_YENI 5 günlük +%1,8 (t 3,65, medyan +%0,7) ve 20 günlük +%2,55 (t 2,6, medyan +%0,4). Bunlar VİOP dışı küçük ve likit olmayan hisselerde. 20 günlükte en iyi %5 çıkarılınca ort. +%0,1'e iniyor (p5 −%17,7, p95 +%29); yani piyango tipi sağ kuyruk. Girişlerin %12'si (GA_PROG'da %21) tavan kilitli.
- İçeriden alım (özet etiketli) ve küme alımı: kenar yok. Etiketli örneklem ana ortak işlemlerine kayık; bu sonuç yönetim kurulu üyesi alımları için kesin değil.

## 3. (B) Yabancı (yurt dışı yerleşik) haftalık hisse akımı

**Veri:** TCMB EVDS3. Arşiv TP.PYUK3 (2005-01 → 2020-09-04) ve yeni seri TP.MKNETHAR.M7 (2020-09-11 →). 48 haftalık örtüşmede korelasyon 1,000, medyan fark 0. Hafta Cuma biter, yayın izleyen **Perşembe 14:30**, giriş Perşembe kapanışında. Kontrol: TCMB'nin indirilebilir zip dosyasındaki 30.10 haftası Excel'inin zaman damgası 05.11.2026 (Perşembe). 23.10 haftası hisse stoku (31.569,3 mn$) web aramasında çıkan basın haberindeki rakamla birebir aynı (33.981,1 → 31.569,3 mn$). Sinyaller: z52 (haftalık akımın önceki 52 hafta ortalaması ve standart sapmasına göre z), z4 (4 haftalık toplamın z'si), akım/stok (bp), ardışık giriş/çıkış serisi. Revize edilmiş son veri kullanıldı (ilk yayın değil). Revizyonlar küçük olsa da hafif bir ileriye bakma yanlılığı var.

**Akım getiriyi izliyor:** z_w ~ aynı hafta XU100 getirisi b=0,09 (t 10,7), önceki hafta b=0,09 (t 9,4), R² 0,18; 2021-26'da da t 5,1 ve 4,9. Yani yayın günü gördüğümüz akım, 1-2 hafta önceki fiyat hareketinin yansıması.

**İleri getiri (Newey-West t, z için 1 standart sapma başına %):**

| Dönem | Sinyal → seri | 1h | 2h | 4h | 8h |
|---|---|---|---|---|---|
| 2006-26 | z → XU100 | +0,10 (1,0) | +0,25 (1,8) | +0,33 (1,5) | +0,84 (2,5) |
| 2006-26 | z4 → XU100 USD | +0,27 (2,3) | +0,43 (2,0) | +0,80 (2,0) | +1,50 (2,2) |
| 2015-20 | z → XU100 USD | +0,60 (2,7) | +0,69 (2,1) | +1,14 (2,05) | +1,40 (1,4) |
| 2021-26 | z → XU100 | −0,12 (−0,5) | +0,41 (1,1) | +0,26 (0,5) | +1,46 (1,9) |
| 2024-26 | z → XU100 | −0,12 (−0,5) | +0,40 (1,0) | −0,24 (−0,4) | +0,81 (1,1) |
| 2006-26 | z → XBANK/XU100 | −0,02 | +0,06 | +0,02 | +0,12 (0,6) |
| 2006-26 | akım/stok → XU100 | ~0 | ~0 | ~0 | ~0 (0,3) |

- z beşlisi (2006-26, 4 haftalık XU100): Q1 +%1,2, Q5 +%2,2, koşulsuz +%1,6. USD bazında Q1 −%0,4, Q5 +%1,2. Fark küçük ve tek yönlü değil (Q2 < Q1).
- 1 haftalık kural (z > 0 iken endeks, değilse dışarıda): 2006-26 içeride haftalık ort. +%0,50, dışarıda +%0,27, t 1,0. 2021-26'da fark 0; 2024-26'da +%0,25 (t 0,5).
- **Yayın gecikmesi:** Cuma kapanışından Perşembe kapanışına kadar geçen 4 günlük getiri z ile ilişkisiz (t −0,3). Gecikmesiz ("hileli") ve gecikmeli 4 haftalık katsayılar aynı (0,33). Gecikme sonucu bozmuyor, çünkü zaten ortada bir kenar yok.
- **Seri epizotları (örtüşmesiz):** Çıkış serisinin 4. haftası (n=39; biri henüz tamamlanmadı): 8h XU100 +%6,4 (koşulsuzdan +%3,2, t 1,2). 5. hafta (n=21): +%9,3 (+%6,1, t 1,4, isabet %57). Giriş serisinin 4. haftası (n=57): 8h +%0,4 (−%2,8, t −2,05). Yön karşıt (çıkış serisinden sonra alım, giriş serisinden sonra temkin) ama 2021-26'da t < 1.
- **Hüküm (B):** Yabancı akımı **fiyatı izliyor, öngörmüyor.** 2015-20'de USD bazında zayıf bir devam etkisi vardı, 2021'den sonra kayboldu. Akım/stok ölçüsünde hiç yok. Bankalarda hiçbir dönemde yok. **İşlem sinyali olarak kullanılmamalı.** Yalnız "5+ haftalık çıkış serisi" karşıt bir arka plan bilgisi olabilir (anlamlı değil).

## 4. (C) Politika faizi döngüsü, bankalar, 2Y DİBS

**Veri:** TCMB 1 hafta repo tablosu (yürürlük tarihleri; karar = bir önceki işlem günü), 187 PPK karar tarihi (2010-2026, TCMB PPK sayfaları), AOFM (EVDS3 TP.APIFON4). **2Y getiri** benim kurduğum seri: TCMB gösterge nitelikli günlük DİBS değerleri (175 sabit kuponlu ve kuponsuz TRT). "Değer" kirli fiyat (kupon gününde kupon kadar düşüyor, doğrulandı). Kupon tarihleri vade − k×182 gün. Bileşik getiri çözülüp 2 yıla doğrusal interpolasyon yapıldı. Kontrol noktaları: 2012-13 %6-9, 09.2018 %26, 12.2023 %36, 08.01.2026 %35,8 (Gedik bülteni %36,8). Sepetler önceden seçildi. İhracatçı: FROTO TOASO ARCLK VESTL EREGL KRDMD SISE BRISA OTKAR KORDS AKSA EGEEN. Yurt içi: BIMAS MGROS SOKM TTKOM TCELL EKGYO ENJSA DOAS AYGAZ AEFES. Eşit ağırlıklı.

**Plasebo (tüm günler):** XBANK/XU100 21/42/63 günlük ortalama −%0,06, −%0,20, −%0,45; standart sapma %5,7, %7,8, %8,9.

### 4.1 Dönüşler (her olay ayrı; %, giriş karar günü kapanışı)

| Karar | Tür | Δfaiz | ΔY2 gün 0 (bp) | XBANK/XU100 g0 | +21g | +42g | +63g | İhr/Yİ +63g |
|---|---|---|---|---|---|---|---|---|
| 28.01.2014 | ilk artırım (gece) | +5,50 | −6 | −3,7 | −1,1 | +6,9 | +4,1 | +1,8 |
| 24.11.2016 | ilk artırım | +0,50 | +21 | −0,9 | −0,1 | −3,0 | +2,3 | +4,5 |
| 24.09.2020 | ilk artırım (sürpriz) | +2,00 | +26 | +3,5 | −3,0 | +7,8 | +3,9 | +29,0 |
| 22.06.2023 | ilk artırım | +6,50 | −119 | −4,1 | −6,4 | +7,5 | +8,8 | −13,6 |
| 17.04.2025 | ilk artırım | +3,50 | −7 | −1,4 | +5,0 | +13,3 | +18,4 | −5,8 |
| **ilk artırım ort.** | n=5 | | | | −1,1 | **+6,5 (p 0,06)** | **+7,5 (5/5, p 0,05)** | +3,2 |
| 22.05.2014 | ilk indirim | −0,50 | +3 | +0,9 | −1,4 | −1,3 | −2,0 | +16,4 |
| 25.07.2019 | ilk indirim | −4,25 | +20 | −0,4 | −3,6 | +2,9 | −2,4 | −8,2 |
| 23.09.2021 | ilk indirim (sürpriz) | −1,00 | −6 | −2,2 | −2,9 | +0,9 | +5,0 | +13,4 |
| 26.12.2024 | ilk indirim | −2,50 | 0 | −0,6 | +3,2 | +5,1 | −9,5 | −2,8 |
| 24.07.2025 | ilk indirim | −3,00 | 0 | +0,2 | −2,8 | −3,8 | −11,4 | −1,7 |
| **ilk indirim ort.** | n=5 | | | | −1,5 | +0,8 | **−4,1 (1/5, p 0,34)** | +3,4 |
| 20.03.2025 | fiili sıkılaştırma (O/N %46) | 0 | +240 | −7,7 | −9,8 | −4,7 | +5,4 | −12,2 |
| 02.03.2026 | fiili sıkılaştırma (repo ihalesine ara, AOFM 37→40) | 0 | +10 | −4,9 | −13,1 | −18,5 | −16,6 | +8,5 |
| 24.08.2026 | fiili gevşeme (repo yeniden, 40→37) | 0 | −32 | +2,8 | **+13,6** | **+23,1** | — | −2,3 |

AOFM algoritmik dönüşler (5 günlük ortalama, uç noktadan ≥ 150bp, giriş t+1; 2011-2026, 24 dönüş): gevşemeden sonra XBANK/XU100 21g +%3,4 (isabet %75, p 0,04), 42g +%6,2 (p 0,01), 63g +%4,2 (10/11 pozitif). Sıkılaşmadan sonra 21g −%0,2, 63g +%4,5 (p 0,06). Fonlamadaki **gevşeme** bankalar için politika faizi indiriminden daha iyi bir tetik oldu. Son örnek 24.08.2026: 42 günde +%23. Uyarı: 2012'deki 7 algoritmik dönüş (4'ü gevşeme) koridor oynaklığından gelen gürültü. Bunlar çıkarılınca 2014-2026'da 8 gevşeme kalıyor. 63g değerleri: −0,2, +12,3, +1,8, +2,5, +5,0, +8,1, +2,9; 2025-05 ve 2025-06 olayları örtüşüyor, 2026-08 henüz tamamlanmadı.

### 4.2 Döngü ve devam kararları (Aralık 2026'nın karşılığı)

| İndirim döngüsü | Karar sayısı | Karardan önceki 63g XBANK/XU100 | Sonraki 21g | Sonraki 63g | İhr/Yİ 63g |
|---|---|---|---|---|---|
| 12.2010-05.2013 | 6 | −1,0 | −0,1 | −5,0 | +5,5 |
| 05.2014-02.2015 | 5 | +4,0 | −1,5 | −3,7 | +9,0 |
| 07.2019-05.2020 | 9 | −2,2 | −3,1 | −9,1 | −3,9 |
| 09.2021-02.2023 | 9 | +3,6 | +1,0 | −2,9 | +3,1 |
| 12.2024-03.2025 | 3 | +7,9 | −4,6 | −12,4 | −4,8 |
| 07.2025-10.2026 | 6 | +6,8 | −1,0 | −4,7 | −9,2 |
| **Ortalama** | 38 | **+3,2** | −1,6 | **−6,3 (6/6 negatif, döngüler arası t −4,2)** | ≈0 |

- Tüm indirimler (n=37): 63g −%5,9, medyan −%4,1, isabet %24. Tüm artırımlar (n=18): 63g +%4,3, isabet %72. Sabit kararlar (n=131): ≈0.
- **Döngü içi sürprizsiz indirim** (dönüş değil, |ΔY2 gün 0| < 25bp; n=24): 21g −%2,3 (isabet %33), 42g −%4,8 (%17), 63g −%6,6 (%17).
- Karardan önceki 63 günde bankalar > %10 koştuysa (n=5 indirim): sonraki 63g −%10,2 (isabet %20). **Bugün aynı ölçü +%22 (22.10 kararından önce) ve son 63 gün +%26.**

### 4.3 Sürprizler (piyasa bazlı: PPK günü ΔY2 en üst ve en alt %10, ≥ +25bp / ≤ −30bp)

| | n | XBANK/XU100 21g | 42g | 63g (isabet, p) | İhr/Yİ 63g (p) |
|---|---|---|---|---|---|
| Şahin sürpriz | 19 | +1,0 | +3,9 | +7,4 (%84, p 0,00) | −1,8 (0,11) |
| Güvercin sürpriz | 19 | +2,3 | +4,6 | +4,2 (%63, p 0,02) | −4,4 (0,01) |

İki uç da bankalar için pozitif. Olaylar 2022-2024'te kümelenmiş (makro-ihtiyati rejim ve bankaların güçlü göreli koşusu). Gün 0'da ΔY2 ile banka tepkisi arasındaki eğim zayıf (t −1,9). **Yön bilgisi vermiyor.** Ders şu: büyük faiz haberi sonrasında bankaların oynaklığı yüksek. Bootstrap p, örtüşmeyi ve zaman kümelenmesini hesaba katmadığı için iyimser.

### 4.4 2Y getiri öncü sinyal mi?

| Dönem | Sinyal | b (63g, 1 puan başına %) | NW t | Örtüşmesiz t (3 başlangıç) | Geçmiş 20g (2010-26 ve 2023-26'da 60g) banka getirisi kontrollü t |
|---|---|---|---|---|---|
| 2010-26 | ΔY2 60g | +0,85 | 5,2 | 3,7 / 5,2 / 2,4 | 4,9 |
| 2010-17 | ΔY2 60g | +0,68 | 1,8 | — | 1,6 |
| 2018-22 | ΔY2 60g | +0,66 | 2,2 | 3,2 / 4,3 / 2,9 (2018-26) | 2,0 |
| 2023-26 | ΔY2 60g | +0,88 | 3,4 | 4,0 / 2,1 / 1,6 | 3,8 |
| 2010-26 | 2Y − AOFM | +0,19 | 0,8 | — | 0,5 |

- Eşzamanlı ilişki ters: 20g ΔY2 ile aynı 20g XBANK/XU100 arasında korelasyon −0,43 (faiz yükselirken bankalar düşüyor). Sonraki 1-3 ayda **tersine dönüyor**: 2023-26'da yükselen 2Y üçlüsünde (ΔY2 +446bp) sonraki 63g XBANK/XU100 +%8,7 (isabet %74), düşen 2Y üçlüsünde (−251bp) −%2,7.
- Kural (aylık, örtüşmesiz): ΔY2(60g) > +100bp ise 21g banka-uzun/XU100-kısa, < −100bp ise tersi, 30bp maliyet. 2010-26 aktif ay başı +%0,45 ile +%1,0 (t 0,65-1,76). 2018-26 +%0,7 ile +%1,6 (t 0,8-1,9). 2023-26 +%1,6 ile +%2,9 (t 1,3-2,2). **Başlangıç gününe duyarlı. Kendi başına bir strateji değil, banka ağırlığı için bir eğim.**
- Bu bulgu 4.2 ile aynı mekanizma: sıkılaşma (yükselen 2Y) → bankalar sonradan toparlanıyor; gevşeme (düşen 2Y, indirimler) → bankalar önce koşuyor, sonra geride kalıyor.

### 4.5 Bugünkü kurulum (05.11.2026 kapanışı)

- Politika faizi %36 (22.10: −100bp, beklendiği gibi), O/N borç verme %39, AOFM %36. 2026 seyri: 22.01'de %37'ye indirim. **01.03.2026'da repo ihalelerine ara verildi, AOFM %40'a çıktı (fiili sıkılaştırma).** 23.08.2026'da ihaleler yeniden başladı (fiili gevşeme). 22.10'da indirim.
- Beklenti: TCMB Ekim Piyasa Katılımcıları Anketi'nde ilk toplantı %36, **ikinci toplantı (10.12.2026) %35**, üçüncü %34,35. AA Finans ve Bloomberg HT yıl sonu medyanı %35. Ekim TÜFE yıllık %29,77 (aylık %2,58, beklenti ~%2,2; kardeş ajan `tr_makro_engel`, AA/TE), yani yukarı risk var.
- Y2 ≈ %40,0 (t−1: %40,18). ΔY2 20g +47bp, **60g −81bp (kural eşiği altında, nötr)**. 2Y − AOFM = +418bp: piyasa 2Y vadede indirim fiyatlamıyor.
- XU100 21.08'den 30.10'a −%26 (14.515 → 10.760), 05.11'de 11.333. XBANK/XU100 63 günde +%26, 21 günde +%8,5.
- **Çıkarım:** 10.12 PPK beklenen bir devam indirimi. Tarihte bu tür kararlardan sonra 1-3 ayda bankalar XU100'ün gerisinde kaldı (n=24, isabet %17-33; döngü düzeyinde 6/6). Üstelik bankalar ön koşuyu yapmış durumda (+%26 / 63g). Yüksek TÜFE sürprizi indirimi erteletirse "sürprizsiz indirim" senaryosu yerine şahin ya da sabit senaryoya geçilir. Tarihte sabit kararlar ≈ 0, şahin sürprizler bankalar için olumlu (63g +%7,4). Asimetri banka-aşırı-ağırlığına karşı değil, **PPK sonrasına taşımaya karşı**.

### 4.6 Hüküm (C)
- **İşe yarayan:** (i) İndirim kararından sonra bankaları XU100'e karşı azaltmak veya kısa tutmak (döngü düzeyinde 6/6, t −4,2; ancak yalnızca 6 bağımsız döngü var). (ii) Fonlama (AOFM) gevşemesinden sonraki 1-2 ayda banka ağırlığını artırmak (12 olay, isabet %75-83). (iii) 2Y'nin 60 günde > 100bp yükselişinden sonra banka ağırlığını artırmak (karşıt, örtüşmesiz t 2-5, kuralı zayıf).
- **İşe yaramayan:** İhracatçı ve yurt içi rotasyonu faiz dönüşlerine göre. Sürpriz yönüne göre banka pozisyonu.
- Uygulama: Bankaların tek hisse vadelisi var (AKBNK GARAN ISCTR YKBNK HALKB VAKBN TSKB), karşı bacak XU030 vadelisi. Göreli pozisyonun TL faiz eşiği yok, teminat getirisi ayrıca kazanılır. Yine de beklenen +%4-6 / 63g, TL nakit (%36) üstüne net bir ek getiri sağlar. Risk: 63 günlük göreli standart sapma %9.

## 5. Sınırlamalar ve çoklu test
- A: 7 olay türü × 3 evren × 2 dönem × 3 ufuk = 126 hücre. t ≈ 2 olan 3-5 hücre şansla beklenir. Tek göze çarpan (VİOP'lu GA_PROG) bu sınırda. İçeriden işlem yönü yalnızca özetten. Hayatta kalma yanlılığı var. Olay listesindeki 85 kod için İş Yatırım'da veri yok; bunlar örneklem dışında (ağırlıkla yönsüz PAS olayları).
- B: Revize veri; ilk yayın vintage'ı kullanılmadı. 2005-2020 arşiv serisinin tanımı yeni seriyle örtüşüyor (korelasyon 1,0).
- C: Dönüşler 5+5 (+3 fiili), döngüler 6+5. Bootstrap p bağımsızlık varsayıyor; döngü düzeyindeki t daha dürüst bir ölçü. 2Y serisi model değerlerinden (TCMB gösterge değerleri) kuruldu; 2023-05 gibi günlerde 300-600bp günlük sıçramalar var. Bu yüzden 20 ve 60 günlük değişimler ve t−1 değeri kullanıldı. XBANK fiyat endeksi (temettü hariç), XU100 de öyle.
- Hiçbir sonuç gerçek zamanlı ileriye dönük test görmedi. Yatırım tavsiyesi değildir.

## 6. Kaynaklar
- KAP bildirim sorgusu: https://www.kap.org.tr (konu: "Payların Geri Alınmasına İlişkin Bildirim", "Pay Alım Satım Bildirimi").
- TCMB EVDS3 (TP.MKNETHAR.*, TP.PYUK*, TP.APIFON4, gösterge DİBS değerleri): https://evds3.tcmb.gov.tr. Menkul kıymet istatistikleri: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Parasal+ve+Finansal+Istatistikler/Menkul+Kiymet+Istatistikleri/. PPK kararları: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/PPK/2026.
- 2026 kararları ve beklentiler: [doviz.com faiz kararları](https://www.doviz.com/faiz-kararlari), [Yalova Hayat, Ekim 2026 kararı](https://www.yalovahayat.com/gundem/tcmb-ekim-2026-faiz-kararini-acikladi-aylar-sonra-bir-ilk-146324), [Ekotürk, Ekim PKA](https://www.ekoturk.com/haberler/piyasa-katilimcilari-anketi-aciklandi-yil-sonu-faiz-beklentisi-yuzde-347/), [Bloomberg HT, Ekim anketi](https://www.bloomberght.com/bloomberg-ht-nin-ekim-ayi-faiz-anketi-sonuclandi-3791499), [Dünya, repo ihaleleri yeniden](https://www.dunya.com/ekonomi/tcmb-bir-hafta-vadeli-repo-ihalelerine-yeniden-basliyor-haberi-837382), [Ekotürk, 6 ay sonra repo](https://www.ekoturk.com/haberler/tcmb-6-ay-sonra-repo-ihalelerine-donuyor-karar-ne-anlama-geliyor/), [Gedik DİBS bülteni 08.01.2026](https://cdn.gedik.com/cdn/bulletin/2026/01/08/DIBS_Bulten_08_01_2026_c9dbf2cd.pdf).
