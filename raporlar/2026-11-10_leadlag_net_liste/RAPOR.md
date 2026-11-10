# Aynı kapanışta giriş, 1–3 gün: bütün araştırmalardan net liste (10.11.2026)

_Yatırım tavsiyesi değildir. Kapsam: VİOP lead-lag (02.11), kapanış 1–3 gün (04.11), kazanç stratejileri BIST + ABD (06–09.11), Midas ETF (07–10.11), altın (07–08.11), altın paneli denetimi (10.11) ve bugün yapılan bağımsız yeniden hesap._

Terimler:
- **Öncü → hedef (lead-lag):** bir varlığın hareketinin başka bir varlığın sonraki hareketini haber vermesi.
- **bps:** baz puan, %0,01. 50 bps = %0,5.
- **σ (sigma):** bir varlığın son 60 gündeki olağan günlük oynaması. "+1σ gün" = olağan oynamanın üstünde bir yükseliş.
- **z:** hareketin σ'ya oranı.
- **Fazla getiri:** işlemin getirisi eksi o yılın sıradan günlerinin aynı süredeki ortalama getirisi. BIST TL bazında zaten yükseldiği için ham getiri yanıltır; fazla getiri bunu ayıklar.
- **t:** bir ortalamanın şanstan ayırt edilebilirliği. 2'nin altı "ayırt edilemiyor", 3'ün üstü "güçlü" demek.

## Kısa yanıt

1. **Senin kalıbın ("ilgili varlık yükselmiş, ana varlık yükselmemiş → al") test edildiği hiçbir yerde çalışmıyor.** ABD ETF'lerinde, BIST çiftlerinde ve altında sonuç aynı: geride kalan yetişmiyor.
2. **Çalışan yön tersi:** öncü güçlü hareket etmiş **ve hedef de o gün aynı yöne gitmişse** hareket 2–3 gün sürüyor.
3. **Gerçek öncü → hedef kuralı olarak elde üç şey var:** ABD rafinerileri → TUPRS (tek doğrulanmış), ABD bankaları → AKBNK (yeni aday), RYGYO → RYSAS (aday, zamanlaması sorunlu).
4. **Lead-lag olmayan ama düzenine birebir uyan dört kural daha var:** güçlü XU030 gününden sonra endeks vadelisi, QQQ ve SMH'de zayıf kapanış dönüşü, SAHOL/AKBNK çifti.
5. **Hepsi küçük:** maliyet öncesi işlem başına +30…+60 bps. Bireysel VİOP komisyonuyla (gidiş-dönüş ~44 bps) çoğu sıfırlanıyor. Hiçbiri "kesin kazandırır" düzeyinde değil.

## Ne yapmalıyım

1. **Kalıbı değiştir.** Kapanışa 10 dakika kala "öncü yükseldi, hedef yerinde sayıyor" görürsen alma. "Öncü güçlü, hedef de artıda" görürsen al. Kanıt: TUPRS kuralında sinyal günü TUPRS ekside kapanmışsa fazla getiri ~0, artıda kapanmışsa 2 günde +58 bps.
2. **Aşağıdaki listeyi kullan, başka çift arama.** "Bakma" tablosundaki 40'tan fazla çift denendi ve elendi.
3. **Aracı kurumundan VİOP komisyonunu yazılı öğren.** Gidiş-dönüş 10–15 bps'in üstündeyse BIST tarafındaki kuralların çoğu kâğıt üstünde kalmalı.
4. **Yeni adayları (2, 3, 4 numara) en az 2–3 ay kâğıt üstünde izle.** Bunlar bugünkü hesaptan çıktı; ileriye dönük sınavı yok.
5. **Aynı güne düşen sinyalleri tek bahis say.** Güçlü XU030 günü, KBE ve rafineri sinyali aynı akşama denk gelirse toplam riski bir işlemlik tut. Önceki planlardaki sınır geçerli: işlem başına sermayenin ~%0,25'i.
6. **Her işlemi kaydet:** tarih, sinyal değeri, hedef o gün artıda mıydı, giriş, çıkış, maliyet.

### Günlük akış (kış saati)

| Saat (TSİ) | Bak | Karar |
|---|---|---|
| Sabah | ABD dün gece: rafineri z'si ve KBE'nin günlük değişimi | Akşam için TUPRS ve AKBNK adaylarını not et |
| 17:50 | XU030 günlük değişimi; TUPRS ve AKBNK artıda mı | Koşul tamamsa 18:00–18:10 arasında gir |
| 23:50 | QQQ ve SMH günün aralığının neresinde | Dibe yakın kapanıyorsa Midas'ta al |

