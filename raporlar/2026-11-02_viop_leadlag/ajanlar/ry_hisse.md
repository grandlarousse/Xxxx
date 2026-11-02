# ry_hisse — Yurt içi hisse→hisse günlük lead-lag (47 VİOP hedefi × 177 BIST hissesi)
Ajan: hisse · Veri: data/daily (Yahoo, ll.decomp: cc = gap + gün-içi; ±%10,5 temizliği; sıfır hacimli günler düşürüldü) · Dönem 02.01.2014–30.10.2026 (cc için ayrıca PRE 2005–2013) · IS 2014–2020 / OOS 2021–2026 · Saatlik 2023-12..2026-10 · Kod: `out/code_y_hisse/` (`run_all.sh`)

## 1. Net bulgular

| # | Bulgu | Rakam | Güven |
|---|---|---|---|
| 1 | **Hisseye özgü günlük öncülük tespit edilemiyor.** lider_{t-k} → hedef_t (cc/gap/gün-içi; k=1..5 ve Σ5g), kendi lag + XU100 + sektör kontrollü, NW | 157.149 testte BH q<0,05 **0** (dep ailesi). (dep,lag) bazında yalnız 4 (hepsi gap, illikit lider). \|t\|>3: cc-lag1 45 / null 22, gap 59 / 20, gün-içi 36 / 21 | (olumsuz) YÜKSEK |
| 2 | IS→OOS replikasyon null düzeyinde | IS top-200 → OOS aynı işaret & p<0,05: cc %3,0, gap %6,5, gün-içi %3,0; 20 kaydırma null'u ort %2,1–2,2 (maks %5–8,5). IS'de BH'den geçen 9 çiftin OOS'ta replike olanı **0** | (olumsuz) YÜKSEK |
| 3 | Piyasa-göreli (hedef − β·XU100, EW177 kontrollü) taramada da sonuç aynı | 74.439 testte BH 0; IS&OOS'ta ayrı ayrı \|t\|>2 aynı işaretli çift 23 (bağımsızlık altında beklenen ≈26) | (olumsuz) YÜKSEK |
| 4 | **"Sistematik lider" yok; lider/takipçi rolleri yıldan yıla değişiyor** | Liderin 47 hedef üzerindeki ort. t sıralaması: ardışık yıllar Spearman −0,12…+0,15; IS vs OOS −0,11. Takipçi IS vs OOS 0,01. 47×47 yön asimetrisi: corr(t_ab, t_ba) = −0,05 | (olumsuz) YÜKSEK |
| 5 | "Çok hedefli lider" görünen THYAO/PGSUS aslında **tek bir piyasa zamanlaması** | THYAO_{t-1} → 47 hedefin 20'sinde gün-içi t>2; ama THYAO idio_{t-1} → XU030 gün-içi_t t=3,32 (IS 1,35 / OOS 3,08); 177 liderli ailede BH geçmiyor (null'da bu \|t\|'ye ulaşma olasılığı 0,12); XU030 vadelisi BT 3 bps OOS SR 0,09 | DÜŞÜK |
| 6 | Senkron yapı güçlü ve istikrarlı (öncülük değil, **eşzamanlılık**) | XU100 artıklarında 12 çok üyeli küme (14 hisse tekil). Banka 7'lisi ort. artık ρ 0,42 (AKBNK–GARAN 0,69), TRALT–TRMET 0,66 (TRENJ ile 0,78), THYAO–PGSUS 0,52, EREGL–KRDMD 0,39 (ISDMR 0,45), CIMSA–OYAKC 0,34, FROTO–TOASO 0,33, MGROS–SOKM 0,31, TCELL–TTKOM 0,31, HEKTS–SASA 0,30, KCHOL–SAHOL 0,29, ASTOR–EUPWR 0,37, EUPWR–GESAN 0,66. 95 senkron satır YÜKSEK | YÜKSEK |
| 7 | Kümeler zamanla **sıkılaştı**; yapı orta-yüksek istikrarlı | Pencere ARI 0,46–0,72, korelasyon matrisi benzerliği 0,56–0,72; çoğu çiftte OOS artık ρ > IS (AKBNK–YKBNK 0,37→0,74; EREGL–ISDMR 0,28→0,59; HEKTS–SASA 0,11→0,45). 2021+ bankalara KCHOL/SAHOL katılıyor | YÜKSEK |
| 8 | Ekonomik çiftlerde öncülük zayıf; en iyileri DÜŞÜK-ORTA | 214 yönlü çiftte BH(cc/gap/intra) 0. En iyi: AGHOL→AEFES gün-içi t 3,32 (IS 2,54/OOS 2,16), CCOLA→AEFES 2,64 (cc-rel IS 2,54/OOS 2,22), KCHOL→AYGAZ 2,82. THYAO→PGSUS/TAVHL/CLEBI, TUPRS→PETKM/AYGAZ, EREGL→KRDMD/ISDMR, bankalar arası: **senkron, öncülük yok** | DÜŞÜK-ORTA / DÜŞÜK |
| 9 | Küme içi gap sapmasının gün-içi dönüşü güçlü — **ama ilk 30 dakikada bitiyor** | Açılıştan (iyimser dolum) 16 bps/gün, OOS SR 3,8; 8 bps sonrası 8,4 bps, SR 2,0. Saatlik veriyle ~10:30 girişte brüt 5,0 bps, 8 bps sonrası **−3,0 bps** (SR −1,0). Eşlerin gap'inin hedefi "çekmesi" IS'de var (t 6,7), OOS'ta yok (t 0,8) | Etki YÜKSEK; işlenebilirlik (olumsuz) YÜKSEK |
| 10 | Banka çiftleri spread ortalamaya dönüşü: zayıf ama IS/OOS tutarlı | 8 banka çifti portföyü, 8 bps: IS SR 0,44 / OOS 0,62 (t 1,5). AKBNK–GARAN / AKBNK–YKBNK / GARAN–YKBNK OOS işlem başına +155/+175/+221 bps (≈30 işlem). Engle-Granger: 27 çiftin hiçbiri IS ve OOS'ta birlikte eşbütünleşik değil | DÜŞÜK |
| 11 | Diğer backtestler maliyet sonrası negatif | IS seçimli lider sepeti → gün-içi: IS SR 3,0 (brüt) → OOS −0,16; 8 bps OOS −1,8. Küme-eşi yakınsama, küme içi cc dönüşü, 5g küme momentum/dönüş: 8 bps OOS SR −0,1…−3,2 | (olumsuz) YÜKSEK |
| 12 | Piyasa düzeyi yan bulgu: küçük/bireysel faktör (EW177 − XU100)_{t-2} → XU030 gap_t | t=3,71 (IS 2,28 / OOS 3,10); hisse taramasındaki gap lag-2 fazlalığının ortak kaynağı (EW kontrolüyle p<0,05 sayısı 908→432). Koşulsuz gece-long'a ek değer katmıyor | DÜŞÜK |
| 13 | Saatlik (gün içi) hisse→hisse öncülük yok | 4.512 testte BH 0; p<0,05 353 (beklenen 226); ilk yarı top-200 → ikinci yarı %2,0 (null ≈%2,5) | (olumsuz) YÜKSEK |
| 14 | VİOP pay vadelileri brifingde varsayılandan likit | Son 12 ay medyan günlük işlem hacmi: AKBNK 4,0 mlr TL, THYAO 3,7, ASELS 3,4 … DOAS 70 mn TL; spot hacmin %27–84'ü | YÜKSEK (bülten verisi) |

