# Denetim: sektor_tematik ailesi

Hazırlanma: 7 Kasım 2026. Denetlenen: `notlar/aile_sektor_tematik.md`, `kod/ajan_sektor_tematik/`, `sonuclar/aile_sektor_tematik/sonuc.json`.
Denetim kodu: `kod/denetim_sektor_tematik/` (d_ortak, d1-d9). Çıktılar: `sonuclar/aile_sektor_tematik/denetim/`. JSON: `sonuclar/aile_sektor_tematik/denetim.json`.
İşlem simülasyonu `lib.trades`/`lib.evaluate` kullanılmadan baştan yazıldı (`d_ortak.sim`, `sim_hold`). Fiyatlar `lib.load`'dan alındı.

## 0. Kısa sonuç

- **S1 (SMH IBS<0,20 → SMH, 1 gün) birebir yeniden üretildi** ve sinyalin kendisi çürütülemedi. 492 işlemin 492'si aynı; brüt farkı 1e-16.
  - Permütasyon testi 10.000 tekrarla yapıldı ve p<0,0001 çıktı. Yıla, oynaklık beşliğine ve 1 günlük getiri ondalığına göre tabakalı sürümlerde de sonuç değişmiyor.
  - En iyi 5 işlem çıkarılınca net 31,5 bp (t 3,05). Eşik 0,10-0,30 arasında plato var.
  - En büyük kazançlar gerçek piyasa olayları ve bağımsız SOXX serisiyle doğrulanıyor.
- **Uygulama varsayımı ajanın dediğinden pahalı.** Ajan kapanıştan önce (TR 23:45-23:58) girmeyi öneriyor ve bunu "hafif iyimser" diye niteliyor.
  - Gün içi veriyle bakınca sinyal günlerinde 15:45-15:55 fiyatı resmî kapanışın **16-22 bp üstünde**.
  - 15:30'da hesaplanan IBS ile giriş, aynı dönemde backtest'e göre brüt **18,6 bp** kaybettiriyor.
  - Kapanış sonrası (after-hours) limit emriyle 17:00 ET civarında girmenin cezası yalnızca **~6 bp**.
- **FDR iddiası abartılı.** İki yönlü BH'yi geçmesinin nedeni, maliyet yüzünden anlamlı biçimde negatif çıkan binlerce satır. Aile taramasında 995 geçen satırın %96'sı negatif.
  - Pozitif yönlü (tek yönlü) BH'de genel taramanın 92 bin satırında da, ailenin 22 bin satırında da **hiçbir test geçmiyor**. S1'in tek yönlü p değeri 2,1e-4; eşik 4,5e-6.
  - S1 ancak ajanın seçimden sonra kurduğu 1.302 testlik kümede geçiyor.
- **Kenar oynaklıkla ölçekleniyor.**
  - En düşük oynaklık beşliğinde 6 bp (t 0,4), en yükseğinde 85 bp.
  - 2020 ve 2026 çıkarılınca 24,8 bp (t 2,07).
  - 1.000 $ pozisyonda gerçekçi girişle kenar 5-18 bp, t ≤ 1,6: **eşiği geçmiyor**.
- **Karar.**
  - S1: **doğrulandı**, ama sayılar ve kural düzeltilmeli. Kapanış sonrası limit girişiyle 2.500 $'da net ~31-36 bp, t 2,7-3,2; en az 2.500 $ pozisyon. abd_endeks ailesinin QQQ IBS stratejisiyle aynı bahis.
  - S2 (SOXL): **zayıf**. Bağımsız değil, Midas'ta bulunurluğu doğrulanmadı, risk eşdeğeri boyutta ek getiri sağlamıyor; SOXL Haziran 2026'dan bu yana −%82.
