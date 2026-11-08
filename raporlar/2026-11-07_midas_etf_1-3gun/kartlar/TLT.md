# TLT — iShares 20+ Year Treasury Bond ETF

**TradingView:** `NASDAQ:TLT` · **Aile:** Tahvil ve döviz · **İzleme kararı:** kabul  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 2,645 | 13.2 | 60 | %-1.9 | 1.0 | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** S1'in dayanağı ve faiz izleme aracı; ailenin en likit/ucuz uzun vade ETF'i (2,6 mlr $/gün, 13 bp, maliyet/oynaklık 0,22). Long yönde eşiği geçen strateji YOK (ay sonu net 14 bp t=1,2; FOMC D-1 net 11 bp t=1,1; RSI2/IBS dönüşü net<0). Risk kuralı: 10Y ihale öncesi pencerede (A-3→A-1) TLT long taşımamak (brüt −41 bp, t=−3,7). **Ana ajan notu:** Uzun vade faiz izleme aracı ve TMV/TBT/TMF dayanağı (kural yok).

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| ABD 30 yıllık getiri değişimi (yüzde puan; beta = getiri/1 puan) — eşzamanlı, öncü değil | `TVC:US30Y` | -0.97 | -0.15 |
| IEF (7-10 yıl) — eşzamanlı, öncü değil | `NASDAQ:IEF` | 0.91 | 1.74 |
| ABD 10 yıllık getiri değişimi (yüzde puan) — eşzamanlı, öncü değil | `TVC:US10Y` | -0.91 | -0.12 |
| LQD (yatırım yapılabilir kredi) — eşzamanlı, öncü değil | `AMEX:LQD` | 0.90 | 1.53 |
| 10 yıllık reel getiri (TIPS) değişimi (yüzde puan; FRED günlük, gecikmeli yayımlanır) — eşzamanlı, öncü değil | `FRED:DFII10` | -0.80 | -0.13 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| 10Y Hazine ihale takvimi: A-3 kapanışı → A-1 kapanışı penceresi | yok (takvim: TreasuryDirect 'Upcoming Auctions' / TradingView Ekonomik Takvim '10-Year Note Auction') | takvim olayı (önceden bilinir; gecikmeli öngörü) | t+1..t+2 (A-2, A-1) | TLT brüt -41 bp / pencere (t -3.72); TLT −41 bp | -3.7 (—/—) | long yönde işlenmez (açığa satış yok): risk kuralı = pencerede long taşıma; kısa yön TMV/TBT ile (S1) | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Ultra T-Bond vadeli (CBOT) | `CBOT:UB1!` | TLT'nin süresine en yakın vadeli; CME Globex Pazar-Cuma neredeyse 23 saat (kış TR 02:00 → ertesi gün 01:00, 01:00-02:00 ara; yaz saatinde bir saat erken). TR 12:00-17:30 arasında TLT/TMV açılış boşluğunu önceden gösterir — öncü değil, izleme aracı. |
| 30 yıllık T-Bond vadeli (CBOT) | `CBOT:ZB1!` | UB1! ile aynı saatler; daha likit. |
| 10 yıllık T-Note vadeli (CBOT) | `CBOT:ZN1!` | Faiz piyasasının en likit vadelisi; ABD veri açıklamaları (TR 16:30) anında tepki. |
| ABD 30 yıllık getiri | `TVC:US30Y` | TLT ile eşzamanlı korelasyon −0,97; Asya/Avrupa saatlerinde de kotasyon. |
| ABD 10 yıllık getiri | `TVC:US10Y` | Genel faiz yönü; CPI/NFP (TR 16:30) tepkisi açılıştan önce görülür. |
| Almanya 10 yıllık getiri | `TVC:DE10Y` | Avrupa seansında (TR ~10:00-19:00) küresel faiz hareketi; ABD açılışından önce. |
| Japonya 10 yıllık getiri | `TVC:JP10Y` | Asya seansında (TR ~03:00-09:00) küresel uzun vade baskısı (BoJ). |
| S&P 500 E-mini vadeli | `CME_MINI:ES1!` | Risk iştahı; hisse-tahvil korelasyonu rejime göre değişiyor (2022'de pozitif). |

## 3. Takvim ve olay riskleri

10 Kas 2026 Sal: 10Y ihale (13:00 ET=TR 21:00) + CPI (TR 16:30) aynı gün; 11 Kas Çar Veterans Day (tahvil nakit piyasası kapalı, NYSE açık: ince işlem); 12 Kas Per 30Y ihale; 26 Kas NYSE kapalı, 27 Kas erken kapanış 13:00 ET (TR 21:00); 4 Ara Cum NFP (8 Ara ihale penceresinin içinde: tarihsel olarak etki daha büyük ama oynak); 8 Ara Sal 10Y yeniden ihraç; 9 Ara Çar FOMC (SEP; TR 22:00); 10 Ara Per 30Y + CPI; 24 Ara erken kapanış, 25 Ara kapalı. TMV/TBT çeyreklik dağıtım ex-date'leri ~Mar/Haz/Eyl/Ara 20-25'i (S1 penceresine denk gelmez).

## 4. Notlar

Fiyat/faiz/kredi/risk öncüleri arasında doğrulanmış gecikmeli öncü YOK: TLT için 18-19 aday × h∈{1,3} (kendi gecikmesi kontrollü, NW) içinde BH-FDR (224 testlik izleme seti) geçen 0; en güçlüsü IEF (h3) t=2.61, +27 bp/sd. leadlag_sweep'te de bu hedef için FDR'li öncü yok. Tek gecikmeli öngörücü TAKVİM: 10Y ihale öncesi pencere (S1). Eşzamanlı sürücüler (30Y/10Y getiri, IEF, LQD) öncü değildir.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_tahvil_doviz.md`, `notlar/denetim_tahvil_doviz.md`.*
