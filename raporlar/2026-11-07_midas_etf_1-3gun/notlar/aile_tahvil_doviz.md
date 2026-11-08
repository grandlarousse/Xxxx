# Aile: tahvil_doviz (Hazine, kredi, TÜFE'ye endeksli, belediye tahvili, kaldıraçlı/ters Hazine ve döviz ETF'leri, 40 ETF)

Hazırlanma tarihi 07.11.2026. Veri aralığı 2016-11-07..2026-11-06. IS dönemi 2016-11..2021, OOS dönemi 2022..2026-11.
Kod `kod/ajan_tahvil_doviz/` altında, tablolar `sonuclar/aile_tahvil_doviz/` altında. Makine okunur sonuç `sonuclar/aile_tahvil_doviz/sonuc.json` dosyasında.
Bu çalışma geçmiş veri testidir (backtest). Geçmiş sonuç gelecekteki getiriyi garanti etmez. Yatırım tavsiyesi değildir.

## 0. Kısa sonuç

* **Eşiği geçen tek strateji S1: "10 yıllık Hazine ihalesi öncesi zayıflık".** Kural: 10 yıllık ihaleden 3 işlem günü önce (A-3) TMV alınır. TMV, TLT'nin −3 katı getiri veren ters ETF'idir. Pozisyon ihaleden bir önceki işlem günü (A-1) kapanışta satılır. Sinyal tamamen takvime dayanır, fiyat göstergesi gerekmez.
  * TMV, C0 modu: n=119 işlem, brüt 124 bp, net 104 bp (2.500 $ pozisyon, 20 bp maliyet), t=3,17. IS 108 bp (t=2,44), OOS 100 bp (t=2,03). Yılların %91'i pozitif. maxDD −%13. En kötü işlem −764 bp. PF 2,19.
  * Dayanakta etki şöyle: TLT bu 2 günlük pencerede ortalama **−41 bp** (t=−3,7) getiri veriyor. Pencere ±5 ve ±10 işlem günü kaydırıldığında (plasebo) etki kayboluyor. Süreye duyarlı her tahvil ETF'inde işaret aynı ve büyüklük süreyle ölçekleniyor.
  * Hipotez önceden kayıtlıydı (hipotezler.csv TD02, "Ek test: TLT C_A-3→C_A-1 < 0"). Literatürde de karşılığı var: Lou, Yan & Zhang (2013), ihale öncesi fiyat baskısı.
  * **Güven: orta.** Gerekçeler: (i) Kaldıraçlı ters ETF gerekiyor ve TMV/TBT'nin Midas'ta bulunurluğu doğrulanamadı. (ii) A-2 açılışında girilirse OOS etkisi zayıf (23 bp). Giriş A-3 seansında yapılmalı; o günün açılışında ya da kapanışında girmek test edildi ve ikisi de çalışıyor. (iii) 2026'da 10 işlemin ortalaması +20 bp ile zayıf kaldı.
* **Diğer her şey maliyet sonrası eşiğin altında kaldı.** Bu listeye ay sonu, FOMC, CPI/NFP, IBS/RSI2 dönüşü, faiz z-skoru, bakır/altın oranı, HYG←SPY ve bütün döviz kuralları dahil. Tahvil ETF'lerinin 1 günlük hareketi 25-60 bp. Bu hareket 13-16 bp gidiş-dönüş maliyeti zor karşılıyor. Döviz ETF'leri hem likiditesiz hem pahalı (20-47 bp).
  * Ay sonu etkisi ve FOMC D-1→D etkisi **brüt olarak gerçek** ve aile genelinde tutarlı (ay sonu brüt t 2,5-3,9; FOMC D-1 brüt t 2,3-3,2). Ancak büyüklükleri 8-27 bp ile küçük. OOS'ta zayıflamışlar ve net t<2.
