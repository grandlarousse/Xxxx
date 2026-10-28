# BIST VİOP Yatırım Komitesi — 5 Ajanlı Tartışma ve Çapraz Kontrol

**Tarih:** 28 Ekim 2026 (yarım gün; 29 Ekim tatil). **Fiyatlar:** 27–28.10 kapanış/son işlem. 30.10 açılışından önce hepsi yeniden kontrol edilmeli.
**Yöntem:** 5 uzman ajan (MAKRO, ENDEKS, HİSSE, OPSİYON, ŞEYTAN). 1. turda her biri bağımsız fikir üretti. 2. turda her ajan diğer dördünün dosyasını okudu, olguları ve hesapları bağımsız doğruladı, oy verdi ve kendi fikrini revize etti. Koordinatör kalan çelişkileri ayrıca kontrol etti.
**Ham dosyalar:** `ajanlar/` (r1_*, r2_*, 00_baseline). **Hesap betikleri:** `hesaplar/`.

> Bu rapor yatırım tavsiyesi değildir. Kaldıraçlı türev ürünlerde sermayenin tamamı ve teminat tamamlama yoluyla fazlası kaybedilebilir. Olasılıkların neredeyse tamamı öznel tahmindir.

---

## 1. Net cevap

**Belirgin bir yön avantajı yok.** Komite "çok düştü, döner" tezini veriyle reddetti. Short tezinin de "bedava baz kazancı" gerekçesini geçersiz saydı. Geriye kalan avantajlar küçük ve koşullu. Önerilen portföy şunlardan oluşuyor: tanımlı riskli opsiyonlar, düşük kaldıraçlı TL carry ve yalnızca belirli tetiklerle açılacak pozisyonlar. **Toplam stop bazlı risk sermayenin ~%2,2–2,6'sı.** Çoğu pozisyon 30.10'dan önce açılmaz, bir kısmı hiç tetiklenmeyebilir.

| # | Pozisyon | Koşul (sağlanmazsa işlem yok) | Boyut (10 mn TL sermaye) | Stop/prim riski | Komite oyu* |
|---|---|---|---|---|---|
| 1 | **Long straddle:** O_XU030E1226C14500 + P14500 (Aralık, Avrupa tipi, nakdi) | 2–6 Kasım arası, makas dahil toplam prim **≤800 puan** (IV ≤ ~%17). Önce 1 lotla derinlik testi | 5 straddle (azami 10) | %0,4–0,8 | 4/4 EVET, ort. **6,25** |
| 2 | **Short F_USDTRY1226** (TL carry) | 30.10'da TCMB gösterge kurunun ortası ≤50,00 ve vadeli ≤52,70; yarısı 30.10'da, yarısı 3.11 TÜFE sonrası. Stop: uzlaşma ≥53,20 | 35–40 kontrat (1 mn TL başına 3,5–4; 1. turdaki 6 değil) | %0,25–0,33 (+%12 şokta ~%2,2–2,5) | 4/4 KOŞULLU/EVET, ort. **5,75** |
| 3 | **"Ralliyi sat" kovası** (ENDEKS + ŞEYTAN birleşik; tek kova, ≤%1) | Rallide giriş, 13.11'e kadar dolmazsa iptal. Ralli geniş tabanlıysa girilmez (XBANK, XU030'u 2 puandan fazla geçiyor **ve** yabancı alımı >200 mn $) | (a) **P14000/P13000 put spread** ≤200 puan, spot ≥14.200'de, 25 adet → %0,5<br>(b) **Short F_XU0301226**, kademeler 14.900 / 15.075, **gün içi** stop 15.550, hedefler 14.100 / 13.700, en geç 04.12 → ~5–6 kontrat, ~%0,3 | ≤%1,0 | Vadeli short 4/4 KOŞULLU, ort. **5,0**. Put spread 2. turda doğdu, diğer ajanlarca oylanmadı |
| 4 | **Long F_GARAN1126 / Short F_YKBNK1126** (hedge 0,85; Kasım vadesi, Aralık vadesi likit değil) | Garanti 3Ç net kârı ≥30 mlr TL (28.10 akşamı açıklanacak, bu rapor yazılırken açıklanmamıştı). %50 30.10'da, %50 YKBNK sonucundan sonra 4.11'de. Oran stopu 3,52, hedef 3,90, en geç 26.11 | Yarım–tam boy: 68/210 – 135/420 kontrat | %0,5–0,7 (en kötü gap ~%2–3,3) | 4/4 KOŞULLU, ort. **5,0** |
| — | Sigorta: long **C14500/C15500 call spread** ≤340 (veya sadece C15500 ≤100) | Yalnızca 3. kalemdeki vadeli short dolarsa | 14 adet | %0,48 | 4/4 KOŞULLU, ort. 4,0 |

