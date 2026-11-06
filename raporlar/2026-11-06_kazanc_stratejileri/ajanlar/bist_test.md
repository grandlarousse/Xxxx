# BIST swing stratejileri: kendi backtestlerimiz (2010-01 → 2026-11-05), TL ve USD, maliyet sonrası, TL risksiz getiriye karşı

Ajan raporu, 06.11.2026. Bu rapor kendi hesaplarımızdan oluşuyor; literatür taraması değil. Kod: `/home/user/Xxxx/raporlar/2026-11-06_kazanc_stratejileri/hesaplar/bist_test/`. Sayısal çıktılar: `.../bist_test/cikti/*.csv|json`. Ham veri repo dışında, `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/bist_test/` altında. Yatırım tavsiyesi değildir.

---

## 0. Kısa cevap

1. **Engel düşük değil, son 3 yılda çok yüksekti.** 2010-26 boyunca TL nakit (TCMB 1 hafta repo, efektif fonlama düzeltmeli, stopaj öncesi) yılda **%16,4** getirdi. XU100 fiyat endeksi aynı dönemde **%20,0/yıl** getirdi; fark yalnızca +3,1 puan. 2024-01 ile 2026-11-05 arasında ise XU100 **%15,8/yıl**, TL nakit **%43,6/yıl** getirdi. Endeksi al-tut stratejisi nakdin yılda aritmetik 27,8 puan (geometrik −%19,4) gerisinde kaldı. USD bazında XU100 2010-26 boyunca **−%2,6/yıl** kaybettirdi. TL nakit USD bazında 2010-26'da −%5,5/yıl, 2024-26'da ise **+%19,1/yıl** getirdi (carry).
2. **İşe yaramayanlar:**
   - **Kesitsel momentum** (3-1, 6-1, 12-1 ay; 36 kombinasyon): ızgara medyanı yılda %15,2, yani TL rf'nin altında. Kendi evreninin eşit ağırlıklı (EW) portföyüne göre −%5,6/yıl geride. Placebo yüzdeliği 0,01-0,76; hiçbiri 0,95'i geçmiyor.
   - **Kısa vadeli reversal** (1 hafta ve 1 ay kaybedenleri almak): EW'ye göre −%17,9/yıl, placebo yüzdeliği 0,00. BIST'te kaybedeni almak para kaybettiriyor.
   - **Endeks trend kuralları** (SMA200, 50/200, 10 ay SMA): XU100, XU030 ve XBANK'ta değer katmıyor. Placebo yüzdeliği 0,18-0,52, XBANK'ta negatif.
3. **Kısmen işe yarayanlar:**
   - **XU100 / XUTUM 12 aylık zaman serisi momentumu (TSMOM):** TL'de yılda %24-25, rf üstü +6,8 ile +7,4 puan. Placebo yüzdeliği 0,86-0,88, istatistiksel olarak anlamlı değil. USD'de T-bill'i geçemiyor.
   - **Sektör endeksi rotasyonu** (son 1-12 ayın en iyi 2-3 sektörü, aylık): ızgara medyanı yılda **%30,6** TL, rf üstü +12,1 puan, Sharpe 0,52, MaxDD −%54. Büyük 15 sektörle ızgara medyanı %29,6, MaxDD −%34. Placebo yüzdeliği büyük sektör setinde 0,95-1,00. Ancak **2024-26'da rf'nin yılda 6-19 puan gerisinde** kaldı. Sektör endeksleri doğrudan alınamıyor.
4. **En güçlü sonuç (önemli çekincelerle): 52 haftalık zirve kırılımı + iz süren stop.**
   - **İşlem başına:** 25 kombinasyonun 25'inde de eşleşmiş rastgele hisseden fazla getiri pozitif. S2 (B52 + trend şablonu) ile iz-stop %15'te 2.073 işlem var, ortalama net +%11,4/işlem (~45 gün), medyan −%2,9, isabet %45, payoff 3,3. Aynı günlerde rastgele likit hisseye göre fark **+%5,3/işlem**, ay-kümeli t = 5,1.
   - **10 slotlu portföy:** 36 portföy varyantının (4 evren/dolum varsayımı × 9 kural) medyanı **yılda %34,8 TL** (rf üstü +15,8 puan), Sharpe 0,74, MaxDD −%41. USD'de yılda %9,4 (T-bill üstü +7,7 puan). Aynı giriş/çıkış tarihlerinde rastgele hisse seçen placebo yılda ~%21 yaptı. Stratejinin Sharpe yüzdeliği 0,83-1,00.
   - **Çekinceler:**
     - Kâr kuyrukta toplanıyor: en iyi %5 işlem net kârın **%70-77'sini** üretiyor.
     - Tavanda alamama / tabanda satamama varsayımı ("gerçekçi dolum") CAGR'yi 5-10 puan düşürüyor. Bu varsayımla tekil işlem kayıpları −%94'e kadar iniyor (2026 manipülasyon çöküşü).
     - Evren hayatta kalanlardan oluşuyor (survivorship).
     - **2024-26'da ızgara medyanı rf'ye eşit** (fazla −0,2 puan).
