# v_dalga: dalga_bist ve dalga_abd raporlarının çekişmeli denetimi

Denetim tarihi: 06.11.2026. Denetlenen dosyalar:
- `ajanlar/dalga_bist.md` ve `hesaplar/dalga_bist/`
- `ajanlar/dalga_abd.md` ve `hesaplar/dalga_abd/`

Yöntem:
- Kodları satır satır okudum: sinyal zamanlaması, dalga etiketi, maliyet, evren ve ızgara.
- Başlık sayılarını rapor kodunu çağırmadan, kendi kodumla önbellekteki ham veriden yeniden hesapladım. Kod: `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/audit_dalga/` (`a1_bist.py`, `a2_sektor.py`, `a4_guncel.py`, `a5_rebal.py`, `b1_abd.py`).
- Literatür sayılarını makale metinleri (GSY NBER WP, Wiest 2023 derlemesi, Ben-David ve diğerleri NBER WP 28369) ve web aramasıyla kontrol ettim.
- Varsayılan tutum şüphecilik. Yeni veri çekmedim; yalnız önbelleği okudum.

Etiketler: **DOĞRU** = bağımsız hesapla ±0,5 puan içinde tutuyor. **KISMEN** = sayı tutuyor ama yorum ya da etiket yanıltıcı, veya sayı kısmen tutuyor. **YANLIŞ** = sayı ya da iddia tutmuyor. **DOĞRULANAMADI** = kaynağa erişilemedi.

---

## 1. Özet karar