## Kullanılabilir liste

Sayılar maliyet öncesi fazla getiridir; parantez içi t değeri. "Yıl" sütunu yıllık yaklaşık işlem sayısı.

### A. Gerçek öncü → hedef

| # | Kural | TradingView | Sinyal ve işlem | Fazla getiri | Yıl | Güven |
|---|---|---|---|---|---|---|
| 1 | **ABD rafinerileri → TUPRS** | Öncü: `NYSE:VLO`, `NYSE:MPC`, `NYSE:PSX`, `NYSE:PBF`, `SP:SPX`. Hedef: `BIST:TUPRS1!` | Dün gece ABD'de dört rafinerinin ortalama getirisi eksi β × S&P 500 getirisi; bunun kendi 250 günlük oynaklığına oranı z. **z > +1 ve TUPRS bugün artıda ise** kapanışta AL, 2–3 gün tut. | 2 gün +33 (2,1); 3 gün +42 (2,1). TUPRS artıdaysa +58 (2,7) / +67 (2,3) | ~26 | ORTA–DÜŞÜK |
| 2 | **ABD bankaları → AKBNK** (yeni aday) | Öncü: `AMEX:KBE`. Hedef: `BIST:AKBNK1!` | KBE dün gece ≥ +1,5σ (bugünlerde ≈ +%1,6) ise bugün kapanışta AKBNK AL, 2 gün tut. | +64 (2,7) | ~16 | DÜŞÜK |
| 3 | **RYGYO → RYSAS** (aday, spot) | Öncü: `BIST:RYGYO`. Hedef: `BIST:RYSAS` | RYGYO günlük getirisi z > +1 (≈ +%3) ise RYSAS'ı kapanışta AL, ertesi kapanışta sat. | +54 (3,1) | ~36 | DÜŞÜK |

### B. Lead-lag değil, ama aynı kapanış + 1–3 gün düzenine uyuyor

| # | Kural | TradingView | Sinyal ve işlem | Fazla getiri | Yıl | Güven |
|---|---|---|---|---|---|---|
| 4 | **Güçlü XU030 günü → endeks devamı** (yeni aday) | `BIST:XU030`, işlem `BIST:XU030D1!` | XU030 günlük getirisi ≥ +1σ (bugünlerde ≈ +%1,9) ise endeks vadelisini kapanışta AL, 3 gün tut. | +30 (2,3) | ~31 | DÜŞÜK |
| 5 | **QQQ zayıf kapanış dönüşü** (Midas) | `NASDAQ:QQQ` | IBS < 0,10 ve gün ekside ise kapanışta AL, 3 gün tut. IBS = (kapanış − günün en düşüğü) / (en yüksek − en düşük). | +62 (3,4), 2016'dan beri | ~19 | ORTA |
| 6 | **SMH zayıf kapanış dönüşü** (Midas) | `NASDAQ:SMH` | IBS < 0,20 ise kapanışta AL, ertesi kapanışta sat. | +38 (3,6), 2016'dan beri | ~50 | ORTA |
| 7 | **SAHOL/AKBNK çifti** (VİOP) | `BIST:SAHOL1!`, `BIST:AKBNK1!` | Oran z'si > +1,5: SAHOL SAT + AKBNK AL. < −1,5: tersi. \|z\| ≤ 1,5 olunca çık. | Önceki çalışma net +63,7 (3,12); gerçekçi +30–50 | ~18 | ORTA (koşullu) |

### Satır satır notlar

**1. TUPRS.** Elde iki bağımsız hesapta aynı yöne çıkan tek öncü–hedef kuralı.
- Önceki VİOP çalışması (vadeli uzlaşma fiyatlarıyla, iki yön): 2 gün tutuşta net +42 bps (t 2,7). Çürütme turu beklentiyi +20–25'e indirdi.
- Bugünkü yeniden hesap (spot fiyatla) uzun tarafı doğruladı; kısa taraf zayıf. Kısa işlemi yarım boyla yap ya da hiç yapma.
- Zayıf yanları: 2024–26'da t ≈ 0,7–1,0; en iyi 10 işlem çıkınca t 1,45; dört hisseden PBF çıkınca zayıflıyor.
- Eşik bugünlerde ≈ %2,7 fark (piyasa olağanüstü oynak; sakin dönemde daha düşük).
- Hazır araç: `raporlar/2026-11-04_kapanis_1-3gun/rehber/tuprs/` (`sinyal_tuprs.py`, `tuprs.pine`).

