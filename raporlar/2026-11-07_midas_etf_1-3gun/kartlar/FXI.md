# FXI — iShares China Large-Cap ETF

**TradingView:** `AMEX:FXI` · **Aile:** Uluslararası / ülke · **İzleme kararı:** kabul  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 872 | 14.9 | 121 | %-3.0 | 1.0 | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** Çin büyük şirketleri için en likit araç (872 mn $, 15 bp). S1 sepet üyesi (C0 h=1 net +37 bp, t 1,17; h=2 +108 bp, t 2,19). MCHI aynı hisseleri taşır (kopya; daha az likit).

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt — tek başına işlem gerekçesi değil)

#### ABD sert düşüş günü Asya aşırı tepki dönüşü (UL03, sepet)  
*İzlemede — zayıf kanıt · güven: orta · id: `uluslararasi_S1`*

- **Sinyal (t kapanışında):** Günlük veri (TradingView'da temettü düzeltmesi 'ADJ' açık). Sinyal günü t: AMEX:SPY günlük değişimi = close/close[1]-1 <= -%1,50. Bu günde sepetteki her ETF için (AMEX:EWJ, AMEX:EWY, AMEX:EWT, AMEX:FXI, AMEX:EWA, AMEX:EWH) kendi günlük değişimi SPY'ın günlük değişiminden küçük ya da eşitse (ETF SPY'dan daha çok düştüyse) o ETF'te long aç; diğerlerinde işlem yok. Eşit tutar (ör. ETF başına 2.500 $). Çıkış: bir sonraki işlem günü kapanışı (h=1). Çıkış günü yeniden sinyal varsa pozisyon korunur. Açığa satış yok; yalnız long. Pine: spy=request.security("AMEX:SPY","D",close/close[1]-1); sig = spy<=-0.015 and (close/close[1]-1)<=spy.
- **Giriş:** C0: t günü ABD kapanışına ~10-15 dk kala (kış saati TR 23:45-23:50; yaz saati TR 22:45-22:50) koşul o anki fiyatlarla sağlanıyorsa piyasa/limit emirle al. Kaçırılırsa kapanış sonrası after-hours (kış TR 00:00-04:00) yalnız limit emirle, kapanış fiyatına yakın limitle. Kapanışa kadar fiyat değiştiğinden C0 hafif iyimserdir.
- **Tutuş / çıkış:** 1 işlem günü (birincil, önceden belirlenmiş). Varyant h=2: sepet net +73 bp, t 2,33 (seçim yapılmadı, yalnız rapor). — t+1 kapanışına ~10 dk kala sat (kış TR ~23:50, yaz ~22:50). Stop kullanılmadı (testte yok). Yedek giriş: t+1 açılışında (TR 17:30 kış) alındıysa h=2 tut (O1 h=2: net +38 bp, t 1,76).
- **İşlem aracı:** EWY, EWT, FXI, EWJ, EWA, EWH (sinyal: SPY (koşul) + işlem yapılan ETF'in kendi günlük getirisi)
- **Geçmiş (ajan):** n=110, net 55.8 bp/işlem (brüt 70.4), kazanma %58, t=2.22, IS 68.0 / OOS 45.7 bp, yılların %78'i pozitif, en kötü işlem -1356 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500$):** C0: net 57 bp (t 3.2, n=288) · O1: net -3 bp (t -0.3, n=288) · C1: net 29 bp (t 2.0, n=274); 1.000$ pozisyonda ana mod net 39 bp (t 2.2)
- **Denetçi düzeltmesi:** C0 h1 2.500$: net 55,8 bp, gün-kümeli BASİT t 1,99 (NW 2,22 şişkin), OOS t 1,42; tek yönlü p 0,024 -> 6 birincil hipotezde BH GEÇMEZ; en iyi 5 gün hariç 18,7 bp (t 0,79); 2020+2026 hariç 21,2 bp (t 1,00); 1.000$ 37,8 bp (t 1,35); +10 bp stres 45,8 bp (t 1,64). Kural metnine uygun 'koru' sürümü: 106 gün, net 57,5 bp, basit t 2,54, en kötü -852 bp; en iyi 5 gün hariç t 1,28, 2020+2026 hariç t 1,19.
- **Denetçi kural düzeltmesi:** Kural aynı kalabilir ama statüsü 'aday strateji' değil 'izleme/keşif sinyali' olmalı. Uygulanırsa: yalnız C0 (ABD kapanışından ~10 dk önce, kış TR 23:50) ve ETF başına >= 2.500$ (tercihen >= 5.000$); çıkış günü yeniden sinyal varsa pozisyonu KORU (yeniden giriş maliyeti ödeme; backtest de buna göre yapılmalı); 'kapanış kaçırılırsa O1 h=2' yedeği önerilmez (FXI O1 h1 net -33 bp, t -2,38); kaldıraçlı (KORU/YINN) uygulama önerilmez.
- **Denetim:** Bağımsız simülatörle (lib.trades/evaluate kullanılmadan) BİREBİR: 110 sinyal günü, 293 işlem, brüt 70,37 bp, net 55,84 bp (2.500$), NW t 2,22, IS 68,0 / OOS 45,7 bp, yıl+ 0,78, en kötü -1.356 bp (EWA 11.03.2020); ETF bazında EWY 108 (t 2,41), EWT 63 (2,00), FXI 37 (1,17), EWJ 30 (1,21), EWA 51 (0,97), EWH 49 (1,54) aynı. Zamanlama temiz: giriş c[t]/çıkış c[t+1] hatası 0, SPY-ETF takvim farkı yok, ham ve düzeltilmiş fiyatla sinyal farkı 0 gün; en büyük kazançlar (EWA 12.03.2020 +1.399, EWY 23.03.2020 +1.232, EWA 23.03.2020 +1.209, EWY 29.07.2026 +1.166, EWY 10.06.2026 +1.135 bp) veri_kalitesi'nde bayraksız gerçek kriz günleri; 2026 EWY hareketleri KORU ile tutarlı (beta 2,92, korelasyon 0,999). Sağlamlık: Lehte: koşullu permütasyon (aynı SPY<=-%1,5 günlerinde aynı sayıda ETF'i rastgele seçme, 5.000 tekrar) p=0,0014 (gözlenen 55,8 vs sim. ort. 35,4 bp); rastgele tarih p=0,0002; SPY düşüş günlerinden rastgele gün+ETF p=0,0036; eşleştirilmiş fark (ETF<=SPY eksi ETF>SPY) +39,7 bp t 2,84, IS 38,8/OOS 40,5, 2020 hariç t 2,39; plasebo Amerika/Avrupa zayıf; göreli koşul sertleştikçe (k=1,25) brüt artıyor -> göreli aşırı tepki mekanizması gerçek görünüyor. Aleyhte: uzun-tek yönlü mutlak getiri birkaç kriz gününe bağlı (rastgele ETF seçimiyle bile 35 bp), alt örneklerde ve maliyet/kayma duyarlılığında eşik altına düşüyor. Mod: C0 56 / O1 -2 / C1 25 bp net (h1); h=2 C0 73 bp (basit t 2,39) ama en iyi 5 gün hariç t 1,25. Yıllar: 2018 -6, 2019 +74, 2020 +122, 2021 +76, 2022 +18, 2023 +30, 2024 -46, 2025 +34, 2026 +200 bp.
- **Denetçinin uyarıları:** (1) Gün-kümeli seride basit t 1,99; NW(1) 2,22 değeri düzensiz aralıklı ardışık sinyal günleri arasındaki -0,19 otokorelasyondan şişiyor (h=1 C0 işlemleri zamanda çakışmaz, NW gerekçesiz) -> t>=2 eşiği sınırda SAĞLANMIYOR. (2) Basit t ile tek yönlü p=0,024 > 0,1/6=0,0167: ajanın '6 birincil hipotez içinde BH geçer' iddiası NW t'ye bağlı, basit t ile GEÇMEZ; Bonferroni(6) de geçmez. (3) Aşırı yoğunlaşma: en iyi 5 gün (110 günden) hariç net 18,7 bp t 0,79; en iyi 10 işlem hariç t 1,33; 2020+2026 hariç 21 bp t 1,00; 2026 hariç OOS 14,9 bp. (4) 1.000$'da net 37,8 bp t 1,35; stres makası +10 bp t 1,64. (5) Kapanışa bağımlı: kenarın 63/76 bp'si gece boşluğu; O1 h1 net -1,7; kenar kapanışı gün dibinde olan işlemlerde (12 Asya ETF IBS<0,1 net 77 bp, IBS>=0,6 -81 bp) toplanıyor -> C0 varsayımı en iyimser olduğu yerde; kapanıştan önce giriş vekili (c + f*aralık, aralık ort. 232 bp) f=0,03 t 1,75, f=0,05 t 1,59. (6) Komşu eşiklerde OOS işareti dönüyor (-1,75: OOS -14; -2,5: OOS -31); ajan yalnız -1,0/-2,0'ı raporlamış. (7) Kural metni ('çıkış günü sinyal varsa pozisyon korunur') ile backtest (çık-yeniden gir, ek maliyet) uyumsuz. (8) Kaldıraçlı sürümlerde KORU verisi 17.03.2020'de tutarsız (EWY +%7,2, KORU -%13,2).
- **Giriş zamanı sağlamlığı:** h=1: C0 brüt 70 bp / O1 13 bp / C1 40 bp. h=2: C0 87 / O1 53 (net 38, t 1.76) / C1 31. O1 ve C1'de brüt kenar pozitif ama kenarın büyük kısmı t kapanışı -> t+1 açılışı gece boşluğunda: AĞIRLIKLA KAPANIŞA BAĞIMLI.
- **Maliyet duyarlılığı:** Sepet C0 h=1 net: 1.000$ 37.8 bp (t 1.51); 2.500$ 55.8 bp (t 2.22); 10.000$ 64.8 bp (t 2.58). Brüt 70.4 bp; ETF başı maliyet 13-16 bp (2.500$).
- **Not:** Sinyal seyrek: 10 yılda 110 gün (yılda ~11), sinyal başına ortalama 2,7 ETF; 6 ETF için ~15.000 $ sermaye gerekebilir. Getiri yüksek oynaklık dönemlerinde yoğun: 2020 hariç net 41 bp (t 1,78), 2020 ve 2026 birlikte hariç net 21 bp (t 1,03). Yıllar: 2018 -6, 2019 +74, 2020 +122, 2021 +76, 2022 +18, 2023 +30, 2024 -46, 2025 +34, 2026 +200 bp (sinyal günü ortalaması). En kötü tek işlem EWA 11 Mar 2020 -1.356 bp; en kötü sepet günü -1.202 bp. EWY hariç sepet net 51 bp (t 2,10). Kaldıraçlı uygulama (dayanak sinyaliyle, Midas'ta bulunurluk doğrulanmadı): KORU<-EWY C0 h=1 net +257 bp (t 1,95), h=2 +337 bp (t 2,12), en kötü -3.776 bp; YINN<-FXI C0 h=1 t 1,25, h=2 +336 bp (t 2,27). Kaldıraçlı sürümler t>=2 eşiğini birincil spesifikasyonda geçmiyor; 3x ürünlerde tek gün -%30..-40 mümkün. TradingView'da düzeltilmemiş grafikte EWT/EWY Aralık temettü ex-günleri sahte 'düşüş' gibi görünebilir: ADJ açık kullanın ya da ex-div gününü atlayın.
- Betik: `/home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_uluslararasi/strateji_S1_ul03_asya.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| KWEB | `AMEX:KWEB` | 0.88 | 0.63 |
| EEM | `AMEX:EEM` | 0.45 | 0.33 |
| CPER | `AMEX:CPER` | 0.41 | 0.28 |
| SLV | `AMEX:SLV` | 0.41 | 0.12 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| SPY koşullu kuralı (S1: SPY<=-%1,5 ve ETF<=SPY) | `AMEX:SPY` | koşullu eşik; doğrusal testte doğrulanmadı | t+1 | Koşul sağlandığında FXI ertesi gün brüt 52 bp (n=50); sepet net +56 bp | 1.2 (—/—) | net 37 bp (IS 41 / OOS 34) | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Hang Seng vadelisi | `HKEX:HSI1!` | gece seansı ~TR 12:15-22:00 |
| Hang Seng endeksi | `TVC:HSI` | yerel kapanış TR 11:00 |
| USD/CNH | `FX:USDCNH` | 24 saat kur |
| FTSE China A50 vadelisi | `SGX:CN1!` | uzun seans Çin duyarlılığı |

## 3. Takvim ve olay riskleri

ABD: CPI 10 Kas, NFP 4 Ara, CPI 10 Ara, FOMC 9 Ara 2026 (Asya'ya ertesi sabah yansır); NYSE 26 Kas kapalı, 27 Kas/24 Ara erken kapanış (TR 21:00). Yerel tatillerde ETF NAV'sız işlem görür. Çin/HK: Ay Yeni Yılı (Şub 2027 başı, teyit edilmeli), teşvik/kur haberleri; YINN 3x.

## 4. Notlar

Doğrulanmış (doğrusal) gecikmeli öncü YOK: aile içi BH-FDR geçen çift yok. En güçlü aday (FDR'siz): EEM h1 t=-2.56 (IS -2.73/OOS -0.94), h3 t=-0.96. Sürücüler eşzamanlıdır, öncü değildir. SPY satırı S1'in koşullu kuralıdır, doğrusal öncü değildir.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_uluslararasi.md`, `notlar/denetim_uluslararasi.md`.*
