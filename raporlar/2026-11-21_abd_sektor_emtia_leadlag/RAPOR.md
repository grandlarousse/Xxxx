# ABD piyasası: sektör ve emtia araçları, işe yarayan yöntemler ve 1–3 günlük kapanış sinyalleri

22 Kasım 2026 · Veri: 20 Kasım 2026 kapanışına kadar · Yatırım tavsiyesi değildir.

## 1. Kısa yanıt

- **"A yükseldi, ertesi gün B'yi al" türü öncülük ABD'de günlük veride yok.** Yaklaşık 63 bin işlem testi ve 404 bin çiftlik tarama yaptık; sıkı ölçütle tek bir "sağlam" sinyal çıkmadı. Bilgi aynı gün fiyatlanıyor.
- **Denenebilir üç kural kaldı** (bölüm 3): panik günü dönüşü (VIX > 25 iken günün dibinde kapanan QQQ'yu al), MU → WDC, rafineri marjı → VLO. Üçü de bağımsız kodla yeniden üretildi; çürütme testlerinden zayıflayarak geçti. Senin uygulayacağın hâlleriyle (yalnız alım, korumasız) 2019 sonrası kanıtları zayıf: "işe yarar" değil, "denenebilir" say.
- **Beklenti küçük:** işlem başına net %0,2–0,3. Makul pozisyon boyutuyla üç kuralın toplam katkısı yılda sermayenin %1,5–2'si düzeyinde; kötü yılda eksi. "Ciddi kazanç" beklentisini bu veriler desteklemiyor.
- **Maliyet belirleyici:** hesaplar gidiş-dönüş 5 bps (bps = yüzde birin yüzde biri) maliyetle yapıldı. Yüzde 0,25 komisyon alan kurumda maliyet 50 bps'i aşar ve hiçbir kural çalışmaz.
- **Her sektör ve emtia için araç haritası** bölüm 4'te; günlük sinyal tablosunu `kod/gunluk_sinyal.py` üretiyor.
- **Bugün:** VIX 35,9. 1. kural 20 Kasım kapanışında açıktı. Pazartesi 23 Kasım için gerçek emir önermiyorum: önce kâğıt üstünde izle.

## 2. Ne yapmalıyım

1. **Önce maliyeti çöz.** Kapanış müzayedesine emir (MOC/LOC, bölüm 6) gönderebilen, düşük komisyonlu bir kurum şart. Kurumun 5 bps'in üstündeki her 1 bps'i beklentiden düşer: 15–20 bps'te 2. ve 3. kural, 30 bps'te 1. kural biter.
2. **Kâğıt üstünde başla: en az 3 ay ya da 5 sinyal.** Amaç kuralı kanıtlamak değil (bu sürede kanıtlanamaz), emir düzenini ve saatleri denemek. Her işlem günü 23:40 TSİ'de (yazın 22:40) `python3 kod/gunluk_sinyal.py` çalıştır; tabloyu ve ertesi günün sonucunu kaydet.
3. **1. kuralı uygularken:**
   - Araç QQQ. IWM ve SMH eklenebilir, ama IWM'de 2019 sonrası kanıt zayıf, SMH'de tek işlem −%10 olabiliyor. Kaldıraçlı ETF ve tek hisse yok.
   - Birden çok ETF aynı gün sinyal verse de tek bahistir. Toplam pozisyon sermayenin %15–20'sini geçmesin. Bu boyutla tarihteki en kötü tek işlem (−%11–12) sermayenin yaklaşık %2'sine, art arda en kötü beş sinyal (−%20) %3–4'üne denk gelir.
   - Emri en geç 23:45 TSİ'de gir (yazın 22:45).
   - Çıkış: ertesi gün kapanış emriyle sat. O gün yine sinyal varsa satma, ekleme de yapma; sinyalin bittiği günün kapanışında sat.
4. **Kapanışı kaçırdıysan** ertesi açılışta girebilirsin; geçmişte etkinin yaklaşık dörtte üçü korundu (+35 bps), ama 2019 sonrası kanıtı zayıf. Ertesi kapanışa kaldıysan girme: o noktada etki kalmıyor (+10 bps, anlamsız).
5. **2. ve 3. kuralı çok küçük boyla dene.** 2. kural: sermayenin en çok %5'i (WDC bu dönemde çok oynak). 3. kural yalnız VIX ≤ 20 iken geçerli; bugün kapalı.
6. **Yapma listesi:** öncü hisse ya da emtia hareketine bakıp takipçiyi almak; takvim etkilerine (ay dönümü, Fed toplantısı öncesi) tek başına güvenmek; bilanço sonrası sürüklenme beklemek; kaldıraçlı ETF'i birkaç gün taşımak; vadeli tabanlı emtia ETF'lerini (UNG, BOIL) uzun süre tutmak.
7. **Zarar sınırı:** 1. kuralın işlem getirilerinin toplamı −%20'ye inerse bırak (%18 boyla bu, toplam paranın yaklaşık %3,5'i eder). Kuralın canlıda doğrulanması yaklaşık 300 işlem ister; yılda 12 sinyalle bu pratik bir sürede olmaz. Bu yüzden ilk yılların kazancı ya da kaybı tek başına bir şey kanıtlamaz.
8. **Önümüzdeki günler:** 26 Kasım NYSE kapalı. 27 Kasım'da erken kapanış (13:00 ET = 21:00 TSİ; betik 20:40). Fed toplantısı 8–9 Aralık, enflasyon verisi 10 Aralık 08:30 ET. Ayın son işlem günü (30 Kasım) ve Fed karar günü kapanışında alım geçmişte hafif olumsuzdu (bölüm 5.4); o günlerde yeni alım açmamak makul bir süzgeç.

## 3. Sinyaller

