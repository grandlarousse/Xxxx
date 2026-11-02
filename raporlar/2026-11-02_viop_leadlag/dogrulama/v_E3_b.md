# v_E3_b — 2. aşama çürütme denemesi: ABD rafineri sepeti (VLO, MPC, PSX, PBF) t-1 → TUPRS gün-içi (t)

Doğrulayıcı: v_E3_b (şeytanın avukatı). Tarih: 02.11.2026.
Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b/` (vb.py kendi kütüphanem; 01_build … 11_fut_bt; çıktılar `res/`, loglar `res/*.log`).
ll.py, elib.py ve vlib.py import edilmedi. Ham parquet'ten kendi hizalamam kullanıldı:
- BIST takvimi: TUPRS ∩ XU100 (v>0).
- Gün-içi = ln(c/o).
- Temizlik: fiyat bazlı c_t/c_{t-1}, [0,895; 1,105] aralığı dışındaysa NaN.
- ABD sinyali: yerel tarih ≤ t_{-1} olan son kapanış (A). "Taze" sürüm (C): yerel tarih < t.
- USDTRY: t günü 00:00 UTC'ye kadarki değişim; BIST açılışından önce bilinir.
- VİOP testi: 2.026 resmi BIST bülteninden (2017–2026; 2019 büyük ölçüde eksik) F_TUPRS ve F_XU030 kendim ayrıştırdım.

## Hüküm: DÜZELT
- İlişki gerçek: tüm çürütme testlerinden sağ çıktı. Güven ORTA.
- Ama dört önemli düzeltme var:
  1. 2014–2017'de etki yok.
  2. IS kanıtı kısmen jenerik bir "ABD t-1" etkisi.
  3. Etki rafineriye özgü değil, "ABD enerji hissesi"ne özgü.
  4. İşlenebilirlik açılış seansı dolumuna bağlı ve açılış seansı çok sığ.
- Strateji güveni:
  - Tek bacak: DÜŞÜK.
  - F_XU030 hedge'li: DÜŞÜK–ORTA.

## 1. Yeniden üretim (bağımsız kod)

| İddia | Benim | Not |
|---|---|---|
| y_h (TUPRS−XU100 gün-içi) ~ US_REF_{t-1}, ES+BZ kontrollü t=4,5 | ALL 4,57 / IS 2,09 / OOS 3,86 (n 3.204). Tek değişkenli: 5,14 / 3,04 / 4,30 | Tuttu |
| VLO tek başına IS 3,8 / OOS 4,5 | 3,70 / 4,40 (y_h). Ham TUPRS gün-içinde 1,96 / 3,11 | Hedge'li hedefe ait |
| ~%62 gün-içinde | Ham: gap b 0,030, gün-içi b 0,049, pay 0,63. **Hedge'li: gap b 0,008 (t 1,2), gün-içi 0,063 (t 5,1), pay 0,89. IS'de hedge'li gap b = 0,000** | TUPRS'a özgü kısım açılışta HİÇ fiyatlanmıyor |
| BT \|z\|>1 tek bacak brüt IS 17,7 (t 2,4) / OOS 25,6 (t 2,3) | Ham TUPRS: IS **14,2 (t 1,96, n 501)** / OOS 25,8 (t 2,28, n 361). Hedge'li: 17,5 (2,32) / 33,5 (3,54) | IS'de 3,5 bps daha düşük; temizlik/hizalama farkı izlenemedi |
| Net 8 bps Sharpe IS 0,44 / OOS 0,62; 15 bps 0,12 / 0,37 | Ham: 8 bps 0,29 / 0,63; 15 bps **−0,04** / 0,38 | IS net kârlılık yok |

## 2. Veri madenciliği ve seçim yanlılığı (en önemli yeni bulgular)
- **Kaç varyant denendi?**
  - Enerji ajanı 39.060 tarama testi yaptı. Bunların 6.510'u H1 ailesinde; TUPRS için 1.085 sürücü denendi.
  - Ayrıca 17+4 backtest ve 2 bölgesel sepet (ABD/AB) denendi.
  - 1. aşama 12 eşik×pencere kombinasyonu denedi; ben 16.
  - Tarama tam dönem (OOS dahil) üzerinde yapıldı. Yani VLO özelinde "OOS" saf değil.
  - Sepet 02_tuprs.py'de sektörel tanımla kuruldu. DK aday listesindeydi ama sepete alınmadı; DINO, CVI ve PARR hiç denenmedi.
- **Yalnız IS (2014–2020) taraması (1.069 sürücü):**
  - VLO 6. sırada (t 3,84), US_REF 13. sırada (3,42).
  - IS'nin ilk 5'i OOS'ta tamamen çöküyor: KCHOL t 4,28 → −0,22; CCL 4,08 → −0,24; IAG.L, AER, STR.VI.
  - IS'de BH-FDR'den 12 sürücü geçiyor. Bunlardan **yalnız 2'si OOS'ta tekrarlıyor: VLO (4,50) ve PARR (3,13); ikisi de rafineri.**
  - Saf veri güdümlü bir IS seçimi bu ilişkiyi tek başına bulamazdı. Bulguyu ayakta tutan şey ekonomik ön bilgi (rafineri → rafineri).
- **Jenerik ABD etkisi:**
  - IS'de sürücülerin %20'sinde |t|>2 (şansla beklenen %5).
  - 5.000 rastgele 4'lü ABD hisse sepetinin ortalama t değeri IS'de **1,74**, OOS'ta 1,20.
  - US_REF IS'de dağılımın %1,7'lik üst kuyruğunda, OOS'ta %0,04'lük kuyrukta.
  - Enerji içermeyen sepetlerin %95 üst sınırı IS 3,04, OOS 2,29.
  - Sonuç: IS anlamlılığının yaklaşık yarısı jenerik bir "ABD t-1 → TUPRS−XU100 gün-içi" kaymasından geliyor. OOS'taki ayrışma ise güçlü.
- **Sepet seçimi kiraz toplama değil:**
  - 9 ABD rafinerisinden (VLO, MPC, PSX, PBF, DINO, DK, CVI, PARR, CLMT) kurulabilecek 126 dörtlü sepetin hepsinde OOS t ≥ 3,38 (medyan 3,98). IS medyanı 2,58 (min 1,74).
  - Seçilen sepet IS'de 126 içinde 18. sırada.
  - **Sepet dışı rafineriler (DINO, DK, CVI, PARR): IS 2,42 / OOS 3,65.**

## 3. Ortak faktör kontrolleri (y_h, NW t; ALL / IS / OOS)
Eklenen kontroller ve sonuçlar:
- ES + BZ: 4,57 / 2,09 / 3,86.
- + EEM, USDTRY, TUR, VIX: 4,68 / 2,25 / 3,88.
- + XLE: 3,43 / **1,63** / 2,91.
- + CL, HO, RB, NG: 3,39 / 1,68 / 2,77.
- + BIST gecikmeleri (TUPRS, XU100, XKMYA, XUSIN, AYGAZ, PETKM cc_{t-1}; TUPRS gün-içi_{t-1}; y_h_{t-1}) + gap_t (TUPRS, XU100): **3,36 / 1,50 / 2,74.**

Diğer bulgular:
- US_REF XU100 gün-içini öngörmüyor (t −1,3). Etki piyasa değil, TUPRS'a özgü.
- USDTRY, EEM ve TUR etkisiz.
- **Rafineriye özgü değil, "ABD enerji hissesi":**
  - Tek değişkenli y_h t (ALL): XLE 4,16, COP 4,35, XOM 3,63, SHEL 3,49, CRAK 4,39, VLO 5,75.
  - Emtialar zayıf: BZ 1,67, CL 0,68, HO 1,09.
  - US_REF'in XLE'den arındırılmış kısmı: ALL 3,23 / IS **1,65** / OOS 2,99.

## 4. Plasebolar
- **Gecikme profili (y_h):** k=1'de 5,14; k=2'de 0,85 (IS −1,04); k=3..6'da 1,1–2,7.
  - "Gelecek" sinyal (k=−1): −1,35.
  - 20 günlük yavaş bileşen kontrolünde k=1 değişmiyor (ALL 4,98).
  - OOS'ta t-2..t-6 toplamı da anlamlı (t 3,76): çok günlü yavaş yayılma var.
- **Rastgele işaret (10.000), BT \|z\|>1 y_h:** ALL p<0,0001, IS p=0,008, OOS p=0,0007.
- **Rastgele işaret, corr:** IS p=0,003. Yıl-içi karıştırmada p<0,001.
- **Kesitsel (145 BIST hissesi, hedge'li gün-içi):**
  - **TUPRS 1. sırada**, DOCO 2., AYGAZ 3. (3,52).
  - |t|>2 olan 12 hisse var, şansla beklenen 7,2.
  - Diğer hisseler: PETKM 0,90; THYAO 0,25; EREGL 0,46; AKBNK −0,99.

## 5. Alt dönem istikrarı

| Dönem | y_h tek değişkenli t | y_h tüm kontroller t | BT ham TUPRS brüt bps (t) | BT hedge'li brüt bps |
|---|---|---|---|---|
| 2014–17 | **0,82** | **0,24** | **3,1 (0,38)** | 2,5 |
| 2018–20 | 2,98 | 1,56 | 26,2 (2,24) | 33,7 |
| 2021–23 | 3,19 | 2,41 | 25,6 (1,37) | 25,9 |
| 2024–26 | 2,88 | 0,74 | 25,9 (1,88) | 39,6 |

- **2014–2017'de etki yok.** Yıllık değerler: 2014 +24, 2015 +2, 2016 +8, 2017 −34 bps. IS anlamlılığı tamamen 2018–2020'den geliyor.
- 2024–26'da tüm kontrollerle t 0,74. Son dönemde sinyal, HO/RB/XLE gecikmelerinden ayırt edilemiyor; işlem açısından bu sorun değil.
- **Son dönem:**
  - Ağustos–Ekim 2026 (fon krizi): ham −61,7 bps (22 işlem), hedge'li −32,8.
  - 2026Ç4: −78 bps (10 işlem).
  - Mart 2025 şoku: ham −29 bps.
  - Gürültüyle uyumlu (SE ≈130 bps), ama yurt içi kriz rejimlerinde çalışmıyor.
- **Yıllara göre pozitiflik:** ham 11/13 yıl, hedge'li 10/13 yıl.

## 6. Uç değer bağımlılığı
- **Simetrik testlerde dayanıklı:**
  - İki uçtan 10'ar işlem atılınca: ham ALL 19,4 (t 3,32); hedge'li 25,2 (4,74).
  - %1 winsor: 18,3 (2,95).
  - Huber t: y_h 5,52 / 3,25 / 4,55.
  - En etkili 10 gözlem hariç NW t: 3,91 / 2,16 / 3,52.
  - Medyan işlem: ham ALL +21, OOS +30 bps.
  - İsabet: %55 (p=0,002); OOS %57.
  - z kovaları monoton: z<−2'de −40 bps, z>2'de +39 bps.
- **Tek yönlü test kırılgan (en iyi 10 işlem atılınca):**
  - Ham IS 3,7 bps (t 0,55); OOS 11,3 (1,10); ALL 12,3 (2,06).
  - Hedge'li ALL 18,1 (3,28); IS 8,0 (1,15); OOS 20,6 (2,23).
  - Tek bacak net kârlılık birkaç büyük güne bağlı.

## 7. Açılış fiyatı gerçekçiliği ve likidite
- **Yahoo açılış fiyatı:** son 60 günde Yahoo `o` = 06:55 müzayede barı (60/60).
- **Yahoo'dan bağımsız test, gerçek F_TUPRS bülten verisi:**
  - Vadeli açılış→kapanış ~ US_REF, NW t: 3,51 (1.992 gün); 2020–26'da 3,29; 2023–26'da 3,59.
  - F_TUPRS − F_XU030: 4,81.
  - BT \|z\|>1 F_TUPRS: brüt 27,3 bps (t 2,60, n 541).
  - Hedge'li: 35,0 bps (t 4,15).
  - **Etki Yahoo açılış artefaktı değil.**
- **2020+ likit dönem, gerçek vadeli:**
  - Tek bacak net 8 bps: 20,7 bps (t 1,72, Sharpe 0,67, bootstrap %2,5 alt sınırı 2,0).
  - Tek bacak net 15 bps: 13,7 bps (t 1,14, alt sınır −5,4).
  - **F_TUPRS − F_XU030 net 11 bps (8+3): 28,0 bps (t 3,03, Sharpe 1,09, alt sınır 14,3).**
  - Hedge'li net 18 bps: 21,0 (t 2,28).
- **AMA vadeli açılış fiyatı = açılış seansı fiyatı (%100):**
  - Açılış seansı günlerin yalnız %64–88'inde oluşuyor.
  - Medyan değer 80–380 bin TL (3–15 kontrat; 1 kontrat ≈ 25,8 bin TL), 3–5 işlem.
  - Büyük emir açılış fiyatından dolmaz.
- **Gerçekçi giriş (saatlik, 2023-11+, 205 işlem):**

  | Giriş | Brüt bps (t) | Net 8 | Net 15 |
  |---|---|---|---|
  | Açılış | 25,8 (1,87) | | |
  | 10:30 TSİ | 14,1 (1,26) | 6,1 | **−0,9** |
  | 11:30 TSİ | 13,4 | | |
  | 13:30 TSİ | 8,3 | | |
  | Hedge'li 10:30 | 21,1 (2,17) | ~10 (8+3 maliyetle) | |

- **Kontrat likiditesi:**
  - F_TUPRS 2017–18'de medyan 45 işlem/gün, ~1,3 mn TL/gün; 2020'de 47 mn TL.
  - 2023+ dönemde 566–1.894 mn TL/gün, >10 bin işlem; 2025+ açık pozisyon ~107 bin kontrat.
  - **IS (2014–2020) backtesti VİOP'ta uygulanamazdı.** Spot TUPRS likit, ama short için açığa satış/ödünç gerekir.

## 8. Mekanizma (1. aşamayla uyumlu, genişletildi)
- VLO saatlik, 2023-12+, n=678. t-1 getirisi 14:30 UTC'de ikiye bölündü:
  - **(i) BIST seansı t-1 sırasında bilinen kısım:** gün-içini öngörüyor (ham t 2,59; hedge'li 2,69); gap'i öngörmüyor (0,67).
  - **(ii) BIST kapanışından sonraki kısım:** gap'te fiyatlanıyor (t 3,73); gün-içine etkisi yok (ham 0,44).
- XLE'de de aynı desen görülüyor.
- Yorum: ABD enerji hisselerinden gelen sektör bilgisi TUPRS'a ~1 gün gecikmeyle, açılış müzayedesinde değil seans içinde yayılıyor (yavaş yayılma).
- Uyarı: bu bir korelasyon; nedensellik kanıtlanmadı.

## 9. 1. aşamayla farklarım
1. 2014–17'de etki yok. 1. aşama 2014–16'yı pozitif (t 1,55) göstermişti. Etki 2018'den beri var.
2. Seçim yanlılığı "sınırlı" denmişti. Sepet seçimi için bu doğru. Ama IS'de jenerik ABD etkisi güçlü (rastgele sepet ortalama t 1,74). Saf IS seçimi bu ilişkiyi bulamazdı; kanıtın gücü ekonomik ön bilgiye ve OOS'a dayanıyor.
3. Özgüllük rafineri değil, ABD enerji hissesi. Arındırılmış rafineri kısmının IS t değeri 1,65.
4. Gerçek VİOP verisi işlenebilirliği DESTEKLİYOR: hedge'li 2020+ net 28 bps, t 3,0. Ama yalnızca küçük boyutta ve açılış seansında. 10:30 girişte tek bacak 15 bps maliyetle sıfır.
5. Son 3 ay (fon krizi) negatif.

## TradingView
NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF (sepet dışı doğrulama: NYSE:DINO, NYSE:DK, NYSE:CVI, NYSE:PARR), AMEX:CRAK, AMEX:XLE, BIST:TUPRS, BIST:AYGAZ, BIST:XU100, BIST:XU030.
VİOP F_TUPRS ve F_XU030 için TV sembolü doğrulanamadı ('?').
