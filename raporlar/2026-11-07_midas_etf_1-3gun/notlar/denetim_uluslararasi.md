# Bağımsız denetim: aile "uluslararası"

Hazırlanma: 07.11.2026. Denetlenen: `notlar/aile_uluslararasi.md`, `sonuclar/aile_uluslararasi/sonuc.json`, `kod/ajan_uluslararasi/*`.
Denetim kodu: `kod/denetim_uluslararasi/` (d1-d7, `sim.py`). Tablolar: `sonuclar/aile_uluslararasi/denetim/`.
Makine okunur sonuç: `sonuclar/aile_uluslararasi/denetim.json`.
Yöntem: işlem simülasyonu `lib.trades`/`lib.evaluate`/`ortak.pooled` KULLANILMADAN yeniden yazıldı (`sim.py`); fiyat için yalnız `lib.load`.
Maliyet: `tarama.csv` makası + 2 x 1,5 USD komisyon. Tüm betikler `python3 -I` ile, tek süreçte çalıştırıldı.

## 0. Kısa sonuç

| Bulgu | Ajan | Denetim kararı | Gerekçe (özet) |
|---|---|---|---|
| uluslararasi_S1 (UL03 Asya sepeti) | aday, güven orta | **zayıf** | Sayılar birebir üretildi, zamanlama temiz. Eşik t ≥ 2 yalnız Newey-West ile sağlanıyor (basit t 1,99). 6 birincil hipotez içindeki FDR "geçer" sonucu da NW'ye bağlı (basit t ile p = 0,024 > 0,0167). En iyi 5 gün çıkarılınca t 0,79. 1.000 $'da t 1,35. Kapanışa bağımlı. Göreli mekanizma (ETF ≤ SPY seçimi) ise permütasyonla destekleniyor. |
| uluslararasi_S2 (EWY IBS) | keşifsel, güven düşük | **zayıf** | Sayılar birebir üretildi. 20.196 satırlık taramadan seçilmiş. IS t 1,29. 2026 hariç t 1,70. Kardeş Asya ETF'lerinde tekrar etmiyor. C1 brüt 0,75 bp. |
| "Doğrusal gecikmeli öncü yok" | iddia | **doğrulandı** | Aile içi 5.370 lag testinde BH-FDR (q = 0,10) geçen 0. Taramadaki t'ler bağımsız regresyonla ±0,1 içinde tekrarlandı. |
| KWEB→EEM, IWM→EWA, VIX→EWA, TIP/DFII10→EWY, DXJ←QQQ | çoğu "aday/kullanılamaz" | **çürütüldü / zayıf** | Kısmi regresyon katsayısı pozitif çıkıyor, ama eşik kuralı olarak net negatif ya da sıfır (ör. IWM z ≥ 1 → EWA net −30 bp, t −3,35). |

**Kabul eşiğini sağlam biçimde geçen strateji yok.** S1 en fazla "izleme / keşif sinyali" olarak tutulabilir.

## 1. S1 — kod ve zamanlama (mercek A)

* **Yeniden üretim, birebir** (`d1_s1_yeniden.py`): 110 sinyal günü, 293 işlem, brüt 70,37 bp, net 55,84 bp, NW t 2,22, IS 68,0 / OOS 45,7 bp, yılların %78'i pozitif, en kötü işlem −1.356 bp (EWA 11.03.2020). ETF bazındaki sayılar da aynı (EWY 108 bp t 2,41; EWT 63 t 2,00; FXI 37 t 1,17; EWJ 30 t 1,21; EWA 51 t 0,97; EWH 49 t 1,54).
* **İleriye bakma yok:**
  * Sinyal t kapanışındaki SPY ve ETF getirisiyle hesaplanıyor.
  * Giriş c[t], çıkış c[t+1]: tarih uyumsuzluğu 0 işlem.
  * SPY ile ETF takvimleri arasında fark yok.
  * Düzeltilmiş ve ham fiyatla üretilen sinyaller aynı (0 gün fark). EWT'deki iki "kayıp dağıtım" düzeltmesi sinyal üretmiyor.
