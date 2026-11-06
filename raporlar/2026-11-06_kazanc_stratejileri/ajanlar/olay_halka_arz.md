# Olay çalışması: Borsa İstanbul halka arzları, 2020–2026 (anahtar: `halka_arz`)

Tarih: 06.11.2026. Veri sonu: 05.11.2026 kapanışı. Yatırım tavsiyesi değildir.

## 0. Karar (kısa)

| Soru | Cevap | Güven |
|---|---|---|
| Katılımcı (arz fiyatından alan) para kazanıyor mu? | Evet. Arz başına medyan **+%45**, ortalama +%67 (tavan bozulduğu gün AOF'tan satış). Arzların %91'inde kâr var. | Yüksek |
| Ne kadar TL? | Az. Eşit dağıtım lotu küçük. Tek hesapla bütün arzlara girilirse yıllık nominal kâr: 2023'te **≈27 bin TL**, 2024'te **≈10 bin**, 2025'te **≈13 bin**, 2026'da (Kasım'a kadar) **≈24 bin TL**. Arz başına medyan kâr 250–450 TL. | Yüksek |
| Tavan serisi bitince almak kâr mı? | Hayır. E kapanışında al: XU100'e göre 5 gün **−%3,7** (t_küme −2,5), 21 gün medyan **−%11**, isabet %36. Takvim-zamanı portföyü XU100'ün çok altında. 63–126 günde ortalama pozitif ama bunu 10 "piyango" hisse yaratıyor; medyan negatif. | Yüksek (5–21 gün) |
| Seri bitince açığa satmak / uzak durmak? | İstatistikte 5 günlük devam eden düşüş var (net +%3,5, t_küme 2,4, isabet %67). Ama 2024–26'da anlamlı değil (t 1,2). Yeni arz payında ödünç pay ve VİOP yok, sol kuyruk −%38 (p5). **Uygulanabilir sonuç: "uzak dur" ve katılımcıysan "seri bitince sat".** | Orta |
| Gün1 tavandan almak? | Gün1'lerin %68'i kilitli tavan; bu günlerde alış emri dolmuyor. Sonradan görülen +%38'lik (5 gün) getiri bu yüzden kâğıt üstünde. Dolabilen 79 günde fazla getiri ≈0 (5 gün +%0,7, 21 gün medyan −%9,8). | Yüksek |
| Satmama taahhüdü (lock-up) bitişi | Etki yok: CAR[0,+5] %0,0, CAR[0,+20] %0,0 (n=200, t≈0). | Yüksek |

Özet: Halka arzda gerçek kazanç **katılım primi**. Bu prim de lot küçüldükçe TL olarak küçüldü. **Seri sonrası** dönemde fiyat ortalamada geri veriyor; bunu kullanmak için gereken açığa satış pratikte mümkün değil. TL eşiğini (%36–40) geçen, sermaye ölçeklenebilir bir halka arz stratejisi bulamadım.

---

## 1. Veri ve yöntem

**Arz listesi.** halkarz.com yıllık arşivinden alındı (2020–2026 sayfaları; ilk sayfalar curl'ün varsayılan başlığıyla indirildi). Toplam 247 kayıt var. Detay sayfalarına önce betikle gidildi ama site `python-requests` istemcisine **HTTP 403** verdi. Tarama orada durduruldu; başlık taklidi ya da engeli aşma denemesi yapılmadı. Bundan sonra her detay sayfası WebFetch aracıyla tek tek okundu. Sayfalardan alınan alanlar: arz tarihi, fiyat, dağıtım yöntemi, lot, ek satış, pazar, ilk işlem tarihi, büyüklük, bireysel kişi sayısı ve lotu, satmama taahhüdü, fiyat istikrarı, iskonto.

- **Hariç tutulanlar (7):**
  - BEWEN (ertelendi)
  - ENPRA ve MARMR (kısmi bölünme; arz değil)
  - ERCB (doğrudan kotasyon, arz verisi yok)
  - GMTAS (talep toplama yok)
  - DMLKT (gayrimenkul sertifikası)
  - ARDYZ (06.02.2020): O tarihte günlük marj ±%20 idi, seri tanımı diğerleriyle karşılaştırılamaz.
- **Nihai örneklem: 240 arz.** Yıllara dağılım (ilk işlem yılı): 2020: 7, 2021: 52, 2022: 38, 2023: 56, 2024: 33, 2025: 18, 2026: 36.
- **Fiyat aralığıyla satılan 9 arz:**
  - Nihai fiyat haber/şirket bülteninden alındı: ARZUM 17,00, KRVGD 9,00, AYDEM 9,90, BIOEN 18,00, PENTA 32,00.
  - İlk gün fiyat limitinden çıkarıldı: KLKIM 14,75, MERCN 8,81, ANGEN 22,50, HTTBT 12,25 (ör. KLKIM'de ilk gün en yüksek fiyat 16,22 = 14,75×1,10). PENTA için bu yöntem 32–35 aralığını vermişti; haber 32,00'ı doğruladı.
- **Tutarlılık kontrolü:** Gün1 baz fiyatı arz fiyatıdır. 240 arzın hepsinde gün1 getirisi [−%10; +%10,05] içinde kalıyor; yani arz fiyatları borsa limitleriyle uyumlu. halkarz'daki ilk işlem tarihi 235 arzda fiyat verisiyle aynı gün. Farklı olan 5 arzda (MANAS, TRILC, DNISI, EGEPO, GENIL) veri tarihi kullanıldı.

**Fiyatlar (İş Yatırım, varsayılan başlıklar, tek istek, ~0,8 sn ara):**
- `ChartData IndexHistoricalAll`: günlük düzeltilmiş kapanış. Birincil seri.
- Aynı sitenin "Hisse Tekil" verisi (`Data.aspx/HisseTekil`): düzeltilmemiş kapanış, gün içi min/max, AOF ve hacim. Kilitli tavan tespiti ve arz fiyatına göre gün1 getirisi bunu gerektiriyor.
  - HG_* düzeltilmemiş, HGDG_* düzeltilmiş seridir.
  - İki düzeltilmiş seri günlük getiride birebir aynı (arz başına %99 persentil fark 6e-6).
  - Hisse Tekil'de TKNKA'nın ilk günü eksik, CITAS hiç yok. Bunlarda yalnız ChartData kullanıldı; kilit bilgisi yok.

**Bedelsiz/bölünme düzeltmesi doğrulandı.** Düzeltilmemiş seride |günlük getiri| >%11 olan 179 gün var (122 hisse; bedelsiz/bölünme). Bunların hepsinde düzeltilmiş seri normal aralıkta. Örnekler (ham → düzeltilmiş):

| Hisse | Tarih | Ham | Düzeltilmiş |
|---|---|---|---|
| KONTR | 19.07.2024 | −%67 | +%6,8 |
| CWENE | 04.12.2024 | −%88 | −%3,1 |
| MIATK | 20.11.2023 | −%93 | −%9,1 |
| SDTTR | 27.08.2026 | −%91 | +%3,2 |
| YEOTK | 03.08.2022 | −%72 | +%10,0 |
| EUPWR | 08.10.2024 | −%68 | −%3,5 |

Düzeltilmiş seride |getiri| >%10,5 olan tek gün kümesi ARDYZ'nin ±%20 dönemine ait. Arz fiyatından toplam getiri şöyle hesaplandı: (ham gün1 / arz fiyatı) × (düzeltilmiş P_t / düzeltilmiş P_gün1).

**Tanımlar.** Hepsi önceden belirlendi; ızgaranın tamamı raporlandı.

- **Tavan günü:** Kapanış ≥ önceki kapanış×1,10'un fiyat adımına aşağı yuvarlanmışı (1 adım tolerans). Düz %9,5 eşiğiyle yalnız 3 arzın seri uzunluğu 1 gün değişiyor.
- **Kilitli tavan:** Tavan günü ve gün içi min = max. Bu günde alış emri dolmuyor.
- **Seri:** Gün1'den başlayan ardışık tavan kapanışları.
- **E:** Seriden sonraki ilk tavan olmayan gün.
- **Fazla getiri ölçüleri:**
  - BH: XU100'e göre al-tut farkı.
  - CAR: günlük (r_i − r_m) toplamı.
  - CARb: r_i − β·r_m (β, E+1..E+250 günlerinden).
- **İstatistik:** t_küme, giriş ayına göre kümelenmiş standart hatayla hesaplandı. Takvim-zamanı portföyü örtüşmeyi ayrıca ele alıyor.
- **Maliyet:** Spot gidiş-dönüş 25 bp.
- **Kapsam dışı:** Bu hisselerin hiçbiri seri döneminde VİOP'ta değildi (47 pay vadelisinden yalnız ASTOR örnekte var, o da sonradan eklendi).

---

## 2. Örneklem: ilk gün ve tavan serisi

| Yıl | n | Eşit % | Bireysel kişi (medyan, bin) | Kişi başı alınan TL (medyan) | Büyüklük (medyan, mn TL) | Gün1 tavan % | Gün1 kilitli % | Seri ort. / medyan | Seri ≥5 % | Seri ≥10 % | Arz→tepe medyan / ort. % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2020 | 7 | 43 | 176 | 818 | 50 | 100 | 100 | 8,1 / 9 | 100 | 14 | 134 / 120 |
| 2021 | 52 | 63 | 75 | 1.792 | 272 | 69 | 52 | 3,0 / 2 | 27 | 4 | 21 / 44 |
| 2022 | 38 | 55 | 162 | 1.192 | 360 | 79 | 62 | 4,1 / 3 | 37 | 11 | 33 / 59 |
| 2023 | 56 | 93 | 2.175 | 428 | 886 | 95 | 89 | 7,1 / 6 | 70 | 29 | 77 / 115 |
| 2024 | 33 | 100 | 1.689 | 773 | 1.300 | 82 | 72 | 4,5 / 3 | 45 | 12 | 33 / 64 |
| 2025 | 18 | 100 | 288 | 3.104 | 2.000 | 67 | 44 | 2,6 / 1,5 | 17 | 11 | 15 / 34 |
| 2026 | 36 | 100 | 718 | 1.699 | 2.150 | 81 | 70 | 4,2 / 4 | 42 | 8 | 46 / 55 |
| **Tümü** | **240** | **82** | **513** | **1.053** | **845** | **81** | **68** | **4,6 / 4** | **45** | **13** | **46 / 69** |

- **Seri uzunluğu dağılımı (adet):** 0:46, 1:25, 2:16, 3:23, 4:23, 5:22, 6:15, 7:16, 8:11, 9:11, 10:10, 11:6, 12:4, 13:4, 14:3, 15:2, 16:1, 19:1, 20:1 (en uzun TRILC).
- **Gün1 getirisi:** 194/240 arz tavanda kapattı (+%9,5…+%10). 19 arz arz fiyatının altında kapattı; bunların 10'u −%5 ile −%10 arasında. Seri içindeki tavan günleri büyük ölçüde kilitli (min=max): arz başına ortalama %71, gün ağırlıklı %76 (1.099 günün 840'ı).
- **Seri, arz büyüklüğü ve başvuran sayısıyla ilişkili:**
  - Yıl içi büyüklük tercili küçük / orta / büyük: medyan seri 5,5 / 4 / 1,5; gün1 tavan %96 / %85 / %61.
  - Başvuran sayısı ile seri arasındaki korelasyon: corr(log kişi, seri) = 0,28.
  - 2024'ten sonra büyük ve fiyat istikrarlı arzlar arttı (VEYAS 10,5 mlr TL; gün1 −%0,1).

---

## 3. Katılımcı getirisi (arz fiyatından, bedelsiz düzeltmeli)

| Satış kuralı | n | Ort. % | Medyan % | t_küme | İsabet % | p5 | p95 |
|---|---|---|---|---|---|---|---|
| Gün1 kapanış | 240 | 7,9 | 10,0 | 22,6 | 90 | −2,5 | 10,0 |
| **Seri bitince E günü AOF** | 240 | **66,6** | **45,4** | 8,0 | 91 | −2,2 | 223,5 |
| E kapanış | 240 | 60,5 | 38,2 | 7,5 | 88 | −2,5 | 199,3 |
| E+21 kapanış | 240 | 64,3 | 33,6 | 8,2 | 75 | −26,8 | 274,7 |
| E+63 kapanış | 233 | 85,3 | 42,9 | 7,2 | 79 | −27,4 | 365,4 |
| E+126 kapanış | 219 | 126,8 | 68,0 | 7,6 | 84 | −21,7 | 487,3 |
| E+250 kapanış | 200 | 188,4 | 95,0 | 7,0 | 86 | −21,3 | 905,4 |

Bu satırlar ham TL getirisi; piyasa ve enflasyon düşülmedi. E+250 yüksek görünüyor çünkü 2020–23'te BIST de TL bazında çok yükseldi. Piyasaya göre durum bölüm 4'te.

- **E günü:** AOF kapanıştan medyan %3,3 yukarıda. E günü genelde tavandan açılıp satılıyor: medyan günlük getiri −%6,2 ve E'lerin %37'si taban kapanış. Bu yüzden "kuyruk bozulunca sat" kuralı, kapanışı beklemekten iyi. AOF satışı ex-post tepeye (medyan %46) çok yakın.
- **2024–26:** E AOF'ta medyan **+%30**, ortalama +%51. Arzların %10'unda E AOF bile arz fiyatının altında.
- **Yıllara göre medyan (E AOF):** 2020 %124, 2021 %18, 2022 %27, 2023 %82, 2024 %30, 2025 %11, 2026 %48.
- **Kırılımlar (E AOF medyanı):**
  - Büyüklük: küçük %69, orta %41, büyük %16.
  - Başvuran sayısı tercili: az %39, orta %36, çok %55.
  - Fiyat istikrarı: var %52, yok %39.

### 3b. Tek hesapla yıllık TL kâr (gerçekçi katılım)

Varsayımlar:
- Her eşit dağıtımlı arza bir hesapla katılım.
- Alınan tutar = bireysel lot / bireysel kişi × fiyat, en çok 20 bin TL (yalnız düşük talepli SELVA'da bağlıyor).
- Satışta %0,2 maliyet. Rakamlar nominal TL.

| Yıl | Eşit arz | Alınan toplam TL | Alınan medyan TL/arz | Kâr: gün1 sat | **Kâr: seri bitince (E AOF)** | Kâr: E+21 | Kâr: E+63 | Arz başı medyan kâr (E AOF) |
|---|---|---|---|---|---|---|---|---|
| 2020 | 3 | 1.505 | 514 | 147 | 2.175 | 2.329 | 2.722 | 807 |
| 2021 | 33 | 97.472 | 1.378 | 5.206 | 40.347 | 64.621 | 81.723 | 277 |
| 2022 | 21 | 40.200 | 909 | 3.078 | 21.450 | 35.580 | 64.799 | 247 |
| 2023 | 52 | 27.058 | 404 | 2.229 | **26.751** | 27.033 | 35.391 | 245 |
| 2024 | 33 | 33.995 | 773 | 2.116 | **10.467** | 5.533 | 4.894 | 293 |
| 2025 | 18 | 66.254 | 3.104 | 2.736 | **13.459** | 13.608 | 46.428* | 307 |
| 2026 (Kasım'a kadar) | 36 | 70.141 | 1.699 | 3.251 | **23.774** | 16.115 | 4.771** | 449 |

\* 2025'te E+63 kârını VSNMD (+%578 BH63) ve DSTKF sürüklüyor.
\** 2026'da pencere dolmayan arzlar toplama girmiyor.

Yorum:
- 2023–2026'da hesap başına yıllık **10–27 bin TL**. Bu, 1 mn TL'lik bir portföyün %1–3'ü kadar. Aile hesaplarıyla (her kişi ayrı hesap) doğrusal artar.
- Talep sırasında 2–3 iş günü bloke olan tutar (eşit dağıtımda talep > tahsis) para piyasası fonu teminatıyla verilirse faiz kaybı neredeyse sıfır.
- Döner bir 30–50 bin TL'lik başvuru bütçesine göre getiri TL eşiğinin üstünde. Ancak mutlak tutar küçük ve ölçeklenmiyor: eşit dağıtımda daha fazla para daha fazla lot getirmiyor.
- Gün1'de satmak kârın ~%10'unu bırakır. Seriyi sonuna kadar tutup E'de satmak en iyi kural. E+21/E+63'e kadar tutmak 2024 ve 2026'da kârı düşürdü.

---

## 4. Seri sonrası getiriler (asıl soru: "tavan bozunca al")

Giriş E kapanışı. 240 arz, 2020–2026.

| Ölçü | n | Ort. % | Medyan % | t | t_küme | İsabet % | p5 | p95 |
|---|---|---|---|---|---|---|---|---|
| R5 ham | 240 | −3,1 | −6,4 | −2,4 | −2,0 | 33 | −29,0 | 38,5 |
| **BH5** | 240 | **−3,7** | **−6,5** | −2,9 | **−2,5** | 33 | −28,1 | 40,2 |
| CAR5 | 240 | −4,7 | −6,2 | −3,8 | −3,1 | 34 | −31,8 | 34,9 |
| CARb5 | 240 | −4,3 | −5,0 | −3,5 | −2,9 | 33 | −31,4 | 35,3 |
| BH21 | 240 | −0,4 | **−11,2** | −0,1 | −0,1 | 36 | −40,2 | 77,6 |
| CAR21 | 240 | −3,9 | −10,6 | −1,8 | −1,5 | 38 | −46,3 | 60,7 |
| CARb21 | 240 | −2,6 | −8,8 | −1,2 | −1,0 | 40 | −45,8 | 61,3 |
| BH21 winsor %2,5 | 240 | −2,0 | −11,2 | −0,9 | −0,7 | 36 | | |
| BH63 | 233 | +9,5 | −6,5 | 2,0 | 1,5 | 42 | −52,7 | 126,0 |
| CAR63 | 233 | +1,9 | −3,1 | 0,6 | 0,4 | 46 | −59,0 | 79,9 |
| CARb63 | 233 | +4,9 | 0,0 | 1,6 | 1,0 | 50 | −56,3 | 88,3 |
| BH126 | 219 | +15,5 | −15,8 | 2,2 | 1,8 | 39 | −65,6 | 172,0 |
| CARb126 | 219 | +12,4 | +0,6 | 3,3 | 2,4 | 51 | −57,5 | 113,7 |

- **Sağ kuyruk:** BH63 ortalaması 10 hisseden geliyor (VSNMD +578%, HKTM +360%, KONTR +271%, EMPAE +257%, DSTKF +250%, PENTA +201%…). En iyi 10 çıkarılınca BH63 ortalaması **−%1,5**.
- Medyan her ufukta negatif. İsabet %33–42. Bu bir "lotarya" dağılımı: çoğu hisse geri veriyor, birkaç hisse katlıyor. Önceden seçmeyi sağlayan bir ölçü bulamadım (aşağıdaki kırılımlar).

**Alternatif girişler (BH, %):**

| Giriş | BH5 ort / medyan | BH21 ort / medyan | BH63 ort / medyan |
|---|---|---|---|
| E kapanış | −3,7 / −6,5 | −0,4 / −11,2 | +9,5 / −6,5 |
| E AOF (kuyruk bozulurken al) | −7,2 / −10,9 (t_küme −4,8) | −3,8 / −14,3 | +5,6 / −10,9 |
| E+1 kapanış | −0,5 / −4,3 | +2,3 / −6,0 | +12,6 / −3,2 (t_küme 2,0) |

E+1'de kilitli tavan yalnız 2 vakada var (alış dolmuyor). Bu iki vaka çıkarılınca E+1 BH21 ortalaması +%0,7, medyanı −%6,4.

**Takvim-zamanı portföyü.** Her arz için al, h gün tut, eşit ağırlık, 25 bp maliyet, boşta nakit = 0. Örtüşme ve kümelenme bu yöntemle çözülüyor.

| Giriş, h, örnek | Aktif gün | Ort. pozisyon | Yıllık (aktif günler) | XU100 aynı günler | Fark bp/gün (t) | Sharpe | MaxDD |
|---|---|---|---|---|---|---|---|
| E kap, 5, tümü | 714 | 1,7 | **−%89,9** | +%36,4 | −88,6 (−4,1) | −2,1 | −%99,9 |
| E kap, 21, tümü | 1.242 | 4,1 | **−%37,4** | +%36,9 | −23,9 (−2,0) | −0,4 | −%95,4 |
| E kap, 21, 2024–26 | 480 | 3,8 | −%72,3 | +%0,2 | −43,1 (−2,3) | −1,6 | −%91,6 |
| E kap, 63, tümü | 1.510 | 9,9 | +%18,1 | +%40,8 | −3,7 (−0,5) | 0,6 | −%79,7 |
| E kap, 63, 2024–26 | 592 | 9,1 | −%37,4 | −%1,7 | −13,5 (−1,0) | −0,6 | −%79,7 |
| E+1 kap, 63, tümü | 1.509 | 9,9 | +%32,3 | +%41,7 | +0,4 (0,1) | 0,8 | −%76,5 |
| E+1 kap, 126, tümü | 1.578 | 18,4 | +%41,1 | +%43,2 | +1,4 (0,2) | 1,0 | −%79,5 |

Sonuç: Seri bitince almak, en iyi durumda XU100 kadar getiriyor ve %75–80 düşüş yaşatıyor. Kısa ufukta açıkça zarar ediyor. TL eşiğini (%36–40) geçmiyor.

### 4b. Kırılımlar (E kapanış girişi, BH, %)

| Kırılım | BH21 ort / medyan (t_küme) | BH63 ort / medyan (t_küme) | n |
|---|---|---|---|
| 2020–23 | +0,5 / −7,7 (0,1) | +11,4 / −3,7 (1,7) | 153 |
| **2024–26** | −2,1 / **−17,3** (−0,4), isabet %25 | +5,8 / −17,4 (0,4) | 87 / 80 |
| Yıl 2024 | −12,3 / −18,8 (−2,4) | −14,1 / −19,1 (−1,4) | 33 |
| Yıl 2025 | +4,7 / −13,5 (0,3) | +45,1 / +7,9 (1,0) | 18 |
| Yıl 2026 | +3,9 / −17,4 (0,6) | +4,2 / −18,4 (0,2) | 36 / 29 |
| Seri 0 | −4,8 / −12,8 (−1,0) | +13,0 / −4,3 (1,7) | 46 |
| Seri 1–2 | +1,6 / −7,1 | +10,0 / +7,8 | 41 |
| Seri 3–5 | +7,4 / −8,4 | +16,8 / −2,6 | 68 |
| Seri 6–10 | −6,0 / −13,1 (−1,4) | +8,1 / −21,4 | 63 |
| **Seri 11+** | −3,2 / −13,2 | **−15,7 / −28,6** (−1,6), isabet %27 | 22 |
| Büyüklük küçük / orta / büyük | +8,9 / −6,6 · −8,7 / −12,6 · −1,9 / −13,2 | +19,9 / −2,7 · +4,5 / −11,1 · +3,3 / −11,5 | ~80 |
| Başvuran az / orta / çok | +7,1 / −3,0 · −8,2 / −15,6 · −0,5 / −9,3 | +22,2 / +0,4 · +3,5 / −3,9 · +3,2 / **−15,5** | ~80 |
| Eşit / Oransal | +1,4 / −11,2 · −8,5 / −11,0 (−2,1) | +11,2 / −7,7 · +2,6 / −4,8 | 196 / 43 |
| Fiyat istikrarı var | **−8,3 / −17,4 (−2,2)** | +6,3 / −12,1 | 103 |
| Fiyat istikrarı yok | +5,5 / −8,2 | +11,7 / −4,6 | 137 |

Okuma:
- En kötü sonrası; uzun seri (6+), çok başvuran, fiyat istikrarlı ve 2024–26 arzlarında görülüyor. Bunlar ilgi gören ve yüksek fiyatlanan arzlar, yani aşırı tepki örüntüsü.
- Az başvuranlı ve küçük arzlarda medyan ~0. Ortalama sağ kuyruk yüzünden pozitif, ama t_küme 1,7–1,8 (anlamlı değil).
- Hiçbir kırılımda medyanı belirgin pozitif ve t_küme > 2 olan bir "alış" kümesi yok.

---

## 5. Gün1 ve seri içi alış (ikincil piyasa)

**Gün1 kapanışından al (BH, %):**

| Alt küme | n | BH5 ort / medyan | BH21 ort / medyan | BH63 ort / medyan |
|---|---|---|---|---|
| Tümü (kâğıt üstü) | 240 | +25,9 / +26,3 | +47,7 / +20,6 | +59,6 / +24,6 |
| **Kilitli tavan: alış DOLMAZ** | 161 | +38,2 / +52,7 | +69,5 / +39,5 | +81,9 / +38,4 |
| **Dolabilir (kilitsiz)** | 79 | **+0,7 / −2,8** | **+3,5 / −9,8** | +12,8 / −3,7 (t_küme 1,9) |

"Halka arz hissesi ilk gün alınır" inancının kaynağı, alınamayan kilitli günler. Dolabilir günlerde fazla getiri yok.

**Seri içi.**
- 840 kilitli tavan gününün ertesinde %90 yine tavan. Ama bu günlerde alış dolmuyor.
- 259 kilitsiz tavan kapanışının ertesinde ortalama +%3,6 (t_küme 7,0). Bu sonuç kapanışın tavan olacağını önceden bildiğimizi varsayıyor (ileriye bakış). Ayrıca kapanış müzayedesinde tavan fiyatından alış ancak kısmen doluyor.
- Uygulanabilir sürüm: Önceki kapanış tavan iken gün içinde kuyruk bozulursa o günün AOF'undan al (414 gün; %44'ü seriyi bitiren E günü).
  - Aynı gün kapanışa kadar **−%0,8** (t_küme −4,6).
  - Ertesi gün +%0,2.
  - +5 gün ortalama +%3,2, medyan −%2,2 (t_küme 1,6).
  - +21 gün ortalama +%8,7, medyan −%5,6 (t_küme 1,7).
  - Sonuç: tutarlı bir avantaj yok; sağ kuyruk yine ortalamayı şişiriyor.

---

## 6. "Seri bitince açığa sat / uzak dur"

Bu bölüm bölüm 4'ün tersi. E günü kilitli taban olan 10 arz çıkarıldı (bu günlerde satış dolmuyor).

| Ölçü | n | Ort. % | Medyan % | t_küme | İsabet % | p5 |
|---|---|---|---|---|---|---|
| −BH5 | 230 | +3,8 | +5,9 | 2,5 | 67 | −37,9 |
| **−BH5 net (−25 bp)** | 230 | **+3,5** | +5,7 | **2,4** | 67 | −38,2 |
| −BH5, 2021 / 2022 / 2023 / 2024 / 2025 / 2026 | 52 / 38 / 53 / 30 / 16 / 34 | +2,0 / +2,8 / +7,4 / +5,3 / **−5,3** / +5,7 | | 0,5 / 2,1 / 2,6 / 1,5 / −0,9 / 1,4 | | |
| −BH5, 2024–26 | 80 | +3,4 | +5,7 | **1,2** | 62 | −38,9 |
| −BH21 | 240 | +0,4 | +11,2 | 0,1 | 64 | −77,6 |
| −BH63 | 233 | **−9,5** | +6,5 | −1,5 | 58 | −126 |
| −BH21 (seri ≥5) | 107 | +5,1 | +11,6 | 1,5 | 65 | −66,6 |

- **İstatistik:** 5 günlük devam eden düşüş tüm örneklemde anlamlı. Ancak 2024–26'da anlamlı değil ve 2025'te ters döndü.
- **Uzun ufuk:** 63 gün ve üstünde açık pozisyon ortalamada zarar ediyor (sağ kuyruk). Dağılımın dişi tarafında −%38 ile −%126 arası kayıplar var.
- **Uygulanabilirlik:**
  - Yeni arz paylarında ödünç pay piyasası pratikte yok.
  - Pay vadelisi yok (VİOP'un 47 sözleşmesi arasında seri dönemindeki bir arz yok).
  - Bu hisseler sık sık tedbir, brüt takas veya tek fiyat uygulamasına giriyor.
  - Dönem dönem genel açığa satış kısıtları da oluyor.
- **Uygulanabilir çıkarım** iki tanedir:
  1. Katılımcı payını E gününde (tavan bozulurken) satmalı. Tutmak sonraki 5 günde ortalama %3,7, medyanda %6,5 kaybettiriyor.
  2. İkincil piyasada seri sonrası "dip" alımından kaçınmak gerekir.

---

## 7. Satmama taahhüdü (lock-up) bitişi

- L = ilk işlem + süre.
- Süre 102 arzda sayfada yazılı (çoğu 1 yıl; ayrıca 180 gün, 18 ay, 2 yıl var). Diğer 98 arz için 365 gün varsayıldı.
- Türkiye'deki taahhüt çoğunlukla "arz fiyatının altında satmama" biçiminde. Fiyat arzın çok üstündeyse arz baskısı beklenebilir.

| Pencere | n | CAR ort / medyan % | t_küme | CARb ort % (t_küme) | İsabet % |
|---|---|---|---|---|---|
| [−10,−1] | 201 | +0,5 / +0,1 | 0,4 | +1,5 (1,1) | 50 |
| [0,+5] | 200 | 0,0 / 0,0 | 0,0 | +0,5 (0,6) | 50 |
| [0,+20] | 200 | 0,0 / −0,4 | 0,0 | +1,7 (1,2) | 48 |
| [−20,+20] | 200 | +0,5 / −0,5 | 0,2 | +4,2 (1,7) | 48 |
| [0,+20], fiyat > 2×arz | 96 | −2,2 / −1,6 | −0,9 | | 46 |
| [0,+20], süre yazılı | 102 | −1,3 / −1,4 | −0,6 | | 46 |
| [0,+20], 2024–26 | 100 | −1,2 / −1,4 | −0,5 | | 46 |

Lock-up bitişinde işlenebilir bir etki yok. En güçlü alt kümede (fiyat > 2×arz) bile CAR[0,+20] −%2,2 ve t −0,9.

---

## 8. Uyarılar ve sınırlamalar

1. **Liste kaynağı tek:** halkarz.com. Alanlar WebFetch özetleyicisiyle sayfadan satır satır alındı, yazım hatası riski var. Fiyatların hepsi gün1 limit testinden geçti. Kişi ve lot alanlarında 2 düzeltme yapıldı (ATAKP lot, GWIND toplam kişi). Bireysel kişi sayısı ve lot sayfada yazıldığı gibi. Oransal dağıtımda kişi başı lot ortalamadır.
2. **Kilit tespiti gün sonu min/max'a dayanıyor:** Emir defteri verisi yok. min<max olan bir tavan günü "kısmen dolabilir" sayıldı; gerçek dolum oranı bundan düşük olabilir.
3. **Hayatta kalma:** Örnekte işlemden kaldırılan hisse yok. 240 arzdan 239'u 04–05.11.2026'da veride var. TERA'nın verisi 27.10.2026'da kesiliyor; muhtemelen işlem durdurma. Bu durum ölçüm pencerelerini etkilemiyor.
4. **Pencereler:** 2026 arzlarının E+63/E+126 pencereleri dolmadı (n düşüyor). Yıllık TL tabloları nominal; 2021 ile 2026 TL'si karşılaştırılamaz (TÜFE).
5. **Beta tahmini:** E+1..E+250 penceresinden; ölçüm penceresiyle örtüşüyor. Alfa çıkarılmadı. CARb yalnız sağlamlık kontrolü.
6. **Dönem etkisi:** 2023'teki uzun seriler (%70'i ≥5 gün) özel bir dönemdi: negatif reel faiz ve 2–4 milyon başvuran. 2024–26'da seriler kısaldı, büyük arzlar ve fiyat istikrarı arttı, seri sonrası düşüş derinleşti (BH21 medyan −%17).

---

## 9. Dosyalar

- **Kod** (`/home/user/Xxxx/raporlar/2026-11-06_kazanc_stratejileri/hesaplar/olay_halka_arz/`):
  - `common.py`: yollar, nazik HTTP
  - `a01_liste_indir.py`: halkarz arşiv sayfaları (403 sonrası durduruldu)
  - `a02_fiyat_indir.py`: İş Yatırım ChartData ve Hisse Tekil
  - `a03_tablo.py`: arz tablosu, nihai fiyat düzeltmeleri, hariç listesi
  - `a04_olay.py`: tavan/kilit/seri, katılımcı, seri sonrası, lock-up ölçüleri ve düzeltme kontrolü
  - `a05_tablolar.py`: bütün tablolar ve takvim-zamanı portföyü
- **Veri ve çıktılar** (repoda değil): `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/halka_arz/`
  - `raw_web/liste_yillar.txt`, `raw_web/detay_satirlar.txt`
  - `px/cd_*.parquet`, `px/ht_*.parquet`
  - `out/ipo_tablo.csv`, `out/ipo_olay.csv` (arz başına bütün ölçüler)
  - `out/seri_ici_gunler.csv`, `out/duzeltme_kontrol.csv`
  - `out/tablolar.md` (tam ızgara)
