# RF1a · Ek 2: maliyet duyarlılığı (kapanış müzayedesi emri senaryosu)

araç: 29/40

## Özet

Müzayede maliyeti (bacak başına yalnız 1,5 bps) IS aday sayısını artırdı ama ayakta kalan kural çıkmadı. Sınanan kural × varyant sayıları birincil analizle aynı: K1 1048, K2 216, K3 164, K7 376. IS adayı 25'ten 42'ye çıktı. Aileye göre birincil → müzayede: K1 1→4, K2 0→0, K3 1→3, K7 23→35. Adapter doğru mu diye aynı kodu 'hisse' komisyonuyla çalıştırdım; birincil aday sayılarını (1/0/1/23) birebir verdi. R6-03'ün OOS değeri de aynı çıktı (123,9 bps).

OOS'ta aynı yönde ve t ≥ 2 olan 5 kural var, hepsi K7'den (bilanço ailesi). K1, K2 ve K3'te 0.
- R6-03 tR uzun, h3: OOS 133 bps, t 3,07, p 0,010.
- R6-04 bilanço öncesi prim, büyük evren, uzun, SPY korunmalı: k10Rp1 (h11) 61 bps t 3,17; k5Rp1 (h6) 52 bps t 3,20; k3Rp1 (h4) 40 bps t 2,59.
- R5-08 a10 kısa, h3: 135 bps, t 2,28, n 48.

Ek 2 ölçütlerinin (a hariç) hepsini sağlayan kural yok:
- R6-03 ve üç R6-04 varyantı son dönemde (2024–2026) negatif: −40 ile −54 bps arası, t −1,3 ile −2,1 arası. Yani (c) maddesinden düşüyorlar.
- R6-04'lerde en iyi %5 işlem çıkınca net de negatif (≈ −40 ile −44 bps), yani (e) maddesinden de düşüyorlar.
- R5-08 a10 kısa'nın OOS t'si 2,28; 2,5 eşiğinin altında, en çok DÜŞÜK olur. Ayrıca komşu ufuklarda OOS t yalnız 0,99 (h1) ve 1,33 (h2), son dönem t 0,85 ve OOS'ta sadece 48 işlem var.

Bu 42 adayın kendi içinde BH %10'u yalnız R6-04 k5Rp1'den geçiyor (q 0,042). O da (c) ve (e) maddelerinden düşüyor. Sonuç: bu senaryoda da geçen yok. Birincil "hiçbiri geçmedi" sonucu bu dört aile için maliyet varsayımına bağlı değil.

