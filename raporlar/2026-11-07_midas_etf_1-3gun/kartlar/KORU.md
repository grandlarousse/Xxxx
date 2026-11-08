# KORU — Direxion Daily South Korea Bull 3X ETF

**TradingView:** `AMEX:KORU` · **Aile:** Uluslararası / ülke · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 405 | 26.5 | 1104 | %-41.9 | 3.0 | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** EWY'nin 3x kaldıraçlısı (405 mn $, 26 bp). Kendi sinyali yok; EWY sinyaliyle (S1/S2) kaldıraçlı uygulama aracı. Midas'ta bulunurluk doğrulanmadı; 1 günlük oynaklık 1.100 bp, son 1 yılda en kötü gün -%42.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| EWY (dayanak) | `AMEX:EWY` | 0.99 | 3.01 |
| EEM | `AMEX:EEM` | 0.93 | 6.43 |
| SMH | `NASDAQ:SMH` | 0.83 | 3.54 |
| XLK | `AMEX:XLK` | 0.79 | 5.04 |
| QQQ | `NASDAQ:QQQ` | 0.78 | 6.63 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| SPY koşullu kuralı (S1: SPY<=-%1,5 ve ETF<=SPY) | `AMEX:SPY` | koşullu eşik; doğrusal testte doğrulanmadı | t+1 | Koşul EWY'de sağlandığında KORU ertesi gün brüt 283 bp (n=68); en kötü -3188 bp | 1.9 (—/—) | KORU için 2.500$'da net 257 bp (IS 122 / OOS 369); t<2 -> eşik altında | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| KOSPI (seans TR 03:00-09:30) | `KRX:KOSPI` | EWY açılış boşluğunu belirleyen yerel seans |
| Nasdaq 100 vadelisi | `CME_MINI:NQ1!` | gece yön; yarı iletken ağırlığı |
| S&P 500 vadelisi | `CME_MINI:ES1!` | gece risk iştahı |

## 3. Takvim ve olay riskleri

ABD: CPI 10 Kas, NFP 4 Ara, CPI 10 Ara, FOMC 9 Ara 2026 (Asya'ya ertesi sabah yansır); NYSE 26 Kas kapalı, 27 Kas/24 Ara erken kapanış (TR 21:00). Yerel tatillerde ETF NAV'sız işlem görür. Kore: Seollal (Şub 2027 başı), çeyreklik vade 10 Ara 2026; KORU'da 3x günlük yeniden dengeleme.

## 4. Notlar

Doğrulanmış (doğrusal) gecikmeli öncü YOK: aile içi BH-FDR geçen çift yok. En güçlü aday (FDR'siz): TIP h1 t=2.40 (IS 2.05/OOS 1.37), h3 t=2.93. Sürücüler eşzamanlıdır, öncü değildir. SPY satırı S1'in koşullu kuralıdır, doğrusal öncü değildir. Reel faiz düşüşü (FRED:DFII10) 3 gün ufkunda pozitif aday (IS/OOS aynı işaret, FDR yok).

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_uluslararasi.md`, `notlar/denetim_uluslararasi.md`.*