* **Döviz ETF'lerinde "ABD hisseleri dün yükseldiyse döviz ETF'i bugün yükselir" etkisi gerçek ama işlenemez.** Etki likit UUP'ta da, ertesi günün gün içi parçasında da var. Yani yalnızca bayat kapanış artefaktı değil. Büyüklüğü 1 sd başına 5-9 bp, maliyet ise 20-47 bp. İşlem kuralına çevrildiğinde net −14..−44 bp.
* **Doğrulanmış (ekonomik) gecikmeli fiyat öncüsü yok.** Tek gecikmeli öngörücü takvimdir (S1). CBOT:UB1!, CBOT:ZB1!, CBOT:ZN1! ve TVC:US30Y gerçek zamanlı izleme araçlarıdır, öncü değildir.
* **ÖNEMLİ VERİ BULGUSU.** Nasdaq API, NYSE Arca ve Cboe listeli ETF'lerin dağıtım geçmişini vermiyor. Ailenin 33/40 ETF'inde toplam getiri eksikti ve ayın ilk işlem günü (ex-date) getirileri −16..−42 bp aşağı yanlı çıkıyordu. Örnek: genel_tum.csv'de HYG CA_ay_sonu satırı brüt −34 bp, t_edge −7 ile sahte sonuç veriyordu. Bu aile Yahoo dağıtım olaylarıyla yeniden hesaplandı. **Başka ailelerdeki NYSE Arca listeli ETF'ler (SPY dahil) için de aynı eksiklik olabilir.**

## 1. Veri ve yöntem

* **Zamanlama:** `kod/lib.py` sözleşmesi uygulandı. Sinyal t kapanışına kadarki bilgiyle hesaplanır. Olay takvimleri (Hazine ihalesi, FOMC, CPI, NFP, ay sonu) önceden bilinir ve kullanılabilir.
  * Hazine getirileri (`lib.fred('DGS10')` vb.) Treasury'nin ~15:30 ET kotasyonlarıdır, yani t kapanışında bilinir. Anlık takip için TVC:US10Y kullanılabilir.
  * VIX kapanışı 16:15 ET'dir. Bu yüzden VIX kullanan kurallarda C0 modu hafif iyimserdir.
* **Maliyet:** `lib.cost_bp` ile aynı formül kullanıldı: 2 × 1,5 USD komisyon + likidite kademesine göre makas. Duyarlılık 1.000 / 2.500 / 10.000 USD pozisyon için ayrı hesaplandı.
* **Dağıtım düzeltmesi:** `kod/ajan_tahvil_doviz/00_temettu_indir.py` Yahoo Finance chart API'sinden dağıtım olaylarını indirir. Ham JSON `sonuclar/aile_tahvil_doviz/temettu_yahoo_ham/`, tablo `temettu_yahoo.csv` dosyasındadır. `td.load()` bu verilerle toplam getiriyi yeniden kurar. `lib.py` değiştirilmedi.
  * Doğrulama: Nasdaq'ta dağıtımı olan 5 ETF'te (TLT, IEF, SHY, BND, EMB) Yahoo ile 119/120 olay eşleşti (fark ≤ 0,0005 $). Tek eksik olay 2026-11-02 dağıtımı; Yahoo'da henüz yok.
  * Aylık ödeyen ETF'ler için Kasım 2026 dağıtımı, bir önceki ayın tutarıyla tahmini olarak eklendi.
  * Düzeltme sonrası ayın ilk günü getirileri normale döndü. Örnek: HYG −34 bp'den +6 bp'ye, AGG −20 bp'den +2,5 bp'ye.
* **Genel kütüphane** (`kod/strategies.py`, aynı parametreler) aile için düzeltilmiş veriyle yeniden çalıştırıldı (`02a_genel_duzeltilmis.py`, tek süreç).
* **Parametre taraması yapılmadı.** Eşikler literatürden ya da hipotez dosyasından alındı. Komşu pencereler ve plasebo yalnız sağlamlık için raporlandı.

## 2. İşlenebilirlik ve kopya grupları (`islenebilirlik.csv`, `kopya_gruplari.csv`)

| ETF | Medyan $ hacim (mn) | Maliyet bp (2.500$) | 1g oynaklık bp | Maliyet/oynaklık | Not |
|---|---|---|---|---|---|
| TLT | 2.645 | 13,2 | 60 | 0,22 | Uzun Hazine temsilcisi |
| TMF (3x) | 159 | 16 | 177 | 0,09 | TLT long aracı |
| TMV (−3x) | 35,8 | 20 | 178 | 0,11 | **S1 aracı** |
| TBT (−2x) | 12,3 | 20 | 124 | 0,16 | S1 alternatifi |
| EDV / ZROZ | 73 / 37 | 16 / 20 | 93 / 103 | 0,17 / 0,19 | TLT kopyası (corr 0,98) |
| IEF | 759 | 14 | 31 | 0,45 | Orta vade |
| LQD / HYG | 3.309 / 3.062 | 13 / 13,3 | 37 / 27 | 0,35 / 0,49 | Kredi |
| AGG, BND, VCIT, TIP, MUB, GOVT, IEI | 105-866 | 14-16,5 | 20-28 | 0,5-0,8 | Hareket maliyete yakın |
| SHY, STIP, BIL, SGOV | 94-1.878 | 13-16 | 6-16 | 1,0-2,1 | Hareket < maliyet |
| UUP | 44,6 | 20 | 42 | 0,48 | En likit döviz ETF'i |
| FXE / FXY | 9,8 / 9,6 | 27 | 34 / 51 | 0,79 / 0,53 | |
| FXF, FXB, FXC, FXA, UDN, YCS, YCL, EUO, ULE, CEW | 0,06-4,9 | 27-47 | 29-104 | 0,45-1,6 | Likiditesiz |

