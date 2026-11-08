# ETHU — 2x Ether ETF

**TradingView:** `CBOE:ETHU` · **Aile:** Kripto · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 144 | 17.0 | 767 | %-28.4 | 2.0 | 2024-06-04 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** 2x ETH (144 mn$/gün, 17 bp); 2×ETHA'ya göre takip kaybı −7,9 bp/gün. Kendi stratejisi yok; ETH sinyali için kaldıraçlı araç. Günlük oynaklık 767 bp (en kötü gün −28%).

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| ETH/USD (16:00 ET getirisi; eşzamanlı) | `COINBASE:ETHUSD` | 1.00 | 2.03 |
| ETHA | `NASDAQ:ETHA` | 1.00 | 2.01 |
| BTC/USD (16:00 ET getirisi; eşzamanlı) | `COINBASE:BTCUSD` | 0.92 | 2.56 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Ethereum spot (Coinbase) | `COINBASE:ETHUSD` | 7/24; ETHA açılış boşluğunu belirleyen dayanak (ETF kapalıyken TR 00:00-17:30, kış). |
| CME Ether vadeli (ön ay) | `CME:ETH1!` | CME Globex Pazar-Cuma; hafta sonu kapalı; kurumsal akış/baz göstergesi. |

## 3. Takvim ve olay riskleri

Bkz. IBIT girdisi: CPI 10 Kas 16:30; 26 Kas kapalı; NFP 4 Ara; FOMC 9 Ara 22:00; CPI 10 Ara (Per) 16:30; 24 Ara erken kapanış 21:00 (TR saati).

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK (sweep FDR 0; ek testler |t|<2). Sürücüler eşzamanlıdır; ayrıntı IBIT/ETHA girdisinde. Kaldıraçlı: 2× dayanak getirisi eksi ~8-12 bp/gün takip kaybı; dayanak (IBIT/ETHA) sinyalleriyle işlem aracı.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_kripto.md`, `notlar/denetim_kripto.md`.*
