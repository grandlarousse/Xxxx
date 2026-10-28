# ENDEKS — 1. Tur (28.10.2026) | BIST 30 vadeli, teknik, fon akımı

Etiketler: **[D]** kaynakla doğrulandı · **[H]** benim hesabım (Yahoo günlük verisi + kod: `scratchpad/scripts/*.py`) · **[T]** tahmin · **[V]** varsayım

**Hüküm:** Spot 13.961'de (F_XU0301226 ~14.649) yön için avantaj yok. Bu seviyeden long'a hem carry (~10,7 puan/gün) hem tarihsel benzerler karşı çıkıyor. Veri yalnızca **aralığın uçlarında, 30 Ekim sonrası, küçük boyutlu** işlemleri destekliyor: birincil fikir tepki yükselişinde short, ikincil fikir dip testinde koşullu long. 30 Ekim'den önce yeni pozisyon açılmamalı.

## 1. Kontrat ve baz
| Unsur | Değer |
|---|---|
| Çarpan / adım | 10 TL × endeks; 0,25 puan = 2,5 TL [D: GCM, BIST] |
| Vadeler | Çift aylar (Şub/Nis/…/Ara). Aynı anda en yakın 3 vade + Aralık işlem görür [D] |
| Ekim son işlem | **30.10.2026 Cuma** [D: Borsadirekt]. Kural: ayın son iş günü; o gün yarım günse bir önceki iş günü [D: BIST] |
| Vade sonu uzlaşma | Son 30 dk TWAP %80 + kapanış %20 [D] |
| Fiyat limiti | Normal seans ±%15, akşam seansı ±%3 [D: GCM] |
| Teminat | Takasbank PSR 0,114 (02.10.2026) → ~15.939 TL/kontrat (Ekim). Aracı kurum +%20. Sürdürme teminatı başlangıcın %75'i [D: Vakıf, Borsadirekt, BIST]. GCM "14,25" ve "1:7" diyor; çelişki aracı kurum ek payından kaynaklanıyor olabilir |
| Aralık vadesi | 14.649, OI 314,4K; Ekim 13.986, OI 210,9K (TradingView, saat damgası yok → ±50 puan belirsizlik) [D] |

**Baz hesabı [H]** (spot XU030 28.10 kapanış 13.960,9; r = %36 ≈ politika faizi/TLREF [V]; Kasım–Aralık temettüsü ≈0 [V]):
- Ekim: teorik 13.961×0,36×2/365 = +27,5; gözlenen +25 → **uyumlu**.
- Aralık: teorik 13.961×(1+0,36×64/365) = **14.842**; gözlenen 14.649 → teorinin **193 puan (%1,3) altında**, zımni faiz **%28,1**.
- Anormal mi? 2026'daki geçmiş gözlemlerde zımni faiz %24–33 bandında: 30.01'de %24–29, 30.03'te %30–33 (Gedik bültenleri) [H]. **Baz normal aralıkta; panik iskontosu yok, sinyal değeri yok.**
- Rollover: Aralık–Ekim farkı 663 puan (zımni %27,9; teorik 855). Long'u devretmek ucuz, short'u devretmek pahalı. Aralık OI'si Ekim'i geçti, yani rollover büyük ölçüde tamamlanmış. Şubat 2027 likit değil (Nisan'da 2. ve sonraki vadelerin OI'si yalnızca yüzlerce kontrattı), bu yüzden takvim spread'ini önermiyorum.
- **Carry:** Long Aralık vadelisi, spot yatay kalsa da vadeye kadar ~688 puan (%4,9) kaybeder, yani ~10,7 puan/gün.

