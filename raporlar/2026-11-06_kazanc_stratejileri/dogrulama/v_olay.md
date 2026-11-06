# Doğrulama: olay çalışmaları (bedelsiz, halka arz, akış/rejim)

06.11.2026. Denetçi: `v_olay`. Yatırım tavsiyesi değildir.

Denetlenen raporlar: `ajanlar/olay_bedelsiz.md`, `ajanlar/olay_halka_arz.md`, `ajanlar/olay_akis_rejim.md` ve bunların kodları.

Kendi kodum ve çıktılarım `scratchpad/audit_olay/` altında (`t1`–`t5`). Varsayılan tutumum şüphecilikti.

## 0. Özet hüküm

| Rapor | İddia | Hüküm | Düzeltilmiş / doğrulanmış sayı |
|---|---|---|---|
| Bedelsiz | Hak günü, SPK onayı ve başvuru tarihleri doğru | **DOĞRU** | Hak günü 13/13, onay 11/11, başvuru 9/10 tuttu (GOODY 2016'da çelişki var) |
| Bedelsiz | YK (ilk) duyurusu tarihi doğru | **KISMEN** | 12 olayın 11'i doğru. SASA 2024 %700'de ilk duyuru 27.03.2024 kapanış sonrası, çalışma ise 06.06.2024 revizyonunu almış (≈48 işlem günü geç). Kod "Özel Durum Açıklaması" konusunu taramıyor. |
| Bedelsiz | Bölünme düzeltmesi temiz | **DOĞRU** | Ayrı çekilmiş seride hak günü |r|>%20 olan olay 0/510; ham medyan sıçrama −%53, düzeltilmiş +%0,1 |
| Bedelsiz | Hak sonrası [1,10] −%3,2 (t −5,6) | **DOĞRU** | −%3,26 (t_tarih −5,5, t_ay −6,2); 2024–26: −%1,45 (t −1,5) |
| Bedelsiz | YK duyurusu [0,0] +%2,4; %18'i tavan kilitli | **DOĞRU** | +%2,24 (t 9,1); kilitli payı %18,4 |
| Bedelsiz | İlk dolabilir kapanışta al, 5 gün tut: −%1,8 | **DOĞRU** | −%1,58 (t −4,2) |
| Bedelsiz | Duyuru etkisinin "tamamı" kilitli günlerde ("kilitsiz [0,1] +%0,1") | **KISMEN** | Sonuca göre koşullama var (kilit, t0 getirisinin kendisiyle tanımlı), bu yüzden totolojiye yakın. Geçerli ölçü dolabilir giriş sonucu (−%1,6 / 5g); hüküm değişmez. |
| Bedelsiz | Sızıntı payı: ön birikimin %65–72'si | **KISMEN** | Kaçırılan ilk duyurular (SASA tipi) ön pencereye düşüp oranı yukarı çekiyor. Payın yalnız üst sınır olduğu söylenebilir. |
| Bedelsiz | Folklorun alım kolları işlenemez | **DOĞRU** | Bağımsız seride de aynı |
| Bedelsiz → temettü | Verim ≥%5, duyuru t0 → hak−1: +%8,5 (t 11) | **DOĞRU, büyüklük KISMEN** | XU100'e karşı +%8,7 (med +%6,7, N=361). Muhafazakâr kıyasla (eşit ağırlıklı toplam getiri) **+%6,5**, med +%4,1, t_ay 6,5. 2024–26: +%13,5 (N=61). Verim %2–5 kovası ≈0, <%2 kovası −%1,4 (raporda +%5,0 ve +%3,4 yazıyor; bunlar kıyas yanlılığı). |
| Halka arz | Liste eksiksiz, arz fiyatları doğru | **DOĞRU** | İş Yatırım "Birincil Halka Arz" listesi 2020+ 241 kod; fark yalnız raporun belgelediği dışlamalar. ARMGD ve NETGL haberle doğrulandı. |
| Halka arz | Katılımcı E-AOF medyan +%45 / ort +%67 | **KISMEN** | Sayı yeniden üretiliyor (+%45,0 / +%66,7). Ancak E günü ileriye bakışla seçiliyor. İleriye bakışsız kural ("kuyruk gün içinde ilk bozulduğunda AOF'tan sat") medyan **+%33**, ort +%51 veriyor; E kapanış satışı medyan +%38. |
| Halka arz | Yıllık tek hesap kârı 10–27 bin TL | **KISMEN** | Rapor kuralıyla doğru (2024: 10,4 bin). İleriye bakışsız kuralla 2023 22,1 / 2024 7,9 / 2025 8,5 / 2026 17,1 bin TL. |
| Halka arz | Seri bitince al: BH5 −%3,7, BH21 medyan −%11,2 | **DOĞRU** | −%3,7 (t_ay −2,5), medyan −%11,2; 2024–26 BH21 medyan −%17,3, isabet %26 |
| Halka arz | Lock-up bitişinde etki yok | **KISMEN** | 98/200 arzda süre 365 gün varsayıldı; ölçüm hatası sonucu sıfıra çekiyor |
| Halka arz | Veri toplama kurallara uygun | **SORUNLU** | halkarz.com betiğe 403 verdi, sonra aynı sayfalar WebFetch ile okundu. Bu, engelin başka bir istemciyle aşılması sayılabilir. Liste ve fiyatlar uyumlu kaynaklardan doğrulanabiliyor; kişi ve lot alanları yalnız bu sayfalardan geliyor. |
| Akış/rejim C1 | İndirim sonrası 63g XBANK/XU100 −%5,9; döngü düzeyinde 6/6 negatif, t −4,2 | **DOĞRU (sayılar), KISMEN (güç)** | Birebir yeniden üretildi. Etkin n=6 döngü ve döngüler sonradan tanımlı; "ön koşu >%10" alt kümesindeki n=5 aslında 3 epizot. |
| Akış/rejim | Bugünkü kurulum: XBANK/XU100 63g +%26, XU100 21.08'den −%22, GARAN 04.11 +%6,8 | **DOĞRU** | +%26,3; −%21,9; +%6,8 / XU100 +%4,1; KAP 03.11 19:54 |
| Akış/rejim B | Akım fiyatı izliyor; 8 haftalık tahmin t 2,5, "2015–20'den geliyor" | **KISMEN** | 2006–26 t 2,51 doğru. TL bazında 2015–20 t yalnız 0,7, 2021–26 t 1,9 (sınırda). "Hiç yok" değil, zayıf. |
| Akış/rejim A | VİOP'lu geri alım programı zayıf aday (n=41) | **DOĞRULANAMADI** | Yeniden hesaplanmadı. Rapor 126 hücrelik çoklu testi zaten not ediyor; kullanılamaz. |
| Akış/rejim C | AOFM gevşemesi (12 olay) +%6,2 / 42g | **DOĞRULANAMADI** | Yeniden hesaplanmadı. n küçük, 2012 gürültüsü var. |

## 1. Ne yaptım

- **Fiyatlar:** Ajanların kendi panelleri yerine `bist_test` ajanının **ayrı çektiği** HisseTekil serilerini (496 bugün işlem gören hisse, ham ve düzeltilmiş kapanış, gün içi en yüksek ve en düşük) ve `bist_test/endeks` ChartData endekslerini kullandım. Bu yüzden N'lerim ajanınkinden küçük; kottan çıkmış hisseler yok. Halka arzda ajanın ham fiyat dosyalarını (`ht_*.parquet`) kullandım, ölçü tablosunu (`ipo_olay.csv`) kullanmadım.
- **Kod:**
  - `t1_temettu.py`, `t1b_taban.py`, `t1c_ew.py`: temettü kuralı. Ham kapanış, kendi t0 kuralım (18:00 ve 17:00 kesimleri), kendi eşit ağırlıklı kıyasım.
  - `t2_bedelsiz.py`: CAR ve işlem kuralları.
  - `t3_halka_arz.py`, `t3b_katilimci_alt.py`: seri, E, katılımcı getirisi, ileriye bakışsız satış kuralı.
  - `t4_ppk_banka.py`: XBANK/XU100, döngüler, bugünkü kurulum.
  - `t5_akim.py`: yabancı akımı z skoru ve NW regresyonları.
- **Olay tarihleri:** 13 bedelsiz olayı, 2 halka arzı ve 2019–2026 PPK kararlarını kamu haber/KAP kaynaklarıyla karşılaştırdım (web araması, varsayılan başlıklar). KAP'a doğrudan istek atmadım.

## 2. Bedelsiz (`olay_bedelsiz`)

### 2.1 Olay tarihi kontrolü (kamu kaynakları)

| Hisse, oran | P1 (YK) | P2 (başvuru) | P3 (SPK onayı) | Hak günü | Sonuç |
|---|---|---|---|---|---|
| SASA 2024 %700 | CSV 06.06.2024 08:53; **gerçek ilk duyuru 27.03.2024 kapanış sonrası** (06.06 revizyon) | 07.06 ✓ | 08.08 bülten ✓ | 12.08 ✓ | **P1 YANLIŞ** |
| ADEL 2024 %1.000 | 01.07 ✓ | 22.07 ✓ | 28.08 (2024/43) ✓ | 04.09 ✓ | ✓ |
| FROTO %900 | 19.11.2024 ✓ (YK 18.11) | 29.01.2025 ✓ | 30.04 (2025/28) ✓ | 07.05 ✓ | ✓ |
| AKSA %1.100 | 26.04.2024 ✓ | 27.05 ✓ | 19.07 ✓ | 24.07 ✓ | ✓ |
| PGSUS %388,76 | 28.02.2024 ✓ | — | 02.05 ✓ | 14.05 ✓ | ✓ |
| KORDS %1.800 | 27.07.2026 seans öncesi ✓ | 28.07 ✓ | 09.09 ✓ | 14.09 ✓ | ✓ |
| TUPRS %600 | 14.02.2023 ✓ | — | 30.03 bülten (2023/21); CSV KAP 31.03 09:42 → aynı t0 ✓ | 04.04 ✓ | ✓ |
| BIMAS 2026 %100 | 20.02 23:20 (YK 19.02; KAP'a 20.02'de) ✓ | 24–25.02 ✓ | 07.05 ✓ | 14.05 ✓ | ✓ |
| EREGL 2024 %100 | 28.02.2024 ✓ | 08.05 ✓ | 21.11 ✓ | 27.11 ✓ | ✓ |
| MIATK %1.200 | 14.03.2023 ✓ | 07.06 ✓ | 10.11 ✓ | 20.11 ✓ | ✓ |
| CWENE 2024 %708 | 19.07 ✓ | 22.07 ✓ | 28.11 (2024/54; CSV'de bülten no "2024" diye yarım ayrıştırılmış) ✓ | 04.12 ✓ | ✓ |
| GOODY 2016 %2.165 | 28.03.2016 20:00 ✓ (haber 29.03) | CSV 14.04; haber "09.05'te başvurdu" | 23.05 (doğrulanamadı) | 01.06 ✓ | P2 çelişkili |
| ALARK 2018 | — | — | — | 14.09.2018 ✓ | ✓ |

**Neden SASA kaçtı:** KAP önbelleği (`kap_CA_all.pkl`) yalnız "Sermaye Artırımı-Azaltımı" ve "Kar Payı" konularını içeriyor. SASA'nın 27.03.2024 bildirimi bu konularda yok, muhtemelen "Özel Durum Açıklaması" konusunda.

**Etkisi:** Doğru duyuru (27.03), raporun [−60,−1] ön penceresine düşüyor. Böyle olaylar duyuru günü etkisini sulandırıyor ve sızıntı payını şişiriyor. Oranı ölçemedim: 12 olayda 1 hata; ≥%500 ve revizyonlu olaylarda daha olası.

### 2.2 Bağımsız yeniden hesap (ayrı çekilmiş fiyat serisi)

| Ölçü | Rapor | Benim | Not |
|---|---|---|---|
| Hak [1,5] | −%2,40 (t −5,9) | −%2,50 (t −6,2), N=509 | |
| Hak [1,10] | −%3,19 (t −5,6) | −%3,26 (t_tarih −5,5, t_ay −6,2) | Aylık kümelemede de sağlam |
| Hak [1,10] 2024–26 | −%1,2 (t −1,3) | −%1,45 (t −1,5) | Zayıflama doğru |
| Hak [−5,−1] | +%2,33 | +%1,83 (t 4,5) | |
| P1 [0,0], kilit payı | +%2,41, %18 | +%2,24 (t 9,1), %18,4 | |
| P1 [−60,−1] | +%9,78 | +%9,78 | |
| P1 dolabilir → +5g BHAR | −%1,80 (t −4,9) | −%1,58 (t −4,2) | |

**Yöntem notları:**
- **Kilit ölçüsü:** "Kapanış = gün içi en yüksek" tanımı, gün içinde tavan altında işlem görüp tavanda kapanan günleri de kilitli sayıyor. Bu günlerde gün içinde alım mümkündü. Kilitli payı biraz abartılı olabilir; hüküm değişmez.
- **Kümelenme:** Yalnız olay gününe göre yapılmış. Bu, örtüşen pencereleri tam yakalamıyor. Aylık kümelemede t'ler benzer çıktı, takvim-zamanı portföyü de raporda var. Sonuç sağlam.
- **Hayatta kalma:** Benim örneklemim yalnız bugün işlem gören hisselerden oluşuyor. Ajanın örneklemi daha geniş. İki sonuç aynı yönde ve büyüklükte.

### 2.3 Temettü (raporun en güçlü bulgusu): mekanik hata yok

| Kontrol | Sonuç |
|---|---|
| Hak günü doğru mu? | Ham kapanış hak gününde verim kadar düşüyor (medyan oran 1,00; ortalama düşüş −%7,99, ortalama verim %7,87). Hak−1 gerçekten temettülü son gün. |
| Verim duyuruda biliniyor mu? | P1 özetleri çoğunlukla "kâr dağıtımına ilişkin YK kararı/önerisi"; tutar duyuruda var. Verim = D/P(t0−1); ileriye bakış yok. Ayar oranından ve brüt/100'den hesaplanan verim birebir aynı. |
| Ham fiyatla, ayrı veriyle | ≥%5: XU100'e karşı +%8,68, med +%6,73, t_tarih 10,8, t_ay 9,5, isabet %74 (N=361). 17:00 kesimiyle +%8,43. |
| Muhafazakâr kıyas | Kıyas: aynı evrenin eşit ağırlıklı **temettü dahil** toplam getirisi; olay getirisi temettüsüz. Sonuç **+%6,47**, med +%4,13, t_ay 6,5, isabet %67. 2024–26: +%13,5 (N=61). Verim %2–5 kovası ±0, <%2 kovası −%1,4. |
| Koşulsuz taban | Aynı hisselerin ex-gün içermeyen 27 günlük BHAR'ı +%1,8 (med −%0,6). Tabandan arındırılmış ≈ **+%6,9**. |
| Uç değer | En iyi %5 hariç +%6,3, t 11,6 |
| Likidite | Medyan 60 günlük TL hacim 4,5 mn; olayların %52'si 5 mn'nin altında. Hacim ≥20 mn TL (N=119): +%10,2, t 8,4. Likit hisselerde de var. |
| Mevsim / kapasite | Girişlerin %81'i Şubat–Mart'ta. 2024–26'da yılda 14–25 olay. |

**TL engeli:** Ham getiri (temettüsüz, hedgesiz) ortalama +%8,8, medyan +%4,8, medyan 27 gün. %40 pro-rata engel ortalama %5,7. Engeli geçen işlem payı tüm dönemde %50, 2024–26'da %77.

**Uygulama:** XU030 vadelisiyle piyasa riski hedgelenirse getiri yaklaşık "TL faizi + BHAR" olur. Bu durumda işlem başına +%6–7 fazla, engelin açıkça üstünde.

**Açık riskler:**
- Yalnız gerçekleşen temettüler örnekte var.
- Etkinin bir kısmı aynı dönemdeki kazanç açıklamalarından olabilir.
- 2024–26 sonucu N=61 olayla ölçülüyor.
- Bu bir "hızlı bakış"tı; önceden kayıtlı bir test değil (verim eşiği %5 sonradan seçilmiş olabilir, ama %3 ve %8 eşiklerinde de sürüyor).

## 3. Halka arz (`olay_halka_arz`)

| Ölçü | Rapor | Benim (ham dosyalardan) |
|---|---|---|
| Gün1 tavan / kilitli | %81 / %68 | %81 / %69 |
| Seri ort / medyan, ≥5 gün | 4,6 / 4, %45 | 4,6 / 4, %44 |
| Katılımcı E-AOF | ort +%66,6, med +%45,4 | ort +%66,7, med +%45,0 (t_ay 7,8) |
| Seri sonrası BH5 | −%3,7 (t_küme −2,5), med −%6,5 | −%3,7 (t_ay −2,46), med −%6,5, isabet %33 |
| BH21 / 2024–26 BH21 | med −%11,2 / med −%17,3, isabet %25 | med −%11,2 / med −%17,3, isabet %26 |
| BH63 | +%9,5, med −%6,5 | +%9,7, med −%5,5 |
| Tek hesap kârı 2023/24/25/26 (bin TL) | 26,8 / 10,5 / 13,5 / 23,8 | 26,7 / 10,4 / 13,4 / 22,7 (TKNKA'nın ilk günü dosyada eksik) |

**Doğru olanlar:**
- **Liste:** İş Yatırım sermaye tablosundaki "Birincil Halka Arz" kayıtları 2020–26'da 241 kod. halkarz örneğinden farkı yalnız ENPRA, MARMR ve GMTAS (raporda dışlananlar). Hayatta kalma yanlılığı görmedim.
- **Fiyat ve tarih:** ARMGD (40 TL, 436.160 katılımcı, ~76 lot) ve NETGL (25,52 TL, ilk işlem 17.09.2026, 3 tavan, 4. gün bozuldu) haberle tutuyor.
- **Gün1 limitleri:** 4 arzda gün1 getirim limit dışı çıktı (TKNKA, ISVEA, LMKDC, KLSYN). Neden: HisseTekil dosyasında ilk günler eksik. Ajan bunları ChartData ile doğru işlemiş.

**Sorunlar:**
1. **E-AOF ileriye bakışı:** E, "kapanışı tavan olmayan ilk gün" olarak tanımlı; bu, gün sonunda bilinir. Seri içi tavan günlerinin bir kısmında gün içinde kuyruk bozulup kapanışta tekrar tavana dönülüyor. Gerçek zamanlı bir "kuyruk bozulunca sat" kuralı bu günlerde erken tetikleniyor (arzların %50'si).
   - İleriye bakışsız kural: medyan **+%32,8**, ort +%51,3; 2024–26 medyanı +%23,7.
   - Kapanış seansında satış (E kapanış): medyan +%38,2.
   - **Düzeltilmiş katılımcı primi:** medyan +%33–38. Yıllık TL kârı %15–35 düşük.
2. **Veri toplama:** halkarz.com 403 verince ajan taramayı durdurmuş, UA taklidi yok. Ama detay sayfalarını WebFetch ile okumuş. Kural "engellenirsen başka kaynak kullan" diyor; bu yol, engelin başka istemciyle aşılması olarak okunabilir. Önerim: kişi ve lot alanları KAP "halka arz satış sonuçları" bildirimlerinden yeniden alınmalı. Liste ve fiyat zaten uyumlu kaynaklardan doğrulanıyor.
3. **Lock-up:** 98/200 arzda süre varsayımsal; "etki yok" sonucu zayıf kanıt.
4. **Takvim-zamanı portföyü:** Yıllık rakamlar (−%90, −%37) yalnız aktif günlerin yıllıklandırılması. Yön doğru, büyüklük sunuma bağlı.

## 4. Akış/rejim (`olay_akis_rejim`)

### 4.1 C1: faiz indirimi ve bankalar

**Karar tarihleri:** 2019–2026 PPK kararlarını bilinen TCMB geçmişiyle tek tek karşılaştırdım; hepsi tuttu. Örnekler: 25.07.2019 −425, 2020 indirimleri, 18.03.2021 +200, 2021 ve 2022 indirimleri, 22.06.2023 +650, 26.12.2024 −250, 20.03.2025 fiili sıkılaştırma, 17.04.2025 +350, 24.07.2025 −300.

**Ölçek hatası:** XBANK'taki 02.07–31.12.2010 1/100 ölçek hatası ayrı çekilmiş seride de var; düzeltme gerekli ve doğru yapılmış.

| Ölçü | Rapor | Benim |
|---|---|---|
| 37 indirim, 63g XBANK/XU100 | −%5,9, isabet %24 | −%5,91, med −%4,13, isabet %24 (fark 0) |
| Döngü düzeyi | −%6,3, t −4,2, 6/6 | −%6,33, t −4,22, 6/6 |
| Sürprizsiz devam indirimi (n=24) 21/42/63g | −2,3 / −4,8 / −6,6 | aynı; isabet %33 / %17 / %17 |
| Plasebo 63g | −%0,45, sd %8,9 | −%0,10, sd %8,3 |
| Ön koşu >%10 sonrası (n=5) | −%10,2 | −%10,2; ama 3'ü aynı 2022 epizodu |

**Eleştiri:**
- Bağımsız gözlem 6 döngü.
- Döngüler sonradan tanımlanmış. 4. döngü 2022'deki 7 aylık arayı içine alıyor; 6. döngü Mart 2026'daki fiili sıkılaştırmanın üzerinden geçiyor.
- 63 günlük göreli oynaklık %8–9 olduğundan tek bir PPK (10.12) yazı-turaya yakın, yalnız eğilimli.
- "Banka-uzunu PPK sonrasına taşıma" önerisi veriyle tutarlı. Ama AOFM gevşemesinden ve 2Y kuralından gelen sinyallerle aynı anda çelişebilir; rapor bunu açıkça birleştirmiyor.

### 4.2 B: yabancı akımı

- z skorunu kendim kurdum; ajanınkiyle korelasyon 1,00.
- Son 5 hafta: −190, −248, −89, −100, −66 mn $ (seri −5 doğru). 23.10 stoku 31.569 mn $.

| Dönem | İleri 8 haftalık XU100 (1 sd başına) | NW t |
|---|---|---|
| 2006–26 | +%0,88 | 2,51 |
| 2015–20 | +%0,51 | 0,71 |
| 2021–26 | +%1,46 | 1,87 |
| 2024–26 | +%0,81 | 1,06 |

"Tüm dönem t'si 2015–20'den geliyor" ifadesi yalnız USD bazında doğru; TL bazında değil. İşlem sinyali olmadığı hükmü doğru.

### 4.3 A: geri alım ve içeriden alım

- GARAN programı KAP'ta 03.11.2026 19:54; giriş 04.11 kapanışı. Doğru ve 17:00 kesimi muhafazakâr.
- Tablolar yeniden hesaplanmadı.
- İçeriden işlem yönü yalnız özetten alınmış ve kontrol paneli yalnız bugün işlem gören hisselerden oluşuyor; rapor ikisini de açıkça yazıyor. "Kenar yok" hükmü kabul, VİOP'lu aday kullanılamaz.

## 5. Son kullanılabilir hükümler

1. **Bedelsiz alım folkloru: yaramaz** (doğrulandı). Hak gününden önce satmak geçerli bir çıkış kuralı. Hak sonrası düşüş 2024–26'da zayıf (−%1,5, t −1,5).
2. **Yüksek verimli temettü (≥%5) duyuru → hak−1: en güçlü aday, bağımsız veriyle yeniden üretildi.**
   - Beklenen fazla getiri **+%6–7 / ~27 işlem günü**; rapordaki +%8,5 kıyas yanlılığı içeriyor.
   - Önkoşullar: XU030 vadelisiyle hedge, hacim filtresi (≥5–20 mn TL), Şubat–Mart girişleri, hak−1 kapanışında çıkış.
   - Sonraki adım: önceden kayıtlı ileri test (2027 sezonu) ve teklif tutarının KAP metninden alınması.
3. **Halka arz:**
   - Kazanç yalnız katılım primi: gerçekçi medyan +%33–38, hesap başına yılda ~8–22 bin TL. Ölçeklenmiyor.
   - Seri sonrası alım zarar ettiriyor (doğrulandı).
   - Kişi ve lot verisi uyumlu bir kaynaktan yeniden alınmalı.
4. **Bankalar ve PPK:** "İndirim sonrası banka göreli zayıflığı" sayısal olarak doğru ama n=6. 10.12 için yalnız pozisyon boyutu eğilimi olarak kullanılmalı, tek başına işlem kuralı değil. Yabancı akımı ve geri alım için sinyal yok.

## Kaynaklar (tarih kontrolleri)

- **SASA:**
  - [Habertürk](https://www.haberturk.com/sasa-dan-bedelsiz-sermaye-artirimi-karari-2024-sasa-sermaye-artirimi-ne-zaman-3673118-ekonomi)
  - [Capital](https://www.capital.com.tr/haberler/tum-haberler/sasa-polyester-bedelsiz-kararini-duyurdu)
  - [Borsatek, karar değişikliği](https://www.borsatek.com/sasadan-sermaye-artirimi-kararinda-degisiklik-109328h/)
  - [Midas](https://www.getmidas.com/midasin-kulaklari/sasadan-700-bedelsiz-sermaye-artirimi-karari-p-37241)
  - [Paratic](https://paratic.com/sasa-polyester-yuzde-700-bedelsiz-icin-tarih-verdi/)
- **ADEL:** [Paraajansı](https://paraajansi.com.tr/sermaye-artirim/100-lot-1100-lot-olacak-1000-rekor-bedelsiz-onaylandi-21459707h), [Midas](https://www.getmidas.com/midasin-kulaklari/adel-kalemcilik-adel-1000-bedelsiz-sermaye-artirimi-nasil-gerceklesecek-p-46335)
- **FROTO:** [Bloomberg HT](https://www.bloomberght.com/ford-otomotiv-de-bedelsiz-sermaye-artirimi-karari-3734905), [Midas](https://www.getmidas.com/midasin-kulaklari/spk-fordun-900-bedelsiz-sermaye-artirimini-onayladi-p-130247)
- **AKSA:** [Milliyet Uzmanpara](https://uzmanpara.milliyet.com.tr/raporlar-analizler/spk--aksa-akrilikin-pay-ihracini-onayladi/1486695)
- **PGSUS:** [Capital](https://www.capital.com.tr/haberler/tum-haberler/pegasus-pgsus-bedelsiz-tarihini-duyurdu)
- **KORDS:** [CNBC-e](https://www.cnbce.com/borsa/bist100de-islem-goren-dev-sirketten-yuzde-1800-oraninda-bedelsiz-sermaye-artirimi-g33870), [hisse.net](https://www.hisse.net/haber/kordsdan-yuzde-1800luk-bedelsiz-tescil-tarihi-belli-oldu-96302)
- **TUPRS:** [halkarz.com haberi](https://halkarz.com/haberler/tupras-tuprs-yuzde-600-bedelsiz-sermaye-artirimi-karari-aldi/), [Midas](https://www.getmidas.com/midasin-kulaklari/tupras-600-bedelsiz-sermaye-artirimi-nasil-gerceklesecek-p-19698)
- **BIMAS:** [Capital](https://www.capital.com.tr/piyasalar/borsa/bim-bedelsiz-sermaye-artirimi-kararini-duyurdu-yuzde-100), [CNBC-e](https://www.cnbce.com/borsa/bim-yuzde-100-bedelsiz-sermaye-artirimi-icin-spkdan-onay-aldi-h29938)
- **EREGL:** [Midas](https://www.getmidas.com/midasin-kulaklari/eregli-demir-celik-eregl-100-bedelsiz-sermaye-artirimi-nasil-gerceklesecek-p-70845)
- **MIATK:** [Midas](https://www.getmidas.com/midasin-kulaklari/mia-teknoloji-miatk-1200-bedelsiz-sermaye-artirimi-nasil-gerceklesecek-p-29757)
- **CWENE:** [Capital](https://www.capital.com.tr/piyasalar/borsa/cw-enerji-bedelsiz-tarihi-belli-oldu)
- **GOODY:** [Borsanın Gündemi, Goodyear etiketi](https://www.borsaningundemi.com/etiket/goodyear/3)
- **ARMGD:** [Midas](https://www.getmidas.com/midasin-kulaklari/armada-gida-kac-lot-verdi-armgd-halka-arz-sonuclari-p-78265)
- **NETGL:** [CNBC-e](https://www.cnbce.com/borsa/yeni-halka-arz-borsa-istanbula-geliyor-iste-netglnin-ilk-islem-tarihi-h37302)
