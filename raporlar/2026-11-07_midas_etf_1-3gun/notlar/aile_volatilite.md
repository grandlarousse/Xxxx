# Aile: volatilite (VXX, VIXY, UVXY, UVIX, SVXY, SVIX, VIXM) — 1-3 günlük işlem değerlendirmesi

Hazırlanma: 07.11.2026. Veri sonu: 06.11.2026 kapanışı. Kod: `kod/ajan_volatilite/`, tablolar: `sonuclar/aile_volatilite/`.
Tüm sayılar 2.500 USD pozisyon maliyetiyle (12 bp komisyon + kademeli makas; bu ailede 16-17 bp, VIXM 27 bp) nettir, aksi yazılmadıkça.
IS = 2021 sonuna kadar, OOS = 2022 ve sonrası. "t" = işlem başı net getirinin t istatistiği.

## 0. Kısa sonuç

* **Kabul eşiğini geçen tek kural (düşük güven): volatilite_S1.** Koşul: RSI(2)(SVXY) < 10 ve SVXY > SMA200 ise SVXY al, 2 gün tut.
  SVXY C0 h=2: n=59, net +157 bp, t=3,16. IS'te +144 bp (n=19, t=1,15), OOS'ta +164 bp (t=3,64). Yılların 5/8'i pozitif, maxDD -%14,5, en kötü işlem -1.375 bp (Şubat 2020).
  O1 h=2 (ertesi açılışta gir): +108 bp, t=2,53. **C1'de (bir gün gecikmeli girişte) kenar yok: -28 bp.** Kenar sinyalden sonraki ilk 1-2 günde.
  Bu sonuç 3.075 testlik BH-FDR'den geçiyor (q=0,10). **Ancak uzun dönem vekil testinde (2010-2018, n=76) kenar sıfır**: kazanç 2019 sonrası, ağırlıkla 2021 ve 2023-2026'dan geliyor. Güven bu yüzden **düşük**.
* **Uzun vol (VXX/VIXY/UVXY/UVIX/VIXM) için 1-3 günlük hiçbir long kural pozitif ve anlamlı değil.** Rejim değişimi, VIX sıçraması, backwardation ve VIX gerilmesi girişlerinin hepsini test ettim. Sonuçlar çoğunlukla negatif, örneğin VXX C1 h=1 rejim girişi -180 bp, t=-2,1. Uzun vol ancak sigorta olarak, bilerek kaybedilen bir prim gibi kullanılabilir.
* **Kontango "taşıma" kuralları (VIX/VIX3M<0,90 iken SVXY, VO01) gerçek ETF verisinde negatif.** Vekil 2009-2021'de çalışmış, 2022 sonrasında çalışmıyor. Elendi.
* **Doğrulanmış gecikmeli öncü yok** (SVXY, SVIX, VXX). Genel taramada 0, ek 144 testte FDR'yi geçen 0. VIX, VIX vadelisi, VVIX ve S&P vadelisi yalnız eşzamanlı sürücü ve gerçek zamanlı izleme aracıdır.
* **Bugünkü durum (06.11.2026 kapanışı):** VIX=25,64, VIX/VIX3M=1,042 (backwardation), VIX9D/VIX=1,06, VVIX=122. SVXY (54,72) SMA200'ün (55,93) altında, RSI2=21. **S1 sinyali yok.** Backwardation döneminde kısa vol ürünlerinin 1-3 günlük dağılımı iki kat geniş (bkz. §4.2).
* **PTP/K-1 uyarısı:** SVXY, UVXY, VIXY ve VIXM ProShares Trust II ürünleridir (emtia havuzu, K-1). SVIX ve UVIX'in Volatility Shares Trust bünyesinde K-1 vermesi muhtemel (doğrulanmadı). Midas'ta PTP ibaresi görünüyorsa ve satışta 2024 UNG vakasındaki gibi **%10 brüt kesinti** uygulanırsa her işlem ~-1.000 bp kaybeder ve S1 tamamen çöker. İşlemden önce Midas'tan yazılı teyit alınmalı. VXX bir ETN'dir (Barclays): PTP değil, ancak ihraççı kredi riski ve ihraç askıya alma riski (Mart 2022) var.

## 1. İşlenebilirlik ve kopya grupları (tarama.csv)

