# EWY — iShares MSCI South Korea ETF

**TradingView:** `AMEX:EWY` · **Aile:** Uluslararası / ülke · **İzleme kararı:** kabul  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 2.361 | 13,0 | 377 | %-14,1 | 1,0x | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** En likit (medyan 2,36 mlr $/gün) ve en ucuz (13 bp) aile üyesi; maliyet/oynaklık 0,03 (ailenin en düşüğü). B4 sepetinin en güçlü üyesi (C0 h=1 net +108 bp, t 2,41, IS ve OOS > 0) ve B5'in (keşifsel) işlem aracı. Güçlü negatif 1 günlük otokorelasyon (IS -0,16 / OOS -0,12).

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt ya da yalnız filtre — tek başına işlem gerekçesi değil)

#### B4 — ABD sert düşüş günü Asya aşırı tepki dönüşü (UL03, sepet)  
*İzlemede — zayıf kanıt · güven: orta · aile kimliği: `uluslararasi_S1`*  
*Bu ETF'nin rolü: sepet üyesi*

- **Sinyal (t kapanışında):** Günlük veri (TradingView'da temettü düzeltmesi 'ADJ' açık). Sinyal günü t: AMEX:SPY günlük değişimi = close/close[1]-1 <= -%1,50. Bu günde sepetteki her ETF için (AMEX:EWJ, AMEX:EWY, AMEX:EWT, AMEX:FXI, AMEX:EWA, AMEX:EWH) kendi günlük değişimi SPY'ın günlük değişiminden küçük ya da eşitse (ETF SPY'dan daha çok düştüyse) o ETF'te long aç; diğerlerinde işlem yok. Eşit tutar (ör. ETF başına 2.500 $). Çıkış: bir sonraki işlem günü kapanışı (h=1). Çıkış günü yeniden sinyal varsa pozisyon korunur. Açığa satış yok; yalnız long. Pine: spy=request.security("AMEX:SPY","D",close/close[1]-1); sig = spy<=-0.015 and (close/close[1]-1)<=spy.
- **Giriş:** C0: t günü ABD kapanışına ~10-15 dk kala (kış saati TR 23:45-23:50; yaz saati TR 22:45-22:50) koşul o anki fiyatlarla sağlanıyorsa piyasa/limit emirle al. Kaçırılırsa kapanış sonrası after-hours (kış TR 00:00-04:00) yalnız limit emirle, kapanış fiyatına yakın limitle. Kapanışa kadar fiyat değiştiğinden C0 hafif iyimserdir.
- **Tutuş / çıkış:** 1 işlem günü (birincil, önceden belirlenmiş). Varyant h=2: sepet net +73 bp, t 2,33 (seçim yapılmadı, yalnız rapor). — t+1 kapanışına ~10 dk kala sat (kış TR ~23:50, yaz ~22:50). Stop kullanılmadı. Ertesi açılışta GİRME (O1 sepette −3 bp; FXI'de −33 bp).
- **İşlem aracı:** EWY, EWT, FXI, EWJ, EWA, EWH (sinyal: SPY (koşul) + işlem yapılan ETF'in kendi günlük getirisi)
- **Geçmiş (ajan):** n=110, net 55.8 bp/işlem (brüt 70.4), kazanma %58, t=2.22, IS 68.0 / OOS 45.7 bp, yılların %78'i pozitif, en kötü işlem -1356 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** C0: net 57 bp (t 3,2, gün kümeli t 1,9, n=288) · O1: net -3 bp (t -0,3, gün kümeli t -0,2, n=288) · C1: net 29 bp (t 2,0, gün kümeli t 1,3, n=274); 1.000 $ pozisyonda ana mod net 39 bp (t 2,2)
- **Denetçi düzeltmesi:** C0 h1 2.500$: net 55,8 bp, gün-kümeli BASİT t 1,99 (NW 2,22 şişkin), OOS t 1,42; tek yönlü p 0,024 -> 6 birincil hipotezde BH GEÇMEZ; en iyi 5 gün hariç 18,7 bp (t 0,79); 2020+2026 hariç 21,2 bp (t 1,00); 1.000$ 37,8 bp (t 1,35); +10 bp stres 45,8 bp (t 1,64). Kural metnine uygun 'koru' sürümü: 106 gün, net 57,5 bp, basit t 2,54, en kötü -852 bp; en iyi 5 gün hariç t 1,28, 2020+2026 hariç t 1,19.
- **Denetçi kural düzeltmesi:** Kural aynı kalabilir ama statüsü 'aday strateji' değil 'izleme/keşif sinyali' olmalı. Uygulanırsa: yalnız C0 (ABD kapanışından ~10 dk önce, kış TR 23:50) ve ETF başına >= 2.500$ (tercihen >= 5.000$); çıkış günü yeniden sinyal varsa pozisyonu KORU (yeniden giriş maliyeti ödeme; backtest de buna göre yapılmalı); 'kapanış kaçırılırsa O1 h=2' yedeği önerilmez (FXI O1 h1 net -33 bp, t -2,38); kaldıraçlı (KORU/YINN) uygulama önerilmez.
- **Denetim:** Bağımsız simülatörle (lib.trades/evaluate kullanılmadan) BİREBİR: 110 sinyal günü, 293 işlem, brüt 70,37 bp, net 55,84 bp (2.500$), NW t 2,22, IS 68,0 / OOS 45,7 bp, yıl+ 0,78, en kötü -1.356 bp (EWA 11.03.2020); ETF bazında EWY 108 (t 2,41), EWT 63 (2,00), FXI 37 (1,17), EWJ 30 (1,21), EWA 51 (0,97), EWH 49 (1,54) aynı. Zamanlama temiz: giriş c[t]/çıkış c[t+1] hatası 0, SPY-ETF takvim farkı yok, ham ve düzeltilmiş fiyatla sinyal farkı 0 gün; en büyük kazançlar (EWA 12.03.2020 +1.399, EWY 23.03.2020 +1.232, EWA 23.03.2020 +1.209, EWY 29.07.2026 +1.166, EWY 10.06.2026 +1.135 bp) veri_kalitesi'nde bayraksız gerçek kriz günleri; 2026 EWY hareketleri KORU ile tutarlı (beta 2,92, korelasyon 0,999). Sağlamlık: Lehte: koşullu permütasyon (aynı SPY<=-%1,5 günlerinde aynı sayıda ETF'i rastgele seçme, 5.000 tekrar) p=0,0014 (gözlenen 55,8 vs sim. ort. 35,4 bp); rastgele tarih p=0,0002; SPY düşüş günlerinden rastgele gün+ETF p=0,0036; eşleştirilmiş fark (ETF<=SPY eksi ETF>SPY) +39,7 bp t 2,84, IS 38,8/OOS 40,5, 2020 hariç t 2,39; plasebo Amerika/Avrupa zayıf; göreli koşul sertleştikçe (k=1,25) brüt artıyor -> göreli aşırı tepki mekanizması gerçek görünüyor. Aleyhte: uzun-tek yönlü mutlak getiri birkaç kriz gününe bağlı (rastgele ETF seçimiyle bile 35 bp), alt örneklerde ve maliyet/kayma duyarlılığında eşik altına düşüyor. Mod: C0 56 / O1 -2 / C1 25 bp net (h1); h=2 C0 73 bp (basit t 2,39) ama en iyi 5 gün hariç t 1,25. Yıllar: 2018 -6, 2019 +74, 2020 +122, 2021 +76, 2022 +18, 2023 +30, 2024 -46, 2025 +34, 2026 +200 bp.
- **Denetçinin uyarıları:** (1) Gün-kümeli seride basit t 1,99; NW(1) 2,22 değeri düzensiz aralıklı ardışık sinyal günleri arasındaki -0,19 otokorelasyondan şişiyor (h=1 C0 işlemleri zamanda çakışmaz, NW gerekçesiz) -> t>=2 eşiği sınırda SAĞLANMIYOR. (2) Basit t ile tek yönlü p=0,024 > 0,1/6=0,0167: ajanın '6 birincil hipotez içinde BH geçer' iddiası NW t'ye bağlı, basit t ile GEÇMEZ; Bonferroni(6) de geçmez. (3) Aşırı yoğunlaşma: en iyi 5 gün (110 günden) hariç net 18,7 bp t 0,79; en iyi 10 işlem hariç t 1,33; 2020+2026 hariç 21 bp t 1,00; 2026 hariç OOS 14,9 bp. (4) 1.000$'da net 37,8 bp t 1,35; stres makası +10 bp t 1,64. (5) Kapanışa bağımlı: kenarın 63/76 bp'si gece boşluğu; O1 h1 net -1,7; kenar kapanışı gün dibinde olan işlemlerde (12 Asya ETF IBS<0,1 net 77 bp, IBS>=0,6 -81 bp) toplanıyor -> C0 varsayımı en iyimser olduğu yerde; kapanıştan önce giriş vekili (c + f*aralık, aralık ort. 232 bp) f=0,03 t 1,75, f=0,05 t 1,59. (6) Komşu eşiklerde OOS işareti dönüyor (-1,75: OOS -14; -2,5: OOS -31); ajan yalnız -1,0/-2,0'ı raporlamış. (7) Kural metni ('çıkış günü sinyal varsa pozisyon korunur') ile backtest (çık-yeniden gir, ek maliyet) uyumsuz. (8) Kaldıraçlı sürümlerde KORU verisi 17.03.2020'de tutarsız (EWY +%7,2, KORU -%13,2).
- **Giriş zamanı sağlamlığı:** h=1: C0 brüt 70 bp / O1 13 bp / C1 40 bp. h=2: C0 87 / O1 53 (net 38, t 1.76) / C1 31. O1 ve C1'de brüt kenar pozitif ama kenarın büyük kısmı t kapanışı -> t+1 açılışı gece boşluğunda: AĞIRLIKLA KAPANIŞA BAĞIMLI.
- **Maliyet duyarlılığı:** Sepet C0 h=1 net: 1.000$ 37.8 bp (t 1.51); 2.500$ 55.8 bp (t 2.22); 10.000$ 64.8 bp (t 2.58). Brüt 70.4 bp; ETF başı maliyet 13-16 bp (2.500$).
- **Not:** Sinyal seyrek: 10 yılda 110 gün (yılda ~11), sinyal başına ortalama 2,7 ETF; 6 ETF için ~15.000 $ sermaye gerekebilir. Getiri yüksek oynaklık dönemlerinde yoğun: 2020 hariç net 41 bp (t 1,78), 2020 ve 2026 birlikte hariç net 21 bp (t 1,03). Yıllar: 2018 -6, 2019 +74, 2020 +122, 2021 +76, 2022 +18, 2023 +30, 2024 -46, 2025 +34, 2026 +200 bp (sinyal günü ortalaması). En kötü tek işlem EWA 11 Mar 2020 -1.356 bp; en kötü sepet günü -1.202 bp. EWY hariç sepet net 51 bp (t 2,10). Kaldıraçlı uygulama (dayanak sinyaliyle, Midas'ta bulunurluk doğrulanmadı): KORU<-EWY C0 h=1 net +257 bp (t 1,95), h=2 +337 bp (t 2,12), en kötü -3.776 bp; YINN<-FXI C0 h=1 t 1,25, h=2 +336 bp (t 2,27). Kaldıraçlı sürümler t>=2 eşiğini birincil spesifikasyonda geçmiyor; 3x ürünlerde tek gün -%30..-40 mümkün. TradingView'da düzeltilmemiş grafikte EWT/EWY Aralık temettü ex-günleri sahte 'düşüş' gibi görünebilir: ADJ açık kullanın ya da ex-div gününü atlayın.
- Betik: `/home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_uluslararasi/strateji_S1_ul03_asya.py`

#### B5 — EWY gün sonu dip dönüşü (IBS<0,10 ve düşüş günü) — KEŞİFSEL  
*İzlemede — zayıf kanıt · güven: dusuk · aile kimliği: `uluslararasi_S2`*  
*Bu ETF'nin rolü: ana araç*

- **Sinyal (t kapanışında):** AMEX:EWY günlük mum: IBS = (close-low)/(high-low) < 0,10 VE close < close[1] ise EWY long (t kapanışı); t+1 kapanışında çık. Pine: ibs=(close-low)/(high-low); sig = ibs<0.10 and close<close[1]. İsteğe bağlı kaldıraçlı uygulama: sinyal EWY'den, işlem AMEX:KORU.
- **Giriş:** C0: EWY kapanışına ~5-10 dk kala (kış TR 23:50, yaz 22:50) gün içi düşük seviyeye çok yakın ve önceki kapanışın altında ise al. IBS kapanış fiyatına bağlı -> C0 iyimser; after-hours limit emriyle de denenebilir.
- **Tutuş / çıkış:** 1 işlem günü — t+1 kapanışına ~10 dk kala sat.
- **İşlem aracı:** EWY (sinyal: EWY)
- **Geçmiş (ajan):** n=214, net 42.1 bp/işlem (brüt 55.1), kazanma %56, t=2.93, IS 25.8 / OOS 52.9 bp, yılların %70'i pozitif, en kötü işlem -468 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** C0: net 42 bp (t 3,1, n=225) · O1: net 6 bp (t 0,7, n=225) · C1: net -9 bp (t -0,6, n=212); 1.000 $ pozisyonda ana mod net 24 bp (t 1,8)
- **Denetçi düzeltmesi:** Ajanınkiyle aynı; ek: 2026 hariç net 21,4 bp t 1,70; 2020+2026 hariç 12,4 bp t 0,95; en iyi 10 hariç 13,1 bp t 1,15; +10 bp kayma t 2,23; f=0,10 kapanış öncesi vekili t 1,69.
- **Denetçi kural düzeltmesi:** Strateji olarak önerilmez; keşifsel izleme. İleride yalnız 2027+ verisinde, kural değişmeden test edilmeli.
- **Denetim:** BİREBİR: n=214, brüt 55,12, net 42,12 bp, t 2,93, IS 25,8 (t 1,29) / OOS 52,9 (t 2,33), yıl+ 0,70, en kötü -468 bp; O1 net 4,9, C1 brüt 0,75 bp. IBS kendi hesabımla; ham EWY h/l verisinde eksik/0 yok. Sağlamlık: Lehte: IBS eşiği 0,05-0,20 aralığında plato (t 2,4-3,7); yıl-tabakalı permütasyon p=0,0014 (yalnız seçim sonrası tek test için geçerli); EWY'nin negatif 1 günlük otokorelasyonu (IS -0,16 / OOS -0,12) eşzamansızlık mekanizmasını (B4 ile aynı) destekliyor. Aleyhte: çoklu test, IS anlamsız, aile tekrarı yok, 2026 bağımlılığı.
- **Denetçinin uyarıları:** 20.196 satırlık taramadan seçildi (Bonferroni p<2,5e-6 gerekir); IS t 1,29 (anlamsız); 2026 (21 işlem, ort. +232 bp) hariç net 21 bp t 1,70; 2020+2026 hariç 12 bp t 0,95; en iyi 10 işlem hariç t 1,15; aynı kural kardeş Asya ETF'lerinde negatif (EWT -7,7, EWJ -4,3, EWA -4,8, INDA -6,8 bp); C1 brüt ~0 -> tamamen kapanışa bağımlı; 1.000$ t 1,68; kapanış öncesi giriş vekili f=0,10 t 1,69; B4 ile çakışmayan işlemler net 19 bp (t 1,42). 2026'da EWY günlük oynaklığı 403 bp (2017-2025: 100-256) -> sonuç tek bir rejime bağlı.
- **Giriş zamanı sağlamlığı:** C0 brüt 55 bp / O1 18 bp (net 5) / C1 1 bp. Kenar neredeyse tamamen gece boşluğunda: KAPANIŞA BAĞIMLI.
- **Maliyet duyarlılığı:** Net: 1.000$ 24.1 bp; 2.500$ 42.1 bp; 10.000$ 51.1 bp (brüt 55.1, maliyet 13 bp).
- **Not:** Kabul eşiğini biçimsel olarak geçiyor (t 2.93, IS 26 / OOS 53 bp, yılların %70'i pozitif, n=214, O1 brüt > 0) ama tarama içinden seçildi ve FDR'yi geçmiyor. Getirinin yarıdan fazlası 2026'dan (21 işlem, ort. +232 bp) ve 2020'den; 2020 ve 2026 hariç net ~+12 bp. KORU (EWY sinyaliyle) C0 h=1 net 99 bp (t 2.39), en kötü -1397 bp. B4 ile EWY'de çakışabilir (aynı gün iki sinyal = tek pozisyon).
- Betik: `/home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_uluslararasi/strateji_S2_ewy_ibs.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| EEM | `AMEX:EEM` | 0.93 | 2.13 |
| SMH | `NASDAQ:SMH` | 0.83 | 1.17 |
| XLK | `AMEX:XLK` | 0.79 | 1.67 |
| QQQ | `NASDAQ:QQQ` | 0.78 | 2.19 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| SPY koşullu kuralı (B4: SPY<=-%1,5 ve ETF<=SPY) | `AMEX:SPY` | koşullu eşik; doğrusal testte doğrulanmadı | t+1 | Koşul sağlandığında EWY ertesi gün brüt 121 bp (n=68); sepet net +56 bp | 2.4 (—/—) | net 108 bp (IS 77 / OOS 135) | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| KOSPI (seans TR 03:00-09:30) | `KRX:KOSPI` | EWY açılış boşluğunu belirleyen yerel seans |
| Nasdaq 100 vadelisi | `CME_MINI:NQ1!` | gece yön; yarı iletken ağırlığı |
| S&P 500 vadelisi | `CME_MINI:ES1!` | gece risk iştahı |

## 3. Takvim ve olay riskleri

ABD: CPI 10 Kas, NFP 4 Ara, CPI 10 Ara, FOMC 9 Ara 2026 (Asya'ya ertesi sabah yansır); NYSE 26 Kas kapalı, 27 Kas/24 Ara erken kapanış (TR 21:00). Yerel tatillerde ETF NAV'sız işlem görür. Kore: Seollal (Şub 2027 başı), çeyreklik vade 10 Ara 2026; KORU'da 3x günlük yeniden dengeleme.

## 4. Notlar

Doğrulanmış (doğrusal) gecikmeli öncü YOK: aile içi BH-FDR geçen çift yok. En güçlü aday (FDR'siz): TIP h1 t=2.31 (IS 1.88/OOS 1.36), h3 t=2.82. Sürücüler eşzamanlıdır, öncü değildir. SPY satırı B4'ün koşullu kuralıdır, doğrusal öncü değildir. Reel faiz düşüşü (FRED:DFII10) 3 gün ufkunda pozitif aday (IS/OOS aynı işaret, FDR yok).

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_uluslararasi.md`, `notlar/denetim_uluslararasi.md`.*
