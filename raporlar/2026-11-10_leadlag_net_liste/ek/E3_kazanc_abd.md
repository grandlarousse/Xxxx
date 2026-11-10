# E3_kazanc_abd — çıkarım defteri (ham ajan çıktısı)

araç: 11/30

## Özet

Sonuc kisa: ABD hisseleri icin, kullanicinin duzenine (kapanisa 10 dk kala sinyal, ayni kapanista giris, 1-3 gun, kapanista cikis) uyan ve maliyetten sonra ayakta kalan bir oncu->hedef kurali kulliyatta YOK. Net uygulanabilir ticker listesi cikmiyor.

1) Lead-lag: ABD'de tek tek hisse fiyati verisi kullanilamadi (Yahoo ve Stooq kapali); butun testler Ken French 49 sektor portfoyleri uzerinde (2010-09/2026, ~4.200 gun, IS 2010-20, OOS 2021-26). Onceden yazilmis 150 testin hicbiri FDR'den (q 0,10) gecmedi; en dusuk q 0,24. Tek 'aday' hastaneler (NYSE:HCA vekili) -> medtech (NYSE:BDX vekili): 5 gunluk piyasa artigi z>+1 ise sonraki 3-5 gunde sektorde +25 bps artik getiri; t 2,82 (A) / 2,38 (B), q 0,24 / 0,43. OOS'ta 10 bps maliyetle +5,8 (A) / +7,5 (B), 20 bps ile -4,2 / -2,5. Hukum FILTRE, giris sinyali degil. Hisse duzeyinde (HCA->BDX) test edilmedi; getiri piyasa-hedgeli artik oldugu icin Midas'ta (yalniz long) beta riski ayrica gelir.
2) Genis tarama (1.320 test): yalniz 4 test FDR'den gecti, hepsi Fin sektorunun ertesi gunu (Insur, Hardw, Food, Paper); bir gun atlayinca hepsi kayboluyor, OOS kuyruk 1-9 bps, maliyet altinda. Diger butun sektor baglari (Meals<-Trans, Fin<-SMB, Drugs<-kendi, vb.) YOK.
3) 'Geride kalan hisse sektore yetisir' turu dogrudan test EDILMEDI. En yakin: sektorlerin kendi gecmis artigi (OWN) ongorucusu; hicbiri FDR'den gecmedi.
4) abd_test tablolarinda 1-3 gun tutulan, kapanista girilen kural yok; testler aylik/yillik ufukta (kaldiracli trend, momentum, sektor rotasyonu, anomaliler). Kisa vade reversal (aylik) 2010-26'da brut +%0,1/yil (t 0,04), 10 bps ile -%4,2; gunluk reversal brut %5,6/yil ama uygulanamaz. Takvim etkileri (ay donumu, bayram, FOMC) 'oldu' ya da 'onemsiz'.
5) Calismanin genel hukmu: ABD'de 1-3 gunluk kapanistan kapanisa islem icin yasayan kenar bulunmadi; kisa ufuk kenarlari bozulmus, ABD surucuLerinin 'oncuLugu' saat farkindan ibaret (VIOP calismasi). Plan S1/S2 lider swing kullaniyor; bunun kendisi geri test edilmedi.
Ek: TL cinsi hedefte tek ABD oncusu AMEX:XLE -> TUPRS (FILTRE, tek basina net +11 bps, t 1,0, IS -6). Bugunku durum: rejim KIRMIZI, VIX 6.11'de 25,64.

## Sinyal defteri

### Hastaneler -> medtech (HCA vekili -> BDX)

