# v_G3_a — Bağımsız doğrulama: G3 (XU030 gece pozitif / gün-içi negatif, "açılışta sat, kapanışta kapat")
Tarih: 02.11.2026 · Doğrulayıcı: v_G3_a (ll.py import edilmedi; hizalama/temizlik kendi kodumda: `out/code_v_G3_a/vcommon.py`)
Kaynak iddia: `out/r1_gunici.md` bulgu #5 (görev metninde #6 yazıyor; içerik #5) ve `out/code_gunici/t1b_drift.py`, `t1_overnight.py`.

## 0. Karar: DÜZELT · yeni güven: DÜŞÜK (işlenebilir strateji olarak), istatistiksel spot olgusu olarak ORTA

| Alt iddia | İddia | Benim yeniden üretimim | Sonuç |
|---|---|---|---|
| XU030 gap 2014–2026 her yıl > 0 | 13/13 | **13/13** (en düşük 2016 +9,3, en yüksek 2022 +28,6 bps/gün) | DOĞRU |
| XU030 gün-içi yılların çoğunda < 0 | 11/13 | **10/13** (2017 +1,4; 2021 +3,4; 2022 +14,3). 2021'in işareti temizliğe bağlı: 2 uç gün (22.03.2021, 17.12.2021) dahil edilirse −5,0 → 11/13. XU100: 11/13 | KÜÇÜK DÜZELTME (2021 ≈ 0) |
| "Açılışta sat, kapanışta kapat" brüt +11 bps/gün (t 2,2) | 2014–2026 bağlamında sunulmuş | +11,1 (t 2,06) **yalnızca 2023-12..2026-10 (h1) penceresinde**. 2014–2026: +7,9 (t 3,06); IS 2014–2020: +10,4 (t 3,45); **OOS 2021–2026: +4,9 (t 1,10)** | DÖNEM YANLIŞ ETİKETLİ |
| 8 bps sonrası +3 | — | 2014–2026 −0,1; OOS −3,1; h1 penceresi +3,1 | sadece h1 penceresinde doğru |
| Endeks vadelisinde (2–4 bps) anlamlı olabilir | hipotez | **VİOP F_XU030 2017–2026: brüt +1,0 bps (t 0,30), 10 yılın 5'i pozitif; 2 bps sonrası −1,0, 4 bps sonrası −3,0.** Sadece 2023–2026 rejiminde var: +12,5 (t 2,19; 2023-12..2026-10), 2–4 bps sonrası +8,5…+10,5 | GENELDE YANLIŞ, yalnız son rejimde |
| 47 hissede gap > 0 / gün-içi < 0 | desen var | Spot: gap>0 47/47, gün-içi<0 45/47 (istisna TUPRS +1,5, ASTOR +4,0), t<−2 23/47 (OOS'ta 5/47). **Pay vadelisinde (SSF) 2017–2026: gün-içi<0 sadece 29/47, medyan −2,4 bps** (spot aynı günler −7,5); 2023+: 44/47, medyan −12,6 | spotta doğru, SSF'de yalnız 2023+ |
| Yahoo açılış artefaktı mı? | test edilmemiş | 2023-12+ için HAYIR (07:30 girişi aynı/daha iyi). 2017–2023 için **kısmen EVET**: spot açılışı vadeli açılışına göre ort. +10,4 bps/gün "yüksek" (t 6,05); fark 2024–2026'da kayboluyor (−0,6, t −0,3) | uzun dönem desenin büyük kısmı vadeliyle yakalanamaz |

**Düzeltilmiş iddia:** Yahoo spot XU030'da 2014–2026 gece getirisi 13/13 yıl pozitif (2020+ döneminde bunun ~%60'ı TL faiz taşıması: spot gap − vadeli gap = 13,6 bps vs beklenen carry 10,4), gün-içi 10/13 yıl negatif (2021 ≈ 0). Spot "aç-sat" 2014–2026 brüt +7,9 bps/gün (t 3,1), ama OOS 2021–2026'da +4,9 (t 1,1); +11 bps (t 2,2) rakamı sadece 2023-12..2026-10 penceresine ait. İşlenebilir enstrümanda (VİOP F_XU030, 09:30 açılış → 18:10 kapanış) 2017–2026 brüt yalnızca +1,0 bps (t 0,3) ve maliyet sonrası negatif. Desen vadelide sadece 2023–2026'da var (yıllık +7,7…+12,9 bps; 4/4 yıl). Bu bir rejim bulgusudur, kısa örneklemdir ve güveni DÜŞÜK. 2021–2022'de tam tersi işledi (−14, −25 bps/gün).