Terimler. **VIX**: S&P 500 opsiyonlarından hesaplanan beklenen oynaklık endeksi; 25'in üstü gergin piyasa. **IBS**: (kapanış − günün en düşüğü) / (günün en yükseği − en düşüğü); 0'a yakınsa fiyat günün dibinde kapanmıştır. **z**: günlük değer bölü önceki 60 günün standart sapması; +1, alışılmış bir günlük hareketin üstü demek. **Piyasadan arındırılmış**: SPY'ın aynı günkü hareketinin etkisi çıkarılmış. **SPY ile korunmuş**: test, aynı anda SPY satılmış gibi hesaplanmış; sen bunu yapmayacaksın, o yüzden "korumasız alım" sonuçlarına bak. **Getiri sayıları**: maliyet düşülmüş ve aracın o dönemdeki olağan ortalama getirisi çıkarılmış; yani kuralın fazladan kattığı. **t (seçim dönemi / sonraki dönem)**: ortalamanın kaç standart hata uzakta olduğu; 2'nin altı zayıf, 3'ün üstü güçlü. Seçim dönemi 2005–2018, sonraki dönem 2019–2026.

### Kural 1: Panik günü dönüşü

- **Kural:** VIX > 25 ve ETF'in IBS'i < 0,2 ise kapanışta al, ertesi kapanışta sat. VIX için dünkü kapanış da kullanılabilir; gün içinde VIX izlemek gerekmez.
- **Araç:** QQQ (istersen IWM, SMH).
- **Sıklık:** QQQ'da yılda ortalama 11–12 sinyal; medyan yıl 5–6; 22 yılın 6'sında hiç yok. Üç ETF birlikte yılda ~15 sinyal günü.
- **Gerçekçi beklenti:** işlem başına net ≈ +%0,3. İsabet %55–58. İşlem başına standart sapma %2,7. En kötü işlem −%11–12; art arda 5 sinyalde −%20.
- **Güçlü kanıt:** 12 ETF'lik sepet, 2005–2026: 452 sinyal günü, +46 bps, t 3,7; 17 yılın 16'sı pozitif; dört kriz dönemi çıkarılınca +56 bps (t 2,9). QQQ 2000–2026: +40 bps (t 2,6).
- **Zayıf kanıt:** sepetin 2019 sonrası t'si 1,8; QQQ tek başına t 2,0 / 1,9 (ön kayıtlı ölçütü geçmiyor). Hiç bakılmamış 2000–2004'te +11 bps (t 0,5). Sonuca bakmadan kurulan sepette +28 bps. Yavaş ayı piyasasında çalışmıyor (2022: +13 bps).
- **Güven:** sepet hâli KOŞULLU; senin uygulayacağın hâl İZLE düzeyi.
- **20 Kasım:** QQQ, IWM ve SMH'de açıktı (VIX'in 25'i aştığı dönemin 2. günü).

### Kural 2: Bellek → depolama (MU → WDC)

- **Kural:** MU'nun piyasadan arındırılmış günlük getirisinin z'si ≥ +1 ise kapanışta WDC al, 3 gün tut.
- **Sıklık:** yılda ~33 sinyal.
- **Gerçekçi beklenti:** 20–50 bps/işlem. WDC'nin 3 günlük oynaklığı uzun dönemde ~%5, şu an ~%9.
- **Güçlü kanıt:** iki yönlü ve SPY ile korunmuş hâli: 1.444 işlem, +51 bps, t 3,7 / 2,4. MU, 158 aday öncü arasında 1. sırada; ters yönde etki yok. Ertesi açılış girişi +41 bps.
- **Zayıf kanıt:** korumasız alım +52 bps ama t 1,0 / 1,7; en iyi 10 işlem çıkınca +21 bps. Seçim dönemindeki güç satış bacağından geliyor.
- **Güven:** korumalı hâli KOŞULLU; korumasız alım İZLE düzeyi. Küçük boy.
- **20 Kasım:** kapalı (z −0,8).

### Kural 3: Rafineri marjı → VLO

- **Kural:** 3-2-1 rafineri marjının günlük dolar değişiminin piyasadan arındırılmış z'si ≥ +1 ve VIX ≤ 20 ise kapanışta VLO al, 2 gün tut. Marj = (2 × benzin + 1 × dizel − 3 × ham petrol) / 3, dolar/varil; betik hesaplar. 20 Kasım'da 41 $/varil.
- **Sıklık:** yılda ~20 sinyal.
- **Gerçekçi beklenti:** 15–30 bps/işlem.
- **Güçlü kanıt:** SPY ile korunmuş: +28 bps, t 2,5 / 2,1; VIX ≤ 20 iken +35 bps (t 3,2 / 2,4). Ham petrol, Brent ve XLE aynı etkiyi vermiyor (öncüye özgü). Sekiz rafineri hissesinin sekizinde işaret pozitif.
- **Zayıf kanıt:** korumasız alım +38 bps (t 2,3 / 1,4); VIX ≤ 20 iken tüm dönemde +48 bps ama 2019 sonrasında +22 bps (t 0,9). En iyi 10 işlem çıkınca sonraki dönem t'si 1,2.
- **Güven:** korumalı hâli KOŞULLU (yalnız sakin piyasada); korumasız alım yalnız izleme ya da çok küçük boy.
- **20 Kasım:** kapalı (z −0,8; VIX 35,9).

**Yıllık katkı hesabı (kaba):** 1. kural: %0,3 × 12 işlem × %18 pozisyon ≈ sermayenin %0,6'sı. 2. kural: %0,2 × 33 × %10 ≈ %0,7. 3. kural: %0,2 × 20 × %10 ≈ %0,4. Toplam yılda %1,5–2; kötü yılda eksi.

**İzleme adayı (para koyma):** soya yağının (ZL=F) piyasadan arındırılmış z'si ≥ +1 → ertesi gün BG ve ADM. 2019–2026'da korumalı hâli +26 / +25 bps (t 3,6 / 3,4); 2020'den beri her yıl pozitif ama 2022'ye kadar küçük. 2018 öncesinde yok. Yalnız alım yapan için 2019 sonrası +17 bps (t 1,6). Biyoyakıt politikasıyla uyumlu bir "yeni rejim" olabilir; yaptığımız test sayısında bu büyüklükte bir sonuç şansla da beklenir.

**Elenenler (özet):**

