# SVXY — ProShares Short VIX Short Term Futures ETF

**TradingView:** `CBOE:SVXY` · **Aile:** Volatilite (VIX) · **İzleme kararı:** kabul  
**Midas:** doğrulanamadı · ⚠ PTP/K-1 ürünü: satışta %10 brüt kesinti (1446(f)) riski

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 85 | 16.0 | 202 | %-15.4 | -0.5 | 2018-09-18 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** S1'in işlem aracı. -0,5x yapıyla kısa vol ürünleri içinde kuyruk riski en düşük olan; likit; maliyet/vol 0,079. PTP/K-1 (ProShares Trust II) %10 kesinti riski var, önce Midas teyidi. 1 günde -%21,4 (05.08.2024), 3 günde -%33,8 görüldü. **Ana ajan notu:** Koşullu: Midas'ta sembol ve PTP %10 kesintisi yoksa; aksi halde yalnız sinyal kaynağı.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt — tek başına işlem gerekçesi değil)

#### SVXY 2 günlük RSI dibi (200 günlük trend üstünde) - kısa vol geri dönüşü  
*İzlemede — zayıf kanıt · güven: dusuk · id: `volatilite_S1`*

- **Sinyal (t kapanışında):** TradingView günlük grafik CBOE:SVXY. Gösterge 1: RSI, uzunluk 2, kaynak kapanış (standart Wilder RSI). Gösterge 2: SMA, uzunluk 200, kaynak kapanış. Sinyal günü t: RSI(2) < 10 VE SVXY kapanışı > SMA(200) -> SVXY al (sinyal de işlem de SVXY verisinde; agresif varyantta aynı SVXY sinyaliyle CBOE:SVIX alınır). Tutuş 2 işlem günü, t+2 kapanışında sat. Pozisyondayken yeni sinyal yok sayılır. Stop yok (backtest stopsuz).
- **Giriş:** C0 (ana): sinyal günü kapanıştan hemen önce RSI(2)'yi canlı fiyatla kontrol edip emir ver, TR kış 23:50-23:59 (yaz 22:50-22:59). Midas'ta MOC/LOC yok; normal seansta limit ya da piyasa emri kullanılır. Alternatif O1: ertesi gün açılışta al, TR kış 17:30 (yaz 16:30); açılış öncesi limit emir verilebilir (pre-market TR kış 12:00-17:30).
- **Tutuş / çıkış:** 2 işlem günü (C0: t kapanışı -> t+2 kapanışı; O1: t+1 açılışı -> t+2 kapanışı). 3 gün tutmak daha kötü (C0 h3 +106 bp, t=1,59). — t+2 günü kapanıştan hemen önce sat (TR kış 23:50-23:59, yaz 22:50-22:59). Bir gün gecikmeli giriş (C1) yapılmamalı: kenar ilk 1-2 günde.
- **İşlem aracı:** SVXY, SVIX (sinyal: SVXY)
- **Geçmiş (ajan):** n=59, net 157.3 bp/işlem (brüt 173.3), kazanma %71, t=3.16, IS 143.6 / OOS 163.8 bp, yılların %62'i pozitif, en kötü işlem -1375 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500$):** C0: net 157 bp (t 3.2, n=59) · O1: net 108 bp (t 2.5, n=59) · C1: net -28 bp (t -0.5, n=55); 1.000$ pozisyonda ana mod net 139 bp (t 2.8)
- **Denetçi düzeltmesi:** Ajanın sayıları doğru; düzeltme yorum ve FDR'de: BH-FDR tek yönlü: GEÇMEZ (yalnız SVIX C0 h1 geçer); Bonferroni: geçmez. 2021 hariç: n=47, net 103 bp, t=1,91, IS -241 bp. En iyi 5 çıkarılınca C0 h2 99 bp (t 2,13), O1 h2 57 bp (t 1,43). Vekil 2010-2018: n=76, 0 bp; 2015-2018 -81 bp. Hisse betası ayrışması: SPY beta 2,28, R² 0,84, alfa 48 bp brüt (t 2,37). Şubat 2018: vekilde 02.02.2018 RSI2=12,4 (sinyale 2,4 puan uzak), 'pozisyon yok' değil 'veri yok / kıl payı'. Cuma sinyalleri (hafta sonu taşıyan) n=17, +84 bp, en kötü -1.375.
- **Denetçi kural düzeltmesi:** Kural aynı kalır (RSI2(SVXY)<10 ve SVXY>SMA200, C0 ya da O1 giriş, t+2 kapanışta çık; C1 yok). Ek: (a) SVXY yalnız Midas'ta bulunurluk ve PTP kesintisi olmadığı teyit edilirse; aksi halde aynı SVXY sinyaliyle QQQ (C0 h2 +73 bp t 2,84; O1 +46 t 2,23) ya da QLD (C0 +154 t 3,01; O1 +103 t 2,51) — aynı olaylar, IS zayıf, bağımsız kanıt değil. (b) SVIX kullanılmamalı. (c) Pozisyon küçük; tek işlemde -%45-50 (Volmageddon tipi) senaryosu kabul edilerek boyutlandır. Güven: düşük (ajanla aynı); 'dogrulandi' değil.
- **Denetim:** Bağımsız motorla (lib.trades/evaluate/rsi kullanılmadan, Wilder RSI, kendi çakışmasız döngü, maliyet tarama.csv makası + 12 bp) birebir: SVXY C0 h2 n=59, brüt 173,3, net 157,3 bp, t=3,16, IS 143,6 (n=19, t=1,15), OOS 163,8 (t=3,64), kazanma 0,71, PF 2,88, maxDD -%14,5, en kötü -1.375, yıl+ 0,625. O1 h2 107,7 (t 2,53); C1 h2 -27,7 (t -0,51). 59/59 işlem ajanla aynı (brüt fark <1e-12). İleriye bakış yok: sinyal yalnız SVXY t kapanışı (VIX/BTC/Hazine kullanılmıyor), giriş/çıkış günleri doğru, çakışma yok, maliyet bir kez düşülüyor. En iyi 5 işlem (12.05.2021, 16.10.2025, 19.07.2021, 29.01.2021, 20.01.2026) veri_kalitesi/veri_duzeltmeleri'nde yok; 3'ü 2021'de. Sağlamlık: Lehte: rastgele giriş permütasyonu (aynı n, aynı tutuş, çakışmasız, 2.000-3.000 tekrar) C0 h2 p=0,0005 (tüm günler), 0,0005 (SMA200 üstü), 0,0003 (VIX ±%10 eşlemeli), 0,0003 (VIX+2 günlük düşüş eşlemeli); döngüsel kaydırma p=0,001; O1 h2 p 0,0003-0,0057 (tek test, seçim yanlılığı düzeltilmemiş). Gerçek SVXY'de parametre platosu: eşik 5-12,5 × SMA 150-250 C0 h2 92-193 bp (t 1,5-3,2); eşik ≥15 ve filtresiz ≈0; RSI(3) de pozitif. 2020 hariç 184 (t 4,15), 2022 hariç 172 (3,54), ikisi hariç 200 (4,73); en iyi 5 çıkarılınca 99 (t 2,13, IS +14). Maliyet: 1.000$ 139 bp (t 2,80), 2.500$ 157 (3,16), 10.000$ 166 (3,34); O1 90/108/117. C0 kapanış öncesi fiyatla (son ~20 dk gürültüsü, 500 tekrar) net 146 bp (p5 114), t 2,98 (p5 2,23); sinyallerin 25/59'u RSI 7-10 arasında. Ayrışma: gece +56, t+1 gün içi +42, t+2 +38 bp (koşulsuz +8/-2/+6): kapanışa bağımlı değil ama gecikmeli girişte (C1) kenar yok. Aile içi: SVIX C0 h2 +354 (t 4,50, n=39, yalnız 2022+), aynı dönemde SVXY +185 (t 4,59) — bağımsız kanıt değil. Yıllar (işlem başı net bp): 2019 -162, 2020 -347, 2021 +368, 2022 -681, 2023 +156, 2024 +124, 2025 +287, 2026 +251.
- **Denetçinin uyarıları:** (1) FDR geçişi yapay: iki yönlü BH'de geçen 113 testin 105'i uzun vol ürünlerinin yapısal kaybı (negatif); pozitif 8 testin hepsi yanlış olsa bile FDR %7<%10. Tek yönlü BH (H1: net>0) ile yalnız 1 test geçer (SVIX C0 h1, yalnız 2022+); SVXY C0 h2 (tek yönlü p=0,00126) GEÇMEZ; Bonferroni (3,3e-5) geçmez; genel kütüphane 92.664 testte tek yönlü BH 0 geçen. (2) IS kanıtı 2021'e bağlı: IS yılları 2019 -162, 2020 -347, 2021 +368 bp/işlem; 2021 hariç IS -241 bp, tüm dönem t=1,91. (3) Uzun dönem vekilde 2010-2014 +37 (t 0,95), 2015-2018 -81 (t -0,61); 2010-2018 komşuları (RSI 5/10/15 × SMA 150/200/250) -24..+2 bp; etki 2021 sonrası. (4) Kuyruk: ajanın 'Şubat 2018 pozisyon yok' ifadesi yanıltıcı (gerçek SVXY verisi 2018-09'da başlıyor); vekilde 02.02.2018 RSI2=12,4 (eşik 10) ve SMA200 üstü: kıl payı; eşik 12,5 olsaydı Volmageddon taşınırdı (-0,5x ile ~-%45-50). Vekilde 20.08.2015 işlemi -2.330 bp. (5) Getirinin çoğu hisse betası: SPY'ye beta 2,28, R²=0,84, alfa brüt 48 bp/işlem (t 2,37). (6) O1'de en iyi 5 çıkarılınca +57 bp t=1,43; C1 çalışmıyor. (7) PTP: ProShares Trust II 26.02.2026 Qualified Notice '10 percent exception applies' (92 gün; sonrası kontrol edilmedi), ancak Midas 2024'te UNG'de geçici %10 brüt kesinti uyguladı; kesinti olursa işlem başı ~-1.000 bp; Midas'ta SVXY bulunurluğu doğrulanmadı.
- **Giriş zamanı sağlamlığı:** h=2: C0 +157 (t=3,16), O1 +108 (t=2,53), C1 -28 (t=-0,51). h=1: C0 +82 (2,44), O1 +26 (1,12), C1 +47 (1,51). h=3: C0 +106 (1,59), O1 +46 (0,75), C1 +28 (0,48). C0 ve O1'de çalışıyor, C1'de çalışmıyor: kenar sinyalden sonraki ilk 1-2 günde, gecikmeli girişte kaybolur.
- **Maliyet duyarlılığı:** SVXY C0 h2 net: 1.000$ +139 bp, 2.500$ +157 bp, 10.000$ +166 bp. O1 h2: +90 / +108 / +117 bp.
- **Not:** Yıllar (C0 h2 net toplam bp): 2019 -647, 2020 -1042, 2021 +4418, 2022 -681, 2023 +2339, 2024 +1236, 2025 +1146, 2026 +2511. Kuyruk: Mart 2020'de 1 işlem -1.375 bp (sinyal 21.02.2020); Ağustos 2024 +355 bp; Şubat 2018, Nisan 2025 ve Kasım 2026'da pozisyon yok. Parametreye duyarlı: RSI<5 ya da <15 komşuları ve filtresiz sürüm zayıf. Sinyal günü VIX yüksekse kazanç büyüyor (VIX>25 iken ort. +460 bp, n=6); bu tanımlayıcı bir gözlem, filtre değil. 06.11.2026: SVXY 54,72 < SMA200 55,93, RSI2 21, sinyal yok. PTP: SVXY ProShares Trust II (K-1). Midas'ta satışta %10 brüt kesinti uygulanırsa her işlem ~-1.000 bp kaybeder ve strateji çöker; işlemden önce Midas'tan teyit alınmalı. Şubat 2018 tipi bir gecede (endeks +%96) SVXY ~-%45-50, SVIX ~-%90+ kaybedebilir. Pozisyon küçük tutulmalı. Midas zarar-durdur emri boşlukta dolmayabilir.
- Betik: `python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_volatilite/strateji_S1.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| VIX günlük log değişimi | `CBOE:VIX` | -0.91 | -0.23 |
| VVIX günlük log değişimi | `CBOE:VVIX` | -0.90 | -0.30 |
| SPY günlük getiri | `AMEX:SPY` | 0.83 | 2.01 |
| VIX/VIX3M oranı günlük değişimi | `CBOE:VIX/CBOE:VIX3M` | -0.82 | -0.46 |
| QQQ günlük getiri | `NASDAQ:QQQ` | 0.74 | 1.13 |

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

Doğrulanmış gecikmeli öncü yok: genel taramada aile hedefleri için FDR'yi geçen 0. Ek 144 testte (VIX/VIX3M düzeyi ve değişimi, VIX9D/VIX, VIX gerilmesi, VVIX/VIX, SPY/QQQ/BTC getirileri, DGS10; kendi gecikmesi kontrollü, Newey-West, C0 ve O1 hizalaması) de 0. Eşzamanlı sürücüler öncü değildir. VIX 16:15 ET'de kapandığı için C0 hizalamasındaki VIX öncülüğü kısmen ileri bakıştır. En güçlü (geçmeyen) aday: QQQ getirisi -> SVXY 3 gün (C0 t=-2,89; IS -2,33, OOS -1,86; FDR yok). QQQ'nun yükseldiği günden sonra SVXY hafif geri veriyor. Kendi fiyat sinyali (RSI2) S1'de kullanılıyor; o bir lead-lag değil.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_volatilite.md`, `notlar/denetim_volatilite.md`.*