\*Oy: kendi fikri hariç diğer 4 ajanın 2. tur oyları, 1–10 ölçeğinde.

**Elenen fikirler (4/4 HAYIR ya da sahibi geri çekti):**
- Dip testinde long F_XU030 (ENDEKS-2): maliyet sonrası beklenen değer ≈0.
- SAHOL/AKBNK pair (HİSSE-2): SAHOL tasfiyedeki fonlarda en sık tutulan BIST 30 payı ve taşıma maliyeti beklenen kârı yiyor.
- Makro kapılı long F_XU030 (MAKRO-2): hedefi spotta +%11–15 gerektiriyor; tetiklenirse call spread'e dönüştürülecek.

---

## 2. Neden: komitenin vardığı beş hüküm

1. **Satış baskısı BIST 30'da büyük ölçüde geride; asıl yük küçük ve orta hisselerde.**
   - Ölçü: XU030/XU100 oranı 1,19'dan 1,25'e çıktı.
   - Tasfiyedeki fonların likit hisse yükü ~32–40 mlr TL. Likit olmayan 146,5 mlr TL'nin ~%45'i ancak 60+ işlem gününde satılabilir (Gedik).
   - Yabancı çıkışı yavaşlıyor: −190, −248, −89 mn $; bu, stokun ~%1,6'sı.
2. **"Çok düştü, yükselir" kanıtlanamadı (ENDEKS):**
   - 22 benzer olayda (30 günde ≥%20 düşüş) 63 günlük medyan getiri **+%2,9**. Koşulsuz medyan +%5,5'in altında, %50'si pozitif.
   - Bu rakam Aralık vadelisinin ~%4,9'luk taşımasını karşılamıyor.
   - Bulgu yönteme duyarlı: başka bir tasarımda 21 günlük getiri +%5,9 çıkıyor.
3. **Vadeli baz bir "avantaj" değil, TL faizinin kendisi:**
   - Long vadeli ile nakit arasında seçim yapan için başabaş **spot +%4,9**. Vadeli ile spot hisse arasında seçim yapan için vadeli **~%1,3–1,4 ucuz**.
   - Bu iki ifade çelişmiyor: farklı kararlara ait (MAKRO ve OPSİYON uzlaştırdı).
   - Zımni finansman %28'dir. 2026 boyunca %24–33 bandında kaldı, yani yapısal ve bir panik sinyali değil.
4. **Opsiyonlarda işlem fiyatları ucuz görünüyor.**
   - Gerçekleşen vol: RV20 %27, RV60 %28, GARCH 1 aylık %32.
   - Uzlaşma fiyatlarının ima ettiği IV ~%24. Ama 27.10'da Aralık straddle gün içinde ~756'dan 510'a indi (IV %17 → %11). Muhtemelen tek bir yapılandırılmış vol satış akışı (P15500 açık pozisyonu 1,6 binden 25 bine çıktı).
   - Vol satmak için gerekçe yok; tanımlı riskli opsiyon almak için var. Bu avantaj yalnızca ≤800 puandan dolum olursa geçerli.
