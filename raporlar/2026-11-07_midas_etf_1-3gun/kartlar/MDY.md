# MDY — State Street SPDR S&P MIDCAP 400 ETF Trust

**TradingView:** `AMEX:MDY` · **Aile:** ABD endeks ve faktör · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 476 | 14.0 | 97 | %-3.9 | 1.0 | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** S&P 400 orta ölçek: S1 kuralı bu ETF'de C1 h=3 net 47 bp (t=2.5); makas 2 bp, 476 mn$/gün. IWM ile 0,92 korelasyon.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| IWM | `AMEX:IWM` | 0.92 | 0.76 |
| SPY | `AMEX:SPY` | 0.81 | 0.92 |
| DIA | `AMEX:DIA` | 0.80 | 0.92 |
| VIX (log değişim) | `CBOE:VIX` | -0.72 | -0.08 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Russell 2000 E-mini | `CME_MINI:RTY1!` | MDY'nin likit vadelisi TradingView doğrulama listesinde yok; RTY1! (0,92 korelasyonlu IWM) ve ES1! izlenir. |
| S&P 500 E-mini | `CME_MINI:ES1!` | Genel piyasa. |

## 3. Takvim ve olay riskleri

SPY satırındaki takvimle aynı (CPI 10 Kas, OPEX 20 Kas, 26-27 Kas tatil/erken kapanış, NFP 4 Ara, FOMC 9 Ara, CPI 10 Ara, OPEX 18 Ara, 24-25 Ara).

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK (aile alt kümesi BH-FDR 0/2.636; yetişme, faiz kanalı ve IWM-SPY ayrıntısı SPY satırında). En güçlü (FDR'siz) gecikmeli satırlar: SPY (h1): t=-2.52, IS -2.1/OOS -1.6, -25 bp/sd; TIP (h3): t=2.51, IS 3.2/OOS 1.1, 29 bp/sd.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_abd_endeks.md`, `notlar/denetim_abd_endeks.md`.*