| # | İddia | Rapor | Denetim | Karar |
|---|---|---|---|---|
| B1 | EW 24 küme CAGR 2012-26 / XU100 / rf | %36,8 / %23,3 / %17,6 | %36,8 / %23,3 / %17,6 | DOĞRU |
| B2 | 2024-26: rf %43,1; EW %10,6; XU100 %15,9; 456 kuralın **0**'ı rf'yi geçti | aynı | aynı; en iyi kural %34,8 | DOĞRU |
| B3 | A (12 ay RS, ilk 3, aylık) 2012-26 %54,7; 2024-26 %12,7 | aynı | %54,1; %12,7. EW'ye göre aylık fark t=3,1 | DOĞRU, ama örneklem içi en iyi |
| B4 | 12 ay ailesi medyanı %41,7, EW'ye göre +3,6 puan | aynı | 32 sepet yapılandırmasında medyan %41,7, EW'yi yenen pay %78 | DOĞRU |
| B5 | Hayatta kalan yanlılığı olmayan sektör endekslerinde EW'ye göre +3,0 puan | aile medyanı | Tek yapılandırma (L252, K3, aylık): +6,1 puan, **t=1,89** | KISMEN: yön doğru, istatistik zayıf |
| B6 | Maliyet 2 katında 12 ay rotasyon %35,2 | özet bunu %41,7'nin yanında veriyor | %35,2, lider sürüm dahil tüm r252'lerin medyanı (taban %38,4). Sepet medyanı %41,7 → %40,0. A %54,7 → %52,4 | KISMEN: etiket karışık, maliyet etkisi aslında küçük (-1,7 ile -3,2 puan) |
| B7 | Aylık IC 12 ay 0,065, t=3,2 | aynı | kod doğru. 4 bakış süresi içinden seçildi; Bonferroni'yi geçer | DOĞRU |
| B8 | İleri test sıra korelasyonu -0,12 | aynı | -0,119 | DOĞRU |
| B9 | 167 dalga, medyan +%55, 101 gün; dalga günleri %31, göreli kazancın tamamı | aynı | CSV ile tutarlı. "Kazancın tamamı dalga günlerinde" ise **tanım gereği doğru** (zigzag yükseliş bacakları) | DOĞRU ama bilgi taşımıyor |
| B10 | Negatif reel faizde dalga patlıyor (2019-20: 42, 2022-23: 42) | aynı | Sayılar doğru. Uygun küme başına: 2019 0,86, **2021 0,42** (en negatif reel faiz yılı), 2024 0,54. 2019'un büyük bölümünde ex post reel faiz pozitifti | KISMEN / zayıf |
| B11 | Örnek dalgalar (Banka +%74/105/63, Koza +%88/126/112, Rafineri +%56, XU100 -%27) | aynı | `dalgalar_taban.csv` ile birebir. Hepsi ex post dip-tepe ölçüsü | DOĞRU (ex post) |
| B12 | Güncel tablo: XU100 11.333, 200 GHO 13.572, 50 GHO 12.691; 12 ay ilk 3 RAFİNERİ/HOLDİNG/KOZA; BANKA/HAVACILIK 126 g RS zirvesi; beta, korelasyonlar | aynı | Hepsi birebir (RAFİNERİ beta 0,54; korelasyon 0,77/0,77/0,79; fazla getiri -0,42/-0,31) | DOĞRU |
| B13 | "Ağustos tepesinden -%25" | | 252 günlük zirve **11.05.2026** (15.134), -%25,1. Ağustos zirvesinden (14.642) -%22,6. 31.08 → 30.10: -%24,9 | KISMEN |
| U1 | B_L12s0_k3: 1930+ %16,7 / piyasa %10,1, t=4,4; 2000+ %14,0 / %8,5, t=1,8; 2015+ %15,5 / %13,5, t=0,6; MaxDD -%66 | aynı | %16,7 / %10,1 (t 4,38); %14,0 / %8,5 (t 1,77); %15,5 / %13,5 (t 0,61); -%65,8 | DOĞRU |
| U2 | Mutlak filtre: DD -%51, getiri aynı. Piyasa filtresi 2015+ %3,4 | aynı | %17,0, DD -%51,2. Piyasa filtresiyle 2015+ %3,5 | DOĞRU |
| U3 | "140 rotasyon kuralının medyanı (k≥3): %12,6 / %11,5 / %13,5" | özet | Bu, yalnız **B-düz** ailesinin (21 kural) medyanı. k≥3 olan 105 kuralın tamamında %12,0 / %11,0 / **%12,2**, yani 2015+ piyasanın (%13,5) altında | KISMEN (yanlış etiket) |
| U4 | 2015+ fark istatistiksel olarak sıfır | aynı | Nokta tahmini +3,4 puan/yıl, %90 blok bootstrap aralığı [-7,2; +15,8]. "Sıfır" değil, **bilgi yok** | KISMEN |
| U5 | 1930+ kenar t=4,4 | | 1930-59'da tutulan sektör-ayların %67'si <10 firmalı, %47'si <5 firmalı "sektör". ≥10 firma şartıyla: 1930+ %15,1 (t 3,96), **2000+ %11,5 (+4,3 puan, t 1,38)**, 2015+ %14,3 (t 0,5) | KISMEN: 2000 sonrası kenar abartılı |
| U6 | 343 dalga, medyan +%91 / 22 ay; tepeden 12 ay sonra RS -%20, %89,5'i geride | aynı | Pickle ile tutarlı. Tepe sonrası geri verme zigzag tanımının (%20 dönüş şartı) mekanik sonucu; raporda bu not yok | DOĞRU ama totolojik |
| U7 | Swing (4-13 hafta): 2015 sonrası tüm varyantlar göreli negatif | aynı | 40 varyantın 40'ı negatif, medyan -%0,95, en iyisi -%0,07 | DOĞRU |
| U8 | GSY replikasyonu: 50 olay, çöküş %41,7 | aynı | 50 olay, 48 tam gözlem, %41,7 | DOĞRU |
| U9 | En güçlü ayırıcı: piyasanın 24 aylık koşusu (t=2,66) | aynı | 10 özellik test edildi; Bonferroni eşiği t≈2,8, geçmiyor. Tablo ayrıca "hemen T-bill'e geç"in (+%9,7, kayıp oranı %0) tutmayı ve stopları domine ettiğini gösteriyor; özet bunu söylemiyor | KISMEN |
| U10 | 5.11.2026 SOX -%10/-%12, MU -%17, SNDK -%22 | [W] | Çoklu kaynak: SOX ~-%12, MU -%17,5, SNDK -%22. "Mart 2020'den beri en kötü" yalnız bir gün içi kaynakta var; Reuters tabanlı haber "Nisan 2025'ten beri en büyük" diyor | KISMEN |

