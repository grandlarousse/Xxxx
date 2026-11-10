# K2 bagimsiz saglamlik hesabi (kod2/k2.py; tum bps; fazla = yil-eslestirilmis; net c1 = 5 (T1), 10 (T2-T7), 13 (T8); c2 = 44)
Tum sonuclar csv'de: K2_tum_sonuc.csv, yil_*.csv (T1,T2,T5,T6,T7,T8 yil yil), T3_plasebo.csv. 'netfazla' = fazla - c1. Kisa taraf: P&L isareti ters; fazla = ayni yilin 'surekli kisa' P&L'ine gore.

| test | n | brut | fazla(t) | net10 veya c1 (t) | netfazla c1 | net44 (t) | IS fazla(t) | OOS | SON | +yil |
|---|--:|--:|--|--|--:|--|--|--|--|--|
| T1 XU030 k1.0 h1 | 598 | 22 | 13(2.2) | 17(2.7) | 8 | 17(2.7) | 8(1.2) | 23(1.9) | 27(2.0) | 13/16 |
| T1 XU030 k1.0 h2 | 519 | 31 | 15(1.5) | 26(2.6) | 10 | 26(2.6) | 7(0.6) | 32(1.5) | 45(1.9) | 10/16 |
| T1 XU030 k1.0 h3 | 458 | 54 | 30(2.3) | 49(3.7) | 25 | 49(3.7) | 22(1.4) | 48(1.8) | 47(1.5) | 13/16 |
| T1 XU030 k1.5 h2 | 247 | 40 | 23(1.5) | 35(2.2) | 18 | 35(2.2) | 9(0.6) | 49(1.5) | 60(2.2) | 12/16 |
| T1 XU100 k1.0 h3 | 458 | 56 | 33(2.6) | 51(4.1) | 28 | 51(4.1) | 23(1.6) | 54(2.1) | 56(1.9) | 13/16 |
| T1 AYNA kisa XU030 z<=-1.0 h2 | 445 | -2 | 9(0.7) | -7(-0.5) | 4 | -7(-0.5) | 16(1.2) | -10(-0.4) | -3(-0.1) | 8/16 |
| T1 AYNA kisa XU030 z<=-1.0 h3 | 387 | -20 | -4(-0.2) | -25(-1.6) | -9 | -25(-1.6) | 3(0.2) | -21(-0.7) | 16(0.4) | 8/16 |
| T2 sepet k1.0 h2 | 518 | 41 | 19(1.9) | 31(3.1) | 9 | -3(-0.3) | 15(1.4) | 28(1.3) | 42(1.7) | 11/16 |
| T2 sepet-XU030 k1.0 h2 | 518 | 10 | 5(2.0) | 0(0.2) | -5 | -34(-13.7) | 9(3.3) | -4(-0.8) | -3(-0.5) | 9/16 |
| T2 sepet k1.0 h3 | 458 | 60 | 28(2.1) | 50(3.8) | 18 | 16(1.2) | 24(1.6) | 38(1.4) | 36(1.1) | 12/16 |
| T2 sepet-XU030 k1.0 h3 | 458 | 8 | -0(-0.0) | -2(-0.6) | -10 | -36(-10.7) | 2(0.7) | -5(-0.7) | -3(-0.4) | 9/16 |
| T2 sepet k1.5 h3 | 228 | 61 | 29(1.4) | 51(2.5) | 19 | 17(0.8) | 19(0.8) | 48(1.2) | 43(1.3) | 14/16 |
| T2 sepet-XU030 k1.5 h3 | 228 | 10 | 2(0.4) | -0(-0.1) | -8 | -34(-6.6) | 11(2.2) | -16(-1.3) | 4(0.4) | 10/16 |
| T4 KCHOL ham k1.0 h3 | 456 | 78 | 46(2.5) | 68(3.7) | 36 | 34(1.9) | 50(2.5) | 38(1.0) | 45(1.0) | 11/16 |
| T4 KCHOL ARTIK k1.0 h3 | 456 | 22 | 17(1.6) | 12(1.1) | 7 | -22(-2.1) | 31(2.7) | -14(-0.6) | -4(-0.1) | 12/16 |
| T4 KCHOL ham k1.5 h2 | 245 | 86 | 64(3.1) | 76(3.7) | 54 | 42(2.1) | 59(2.5) | 74(1.8) | 97(2.5) | 13/16 |
| T4 KCHOL ARTIK k1.5 h2 | 245 | 45 | 41(3.4) | 35(2.8) | 31 | 1(0.0) | 52(3.9) | 20(0.8) | 32(1.2) | 14/16 |
| T4 TUPRS ham k1.0 h3 | 458 | 81 | 40(2.2) | 71(3.9) | 30 | 37(2.0) | 26(1.3) | 69(1.9) | 46(1.1) | 14/16 |
| T4 TUPRS ARTIK k1.0 h3 | 458 | 37 | 17(1.2) | 27(1.9) | 7 | -7(-0.5) | 11(0.7) | 30(1.1) | 13(0.4) | 9/16 |
| T4 ASELS ham k1.0 h3 | 457 | 88 | 36(1.8) | 78(3.8) | 26 | 44(2.1) | 28(1.3) | 55(1.2) | 20(0.3) | 12/16 |
| T4 ASELS ARTIK k1.0 h3 | 457 | 40 | 9(0.5) | 30(1.7) | -1 | -4(-0.2) | 8(0.4) | 9(0.2) | -22(-0.4) | 10/16 |
| T4 EREGL ham k1.0 h3 | 458 | 71 | 35(2.0) | 61(3.4) | 25 | 27(1.5) | 23(1.1) | 63(1.7) | 43(0.9) | 11/16 |
| T4 EREGL ARTIK k1.0 h3 | 458 | 25 | 12(0.8) | 15(1.1) | 2 | -19(-1.3) | 6(0.4) | 24(0.8) | 9(0.2) | 7/16 |
| T5 KBE z>=1.0 -> AKBNK h2 | 488 | 51 | 40(2.6) | 41(2.6) | 30 | 7(0.4) | 41(2.5) | 37(1.0) | 57(1.3) | 13/16 |
| T5 AKBNK k1.0 h2 | XU030z<1 | 395 | 53 | 43(2.5) | 43(2.4) | 33 | 9(0.5) | 40(2.1) | 53(1.3) | 67(1.4) | 13/16 |
| T5 KBE z>=1.5 -> AKBNK h1 | 248 | 36 | 29(1.8) | 26(1.7) | 19 | -8(-0.5) | 15(0.8) | 58(2.0) | 101(3.1) | 10/16 |
| T5 KBE z>=1.5 -> AKBNK h2 | 231 | 79 | 64(2.7) | 69(2.9) | 54 | 35(1.5) | 68(2.5) | 56(1.1) | 115(1.8) | 11/16 |
| T5 AKBNK k1.5 h2 | XU030z<1 | 185 | 70 | 56(2.0) | 60(2.1) | 46 | 26(0.9) | 56(1.8) | 55(0.9) | 116(1.5) | 9/16 |
| T5 AKBNK k1.5 h2 | XU030z>=1 | 46 | 114 | 99(2.3) | 104(2.4) | 89 | 70(1.6) | 116(2.1) | 59(0.8) | 109(1.1) | 8/11 |
| T5 KBE z>=1.5 -> XU030 h2 | 232 | 48 | 32(2.0) | 38(2.4) | 22 | 4(0.2) | 31(1.8) | 35(1.0) | 62(1.5) | 9/16 |
| T5 KBE z>=1.5 -> BANKA4 h2 | 231 | 67 | 50(2.2) | 57(2.5) | 40 | 23(1.0) | 49(2.0) | 53(1.1) | 111(1.9) | 10/16 |
| T5 KBE z>=1.5 -> AKBNK h3 | 211 | 68 | 46(1.4) | 58(1.8) | 36 | 24(0.8) | 49(1.4) | 41(0.6) | 104(1.1) | 12/16 |
| T6 TUPRS UZUN z>1 h2 | 390 | 64 | 33(2.1) | 54(3.4) | 23 | 20(1.3) | 29(1.6) | 39(1.4) | 25(0.8) | 10/13 |
| T6 TUPRS KISA z<-1 h2 | 371 | -3 | 23(1.4) | -13(-0.8) | 13 | -47(-2.9) | 2(0.1) | 59(1.9) | 19(0.6) | 8/13 |
| T6 uzun h2 | (a) TUPRS_t<=0 | 173 | 33 | 1(0.1) | 23(1.0) | -9 | -11(-0.4) | 0(0.0) | 3(0.1) | -27(-0.6) | 5/13 |
| T6 uzun h2 | (b) TUPRS_t>0 | 217 | 89 | 58(2.7) | 79(3.6) | 48 | 45(2.1) | 52(2.2) | 68(1.7) | 64(1.4) | 8/13 |
| T6 uzun h2 | (c) goreli<=medyan | 195 | 57 | 26(1.2) | 47(2.2) | 16 | 13(0.6) | 42(2.0) | 0(0.0) | -40(-0.8) | 9/13 |
| T6 uzun h2 | (c) goreli>medyan | 195 | 72 | 40(1.7) | 62(2.5) | 30 | 28(1.1) | 14(0.5) | 75(2.0) | 80(1.8) | 10/13 |
| T6 TUPRS UZUN z>1 h3 | 351 | 89 | 42(2.1) | 79(3.8) | 32 | 45(2.2) | 42(1.8) | 43(1.1) | 32(0.7) | 10/13 |
| T6 TUPRS KISA z<-1 h3 | 332 | 3 | 41(2.0) | -7(-0.3) | 31 | -41(-2.0) | 17(0.8) | 85(2.0) | 43(1.0) | 8/13 |
| T6 uzun h3 | (a) TUPRS_t<=0 | 156 | 58 | 11(0.4) | 48(1.6) | 1 | 14(0.5) | 8(0.2) | 16(0.3) | -23(-0.4) | 7/13 |
| T6 uzun h3 | (b) TUPRS_t>0 | 195 | 113 | 67(2.3) | 103(3.6) | 57 | 69(2.4) | 68(2.2) | 64(1.2) | 75(1.2) | 9/13 |
| T6 uzun h3 | (c) goreli<=medyan | 176 | 99 | 54(2.0) | 89(3.3) | 44 | 55(2.0) | 70(2.4) | 27(0.5) | 3(0.0) | 10/13 |
| T6 uzun h3 | (c) goreli>medyan | 175 | 78 | 30(1.0) | 68(2.2) | 20 | 34(1.1) | 11(0.3) | 57(1.1) | 59(1.0) | 8/13 |
| T7 RYGYO z>1 -> RYSAS h1 | 540 | 73 | 54(3.1) | 63(3.6) | 44 | 29(1.6) | 33(1.5) | 89(3.0) | 119(3.0) | 11/16 |
| T7 1 gun gec giris | 539 | 36 | 17(1.0) | 26(1.5) | 7 | -8(-0.5) | 12(0.6) | 25(0.8) | 40(1.0) | 10/16 |
| T8 QQQ h2 tum | 323 | 49 | 38(3.0) | 36(2.9) | 25 | 36(2.9) | 26(1.9) | 61(2.4) | 52(1.8) | 14/16 |
| T8 QQQ h2 2016+ | 218 | 66 | 54(3.5) | 53(3.5) | 41 | 53(3.5) | 48(2.6) | 61(2.4) | 52(1.8) | 11/11 |
| T8 QQQ h2 2011-15 | 105 | 14 | 3(0.1) | 1(0.0) | -10 | 1(0.0) | 3(0.1) | -(-) | -(-) | 3/5 |
| T8 QQQ h3 tum | 304 | 68 | 50(3.4) | 55(3.7) | 37 | 55(3.7) | 41(2.5) | 70(2.3) | 61(1.6) | 15/16 |
| T8 QQQ h3 2016+ | 206 | 81 | 62(3.4) | 68(3.7) | 49 | 68(3.7) | 56(2.6) | 70(2.3) | 61(1.6) | 11/11 |
| T8 QQQ h3 2011-15 | 98 | 41 | 24(1.0) | 28(1.1) | 11 | 28(1.1) | 24(1.0) | -(-) | -(-) | 4/5 |
| T8 SMH h1 tum | 800 | 32 | 24(3.1) | 19(2.4) | 11 | 19(2.4) | 17(2.1) | 42(2.3) | 57(2.0) | 11/16 |
| T8 SMH h1 2016+ | 536 | 47 | 38(3.6) | 34(3.3) | 25 | 34(3.3) | 34(2.8) | 42(2.3) | 57(2.0) | 10/11 |
| T8 SMH h1 2011-15 | 264 | 0 | -4(-0.4) | -13(-1.4) | -17 | -13(-1.4) | -4(-0.4) | -(-) | -(-) | 1/5 |
| T8 SMH h3 tum | 576 | 50 | 26(1.9) | 37(2.7) | 13 | 37(2.7) | 17(1.3) | 47(1.4) | 25(0.5) | 12/16 |
| T8 SMH h3 2016+ | 391 | 66 | 36(2.0) | 53(2.9) | 23 | 53(2.9) | 28(1.4) | 47(1.4) | 25(0.5) | 10/11 |
| T8 SMH h3 2011-15 | 185 | 16 | 4(0.2) | 3(0.2) | -9 | 3(0.2) | 4(0.2) | -(-) | -(-) | 2/5 |