| Grup | Test sayısı | Sonuç |
|---|---|---|
| Önceden yazılı 925 öncü → hedef çifti (emtia → hisse, lider → takipçi, faiz/kredi/dolar/VIX → sektör) | 8.298 | 0 sağlam, 1 koşullu (MU → WDC). Şansla beklenen de bu kadar |
| Emtia özel yapıları (altın/gümüş oranı, vade eğrisi, enflasyona endeksli tahvil, dolar, 52 hafta zirvesi, stok raporu günleri) | 403 | Yalnız rafineri marjı → VLO kaldı. Emtia ETF'lerinde 52 hafta zirvesine yakınken almak ters çalışıyor |
| Çapraz varlık (VIX vade yapısı, kredi, faiz, dolar, risk iştahı, Bitcoin → kripto hisseleri) | 867 | Hiçbiri. Görünen etkiler piyasanın kendi aşırı satış dönüşü |
| Körlemesine tarama (738 öncü × 548 hedef) | 403.876 çift | Seçim döneminde seçilen 171 çiftten sonraki dönemde tutan oran şansla aynı (%1). Her yıl yeniden seçimle: maliyetsiz +2 bps, maliyetle −7 bps |
| "Grup içinde geride kalan hisse yetişir" | 34 | Maliyetsiz kazanç 2005–09'da 9 bps, 2022–23'te 0; 5 bps maliyetle eksi |
| Aracın kendi geçmişi (IBS, 2 günlük RSI, art arda düşüş, momentum; 186 ETF ve 40 hisse grubu) | 51.086 | Tek tutarlı küme 1. kural. Momentum ve "en iyileri/en kötüleri sırala, al" kuralları çalışmıyor |
| Takvim (ay dönümü, tatil öncesi, Fed toplantısı, opsiyon vadesi, haftanın günü, enflasyon/istihdam günleri) | 1.749 | 0 sağlam, 0 koşullu. Ay dönümü, Fed öncesi ve haftanın günü etkileri kayboldu; tatil öncesi etki yalnız son dönemde görünüyor (kanıt değil) |
| Bilanço (sonrası sürüklenme, emsallere yayılım, öncesi prim) | 74 | Hiçbiri. Büyük tepkiden sonra maliyeti aşan devam yok |
| Sigorta-borsa grubunda "aşırı yükseleni sat", temel tüketimde "düşeni al", rafineri marjı → PBF, IYR, EWJ | — | Çürütmede düştü (seçim ürünü ya da veri yanılgısı) |

## 4. Sektör ve emtia araç haritası

Parantez içindeki iki sayı: 2026'da yılbaşından beri getiri / son 1 ay (%), 20 Kasım itibarıyla. Likidite ölçütü: ETF için günlük en az ~20 mn $, hisse için ~50 mn $; altındakiler "ince" diye işaretli. "Yüksek betalı" = piyasadan daha sert hareket eden. "Sürücü" sütunundaki ilişkilerin hepsi test edildi; aksi yazılmadıkça **aynı gün fiyatlanıyor, ertesi güne öncülük yok**. Ayrıntılı kartlar: `ek/sektor/`, `ek/emtia/`.

### 4.1 Sektörler

