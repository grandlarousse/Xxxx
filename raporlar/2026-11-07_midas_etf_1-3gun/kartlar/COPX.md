# COPX — Global X Copper Miners ETF

**TradingView:** `AMEX:COPX` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 239 | 14,0 | 302 | %-10,6 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Bakır madencileri: 239 mn $, ~14 bp, oynaklık 302 bp; CPER'in likit/PTP'siz alternatifi. Strateji yok; COMEX:HG1! ve Çin göstergeleriyle izlenir. **Ana ajan notu:** Strateji yok; COMEX:HG1! ile izlenir.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| CPER (eşzamanlı sürücü, öncü değil) | `AMEX:CPER` | 0.82 | 1.39 |
| GDX (eşzamanlı sürücü, öncü değil) | `AMEX:GDX` | 0.80 | 0.75 |
| EEM (eşzamanlı sürücü, öncü değil) | `AMEX:EEM` | 0.75 | 1.36 |
| FXI (eşzamanlı sürücü, öncü değil) | `AMEX:FXI` | 0.46 | 1.14 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| CPER | `AMEX:CPER` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | +5.1 bp / 1 sd öncü hareketi (h=1); IS 2,19 / OOS -2,08: işaret değişti. | 0.5 (2.2/-2.1) | kullanılamaz | denetlenmedi |
| GDX | `AMEX:GDX` | gecikmeli (r_L(t) -> r_T(t+1..t+3), kendi gecikmesi kontrollü) | 3 gün | +35.2 bp / 1 sd öncü hareketi (h=3); Kural GDX z≥+1,5 -> COPX: C0 h3 net 40 bp (t 1,27), O1 negatif; GDX z≤-1,5 sonrası COPX zayıf (C0 h1 net -48 bp, t -1,95). | 2.6 (2.7/1.5) | doğrulanmadı (FDR yok) | zayıf — t 2,76, IS 3,02/OOS 1,58, 36 bp/sd (h3) > 14 bp; gece t 2,44, gün içi 0,89; kural t 1,27, O1 negatif; FDR yok. |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| COMEX bakır vadeli | `COMEX:HG1!` | ~23 saat işler; COPX açılış boşluğunu önceden gösterir (COPX-CPER 0,82, beta 1,39). |
| Hang Seng vadeli | `HKEX:HSI1!` | Çin risk iştahı; TR sabahı Asya seansı. |
| USD/CNH | `FX_IDC:USDCNH` | Çin para birimi; bakır talebi beklentisi. |
| S&P 500 e-mini | `CME_MINI:ES1!` | Genel risk iştahı (madencilik hissesi). |

## 3. Takvim ve olay riskleri

Çin PMI/ticaret verileri (TR 04:30-05:00), ABD tarife kararları (30.07.2025 CPER -%19), FOMC/CPI genel risk.

## 4. Notlar

Doğrulanmış gecikmeli öncü yok. Bakır vadeli (HG1!) ve Asya seansı açılış boşluğunu gösterir.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
