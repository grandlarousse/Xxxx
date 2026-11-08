# SCO — ProShares UltraShort Bloomberg Crude Oil

**TradingView:** `AMEX:SCO` · **Aile:** Enerji ve tarım emtiası · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı · ⚠ PTP/K-1 yapısı: satışta %10 brüt kesinti (1446(f)) riski — uygulamada 'PTP' ibaresini ve kesintiyi teyit etmeden kısa vadeli işlem yapmayın

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 102 | 17,3 | 399 | %-12,2 | -2,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** [PTP] maliyet/oynaklık 0.043. -2x ham petrol (102 mn$, 17 bp); açığa satış olmadığından petrol düşüş görüşü için tek pratik araç. Doğrulanmış strateji yok. PTP.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| USL | `AMEX:USL` | -0.98 | -1.96 |
| BNO | `AMEX:BNO` | -0.92 | -1.20 |
| USO | `AMEX:USO` | -0.91 | -1.14 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| WTI ham petrol vadelisi (ön ay) | `NYMEX:CL1!` | dayanak; Globex ~23 saat, açılış boşluğunu önceden gösterir |
| WTI 2. ay | `NYMEX:CL2!` | CL2!/CL1!-1 kontango göstergesi |
| Brent vadelisi (ön ay) | `ICEEUR:BRN1!` | Brent; Londra saatlerinde fiyat keşfi |
| Dolar endeksi | `TVC:DXY` | dolar şoku emtiaya ters |

## 3. Takvim ve olay riskleri

EIA WPSR Çar 10:30 ET (TR 18:30; 12 Kas Per 12:00 ET); API Salı 16:30 ET; CL vadesi 20 Kas, 21 Ara 2026; USO roll 1-7 Ara 2026; OVX >= 1,25xSMA20 iken boyutu küçült.

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK (ölçüt: FDR + IS/OOS aynı işaret + bp/sd > 17 bp maliyet; geçen 0). En güçlü geçmeyen: VVIX_dlog h3 t=2.84 (IS 1.83/OOS 2.27, 44.0 bp/sd, FDR=H). Yetişme boşluğunun kendi getirisine ek katkısı: gap(USO) h3 t=0.75 (IS 0.88/OOS -0.21, 17.9 bp/sd). Sürücüler eşzamanlıdır, öncü değildir.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_enerji_tarim.md`, `notlar/denetim_enerji_tarim.md`.*