- **Lead-lag.**
  - EEM→KWEB (negatif): doğrulandı; ancak yalnız "alma" filtresi olarak kullanılabilir.
  - QQQ/SPY→IGV: **zayıf**. SPY(t) kontrolüyle t 0,17'ye düşüyor; endeksin kendi ertesi gün dönüşü beta üzerinden IGV'ye taşınıyor. Kural düzeyinde brüt −5,8 bp, maliyetin altında.
  - Yarı iletkenlerde "NVDA/TSM/AVGO/EWT/EWY öncü değil" iddiası doğrulandı.
- **TradingView.** Çıktıdaki 105 benzersiz kodun hepsi doğrulama dosyalarında "dogrulandi" ya da "dogrulandi_kanonik".

## 1. Kod ve zamanlama denetimi (mercek A)

| Kontrol | Sonuç |
|---|---|
| IBS (düzeltilmiş o/h/l/c) ile ham parquet'ten IBS | Fark 0; sinyal uyuşmazlığı 0. Düzeltme faktörü aynı günün o/h/l/c'sine birlikte uygulanıyor. |
| İleriye bakma | IBS yalnız t gününün mumunu kullanıyor. Kayan pencere, olay takvimi, VIX/BTC/Hazine verisi yok. Ancak IBS t kapanışını kullandığı için yalnız resmî kapanışta girişte geçerli (bkz. §3). |
| Giriş/çıkış günleri | C0: c[t]→c[t+1]; O1: o[t+1]→c[t+1]; C1: c[t+1]→c[t+2]. Ajanın betiği (lib.trades) ile aynı. |
| Çakışma | Pozisyondayken gelen sinyal yok sayılıyor. Çıkış günü gelen sinyal yeni işlem sayılıyor ve tam maliyet tekrar düşülüyor (muhafazakâr). |
| Maliyet | SMH 13 bp (12 komisyon + 1 makas), SOXL 14,2 bp. İşlem başına bir kez düşülüyor; doğru. Makas son 252 günün likiditesinden geliyor; 2016-2018'de SMH daha az likitti (ihmal edilebilir). |
| En iyi 5 işlem | 2025-04-08→09 (+%17,0, gümrük tarifesi ertelemesi; listedeki gerçek olay), 2022-11-09→10 (+%10,1, CPI), 2020-03-12→13 (+%9,6), 2020-03-16→17 (+%8,0), 2024-07-30→31 (+%7,5). Hepsi SOXX'te de var (t+1: +18,6 / +10,3 / +10,7 / +8,8 / +6,7 %) ve QQQ'da da yukarı. veri_kalitesi bayrakları SOXL'ün gerçek hareketlerinden geliyor; veri hatası yok. |
| Bozuk kapanış artefaktı | Sinyal günlerinde SMH−SOXX kalıntısı t günü +3,4 bp, t+1'de −3,8 bp: bozuk kapanış izi yok. İki seride birden IBS<0,2 olan 448 işlem: 40,8 bp (t 3,63). |
| 2026 aşırı hareketleri | SMH 2026-06-05 −%9,2 ve 2026-11-05 −%11,2. SOXX de aynı yönde hareket ediyor; gerçek. |

Ajanın betiğinde hata bulunmadı. S1 ve S2'nin tüm ana sayıları birebir yeniden üretildi (`d1_cikti.txt`).

## 2. İstatistiksel sağlamlık (mercek B)

### 2.1 S1 yeniden üretim ve dilimler (2.500 $, C0 h1, resmî kapanış)

| Dilim | n | Net (bp) | t |
|---|---|---|---|
| Tümü | 492 | 41,8 | 3,69 |
| IS / OOS | 256 / 236 | 43,3 / 40,1 | 3,13 / 2,20 |
| 2020 hariç | 429 | 32,3 | 2,78 |
| 2022 hariç | 427 | 47,8 | 4,05 |
| 2020 + 2022 hariç | 364 | 37,7 | 3,12 |
| 2020 + 2026 hariç | 391 | 24,8 | 2,07 |
| 2017-2019 | 136 | 25,3 | 1,71 |
| En iyi 5 hariç | 487 | 31,5 | 3,05 |
| En iyi 10 hariç | 482 | 25,3 | 2,51 |
| "Tut" kuralı (ardışık sinyalde satma) | 406 pozisyon | 52,7 | 4,25 |