**2. KBE → AKBNK.** Bugünkü taramadan çıktı, önceki çalışmalarda yoktu.
- 2011–21'de +68 (t 2,5), 2022 sonrası +56 ama t 1,1. 16 yılın 11'i pozitif.
- Endeksin o gün güçlü olmasından bağımsız: XU030'un sakin olduğu günlerde de +56 (t 2,0).
- Hedef sıralaması tutarlı: XU030 +32 < dört banka sepeti +50 < AKBNK +64.
- Çekince: önceki VİOP çalışması sektör emsallerinin kapanıştan kapanışa etkisini t ≤ 1,5 ile elemişti. Bu aday o sonuçla çelişiyor; kâğıtta sına.

**3. RYGYO → RYSAS.** İki ayrı hesapta pozitif, ama senin düzenine tam oturmuyor.
- Önceki çalışma: net +34,8 bps (t 2,40), 2024–26'da +97,5 (t 3,92); en iyi 10 işlem çıkınca t 1,04.
- Sinyal RYGYO'nun kapanış müzayedesinde (18:08–18:10) kesinleşiyor. Kapanışa 10 dakika kala gördüğün değer değişebilir.
- Bir gün geç girince kenar kayboluyor (+17, t 1,0).
- İnce hisse: RYSAS'ın medyan günlük hacmi ~145 milyon TL.
- Kazancın çoğu 2022 sonrasında; öncesi t 1,5.

**4. Güçlü XU030 günü.** Senin sorduğun kalıbın çalışan hâli bu: "geride kalanı al" değil, "güçlü günü izle".
- 458 işlem, 16 yılın 13'ü pozitif. Rastgele günlerle karşılaştırmada p = 0,0025.
- Tek tek hisse almak bir şey katmıyor: 15 hisselik sepetin endekse göre farkı sıfır. Bu yüzden işlem endeks vadelisinde.
- Tersi yok: sert düşüş gününden sonra açığa satış kazandırmıyor.
- 2022 tek başına ortalamanın epeyini taşıyor (o yıl +90).

**5–6. QQQ ve SMH.** Öncü yok; varlığın kendi zayıf kapanışından dönüşü.
- İki kural da 2016'dan beri her yıl pozitif (QQQ 11/11), 2011–15'te yok. Rejime bağlı.
- QQQ'da kapanıştan 10 dakika önce tahminle girilince önceki çalışmanın rakamı +76'dan +56 bps'e iniyor (t 2,4).
- SMH'de kenar yalnız aynı kapanışta var; ertesi kapanışta girince ~+2 bps'e düşüyor. Senin düzenin için uygun olan tam bu.
- İkisi büyük ölçüde aynı günlerde sinyal veriyor; tek bahis say.
- Midas maliyeti: emir başına 1,5 USD; 2.500 USD pozisyonda gidiş-dönüş ~12 bps. Daha küçük pozisyonda kenarı yer.

**7. SAHOL/AKBNK.** İki bacaklı, düşük komisyon şart.
- 3 günle sınırlayınca +26 (t 1,28)'e iniyor; işlemlerin %10'u 10 günü aşıyor. 1–3 güne tam sığmıyor.
- Yeniden hesapta 44 bps maliyetle 3 günlük sonuç +6 bps.
- Kazanç çalışmasında 1–3 günlük sürüm emekli edilip 20 günlük sürüme geçilmişti.

## Listeden çıkanlar

Önceki listelerde vardı, bugünkü kanıtla çıkardım:

| Kural | Neden |
|---|---|
| Altın → TRALT (`TVC:GOLD` 17:55 → `BIST:TRALT1!`) | 10.11 denetimi: bireysel maliyetle hedge'siz +11,5 bps (t 0,58). 2021–23'te üç yıl zarar. Kazandırdığı kanıtlı değil. |
| Koza grubu (`BIST:TRMET1!` / `BIST:TRALT1!`) | Sönmüş. 2024–26 t 0,93; yeniden hesapta net ~0. |
| `ASX:FMG` + `ASX:BHP` → EREGL | Yeniden hesapta 2022 sonrası hedge'li sonuç negatif. |
| Altın gün içi → `AMEX:GDXJ` | İstatistik gerçek (t −5,3) ama maliyet sonrası al-tut'a üstünlüğü t 1,4. Tek başına kenar değil. |
| XU030 vadeli baz sıçraması | Sinyal 18:10–18:15'te belli oluyor; "kapanışa 10 dakika kala" düzenine uymuyor. 2024–26 t 1,1. |
| VİOP ons altın (`BIST:XAUUSD1!`) için her şey | 2.621 testin hiçbiri çoklu test düzeltmesini geçmiyor; panelde 66 testte 0 sinyal. |

## Bakma listesi: denendi, çalışmıyor

