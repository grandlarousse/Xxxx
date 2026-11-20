# W3-C — XU030 → elektrik gecikmesi: çürütme denemesi (geliştirme paneli)

**Sınanan.** `A5_gecikme1_viop3_h3`: z(XU030) ≥ 1 ve z(XELKT) < 0,5 → AKSEN, ENJSA, ODAS spot AL, 3 gün. 230 satır (`ek/w3c_gecikme_sonuc.csv`; 150'si parametre komşuluğu). Ölçü `own`, dolabilir; rakamlar bps, sıra IS / OOS-1.

**Sonuç: kural çürütülmedi ama güçlenmedi de. Yeni kural DONDURULMADI.**

## Bulgular

1. **Yarısı piyasa, yarısı yetişme.** (a) koşulsuz XU030 z ≥ 1: +40 (t 2,2) / +71 (1,5). (b) sektör de güçlü: +23 (1,0) / +37 (0,6). (c) özgün: +80 (2,9) / +165 (2,2). (c) − (b) farkı 57 (t 1,7) / 128 (1,4): tek başına anlamlı değil, iki dönemde aynı yönde. Aynı günlerde XU030'un kendisi de sürüyor: +57 (2,7) / +86 (1,6); XU030 vadelisi (2017+) +95 / +88. XU030 β'sıyla korunmuş üçlü: +40 (1,7) / +83 (1,7).
2. **Tek hisse taşımıyor.** AKSEN +59 / +199, ENJSA +148 / +104, ODAS +127 / +192. Büyük beş hisse +57 (2,4) / +145 (2,2); üçlü dışı sektör sepeti +22 (1,0) / +113 (1,6): etki büyük, likit hisselerde.
3. **Sivrilme yok.** XU030 eşiği 0,75 → 1,5 arasında etki düzgün artıyor (58, 80, 84, 72 / 76, 165, 303, 373). XELKT koşulu gevşedikçe düzgün azalıyor (< 0,5: 80 / 165; < 1: 57 / 86; koşulsuz: 40 / 71). Pencere 40 ve 120'de 55 / 109 ve 54 / 149: 60 günlük pencere en iyisi, gerçek etki IS rakamından küçük olabilir. XELKT z < 0,5 ve XU030 eşiği ≤ 1,5 olan 24 satırın (h 1–5, üç pencere) hepsi iki dönemde artı.
4. **Yıllar ve küme.** 15 yılın 13'ü artı (2013, 2017 eksi). En iyi 10 gün hariç +44; OOS-1'de en iyi 3 gün hariç +66, medyan +96. OOS-1'in iki büyük günü seçim haftaları (2023-05-26: +1265; 2024-04-04: +1105). Kümelenme az: 29 sinyal günü 22 ayrı kümede. Kaydırma p-değeri 0,011 / 0,007.
5. **Giriş.** t+1 kapanışından giriş: +63 (2,0) / +20 (0,3). OOS-1'de kazancın çoğu ilk gün (h1: +125), IS'te 3–5 güne yayılı (27, 50, 80, 105). 17:00 değerleriyle kurulan sinyal kapanış sinyalinin yalnız **%55**'ini yakalıyor, sinyallerinin %35'i yanlış; sonucu +81 (1,7) / +101 (1,2) (kapanış sinyali 2017+: +89 / +165). Kaçan sinyaller en iyileri (+67 / +255), yanlışlar zararsız (+32 / +125, t < 1). 18:00 dolayındaki değerle yakalama %92 / %83.
6. **Vadeli.** Vadeli fiyatıyla (ikisinin kötüsü) +171 (3,5) / +173 (2,4). Ham getiri ise spotta 211 / 213, vadelide 176 / 154: üç günde 35–60 bps taşıma kaybı. Maliyet 36 (spot) ve 31 (vadeli). **Spot daha iyi.** Muhafazakâr maliyetle spot net +37 / +104.
7. **Kanıtın gücü.** OOS-1'deki t = 2,16, 36 alım kuralının en iyisi (5,4'lük kesit modeli hariç); 41 denemede bu kadar iyisinin şansla çıkma olasılığı %46. Lehine: IS'te önceden yazılıydı (t 2,9), mekanizması söylenebilir, komşuları düzgün. Aleyhine: yarısı piyasa momentumu, gecikme koşulunun katkısı t ≈ 1,5.

**Ölçü uyarısı (kütüphane hatası değil).** OOS-1'de “her gün AL” satırı `own` ölçüsünde −49 bps (t −2,0; sepet −54, t −2,5): 2022 rallisi gecikmeli ortalamayı şişiriyor. OOS-1'deki bütün alım kuralları yaklaşık bu kadar aşağı çekilmiş görünür; kuralın dönem içi tabana göre fazlası +214.

## DONDURULMUŞ KURAL: yok

- Koşulsuz XU030 momentumu daha sade ama (b) yarısı etkisiz: özgünün seyreltilmişi; OOS-1 t 1,5, temel maliyet sonrası +16 / +33, t+1 girişinde OOS-1 −15.
- Geniş sepet (büyük beş, sektör) üçlüden sağlam değil.
- Daha yüksek eşik ya da h = 1 OOS-1'de parlak; seçmek veri gözetlemesi olur.
- Kasada beklenen (özgün kural): ~13–14 bağımsız olay; gün sd'si 320–400 bps. %80 güçle saptanabilir etki 220–270 bps. Gerçek etki 80 ise güç %18–23, 165 ise %44–58; Holm düzeltmesiyle %3–24. En olası sonuç: **güç yetersiz**.

## Diğer zayıf artılar (izlemeye değmez)

`A6_V1_dbaz_uzl_z1_yuk_spotAL_h3`: +88 / +46 (t 1,0), net +8; 2024: +11, 2025: −18, sönüyor. `A3_big_z10_small_h3`: +47 / +32 (t 0,6), en iyi 10 gün hariç 0. `A1_FL_th2.0_h1`: +34 / +35 (t 1,1), net −27; işlemlerin %58'i ZOREN.
## Pratik anlam

- Tarif: XU030 günü olağan oynaklığından fazla yükselmiş (medyan +%1,8 / +%2,4), XELKT yerinde saymış (medyan +%0,1 / +%0,4). Yılda yaklaşık 10 gün.
- Öneri değil, izleme listesi. Kasa bunu büyük olasılıkla ne doğrular ne çürütür; kâğıt üstünde izlemek gerekir.
- İzlenecekse: karar olabildiğince geç (17:50–18:00) verilir; 17:00'de sinyalin yarısı henüz görünmez. Araç spot. Ertesi güne ertelenirse kazancın çoğu kaçar.

**Öz-denetim.** `build()` boş liste döndürür; `self_check_causal(build, P)` = `{}`. Tarama sinyalleri (`build_tarama`, 9 sinyal, üç kesim): hepsi 0,0. `run.sh` 22 sn.
