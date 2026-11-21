# K1 — Backtest sonucu (dogalgaz araclari, kapanista giris, 1-3 gun)

Betik: `kod/01_backtest.py <veri>` (tek komut, ~10 sn). Tum satirlar: `ek/K1_tum_testler.csv` (705 satir). Tarih: 2026-11-20 son veri.

## 1. Veri kontrolu
- NG=F-UNG |fark|>%6 gun: 60 ; ayin 27-30u: 49 -> NG=F sinyal olarak kullanilmadi
- BOIL |r|>%60: 0 KOLD |r|>%60: 0 -> atilan gun 0
- BOIL-2xUNG basit |sapma|>%5 gun: 35 KOLD+2xUNG: 36 (atilmadi; denetim m.6)
- BOIL hacim 0 gun: 83 KOLD: 4 (fiyat korundu)
- UNG acilis=kapanis & H=L (acilis gecersiz) gun: 0
- TTF hacim 0 gun: 469 ; X1 baslangic: 2019-01-25
- UNL gecersiz gun (kapanis degismedi ya da hacim 0): 142
- NEXT hacim 0 gun: 335 ; CRK |r|>%25: 19
- G4 saatlik gun (14:30 ve 15:30 bari var): 723 ilk 2023-12-26
- EIA gunu: Persembe varsayimi (Persembe tatilse ayni haftanin Carsambasi); gercek EIA takvimi kullanilmadi. EIA gun sayisi: 1023
- Sepet uye-gun sayisi ort.: 4.86 ; gaz sepeti ilk gun: 2007-06-14
- Toplam sinyal hucresi: 416 ; BH sayimina giren IS testi: 398 ; kesif (G4): 18
- NG=F gunluk ve saatlik seri karistirilmadi; G4 yalniz UNG saatlik barlarla (14:30 bar acilisi -> 15:30 bar kapanisi).
- Bolunme: ham (duzeltilmemis) fiyat yok; duzeltilmis veride |r|>%60 gun 0, atilan gun 0. BOIL-2xUNG sapmalari endeks vade takvimi farkindan; atilmadi.
- Hayatta kalma yanliligi: SWN, eski CHK, CTRA/COG yok; 2021 oncesi sepet yalniz hayatta kalanlar (E testleri iyimser).
- EIA: gercek yayin takvimi yerine Persembe varsayimi. UNG roll penceresi: vade bitiminden onceki 10.-7. is gunu yaklasigi (USCF takvimi kullanilmadi). Is gunu = NYSE islem gunu.

## 2. Test sayisi ve etiketler
- Sinyal hucresi: 416 (BH sayimina giren IS testi 398; G4 kesif 18, BH disi). Islem satiri: 289.
- En kucuk BH q: 0.967; IS |t|>=2 hucre: 4. Adim 1 (|t|>=2 ve q<=0,10) gecen hucre: 0.
- Etiketler (islem satiri): KULLANILAMAZ: 285; IZLE (yalniz OOS) +gap: 2; IZLE (yalniz OOS): 2
- Sans beklentisi: 289 islem satirinda OOS t>=2 ile ~%2,5 rastlantisal isabet ~7 satir; "IZLE (yalniz OOS)" satirlari bu duzeyde.
- Kurallar: IS gaz hucrelerinde 2011-10-06 - 2021-12-31 (UNG 2007-2011 yalniz `pre_*` kolonlari); OOS 2022-01-03+. t: gunluk strateji P&L serisi, cakisan lotlar toplanir, Newey-West gecikme h; `*_t_ind` ortusmeyen alt kume.
- Adim 2-3 islem goren urunle (yukari: BOIL ve UNG uzun; asagi: KOLD uzun; hisse: sepet uzun). Birlesik yon ve korumali satirlar BH'ye girer, etiket almaz (teshis).
- GUCU YETERSIZ: denetim m.4, adim 1'i gecip OOS'de gecemeyen hucrelere uygulanir (MDE > 2x|IS ort|); adim 1 gecen olmadigindan 0. MDE her satirda `MDE` kolonunda.
- Maliyet: taban (UNG 10, BOIL/KOLD 15, hisse 6-12 bps); `OOS_net2x` 2 kat, `OOS_netz` |z_UNG|>2 gunlerinde 2 kat.

