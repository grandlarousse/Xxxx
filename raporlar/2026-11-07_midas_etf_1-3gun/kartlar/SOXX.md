# SOXX — iShares PHLX SOX Semiconductor Sector Index Fund

**TradingView:** `NASDAQ:SOXX` · **Aile:** Sektör ve tematik · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 3.333 | 13,0 | 309 | %-12,1 | 1,0x | 2016-11-07 |

**Kademe:** A — denetimden geçmiş kural var  
**Neden izleme listesinde:** SMH'nin kopyası (korelasyon 0.98): A2 aynı sonucu veriyor (43 bp, t 3.9) ama bağımsız kanıt değil; SMH daha likit.

*Dayanak / ana araç kartı: `kartlar/SMH.md` (sürücüler ve gerçek zamanlı izleme listesi orada daha ayrıntılı).*

## 1. Ne zaman girilir?

#### A2 — Yarı iletken gün sonu zayıflığı dönüşü (SMH IBS<0.20, 1 gün)  
*Uygulanabilir (denetçi doğruladı) · güven: orta · aile kimliği: `sektor_tematik_S1`*  
*Bu ETF'nin rolü: kopya araç (aynı sinyal SMH'den)*

- **Sinyal (t kapanışında):** TradingView'da NASDAQ:SMH günlük grafiği. Gösterge IBS = (close - low) / (high - low), aynı günün mumu (Pine: ibs = (close-low)/(high-low); high=low ise sinyal yok). Koşul: IBS < 0.20 (kapanış gün içi aralığın alt %20'sinde). İşlem: NASDAQ:SMH long al, ertesi işlem günü kapanışında sat. Filtre yok (SMA200 filtresi sonucu iyileştirmiyor). Pozisyondayken ertesi gün yine IBS<0.20 olursa satma, bir gün daha tut (backtest bunu sat+yeniden al sayar; tutmak 3 $ komisyon kazandırır).
- **Giriş:** ANA YOL: resmî ABD kapanışından sonra kesin IBS'yi gör (SMH günlük mum); IBS<0,20 ise after-hours'ta (tercihen TR 00:00-01:00 kış / 23:00-00:00 yaz) resmî kapanış fiyatı + 2-5 sent LİMİT emirle, tam adet al (denetçi bu yolun maliyetini ~6 bp ölçtü). İKİNCİ YOL: kapanıştan dakikalar önce (kış TR 23:45-23:58) anlık IBS ile piyasa/agresif limit emir (kapanış öncesi sınıflama hatası ~15-20 bp maliyet). Ertesi açılışta (O1) GİRME: kenar ~17 bp'ye, C1'de ~0'a düşer.
- **Tutuş / çıkış:** 1 işlem günü (h=1). h=2/h=3 de pozitif (net 52/66 bp, t 3.4/3.3) ama birincil kural h=1. — Ertesi işlem günü kapanışından hemen önce sat (kış TR 23:45-23:58 / yaz 22:45-22:58). Stop yok (backtest stopsuz).
- **İşlem aracı:** SMH (sinyal: SMH)
- **Geçmiş (ajan):** n=492, net 41.8 bp/işlem (brüt 54.8), kazanma %59, t=3.69, IS 43.3 / OOS 40.1 bp, yılların %91'i pozitif, en kötü işlem -1069 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** C0: net 44 bp (t 3,7, n=483) · O1: net 19 bp (t 2,1, n=483) · C1: net 1 bp (t 0,1, n=409); 1.000 $ pozisyonda ana mod net 26 bp (t 2,2)
- **Denetçi düzeltmesi:** Uygulama cezalı (2.500$): AH girişi (+6 bp, ölçülen 17:00 ET primi) net 35.8 bp, t 3.16, IS 37.3 (t 2.69) / OOS 34.1 (t 1.87), yılların %82'si +, PF 1.49; AH + makas varsayımı (+11 bp) 30.8 bp, t 2.72, OOS t 1.60; kapanış öncesi giriş (+19 bp) 22.8 bp, t 2.01, OOS 21.1 (t 1.16), yılların %73'ü +. 1.000$: AH 17.8 bp (t 1.57) / kapanış öncesi 4.8 bp (t 0.42) -> eşik altında. 10.000$: AH 44.8 bp. Tut kuralı + AH: 46.7 bp/pozisyon (t 3.77). FDR: iki yönlü BH geçer, tek yönlü BH (92k ve 22k tarama) geçmez.
- **Denetçi kural düzeltmesi:** NASDAQ:SMH günlük IBS=(close-low)/(high-low) RESMİ KAPANIŞTAN SONRA hesaplanır; IBS<0.20 ise after-hours'ta (kış TR 00:00-01:00, yaz 23:00-00:00) resmi kapanış fiyatı + 2-5 sent limit emirle al (Midas'ta uzatılmış saatte yalnız limit). Ertesi gün kapanışa yakın sat (ya da yine after-hours limitle); ertesi gün de IBS<0.20 ise satma, bir gün daha tut. Pozisyon en az 2.500$ (1.000$'da kenar komisyon+giriş cezasıyla ~0). İsteğe bağlı (yalnız IS'te seçildi): 20g yıllık oynaklık < ~%24 iken sinyali atla (2.500$ AH: 46.3 bp, t 3.17, OOS 40.2 t 2.00). abd_endeks QQQ IBS pozisyonu açıksa ek risk sayılır (aynı bahis).
- **Denetim:** Bağımsız simülatörle (lib.trades/evaluate kullanılmadan) birebir: n=492, brüt 54.8, net 41.8 bp @2.500$, t 3.69, IS 43.3 (t 3.13) / OOS 40.1 (t 2.20), 11 yılın 10'u +, maxDD -%21.4, en kötü -1069 bp. 492 işlemin 492'si ajanın listesiyle aynı (brüt farkı 1e-16). IBS ham ve düzeltilmiş fiyattan aynı. Tut kuralı (ardışık sinyalde satma): 406 pozisyon, 52.7 bp, t 4.25. Sağlamlık: Permütasyon (10.000, aynı sayıda rastgele gün, h=1): p=0.0001 düz; yıl tabakalı 0.0001; oynaklık beşliği tabakalı 0.0001; 1g getiri ondalığı tabakalı 0.0006 (kenarın ~16 bp'si düz 1g dönüş). NW regresyonu z1+düşüş günü kontrollü IBS<0.2 katsayısı +39 bp (t 2.89). En iyi 5 hariç 31.5 bp (t 3.05), en iyi 10 hariç 25.3 (t 2.51). En iyi 5 işlem gerçek olaylar (2025-04-09, 2022-11-10, 2020-03-13, 2020-03-17, 2024-07-31), SOXX'te bağımsız olarak doğrulanıyor; bozuk kapanış izi yok (SMH-SOXX kalıntısı t +3.4 / t+1 -3.8 bp). Eşik plato: C0 0.10-0.30 net 29-55 bp, t 3.2-4.1 (O1'de plato zayıf). 2020 hariç 32.3 (t 2.78), 2022 hariç 47.8 (t 4.05), 2020+2022 hariç 37.7 (t 3.12). Ailede aynı kural: yalnız SMH/SOXX Bonferroni(39) geçer; XLK 19 (OOS 5), QQQ 17.6, XBI 15.9; diğerleri <=7 bp. C1 h1 kenar ~0; O1 brüt kenar +27 bp (>0).
- **Denetçinin uyarıları:** (1) Kapanışa bağımlı: IBS t kapanışını kullanır; ajanın önerdiği kapanış öncesi giriş (TR 23:45-23:58) pahalı. Gün içi veri (Yahoo 60 dk, 2023-12..2026-11): sinyal günlerinde 15:30->kapanış -33 bp; 15:30 IBS+15:30 giriş backtest'e göre brüt -18.6 bp (net 44.2 vs 62.8, t 1.61 vs 2.23); 5 dk örnekte (n=10) 15:45-15:55 fiyatı resmi kapanışın 16-22 bp üstünde. Ajan bunu 'hafif iyimser' diye niteledi: aslında kenarın ~%40-45'i. (2) FDR iddiası abartılı: iki yönlü BH'yi maliyetin anlamlı kıldığı negatif satırlar gevşetiyor (aile 995 geçen, %96 negatif); tek yönlü (pozitif) BH'de genel_tum 92k ve aile 22k satırında HİÇBİR test geçmiyor (A2 p1=2.1e-4, ilk sıra eşiği 4.5e-6); Bonferroni geçmez; yalnız ajanın seçim sonrası 1302'lik kümesinde geçer. (3) Kenar oynaklıkla ölçekleniyor: 20g oynaklık Q1 6 bp (t 0.39) ... Q5 85 bp; 2020+2026 hariç 24.8 bp (t 2.07); 2017-2019 25.3 (t 1.71). (4) 1.000$'da gerçekçi girişle eşik altında (AH: 17.8 bp t 1.57, OOS t 0.88, yılların %55'i +; kapanış öncesi: 4.8 bp). (5) O1 h1 net 15.5 (t 1.83), OOS t 0.96; O1 1.000$ -2.5 bp. (6) Bağımsız değil: sinyallerin %70'i QQQ IBS<0.2 ile aynı gün; abd_endeks QQQ IBS stratejisiyle aynı bahis.
- **Giriş zamanı sağlamlığı:** C0 h1 net 41.8; O1 h1 brüt 28.5 (koşulsuza göre kenar 27.1, net 15.5, t 1.83); C1 h1 brüt 15.3 (kenar 1.9 ≈ 0). O1'de brüt kenar > 0 olduğu için yalnız kapanışa bağımlı değil, ama etki ilk gün içinde sönüyor: en iyi kapanışta (C0) girilir; bir gün geç (C1) girmek kenarı yok eder.
- **Maliyet duyarlılığı:** 1.000$: 23.8 bp | 2.500$: 41.8 bp | 10.000$: 50.8 bp (net, işlem başına)
- **Not:** Kabul eşiklerini geçiyor (n=492 ≥40, t 3.69, IS 43 / OOS 40 bp, 11 yılın 10'u pozitif, O1 brüt kenar > 0). Güven 'orta' çünkü: tek bağımsız küme, aday çok sayıda test içinden seçildi (FDR'yi yine de geçiyor), C0 girişte IBS kapanıştan ~15 dk önce tahmin ediliyor (eşiğe yakın günlerde yanlış sınıflama). Komşu eşikler 0.10/0.15/0.25/0.30: net 55/39/40/29 bp, hepsi t>3 (seçim yapılmadı). En kötü işlemler: 2020-03-11 (-10.7%), 2025-01-24 (DeepSeek, -10.0%), 2025-04-03 (gümrük tarifesi, -7.7%): sinyal sert düşüş günlerinde de tetiklenir, pozisyon küçük tutulmalı. Yılda ~49 işlem (zamanın ~%20'si piyasada). Takvim riskleri: NVDA bilançosu (kapanış sonrası), FOMC/CPI günleri.
- Betik: `python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_sektor_tematik/strateji_adaylari.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| XLK | `AMEX:XLK` | 0.91 | 1.59 |
| QQQ | `NASDAQ:QQQ` | 0.89 | 2.06 |
| EEM | `AMEX:EEM` | 0.84 | 1.57 |
| TSM | `NYSE:TSM` | 0.83 | 0.98 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Nasdaq-100 vadelisi (neredeyse 24 saat) | `CME_MINI:NQ1!` | ETF kapalıyken (TR 00:00-17:30) teknoloji yönünü gösterir; açılış boşluğunu önceden verir. |
| KOSPI endeksi (Kore) | `KRX:KOSPI` | Asya seansında (TR ~03:00-09:30) bellek/yarı iletken (Samsung, SK Hynix) hareketi; SMH açılışını önceden gösterir. |
| NVIDIA (uzatılmış seans) | `NASDAQ:NVDA` | Bilanço kapanış sonrası açıklanır; after-hours/pre-market fiyatı SMH açılış boşluğunu gösterir (SMH ile 1y korelasyon 0.73). |
| PHLX Yarı İletken Endeksi | `NASDAQ:SOX` | Yalnız ABD seansında hesaplanır: gerçek zamanlı gün içi sürücü, kapalı saatte öncü değil. |

## 3. Takvim ve olay riskleri

SMH ile aynı.

## 4. Notlar

Doğrulanmış gecikmeli öncü yok. SMH ile aynı (kopya).

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_sektor_tematik.md`, `notlar/denetim_sektor_tematik.md`.*
