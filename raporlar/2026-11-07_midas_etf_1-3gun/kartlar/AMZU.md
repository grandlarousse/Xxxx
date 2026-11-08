# AMZU — Direxion Daily AMZN Bull 2X ETF

**TradingView:** `NASDAQ:AMZU` · **Aile:** Tek hisse kaldıraçlı · **İzleme kararı:** kabul  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 83 | 16,0 | 424 | %-11,1 | 2,0x | 2022-09-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** B10 sepetinin AMZN aracı (sinyal NASDAQ:AMZN). Medyan günlük hacim 83 mn$, maliyet 16,0 bp, maliyet/1g oynaklık 0,038. Gerçekleşen kaldıraç son 1y 1,99 (2024 başına kadar 1,5x idi). 1y getiri -%8, son 1y en kötü gün -%11,1. Midas'ta bulunurluğu resmî doğrulanmadı.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt ya da yalnız filtre — tek başına işlem gerekçesi değil)

#### B10 — Mega-cap hisse RSI(2) dibi (hisse 200 günlük ortalamanın üstünde) -> 2x tek hisse ETF, SMA5'e dönüşte çıkış (en çok 3 gün)  
*İzlemede — zayıf kanıt · güven: dusuk · aile kimliği: `tek_hisse_kaldiracli_S1`*  
*Bu ETF'nin rolü: AMZN'nin 2x aracı*

