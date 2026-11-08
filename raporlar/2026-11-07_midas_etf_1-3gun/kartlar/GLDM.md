# GLDM — SPDR Gold MiniShares Trust

**TradingView:** `AMEX:GLDM` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 427 | 14.0 | 181 | %-10.1 | 1.0 | 2018-06-26 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** GLD kopyası (0,999), maliyet 14 bp, geçmiş 2018-06'dan. Uzun vadeli tutuş için ucuz gider oranı; 1-3 günde GLD'ye üstünlüğü yok.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| GLD (eşzamanlı sürücü, öncü değil) | `AMEX:GLD` | 1.00 | 0.99 |
| SLV (eşzamanlı sürücü, öncü değil) | `AMEX:SLV` | 0.84 | 0.37 |
| GDX (eşzamanlı sürücü, öncü değil) | `AMEX:GDX` | 0.86 | 0.49 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| COMEX altın vadeli (sürekli) | `COMEX:GC1!` | ~23 saat işler (TR kış 02:00-01:00); ETF kapalıyken oluşan hareket açılış boşluğunu gösterir. İzleme aracı, öncü değil. |
| Spot altın | `OANDA:XAUUSD` | Asya/Londra seansı; TR 12:00-17:30 arasında GLD açılışını önceden gösterir. |

## 3. Takvim ve olay riskleri

FOMC 09.12.2026 14:00 ET (TR 22:00; örneklemde FOMC sonrası altın zayıf, anlamsız); CPI 10.11 ve 10.12.2026, NFP 04.12.2026 08:30 ET (TR 16:30, açılıştan 1 saat önce); COMEX teminat değişiklikleri (30.01.2026 gümüş şoku); Çin tatilleri Asya seansını inceltir; ay sonu 30.11.2026 (S1/S2).

## 4. Notlar

GLD kopyası; doğrulanmış gecikmeli öncü yok.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