## 1. Veri ve tanımlar (bağımsız)
- **Spot:** `data/daily/<SYM>.parquet` (Yahoo), `ldate` = işlem günü. gap = ln(o_t/c_{t−1}), gün-içi = ln(c_t/o_t). Temizlik: fiyat bazlı |ln(c_t/c_{t−1})| > ln(1,105) olan gün NaN (simetrik); |gap| veya |gün-içi| > ln(1,105) olan gün de NaN. o∉[l,h] olan gün NaN (XU030'da 3 gün). Hisselerde temettü bileşeni adj/c oranından alındı (gap_tr). Sonuçlar gap_tr ile aynı.
- **Saatlik/5 dk:** `data/h1`, `data/m5` (bar başlangıcı UTC).
- **VİOP:** `data/viop/viop_YYYYMMDD.csv` (ortak dizin; 2017-03-06 … 2026-10-30, **2.422 gün**; 2017-03 öncesi bülten yok, 404 döndü). 2017–2019 aralığının bir kısmını ben indirdim (`b0_dl_2017_2019.py`, istek arası 0,5 sn, dosya varsa atla); kalanını diğer iki ajanın indiricisi getirdi.
  - Ön vade: VADE TARIHI > TARIH olan en yakın vade (vade günü bir sonrakine geçer). Ön vade, %100 en hacimli sözleşmeyle aynı.
  - f_gap = ln(ACILIS_T / ÖNCEKİ UZLAŞMA_T), f_gapc = ln(ACILIS_T / KAPANIS_{T−1}), f_intra = ln(KAPANIS_T / ACILIS_T). Aynı sözleşme olduğu için roll sıçraması yok.

## 2. Zamanlama denetimi
| Kontrol | Sonuç |
|---|---|
| Yahoo günlük o = açılış müzayedesi mi? | m5 06:55 barı kapanışı = günlük o: XU030, XU100 ve 47 hissede 59/59 gün (%100) |
| Yahoo günlük c | Kapanış müzayedesi (14:55 m5 sürekli fiyatından sonra). Son 59 günde müzayede ort. +3,7 bps (XU030) |
| h1 ilk bar 'o' | Endekslerde %98,7 = önceki kapanış (KULLANILMAMALI). Hisselerde %99,4 = günlük o |
| h1 kış saati | 14:30 barı yok, yani son ~40 dk eksik. Yazın son sürekli fiyat 15:00 UTC, kışın 14:30 UTC |
| VİOP ACILIS saati | ES=F saatlik ile regresyon (n=169, 2024-06+): f_gap ES'in 15→16 UTC (β 0,48, t 2,6), 16→20 (β 0,68, t 5,8) ve 20→06 UTC (β 0,94, t 9,3) pencerelerine yükleniyor. Yani ACILIS **sabah 09:20–09:30 TSİ açılışı**, akşam seansının ilk işlemi değil. ACILIS = ACILIS SEANSI FİYATI: 2023+ günlerin %98'i (açılış seansı 2022 sonunda başlıyor) |
| VİOP KAPANIS saati | ln(KAPANIS/UZLAŞMA) T günü 15→16 ve 16→20 UTC ES'e yüklenmiyor (t 0,6 / 0,1); sd 8 bps. Yani **18:10 normal seans kapanışı**, akşam seansı dahil değil |
| VİOP 2017–2022 ACILIS tutarlılığı | corr(f_gap, S&P_{T−1}) 0,12–0,39, spot gap ile benzer ya da daha yüksek. corr(f_intra, S&P_{T−1}) ≈ 0 (−0,07…+0,06), yani ACILIS ABD bilgisini içeriyor, bayat değil. 2020'de akşam seansı başlangıcında kırılma yok |
| İleriye bakma | Strateji koşulsuz (her gün sat), sinyal bilgisi yok. Tek varsayım dolum fiyatı: spotta açılış müzayedesi, vadelide 09:30 açılış seansı/ilk işlem |
| Vadeli fiyat adımı | Bülten fiyatları 2025Ç1'den itibaren tam sayı. Adım 0,25 → 1,00 puan, endeks 10–16 bin → 0,6–1 bps/tik |

## 3. Spot kanıt (Yahoo, 2014–2026)
**XU030 yıllık (bps/gün):**

| yıl | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gap | 14,7 | 10,2 | 9,3 | 14,3 | 13,1 | 18,7 | 21,8 | 14,1 | 28,6 | 28,0 | 25,6 | 16,3 | 10,4 |
| gün-içi | −4,7 | −17,9 | −5,8 | +1,4 | −21,8 | −10,9 | −13,5 | +3,4* | +14,3 | −15,9 | −13,8 | −11,2 | −5,9 |
| t(gün-içi) | −0,6 | −2,2 | −0,8 | 0,2 | −2,3 | −1,4 | −1,6 | 0,4 | 1,2 | −1,1 | −1,6 | −1,3 | −0,5 |

\* 2 uç gün temizlenmezse −5,0. Tek yılda |t|>2 olan sadece 2015 ve 2018.

- "Aç-sat" XU030 brüt: 2014–2026 +7,92 (t 3,06, NW-t 3,12; medyan +9,3; %1 kırpılmış +7,1; en uç 20 gün çıkarılınca +6,5, t 2,7). Yıl-blok bootstrap %95 GA [+2,4, +12,9]. **İlk yarı (≤2020-05) +11,2 (t 3,5), ikinci yarı +4,7 (t 1,1).** 250 günlük kayan ortalama günlerin %70'inde > 0 (aralık −15…+26).
- IS 2014–2020 +10,4 (t 3,45) / **OOS 2021–2026 +4,9 (t 1,10)**. Kriz pencereleri (Ara-21, Haz-23, Mar-25, Eyl–Eki-26) hariç tam dönem +7,5 (t 2,9). Mar–Nis 2025 ve Eyl–Eki 2026 tek başına +3.100 bps katkı veriyor (toplam 25.350 bps).
- Gap'e koşullu: gün-içi = −6,9 bps (t −2,6) − 0,06·gap. Sabit terim kalıyor, yani desen sadece gap dönüşü değil. Haftanın günü: Salı −16, Çarşamba −17, Pazartesi +4,7 bps.
- 2014 öncesi (açılış verisi şüpheli): 2005–2013 aç-sat +2,1 (t 0,6), 2010–2013 +7,1 (t 1,5). Desen 2014 öncesinde zayıf.
- 47 hisse: gap>0 47/47, gün-içi<0 45/47. Eşit ağırlıklı sepet aç-sat 2014–2026 +9,5 (t 4,1), OOS +7,7 (t 1,9).

**Saatlik ayrıştırma (2023-12..2026-10, XU030, bps/gün, t):** açılış→07:30 **+1,6 (0,8)**, 07:30–08:30 +0,7, 08:30 −2,7 (−2,1), 09:30 −0,6, 10:30 −1,3, 11:30 −0,6, 12:30 +0,1, 13:30 −4,5 (−2,5), 14:30 (yaz) −4,3 (−2,3), son sürekli→kapanış −1,2 (−1,1). Negatif kayma açılış müzayedesinden değil, gün boyu ve son iki saatten geliyor.

Alternatif giriş/çıkış, XU030 brüt (t):
- A açılış→kapanış: 11,2 (2,1)
- B 07:30→kapanış: 12,7 (2,6)
- C 08:30→kapanış: 13,4 (3,1)
- D açılış→son sürekli: 10,1 (1,9)
- F sadece kapanış müzayedesi: 1,2 (1,1; IS +4,9, OOS −3,2)

EW47'de B 17,0 (t 3,6). **Bu pencerede açılış artefaktı yok.**

## 4. VİOP vadeli kanıtı (işlenebilir enstrüman)
**F_XU030 yıllık, aynı günlerde spot ile (bps/gün):**

| yıl | n | f_gap | s_gap | f_gün-içi | s_gün-içi | fark (f−s) | sd f_gap / s_gap |
|---|---|---|---|---|---|---|---|
| 2017 | 208 | 2,5 | 15,0 | +6,8 | −2,8 | +9,6 (t 3,2) | 13 / 45 |
| 2018 | 251 | 0,3 | 13,1 | −13,5 | −21,8 | +8,2 (t 2,3) | 22 / 61 |
| 2019 | 249 | 0,7 | 18,7 | +1,3 | −10,9 | +12,2 (t 2,9) | 15 / 59 |
| 2020 | 250 | 3,7 | 21,8 | +3,8 | −13,5 | +17,3 (t 3,7) | 30 / 80 |
| 2021 | 236 | 3,7 | 13,7 | +15,5 | +7,5 | +8,1 (t 1,6) | 27 / 64 |
| 2022 | 249 | 9,6 | 28,2 | +24,6 | +15,0 | +9,6 (t 1,8) | 44 / 59 |
| 2023 | 247 | 14,2 | 31,0 | −11,3 | −18,9 | +7,7 (t 1,5) | 82 / 105 |
| 2024 | 248 | 9,7 | 25,6 | −13,3 | −13,8 | +0,5 | 41 / 68 |
| 2025 | 250 | 5,8 | 16,3 | −11,9 | −11,2 | −0,7 | 71 / 80 |
| 2026 | 205 | 3,4 | 11,1 | −7,7 | −6,0 | −1,8 | 72 / 72 |

- **Vadeli aç-sat (sat ACILIS, al KAPANIS):**

  | Dönem | Brüt bps/gün (t) | 1 bps sonrası | 2 bps sonrası | 4 bps sonrası | 8 bps sonrası |
  |---|---|---|---|---|---|
  | 2017–2026 (n 2.410) | +1,03 (0,30) | +0,0 | −1,0 | −3,0 | −7,0 |
  | IS 2017–2020 | +1,3 (0,3) | | | | |
  | OOS 2021–2026 | +0,8 (0,2) | | | | |
  | OOS kriz hariç | −0,1 | | | | |
  | 2023-12..2026-10 | +12,5 (2,19) | | +10,5 | +8,5 | +4,5 |

  Pozitif yıl 5/10 (2017 −6,8; 2018 +13,5; 2019 −1,3; 2020 −1,5; 2021 −14,4; 2022 −24,7; 2023 +12,5; 2024 +12,9; 2025 +12,1; 2026 +7,7). Yıl-blok bootstrap GA [−7,3, +8,3], P(≤0) = 0,39. 2023-12..2026-10 penceresinin yıllık Sharpe'ı 2 bps sonrası 1,08, 4 bps sonrası 0,87.
- **Spot–vadeli farkı:** Aynı 2.393 günde spot aç-sat +7,8, vadeli +0,6 bps. Fark (f_gün-içi − s_gün-içi) 2017–2023 boyunca **+10,4 bps/gün (t 6,05)**, 2024–2026'da −0,6 (t −0,3). Fark spot gap kantiliyle monoton artıyor: en düşük kantil −34,5, en yüksek +51,2 bps. 2017–2022'de spot gap'in sd'si vadeli gap'in 2–4 katı. Yorum: o yıllarda endeksin ilk değeri (≈10:00, 30 hissenin müzayede fiyatları) vadelinin 09:30 açılışına göre gürültülü ve aşırı tepkili; gün içinde geri veriyor. Bu bileşen **sadece 30 hisseyi açılış müzayedesinde satan bir sepet işlemcisi** için gerçek olabilir (hisse maliyetleri ve açığa satış kısıtıyla). Vadeliyle yakalanamaz. Neden 2024'te kaybolduğu bilinmiyor; VİOP açılış seansı 2022 sonunda başladı, spot açılış müzayedesi kuralları da değişmiş olabilir (doğrulanmadı).
  - 2017'de vadeli 09:30'da, spot ~10:00'da açılıyordu. 09:30–10:00 arası sistematik bir yükseliş de aynı imzayı verir. Bülten verisiyle ayırt edilemiyor; sonuç her iki yorumda da aynı (vadeli aç-sat 2017–2022'de işlemiyor).
