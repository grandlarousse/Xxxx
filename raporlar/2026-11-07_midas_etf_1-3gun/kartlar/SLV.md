# SLV — iShares Silver Trust

**TradingView:** `AMEX:SLV` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 1,376 | 14.1 | 398 | %-28.5 | 1.0 | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Gümüşün ana aracı: 1,4 mlr $, ~14 bp, 1g oynaklık ~400 bp (maliyet/oynaklık 0,035). Doğrulanmış strateji YOK; COMEX:SI1! ve altın ile izlenir. 30.01.2026'da -%28,5 (tek gün) gerçek kuyruk riski. **Ana ajan notu:** Strateji/öncü yok; COMEX:SI1! ile izlenir; 30.01.2026'da tek gün -%28,5.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| GLD (eşzamanlı sürücü, öncü değil) | `AMEX:GLD` | 0.84 | 1.92 |
| GDX (eşzamanlı sürücü, öncü değil) | `AMEX:GDX` | 0.81 | 1.05 |
| CPER (eşzamanlı sürücü, öncü değil) | `AMEX:CPER` | 0.69 | 1.61 |
| UUP (eşzamanlı sürücü, öncü değil) | `AMEX:UUP` | -0.39 | -3.84 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| T10YIE_d | `FRED:T10YIE` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | +14.8 bp / 1 sd öncü hareketi (h=1); Kural (≥+5 bp -> SLV): O1 h1 net -7 bp, OOS negatif; etki yalnız C0 gecesinde (veri o an bilinmez). | 3.4 (3.3/1.8) | kullanılamaz | denetlenmedi |
| GDX | `AMEX:GDX` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | +13.8 bp / 1 sd öncü hareketi (h=1);  | 1.4 (1.2/0.7) | anlamsız | denetlenmedi |
| GLD | `AMEX:GLD` | yetişme (beta60*r_L(t) - r_T(t) -> r_T(t+1..t+1)) | 1 gün | -2.3 bp / 1 sd öncü hareketi (h=1);  | -0.3 (0.5/-0.6) | anlamsız | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| COMEX gümüş vadeli | `COMEX:SI1!` | ~23 saat işler; SLV/SIL açılış boşluğunu önceden gösterir. |
| Spot gümüş | `OANDA:XAGUSD` | Asya/Londra seansı gümüş fiyatı. |
| COMEX altın vadeli | `COMEX:GC1!` | Gümüşün ana eşzamanlı sürücüsü (SLV-GLD 0,84). |

## 3. Takvim ve olay riskleri

FOMC 09.12.2026 14:00 ET (TR 22:00; örneklemde FOMC sonrası altın zayıf, anlamsız); CPI 10.11 ve 10.12.2026, NFP 04.12.2026 08:30 ET (TR 16:30, açılıştan 1 saat önce); COMEX teminat değişiklikleri (30.01.2026 gümüş şoku); Çin tatilleri Asya seansını inceltir; ay sonu 30.11.2026 (S1/S2).

## 4. Notlar

Doğrulanmış gecikmeli öncü yok. 30.01.2026 (-%28,5) gibi teminat/likidasyon şokları gece oluşur; gerçek zamanlı COMEX:SI1! izlenmeli.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