## 3. Etiketli ozet tablo (KULLANILABILIR + IZLE + her testten en guclu bos sonuc)
| CSV satir | test | kural | urun | n / yilda | IS ort bps (t) | OOS ort bps (t) | 2024-26 ort bps (t) | OOS net bps | OOS isabet | etiket |
|---|---|---|---|---|---|---|---|---|---|---|
| 140 | G3 | r_gece z yukari |z|>1 | KOLD h=1 | 543 / 36 | 44.0 (1.54) | 129.1 (2.02) | 118.4 (1.41) | 114.1 | 0.53 | IZLE (yalniz OOS) +gap |
| 386 | T2 | G1 oyn.orta r_UNG z yukari |z|>1 | KOLD h=1 | 156 / 11 | 4.3 (0.07) | 239.8 (2.07) | 286.2 (2.17) | 224.8 | 0.64 | IZLE (yalniz OOS) +gap |
| 664 | X1 | TTF r z yukari |z|>2 -> UNG | BOIL h=3 | 51 / 7 | 357.2 (1.47) | 782.2 (2.30) | 922.6 (2.02) | 767.2 | 0.59 | IZLE (yalniz OOS) |
| 665 | X1 | TTF r z yukari |z|>2 -> UNG | UNG h=3 | 51 / 7 | 162.1 (1.30) | 390.5 (2.16) | 458.9 (1.90) | 380.5 | 0.68 | IZLE (yalniz OOS) |
| | | **her testten en guclu bos sonuc (tum donem t en yuksek)** | | | | | | | | |
| 422 | E1 | r_UNG z yukari |z|>0 -> sepet | SEPET h=2 | 2339 / 120 | 9.0 (0.79) | 22.0 (1.30) | 5.0 (0.25) | 11.9 | 0.51 | KULLANILAMAZ |
| 502 | E2 | UNG 3g z yukari |z|>1 -> sepet | SEPET h=3 | 672 / 35 | 34.0 (1.18) | 21.5 (0.57) | -21.4 (-0.60) | 11.3 | 0.49 | KULLANILAMAZ |
| 562 | E3 | sepet fazla getiri z asagi |z|>1 -> UNG | KOLD h=3 | 584 / 39 | 87.8 (1.77) | 152.8 (1.46) | 175.2 (1.29) | 137.8 | 0.56 | KULLANILAMAZ |
| 565 | E4 | EQT fazla getiri z yukari |z|>0 -> kucukler | KUCUK h=1 | 2377 / 125 | 12.6 (1.55) | 13.8 (1.28) | 8.5 (0.65) | 1.8 | 0.51 | KULLANILAMAZ |
| 590 | E5 | hisse-sepet artik z <-1.5 AL (ham) | hisse h=3 | 1378 / 72 | 24.0 (0.92) | 27.3 (0.82) | 3.7 (0.11) | 17.2 | 0.48 | KULLANILAMAZ |
| 611 | E6 | 5g UNG - 5g sepet fazla z <-1 -> sepet | SEPET h=2 | 806 / 43 | 20.3 (0.69) | -3.1 (-0.08) | 28.6 (0.85) | -13.3 | 0.43 | KULLANILAMAZ |
| 19 | G1 | r_UNG z >1 (yukari) | KOLD h=1 | 552 / 37 | 10.9 (0.40) | 107.9 (1.80) | 122.9 (1.55) | 92.9 | 0.53 | KULLANILAMAZ |
| 56 | G2 | 3g birikimli z asagi |z|>1 | KOLD h=1 | 673 / 45 | 38.9 (1.67) | 40.2 (0.81) | -18.2 (-0.28) | 25.2 | 0.53 | KULLANILAMAZ |
| 152 | G3 | r_gece z asagi |z|>1 | KOLD h=3 | 602 / 40 | 76.8 (1.35) | 168.8 (1.75) | 98.8 (0.98) | 153.8 | 0.58 | KULLANILAMAZ |
| 215 | G4 | UNG 14:30-16:00 z yukari |z|>1 -> h=1 | BOIL h=1 | 95 / 35 | kesif | tum 74.1 (1.14) | 74.1 (1.14) | 59.1 | 0.58 | KULLANILAMAZ |
| 224 | G5 | EIA gunu (Per) r_UNG z asagi |z|>0 | KOLD h=1 | 423 / 28 | 29.3 (1.16) | 54.5 (1.03) | 38.9 (0.68) | 39.5 | 0.53 | KULLANILAMAZ |
| 263 | G6 | bitis gunu Per (UNG uzun kosullu) | KOLD h=1 | 765 / 51 | 43.7 (1.86) | 70.7 (1.68) | 90.3 (2.04) | 55.7 | 0.55 | KULLANILAMAZ |
| 274 | G7 | son islem gununden sonraki 5 gun (giris E, cikis E+5) | KOLD h=5 | 181 / 12 | 251.1 (2.15) | -17.7 (-0.06) | -287.1 (-1.01) | -32.7 | 0.47 | KULLANILAMAZ |
| 284 | G8 | 20g (UNG-UNL) isaret asagi (neg=contango) | KOLD h=1 | 2168 / 143 | 21.2 (1.56) | 50.3 (1.95) | 17.3 (0.59) | 35.3 | 0.53 | KULLANILAMAZ |
| 317 | T1 | MA10 asagi | KOLD h=1 | 2064 / 136 | 15.5 (1.19) | 20.2 (0.74) | 9.9 (0.32) | 5.2 | 0.51 | KULLANILAMAZ |
| 363 | T2 | G1 oyn.dusuk r_UNG z asagi |z|>0 | KOLD h=1 | 725 / 48 | 19.9 (1.18) | 28.5 (0.87) | 7.3 (0.19) | 13.5 | 0.51 | KULLANILAMAZ |
| 658 | X1 | TTF r z yukari |z|>2 -> UNG | BOIL h=2 | 51 / 7 | 75.9 (0.38) | 482.9 (1.57) | 569.4 (1.35) | 467.9 | 0.59 | KULLANILAMAZ |
| 690 | X2 | TTF z asagi |z|>1 -> LNG sepeti | LNGSEP h=3 | 210 / 28 | 90.7 (1.50) | 24.0 (0.58) | 29.7 (0.56) | 16.6 | 0.47 | KULLANILAMAZ |
| 696 | X3 | USO z asagi |z|>1 -> UNG | KOLD h=1 | 581 / 39 | 16.9 (0.66) | 56.2 (1.14) | 47.5 (0.84) | 41.2 | 0.55 | KULLANILAMAZ |

