# V4 — çürütme: S3, T1/T2, K1/K2 (kasa açık; betimsel, yeni kural dondurulmadı)

Kod `kod/v4_curutme_diger/run.sh`; tablo `ek/v4_curutme_diger.csv` (496 satır; S3 olay listesi içinde). Ana tablo birebir yinelendi (S3 havuz +156,7, t 3,01; bağımsız kısa kodla +157,3). Rakamlar bps, maliyet öncesi; sıra IS / OOS-1 / kasa.

## S3 — XU030 gecikmesi: ÇÜRÜTÜLDÜ (öneri olarak; biçimsel sınıf “güç yetersiz”)

1. **Kuyruk.** 2023+: 45 sinyal günü, 39 bağımsız olay. En iyi 2 gün (2023-05-26, 2024-04-04; seçim haftaları) çıkınca +106 (t 2,7); 3 çıkınca +94 (2,4); 5 çıkınca +70 (1,9); 10 çıkınca +25 (0,7). Yıllar: +173, +189, +204, 2026 +50. Holm eşiğini (41 kural) yalnız o iki günle geçiyor.
2. **Gecikme değil, momentum.** Aynı günlerde XU030'un kendisi 3 günde +54 / +139 / +34. β korumalı üçlü +29 (t 1,2) / +97 (2,0) / +11 (0,2). Gecikme koşulunun katkısı (sektör geride − sektör de güçlü): +61 (1,8) / +131 (1,5) / **−6 (−0,1)**. 2023+'da koşulsuz “XU030 z ≥ 1” β korumalı +70 (t 2,8), sektör de güçlüyken +72: XELKT koşulu bir şey eklemiyor. Bu koşulsuz etki IS'te yok (+4).
3. **Kıyas.** Merkezli ±60 gün: +63 / +205 / +46; aynı ayın diğer günleri: +50 / +208 / +63. Kasa her ölçüde t ≤ 1.
4. **Karar anı (2023+).** Sinyalin 17:00'de %58'i, 17:30'da %63'ü (sinyallerin %29'u yanlış; sonuç +80, t 1,3), 18:00'de %84'ü görünüyor. 17:50 için XU030 5 dakikalık verisi yalnız 410 gün: 18 sinyalin 16'sı yakalanıyor, 21 sinyalin 5'i yanlış. Geç oluşan sinyaller en iyileri (+193 … +387): kazanç XU030'un kapanışa doğru güçlendiği günlerde. Üçlünün 17:30 → kapanış getirisi sinyal günlerinde 0. Uygulanabilir yol 17:50–17:55'te bakıp kapanış seansına emir; t+1 girişi +63 (t 1,3).
5. **Vadeli ve maliyet.** Vadeli aynı olaylarda 3 günde spotun 48–54 bps gerisinde (taşıma 14–15 bps/gün). ODAS 4,35 TL: bir fiyat adımı 23 bps. Spot temel maliyet 30: işlem başına net OOS-1 +191, kasa **+11** (muhafazakâr −14).
6. **Hisse ve risk.** Havuzda üç hisse de artı (+153, +145, +172); kasada ENJSA +102, AKSEN +7, ODAS +15. En kötü olaylar (üçlü, ham 3 gün): −508, −310, −260; tek hisse −892.

**Beklenti:** olay başına brüt +40 … +70, net 0 … +40; yılda 10 olay. Para yatırılacak kural değil; kâğıt üstünde izlenir.

## T1 (model): ÇÜRÜTÜLDÜ (öneri olarak) · T2 (sade): ŞARTLI KABUL (yalnız seçim süzgeci)

7. Kasadaki +41 / +38, çıkış ertelemeli hesabın çöküş serileriyle şişmesi. Düz ertesi gün getirisiyle T1 +5,5 / +22,9 / +19,4; T2 +9,2 / +16,3 / +15,3. BIGEN, LYDYE, MAGEN, ESEN çıkınca kasa T1 +13,3 (t 3,1), T2 +8,3 (1,4); kıyas “son 5 günde tabansız” olunca +6,7 (1,6) ve +5,2 (0,9). Seçilenlerin evren medyanını geçme oranı %51 ve %50: isabet yok. Kazanç tavandan gelmiyor: T2 seçilenlerinde ertesi gün tavan %1,4 (evren %1,9), taban %0,2 (evren %1,2). ±%5 kırpılınca havuz T1 +15,7 (t 6,4), T2 +12,0 (3,7).
8. **Sadeleştirme.** Taşıyan koşul oynaklık. Yalnız “sakin yarı”: +5,4 (t 3,2) / +8,0 (3,4) / +12,2 (4,6); çöküşsüz kasa +9,1 (3,5). Yalnız “günün en üst üçte biri”: +3 / +4 / +4 (t ≈ 1). İki koşul (sakin + güçlü): +8,8 / +12,3 / +14,9. TradingView vekili (20 günlük ortalama gün içi aralık): +7,7 / +10,5 / +17,2.
9. **Birleşim (DOĞRULANMADI).** S1 günü T2 seçilenleri − sepet, 3 gün: −41 (t −2,5) / +30 (1,0) / +22 (1,0); S2 günü −29 / +32 / +51. IS'te ters işaret: desteklenmiyor.

**Şart ve beklenti:** al-sat kuralı değil (maliyet ~36). Zaten alınacaksa 20 günlük oynaklığı sektör medyanının altındaki hisse; fark günde +5 … +12 bps, isabet %50.

## K1: ÇÜRÜTÜLDÜ (bağımsız bulgu olarak) · K2: ŞARTLI KABUL

10. K1 düz getiriyle −12,5 / −25,7 / −49; tabanda kapananlar çıkınca −4,9 (t −0,9) / −16,7 (−3,4) / −3,2 (−0,5): taban serilerinin gölgesi. K2 düz −78 / −119 / −270 (ana tablodaki −627 çıkış ertelemesinden). Tabana değenler çıkıp kıyas temizlenince −17 (t −0,7) / −70 (−2,7) / −67 (−2,5); havuz −69 (−3,6). IS'te yok. Bu kayıp 2023+'da gün içinde (gece −18, gün içi −48): ertesi sabah açılışta almak kurtarmaz.

**Pratik kural:** “O gün tabana değmiş ya da XELKT endeksinin 5 puan ve fazlası gerisinde kapanmış hisse kapanışta alınmaz.” Kapsam hisse-günlerin %3 / %3 / %5'i; işaretlenenler ertesi gün sektörün −81 / −102 / −236 altında. Tabana değmeden 5 puan geride kalanlar: −28 (t −1,3) / −61 (−2,4) / −38 (−1,5). Rastgele alıcıya katkı günde +2 / +3 / +11 bps.
