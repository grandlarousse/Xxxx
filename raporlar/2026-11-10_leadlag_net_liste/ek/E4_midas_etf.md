# E4_midas_etf — çıkarım defteri (ham ajan çıktısı)

araç: 21/32

## Özet

Sonuc: bu kulliyatta dogrulanmis, C0'a (ayni kapanista giris) uyan, maliyet sonrasi calisan bir oncu->hedef (lead-lag) kurali YOK. RAPOR'un hukmu bu ve c0_leadlag.csv'yi bagimsiz ozetleyince ayni sonuca vardim.

Dogrulananlar (sizin bildikleriniz): 108.286 testte fdr10 ve fdr05 gecen 0. Tur medyanlari net -17,0 (GERIDE), -19,1 (L_UP), -19,1 (ONDE), -21,4 (L_DN), -20,7 (OWN_DN), -28,2 (OWN_UP) bp. t>3: 17 satir. Duzeltme: "sans beklentisinin altinda" cikarimi gecerli degil; butun dagilim maliyetle negatife kaymis (medyan t -0,64, satirlarin yalniz %28'i t>0). Dogru okuma: en yuksek t 3,67; 108 bin testte saf gurultuyle bile yaklasik 4 civari t beklenir. En kucuk p 3,4e-4, Bonferroni'de ~37'ye cikar.

Benim ek kontrolum (dosyadan hesapladim): ornek-ici (IS) t>3 olan 162 satirin OOS medyani -42 bp, yalniz %22'si OOS'ta pozitif; IS t>2,5 olan 420 satirda medyan -28 bp, %27 pozitif. Yani IS'te guclu gorunmek OOS'u ongormuyor; secim gurultu. Siki suzgecim (t>2,5, IS t ve OOS t>1,5, yil>=%70, en iyi 5 cikinca t>1,5) 39 satir birakiyor; 26 hedefe yayili, hepsi ayni birkac ortak risk bahsinin tekrari.

GERIDE (yetisme) 26.087 testte medyan -17 bp, %31 pozitif; en iyiler IWM->SPY/VOO/IVV/SSO/UDOW h3 kumesi (tek bahis; h1 negatif, h2 ~0), SOXL ve EWT<-SMH. Yetisme kalibi genel olarak calismiyor. t>2,5 olan 139 satir kumeleniyor: maden/metal/uranyum 50 (URNM 14, RING 8, SIL 6), yari iletken 22 (SOXL 10, SMH/SOXX 12), konut/savunma/diger sektor 24; kaldiracli hedef orani %21 (tum testte %5). Oncu tarafinda LQD 16, IWM 12, TLT 11, VIX_dlog 10: ortak risk-istahi/faiz faktoru. Hedefin kendi sinyali (OWN) 1.289 testte hic t>2,5 vermedi; ancak URNM, RING, SIL, TAN icin hedefin kendi yukselis sinyali (OWN_UP) zaten pozitif, yani "ONDE" orada oncunun degil hedefin kendi momentumu. Oncu katkisi en net ASHR<-TLT, SMH<-XLK, EWT<-SMH, UDOW<-IWM, YANG<-CPER'de.

C0'da ayakta gorunenler lead-lag degil, kendi sinyali: A1 QQQ IBS (h3 +77 bp t 3,9; kapanistan 10 dk once tahminle +56, t 2,4) ve A2 SMH IBS (h1 +42 t 3,7). Digerleri Kademe B, zayif. B4 Asya sepeti ve B10 mega-cap->2x ETF'in oncusu ayni gunun SPY dususu / hissenin kendi RSI'i; gecikmeli oncu degil.

Midas: emir basina 1,5 $ (2.500 $'da gidis-donus 12 bp), MOC/LOC yok (kapanistan ~10 dk once piyasa/limit emri ya da after-hours limit), kesirli var, acigasatis yok, kaldiracli ETF bulunurlugu (SOXL vb.) dogrulanamadi. Tarama maliyeti 13-48 bp, medyan 16.

Pratik: lead-lag adaylarini en fazla kagit uzerinde izleyin; para yatirilabilecek tek sey A1/A2 (yari boyut, mevcut yuksek oynaklikta).

## Sinyal defteri

### A1 QQQ zayif kapanis donusu (IBS<0,10 ve dusus gunu)

- **sinif:** ABD-ETF
- **tur:** kendi-sinyali
- **oncu:** yok (QQQ kendi IBS'si)
- **hedef:** NASDAQ:QQQ
- **kural:** IBS=(kapanis-dusuk)/(yuksek-dusuk) < 0,10 VE kapanis < onceki kapanis; t kapanisinda al; 3 is gunu sonra kapanista sat; stop yok; pozisyondayken yeni sinyal yok sayilir. TV: NASDAQ:QQQ gunluk.
- **sinyal_saati:** kapanis ~23:50 TSI (kis); IBS kapanisa kadar tahmin edilir
- **giris_orijinal:** C0 (c0_tablo); ana yol C1 (ertesi kapanis)
- **c0_uyumu:** kismen
- **c0_notu:** IBS kapanisa ~10 dk kala bilinmiyor; sinir gunleri (IBS 0,08-0,12, |r|<%0,1) sonucu duyarli. C1 bundan bagimsiz.
- **tutma:** 3 gun (h1 +27 t2,1; h2 +59 t3,6)
- **yon:** long
- **n:** 189 (h3, C0)
- **net_bp:** +77,3 (h3 C0); C1 h3 +68,3 t3,48 n177
- **t:** 3,89 (en iyi 5 cikinca 3,18)
- **is_oos:** IS +83,9 / OOS +71,3; yil pozitif %100; kazanma %64
- **son_donem:** 2026: n=10, C1'de yalniz +5 bp; yuksek oynaklik rejiminde islem std 319 bp
- **maliyet:** 2.500 $ pozisyon: 12 bp komisyon + makas (c0 maliyet satiri 13-16 bp)
- **hukum:** dogrulandi, guven orta (Kademe A); gercekci beklenti +45-55 bp; secim duzeltmeli p 0,025-0,055 (cok-test sinirda); C0 kapanis oncesi tahminle 76->56 bp (t 3,68->2,43); SPY (B1) ile sinyallerin %73'u ayni gun; kaldiracli kullanma
- **guven:** orta
- **kaynak:** sonuclar/c0_tablo.csv satir A1 QQQ; RAPOR.md §2 A1 (satir 79-120); notlar/denetim_abd_endeks.md satir 66-71
- **alinti:** QQQ C0: 76 → 56 bp (t 3,68 → 2,43). Sınırdaki işlemler ortalamanın üstünde kazandırmış

### A2 SMH gun sonu zayifligi donusu (IBS<0,20)

- **sinif:** ABD-ETF
- **tur:** kendi-sinyali
- **oncu:** yok (SMH kendi IBS'si)
- **hedef:** NASDAQ:SMH (kopya NASDAQ:SOXX)
- **kural:** IBS < 0,20 (dusus sarti yok); t kapanisinda al (after-hours kapanis+2-5 sent limit ya da kapanis oncesi); ertesi kapanista sat; ertesi gun IBS<0,20 ise bir gun daha tut.
- **sinyal_saati:** kapanis ~23:50 TSI ya da kapanis sonrasi 00:00-01:00 after-hours (kis)
- **giris_orijinal:** C0
- **c0_uyumu:** evet
- **c0_notu:** Kenar yalniz C0'da var; after-hours limit en temiz yol. A1 sinyallerinin ~%90'i A2 gunlerine denk geliyor (ayni risk faktoru).
- **tutma:** 1 gun (h2 +51,8 t3,37; h3 +64,4 t3,2)
- **yon:** long
- **n:** 483 (h1)
- **net_bp:** +42,3 (h1)
- **t:** 3,69 (en iyi 5 cikinca 3,05)
- **is_oos:** IS +44,4 / OOS +40,1; yil pozitif %100; kazanma %58
- **son_donem:** 2026: +109 bp (n=38, yuksek vol); dusuk vol rejiminde +14 (t1,1), orta +38, yuksek +65
- **maliyet:** 2.500 $: 12 bp komisyon + makas; after-hours girisin ~6 bp, kapanis oncesi ~15-20 bp ek maliyeti denetcide
- **hukum:** Kademe A, guven orta; gercekci +31-36 bp; 1.000 $'da esik alti; ertesi kapanis (C1) girisinde kenar +2 bp'ye, ertesi acilista +17'ye dusuyor: kenar tamami ilk gecede
- **guven:** orta
- **kaynak:** sonuclar/c0_tablo.csv satir A2 SMH; RAPOR.md §2 A2 (satir 122-154); sonuclar/c1_tablo.csv A2

### EWT <- SMH yetisme (EWT, SMH'nin ima ettiginden geride)

- **sinif:** ABD-ETF
- **tur:** yetisme
- **oncu:** AMEX:SMH (ya da NASDAQ:SMH; on ek tv_etf.csv'den teyit)
- **hedef:** AMEX:EWT
- **kural:** GERIDE: kalinti = r_EWT(t) - beta60*r_SMH(t); kalinti/sd60 <= -2 ise EWT al; beta ve sd t-1'e kadarki 60 gunle; h=1 kapanista sat.
- **sinyal_saati:** kapanis ~23:50 TSI (her iki ETF de ABD seansinda)
- **giris_orijinal:** C0
- **c0_uyumu:** kismen
- **c0_notu:** z esigi (-2) kapanisa 10 dk kala sinir gunlerinde degisebilir; bu duyarlilik c0_leadlag'de modellenmedi.
- **tutma:** 1 gun
- **yon:** long
- **n:** 89
- **net_bp:** +64,0
- **t:** 3,05 (en iyi 5 cikinca 2,02)
- **is_oos:** IS +83,5 / OOS +43,2 (OOS t 1,57); yil pozitif %90
- **maliyet:** 14 bp (c0_leadlag cost_bp)
- **hukum:** c0_leadlag'de gevsek suzgecten gecer; FDR gecmez (p>0,0005); denetci/yeniden uretim yok; EWT kendi sinyali (OWN) anlamsiz (t<1,3) yani oncu katkisi var gorunuyor; B4 Asya sepetiyle ayni mekanizma ailesi (EWT sepet uyesi, S1 t 2,00)
- **guven:** dusuk
- **kaynak:** sonuclar/c0_leadlag.csv (target=EWT, leader=SMH, kind=GERIDE, h=1); kod/c0_leadlag.py basi

### SMH <- XLK goreli ustunluk devami (ONDE)

- **sinif:** ABD-ETF
- **tur:** goreli-momentum
- **oncu:** XLK (AMEX; on ek teyit)
- **hedef:** NASDAQ:SMH
- **kural:** ONDE: kalinti = r_SMH(t) - beta60*r_XLK(t); kalinti/sd60 >= +2 ise SMH al; 2 gun sonra kapanista sat.
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0
- **c0_uyumu:** kismen
- **c0_notu:** A2'nin zit ucu (A2 zayif kapanista alir, bu guclu gunde alir); ayni SMH'de iki kural birbirini dislayabilir.
- **tutma:** 2 gun (h1 +65,6 t2,68; h3 +85,0 t1,97)
- **yon:** long
- **n:** 75 (h2)
- **net_bp:** +107,6
- **t:** 3,40 (en iyi 5 cikinca 2,56)
- **is_oos:** IS +113,0 / OOS +102,1 (OOS t 2,43); yil pozitif %100
- **maliyet:** 13 bp
- **hukum:** c0_leadlag'de en tutarli lead-lag satirlarindan; ama p=5,5e-4, FDR gecmez; SMH ve XLK ortak holding (NVDA vb.) bu yuzden bagimsiz oncu degil, sektor ici goreli momentum; h3'te t 1,97 'plato' zayif; SMH<-QQQ ONDE h2 +87 t2,55; SMH OWN_UP h2 -53 (negatif)
- **guven:** dusuk
- **kaynak:** sonuclar/c0_leadlag.csv (SMH, XLK, ONDE, h=2); satirlar SMH<-QQQ/XLK ONDE h1-h3

### ASHR <- TLT yukselis (L_UP)

- **sinif:** ABD-ETF
- **tur:** leadlag
- **oncu:** NASDAQ:TLT
- **hedef:** AMEX:ASHR
- **kural:** L_UP: z_TLT(t)=r_TLT/sd60 >= +2 ise ASHR al; ertesi kapanista sat.
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0
- **c0_uyumu:** evet
- **c0_notu:** Her iki enstruman ABD seansinda; sinyal kapanis oncesi bilinir (esik sinirinda hata payi).
- **tutma:** 1 gun (h2 +46 t1,95; h3 +73 t2,48)
- **yon:** long
- **n:** 62
- **net_bp:** +71,0
- **t:** 3,58 (en iyi 5 cikinca 2,55)
- **is_oos:** IS +70,6 / OOS +71,7 (OOS t 3,13); yil pozitif %80
- **maliyet:** 16 bp
- **hukum:** tum c0_leadlag'in en kucuk p'si (3,4e-4) ama FDR/Bonferroni gecmez; ekonomik mekanizma belirsiz (faiz dususu -> Cin A-hisse ETF'i); h2'de zayiflama; L_DN simetrisi calismiyor (-17 bp); TLT L_UP 630 testin 41'i t>2 (gurultu orani)
- **guven:** dusuk
- **kaynak:** sonuclar/c0_leadlag.csv (ASHR, TLT, L_UP, h=1..3)

### SPY/VOO/IVV/SSO/SPXL/UDOW <- IWM yetisme, 3 gun (GERIDE)

- **sinif:** ABD-ETF
- **tur:** yetisme
- **oncu:** IWM
- **hedef:** AMEX:SPY (ayni kume: VOO, IVV, SSO, SPXL, UPRO, UDOW, DIA, XLK)
- **kural:** GERIDE: kalinti = r_hedef(t) - beta60*r_IWM(t); kalinti/sd60 <= -2 ise hedefi al; 3 gun sonra kapanista sat.
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0
- **c0_uyumu:** evet
- **tutma:** 3 gun (SPY h1 -21,2 t-1,43; h2 +7,4)
- **yon:** long
- **n:** 63 (SPY h3)
- **net_bp:** SPY +70,2; SSO +151,8; SPXL +197,0; UDOW +234,3 (t 3,28, n75)
- **t:** SPY 2,67; SSO 2,95; VOO 2,91; UDOW 3,28
- **is_oos:** SPY IS +42,7 / OOS +102,3 (OOS t 2,72); UDOW IS +213,6 / OOS +255,6; yil pozitif %90
- **maliyet:** 13-16 bp
- **hukum:** tek bahis, 8-10 hedefte tekrar ediyor (ayni sinyal gunleri); yalniz h3, h1 negatif, h2 ~0 yani yapi tutarsiz; aile notu AE13 ters yonu (IWM'in SPY'i izlemesi) net negatif buluyor (-28 h1, -89 h3)
- **guven:** dusuk
- **kaynak:** sonuclar/c0_leadlag.csv (leader=IWM, kind=GERIDE); notlar/aile_abd_endeks.md satir 220-240 (AE13)

### SOXL <- QQQ / XLK goreli ustunluk (ONDE), 3x

- **sinif:** ABD-ETF
- **tur:** goreli-momentum
- **oncu:** NASDAQ:QQQ (ve XLK)
- **hedef:** SOXL (3x yari iletken; Midas bulunurlugu dogrulanamadi)
- **kural:** ONDE: SOXL'un QQQ'ya gore beta-kalintisi z>=+2 ise SOXL al; h=1 (h2 de pozitif).
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0
- **c0_uyumu:** kismen
- **c0_notu:** Midas'ta SOXL var mi dogrulanamadi.
- **tutma:** 1-2 gun
- **yon:** long
- **n:** 67 (h1)
- **net_bp:** +248,7 (h1); h2 +302,6 t2,74; XLK ONDE h2 +311,0 t2,88
- **t:** 3,15 (en iyi 5 cikinca 2,06)
- **is_oos:** IS +158,1 / OOS +383,1 (OOS t 2,54); yil pozitif %80
- **maliyet:** 14,2 bp
- **hukum:** SMH ONDE bulgusunun 3x kopyasi, ayni bahis; en kotu islem -1.328 bp; SOXL kendi dususu (OWN_DN h1 +158 t2,0) da pozitif; SOXL 52 hafta zirvesinden -%85, yuksek oynaklik rejiminde kaldiracli arac onerilmiyor
- **guven:** dusuk
- **kaynak:** sonuclar/c0_leadlag.csv (SOXL, QQQ/XLK, ONDE); RAPOR.md §0 oynaklik rejimi (satir 21-33)

### TAN <- DIA goreli ustunluk (ONDE)

- **sinif:** ABD-ETF
- **tur:** goreli-momentum
- **oncu:** DIA
- **hedef:** TAN (gunes enerjisi)
- **kural:** ONDE: TAN'in DIA'ya gore beta-kalintisi z>=+2 ise TAN al; ertesi kapanista sat.
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0
- **c0_uyumu:** kismen
- **tutma:** 1 gun
- **yon:** long
- **n:** 70
- **net_bp:** +94,8
- **t:** 3,20 (en iyi 5 cikinca 2,16)
- **is_oos:** IS +88,4 / OOS +107,1 (OOS t 1,83); yil pozitif %90
- **maliyet:** 16 bp
- **hukum:** gevsek suzgec; TAN OWN_UP h2 +73 (t1,84) yani hedefin kendi momentumu da pozitif; DIA ile mekanik bag zayif
- **guven:** dusuk
- **kaynak:** sonuclar/c0_leadlag.csv (TAN, DIA, ONDE, h=1)

### URNM <- XLK / CPER / DIA / LQD (uranyum ETF'i, ONDE ve L_UP)

- **sinif:** ABD-ETF
- **tur:** goreli-momentum
- **oncu:** XLK (ayrica CPER, DIA, SPY, LQD)
- **hedef:** URNM
- **kural:** ONDE: URNM'nin XLK'ya gore beta-kalintisi z>=+2 ise URNM al; h=1.
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0
- **c0_uyumu:** kismen
- **tutma:** 1 gun
- **yon:** long
- **n:** 57
- **net_bp:** +137,8 (XLK); CPER +131,4 t3,21; LQD L_UP h2 +220,3 t2,90 n35
- **t:** 3,24
- **is_oos:** IS +236,5 / OOS +84,5 (OOS t 1,71): OOS'ta belirgin dusus; CPER'de IS +284,6 / OOS +56,8 (OOS t 1,45)
- **maliyet:** 20 bp
- **hukum:** URNM tek basina t>2,5 satirlarin 14'u; 7 farkli oncuyla ayni sonuc yani oncu degil hedefin kendi hareketi (URNM OWN_UP h1 +94,7 t2,14); en yuksek maliyet kademesi; OOS'ta zayifliyor
- **guven:** dusuk
- **kaynak:** sonuclar/c0_leadlag.csv (target=URNM)

### RING <- LQD yukselis (L_UP)

- **sinif:** ABD-ETF
- **tur:** leadlag
- **oncu:** LQD
- **hedef:** RING (altin madenci)
- **kural:** L_UP: z_LQD >= +2 ise RING al; 2 gun sonra kapanista sat.
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0
- **c0_uyumu:** evet
- **tutma:** 2-3 gun (h3 +204 t2,95)
- **yon:** long
- **n:** 59 (h2)
- **net_bp:** +213,4
- **t:** 3,10 (en iyi 5 cikinca 2,08)
- **is_oos:** IS +242,4 / OOS +181,3 (OOS t 2,37); yil pozitif %80
- **maliyet:** 20 bp
- **hukum:** LQD ayni anda GDX, SIL, URNM, SOXX, SMH hedeflerinde de t>2,5 verir: tek 'tahvil yukselisi -> riskli ETF' faktoru; RING OWN_UP h3 +99,7 t2,09
- **guven:** dusuk
- **kaynak:** sonuclar/c0_leadlag.csv (RING, LQD, L_UP)

### YANG <- CPER yukselis (L_UP), -3x Cin

- **sinif:** ABD-ETF
- **tur:** leadlag
- **oncu:** CPER (K-1/PTP yapisi)
- **hedef:** YANG (-3x FTSE China 50)
- **kural:** L_UP: z_CPER >= +2 ise YANG al; h=1.
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0
- **c0_uyumu:** evet
- **tutma:** 1 gun
- **yon:** long
- **n:** 53
- **net_bp:** +208,2
- **t:** 3,18 (en iyi 5 cikinca 2,06)
- **is_oos:** IS +122,7 / OOS +296,9 (OOS t 3,13); yil pozitif %70
- **maliyet:** 20 bp
- **hukum:** mantik ters (bakir yukselisi -> Cin -3x al); en kotu islem -912 bp; ters kaldiracli arac; Midas bulunurlugu belli degil; ters ETF'li varyantlar rapora gore genelde net negatif
- **guven:** dusuk
- **kaynak:** sonuclar/c0_leadlag.csv (YANG, CPER, L_UP, h=1); RAPOR.md §4 ters ETF (satir 241)

### SIL <- GVZ degisimi (altin oynakligi), ONDE

- **sinif:** ABD-ETF
- **tur:** goreli-momentum
- **oncu:** GVZ_dlog (Cboe; islem gormez)
- **hedef:** SIL (gumus madenci)
- **kural:** ONDE: SIL'in GVZ degisimine gore beta-kalintisi z>=+2 ise SIL al; h=2.
- **sinyal_saati:** kapanis; GVZ kapanisi 16:15 ET, ETF kapanisindan sonra
- **giris_orijinal:** C0
- **c0_uyumu:** hayir
- **c0_notu:** GVZ/VIX serileri 16:15 ET'de kapanir: kapanistan 10 dk once bilinen deger degil (ileriye bakma riski).
- **tutma:** 2 gun
- **yon:** long
- **n:** 50
- **net_bp:** +131,1
- **t:** 3,36 (en iyi 5 cikinca 2,24)
- **is_oos:** IS +2,2 (IS t 0,05) / OOS +210,0 (OOS t 4,0)
- **maliyet:** 16 bp
- **hukum:** IS'te hic kanit yok, kazanc tamamen 2022+; oncu islem gormeyen endeks ve gec kapaniyor; GVZ'nin SIL ile beta'si dusuk oldugundan satir fiilen SIL OWN_UP (h2 +67,6 t1,64)
- **guven:** dusuk
- **kaynak:** sonuclar/c0_leadlag.csv (SIL, GVZ_dlog, ONDE, h=2); RAPOR.md §9 zamanlama (satir 378)

### QQQ'nun IBS sinyali -> SMH (capraz) 

- **sinif:** ABD-ETF
- **tur:** leadlag
- **oncu:** NASDAQ:QQQ (IBS<0,10+dusus)
- **hedef:** NASDAQ:SMH
- **kural:** A1 sinyali (QQQ IBS<0,10 ve dusus) ertesi kapanista SMH al, 3 gun tut; ayni sinyalle SPY->QQQ de test edildi.
- **sinyal_saati:** sinyal t kapanisi, giris ertesi gun kapanis ~23:50 TSI
- **giris_orijinal:** C1 (c0_tablo'da yok)
- **c0_uyumu:** kismen
- **c0_notu:** C0 sayilari c0_tablo.csv'de yok; ayni gun C0 girisi olarak raporlanmadi.
- **tutma:** 3 gun (h2 +61,7 t2,60; h1 +30,7 t1,60)
- **yon:** long
- **n:** 177 (h3, C1)
- **net_bp:** +106,8 (C1 h3); SPY sinyali->QQQ C1 h3 +69,1 t3,27
- **t:** 3,41
- **is_oos:** IS +100,6 / OOS +112,5; yil pozitif %100
- **maliyet:** 2.500 $ varsayimi (13 bp SMH)
- **hukum:** A1'in yuksek-beta kopyasi (SMH beta ~1,8 x QQQ): bagimsiz oncu etkisi yok, ayni dip-donus; SMH sinyali->QQQ zayif (+29 t2,05)
- **guven:** dusuk
- **kaynak:** sonuclar/c1_tablo.csv satirlar 'X QQQ sinyali -> SMH', 'X SPY sinyali -> QQQ', 'X SMH sinyali -> QQQ'

### B4 Asya sepeti: SPY<=-%1,5 gununde SPY'dan cok dusen Asya ETF'leri

- **sinif:** ABD-ETF
- **tur:** yetisme
- **oncu:** AMEX:SPY (gunluk getiri <= -%1,5)
- **hedef:** AMEX:EWJ, EWY, EWT, FXI, EWA, EWH (sepet; her uye ayni gun SPY'dan cok dusmusse)
- **kural:** SPY gunluk getirisi <= -1,5% VE ETF getirisi <= SPY getirisi ise o Asya ETF'ini t kapanisinda al; ertesi kapanista sat (h=1). Yilda ~11 sinyal gunu.
- **sinyal_saati:** kapanis ~23:50 TSI (SPY dususu o gun belli)
- **giris_orijinal:** C0
- **c0_uyumu:** evet
- **c0_notu:** Tanimin oncusu SPY'nin ayni gun dususu; gecikmeli oncu degil, SPY'ya gore goreli ortalamaya donus/NAV eszamansizligi.
- **tutma:** 1 gun (h2 +75,1 t2,45; h3 +72,6 t1,73)
- **yon:** long
- **n:** 110 sinyal gunu (293 islem)
- **net_bp:** +52,9 (c0_tablo, gun kumeli); RAPOR §3'te +57
- **t:** 1,89 gun kumeli (islem bazli 3,2; NW 2,22)
- **is_oos:** IS +65,7 / OOS +41,8; C1 h1 +30,7 t1,27; O1 -3
- **son_donem:** 2018 ve 2024 negatif; son sinyal 05.11.2026
- **maliyet:** 2.500 $ (EWY 13, EWJ/EWT 14, FXI 14,9, EWA/EWH 16 bp)
- **hukum:** Kademe B, zayif: gun kumeli t 1,9 esik alti, en iyi 5 gun cikinca t 0,79, 1.000 $'da t 1,35; ertesi acilista girmek zararli (-3 bp); 'ayakta kalan' sayilmaz; denetci 'zayif', 'izleme sinyali'
- **guven:** dusuk
- **kaynak:** sonuclar/c0_tablo.csv satir B4; kod/kurallar.py B4; notlar/aile_uluslararasi.md satir 11-12, 57; notlar/denetim_uluslararasi.md satir 13, 22, 47
- **alinti:** Aynı gün açılan işlemler bağımsız değil: gün bazında t 1,9, eşik altı.

### B10 mega-cap hisse RSI(2) dibi -> 2x ETF

- **sinif:** ABD-hisse
- **tur:** ortalamaya-donus
- **oncu:** yok (dayanak hissenin kendi RSI(2)'si; NVDA, TSLA, AAPL, AMZN, META, MSFT, GOOGL)
- **hedef:** NASDAQ:NVDL, TSLL, AMZU, MSFU, GGLL (yedek AAPU, METU); yuksek oynaklikta hissenin kendisi
- **kural:** Hisse RSI(2) < 10 VE hisse kapanisi > SMA(200): t kapanisinda 2x ETF al; hisse kapanisi > SMA(5) olunca ayni kapanista, en gec t+3 kapanisinda sat; her sinyale esit pay; stop yok. RSI Wilder/RMA.
- **sinyal_saati:** kapanis ~23:50 TSI (sinyallerin %33'unde RSI 7-10: kapanis oncesi karar donebilir)
- **giris_orijinal:** C0
- **c0_uyumu:** kismen
- **c0_notu:** Lead-lag degil, hissenin kendi sinyali; 2x ETF yerine hisse onerisi yuksek oynaklik rejiminde.
- **tutma:** h<=3 (c0_tablo sabit h: h1 +37,4 t1,14; h2 +88,4 t2,14; h3 +127,6 t2,65)
- **yon:** long
- **n:** 201 (h3, gun kumeli)
- **net_bp:** +127,6 (h3); RAPOR'da +120 (SMA5 cikisli)
- **t:** 2,65 gun kumeli
- **is_oos:** RAPOR: C0/O1/C1 = 120/104/98; c0_tablo IS bos, OOS 127,6
- **son_donem:** 2020 ve 2024'e bagli; 06.11.2026'da 7 hissenin 4'u SMA200 altinda (sinyal uretmez)
- **maliyet:** 16-23 bp (TSLL 23,4)
- **hukum:** zayif: ayni kural S1 disi 47 hissede +11,5 bp t 0,77 (zamanlama kenari +5,5 t 0,37); dayanaklar sonradan secilmis kazananlar; bilanco islemlerinden (n=24, +569 bp) onemli kisim; en kotu islem -%45 (TSLA 2x); denetci 'ZAYIF'
- **guven:** dusuk
- **kaynak:** sonuclar/c0_tablo.csv satir B10; notlar/denetim_tek_hisse_kaldiracli.md satir 8-12, 70-74; notlar/aile_tek_hisse_kaldiracli.md satir 8-12, 98
- **alinti:** Kenar, sonradan seçilmiş 7 kazanandaki V-dönüşlerinden geliyor.

### B2 GDXJ IBS<0,10 ve dusus, 3 gun

- **sinif:** ABD-ETF
- **tur:** kendi-sinyali
- **oncu:** yok (GDXJ kendi IBS'si)
- **hedef:** AMEX:GDXJ (JNUG 2x, Midas dogrulanmadi)
- **kural:** IBS<0,10 ve kapanis<onceki kapanis; t kapanisinda al; 3 gun sonra kapanista sat.
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0
- **c0_uyumu:** kismen
- **tutma:** 3 gun (h1 +43,7 t2,84; h2 +54,7 t2,40)
- **yon:** long
- **n:** 253
- **net_bp:** +102,3
- **t:** 3,36 (en iyi 5 cikinca 2,62)
- **is_oos:** IS +75,7 / OOS +130,1; yil pozitif %80
- **son_donem:** C1'de +24 bp t0,75 (C1 h3) yani kenar C0'a bagimli
- **maliyet:** 2.500 $
- **hukum:** Kademe B zayif: madenci havuzunda IS kaniti yok (t 0,5), esik komsulugunda IS cokuyor; kapanisa bagimli (kapanis kacarsa atla); maxDD -%25
- **guven:** dusuk
- **kaynak:** sonuclar/c0_tablo.csv B2; sonuclar/c1_tablo.csv B2; RAPOR.md §3 B2 (satir 167)

### B5 EWY IBS<0,10 ve dusus, 1 gun

- **sinif:** ABD-ETF
- **tur:** kendi-sinyali
- **oncu:** yok (EWY kendi IBS'si)
- **hedef:** AMEX:EWY (KORU 3x, Midas dogrulanmadi)
- **kural:** IBS<0,10 ve kapanis<onceki kapanis; t kapanisinda al; ertesi kapanista sat.
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0
- **c0_uyumu:** kismen
- **tutma:** 1 gun (h2 +46,3 t2,44; h3 +39,0 t1,55)
- **yon:** long
- **n:** 225
- **net_bp:** +42,2
- **t:** 3,09 (en iyi 5 cikinca 2,22)
- **is_oos:** IS +27,9 / OOS +52,9; yil pozitif %80
- **son_donem:** 2026'nin asiri oynaklik rejimine bagli (EWY 20g oynaklik %71)
- **maliyet:** 2.500 $ (EWY 13 bp)
- **hukum:** Kademe B; taramadan secildi; C1 girisinde -9 bp (t -0,60) yani kenar yalniz ayni kapanista
- **guven:** dusuk
- **kaynak:** sonuclar/c0_tablo.csv B5; sonuclar/c1_tablo.csv B5; RAPOR.md §3 B5

### B1 SPY IBS<0,10 ve dusus, 3 gun

- **sinif:** ABD-ETF
- **tur:** kendi-sinyali
- **oncu:** yok
- **hedef:** AMEX:SPY (SSO, SPXL)
- **kural:** IBS<0,10 ve kapanis<onceki kapanis; t kapanisinda al (RAPOR ana yol C1); 3 gun tut.
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0 (ana mod C1)
- **c0_uyumu:** kismen
- **c0_notu:** SPY C0 kapanis-oncesi tahminden etkilenmiyor (36->39 bp).
- **tutma:** 3 gun (C0 h1 +6,9 t0,65; h2 +28,1 t2,18)
- **yon:** long
- **n:** 181 (h3 C0)
- **net_bp:** +37,2 (C0); C1 h3 +53,8 t2,87
- **t:** 2,18 (C0; en iyi 5 cikinca 1,39)
- **is_oos:** C0 IS +19,4 / OOS +52,0; yil pozitif %90
- **son_donem:** VIX<20'de 1.000 $'da negatif
- **maliyet:** 2.500 $
- **hukum:** Kademe B; secilmis sivri tepe, secim duzeltmeli p=0,20; QQQ ile ayni gun sinyal verirse yalniz A1
- **guven:** dusuk
- **kaynak:** sonuclar/c0_tablo.csv B1; RAPOR.md §3 B1

### B3a/B3b ay sonu (GDX / GLD)

- **sinif:** Altin-ETF
- **tur:** takvim
- **oncu:** yok (takvim)
- **hedef:** AMEX:GDX (B3a), AMEX:GLD (B3b)
- **kural:** Ayin son islem gunu kapanisinda al, yeni ayin 3. islem gunu kapanisinda sat.
- **sinyal_saati:** takvimle onceden bilinir
- **giris_orijinal:** C0
- **c0_uyumu:** evet
- **c0_notu:** Takvim sinyali, kapanis tahmini gerekmez. Bir sonraki giris 30.11.2026 kapanisi.
- **tutma:** 3 gun
- **yon:** long
- **n:** 117
- **net_bp:** GDX +74,1; GLD +34,2
- **t:** GDX 2,01; GLD 2,16 (en iyi 5 cikinca GDX 0,96; GLD 1,16)
- **is_oos:** GDX IS +61,9 / OOS +86,5; GLD IS +23,0 / OOS +45,4
- **son_donem:** C1'de GDX +43,6 t1,18; GLD +18,3 t1,04; son yillara bagimli
- **maliyet:** 2.500 $
- **hukum:** Kademe B zayif; ikisi ayni bahis; en iyi 5 islem cikinca t<1,2
- **guven:** dusuk
- **kaynak:** sonuclar/c0_tablo.csv B3a, B3b; RAPOR.md §3 B3, §3 takvim (satir 178-181)

### B6 10Y Hazine ihalesi oncesi TBT

- **sinif:** ABD-ETF
- **tur:** olay
- **oncu:** yok (ihale takvimi)
- **hedef:** TBT (tercih; TMV -3x)
- **kural:** 10Y ihalesinden 3 is gunu once kapanista al, ihaleden 1 gun once kapanista sat.
- **sinyal_saati:** takvimle onceden bilinir
- **giris_orijinal:** C0
- **c0_uyumu:** evet
- **tutma:** 2 gun
- **yon:** long
- **n:** 117
- **net_bp:** +60,8 (h2); TMV +102
- **t:** 2,80 (en iyi 5 cikinca 1,80)
- **is_oos:** IS +60,0 / OOS +61,6; yil pozitif %100
- **son_donem:** C1'de +17,0 t0,74
- **maliyet:** 2.500 $
- **hukum:** Kademe B zayif: 2002-2016'da calismiyor, global FDR yok, ters kaldiracli, Midas dogrulanmadi; sonraki ihale 08.12.2026 (giris 03.12 kapanisi)
- **guven:** dusuk
- **kaynak:** sonuclar/c0_tablo.csv B6; RAPOR.md §3 B6

### B7 EIA dogalgaz raporu oncesi KOLD (Kasim-Mart)

- **sinif:** ABD-ETF
- **tur:** olay
- **oncu:** yok (EIA takvimi)
- **hedef:** KOLD (PTP/K-1)
- **kural:** Rapor gununden once kapanista KOLD al, rapor gunu kapanisinda sat; yalniz Kasim-Mart.
- **sinyal_saati:** takvimle onceden bilinir
- **giris_orijinal:** C0
- **c0_uyumu:** evet
- **tutma:** 1 gun (h3 +210 t2,29)
- **yon:** long
- **n:** 203
- **net_bp:** +117,9
- **t:** 2,52 (en iyi 5 cikinca 1,65)
- **is_oos:** IS +149,3 / OOS +85,5
- **son_donem:** C1 h1 -26,6 t-0,56
- **maliyet:** 2.500 $
- **hukum:** Kademe B zayif: mevsim ayrimi sonradan yapildi, en iyi 10 islem cikinca t 0,6, PTP (%10 kesinti riski), tek islemde -%17
- **guven:** dusuk
- **kaynak:** sonuclar/c0_tablo.csv B7; RAPOR.md §3 B7

### B9 SVXY RSI(2)<10 ve SVXY>SMA200

- **sinif:** ABD-ETF
- **tur:** ortalamaya-donus
- **oncu:** yok (SVXY kendi RSI'i)
- **hedef:** CBOE:SVXY (PTP teyidi yoksa ayni sinyalle QQQ/QLD)
- **kural:** RSI(2)<10 ve SVXY>SMA200: t kapanisinda al; 2 gun sonra kapanista sat.
- **sinyal_saati:** kapanis ~23:50 TSI
- **giris_orijinal:** C0
- **c0_uyumu:** kismen
- **tutma:** 2 gun (h1 +82,3 t2,44)
- **yon:** long
- **n:** 59
- **net_bp:** +157,3
- **t:** 3,16 (en iyi 5 cikinca 2,13)
- **is_oos:** IS +143,6 / OOS +163,8; yil pozitif %62,5
- **son_donem:** IS kaniti yalniz 2021; C1 h2 -27,7
- **maliyet:** 2.500 $
- **hukum:** Kademe B zayif: 2010-2018 vekilinde kenar 0, Subat 2018 tipi kuyruk riski, PTP; SVIX elendi
- **guven:** dusuk
- **kaynak:** sonuclar/c0_tablo.csv B9; RAPOR.md §3 B9

### DBB <- KWEB gecikmeli oncu (regresyon, kural degil)

- **sinif:** diger
- **tur:** leadlag
- **oncu:** KWEB
- **hedef:** DBB (Invesco DB baz metaller; K-1)
- **kural:** h1 gecikme regresyonu: KWEB'in dunku getirisi DBB'nin bugunku getirisini aciklar; esik kurali olarak test edilmedi.
- **giris_orijinal:** regresyon (C1 benzeri hizalama)
- **c0_uyumu:** hayir
- **c0_notu:** Kural degil istatistik; C0 ile test edilmedi.
- **tutma:** 1-3 gun
- **yon:** long
- **net_bp:** 1 sd basina 10,5 bp (h1), 14,4 bp (h3)
- **t:** lag_t h1 4,04 (OOS 3,20); h3 3,07 (OOS 2,05)
- **hukum:** FDR (q=0,10) geciyor ama islem kurali yok; DBB K-1 yapisi, likidite dusuk; maliyet uzerinde oldugu gosterilmedi
- **guven:** dusuk
- **kaynak:** sonuclar/leadlag_sweep.csv (target=DBB, leader=KWEB); RAPOR.md §0 lead-lag (satir 39-45)

## Elenenler

- **c0_leadlag.csv tum 108.286 test (FDR):** fdr10 ve fdr05 gecen satir 0; medyan net -17..-28 bp; t>3 yalniz 17; en yuksek t 3,67; en kucuk p 3,4e-4. _( sonuclar/c0_leadlag.csv )_
- **GERIDE (yetisme) turu genel:** 26.087 test, medyan -17,0 bp, %31 pozitif, t>3 yalniz 5 (SOXL<-USL, EWC<-DFII10, UDOW<-IWM, EWT<-SMH, XLK<-IWM); h1 medyani -12,7, h3 -20,7. _( sonuclar/c0_leadlag.csv )_
- **Hedefin kendi sinyali OWN_DN / OWN_UP (z<=-2 ya da >=+2):** 1.289 testte t>2,5 yok (max 2,14); medyan -20,7 / -28,2 bp. _( sonuclar/c0_leadlag.csv )_
- **L_DN (oncu dususu -> hedefi al):** 27.606 test, medyan -21,4 bp, yalniz %24 pozitif; t>3 yalniz 1. _( sonuclar/c0_leadlag.csv )_
- **VIX/GVZ/DFII10/T10YIE degisimi oncu satirlari (UGL, GLDM, SILJ, GDX, GDXJ, RING <- VIX_dlog L_DN; SIL <- GVZ; EWC/UDOW <- DFII10):** Oncu kapanisi ETF kapanisindan sonra (VIX 16:15 ET) ya da gunluk veri: C0'da kapanistan 10 dk once bilinemez; ayrica EWC<-DFII10 OOS t 0,08. _( RAPOR.md §9 zamanlama (satir 378); sonuclar/c0_leadlag.csv )_
- **Doviz gecikmeli oncu (FXE/FXF/FXY <- SPY/QQQ/DIA/HYG/LQD; UUP <- SPY ters):** lag_t 4-5 ama 1 sd basina 5-9 bp; kurala cevrilince net -14..-44 bp; z>=2 bile net negatif; maliyet 27 bp, likidite 5-10 mn $/gun. _( notlar/aile_tahvil_doviz.md satir 228-250; sonuclar/leadlag_sweep.csv )_
- **T10YIE (basabas enflasyon) -> QQQ/SMH/QLD/QYLD yetisme (3 gunluk catch_t 3,4-3,8):** Etki tamami 2020'den: 2020 haric t 0,75, OOS t ~0,4; SOXS/TECS/SQQQ ters ETF satirlari da ayni. _( notlar/aile_abd_endeks.md satir 229-232; sonuclar/leadlag_sweep.csv )_
- **SGOV/BIL yetisme bayraklari (t 4-11):** 1 sd basina 0,4-1 bp, maliyet 13-14 bp; eksik dagitim verisinin testere disi artefakti. _( notlar/aile_tahvil_doviz.md satir 252-258 )_
- **IGV<-QQQ/SPY ve KWEB<-EEM (negatif gecikmeli oncu):** Yalniz 'alma' filtresi; long-only icin kural degil: KWEB z>+1 sonrasi net -46,5 bp (t -3,73); IGV QQQ-kontrolunde t 0,17. _( notlar/denetim_sektor_tematik.md satir 28-29, 185-187 )_
- **IWM'in SPY'i izlemesi (IWM al, SPY IWM'den iyi gunden sonra):** Isaret ters: net -28 bp (h1), -89 bp (h3), kontrollu t -2,78. _( notlar/aile_abd_endeks.md AE13 satir 233-236 )_
- **SPY/QQQ dususu -> tek hisse 2x ETF (piyasa dusus gunu):** Yalniz QQQ O1 h1 +109 bp t 2,44; C0, C1 ve h2-3 anlamsiz; gercek ETF'te C0 negatif; ek lead-lag ailesinde FDR geciyor ama hepsi negatif isaretli piyasa-geri-donusu. _( notlar/aile_tek_hisse_kaldiracli.md satir 126 )_
- **BTC/Coinbase -> MSTR/COIN/MSTU ertesi gun; SMH->NVDA:** Onculuk yok (t -1,26/-0,98); BTC yalniz ertesi acilis boslugunu gosteren izleme araci (corr 0,88). _( notlar/aile_tek_hisse_kaldiracli.md satir 14, 127; notlar/aile_kripto.md satir 16 )_
- **Petrol->XLE/XOP yetisme (EN06), XOP<-UNG, CANE<-BNO:** XLE C0 h1 +50 bp t1,37 yalniz IS, kendi getirisi kontrolunde t 0,56; CANE net -25; XOP<-UNG t0,89 OOS negatif. _( notlar/aile_enerji_tarim.md satir 86, 92-95 )_
- **B8 USO alt Bollinger kirilimi:** C0'da net negatif (h1 -37,8 t-1,04; h2 -34,8; h3 -10,5); yalniz C1 h2 +108 t2,8 (C0 uyumsuz). _( sonuclar/c0_tablo.csv B8; RAPOR.md §3 B8 )_
- **F IBIT/BTC trend filtresi:** Strateji degil; C0 h1 -4,8 t-0,24, h2 -1,3, h3 +29,7 t0,57. _( sonuclar/c0_tablo.csv F; RAPOR.md §3 F )_
- **Kirilim/momentum (20 gunluk zirve), sektor rotasyonu, takvim etkileri (FOMC, CPI, OPEX, ay donumu):** Kirilim neredeyse her ailede negatif; asiri satilan sektoru al ters cikti (-14 bp t-2,2); takvimler maliyet sonrasi esik alti ya da negatif. _( RAPOR.md §4 (satir 232-239) )_
- **Dogalgaz/petrol/altin-gumus/VIX/kripto/tarim urunleri 1-3 gun long kurallari; ters ETF'li varyantlar:** Hicbiri maliyeti yenmiyor; BOIL gunluk -36 bp bozulma, VXX -9,6, UVXY -18; ters ETF varyantlari neredeyse hepsi net negatif. Tek saglam kural kacinma: UNG/BOIL long'u EIA raporuna tasima. _( RAPOR.md §4 (satir 188-243) )_
- **B4/B10 'alinan' ama gecikmeli oncu olarak sunulamaz:** Oncu ayni gun SPY dususu ya da hissenin kendi RSI'i; gun kumeli t 1,89 (B4) ve t 2,65 yalniz h3 (B10), her ikisi denetcide 'zayif'. _( sonuclar/c0_tablo.csv; notlar/denetim_uluslararasi.md satir 13; notlar/denetim_tek_hisse_kaldiracli.md satir 8 )_
- **Yuksek oynaklik rejiminde kaldiracli araclar (TQQQ, SOXL, NVDL, TSLL, KORU):** Rapor su an onermiyor: VIX 25,6, SMH 20g oynaklik %62 (10 yilin %97'lik dilimi); TQQQ tek islemde -%31, SOXL maxDD -%53. _( RAPOR.md §0 (satir 21-33), §8 (satir 344-347) )_

## Çelişkiler

- B4 sayilari uc farkli yerde farkli: RAPOR §3 '+57 bp (islem bazli t 3,2; gun kumeli t 1,9)'; c0_tablo.csv h1 '+52,9 bp, t 1,89 (gun kumeli, n=110)'; aile notu 'net +56 bp, NW t 2,22'; denetim 'gun kumeli basit t 1,99'. Tutarli sonuc: gun kumeli t ~1,9-2,0, esik altinda.
- B10 sayilari tanim farkindan ayrisiyor: RAPOR §3 'ETF sepeti +120 bp (t 2,7; gun kumeli 2,65) C0/O1/C1 = 120/104/98' (SMA5 cikisli, en gec 3 gun); c0_tablo.csv sabit tutusta h1 +37,4 t1,14, h2 +88,4 t2,14, h3 +127,6 t2,65; aile notu TH03 +111 bp t3,13 (605 islem, hisse bazinda). Headline t 2,65 yalniz h3 sabit tutusta; h1'de t 1,14.
- RAPOR §3 B2 'madenci havuzunda IS kaniti yok (t 0,5)' ama c0_tablo.csv B2 h3 IS +75,7 bp ve yil pozitif %80; kenar OOS'ta (+130). Havuz t'si ile kural t'si farkli olcu; IS'te kanit olmadigi cumlesi c0_tablo ile bire bir ortusmuyor.
- A1 C0: RAPOR §2 '+77 bp t 3,9' (kapanis fiyatiyla) ile denetim '76->56 bp (t 3,68->2,43)' (kapanis oncesi tahminle) farkli; RAPOR basligi C1 +68 bp'yi ana alir. Kullanicinin C0 duzeni icin gecerli sayi ~+56 bp, t ~2,4.
- RAPOR 'Lead-lag' ozetinde c0_leadlag.csv (108.286 test) hic anilmiyor; §10 dosya tablosu da onu listelemiyor: yalniz C1 hizali leadlag_sweep.csv (13.694 cift) anlatiliyor. C0 taramasi RAPOR'un hukmuyle ayni sonuca varsa da rapora girmemis; denetci yeniden uretimi yok.
- IWM-SPY yonleri: c0_leadlag'de GERIDE (SPY, IWM'in ima ettiginden geride -> SPY al) h3'te pozitif (+70 bp t2,67), aile notu AE13 ise ters yonu (SPY IWM'den iyi gun -> IWM al) net negatif buluyor. Farkli yon, dogrudan celiski degil; ama 'kucuk/buyuk hisse' iliskisi h1'de negatif, h3'te pozitif ve tutarsiz.
- Kullanicinin 'sans beklentisinin altinda' cikarimi dosyayla desteklenmiyor: t dagilimi maliyet nedeniyle negatife kaymis (medyan t -0,64; yalniz %28 t>0), bu yuzden N(0,1) beklentisi gecerli degil. Sonuc (FDR gecen yok) dogru, gerekce farkli.
- Kullanicinin 'XLK->WCLD ONDE h2' satiri n=33 ile en kucuk orneklem (t 3,67 ama p 4,4e-4, 33 islem); WCLD kartlarda/izleme listesinde ayri bir dogrulama yok.
- sonuclar/leadlag_sweep.csv'de 'dogru oncu' FDR bayraklari (43 lag h1, 110 catch h3, 2 catch h1) RAPOR'la uyumlu, ama RAPOR 'FDR'yi geçen 43 bayrağın çoğu döviz' diyor; listede ayrica DBB<-KWEB (lag_t 4,04, OOS 3,20) var ve rapor bunu ayri anmiyor.

## Açık kalanlar

- c0_leadlag.csv'de sinyal z-esigi kapanisa ~10 dk kala sinir gunlerinde modellenmedi (kapanis fiyatiyla hesaplandi); A1 icin bu duyarlilik 76->56 bp olarak olculmustu, lead-lag icin yok.
- c0_leadlag.csv icin 2024-26 'son donem' kirilimi yok (IS=2016-2021, OOS=2022-2026); son_donem alani bos birakildi.
- c0_leadlag satirlari icin denetci yeniden uretimi, islem-bazli yil kirilimi ve kumeli (ayni sinyal gunu) t yok; birden fazla hedefin ayni sinyal gununu paylastigi (ornek IWM kumesi, URNM, SOXL/SMH/SOXX) satirlar bagimsiz sayilmamali.
- Benim IS-secili OOS kontrolum (IS t>3 -> OOS medyan -42 bp, %22 pozitif) dosyadan yaptigim ozet hesap; calismanin kendi raporunda yok.
- Midas'ta bulunurluk: SOXL, UDOW, URNM, TAN, RING, WCLD, YANG, NUGT, JNUG, KORU, NVDL, TSLL vb. dogrulanamadi (resmi sembol listesi yok; 1x ETF'ler dahil hicbiri resmen dogrulanamadi); yalniz TQQQ 'muhtemel'. Uygulamada arayarak teyit gerekir.
- Midas BSMV ve USD/TL kur makasi maliyete dahil degil (yayimlanmiyor); 1,5 $/emir uzerine BSMV eklenip eklenmedigi dogrulanamadi.
- Kesirli emrin uzatilmis saatte (after-hours) kabul edilip edilmedigi belirsiz; A2 icin tam adet onerisi bundan.
- Oncu/hedef TradingView borsa onekleri yalnizca dosyada acikca gecenler icin yazildi (NASDAQ:QQQ, NASDAQ:SMH, NASDAQ:TLT, AMEX:EWY/EWT/FXI/EWJ/GDX/GDXJ/GLD/SPY/ASHR vb.); XLK, WCLD, URNM, TAN, RING, SIL, YANG icin kart/tv_etf.csv okunmadi.
- B4 sepetinin ETF<=SPY kosulunun kod ayrintisi (kod/ajan_uluslararasi/strateji_S1_ul03_asya.py) ve B10'un esit pay hesabi kodu okunmadi; tanim kurallar.py ve aile notlarindan alindi.
- kartlar/<SYM>.md ve notlar/denetim_* dosyalarinin yalniz lead-lag ilgili bolumleri tarandi; tum satir ici lead-lag kurallari (Y2/Y2b KWEB esik kurallari, 225 sektor lead-lag kurali) tek tek okunmadi.
- Max t'nin saf gurultu altindaki beklentisi (~4) kabaca bilinen normal-maksimum yaklasimidir; dosyada permutasyon tabanli bir referans yok.
