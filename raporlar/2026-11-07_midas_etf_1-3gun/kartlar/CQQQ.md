# CQQQ — Invesco China Technology ETF

**TradingView:** `AMEX:CQQQ` · **Aile:** Uluslararası / ülke · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 46 | 20,0 | 194 | %-5,3 | 1,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Çin teknoloji (46 mn $, 20 bp). B4 genişletilmiş kontrolde C0 h=1 net +47 bp (t 1,60), IS ve OOS > 0.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| KWEB | `AMEX:KWEB` | 0.69 | 0.79 |
| EEM | `AMEX:EEM` | 0.68 | 0.79 |
| FXI | `AMEX:FXI` | 0.61 | 0.96 |
| QQQ | `NASDAQ:QQQ` | 0.58 | 0.84 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Hang Seng vadelisi | `HKEX:HSI1!` | gece seansı |
| USD/CNH | `FX:USDCNH` | 24 saat kur |

## 3. Takvim ve olay riskleri

ABD: CPI 10 Kas, NFP 4 Ara, CPI 10 Ara, FOMC 9 Ara 2026 (Asya'ya ertesi sabah yansır); NYSE 26 Kas kapalı, 27 Kas/24 Ara erken kapanış (TR 21:00). Yerel tatillerde ETF NAV'sız işlem görür. Çin/HK: Ay Yeni Yılı (Şub 2027 başı, teyit edilmeli), teşvik/kur haberleri; YINN 3x.

## 4. Notlar

Doğrulanmış (doğrusal) gecikmeli öncü YOK: aile içi BH-FDR geçen çift yok. En güçlü aday (FDR'siz): XLE h1 t=-3.00 (IS -4.87/OOS -0.35), h3 t=-1.98. Sürücüler eşzamanlıdır, öncü değildir.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_uluslararasi.md`, `notlar/denetim_uluslararasi.md`.*
