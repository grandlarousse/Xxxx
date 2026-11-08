# BNO — United States Brent Oil Fund, LP ETV

**TradingView:** `AMEX:BNO` · **Aile:** Enerji ve tarım emtiası · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 91 | 16.0 | 309 | %-10.3 | 1.0 | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** [PTP] maliyet/oynaklık 0.052. Brent; USO ile 0,97-0,98 korelasyon (bağımsız kanıt değil). USO yerine kullanılabilir (91 mn$, 16 bp); aynı PTP (USCF) riski.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| USO | `AMEX:USO` | 0.97 | 0.94 |
| USL | `AMEX:USL` | 0.92 | 1.43 |
| XLE | `AMEX:XLE` | 0.65 | 1.36 |

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

Doğrulanmış gecikmeli öncü YOK (ölçüt: FDR + IS/OOS aynı işaret + bp/sd > 16 bp maliyet; geçen 0). En güçlü geçmeyen: VVIX_dlog h3 t=-2.92 (IS -1.48/OOS -2.32, -24.9 bp/sd, FDR=H). Yetişme boşluğunun kendi getirisine ek katkısı: gap(USO) h1 t=0.73 (IS 0.65/OOS 0.38, 6.1 bp/sd). Sürücüler eşzamanlıdır, öncü değildir.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_enerji_tarim.md`, `notlar/denetim_enerji_tarim.md`.*
