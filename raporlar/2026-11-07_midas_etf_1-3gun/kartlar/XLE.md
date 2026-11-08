# XLE — State Street Energy Select Sector SPDR ETF

**TradingView:** `AMEX:XLE` · **Aile:** Enerji ve tarım emtiası · **İzleme kararı:** kabul  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 2.016 | 13,6 | 147 | %-4,7 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** [40act] maliyet/oynaklık 0.093. Ailenin en likit ve PTP'siz aracı (2 mlr$, 13,6 bp). Doğrulanmış strateji yok (EN06 yetişme, EN08 IBS elendi; B8 sinyaliyle t 1,80); sürücüleri net (petrol, S&P 500). Enerjide PTP riski almadan yön görüşü için ana araç.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| USL | `AMEX:USL` | 0.70 | 0.52 |
| BNO | `AMEX:BNO` | 0.65 | 0.31 |
| USO | `AMEX:USO` | 0.63 | 0.29 |

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

Doğrulanmış gecikmeli öncü YOK (ölçüt: FDR + IS/OOS aynı işaret + bp/sd > 14 bp maliyet; geçen 0). En güçlü geçmeyen: KWEB h3 t=2.75 (IS 1.88/OOS 2.00, 20.4 bp/sd, FDR=H). Yetişme boşluğunun kendi getirisine ek katkısı: gap(XOP) h1 t=2.20 (IS 1.60/OOS 1.92, 18.1 bp/sd). Sürücüler eşzamanlıdır, öncü değildir.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_enerji_tarim.md`, `notlar/denetim_enerji_tarim.md`.*
