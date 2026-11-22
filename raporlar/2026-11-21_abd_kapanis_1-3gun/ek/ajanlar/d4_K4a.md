# K4a · backtest

araç: 29/40

Sınanan kural × varyant: 674 · IS adayı: 10 · OOS'tan geçen: 0

## Özet

Sınanan: 13 önceden yazılı kural (R8-01…R8-08, R1-03, R1-04, R1-11, R1-14, R7-10) ve yöntem denetçisinin eki: IBS (kapanışın gün içi aralıktaki yeri) <0,2 ve >0,8, RSI(2) <10 ve >90, üst üste ≥3/5/7 düşüş günü, 20 günlük σ'ya göre ≤−2σ ve ≤−3σ. Ek sinyaller 4 endeks ETF'inde, 5 sektör ETF'inde ve dönem başı 150 hisselik havuzda sınandı. Toplam 170 sinyal ve 674 varyant var: h=1,2,3 ve "çıkış t+1 açılış", Giriş K, korunmasız, hisse başı komisyon. İleriye bakma testi üç kesim tarihinde temiz çıktı.

IS'te (2010–2019) 10 aday çıktı. Tek yönlü kurallarda t_anormal ≥ 2 şartı da arandı. Adayların 6'sı 10'dan az işleme dayanıyor: VIX(t−1)≥40 + 5 gün bekleme (n=7), R8-08'in karşılaştırma kolu olan "ayı rallisinde uzun" (n=4–6), SMH'de seri≥7 (n=3), QQQ'da 6 gün düşüş sonrası gece (n=10).