- **Sinyal (t kapanışında):** TradingView günlük grafik, sinyal DAYANAK HİSSENİN verisinden (ETF'nin kendi fiyatından değil): NASDAQ:NVDA, NASDAQ:TSLA, NASDAQ:AAPL, NASDAQ:AMZN, NASDAQ:META, NASDAQ:MSFT, NASDAQ:GOOGL. Göstergeler (kaynak: kapanış): RSI uzunluk 2 (standart Wilder RSI), SMA 200, SMA 5. Giriş sinyali t günü: hisse RSI(2) < 10 VE hisse kapanışı > hisse SMA(200). İşlem aracı (aynı hissenin 2x ETF'i): NVDA->NASDAQ:NVDL, TSLA->NASDAQ:TSLL, AAPL->NASDAQ:AAPU, AMZN->NASDAQ:AMZU, META->NASDAQ:METU, MSFT->NASDAQ:MSFU, GOOGL->NASDAQ:GGLL. Çıkış: girişten sonraki işlem günlerinde hisse kapanışı > hisse SMA(5) olan ilk gün kapanışta sat; olmazsa girişten sonraki 3. işlem günü kapanışında sat. Aynı hissede pozisyondayken gelen yeni sinyal yok sayılır; hisseler birbirinden bağımsız işlenir (aynı anda birden çok pozisyon olabilir: medyan 2, en çok 7). Stop yok (backtest stopsuz). Bilanço: ana kural bilançoyu taşır (işlemlerin ~%4'ü). Muhafazakâr varyant: sinyal günü ile t+3 arasında seans sonrası bilanço duyurusu varsa girme, pozisyondaysan duyuru günü kapanıştan önce çık (bu varyant C0 +84 bp, t=2,44; bkz. notlar).
- **Giriş:** C0 (ana): sinyal günü kapanıştan hemen önce (TR kış 23:45-23:58, yaz 22:45-22:58) hissenin canlı fiyatıyla RSI(2) ve SMA200'ü kontrol edip ETF'i normal seansta piyasa ya da agresif limit emirle al (Midas'ta MOC/LOC yok). RSI(2) son fiyata çok duyarlı: eşiğe yakınsa O1'i kullan. O1 (yedek, kapanış izlemeye gerek yok): ertesi gün açılışta al, TR kış 17:30 (yaz 16:30); pre-market (TR kış 12:00-17:30) yalnız limit emir.
- **Tutuş / çıkış:** En çok 3 işlem günü (ortalama 2,5 gün: işlemlerin %62'si 3 gün, %22'si 2 gün, %15'i 1 gün). — Her işlem günü kapanıştan hemen önce (TR kış 23:45-23:58, yaz 22:45-22:58) hisse fiyatı kendi SMA(5)'inin üstündeyse ETF'i sat; değilse sinyal gününden sonraki 3. işlem günü (t+3) aynı saatte sat. C0'da kontrol t+1, t+2, t+3 kapanışlarında; O1'de giriş günü (t+1) kapanışından itibaren, en geç t+3. Kapanış sonrası (TR kış 00:00-04:00) yalnız limit emirle satılabilir; backtest kapanış fiyatını kullanır.
- **İşlem aracı:** NVDL, TSLL, AAPU, AMZU, METU, MSFU, GGLL (sinyal: Dayanak hisseler: NASDAQ:NVDA, NASDAQ:TSLA, NASDAQ:AAPL, NASDAQ:AMZN, NASDAQ:META, NASDAQ:MSFT, NASDAQ:GOOGL)
- **Geçmiş (ajan):** n=605, net 111.0 bp/işlem (brüt 128.1), kazanma %64, t=3.13, IS 103.8 / OOS 117.1 bp, yılların %80'i pozitif, en kötü işlem -4457 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** C0: net 120 bp (t 2,7, gün kümeli t 2,7, n=261) · O1: net 104 bp (t 2,5, gün kümeli t 2,4, n=261) · C1: net 98 bp (t 2,1, gün kümeli t 1,7, n=242); 1.000 $ pozisyonda ana mod net 102 bp (t 2,3)
- **Denetçi düzeltmesi:** maxDD (günlük değerlemeli, 1/7 sermaye): -%25,3 (ajan -%11,5); 2020 dışı -%14,8. Bilanço uygulanabilir: ATLA C0 79,4 bp t=2,33, pozitif yıl %50; ERKEN ÇIK C0 98,4 t=2,87, O1 75,1 t=2,39 (OOS 53,5 t=1,44). 2020+2024 hariç: C0 52 bp t=1,42 (OOS 44 t=0,79). Ex-ante evren (B10 dışı 47 hisse): net 11,5 bp t=0,77, kenar 5,5 bp t=0,37. Günlük portföy NW t: C0 2,75, O1 2,29. Güncel durum (06.11.2026): NVDA, TSLA, META, GOOGL SMA200 altında; filtre açık yalnız AAPL, AMZN, MSFT; RSI2<10 olan yok. Toplam test ~7.800 (ajan 7.310 + denetim ~490); B10 p=0,0019, birleşik FDR'yi geçmiyor.
- **Denetçi kural düzeltmesi:** Ana kural aynı (TH03). Değişiklikler: (a) Bilanço: tepki günü t+1..t+3 içindeyse gir, ama duyuru günü (E, seans sonrası duyuru) kapanışından önce sat ('ERKEN ÇIK'; C0 98,4 bp t=2,87, IS 103,7 t=2,03, OOS 93,9 t=2,03, pozitif yıl %70). Ajanın 'bilanço hariç +84 bp' sayısı uygulanabilir değil. (b) 15:45 ET'de (TR kış 23:45) RSI(2) 7-13 aralığındaysa C0 yerine O1 kullan (ertesi açılış; 101 bp t=2,93). (c) Sermaye: her hisseye en çok 1/7; 7 pozisyon aynı anda açılabilir; günlük değerlemeli maxDD -%25. (d) Alternatif araç: aynı sinyalle hissenin kendisi. Midas'ta kesin var; 1x C0 2.500$ net 57,9 bp t=3,27, 5.000$ 63,9 bp t=3,61; swap sürüklemesi ve ürün bulunurluğu riski yok.
- **Denetim:** Bağımsız simülasyonla birebir yeniden üretildi (lib.trades/evaluate/thk kullanılmadı; RSI Wilder/RMA, SMA, sentetik 2x ve havuz kendi kodum). 605 işlemin 605'i ajanınkiyle aynı (hisse, sinyal ve çıkış günü). Dayanak C0 n=605 net 111,0 bp t=3,13 (IS 103,8 t=2,01, OOS 117,1 t=2,40); O1 101,2 t=2,93; C1 75,9 t=2,14. Gerçek ETF C0 n=261 127,6 bp t=2,65, O1 107,8 t=2,38, C1 85,5 t=1,66. Sentetik kalibrasyon bağımsız ölçümle aynı (gerçek ETF − sentetik, günde -1,1 ile -2,8 bp; MSTR -13). İleriye bakma yok: sinyal t kapanışına kadarki veriyle, SMA5 çıkışı j kapanışında görülüp uygulanıyor, bilanço takvimi önceden bilinir. En büyük 5 kazanç gerçek olay, veri hatası değil: 3'ü bilanço tepki günü (TSLA 24.10.2024 +%21,9; META 27.04.2023 +%13,9; NVDA 23.02.2023 +%14,0); diğer ikisi TSLA 31.01.2022 ve 09.09.2020. Muhafazakâr çıkış (ertesi açılışta satış) C0 139 bp t=3,39: kapanışta çıkış varsayımı iyimser değil. Sağlamlık: 7 hisse içinde zamanlama kenarı gerçek. Rastgele giriş permütasyonu (2.000): C0 tüm günler p=0,008, rejim eşlenik p=0,003; O1 p=0,0045 / 0,001. Ortak dairesel kaydırma (kümelenme korunur) p=0,001. Kenar 75-84 bp. Parametre platosu: 180 komşu varyantın (RSI 6-14, trend SMA 150-250, çıkış SMA 3-7, en uzun tutuş 2-5 gün) hepsi pozitif, 158'inde t≥2, medyan 109 bp t=2,77; ana kural t sırasında 50/180 (RSI<8'de çukur 78 bp t=1,85). Yıl çıkarma: 2020 hariç 94 bp t=2,69 (IS 61, t=1,26); 2022 hariç 118 t=3,33; 2020 ve 2022 hariç 102 t=2,91; 2020 ve 2024 hariç 52 t=1,42. En iyi 5 işlem çıkarılınca C0 93 t=2,74, O1 72,5 t=2,29; en iyi 10 çıkarılınca C0 70 t=2,16, O1 57,5 t=1,87. Maliyet (1.000$): C0 93,0 t=2,62, O1 83,2 t=2,41, C1 57,9 t=1,63; gerçek ETF 1.000$ C0 109,6 t=2,28, O1 89,8 t=1,98. Günlük portföy Newey-West t: C0 2,75 (IS 1,77, OOS 2,20), O1 2,29. Piyasa dibi (aynı gün QQQ RSI2<10) n=251 111,5 bp t=1,73; hisseye özgü dip n=354 110,7 bp t=2,61. QQQ'nun kendi kuralı O1'de 17 bp t=0,38: etki endeksten gelmiyor. Midas: sinyal günlerinin %33'ünde RSI(2) eşiğe yakın (7-10), C0 kararı son dakikada dönebilir; O1 temiz yedek. Ürün bulunurluğu doğrulanmadı. PTP beklenmez. En kötü işlem -%44,6. Hüküm: mekanik kabul eşiklerini geçiyor ve 7 hisse içinde sağlam; ama ex-ante evrende yok ve iki yıla bağlı. Seçilmiş kazananların sürmesine dayalı bir rejim bahsi: küçük pozisyonla.
- **Denetçinin uyarıları:** (1) maxDD olduğundan küçük: ajanın -%11,5'i sinyal-günü ortalamalarının ardışık çarpımı. Günlük değerlemeli portföyde (her hisseye 1/7) maxDD -%25,3 (10.03.2020 → 18.03.2020); 2020 dışında -%14,8. (2) 'Bilanço hariç' +84 bp t=2,44 gerçekleşen tutuşa göre süzülmüş: SMA5 çıkışı ileriki fiyata bağlı olduğundan hafif ileriye bakma var ve uygulanamaz. Uygulanabilir 'ATLA' (tepki günü t+1..t+3 içindeyse girme) C0 79,4 bp t=2,33 (IS t 1,63, OOS t 1,66), pozitif yıl %50: eşik altı. (3) Güncel durum eksik: META ve GOOGL de SMA200'ün altında, filtre 7 hissenin 4'ünde kapalı (ajan yalnız NVDA ve TSLA'yı yazmış). (4) EN ÖNEMLİSİ seçim yanlılığı: aynı kural ex-ante evrende çalışmıyor. B10 dışı 47 hisse (Kasım 2016'nın en büyük 30'u + tek hisse LETF'i olan diğer 15 + TSM/AVGO) C0 net 11,5 bp t=0,77, zamanlama kenarı 5,5 bp t=0,37. 2016'nın en büyük 30'u 8,9 bp t=0,64 (IS -10 bp). LETF'i olan diğer 15 hisse 18,9 bp t=0,60, kenar -14 bp. (5) Kenar iki yıla bağlı: 2020 ve 2024 hariç C0 52 bp t=1,42, OOS 44 bp t=0,79. (6) Birleşik FDR'yi geçmiyor (p=0,0019; ~7.800 test, BH eşiği ~4e-5).
- **Giriş zamanı sağlamlığı:** Dayanak havuzu (2016-11..2026-11, sentetik kalibre 2x): C0 net 111,0 bp t=3,13 (IS 103,8 t=2,01, OOS 117,1 t=2,40); O1 101,2 t=2,93 (IS 100,7, OOS 101,5); C1 75,9 t=2,14 (IS 65,4, OOS 85,4). Zamanlama kenarı (aynı tutuş süreli koşulsuz getiri düşülmüş): C0 74,0 bp t=2,06, O1 76,1 bp t=2,18, C1 46,7 bp t=1,30: kenar ilk günlerde, gecikmeli girişte (C1) yarıya iner. Gerçek ETF verisi (2022+, sinyal hisseden): C0 127,6 bp t=2,65 (n=261), O1 107,8 t=2,38, C1 85,5 t=1,66; yalnız 2x dönemi (2024+): C0 149,2 t=2,44, O1 122,1 t=2,10. Kapanışa bağımlı değil (O1'de de çalışıyor).
- **Maliyet duyarlılığı:** Dayanak havuzu C0: 1.000$ 93,0 bp (t=2,62), 2.500$ 111,0 bp (t=3,13), 10.000$ 120,0 bp (t=3,38). O1: 83,2 / 101,2 / 110,2 bp. Gidiş-dönüş maliyet 16-23 bp (TSLL 23 bp: 8,8$ fiyatta 1 sentlik adım ~11 bp makas). Ortalama brüt kenar (128 bp) maliyetin ~6-8 katı.
- **Not:** Kaldıraçlı ETF Midas'ta yoksa ya da riski fazla geliyorsa aynı sinyalle hissenin kendisi (denetçi: 1x hisse daha sağlam araç). Aynı anda en çok 2 hisse. Yıllık (sinyal tarihi başına ort. net, bp toplamı): {2017: 1201, 2018: 1027, 2019: 634, 2020: 10530, 2021: 6636, 2022: -1166, 2023: 1996, 2024: 19353, 2025: -2606, 2026: 8897}. Negatif yıllar 2022 ve 2025 (ayı/sert düşüş dönemlerinde dip alımı tekrar tekrar zarar). En kötü işlem -4.457 bp (TSLA 2x, ~-%45); hisse başına maxDD %18-%72 (TSLA); 1/7 sermaye kaba portföy maxDD -11,5%. Sinyaller piyasa geneli düşüşlerde kümelenir (eşzamanlı 7 pozisyona kadar): pozisyon başına sermayeyi buna göre böl. Kanıt sınırlılıkları: (1) dayanak evreni sonradan kazananlardan oluşuyor (hayatta kalma/seçim yanlılığı): net getirinin bir kısmı 2016-2026 mega-cap yükselişi; zamanlama kenarı ~74-76 bp ve t~2,1 (C0/O1), bilanço işlemleri hariç ~47 bp t~1,4. (2) Birleşik FDR'yi geçmiyor. (3) 2x ETF 1-3 günde 2x hisseden 9-14 bp geride (finansman/ücret; TH01). (4) Midas'ta bu ETF'lerin bulunurluğu resmî olarak doğrulanamadı. Son veri (06.11.2026): 7 hissenin hiçbirinde sinyal yok; NVDA, TSLA SMA200 altında (filtre kapalı). BİLANÇO (önemli): işlemlerin 24'ü (~%4) tutuşta bir bilanço tepki gününü taşıyor ve ortalama 569 bp (t=1,80, en kötü -2.491 bp) getiriyor. Bunlar çıkarılınca C0 n=581 net 83,7 bp t=2,44 (IS 88,2 t=1,68, OOS 79,8 t=1,77), O1 74,0 t=2,25, gerçek ETF C0 92,8 t=2,13; zamanlama kenarı ~47 bp t~1,35-1,49 (anlamsız). Yani sürüklenme dışı kenarın önemli kısmı az sayıda bilanço öncesi dip işleminden geliyor. Muhafazakâr kullanım: tutuş içinde bilanço (seans sonrası duyuru) varsa girme ya da duyuru günü kapanıştan önce çık (TH04).
- Betik: `python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_tek_hisse_kaldiracli/aday_S1.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| AMZN (dayanak hisse, aynı gün) | `NASDAQ:AMZN` | 1.00 | 1.97 |
| SPY günlük getiri (aynı gün) | `AMEX:SPY` | 0.56 | 2.71 |
| VIX günlük log değişimi (aynı gün, ters yön) | `CBOE:VIX` | -0.50 | -0.25 |
| QQQ günlük getiri (aynı gün) | `NASDAQ:QQQ` | 0.50 | 1.54 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| SPY günlük getirisi (t) -> AMZN t+1 getirisi, kendi getirisi kontrollü | `AMEX:SPY` | gecikmeli (lag), NEGATİF katsayı | 1 gün | 1 sd SPY hareketi -> 2x ETF'te ertesi gün -50 bp (ters yönde); maliyet 16 bp | -3.3 (-2.6/-2.0) | FDR yalnız 152 testlik ek lead-lag ailesinde; birleşik FDR yok; OOS zayıf. Kurala çevrilince (piyasa z<-2 -> 2x long) maliyet sonrası doğrulanmadı (bkz. elenen). | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| AMZN uzatılmış seans (pre-market 04:00-09:30 ET = TR kış 12:00-17:30; after-hours 16:00-20:00 ET = TR kış 00:00-04:00) | `NASDAQ:AMZN` | ETF açılış boşluğunun ana kaynağı (≈2x). Grafikte uzatılmış saatleri aç; bilanço tepkisi after-hours'ta görülür. |
| Nasdaq 100 E-mini vadelisi | `CME_MINI:NQ1!` | ~23 saat işler; ETF kapalıyken piyasa yönünü gösterir (izleme, öncü değil). |

## 3. Takvim ve olay riskleri

AMZN sonraki bilanço tarihi henüz açıklanmadı (Nasdaq boş); 2023-2026 düzenine göre yaklaşık 01.02-06.02.2027 arası, seans sonrası (tepki ertesi gün açılış boşluğunda). Son duyuru 2026-10-29. Ortak: CPI 10.11 ve 10.12 (TR 16:30); opex 20.11; 26.11 kapalı, 27.11 erken kapanış (TR 21:00); NFP 04.12 (TR 16:30); FOMC 09.12 (TR 22:00); triple witching 18.12; 24.12 erken kapanış, 25.12 kapalı.

## 4. Notlar

İşlem için doğrulanmış gecikmeli öncü yok (genel taramada aile FDR bayrağı 0). Ek dayanak testindeki ilişkiler NEGATİF işaretli piyasa-geri dönüşü; OOS zayıf, kural olarak maliyet sonrası doğrulanmadı. Sürücüler eşzamanlıdır, öncü değil.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_tek_hisse_kaldiracli.md`, `notlar/denetim_tek_hisse_kaldiracli.md`.*
