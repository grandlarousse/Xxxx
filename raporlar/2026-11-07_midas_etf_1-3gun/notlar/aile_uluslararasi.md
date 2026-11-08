# Aile: uluslararası (68 ETF) — 1-3 günlük işlem, Midas koşullarıyla

Hazırlanma: 07.11.2026. Veri: 2016-11-07 .. 2026-11-06 (IS = ..2021, OOS = 2022..). Tüm getiriler toplam getiri düzeltmeli.
Maliyet: Midas 2 x 1,5 USD + kademeli makas (`lib.cost_bp`; 2.500 $ pozisyonda bu ailede 13-47 bp gidiş-dönüş).
Sonuçların makinece okunur özeti: `sonuclar/aile_uluslararasi/sonuc.json`.

## 0. Kısa sonuç

* Genel kütüphanede (IBS, RSI2, takvim, VIX rejimi; 297 sinyal x mod x ufuk) **aile genelinde tutarlı ve FDR'den geçen sinyal yok.**
  Ülke ETF'lerinde IBS etkisi (Pandey & Joshi 2023, maliyetsiz) brüt 5-9 bp; maliyet (~15 bp) sonrası negatif.
* **Tek aday strateji: `uluslararasi_S1` (UL03).** SPY'ın günlük getirisi <= -%1,5 olan günde, SPY'dan daha çok düşen Asya ETF'lerini
  (EWJ, EWY, EWT, FXI, EWA, EWH) kapanışta al, ertesi gün kapanışta sat. Sepet: 110 sinyal günü, brüt +70 bp, **net +56 bp** (2.500 $),
  t 2,22, IS +68 / OOS +46 bp, yılların %78'i pozitif. Mekanizma testleri (plasebo, aynı gün eşleştirme) tutarlı. **Güven: orta** —
  kapanışa bağımlı, getiri yüksek oynaklık yıllarında yoğun, tüm varyantlarla birlikte FDR'yi geçmiyor.
