# Denetim: C0 (aynı kapanışta giriş) lead-lag taraması ve TLT örüntüsü (10.11.2026)

Denetlenen dosyalar: `kod/c0_leadlag.py`, `kod/lib.py` (trades, stats, cost_bp), `kod/leadlag_sweep.py` (build_panel), `sonuclar/c0_leadlag.csv`.
Denetim kodu: `kod/denetim_c0/` (lib.trades, lib.stats, lib.cost_bp ve build_panel kullanılmadı; yalnız `lib.load` fiyat katmanı olarak kullanıldı. Öncüler ham parquet dosyalarından yeniden kuruldu.) Hepsi `python3 -I` ile ve tek süreçle çalıştırıldı.

## Özet

| Görev | Sonuç |
|---|---|
| 1. Kod doğruluğu | 25/25 satır birebir yeniden üretildi (n, net_bp, t, maliyet). Benim kurduğum öncü paneli build_panel ile aynı (max fark 0, NaN deseni aynı). Maliyet bir kez düşülüyor. |
| 2. Zamanlama | Tarih kayması yok. BTC/ETH 16:00 ET doğru. VIX ailesinde 15 dk'lık hafif ileriye bakış var (küçük). **Hata:** Hazine öncülerinde z-skoru günlerin %30'unda NaN, OVX/GVZ'de %10. İleriye bakış değil, olay kaybı. "0 geçen" sonucu yapay değil. |
| 3. TLT örüntüsü | Sayılar birebir doğru. Ama seçim düzeltmeli p = 0,54 / 0,61 / 0,85 / 0,79 (dört ayrı null). Gözlenen 1. sıra değeri (medyan t 1,379), bilgisiz bir dünyada 576 kombinasyonun en iyisinin **tipik** değerinin altında kalıyor. QQQ/SPY'de en iyi 5 işlem çıkarılınca sonuç kayboluyor. **Karar: çürütüldü** (bir keşif ya da kural olarak). |
| 4. Kaçırılan | **Yok.** Taramanın kapsamadığı seviye tabanlı VIX öncüleri ve çok günlük öncü getirisi kısaca test edildi. Hiçbiri anlamlı değil. |

## 1) Kod doğruluğu

`d1_yeniden.py`: CSV'den rastgele 15 satır (tohum 20261110) ve t'ye göre en iyi 10 satır, kendi C0 simülasyonumla yeniden üretildi. Simülasyonun kuralları şöyle:
- t kapanışında al, t+h kapanışında sat.
- Pozisyondayken gelen sinyal atlanır.
- Çıkış günü gelen sinyalle aynı kapanışta yeniden girilebilir.
- Maliyet bir kez düşülür: 12 bp + makas kademesi, 1 sentlik adım tabanıyla.

Sonuç: **25/25 satırda n, net_bp, t ve maliyet birebir aynı** (fark 0,00). Tablo `kod/denetim_c0/d1_yeniden.csv` dosyasında. Örnekler:

| küme | hedef | öncü | tip | h | n | net bp | t |
|---|---|---|---|---|---|---|---|
| en iyi t | WCLD | XLK | ONDE | 2 | 33 | 136,2 | 3,67 |
| en iyi t | ASHR | TLT | L_UP | 1 | 62 | 71,0 | 3,58 |
| en iyi t | SMH | XLK | ONDE | 2 | 75 | 107,6 | 3,40 |
| rastgele | ARKK | VIX_dlog | ONDE | 3 | 87 | 74,3 | 1,55 |
| rastgele | EFA | EWJ | GERIDE | 3 | 59 | −62,4 | −2,26 |

Tüm CSV'de max |brüt − net − maliyet| = 3e-13, yani maliyet iki kez düşülmüyor. Beta, kalıntı oynaklığı ve öncü oynaklığı `shift(1)` ile t−1'e kadar alınıyor; bu doğru.

