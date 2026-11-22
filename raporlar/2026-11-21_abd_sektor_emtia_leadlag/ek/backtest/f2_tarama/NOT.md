# F2b notu: körlemesine tarama, yürüyen seçim, geride kalan, ETF ters öncülük, yabancı seans farkı

Betik: `kod/f2_tarama.py hepsi` (~3 dk). Veri son günü 20.11.2026.

**Sonuç: kullanılabilir (SAĞLAM ya da gerçek KOŞULLU) sinyal yok.** 20 Kasım kapanışında bu aileden açılacak pozisyon yok.

## Kaç test, kaç yanlış pozitif beklenir
- Tarama: 403.876 çift (738 öncü × 548 hedef, h=1). İşlem testi: 601 satır (+45 kıyas, +42 çürütme varyantı). Toplam 404.477.
- Taramada "IS |t| ≥ 2,5 ve OOS aynı işaret t ≥ 2,5" geçen 136 çift. Şansla beklenen: teorik 31; taramanın kendi kuyruk oranlarıyla 74 (IS kuyruğu teorinin 1,6 katı). Yani geçenlerin en az yarısı sahte.
- İşlem testlerinde beklenen: SAĞLAM 0,02, KOŞULLU 0,08 (keşif satırları taramadan seçildiği için gerçekte daha yüksek).

## 1) Körlemesine tarama
- IS'te BH q=%10: 171 çift (|t| ≥ 4,10). OOS'ta tutan (aynı işaret, t ≥ 2,5): **6 (%3,5)**. Şans: teorik %0,62, ampirik %0,97. Hizalı OOS t medyanı 0,79.
- 171'in 65'inde hedef IMPUY (tezgah üstü, kapanışı bayat). OTC, bayat ve ikizler çıkınca **1/100 = %1,0: şansla aynı.** Negatif işaretli 34 seçimin hiçbiri tutmadı.
- Doz–yanıt: IS |t| 4–5 olan çiftlerin OOS hizalı t ortalaması 0,5 (yaklaşık %90 büzülme).
- OOS p değerlerine BH (8.185 IS seçimi): 5 çift (EZU/VGK/WOOD→EWH, PRU→HMC, SBSW→IMPUY).
- İşlem testi (B1/B1r, maliyetli): ön kayıtlı yoldaki 6 çift: IMPUY'da h=1 etkisi ertesi açılış girişinde −11…−19 bps → bayat fiyat, ELENDİ; h=3'te 3 İZLE. Keşif (+) 30 çift, 180 test: **hiçbiri İZLE bile değil.** Keşif (−) 30 çift: VHT→INTC kural gereği KOŞULLU (h=1: 34 bps, IS t 3,1, OOS t 4,0), 9 İZLE. Hiçbiri öncüye özgü değil.

## 2) Yürüyen seçim (asıl test)
- Her yıl ~1.000 çift, ~400 hedef. Pencerenin %80'i ortakken seçilen çiftlerin yalnız %22–34'ü ertesi yıl yeniden seçiliyor: seçim büyük ölçüde gürültü.
- Maliyetsiz: işlem başına 2,2 bps (t 3,7; IS 3,0, OOS 2,6). Yalnız pozitif öncüler 4,1 bps; negatifler 0,1 bps.
- Maliyetli: **−7 bps**; her alt dönemde −5,5…−8,4. 36 satırın hepsi ELENDİ.

## 3) Grup içinde geride kalan
- Maliyetsiz AL bacağı (h=1, sürüklenme düzeltilmiş): 8,9 → 4,8 → 4,9 → 2,8 → 0,1 → 2,9 bps (2005-09 … 2024-26); hiçbir dönemde t ≥ 1,6.
- Maliyet duyarlılığı (AL, h=1): 5 bps → −0,5; 10 → −5,5; 20 → −15,5. h=3, 5 bps: +3,9 (t 0,6; OOS +1,5).
- Likidite yarıları, büyük grup hareketi, sektör ETF artığı, SPY hedge: 34 satırın hepsi ELENDİ.

## 4) ETF ters öncülük
- SPY→IWM, QQQ→IWM, XLF→KRE, SPY→IJR, SPY→XBI: öncü katsayısı −5…−17 bps/z (t −1,9…−3,3). Hedef öncüyle hedge edilince IS'te sıfır (SPY→IWM −0,06 bps, t −0,05), OOS −1,9 (t −1,0). **Öncüye özgü değil: piyasanın kendi dönüşü betayla taşınıyor.** İstisna 15 hücrenin 2'si (XBI OOS, KRE 2024-26).
- İşlem testi: SPY→IWM h=1 +6 bps (IS t 1,2; OOS 0,8). 36 satır ELENDİ.

## 5) Yabancı seans farkı
- 11 çift, 99 test: hepsi ELENDİ. Kur ETF'i düzeltmesi fark oynaklığını %5–17 azaltıyor (EWJ'de azaltmıyor); TWD ve KRW düzeltilemedi.
- BHP ve RIO'da fark kapanmıyor, açılıyor (−16…−31 bps; ters yön, sınıflanmaz). TSM prim sinyali IS t 2,8–3,1 → OOS 0,1.

## Çürütme (VHT→INTC)
Öncü 1 gün gecikince 4,5 bps (t 0,7). VHT yerine SPY: 16,9 bps (t 2,6). Sinyal günlerinde SPY z ortalaması −1,42: bu bir piyasa düşüş günü sinyali. "VHT var, SPY yok" günlerinde IS t 0,66. En büyük iki işlem INTC'nin tek günlük −%26 ve −%29 çöküşü (02.08.2024; 30.10.2026 doğrulanmadı). **Kullanılamaz.**

## Veri sorunları
- IMPUY (OTCQX, günde ~1 mn $) bayat hedef listesinde yoktu; betikte OTC bayrağı eklendi.
- BABA–9988.HK verisi 26.11.2019'da başlıyor: IS yok, A koşulu sınanamaz.
- Yerel tatilde yerel getiri 0 sayılıyor: tatil günlerinde sahte fark oluşur.
- Havuz plasebosu 300 tekrarlı (1.000 yerine); hiçbir havuz satırında gerekmedi.
