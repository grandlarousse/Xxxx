# GDXJ — VanEck Junior Gold Miners ETF

**TradingView:** `AMEX:GDXJ` · **Aile:** Değerli/sanayi metalleri ve madenciler · **İzleme kararı:** kabul  
**Midas:** doğrulanamadı (uygulamada sembolü arayarak kontrol edin)

| Medyan günlük işlem (mn $) | Gidiş-dönüş maliyet, 2.500$ (bp) | Günlük oynaklık (bp, 1y) | Son 1 yılda en kötü gün | Kaldıraç | Veri başlangıcı |
|---|---|---|---|---|---|
| 563 | 14.0 | 357 | %-13.6 | 1.0 | 2016-11-07 |

**Kademe:** B — kural var ama kanıt zayıf (küçük boyut / kağıt üstünde izle)  
**Neden izleme listesinde:** 563 mn $, ~14 bp, oynaklık 356 bp. Ailenin en güçlü adayı S3 (IBS dip alımı) bu ETF'de.

## 1. Ne zaman girilir?

Bu ETF için denetimden geçmiş (doğrulanmış) bir 1-3 günlük giriş kuralı yok.

### İzlemede (zayıf kanıt — tek başına işlem gerekçesi değil)

#### Genç altın madencileri IBS dip alımı (GDXJ)  
*İzlemede — zayıf kanıt · güven: orta · id: `metal_madenci_S3`*