- **Gece tarafı (vadeli = fazla getiri):** Uzun KAPANIS→ACILIS +5,1 bps (t 5,1); IS +1,2 (t 1,7), OOS +7,6 (t 4,9). f_gap 10/10 yıl > 0, ama 2017–2021'de sadece +0,3…+3,7 bps. 2 bps sonrası +3,1, 4 bps sonrası +1,1 (OOS'ta +5,6 / +3,6). Spottaki "13/13 gece pozitif" olgusunun büyük bölümü yüksek faiz döneminde TL carry'sidir (2020-08+: spot gap − vadeli gap 13,6 bps, beklenen carry 10,4 bps; 2024–2026'da fark ≈ carry). Akşam seansı XU030 vadelisinde açık, gece pozisyonu taşınabilir.
- **Diğer endeks vadelileri (aç-sat):**
  - **F_XLBNK** 2019–2026: +8,2 (t 1,44), 8 yılın 7'si pozitif (2022 −5,1), 2023-12+ +11,2 (t 1,4), 4 bps sonrası +4,2. Yıl-blok bootstrap GA [+2,9, +13,4]; 8 blokla iyimser, iid t 1,4 daha gerçekçi. Günlük medyan işlem 277 (2023+ ~600). XU030'dan daha istikrarlı, ama ayrı bir hipotez olarak test edilmeli (çoklu karşılaştırma: 4 endeks).
  - **F_X10XB**: +5,2 (t 1,1), 5/8 yıl.
  - **F_XSD25**: işlem gören sadece 68 gün, kullanılamaz.