## 2) Zamanlama ve yapay sıfır kontrolü (`d2_zamanlama.py`, `d6_hazine_duzeltme.py`)

**Tarih hizalaması.** Her öncünün referans ETF ile korelasyonu gecikme 0'da en büyük; ±1, ±2 gecikmede yaklaşık 0. Kayma yok.

| öncü | referans | gecikme −1 | gecikme 0 | gecikme +1 |
|---|---|---|---|---|
| VIX_dlog | SPY | 0,107 | −0,731 | 0,054 |
| DGS10_d | IEF | −0,030 | −0,972 | 0,017 |
| DGS30_d | TLT | −0,040 | −0,953 | 0,030 |
| BTC_16ET | IBIT | −0,068 | 0,999 | −0,076 |
| ETH_16ET | ETHA | −0,042 | 0,999 | −0,053 |

**BTC/ETH saati.** Coinbase mum zaman damgası mumun başlangıcıdır. IBIT kapanış getirisiyle korelasyon şöyle:

| mum başlangıcı (ET) | 14:00 | **15:00** | 16:00 |
|---|---|---|---|
| korelasyon | 0,9645 | **0,9988** | 0,9666 |

Kodun seçtiği mum (15:00 başlangıçlı, kapanışı 16:00 ET) doğru. İleriye bakış yok.

**VIX ailesi (kapanış 16:15 ET).** VIX'in SPY'nin 16:00 getirisiyle açıklanmayan kısmı, ertesi sabahki SPY gece boşluğuyla −0,096 korelasyonlu. Bu, 16:00 ile 16:15 arasındaki bilginin sızdığını gösteriyor; sızıntı küçük ama gerçek.
- Yönü şöyle: VIX L_DN ve VVIX L_DN gibi "oynaklık düştü, al" kurallarını hafifçe şişirir, L_UP kurallarını hafifçe bastırır.
- VVIX_dlog L_DN h3, medyan t sıralamasında 5. (0,845). Bu sıranın bir kısmı sızıntıdan gelebilir.
- TLT bulgusuyla ilgisi yok.

**Hazine (~15:30 ET teklifleri).** İleriye bakış yok; veri 16:00'a göre 30 dk eski. Tek pratik not: resmî seri kapanıştan sonra yayımlanıyor, bu yüzden canlı uygulamada anlık faiz ya da TLT'nin kendisi kullanılmalı.