* **En büyük kazançlar** (tümü veri_kalitesi.csv'de bayraksız; gerçek kriz günleri):

| Sinyal günü | ETF | Net bp | Not |
|---|---|---|---|
| 12.03.2020 | EWA | +1.399 | +1.382 bp'si gece boşluğu |
| 23.03.2020 | EWY | +1.232 | |
| 23.03.2020 | EWA | +1.209 | |
| 29.07.2026 | EWY | +1.166 | |
| 10.06.2026 | EWY | +1.135 | |

  2026'daki EWY hareketleri KORU ile tutarlı (2026'da β 2,92, korelasyon 0,999). Veri hatası değil, ama olağandışı bir oynaklık rejimi: EWY'nin günlük oynaklığı 2026'da 403 bp, 2017-2025'te 100-256 bp.
* **Getirinin kaynağı:** işlem başına ortalama gece boşluğu (c_t → o_t+1) +63 bp, ertesi gün içi +13 bp.
* **Kural metni ile backtest uyumsuz.** Metin "çıkış günü yeniden sinyal varsa pozisyon korunur" diyor; backtest ise çıkıp yeniden giriyor ve ek maliyet ödüyor.
  * Metne uygun "koru" sürümü: net 57,5 bp, basit t 2,54, en kötü −852 bp.
  * Ama bu sürümde de en iyi 5 gün hariç t 1,28; 2020+2026 hariç t 1,19 (`d7_hold.py`).
* **KORU verisinde tutarsızlık:** 17.03.2020'de EWY +%7,2 iken KORU −%13,2. Kaldıraçlı sonuçlara güveni azaltıyor.

## 2. S1 — istatistiksel sağlamlık (mercek B, `d2_s1_saglamlik.py`)

* **t istatistiği:** gün-kümeli seride basit t **1,99**. NW(1) 2,22, NW(3) 2,12.
  * NW'nin t'yi yükseltmesinin nedeni, düzensiz aralıklı ardışık sinyal günleri arasındaki −0,19 otokorelasyon (kriz günü → toparlanma günü). Ardışık sinyaller arası medyan aralık 10 takvim günü.
  * h = 1 C0 işlemleri zamanda çakışmadığı için NW düzeltmesine gerekçe yok. Doğru ölçüt basit t'dir; eşik t ≥ 2 **sınırda sağlanmıyor**.
* **Çoklu test:**
  * Basit t ile tek yönlü p = 0,024. 6 birincil hipotezde BH için ilk sıra eşiği 0,1/6 = 0,0167 → **geçmez**. Ajanın "6 hipotez içinde geçer" sonucu NW t'ye (p = 0,013) bağlı.
  * Bonferroni(6) eşiği 0,0083 → geçmez.
  * Ajanın kendi 564 testi içinde de geçmez. Bu denetimin ~280 sağlamlık değerlendirmesi yeni strateji aramak için değildi.
* **Yıl yıl** (sinyal günü ortalaması, net bp): 2018 −6, 2019 +74, 2020 +122, 2021 +76, 2022 +18, 2023 +30, 2024 −46, 2025 +34, 2026 +200.
* **Alt örnekler** (C0, h = 1, 2.500 $):

| Alt örnek | Net bp | Basit t | Not |
|---|---|---|---|
| 2020 hariç | 41,1 | 1,83 | |
| 2022 hariç | 66,3 | 1,93 | |
| 2026 hariç | 41,4 | 1,43 | OOS 14,9 |
| 2020 + 2022 hariç | 49,3 | 1,79 | |
| 2020 + 2026 hariç | 21,2 | 1,00 | |
| Mart 2020 hariç | 44,7 | 2,14 | |
| En iyi 5 işlem hariç | 43,6 | 1,71 | |
| **En iyi 5 gün hariç (110 günden)** | **18,7** | **0,79** | |
| En iyi 10 işlem hariç | 31,8 | 1,33 | |

* **Parametre komşuluğu** (k = 1, SPY eşiği): eşik ilerledikçe OOS işareti dönüyor; −1,5 en iyi t.

| SPY eşiği | Net bp | Basit t | OOS net bp |
|---|---|---|---|
| −1,0 | 28 | 1,65 | 15 |
| −1,25 | 38 | 1,71 | 21 |
| −1,5 | 56 | 1,99 | 46 |
| −1,75 | 47 | 1,37 | −14 |
| −2,0 | 75 | 1,76 | 2 |
| −2,5 | 85 | 1,33 | −31 |

  Ajan yalnız −1,0 ve −2,0'ı raporlamış. Göreli koşulu sertleştirmek (ETF ≤ 1,25·SPY) brüt kenarı büyütüyor; bu, mekanizmayla tutarlı ve monoton bir ilişki. Tümleyen grup (ETF > SPY) her eşikte net ≈ 0.