## 4. L1 — kaldirac erimesi (ortusmeyen pencereler, 2011-10+; bps)
fark = gerceklesen - (+-2 x birikimli UNG); oynaklik = ideal gunluk 2x bilesik - 2x birikimli (kesin); s2 yaklasik = -c*Sum(u^2) (log bazli, basit farki abartir); artik = gercek - ideal + ucret (vade takvimi/endeks farki).

| h | BOIL fark | BOIL oynaklik | BOIL artik | KOLD fark | KOLD oynaklik | KOLD artik | ucret | ikisi kaybetti |
|---|---|---|---|---|---|---|---|---|
| 1 | -5.4 | 0.0 | -5.02 | 1.47 | 0.0 | 1.85 | -0.38 | 0.01 |
| 2 | -10.64 | -0.73 | -9.16 | 1.73 | -2.18 | 4.66 | -0.75 | 0.02 |
| 3 | -16.01 | -0.47 | -14.41 | 3.59 | -1.18 | 5.9 | -1.13 | 0.03 |
| 5 | -28.08 | -3.66 | -22.54 | 1.29 | -7.9 | 11.07 | -1.88 | 0.04 |
| 10 | -55.73 | -13.39 | -38.57 | 3.34 | -22.38 | 29.49 | -3.77 | 0.08 |
| 21 | -120.81 | -25.55 | -87.35 | -1.63 | -37.76 | 44.05 | -7.92 | 0.10 |
- h=10 rejime gore BOIL fark / oynaklik: tum -55.73/-13.39; dusuk -58.06/-6.84; orta -54.12/-17.21; yuksek -54.33/-17.82 (tamami `ek/K1_L1.csv`).

## 5. L2 — kosulsuz ortalama gunluk getiri (bps, t)
| arac | 2012-21 | 2022-26 | kis 2012-21 | yaz 2012-21 | kis 2022-26 | yaz 2022-26 |
|---|---|---|---|---|---|---|
| UNG | -4.7 (-0.86) | -4.8 (-0.43) | -18.6 (-1.91) | 4.9 (0.78) | -5.4 (-0.26) | -4.5 (-0.35) |
| BOIL | -13.3 (-1.30) | -18.2 (-0.88) | -42.1 (-2.29) | 6.5 (0.55) | -23.9 (-0.63) | -14.5 (-0.61) |
| KOLD | 9.5 (0.93) | 14.0 (0.68) | 36.5 (2.00) | -9.2 (-0.78) | 18.7 (0.49) | 10.9 (0.46) |

