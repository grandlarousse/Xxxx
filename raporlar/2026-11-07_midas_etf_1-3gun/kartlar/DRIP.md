# DRIP — Direxion Daily S&P Oil & Gas Exp. & Prod. Bear 2X ETF

**TradingView:** `AMEX:DRIP` · **Aile:** Enerji ve tarım emtiası · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 55 | 16.0 | 379 | %-11.4 | -2.0 | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** [40act] maliyet/oynaklık 0.042. -2x XOP (55 mn$, 16 bp); PTP'siz enerji düşüş aracı (ERY'den likit/ucuz). Doğrulanmış strateji yok.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| XLE | `AMEX:XLE` | -0.92 | -2.36 |
| USL | `AMEX:USL` | -0.74 | -1.40 |
| BNO | `AMEX:BNO` | -0.70 | -0.86 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| S&P 500 e-mini | `CME_MINI:ES1!` | genel hisse yönü |
| WTI vadelisi | `NYMEX:CL1!` | petrol hareketi aynı gün yansır |
| Doğalgaz vadelisi | `NYMEX:NG1!` | gaz üreticileri |

## 3. Takvim ve olay riskleri

EIA WPSR (Çar); CPI 10 Kas, NFP 4 Ara, FOMC 9 Ara 2026; yarım gün 27 Kas (TR 21:00).

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK (ölçüt: FDR + IS/OOS aynı işaret + bp/sd > 16 bp maliyet; geçen 0). En güçlü geçmeyen: VVIX_dlog h3 t=2.46 (IS 2.27/OOS 0.98, 46.8 bp/sd, FDR=H). Yetişme boşluğunun kendi getirisine ek katkısı: gap(XLE) h1 t=-1.69 (IS -1.60/OOS -0.66, -47.9 bp/sd). Sürücüler eşzamanlıdır, öncü değildir.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_enerji_tarim.md`, `notlar/denetim_enerji_tarim.md`.*
