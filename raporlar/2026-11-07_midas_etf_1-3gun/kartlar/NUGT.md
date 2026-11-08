# NUGT — Direxion Daily Gold Miners Index Bull 2X ETF

**TradingView:** `AMEX:NUGT` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 110 | 16.0 | 635 | %-25.2 | 2.0 | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** 2x GDX (1940 Kanunu, PTP değil; Midas'ta bulunurluğu doğrulanmadı). 2020-Q2'ye kadar 3x idi. S1'in kaldıraçlı uygulaması; 2x dönemde 3 günlük oynaklık kaybı ~-5 bp (küçük), ama maxDD ve tek işlem kaybı ~2 kat.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| GDX (eşzamanlı sürücü, öncü değil) | `AMEX:GDX` | 1.00 | 1.99 |
| GLD (eşzamanlı sürücü, öncü değil) | `AMEX:GLD` | 0.87 | 3.04 |
| SLV (eşzamanlı sürücü, öncü değil) | `AMEX:SLV` | 0.82 | 1.27 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| GLD | `AMEX:GLD` | yetişme (beta60*r_L(t) - r_T(t) -> r_T(t+1..t+1)) | 1 gün | -17.3 bp / 1 sd öncü hareketi (h=1);  | -0.7 (-0.5/-0.7) | yok | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| COMEX altın vadeli | `COMEX:GC1!` | Madencilerin ana sürücüsü (GDX-GLD 0,86, beta 1,53); gece hareketi madenci açılışına ~1,5x yansır. |
| COMEX gümüş vadeli | `COMEX:SI1!` | İkincil sürücü (GDX-SLV 0,81). |
| S&P 500 e-mini | `CME_MINI:ES1!` | Madenciler hisse olduğu için genel risk iştahı; açılış öncesi yön. |

## 3. Takvim ve olay riskleri

FOMC 09.12.2026 14:00 ET (TR 22:00; örneklemde FOMC sonrası altın zayıf, anlamsız); CPI 10.11 ve 10.12.2026, NFP 04.12.2026 08:30 ET (TR 16:30, açılıştan 1 saat önce); COMEX teminat değişiklikleri (30.01.2026 gümüş şoku); Çin tatilleri Asya seansını inceltir; ay sonu 30.11.2026 (S1/S2). Ek: madenci bilanço dönemleri (Şub, Nis-May, Tem-Ağu, Eki-Kas).

## 4. Notlar

2x GDX; sinyaller GDX'ten alınır. Doğrulanmış gecikmeli öncü yok.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
