# IEMG — iShares Core MSCI Emerging Markets ETF

**TradingView:** `AMEX:IEMG` · **Aile:** Uluslararası / ülke · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 897 | 14,0 | 160 | %-6,4 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** EEM'in kopyası (MSCI EM IMI); bağımsız kanıt değil. 897 mn $, 14 bp; EEM'e yedek.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| SMH | `NASDAQ:SMH` | 0.85 | 0.51 |
| QQQ | `NASDAQ:QQQ` | 0.84 | 1.00 |
| XLK | `AMEX:XLK` | 0.82 | 0.73 |
| EWJ | `AMEX:EWJ` | 0.80 | 0.93 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Hang Seng vadelisi | `HKEX:HSI1!` | Çin ağırlığı |
| KOSPI | `KRX:KOSPI` | Kore ağırlığı |
| USD/CNH | `FX:USDCNH` | 24 saat kur |
| S&P 500 vadelisi | `CME_MINI:ES1!` | gece risk iştahı |

## 3. Takvim ve olay riskleri

ABD: CPI 10 Kas, NFP 4 Ara, CPI 10 Ara, FOMC 9 Ara 2026 (Asya'ya ertesi sabah yansır); NYSE 26 Kas kapalı, 27 Kas/24 Ara erken kapanış (TR 21:00). Yerel tatillerde ETF NAV'sız işlem görür. EM: Çin+Kore+Tayvan+Hindistan takvimleri; MSCI Kasım endeks değişikliği ay sonu (teyit edilmeli).

## 4. Notlar

Doğrulanmış (doğrusal) gecikmeli öncü YOK: aile içi BH-FDR geçen çift yok. En güçlü aday (FDR'siz): KWEB h1 t=3.23 (IS 2.90/OOS 1.85), h3 t=0.65. Sürücüler eşzamanlıdır, öncü değildir. KWEB(t)->EEM(t+1) kısmi katsayısı pozitif (t 3,4) ama tek başına kural olarak ters işaretli -> kullanılamaz.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_uluslararasi.md`, `notlar/denetim_uluslararasi.md`.*
