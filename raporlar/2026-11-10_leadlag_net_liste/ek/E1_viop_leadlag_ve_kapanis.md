# E1_viop_leadlag_ve_kapanis — çıkarım defteri (ham ajan çıktısı)

araç: 13/30

## Özet

Kullanicinin kalibina (oncu hareket etti, hedef geride, ertesi gunlerde yetisme) birebir uyan ve dogrulamadan saglam cikan kural bulunamadi. Dosyalarda 'sektor emsali yukseldi, hisse geride kaldi' biciminde tek degisken olarak test edilen sinyal ise yaramiyor (k_dis: emsal-hisse ayrismasi, 'hissenin kendi artigi emsal etkisini goturuyor'). Calisan sey emsal artigi: yani oncunun KENDI hareketi, hedefin geride olup olmamasina bakilmadan.

Kapanis-kapanis (VIOP uzlasmasi) profilinde dort aday ayakta, hepsi kucuk ve orta/dusuk guvenli. (1) ABD rafinerileri t-1 -> TUPRS: tek net lead-lag; h2 net +42 bps (t 2,7), ama 2024-26 +26 (t 1,0), en iyi 10 islem cikinca t 1,45, PBF'ye bagimli, fon krizinde -142. (2) SAHOL/AKBNK z: lead-lag degil, ortalamaya donus; 2021-26 net +64-70, gercekci beklenti yarisi; 3 gunle sinirlayinca t 1,3-1,65'e duser, yani 1-3 gun C0 profiline tam uymaz (%10 islem >10 gun). (3) Koza TRMET: goreli momentum, kenarin cogu 'sinyal surerse uzat' kuralindan; sabit h2'de net15+tik ~+3; 2026 negatif. (4) XU030 baz sicramasi: mikroyapi; sinyal 18:10-18:15'te belli oluyor, ertesi gun giris -1,8 bps; C0 penceresine kismen uyar.

Dusuk guvenliler: altin->TRALT (hedge'li, h2, 17:55 spot altin; net +35,5, t 2,2; en iyi 10 cikinca t 0,94), FMG/BHP->EREGL (h3 hedge'li; OOS t 0,9), USDTRY->THYAO (kazanc carry/drift; surukluyu cikarinca 2024-26 t 0,8). Kredi notu ve ay donumu yilda 1-2 olay/rejim.

02.11 RAPOR'unda gunluk gecikmeli (t -> t+1 kapanis) dogrulanmis oncu-hedef cifti yoktu: dogrulananlar gun ici (acilis->kapanis) ya da acilis gap'iydi; 04.11'de gap'ler acilista bitti, gun ici kalinti t gunu icinde tukendi (ertesi kapanisa kalan 8-26 bps, t<=1,5). Istisnalar TUPRS ve EREGL.

Notlar arasi celiski var (celiskiler alanina bakin): ozellikle 'dortte dort zayifliyor' ifadesi SAHOL ve altin icin tutmuyor; Koza ve TUPRS icin dogru.

## Sinyal defteri

### ABD rafinerileri (t-1) -> TUPRS

- **sinif:** BIST-VIOP
- **tur:** leadlag
- **oncu:** NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF (beta*SP:SPX cikarilmis)
- **hedef:** BIST:TUPRS1! (F_TUPRS)
- **kural:** P = ort(VLO,MPC,PSX,PBF) - beta*S&P500, ABD'nin onceki gunu (BIST gunu t'den onceki ABD gunleri; beta 250 gun, o gun haric). z = P / 250 BIST gunu std. |z|>1 -> z yonunde (z>0 uzun, z<0 kisa), t uzlasmasinda (18:00-18:10) ac; t+2 uzlasmasinda kapat. Cikis gunu |z|>1 ayni yon -> 2 gun uzat; ters yon -> cevir. Pozisyon yokken yeni sinyal; kontrat vadeye >=3 is gunu kalan. Tek bacak, hedge'siz ana kural.
- **sinyal_saati:** ABD kapanisi (kis 00:00 TSI); karar sabah, emir 18:00-18:10
- **giris_orijinal:** t gunu VIOP uzlasmasi (ayni kapanis, C0)
- **c0_uyumu:** evet
- **c0_notu:** Sinyal onceki gece belli, BIST fiyatina bagli degil; giris 17:50-18:10'da yapilabilir. Ama kuralin 'hedef henuz hareket etmemis' kosulu yok: hedefin kendi gunluk hareketine bakmaz. Uzatma/cevirme nedeniyle 1-3 gun siniri asilabilir. Cikis t+2.
- **tutma:** h2 ana kural (h1 zayif, h3 tutarsiz); rehberde uzatma/cevirme var, en uzun 8 gun
- **yon:** iki yon
- **n:** 492 blok (53/yil) k_dis; 411 pozisyon rehber
- **net_bps:** h1/h2/h3 (8bps): +13,6 (t1,5) / +41,8 (t2,9) / +55,3 (t2,7) k_dis; curut h2 +42,0 (2,72), h3 +41,6 (1,93). Rehber pozisyon bazli +49,2 (t2,53); long +60,5 (213 islem), short +37,1 (198)
- **t:** h2 2,7 (blok); 2,53 (pozisyon)
- **is_oos:** DF h2 IS +32,6 (t1,75) / OOS +50,7 (t2,3) k_dis; curut IS +34,5 (1,71) / OOS +48,8 (2,12); pozisyon IS +39,6 (1,56) / OOS +58,2 (1,98)
- **son_donem:** 2024-26 +26,3 (t1,02) blok; +30,5 (t0,90, n137) pozisyon; rejim-drift duzeltmeli +21,4 (t0,84). En iyi 10 cikinca h2 +20,4 (t1,45), h3 +11,5 (t0,58). PBF cikarilinca t 1,67; yalniz PSX ~0. Fon krizi 2026-09/10 -142 bps (n=9). 2017-19 -9,4
- **maliyet:** 8 bps + tik: +49,2; 15 bps: +42,2 (pozisyon) / +35,0 (blok)
- **hukum:** KOSULLU / ORTA (curut): sinyal gercek, buyukluk abartili; beklenti net +20-25 bps/islem (curut), rehber +20-30; yalniz h2, kucuk boyut
- **guven:** ORTA
- **kaynak:** 2026-11-04_kapanis_1-3gun/rehber/tuprs/REHBER_tuprs.md §2, §8, §13; notlar/k_dis.md 'Kullanilabilir adaylar' #1; notlar/k_dis-suruculer_curut.md 'Aday ayrintilari 1'