**Yıl yıl.** 10/11 yıl pozitif, ama tek tek yıllar çoğunlukla t<1. Zayıf yıllar: 2018 (12 bp), 2022 (2 bp). Güçlü yıllar: 2020 (106 bp) ve 2026 (109 bp).

**Oynaklık beşliği (20 günlük).**

| Beşlik | Net (bp) | t |
|---|---|---|
| Q1 (düşük) | 6 | 0,39 |
| Q2 | 23 | — |
| Q3 | 38 | — |
| Q4 | 44 | — |
| Q5 (yüksek) | 85 | 2,31 |

Bugünkü oynaklık yıllık %62; Q5 eşiği %39.

### 2.2 Permütasyon (S1 brüt, 10.000 tekrar)

Gözlenen 54,8 bp, rastgele ortalama 13,2 bp.

| Tabakalama | p | Rastgele ortalama (bp) |
|---|---|---|
| Yok | 0,0001 | 13,2 |
| Yıla göre | 0,0001 | — |
| 20g oynaklık beşliğine göre | 0,0001 | 13,8 |
| 1g getiri ondalığına göre | 0,0006 | 29,9 |

Son satır, kenarın yaklaşık 16 bp'sinin düz 1 günlük dönüşten geldiğini gösteriyor; IBS bunun üstüne ~25 bp ekliyor.

Newey-West regresyonunda z1 ve düşüş günü kontrolüyle IBS<0,2 katsayısı +39 bp (t 2,89).

### 2.3 Parametre komşuluğu

| Mod | IBS eşiği 0,10-0,30 | Değerlendirme |
|---|---|---|
| C0 | Net 29-55 bp, t 3,2-4,1 | Plato |
| O1 | 0,125-0,15'te OOS ≈ −2 bp | Plato zayıf |

Ajanın komşu eşik raporu doğru.

### 2.4 Giriş modu ve maliyet

| Mod / pozisyon | Net (bp) | t | Not |
|---|---|---|---|
| O1 h1 (2.500 $) | 15,5 | 1,83 | Brüt kenar +27 bp; OOS 13,4 bp (t 0,96); yılların %45'i pozitif |
| O1 h1 (1.000 $) | −2,5 | — | |
| C1 h1 | 2,3 | — | Kenar ≈ 0 |
| C0, 1.000 $ (backtest) | 23,8 | 2,10 | |
| C0, 10.000 $ | 50,8 | 4,48 | |

Kabul ölçütündeki "O1'de brüt kenar > 0" şartı sağlanıyor (+27 bp). Etki ilk gün sönüyor.

### 2.5 Çoklu test (`d8_cikti.txt`)

