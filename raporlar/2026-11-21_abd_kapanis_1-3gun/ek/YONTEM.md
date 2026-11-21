# Yöntem planı (hesaptan önce yazıldı) — ABD piyasası, kapanış sinyali, 1–3 gün taşıma

Sürüm 1 (taslak, 21.11.2026). Hesaplamalar başlamadan önce yöntem denetçisinin itirazlarıyla güncellenecek. Sonuçlar görüldükten sonra bu dosyadaki eşikler değiştirilmez; değişiklik olursa "sapmalar" başlığına yazılır.

## 1. Profil ve soru

- Yatırımcı gün içi işlem yapmıyor. Karar ABD kapanışında (16:00 ET; TSİ 00:00 kış, 23:00 yaz) veriliyor, pozisyon 1–3 işlem günü taşınıyor.
- Soru: ABD'de işlem gören ETF ve hisselerde, kapanışta bilinen bir sinyalle (özellikle lead-lag: bir varlığın hareketi başka bir varlığın sonraki 1–3 gününü öngörüyor mu?) maliyet sonrası anlamlı kazanç bırakan kurallar var mı; hangi araçlarla uygulanır?
- "Ciddi kazanç" ölçüsü: işlem başına net beklenti (bps), yılda işlem sayısı, işlem başına 1σ risk, en kötü işlem, stratejinin en büyük düşüşü. Kaldıraçlı ETF kullanımı ayrı satırda raporlanır.

## 2. Veri