**Kopya grupları** (son 3 yıl getiri korelasyonu):

| Grup | Üyeler | Korelasyon |
|---|---|---|
| Uzun Hazine | TLT / TLH / EDV / ZROZ | 0,95-0,99 |
| Uzun Hazine kaldıraçlı | TMF / UBT | 0,98 |
| Uzun Hazine ters | TMV / TBT | 0,99 |
| Orta vade | IEF / IEI / GOVT | 0,88-0,97 |
| Toplam tahvil | AGG / BND | 0,97 |
| Yatırım yapılabilir kredi | LQD / VCIT | 0,96 |
| Yüksek getiri | HYG / JNK / USHY | 0,98 |
| TÜFE'ye endeksli | TIP / SCHP | 0,97 |
| Hazine bonosu | BIL / SGOV | 0,88 |
| Euro | FXE / ULE (2x) / EUO (−2x) | \|0,95-0,98\| |
| Yen | FXY / YCL (2x) / YCS (−2x) | \|0,96-0,98\| |
| Dolar | UUP / UDN | −0,80 |

UUP ile FXE arasındaki korelasyon −0,87. Bu yüzden aynı kuralın UUP'ta pozitif, FXE'de negatif çıkması aynı bilgidir.

**Tutarlılık temsilcileri:**
* Tahvil (11 ETF): TLT, IEF, SHY, AGG, LQD, HYG, BKLN, TIP, STIP, EMB, MUB. Hepsi büyük ölçüde aynı faiz faktörüne bağlıdır; bunlar bağımsız kanıt değil, farklı vade ve kredi kesitleridir.
* Döviz (8 ETF): UUP, FXE, FXY, FXF, FXB, FXA, FXC, CEW.

**Bayat fiyat göstergeleri** (son 3 yıl):
* Sıfır getirili gün oranı her ETF'te < %5. Bunun tek istisnası BIL/SGOV'dur (%15-18; 1 sentlik fiyat adımı nedeniyle, nakit benzeri ürünler).
* Çok düşük hacimli gün oranı ULE'de %76, CEW'de %90.
* SPY(t−1) ile ETF(t) korelasyonu bütün döviz ETF'lerinde ~|0,1|. Likit UUP −0,11 ile likiditesiz FXF +0,12 benzer düzeyde.

**PTP/K-1 notları:**
* UUP ve UDN Invesco DB emtia havuzu fonlarıdır. YCS, YCL, EUO ve ULE ProShares Trust II'ye bağlıdır. Bu ürünler K-1 verir ve PTP sayılır: 1446(f) kapsamında %10 brüt satış stopajı riski var. Midas uygulamasında "PTP" ibaresi kontrol edilmeli.
* CurrencyShares döviz trust'ları (FXE, FXY vb.) grantor trust'tır, PTP değildir.
* TMV, TMF (Direxion) ve TBT (ProShares Trust) 1940 Yasası fonlarıdır. PTP olmadıkları ihraççı belgesiyle teyit edilmeli.

## 3. Genel kütüphane: aile içi (`genel_aile_tutarlilik_*.csv`, `genel_aile_havuz.csv`, `genel_aile_fdr.csv`)

* 11.880 satırlık (40 ETF × 297) iki yönlü BH-FDR testinde 8.362 satır geçti. Bunların neredeyse tamamı **net negatif** çıktı: maliyet, düşük oynaklıklı ETF'lerde kesin kayıp yaratıyor. Net pozitif geçen 9 satır var. Bunlar ya TMF/TMV/TBT'de tekil sonuçlar ya da küçük n'li HYG/JNK/EMB tatil öncesi satırları; aile tutarlılığı yok.
* Hiçbir kural temsilcilerin %60'ında net pozitif değil. Havuzlanmış temsilci sepetlerinin hepsi net ≤ +2 bp.
* **Tek tutarlı brüt etki ay sonu** (CA_ay_sonu_3). 11/11 tahvil temsilcisinde brüt > 0. Sepet brüt getirisi 9-13 bp, t 2,5-3,5. Ancak 14 bp maliyetin altında kalıyor.
* Döviz tarafında brüt sepetler 2-16 bp, net −20..−34 bp.

