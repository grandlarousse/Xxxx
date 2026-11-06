# dalga_bist: BIST tema/küme dalgaları 2012-2026 ve yakalama kuralları

Ajan anahtarı: `dalga_bist`. Tarih: 06.11.2026 (Cuma). Veri: İş Yatırım ChartData, günlük düzeltilmiş kapanış, 06.11.2026 ~12:45 TSİ'de çekildi. Backtestler **05.11.2026 kapanışına** kadar. 06.11 verisi gün içi anlık fiyat olduğu için yalnız güncel durum tablosunda ayrı bir sütunda kullanıldı. Kod ve çıktılar: `hesaplar/dalga_bist/`. Yatırım tavsiyesi değildir.

## 0. Net cevap

1. **Dalgalar gerçek ve büyük.** 24 küme, 2012-2026 arasında taban tanıma göre 167 dalga verdi: XU100'e göre ≤6 ayda en az +%30, bacak sonu en az %15 göreli dönüşle teyitli. Dalga medyanı +%55 göreli ve 101 işlem günü. Dalga günleri küme-günlerin %31'i, ama göreli kazancın tamamı bu günlerde (+88,5 log birimi). Dalga dışı günler toplamda -62,6.
2. **Dalgayı sistematik yakalamak, kümeleri körlemesine tutmaktan pek iyi değil.** Zamanlama yapmayan kontrol, 24 kümenin eşit ağırlıklı sepeti (EW): 2012-26'da yıllık bileşik getiri (CAGR) %36,8, XU100 %23,3, TL rf %17,6. 456 kural yapılandırmasının yalnız %34'ü EW'yi geçti. Olay kurallarının (RS kırılımı, genişlik, ikili momentum) sepet medyanı EW'nin yılda 3-6 puan altında.
3. **Sağlam çıkan tek aile 12 aylık göreli güç (RS) rotasyonu.** Her ay sonu 12 aylık getirisi XU100'e göre en iyi 3 küme alınıyor, sepet olarak tutuluyor. 32 yapılandırmanın medyanı: CAGR %41,7, EW'ye göre yılda +3,6 puan, MaxDD -%40, Sharpe 0,85 (EW 0,77), USD CAGR %13,6.
   - Hayatta kalan yanlılığı olmayan **sektör endeksi** evreninde aynı kural EW'yi yılda +3,0 puan geçti (mikro sektörler hariç).
   - Aylık momentum IC'si en güçlü 12 ayda: 0,065, t=3,2. Bunun ekonomik karşılığı yaklaşık **yılda +3-5 puanlık** bir üstünlük. Daha fazlası beklenmemeli.
4. **2024-26 rejiminde hiçbir küme kuralı TL rf'yi geçemedi.** 456 yapılandırmanın 0'ı. Bu dönemde rf %43,1, en iyi kural %34,8, 12 ay rotasyon medyanı %16-17, EW %10,6, XU100 %15,9.
   - Aynı kurallar 2019-23 negatif reel faiz döneminde %100, 2012-18'de %87 oranında rf'yi geçti.
   - Küme dalgası avcılığının getirisi faiz rejimine bağlı. Yüksek reel faizde spot uzun pozisyonla TL eşiği (%36-40) aşılamıyor.
5. **Yanlış başlangıç oranı yüksek, kazanç birkaç büyük dalgadan geliyor.** Olay kurallarında yanlış başlangıç (hiçbir dalgaya değmeyen işlem) %36-57, medyan %47. XU100'e göre isabet %46, ortalama net işlem +%9,3, medyan +%0,1.
   - Rotasyonda en iyi %10'luk tutma dönemi pozitif katkının ~2/3'ünü veriyor.
   - Dar iz süren stop (%10) yakalamayı düşürüyor. Çıkış RS kaybı veya ay sonu sıralamasıyla yapılmalı.
6. **"Lider hisse" sürümü sepetten kötü.** Rotasyonda medyan CAGR 5-12 puan düşük (olay kurallarında 0-9 puan), MaxDD -%55 ile -%80 arası. XU100>200 GHO (günlük hareketli ortalama) filtresi olay kurallarında CAGR'ı 2-6 puan artırıyor ve 2024-26'yı belirgin iyileştiriyor. 12 ay rotasyonda tüm dönemde nötr.
7. **Bugün (05.11 kapanışı):**
   - XU100 11.333. Ağustos tepesinden -%25 (fon krizi), 50 ve 200 GHO altında. **Piyasa filtresi KAPALI**, hiçbir kümede mutlak momentum (6 ay TL getiri > rf) yok. Filtreli kurallar nakitte.
   - Göreli güçte RS kırılımı veren kümeler: **BANKA** (126 g RS zirvesi, 3 ay +%23 göreli) ve **HAVACILIK** (126 g zirve, +%16).
   - 12 ay RS ilk 3: **RAFİNERİ, HOLDİNG, KOZA_ALTIN**. RAFİNERİ ve KOZA dönüyor, HOLDİNG RS yükselişte.
   - Dip: CAM_SERAMİK, BEYAZ_EŞYA, KİMYA, GÜBRE, YENİLENEBİLİR, ELK_EKİPMAN.
   - Banka, holding ve havacılık tek risk bloğu (günlük korelasyon 0,77-0,79). RAFİNERİ bu bloğa doğal karşı ağırlık: fazla getiri korelasyonu bankayla -0,42, havacılıkla -0,31.

## 1. Veri ve yöntem

- **Fiyat:** ChartData `IndexHistoricalAll` (period=1440), 2009-06 → 2026-11-06. 135 hisse, 29 endeks ve USDTRY için varsayılan istek başlıklarıyla tek tek istek, 0,7 sn bekleme. Ham önbellek scratchpad'de; repoda ham veri yok.
- **Fiyat düzeltmesi:** Hisseler temettü ve bedelsiz düzeltmeli, XU100 fiyat endeksi. Kümeler XU100'e göre yılda ~2-4 puan temettü avantajlı görünür.
- **Temizlik:** |günlük getiri|>%35 olan 14 gün 0 yapıldı (AFYON 2010, AKGRT 2019 tek günlük hatalı fiyat, USAK 2012). Halka arz sonrası ilk 20 işlem günü küme getirisine girmez. Askıda fiyat en çok 5 gün ileri taşınır.
- **Kümeler:** Bugün işlem gören, görece likit üyeler, eşit ağırlık, günlük yeniden dengeleme yaklaşımı. Küme en az 2 üye ve 130 gün geçmişle "uygun" sayılır.
- **Hayatta kalan yanlılığı:** Birleşen veya kotasyondan çıkan hisseler (TRKCM/ANACM/SODA vb.) yok. Bugün likit olan hisse genellikle geçmişte kazanmış hissedir. Bu yüzden sektör endeksi kontrolü yapıldı (§3.6).

