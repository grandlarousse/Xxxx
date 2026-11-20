araç: 36/40

## Özet

Beş işin hepsi yapıldı; dondurulmuş kurallarla eşleşme denetimi 0 farklı hücre, bilinen IS / OOS-1 / kasa / havuz rakamları birebir yeniden üretildi (S1 +44 / +85 / +86 / +83).

- **S1 (zirve20) kapanıştan önce uygulanabilir.** 17:50 XELKT değeriyle, tamponsuz: yakalama 0,95, kesinlik 0,94; getiri kaybı −3 bps (2017+), +2 (2023+), kasa −10. Tampon gerekmiyor: +%0,3 tampon kesinliği 0,99'a çıkarıp yakalamayı 0,82'ye indiriyor.
- **S2 (z ≥ 1) uygulanabilir.** 17:50'de 0,87 / 0,91, 17:55'te 0,90 / 0,93; kayıp −6 bps (2017+), +5 (2023+). Eşiği sıkılaştırmak (z ≥ 1,2) kaybettiriyor (−14), çünkü kaçan günler iyi (+120) ve yanlış sinyaller zararsız (+81).
- **S3 (gecikme) kapanıştan önce güvenilir değil.** 17:00'de yakalama 0,56; 18:00 son sürekli işlem değeriyle 0,89 / 0,83 ama getiri 2023+'da 157 → 90. Kaçan 7 gün en iyileri (+508).
- **XU030 5 dk tamamlanamadı.** SABIRLI kipi 10 dakikadan uzun denendi, yeni gün gelmedi (414 gün kaldı); süreci durdurdum. S3 için 17:00 ve 18:00 İş Yatırım saatlik veriyle tam (2017+). 17:30–17:55 satırları 1.067 günlük alt örneklem: 411 gün gerçek 5 dk, 656 gün XU100 oranı vekili, 17:30'da ayrıca 160 gün Yahoo saatlik.
- **T2 / K1 / K2 17:30 fiyatıyla çalışıyor.** Örtüşme yaklaşık 0,8; getiriler kapanış sürümüyle aynı ya da daha güçlü. T2 için yalnız sade kural kuruldu (model kuralı kurulum başına 11 sn sürdüğü için dışarıda bırakıldı).
- **Dolum.** Sinyal günlerinde tavanda kapanma S1 %4,3, S2 %5,6 (bütün günler %2,6); bunların dörtte biri 17:30'dan sonra oluşuyor. Çıkış günü taban kilidi %0,6–0,9.
- **17:50–17:59'da sürekli işlemde almanın ortalama fiyat avantajı yok.** Karar anı sinyaliyle koşullandığında XELKT kapanışı 17:50–18:00 ortalamasından +0,3 (S1) ve +2,5 (S2) bps farklı. Kapanış sinyaliyle koşullamak yanıltıcı (+10 bps görünür), çünkü son dakikaları yükselen günleri seçer; notta karar anı koşullaması kullanıldı.
- **Kapanış seansı emri.** 18:01–18:05'te limit, piyasa ve piyasadan limite emir girilebiliyor; eşleşmeyen piyasa emri iptal ediliyor; 18:08–18:10'da yalnız kapanış fiyatından limit emir.

`run.sh` uçtan uca tek seferde çalıştırılmadı; üç betik ayrı ayrı çalıştırıldı (t5 yaklaşık 25 dk), sonra birleştirildi.

Dosyalar:
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v6_zamanlama.csv (984 satır; `is` = endeks_sinyali | dolum | hisse_kurali)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v6_zamanlama.md (597 kelime)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/v6_zamanlama/ (run.sh, v6lib.py, t1_endeks.py, t3_dolum.py, t5_hisse.py, birlestir.py)

## İddia defteri

Dosya kısaltması: CSV = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v6_zamanlama.csv. Getiriler bps, `per`, h = 3, giriş kapanış fiyatı; "→" kapanış sinyali → saatinde karar.