- **47 pay vadelisi (SSF, ön vade, işlem sayısı ≥ 20):**
  - 2017–2026: gün-içi<0 29/47, t<−2 4/47, medyan −2,4 bps (spot aynı günler −7,5).
  - 2023+: 44/47 negatif, 15 hissede t<−2, medyan −12,6.
  - EW SSF aç-sat yıllık: 2017 −3,6 · 2018 +20,1 · 2019 −2,2 · 2020 −5,0 · 2021 −7,7 · 2022 −28,1 · 2023 +18,1 · 2024 +13,3 · 2025 +9,6 · 2026 +13,4. Spot aynı günlerde 2017–2022'de sistematik olarak 6–15 bps daha iyi.
  - 2023+ EW +13,6 (t 2,4): 8 bps sonrası +5,6, 15 bps sonrası −1,4. Tek hisse bazında 2023+ brütü 8 bps'yi geçen 32/47, 15 bps'yi geçen 17/47. 2017+ tam dönemde 8 bps'yi geçen sadece 10/47.

## 5. Maliyet gerçekçiliği
- XU030 vadelisi: tik 0,6–1 bps. Sürekli seansta 1 tik spread'i karşılamanın gidiş-dönüş maliyeti ~1 bps. Borsa + Takasbank + aracı komisyonu kurumsal hesapta ~1–2 bps, perakendede 3–6+ bps gidiş-dönüş (aracıya göre değişir, doğrulanmadı). 2–4 bps varsayımı düşük maliyetli hesap için makul. Açılış seansı (müzayede) fiyatından dolum: emir müzayedeye katılırsa mümkün. Müzayede fiyatına kendi etkin de olur; günlük 6,9 milyar TL medyan hacimde küçük pozisyon için önemsiz.
- Yıllık 250 gidiş-dönüş: 3 bps maliyet yıllık ~%7,5 sürüklenme demek. Tam dönem brüt (~%2,6/yıl) bunu karşılamıyor.
- SSF: 8–15 bps varsayımıyla tek hisse bazında anlamlı net kalan yok. Sepet 2023+ 8 bps'de +5,6.