| yil | h2 n | h2 brut | h2 fazla | h3 n | h3 brut | h3 fazla |
|--|--:|--:|--:|--:|--:|--:|
| 2011 | 25.0 | -36 | -14 | 24.0 | 30 | 65 |
| 2012 | 40.0 | 14 | -23 | 36.0 | 3 | -52 |
| 2013 | 36.0 | -9 | 8 | 32.0 | 47 | 72 |
| 2014 | 31.0 | 45 | 23 | 27.0 | 13 | -20 |
| 2015 | 28.0 | 46 | 62 | 24.0 | 33 | 58 |
| 2016 | 31.0 | -13 | -20 | 27.0 | 43 | 34 |
| 2017 | 38.0 | 18 | -15 | 35.0 | 9 | -41 |
| 2018 | 29.0 | 30 | 51 | 26.0 | 22 | 53 |
| 2019 | 31.0 | 12 | -7 | 29.0 | 60 | 33 |
| 2020 | 27.0 | 37 | 24 | 23.0 | 84 | 62 |
| 2021 | 37.0 | 26 | 4 | 33.0 | 58 | 25 |
| 2022 | 35.0 | 148 | 64 | 30.0 | 214 | 90 |
| 2023 | 35.0 | -14 | -36 | 30.0 | 45 | 10 |
| 2024 | 38.0 | 59 | 34 | 29.0 | 77 | 39 |
| 2025 | 28.0 | 82 | 71 | 26.0 | 89 | 72 |
| 2026 | 30.0 | 48 | 35 | 27.0 | 48 | 31 |