| ETF | TV | Yapı | Medyan $ hacim (mn) | Maliyet bp | 1g vol bp | maliyet/vol | 1g en kötü (1y) | Not |
|---|---|---|---|---|---|---|---|---|
| SVXY | CBOE:SVXY | -0,5x kısa vade (ProShares Trust II, K-1) | 85,0 | 16,0 | 202 | 0,079 | -%15,4 | 2018-02-27'de -1x'ten -0,5x'e indi. Veri 2018-09'dan başlıyor, yani tamamı -0,5x dönemi |
| SVIX | CBOE:SVIX | -1x kısa vade (Volatility Shares) | 60,1 | 16,9 | 389 | 0,044 | -%29,9 | 2022-03+; Şubat 2018 tipi olayda ~%90+ kayıp potansiyeli |
| VXX | CBOE:VXX | +1x ETN (Barclays) | 214,6 | 16,6 | 393 | 0,042 | -%9,6 | PTP değil; kredi riski |
| VIXY | CBOE:VIXY | +1x ETF (ProShares Trust II) | 69,6 | 16,8 | 394 | 0,043 | -%9,9 | VXX'in kopyası (aynı endeks) |
| UVXY | CBOE:UVXY | +1,5x (ProShares Trust II) | 237,4 | 16,3 | 596 | 0,027 | -%15,0 | 2018'de 2x'ten 1,5x'e indi |
| UVIX | CBOE:UVIX | +2x (Volatility Shares) | 158,3 | 16,0 | 789 | 0,020 | -%19,5 | -35 bp/gün koşulsuz kayıp |
| VIXM | CBOE:VIXM | +1x orta vade (ProShares Trust II) | 3,6 | 27,0 | 118 | 0,228 | -%4,1 | Düşük likidite, yüksek maliyet |