## 6. Karşı argümanlar / sınırlamalar
- 2014–2016 vadeli bülteni yok (borsaistanbul.com'da 2017-03-06 öncesi 404). İddianın 2014–2016 kısmı vadeliyle test edilemedi.
- Vadeli açılışı 09:30, spot açılışı 10:00. 09:30–10:00 içi hareket ile spot açılış müzayedesi aşırılığı bülten verisiyle ayrılamıyor. Vadeli için "10:00'da sat" varyantı test edilemedi (vadeli gün-içi veri yok).
- KAPANIS = son işlem fiyatı. Kapanışta piyasa emriyle 1 tik kayma olası (dahil edildi). UZLAŞMA ile çıkış (kapanış 10 dk ağırlıklı ortalama) sonuçları neredeyse aynı (f_gün-içi_u ≈ f_gün-içi).
- 2023–2026 vadeli bulgusu (4/4 yıl) bu tur dahil aynı veriden keşfedildi; gerçek OOS yok. 2021–2022'de tam tersi işlemesi rejim bağımlılığını gösteriyor (KKM/negatif reel faiz dönemi: gün-içi yükseliş).
- Mekanizma: Küresel literatürde (gece pozitif / gün-içi negatif "tug of war") benzer desen var. TR'de yüksek nominal faiz geceyi mekanik olarak şişiriyor. Gün-içi negatif kısmın 2023+ vadelide de olması, açığa satış kısıtı + bireysel yatırımcının açılışta alım baskısı hipoteziyle uyumlu. Test edilmedi.
- Çoklu test: bu doğrulamada 4 endeks vadelisi + 47 SSF + ~6 giriş/çıkış varyantı bakıldı. XU030 için tek, önceden tanımlı test (iddianın kendisi) raporlandı. XLBNK bulgusu post-hoc.

## 7. Kod (yeniden üretim, hepsi `nice -n 10 python3 -I`)
`/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_a/`
- `vcommon.py`: bağımsız yükleme ve temizlik
- `a1_daily_years.py`: spot yıllar, IS/OOS, 47 hisse
- `a2_h1_segments.py`: saatlik segmentler ve alternatif giriş/çıkış
- `a3_robust.py`: medyan, bootstrap, hafta günü, gap koşullu, temizlik farkı
- `a4_m5_auction.py`: açılış/kapanış müzayedesi kontrolü
- `b0_dl_2017_2019.py`: VİOP indirici
- `b1_viop_parse.py`: bülten ayrıştırma → `res/viop_fut.parquet`
- `b2_viop_xu030.py`, `b3_viop_timing.py`: ACILIS/KAPANIS saat doğrulaması (ES)
- `b4_viop_all.py`: tüm endeks vadelileri + 47 SSF
- `b5_viop_bt.py`: vadeli backtest, maliyet, yıllar, bootstrap
- `b6_carry.py`: carry ayrıştırması
- `b7_open_check.py`, `b8_spot_vs_fut.py`: spot–vadeli açılış farkı

Çıktılar `res/` altında: a1_*.csv, a2_variants.csv, a4_m5.csv, b4_all.csv, b4_ssf_years.csv, b5_bt.csv, b5_*_years.csv, b8_disc_years.csv, *.log.

TradingView: `BIST:XU030D1!` (ön ay sürekli; roll sıçraması var), `BIST:XU030`, `BIST:XLBNKD1!`, `BIST:X10XBD1!`, pay vadelisi `BIST:<KOD>1!` (ör. `BIST:GARAN1!`).
