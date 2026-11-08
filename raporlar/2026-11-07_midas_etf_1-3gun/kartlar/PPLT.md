# PPLT — abrdn Physical Platinum Shares ETF

**TradingView:** `AMEX:PPLT` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 44 | 20,0 | 320 | %-18,4 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Platin: 44 mn $, ~20 bp, oynaklık 320 bp. Strateji yok; NYMEX:PL1! ile izlenir. GDX sert düştüğü günün ertesinde PPLT de zayıf (kaçınma işareti, FDR'siz).

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| SLV (eşzamanlı sürücü, öncü değil) | `AMEX:SLV` | 0.84 | 0.66 |
| GLD (eşzamanlı sürücü, öncü değil) | `AMEX:GLD` | 0.76 | 1.36 |
| GDX (eşzamanlı sürücü, öncü değil) | `AMEX:GDX` | 0.76 | 0.76 |
| CPER (eşzamanlı sürücü, öncü değil) | `AMEX:CPER` | 0.65 | 1.19 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| GDX | `AMEX:GDX` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | +23.0 bp / 1 sd öncü hareketi (h=1); Kural: GDX z≥+1,5 -> PPLT C0 h1 net 6,6 bp (t 0,43); GDX z≤-1,5 -> PPLT ertesi gün zayıf (O1 h1 net -40 bp, t -3,55): yalnız 'o gün PPLT alma' filtresi. | 3.0 (2.9/1.5) | uzun yön kullanılamaz; kaçınma filtresi FDR'siz | zayıf — t 3,20, IS 3,42/OOS 1,49, 23 bp/sd (maliyet 20); etki çoğunlukla gece (t 3,40) -> PPLT kapanışının bayatlığı/platin vadelisinin 16:00 sonrası işlemesi; FDR yok; ajanın kuralı (GDX z≥1,5) t 0,43. |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| NYMEX platin vadeli | `NYMEX:PL1!` | ~23 saat; açılış boşluğu. |
| COMEX altın vadeli | `COMEX:GC1!` | Değerli metal kompleksi (PPLT-GLD 0,76). |

## 3. Takvim ve olay riskleri

WPIC arz-talep raporları, Rusya/Güney Afrika arz haberleri, otomotiv talebi; FOMC/CPI.

## 4. Notlar

Doğrulanmış gecikmeli öncü yok.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