| Küme | Üyeler (V = VİOP pay vadelisi var) | Uygunluk |
|---|---|---|
| BANKA | AKBNK V, GARAN V, YKBNK V, ISCTR V, VAKBN V, HALKB V, TSKB V, ALBRK, SKBNK | 2009 |
| HOLDİNG | KCHOL V, SAHOL V, DOHOL V, AGHOL, ALARK V, TKFEN V, NTHOL, GLYHO | 2009 |
| HAVACILIK | THYAO V, PGSUS V, TAVHL V, CLEBI | 2009 (PGSUS 2013) |
| RAFİNERİ | TUPRS V, PETKM V, AYGAZ, TRCAS | 2009 |
| ÇELİK | EREGL V, KRDMD V, ISDMR, BRSAN V, CEMTS, KCAER, IZMDC | 2009 |
| KOZA_ALTIN | TRALT V, TRMET V, TRENJ (eski KOZAL/KOZAA/IPEKE; 2015 TMSF dönemi dahil) | 2010 |
| SAVUNMA | ASELS V, OTKAR, SDTTR, ALTNY, ONRYT | 2009 (2023'e kadar 2 üye) |
| ÇİMENTO | CIMSA V, OYAKC V, AKCNS, BTCIM, NUHCM, AFYON, BSOKE, GOLTS, KONYA | 2009 |
| ELK_EKİPMAN (trafo/kablo) | ASTOR V, EUPWR, GESAN, KONTR, PRKAB | 2020-11 (ASTOR 2023-02) |
| PERAKENDE | BIMAS V, MGROS V, SOKM V, MAVI, CRFSA | 2009 |
| OTOMOTİV | FROTO V, TOASO V, DOAS V, TTRAK, KARSN, ASUZU | 2009 |
| OTO_YAN | EGEEN, BRISA, KORDS, FMIZP, JANTS | 2009 |
| TELEKOM | TCELL V, TTKOM V | 2009 |
| GYO | EKGYO V, ISGYO, TRGYO, SNGYO, HLGYO, OZKGY, RYGYO | 2010 |
| KİMYA | SASA V, AKSA, ALKIM, DYOBY, KMPUR | 2009 |
| GÜBRE | GUBRF V, HEKTS V, BAGFS | 2009 |
| CAM_SERAMİK | SISE V, KUTPO, EGSER, USAK, QUAGR | 2009 |
| GIDA | ULKER V, AEFES V, CCOLA, TATGD, TUKAS, BANVT, PNSUT | 2009 |
| ELK_ÜRETİM | AKSEN V, ENJSA V, ZOREN, ODAS V, AYDEM, AKENR | 2010 |
| YENİLENEBİLİR | GWIND, NATEN, CWENE, ALFAS, SMRTG, YEOTK | 2021-12 |
| TEKNOLOJİ (küçük) | LOGO, NETAS, KAREL, INDES, LINK, ARDYZ, FONET, ALCTL | 2009 |
| BEYAZ_EŞYA | ARCLK V, VESTL V, VESBE | 2009 |
| SİGORTA | ANSGR, AKGRT, ANHYT, TURSG, AGESA, RAYSG | 2009 |
| SAĞLIK | SELEC, DEVA, ECILC, LKMNH, MPARK | 2009 |

Ek evren: 22 BIST sektör endeksi (XBANK, XHOLD, XUTEK, XELKT, XGIDA, XGMYO, XKMYA, XMADN, XMANA, XMESY, XINSA, XTAST, XTEKS, XTRZM, XULAS, XILTM, XKAGT, XSGRT, XTCRT, XFINK, XBLSM, XSPOR).

- **TL rf:** TCMB ortalama fonlama veya politika faizine yakın, elle kurulmuş adım fonksiyonu (`veri.py`), 2012-26 CAGR %17,6. FRED'deki TR gecelik serisi koridor alt bandı olduğu için kullanılmadı. 2021-23'te mevduat ve KKM getirisi politika faizinin üstündeydi, bu yıllarda rf düşük kalmış olabilir.
- **Zamanlama:** Sinyal t kapanışında yalnız ≤t bilgisiyle üretilir. İşlem t+1 kapanışında (taban gecikme L=1), getiri t+2'den başlar. L=0 duyarlılığı ayrıca test edildi.
- **Maliyet:** Tek yön %0,25 × ağırlık değişimi. %0,50 duyarlılığı test edildi. Lider değişimi tam devir sayıldı. Nakit ve boş slot TL rf kazanır. Vergi yok.
- **Dalga tanımı (sonuçlara bakmadan ilan edildi):**
  - Göreli endeks R = küme TL getiri endeksi / XU100. log R üzerinde zigzag çizilir, dönüş eşiği %15.
  - Bir yükseliş bacağı, içinde ≤126 işlem günlük bir pencerede R +%30 artmışsa **dalgadır**.
  - Sert sürüm: dönüş %20, eşik +%50. Bu sürümde 69 küme dalgası çıktı.

## 2. Dalga envanteri

Taban tanım, 2012+: **167 dalga**.

| Yıl | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Dalga sayısı | 4 | 12 | 4 | 4 | 7 | 5 | 10 | 19 | 23 | 10 | 20 | 22 | 13 | 5 | 9 |

- **Küme başına dalga sayısı:** KOZA_ALTIN 21, SAĞLIK 11, TEKNOLOJİ 11, SAVUNMA 10, BEYAZ_EŞYA, CAM ve ELK_EKİPMAN 9'ar. HOLDİNG yalnız 1 (2026), BANKA 4.
- **Küçük ve az üyeli kümeler dalgaya yatkın:** 3 üyeli KOZA en oynak küme (yıllık oynaklık %52).
- **Negatif reel faiz dönemlerinde dalga sayısı patlıyor:** 2019-20, 2022-23. 2024-26 yüksek reel faiz döneminde azalıyor.

**Öne çıkan dalgalar.** rel = XU100'e göre göreli getiri. TL ve USD mutlak getiridir. Sürücü sütunu genel bilgidir, olay bazında doğrulanmadı. 2026 için haber taraması kullanıldı.

| Küme | Dip → Tepe | Gün | rel | TL | USD | XU100 | Lider | Sürücü |
|---|---|---|---|---|---|---|---|---|
| ÇELİK | 2019-02 → 2021-08 | 618 | +195% | +307% | +147% | +38% | IZMDC +426% | 2020-21 küresel çelik fiyat patlaması |
| GÜBRE | 2019-01 → 2020-06 | 347 | +399% | +492% | +384% | +19% | GUBRF +852% | Gübre fiyatları, küçük şirket spekülasyonu |
| ÇİMENTO | 2020-03 → 2021-03 | 259 | +203% | +387% | +279% | +60% | BTCIM +656% | Covid sonrası %8,25 politika faizi, inşaat ve ihracat |
| OTO_YAN | 2020-03 → 2021-04 | 261 | +287% | +552% | +426% | +69% | JANTS +2386% | Negatif reel faiz, bireysel yatırımcı akını |
| KİMYA | 2020-03 → 2021-05 | 284 | +197% | +385% | +272% | +63% | SASA +802% | SASA PTA yatırımı hikayesi |
| OTOMOTİV | 2021-06 → 2022-08 | 279 | +93% | +273% | +82% | +93% | ASUZU +2097% | Çip kıtlığında fiyatlama gücü, döviz geliri |
| BANKA | 2022-03 → 2022-09 | 112 | +94% | +202% | +141% | +55% | SKBNK +383% | 2022 negatif reel faiz, TÜFE'ye endeksli menkul kıymet (TÜFEX) kârı, KKM |
| HAVACILIK | 2022-03 → 2022-12 | 191 | +81% | +368% | +263% | +158% | THYAO +473% | Turizm toparlanması, %80 enflasyonda döviz geliri |
| YENİLENEBİLİR | 2022-08 → 2022-11 | 64 | +169% | +313% | +301% | +53% | SMRTG +758% | 2022 enerji krizi, güneş temalı halka arzlar |
| KOZA_ALTIN | 2022-09 → 2023-01 | 101 | +73% | +170% | +162% | +56% | TRALT +279% | Altın ve TL değer kaybı |
| SİGORTA | 2023-02 → 2024-06 | 331 | +339% | +808% | +430% | +107% | RAYSG +4344% | Faiz artışında yüksek fon getirisi; RAYSG düşük halka açıklık |
| SAVUNMA | 2023-05 → 2024-02 | 203 | +100% | +312% | +158% | +106% | SDTTR +431% | SDTTR halka arzı, savunma bütçesi ve ihracat, jeopolitik |
| ÇİMENTO | 2023-05 → 2023-12 | 140 | +88% | +215% | +113% | +67% | BSOKE +410% | Deprem sonrası yeniden yapım, fiyat artışları |
| ELK_EKİPMAN | 2023-02 → 03, 2023-06 → 07 (sert: 2023-05 → 09) | 20 / 19 / 93 | +43% / +46% / +55% | +46 / +80 / +166% | | | ASTOR, EUPWR | Trafo halka arzları (ASTOR 01/23, EUPWR 04/23), şebeke ve yenilenebilir yatırımı, küresel trafo kıtlığı. Halka arz tavan serisinin ilk 20 günü dışlandı. |
| BANKA | 2023-07 → 2023-12 | 102 | +32% | +53% | +42% | +16% | SKBNK +130% | Seçim sonrası ortodoks dönüş, Haziran 2023'ten itibaren faiz artışları, yabancı girişi |
| BANKA | 2024-03 → 2025-07 | 332 | +74% | +105% | +63% | +18% | GARAN +161% | %50'de faiz zirvesi, dezenflasyon ve indirim döngüsü beklentisi (Aralık 2024'te başladı); Mart 2025 şoku arada |
| HAVACILIK | 2023-09 → 2025-04 | 392 | +88% | +127% | +62% | +21% | CLEBI +297% | Rekor trafik, ucuz değerleme |
| GYO | 2024-04 → 2025-11 | 395 | +104% | +152% | +92% | +24% | SNGYO +267% | Enflasyona karşı koruma, net aktif değerine (NAD) göre iskonto kapanması |
| SAVUNMA | 2025-02 → 2025-06 | 82 | +45% | +34% | +23% | -7% | ASELS +78% | Avrupa'nın yeniden silahlanması (ReArm Europe), Mayıs 2025 Hindistan-Pakistan çatışması |
| KOZA_ALTIN | 2024-10 → 2025-04 | 131 | +64% | +73% | +54% | +5% | TRENJ +111% | Altın rallisi |
| KOZA_ALTIN | **2025-08 → 2026-01/02** | 119-143 | **+88% / +100%** | +126% / +151% | +112% / +132% | +20% | TRALT +163% | 2025-26 altın rekorları (>4.000 $/ons) |
| ELK_EKİPMAN | 2026-01/03 → 2026-06 | 60-98 | +53% | +60% / +79% | +53% / +68% | +5-16% | ASTOR +208%, EUPWR +147% | Hipotez: veri merkezi ve şebeke talebi, ABD trafo kıtlığı, ihracat (doğrulanmadı) |
| HOLDİNG | 2026-03 → 2026-10 (teyitsiz) | 140 | +35% | +25% | +12% | -7% | TKFEN +219% | Doğrulanmadı |
| RAFİNERİ | 2026-06 → 2026-10-30 (teyitsiz) | 92 | +56% | +14% | +6% | **-27%** | TUPRS +58% | Petrol yeniden 100 $ üstünde, fon krizi satışında savunmacı ve döviz bağlantılı kazanç |