- **sinif:** ABD-hisse
- **tur:** leadlag
- **oncu:** NYSE:HCA (FF49 Hlth vekili; kontrol NYSE:UHS)
- **hedef:** NYSE:BDX (FF49 MedEq vekili)
- **kural:** e = r_HCA - beta252*r_SPX (log); S = son 5 gunun e toplami; z = (S - ort252(S))/std252(S); z>+1 ise sonraki 3-5 seansta BDX lehine. Test edilen: FF49 Hlth 5g artik z -> MedEq artigi, L=5,h=5. z<-1 bilgi tasimiyor.
- **sinyal_saati:** ABD t kapanisinda bilinir (00:00 TSI); okuma 00:30-01:00 ya da 08:00-09:00 TSI
- **giris_orijinal:** A: t kapanisindan t+h kapanisina (t+1 gecesi dahil, ust sinir); B: t+2..t+h+1 (t+1 atlanir, muhafazakar). Acilis fiyati yok
- **c0_uyumu:** kismen
- **c0_notu:** A varyanti kapanis girisine yakin ama sinyal t kapanisini icerir (10 dk once tam bilinmez). Getiri piyasa-hedgeli artik; Midas'ta (long-only) beta riski hedgelenemez. Giris sebebi degil, sirlama.
- **tutma:** 3-5 seans (10 gunde kayboluyor)
- **yon:** long (yalniz z>+1)
- **n:** ~4.206 gun; OOS uygun kuyruk n=233
- **net_bp:** OOS z>+1 kuyrugu: A brut 15,8 -> net10 +5,8 / net20 -4,2; B brut 17,5 -> net10 +7,5 / net20 -2,5. Tam ornek kuyruk 5 gunde +25,0 (IS +29,6 / OOS +17,5)
- **t:** A 2,82 (p 0,005); B 2,38
- **is_oos:** A: IS t 1,95 / OOS t 2,02; B: IS 1,05 / OOS 2,33. 17 yilin 14'unde pozitif (negatif: 2016-18)
- **son_donem:** 2024-26 icin ayri net hesaplanmadi. OOS 2021-09/2026'da 20 bps ile net ~ -2,5; B'de IS t 1,05'e dusuyor; q 0,24 (A) / 0,43 (B) FDR'den gecmiyor; 5,10 gun komsuda (5,10)/(10,5) t ~1,0
- **maliyet:** 10 bps ve 20 bps gidis-donus (IBKR buyuk hisse ~10; kayma dahil ~20)
- **hukum:** FILTRE (KENAR degil): sektorde BDX'e oncelik; FDR gecmedi; hisse (HCA->BDX) duzeyinde TEST EDILMEDI
- **guven:** dusuk
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §0 madde 3, §2.1, §2.3, §4.2; hesaplar/leadlag_uygulama/abd/cikti/t01_birincil.csv (Hlth,5,5 satiri); hesaplar/leadlag_uygulama/abd/ll_z_filtre.pine
- **alinti:** Etki yalnız z > +1 kuyruğunda: 5 günde +25 bps artık getiri (IS +30, OOS +18).

### Fin sektoru ertesi gun <- Insur/Hardw/Food/Paper (genis tarama)