* **Permütasyon** (her biri 5.000 tekrar):
  * (a) Rastgele tarih, ETF yapısı korunarak: p = 0,0002. Saf boş hipotez; bilgi vermez.
  * (b) Aynı SPY düşüş günlerinde, aynı sayıda ETF'in rastgele seçimi: gözlenen 55,8 bp, simülasyon ortalaması 35,4 bp, **p = 0,0014**.
  * (c) SPY ≤ −%1,5 günlerinden rastgele gün ve rastgele ETF: p = 0,0036.
  * Eşleştirilmiş fark (aynı gün ETF ≤ SPY eksi ETF > SPY): +39,7 bp, t 2,84, IS 38,8 / OOS 40,5; 2020 hariç t 2,39.
  * **Yorum:** göreli aşırı tepki (Levy-Lieberman) gerçek görünüyor. Ancak uzun-tek yönlü mutlak getirinin büyük kısmı, birkaç kriz gününde tüm piyasanın toparlanmasından geliyor (rastgele seçimle bile 35 bp).
* **Maliyet ve uygulanabilirlik:**
  * Pozisyon büyüklüğüne göre: 1.000 $'da net 37,8 bp (t 1,35); 10.000 $'da 64,8 bp (t 2,31).
  * Stres günü makası +10 bp → t 1,64; +20 bp → t 1,28.
* **Kapanışa bağımlılık** (`d6_kapanis_oncesi.py`):
  * Ertesi gün açılışta girişte (O1, h = 1) net −1,7 bp; ertesi gün kapanışta girişte (C1, h = 1) net 25 bp (t 1,06).
  * Kenar, kapanışı gün dibine yakın olan işlemlerde toplanıyor. 12 Asya ETF'inde IBS < 0,1: net 77 bp; IBS ≥ 0,6: −81 bp. Yani C0 varsayımı tam da en iyimser olduğu işlemlerde para kazandırıyor (son dakika satışı).
  * Kapanıştan ~10 dk önce giriş vekili (giriş = c + f·aralık; sinyal günlerinde ortalama aralık 232 bp): f = 0,03 → t 1,75; 0,05 → t 1,59; 0,10 → t 1,18.
* **Post-hoc kontrol:** S1 ∩ IBS < 0,3 de en iyi 5 gün çıkarılınca t 0,92'ye iniyor. Yeni kural olarak önerilmez.
* **Midas:**
  * Açığa satış gerekmez; MOC olmadığından kapanıştan önce piyasa/limit emri ya da after-hours limit emri gerekir. Kapanış dipte oluştuysa after-hours'ta kapanış fiyatına limit dolmayabilir.
  * Aynı gün en fazla 6 ETF → 15.000 $ sermaye. Mart 2020'de 8 sinyal günü var.
  * Kaldıraçlı sürümler (KORU h = 1 t 1,95, en kötü −3.188 bp; YINN h = 1 t 1,25) önerilmez; Midas'ta bulunurlukları da doğrulanmadı. Bu ailede PTP ürünü yok.

## 3. S2 — EWY IBS (`d3_s2_ewy_ibs.py`)

* **Yeniden üretim, birebir:** n = 214, brüt 55,12, net 42,12 bp, t 2,93, IS 25,8 (t 1,29) / OOS 52,9 (t 2,33), yılların %70'i pozitif. Ham EWY verisinde h/l eksik ya da 0 değil; kapanış = dip olan gün 28.
* **Çürütmeye en yakın bulgular:**
  * Seçim yanlılığı: 20.196 satırlık taramadan seçildi. Bonferroni için p < 2,5e−6 gerekir.
  * IS t 1,29 (anlamsız).
  * Alt örnekler: 2026 hariç (21 işlem, ortalama +232 bp) net 21 bp, t 1,70; 2020 + 2026 hariç 12 bp, t 0,95; en iyi 10 işlem hariç t 1,15.
  * Aynı kural kardeş ETF'lerde negatif: EWT −7,7, EWJ −4,3, EWA −4,8, INDA −6,8, VGK −7,9 bp.
  * Gecikmeli girişte kenar yok: ertesi gün kapanışta giriş (C1) brüt 0,75 bp; ertesi gün açılışta giriş (O1) net 4,9 bp.
  * Pozisyon büyüklüğü ve kayma: 1.000 $'da t 1,68; kapanış öncesi giriş vekili f = 0,10 → t 1,69.
  * S1 ile aynı güne düşmeyen işlemler net 19 bp (t 1,42).
