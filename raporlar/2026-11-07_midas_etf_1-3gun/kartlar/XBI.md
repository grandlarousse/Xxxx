# XBI — State Street SPDR S&P Biotech ETF

**TradingView:** `AMEX:XBI` · **Aile:** Sektör ve tematik · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 1,237 | 13.0 | 190 | %-6.7 | 1.0 | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** IBS<0.20 sınırda (net 16 bp, t 1.8, IS ~2 bp): kabul eşiğini geçmiyor. Likit (1.2 mlr $), ayrı küme (biyoteknoloji); sürücü IWM/VIX.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| IWM | `AMEX:IWM` | 0.63 | 1.02 |
| SPY | `AMEX:SPY` | 0.52 | 1.14 |
| VIX_dlog | `CBOE:VIX` | -0.51 | -0.12 |
| QQQ | `NASDAQ:QQQ` | 0.47 | 0.66 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| SPY/QQQ (zayıf, doğrulanmadı) | `AMEX:SPY` | negatif gecikme | 1 gün | SPY +1 sd -> XBI ertesi gün -25 bp; IS t -3.27, OOS t -1.16: OOS zayıf | -3.2 (-3.3/-1.2) | test edilmedi (OOS zayıf) | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Russell 2000 vadelisi | `CME_MINI:RTY1!` | Küçük ölçekli/bölgesel banka/biyotek açılış boşluğu. |
| VIX | `CBOE:VIX` | Risk iştahı; gün içi (16:15 ET kapanış). |

## 3. Takvim ve olay riskleri

FOMC/CPI (faize duyarlı küçük ölçek), FDA kararları (tek hisse), JPM Sağlık Konferansı (Ocak).

## 4. Notlar

Doğrulanmış gecikmeli öncü yok. (SPY/QQQ ilişkisi OOS'ta zayıflıyor).

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_sektor_tematik.md`, `notlar/denetim_sektor_tematik.md`.*