| Sektör / alt sektör | Ana ETF | Kaldıraçlı / ters | En likit öncüler | Yüksek betalı takipçiler | 1–3 günde ne sürer |
|---|---|---|---|---|---|
| **Teknoloji** – geniş | XLK (+4 / −18) | TECL / TECS 3x; TQQQ / SQQQ 3x (Nasdaq-100) | NVDA, MSFT, AAPL, AVGO | — | Yapay zekâ harcama anlatısı, faiz |
| Yarıiletken | SMH (+11 / −24), SOXX (+23 / −22) | SOXL / SOXS 3x; NVDL 2x NVDA | NVDA, AMD, AVGO, TSM, MU, AMAT, LRCX, ASML | SMCI, CRDO, ALAB, COHR, LITE, AAOI | NVDA haberleri, TSMC aylık satış, bellek fiyatı |
| Donanım, ağ, depolama | (XLK içinde) | — | DELL, ANET, CSCO, VRT, STX, WDC | SNDK, CLS, CIEN | MU → WDC: 2. kural |
| Yazılım, bulut | IGV (−13 / −16) | likit kaldıraçlı yok | MSFT, ORCL, PLTR, NOW, CRM | DDOG, TEAM, MDB, SNOW | Büyük şirket bilançoları, 10 yıllık faiz |
| Siber güvenlik | CIBR (+28 / −11) | — | PANW, CRWD, FTNT, NET | OKTA, ZS, S | Grubun en dirençlisi |
| **İletişim** – internet, medya | XLC (−14 / −7) | FNGU 3x | GOOGL, META, NFLX, DIS | RDDT, SNAP, PINS, TTD | XLC pratikte META + GOOGL bahsi |
| Telekom | IYZ | — | T, VZ, TMUS | — | Savunmacı; düşük oynaklık |
| **Takdire bağlı tüketim** – perakende | XLY (−5 / −2), XRT (+2 / −3) | — | AMZN, WMT, COST, HD, TGT, TJX | CVNA, W, SHOP, RH | Bilanço sezonu; WMT/COST savunmacı |
| Otomotiv, elektrikli araç | (likit ETF yok) | TSLL 2x TSLA | TSLA, GM, F | RIVN, LCID, NIO, XPEV | TSLA ve Çin akışı |
| Konut | ITB (−4 / 0), XHB (−5 / −3) | NAIL 3x | DHI, LEN, PHM, NVR, TOL | RKT, BLDR, Z, OPEN | Mortgage ve 10 yıllık faiz (aynı gün) |
| Seyahat, eğlence | JETS (−3 / +1) | — | UAL, DAL, AAL, BKNG, RCL, CCL | NCLH, JBLU, ALK, DKNG | Petrol (ters yön, aynı gün) |
| Çin ADR'leri | KWEB (−39 / −11), FXI (−18 / −4) | YINN / YANG 3x | BABA, PDD, JD, BIDU | FUTU, BILI, NIO | Hong Kong seansı ABD açılışında fiyatlanmış olur |
| **Finans** – geniş | XLF (+1 / −4) | FAS / FAZ 3x | JPM, BAC, GS, MS, C, WFC | GS, MS, COF, IBKR | XLF'nin dörtte biri BRK-B, V, MA |
| Bankalar | KBWB, KRE (+7 / −6), KBE (+4 / −5) | DPST 3x (25 mn $, sınırda) | JPM, BAC; PNC, USB, TFC, FITB, KEY | WAL, ZION, FLG | Getiri eğrisi (öncülük çıkmadı) |
| Borsalar, varlık yöneticileri | (IAI ince) | — | SCHW, BLK, CME, ICE, BX, KKR, APO | ARES, CG, LPLA, HOOD | CME ve CBOE piyasa düşerken yükselir |
| Ödeme, finansal teknoloji | (XLF içinde) | — | V, MA, PYPL, SOFI | XYZ, AFRM, UPST | — |
| Sigorta | KIE (+8 / −1) | — | TRV, CB, PGR, ALL, MET, AIG | MET, PRU | Düşük oynaklık |
| Bitcoin ve kripto hisseleri | IBIT (−34 / −28), BITO (Bitcoin fonları) | BITX 2x; CONL 2x COIN | MSTR, COIN, HOOD | IREN, CIFR, CLSK, MARA, RIOT | Bitcoin → hisse öncülüğü yok. Madenciler artık yapay zekâ barındırma hissesi gibi davranıyor |
| **Gayrimenkul** | XLRE (+8 / 0), IYR, VNQ | DRN / DRV 3x (ince) | WELL, EQIX, AMT, DLR, PLD | IRM, CBRE, AGNC, NLY | 10 yıllık faiz |
| **Sağlık** – geniş, ilaç | XLV (+16 / −2); ilaç: IHE | CURE 3x (ince) | LLY, JNJ, ABBV, MRK, AMGN, PFE | NVO, ALNY, HIMS | Politika ve ilaç onayı haberleri |
| Biyoteknoloji | XBI (+15 / −8), IBB (+18 / −5) | LABU / LABD 3x | REGN, VRTX, AMGN, GILD | MRNA, CRSP, NTLA, VKTX | Risk iştahı, faiz |
| Cihaz, sağlık sigortası | IHI (−10 / +1), IHF (+14 / −10) | — | TMO, ISRG, SYK, BSX; UNH, CVS, HUM, ELV | NTRA, DXCM; HUM, CNC | Medicare duyuruları: tek günde −%10'u aşan düşüşler |
| **Temel tüketim** | XLP (+19 / 0) | — | WMT, COST, PG, KO, PEP, PM | CELH, EL, DLTR, DG | Savunmacı rotasyon |
| Tarım işleme | (MOO ince) | — | ADM, BG, TSN | CTVA | Soya yağı → BG/ADM: izleme adayı |
| **Sanayi** – geniş, makine | XLI (+2 / −6), PAVE, GRID | DUSL 3x (ince) | GEV, CAT, ETN, PWR, DE | STRL, PRIM, MTZ, VRT | Yapay zekâ altyapı anlatısı (NVDA ile aynı gün) |
| Havacılık, savunma | ITA (−7 / −3), XAR | DFEN 3x (ince) | GE, BA, RTX, LMT, NOC, GD | KTOS, AVAV, AXON | Jeopolitik haber |
| Taşımacılık, denizcilik | IYT (+6 / −4) | — | UNP, UPS, CSX, FDX; FRO, DHT, STNG | XPO, SAIA; TNK | Tankerlerde navlun ve Hürmüz |
| **Kamu hizmetleri** | XLU (+2 / 0) | UTSL 3x (ince) | NEE, SO, DUK, CEG, VST | TLN, NRG, BE | Düzenlenmiş şirketler faizle; bağımsız üreticiler yapay zekâ anlatısıyla |
| **Enerji** – geniş, arama-üretim | XLE (+38 / −10), XOP (+35 / −15) | ERX / ERY 2x; GUSH / DRIP 2x (sınırda) | XOM, CVX, COP, OXY, EOG | APA, CVE, PBR | Petrol (aynı gün); 2026'da SPY'la ters yönlü |
| Petrol hizmetleri | OIH (+16 / −12) | — | SLB, BKR, HAL | RIG, VAL, PTEN, LBRT | Petrol; sondaj kulesi sayısı |
| Rafineri | CRAK (41 mn $, sınırda) | — | VLO, MPC, PSX, DINO | PBF, DK, CVI, PARR | Rafineri marjı: 3. kural |
| Boru hattı, LNG; doğal gaz | AMLP (+12 / −5) | — | LNG, WMB, KMI; EQT, EXE, AR | — | Doğal gaz → üretici öncülüğü yok |
| Uranyum, nükleer | URA (−37 / −21) | — | CCJ, CEG, VST, BWXT | LEU, UEC, NXE, OKLO, SMR | Uranyum fiyatından çok yapay zekâ anlatısı |
| Güneş, temiz enerji | TAN (−31 / −18), ICLN | — | FSLR, NXT, ENPH | SEDG, RUN, ARRY | Faiz, politika |
| **Malzeme** – kimya, gübre | XLB (+8 / −6) | — | LIN, SHW, DOW, LYB, CF, MOS, NTR | MOS, CF, LYB | Gübrede Orta Doğu kaynaklı üre arz şoku (kimya için neden doğrulanmadı) |
| Altın madencileri | GDX (−20 / −16), GDXJ (−29 / −20) | NUGT / DUST 2x; JNUG / JDST 2x | NEM, AEM, B, WPM, AU, KGC | CDE, BTG, GFI, IAG | Altın (aynı gün); gecikme yok |
| Gümüş madencileri | SILJ (−33 / −22), SIL | — | HL, CDE, PAAS, AG | EXK | Gümüş |
| Bakır, çeşitlendirilmiş | COPX (−21 / −23), XME (−22 / −17) | — | FCX, VALE, BHP, RIO, SCCO, TECK | HBM, ERO | Bakır, Çin verisi |
| Çelik, alüminyum | (SLX ince) | — | NUE, STLD, CLF, AA | CLF, CENX | Gümrük tarifesi haberleri |
| Lityum, nadir toprak | REMX (−43 / −18) | — | MP, ALB, SQM | UUUU | Çin ihracat kısıtları |
| İnşaat malzemesi, orman | (likit ETF yok) | — | CRH, MLM, VMC, WY | LPX, EXP | Faiz, konut |

