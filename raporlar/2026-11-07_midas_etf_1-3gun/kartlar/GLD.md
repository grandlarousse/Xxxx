# GLD — SPDR Gold Shares

**TradingView:** `AMEX:GLD` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** kabul  
**Midas:** muhtemel

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 3,739 | 13.0 | 182 | %-10.3 | 1.0 | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** Altının ana aracı: 3,7 mlr $ medyan hacim, gidiş-dönüş ~13 bp (maliyet/1g oynaklık 0,07), grantor trust (PTP değil). S2 (ay sonu) ve S4 (IBS) adayları; gerçek zamanlı sürücü COMEX:GC1!.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt — tek başına işlem gerekçesi değil)

#### Ay sonu (turn-of-month) - altın (GLD)  
*İzlemede — zayıf kanıt · güven: dusuk · id: `metal_madenci_S2`*

- **Sinyal (t kapanışında):** S1 ile aynı takvim kuralı, işlem AMEX:GLD: ayın SON NYSE işlem günü kapanışında al, yeni ayın 3. işlem günü kapanışında sat. Gösterge yok. S1 ile AYNI etkidir (GLD-GDX 1y korelasyon 0,86); ikisini birlikte açmak aynı bahsi ikiye katlar.
- **Giriş:** C0: ayın son işlem günü TR ~23:45-23:59 (kış) / ~22:45-22:59 (yaz); MOC yok, piyasa ya da limit emir. O1 alternatifi: net 18,7 bp, t 1,19.
- **Tutuş / çıkış:** 3 işlem günü. — Yeni ayın 3. işlem günü kapanışında (TR ~23:45-23:59 kış) sat.
- **İşlem aracı:** GLD, IAU/GLDM (kopya) (sinyal: Takvim (NYSE); işlem AMEX:GLD)
- **Geçmiş (ajan):** n=111, net 39.9 bp/işlem (brüt 52.9), kazanma %56, t=2.45, IS 33.8 / OOS 45.4 bp, yılların %70'i pozitif, en kötü işlem -388 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500$):** C0: net 34 bp (t 2.2, n=117) · O1: net 17 bp (t 1.1, n=117) · C1: net 18 bp (t 1.0, n=117); 1.000$ pozisyonda ana mod net 16 bp (t 1.0)
- **Denetçi düzeltmesi:** Sayılar doğru. Ek: 2024-26 hariç 15,9 bp/t 0,90; en iyi 5 hariç 21,7/t 1,46; 1.000$ 21,9/t 1,34.
- **Denetim:** Birebir: n=111, brüt 52,9, net 39,9 bp, t 2,45, IS 33,8 (t 1,65) / OOS 45,4 (t 1,81), maxDD -%7,7. Sağlamlık: 2020 hariç t 1,97, 2022 hariç t 2,64; son gün girişinde h2-h6 t 1,8-2,7; kopyalarda aynı (takvim kuralı OHLC'den bağımsız olduğu için beklenen).
- **Denetçinin uyarıları:** S1 ile aynı etki (GLD-GDX 0,86) -> bağımsız kanıt değil; FDR geçmez; 2024-26 hariç 15,9 bp/t 0,90 (son üç yılın altın boğasına bağlı); en iyi 5 hariç 21,7/t 1,46; 1.000$'da 21,9/t 1,34; +10 bp kaymada t 1,83; O1 t 1,19, C1 t 1,30; permütasyon p 0,012; 2021-2023 üç yıl üst üste ≤0.
- **Giriş zamanı sağlamlığı:** C0: n=111, brüt 52.9 bp, net 39.9 bp, t 2.45; O1: n=111, brüt 31.7 bp, net 18.7 bp, t 1.19; C1: n=111, brüt 36.7 bp, net 23.7 bp, t 1.30
- **Maliyet duyarlılığı:** 1.000$: net 21.9 bp | 2.500$: net 39.9 bp | 10.000$: net 48.9 bp (2.500$ maliyeti 13.0 bp)
- **Not:** Tek ETF eşiğini geçer (t 2,45; IS 33,8/t1,65; OOS 45,4/t1,81; yılların %70'i pozitif; O1/C1 brüt 31,7/36,7 bp) ama FDR'yi geçmez. Yıl ortalaması çıkarılmış kenar 36,4 bp (t 2,28, yılların %90'ı pozitif); en iyi yıl (2025) hariç t 1,65. Etkinin bir kısmı ilk gece (C0 h1 31 bp vs O1 h1 9,5 bp). Düşük oynaklıklı (maxDD -%8) ve PTP'siz olduğundan S1'den daha sakin bir uygulama. (IS t=1.65, OOS t=1.81)
- Betik: `python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_metal_madenci/t5_adaylar.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| GDX (eşzamanlı sürücü, öncü değil) | `AMEX:GDX` | 0.86 | 0.49 |
| SLV (eşzamanlı sürücü, öncü değil) | `AMEX:SLV` | 0.84 | 0.37 |
| UUP (eşzamanlı sürücü, öncü değil) | `AMEX:UUP` | -0.42 | -1.82 |
| DFII10_d (eşzamanlı sürücü, öncü değil) | `FRED:DFII10` | -0.22 | -0.11 |
| FXE (eşzamanlı sürücü, öncü değil) | `AMEX:FXE` | 0.45 | 2.43 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| GDX | `AMEX:GDX` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | +10.9 bp / 1 sd öncü hareketi (h=1); GDX'in GLD'ye göre artığı ≥+1,5 sd kuralı: C0 h3 net 22 bp (t 1,29), O1 h1 negatif. | 2.4 (1.7/1.5) | doğrulanmadı (FDR yok; kural maliyet sonrası anlamsız) | zayıf — t 2,33, IS 1,52/OOS 1,58, 10,6 bp/sd < 13 bp maliyet; etkinin çoğu gece (t 2,16); FDR yok. |
| T10YIE_d | `FRED:T10YIE` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | +7.1 bp / 1 sd öncü hareketi (h=1); Veri kapanıştan sonra yayımlanır; O1/C1 kuralı negatif. | 2.8 (2.4/1.5) | maliyet altında (7 bp/sd < 13 bp) | denetlenmedi |
| DFII10_d | `FRED:DFII10` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | -4.3 bp / 1 sd öncü hareketi (h=1); IS ve OOS işaretleri ters (2022 kırılması). | -1.3 (-3.9/1.0) | kullanılamaz | denetlenmedi |
| UUP | `AMEX:UUP` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | +1.5 bp / 1 sd öncü hareketi (h=1); Eşzamanlı ters ilişki güçlü, gecikmeli yok. | 0.5 (0.5/0.5) | yok | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| COMEX altın vadeli (sürekli) | `COMEX:GC1!` | ~23 saat işler (TR kış 02:00-01:00); ETF kapalıyken oluşan hareket açılış boşluğunu gösterir. İzleme aracı, öncü değil. |
| Spot altın | `OANDA:XAUUSD` | Asya/Londra seansı; TR 12:00-17:30 arasında GLD açılışını önceden gösterir. |
| Dolar endeksi | `TVC:DXY` | Altınla eşzamanlı ters hareket (UUP corr_1y -0,42); gece/sabah değişimi açılış yönü için. |
| ABD 10y getiri / T-Note vadeli | `CBOT:ZN1!` | Faiz şokları (CPI/NFP 08:30 ET = TR 16:30 kış) açılıştan önce altına yansır. Alternatif: TVC:US10Y. |

## 3. Takvim ve olay riskleri

FOMC 09.12.2026 14:00 ET (TR 22:00; örneklemde FOMC sonrası altın zayıf, anlamsız); CPI 10.11 ve 10.12.2026, NFP 04.12.2026 08:30 ET (TR 16:30, açılıştan 1 saat önce); COMEX teminat değişiklikleri (30.01.2026 gümüş şoku); Çin tatilleri Asya seansını inceltir; ay sonu 30.11.2026 (S1/S2).

## 4. Notlar

Doğrulanmış gecikmeli öncü yok. Altın günlük frekansta ABD kapanışından sonra gelen bilgiye (Asya/Londra seansı) tepki verir: bu 'öncü' değil, gerçek zamanlı izlenecek açılış boşluğudur. Getirinin tamamına yakını gece oluşuyor (gece +5,1 bp/gün t 3,20; gün içi -0,6 bp).

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