## 4. Aileye özel hipotez testleri (`03_hipotezler.py` → `hipotez_testleri.csv`, 693 test; birincil kurallar `hipotez_ozet.csv`)

Tablodaki tüm satırlar C0 modundadır. Net değerler 2.500 $ pozisyon içindir.

| Hipotez | Kural | ETF | h | n | Brüt bp | Net bp | t | IS / OOS net | Yıl+ |
|---|---|---|---|---|---|---|---|---|---|
| TD01 ay sonu | Sondan 4. gün → ay son günü | TLT | 3 | 117 | 27 | 14 | 1,20 | 26 / 2 | 0,90 |
| | | TMF | 3 | 117 | 68 | 52 | 1,51 | 90 / 15 | 0,90 |
| | | IEF | 3 | 117 | 21 | 7 | 1,27 | 7 / 8 | 0,60 |
| TD02 ihale sonrası | A30 → +2 gün | TLT | 2 | 117 | −5 | −18 | −1,53 | 8 / −44 | 0,50 |
| **TD02 ihale öncesi** | **A10-3 → A10-1** | **TMV** | 2 | 117 | **122** | **102** | **3,09** | 104 / 100 | 1,00 |
| | | **TBT** | 2 | 117 | 81 | 61 | 2,80 | 60 / 62 | 1,00 |
| | | TLT (long) | 2 | 117 | −40 | −53 | −4,86 | −55 / −51 | 0,00 |
| TD03 FOMC | D-2 → D+1 | TLT | 3 | 77 | 43 | 30 | 1,62 | 31 / 28 | 0,60 |
| | | TMF | 3 | 77 | 120 | 104 | 1,91 | 115 / 94 | 0,70 |
| TD04 CPI/NFP | Önceki gün → olay günü | TLT | 1 | 232 | −5 | −18 | −2,43 | −8 / −28 | 0,10 |
| TD10 TLT dönüşü | RSI2<10 → TLT | TLT | 3 | 171 | 7 | −7 | −0,61 | −8 / −5 | 0,50 |
| | TLT RSI2>90 → TMV | TMV | 3 | 171 | 77 | 57 | 1,69 | 48 / 70 | 0,60 |
| TD11 faiz z | ΔDGS10 z≥2 → TLT (dönüş) | TLT | 1 | 63 | −31 | −44 | −2,83 | −41 / −48 | 0,30 |
| TD05 FOMC döviz | D-1 → D | FXA / UDN / UUP | 1 | 77 | 16 / 8 / −7 | −31 / −39 / −27 | <0 | | |
| TD06 ay sonu USD | SPY ay içi ≥ +%3 → FXE | FXE | 2 | 37 | 3 | −24 | −2,72 | −19 / −30 | 0,20 |
| TD07 güvenli liman | SPY ≤ −%2 veya VIX +%20 → FXY | FXY | 2 | 99 | −12 | −39 | −3,51 | −48 / −27 | 0,10 |
| TD12 JPY←DGS2 | ΔDGS2 z≥1,5 → YCS | YCS | 1 | 161 | −6 | −53 | −5,70 | | 0,10 |
| TD09 bakır/altın | CPER/GLD 5g ≥ +%3 → TBT | TBT | 3 | 184 | 32 | 12 | 0,60 | −16 / 41 | 0,70 |
| TD13 HY←SPY | SPY z≤−1,5 → HYG | HYG | 1 | 175 | 5 | −9 | −1,66 | −3 / −14 | 0,40 |
| TD08 döviz gün saati | UUP/FXE/FXY/FXF/FXB gece ve gün içi | | her gün | 2.512 | \|≤2,3\| | | | | |
| TD14 döviz 5 günlük | Momentum / dönüş | 7 döviz ETF'i | 3 | | | Tümü net < 0 | | | |