---

## 2. dalga_bist: ayrıntılı bulgular

### 2.1 İleriye bakma (look-ahead)
- **Sinyal zamanlaması temiz.** `motor.getiri_seri` ağırlıkları 1+L gün kaydırıyor: sinyal t, işlem t+1 kapanışı, getiri t+2. EW kıyası da 2 gün kaydırılmış.
- **Rotasyon skoru:** `Rel_t / Rel_{t-252}`; yalnız ≤t bilgisi kullanıyor. Kendi kodumla, motoru kullanmadan %54,1 buldum; rapor %54,7. Fark uygunluk kuralından geliyor: bende 252 gün, raporda 130 gün.
- **Dalga etiketi ex post**, ama yalnız değerlendirmede kullanılıyor; kurallara girmiyor. Bu doğru.
- **Bilgi taşımayan iddialar:**
  - "Göreli kazancın tamamı dalga günlerinde": zigzag yükseliş bacağı seçtiği için tanım gereği doğru.
  - "Dalga sonrası -%10/-%11 geri verme": tepe sonrası ≥%15 dönüş şartından geliyor. Rapor bunu kısmen kabul ediyor.
- **Küçük risk:** `motor.Veri.Rel`, uygun olmayan dönemde küme endeksini düz tutuyor (`nan_to_num`). Yeni uygun olmuş bir kümenin 12 ay skoru, uygunluk öncesi kısımda XU100'ün ters hareketini içeriyor. Bu ileriye bakma değil; sonuca etkisi ~0,6 puan.

### 2.2 Geriye dönük seçim (hindsight) ve hayatta kalan yanlılığı

Küme üyeleri bugün likit olan hisselerden seçilmiş; 133 üyenin 31'i 2012 sonrası halka arz. Dört tema kümesi bugün bilinen kazananların etrafında kurulmuş: KOZA_ALTIN, SAVUNMA (SDTTR, ALTNY, ONRYT), ELK_EKİPMAN (KONTR, ASTOR, EUPWR) ve YENİLENEBİLİR. Bu yanlılığı ölçtüm (A kuralı, maliyet %0,25):

| Evren | A CAGR | EW CAGR | Fark (CAGR) | Aylık fark t | 2012-18 | 2019-23 | 2024-26 | A 2024-26 |
|---|---|---|---|---|---|---|---|---|
| Rapor evreni (24 küme) | 54,1% | 36,8% | +12,6 | 3,11 | +15,0 | +19,0 | +2,4 | 12,7% |
| 4 tema kümesi hariç (20 küme) | 50,0% | 35,7% | +10,5 | 2,96 | +11,4 | +17,0 | +1,3 | 12,6% |
| Yalnız 2012 öncesi listelenen üyeler | 48,5% | 36,9% | +8,4 | 2,14 | +16,5 | **+4,4** | +1,5 | 14,2% |
| Yalnız 2012 öncesi listelenenler, tema hariç | 46,9% | 35,8% | +8,2 | 2,29 | +11,2 | +8,8 | +4,0 | 15,1% |
| BIST sektör endeksleri (20; XFINK/XSPOR hariç) | 36,4% | 28,5% | +6,1 | **1,89** | +8,9 | +12,4 | -1,0 | 9,7% |
| BIST sektör endeksleri (22) | 37,2% | 28,1% | +7,1 | 1,93 | +8,3 | +3,7 | +24,9 | 37,1% (XFINK etkisi) |
| A, maliyet %0,50 | 51,8% | 36,8% | +11,0 | 2,78 | | | | 10,6% |
| A, K=5 | 49,8% | 36,8% | +9,5 | 3,37 | | | | 16,8% |

