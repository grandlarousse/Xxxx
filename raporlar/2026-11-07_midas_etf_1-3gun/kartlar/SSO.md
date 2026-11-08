# SSO — ProShares Ultra S&P500

**TradingView:** `AMEX:SSO` · **Aile:** ABD endeks ve faktör · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 211 | 14,0 | 170 | %-8,8 | 2,0x | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** SPY 2x aracı: daha ılımlı kaldıraç (B1 C1 net 121 bp, t=3,0; en kötü işlem −%13,8). 3 günlük kaldıraç kaybı ≈2 bp.

*Dayanak / ana araç kartı: `kartlar/SPY.md` (sürücüler ve gerçek zamanlı izleme listesi orada daha ayrıntılı).*

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt ya da yalnız filtre — tek başına işlem gerekçesi değil)

#### B1 — Zayıf kapanış dönüşü (IBS<0,10 + düşüş günü) — S&P 500 / SPY, 3 gün  
*İzlemede — zayıf kanıt · güven: orta · aile kimliği: `abd_endeks_S1`*  
*Bu ETF'nin rolü: 2x araç*

- **Sinyal (t kapanışında):** TradingView günlük grafik AMEX:SPY (ayarlarda temettü düzeltmesi 'ADJ' açık). IBS=(kapanış−düşük)/(yüksek−düşük). SİNYAL (t günü kapanışı): IBS<0,10 VE kapanış<önceki günün kapanışı (gün düşüşle ve günün dibine çok yakın kapandı). İŞLEM: AMEX:SPY long (alternatif araç: AMEX:SSO 2x / AMEX:SPXL 3x — sinyal yine SPY verisinden). Ana mod C1: t+1 kapanışında al, 3 işlem günü sonra (t+4) kapanışta sat. Pozisyondayken gelen yeni sinyal yok sayılır. Stop yok. Pine: ibs=(close-low)/(high-low); sinyal = ibs<0.10 and close<close[1]
- **Giriş:** Sinyali t akşamı ABD kapanışından sonra (kış TR 00:00 / yaz 23:00) gör; ertesi işlem günü (t+1) kapanıştan 5-10 dk önce (kış TR ~23:50, yaz ~22:50) piyasa ya da agresif limit emriyle al (Midas'ta MOC/LOC yok). Alternatif C0: t günü TR ~23:50'de anlık fiyatla IBS<0,10 ve düşüş koşulu sağlanıyorsa aynı kapanışta al (hafif iyimser). O1 (t+1 açılışı TR 17:30 kış/16:30 yaz) daha zayıf.
- **Tutuş / çıkış:** 3 işlem günü — Girişten 3 işlem günü sonra kapanıştan 5-10 dk önce sat (kış TR ~23:50, yaz ~22:50). Erken kapanış günlerinde (27 Kas 2026, 24 Ara 2026) kapanış 13:00 ET = TR 21:00. Erken çıkış kuralı yok.
- **İşlem aracı:** SPY, SSO, SPXL (sinyal: SPY)
- **Geçmiş (ajan):** n=155, net 55.7 bp/işlem (brüt 68.7), kazanma %63, t=2.79, IS 78.1 / OOS 40.3 bp, yılların %100'i pozitif, en kötü işlem -675 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** C0: net 80 bp (t 2,3, n=181) · O1: net 61 bp (t 1,8, n=181) · C1: net 115 bp (t 3,0, n=165); 1.000 $ pozisyonda ana mod net 97 bp (t 2,6)
- **Denetçi düzeltmesi:** SPY'da gerçekçi beklenti: net ≈25-35 bp/işlem (2.500$; komşu medyanı 27,5; en iyi 5 hariç 30,0/t1,93; takvim zamanlı OOS ≈24 net). 1.000$ pozisyonda ≈7-17 bp, VIX<20'de negatif. Seçim düzeltmeli p=0,20.
- **Denetçi kural düzeltmesi:** Kural aynı (SPY IBS<0,10 ve kapanış<önceki kapanış). SPY sinyali bağımsız strateji değil, A1 ile aynı fırsat kümesinin piyasa geneli göstergesi olarak kullanılmalı. İşlem aracı olarak QQQ tercih edilmeli (SPY sinyali -> QQQ C1 74 bp t=3,34; C0 57/t2,65; O1 45/t2,08). C0 ile C1 arasında gerçek fark yok; pozisyondayken gelen sinyalde ne yapılacağı (yok say / uzat) önceden sabitlenmeli.
- **Denetim:** Birebir: SPY C1 h3 n=155, brüt 68,7, net 55,7, kazanma 0,63, PF 1,93, t=2,79, IS 78,1 (t 2,09), OOS 40,3 (t 1,85), yıl+ 1,0, maxDD -%12, en kötü -675. C0 35,9/t1,98 (IS 17/t0,60); O1 24,8/t1,35 (IS 4/t0,14); ek C2 19,0/t0,97 (OOS -3,7). Kaldıraçlı: SSO 121/t3,00, SPXL 183/t2,99, UPRO 185/t3,02 (en kötü -%22,8). Kod hatası/ileriye bakış yok; en büyük 5 kazanç gerçek kriz dönüşleri (20.03.2020 +1.716, 03.04.2025 +858, 11.03.2022 +577, 21.12.2018 +572, 12.05.2020 +476 bp). Sağlamlık: Tek test permütasyonu güçlü: rastgele gün p=0,0005; düşüş+VIX eşleşmeli p=0,002; dairesel p=0,0005. IBS katkısı gerçek (düşüş & IBS≥0,30: 5 bp; tüm düşüş günleri 7 bp). 2020 hariç 47,2/t2,79; 2022 hariç 64,1/t2,92. Maliyet 1.000/2.500/10.000$: 38/56/65 bp. Ancak seçim düzeltmesi, komşuluk ve en iyi 5 hariç testlerinde eşik altına düşüyor.
- **Denetçinin uyarıları:** (1) Başlık hücresi (C1 h=3) 9 mod×tutuş hücresinin en iyisi ve sivri tepe: C1 h=1-4 13/22/56/45 bp (t 1,1/1,3/2,8/1,9); mod ekseninde C0/C1/C2 36/56/19 bp. (2) Seçim düzeltmeli test (SPY'da 279 hücre max-t, dairesel kaydırma): null max-t medyanı 2,29, %95'i 3,22 -> p=0,20; aile düzeyi p=0,09. Tek yönlü BH ve Bonferroni geçmez. (3) En iyi 5 işlem hariç net 30,0 bp, t=1,93 (C0'da 20,1/t1,17). (4) Komşu 54 hücrenin yalnız %30'unda t≥2 (medyan net 27,5 bp). (5) Kâr VIX≥20 günlerinde: VIX<20 n=72 brüt 25,8 -> net 2.500$'da 12,8, 1.000$'da -5,2 bp. (6) C1'in C0'dan iyi görünmesi çakışmasızlık kuralının yol artefaktı: takvim zamanlı sürümde C0 t=2,66 ≈ C1 t=2,70; 'yeni sinyalde süreyi uzat' kuralıyla C0 52 bp/t2,73, C1 54/t2,33. (7) 2024+ n=44 t=1,54. OOS t=1,85<2.
- **Giriş zamanı sağlamlığı:** C0: brüt 49 bp, net 36 bp, t=1.98; O1: brüt 38 bp, net 25 bp, t=1.35; C1: brüt 69 bp, net 56 bp, t=2.79
- **Maliyet duyarlılığı:** 1.000$: 38 bp | 2.500$: 56 bp | 10.000$: 65 bp (net, işlem başı)
- **Not:** Aile genelinde en tutarlı sonuç: 19 grup temsilcisinin 19'unda C1 h=3 net>0, 18'inde IS ve OOS>0; 6 çekirdek endeks ETF'si sepeti t=2,44 (C1), SPY+QQQ+IWM sepeti t=2,77. Komşu eşikler (IBS 0,05-0,30, düşüş şartlı/şartsız) IS ve OOS'ta hep pozitif. Sinyal sonrası 1-4. günler ortalamanın üstünde, 5. gün negatif. Koşulsuz 3 günlük getiri 16 bp, kenar (edge) 53 bp (t=2,64). 2020 hariç C1 net 47 bp (t=2,79); 2024+ net 51 bp (t=1,54). Yılda ~16 işlem. ÖNEMLİ: etki piyasa geneli zayıf kapanışlarda — 19 temsilcinin ≥10'unun aynı gün sinyal verdiği 99 günde gün-ortalaması net 94 bp (t=3,55), 1-10 ETF'in sinyal verdiği günlerde ≈0; sinyal SPY'dan alınmalı (19 temsilci gün-sepeti t=1,23 bu yüzden düşük). SPY sinyaliyle başka ETF'de işlem (C1): QQQ 74 bp t=3,34; IWM 59 bp t=2,40; MDY 56 t=2,34; RSP 50 t=2,34; DIA 45 t=2,20 (sonradan bakıldı, bilgi). VIX≥20 iken SPY C1 net 93 bp (t=2,75, n=83), VIX<20 iken 13 bp (t=0,75, n=72) — 7 filtre denendiği için yalnız bilgi, kurala eklenmedi. Kaldıraçlı araç (C1): SSO (2x): net 121 bp, t=3.00, maxDD -23%, en kötü işlem -13.8%, en kötü gün -19.1%; UPRO (3x): net 185 bp, t=3.02, maxDD -35%, en kötü işlem -22.8%, en kötü gün -29.0%; SPXL (3x): net 183 bp, t=2.99, maxDD -35%, en kötü işlem -22.8%, en kötü gün -28.7%. Sabit komisyonda kaldıraç yalnız sermaye verimliliği sağlar (2.500$ SPXL ≈ 7.500$ SPY, aynı 3$), kuyruk riski 3 kat. Literatürle uyumlu: h=1'de net ~0 (Pandey & Joshi 2023), etki 2-4 günde. SPY-QQQ sinyallerinin %73'ü aynı gün. IS t=2.09, OOS t=1.85.
- Betik: `python3 -I kod/ajan_abd_endeks/05_adaylar.py (sayıları basar; önce 01-04 gerekmez)`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| SPY | `AMEX:SPY` | 1.00 | 1.99 |
| QQQ | `NASDAQ:QQQ` | 0.93 | 1.18 |
| VIX (log değişim) | `CBOE:VIX` | -0.86 | -0.18 |
| XLK | `AMEX:XLK` | 0.85 | 0.82 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| S&P 500 E-mini vadeli | `CME_MINI:ES1!` | Dayanak SPY ile aynı izleme seti (SPY satırına bakın); vadeli hareketi x kaldıraç = beklenen açılış boşluğu. |

## 3. Takvim ve olay riskleri

SPY satırındaki takvimle aynı (CPI 10 Kas, OPEX 20 Kas, 26-27 Kas tatil/erken kapanış, NFP 4 Ara, FOMC 9 Ara, CPI 10 Ara, OPEX 18 Ara, 24-25 Ara).

## 4. Notlar

Kaldıraçlı araç: sinyal ve öncü analizi dayanak SPY üzerinden yapılır (korelasyon ≈1,00). Doğrulanmış gecikmeli öncü YOK (aile alt kümesi BH-FDR 0/2.636; yetişme, faiz kanalı ve IWM-SPY ayrıntısı SPY satırında). En güçlü (FDR'siz) gecikmeli satırlar: TIP (h3): t=2.67, IS 3.2/OOS 1.4, 50 bp/sd; DFII10_d (h3): t=-2.53, IS -2.7/OOS -1.5, -42 bp/sd. Bu ETF için işlem sinyali öncüden değil kendi fiyat deseninden gelir (B1/A1: IBS<0,10 + düşüş).

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_abd_endeks.md`, `notlar/denetim_abd_endeks.md`.*
