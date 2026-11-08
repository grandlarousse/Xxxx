# URA — Global X Uranium ETF

**TradingView:** `AMEX:URA` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 171 | 16,0 | 318 | %-9,9 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Uranyum: 171 mn $, ~16 bp, oynaklık 320 bp. Strateji yok; risk iştahı (ES/NQ) ve EEM ile eşzamanlı hareket; SPY ile ters gecikmeli ilişki zayıf (FDR yok).

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| EEM (eşzamanlı sürücü, öncü değil) | `AMEX:EEM` | 0.69 | 1.35 |
| IWM (eşzamanlı sürücü, öncü değil) | `AMEX:IWM` | 0.69 | 1.88 |
| SMH (eşzamanlı sürücü, öncü değil) | `NASDAQ:SMH` | 0.67 | 0.80 |
| SPY (eşzamanlı sürücü, öncü değil) | `AMEX:SPY` | 0.65 | 2.43 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| SPY | `AMEX:SPY` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | -22.3 bp / 1 sd öncü hareketi (h=1); Negatif (SPY yükselince ertesi gün URA zayıf); IS -2,22 / OOS -1,48; kural (SPY z≤-1,5 -> URA long) t ≤ 1,25. | -2.6 (-2.2/-1.5) | doğrulanmadı (FDR yok) | zayıf — t -2,67, IS -2,38/OOS -1,49, -22 bp/sd (maliyet 16); FDR yok; ajanın kuralı t≤1,25. |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| S&P 500 e-mini | `CME_MINI:ES1!` | URA'nın SPY betası ~2,4 (1y); risk iştahı. |
| Nasdaq 100 e-mini | `CME_MINI:NQ1!` | Yapay zekâ/veri merkezi enerji teması (URA-SMH 0,67). |

## 3. Takvim ve olay riskleri

Kazatomprom/Cameco üretim açıklamaları, SPUT fon alımları, ABD enerji politikası haberleri; genel risk (FOMC/CPI).

## 4. Notlar

Doğrulanmış gecikmeli öncü yok. Fiziki uranyum (Sprott SPUT) ve Cameco gerçek zamanlı izlenebilir ama TradingView kodları doğrulanmadı (tv_dogrulanacak).

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