- Günlük açılış/yüksek/düşük/kapanış/hacim ve düzeltilmiş kapanış, Yahoo chart API, 2005-01-01 → 2026-11-20. Evren ~460 kod (geniş endeks, sektör, tema, faktör, kaldıraçlı/ters, çapraz varlık, ülke ETF'leri; göstergeler; ~230 hisse, tema kümeleriyle).
- Düzeltilmiş açılış = açılış × (düzeltilmiş kapanış / kapanış).
- **Kapanış saati sınıfı (ileriye bakma önlemi):**
  - `ABD16`: ABD hisse ve ETF'leri (16:00 ET kapanış). Sinyal girdisi olarak aynı gün kullanılabilir.
  - `ONCE`: ABD kapanışından önce kapanan seriler (Asya/Avrupa endeksleri; CBOE faiz endeksleri ^TNX vb. 15:00 ET). Aynı gün kullanılabilir.
  - `SONRA`: günlük çubuğu ABD kapanışından sonra kapanan seriler (BTC-USD ve diğer kripto, =X döviz, =F vadeli). Sinyal girdisi olarak **yalnız 1 gün gecikmeli** kullanılır; aynı gün bilgi için ETF vekilleri kullanılır (IBIT/GBTC/BITO, UUP/FXE/FXY, USO/BNO, GLD/SLV, CPER, TLT/IEF, VIXY/VXX).
  - ^VIX ailesi 16:15 ET'de kapanır: birincil testte kullanılır, ayrıca VIXY ile ve 1 gün gecikmeli sağlamlık testi yapılır.
- Bilanço tarihleri: SEC EDGAR 8-K (madde 2.02) kabul zaman damgası (seans öncesi / seans sonrası ayrımı). Konumlanma verisi: SqueezeMetrics DIX/GEX (kapanıştan sonra yayımlanır → giriş ertesi açılış).
- Evren bugünden seçildi (hayatta kalma yanlılığı). Bu yüzden birincil ölçü **korunmalı (hedge'li) getiri** ve göreli sinyallerdir; yalnız uzun yönlü mutlak getiriler bu yanlılıkla işaretlenir.

## 3. Getiri tanımları ve giriş varyantları

- A1 (birincil): giriş t kapanışı, çıkış t+h kapanışı, h ∈ {1,2,3}. Getiri düzeltilmiş kapanıştan.
- A2: giriş t+1 açılışı, çıkış t+h kapanışı (kapanışı görüp emri sonradan veren yatırımcı).
- A3: giriş t+1 kapanışı, çıkış t+1+h kapanışı (bir gün gecikme; sinyalin ömrü).
- Ayrıştırma: t kapanış→t+1 açılış (gece) ve t+1 açılış→kapanış (gün içi) payı.
- Korunmalı getiri: hedef Y için r_Y − β·r_M; M = SPY (hisse ve sektörler için ayrıca kendi sektör ETF'i), β 250 günlük kayan pencere, **1 gün gecikmeli**. Korunmasız getiri de raporlanır.

## 4. Dönemler

- IS (keşif): 2010-01-01 – 2019-12-31. OOS (doğrulama): 2020-01-01 – 2023-12-31. Son dönem (kilitli): 2024-01-01 – 2026-11-20; yalnız OOS'tan geçen sinyaller için açılır ve "zayıflama" kontrolü olarak raporlanır.
- 2005–2009 verisi yalnız stres testi için (2008).
- Kısa geçmişli araçlar (2021 sonrası listelenenler): ayrı sınıf, en fazla "DÜŞÜK" güven alabilir.
- Rejim koşulu (önceden belirlenmiş): VIX < 20, 20–30, > 30. Bugünkü rejim (VIX 35,9) için koşullu sonuç ayrıca verilir.

## 5. Sinyal aileleri (önceden yazılı)

| Aile | Tanım | Sinyal biçimi |
|---|---|---|
| A. Lider → takipçi | X'in t günü getirisi Y'nin sonraki h gününü aynı yönde öngörür | z_X = r_X,t / σ60(X); eşik \|z\| > 1 ve > 2; ayrıca sürekli (eğim) |
| B. Göreli gecikme / çift dönüşü | u = r_Y − β·r_X artığının k ∈ {1,3,5} günlük toplamı; z > 1,5 → ters yönde (dönüş) ya da aynı yönde (yakalama); iki yön de test edilir | z-skoru, eşik 1,5 ve 2 |
| C. Çapraz varlık → endeks/sektör | Kredi, faiz, dolar, petrol, altın, bakır, kripto, volatilite vadesi (VIX/VIX3M) | A ile aynı |
| D. Kendi serisinde uç hareket | Büyük düşüş/yükseliş, üst üste k gün, RSI(2), 200 günlük ortalamaya göre konum; VIX rejimiyle | Olay çalışması |
| E. Takvim/olay | Ay dönümü, FOMC öncesi, opsiyon vadesi haftası, tatil öncesi, haftanın günü, çeyrek sonu yeniden dengeleme | Olay çalışması |
| F. Volatilite ürünleri | VIX vade yapısı → VXX/SVXY/UVXY | Eşik |
| G. Bilanço | İlk tepki günü kapanışında giriş: hissenin kendisi (1–3 gün sürüklenme) ve henüz açıklamamış emsalleri | Olay çalışması |
| H. Konumlanma | DIX, GEX → SPY/QQQ; giriş ertesi açılış | Eşik (çeyreklikler) |
| S. Sistematik tarama | Evrendeki bütün sıralı (X,Y) çiftleri × h × iki biçim (A ve B) | Aşağıdaki çoklu test kuralı |

Literatür ajanlarının bulduğu, kaynağı olan kurallar hesaptan önce bu listeye eklenir (`hipotezler.csv`).

## 6. İstatistik

- Birim: sinyal olayı. Pozisyon açıkken gelen yeni sinyal alınmaz (örtüşmeyen işlemler); ayrıca örtüşen tüm olaylarla Newey–West (gecikme h) t-istatistiği.
- Her sinyal için: yılda işlem sayısı, ortalama (bps, brüt ve net), isabet oranı, t, IS/OOS/son dönem ayrı ayrı, en iyi 10 işlem çıkarılınca ortalama ve t, en kötü işlem, strateji bazında en büyük düşüş, çarpıklık.
- Çoklu test: önceden yazılı ailelerde aile içi Benjamini–Hochberg (%5). Sistematik taramada: IS'te BH-FDR %5 → adaylar; OOS'ta aynı yön ve Bonferroni (aday sayısına göre) tek yönlü; sonra son dönem.
- Plasebo: sinyal tarihlerini karıştırma (blok bootstrap) ve aynı oynaklıkta rastgele "lider" ile sahte keşif oranı ölçülür.
- Bağımsız çürütme: ayakta kalan her sinyal, motoru kullanmayan ayrı bir kodla yeniden üretilir; parametre komşuluğu (eşik ±0,5, pencere ±%50), A2/A3 girişleri, maliyet ×2, alt dönemler, en iyi 10 işlemsiz.

## 7. Maliyet

- Bacak başına (tek yön) varsayım, 60 günlük ortalama dolar hacmine göre: > 1 milyar $: 1,5 bps; 200 milyon–1 milyar $: 3 bps; 50–200 milyon $: 7 bps; < 50 milyon $: 15 bps. Kaldıraçlı/ters ETF'lere +1 bps.
- Açığa satışta ödünç maliyeti: yıllık %0,5 (genel), zor ödünç alınan küçük hisselerde yıllık %10 varsayımı ayrıca.
- Korunmalı sinyallerde iki bacağın maliyeti de düşülür. Kaldıraçlı ETF'lerin taşıma maliyeti fiyat serisinin içindedir; ayrıca düşülmez.

## 8. Karar ölçütleri (önceden)

- **UYGUN:** IS ve OOS aynı yön; OOS t ≥ 2,0 ve çoklu test eşiğini geçiyor; OOS'ta ≥ 30 işlem; muhafazakâr maliyetle OOS ve son dönemde net > 0 (son dönem t ≥ 1,0); en iyi 10 işlemsiz t ≥ 1,5; bağımsız kod aynı sonucu veriyor; A2 ya da A3'te tamamen kaybolmuyor (kayboluyorsa "yalnız kapanışta giren için" notu).
- **KOŞULLU:** OOS'tan geçiyor ama son dönemde zayıflıyor, rejime bağlı ya da az sayıda olaya dayanıyor.
- **DÜŞÜK:** IS ve OOS aynı yön ama t < 2 ya da işlem sayısı az.
- **ELENDİ:** diğerleri. Elenenler nedenleriyle raporlanır.

## 9. Bilinen sınırlar

- Günlük veriyle "kapanışta bilinen sinyal" ile "kapanış fiyatından işlem" aynı anda varsayılıyor; gerçekte sinyal ~15:50 ET'de hesaplanır. Ayakta kalanlar için son 60 günün 5 dakikalık verisiyle 15:50 ve 16:00 sinyalleri karşılaştırılır.
- Yahoo verisi: temettü/bölünme düzeltmeleri ve kaldıraçlı ETF ters bölünmeleri kalite kontrolünden geçirilir.
- Geçmiş performans geleceği garanti etmez; kenarlar yayımlandıkça ve kalabalıklaştıkça erir.

## Sapmalar

(boş)