En önemli çekince: R6-04'ün büyük evren uzun bacağı, d4_K7'deki hayatta kalma yanlılıklı "bütün olaylar" tabanıyla neredeyse aynı şey (bilançodan önce al, R+1'de çık). Bu taban birincil analizde de OOS'ta +61 bps vermişti. Ayrıca bu varyantların ufku 4, 6 ve 11 gün; yatırımcının 1–3 günlük profilinin dışında. Bu ufuklar özgün betiğin tanımı. K7'nin tepki günü uyuşmazlığı (%12–20) nedeniyle bu aile zaten en çok KOŞULLU olabilir.

## Aile tablosu

| aile | varyant | IS adayı (birincil) | IS adayı (müzayede) | OOS t ≥ 2 | Ek 2'den geçen |
|---|---|---|---|---|---|
| K1 (A, lider → takipçi) | 1048 | 1 | 4 | 0 | 0 |
| K2 (B, çiftler / artık / kesitsel dönüş) | 216 | 0 | 0 | 0 | 0 |
| K3 (C, çapraz varlık) | 164 | 1 | 3 | 0 | 0 |
| K7 (G, bilanço) | 376 | 23 | 35 | 5 | 0 |

## Adaylar

| kural_id | aile | ad | hedef | yon | h | cikis | korunma | is_net_bps | is_t | oos_net_bps | oos_n | oos_t | oos_t_anormal | oos_p | son_net_bps | son_t | girisA_oos_net_bps | girisA_oos_t | en_iyi5suz_bps | saatlik_1530 | birincil_oos_net_bps | olcutler | gerekce |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R6-04/k5Rp1/B/uzun | K7 | G4 bilanço öncesi prim: R-5 kapanışında al, R+1'de çık (büyük evren, yalnız uzun) | COK(122) | uzun | 6 | kapanis | SPY:250 | 31.37 | 3.14 | 51.79 | 1951 | 3.2 | 3.1 | 0.001 | -42.48 | -1.99 | 48.65 | 2.99 | -40.18 | sinyal fiyattan bağımsız (takvim): örtüşme %100, korunan pay 1,0 | 41.07 | b+ c− d+ e− f+ | Kendi 42 adayı içinde BH %10'dan geçen tek kural (q 0,042). Son dönem negatif, en iyi %5 çıkınca negatif. VIX>30: 19 bölüm, aynı işaret %37, destekli değil. Yıllar: 2025 −88, 2026 −59 bps. Hayatta kalma yanlılıklı tabanla aynı; h=6 profil dışı. Birincil (hisse) OOS t 2,54. |
| R6-04/k10Rp1/B/uzun | K7 | G4 bilanço öncesi prim: R-10 kapanışında al, R+1'de çık (büyük evren, yalnız uzun) | COK(122) | uzun | 11 | kapanis | SPY:250 | 31.44 | 2.72 | 61.39 | 1916 | 3.17 | 2.82 | 0.0048 | -40.35 | -1.71 | 57.22 | 2.96 | -43.92 | sinyal fiyattan bağımsız (takvim): örtüşme %100, korunan pay 1,0 | 50.62 | b+ c− d+ e− f+ | Son dönem negatif (2025 −113, 2026 −39 bps). En iyi %5 çıkınca −44 bps. OOS-2022'de t 1,85. VIX>30: 21 bölüm, %62, destekli değil. h=11, 1–3 gün profilinin dışında. RF1a içi BH q 0,101. |
| R6-03/tR/B/uzun | K7 | So-Wang bilanço öncesi dönüş, yalnız uzun: R-2 kapanışında (t-4→t-2 SPY'ye göre getiri < genişleyen q20) al, R+1'de çık | COK(122) | uzun | 3 | kapanis | yok | 95.9 | 3.23 | 132.63 | 460 | 3.07 | 2.55 | 0.0104 | -54.23 | -1.29 | 123.96 | 3.02 | 31.8 | son 730 gün: 331 kapanış tetiği, örtüşme %91,8; ikisi de negatif (kapanış −55, 15:30 −73 bps), korunan pay 1,33 anlamsız | 123.91 | b+ c− d+ e+ f+ | Birincil analizde OOS'tan geçen tek kural; müzayede maliyetiyle de yalnız (c) maddesinden düşüyor. Son dönem −54 bps (2025 −107, 2026 −100 bps). VIX>30: 15 bölüm, %73, destekli. Tek yönlü uzun; tepki günü uyuşmazlığı %12–20; hayatta kalma yanlılığı. RF1a içi BH q 0,109. |
| R6-04/k3Rp1/B/uzun | K7 | G4 bilanço öncesi prim: R-3 kapanışında al, R+1'de çık (büyük evren, yalnız uzun) | COK(122) | uzun | 4 | kapanis | SPY:250 | 30.2 | 3.18 | 40.11 | 1953 | 2.59 | 2.53 | 0.0104 | -43.34 | -2.13 | 38.26 | 2.47 | -43.02 | sinyal fiyattan bağımsız (takvim): örtüşme %100, korunan pay 1,0 | 29.54 | b+ c− d+ e− f+ | Son dönem anlamlı biçimde negatif (t −2,13). En iyi %5 çıkınca −43 bps. net/σ 0,155. Birincil (hisse) OOS t 1,91: yalnız maliyet düşünce aday oluyor. RF1a içi BH q 0,109. |
| R5-08/a10/B/kisa | K7 | R5-8 /hisse−sektör/ ≥ %10 tepki günü yönünde (sürüklenme), yalnız kısa | COK(82) | kisa | 3 | kapanis | SPY:250 | 122.55 | 2.08 | 135.37 | 48 | 2.28 | 2.62 | 0.0436 | 52.97 | 0.85 | 135.13 | 2.48 | 88.87 | son 730 gün: 64 kapanış tetiği, örtüşme %93,8; kapanış 43 bps, 15:30 75 bps, korunan pay 1,74 (hacim koşulu gün sonu hacmiyle) | 122.73 | b− c+ d+ e+ f+ | OOS t 2,28 < 2,5, en çok DÜŞÜK. OOS'ta 48 işlem. Komşu h1 ve h2'de OOS t 0,99 ve 1,33; yalnız h3 geçiyor, kırılgan. Son dönem t 0,85. VIX>30: 7 bölüm, %43. OOS-2022'de t 1,02. Birincilde h3 aday değildi (IS t eşikte). RF1a içi BH q 0,37. |
| R6-04/k10Rp1/K/uzun | K7 | G4 bilanço öncesi prim R-10 → R+1 (küçük/tema evreni, uzun) | COK(121) | uzun | 11 | kapanis | SPY:250 | 99.31 | 2.66 | 140.7 | 820 | 1.77 | 0.97 | 0.144 |  |  |  |  |  |  | 119.65 |  | OOS t < 2, t_anormal < 1; tema evreni. Elendi. |
| R5-08/a5/B/iki | K7 | R5-8 /hisse−sektör/ ≥ %5 tepki günü yönünde (iki yön) | COK(119) | iki | 2 | kapanis | SPY:250 | 39.37 | 3.49 | 29.69 | 520 | 1.7 | 2.01 | 0.162 |  |  |  |  |  |  | 18.36 |  | Aynı yön ama OOS t_kume 1,70 < 2. |
| R5-08/a5/B/iki | K7 | R5-8 /hisse−sektör/ ≥ %5 tepki günü yönünde (iki yön) | COK(119) | iki | 3 | kapanis | SPY:250 | 42.82 | 3.24 | 30.46 | 520 | 1.5 | 1.75 | 0.425 |  |  |  |  |  |  | 19.09 |  | OOS t 1,50 < 2. |
| R5-08/a10/B/iki | K7 | R5-8 /hisse−sektör/ ≥ %10 tepki günü yönünde (iki yön) | COK(93) | iki | 3 | kapanis | SPY:250 | 89 | 2.63 | 64.41 | 115 | 1.45 | 1.51 | 0.165 |  |  |  |  |  |  | 52.84 |  | OOS t 1,45 < 2 (h1 1,39, h2 1,37). |
| R5-08/a10/B/kisa | K7 | R5-8 ≥ %10, yalnız kısa | COK(82) | kisa | 2 | kapanis | SPY:250 | 133.57 | 3.05 | 72.21 | 48 | 1.33 | 1.6 | 0.164 |  |  |  |  |  |  | 60.02 |  | OOS t 1,33 < 2; h3'teki geçişin komşu ufukta tutmadığını gösteriyor. |
| R6-03/tF/B/uzun | K7 | So-Wang uzun, t = dosyalama günü | COK(122) | uzun | 3 | kapanis | yok | 85.85 | 2.86 | 39.36 | 468 | 1.02 | 0.41 | 0.561 |  |  |  |  |  |  | 30.57 |  | Komşu tarih tanımında OOS t 1,02; R6-03 parametreye duyarlı. |
| R6-01/AR5/B/iki | K7 | Tepki günü /AR/ ≥ %5 ve hacim ≥ 2x yönünde | COK(120) | iki | 2 | kapanis | yok | 47.6 | 3.99 | 19.06 | 473 | 1.02 | 1.02 | 0.252 |  |  |  |  |  |  | 12.09 |  | IS'teki güçlü devam etkisi 2020 sonrasında kayboldu (h1 t −0,21, h3 0,66). |
| A-KR-ii-W250-z2-ayrisma-yeni | K1 | kripto: takipçi − b·lider z<−2 (W250) → ayrışma devam (yeni yapı) | COK | iki | 3 | kapanis | SPY:250 | 226.04 | 2.03 | 56.48 | 327 | 0.76 | 0.63 | 0.118 |  |  |  |  |  |  | 33.69 |  | Yeni yapı hattı (OOS2 2024–26, eşik t ≥ 3); OOS2 t 0,76. Elendi. |
| R8-09/U | K3 | Panik rejiminde 12-1 kaybedenler uzun | sepet COK | uzun | 3 | kapanis | yok | 456.55 | 2.74 | 93.97 | 238 | 0.26 | 0.05 | 0.313 |  |  |  |  |  |  | 25.43 |  | IS ≈ 8 olay gününe dayanıyor; OOS t 0,26. Elendi. |
| C-ULKE/W60/z2 | K3 | Ülke ETF ABD seansı z(60) > 2 → ertesi gün dönüş | 8 ülke ETF havuzu | iki | 1 | kapanis | yok | 24.2 | 2.26 | 5.32 | 419 | 0.19 | 0.27 | 0.892 |  |  |  |  |  |  | -5.43 |  | Müzayede maliyetiyle yeni IS adayı; OOS t 0,19. Elendi. |
| R8-09/LS | K3 | Panik kaybedenler uzun, kazananlar kısa (gece) | sepet | iki | 0 | acilis | yok | 35.49 | 3.1 | -19.69 | 690 | -0.46 | -0.36 | 0.628 |  |  |  |  |  |  | -64.29 |  | OOS'ta işaret döndü. Elendi. |
| A-EV-ii-W60-z1-ayrisma-yeni | K1 | EV: takipçi − b·lider z<−1 (W60) ayrışma, gece (yeni yapı) | COK | iki | 0 | acilis | SPY:250 | 27.86 | 2.07 | -14.39 | 951 | -1.17 | -0.38 | 0.336 |  |  |  |  |  |  | -49.73 |  | OOS2'de ters işaret. Elendi. |
| A-YZ-i-W250-z2-donus-yeni | K1 | yapay zekâ yazılımı: lider artık z>2 → takipçi dönüş, gece (yeni yapı) | COK | iki | 0 | acilis | SPY:250 | 59.05 | 2.08 | -23.96 | 92 | -0.72 | -0.3 | 0.709 |  |  |  |  |  |  | -63.14 |  | OOS2'de ters işaret. Elendi. |
| A-UZ-ii-W250-z1-yakalama-yeni | K1 | uzay: takipçi − b·RKLB z<−1 (W250) → yakalama (yeni yapı) | COK(3) | iki | 1 | kapanis | SPY:250 | 2174.8 | 2.16 | -68.29 | 285 | -1.37 | -1.07 | 0.13 |  |  |  |  |  |  | -90.42 |  | IS2'de yalnız 2 işlem (birincildeki aynı artefakt); OOS2'de ters işaret. Elendi. |

## Bugünkü durum

Ek 2 ölçütlerinin (a hariç) hepsini sağlayan kural yok; bugün uygulanacak bir sinyal yok. Bilgi için, OOS'ta t ≥ 2 olan beş kuralın 20.11.2026 durumu:
- R6-03 tR uzun: INTU'da 18.11 kapanışında açılmış bir pozisyon var. Panele göre INTU'nun tepki günü 20.11. Çıkış 23.11 kapanışı (R+1).
- R6-04 k10/k5/k3 Rp1 uzun: INTU'da sırasıyla 6.11, 13.11 ve 17.11 kapanışında açılmış pozisyonlar var; çıkış 23.11 kapanışı. Kural takvime dayalı. 23.11 kapanışında giriş için tepki gününün sırasıyla 23.11'den 3, 5 ya da 10 işlem günü sonra olması gerekir. Tarihler tahmini; K7_bugun.csv'ye göre büyük evrende yakın olaylar: ADI 24.11, DE ve WDAY 25.11, CRM 3.12, AVGO, COST, LULU ve ADBE 10–11.12.
- R5-08 a10 kısa: 18–20.11'de tetiklenme yok (INTU'da 20.11 koşulu sağlanmadı). 23.11 kapanışı için tetik koşulu: tepki günü 23.11 olan büyük evren hissesinde (hisse günlük getirisi − sektör ETF'i günlük getirisi) ≤ −%10 ve hacim(23.11) ≥ hacim(20.11) ise kapanışta açığa sat ve SPY:250 β ile koru. Tahmine göre 23.11'de bilanço tepki günü olan büyük evren hissesi yok.
Bunların hiçbiri Ek 2'den geçmedi; ikisi (R6-03 ve R5-08) en çok DÜŞÜK, diğerleri ELENDİ.

## Sapmalar

Ölçüt, kural ve varyant değişmedi. Özgün betikler, motor.py ve yukle.py'ye dokunulmadı; aileler modül olarak içe aktarıldı. Kural üretimi ve aday ölçütü ailelerin kendi işlevleriyle yapıldı (K1.gecti, K2.gecti, K3.karar_t mantığı, K7.gecti; K7'de n ≥ 10 ve rejim satırları V<20/V>30 dahil). Sapmalar ve yorumlar:
1. 15:30 testi aileye özgü yazıldı.
- R6-03: özgün asama_tani'deki so_wang(fiyat_s) yöntemi kullanıldı; ölçü net_hisse yerine net_muzayede.
- R5-08: (hisse − sektör ETF) getirisi 15:30 fiyatı / önceki günün ham kapanışıyla kuruldu. Hacim koşulu (hacim R ≥ hacim R−1) gün sonu hacmiyle kaldı, çünkü saatlik veride 15:30 hacmi yok.
- R6-04: sinyal fiyattan bağımsız (takvim günü). Örtüşme tanım gereği %100, ayrı hesap yapılmadı.
2. Yıllara göre net, uzun/kısa bacak ve VIX > 30 bölümleri, motorun net_bps'iyle tutarlı olsun diye işlem listesinin tamamından (portföy dışındakiler dahil) hesaplandı.
3. Birincil maliyetle karşılaştırma satırları ('hisse') OOS'ta bootstrap'sız hesaplandı ve sonuc_ek2_RF1a.csv'ye eklendi (117 satır, komisyon='hisse').
4. OOS'ta "aynı yön ve t ≥ 2" testinde tek yönlü kurallar için t_anormal ≥ 2 de istendi (aile gecti işlevi, Sapma 4). Beş kuralın hepsinde t_anormal ≥ 2,5, sonucu değiştirmiyor.
5. Ek 2 (c) yalnız net > 0 istiyor; t de raporlandı. Yeni yapı hattındaki K1 adaylarında (OOS2 eşiği t ≥ 3) ayrı son dönem yok; hiçbiri OOS'ta t ≥ 2'ye ulaşmadığı için ayrıntı hesaplanmadı.
6. Doğrulama amacıyla aynı adapter EK2_KOM=hisse ile çalıştırıldı; çıktısı proje dosyalarına değil scratchpad/denetim_hisse altına yazıldı. Birincil IS aday sayıları birebir çıktı: K1 1, K2 0, K3 1, K7 23.

## Notlar

- Aileler arası BH için 42 adayın OOS p_bootstrap değerleri: /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2/RF1a/oos_ozet_RF1a.csv, oos_p sütunu. Hesaplanamayan p yok; olsaydı 1,0 yazılacaktı.
- En küçük p'ler: R6-04 k5Rp1 0,0010; k10Rp1 0,0048; R6-03 tR 0,0104; R6-04 k3Rp1 0,0104; R5-08 a10 kısa 0,0436. Diğerleri ≥ 0,118.
- Yalnız bu 42 aday içinde BH %10'dan yalnız k5Rp1 geçiyor (q 0,042). k10Rp1, R6-03 ve k3Rp1'in q değerleri 0,10–0,11, eşiğin hemen üstünde.
- Ek 2'nin dokuz ailesi birleşince m büyüyeceği için q değerleri daha da yükselir. Zaten (c) maddesi hepsini eliyor.
- "İnanılmayacak kadar iyi" denetimi: R6-03 ve R5-08 a10 kısa'da OOS işlem başına > 100 bps var ama t < 6. Yine de K7'nin bakis_testi'ni (bütün 112 varyantın imzası, 3 T0) yeniden çalıştırdım: temiz (0 fark). K1 ve K2'de OOS'ta t ≥ 2 olan kural olmadığı için oradaki bakis_testi sütun kümesi sorunu bu işe girmedi.
- K1 A-UZ adayı IS2'de yine yalnız 2 işleme dayanıyor (2.175 bps); birincildeki küçük örneklem artefaktı.
- R6-04 k10/k5/k3 Rp1 büyük evren uzun yeni aday. Ama kapsamı d4_K7'nin hayatta kalma tanısıyla ("bütün olaylar R−2'de al, R+1'de çık", OOS +61 bps) neredeyse aynı. Panel bugünün listesinden kurulduğu için uzun yönlü bilanço öncesi prim sistematik olarak şişer. 2025–2026'daki çöküş (−40 ile −113 bps arası) de bununla uyumlu.
- R5-08 a10 kısa yalnız kısa bacakta. Hayatta kalma yanlılığı kısa bacağın aleyhine işler (borsadan çıkan kaybedenler panelde yok), yani bu sonuç bu açıdan muhafazakâr. Ama OOS'ta yalnız 48 işlem var ve 2008'de −201 bps.
- Müzayede maliyeti işlem başına ~10–20 bps kazandırıyor (örnek: R6-04 k3Rp1, hisse 29,5 → müzayede 40,1 bps). K7'nin 12 yeni adayının hepsi bu farktan geliyor. K1 ve K3'ün yeni adayları OOS'ta sıfıra yakın ya da ters.
- Paylaşılan makinede OMP_NUM_THREADS=1 kullanıldı. Bütün aşamalar toplam 3 dakikanın altında sürdü. git işlemi yapılmadı.

## Dosyalar

- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/ek2_RF1a.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/ek2_RF1a_detay.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/aday_ek2_RF1a.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/sonuc_ek2_RF1a.csv
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2/RF1a/oos_ozet_RF1a.csv
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2/RF1a/detay_K7.json
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2/RF1a/is_K1.pkl
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2/RF1a/is_K2.pkl
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2/RF1a/is_K3.pkl
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2/RF1a/is_K7.pkl
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2/RF1a/denetim_hisse/
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2/RF1a/k7_bakis.txt
