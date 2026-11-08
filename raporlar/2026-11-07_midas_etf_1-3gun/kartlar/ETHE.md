# ETHE — Grayscale Ethereum Staking ETF Shares

**TradingView:** `AMEX:ETHE` · **Aile:** Kripto · **İzleme kararı:** kabul  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 50 | 17,6 | 382 | %-13,9 | 1,0x | 2024-07-23 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** ETHA kopyası (corr 0,9997); 50 mn$/gün, makas ~6 bp (18 bp). Midas'ta sembol sayfası DOĞRULANMIŞ → ETHA yoksa kullan. **Ana ajan notu:** Midas'ta sembol sayfası doğrulanmış spot ETH ETF'i; ETHA ile eş birincil.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| ETH/USD (16:00 ET getirisi; eşzamanlı) | `COINBASE:ETHUSD` | 1.00 | 1.00 |
| ETHA | `NASDAQ:ETHA` | 1.00 | 0.99 |

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

Doğrulanmış gecikmeli öncü YOK (sweep FDR 0; ek testler |t|<2). Sürücüler eşzamanlıdır; ayrıntı IBIT/ETHA girdisinde. ETHA kopyası (corr 0,9997).

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_kripto.md`, `notlar/denetim_kripto.md`.*