- **Sinyal (t kapanışında):** AMEX:GDXJ günlük (1D) mum. IBS = (close - low) / (high - low). Sinyal: high > low VE IBS < 0.10 VE close < close[1]. Pine: ibs=(close-low)/(high-low); sinyal = high>low and ibs<0.10 and close<close[1]. Sinyal ve işlem AMEX:GDXJ; kaldıraçlı alternatif AMEX:JNUG (sinyal yine GDXJ mumundan). Pozisyon açıkken gelen yeni sinyaller yok sayılır.
- **Giriş:** C0: sinyal günü kapanıştan önce TR ~23:45-23:55 (kış) / ~22:45-22:55 (yaz) anlık fiyatla IBS'yi hesapla (fiyat günün dibine çok yakın ve dünkü kapanışın altında) -> piyasa/limit emir. Kapanışta kaçırılırsa ertesi gün açılışta al (O1, TR 17:30 kış / 16:30 yaz): O1 sürümü de güçlü (net 72 bp, t 2,74).
- **Tutuş / çıkış:** 3 işlem günü. — Girişten sonraki 3. işlem günü kapanışında (TR ~23:45-23:59 kış) sat; stop/erken çıkış yok.
- **İşlem aracı:** GDXJ, JNUG (kaldıraçlı, Midas'ta doğrulanmadı) (sinyal: AMEX:GDXJ (kendi mumu))
- **Geçmiş (ajan):** n=240, net 107.2 bp/işlem (brüt 121.2), kazanma %56, t=3.39, IS 85.4 / OOS 127.6 bp, yılların %80'i pozitif, en kötü işlem -855 bp
- **Ana ajan son kontrolü (düzeltilmiş veri, 2.500$):** C0: net 102 bp (t 3.4, n=253) · O1: net 68 bp (t 2.7, n=253) · C1: net 24 bp (t 0.7, n=235); 1.000$ pozisyonda ana mod net 84 bp (t 2.8)
- **Denetçi düzeltmesi:** Ajanın sayıları doğru. Eklenmesi gerekenler: O1 h1..h5 net 9/27/72/44/61 bp (t 0,68/1,39/2,74/1,15/1,50); C1 h3 31 bp/t 0,93; madenci havuzu IS 14 bp/t 0,51, OOS 113/t 3,45; FDR: tek yönlü GEÇMEZ (iki yönlü 'geçer' kullanılmamalı); güven 'orta' -> 'düşük-orta (zayıf)'.
- **Denetçi kural düzeltmesi:** Kural aynı, 'KAPANIŞA BAĞIMLI' etiketiyle: AMEX:GDXJ IBS<0,10 & close<close[1]; kapanıştan 5-10 dk önce anlık fiyatla kontrol, limit emir (son fiyat +1-2 sent; panik günlerinde piyasa emri verme); 3. kapanışta çık. Aynı gün S4 (GLD IBS) ya da S1/S2 (ay sonu) tetiklenirse ek pozisyon açma (aynı bahis). Küçük pozisyon (maxDD -%26, tek işlem -%8,5); JNUG yalnız Midas bulunurluğu doğrulanırsa ve yarım boyutla.
- **Denetim:** Bağımsız motorla (lib.trades/evaluate kullanılmadan, kod/denetim_metal_madenci/motor.py + d1_yeniden.py) birebir: n=240, brüt 121,2, net 107,2 bp, t 3,39, IS 85,4 (t 1,82) / OOS 127,6 (t 2,99), yıl+ 0,80, PF 1,86, maxDD -%26,2, en kötü -855 bp; 240 işlemin tarihleri ve brüt getirileri ajanınkiyle aynı (fark <1e-16). İleriye bakma yok (IBS ve close<close[1] t barından; C0 girişi aynı kapanış -> kapanışa bağımlı; çıkış t+3 kapanışı; çakışma ve maliyet doğru). Tarihsel likiditeyle maliyet: 106,6 bp/t 3,38; katı çakışma n=222, t 3,28; 200 günlük ısınma kaldırılınca n=258, 103 bp, t 3,34. Sağlamlık: Geçti: 2020 hariç 81,6 bp/t 2,76; 2022 hariç t 3,22; 2020+2022 hariç 80,9/t 2,54; 2024-26 hariç 74/t 2,04; en iyi 5 işlem hariç 70,3/t 2,65; rastgele giriş permütasyonu 5.000 tekrar p=0,0004 (yıl tabakalı p=0,0002; rastgele ort 23-25 bp); 1.000$ (32 bp) 89 bp/t 2,82; 10.000$ 116/t 3,68; +10 bp kayma 97/t 3,08; C0 h1-h5 hepsi t>2,2; JNUG ile 173 bp/t 2,70 (maxDD -%51). Kaldı: FDR/Bonferroni; IS t 1,82<2; eşik ≥0,125'te IS t<0,5; O1/C1 h komşulukları; madenci havuzu IS t 0,51.
- **Denetçinin uyarıları:** (1) Çoklu test: 8.316 aile satırında 1. sıra; tek yönlü p≈0,0004, BH (10.049 test, eşik ~6,7e-5) ve Bonferroni altında GEÇMEZ; 'iki yönlü BH'de geçer' ifadesi anlamsız (eşiği maliyet yüzünden anlamlı negatif çıkan testler gevşetiyor). (2) IS kanıtı yalnız seçilen ETF'de: aynı kural IS'te GDX -3 bp, RING -11, SILJ -50; madenci havuzu IS 14 bp/t 0,51 (OOS 113/t 3,45); OOS da seçimde görülmüş veri (tam örneklem t'siyle seçildi). (3) Eşik komşuluğu IS'te çöküyor: 0,125 -> IS t 0,49; 0,15 -> 0,32; 0,20 -> 0,28 (OOS her eşikte 2,7-3,3): 2022-2026 madenci rejimine özgü. (4) 'O1'de de güçlü' abartı: O1 h1..h5 t 0,68/1,39/2,74/1,15/1,50 (sivri tepe); C1 h3 t 0,93; C0 kenarının ~1/3'ü sinyal gecesinde (33,7 bp vs koşulsuz 10,5) -> 'kapanışa bağımlı' etiketlenmeli; Midas'ta MOC yok, sinyal 5-10 dk önceki fiyatla tahmin edilir (yanlış sınıflandırma gün içi veri olmadan ölçülemedi). (5) En büyük kazanç 12.03.2020 (+%33,7): GDXJ -%26,3 kapanırken GDX -%11,4, JNUG'dan çıkan endeks ~-%20,5 -> kapanış NAV'a göre ~%6-7 iskontolu; ertesi açılış +%18,8; gerçek olay ama o gün 2 bp makas varsayımı geçersiz. (6) S4 sinyallerinin %52'si S3 ile aynı gün (getiri korelasyonu 0,81); S3 kenarı GLD de zayıf kapandığında yoğun (GLD IBS<0,2: 147 bp/t 3,09; diğer: 63 bp/t 1,55). (7) IBS etkisi geniş hisse ETF olgusu (genel_tum'da ETF'lerin %84'ünde kenar>0, QQQ t 3,68): ön kanıt var ama GDXJ büyüklüğü seçimle şişmiş.
- **Giriş zamanı sağlamlığı:** C0: n=240, brüt 121.2 bp, net 107.2 bp, t 3.39; O1: n=240, brüt 86.2 bp, net 72.2 bp, t 2.74; C1: n=222, brüt 45.3 bp, net 31.3 bp, t 0.93
- **Maliyet duyarlılığı:** 1.000$: net 89.2 bp | 2.500$: net 107.2 bp | 10.000$: net 116.2 bp (2.500$ maliyeti 14.0 bp)
- **Not:** Ailenin en güçlü sonucu: n=240, net 107 bp, t 3,39, IS 85 (t1,82) / OOS 128 (t2,99), yılların %80'i pozitif; O1'de de güçlü (t 2,74), komşu h: h1 t2,81, h2 t2,48; yıl ortalaması çıkarılmış kenar 98 bp (t 3,14); en iyi yıl (2020) hariç t 2,76; 30.01.2026 şoku hariç 102 bp (t 3,23). C1'de zayıf (31 bp, t 0,93): sinyalden sonra bir gün beklemek kenarın çoğunu kaçırır. FDR: iki yönlü BH'de geçer, tek yönlü BH'de geçmez. Uyarılar: genel taramada (31 sinyal x 9 kombinasyon x 28 ETF) en iyiler arasından geldiği için seçim yanlılığı var; geniş madenci havuzunda IS dönemi zayıf; boğa piyasasında (2024-2026) dip alımı. JNUG ile: net 173 bp, t 2,70, maxDD -%51, en kötü işlem -%21. (IS t=1.82, OOS t=2.99)
- Betik: `python3 -I /home/user/Xxxx/raporlar/2026-11-07_midas_etf_1-3gun/kod/ajan_metal_madenci/t5_adaylar.py`