**Kopya grupları.** Ailede bağımsız dayanak yalnız iki tane: (i) S&P 500 VIX kısa vadeli vadeli endeksi (VXX, VIXY, UVXY, UVIX, SVXY, SVIX: aynı endeksin ±k katı) ve (ii) orta vadeli endeks (VIXM).
"SVXY'de çalışıp VXX'te ters yönde görünmesi" ya da "SVIX'te daha güçlü çıkması" **bağımsız kanıt değildir**. Bunlar aynı endeksin ölçeklenmiş halidir. Ailede tutarlılık bu yüzden üç yerden kontrol edildi: farklı ürün dönemleri (SVXY 2018+, SVIX 2022+), sentetik uzatma (SVXY_EK: 2017-07..2018-09 için VIXY'den -0,5x) ve uzun dönem vekil (VEKIL, 2009-09+).

**Uzun dönem vekil (VEKIL).** Kısa vadeli endeksin günlük log getirisi şöyle modellendi: dlog VIX, dlog VIX3M, dlog VIX6M ve önceki günün log(VIX/VIX3M) değeri. Katsayılar **yalnız** VIXY 2017-07..2021 verisiyle tahmin edildi. 2022-2026 örneklem dışı korelasyonu 0,967. Ortalama sürüklenme -21,9 bp (gerçek), vekilde -21,6 bp. -0,5x vekil ile gerçek SVXY'nin günlük korelasyonu 0,965. Açılış fiyatı olmadığı için vekilde yalnız C0 ve C1 hesaplanabildi. Vekil bir modeldir, işlem görmez; destekleyici kanıt olarak kullanıldı (`vlib.proxy_vxx`).

## 2. Genel kütüphane (genel_tum.csv) — aile içinde

* Aile ETF'leri için 2.079 test (31 sinyal × 3 mod × 3 h, artı erken çıkış). Aile içi BH-FDR'yi (q=0,10) 115 test geçiyor. Bunların **büyük çoğunluğu negatif**: uzun vol tutmanın ve VIXM maliyetinin yarattığı kayıp. Örnekler: VIXM VX_kontango_09 O1 h1 -24 bp (t=-7,3), VXX CA_cum O1 h3 -124 bp (t=-3,9).
* Pozitif tarafta aile içinde tutarlı tek sinyal **MR_rsi2_lt10_ust200** (kısa vol ürününde RSI2 dibi). SVXY C0 h2 +157 (t=3,16), SVIX C0 h2 +297 (t=4,06, yalnız OOS). Ayna yönü de tutarlı: VXX'te RSI2>90 sonrası VXX düşüyor (MO_rsi2_gt90 VXX O1 h3 -220 bp). Ama bu aynı dayanağın tersidir, bağımsız kanıt sayılmaz. Bu sinyali §3.1'de derinlemesine test ettim.
* MR_3gun_dusus (SVXY C0 h2 +112, t=2,6) S1 ile büyük ölçüde örtüşüyor ve daha zayıf (O1 h2 +44 t=1,2, C1 h2 +7). Ayrı strateji yapılmadı.
* CA_cum (Cuma sinyali: Pazartesi açılışta al) SVIX O1 h1 +62 (t=2,9). Bu, Pazartesi gün içi etkisidir, §3.3'te inceledim: yalnız 2022 ve sonrasında var, IS'te yok.
* VX_* sinyalleri (genel kütüphanede) aile içinde FDR'den geçmiyor. VX_kontango_09 SVXY'de negatif (C0 h1 -15 bp, t=-2,9).

## 3. Aileye özel hipotezler (kendi kodum)

Betikler: `hipotez_testleri.py` (843 test), `aday_rsi2.py` (48 test + 60 komşu parametre), `ek_testler.py` (45 test), `olcumler.py` (ölçüm tabloları), `leadlag_vol.py` (144 lead-lag testi).
**Toplam strateji testi: 2.079 (genel kütüphane, aile ETF'leri) + 996 (bu ajan) = 3.075.** Birleşik BH-FDR q=0,10 eşiği p ≤ 0,00364. Geçen 113 testin 105'i negatif. Pozitif 8 testin tamamı RSI2-dip ailesinden (SVXY C0 h2 ve SVIX varyantları): `sonuclar/aile_volatilite/tum_testler_fdr.csv`.
Parametre taraması yapılmadı. Eşikler hipotezler.csv ve görev yönlendirmesinden alındı. Komşu parametreler yalnız raporlandı.

### 3.1 volatilite_S1: RSI2 dibi + SMA200 (kabul, düşük güven)

| Araç / mod | h | n | net bp | t | IS net (t, n) | OOS net (t) | yıl+ | maxDD | en kötü |
|---|---|---|---|---|---|---|---|---|---|
| SVXY C0 | 1 | 73 | 82 | 2,44 | 46 (0,56; 24) | 100 (3,22) | 0,62 | -%18,9 | -965 |
| **SVXY C0** | **2** | **59** | **157** | **3,16** | **144 (1,15; 19)** | **164 (3,64)** | **0,62** | **-%14,5** | **-1.375** |
| SVXY C0 | 3 | 55 | 106 | 1,59 | 69 | 122 | 0,62 | -%22,8 | -1.257 |
| SVXY O1 | 2 | 59 | 108 | 2,53 | 107 (1,11) | 108 (2,46) | 0,75 | -%13,6 | -794 |
| SVXY C1 | 1 | 59 | 47 | 1,51 | 86 | 28 | 0,62 | -%12,6 | -818 |
| SVXY C1 | 2 | 55 | -28 | -0,51 | -20 | -31 | 0,50 | -%37,5 | -1.234 |
| SVIX (SVXY sinyali) C0 | 2 | 39 | 354 | 4,50 | — | 354 | 1,00 | -%6,8 | -683 |
| SVIX (SVXY sinyali) O1 | 2 | 39 | 259 | 3,45 | — | 259 | 1,00 | -%8,9 | -889 |
| SVXY_EK (2017-07+) C0 | 2 | 63 | 134 | 2,68 | 82 (0,72) | 164 | 0,56 | -%25,2 | -1.375 |
| VEKIL -0,5x (2010+) C0 | 2 | 135 | 38 | 1,11 | 11 (0,25; 94) | 100 (2,33) | 0,59 | -%39,2 | -2.330 |
| VEKIL -0,5x, 2010-2018 alt dönemi C0 | 2 | 76 | 0 | 0,00 | | | | | |
| VEKIL -0,5x C1 | 2 | 122 | -22 | -0,63 | 4 | -77 | 0,53 | | |

* Maliyet duyarlılığı (SVXY C0 h2): 1.000 USD'de 139 bp, 2.500 USD'de 157 bp, 10.000 USD'de 166 bp. O1 h2 için sırasıyla 90, 108 ve 117 bp.
* Yıllara göre (C0 h2, net toplam bp): 2019 -647 · 2020 -1.042 · 2021 +4.418 · 2022 -681 · 2023 +2.339 · 2024 +1.236 · 2025 +1.146 · 2026 +2.511.
* Kuyruk dönemleri: Mart 2020'de 1 işlem, -1.375 bp (sinyal 21.02.2020, çıkış 25.02.2020). Ağustos 2024'te 1 işlem, +355 bp. Şubat 2018, Nisan 2025 ve Kasım 2026'da pozisyon yok (filtre SMA200 altındaydı ya da sinyal yoktu).
* Sinyal günündeki VIX düzeyine göre ortalama net: VIX≤15 iken +7 bp (n=8), 15-20 arası +71 (n=26), 20-25 arası +243 (n=19), >25 iken +460 (n=6). Tanımlayıcı bilgidir, filtre olarak kullanılmadı.
* Komşu parametreler (SVXY_EK h=2, `aday_rsi2_komsu.csv`): RSI<10 yerel tepe. RSI<5 ve SMA200 ile C0 +79 (t=0,96). RSI<15 ve SMA200 ile C0 +48 (t=1,29, IS -58). SMA100 ile C0 +86 (t=1,79). Filtresiz C0 +33 (t=0,86). **Sonuç eşik ve filtreye duyarlı.**
* Mekanizma: kısa vadeli VIX vadelisi iki günde sert yükselir. Uzun vadeli sakin rejimde (SVXY>SMA200) bu yükselişin bir kısmı 1-2 günde geri verilir (vol risk primi ve ortalamaya dönüş). 2022 sonrasında vol sıçramalarının daha kısa sürdüğü gözlemiyle uyumlu. 2010-2018 vekilinde bu etki görülmüyor.
* Kabul ölçütleri: net>0 ✓, t≥2 ✓ (C0 3,16; O1 2,53), IS>0 ve OOS>0 ✓, yıl+ %62,5 ✓ (sınırda), n≥40 ✓, O1'de brüt kenar>0 ✓, FDR ✓ (yalnız C0 h2).
  Aleyhte olanlar: C1 çalışmıyor (kenar ilk günlerde), IS'te t=1,15 ve n=19 zayıf, uzun dönem vekilde 2010-2018'de kenar yok, parametreye duyarlı. **Bu nedenle güven: düşük.**

### 3.2 Vade yapısı, sıçrama ve VVIX hipotezleri (elendi)

Hücreler: net bp (t) n. Ana araç SVXY (kısa vol long) ve VXX (uzun vol long). Ayrıntı: `hipotez_testleri.csv`.

| Hipotez | Sonuç |
|---|---|
| VO01: VIX/VIX3M<0,90 ve VIX<SMA10 → SVXY, en çok 3 gün, oran ≥1 olursa erken çık | SVXY C0 -21 (-1,35) n326 · O1 -29 (-1,95) · C1 -22 (-1,35). Vekil -0,5x C0: IS +22, OOS -13. **2022+ çalışmıyor** (Quantpedia'daki "örneklem dışı hafif negatif" bulgusuyla uyumlu) |
| H_kont09 (VIX/VIX3M<0,90 → SVXY) | SVXY C0 h3 -12 (-0,8) · O1 h1 -19 (-4,5). Gün içi kayıp, gece kazanç: taşıma işlem maliyetini karşılamıyor |
| VO02: backwardation (≥1,00) → SVXY ortalaması negatif mi? | Ortalama ≈0 (SVXY 3 günlük ileri getiri -0,0 bp). **Ancak kuyruk 2 kat**: std 702 bp (R3M<0,95'te 310), %1'lik dilim -2.412 bp (-1.053'e karşı). Risk kuralı olarak geçerli, getiri kuralı olarak geçersiz |
| VO03: VXX/VIXY/UVXY/UVIX koşulsuz kaybı | Günlük ort: VXX -9,6, VIXY -11,1, UVXY -18,4, UVIX -34,5 bp. 3 günlük: VXX -32, UVIX -121 (NW t -2,0). 0,95≤R3M<1 bölgesinde en kötü (VXX 1g -53, t -2,0). R3M≥1'de ≈0 (VXX +36, t 0,6). Al-tut maxDD %-99,6 / %-99,99 |
| VO04: backwardation → kontango dönüş günü → SVXY 3 gün | SVXY C0 h1 +62 (1,5) n49 · O1 h1 +59 (1,6) · C1 h1 -38 (-0,9) · C0 h3 +53 (0,6). Vekil C1 h3 +96 (1,8). Anlamlı değil |
| VO05: VIX/VIX3M≥1,05 → SPY/QQQ 3 gün | SPY O1 h3 +50 (0,76) n34 · QQQ O1 h2 +56 (1,32). Anlamlı değil |
| VO06: kaldıraç sapması e_h = r_ETF - k·r_VXX | UVXY 3g -4,4 bp (t -0,7) · UVIX -17,6 (-1,5) · SVIX -14,4 (-2,0) · SVXY ≈ -1. En oynak %20'lik dilimde UVXY -33 bp/3g. Yönü teoriyle uyumlu, büyüklüğü 1-3 günde küçük |
| VIX sıçraması ≥%15 / ≥%20 → SVXY (dönüş) | SVXY: tüm mod/h'de \|t\|<1,1 (ör. %20 C0 h1 +67 (1,0) n49, C1 h1 -21). SVIX O1 h2 +324 (2,0) n18, yalnız 2022+. Elendi |
| VIX sıçraması → VXX/UVXY (devam) | VXX %20: C0 h1 -109, O1 h3 -121, C1 h1 -42 (hepsi negatif). UVIX %15 O1 h2 -496 (-2,4). **Devam yok, kayıp** |
| Rejim değişimi (oran 1'i yukarı keser) → VXX/UVXY | VXX C0 h1 +74 (0,6; VIX 16:15'te kapandığı için C0 iyimser) · O1 h1 +68 (0,8) · O1 h2 -102 · C1 h1 **-180 (-2,07)** · UVXY C1 h1 -284 (-1,96). Kazanma oranı %24-48. **Kanıt: rejim girişlerinde uzun vol 1-3 günde çoğunlukla kaybettiriyor** |
| VIX ≥ 1,20×SMA10 (Schaeffer) → SVXY | SVXY C1 h1 +64 (1,4), C1 h2 -44, IS negatif. SVIX C1 h1 +330 (3,1) yalnız 2022+. Tutarsız |
| VIX9D/VIX <0,90 → SVXY · >1,00 → VXX | SVXY O1 h1 -20 (-4,0). VXX tarafı negatif (-22..-55). Elendi |
| VVIX ≥1,10×SMA10 · VVIX +%10 → SVXY | \|t\|≤1,5. VVIX sıçraması C1'de negatif (SVXY C1 h1 -69). Elendi |

### 3.3 Ek (sonradan bakılan) testler: test sayısına eklendi

* **E1 "gergin bölge" (0,95≤VIX/VIX3M<1,00 → SVXY):** C0 h3 +57 (1,36) n141, O1 h3 +49 (1,28), C1 h1 +7. Vekil C0 h1 +2. Anlamlı değil, elendi.
* **E2 Pazartesi gün içi (Pazartesi açılışta al, aynı gün kapanışta sat):** SVXY tüm dönem +2 bp (t=0,25). IS -22, OOS +18 (t=1,98). SVIX OOS +48 (t=2,62). Ayna VXX OOS -86 (t=-4,46).
  Kırpılmış OOS ortalaması SVXY'de +36 bp brüt, yani tek bir uç güne bağlı değil. Yıllara göre (brüt): 2018 -71, 2019 -20, 2020 +20, 2021 0, 2022 +20, 2023 +74, 2024 +1, 2025 +50, 2026 +26.
  **2022 sonrası bir rejim gibi görünüyor, IS'te yok.** Kabul eşiğini geçmiyor (IS>0 değil). İzlenebilir bir gözlem olarak not edildi.
  VIXM'de Pazartesi gün içi her iki dönemde de negatif (-46 bp net, t=-6,45): uzun vol ürününü Pazartesi açılışta almak sistematik olarak kötü.

## 4. Kuyruk riski (mutlaka okunmalı)

### 4.1 ETF'lerin kendi en kötü hareketleri (`olcum_kuyruk.csv`)

| ETF | 1 gün | 2 gün | 3 gün | Al-tut maxDD |
|---|---|---|---|---|
| SVXY | -%21,4 (05.08.2024) | -%30,7 | -%33,8 | -%62 (Mart 2020) |
| SVIX | -%38,9 (05.08.2024) | -%52,2 | -%56,4 | -%79 (Nisan 2025) |
| VXX | -%20,6 (09.04.2025) | -%22,1 | -%27,3 | -%99,6 |
| UVXY | -%31,6 (09.04.2025) | -%33,7 | -%38,9 | -%99,99 |
| UVIX | -%43,8 (09.04.2025) | -%46,5 | -%54,7 | -%99,99 |
| VIXM | -%14,9 (06.08.2024) | -%23,2 | -%22,6 | -%73 |

Olay dönemleri (dönem içindeki toplam getiri): Mart 2020'de SVXY -%53. Ağustos 2024'te SVXY -%18, SVIX -%39. Nisan 2025'te SVXY -%22, SVIX -%44. Kasım 2026'da (02-06.11) SVXY -%10, SVIX -%21; 05.11.2026'da SVXY -%15,4, SVIX -%29,9.
**Şubat 2018:** endeks 05.02.2018'de NAV bazında yaklaşık +%96 sıçradı. O dönemin -1x ürünleri (XIV, eski SVXY) %90'ın üzerinde kaybetti. Bugünkü -0,5x yapıyla NAV bazında tahmini kayıp ~-%45-50. VIXY kapanışlarından türettiğim -0,5x sentetikte 01-08.02.2018 kaybı -%32. Bu rakam iyimser, çünkü 16:00 ET kapanışı 16:15'teki sıçramayı tam yansıtmıyor.
**SVIX -1x olduğu için Şubat 2018 tipi bir olayda neredeyse tamamen silinebilir.** Bu yüzden S1 için SVXY önerilir, SVIX yalnız küçük pozisyonla.

### 4.2 Rejime göre dağılım (VO02/VO03, `olcum_vo02_vo03_rejim.csv`)

SVXY'nin 1 günlük getirisi VIX/VIX3M<0,95 iken std 198 bp, %1'lik dilim -682 bp. R3M≥1 iken std 449 bp, %1'lik dilim -1.515 bp. **Backwardation'da gecelik kısa vol taşımak, ortalama getiriyi değiştirmeden riski iki katına çıkarıyor.**

## 5. Lead-lag

* **(a) Eşzamanlı sürücüler (öncü DEĞİL)**, kaynak leadlag_sweep, son 1 yıl. SVXY: VIX günlük log değişimi corr -0,905 (beta -0,225); VVIX -0,898; SPY +0,833 (beta 2,0); VIX/VIX3M değişimi -0,825; QQQ +0,739.
  SVIX'te aynı sıra (SPY beta 3,96). VXX: VIX +0,909 (beta 0,417), VVIX +0,901, SPY -0,839 (beta -3,72).
  Asıl dayanak VIX vadelileridir (CBOE:VX1!, CBOE:VX2!). Endeks her gün 1. aydan 2. aya kayan bir karışım tutar. Bu ikisi için günlük veri setimde yok, korelasyon hesaplanmadı.
* **(b) Gecikmeli öncüler: doğrulanmış gecikmeli öncü yok.** Genel taramada (36 ETF, VIX, VVIX, OVX, GVZ, BTC 16:00 ET, faizler) ailede FDR'yi geçen 0. Ek 144 testte de 0 geçti. Bu testler durum değişkenlerini (VIX/VIX3M düzeyi ve değişimi, VIX9D/VIX, VIX gerilmesi, VVIX/VIX), SPY/QQQ/BTC getirilerini ve 10 yıllık faiz değişimini kapsıyor. Kendi gecikmesi kontrol edildi, Newey-West kullanıldı, C0 ve O1 hizalaması ayrı bakıldı.
  En güçlü (geçmeyen) adaylar: VXX ← VVIX/VIX oranı (O1 h1 t=3,17; IS 2,05, OOS 2,72; 1 sd'de 22 bp, yani maliyetin 1,3 katı; p=0,0015 > FDR eşiği). SVXY ← QQQ getirisi (h3 C0 t=-2,89; IS -2,33, OOS -1,86): QQQ'nun yükseldiği günden sonraki 3 günde SVXY hafif geri veriyor.
  Not: VIX 16:15 ET'de kapandığı için C0 hizalamasında VIX tabanlı "öncülük" kısmen 15 dakikalık ileri bakıştır. O1 sonuçları temizdir.
* **(c) Gerçek zamanlı izleme (açılış boşluğu için; öncü değil):** CBOE:VX1! ve CBOE:VX2! (VIX vadelileri neredeyse 24 saat işler, ETF'lerin dayanağıdır). CME_MINI:ES1! ve CME_MINI:NQ1! (S&P ve Nasdaq vadelileri). FX_IDC:USDJPY (taşıma işlemi çözülmesi ve risk iştahı; 5 Ağustos 2024 örneği). VIX vadelisi ETF açılmadan önce yükselmişse, SVXY/SVIX açılışta aşağı boşluk yapar.
  Pratik kontrol: TR saatiyle 12:00-17:30 arası (pre-market) VX1! değişimine bakın. Kabaca SVXY açılış boşluğu ≈ -0,5 × (VX1!/VX2! karışımının % değişimi).

## 6. İzleme listesi kararı

| ETF | Karar | Gerekçe |
|---|---|---|
| SVXY | **kabul** | S1'in işlem aracı. 85 mn $ hacim, maliyet/vol 0,08, -0,5x yapı ailede kuyruk riski en düşük kısa vol ürünü. PTP/K-1 riski var (önce Midas teyidi) |
| SVIX | yedek | S1'in agresif varyantı (2x duyarlılık, 2022+ verisi güçlü). Şubat 2018 tipi olayda yok olma riski. PTP muhtemel |
| VXX | yedek | Uzun vol gerekiyorsa tek ETN (PTP değil), en likit 1x araç. **1-3 günlük long kuralların hiçbiri pozitif değil**, yalnız koruma/sigorta amaçlı. Kopyası VIXY'ye tercih edilir |
| VIXY | red | VXX'in kopyası; daha az likit; ProShares Trust II (PTP riski) |
| UVXY | red | 1,5x; -18 bp/gün koşulsuz kayıp; rejim/sıçrama girişleri negatif; PTP riski |
| UVIX | red | 2x; -35 bp/gün; 1 günde -%44 görülmüş; tüm long kurallar negatif |
| VIXM | red | 3,6 mn $ hacim, 27 bp maliyet (maliyet/vol 0,23); kural yok; Pazartesi açılış etkisi negatif |

## 7. Sınırlamalar

* Gerçek ETF geçmişi kısa: SVXY 2018-09+, SVIX/UVIX 2022-03+. Vekil endeks bir modeldir, açılış fiyatı yoktur.
* SVXY'nin 2018-02 öncesi -1x verisi elimde yok. Şubat 2018 yalnız sentetik ve vekil ile temsil edildi. Gerçek NAV kaybı bu serilerin gösterdiğinden büyük olurdu.
* C0 girişleri kapanış fiyatını kullanır. Midas'ta MOC/LOC olmadığı için pratikte 23:50-23:59 (TR, kış) arasında emir verilir. VIX tabanlı sinyallerde 16:15 kapanışı ayrıca ileri bakış yaratır; S1 ise SVXY'nin kendi fiyatına dayandığı için bu etki yalnız son dakika kaymasıyla sınırlı.
* Makas kademeli bir tahmindir. Volatilite ürünlerinde stres günlerinde makas çok açılır ve bu backtestte yok.
* Vergi (TL bazında kur farkı), PTP kesintisi ve Midas'ta bu ürünlerin listelenip listelenmediği doğrulanmadı.
* Midas'ın zarar-durdur emri %2 kayma limitli stop-limittir. Bu ürünlerdeki %15-40'lık boşluklarda dolmayabilir. Backtestlerde stop yok.

## 8. Tekrar üretim

```
python3 -I kod/ajan_volatilite/hipotez_testleri.py   # 843 test -> hipotez_testleri.csv
python3 -I kod/ajan_volatilite/aday_rsi2.py          # S1 araç/mod/komşu -> aday_rsi2_*.csv
python3 -I kod/ajan_volatilite/ek_testler.py         # E1/E2 -> ek_testler.csv
python3 -I kod/ajan_volatilite/olcumler.py           # VO02/VO03/VO06, hafta günü, kuyruk
python3 -I kod/ajan_volatilite/leadlag_vol.py        # lead-lag ek testleri
python3 -I kod/ajan_volatilite/strateji_S1.py        # S1 tüm sayıları + FDR + güncel durum (çıktı: strateji_S1_cikti.txt)
```
