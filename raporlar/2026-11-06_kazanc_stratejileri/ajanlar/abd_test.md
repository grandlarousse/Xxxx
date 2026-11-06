# ABD swing stratejileri: kendi backtestlerimiz (2026-11-06)

Kapsam: Test 2 (kaldiracli trend), Test 1 (momentum / sektor rotasyonu), Test 3 (Chen-Zimmermann ~212 anomalinin yayin sonrasi bozulmasi), Test 5 (kisa vade reversal, PEAD bozulmasi), ek olarak TL carry engel orani, momentum x kaldirac x trend kombinasyonu ve kayan pencere analizi. Test 4 (earnings gap / episodic pivot) yapilamadi (asagida neden).
Kod: `/home/user/Xxxx/raporlar/2026-11-06_kazanc_stratejileri/hesaplar/abd_test/` (ortak.py, test1..test7, cikti/ altinda CSV ve tablolar). Ham veri repo disinda (scratchpad/data).

## 0. Yonetici ozeti (sayilarla)

1. **ABD'de buyuk swing getirisinin kamuya acik verilerde gorulen tek tutarli kaynagi "kaldiracli beta + trend filtresi"dir, alfa degil.** Sentetik 2x/3x gunluk-rebalans endekslerde 200-DMA filtresi uzun donemde CAGR'yi artirip MaxDD'yi dusurdu (piyasa 3x: BH 10.6% / -100% -> 200DMA 20.8% / -78%, 1927-2026, lag0; lag1 ile 17.9% / -85%). Ama **2010-2026'da filtre her kaldiracta getiriyi dusurdu** (piyasa 3x: BH 27.8% vs 200DMA 18.5-19.3%; NDX 3x: 35.6% vs 24-26%). Filtre bir sigorta; son 16 yilda primi odendi, sigorta tazminati (2000-02, 2008 tipi uzun ayi) gelmedi.
2. **3x Nasdaq-100 + 200DMA 2000-02'de koruma saglamadi**: pencere getirisi -89% (pencere ici MaxDD -94%), tam donem MaxDD -97% (lag0) / -88% (lag1). Volatil ayi piyasasinda whipsaw, filtreyi etkisizlestiriyor. 2x NDX + 200DMA: 2000-02'de -71%.
3. **Kayan 5 yillik pencerede** (1990+): NDX 2x+200DMA medyan 18.2%, P10 2.8%, %5.7 negatif, %61.6 olasilikla >%15; NDX 3x+200DMA medyan 22.1%, P10 -0.6%, %10 negatif. Piyasa 2x+200DMA medyan 12.9-13.9%. Yani USD'de %15+ hedefi ancak kaldiracla, yaklasik yazi-tura olasilikla ve -40..-90% arasi drawdown kabul ederek yakalaniyor.
4. **Momentum faktoru (UMD, uzun-kisa) 2000 sonrasi neredeyse oldu**: UMD+RF CAGR 2000-2026 2.8%, 2010-2026 4.0% (T-bill'in ~2.6 puan ustu), Sharpe 0.14-0.26. Vol-yonetimli UMD tam ornekte Sharpe'i 0.45 -> 0.81'e cikardi (Barroso-Santa-Clara replikasyonu), ama 2010-2026'da sadece 6.1% CAGR / Sharpe 0.46.
5. **Sadece-uzun momentum (VW ust desil)** 2010-2026 17.8% vs piyasa 14.1% (Sharpe 0.79 vs 0.87, MaxDD -31% vs -25%). Getiri farki var ama risk-ayarli fark yok; 2000-2026'da 10.9% vs 8.5%.
6. **Sektor/endustri rotasyonu (sektor ETF vekili)**: 49 endustri top-N izgarasinin (24 kombinasyon) medyani 2010-2026'da 14.2% vs piyasa 14.1% (fark +0.1 puan, kombinasyonlarin %50'si piyasayi geciyor); 12 endustride +0.5 puan. 1927-2026 ve 2000-2026'da +2..+4 puan ve tum kombinasyonlar piyasanin ustunde. 2020-2026'da +1..+2 puan (enerji 2021-22, yari iletken/AI 2023-25 rejimi). Kaldiracsiz %15-20 USD hedefini guvenilir sekilde vermiyor.
7. **Chen-Zimmermann 212 anomali**: medyan uzun-kisa getiri IS 0.60%/ay -> yayin sonrasi 0.24%/ay (oran 0.38; havuzlanmis 0.45). 2010-2025 medyani 0.20%/ay (~2.4%/yil, maliyet oncesi); likidite filtresiyle (ME > NYSE 20. persantil) 0.13%/ay, deger-agirlikli versiyonda 0.07%/ay. 2010 sonrasi en iyi aile: momentum/trend (0.51%/ay ort.), likidite/hacim, value, kalite; en kotuler: uzun vade reversal (0.05), kisa vade reversal VW'de negatif.
8. **PEAD / kazanc olayi sinyalleri** uzun-kisa olarak hala pozitif (AnnouncementReturn 2010-19: 0.72, 2020-25: 0.37%/ay; EarningsStreak 0.41/0.97) ama bu getirinin cogu kucuk hisselerde ve kisa bacakta. **Sadece-uzun ust portfoy, VW piyasaya karsi 2010-2025'te ~0** (AnnouncementReturn -1.4%/yil, EarningsStreak +0.7%, REV6 -1.0%, EarningsSurprise -0.7%); boyut etkisi ayiklaninca (ust portfoy - ayni sinyalin tum portfoylerinin ortalamasi) -0.2..+2.7%/yil (OP versiyonlarinda AnnouncementReturn t=3.3, EarningsStreak t=2.7, RevenueSurprise t=2.4; likidite filtreli versiyonlarda t<2). Bir swing trader'in "earnings sonrasi guclu hisseyi al" yaklasiminin akademik cekirdegi 2010 sonrasi kucuk ve VW endeksi gecmiyor.
9. **Kisa vade reversal (aylik, French ST_Rev)** 2010-2026 brut 0.1%/yil (t=0.04), 2020-2026 -5.2%/yil; makul maliyetle net -2..-9%/yil. Oldu.
10. **Engel orani gercegi**: TL para piyasasi carry'si USD bazinda son 12 ayda ~+22.5% (brut, stopaj oncesi) ama 2010-2026'da **-7.2%/yil, MaxDD -85%**; 2020-2026 -10.1%/yil. "Risksiz %40-50" USD bazinda risksiz degil; rejime bagli bir carry trade ve kendisi de devaluation kuyruk riski tasiyor.

Durust sonuc: kamuya acik, belgelenmis ABD swing anomalileri ile kaldiracsiz USD %15-20 surekli getiri **bu verilerde yok**. %15-25 bandi, ancak (i) kaldiracli endeks + trend filtresi veya (ii) momentum/sektor rotasyonu + kaldirac ile, -40%..-90% drawdown ve 2-5 yillik kotu pencereler kabul edilerek goruluyor. Bunun kaynagi alfa degil, kaldiracli hisse senedi risk primi + 2010-2026 teknoloji rejimi.

## 1. Veri, varsayimlar, yanliliklar

| Veri | Kaynak (URL) | Tur | Donem | Not |
|---|---|---|---|---|
| CRSP VW piyasa (Mkt-RF+RF), gunluk/aylik, temettu dahil | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html (F-F_Research_Data_Factors[_daily]) | akademik veri (CRSP) | 1926-07..2026-09 | S&P 500 TR vekili (S&P degil; tum NYSE/AMEX/Nasdaq VW) |
| Momentum (Mom) aylik + gunluk, ST_Rev aylik + gunluk | ayni kutuphane | akademik | 1927-01..2026-09 | 2x3 VW, uzun-kisa |
| 10 Prior(12-2) portfoyu, 49 ve 12 endustri VW (aylik, 49 gunluk) | ayni kutuphane | akademik | 1926-07..2026-09 | |
| Nasdaq-100 fiyat endeksi | https://fred.stlouisfed.org/series/NASDAQ100 | endeks (fiyat) | 1986-01-02..2026-11-05 | temettu YOK -> sabit +0.7%/yil eklendi (yaklasik) |
| 3-ay T-bill (DTB3), Fed funds (DFF, DFEDTARU) | https://fred.stlouisfed.org/series/DTB3 , /DFF , /DFEDTARU | resmi | ..2026-11-04 | DTB3 4.03%, DFF 3.88%, hedef ust sinir 4.00% (2026-11-04/05) |
| TR gecelik faiz, USD/TRY aylik ortalama | https://fred.stlouisfed.org/series/IRSTCI01TRM156N , /CCUSMA02TRM618N | OECD/IMF via FRED | ..2026-08/09 | TL carry hesabi icin |
| Chen-Zimmermann OpenAP, Data-Release-2026.10 | https://huggingface.co/datasets/OpenSourceAP/CrossSection (PredictorLSretWide, PredictorPortsFull, LiqScreen_ME_gt_NYSE20pct, LiqScreen_VWforce, SignalDoc.csv) ; https://www.openassetpricing.com/data/ | akademik replikasyon (peer-reviewed: Chen & Zimmermann, Critical Finance Review 2022) | 1926..2025-12 | opsiyon tabanli 7 sinyal 2022-12'de bitiyor |

**Varsayimlar**
- Sentetik LETF gunluk getirisi = L*r - (L-1)*(rf + spread) - ER; spread T-bill+0.5% ve +1.0% (ana tablo +1.0%), ER 0.9% (UPRO/TQQQ ~0.84-0.95% bandi), 1x icin ER 0.1%. Gunluk -%99.9 taban.
- Sinyal t gunu kapanisinda hesaplanir, getiri t+1'den (lag0) veya t+2'den (lag1) itibaren uygulanir. Disarida T-bill (French 1-ay RF; 2026-09 sonrasi DTB3). Gecis basina 10 bp (izgara: 0/10/25 bp).
- MKT icin MA sinyali toplam getiri endeksinden (fiyat endeksi yok) hesaplandi; temettu drifti nedeniyle sinyal hafifce "iceride" tarafina kayar.
- Endustri momentumu: t ay sonu, son K ay (skip ay atlamali) log-getiriye gore ilk N endustri, esit agirlik, t+1 ay tutulur; devir * 10 bp maliyet.
- Tum getiriler USD, vergi oncesi. Turk mukimi icin vergi, kur ve aracı kurum maliyetleri dahil degil.

**Yanliliklar / sinirlar**
- Sentetik LETF ile gercek LETF arasinda swap maliyeti, takip hatasi, gun-ici likidite farki var. Kontrol: sentetik 3x NDX 2022 takvim yili -79%; TQQQ'nun bilinen 2022 getirisi de yaklasik -79% (bellekten; bu oturumda web aramasi butcesi tukendigi icin dogrulanamadi). 1987 ve 2000-02 icin gercek 3x urun yoktu; o donem sonuclari varsayimsal.
- 2010-2026 alt donemi ABD tarihinin en guclu boga donemlerinden biri; BH lehine yanli. 1926-2026 ornegi ise 1929-32 gibi bir daha olmayabilecek bir cokusu iceriyor.
- Izgara medyanlari raporlandi; tek "en iyi" parametre secilmedi. Yine de MA/10-ay kurallari literaturden onceden bilinen kurallar; tamamen "temiz" OOS degil.
- CZ portfoyleri OP (orijinal makale) tarzi; cogu esit agirlikli ve mikro-cap iceriyor, maliyet oncesi; uygulanabilir getiri daha dusuk.
- Endustri portfoyleri yatirilabilir ETF degil (49 endustrinin bir kismi cok az hisseli); 12 endustri SPDR sektorlerine daha yakin vekil.
- Web arama butcesi bu oturumda tukendigi icin literatur atiflari (McLean-Pontiff, Barroso-Santa-Clara vb.) bellekten verildi ve "dogrulanmadi" isaretli; tum sayisal sonuclar ise burada listelenen ham veriden yeniden uretilebilir.