## 2. Düşüşün yapısı: zorunlu satış bitti mi?
- **Yabancı [D, TCMB üzerinden haberler]:** 25 Eyl haftası **+358,6** mn $, 2 Eki **−189,9**, 9 Eki **−248,2**, 16 Eki **−88,8**. Üç haftalık çıkış −526,9 mn $; bu, 33,98 mlr $'lık stokun yalnızca ~%1,6'sı. Çıkış yavaşlıyor ve düşüşün ana sürücüsü yabancı değil.
- **Fon tasfiyesi [D: Gedik 05.10]:** Tasfiyedeki fonların büyüklüğü 1.233 → 652 mlr TL (31.08→30.09). Likit hisse pozisyonu yalnızca ~40,3 mlr TL ve büyük, likit hisselerde, yani hızla satılabilir. Asıl yük likit olmayan **123 hissede 146,5 mlr TL**: %20 ADV satış varsayımıyla bunun **%45'inin satışı 60 işlem gününden uzun sürer**. Para piyasası fonlarında ayrıca %22,4 puanlık pay senedi repo teminatı var. Sonuç: arz baskısı küçük ve orta ölçekli hisselerde 2027 1. çeyreğe kadar sürebilir. 7596 sayılı Kanun (RG 27.10) borsa dışı satışa izin veriyor, bu da borsadaki baskıyı azaltır.
- **Kredili işlem [D]:** Ağustos sonu stok 129,2 mlr TL. Teminat tamamlama çağrısı Eylül'de 1,13 mlr TL'ye çıktı. **Ekim verisi bulunamadı, test edilemedi.** SPK'nın asgari özkaynak oranını %35'ten %20'ye indiren esnekliği **30.10 seans sonunda bitiyor** (uzatılmazsa sona erer).
- **BIST 30'un göreli gücü [H]:** XU030/XU100 oranı 1,188 → 1,25. BIST Tüm-100 iki haftada −%10,5 ve −%11,5 [D: Paraanaliz]. Zorunlu satış ağırlıkla BIST 30 dışında.
- **Diğer:** MKK yatırımcı sayısı Eylül'de −105 bin (−%1,54); yabancı saklama payı %36,93 (fiyat etkisi; Paraanaliz ~%40 diyor, çelişki). SAHOL geri alımı günde ~25 mn TL: akış değil, sinyal. 23.10'a kadar 68 mlr TL ara ödeme [D: AA/apara]. VİOP toplam OI ~525K, Nisan ön vadesiyle (~520K) aynı: vadelilerde kaldıraç azaltımı yok.
- **Hüküm [T]:** BIST 30'da en yoğun mekanik satış muhtemelen geride. Göstergeler: 23.10'daki uzun alt fitil (XU100 gün içi 10.707), yavaşlayan yabancı çıkışı, göreli güç. Küçük hisselerde satış sürüyor. Kuyruk riski: 30.10'da esneklik uzatılmazsa teminat tamamlama satışları.

## 3. Tarihsel benzerler [H] (örneklem küçük, sonuçlar yönteme duyarlı)
- **(a)** XU100'ün 30 işlem gününde ≥%20 düştüğü 22 olay (1997–2023): 21 günlük getiri medyanı +%3,3 (%67 pozitif). **63 günlük medyan +%2,9 (%50 pozitif)**, koşulsuz +%5,5'in altında. 63 gün içindeki en kötü düşüş medyanı **−%10**. Kötü sonuçlar: 1998/08 −%27, 2008/09 −%23.
- **(b)** 6 hafta üst üste düşüş: yalnızca 2 emsal var. 2002/12: 63 gün sonra −%3,0; 2008/02: +%0,8. Kendi içlerindeki en kötü düşüş −%15 ve −%7.
- **(c)** Bugünkü konuma en yakın tasarım: XU030, ilk −%17 kırılımından 7 gün sonrası, epizot başına tek gözlem, n=22. 21 günlük medyan **+%1,2**, 42 günlük +%3,1. Dolar bazında 42 günlük medyan **−%0,4**. P(önce +%5,3, sonra −%4,5) = **0,32**; koşulsuz değer 0,48. Uyarı: durumdaki tüm günleri sayan tasarımda güçlü dönüş çıkıyor (21 günlük +%5,9), yani bulgu kırılgan.
- **Dolar bazı [H]:** XU100/USDTRY = **224**. 2023 Haziran'dan beri en düşük (o dönem 220), 9 Eylül'e göre −%25. 2005 sonrası dağılımda %27'lik dilimde; 2018 ve 2021 dipleri 124–134. Ucuz ama zamanlama sinyali değil.
- **Sonuç:** "Çok düştü, yükselir" iddiası kanıtlanmıyor. 42 günlük medyan getiri (~%3), long'un aynı sürede ödediği carry'den (~%4,5) düşük.