**HATA: z-skorunda NaN kaybı.** `z_of` ve kalıntı tarafındaki `rolling(60)` varsayılan olarak `min_periods=60` kullanıyor. Pencerede tek bir NaN bile olsa z, 60 gün boyunca NaN oluyor.
- Hazine Columbus ve Veterans günlerinde kapalı, borsa açık. SPY takviminde 18 eksik gün var ve her biri iki NaN fark üretiyor.
- Sonuç: **DGS10_d, DGS2_d, DGS30_d, DFII10_d ve T10YIE_d'de günlerin %30,1'inde z = NaN.** Her yıl Ekim–Ocak dönemi kayboluyor.
- OVX ve GVZ'de 4 eksik gün nedeniyle oran %9,8.
- Etki: Hazine olaylarının %25–35'i kayboluyor. Örneğin DGS10 z ≤ −2 olay sayısı 47'den 63'e çıkması gerekirken 47'de kalıyor.
- Hatayı düzelttim (z'yi serinin kendi takviminde hesaplayarak). En iyi Hazine kombinasyonu T10YIE_d L_UP h2 oluyor ve medyan t'si 0,887'den 1,224'e çıkıyor. Bu yine de TLT'nin 1,379'unun altında, yani 1. sıra değişmiyor. Bu hata "0 geçen" sonucunu açıklamaz.

**"0 geçen" yapay mı? Hayır.**
- En küçük tek yönlü p değeri 3,4e-4. BH %10'da 1. sıranın geçmesi için p ≤ 0,1/m gerekiyor; bu p ancak aile m ≤ 290 test olsaydı geçerdi.
- Taramanın üst kuyruğu şansın bile altında. t > 2,5 olan test sayısı gözlenende 139. Aynı sayının null medyanı dairesel kaydırmada 366, rastgele günde 512, wild bootstrap'ta 301 (p = 0,91–1,0).
- En büyük t gözlenende 3,67, null medyanında 4,1–4,5.
- Sinyaller doğru günlere oturuyor. Örneğin 62 TLT z ≥ 2 gününde TLT ortalama +213 bp (en az +108 bp) yükselmiş.
- z hiçbir zaman toptan NaN değil; NaN yalnız yukarıdaki serilerde.

**Diğer küçük iyimserlikler (ileriye bakış sayılmaz):**
1. Makas kademesi son 252 günün dolar hacminden geliyor. 2017 için maliyet hafifçe düşük tahmin ediliyor. QQQ, SPY ve SMH'de makas 1 bp olduğundan önemsiz.
2. C0'da sinyal kapanış fiyatıyla hesaplanıyor ve aynı fiyattan giriliyor. Gerçekte sinyal, kapanış emri kesim saatinden (15:50–15:59 ET) önce tahmin edilmek zorunda.
3. GERIDE ve OWN_DN, hedefin kendi kapanışını kullanıyor. Alış fiyatından gelen kapanışlar mekanik geri dönüş üretir (bid-ask sıçraması). Tam makas maliyete eklendiği için bu kısmen karşılanıyor.

## 3) TLT örüntüsü: TLT z ≥ 2 → kapanışta QQQ / SPY / SMH al

### (a) Bağımsız uygulama (`d4_tlt.py`): birebir doğru

| hedef | h | n | net bp | t | IS t (≤2021) | OOS t | koşulsuz 3g brüt bp |
|---|---|---|---|---|---|---|---|
| QQQ | 1 | 62 | 36,9 | 1,33 | 1,70 | −0,27 | |
| QQQ | 3 | 56 | 75,3 | 2,03 | 1,64 | 1,18 | 23,6 |
| SPY | 3 | 56 | 60,7 | 1,88 | 1,47 | 1,19 | 17,8 |
| SMH | 3 | 56 | 136,5 | 2,79 | 1,89 | 2,06 | 38,1 |

210 hedefin %72,4'ü pozitif; bu da doğru.

### (b) Seçim düzeltmesi (`d3_secim.py`, `d3b_analiz.py`, `d7_wild.py`; P = 1000)

İstatistik, 576 kombinasyonun (48 öncü × 4 tip × 3 tutuş) her birinde hedefler arası medyan t. 547 kombinasyonda en az bir hedef var.
- Gözlenen sıralama: TLT L_UP h3 1,379; DBA L_DN h1 0,890; T10YIE_d L_UP h2 0,887; IEF L_UP h3 0,848; VVIX L_DN h3 0,845.
- Null'larda olay günleri rastgeleleştirildi ve her (öncü, tip, hedef, h) için işlem sayısı korundu.

| null | null'da max medyan t: q50 | q95 | **seçim düzeltmeli p** | TLT L_UP h3 tek başına p |
|---|---|---|---|---|
| A: dairesel kaydırma, tüm öncülere aynı ofset (bağımlılık korunur) | 1,41 | 2,05 | **0,54** | 0,012 |
| B: dairesel kaydırma, her öncüye ayrı ofset | 1,44 | 2,05 | **0,61** | 0,009 |
| C: rastgele gün (öncü/tip başına ortak gün havuzu) | 1,63 | 2,34 | **0,85** | 0,016 |
| D: wild bootstrap (olay günü oynaklığı korunur; aynı takvim gününe ortak ±1) | 1,63 | 2,31 | **0,79** | 0,021 |

- Gözlenen 1. sıra değeri 1,379, her null'da "en iyi kombinasyonun" medyan değerinin altında. Bilgisiz bir taramada 1. sıranın en az bu kadar iyi görünmesi normal.
- Tek başına (önceden belirlenmiş olsaydı) p ≈ 0,01–0,02 olurdu. Tek hedeflerde unadjusted p: QQQ h3 0,05–0,06, SMH h3 0,01–0,02.
- Pozitif hedef oranı %72,4. Tek başına p ≈ 0,05–0,06 (ana ajanın "p ≈ 0,05" bulgusu buna karşılık geliyor).
- Seçim düzeltmeli p (≥150 hedefli kombinasyonlar) 0,29–0,38. Ayrıca en yüksek pozitif oran TLT'de değil, T10YIE_d L_UP h2'de (%77,9).

### (c) Sağlamlık (net bp / t; h = 1, 2, 3)

| varyant | QQQ h3 | SPY h3 | SMH h3 | QQQ h1 / h2 t |
|---|---|---|---|---|
| TLT z ≥ 1,5 (n = 123) | 46 / 2,02 | 28 / 1,44 | 87 / 2,68 | 1,12 / 1,18 |
| **TLT z ≥ 2 (n = 56)** | 75 / 2,03 | 61 / 1,88 | 136 / 2,79 | 1,33 / 1,17 |
| TLT z ≥ 2,5 (n = 26) | 54 / 0,98 | 39 / 0,77 | 91 / 1,15 | 0,69 / 0,23 |
| DGS10 dz ≤ −2, tarama tanımı (NaN kayıplı, n = 42) | 51 / 1,17 | 36 / 0,95 | 69 / 1,16 | 0,37 / 0,72 |
| DGS10 dz ≤ −2, Hazine takvimi (düzeltilmiş, n = 59) | 66 / 1,92 | 52 / 1,73 | 115 / 2,37 | 1,38 / 1,43 |
| DGS30 dz ≤ −2, Hazine takvimi | 38 / 1,23 | 33 / 1,22 | 76 / 1,80 | 1,45 / 0,37 |
| 2020 hariç | 53 / 1,47 | 41 / 1,40 | 109 / 2,36 | 0,95 / 0,88 |
| **en iyi 5 işlem hariç** | **25 / 0,76** | **15 / 0,55** | 70 / 1,67 | −0,18 / −0,14 |
| 2020 hariç + en iyi 5 hariç | 4 / 0,11 | 2 / 0,06 | 47 / 1,13 | −0,46 / −0,59 |
| C1 (ertesi kapanışta giriş) | 54 / 1,33 | 49 / 1,15 | 113 / 2,12 | −0,37 / 0,23 |

- **Yoğunlaşma.** QQQ h3'te en iyi 5 işlem toplam net kârın %70'i: 2020-03-20, 2019-01-03, 2020-02-28, 2024-11-04, 2020-03-16. Bunların 3'ü COVID çöküşünde. SMH'de bu pay %53.
- **Eşik komşuluğu.** 2,5'te sonuç çöküyor. h1 ve h2 her yerde zayıf. Etki yalnız h3'te ve yalnız 2 eşiği çevresinde.
- **Hazine eşdeğeri.** Düzeltilmiş DGS10 sinyali benzer büyüklük veriyor. Ama TLT ile DGS10 değişimi −0,97 korelasyonlu, yani bu bağımsız bir kanıt değil.
- **Mekanizma.** TLT z ≥ 2 günlerinin %77'sinde SPY düşmüş (ortalama −99 bp). Bu bir "riskten kaçış sonrası toparlanma" örüntüsü:

  | koşul | n | QQQ h3 net bp | t |
  |---|---|---|---|
  | TLT z ≥ 2 ve SPY < 0 | 42 | 96 | 2,02 |
  | TLT z ≥ 2 ve SPY ≥ 0 | 14 | 13 | 0,34 |

- **Koşulsuz kayma.** Tüm günler üzerinde HAC regresyonuyla, koşulsuz kaymaya göre kenar: QQQ kukla katsayısı 45 bp (t 1,00), SPY 32 bp (t 0,71), SMH 82 bp (t 1,42). Kenar koşulsuz kaymadan anlamlı biçimde ayrışmıyor. SMH'nin t'si büyük ölçüde SMH'nin olağanüstü kaymasından geliyor: koşulsuz 3 günlük brüt getiri +38 bp. SMH "SPY z ≤ −1,5" gibi başka düşüş sinyallerinde de t 2,3 veriyor.

### (d) 1.000 $ pozisyon (komisyon 30 bp + makas)

| hedef | h | net bp | t |
|---|---|---|---|
| QQQ | 3 | 57 | 1,55 |
| SPY | 3 | 43 | 1,33 |
| SMH | 3 | 118 | 2,43 |
| SPY | 1 | 2 | 0,10 |
| SPY | 2 | 3 | 0,11 |

### Karar: **çürütüldü** (keşif ya da kural olarak)

Rakamlar doğru. Ancak örüntünün 576 kombinasyon içinde 1. çıkması, bilgi içermeyen olay günleriyle beklenen sonuçtan ayırt edilemiyor (p = 0,54–0,85). QQQ ve SPY'de etki 5 işleme, özellikle Mart 2020'ye dayanıyor. Komşu eşikte (2,5) ve kısa tutuşlarda (h1, h2) çöküyor. Koşulsuz kaymaya göre anlamlı değil (t ≈ 1).

"Riskten kaçış günü (TLT↑ ve SPY↓) sonrası hisse toparlanması" ekonomik olarak makul. Yalnız örneklem dışında izlenecek bir hipotez olarak tutulabilir, işlem kuralı olarak önerilmemeli.

## 4) Kaçırılan (`d5_kacirilan.py`)

Tarama yalnız 1 günlük öncü z'si ve VIX/VIX3M oranının günlük değişimini kullanıyor. Literatürde ve uygulamada bilinen ama taramada olmayan üç öncü C0, yalnız long ve maliyetli olarak kısaca test edildi (SPY ve QQQ, h = 1–3):

| sinyal | en iyi sonuç | en iyi 5 hariç t |
|---|---|---|
| VIX/VIX3M ≥ 1 (vade yapısı ters dönmüş) | QQQ h3: 59 bp, t 1,59, n = 87; IS t 0,95 | 0,56 |
| Connors "VIX stretch" (VIX ≥ 1,10 × SMA10) | QQQ h3: 16 bp, t 0,78 | |
| SPY 5 günlük z ≤ −2 | QQQ h2: 56 bp, t 1,21 | |

Hiçbiri anlamlı değil. VIX sinyallerinde ayrıca 16:15 sızıntısı var. HY OAS (FRED) panelde yok, ama HYG öncü olarak taramada mevcut. **Sonuç: yok.**

## Dosyalar

- `kod/denetim_c0/ortak.py`: bağımsız öncü paneli, maliyet, z ve C0 simülasyonu.
- `d1_yeniden.py` / `d1_yeniden.csv`: Görev 1.
- `d2_zamanlama.py` / `d2_z_nan.csv` ve `d6_hazine_duzeltme.py` / `.csv`: Görev 2.
- `d3_secim.py`: null A, B, C. Yaklaşık 3 dakika sürer ve ~1,1 GB'lık bir npz üretir; bu dosya depo dışında tutuldu. Kullanım: `python3 -I kod/denetim_c0/d3_secim.py 1000 <npz_yolu>`, ardından `d3b_analiz.py <npz_yolu>`. Sonuçlar `d3_sonuc.csv` dosyasında.
- `d7_wild.py` / `d7_wild.npz`: null D.
- `d4_tlt.py` / `d4_a.csv`, `d4_c.csv`: Görev 3a, 3c ve 3d.
- `d5_kacirilan.py` / `.csv`: Görev 4.