Dönem sütunları, aylık aritmetik farkın yıllık karşılığıdır (puan).

- **Jackknife:** kümeleri tek tek çıkarınca A'nın EW'ye farkı +11,2 ile +14,7 puan arasında kalıyor. Tek bir kümeye bağlı değil.
- **Sonuç:**
  - 12 ay RS rotasyonunun EW'yi geçmesi seçim yanlılığından tümüyle kaynaklanmıyor.
  - Büyüklüğü şişkin: örneklem içi +12,6 puan. Yanlılıksız evrende +6 puan ve t≈1,9, yani sınırda anlamlı.
  - 2019-23 üstünlüğü büyük ölçüde sonradan halka arz edilen hayatta kalanlardan geliyor: +19 puandan +4,4 puana düşüyor.
  - Raporun "+3-5 puan, daha fazlası beklenmemeli" tahmini makul, hatta temkinli.
- **Ay içi al-tut ile günlük yeniden dengeleme** (aylık çerçeve): EW %36,6 → %37,5, A %53,6 → %54,4. Günlük dengeleme getiriyi şişirmiyor. Ancak A'nın 2024-26 getirisi %10,6 → %3,2 oynuyor; kısa pencere gürültülü.
- **Veri hijyeni:** XBANK, XFINK, XILTM, XSPOR ve XUMAL serileri 02.07.2010 → 03.01.2011 arasında 1/100 ölçekte (-%99 / +%10.000 günleri). `veri.panel` içindeki |r|>%35 temizliği yalnız hisselere uygulanıyor, endekslere değil. Bu dönem backtest başlangıcından ve ilk 12 aylık bakıştan önce kalıyor; temizleyince sonuç değişmiyor (CAGR %36,36'ya karşı %36,33). Yine de düzeltilmeli.

### 2.3 Parametre madenciliği ve maliyet
- **Izgara:** 456 küme ve 192 sektör yapılandırması. Rapor medyanları veriyor ve ileri test yapmış (-0,12). Bu iyi bir uygulama.
- **12 ay ailesi tanı testinden sonra eklenmiş.** Ancak literatürün standart bakış süresi; IC 4 bakış süresi arasında Bonferroni'yi geçiyor (t=3,2). Madencilik riski orta.
- **"A %54,7"** ailenin en iyisi; medyan %41,7. Raporda açıkça yazıyor.
- **Maliyet %0,25/yön** likit üyeler için makul. Küçük üyelerde (RAYSG, JANTS, KONTR, SMRTG) makas daha geniş. Küme içi dengeleme maliyeti yok.
- **Maliyet iki katına çıkınca:** A için -2,3 puan, sepet medyanı için -1,7 puan. Özetteki "%41,7 → %35,2" yan yana koyuşu yanlış: %35,2, lider sürüm dahil medyanın (%38,4) karşılığı.
- **TL rf:** elle kurulmuş adım fonksiyonu.
  - 2026'da 12.06'dan itibaren %36 varsayılmış. Haber kaynaklarına göre TCMB faizi 22.10.2026'da %37'den %36'ya indirdi. Fark küçük.
  - 2021-23 ve 2024'te mevduat ve para piyasası getirileri politika faizinin üstündeydi. Bu yüzden "rf'yi geçemedi" sonucu, gerçek engel karşısında daha da güçlü.
- **Yanlış başlangıç tanımı cömert:** işlem herhangi bir dalganın herhangi bir kısmına değiyorsa "doğru" sayılıyor. ABD raporunda ise giriş [dip, tepe) içinde olmalı. BIST'in %47'si ile ABD'nin %64-76'sı bu yüzden karşılaştırılamaz.

### 2.4 VİOP hedge'li sürüm
- Formül: getiri + maruziyet × (rf - %3 temettü - XU100) - %0,6/yıl. Vadelinin tam politika faizini taşıdığını varsayıyor.
- Modellenmeyenler:
  - XU030 vadeli bazının gerçekleşen örtük faizi
  - XU030/XU100 farkı
  - Teminat nakdinin getirisi
- Sonuç değişmiyor: 2024-26'da %33'e karşı rf %43.

---

## 3. dalga_abd: ayrıntılı bulgular

### 3.1 İleriye bakma ve zamanlama
- **Zamanlama temiz.**
  - Aylık rotasyon: `mom` t ayı sonuna kadar olan getirilerle hesaplanıyor, ağırlık t+1 getirisini alıyor.
  - Swing kuralları sinyali izleyen günün kapanışında giriyor.
  - GSY özellikleri karar anında biliniyor: BE/ME Temmuz kuralına uyuyor, volatilite t'ye kadar.
- **French/CRSP verisinde hayatta kalan yanlılığı yok.** Bu BIST'e göre büyük avantaj.
- **Dalga sonrası istatistikler büyük ölçüde mekanik:** tepeden 12 ay sonra -%20, %89,5'i geride, %62'si yarısını geri veriyor. Zigzag tepesi, ≥%20 RS dönüşüyle teyit edilen ex post maksimum.
- **"Zamanında sinyal %82-91" cömert bir ölçü:** tepeden bir ay önceki sinyal de "isabet" sayılıyor. Gecikme medyanı, dalganın %27-35'i gerçekleştikten sonra.

### 3.2 Parametre madenciliği ve ticarete uygunluk
- **Başlık kuralı ızgaranın en iyilerinden:** B_L12s0_k3, 1930+'da 140 kuralın 3.'sü.
- **Medyan etiketi yanlış:** k≥3 olan 105 kuralın medyanı 2015+ %12,2, yani piyasanın altında. Raporun verdiği %13,5 yalnız B-düz ailesine ait.
- **İnce "sektörler" (bkz. U5):** 1930-50'lerin "sektör momentumu" çoğu ayda 1-9 hisselik portföy demek. ≥10 firma şartıyla:
  - 1930+ kenar +5,3 puan/yıl (t 3,96) olarak kalıyor.
  - 2000+ kenar +4,3 puana ve t=1,38'e düşüyor.
  - Rapordaki "2000 sonrası ~%14" pratikte ~%11,5.
- **EW49 kıyası** (raporda "test edilmedi"): 2015+ +5,1 puan, t=0,97. Yine anlamsız.
- **Maliyet 10/25 bp makul;** ETF'lerle uygulanabilir. French sektörleri doğrudan alınıp satılamaz, rapor bunu belirtiyor.

### 3.3 Literatür kontrolü

| İddia | Kontrol | Karar |
|---|---|---|
| MG 1999: %0,43/ay (6-6), sektör düzeltilmiş hisse momentumu %0,13/ay, en güçlüsü 1-1 | Wiest (2023) metni birebir | DOĞRU (ikincil kaynak) |
| Grundy-Martin: 1 ay atlanınca %0,16/ay, anlamsız | Wiest (2023) | DOĞRU |
| Grobys-Kolari (2020): 48 sektör, 1926-2018; %0,62 / %0,57 / %0,80; korelasyon 0,14; opsiyonellik yok | Wiest (2023) | DOĞRU |
| Arnott-Clements-Kalesnik-Linnainmaa (2023, **JF**) | Yayın RFS 36(8), 2023. Clements yalnız WP'de yazar. İçerik (endüstri momentumu faktör momentumuyla açıklanıyor) doğru | KISMEN (künye) |
| HTV 2007: 34 sektörün ~14'ü | Özet yalnız "a number of industries … lead by up to two months" diyor; 14 sayısı teyit edilemedi (rapor da bunu not ediyor) | DOĞRULANAMADI |
| Cohen-Frazzini: ~%1,55/ay | Özet: "monthly alphas of over 150 basis points" | DOĞRU |
| McLean-Pontiff: -%26 / -%58 | Bilinen sayılar | DOĞRU |
| GSY: 40 olay; %53 çöküş; +%150'de %80; 1 yıl +%7 (net +%5), 2 yıl %0; çökenler tepeye ~6 ay ve +%30; 21 çöküşün 17'sinde tek ay ≤-%20; ABD'de Bonferroni'yi yalnız ivme geçiyor; devir ve satış büyümesi ayırmıyor; satış stratejisi +10 puan | NBER WP 23191 metni birebir | DOĞRU |
| Ben-David ve diğerleri (2023 RFS): -%3,1/yıl; yeni lansmanlar ~-%5/yıl; ücret 58'e karşı 35 bp | WP metni: -%3,1/yıl doğru, ücretler doğru. İlk 5 yıl "about **-6%** annually" (5 yılda ~%30; 4 faktör alfası -%6/yıl) | KISMEN (-%5 değil, ~-%6) |
| Morningstar: 15 yılda ~%9-10 hem yaşadı hem endeksi geçti | Mid-2024'e kadar 15 yılda %9 (Capital Group ve Portfolio Adviser, Morningstar'a atıfla) | DOĞRU |

