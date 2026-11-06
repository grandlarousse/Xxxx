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

{{t6a}}

Yorum: Mevcut "ortodoks" rejimde (2024-2026) TL carry USD bazinda brut ~%21/yil verdi; stopaj (~%15-17.5, dogrulanmali) dusulunce ~%16-18. Bu, kullanicinin ABD stratejisi icin bugunku firsat maliyetidir. Ancak ayni carry 2010-2026'da USD bazinda -%7.2/yil ve -%85 MaxDD; 2018 ve 2021 kur soklari tipik. Yani engel "risksiz %40-50 TL" degil, "kuyruk riski yuksek ~%15-20 USD carry"dir. Karsilastirmada ABD stratejisinin MaxDD'si bu carry'nin MaxDD'siyle birlikte okunmali. Not: shared context'teki Fed funds 3.75-4.00% bandi FRED ile uyumlu (DFEDTARU 4.00, DFF 3.88, DTB3 4.03).

## 3. Test 2: Kaldiracli trend (sentetik 1x/2x/3x, 200-DMA ve 10-ay SMA)

Hucre formati: **CAGR % / MaxDD % / Sharpe** (Sharpe = T-bill ustu ortalama / vol). Spread T-bill+1%, ER 0.9%, 10 bp/gecis. "1926-2026 (tam)" MKT icin 1927-04'te (200 gun isinma sonrasi), NDX "1986-2026 (tam)" 1986-10'da baslar. MKT 2026-09-30, NDX 2026-11-05'te biter.

### 3.1 lag0 (t kapanis sinyali, t+1 uygulama)
{{t2k0}}

### 3.2 lag1 (1 gun ek gecikme; daha gercekci)
{{t2k1}}

### 3.3 Tam istatistikler (lag0, spread 1%, 10bp): en kotu yil, T-bill ustu CAGR, yillik gecis
{{t2full}}

### 3.4 Robustluk izgarasi (MA 100/150/200/250 gun x bant 0/1/2% x lag 0/1 x maliyet 0/10/25 bp = 72 kombinasyon, spread 1%)
{{t2grid}}

### 3.5 Kriz pencereleri (lag0, maliyetsiz, spread 1%): pencere getirisi / pencere ici MaxDD
{{t2crisis}}

### 3.6 Kayan pencere: baslangic tarihi sansina duyarlilik (lag1, 10bp, spread 1%) (Test 7)
{{t7}}

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
{{t1k}}

### 4.1 Endustri momentum izgarasi (K 3/6/9/12 ay x skip 0/1 x N; 49 endustride N 3/5/10, 12 endustride N 3/5), 10 bp/devir
{{t1grid}}

### 4.2 Izgara medyani vs benchmark (EW endustri ve CRSP VW piyasa)
{{t1diff}}

### 4.3 Momentum crash ve vol-yonetim
{{t1crash}}

### 4.4 UMD on yillara gore
{{t1dec}}