* **Lehte bulgular:**
  * Eşikte plato: IBS 0,05-0,20 aralığında t 2,4-3,7.
  * Yıl-tabakalı permütasyon p = 0,0014 (yalnız seçim sonrası tek test için geçerli).
  * EWY'nin 1 günlük otokorelasyonu IS ve OOS'ta negatif (−0,16 / −0,12); S1 ile aynı eşzamansızlık mekanizmasına işaret ediyor.
* **Karar: zayıf.** Keşifsel kalmalı; strateji olarak önerilmemeli.

## 4. Lead-lag (`d4_leadlag.py`)

* **Yeniden hesap:** kendi gecikmesi kontrollü OLS, Newey-West. Seçilen 20 çiftte taramanın lag_t_h1/h3 değerlerinden sapma ±0,15 içinde.
* **Aile içi FDR:** 5.370 p değeri (lag h1 + h3). BH (q = 0,10) geçen 0; en küçük p 1,1e−4, Bonferroni eşiği 9,3e−6 → **"doğrulanmış gecikmeli öncü yok" iddiası doğru**.
* **IS ve OOS'ta |t| ≥ 2 ve aynı işaretli çiftler:**
  * h = 1: EEM←KWEB, MCHI←KWEB, EWA←IWM, DXJ←SPY/QQQ/DIA, CWEB←EEM, EDC/EDZ←KWEB.
  * h = 3: EWH←LQD, CQQQ←TLT, VNM←TIP/DFII10, UAE←T10YIE.
  * Bunların hepsi kendi gecikmesine koşullu kısmi katsayılar.
* **Eşik kuralına çevrildiğinde** (C0, h = 1, 2.500 $):

| Kural | Net bp | t | Not |
|---|---|---|---|
| KWEB z ≥ 1 → EEM | −18 | −2,16 | |
| KWEB z ≥ 1,5 → EEM | −38 | | |
| IWM z ≥ 1 → EWA | −30 | −3,35 | |
| VIX düşüşü (z ≤ −1) → EWA | −20 | −2,10 | |
| TIP z ≥ 1,5 → EWY | 10 | | OOS −8 |
| DFII10 düşüşü z ≥ 1 → EWY | 8 | 0,59 | |
| QQQ z ≤ −1 → DXJ | 3 | | |
| EEM z ≤ −1 → FXI | 1 | | |

  Hiçbiri maliyeti tutarlı biçimde karşılamıyor. Kısmi katsayı ile kural arasındaki işaret farkı, iki yüksek korelasyonlu seriden doğan "kendi dönüşü" etkisinden geliyor.
* **Zamanlama notu:** DFII10/TIP (Hazine reel faiz) serisi gün sonundan sonra yayımlanır. C0 için hafif ileriye bakma riski var; O1/C1 temiz.
* **Bayat fiyat riski:** hedeflerin çoğu likit, bu nedenle düşük. CWEB/VNM gibi ince ürünlerde gecikmeli ilişkiler bayat kapanıştan kaynaklanabilir.
* **TradingView kodları:** ajanın sonuc.json'unda geçen 192 kodun tamamı tv_etf.csv ya da tv_dogrulama.csv'de "dogrulandi". Doğrulanmamış kodlar tv_dogrulanacak listesinde. Uygun.

## 5. İzleme listesine itirazlar

* **EWJ (kabul → yedek önerisi):**
  * Tek başına S1 sonucu zayıf: t 1,21, OOS +5 bp, yılların %50'si pozitif. Ertesi gün kapanışta girişte −35 bp.
  * Doğrulanmış gecikmeli öncü yok. Kabul gerekçesi yalnız likidite ve gerçek zamanlı izlenebilirlik.
