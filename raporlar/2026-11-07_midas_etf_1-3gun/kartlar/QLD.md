# QLD — ProShares Ultra QQQ

**TradingView:** `AMEX:QLD` · **Aile:** ABD endeks ve faktör · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 368 | 14,0 | 266 | %-12,7 | 2,0x | 2016-11-07 |

**Kademe:** A — denetimden geçmiş kural var  
**Neden izleme listesinde:** QQQ 2x aracı: A1 C1 net 145 bp (t=3,5), en kötü işlem −%19,6. Midas bulunurluğu doğrulanmadı.

*Dayanak / ana araç kartı: `kartlar/QQQ.md` (sürücüler ve gerçek zamanlı izleme listesi orada daha ayrıntılı).*

## 1. Ne zaman girilir?

#### A1 — Zayıf kapanış dönüşü (IBS<0,10 + düşüş günü) — Nasdaq-100 / QQQ, 3 gün  
*Uygulanabilir (denetçi doğruladı) · güven: orta · aile kimliği: `abd_endeks_S2`*  
*Bu ETF'nin rolü: 2x araç (dayanak tutarının ~1/2'si)*

- **Sinyal (t kapanışında):** TradingView günlük grafik NASDAQ:QQQ (ayarlarda temettü düzeltmesi 'ADJ' açık). IBS=(kapanış−düşük)/(yüksek−düşük). SİNYAL (t günü kapanışı): IBS<0,10 VE kapanış<önceki günün kapanışı (gün düşüşle ve günün dibine çok yakın kapandı). İŞLEM: NASDAQ:QQQ long (alternatif araç: AMEX:QLD 2x / NASDAQ:TQQQ 3x — sinyal yine QQQ verisinden). Ana mod C1: t+1 kapanışında al, 3 işlem günü sonra (t+4) kapanışta sat. Pozisyondayken gelen yeni sinyal yok sayılır. Stop yok. Pine: ibs=(close-low)/(high-low); sinyal = ibs<0.10 and close<close[1]
- **Giriş:** Sinyali t akşamı ABD kapanışından sonra (kış TR 00:00 / yaz 23:00) gör; ertesi işlem günü (t+1) kapanıştan 5-10 dk önce (kış TR ~23:50, yaz ~22:50) piyasa ya da agresif limit emriyle al (Midas'ta MOC/LOC yok). Alternatif C0: t günü TR ~23:50'de anlık fiyatla IBS<0,10 ve düşüş koşulu sağlanıyorsa aynı kapanışta al (hafif iyimser). O1 (t+1 açılışı TR 17:30 kış/16:30 yaz) daha zayıf.
- **Tutuş / çıkış:** 3 işlem günü — Girişten 3 işlem günü sonra kapanıştan 5-10 dk önce sat (kış TR ~23:50, yaz ~22:50). Erken kapanış günlerinde (27 Kas 2026, 24 Ara 2026) kapanış 13:00 ET = TR 21:00. Erken çıkış kuralı yok.
- **İşlem aracı:** QQQ, QLD, TQQQ (sinyal: QQQ)
- **Geçmiş (ajan):** n=169, net 70.6 bp/işlem (brüt 83.6), kazanma %60, t=3.46, IS 76.2 / OOS 65.9 bp, yılların %100'i pozitif, en kötü işlem -831 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** C0: net 161 bp (t 4,1, n=189) · O1: net 121 bp (t 3,3, n=189) · C1: net 141 bp (t 3,5, n=177); 1.000 $ pozisyonda ana mod net 123 bp (t 3,1)
- **Denetçi düzeltmesi:** Beklenti backtestin altında alınmalı: gerçekçi net ≈45-55 bp/işlem (2.500$; en iyi 5 hariç 47, takvim zamanlı OOS ≈48), t≈2,5-3. Güven: orta. Seçim düzeltmeli p=0,025-0,055 (QQQ), aile düzeyi 0,09.
- **Denetim:** Bağımsız motorla (lib.trades/evaluate/ae.full_eval kullanılmadan; IBS ham OHLC'den çapraz kontrol, fark <1e-13) birebir: QQQ C1 h3 n=169, brüt 83,6, net 70,6 bp, kazanma 0,60, PF 2,06, t=3,46, IS 76,2 (t 2,57), OOS 65,9 (t 2,33), yıl+ 1,0, maxDD -%9, en kötü -831 bp. C0 76,2/t3,68; O1 55,3/t2,94; ek C2 (t+2 kapanış) 54,1/t2,65. İleriye bakış yok (sinyal yalnız t OHLC + t-1 kapanış), giriş/çıkış günleri doğru, çakışma yok, maliyet bir kez. En büyük kazançlar 20.03.2020, 03.04.2025 (09.04.2025 gümrük ertelemesi), 11.03.2022: gerçek olaylar, veri hatası yok. Sağlamlık: Permütasyon (2.000): rastgele gün p=0,0005; düşüş günü + VIX beşte biri eşleşmeli p=0,004 (C1) / 0,0005 (C0) / 0,012 (O1); dairesel kaydırma p=0,0005. Parametre platosu: eşik 0,05-0,20 × h 2-4 × 3 mod (54 hücre) medyan net 57 bp, %78'inde t≥2, %96'sında IS>0 ve OOS>0. Takvim zamanlı (örtüşmeli) C1 26,1 bp/gün t=3,52 (OOS 20,5 bp/gün). 2020 hariç 61,5/t3,03; 2022 hariç 80,1/t3,68; en iyi 5 hariç 47,2/t2,65. VIX<20 net 47 bp, VIX≥20 91 bp. Maliyet 1.000/2.500/10.000$: 53/71/80 bp. SPY sinyaliyle QQQ C1 74 bp t=3,34.
- **Denetçinin uyarıları:** (1) Tam çoklu test düzeltmesinde sınırda: tek yönlü BH (17.391 test) 0 geçen, Bonferroni t≈4,4-4,5 gerekir. Kendi seçim düzeltmeli testim (QQQ'da genel kütüphanenin 279 hücresinin max-t'si, dairesel kaydırma null) p=0,025 (C0) / 0,055 (C1); aile düzeyi (19 temsilcinin ort. t'si, 279 hücre) p=0,09. QQQ ailenin en iyi sonucu (ETF seçimi düzeltilmedi). (2) C0 sonucu kapanış öncesi sınıflamaya duyarlı: IBS 0,08-0,12 / |r|<%0,1 sınır günleri çıkarılınca 76→56 bp (t 2,43). (3) 2024+ n=43, t=1,62. (4) En iyi 5 işlem ortalamanın ~23 bp'sini taşıyor (kriz dönüşleri). (5) Örneklem 2016+ boğa piyasası; uzun ayı piyasası test edilmedi. (6) SPY ile sinyal günlerinin %73'ü ortak: B1 ile birlikte almak risk ikilemesi.
- **Giriş zamanı sağlamlığı:** C0: brüt 89 bp, net 76 bp, t=3.68; O1: brüt 68 bp, net 55 bp, t=2.94; C1: brüt 84 bp, net 71 bp, t=3.46
- **Maliyet duyarlılığı:** 1.000$: 53 bp | 2.500$: 71 bp | 10.000$: 80 bp (net, işlem başı)
- **Not:** B1 ile aynı kural, Nasdaq-100 dayanağı; tüm modlarda t>2,9 (C0 3,68 / O1 2,94 / C1 3,46), IS ve OOS t>2. Kenar 60 bp (t=2,95), koşulsuz 3 günlük 23 bp. 2020 hariç net 62 bp (t=3,03); 2024+ 70 bp (t=1,62). QQQ'nun 2016-2026 güçlü teknoloji trendi sonucu şişirmiş olabilir (aynı kural her endekste pozitif ama en güçlü QQQ'da: seçim yanlılığı riski). B1 ile sinyallerin %73'ü aynı gün: ikisini birlikte almak çeşitlendirme değil, riski ikiye katlar; birini seç ya da pozisyonu böl. QQQ'nun SPY'ın sinyal vermediği (yalnız teknoloji) günlerdeki sinyalleri C1'de zayıf (n=50, net 42 bp, t=1,49), C0'da güçlü (n=54, 95 bp, t=3,03). Kaldıraçlı araç (C1): QLD (2x): net 145 bp, t=3.50, maxDD -20%, en kötü işlem -19.6%, en kötü gün -24.3%; TQQQ (3x): net 220 bp, t=3.50, maxDD -32%, en kötü işlem -31.0%, en kötü gün -34.5%. TQQQ'da tek işlemde −%31 kayıp yaşandı (Mart 2020); kaldıraçlı kullanım yalnız küçük sermaye payıyla. IS t=2.57, OOS t=2.33.
- Betik: `python3 -I kod/ajan_abd_endeks/05_adaylar.py (sayıları basar; önce 01-04 gerekmez)`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| QQQ | `NASDAQ:QQQ` | 1.00 | 2.00 |
| XLK | `AMEX:XLK` | 0.96 | 1.44 |
| SPY | `AMEX:SPY` | 0.93 | 2.90 |
| SMH | `NASDAQ:SMH` | 0.91 | 0.91 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Nasdaq-100 E-mini vadeli | `CME_MINI:NQ1!` | Dayanak QQQ ile aynı izleme seti (QQQ satırına bakın); vadeli hareketi x kaldıraç = beklenen açılış boşluğu. |

## 3. Takvim ve olay riskleri

SPY satırındaki takvimle aynı (CPI 10 Kas, OPEX 20 Kas, 26-27 Kas tatil/erken kapanış, NFP 4 Ara, FOMC 9 Ara, CPI 10 Ara, OPEX 18 Ara, 24-25 Ara).

## 4. Notlar

Kaldıraçlı araç: sinyal ve öncü analizi dayanak QQQ üzerinden yapılır (korelasyon ≈1,00). Doğrulanmış gecikmeli öncü YOK (aile alt kümesi BH-FDR 0/2.636; yetişme, faiz kanalı ve IWM-SPY ayrıntısı SPY satırında). En güçlü (FDR'siz) gecikmeli satırlar: TIP (h3): t=3.05, IS 3.3/OOS 1.6, 52 bp/sd; DFII10_d (h3): t=-3.02, IS -2.8/OOS -1.8, -44 bp/sd. Bu ETF için işlem sinyali öncüden değil kendi fiyat deseninden gelir (B1/A1: IBS<0,10 + düşüş).

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_abd_endeks.md`, `notlar/denetim_abd_endeks.md`.*
