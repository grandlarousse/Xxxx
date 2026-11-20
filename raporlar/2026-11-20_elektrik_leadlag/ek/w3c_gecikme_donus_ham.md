araç: 30/40

## Özet

A5_gecikme1_viop3_h3 çürütülmedi ama güçlenmedi de. **Yeni kural dondurulmadı**: `rules.py` içinde `FROZEN = []`, `build()` boş liste döndürür. Özgün kural kasaya zaten ayrıca giriyor. Bütün rakamlar bps, sıra IS / OOS-1, ölçü `own`, dolabilir.

- **Gecikme mi, piyasa mı:** yarı yarıya. Koşulsuz XU030 z ≥ 1: +40 (t 2,2) / +71 (1,5). Sektör de güçlüyken: +23 (1,0) / +37 (0,6). Özgün: +80 (2,9) / +165 (2,2). Özgün ile "sektör de güçlü" farkı 57 (t 1,7) / 128 (1,4): tek başına anlamlı değil. Aynı günlerde XU030'un kendisi +57 (2,7) / +86 (1,6); XU030 β'sıyla korunmuş üçlü +40 (1,7) / +83 (1,7).
- **Hisse:** üçü de iki dönemde artı; tek hisse taşımıyor. Üçlü dışı sektör sepetinde IS'te zayıf (+22, t 1,0).
- **Komşuluk:** sivrilme yok. XU030 eşiği 0,75 → 1,5 arasında ve XELKT koşulu sıkılaştıkça etki düzgün artıyor. 60 günlük pencere üç pencerenin en iyisi (40 ve 120'de IS +55 ve +54).
- **Yıl ve küme:** 15 yılın 13'ü artı; kaydırma p-değeri 0,011 / 0,007; OOS-1'de 29 sinyal günü 22 ayrı kümede. OOS-1'in en büyük iki günü seçim haftaları.
- **Giriş:** t+1 kapanışından girişte +63 / +20. 17:00 değerleriyle kurulan sinyal kapanış sinyalinin yalnız %55'ini yakalıyor, sinyallerinin %35'i yanlış; getirisi +81 / +101. 18:00 dolayındaki değerle yakalama %92 / %83.
- **Vadeli:** ham getiri spotta 211 / 213, vadelide 176 / 154; maliyet 36 ve 31. Spot daha iyi.
- **Kanıtın gücü:** OOS-1 t'si 2,16, kesit modeli dışındaki 36 alım kuralının en iyisi; şansla çıkma olasılığı %46. Kasada ~13–14 olay beklenir; %80 güçle saptanabilir etki 220–270 bps. Gerçek etki 80–165 ise güç %18–58, Holm düzeltmesiyle %3–24. En olası kasa sonucu "güç yetersiz".
- **Neden dondurmadım:** koşulsuz sürüm özgünün seyreltilmişi; geniş sepet daha sağlam değil; yüksek eşik ya da h = 1 seçmek veri gözetlemesi olur.
- **Diğer üç zayıf artı** (A6_V1 h3, A3_big, A1_FL): gürültüden ayırt edilemiyor, izlemeye değmez.

**Ölçü uyarısı (kütüphane hatası değil, ana ajanın bilmesi gerekir):** OOS-1'de "her gün AL" satırı `own` ölçüsünde üçlü için −49 (t −2,0), sektör sepeti için −54 (t −2,5). 2022 rallisi gecikmeli 250 günlük ortalamayı şişiriyor. OOS-1'deki bütün `own` ölçülü alım kuralları yaklaşık bu kadar aşağı çekilmiş görünür; "IS'te artıda olanların %38'i OOS-1'de artıda" bulgusunun bir kısmı bu kaymadan gelebilir.

Öz-denetim: `self_check_causal(build, P)` = `{}` (kural yok). Tarama sinyalleri (`build_tarama`, 9 sinyal, 3 kesim) hepsi 0,0. `run.sh` 22 sn.

Dosyalar:
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/w3c_gecikme.md
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/w3c_gecikme_sonuc.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3c_gecikme/rules.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3c_gecikme/tara.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3c_gecikme/denetim.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3c_gecikme/run.sh
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3c_gecikme/tara_log.txt
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3c_gecikme/denetim_log.txt

## İddia defteri

CSV = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/w3c_gecikme_sonuc.csv; LOG = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3c_gecikme/tara_log.txt. Sayılar IS / OOS-1.

iddia | dosya yolu | sayı | güven
--- | --- | --- | ---
Özgün kural yeniden üretildi | CSV, S1_c_ozgun_gecikme_viop3_h3 | +80 (t 2,90; 124 olay) / +165 (t 2,16; 24 olay) | yüksek
Koşulsuz XU030 z ≥ 1 → üçlü h3 | CSV, S1_a_kosulsuz_viop3_h3 | +40 (t 2,15; 359) / +71 (t 1,46; 74) | yüksek
Sektör de güçlüyken etki yok | CSV, S1_b_sektor_da_guclu_viop3_h3 | +23 (t 1,01) / +37 (t 0,63) | yüksek
Özgün − "sektör de güçlü" farkı tek başına anlamlı değil | LOG, S1 | 57 (Welch t 1,65) / 128 (t 1,38) | orta
Aynı günlerde XU030 endeksi de sürüyor (h3) | CSV, S1_c_ozgun_gecikme_XU030endeks_h3 | +57 (t 2,70) / +86 (t 1,60) | yüksek
XU030 vadelisi (2017-03+) aynı günlerde | CSV, S1_c_ozgun_gecikme_XU030vadeli_h3 | +95 (t 2,44; 47 olay) / +88 (t 1,58) | orta
XU030 β korumalı üçlü | CSV, S1_c_ozgun_gecikme_viop3_XU030korumali_h3 | +40 (t 1,67) / +83 (t 1,69) | orta
AKSEN tek başına | CSV, S2_c_ozgun_gecikme_AKSEN_h3 | +59 (t 1,76) / +199 (t 2,09) | yüksek
ENJSA tek başına | CSV, S2_c_ozgun_gecikme_ENJSA_h3 | +148 (t 3,20; 41 olay) / +104 (t 1,30) | yüksek
ODAS tek başına | CSV, S2_c_ozgun_gecikme_ODAS_h3 | +127 (t 2,52) / +192 (t 1,83) | yüksek
Büyük beş hisse | CSV, S2_c_ozgun_gecikme_BIG5_h3 | +57 (t 2,44) / +145 (t 2,22) | yüksek
Üçlü dışı sektör sepeti | CSV, S2_c_ozgun_gecikme_sepet_ex3_h3 | +22 (t 1,00) / +113 (t 1,61) | yüksek
XU030 eşiği 0,75; 1; 1,25; 1,5 (XELKT < 0,5; h3; pencere 60) | CSV, S3_w60_X_ge*_E_lt0.5_viop3_h3 | IS 58, 80, 84, 72; OOS-1 76, 165, 303, 373 | yüksek
XELKT koşulu < 0; < 0,5; < 1; koşulsuz (XU030 ≥ 1; h3) | CSV, S3_w60_X_ge1.0_* | IS 47, 80, 57, 40; OOS-1 132, 165, 86, 71 | yüksek
z penceresi 40 ve 120 | CSV, S3_w40_… ve S3_w120_…_X_ge1.0_E_lt0.5_viop3_h3 | 55 (t 1,9) / 109 (t 1,3); 54 (t 2,0) / 149 (t 1,9) | yüksek
Tutma süresi h = 1, 2, 3, 5 | CSV, S3_w60_X_ge1.0_E_lt0.5_viop3_h* | IS 27, 50, 80, 105; OOS-1 125, 136, 165, 98 | yüksek
XELKT < 0,5 ve eşik ≤ 1,5 satırlarının hepsi iki dönemde artı | CSV, soru = S3 | 24 / 24 satır | yüksek
Yıllara göre | CSV, yillar_bps (S1_c) | 15 yılın 13'ü artı; 2013: −88, 2017: −58 | yüksek
En iyi günler hariç | CSV, top10_haric_bps, ek_top3_haric_OOS1_bps | en iyi 10 gün hariç +44; OOS-1 en iyi 3 gün hariç +66; OOS-1 medyan +96 | yüksek
Kaydırma p-değeri (1.000 kaydırma) | CSV, ek_kaydirma_p_IS / _OOS1 | 0,011 / 0,007 | orta
Kümelenme | LOG, S4 | IS 150 sinyal günü 110 kümede; OOS-1 29 günü 22 kümede | yüksek
t+1 kapanışından giriş | CSV, S5_c_ozgun_gecikme_viop3_giris_t+1kapanis_h3 | +63 (t 2,04) / +20 (t 0,31) | yüksek
17:00 sinyali kapanış sinyalini ne kadar yakalıyor (2017+) | LOG, S5 | yakalama %55 / %55; yanlış %35 / %36 | orta
17:00 sinyalinin getirisi (kapanış sinyali 2017+: +89 / +165) | CSV, S5_gecikme_sinyal1700_viop3_h3 | +81 (t 1,67) / +101 (t 1,15) | orta
Kaçan ve yanlış sinyaller | CSV, S5_gecikme_sinyal1700_kacan / _yanlis | kaçan +67 / +255; yanlış +32 / +125 (t < 1) | düşük
Vadeli fiyatıyla (ikisinin kötüsü) | CSV, S6_c_ozgun_gecikme_viop3_h3, arac = viop_vadeli | +171 (t 3,45; 32 olay) / +173 (t 2,36) | orta
Ham getiri spot ve vadeli (kontrat dönemi) | LOG, "S6 ham getiri" | spot 211 / 213; vadeli 176 / 154; maliyet 36 ve 31 | orta
Kasada beklenen olay ve güç | LOG, S7 | 13–14 olay; saptanabilir etki 220–272 bps; güç %18–58 (Holm ile %3–24) | orta
OOS-1'de `own` ölçüsünün tabanı eksi | CSV, S0_hergun_viop3_h3, S0_hergun_sepet_h3 | üçlü +7 / −49 (t −2,0); sepet −1 / −54 (t −2,5) | yüksek
Nedensellik öz-denetimi | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3c_gecikme/denetim_log.txt | build: {} (kural yok); 9 tarama sinyali × 3 kesim: 0,0 | yüksek

## açık kalanlar

- **Ölçü kayması bütün OOS-1 hükümlerini etkiliyor olabilir.** Yalnız üçlü, sektör sepeti, büyük beş ve XU030 için ölçtüm (h3: −49, −54, −48, −33). Diğer ailelerin OOS-1 sonuçlarını dönem içi tabana göre yeniden okumak ana ajanın kararı; ben yapmadım (görev dışı).
- **17:50 sinyali doğrudan ölçülemedi.** Saatlik veriyle yalnız 17:00 (yakalama %55) ve ~18:00 (%83–92) sınandı; 17:50 bu ikisinin arasında bir yerde. "18:00" değeri kullanıcının karar anından sonradır, üst sınır olarak okunmalı.
- **Özgün − "sektör de güçlü" farkı** iki dönemde aynı yönde ama her birinde t < 1,7; birleşik bir test yapmadım.
- **XU030 korumalı üçlü** günlük yeniden dengelenen β ile kuruldu; endeks vadelisinin taşıma maliyeti ve işlem maliyeti düşülmedi. Sözde sütun satırlarında (endeks, endeks vadelisi, korumalı) maliyet ve net sütunları anlamsızdır; CSV'nin `not` sütununda yazılı.
- **Vadeli IS dönemi kısa** (32 olay; ENJSA 2018-12, ODAS 2021-04, AKSEN 2022-11'den başlar).
- **Diğer üç alım kuralı** için yeni hesap yapmadım; hüküm `ek/oos1_sonuc.csv` satırlarına dayanıyor.
- Not dosyası `wc -w` ile 703 kelime (biçim imleri dâhil); görevdeki 700 sınırının 3 üstünde.
- Hiçbir şey commit edilmedi; `panel_full` ve `raw` açılmadı.