**OOS'ta (2020–2023) hiçbir aday geçmedi (0/10).** Beşinin işareti döndü, sonuç ELENDİ. Beşi aynı yönde kaldı ama t<2, sonuç DÜŞÜK: DIA'da seri≥5 (h=1 ve 2), IWM'de seri≥5 (gece), SMH'de seri≥7 (OOS'ta 1 işlem). OOS'tan geçen olmadığı için Giriş G, korunmalı satırlar, 15:30 testi ve sağlamlık testleri yalnız tanım gereği yapılmadı. Kaldıraçlı ETF satırları (UPRO/SPXU, SSO/SDS, TQQQ/SQQQ, QLD/QID, SOXL/SOXS, TNA/TZA) her sinyal için sonuc_K4a.csv'de duruyor. Test sayısına katılmadılar.

Klasik "düşeni al" kuralları IS'te tutmadı: SPY'de RSI(2)<10, IBS<0,2, −2σ, R7-10 ve R8-07. 2010–2019'da net 1–18 bps, t ≤ 1,0. Bu kuralların 2020 sonrası (OOS ve son dönem) satırları pozitif. Örnek: SPY RSI(2)<10, h=1, OOS +40 bps t 1,9, son dönem +33 bps t 2,2. Ama bu bir seçimin ürünü değil, kurallar IS'te elendi.

En önemli çekince rejim kırılımında. VIX(t−1)>30 ve SPY 200 günlük ortalamanın altındayken bu kurallar 2005–2026 toplamında güçlü görünüyor:
- SPY RSI(2)<10: n=61, +141 bps, t 2,8
- IBS<0,2: n=102, +81 bps, t 3,0

Bu bulgu sonradan bakılmış bir rejim alt kümesi, ve VIX>30 rejiminde IS zayıf: RSI(2) için n=23, +36 bps, t 0,6. Doğrulanmış sinyal sayılamaz.

Felaket dönemleri: VIX(t−1)≥35'te uzun kuralı Eylül–Kasım 2008'de 46 işlemde −2.809 bps kaybetti (9 ardışık kayıp), Şubat–Mart 2020'de −1.927 bps. İçinde bulunduğumuz Ekim–Kasım 2026 bölümünde SPY RSI(2)<10 7 işlemde −728 bps (4 ardışık kayıp), seri≥3 ise −674 bps getirdi.

Bugüne benzeyen günler (SPY 7+ gün düşüş, 2005'ten beri 7 bağımsız seri, hepsi 200 günlük ortalamanın altında): sonraki 1/2/3/5 günde ortalama +%2,7/+%2,5/+%2,3/+%1,8, isabet %71–86. Ama n=7 ve ortalamayı 10 Ekim 2008'deki +%14,5 çekiyor. Betimsel bir tablo, sinyal değil.

## Tablo

| kural_id | ad | hedef | yon | h | giris | korunma | is_net_bps | oos_net_bps | oos_n | oos_t | oos_p | son_net_bps | son_t | girisA_oos_net_bps | basabas_bps | vix30 | sinif | gerekce |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R8-03:VIX(t-1)>=40:bekle5 | VIX(t-1)>=40, 5 gün bekleme: SPY uzun | SPY | uzun | 2 | K | yok | 235.5 | -92 | 9 | -0.44 | 0.602 | 864 |  | -25 | -40 | 7 bölüm, %43 pozitif | ELENDİ | IS'te 7 işlem; OOS'ta işaret döndü (son dönemde 1 işlem, t yok). |
| R8-03:VIX(t-1)>=40:bekle5 | VIX(t-1)>=40, 5 gün bekleme: QQQ uzun | QQQ | uzun | 2 | K | yok | 285.3 | -74.7 | 9 | -0.47 | 0.664 | 985 |  | -26 | -32 | 7 bölüm, %57 pozitif | ELENDİ | Az olay; OOS'ta işaret döndü. |
| R8-06:seri==6 | QQQ 6. düşüş kapanışında uzun, ertesi açılışta çık | QQQ | uzun | 0 (t+1 açılış) | K | yok | 86.1 | -193.6 | 2 |  | 0.241 | 104 |  |  | -93 | 4 bölüm, %75 pozitif | ELENDİ | IS'te 10 işlem; OOS'ta 2 işlemin ikisi de zarar (t hesaplanamaz). |
| R8-08:uzun(karsilastirma) | SPY<200g, VIX(t-1)>=30, SPY>=+%3 günü uzun (karşılaştırma kolu) | SPY | uzun | 3 | K | yok | 102.7 | -240.1 | 7 | -1.63 | 0.283 | -188 |  | -91 | -115 | 8 bölüm, %50 pozitif | ELENDİ | IS'te 6 işlemin hepsi kârlı (az olay); OOS'ta işaret döndü. |
| R8-08:uzun(karsilastirma) | SPY<200g, VIX(t-1)>=30, QQQ>=+%4 günü uzun | QQQ | uzun | 3 | K | yok | 116 | -194.4 | 5 | -1.15 | 0.498 | -198 |  | 8 | -92 | 7 bölüm, %57 pozitif | ELENDİ | IS'te 4 işlem, t=8,6 ama örneklem çok küçük; OOS'ta işaret döndü. |
| K4a-seri>=5 | IWM >=5 gün üst üste düşüş: kapanışta uzun, t+1 açılışta çık | IWM | uzun | 0 (t+1 açılış) | K | yok | 35.4 | 13.9 | 21 | -0.08 | 0.477 | -2 | 0.25 |  | 10 | 8 bölüm, %88 pozitif | DÜŞÜK | Aynı yön ama OOS t≈0; son dönemde sıfır. |
| K4a-seri>=5 | DIA >=5 gün üst üste düşüş: kapanışta uzun | DIA | uzun | 1 | K | yok | 33.3 | 41.5 | 20 | 1.51 | 0.083 | -3 | -0.36 | 47 | 25 | 6 bölüm, %100 pozitif | DÜŞÜK | Aynı yön; OOS t=1,5<2 ve n=20; son dönem negatif. |
| K4a-seri>=5 | DIA >=5 gün üst üste düşüş: kapanışta uzun | DIA | uzun | 2 | K | yok | 77.9 | 16.6 | 15 | 0.77 | 0.684 | -15 | -0.56 | 7 |  | 4 bölüm, %50 pozitif | DÜŞÜK | Aynı yön ama OOS t=0,8; son dönem negatif. |
| K4a-seri>=7 | SMH >=7 gün üst üste düşüş: kapanışta uzun | SMH | uzun | 1 | K | yok | 158 | 150.5 | 1 |  | 0.631 | 1 | 0.03 | 128 |  | 1 bölüm, %100 pozitif | DÜŞÜK | Az olay: IS'te 3, OOS'ta 1 işlem (OOS t hesaplanamaz). |
| K4a-seri>=7 | SMH >=7 gün üst üste düşüş: kapanışta uzun | SMH | uzun | 2 | K | yok | 264 | 287.1 | 1 |  | 0.565 | -46 | -0.27 | 264 |  | 1 bölüm, %100 pozitif | DÜŞÜK | Az olay (IS 3, OOS 1); son dönem negatif. |
| R8-07:RSI2<10:cikis>70 | SPY RSI(2)<10 uzun; çıkış RSI(2)>70, en çok 5 gün | SPY | uzun | değişken (en çok 5) | K | yok | 18 | 47 | 51 | 1.6 |  | 93 | 4.6 |  |  | 9 bölüm, %78 pozitif | ELENDİ | IS t=1,0, t_anormal=0,2: aday olmadı; 2020 sonrası güçlenme seçim dışı. |
| K4a-RSI2<10 | SPY RSI(2)<10: kapanışta uzun | SPY | uzun | 1 | K | yok | 1 | 40 | 98 | 1.9 |  | 33 | 2.2 |  |  | 13 bölüm, %92 pozitif | ELENDİ | IS'te net 1 bps, t=0,3; yalnız 2020 sonrası pozitif. |
| K4a-IBS<0,2 | SPY IBS<0,2: kapanışta uzun | SPY | uzun | 1 | K | yok | 4 | 13 | 216 | 0.9 |  | 6 | 1 |  |  | 12 bölüm, %75 pozitif | ELENDİ | IS t=0,4; maliyet sonrası kenar yok. |
| K4a-IBS<0,2 | QQQ IBS<0,2: kapanışta uzun | QQQ | uzun | 3 | K | yok | 28 | 47 | 147 | 2.3 |  | 28 | 1.2 |  |  |  | ELENDİ | IS t_olcekli 2,5 ama t_anormal 1,0: kazanç QQQ'nun kendi yükselişi (en yakın kaçan). |
| R7-10:r<=-1,5% | SPY r<=-%1,5: kapanışta uzun, t+1 açılışta çık (NY Fed SR917) | SPY | uzun | 0 (t+1 açılış) | K | yok | 5 | 3 | 87 | 0.7 |  | -18 | 0.1 |  |  |  | ELENDİ | Gece dönüşü maliyetten sonra yok (2020 yayını; yayın sonrası da sıfır). |
| R8-01:r<=-3% | SPY r<=-%3: kapanışta uzun | SPY | uzun | 1 | K | yok | 13 | 21 | 23 | -0.3 |  | -108 | -0.8 |  |  | 7 bölüm, %100 pozitif | ELENDİ | IS t=-0,5; son dönem -108 bps. |
| R8-03:VIX(t-1)>=35 | VIX(t-1)>=35: SPY uzun | SPY | uzun | 1 | K | yok | 51 | 6 | 53 | 0.1 |  | 65 | 0.3 |  |  | 12 bölüm, %50 pozitif | ELENDİ | IS t=1,7<2; 2008'de 46 işlemde -2.809 bps. |
| K4a-z<=-2 | SPY getiri <= -2σ: kapanışta uzun | SPY | uzun | 1 | K | yok | 1 | 53 | 41 | 1.7 |  | -15 | 0.4 |  |  | 9 bölüm, %78 pozitif | ELENDİ | IS t=-0,1. |
| R8-04:VIX(t-1)>=30:iki | VIX(t-1)>=30: SPY r<=-%1,5 uzun / r>=+%1,5 kısa | SPY | iki | 1 | K | yok | 13 | 82 | 69 | 1.7 |  | 114 | 0.9 |  |  |  | ELENDİ | IS t=0,5 (Sentana-Wadhwani 1992); 2020 sonrası pozitif ama seçim dışı. |
| R8-08:kisa | SPY<200g, VIX(t-1)>=30, SPY>=+%3 günü kısa | SPY | kisa | 1 | K | yok | -24 | 225 | 10 | 2 |  | 428 |  |  |  |  | ELENDİ | IS'te negatif (7 işlem); OOS'ta yalnız 10 işlem. |
| R8-05:MAC5:hepsi | SPY -(5 günlük getiri toplamı) işareti | SPY | iki | 1 | K | yok | -4 | -5 | 1006 | -1.7 |  | -3 |  |  |  |  | ELENDİ | Günlük işlem maliyeti kenarı siliyor (yazarların uyarısı doğrulandı). |
| R1-03:egim_alt%20 | VIX3M/VIX-1 (t-1) alt %20: SPY uzun | SPY | uzun | 1 | K | yok | 8 | 0 | 120 | 0 |  | -8 | -0.8 |  |  |  | ELENDİ | Fassas (2019) yayın sonrası sıfır; 1 gün gecikmeli VIX ile kenar yok. |
| K4a-IBS<0,2 | Dönem başı 150 hisse IBS<0,2: kapanışta uzun (havuz) | COK (hisse) | uzun | 1 | K | yok | -1 | 10 | 33141 | 1.2 |  | 5 | 0.6 |  |  |  | ELENDİ | IS t_kume=-0,3. |
| K4a-seri>=7 | SPY >=7 gün üst üste düşüş: kapanışta uzun | SPY | uzun | 1 | K | yok | 138 | 423 | 1 |  |  |  |  |  |  | 4 bölüm, %100 pozitif | ELENDİ | IS'te 4 işlem, t=0,8: sınanamayacak kadar az olay. |

## Elenenler

- **IS'te elenen 664 varyant** (aday olmayan her şey ELENDİ):
  - R8-01: SPY/QQQ'da ≤−%3 günü. IS t ≤ 0,8; son dönem negatif.
  - R8-02: teyitli giriş, 4 kol. n=5–9; ertesi gün aşağı kolu IS'te +197 bps ama t=2,4 ve t_anormal 1,8, aday değil.
  - R8-03: VIX(t−1) eşikleri ve yüzdelik. Yalnız ≥40 + 5 gün bekleme aday oldu, OOS'ta işareti döndü. Diğer eşiklerde IS t < 2. 2008 ve 2020 felaketlerinde ağır kayıp.
  - R8-04: VIX koşullu dönüş. IS t ≤ 1,2; 2020 sonrası pozitif.
  - R8-05: MAC(5). Maliyet sonrası negatif, IS t −2,3.
  - R8-06: tam N günlük seri. Yalnız N=6 QQQ gece aday oldu, OOS n=2 ve ikisi de zarar.
  - R8-07: RSI(2) değişken çıkış. IS t 0,8–1,0; son dönem +88/93 bps (t 2,7/4,6) ama seçim dışı.
  - R8-08: ayı rallisini satmak. Kısa kolun IS'i negatif; karşılaştırma uzun kolu IS'te n=4–6 ile aday, OOS'ta döndü.
  - R1-03 (Fassas, eğim): yayın sonrası sıfır.
  - R1-04 (VIX 2 yıllık zirve): n=8 bölüm, %40 pozitif.
  - R1-11: VIX/VIX3M<1 tutma. Kazanç tamamen piyasanın kendi eğilimi (t_anormal ≈ 0).
  - R1-14 (VIX9D/VIX): IS t < 1.
  - R7-10 (NY Fed gece dönüşü): gece çıkışında maliyet sonrası ~0.
  - Denetçi eki: SPY/QQQ'da IBS<0,2 ve RSI(2)<10 IS'te 1–28 bps. QQQ IBS h=3'te t=2,5 çıktı ama anormal getiri şartı (t_anormal=1,0) sağlanmadı.
  - IBS>0,8 ve RSI(2)>90 kısa kolları her yerde negatif (havuzda IS t_olcekli −23).
  - −2σ/−3σ: IS t < 1. Sektör ETF'leri ve hisse havuzunda aday yok.
- **OOS'ta elenen 5**: R8-03 ≥40 bekleme (SPY, QQQ), R8-06 N=6 QQQ gece, R8-08 karşılaştırma uzun (SPY, QQQ). Hepsinde işaret döndü.
- **DÜŞÜK 5**: DIA seri≥5 (h=1, h=2), IWM seri≥5 (gece), SMH seri≥7 (h=1, h=2). Aynı yöndeler ama OOS t < 2 ya da 1 işlem.
- UYGUN ya da KOŞULLU sonuç yok.

## Bugünkü durum

**20 Kasım 2026 kapanışı** (SPY 689,81; 200 günlük ortalama yaklaşık 732,8, yani %5,5 altında; 7 gün üst üste düşüş; zirveden −%11,5).

Hiçbir kural OOS'tan geçmediği için "geçen kuralın açık sinyali" yok. Elenmiş kurallardan 20 Kasım'da açık olanlar bilgi amaçlıdır, kullanılmamalı:
- R8-01 (SPY ve QQQ ≤−%3; SPY o gün −%3,6)
- R7-10 (≤−%1,5 ve ≤−%2,5)
- R8-06 seri==7 (SPY)
- R8-07 ve denetçi RSI(2)<10 (9 ETF'nin hepsinde; havuzda 107 hisse)
- IBS<0,2 (9 ETF; 132 hisse)
- seri≥7 (SPY, SMH, XBI)
- −2σ (SPY, QQQ, SMH, SOXX)

20 Kasım'da VIX(t−1) 28,44 olduğu için VIX≥30/35 koşullu kurallar kapalıydı. Aynı gün VIX (16:15) 35,89'du; bu yalnız sızıntılı satırda kullanıldı.

**23 Kasım kapanışı için tetikler.** VIX(t−1) = 35,89 olacağından VIX≥30/35 koşulları sağlanmış sayılır. Bu kurallar hep elenmiş durumda; SPY fiyatı ve S&P karşılığı (6910 × SPY/689,81):

| Kural | SPY koşulu | S&P karşılığı |
|---|---|---|
| R8-03 VIX≥35'te uzun | fiyattan bağımsız tetiklenir | — |
| Her aşağı kapanış: seri 8 olur, seri≥3/5/7 açılır | < 688,09 | < 6.893 |
| RSI(2)<10 açık kalır | ≤ 691,5 (+%0,25'e kadar) | ≤ 6.927 |
| R7-10 ve R8-04 uzun kolu (≤−%1,5) | ≤ 679,46 | ≤ 6.806 |
| R8-01 (≤−%3) | ≤ 669,12 | ≤ 6.703 |
| −2σ | ≤ 665,7 (−%3,5) | ≤ 6.668 |
| −3σ | ≤ 655,3 | — |
| R8-08 kısa (SPY<200g ve VIX(t−1)≥30) | ≥ 710,50 (+%3) | ≥ 7.117 |

R8-08 kısa için QQQ eşiği ≥ 632,8 (+%4). Seri==5, seri==6 ve VIX 504 gün zirvesi tetiklenmez.

**Tarihsel analog** (SPY 7+ gün düşüş, 2005–2026, 7 bağımsız seri, hepsi 200 günlük ortalamanın altında). Sonraki getiriler:

| Gün | Ortalama | Medyan | İsabet | En kötü |
|---|---|---|---|---|
| 1 | +%2,69 | +%0,78 | %71 | −%2,64 |
| 2 | +%2,54 | +%2,28 | %71 | −%4,17 |
| 3 | +%2,25 | +%2,16 | %86 | −%4,31 |
| 5 | +%1,75 | +%1,70 | %86 | −%6,38 |

- **Ek olarak VIX(t)≥30 olanlar** (4 seri, 5 gün: 10 Ekim 2008, 25 Kasım 2011, 21/24 Aralık 2018, 28 Şubat 2020): 1 günde ortalama +%4,8 (en kötü −%2,6), 3 günde +%4,7 (en kötü +%1,7).
- **Gevşek koşul, seri≥5 ve VIX≥30** (23 gün, 12 bölüm): 1 günde +%1,1, isabet %57, en kötü −%7,0. 2 günde +%2,3, en kötü −%9,2. 5 günde +%2,6, en kötü −%7,7.

Analog sayısı küçük ve ortalamayı 2008'in +%14,5'lik tek günü taşıyor. Betimsel, doğrulanmış sinyal değil. Ayrıca içinde bulunduğumuz Ekim–Kasım 2026 bölümünde "düşeni al" kuralları zarar etti: RSI(2)<10, 7 işlemde −728 bps.

## Sapmalar

1. **h=5 sınanmadı.** Kurallarda yazılı h=5 (R8-01, 02, 03, R1-03, 04) YONTEM ızgarasındaki h=1,2,3 ve "t+1 açılış" çıkışıyla değiştirildi. h=5 yalnız bugünkü analog tablosunda betimsel olarak var.
2. **Rejim kovaları.** R8-01'deki VIX≥35 × 200g dört kovası yerine YONTEM'in standart rejimleri raporlandı: VIX(t−1) <20 / 20–30 / >30 × 200 günlük ortalamanın üstü/altı.
3. **VIX'e dayanan kurallarda 1 gün gecikme.** Kural metni "aynı kapanış" diyor; SONRA sınıfı gereği VIX, VIX3M ve VIX9D 1 gün gecikmeli kullanıldı. Aynı gün VIX yalnız R8-03-SZ "sızıntılı üst sınır" satırlarında var; bunlar teste ve adaylığa katılmadı.
4. **R8-07 değişken çıkış.** Çıkış "RSI(2)>70/90, en çok 5 gün" kuralıyla belirlendi. Girişler çıkış gününe göre ayrıldı, her parça motorun islemler(h=k) işleviyle hesaplandı ve istatistik motorun _ozet işlevinden alındı. Günlük seri parçaların gunluk toplamı. mdd, yıllık net ve bootstrap yalnız 'hepsi' satırında. sonuc_K4a.csv'de h=5 ve cikis='rsi>70' olarak kodlandı.
5. **R1-11 bir tutma stratejisi.** Her gün yenilenen 1–3 günlük sinyal olarak yaklaşık hesaplandı; bu, maliyeti olduğundan fazla gösterir.
6. **Seri tanımı.** R8-06 "tam N. düşüş" (==N) olarak, denetçi eki "≥N" olarak tanımlandı; ikisi ayrı varyant.
7. **IS adaylığı.** Yalnız Giriş K, korunmasız, hisse başı komisyon satırlarından belirlendi. Korunmalı ve Giriş A/G varyantları test sayısına katılmadı (gereği OOS'tan geçen olmadığı için doğmadı).
8. **Ek satırlar test sayısına katılmadı.** Kaldıraçlı ETF satırları ve rejim satırları raporlandı ama seçimde kullanılmadı.
9. **OOS satırları elenenler için de yazıldı.** Aday listesi dosyaya yazılıp kilitlendikten sonra, bilgi amaçlı ve tam şema için yazıldı. Seçimde kullanılmadı.
10. **RSI(2) başlangıcı.** Wilder yumuşatması ilk farkla başlatıldı (SMA tohumu yok); α=0,5 olduğu için birkaç günde etkisi kalmaz.
11. **Yapılmayanlar.** OOS'tan geçen olmadığı için 15:30 testi (K4a_1530.csv üretilmedi), bölünme-düzeltmeli fiyatla örtüşme, ikinci kaynak, sağlamlık ve komşu parametre testleri yapılmadı.

## Notlar

**Motor ve veri**
- Motorda hata bulunmadı. bakis_testi üç kesim tarihinde (2015, 2021, 2025) temiz geçti.
- Hisse havuzunda evren sütunları bozuk kopyaya göre değiştiği için ileriye bakma testi günlük toplamlarla yapıldı.

**Mükerrer varyant**
- R1-03 kontrol kolu (s>0, yani VIX3M>VIX) ile R1-11 (VIX/VIX3M<1) matematiksel olarak aynı koşul. İkisi de test sayısında (674), sonuçları birebir aynı.

**İnanılmayacak kadar iyi görünen sonuçlar**
- >100 bps, t>6 ya da isabet >%70 olan sonuçların hepsi 3–10 olaylık örneklerden geliyor: R8-08 karşılaştırma kolunda QQQ n=4 t=8,6, SMH seri≥7 n=3, VIX≥40 n=7.
- Veri ya da ileriye bakma hatası değil, küçük örneklem. Hepsi OOS'ta düştü.

**Ana ajanın bilmesi gerekenler**
- **BH için p-değerleri.** 10 adayın OOS p_bootstrap değerleri: 0,602; 0,664; 0,241; 0,283; 0,498; 0,477; 0,083 (DIA h1); 0,684 (DIA h2); 0,631; 0,565. Hiçbiri BH'den geçmez. Hesaplanamayan yok.
- **Sonradan bakılan rejim örüntüsü.** VIX(t−1)>30 ve SPY 200 günlük ortalamanın altında, "düşeni al" kuralları 2005–2026 toplamında güçlü:
  - SPY RSI(2)<10 h=1: n=61, +141 bps, t 2,8
  - IBS<0,2: n=102, +81 bps, t 3,0
  - −2σ: n=13, +291 bps
  - hisse havuzunda IBS<0,2: +96 bps, t_kume 2,5

  Ama VIX>30'da IS zayıf (RSI(2) h=1: n=23, +36 bps, t 0,6) ve 13 rejim × 674 varyantlık çoklu test içinde sonradan seçilmiş bir alt küme. Doğrulanmış sayılmamalı. Ayrıca 2008 Eylül–Kasım ve Ekim–Kasım 2026 bölümleri kayıplı. Bu satırlar "bugünkü rejimde destekli" ölçütünü de sağlamaz, çünkü adaylık yok.
- **2020 sonrası güçlenme.** RSI(2)<10 ve R8-07 2020 sonrası (OOS ve son dönem) pozitif ama IS'te yok. Bir rejim değişimi olabilir; bu yöntemle sınanamaz.
- **Kaldıraçlı satırlar.** Örnek: SPY RSI(2)<10 → UPRO, h=1, IS +2 bps, OOS +124 bps, son dönem +96 bps. IS zayıflığı aynen sürüyor.
- **SOXS ve SQQQ.** Ters bölünmeler yüzünden bazı günler hedef dışında kalmış olabilir (MOTOR.md bilinen sınır).
- **Felaket dönemlerindeki kayıplar** (Eylül–Kasım 2008, Şubat–Mart 2020, 2022): K4a_felaket.csv.
- **VIX>30 bölüm tabloları** (her bölüm için işlem sayısı, toplam ve en kötü işlem): K4a_vix30_bolum.csv.

## Dosyalar

- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/kod/aile_K4a.py
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/aday_K4a.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/sonuc_K4a.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/K4a_oos_kontrol.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/K4a_sinif.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/K4a_vix30_bolum.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/K4a_felaket.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/K4a_bugun_analog.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/K4a_bugun_analog_ozet.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/K4a_bugun_sinyal.csv
- /home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun/ek/veri/K4a_tetik_23kasim.csv
