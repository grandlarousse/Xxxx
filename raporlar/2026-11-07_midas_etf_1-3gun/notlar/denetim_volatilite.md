# Denetim: volatilite ailesi (bağımsız denetçi)

Hazırlanma: 07.11.2026. Veri sonu: 06.11.2026. Denetim kodu: `kod/denetim_volatilite/`. Tablolar ve ekran çıktıları: `sonuclar/aile_volatilite/denetim/`.
JSON: `sonuclar/aile_volatilite/denetim.json`. İşlem simülasyonunu `lib.trades`, `lib.evaluate` ve `lib.rsi` kullanmadan kendim yazdım (`dlib.py`: Wilder RSI, kendi çakışmasız işlem döngüsü, maliyet `tarama.csv`'deki makastan). Fiyatları yalnız `lib.load` ile okudum.

## 0. Hüküm

* **volatilite_S1 (RSI2(SVXY)<10 ve SVXY>SMA200 ise SVXY al, 2 gün tut): ZAYIF.** Sayılar birebir yeniden üretiliyor ve kodda ileriye bakış yok. Rastgele giriş testleri de güçlü. Buna karşın dört nokta kuralı "doğrulandı" düzeyine taşımıyor:
  (1) BH-FDR geçişi bir yapay sonuç: geçen 113 testin 105'i, uzun vol ürünlerinin bilinen yapısal kaybından gelen negatif testler. Tek yönlü testte (strateji kârlı mı sorusu) SVXY C0 h2 FDR'yi geçmiyor, Bonferroni'yi de geçmiyor.
  (2) IS kanıtının tamamı 2021'den geliyor. 2021 çıkarılınca IS -241 bp, tüm dönem t=1,91.
  (3) Uzun dönem vekilde 2010-2018 arasında kenar sıfır ve komşu parametreler de sıfır ya da negatif.
  (4) Kuyruk riski: kural, Şubat 2018 çöküşüne RSI2=12,4 ile kıl payı girmemiş. Ajanın "Şubat 2018: pozisyon yok" ifadesi, kuralın olaydan kaçtığını değil verinin olmadığını gösteriyor.
* **Lead-lag:** "Doğrulanmış gecikmeli öncü yok" sonucu doğru. Öne çıkan iki aday (VVIX/VIX → VXX, QQQ → SVXY) yeniden hesaplandı ve ikisi de çürük.
* **Kaçırılan:** S1 sinyalinin getirisinin büyük kısmı hisse betası (SPY'ye beta 2,28, R²=0,84). Aynı SVXY sinyaliyle PTP olmayan QQQ/QLD alınabilir: benzer t, yarı kuyruk. Kanıt aynı 59 olay olduğu için bağımsız değil. Kuyruk riski ise ajanın yazdığından ciddi.

## 1. volatilite_S1: kod ve zamanlama (mercek A)

**Yeniden üretim (kendi motorum, 2.500 $ maliyet 16 bp):**

| Mod | h | n | brüt | net | t | IS net (t, n) | OOS net (t) | kazanma | PF | maxDD | en kötü |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | 1 | 73 | 98,3 | 82,3 | 2,44 | 45,7 (0,56; 24) | 100,2 (3,22) | 0,71 | 2,04 | -%18,9 | -965 |
| **C0** | **2** | **59** | **173,3** | **157,3** | **3,16** | **143,6 (1,15; 19)** | **163,8 (3,64)** | 0,71 | 2,88 | -%14,5 | -1.375 |
| C0 | 3 | 55 | 121,5 | 105,5 | 1,59 | 68,6 | 122,0 | 0,69 | 1,72 | -%22,8 | -1.257 |
| O1 | 2 | 59 | 123,7 | 107,7 | 2,53 | 106,7 (1,11) | 108,1 (2,46) | 0,68 | 2,27 | -%13,6 | -794 |
| C1 | 2 | 55 | -11,7 | -27,7 | -0,51 | -19,6 | -31,4 | 0,55 | 0,82 | -%37,5 | -1.234 |

* Ajanın işlem listesiyle karşılaştırma: 59/59 aynı sinyal günü, brüt fark < 1e-12. lib.rsi ile Wilder RSI'ın (SMA tohumlu, TradingView `ta.rsi` tanımı) 30. günden sonraki farkı 0.
* İleriye bakış kontrolü: sinyalin girdileri yalnız SVXY'nin kendi t kapanışı (RSI2, SMA200). VIX'in 16:15 kapanışı, BTC ya da Hazine verisi kullanılmıyor. Girişler C0'da t kapanışında, O1'de t+1 açılışında, C1'de t+1 kapanışında. Çıkışlar doğru günde. Çakışma yok: pozisyon kapanmadan yeni sinyal alınmıyor, çıkış günündeki sinyal yeni işlem açabiliyor. Maliyet her işlemden bir kez düşülüyor. **Kod hatası bulmadım.**
* SVXY verisi 2018-09-18'de başlıyor. SMA200 ısınması nedeniyle ilk sinyal 2019-07-31'de. Bölünme ya da temettü artefaktı yok (raw/adj oranı 1,0). En büyük günlük hareketler gerçek olaylar.
* **En iyi 5 işlem** (net bp): 12.05.2021 (+1.075; enflasyon şoku sonrası), 16.10.2025 (+816), 19.07.2021 (+728), 29.01.2021 (+695; GameStop dalgası), 20.01.2026 (+609). Hiçbiri `veri_kalitesi.csv` ya da `veri_duzeltmeleri.csv`'de değil ve tek bir olaya yığılma yok. Ancak 5 işlemden 3'ü 2021'de.
* **C0 uygulanabilirliği:** Midas'ta MOC yok, sinyal kapanıştan 10-20 dk önceki fiyatla hesaplanmalı. Bunu simüle ettim: son ~20 dakikanın gürültüsü × 1,3, 500 tekrar, giriş fiyatı da kapanış öncesi fiyat. Sonuç: n≈61, net ortalama 146 bp (p5 114), t ortalama 2,98 (p5 2,23). Son dakika belirsizliğine dayanıklı. Sinyallerin 25/59'unda RSI2 7-10 arasında, yani eşiğe yakın.

## 2. volatilite_S1: istatistiksel sağlamlık (mercek B)

**Çoklu test.** Ajanın 3.075 p değeriyle (`tum_testler_fdr.csv`):

| Yöntem | Geçen | SVXY C0 h2 (p=0,0025) |
|---|---|---|
| BH iki yönlü (ajanın yöntemi) | 113 (105'i negatif) | geçer (eşik 0,00364) |
| **BH tek yönlü (H1: net>0)** | **1** (SVIX C0 h1, yalnız 2022+) | **geçmez** (tek yönlü p=0,00126) |
| Bonferroni (0,10/3.063 = 3,3e-5) | — | geçmez |
| Genel kütüphane (92.664 test), tek yönlü BH | 0 | geçmez |

Neden önemli: iki yönlü BH'de 105 gerçek negatif keşif, yani VXX/UVXY/VIXM'in yapısal kaybı, eşiği yükseltiyor. Pozitif 8 testin **hepsi** yanlış keşif olsa bile FDR 8/113 = %7 < %10 olur. Dolayısıyla bu "geçiş", pozitif kural için neredeyse hiç kanıt taşımıyor.

**Rastgele giriş permütasyonu** (aynı n=59, aynı tutuş, çakışmasız; 2.000-3.000 tekrar):

| Sıfır hipotezi havuzu | C0 h2 gözlenen 157 → rastgele ort / p95 / p | O1 h2 gözlenen 108 → p |
|---|---|---|
| Tüm günler | -3 / 65 / 0,0005 | 0,0010 |
| SMA200 üstü günler | -4 / 50 / 0,0005 | 0,0005 |
| VIX düzeyi ±%10 eşlemeli | 0 / 63 / 0,0003 | 0,0003 |
| VIX + 2 günlük düşüş eşlemeli | 11 / 93 / 0,0003 | 0,0057 |
| Döngüsel kaydırma (kümelenme korunur) | -6 / 42 / 0,0010 | — |

2019-2026 içinde sinyal günleri benzer oynaklıktaki rastgele günlerden açıkça farklı. Bu p değerleri tek test içindir. Kural ~1.000 pozitif yönlü denemenin en iyilerinden biri olarak seçildiği için seçim yanlılığına karşı düzeltilmiş değildir.

**Parametre komşuluğu (gerçek SVXY, C0 h2 net bp; satır RSI2 eşiği, sütun SMA):**

| eşik \ SMA | yok | 100 | 150 | 200 | 250 |
|---|---|---|---|---|---|
| 5 | 31 | 119 | 193 | 117 | 144 |
| 7,5 | 15 | 112 | 163 | 142 | 142 |
| 10 | 42 | 101 | 148 | **157** | 154 |
| 12,5 | 15 | 50 | 92 | 98 | 90 |
| 15 | -5 | -1 | 44 | 59 | 43 |
| 20 | -3 | -10 | -3 | 7 | -11 |

* Eşik 5-12,5 ve SMA 150-250 bölgesi geniş bir plato (t 1,5-3,2). Sivri bir tepe yok. Gerçek SVXY'de ajanın "parametreye duyarlı" yorumundan daha iyi görünüyor.
* SMA filtresi şart: filtresiz sürüm ≈0. Eşik ≥15'te kenar kayboluyor. RSI(3)'te SMA 150-250 ile de pozitif.
* O1'de aynı plato daha zayıf (medyan 71 bp). C1'de eşik ≤10 iken negatif.

**Alt örnekler (C0 h2):**

| Alt örnek | n | net | t | IS net |
|---|---|---|---|---|
| Tümü | 59 | 157 | 3,16 | 144 |
| 2020 hariç | 56 | 184 | 4,15 | 236 |
| 2022 hariç | 58 | 172 | 3,54 | 144 |
| 2020 ve 2022 hariç | 55 | 200 | 4,73 | 236 |
| **2021 hariç** | 47 | **103** | **1,91** | **-241** |
| En iyi 5 çıkarılınca | 54 | 99 | 2,13 | 14 |
| O1 h2, en iyi 5 çıkarılınca | 54 | 57 | 1,43 | 6 |

* Yıllar (C0 h2, işlem başı ortalama net bp): 2019 -162 (4), 2020 -347 (3), 2021 +368 (12), 2022 -681 (1), 2023 +156 (15), 2024 +124 (10), 2025 +287 (4), 2026 +251 (10).
* **IS'in 2/3 yılı negatif ve IS kârının tamamı 2021'den geliyor.**

**Maliyet:** C0 h2 net 1.000 $'da 139 bp (t 2,80), 2.500 $'da 157 bp (3,16), 10.000 $'da 166 bp (3,34). O1 h2 için 90 (2,11), 108 (2,53) ve 117 bp (2,75).

**Mod sağlamlığı:** C0 ve O1 çalışıyor, C1 çalışmıyor. Kenar sinyalden sonraki ilk iki günde. Ayrışma (73 sinyal günü, brüt bp): gece (t kapanış → t+1 açılış) +56 (koşulsuz +8), t+1 gün içi +42 (-2), t+2 +38 (+6). Kural yalnız kapanışa bağımlı değil, ama gecikmeli girişte kenar yok.

**Uzun dönem (vekil, ajanın modeli):** Vekil, gerçek sinyal günlerinde gerçek SVXY getirisini iyi izliyor (korelasyon 0,978; brüt 151'e karşı 173 bp). Vekil üzerinde dönem dönem sonuçlar:

| Dönem | n | net bp | t |
|---|---|---|---|
| 2010-2014 | 52 | +37 | 0,95 |
| 2015-2018 | 24 | -81 | -0,61 |
| 2019-2021 | 18 | +59 | 0,50 |
| 2022-2026 | 41 | +100 | 2,33 |

2010-2018'de RSI<5/10/15 × SMA150/200/250 komşularının tamamı -24..+2 bp. **Etki yalnız 2021 sonrasına ait.**

**Hisse betası ayrışması:** S1 işlem getirisi = a + b × SPY (aynı pencere). Sonuç: b = 2,28, R² = 0,84, alfa (brüt) 48 bp/işlem (t 2,37). QQQ'ya göre b = 1,58, alfa 37 bp (t 1,30). Kazancın çoğu, oynaklık sıçraması sonrası hisse toparlanmasının kaldıraçlı hali.

**Kuyruk (ajanın yazdığından ciddi):**

* Vekilde 02.02.2018 (Cuma) RSI2 = **12,4** (eşik 10) ve SVXY>SMA200. 30.01.2018 sinyali 01.02'de kâra çıkmış. Eşik 12,5 olsaydı (gerçek veride +98 bp'lik komşu) kural 02.02 kapanışında girip 05.02 Volmageddon'u taşırdı. Bugünkü -0,5x yapıyla NAV kaybı ~%45-50 olurdu. VIXY'den türetilen -0,5x sentetik 16:00 kapanışlarıyla -%15,8 gösteriyor, ancak bu 16:15 sıçramasını kaçırdığı için iyimser.
* Vekilde en kötü işlemler: 20.08.2015 → 24.08.2015 **-2.330 bp**, 21.02.2020 -1.376, 09.10.2018 -1.203, 09.06.2016 -986.
* Cuma sinyalleri (hafta sonu taşınan) n=17, ortalama +84 bp, en kötüsü -1.375. Diğer günler n=42, +187 bp.
* Kural yapı gereği rejim geçişlerinin ilk gününde kısa vol alıyor. Yılda ~8 işlem ve yıllık ~%13 bileşik getiriyle, -%48'lik tek bir olay ~4-5 yıllık kârı siler. SVIX'te (-1x) bu olay pozisyonun neredeyse tamamını götürür.

**Midas uygulanabilirliği:**

* SVXY ProShares Trust II ürünü (K-1/PTP). `midas_kosullari.md` §5.4'e göre ProShares Trust II'nin 26.02.2026 tarihli 92 günlük Qualified Notice'i "10 percent exception applies" diyor. Bu durumda yasal olarak %10 kesinti gerekmez. Ancak bildirim 92 gün geçerli ve sonrası kontrol edilmedi. Midas 2024'te UNG'de kesintiyi 1-1,5 hafta boyunca yine de uyguladı.
* Kesinti brüt satış tutarı üzerinden olur, yani 2 günlük işlemde -1.000 bp. Bu, kuralın 6 katı.
* Midas'ta SVXY'nin bulunurluğu doğrulanmadı. SVIX/UVIX (Volatility Shares Trust) büyük olasılıkla K-1 veriyor; doğrulanmadı.
* Açığa satış yok; kural yalnız long olduğu için uygun. C0 için 23:50-23:59 TR (kış) aralığında normal seans limit emri gerekir. Stop emri %15-40'lık boşluklarda dolmayabilir.

## 3. Lead-lag

| Hedef ← öncü | Hizalama | t (tüm) | IS t | OOS t | Kendi gecikmesi ile | Ekonomik | Karar |
|---|---|---|---|---|---|---|---|
| VXX ← VVIX/VIX | O1 h1 | 3,17 | 2,05 | 2,72 | kontrol edildi, t aynı | 1 sd = 22 bp (maliyet 16,6) | **çürük**: IS'te belirlenen üst %20 eşiğiyle işlem OOS'ta negatif (O1 h1 -36, O1 h2 -32 bp), FDR yok. VXX'in -9,6 bp/gün kaybı baskın |
| VXX ← VVIX/VIX | C0 h1 | 1,95 | 0,89 | 2,69 | | | VIX 16:15 kapanışı yüzünden C0 kirli |
| SVXY ← QQQ getirisi | C0 h3 | -2,89 | -2,33 | -1,86 | kendi gecikmesi t=+1,18 | 1 sd = -47 bp | **çürük**: h1'de IS -2,88 / OOS +0,27 (işaret tutarsız), O1'de anlamsız, FDR yok, ve açığa satış olmadığı için işlenemez |
| SVIX ← VVIX/VIX | O1 h1 | -2,28 | — | — | | | yalnız 2022+, FDR yok, zayıf |

* `leadlag_sweep.csv`'deki aile hedeflerinin (336 satır) hiçbirinde FDR bayrağı yok. En yüksek |t| değerleri (VIXM/UVXY/VIXY/SVXY ← QQQ) IS'te var, OOS'ta yok.
* Bayat fiyat riski düşük: SVXY, VXX ve UVXY likit, son işlem 16:00'da. VIXM likiditesiz (3,6 mn $) ve oradaki QQQ öncülüğünün (IS 3,2 → OOS 0,4) bir kısmı bayat fiyat artefaktı olabilir.
* Eşzamanlı sürücüler (VIX, VVIX, SPY, QQQ, VIX/VIX3M) doğru biçimde "öncü değil" olarak ayrılmış.
* Gerçek zamanlı izleme araçlarının TV kodları doğrulanmış: CBOE:VX1!, CBOE:VX2! (kanonik), CME_MINI:ES1!, CME_MINI:NQ1!, FX_IDC:USDJPY (kanonik).

## 4. Elenen hipotezlerden örnek kontrol (kendi motorum)

| Hipotez | Benim sonucum | Ajan |
|---|---|---|
| VO01 SVXY | C0 -20,9 (t -1,35), O1 -28,9 (-1,95), C1 -21,8 (n=326/263) | aynı |
| H_kont09 SVXY O1 h1 | -19,4 bp (t -4,45) | aynı |
| VO03 koşulsuz günlük ortalama | VXX -9,6, VIXY -11,1, UVXY -18,4, UVIX -34,5, SVXY +6,0, SVIX +12,0 bp | aynı |
| E2 Pazartesi gün içi (benim tanımım: ertesi işlem günü Pazartesi) | SVXY +7,6 (t 0,92; IS -18, OOS +26 t 2,81); SVIX OOS +62 (t 3,42); VXX OOS -101 (t -5,19) | ajanın Cuma tanımı: +2 bp, OOS +18. Rejim etkisi (2022+), IS'te yok; elenmesi doğru |

## 5. İzleme listesine itirazlar

* **SVXY (kabul → koşullu kabul).** Sinyal kaynağı olarak kalmalı (CBOE:SVXY). İşlem aracı olarak, Midas'ta bulunurluk ve PTP kesintisi uygulanmadığı uygulama içinde teyit edilmeden kullanılmamalı. Teyit yoksa aynı sinyal QQQ/QLD ile işlenebilir (§6).
* **SVIX (yedek → red).** Kanıtı yalnız 2022+ (n=39, tek rejim) ve SVXY'nin aynı olaylarının ~2 katı. Bağımsız kanıt değil. -1x yapı nedeniyle Şubat 2018 tipi olayda ~%90+ kayıp riski taşıyor ve kural böyle bir olaya kıl payı girmemiş. PTP muhtemel. Bireysel 1-3 günlük işlemci için uygun değil.
* **VXX (yedek).** Kabul edilebilir, ancak açıkça "işlem adayı değil, yalnız koruma" olarak işaretlenmeli. S1 sinyal günlerinde VXX C0 h2 -350 bp (t -3,58) ve 1-3 günlük hiçbir long kural pozitif değil.
* VIXY, UVXY, UVIX ve VIXM için red kararlarına katılıyorum.

## 6. Kaçırılan fırsat ve risk

* **Aynı sinyal, PTP'siz araç.** SVXY sinyali (RSI2<10 ve SVXY>SMA200) t kapanışında görülünce QQQ ya da QLD almak:

| Araç | C0 h2 net (t) | O1 h2 net (t) | C1 h2 | IS net (t) | OOS net (t) | en kötü | maxDD |
|---|---|---|---|---|---|---|---|
| QQQ | +73 (2,84) | +46 (2,23) | +10 | +33 (0,62) | +92 (3,27) | -660 | -%7 |
| QLD | +154 (3,01) | +103 (2,51) | +27 | +77 (0,72) | +191 (3,39) | -1.289 | -%13 |
| TQQQ | +236 (3,09) | +159 (2,59) | +48 | +118 | +293 | -1.882 | -%19 |
| SVXY (karşılaştırma) | +157 (3,16) | +108 (2,53) | -28 | +144 | +164 | -1.375 | -%14,5 |

* QQQ'nun kendi RSI2<10 ve SMA200 sinyali çok daha zayıf: C0 +23 (t 1,25), O1 -6. Yani SVXY sinyali hisse için ek bilgi taşıyor. Kendi sinyalinin olmadığı SVXY-sinyali günlerinde QQQ O1 h2 +69 (t 2,61).
* Bu sonuçlar aynı 59 olaya dayanıyor (bağımsız kanıt değil), IS'te zayıf ve sonradan bakılmış. QQQ'da en iyi 5 işlem çıkarılınca C0 +43 (t 1,77), O1 +23 (t 1,18).
* Yine de PTP kesintisi ve Volmageddon tipi kuyruk riski olmadan aynı kenarın büyük kısmını veriyor. QLD/TQQQ'nun Midas'ta bulunurluğu doğrulanmadı (TQQQ "muhtemel").
* **Risk:** S1'in en büyük riski, rejim geçişinin ilk gününde kısa vol almak. Vekilde Ağustos 2015'te tek işlemde -%23 ve Şubat 2018'de kıl payı. Pozisyon küçük tutulmalı. "Şubat 2018: pozisyon yok" ifadesi raporlarda kullanılmamalı.

## 7. Tekrar üretim

```
python3 -I kod/denetim_volatilite/denetim_S1.py         # yeniden üretim, alt örnek, permütasyon, komşuluk, C0 duyarlılığı, diğer araçlar
python3 -I kod/denetim_volatilite/denetim_ek.py         # VIX eşlemeli permütasyon, vekil sadakati, beta ayrışması, QQQ/QLD/TQQQ
python3 -I kod/denetim_volatilite/denetim_subat2018.py  # Şubat 2018 kıl payı, vekil kuyruk tablosu
python3 -I kod/denetim_volatilite/denetim_leadlag.py    # öncü iddialarının bağımsız HAC yeniden hesabı
python3 -I kod/denetim_volatilite/denetim_elenen.py     # elenen hipotezlerden örnekler
```