| Grup | Çiftler | Sonuç |
|---|---|---|
| ABD ETF "yetişme" | GLD→GDX, GLD→GDXJ, GLD→SLV, SLV→SIL, GDX→GDXJ, SPY→IWM, QQQ→IWM, SPY↔QQQ, QQQ→SMH, XLK→SMH, SMH↔NVDA, SMH→SOXX, USO→XLE, XLE→XOP, TLT→XLU, CPER→COPX, FXI→KWEB, EEM→EWZ, SMH→EWT, SMH→EWY, IBIT→MSTR/COIN/ETHA, QQQ→ARKK | 234 testin medyanı net −30 bps; sağlam çıkan yok |
| Midas'taki bütün ETF'ler | 226 hedef × 240 öncü, 108.286 test | Çoklu test düzeltmesini geçen 0 |
| BIST çiftleri | AKBNK↔GARAN, GARAN↔YKBNK, THYAO↔PGSUS, TCELL↔TTKOM, EREGL↔KRDMD, FROTO↔TOASO, TRALT↔TRMET, KCHOL↔SAHOL | Yetişme yok; banka çiftlerinde 1 günlük dönüş −18…−21 bps |
| Gece sürücüleri | `CME_MINI:ES1!`, `CME_MINI:NQ1!`, `NASDAQ:TUR`, Brent, gece altını | Açılışta fiyatlanıyor; kapanışta giren bunu zaten yaşamış oluyor |
| Sektör emsalleri | Havayolu → THYAO/PGSUS, `NYSE:TKC` → TCELL, bira → AEFES, Avrupa savunma → ASELS, çelik → EREGL/KRDMD | Etki aynı gün içinde bitiyor |
| Altının öncüleri | Dolar, faiz, S&P, VIX, petrol, BTC, gümüş → altın | 240 testin %2,1'i anlamlı; şans beklentisi %4,6 |
| ABD sektörleri | 49 sektör, 1.320 test | 4'ü geçti, bir gün atlayınca kayboluyor |
| Kaldıraçlı altın ETF'leri | NUGT, JNUG, 2× GLD | Yılda ≈%7–20 aşınma |

## Gerekçe ve kanıt

**Kalıbın neden çalışmadığı.** Dört ayrı yerde aynı sonuç çıktı:
- Midas taramasında "hedef öncünün gerisinde kaldı" türünde 26.087 test var. Maliyet sonrası medyan −17 bps.
- Bugün 26 klasik ABD çiftini senin kuralınla ayrıca sınadım. "Hedef geride" koşulunu eklemek sonucu iyileştirmedi (medyan fark −8 bps), işlem sayısını onda bire indirdi.
- BIST'te aynı koşul 297 testte sağlam tek sonuç vermedi.
- Altın çalışmasında yetişme hipotezi reddedildi; ölçülen işaret tersti.

Yorumum: günlük kapanışta "geride kalmak" çoğu zaman bir nedene dayanıyor (hisseye özgü haber, akış). Fiyat farkı bedava bir açık değil.

**Yeni adayların nereden çıktığı.** Bugünkü yeniden hesapta 1.629 test önceden yazıldı; "öncü yükseldi → hedefi al" sürümü kontrol olarak konmuştu. BIST'te sağlam çıkan 32 satırın hepsi bu kontrol kolundandı. İkinci ve bağımsız bir kod bunları çürütmeye çalıştı:
- Tek tek hisse etkisi endeks momentumuna indirgendi (4 numara).
- KBE → AKBNK endeks etkisine indirgenmedi (2 numara).
- Ham getirinin yaklaşık yarısı TL sürüklenmesiydi; tablolardaki sayılar bu ayıklandıktan sonraki fazla getiridir.

**Maliyet.** BIST tarafında sayılar 10 bps gidiş-dönüş varsayımıyla ayakta. 44 bps'te fazla getiriden kalan: TUPRS ~0, KBE → AKBNK +20, RYSAS +10, hisse sepeti negatif. Endeks vadelisi ucuz olduğu için 4 numara bundan az etkilenir.

**Vadeli ve spot farkı.** Yeniden hesap spot fiyatla yapıldı. Vadelide uzun pozisyon TL faizini taşır; fazla getiri ölçüsü bunu kabaca karşılar ama birebir değil.

## Emin olunmayanlar ve doğrulama kapsamı