## 2. Engel orani: TL carry'nin USD getirisi (Test 6a)


**(a) TL para piyasasi carry'sinin USD getirisi (brut, stopaj/vergi oncesi; aylik ortalama kur ile yaklasik)**

| Donem | Ay | USD_CAGR | TL_faiz_ort | USDTRY_degisim_yillik | TL_bilesik_yillik | MaxDD |
|---|---|---|---|---|---|---|
| 2010-2026 | 191 | -7.2% | 14.6% | 24.3% | 15.3% | -85.1% |
| 2015-2026 | 131 | -8.9% | 18.9% | 32.1% | 20.3% | -80.0% |
| 2020-2026 | 71 | -10.1% | 25.6% | 42.6% | 28.3% | -70.6% |
| 2023-07..2026-08 (ortodoks donus) | 34 | 6.2% | 40.5% | 39.1% | 47.6% | -8.9% |
| 2024-2026 | 32 | 21.1% | 41.8% | 24.0% | 50.2% | -0.4% |
| Son 12 ay | 12 | 22.5% | 36.3% | 17.3% | 43.7% | 0.0% |


Yorum: Mevcut "ortodoks" rejimde (2024-2026) TL carry USD bazinda brut ~%21/yil verdi; stopaj (~%15-17.5, dogrulanmali) dusulunce ~%16-18. Bu, kullanicinin ABD stratejisi icin bugunku firsat maliyetidir. Ancak ayni carry 2010-2026'da USD bazinda -%7.2/yil ve -%85 MaxDD; 2018 ve 2021 kur soklari tipik. Yani engel "risksiz %40-50 TL" degil, "kuyruk riski yuksek ~%15-20 USD carry"dir. Karsilastirmada ABD stratejisinin MaxDD'si bu carry'nin MaxDD'siyle birlikte okunmali. Not: shared context'teki Fed funds 3.75-4.00% bandi FRED ile uyumlu (DFEDTARU 4.00, DFF 3.88, DTB3 4.03).

## 3. Test 2: Kaldiracli trend (sentetik 1x/2x/3x, 200-DMA ve 10-ay SMA)

Hucre formati: **CAGR % / MaxDD % / Sharpe** (Sharpe = T-bill ustu ortalama / vol). Spread T-bill+1%, ER 0.9%, 10 bp/gecis. "1926-2026 (tam)" MKT icin 1927-04'te (200 gun isinma sonrasi), NDX "1986-2026 (tam)" 1986-10'da baslar. MKT 2026-09-30, NDX 2026-11-05'te biter.

### 3.1 lag0 (t kapanis sinyali, t+1 uygulama)

| Dayanak | L | Strateji | 1926-2026 (tam) | 1950-2026 | 1986-2026 (tam) | 1986-2026 | 2010-2026 | 2020-2026 |
|---|---|---|---|---|---|---|---|---|
| MKT | 1 | 10aySMA | 9.1 / -45 / 0.54 | 10.3 / -32 / 0.59 |  | 9.3 / -32 / 0.52 | 9.2 / -22 / 0.62 | 11.1 / -17 / 0.65 |
| MKT | 1 | 200DMA | 10.4 / -34 / 0.66 | 10.9 / -32 / 0.68 |  | 9.1 / -32 / 0.54 | 8.9 / -23 / 0.64 | 11.2 / -19 / 0.67 |
| MKT | 1 | BH | 9.7 / -84 / 0.45 | 11.5 / -55 / 0.53 |  | 11.3 / -55 / 0.52 | 14.1 / -34 / 0.75 | 15.0 / -34 / 0.64 |
| MKT | 2 | 10aySMA | 12.6 / -76 / 0.49 | 14.2 / -58 / 0.54 |  | 12.6 / -58 / 0.48 | 14.0 / -40 / 0.58 | 16.5 / -33 / 0.61 |
| MKT | 2 | 200DMA | 15.9 / -60 / 0.63 | 16.3 / -58 / 0.65 |  | 13.1 / -58 / 0.51 | 14.1 / -41 / 0.60 | 17.2 / -35 / 0.63 |
| MKT | 2 | BH | 11.4 / -98 / 0.40 | 14.7 / -88 / 0.48 |  | 14.3 / -88 / 0.47 | 22.3 / -60 / 0.71 | 21.0 / -60 / 0.60 |
| MKT | 3 | 10aySMA | 15.1 / -91 / 0.49 | 17.4 / -78 / 0.54 |  | 14.7 / -78 / 0.48 | 17.7 / -57 / 0.58 | 20.9 / -47 / 0.61 |
| MKT | 3 | 200DMA | 20.8 / -78 / 0.64 | 21.3 / -75 / 0.66 |  | 16.3 / -75 / 0.52 | 18.5 / -55 / 0.61 | 22.2 / -49 / 0.64 |
| MKT | 3 | BH | 10.6 / -100 / 0.40 | 16.2 / -98 / 0.48 |  | 14.4 / -98 / 0.47 | 27.8 / -77 / 0.71 | 22.6 / -77 / 0.60 |
| NDX | 1 | 10aySMA |  |  | 12.5 / -40 / 0.55 |  | 11.9 / -28 / 0.65 | 15.6 / -28 / 0.67 |
| NDX | 1 | 200DMA |  |  | 11.7 / -59 / 0.53 |  | 12.2 / -22 / 0.71 | 17.1 / -22 / 0.80 |
| NDX | 1 | BH |  |  | 14.6 / -83 / 0.54 |  | 17.8 / -35 / 0.82 | 18.4 / -35 / 0.68 |
| NDX | 2 | 10aySMA |  |  | 16.9 / -71 / 0.52 |  | 18.2 / -52 / 0.61 | 22.8 / -52 / 0.64 |
| NDX | 2 | 200DMA |  |  | 16.4 / -86 / 0.52 |  | 19.9 / -40 / 0.68 | 27.4 / -40 / 0.77 |
| NDX | 2 | BH |  |  | 16.9 / -99 / 0.50 |  | 28.7 / -64 / 0.78 | 25.6 / -64 / 0.65 |
| NDX | 3 | 10aySMA |  |  | 17.5 / -89 / 0.52 |  | 21.7 / -70 / 0.61 | 25.7 / -70 / 0.64 |
| NDX | 3 | 200DMA |  |  | 17.8 / -97 / 0.52 |  | 25.7 / -55 / 0.69 | 34.8 / -55 / 0.77 |
| NDX | 3 | BH |  |  | 12.0 / -100 / 0.50 |  | 35.6 / -82 / 0.78 | 25.8 / -82 / 0.65 |


### 3.2 lag1 (1 gun ek gecikme; daha gercekci)

| Dayanak | L | Strateji | 1926-2026 (tam) | 1950-2026 | 1986-2026 (tam) | 1986-2026 | 2010-2026 | 2020-2026 |
|---|---|---|---|---|---|---|---|---|
| MKT | 1 | 10aySMA | 8.9 / -48 / 0.52 | 10.2 / -32 / 0.58 |  | 9.1 / -32 / 0.51 | 8.7 / -22 / 0.59 | 11.7 / -17 / 0.69 |
| MKT | 1 | 200DMA | 9.5 / -41 / 0.59 | 10.2 / -29 / 0.60 |  | 8.6 / -29 / 0.50 | 9.1 / -23 / 0.65 | 11.8 / -23 / 0.71 |
| MKT | 1 | BH | 9.7 / -84 / 0.45 | 11.5 / -55 / 0.53 |  | 11.3 / -55 / 0.52 | 14.1 / -34 / 0.75 | 15.0 / -34 / 0.64 |
| MKT | 2 | 10aySMA | 12.2 / -78 / 0.47 | 14.1 / -58 / 0.53 |  | 12.3 / -58 / 0.46 | 13.1 / -42 / 0.54 | 17.7 / -34 / 0.65 |
| MKT | 2 | 200DMA | 14.1 / -69 / 0.56 | 14.6 / -54 / 0.57 |  | 12.0 / -54 / 0.47 | 14.6 / -42 / 0.62 | 18.4 / -42 / 0.67 |
| MKT | 2 | BH | 11.4 / -98 / 0.40 | 14.7 / -88 / 0.48 |  | 14.3 / -88 / 0.47 | 22.3 / -60 / 0.71 | 21.0 / -60 / 0.60 |
| MKT | 3 | 10aySMA | 14.4 / -92 / 0.48 | 17.2 / -77 / 0.53 |  | 14.2 / -77 / 0.46 | 16.2 / -57 / 0.54 | 22.7 / -48 / 0.65 |
| MKT | 3 | 200DMA | 17.9 / -85 / 0.57 | 18.5 / -73 / 0.58 |  | 14.3 / -73 / 0.47 | 19.3 / -57 / 0.63 | 24.1 / -57 / 0.68 |
| MKT | 3 | BH | 10.6 / -100 / 0.40 | 16.2 / -98 / 0.48 |  | 14.4 / -98 / 0.47 | 27.8 / -77 / 0.71 | 22.6 / -77 / 0.60 |
| NDX | 1 | 10aySMA |  |  | 12.8 / -40 / 0.56 |  | 11.5 / -28 / 0.62 | 15.2 / -28 / 0.65 |
| NDX | 1 | 200DMA |  |  | 12.2 / -39 / 0.55 |  | 11.9 / -22 / 0.68 | 16.8 / -22 / 0.77 |
| NDX | 1 | BH |  |  | 14.6 / -83 / 0.54 |  | 17.8 / -35 / 0.82 | 18.4 / -35 / 0.68 |
| NDX | 2 | 10aySMA |  |  | 17.5 / -70 / 0.53 |  | 17.3 / -52 / 0.59 | 22.0 / -52 / 0.62 |
| NDX | 2 | 200DMA |  |  | 17.2 / -71 / 0.53 |  | 19.0 / -41 / 0.65 | 26.6 / -41 / 0.74 |
| NDX | 2 | BH |  |  | 16.9 / -99 / 0.50 |  | 28.7 / -64 / 0.78 | 25.6 / -64 / 0.65 |
| NDX | 3 | 10aySMA |  |  | 18.2 / -88 / 0.53 |  | 20.2 / -70 / 0.59 | 24.5 / -70 / 0.62 |
| NDX | 3 | 200DMA |  |  | 18.8 / -88 / 0.54 |  | 24.0 / -57 / 0.66 | 33.1 / -57 / 0.75 |
| NDX | 3 | BH |  |  | 12.0 / -100 / 0.50 |  | 35.6 / -82 / 0.78 | 25.8 / -82 / 0.65 |


### 3.3 Tam istatistikler (lag0, spread 1%, 10bp): en kotu yil, T-bill ustu CAGR, yillik gecis

**MKT: ana sonuclar (spread T-bill+1.0%, ER 0.9%, sinyal t kapanis -> t+1, gecis maliyeti 10 bp)**

