# TRALT ← Altın (Strateji C): uygulama rehberi

Hazırlanma: 04.11.2026. Veri: VİOP bültenleri (Borsa İstanbul) 2017-03 → 03.11.2026, Yahoo günlük/saatlik/5 dk. Yatırım tavsiyesi değildir.
**Güven: DÜŞÜK.** Etki gerçek görünüyor ama küçük, rejime bağlı ve kazancın önemli kısmı birkaç büyük işlemden geliyor.

---

## 1. Kural tek paragrafta

Her BIST günü 17:55'te ons altının (TVC:GOLD) bir önceki BIST gününün 17:55 fiyatına göre log değişimini hesaplayın: **g**. Bunu son 250 günün aynı türden değişimlerinin standart sapmasına bölün: **z = g / σ**. Açık pozisyon yokken:

- **z > +1** ise TRALT vadelisi AL, XU030 vadelisi SAT.
- **z < −1** ise TRALT vadelisi SAT, XU030 vadelisi AL.

Oran: 1 XU030D kontratına karşılık N = yuvarla(10·XU030 / (β·100·TRALT)) TRALT kontratı alınır. β, TRALT'ın XU030'a göre 250 günlük betasıdır. Pozisyon 18:00–18:10 uzlaşma penceresinde açılır ve **2 BIST günü sonra** aynı pencerede kapatılır. Pozisyon açıkken yeni sinyale bakılmaz. Çıkış günü aynı yönde yeni sinyal varsa pozisyon kapatılmaz, 2 gün daha taşınır. Ters yönde sinyal varsa pozisyon çevrilir.

Araştırmadaki kural birebir yeniden üretildi (c3_gold.py; VİOP XAUUSD uzlaşma değişimi, F_TRALT − β·F_XU030, h=2, |z|>1, örtüşmesiz): n 405, yılda 54,6 işlem, net +42,9 bps (t 2,54), 15 bps maliyetle +35,9; IS +44,1 (1,82) / OOS +42,3 (1,89); en iyi 10 işlem çıkınca +20,7 (t 1,31); 2024–26 +69,7 (t 2,44). Rakamlar yayımlananla aynı. Pratik kuraldaki tek fark sinyal kaynağı: VİOP altın uzlaşması işlemle aynı dakikalarda oluşur ve önceden bilinemez. Onun yerine 17:55'teki spot altın kullanılır.

## 2. TradingView'da izlenecek kodlar (yalnız tv_final.csv'de doğrulanmış kodlar)