**Test 1 bulgulari**
- UMD'nin primi 2000'den beri kayboldu (2000'ler -2.0%/yil, 2010'lar +2.6%, 2020'ler +2.5%). Vol-yonetim crash'leri yumusatiyor (2009-04: -34.4% -> -10.1%) ve tam ornekte Sharpe'i ikiye katliyor (0.45 -> 0.81; Barroso & Santa-Clara 2015 JFE, doi:10.1016/j.jfineco.2014.11.010, bellekten: 0.53 -> 0.97), ama 2010 sonrasi mutlak getiri T-bill +4.7 puan (2010-2026). Uzun-kisa momentum ayrica bireysel yatirimci icin aciga satis maliyeti nedeniyle pratik degil.
- Sadece-uzun VW ust desil 2010-2026'da 17.8% (piyasa 14.1%), 2020-2026 21.6% (15.0%); ancak vol 22-27% ve Sharpe piyasadan yuksek degil. Bu MTUM tipi bir urunun ust siniri (ust desil, maliyetsiz, aylik rebalans).
- Endustri rotasyonu: uzun ornekte saglam (+2..+4 puan, tum kombinasyonlar piyasanin ustunde), 2010-2026'da yaklasik sifir alfa (+0.1/+0.5 puan). 2020-2026'daki +1..+4 puan, enerji ve AI temalarina denk geliyor; rejim bagimli.
- Endustri momentumuna piyasa 10-ay SMA filtresi eklemek 1950-2026'da MaxDD'yi -51% -> -29%'a indirdi ama 2010-2026 CAGR'yi 14.7% -> 8.5%'e dusurdu.

## 5. Test 6b: Endustri momentumu x gunluk kaldirac x 200-DMA (onceden secilmis 8 varyant)

Gunluk 49 endustri VW verisiyle; secim aylik, tutma gunluk, kaldirac maliyeti T-bill+1%, ER 0.9%, 10 bp/devir ve gecis. Hucre: CAGR / MaxDD / Sharpe.
{{t6k}}

Bulgular: Uzun ornekte 2x endustri momentumu + 200DMA en yuksek CAGR'yi verdi (1927-2026 20.3-23.1%), ama 2000-2026'da 10-11.5%, 2010-2026'da 9.7-9.8% (MaxDD -57%), yani piyasa 2x+200DMA referansinin (14.1%) altinda. Filtresiz 2x endustri momentumu 2010-2026'da 21.4-22.5%, 2020-2026'da 26-31% ama MaxDD -61..-64% ve 1927-2026'da -97..-99%. Sektor rotasyonuna kaldirac eklemek getiriyi buyutuyor ama kotu donemleri de; filtre son 16 yilda yine pahali.

## 6. Test 3: Chen-Zimmermann anomalilerinin yayin sonrasi bozulmasi

IS = makalenin orneklem yillari; OOS = orneklem sonu..yayin yili; yayin sonrasi = yayin yili+1..2025. Uzun-kisa, aylik %, maliyet oncesi.
{{t3all}}

### 6.1 Aile bazli
{{t3fam}}

### 6.2 2010-2025 t-istatistigine gore ilk 15 (EX-POST secim; coklu test yanliligi; opsiyon tabanli SmileSlope/CPVolSpread/dCPVolSpread 2022'de bitiyor)
{{t3top}}

### 6.3 PEAD/kazanc ve momentum sinyalleri on yillara gore (%/ay, LS)
{{t3pead}}

### 6.4 Sadece-uzun ust portfoyler (Test 6c): VW piyasaya karsi ve boyut-notr
{{t6c}}

### 6.5 Yayin donemi ve tum-anomali ortalamasi
{{t3pub}}

**Test 3 bulgulari**
- Bozulma McLean & Pontiff (2016, JF, doi:10.1111/jofi.12365; bellekten: OOS ~%26, yayin sonrasi ~%58 dusus) ile uyumlu: bizim havuzlanmis oranlarimiz OOS/IS 0.62 (%38 dusus), yayin sonrasi/IS 0.45 (%55 dusus); sinyal-bazli medyan 0.38.
- 2010-2025'te tum anomalilerin esit agirlikli ortalamasi ~2.9%/yil (2010-19) ve 4.7%/yil (2020-25), maliyet oncesi, uzun-kisa. Bu, %15-20 USD hedefinin cok altinda; kaldirac gerektirir ve maliyetler (Novy-Marx & Velikov 2016 RFS, doi:10.1093/rfs/hhv063; bellekten) yuksek devirli olanlari sifirliyor.
- Uygulanabilir versiyonlarda (VWforce) 2010-2025 medyan 0.07%/ay; yani "anomali avciligi" ile likit hisselerde ciddi alfa yok.
- 2010 sonrasi en iyi ayakta kalan aileler: momentum/trend (ozellikle Mom12m, Mom6m 2020-25: 1.9-2.1%/ay LS, ama EW ve kisa bacak agirlikli), value (2021-25'te 1.17%/ay toparlanma), likidite/hacim. En kotu: uzun vade reversal, kisa vade reversal, mevsimsellik, "diger".
- PEAD: AnnouncementReturn (yayin 1996) 1990'larda 1.34, 2000'lerde 1.05, 2010'larda 0.72, 2020'lerde 0.37 %/ay — monoton dusus. Likidite filtresiyle 2010-25 sadece 0.24%/ay.

## 7. Test 5: Kisa vade reversal

{{t5}}

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