| Donem | L | Strateji | CAGR | Vol | Sharpe | MaxDD | EnKotuYil | EnKotuYilT | ExcessCAGR | Gecis_yil |
|---|---|---|---|---|---|---|---|---|---|---|
| 1926-2026 (tam) | 1 | BH | 9.7% | 17.2% | 0.45 | -84.1% | -44.4% | 1931 | 6.6% | 0.0 |
| 1950-2026 | 1 | BH | 11.5% | 15.3% | 0.53 | -54.6% | -36.5% | 2008 | 7.5% | 0.0 |
| 1986-2026 | 1 | BH | 11.3% | 18.0% | 0.52 | -54.6% | -36.5% | 2008 | 8.2% | 0.0 |
| 2010-2026 | 1 | BH | 14.1% | 17.6% | 0.75 | -34.2% | -20.0% | 2022 | 12.6% | 0.0 |
| 2020-2026 | 1 | BH | 15.0% | 20.7% | 0.64 | -34.2% | -20.0% | 2022 | 12.1% | 0.0 |
| 1926-2026 (tam) | 1 | 200DMA | 10.4% | 11.3% | 0.66 | -34.1% | -17.0% | 2000 | 7.3% | 5.4 |
| 1950-2026 | 1 | 200DMA | 10.9% | 10.3% | 0.68 | -31.9% | -17.0% | 2000 | 7.0% | 5.6 |
| 1986-2026 | 1 | 200DMA | 9.1% | 11.6% | 0.54 | -31.9% | -17.0% | 2000 | 6.0% | 6.0 |
| 2010-2026 | 1 | 200DMA | 8.9% | 12.2% | 0.64 | -22.9% | -13.1% | 2022 | 7.4% | 5.6 |
| 2020-2026 | 1 | 200DMA | 11.2% | 12.9% | 0.67 | -19.3% | -13.1% | 2022 | 8.3% | 5.4 |
| 1926-2026 (tam) | 1 | 10aySMA | 9.1% | 12.0% | 0.54 | -45.1% | -21.9% | 1940 | 6.0% | 1.4 |
| 1950-2026 | 1 | 10aySMA | 10.3% | 11.1% | 0.59 | -32.3% | -16.5% | 1990 | 6.3% | 1.5 |
| 1986-2026 | 1 | 10aySMA | 9.3% | 12.8% | 0.52 | -32.3% | -16.5% | 1990 | 6.2% | 1.5 |
| 2010-2026 | 1 | 10aySMA | 9.2% | 13.1% | 0.62 | -21.9% | -11.2% | 2022 | 7.7% | 1.7 |
| 2020-2026 | 1 | 10aySMA | 11.1% | 12.9% | 0.65 | -16.7% | -11.2% | 2022 | 8.2% | 1.8 |
| 1926-2026 (tam) | 2 | BH | 11.4% | 34.3% | 0.40 | -98.5% | -73.4% | 1931 | 8.3% | 0.0 |
| 1950-2026 | 2 | BH | 14.7% | 30.7% | 0.48 | -88.2% | -67.0% | 2008 | 10.8% | 0.0 |
| 1986-2026 | 2 | BH | 14.3% | 36.1% | 0.47 | -88.2% | -67.0% | 2008 | 11.3% | 0.0 |
| 2010-2026 | 2 | BH | 22.3% | 35.3% | 0.71 | -59.8% | -41.8% | 2022 | 20.8% | 0.0 |
| 2020-2026 | 2 | BH | 21.0% | 41.5% | 0.60 | -59.8% | -41.8% | 2022 | 18.1% | 0.0 |
| 1926-2026 (tam) | 2 | 200DMA | 15.9% | 22.5% | 0.63 | -60.3% | -37.0% | 2000 | 12.8% | 5.4 |
| 1950-2026 | 2 | 200DMA | 16.3% | 20.6% | 0.65 | -58.2% | -37.0% | 2000 | 12.3% | 5.6 |
| 1986-2026 | 2 | 200DMA | 13.1% | 23.3% | 0.51 | -58.2% | -37.0% | 2000 | 10.0% | 6.0 |
| 2010-2026 | 2 | 200DMA | 14.1% | 24.3% | 0.60 | -40.8% | -25.0% | 2022 | 12.6% | 5.6 |
| 2020-2026 | 2 | 200DMA | 17.2% | 25.7% | 0.63 | -35.4% | -25.0% | 2022 | 14.3% | 5.4 |
| 1926-2026 (tam) | 2 | 10aySMA | 12.6% | 24.0% | 0.49 | -75.9% | -41.2% | 1940 | 9.5% | 1.4 |
| 1950-2026 | 2 | 10aySMA | 14.2% | 22.1% | 0.54 | -57.8% | -36.3% | 1990 | 10.2% | 1.5 |
| 1986-2026 | 2 | 10aySMA | 12.6% | 25.6% | 0.48 | -57.8% | -36.3% | 1990 | 9.6% | 1.5 |
| 2010-2026 | 2 | 10aySMA | 14.0% | 26.2% | 0.58 | -40.4% | -22.7% | 2022 | 12.5% | 1.7 |
| 2020-2026 | 2 | 10aySMA | 16.5% | 25.8% | 0.61 | -33.3% | -22.7% | 2022 | 13.6% | 1.8 |
| 1926-2026 (tam) | 3 | BH | 10.6% | 51.5% | 0.40 | -99.9% | -88.7% | 1931 | 7.5% | 0.0 |
| 1950-2026 | 3 | BH | 16.2% | 46.0% | 0.48 | -98.2% | -85.4% | 2008 | 12.2% | 0.0 |
| 1986-2026 | 3 | BH | 14.4% | 54.1% | 0.47 | -98.2% | -85.4% | 2008 | 11.3% | 0.0 |
| 2010-2026 | 3 | BH | 27.8% | 52.9% | 0.71 | -77.2% | -60.0% | 2022 | 26.4% | 0.0 |
| 2020-2026 | 3 | BH | 22.6% | 62.2% | 0.60 | -77.2% | -60.0% | 2022 | 19.7% | 0.0 |
| 1926-2026 (tam) | 3 | 200DMA | 20.8% | 33.8% | 0.64 | -78.4% | -53.6% | 2000 | 17.7% | 5.4 |
| 1950-2026 | 3 | 200DMA | 21.3% | 30.9% | 0.66 | -74.9% | -53.6% | 2000 | 17.3% | 5.6 |
| 1986-2026 | 3 | 200DMA | 16.3% | 34.9% | 0.52 | -74.9% | -53.6% | 2000 | 13.2% | 6.0 |
| 2010-2026 | 3 | 200DMA | 18.5% | 36.5% | 0.61 | -55.0% | -35.5% | 2022 | 17.1% | 5.6 |
| 2020-2026 | 3 | 200DMA | 22.2% | 38.6% | 0.64 | -49.2% | -35.5% | 2022 | 19.3% | 5.4 |
| 1926-2026 (tam) | 3 | 10aySMA | 15.1% | 36.1% | 0.49 | -91.1% | -56.8% | 1940 | 12.0% | 1.4 |
| 1950-2026 | 3 | 10aySMA | 17.4% | 33.2% | 0.54 | -78.2% | -51.8% | 1990 | 13.4% | 1.5 |
| 1986-2026 | 3 | 10aySMA | 14.7% | 38.3% | 0.48 | -78.2% | -51.8% | 1990 | 11.7% | 1.5 |
| 2010-2026 | 3 | 10aySMA | 17.7% | 39.3% | 0.58 | -57.5% | -33.0% | 2022 | 16.2% | 1.7 |
| 2020-2026 | 3 | 10aySMA | 20.9% | 38.8% | 0.61 | -47.2% | -33.0% | 2022 | 18.0% | 1.8 |

**NDX: ana sonuclar (spread T-bill+1.0%, ER 0.9%, sinyal t kapanis -> t+1, gecis maliyeti 10 bp)**

| Donem | L | Strateji | CAGR | Vol | Sharpe | MaxDD | EnKotuYil | EnKotuYilT | ExcessCAGR | Gecis_yil |
|---|---|---|---|---|---|---|---|---|---|---|
| 1986-2026 (tam) | 1 | BH | 14.6% | 26.3% | 0.54 | -82.6% | -41.5% | 2008 | 11.6% | 0.0 |
| 2010-2026 | 1 | BH | 17.8% | 20.9% | 0.82 | -35.2% | -32.6% | 2022 | 16.4% | 0.0 |
| 2020-2026 | 1 | BH | 18.4% | 25.2% | 0.68 | -35.2% | -32.6% | 2022 | 15.5% | 0.0 |
| 1986-2026 (tam) | 1 | 200DMA | 11.7% | 18.4% | 0.53 | -58.6% | -24.0% | 2000 | 8.7% | 7.0 |
| 2010-2026 | 1 | 200DMA | 12.2% | 16.0% | 0.71 | -22.0% | -17.4% | 2022 | 10.8% | 5.8 |
| 2020-2026 | 1 | 200DMA | 17.1% | 18.3% | 0.80 | -22.0% | -17.4% | 2022 | 14.2% | 3.2 |
| 1986-2026 (tam) | 1 | 10aySMA | 12.5% | 19.5% | 0.55 | -39.9% | -22.3% | 1990 | 9.5% | 1.7 |
| 2010-2026 | 1 | 10aySMA | 11.9% | 17.5% | 0.65 | -28.0% | -9.6% | 2016 | 10.4% | 1.8 |
| 2020-2026 | 1 | 10aySMA | 15.6% | 20.4% | 0.67 | -28.0% | -8.4% | 2026 | 12.6% | 1.2 |
| 1986-2026 (tam) | 2 | BH | 16.9% | 52.6% | 0.50 | -98.9% | -72.8% | 2000 | 13.9% | 0.0 |
| 2010-2026 | 2 | BH | 28.7% | 41.8% | 0.78 | -63.5% | -60.3% | 2022 | 27.3% | 0.0 |
| 2020-2026 | 2 | BH | 25.6% | 50.4% | 0.65 | -63.5% | -60.3% | 2022 | 22.7% | 0.0 |
| 1986-2026 (tam) | 2 | 200DMA | 16.4% | 36.7% | 0.52 | -86.3% | -54.1% | 2000 | 13.3% | 7.0 |
| 2010-2026 | 2 | 200DMA | 19.9% | 31.9% | 0.68 | -40.3% | -32.5% | 2022 | 18.5% | 5.8 |
| 2020-2026 | 2 | 200DMA | 27.4% | 36.6% | 0.77 | -40.3% | -32.5% | 2022 | 24.5% | 3.2 |
| 1986-2026 (tam) | 2 | 10aySMA | 16.9% | 39.0% | 0.52 | -71.4% | -45.4% | 1990 | 13.9% | 1.7 |
| 2010-2026 | 2 | 10aySMA | 18.2% | 35.0% | 0.61 | -51.7% | -22.3% | 2026 | 16.7% | 1.8 |
| 2020-2026 | 2 | 10aySMA | 22.8% | 40.7% | 0.64 | -51.7% | -22.3% | 2026 | 19.9% | 1.2 |
| 1986-2026 (tam) | 3 | BH | 12.0% | 78.9% | 0.50 | -100.0% | -91.5% | 2000 | 9.0% | 0.0 |
| 2010-2026 | 3 | BH | 35.6% | 62.6% | 0.78 | -81.5% | -78.9% | 2022 | 34.1% | 0.0 |
| 2020-2026 | 3 | BH | 25.8% | 75.6% | 0.65 | -81.5% | -78.9% | 2022 | 22.8% | 0.0 |
| 1986-2026 (tam) | 3 | 200DMA | 17.8% | 55.1% | 0.52 | -97.1% | -76.8% | 2000 | 14.8% | 7.0 |
| 2010-2026 | 3 | 200DMA | 25.7% | 47.9% | 0.69 | -55.2% | -45.2% | 2022 | 24.2% | 5.8 |
| 2020-2026 | 3 | 200DMA | 34.8% | 54.9% | 0.77 | -55.2% | -45.2% | 2022 | 31.8% | 3.2 |
| 1986-2026 (tam) | 3 | 10aySMA | 17.5% | 58.5% | 0.52 | -88.9% | -67.6% | 2000 | 14.4% | 1.7 |
| 2010-2026 | 3 | 10aySMA | 21.7% | 52.4% | 0.61 | -70.0% | -36.3% | 2026 | 20.2% | 1.8 |
| 2020-2026 | 3 | 10aySMA | 25.7% | 61.1% | 0.64 | -70.0% | -36.3% | 2026 | 22.8% | 1.2 |