## 4. Teknik (XU030 spot) [H]; kanıt değeri sınırlı
- SMA20 14.722 (−%5,2), EMA20 14.663, SMA50 15.751, SMA200 15.664 (−%10,9). Tüm ortalamalar düşüyor.
- RSI(14) günlük 32,6, haftalık 37,4. XU100'de 30.09'daki RSI dibi 22,2; fiyat şimdi daha düşük ama RSI daha yüksek, zayıf bir pozitif uyumsuzluk.
- ATR14 344 puan (%2,5); 20 günlük realize volatilite %27.
- Destek: 13.370 (23.10 dibi), 13.252/12.830 (Ata), Fib %61,8 = 12.716. Direnç: 14.170–14.200, Fib %38,2 = 14.456, 14.547 (Ata), EMA/SMA20 14.66–14.72.
- Not: Seviyeler spot. Aralık vadelisi ≈ spot × (1 + 0,28 × kalan gün/365).

## 5. Baseline düzeltmeleri
1. "Zirve 14.235,83 (14 Eyl)" aslında çöküş öncesi son kapanış. Kapanış zirvesi 9 Eylül'de 14.505,5; 52 haftalık zirve 11 Mayıs'ta 15.134 (zirveden −%26) [H].
2. 9 Ekim haftası yabancı çıkışı **−248,2** mn $; baseline'daki −348 yanlış. 3 haftalık toplam (−527) doğru.
3. "2007'den beri en sert" ifadesi hatalı; doğrusu **Şubat 2008'den beri en uzun haftalık düşüş serisi** [D + H].
4. Fon büyüklüğü: Gedik'e göre 129 fon, Ağustos sonu 1.233 mlr TL; baseline'daki "223 fon / 1,10 trilyon" ile tutmuyor.
5. 27.10 XU100 kapanışı 11.151 (Investing 11.249 değil); Ekim kontratı 13.942 (AA) veya 14.015 (Ata).

