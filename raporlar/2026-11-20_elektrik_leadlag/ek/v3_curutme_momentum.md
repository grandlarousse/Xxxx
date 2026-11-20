# V3 — çürütme: sektör momentumu sepet kuralları S1 ve S2

S1 = XELKT 20 günlük en yüksek kapanış → sepet AL, 3 gün. S2 = XELKT z ≥ 1 → sepet AL, 3 gün. Dönem “havuz” = 2023-01 → 2026-11. Rakamlar bps, maliyet öncesi; `per` = sinyal günleri − dönemin sıradan günleri. Kod: `kod/v3_curutme_momentum/run.sh <panel_full>` (4 sn). Tablo: `ek/v3_curutme_momentum.csv` (856 satır). Rapor rakamları (`elib`) birebir yeniden üretildi; `px.parquet` fiyatından bağımsız hesap: S1 +75, S2 +63.

## Hüküm

- **S1: ÇÜRÜTÜLDÜ** (nakitten girip 3 gün taşınan bağımsız alım kuralı olarak). İstatistiksel “devam” etkisi çürütülmedi; yalnız zamanlama süzgeci olarak şartlı kullanılabilir (şartlar aşağıda).
- **S2: ÇÜRÜTÜLDÜ.** Maliyet ve TL faizi sonrası beklenen kazanç sıfırın altında; eşik büyüdükçe etki OOS'ta artmıyor.

## Çürüten bulgular

1. **Kıyas şişkin: asıl rakip nakit.** 2023 sonrasında sepetin sıradan 3 günü −3 bps; yani `per` ≈ ham getiri. Nakitten giren kişi 3 gün faizden vazgeçer. XU030 vadelisinin bazından zımni TL faizi (alt sınır): %30 / %37 / %33 / %27 (2023–26), 3 gün ≈ 32–44 bps. Ham − temel maliyet (30) − faiz: **S1 +6, S2 −4**; muhafazakâr maliyetle (55) −19 / −29; kasada −18 / −6.
2. **Kümelenme (S1).** 174 sinyal günü = 40 dalga; artıda yalnız 18'i. En iyi 3 dalga (2023 Haziran, 2024 Ocak, 2025 Temmuz) kazancın %83'ü; onlar hariç gün ortalaması +19. Dalga boyu taşıyan için 40 gidiş-dönüş: ortalama +154, **medyan −44, kazanan %42**; en iyi 3 hariç +25. Yalnız dalganın ilk gününde giren: +65 (t 1,7); 10 günlük aradan sonraki ilk zirvede +28 (t 0,6). Blok önyükleme %90 aralık: S1 [+22, +128], S2 [+22, +113]; maliyetin altında kalma olasılığı %11–13.
3. **Trend denetimi.** Sinyal + XELKT 20/60 günlük getiri + XU100 regresyonu: S1 +45 (t 1,2), kasada +20 (t 0,4); S2 +69 (t 2,2).
4. **S2'nin kendi katkısı zayıf.** Zirve olmayan z ≥ 1 günleri +35 (t 0,9; OOS-1 +9). Eşik 1,25 → +60 (t 1,3), 1,5 → +27 (t 0,5; OOS-1 −3). 2024'te `per` −18.
5. **Yıllık (gerçekçi benzetim; yılın %28–38'i piyasada).** S1 net temel: +%23,6 / +8,9 / +13,3 / +0,5; muhafazakâr +20,6 / +5,7 / +11,1 / −2,0; **nakde göre** +16,1 / −1,5 / +2,8 / −7,0 (kazancın tamamı 2023). S2 net temel +7,5 / +1,4 / +23,9 / +4,4; nakde göre −3,5 / −11,0 / +11,4 / −5,2 (toplam −8,2).
6. **Kazanç sağ kuyruktan.** İşlemlerin %5,7'si (sonraki 3 günde tavan yapanlar, ort. +%11,9) toplam `per` kazancının %91'i; işlem medyanı +35 (S1), +21 (S2). AKSEN −4, ENJSA −10; en likit 5 hisse +41 (t 1,0).

## Çürütemediğim noktalar

- **Rejim yapaylığı değil.** “Aynı ayın diğer günleri” kıyası eksi çıkıyor (S1 −52) ama bu kıyas mekanik yanlı: günleri karıştırılmış, öngörüsüz dünyada aynı ölçü −109 veriyor. Düzeltilmiş: S1 +67 (p 0,07), S2 +73 (p 0,003); ±60 gün merkezli: +72 / +64. β·XU100 korumalı: +46 (t 2,0) / +63 (t 2,5).
- Sektöre özgü değil, BIST orta-küçük hisse olgusu: aynı kural XUSIN'de +72 (t 3,0), XUTUM'da +49; XU030'da −5.
- **Likidite.** Üçte birlikler S1 +66 / +70 / +95, S2 +64 / +79 / +56; fiyatı ≥ 5 TL olanlar +78; BIGEN, LYDYE, MAGEN hariç +64 / +60.
- **Dolum.** Tavana ≤ %1 yakın kapananlar işlemlerin %0,5–1,1'i; çıkarınca +77 / +68. t+1 açılışından giriş +64 (t 2,2) / +54 (t 1,8); t+1 kapanışından +46 (t 1,4) / +50 (t 1,7). Çıkışta taban kilidi işlemlerin %1,2'si (o işlemlerde ort. −%15).
- **Karar anı.** 17:50 değeriyle S1 sinyalinin %96'sı yakalanıyor, yanlış %5, getiri +76 (t 2,5); S2 %90 / %6, +69.
- **Parametre.** S1 pencere 10–60 ve h 1–5'te düzgün (h3: 81–96). h = 1: +42 (t 3,5) ama maliyetin altında kalır.
- Kapasite: kapanış seansının %10'u kuralıyla eşit ağırlıklı sepet ≈ 0,74 milyon TL; en sığ 5 hisse hariç 2,1 milyon TL.

## Aşağı yön

XELKT z ≤ −1 sonrası ertesi gün: havuz −48 (t −2,2), kasa −109, IS −22, OOS-1 −2. 20 günlük dip: −24 (t −0,9). Tutarsız; zayıf kaçınma bilgisi.

## Dürüst beklenti

- **S1, 3 günlük tek işlem** (yılda ~21): ham ortalama +73, medyan +62, kazanan %59; temel maliyet sonrası ≈ +43, faiz de düşülünce ≈ 0–10. En kötü 3 gün −%8,9; en kötü onda birlik −%3,0 ve altı; en kötü dalga −%5,3.
- **Yıllık:** nakde göre −7 ile +16 puan arası; 2023 gibi bir ralli yoksa beklenti sıfır dolayı, kötü yılda −7…−10 puan.
- **S2:** işlem başına ham +50 (t 1,5); nakde göre dört yılın üçü ekside; en kötü 3 gün −%10,4.

## S1'in şartlı kullanımı (öneri değil, süzgeç)

Sektör hissesi zaten alınacaksa: alım zirve günü ya da dalga içinde yapılır; zirveden uzakken ya da z ≤ −1 gününde alınmaz. Karar 17:50, emir kapanış seansı; sepet AKSEN/ENJSA ile sınırlanmaz; dalgaların yarıdan fazlasının zararla kapanacağı kabul edilir.

**Sınırlar.** Faiz vadeli bazından türetildi, banka ya da fon getirisiyle doğrulanmadı (gerçek oran daha yüksekse sonuç ağırlaşır). Hayatta kalma yanlılığı sürüyor. Tavan/taban ayıklaması geriye dönük tanıdır.
