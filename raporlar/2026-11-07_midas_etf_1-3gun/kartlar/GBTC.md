# GBTC — Grayscale Bitcoin Trust (BTC)

**TradingView:** `AMEX:GBTC` · **Aile:** Kripto · **İzleme kararı:** kabul  
**Midas:** sembol sayfası var (getmidas.com; resmî ürün listesi yok)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 136 | 16,0 | 281 | %-13,2 | 1,0x | 2024-01-11 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** IBIT kopyası (corr 0,9992); 136 mn$/gün, makas ~4 bp (16 bp). Midas'ta sembol sayfası DOĞRULANMIŞ tek spot BTC ETF'si → IBIT/FBTC yoksa birinci seçenek. Yüksek yönetim ücreti 1-3 günde önemsiz. **Ana ajan notu:** Midas'ta sembol sayfası doğrulanmış spot BTC ETF'i; IBIT ile eş birincil.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt ya da yalnız filtre — tek başına işlem gerekçesi değil)

#### F — FİLTRE (strateji değil) — BTC trend filtresi (kapanış > SMA10 > SMA50) → IBIT 3 gün long  
*Filtre — strateji değil · güven: dusuk · aile kimliği: `kripto_S2`*  
*Bu ETF'nin rolü: filtre*

- **Sinyal (t kapanışında):** TradingView günlük grafik NASDAQ:IBIT (ETH için NASDAQ:ETHA kendi grafiği). SİNYAL (t kapanışı): kapanış > SMA(10) VE SMA(10) > SMA(50). İŞLEM: NASDAQ:IBIT long (Midas'ta IBIT yoksa AMEX:GBTC — sembol sayfası doğrulanmış — veya CBOE:FBTC). 3 işlem günü tut; pozisyondayken yeni sinyal yok sayılır, çıkış günü koşul sürüyorsa yeniden girilebilir. COINBASE:BTCUSD günlük mumunu sinyal için KULLANMA (00:00 UTC = TR 03:00'te kapanır, ABD kapanışında bilinmez); BTC ile hesaplanacaksa 16:00 ET (kış TR 00:00) anlık fiyatı kullan. Pine: c=close; sig = c > ta.sma(c,10) and ta.sma(c,10) > ta.sma(c,50)
- **Giriş:** C0: t günü kapanıştan 5-10 dk önce (kış TR ~23:50, yaz ~22:50) koşul sağlanıyorsa piyasa/agresif limit alış; alternatif: kapanış sonrası after-hours (kış TR 00:00-04:00, yaz 23:00-03:00) yalnız limit emir. O1 (t+1 açılış TR 17:30) ve C1 (t+1 kapanış) dayanakta pozitif, ETF döneminde zayıf.
- **Tutuş / çıkış:** 3 işlem günü — Girişten 3 işlem günü sonra kapanıştan 5-10 dk önce (kış TR ~23:50, yaz ~22:50) sat. Erken çıkış/stop yok (test edilmedi).
- **İşlem aracı:** IBIT, GBTC, FBTC, ETHA (sinyal: IBIT (kendi günlük kapanışı) veya BTC 16:00 ET fiyatı; ETH için ETHA)
- **Geçmiş (ajan):** n=317, net 152.8 bp/işlem (brüt 167.1), kazanma %54, t=3.42, IS 225.0 / OOS 58.0 bp, yılların %70'i pozitif, en kötü işlem -2498 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** C0: net 30 bp (t 0,6, n=75) · O1: net 36 bp (t 0,7, n=75) · C1: net -42 bp (t -0,6, n=59) [bu ETF için ayrı hesap yok; ana araç IBIT rakamları]
- **Denetçi düzeltmesi:** BTC_D C0 h3: n=320, net 154,8 bp, t=3,50; IS 227 (t 3,30), OOS 58 (t 1,26). Permütasyon p: tüm 0,0125 / IS 0,034 / OOS 0,16. 2017 hariç 92 bp (t 2,07). IBIT kendi sinyali C0 19 bp (t 0,38), O1 30, C1 -26. BTC 16:00 ET 2023-08+ C0 65 bp (t 1,34).
- **Denetçi kural düzeltmesi:** Kural aynı kalabilir (IBIT kendi günlük kapanışı ile c>SMA10>SMA50 -> 3 gün). Ancak 'aday strateji' değil, yalnız rejim filtresi olarak işaretlenmeli: 2024+ IBIT verisinde kenar t < 1.
- **Denetim:** Bağımsız motorla yeniden üretildi. BTC_D serisi ajanınkiyle aynı (2.513 ortak gün, fark 0). Sinyal c>SMA10>SMA50, C0 h=3, IBIT maliyeti 14,33 bp. Sonuç: n=320, brüt 169,1, net 154,8 bp, t=3,50, IS 227,3 (t 3,30) / OOS 58,0 (t 1,26), yıl+ 0,70, maxDD -%57,7, en kötü -2.498 bp. Ajan: n=317, net 152,8, t=3,42; fark yalnız ısınma penceresinden (ajan ilk 60 günü, ben ilk 50 günü atladım). C1 net 141,9 (OOS 26, t 0,51). İleri bakış yok: BTC_D'de sinyal ve giriş aynı 00:00 UTC kapanışında; rolling pencereler t'yi içeriyor ve shift gerekmiyor; çıkış t+3 kapanışı; işlemler çakışmıyor; maliyet bir kez düşülüyor. En iyi 5 işlem (04.12.2017 +4.935 bp, 09.05.2019, 09.08.2017, 31.12.2020, 20.06.2019) gerçek BTC rallileri ve net toplamın %32'si. IBIT kendi grafiği C0 n=78, net 19,3 bp (t 0,38); ajan n=75, 29,7 bp. Sağlamlık: Biçimsel eşiği yalnız dayanakta (BTC_D, 00:00 UTC) geçiyor: t≥2, IS ve OOS > 0, yılların %70'i pozitif, C1 brüt kenarı > 0. 2020 hariç 148 (t 3,09); 2022 hariç 165 (t 3,71); ikisi birden hariç 159 (t 3,32). Tutuş komşuluğu h1/h2/h5: OOS 7 / 25 / 92 bp, hepsinde t < 1,3. Maliyet: 1.000$ 137 (OOS 40) | 2.500$ 155 (OOS 58) | 10.000$ 164 (OOS 67). Sonuç: 'trend varken BTC long' bir beta zamanlaması. 2022 sonrasında ve ETF'nin kendisinde anlamlı değil. Strateji olarak değil, rejim filtresi olarak kullanılabilir (trend yokken long açmamak).
- **Denetçinin uyarıları:** (1) Kenarın çoğu BTC drift'i ve 2017: rastgele giriş permütasyonunda (aynı n, aynı 3 gün tutuş, 10.000 tekrar) tüm dönem p=0,0125, IS p=0,034, OOS p=0,16. OOS drift üstü kenar 43,7 bp (t≈0,95). 2017 hariç tüm dönem 92 bp (t 2,07), IS 130 bp (t 1,65). (2) Uygulanacak araçta kanıt yok: IBIT kendi sinyali C0 19 (t 0,38) / O1 30 / C1 -26 bp; IBIT'e BTC 16:00 ET sinyali C0 44 / O1 17 / C1 0,6 bp; GBTC 13 bp. Birebir zamanlı BTC 16:00 ET 2023-08+ C0 65 bp (t 1,34); aynı dönemde 00:00 UTC serisi 89 bp, yani 3-4 saatlik kayma sonucu biraz iyileştiriyor. (3) FDR: ajanın eşiğinde (p<=0,00047) geçmiyor (p=0,0007); Bonferroni de geçmiyor. (4) Komşu parametreler plato gibi görünüyor (36 kombinasyonun 35'inde OOS net > 0) ama OOS t'lerin hepsi < 2 (-0,45..1,89). IS'te en iyi kombinasyon (5/30) OOS'ta 24 bp. (5) 1.000$'da OOS 40 bp (t 0,87). (6) Ayı yıllarında kaybediyor (2018 -444, 2022 -277 bp/işlem) ve hafta sonu boşluk riski taşıyor. ETH versiyonu: ETH_D OOS 30 bp (t 0,48), ETHA kendi C1 -14 bp.
- **Giriş zamanı sağlamlığı:** BTC_D 2016-11..2026-11: C0 net 153 (t=3.42), C1 net 135 (t=2.75; IS 220 / OOS 26); BTC 16:00 ET 2023-08+: C0 67 (t=1.36), O1 44, C1 49; IBIT kendi grafiği: C0 30 (t=0.57), O1 36, C1 −42; IBIT←BTC 16:00 ET: C0 44, O1 17, C1 1 bp (net).
- **Maliyet duyarlılığı:** Dayanak BTC_D (IBIT maliyeti): 1.000$ 135 | 2.500$ 153 | 10.000$ 162 bp; IBIT 2024+ (BTC 16:00 ET sinyali): 1.000$ 26 | 2.500$ 44 | 10.000$ 53 bp
- **Not:** Aşağıdaki 'Geçmiş (ajan)' rakamı dayanak BTC'nin 00:00 UTC serisine (2016+) aittir; ETF'te geçerli değildir (son kontrol: IBIT C0 +30 bp, t 0,6). Yalnız 'BTC trendi yukarı mı' filtresi olarak kullanın. Biçimsel eşik dayanak uzun testinde geçiyor (t≥2, IS ve OOS>0, yılların %70'i +, n=317, C1'de de pozitif); ETF döneminde zayıf. Komşu parametreler (SMA 5/50, 10/30, 20/50, 10/100) BTC_D'de benzer (t 3,4-4,2; OOS 41-58 bp) — parametre seçimine duyarlı değil. Ancak: (1) Kazancın çoğu IS boğa piyasası (IS net 225 / kenar 107 bp; OOS net 58 bp t=1,26, kenar 44 bp). (2) Ayı yıllarında kaybeder (yıllık ort. 2018 −444, 2022 −277 bp/işlem). (3) IBIT'te (2024-01..2026-11) C0 +30-44 bp, t<1; C1 ~0/negatif. (4) BTC_D'de sinyal 00:00 UTC kapanışından (16:00 ET'den 3-4 saat sonra) — kendi içinde ileri bakışsız ama ETF zamanlamasıyla birebir değil; birebir 16:00 ET serisi yalnız 3,4 yıl. (5) Kenarın bir kısmı BTC'nin pozitif drift'i: strateji 'trend varken long BTC' — ayı piyasasında da sinyal üretir. (6) Kaldıraçlı araç (BITX) kullanılırsa 2×IBIT'e göre takip kaybı ~−12 bp/gün (3 günde −37 bp). Yılda ~30 işlem; pozisyonda olma oranı ~%40. Hafta sonu riskini (Cuma→Pazartesi boşluğu) taşır.
- Betik: `python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_kripto/05_adaylar.py  (işlemler: /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/sonuclar/aile_kripto/aday_kripto_S2_islemler.csv)`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| BTC/USD (16:00 ET getirisi; eşzamanlı) | `COINBASE:BTCUSD` | 1.00 | 1.00 |
| IBIT | `NASDAQ:IBIT` | 1.00 | 1.00 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Bitcoin spot (Coinbase) | `COINBASE:BTCUSD` | 7/24 işler. ETF kapalıyken (TR 00:00-17:30, kış) BTC'nin 16:00 ET'den sonraki hareketi ertesi açılış boşluğunu belirler: IBIT açılış boşluğu ≈ BTC 16:00→09:30 ET hareketi (R²=0,96, eğim 1,00; Pazartesi R²=0,98 = hafta sonu hareketi). Öncü değil, açılışı önceden gösteren izleme aracı. |
| CME Bitcoin vadeli (ön ay) | `CME:BTC1!` | CME Globex Pazar-Cuma (kış: TR 02:00 → ertesi gün 01:00, günlük 1 saat ara); hafta sonu kapalı → Pazartesi 'CME boşluğu'. Kurumsal akış/baz (vadeli primi) göstergesi. |

## 3. Takvim ve olay riskleri

Bkz. IBIT girdisi: CPI 10 Kas 16:30; 26 Kas kapalı; NFP 4 Ara; FOMC 9 Ara 22:00; CPI 10 Ara (Per) 16:30; 24 Ara erken kapanış 21:00 (TR saati).

## 4. Notlar

Doğrulanmış gecikmeli öncü YOK (sweep FDR 0; ek testler |t|<2). Sürücüler eşzamanlıdır; ayrıntı IBIT/ETHA girdisinde. IBIT kopyası (corr ~0,999).

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_kripto.md`, `notlar/denetim_kripto.md`.*