## 6. FİKİR 1 (birincil): Tepkide short, F_XU0301226
- **Giriş:** 15.000–15.100 limit satış (≈ spot 14.380–14.480: Fib %38,2 ve Ata direnci). Yalnızca 30.10 açılışından ≥30 dk sonra; dolmazsa işlem yok.
- **Zarar-kes:** 15.500 (≈ spot 14.860–14.930, SMA20 üstü). **Hedef:** 13.800 (≈ spot 13.430–13.490, 23.10 dibinin üstü). **Süre:** dolumdan sonra ≤25 işlem günü, en geç 04.12 (PPK 10.12'den önce).
- **Boyut:** Sermayenin %0,75'i risk. Kontrat sayısı = (sermaye × 0,0075) / (450 × 10 × 1,5 gap çarpanı). 1 mn TL sermayeye 1 kontrat: normal risk 4.500 TL (%0,45), 2× gap senaryosunda ~%0,9.
- **Kontrat ekonomisi:** Nominal ≈ 150.500 TL; 1 puan = 10 TL. Teminat ≈ 17,2 bin TL (Takasbank) / ~20,6 bin TL (aracı kurum). Teminat ile kaldıraç ~7–9×; sermayeye göre nominal 0,15×.
- **Getiri/risk:** 1.250 / 450 = **2,8** (carry dahil; yalnız spotta 2,3).
- **Olasılık [T]:** Benzer simülasyon (spotta +%3 dolum, +%3 stop, −%7 hedef; n=22): dolum %73, dolarsa hedefe ulaşma 7/16 = %44. Benim tahminim **%35–45**. %40'ta beklenen değer ≈ +230 puan (+2.300 TL) eksi maliyet (~100–200 TL [V]).
- **Tez:** A) Likit olmayan fon stoku 60+ günde eriyor, soruşturma genişliyor (114 gözaltı, eski SPK başkanı), Brent 110 $ üstünde. → B) Tepkiler kırılan destek ve EMA20 bölgesinde (14,4–14,7 bin) satıcı buluyor. → C) Short vadeli pozisyon günde ~10,7 puan baz yakınsaması kazanıyor. → D) Benzerlerdeki 42 günlük medyan getiri (~%3), baz erimesinden (~%4,5) küçük. → **Sonuç:** küçük pozitif beklenti.
- **Karşı argüman / en büyük risk:** SPK uzatması, ödemelerin yarattığı nakit, Hürmüz çözümüyle petrol düşüşü, yabancının dipten alımı (25 Eylül emsali); dipte short kalabalık olabilir; baz adil değere yakınsarsa short ~190 puan kaybeder.
- **Çöktüren varsayım:** "BIST 30 kendi stokundan bağımsız olarak satış baskısı görmeye devam eder." 2019 Mayıs ve 2020 Mart'taki gibi V dönüşü bu varsayımı çürütür.
- **Yanlışlama:** XU030 spot kapanışı >14.850, veya art arda 2 hafta >200 mn $ yabancı hisse alımı, veya kamu kaynaklı alım programı duyurusu.
- **Güven: 4/10.**

