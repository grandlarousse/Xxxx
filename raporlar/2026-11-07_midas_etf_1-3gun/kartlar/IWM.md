# IWM — iShares Russell 2000 Index Fund

**TradingView:** `AMEX:IWM` · **Aile:** ABD endeks ve faktör · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 7.828 | 13,0 | 117 | %-4,6 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Russell 2000: likit (7,8 mlr$), maliyet/oynaklık 0,11. B1 kuralı bu ETF'de C1 h=3 net 39 bp (t=1.9) — kendi sinyaliyle eşik altı (C0 t=0,8); SPY sinyaliyle IWM'de işlem C1 net 59 bp (t=2,40, sonradan bakıldı). Bağımsız küçük ölçek dayanağı. İzleme: CME_MINI:RTY1!. **Ana ajan notu:** Kendi sinyali gürültü; yalnız küçük şirket izlemesi (CME_MINI:RTY1!).

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| SPY | `AMEX:SPY` | 0.83 | 1.14 |
| DIA | `AMEX:DIA` | 0.78 | 1.09 |
| VIX (log değişim) | `CBOE:VIX` | -0.75 | -0.11 |
| QQQ | `NASDAQ:QQQ` | 0.74 | 0.65 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Russell 2000 E-mini vadeli | `CME_MINI:RTY1!` | CME Globex ~23 saat; IWM açılış boşluğunu önceden gösterir (IWM varyansının ~%40'ı gece). |
| S&P 500 E-mini vadeli | `CME_MINI:ES1!` | Genel piyasa yönü (IWM betası SPY'a 1,14). |
| ABD 2 yıllık getiri | `TVC:US02Y` | Küçük ölçek finansman/faiz duyarlılığı; veri günlerinde açılış öncesi. |

## 3. Takvim ve olay riskleri

SPY satırındaki takvimle aynı (CPI 10 Kas, OPEX 20 Kas, 26-27 Kas tatil/erken kapanış, NFP 4 Ara, FOMC 9 Ara, CPI 10 Ara, OPEX 18 Ara, 24-25 Ara).

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK (aile alt kümesi BH-FDR 0/2.636; yetişme, faiz kanalı ve IWM-SPY ayrıntısı SPY satırında). En güçlü (FDR'siz) gecikmeli satırlar: SPY (h1): t=-2.65, IS -2.3/OOS -1.5, -29 bp/sd; DIA (h1): t=-2.45, IS -2.1/OOS -1.5, -29 bp/sd.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_abd_endeks.md`, `notlar/denetim_abd_endeks.md`.*
