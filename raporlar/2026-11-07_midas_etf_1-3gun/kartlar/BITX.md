# BITX — 2x Bitcoin ETF

**TradingView:** `CBOE:BITX` · **Aile:** Kripto · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 172 | 18.4 | 556 | %-26.2 | 2.0 | 2023-06-27 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** 2x BTC (172 mn$/gün, 18 bp). Dayanak sinyaliyle kaldıraçlı araç; ama 2×IBIT'e göre takip kaybı −11,5 bp/gün (t=−8,7; 3 günde −37 bp). Kaldıraçlı/ters ürünlerin Midas'ta bulunurluğu doğrulanmadı.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| BTC/USD (16:00 ET getirisi; eşzamanlı) | `COINBASE:BTCUSD` | 1.00 | 2.01 |
| IBIT | `NASDAQ:IBIT` | 1.00 | 2.00 |
| Nasdaq-100 (QQQ) | `NASDAQ:QQQ` | 0.49 | 2.04 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Bitcoin spot (Coinbase) | `COINBASE:BTCUSD` | 7/24 işler. ETF kapalıyken (TR 00:00-17:30, kış) BTC'nin 16:00 ET'den sonraki hareketi ertesi açılış boşluğunu belirler: IBIT açılış boşluğu ≈ BTC 16:00→09:30 ET hareketi (R²=0,96, eğim 1,00; Pazartesi R²=0,98 = hafta sonu hareketi). Öncü değil, açılışı önceden gösteren izleme aracı. |
| CME Bitcoin vadeli (ön ay) | `CME:BTC1!` | CME Globex Pazar-Cuma (kış: TR 02:00 → ertesi gün 01:00, günlük 1 saat ara); hafta sonu kapalı → Pazartesi 'CME boşluğu'. Kurumsal akış/baz (vadeli primi) göstergesi. |

## 3. Takvim ve olay riskleri

Bkz. IBIT girdisi: CPI 10 Kas 16:30; 26 Kas kapalı; NFP 4 Ara; FOMC 9 Ara 22:00; CPI 10 Ara (Per) 16:30; 24 Ara erken kapanış 21:00 (TR saati).

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK (sweep FDR 0; ek testler |t|<2). Sürücüler eşzamanlıdır; ayrıntı IBIT/ETHA girdisinde. Kaldıraçlı: 2× dayanak getirisi eksi ~8-12 bp/gün takip kaybı; dayanak (IBIT/ETHA) sinyalleriyle işlem aracı.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_kripto.md`, `notlar/denetim_kripto.md`.*
