# Denetim: tek hisse kaldıraçlı aile (bağımsız)

Hazırlanma: 08.11.2026. Kod `kod/denetim_tek_hisse_kaldiracli/` (d0-d8), tablolar `sonuclar/aile_tek_hisse_kaldiracli/denetim/`, JSON `sonuclar/aile_tek_hisse_kaldiracli/denetim.json`.
Yöntem: işlem simülasyonu, RSI (Wilder/RMA, TradingView gibi SMA tohumlu), SMA, sentetik 2x ve havuz istatistikleri sıfırdan yazıldı. `lib.trades`, `lib.evaluate` ve `thk` kullanılmadı; `lib.load` yalnız ETF fiyatı için kullanıldı.

## 0. Hüküm

**S1 (TH03 hisse RSI(2) dibi → 2x tek hisse ETF): ZAYIF.**
* Sayılar birebir yeniden üretildi; kodda hata ya da ileriye bakma bulunmadı.
* Seçilmiş 7 hisse içinde zamanlama kenarı gerçek: permütasyon p 0,001-0,008. Parametre platosu da var.
* Ama aynı kural, hisseler ex-ante seçilince çalışmıyor. Bu, ajanın "düşük güven" uyarısından daha ağır bir sonuç:
  * S1 dışındaki 47 hissede net +11,5 bp (t=0,77), zamanlama kenarı +5,5 bp (t=0,37).
  * Kasım 2016'nın en büyük 30 hissesinde (S1'in 7'si hariç) net +8,9 bp (t=0,64).
  * Tek hisse kaldıraçlı ETF'i olan diğer 15 hissede (AMD, NFLX, PLTR, SMCI, MU...) +18,9 bp (t=0,60).
* Kenar iki yıldan geliyor. 2020 ve 2024 çıkarılınca C0 +52 bp (t=1,42), OOS +44 bp (t=0,79).
* Birleşik FDR'yi geçmiyor.
* Ajanın iki sayısı düzeltilmeli. maxDD -%11,5 değil, günlük değerlemeyle -%25,3. "Bilanço hariç" varyantı gerçekleşen tutuşa göre süzülmüş.

**Gecikmeli öncü:** ajanın "doğrulanmış gecikmeli öncü yok" sonucu doğru. Regresyonlar birebir çıktı. Tek hisse kuralına çevrilince hiçbiri t≥2'ye ulaşmıyor.

## 1. A merceği: kod ve zamanlama

| Kontrol | Sonuç |
|---|---|
| İşlem listesi | Denetim 605 işlem, ajan 605: **605'i ortak** (aynı hisse, sinyal ve çıkış günü) |
| Dayanak C0 / O1 / C1 | 111,0 bp t=3,13 / 101,2 t=2,93 / 75,9 t=2,14. IS 103,8 (2,01), OOS 117,1 (2,40). Ajanla aynı |
| Gerçek ETF (2022+) | C0 127,6 bp t=2,65 n=261; O1 107,8 t=2,38; C1 85,5 t=1,66. Ajanla aynı |
| Sentetik kalibrasyon (bağımsız) | Gerçek ETF − sentetik, 2x döneminde günde: NVDA -2,8, TSLA -2,8, AAPL -1,3, AMZN -2,1, META -1,8, MSFT -1,1, GOOGL -1,5, MSTR -13,0, COIN -5,1 bp. Corr 0,999-1,000. Ajanla aynı |
| İleriye bakma | Yok. RSI(2) ve SMA200 t kapanışına kadar. SMA5 çıkışı j kapanışında görülüp j kapanışında uygulanıyor. Bilanço takvimi önceden bilinir |
| Muhafazakâr çıkış (koşul kapanışta, satış ertesi açılış) | C0 139 bp t=3,39. Kapanışta çıkış varsayımı iyimser değil |
| Veri | Hisse serilerinde bölünme hatası yok. En büyük 5 kazanç gerçek olay: TSLA 24.10.2024 (+%21,9 bilanço), META 27.04.2023 (+%13,9 bilanço), NVDA 23.02.2023 (+%14,0 bilanço), TSLA 31.01.2022 (+%10,7), TSLA 09.09.2020 (+%10,9). `veri_duzeltmeleri`'nde satır yok. `veri_kalitesi`'ndeki TSLL 24.10.2024 satırı gerçek bilanço hareketi |

