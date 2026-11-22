# RF1b · Ek 2: maliyet duyarlılığı (kapanış müzayedesi emri senaryosu)

araç: 29/40

## Özet

Kapanış/açılış müzayedesi emri senaryosunda (bacak başına yalnız 1,5 bps komisyon; hacim kademesi ve VIX çarpanı yok; nakit faizi, ödünç ücreti ve temettü kesintisi aynen) beş ailenin 1.616 varyantı yeniden elendi. Varyantların dağılımı: K4a 674, K4b 124, K5 191, K6 449, K9 178. Bu sayılar birincil analizle birebir aynı. Birincil maliyetle ('hisse') aynı koşuda yeniden hesaplanan IS aday sayıları da d4 dosyalarıyla örtüşüyor: 10, 1, 4, 5 ve 1.

Ne değişti: ucuz maliyet IS netini ETF'lerde işlem başına 2–12 bps, SPY korunmalı VIXY'de yaklaşık 58 bps (VIX > 30 çarpanı kalktığı için) artırdı. IS adayı 21'den 27'ye çıktı. Yeni 6 aday:
- K4a seri≥5 SOXX gece
- K4a seri≥7 hisse havuzu gece
- K4b R3-02 kontrol gece
- K5 R6-09 (havuz, t_kume 2,61)
- K6 DIX üst %10 → SPY ve SPXL h=1

Ne ayakta kaldı: hiçbir şey. 27 adayın hiçbiri OOS'ta aynı yönde ve ilgili t ≥ 2 değil, bu yüzden Ek 2'nin (b)–(f) ölçütlerine ve madde 7'ye geçen kural yok. En yakın üç aday:
- K4a seri≥5 DIA h=1: OOS +46 bps, t 1,63, t_anormal 1,10, p 0,056. Son dönem −1 bps.
- K5 R7-06A QQQ h=2: +37 bps, t 1,52, p 0,26.
- K4a hisse havuzu seri≥7 gece: +13 bps, t 0,99, p 0,072.

Bu 27 aday içinde BH q en az 0,79 çıktı. Birincil sonuç ("hiçbiri geçmedi") bu beş ailede maliyet varsayımından bağımsız. Adayların sırası ve işaretleri iki senaryoda neredeyse aynı: OOS'taki fark yalnız maliyet farkı kadar.

K9, betimsel ve karar dışı: koşulsuz "kapanışta al, açılışta sat" kuralının müzayede neti işlem başına şöyle:
- SPY: IS −0,0 bps, OOS −1,5 bps, son dönem +1,0 bps (t 0,65)
- QQQ: +1,8 / −0,9 / +2,9 bps
- IWM: +0,8 / +3,2 / +1,7 bps
- DIA: +0,0 / −1,4 / −1,2 bps
- TQQQ: IS +12,2 bps (t 2,90), OOS +2,9, son dönem +14,3 (t 2,06), 2005–2026 toplamı +10,3 (t 3,47)
- UPRO: 2005–2026 toplamı +6,5 bps (t 2,39)

Bu kurallarda anormal getiri tanım gereği 0 olduğu için t_anormal şartı hepsini eler. Bu şart değiştirilmedi.

En önemli çekince: müzayede senaryosu bacak başına 1,5 bps ile alt sınır maliyettir. Müzayede dengesizliği, emir kesim saati ve kaldıraçlı ETF'lerde müzayede derinliği modellenmedi. Yine de en iyimser maliyetle bile OOS'u geçen kural yok, bu yüzden çekince sonucu değiştirmiyor.

## Aile tablosu

| aile | varyant | IS adayı (birincil) | IS adayı (müzayede) | OOS t ≥ 2 | Ek 2'den geçen |
|---|---|---|---|---|---|
| K4a | 674 | 10 | 12 | 0 | 0 |
| K4b | 124 | 1 | 2 | 0 | 0 |
| K5 | 191 | 4 | 5 | 0 | 0 |
| K6 | 449 | 5 | 7 | 0 | 0 |
| K9 | 178 | 1 | 1 | 0 | 0 |

## Adaylar