## 2. Lead-lag

### Eşzamanlı sürücüler (aynı gün birlikte hareket eder — öncü değildir)

| Sürücü | TradingView | corr (1y) | beta (1y) |
|---|---|---|---|
| GDX (eşzamanlı sürücü, öncü değil) | `AMEX:GDX` | 0.99 | 1.10 |
| GLD (eşzamanlı sürücü, öncü değil) | `AMEX:GLD` | 0.86 | 1.68 |
| SLV (eşzamanlı sürücü, öncü değil) | `AMEX:SLV` | 0.82 | 0.70 |

### Gecikmeli öncüler (bugünkü hareketi sonraki 1-3 günde bu ETF'ye yansıyan)

| Öncü | TradingView | Tür | Ufuk | Ne beklenir | t (IS/OOS) | Maliyet sonrası | Denetim |
|---|---|---|---|---|---|---|---|
| GLD | `AMEX:GLD` | yetişme (beta60*r_L(t) - r_T(t) -> r_T(t+1..t+1)) | 1 gün | -3.5 bp / 1 sd öncü hareketi (h=1); Kendi gecikmesi kontrollü t -0.74. | -0.2 (-0.1/-0.4) | yok | denetlenmedi |
| LQD | `AMEX:LQD` | gecikmeli (r_L(t) -> r_T(t+1..t+1), kendi gecikmesi kontrollü) | 1 gün | +41.9 bp / 1 sd öncü hareketi (h=1); IS 3,42 / OOS ~0. | 2.6 (3.4/-0.0) | kullanılamaz | denetlenmedi |

### Gerçek zamanlı izlenecekler (ETF kapalıyken işler; açılış boşluğunu önceden gösterir)

| Gösterge | TradingView | Neden |
|---|---|---|
| COMEX altın vadeli | `COMEX:GC1!` | Madencilerin ana sürücüsü (GDX-GLD 0,86, beta 1,53); gece hareketi madenci açılışına ~1,5x yansır. |
| COMEX gümüş vadeli | `COMEX:SI1!` | İkincil sürücü (GDX-SLV 0,81). |
| S&P 500 e-mini | `CME_MINI:ES1!` | Madenciler hisse olduğu için genel risk iştahı; açılış öncesi yön. |

## 3. Takvim ve olay riskleri

FOMC 09.12.2026 14:00 ET (TR 22:00; örneklemde FOMC sonrası altın zayıf, anlamsız); CPI 10.11 ve 10.12.2026, NFP 04.12.2026 08:30 ET (TR 16:30, açılıştan 1 saat önce); COMEX teminat değişiklikleri (30.01.2026 gümüş şoku); Çin tatilleri Asya seansını inceltir; ay sonu 30.11.2026 (S1/S2). Ek: madenci bilanço dönemleri (Şub, Nis-May, Tem-Ağu, Eki-Kas).

## 4. Notlar

Doğrulanmış gecikmeli öncü yok; S3 (IBS) kendi fiyatına dayalı bir ortalamaya dönüş kuralıdır, öncü değildir.

---
*Geçmiş performans geleceği garanti etmez. Yatırım tavsiyesi değildir. Kaynak: `notlar/aile_metal_madenci.md`, `notlar/denetim_metal_madenci.md`.*