- T3 plasebo (2000 cekilis, tohum 20261110, cakismasiz, yil dagilimi esit): T1 XU030 k1 h2 n519 gercek 31 / plasebo 17 (sd 9) p=0.0465; T1 XU030 k1 h3 n458 gercek 54 / plasebo 25 (sd 10) p=0.0025; T2 sepet k1 h3 n458 gercek 60 / plasebo 33 (sd 11) p=0.0075

## Hukumler
- T1 ZAYIFLADI: endeks momentumu var ama yil-eslestirilmis fazla h3 +30 (t 2,3), h2 +15 (t 1,5); IS zayif (t 1,4), 2022 yili tek basina asiri (fazla +90); AYNA yok: z<=-1 sonrasi h2 ham getiri -2, h3 +20 (devam degil) -> simetrik momentum degil, TL surukleme izi.
- T2 CURUTULDU (hisse sepeti olarak): sepet-XU030 farki ~0 (h3 -0, t 0,0; h2 +5, OOS ve SON negatif). Etki hisse secimi degil endeksin kendisi; 44 bps'te fazla eksi maliyet negatif (28-44).
- T3 ZAYIFLADI: plasebo p 0,047 / 0,0025 / 0,0075; gercek sinyal yil dagiliminin urunu degil ama plasebo ortalamasi gercegin ~yarisi (h3 54 vs 25), yani brutun yarisi surukleme. Fazla t 1,5-2,3: cok-test duzeltmesini gecmez.
- T4: KCHOL ZAYIFLADI (ham fazla k1,5 h2 +64 t 3,1; artik +41 t 3,4 ama OOS artik t 0,8; net44 fazla +20); TUPRS CURUTULDU (k1 h3 fazla +40 t 2,2, artik +17 t 1,2; net44 fazla -4); ASELS CURUTULDU (artik ~0); EREGL ZAYIFLADI (k1,5 h2 fazla +53 t 2,7 ama k1 h2/h3 t<=2). Etki buyuk olcude endeks momentumu, hisseye ozgu kisim yalniz KCHOL k1,5'te IS'te.
- T5 ZAYIFLADI (en saglam aday, ayakta degil): KBE k1,5 -> AKBNK h2 fazla +64 (t 2,7); IS/OOS/SON hepsi pozitif ama OOS t 1,1, 11/16 yil; ayni gun XU030 z>=1 orani %20, XU030 z<1 alt kumesinde de +56 (t 2,0) -> endeks etkisine indirgenmiyor; hedef sirasi XU030 32 < 4 banka 50 < AKBNK 64 (tutarli). net10 fazla +54, net44 fazla +20 (t belirsiz). k1,0 h2 +40 t 2,6 yonu dogruluyor.
- T6 ZAYIFLADI: uzun fazla h2 +33 (2,1), h3 +42 (2,1); IS 45 / OOS 43 (t 1,1) / SON 32 (t 0,7); net44 fazla ~0 (-2). Kisa taraf brut ~0 (-3/+3) -> kisa yok. 'Hedef geride' kosulu TERS: TUPRS t gunu <=0 ise fazla +1/+11 (t 0,1/0,4) -> CURUTULDU; >0 ise +58/+67 (t 2,7/2,3). Endekse gore goreli alt gruplar tutarsiz (h2 26<40, h3 54>30).
- T7 ZAYIFLADI: z>1 -> RYSAS h1 fazla +54 (t 3,1), net10 +63; ama IS t 1,5 (OOS 89 t 3,0, SON 119 t 3,0 -> yeni donem yogun), 1 gun gec giris fazla +17 (t 1,0), net10 +26 (t 1,5), net44 ~-8; net44'te fazla +10. RYSAS 250g medyan hacim 145 mn TL, RYGYO 79 mn TL (ince). Kapanista 10 dk kala RYGYO z'si kesin bilinmez; kural ayakta degil.
- T8: fark DONEMDEN geliyor. QQQ h2: tum +36 net t 2,9 (K1 +34 t 2,7 ile uyumlu), 2016+ +53 t 3,5, 2011-15 +1 t 0,0; QQQ h3 2016+ +68 t 3,7 (onceki +77 t 3,9 ile uyumlu), 2011-15 +28 t 1,1. SMH h1: 2016+ +34 t 3,3, 2011-15 -13 t -1,4. Hukum: 2016+ AYAKTA (QQQ 11/11 yil pozitif fazla), 2011-15 YOK -> rejim bagimli, tum donemde ZAYIFLADI.