| kural_id | aile | ad | hedef | yon | h | cikis | korunma | is_net_bps | is_t | oos_net_bps | oos_n | oos_t | oos_t_anormal | oos_p | son_net_bps | son_t | girisA_oos_net_bps | girisA_oos_t | en_iyi5suz_bps | saatlik_1530 | birincil_oos_net_bps | olcutler | gerekce |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K4a-seri>=5 | K4a | DIA ust uste >=5 dusus gunu -> kapanista uzun | DIA | uzun | 1 | kapanis | yok | 37.45 | 2.42 | 46.49 | 20 | 1.63 | 1.1 | 0.056 | -1.14 | -0.31 | 52.62 | 1.94 | 3.41 | hesaplanmadi (OOS t<2) | 41.52 | b- c- d+ e+ f+ (bilgi amacli; OOS t<2) | OOS t 1,63 < 2 ve t_anormal 1,10 < 2: DUSUK. En yakin aday. |
| R7-06A | K5 | Vade haftasi pazartesi-sali QQQ uzun | QQQ | uzun | 2 | kapanis | yok | 35.29 | 3.38 | 36.81 | 48 | 1.52 | 0.78 | 0.261 | 24.91 | 0.76 | 62.42 | 1.88 | 11.14 | hesaplanmadi (OOS t<2) | 33.98 | b- c+ d+ e+ f+ (bilgi amacli; OOS t<2) | OOS t 1,52 ve t_anormal 0,78: DUSUK; endeksin yukselis egilimini tasiyor. |
| R3-07 | K6 | DIX 252g ust %10 -> SPXL uzun (Giris A) | SPXL | uzun | 1 | kapanis | yok | 37.02 | 2.35 | 30.19 | 169 | 1.19 | 0.78 | 0.222 | 15.55 | 0.56 | 30.19 | 1.19 | -17.02 | gerekmez (kural zaten ertesi acilista giriyor) | 19.23 | b- c+ d- e- f- | Yalniz muzayede maliyetiyle yeni aday (birincilde aday degildi). OOS t 1,19: DUSUK. |
| R1-01 | K6 | Simon-Campasano roll vekili; VIXY uzun bacak (roll<-0,10), SPY korumali | VIXY | uzun | 5 | kapanis | SPY:250 | 822.48 | 3.3 | 465.58 | 9 | 1.16 | 0.82 | 0.296 | -442.28 | -0.66 | 518.43 | 1.38 | -345.57 | hesaplanmadi (OOS t<2) | 413.01 | b- c- d- e- f+ | OOS'ta 9 islemin hepsi 2020'de; t 1,16. Son donemde zararli. DUSUK. |
| R1-01 | K6 | VIXY uzun bacak (roll<-0,10), SPY korumali | VIXY | uzun | 2 | kapanis | SPY:250 | 315.35 | 2.49 | 239.93 | 18 | 1.1 | 0.9 | 0.228 | -130.19 | -0.65 | 183.31 | 0.89 | -56.67 | hesaplanmadi | 188.53 | b- c- d- e- f+ | OOS'taki 18 islemin hepsi 2020'de; t 1,10: DUSUK. |
| K4a-seri>=7 | K4a | Donem basi hisse havuzu, ust uste >=7 dusus -> gece uzun | COK(176) | uzun | 0 | acilis | yok | 19.93 | 2.47 | 12.76 | 689 | 0.99 | 0.83 | 0.072 | -8.87 | -0.71 |  |  | -13.31 | hesaplanmadi | 4.05 | b- c- d? e- f- | Yalniz muzayede maliyetiyle yeni aday (birincil IS neti 8,4 bps). OOS t_kume 0,99: DUSUK. Giris A gece kuralinda uygulanmaz. |
| R3-07 | K6 | DIX 252g ust %10 -> SPY uzun (Giris A) | SPY | uzun | 1 | kapanis | yok | 11.06 | 2.1 | 8.83 | 169 | 0.93 | 0.79 | 0.296 | 2.61 | 0.28 | 8.83 | 0.93 | -6.94 | gerekmez | 5.14 | b- c+ d- e- f- | Yeni aday; OOS t 0,93 ve net < 10 bps: DUSUK / onemsiz. |
| R3-02.SPY.kontrol | K4b | SPY /r/>=%1,5 ve IBS 0,3-0,7 -> ters yon (kontrol) | SPY | iki | 3 | kapanis | yok | 113.67 | 2.22 | 49.9 | 22 | 0.86 | 0.56 | 0.485 | 136.57 | 2.29 | 67.23 | 1.49 | -78.9 | hesaplanmadi | 44.61 | b- c+ d- e- f+ | OOS t 0,86; kontrol varyanti (mekanizma degil). Uzun bacak +101, kisa bacak +7 bps. DUSUK. |
| K4a-seri>=5 | K4a | DIA >=5 dusus gunu -> uzun | DIA | uzun | 2 | kapanis | yok | 81.89 | 2.96 | 21.3 | 15 | 0.85 | 0.28 | 0.595 | -13.23 | -0.53 | 12.12 | 0.43 | -26.94 |  | 16.6 | b- c- d- e- f+ | OOS t 0,85: DUSUK. |
| EK-B1h1 | K5 | TLT ay sonu uzun T-1->T | TLT | uzun | 1 | kapanis | yok | 20.11 | 3.34 | 6.46 | 48 | 0.85 | 0.75 | 0.662 | -14.89 | -1.52 | 2.55 | 0.78 | -10.13 |  | 3.47 | b- c- d- e- f- | OOS t 0,85, son donem negatif: DUSUK. |
| R1-01 | K6 | VIXY uzun bacak (roll<-0,10), SPY korumali | VIXY | uzun | 3 | kapanis | SPY:250 | 530.87 | 2.8 | 298.48 | 13 | 0.84 | 0.69 | 0.323 | -271.19 | -0.53 | 386.35 | 1.1 | -291.05 |  | 245.31 | b- c- d- e- f+ | OOS islemlerinin hepsi 2020'de; t 0,84: DUSUK. |
| EK-B1h3 | K5 | TLT ay sonu uzun T-3->T | TLT | uzun | 3 | kapanis | yok | 45.02 | 4.23 | 18.47 | 48 | 0.74 | 1.51 | 0.374 | 3.56 | -0.33 | 9.34 | 0.44 | -0.01 |  | 15.75 | b- c+ d- e- f+ | OOS t 0,74: DUSUK. |
| K4a-seri>=5 | K4a | SOXX >=5 dusus -> gece uzun | SOXX | uzun | 0 | acilis | yok | 76.88 | 2.33 | 5.92 | 19 | 0.63 | 0.1 | 0.842 | -1.34 | -0.29 |  |  | -19.62 |  | -0.97 | b- c- d? e- f- | Yeni aday; OOS t 0,63: DUSUK. |
| EK-B1h2 | K5 | TLT ay sonu uzun T-2->T | TLT | uzun | 2 | kapanis | yok | 29.42 | 2.94 | 4.32 | 48 | 0.51 | 0.66 | 0.798 | 16.46 | 0.46 | 19.14 | 1.47 | -13.1 |  | 1.38 | b- c+ d- e- f- | OOS t 0,51: DUSUK. |
| R6-09 | K5 | Erken/gec bilanco havuzu (iki yonlu) | COK(144) | iki | 4 | kapanis | yok | 36.2 | 2.61 | 5.16 | 1168 | 0.19 | -0.19 | 0.282 | 23.33 | 0.95 | -1.14 | -0.04 | -87.93 |  | -1.79 | b- c+ d- e- f- | Yeni aday (birincilde t_kume 1,98); OOS t_kume 0,19. Kisa bacak -104 bps: DUSUK. |
| K4a-seri>=5 | K4a | IWM >=5 dusus -> gece uzun | IWM | uzun | 0 | acilis | yok | 38.3 | 3.03 | 16.84 | 21 | 0.02 | 0.61 | 0.391 | -0.24 | 0.35 |  |  | -0.51 |  | 13.89 | b- c- d? e- f- | OOS t 0,02: DUSUK. |
| R8-03 | K6 | VIX 252g yuzdelik >=%97 -> SPY uzun | SPY | uzun | 5 | kapanis | yok | 157.46 | 3.71 | -24.23 | 15 | 0 | -0.84 | 0.868 | 165.03 | 1.85 | 24.36 | 0.22 | -137.4 |  | -30.56 | b- c+ d- e- f- | OOS'ta isaret dondu: ELENDI. |
| R8-03 | K6 | VIX 252g yuzdelik >=%97 -> QQQ uzun | QQQ | uzun | 5 | kapanis | yok | 193.7 | 3.6 | 5.74 | 15 | -0.11 | -0.95 | 0.961 | 198.6 | 1.61 | 48.15 | 0.05 | -89.36 |  | -0.59 | b- c+ d- e- f- | OOS'ta olcekli t ve t_anormal negatif: ELENDI. |
| R8-03:VIX(t-1)>=40:bekle5 | K4a | VIX(t-1)>=40 + 5 gun bekle -> SPY uzun | SPY | uzun | 2 | kapanis | yok | 242.53 | 2.15 | -85.02 | 9 | -0.4 | -0.63 | 0.63 | 870.82 |  |  |  | -310.79 |  | -92.02 | b- c(n=1) d- e- f- | IS'te n=7; OOS'ta isaret dondu: ELENDI. |
| R8-03:VIX(t-1)>=40:bekle5 | K4a | VIX(t-1)>=40 + 5 gun bekle -> QQQ uzun | QQQ | uzun | 2 | kapanis | yok | 292.43 | 2.5 | -67.69 | 9 | -0.43 | -0.68 | 0.696 | 992.31 |  |  |  | -290.34 |  | -74.69 | b- c(n=1) d- e- f- | OOS'ta isaret dondu: ELENDI. |
| R7-10b | K9 | SPY kk <= -%2,5 -> QQQ uzun | QQQ | uzun | 3 | kapanis | yok | 138.81 | 2.63 | 25.29 | 26 | -0.46 | -0.24 | 0.73 | 31.27 | 0.49 | -15.21 | -0.67 | -82.15 |  | 20.11 | b- c+ d- e- f- | OOS'ta net > 0 ama olcekli t ve anormal getiri negatif: ELENDI. |
| R3-02.SPY.kontrol | K4b | SPY kontrol varyanti, gece | SPY | iki | 0 | acilis | yok | 44.14 | 2.06 | -16.81 | 25 | -0.75 | -0.32 | 0.516 | -7.18 | -0.09 |  |  | -52.66 |  | -22.01 | b- c- d? e- f- | Yeni aday; OOS'ta isaret dondu: ELENDI. |
| R8-08:uzun(karsilastirma) | K4a | Ayi rallisinde uzun (karsilastirma kolu) QQQ | QQQ | uzun | 3 | kapanis | yok | 122.96 | 8.73 | -187.38 | 5 | -1.13 | -1.27 | 0.486 |  |  |  |  |  |  | -194.38 | b- c(n=1) d- e- f- | IS'te n=4 (t 8,7 kucuk orneklemden). OOS'ta isaret dondu: ELENDI. |
| R8-08:uzun(karsilastirma) | K4a | Ayi rallisinde uzun SPY | SPY | uzun | 3 | kapanis | yok | 109.69 | 4.19 | -233.07 | 7 | -1.59 | -1.34 | 0.296 |  |  |  |  |  |  | -240.07 | b- c- d- e- f- | OOS'ta isaret dondu: ELENDI. |
| R8-06:seri==6 | K4a | QQQ 6 gun dusus -> gece uzun | QQQ | uzun | 0 | acilis | yok | 88.57 | 4.16 | -189.05 | 2 |  |  | 0.241 | 106.23 |  |  |  |  |  | -193.55 | b- (n=2) | OOS'ta 2 islem, isaret dondu: ELENDI. |
| K4a-seri>=7 | K4a | SMH >=7 dusus -> uzun | SMH | uzun | 1 | kapanis | yok | 172.04 | 5.04 | 155.49 | 1 |  |  | 0.631 | 3.47 | 0.04 | 132.8 |  |  |  | 150.49 | b- (n=1) | IS'te n=3, OOS'ta n=1: t hesaplanamaz, DUSUK (az olay). |
| K4a-seri>=7 | K4a | SMH >=7 dusus -> uzun | SMH | uzun | 2 | kapanis | yok | 277.98 | 2.73 | 292.09 | 1 |  |  | 0.565 | -43.9 | -0.27 | 269.09 |  |  |  | 287.09 | b- (n=1) | OOS'ta n=1: DUSUK (az olay). |

