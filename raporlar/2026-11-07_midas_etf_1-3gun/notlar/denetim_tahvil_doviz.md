# Denetim: tahvil_doviz ailesi (bağımsız denetçi)

Hazırlanma tarihi 08.11.2026. Bu notta aile ajanının tek aday stratejisi S1, lead-lag iddiaları ve izleme listesi kararları denetleniyor.
* Kod: `kod/denetim_tahvil_doviz/` (d01–d07). Tablolar: `sonuclar/aile_tahvil_doviz/denetim/`.
* Ham indirmeler `sonuclar/aile_tahvil_doviz/denetim_ham/` altında: FRED DGS10/20/30/5, fiscaldata 10Y ihale geçmişi 1979-2026, Yahoo TLT 2002-2016 ve TBT 2008-2016.
* İşlem simülasyonu `lib.trades`, `lib.evaluate` ve `td.full_eval` kullanılmadan yazıldı. Fiyatlar `lib.load` ve `td.load` ile alındı.
* Bu bir geçmiş veri testidir ve yatırım tavsiyesi değildir.

## 0. Karar özeti

| Bulgu | Ajan | Denetim |
|---|---|---|
| S1: 10Y ihale A-3 kapanışı → A-1 kapanışı, TMV/TBT long | kabul, güven "orta" | **ZAYIF.** Sayılar birebir yeniden üretildi, ileriye bakma yok. Ancak **örneklem öncesinde (2002-2016) etki yok**. OOS kenarı hafta sonu boşluğuna bağlı. En iyi 10 işlem çıkarılınca t=1,30. |
| TLT/TMV/TBT/TMF için doğrulanmış fiyat öncüsü yok | — | **Doğrulandı** |
| UUP ← SPY/HYG/LQD gecikmesi gerçek ama işlenemez | — | **Doğrulandı** |
| NYSE Arca listeli ETF'lerde dağıtım verisi yok | veri uyarısı | **Doğrulandı ve proje geneline yayılıyor.** SPY, IWM, DIA, VOO, IVV, SCHD, JEPI, XLF, XLE, GLD, EEM, HYG, AGG, LQD, TMV, TBT ve TMF'de ham veride dağıtım olayı sayısı 0. |
| İzleme: TMV kabul | kabul | **Yedek olmalı** |

## 1. S1 — A) Kod ve zamanlama

