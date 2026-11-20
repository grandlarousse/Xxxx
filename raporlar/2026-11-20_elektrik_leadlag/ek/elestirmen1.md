araç: 23/45

# Eleştirmen 1: rakam ve çıkarım denetimi (RAPOR.md, bölüm 1–3)

Kaynak yolları `/home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/` klasörüne göredir. "Eleştirmen hesabı" yazan yerler kaynak dosyada hazır durmayan, oradaki rakamlardan benim türettiğim değerlerdir. RAPOR.md değiştirilmedi.

## KRİTİK

**K1. "S1 ve S2 kasada, önceden kayda geçirilen ölçüyle ve çoklu test düzeltmesiyle doğrulandı." (3.2; ayrıca 6. bölümde "üç dönemde de var")**
- Sorun (a): düzeltmenin eşiği yazılmamış. `ek/YONTEM_EK.md` E11 ve E13: Holm, alfa 0,10, 10 kural. `ek/kasa_sonuc.csv`: S1 p 0,0068, S2 p 0,0111. Alfa 0,05 olsaydı S2 geçmezdi (eşik 0,0083), S1 kıl payı geçerdi (eşik 0,0071).
- Sorun (b): rapor sade seçim kuralını ve "en kötü beşte birlik"i çöküş hisseleri kirlenmesi yüzünden geri çekiyor, aynı duyarlılığı S1 ve S2'ye uygulamıyor. `ek/v1_yeniden_momentum.csv`: üç hisse çıkınca kasa S1 +59 (t 1,67), S2 +82 (t 2,11). Tek yönlü p yaklaşık 0,047 ve 0,018; Holm eşikleri 0,014–0,017 olduğu için ikisi de geçmiyor (eleştirmen hesabı, normal yaklaşım).
- Sorun (c): kasadaki S1 büyüklüğü kıyasa göre +17 ile +93 arasında oynuyor. `ek/v3_curutme_momentum.csv` (S1, kasa): ±60 gün sinyalsiz günlere göre +43 (t 1,4); trend kontrollü regresyon +20 (t 0,4). `ek/kasa_sonuc.csv`: piyasaya göre (`dol_mkt`) +17 (t 0,65); ilk kayıtlı ölçüyle (`dol_own`) +24 (t 0,7).
- Sorun (d): 2023 sonrası havuzda S1 ve S2 yalnız hafif düzeltmeden (BH, q 0,10) geçti, Holm'den geçmedi (`ek/tum_oos_sonuc.csv`: `holm_tum_OOS` False). Rapor bunu açık söylemiyor.
- Öneri: "S1 ve S2 kasada önceden kayıtlı ölçüyle (dönem-nötr kıyas; Holm, alfa 0,10) geçti. Bu sonuç kıyasa duyarlı: üç çöküş hissesi çıkarılınca S1 +59 (t 1,7), S2 +82 (t 2,1) oluyor ve aynı eşik geçilmiyor; trend kontrol edilince S1 kasada +20 (t 0,4). 2023 sonrası havuzda ikisi de yalnız hafif düzeltmeden geçti. 'Doğrulandı' yerine 'kayıtlı ölçüyle geçti, sağlamlık sınamalarında zayıfladı' denmeli." 6. bölümdeki "istatistiksel olarak üç dönemde de var" ifadesi de buna göre yumuşatılmalı (sınama döneminde t 1,8 ve 1,2).

