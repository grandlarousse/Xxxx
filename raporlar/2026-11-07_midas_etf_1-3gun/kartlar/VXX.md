# VXX — iPath S&P 500 VIX Short-Term Futures ETN

**TradingView:** `CBOE:VXX` · **Aile:** Volatilite (VIX) · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 215 | 16.6 | 393 | %-9.6 | 1.0 | 2018-01-18 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Uzun vol gerekiyorsa tek ETN (PTP değil, Barclays kredi riski var), en likit 1x araç. VIXY'nin kopyası ama ona tercih edilir. 1-3 günlük hiçbir long kural pozitif değil (koşulsuz -9,6 bp/gün); yalnız koruma amaçlı. **Ana ajan notu:** İşlem adayı değil; yalnız koruma (1-3 günlük hiçbir long kural pozitif değil).

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| VIX günlük log değişimi | `CBOE:VIX` | 0.91 | 0.42 |
| VVIX günlük log değişimi | `CBOE:VVIX` | 0.90 | 0.56 |
| SPY günlük getiri | `AMEX:SPY` | -0.84 | -3.72 |
| VIX/VIX3M oranı günlük değişimi | `CBOE:VIX/CBOE:VIX3M` | 0.82 | 0.85 |
| QQQ günlük getiri | `NASDAQ:QQQ` | -0.74 | -2.10 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| VIX vadelisi ön ay | `CBOE:VX1!` | ETF'lerin dayanağı (1. ve 2. ay karışımı). Neredeyse 24 saat işler; ETF kapalıyken açılış boşluğunu doğrudan gösterir. SVXY boşluğu ≈ -0,5 x VX karışımı değişimi. |
| VIX vadelisi 2. ay | `CBOE:VX2!` | Endeks ağırlığı ay içinde 1. aydan 2. aya kayar; vade sonuna doğru VX2! daha belirleyici olur. |
| S&P 500 E-mini vadelisi | `CME_MINI:ES1!` | 23 saat işler. Gece S&P düşüşü VIX vadelisini yükseltir (SVXY'nin SPY'ye betası ~2). |
| Nasdaq 100 E-mini vadelisi | `CME_MINI:NQ1!` | Teknoloji kaynaklı gece şoklarını gösterir. |
| USD/JPY | `FX_IDC:USDJPY` | Taşıma işlemi çözülmesi ve risk iştahı göstergesi (5 Ağustos 2024'te yenin sert değer kazanması vol sıçramasından önce geldi). Öncü olarak test edilmedi, yalnız izleme amaçlı. |

## 3. Takvim ve olay riskleri

Yaklaşan olaylar (ET; TR = ET+8 kış): CPI 10.11.2026 ve 10.12.2026 08:30 (TR 16:30, açılıştan önce); NFP 04.12.2026 08:30; FOMC 09.12.2026 14:00 (TR 22:00); VIX vade/uzlaşma 18.11.2026 ve 16.12.2026 (Çarşamba); aylık opsiyon vadesi 20.11.2026; triple witching 18.12.2026; 26.11.2026 kapalı, 27.11 ve 24.12 erken kapanış (13:00 ET, TR 21:00); 25.12 kapalı. Hafta sonu ve tatil boşlukları kısa vol için risklidir (3 günlük boşluk). Şu an VIX/VIX3M 1,04 (backwardation): kısa vol ürünlerinde 1-3 günlük dağılım normalin ~2 katı.

## 4. Notlar

Doğrulanmış gecikmeli öncü yok: genel taramada aile hedefleri için FDR'yi geçen 0. Ek 144 testte (VIX/VIX3M düzeyi ve değişimi, VIX9D/VIX, VIX gerilmesi, VVIX/VIX, SPY/QQQ/BTC getirileri, DGS10; kendi gecikmesi kontrollü, Newey-West, C0 ve O1 hizalaması) de 0. Eşzamanlı sürücüler öncü değildir. VIX 16:15 ET'de kapandığı için C0 hizalamasındaki VIX öncülüğü kısmen ileri bakıştır. En güçlü (geçmeyen) aday: VVIX/VIX oranı -> VXX ertesi gün (O1 h1 t=3,17; IS 2,05, OOS 2,72; 1 sd'de 22 bp, maliyetin 1,3 katı; p=0,0015 > FDR eşiği). VXX'in koşulsuz -9,6 bp/gün kaybı karşısında işlenebilir değil.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_volatilite.md`, `notlar/denetim_volatilite.md`.*
