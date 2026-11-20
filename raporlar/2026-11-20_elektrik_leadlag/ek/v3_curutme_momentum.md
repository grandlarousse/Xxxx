# V3 — çürütme: sektör momentumu sepet kuralları S1 ve S2

S1 = XELKT 20 günlük en yüksek kapanış → sepet AL, 3 gün. S2 = XELKT z ≥ 1 → sepet AL, 3 gün. “Havuz” = 2023-01 → 2026-11. Rakamlar bps, maliyet öncesi; `per` = sinyal günleri − dönemin sıradan günleri. Kod: `kod/v3_curutme_momentum/run.sh <panel_full>`; tablo: `ek/v3_curutme_momentum.csv` (856 satır). Rapor rakamları birebir yeniden üretildi.

## Hüküm

- **S1: ÇÜRÜTÜLDÜ** (nakitten girip 3 gün taşınan bağımsız alım kuralı olarak). İstatistiksel “devam” etkisi çürütülmedi; yalnız zamanlama süzgeci olarak şartlı kullanılabilir.
- **S2: ÇÜRÜTÜLDÜ.** Maliyet ve TL faizi sonrası beklenen kazanç sıfırın altında; eşik büyüdükçe etki OOS'ta artmıyor.

## Çürüten bulgular

1. **Asıl rakip nakit.** 2023 sonrasında sepetin sıradan 3 günü −3 bps; yani `per` ≈ ham getiri. Nakitten giren 3 gün faizden vazgeçer. XU030 vadelisinin bazından zımni TL faizi (alt sınır): %30 / %37 / %33 / %27 (2023–26); 3 gün ≈ 32–44 bps. Ham − temel maliyet (30) − faiz: **S1 +6, S2 −4**; muhafazakâr maliyetle (55) −19 / −29; kasada −18 / −6.
2. **Kümelenme (S1).** 174 sinyal günü = 40 dalga; yalnız 18'i artıda. En iyi 3 dalga (2023 Haziran, 2024 Ocak, 2025 Temmuz) kazancın %83'ü; onlar hariç gün ortalaması +19. Dalga boyu taşıyan için 40 gidiş-dönüş: ortalama +154, **medyan −44, kazanan %42**. Yalnız dalganın ilk gününde giren +65 (t 1,7); 10 günlük aradan sonraki ilk zirvede +28 (t 0,6). Blok önyükleme %90 aralık: S1 [+22, +128], S2 [+22, +113].
3. **Trend denetimi.** Sinyal + XELKT 20/60 günlük getiri + XU100 regresyonunda S1 +45 (t 1,2), kasada +20 (t 0,4); S2 +69 (t 2,2).
4. **S2'nin kendi katkısı zayıf.** Zirve olmayan z ≥ 1 günleri +35 (t 0,9; OOS-1 +9). Eşik 1,25 → +60 (t 1,3); 1,5 → +27 (OOS-1 −3). 2024'te `per` −18.
5. **Yıllık benzetim** (yılın %28–38'i piyasada; 2023 / 24 / 25 / 26). S1 net temel +%23,6 / +8,9 / +13,3 / +0,5; muhafazakâr +20,6 / +5,7 / +11,1 / −2,0; **nakde göre** +16,1 / −1,5 / +2,8 / −7,0. S2 net temel +7,5 / +1,4 / +23,9 / +4,4; nakde göre −3,5 / −11,0 / +11,4 / −5,2.
6. **Kazanç sağ kuyruktan.** Sonraki 3 günde tavan yapan işlemler (%5,7; ort. +%11,9) toplam `per` kazancının %91'i; işlem medyanı +35 (S1), +21 (S2). AKSEN −4, ENJSA −10; en likit 5 hisse +41 (t 1,0).

## Çürütemediğim noktalar

- **Rejim yapaylığı değil.** “Aynı ayın diğer günleri” kıyası eksi çıkıyor (S1 −52) ama mekanik yanlı: günleri karıştırılmış, öngörüsüz dünyada aynı ölçü −109 veriyor. Düzeltilmiş: S1 +67 (p 0,07), S2 +73 (p 0,003); ±60 gün merkezli +72 / +64. β·XU100 korumalı +46 (t 2,0) / +63 (t 2,5).
- Sektöre özgü değil: aynı kural XUSIN'de +72 (t 3,0), XUTUM'da +49; XU030'da −5.
- **Likidite.** Üçte birlikler (likit → sığ) S1 +66 / +70 / +95, S2 +64 / +79 / +56.
- **Dolum.** Tavana ≤ %1 yakın kapananlar hariç +77 / +68. t+1 açılışından giriş +64 (t 2,2) / +54 (t 1,8); t+1 kapanışından +46 (t 1,4) / +50 (t 1,7). Çıkışta taban kilidi: işlemlerin %1,2'si, ort. −%15.
- **Karar anı.** 17:50 değeriyle S1 sinyalinin %96'sı yakalanıyor, yanlış %5, getiri +76 (t 2,5); S2 %90 / %6, +69.
- **Parametre.** S1 pencere 10–60'ta düzgün (h3: 78–96). h = 1: +42 (t 3,5), maliyet sonrası ≈ +12.
- **Kapasite** (kapanış seansının %10'u): eşit ağırlıklı sepet ≈ 0,74 milyon TL; en sığ 5 hisse hariç 2,1 milyon TL.

## Aşağı yön

XELKT z ≤ −1 sonrası ertesi gün: havuz −48 (t −2,2), kasa −109, IS −22, OOS-1 −2. Tutarsız.

## Dürüst beklenti

- **S1, 3 günlük tek işlem** (yılda ~21): ham ortalama +73, medyan +62, kazanan %59; temel maliyet sonrası ≈ +43, faiz de düşülünce ≈ 0–10. En kötü 3 gün −%8,9; en kötü dalga −%5,3.
- **S1 yıllık:** nakde göre −7 ile +16 puan; 2023 gibi bir ralli yoksa sıfır dolayı.
- **S2:** işlem başına ham +50 (t 1,5); nakde göre dört yılın üçü ekside (toplam −8,2 puan); en kötü 3 gün −%10,4.

## S1'in şartlı kullanımı

Sektör hissesi zaten alınacaksa alım zirve günü ya da dalga içinde yapılır; z ≤ −1 gününde alınmaz. Karar 17:50, emir kapanış seansı; dalgaların yarıdan fazlası zararla kapanır.

**Sınırlar.** Faiz vadeli bazından türetildi; fon ya da mevduat getirisiyle doğrulanmadı (gerçek oran yüksekse sonuç ağırlaşır). Hayatta kalma yanlılığı sürüyor.
