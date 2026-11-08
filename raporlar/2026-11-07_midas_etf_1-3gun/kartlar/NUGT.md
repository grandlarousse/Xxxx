# NUGT — Direxion Daily Gold Miners Index Bull 2X ETF

**TradingView:** `AMEX:NUGT` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 110 | 16,0 | 635 | %-25,2 | 2,0x | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** 2x GDX (1940 Kanunu, PTP değil; Midas'ta bulunurluğu doğrulanmadı). 2020-Q2'ye kadar 3x idi. B3a'nın kaldıraçlı uygulaması; 2x dönemde 3 günlük oynaklık kaybı ~-5 bp (küçük), ama maxDD ve tek işlem kaybı ~2 kat.

*Dayanak / ana araç kartı: `kartlar/GDX.md` (sürücüler ve gerçek zamanlı izleme listesi orada daha ayrıntılı).*

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt ya da yalnız filtre — tek başına işlem gerekçesi değil)

#### B3a — Ay sonu (turn-of-month) - altın madencileri (GDX)  
*İzlemede — zayıf kanıt · güven: dusuk · aile kimliği: `metal_madenci_S1`*  
*Bu ETF'nin rolü: 2x araç (Midas doğrulanmadı)*

- **Sinyal (t kapanışında):** Takvim kuralı, gösterge yok: NYSE'de ayın SON işlem günü AMEX:GDX kapanışta alınır, yeni ayın 3. işlem gününün kapanışında satılır (3 işlem günü). Sinyal ve işlem aynı ETF (AMEX:GDX); kaldıraçlı alternatif AMEX:NUGT (aynı tarihler). Filtre/stop yok. Tatiller NYSE takvimine göre (sonraki sinyaller: 30.11.2026 Pzt -> çıkış 03.12.2026; 31.12.2026 Per -> çıkış 06.01.2027; 29.01.2027 Cum -> çıkış 03.02.2027).
- **Giriş:** C0: ayın son işlem günü kapanıştan hemen önce; kış saatinde (1 Kas 2026 - 14 Mar 2027) TR ~23:45-23:59, yaz saatinde TR ~22:45-22:59. Midas'ta MOC/LOC yok: son dakikalarda piyasa emri ya da son fiyatın 1-2 sent üstüne limit emir. Kaçırılırsa O1 (yeni ayın ilk açılışı TR 17:30 kış/16:30 yaz) zayıf da olsa pozitif (net 44,5 bp, t 1,23).
- **Tutuş / çıkış:** 3 işlem günü (girişten sonraki 3. kapanış). — Yeni ayın 3. işlem günü kapanışından hemen önce (TR ~23:45-23:59 kış / 22:45-22:59 yaz) sat; erken çıkış ve stop yok.
- **İşlem aracı:** GDX, NUGT (kaldıraçlı, Midas'ta doğrulanmadı) (sinyal: Takvim (NYSE); işlem AMEX:GDX)
- **Geçmiş (ajan):** n=111, net 84.5 bp/işlem (brüt 97.7), kazanma %56, t=2.20, IS 82.3 / OOS 86.5 bp, yılların %90'i pozitif, en kötü işlem -873 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** C0: net 161 bp (t 1,9, n=117) · O1: net 105 bp (t 1,4, n=117) · C1: net 94 bp (t 1,1, n=117); 1.000 $ pozisyonda ana mod net 143 bp (t 1,7)
- **Denetçi düzeltmesi:** Sayılar doğru. Ek: en iyi 5 hariç 40,2 bp/t 1,17; 2020 hariç 61,7/t 1,58; 2024-26 hariç 53,9/t 1,29; permütasyon p 0,025; 1.000$ 66,5/t 1,74.
- **Denetçi kural düzeltmesi:** Kural doğru tanımlı; B3b ile aynı anda açılmamalı (aynı bahis); 'büyük ölçüde kapanışa bağımlı' etiketi korunmalı.
- **Denetim:** Birebir: n=111, brüt 97,7, net 84,5 bp, t 2,20, IS 82,3 (t 1,75) / OOS 86,5 (t 1,44); tarih/getiriler aynı. Veride NYSE işlem günlerinden eksik/fazla gün yok, ay sonu tespiti doğru; takvim önceden bilinir, ileriye bakma yok. Sağlamlık: Son gün girişinde tutuş platosu (h1..h6 t 1,8-2,6, hep pozitif); GDXJ/RING/XME/COPX/URA aynı yönde (tek küme, bağımsız değil); baz metallerde yok; TOM literatürüyle uyumlu.
- **Denetçinin uyarıları:** FDR geçmez (p1 0,015); en iyi 5 işlem hariç 40 bp/t 1,17; 2020 hariç 62/t 1,58; 2024-26 hariç 54/t 1,29; permütasyon p=0,025 (yıl tabakalı 0,028); 1.000$'da 66,5 bp/t 1,74; +10 bp kaymada t 1,94; O1 h3 t 1,23, C1 h3 t 1,36; etkinin yarısı ilk gece (C0 h1 53 bp/t 2,40) -> büyük ölçüde kapanışa bağımlı. Sondan 2./3./4. gün girişleri h1-h3'te negatif (ayın son günü GDX -18 bp): etki yalnız yeni ayın ilk günleri. Madenci havuzu t 1,83 (IS 1,59/OOS 1,17); NUGT 2x döneminde t 1,90.
- **Giriş zamanı sağlamlığı:** C0: n=111, brüt 97.7 bp, net 84.5 bp, t 2.20; O1: n=111, brüt 57.7 bp, net 44.5 bp, t 1.23; C1: n=111, brüt 64.7 bp, net 51.6 bp, t 1.36
- **Maliyet duyarlılığı:** 1.000$: net 66.5 bp | 2.500$: net 84.5 bp | 10.000$: net 93.5 bp (2.500$ maliyeti 13.1 bp)
- **Not:** Eşik ölçütlerini tek ETF düzeyinde geçer (net>0, t≥2, IS ve OOS>0, yılların %90'ı pozitif, n=111, O1/C1 brüt>0) ama FDR'yi geçmez ve aile havuzu t<2,5. Etkinin yaklaşık yarısı ay başının ilk gecesinde (C0 h1 brüt 66 bp vs O1 h1 26 bp) -> 'büyük ölçüde kapanışa bağımlı'. Getiri boğa yıllarında yoğun (2020: 273 bp, 2025: 247, 2026: 189/işlem); yıl ortalaması çıkarılmış kenar 72,5 bp (t 1,92); en iyi yıl hariç t 1,58; 2020/2025/2026 hariç net 16 bp (t 0,42). 2023'te -74 bp. 30.01.2026 şoku hariç net 81 bp. Hisse piyasalarında bilinen ay dönümü etkisiyle (Lakonishok-Smidt 1988, McConnell-Xu 2008) uyumlu ama bu örneklemde SPY'de zayıf. NUGT ile: net 188 bp, t 2,19, maxDD -%37, en kötü işlem -%17,6. (IS t=1.75, OOS t=1.44)
- Betik: `python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_metal_madenci/t5_adaylar.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| GDX (eşzamanlı sürücü, öncü değil) | `AMEX:GDX` | 1.00 | 1.99 |
| GLD (eşzamanlı sürücü, öncü değil) | `AMEX:GLD` | 0.87 | 3.04 |
| SLV (eşzamanlı sürücü, öncü değil) | `AMEX:SLV` | 0.82 | 1.27 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| GLD | `AMEX:GLD` | yetişme (beta60*r_L(t) - r_T(t) -> r_T(t+1..t+1)) | 1 gün | -17.3 bp / 1 sd öncü hareketi (h=1);  | -0.7 (-0.5/-0.7) | yok | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| COMEX altın vadeli | `COMEX:GC1!` | Madencilerin ana sürücüsü (GDX-GLD 0,86, beta 1,53); gece hareketi madenci açılışına ~1,5x yansır. |
| COMEX gümüş vadeli | `COMEX:SI1!` | İkincil sürücü (GDX-SLV 0,81). |
| S&P 500 e-mini | `CME_MINI:ES1!` | Madenciler hisse olduğu için genel risk iştahı; açılış öncesi yön. |

## 3. Takvim ve olay riskleri

FOMC 09.12.2026 14:00 ET (TR 22:00; örneklemde FOMC sonrası altın zayıf, anlamsız); CPI 10.11 ve 10.12.2026, NFP 04.12.2026 08:30 ET (TR 16:30, açılıştan 1 saat önce); COMEX teminat değişiklikleri (30.01.2026 gümüş şoku); Çin tatilleri Asya seansını inceltir; ay sonu 30.11.2026 (B3a/B3b). Ek: madenci bilanço dönemleri (Şub, Nis-May, Tem-Ağu, Eki-Kas).

## 4. Notlar

2x GDX; sinyaller GDX'ten alınır. Doğrulanmış gecikmeli öncü yok.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
