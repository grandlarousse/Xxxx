# SILJ — Amplify Junior Silver Miners ETF

**TradingView:** `AMEX:SILJ` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 139 | 16.0 | 377 | %-15.0 | 1.0 | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Genç gümüş madencileri: 139 mn $, ~16 bp; S5 (düşük güven) bu ETF'de; GDX ile 0,96 korelasyon.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| GDX (eşzamanlı sürücü, öncü değil) | `AMEX:GDX` | 0.96 | 1.13 |
| GLD (eşzamanlı sürücü, öncü değil) | `AMEX:GLD` | 0.83 | 1.73 |
| SLV (eşzamanlı sürücü, öncü değil) | `AMEX:SLV` | 0.83 | 0.76 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| SLV | `AMEX:SLV` | yetişme (beta60*r_L(t) - r_T(t) -> r_T(t+1..t+1)) | 1 gün | -8.9 bp / 1 sd öncü hareketi (h=1); Kendi gecikmesi kontrollü t -1.39. | -0.9 (-0.7/-0.5) | yok | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| COMEX altın vadeli | `COMEX:GC1!` | Madencilerin ana sürücüsü (GDX-GLD 0,86, beta 1,53); gece hareketi madenci açılışına ~1,5x yansır. |
| COMEX gümüş vadeli | `COMEX:SI1!` | ~23 saat işler; SLV/SIL açılış boşluğunu önceden gösterir. |
| S&P 500 e-mini | `CME_MINI:ES1!` | Madenciler hisse olduğu için genel risk iştahı; açılış öncesi yön. |

## 3. Takvim ve olay riskleri

FOMC 09.12.2026 14:00 ET (TR 22:00; örneklemde FOMC sonrası altın zayıf, anlamsız); CPI 10.11 ve 10.12.2026, NFP 04.12.2026 08:30 ET (TR 16:30, açılıştan 1 saat önce); COMEX teminat değişiklikleri (30.01.2026 gümüş şoku); Çin tatilleri Asya seansını inceltir; ay sonu 30.11.2026 (S1/S2). Ek: madenci bilanço dönemleri (Şub, Nis-May, Tem-Ağu, Eki-Kas).

## 4. Notlar

Doğrulanmış gecikmeli öncü yok.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
