# e1_etf_zaman_takvim — Midas cephesi: altın/gümüş/madenci ETF'lerinin kendi zaman serisi ve takvim yapısı

Tarih: 2026-11-07. Ufuk: 1, 3 ve 5 NYSE işlem günü, ABD kapanışından kapanışına (16:00 ET). Karar anı gün t 15:00 ET (`cut_utc`).
IS = 2008–2017, OOS = 2018–2026-11, ayrıca 2022+ alt dönemi. Hedefler: GLD (ana), IAU, GLDM, GDX, GDXJ, SLV; kaldıraçlı UGL, NUGT, JNUG; ters GLL, DUST, JDST, ZSL.

---

## 0. Kısa sonuç

1. **Toplam tablo gürültüden ayırt edilemiyor.** 1.046 öngörücü/kural testinin 42'sinde |t|≥2 çıktı. Sıfır hipotezi altında yaklaşık 48 beklenirdi. |t|≥3 olan 4 test var, beklenen yaklaşık 2,8. Benjamini-Hochberg ile en küçük q = 0,52. Hiçbir test %10 FDR'yi geçmiyor. Aşağıdaki "en iyi" bulgular bu arka plana göre okunmalı.
2. **GLD'nin kendi fiyatından türeyen kurallar işe yaramıyor.** Bu kurallar momentum (1–250 gün), MA filtreleri, Donchian, RSI(2)/Connors, Bollinger, ardışık seriler ve >2σ günlerdir. Trend filtreleri (P>SMA200, SMA50>SMA200, 12 aylık momentum) al-tut Sharpe'ını aşmıyor (GLD tam dönem 0,48–0,52 vs al-tut 0,52). Drift çıkarılmış Sharpe ≈ 0 (−0,03 ile 0,09 arası). IS'te seçilen 126 kuralın yalnız 62'si OOS'ta aynı işareti korudu, yani yazı-tura düzeyi.
3. **GLD getirisinin neredeyse tamamı gece oluşuyor.** Kapanış→açılış getirisi yılda %9,0 (t=3,0; OOS %14,1, t=3,4). Açılış→kapanış ≈ 0 (−%1,1/yıl). Ancak "kapanışta al, açılışta sat" yılda 252 gidiş-dönüş gerektiriyor. Başabaş maliyet GLD'de işlem başına 4–7 bps. 10 bps temel maliyetle net getiri −%10/yıl (OOS). **Uygulanamaz.** Madencilerde de başabaş 8–12 bps, yani maliyet sonrası yine sıfırın altında.
4. **Bu cephedeki tek tutarlı aday madenci takvimi.** GDXJ/GDX'i **ayın ilk işlem günü** ve **NYSE tatilinden önceki son işlem günü** 1 gün tutmak:
   - GDXJ: tam dönem t=4,25, IS 2,62, OOS 3,41. Yıllık P&L 18 yılın 17'sinde pozitif.
   - Yalnız uzun, 10 bps maliyetle OOS net Sharpe 1,08 (stres maliyette 0,93), yılda yaklaşık 19 gidiş-dönüş.
   - GDX'te tatil öncesi etkisi aynı gün SPY getirisi kontrol edildikten sonra da duruyor (t=2,55).
   - Ancak bu sepet tam örneklem takvim tablosuna bakıldıktan sonra kuruldu. Bileşenlerin global FDR q'su 0,52. Bu yüzden etiket **ORTA**, YÜKSEK değil.
5. **Kısa bacak yok.** Ters ETF'li (GLL/DUST/JDST/ZSL) sürümler hiçbir kuralda yalnız uzun sürümü OOS'ta anlamlı biçimde geçmedi. IS'te 3x DUST/JDST aşınması yüzünden çoğu daha kötü. Midas'ta açığa satış yokluğu pratikte bir kayıp değil, çünkü kısa tarafta kenar bulunamadı.
6. **Kaldıraçlı ETF'ler 1–5 günde nominal kaldıracı iyi izliyor ama pahalı.** UGL'nin 1/3/5 günlük gerçekleşen kaldıracı 2,00/2,02/2,01. Buna karşılık 2×GLD'ye göre yıllık −%6,9 kaybediyor (oynaklık aşınması −%3,0 + ücret/finansman −%3,9). NUGT 2x döneminde yılda −%20 (5 günde −40 bps); 3x döneminde −%53.
7. **ETF seçimi:** 1–5 günlük işlem için GLD ≈ IAU ≈ GLDM. Fark gider oranında: 5 günlük tutuşta GLD 0,8 bps, GLDM 0,2 bps. Fiyat kademesi (1 sent) farkı: GLD 0,25 bps, GLDM/IAU ~1,2 bps. İkisi de 10 bps'lik Midas maliyetinin yanında küçük. Likidite çok farklı: GLD günde 3,7 milyar $, GLDM 0,42 milyar $. Uzun tutuşta GLDM, kısa vadeli ve büyük tutarlı işlemde GLD.

---

## 1. Veri, zaman ve yöntem

**Hedef.** `fwd_h = log(c_{t+h}) − log(c_t)`, temettü düzeltmeli kapanış (`c_*` = Yahoo adjclose). Giriş gün t kapanışı, çıkış t+h kapanışı.

**Bilgi zamanları:**

