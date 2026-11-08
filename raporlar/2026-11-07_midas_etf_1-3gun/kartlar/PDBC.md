# PDBC — Invesco Optimum Yield Diversified Commodity Strategy No K-1 ETF

**TradingView:** `NASDAQ:PDBC` · **Aile:** Enerji ve tarım emtiası · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 92 | 17.3 | 134 | %-4.3 | 1.0 | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** [40act] maliyet/oynaklık 0.130. K-1'siz geniş emtia (92 mn$, 17 bp), USO ile 0,89 korelasyon: petrol görüşü için PTP'siz ama düşük oynaklıklı vekil (maliyet/oynaklık 0,13). Doğrulanmış strateji yok.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| BNO | `AMEX:BNO` | 0.90 | 0.39 |
| USO | `AMEX:USO` | 0.89 | 0.37 |
| USL | `AMEX:USL` | 0.89 | 0.59 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| WTI vadelisi | `NYMEX:CL1!` | en büyük bileşen enerji |
| Brent | `ICEEUR:BRN1!` | petrol |
| Altın | `COMEX:GC1!` | metal |
| Bakır | `COMEX:HG1!` | metal |
| Mısır | `CBOT:ZC1!` | tarım |

## 3. Takvim ve olay riskleri

EIA WPSR (Çar); CPI 10 Kas, FOMC 9 Ara 2026; dolar şokları.

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK (ölçüt: FDR + IS/OOS aynı işaret + bp/sd > 17 bp maliyet; geçen 0). En güçlü geçmeyen: KWEB h3 t=3.08 (IS 2.02/OOS 2.55, 17.5 bp/sd, FDR=H). Yetişme boşluğunun kendi getirisine ek katkısı: gap(DBA) h1 t=2.08 (IS 2.18/OOS 0.92, 12.3 bp/sd). Sürücüler eşzamanlıdır, öncü değildir.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_enerji_tarim.md`, `notlar/denetim_enerji_tarim.md`.*