Notlar:
* TD02 tablosunda n=117 çünkü 03_hipotezler.py'de 60 günlük ısınma uygulanıyor. S1 betiğinde ısınma yok ve n=119.
* TD08 için maliyet 20-47 bp. Ortalama hareket ekonomik değil.
* TD07'de işaret beklenenin tersi çıktı: şoktan sonra yen ve frank ertesi gün geri veriyor (FXF O1 brüt −16 bp, t=−5,2). Ancak bu yön sonradan bulundu ve ucuz bir işlem aracı yok (YCS maliyeti 47 bp). **Kabul edilmedi.**

## 5. Aday S1 — ayrıntı (`strateji_S1_ihale_oncesi.py`; çalıştırınca bu sayıları basar)

**Kural.**
* A = 10 yıllık Hazine (10-Year Note) ihale günü. Kaynak: TreasuryDirect "Upcoming Auctions" ya da Hazine geçici takvimi. TradingView Ekonomik Takvim'de "10-Year Note Auction" olarak görünür.
* A-3 günü AMEX:TMV (ya da AMEX:TBT) alınır. A-1 günü kapanıştan 5-10 dk önce satılır. İhale günü tutulmaz.
* A-3 genellikle ihaleden önceki Perşembe ya da Cuma'dır. Tarihsel dağılım: 77 Cuma, 30 Perşembe, 12 Çarşamba.

**Giriş modları** (TMV, 2.500 $):

| Mod | Brüt bp | Net bp | t | IS net (t) | OOS net (t) | Yıl+ |
|---|---|---|---|---|---|---|
| C0 (A-3 kapanışında al) | 124 | 104 | 3,17 | 108 (2,44) | 100 (2,03) | 0,91 |
| A-3 açılışında al (O1, sinyal A-4) | 118 | 98 | 2,82 | 93 | 103 | 0,82 |
| O1 (A-2 açılışında al) | 81 | 61 | 1,98 | 97 (2,20) | 23 (0,55) | 0,82 |
| C1 (A-2 kapanışında al) | 65 | 45 | 1,14 | 77 | 12 | 0,64 |

* Etkinin önemli bir kısmı A-3 kapanışından A-2 açılışına uzanan gece boşluğunda oluşuyor; bu çoğunlukla hafta sonu boşluğudur. Bu yüzden **giriş A-3 seansı içinde yapılmalı**.
* O1 ve C1 modlarında brüt kenar yine pozitif (81 ve 65 bp), dolayısıyla eşik koşulu sağlanıyor.

**Maliyet duyarlılığı** (TMV net, işlem başına):

| Pozisyon | Net bp |
|---|---|
| 1.000 $ | 86 |
| 2.500 $ | 104 |
| 10.000 $ | 113 |

TBT (C0) için: n=119, net 62 bp, t=2,87, IS 63 / OOS 62 bp, yıl+ 0,91, en kötü işlem −516 bp.

**Aile içi** (aynı pencere, brüt, C0):

| ETF | Brüt bp | t |
|---|---|---|
| TLT | −41 | −3,7 |
| EDV | −54 | −3,6 |
| ZROZ | −60 | −3,7 |
| TLH | −31 | −3,7 |
| IEF | −19 | −4,1 |
| IEI | −10 | −4,1 |
| GOVT | −15 | −4,2 |
| AGG | −13 | −3,4 |
| LQD | −22 | −3,2 |
| TIP | −13 | −2,4 |
| EMB | −21 | −2,6 |
| SHY | −3 | −3,5 |
| MUB | −3 | −0,8 |
| HYG | −3 | −0,6 |

Etki süreyle ölçekleniyor. Belediye tahvili (MUB) ve yüksek getirili kredi (HYG) etkilenmiyor; bu, Hazine arzı yorumuyla tutarlı. Ancak bu ETF'ler aynı faiz faktörüne bağlı olduğu için bağımsız kanıt sayılmaz.

**Komşu pencereler** (TLT brüt / TMV net):

| Pencere | TLT brüt bp | t | TMV net bp |
|---|---|---|---|
| A-4 → A-1 | −39 | −3,1 | 101 |
| A-3 → A-2 | −25 | −2,9 | 54 |
| A-2 → A-1 | −16 | −1,9 | 32 |
| A-3 → A (ihale günü dahil) | −43 | −3,0 | 117 |
| A-1 → A (yalnız ihale günü) | −6 | −0,8 | 2 |
| A → A+2 (ihale sonrası) | −9 | −0,7 | 12 |
| 30Y ihalesi A30-3 → A30-1 | −16 | −1,2 | 39 |

