# Yöntem protokolü: BIST elektrik hisselerinde 1–3 günlük öncülük (lead-lag) sinyalleri

Bu belge hesaptan ÖNCE yazıldı. Bütün analiz ajanları buna uyar. Sapma olursa çıktıda “SAPMA:” diye belirtilir.

## 0. Soru ve işlem profili

- Kullanıcı sinyalin geldiği gün (t) **kapanışta** pozisyon açar, **1, 2 ya da 3 işlem günü** taşır, kapanışta çıkar.
- Araçlar: spot hisse (yalnız AL) ve VİOP pay vadelisi (AL ve SAT). XELKT'de VİOP kontratı olanlar: **AKSEN, ENJSA, ODAS**. Endeks tarafında yalnız XU030 vadelisi var; XELKT'nin vadelisi ya da fonu yok.
- Aranan şey: (a) elektrik hisseleri arasında, (b) hisse ↔ XELKT, (c) hisse/XELKT ↔ XU030 arasında, t günü bilinen bir bilginin t+1…t+3 getirisini öngörmesi.
- Kapsam dışı: gün içi al-sat, açılışta giriş, dış sürücüler (PTF, doğal gaz, kur). Bunlar yalnız kontrol değişkeni olabilir.

## 1. Evren

- XELKT'nin 20.11.2026 üyeleri (42 hisse, KAP): A1YEN AHGAZ AKENR AKFYE AKSEN AKSUE ALFAS ARFYE AYDEM AYEN BESTE BIOEN BIGEN CONSE CWENE CANTE CATES ARASE ECOGR ENDAE ENJSA ENERY ESEN GWIND HUNER ENTRA IZENR KLYPV LYDYE MAGEN MASFN METEN MOGAN NTGAZ NATEN ODAS PAMEL SMRTG TATEN VEYAS ZEDUR ZOREN.
- Komşu girdiler (yalnız sinyal kaynağı): ASTOR, ALARK, EUPWR, GESAN (elektrik ekipmanı / enerji holdingi).
- Endeksler: XELKT, XU030, XU100, XUTUM, XUHIZ; XU030 yakın vade vadelisi.
- Bilinen sınır: evren bugünkü üyelerden oluşuyor (hayatta kalma yanlılığı). Endeksten çıkan hisseler yok. Raporlarda belirtilir.

## 2. Veri dönemleri (veri gözetlemesine karşı üç parça)

| Parça | Dönem | Kim görür |
|---|---|---|
| IS (keşif) | başlangıç → 2022-12-30 | 2. dalga |
| OOS-1 (doğrulama) | 2023-01-02 → 2025-06-30 | 2. dalga |
| **Kasa (holdout)** | 2025-07-01 → veri sonu | **yalnız 3. dalga**; 2. dalga ajanlarına verilmez |