## Bugünkü durum

Uygulanmaz. Bu senaryoda OOS'u geçen kural yok, bu yüzden 20 Kasım 2026 kapanış sinyali ve 23 Kasım tetik koşulu hesaplanmadı.

## Sapmalar

1. Özgün betiklerin hiçbiri değiştirilmedi. Kural üretimi şöyle alındı:
- K4a, K5, K6 ve K9 modül olarak içe aktarıldı.
- K4b modül düzeyinde çalıştığı için kaynağı "1) sinyaller + bakis" başlığına kadar exec ile aynen yürütüldü.
- Ortak yardımcılar ve aday/sonuç adımları ek2_<aile> adlandırmasının dışında üç ayrı dosyada: ek2_ortak_RF1b.py, ek2_RF1b_aday.py, ek2_RF1b_sonuc.py.

2. IS ve OOS aynı çağrıda iki komisyonla koşuldu: komisyon=("hisse","muzayede"). Bu, birincil karşılaştırma satırını verir. Aday seçimi yalnız muzayede satırlarıyla yapıldı.

3. Aday listesi OOS koşusundan önce yazıldı (dosya zamanı 00:50, OOS sonrası).

4. Ek 2'nin (b)–(f) ölçütleri ve 15:30 testi yapılmadı: tanım gereği yalnız OOS'ta aynı yön ve t ≥ 2 olan kurallar için yapılacaktı, böyle kural çıkmadı. Bilgi amacıyla bütün adaylar için şunlar yine de verildi: son dönem, Giriş A, en iyi %5'siz net, uzun/kısa bacak, VIX > 30 ve yıllık dökümler. Tablodaki "olcutler" sütunu bu sayılardan türetildi ve karar değil.