**Bulunan hatalar ve düzeltmeler:**
1. **maxDD olduğundan küçük.** Ajan "1/7 sermaye kaba portföy maxDD -%11,5" yazmış. Bu, sinyal-günü ortalamalarının ardışık çarpımıdır, açık pozisyonları günlük değerlemez. Günlük değerlemeli portföyde (her hisseye 1/7) maxDD **-%25,3**: 10.03.2020 → 18.03.2020, sekiz günde. 2020 dışında -%14,8 (2025). Portföyün yıllık getirisi %11,3, Sharpe 0,77, Newey-West t 2,75 (IS 1,77, OOS 2,20). O1'de NW t 2,29.
2. **"Bilanço hariç" +84 bp (t=2,44) uygulanamaz bir süzgeç.** İşlemler gerçekleşen tutuşa göre atılıyor. Çıkış günü ileriki fiyata bağlı: SMA5'le erken çıkan işlem kalıyor, bilançoya taşınan atılıyor. Uygulanabilir iki varyant şöyle:
   * **ATLA** (tepki günü t+1..t+3 içindeyse girme): C0 79,4 bp t=2,33, IS t 1,63, OOS t 1,66. Pozitif yıl oranı **%50**, %60 eşiğinin altında.
   * **ERKEN ÇIK** (duyuru günü E kapanışında sat): C0 98,4 bp t=2,87, IS 103,7 (2,03), OOS 93,9 (2,03), pozitif yıl %70. O1'de 75,1 t=2,39, ama OOS 53,5 (t=1,44).
   * Ajanın kuraldaki "muhafazakâr varyant" sayısı yerine bunlar yazılmalı.
3. **Güncel durum eksik yazılmış.** 06.11.2026 kapanışında yalnız NVDA ve TSLA değil, **META (610 < 632) ve GOOGL (285 < 340) da SMA200'ün altında**. Trend filtresi 7 hissenin 4'ünde kapalı. Açık olanlar: AAPL, AMZN, MSFT.
4. **AMZU öncü notu.** AMZN ← SPY için "OOS zayıf" yazılmış, ama bu ilişki OOS'ta da sürüyor: t -2,06 (IS -2,59). Yine de tek hisse kuralı olarak doğrulanmıyor (§3).

## 2. B merceği: istatistiksel sağlamlık