## Oz-denetim ve acik kalanlar
- Ileriye bakis yok: sd60/sd250 ve beta 1 gun gecikmeli; giris t kapanisi, ABD d -> BIST ilk sonraki gun; T4 beta t-1'e kadar. T1 ilk 3 islem (2011-02-01, 02-04, 03-03) ham JSON'dan saf python ile elle yeniden hesaplandi: z ve getiri (-177,7/-36,8/-27,2 bps) pandas ile birebir.
- Ornek K1 ile ayni: XU030 k1 h3 n458, KCHOL k1,5 h2 n245 (K1 246). Brut/net sayilar K1'i yeniden uretti; fark yil-eslestirmeden: fazla genelde bruttun ~%40-60'i.
- Maskelenen veri hatasi: PGSUS, RYGYO, RYSAS 1'er gun. Hacim0 gunleri atildi (RYSAS son 250g'de hacim0 yok). Pozisyon cikis gunu yeni girise acik.
- Acik: cok-test duzeltmesi yok (K1 tarama sonucu secildi -> t'ler iyimser); blok/bootstrap t yok; gercek spread/likidite yok (44 bps varsayim); kapanis -10 dk sinyal vekili (kesin kapanis z yerine) test edilmedi; 2022 ciktilari disarida denenmedi.
