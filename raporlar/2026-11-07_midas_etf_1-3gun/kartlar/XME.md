# XME — State Street SPDR S&P Metals & Mining ETF

**TradingView:** `AMEX:XME` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 226 | 14,0 | 238 | %-7,8 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Metal-madencilik hisseleri: 226 mn $, ~14 bp. Ay sonu kuralı XME'de de eşikte (t 2,33) -> B3a ailesinin kanıtı; tek başına strateji değil.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| GDX (eşzamanlı sürücü, öncü değil) | `AMEX:GDX` | 0.75 | 0.55 |
| IWM (eşzamanlı sürücü, öncü değil) | `AMEX:IWM` | 0.72 | 1.45 |
| CPER (eşzamanlı sürücü, öncü değil) | `AMEX:CPER` | 0.67 | 0.89 |
| EEM (eşzamanlı sürücü, öncü değil) | `AMEX:EEM` | 0.68 | 0.98 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| DIA | `AMEX:DIA` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | -28.1 bp / 1 sd öncü hareketi (h=1); Negatif katsayı (DIA yükselince ertesi gün XME zayıf), FDR yok. | -2.9 (-2.6/-1.4) | kullanılamaz | zayıf — t -2,80, IS -2,69/OOS -1,47; FDR yok; 13.694 testlik taramada bu düzey t beklenen gürültü. |
| CPER | `AMEX:CPER` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | -2.8 bp / 1 sd öncü hareketi (h=1);  | -0.4 (0.5/-1.4) | anlamsız | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| COMEX bakır vadeli | `COMEX:HG1!` | Baz metal fiyatı. |
| Russell 2000 e-mini | `CME_MINI:RTY1!` | XME küçük/orta ölçekli döngüsel hisse; IWM ile 0,72. |
| COMEX altın vadeli | `COMEX:GC1!` | Altın madencisi ağırlığı (GDX ile 0,75). |

## 3. Takvim ve olay riskleri

ABD çelik/alüminyum tarife kararları, Çin PMI, ay sonu (B3a ailesi). FOMC/CPI genel risk.

## 4. Notlar

Doğrulanmış gecikmeli öncü yok.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