- 2. dalga ajanları yalnız `panel_dev/` klasörünü kullanır (2025-06-30'da kesik). Kendileri veri indirmez, `panel_full/` ve `raw/` klasörlerine bakmaz.
- Kural seçimi, eşik ve parametre ayarı yalnız IS üzerinde yapılır. OOS-1 yalnız raporlanır; OOS-1'e bakıp parametre değiştirilirse “SAPMA” yazılır.

## 3. Getiri ve zaman tanımları

- `r_cc(t)` = düzeltilmiş kapanış(t)/düzeltilmiş kapanış(t−1) − 1. `r_co(t)` = açılış(t)/kapanış(t−1) − 1 (gece). `r_oc(t)` = kapanış(t)/açılış(t) − 1 (gün içi).
- Sinyal yalnız t günü kapanışına kadar bilinen veriden kurulur. Giriş fiyatı = t kapanışı. İleri getiriler: `f1 = c(t+1)/c(t) − 1`, `f2 = c(t+2)/c(t) − 1`, `f3 = c(t+3)/c(t) − 1`. Ayrıca `f1` gece (`r_co(t+1)`) ve gün içi (`r_oc(t+1)`) diye ayrılır.
- VİOP bacağı için ayrıca uzlaşmadan uzlaşmaya getiri hesaplanır (aynı kontrat içinde; vade geçişinde sıçrama yok).
- **Uygulanabilirlik (dolum) kuralı:**
  - Hedef hisse t günü **tavanda kapandıysa** alım gerçekleşmez: o gözlem “dolmaz” sayılır. Tabanda kapandıysa satış gerçekleşmez.
  - Çıkış günü hisse tabanda kilitliyse (uzun pozisyon) çıkış bir sonraki kilitsiz kapanışa kayar.
  - Her tablo iki sütun verir: “hepsi” ve “dolabilir”. Karar “dolabilir” sütununa göre verilir.
  - Halka arzın ilk 20 işlem günü ve hacmi sıfır olan günler hedef olarak kullanılmaz.
- **Kayma (drift) düzeltmesi:** TL bazında hisseler enflasyon nedeniyle koşulsuz olarak yükselir. “Sinyal günlerinin ortalama getirisi > 0” kanıt değildir. Her sonuç şu üç ölçüyle verilir:
  1. ham getiri,
  2. fazla getiri = hedefin getirisi − aynı günlerde hedefin koşulsuz ortalaması (ya da aynı gün eşit ağırlıklı XELKT sepeti),
  3. piyasadan arındırılmış getiri = hedef − β·XU100 (β: 250 günlük, 1 gün gecikmeli).
- Karar ölçüsü: (2). Ham getiri yalnız bilgi içindir.

## 4. Maliyet varsayımları (gidiş-dönüş, bps; 1 bps = %0,01)

| Senaryo | Spot | VİOP AKSEN | VİOP ENJSA | VİOP ODAS |
|---|---|---|---|---|
| düşük | 10 | 8 | 10 | 25 |
| **temel** | **25** | **15** | **18** | **35** |
| bireysel/muhafazakâr | 50 | 25 | 25 | 45 |

- Spot maliyetine fiyat adımı da eklenir: düşük fiyatlı hisselerde bir adım 20–100 bps olabilir. `meta.csv`'deki `tick_bps` yarım adım olarak eklenir (kapanış seansında tek fiyat oluştuğu için “dolabilir” gözlemlerde yarısı alınır).
- Bu rakamlar 1. dalgadaki piyasa yapısı ajanınca doğrulanınca güncellenebilir; güncel tablo `ek/maliyet.md`'dedir.

## 5. İstatistik kuralları

- **Tarih kümelemesi:** havuzlanmış (panel) testlerde gözlemler aynı gün içinde bağımlıdır. t-istatistiği tarihe göre kümelenir ya da önce günlük kesit ortalaması alınıp zaman serisi üzerinden hesaplanır (Fama–MacBeth). Hisse-gün sayısına bölünmüş saf t kullanılmaz.
- Örtüşen tutma süreleri (h=2,3): Newey–West (gecikme ≥ h) ya da örtüşmeyen örnekleme.
- **Çoklu test:** her aile yaptığı test sayısını bildirir. IS p-değerlerine Benjamini–Hochberg (q = 0,10) uygulanır. Aile içi en iyi sonucun şansla çıkma olasılığı ayrıca yer değiştirme (tarihleri blok hâlinde kaydırma/karıştırma) testiyle verilir.
- **Aday olma şartları (hepsi):**
  1. IS'te BH-FDR'den geçer ya da önceden yazılmış tek hipotezse |t| ≥ 2,5.
  2. OOS-1'de aynı yön ve |t| ≥ 1,5; etki büyüklüğü IS'in en az yarısı.
  3. “Dolabilir” gözlemlerde, temel maliyet düşüldükten sonra fazla getiri > 0 ve işlem başına ≥ +15 bps (spot) ya da ≥ +10 bps (VİOP).
  4. En az 40 bağımsız olay (IS+OOS-1), en az 3 ayrı yılda pozitif.
  5. En iyi 10 işlem (ya da en iyi %5) çıkarılınca işaret değişmez.
  6. Tek bir hisseye ya da tek bir döneme (örn. 2020–21 bireysel yatırımcı dalgası) dayanmaz; dayanıyorsa açıkça yazılır.
- Şartları kıl payı kaçıranlar “izleme listesi” olarak ayrıca bildirilir; elenenler de nedenleriyle yazılır. **Olumsuz sonuç da sonuçtur:** “bu ailede kullanılabilir sinyal yok” geçerli bir bulgudur, zorlama yapılmaz.
- Parametre ızgarası küçük ve önceden yazılı tutulur (aşağıda). Izgara dışı denemeler “keşif amaçlı” etiketiyle ayrı raporlanır ve aday olamaz; ancak 3. dalgada kasada sınanmak üzere önerilebilir.

## 6. Sinyal aileleri ve önceden yazılı ızgaralar

Ortak ızgara: tutma h ∈ {1, 2, 3}; eşik z ∈ {1, 1,5, 2} (z = getirinin 60 günlük, 1 gün gecikmeli std'ye oranı) ya da mutlak eşik ∈ {%3, %5, %7}; yön: yukarı ve aşağı ayrı.

- **A1 Hisse → hisse (ikili):** her sıralı (j → i) çifti için `f_h(i)` ~ `r_cc(j,t)`; kontroller: `r_cc(i,t)`, XU100(t). Doğrusal ve eşikli (|r_j| büyük günler). Lider/izleyici matrisi; liderliğin yıldan yıla kalıcılığı.
- **A2 Endeks ↔ hisse:** XELKT(t), hisse-hariç eşit ağırlıklı elektrik sepeti(t), XU030(t), XU100(t), XELKT − β·XU030 (sektöre özgü hareket), büyük elektrik hisseleri sepeti → `f_h(i)`. Ters yön: hisse → XELKT sepeti. Endeks düzeyi: XU030(t) → XELKT(t+1…t+3) ve tersi. Komşular (ASTOR, ALARK, EUPWR, GESAN) → elektrik hisseleri.
- **A3 Kesit:** sektöre göre geride kalanın yetişmesi / öne geçenin geri dönmesi (hisse k günlük getirisi − XELKT k günlük getirisi, k ∈ {1, 3, 5}); büyük → küçük (piyasa değeri ya da hacme göre üçte birlikler, Lo–MacKinlay çapraz otokorelasyonu); yüksek hacimli → düşük hacimli.
- **A4 Olay:** j hissesi tavanda kapanır → sektördeki diğer hisseler t+1…t+3; sektör günü (XELKT ≥ +%3 / ≤ −%3); genişlik (üyelerin ≥ %50'si > +%2); taban bulaşması; hacim patlaması (hacim > 3× 20 günlük medyan) olan hisse → akranları.
- **A5 XELKT / XU030 rotasyonu:** XELKT'nin XU030'a göreli gücü (k ∈ {1, 3, 5, 10} gün) → XELKT sepeti ve AKSEN/ENJSA/ODAS `f_h`; XU030 büyük hareket etti ama XELKT etmedi (gecikme) → ertesi gün yetişme; XELKT 20 günlük zirve/dip kırılımı.
- **A6 VİOP:** AKSEN/ENJSA/ODAS vadelilerinde baz değişimi (uzlaşma − spot kapanış), vadeli hacmi ve açık pozisyon sıçraması → ertesi gün spot ve vadeli; XU030 vadelisi bazı → elektrik hisseleri. Vadelide uzlaşma ile son fiyat farkı ve dolum gerçekçiliği.
- **A7 Gün içi zamanlama:** saatlik veriyle (son ~2 yıl) günün son saati / öğleden sonra getirisi (XU030, XELKT, lider hisseler) → izleyenlerin ertesi günü; t günü sinyalinin 17:50 fiyatıyla hesaplanması kapanış fiyatıyla hesaplanana ne kadar yakın.
- **A8 Birleşik model:** gecikmeli öz/akran/endeks getirileri ve hacimlerle yürüyen pencereli (walk-forward) ridge/lasso ve bir ağaç modeli → ertesi gün kesit sıralaması; en üst beşte birlik AL sepeti. Yalnız ileriye dönük tahminler değerlendirilir.

## 7. Çıktı biçimi (analiz ajanları)

- Kod: `kod/<ajan>/` altında, baştan sona çalışır tek giriş betiği (`run.sh` ya da `main.py`).
- Sonuç tablosu: `ek/<ajan>_sonuc.csv`; sütunlar en az: `aile, sinyal_tanimi, hedef, yon, h, n_IS, ort_fazla_IS_bps, t_IS, n_OOS1, ort_fazla_OOS1_bps, t_OOS1, dolabilir_oran, net_temel_bps_IS, net_temel_bps_OOS1, bh_gecti, yil_pozitif_orani, top10_haric_bps, aday_mi, not`.
- Not: `ek/<ajan>.md` (en çok 600 kelime): ne test edildi, test sayısı, kaç tanesi geçti, adaylar (tam kural: girdi, eşik, hedef, giriş/çıkış), elenenler ve neden, bilinen zayıflıklar.
- 3. dalga için her aday **dondurulmuş kural** olarak yazılır: bir başkasının veriden yeniden kurabileceği kadar açık (formül, pencere, eşik, evren filtresi).