- **2, 3 ve 4 numara bu oturumda bulundu.** Taramadan seçildikleri için t değerleri iyimser. Sağlamlık testlerine ayrıca çoklu test düzeltmesi uygulanmadı.
- **"Hedef artıda ise al" süzgeci** tek kuralda (TUPRS) ve sonradan bakılarak bulundu. Diğer bulgularla aynı yönde ama tek başına kanıt değil.
- **Sinyal tam kapanış fiyatıyla hesaplandı.** Kapanışa 10 dakika kalaki değerle test yalnız QQQ için var.
- **Veri Yahoo günlük spot.** VİOP uzlaşma fiyatıyla yeniden hesap yapılmadı. Kapanış fiyatından dolum varsayıldı.
- **Midas:** kapanışta eşleşen emir türü listede bulunamadı; ETF'lerin Midas'ta bulunurluğu resmen doğrulanamadı.
- **Piyasa şu an olağanüstü oynak** (5 Kasım'da QQQ −%6,5, SMH −%11,2). Eşikler buna göre yüksek; geçmiş ortalamalar bu rejimi iyi temsil etmeyebilir.

Doğrulama kapsamı:
- Önceki sekiz kural bağımsız kodla yeniden hesaplandı (76 satır); 1.629 yeni test önceden yazılı aileyle koşuldu.
- Öne çıkan bulgular ikinci bir bağımsız kodla sınandı (8 test): 1'i çürütüldü, 7'si zayıfladı, hiçbiri "sağlam" çıkmadı.
- Rapora giren 19 iddia kaynak dosyalarla karşılaştırıldı: hepsinin ana sayısı doğru çıktı; 3 düzeltme yapıldı, 2 alt parça bulunamadığı için rapora alınmadı.
- Midas tarama özeti (108.286 test) dosyadan doğrudan hesaplandı.

## Son durum (10 Kasım kapanışı)

| Kural | Değer | Sinyal |
|---|---|---|
| TUPRS | Rafineri z ≈ +1,6 (9 Kasım ABD); TUPRS 10 Kasım −%0,3 | Öncü var, hedef ekside: süzgece göre pas |
| KBE → AKBNK | KBE 9 Kasım +%1,8 (z 1,7); AKBNK 10 Kasım −%0,35 | Kural sinyal veriyor (kâğıt) |
| RYGYO → RYSAS | RYGYO 10 Kasım +%1,1 | Yok |
| XU030 | 10 Kasım −%0,02 (9 Kasım'da +%2,2, sinyal vardı) | Yok |
| QQQ / SMH | 9 Kasım IBS 0,85 / 0,89 | Yok |

Değerler Yahoo verisinden benim hesabım; önceki günlük raporlardaki betiklerle karşılaştırılmadı.

## Kaynaklar

Hepsi bu depoda; dış kaynak kullanılmadı.
- `raporlar/2026-11-04_kapanis_1-3gun/` (PRATIK_LISTE, notlar, rehber) ve `raporlar/2026-11-02_viop_leadlag/RAPOR.md`
- `raporlar/2026-11-06_kazanc_stratejileri/` — dal `claude/borsa-kazanc-stratejileri-rfxr81`
- `raporlar/2026-11-07_midas_etf_1-3gun/` — dal `claude/fervent-ptolemy-1mgxu3` (`sonuclar/c0_leadlag.csv`, `c0_tablo.csv`)
- `raporlar/2026-11-07_xauusd_altin/` — dal `claude/laughing-dijkstra-e0ixur`
- `raporlar/2026-11-10_altin_panel_denetimi/` — dal `claude/gold-futures-strategy-review-6tvfdq`
- Bu klasör: `ek/` (beş çıkarım defteri, doğrulama notu) ve `ek/yeniden_hesap/` (kod, tablolar)

## Devam notu

1. Sonuç: "öncü yükseldi, hedef geride → al" kalıbı çalışmıyor; çalışan yön devam. Liste 7 kural, hepsi küçük.
2. Tek doğrulanmış öncü–hedef: ABD rafinerileri → TUPRS. Yeni adaylar: KBE → AKBNK, güçlü XU030 günü, RYGYO → RYSAS (kâğıtta).
3. Dosyalar: bu `RAPOR.md`; ham defterler `ek/E1…E5`; yeniden hesap `ek/yeniden_hesap/` (K1_OZET, K2_OZET, kod).
4. Açık işler: yeni adayların VİOP uzlaşma verisiyle ve kapanışa 10 dakika kalaki sinyalle sınanması; komisyon teyidi.
5. Önceki çalışmalar ayrı dallarda duruyor (Kaynaklar bölümü); ana dala birleştirilmedi.

_Maliyet: Seviye M · 10 ajan (9 sonnet: 5 çıkarım, 2 kod, 1 defter doğrulayıcı, 1 … ; 1 opus eleştirmen) · 2 dalga · bütçesini aşan ajan yok._