## 7. FİKİR 2 (ikincil, koşullu): Dip testinde long, F_XU0301226
- **Giriş:** 13.950–14.050 (≈ spot 13.380–13.480). **Ön koşul:** 30.10'da SPK esnekliğini uzatmış olmalı ve teminat çağrılarında sıçrama olmamalı.
- **Zarar-kes:** 13.500 (≈ spot 13.000). **Hedef:** 14.650 (≈ spot 14.250). **Süre:** ≤20 işlem günü.
- **Boyut:** Sermayenin %0,5'i risk. 1 mn TL'ye 1 kontrat (risk 5.000 TL). Nominal ≈ 140 bin TL, teminat ≈ 16–19 bin TL.
- **Getiri/risk:** 650 / 500 = **1,3** (carry R:R'yi düşürüyor; yalnız spotta 1,7).
- **Olasılık [T]:** Simülasyonda dolum %68, dolarsa hedef 9/15 = %60. Tahminim **%45–55**. Beklenen değer ≈ +75 puan, yani maliyet sonrası **sıfıra yakın**.
- **Tez:** 23.10 dibi zorunlu satışın temizlendiği fiyat → düşük hacimli test + politika desteği → daha yüksek dip.
- **En büyük risk:** Düşen bıçak (1998/08 ve 2008/09 tipi sistemik yayılma).
- **Yanlışlama:** Spot kapanışı <13.000, esnekliğin uzatılmaması, haftalık yabancı çıkışı >300 mn $.
- **Güven: 3/10.**
- Aynı anda tek pozisyon; birinin stopu diğerinin girişi değildir.

## 8. Olay ve gap riski
- 30.10 aynı gün birçok olayı topluyor: 1,5 günlük kapanış sonrası açılış, Fed kararının (28.10 akşamı) fiyatlanması, Ekim vadesinin sona ermesi, SPK esnekliğinin bitişi, 1 mn TL'lik ödemelerin başlaması, muhtemelen TCMB haftalık menkul kıymet verisi [V].
- 1,5–2 ATR'lik açılış gap'i (500–700 puan) olası [T].
- Ekim enflasyonu 03.11 [V, doğrulanmadı]; PPK 10.12 [D]. Aralık vadesi 31.12; o gün yarım gün ilan edilirse vade bir önceki iş gününe kayar.

**2. tur için test edilebilir iddialar:** (i) Aralık bazının zımni faizi normal aralıkta. (ii) Benzerlerde dönüşün avantajı carry'yi aşmıyor. (iii) Zorunlu satış BIST 30 dışında yoğunlaşıyor. (iv) 30.10 tek günlük kuyruk riski taşıyor.

## Kaynaklar
GCM kontrat sayfası https://www.gcmyatirim.com.tr/viop/viop-sozlesmeleri/endeks-sozlesme/borsa-istanbul-bist-30-endeksi-xu030d · BIST spesifikasyonu (2014) https://www.borsaistanbul.com/files/viop-ozet-bilgiler-dokumani.pdf · https://www.borsadirekt.com/viop/xu030 · https://www.vakifyatirim.com.tr/viop-teminat-tutarlari · https://tr.tradingview.com/symbols/BIST-XU030DZ2026/ · https://tr.tradingview.com/symbols/BIST-XU030DV2026/ · Gedik VİOP bültenleri https://cdn.gedik.com/media/media/wwffprgv/viop_bulten_30032026.pdf , https://cdn.gedik.com/cdn/bulletin/2026/01/30/VIOP_Bulten_30012026_3af68c60.pdf · Gedik tasfiye raporu https://cdn.gedik.com/media/media/tvmjp14x/gedik_yatirim_tasfiye_fonlari_degerlendirme_05102026.pdf · Yabancı akımı https://www.foreks.com/haber/detay/6ad0b9f3422c786f3f7a3939/PICNEWS/tr/yabanci-yatirimci-hissede-satisa-devam-etti-tahvile-451-milyon-dolar-aktardi-15-10-26/ , https://www.sabah.com.tr/ekonomi/tcmb-acikladi-yabanci-yatirimcilar-888-milyon-dolar-hisse-satti-7686187 · SPK esnekliği https://www.endeks24.com/spk-kredili-islemlerdeki-esnekligi-30-ekime-kadar-uzatti · Kredili işlem https://www.borsatek.com/araci-kurum-bono-itfa-borsa-riski/ · 68 mlr TL ödeme ve vadeli fiyatlar https://www.apara.com.tr/piyasalar/2026/10/28/viopta-endeks-kontrati-gune-yukselisle-basladi · Ata teknik https://www.foreks.com/haber/detay/6ae0475f422c786f3f7aa782/FRKS/tr/analiz-viop-teknik-bulten-ata-yatirim-27-10-26/ · Düşüş serisi ve soruşturma https://www.cumhuriyet.com.tr/ekonomi/fon-krizi-borsa-yi-vurdu-18-yilin-en-uzun-dusus-serisi-2550017 · Brent ve küçük hisseler https://www.paraanaliz.com/haberler/borsa-da-bu-hafta-ne-bekleniyor-bist-100-de-10-bin-puan-riski · VİOP hacmi https://www.gcmyatirim.com.tr/arastirma-analiz/yurtici-piyasalar-haftalik-bulten/2026-10-19-bist30-kontrati-viop · MKK https://www.hisse.net/haber/borsada-yatirimci-sayisi-geriledi-yabancilarin-payi-yukseldi-99959 · SAHOL geri alımı https://www.borsatek.com/sahol-27-ekimde-geri-alim/ · PPK takvimi https://www.cnbce.com/faiz/turkiye-cumhuriyet-merkez-bankasi-2026-yili-para-politikasi-kurulu-ppk-toplantilari-ve-rapor-takvimini-acikladi-h22037 · 27.10 piyasa verisi https://cnbce.com/borsa/borsa-istanbul-canli-piyasalarda-yeni-yukselis-beklentisi-27-ekim-2026-h40399 · Fiyat serileri: https://query1.finance.yahoo.com/v8/finance/chart/XU030.IS (ayrıca XU100.IS, TRY=X)