iddia | dosya yolu ya da URL | sayı ya da birebir kısa alıntı | güven
---|---|---|---
Yeniden kurulan S1/S2/S3 dondurulmuş kurallarla aynı | kod/v6_zamanlama/t1_endeks.py çıktısı | farklı hücre 0; S1 +44 / +85 / +86, havuz +83 | yüksek
S1 17:50 tamponsuz, 2017+ | CSV (S1, 1750, +0.00%, TUM17) | yakalama 0,95, kesinlik 0,94; 76,3 → 73,1 (−3,2) | yüksek
S1 17:50 dönemler | CSV | IS17 73,9 → 68,3; OOS-1 82,0 → 94,3; kasa 81,0 → 71,4; 2023+ 78,6 → 80,5 | yüksek
S1 17:30 / 17:45 / 17:55 / 18:00, 2017+ | CSV | 0,94 / 0,90; 0,94 / 0,93; 0,97 / 0,93; 0,97 / 0,95 | yüksek
S1 17:55, 2023+ | CSV | 78,6 → 62,9 (−15,8); yanlış 10 gün −210 bps | orta (10 gün)
S1 tampon +%0,3 (17:50, 2017+) | CSV | yakalama 0,82, kesinlik 0,99; getiri 85,3 | yüksek
S1 tampon −%0,15 (17:50, 2017+) | CSV | 0,98 / 0,88; getiri 68,5 | yüksek
S1 17:50 yanlış ve kaçan sinyaller | CSV | yanlış 32 gün +55; kaçan 25 gün +117 | orta
S2 17:50 z ≥ 1, 2017+ | CSV (S2, 1750, z>=1, TUM17) | 0,87 / 0,91; 72,3 → 66,7 (−5,6) | yüksek
S2 17:50 dönemler | CSV | IS17 76,2 → 64,0; OOS-1 49,7 → 64,8; kasa 95,2 → 82,7; 2023+ 68,2 → 73,1 | yüksek
S2 17:55 ve 18:00, 2017+ | CSV | 0,90 / 0,93 (−6,3); 0,92 / 0,92 (−5,8) | yüksek
S2 tampon z ≥ 1,2 (17:50) | CSV | 0,69 / 0,98; getiri 58,3 (−14,0) | yüksek
S2 gevşek z ≥ 0,9 (17:50) | CSV | 0,94 / 0,83; getiri 70,5 (−1,8) | yüksek
S2 17:50 kaçan ve yanlış | CSV | kaçan 50 gün +120; yanlış 34 gün +81 | orta
S3 17:00 (isy saatlik + vekil, 2017+) | CSV (S3, 1700) | 0,56 / 0,66; 120,5 → 93,6 | yüksek
S3 18:00 son değer, 2017+ | CSV (S3, 1800, TUM17) | 0,89 / 0,83; 120,5 → 95,5 (t 3,4) | yüksek
S3 18:00, 2023+ | CSV (S3, 1800, H2023) | 0,84 / 0,93; 156,7 → 90,2 (t 2,1); kaçan 7 gün +508 | orta
S3 17:50 (1.067 gün alt örneklem) | CSV (S3, 1750, TUM17) | 0,72 / 0,77; 65,4 → 16,8 | düşük (656 gün vekil)
S3 gevşek eşik zX ≥ 0,9, zE < 0,7 (18:00) | CSV | yakalama 1,00, kesinlik 0,56; getiri 101,3 (t 4,3) | orta
XU100 oranı vekilinin hatası (17:50) | t1_endeks.py çıktısı | 385 gün, medyan 1,9 bps, %95'lik 9,4 bps | yüksek
XU030 5 dk gün sayısı indirme sonrası | scratchpad/el/data/raw/d2/isy/m5/XU030.parquet | 414 gün (2017: 233, 2018: 42, 2026: 139) | yüksek
T2 17:30 fiyatı (2023-12-21+, 729 gün) | CSV (hisse_kurali, T2, 1730) | kesinlik 0,80, yakalama 0,81; +32,5 (t 6,4), kapanış +30,5 | yüksek
K1 17:30 | CSV (K1, 1730) | 0,80 / 0,80; −80,5, kapanış −72,0 | yüksek
K2 17:30 | CSV (K2, 1730) | kesinlik 0,90, yakalama 0,76; −468, kapanış −409 | yüksek
T2 / K1 / K2 18:00 son fiyat (440 gün) | CSV (saat 1800) | 0,89 / 0,87; 0,88 / 0,88; 0,94 / 0,89 | yüksek
Sinyal günü tavanda kapanan pay (2017+) | CSV (dolum, tavanda_kapanan_oran) | S1 %4,26; S2 %5,59; bütün günler %2,60; kasa S1 %1,95, S2 %3,57 | yüksek
17:30'da tavanda değil, tavanda kapandı (2023-12+) | CSV (tavan_1730da_yok_kapanista_var_oran) | S1 %0,55; S2 %0,96; tavan kapanışlarının %23–26'sı | orta
Tavana ≤ %1 yakın kilitsiz kapanış (2017+) | CSV (tavana_1pct_yakin_kilitsiz_oran) | S1 %0,69; S2 %1,08 | orta (tavan fiyatı kestirim)
XELKT kapanış − 17:50–18:00 ortalaması, karar anı sinyali | CSV (XELKT_kapanis_eksi_1750_1759_ort_bps) | 2017+ S1 +0,3, S2 +2,5; 2023+ +0,8, +1,0; kasa −1,9, −1,5 | yüksek
Çıkış günü (t+3) taban kilidi | CSV (cikis_gunu_t3_tabanda_kilit_oran) | S1 %0,88; S2 %0,55; S3 0/430; bütün günler %0,84, kasa %1,71 | yüksek
Kapanış seansı emir türleri | https://borsaistanbul.com/piyasalar/pay-piyasasi/piyasa-isleyisi | "açığa satış emri, limit emir, piyasa emri, piyasadan limite, KİE, dengeleyici emirler"; ±%3; eşleşmeyen piyasa emri iptal | orta (özetleyici model üzerinden okundu)