**Yeniden üretim** (`d01_s1_yeniden.py`):
* Kendi simülasyonumla TMV C0'da 119/119 işlem tarih tarih eşleşti. Brüt getiri farkı en fazla 5e-12 bp.
* TMV C0: n=119, brüt 124,1 bp, net 104,1 bp, t=3,17, kazanma %58,8, PF 2,19.
* IS: net 108,2 bp (t=2,44). OOS: net 99,9 bp (t=2,03). Pozitif yıl oranı 0,91. maxDD −%13,0. En kötü işlem −764 bp.
* Maliyete göre net: 1.000 $ pozisyonda 86 bp, 2.500 $'da 104 bp, 10.000 $'da 113 bp.
* TBT C0: net 62,3 bp, t=2,87, IS 62,9 / OOS 61,6 bp (t=1,88).
* Kendi kodumdaki bir hatayı (ilk sinyalde `IDX[-1]`'e sarma) düzelttikten sonra O1 ve C1 de birebir eşleşti:

| Giriş modu | Net bp | t | OOS net bp (t) |
|---|---|---|---|
| O1 | 60,8 | 1,99 | 23,2 (0,55) |
| C1 | 45,0 | 1,14 | 11,5 (0,23) |
| A-3 açılışı | 98,1 | 2,82 | 103,3 |

**Zamanlama kontrolü:**
* Sinyal yalnızca takvime dayanıyor. Hazine geçici ihale takvimi aylar önceden, her ihale ise yaklaşık bir hafta önceden ilan ediliyor. Bu yüzden A-3 günü ihale tarihi biliniyor.
* İhale günlerinin hepsi NYSE işlem günü (2016 öncesindeki 10 satır veri aralığının dışında).
* İşlemler çakışmıyor (ayda bir işlem). Giriş ve çıkış fiyatları doğru günden alınıyor. Maliyet bir kez düşülüyor (20 bp = 12 + 8).
* TMV ve TBT dağıtım ex-date'lerinden hiçbiri pencerelerin içine düşmüyor. `lib.load` ile `td.load` arasındaki fark 0 bp.

**En büyük 5 kazanç** (hepsi gerçek olay; `veri_kalitesi.csv` ve `veri_duzeltmeleri.csv`'de satır yok, Hazine getirisi de aynı yönde hareket ediyor):

| Sinyal günü | TMV net bp | Olay | ΔDGS30 |
|---|---|---|---|
| 2025-04-04 | +1.510 | Nisan 2025 tarife/bono satışı | +30 bp |
| 2019-09-06 | +1.077 | | +17 bp |
| 2020-11-05 | +973 | Seçim ve 9 Kas Pfizer aşı haberi | +19 bp |
| 2022-12-07 | +857 | | +14 bp |
| 2022-04-07 | +778 | | +15 bp |

* Etki yalnızca ETF'de değil, Hazine getirilerinde de var: pencerede ortalama ΔDGS10 +2,80 bp (t=4,68). Bayat fiyat ya da ETF artefaktı değil.

## 2. S1 — B) İstatistiksel sağlamlık

**Permütasyon** (`d02`, `d06`; 20.000 tekrar, aynı n ve 2 günlük tutuş):

| Test | p | Not |
|---|---|---|
| Rastgele gün | 0,0010 | |
| Aynı ay ve aynı haftanın günü eşlenik | 0,00005 | |
| Eşlenik, yalnız IS | 0,0002 | |
| Eşlenik, yalnız OOS | **0,040** | Aynı ay ve aynı gündeki rastgele pencereler de OOS'ta TMV'ye ortalama +44 bp kazandırıyor (2022-23 faiz yükselişi, Pazartesi etkisi). Gerçek OOS fazlası ~76 bp, 120 değil. |

* Takvim ±5..20 gün kaydırıldığında (32 kaydırma) hiçbiri gözlenen −41 bp'ye yaklaşmıyor. En düşüğü −19,6 bp.

**Aykırı değer ve dönem duyarlılığı:**

| Kesit | n | Net bp | t |
|---|---|---|---|
| En iyi 5 işlem hariç | 114 | 63,1 | 2,23 |
| **En iyi 10 işlem hariç** | 109 | **34,6** | **1,30** |
| %5/%95 winsorize | 119 | 99,7 | 3,54 |
| Medyan işlem | — | 63,5 | — |
| 2020 hariç | 107 | 87,5 | 2,57 |
| 2022 hariç | 107 | 100,7 | 2,97 |
| 2020 ve 2022 hariç | 95 | 81,5 | 2,33 |
| 2023-2026 | 46 | 90,8 | 1,71 |
| 2024-2026 | 34 | 99,1 | 1,60 |
| 2026 | 10 | +20 | — |

**Kapanışa bağımlılık** (`d05`; TMV, OOS kenarının nereden geldiği):

| Parça | Brüt OOS bp | t |
|---|---|---|
| A-3 kapanışı → A-2 açılışı (çoğunlukla hafta sonu) | +76 | 3,21 |
| A-2 seansı + A-1 | +43 | 1,02 |
| A-3 seansı (açılış → kapanış) | ~0 | — |

* Yani OOS'taki kenar büyük ölçüde gece/hafta sonu taşımasından geliyor. Strateji **"kapanışa (gece taşımaya) bağımlı"** diye işaretlenmeli.
* A-3 açılışında da kapanışında da girmek çalışıyor. A-2'de girmek (O1, C1) çalışmıyor.

**Kesitlerde zayıflık** (`d02`):

| Kesit | n | TMV net bp | t | Not |
|---|---|---|---|---|
| A-3 = NFP günü | 74 | 61,7 | 1,41 | |
| A-3 = Cuma | 77 | 55,7 | 1,33 | |
| Yeni ihraç ayları (Şub/May/Ağu/Kas) | 39 | 58,1 | 0,97 | En büyük arz bu aylarda; arz hikâyesinin tersi |
| Yeniden ihraçlar | 80 | 126,6 | 3,22 | |
| 30Y ihale penceresi | — | — | — | ΔDGS30 +1,08 bp, t=1,58. Uzun ucu (TLT) en çok bu ihalenin etkilemesi beklenirdi. |

**ÖRNEKLEM ÖNCESİ TEST** (`d03`, `d07`). Bu, gerçek dış örneklemdir ve kural birebir aynıdır (A-3 kapanışı → A-1 kapanışı, C0).

| Seri | Dönem | n | Brüt bp | t | Beklenen işaret |
|---|---|---|---|---|---|
| TLT | 2002-08..2016-10 | 141 | **+7,6** | 0,79 | negatif |
| TBT | 2008-05..2016-10 | 99 | **−17,0** | −0,68 | pozitif |
| ΔDGS10 | 1990-2016 | 195 | +0,40 | 0,69 | pozitif |
| ΔDGS10 | 2008-2016 (bugünküyle aynı aylık takvim) | 102 | +0,20 | 0,25 | pozitif |
| ΔDGS10 | 2016-11..2026 (örneklem) | — | +2,9 | 5,0 | pozitif |

* TLT'de işaret yanlış. TBT'de işaret yanlış; net −37 bp, yılların yalnız %11'i pozitif.
* Örneklem içinde getiri etkisi örneklem öncesine göre 7-14 kat büyük.
* Komşu pencereler örneklem öncesinde: A-4→A-1 ve A-5→A-1 doğru işaretli ama anlamsız (TBT +33 / +53 bp, t 1,05 / 1,48). A-3→A-1 yanlış işaretli.
* 2008-2016'da klasik Lou-Yan-Zhang deseni görülüyordu: A-5→A-1 arasında DGS30 +2,25 bp (t=2,07), ihale sonrası toparlanma A→A+2 arasında DGS10 −2,2 bp (t=−2,76). 2016 sonrasında desen değişti: yükseliş A-3→A-1'e yoğunlaştı, toparlanma kayboldu.
* **Sonuç: S1'in tam penceresi kalıcı bir anomali değil, 2016-2026 rejimine özgü.** Bu rejim, yükselen arz/açık ve bayi bilanço kısıtları dönemidir.

**Çoklu test:**
* Ajan 12.827 test sayıyor. Katı tek yönlü BH'de (12.515 strateji testi) S1 geçmiyor. Bonferroni'de de geçmiyor.
* Yalnız önceden kayıtlı 58 testlik odaklı sette geçiyor (tek yönlü p≈0,001 < 0,10/58).
* Önceden kayıtlı hipotez 10Y **veya** 30Y ihalesini kapsıyordu. 30Y yarısı zayıf çıktı ve atıldı.
* Literatürdeki ihale sonrası toparlanma yarısı da tutmuyor.

**Midas uygulanabilirliği:**
* Açığa satış yok; kısa yön yalnız ters ETF ile alınabiliyor. TMV/TBT'nin Midas'ta bulunurluğu doğrulanmadı.
* MOC/LOC emri yok. Giriş kapanıştan dakikalar önce piyasa ya da agresif limit emriyle yapılabilir. Sinyal takvime dayandığı için C0 iyimserliği küçük.
* TMV ve TBT 1940 Yasası fonlarıdır, PTP değildir (ihraççı belgesiyle teyit edilmeli).
* −3x ürünün en kötü 2 günlük işlemi −%7,6.
* 1.000 $ pozisyonda net 86 bp.

**S1 kararı: ZAYIF.**
* Örneklem içinde istatistiksel olarak gerçek: IS ve OOS'ta pozitif, permütasyon p≤0,001, Hazine getirilerinde de var. Kabul eşiği teknik olarak sağlanıyor.
* Ancak (i) dayanakta 14 yıllık örneklem öncesi testte tam kural çalışmıyor; (ii) OOS kenarı hafta sonu boşluğuna bağlı ve eşlenik permütasyonda OOS p=0,04; (iii) en iyi 10 işlem çıkarılınca t=1,30; (iv) 2023-2026'da t=1,71; (v) global FDR'yi geçmiyor.
* "Kabul" stratejisi olarak sunulmamalı. Kullanılacaksa küçük pozisyonla ve "rejime bağlı, deneme" etiketiyle kullanılmalı. TBT (−2x) TMV'ye tercih edilmeli: en kötü işlem −516 bp'ye karşı −764 bp, maxDD −%9'a karşı −%13.

## 3. Lead-lag (`d04_leadlag.py`)

Yöntem: kendi gecikmesi kontrollü OLS, Newey-West t, 30 testlik dar set.

* **TLT/TMV/TMF ← IEF (h3):** t=2,6 / −2,4 / 2,4. IS/OOS aynı işaretli ama her biri t<2 (1,7-1,9).
  * Ajanın 224 testlik setinde ve leadlag_sweep'te (47 öncü) FDR'yi geçmiyor.
  * Önceden belirlenmiş tek eşikli işlem kuralı (TLT-IEF kalıntı z ≤ −1,5 → TLT/TMF long; z ≥ +1,5 → TMV long; h=3) net t<1,1 ve IS/OOS'ta işaret dönüyor (TMF IS +136 / OOS −24 bp).
  * **Doğrulanmış gecikmeli öncü yok; ajan doğru.**
* **TBT ← IEF yetişme (h3):** leadlag_sweep'teki tek FDR bayrağı. Kendi gecikmesi kontrol edilince t=−1,82. **Reddi doğru.**
* **TBT ← ΔDGS30 (h1):** t=−2,53, ancak OOS t=−1,36. Geniş sette FDR'yi geçmiyor.
* **UUP ← SPY/HYG/LQD (h1):** t −3,8 / −4,4 / −3,9, büyüklük 8-9,6 bp/sd. Gece parçasında t=−2,86, gün içi parçasında t=−2,68.
  * Gerçek ve bayat fiyat artefaktı değil, ama 20 bp maliyetin altında. **Ajan doğru.**
* **Gerçek zamanlı izleme kodları** (CBOT:UB1!, ZB1!, ZN1!, TVC:US30Y/US10Y/DE10Y/JP10Y, CME_MINI:ES1!):
  * Hepsi tv_dogrulama'da "dogrulandi" durumunda.
  * CME Globex saatleri doğru: kış TR 02:00 → ertesi gün 01:00, yaz bir saat erken.
  * 13:00 ET = TR 21:00 (kış) doğru.
* FRED:DFII10 gecikmeli yayımlanır; eşzamanlı sürücü olarak doğru etiketlenmiş, gerçek zamanlı izleme aracı değil.

## 4. İzleme listesine itirazlar

* **TMV kabul → yedek.** S1 zayıf, Midas bulunurluğu doğrulanmadı ve ürün −3x.
* **TBT:** Yedek kalsın. S1 denenecekse tercih edilecek araç TBT olmalı (daha düşük kuyruk riski). Ancak likidite 12,3 mn $ ile tercih edilen alt sınırda.
* **TLT, TMF, UUP ve diğer red kararları:** İtiraz yok. UUP'nin PTP/K-1 (1446(f)) riski notu doğru. CurrencyShares ürünleri grantor trust'tır.

## 5. Kaçırılanlar

1. **Örneklem öncesi test yapılmamış.** Yapıldığında S1'in tam penceresi 2002-2016 TLT ve 2008-2016 TBT'de çalışmıyor (bölüm 2). Bu, S1'in en önemli zayıflığı.
2. **Dağıtım verisi eksikliği proje geneline yayılıyor.** NYSE Arca (PSE) listeli tüm ETF'lerde ham veride dağıtım yok: SPY, IWM, DIA, VOO, IVV, SCHD, JEPI, XLF, XLE, EEM, HYG, AGG, LQD, TMV, TBT, TMF.
   * `lib._fix_dividends` yalnız Haziran/Aralık'taki %4'ten büyük boşlukları yakalıyor. Bu yüzden `lib.load`'un "toplam getiri" iddiası PSE ETF'leri için yanlış.
   * SPY'nin ex-date'i çeyrek sonu aylarının 3. Cuma'sıdır, yani çeyreklik opex gününün kendisi (Yahoo: 2023-03-17 … 2025-09-19, hepsi 3. Cuma; ~1,5-1,9 $ ≈ 30 bp). Bu nedenle diğer ailelerdeki opex'e ya da ex-date'e değen 1-3 günlük kurallar SPY'de ~−30 bp, aylık yüksek dağıtımlı ETF'lerde (JEPI vb.) ayda bir ~−50..−80 bp aşağı yanlı olabilir.
   * Ajan bunu uyardı. Bu denetim bulguyu doğruluyor ve nihai rapordan önce `lib` düzeyinde düzeltilmesini öneriyor.
3. **Rejim riski.** S1 kârının büyük kısmı faiz şoku pencerelerinde (2019-09, 2020-11, 2022, 2025-04) oluşmuş. 2026'da 10 işlemde ortalama +20 bp. Hazine geri alım programı (2024+) ve ihale yapısındaki değişiklikler etkiyi zaten değiştirmiş olabilir.

## 6. Tekrar üretim (`python3 -I`, tek süreç)

```
python3 -I kod/denetim_tahvil_doviz/d01_s1_yeniden.py
python3 -I kod/denetim_tahvil_doviz/d02_s1_saglamlik.py
python3 -I kod/denetim_tahvil_doviz/d03_s1_orneklem_oncesi.py
python3 -I kod/denetim_tahvil_doviz/d04_leadlag.py
python3 -I kod/denetim_tahvil_doviz/d05_kacirilan.py
python3 -I kod/denetim_tahvil_doviz/d06_perm_alt.py
python3 -I kod/denetim_tahvil_doviz/d07_pencere_orneklem_oncesi.py
```
