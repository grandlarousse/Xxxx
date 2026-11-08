# MSTU — T-Rex 2X Long MSTR Daily Target ETF

**TradingView:** `CBOE:MSTU` · **Aile:** Tek hisse kaldıraçlı · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 176 | 16.0 | 1026 | %-33.9 | 2.0 | 2024-09-18 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Doğrulanmış strateji YOK (S1 MSTR'de n=68, t=0,78; TH06 BTC öncülüğü yok). Yalnız net sürücüyle takip edilebilir: BTC (corr_1y 0,86); BTC'nin gece hareketi (16:00->09:00 ET) MSTR açılış boşluğu varyansının %77'sini açıklıyor. Maliyet/oynaklık oranı ailede en iyi (0,016) ama 3 günlük tutuşta 2xMSTR'den ort. -57 bp geride (swap finansmanı), 1y getiri -%89, son 1y en kötü gün -%33,9. Çok küçük pozisyon dışında önerilmez.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| MSTR (dayanak hisse, aynı gün) | `NASDAQ:MSTR` | 1.00 | 1.97 |
| IBIT günlük getiri (aynı gün) | `NASDAQ:IBIT` | 0.86 | 3.09 |
| BTC 16:00 ET günlük getiri (aynı gün) | `COINBASE:BTCUSD` | 0.86 | 3.10 |
| BITO günlük getiri (aynı gün) | `AMEX:BITO` | 0.84 | 2.92 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Bitcoin spot (Coinbase) | `COINBASE:BTCUSD` | 7/24 işler. BTC'nin 16:00 ET -> ertesi 09:00 ET hareketi MSTR açılış boşluğuyla corr 0,88, beta 1,22 (MSTU ≈ 2x): gece BTC %5 düşerse MSTU açılışı ~%12 aşağı beklenir. |
| CME Bitcoin vadelisi | `CME:BTC1!` | Kurumsal BTC fiyatı; hafta sonu kapalı. |
| MSTR uzatılmış seans | `NASDAQ:MSTR` | Pre-market TR kış 12:00-17:30. |

## 3. Takvim ve olay riskleri

MSTR sonraki bilanço tarihi henüz açıklanmadı (Nasdaq boş); 2023-2026 düzenine göre yaklaşık 02.02-05.02.2027 arası, seans sonrası (tepki ertesi gün açılış boşluğunda). Son duyuru 2026-10-29. Ortak: CPI 10.11 ve 10.12 (TR 16:30); opex 20.11; 26.11 kapalı, 27.11 erken kapanış (TR 21:00); NFP 04.12 (TR 16:30); FOMC 09.12 (TR 22:00); triple witching 18.12; 24.12 erken kapanış, 25.12 kapalı.

## 4. Notlar

Doğrulanmış gecikmeli öncü yok. TH06: BTC 16:00 ET artığı -> MSTR ertesi gün t=-0,98 (h1), BTC getirisi t=-1,26, yetişme boşluğu t=-0,89 (2023-06+, IS yok). Kural testi (u>=2sd -> 2x long, C0 h1) n=45 +213 bp t=0,85. BTC yalnız eşzamanlı sürücü ve gerçek zamanlı izleme aracıdır.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_tek_hisse_kaldiracli.md`, `notlar/denetim_tek_hisse_kaldiracli.md`.*