### SAHOL/AKBNK oran ortalamaya donusu (Kural A)

- **sinif:** BIST-VIOP
- **tur:** ortalamaya-donus
- **oncu:** BIST:AKBNK (beta ile), karsi bacak BIST:SAHOL
- **hedef:** BIST:SAHOL1! / BIST:AKBNK1! (cift)
- **kural:** S = toplam(r_SAHOL - beta*r_AKBNK), beta = cov250/var250 (1 gun gecikmeli, en az 125 gun). z = (S - ort60)/std60. Giris: |z|>1,5 olan yeni bolumun ilk kapanisinda. z>+1,5: F_SAHOL sat, F_AKBNK al; z<-1,5 tersi. Cikis (A): |z|<=1,5 olan gunun uzlasmasi; zaman siniri ve stop yok. N_AKBNK = yuvarla(N_SAHOL*beta*F_SAHOL/F_AKBNK) (bugun ~0,88; pratikte 1:1).
- **sinyal_saati:** Kapanis (spot ~18:05); emir 18:05 sonrasi, uzlasma 18:10
- **giris_orijinal:** Ayni akşam VIOP uzlasmasi (C0); ertesi gun uzlasma da test edildi
- **c0_uyumu:** kismen
- **c0_notu:** Sinyal kapanista bilinir, giris ayni uzlasma. Ancak lead-lag degil (oncu->hedef yok, iki bacakli oran donusu) ve tutma %10 islemde >10 gun; 1-3 gun siniri uygulanirsa kenar zayiflar. Sabit 1-2 gun calismiyor.
- **tutma:** Medyan 2, ortalama 3,7-3,8 gun; %75 <=4; %90 <=10-11; en uzun 17. Sabit 1/2/3 gun: OOS -19,5 (t-1,12) / +10,7 (0,48) / +47,1 (1,71)
- **yon:** iki yon (long ve short spread)
- **n:** OOS 2021-26: 108 (k_sahol_a) / 106 (k_sahol_b), yilda ~18
- **net_bps:** OOS VIOP A: +63,7 / +69,7 (b); IS spot 2014-20 +57,7. Short spread 67 islem +59 bps, long 41 islem +71 bps (a). h1/h3 brut olay profili OOS: 1 (t0,1) / 58 (t2,2)
- **t:** 3,12 (a) / 3,35 (b); gunluk NW 2,43 / 2,57
- **is_oos:** IS spot 2014-20 +57,7 (3,53) / OOS VIOP 2021-26 +63,7 (3,12). Spot 2005-13 -5,8 (t-0,20) (b)
- **son_donem:** VIOP 2021-22 +21 (t0,53); 2023 +136; 2024 +55 (t0,65); 2025 +51 (1,40); 2026 +137 (4,60); 2024-26 +81,9 (2,75) (a). En iyi 5 cikinca +53,4 (2,60), en iyi 10 cikinca +39,9 (1,93). Maks dusus -2.365/-2.515 bps, ~23 ay su altinda. A + en cok 3 gun: +26 (1,28) (a) / +33,5 (1,65) (b). Benzer ciftlerde tekrarlanmiyor (SAHOL/YKBNK 29, t0,99; SAHOL/GARAN 17, t0,56). Ongorusel beklenti: yarisi, ~30-50 bps
- **maliyet:** 8 bps+tik; 15 bps+tik: 50 (2,44) / 56,6 (2,70); bireysel ~22,5 bps: +51,6 (2,47); 30 bps: ~21-28,6 (t1,0-1,34); basabas ~46-50 bps
- **hukum:** KOSULLU / ORTA. Mekanik hata yok, plasebo p 0,0015, ama 'OOS t~3' abartili; kenar bolgesel/donemsel
- **guven:** ORTA (alt uc)
- **kaynak:** 2026-11-04_kapanis_1-3gun/notlar/k_sahol_a.md §1, §4, §8; notlar/k_sahol_b.md Bagimsiz yeniden hesap, Kontrol 3-6; PRATIK_LISTE.md satir 16

### Koza grubu goreli momentumu (TRMET)

- **sinif:** BIST-VIOP
- **tur:** goreli-momentum
- **oncu:** BIST:TRALT, BIST:TRENJ (grup ortalamasi); beta icin TRALT
- **hedef:** BIST:TRMET1! AL + BIST:TRALT1! SAT (yaklasik 1:2 kontrat)
- **kural:** u = r_TRMET - beta_g*ort(r_TRALT, r_TRENJ), beta_g 250g (shift 1, [0,2;2,0]). z3 = (u_t+u_t-1+u_t-2)/(sigma60*sqrt3). z3>+1,5: TRMET1! al + beta_TA(~0,69)*nominal TRALT1! sat; z3<-1,5 tersi. t uzlasmasinda gir; t+2'de cik. Cikis gununde z3 ayni yonde >1,5 ise 2 gun uzat (en fazla 6 gun). Limit kilidi gunu girme.
- **sinyal_saati:** 17:50-17:55 (canli fiyat); emir 18:00-18:10
- **giris_orijinal:** t gunu VIOP uzlasmasi (ayni kapanis, C0)
- **c0_uyumu:** kismen
- **c0_notu:** Sinyal 17:50'de canli bilinir, ayni kapanista giris. Ama kural 'oncu->hedef yetisme' degil, hedefin kendi goreli momentumu; TRALT hedge bacagi. Kenar uzatmayla 6 gune cikiyor (C0'in 1-3 gunu asilir). Ertesi gun girmek ~-19 bps.
- **tutma:** h1/h2/h3 brut (E0): +26 (t4,2) / +44 (t4,0) / +55 (t3,6); E2 (ertesi giris): +18 / +29 (t2,5) / +34. Pratik kural ort. tutma 2,65 gun, %27 uzatilmis
- **yon:** iki yon; long/short ayri sayi dosyada yok
- **n:** 283 sinyal gunu, 120 bagimsiz olay (k_yurtici); pratik kural P0L 141 islem (18,3/yil)
- **net_bps:** P0L brut +51,7; net8 +43,2; net15 +35,8; net15+tik +28,8. Sabit h2 uzatmasiz kilitli: brut +25,2, net15+tik +3,4; sabit h3 +40,5 / +18,7
- **t:** P0L 3,00; E0 h2 4,05; E2 h2 2,59
- **is_oos:** P0L IS 2019-21 +61,0 (2,40) / OOS 2022-26 +46,7 (2,05)
- **son_donem:** 2024-26 brut +21,7 (t0,93, n52), net15+tik +1,0; 2026 brut -11 / net -29 (n16), 2026 net15+tik toplam -458 bps; en iyi 10 cikinca +10,2 (t0,87); kazanc 'surerse uzat' kuralindan; spot 2010-16 ters isaret; mekanizma belirsiz, TMSF/birlesme riski
- **maliyet:** 8 / 15 bps ve +tik (ort. 7,0 bps; 2024+ 4,8); 1 mn TL emirde ~21-25 bps etki
- **hukum:** KOSULLU / ORTA (curut) ama rehber DUSUK; kucuk boyut, kurali bozmadan
- **guven:** DUSUK (rehber); ORTA (k_yurtici/curut)
- **kaynak:** 2026-11-04_kapanis_1-3gun/rehber/koza/REHBER_koza.md §1, §9.1-9.3b, §13; notlar/k_yurtici.md (h); notlar/k_yurtici-takvim_curut.md Aday 2