| Test | C0 | O1 |
|---|---|---|
| Rastgele giriş permütasyonu, tüm günler (2.000) | gerçek brüt 128 vs rastgele 53 bp, **p=0,008** | 116 vs 42, p=0,0045 |
| Permütasyon, rejim eşlenik (hisse>SMA200 günleri) | 128 vs 51, **p=0,003** | 116 vs 32, p=0,001 |
| Ortak dairesel kaydırma (kümelenme korunur, 1.000) | 128 vs 39, p=0,001 | 116 vs 27, p=0,001 |
| Parametre komşuluğu (RSI 6-14 × trend SMA 150/200/250 × çıkış SMA 3/5/7 × en uzun tutuş 2-5 gün = 180) | 180/180 pozitif, 158'inde t≥2, medyan 109 bp t=2,77. Ana kural t sırasında 50/180: plato, sivri tepe değil. RSI<8'de çukur var (78 bp t=1,85): gürültü | 125/180 t≥2 |
| 2020 hariç | 94 bp t=2,69 (IS 61, t=1,26) | 79 t=2,44 |
| 2022 hariç | 118 t=3,33 | 106 t=3,05 |
| 2020 ve 2022 hariç | 102 t=2,91 | 84 t=2,59 |
| **2020 ve 2024 hariç (en iyi iki yıl)** | **52 bp t=1,42; OOS 44 bp t=0,79** | 51 t=1,51 |
| En iyi 5 işlem çıkarılınca | 93 t=2,74 (IS 102, OOS 86) | 72,5 t=2,29 |
| En iyi 10 işlem çıkarılınca | 70 t=2,16 | 57,5 t=1,87 |
| 1.000$ pozisyon (30 bp komisyon) | 93,0 t=2,62; gerçek ETF 109,6 t=2,28 | 83,2 t=2,41; gerçek ETF 89,8 t=1,98 |
| C1 | 75,9 t=2,14 (1.000$'da 57,9 t=1,63) | |

Yıl yıl (C0, işlem başına ortalama net bp): 2017 +54, 2018 +50, 2019 +54, 2020 +132, 2021 +165 (t 2,50), 2022 -14, 2023 +71, 2024 **+273 (t 3,40)**, 2025 -71, 2026 +192 (t 2,26). Tek başına t≥2 olan yıllar yalnız 2021, 2024 ve 2026.

**Hayatta kalma / seçim yanlılığı testi (en önemli bulgu, `d4_evrenler.csv`).** Kural hiç değiştirilmeden başka hisselerde denendi: sentetik 2x, 16 bp maliyet. Zamanlama kenarı = işlem brüt getirisi − aynı hissede rejim günlerinden aynı süreli rastgele girişin ortalaması.

| Evren | Hisse | n | Net C0 (bp) | t | IS / OOS | Kenar (t) | Pozitif hisse oranı |
|---|---|---|---|---|---|---|---|
| S1'in 7 mega-cap'i (ex-post seçim) | 7 | 605 | 112,0 | 3,16 | 105 / 118 | 75,9 (2,12) | 1,00 |
| Kasım 2016'nın en büyük 30'u (S1'in 7'si hariç) | 30 | 2.151 | 8,9 | 0,64 | -10 / 24 | 18,5 (1,33) | 0,47 |
| Kasım 2016'nın en büyük 35'i (S1'in 5'i dahil) | 35 | 2.592 | 14,6 | 1,11 | 3 / 24 | 19,4 (1,46) | 0,54 |
| Tek hisse LETF'i olan diğer 15 hisse (AMD, NFLX, BA, PYPL, NKE, BABA, LLY, SMCI, PLTR, CRM, ADBE, QCOM, MU, UBER, SHOP) | 15 | 1.085 | 18,9 | 0,60 | 17 / 20 | -14,2 (-0,45) | 0,53 |
| TSM + AVGO | 2 | 185 | 76,6 | 1,51 | -18 / 161 | 40,4 (0,79) | 1,00 |
| **S1 dışı tüm hisseler** | 47 | 3.421 | **11,5** | **0,77** | 3 / 18 | **5,5 (0,37)** | 0,51 |

O1 sonuçları da aynı yönde: S1 dışı 47 hisse +13,0 bp t=0,90.

Sonuç: S1'in kenarı genel bir "büyük hisse ya da yüksek oynaklıklı hisse RSI(2) dibi" etkisi değil. Kenar, sonradan seçilmiş 7 kazanandaki V-dönüşlerinden geliyor. Bu hisseler tek hisse kaldıraçlı ETF'i çıkacak kadar popülerleştiği için seçildi. Bu yüzden S1'in "dayanakta 10 yıllık test" ve OOS kanıtı bağımsız değildir: seçim, OOS dönemi de bilinerek yapıldı. 7 hisse içindeki zamanlama kenarı (permütasyon p≈0,003) gerçek. Ama ileride sürmesi, bu hisselerin ayrıcalıklı konumunun sürmesine bağlı bir rejim bahsi.

**Piyasa geneli ve hisseye özgü dip:**
* Aynı gün QQQ RSI(2)<10 olan sinyaller (piyasa dibi): n=251, 111,5 bp, t=1,73, IS 50.
* QQQ RSI(2)≥10 olan sinyaller (hisseye özgü dip): n=354, 110,7 bp, t=2,61.
* QQQ'nun kendi sinyaliyle 2x QQQ: C0 73,7 (t=1,66), O1 16,9 (t=0,38). Etki piyasa endeksinden gelmiyor.

**Çoklu test:**
* Ajanın 7.310 testi ayrı ayrı sayıldı ve doğrulandı. Birleşik BH eşiği p≤4,1e-05, 4 test geçiyor.
* Denetim ~490 test ekledi (360 komşu varyant, 6 permütasyon, evren/bilanço/öncü testleri). Toplam ~7.800.
* S1'in p'si 0,0019. Birleşik FDR'yi de, Bonferroni'yi de geçmiyor.
* Yalnız dar, ön-kayıtlı TH01-TH07 ailesinde geçiyor (≈7 birincil test × 0,0019 ≈ 0,013).

**Midas uygulanabilirliği:**
* Uzun yön, açığa satış gerekmiyor. Bu ETF'ler 1940 Yasası kapsamında swap kullanan fonlar; PTP/K-1 beklenmez, ama Midas'ta "PTP" ibaresi kontrol edilmeli.
* Ürün bulunurluğu doğrulanmadı. MOC yok: C0 girişi TR kış 23:45-23:58'de canlı fiyatla limit ya da piyasa emri gerektirir.
* **Sinyal günlerinin %33'ünde RSI(2) 7-10 arasında**, yani eşiğe yakın. Bunun yanında 319 sinyal-olmayan günde RSI 10-13 arasındaydı. Kapanıştan dakikalar önceki karar bu günlerde dönebilir. O1 (101 bp, t=2,93) temiz yedek.
* En kötü işlem -%44,6 (TSLA 2x, Mart 2020). Gece riski 2x'tir.

## 3. Gecikmeli öncüler (bağımsız yeniden hesap, `d5_leadlag_regresyon.csv`)

r_hisse(t+1) = a + b·r_öncü(t) + c·r_hisse(t), Newey-West t:

| Hedef ← öncü | t (tam / IS / OOS) | 2x etki / 1 sd | Yetişme t (tam / IS / OOS) | Karar |
|---|---|---|---|---|
| AMZN ← SPY | -3,28 / -2,59 / **-2,06** | -51 bp (OOS -46) | -2,83 / -2,09 / -2,04 | İşaret tutarlı, negatif (piyasa geri dönüşü). Tek hisse kuralı (SPY z<-1/-1,5/-2 → AMZU 2x, 1 gün) t 1,1-1,6, OOS yarıya iniyor: **zayıf** |
| GOOGL ← SPY | -3,19 / -3,05 / -1,54 | -54 (OOS -26) | -3,05 / -2,75 / -1,61 | Kural C0 OOS negatif: **çürütüldü** (işlem için) |
| AAPL ← SPY | -2,84 / -3,57 / -0,67 | -48 (OOS -11) | | OOS etkisi maliyetin altında: **çürütüldü** |
| MSFT ← SPY | -2,48 / -2,65 / -0,84 | -48 (OOS -16) | | Kural OOS negatif: **çürütüldü** |
| NVDA ← XLK (yetişme) | -2,70 / -4,02 / +0,26 | -96 (OOS +9) | -2,65 / -3,59 / -0,13 | OOS'ta yok: **çürütüldü** |
| NVDA ← SMH | -1,92 / -2,96 / +0,31 | | -2,09 / -2,82 / -0,12 | **Çürütüldü** |
| TSLA ← QQQ | -0,34 | | | Yok |

* `leadlag_sweep.csv`'de 576 aile satırında FDR bayrağı 0. Ajanla uyumlu.
* Likit mega-cap hisse ve ETF'lerde bayat fiyat artefaktı beklenmez. Bulunan ilişkiler zaten negatif işaretli (ortalamaya dönüş), bayat fiyatın üreteceği pozitif yetişme değil.
* **Gerçek zamanlı izleme (öncü değil):** BTC'nin 16:00 ET → ertesi 09:00 ET hareketi MSTR açılış boşluğuyla corr **0,880** (beta 1,23, R² 0,77, n=863, 2023-06+). COIN için corr 0,776. Ajanın iddiası doğrulandı. MSTU için COINBASE:BTCUSD gece izleme aracıdır.
* TradingView kodları: kullanılan tüm kodlar `tv_etf.csv` ve `tv_dogrulama.csv`'de "dogrulandi": NASDAQ:NVDL/TSLL/AAPU/AMZU/METU/MSFU/GGLL/NVDU/CONL/TSLQ/NVDS, CBOE:MSTU, NASDAQ:NVDA/TSLA/AAPL/AMZN/META/MSFT/GOOGL/MSTR, AMEX:SPY/XLK/DIA/XLF/HYG/BITO, NASDAQ:QQQ/SMH/IBIT, CBOE:VIX, CME_MINI:NQ1!, COINBASE:BTCUSD, CME:BTC1!, OSE:NK2251!. `tv_dogrulanacak` boş kalabilir.

## 4. İzleme listesi itirazları

* **AAPU: kabul → yedek önerilir.** AAPL S1'in en zayıf dayanağı: C0 54 bp t=0,93, O1 36 bp, C1 **-7 bp**; gerçek ETF 35 bp t=0,57. Maliyet/oynaklık 0,051, kabul edilenlerin en kötüsü. Kabul için tek gerekçe dayanak sürücüsü kalıyor.
* **METU: kabul → yedek önerilir.** Gerçek ETF'te S1 C0 -45, O1 -100, C1 **-217 bp**. Geçmişi kısa (2024-06+). Sentetikte de en zayıf (45 bp t=0,66).
* **TSLL kabul edilebilir, ama** 8,8$ fiyatla 1 sentlik adım ~11 bp makas, toplam maliyet 23 bp, 2x TSLA'da en kötü işlem -%45. Pozisyon küçük tutulmalı.
* Genel: "kabul" gerekçesi "S1 sepetinin aracı" diye yazılmış. S1 zayıf olduğu için kabulün dayanağı, likidite ve dayanak hissenin net sürücü olmasıdır. Bu açıkça yazılmalı.
* MSTU "yedek" ve CONL, TSLQ, NVDS "red" kararlarına itiraz yok.

## 5. Kaçırılan

1. **Aynı sinyali doğrudan hisseyle uygulamak.** Midas'ta ABD hisseleri kesin var; kaldıraçlı ETF bulunurluğu doğrulanmadı. 1x hisse, C0, 2.500$: net 57,9 bp, **t=3,27** (IS 2,13, OOS 2,48), en kötü işlem -%23. 5.000$ hisse, 2.500$'lık 2x ETF ile aynı dolar maruziyetidir: 63,9 bp, t=3,61. İşlem başına net ~32$, 2x ETF'te ~28$. Swap sürüklemesi (3 günde 10-15 bp), fon kapanma ve ürün bulunurluğu riski olmaz. Sermaye kısıtı yoksa daha sağlam araç budur. Kaldıraç yalnız sermaye verimliliği için gerekir.
2. **Hayatta kalma testi ve gerçek drawdown** (§2). Aile notunda seçim yanlılığı nitel olarak yazılmış ama test edilmemiş. Ex-ante evren testi kenarı 5-19 bp'ye (t<1,5) düşürüyor. Bu, S1'in en önemli riskidir.
3. **Yaklaşan olay.** NVDA bilançosu 17.11.2026 seans sonrası. NVDA şu an SMA200'ün altında, yani S1 sinyali üretmez. "Erken çık" kuralı yine de not edilmeli.

## 6. Tekrar üretim

```
python3 -I kod/denetim_tek_hisse_kaldiracli/d0_veri.py          # ex-ante evren verisi (Nasdaq; önbellekli, kod/denetim_.../veri/)
python3 -I kod/denetim_tek_hisse_kaldiracli/d1_kalibrasyon.py
python3 -I kod/denetim_tek_hisse_kaldiracli/d2_S1_yeniden.py     # A merceği + yıllar, en iyi işlemler, bilanço, gerçek ETF, günlük portföy
python3 -I kod/denetim_tek_hisse_kaldiracli/d3_saglamlik.py      # permütasyon + 360 komşu varyant
python3 -I kod/denetim_tek_hisse_kaldiracli/d4_hayatta_kalma.py  # ex-ante evren, piyasa ayrıştırması
python3 -I kod/denetim_tek_hisse_kaldiracli/d5_leadlag.py
python3 -I kod/denetim_tek_hisse_kaldiracli/d6_ek.py             # 1x hisse, SPY-düşüş kuralı, güncel durum
python3 -I kod/denetim_tek_hisse_kaldiracli/d7_bilanco_uygulanabilir.py
python3 -I kod/denetim_tek_hisse_kaldiracli/d8_dd_esik.py
```