5. **Pratik sonuç.** Bu testlerde TL rf'yi istikrarla aşan tek yapı fiyat zirvesi kırılımına giren, kaybedeni %15 iz-stop ile kesen ve kazananı koşturan bir portföy. Bu bir mikro kenar değil; büyük ama sağ kuyruğa bağımlı bir getiri profili. Ortalama yılı değil, birkaç dev yılı (2020, 2022, 2025) ve birkaç dev işlemi yakalamaya dayanıyor. Klasik "momentum sıralaması" ve "düşeni al" BIST'te çalışmıyor.

---

## 1. Veri, evren, maliyet, risksiz faiz

Tanım notu: tablolardaki "rf üstü" ve "Fazla" sütunları geometrik fazla getiridir: (1+CAGR)/(1+rf CAGR) − 1. "Placebo yüzdeliği", stratejinin Sharpe'ının placebo dağılımındaki yeridir (1,00 = tüm çekilişlerin üstünde).


| Bileşen | Kaynak | Not |
|---|---|---|
| Hisse günlük fiyat | İş Yatırım HisseTekil: `https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse=KOD&startdate=01-01-2009&enddate=06-11-2026` | `HGDG_KAPANIS` temettü ve bedelsiz düzeltmeli kapanış. Kontrol: TUPRS'te 10.03.2023'te −%7,1 temettü, 04.04.2023'te %600 bedelsiz adımı görülüyor. `HG_KAPANIS` ham fiyat, `HGDG_HACIM` TL hacim, `DD_DEGER` USDTRY. requests varsayılan başlıklarıyla, sıralı, 0,7 sn beklemeyle çekildi. Kardeş ajanın aynı uç noktadan çektiği 259 hisse yeniden istek atılmadan okundu. |
| Endeksler | İş Yatırım ChartData `IndexHistoricalAll?period=1440` | **Fiyat** endeksleri, temettü hariç. Veri hatası: XBANK, XFINK, XILTM, XSPOR ve XUMAL'de 02.07-31.12.2010 arası değerler /100 ölçekliydi; ×100 ile düzeltildi. |
| Evren listesi | KAP Endeksler sayfası (`https://www.kap.org.tr/tr/Endeksler`, kardeş ajanın indirdiği HTML), **güncel** XUTUM (580) + diğer endeks üyeleri = 589 kod | Çekilen: 490 kod. Ek olarak güncel listede olmayan 6 hisse (SNPAM, BOLUC, TERA, KONTR, ALVES, ADANA) dahil edildi. Toplam 496 dosya, ≥120 günlük veri olan **485 hisse**. Eksik 99 kod, süre kısıtı yüzünden çekilmedi; alfabetik M-U aralığındaki küçük hisseler (liste `u01`/`f01` log'unda). |
| Uygun evren (her tarih) | ≥260 gün geçmiş, son 20 günün ≥15'inde işlem, 60 günlük medyan TL hacim | Ortalama uygun hisse sayısı: 207 (2010) → 290 (2018) → 466 (2026). Testler en likit 100/150 (kesitsel) veya 75/150 (kırılım) hisseyle yapıldı. |
| TL rf | TCMB 1 hafta repo resmi tablosu: `https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/1+Hafta+Repo` | EVDS anahtarsız erişilemediği için seçildi. Efektif fonlamanın politika faizini belirgin aştığı dönemlerde **yükseltici** düzeltme uygulandı: 21.10.2011-06.2012 %9,5; 2012 H2 %7; 07.2013-01.2014 %6,75; 2015-11.2016 %8,75; 24.01.2017-25.04.2018 %12; 26.04-31.05.2018 %14,5; 20.03-17.04.2025 %46. Getiri stopaj öncesi; hisse kazancı %0 stopajlı olduğu için bu seçim engeli olduğundan yüksek gösterir (muhafazakâr). Son değer %36 (23.10.2026). |
| USD rf | FRED DTB3 (`https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTB3`) | 2010-26: %1,5/yıl, 2024-26: %4,5/yıl, son %4,03. |
| USDTRY | ChartData `USDTRY` | 1,474 (04.01.2010) → 50,048 (05.11.2026), yılda %23,3 değer kaybı. |
| Maliyet | Spot 25 bp gidiş-dönüş (12,5 bp/yön × turnover); stres 50 bp. VIOP endeks 12,5 bp. | Kesitsel testlerde turnover tam hesaplandı: kaymış ağırlıktan yeni ağırlığa Σ\|Δw\|. |
| Zamanlama | Sinyal t kapanışında, işlem t+1 kapanışında; endeks trendinde getiri t+2'den itibaren | Look-ahead yok. Ay ve hafta sonu sinyali, ertesi işlem günü kapanışında uygulanıyor. |
| Fiyat temizliği | \|r_adj\| > %25 olan 22 gün işaretlendi | 13'ünde ham fiyat aynı hareketi gösterdi (gerçek), korundu. 4'ünde düzeltme hatası vardı, ham getiriyle değiştirildi. 5'i sıfırlandı. |

### Bilinen biaslar (sonuçları okurken akılda tutun)

1. **Survivorship (en büyüğü).** Evren bugün işlem gören hisselerden oluşuyor. Kota alınıp çıkan, birleşen veya şu an Yakın İzleme Pazarı'nda olup XUTUM dışında kalan hisseler eksik. EW-top150 evreni (aylık) yılda **%25,8**, XU100 fiyat endeksi %20,1 getirdi. +5,7 puanlık fark survivorship, EW ve temettü (~%2-4) etkilerinin toplamı. Bu yüzden tüm hisse testleri **aynı evrenin EW'sine** ve **eşleşmiş rastgele portföylere** karşı da raporlandı. Endeks testleri (T4, T5) survivorship içermiyor.
2. **IPO seçimi.** 485 hissenin 213'ü 2009'dan önce, 272'si sonra listelenmiş; yalnızca 2021-23 arası 122 halka arz var. Sonradan başarılı olup listede kalanlar fazla temsil ediliyor. Hafifletmek için "kohort2009" testi yapıldı: yalnız 31.12.2009'da zaten işlem gören hisseler.
3. **Tavan/taban dolum.** Kapanışta alım/satım varsayımı tavan ve taban serilerinde gerçekçi değil. "Gerçekçi" varyantta giriş günü ≥ +%9,5 kapanan işlemler atlandı. Çıkış günü ≤ −%9,5 ise çıkış taban bitene kadar ertelendi.
4. **Endeksler fiyat endeksi.** Temettü dahil edilmediği için al-tut ve trend getirileri yılda ~2-4 puan düşük görünüyor. Hisse testleri temettü dahil.
5. **Parametre madenciliği.** Kurallar test öncesinde literatür ve uygulama standartlarından seçildi; en iyi kombinasyon değil **ızgara medyanı** raporlanıyor. Bir istisna var: "kısa vadeli kazananlar" (KMOM) testi reversal negatif çıktıktan sonra eklendi, yani post-hoc.
6. **Portföy yol bağımlılığı.** 10 slotlu kırılım portföyü, hangi sinyalin slot bulduğuna çok duyarlı. Evren 456'dan 485 hisseye genişleyince tek bir kombinasyonun CAGR'si 3-11 puan değişti. İşlem bazlı istatistikler çok daha kararlı.

---

## 2. TEST 4: Endeks trend takibi (XU100, XU030, XBANK, XUTUM). Dışarıdayken nakit TL rf kazanıyor.

Kurallar: A) Kapanış > SMA200 (günlük), B) SMA50 > SMA200, C) ay sonu > 10 aylık SMA, D/E/F) 12/6/3 aylık TSMOM (endeks getirisi > aynı dönemin rf getirisi, ay sonu). Maliyet VIOP 12,5 bp. Placebo: aynı "içeride" ve "dışarıda" süreleri rastgele sıralanarak 300 çekiliş yapıldı.