**K2. "medyan +62, işlemlerin %59'u artıda" (2.5) ile "çıkışı son sinyalden 3 gün sonraya ertele" (2.2, madde 6) aynı uygulamayı anlatmıyor**
- Sorun: 2.5'teki rakamlar "pozisyondayken gelen sinyali yok say, 3. gün sat" uygulamasına ait (82 örtüşmeyen işlem). 2.2'de önerilen ise ertelemeli tutma. Onun dağılımı çok farklı.
- Kaynak: `ek/v5_sepet.csv` (`3_politika`, S1, HAVUZ). "yoksay": 82 işlem, ham ort. +73, zarar olasılığı %41. "uzat": 40 giriş, ortalama tutma 7,1 gün, ham ort. +188, zarar olasılığı ham %55, maliyet sonrası %57,5, en kötü %5 −477 bps, t 1,7. `ek/v3_curutme_momentum.csv` (`5_yillik`): pozisyon dönemi ort. +154, medyan −44, kazanan %42, en iyi 3 dalga hariç ort. +25, en kötü −533.
- Ek: 7 günlük tutmada faiz 32–44 değil yaklaşık 75–105 bps olur (eleştirmen hesabı, aynı %27–37 oranıyla). 2.6'daki "20 işlem" ölçütü ertelemeli tutmada yaklaşık iki yıl eder.
- Öneri (ikisinden biri): (1) 2.2 madde 6: "Pozisyondayken gelen yeni sinyali yok say; 3. işlem günü sat." (2) Erteleme kalacaksa 2.5'e: "Ertelemeli tutmada yılda yaklaşık 10 giriş, ortalama 7 gün. Girişlerin %55–58'i zararla kapanır, medyan −44 bps. Ortalama (+154…+188 bps) birkaç büyük dalgadan gelir; en iyi 3 dalga hariç +25. En kötü dalga −%5,3."

**K3. "Göreli üstünlük her yıl var; mutlak kâr yok." (3.4)**
- Sorun: S2 için yanlış. 2024'te S2 ham +10, sıradan gün +27: S2 sıradan günün 17–18 bps altında (`ek/v3_curutme_momentum.md` madde 4: "2024'te `per` −18"). S1'de fark her yıl artı ama yalnız 2023'te anlamlı: `ek/v3_curutme_momentum.csv` yıl içi kıyas +167 (t 2,2), +72 (1,2), +21 (0,5), +75 (1,4). "Mutlak kâr yok" da kesin değil: ham getiri her yıl artı; eksik olan maliyet ve faiz sonrası kâr.
- Öneri: "S1 her yıl sıradan günden iyi, ama fark yalnız 2023'te anlamlı (t 2,2; sonraki yıllar t 0,5–1,4). S2 2024'te sıradan günün 18 bps altında kaldı. Nakde göre S1 2023 ve 2025'te artıda, S2 yalnız 2025'te."

## ÖNEMLİ

**Ö1. 3.3 tablosu, "Kalan" sütunu: "yaklaşık +6", "−18", "−4", "−6"**
- Sorun: S1 ve S2 satırları maliyet 30 ile, S3 satırları 35 ile hesaplanmış; tabloda ise "30–35" yazıyor. Aralığın üst ucuyla S1 +2 ve −23, S2 −9 ve −11 (eleştirmen hesabı). Ayrıca "S2, kasa" satırında ham +57 yazıyor, kalan −6 ise ham 59 ile hesaplanmış.
- Kaynak: `ek/v3_curutme_momentum.csv` (`5_maliyet`): temel maliyet 30,2 ve 30,4; kalan +6,5, −18,1, −4,4, −6,0. `ek/kasa_sonuc.csv`: S2 `dol_raw_KASA_bps` 59,0; `maliyet_temel_bps` 35,1–35,8.
- Öneri: S2 kasa ham "+59". Kalan sütununa aralık: S1 "+2…+6" ve "−23…−18"; S2 "−9…−4" ve "−11…−6". Tablo altına: "Kalan, maliyet 30 ile hesaplandı; 35 ile 5 bps düşer."

**Ö2. "S3, 2023 sonrası … yaklaşık +100" (3.3)**
- Sorun: bu rakam kapanış değeriyle kurulan, önceden bilinemeyen sinyale ait. Rapor 3.7'de uygulanabilir sürümü veriyor ama tabloya yansıtmıyor.
- Kaynak: `ek/v6_zamanlama.csv` (S3, 18:00, temel eşik): 2023 sonrası 157 → 90 (t 2,1); kasa 41 → 11 (t 0,26). `ek/v4_curutme_diger.md`: "olay başına brüt +40 … +70, net 0 … +40". Kasada hisse bazında yalnız ENJSA artıda (+102; AKSEN +7, ODAS +15).
- Öneri: tabloya satır: "S3, 18:00 kararıyla: 2023 sonrası kalan yaklaşık +35, kasada yaklaşık −15 (yaklaşık hesap)". Metne: "Çürütme ekibinin beklentisi olay başına net 0…+40 bps."