### FMG + BHP (ASX) -> EREGL

- **sinif:** BIST-VIOP
- **tur:** leadlag
- **oncu:** ASX:FMG, ASX:BHP (- beta*ASX200 artigi)
- **hedef:** BIST:EREGL1! (F_EREGL); hedge: BIST:XU030D1!
- **kural:** Sepet artigi (FMG, BHP - beta*ASX200) bugunku (t_onceki < tarih <= t) ; z = sinyal / 250 gun std; |z|>1 -> yon(z), h=3 gun tut. Hedge'li: F_EREGL - beta*F_XU030 (beta gecmis 250 gun); 'raw' = hissenin tek bacagi. Giris/cikis VIOP uzlasmasi; orneklemeyen islemler; hedge'li islemde +3 bps XU030 maliyeti. Hedge orani icin sayisal beta dosyada verilmemis.
- **sinyal_saati:** ASX BIST acilmadan kapanir (06:00 UTC snap); sinyal sabah belli; giris t uzlasmasi 18:00-18:10
- **giris_orijinal:** t gunu VIOP uzlasmasi (C0)
- **c0_uyumu:** evet
- **c0_notu:** Sinyal Asya kapanisindan beri belli; kullanicinin 'oncu hareket etmis' kalibina yakin ama hedefin geride kalip kalmadigina bakmaz. 3 gun tutma sinirda. Yilda ~43-50 islem.
- **tutma:** hedge'li h1/h2/h3: +10,6 (t1,4) / +28,1 (t2,5) / +46,9 (t3,2) k_dis; curut +13 / +28 / +46, h5 +12 (t0,46). Raw h3 +51,7 (t2,6)
- **yon:** iki yon; ayri sayi dosyada yok
- **n:** 373, ~43 islem/yil (h3); ~50/yil (h2)
- **net_bps:** h3 hedge'li net8 +46,3 (curut) / +46,9 (k_dis); net15 +39,3
- **t:** 2,95 (curut) / 3,2 (k_dis)
- **is_oos:** DF h3 hedge'li IS +73,6 (t3,7) / OOS +22,3 (t1,0) k_dis; curut IS +80,7 (3,54) / OOS +19,7 (0,92)
- **son_donem:** 2022-23 -50 (t-1,45); 2024-26 +59,2 (t2,21); OOS IS'ten zayif; 1 gun eski ASX sinyali etkisiz (t0,6); yalniz FMG veya yalniz BHP h2 t<=1,1; FMG cikarilinca t~0; en iyi 10 cikinca +21,6 (t1,55); HEKTS gibi ilgisiz hisse de t 2,6-3,1; 4.-5. gunde etki geri donuyor; KRDMD'de IS ~0. 02.11 RAPOR: artiklastirilinca OOS net 8-18 bps (t<=1,2), hedge'li negatif
- **maliyet:** 8 / 15 bps (+3 hedge); EREGL kucuk emir 7,2 bps
- **hukum:** KOSULLU / DUSUK; yalniz h3, hedge'li, kucuk pozisyon
- **guven:** DUSUK (curut); ORTA (k_dis)
- **kaynak:** 2026-11-04_kapanis_1-3gun/notlar/k_dis.md Aday #2 ve ayrinti 2; notlar/k_dis-suruculer_curut.md Aday 2; PRATIK_LISTE.md satir 22; 2026-11-02_viop_leadlag/RAPOR.md Japon celik/ASX satiri

### VIOP altin (bugun) -> TRALT, hedge'li

- **sinif:** Altin-VIOP
- **tur:** leadlag
- **oncu:** TVC:GOLD (pratik, 17:55); arastirma sinyali BIST:XAUUSD1! uzlasmasi (yedek OANDA:XAUUSD)
- **hedef:** BIST:TRALT1! AL/SAT + BIST:XU030D1! ters yon
- **kural:** g = ln(altin_17:55 / onceki BIST gunu 17:55); z = g/sigma250 (17:55/18:00 anlik degisimlerden). z>+1: TRALT AL, XU030 SAT; z<-1: TRALT SAT, XU030 AL. Oran N = yuvarla(10*XU030/(beta*100*TRALT)), beta = TRALT/XU030 250 gun. 18:00-18:10'da ac, 2 BIST gunu sonra kapat; cikista ayni yon sinyal -> 2 gun daha tasi, ters -> cevir (en fazla 3 gun uzat). Arife gunu giris yok; tavanda AL / tabanda SAT kilidinde girme.
- **sinyal_saati:** 17:55 (spot altin); emir 18:00-18:10
- **giris_orijinal:** t gunu VIOP uzlasmasi (C0); arastirmada sinyal ayni uzlasma penceresindeydi
- **c0_uyumu:** evet
- **c0_notu:** Sinyal 17:55'te bilinir (spot altin), giris 18:00-18:10; kullanicinin 'oncu hareket etmis' kalibina yakin. Ancak 2 bacakli (XU030 hedge zorunlu); 1 mn TL'de 1 XU030D kontrati iri kalir. Midas'ta uygulanamaz (VIOP).
- **tutma:** h1/h2/h3 k_dis: +25,9 (t2,4) / +51,8 (t3,2) / +54,4 (t2,3). Rehber pratik esik 1,0: h1 +19,5 (1,79) / h2 +36,4 (2,23) / h3 +30,2 (1,19)
- **yon:** iki yon; long +41,4 (237 islem) / short +27,9 (186) kurucu; denetim long +46,4 / short +23,6
- **n:** 405 (arastirma), 423 (pratik), ~54/yil
- **net_bps:** Arastirma h2 +42,9 (t2,54) curut; pratik kural 8+3 bps: +35,5 (t2,20) kurucu / +36,4 (2,23) denetim; hedge'siz +25,2 (t1,31)
- **t:** 2,2-2,54
- **is_oos:** IS +44,1 (1,82) / OOS +42,3 (1,89) arastirma; pratik IS +36,2 (1,66) / OOS +35,1 (1,59)
- **son_donem:** 2024-26 +69,7 (t2,44) arastirma / +54,0 (1,96) pratik; yillar: 2019 +35, 2020 +103, 2021 -48, 2022 +6, 2023 0, 2024 +47, 2025 +34, 2026 +89; fon krizi 2026-09/10 7 islem -82. Rejim: z katsayisi t 2019-20 3,4, 2021-22 0,0, 2023-24 0,9, 2025-26 1,7. En iyi 10 cikinca +20,7 (1,31) arastirma / +14,1 (0,94) pratik. Dunku altin etkisiz (t0,07-0,5). Izgara-duzeltmeli p 0,024; Bonferroni x32 0,77. Esik 1,2-1,3 civarinda cukur
- **maliyet:** 8+3 bps; 15+3: +28,5 (t1,77); tik: +29,9 (1,86); 1 birim ~11 bps
- **hukum:** KOSULLU / DUSUK; altin trend rejiminde, yalniz iki bacakla, kucuk boyut; hedge'siz yapma
- **guven:** DUSUK
- **kaynak:** 2026-11-04_kapanis_1-3gun/rehber/altin/REHBER_altin.md §1, §8, §9; notlar/k_dis.md ayrinti 3; notlar/k_dis-suruculer_curut.md Aday 3

