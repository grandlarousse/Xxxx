# Yöntem şartnamesi (hesaptan önce yazıldı, 10.11.2026)

Amaç: Kullanıcının paneli (GLD, TVC:GOLD, VİOP ons altın, GDX, PHYS, GDXJ, COMEX GC, TRMET vadelisi; izleme listesinde USDTRY) ve bu panelle yürüttüğü strateji, şu profil için para kazandırır mı?

- İşlem yapılan iki araç: **F_TRALT** (pay vadelisi, 100 pay) ve **F_XAUUSD** (VİOP dolar/ons altın vadelisi, 1 ons).
- Karar 17:55 TSİ (14:55 UTC), giriş aynı günün VİOP uzlaşmasında, çıkış 1–3 VİOP günü sonraki uzlaşmada. Gün içi işlem yok.
- Pozisyon büyüklüğü 10–30 bin USD.

Önceki çalışmalar (aynı depoda): `raporlar/2026-11-04_kapanis_1-3gun/rehber/altin/REHBER_altin.md` (altın z>1 → TRALT − β·XU030, 2 gün; net +35,5 bps, t 2,2, güven DÜŞÜK; hedge'siz +25 bps, t 1,3) ve `rehber/koza/REHBER_koza.md` (TRMET göreli momentumu; 2024–26 net ≈ 0). Bu çalışma onları tekrar etmez; **paneldeki diğer araçların ek bilgi taşıyıp taşımadığını** ve **kullanıcının gerçek kullanım biçiminin beklenen kazancını** ölçer.

## Veri (indirildi, `<S>/veri/`)

- `viop_filtre.csv`: Borsa İstanbul VİOP günlük bültenleri 2018-11 → 2026-11-10; F_XAUUSD, F_XAUTRY, F_TRALT/F_KOZAL, F_TRMET/F_KOZAA, F_XU030, F_USDTRY satırları. Sütunlar: uzlaşma, önceki uzlaşma, kapanış, AOF, hacim, miktar, açık pozisyon, vade.
- `yahoo_daily/*.csv` (2005+; o,h,l,c,adj; `ldate` = borsa yerel tarihi), `yahoo_h1/*.csv` (son 730 gün, UTC damgalı), `yahoo_m5/*.csv` (son 60 gün).
- İzin verilen kaynak yalnız bunlar. TradingView iç uç noktalarından veri çekilmez.

## Zaman kuralları (Türkiye yıl boyu UTC+3)

- BIST günü t için karar anı T_t = t 14:55 UTC.
- ABD seansı: yaz saatinde 13:30–20:00 UTC, kış saatinde 14:30–21:00 UTC. "Son tamamlanmış ABD seansı" = kapanış anı T_t'den önce olan en son ABD işlem günü (tatiller iki tarafta ayrı ele alınır).
- Getiri zinciri: aynı kontratta r = ln(uzlaşma_t / önceki uzlaşma_t). Ön vade = girişte vadesine ≥ 3 VİOP günü kalan en yakın kontrat; pozisyon aynı kontratta taşınır.
- Yarım gün (arife) ve tavan/taban kilidi (|r| ≥ %9,5 vekili) günlerinde giriş yok sayılır; ayrı raporlanır.

## Hedefler (girişten k = 1, 2, 3 gün sonrası)

- A1: F_TRALT (hedge'siz).
- A2: F_TRALT − β·F_XU030 (β: spot TRALT'ın XU030'a 250 günlük betası, 1 gün gecikmeli).
- A3: F_TRALT − b·F_XAUUSD (b: 250 günlük beta, gecikmeli). Yalnız kullanıcının iki aracını kullanan çift.
- B1: F_XAUUSD (USD getirisi).

## Öngörücüler (hepsi T_t'de biliniyor olmalı)

1. g: F_XAUUSD'nin o günkü uzlaşma değişimi (17:55 anlık altının vekili; önceki çalışmada korelasyon 0,98–0,99). z = g/σ250 (gecikmeli).
2. g'nin ayrışımı (saatlik GC=F, 2024-06+): gece kısmı (15:00 UTC t−1 → 06:30 UTC t) ve BIST saatleri kısmı (06:30 → 15:00 UTC t).
3. Son tamamlanmış ABD seansı (kapanıştan kapanışa): r_GLD, r_GDX, r_GDXJ, r_PHYS; artıklar e_GDX = r_GDX − β·r_GLD, e_GDXJ = r_GDXJ − β·r_GDX, e_PHYS = r_PHYS − r_GLD.
4. ABD seansının T_t'ye kadarki kısmı (saatlik, 2023-12+): GDX'in önceki kapanıştan T_t'ye kadarki getirisinin aynı penceredeki GLD'ye göre artığı.
5. TRALT'ın kendi hareketi: o günkü r, 3 günlük toplam; altına göre o günkü artık u = r_TRALT − b·g ("eksik tepki" hipotezi).
6. TRMET göreli hareketi: r_F_TRMET − β·r_F_TRALT (o gün ve 3 günlük).
7. F_USDTRY'nin o günkü değişimi.
8. Teknik (kullanıcının grafiğinde bant + ortalama var): uzlaşma zincirinden kurulan sürekli seride sign(P − MA20), Bollinger %b(20,2) uçları, 20 günlük Donchian kırılımı. F_TRALT ve F_XAUUSD için.
9. Yalnız B1 için ek: g'nin 1, 3, 5 günlük toplamı (momentum/dönüş); son tamamlanmış ABD seansında SLV'nin GLD'ye göre artığı, dolar endeksi (DX-Y.NYB), ^TNX, TIP, ^VIX, SPY değişimleri.

## Test

1. Öngörü regresyonu: y(t→t+k) = a + b·x_t. x gecikmeli 250 günlük σ ile ölçeklenir; b "1σ başına bps". Newey–West t (gecikme k+1). Dönemler: tam (17.12.2018 → 09.11.2026), IS (< 2022), OOS (≥ 2022), yakın (≥ 2024). Saatlik veriye dayananlar yalnız kısa örneklemde; iki yarıya bölünür ve "kısa örneklem" etiketi alır.
2. Çoklu test: TRALT ailesi (A1–A3) ve altın ailesi (B1) için ayrı ayrı bütün (öngörücü × hedef × k) testleri sayılır; BH-FDR q ve Bonferroni raporlanır.
3. Geçme ölçütü (önceden sabit): tam dönem |t| ≥ 3,0 ya da (|t| ≥ 2,0 ve q ≤ 0,10); IS ve OOS aynı işaret ve OOS |t| ≥ 1,5; 2024–26 aynı işaret.
4. Geçenler için işlem kuralı: |z| > 1 (sabit; 0,75 ve 1,25 yalnız duyarlılık), örtüşmesiz, giriş/çıkış uzlaşmada, k = 2 ana (1 ve 3 raporlanır). Maliyet (gidiş-dönüş): TRALT 8 bps (düşük) / 23 bps (bireysel tarife); XU030 bacağı β×3 / β×8; XAUUSD 3 / 10 bps. Ölçüler: n, yılda işlem, brüt/net ortalama, t, isabet, IS/OOS/2024–26, en iyi 10 işlem hariç, en kötü işlem, maksimum düşüş, yıl tablosu, long/short ayrı. Plasebo: sinyalin dairesel kaydırılması (≥ 500 kaydırma) ile ampirik p.
5. Sağlama: önceki araştırma kuralı (z_g > 1, hedef A2, k = 2) yeniden üretilir. Beklenen: n ≈ 405–423, net ≈ +36…+43 bps (8+3 maliyet). Fark > 10 bps ise dur ve bildir.
6. Koşulsuz taban: F_XAUUSD ve F_TRALT'ta "her zaman long" k günlük ortalama getiri. Altın 2024–26'da güçlü yükseldi; her kural long/short ayrı ve bu tabana göre raporlanır.
7. Beklenen kazanç (mevcut strateji): yeniden üretilen işlem listeleri (A2, A1, A3) üzerinde blok bootstrap (yıl başına gerçek işlem sayısıyla, 5.000 tekrar). 10/20/30 bin USD TRALT nominali için yıllık kâr/zarar dağılımı: ortalama, %5–%95, zararlı yıl olasılığı, en kötü düşüş. Senaryolar: tam dönem; yalnız 2024–26; en iyi 10 işlem hariç; düşük ve bireysel maliyet.
8. F_XAUUSD taşıma maliyeti: bültendeki ardışık iki vadenin uzlaşma farkından yıllıklandırılmış taşıma (carry). Long pozisyonun 2 günlük maliyeti bps olarak.
9. Likidite: son 12 ayda F_XAUUSD ve F_TRALT ön vadede medyan günlük işlem hacmi, miktar, açık pozisyon; 10–30 bin USD'nin günlük hacme oranı.

## Bilinen tuzaklar (denetçiden özellikle bakması istenir)

- Sinyal uzlaşmada oluşuyorsa girişte bilinmez (g vekili). ABD seansı eşlemesinde ileriye bakma.
- KOZAL vadelisi 2018–20'de çok illikit (günlük 0,2–16 mn TL).
- Altın 2024–26 rallisi: long yanlısı her kural iyi görünür.
- Örtüşen getiriler, vade geçişi, limit kilidi, arife günleri.
- Onlarca test: çoklu test düzeltmesi olmadan bulgu yok.