| Kod | Rol | Neden |
|---|---|---|
| **TVC:GOLD** | Sinyal girdisi | Spot ons altın. Vade geçişi olmadığı için sıçrama yapmaz. TradingView'ın kendi verisidir ve genellikle ücretsiz hesapta da gerçek zamanlıdır (sembol yanında gecikme ibaresi olup olmadığına bakın). 17:55 değeri sinyali belirler. |
| OANDA:XAUUSD | Sinyal girdisi (yedek) | TVC:GOLD açılmazsa aynı işi görür. Seviye birkaç dolar farklı olabilir; önemli olan yüzde değişim. |
| BIST:XAUUSD1! | Bağlam (senkron, araştırmanın asıl sinyali) | VİOP ons altın vadelisi. Araştırmadaki sinyal bunun uzlaşmasıydı. TV'de 15 dk gecikmelidir, canlı fiyatı aracı kurum ekranından alın. Ertesi sabah bültendeki uzlaşma değişimiyle dünkü kararınızı kontrol edin. |
| COMEX:GC1! | Yalnız bağlam, **sinyal için kullanmayın** | Sürekli kontrattır ve vade geçişinde %0,5–2 sıçrar. Yahoo GC=F'de 2,3 yılda 11 sahte sıçrama ölçüldü. Ücretsiz hesapta CME verisi de gecikmelidir. |
| **BIST:TRALT1!** (vade kodu ör. BIST:TRALTX2026) | İşlem aracı | TRALT pay vadelisi (100 pay). Aylık vadeli, A sınıfı likidite. Tik 0,01 TL, 35 TL fiyatta yaklaşık 3 bps. |
| **BIST:XU030D1!** (ör. BIST:XU030DZ2026) | Hedge (işlem aracı) | BIST 30 vadelisi, 1 kontrat = endeks × 10 TL. **Yalnız çift aylarda** vadesi vardır (Kasım'da Aralık kontratı kullanılır). |
| BIST:TRALT | Bağlam / kilit kontrolü | Spot. β hesabında ve tavan/taban kilidini görmek için. |
| BIST:XU030 | β girdisi | Spot endeks. |
| BIST:TRMET, BIST:TRENJ | Bağlam (senkron) | Koza grubu. TRALT'ın grup faktörü altın bağından daha güçlü: varyans payı %42, altının günlük kısmi korelasyonu 0,21. Grupta özel bir haber varsa altın sinyalini o gün devre dışı bırakır. Bunlarla işlem yapılmaz. |
| FX_IDC:XAUTRYG / BIST:XAUTRY1! | Bağlam | Gram altın TL. Ayrı bir sürücü değil (USDTRY katkısı ≈0), sinyal için kullanılmaz. |
| AMEX:GDX | Bağlam | Altın madencileri. Ertesi sabah TRALT açılışını etkiler. Bu stratejide kullanılmaz. |

TradingView'daki 15 dakikalık BIST gecikmesi sinyali etkilemez, çünkü sinyal yalnız altına bakar. BIST fiyatları yalnız kontrat sayısını (N) hesaplamak için gerekir. Emirleri aracı kurumun canlı ekranından verin.

## 3. Günlük akış (saat saat, TSİ)

**Sabah 09:30–10:00**
1. `python3 sinyal_altin.py` komutunu çalıştırın. Çıktıda dünkü kapanışın z değeri, kurala göre açık pozisyon olup olmadığı, çıkış tarihi ve kullanılacak vade kodları yazar.
2. Bugün çıkış günüyse not alın. Bugün yarım gün (arife) ise kural uygulanmaz (bkz. §7).
3. KAP'ta TRALT, TRMET, TRENJ ve Koza grubuyla ilgili haber olup olmadığına bakın. Olay günlerinde yeni pozisyon açmayın.

**Gün içi:** İşlem yok. İsterseniz TradingView'da `altin.pine` göstergesinin "Altın sinyali (geçici)" alarmını kurun. Sinyal gün içinde oluşup kaybolabilir; karar yalnız 17:55'te verilir.

**17:45 – ön kontrol**
- TVC:GOLD fiyatını okuyun. Betiğin sabah yazdığı "BUGÜN 17:55 TETİĞİ" seviyelerine bakın. Örnek, 04.11.2026: AL ≥ 4.022,7 / SAT ≤ 3.888,0 (COMEX Aralık vadelisi seviyesiyle). Spot fiyatta seviye değil yüzde eşiği kullanın: dünkü 17:55 değerine göre ±%1,70.
- |z| 0,9–1,1 arasındaysa karar 17:55'te değişebilir. 17:55'e kadar bekleyin.

**17:50–17:55 – kesin karar**
- g = ln(altın_17:55 / dünkü altın_17:55), z = g / σ. σ'yı betikten alın (bugün %1,70). Betiği bu saatte yeniden çalıştırmak da olur, ama Yahoo'nun COMEX verisi yaklaşık 10 dk gecikmelidir ve 17:55'te size 17:45 fiyatını verir. Bu yüzden TVC:GOLD ile kendiniz hesaplamak daha iyidir.
- |z| ≤ 1 ise bugün işlem yok. Açık pozisyonun çıkış günüyse 18:00–18:10'da kapatın.
- |z| > 1 ise:
  - Pozisyon yoksa yön(z) ile açın.
  - Aynı yönde pozisyon bugün kapanacaksa **hiçbir şey yapmayın**: pozisyon 2 gün daha taşınır ve sayaç sıfırlanır. Backtest'te işlemlerin %13'ü (56/423) böyle devam ediyor ve işlem başı +1,4 bps maliyet kazandırıyor.
  - Ters yönde pozisyon bugün kapanacaksa çevirin (2 kat miktar).
- **Kilit kontrolü (aracı kurum ekranı):** AL sinyalinde TRALT vadelisi tavanda kilitliyse (satıcı yok), SAT sinyalinde tabanda kilitliyse bugün girmeyin.

**18:00–18:10 – emir (uzlaşma penceresi)**
- TRALT bacağı için pay vadelisinin uzlaşması son 10 dakikanın VWAP'ıdır ve seans 18:10'da kapanır. Emri 2–3 parçaya bölüp en iyi alış/satış fiyatından limitli verin. 18:08'den sonra kalan kısmı karşı fiyattan tamamlayın.
- XU030 bacağı için endeks vadelisi 18:15'e kadar açıktır (uzlaşma ≈18:05–18:15). Aynı pencerede, TRALT bacağıyla birlikte yapın.
- Bir bacak dolmazsa doldurulan bacağı da aynı gün kapatın. Yarım hedge'le gece taşımayın.
- Akşam seansını kullanmayın. Pay vadelisinin akşam seansı yoktur.

**Ertesi gün (t+1):** Bir şey yapmayın. Stop kuralı yoktur, çünkü backtest stopsuz yapıldı.

**t+2 günü 17:55:** Yeni z'yi hesaplayın. Aynı yönde sinyal varsa pozisyonu tutun, ters yönde varsa çevirin, sinyal yoksa 18:00–18:10'da kapatın. Çıkış günü TRALT size karşı kilitliyse (long'da taban, short'ta tavan), ertesi günün uzlaşmasında çıkın. En fazla 3 gün uzatın.

## 4. Örnek işlemler (gerçek VİOP uzlaşma fiyatlarıyla)

**Zararlı işlem: 30.10.2026 SAT.** Altın 17:55'te 3.923,8. Önceki BIST günü (28.10; 29.10 tatil) 4.054,4 → g −%3,27, σ %1,69, z −1,94 (uzlaşmayla z −2,01). β 1,24, N = 34.
- SAT 34 × F_TRALT1126 @ 33,25 / AL 1 × F_XU0301226 @ 14.108.
- Çıkış 03.11 uzlaşması: TRALT 34,94 / XU030 14.412.
- TRALT bacağı −5.746 TL, XU030 bacağı +3.040 TL, brüt −2.706 TL. Maliyet (11 bps) ~124 TL, net **−2.830 TL** (−241 bps).

**Kârlı işlem: 19.08.2026 AL.** z +1,60. 29 × F_TRALT0826 @ 51,04 → 54,83; 1 × F_XU0300826 @ 16.759 → 16.808.
- TRALT bacağı +10.991 TL, XU030 bacağı −490 TL, net **+10.338 TL** (+672 bps).

**Bugün (04.11.2026, 12:34 itibarıyla geçici):** Altın COMEX Aralık vadelisinde 4.054,9, dünkü 17:55'e (3.954,8) göre +%2,50 → z +1,47 → AL. Kesin karar 17:55'te verilir. Sinyal sürerse yaklaşık 30 TRALT AL + 1 XU030D SAT (N'yi 17:55'te vadeli fiyatlarla yeniden hesaplayın), 18:00–18:10'da. Not: TRALT spot gün içinde zaten +%8,6. Kural buna bakmaz. Backtest'te aynı gün TRALT hareketi kontrol edildiğinde de altın katsayısı anlamlı kalıyor (§9).

## 5. Kontrat sayısı (1.000.000 TL sermaye, işlem başı %0,5–1 risk)

- **1 birim = 1 XU030D + N TRALT.** 03.11 uzlaşmalarıyla: TRALT 34,94, XU030 14.412, β 1,29 → N = 32. TRALT tutarı 111.808 TL, XU030 tutarı 144.120 TL.
- **Risk ölçüsü:** 1σ 2 günlük hedge'li hareket. Backtest 2024–26'da işlem başı std 359 bps, yani 1 birimde ≈ 4.000 TL (%0,40). Son 250 günün spot oynaklığıyla (fon krizi dahil) %5,0, yani ≈ 5.600 TL (%0,56).
  - %0,5 risk (5.000 TL): **1 birim**.
  - %1 risk (10.000 TL): **2 birim** (2 XU030D + 64 TRALT). Spot oynaklıkla bütçe ancak 1 birim taşır.
- **Kötü senaryo (1 birim, güncel fiyatla):**
  - 5. persentil işlem −454 bps ≈ −5.100 TL.
  - En kötü işlem −1.409 bps ≈ −15.700 TL (%1,6; 22.06.2023).
  - Maksimum ardışık düşüş −4.196 bps ≈ −46.900 TL (%4,7). Nisan → Ekim 2023 arası, yaklaşık 6 ay sürdü.
  - En uzun kayıp serisi 5 işlem.
- **Teminat (1 birim):** ≈ %15 × 111.808 + %11 × 144.120 ≈ 32.600 TL. Gerçek oranı aracı kurumdan alın.
- **Öneri:** Güven DÜŞÜK olduğu için 1.000.000 TL'de **1 birim**. ~700.000 TL'nin altında 1 XU030 kontratı hedge'i bütçeye göre büyük kalır. Bu durumda stratejiyi hedge'siz uygulamayın; hedge'siz sürüm zayıf (§8).
- Beklenti (8+3 bps maliyetle +35,5 bps × 111.808 TL): 1 birim işlem başı ≈ +400 TL, yılda 54 işlemle ≈ +21.000 TL. Bu, 1 mn TL'nin ~%2'si eder. 15+3 bps maliyetle ≈ +17.000 TL.

## 6. Vade devri

- Girişte vadesine **en az 3 BIST iş günü** kalan en yakın kontratı seçin (vade = ayın son iş günü). TRALT aylık, XU030 çift aylıktır.
- Kasım 2026'da F_TRALT1126 + F_XU0301226 kullanılır. 26.11.2026'dan itibaren (kalan gün < 3) TRALT için F_TRALT1226 kullanılır.
- Bu kuralla 2 günlük bir işlem vadeye girmez. Ancak aynı yönde devam ettirilen bir pozisyon vadeye 3 günden az kalan bir kontrattaysa, devam günü 18:00–18:10'da eski kontratı kapatıp yenisini açın. Bu bir gidiş-dönüş maliyeti daha demektir.
- Backtest bunu modelliyor: her işlem giriş günü seçilen kontratın kendi uzlaşmalarıyla hesaplandı (bedelsiz/temettü düzeltmeli önceki uzlaşma). Araştırmadaki ön vade geçişli getiriye göre fark +0,5 bps.

## 7. Ne zaman yapılmaz

1. **Limit kilidi:** AL sinyalinde TRALT vadelisi tavan kilitliyse, SAT sinyalinde taban kilitliyse girmeyin. 2018–26'da 5 giriş böyle atlandı (uzlaşma sinyaliyle ayrıca 1 çıkış uzadı). Bu kural ortalamayı 3 bps düşürüyor, çünkü atlanan işlemlerin içinde büyük kazançlar da vardı. Ama o fiyattan dolum gerçekçi değil.
2. **Yarım gün / erken kapanış (arife):** 17:55 kuralı uygulanamaz, işlem yok.
3. **TRALT/Koza grubunda olay:** KAP haberi, TVF/TMSF kararı, bedelsiz, temettü, devre kesici. Örnek: 20.08.2024 TVF devri, TRALT +%9,5. Grup faktörü altından güçlüdür.
4. **Altın verisi bayatsa:** ABD/COMEX tatili, TVC:GOLD'da 17:55'te işlem yok. Bu günlerde z ≈ 0 olur ve zaten sinyal çıkmaz.
5. **Hedge kurulamıyorsa** (sermaye küçük, XU030 bacağı dolmadı): tek bacakla yapmayın.
6. **Parametre değiştirmeyin.** Eşik 1,0, tutma 2 gün, σ 250 gün. Eşik duyarlılığı yüksek ve düzensiz: 0,9 → +47, 1,0 → +42, 1,1 → +47, 1,25 → +24, 1,5 → +45 bps.
7. **σ'yı günlük kapanıştan hesaplamayın.** σ, 17:55/18:00 anlık değişimlerinden hesaplanmalı. Yahoo GC=F günlük kapanış σ'sı uzlaşma σ'sından %12 büyük çıkıyor (eşik fiilen 1,12 olur) ve bu sürümde sonuç +42'den +28'e düşüyor.

## 8. Backtest: TAM bu kuralın sonuçları (VİOP uzlaşma fiyatlarıyla)

Dönem 17.12.2018 → 03.11.2026. Getiri, işlem başına TRALT tutarına göre bps cinsinden. Maliyet gidiş-dönüş; "+3" XU030 bacağının payı. "Tik" maliyet senaryosu: TRALT'ta her yönde 1 tik + 4,2 bps komisyon, XU030'da β × (her yönde 1 tik + 4,2 bps).

**Pratik kural (P):**
- Sinyal: 2024-07'den itibaren 18:00 TSİ anlık altın (betik σ'sı). Daha öncesi için saatlik veri yok, VİOP uzlaşma sinyali vekil olarak kullanıldı.
- Uygulama: aynı kontrat, spot β, tam sayı kontrat, vadeli kilit kuralı.

