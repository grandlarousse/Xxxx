# SOXL — Direxion Daily Semiconductor Bull 3X ETF

**TradingView:** `AMEX:SOXL` · **Aile:** Sektör ve tematik · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 6.540 | 14,2 | 916 | %-38,7 | 3,0x | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** A2 sinyalinin 3x aracı (A2-3x). Çok likit (6.5 mlr $/gün), maliyet/oynaklık 0.015. UYARI: Midas'ta bulunurluğu DOĞRULANAMADI; 3x kaldıraç, 1 günden uzun tutuşta oynaklık kaybı; 1940 Kanunu fonu (PTP değil). **Ana ajan notu:** Koşullu: Midas bulunurluğu doğrulanmadı; risk eşdeğerinde SMH'ye üstünlüğü yok; 1 günden uzun tutma.

*Dayanak / ana araç kartı: `kartlar/SMH.md` (sürücüler ve gerçek zamanlı izleme listesi orada daha ayrıntılı).*

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt ya da yalnız filtre — tek başına işlem gerekçesi değil)

#### A2-3x — A2'nin 3x aracı: SMH IBS<0.20 sinyaliyle SOXL (1 gün)  
*İzlemede — zayıf kanıt · güven: orta · aile kimliği: `sektor_tematik_S2`*  
*Bu ETF'nin rolü: 3x araç (SMH tutarının ~1/3'ü)*