### 3.4 Haber kaynaklı tema haritası
- Doğrulananlar:
  - 5.11 çip çöküşü (SOX ~-%12; MU, SNDK)
  - BIST tarafında fon krizi: XU100 30.10 kapanışı 10.759,56, önbellekteki seriyle tutarlı
- OKLO, kuantum, BTC, LMT gibi diğer kalemler tek tek denetlenmedi.
- Rapor bu rakamları [W] olarak işaretliyor ve düşük güvenilirlikli kaynakları ayırıyor. Uygun.

---

## 4. Geriye dönük seçim (hindsight) değerlendirmesi

| Risk | dalga_bist | dalga_abd |
|---|---|---|
| Evren / hayatta kalan | **Yüksek.** Üyeler bugünün likit hisseleri; 4 tema kümesi bugünün kazananları etrafında kurulu. Ölçülen etki: A'nın EW'ye farkı +12,6'dan +6/+8 puana iniyor | Yok (CRSP) |
| Dalga etiketi | Ex post; kurallarda kullanılmıyor. Doğru ayrılmış | Aynı |
| Sinyal zamanlaması | Temiz (t+1 işlem, L=0 testi var) | Temiz |
| Parametre madenciliği | Orta. Medyan ve ileri test raporlanmış; 12 ay ailesi sonradan eklenmiş | Orta. Başlık kuralı ızgaranın en iyilerinden; medyan etiketi yanlış |
| Bilgi taşımayan istatistikler | Dalga günleri ve dalga sonrası geri verme | Dalga sonrası -%20 ve geri verilen pay |
| Dönem seçimi | 2012 başlangıcı veriyle sınırlı; 2024-26 rejimi raporlanmış | Uzun örneklem; 2015+ zayıflığı açıkça raporlanmış |