**Ö3. "Bu üç hisse çıkarılınca S1 kasada +59 (t 1,7) … kasadaki büyüklüğün yaklaşık üçte biri buradan geliyordu." (3.2)**
- Sorun: tablo ortak kütüphane rakamı (86 ve 95), çöküşsüz rakamlar bağımsız koddan (93 → 59, 103 → 82). Aynı kodla karşılaştırma: `ek/v3_curutme_momentum.csv` (`3_kimde`): S1 kasa +56 (t 1,6), havuz +64 (t 2,1); S2 kasa +77 (t 2,0), havuz +60 (t 1,9). "Üçte biri" S1 için doğru (%35), S2 için beşte biri (%19).
- Öneri: "Aynı hesapla üç hisse çıkınca S1 kasada 86 → 56 (t 1,6), S2 95 → 77 (t 2,0). S1'de büyüklüğün üçte biri, S2'de beşte biri buradan geliyordu."

**Ö4. Güven etiketleri: S1 "Orta", S2 "Orta-düşük" (2.1)**
- Sorun: `ek/v3_curutme_momentum.md` hükmü ikisi için de "ÇÜRÜTÜLDÜ" (bağımsız alım kuralı olarak). S2'nin kendi katkısı zayıf: zirve olmayan S2 günleri +35 (t 0,9), ham +32, maliyet sonrası +2 (`ek/v5_sepet.csv`, `3_birlesim`, yalnizS2); eşik büyüdükçe etki artmıyor.
- Öneri: S1 "İstatistiksel etki: orta; kâr: yok. Yalnız zamanlama süzgeci". S2 "Düşük; S1 ile aynı gün gelmedikçe tek başına kullanma".

**Ö5. "K Kaçınma (temiz kıyas) −17 (−0,7) / −70 (−2,7) / −67 (−2,5) / −69 (−3,6)" (3.2)**
- Sorun: satır 1 günlük getiridir, tablonun öbür satırları 3 günlük. Ayrıca rakamlar kuralın tamamına değil, "eşit ağırlıklı sektörün 5 puan gerisinde olup tabana değmemiş" alt kümeye ait. Etki keşif döneminde yok. Göstergenin kullandığı XELKT kıyasıyla aynı alt küme kasada −38 (t −1,5).
- Kaynak: `ek/v4_curutme_diger.csv`: "K2 v4" satırları (rapor rakamı); "XELKT endeksinden >=5 puan geride, tabana degmemis" −28 (−1,3) / −61 (−2,4) / −38 (−1,5); "BIRLESIK5" −81 / −102 / −236 (kirli kıyas).
- Öneri: satır adı "K Kaçınma, tabana değmeyenler (ertesi gün, 1 günlük)". Not: "Etki 2010–2022'de yok; XELKT kıyasıyla kasada −38 (t −1,5)."