| Maliyet | n | Yılda | Brüt | Net | t | İsabet | IS (<2022) | OOS (2022+) | 2024–26 | En iyi 10 çıkınca |
|---|---|---|---|---|---|---|---|---|---|---|
| 8+3 bps | 423 | 53,8 | +46,5 | **+35,5** | 2,20 | %54,4 | +36,2 (1,66) | +35,1 (1,59) | +54,0 (1,96; n 170) | +14,1 (0,94) |
| 15+3 bps | 423 | 53,8 | +46,5 | +28,5 | 1,77 | %53,7 | +29,2 | +28,1 | +47,0 (1,71) | +7,1 (0,48) |
| tik | 423 | 53,8 | +46,5 | +29,9 | 1,86 | %53,9 | +31,1 | +29,3 | +48,2 (1,75) | +8,6 (0,57) |
| 8+3, devamda işlem yok | 423 | 53,8 | +46,5 | +36,9 | 2,29 | %54,6 | +38,0 | +36,4 | +55,5 (2,01) | +15,6 (1,04) |

- **Yıllar (8+3):** 2019 +35 · 2020 +103 · 2021 −48 · 2022 +6 · 2023 0 · 2024 +47 · 2025 +34 · 2026 +89. Fon krizi (2026-09/10, 7 işlem) −82.
- **İşlem profili:** Tutma 2,0 gün. Ortalama kazanç +262, ortalama kayıp −234 bps. Long işlemler +41,4 (237), short işlemler +27,9 (186).
- **Riskler:** Maksimum düşüş −4.196 bps (birim TRALT tutarının toplamı), en kötü işlem −1.409 bps (22.06.2023).