### 3.4 Robustluk izgarasi (MA 100/150/200/250 gun x bant 0/1/2% x lag 0/1 x maliyet 0/10/25 bp = 72 kombinasyon, spread 1%)

**MKT: robustluk izgarasi (n in 100/150/200/250, bant 0/1/2%, lag 0/1, maliyet 0/10/25bp = 72 kombinasyon): MEDYAN ve [min,max]**

| Donem | L | CAGR_med | CAGR_min | CAGR_max | Sharpe_med | MaxDD_med | MaxDD_worst | Gecis_med |
|---|---|---|---|---|---|---|---|---|
| 1926-2026 (tam) | 1 | 9.8% | 7.7% | 11.1% | 0.61 | -41.8% | -52.4% | 2.9 |
| 1926-2026 (tam) | 2 | 14.5% | 11.4% | 16.9% | 0.58 | -68.9% | -78.2% | 2.9 |
| 1926-2026 (tam) | 3 | 18.4% | 14.1% | 22.3% | 0.58 | -84.7% | -90.8% | 2.9 |
| 1950-2026 | 1 | 10.6% | 8.0% | 11.9% | 0.64 | -30.7% | -48.9% | 2.9 |
| 1950-2026 | 2 | 15.2% | 11.8% | 17.6% | 0.60 | -57.2% | -73.7% | 2.9 |
| 1950-2026 | 3 | 19.4% | 14.5% | 23.0% | 0.61 | -75.5% | -86.8% | 2.9 |
| 1986-2026 | 1 | 9.3% | 5.8% | 10.8% | 0.55 | -30.7% | -48.9% | 3.0 |
| 1986-2026 | 2 | 13.1% | 8.9% | 15.8% | 0.51 | -57.2% | -73.7% | 3.0 |
| 1986-2026 | 3 | 16.0% | 11.2% | 20.0% | 0.52 | -75.5% | -86.8% | 3.0 |
| 2010-2026 | 1 | 9.2% | 5.8% | 10.9% | 0.65 | -21.8% | -28.7% | 3.2 |
| 2010-2026 | 2 | 14.5% | 10.2% | 17.8% | 0.61 | -40.1% | -49.0% | 3.2 |
| 2010-2026 | 3 | 19.0% | 14.0% | 24.1% | 0.61 | -54.6% | -65.3% | 3.2 |
| 2020-2026 | 1 | 11.3% | 8.8% | 14.7% | 0.66 | -20.4% | -28.7% | 3.1 |
| 2020-2026 | 2 | 17.0% | 11.6% | 24.3% | 0.62 | -38.3% | -49.0% | 3.1 |
| 2020-2026 | 3 | 21.8% | 12.8% | 33.2% | 0.63 | -53.2% | -65.3% | 3.1 |

**NDX: robustluk izgarasi (n in 100/150/200/250, bant 0/1/2%, lag 0/1, maliyet 0/10/25bp = 72 kombinasyon): MEDYAN ve [min,max]**

| Donem | L | CAGR_med | CAGR_min | CAGR_max | Sharpe_med | MaxDD_med | MaxDD_worst | Gecis_med |
|---|---|---|---|---|---|---|---|---|
| 1986-2026 (tam) | 1 | 12.1% | 8.8% | 13.3% | 0.55 | -44.0% | -76.4% | 3.7 |
| 1986-2026 (tam) | 2 | 16.8% | 12.9% | 18.9% | 0.53 | -75.1% | -94.9% | 3.7 |
| 1986-2026 (tam) | 3 | 18.3% | 12.5% | 22.0% | 0.53 | -91.7% | -99.2% | 3.7 |
| 2010-2026 | 1 | 11.5% | 6.5% | 13.4% | 0.66 | -24.5% | -30.6% | 3.5 |
| 2010-2026 | 2 | 18.1% | 11.0% | 21.9% | 0.63 | -44.1% | -51.9% | 3.5 |
| 2010-2026 | 3 | 22.6% | 13.9% | 28.7% | 0.63 | -59.7% | -68.4% | 3.5 |
| 2020-2026 | 1 | 16.3% | 10.9% | 18.7% | 0.76 | -23.0% | -30.6% | 3.1 |
| 2020-2026 | 2 | 26.2% | 16.2% | 30.5% | 0.74 | -41.5% | -51.9% | 3.1 |
| 2020-2026 | 3 | 33.1% | 17.3% | 39.5% | 0.75 | -56.9% | -67.8% | 3.1 |


### 3.5 Kriz pencereleri (lag0, maliyetsiz, spread 1%): pencere getirisi / pencere ici MaxDD

**MKT: kriz pencereleri (spread 1%, lag0, maliyetsiz): pencere getirisi / pencere ici MaxDD**

| L | Strateji | 1929-32 | 1987 Ekim | 2000-02 | 2008 (07/10-09/03) | 2020 Covid (Sub-Nis) | 2022 |
|---|---|---|---|---|---|---|---|
| 1 | 10aySMA | -21% / -36% | -21% / -32% | -13% / -26% | -1% / -10% | -8% / -13% | -11% / -13% |
| 1 | 200DMA | -19% / -20% | -9% / -15% | -19% / -26% | -8% / -11% | -13% / -17% | -12% / -13% |
| 1 | BH | -79% / -84% | -22% / -33% | -38% / -49% | -45% / -55% | -9% / -34% | -20% / -26% |
| 2 | 10aySMA | -44% / -61% | -43% / -58% | -37% / -48% | -6% / -20% | -16% / -24% | -23% / -26% |
| 2 | 200DMA | -38% / -39% | -19% / -28% | -45% / -52% | -19% / -24% | -25% / -32% | -24% / -26% |
| 2 | BH | -97% / -98% | -45% / -60% | -73% / -81% | -77% / -84% | -26% / -60% | -42% / -48% |
| 3 | 10aySMA | -63% / -78% | -63% / -76% | -57% / -65% | -12% / -29% | -24% / -35% | -33% / -37% |
| 3 | 200DMA | -54% / -55% | -30% / -40% | -64% / -69% | -28% / -35% | -36% / -45% | -35% / -36% |
| 3 | BH | -100% / -100% | -66% / -78% | -90% / -94% | -92% / -95% | -45% / -77% | -60% / -66% |

**NDX: kriz pencereleri (spread 1%, lag0, maliyetsiz): pencere getirisi / pencere ici MaxDD**

| L | Strateji | 1987 Ekim | 2000-02 | 2008 (07/10-09/03) | 2020 Covid (Sub-Nis) | 2022 |
|---|---|---|---|---|---|---|
| 1 | 10aySMA | -23% / -40% | -7% / -36% | -19% / -25% | -13% / -28% | -7% / -15% |
| 1 | 200DMA | -5% / -14% | -37% / -51% | -16% / -22% | -7% / -22% | -17% / -19% |
| 1 | BH | -20% / -40% | -73% / -83% | -40% / -53% | 0% / -28% | -33% / -35% |
| 2 | 10aySMA | -47% / -67% | -38% / -63% | -38% / -46% | -31% / -52% | -16% / -28% |
| 2 | 200DMA | -14% / -27% | -71% / -81% | -34% / -42% | -17% / -40% | -32% / -34% |
| 2 | BH | -45% / -67% | -97% / -99% | -73% / -83% | -9% / -52% | -60% / -63% |
| 3 | 10aySMA | -67% / -83% | -65% / -81% | -54% / -63% | -49% / -70% | -24% / -40% |
| 3 | 200DMA | -22% / -38% | -89% / -94% | -49% / -58% | -28% / -55% | -45% / -47% |
| 3 | BH | -66% / -84% | -100% / -100% | -91% / -95% | -26% / -70% | -79% / -81% |


### 3.6 Kayan pencere: baslangic tarihi sansina duyarlilik (lag1, 10bp, spread 1%) (Test 7)

| Strateji | Pencere | Ornek | Medyan | P10 | P90 | <0 | >%10 | >%15 | >%20 |
|---|---|---|---|---|---|---|---|---|---|
| MKT 1x BH | 3y | 1950+ baslangic | 12.0% | -0.4% | 21.7% | 10.2% | 62.6% | 32.8% | 13.6% |
| MKT 1x BH | 3y | 1990+ baslangic | 12.5% | -4.4% | 22.6% | 13.8% | 64.2% | 34.1% | 14.8% |
| MKT 1x BH | 5y | 1950+ baslangic | 12.1% | 1.0% | 19.2% | 7.0% | 63.9% | 30.0% | 7.7% |
| MKT 1x BH | 5y | 1990+ baslangic | 12.0% | -0.3% | 19.2% | 10.5% | 62.5% | 31.2% | 8.9% |
| MKT 1x 200DMA | 3y | 1950+ baslangic | 9.9% | 2.6% | 18.5% | 5.1% | 48.7% | 19.2% | 7.6% |
| MKT 1x 200DMA | 3y | 1990+ baslangic | 8.4% | 0.5% | 16.6% | 9.1% | 40.2% | 15.1% | 5.2% |
| MKT 1x 200DMA | 5y | 1950+ baslangic | 9.7% | 4.1% | 17.0% | 0.7% | 48.1% | 15.8% | 2.7% |
| MKT 1x 200DMA | 5y | 1990+ baslangic | 8.5% | 2.2% | 15.6% | 1.6% | 39.4% | 11.3% | 1.3% |
| NDX 1x BH | 3y | 1990+ baslangic | 16.4% | -2.7% | 34.7% | 13.0% | 71.7% | 57.2% | 34.6% |
| NDX 1x BH | 5y | 1990+ baslangic | 16.3% | -1.9% | 28.2% | 13.1% | 69.2% | 56.1% | 32.6% |
| NDX 1x 200DMA | 3y | 1990+ baslangic | 11.5% | 3.4% | 28.5% | 4.4% | 57.0% | 35.4% | 19.9% |
| NDX 1x 200DMA | 5y | 1990+ baslangic | 11.6% | 3.3% | 24.3% | 0.8% | 58.2% | 36.8% | 20.1% |
| MKT 2x BH | 3y | 1950+ baslangic | 16.9% | -9.6% | 37.5% | 16.2% | 69.7% | 54.1% | 39.5% |
| MKT 2x BH | 3y | 1990+ baslangic | 18.8% | -18.4% | 38.5% | 19.5% | 71.6% | 61.0% | 47.2% |
| MKT 2x BH | 5y | 1950+ baslangic | 16.3% | -7.5% | 33.4% | 19.5% | 66.4% | 54.0% | 36.1% |
| MKT 2x BH | 5y | 1990+ baslangic | 17.2% | -9.1% | 32.8% | 25.2% | 64.8% | 57.2% | 42.5% |
| MKT 2x 200DMA | 3y | 1950+ baslangic | 14.4% | -0.6% | 31.0% | 10.8% | 65.4% | 48.6% | 31.5% |
| MKT 2x 200DMA | 3y | 1990+ baslangic | 12.8% | -5.1% | 28.1% | 13.6% | 60.0% | 45.4% | 30.4% |
| MKT 2x 200DMA | 5y | 1950+ baslangic | 13.9% | 2.2% | 27.7% | 4.6% | 64.2% | 46.3% | 27.4% |
| MKT 2x 200DMA | 5y | 1990+ baslangic | 12.9% | 0.3% | 25.8% | 9.4% | 59.6% | 42.5% | 23.6% |
| NDX 2x BH | 3y | 1990+ baslangic | 27.9% | -20.2% | 61.2% | 19.2% | 70.0% | 64.6% | 60.4% |
| NDX 2x BH | 5y | 1990+ baslangic | 24.6% | -22.5% | 48.7% | 22.2% | 66.6% | 63.7% | 58.2% |
| NDX 2x 200DMA | 3y | 1990+ baslangic | 18.6% | 2.3% | 47.2% | 6.6% | 71.0% | 56.5% | 46.4% |
| NDX 2x 200DMA | 5y | 1990+ baslangic | 18.2% | 2.8% | 41.4% | 5.7% | 77.5% | 61.6% | 45.2% |
| MKT 3x BH | 3y | 1950+ baslangic | 19.5% | -21.2% | 53.5% | 21.2% | 67.5% | 59.1% | 49.2% |
| MKT 3x BH | 3y | 1990+ baslangic | 24.3% | -35.1% | 53.1% | 23.0% | 67.9% | 64.7% | 58.3% |
| MKT 3x BH | 5y | 1950+ baslangic | 18.6% | -18.2% | 47.6% | 23.2% | 63.9% | 56.8% | 47.0% |
| MKT 3x BH | 5y | 1990+ baslangic | 20.5% | -21.3% | 46.3% | 28.9% | 62.7% | 58.3% | 50.7% |
| MKT 3x 200DMA | 3y | 1950+ baslangic | 18.6% | -5.1% | 43.9% | 16.6% | 69.0% | 58.2% | 47.3% |
| MKT 3x 200DMA | 3y | 1990+ baslangic | 16.6% | -10.9% | 40.0% | 18.3% | 65.7% | 54.3% | 45.2% |
| MKT 3x 200DMA | 5y | 1950+ baslangic | 17.5% | -0.7% | 39.9% | 11.5% | 67.7% | 55.2% | 44.0% |
| MKT 3x 200DMA | 5y | 1990+ baslangic | 15.9% | -2.6% | 35.9% | 15.5% | 65.6% | 51.7% | 41.7% |
| NDX 3x BH | 3y | 1990+ baslangic | 35.2% | -44.3% | 83.6% | 24.1% | 67.1% | 64.1% | 60.7% |
| NDX 3x BH | 5y | 1990+ baslangic | 28.0% | -49.6% | 68.8% | 32.1% | 62.9% | 59.8% | 56.1% |
| NDX 3x 200DMA | 3y | 1990+ baslangic | 22.6% | -2.5% | 58.4% | 13.5% | 70.8% | 62.2% | 54.8% |
| NDX 3x 200DMA | 5y | 1990+ baslangic | 22.1% | -0.6% | 50.6% | 10.2% | 77.0% | 66.6% | 57.2% |