---

## 5. Kullanılabilir son hükümler

1. **BIST'te 12 ay RS ile ilk 3 küme rotasyonu tek savunulabilir küme kuralı.**
   - Yanlılıktan arınmış beklentisi EW'nin yılda ~+5±5 puan üstü, MaxDD ~-%40/-%48.
   - Ama 2024-26'da hiçbir uzun küme kuralı TL rf'yi (%43) geçmedi. Mevcut rejimde (politika %36, XU100 200 GHO altında, fon krizi) bir getiri motoru değil, **küme seçme filtresi**.
2. **Olay ve kırılım kuralları EW'yi geçmiyor** (medyan -3/-6 puan). "Dalga yakalama" iddiası pratikte "kümeleri tut" getirisine yakın; kazanç birkaç büyük dalgaya bağlı.
3. **Güncel sinyaller sayısal olarak doğru.**
   - 12 ay ilk 3: RAFİNERİ, HOLDİNG, KOZA (sonraki yeniden dengeleme 30.11).
   - 126 g RS zirvesi: BANKA ve HAVACILIK.
   - Filtreli kurallar nakitte.
   - RAFİNERİ liderliği düşük betadan geliyor (0,54). Banka, holding ve havacılık tek risk bloğu.
4. **ABD'de 12 ay ilk 3 sektör rotasyonu uzun vadede gerçek, 2000 sonrası sınırda (≥10 firma evreninde t≈1,4), 2015 sonrası belirsiz.**
   - USD engelini (~%12-15) güvenilir aşmıyor.
   - Swing ufkunda sektör düzeyinde kenar yok: 2015+ 40 varyantın 40'ı negatif.
