# UNG — United States Natural Gas Fund LP

**TradingView:** `AMEX:UNG` · **Aile:** Enerji ve tarım emtiası · **İzleme kararı:** yedek  
**Midas:** işlem görmüş (2023 kullanıcı kaydı; resmî ürün listesi yok) · ⚠ PTP/K-1 yapısı: satışta %10 brüt kesinti (1446(f)) riski — uygulamada 'PTP' ibaresini ve kesintiyi teyit etmeden kısa vadeli işlem yapmayın

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 137 | 22,7 | 363 | %-24,9 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** [PTP] maliyet/oynaklık 0.063. Doğalgaz dayanak referansı (137 mn$, 22,7 bp). Uzun vadeli negatif sürüklenme (koşulsuz -10 bp/gün); EIA günü long tutmayın. PTP ve Midas'ta 2024'te %10 kesinti şikâyeti belgelenmiş. Long araç olarak önerilmez.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| UNL | `AMEX:UNL` | 0.95 | 1.61 |
| USL | `AMEX:USL` | 0.25 | 0.47 |
| BNO | `AMEX:BNO` | 0.22 | 0.27 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| EIA doğalgaz depolama raporu takvimi (Kasım-Mart) — takvim olayı, gecikmeli fiyat öncüsü değil | yok (takvim: ir.eia.gov/ngs/schedule.html) | takvim_olayi (doğrulanmamış: FDR geçmiyor, post-hoc mevsim ayrımı) | 1 gün (rapor günü) | Kas-Mar rapor günü UNG -65 bp (diğer günler -5 bp); long araç için kaçın sinyali | -2.3 (-2.2/-1.2) | KOLD +100 bp net; UNG/BOIL long negatif | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Henry Hub doğalgaz vadelisi (ön ay) | `NYMEX:NG1!` | dayanak; Globex'te gece işler |
| Doğalgaz 2. ay | `NYMEX:NG2!` | NG2!/NG1!-1 kontango göstergesi |
| Hollanda TTF gaz vadelisi | `ICEENDEX:TFM1!` | Avrupa gazı; ABD açılışından önce işler |

## 3. Takvim ve olay riskleri

EIA depolama: 13 Kas Cum, 19 Kas, 25 Kas Çar 12:00 ET, 3/10/17/24/31 Ara (TR 18:30); NG vadesi 25 Kas, 29 Ara; UNG roll 11-16 Kas, 15-18 Ara; BOIL/KOLD roll 8-14 Ara 2026.

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK (ölçüt: FDR + IS/OOS aynı işaret + bp/sd > 23 bp maliyet; geçen 0). En güçlü geçmeyen: KWEB h3 t=2.55 (IS 2.26/OOS 1.62, 31.0 bp/sd, FDR=H). Yetişme boşluğunun kendi getirisine ek katkısı: gap(BOIL) h1 t=0.93 (IS -0.15/OOS 1.12, 7.8 bp/sd). Sürücüler eşzamanlıdır, öncü değildir.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_enerji_tarim.md`, `notlar/denetim_enerji_tarim.md`.*
