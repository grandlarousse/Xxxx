# EWZ — iShares MSCI Brazil ETF

**TradingView:** `AMEX:EWZ` · **Aile:** Uluslararası / ülke · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 977 | 15.1 | 220 | %-19.8 | 1.0 | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Likit (977 mn $, 15 bp), yüksek oynaklık (222 bp). Doğrulanmış strateji/öncü yok (S1 plasebo grubunda; USO öncülüğü yok).

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| EEM | `AMEX:EEM` | 0.41 | 0.56 |
| EWJ | `AMEX:EWJ` | 0.38 | 0.62 |
| IWM | `AMEX:IWM` | 0.35 | 0.69 |
| CPER | `AMEX:CPER` | 0.35 | 0.44 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Ibovespa | `BMFBOVESPA:IBOV` | ABD ile büyük ölçüde eşzamanlı |
| USD/BRL | `FX_IDC:USDBRL` | kur getirinin büyük kısmı |
| Brent vadelisi | `ICEEUR:BRN1!` | Petrobras ağırlığı |

## 3. Takvim ve olay riskleri

Brezilya: Copom kararları, Karnaval (Şub 2027), BRL oynaklığı.

## 4. Notlar

Doğrulanmış (doğrusal) gecikmeli öncü YOK: aile içi BH-FDR geçen çift yok. En güçlü aday (FDR'siz): GDX h1 t=1.43 (IS 1.56/OOS -0.48), h3 t=2.33. Sürücüler eşzamanlıdır, öncü değildir.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_uluslararasi.md`, `notlar/denetim_uluslararasi.md`.*