**Test 2 bulgulari**
- Uzun donemde (1927-2026, 1950-2026) 200-DMA, kaldiracli BH'ye gore CAGR'yi +1.6..+10 puan artirip MaxDD'yi 20-40 puan azaltti; izgara medyani da ayni yonde (piyasa 3x medyan 18.4%, min 14.1%, max 22.3%). Bu, Gayed & Bilello "Leverage for the Long Run" (SSRN 2741701, 2016; bellekten, dogrulanmadi) bulgusuyla uyumlu.
- **Volatilite sonumlemesi (decay) gercek**: NDX 1986-2026'da 1x BH 14.6% iken 3x BH 12.0% (MaxDD -100%). Kaldirac tek basina kazanmiyor; ayi piyasasinda cikmak sart.
- **2010-2026'da trend filtresi pahaliydi**: MKT 1x 200DMA 8.9% vs BH 14.1%; 3x 18.5% vs 27.8%. Hizli V donusleri (2011, 2015-16, 2018-Q4, 2020, 2022-23) whipsaw uretti (yilda ~5-6 gecis bantsiz; %1-2 bantla ~3).
- **Lag duyarliligi yuksek ve yol bagimli**: NDX 1x 200DMA tam donem MaxDD lag0'da -59%, lag1'de -39%; NDX 3x lag0 -97%, lag1 -88%. Tek bir gunluk kayma sonucu 20 puan oynatiyorsa, backtest MaxDD'si bir tahmin degil bir orneklemdir.
- **2020 Covid**: 200DMA cikisi gec kaldi; NDX 3x+200DMA -28% (pencere ici -55%), MKT 3x -36%. **2022**: NDX 3x+200DMA -45%, BH -79%. **2008**: filtre iyi calisti (MKT 3x -28% vs BH -92%). **2000-02**: MKT'de yarim koruma (3x -64% vs -90%), NDX'te neredeyse koruma yok (3x -89% vs -100%).
- 10-ay SMA, 200-DMA'dan genelde zayif (ozellikle 1987 Ekim ve 2020 gibi hizli coküslerde aylik kontrol gec kaliyor) ama yilda ~1.5 gecisle cok daha az islem maliyeti/vergi olayi uretir.
- Spread 0.5% -> 1.0% gecisi 3x'te CAGR'yi ~0.9-1.3 puan dusuruyor; ER ve swap maliyeti ciddi ama belirleyici degil.

## 4. Test 1: Momentum (UMD, vol-yonetimli UMD, sadece-uzun momentum, endustri rotasyonu)

Hucre: **CAGR % / MaxDD % / Sharpe** (aylik veri, USD, toplam getiri; UMD sifir maliyetli uzun-kisa oldugu icin +RF ile teminatli getiri olarak gosterildi).

| Strateji | 1927-2026 (tam) | 1950-2026 | 2000-2026 | 2010-2026 | 2020-2026 |
|---|---|---|---|---|---|
| Piyasa (CRSP VW TR) | 10.3 / -84 / 0.45 | 11.7 / -50 / 0.55 | 8.5 / -50 / 0.48 | 14.1 / -25 / 0.87 | 15.0 / -25 / 0.73 |
| UMD+RF (uzun-kisa, teminatli) | 9.5 / -78 / 0.45 | 11.4 / -58 / 0.58 | 2.8 / -58 / 0.14 | 4.0 / -25 / 0.26 | 5.4 / -25 / 0.24 |
| VolYon. UMD+RF (hedef %12) | 16.3 / -42 / 0.81 | 18.9 / -24 / 0.91 | 6.5 / -24 / 0.40 | 6.1 / -18 / 0.46 | 7.3 / -11 / 0.49 |
| Mom ust desil VW (sadece uzun) | 16.8 / -76 / 0.66 | 18.2 / -51 / 0.72 | 10.9 / -51 / 0.49 | 17.8 / -31 / 0.79 | 21.6 / -31 / 0.75 |
| Mom ust %20 VW (sadece uzun) | 14.9 / -74 / 0.64 | 16.1 / -51 / 0.72 | 9.7 / -51 / 0.50 | 15.2 / -28 / 0.82 | 15.4 / -28 / 0.66 |
| Endustri49 mom K=6 skip=0 top5 | 13.8 / -83 / 0.55 | 15.7 / -51 / 0.66 | 13.4 / -51 / 0.63 | 14.7 / -24 / 0.72 | 21.0 / -20 / 0.78 |
| Endustri49 mom K=12 skip=1 top5 | 15.6 / -77 / 0.62 | 17.2 / -60 / 0.71 | 12.6 / -60 / 0.58 | 15.5 / -30 / 0.74 | 18.8 / -23 / 0.73 |
| Endustri12 mom K=6 skip=0 top3 | 13.4 / -82 / 0.60 | 14.5 / -43 / 0.70 | 10.5 / -42 / 0.57 | 13.2 / -21 / 0.72 | 17.3 / -21 / 0.70 |
| Endustri12 mom K=12 skip=1 top3 | 13.0 / -77 / 0.58 | 14.5 / -42 / 0.69 | 10.5 / -42 / 0.57 | 15.6 / -23 / 0.85 | 19.3 / -22 / 0.81 |
| Endustri49 K=6 top5 + piyasa 10aySMA | 11.9 / -66 / 0.54 | 13.2 / -29 / 0.61 | 11.7 / -25 / 0.64 | 8.5 / -25 / 0.48 | 12.0 / -25 / 0.52 |
| Endustri49 K=12 skip1 top5 + piyasa 10aySMA | 12.8 / -59 / 0.59 | 13.7 / -31 / 0.64 | 9.8 / -27 / 0.55 | 7.5 / -27 / 0.45 | 7.1 / -24 / 0.32 |
| EW 49 endustri (benchmark) | 11.0 / -85 / 0.46 | 12.0 / -53 / 0.54 | 10.1 / -53 / 0.55 | 12.7 / -26 / 0.74 | 13.0 / -25 / 0.60 |
| EW 12 endustri (benchmark) | 10.7 / -83 / 0.47 | 11.9 / -50 / 0.59 | 8.9 / -50 / 0.52 | 12.8 / -23 / 0.80 | 12.8 / -23 / 0.62 |


### 4.1 Endustri momentum izgarasi (K 3/6/9/12 ay x skip 0/1 x N; 49 endustride N 3/5/10, 12 endustride N 3/5), 10 bp/devir

| Evren | Donem | CAGR_med | CAGR_min | CAGR_max | Sharpe_med | MaxDD_med | Devir_med | n |
|---|---|---|---|---|---|---|---|---|
| 12 | 1927-2026 (tam) | 12.4% | 10.4% | 14.6% | 0.56 | -78.0% | 21.8% | 16 |
| 12 | 1950-2026 | 13.8% | 12.0% | 15.6% | 0.68 | -43.0% | 21.6% | 16 |
| 12 | 2000-2026 | 10.4% | 8.7% | 11.6% | 0.59 | -41.5% | 23.6% | 16 |
| 12 | 2010-2026 | 14.6% | 12.3% | 15.7% | 0.84 | -21.5% | 22.4% | 16 |
| 12 | 2020-2026 | 16.0% | 12.5% | 20.4% | 0.73 | -21.3% | 23.5% | 16 |
| 49 | 1927-2026 (tam) | 14.6% | 11.8% | 17.6% | 0.56 | -82.1% | 32.4% | 24 |
| 49 | 1950-2026 | 15.6% | 12.4% | 18.2% | 0.66 | -53.4% | 32.1% | 24 |
| 49 | 2000-2026 | 12.1% | 9.0% | 14.8% | 0.58 | -53.4% | 33.2% | 24 |
| 49 | 2010-2026 | 14.2% | 10.6% | 18.6% | 0.74 | -25.1% | 34.4% | 24 |
| 49 | 2020-2026 | 17.1% | 10.1% | 24.2% | 0.69 | -21.7% | 31.0% | 24 |


### 4.2 Izgara medyani vs benchmark (EW endustri ve CRSP VW piyasa)

| Evren | Donem | Medyan_CAGR | EW_bench | Piyasa | Fark_EW | Fark_Piyasa | Pay_pozitif_vs_piyasa |
|---|---|---|---|---|---|---|---|
| 12 | 1927-2026 (tam) | 12.4% | 10.7% | 10.3% | 1.7% | 2.2% | 100.0% |
| 12 | 1950-2026 | 13.8% | 11.9% | 11.7% | 1.9% | 2.2% | 100.0% |
| 12 | 2000-2026 | 10.4% | 8.9% | 8.5% | 1.5% | 1.9% | 100.0% |
| 12 | 2010-2026 | 14.6% | 12.8% | 14.1% | 1.8% | 0.5% | 56.2% |
| 12 | 2020-2026 | 16.0% | 12.8% | 15.0% | 3.2% | 1.0% | 62.5% |
| 49 | 1927-2026 (tam) | 14.6% | 11.0% | 10.3% | 3.6% | 4.3% | 100.0% |
| 49 | 1950-2026 | 15.6% | 12.0% | 11.7% | 3.6% | 4.0% | 100.0% |
| 49 | 2000-2026 | 12.1% | 10.1% | 8.5% | 2.0% | 3.7% | 100.0% |
| 49 | 2010-2026 | 14.2% | 12.7% | 14.1% | 1.6% | 0.1% | 50.0% |
| 49 | 2020-2026 | 17.1% | 13.0% | 15.0% | 4.1% | 2.1% | 66.7% |


