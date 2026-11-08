# NVDU — Direxion Daily NVDA Bull 2X ETF

**TradingView:** `NASDAQ:NVDU` · **Aile:** Tek hisse kaldıraçlı · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 49 | 20.0 | 479 | %-18.8 | 2.0 | 2023-09-13 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** NVDL'nin kopyası (aynı dayanak, 2x; günlük getiri korelasyonu 1,00). Hacim 49 mn$, maliyet 20 bp (NVDL 16 bp). Yalnız Midas'ta NVDL yoksa S1 için.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| NVDA (dayanak hisse, aynı gün) | `NASDAQ:NVDA` | 1.00 | 1.99 |
| XLK günlük getiri (aynı gün) | `AMEX:XLK` | 0.75 | 2.01 |
| SMH günlük getiri (aynı gün) | `NASDAQ:SMH` | 0.73 | 1.31 |
| QQQ günlük getiri (aynı gün) | `NASDAQ:QQQ` | 0.72 | 2.57 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| XLK'ya göre geride kalma (beta60 x r_XLK - r_NVDA) (t) -> NVDA t+1 | `AMEX:XLK` | gecikmeli (yetisme), NEGATİF katsayı | 1 gün | 1 sd XLK hareketi -> 2x ETF'te ertesi gün -64 bp (ters yönde); maliyet 16 bp | -2.7 (-3.6/-0.1) | FDR yalnız 152 testlik ek lead-lag ailesinde; birleşik FDR yok; OOS zayıf. Kurala çevrilince (piyasa z<-2 -> 2x long) maliyet sonrası doğrulanmadı (bkz. elenen). | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| NVDA uzatılmış seans (pre-market 04:00-09:30 ET = TR kış 12:00-17:30; after-hours 16:00-20:00 ET = TR kış 00:00-04:00) | `NASDAQ:NVDA` | ETF açılış boşluğunun ana kaynağı (≈2x). Grafikte uzatılmış saatleri aç; bilanço tepkisi after-hours'ta görülür. |
| Nasdaq 100 E-mini vadelisi | `CME_MINI:NQ1!` | ~23 saat işler; ETF kapalıyken piyasa yönünü gösterir (izleme, öncü değil). |
| Nikkei 225 vadelisi (OSE) | `OSE:NK2251!` | Asya seansı teknoloji risk iştahı (yalnız bağlam). |

## 3. Takvim ve olay riskleri

NVDA sonraki bilanço 2026-11-17 seans sonrası (16:00 ET sonrası; TR kış 00:00 sonrası) (Nasdaq/Zacks tahmini). Ortak: CPI 10.11 ve 10.12 (TR 16:30); opex 20.11; 26.11 kapalı, 27.11 erken kapanış (TR 21:00); NFP 04.12 (TR 16:30); FOMC 09.12 (TR 22:00); triple witching 18.12; 24.12 erken kapanış, 25.12 kapalı.

## 4. Notlar

İşlem için doğrulanmış gecikmeli öncü yok (genel taramada aile FDR bayrağı 0). Ek dayanak testindeki ilişkiler NEGATİF işaretli piyasa-geri dönüşü; OOS zayıf, kural olarak maliyet sonrası doğrulanmadı. Sürücüler eşzamanlıdır, öncü değil. NVDL <- SMH: SMH getirisi -> NVDA t+1 t=-1,72 (IS -2,69, OOS +0,30), yetişme t=-2,08 (OOS -0,13); kural (yetişme>=2sd, C0 h1) +68 bp t=0,55: öncü değil.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_tek_hisse_kaldiracli.md`, `notlar/denetim_tek_hisse_kaldiracli.md`.*