## açık kalanlar

- **XU030 5 dk verisi eksik** (2018-03 → 2026-05 arası yok). S3'ün 17:30–17:55 hükmü vekil ağırlıklı alt örnekleme dayanıyor; o alt örneklemde kapanış sinyalinin kendisi de zayıf (IS17 parçası +4 bps). Sağlam olan yalnız 17:00 ve 18:00 sonuçları.
- **Hisse düzeyinde gerçek 17:50–17:59 fiyatı** yalnız son 60 günde var (3–5 sinyal günü). "Sürekli işlemde al" seçeneğinin hisse düzeyi hükmü verilemedi; endeks düzeyi sonuç değer ağırlıklı, sepet eşit ağırlıklı.
- **Açıklanamayan fark:** Yahoo verisinde eşit ağırlıklı sepette resmi kapanış, 18:00 son fiyatın ortalama 7 bps altında (bütün günler, t −12,9); endekste bu fark yaklaşık 0. Temettü düzeltmesi artığı ya da alış-satış sıçraması olabilir; ayrıştırılmadı.
- **KAFE (kapanış fiyatlı emir)** yalnız arama özetinde geçti; Borsa İstanbul sayfasında bulunamadı. Pay Piyasası Prosedürü PDF'i açılmadı. Fiyat belirleme penceresi kaynaklarda 18:05–18:07 ve 18:05–18:08 diye iki biçimde geçiyor.
- **Kapanış seansı derinliği yok.** "Limit emir kapanış fiyatından dolar" varsayımı ölçülemedi (A7'nin dolaylı hacim tahmini dışında).
- **K2 düzeyleri** 2023-12+ döneminde çöküş serilerinden etkileniyor (−409); tabanda kapananlar hariç sürüm vekille ayrıca koşulmadı.
- **T2'de `lim_up_touch` / `lim_dn_touch` vekillenmiyor** (vekil.py sınırı): 17:30'dan sonra tavana ya da tabana değen hisse 17:30'da bilinemez, T2 örtüşmesi bu yüzden biraz iyimser.
- **Ham dosyaya dokunuldu:** indirme betiği `raw/d2/isy/m5/XU030.parquet` dosyasını aynı içerikle yeniden kaydetti (414 gün, okunuyor). Depoda `kod/v4_curutme_diger/` altında benim yapmadığım değişiklikler görünüyor; dokunmadım.