**TL, 2010-01 → 2026-11 (seçme satırlar; tamamı `cikti/t04_ozet.csv`)**

| Endeks | Kural | İçeride | Geçiş/yıl | CAGR | rf üstü | Vol | Sharpe | MaxDD | 2024-26 CAGR | 2024-26 rf üstü | Placebo yüzdeliği |
|---|---|---|---|---|---|---|---|---|---|---|---|
| XU100 | AL-TUT | %100 | 0 | %20,0 | +%3,1 | %24,7 | 0,25 | −%34,3 | %15,8 | −%19,4 (geometrik; aritmetik −27,8 puan) | - |
| XU100 | TL rf | %0 | 0 | %16,4 | 0 | - | - | 0 | %43,6 | 0 | - |
| XU100 | A P>SMA200 | %71 | 8,3 | %19,4 | +%2,5 | %20,3 | 0,23 | −%33,7 | %20,8 | −%16,0 | 0,52 |
| XU100 | B 50>200 | %72 | 1,6 | %18,8 | +%2,0 | %21,2 | 0,20 | −%31,8 | %16,3 | −%19,1 | 0,31 |
| XU100 | C 10 ay SMA | %69 | 2,1 | %18,6 | +%1,9 | %20,6 | 0,19 | −%31,8 | %25,2 | −%13,0 | 0,30 |
| XU100 | TSMOM 12 ay | %54 | 1,5 | **%24,4** | **+%6,8** | %18,6 | **0,45** | −%37,8 | %35,4 | −%5,9 | 0,88 |
| XU100 | TSMOM 12 ay, 2x VIOP | %54 | 1,5 | %28,3 | +%10,2 | %37,1 | 0,45 | −%68,7 | %24,9 | −%13,2 | - |
| XU100 | TSMOM 3 ay | %51 | 2,9 | %20,6 | +%3,6 | %17,7 | 0,29 | −%29,8 | %35,1 | −%6,1 | 0,68 |
| XU030 | TSMOM 12 ay | %50 | 1,5 | %21,6 | +%4,4 | %19,2 | 0,32 | −%39,1 | %36,2 | −%5,3 | 0,77 |
| XU030 | TSMOM 3 ay | %50 | 3,2 | %15,5 | −%0,8 | %18,7 | 0,05 | −%31,2 | %35,8 | −%5,6 | 0,24 |
| XBANK | AL-TUT | %100 | 0 | %16,8 | +%0,3 | %35,7 | 0,19 | −%53,0 | - | - | - |
| XBANK | A P>SMA200 | %61 | 7,7 | %14,4 | −%1,7 | %27,9 | 0,08 | −%41,7 | %8,9 | −%24,3 | 0,41 |
| XBANK | TSMOM 6 ay | %50 | 2,0 | %20,4 | +%3,4 | %25,8 | 0,26 | −%39,1 | %29,3 | −%10,1 | 0,77 |
| XUTUM | TSMOM 12 ay | %56 | 1,2 | **%25,0** | **+%7,4** | %18,2 | **0,48** | −%35,7 | %40,1 | −%2,6 | 0,86 |
| XUTUM | TSMOM 3 ay | %52 | 2,9 | %24,2 | +%6,7 | %17,1 | 0,46 | −%29,1 | %41,3 | −%1,8 | 0,86 |