| Öngörücü | Kaynak | Bilgi zamanı (ET) | UTC (yaz / kış) | Kullanım |
|---|---|---|---|---|
| ETF kendi kapanışı t-1 ("strict": mom, MA, Donchian, RSI2, Bollinger, seri, σ) | Yahoo adjclose | t-1 16:00 | t-1 20:00 / 21:00 | gün t sinyali |
| GLD'nin 15:00 ET tahmini fiyatı p15 = c_{t-1}·xau_cut_t/xau_close_{t-1} ("nc") | Dukascopy spot | t 15:00 | t 19:00 / 20:00 | gün t sinyali. p15 hareketi ile GLD gün getirisinin korelasyonu 0,98 |
| SLV için XAG 15:00 ET (cut-cut) ("nc") | Dukascopy (2016+) | t 15:00 | t 19:00 / 20:00 | gün t sinyali; IS yalnız 2016–17 |
| Açılış boşluğu gece_t = log(açılış_t / kapanış_{t-1}) | Yahoo open | t 09:30 | t 13:30 / 14:30 | gün t sinyali |
| gece_{t-1}, gün içi_{t-1} | Yahoo | t-1 16:00 | t-1 20:00 / 21:00 | gün t sinyali |
| Takvim (haftanın günü, ay, tatil, 3. Cuma, COMEX OG vadesi, GC ilk bildirim) | takvim | önceden | — | giriş = olay gününden önceki kapanış |
| FOMC kararı (2013+ 14:00; 2009–12 14:15; 2011–12 basın toplantılı 12:30) | federalreserve.gov | t 14:00 | t 18:00 / 19:00 | FOMC günü getirisi için giriş önceki kapanış. Tepki sinyali (15:00 ET'ye kadar hareket) karar anından önce |
| CPI / NFP | BLS | t 08:30 | t 12:30 / 13:30 | aynı mantık |
| GLD NAV t-1 (prim testi) | SSGA | t-1 akşam (varsayım 23:00 UTC) | — | gün t sinyali |
| Saatlik 10:30 ET, 5 dk 09:35 ET, ön seans | Yahoo saatlik/5 dk | — | — | **yalnız dolum gerçekçiliği**, sinyal değil |

**Yöntem kuralları:**
- Örtüşen getirilerde Newey-West lag = max(h, 5).
- Sürekli öngörücülerde Spearman IC ve sıra dönüşümlü NW t (`split_stats`).
- Kurallarda (±1/0) ham getiri ~ sinyal NW regresyonu (`rstats`).
- Yıl yıl işaret tutarlılığı: yıllık korelasyonun işareti.

**Backtest:**
- Pozisyon gün t kapanışında alınır ve h gün tutulur. 1/h kademeli uygulama, basit getiriler.
- Maliyet = |Δağırlık| × tek yön (RT/2).
- Temel/stres gidiş-dönüş maliyeti: GLD/IAU/GLDM/GDX/GDXJ/SLV 10/20 bps; kaldıraçlı/ters 20/40 bps.

**Sürümler:**
- (i) `ideal_ls`: açığa satış serbest. Midas'ta yok, yalnız kıyas için.
- (ii) `long_only`: yalnız uzun, değilse nakit (nakit getirisi 0 varsayıldı, muhafazakâr).
- (iii) `inv_*`: kısa sinyalde ters ETF'te beta eşleştirmeli uzun. GLL/ZSL ağırlığı 0,5. DUST/JDST ağırlığı 2020-04 öncesi 1/3, sonrası 0,5.
- (iv) `lev_*`: aynı sinyal kaldıraçlı uzun ETF'te, tam nominal (UGL, NUGT, JNUG, AGQ).
- `*_demeaned`: hedef getiriden örneklem ortalaması çıkarılmış Sharpe (drift tuzağı kontrolü).
- Her tabloda al-tut Sharpe'ı aynı pencerede verildi.

**Direxion kaldıraç değişimi.** NUGT/DUST/JNUG/JDST 3x'ten 2x'e geçti. Veride geçiş 24.03–01.04.2020 arasında görülüyor, kesim 2020-04-01 alındı.

**IS seçimi.** Parametreli ailelerde parametre IS |t|'ye göre seçildi ve OOS tek sefer değerlendirildi (`a_is_secim.csv`). Takvim ve "aşırı satım" ızgarasında tanımlar literatürden sabit. Seçim etkisi ayrıca tartışılıyor (bölüm 2 ve 8).

**Kayıt.** Her test `register(agent='e1_etf_zaman_takvim')` ile kaydedildi: toplam **1.102 kayıt**, 30 aile, yineleme yok. Betimsel ve aşınma testleri ile `f_final` yinelemeleri çıkarılınca **1.046 öngörücü/kural testi** kalıyor.

---

## 2. Çoklu test: toplam tablo

| Ölçüt | Gözlenen | Sıfır altında beklenen |
|---|---|---|
| Öngörücü/kural testi | 1.046 | — |
| \|t\| ≥ 2 | 42 | ≈ 48 |
| \|t\| ≥ 3 | 4 | ≈ 2,8 |
| BH-FDR en küçük q | 0,52 | — |
| IS'te seçilen kural (a ailesi, 126 adet) OOS'ta aynı işaret | 62 (%49) | %50 |
| IS'te seçilen kural OOS aynı işaret ve \|t_oos\|≥2 | 4 | ≈ 3 (%2,5) |

Testler birbirine bağımlı (GLD strict ile nc, h=1/3/5 örtüşmesi). Etkin test sayısı daha düşük, ama sonuç değişmiyor: **bu ailede sistematik bir öngörü gücü kanıtı yok.** Öne çıkan birkaç sonuç önsel mekanizması olan madenci takvim etkileri. Bunlar ancak önsel kanıta dayanarak ciddiye alınabilir. Tüm 1.102 kayıt üzerinden yapılan FDR, aşınma ve gece testleri gibi kesin anlamlı betimsel testler yüzünden daha iyimser görünüyor (GDXJ ilk gün q=0,055). Bu sayı yanıltıcı, karar için öngörücü-yalnız FDR esas alındı.

---

## 3. (a) Zaman serisi kuralları (612 + 40 bacak + 96 ızgara + 2 Connors testi)

**Momentum/dönüş (Spearman IC):**
- GLD `mom250` h=1: IC 0,044, t=2,92 (IS 1,53, OOS 2,25). Ancak **yalnız 4/18 yılda** pozitif. Etki yıllar arası seviye farkından geliyor: boğa yıllarında hem 12 aylık momentum hem getiri yüksek. Yıl içinde öngörü yok, placebo kaydırmalarında IC sabit (~0,044). **Drift artefaktı.**
- GLD kısa vade dönüşü (15:00 ET hareketi, h=1): IC −0,031, t=−2,07, 15/19 yıl. Ancak işaret kuralının uzun ve kısa bacak farkı yalnız 2,7 bps/gün (t=0,78). Yılda 65 gidiş-dönüş maliyetle drift çıkarılmış Sharpe −0,38. **Ölü.**
- Madenciler 5–60 günde zayıf dönüş eğilimi gösteriyor: IC −0,03 ile −0,05, 13–17/19 yıl aynı işaret, ama |t| < 1,9.

**Trend filtreleri (yalnız uzun, 10 bps, h=5):**

| Kural | tam | IS | OOS | 2022+ | drift çıkarılmış (tam/OOS) | al-tut (tam/OOS) |
|---|---|---|---|---|---|---|
| GLD P>SMA200 | 0,52 | 0,29 | 0,74 | 0,92 | 0,09 / 0,05 | 0,52 / 0,81 |
| GLD SMA50>SMA200 | 0,49 | 0,29 | 0,68 | 0,74 | 0,06 / −0,00 | 0,52 / 0,81 |
| GLD 12 ay momentum>0 | 0,48 | 0,27 | 0,67 | 0,81 | 0,06 / −0,02 | 0,52 / 0,81 |
| GDX P>SMA200 | 0,13 | −0,03 | 0,28 | 0,54 | −0,08 / −0,22 | 0,30 / 0,61 |
| SLV 12 ay momentum>0 | 0,40 | 0,41 | 0,41 | 0,58 | 0,14 / −0,01 | 0,35 / 0,53 |

Trend filtreleri yalnız düşüşü kısaltıyor: GLD MDD −%36'ya karşılık al-tut −%46. Zamanlama değeri yok. GDX'te trend filtresi ters çalışıyor: SMA200 altındayken sonraki 5 gün daha iyi, 16/18 yıl, ama t=−1,2.

**RSI(2)/Connors (GLD):**
- Klasik Connors kuralı (RSI2<10 ve P>SMA200 al, P>SMA5 olunca sat; 15:00 ET kararıyla): yalnız uzun Sharpe 0,26/0,29 (tam/OOS), drift çıkarılmış 0,09/0,04. Kısa simetriği GLL ile −0,04.
- RSI2<10&SMA200, h=3: OOS −0,01.
- **İnternetteki "GLD'de RSI(2) çalışır" iddiaları bizim veride tutmuyor.**

**Bollinger/seri/2σ:**
- GDXJ Bollinger dönüşü (±2σ, h=5): t=2,42. IS 0,46 iken OOS 3,15, yani etki 2018 sonrası ortaya çıkmış.
- GLD BollZ<−2 sonrası 5 gün: +64 bps (koşulsuz 5 günlük ortalama 15 bps), t=2,04 (IS 0,90, OOS 2,52), 16/19 yıl. OOS net Sharpe 0,70, yılda 2,2 gidiş-dönüş. Izgaradan seçildiği için **DÜŞÜK–ORTA**.
- >2σ gün sonrası: altında da madencide de anlamlı dönüş veya devam yok. Caporale-Plastun (2020) sonucuyla uyumlu.

**Madenci "aşırı satım" ızgarası** (8 tanım × 3 ufuk, yalnız uzun bacak; `a_oversold_grid.csv`):
- OOS'ta GDX ve GDXJ'de 8 tanımın neredeyse hepsi pozitif (h=3/5'te 8/8). IS'te karışık, GDXJ'de çoğu negatif.
- En güçlüsü GDX 5 gün üst üste düşüş → 1 gün tut: +77 bps, t=3,43 (IS 2,07, OOS 2,98, 2022+ 3,03), 15/18 yıl. Sinyal günü yalnız 90, GDXJ'de tekrar etmiyor (t=0,17). GLD ve SLV'de dönüş yok (SLV'de 3 gün düşüş sonrası hafif devam).
- **ORTA** (ızgara seçimi + tek ETF).

**Ters ETF'li sürümler:** Bollinger ve seri kurallarında `inv_DUST`/`inv_JDST` IS Sharpe'ı negatif (−0,05 ile −0,53), OOS ≈ yalnız uzun. Kısa bacak (üst bant üstü → GDX 5 gün −78 bps, t=−2,36) DUST'un aşınmasıyla birlikte kâra dönmüyor.

---

## 4. (b) Gece ve gün içi ayrışımı

Yıllık toplam log getiri (%). Gece: kapanış t-1 → açılış t (temettü gece bacağında). Gün içi: açılış → kapanış.

**GLD** — 19 yılın 14'ünde gece pozitif, 13'ünde gece > gün içi:

| | 2008 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gece | 12,0 | 19,2 | 20,4 | 15,1 | −2,1 | −27,7 | −2,6 | −8,7 | 17,1 | 2,7 | 4,4 | 12,2 | 27,6 | 1,8 | −5,9 | 10,0 | 24,2 | 39,6 | 10,2 |
| gün içi | −10,1 | 2,4 | 5,3 | −6,0 | 8,5 | −5,6 | 0,4 | −2,6 | −9,3 | 9,4 | −6,3 | 4,2 | −5,4 | −6,1 | 5,1 | 1,9 | −0,5 | 9,7 | −16,4 |
| toplam | 1,9 | 21,5 | 25,7 | 9,1 | 6,4 | −33,3 | −2,2 | −11,3 | 7,7 | 12,1 | −2,0 | 16,4 | 22,2 | −4,2 | −0,8 | 11,9 | 23,6 | 49,3 | −6,2 |

**GDX** — gece 17/19 yıl pozitif; gün içi 2008–2017'de sistematik negatif:

| | 2008 | 09 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gece | 72,2 | 59,7 | 42,3 | 25,0 | 8,2 | −17,2 | 23,3 | 13,8 | 52,1 | 13,5 | 11,6 | 6,8 | 54,0 | 13,2 | −7,7 | 18,7 | 23,7 | 32,8 | 5,4 |
| gün içi | −109,6 | −28,4 | −13,1 | −42,5 | −17,5 | −60,5 | −36,6 | −42,2 | −9,7 | −2,2 | −20,8 | 26,7 | −32,7 | −23,3 | −1,8 | −9,2 | −13,6 | 60,7 | −3,3 |

**"Getiri gece mi oluşuyor?"**
- GLD için **evet, hem yükselişte hem düşüşte**. 2013–2015 ayı piyasasında gece de negatifti. Yani bu bir "gece primi" değil. Altının fiyat keşfi Asya/Londra saatlerinde ve 08:30 ET verilerinde oluyor. ABD seansı ortalamada bir şey eklemiyor.
- GDX için gece/gün içi asimetrisi IS'te çok güçlü: gece %29/yıl, gün içi −%36/yıl. OOS'ta zayıfladı (gün içi −%2). Bu, hisse senetlerindeki gece–gün içi asimetrisiyle ve Quantpedia'nın (2025) "OHLC açılışına güvenme" uyarısıyla uyumlu.

**Ortalama testleri (yıllık %, NW t):**

| ETF | gece tam (t) | gece OOS (t) | gün içi tam (t) | gün içi OOS (t) |
|---|---|---|---|---|
| GLD | 9,0 (3,02) | 14,1 (3,37) | −1,1 (−0,40) | −1,6 (−0,47) |
| GLDM (2018+) | 16,9 (3,84) | 16,9 (3,84) | −3,0 (−0,86) | — |
| GDX | 24,0 (4,50) | 18,0 (2,25) | −19,9 (−2,80) | −2,0 (−0,22) |
| GDXJ | 26,4 (4,49) | 26,4 (3,13) | −24,1 (−3,00) | −12,2 (−1,18) |
| SLV | 11,6 (2,06) | 18,8 (2,23) | −5,5 (−1,10) | −6,7 (−0,99) |
| NUGT | 23,6 (1,74) | 15,9 (0,92) | −62,7 (−3,33) | −16,3 (−0,75) |

**Pratik alternatif "kapanışta al, açılışta sat" (CO)** — net yıllık getiri %:

| ETF | 0 bps tam / OOS / 2022+ | 10 bps OOS | 20 bps OOS | Başabaş (bps/RT) tam / OOS / 2022+ | Al-tut OOS |
|---|---|---|---|---|---|
| GLD | 9,9 / 14,9 / 17,3 | −10,3 | −35,5 | 3,9 / 5,9 / 6,9 | 14,0 |
| GDX | 26,8 / 20,9 / 18,4 | −4,3 | −29,5 | 10,7 / 8,3 / 7,3 | 23,5 |
| GDXJ | 29,8 / 30,1 / 24,8 | +4,9 | −20,3 | 11,8 / 11,9 / 9,8 | 24,3 |
| NUGT | 39,6 / 29,7 / 25,9 | +4,5 (10 bps) / −20,7 (20 bps) | — | 15,7 / 11,8 / 10,3 | 37,6 |
| JNUG | 64,3 / 54,8 / 48,6 | +4,4 (20 bps) / −1,8 (2022+, 20 bps) | — | 25,5 / 21,7 / 19,3 | 35,7 |

Maliyetsiz CO, GLD'de al-tut ile aynı getiriyi daha düşük oynaklıkla verir (Sharpe 1,15 vs 0,81, OOS). Ama Midas maliyetinin 10 bps varsayıldığı her senaryoda CO al-tut'un çok altında kalıyor. JNUG'nun başabaşı (OOS 21,7 bps) kaldıraçlı maliyet varsayımına (20 bps) çok yakın, NUGT'unki (11,8 bps) altında. 2022+ döneminde ve gerçekçi açılış dolumuyla (aşağıda) sıfırın altına iniyor. NUGT'un kendi maliyeti (20 bps) ile OOS net getirisi −%20,7.

**Açılışta piyasa emri gerçekçi mi?** (`b_dolum_gercekcilik.csv`)
- Son 730 günde (saatlik veri) GLD'nin gece getirisi resmî açılışa kadar 10,8 bps/gün, 10:30 ET'ye kadar 8,8 bps/gün. Gece etkisi ilk saatte kısmen korunuyor.
- Son 60 günde (5 dk veri) resmî açılış ile 09:35 ET fiyatı arasındaki ortalama mutlak fark: GLD 11,8, GDX 51, GDXJ 58, NUGT 105 bps. Madencilerde açılışta piyasa emri, resmî açılış baskısından tek işlemde onlarca bps sapabilir. CO'nun ince kenarı bunu kaldırmaz.
- Midas'ın emirleri açılış müzayedesine yönlendirip yönlendirmediği ve ön seans işlemine izin verip vermediği doğrulanamadı (site haritasında ETF sayfası yok).

**Hafta sonu gecesi:** GLD hafta sonu gecesi 3,6 bps ile hafta içi gecesi 3,6 bps aynı. Fark yok (3 test, hepsi |t|<1,5 fark).

**Açılış boşluğu öngörür mü?**
- GDX/GDXJ'de gün t açılış boşluğu, ertesi kapanıştan kapanışa getiriyi sıra (Spearman) bazında ters öngörüyor: IC −0,044/−0,049, t=−3,06/−3,17, 15/19 ve 15/18 yıl.
- Ancak ham getiri regresyonunda t=−0,50/−0,58. Ayrıştırınca etki ertesi gecede (t=−1,9/−2,4), gün içinde değil.
- İşaret ve eşik kurallarında IS'te seçilen eşikler OOS'ta negatif: GDX Sharpe −0,15, GDXJ 0,10.
- **Sıralama artefaktı, ticari değil (YOK).**

---

## 5. (c) Takvim (195 test: 168 getiri günü + 27 olay tepkisi)

Kurgu: gün D getirisi, giriş D'den önceki işlem günü kapanışında. Tam dönem |t|'ye göre ilk 10:

| ETF | Test | n | olay günü ort. (bps) | diğer (bps) | t | t_IS | t_OOS | t_2022+ | yıl |
|---|---|---|---|---|---|---|---|---|---|
| GDXJ | ayın ilk işlem günü | 204 | 63,8 | −2,2 | 3,21 | 1,96 | 2,60 | 1,51 | 15/18 |
| GDXJ | tatil öncesi gün | 156 | 58,3 | −1,2 | 2,96 | 1,81 | 2,39 | 1,77 | 15/18 |
| GDX | tatil öncesi gün | 171 | 47,3 | −0,2 | 2,93 | 1,71 | 2,45 | 1,77 | 16/19 |
| GDXJ | FOMC sonrası gün | 135 | −73,8 | 3,4 | −2,63 | −2,92 | −0,72 | −1,05 | 14/18 |
| GLD | Ocak | 383 | 17,0 | 1,9 | 2,44 | 2,22 | 1,19 | 1,20 | 15/19 |
| SLV | FOMC günü | 150 | 44,0 | 1,0 | 2,43 | 2,16 | 1,22 | 0,31 | 14/19 |
| GDXJ | TOM (son 1 + ilk 3) | 817 | 21,6 | −3,9 | 2,36 | 1,88 | 1,44 | 0,68 | 14/18 |
| GDX | Aralık son 7 işlem günü | 126 | 35,4 | 0,6 | 2,34 | 2,37 | 0,82 | −1,01 | 12/18 |
| GDX | FOMC günü | 150 | 57,8 | −0,3 | 2,30 | 2,85 | 0,01 | −0,41 | 12/19 |
| GDXJ | Aralık son 7 işlem günü | 119 | 36,7 | −0,1 | 2,02 | 1,76 | 1,07 | −0,85 | 11/17 |

**Katı IS protokolü** (her ETF'te IS |t|'si en yüksek takvim testi seçilip OOS'a bakılırsa):
- GLD → Ocak (OOS t=1,19, aynı işaret)
- GDX → FOMC günü (OOS 0,01)
- GDXJ → NFP sonrası 5 gün (OOS −0,20)
- SLV → FOMC günü (OOS 1,22)

Hiçbiri OOS |t|≥2 vermiyor. Ayın ilk günü ve tatil öncesi IS sıralamasında ilk 5'te ama birinci değil. Bu etkiler **önsel hipotez** olarak değerlendirildi: hisse senedi literatüründe ay dönümü (Ariel 1987; Lakonishok-Smidt 1988; Etula ve diğ. 2020 ay sonu likidite talebi) ve tatil öncesi (Ariel 1990) etkileri var, Incrementum da GLD/GDX/GDXJ'de ilk gün iddiasını dile getiriyor.

**Sağlamlık (madenci takvimi):**
- **SPY kontrolü** (aynı gün SPY getirisi regresyona eklendi):
  - GDX tatil öncesi 40,9 bps, t=2,55 (OOS t=2,09); GDX ilk gün 21,9 bps, t=1,19 (OOS 2,49).
  - GDXJ tatil öncesi 53,2 bps, t=2,66; GDXJ ilk gün 58,4 bps, t=2,79.
  - Yani bu etkiler hisse piyasası etkisinin beta kanalıyla taşınması değil.
- **Komşu gün placebo** (GDXJ, ort. bps): ayın 2. günü −4,6, 3. günü 22,2, son günü 5,3, sondan 2. −19,6. Etki ilk güne özgü. Tatil öncesinden bir önceki gün 30,5 bps: "tatil öncesi penceresi" iki güne yayılıyor. Tatil sonrası 14,6.
- **Yıl-içi rastgele gün permütasyonu** (5.000 çekiliş, tek yönlü p): GDXJ sepet 0,0002; GDXJ ilk gün 0,0004; GDX tatil öncesi 0,008; GDXJ tatil öncesi 0,007; GDX sepet 0,009. Bu p değerleri tek test içindir, çoklu test düzeltmesi yapılmamıştır.
- **Tatil türüne göre** (GDX/GDXJ bps): Noel öncesi 134/138, Bağımsızlık Günü öncesi 141/184, İşçi Bayramı öncesi 81/134, Kutsal Cuma öncesi 83/34, Yılbaşı öncesi 61/51, Şükran 37/37, MLK 43/−3, Memorial 13/5, Washington −19/7, Juneteenth (4+1 gözlem) negatif. Etki birkaç büyük tatilde yoğun ama yaygın.
- **GLD'de aynı etkiler zayıf.** Tatil öncesi 15 bps (t=1,77) maliyet sonrası OOS Sharpe 0,36, stres maliyette −0,02. İlk gün etkisi yalnız OOS'ta (t=2,40; IS −0,09).

**Olaylar:**
- FOMC günü (giriş önceki kapanış) GDX'te IS'te güçlüydü (t=2,85), OOS'ta kayboldu (0,01). Altında FOMC sonrası 5 günde −42 bps zayıflık var, t=−1,83.
- CPI/NFP günü ve olay günü 15:00 ET tepkisinin devamı/dönüşü: GDX NFP tepkisi h=3 için t=2,81 (IS 1,93, OOS 2,01, n=206), tek başına ve izole. Diğer 26 olay-tepki testinde anlamlı devam/dönüş yok.
- **Haftanın günü, ay mevsimselliği (Ocak dışında), aylık opsiyon vadesi haftası/3. Cuma, COMEX OG altın opsiyon vadesi ve GC ilk bildirim günü:** hiçbiri |t|≥2 değil.
- **Aralık vergi zararı / Ocak madenci etkisi:** Aralık 1–20'de madenci zayıflığı yok. Aralık son 7 günü GDX'te IS'te pozitif (2,37), OOS'ta zayıf (0,82). Ocak ilk 10 gün GDXJ'de IS'te 1,94, OOS'ta −0,03. **Tutmuyor.**

---

## 6. (d) Kaldıraçlı ve ters ETF'ler

**Gerçekleşen kaldıraç** (örtüşmeyen h günlük basit getiri regresyonu):

| ETF | Rejim | L | 1 gün | 3 gün | 5 gün | 20 gün | sapma std 1/5 gün (bps) |
|---|---|---|---|---|---|---|---|
| UGL | tümü | 2 | 2,00 | 2,02 | 2,01 | 2,01 | 17 / 29 |
| GLL | tümü | −2 | −2,00 | −2,00 | −2,00 | −1,91 | 19 / 41 |
| NUGT | 2x (2020-04+) | 2 | 1,98 | 2,00 | 2,01 | 2,08 | 24 / 46 |
| NUGT | 3x (2020-04 öncesi) | 3 | 2,81 | 2,88 | 2,78 | 2,94 | 125 / 311 |
| DUST | 2x | −2 | −1,98 | −1,97 | −1,95 | −1,73 | 27 / 116 |
| JNUG | 2x | 2 | 1,95 | 1,99 | 2,00 | 2,09 | 37 / 59 |
| JDST | 2x | −2 | −1,96 | −1,97 | −1,96 | −1,68 | 34 / 132 |
| AGQ | tümü | 2 | 2,03 | 2,03 | 2,04 | 1,99 | 35 / 71 |
| ZSL | tümü | −2 | −2,03 | −2,00 | −1,97 | −1,83 | 48 / 194 |

1–5 günlük ufukta 2x ürünler nominal kaldıracı iyi izliyor. 3x dönemdeki NUGT/DUST/JNUG/JDST ise 1 günde bile ~2,8 verdi, büyük ölçüde Mart 2020 ve kapanış zamanı uyumsuzlukları yüzünden.

**Aşınma** (yıllık: LETF log getirisi − L × dayanak log getirisi):

| ETF | Rejim | Gerçek | Teori −(L²−L)/2·σ² | Ücret, finansman vb. | 1 gün (bps) | 5 gün (bps) |
|---|---|---|---|---|---|---|
| UGL | tümü | −6,9% | −3,0% | −3,9% | −2,7 | −13,7 |
| GLL | tümü | −6,6% | −8,9% | +2,2% | −2,6 | −13,2 |
| NUGT | 2x | −20,3% | −14,5% | −5,8% | −8,1 | −40,3 |
| NUGT | 3x | −53,2% | −47,1% | −6,1% | −21,1 | −105,5 |
| DUST | 2x | −35,3% | −43,4% | +8,1% | −14,0 | −70,1 |
| JNUG | 2x | −24,8% | −18,8% | −5,9% | −9,8 | −49,1 |
| JDST | 2x | −48,7% | −56,5% | +7,8% | −19,3 | −96,7 |
| AGQ | tümü | −17,7% | −10,5% | −7,1% | −7,0 | −35,1 |
| ZSL | tümü | −34,6% | −31,6% | −2,9% | −13,7 | −68,6 |

Aşınma oynaklık rejimine bağlı: σ20 en yüksek üçte birde 5 günlük aşınma NUGT −135, DUST −245, UGL −17 bps. UGL vadeli/swap üzerinden tuttuğu için finansman maliyeti taşıyor, GLL ters yönde bunu kazanıyor.

**"Kaldıraçlı ETF ile aynı sinyal":**
- Madenci takvim sepetinde JNUG yıllık getiriyi ikiye katlıyor (OOS %26 vs %13) ama Sharpe'ı artırmıyor (1,00 vs 1,08).
- GDX 5 gün düşüş kuralında NUGT 0,76 vs GDX 0,78.
- Kaldıraçlı sürüm hiçbir kuralda Sharpe'ı iyileştirmiyor. 1 günlük tutuşta aşınma küçük (NUGT 2x ~8 bps), 5 günde kenarın önemli bir kısmını yiyor.

---

## 7. (e) Hangi ETF hangi iş için?

| ETF | Gider %/yıl* | Fiyat $ | Medyan günlük $ hacim (mn, son 1 yıl) | 1 sent = bps | Günlük tutma (bps) | Spot'a korelasyon (2018-09+) | İz sürme hatası %/yıl | İz sürme farkı %/yıl | 5 gün sapma std (bps) | Roll 5 dk üst sınır (bps) |
|---|---|---|---|---|---|---|---|---|---|---|
| GLD | 0,40 | 372,5 | 3.742 | 0,25 | 0,16 | 0,9994 | 0,65 | −0,37 | 5,9 | 5,2 |
| IAU | 0,25 | 76,4 | 535 | 1,22 | 0,10 | 0,9988 | 0,87 | −0,26 | 6,4 | 5,2 |
| GLDM | 0,10 | 80,4 | 424 | 1,16 | 0,04 | 0,9989 | 0,83 | −0,15 | 7,7 | — |
| SGOL | 0,17 | 38,7 | 138 | 2,40 | 0,07 | 0,9987 | 0,92 | −0,19 | 7,9 | — |
| BAR | 0,17 | 40,0 | 14 | 2,32 | 0,07 | 0,9977 | 1,19 | −0,19 | 7,4 | — |
| AAAU | 0,18 | 40,1 | 71 | 2,32 | 0,07 | 0,9970 | 1,37 | −0,19 | 9,1 | — |
| GDX | 0,51 | 87,6 | 1.912 | 1,14 | 0,20 | — | — | — | — | 11,5 |
| GDXJ | 0,51 | 107,7 | 561 | 0,87 | 0,20 | — | — | — | — | 11,3 |
| SLV | 0,50 | 46,9 | 1.383 | 1,65 | 0,20 | — | — | — | — | 6,7 |
| UGL | 0,95 | 43,2 | 147 | 1,84 | 0,38 | — | — | — | — | — |
| GLL | 0,95 | 26,0 | 60 | 4,33 | 0,38 | — | — | — | — | — |
| NUGT | ~1,0 | 142,2 | 110 | 0,60 | 0,40 | — | — | — | — | 22,0 |
| JNUG | ~1,0 | 127,9 | 48 | 0,56 | 0,40 | — | — | — | — | — |
| DUST | ~1,0 | 37,7 | 55 | 1,96 | 0,40 | — | — | — | — | — |

\*Gider oranları ihraççı sayfalarındaki bilinen değerlerdir; bu oturumda doğrulanmadı. Yıllık iz sürme farkı bunlarla tutarlı: GLD −0,37 (2008–2026 her yıl −0,28 ile −0,47), IAU −0,26, GLDM −0,15. Roll tahmini 5 dk'lık mikro dönüşleri içerdiği için kotasyon farkının üst sınırıdır. GLD'nin gerçek kotasyon farkı ~1 sent (0,25 bps). Abdi-Ranaldo günlük tahmincisi bu likiditede oynaklığı ölçtüğü için (tüm altın ETF'lerinde ~61 bps) kullanılmadı.

**Öneri:**
- **1–5 günlük altın işlemi:** GLD veya GLDM.
  - GLD: en derin likidite ve en dar bps kademe. Büyük tutarda ve açılışa/kapanışa yakın emirde en az kayma.
  - GLDM: 5 günde ~0,6 bps daha ucuz tutma, ama ~1 bps daha geniş kademe. Kısa işlemde fark başabaş.
  - Midas'ın 10 bps varsayımı her ikisini de gölgede bırakıyor.
- **Haftalar–aylar:** GLDM (veya IAU).
- **Madenci işlemi:** GDX likit. GDXJ etkilerde daha güçlü ama 3,4 kat daha az likit ve 5 dk sapması yüksek.
- **Kaldıraçlı/ters:** yalnız 1–3 günlük net sinyalde ve küçük tutarda. 2x ürünlerde 5 günlük aşınma 13–50 bps.
- GLD–IAU–GLDM arasında günlük getiri farkı std'si ~6 bps: aynı kapanışta bile "aynı altın" değiller. Sinyal GLD üzerinde kurulup GLDM ile uygulanırsa 1 günde ~6 bps gürültü ekleniyor, sistematik sapma eklenmiyor. GLD kurallarının IAU/GLDM sonuçları neredeyse aynı (`a_strat_all.csv`).
- GLD kapanış/NAV primi (t-1) sonraki getiriyi öngörmüyor: t=−0,80. Prim, LBMA PM'den 16:00 ET'ye kadarki altın hareketinden ibaret.

---

## 8. Son adaylar: uygulanabilir sürümler, yıl yıl, uç dönemler

**Net Sharpe** (10 bps; kaldıraçlı 20 bps). Bu kuralların hepsi yalnız uzun olduğu için ters ETF sürümü yalnız uzunla aynı:

| Strateji | ETF | Sürüm | Tam | IS | OOS | 2022+ |
|---|---|---|---|---|---|---|
| Madenci takvim sepeti (tatil öncesi ∪ ayın ilk günü), h=1 | GDXJ | yalnız uzun | 0,89 | 0,71 | **1,08** | 0,92 |
| | GDXJ | drift çıkarılmış | 0,83 | 0,71 | 0,91 | 0,77 |
| | GDXJ→JNUG | kaldıraçlı | 0,81 | 0,59 | 1,00 | 0,84 |
| | GDX | yalnız uzun | 0,50 | 0,04 | 1,07 | 1,00 |
| | GDX→NUGT | kaldıraçlı | 0,75 | 0,48 | 1,03 | 0,96 |
| Madenci tatil öncesi, h=1 | GDX | yalnız uzun | 0,56 | 0,37 | 0,75 | 0,79 |
| | GDXJ | yalnız uzun | 0,62 | 0,50 | 0,74 | 0,78 |
| Madenci ayın ilk günü, h=1 | GDXJ | yalnız uzun | 0,68 | 0,52 | 0,84 | 0,62 |
| | GDX | yalnız uzun | 0,26 | −0,15 | 0,83 | 0,72 |
| GDX 5 gün üst üste düşüş → al, h=1 | GDX | yalnız uzun | 0,61 | 0,49 | 0,78 | 1,03 |
| GDX 4 gün üst üste düşüş → al, h=3 | GDX | yalnız uzun | 0,57 | 0,38 | 0,86 | 1,08 |
| GLD yalnız Ocak'ta uzun | GLD | yalnız uzun | 0,66 | 0,73 | 0,59 | 0,66 |
| | GLD | drift çıkarılmış | 0,50 | 0,63 | 0,34 | 0,47 |
| GLD BollZ<−2 → 5 gün | GLD | yalnız uzun | 0,41 | 0,23 | 0,70 | 0,50 |
| GLD tatil öncesi | GLD | yalnız uzun | 0,19 | 0,07 | 0,36 | 0,08 |
| *Al-tut* | GDX / GDXJ / GLD | | 0,30 / 0,28 / 0,52 | 0,07 / 0,02 / 0,29 | 0,61 / 0,54 / 0,81 | 0,76 / 0,69 / 0,93 |

**OOS (2018–2026) ayrıntı:**

| Strateji | ETF | Yıllık % (10 bps) | Yıllık % (stres) | Sharpe (stres) | Gidiş-dönüş/yıl | MDD % |
|---|---|---|---|---|---|---|
| Takvim sepeti | GDXJ | 13,1 | 11,2 | 0,93 | 18,6 | −12,6 |
| Takvim sepeti | GDX | 11,5 | 9,6 | 0,90 | 18,6 | −11,4 |
| Tatil öncesi | GDX | 5,0 | 4,1 | 0,62 | 9,3 | −5,7 |
| İlk gün | GDXJ | 8,3 | 7,1 | 0,72 | 12,1 | −9,8 |
| GDX 5 gün düşüş | GDX | 4,0 | 3,7 | 0,72 | 3,4 | −5,2 |
| GLD Ocak | GLD | 3,2 | 3,1 | 0,57 | 1,0 | −10,3 |

**Yıllık net P&L** (%, yalnız uzun, 10 bps):

| Yıl | Sepet GDXJ | Sepet GDX | Tatil öncesi GDX | GDX 5 gün düşüş | GLD Ocak |
|---|---|---|---|---|---|
| 2008 | — | −29,3 | −2,7 | 9,8 | 7,5 |
| 2009 | 10,3 | 1,4 | 5,1 | −1,9 | 5,7 |
| 2010 | 14,8 | 5,8 | 1,4 | 0,9 | −1,2 |
| 2011 | 0,4 | −3,9 | −0,1 | −2,7 | −6,6 |
| 2012 | 24,4 | 16,7 | 9,0 | 3,0 | 10,8 |
| 2013 | −10,8 | −11,7 | 0,6 | 6,7 | −0,6 |
| 2014 | 20,7 | 15,5 | 4,6 | 4,8 | 3,4 |
| 2015 | 4,2 | 2,5 | 4,8 | 6,9 | 8,4 |
| 2016 | 9,7 | 6,8 | 1,7 | 0,0 | 5,3 |
| 2017 | 1,4 | 1,2 | −1,4 | 3,5 | 5,2 |
| 2018 | 15,7 | 13,2 | 8,9 | 3,8 | 3,1 |
| 2019 | 1,4 | 0,8 | 1,0 | −0,4 | 2,8 |
| 2020 | 28,6 | 24,5 | 7,0 | 2,6 | 4,3 |
| 2021 | 16,3 | 12,4 | 3,8 | −1,1 | −3,2 |
| 2022 | 17,2 | 14,9 | 4,4 | 0,3 | −1,7 |
| 2023 | 11,0 | 10,3 | 3,2 | 13,4 | 5,6 |
| 2024 | 11,5 | 11,6 | 11,1 | 4,3 | −1,5 |
| 2025 | 13,2 | 12,6 | 2,3 | 8,3 | 6,5 |
| 2026 | 0,6 | 1,2 | 2,6 | 4,2 | 12,3 |
| Pozitif yıl | 17/18 | 16/19 | 16/19 | 14/19 | 13/19 |

**Uç dönemler** (dönem içi net P&L; dönemler hariç Sharpe):
- **Takvim sepeti GDX:** 2008'de −%29,3 (Eylül–Kasım 2008 ay başları). 2008 hariç tam Sharpe 0,50 → 0,70. Nisan 2013'te −%1,1, Mart 2020'de +%4,0, Ocak–Şubat 2026'da +%5,5. Hepsi hariç OOS Sharpe 1,01.
- **Takvim sepeti GDXJ** (2009 sonrası): Nisan 2013 −%2,1, Mart 2020 +%5,6, Ocak–Şubat 2026 +%5,7. Hepsi hariç tam 0,87, OOS 1,01.
- **GDX 5 gün düşüş:** 2008 +%9,8, Nisan 2013 +%4,3. Bunlar hariç tam Sharpe 0,61 → 0,54, OOS 0,79. Kenarın bir kısmı kriz dönemlerinden geliyor.
- **GLD Ocak:** Ocak 2026 +%12,3 (tek ay). Hariç tam Sharpe 0,66 → 0,65, OOS 0,59 → 0,55.

---

## 9. İddialar ve güven etiketleri

| # | İddia | t_tam | t_IS | t_OOS | Yıl | OOS net Sharpe (yalnız uzun) | Etiket |
|---|---|---|---|---|---|---|---|
| 1 | GDXJ'yi ayın ilk işlem günü ve tatil öncesi gün tut (1 gün) | 4,25 | 2,62 | 3,41 | 15/18 (P&L 17/18) | 1,08 | **ORTA** |
| 2 | GDX tatil öncesi gün (SPY kontrollü t=2,55) | 2,93 | 1,71 | 2,45 | 16/19 | 0,75 | **ORTA** |
| 3 | GDX 5 gün üst üste düşüş → 1 gün al | 3,43 | 2,07 | 2,98 | 15/18 | 0,78 | **ORTA** |
| 4 | GLD Ocak etkisi | 2,44 | 2,22 | 1,19 | 15/19 | 0,59 (al-tut 0,81; drift çıkarılmış 0,34) | **ORTA** (zayıf) |
| 5 | GLD BollZ<−2 → 5 gün al | 2,04 | 0,90 | 2,52 | 16/19 | 0,70 | **DÜŞÜK** |
| 6 | GLD getirisinin gece oluşması (olgu); CO stratejisi | 3,02 | 1,08 | 3,37 | 14/19 | CO 10 bps: −0,79 | olgu ORTA, strateji **YOK** |

**Neden YÜKSEK yok?**
- 1 numaralı iddia (ve GDXJ ilk gün tek başına) mekanik ölçütlerin hepsini sağlıyor: |t|≥3, IS/OOS aynı işaret, OOS |t|≥2, yılların ≥%70'i, OOS Sharpe>0,3.
- Ancak sepet tam örneklem tablosu görüldükten sonra iki en iyi takvim testinin birleşimi olarak kuruldu.
- Bileşenlerin öngörücü-yalnız global FDR q'su 0,52. Ailedeki |t|≥2 sayısı sıfır altında beklenenden az.
- IS'te katı seçim protokolü bu etkileri birinci sıraya koymuyordu.
- Bu yüzden ORTA'ya indirildi. Önsel literatür kanıtını (hisse senedi ay dönümü ve tatil öncesi etkileri) kabul eden okuyucu bunu "ORTA+" olarak okuyabilir.
- 3 numaralı iddia 24 tanımlık ızgaranın en iyisi ve GDXJ'de tekrar etmiyor.

---

## 10. Negatif bulgular (test edildi, tutmadı)

- GLD/GDX/GDXJ/SLV momentum 1–250 gün (Spearman). GLD 12 ay momentumunun tam dönem t'si yıllar arası drift artefaktı (4/18 yıl).
- MA filtreleri (P>SMA10/20/50/100/200; 5/20, 10/50, 20/100, 50/200 kesişimleri): zamanlama değeri yok. Drift çıkarılmış Sharpe ≈ 0. GLD P>SMA10 IS'te en iyi (t_IS=2,54), OOS −0,47.
- Donchian 20/55 durum kuralı: GLD'de IS negatif (−2,0), OOS pozitif; işaret döndü.
- RSI(2) (eşik 5/10/20, SMA200 filtreli/filtresiz) ve klasik Connors çıkışlı GLD kuralı: drift çıkarılmış Sharpe 0,04 (OOS).
- Bollinger(20,2) GLD ±; SLV Bollinger; >2σ ve >3σ gün sonrası dönüş/devam (her dört ETF).
- Ardışık seriler GLD/SLV (dönüş yok; SLV'de 3 gün düşüş sonrası hafif devam, t=−1,6).
- GLD kapanışa yakın 1 günlük dönüş: IC −0,031, ama yılda 65 gidiş-dönüş ile net negatif.
- Gece/gün içi: CO (kapanışta al, açılışta sat) ve OC stratejileri 10 bps'te negatif. Hafta sonu gecesi farkı yok. Açılış boşluğu dönüşü yalnız sıra artefaktı.
- Takvim: haftanın günü (20 test), ay mevsimselliği (Ocak dışında, 48 test; Eylül/Kasım "sonbahar etkisi" yok), aylık opsiyon vadesi haftası/3. Cuma/sonrası, COMEX OG altın opsiyon vadesi [−2..0] ve [+1..+2], GC ilk bildirim günü, CPI ve NFP günü, FOMC günü (OOS'ta kayboldu), FOMC sonrası gün GDXJ (IS −2,92, OOS −0,72), FOMC/CPI/NFP günü tepkisinin devamı/dönüşü (GDX NFP h=3 hariç izole), Aralık vergi zararı ve Ocak madenci etkisi.
- Ters ETF'lerle kısa bacak: hiçbir kuralda OOS'ta yalnız uzun sürüme anlamlı katkı yok. IS'te DUST/JDST 3x aşınmasıyla negatif.
- Kaldıraçlı ETF ile aynı sinyal: Sharpe'ı iyileştirmiyor, yalnız getiriyi ve düşüşü ölçekliyor.
- GLD kapanış/NAV primi (t-1): öngörü yok.

---

## 11. Midas kullanıcısı için pratik okuma

1. **Altına yön sinyali bu ailede yok.** ETF'in kendi grafiğine bakarak 1–5 günlük al-sat yapmanın (trend, RSI, Bollinger, seri) maliyet sonrası al-tut'a göre değeri yok. GLD'de "pozisyondaysan kal" en iyi kıyas.
2. **Gece tutmak önemli.** Altının hareketi ABD seansı dışında oluşuyor. Gün içinde girip kapanışta çıkmak (OC) tarihsel olarak getirinin neredeyse tamamını kaçırıyor: OOS −%1/yıl. Kapanışta alıp açılışta satmak ise maliyet yüzünden tutmuyor.
3. **Madenci takvimi tek kayda değer aday.** Örnek uygulama: ayın son işlem gününün kapanışına yakın GDX/GDXJ al, ayın ilk işlem gününün kapanışına yakın sat. Tatil öncesi gün için aynısı (tatilden iki işlem günü önce al, tatilden önceki son gün kapanışta sat). Yılda yaklaşık 19 işlem.
   - Beklenti dönem başına 30–60 bps brüt.
   - 10–20 bps maliyetle hâlâ pozitif, ama tek bir 2008 benzeri ay başı −%10'u aşabiliyor.
   - Büyüklük küçük tutulmalı ve "ORTA" güvende olduğu unutulmamalı.
   - JNUG/NUGT ile ölçek büyür, Sharpe artmaz.
4. **Uygulama:** 15:45–15:55 ET (TSİ 23:45–23:55 kışın; 22:45–22:55 yazın) limit emir varsayıldı. Açılışta piyasa emri madencilerde tek işlemde 50–100 bps sapabiliyor (5 dk veri), açılış odaklı stratejilerden kaçınılmalı.
5. **ETF:** altında kısa vade için GLD, uzun tutuşta GLDM. Kaldıraçlı ürünlerde 5 günlük aşınma UGL için −14 bps, NUGT 2x için −40 bps. Yüksek oynaklık döneminde bu iki-üç katına çıkıyor.

---

## 12. Sınırlamalar

- Yahoo açılış fiyatı resmî açılış baskısı; gerçekçi dolum yalnız son 730 gün (saatlik) ve 60 gün (5 dk) için ölçülebildi.
- Midas'ın gerçek maliyet yapısı (komisyon + kur makası), ETF listesi, ön seans ve açılış müzayedesi yönlendirmesi bu çalışmada doğrulanamadı. 10/20 ve 20/40 bps varsayımdır.
- Nakit getirisi 0 alındı. Yalnız uzun stratejiler gerçekte nakit faizi kazanır, bu da az bulunan zamanlı stratejileri biraz iyileştirir.
- SLV "nc" (15:00 ET) sürümleri 2016+ veriyle sınırlı; IS yalnız 2016–17.
- Olay takvimleri 2009+ (FOMC 2008 elle eklendi; CPI/NFP 2008 yok).
- Kaldıraç rejimi kesimi (2020-04-01) yaklaşık; Mart 2020'nin son haftası geçiş.
- Gider oranları bellekten; ihraççı sitelerinden kontrol edilmeli.

---

## 13. Dosyalar (`out/e1_etf_zaman_takvim/`)

- **Kod:** `e1_common.py` (ortak), `a_ts.py`, `a_strat.py`, `a_os.py`, `b_night.py`, `b2_gap.py`, `c_cal.py`, `d_lev.py`, `e_etf.py`, `f_final.py`, `g_perm.py`, `g_placebo.py`, `run_all.sh` (hepsini sırayla çalıştırır, ~1 dk).
- **(a):** `a_ts_all.csv` (612 test), `a_is_secim.csv`, `a_strat_all.csv`, `a_strat_legs.csv`, `a_oversold_grid.csv`.
- **(b):** `b_yillik_gece_gunici.csv`, `b_ortalama_testleri.csv`, `b_strateji_CO_OC.csv`, `b_basabas_maliyet.csv`, `b_dolum_gercekcilik.csv`, `b_haftasonu_gece.csv`, `b_ongoru.csv`, `b2_gap_*.csv`.
- **(c):** `c_takvim_testleri.csv`, `c_olay_tepki_sonrasi.csv`, `f_tatil_oncesi_gunler.csv`, `g_komsu_gun_placebo.csv`, `g_permutasyon.csv`.
- **(d):** `d_gerceklesen_kaldirac.csv`, `d_asinma.csv`, `d_yillik_kaldirac.csv`, `d_asinma_vol_rejimi.csv`.
- **(e):** `e_etf_secim.csv`, `e_yillik_iz_farki.csv`, `midas_us_tickers.txt` (Midas site haritasındaki ABD hisse sayfaları; ETF sayfası yok).
- **Son adaylar:** `f_final_strateji.csv`, `f_final_yillik.csv`, `f_final_uc_donem.csv`, `f_final_testler.csv`.
- **Kayıt ve FDR:** `../registry/e1_etf_zaman_takvim.csv` (1.102 test), `kayit_fdr.csv` (tüm kayıtlar BH), `kayit_fdr_ongorucu.csv` (1.046 öngörücü testi BH), `g_placebo_lead.csv`.