## 6. L3 — maruziyet (secili; tamami `ek/K1_L3.csv`)
| arac | beta son250 | R2 | beta 2022+ | R2 | yillik oyn | ort abs 1g % | ort abs 3g % | 60g dolar hacmi mn |
|---|---|---|---|---|---|---|---|---|
| AR | 0.29 | 0.21 | 0.40 | 0.29 | 0.37 | 1.84 | 3.23 | 153 |
| BOIL | 1.85 | 0.97 | 1.81 | 0.97 | 1.10 | 4.61 | 8.10 | 128 |
| CNX | 0.22 | 0.20 | 0.22 | 0.17 | 0.29 | 1.46 | 2.47 | 64 |
| CRK | 0.46 | 0.24 | 0.49 | 0.28 | 0.55 | 2.64 | 4.81 | 39 |
| EQT | 0.26 | 0.24 | 0.34 | 0.28 | 0.30 | 1.43 | 2.50 | 418 |
| EXE | 0.28 | 0.29 | 0.27 | 0.25 | 0.30 | 1.43 | 2.48 | 281 |
| FCG | 0.14 | 0.07 | 0.16 | 0.10 | 0.29 | 1.44 | 2.62 | 27 |
| KOLD | -1.84 | 0.97 | -1.81 | 0.96 | 1.10 | 4.60 | 7.85 | 84 |
| LNG | 0.05 | 0.01 | 0.09 | 0.04 | 0.32 | 1.51 | 2.75 | 601 |
| RRC | 0.25 | 0.16 | 0.35 | 0.25 | 0.37 | 1.68 | 3.01 | 183 |
| TTF_F | 0.32 | 0.06 | 0.18 | 0.02 | 0.81 | 3.54 | 6.07 |  |
| UNG | 1.00 | 1.00 | 1.00 | 1.00 | 0.59 | 2.51 | 4.33 | 254 |
| XOP | 0.12 | 0.06 | 0.15 | 0.08 | 0.30 | 1.49 | 2.72 | 563 |

## 7. On kayitsiz kesifler (en cok IZLE; hicbiri etiket almadi)
- BOIL, 2xUNG'yi tek gunde bile ortalama -5.4 bps/gun geride izliyor (h=1'de oynaklik erimesi tanim geregi 0; fark ucret -0.38 + artik -5.02). KOLD artigi 1.85 bps/gun. Kaynak: BOIL/KOLD endeksinin (Bloomberg NG alt endeksi) UNG'den farkli vade gecis takvimi. Uzun BOIL tasimanin yapisal maliyeti.
- Isaret degisimi: UNG z>2 yukari gununden sonra h=1 UNG ort. IS 9.2 bps (t 0.23), OOS -280.3 bps (t -2.32), n_OOS 32; z>1'de OOS -67.5 (t -2.02). IS secimi BOIL dedigi icin kural geregi KULLANILAMAZ; 2022+ buyuk yukselis sonrasi donus yalniz gozlem (CSV satir 34, 18).
- Isaret kaliciligi (UNG sinyal satirlari, n=224): 2007-2011 ile IS ayni isaret %67, IS ile OOS ayni isaret %67.

## 8. Yapilamayanlar ve sinirlar
- G9 (NOAA HDD): yapilmadi (istege bagli; gorev veri indirmeyi yasakliyor). Test sayimina girmedi.
- Gercek EIA yayin takvimi ve USCF roll takvimi kullanilamadi (yaklasik kurallar; bolum 1).
- Ham fiyatla bolunme orani kontrolu yapilamadi (yalniz duzeltilmis veri); |r|>%60 kontrolu 0 gun.
- Korumali E5 hedefi icin t+1 acilis duyarliligi yok (hisse bazli gece getirisi kurulmadi); teshis satiri.
- Kesif (G4, 2023-12+) satirlarinda IS/OOS ayrimi yok; yon tum donemden secildi, en cok IZLE.
- X1 TTF sinyali 2019-01-25den (hacim kurali); IS yalniz 3 yil. Duyarlilik kolonlari: `ttf_gecikme1_ort`, `ttf_aydonumu_haric_ort`.
