# KWEB — KraneShares CSI China Internet ETF

**TradingView:** `AMEX:KWEB` · **Aile:** Sektör ve tematik · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 594 | 16.0 | 168 | %-4.5 | 1.0 | 2016-11-07 |

**Kademe:** C — kural yok; sürücüleriyle takip  
**Neden izleme listesinde:** Doğrulanmış negatif gecikme: EEM güçlü yükseldiği günün ertesi KWEB brüt -14..-34 bp (FDR, IS/OOS negatif) -> long-only için 'alma/çık' kuralı. Gerçek zamanlı izleme: Hang Seng vadelisi. Likit (594 mn $).

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| FXI | `AMEX:FXI` | 0.88 | 1.22 |
| EEM | `AMEX:EEM` | 0.45 | 0.46 |
| SPY | `AMEX:SPY` | 0.41 | 0.81 |
| CPER | `AMEX:CPER` | 0.39 | 0.37 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| EEM | `AMEX:EEM` | negatif gecikme (kendi gecikmesi kontrollü) | 1 gün | EEM +1 sd -> KWEB ertesi gün ~-34..-37 bp. Kural: EEM 1g z>+1 -> ertesi gün KWEB brüt -34 bp (C0), -14 (O1), -25 (C1); IS -37 / OOS -62 bp net | -3.8 (-2.9/-2.7) | Long-only için 'alma/çık' kuralı (brüt etki maliyetin 1-2 katı). Kısa yön ancak ters ETF ile; bu ailede test edilmedi. | doğrulandı — Yeniden hesap: t -3.64 (IS -2.52 / OOS -2.70), -34 bp/sd; büyük günler hariç t -4.37; SPY(t) kontrolüyle -2.73. Kural EEM z>+1 -> KWEB C0 h1 brüt -30.5 bp, net -46.5 (t -3.73), IS -33.8 / OOS -59.4, 10 yılın 7'si negatif: maliyetten büyük. Mekanizma: EEM'in kendi ertesi gün dönüşü (EEM AR1 -0.13, t -2.47) beta ile KWEB'e taşınıyor (EEM(t+1) eşzamanlı kontrolüyle t +0.74). Long-only'de yalnız 'alma/çık' filtresi; ailede kısa araç yok. Bayat fiyat riski yok (KWEB 594 mn$/gün). |
| FXI | `AMEX:FXI` | negatif gecikme | 1 gün | FXI +1 sd -> KWEB ertesi gün -47 bp (ek test, FDR); OOS t -1.70 | -2.7 (-2.2/-1.7) | EEM ile aynı olgu; işlem kuralı EEM ile test edildi | zayıf — t -2.54, OOS -1.67; EEM ile aynı olgu. |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| Hang Seng vadelisi | `HKEX:HSI1!` | KWEB varlıklarının çoğu Hong Kong'da işlem görür: ABD kapalıyken (TR 04:15-11:10 + gece seansı) KWEB'in açılış boşluğunu doğrudan gösterir. |
| Hang Seng endeksi | `TVC:HSI` | Spot endeks; seans kapanışı. |
| USD/CNH | `FX:USDCNH` | Yuan zayıflığı Çin varlıklarında risk iştahını gösterir; 24 saat. |
| FTSE China A50 vadelisi (SGX) | `SGX:CN1!` | Çin anakara hisseleri; Asya saatlerinde. |

## 3. Takvim ve olay riskleri

Hong Kong tatilleri (KWEB işlem görür, dayanak kapalı: bayat NAV), Çin PMI (ayın 1'i), Ekim Altın Haftası, ABD-Çin ticaret/teknoloji kararları.

## 4. Notlar

Doğrulanmış gecikmeli öncü: EEM (negatif). Hang Seng vadelisi öncü değil, ABD kapalıyken KWEB'in fiyatlandığı piyasadır (açılış boşluğunun kaynağı).

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_sektor_tematik.md`, `notlar/denetim_sektor_tematik.md`.*
