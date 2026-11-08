# KORU — Direxion Daily South Korea Bull 3X ETF

**TradingView:** `AMEX:KORU` · **Aile:** Uluslararası / ülke · **İzleme kararı:** yedek  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 405 | 26,5 | 1.104 | %-41,9 | 3,0x | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** EWY'nin 3x kaldıraçlısı (405 mn $, 26 bp). Kendi sinyali yok; EWY sinyaliyle (B4/B5) kaldıraçlı uygulama aracı. Midas'ta bulunurluk doğrulanmadı; 1 günlük oynaklık 1.100 bp, son 1 yılda en kötü gün -%42.

*Dayanak / ana araç kartı: `kartlar/EWY.md` (sürücüler ve gerçek zamanlı izleme listesi orada daha ayrıntılı).*

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt ya da yalnız filtre — tek başına işlem gerekçesi değil)

#### B5 — EWY gün sonu dip dönüşü (IBS<0,10 ve düşüş günü) — KEŞİFSEL  
*İzlemede — zayıf kanıt · güven: dusuk · aile kimliği: `uluslararasi_S2`*  
*Bu ETF'nin rolü: 3x araç (Midas doğrulanmadı, en fazla 1 gün)*

- **Sinyal (t kapanışında):** AMEX:EWY günlük mum: IBS = (close-low)/(high-low) < 0,10 VE close < close[1] ise EWY long (t kapanışı); t+1 kapanışında çık. Pine: ibs=(close-low)/(high-low); sig = ibs<0.10 and close<close[1]. İsteğe bağlı kaldıraçlı uygulama: sinyal EWY'den, işlem AMEX:KORU.
- **Giriş:** C0: EWY kapanışına ~5-10 dk kala (kış TR 23:50, yaz 22:50) gün içi düşük seviyeye çok yakın ve önceki kapanışın altında ise al. IBS kapanış fiyatına bağlı -> C0 iyimser; after-hours limit emriyle de denenebilir.
- **Tutuş / çıkış:** 1 işlem günü — t+1 kapanışına ~10 dk kala sat.
- **İşlem aracı:** EWY (sinyal: EWY)
- **Geçmiş (ajan):** n=214, net 42.1 bp/işlem (brüt 55.1), kazanma %56, t=2.93, IS 25.8 / OOS 52.9 bp, yılların %70'i pozitif, en kötü işlem -468 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500 $):** C0: net 100 bp (t 2,5, n=225) · O1: net 33 bp (t 1,3, n=225) · C1: net -16 bp (t -0,4, n=212); 1.000 $ pozisyonda ana mod net 82 bp (t 2,1)
- **Denetçi düzeltmesi:** Ajanınkiyle aynı; ek: 2026 hariç net 21,4 bp t 1,70; 2020+2026 hariç 12,4 bp t 0,95; en iyi 10 hariç 13,1 bp t 1,15; +10 bp kayma t 2,23; f=0,10 kapanış öncesi vekili t 1,69.
- **Denetçi kural düzeltmesi:** Strateji olarak önerilmez; keşifsel izleme. İleride yalnız 2027+ verisinde, kural değişmeden test edilmeli.
- **Denetim:** BİREBİR: n=214, brüt 55,12, net 42,12 bp, t 2,93, IS 25,8 (t 1,29) / OOS 52,9 (t 2,33), yıl+ 0,70, en kötü -468 bp; O1 net 4,9, C1 brüt 0,75 bp. IBS kendi hesabımla; ham EWY h/l verisinde eksik/0 yok. Sağlamlık: Lehte: IBS eşiği 0,05-0,20 aralığında plato (t 2,4-3,7); yıl-tabakalı permütasyon p=0,0014 (yalnız seçim sonrası tek test için geçerli); EWY'nin negatif 1 günlük otokorelasyonu (IS -0,16 / OOS -0,12) eşzamansızlık mekanizmasını (B4 ile aynı) destekliyor. Aleyhte: çoklu test, IS anlamsız, aile tekrarı yok, 2026 bağımlılığı.
- **Denetçinin uyarıları:** 20.196 satırlık taramadan seçildi (Bonferroni p<2,5e-6 gerekir); IS t 1,29 (anlamsız); 2026 (21 işlem, ort. +232 bp) hariç net 21 bp t 1,70; 2020+2026 hariç 12 bp t 0,95; en iyi 10 işlem hariç t 1,15; aynı kural kardeş Asya ETF'lerinde negatif (EWT -7,7, EWJ -4,3, EWA -4,8, INDA -6,8 bp); C1 brüt ~0 -> tamamen kapanışa bağımlı; 1.000$ t 1,68; kapanış öncesi giriş vekili f=0,10 t 1,69; B4 ile çakışmayan işlemler net 19 bp (t 1,42). 2026'da EWY günlük oynaklığı 403 bp (2017-2025: 100-256) -> sonuç tek bir rejime bağlı.
- **Giriş zamanı sağlamlığı:** C0 brüt 55 bp / O1 18 bp (net 5) / C1 1 bp. Kenar neredeyse tamamen gece boşluğunda: KAPANIŞA BAĞIMLI.
- **Maliyet duyarlılığı:** Net: 1.000$ 24.1 bp; 2.500$ 42.1 bp; 10.000$ 51.1 bp (brüt 55.1, maliyet 13 bp).
- **Not:** Kabul eşiğini biçimsel olarak geçiyor (t 2.93, IS 26 / OOS 53 bp, yılların %70'i pozitif, n=214, O1 brüt > 0) ama tarama içinden seçildi ve FDR'yi geçmiyor. Getirinin yarıdan fazlası 2026'dan (21 işlem, ort. +232 bp) ve 2020'den; 2020 ve 2026 hariç net ~+12 bp. KORU (EWY sinyaliyle) C0 h=1 net 99 bp (t 2.39), en kötü -1397 bp. B4 ile EWY'de çakışabilir (aynı gün iki sinyal = tek pozisyon).
- Betik: `/home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_uluslararasi/strateji_S2_ewy_ibs.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| EWY (dayanak) | `AMEX:EWY` | 0.99 | 3.01 |
| EEM | `AMEX:EEM` | 0.93 | 6.43 |
| SMH | `NASDAQ:SMH` | 0.83 | 3.54 |
| XLK | `AMEX:XLK` | 0.79 | 5.04 |
| QQQ | `NASDAQ:QQQ` | 0.78 | 6.63 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| SPY koşullu kuralı (B4: SPY<=-%1,5 ve ETF<=SPY) | `AMEX:SPY` | koşullu eşik; doğrusal testte doğrulanmadı | t+1 | Koşul EWY'de sağlandığında KORU ertesi gün brüt 283 bp (n=68); en kötü -3188 bp | 1.9 (—/—) | KORU için 2.500$'da net 257 bp (IS 122 / OOS 369); t<2 -> eşik altında | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| KOSPI (seans TR 03:00-09:30) | `KRX:KOSPI` | EWY açılış boşluğunu belirleyen yerel seans |
| Nasdaq 100 vadelisi | `CME_MINI:NQ1!` | gece yön; yarı iletken ağırlığı |
| S&P 500 vadelisi | `CME_MINI:ES1!` | gece risk iştahı |

## 3. Takvim ve olay riskleri

ABD: CPI 10 Kas, NFP 4 Ara, CPI 10 Ara, FOMC 9 Ara 2026 (Asya'ya ertesi sabah yansır); NYSE 26 Kas kapalı, 27 Kas/24 Ara erken kapanış (TR 21:00). Yerel tatillerde ETF NAV'sız işlem görür. Kore: Seollal (Şub 2027 başı), çeyreklik vade 10 Ara 2026; KORU'da 3x günlük yeniden dengeleme.

## 4. Notlar

Doğrulanmış (doğrusal) gecikmeli öncü YOK: aile içi BH-FDR geçen çift yok. En güçlü aday (FDR'siz): TIP h1 t=2.40 (IS 2.05/OOS 1.37), h3 t=2.93. Sürücüler eşzamanlıdır, öncü değildir. SPY satırı B4'ün koşullu kuralıdır, doğrusal öncü değildir. Reel faiz düşüşü (FRED:DFII10) 3 gün ufkunda pozitif aday (IS/OOS aynı işaret, FDR yok).

---
*Kural kodları (A1, A2, B1-B10, F) RAPOR.md ile aynıdır. Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_uluslararasi.md`, `notlar/denetim_uluslararasi.md`.*
