# YINN — Direxion Daily FTSE China Bull 3X ETF

**TradingView:** `AMEX:YINN` · **Aile:** Uluslararası / ülke · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 56 | 16,0 | 362 | %-8,6 | 3,0x | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** FXI'nin 3x kaldıraçlısı (56 mn $, 16 bp). FXI sinyaliyle B4 uygulaması (C0 h=2 net +336 bp, t 2,27; C0 h=1 t 1,25). Midas'ta bulunurluk doğrulanmadı.

*Dayanak / ana araç kartı: `kartlar/FXI.md` (sürücüler ve gerçek zamanlı izleme listesi orada daha ayrıntılı).*

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| FXI (dayanak) | `AMEX:FXI` | 1.00 | 2.96 |
| KWEB | `AMEX:KWEB` | 0.88 | 1.88 |
| EEM | `AMEX:EEM` | 0.46 | 1.00 |
| SLV | `AMEX:SLV` | 0.42 | 0.36 |
| CPER | `AMEX:CPER` | 0.42 | 0.84 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| SPY koşullu kuralı (B4: SPY<=-%1,5 ve ETF<=SPY) | `AMEX:SPY` | koşullu eşik; doğrusal testte doğrulanmadı | t+1 | Koşul FXI'de sağlandığında YINN ertesi gün brüt 136 bp (n=50); en kötü -2706 bp | 1.2 (—/—) | YINN için 2.500$'da net 120 bp (IS 134 / OOS 108); t<2 -> eşik altında | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Hang Seng vadelisi | `HKEX:HSI1!` | gece seansı ~TR 12:15-22:00 |
| Hang Seng endeksi | `TVC:HSI` | yerel kapanış TR 11:00 |
| USD/CNH | `FX:USDCNH` | 24 saat kur |
| FTSE China A50 vadelisi | `SGX:CN1!` | uzun seans Çin duyarlılığı |

## 3. Takvim ve olay riskleri

ABD: CPI 10 Kas, NFP 4 Ara, CPI 10 Ara, FOMC 9 Ara 2026 (Asya'ya ertesi sabah yansır); NYSE 26 Kas kapalı, 27 Kas/24 Ara erken kapanış (TR 21:00). Yerel tatillerde ETF NAV'sız işlem görür. Çin/HK: Ay Yeni Yılı (Şub 2027 başı, teyit edilmeli), teşvik/kur haberleri; YINN 3x.

## 4. Notlar

Doğrulanmış (doğrusal) gecikmeli öncü YOK: aile içi BH-FDR geçen çift yok. En güçlü aday (FDR'siz): EEM h1 t=-2.51 (IS -2.80/OOS -0.85), h3 t=-0.69. Sürücüler eşzamanlıdır, öncü değildir. SPY satırı B4'ün koşullu kuralıdır, doğrusal öncü değildir.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_uluslararasi.md`, `notlar/denetim_uluslararasi.md`.*