### XU030 vadeli kapanis bazi sicramasi

- **sinif:** BIST-VIOP
- **tur:** mikroyapi
- **oncu:** BIST:XU030 (spot kapanis), BIST:XU030D1!
- **hedef:** BIST:XU030D1!
- **kural:** 18:10'da spot kapanis cikar. b = ln(XU030 vadeli son fiyat 18:15 / XU030 spot kapanis). Delta b = b - dunku b (ayni vade). z120 = Delta b / 120 gun std (sigma ~50 bps); |z|>1 -> ters yon: vadeli ucuz kapandiysa AL, pahali ise SAT. 18:15'e kadar gir, ertesi gun uzlasmada kapat (h1).
- **sinyal_saati:** 18:10 (spot kapanis) - 18:15 (vadeli)
- **giris_orijinal:** Vadeli son islem fiyati 18:15 (E1); uzlasma girisi (E0) daha dusuk
- **c0_uyumu:** kismen
- **c0_notu:** Sinyal spot kapanis (18:05-18:10) ve vadeli 18:15 son fiyatini gerektirir; kullanicinin 17:50-18:10 penceresinde tam bilinemez, 18:10-18:15'te ekran basinda olmak gerekir. Lead-lag degil mikroyapi; ertesi gun girisle kenar yok.
- **tutma:** h1 (h2-h3'te etki soner, t 2,1-2,5)
- **yon:** AL +28,6 (t2,9); SAT +18,7 (t1,2) (brut)
- **n:** 605-607, 65/yil
- **net_bps:** E1 brut +25,0 (t2,93)/+24,7 (t2,87); E0 +19,2 (t2,27); net (3-4,8 bps) ~+20
- **t:** 2,93
- **is_oos:** IS +22 (t2,1) / OOS +28 (t2,1) k_yurtici; PRATIK_LISTE IS +24 / OOS +25 (t1,85)
- **son_donem:** 2024-26 +17 (t1,1); egim 2017-19 -0,74 -> 2020-22 -0,34 -> 2023-26 -0,29 (zayifliyor); donemler 17-19 +38, 20-21 +9, 22-23 +42; en iyi 10 cikinca +12 (t1,6); E2 (1 gun gec) -1,8 (t-0,2); FDR ancak geciyor (q 0,03)
- **maliyet:** XU030 3 bps; net ~+14-20 bps
- **hukum:** UYGUN / ORTA (etki kuculuyor)
- **guven:** ORTA
- **kaynak:** 2026-11-04_kapanis_1-3gun/notlar/k_yurtici.md (e) XU030 vadelisi k8; notlar/k_yurtici-takvim_curut.md Aday 1; PRATIK_LISTE.md satir 15

### VIOP USDTRY 5 gunluk degisim -> THYAO

- **sinif:** BIST-VIOP
- **tur:** leadlag
- **oncu:** VIOP USDTRY uzlasmasi (TradingView'da dogrulanmis kod yok; Yahoo TRY=X zaman damgasi guvenilmez)
- **hedef:** BIST:THYAO1!
- **kural:** VIOP USDTRY uzlasmasinin 5 gunluk kumulatif degisimi; z = sinyal / 250 gun std; |z|>1 -> yon(z), h gun tut (h3 ana). Raw tek bacak (hedge'li surumde ~%2 plasebo).
- **sinyal_saati:** Uzlasma penceresi (~18:00-18:10); sinyal girisle ayni anda
- **giris_orijinal:** t gunu VIOP uzlasmasi
- **c0_uyumu:** kismen
- **c0_notu:** Sinyal VIOP USDTRY uzlasmasi (18:00-18:10) ile ayni anda olusur; TradingView'da uygun spot vekil yok.
- **tutma:** h1/h2/h3 k_dis: +26,6 (t2,6) / +55,4 (t3,1) / +96,3 (t3,9); h3 15 bps +89,3
- **yon:** 'kur yukseldi -> al' brut +187; 'kur dustu -> sat' +55; uzun sinyaller +150 (t3,3, n106)
- **n:** 282 (31/yil) curut
- **net_bps:** h3 raw net8 +99,3 (t3,79) curut; carry cikarilmis +96,5 (t3,0)
- **t:** 3,79
- **is_oos:** IS +87,6 (2,19) / OOS +112,1 (3,37) curut; k_dis h3 IS +88,4 (2,5) / OOS +105,3 (3,0)
- **son_donem:** 2024-26 +73,7 (t2,12) ama drift duzeltmeli +28,7 (t0,82); carry cikarilmis 2024-26 +66 (t1,27, n49); 2024-26'da sinyallerin ~%0-8'i uzun: fiilen surekli THYAO short; spot kurla (Yahoo t-1, saatlik 15:00) t ~0-1,6, saatlik TRY=X -71 (t-2,27); kriz pencereleri cikarilinca +54,9 (t2,2); en iyi 10 cikinca +59,3 (t2,5)
- **maliyet:** 8 / 15 bps; THYAO 5,9 bps
- **hukum:** KOSULLU / DUSUK: kazancin kaynagi carry/drift; yalniz TL soku donemlerinde
- **guven:** DUSUK (curut); ORTA (k_dis); COK DUSUK (PRATIK_LISTE)
- **kaynak:** 2026-11-04_kapanis_1-3gun/notlar/k_dis.md ayrinti 4; notlar/k_dis-suruculer_curut.md Aday 4; PRATIK_LISTE.md satir 25

### Avrupa savunma (RHM, BAE, LDO, SAAB) 15:00 UTC -> ASELS

- **sinif:** BIST-VIOP
- **tur:** leadlag
- **oncu:** Avrupa savunma sepeti (RHM, BAE, LDO, SAAB; TV kodlari notlarda verilmemis)
- **hedef:** BIST:ASELS1!
- **kural:** 15:00 UTC'ye kadarki sepet artigi; z = sinyal/120 saat std; |z|>1 -> yon(z), h2 tut.
- **sinyal_saati:** 15:00 UTC = 18:00 TSI
- **giris_orijinal:** t gunu VIOP uzlasmasi
- **c0_uyumu:** kismen
- **c0_notu:** Saatlik sinyal 18:00'de; tek rejime bagli.
- **tutma:** saatlik raw h2 +93,8 (t2,85) k_dis; curut +62,8 (t1,74); h3 +100 (t2,4)
- **yon:** belirtilmemis
- **n:** 120, 48/yil (2024-04+)
- **net_bps:** curut h2 raw +62,8; hedge'li +32 (t1,0)
- **t:** 1,74
- **is_oos:** Yarilar +76 / +52
- **son_donem:** Yillar 2024 0, 2025 +166, 2026 +3 (tek yil); en iyi 10 cikinca -2 (t-0,06); izgara-duzeltmeli p 0,19; gunluk vekil 2019-21 negatif
- **maliyet:** 8/15 bps; ASELS 6,1 bps
- **hukum:** UYGUN DEGIL (curut)
- **guven:** DUSUK
- **kaynak:** 2026-11-04_kapanis_1-3gun/notlar/k_dis-suruculer_curut.md Aday 5; notlar/k_dis.md ayrinti 5

### Kredi notu kademe karari -> ters pozisyon

- **sinif:** BIST-VIOP
- **tur:** olay
- **oncu:** Kredi notu karari (S&P/Moody's/Fitch)
- **hedef:** BIST:XU030D1!
- **kural:** Tepki gununun F_XU030 uzlasmasinda kararin tersine gir, 2 gun tut.
- **sinyal_saati:** Tepki gunu
- **giris_orijinal:** Tepki gunu uzlasmasi
- **c0_uyumu:** evet
- **c0_notu:** Olay gunu kapanis; yilda 1-2 firsat.
- **tutma:** h1 +61 / h2 +156 (t3,0, bootstrap p0,016) / h3 +180 k_dis
- **yon:** dususlerde +190 (n10), yukseltmelerde +99 (n6)
- **n:** 16, yilda 1-2
- **net_bps:** h2 +142 (t2,93) curut; net15 +135
- **t:** 2,93-3,0
- **is_oos:** 2017-21 +160 (n7) / 2022-26 +152 (n9)
- **son_donem:** Son iki karar kayip (S&P 2024-11 -217, Moody's 2025-07 -53); 2024-26 n=6 +99; en iyi 3 cikinca +94 (t1,87); kaba Bonferroni p~0,14; kademe karari 2026'da yok; tepki gununde karar yonunde hareket yalniz %31; 02.11 RAPOR: acilis girisli +208 bps/olay (n20), 2000-13 ve diger ulkelerde calismiyor
- **maliyet:** 3 bps XU030
- **hukum:** KOSULLU / DUSUK
- **guven:** DUSUK
- **kaynak:** 2026-11-04_kapanis_1-3gun/notlar/k_dis.md ayrinti 6; notlar/k_dis-suruculer_curut.md Aday 6; PRATIK_LISTE.md satir 23

### TCELL-TTKOM goreli donus

- **sinif:** BIST-VIOP
- **tur:** ortalamaya-donus
- **oncu:** BIST:TTKOM (cift)
- **hedef:** BIST:TCELL1! / BIST:TTKOM1!
- **kural:** Z20 > 2 (goreli getiri 20 gunluk z), 2-3 gun tut.
- **sinyal_saati:** Kapanis
- **giris_orijinal:** t gunu uzlasmasi (E0)
- **c0_uyumu:** evet
- **c0_notu:** Kapanista bilinir.
- **tutma:** h2 +32 (t2,8), h3 +41 (t2,85) k_yurtici; E2 h2 +27 (t2,3)
- **yon:** belirtilmemis
- **n:** belirtilmemis
- **net_bps:** curut: vadeli sinyalle E0 h3 +39,5 (t2,67), E2 +27,3 (t1,67); spot sinyal E0 +34,7 (t2,25), E2 +23,5 (t1,44)
- **t:** 2,67
- **is_oos:** IS +54 / OOS +30 (t1,5)
- **son_donem:** Getiri 2020-21'e yigili (+93..+120); 2017-19 ve 2022-23 ~0 / negatif; log-fiyat yayilimi ~0; q 0,17-0,24
- **maliyet:** 8/15 bps
- **hukum:** UYGUN DEGIL / DUSUK (curut)
- **guven:** DUSUK-ORTA (k_yurtici) / DUSUK (curut)
- **kaynak:** 2026-11-04_kapanis_1-3gun/notlar/k_yurtici.md ozet tablo #4; notlar/k_yurtici-takvim_curut.md Aday 4

### KCHOL NAV sapmasi (holding iskontosu)

- **sinif:** BIST-VIOP
- **tur:** ortalamaya-donus
- **oncu:** Istirak NAV sepeti (KCHOL'un bagli ortakliklari)
- **hedef:** BIST:KCHOL1! - beta*BIST:XU030D1!
- **kural:** zdev = (D - MA60(D))/std250, D = log KCHOL - log NAV sepeti; zdev>0,5 -> KCHOL'u XU030'a hedge'li al, h3.
- **sinyal_saati:** Kapanis
- **giris_orijinal:** t gunu uzlasmasi
- **c0_uyumu:** evet
- **c0_notu:** 'Holding NAV'sinin gerisinde kaldi -> al' kalibina en yakin yetisme testi; kenar maliyetle yok oluyor.
- **tutma:** h3 +14,8 (t3,3) VIOP; spot 2014+ +17,3 (t5,3)
- **yon:** belirtilmemis
- **n:** sinyal gunlerin %56'sinda acik
- **net_bps:** brut h3 +14,8 / +11,4 (curut); net ~+7 (8 bps) / ~0 (15 bps); curut E0 net ~+5, E2 ~+2
- **t:** 3,3 (k_yurtici) / 2,36 (curut)
- **is_oos:** IS 2017-21 +1,9 (t0,3) / OOS +29,9 (t4,2)
- **son_donem:** 2017-21 -1 (t-0,2); spot da 2017-21 ~0; 02.11 RAPOR t 1,0-1,5
- **maliyet:** KCHOL 6,7 + XU030 3 bps
- **hukum:** UYGUN DEGIL / DUSUK (tek basina; net kucuk)
- **guven:** DUSUK-ORTA / DUSUK
- **kaynak:** 2026-11-04_kapanis_1-3gun/notlar/k_yurtici.md (g); notlar/k_yurtici-takvim_curut.md Aday 5

### Ay donumu (ayin son gunu al, ilk gun sat)

- **sinif:** BIST-VIOP
- **tur:** takvim
- **oncu:** yok (takvim)
- **hedef:** BIST:XU030D1!
- **kural:** Ayin son VIOP gunu uzlasmasinda AL, ertesi gun uzlasmasinda SAT.
- **sinyal_saati:** Takvim
- **giris_orijinal:** Ayin son gunu uzlasmasi
- **c0_uyumu:** evet
- **c0_notu:** Takvim sinyali, lead-lag degil.
- **tutma:** h1 +44,2 (t2,42)
- **yon:** yalniz long
- **n:** 115
- **net_bps:** E0 h1 brut +44,2; E2 +8
- **t:** 2,42
- **is_oos:** 2017-19 -7, 2020-21 +82, 2022-23 +104
- **son_donem:** 2024-26 +26 (t0,8); simetrik budama +37 (3,1) ama en iyi 10 cikinca +7 (t0,5); FDR q 0,052 gecmiyor; spot XU100 2005-20 +12 (t0,9); 2021-22 agirlikli
- **maliyet:** XU030 3 bps
- **hukum:** KOSULLU / DUSUK
- **guven:** DUSUK
- **kaynak:** 2026-11-04_kapanis_1-3gun/notlar/k_yurtici-takvim_curut.md Aday 7; notlar/k_yurtici.md (d)

### Pay vadelisi kapanis baz sapmasi (kesitsel)

- **sinif:** BIST-VIOP
- **tur:** mikroyapi
- **oncu:** BIST:<KOD> spot kapanis muzayedesi
- **hedef:** BIST:<KOD>1! (pay vadelileri)
- **kural:** Vadeli kapanis spot muzayedesine gore pahali/ucuz ise ters yon; kesitsel ust/alt %20 L/S ya da hisse bazinda |z|>1,5 (anom_close_dev / 120g std).
- **sinyal_saati:** 18:10 (pay vadelisi ve spot muzayede birlikte biter)
- **giris_orijinal:** E1 vadeli son islem fiyati
- **c0_uyumu:** hayir
- **c0_notu:** Kapanis muzayedesinde ayni anda; kullanici penceresinde yakalanamaz.
- **tutma:** h1
- **yon:** belirtilmemis
- **n:** belirtilmemis
- **net_bps:** Kesitsel E1 h1 +23-25 (t17-18); hacimce ilk 15 + 2022-09 sonrasi +16,5, net15 +1,5; curut A sinifi E1 h1 +11,7, net ~+5/-1; tek bacak curutte +12,5 (t0,95) (taramada +39,6, t2,6)
- **t:** 3,8 (curut E1)
- **is_oos:** belirtilmemis
- **son_donem:** E2 (ertesi gun giris) +0,3...+7 / ~0: etki yalniz kapanis aninda
- **maliyet:** net15 +1,5
- **hukum:** Strateji olarak UYGUN DEGIL; yalniz yurutme ipucu (~5-10 bps)
- **guven:** Istatistik YUKSEK / islem DUSUK
- **kaynak:** 2026-11-04_kapanis_1-3gun/notlar/k_yurtici.md (e); notlar/k_yurtici-takvim_curut.md Aday 3

## Elenenler

- **Gece suruculeri (ES, Brent, TKC, TUR, gece altini) -> acilis gap'i:** Bilgi BIST kapanisindan sonra geliyor ve ertesi acilista fiyatlaniyor; acilistan sonra kalinti ~0 (612 gun ici testte FDR 0). Kapanis-kapanis yatirimci hareketi zaten yasamis oluyor. _( PRATIK_LISTE.md satir 32; 2026-11-02_viop_leadlag/RAPOR.md Zaman bolumu )_
- **Sektor emsalleri gun ici oncullugu (genel anomali, havuzlanmis):** t 7,1 gercek ama brut 3-11 bps/pozisyon < 8-15 bps maliyet; yansima t gunu icinde bitiyor, ertesi kapanisa kalan 8-26 bps, t<=1,5 (TUPRS ve EREGL haric). _( PRATIK_LISTE.md satir 33; RAPOR.md Gercek oncuuluk bolumu )_
- **Havayolu sepetleri -> THYAO/PGSUS/TAVHL:** Saatlik raw h2 THYAO +55,6 (t2,2), PGSUS +63,1 (t2,3); gunluk vekillerde net 8 bps +5...+20 (t<1,5), hedge'li ~0, 2026 negatif; etki t gunu icinde tukeniyor. _( notlar/k_dis.md Olumsuz bulgular; k_dis-suruculer_curut.md UYGUN DEGIL listesi )_
- **TKC -> TCELL:** Kapanis-kapanis isaret ters: DF hedge'li h2 -37,4 bps (t-3,0); TCELL'in kendi donusu, P katsayisi ~0; saatlik parite +8 bps (t0,5). _( notlar/k_dis.md Olumsuz bulgular )_
- **Kuresel bira -> AEFES:** DF hedge'li h1 +18,3 (t1,5), saatlik negatif; BIRA sepeti hedef disi PGSUS'u da 'ongoruyor' (mekanizma yok). _( notlar/k_dis.md Olumsuz bulgular )_
- **Avrupa/ABD/Japon celigi -> EREGL/KRDMD/BRSAN:** t ~0-1,9; Japon celigi EREGL'de ters; ABD celigi->BRSAN saatlik t 1,6-2,1 ama kisa orneklem. (FMG/BHP->EREGL ayri satirda.) _( notlar/k_dis.md Olumsuz bulgular )_
- **Altin madencileri (GDX, NEM) -> TRALT/TRMET:** VIOP altininin kendisinden zayif; FDR yok. _( notlar/k_dis.md; k_dis-suruculer_curut.md )_
- **Cok gunluk ES/EEM/Brent/COMEX altin/TUR/DIBS -> 47 hisse + F_XU030:** 50.688 testte surucuye ozgu FDR'den gecen yok (VIOP USDTRY haric); TUR t-1 -> XU030 h1-h3 t 2,0-2,5, FDR yok. _( notlar/k_dis.md Olumsuz bulgular (b) )_
- **Gunluk hisse->hisse ve endeks->hisse oncullugu:** 157 bin + 12,7 bin test (+1.482 saatlik), FDR'den gecen 0; liderlik siralamasi yildan yila korunmuyor. _( 2026-11-02_viop_leadlag/RAPOR.md Yurt ici baglar )_
- **Genel cift donusleri (13 cift) ve 'emsal - hisse ayrismasi':** Havuzda donus yok; VIOP E0 h1 -3...-9 bps (t -1,3...-3,4); plasebo evreninde (2.162 cift) E0 -16, E2 -9 bps. Ayrisma (D) tek degiskenle calismiyor: hissenin kendi artigi emsal etkisini goturuyor; XU030'da div katsayisi kisa vadeli momentum (t -1,4...-2,1). _( notlar/k_yurtici.md (f); k_yurtici-takvim_curut.md UYGUN DEGIL; k_dis.md Olumsuz bulgular )_
- **Banka ciftleri (AKBNK-GARAN, YKBNK-ISCTR, VAKBN-HALKB):** E0 h1 donus kaybettiriyor (-18...-21, t-3,5); yalniz E2 ile h5'te pozitif (YKBNK-ISCTR REV3>2 +78, t2,95; AKBNK-GARAN Z60>1,5 +41, t3,0): 1-3 gun disinda. _( notlar/k_yurtici.md (f) )_
- **THYAO-PGSUS goreli donus; TRALT-TRMET goreli donus:** THYAO-PGSUS Z20>1,5 h2 -25 (t-3,3) donus yonunde, sonuyor; TRALT-TRMET REV3>2 h3 -88 (t-3,75), 0/8 yil: donus degil momentum (Koza satirina bakin). _( notlar/k_yurtici.md (f) )_
- **SAHOL/diger holding-banka ciftleri (SAHOL/YKBNK, /GARAN, /ISCTR, KCHOL/*, AKBNK/YKBNK):** Ayni kural VIOP 2021-26: SAHOL/YKBNK +29 (t0,99), SAHOL/GARAN +17 (t0,56), SAHOL/ISCTR +5, KCHOL/SAHOL -26, AKBNK/YKBNK -42; yalniz SAHOL/AKBNK anlamli (secim yanliligi; 24 ana/yavru ciftinden 1'i). _( notlar/k_sahol_b.md Kontrol 6 )_
- **Tavan/taban sonrasi:** Olay gunlerinin %83-86'sinda VIOP da limitte kilitli; dolan yon kaybettiriyor (tavanda sat h1 -99, tabanda al -252 bps). _( notlar/k_yurtici.md (b); PRATIK_LISTE.md satir 34 )_
- **Hisse kapanis muzayedesi donusu:** VIOP uzlasmasi muzayede hareketinin ~%50'sini izliyor, fark ertesi gun ayni yonde kapaniyor; hisseye ozgu CA_id ~0; donus yalniz spotta (acigi satis gerekir). _( notlar/k_yurtici.md (c) )_
- **Temettu oncesi yukselis:** Yalniz spotta (VIOP47 +74, t2,9); VIOP uzlasmasi +5 (t0,15) / yuksek verimde +15 (t0,3): vadeli temettuyu bazda fiyatliyor. _( notlar/k_yurtici.md (a) )_
- **FOMC / NFP / CPI gunleri risk azaltma; akşam seansi hareketi:** 1-3 gunluk std orani 0,73-1,19, bootstrap p 0,09-0,92; yarim pozisyon getiri kaybi > risk azalmasi. Akşam ES hareketi ertesi getiriyi %1,5-2,8 aciklar, giris alfasi yok (t<=1,1). _( notlar/k_dis.md (d)(e); k_dis-suruculer_curut.md 7-8 )_
- **Koza TERS kural (TRALT artigi, TRALT1! - beta*TRMET1!):** Kilitli P0L'de brut +30,4 (t1,83), en iyi 10 cikinca -4,7, gecikmeli giriste kayboluyor. _( rehber/koza/REHBER_koza.md §9.3 )_
- **Bayram/tatil oncesi, BIST30/50 donem degisikligi:** Tutarli etki yok; donem degisikligi n=18, fade yonu -117...-325 ama fon krizi iceriyor (COK DUSUK). _( notlar/k_yurtici.md (d) )_
- **Kapanis muzayedesi/gun ici XU030 ogleden sonra dususu ve acilis gap geri donusu (02.11 RAPOR):** Gun ici (11:00->kapanis) mevsimsellik, lead-lag degil, kapanis-kapanis profilinde yok; gap geri donusu likit yarida ~0. _( 2026-11-02_viop_leadlag/RAPOR.md Islenebilir adaylar tablosu )_

## Çelişkiler

- PRATIK_LISTE.md (satir 69 'Dort adayin dordu de son donemde zayifliyor') ile k_sahol_a/b ve curut dosyalari celisiyor: SAHOL/AKBNK A 2024-26 +81,9 (t2,75), 2026 +137 (t4,60), son 12 ay +109 (t3,23) (k_sahol_a/b); altin->TRALT 2024-26 +69,7 (t2,44) ve FMG/BHP->EREGL 2024-26 +59,2 (t2,21) (curut). Zayiflama yalniz TUPRS (+26, t1,0 / +30,5, t0,90) ve Koza (+21,7, t0,93; 2026 net -29) icin dogru. (Not: PRATIK_LISTE tablosu 'dortluyu' XU030 baz, SAHOL, Koza, TUPRS olarak sayiyor; SAHOL'de 2024-26 ayri soylenmemis.)
- SAHOL/AKBNK: k_sahol_a 'ayni aksam uygulamak gerekiyor' (ertesi gun uzlasmasiyla IS spot A 23 bps, t1,04; OOS VIOP 94, t3,33) der; k_sahol_b ayni uyariyi 'spot vekili artefakti' sayar: ertesi gun uzlasmasi A +82,7 (t2,96), 12.2023+ +124,8 (t3,53), 'ikisi de calisiyor'. Gec girisin etkisi iki not arasinda tutarsiz.
- SAHOL/AKBNK sayilari: k_sahol_a OOS 108 islem +63,7 (t3,12) / k_sahol_b 106 islem +69,7 (t3,35); PRATIK_LISTE 'net +64-70' veriyor ama 'gercekci +30-50' (k_sahol_b: 'yarisi'). Ayrica A + en cok 3 gun: OOS +26 (t1,28) (a) / +33,5 (t1,65) (b); C0'in 1-3 gunu ile kuralin kuyrugu (%10 islem >10 gun) uyusmuyor.
- TUPRS h3: k_dis +55,3 (t2,7); curut bagimsiz hesapla +41,6 (t1,93) ve 'tarayicinin h3 rakami abartili' der; h2 iki yerde tutarli (+41,8 / +42,0). PRATIK_LISTE'nin 't uzlasmasinda gir, t+2 cik, net +42, t2,7' blok bazlidir (492 islem); rehber pozisyon bazli +49,2 (t2,53, 411 islem) ve uzatma/cevirme icerir (en uzun 8 gun) - 'sabit 2 gun' degildir.
- Koza: PRATIK_LISTE '2 gun tutulur, h2 +45 (t4,05)' der; REHBER_koza ayni +44,6 (t4,05) rakamini orgusen sinyal gunleri icin verir ama uygulanabilir pratik kural uzatmalidir (6 gune kadar). Uzatmasiz sabit h2 kilitli: brut +25,2, net15+tik +3,4; kenarin cogu 'surerse uzat' kuralindan. k_yurtici '7/8 yil' ve E2 '8/8 yil' der; rehber 2026 brut -11, net -29 verir.
- Altin->TRALT guven etiketi: k_dis ORTA/UYGUN, curut KOSULLU/DUSUK, PRATIK_LISTE DUSUK, rehber DUSUK. h2 hedge'li net: k_dis +51,8 (t3,2) > curut +42,9 (t2,54) > rehber pratik +35,5 (t2,20) / +36,4 (t2,23). Rehber yilda 2021 -48, PRATIK_LISTE 'yalniz altin rallisi donemlerinde' diyor (2019-20 ve 2025-26): 2023-24 hem 0 hem pozitif (+47 2024).
- EREGL<-FMG/BHP: k_dis ORTA/UYGUN, curut DUSUK; OOS DF h3 hedge'li +22,3 (t1,0) (k_dis) / +19,7 (t0,92) (curut) ve 02.11 RAPOR 'artiklastirilinca OOS net 8-18 bps, hedge'li negatif'; IS ise +73,6-80,7 (t3,5-3,7). PRATIK_LISTE bunu 'OOS t 0,9; 2022-23'te negatif' diye ozetliyor (k_dis'te OOS t 1,0).
- 02.11 RAPOR'unda dogrulanmis gunluk gecikmeli (t -> t+1 kapanis) oncu-hedef cifti yok: islenebilir adaylarin hepsi gun ici (acilis->kapanis) ya da gap; SAHOL/AKBNK 'ertesi acilista' giris, VIOP t 2,3-2,9. 04.11 dosyalarinda ayni adaylar (rafineri->TUPRS, FMG->EREGL, altin->TRALT) kapanis-kapanis olarak yeniden test edilince biri kalinti gosteriyor, havayolu/TKC/celik dusuyor. RAPOR TUPRS 'gun ici, hedge'li t 4,3-5,3, tek bacak net 8 bps t 1,7' ile 04.11 'kapanis-kapanis h2 net 8 bps t 2,7' farkli kurgulardir (karsilastirilamaz).
- PRATIK_LISTE satir 15 'XU030 baz sicramasi: Yilda ~65 islem; IS +24, OOS +25 (t1,85)' ile k_yurtici 'IS +22 (t2,1) / OOS +28 (t2,1)' farkli; ayrica PRATIK_LISTE UYGUN diyor ama giris 18:10-18:15, C0 penceresiyle ortusmuyor.
- Kredi notu: 02.11 RAPOR acilis girisli +208 bps/olay (n=20) / 04.11 uzlasma girisli h2 +142-156 (n=16); k_dis 'kademe + gorunum n=25 +115 (t3,0)' ile curut n=16 farkli olay tanimi; ikisi de 'DUSUK'.

## Açık kalanlar

- Koza (TRMET/TRALT) ve EREGL (FMG/BHP) icin long ve short tarafin ayri n/bps sayilari okunan notlarda bulunamadi (yalniz XU030 baz, TUPRS, altin ve SAHOL icin var). res/*.csv ve islemler_P0L.csv acilmadi.
- EREGL<-FMG/BHP kuralinin hedge oranina dair sayisal beta ve ASX200 beta penceresi yazili degil (yalniz 'beta gecmis 250 gun'); ayri rehber klasoru yok.
- Rehber/koza, tuprs ve altin altinda .pine ve json dosyalari ile denetim/kod acilmadi; Pine'larin hicbiri TradingView'da derlenmedi (rehberler belirtiyor).
- TUPRS icin h1/h2/h3 ayrimi 2024-26 alt donemde yalniz rehberin duyarlilik tablosundan (esik 1: h1 +14,3 t0,80; h2 +30,5 t0,90; h3 +30,3 t0,74) alindi; k_dis'te alt donem h-kirilimi yok.
- Avrupa savunma sepeti ve USDTRY icin TradingView kodlari notlarda net verilmemis (savunma uyeleri RHM/BAE/LDO/SAAB isim olarak var).
- 02.11 RAPOR'daki dogrulama/ ve hukumler.json dosyalari (RAPOR'da referans verilen) okunmadi; 'gunluk gecikmeli dogrulanmis cift yok' sonucu RAPOR.md gövdesine dayaniyor.
- Midas/ABD hisse-ETF tarafi bu gorevde kapsam disi; yalniz VIOP pay vadelileri incelendi.