* `uluslararasi_S2` (EWY'de IBS<0,10 ve düşüş günü -> ertesi gün dönüş): eşiği biçimsel olarak geçiyor (t 2,93, IS/OOS > 0) ama
  taramadan seçildi ve FDR'yi geçmiyor. **Güven: düşük (keşifsel).**
* **Doğrulanmış (doğrusal) gecikmeli öncü yok.** Aile içi 2.685 hedef-öncü çiftinde lag_t_h1/h3 için BH-FDR (q=0,10) geçen çift yok.
* İzleme: **kabul** EWY, EWT, FXI, EWJ; **yedek** EWA, EWH, EEM, IEMG, EFA, VGK, EWZ, INDA, ASHR, CQQQ, KORU, YINN; geri kalan 52 ETF red.
  TUR (Türk yatırımcı için ilginç) ince: medyan 6,8 mn $/gün, tahmini gidiş-dönüş 27 bp (1.000 $'da 45 bp) -> red.

## 1. Yöntem

1. **İşlenebilirlik** (`kod/ajan_uluslararasi/a1_islenebilirlik_genel.py`, çıktı `islenebilirlik.csv`): tarama.csv'den medyan dolar hacim,
   makas, maliyet, oynaklık. 33 ETF >= 20 mn $, 9 ETF 10-20 mn $, 26 ETF < 10 mn $.
   Kopya grupları (ilk eleman temsilci): EM (EEM ~ VWO, IEMG; EDC/EDZ 3x), EAFE (EFA ~ VEA, IEFA), Avrupa (VGK ~ EZU; EURL 3x),
   Çin büyük (FXI ~ MCHI; YINN/YANG 3x), Çin A (ASHR; CHAU 2x), Japonya (EWJ ~ DXJ kur korumalı), Brezilya (EWZ; BRZU 2x; ILF örtüşür),
   Meksika (EWW; MEXX 3x), Hindistan (INDA ~ EPI; INDL 2x), Kore (EWY; KORU 3x). Bağımsız likit (>= 10 mn $) 1x temsilci: 29 ETF.
2. **Aile havuzu testi** (`a2_aile_havuz.py`): strategies.LIB'in 31 sinyali x C0/O1/C1 x h=1,2,3 (+ erken çıkış) = 297 kombinasyon,
   29 bağımsız temsilcide. İşlemler **sinyal tarihine göre kümelendi** (aynı gün işlem yapan ETF'lerin ortalaması = 1 gözlem) ve
   Newey-West t hesaplandı. Bu, ETF başına t'leri toplamanın (Stouffer) ortak EM faktörünü kaç kez saydığı sorununu giderir:
   ör. 'tatil öncesi C1 h=3' ETF başına Stouffer 6,9 iken gün-kümeli t 1,69.
3. **Aile hipotezleri** (`a3_hipotezler.py`): hipotezler.csv UL01-UL06 + yönlendirme (Asya <- SPY/QQQ, KWEB -> EM, EWZ <- USO, DXJ).
   Kurallar önceden sabit (literatür/yuvarlak eşik); her hipotez x mod x h bir test (135 test).
4. **UL03 sağlamlık** (`a4_ul03_saglamlik.py`, 108 test): ETF bazında, plasebo (eşzamanlı Amerika, Avrupa, SPY'ın kendisi), tümleyen
   (aynı gün SPY'dan az düşenler), komşu eşikler (yalnız rapor), 2020 hariç, listede olmayan 6 Asya ETF'i, kaldıraçlı uygulama.
5. **IBS x bölge** (`a5_ibs_bolge.py`, 24 havuz testi): IBS dönüşünün eşzamansızlıkla (Asya/Avrupa/Amerika) ilişkisi ve EWY ayrıntısı.
6. **Lead-lag**: `sonuclar/leadlag_sweep.csv` aile satırları (56 hedef x 48 öncü = 2.685 çift) incelendi; aile içi BH-FDR yeniden hesaplandı;
   'yetişme' sinyali kural olarak (UL04v) ve öncünün kendi gecikmesine ek katkısı (lag testi + KWEB eşik kuralları Y2/Y2b) ayrıca sınandı.
7. **FDR**: tek yönlü p (H1: net > 0) ile BH q=0,10. Not: iki yönlü p ile çok sayıda anlamlı NEGATİF sonuç BH eşiğini gevşetiyor;
   genel_tum aile satırlarında iki yönlüde 22 'geçen' görünürken tek yönlüde 0.

**Toplam test**: 297 + 135 + 108 + 24 = **564 havuz testi** (kendi kodum) + incelenen 20.196 genel_tum aile satırı + 2.685 x 4 lead-lag istatistiği.

## 2. Bulgular

### 2.1 Genel kütüphane — aile havuzu (`aile_havuz_genel.csv`)
Hiçbir kombinasyon FDR'yi geçmedi; en yüksek gün-kümeli t'ler: CA_tatil_oncesi C1 h=3 (t 1,69; mekanizmasız: tatil SONRASI giriş),
CA_ay_sonu C0 h=3 (ay sonu kapanışı -> yeni ayın 3. günü; brüt 46 bp, net 29 bp, t 1,38, OOS +4 bp). IBS/RSI2 ailesinde O1 ve C1 modları
sistematik olarak negatif; C0'da brüt 5-19 bp (maliyetin altında ya da ancak eşit).

### 2.2 Aile hipotezleri (birincil spesifikasyon; `hipotez_havuz.csv`)

| Hipotez | ETF | gün | brüt bp | net bp | t | IS net | OOS net | Sonuç |
|---|---|---|---|---|---|---|---|---|
| UL01 ülke IBS<0,2 (C0 h1) | 10 | 1.288 | 8,6 | -8,9 | -2,2 | -0,5 | -17,3 | red |
| UL02 kesitsel en düşük IBS 3 (C0 h1) | 17 | 2.313 | 8,1 | -8,3 | -3,1 | -6,1 | -10,2 | red |
| **UL03 SPY<=-%1,5 ve ETF<=SPY, Asya (C0 h1)** | 6 | 110 | **70,4** | **55,8** | **2,22** | 68,0 | 45,7 | **aday (S1)** |
| UL04v SPY'a göre kalıntı z<=-2 (C0 h1) | 29 | 789 | 6,0 | -11,5 | -1,8 | -9,2 | -14,0 | red |
| UL05 ay dönümü (C0 h3) | 9 | 111 | 9,8 | -5,1 | -0,4 | -9,5 | -1,2 | red |
| UL06 FOMC öncesi (C0 h1) | 5 | 73 | 21,1 | 7,0 | 0,5 | 6,0 | 7,9 | red |
| Y1 SPY z<=-2 -> Asya (C0 h1) | 6 | 88 | 30,1 | 15,7 | 0,8 | 25,3 | 7,0 | red |
| Y2 KWEB z>=1 -> EM/Asya (C0 h1) | 10 | 338 | -2,2 | -18,0 | -2,1 | -21,4 | -14,7 | red |
| Y3 USO z>=1,5 -> EWZ (C0 h1) | 2 | 137 | 0,0 | -15,6 | -0,8 | -16,8 | -14,4 | red |

Birincil 6 literatür hipotezi içinde BH q=0,10: yalnız UL03 geçer (tek yönlü p=0,013 <= 0,1/6). 564 havuz testinin tamamı içinde geçmez.

### 2.3 uluslararasi_S1 ayrıntı (`strateji_S1_ul03_asya.py`, `S1_*.csv`, `ul03_*.csv`)

* **Mod sağlamlığı** (sepet, brüt bp): h=1 C0 70 / O1 13 / C1 40; h=2 C0 87 / O1 53 (net 38, t 1,76) / C1 31. O1/C1'de brüt pozitif
  ama kenarın çoğu t kapanışı -> t+1 açılışı arasındaki gece boşluğunda -> **ağırlıkla kapanışa bağımlı.**
* **Maliyet** (C0 h1 net): 1.000 $ 37,8 bp (t 1,51) / 2.500 $ 55,8 (t 2,22) / 10.000 $ 64,8 (t 2,58).
* **Mekanizma** (Levy & Lieberman 2013: eşzamansız saatlerde ETF fiyatı S&P'ye aşırı tepki verir):
  aynı SPY düşüş günlerinde SPY'dan daha çok düşen Asya ETF'leri, az düşenlerden ertesi gün +39,7 bp daha iyi (t 2,88);
  Asya, eşzamanlı Amerika ETF'lerinden +43,8 bp daha iyi (t 2,40). Plasebolar (brüt C0 h1): Amerika 21,5, Avrupa 17,3, SPY'ın kendisi 24,2,
  tümleyen (ETF>SPY) 22,1 bp.
* **Kesitsel tekrar**: listede olmayan 6 Asya ETF'i (INDA, EWS, ASHR, CQQQ, EIDO, VNM) net +35 bp (t 1,71; IS +48 / OOS +20).
* **ETF bazında** C0 h1 net: EWY +108 (t 2,41), EWT +63 (2,00), FXI +37 (1,17), EWJ +30 (1,21), EWA +51 (0,97; OOS -8), EWH +49 (1,54).
* **Yoğunlaşma**: 2020 hariç net 41 bp (t 1,78); 2020 ve 2026 hariç 21 bp (t 1,03). VIX>=25 günleri 65 bp, VIX<25 günleri 46 bp.
* **Komşu eşikler** (seçim için değil): -%1,0 net 28 bp (OOS 15); -%2,0 net 75 bp (OOS 2). Eşik -%1,5 literatür değeri; değiştirilmedi.
* **Kaldıraçlı uygulama** (sinyal dayanaktan): KORU<-EWY C0 h1 net +257 bp (t 1,95), h2 +337 (t 2,12), en kötü -3.776 bp;
  YINN<-FXI C0 h1 t 1,25, h2 +336 (t 2,27); CWEB<-KWEB h1 +145 (t 2,33; ince). Birincil spesifikasyonda t<2 -> yalnız alternatif araç.

### 2.4 uluslararasi_S2 (keşifsel; `strateji_S2_ewy_ibs.py`)
EWY: n=214, brüt 55, net 42 bp, t 2,93, IS +26 / OOS +53, O1 brüt 18 (net 5), C1 brüt 1. Aynı kural 29 likit ETF'te: net pozitif oranı 0,48,
t>=2 yalnız EWY. EWY'yi ayıran: ailenin en düşük maliyet/oynaklık oranı (0,034) ve güçlü negatif 1 günlük otokorelasyon (IS -0,16, OOS -0,12;
gün içi getiri ile ertesi gece boşluğu korelasyonu -0,11/-0,14). Getirinin yarıdan fazlası 2026 ve 2020'den. FDR yok -> düşük güven.

### 2.5 Lead-lag
* **Eşzamanlı sürücüler** (öncü değil): EWY/EWT/EEM <- SMH, QQQ, XLK, EEM (corr_1y 0,8-0,93); FXI <- KWEB (0,88); EWJ <- EEM, SPY;
  EFA/VGK <- DIA, SPY, EWJ; EWZ zayıf bağlı (EEM 0,41); INDA <- petrol ters (BNO -0,60). Ayrıntı `sonuc.json` -> leadlag.
* **Gecikmeli öncü**: aile içi BH-FDR geçen yok. Tarama-genelinde FDR geçen iki çift (DXJ <- QQQ ters; CWEB <- EEM ters) eşik kuralına
  çevrildiğinde kâr yok (DXJ) ya da araç ince (CWEB). KWEB(t)'nin EEM/FXI/Asya(t+1) üzerindeki pozitif kısmi katsayısı (t~3,4, IS/OOS aynı
  işaret) kendi gecikmesine koşullu; tek başına kural olarak ters işaretli (KWEB düşüşü sonrası EEM ertesi gün +11 bp) -> kullanılamaz.
  Reel faiz (DFII10 düşüşü / TIP yükselişi) -> EWY/EWT/EWJ 3 gün: IS/OOS aynı işaret, FDR yok (keşifsel izleme).
* **Yetişme (catch)** testindeki 78 FDR sonucu (EWY, UAE, EDZ...) ilgisiz öncülerle (UNG, DBA, TIP) de çıktığı için ETF'in kendi 1 günlük
  dönüşünü yansıtır; öncünün katkısı lag testinde (kendi gecikmesi kontrollü) yok. Kural hâline getirilmiş kalıntı dönüşü (UL04v) maliyet sonrası negatif.
* **Gerçek zamanlı izleme** (ETF açılış boşluğunu önceden gösterir, öncü değil): OSE:NK2251!, TVC:NI225, FX_IDC:USDJPY (EWJ);
  KRX:KOSPI, CME_MINI:NQ1! (EWY/KORU); HKEX:HSI1!, TVC:HSI, FX:USDCNH, SGX:CN1! (FXI/YINN/EWH/CQQQ); SSE:000300 (ASHR);
  EUREX:FDAX1!, TVC:SX5E, TVC:UKX, FX:EURUSD (EFA/VGK); BMFBOVESPA:IBOV, FX_IDC:USDBRL, ICEEUR:BRN1! (EWZ); NSE:NIFTY (INDA);
  TUR için BIST:XU100, FX_IDC:USDTRY. Doğrulanmamış kodlar `sonuc.json` -> tv_dogrulanacak.

## 3. Strateji kuralları (TradingView'da uygulanabilir)

**uluslararasi_S1** — Günlük grafik, temettü düzeltmesi (ADJ) açık.
`spy = request.security("AMEX:SPY","D", close/close[1]-1)`; her ETF (AMEX:EWJ, AMEX:EWY, AMEX:EWT, AMEX:FXI, AMEX:EWA, AMEX:EWH) için
`sig = spy <= -0.015 and (close/close[1]-1) <= spy`. Sinyal olan ETF'leri eşit tutarla ABD kapanışına ~10-15 dk kala al
(kış TR 23:45-23:50; yaz TR 22:45-22:50) ya da kapanış sonrası after-hours limit emri (kış TR 00:00-04:00); ertesi işlem günü kapanışına
~10 dk kala sat. Çıkış günü yeniden sinyal varsa tut. Kapanış kaçırılırsa: t+1 açılışında (kış TR 17:30) al, h=2 tut (O1 h=2 net +38 bp, t 1,76).

**uluslararasi_S2 (keşifsel)** — AMEX:EWY: `ibs=(close-low)/(high-low)`, `sig = ibs < 0.10 and close < close[1]`; kapanışa ~5-10 dk kala al,
ertesi gün kapanışında sat. İsteğe bağlı araç AMEX:KORU (3x; Midas bulunurluğu doğrulanmadı).

Betikler (çalıştırınca sayıları basar):
`python3 -I kod/ajan_uluslararasi/strateji_S1_ul03_asya.py` ve `python3 -I kod/ajan_uluslararasi/strateji_S2_ewy_ibs.py`.
Tüm zincir: a1 -> a2 -> a3 -> a4 -> a5 -> strateji_S1 -> strateji_S2 -> a6 (sonuc.json).

## 4. İzleme listesi (kabul / yedek)

| ETF | Karar | TV | Medyan $ hacim (mn) | Maliyet bp (2.500$) | 1g oynaklık bp | Neden |
|---|---|---|---|---|---|---|
| EWY | kabul | AMEX:EWY | 2.361 | 13,0 | 378 | S1 en güçlü üye, S2 aracı; maliyet/oynaklık 0,03 |
| FXI | kabul | AMEX:FXI | 872 | 14,9 | 122 | S1 üyesi; MCHI kopya |
| EWJ | kabul | AMEX:EWJ | 482 | 14,0 | 140 | S1 üyesi (tek başına zayıf); gerçek zamanlı izleme kolay |
| EWT | kabul | AMEX:EWT | 450 | 14,0 | 221 | S1 üyesi (t 2,00) |
| EEM | yedek | AMEX:EEM | 1.617 | 13,7 | 166 | EM ölçütü; strateji yok (S1 kuralı t 1,6) |
| EFA | yedek | AMEX:EFA | 1.518 | 13,0 | 104 | likit ama düşük oynaklık; strateji yok |
| EWZ | yedek | AMEX:EWZ | 977 | 15,1 | 222 | likit, oynak; strateji/öncü yok |
| IEMG | yedek | AMEX:IEMG | 897 | 14,0 | 161 | EEM kopyası |
| KORU | yedek | AMEX:KORU | 405 | 26,5 | 1.104 | EWY sinyaliyle 3x uygulama aracı |
| INDA | yedek | CBOE:INDA | 299 | 14,0 | 102 | S1 kuralı pozitif ama OOS negatif |
| VGK | yedek | AMEX:VGK | 234 | 14,0 | 105 | Avrupa temsilcisi; strateji yok |
| ASHR | yedek | AMEX:ASHR | 148 | 16,0 | 115 | S1 genişletilmiş kontrolde pozitif |
| EWA | yedek | AMEX:EWA | 86 | 16,0 | 117 | S1 üyesi, OOS negatif |
| EWH | yedek | AMEX:EWH | 67 | 16,3 | 110 | S1 üyesi |
| YINN | yedek | AMEX:YINN | 56 | 16,0 | 362 | FXI sinyaliyle 3x uygulama aracı |
| CQQQ | yedek | AMEX:CQQQ | 46 | 20,0 | 194 | S1 genişletilmiş kontrolde pozitif |

Red gerekçeleri (52 ETF) `izleme.csv`'de: kopyalar (VWO, VEA, IEFA, EZU, MCHI, EPI, DXJ), strateji yok (EWW, EWC, ILF, Avrupa tek ülkeleri...),
likidite < 10 mn $ (26 ETF; TUR, EIS, EDC, BRZU, INDL, EURL, MEXX, CHAU...).

## 5. Elenenler (özet)
UL01/UL02 IBS (maliyet), UL04 kalıntı/yetişme (kendi dönüşü, maliyet sonrası negatif; Avrupa'da devam), UL05 ay dönümü (OOS yok), UL06 FOMC öncesi
(drift yok), koşulsuz büyük ABD düşüşü sonrası Asya alımı (Y1; t 0,75), DXJ/QQQ ters gecikmesi (kural kârsız), KWEB->EM (işaret sorunu),
USO->EWZ (yok), genel kütüphanenin 297 kombinasyonu (havuzda FDR yok), kaldıraçlıların kendi sinyalleri, 26 ince ETF, kopyalar.

## 6. Sınırlamalar
* C0 girişi kapanış fiyatıyla hesaplandı; gerçekte emir kapanıştan dakikalar önce ya da after-hours'ta verilir (S1/S2 kapanışa bağımlı).
* iNAV/NAV verisi yok: prim/iskonto hipotezi (UL04) yalnız SPY kalıntısı vekiliyle test edildi.
* Makas kademeli tahmin; stres günlerinde (S1'in tetiklendiği günler) gerçek makas daha geniş olabilir.
* S1 seyrek (yılda ~11 gün) ve getirisi oynak dönemlerde yoğun; 2018 ve 2024 negatif. Tek bir yılda tekrar etmeyebilir.
* Kaldıraçlı/ters ürünlerin Midas'ta bulunurluğu resmî olarak doğrulanmadı; 3x ürünlerde tek günde -%30..-40 mümkün (KORU son 1 yılda -%42).
* Bu ailede PTP/K-1 ürünü yok (1446(f) stopaj riski bu aileyi ilgilendirmiyor).
* Yerel tatillerde (Ay Yeni Yılı vb.) ETF NAV'sız işlem görür; sinyal o günlerde güvenilmez olabilir.
