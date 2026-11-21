# Backtest şartnamesi (ön kayıt) — ABD doğalgaz araçları, kapanışta giriş, 1–3 gün taşıma

Yazan: ana ajan, 21.11.2026. Hesaptan ÖNCE yazıldı. Testler bu listeyle sınırlıdır; liste dışı bulgu "ön kayıtsız keşif" diye ayrı raporlanır ve en çok İZLE etiketi alır.

## 0. Kullanıcı profili (bağlayıcı)
- Karar ABD seans kapanışında (16:00 ET) verilir. Sinyal en geç 15:50–16:00 ET'de bilinen veriye dayanır. t gününün kapanış fiyatının kendisi sinyalde kullanılabilir (kapanışa yakın emir varsayımı); duyarlılık: giriş t+1 açılışında.
- Pozisyon 1, 2 ya da 3 işlem günü taşınır, kapanışta kapatılır. Getiri: kapanış(t) → kapanış(t+h), h = 1, 2, 3.
- Kullanıcı yalnız SATIN ALIR. Düşüş yönü ters ETF (KOLD) alınarak oynanır. Hisselerde yalnız uzun bacak işlenebilir; korumalı (hedge'li) sonuç yalnız teşhis içindir.

## 1. Veri (indirildi, yeniden indirme)
Klasör: `/tmp/claude-0/-home-user-Xxxx/5d057400-14bf-5bed-9672-13b83c353925/scratchpad/ngdata`
- `d_<TICKER>.csv`: günlük, temettü ve bölünme düzeltmeli OHLCV (yfinance, auto_adjust). `=` → `_`, `^` silinmiş (ör. `d_NG_F.csv`, `d_TTF_F.csv`, `d_VIX.csv`).
- `h_<TICKER>.csv`: 60 dakikalık, yaklaşık son 2 yıl (hisse/ETF 2023-12-26'dan, NG=F ve TTF=F 2024-07-01'den). Saat ET, ofsetli.
- `_kapsam.csv`: kapsam tablosu. CTRA ve SWN yok (listeden çıkmış). EXE 2021-02'den (iflas sonrası CHK), GPOR 2021-05'ten, BKV 2024-09, INR 2025-01, VG 2025-01, CEG 2022-01, TLN 2023-06, GEV 2024-03, TTF=F 2017-10, BOIL/KOLD 2011-10, UNL 2010-01, UNG 2007-04.
- İndirme betiği: `raporlar/2026-11-21_dogalgaz_1-3gun/kod/00_indir.py`.

Bilinen veri tuzakları (önce kontrol et, bulduğunu raporla):
1. **NG=F günlük kapanışının saati belirsiz** (14:30 ET uzlaşma mı, 17:00 ET son işlem mi) ve günlük seri ile saatlik seri farklı vadeyi gösterebiliyor (20.11.2026: günlük 3,411; saatlik 3,748). Bu yüzden gaz sinyali için birincil seri **UNG** (16:00 ET kapanış, işlem gören fiyat). NG=F yalnız çapraz kontrol ve 14:30 analizi (saatlik) için. Vade geçişi günlerindeki sahte sıçramaları ayıkla.
2. TTF=F günlük barının tarihi ve kapanış saati: t tarihli bar 16:00 ET'de biliniyor olmalı. Saatlik veriyle doğrula; emin değilsen sinyali 1 gün geciktirilmiş hâliyle de raporla.
3. BOIL/KOLD ters bölünmeleri: |günlük getiri| > %60 olan günleri ve BOIL ≈ 2×UNG, KOLD ≈ −2×UNG ilişkisinden sapan günleri listele; bozuk günleri at ve say.
4. Hayatta kalma yanlılığı: listeden çıkan gaz üreticileri (SWN, eski CHK, CTRA, COG, GPOR-eski) yok. Raporda belirt.
5. Tatil ve yarım günler, eksik barlar: hizalamayı işlem günü takvimiyle yap; ileri doldurma yapma.

## 2. Örneklem ve istatistik standardı
- **Keşif (IS):** serinin başı – 2021-12-31. **Örneklem dışı (OOS):** 2022-01-03 – son gün. Kısa serili testler (saatlik veri, 2023+ hisseler) yalnız "keşif amaçlı" sayılır, en çok İZLE alır.
- Her ızgara hücresi bir testtir. Toplam test sayısını raporla.
- Ölçüler: işlem sayısı, yılda işlem, işlem başına ortalama (bps), medyan, isabet oranı, t istatistiği (h>1 için Newey–West, gecikme h−1; ayrıca örtüşmeyen işlemlerle), IS / OOS / 2024–2026 ayrı ayrı, maliyet sonrası ortalama.
- Sinyal ölçeklemesi: z = getiri / σ60 (σ, t−1'e kadar 60 günlük std; ileri bakış yok). Beta: 250 günlük, 1 gün gecikmeli.
- **Maliyet (gidiş-dönüş):** UNG 10 bps; BOIL, KOLD 15 bps; EQT, EXE, LNG, KMI, WMB, XOP 6 bps; diğer hisseler 12 bps; FCG 15 bps. Duyarlılık: 2 katı.
- **Seçim kuralı:**
  1. IS'de |t| ≥ 2,0 ve bütün IS testleri üzerinde Benjamini–Hochberg q ≤ 0,10.
  2. OOS'de aynı işaret, t ≥ 1,65 (tek yön) ve maliyet sonrası ortalama > 0.
  3. Sağlamlık: en az 10 işlemli yılların ≥ %60'ında pozitif; en iyi %5 işlem çıkarılınca net ortalama hâlâ > 0; komşu ızgara hücreleri aynı işaretli; t+1 açılış girişinde etkinin ≥ %50'si kalıyor (kalmıyorsa "gap etkisi" diye işaretle: kapanışta alan için yine geçerli ama kırılgan); 2024–2026 negatif değil; kış (Kas–Mar) ve yaz ayrı raporlanır.
- **Etiket:** KULLANILABİLİR (1+2+3), İZLE (1+2 var, 3'te eksik; ya da yalnız OOS'de güçlü, ya da kısa örneklem), KULLANILAMAZ (diğerleri). Boş sonuçlar da tabloda yer alır.
- Kullanıcı gerçek ürünle işlem yapar: gaz yönü sinyallerinde sonucu hem UNG getirisiyle hem **gerçek BOIL (yukarı) / KOLD (aşağı) getirisiyle** ver.

## 3. Testler

### G — Gazın kendi dinamiği (işlem: UNG / BOIL / KOLD)
- **G1** 1 günlük momentum ya da dönüş: sinyal sign(r_UNG,t), eşik |z| > {0; 1; 2}; h ∈ {1,2,3}. (9 hücre × yön birleşik; ayrıca yukarı ve aşağı günler ayrı.)
- **G2** Çok günlük: 3 ve 5 günlük birikimli getiri z'si, eşik |z| > {1; 2}; h ∈ {1,2,3}.
- **G3** Gece / gün içi ayrımı: r_gece,t (kapanış t−1 → açılış t) ve r_güniçi,t (açılış → kapanış) ayrı öngörücü; eşik |z| > {0; 1}; h ∈ {1,2,3}. Ayrıca h=1 getirisini gece ve gün içi parçasına ayır (etki gap'te mi?).
- **G4** Uzlaşma sonrası hareket (keşif amaçlı, saatlik veri): UNG 14:30 ET → 16:00 ET getirisi (14:30 barının açılışı → 15:30 barının kapanışı); eşik |z| > {0; 1}; hedef: sonraki gece, sonraki gün, h=1.
- **G5** EIA depolama raporu günü (normalde Perşembe 10:30 ET): Perşembe UNG getirisi (Çar kapanış → Per kapanış), eşik |z| > {0; 1}; h ∈ {1,2,3}; Perşembe olmayan günlerle karşılaştır. Mümkünse EIA'nın gerçek yayın takvimini kullan (tatil kaymaları); değilse Perşembe varsayımını belirt.
- **G6** Haftanın günü: UNG kapanış→kapanış ortalama getirisi, bitiş gününe göre (Pzt…Cum); hafta sonu taşıma (Cum → Pzt); kış ve yaz ayrı. (5 + 2 test)
- **G7** Takvim: (a) öndeki vadenin son işlem gününden önceki 5 ve sonraki 5 işlem günü (NG vadelisi: teslim ayının ilk takvim gününden 3 iş günü önce biter); (b) UNG'nin vade geçiş penceresi (USCF takvimi; bulamazsan vade bitiminden önceki 10.–7. iş günleri yaklaşığı ve bunu belirt); (c) ay dönümü (son 1 + ilk 3 gün). Ay bazında mevsimsellik yalnız bilgi amaçlı tablo.
- **G8** Eğri/taşıma vekili: son 20 günde (r_UNG − r_UNL) birikimli farkın işareti ve z'si (negatif = contango baskısı) → sonraki h günde UNG; eşik {0; 1}; h ∈ {1,2,3}.
- **G9** (isteğe bağlı, ≤ 4 araç çağrısında veri alınabiliyorsa) NOAA CPC gaz ağırlıklı günlük HDD (`https://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_data/`): 7 günlük HDD anomalisi değişimi → ertesi gün UNG. Alınamazsa "yapılmadı" yaz, zorlama.

### E — Gaz → gaz hisseleri ve hisseler arası öncülük
Sepet = eşit ağırlıklı gaz üreticileri (EQT, AR, RRC, CNX, CRK; 2021'den sonra EXE ve GPOR eklenir). Ham ve korumalı (− β·XOP) getiri ayrı.
- **E1** z(r_UNG,t), eşik |z| > {0; 1; 2} → sepet t+1…t+h, h ∈ {1,2,3}. Tek tek hisseler yalnız betimleyici tablo (test sayılmaz).
- **E2** UNG 3 ve 5 günlük birikimli z, eşik |z| > 1 → sepet h ∈ {1,2,3}.
- **E3** Ters yön: sepetin XOP'a göre fazla getirisi z, eşik {0; 1} → UNG h ∈ {1,2,3}.
- **E4** Büyükten küçüğe: EQT'nin XOP'a göre fazla getirisi z, eşik {0; 1} → küçükler sepeti (CRK, AR, RRC, CNX) fazla getirisi h ∈ {1,2}.
- **E5** Sepet içi artık dönüşü: hisse getirisi − sepet getirisi, z < −1,5 olan hisseyi AL (yalnız uzun bacak; ham ve sepet korumalı), h ∈ {1,2,3}; havuzlanmış. Ayna test: z > +1,5 olan hisse sonraki günlerde geri veriyor mu (teşhis).
- **E6** Yetişme: 5 günlük UNG getirisi ile 5 günlük sepet fazla getirisi (XOP'a göre) farkı z > 1 (gaz çıktı, hisseler geride) → sepet h ∈ {1,2,3}; ayna (z < −1) ayrı.
- **E7** UNG → LNG sepeti (LNG, NEXT, 2025+ VG) ve boru hattı sepeti (KMI, WMB): eşik |z| > 1; h ∈ {1,2}. (Beklenti: boş.)

### X — Piyasalar arası
- **X1** TTF=F r_t z, eşik |z| > {0; 1; 2} → UNG h ∈ {1,2,3}; ayrıca 2022+ alt dönem.
- **X2** TTF=F r_t z, eşik |z| > 1 → LNG sepeti (LNG, NEXT, VG) ham ve SPY korumalı, h ∈ {1,2,3}.
- **X3** USO r_t z, eşik |z| > 1 → UNG h ∈ {1,2}; XOP r_t z → gaz sepeti (ham) h=1.
- **X4** (keşif amaçlı, 2023+) Elektrik/yapay zekâ sepeti (VST, CEG, NRG) fazla getirisi z > 1 → gaz sepeti h ∈ {1,2}.

### L — Kaldıraçlı ürün yapısı (sinyal değil, maliyet ölçümü)
- **L1** BOIL ve KOLD için 1, 2, 3, 5, 10, 21 günlük gerçek getiri ile aynı dönemin 2× ya da −2× UNG getirisi arasındaki ortalama fark (erime), oynaklık rejimine göre (σ60 üçte birlikleri). "İkisi birden kaybetti" sıklığı.
- **L2** Koşulsuz ortalama günlük getiri: UNG, BOIL, KOLD; kış ve yaz ayrı; 2012–2021 ve 2022–2026.
- **L3** Maruziyet tablosu: bütün araçlar için UNG'ye aynı gün betası ve R² (son 250 gün ve 2022+), yıllık oynaklık, ortalama |1 günlük| ve |3 günlük| getiri, son 60 gün ortalama dolar hacmi.

## 4. Çıktı
- Kod: `raporlar/2026-11-21_dogalgaz_1-3gun/kod/` (tek ana betik + gerekiyorsa yardımcı; veri klasörü argüman).
- `raporlar/2026-11-21_dogalgaz_1-3gun/ek/K1_tum_testler.csv`: her test bir satır (kimlik, hedef, eşik, h, n, IS ort/t, OOS ort/t, 2024–26 ort/t, net ort, isabet, q değeri, etiket).
- `raporlar/2026-11-21_dogalgaz_1-3gun/ek/K1_sonuc.md`: ≤ 120 satır: veri kontrolü bulguları, test sayısı, etiketli özet tablo (yalnız KULLANILABİLİR + İZLE satırları ve her gruptan en güçlü boş sonuç), L1–L3 tabloları, ön kayıtsız keşifler, yapılamayanlar.