**Araştırmadan pratik kurala kayıp zinciri (8+3, net bps / t):**
1. Araştırma (yeniden hesap, 03.11'e uzatılmış): +42,1 (2,50).
2. Aynı kontrat + vadeli β: +42,6 (2,52).
3. + spot β (Yahoo): +42,2 (2,58).
4. + tam sayı kontrat (1 XU030 + N TRALT): +42,5 (2,59). Uygulama kaybı yok.
5. + vadeli limit kilidi kuralı: +39,5 (2,40), −3 bps.
6. + pratik sinyal (17:55/18:00 anlık altın, 2024-07+): **+35,5 (2,20)**, −4 bps.
- Hedge'siz (yalnız TRALT): +25,2 (1,31), en iyi 10 çıkınca +1,4 (0,08). **Hedge'siz yapmayın.**

**17:45–17:55 fiyatıyla hesaplanan sinyalin farkı:**
- 5 dk veri (27.08–03.11.2026, 46 gün):
  - 17:55 sinyali uzlaşma z'siyle 0,990 korele. 6 sinyal gününün 6'sı aynı, işlemler birebir aynı.
  - 17:45'te korelasyon 0,983; 6 sinyalin 5'i aynı.
  - Uzlaşmaya en yakın an 18:00–18:10 (0,993). VİOP altın uzlaşması bu penceredeki fiyat.
- Saatlik veri (07.2024 → 11.2026, 546 gün):
  - 18:00 anlık z, uzlaşma z'siyle 0,977 korele. Uzlaşma sinyallerinin 155/170'i 18:00'te de sinyal veriyor; ters işaret 0.
  - Aynı dönem kural sonucu: uzlaşma sinyali +80,1 (t 2,44; n 138), 18:00 betik σ'sıyla +67,3 (2,02; n 131), 17:00 sinyali +73,4 (2,36).
  - Zamanlama kaybı 7–13 bps/işlem. Bu fark, işlem başı ~360 bps oynaklık yanında gürültü düzeyinde.
- Yahoo GC=F ham (vade sıçramalı) sürüm de +59,7 veriyor. Ama sıçrama günlerinde sahte sinyal riski var: Yahoo'da aynı kontrat kullanılmalı, TradingView'da TVC:GOLD.

## 9. Bu bir lead-lag mı?

**Kısmen, ama klasik "biri önce, diğeri ertesi gün" değil.**
- TRALT altına aynı gün ve hızla tepki veriyor: z'lerin aynı gün korelasyonu 0,25, 5 dakika içinde fiyatlanıyor. Ancak tepki eksik kalıyor; altın şokunun bir kısmı sonraki 1–2 günde TRALT'a geçiyor.
- Bunu destekleyen regresyon: TRALT'ın 2 günlük hedge'li ileri getirisi; altın z, TRALT'ın kendi aynı gün hareketi ve XU030 birlikte kontrol edildi (Newey-West).
  - Altın katsayısı +25 bps/σ, **t 2,84**.
  - TRALT'ın kendi hareketi +2,8, **t 0,29**.
- Yani bu **momentum değil**: TRALT'ın kendi yükselişi geleceği öngörmüyor, öngören altın.
- **Zamanlama artefaktı da değil:** sinyal 17:55'te biliniyor, giriş aynı akşamın uzlaşmasında.
- Bilgi çabuk sönüyor: dünkü altının etkisi yok (t 0,71; araştırmada t 0,07–0,5).
- Etki rejime bağlı: z katsayısı 2019–20'de güçlü, 2021–22'de sıfır, 2023–24'te zayıf, 2025–26'da yeniden pozitif.

## 10. Güncel durum (03.11.2026 kapanışı; 04.11 12:34 itibarıyla)

- 30.10: uzlaşma z −2,01 (17:55 anlık z −1,94) → SAT. 03.11 uzlaşmasında −241 bps ile kapandı.
- 02.11: z +0,57 (anlık +0,77) → sinyal yok. 03.11: z −0,27 (anlık −0,31) → sinyal yok.
- **03.11 kapanışı itibarıyla açık pozisyon yok.**
- 04.11 geçici: altın +%2,50, z +1,47 → **AL adayı**. 17:55'te teyit edin. Tetik: COMEX Aralık ≥ 4.022,7 (AL) / ≤ 3.888,0 (SAT); spot için yüzde olarak ±%1,70.
- Yarın (05.11) için yaklaşık tetik, bugün 17:55 fiyatı × e^±0,0171. Şu anki fiyatla ≈ 4.124,7 / 3.986,3 (COMEX).
- Kontratlar: F_TRALT1126 + F_XU0301226 (TV: BIST:TRALTX2026, BIST:XU030DZ2026). 1 birim = 1 XU030D + 30–32 TRALT.

## 11. Riskler

- **Rejim:** 2021–23'te etki yoktu ya da negatifti (2021 −48 bps/işlem). Önceki çalışma 2023Y2–2024Y2'de altın–TRALT bağının koptuğunu buldu.
- **Az sayıda büyük işlem:** En iyi 10 işlem (%2) çıkınca t 0,94. Kuyruk olayları sonucu belirliyor.
- **Son dönem zayıf:** Fon krizi (Eyl–Eki 2026) 7 işlem, ortalama −82 bps.
- **Çoklu test:** Araştırmada ızgara düzeltmeli p 0,024. Kaba Bonferroni ×32 ile 0,77.
- **Olay riski:** TRALT bir Koza grubu/TVF olay hissesi. Grup haberi altını bastırır.
- **Dolum:** Uzlaşma (VWAP) fiyatından dolum varsayıldı; 18:00–18:10'da kayma olabilir. Limit kilidinde dolum olmaz.
- **Veri vekilleri:** 2024-07 öncesi pratik sinyal ölçülemedi (Yahoo saatlik veri 730 gün), uzlaşma sinyali vekil olarak kullanıldı. Pine göstergesi derlenmedi.
- **Teminat ve kaldıraç:** Pay vadelisinde teminat ~%13–17, XU030'da ~%11. Gece boşluğu (ABD gecesi) TRALT'ta büyük olabilir.

## 12. Dosyalar

- `sinyal_altin.py`: günlük sinyal betiği (pandas/numpy/requests; Yahoo). `python3 sinyal_altin.py --sermaye 1000000 --risk 0.75 [--f-tralt 34.94 --f-xu030 14412]`
- `altin.pine`: TradingView Pine v5 göstergesi (BIST günlük grafik). Derlenmedi; ilk kullanımda betik çıktısıyla karşılaştırın.
- `kod/01_repro.py` (araştırmanın yeniden üretimi), `kod/03_backtest.py` (pratik kural backtest'i), `kod/02_timing.py` (zamanlama), `kod/04_leadlag.py` (lead-lag regresyonu), `kod/pl.py` (yardımcılar), `kod/ydl_a.py` (Yahoo indirici, kendi dizinine yazar).
- `sonuc/backtest_ozet.csv`, `sonuc/pratik_islemler.csv`, `sonuc/seriler.csv`, `sonuc/zamanlama_corr.csv`, `sonuc/leadlag.txt`, `sonuc/sinyal_cikti.txt`, `sonuc/log03.txt`.