### 4.2 Emtialar

| Emtia | ABD'de işlem gören araç | Yapı ve tuzak | Kaldıraçlı / ters | İlgili hisseler |
|---|---|---|---|---|
| Ham petrol (WTI, Brent) | USO (+102 / −14), BNO (+108 / −14) | Vadeli tabanlı. Yakın vade pahalıyken (backwardation) vade devri kazandırır: USO 3 yılda +%96, vadeli serisi +%10. Eğri ters dönerse eritir | UCO / SCO 2x | XOM, COP, OXY; SLB, HAL; tankerler FRO, DHT |
| Doğal gaz | UNG (−14 / +7) | Uzak vade pahalıyken (contango) erir: UNG 3 yılda −%60, vadeli +%7. Yalnız 1–3 gün için | BOIL / KOLD 2x | EQT, EXE, AR; LNG |
| Benzin, dizel | UGA (ince) | Saf dizel ETF'i yok | — | VLO, MPC, PSX, PBF |
| Uranyum | URA, URNM (madenci hissesi); Sprott fiziki uranyum fonu (Toronto'da U.U; ABD'de tezgâh üstü SRUUF) | Fon net varlık değerine ~%20 iskontolu işlem görüyor; spot fiyatı izlemiyor | — | CCJ, UEC, NXE, LEU |
| Kömür, elektrik, karbon | ETF yok (KRBN çok ince) | — | — | BTU, HCC; VST, CEG, NRG |
| Altın | GLD (−18 / −12), IAU, GLDM | Fiziki külçe; vade devri yok. Gider: GLD %0,40, IAU %0,25, GLDM %0,10 | UGL / GLL 2x | GDX, NEM, AEM |
| Gümüş | SLV (−43 / −25), SIVR | Fiziki. Oynaklığı altının ~1,7 katı | AGQ / ZSL 2x | SILJ, PAAS, HL |
| Platin, paladyum | PPLT (−37 / −17), PALL (−44 / −15) | Fiziki; hacim düşük (22–30 mn $) | UPLT, UPAL 2x (Nisan 2026'da açıldı; çok ince) | SBSW |
| Bakır | CPER (−6 / −14) | Vadeli; hacim 19 mn $; kapanış fiyatı bayat olabiliyor | CPXR, UCOP 2x (ince) | FCX, SCCO, COPX |
| Alüminyum, çinko | DBB (bakır + alüminyum + çinko sepeti, ince) | Saf ürün yok | — | AA, CENX; TECK |
| Nikel, kalay, kobalt, demir cevheri, lityum | Saf ABD ürünü yok (tek metal ETN'leri 2023'te borsadan çıktı) | — | — | VALE, BHP, RIO; ALB, SQM; MP |
| Mısır, buğday, soya, şeker | CORN, WEAT, SOYB, CANE | Vadeli; hepsi çok ince (1–10 mn $/gün); kapanış fiyatları bayat. Kısa vadeli işleme uygun değil | CXRN, WXET 2x | ADM, BG, DE, CF, MOS, NTR |
| Kahve, kakao | ABD'de ETF yok (eski ETN'ler 2023'te borsadan çıktı) | Yalnız vadeli | — | SBUX; HSY, MDLZ |
| Pamuk, canlı sığır | Tek emtia ürünü bulunamadı | Yalnız vadeli | — | TSN |
| Kereste, kurşun, pirinç, yulaf, portakal suyu, domuz, soya yağı, Avrupa gazı | ABD'de ürün yok | Yalnız vadeli (kereste için WOOD ve CUT hisse fonları çok ince) | — | WY (kereste); ADM, BG (soya yağı) |
| Tarım sepeti | DBA (+2 / −6) | Vadeli sepet; 27 mn $/gün | — | — |
| Geniş emtia | DBC (+31 / −13) | Enerji ağırlıklı vadeli sepet | — | — |

**Kaldıraçlı ETF uyarısı.** Bu ürünler günlük hedefe göre her gün yeniden dengelenir; birkaç gün ya da hafta taşınınca getiri taban varlığın katı olmaz. 2026 örnekleri: SOXX +%23 iken 3 katlı SOXL −%26; ITB −%4 iken NAIL −%39; TSLA −%23 iken TSLL −%57; SLV −%43 iken AGQ −%81. 1. kuralın sinyal günlerinde bile TQQQ, QQQ'nun üç katının işlem başına 13,5 bps gerisinde kaldı; en kötü işlemi −%18.

## 5. Gerekçe ve kanıt

### 5.1 Öncülük neden çıkmadı

Altı ayrı test ailesi aynı sonuca vardı: bir varlığın bugünkü hareketi, ilgili başka bir varlığın sonraki 1–3 gününü öngörmüyor. Önceden yazılı 925 çiftte hipotez yönünde t ≥ 2 verenlerin oranı %2, ters yönde t ≤ −2 verenlerin oranı %18'di; yani "öncü yükseldi, takipçiyi al" ortalamada kaybettirdi. Bunun bir kısmı maliyet, bir kısmı da piyasanın kendi günlük dönüşü: öncü ile takipçi aynı gün birlikte hareket ediyor, ertesi gün birlikte geri geliyor.

Körlemesine tarama bunu doğruladı. Seçim döneminde çok güçlü görünen 171 çift sonraki dönemde şansla beklenen oranda tuttu; tutanların çoğunda da hedef, kapanış fiyatı bayat olan tezgâh üstü bir kâğıttı. Her yıl yeniden seçim yapan sürümde maliyetsiz kazanç işlem başına 2 bps, maliyetle −7 bps.

Akademik yazın aynı şeyi söylüyor. NYSE'de büyük hisselerden küçüklere günlük gecikmeli ilişki 1990'ların sonunda hata düzeyine indi (Tóth ve Kertész). Ağ yöntemleriyle bulunan öncülük sinyali maliyetsiz günde 2,4 bps veriyor ve 2012'den sonra bozuluyor (Bennett, Cucuringu, Reinert). Petrol, sektör getirilerini yaklaşık 7–8 işlem günü gecikmeyle öngörüyor ve bu yalnız sektörlerin beşte birinde anlamlı (Fan ve Jahan-Parvar). Emtia, kredi, tahvil ve sektörler arası öncülük kanıtının neredeyse tamamı aylık frekansta.

### 5.2 Panik günü dönüşü (1. kural)

Çalışan tek yaygın etki kısa vadeli dönüş: yüksek oynaklık döneminde günün dibinde kapanan hisse ETF'i ertesi gün ortalamada toparlanıyor. Yazınla uyumlu: endekslerde bugünkü getiriyle dünkü getiri arasındaki ilişki 2000'lerden beri negatif (Baltussen, van Bekkum, Da 2018) ve dönüş stratejilerinin beklenen getirisi VIX'le birlikte büyüyor (Nagel 2012). Mantığı: panikte satıcılar acele eder, karşı tarafa geçen daha yüksek prim ister.

Kural ne katıyor? VIX > 25 olan her gün almak +4 bps veriyor; aynı günlerde dibe yakın kapanmayan ETF'ler −7 bps. Fark kuraldan geliyor: sinyal günleri rastgele günlerle değiştirilince bu sonuç 1.000 denemenin 4'ünden azında çıkıyor. Kazanç gecede değil, ertesi gün içinde oluşuyor.

Zayıf yanları, çürütme testlerinden:
- **Seçim yanlılığı.** Tek tek ETF'lerde görülen 37–79 bps'lik sonuçlar sonradan seçilmiş araçlara ait. Sonuca bakılmadan kurulan sepette etki +28 bps; seçilmiş sepetin 2000–2026 birleşik sonucu +34 bps. Beklentiyi +30 bps al.
- **Tek bahis.** Kazancın yaklaşık %70'i piyasanın kendi dönüşü. 12 ETF'te sinyal = 1 sinyal.
- **Yavaş ayı piyasasında çalışmıyor** (2022: +13 bps; 2002–03 negatif). Hızlı çöküş ve toparlanmalarda çalışıyor (2008–09, 2020).
- **Kasım 2026.** Kural beş kez tetiklendi; kapanan dört işlemin toplamı sıfıra yakın (19 Kasım −%5,0).
- **"Yarıiletkene özgü" pay doğrulanmadı.** Hisse grubunda görünen ek kazanç ETF'te (SMH, SOXX) yok; eski dönem kanıtı likit olmayan hisselere dayanıyor.

20 Kasım benzeri günler için geçmiş kesitler çelişiyor: VIX'in 25'i aştığı dönemin ilk üç gününde açılan işlemler +25 bps (t 1,4); bir önceki gün de sinyal olan günler +76 bps (t 3,8). İkisi de sonradan bakılmış kesit; ağırlık verme.

Zamanlama denetimi: son 59 günün 5 dakikalık verisinde 15:45'te hesaplanan sinyal kapanıştaki sinyalle %81 örtüşüyor (15:40 ayrıca sınanmadı). VIX'i bir gün gecikmeli kullanınca sonuç aynı ya da daha iyi (+56 bps, sonraki dönem t 2,4). IBS 0,15–0,20 bandı da diğerleri kadar iyi çalışıyor; sınırda işlem açmamak temkin tercihidir, kanıt bunu gerektirmiyor.

### 5.3 Gece primi

186 ETF'in medyanında getirinin tamamı gecede (kapanış → açılış) oluşuyor: gece başına +5 bps, gün içi sıfıra yakın; bu 2019 sonrasında da sürüyor. Kapanışta alıp taşıyan profil bu rüzgârı arkasına alır. Ama tek başına strateji değil: her gece alıp sabah satmak maliyeti karşılamıyor.

### 5.4 Takvim

Ay dönümü, Fed toplantısı öncesi gün, tatil öncesi gün, opsiyon vadesi haftası, haftanın günü: 1.749 testte tek bir koşullu sinyal yok. Seçim döneminde t ≈ 2 veren ay dönümü ve Fed öncesi etkileri 2019 sonrasında sıfır. Yazın da Fed öncesi sürüklenmenin (Lucca ve Moench: 49 bps) 2015'ten sonra kaybolduğunu, klasik ay dönümünün son on yılda silindiğini bildiriyor.

Zayıf süzgeç adayları (kanıt değil): çeyrek sonu olmayan ay sonunun son günü kapanışında alım −19 bps; Fed karar günü alıp 2 gün tutmak −30 bps; tatil öncesi gün +15 bps.

### 5.5 Trend, momentum, rotasyon

Sektör ETF'lerini son 1–252 günlük getirilerine göre sıralayıp en iyileri almak 2015 sonrasında hiçbir pencerede anlamlı değil. 200 günlük ortalama süzgeci getiriyi artırmıyor, oynaklığı azaltıyor. AQR'nin zaman serisi momentumu faktöründe getiri/risk oranı (Sharpe) 1985–2009'da 1,4 iken 2015 – Mayıs 2026'da 0,24. Emtia ETF'lerinde 52 hafta zirvesine yakınken almak bizim testte ters çalıştı.

### 5.6 Bilanço

Büyük tepki (|z| ≥ 2) veren 19.056 bilanço olayında, tepki günü kapanışında tepki yönünde girmek ertesi gün −3 bps. Lider bilançosundan emsallere yayılım yok; emsal aynı gün hareket ettiyse kalan şey hafif bir geri dönüş. Bilanço öncesi alıp tepki günü satmak ortalamada +25 bps ama standart sapması %6,9, en kötü %5'in eşiği −%10: kumar. Yazınla uyumlu: büyük hisselerde bilanço sonrası sürüklenme 2006'dan beri yok (Martineau 2022).

### 5.7 2. ve 3. kural

**MU → WDC.** Önceden yazılı bir hipotezdi (bellek fiyat döngüsü: MU'nun haberi depolama hisselerine birkaç günde yayılır). MU'yu 59 yarıiletken ve 99 rastgele hisseyle değiştirince MU birinci çıkıyor; ters yön sıfır; hedefin aynı gün tepkisi hesaba katılınca da anlamlı. Zayıf yanı: seçim dönemindeki gücü satış bacağından geliyor, yalnız alım yapan için kanıt daha zayıf.

**Rafineri marjı → VLO.** Öncüye özgü: ham petrol, Brent ve XLE aynı etkiyi vermiyor, benzin marjı veriyor. Öncü bir gün geciktirilince etki kayboluyor (olması gereken bu). Ama korumalı hâli yalnız sakin piyasada çalışıyor, korumasız alımın 2019 sonrası kanıtı zayıf ve sonuç en iyi 10 işleme duyarlı.

## 6. Uygulama: emir, saat, maliyet

**Emir türü.** Kapanış fiyatından işlem için kapanış müzayedesine giden emir gerekir: MOC (kapanışta piyasa fiyatından) ya da LOC (kapanışta limitli). Emir resmi kapanış fiyatından gerçekleşir. Kapanış emri olmayan kurumda seçenek ertesi sabah açılış emri (bölüm 2, madde 4).

**Tek çizelge:** 23:40 TSİ betik, en geç 23:45 TSİ emir (yazın 22:40 / 22:45). ABD kapanışı kış saatinde (1 Kasım 2026 – 14 Mart 2027) 00:00 TSİ, yaz saatinde 23:00 TSİ.

| Borsa | Borsanın emir kesimi (ET) | Interactive Brokers'ın bildirdiği kesim | Örnek |
|---|---|---|---|
| NYSE | 15:50 | 15:50 | VLO |
| Nasdaq | MOC 15:55, LOC 15:58 | 15:55 | QQQ, SMH, WDC |
| NYSE Arca | 15:59 (2019 tarihli kaynak) | 15:50 | IWM ve ETF'lerin çoğu |

**Kurumlar** (kaynaklı bilgiler; kapanış emri desteğini hesabı açmadan önce kurumdan teyit et):

| Kurum | ABD hisse komisyonu | Kapanış emri | Gidiş-dönüş maliyet |
|---|---|---|---|
| Interactive Brokers | hisse başına 0,005 $, emir başına en az 1 $ | var | 2–5 bps (pozisyon en az ~4.000 $ ise) |
| Midas | emir başına 1,5 $ | belgelenmiş bilgi bulunamadı | 5 bps (pozisyon ~6.000 $ ise); küçük pozisyonda 25 bps'e kadar |
| İş Yatırım, Yapı Kredi | %0,25 | belgelenmiş bilgi bulunamadı | 50–70 bps |

Türkiye, Interactive Brokers'ın ülke listesinde var; hesabın hangi kuruluş altında açıldığı ve ETF erişimi doğrulanmadı. Türkiye'deki kurumlarda kapanış emri, kaldıraçlı ETF ve açığa satış desteği için belgelenmiş bilgi bulunamadı.

**Not.** Gün içi al-sat yapanlara uygulanan 25 bin dolarlık kuralı FINRA yeni gün içi teminat standartlarıyla değiştirdi (yürürlük 4 Haziran 2026; kurumlara 20 Ekim 2027'ye kadar geçiş süresi var, kurumuna sor). 1–3 gün taşıma zaten bu kurala girmiyordu. Vergi için mali müşavire danış.

## 7. Emin olunmayanlar ve doğrulama kapsamı

**Düzeltilen varsayımlar.**
- "Öncü–takipçi sinyalleriyle 1–3 günde ciddi kazanç": veriler desteklemiyor. Günlük frekansta öncülük neredeyse yok; kalan iki örnek küçük ve koşullu.
- "Her sektör ve emtia için kazandıran bir sinyal": araçlar var, sektöre özgü sinyal yok. Çalışan tek yaygın etki piyasa geneline ait.
- Kaldıraçlı ETF kazancı büyütmenin yolu değil; oynaklık yüksekken eritiyor.

**Emin olunmayanlar.**
- Üç kuralın senin uygulayacağın hâllerinde 2019 sonrası kanıt zayıf (t 1,9 / 1,7 / 0,9). Gerçek üstünlük sıfır da olabilir.
- 1. kural 2000–2004'te çalışmadı; bir sonraki yavaş ayı piyasasında da çalışmayabilir.
- Yahoo'nun enerji vadelilerindeki günlük kapanışın uzlaşma fiyatı mı (14:30 ET) son işlem mi olduğu kesinleşmedi. Dolaylı testlerde ileri bakış izi yok; 3. kuralda ertesi açılış girişi etkiyi koruyor.
- Hisse evreni bugün işlem görenlerden oluşuyor (batanlar yok). Bu yüzden hisse düzeyindeki "düşeni al" sinyallerini kullanmadık.
- 15:45 sinyalinin kapanışla örtüşmesi yalnız son 59 günde (5 panik günü) ölçüldü.
- Kartlarda "doğrulanmadı (bellek)" diye işaretli bilgiler kaldı (bazı gider oranları, kapanmış ürünlerin tarihleri).

**Doğrulama kapsamı.**
- Yöntem hesaplardan önce bağımsız bir eleştirmene denetletildi; 12 değişiklik yapıldı (`YONTEM.md` bölüm 10). Bu sırada bir veri hatası (vadeli ve kur serilerinin yaz saatinde bir gün kayması) ve bir kütüphane hatası düzeltildi.
- Ayakta kalan 8 sinyal ortak kütüphane kullanılmadan sıfırdan yeniden üretildi: sayıların hepsi tuttu. İki çürütücü sinyalleri kırmaya çalıştı: 3'ü koşullu kaldı, 5'i düştü.
- Rapordaki 37 kaynaklı iddia iki doğrulayıcıya verildi: 30'u aynen doğrulandı, 7'si kısmen doğrulandı ve raporda düzeltildi, yanlış çıkan yok. Rapordaki 28 bağlantının 27'si toplu denetimde açıldı; NYSE takvim sayfası otomatik isteği reddediyor (içeriğini doğrulayıcı görmüştü).
- Bir eleştirmen taslağı dayanak dosyalarla karşılaştırdı: backtest sayıları ve araç tablosundaki 51 yüzde tuttu; 22 itirazın hepsi işlendi (sinyal sıklığı, etiketler, betik çıktısı, eksik satırlar).
- Açık kalan: kurumların kapanış emri desteği; 15:40 zamanlaması; soya yağı adayının yeni veriyle sınanması.

## 8. Kaynaklar

Yazın:
- Tóth, Kertész: günlük öncülüğün kaybolması — https://arxiv.org/pdf/physics/0506071
- Bennett, Cucuringu, Reinert 2022 — https://arxiv.org/pdf/2201.08283
- Baltussen, van Bekkum, Da 2018 — https://personal.eur.nl/vanbekkum/2018%20JFE%20BaltussenVanBekkumDa.pdf
- Nagel 2012, Evaporating Liquidity — https://www.nber.org/papers/w17653.pdf
- Fan, Jahan-Parvar: petrol ve sektör getirileri — https://economics.ecu.edu/wp-content/pv-uploads/sites/165/2019/07/ECU0912.pdf
- Lucca, Moench: Fed toplantısı öncesi sürüklenme — https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf
- Kurov vd. 2021: sürüklenmenin kaybolması — https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html
- Ay dönümünün kaybolması (blog) — https://www.quantseeker.com/p/turn-of-the-month-strategies-do-they
- Martineau 2022 — https://cfr.ivo-welch.info/published/papers/martineau2021rest.pdf
- AQR zaman serisi momentumu verisi — https://www.aqr.com/-/media/AQR/Documents/Insights/Data-Sets/Time-Series-Momentum-Factors-Monthly.xlsx

Uygulama:
- Nasdaq kapanış müzayedesi — https://www.nasdaqtrader.com/content/productsservices/Trading/ClosingCrossfaq.pdf
- NYSE kapanış müzayedesi — https://www.nyse.com/publicdocs/nyse/NYSE_Auctions_Closing_Process_Fact_Sheet.pdf
- NYSE ve Arca kesimleri (2019 rehberi) — https://download.lightspeed.com/On%20Close%20and%20On%20Open%20Guide.pdf
- Interactive Brokers kapanış emri — https://www1.interactivebrokers.com/en/trading/orders/moc.php
- Interactive Brokers komisyon — https://www.interactivebrokers.com/en/pricing/commissions-stocks.php
- Midas ücretler — https://www.getmidas.com/ucretler/
- İş Yatırım tarife — https://www.isyatirim.com.tr/tr-tr/destek/Documents/pdf/komisyon-ve-masraf-tarifesi.pdf
- Yapı Kredi yurt dışı hisse — https://www.yapikredi.com.tr/bireysel-bankacilik/yatirim-urunleri/hisse-senetleri/yurt-disi-hisse-senetleri
- FINRA 26-10 — https://www.finra.org/rules-guidance/notices/26-10
- SEC: kaldıraçlı ve ters ETF'ler — https://www.investor.gov/publications-research-studies/info-sheets/Leveraged-Inverse-ETFs
- NYSE saatler ve tatiller — https://www.nyse.com/trade/hours-calendars
- Fed toplantı takvimi — https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm
- Enflasyon verisi takvimi — https://www.bls.gov/schedule/news_release/cpi.htm

Araçlar ve 2026 durumu: her kartın sonundaki iddia defteri (`ek/sektor/*.md`, `ek/emtia/*.md`, `ek/uygulama/l6_uygulama.md`). Altın ETF gider oranları — https://247wallst.com/investing/2026/07/05/gold-is-up-again-in-2026-and-after-reviewing-every-way-to-own-bullion-these-3-etfs-cover-the-trade-at-three-cost-levels/ · Tek metal ETN'lerinin borsadan çıkışı — https://etfdb.com/news/2023/06/09/barclays-redeems-21-ipath-etns-this-week-etfs/ · UPLT, UPAL, UCOP — https://www.proshares.com/press-releases/proshares-launches-first-etfs-targeting-2x-daily-returns-of-platinum-and-palladium · Sprott uranyum fonu — https://sprott.com/investment-strategies/physical-commodity-funds/uranium/ · Gübre arz şoku — https://www.morningstar.com/news/marketwatch/20260311360/the-sp-500s-biggest-gainer-since-the-iran-conflict-started-is-not-an-oil-stock

Kendi hesaplarımız: `ek/backtest/` (aile başına `sonuclar.csv`, `ayakta_kalanlar.csv`, `NOT.md`), `ek/dogrulama/` (yeniden üretim, çürütme A ve B, iddia doğrulaması, yöntem sınaması).

## 9. Devam notu

1. Bulunan: ABD'de günlük öncülük yok; denenebilir üç kural kaldı (panik günü dönüşü QQQ; MU → WDC; rafineri marjı → VLO, yalnız VIX ≤ 20). İzleme adayı: soya yağı → BG/ADM.
2. Ana dosyalar: bu rapor; `YONTEM.md` (ön kayıt ve eleştirmen değişiklikleri); `kod/gunluk_sinyal.py` (günlük tablo); `kod/ortak.py` (test kütüphanesi).
3. Kanıt: `ek/backtest/<aile>/`, `ek/dogrulama/CURUTME_A.md`, `CURUTME_B.md`, `YENIDEN_URETIM.md`. Araç kartları: `ek/sektor/`, `ek/emtia/`.
4. Veri depoda değil; `python3 kod/indir.py veri` ile yeniden iner (Yahoo, ~1.090 sembol), bilanço takvimi `kod/indir_bilanco.py` ile.
5. Açık işler: kâğıt üstünde izleme sonuçları; kurumun kapanış emri desteği; soya yağı adayının yeni veriyle sınanması.

Maliyet özeti: Seviye L+ (onaylı; tahmin ~41 ajan). 32 alt ajan: 26 Opus, 6 Fable. Üretici 25 (1. dalga 16; 2. dalga 7; boşluk kapatma 2); doğrulama 5 (yeniden üretim 1, çürütme 2, iddia doğrulama 2); eleştirmen 2 (yöntem, taslak). 3 üretim dalgası + doğrulama. Kontrol noktasını geçen 3 ajan (36/35, 36/35, 40/35: dosya yazımı ve kısa ön hesap). Aşılan sınır yok. 1. dalgada ortak web arama kotası doldu; 8 ajan aramayı erken kesti, boşluklar 3. dalgada kapatıldı.