* **FXI (kabul, şerhli):**
  * S1 tek başına t 1,17.
  * Ertesi gün açılışta girişte net −33 bp (t −2,38). Ajanın sepet için önerdiği "kapanış kaçırılırsa ertesi açılışta al" yedeği FXI'de zararlı.
* **EWY (kabul, şerhli):**
  * Her iki stratejinin sonucu da 2026'daki olağandışı oynaklık rejimine (günlük 403 bp, fiyat 97 → 202 → 137) bağlı.
  * Pozisyon büyüklüğü bu rejime göre ayarlanmalı.
* **EWT (kabul, şerhli):** S1'de ertesi gün kapanışta girişte OOS −22 bp; tek başına sınırda (t 2,00).
* **EFA ve VGK (yedek → red önerisi):**
  * Günlük oynaklık düşük (104-105 bp), maliyet/oynaklık 0,125-0,13.
  * Strateji ya da gecikmeli öncü yok; yalnız eşzamanlı sürücüleri var.
* **EWA (yedek):** S1 OOS −8 bp. Lead-lag adayları (IWM, VIX) kural olarak negatif. "Yedek" cömert bir karar.
* **INDA (yedek):** S1 OOS −8 bp; ertesi gün kapanışta girişte −39 bp. Yalnız Hindistan'a maruziyet için yedek kalabilir.
* **KORU (yedek, şerhli):**
  * 17.03.2020 veri tutarsızlığı.
  * Son 1 yılda en kötü gün −%42; makas fiyat adımına dayalı (14,5 bp).
  * Midas'ta bulunurluğu doğrulanmadı. Yalnız dayanak sinyaliyle, en fazla 1 gün tutulmalı.

## 6. Kaçırılan fırsat / risk

1. **Risk: t ve FDR yorumu.** Ailenin tek adayı (S1), NW düzeltmesi ve birkaç kriz günü olmadan eşiği geçmiyor. Raporda "orta güven" yerine "düşük-orta güven, izleme sinyali" denmeli.
2. **Risk: C0 kapanış kaynaklı iyimserlik.** Kenar, kapanışı gün dibinde olan işlemlerde toplanıyor ve Midas'ta MOC yok. Günlük aralığın %3-5'i kadar kayma bile t'yi 1,6-1,75'e indiriyor.
3. **Fırsat (sınırlı): SH ile korunan S1** (`d5_kacirilan.py`; açığa satış olmadan göreli kenarı yakalamak için). Sinyal günü seçilen Asya ETF'leri alınır, toplam tutar kadar tek SH emri verilir; t → t+1 kapanış.
   * En kötü gün −1.202 bp'den −356 bp'ye iniyor; standart sapma 294 bp'den 138 bp'ye düşüyor.
   * Ancak 2.500 $ bacaklarda net 18,7 bp (t 1,42). 10.000 $ bacaklarda net 32 bp (t 2,46), ama 2020 + 2026 hariç 13 bp (t 1,05).
   * Büyük sermaye için risk azaltma seçeneği; strateji değil.
4. **Fırsat (aile dışı teyit):** aynı S1 kuralı KWEB'de (sektör/tematik ailesi; 594 mn $/gün, 16 bp) n = 73, net 72 bp, t 2,30, IS 33 / OOS 102 bp. Mekanizmayı destekliyor. Ancak sonuç görüldükten sonra eklenirse seçim yanlılığı olur, ve FXI/CQQQ ile yüksek korelasyonlu.
5. **Bilgi:** son S1 sinyali 05.11.2026 (3 ETF, sepet net +252 bp). Veri 06.11.2026'da bitiyor.

## 7. Yeniden üretim komutları
```
python3 -I kod/denetim_uluslararasi/d1_s1_yeniden.py
python3 -I kod/denetim_uluslararasi/d2_s1_saglamlik.py      # ~50 sn (permütasyonlar)
python3 -I kod/denetim_uluslararasi/d3_s2_ewy_ibs.py
python3 -I kod/denetim_uluslararasi/d4_leadlag.py
python3 -I kod/denetim_uluslararasi/d5_kacirilan.py
python3 -I kod/denetim_uluslararasi/d6_kapanis_oncesi.py
python3 -I kod/denetim_uluslararasi/d7_hold.py
```