- **sinif:** ABD-hisse
- **tur:** leadlag
- **oncu:** FF49 Insur, Hardw, Food, Paper sektor artiklari (tek hisse/ETF kodu yok)
- **hedef:** FF49 Fin portfoyu (TW/CME vekil; NASDAQ:TW, NASDAQ:CME) - islem enstrumani yok
- **kural:** Sektor piyasa artigi (L=1) -> Fin artigi h=1 (Paper icin h=3); 252g z; 1.320 test icinde
- **sinyal_saati:** t kapanisi
- **giris_orijinal:** A: t+1 kapanis-kapanis; B: t+2
- **c0_uyumu:** hayir
- **c0_notu:** Kazanc t+1 gecesine bagli; kapanista girince yok oluyor
- **tutma:** 1 gun (Paper 3)
- **yon:** Insur -, Food -, Paper -, Hardw +
- **n:** ~4.200 gun
- **net_bp:** OOS uygun kuyruk +1..+9 bps brut; 10 bps ile -1..-9 net
- **t:** A: Insur -4,30; Hardw +4,19; Food -3,72; Paper(h3) -3,66
- **is_oos:** B'de hepsi kayboluyor (en dusuk q 0,60)
- **son_donem:** OOS uygun kuyruk 1-9 bps; maliyet altinda
- **maliyet:** 10 bps
- **hukum:** YOK (FDR gecen tek 4 test, B'de sifira iniyor; vekil kirli: Fin'de REIT'ler var)
- **guven:** orta
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §0 madde 2, §2.2
- **alinti:** 4 test FDR'den geçti. Hepsi Fin hedefinde ve ertesi güne ait

### Seyahat/havayolu -> otel (Meals <- Trans)

- **sinif:** ABD-hisse
- **tur:** leadlag
- **oncu:** FF49 Trans (NYSE:DAL, AMEX:JETS vekil)
- **hedef:** NASDAQ:MAR, NASDAQ:HLT (FF49 Meals)
- **kural:** Trans artigi L=1, h=3 -> Meals artigi; en guclu test (21 testin)
- **giris_orijinal:** A: t+1..t+3; B: t+2..t+4
- **c0_uyumu:** hayir
- **c0_notu:** Yalniz ertesi acilis beklentisi
- **tutma:** 3 gun
- **yon:** long
- **net_bp:** b +3,8 bps/sigma
- **t:** A 2,02; B 0,61
- **is_oos:** IS t 1,05 / OOS t 1,99 (A); q 0,55
- **son_donem:** B'de 0,61: bilgi t+1'de fiyatlaniyor
- **maliyet:** 10/20 bps
- **hukum:** YOK (islenebilir degil)
- **guven:** orta
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §2.1 ve §3.5

### Sigorta sektoru kendi 5g artigi (ters)

- **sinif:** ABD-hisse
- **tur:** ortalamaya-donus
- **oncu:** FF49 Insur kendi 5 gunluk artigi
- **hedef:** NASDAQ:ACGL, NYSE:MRSH (FF49 Insur)
- **kural:** (L=5,h=5) kendi artik z
- **giris_orijinal:** A: t+1..t+5; B: t+2..t+6
- **c0_uyumu:** kismen
- **c0_notu:** Yalniz long Midas'ta ters (short) yon kullanilamaz
- **tutma:** 5 gun
- **yon:** ters (yukselenin sonraki 5 gunu zayif)
- **net_bp:** b -10,9 bps/sigma
- **t:** A -2,54; B -2,65
- **is_oos:** IS -2,52 / OOS -1,03; q 0,42
- **son_donem:** OOS t -1,03
- **maliyet:** 10/20 bps
- **hukum:** YOK
- **guven:** orta
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §2.1

### LabEq <- piyasa (5,5)

- **sinif:** ABD-hisse
- **tur:** leadlag
- **oncu:** MKT (piyasa 5 gunluk getiri; SP:SPX)
- **hedef:** NYSE:TMO (FF49 LabEq)
- **kural:** MKT (5,5) z -> LabEq artigi
- **giris_orijinal:** A: t+1..t+5
- **c0_uyumu:** kismen
- **tutma:** 5 gun
- **yon:** ters
- **net_bp:** b -11,5 bps/sigma
- **t:** A -2,89; B -2,27
- **is_oos:** IS -2,54 / OOS -1,55; q 0,24
- **son_donem:** OOS -1,55
- **maliyet:** 10/20 bps
- **hukum:** YOK
- **guven:** dusuk
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §2.1, §3.6

### Ilac sektoru kendi 1g artigi

- **sinif:** ABD-hisse
- **tur:** kendi-sinyali
- **oncu:** FF49 Drugs kendi artigi (L=1)
- **hedef:** NASDAQ:RPRX (ekonomik olarak Drugs; SIC'e gore Fin)
- **kural:** (L=1,h=1)
- **giris_orijinal:** A: t+1; B: t+2
- **c0_uyumu:** hayir
- **tutma:** 1 gun
- **yon:** long
- **net_bp:** b +3,9 bps/sigma
- **t:** A 3,07; B -0,05
- **is_oos:** IS 2,60 / OOS 1,75; q 0,24
- **son_donem:** B'de sifir: yalniz ertesi gun
- **hukum:** YOK
- **guven:** orta
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §2.1, §3.6

### Saglik sektoru <- piyasa (1,1)

- **sinif:** ABD-hisse
- **tur:** leadlag
- **oncu:** MKT
- **hedef:** NYSE:EHC (FF49 Hlth)
- **kural:** MKT (1,1) -> Hlth artigi
- **c0_uyumu:** hayir
- **net_bp:** b +3,4 bps/sigma
- **t:** A 2,15; B 0,42
- **is_oos:** IS 2,19 / OOS 0,59; q 0,55
- **son_donem:** OOS t 0,59
- **hukum:** YOK
- **guven:** orta
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §2.1, §3.2

### Fin <- SMB (5,5)

- **sinif:** ABD-hisse
- **tur:** leadlag
- **oncu:** SMB faktoru (buyuk-kucuk)
- **hedef:** NASDAQ:TW, NASDAQ:CME (FF49 Fin)
- **kural:** SMB (5,5) -> Fin artigi
- **c0_uyumu:** kismen
- **net_bp:** b +8,2 bps/sigma
- **t:** A 2,17; B 2,03
- **is_oos:** IS 1,53 / OOS 1,65; q 0,55
- **son_donem:** OOS 1,65 (anlamsiz)
- **hukum:** YOK
- **guven:** orta
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §2.1, §3.3

### Hshld <- kendi 5g artigi

- **sinif:** ABD-hisse
- **tur:** ortalamaya-donus
- **oncu:** FF49 Hshld kendi artigi
- **hedef:** NYSE:SN (FF49 Hshld)
- **kural:** (5,5)
- **c0_uyumu:** kismen
- **net_bp:** b -11,6 bps/sigma
- **t:** A -2,01; B -1,35
- **is_oos:** IS -1,75 / OOS -0,99; q 0,55
- **hukum:** YOK
- **guven:** dusuk
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §2.1, §3.6

### Meals <- Autos (genis tarama)

- **sinif:** ABD-hisse
- **tur:** leadlag
- **oncu:** FF49 Autos
- **hedef:** NASDAQ:MAR/NASDAQ:HLT (FF49 Meals)
- **kural:** genis tarama
- **giris_orijinal:** B
- **c0_uyumu:** kismen
- **net_bp:** 20 bps sonrasi net -10 bps
- **is_oos:** IS ve OOS ikisi de anlamli (B'de tek)
- **son_donem:** net -10 bps
- **hukum:** YOK
- **guven:** dusuk
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §2.2

### MedEq <- Drugs/LabEq/MKT/SMB/dVIX/kendi (BDX icin diger oncular)

- **sinif:** ABD-hisse
- **tur:** leadlag
- **oncu:** FF49 Drugs, LabEq; MKT, SMB; dVIX
- **hedef:** NYSE:BDX (FF49 MedEq)
- **kural:** (1,1),(1,3),(5,5)
- **c0_uyumu:** kismen
- **t:** |t|<2,1 hepsinde (ornegin MKT (1,1) A 1,96 ama B -1,13; dVIX (5,5) A -2,09)
- **is_oos:** MKT(1,1) A OOS 1,13; MKT(5,5) A 1,67
- **hukum:** YOK
- **guven:** orta
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §2.1; hesaplar/leadlag_uygulama/abd/cikti/t01_birincil.csv (MedEq,BDX satirlari)

### Odeyici -> saglayici (Hlth <- Insur/MedEq)

- **sinif:** ABD-hisse
- **tur:** leadlag
- **oncu:** FF49 Insur (NYSE:UNH vekil), MedEq
- **hedef:** NYSE:EHC
- **kural:** (1,1),(1,3),(5,5)
- **c0_uyumu:** kismen
- **t:** |t| <= 1,4 (A ve B)
- **hukum:** YOK
- **guven:** orta
- **kaynak:** ajanlar/leadlag_abd_uygulama.md §3.2

### ABD rafineri/enerji -> TUPRS (yan iliski, ABD oncu, BIST hedef)

- **sinif:** BIST-VIOP
- **tur:** leadlag
- **oncu:** AMEX:XLE - beta*SP:SPX (ABD t-1; test: FF49 Oil artigi)
- **hedef:** BIST:TUPRS1!
- **kural:** ABD oncu getiri artigi, 1 sigma basina
- **giris_orijinal:** tek basina islem 15,5 bps
- **c0_uyumu:** kismen
- **c0_notu:** ABD hisse hedefi degil; TUPRS ana kurali bu ajanin kapsami disinda
- **yon:** ayni
- **net_bp:** +15,8 bps/1 sigma; tek basina islem net +11 (t 1,0)
- **t:** NW t 3,96; q 0,003
- **is_oos:** IS 2,09 / OOS 3,10 / 2024+ 1,69; tek basina islemde IS net -6
- **son_donem:** 2024+ t 1,69 (dusus); tek basina islem t 1,0
- **hukum:** FILTRE (kenar degil; kombinasyon TEST EDILMEDI)
- **guven:** orta
- **kaynak:** uygulama/LEADLAG_UYGULAMA.md satir ~77 (Yan iliskiler tablosu)

### Brent gece -> TUPRS / ABD t-1

- **sinif:** BIST-VIOP
- **tur:** leadlag
- **oncu:** ICEEUR:BRN1!
- **hedef:** BIST:TUPRS1!
- **kural:** ABD t-1
- **c0_uyumu:** kismen
- **net_bp:** -1,9
- **t:** 2,23; q 0,19
- **hukum:** YOK
- **guven:** orta
- **kaynak:** uygulama/LEADLAG_UYGULAMA.md Yan iliskiler tablosu

### Aylik kisa vade reversal (French ST_Rev)

- **sinif:** ABD-hisse
- **tur:** ortalamaya-donus
- **oncu:** onceki ay kaybedenler - kazananlar (VW 2x3)
- **hedef:** piyasa genisligi (islem enstrumani yok; AMEX:SPY vekil degil)
- **kural:** aylik 2x3 VW, onceki ay sirali
- **c0_uyumu:** hayir
- **tutma:** 1 ay
- **yon:** kaybedeni al
- **net_bp:** 2010-26 yillik brut +0,1%; net c10 -4,2%, c20 -8,5%; 2020-26 brut -5,2%, net c10 -9,5%
- **t:** 2010-2026: 0,04; 1927-2026: 6,35
- **is_oos:** 1963-89 yillik %9,3 (t 5,44); 1990-2009 %2,8 (t 0,94); 2010-26 %0,1
- **son_donem:** 2020-2026: -5,2%/yil (t -1,01)
- **maliyet:** 5/10/20 bps (varsayimsal, aylik %90 tek-yon devir)
- **hukum:** OLDU (kullanilamaz)
- **guven:** yuksek
- **kaynak:** ajanlar/abd_test.md §7 (Test 5) ve hesaplar/abd_test/cikti/t5_tablolar.md

### Gunluk reversal (gunluk rebalans ST_Rev)

- **sinif:** ABD-hisse
- **tur:** ortalamaya-donus
- **oncu:** gunluk kaybedenler - kazananlar
- **hedef:** yok
- **kural:** gunluk tam devir
- **c0_uyumu:** hayir
- **tutma:** 1 gun
- **net_bp:** 2010-26 yillik brut %5,6, Sharpe 0,40; net yok
- **is_oos:** 1963-89 %30,7 / 1990-2009 %28,1 / 2010-26 %5,6 / 2020-26 %5,1
- **son_donem:** 2020-26 brut %5,1, Sharpe 0,26
- **hukum:** uygulanamaz (tam devir, maliyet yok)
- **guven:** orta
- **kaynak:** ajanlar/abd_test.md §7 (Gunluk_STR_yillik sutunu)

### VIX>25 sonrasi reversal (panik rejimi)

- **sinif:** ABD-hisse
- **tur:** ortalamaya-donus
- **oncu:** onceki ay sonu VIX>25 (CBOE:VIX)
- **hedef:** asiri satilmis kaliteli hisseler (enstruman yok)
- **kural:** ST_Rev, VIX>25 aylari
- **c0_uyumu:** hayir
- **tutma:** 1 ay
- **n:** 29 ay (2010-26)
- **net_bp:** +0,55%/ay VIX>25; digerlerinde -0,08%/ay
- **son_donem:** 2010-26 n=29
- **hukum:** yalniz not: ufuk aylik, dogrulama dosyalarinda teyidi yok
- **guven:** dusuk
- **kaynak:** ajanlar/abd_swing_kenarlar.md §5 (tablo satiri 'Reversal x stres'); uygulama/NET_LISTE_ABD.md §3
- **alinti:** Önceki ay sonu VIX > 25 olan aylarda STR 2010–26 +%0,55/ay (n = 29), diğerlerinde −%0,08.

### G2 VIX panik cozulmesi (SPY)

- **sinif:** ABD-ETF
- **tur:** olay
- **oncu:** CBOE:VIX paniği
- **hedef:** AMEX:SPY
- **kural:** 40 seans tutma
- **c0_uyumu:** hayir
- **tutma:** 40 seans
- **n:** 25
- **net_bp:** piyasaya gore ~+1,8 puan
- **t:** ~1,7
- **is_oos:** orneklem ici
- **hukum:** yalniz golge kayit
- **guven:** dusuk
- **kaynak:** uygulama/NET_LISTE_ABD.md §5 (G2 satiri)

### Ay donumu (TOM: son gun + ilk 3 gun)

- **sinif:** ABD-ETF
- **tur:** takvim
- **oncu:** takvim
- **hedef:** AMEX:SPY (CRSP VW piyasa vekil)
- **kural:** son is gunu + ilk 3 is gunu
- **c0_uyumu:** kismen
- **tutma:** 4 gun
- **net_bp:** 2010-26: TOM 7,6 bp/gun vs diger 5,5; TOM-only CAGR %4,6 vs BH %14,2
- **is_oos:** 1927-87 16,3 vs 1,2; 1988-2009 12,0 vs 2,5
- **son_donem:** 2010-26 7,6 vs 5,5 bp/gun (getirinin %24'u gunlerin %19'unda)
- **hukum:** OLDU
- **guven:** orta
- **kaynak:** ajanlar/abd_swing_kenarlar.md §5 (tablo 'Ay donumu')

### Bayram oncesi

- **sinif:** ABD-ETF
- **tur:** takvim
- **oncu:** takvim
- **hedef:** AMEX:SPY (vekil)
- **kural:** bayram oncesi gun
- **c0_uyumu:** kismen
- **tutma:** 1 gun
- **n:** 156
- **net_bp:** 2010-26: 13,0 bp (ortalama gun 5,9 bp); toplam katki ~%0,7/yil
- **is_oos:** 1927-87 33,7; 1988-2009 14,2; 2010-26 13,0 bp
- **hukum:** ONEMSIZ
- **guven:** orta
- **kaynak:** ajanlar/abd_swing_kenarlar.md §5

### Pre-FOMC drift

- **sinif:** ABD-ETF
- **tur:** takvim
- **oncu:** FOMC
- **hedef:** AMEX:SPY
- **kural:** duyurudan onceki 24 saat
- **c0_uyumu:** hayir
- **tutma:** 1 gun
- **net_bp:** 1994-2011 +49 bp (t>4,5)
- **son_donem:** 2015 sonrasi esasen yok
- **hukum:** OLDU
- **guven:** orta
- **kaynak:** ajanlar/abd_swing_kenarlar.md §5; dogrulama/v_abd.md #25 (DOGRU)

### S1 baz kirilimi / S2 geri cekilme (Tier A swing)

- **sinif:** ABD-hisse
- **tur:** kendi-sinyali
- **oncu:** yok (kendi RS: hisse/SPX, ABD_RJ)
- **hedef:** NYSE:BDX, NYSE:EHC, NASDAQ:TW, NASDAQ:ACGL, NASDAQ:MAR
- **kural:** ABD_RJ 'S1 on kosul/S2 lider' EVET, pivot <= %3 uzak, stop 1,0-2,0 ATR ve <= %8; ilk 3 seans basarisiz kirilim -> MOO ile cik; +2R ya da 4. seansta +1R -> yarisini sat
- **c0_uyumu:** kismen
- **c0_notu:** Girisler acilis (MOO) ya da 16:45-17:15 TSI; kapanis girisli 1-3 gun lead-lag degil
- **tutma:** 3-4 seans + trend
- **son_donem:** KEN/PLAN dayanak: kazananlarin ortak yontemi; geri test yok
- **hukum:** TEST EDILMEDI (geri test yok); rejim KIRMIZI, en erken pilot 16.11
- **guven:** dusuk
- **kaynak:** uygulama/NET_LISTE_ABD.md §3, §0; dogrulama/v_abd.md §4 madde 2
- **alinti:** ABD'de bu ufukta yaşayan bir kenar bulunmadı.

### G1 bilanco gap'i (2.-5. gun) PEAD

- **sinif:** ABD-hisse
- **tur:** olay
- **oncu:** bilanco gap'i
- **hedef:** U, EW, NYSE:SN, NYSE:BDX adaylari
- **kural:** 2.-5. gun
- **c0_uyumu:** hayir
- **tutma:** 2-5 gun
- **net_bp:** sadece-uzun ust portfoy VW piyasayi gecmiyor (AnnouncementReturn -1,4%/yil 2010-25)
- **hukum:** yalniz golge kayit; buyuk hissede PEAD yok (Martineau)
- **guven:** orta
- **kaynak:** uygulama/NET_LISTE_ABD.md §5; ajanlar/abd_test.md §0 madde 8, §6.4; dogrulama/v_abd.md #23

### Sektor ETF rotasyonu (kume izni)

- **sinif:** ABD-ETF
- **tur:** goreli-momentum
- **oncu:** sektor ETF'leri (AMEX:XLV, AMEX:IHI, AMEX:XLF, AMEX:XRT)
- **hedef:** sektor ETF'leri
- **kural:** top-N, aylik
- **c0_uyumu:** hayir
- **tutma:** 1 ay
- **net_bp:** 49 endustri izgarasi medyani 2010-26 %14,2 vs piyasa %14,1 (+0,1 puan); 40 varyantin 40'i negatif (VD U7)
- **son_donem:** 2020-26 +1..+2 puan
- **hukum:** yalniz kume izni filtresi
- **guven:** orta
- **kaynak:** ajanlar/abd_test.md §0 madde 6; uygulama/NET_LISTE_ABD.md §5

### Overnight momentum (MOC girisli)

- **sinif:** ABD-hisse
- **tur:** mikroyapi
- **oncu:** momentum
- **hedef:** momentum isimleri
- **kural:** kapanista (MOC) gir, gun ici kovalama
- **c0_uyumu:** evet
- **c0_notu:** Kapanis girisi C0'a uyar ama kanit literatur (Lou-Polk-Skouras) ve geri test yok
- **tutma:** gece
- **net_bp:** literatur: ~%0,95/ay overnight, %0,11 intraday
- **hukum:** TEST EDILMEDI; yalniz-gece al-sat maliyeti kenari yer
- **guven:** dusuk
- **kaynak:** ajanlar/abd_swing_kenarlar.md §3.1 (satir ~152-154); uygulama/NET_LISTE_ABD.md §3

## Elenenler

- **Piyasa, SMB, dVIX ve sektorun kendi gecmisi -> herhangi hedef sektor:** Hicbiri FDR'den gecmedi; MKT/SMB/dVIX/kendi icin etiket YOK. _( ajanlar/leadlag_abd_uygulama.md §0 madde 5 )_
- **Hisse -> hisse ve endeks -> hisse gunluk onculuk (VIOP calismasi):** ~170 bin testte FDR 0; ABD suruculerinin onculugu saat farkindan ibaret, acilistan sonra kalinti ~0. _( uygulama/NET_LISTE_ABD.md §4 )_
- **Kaldiracli trend (3x NDX + 200 GHO):** Alfa degil beta; 2000-02'de -%89; 2010-26'da filtre getiriyi dusurdu; ufuk ay/yil. _( ajanlar/abd_test.md §0 madde 1-3 )_
- **UMD momentum (uzun-kisa):** 2000 sonrasi neredeyse oldu (CAGR %2,8; 2010-26 %4,0); ufuk aylik. _( ajanlar/abd_test.md §0 madde 4 )_
- **Sadece-uzun momentum (VW ust desil):** Risk ayarli fark yok (Sharpe 0,79 vs 0,87); ufuk aylik. _( ajanlar/abd_test.md §0 madde 5 )_
- **Chen-Zimmermann 212 anomali:** Yayin sonrasi bozulma 0,60 -> 0,24 %/ay; 2010-25 VW 0,07 %/ay; kisa vade reversal ailesi VW'de negatif. _( ajanlar/abd_test.md §0 madde 7; hesaplar/abd_test/cikti/t3_tablolar.md )_
- **PEAD / kazanc olayi sadece-uzun portfoy:** VW piyasayi gecmiyor, buyuk hissede 2006'dan beri yok (Martineau; v_abd #23 DOGRU). _( ajanlar/abd_test.md §0 madde 8 )_
- **Hisseye ozgu kanallar (emsal bilanco, MOVE/VIX, afet, RevPAR, CMS):** Hisse/olay verisi yok, TEST EDILMEDI; yalniz RISK/FILTRE etiketi, giris sebebi degil. _( ajanlar/leadlag_abd_uygulama.md §0 madde 6 )_
- **Kasirga sezonu (Agu-Eki) FF49 Insur:** Fark +1,7 bps/gun, t 0,75; YOK (ACGL'ye ozgu etki TEST EDILMEDI). _( ajanlar/leadlag_abd_uygulama.md §2.4 )_
- **Insider kume alimi:** Yayin sonrasi test yok; ertelendi (VA #26). _( uygulama/NET_LISTE_ABD.md §5 )_
- **Earnings gap / episodic pivot:** Veri engeli, test YAPILAMADI (Stooq/Yahoo kapali). _( ajanlar/abd_test.md §8 )_

## Çelişkiler

- Kisa vade reversal 2010-26: abd_test.md §7 brut +%0,1/yil (t 0,04) ve 2020-26 -%5,2; abd_swing_kenarlar.md §5 -%0,5/yil (SR 0,01) ve 2021-26 -%5,6. Hukum ayni (oldu), sayilar farkli.
- abd_test.md §9 madde 6 'S&P 200-DMA'nin %5,0 ustunde, YTD +%12,3' diyor; dogrulama/v_abd.md #32 bunu YANLIS/eskimis ilan ediyor (4.11 verisi; 5.11'de ~%0,4 ustunde, YTD ~+%7,4). Dogrulama gecerli.
- NET_LISTE_ABD.md §4 'ABD hisseleri hic test edilmedi' ve lead-lag calismasi yalniz 47 VIOP dayanagini kapsar diyor; leadlag_abd_uygulama.md ise ABD'yi sektor (FF49) duzeyinde 1.471 testle taradi. Celiski degil kapsam farki: hisse duzeyi hala yok.
- NET_LISTE_ABD.md'deki NASDAQ:MAR/NYSE:HLT ve NYSE:HLT/AMEX:XRT kodlari yanlis; Hilton'un kodu NASDAQ:HLT (leadlag_abd_uygulama.md §0 madde 7).
- leadlag_abd_uygulama.md §2.1 MedEq<-Hlth icin IS t 1,95/OOS 2,02 (A) verirken §2.3 B varyantinda IS t 1,05/OOS 2,33; kanit varyanta gore degisiyor, IS'de bir gun atlayinca zayifliyor.
- NET_LISTE_ABD.md §3 'Kar gece olusuyor' diyor (overnight); ayni belge ABD'de 1-3 gunluk kenar yok diyor ve Plan 17:30-00:00 arasi emir degisikligini yasakliyor: kapanis girisi pratikte mumkun mu belirsiz.

## Açık kalanlar

- HCA -> BDX tek hisse duzeyinde (ve NYSE:UHS kontrolu) test edilmedi; yalniz FF49 sektor portfoyu. LL_z Pine betigi derlenmedi.
- MedEq<-Hlth icin 2024-26 ayri net hesaplanmadi.
- 'Geride kalan hisse sektore yetisir' turu (hisse/sektor ETF orani, BDX/IHI gibi) dogrudan test edilmedi; yalniz sektorlerin kendi gecmis artigi (OWN) ongorucusu test edildi, hicbiri FDR'den gecmedi.
- abd_test tablolarinda 1-3 gun tutulan kapanis girisli (dip alimi, IBS/RSI2, kirilim) kural yok; t1-t7 tablolari aylik/yillik ufuklu. Bu satirlar cikarim: tablolarin tamamini satir satir okumadim, ozet ve baslik duzeyinde grep yaptim.
- ajanlar/abd_swing_kenarlar.md ve uygulama/LEADLAG_UYGULAMA.md yalniz grep ve hedefli bolumlerle okundu; v_abd.md hukum tablosu ve §2.1 okundu.
- S1/S2 ve ABD_RJ rejim kurallarinin geri testi yok; kullanicinin tarzina en yakin (breakout/pullback) test hic yapilmadi (v_abd.md §4 madde 2).
- TUPRS ana kurali (BIST hedef) bu ajanin kapsami disinda kaldi.