**USD (fazla getiri T-bill'e göre):**

| Endeks | Kural | CAGR | Fazla | MaxDD |
|---|---|---|---|---|
| XU100 | Al-tut | −%2,6 | −%4,1 | −%75,2 |
| XU100 | TSMOM12 | +%0,9 | −%0,6 | −%73,5 |
| XU100 | TSMOM12 2x | +%4,1 | +%2,5 | −%85,5 |
| XUTUM | TSMOM12 | +%1,4 | −%0,1 | - |
| XUTUM | TSMOM12 2x | +%5,3 | +%3,7 | −%84,2 |
| XBANK | Al-tut | −%5,3 | - | −%91,4 |

**Vol hedefleme** (%25, en fazla 2x) hiçbir endekste Sharpe'ı iyileştirmedi. Örnek: XU100 TSMOM12 0,45 → 0,44; XU100 A 0,23 → 0,20.

**Yıllık (TL):** XU100 TSMOM12 / XU100 al-tut / TL rf

| Yıl | TSMOM12 | Al-tut | TL rf |
|---|---|---|---|
| 2018 | +%2,5 | −%20,9 | +%17,4 |
| 2020 | +%49,1 | +%29,1 | +%10,2 |
| 2022 | +%196,6 | +%196,6 | +%12,9 |
| 2024 | +%54,5 | +%31,6 | +%49,1 |
| 2025 | +%43,5 | +%14,6 | +%43,5 |
| 2026 YTD | +%6,2 | +%0,6 | +%30,6 |

**Yorum.** Fiyat/SMA trend kuralları BIST'te düşüşleri kesiyor, ama yükselişleri de kaçırıyor; net değer sıfır, placebo ortası. 12 aylık TSMOM tutarlı en iyi aday: yılda +7 puan, MaxDD al-tut ile aynı. Yine de placebo yüzdeliği 0,86-0,88 ile tek başına "kanıt" değil. Uygulama VIOP endeks kontratı + teminatın PPF/repoda tutulmasıyla yapılabilir. 2x kaldıraç ortalamayı artırıyor, ama MaxDD −%69'a çıkıyor. USD'de anlamlı bir şey yok.

---

## 3. TEST 5: Sektör endeksi rotasyonu (aylık, en iyi 2-3 sektör, EW, 25 bp)

Evren 21 saf sektör endeksi: XBANK, XSGRT, XFINK, XGMYO, XHOLD, XELKT, XILTM, XULAS, XTCRT, XTRZM, XSPOR, XGIDA, XKMYA, XMANA, XMESY, XKAGT, XTAST, XTEKS, XUTEK, XMADN (2013+), XINSA (2013+). "Büyük" set 15 sektör: XSPOR, XTEKS, XKAGT, XMADN, XFINK ve XTRZM çıkarıldı. Lookback {1, 3, 6, 12} ay × top {2, 3}. Placebo: aynı sayıda ve aynı yenileme oranıyla rastgele sektör seçimi, 300 çekiliş.

| Strateji (TL, 21 sektör) | CAGR | rf üstü | Vol | Sharpe | MaxDD | 2024-26 CAGR | 2024-26 rf üstü | Placebo yüzdeliği | Aylık turnover |
|---|---|---|---|---|---|---|---|---|---|
| EW tüm sektörler | %25,2 | +%7,5 | %26,1 | 0,40 | −%35,6 | %14,5 | −%21,0 | - | - |
| XU100 | %19,8 | +%2,9 | %26,8 | 0,23 | −%31,0 | %14,1 | −%21,3 | - | - |
| MOM1 top3 | %31,8 | +%13,2 | %33,0 | 0,54 | −%50,9 | %43,9 | −%0,7 | 0,98 | 1,53 |
| MOM3 top2 | %33,4 | +%14,5 | %37,0 | 0,55 | −%43,0 | %60,4 | +%10,6 | 0,97 | 1,04 |
| MOM6 top3 | %27,6 | +%9,6 | %33,4 | 0,44 | −%56,1 | %43,2 | −%1,2 | 0,84 | 0,68 |
| MOM12 top3 | %37,1 | +%17,7 | %35,7 | 0,64 | −%46,2 | %50,8 | +%3,9 | 0,99 | 0,51 |
| **Izgara medyanı (8)** | **%30,6** | **+%12,1** | - | **0,52** | **−%53,5** | - | - | 0,72-0,99 | - |
| Büyük 15 sektör, ızgara medyanı | %29,6 | +%11,3 | ~%29 | 0,51 | −%34,3 | %17-37 (8 kombinasyon) | −%6 ile −%20 | 0,95-1,00 | - |
| Büyük 15, MOM12 top3 | %31,7 | +%13,1 | %28,5 | 0,57 | −%35,0 | %23,0 | −%15,2 | 0,99 | 0,45 |

- **USD:** 21 sektör MOM12 top3 yılda %11,1 (T-bill üstü +%9,4), MaxDD −%58. Büyük set MOM12 top3 %6,7.
- **Rejim filtresi** (XU100 > SMA200): MaxDD'yi 5-15 puan düşürdü (örn. büyük MOM12 top3 −%35 → −%27). CAGR'yi değiştirmedi.
- **Maliyet 50 bp'ye çıkınca** CAGR 1-3 puan düştü.
- **Getiri yoğunlaşması:** Büyük set MOM12 top3 2017'de +%107, 2022'de +%268 yaptı. Aynı kural 2024'te %43,0 (rf %48,8), 2025'te %30,4 (rf %43,5), 2026'da −%5,3 (rf %30,0) getirdi.
- **Seçim sıklığı** (büyük set, MOM12 top3): XUTEK %50, XULAS %36, XMANA %31, XMESY %24.

**Yorum.** Sektör rotasyonu, endeks seviyesinde (survivorship yok) EW sektörlere göre yılda ~+5 puan, rastgele sektör seçimine göre ~+8-15 puan ekliyor. Placebo yüzdeliği büyük sette 0,95'in üstünde. Bu rapordaki en "temiz" (biassız) pozitif sonuç bu. Üç ciddi sorun var:
- 2024-26'da üç yılın üçünde de rf'nin altında kaldı.
- Sektör endeksleri doğrudan alınamıyor (BYF/VIOP karşılığı çoğu sektörde yok). Sepetle kopyalamak takip hatası ve ek maliyet getiriyor.
- Volatilite %29-37, MaxDD −%35 ile −%58.

---

## 4. TEST 1 ve 2: Kesitsel momentum ve kısa vadeli reversal (hisse, en likit 100/150)

Izgara: lookback {3-1, 6-1, 12-1 ay} × rebalans {haftalık, 2 haftalık, 4 haftalık} × dilim {D10, Q5} × evren {100, 150} = 36 kombinasyon. Long-only, "long − XU100 (VIOP kısa)" ve rejim filtreli versiyonlar ayrıca test edildi. Placebo: aynı sayıda hisse ve aynı yenileme oranıyla rastgele seçim, 200 çekiliş.

| Test (TL, 25 bp) | n | Medyan CAGR | Medyan rf üstü | Sharpe | MaxDD | 2024-26 CAGR | 2024-26 rf üstü | En iyi / en kötü CAGR |
|---|---|---|---|---|---|---|---|---|
| EW top150 evren (W4, kıyas) | - | %25,8 | +%8,1 | 0,41 | −%38,3 | %3,6 | −%28,6 | - |
| MOM long-only | 36 | %15,2 | −%1,0 | 0,18 | −%74,8 | −%7,5 | −%35,8 | %26,6 / %5,2 |
| MOM, aynı evrenin EW'sine göre | 36 | **−%5,6/yıl** | - | IR −0,24 | - | −%4,3 | - | +%0,7 / −%14,8 |
| MOM long − XU100 | 36 | %12,3 | −%3,5 | −0,02 | −%62,5 | %17,7 | −%18,2 | - |
| MOM + rejim (XU100>SMA200) | 36 | %19,8 | +%3,0 | 0,26 | −%44,7 | %11,3 | −%22,9 | - |
| MOM, USD | 36 | −%6,7 | −%8,1 | 0,00 | −%83,8 | - | - | - |
| REV (1h ve 1ay kaybedenler) | 12 | %1,0 | −%13,2 | −0,26 | −%87,1 | −%47,1 | −%63,2 | - |
| REV, EW'ye göre | 12 | **−%17,9/yıl** | - | IR −1,28 | - | - | - | - |
| KMOM (1h ve 1ay kazananlar, post-hoc) | 12 | %17,9 | +%1,3 | 0,20 | −%55,5 | %19,1 | −%17,2 | - |
| KMOM, EW'ye göre | 12 | −%3,3/yıl | - | - | - | - | - | - |

**Placebo** (Sharpe; yüzdelik):
- MOM Q5 top150: 3-1 W1 0,23 (0,33); 6-1 W1 0,18 (0,07); 12-1 W1 0,18 (0,05); 3-1 W4 0,36 (0,51); 6-1 W4 0,42 (0,76); 12-1 W4 0,33 (0,16); 12-1 W2 0,19 (0,01).
- REV1h D10: −0,55 (0,00). REV1ay D10 W4: −0,17 (0,00).
- KMOM1h D10: −0,26 (0,01). KMOM1ay D10 W4: 0,48 (0,97, tek konfigürasyon, post-hoc).

**Yorum.** BIST'te getiri sıralamasına dayalı momentum hiçbir ufukta rastgele seçimden iyi değil. Son 1 haftanın **iki ucu da** (en çok yükselen ve en çok düşen) EW'ye göre yılda 13-20 puan kaybettiriyor. Bu, "lottery/MAX" etkisiyle uyumlu. Uç hareket eden hisseyi kovalamak da, düşüşte almak da zarar ediyor. Kullanıcının daha önce live denediği 1-3 günlük mikro kenarların yanında, bu sonuç "sıralama ile hisse seçimi" ailesinin tamamen elenebileceğini gösteriyor.

---

## 5. TEST 3: 52 haftalık / 6 aylık zirve kırılımı ve trend şablonu (olay bazlı + 10 slotlu portföy)

**Tanımlar:**
- **TT:** P > SMA50 > SMA150 > SMA200; SMA200 21 gün öncesinden yüksek; P ≥ 1,25 × 52 haftalık dip; P ≥ 0,75 × 52 haftalık zirve; RS (0,4·R3a + 0,2·R6a + 0,2·R9a + 0,2·R12a) evren içi yüzdeliği ≥ 80.
- **B52:** kapanış, önceki 252 günün en yüksek kapanışının üstünde. **B126:** aynısı 126 gün için.
- **Sinyaller:** S1 = B52; S2 = B52 + TT; S3 = B126 + TT; S4 = TT'nin ilk günü; S5 = S2 + XU100 > SMA200.
- **Çıkışlar:** sabit 10, 20 veya 40 gün; %15 iz süren stop (zirve kapanıştan, en fazla 120 gün); kapanışın SMA50 altına inmesi.
- **İşlem kuralları:** maliyet 25 bp. Aynı hissede açık işlem varken yeni giriş yok.
- **Placebo:** (a) işlem bazında, aynı giriş-çıkış günlerinde tüm likit evrenin ortalaması; (b) portföy bazında, her işlemin hissesini aynı gün rastgele bir likit hisseyle değiştirip portföyü yeniden simüle etmek, 40 çekiliş.

### 5.1 İşlem bazlı (ana evren: en likit 150, 2010-2026)

| Sinyal | Çıkış | N | Gün | Ort. net | Medyan | İsabet | Payoff | Çarpıklık | p05 / p95 | Placebo üstü | t (ay-küme) | 2024-26 placebo üstü |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 B52 | sabit 20 | 6.129 | 20 | %4,0 | %1,5 | %54 | 1,56 | 4,5 | −%20 / +%36 | +%1,1 | 2,7 | +%2,7 |
| S1 B52 | iz %15 | 3.457 | 49 | %11,7 | −%1,3 | %48 | 3,20 | 5,7 | −%19 / +%85 | +%4,6 | 5,8 | +%7,1 |
| S2 B52+TT | sabit 20 | 3.292 | 20 | %3,8 | %0,8 | %53 | 1,53 | 4,9 | −%24 / +%40 | +%1,2 | 1,8 | +%4,0 |
| S2 B52+TT | iz %15 | 2.073 | 45 | %11,4 | −%2,9 | %45 | 3,30 | 6,4 | −%20 / +%88 | **+%5,3** | **5,1** | +%10,9 |
| S2 B52+TT | SMA50 altı | 2.108 | 40 | %11,0 | −%3,5 | %41 | 3,88 | 6,7 | −%23 / +%86 | +%4,9 | 4,3 | +%13,9 |
| S4 TT ilk gün | sabit 20 | 4.032 | 20 | %2,4 | %0,1 | %51 | 1,41 | 5,3 | - | +%0,4 | 1,5 | +%1,2 |
| S5 S2+rejim | iz %15 | 1.855 | 45 | %12,0 | −%2,1 | %46 | 3,31 | 5,5 | −%20 / +%90 | +%5,7 | 5,4 | +%10,9 |

- **25 kombinasyonun medyanı:** ort. net %7,4, isabet %51, payoff 1,73, placebo üstü +%2,3 (t 2,9). Placebo üstü fark 25/25 kombinasyonda pozitif.
- **Gerçekçi dolumla** medyan placebo üstü +%1,6 (23/25 pozitif). Top75 evrende +%1,8 (25/25). Kohort2009'da +%1,1 (22/25).
- **Trend şablonunun katkısı:** sadece TT sinyali (S4) neredeyse sıfır üretiyor. Değer **zirve kırılımı tetikleyicisinden** ve **kazananı koşturan çıkıştan** geliyor.
- **Sabit 20 gün tutma** pozitif ama küçük (+%1,1 ile +%1,5/işlem). İz-stop ve SMA50 çıkışı bunu ~4 katına çıkarıyor.
- **Yıllık tutarlılık** (S2 iz %15, placebo üstü): 17 yılın 15'inde pozitif (2011 −%1,1, 2019 −%0,8). 2020 +%7,8, 2022 +%9,6, 2025 +%17,4.
- **Kuyruk bağımlılığı:** en iyi %5 işlem net kârın %70'ini üretiyor. En iyi 20 işlem çıkarılırsa ortalama %11,4 → %8,4/işlem, placebo üstü %5,3 → %2,7. 2025-26'nın en iyi 10 işlemi (KTLEV +%593, ODINE +%520, HEDEF, PEKGY, PASEU…) o dönemin toplam net kârının 2/3'ü.

### 5.2 10 slotlu portföy (her girişte özkaynak/10; slot doluysa RS önceliği; boş nakit TL rf kazanıyor)

| Evren / dolum | Kural | CAGR TL | rf üstü | Sharpe | MaxDD | 2024-26 CAGR | 2024-26 rf üstü | CAGR USD | Placebo medyan CAGR | Sharpe yüzdeliği |
|---|---|---|---|---|---|---|---|---|---|---|
| Ana (top150) | S1 sabit 20 | %30,7 | +%12,2 | 0,57 | −%43,3 | %59,6 | +%11,0 | %6,0 | %20,6 | 0,93 |
| Ana | S1 iz %15 | %42,7 | +%22,6 | 0,97 | −%33,0 | %41,8 | −%1,5 | %15,8 | %23,1 | 1,00 |
| Ana | S2 iz %15 | %50,9 | +%29,6 | 1,19 | −%38,6 | %125 | +%56,5 | %22,4 | %22,4 | 1,00 |
| Ana | S5 iz %15 | %54,1 | +%32,4 | 1,35 | −%31,6 | %110 | +%46,2 | %25,0 | - | - |
| Gerçekçi dolum | S1 iz %15 | %33,0 | +%14,2 | 0,68 | **−%61,3** | %17,9 | −%18,0 | %7,9 | %21,3 | 1,00 |
| Gerçekçi dolum | S2 iz %15 | %36,2 | +%17,0 | 0,78 | −%45,1 | %60,1 | +%11,3 | %10,5 | %22,3 | 1,00 |
| Gerçekçi dolum | S2 sabit 20 | %24,4 | +%6,8 | 0,38 | −%57,7 | %27,3 | −%11,5 | %0,9 | %17,8 | 0,93 |
| Top75 | S2 iz %15 | %35,4 | +%16,3 | 0,81 | −%27,3 | %73,8 | +%20,8 | %9,8 | %20,4 | 1,00 |
| Top75 | S1 iz %15 | %26,6 | +%8,7 | 0,49 | −%32,3 | %32,9 | −%7,6 | %2,7 | %18,3 | 1,00 |
| Kohort2009 | S2 iz %15 | %39,5 | +%19,9 | 0,90 | −%39,8 | %39,9 | −%2,8 | %13,2 | %25,2 | 1,00 |
| Kohort2009 | S5 iz %15 | %41,9 | +%21,9 | 1,03 | −%26,4 | %45,8 | +%1,4 | %15,1 | - | - |
| **36 varyantın medyanı** | - | **%34,8** | **+%15,8** | **0,74** | **−%41,4** | **%43,5** | **−%0,2** | **%9,4** (+%7,7 T-bill üstü) | ~%21 | 0,83-1,00 |

**Yıllık (TL, ana evren, S2 iz %15):**

| 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 YTD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| +%52 | −%17 | +%49 | +%12 | +%41 | +%9 | −%5 | +%54 | −%10 | +%52 | +%89 | +%44 | +%280 | +%50 | +%59 | +%190 | +%114 |

Aynı kural gerçekçi dolumla 2026'da +%16, S1 iz %15 gerçekçi dolumla 2026'da −%39. Fark, Eylül 2026 fon/manipülasyon çöküşünde tabandan çıkamamaktan geliyor. Gerçekçi varyantın en kötü işlemleri: ALKLC −%94, IEYHO −%94, ANELE −%94, MANAS −%88.

**Yorum.**
1. **Bu, testlerdeki tek hisse-düzeyi pozitif kenar.** Rastgele hisseyle yapılan aynı-zamanlama placebosu yılda ~%21 üretiyor. Kırılım + iz-stop portföyü yılda +8 ile +33 puan ekliyor.
2. **Getirinin iki kaynağı var:** (a) piyasa zamanlaması, yani kırılımlar yükseliş dönemlerinde yoğunlaşıyor; (b) seçim, yani zirve yapan hisse sonraki 1-3 ayda rastgele hisseyi işlem başına %2-5 geçiyor.
3. **Ancak:**
   - (i) Kâr birkaç dev işleme ve yıla bağımlı.
   - (ii) Gerçekçi dolumda MaxDD −%45 ile −%61.
   - (iii) Survivorship, IPO seçimi ve eksik YİP hisseleri sonucu muhtemelen yukarı çarpıtıyor. Kohort2009 ve top75 varyantları sonucu küçültüyor ama yok etmiyor.
   - (iv) 2024-26 ızgara medyanı rf'ye eşit. Pozitif 2024-26 sonuçları ağırlıkla manipülasyon döngüsündeki hisselerin yükseliş bacağından geliyor.
4. **Uygulanabilirlik:** spot, long-only, 10 pozisyon. Kırılım hisselerinin çoğunun VIOP pay kontratı yok, yani kaldıraç ve açığa satış gerekmiyor (ve mümkün de değil). Kapasite küçük-orta: top150 evrende küçük hisseler var; işlem başı birkaç milyon TL üstü slipaj üretir, bu test edilmedi.

---

## 6. TEST 6: Rejim filtresi ve vol hedefleme (özet)

| Test | Rejim filtresinin (XU100 > SMA200) etkisi |
|---|---|
| Momentum (T1) | CAGR %15,2 → %19,8, MaxDD −%75 → −%45. EW'yi yine geçmiyor. |
| Sektör (T5) | CAGR ±2 puan, MaxDD −5 ile −15 puan. |
| Kırılım (T3) | S5, S2'ye göre CAGR +1 ile +6 puan, MaxDD −5 ile −13 puan iyileşme. |

Bu bir **risk kontrolü**, getiri kaynağı değil. Vol hedefleme (%25) endeks trendinde fayda sağlamadı.

---

## 7. Sonuç: ne işe yarıyor, ne yaramıyor (bu veriyle)

| Yaklaşım | TL rf'yi aşıyor mu (2010-26)? | 2024-26? | Kanıt kalitesi | Uygulanabilirlik |
|---|---|---|---|---|
| XU100 al-tut | +3,1 puan | −19 puan (geometrik) | Biassız | Kolay |
| Endeks SMA trendleri | ~0 | Negatif | Placebo ortası | Kolay (VIOP) |
| XU100/XUTUM TSMOM12 | +7 puan | −3 ile −6 puan | Placebo 0,86-0,88 | Kolay (VIOP) |
| Sektör rotasyonu | +11 ile +12 puan (medyan) | −6 ile −19 puan (büyük set) | Biassız, placebo ≥0,95 | Zor (sepet) |
| Kesitsel momentum | −1 puan; EW'nin 5,6 puan gerisinde | −36 puan | Placebo ≤0,76 | - |
| Reversal (düşeni al) | −13 puan; EW'nin 18 puan gerisinde | −63 puan | Placebo 0,00 | - |
| **52 haftalık kırılım + iz-stop (10 slot)** | **+16 puan (36 varyant medyanı)** | **≈0 (medyan)** | Survivorship'li evren, placebo 0,83-1,00, kuyruk bağımlı | Spot, long-only |

**Kullanıcının stiline ("stratejik kümelenme", haftalar-aylar ufku) uyan sonuç:** küme seçiminde sektör ve endeks momentumunu (12 ay ve 3 ay), hisse seçiminde ise 52 haftalık zirve kırılımını kullanmak. Pozisyon yönetiminde sabit hedef değil iz-stop veya SMA50 çıkışı kullanmak. Kaybedeni kesip kazananı koşturmak, testteki pozitif getirinin ana kaynağı. Bu yapı bile son 3 yılda ancak TL faizine yetişti. Faiz %36 iken beklenen fazla getiri muhtemelen 2010-26 ortalamasının altında.

---

## 8. Dosyalar

- **Kod** (`/home/user/Xxxx/raporlar/2026-11-06_kazanc_stratejileri/hesaplar/bist_test/`):
  - Veri: `u01_evren.py` (KAP üyelikleri), `f01_hisse.py` + `f01b_ters.py` (HisseTekil), `f02_endeks.py` (ChartData), `u02_panel.py` (temizlik ve likidite).
  - Altyapı: `ortak.py` (rf, istatistik, motor), `motor.py` (seçim, placebo).
  - Testler: `t01_momentum_reversal.py`, `t03_kirilim_trend_sablonu.py` (ortam değişkenleri `UNIV=top75|kohort2009`, `GERCEKCI=1`, `NPL`), `t04_endeks_trend.py`, `t05_sektor_rotasyon.py` (`SET=buyuk`).
  - Tablolar: `r01_tablolar.py`.
- **Çıktılar** (`.../bist_test/cikti/`): `t01_ozet.csv`, `t01_placebo.json`, `t01_yillik_TL.csv`, `t03_islem_ozet*.csv`, `t03_portfoy*.csv`, `t03_portfoy_yillik_TL*.csv`, `t03_islemler_S2_iz15*.csv`, `t03_yillik_islem_S2_iz15*.csv`, `t04_ozet.csv`, `t04_yillik.csv`, `t04_placebo.json`, `t05_ozet*.csv`, `t05_yillik*.csv`, `t05_placebo*.json`, `u02_temizlik.json`.
- **Doğrulanamayanlar:** Web arama kotası (oturum geneli) doldu. TL mevduat ve PPF stopaj oranları bu ajan tarafından teyit edilmedi; kardeş rapor `ajanlar/abd_pratik.md` BIST pay kazancı için %0 stopaj veriyor. Rf stopaj öncesi kullanıldığı için engel muhafazakâr.