* Etki ihale gününden önce oluşuyor.
* İhale sonrasında toparlanma görülmüyor (TD02 ihale sonrası hipotezi reddedildi).

**Plasebo** (pencere kaydırılarak):

| Kaydırma | TLT brüt bp | t |
|---|---|---|
| −10 işlem günü | +17 | 1,2 |
| −5 işlem günü | −3 | −0,3 |
| +5 işlem günü | −10 | −1,0 |
| +10 işlem günü | +12 | 1,2 |

**Kontroller:**
* Pencerelerde hiç CPI ve FOMC yok.
* NFP içeren 26 pencerede TLT −66 bp. NFP içermeyen 93 pencerede TLT −34 bp (t=−2,6), TMV net +84 bp (t=2,18).
* Haftanın günü eşlenik koşulsuz 2 günlük TLT ortalaması −2 bp. Fark −38 bp.
* 2020 hariç TMV net 88 bp (t=2,57). 2022 hariç 101 bp (t=2,97). 2016'daki tek işlem (+700 bp) hariç 99 bp (t=3,02).
* En iyi 5 işlem hariç 63 bp (t=2,23). Medyan işlem +64 bp, kazanma oranı %59.

**Yıllara göre** TMV net (bp): 2017 −8, 2018 +28, 2019 +102, 2020 +252, 2021 +117, 2022 +135, 2023 +67, 2024 +85, 2025 +179, 2026 +20 (10 işlem). 2016'da tek işlem var.

**En kötü işlemler** (TMV): 2019-08-02 −764 bp, 2023-10-06 −679 bp, 2022-05-06 −563 bp.

**Sıradaki sinyaller:**
* 10 Kas 2026 (Salı) ihalesinin A-3 günü 5 Kas Perşembe'ydi. Bu sinyal açık; pozisyon 9 Kas Pazartesi kapanışta kapanır. 10 Kas'ta CPI de var, ancak bu ihale günüdür ve pencerenin dışındadır.
* 8 Ara 2026 (Salı, yeniden ihraç) için giriş 3 Ara Perşembe TR ~23:50, çıkış 7 Ara Pazartesi. 4 Ara'daki NFP pencerenin içinde kalıyor.

**Midas uygulaması:**
* MOC/LOC emri yok. Normal seansta, kapanıştan 5-10 dk önce piyasa ya da agresif limit emri verilmeli. Saatler: kış TR ~23:50, yaz ~22:50.
* Açığa satış olmadığı için kısa yön yalnız ters ETF ile alınabiliyor.
* TMV/TBT'nin Midas'ta bulunurluğu ve "parçalı" etiketi uygulamada kontrol edilmeli.
* −3x ETF'te stop-limit dolmayabilir, çünkü %2'den büyük boşluklarda stop limit dışında kalır.

## 6. Eşik altı kalanlar (özet; ayrıntı `sonuc.json` → `elenen`)

* **FOMC D-1 → D, TMF (`strateji_S2_fomc.py`).** n=79, net 53 bp, t=1,91 (IS t 1,42, OOS t 1,31).
  * 60 günlük ısınmayla t=2,19 çıkıyordu; yalnız 2 işlemin değişmesiyle eşiğin altına düşüyor, yani sonuç kırılgan. 2025 ve 2026 negatif.
  * Etki D-1 kapanışından D açılışına kadar oluşuyor: O1 modunda net 4 bp, C1'de −3 bp.
  * TLT'de brüt 24 bp (t=2,5); aile genelinde brüt pozitif (t 2,3-3,2). Gerçek ama küçük bir etki. **Reddedildi.**
* **TLT ay sonu.** Brüt etki aile genelinde pozitif, ama TLT'de OOS net 2 bp ve t=1,2. TMF'de net 52 bp, t=1,51, OOS 15 bp.
* **TLT RSI2>90 → TMV.** Net 57 bp, t=1,69. Eşik altı.
* **Döviz hipotezlerinin hepsi** (TD05, TD06, TD07, TD08, TD12, TD14) maliyet sonrası net negatif.

## 7. Lead-lag (`04_leadlag.py`)

**(a) leadlag_sweep aile alt kümesi** (1.431 satır):
* Gecikmeli öncülük (h1) testinde FDR'yi 35 satır geçiyor. Hepsi FXE, FXF, UUP ve FXY hedefli ve öncüleri SPY/QQQ/IWM/DIA/HYG/LQD/EEM/sektör ETF'leri.
* Büyüklük 1 sd başına 4-9 bp. Bu, maliyetin en fazla 0,47'si.
* h3'te FDR geçen satır yok.

