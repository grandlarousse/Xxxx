# SOXX — iShares PHLX SOX Semiconductor Sector Index Fund

**TradingView:** `NASDAQ:SOXX` · **Aile:** Sektör ve tematik · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 3,333 | 13.0 | 309 | %-12.1 | 1.0 | 2016-11-07 |

**Kademe:** A — denetimden geçmiş kural var  
**Neden izleme listesinde:** SMH'nin kopyası (korelasyon 0.98): S1 aynı sonucu veriyor (43 bp, t 3.9) ama bağımsız kanıt değil; SMH daha likit.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

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
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_sektor_tematik.md`, `notlar/denetim_sektor_tematik.md`.*