**Özet yorum:** Yurt içi hisseler arasında **günlük, hisseye özgü, istatistiksel olarak ayırt edilebilir bir öncülük ilişkisi yok.** Bilgi aynı gün içinde (senkron) fiyatlanıyor. Bu, uluslararası turdaki "gün-içinde kalıntı yok" bulgusuyla tutarlı. Bulunabilen tek güçlü gecikmeli etki hissenin **kendi** açılış gap'inin gün-içi kısmi dönüşü; o da ilk 30 dakikada tükeniyor.

## 2. Yöntem
- **Evren:** hedef 47 VİOP dayanağı; aday lider panelde verisi olan 177 BIST hissesi (catalog VIOP + BIST_other, X* endeksleri hariç). Günlük sektör endekslerinden yalnız XU030/XU100/XBANK/XUSIN Yahoo'da var (diğer ≈40 endeks dosyası tek satır) → sektör kontrolü bankalar için XBANK, XUSIN üyeleri için XUSIN, diğerleri için yok. Bunu telafi etmek için piyasa-göreli tarama ve EW177 kontrolü eklendi.
- **Model (ana tarama):** y_{j,t} = a + b·r_{i,t-k} + c₁ r_{j,t-1} + c₂ XU100_{t-1} + c₃ Sektör_{t-1} [+ k>1: aynı üçlünün _{t-k} değerleri; Σ5g: Σ_{t-5..t-1}] + e. y ∈ {cc, gap, gün-içi, gün-içi|gap_t (hedef ve XU100 gap_t kontrollü)}. Lider her zaman cc. Bartlett NW (5 lag). Her çiftin kendi tam-örneklem maskesi var; matris çarpımlarıyla vektörize edildi (`hreg.nw_batch`, statsmodels ile b aynı, t ±%1).
- **Dönemler:** FULL / IS / OOS / PRE (2005–13, cc) / her yıl ayrı (lag1 cc ve gün-içi).
- **Çoklu test:** BH q=0,05; (i) dep ailesi (6 lag birlikte, 49.626 test), (ii) (dep,lag) ailesi (8.271), (iii) tümü (157.149). Piyasa-göreli tarama 74.439, saatlik 4.512, piyasa düzeyi 1.062, ekonomik çiftler 214×3 test daha → toplam ≈240 bin tam dönem testi (dönem ve yıllık kırılımlar hariç).
- **Null:** lider paneli 20 rastgele ofsetle (≥250 gün) **dairesel kaydırıldı**; tüm liderler aynı ofsetle kaydırıldığından liderler arası korelasyon ve oynaklık kümelenmesi korunuyor, yalnız lider–hedef hizası bozuluyor. Hedef ve kontroller yerinde kalıyor. Lag1 cc/gap/gün-içi × FULL/IS/OOS (piyasa-göreli taramada 10 ofset).
- **Bayat fiyat:** (a) lider/hedef OOS medyan TL hacmi oranı (>3 → `stale_flag`), (b) hacim filtresi: TL hacmi geçmiş 60g medyanının %30'unun altındaki günler hedefte t ve t-1, liderde t-1 için maskelendi (hedef günlerinin medyan %1,6'sı), (c) gap/gün-içi ayrıştırması (bayat kapanış gap'te düzelir).
- **Senkron:** XU100 artıkları (β tam dönem), ortalama bağlantılı hiyerarşik kümeleme (1−ρ eşik 0,86; 0,80 ve 0,90 da raporlandı), PCA (tüm 47 için ortak örneklem 2023-02+; 46 hisse ile 2018-06+), 4 pencere (2014–17, 2018–20, 2021–23, 2024–26) arası ARI ve matris benzerliği. Mekanik içerme sağlamlığı: piyasa = EW177 ile ARI 0,70.

## 3. Senkron yapı
**Kümeler (tam dönem, eşik 0,86; ort. küme-içi artık ρ):** Bankalar AKBNK-GARAN-HALKB-ISCTR-TSKB-VAKBN-YKBNK (0,42) · Perakende/gıda BIMAS-MGROS-SOKM-ULKER (0,20) · Havacılık PGSUS-TAVHL-THYAO (0,36) · Koç-dayanıklı/oto ARCLK-FROTO-TOASO (0,21) · TCELL-TTKOM (0,31) · KCHOL-SAHOL (0,29) · HEKTS-SASA (0,30) · TRALT-TRMET (0,66) · AKSEN-ODAS (0,19) · CIMSA-OYAKC (0,34) · PETKM-TUPRS (0,17) · EREGL-KRDMD (0,39). Tekil kalanlar: AEFES, ALARK, ASELS, ASTOR, BRSAN, DOAS, DOHOL, EKGYO, ENJSA, ENKAI, GUBRF, SISE, TKFEN, VESTL (bunların eşleri VİOP dışında: ASTOR–EUPWR/ALFAS/GESAN/CWENE 0,29–0,37; BRSAN–BRYAT 0,57; VESTL–VESBE 0,47; ASELS–ALTNY/SDTTR 0,21–0,26; AEFES–AGHOL/CCOLA 0,23–0,24; GUBRF–BAGFS 0,21; ODAS–CANTE 0,31).
Gevşek eşikte (0,90) bankalar + KCHOL/SAHOL birleşiyor; enerji (AKSEN-ALARK-ODAS-VESTL), emtia (GUBRF-TRALT-TRMET), çelik + SISE, ASTOR-BRSAN kümeleri oluşuyor.

**PCA (XU100 artıkları, 2023-02..2026-10, 47 hisse):** PC1 %10,9 = banka(+)/holding karşısında sanayi-emtia(−) (TRALT, TRMET, CIMSA, ASTOR, OYAKC, KRDMD) — **banka↔sanayi rotasyonu**. PC2 %5,7 = kamu bankaları + "bireysel/tema" hisseleri (VAKBN, HALKB, OYAKC, EREGL, KRDMD, EKGYO, HEKTS, TRALT) karşısında yabancı-ağırlıklı defansif/büyükler (BIMAS, MGROS, THYAO, PGSUS, FROTO, KCHOL). PC3 %4,8 = perakende/gıda (SOKM, MGROS, ULKER, AEFES) karşısında TUPRS/SASA/HEKTS/ASELS. PC4 = Koç/Sabancı holding (SISE, ARCLK, KCHOL, FROTO, SAHOL, DOHOL). PC5/6 = havacılık ve Koza grubu. İlk 8 özdeğerin hepsi Marchenko-Pastur üst sınırının (1,56) üstünde. Ham getiride PC1 (piyasa) %42,6.
**İstikrar:** ARI 2014↔2018 0,62; 2018↔2021 0,61; 2021↔2024 0,72; 2014↔2024 0,50. Küme-içi artık ρ yıllara göre: TRALT–TRMET 13/13 yıl ≥0,50; bankalar 0,16 (2014) → 0,55 (2021) → 0,46 (2026); havacılık 0,14 → 0,64 (2021) → 0,50; HEKTS–SASA 2021 öncesi ≈0 → 2022–25'te 0,45–0,66; PETKM–TUPRS istikrarsız (−0,14…0,49).

## 4. Günlük lead-lag taraması (ayrıntı)

| dep | lag | test | p<0,05 | \|t\|>3 | BH (dep,lag) | null p<0,05 / \|t\|>3 / BH | IS-BH → OOS rep |
|---|---|---|---|---|---|---|---|
| cc | 1 | 8.271 | 506 | 45 | 0 | 395 / 22,2 / 0,0 | 1 → 0 |
| cc | 2–5 | 4×8.271 | 407–509 | 15–33 | 0 | – | 0 |
| cc | Σ5 | 8.271 | 474 | 27 | 0 | – | 0 |
| gap | 1 | 8.271 | 608 | 59 | 1 | 393 / 20,4 / 0,1 | 0 |
| gap | 2 | 8.271 | **908** | **91** | 3 | – | 0 |
| gap | 3–5, Σ5 | | 418–627 | 12–49 | 0 | – | 1 → 0 |
| gün-içi | 1 | 8.271 | 474 | 36 | 0 | 401 / 21,0 / 0,0 | 4 → 0 |
| gün-içi | 2–5, Σ5 | | 394–509 | 15–32 | 0 | – | 0 |
| gün-içi\|gap | 1 | 8.271 | 481 | 36 | 0 | – | 3 → 0 |

- p<0,05 sayısında null'a göre ~%20–50'lik, \|t\|>3'te ~2 katlık bir **dağınık fazlalık** var: çok sayıda çok küçük etki (\|pc\|≈0,03–0,07) olabilir, tek tek ayırt edilemiyor ve maliyeti karşılamıyor.
- **gap lag-2 fazlalığı (ort. t +0,56) ortak bir faktör:** (EW177 − XU100)_{t-2} → hedef gap_t, 47 hedefin 40'ında t>2. EW kontrollü piyasa-göreli taramada p<0,05 sayısı 432'ye iniyor.
- **Ortalama çapraz dönüş:** cc lag-1 ortalama t −0,19, EW_{t-1} → hedef gap_t ort t −1,57. "Bireysel/küçük hisse günü"nden sonraki açılış büyükler için hafif negatif. Bu çifte özgü değil, piyasa faktörü.
- (dep,lag) ailesinde BH'den geçen 4 çift: EGEEN→HALKB gap (t −4,5), AFYON→ENKAI, ASUZU→TTKOM, TURSG→ULKER gap lag-2 (t 4,3–4,5; IS ve OOS t 2,4–3,8). Hepsinde lider hedeften 3–15 kat **daha illikit**; mekanizma şüpheli, büyük olasılıkla küçük-hisse faktörü. Gap işlenemez. DÜŞÜK.
- **Bayat fiyat:** likidite oranı kovalarına göre lag1 cc ort. t: lider ≥10× daha likit +0,25 (83 çift), 3–10× −0,01, 1–3× +0,01, <0,1× −0,33. Lo–MacKinlay yönünde ama zayıf bir eğim var; 47 hedefin hepsi likit olduğundan bu etki küçük. Hacim filtresi (lag1) en güçlü adayların t'sini değiştirmiyor (ör. THYAO→KCHOL gün-içi 3,80 → 3,75).
- **PRE (2005–2013):** ekonomik çiftlerin bir kısmında lag1 işareti ters ve anlamlı (AKBNK→SAHOL PRE t −3,57; YKBNK→KCHOL −3,62). İlişkiler rejime bağlı.

## 5. Asimetri: lider / takipçi
- Ortalama t'ye göre en "lider" hisseler THYAO (+2,00; gün-içi +1,91), BERA, PGSUS (+1,16), DOCO, TATEN, TCELL; en "ters lider" (sonraki gün diğerlerini aşağı iten) IZENR (−1,94), KRDMB, KRDMA, ASELS, DOHOL, EREGL, ASTOR, KRDMD. Bu sıralamanın yıllar arası Spearman'ı ≈0, IS↔OOS −0,11. Rol **kalıcı değil**. THYAO'nun skoru neredeyse tamamen OOS'tan geliyor (IS ort t 0,58 → OOS 2,17) ve piyasa zamanlaması (Bulgu 5).
- Liderlik skoru ile likidite arasında Spearman 0,18: büyükten küçüğe çok zayıf bir eğilim.
- Takipçi tarafında da istikrar yok (IS↔OOS 0,01). 47×47 yönlü çiftlerde t_ab ile t_ba ilişkisiz (−0,05). \|t_ab − t_ba\|>3 olan 63/1.081 çift, rastgele beklentiyle uyumlu.

## 6. Ekonomik bağlantılı çiftler (senkron vs öncülük)
Kontroller tarama ile aynı. "öncülük t" = lider_{t-1} → hedef gün-içi_t (cc t parantez içinde). Tüm 214 yön `f_y_hisse.csv`'de.

| Grup | Senkron (XU100 kısmi ρ, IS→OOS) | En iyi öncülük yönü (gün-içi t; cc t) | Sonuç |
|---|---|---|---|
| THYAO–PGSUS–TAVHL–CLEBI | THYAO–PGSUS 0,52 (0,48→0,58, 13/13 yıl +); PGSUS–TAVHL 0,29; THYAO–TAVHL 0,27; THYAO–CLEBI 0,20 | THYAO→TAVHL 2,28 (3,02; PRE −1,96); CLEBI→THYAO 2,60; THYAO→PGSUS 0,29 (1,04); PGSUS→THYAO 1,00 (0,43) | Senkron YÜKSEK; öncülük DÜŞÜK |
| TUPRS→AYGAZ/PETKM | TUPRS–AYGAZ 0,32; TUPRS–PETKM 0,17 (istikrarsız) | TUPRS→AYGAZ 1,83 (2,26); TUPRS→PETKM <1 | Senkron YÜKSEK/ORTA; öncülük ÇOK DÜŞÜK |
| EREGL→KRDMD/ISDMR/BRSAN | EREGL–ISDMR 0,45; EREGL–KRDMD 0,39; KRDMD–ISDMR 0,33; BRSAN ile ≈0 | EREGL lider olarak sıfır/negatif: EREGL→ISDMR cc −2,08, EREGL→BRSAN −1,72, EREGL→KRDMD +0,67; KRDMD→BRSAN gap −3,02; gün-içi \|t\|≤1,3 | Senkron YÜKSEK; öncülük yok |
| Bankalar (7) | 0,23–0,69 (TSKB dışındaki çiftler 13/13 yıl +, TSKB çiftleri %77–92; özel bankalar OOS'ta 0,6–0,74) | Bankalar arası lag1 çoğunlukla **negatif** (42 yönün cc'de 27'si, gap'te 35'i; GARAN→YKBNK cc −2,10, GARAN→ISCTR gap −3,09): öne geçen banka ertesi açılışta diğerine göre geri veriyor (XBANK kontrolüyle). AKBNK/ISCTR lider olduğunda hafif pozitif (gün-içi t ≤1,9). Kamu↔özel yönünde de öncülük yok | Senkron YÜKSEK; öncülük yok; spread dönüşü DÜŞÜK (Bulgu 10) |
| FROTO–TOASO–DOAS–OTKAR–TTRAK | FROTO–TOASO 0,33; diğerleri 0,07–0,19 | FROTO→TTRAK 2,14 (2,61); DOAS←OTKAR 2,10 | Senkron YÜKSEK/ORTA; öncülük DÜŞÜK |
| ASTOR–EUPWR–GESAN–CWENE (2023+) | EUPWR–GESAN 0,66; ASTOR–EUPWR 0,37; GESAN–CWENE 0,39 | Gün-içi \|t\|≤1,4 (gap'te EUPWR→GESAN 1,97) | Senkron ORTA (kısa örneklem); öncülük yok |
| BIMAS–MGROS–SOKM | MGROS–SOKM 0,31; BIMAS–SOKM 0,25; BIMAS–MGROS 0,22 (0,06→0,36) | Gün-içi \|t\|≤1,1; gap'te MGROS→BIMAS 2,62, BIMAS→MGROS 1,98 (işlenemez) | Senkron YÜKSEK; öncülük yok |
| GUBRF–BAGFS–HEKTS | GUBRF–BAGFS 0,21; BAGFS–HEKTS 0,16; GUBRF–HEKTS 0,13 | GUBRF→HEKTS 2,88 (IS 0,65 / OOS 2,90; PRE −2,37); GUBRF→BAGFS 1,82 | Senkron ORTA; öncülük DÜŞÜK (yalnız OOS) |
| CIMSA–OYAKC–AKCNS–NUHCM–BUCIM | 0,26–0,44 (CIMSA–AKCNS 0,42) | AKCNS→NUHCM 1,0 (cc 1,95); OYAKC→EKGYO 2,37 | Senkron YÜKSEK; öncülük ÇOK DÜŞÜK |
| ASELS↔OTKAR | 0,09 | OTKAR→ASELS 1,91; ASELS→OTKAR −1,43 | Zayıf; DÜŞÜK |
| TCELL↔TTKOM | 0,31 (0,20→0,40) | TCELL→TTKOM 1,78 (cc 2,19; PRE −1,90) | Senkron YÜKSEK; öncülük DÜŞÜK |
| AEFES–CCOLA–AGHOL | 0,13–0,24 | **AGHOL→AEFES 3,32** (IS 2,54/OOS 2,16; PRE +0,98); **CCOLA→AEFES 2,64** (cc 3,34; IS 2,15/OOS 1,58) | Bu turdaki en iyi ekonomik öncülük: **DÜŞÜK-ORTA** (BH yok; BT 8 bps OOS SR 0,36 / −0,24) |
| KCHOL/SAHOL grupları | SAHOL–AKBNK 0,30; KCHOL–SAHOL 0,29; KCHOL–FROTO/ARCLK 0,17 | AKBNK→SAHOL 3,44 (PRE −3,57!); KCHOL→AYGAZ 2,82 (likidite oranı 36, bayat fiyat riski) | DÜŞÜK |

## 7. Backtestler (yalnız VİOP'taki 47 hedef işlem görür; maliyet birim brüt pozisyon başına gidiş-dönüş)

| Strateji | IS (bps/gün, SR) | OOS 8 bps | OOS 15 bps | Not |
|---|---|---|---|---|
| BT1 IS seçimli lider sepeti (\|t_IS\|≥3, ≤5 lider) → hedef gün-içi | brüt 11,0 / SR 3,0 | −8,7 / SR −1,78 | −15,6 / −3,2 | Klasik aşırı uyum: 21 hedefin 4'ünde OOS SR>0 |
| BT1r 3 en yakın eşin (177'den) rölatif getirisi_{t-1} → gün-içi (yakınsama) | brüt 1,5 / 0,83 | −9,0 / −3,2 | −16 | Havuz ρ IS 0,011 → OOS 0,001 |
| BT2 çift spread z60 (giriş \|z\|>2, çıkış \|z\|<0,5/20g), 27 çift | ≈0 | ≈0 (SR −0,02) | | Engle-Granger hiçbirinde IS+OOS birlikte değil |
| BT2 yalnız 8 banka çifti | SR 0,44 | 2,3 bps/gün, **SR 0,62** (t 1,5) | | DÜŞÜK güven; AKBNK–GARAN, AKBNK–YKBNK, GARAN–YKBNK işlem başına +155…+221 bps |
| BT2 IS SR>0,3 seçimli 9 çift | SR 1,50 | SR 0,34 (t 0,8) | | Zayıflıyor |
| BT3 küme içi dönüş (cc_{t-1} sapması) → gün-içi | brüt 1,7 / 0,64 | −9,1 / −2,6 | −16,1 | Brüt OOS −1,1: dönüş artık yok |
| **BT3g küme-göreli gap_t sapması → gün-içi (açılış dolumu)** | brüt 15,6 / **5,1** | **8,4 / SR 1,97** | 1,4 / 0,34 | 2014–15 hariç her yıl +. Kaynağı **kendi gap'in dönüşü** (b_own −0,15, t −10) |
| BT3g gerçekçi giriş (~10:30, saatlik, 2023-12+) | – | brüt 5,0; **8 bps −3,0 / SR −1,04** | | Dönüşün çoğu ilk 30 dk'da: işlenemez |
| BT4a 5g küme momentum → gün-içi (günlük) | −1,1 | −6,1 / −0,97 | −13,1 | Dönüş yönü de negatif |
| BT4b 5g küme momentum, 5 gün tut | 14 bps/işlem / 0,56 | −4,8 / −0,15 | −11,8 | t<1,4 |
| Ekonomik çift lag-1 (214 yön) sign(lider_{t-1}) → gün-içi | | OOS SR medyan <0; en iyi 0,64 (OYAKC→EKGYO, GUBRF→HEKTS) | | Hiçbiri t>2 değil |
| THYAO idio_{t-1} → XU030 gün-içi (endeks vadelisi, 3 bps) | SR 0,07 | SR 0,09 | | z>1: OOS SR 1,35, IS 0,16 → DÜŞÜK |

**İşlenebilirlik:** VİOP pay vadelisi bültenine göre (249 gün, 11.2025–10.2026) medyan günlük işlem hacmi AKBNK 4.028, THYAO 3.688, ASELS 3.444, YKBNK 3.035, ISCTR 2.774, ASTOR 2.167, TUPRS 1.905, KCHOL 1.874 mn TL … en düşükler VESTL 98, DOAS 70 mn TL. Yani 47 kontratın çoğu günlük işlem için yeterince likit; sorun likidite değil, **sinyalin olmaması**. Pay vadelilerinde akşam seansı yok, gap fiyatlanması yakalanamaz. VİOP açılış seansı verisi var (bülten "ACILIS SEANSI" sütunları), ama gap-fade için açılış fiyatından dolum iyimser bir varsayım.

## 8. Saatlik ek (lead_hourly)
47 hedef × 97 lider, aynı gün içi r_{h-1} → r_h (kendi ve XU100 r_{h-1} kontrollü). BH 0; en güçlüler GESAN/ASTOR/CANTE/EKGYO (bireysel yatırımcı ağırlıklı) → büyükler pozitif (t 3–4,3, pc ≈0,05–0,07), ama ilk yarı top-200'ün ikinci yarıda replikasyonu %2,0 (null ≈%2,5). Seçilen en iyi 5 çift brüt 1,2–1,9 bps/bar, 8 bps maliyet karşısında anlamsız. Not: 15:00 kapanış seansı barı veride neredeyse yok; kapanış müzayedesi kaynaklı öncülük test edilemedi.

## 9. Karşı argümanlar ve sınırlamalar
- **Güç:** Günlük NW t testleri \|pc\|≈0,05'lik etkileri tek tek yakalayabilir (n≈3.200). BH 157 bin testte p≈3·10⁻⁷ eşiği istiyor (\|t\|≈5); \|pc\|<0,08 bir ilişki tek başına geçemez. Bu yüzden "yok" demek "ekonomik olarak işlenebilir büyüklükte yok" demek. Bunu null ile kalibre edilmiş fazlalık ve IS→OOS replikasyonu destekliyor.
- **Kontrol seçimi:** XBANK/XUSIN kontrolü banka→banka ve sanayi içi öncülüğü kısmen emebilir. Piyasa-göreli tarama (sektör + EW) ve kontrolsüz ekonomik çift tablosu aynı sonucu veriyor.
- **Sektör endeksleri:** Yahoo'da XHOLD/XGIDA/XELKT/XKMYA... günlük verisi yok (tek satır). Holding, enerji, gıda, telekom için resmi sektör kontrolü kullanılamadı.
- **Veri:** SASA'da Yahoo hacmi 2025-06'dan beri günlerin ~%45'inde 0 (veri hatası). Bu günler düşürüldü, SASA'nın son dönemi seyrek. TRALT/TRMET yeni kodlar, saatlik ilk yarı yok. Yahoo açılış fiyatı = tek fiyat açılış müzayedesi; gap/gün-içi ayrıştırması buna dayanıyor.
- **Mekanik içerme:** XU100 hedefi ve lideri içeriyor. Lagged kontrollerde etkisi küçük; senkron kümelemede EW177 ile ARI 0,70, matris benzerliği 0,75.
- **Rejim:** Senkron kümeler 2021 sonrası belirgin sıkılaştı (KKM/yüksek enflasyon döneminde banka ve tema hareketleri). Eyl–Eki 2026 fon krizi örneklemin son 2 ayı; ayrı test edilmedi.
- **Bayat fiyat:** Hedefler likit olduğundan klasik büyük→küçük gecikmesi ancak VİOP dışı küçük hedeflerde görülürdü; bu tur kapsamı dışında. Likidite eğimi (+0,25 / −0,33) bu yönü doğruluyor.

## 10. TradingView
Hisseler: `BIST:<KOD>` (ör. BIST:THYAO, BIST:AGHOL, BIST:CCOLA, BIST:EUPWR). VİOP pay vadelisi (47 dayanak): `BIST:<KOD>1!` (ör. BIST:AEFES1!, BIST:AKBNK1!, BIST:GARAN1!). XU030 vadelisi `BIST:XU0301!`. EW177 faktörü için TradingView'da hazır ticker yok; yaklaşık olarak BIST:XUTUM − BIST:XU100 (veya BIST:XYUZO) kullanılabilir (doğrulanmadı, '?').

## 11. Dosyalar
- `out/f_y_hisse.csv` — 454 satır: 22 aile özeti, 150 senkron (küme + eş + ekonomik çift), 230 öncülük (214 ekonomik yön + tarama adayları + piyasa düzeyi), 37 backtest.
- `out/y_hisse_matrix.parquet` — tam matris (231.616 satır): hedef × lider × dep (cc/gap/intra/intra_g/cc_rel/gap_rel/intra_rel) × lag; b, t, pc, n, p, BH bayrakları, IS/OOS/PRE t, 2014–2026 yıllık t, hacim filtreli t, likidite oranı, bayat bayrağı.
- `out/code_y_hisse/res/` — sync.txt, fdr.txt, rel.txt, pairs.csv, bt.txt, gapfade.txt, hourly.txt, market.txt, viop_liq.csv, leader_scores.csv, follower_scores.csv, clusters_*.csv.