**(b) Döviz ← SPY ayrıştırması** (kendi gecikmesi kontrollü, Newey-West t):

| ETF | Tam t (bp/sd) | Gece (C→O) t | Gün içi (O→C) t | IS / OOS t | Medyan $ hacim (mn) |
|---|---|---|---|---|---|
| UUP | −3,92 (−8,0) | −2,88 | −2,68 | −3,31 / −2,65 | 44,6 |
| FXE | 4,96 (5,9) | 2,54 | 4,35 | 5,08 / 2,32 | 9,8 |
| FXY | 4,02 (7,5) | 2,40 | 5,01 | 3,65 / 2,02 | 9,6 |
| FXF | 5,26 (7,9) | 2,87 | 5,08 | 6,53 / 2,46 | 4,9 |

* Etki likit UUP'ta da ve ertesi günün gün içi parçasında da var. Bu yüzden **yalnız bayat kapanış artefaktı değil**; döviz piyasası ABD hisse bilgisini yavaş fiyatlıyor.
* İşlem kuralına çevrildiğinde (SPY z≥1 → FXE/FXF/FXY/FXB, SPY z≤−1 → UUP, h=1) brüt +2..+8 bp, net −14..−44 bp.
* z≥2 eşiğinde bile net < 0. 10.000 $ pozisyonda en iyi sonuç +3 bp ve t<1. **Ekonomik değil.**

**(c) HYG/JNK/USHY ← SPY:**
* İşaret NEGATİF: SPY yükseldiği günün ertesinde HYG geri veriyor. t=−2,96 (IS −2,5 / OOS −1,5), 1 sd başına −11 bp; maliyet 13 bp.
* Açığa satış yok. SPY düşüşü sonrası HYG long kuralı da net negatif.

**(d) "Yetişme" testleri** (kendi gecikmesi kontrollü):
* BIL ve SGOV'daki t≈7-11 sonuçlar ekonomik değil: 1 sd başına 0,4-1 bp, maliyet 13-14 bp.
* Bu sonuçlar ayrıca eksik dağıtım verisinin testere dişi deseninden kaynaklanıyor. Düzeltilmiş veride kendi gecikmesi kontrol edilince işaret dönüyor ya da kayboluyor (BIL←VIX h3: kontrollü t eski veride +2,68, düzeltilmiş veride −2,40, 1 sd başına −0,8 bp).
* GOVT←IEF/SHY: kontrollü t 2,4-3,0, büyüklük 4-5 bp/sd; maliyet 16,5 bp.
* TBT←IEF (h3): kontrollü t=1,83, büyüklük 16 bp/sd; maliyet 20 bp.

**(e) İzleme ETF'leri** (TLT, TMF, TMV, TBT, EDV, UUP) × 19 aday öncü × h∈{1,3}, toplam 224 test:
* BH-FDR'yi 5 satır geçti. Hepsi UUP ← HYG/LQD/SPY/QQQ/TIP (h1); hiçbiri maliyetin üstünde değil.
* **TLT, TMF, TMV, TBT ve EDV için doğrulanmış gecikmeli öncü yok.**
* Sınırda kalan bir gözlem var: TLT ← IEF (h3), t=2,61, IS 2,0 / OOS 1,8, 27 bp/sd. FDR'yi geçmiyor; izlenebilir ama sinyal değil.

**Eşzamanlı sürücüler (öncü değil):** TLT için 30Y getiri (TVC:US30Y, corr −0,97), IEF (0,91), 10Y getiri (TVC:US10Y, −0,91), LQD (0,90), reel getiri (FRED:DFII10, −0,80).

**Gerçek zamanlı izleme (öncü değil):** CBOT:UB1!, CBOT:ZB1!, CBOT:ZN1!, TVC:US30Y, TVC:US10Y, TVC:DE10Y, TVC:JP10Y. CME Globex kış saatinde TR 02:00'den ertesi gün 01:00'e kadar açık.

## 8. İzleme listesi

| Karar | ETF'ler | Gerekçe |
|---|---|---|
| **Kabul** | TMV | S1 aracı |
| **Yedek** | TBT | S1 alternatifi (−2x, 12 mn $) |
| | TLT | S1'in dayanağı ve faiz izleme aracı. Long yönde eşiği geçen strateji yok. Risk kuralı: ihale öncesi pencerede long taşıma. |
| | TMF | TLT long sinyalleri için komisyon-verimli araç. Kabul edilmiş long sinyal yok. |
| **Red** | Diğer 36 ETF | Kopya, hareket < maliyet, likiditesizlik ya da PTP riski. Gerekçeler `sonuc.json → izleme` içinde. |