5. **GSY bayrağı:** +%100 koşuda boyut küçültme ve stop sıkılaştırma mantıklı. Ancak "piyasa 24 ay koşusu" ayırıcısı Bonferroni'yi geçmiyor. Tarihsel olarak en iyi seçenek hemen çıkmaktı.
6. **Düzeltilmesi gerekenler:**
   - BIST: endeks serilerinde ölçek temizliği; özetteki maliyet etiketi; "Ağustos tepesi" (-%22,6) ifadesi; reel faiz ve dalga iddiasının yumuşatılması.
   - ABD: "140 kural medyanı" etiketi; Arnott künyesi; Ben-David -%6; 2015+ için "sıfır" yerine "belirsiz"; dalga sonrası istatistiklerin mekanik olduğu notu.

Kaynaklar (literatür ve haber kontrolü):
- [Ben-David ve diğerleri, NBER WP 28369](https://www.nber.org/system/files/working_papers/w28369/revisions/w28369.rev2.pdf)
- [SFI özeti](https://sfi.ch/en/publications/competition-for-attention-in-the-etf-space)
- [Capital Group: tematik ETF'ler (Morningstar %9)](https://www.capitalgroup.com/advisor/ca/en/investments/exchange-traded-funds/resources/thematic-etfs--3-things.html)
- [Portfolio Adviser: Morningstar tematik raporu](https://portfolio-adviser.com/?p=311991)
- [HTV eScholarship](https://escholarship.org/content/qt6x49x543/qt6x49x543.pdf?t=krnr78)
- [Cohen-Frazzini, IDEAS](https://ideas.repec.org/a/bla/jfinan/v63y2008i4p1977-2011.html)
- [Arnott ve diğerleri, RFS 36(8)](https://econpapers.repec.org/RePEc:oup:rfinst:v:36:y:2023:i:8:p:3034-3070.)
- [Wiest 2023, FMPM](https://link.springer.com/content/pdf/10.1007/s11408-022-00417-8.pdf?pdf=button)
- [Yahoo: Micron -%17](https://finance.yahoo.com/markets/article/micron-declines-12-as-chip-sell-off-deepens-163137019.html)
- [el7/Reuters: SOX -%12,2](https://el7.ai/en/news/2026-11-05-micron-and-sk-hynix-shares-plunge-as-semiconductor-selloff-intensifies)
- [Grafa](https://grafa.com/en/news/united-states/us-semiconductor-stocks-selloff-ai-trade-unwind-november-2026)
- [Medyascope 03.11.2026](https://medyascope.tv/2026/11/03/fon-krizi-basladigindan-bu-yana-borsa-istanbulda-neler-oldu/)
- [Endeks24: fon krizinden bugüne](https://www.endeks24.com/borsa-istanbul-neden-dusuyor-fon-krizinden-bugune-tablo)
- [Paratic](https://paratic.com/borsada-tarihe-gecen-dususler-fon-krizi-listeye-girdi/)