5. **TL carry yapısal ama negatif çarpık (MAKRO, düzeltilmiş hali):**
   - Aralık kontratı yıllık ~%31 kur artışı fiyatlıyor. 2026'da gerçekleşen hız ~%19–20, son 3 haftada ~%24.
   - Ortodoks politika döneminde (Ağu 2023–Ağu 2026, 778 kayan pencere) 64 günlük kısa vadeli pozisyon ortalama +%2,6 getirdi, %88 oranında pozitif kapattı.
   - Ancak 2018, 2021 ve 2023 şoklarında stopsuz kayıp −%19 ile −%31 arasıydı. Şoktan bir gün önce girilmiş olsaydı gap kaybı −%22,6 olurdu.
   - Revize beklenen değer kontrat başına ~+230 TL (64 günde nominalin ~%0,44'ü). 2018 tipi bir gap'in olasılığı %4'ü aşarsa beklenen değer negatife döner.

---

## 3. Kanıt ve veri (doğrulanmış çekirdek)

| Kalem | Değer | Doğrulama |
|---|---|---|
| Politika faizi | %37 → **%36** (22.10), koridor %34,5–39 | TCMB karar metni, birden çok kaynak |
| Eylül TÜFE | yıllık **%29,73**, aylık %1,84 | TÜİK, birden çok kaynak |
| Ekim anketi | yıl sonu TÜFE %29,63; yıl sonu faiz %35; yıl sonu USDTRY 51,55 | TCMB anketi (Foreks) |
| Reel faiz | ex-post ~%4,8; ex-ante ~**%9,8** | hesap |
| Fed | 16.09.2026'da **+25 bp → %3,75–4,00** (oylama 12–0); sonraki FOMC kararı 28.10 21:00 TSİ | federalreserve.gov (iki ajan ayrı ayrı teyit etti) |
| BIST 100 | 27.10: 11.151,03 · 28.10: 11.165,44 | cnbce, Endeks24, Yahoo (Investing'in 11.249'u hatalı) |
| BIST 30 spot | 28.10: 13.960,9 | Yahoo |
| F_XU0301226 | 27.10 uzlaşma 14.638; 28.10 son işlem ~14.644; açık pozisyon 314 bin | Borsa İstanbul VİOP bülteni |
| F_USDTRY1226 | 27.10 uzlaşma 52,516; 28.10 ~52,47; açık pozisyon 895 bin | BIST bülteni |
| USDTRY spot | ~49,74–49,78 | TCMB gösterge |
| Teminat (Takasbank GM 2174) | PSR: XU030 %11,4, USDTRY %11,0, GARAN %14,4, YKBNK %15,8. **2.11'de güncelleniyor (artış olası)** | birincil |
| Swap hariç net rezerv | ~56 mlr $ (Ağu) → 37,9 (2.10) → 44,2 (9.10); brüt 169–172 | ikincil (iki kaynak) |
| Eylül işsizliği | %8,4 | TÜİK (teyit edildi) |
| MSCI (15.10) | FIF/NOS artışları ve yeni eklemeler donduruldu; sınıflandırma riski **Haziran 2027**. Yakın vadede zorunlu pasif çıkış yok | MSCI bülteni (Business Wire üzerinden) |
| SPK kredili işlem esnekliği | özkaynak oranı %35 yerine %20; **30.10 seans sonunda bitiyor**, 28.10 itibarıyla uzatma kararı bulunamadı | SPK kararı (haberler); uzatılmazsa tahmini satış 2,8–8,5 mlr TL (günlük hacmin %3–8'i) |
| Fon krizi ölçeği | tasfiyedeki fonlar: 1.233 mlr TL (31.08) → 992 (16.09) → **652** (30.09); 30.09 itibarıyla piyasa değerinin ~%4'ü, GSYH'nin ~%1'i. Bu bir **stok (fon büyüklüğü)**, zarar değil | Gedik, Reuters |
| Brent | ~115 $ üstü (28.10); aylık ~+%13 | iki kaynak |

**Çapraz kontrolde düzeltilen hatalar (tartışmanın somut çıktısı):**

| Kim | İddia | Doğrusu | Kim yakaladı |
|---|---|---|---|
| Koordinatör (ortak veri dosyası) | "14 Eylül zirvesi 14.235,83" | Bu çöküş öncesi son kapanış. Eylül kapanış zirvesi **9.09'da 14.505,5**; tüm zamanların kapanış zirvesi 11.05.2026'da 15.133,5 | ENDEKS, ŞEYTAN, OPSİYON |
| Koordinatör | "1,1 trn TL / 223 fon" | Bayat veri (15.09'da 299 kapalı fonun toplamı); tasfiye kapsamı 30.09'da 652 mlr TL | ŞEYTAN |
| Koordinatör | 9 Ekim haftası yabancı çıkışı −348 mn $ | **−248,2** mn $ | ENDEKS |
| MAKRO | "+%12 kur gap'i = −3.258 TL/kontrat, sermayenin %2'si" | Bu, +%6,2'lik harekete denk geliyor. +%12'de kayıp **−6.297 TL**; 6 kontratta **%3,8**. Boyut 4 kontrata indirildi | OPSİYON, ŞEYTAN, HİSSE, ENDEKS (bağımsız olarak dördü) |
| MAKRO | Aralık USDTRY hacmi 8.848 | Açık pozisyon 895 bin, hacim 29 bin (Foreks kısmi veri vermiş) | MAKRO (kendi bülten kontrolü) |
| HİSSE | Pair Aralık vadesiyle | Aralık pay vadelileri likit değil (F_GARAN1226: 134 kontrat); **Kasım** kontratına taşındı | OPSİYON, HİSSE |
| ŞEYTAN | "2 yıllık tahvil %39,8 > politika faizi, yani indirim fiyatlanmıyor" | %39,8 bileşik getiri; basit getiri ~%36,3, eğri düz | MAKRO, ŞEYTAN |
| ŞEYTAN | "Spot yatay kalsa da short +1.025 puan kazanır" | Spot yatay kalırsa giriş emri hiç dolmaz. Beklenen değer 0,6R değil ~0,45R | OPSİYON |
| ŞEYTAN | "Baz iskontosu = kalabalık short" | İskonto 2026 boyunca yapısal; sıkışma sinyali değil | ENDEKS, OPSİYON |
| ENDEKS | Aralık 14.649 (28.10) | Bu 27.10 fiyatıydı; sonuç değişmedi | ENDEKS |
| HİSSE | Pair "beta-nötr" | Piyasa şoklarına karşı nötr, ama son 9 faiz indirimi gününün 8'inde negatif kapandı (ort. −%1,1). Fiilen "short faiz indirimi" pozisyonu | MAKRO'nun itirazı, HİSSE'nin verisi |

---

## 4. Pozisyon detayları ve neden-sonuç zincirleri

### 4.1 Straddle (en yüksek oy; yön bağımsız)
- **Zincir:** Takvim çok yoğun: 30.10 vade, SPK esnekliğinin bitişi, FOMC sonrası ilk seans → 2.11 teminat güncellemesi → 3.11 TÜFE ve YKBNK sonucu → 12.11 Enflasyon Raporu → 27.11 FİR → 10.12 PPK. Komite yönde bölünmüş. Opsiyonlar ~%11–17 vol fiyatlıyor, gerçekleşen vol %27 → yönden bağımsız olarak ±%5'lik hareketi ucuza almak mümkün.
- **Koordinatörün bağımsız Black-76 kontrolü** (F=14.644, 64 gün): straddle adil değeri σ%17'de 784, σ%24'te 1.102, σ%27'de 1.238 puan. **800 puandan dolarsa avantaj ~%25–35.** Uzlaşma seviyesinden (~1.100) alınırsa beklenen değer sıfır veya negatif.
- **Getiri profili:** Başabaş 13.700 / 15.300. Maks zarar prim kadar (≤8.000 TL/straddle).
- **Yönetim:** IV %23'e dönerse yarısını sat. |Δ| > 0,35 olursa vadeliyle nötrle. Değeri ≤400 puana inerse kapat. 15.12'de kapat.
- **Neyde bozulur:** Sessiz toparlanma (RV %15–17, endeks 14.000–15.000 bandında). Ucuz fiyatlar bayat veya sığ işlemler olabilir; put bacağında derinlik zayıf (27.10'da 29 işlemde 266 kontrat).

### 4.2 Short F_USDTRY1226 (TL carry)
- **Zincir:** TCMB fiyat istikrarı için kur kanalını kullanıyor → aylık ~%1,6–2,0 kontrollü kayma → vadeli bunu yıllık %31 primle fazla fiyatlıyor → aradaki 7–11 puan vade sonunda short pozisyona akar.
- **Kırılma noktası:** Vade sonu kuru **52,47** (yıllık %31 hız).
- **Çıkış/yanlışlama:**
  - Kur hızı (10 günlük) yıllık %35'i aşarsa.
  - Brüt rezerv 160 mlr $'ın altına inerse.
  - Haftalık repo ihalesi durdurulursa.
  - CDS 300'ü aşarsa.
  - Siyasi veya hukuki bir şok olursa (açılışta çık).
- **En büyük risk:** Tek seferlik devalüasyon. Uygulanabilir bir hedge yok: C57000 işlem görmüyor, C56000 beklenen değerin tamamını yiyor.
- **Bilinmeyen:** Döviz vadelide bireysel yatırımcı için **stopaj teyit edilmedi**. Varsa carry getirisini doğrudan azaltır; aracı kurumdan teyit edin.

### 4.3 "Ralliyi sat" kovası
- **Zincir:** Likit olmayan fon stoku 60+ günde eriyor. ÖSBA temerrütleri 2026'da 43'e çıktı (2024–25'te yılda 5). Brent 115 $ üstünde. Mevduat ve para piyasası fonu ~%36–44 getiri veriyor → tepki rallileri kırılan destek bölgesinde (14.400–14.700 spot) satıcı bulur → endeks dönemi nakdin gerisinde kapatır.
- **2026 kanıtı bu zinciri kısmen destekliyor:** XU030 yılbaşından beri +%14, nakit getirisi ~%30+.
- **Dolum olasılığı** (σ %27): 14.900 için ~%72, 15.050 için ~%57. Koşulsuz beklenen değer **~+0,16R**, yani ince.
- **Squeeze itirazı (HİSSE) test edildi:**
  - Fon krizi hisselerinin XU030 ağırlığı ~%6,5. Endeksi +%3 taşımaları için hepsinin ortalama +%46 yükselmesi gerekir; vadeli short bu riski kaldırıyor.
  - Asıl yukarı risk ASELS (ağırlık ~%15, 3Ç beklentiyi geçti) ve bankalar (~%22).
- **Put spread neden tercihli?** Tanımlı risk sağlıyor: gap, limit kilidi ve sıkışma riski yok. Fiyatı (≤200) σ%24 adil değerinin (214) altında.
  - **Koordinatör uyarısı:** Beklenen değer tamamen ŞEYTAN'ın öznel "%30 olasılıkla 13.000 altı" varsayımından geliyor. Risk-nötr olasılık **~%13–16** (σ %24–27). Piyasa olasılıklarıyla beklenen değer ≈0.
  - Bu bir görüş pozisyonu, arbitraj değil. Diğer ajanlar 2. turda bunu oylayamadı.
- **Yanlışlama:** Spot kapanışı >14.850 (vadeli short için) veya >15.100 (genel). İki hafta üst üste >200–300 mn $ yabancı alımı. SPK esnekliği uzatır ve teminat çağrıları düşer. Kasım'da yeni ÖSBA temerrüdü olmaz.

### 4.4 GARAN/YKBNK pair
- **Zincir:** Faiz indirimi yavaş (100 bp), risk maliyeti ~300 bp'ye yaklaşıyor, sektörde sorunlu kredi hacmi çeyrekte +%50 → NIM toparlanması gecikiyor (Akbank'ın swap düzeltmeli NIM'i −100 bp) → ROE'si ~%27 olan GARAN ile ~%15 olan YKBNK benzer F/DD'den (~1,0–1,05) fiyatlanıyor → bu fark açılır.
- **Neyde bozulur:**
  - Ekim TÜFE düşük gelir ve hızlı indirim fiyatlanırsa YKBNK'nın yüksek faiz betası pair'i ezer.
  - YKBNK sonucu ve TÜFE aynı gün (3.11); bu yüzden giriş ikiye bölündü.
  - Kasım vadesi 10.12 PPK'dan önce bittiği için karar günü riski pencerenin dışında.
- **Gap stresi:** YKBNK +%10, GARAN −%5 olursa kayıp ~%3,3 (tam boy). Bu yüzden önce yarım boyla başlanmalı.
- **Teminat:** GM 2174'e göre GARAN-YKBNK arasında %60 teminat mahsubu var; fiilî teminat hesaplananın %40–50 altında olabilir.

---

## 5. Portföy riski ve stres testi (OPSİYON hesabı, 10 mn TL)

Not: Tablo, OPSİYON'un kurduğu varyantı gösteriyor: 13 kontrat vadeli short, put spread yok, USDTRY 35 kontrat, tam boy pair. Put spread'li varyantta squeeze senaryosundaki (ii) kayıp daha küçük olur. Buna karşılık TL şokunda (iii) bear kovasının kazancı da azalır; çünkü put spread'in kazancı en fazla 800 puanla sınırlı.

| Senaryo | Rally short doldu | Rally short dolmadı |
|---|---|---|
| (i) 30.10 açılışı: BIST30 −%8, USDTRY +%5 | **+%0,66** | −%0,89 |
| (ii) BIST30 +%8 short squeeze ("tasfiye bitti") | **−%0,78** | +%0,77 |
| (iii) USDTRY +%12 devalüasyon + BIST30 −%15 | **+%1,07** | **−%1,84** |
| 2021 tipi: TL çöker, nominal BIST yükselir | carry ve short birlikte kaybeder, **~−%3** (straddle kısmen telafi eder) | carry kaybı |
| İdiosenkratik: YKBNK tavan, GARAN yatay | −%1,5 ilave | −%1,5 ilave |

- **Limitler:** Fikir başına ≤%1; toplam ≤%4 (gerçekleşen ~%2,2–2,6); ortak stres ≤%7; teminat kullanımı ~%10 (aracı kurum çarpanıyla ~%15).
- **Gizli korelasyon (koordinatör notu):** Straddle dışındaki üç pozisyonun ortak varsayımı aynı: "ortodoks rejim ve kontrollü TL sürer". Bu varsayım çökerse çeşitlendirme sanılandan zayıftır.

---

## 6. Önemli karşı argümanlar

- **Boğa tarafı:**
  - Zorunlu satış bitince sert V dönüşleri görülmüştür (Mayıs 2019, Mart 2020).
  - Şirket geri alımları sürüyor.
  - Yabancı takas oranı yükseliyor; satan yerli kaldıraçlı yatırımcı.
  - MSCI riski 2027'ye kaydı.
  - Dolar bazında BIST 100 ~224 $; Haziran 2023'ten beri en düşük seviye.
  - Devlet destek refleksi (esneklik uzatma, kamu kaynaklı alım) short'ları sıkıştırabilir.
- **Ayı tarafı:**
  - Dolar bazında tarihî dip değil: 2018 ve 2021'de 124–143 $.
  - BIST 100 PD/DD 1,65 ile ortalamanın (1,4) üstünde.
  - Kâr marjları düşüyor; Brent 115 $; CDS 244–255; ÖSBA zinciri.
  - Tasfiye Mart 2027'ye kadar sürüyor ve ayni ödemeler küçük hisselere yeni arz yaratıyor.
- **Carry'ye karşı:** "Kazanç kademeli birikir, kayıp tek seferde gelir." 2026'da üç şok (İran savaşı, Mayıs'taki "mutlak butlan", fon krizi) rezervle emildi. Bu hem tezin temeli hem kuyruk riskinin kaynağı.

---

## 7. Sınırlamalar (dürüst muhasebe)

1. **Aynı model, aynı girdi.** 5 ajan aynı modelden türetildi ve aynı başlangıç dosyasıyla başladı. Çapraz kontrol 11 olgu ve hesap hatasını yakaladı, ama **ortak kör noktaları yakalamaz**. ŞEYTAN, ENDEKS ile yaptığı short yakınsamasının büyük ölçüde ortak girdi yanlılığı olduğunu kendisi kabul etti.
2. **Olasılıklar öznel.** Benzer olay örneklemleri küçük (n=22, n=2) ve tasarıma duyarlı. Beklenen değerlerin hepsi ince (+0,16R ile +0,8R arası, varsayıma bağlı).
3. **Veri zaman damgaları.** Bazı vadeli fiyatlar Foreks/TradingView ekranlarından (±50 puan). 28.10 resmi uzlaşma bülteni yazım anında yayımlanmamıştı. Bu akşam FOMC kararı ve Garanti sonucu açıklanacak; **30.10 açılışında her şey yeniden fiyatlanacak.**
4. **Teyit edilemeyenler:**
   - Endeks vadeli günlük fiyat limiti: ±%10 en güncel görünen duyuru (2022, "ikinci duyuruya kadar"); bazı dokümanlarda ±%15/±%20 yazıyor.
   - SPK esnekliğinin 30.10 sonrası durumu.
   - Ekim TÜFE beklentisi (aylık ~%2,0–2,4 türetme, anket yok).
   - Stopaj ve komisyon.
   - Opsiyon makasları (bültende yok).
5. **Uygulanabilirlik:** Opsiyon fikirleri limit fiyat koşuluna bağlı; derinlik sığ. 1 mn TL gibi küçük sermayede kontrat tam sayılı olduğu için hedeflenen risk yüzdeleri tutturulamayabilir: 1 F_XU030 ≈ 145–150 bin TL nominal ≈ ~%0,45–0,56 stop riski.

---

## 8. Sonuç

- **Bugün (28.10) işlem yok.** Gerekçe: tatil öncesi kapanış, bu akşam FOMC ve Garanti, 30.10'da vade sonu ile SPK esnekliğinin bitişi aynı gün.
- **30.10 sonrası öncelik sırası:**
  1. Ucuzsa vol al (straddle ≤800).
  2. Küçük boyutlu TL carry (1 mn TL başına ≤4 kontrat).
  3. Ralli gelirse tanımlı riskle sat.
  4. Garanti koşulu sağlanırsa yarım boy banka pair'i.
- **Komitenin en sağlam ortak bulgusu bir uyarı:** Bu seviyeden yönlü long, bu seviyeden yönlü short ve "baz bedava para" — üçü de veriyle desteklenmiyor.
- **Hiçbir koşul tetiklenmezse:** ~%36 brüt (ex-ante reel ~%10) faiz getiren nakitte beklemek **meşru ve güçlü bir referans** seçenek.

### Kritik takvim
| Tarih | Olay |
|---|---|
| 28.10 21:00 | FOMC kararı; Garanti 3Ç |
| 30.10 | Ekim VİOP vadesi; SPK kredili işlem esnekliğinin bitişi; PPK özeti; tatil sonrası ilk tam seans |
| 2.11 | Takasbank risk parametresi güncellemesi |
| 3.11 | Ekim TÜFE; YKBNK 3Ç |
| 5.11 | ISCTR, VAKBN 3Ç |
| 12.11 | TCMB Enflasyon Raporu |
| 13.11 | "Ralliyi sat" emirlerinin son geçerlilik günü |
| 26.11 | Pair'in son kapanış günü (Kasım vadesi) |
| 27.11 | Finansal İstikrar Raporu |
| 04.12 | Vadeli short'un son kapanış günü |
| 10.12 | PPK |
| 15.12 | Straddle'ın kapanışı |
| 31.12 | Aralık vadesi |

### Ana kaynaklar
- TCMB faiz kararı: https://www.qnbinvest.com.tr/investodak/qnbarastirma/tcmb-ekim-ayi-faiz-kararini-acikladi-politika-faizi-36ya-indirildi
- Eylül TÜFE: https://gazeteoksijen.com/ekonomi/eylulde-enflasyon-yillik-yuzde-29-73-aylik-yuzde-1-84-oldu-291680
- 27.10 piyasa verisi: https://www.cnbce.com/borsa/borsa-istanbul-canli-piyasalarda-yeni-yukselis-beklentisi-27-ekim-2026-h40399
- Fed 16.09.2026: https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm
- VİOP günlük bülteni: https://www.borsaistanbul.com/data/vadeli/viop_20261027.csv
- Takasbank GM 2174: https://www.isyatirim.com.tr/tr-tr/Resmi-Duyurular/Documents/GenelMektup2174.pdf
- MSCI dondurma kararı: https://finance.yahoo.com/markets/world-indices/articles/msci-implements-freeze-msci-turkey-212400488.html
- Tasfiye fonları (Gedik): https://cdn.gedik.com/media/media/tvmjp14x/gedik_yatirim_tasfiye_fonlari_degerlendirme_05102026.pdf
- Fon krizi: https://www.birgun.net/haber/tera-ve-pusula-ile-gundeme-geldi-fon-krizi-nedir-nasil-patladi-son-durum-ne-735571
- Düşüş serisi: https://www.cumhuriyet.com.tr/ekonomi/fon-krizi-borsa-yi-vurdu-18-yilin-en-uzun-dusus-serisi-2550017
- Endeks vadeli fiyat limiti (±%10): https://www.borsaistanbul.com/files/20221215-13341_viopta-bist-surdur.25-endeksi-vis-isl-acilmasi.pdf
- Garanti 3Ç beklentisi: https://www.yatirimx.com.tr/piyasa/garanti-bbva-3-ceyrek-beklentisi-uc-araci-kurumdan-kr-artisi-tahmini/26515
- Tam kaynak listeleri her ajan dosyasının sonunda (`ajanlar/`).
