# GLDM — SPDR Gold MiniShares Trust

**TradingView:** `AMEX:GLDM` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 427 | 14,0 | 181 | %-10,1 | 1,0x | 2018-06-26 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** GLD kopyası (0,999), maliyet 14 bp, geçmiş 2018-06'dan. Uzun vadeli tutuş için ucuz gider oranı; 1-3 günde GLD'ye üstünlüğü yok.

*Dayanak / ana araç kartı: `kartlar/GLD.md` (sürücüler ve gerçek zamanlı izleme listesi orada daha ayrıntılı).*

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt ya da yalnız filtre — tek başına işlem gerekçesi değil)

#### B3b — Ay sonu (turn-of-month) - altın (GLD)  
*İzlemede — zayıf kanıt · güven: dusuk · aile kimliği: `metal_madenci_S2`*  
*Bu ETF'nin rolü: kopya araç*

- **Sinyal (t kapanışında):** B3a ile aynı takvim kuralı, işlem AMEX:GLD: ayın SON NYSE işlem günü kapanışında al, yeni ayın 3. işlem günü kapanışında sat. Gösterge yok. B3a ile AYNI etkidir (GLD-GDX 1y korelasyon 0,86); ikisini birlikte açmak aynı bahsi ikiye katlar.
- **Giriş:** C0: ayın son işlem günü TR ~23:45-23:59 (kış) / ~22:45-22:59 (yaz); MOC yok, piyasa ya da limit emir. O1 alternatifi: net 18,7 bp, t 1,19.
- **Tutuş / çıkış:** 3 işlem günü. — Yeni ayın 3. işlem günü kapanışında (TR ~23:45-23:59 kış) sat.
- **İşlem aracı:** GLD, IAU/GLDM (kopya) (sinyal: Takvim (NYSE); işlem AMEX:GLD)
- **Geçmiş (ajan):** n=111, net 39.9 bp/işlem (brüt 52.9), kazanma %56, t=2.45, IS 33.8 / OOS 45.4 bp, yılların %70'i pozitif, en kötü işlem -388 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** C0: net 34 bp (t 2,2, n=117) · O1: net 17 bp (t 1,1, n=117) · C1: net 18 bp (t 1,0, n=117) [bu ETF için ayrı hesap yok; ana araç GLD rakamları]
- **Denetçi düzeltmesi:** Sayılar doğru. Ek: 2024-26 hariç 15,9 bp/t 0,90; en iyi 5 hariç 21,7/t 1,46; 1.000$ 21,9/t 1,34.
- **Denetim:** Birebir: n=111, brüt 52,9, net 39,9 bp, t 2,45, IS 33,8 (t 1,65) / OOS 45,4 (t 1,81), maxDD -%7,7. Sağlamlık: 2020 hariç t 1,97, 2022 hariç t 2,64; son gün girişinde h2-h6 t 1,8-2,7; kopyalarda aynı (takvim kuralı OHLC'den bağımsız olduğu için beklenen).
- **Denetçinin uyarıları:** B3a ile aynı etki (GLD-GDX 0,86) -> bağımsız kanıt değil; FDR geçmez; 2024-26 hariç 15,9 bp/t 0,90 (son üç yılın altın boğasına bağlı); en iyi 5 hariç 21,7/t 1,46; 1.000$'da 21,9/t 1,34; +10 bp kaymada t 1,83; O1 t 1,19, C1 t 1,30; permütasyon p 0,012; 2021-2023 üç yıl üst üste ≤0.
- **Giriş zamanı sağlamlığı:** C0: n=111, brüt 52.9 bp, net 39.9 bp, t 2.45; O1: n=111, brüt 31.7 bp, net 18.7 bp, t 1.19; C1: n=111, brüt 36.7 bp, net 23.7 bp, t 1.30
- **Maliyet duyarlılığı:** 1.000$: net 21.9 bp | 2.500$: net 39.9 bp | 10.000$: net 48.9 bp (2.500$ maliyeti 13.0 bp)
- **Not:** Tek ETF eşiğini geçer (t 2,45; IS 33,8/t1,65; OOS 45,4/t1,81; yılların %70'i pozitif; O1/C1 brüt 31,7/36,7 bp) ama FDR'yi geçmez. Yıl ortalaması çıkarılmış kenar 36,4 bp (t 2,28, yılların %90'ı pozitif); en iyi yıl (2025) hariç t 1,65. Etkinin bir kısmı ilk gece (C0 h1 31 bp vs O1 h1 9,5 bp). Düşük oynaklıklı (maxDD -%8) ve PTP'siz olduğundan B3a'den daha sakin bir uygulama. (IS t=1.65, OOS t=1.81)
- Betik: `python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_metal_madenci/t5_adaylar.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| GLD (eşzamanlı sürücü, öncü değil) | `AMEX:GLD` | 1.00 | 0.99 |
| SLV (eşzamanlı sürücü, öncü değil) | `AMEX:SLV` | 0.84 | 0.37 |
| GDX (eşzamanlı sürücü, öncü değil) | `AMEX:GDX` | 0.86 | 0.49 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

Doğrulanmış (denetimden geçmiş) gecikmeli öncü yok: bu ETF'nin sürücüleri aynı gün fiyatlanıyor.

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| COMEX altın vadeli (sürekli) | `COMEX:GC1!` | ~23 saat işler (TR kış 02:00-01:00); ETF kapalıyken oluşan hareket açılış boşluğunu gösterir. İzleme aracı, öncü değil. |
| Spot altın | `OANDA:XAUUSD` | Asya/Londra seansı; TR 12:00-17:30 arasında GLD açılışını önceden gösterir. |

## 3. Takvim ve olay riskleri

FOMC 09.12.2026 14:00 ET (TR 22:00; örneklemde FOMC sonrası altın zayıf, anlamsız); CPI 10.11 ve 10.12.2026, NFP 04.12.2026 08:30 ET (TR 16:30, açılıştan 1 saat önce); COMEX teminat değişiklikleri (30.01.2026 gümüş şoku); Çin tatilleri Asya seansını inceltir; ay sonu 30.11.2026 (B3a/B3b).

## 4. Notlar

GLD kopyası; doğrulanmış gecikmeli öncü yok.

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