**Ö6. [eksik uyarı] İlk kayıtlı ölçüyle sonuç**
- Rapor 3.8 ve 4'te ölçünün değiştiğini söylüyor, rakam vermiyor. `ek/YONTEM_EK.md` E11: "5 birincil kuralın hiçbiri geçmedi (en küçük tek yönlü p = 0,33)". `ek/kasa_sonuc.csv` (`dol_own`): S1 sınama +20 (t 0,4), kasa +24 (t 0,7); S2 +3 (t 0,1), kasa +30 (t 0,7).
- Öneri (3.8'e): "İlk ölçüyle S1 ve S2 sınamada ve kasada anlamsızdı (t 0,1–0,7). Bulgu, ölçü düzeltmesinin doğru olduğu kabulüne dayanır."

**Ö7. [eksik uyarı] Trend denetimi: "aylık trend yapaylığı değil" (3.5)**
- `ek/v3_curutme_momentum.csv` (`1_rejim`): XELKT 20/60 günlük getirisi ve XU100 kontrol edilince S1 +45 (t 1,2), kasada +20 (t 0,4); "zirveye ≤ %2 yakın günler" içinde fark +40 (t 1,3), kasada +21 (t 0,6). S2 +69 (t 2,2).
- Öneri: "Trend kontrol edilince S1'in kendi katkısı +45'e (t 1,2) iniyor: zirve koşulu, 'sektör zaten yükseliyor' bilgisinin üstüne az şey ekliyor."

**Ö8. [eksik uyarı] Düşüş günü uyarısı ve bugünkü durum**
- `ek/v3_curutme_momentum.csv` (`8_asagi`): XELKT z ≤ −1 gününden sonra sepet ertesi gün −48 (t −2,2), kasada −109 (t −3,2). `ek/v3_curutme_momentum.md`: "z ≤ −1 gününde alınmaz"; keşifte −22, sınamada −2 (tutarsız). `araclar/ornek_cikti_2026-11-20.txt`: bugün XELKT z −1,11.
- Öneri (2.1 "Bugünkü durum"a): "Bugün XELKT z −1,1. Böyle günlerden sonra sepet 2023 sonrasında ertesi gün ortalama −48 bps (kasada −109); doğrulanmış kural değil, ama bugün alım için neden yok."

**Ö9. [eksik uyarı] Taban kilidi kasa döneminde ağırlaştı: "işlemlerin yaklaşık %1'inde … ortalama kayıp %15" (2.5)**
- `ek/v5_sepet.csv` (`5_risk`, S1): kasada sinyal günlerinin %28'inde sepette çıkışı kilitli en az bir hisse (havuz %21); kilitli işlem ortalaması −%21; bir MAGEN işlemi −%32. `ek/v6_zamanlama.md`: bütün günlerde çıkış günü taban kilidi kasada %1,7 (genel %0,8).
- Öneri: "Kasa döneminde her dört sinyal gününün birinde sepette çıkışı kilitli en az bir hisse vardı; kilitli işlemlerin ortalama kaybı %21, en kötüsü %32."

**Ö10. [eksik uyarı] "VİOP baz, hacim, açık pozisyon … Kullanılabilir sinyal yok" (3.6; kısa yanıt 1. madde)**
- `ek/tum_oos_sonuc.csv`: `A6_V1_dbaz_uzl_z1_yuk_spotAL_h3` (vadeli bazı yukarı sıçrayınca üçlüde spot AL, 3 gün) 2023 sonrasında +75 (t 2,07; 140 bağımsız olay), hafif düzeltmeden geçen 10 kuraldan biri. Holm'den geçmedi, keşifte t 1,6, kasada ayrıca sınanmadı; `ek/w3c_gecikme.md`: "sönüyor".
- Öneri: "Doğrulanmış sinyal yok. Bir baz kuralı 2023 sonrasında +75 (t 2,1) verdi ama en sıkı düzeltmeden geçmedi ve kasada sınanmadı; izleme."

## KÜÇÜK

1. **"XELKT artışı bunun yarısından az (bugün < %1,05)" (2.1, S3).** "Bunun" XU030 oynaklığını gösteriyor (yarısı %0,93); %1,05 XELKT'nin kendi oynaklığının yarısı (`araclar/ornek_cikti_2026-11-20.txt`: "XELKT z < 0,5"). Öneri: "XELKT artışı kendi 60 günlük oynaklığının yarısından az".
2. **"ham ortalama +74 bps, medyan +62, %59'u artıda" (2.5).** +74, 174 sinyal gününün ortalaması (medyanı +78); +62 ve %59, 82 örtüşmeyen işleme ait (ortalaması +73; maliyet sonrası kazanan %57). Kaynak: `ek/v5_sepet.csv`, `ek/v3_curutme_momentum.csv`. Öneri: "82 örtüşmeyen işlemde ham ortalama +73, medyan +62; %59'u artıda (maliyet sonrası %57)".
3. **Yuvarlama.** `ek/tum_oos_sonuc.csv`: S1 ham 74,55 (rapor +74; doğrusu +75), S2 ham 63,80 (rapor +63; doğrusu +64). Kalan sütunu değişmiyor.
4. **"fazla getiri 78'den 46'ya" (2.4).** 78 sepet düzeyi ölçü, tablodaki 83 hisse düzeyi ölçü (`ek/v3_curutme_momentum.csv`: 77,6 ve 82,6). Öneri: "(aynı ölçüyle 78'den 46'ya)". t değeri `ek/v5_sepet.csv`'de 1,33, `ek/v3_curutme_momentum.csv`'de 1,40.
5. **15 hisselik liste, "…BIOEN, KLYPV" (2.3).** `ek/v5_sepet.csv` ile aynı; ama rapor "güncel listeyi `sinyal.py` verir" diyor ve aynı günün çıktısında 20. sıra TATEN, KLYPV 21. (ikisi de 79 mn TL). Öneri: "sıra eşit hacimlerde değişebilir (bugün KLYPV ve TATEN)".
6. **"100 bin TL'lik sepet sorunsuz" (2.3).** `ek/v5_sepet.md`: hisse başına 2.381 TL; "LYDYE alınamaz (2.902 TL)". Öneri: "LYDYE dışında sorunsuz".
7. **"İkisi yarım puan ayrışabilir" (2.7).** `araclar/hisse_sektor_fark.pine`: "yarım puan ve daha fazla". Öneri: "yarım puan ve daha fazla".
8. **"VİOP satış kuralları | 6 kural" (3.6).** Tablolarda 5 satış kuralı sayılıyor (`ek/tum_oos_sonuc.csv`'de 4, `ek/kasa_sonuc.csv`'de 1); t aralığı −0,7…+1,0 doğru. 6 sayısının kaynağı bulunamadı.
9. **"sekiz sinyal ailesini yalnız keşif verisiyle taradı … 41 kural" (3.1).** Gün içi ailesi (A7) 2023-12 → 2025-06 verisiyle çalıştı ve kural dondurmadı (`ek/a7_gunici.md`). 41 kuralın ikisi aynı (S2: `A2_xelkt_z1_tum_h3` = `A5_mom1_sepet_h3`): 40 ayrı kural, hafif düzeltmeden geçen 9 ayrı kural.
10. **"2023 → 2025/6" sütunu (3.2).** Rakamlar `ek/kasa_sonuc.csv`'den. Kasa öncesi tablo `ek/oos1_sonuc_donem_notr.csv` biraz farklı: S1 +87 (1,9), S2 +52 (1,2), S3 +209 (2,8), S1 üçlü +47 (1,0). İşaretler aynı; bir cümleyle belirtilmeli.
11. **"'XELKT geride' koşulu olmadan da aynı sonuç çıkıyor (+98, t 2,7)" (3.5).** +98, S3'ün +157'siyle aynı değil; koşulun ek katkısı +82 (t 1,3), kasada −6 (`ek/v4_curutme_diger.csv`). Öneri: "koşul olmadan da +98 (t 2,7); koşulun ek katkısı anlamsız".
12. **"tersi doğru, geride kalan geride kalmaya devam ediyor" (2.4).** Yalnız sert geride kalanlar için geçerli. Tabanda kapananlar çıkınca en kötü beşte birlik kasada −3 (t −0,5) (`ek/v4_curutme_diger.csv`, K1 v2). Öneri: "yetişme yok; sert geride kalanlar (taban, 5 puan) ertesi gün de zayıf".
13. **"S1'de −3 bps, S2'de −6 bps (2017 sonrası)" (3.7).** Doğru; kasada kayıp daha büyük: S1 −10, S2 −12 (`ek/v6_zamanlama.csv`).

## Sayım

- Kontrol edilen sayı (bps, t, yüzde, adet, tarih, fiyat düzeyi; bölüm 1–3): yaklaşık 257.
- Doğru: 251.
- Yanlış ya da kaynakla tutarsız: 5 (S2 kasa ham +57 → +59; S1 ham +74 → +75; S2 ham +63 → +64; "yarım puan" → "yarım puan ve daha fazla"; 15'lik listenin son hissesi araç çıktısıyla uyuşmuyor).
- Kaynağı bulunamayan: 1 ("6 kural").
- Rakamı doğru, çıkarımı yanlış ya da yanıltıcı: K1, K2, K3, Ö1–Ö5, KÜÇÜK 1, 11, 12.
- Bakılmayan: 4.–6. bölümler; `ek/a*_sonuc.csv` büyük tabloları (ilgili rakamlar `.md` notlarından ve özet tablolardan kontrol edildi); `ek/*_donus_ham.md` dosyalarından yalnız v5 ve v7 arandı.