| Test kümesi | İki yönlü BH | Tek yönlü (pozitif) BH | Bonferroni |
|---|---|---|---|
| genel_tum, 92.435 | geçer (19.520 satır geçiyor) | **0 satır geçer** | geçmez |
| Aile, 21.978 | geçer (995 satır; %96'sı negatif) | **0 satır geçer** | geçmez |
| Ajanın 1.302 testi | geçer | 15 satır geçer, hepsi yarı iletken/teknoloji IBS varyantı | — |
| Aynı kural 39 ETF'de | — | — | SMH ve SOXX geçer |

İki yönlü BH'nin geçmesi, maliyetin anlamlı kıldığı negatif satırların BH eşiğini gevşetmesinden kaynaklanıyor. Kârlı strateji arayışı için uygun boş hipotez tek yönlüdür ve tek yönlü BH'de keşif taramasında S1 geçmiyor. Ajanın 1.302'lik kümesi, S1 seçildikten sonra eklenen S1 satırlarını içerdiği için kısmen döngüsel.

Kanıtı ayakta tutanlar: literatürdeki IBS etkisi (Nasdaq/SPY), teknoloji kümesinde tutarlılık (SMH, SOXX, QQQ, XLK) ve IS/OOS'ta benzer büyüklük.

## 3. C0 uygulanabilirliği: gün içi veriyle test (`d2`, `d3`)

Midas'ta MOC/LOC yok. Yahoo saatlik barlarıyla (2023-12-11..2026-11-06; 730 gün; Nasdaq günlük H/L ile medyan fark 0 bp) ve son 60 günün 5 dakikalık barlarıyla test edildi.

| Senaryo (sinyal SMH; işlem SMH; 2.500 $) | n | Brüt (bp) | Net (bp) | t |
|---|---|---|---|---|
| A. Resmî IBS, resmî kapanışta giriş (backtest) | 121 | 75,8 | 62,8 | 2,23 |
| B. 15:30 IBS, 15:30 fiyatıyla giriş, ertesi kapanışta çıkış | 118 | 57,2 | 44,2 | 1,61 |
| C. 15:30 IBS ve giriş, ertesi gün 15:30 çıkış | 118 | 63,0 | 50,0 | 1,88 |
| D. 15:30 IBS, resmî kapanışta giriş (yalnız sınıflama hatası) | 118 | 53,3 | 40,3 | 1,46 |
| AH: resmî IBS, 17:00 ET after-hours fiyatıyla giriş | 121 | 69,9 | 56,9 | 2,03 |

**Saatlik veriden.**
- Resmî sinyal günlerinde 15:30→kapanış hareketi ortalama −33 bp.
- 121 resmî sinyal gününün yalnız 81'i 15:30'da da sinyal veriyor.

**5 dakikalık veriden (n=10 sinyal, küçük örnek).**
- Sinyal günlerinde 15:45, 15:50 ve 15:55 fiyatları resmî kapanışın +15,8, +21,7 ve +17,0 bp üstünde.
- Diğer günlerde bu fark −4 ile −8 bp arasında.

**Sonuç.** Kapanıştan önce giriş, kenarın yaklaşık 15-20 bp'sini kaybettiriyor. Midas'ın after-hours seansı (kış TR 00:00-04:00 / yaz 23:00-03:00, yalnız limit emir) resmî kapanışa çok daha yakın fiyat veriyor: 17:00 ET'de +6 bp. Bu yolda sınıflama hatası da yok, çünkü IBS resmî kapanışla hesaplanıyor. After-hours makası ölçülemedi; +5 bp ek varsayım eklendi.

**Düzeltilmiş S1 (`d6_duzeltilmis.csv`).**

| Senaryo | 1.000 $ | 2.500 $ | 10.000 $ |
|---|---|---|---|
| Backtest | 23,8 (t 2,10) | 41,8 (t 3,69) | 50,8 |
| AH girişi (+6 bp) | 17,8 (t 1,57; OOS t 0,88; yılların %55'i +) | **35,8 (t 3,16; IS 37,3 / OOS 34,1, OOS t 1,87; yılların %82'si +)** | 44,8 |
| AH + makas (+11 bp) | 12,8 (t 1,13) | 30,8 (t 2,72; OOS t 1,60) | 39,8 |
| Kapanış öncesi (+19 bp) | 4,8 (t 0,42) | 22,8 (t 2,01; OOS t 1,16; yılların %73'ü +) | 31,8 |
| "Tut" kuralı + AH (+6 bp) | — | 46,7 bp/pozisyon (t 3,77) | — |

## 4. S2 (SOXL)

**Yeniden üretim.**
- Birebir: 145,8 bp, t 4,23; IS 144 / OOS 148 bp.
- En iyi 5 işlem hariç: 114,3 bp (t 3,64).
- O1: 72,3 bp (t 2,74). C1: ≈ 0.

**Gün içi test.** Backtest varyantı (A) 229 bp, t 2,59. Gerçekçi 15:30 varyantı (B) 190 bp, t 2,22.

**Sorunlar.**
- S1 ile aynı sinyal; bağımsız kanıt değil.
- Midas'ta bulunurluğu doğrulanmadı.
- Risk eşdeğeri boyutta (833 $) işlem başına 10,15 $, SMH'nin 2.500 $'lık işleminde 10,44 $: ek getiri yok.
- Tam tutarla kullanımda maxDD −%53,5, en kötü işlem −%30,6.
- İşlem günlerinde SOXL − 3×SOXX ortalama −15,7 bp.
- SOXL 2026-06-04'te 262,7 iken 2026-11-06'da 46: −%82. 1 günlük oynaklık ~%9.

**Karar:** zayıf. Ayrı bir strateji olarak sunulmamalı; S1'in isteğe bağlı aracı olabilir.

## 5. Gecikmeli öncüler (`d4_leadlag.csv`)

Model: r_T(t+1) = a + b·r_L(t) + c·r_T(t), Newey-West(5).

| Hedef ← öncü | t | IS / OOS t | bp/sd | SPY(t) kontrolüyle t | r_L(t+1) eşzamanlı kontrolüyle t | Kural | Karar |
|---|---|---|---|---|---|---|---|
| IGV ← QQQ | −3,43 | −2,05 / −2,53 | −32 | **0,17** | −1,03 | z>+1 → IGV brüt −5,8 bp; yılların yarısı negatif | zayıf: endeks dönüşü beta üzerinden; maliyetin altında |
| IGV ← SPY | −3,52 | −2,70 / −2,62 | −35 | — | −2,10 | — | zayıf (QQQ ile aynı olgu) |
| KWEB ← EEM | −3,64 | −2,52 / −2,70 | −34 | −2,73 | +0,74 | z>+1 → KWEB brüt −30,5 bp, net −46,5 (t −3,73); IS −34 / OOS −59; 10 yılın 7'si negatif | doğrulandı (yalnız "alma" filtresi) |
| KWEB ← FXI | −2,54 | −2,08 / −1,67 | −47 | — | — | — | zayıf |
| SMH ← QQQ | −2,38 | −2,10 / −1,12 | — | — | — | — | zayıf (ajanla aynı) |
| XBI ← SPY | −3,02 | — / −1,16 | — | — | — | — | zayıf (ajanla aynı) |
| COPX ← XME | +2,82 | — / 1,58 | — | — | — | Maliyeti karşılamıyor | zayıf (ajanla aynı) |
| XLK ← AAPL, h3 | −3,44 | −2,08 / −2,42 | — | −3,25 | — | Kurala çevrilmedi | zayıf (h1 yok; ajan "kullanma" diyor, makul) |
| SMH ← NVDA / TSM / AVGO / EWT / EWY | 0,22 / 0,54 / −0,27 / 0,78 / 0,41 | — | — | — | — | — | "Öncü değil" iddiası doğrulandı |

Notlar:
- IGV satırında r_L(t+1) kontrolüyle etki −5 bp/sd'ye iniyor. QQQ'nun kendi gecikme katsayısı −0,118 (t −2,46).
- KWEB satırında büyük günler çıkarılınca t −4,37'ye güçleniyor. EEM'in kendi gecikme katsayısı −0,13 (t −2,47).
- Bayat fiyat riski: tüm hedef ETF'ler likit (medyan günlük hacim > 590 mn $); kapanış baskısı 16:00'da, bayat fiyat artefaktı beklenmez.

## 6. Diğer iddialar

**FOMC.** 87 karar gününde 6 faize duyarlı ETF'lik sepetin gün içi getirisi −30,1 bp (t −2,15; permütasyon p 0,0013). Ancak aynı günlerde SPY de −17,1 bp; sepet ile SPY farkı −13,0 bp (t −1,43). Etkinin çoğu FOMC gününün piyasa geneli zayıflığı; sektöre özgü kısım anlamlı değil. Ajan beta-hedge'li değeri −17 bp, t −2,3 buluyor; ben basit farkla bakıyorum. Her iki durumda "faize duyarlı sektöre özgü" vurgusu abartılı.

**Reddedilen kalıntı kuralı (11 SPDR, z1<−2 → al, C0 h1).** Net −14,2 bp, ajanla aynı. Red doğru. SPY-hedge'li brüt −6,4 bp (t −0,17): SPDR'lerde "kalıntı devamı" anlamlı değil.

**TradingView.** 105 kodun tamamı doğrulanmış. `tv_dogrulanacak` listesi (TWSE:2330, TVC:TWII, KRX:000660) doğru biçimde ayrılmış.

## 7. İzleme listesine itirazlar

- **SOXL (kabul → yedek/koşullu).**
  - Midas'ta bulunurluğu doğrulanmadı.
  - Risk eşdeğeri boyutta SMH'ye göre ek getiri yok.
  - Tam tutarla maxDD −%53; SOXL Haziran 2026'dan bu yana −%82.
- **SMH (kabul).** Kural düzeltilmeli: after-hours limit girişi, en az 2.500 $ pozisyon.
- **IGV (yedek).** "Doğrulanmış negatif gecikme" gerekçesi zayıf: SPY kontrolüyle kayboluyor ve kural brütü −6 bp. Strateji ya da özgün öncü yok; red ya da yalnız likit yedek.
- **XLK (yedek).** IBS kuralının OOS'u 5 bp; after-hours cezasıyla OOS ≈ 0. SMH ile korelasyonu 0,94; ayrı bir fırsat sunmuyor. Red önerilir.
- **KRE (yedek).** FOMC riski büyük ölçüde piyasa geneli (sepet − SPY t −1,43).
- **KWEB (yedek).** EEM öncüsü doğrulandı (yalnız filtre). Long strateji olmadığı için pratik değeri sınırlı.

## 8. Kaçırılan

1. **Uygulama: kapanış öncesi yerine kapanış sonrası limit emir.**
   - Sinyal günlerinde SMH son 15 dakikada da düşüyor; 15:45-15:55 fiyatı kapanışın 16-22 bp üstünde.
   - After-hours 17:00 ET fiyatı kapanışın yalnız +6 bp üstünde.
   - Kural: resmî kapanıştan sonra IBS'i hesapla; <0,20 ise after-hours'ta (kış TR 00:00-01:00 / yaz 23:00-00:00) resmî kapanış + birkaç sentlik limit emir ver.
   - Etkisi: 2.500 $'da net ~35 bp. Kapanış öncesi girişte ~23 bp.
2. **Oynaklık rejimi.**
   - Kenar düşük oynaklıkta ≈ 0; sabit 3 $ komisyon 1.000 $'da kenarı yiyor.
   - Eşik yalnız IS'te seçildi (IS medyanı, 20g yıllık oynaklık > %24) ve after-hours cezasıyla test edildi:
     - 2.500 $: 46,3 bp (t 3,17; OOS 40,2, t 2,00).
     - 1.000 $: 28,3 bp (t 1,93; OOS 22,2, t 1,10).
   - Komşu eşikler (q40 / q60) benzer sonuç veriyor. Mütevazı bir iyileşme; 1.000 $'da yine de eşik altında.
3. **Risk.** Şu an aşırı oynaklık rejimindeyiz (SMH 2026-11-05 −%11,2). S1 sinyalleri bu rejimde sık tetikleniyor ve tek işlemde SMH'de −%10, SOXL'de −%30 görülebilir. S1 sinyallerinin %70'i QQQ'da da IBS<0,20 olan günlere düşüyor (342/492). Regresyonda SMH IBS ve QQQ IBS katsayıları birbirine yakın: 31 bp (t 2,4) ve 32 bp (t 2,1). Bu nedenle S1, abd_endeks ailesinin QQQ IBS stratejisiyle (S2: IBS<0,10 + düşüş günü, 3 gün) aynı gün açılabilir; ikisi birlikte tutulursa aynı riske iki kez girilir.
