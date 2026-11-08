# KRE — State Street SPDR S&P Regional Banking ETF

**TradingView:** `AMEX:KRE` · **Aile:** Sektör ve tematik · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 1.022 | 13,4 | 131 | %-5,1 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Strateji yok; net sürücüler (XLF, IWM, faiz). FOMC karar günü riski ölçüldü (faize duyarlı grup gün içi brüt -26 bp). Likit (1 mlr $), maliyet/oynaklık 0.10 (sınırda).

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| XLF | `AMEX:XLF` | 0.69 | 0.93 |
| IWM | `AMEX:IWM` | 0.60 | 0.66 |
| SPY | `AMEX:SPY` | 0.38 | 0.58 |
| VIX_dlog | `CBOE:VIX` | -0.38 | -0.06 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Russell 2000 vadelisi | `CME_MINI:RTY1!` | Küçük ölçekli/bölgesel banka/biyotek açılış boşluğu. |
| 10 yıllık ABD tahvil vadelisi | `CBOT:ZN1!` | Faiz hareketi gece de işler; banka/konut ETF'lerinin açılışını etkiler. |
| ABD 2 yıllık getiri | `TVC:US02Y` | Fed beklentisi; bölgesel bankalar için marj/fonlama baskısı göstergesi. |

## 3. Takvim ve olay riskleri

FOMC karar günü: faize duyarlı 6 ETF'te gün içi brüt -26 bp (IS -32 / OOS -48), karar günü yeni long açma. CPI, banka bilançoları (Ocak/Nisan/Temmuz/Ekim ortası), Fed stres testi (Haziran).

## 4. Notlar

Doğrulanmış gecikmeli öncü yok. (XLF -> KRE t -1.85; ST04 XLF->KRE anlamsız).

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_sektor_tematik.md`, `notlar/denetim_sektor_tematik.md`.*