### 4.3 Momentum crash ve vol-yonetim

| Ay | UMD | VolYon_UMD |
|---|---|---|
| 1932-08 | -52.6% | -22.0% |
| 1932-07 | -45.6% | -20.6% |
| 2009-04 | -34.4% | -10.1% |
| 1939-09 | -31.4% | -29.1% |
| 2001-01 | -25.4% | -20.7% |
| 1938-06 | -24.9% | -11.0% |
| 1931-06 | -17.5% | -10.2% |
| 1933-04 | -17.1% | -11.6% |


### 4.4 UMD on yillara gore

| On yil | UMD yillik | VolYon UMD yillik |
|---|---|---|
| 1920 | 25.0% | 33.7% |
| 1930 | -6.9% | -0.3% |
| 1940 | 6.4% | 8.6% |
| 1950 | 10.9% | 20.1% |
| 1960 | 11.1% | 21.3% |
| 1970 | 9.3% | 18.4% |
| 1980 | 8.6% | 15.7% |
| 1990 | 13.7% | 25.2% |
| 2000 | -2.0% | 4.3% |
| 2010 | 2.6% | 4.8% |
| 2020 | 2.5% | 4.4% |


**Test 1 bulgulari**
- UMD'nin primi 2000'den beri kayboldu (2000'ler -2.0%/yil, 2010'lar +2.6%, 2020'ler +2.5%). Vol-yonetim crash'leri yumusatiyor (2009-04: -34.4% -> -10.1%) ve tam ornekte Sharpe'i ikiye katliyor (0.45 -> 0.81; Barroso & Santa-Clara 2015 JFE, doi:10.1016/j.jfineco.2014.11.010, bellekten: 0.53 -> 0.97), ama 2010 sonrasi mutlak getiri T-bill +4.7 puan (2010-2026). Uzun-kisa momentum ayrica bireysel yatirimci icin aciga satis maliyeti nedeniyle pratik degil.
- Sadece-uzun VW ust desil 2010-2026'da 17.8% (piyasa 14.1%), 2020-2026 21.6% (15.0%); ancak vol 22-27% ve Sharpe piyasadan yuksek degil. Bu MTUM tipi bir urunun ust siniri (ust desil, maliyetsiz, aylik rebalans).
- Endustri rotasyonu: uzun ornekte saglam (+2..+4 puan, tum kombinasyonlar piyasanin ustunde), 2010-2026'da yaklasik sifir alfa (+0.1/+0.5 puan). 2020-2026'daki +1..+4 puan, enerji ve AI temalarina denk geliyor; rejim bagimli.
- Endustri momentumuna piyasa 10-ay SMA filtresi eklemek 1950-2026'da MaxDD'yi -51% -> -29%'a indirdi ama 2010-2026 CAGR'yi 14.7% -> 8.5%'e dusurdu.

## 5. Test 6b: Endustri momentumu x gunluk kaldirac x 200-DMA (onceden secilmis 8 varyant)

Gunluk 49 endustri VW verisiyle; secim aylik, tutma gunluk, kaldirac maliyeti T-bill+1%, ER 0.9%, 10 bp/devir ve gecis. Hucre: CAGR / MaxDD / Sharpe.

| Strateji | 1927-2026 | 1950-2026 | 2000-2026 | 2010-2026 | 2020-2026 |
|---|---|---|---|---|---|
| Ind49 K=6 s=0 top5 L=1 | 13.7 / -82 / 0.57 | 15.8 / -55 / 0.68 | 13.8 / -55 / 0.59 | 14.9 / -36 / 0.67 | 21.8 / -36 / 0.76 |
| Ind49 K=6 s=0 top5 L=1 +200DMA | 13.4 / -51 / 0.66 | 13.7 / -38 / 0.68 | 8.7 / -38 / 0.45 | 7.9 / -34 / 0.43 | 13.3 / -27 / 0.56 |
| Ind49 K=6 s=0 top5 L=2 | 17.5 / -99 / 0.53 | 22.3 / -82 / 0.62 | 17.9 / -82 / 0.55 | 21.4 / -63 / 0.63 | 31.1 / -61 / 0.72 |
| Ind49 K=6 s=0 top5 L=2 +200DMA | 20.3 / -82 / 0.64 | 20.6 / -64 / 0.65 | 11.5 / -64 / 0.43 | 9.7 / -57 / 0.40 | 18.2 / -51 / 0.54 |
| Ind49 K=12 s=1 top5 L=1 | 15.3 / -77 / 0.64 | 17.3 / -62 / 0.72 | 12.9 / -62 / 0.54 | 15.7 / -37 / 0.68 | 19.3 / -37 / 0.69 |
| Ind49 K=12 s=1 top5 L=1 +200DMA | 14.5 / -44 / 0.76 | 14.8 / -36 / 0.76 | 8.0 / -36 / 0.42 | 7.9 / -34 / 0.43 | 9.0 / -22 / 0.38 |
| Ind49 K=12 s=1 top5 L=2 | 20.9 / -97 / 0.59 | 24.9 / -89 / 0.67 | 15.3 / -89 / 0.50 | 22.5 / -64 / 0.64 | 26.2 / -63 / 0.65 |
| Ind49 K=12 s=1 top5 L=2 +200DMA | 23.1 / -75 / 0.73 | 23.0 / -62 / 0.72 | 10.1 / -62 / 0.40 | 9.8 / -57 / 0.40 | 9.5 / -45 / 0.36 |
| Piyasa 2x +200DMA (referans) | 15.8 / -60 / 0.63 | 16.3 / -58 / 0.65 | 8.1 / -58 / 0.37 | 14.1 / -41 / 0.60 | 17.2 / -35 / 0.63 |
| Piyasa 1x BH | 9.8 / -84 / 0.45 | 11.6 / -55 / 0.54 | 8.5 / -55 / 0.42 | 14.2 / -34 / 0.76 | 15.2 / -34 / 0.65 |


Bulgular: Uzun ornekte 2x endustri momentumu + 200DMA en yuksek CAGR'yi verdi (1927-2026 20.3-23.1%), ama 2000-2026'da 10-11.5%, 2010-2026'da 9.7-9.8% (MaxDD -57%), yani piyasa 2x+200DMA referansinin (14.1%) altinda. Filtresiz 2x endustri momentumu 2010-2026'da 21.4-22.5%, 2020-2026'da 26-31% ama MaxDD -61..-64% ve 1927-2026'da -97..-99%. Sektor rotasyonuna kaldirac eklemek getiriyi buyutuyor ama kotu donemleri de; filtre son 16 yilda yine pahali.

## 6. Test 3: Chen-Zimmermann anomalilerinin yayin sonrasi bozulmasi

IS = makalenin orneklem yillari; OOS = orneklem sonu..yayin yili; yayin sonrasi = yayin yili+1..2025. Uzun-kisa, aylik %, maliyet oncesi.

| Olcu | Deger |
|---|---|
| Sinyal sayisi (yayin sonrasi >=24 ay) | 209 / 212 |
| IS ortalama aylik LS getiri, medyan | 0.60% |
| OOS (orneklem sonu..yayin) medyan | 0.38% |
| Yayin sonrasi medyan | 0.24% |
| Yayin sonrasi / IS orani: medyan (sinyal bazli) | 0.38 |
| Yayin sonrasi / IS orani: ort(POST)/ort(IS) (havuzlanmis) | 0.45 |
| OOS / IS orani (havuzlanmis) | 0.62 |
| Yayin sonrasi t>2 olan pay | 24.9% |
| Yayin sonrasi ortalama negatif olan pay | 16.7% |
| 2010-2025 medyan aylik LS (OP tarzi) | 0.20%  (yillik ~2.4%) |
| 2010-2025 t>2 olan pay | 22.2% |
| 2016-2025 medyan aylik LS | 0.18% |
| 2021-2025 medyan aylik LS | 0.33% |
| 2010-2025 medyan, ME>NYSE20p likidite filtresi | 0.13% |
| 2010-2025 medyan, VWforce (deger agirlikli) | 0.07% |
| IS medyan, VWforce | 0.36% |


### 6.1 Aile bazli

| Aile | n | IS ort %/ay | Yayin-sonr %/ay | 2010-25 ort %/ay | 2010-25 medyan | 2010-25 >0 pay | 2010-25 t>2 pay | 2010-25 medyan Sharpe | 2010-25 ME>NYSE20p | 2010-25 VWforce | 2021-25 ort | POST/IS | R10/IS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Momentum/trend | 20 | 1.05 | 0.42 | 0.51 | 0.38 | 85.0% | 25.0% | 0.36 | 0.31 | 0.39 | 0.94 | 0.40 | 0.49 |
| Likidite/hacim/sahiplik | 27 | 0.75 | 0.46 | 0.46 | 0.19 | 70.4% | 25.9% | 0.17 | 0.23 | -0.01 | 0.42 | 0.60 | 0.61 |
| Deger (value) | 17 | 0.78 | 0.49 | 0.36 | 0.26 | 94.1% | 29.4% | 0.25 | 0.14 | -0.06 | 1.17 | 0.63 | 0.46 |
| Kisa vade reversal | 1 | 2.96 | 1.50 | 0.34 | 0.34 | 100.0% | 0.0% | 0.20 | 0.08 | -0.72 | -0.43 | 0.51 | 0.11 |
| Karlilik/kalite | 16 | 0.65 | 0.41 | 0.33 | 0.28 | 81.2% | 18.8% | 0.32 | 0.30 | 0.21 | 0.66 | 0.63 | 0.52 |
| Risk/volatilite/kaldirac | 22 | 0.64 | 0.26 | 0.26 | 0.22 | 81.8% | 13.6% | 0.21 | 0.14 | 0.16 | 0.39 | 0.40 | 0.41 |
| Mevsimsellik (MomSeason vb.) | 10 | 0.79 | 0.24 | 0.25 | 0.19 | 70.0% | 10.0% | 0.19 | 0.15 | 0.18 | 0.18 | 0.30 | 0.31 |
| Yatirim/ihrac | 38 | 0.56 | 0.22 | 0.23 | 0.16 | 78.9% | 18.4% | 0.29 | 0.21 | 0.10 | 0.30 | 0.39 | 0.41 |
| Kazanc/analist (PEAD ailesi) | 23 | 0.65 | 0.22 | 0.18 | 0.15 | 73.9% | 34.8% | 0.30 | 0.08 | 0.10 | 0.34 | 0.33 | 0.28 |
| Tahakkuk (accruals) | 5 | 0.51 | 0.19 | 0.17 | 0.13 | 60.0% | 40.0% | 0.30 | 0.12 | 0.14 | 0.45 | 0.38 | 0.34 |
| Diger | 27 | 0.50 | 0.18 | 0.15 | 0.09 | 48.1% | 22.2% | 0.10 | 0.15 | 0.13 | 0.00 | 0.36 | 0.31 |
| Uzun vade reversal | 6 | 0.53 | 0.26 | 0.05 | 0.12 | 66.7% | 0.0% | 0.12 | 0.05 | -0.05 | 0.25 | 0.49 | 0.09 |


### 6.2 2010-2025 t-istatistigine gore ilk 15 (EX-POST secim; coklu test yanliligi; opsiyon tabanli SmileSlope/CPVolSpread/dCPVolSpread 2022'de bitiyor)

| sig | fam | year | IS | POST | R10 | t10 | R10_ME>NYSE20p | R10_VWforce |
|---|---|---|---|---|---|---|---|---|
| SmileSlope | Risk/volatilite/kaldirac | 2011 | 1.83 | 0.85 | 0.89 | 6.26 | 0.65 | 0.83 |
| EarningsStreak | Kazanc/analist (PEAD ailesi) | 2012 | 1.09 | 0.67 | 0.62 | 4.84 | 0.37 | 0.31 |
| AnnouncementReturn | Kazanc/analist (PEAD ailesi) | 1996 | 1.14 | 0.80 | 0.59 | 4.12 | 0.24 | 0.34 |
| dCPVolSpread | Likidite/hacim/sahiplik | 2014 | 1.36 | 0.69 | 0.58 | 4.09 | 0.32 | 0.52 |
| VolumeTrend | Likidite/hacim/sahiplik | 1996 | 0.55 | 0.65 | 0.47 | 4.05 | 0.34 | 0.43 |
| XFIN | Yatirim/ihrac | 2006 | 1.07 | 1.23 | 1.39 | 3.60 | 0.45 | 0.55 |
| RIO_Volatility | Likidite/hacim/sahiplik | 2005 | 1.00 | 0.76 | 1.04 | 3.55 | 1.01 | -0.67 |
| ShareIss1Y | Yatirim/ihrac | 2008 | 0.69 | 0.94 | 1.13 | 3.38 | 0.41 | 0.36 |
| ShareIss5Y | Yatirim/ihrac | 2006 | 0.51 | 0.87 | 0.97 | 3.33 | 0.42 | 0.59 |
| CPVolSpread | Risk/volatilite/kaldirac | 2009 | 0.98 | 0.47 | 0.47 | 3.28 | 0.37 | 0.47 |
| ChTax | Diger | 2011 | 1.05 | 0.43 | 0.44 | 3.23 | 0.28 | 0.00 |
| MomVol | Momentum/trend | 2000 | 1.63 | 1.29 | 2.05 | 3.23 | 1.04 | 0.86 |
| ShortInterest | Likidite/hacim/sahiplik | 2001 | 0.81 | 0.99 | 0.95 | 3.21 | 0.27 | 0.20 |
| Mom12mOffSeason | Mevsimsellik (MomSeason vb.) | 2008 | 1.29 | 0.94 | 1.62 | 3.16 | 1.08 | 1.37 |
| RevenueSurprise | Kazanc/analist (PEAD ailesi) | 2006 | 0.73 | 0.37 | 0.43 | 3.15 | 0.26 | 0.14 |


### 6.3 PEAD/kazanc ve momentum sinyalleri on yillara gore (%/ay, LS)

| Sinyal | Yayin | Agirlik | 1970-89 | 1990-99 | 2000-09 | 2010-19 | 2020-25 | 2010-25 ME>NYSE20p |
|---|---|---|---|---|---|---|---|---|
| AnnouncementReturn | 1996 | EW | 1.03 | 1.34 | 1.05 | 0.72 | 0.37 | 0.24 |
| EarningsSurprise | 1984 | EW | 1.12 | 0.63 | 0.26 | 0.05 | 0.46 | 0.04 |
| EarningsStreak | 2012 | EW | 1.45 | 1.39 | 0.66 | 0.41 | 0.97 | 0.37 |
| EarnSupBig | 2007 | EW | 0.59 | -0.10 | 0.18 | 0.04 | 1.03 | 0.14 |
| RevenueSurprise | 2006 | EW | 0.68 | 0.56 | 0.61 | 0.49 | 0.34 | 0.26 |
| AnalystRevision | 1984 | EW | 1.11 | 1.05 | 0.31 | 0.14 | 0.16 | 0.14 |
| REV6 | 1996 | EW | 1.05 | 1.04 | 0.50 | 0.52 | 0.76 | 0.43 |
| ChangeInRecommendation | 2004 | EW |  | 1.15 | 0.59 | 0.25 | 0.28 | 0.13 |
| EarningsConsistency | 2009 | EW | 0.17 | 0.08 | 0.33 | 0.34 | 0.33 | 0.17 |
| NumEarnIncrease | 2012 | EW | 0.59 | 0.55 | 0.41 | 0.26 | 0.40 | 0.23 |
| STreversal | 1990 | EW | 3.35 | 3.28 | 1.73 | 0.36 | 0.31 | 0.08 |
| IndMom | 1999 | EW | 0.18 | 0.42 | 0.80 | -0.09 | 0.34 | 0.04 |
| Mom12m | 1993 | EW | 1.28 | 0.83 | -0.40 | 1.25 | 1.94 | 0.73 |
| Mom6m | 1993 | EW | 0.70 | 0.29 | 0.80 | 0.69 | 2.13 | 0.74 |
| ResidualMomentum | 2011 | EW | 1.11 | 1.67 | 0.65 | 0.05 | 0.79 | 0.15 |
| IntMom | 2012 | VW | 2.18 | 1.95 | 0.42 | 0.66 | 0.84 | 0.16 |
| MomSeason | 2008 | EW | 0.69 | 1.07 | 1.01 | 0.26 | -0.60 | -0.09 |


### 6.4 Sadece-uzun ust portfoyler (Test 6c): VW piyasaya karsi ve boyut-notr

**(c) Sadece-uzun ust portfoy - CRSP VW piyasa (aylik fazla getiri, maliyet oncesi); ayrica ust portfoy - ayni sinyalin tum portfoylerinin ortalamasi (boyut etkisini ayiklar)**

| Sinyal | Versiyon | Donem | Ust_port | Ort_fazla_ay | Yillik | t | Ust_eksi_portort_yillik | t2 |
|---|---|---|---|---|---|---|---|---|
| AnnouncementReturn | OP | 1990-2009 | 05 | 1.07% | 12.8% | 3.73 | 8.3% | 6.69 |
| AnnouncementReturn | OP | 2010-2025 | 05 | -0.12% | -1.4% | -0.52 | 2.7% | 3.29 |
| AnnouncementReturn | OP | 2020-2025 | 05 | -0.42% | -5.0% | -0.84 | 1.6% | 0.97 |
| AnnouncementReturn | ME>NYSE20p | 1990-2009 | 05 | 0.60% | 7.2% | 2.53 | 5.2% | 3.55 |
| AnnouncementReturn | ME>NYSE20p | 2010-2025 | 05 | -0.17% | -2.1% | -0.88 | 0.9% | 1.00 |
| AnnouncementReturn | ME>NYSE20p | 2020-2025 | 05 | -0.43% | -5.1% | -1.03 | 0.3% | 0.17 |
| EarningsStreak | OP | 1990-2009 | 05 | 0.75% | 8.9% | 4.10 | 7.2% | 9.30 |
| EarningsStreak | OP | 2010-2025 | 05 | 0.06% | 0.7% | 0.29 | 2.6% | 2.67 |
| EarningsStreak | OP | 2020-2025 | 05 | 0.18% | 2.2% | 0.41 | 6.1% | 3.15 |
| EarningsStreak | ME>NYSE20p | 1990-2009 | 05 | 0.69% | 8.3% | 3.36 | 6.0% | 6.08 |
| EarningsStreak | ME>NYSE20p | 2010-2025 | 05 | -0.01% | -0.2% | -0.06 | 1.4% | 1.31 |
| EarningsStreak | ME>NYSE20p | 2020-2025 | 05 | 0.14% | 1.7% | 0.30 | 5.0% | 2.23 |
| REV6 | OP | 1990-2009 | 05 | 0.75% | 9.0% | 2.85 | 5.9% | 4.63 |
| REV6 | OP | 2010-2025 | 05 | -0.09% | -1.0% | -0.28 | 1.8% | 1.01 |
| REV6 | OP | 2020-2025 | 05 | 0.13% | 1.6% | 0.20 | 5.7% | 1.50 |
| REV6 | ME>NYSE20p | 1990-2009 | 05 | 0.46% | 5.5% | 2.19 | 3.0% | 2.50 |
| REV6 | ME>NYSE20p | 2010-2025 | 05 | 0.03% | 0.4% | 0.14 | 2.2% | 1.58 |
| REV6 | ME>NYSE20p | 2020-2025 | 05 | 0.30% | 3.5% | 0.60 | 7.1% | 2.46 |
| EarningsSurprise | OP | 1990-2009 | 10 | 0.47% | 5.7% | 2.96 | 2.9% | 3.51 |
| EarningsSurprise | OP | 2010-2025 | 10 | -0.06% | -0.7% | -0.35 | 0.6% | 0.72 |
| EarningsSurprise | OP | 2020-2025 | 10 | -0.04% | -0.5% | -0.13 | 2.5% | 1.48 |
| EarningsSurprise | ME>NYSE20p | 1990-2009 | 10 | 0.33% | 4.0% | 2.00 | 0.8% | 0.86 |
| EarningsSurprise | ME>NYSE20p | 2010-2025 | 10 | -0.10% | -1.2% | -0.61 | -0.2% | -0.21 |
| EarningsSurprise | ME>NYSE20p | 2020-2025 | 10 | -0.03% | -0.4% | -0.09 | 1.7% | 0.91 |
| RevenueSurprise | OP | 1990-2009 | 05 | 0.78% | 9.4% | 3.48 | 3.0% | 4.16 |
| RevenueSurprise | OP | 2010-2025 | 05 | 0.03% | 0.4% | 0.19 | 2.2% | 2.41 |
| RevenueSurprise | OP | 2020-2025 | 05 | 0.00% | 0.1% | 0.01 | 1.6% | 0.80 |
| RevenueSurprise | ME>NYSE20p | 1990-2009 | 05 | 0.27% | 3.2% | 1.62 | 0.1% | 0.13 |
| RevenueSurprise | ME>NYSE20p | 2010-2025 | 05 | 0.07% | 0.8% | 0.45 | 1.7% | 1.88 |
| RevenueSurprise | ME>NYSE20p | 2020-2025 | 05 | -0.00% | -0.0% | -0.01 | 1.6% | 0.80 |
| AnalystRevision | OP | 1990-2009 | 05 | 0.63% | 7.6% | 2.84 | 4.2% | 3.73 |
| AnalystRevision | OP | 2010-2025 | 05 | -0.20% | -2.4% | -0.86 | 0.3% | 0.30 |
| AnalystRevision | OP | 2020-2025 | 05 | -0.15% | -1.8% | -0.30 | 3.5% | 2.10 |
| AnalystRevision | ME>NYSE20p | 1990-2009 | 05 | 0.50% | 6.0% | 2.63 | 4.1% | 3.58 |
| AnalystRevision | ME>NYSE20p | 2010-2025 | 05 | -0.13% | -1.6% | -0.68 | 0.1% | 0.07 |
| AnalystRevision | ME>NYSE20p | 2020-2025 | 05 | -0.14% | -1.7% | -0.35 | 2.0% | 1.29 |
| Mom12m | OP | 1990-2009 | 10 | 0.66% | 7.9% | 1.95 | 3.1% | 0.96 |
| Mom12m | OP | 2010-2025 | 10 | -0.02% | -0.3% | -0.08 | 3.5% | 1.50 |
| Mom12m | OP | 2020-2025 | 10 | 0.08% | 1.0% | 0.13 | 6.6% | 1.37 |
| Mom12m | ME>NYSE20p | 1990-2009 | 10 | 0.51% | 6.2% | 1.41 | 4.0% | 1.08 |
| Mom12m | ME>NYSE20p | 2010-2025 | 10 | 0.09% | 1.0% | 0.29 | 3.2% | 1.22 |
| Mom12m | ME>NYSE20p | 2020-2025 | 10 | 0.31% | 3.7% | 0.53 | 7.9% | 1.49 |
| Mom6m | OP | 1990-2009 | 10 | 0.85% | 10.1% | 2.41 | 5.9% | 1.81 |
| Mom6m | OP | 2010-2025 | 10 | -0.25% | -3.0% | -0.82 | 1.1% | 0.50 |
| Mom6m | OP | 2020-2025 | 10 | -0.08% | -0.9% | -0.11 | 5.2% | 1.16 |
| Mom6m | ME>NYSE20p | 1990-2009 | 10 | 0.69% | 8.3% | 1.82 | 6.4% | 1.73 |
| Mom6m | ME>NYSE20p | 2010-2025 | 10 | -0.02% | -0.2% | -0.07 | 2.2% | 0.87 |
| Mom6m | ME>NYSE20p | 2020-2025 | 10 | 0.20% | 2.4% | 0.34 | 7.1% | 1.42 |
| IndMom | OP | 1990-2009 | 03 | 0.60% | 7.1% | 2.09 | 3.2% | 1.79 |
| IndMom | OP | 2010-2025 | 03 | -0.42% | -5.1% | -1.97 | -0.6% | -0.59 |
| IndMom | OP | 2020-2025 | 03 | -0.54% | -6.5% | -1.19 | 0.3% | 0.17 |
| IndMom | ME>NYSE20p | 1990-2009 | 03 | 0.29% | 3.5% | 1.17 | 1.8% | 0.93 |
| IndMom | ME>NYSE20p | 2010-2025 | 03 | -0.23% | -2.8% | -1.34 | -0.1% | -0.14 |
| IndMom | ME>NYSE20p | 2020-2025 | 03 | -0.33% | -3.9% | -0.94 | 1.0% | 0.73 |


### 6.5 Yayin donemi ve tum-anomali ortalamasi

**Yayin donemine gore**

| yayin_grup | n | IS | POST | R10 | POST/IS |
|---|---|---|---|---|---|
| <=1995 | 28 | 0.79 | 0.44 | 0.24 | 0.56 |
| 1996-2005 | 74 | 0.62 | 0.30 | 0.31 | 0.49 |
| 2006-2016 | 110 | 0.71 | 0.28 | 0.29 | 0.40 |

**Tum anomalilerin esit agirlikli ortalamasi (her ay mevcut sinyaller), ortalama yillik getiri**

| 1963-1979 | 1980-1999 | 2000-2009 | 2010-2019 | 2020-2025 |
|---|---|---|---|---|
| 6.1% | 8.0% | 7.2% | 2.9% | 4.7% |


**Test 3 bulgulari**
- Bozulma McLean & Pontiff (2016, JF, doi:10.1111/jofi.12365; bellekten: OOS ~%26, yayin sonrasi ~%58 dusus) ile uyumlu: bizim havuzlanmis oranlarimiz OOS/IS 0.62 (%38 dusus), yayin sonrasi/IS 0.45 (%55 dusus); sinyal-bazli medyan 0.38.
- 2010-2025'te tum anomalilerin esit agirlikli ortalamasi ~2.9%/yil (2010-19) ve 4.7%/yil (2020-25), maliyet oncesi, uzun-kisa. Bu, %15-20 USD hedefinin cok altinda; kaldirac gerektirir ve maliyetler (Novy-Marx & Velikov 2016 RFS, doi:10.1093/rfs/hhv063; bellekten) yuksek devirli olanlari sifirliyor.
- Uygulanabilir versiyonlarda (VWforce) 2010-2025 medyan 0.07%/ay; yani "anomali avciligi" ile likit hisselerde ciddi alfa yok.
- 2010 sonrasi en iyi ayakta kalan aileler: momentum/trend (ozellikle Mom12m, Mom6m 2020-25: 1.9-2.1%/ay LS, ama EW ve kisa bacak agirlikli), value (2021-25'te 1.17%/ay toparlanma), likidite/hacim. En kotu: uzun vade reversal, kisa vade reversal, mevsimsellik, "diger".
- PEAD: AnnouncementReturn (yayin 1996) 1990'larda 1.34, 2000'lerde 1.05, 2010'larda 0.72, 2020'lerde 0.37 %/ay — monoton dusus. Likidite filtresiyle 2010-25 sadece 0.24%/ay.

## 7. Test 5: Kisa vade reversal


**French ST_Rev (onceki ay kaybedenler - kazananlar, VW 2x3), brut; net = VARSAYIMSAL maliyet**

| Donem | Ay | Ort_ay | Yillik | t | Sharpe | Pozitif_yil | Gunluk_STR_yillik | Gunluk_Sharpe | Net_yillik_c5bp | Net_yillik_c10bp | Net_yillik_c20bp |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1927-2026 | 1197 | 0.6% | 7.6% | 6.35 | 0.64 | 75.0% | 56.0% | 3.76 | 5.5% | 3.3% | -1.0% |
| 1963-1989 | 324 | 0.8% | 9.3% | 5.44 | 1.05 | 96.3% | 30.7% | 3.62 | 7.2% | 5.0% | 0.7% |
| 1990-2009 | 240 | 0.2% | 2.8% | 0.94 | 0.21 | 55.0% | 28.1% | 1.97 | 0.6% | -1.5% | -5.9% |
| 2010-2026 | 201 | 0.0% | 0.1% | 0.04 | 0.01 | 52.9% | 5.6% | 0.40 | -2.0% | -4.2% | -8.5% |
| 2020-2026 | 81 | -0.4% | -5.2% | -1.01 | -0.39 | 28.6% | 5.1% | 0.26 | -7.4% | -9.5% | -13.8% |

**2010+ takvim yili getirileri (2026 = Ocak-Eylul)**

| Yil | ST_Rev | UMD |
|---|---|---|
| 2010 | 8.4% | 6.3% |
| 2011 | -6.1% | 8.2% |
| 2012 | 6.1% | -1.4% |
| 2013 | -1.5% | 5.4% |
| 2014 | -2.6% | 0.7% |
| 2015 | 1.3% | 21.1% |
| 2016 | 5.5% | -18.2% |
| 2017 | 3.5% | 3.8% |
| 2018 | 3.9% | 10.7% |
| 2019 | 17.1% | -5.5% |
| 2020 | -7.4% | -0.9% |
| 2021 | 4.0% | -2.9% |
| 2022 | -6.5% | 20.2% |
| 2023 | 4.7% | -20.5% |
| 2024 | -8.3% | 18.5% |
| 2025 | -18.0% | -2.2% |
| 2026 | -6.5% | 11.0% |


Bulgular: ST_Rev 1963-89'da yillik 9.3% brut (Sharpe 1.05), 1990-2009'da 2.8%, 2010-2026'da 0.1% (t=0.04), 2020-2026'da -5.2%. Gunluk-rebalans gunluk ST_Rev brut 2010-2026'da 5.6%/yil ama gunluk tam devirle uygulanamaz. Net hesap varsayimsal (aylik bacak basina %90 tek-yon devir); 10 bp ile 2010-2026 net -4.2%/yil. BIST lead-lag calismasindaki 1-3 gunluk kucuk/kirilgan edge'lerin ABD karsiligi da ayni sekilde bozulmus gorunuyor.

## 8. Test 4: Earnings gap / episodic pivot — YAPILAMADI

- Gunluk hisse verisi icin denenen kaynaklar: Stooq (https://stooq.com/q/d/l/?s=spy.us&i=d) baglanti sifirlama (curl 35, proxy kaydinda tekrarlayan "tunnel closed"); Yahoo chart API varsayilan basliklarla HTTP 429 "Too Many Requests". Kurallar geregi (UA taklidi / bot-kontrolu asma yok) yeniden denenmedi. yfinance kutuphanesi tarayici taklidi yaptigi icin kullanilmadi.
- Vekil olarak CZ'nin olay-tabanli sinyalleri kullanildi (AnnouncementReturn = kazanc aciklamasi etrafindaki 3 gunluk getiri; EarningsSurprise, EarningsStreak, RevenueSurprise, REV6). Sonuc (6.3-6.4): uzun-kisa getiri 2010 sonrasi azalarak suruyor; sadece-uzun ust portfoy VW piyasayi gecmiyor.
- Not: "gap > %5-10, hacim > 3x" tipi episodic pivot kurallarinin akademik/audit edilmis bir uzun donem kaydini bu oturumda bulamadik/test edemedik; populer trader iddialari (ornegin sosyal medya/kurs pazarlamasi) hayatta kalan secilimi ve dogrulanmamis kayit riski tasir. Bu test icin onerilen yol: CRSP/WRDS veya ucretli ama mesru bir gunluk veri saglayicisi (survivorship-free, delist dahil) ile yeniden calistirmak.

## 9. Kullanici icin cikarimlar (swing, haftalar-aylar, kumelenmis pozisyonlar)

1. **Gercekci beklenti tablosu (USD, vergi oncesi, 5 yillik kayan pencere, 1990+)**: NDX 1x BH medyan 16.3% (P10 -1.9%); NDX 2x+200DMA medyan 18.2% (P10 2.8%, MaxDD tarihsel -41..-86%); NDX 3x+200DMA medyan 22.1% (P10 -0.6%, MaxDD -55..-97%); piyasa 2x+200DMA 12.9%. Kaldiracsiz momentum/sektor rotasyonu: 2010-2026'da piyasa +0..+4 puan.
2. **TL carry ile kiyas**: Bugunku ~%16-22 USD carry'yi gecmek icin ABD tarafinda en az 2x kaldiracli bir trend/momentum yapisi gerekiyor; ama carry'nin kendisi -%85 MaxDD gecmisine sahip. Iki riskli varligi karsilastiriyorsunuz, risksiz ile riskliyi degil.
3. **Kumelenme (strategic clustering) tarziniza en yakin, kanitli yapi**: tema/sektor seviyesinde momentum (12-1 ay veya 6 ay), ayda bir rebalans, 3-5 kume; kaldiraci kume seviyesinde degil portfoy seviyesinde ve trend filtresine bagli uygulamak. Kanit: uzun ornekte +2..+4 puan, son 16 yilda ~0..+2 puan; yani bu bir "edge" degil, "kotu temalardan uzak durma" disiplini.
4. **Kacinilmasi gerekenler (veriye gore)**: kisa vade reversal (oldu), uzun-kisa faktor yatirimi (maliyet ve kisa bacak), 3x NDX'i filtre ile "guvenli" sanmak (2000-02: -89%), backtest MaxDD'sine guvenmek (lag1 ile 20 puan oynuyor).
5. **Uygulama (Turk mukimi) — dogrulanmasi gereken noktalar**: ABD-domisilli LETF'lere (UPRO/TQQQ/SSO/QLD) yurt disi araci kurum ile erisim AB PRIIPs kisitina tabi degil gibi gorunuyor; ABD gayrimukimler icin $60k ustu ABD varliklarinda veraset vergisi riski; temettu stopaji (ABD-Turkiye anlasmasi) ve Turkiye'de yurt disi menkul kazancinin beyani. Bu oturumda web aramasi tukendigi icin dogrulanmadi; ayri bir dogrulama gerekli.
6. **Su anki durum (FRED, 2026-11-04/05)**: S&P 500 200-DMA'nin %5.0 ustunde (zirveden -1.7%, YTD +12.3%); Nasdaq-100 200-DMA'nin %4.8 altinda (zirveden -14.7%, Ekim -6.7%, Kasim ilk 4 gun -6.2%). Yani NDX trend kurali su an "disarida", SPX kurali "iceride". (Bilgi amacli; tavsiye degil.)

## 10. Ek: dosyalar
- Kod: ortak.py, test1_momentum.py, test2_kaldiracli_trend.py, test3_cz_decay.py, test5_strev.py, test6_kombine_ve_engel.py, test7_kayan_pencere.py, rapor_olustur.py
- Ciktilar: hesaplar/abd_test/cikti/ (t1_ozet.csv, t1_izgara.csv, t2_ozet.csv, t2_izgara.csv, t2_kriz.csv, t3_sinyal_bazli.csv, t6_kombine.csv ve *_tablolar.md)
- Calistirma: `python3 -I hesaplar/abd_test/testN_*.py` (veri yolu ortak.py icinde DATA)
