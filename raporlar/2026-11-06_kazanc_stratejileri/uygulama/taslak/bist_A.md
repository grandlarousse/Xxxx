# Taslak A — BIST/VİOP swing planı: "Trend/RS lideri + küme (pozitif çarpıklık)"

- **Hazırlanma:** Cuma 06.11.2026, ~14:00 TSİ. Veri: 05.11.2026 kapanışı (tarama, VİOP resmi bülteni). Plan **Pazartesi 09.11.2026**'dan itibaren geçerli.
- **Açı:** 52 haftalık kapanış zirvesi kırılımı + trend şablonu, likit ve arz baskısı (overhang) olmayan isimler (öncelik VİOP'taki 47 dayanak), 12 aylık küme RS sıralaması, rejim kapısı, pay vadelisiyle sermaye verimliliği, XU030 vadelisiyle hedge, iz süren stop. Bugünkü ayı rejiminde **bekleme modu** ve kesin tetikler.
- **Kanıt hiyerarşisi:** Doğrulama dosyaları (`dogrulama/v_*.md`) ajan raporlarıyla çeliştiğinde doğrulama esas alındı. Kaynak kısaltmaları en sonda (§10). "[EK-n]" bu taslak için yapılan ek hesaplardır (yöntem §10.2).
- **Henüz yazılmamış dosyalar:** `olay_bedelsiz.md`, `olay_akis_rejim.md` ve `v_olay.md` yazım anında klasörde yoktu; kullanılmadı.
- Yatırım tavsiyesi değildir. Bütün getiri aralıkları geçmiş veriden ve öznel olasılıklardan türetilmiştir; belirsizlik büyüktür.

---

## 0. Tek paragraf özet

Bu açı, BIST'te kendi testlerimizde (2010–26) maliyet sonrası işlem başına pozitif kalan **tek hisse seçimi kenarına** dayanıyor: 52 haftalık kapanış zirvesi kırılımı + trend şablonu + %15 iz süren stop. Ancak kâr sağ kuyrukta toplanıyor ve **2024–26 gibi yüksek reel faizli dönemde TL engelini ancak yakaladı**. Bugün rejim **KAPALI**: XU100 200 günlük ortalamanın %16,5 altında, 12 aylık zaman serisi momentumu kapalı, makro tetiklerin 0/5'i sağlanıyor, VİOP-47'de kırılım veren hisse yok. Bu yüzden plan Pazartesi **sermayenin ≥%95'ini vergi sonrası en yüksek getirili düşük riskli araçta** (32 günlük TL mevduat merdiveni + banka iştiraki PPF) tutuyor. Risk tarafında yalnız **en fazla 2 "pilot"** kırılım işlemine izin var (işlem başı hesabın %0,25'i risk). Kesin fiyat tetiklerini içeren bir izleme listesi tutuluyor. Rejim GEÇİŞ'e (risk 0,5%) ya da AÇIK'a (risk 1%) döndüğünde kurallar tam boy devreye giriyor. Önümüzdeki 12 ay için dürüst beklenti: hesap düzeyinde engelin **+0…+4 puan** üstü (beklenen değer). %80 aralık **−4…+12 puan**. Engelin kendisi net ~%31–38. "Yüksek getiri" ancak rejim dönerse ve sağ kuyruktaki birkaç işlem yakalanırsa gelir.

---

## 1. Sermaye dağılımı kararı

### 1.1 Engel ve çekirdek araç karşılaştırması (bireysel, vergi sonrası)

| Araç | Bugünkü brüt | Stopaj (birey) | Net beklenti, 12 ay | Likidite / risk | Karar | Kaynak |
|---|---|---|---|---|---|---|
| **32 günlük TL mevduat, aylık yenileme** | Banka ort. %39,52 (06.11, ikincil kaynak) | %17,5 (6 aya kadar vade) | Faiz sabit kalırsa ~%37,9. Anket patikasında (12 ay sonra %29) ~%31–33 | Vade kırılırsa faiz yanar. Banka riski: TMSF limitini bankanızdan teyit edin | **Çekirdeğin ana gövdesi** | v_capraz #4, #6 |
| **Banka iştiraki PPF** (bir mevduat bankasının portföy şirketi) | İleriye dönük brüt ~%37–42. Son 1 yıl medyanı brüt %45,5 | %17,5, itfada birikmiş kazançtan bir kez | ~%31–35 | T+0/T+1 likit. Tasfiyedeki 15 PPF'nin 4'ü %95–99,9 kaybettirdi: **yalnız banka PYŞ'si**. Ters repo teminatında grup ihracı olmamalı (KAP portföy raporu) | **Likidite tamponu ve VİOP teminatı** | v_bist #13, §3.3; v_profesyonel eksik 2; tr_makro §1.3 |
| DİBS / hazine bonosu (≤1 yıl vade) | 2 yıllık %39,38 bileşik (06.11) | %0 yalnız muafiyet kapsamındaysa. GİB rehberi 30.06.2026'ya kadarki alımları sayıyor; 31.12.2026 uzatması yalnız ikincil kaynakta. Aksi halde %10 | ~%35–39 | Faiz riski. TL şokunda hisseyle birlikte kaybeder | **Opsiyonel, çekirdeğin ≤%10'u.** Ön koşul: aracı kurumdan **yazılı** %0 stopaj teyidi | v_capraz #8; hazırlık §4c |
| XU030 nakit-taşıma (BIST30 sepeti veya BYF long + F_XU030 short) | Aralık resmi uzlaşma 14.734, spot 14.101 → ima **%29,3** (56 gün, basit) | %0 / %0 | ~%28–29 (sepet maliyeti ve takip hatası öncesi) | Teminat, takip hatası | **Bugün HAYIR.** Net mevduattan ~8 puan düşük | anchor (resmi bülten); v_profesyonel T12; v_capraz eksik 1 |
| Short F_USDTRY (TL carry) | Fiyatlanan − beklenen kur farkı ~13 puan (daralıyor) | **%10** | USD bazında yıllık ~+%10–12, vergi öncesi ve kuyruk hariç | 2010–26 Sharpe −0,51, MaxDD −%90. Tek ayda −%25…−35. USD teminat ~%0 kazanır | **A planında 0.** Kuyruğu hisse/banka kuyruğuyla aynı yönde | tr_makro §4.3; v_capraz #19, eksik 8 |

**Not (hata düzeltmesi):** Tarama dosyası ve `bist_hafta_hazirlik.md` §0-8, XU030 Aralık için %23,3 ima faiz ve "%1,8 iskonto" veriyor. Bu **yanlış**: yanlış vadeli fiyatı kullanılmış. Resmi uzlaşmayla ima faiz %29,3, iskonto 56 günde ~%1 (v_profesyonel T12). Her hesapta `https://www.borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv` kullanılmalı.

**Engel tanımı (bu planın ölçütü):** Her risk kolunun getirisi, **aynı dönemde aynı TL'nin çekirdekte vergi sonrası kazanacağı getiriyle** karşılaştırılır. Bugün bu ~%31–38/yıl, yani ayda ~%2,3–2,7. Reel karşılığı ~%5–8; "reel %40–50" algısı yanlış (v_capraz #3–4).

### 1.2 Karar: rejime göre dağılım

| Rejim (bkz. §3) | Çekirdek | A1 kırılım | A2 küme rotasyonu | A3 XU030 vadelisi | Brüt uzun hisse/endeks maruziyeti |
|---|---|---|---|---|---|
| **KAPALI (bugün)** | ≥%95: %60 mevduat merdiveni + %40 banka PPF | En fazla 2 pilot × hesabın %1,67'si = ≤%3,4 nominal | 0 (nakit) | 0 | ≤%5 |
| GEÇİŞ | ≥%85 | En fazla 4 × %3,33 = ≤%13,3 | 0 | 0 (yalnız hedge kuralı) | ≤%15 |
| AÇIK | Spot ağırlıklıysa ≥%40. Pay vadelisi kullanılıyor ve teminat PPF ise ~%95'i nemalanmaya devam eder | ≤%45 nominal (eklemeler dahil) | ≤%20 | Sentetik long ≤%20, yalnız 12 aylık TSMOM açıkken | **≤%60** (stres sınırı, §5) |

Gerekçeler:
- **Çekirdek ağırlığı.** BIST'te son 3 yılda neredeyse hiçbir hisse fonu PPF medyanını geçemedi (91 fondan 1'i; v_profesyonel T1–T2). Pozitif reel faiz döneminde hiçbir uzun-hisse yapısı nakdi geçmedi (swing §10; dalga_bist §0-4; v_dalga §5-1). Varsayılan pozisyon nakit.
- **Mevduat/PPF oranı.** Faiz sabit kalırsa mevduat net ~%37,9, PPF ~%31–35; mevduat 2–5 puan önde. PPF ise sinyal geldiğinde T+1 nakit sağlıyor ve aracı kurumda VİOP teminatı olabiliyor. Bugün risk kolları çok küçük olduğu için ağırlık mevduatta.
- **2027 vergi riski.** %17,5 stopaj 31.12.2026'da sona eriyor. İndirim haberi tek ikincil kaynağa dayanıyor (v_capraz eksik 6). Aralık sonunda yeniden bakılacak.

### 1.3 Uygulama, 1 / 5 / 20 milyon TL örnekleri (bugün, KAPALI)

| Kalem | 1 mn TL | 5 mn TL | 20 mn TL |
|---|---|---|---|
| Mevduat merdiveni %60: 4 dilim × %15, vadeler 4 hafta arayla | 4 × 150.000 | 4 × 750.000 | 4 × 3.000.000 (≥3 bankaya bölün) |
| Banka iştiraki PPF %40 | 400.000 | 2.000.000 | 8.000.000 (≥2 banka PYŞ'si) |
| İçinden pilot bütçesi (≤%3,4 nominal) | ≤33.000 | ≤167.000 | ≤667.000 |
| Çekirdeğin beklenen aylık net getirisi (~%2,5–2,7) | ~25–27 bin | ~125–135 bin | ~0,50–0,54 mn |
| Pilot işlem başı risk (%0,25) | 2.500 | 12.500 | 50.000 |

Merdiven takvimi: dilim 1 Pazartesi 09.11, dilim 2 16.11, dilim 3 23.11, dilim 4 30.11. Böylece her hafta hesabın %15'i vadeye gelir. Kurulum sırasında henüz bağlanmamış dilimler PPF'te bekler: PPF payı Pazartesi %85'tir, 30.11'de %40'a iner. Rejim AÇIK'a dönerse risk kolları önce PPF'ten, sonra vadesi gelen dilimden fonlanır; hiçbir dilim vadesinden önce bozulmaz.

---

## 2. Strateji kolları

### 2.1 A1 — Lider kırılımı (ana kol)

**Tanımlar.** Hepsi kapanış fiyatıyla, temettü ve bedelsiz düzeltmeli seriden hesaplanır. Testteki tanımlar birebir korunmuştur (bist_test §5; kod `hesaplar/bist_test/t03_kirilim_trend_sablonu.py`).

| Kod | Koşul |
|---|---|
| **B52** | Bugünkü kapanış > önceki 252 işlem gününün en yüksek kapanışı |
| **TT** (trend şablonu, 7 koşul) | Fiyat > SMA50 > SMA150 > SMA200; SMA200 21 gün öncekinden yüksek; fiyat ≥ 1,25 × 52 haftalık dip; fiyat ≥ 0,75 × 52 haftalık zirve; RS yüzdeliği ≥ %80. RS = 0,4·R3a + 0,2·R6a + 0,2·R9a + 0,2·R12a; yüzdelik en likit 150 hisse içinde |
| **S2 sinyali** | B52 + TT. Tam boy |
| **S1 sinyali** | B52 var, TT eksik. Yarım boy |

Not: Tarama betiğindeki şablon (`bist_tarama.py`) testten biraz farklı: RS ≥70, dip ×1,30, 100 hisselik evren. Karar için §4.4'teki test tanımlı tablo esas alınır. Betik ön eleme olarak kullanılır.

**Giriş kuralları**
1. Sinyal t günü kapanışında oluşur. Giriş **t+1 kapanışında** yapılır; testte de böyle. v_bist #24'e göre bir gün gecikme 52 hafta sinyalini zayıflatmıyor.
2. Spot emir: t+1 günü **kapanış seansına (18:00–18:10) limitli alış**. Limit = önceki kapanış × 1,05.
   - Aracı kurumunuz kapanış seansı emrini önceden girmeye izin veriyorsa sabah girin. Vermiyorsa 17:55–18:07 arasında tek emir yeter; bu ekran takibi değildir.
3. Pay vadelisi emri (yalnız VİOP-47 ve §2.1.3 koşulları sağlanırsa): t+1 günü 17:55–18:08 arasında ön ay kontratına limitli alış. Limit = son fiyat + 2 fiyat adımı.
4. **Tavan kuralı.** Giriş günü hisse tavanda kilitliyse (≥+%9,5) emir dolmaz, iptal edilir. Ertesi kapanışta koşullar hâlâ sağlanıyorsa yeniden denenir. Bu, testteki "gerçekçi dolum" varsayımıdır (bist_test §1 bias 3).
5. **Bilanço kuralı.** Şirket sinyal kapanışı ile giriş kapanışı arasında finansal tablo açıklayacaksa giriş yapılmaz. Açıklamadan sonraki ilk kapanışta sinyal yeniden değerlendirilir.
   - Bu kural test edilmedi. Gerekçe: bilanço gap'i riski tanımsız R üretir.
   - KAP'ta bilanço tarihi kontrol edilir. 9.11 konsolide 3. çeyrek tabloları için yasal son gündür (hazırlık §2).
6. **Olay günü kuralı (yalnız bu hafta).** Çarşamba 11.11 kapanışında yeni giriş yok: 12.11 01:00'de MSCI duyurusu, 13.11'de kredili işlem esnekliğinin bitişi var. Salı sinyalleri Perşembe 12.11 kapanışında uygulanır (t+2). Test edilmedi; maliyeti bir günlük gecikmeden ibaret.
7. **Ekransız alternatif.** 18:00'de erişim yoksa t+1 açılış seansında (09:40–09:55) limitli emir girilir: limit = sinyal kapanışı × 1,03. Bu varyant test edilmedi. Yalnız zorunlu hallerde kullanılır ve günlükte işaretlenir.
8. Bildirim: her bekleme listesi hissesi için TradingView alarmı kurulur. Örnek: "BIST:ENJSA, Kapanış, eşik 127,00, bar kapanışında bir kez". Alarmlar 18:15'te okunur.

**Çıkış kuralları**

| Kod | Kural | Uygulama | Kanıt |
|---|---|---|---|
| E1 iz-stop | Kapanış ≤ girişten beri en yüksek kapanış × 0,85 | t+1 kapanış seansında limitli satış, limit = önceki kapanış × 0,95. Taban kilitliyse ertesi gün tekrarlanır | bist_test §5.1 (tüm kombinasyonlarda en iyi çıkışlardan) |
| E2 süre | Girişten itibaren 120 işlem günü | 120. gün kapanışında satış | bist_test §5 (testte azami 120 gün) |
| E3 felaket emri | Aracı kurumda bekleyen şartlı satış. Tetik = en yüksek kapanış × 0,80; limit = tetik × 0,97 | Her Cuma 18:30'da güncellenir. Yalnız E1'in kaçırıldığı günler için yedek | **Test edilmedi**; sermaye koruma |
| E4 dışlama | Hisse VBTS tedbirine (brüt takas, tek fiyat) girerse, SPK soruşturma ya da suç duyurusu listesine eklenirse ya da fon payı / fiili dolaşım oranı %20'yi aşarsa | Ertesi kapanışta koşulsuz çıkış | tr_profesyonel §6; **test edilmedi** |
| E5 büyük kazanç | Pozisyon girişten itibaren ≥+%100 kâra ulaşırsa iz-stop %15'ten %10'a sıkılaşır | Kalıcıdır | GSY uyarısı (v_dalga §5-5); **test edilmedi** |

Kısmi kâr alma yok. Kârın yarısından fazlası en iyi %5'lik işlemlerden geliyor (VİOP-47'de %52, tüm evrende %70; [EK-1], bist_test §5.1). Kısmi satış tam da bu kuyruğu keser.

**Boyut (rejime göre r₀ = işlem başı risk, hesabın %'si)**

| Rejim | r₀ | Azami açık A1 pozisyonu | A1 toplam açık risk |
|---|---|---|---|
| KAPALI | 0,25 (yalnız pilot; yalnız S2) | 2 | %0,5 |
| GEÇİŞ | 0,50 | 4 | %2,0 |
| AÇIK | 1,00 | 6 (her biri +1 ekleme) | %6,0 |

- **Nominal formülü:** nominal = hesap × r₀ × çarpan / stop mesafesi.
- **Stop mesafesi:** %15 (iz-stop). İki durumda **%25**: son 3 yılda yılda ≥5 limit günü yaşayan hisseler (GUBRF 9,4; TKFEN 9,4; BRSAN 8,0; HALKB 7,1; SASA 7,0; ASTOR 6,7; VESTL 6,4; HEKTS 5,4; kaynak PRATİK_LİSTE risk tablosu) ve ATR%'si 4,5'in üstünde olanlar. Nedeni gap ve taban kilidi.
- **Çarpanlar:** S2 ×1,0; S1 ×0,5; VİOP dışı BIST100 (evren U2) ×0,75.
- **Tavan:** tek pozisyon nominali ≤ hesabın %15'i.

**Boyut örnekleri.** Fiyatlar 05.11 kapanışı. Pay vadelisi kontratı = 100 pay.

| Durum | 1 mn TL | 5 mn TL | 20 mn TL |
|---|---|---|---|
| KAPALI pilot (r₀ 0,25, stop %15): nominal %1,67 | 16.667 TL → ENJSA 139 pay (119,30) veya 1 kontrat (11.845) | 83.333 → 698 pay veya 7 kontrat | 333.333 → 2.794 pay veya 28 kontrat |
| AÇIK S2 (r₀ 1,0, stop %15): nominal %6,67 | 66.667 → KCHOL 329 pay (202,30) veya 3 kontrat (Kasım 206,05 → 20.605/kontrat) | 333.333 → 1.647 pay veya 16 kontrat | 1,33 mn → 6.590 pay veya 64 kontrat |
| AÇIK, limit riskli hisse (stop %25): nominal %4 | 40.000 | 200.000 | 800.000 |
| İşlem başı risk (AÇIK) | 10.000 TL | 50.000 TL | 200.000 TL |

**Piramit (ekleme) kuralı.** Tek ekleme yapılır. Kurgu risk-nötrdür; etkisi test edilmedi.
- Koşullar: rejim AÇIK; pozisyon kapanışı ≥ giriş × 1,10; aynı gün kapanış yeni bir 20 günlük kapanış zirvesi; küme ve blok sınırları aşılmıyor; ekleme sonrası nominal ≤ hesabın %15'i.
- Miktar ve zaman: **ilk adedin %50'si**, t+1 kapanış seansında.
- İz-stop tüm pozisyon için aynı kalır: en yüksek kapanış × 0,85.
- Neden risk-nötr: ekleme fiyatı A (giriş = 1) iken stopta toplam kayıp = 1 − 0,775·A. A = 1,10'da bu 0,1475'tir, yani ilk riskin (0,15) altında. A büyüdükçe daha da azalır.
- GEÇİŞ ve KAPALI'da ekleme yok.
- Günlükte "ekleme" ayrı satır olarak tutulur; katkısı ayrıca ölçülür.

**2.1.3 Spot mu, pay vadelisi mi?** Pay vadelisi kaldıraç için değil, finansman verimliliği için kullanılır. Nominal, spot formülüyle hesaplanandan büyük olamaz.

Pay vadelisi yalnız şu dört koşulun hepsi sağlanırsa kullanılır, aksi halde spot:
1. Aracı kurum VİOP teminatı olarak PPF payını (ya da DİBS'i) kabul ediyor veya nakit teminata TLREF − 5 puandan yüksek nema ödüyor. **Yazılı teyit şart.** Nakit teminat boşta durursa teminat × ~%37 fırsat maliyeti avantajı siler (seytan §3.1).
2. Ön ay kontratının ima taşıma oranı ≤ TLREF − 3 puan.
   - İma oran = (uzlaşma / spot − 1) × 365 / gün.
   - 5.11 değerleri: KCHOL %27,1; GARAN 25,2; THYAO 25,6; TUPRS 29,9; BIMAS 28,9; AKBNK 26,3; YKBNK 28,0; ALARK 24,5. TLREF %35,85. [EK-6]
   - İma oran < %15 ya da negatifse (ör. ENJSA Kasım −%10,4, FROTO −%40) KAP'ta temettü veya sermaye işlemi aranır. Açıklanamıyorsa spot kullanılır.
3. Ön ay açık pozisyon ≥ 20.000 kontrat ve günlük işlem hacmi ≥ 100 mn TL. Uzak vadeler sığ: 5.11'de KCHOL Kasım açık pozisyonu 153 bin, Aralık 6,8 bin [EK-6].
4. Aracı kurum teminat oranı ≤ %35. ASTOR, HALKB ve VESTL %100, GUBRF %50 (QNB, 03.11) → bu isimlerde yalnız spot (v_bist #16).

Ek kurallar:
- **Devir (roll):** vadeden 3 iş günü önce kapanışta yapılır. Kasım kontratı için **25.11 Çarşamba**. Pay vadelileri **fiziki teslimatlıdır** (hazırlık §5). Yeni vadenin o günkü işlem hacmi < 20 mn TL ise pozisyon spota taşınır.
- **Teminat tamponu:** hesapta serbest teminat ≥ 2 × sürdürme teminatı. Pay vadelilerinin toplam başlangıç teminatı ≤ hesabın %20'si.
- **Beklenen avantaj:** spot yerine pay vadelisi kullanınca nominal kadar nakit çekirdekte kalır. Avantaj = çekirdeğin net getirisi − ima taşıma oranı. Nakit PPF'teyse yılda nominalin ~0–6 puanı, mevduattaysa ~8–13 puanı. 60 günlük ortalama tutmada ~%0–2. Devir maliyeti (her biri ~5–15 bps, tahmin) bundan düşülür. Akşam seansında pay vadelisi işlem görmez.

**A1 beklentisi (dürüst aralık)**

| Ölçü | Backtest: tüm likit evren (S2 + iz %15) | Backtest: yalnız VİOP-47 [EK-1] | İskonto sonrası beklenti |
|---|---|---|---|
| İşlem sayısı / yıl | ~123 | ~27 | AÇIK rejimde VİOP-47 + U2 ile ~25–50. KAPALI'da ~0–5 |
| Ortalama net / işlem | +%11,4 | +%11,8 (gerçekçi dolum +%11,3) | +%4…+%8, yani +0,3…+0,5R |
| Medyan | −%2,9 | +%1,2 | −%3…+%1 |
| İsabet | %45 | %51 | %42–50 |
| Kazanç/kayıp oranı | 3,3 | 3,0 | 2–3 |
| Aynı gün likit evrene göre fark | +%5,3 (t 5,1) | +%4,15 (t 3,3) | +%1,5…+%3 |
| 2024–26 | Fark +%10,9; portföy ≈ engel | n=56; ort. +%4,2; medyan +%1,5; fark +%5,1 (t 1,9) | ≈0…+0,3R |
| En kötü işlem | −%37,6 (gerçekçi: −%94, pump isimleri) | −%25,9 (gerçekçi: −%38,5) | −1,7R…−2,5R |
| En uzun kayıp serisi | — | 13 işlem [EK-5] | 8–13 |
| Ortalama tutma | 45 gün | 60 gün | 40–60 gün |

**Portföy düzeyi [EK-2].** 6 slot, slot başı özkaynağın 1/6'sı, boş nakit %17,5 stopaj sonrası mevduat/PPF getirisi kazanıyor, risksiz faiz günlük bileşik olarak düzeltildi:

| Dönem | VİOP-47 kırılım | Vergi sonrası engel | Vergi öncesi engel |
|---|---|---|---|
| 2010–26 | %32,6/yıl | %15,1 | %18,6 |
| 2016–26 | %44,4 | %20,2 | %25,0 |
| 2024–26 | %44,3 | **%43,1** | %54,4 |

- MaxDD −%28 (gerçekçi dolumla −%34).
- 12 aylık TSMOM kapısıyla: 2010–26 %30,1, 2024–26 %50,4, MaxDD −%26.
- **Önemli çekince:** VİOP-47 bugünkü listedir; geçmişin kazananlarından oluşur, dolayısıyla yukarı yanlıdır. Kendi tahminim: %30–50 iskonto.
- Bu planın boyutlandırması backtestin 1/6 ağırlığından çok küçüktür: AÇIK'ta pozisyon başına %6,7, toplam ≤%45. Hesap düzeyindeki etki aşağı yukarı 0,4–0,6 ile çarpılır.

### 2.2 A2 — Küme rotasyonu (12 aylık RS, ilk 3 küme)

- **Kural (dalga_bist §4; v_dalga §5-1).** Ayın son işlem günü kapanışında her küme için skor = R_t / R_{t−252} − 1. Burada R = küme eşit ağırlıklı endeksi / XU100. Kümeler §4.3'tedir.
  - İlk 3 küme alınır, işlem ertesi gün kapanışında yapılır.
  - Ay sonunda ilk 3'ten düşen küme satılır. Ara stop yok.
- **Filtre (dalga_bist §3.7 "B" kuralı).** Slot yalnız şu iki koşulda dolu tutulur: XU100 > SMA200 **ve** kümenin 3 aylık TL getirisi > aynı dönemin TL nakit getirisi. Aksi halde slot çekirdekte (nakit) kalır.
- **Uygulama.** Her küme için en likit 2–3 VİOP dayanağı eşit ağırlıkla alınır. Tek lider hisse sürümü sepetten kötü: medyan CAGR 35,2'ye karşı 41,7, MaxDD −%58 (dalga_bist §3.2).
- **Boyut.** Kol nominali ≤ hesabın %20'si (küme başına ~%6,7). A1 ile aynı hisse ortaksa risk bir kez sayılır, brüt sınıra (§5) dahil edilir.
- **Kol kesici.** A2'nin zirveden kaybı hesabın %5'ine ulaşırsa kol kapatılır ve bir sonraki ay sonuna kadar açılmaz. Test edilmedi; sermaye koruma kuralı.
- **Beklenti.**
  - Yanlılıktan arınmış hali eşit ağırlıklı küme sepetine göre yılda +5 ± 5 puan; MaxDD −%40/−%48 (v_dalga §5-1).
  - 2024–26'da 456 küme kuralının hiçbiri TL nakdi geçmedi.
  - Engel üstü getiri ancak AÇIK rejimde beklenir: kol nominali üzerinden yılda +0…+10 puan, hesap düzeyinde +0…+2 puan.
- **Bugün:** 12 aylık sıralama RAFİNERİ +%26,5, HOLDİNG +%23,9, KOZA_ALTIN +%18,9 (4. PERAKENDE +%17,6). Ancak XU100 < SMA200 ve üç kümenin de 3 aylık TL getirisi negatif (−5,8 / −6,8 / −25,4). **A2 = nakit.** Sonraki hesap 30.11 kapanışı, işlem 01.12 kapanışı.

**Küme RS'si A1 için giriş filtresi DEĞİL [EK-3].** Bu taslak için test ettim.
- Yöntem: 909 kırılım işlemi (2012–26) kümelerine eşlendi.
- Sonuç: sinyal günü 12 aylık sıralamada ilk 3'teki kümelerden gelen kırılımlar aynı gün likit evrene göre +%4,9 fark verdi. Alt yarıdaki kümelerden gelenler +%5,3 verdi. 2024–26'da da fark yok.
- Yorum: hisse RS ≥%80 şartı bilginin tamamını zaten taşıyor.
- Bu yüzden küme sıralaması A1'de yalnız iki işe yarar:
  1. Slot doluyken iki sinyal yarışırsa üst sıradaki kümenin hissesi seçilir.
  2. Konsantrasyon sınırı (§5).

### 2.3 A3 — XU030 vadeli katmanı (hedge ve rejim beta'sı)

**A3a, sentetik endeks long (yalnız AÇIK + TSMOM12 açıkken).**
- Pozisyon: long F_XU030, ön likit vade, nominal ≤ hesabın %20'si. Brüt sınır %60 içinde kalır.
- Nakit çekirdekte kalır; vadeli bugün nakit + spota göre ~%1 ucuz (56 gün).
- Ay sonunda TSMOM12 kapanırsa çıkılır.
- Kanıt: XU100 TSMOM12, 2010–26'da risksiz faizin +6,8 puan üstü; placebo yüzdeliği 0,86–0,88, yani istatistiksel olarak anlamlı değil (bist_test §2). 2× kaldıraçta MaxDD −%69, bu yüzden 1×'i aşmaz.
- Beklenti: hesap düzeyinde yılda +0…+2 puan.

**A3b, hedge kuralları (test edilmedi; risk kontrolü).**
- **H1 olay hedge'i.** Brüt uzun nominal ≥ hesabın %30'u iken önceden bilinen ikili bir olay ertesi seansa düşüyorsa (MSCI duyurusu, SPK kredili işlem kararı, PPK, seçim/anayasa takvimi duyurusu), olay günü kapanışında short F_XU030 açılır.
  - Miktar: kontrat = aşağı yuvarla(0,5 × Σ(βᵢ × nominalᵢ) / (F × 10)).
  - Olaydan sonraki ilk kapanışta kapatılır.
- **H2 piyasa freni.** Brüt uzun nominal ≥ %30 iken XU100 iki kapanış üst üste SMA50'nin altında kapanırsa aynı formülle %50 hedge açılır. XU100 iki kapanış üst üste SMA50 üstünde kapanınca ya da brüt uzun nominal %20'nin altına inince kaldırılır.
- **İstisna.** TUPRS, PETKM ve ASELS β hesabına alınmaz; XU030 hedge'i bu hisselerde riski azaltmıyor, hatta gece riskini artırıyor (PRATİK_LİSTE §3).
- **Maliyet.** Vadeli bugün ~6,5 puan/yıl iskontolu (TLREF %35,85 − ima %29,3). Short hedge bu iskontoyu kaybeder: hedge'lenen nominalin ayda ~%0,55'i. Örnek: 20 mn TL hesap, 8 mn TL uzun, ortalama β 0,95 → 0,5 × 7,6 mn / 147.340 = 25,8 → 25 kontrat → ayda ~20 bin TL. Bu yüzden hedge kalıcı değil, olay ve fren aracıdır.
- **Kontrat ve teminat.** 14.734 × 10 = 147.340 TL nominal. Takasbank asgarisi %11,4 ≈ 16,8 bin TL; QNB oranı %20 ≈ 29,5 bin TL; aracı kurumunuzdan teyit edin.
  - 1 mn TL'lik hesapta tek kontrat hesabın %14,7'si eder; hesaplanan kontrat < 1 ise hedge yapılmaz.
  - Endeks vadelileri akşam seansında (19:00–23:00) da işlem görür. Hedge gerekirse oradan da açılabilir.

### 2.4 Bu açının bilerek dışarıda bıraktıkları

| Fikir | Neden dışarıda | Kaynak |
|---|---|---|
| Kesitsel 12-1 momentum, kısa vadeli dönüş ("düşeni al") | BIST'te çalışmıyor; haftalık kaybedenler kaybetmeye devam ediyor | bist_test §4; swing §3.3 |
| Endeks SMA trend kuralları (tek başına) | Değer katmıyor; placebo ortası | bist_test §2 |
| Tavan serisi sonrası halka arz alımı | 53'ün 52'si (doğrulamaya göre 50–51'i) düştü; medyan −%55 | v_bist #11; olay_halka_arz §0 |
| Pump ve overhang isimlerinde "dipten tepki" | Negatif çarpık; arz Mart 2027'ye kadar sürebilir | tr_profesyonel §6 |
| Kredili spot alım | Örtük maliyet ~%60 | v_bist #3 |
| TL carry, XU030 nakit-taşıma, çiftler, temettü öncesi koşu | Başka açıların kolları. Aynı hesapta yürütülürse toplam risk sınırına (§5) dahil edilir | — |
| Kullanıcının 4 lead-lag sinyali | A planından bağımsız. Sürdürülecekse toplam açık risk ≤ %8 içinde kalır | PRATİK_LİSTE |
| Özel durumlar (ZPAT, ayrılma hakkı, AKCNS 260,25 TL iddiası) | Çalışılmadı. Doğrulanmamış; KAP/SPK teyidi olmadan işlem yok. Tera'nın PEKGY ZPAT yükümlülüğünü yerine getirmediği emsal var | v_bist §3-4 |

---

## 3. Rejim anahtarı

### 3.1 Tanım

Seviye her **Cuma kapanışında** ve **ayın son işlem günü kapanışında** belirlenir, ertesi işlem gününden geçerli olur.

Tek istisna: AÇIK'tayken XU100 kapanışı SMA200'ün %3 altına inerse seviye aynı akşam GEÇİŞ'e düşer.

| Seviye | Koşul | Kanıt düzeyi |
|---|---|---|
| **AÇIK** | (T1) XU100 kapanışı > SMA200 **veya** (T2) ay sonunda XU100'ün 12 aylık getirisi > aynı 12 ayın TL nakit getirisi (TSMOM12; ölçüt banka PPF medyanı ya da TLREF bileşiği) | Test edildi: S5 = kırılım + SMA200 (bist_test §5–6). 52 hafta + TSMOM12 2023–26'da %50–52'ye karşı nakit %36 (swing §4.1). VİOP-47 sürümü [EK-2] |
| **GEÇİŞ** | AÇIK değil, **ama** (T3) XU100 son 5 kapanışın 5'inde SMA50 üstünde **ve** aşağıdaki 5 makro tetikten ≥3'ü sağlanıyor | **Test edilmedi** (tetikler tr_makro §5.1'den). Bu yüzden yarım boy |
| **KAPALI** | Diğer bütün durumlar | — |

**Makro tetikler** (hepsi kamuya açık; tr_makro §5.1–5.3):

| Kod | Tetik | Veri günü |
|---|---|---|
| M1 | Swap hariç net rezerv 3 hafta üst üste artıyor | Perşembe 14:30 |
| M2 | Aylık TÜFE < %2,0 | Sonraki: 03.12, Kasım TÜFE |
| M3 | Yabancı net hisse alımı 2 hafta üst üste ve toplam ≥ +200 mn $ | Perşembe 14:30 |
| M4 | 5 yıllık CDS < 230 | Günlük |
| M5 | XBANK kapanışı > kendi SMA200'ü | Günlük |

### 3.2 Bugün ne diyor (05.11 kapanışı)

| Gösterge | Eşik | Değer | Sağlanıyor mu? |
|---|---|---|---|
| T1: XU100 > SMA200 | 13.572. XU100 yatay kalırsa 30.11'de ~13.380 [EK-4] | 11.333 (−%16,5; gereken +%19,8) | Hayır |
| T2: TSMOM12 (30.11 ay sonu) | XU100(30.11.2026) > 10.898,7 × (1 + 12 aylık nakit getirisi ≈ %45) ≈ **15.800** | 12 ay +%3,8'e karşı nakit ~%45 | Hayır |
| T3: XU100 > SMA50 (5 gün) | 12.691. Yatay kalırsa 30.11'de ~11.700 [EK-4] | −%10,7 | Hayır |
| M1 rezerv | 3 hafta artış | 30,8 → 24,3 mlr $ | Hayır |
| M2 TÜFE | < %2,0 | Ekim %2,58 | Hayır |
| M3 yabancı | 2 hafta net alım, ≥+200 mn $ | Son 6 haftada −334 mn $; son hafta −66 mn $ | Hayır |
| M4 CDS | < 230 | ~248 | Hayır |
| M5 XBANK | > 16.955 | 16.085 (SMA50'de, SMA200'ün −%5,1 altında) | Hayır |
| Bilgi: genişlik | BIST100'de SMA200 üstündeki hisse oranı ≥ %40 | %13 | — |
| Bilgi: sektör endeksleri | SMA200 üstünde olan var mı | Hiçbiri | — |

**Sonuç: KAPALI.** A1 yalnız pilot (r₀ %0,25, en fazla 2, yalnız S2). A2 nakit. A3 kapalı. Hedge gerekmiyor çünkü pozisyon yok.

En olası ilk değişim GEÇİŞ olur. XU100 yatay kalırsa SMA50'ye uzaklık Kasım sonunda ~%3'e iner, yani teknik koşul haftalar içinde gelebilir. Bağlayıcı olan makro tetikler. TSMOM12'nin 2026 içinde açılması pratikte imkânsız: XU100'ün ~+%40 yükselmesi gerekir.

### 3.3 9–13 Kasım günlük plan (saatler TSİ)

| Gün | Saat | Ne yapılır |
|---|---|---|
| **Pzt 9.11** (konsolide 3. çeyrek tabloları için yasal son gün) | 09:00–12:00 | Çekirdeği kur: mevduat dilim 1 (%15) ve banka PPF (%85 = kalıcı %40 + geçici %45). Geçici %45, 16.11, 23.11 ve 30.11 mevduat dilimleri (3 × %15) için vadelerine kadar PPF'te bekler. Pilot bütçesi kalıcı %40'ın içindedir. PPF emri fon izahnamesindeki saat sınırından önce verilir (çoğunda 13:30; teyit edin) |
| | gün içi | İşlem yok. Aracı kuruma §9'daki 6 soru sorulur (teminat, nema, komisyon, şartlı emir, kapanış seansı emri) |
| | 18:20+ | `bist_tarama.py` 06.11 ve 09.11 verisiyle çalıştırılır. Ardından §4.4 bekleme tablosu güncellenir ve TradingView alarmları kurulur. Pazartesi kapanış sinyali ancak şirket akşam bilanço açıklamıyorsa Salı kapanışında uygulanır (§2.1 kural 5). ENJSA, KCHOL, BIMAS, ALARK ve KRDMD'nin bilanço tarihi KAP'tan kontrol edilir |
| **Sal 10.11** | 10:00 / 16:30 | Eylül sanayi üretimi; ABD Ekim TÜFE. İşlem yok |
| | 18:20+ | Bilanço sonrası ilk kapanış. Bekleme listesinde S2 oluşursa giriş **Perşembe 12.11** kapanışında (Çarşamba engelli) |
| **Çar 11.11** | kapanış | **Yeni giriş yok.** MSCI duyurusu 12.11 01:00 |
| **Per 12.11** | 07:00 | MSCI sonuçları okunur. Türkiye'de silinme veya ağırlık azaltma alan hisseler **30.11 kapanışına kadar** A1/A2 girişlerinden çıkarılır. Ekleme yok, çünkü artışlar donduruldu |
| | 10:30 | TCMB Enflasyon Raporu: bilgi amaçlı |
| | 14:30 | Rezerv ve yabancı akımı: M1 ve M3 güncellenir |
| | 18:00 | Salı/Çarşamba S2 sinyalleri varsa pilot girişi (en fazla 2) |
| | akşam | SPK bülteni: kredili işlem esnekliğinin uzatılıp uzatılmadığı |
| **Cum 13.11** | 10:00 | Ödemeler dengesi: bilgi amaçlı |
| | 18:00 | Esneklik bu akşam sona eriyor. **Uzatılmadıysa:** 16–20.11 arasında VİOP dışı (U2) yeni giriş yok, çünkü kredili pozisyonu yüksek orta/küçük hisselerde zorunlu satış riski var. VİOP-47 pilotları serbest |
| | 18:30 | **Haftalık rejim değerlendirmesi** (§3.2 tablosu). Felaket emirleri güncellenir. Haftalık günlük özeti yazılır |

### 3.4 Kasım sonuna kadar

| Tarih | Olay | Plan |
|---|---|---|
| 16.11 | Mevduat dilim 2 | Haftalık rutin |
| 16–20.11 | Kredili işlem esnekliği bittiyse teminat tamamlama ve zorla satış dalgası | U2 girişleri durur; VİOP-47 serbest |
| 18.11 | FOMC tutanakları | Bilgi |
| 19.11 | Bankalar için konsolide 3. çeyrek son günü (HALKB vb.) | Banka sinyallerinde §2.1 bilanço kuralı |
| 20.11 | Haftalık rejim değerlendirmesi | — |
| 23.11 | Mevduat dilim 3 | — |
| **25.11 Çar** | Kasım pay vadelisi devri için son gün | Açık pay vadelisi varsa kapanışta Aralık'a geçilir |
| 27.11 | TCMB Finansal İstikrar Raporu; haftalık rejim değerlendirmesi | — |
| **30.11 Pzt** | VİOP Kasım vade sonu (pay vadelilerinde fiziki teslimat); MSCI değişiklikleri kapanışta | **Ay sonu:** T2 (TSMOM12) testi, A2 küme sıralaması (işlem 01.12 kapanışında), rejim değerlendirmesi, mevduat dilim 4, aylık performans raporu (§7) |
| 03.12 / 10.12 | Kasım TÜFE (M2) / PPK | Rejim girdisi |

---

## 4. Evren, dışlama listesi, kümeler, güncel adaylar

### 4.1 Evren

- **U1 (öncelikli):** VİOP'ta pay vadelisi olan 47 dayanak. Hazırlık §5'teki BIST50 listesi ve tarama (e) tablosu.
  - İçlerinde limit riski yüksek olanlar %25 stop mesafesiyle boyutlanır: GUBRF, TKFEN, BRSAN, HALKB, SASA, ASTOR, VESTL, HEKTS.
  - Gidiş-dönüş makası 20 bps'yi aşanlarda pay vadelisi kullanılmaz: HEKTS 36, SASA 43, ODAS 20 bps (PRATİK_LİSTE risk tablosu).
- **U2 (yalnız spot, ×0,75):** BIST100 üyesi, VİOP'ta olmayan, 60 günlük medyan TL hacmine göre en likit 100 içinde, aşağıdaki dışlama listesinde olmayan hisseler.
  - Pozisyon ≤ 20 günlük medyan günlük TL hacminin %5'i.
  - Bugün likidite eşiği nedeniyle U2 dışında kalanlar: RYGYO (likidite sırası 127), GMTAS (112), TRGYO (149), ISDMR (141), GLYHO (194).

### 4.2 Dışlama listesi (giriş yok; açıksa E4 ile çıkılır)

1. **SPK suç duyurusu yapılan 13 hisse:** KTLEV, GUNDG, DSTKF, OZATD, TRHOL, ODINE, VSNMD, IEYHO, ALKLC, ANELE, PASEU, SELEC, MANAS (v_profesyonel T10).
2. **Fon payı / fiili dolaşım oranı > %20 olan arz baskılı hisseler:** PASEU, KTLEV, ANELE, TEHOL, TRHOL, OZATD, GUNDG, DSTKF, PEKGY, SKYLP, SELEC, KARCL, IEYHO, TMPOL, ODINE, ISVEA, MAGEN, BALSU, ISKPL, DAGI, INFO (tr_profesyonel §4.5; v_profesyonel T6). Ayrıca **GLRMK**: Pusula'nın payı fiili dolaşımın %22'si (tr_profesyonel §6).
3. **Grup ve kayyum şirketleri:** TERA, TEHOL, TRHOL, HEDEF, HDFGS, DSTKF, BIGEN.
4. **Dinamik dışlamalar** (her girişten önce kontrol edilir):
   - Güncel VBTS tedbiri (KAP / Borsa İstanbul "tedbirli hisseler").
   - Son 20 günde ≥3 ardışık tavan kapanış (seri sonrası alım kaybettiriyor).
   - Halka arzdan bu yana < 252 işlem günü.
   - fonoloji/KAP'a göre fon payı / fiili dolaşım > %20.
   - MSCI'dan silinme veya ağırlık azaltma alan hisse (01.12'ye kadar).
   - Aynı hisse aynı anda başka bir stratejide ters yönde açık.

### 4.3 Kümeler (dalga_bist §1; V = VİOP'ta var) ve korelasyon blokları

| Küme | Üyeler | 12 ay RS (5.11) | Sıra |
|---|---|---|---|
| RAFİNERİ | TUPRS V, PETKM V, AYGAZ, TRCAS | +%26,5 | 1 |
| HOLDİNG | KCHOL V, SAHOL V, DOHOL V, AGHOL, ALARK V, TKFEN V, NTHOL, GLYHO | +%23,9 | 2 |
| KOZA_ALTIN | TRALT V, TRMET V, TRENJ | +%18,9 | 3 |
| PERAKENDE | BIMAS V, MGROS V, SOKM V, MAVI, CRFSA | +%17,6 | 4 |
| BANKA | AKBNK V, GARAN V, YKBNK V, ISCTR V, VAKBN V, HALKB V, TSKB V, ALBRK, SKBNK | +%3,9 (126 günlük RS kırılımı) | 5 |
| ÇELİK | EREGL V, KRDMD V, ISDMR, BRSAN V, CEMTS, KCAER, IZMDC | +%3,3 | 6 |
| GYO | EKGYO V, ISGYO, TRGYO, SNGYO, HLGYO, OZKGY, RYGYO | −%1,7 | 7 |
| TELEKOM | TCELL V, TTKOM V | −%5,0 | 8 |
| SAĞLIK | SELEC (dışlanmış), DEVA, ECILC, LKMNH, MPARK | −%8,5 | 9 |
| ELK_ÜRETİM | AKSEN V, ENJSA V, ZOREN, ODAS V, AYDEM, AKENR | −%12,5 | 10 |
| GIDA | ULKER V, AEFES V, CCOLA, TATGD, TUKAS, BANVT, PNSUT | −%12,9 | 11 |
| HAVACILIK | THYAO V, PGSUS V, TAVHL V, CLEBI | −%13,2 (126 günlük RS kırılımı) | 12 |
| TEKNOLOJİ, OTOMOTİV, SAVUNMA, SİGORTA, ÇİMENTO, ELK_EKİPMAN, OTO_YAN, YENİLENEBİLİR, GÜBRE, KİMYA, BEYAZ_EŞYA, CAM_SERAMİK | dalga_bist §1'deki gibi | −%15,6 … −%59,7 | 13–24 |

- **Bu taslağın eki: ENERJİ_DAĞITIM.** Bugün trend şablonunu tam geçen üç hisse aynı işte: ENJSA, AHGAZ, ENERY (doğalgaz/elektrik dağıtımı). Kümeleme sınırı açısından **tek küme** sayılırlar. Korelasyonları ölçülmedi; ihtiyat kuralı.
- **Korelasyon blokları** (dalga_bist §5; günlük korelasyon 0,70–0,79):
  - **Blok 1:** BANKA + HOLDİNG + HAVACILIK + TELEKOM + GYO.
  - **Blok 2:** ELK_EKİPMAN + YENİLENEBİLİR + TEKNOLOJİ + ELK_ÜRETİM.
  - **Blok 3:** sanayi kümeleri.
  - **Ayrıştırıcılar:** RAFİNERİ (bankayla fazla getiri korelasyonu −0,42), SAVUNMA, KOZA.
- Düşen piyasada RS liderliği büyük ölçüde düşük beta demektir; örneğin RAFİNERİ'nin betası 0,55 (dalga_bist §5).

### 4.4 Güncel adaylar (05.11 kapanışı; Cuma kapanışından sonra yeniden hesaplanacak)

**Bugün sinyal veren (B52 + TT) VİOP-47 ya da U2 hissesi: YOK.** Test tanımıyla en likit 150 hisse içinde 05.11'de yeni 52 haftalık kapanış zirvesi yapan hisse yok. Tetik = kapanış > 52 haftalık kapanış zirvesi (gerçek fiyat). TT = test tanımıyla 7 koşulun kaçı sağlanıyor [EK-4]. Kaynak: `tarama/bist_tarama_20261105.csv`.

| Hisse | Evren | Küme / blok | Kapanış | **Tetik (kapanış >)** | Gereken | TT | Eksik | Not |
|---|---|---|---|---|---|---|---|---|
| **ENJSA** | U1 | ENERJİ_DAĞITIM / ELK_ÜRETİM | 119,30 | **127,00** (17.04.2026) | +%6,5 | 7/7 | — | Tek VİOP şablon adayı. Bilanço ≤9.11 akşamı. Pay vadelisi ima taşıma oranı anormal → spot. β 0,60; yılda 0,3 limit günü |
| **AHGAZ** | U2 | ENERJİ_DAĞITIM | 46,00 | **48,70** (12.10.2026) | +%5,9 | 7/7 | — | Likidite sırası 74; yalnız spot, ×0,75 |
| **ENERY** | U2 | ENERJİ_DAĞITIM | 13,80 | **14,60** (12.10.2026) | +%5,8 | 7/7 | — | Likidite sırası 38; yalnız spot, ×0,75. ATR %4,3 (yüksek) |
| KCHOL | U1 | HOLDİNG (2.) / Blok 1 | 202,30 | **225,50** (11.09.2026) | +%11,5 | 6/7 | Fiyat > SMA50 (211,11) | Pay vadelisi çok likit (ima %27,1) |
| GARAN | U1 | BANKA / Blok 1 | 142,00 | **158,59** (03.02.2026) | +%11,7 | 3/7 | Ortalama dizilimi, dip | Kırılırsa yalnız **S1, yarım boy**. Zirve Şubat 2027 başında pencereden çıkar |
| MPARK | U2 | SAĞLIK | 429,25 | **495,00** (12.05.2026) | +%15,3 | 5/7 | SMA dizilimi | — |
| ALARK | U1 | HOLDİNG / Blok 1 | 101,30 | **117,40** (11.09.2026) | +%15,9 | 6/7 | Fiyat > SMA50 (106,08) | — |
| THYAO | U1 | HAVACILIK / Blok 1 | 297,00 | **348,25** (07.07.2026) | +%17,3 | 2/7 | Dizilim, RS | Kırılırsa S1 |
| BIMAS | U1 | PERAKENDE (4.) | 369,25 | **433,75** (23.09.2026) | +%17,5 | 6/7 | Fiyat > SMA50 (402,11) | — |
| BRSAN | U1 | ÇELİK | 649,00 | **769,50** (10.02.2026) | +%18,6 | 5/7 | P > 50, 150 > 200 | Yılda 8 limit günü → stop %25 |
| TUPRS | U1 | RAFİNERİ (1.) | 331,75 | **409,90** (18.09.2026) | +%23,6 | 6/7 | Fiyat > SMA50 (381,02) | XU030 hedge'i çalışmıyor |
| KRDMD | U1 | ÇELİK | 36,72 | **47,48** (09.09.2026) | +%29,3 | 6/7 | Fiyat > SMA50 | ATR %5 → stop %25 |

Okuma:
- Tetiklere en yakın üç isim aynı küme (ENERJİ_DAĞITIM). Küme sınırı KAPALI'da 1, GEÇİŞ ve AÇIK'ta 2 pozisyon (§5).
  - Seçim önceliği: önce U1 (VİOP-47), eşitlikte RS yüzdeliği yüksek olan.
  - Bugünkü KAPALI rejimde üçü birden tetiklenirse yalnız ENJSA alınır. GEÇİŞ'te ikinci isim AHGAZ olur (RS 0,98; ENERY 0,97).
- Banka, holding ve havacılık bloğu rejim dönüşünün ilk sinyallerini verir. Bu üç küme tek risk bloğudur.

---

## 5. Risk sınırları

| Sınır | KAPALI | GEÇİŞ | AÇIK | Kaynak / not |
|---|---|---|---|---|
| İşlem başı risk r₀ (hesabın %'si) | 0,25 | 0,50 | 1,00 (ölçekleme sonrası azami 1,50; §7) | seytan §3.5 (pozitif çarpık sistemde %0,5–1); boyut bu taslağın kararı |
| A1 toplam açık risk | %0,5 | %2 | %6 | — |
| Küme başına | 1 | 2 pozisyon | 2 pozisyon ve ≤ 2 × r₀ risk | Kümeler tek bahis (seytan §3.6) |
| Korelasyon bloğu başına (Blok 1 vb.) | 1 | 3 pozisyon | 3 pozisyon ve ≤ 2,5 × r₀ risk | dalga_bist §5 |
| Brüt uzun nominal (A1+A2+A3) | ≤%5 | ≤%15 | **≤%60** | **Stres kuralı:** iki ardışık taban (−%19) senaryosunda kayıp ≤ hesabın %11–12'si |
| Hedge'siz net beta-nominal | — | — | ≤%50; aşılırsa H2 freni | — |
| Tek pozisyon nominali | %1,7 | %3,4 | %15 | — |
| Limit riskli hisse | En fazla 1 açık, stop mesafesi %25 | aynı | aynı | Limit günü sayıları: PRATİK_LİSTE risk tablosu |
| Aylık kayıp sınırı (bütün A kollarının takvim ayı içindeki piyasa değeri kaybı) | Hesabın %0,5'i | %1 | %3 | Aşılırsa ay sonuna kadar yeni giriş yok; mevcut stoplar işler |
| Kol düşüşü (A kollarının zirveden kümülatif kaybı, hesap %'si) | — | — | ≥%10 → r₀ yarıya, en az 2 ay. ≥%15 → yeni giriş durur, §7 incelemesi | Beklenen düşüş bandı: hesap düzeyinde −%10…−%20 (§8) |
| Pay vadelisi başlangıç teminatı toplamı | ≤%5 | ≤%10 | ≤%20 | — |
| Serbest teminat | ≥ 2 × sürdürme teminatı | aynı | aynı | Gap'te teminat çağrısına karşı |
| Kaldıraç | **Brüt nominal ≤ hesabın 1,0 katı; kredili spot yok** | | | v_bist #3 |
| Bütün stratejiler dahil toplam açık risk | ≤%8 | | | 4 lead-lag sinyali ve başka kollar dahil |

**Limit kilidi (gap) riski.** Spot taban kilitliyken pay vadelisi de çoğu zaman kilitlidir: olay günlerinin %83'ünde (PRATİK_LİSTE §2). Pay vadelisi çıkış yolu değildir. Bu riskin tek ilacı boyuttur (stop mesafesi %25 ve brüt sınır %60).

Testteki en kötü VİOP-47 işlemi −%25,9 (gerçekçi dolumla −%38,5), yani ~−1,7R ile −2,6R. Pump isimleri dışlanmasaydı bu rakam −%94 olurdu (bist_test §5.2).

---

## 6. Yürütme, maliyet, vergi, kayıt

**Maliyet hedefi.** Gidiş-dönüş toplam maliyet ≤ 25 bps; backtest bu varsayımı kullanıyor (bist_test §1).
- Makas: A sınıfı likit isimlerde 5,6–9 bps, C sınıfında 7–43 bps (PRATİK_LİSTE risk tablosu).
- Komisyon: banka liste fiyatı on binde 8–10 (yön başına 8–10 bps). Aktif müşteride on binde 1–4 tipik (teyitsiz). Üstüne komisyonun %5'i BSMV (hazırlık §5).
- **Kural:** komisyon yön başına on binde 3'ün altında pazarlık edilir. Toplam maliyet 40 bps'yi aşarsa U2 evreni kapatılır ve yalnız A sınıfı isimlerle çalışılır.
- Maliyetin 50 bps'ye çıkması kırılım portföyünde yıllık getiriyi ~1,4 puan düşürüyor (v_bist §2.6). Asıl risk kayma ve tavanda dolum.

**VİOP teminatı.**
- Takasbank asgarisi (02.11.2026'dan geçerli parametreler; hazırlık notu GM 2176 olarak veriyor): XU030 %11,4; pay vadelileri %12,7 (BIMAS) ile %17,0 (HALKB) arası.
- Aracı kurum oranları çok daha yüksek. Örnek, QNB 03.11: XU030 %20, pay vadelilerinin çoğu %33,3, ASTOR/HALKB/VESTL %100, GUBRF %50 (v_bist #16).
- **Kendi aracı kurumunuzdan sözleşme bazında yazılı alın.**

**Vergi (birey).**

| Kalem | Stopaj | Kaynak |
|---|---|---|
| BIST pay alım-satım kazancı | %0 | GVK geçici 67 (süre 31.12.2030'a uzatıldı) |
| Pay ve pay endeksi VİOP sözleşmeleri | %0 | v_capraz #7, #9 |
| F_USDTRY ve diğer VİOP sözleşmeleri | %10 | v_capraz #7 |
| PPF ve 6 aya kadar mevduat | %17,5 | v_capraz #6 |
| DİBS | Yalnız muafiyet döneminde alınana %0 | v_capraz #8 |

Temettü stopajı ayrıdır; aracı kurumdan teyit edin. Hisse kazancı vergisiz, nakit getirisi vergili olduğu için yapı hisse kolları lehine ~5–7 puan vergi avantajı taşır. Bu avantaj engel karşılaştırmasına zaten dahil (§1.1).

**Kayıt.**
1. Her işlem §7.2'deki alanlarla `gunluk_A.csv` dosyasına yazılır.
2. Her akşam o günün VİOP bülteni (`viop_YYYYMMDD.csv`) ve tarama çıktısı arşivlenir.
3. Aylık ekstreler (aracı kurum, MKK e-Yatırımcı) saklanır.
4. Çekirdek getirisi aylık olarak ayrı hesaplanır, çünkü bütün kol performansları çekirdeğe göre ölçülüyor.

---

## 7. Öldürme kriterleri ve ileriye dönük ölçüm protokolü

### 7.1 Hipotez kartı (09.11.2026 tarihli, değiştirilemez)

- **Mekanizma:** Zirve kırılımında yatırımcının yetersiz tepkisi ve çapalanma, kazananı koşturmak; sağ kuyruk (Bessembinder tipi).
- **Evren:** U1 ve U2.
- **Kurallar:** §2.1.
- **Beklenen değerler:** E[R] = +0,3…+0,5R; isabet %42–50; kazanç/kayıp 2–3; AÇIK rejimde yılda 25–50 işlem.
- **Denenen varyant sayısı:** bist_test'te 25 işlem kombinasyonu, 36 portföy varyantı; bu taslakta 4 alt küme × 2 rejim filtresi.
- **Kart değişikliği yeni hipotez sayılır;** eski işlemlerle karıştırılmaz.

### 7.2 Günlük alanları (işlem başına bir satır; eklemeler ayrı satır)

```
islem_id, kol(A1/A2/A3), alt_tip(S2/S1/pilot/ekleme/hedge), hisse, evren(U1/U2), kume, blok,
rejim(KAPALI/GECIS/ACIK), sinyal_tarihi, sinyal_kapanisi, tetik_seviyesi, TT_puani, RS_yuzdelik,
zirveye_uzaklik, giris_tarihi, hedef_fiyat(t+1 kapanis), gerceklesen_fiyat, kayma_bps, arac(spot/F_kodu),
adet_veya_kontrat, nominal_TL, stop_mesafesi(0,15/0,25), R_TL(=nominal×stop), r0, carpan,
ima_tasima_orani(VIOP ise), teminat_TL, en_yuksek_kapanis, MFE_%, MAE_%, cikis_tarihi,
cikis_nedeni(E1..E5/E-ay-sonu), cikis_fiyati, brut_%, komisyon+BSMV_TL, makas_tahmini_TL, devir_maliyeti_TL,
net_TL, net_%, R_katsayisi(=net_TL/R_TL), gun_sayisi, XU030_ayni_donem_%, cekirdek_ayni_donem_% (engel),
placebo_% (aynı tarihlerde VİOP-47 eşit ağırlıklı ortalaması), notlar
```

### 7.3 Aylık rapor

Rapor her ayın son işlem günü hazırlanır. İçeriği:
- E[R] ve bootstrap %90 güven aralığı; isabet; kazanç/kayıp; profit factor.
- En iyi %5 ve %10 işlemin kâr payı (>%50 normaldir).
- Ortalama kayma; çıkışta kayma.
- Engele göre kol getirisi: TL bazında (kol P&L − aynı sermayenin çekirdek getirisi).
- XU030'a göre β ve korelasyon.
- Rejim bazında ayrışma.
- Gerçekleşen düşüşün beklenti bandındaki yeri (§8).

### 7.4 Ölçekleme (boyut artırma) şartları

- 12 ay ve **≥ 40 kapanmış A1 işlemi** tamamlanmadan r₀ rejim tablosunun üstüne çıkarılmaz. Bu süre içinde yalnız küçültme ya da öldürme kararı verilebilir.
- **r₀ 1,0 → 1,25** (AÇIK). Hepsi gerekli: ≥40 işlem; ortalama R ≥ +0,30; placeboya göre fark > 0 ve t ≥ 1,5; kayma ≤ backtest kenarının %25'i; kol düşüşü hiç %10'a ulaşmamış.
- **r₀ 1,25 → 1,50.** ≥100 işlem; ortalama R ≥ +0,30; SPRT (H0: μ=0, H1: μ=+0,4R, α=0,05, β=0,20) H1'i kabul etmiş. Brüt sınır %60'tan %75'e çıkar.
- **Gerçekçi takvim.** +0,4R'lik bir sistemi doğrulamak ~100–200 işlem ister; +0,2R'de ~400 işlem (seytan §3.7). AÇIK rejimde bile bu **2–4 yıl** sürer. Pilot işlemler hipotezi test etmez; yalnız yürütmeyi (kayma, dolum, disiplin) test eder.

### 7.5 Öldürme / küçültme kriterleri (önceden yazılı)

| # | Tetik | Eylem |
|---|---|---|
| K1 | 30 işlemden sonra ortalama R < −0,20 | r₀ yarıya; mekanizma incelemesi |
| K2 | 60 işlemden sonra ortalama R'nin %90 güven aralığının üst sınırı < +0,10 | A1 durur. Yeniden açılması için yeni hipotez kartı gerekir |
| K3 | 100 işlemden sonra ortalama R ≤ 0 | A1 kapanır |
| K4 | Ortalama kayma ve maliyet > 40 bps gidiş-dönüş, ya da backtest brüt kenarının %50'sinden fazla | Yürütme düzeltilir: yalnız A sınıfı isimler, pay vadelisi, emir saatleri. Düzelmezse U2 kapanır |
| K5 | Kol düşüşü (hesap %'si) ≥%10 | r₀ yarıya, en az 2 ay |
| K5 | Kol düşüşü ≥%15 | Yeni giriş durur, inceleme |
| K6 | 12 aylık kol getirisinin XU030'la korelasyonu > 0,7 **ve** XU030 + çekirdek kombinasyonuna göre kalıntı alfa ≤ 0 | Kol yalnız beta taşıyor demektir. A1 durur; gerekirse yerine A3a konur |
| K7 | Mekanizma değişikliği: kırılım günlerinde sistematik kurumsal satış (MSCI çıkışı, statü düşüşü), ya da SPK/BIST'in fiyat limitini veya açığa satış rejimini değiştirmesi | t-istatistiğine bakmadan inceleme ve gerekirse durdurma |
| K8 | A2 kol kaybı hesabın ≥%5'i | A2 kapanır (§2.2) |
| K9 | Toplam hesabın engele göre kaybı ≥%25 (bütün stratejiler) | Bütün kollarda boyut yarıya. ≥%35'te çekirdek dışındaki her şey kapanır (seytan §5.2-8) |

---

## 8. Beklenen sonuç aralıkları ve engelle karşılaştırma

### 8.1 Önümüzdeki 12 ay (bugünden), hesap düzeyinde, engele göre puan farkı

Senaryo olasılıkları öznel (tr_makro §5.2). Kol katkıları bu planın boyutlandırmasıyla kaba tahmindir.

| Senaryo (olasılık) | Rejim yolu | A kollarının engel üstü katkısı (hesabın puanı) | Açıklama |
|---|---|---|---|
| S1 krizin sönümlenmesi (%35) | 1–3 ay içinde GEÇİŞ, sonra AÇIK. Banka/holding/havacılık kırılımları | **+5 … +15** | Ortalama brüt %30–50 nominal × liderlerde %20–40 hareket. Kuyruktan 1–2 büyük işlem gelirse üst uç |
| S2 yatay kanama (%40) | KAPALI kalır; seyrek pilotlar | **−1 … +1** | Pilotların çoğu %15 iz-stopla kapanır. Toplam risk ≤%0,5 |
| S3 kontrollü kur hızlanması (%15) | Nominal TL hisse yatay/yukarı, dağınık kırılımlar | **−2 … +4** | Dövizli bilanço liderleri kırılabilir; banka bloğu zayıf |
| S4 kırılma (%10) | KAPALI; gap'ler | **−1 … −4** (KAPALI'da). AÇIK'a geçtikten sonra gelirse **−6 … −11** | Brüt %60 × iki taban stresi |
| **Beklenen değer** | | **≈ +2 puan** (kaba aralık +0…+4) | %80 aralık ≈ **−4 … +12** |

**Toplam hesap TL getirisi, 12 ay:** engel ~%31–38 + yukarıdaki fark → **~%27–50**. Medyan senaryoda engele çok yakın.

Bu planın 12 ay içinde çekirdeğin altında kalma olasılığı ~%40–50. Sebep pozitif çarpıklık: kazanç birkaç işlemde, ceza ise çok sayıda küçük kayıpta gelir (seytan §3.5).

### 8.2 Uzun vade (3–5 yıl, rejim normale dönerse)

- **A1:** VİOP-47 kırılım portföyü 2010–26'da vergi sonrası engelin yılda ~+17 puan üstünde (1/6 ağırlıkla) [EK-2]. Bu planın boyutu (×0,4–0,6) ve %30–50 yanlılık iskontosuyla **+4…+8 puan/yıl**. Yüksek reel faiz dönemlerinde **−3…+3**.
- **A2:** AÇIK rejimde +0…+2 puan.
- **A3a:** +0…+2 puan.
- **Hesap düzeyinde engele göre düşüş:** medyan −%10…−%15, kötü yıl −%20.
- **İşlem bazında:** isabet %42–50; ortalama kazanç ortalama kaybın 2–3 katı; 8–13 işlemlik kayıp serileri olağan. Kârın yarıdan fazlası en iyi %5 işlemden gelir.
- **Gerçekçi tavan:** 2017, 2020, 2022 gibi negatif reel faizli boğa yıllarında kol nominali üzerinden +%100…+%280 mümkün oldu (bist_test §5.2 yıllık tablo). Bu planın brüt sınırıyla hesap düzeyinde **+%40…+%100**. Ancak bu yılları önceden bilmek mümkün değil; plan bunlara dayanamaz.

### 8.3 Bu tahminleri yanlış çıkarabilecekler

1. **Yanlılık.** VİOP-47 bugünkü listedir, yani geçmişin kazananları; evrende hayatta kalma yanlılığı var.
2. **Kenar çürümesi.** 52 hafta sinyalinin long-only anlamlılığı büyük ölçüde 2022'ye dayanıyor (v_bist #24).
3. **Henüz görülmemiş rejim.** MSCI statü düşüşü (Haziran 2027) ve fon tasfiye arzı (~17.03.2027'ye kadar) likit liderlerde bile kırılımları boğabilir.
4. **Yürütme.** Kapanış seansında kayma, tavan ve tabanda dolmama.
5. **Engelin kendisi.** Faiz indirimleri hızlanırsa engel düşer (lehe); stopaj indirilirse yükselir.

---

## 9. Pazartesi 09.11.2026 kontrol listesi (tek sayfa)

**Hafta sonu (Cuma 18:20 sonrası – Pazar)**
- [ ] `python3 bist_tarama.py --veri ~/bist_veri --cikti ../tarama` (06.11 kapanışıyla). Hesaplanacaklar: §4.4 tablosu, tetikler, TT puanları, SMA50/200, XBANK.
- [ ] VİOP bülteni `viop_20261106.csv` indirilir. F_XU030 Aralık uzlaşması ve ima faiz yeniden hesaplanır; Pazartesi kararında bu değer kullanılır.
- [ ] TradingView alarmları kurulur (kapanış bazlı, "bar kapanışında bir kez"): ENJSA > 127,00; AHGAZ > 48,70; ENERY > 14,60; KCHOL > 225,50; GARAN > 158,59; MPARK > 495,00; ALARK > 117,40; THYAO > 348,25; BIMAS > 433,75; BRSAN > 769,50; TUPRS > 409,90; KRDMD > 47,48. Tarama sonrası değişen seviyeler güncellenir. Ayrıca XU100 > 12.691 (SMA50) ve XU100 > 13.572 (SMA200).
- [ ] `gunluk_A.csv` şablonu açılır (§7.2) ve hipotez kartı (§7.1) tarihlenir.

**Pazartesi sabah (09:00–12:00)**
- [ ] Mevduat dilim 1: hesabın %15'i, 32 gün, en iyi oranı veren 1–3 banka. Örnek tutarlar: 150 bin / 750 bin / 3 mn TL.
- [ ] Banka iştiraki PPF: hesabın %85'i (kalıcı %40 + 16/23/30.11 mevduat dilimleri için geçici %45).
  - Kontrol: fon kurucusu bir mevduat bankasının iştiraki; KAP portföy raporunda grup ihracı yok; fon tasfiye listesinde değil; işlem saat sınırı.
  - Pilot bütçesi (≤ hesabın %3,4'ü) kalıcı %40'ın içindedir.
- [ ] Aracı kuruma yazılı sorulacaklar:
  1. VİOP teminatı olarak PPF/DİBS kabul ediliyor mu, kesinti oranı ne?
  2. Nakit teminata nema var mı, oranı ne?
  3. Pay vadelisi ve XU030 kurum teminat oranları (sözleşme bazında)?
  4. Spot ve VİOP komisyonu (hedef < on binde 3)?
  5. Kapanış seansı emri önceden girilebiliyor mu?
  6. Şartlı (stop-limit) satış emri ve süresi?
- [ ] DİBS stopajının %0 olduğu yazılı teyit edilmeden DİBS alınmaz.

**Pazartesi gün içi**
- [ ] İşlem yok. Ekran takibi yok.

**Pazartesi akşam (18:15–19:00)**
- [ ] Alarmlar okunur. Tetik + TT 7/7 + dışlama listesinde değil + bilanço kuralı sağlanıyor ise → **pilot** (r₀ %0,25), en fazla 2, aynı kümeden en fazla 1.
  - Giriş t+1 kapanış seansında. Çarşamba 11.11'de giriş yok.
- [ ] Rejim tablosu (§3.2) doldurulur. Beklenen sonuç: **KAPALI**.
- [ ] KAP: 9.11 akşamı açıklanan bilançolar (ENJSA, KCHOL, BIMAS, ALARK, KRDMD ve diğer VİOP dayanakları) not edilir. Bilanço sonrası ilk kapanış Salı 10.11.

**Hafta içi sabitler**
- [ ] Per 12.11 07:00 MSCI listesi → dinamik dışlama. 14:30 rezerv ve yabancı akımı → M1, M3.
- [ ] Cum 13.11 akşam: SPK kredili işlem kararı. Uzatılmadıysa 16–20.11 arasında U2 girişi yok.
- [ ] Cum 13.11 18:30: haftalık rejim değerlendirmesi, felaket emirleri, günlük özeti.

**Asla**
- Kredili spot.
- Dışlama listesindeki hisse.
- Tavan serisi sonrası halka arz alımı.
- Bekleme modunda tam boy giriş.
- Nominalin spot formülünü aşması.
- Vadede fiziki teslimata kalmak.
- Hedge'i kalıcı pozisyona çevirmek.

---

## 10. Kaynaklar ve ek hesaplar

### 10.1 Kısaltmalar

Hepsi `/home/user/Xxxx/raporlar/` altında.

| Kısaltma | Dosya |
|---|---|
| **bist_test** | `2026-11-06_kazanc_stratejileri/ajanlar/bist_test.md`; kod ve işlem listeleri `hesaplar/bist_test/` |
| **swing** | `.../ajanlar/bist_swing_kenarlar.md` |
| **dalga_bist** | `.../ajanlar/dalga_bist.md`; `hesaplar/dalga_bist/` |
| **tr_makro** | `.../ajanlar/tr_makro_engel.md` |
| **tr_profesyonel** | `.../ajanlar/tr_profesyonel.md` |
| **seytan** | `.../ajanlar/seytan_taban_oranlar.md` |
| **olay_halka_arz**, **bist_kim** | `.../ajanlar/olay_halka_arz.md`, `.../ajanlar/bist_kim_kazaniyor.md` |
| **v_bist, v_capraz, v_dalga, v_profesyonel** | `.../dogrulama/` (çelişkide esas) |
| **hazırlık** | `.../uygulama/bist_hafta_hazirlik.md` (§0-8'deki XU030 iskontosu yanlış; §1.1 nota bakın) |
| **tarama** | `.../uygulama/tarama/bist_tarama_20261105.md/.csv`; betik `.../uygulama/kod/bist_tarama.py` |
| **PRATİK_LİSTE** | `2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md` ve `risk_ve_boyut_tablosu.csv` |
| **komite** | `2026-10-28_viop_komite_raporu.md` |
| **Birincil veri** | Borsa İstanbul VİOP bülteni `https://www.borsaistanbul.com/data/vadeli/viop_20261105.csv` (varsayılan başlıklarla indirildi) |

### 10.2 Bu taslak için yapılan ek hesaplar (scratchpad; repoda değil)

Betikler `/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/bistA/` altında, `an1.py` – `an5.py`. Girdiler bist_test'in işlem listeleri (`t03_islemler_S2_iz15*.csv`), fiyat paneli ve dalga_bist'in küme göreli endeksidir. Yeni piyasa verisi çekilmedi; tek istisna 5.11 VİOP bültenidir.

| Kod | İçerik |
|---|---|
| **EK-1** | S2 + iz %15 işlemleri, bugünkü VİOP-47 listesi alt kümesi. Ana / gerçekçi dolum / kohort 2009 evrenleri; 2022 hariç ve 2024–26 dilimleri; XU100 > SMA200 ayrımı |
| **EK-2** | Aynı alt kümeyle 6 ve 10 slotlu portföy. Risksiz faiz günlük bileşik olarak düzeltildi (v_bist §2.1). Boş nakit %17,5 stopaj sonrası. TSMOM12 ve SMA200 kapıları |
| **EK-3** | Kırılım işlemleri sinyal günündeki 12 aylık küme RS sırasına göre ayrıştırıldı. Sonuç: küme filtresi kırılım işlemine katkı yapmıyor |
| **EK-4** | 05.11 itibarıyla test tanımıyla TT (7 koşul), 52 haftalık zirve ve tarihi; SMA50/200'ün yatay piyasa varsayımıyla 30.11 projeksiyonu; TSMOM12 eşiği (XU100 28.11.2025 = 10.898,7) |
| **EK-5** | VİOP-47 işlemlerinde en uzun kayıp serisi (13), eşzamanlı açık işlem sayısı (ortalama 6,4, medyan 5), R dağılımı (yüzdelik 5 / 50 / 95 = −1,23 / 0 / +5,45) |
| **EK-6** | 5.11 resmi bülteninden pay vadelisi uzlaşmaları, açık pozisyon, işlem hacmi ve spot kapanışa göre ima taşıma oranları. Saat farkı nedeniyle ±1–2 puan hata payı var |

**Çekinceler.**
- VİOP-47 alt kümesi bugünkü listeye göre seçildi: ileriye bakma ve hayatta kalma yanlılığı var, sonuçlar yukarı yanlı.
- İşlem listeleri bist_test'in hatalarını taşıyor: 2020 öncesi limit modeli ±%9,5 kabul edilmiş (gerçekte ±%20), kurumsal işlem temizliği kusurlu (v_bist §2.2–2.3).
- Ek hesaplar örneklem içidir. Rakamlar bir "kanıt" değil, beklenti aralığının kaba ayarıdır.