**Dalga sonrası:** Kuralların dalgadaki pozisyonu, tepeden sonra kapanana kadar medyan **-%10-11 göreli** geri veriyor (`dalga_yakalama_ozet.csv`). Zigzag tanımı tepe sonrası ≥%15 göreli düşüşü zaten şart koştuğu için "dalga bitince geri verir" tespiti kısmen tanım gereği.

## 3. Yakalama kuralları

### 3.1 Izgara

- **Olay kuralları.** Her kümede bir durum makinesi çalışır; aynı anda en çok 3 küme slotu (her biri 1/3) dolar, mevcut pozisyon korunur, boş slot 126 günlük RS'ye göre doldurulur. Giriş ve çıkış seçenekleri:

  | Bileşen | Seçenekler |
  |---|---|
  | Giriş | `rs63` / `rs126` (R yeni 3 / 6 ay zirvesi), `rs63br` (63 g zirve + genişlik ≥%60), `br70` (üyelerin ≥%70'i 50 GHO üstü ve R>MA50), `dm6` / `dm3` (6 / 3 ay TL getiri > rf ve göreli getiri > 0) |
  | Çıkış | `ma50` (R<MA50), `rstr10` (R zirveden -%10), `tr15` (küme fiyatı zirveden -%15), `ma50\|tr15`, `br40`, `dm` |

  Toplam 18 giriş-çıkış çifti × filtre {yok, XU100>200 GHO} × {sepet, lider} = 72 yapılandırma.
- **Rotasyon.** 32 yapılandırmalı ızgara: skor {1, 3, 6 ay göreli getiri, bileşik ortalama} × K∈{2,3} × {haftalık, aylık} × mutlak filtre (3 ay TL > rf) × piyasa filtresi × {sepet, lider} × tampon {0, K+2}. Sonradan eklenen aileler: 12 ay ve 12-1 ay. Bunlar Moskowitz-Grinblatt sektör momentumunun standart tanımı, ancak tanı testinden **sonra** eklendi; veri gözetleme riski var. Toplam 384 rotasyon yapılandırması.

### 3.2 Aile medyanları (2012-01 → 2026-11-05, net)

| Aile (sepet) | CAGR | EW'ye göre | MaxDD | Sharpe | 2012-18 | 2019-23 | 2024-26 | 2024-26 rf'ye göre | USD CAGR |
|---|---|---|---|---|---|---|---|---|---|
| **Rot 12 ay (r252)** | **41,7%** | **+3,6** | -40% | **0,85** | 25,8% | 88,4% | 16,6% | -18,6 | 13,6% |
| **Rot 12-1 ay** | **41,5%** | **+3,5** | -40% | 0,82 | 25,4% | 85,0% | 17,3% | -18,0 | 13,4% |
| Rot 6 ay | 36,8% | 0,0 | -41% | 0,70 | 19,9% | 83,6% | 15,7% | -19,2 | 9,6% |
| Rot 1 ay | 36,5% | -0,2 | -41% | 0,71 | 23,3% | 76,5% | 14,3% | -20,2 | 9,4% |
| Rot bileşik | 35,5% | -1,0 | -49% | 0,65 | 22,3% | 83,3% | 6,0% | -25,9 | 8,6% |
| Rot 3 ay | 31,7% | -3,7 | -52% | 0,55 | 20,9% | 73,4% | 2,2% | -28,6 | 5,6% |
| Olay rs126 | 32,1% | -3,5 | -39% | 0,62 | 21,8% | 64,7% | 17,2% | -18,1 | 5,8% |
| Olay dm6 | 32,7% | -3,0 | -42% | 0,61 | 17,6% | 73,9% | 14,0% | -20,4 | 6,3% |
| Olay dm3 | 30,9% | -4,3 | -45% | 0,57 | 18,0% | 66,2% | 12,1% | -21,6 | 4,9% |
| Olay rs63 | 29,8% | -5,1 | -39% | 0,55 | 19,9% | 63,8% | 15,7% | -19,2 | 4,0% |
| Olay rs63br | 29,2% | -5,6 | -40% | 0,51 | 18,7% | 58,4% | 15,7% | -19,1 | 3,5% |
| Olay br70 | 28,6% | -6,0 | -43% | 0,47 | 19,6% | 57,2% | 13,9% | -20,4 | 3,1% |
| **Kıyas: EW 24 küme** | 36,8% | 0 | -37% | 0,77 | 18,6% | 88,9% | 10,6% | -22,7 | 9,6% |
| Kıyas: XU100 (fiyat) | 23,3% | -9,9 | -34% | 0,32 | 8,6% | 52,8% | 15,9% | -19,0 | -1,2% |
| Kıyas: TL rf | 17,6% | | 0 | | 9,8% | 15,9% | 43,1% | 0 | -5,8% |

**Lider hisse sürümü sepetten kötü:**

| Aile | Lider medyan CAGR | Sepet medyan CAGR | Lider MaxDD |
|---|---|---|---|
| Rot 12 ay | 35,2% | 41,7% | -58% |
| Rot 6 ay | 31,7% | 36,8% | -64% |
| Rot 1 ay | 28,1% | 36,5% | -80% |
| Olay br70 | 19,6% | 28,6% | -57% |

Lider seçimi 2024-26'da daha da kötü (-%15 ile -%22 CAGR'lı aileler var).