- **Sinyal (t kapanışında):** Sinyal A2 ile aynı: NASDAQ:SMH günlük IBS = (close-low)/(high-low) < 0.20. İşlem AMEX:SOXL (3x yarı iletken) long al, ertesi işlem günü kapanışında sat. Sinyal SOXL'ün kendi mumundan DEĞİL, SMH'den hesaplanır (SOXX IBS de olur: 139 bp, t 4.3). Aynı riski almak için SOXL tutarı SMH'ye ayrılacak tutarın ~1/3'ü olmalı.
- **Giriş:** C0: kış TR 23:45-23:58 / yaz 22:45-22:58, kapanıştan hemen önce (kaldıraçlı fonun kapanış yeniden dengelemesi son dakikalarda oynaklık yaratır; limit emir). O1 alternatifi: ertesi açılış (kış TR 17:30 / yaz 16:30).
- **Tutuş / çıkış:** 1 işlem günü. 1 günden uzun tutuşta oynaklık kaybı ölçüldü: SOXL-3×SOXX sapması h1 -9 bp, h3 -31 bp, σ20≥%3 iken h3 -75 bp (ortalama). — Ertesi işlem günü kapanışından hemen önce sat. Stop yok.
- **İşlem aracı:** SOXL (sinyal: SMH)
- **Geçmiş (ajan):** n=492, net 145.8 bp/işlem (brüt 160.0), kazanma %61, t=4.23, IS 144.0 / OOS 147.7 bp, yılların %91'i pozitif, en kötü işlem -3056 bp
- **Denetçi düzeltmesi:** AH girişi cezası SOXL'de ~3x (yaklaşık -18 bp) varsayılırsa 2.500$ net ~128 bp; risk eşdeğeri (SMH tutarının 1/3'ü) dolar kârı SMH ile aynı.
- **Denetçi kural düzeltmesi:** Ayrı strateji olarak sunulmamalı; A2'nin isteğe bağlı aracı, yalnız Midas'ta SOXL doğrulanırsa ve SMH tutarının en fazla 1/3'üyle; aynı after-hours giriş kuralı.
- **Denetim:** Birebir: n=492, brüt 160.0, net 145.8 bp, t 4.23, IS 144.0 / OOS 147.7, maxDD -%53.5, en kötü -3056 bp. En iyi 5 hariç 114.3 (t 3.64); O1 h1 72.3 (t 2.74); C1 h1 kenar ~0. Gün içi test: 15:30 IBS + 15:30 giriş net 190 bp (t 2.22) vs backtest 229 (t 2.59). Sağlamlık: İstatistik olarak A2'nin 3 katı; A2'nin sağlamlık testleri geçerli. 1.000$: 127.8 bp (t 3.71) backtest.
- **Denetçinin uyarıları:** A2 ile aynı sinyal (bağımsız kanıt değil); SOXL'ün Midas'ta bulunurluğu doğrulanmadı; risk eşdeğeri boyutta (833$) işlem başına 10.15$ vs SMH 2.500$ ile 10.44$: ek getiri yok, yalnız sermaye verimi; tam tutarla maxDD -%53.5, en kötü işlem -%30.6; işlem günlerinde SOXL-3xSOXX -15.7 bp; SOXL 2026-06-04 262.7 -> 2026-11-06 46 (-%82), 1g oynaklık ~%9: A2 sinyalleri bu rejimde sık tetiklenir ve tek işlem -%30 olabilir. A2'nin kapanış/FDR sorunları aynen geçerli.
- **Giriş zamanı sağlamlığı:** C0 h1 net 145.8; O1 h1 brüt 86.5 (net 72.3, t 2.74); C1 h1 brüt 32.7 (koşulsuza göre kenar -0.3 ≈ 0).
- **Maliyet duyarlılığı:** 1.000$: 127.8 bp | 2.500$: 145.8 bp | 10.000$: 154.8 bp (net, işlem başına; SOXL tutarı)
- **Not:** Risk eşdeğeri karşılaştırma: SOXL'ü SMH tutarının 1/3'üyle (ör. 833 $) almak, 2.500 $'lık SMH ile işlem başına ~aynı dolar kârı verir (SOXL 833$: ~122 bp x 833 = ~10.1 $; SMH 2.500$: 41.8 bp x 2.500 = ~10.4 $), çünkü sabit 3 $ komisyon küçük tutarda daha ağır. SOXL'ün tek avantajı sermaye verimi; karşılığında maxDD -53% (işlem başına tam sermaye), en kötü işlem -30.6% (2020-03-11). Midas'ta SOXL bulunurluğu DOĞRULANAMADI (notlar/midas_kosullari.md: 'doğrulanamadı'); uygulamada Keşfet > Pay ara ile kontrol edilmeli. PTP değil (1940 Kanunu fonu).
- Betik: `python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_sektor_tematik/strateji_adaylari.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| XLK | `AMEX:XLK` | 0.92 | 4.86 |
| QQQ | `NASDAQ:QQQ` | 0.89 | 6.29 |
| EEM | `AMEX:EEM` | 0.84 | 4.79 |
| TSM | `NYSE:TSM` | 0.83 | 3.01 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Nasdaq-100 vadelisi (neredeyse 24 saat) | `CME_MINI:NQ1!` | ETF kapalıyken (TR 00:00-17:30) teknoloji yönünü gösterir; açılış boşluğunu önceden verir. |
| KOSPI endeksi (Kore) | `KRX:KOSPI` | Asya seansında (TR ~03:00-09:30) bellek/yarı iletken (Samsung, SK Hynix) hareketi; SMH açılışını önceden gösterir. |
| NVIDIA (uzatılmış seans) | `NASDAQ:NVDA` | Bilanço kapanış sonrası açıklanır; after-hours/pre-market fiyatı SMH açılış boşluğunu gösterir (SMH ile 1y korelasyon 0.73). |
| TSMC ADR (pre-market) | `NYSE:TSM` | Tayvan seansı sonrası TSMC ADR'ı pre-market'te (TR 12:00-17:30) fiyatlanır. |

## 3. Takvim ve olay riskleri

SMH ile aynı; ayrıca σ20≥%3 dönemlerinde 1 günden uzun tutuşta ölçülen kayıp (3 günde ~-75 bp).

## 4. Notlar

Doğrulanmış gecikmeli öncü yok. Sinyal SMH'den alınır (A2-3x). Kaldıraçlı fon kapanışta yeniden dengeler: son dakikalarda oynaklık artabilir.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_sektor_tematik.md`, `notlar/denetim_sektor_tematik.md`.*