## 9. Test sayısı ve FDR

Toplam **12.827 test**:
* Strateji testleri 12.515: düzeltilmiş genel kütüphane 11.880, aile hipotezleri 693, S1/S2 sağlamlık testleri ve döviz kuralları.
* Lead-lag regresyonları 312.

FDR sonuçları:
1. **İki yönlü BH-FDR, q=0,10, tüm strateji testleri:** 8.709 test geçiyor (eşik p≤0,070), bunların 29'u net pozitif. S1-TMV (p=0,0020) ve S1-TBT (p=0,0049) geçiyor. Bu ölçüt, maliyet yüzünden kesin negatif çıkan satırlarla "şişiyor".
2. **Katı tek yönlü BH ("net > 0", 12.515 test):** geçen yok. S1 de geçmiyor.
3. **Odaklı, önceden kayıtlı birincil kurallar (58 test):** tek yönlü BH'de yalnız TD02 ihale öncesi TMV (p=0,0012) ve TBT (p=0,0030) geçiyor.
4. **Brüt etki BH (693 hipotez testi):** 43 satır geçiyor. Bunlar ay sonu (IEF/AGG/GOVT/SHY/TIP/LQD), FOMC D-1 (TLT/IEF/EDV/AGG) ve ihale öncesi (TLT/IEF/TBT/TMV) satırları. Yani etkiler istatistiksel olarak var; sorun büyüklük/maliyet oranı.

## 10. Sınırlamalar

* Dağıtım düzeltmesi Yahoo verisine dayanıyor. Nasdaq ile eşleşmesi doğrulandı (5 ETF, 119/120 olay). 2026-11-02 dağıtımı tahmini. Dağıtım vergisi (%20 ABD stopajı) modellenmedi. S1 penceresi TMV, TBT ve TLT ex-date'lerine denk gelmiyor.
* Kaldıraçlı/ters ETF'lerin günlük yeniden dengelemesi gerçek veride zaten içeriliyor. Ancak 2016-2026'nın faiz rejimi (2020 düşüş, 2022 yükseliş) tekrar etmeyebilir.
* İhale büyüklüğü, birincil bayi kapasitesi ve Hazine geri alım (buyback) programı (2024+) etkiyi değiştirebilir. 2026'daki zayıflık (10 işlemde +20 bp) izlenmeli.
* Maliyet modeli kaba: makas likidite kademesinden tahmin edildi. TMV'nin 8 bp makas varsayımı medyan 36 mn $ hacme göre konuldu; volatil günlerde makas açılabilir.
* Midas'ta TMV, TBT ve TMF bulunurluğu, parçalı alım ve PTP durumu doğrulanamadı. Döviz kaldıraçlı ürünleri (YCS, YCL, EUO, ULE) ile UUP/UDN için K-1/PTP riski var.
* Tahvil ETF'leri için gün içi (dakikalık) veri yok. C0 girişinin kapanıştan dakikalar önceki fiyatla yapılacağı varsayıldı; S1'de sinyal fiyattan bağımsız olduğu için bu iyimserlik sınırlı.

## 11. Tekrar üretim (sırayla, `python3 -I`, tek süreç)

```
python3 -I kod/ajan_tahvil_doviz/00_temettu_indir.py      # ham JSON önbellekte; ağ yoksa önbellekten okur
python3 -I kod/ajan_tahvil_doviz/01_islenebilirlik.py
python3 -I kod/ajan_tahvil_doviz/02a_genel_duzeltilmis.py # ~1 dk
python3 -I kod/ajan_tahvil_doviz/02_genel_aile.py
python3 -I kod/ajan_tahvil_doviz/03_hipotezler.py
python3 -I kod/ajan_tahvil_doviz/04_leadlag.py
python3 -I kod/ajan_tahvil_doviz/strateji_S1_ihale_oncesi.py   # ADAY S1: tüm sayıları basar
python3 -I kod/ajan_tahvil_doviz/strateji_S2_fomc.py           # reddedilen S2 (FOMC) ayrıntısı
python3 -I kod/ajan_tahvil_doviz/06_sonuc_json.py              # FDR muhasebesi + sonuc.json
```
