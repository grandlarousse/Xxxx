# XOP — State Street SPDR S&P Oil & Gas Exploration & Production ETF

**TradingView:** `AMEX:XOP` · **Aile:** Enerji ve tarım emtiası · **İzleme kararı:** kabul  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 532 | 14,0 | 189 | %-6,4 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** [40act] maliyet/oynaklık 0.074. PTP'siz petrol/gaz üreticileri (532 mn$, 14 bp, oynaklık XLE'den yüksek). XLE ile 0,92-0,94 korelasyon. B8 sinyaliyle net 131 bp t 2,49 ama h=1/h=3'te ~0 (kırılgan). **Ana ajan notu:** Denetçi: PTP'siz, XLE kadar uygun 1-3 günlük enerji aracı.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| XLE | `AMEX:XLE` | 0.92 | 1.19 |
| USL | `AMEX:USL` | 0.74 | 0.71 |
| BNO | `AMEX:BNO` | 0.71 | 0.43 |

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

Doğrulanmış gecikmeli öncü YOK (ölçüt: FDR + IS/OOS aynı işaret + bp/sd > 14 bp maliyet; geçen 0). En güçlü geçmeyen: VVIX_dlog h3 t=-2.63 (IS -2.54/OOS -1.03, -23.1 bp/sd, FDR=H). Yetişme boşluğunun kendi getirisine ek katkısı: gap(UNG) h3 t=2.70 (IS 2.36/OOS 1.27, 109.8 bp/sd). Sürücüler eşzamanlıdır, öncü değildir.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_enerji_tarim.md`, `notlar/denetim_enerji_tarim.md`.*
