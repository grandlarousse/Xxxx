# SBIT — ProShares UltraShort Bitcoin ETF

**TradingView:** `AMEX:SBIT` · **Aile:** Kripto · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 57 | 16,0 | 561 | %-20,3 | -2,0x | 2024-04-02 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Kısa BTC görüşü için −2x araç (yedek). Perşembe kuralı (S1 (çürütüldü)) çürütüldü; doğrulanmış strateji yok. **Ana ajan notu:** S1 (çürütüldü) çürütüldü; yalnız kısa BTC görüşü için araç.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| BTC/USD (16:00 ET getirisi; eşzamanlı) | `COINBASE:BTCUSD` | -0.99 | -2.01 |
| IBIT | `NASDAQ:IBIT` | -0.99 | -2.00 |
| Nasdaq-100 (QQQ) | `NASDAQ:QQQ` | -0.48 | -2.04 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Bitcoin spot (Coinbase) | `COINBASE:BTCUSD` | 7/24 işler. ETF kapalıyken (TR 00:00-17:30, kış) BTC'nin 16:00 ET'den sonraki hareketi ertesi açılış boşluğunu belirler: IBIT açılış boşluğu ≈ BTC 16:00→09:30 ET hareketi (R²=0,96, eğim 1,00; Pazartesi R²=0,98 = hafta sonu hareketi). Öncü değil, açılışı önceden gösteren izleme aracı. |
| CME Bitcoin vadeli (ön ay) | `CME:BTC1!` | CME Globex Pazar-Cuma (kış: TR 02:00 → ertesi gün 01:00, günlük 1 saat ara); hafta sonu kapalı → Pazartesi 'CME boşluğu'. Kurumsal akış/baz (vadeli primi) göstergesi. |
| Ethereum spot (Coinbase) | `COINBASE:ETHUSD` | 7/24; kripto risk iştahı (IBIT ile corr 0,92). |
| Nasdaq-100 E-mini vadeli | `CME_MINI:NQ1!` | ~23 saat işler; ABD hisse risk iştahı (IBIT-QQQ corr 0,49, beta 1,03). Makro haber (CPI/NFP TR 16:30) tepkisini açılış öncesi gösterir. |

## 3. Takvim ve olay riskleri

TR saatiyle (ABD kış saati): CPI 10 Kas 2026 Sal 16:30; aylık opsiyon vadesi 20 Kas Cum; Şükran Günü 26 Kas Per KAPALI (S1 (çürütüldü) işlemi yok), 27 Kas Cum erken kapanış 21:00; NFP 4 Ara Cum 16:30; FOMC 9 Ara Çar 22:00 (SEP); CPI 10 Ara Per 16:30 (S1 (çürütüldü) günü — CPI'lı Perşembeler çok oynak); triple witching 18 Ara Cum; 24 Ara Per erken kapanış 21:00; 25 Ara ve 1 Oca kapalı. Kripto 7/24 işler: hafta sonu/tatil hareketi Pazartesi (tatil ertesi) açılışında boşluk olarak gelir. CME BTC/ETH vadeli aylık vadesi ayın son Cuması (kural; takvim dosyalarında yok, doğrulanmadı).

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK. leadlag_sweep'te ailenin 765 hedef×öncü satırında (3.060 test) global ve aile içi BH-FDR geçen 0. Ek testler (BTC/ETH 16:00 ET → hedef t+1/t+3, kendi gecikmesi kontrollü; 'yetişme' u=β60·r_BTC−r_T kendi getirisi kontrollü) hiçbiri |t|≥2 değil. Yetişme kuralları (u≥+2σ → long) maliyetli backtestte anlamsız. BTC gece hareketi → IBIT gün içi devamı: z≥+1'de IBIT O1 net +29 bp (t=1,40), z≤−1'de SBIT +48 bp (t=1,09) — anlamsız. Gün içi BTC ile korelasyon ~1 olduğundan 'sürücüler' eşzamanlıdır, öncü değildir. Ters ürün: dayanak düşüşünde kazanır; S1 (çürütüldü) aracı (SBIT) / düşük riskli alternatif (BITI).

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_kripto.md`, `notlar/denetim_kripto.md`.*