**XU100>200 GHO filtresi:**
- Olay kurallarında medyan CAGR'ı 2-6 puan artırıyor, MaxDD'yi düşürüyor. 2024-26'da 5-11 puan katkı (rs126: %5,6'dan %14,9'a).
- 12 ay rotasyonda tüm dönemde nötr (%38,8'e karşı %38,4), 2024-26'da +9 puan.

### 3.3 Olay kurallarının işlem istatistikleri

İşlemler slotsuz, tüm kümelerde, 2012+.

| Kural (sepet) | İşlem/yıl | Ort. gün | XU100'e göre isabet | rf'ye göre isabet | Ort. net/işlem | Medyan net | Yanlış başlangıç | Dalga yakalama | Portföy CAGR / DD / 2024-26 |
|---|---|---|---|---|---|---|---|---|---|
| rs126 → rstr10, filtreli | 32 | 40 | 53% | 47% | +8,2% | +0,5% | **36%** | 30% | 36,8% / -32% / 23,3% |
| rs126 → rstr10, filtresiz | 24 | 95 | 46% | 50% | +16,7% | +3,6% | 41% | 42% | 43,7% / -43% / 15,4% |
| rs63 → tr15, filtresiz | 27 | 123 | 51% | 44% | +24,9% | +3,6% | 45% | **63%** | 29,5% / -40% / 5,4% |
| rs63 → ma50, filtresiz | 52 | 38 | 42% | 45% | +6,5% | +0,4% | 51% | 45% | 29,0% / -45% / 10,5% |
| dm6 → tr15, filtreli | 71 | 41 | 49% | 41% | +7,7% | -0,5% | 53% | 59% | 31,8% / -42% / 11,6% |
| br70 → br40, filtresiz | 65 | 40 | 49% | 39% | +9,5% | -0,3% | 55% | 59% | 33,3% / -40% / 15,7% |
| 72 olay yapılandırmasının medyanı | | 40 | 46% | | +9,3% | +0,1% | 47% | 47% | 29,5% (sepet 30,5%) |

Yanlış başlangıç oranı giriş türüne göre: rs126 %37, rs63 %44, br70 %54, dm3 %55, dm6 %57. 6 aylık RS zirvesi en az yanlış başlangıç veren giriş, ama yakalama payı da en düşük (%35).

**Dalga bazında yakalama (167 dalga) ve sızıntı:**

| Kural | Ort. yakalama | Hiç girmedi | Giriş gecikmesi (medyan gün) | Tepeden sonra çıkış (gün) | Dalga içi kazancın payı | Dalga dışı kaybın payı | Pozisyon günlerinin dalga payı |
|---|---|---|---|---|---|---|---|
| A: rot 12 ay K3 aylık | 23% | 53% | 39 | 68 | 26% | 21% | 54% |
| E: rs126 → rstr10, filtreli | 30% | 17% | 55 | 13 | 35% | 25% | 54% |
| F: rs63 → tr15 | **63%** | 5% | 23 | 29 | 67% | **55%** | 40% |
| G: dm6 → tr15, filtreli | 59% | 10% | 15 | 21 | 61% | 48% | 38% |

- Taban oranda küme-günlerin %31'i dalga günü. Sinyaller pozisyon günlerinde bunu %38-54'e çıkarıyor, yani seçicilik var.
- Ama yüksek yakalama dalga dışı kayıpla birlikte geliyor. F dalga hareketinin 2/3'ünü alıyor, dalga dışı kayıpların da yarısından fazlasını yiyor. Sonuç: net getiri, kümeleri her zaman tutmaya yakın.

### 3.4 Sağlamlık

- **İleri yürüyüş.** 2012-18 Sharpe sırası ile 2019-23 CAGR sırası arasında Spearman korelasyonu **-0,12**; 2012-18 CAGR ile 2024-26 CAGR arasında 0,25. 2012-18'in en iyi 10 yapılandırması 2019-23'te EW'yi yılda -9,1 puan, tüm yapılandırmaların medyanı -4,1 puan geride kaldı. **Izgaranın en iyisini seçmek işe yaramıyor; aile medyanına bakılmalı.**
- **EW'yi yenen yapılandırma payı:** 2012-18'de %62, 2019-23'te %33, 2024-26'da %36.
- **Maliyet %0,50/yön:** 12 ay rotasyon %38,4'ten %35,2'ye (düşük devir, yılda ~3 tam devir). 1 ay rotasyon %34,5'ten %24,5'e. Olay kuralları 4-5 puan kaybediyor.
- **Gecikme 0 (sinyal günü kapanışı):** +0 ile +2 puan. Sinyaller ertesi güne kaymaya duyarsız.

### 3.5 Tanı testleri (`calis_tani.py`)

**Kümeler arası momentum, aylık sıra-IC (ileri 21 gün, EW'ye göre):**

| Bakış süresi | IC | t | Pozitif ay oranı |
|---|---|---|---|
| 1 ay | 0,025 | 1,3 | |
| 3 ay | 0,026 | 1,3 | |
| 6 ay | 0,047 | 2,4 | |
| **12 ay** | **0,065** | **3,2** | 61% |

- 12 aya göre ilk 3 küme, EW'yi brüt yılda ~+10 puan geçiyor; son 3 küme yılda -11 puan geride. "Kaybeden kaybetmeye devam ediyor" tarafı en az kazananlar kadar güçlü.
- 12 ay IC dönemlere göre: 2024-26 0,10 (t 2,2), 2012-18 0,05.

**Olay çalışması (taze sinyal, log, EW'ye göre):**
- 126 gün RS kırılımı + XU100>200 GHO: 21 gün içinde +%1,1 (t 2,4). Koşulsuz kıyas -%0,2. Etki 63 günde +%0,6, 126 günde -%0,1'e iniyor.
- Filtresiz 126 gün kırılımı: 21 günde +%0,8 (t 1,9).
- DM6 girişi 63 günde -%1,6 (t -2,1): **ikili momentum girişi geç kalıyor**.
- Genişlik ≥%70: 0 ile negatif arası.
- Sonuç: Kırılımın kendisi kısa vadede zayıf bir avantaj taşıyor. Asıl bilgi 12 aylık sıralamada.

### 3.6 Hayatta kalan yanlılığı kontrolü: sektör endeksi evreni

BIST sektör endekslerinin bileşimi tarihsel olarak değişiyor, bu yüzden bu evrende üye seçimi yanlılığı yok. Endeksler fiyat endeksi, kıyas da fiyat endeksi.

- **EW sektör kıyası:** 22 endeks CAGR %28,1; mikro sektörler XFINK ve XSPOR hariç %28,5. XU100 %23,3.
- **12 ay rotasyon medyanı:** 22 endekste %34,8 (EW'ye göre +5,2). XFINK/XSPOR hariç %32,4 (+3,0); aylık sürümde %33,5 (+3,9). XFINK/XSPOR hariç yapılandırmaların %66'sı EW'yi yeniyor.
- **2024-26 uyarısı:** Hariç tutulmamış evrende 2024-26 getirisi %44 ile çok güçlü görünüyor. Bu, XFINK'in 2024-25'teki +%444'lük ve 2025-26'daki +%223'lük dalgasından geliyor ve işlenebilir değil. Hariç tutunca 2024-26 %20, rf'nin 16 puan altında.
- **Yanlılık tahmini:** Küme EW %36,8, sektör EW + ~%3 temettü ≈ %31,5. Küme evreninde **yılda ~5 puanlık seçim/hayatta kalan primi** olduğu tahmin ediliyor. Kuralların EW'ye göre farkı bu yanlılıktan büyük ölçüde arınık; XU100'e göre farkı ise şişkin.

### 3.7 Seçilen kurallar: yıllık tablo ve VİOP hedge'li sürüm

- **A:** 12 ay RS, en güçlü 3 küme, aylık, sepet, filtresiz. Ailenin örneklem içi en iyisi; aile medyanı %41,7.
- **B:** A + 3 ay TL > rf + XU100>200 GHO.
- **E:** rs126 → rstr10 olay kuralı, filtreli.
- **_H sütunları:** Aynı portföyün yanında beta=1 XU030 vadeli kısa pozisyon. Getiri + maruziyet × (rf - %3 temettü - XU100) - yılda %0,6 devir maliyeti.

| Yıl | rf | XU100 | EW | A | A_H | B | B_H | E | E_H |
|---|---|---|---|---|---|---|---|---|---|
| 2012 | 8,1 | 52,6 | 50,3 | 88,4 | 27,4 | 49,9 | 34,4 | 67,5 | 34,9 |
| 2013 | 6,0 | -13,3 | -4,0 | 5,1 | 24,2 | 15,7 | 21,5 | 17,4 | 18,9 |
| 2014 | 9,0 | 26,4 | 47,2 | 62,2 | 33,2 | 43,3 | 28,0 | 41,5 | 23,0 |
| 2015 | 8,3 | -16,3 | 1,7 | 6,7 | 33,0 | -4,8 | 1,4 | 5,0 | 25,4 |
| 2016 | 8,4 | 8,9 | 18,8 | 15,7 | 10,3 | -2,5 | 8,5 | -13,0 | 2,2 |
| 2017 | 11,5 | 47,6 | 58,6 | 114,4 | 56,1 | 64,4 | 39,7 | 38,6 | 7,5 |
| 2018 | 17,6 | -20,9 | -19,0 | -1,9 | 41,0 | 19,6 | 32,1 | 14,3 | 23,9 |
| 2019 | 20,2 | 25,4 | 77,4 | 91,2 | 74,6 | 54,1 | 58,0 | 39,7 | 53,9 |
| 2020 | 10,7 | 29,1 | 98,1 | 159,5 | 117,7 | 52,9 | 63,4 | 38,9 | 29,4 |
| 2021 | 17,5 | 25,8 | 33,9 | 55,7 | 39,7 | 71,2 | 56,1 | 35,7 | 29,2 |
| 2022 | 12,9 | 196,6 | 251,4 | 283,2 | 38,7 | 281,3 | 43,9 | 311,2 | 46,9 |
| 2023 | 18,0 | 35,6 | 41,7 | 82,7 | 53,2 | 52,2 | 40,9 | 30,9 | 27,2 |
| 2024 | 48,1 | 31,6 | 41,8 | 44,9 | 55,8 | 40,3 | 32,3 | 43,1 | 60,8 |
| 2025 | 43,2 | 14,6 | 5,2 | -0,2 | 20,1 | 36,2 | 39,8 | 11,4 | 26,8 |
| 2026 YTD | 29,8 | 0,6 | -10,9 | -3,0 | 20,2 | 0,8 | 22,0 | 13,3 | 7,4 |
| **CAGR 2012-26** | 17,6 | 23,3 | 36,8 | **54,7** | 41,7 | 43,3 | 34,3 | 36,8 | 27,3 |
| **CAGR 2024-26** | **43,1** | 15,9 | 10,6 | 12,7 | 33,2 | 26,1 | 33,4 | 23,3 | 32,0 |
| MaxDD | | -34 | -37 | -39 | -32 | -39 | -30 | -32 | -23 |

USD CAGR: A 2012-26 %24,0 (hedge'li %13,5), 2024-26 -%6,2 (hedge'li +%10,8). B 2012-26 %14,9, 2024-26 %4,9 (hedge'li %10,9).

**A'nın tutma dönemleri:**
- Yılda 8,9 dönem, medyan 42 gün. Kullanıcının swing ufkuna uyuyor.
- Dönemlerin %56'sı XU100'ü, %61'i rf'yi yeniyor. Ortalama göreli +%10,8, medyan +%1,1.
- En iyi %10'luk dönem, pozitif göreli katkının %66'sını veriyor.
- En sık tutulan kümeler: KOZA, SAVUNMA, TEKNOLOJİ, HAVACILIK, GÜBRE.

**Hedge mantığı:**
- Uzun küme + kısa XU030 vadeli ≈ rf - temettü + göreli getiri. Vadeli fiyatı TL faizini taşıdığı için kısa vadeli taraf rf kazandırır, eşik kendiliğinden rf olur.
- 2012-26'da A_H %41,7 (rf'ye göre yılda +20 puan). Ama bunun yaklaşık 7 puanı, yanlılık içeren EW primi.
- 2024-26'da küme evreni XU100'ün altında kaldı: EW %10,6, XU100 %15,9. Bu yüzden hedge'li sürümler de rf'nin ~10 puan altında: %33'e karşı %43.
- Teminat (vadeli kontrat başlangıç teminatı ~%15) ve XU030/XU100 baz farkı modellenmedi.

## 4. En sağlam yakalama kuralı (önerilen tanım)

**"12 ay göreli güç, ilk 3 küme, ay sonu".** Her ayın son işlem günü kapanışında:

1. Uygun her küme için skor hesaplanır: `R_t / R_{t-252} - 1` (R = küme EW endeksi / XU100).
2. İlk 3 küme eşit ağırlıkla sepet olarak alınır. Küme içi eşit ağırlık; pratikte VİOP'lu üyelerle de kurulabilir.
3. İşlem ertesi gün kapanışında yapılır.
4. Ay sonunda ilk 3'ten düşen küme satılır. Ara stop yok; çıkış = RS sıralama kaybı.
5. İsteğe bağlı: XU100>200 GHO ve küme 3 ay TL > rf değilse ilgili slot nakit (B).

**Beklenti.** Aile medyanı CAGR ~%42, EW'ye göre yılda +3-5 puan, MaxDD ~-%40. Sektör endeksleriyle teyit EW'ye göre +3 puan. 2024-26 gibi yüksek reel faiz rejiminde spot uzun pozisyon TL rf'yi geçmedi: **2024-26 boyunca 456 yapılandırmanın hiçbiri geçmedi.**

**Kullanım önerisi:**
- (i) Kümeyi seçme filtresi olarak kullan: son 3'ten uzak dur, ilk 3'te ara.
- (ii) Rejim kötüyken (XU100<200 GHO, yüksek reel faiz) ya nakit ya da VİOP'ta XU030 kısa ile göreli dalga oyna.
- (iii) Pozisyonu dalga boyunca taşı: dar stop koyma. Getiri, az sayıda büyük dalgadan geliyor.

## 5. Güncel durum (05.11.2026 kapanışı; son sütun 06.11 gün içi göreli değişim)

**Piyasa:**
- XU100 11.333 (06.11 gün içi 11.297). 200 GHO 13.572, 50 GHO 12.691. 252 günlük zirveden -%25,1.
- 31.08 → 30.10 arasında -%24,9: 2008'den beri en sert iki aylık düşüş.
- Haber kaynaklarına göre sürücüler: Pusula/Tera/Atlas fonlarında ödeme krizi ve SPK'nın 131 fonu tasfiye kararı (17.09), 15.10'da MSCI'ın Türkiye endeks değişikliklerini dondurması, petrolün 100 $ üstü. Satış, fonların tuttuğu küçük ve orta ölçekli hisselerde yoğun; bankalar alımla öne çıktı.
- **Piyasa filtresi kapalı. DM6 hiçbir kümede açık değil.** Kümelerin hiçbirinde 6 ay TL getiri rf'yi geçmiyor; 63 günde TL bazında yalnız BANKA pozitif (+%1,1).

| Sıra (12 ay) | Küme | rel 1 ay | rel 3 ay | rel 6 ay | rel 12 ay | TL 3 ay | R/MA50 | 126 g RS zirvesinden gün | Genişlik 50 | Durum | 06.11 gün içi |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | RAFİNERİ | -3,6 | +14,5 | +17,8 | +26,5 | -5,8 | -3,4 | 4 | 0% | **Dönüyor** (dalga tepesi 30.10) | -2,0 |
| 2 | HOLDİNG | +1,4 | +13,3 | +29,7 | +23,9 | -6,8 | +5,7 | 17 | 0% | **RS yükseliş** | -0,2 |
| 3 | KOZA_ALTIN | -9,7 | -9,2 | +15,6 | +18,9 | -25,4 | -7,0 | 28 | 0% | Dönüyor (12 ay RS zirvesinden -%23) | -0,1 |
| 4 | PERAKENDE | -4,9 | +6,2 | +20,7 | +17,6 | -12,7 | -1,2 | 15 | 0% | Dönüyor | -1,8 |
| 5 | **BANKA** | +6,8 | **+22,9** | +17,0 | +3,9 | +1,1 | +9,3 | **0** | 44% | **KIRILIM** (126 g RS zirvesi) | +0,5 |
| 6 | ÇELİK | -2,9 | -1,9 | +16,9 | +3,3 | -19,3 | -1,5 | 49 | 0% | Dönüyor | -0,7 |
| 7 | GYO | -1,3 | +11,1 | +19,9 | -1,7 | -8,6 | +3,9 | 20 | 14% | RS yükseliş | -0,5 |
| 8 | TELEKOM | +0,5 | +8,3 | +1,8 | -5,0 | -10,9 | +5,5 | 12 | 0% | RS yükseliş | -1,7 |
| 9 | SAĞLIK | +2,1 | -7,0 | +10,2 | -8,5 | -23,5 | -6,5 | 39 | 20% | Dönüyor | -0,8 |
| 10 | ELK_ÜRETİM | -2,7 | -6,2 | -7,0 | -12,5 | -22,8 | -1,5 | 107 | 17% | Düşüş | -1,1 |
| 11 | GIDA | -1,9 | +1,7 | +0,2 | -12,9 | -16,4 | +2,1 | 121 | 0% | Zayıf RS yükseliş | -0,3 |
| 12 | **HAVACILIK** | +9,4 | **+16,1** | +12,2 | -13,2 | -4,5 | +13,0 | **0** | 50% | **KIRILIM** (126 g RS zirvesi) | 0,0 |
| 13 | TEKNOLOJİ | -10,4 | -14,5 | -7,8 | -15,6 | -29,7 | -6,3 | 110 | 0% | Düşüş | +0,3 |
| 14 | OTOMOTİV | -2,9 | +0,6 | -7,2 | -22,8 | -17,3 | -0,8 | 107 | 0% | Düşüş | +2,4 |
| 15 | SAVUNMA | -8,4 | -9,7 | -15,2 | -24,7 | -25,8 | -6,4 | 110 | 0% | Düşüş | -0,5 |
| 16 | SİGORTA | -4,5 | -8,2 | -10,1 | -27,0 | -24,5 | -3,0 | 103 | 0% | Düşüş | -1,6 |
| 17 | ÇİMENTO | +1,6 | -20,3 | -25,0 | -27,8 | -34,5 | -3,7 | 112 | 22% | Düşüş | +0,3 |
| 18 | ELK_EKİPMAN | -4,8 | -36,1 | -30,3 | -28,2 | -47,4 | -10,6 | 109 | 20% | Düşüş | +0,5 |
| 19 | OTO_YAN | -5,2 | -2,7 | -3,4 | -34,1 | -19,9 | -2,7 | 112 | 0% | Düşüş | -0,2 |
| 20 | YENİLENEBİLİR | -8,8 | -35,0 | -25,9 | -34,4 | -46,5 | -11,8 | 110 | 0% | Düşüş | +1,0 |
| 21 | GÜBRE | -14,8 | -17,7 | -30,0 | -34,8 | -32,3 | -12,3 | 121 | 0% | Düşüş | -1,2 |
| 22 | KİMYA | -4,4 | -19,8 | -22,5 | -35,8 | -34,0 | -5,5 | 122 | 0% | Düşüş | -1,7 |
| 23 | BEYAZ_EŞYA | -9,8 | -22,2 | -31,1 | -55,0 | -36,0 | -11,7 | 121 | 0% | Düşüş | -2,8 |
| 24 | CAM_SERAMİK | -6,1 | -28,3 | -34,8 | -59,7 | -41,0 | -11,4 | 111 | 0% | Düşüş | -2,6 |

Göreli ve TL değerler yüzde, rel = XU100'e göre.

**Kuralların bugünkü seçimi** (bir sonraki ay sonu yeniden dengelemesi 30.11):

| Kural | Seçim |
|---|---|
| A (12 ay) | RAFİNERİ, HOLDİNG, KOZA_ALTIN (Ekim sonundan beri tutuluyor) |
| 12-1 ay | KOZA_ALTIN, RAFİNERİ, PERAKENDE |
| 6 ay | HOLDİNG, PERAKENDE, GYO |
| Bileşik (1/3/6 ay) | BANKA, HOLDİNG, HAVACILIK |
| B ve filtreli olay kuralları | **Nakit** |

**Dikkat:** Düşen piyasada RS liderliği büyük ölçüde **düşük beta ve savunmacılık** demek. RAFİNERİ'nin betası 0,55. Klasik bir momentum dalgası değil.

**Odak üyeler** (rel 3 ay XU100'e göre; V = VİOP):

| Küme | Üyeler |
|---|---|
| BANKA | GARAN V +%35,9 (50 ve 200 GHO üstü), HALKB V +%31,7, YKBNK V +%30,5, ISCTR V +%28,4, VAKBN V +%25,8, AKBNK V +%21,2, TSKB V +%12,0 |
| HAVACILIK | TAVHL V +%29,3 (200 GHO üstü), THYAO V +%17,9, PGSUS V +%10,8 |
| HOLDİNG | KCHOL V +%23,9, ALARK V +%21,0, SAHOL V +%17,5, TKFEN V +%14,6 (12 ay +%143) |
| RAFİNERİ | TUPRS V +%26,9 (12 ay +%87, 200 GHO üstü), PETKM V +%10,8 |
| KOZA | TRALT V -%10,8 (12 ay +%43), TRMET V -%4,9 |
| PERAKENDE | SOKM V +%26,4, BIMAS V +%17,1, MGROS V -%15,9 |

Tam tablo: `cikti/guncel_uye_tablosu.csv`.

**Boyutlama için korelasyon haritası (son 250 gün):**

- **Blok 1, büyük sermaye ve finans:** BANKA, HOLDİNG, HAVACILIK, TELEKOM ve GYO. Günlük getiri korelasyonu 0,70-0,79, fazla getiri korelasyonu 0,2-0,4. BANKA ve HAVACILIK kırılımlarını birlikte almak tek bir beta bahsi. Toplam risk tek tema gibi sınırlanmalı.
- **Blok 2, küçük-orta büyüme ve tema:** ELK_EKİPMAN, YENİLENEBİLİR, TEKNOLOJİ ve ELK_ÜRETİM. Fazla getiri korelasyonu 0,44-0,57, günlük korelasyon 0,62-0,75. Fon krizi satışının merkezi.
- **Blok 3, sanayi:** ÇİMENTO, OTO_YAN, KİMYA, CAM, BEYAZ_EŞYA ve SAĞLIK. Fazla getiri korelasyonu 0,38-0,45.
- **Ayrıştırıcılar:** RAFİNERİ (diğerleriyle günlük korelasyon 0,14-0,37; fazla getiri korelasyonu BANKA ile -0,42, HAVACILIK ile -0,31), SAVUNMA (BANKA ile -0,35), KOZA_ALTIN (fazla getiri korelasyonu ~0).
- **Oynaklık ve beta (1 yıl):** KOZA %52 / 1,27, ELK_EKİPMAN %48 / 1,21, BANKA %34 / 1,13, RAFİNERİ %31 / 0,55, HOLDİNG %26 / 0,91. Ters oynaklıkla KOZA ve ELK_EKİPMAN yarım boyut alır.
- **Örnek bir küme çifti** (hesaplanan korelasyonlar, test edilmiş bir kural değil): uzun BANKA veya HAVACILIK + uzun RAFİNERİ, iki ayrı bacak olarak düşük göreli korelasyonlu bir çift oluşturur. Toplam beta ise XU030 vadeliyle ayarlanmalı.

## 6. Uyarılar

1. **Hayatta kalan ve seçim yanlılığı.** Küme evreninde yılda ~5 puan tahmin ediliyor (§3.6). XU100'e göre farklar şişkin, EW'ye göre farklar daha güvenilir.
2. **Temettü uyumsuzluğu.** XU100 fiyat endeksi, kümeler toplam getiri. Yılda ~3 puan fark.
3. **Basitleştirilmiş varsayımlar:**
   - Günlük yeniden dengelenen EW sepet; küme içi dengeleme maliyeti yok.
   - Küçük üyelerde (RAYSG, JANTS, KONTR, SMRTG) makas ve kapasite %0,25/yönden kötü olabilir.
   - Vergi yok.
4. **Elle kurulmuş rf.** 2021-23'te gerçek TL getirisi politika faizinin üstündeydi. Bu yıllarda rf'ye göre farklar şişkin olabilir.
5. **Dalga tanımına dair sınırlar:**
   - Dalga sayımı ex post bir tanım.
   - 2-3 üyeli kümeler (KOZA, TELEKOM, GÜBRE, BEYAZ_EŞYA) dalga sayısını şişiriyor.
   - Halka arz tavan serileri (ASTOR, EUPWR, SDTTR) ilk 20 gün dışlandığı için kısmen sayılmadı.
   - KOZA grubunun 2015-16 TMSF dönemi verisinde sıçramalar var.
6. **Çoklu test.** 456 küme ve 192 sektör yapılandırması denendi. "En iyi" rakamlar (A %54,7) iyimser; ileri yürüyüşte en iyiler kalıcı değil. 12 ay ailesi tanı testinden sonra eklendi; literatürde önceden tanımlı olsa da veri gözetleme riski taşıyor.
7. **Rejim.** 2024-26'da hiçbir uzun küme kuralı rf'yi geçmedi. Eylül-Ekim 2026 fon krizi küçük sermaye kümelerinde zorunlu satış yarattı; RS sıralaması şu an savunmacılığı ölçüyor. Kriz sonrası toparlanmada en sert düşenler (Blok 2) kısa vadede tepki verebilir. Bu test edilmedi; 1 ay IC'si zayıf pozitif, kısa vadeli tersine dönüş kanıtı yok.
8. **Güncel tablonun kapsamı.** 05.11 kapanışına dayanıyor; 06.11 gün içi fiyat sadece bilgi amaçlı. Haber sürücüleri web kaynaklı ve doğrulanmadı.

**Kaynaklar (yalnız güncel piyasa bağlamı için):**
- [Endeks24: BIST 100 iki ayda %25 düştü](https://www.endeks24.com/bist-100-iki-ayda-yuzde-25-dustu)
- [Midas: Borsa neden düşüyor (16.10.2026)](https://www.getmidas.com/midasin-kulaklari-ow/borsa-neden-dusuyor-bist-100de-dususun-nedenleri-16-ekim-2026-p-821874)
- [Sözcü: devre kesici](https://www.sozcu.com.tr/borsa-cakildi-yuzde-5-in-uzerinde-geriledi-p358745)
- [Evrensel: Pusula'nın fonu çöktü](https://www.evrensel.net/haber/6000741/pusulanin-fonu-coktu-bist-100-yuzde-6-deger-kaybetti)
- [Medyascope: fon krizi nasıl başladı](https://medyascope.tv/2026/10/01/fon-krizi-nasil-basladi-nasil-oldu-ne-yapilabilirdi/)
- [Ekonomi Gazetesi: 10 soruda fon krizi](https://www.ekonomigazetesi.com/ekonomi/10-soruda-fon-krizi-ne-oldu-ne-olacak-90966)

## 7. Dosyalar

**Kod** (`hesaplar/dalga_bist/`):

| Dosya | İçerik |
|---|---|
| `kumeler.py` | Küme tanımları, VİOP listesi |
| `fetch.py` | ChartData indirici |
| `veri.py` | Panel, temizlik, rf |
| `dalga.py` | Zigzag dalga tanımı |
| `motor.py` | Olay ve rotasyon backtest motoru, ölçüler |
| `calis_dalga.py` | Dalga listesi |
| `calis_test.py` | Ana ızgara; COST, LAG ve SUF ortam değişkenleri |
| `calis_rot_ek.py` | 12 ay ve 12-1 ay rotasyon |
| `calis_tani.py` | IC ve olay çalışması |
| `calis_ozet.py` | Aile medyanları, ileri yürüyüş, duyarlılık |
| `calis_sektor.py` | Sektör endeksi kontrolü; EXCL ortam değişkeni |
| `calis_secilen.py` | Yıllık tablo, hedge, tutma dönemleri |
| `calis_ornek.py` | Dalga bazında yakalama, sızıntı |
| `calis_guncel.py` | Güncel durum, korelasyon |

**Çıktılar** (`cikti/`):

| Konu | Dosyalar |
|---|---|
| Dalgalar | `dalgalar_taban.csv`, `dalgalar_sert.csv`, `dalga_yakalama*.csv`, `dalga_sizinti.csv` |
| Izgaralar | `izgara_olay*.csv`, `izgara_rot*.csv`, `izgara_sektor_rot*.csv` |
| Özetler | `ozet_tum_kurallar.csv`, `ozet_aile_medyan.csv`, `secilen_yillik.csv`, `tutma_*.csv`, `tani_*.csv` |
| Güncel durum | `guncel_kume_tablosu.csv`, `guncel_uye_tablosu.csv`, `guncel_korelasyon_*.csv`, `guncel_oynaklik_beta.csv` |

**Ham veri ve günlük seriler:** `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/dalga_bist/`. Repoda değil.
