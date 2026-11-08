# ASHR — Xtrackers Harvest CSI 300 China A-Shares ETF

**TradingView:** `AMEX:ASHR` · **Aile:** Uluslararası / ülke · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 148 | 16,0 | 115 | %-3,3 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Çin A payları (148 mn $, 16 bp). B4 genişletilmiş kontrolde C0 h=1 net +51 bp (t 1,60), IS ve OOS > 0.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| EEM | `AMEX:EEM` | 0.68 | 0.47 |
| SMH | `NASDAQ:SMH` | 0.60 | 0.26 |
| EWJ | `AMEX:EWJ` | 0.58 | 0.48 |
| QQQ | `NASDAQ:QQQ` | 0.57 | 0.49 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| CSI 300 | `SSE:000300` | dayanak; kapanış TR 10:00 |
| FTSE China A50 vadelisi | `SGX:CN1!` | gece seansı |
| USD/CNH | `FX:USDCNH` | 24 saat kur |

## 3. Takvim ve olay riskleri

ABD: CPI 10 Kas, NFP 4 Ara, CPI 10 Ara, FOMC 9 Ara 2026 (Asya'ya ertesi sabah yansır); NYSE 26 Kas kapalı, 27 Kas/24 Ara erken kapanış (TR 21:00). Yerel tatillerde ETF NAV'sız işlem görür. Çin/HK: Ay Yeni Yılı (Şub 2027 başı, teyit edilmeli), teşvik/kur haberleri; YINN 3x.

## 4. Notlar

Doğrulanmış (doğrusal) gecikmeli öncü YOK: aile içi BH-FDR geçen çift yok. En güçlü aday (FDR'siz): XLE h1 t=-2.48 (IS -3.86/OOS 0.42), h3 t=-1.88. Sürücüler eşzamanlıdır, öncü değildir.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_uluslararasi.md`, `notlar/denetim_uluslararasi.md`.*