5. Atlanan ya da yeniden koşulmayan adımlar:
- IS adaylarının IS bootstrap'ı (K4a'daki bilgi sütunu) atlandı; aday seçimine girmiyor.
- İleriye bakma testi yalnız K4b'de yeniden koşuldu; temiz çıktı. Diğer ailelerde sinyal işlevleri aynen içe aktarıldığı için özgün temiz test geçerli sayıldı.

6. Gece kurallarında Giriş A tanımsız (açılışta gir, açılışta çık). K6 DIX kuralları zaten ertesi açılışta giriyor; Giriş A satırı kuralın kendisi.

7. K9'un yeni yapı hattı için kullandığı OOS eşiği 3,0'dı. Bu hatta aday çıkmadığı için konu boşa düştü.

8. Bu 27 aday için BH q bilgi amacıyla hesaplandı (en düşük 0,79). Aileler arası BH ana ajanda; bütün p-değerleri ek2_RF1b_oos_ayrinti.csv'nin oos_p sütununda, hesaplanamayanlar 1,0.

## Notlar

Tutarlılık: beş ailede varyant sayıları (674/124/191/449/178) ve birincil maliyetle yeniden hesaplanan IS aday sayıları (10/1/4/5/1) d4 dosyalarıyla birebir aynı. Birincil OOS değerleri de d4 ile örtüşüyor (örnek: K4b R3-02 kontrol h=3 +44,6 bps, t 0,79; d4'te +45, t 0,79).

Şüpheli görünen ama açıklanan sonuçlar (işlem başına > 100 bps ve t > 6 kontrolü):
- K4a R8-08 QQQ: IS'te t 8,73, yalnız 4 işlem. SMH seri≥7: 3 işlem. Büyüklük küçük örneklemden geliyor, iki kural da birincil analizde de aday. OOS'ta R8-08 işaret değiştirdi; SMH 1 işlemle sınanamaz kaldı. Ayrıca ileriye bakma ya da veri hatası aranmadı (yalnız K4b'de test yeniden koşuldu).
- K6 VIXY'deki 300–800 bps işlem başı getiri 2020 ve öncesi birkaç volatilite patlamasından geliyor; OOS'taki işlemlerin hepsi 2020'de.

Maliyet etkisi:
- ETF'lerde gidiş-dönüş tasarrufu 2–12 bps.
- SPY korumalı VIXY'de yaklaşık 50–58 bps (VIX > 30 çarpanı ve hacim kademesi kalktığı için).
- Hisse havuzlarında 9–16 bps.

K9 betimsel: TQQQ koşulsuz gece neti müzayede maliyetiyle 2005–2026 boyunca +10,3 bps/gece (t 3,47). Bu bir kural değil: anormal getiri 0 ve 3x kaldıraçlı gece beta primi. Ayrıca bacak başına 1,5 bps varsayımı kaldıraçlı ETF müzayedelerinde iyimser olabilir. Ters ETF'ler betimlemeye alınmadı.

Ara dosyalar (scratchpad/ek2): is_*.pkl, oos_*.pkl, oossema_*.pkl, betim_K9_gece.csv, aile_ozet_is.csv. sonuc_ek2_RF1b.csv'de 3.420 satır var: 1.616 varyant × 2 komisyon IS satırı ve 188 aday OOS/SON satırı. Notlar sütununda aile ve anahtar yazılı.

## Dosyalar

- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/aday_ek2_RF1b.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/sonuc_ek2_RF1b.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/ek2_RF1b_oos_ayrinti.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/ek2_RF1b_K9_gece_betim.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/ek2_K4a.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/ek2_K4b.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/ek2_K5.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/ek2_K6.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/ek2_K9.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/ek2_ortak_RF1b.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/ek2_RF1b_aday.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/ek2_RF1b_sonuc.py
- /tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/ek2/is_hepsi.pkl
