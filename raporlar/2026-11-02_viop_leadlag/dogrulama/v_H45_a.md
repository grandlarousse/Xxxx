# v_H45_a — Bağımsız doğrulama: H45 (KCHOL açılış NAV ayrışması; ENKAI–TUR_{t-1}; ENKAI–USDTRY_{t-1})
Tarih: 02.11.2026. Veri sonu: 30.10.2026. Kod: `out/code_v_H45_a/` (ll.py import EDİLMEDİ; hizalama/temizlik `vlib.py`'de sıfırdan yazıldı). Çalıştırma sırası: 01_audit → 02_kchol → 03_enkai → 04_hourly → 05_bt → 06_extra → 07_bigmove (`nice -n 10 python3 -I`). Loglar: `log01..log07.txt`; sonuç tabloları `res_*.csv`.
t değerleri Newey-West(5). IS = 2014–2020, OOS = 2021–2026. Maliyet gidiş-dönüş.

## 0. Karar özeti
| Alt iddia | Yeniden üretildi mi | Gap-fade / bid-ask mekaniği mi? | Zamanlama | İşlenebilir mi (maliyet sonrası) | Yeni güven |
|---|---|---|---|---|---|
| (a) KCHOL açılış NAV ayrışması → KCHOL gün-içi | EVET, birebir: corr +0,096, t 4,92 (IS 4,95 / OOS 2,14); BT 8 bps IS +21,8 / OOS +6,7 (t 0,72); 2025 −15,7, 2026 −1,1 bps/işlem | HAYIR, yalnız kendi gap'i değil: KCHOL gap'i kontrolünde NAVgap +0,29 (t 3,9). XU030 gap'i kontrolünde de +0,31 (t 3,9). 300 rastgele Koç-dışı sepetin 300'ünü geçiyor | **SORUNLU.** Sinyal açılış müzayedesi fiyatlarından hesaplanıyor; backtest de girişi aynı müzayede fiyatından yapıyor. Bu dolum fiilen mümkün değil | **HAYIR.** 2023-11 sonrasında öngörülebilirliğin tamamı ilk 30 dakikada (o→07:30 corr +0,18). 07:30 girişiyle brüt −5,7 bps, 8 bps maliyetle −13,7 bps | İstatistik: ORTA. İşlem: ÇOK DÜŞÜK |
| (b) ENKAI: TUR_{t-1} → gün-içi (negatif) | EVET: corr −0,109, t −5,17 (IS −2,47 / OOS −5,14). Gap +0,12. Taramada FDR'yi geçen tek intra1 sonucu (6.546 test) | HAYIR: ENKAI gap'i kontrolünde TUR −0,093 (t −4,6). Gün-içi tepki gap tepkisinin ~2 katı ve ters yönde (net cc_t negatif). Bu açılış gap'inin geri dönüşü değil | Uygun. TUR kapanışı 20/21 UTC, müzayededen önce biliniyor | z>1, 8 bps: IS +1,6 (t 0,2), OOS +23,4 (t 1,8). 2021–22 çıkarılınca OOS +0,9. Büyük hareketlerde (z>2) OOS +132 bps (t 4,5, n=57) ama eşik sonradan seçildi. Etki piyasa genelinde (47/47 hisse pozitif). (c) ile aynı kanal | İstatistik: ORTA. İşlem: DÜŞÜK |
| (c) ENKAI: USDTRY_{t-1} → gün-içi (pozitif) | EVET, iddianın 12σ temizliğiyle birebir: t 3,30 (IS 4,21 / OOS 1,37). Temizlik olmadan t 4,30 (IS 5,22 / OOS 2,46). Fark tamamen 4 kriz gününden | HAYIR: ENKAI gap'i kontrolünde USD +0,196 (t 3,9) | Uygun, yalnızca 2011+ (Yahoo FX saat konvansiyonu 11.2010'da değişti) | z>1, 8 bps: IS +11,5 (t 1,6), OOS +50,1 (t 2,7, n=152). En büyük 10 gün OOS kârın %64'ü. 2021–22 hariç OOS +22,8 (t 1,2). 2023-11 sonrası corr −0,02 | İstatistik: ORTA−. İşlem: DÜŞÜK |

**Genel hüküm: DÜZELT.** İstatistiksel ilişkilerin üçü de bağımsız olarak üretildi ve hiçbiri açılış gap'inin mekanik geri dönüşüne (gap-fade / bid-ask) indirgenemiyor. Düzeltmeler:
- (a)'nın backtesti gerçekleştirilemeyecek bir dolum varsayıyor. Etki birkaç dakika içinde kapanıyor. "OOS'ta zayıf" değil, "işlenemez" denmeli.
- (b) ve (c) ayrı iki bulgu değil, aynı TL/Türkiye-riski kanalı. İkisi birlikte regresyona konunca IS'te USD, OOS'ta TUR baskın çıkıyor.
- (c)'nin rakamı (t 3,3) 4 kriz gününü silen 12σ temizliğine bağlı. Seçilen kurala göre t 3,3 ile 4,3 arasında değişiyor.
- TV ticker düzeltmesi: TUR NasdaqGM'de işlem görüyor. Doğru kod `NASDAQ:TUR`, `AMEX:TUR` değil.

## 1. Veri ve zamanlama denetimi (01_audit.py)
1. **Yahoo günlük açılış = açılış müzayedesi fiyatı.** Son 60 günde m5 06:55 UTC barıyla 1,00 eşleşiyor (KCHOL, ENKAI, 8 iştirak, XU030/XU100). İlk sürekli işlem fiyatıyla (07:00 barının açılışı) yalnızca %43–70 eşleşiyor. Endekslerde h1 ilk barının açılışı önceki kapanış (%2–3 eşleşme), bu yüzden endeks açılışı günlük veriden alındı.
   - Sonuç: (a)'nın sinyali (NAVgap − KCHOLgap) müzayede sonucu açıklandığında, yani ~07:00 UTC'de, biliniyor. Hedef olan intra = ln(c/o) ise girişi aynı müzayede fiyatından varsayıyor. Bu fiyattan dolum alınamaz.
   - (b) ve (c)'de sinyal müzayededen önce biliniyor. Spotta açılışta-piyasa (MOO) emriyle müzayedeye katılmak mümkün. VİOP pay vadelisi 06:30 UTC'den itibaren sürekli işlem görüyor.
2. **2014–2015 açılış kalitesi:** aynı gün o==c oranı KCHOL'da %16–17, iştiraklerde %5–24. Normal düzey 2016 sonrası %1–4. Bu yüzden "strict" varyant eklendi: o==c veya o==önceki c olan günler atıldı. Ayrıca 2016+ alt örneklemi test edildi. (a) bu temizlikte güçleniyor: 2016+ t 4,00; strict t 4,28; strict OOS t 2,33. Bozuk açılış verisinden kaynaklanan bir artefakt değil.
3. **Yahoo FX günlük kapanış saati (yeni bulgu, diğer ajanlar için önemli):** EURUSD=X ile FXE (ABD kapanışlı) korelasyonuna bakıldı.
   - 2005–2009: ldate D 'c' ile aynı gün korelasyon 0,94–0,97. Kapanış D günü sonu.
   - 2011+: ertesi gün korelasyonu 0,85–0,98. Kapanış ≈ 00:00 UTC D.
   - Geçiş ≈ 12.11.2010. TRY=X–TUR ve TRY=X–XU100'de de aynı kırılma var.
   - **ll.FX_FIX (tüm geçmişe 1 gün kaydırma) 2010-11 öncesinde yanlış ve o dönemde 1 günlük ileriye bakma (look-ahead) yaratıyor.** 2014+ gap/gün-içi testleri bundan etkilenmez. 2005/2010 başlangıçlı senkron/lead analizlerinde 2005–2010 dışlanmalı.
   - h1 kontrolü (2024+): TRY=X günlük c ile 00:00 UTC h1 fiyatı arasındaki medyan fark 2,8 bps; 15:00 UTC fiyatıyla 4,7 bps. Ayrım zayıf ama tutarlı.
4. **TUR hizası:** BIST t için TUR_{t-1} = ABD tarihi < t olan son kapanış / ABD tarihi < t_prev olan son kapanış. İddianın hizasıyla (yerel tarih ≤ t_prev) sonuç neredeyse aynı: t −5,03 vs −5,17.

## 2. (a) KCHOL açılış NAV ayrışması (02_kchol.py, 04_hourly.py, 05_bt.py, 06_extra.py)
Sinyal: sig_t = NAVgap_t − KCHOLgap_t. NAV ağırlıkları iddiadakiyle aynı (TUPRS .33, YKBNK .24, FROTO .20, ARCLK .07, TOASO .04, AYGAZ .03, TTRAK .03, OTKAR .02); eksik iştirak olursa ağırlıklar yeniden normalize edildi.

**Yeniden üretim**
- corr +0,096, t 4,92, n 3.177. IS +0,141 (t 4,95), OOS +0,059 (t 2,14).
- Yılların 13/13'ünde pozitif. 2025'te +0,015, 2026'da +0,104. Korelasyon 2026'da kaybolmamış.

**Mekanik ayrıştırma** (KCHOL intra ~ NAVgap + KCHOLgap)
- Tam dönem: NAVgap +0,293 (t 3,86), KCHOLgap −0,279 (t −4,90). Katsayılar eşit büyüklükte ve zıt işaretli, yani gerçek bir ayrışma yapısı var.
- OOS: NAVgap +0,23 (t 1,6).
- XU030 gap'i eklenince NAV'a özgü bileşen (NAVgap − X30gap) +0,31 (t 3,9) kalıyor. XU030'un kendisi ≈0.
- Kendi gap fade'i tek başına zayıf: corr +0,051 (t 2,4), OOS t 1,1. Backtesti (8 bps) IS +3,6 / OOS −6,4.
- Plasebo: Koç dışındaki VİOP hisselerinden aynı ağırlıklarla kurulan 300 rastgele 8'li sepet.
  - t_sig: medyan 2,87, %95 3,85, en yüksek 4,58. Gerçek NAV 4,92 (100. yüzdelik).
  - Kgap kontrollü sepet katsayısının t'si: rastgelede %95 2,71. Gerçek 3,86.
  - OOS t: rastgelede en yüksek 1,56. Gerçek 2,14.
- Genellik: "XU030gap − kendi gap → intra" 47 hissenin 13'ünde t>3. KCHOL 4. sırada. Yani piyasaya göre idiyosenkratik gap'in geri dönmesi genel bir olgu. KCHOL'da buna ek olarak NAV'a özgü bir bileşen var.
- Alternatif ağırlıklar:
  - Eşit ağırlık: t 4,14, OOS 1,51.
  - İlk-3 iştirak: t 5,08, OOS 2,16; BT8 OOS +17,2 (t 2,06).
  - Kayan regresyon ağırlığı (look-ahead yok): t 3,89, OOS 1,09; BT8 OOS +6,9.

**Zamanlama / alternatif giriş — kritik test** (2023-11-30..2026-10-30, h1)
- Aynı sinyalin farklı pencerelerle korelasyonu:
  - Müzayede → kapanış: +0,069 (t 1,92).
  - Müzayede → 07:30: **+0,182 (t 2,29)**.
  - 07:30 → kapanış: **−0,010 (t −0,22)**.
  - 08:30 → kapanış: +0,015.
- Regresyonla:
  - o→07:30: NAVgap +0,205 (t 1,9), Kgap −0,255 (t −2,3).
  - 07:30→c: NAVgap +0,15 (t 0,8), Kgap −0,005.
- Kendi-gap bileşeni (müzayede gürültüsü / bid-ask benzeri) ilk 30 dakikada tamamen geri dönüyor. NAV bileşeni de büyük ölçüde ilk 30 dakikada kapanıyor.
- m5 (60 gün): 07:05 girişinde corr +0,11; 07:15'te +0,02; 07:30'da +0,00.
- Backtest (z>0.5, aynı pozisyonlar):
  | Giriş | Brüt | 8 bps | 15 bps |
  |---|---|---|---|
  | Müzayede (o) | +7,1 | −0,9 | — |
  | 07:30 | −5,7 | −13,7 (t −1,3) | −20,7 |
  | 08:30 | +1,5 | −6,5 | — |
- 2023 öncesi için gün-içi veri yok. Ancak mekanizma "KCHOL müzayede fiyatı iştiraklerin müzayedesine göre bayat, dakikalar içinde yakalıyor" ise iddianın IS kârı da (+21,8 bps) erişilemez müzayede dolumuna dayanıyor.

**Backtest tekrarı** (müzayede girişi; iddia kurgusu z>0.5)
- 8 bps: IS +21,8 (t 3,6), OOS +6,7 (t 0,72). 15 bps: IS +14,8, OOS −0,3.
- Yıllar (8 bps): 2014 +30, 2015 +8, 2016 +44, 2017 −2, 2018 +30, 2019 +31, 2020 +18, 2021 +1, 2022 +30, 2023 +9, 2024 +18, 2025 −16, 2026 −1.
- Varyantlar:
  - z>1: OOS −13,3.
  - sign(sig): OOS +5,4.
  - XU030 hedge'li (+3 bps): OOS +5,5 (t 0,9).
  - Strict açılış: OOS +16,3 (t 1,2).
- Kaydırılmış-sinyal null (OOS, 8 bps): ortalama −9,6; %5–%95 aralığı [−25,9, +4,7].

**Sonuç (a):** İstatistik gerçek ve NAV'a özgü; mekanik değil. Ancak işlenemez: erişilebilir ilk girişlerde (07:05–07:30) edge yok. "2025–26'da kayboldu" ifadesi korelasyon için doğru değil (2026 corr 0,10), backtest kârı için doğru. Açık soru: BIST'in yayımladığı teorik/gösterge açılış fiyatlarıyla müzayede kapanmadan sinyal kurulup müzayedeye katılmak (ya da 06:30'dan beri işlem gören VİOP KCHOL vadelisi) bu etkiyi yakalayabilir mi? Veri yok, test edilemedi.

## 3. (b) ENKAI – TUR_{t-1} (03_enkai.py, 05_bt.py, 06_extra.py, 07_bigmove.py)

**Yeniden üretim**
- ENKAI intra: corr −0,109, t −5,17 (IS −2,47 / OOS −5,14). Yılların %85'inde negatif. 2024 −0,00, 2025 −0,04, 2026 −0,14.
- ENKAI gap: +0,121 (t 4,9).
- 2021–22 çıkarılınca: −0,077 (t −3,5).

**Mekanik mi?**
- ENKAI intra ~ TUR + Egap: TUR −0,093 (t −4,64), OOS −0,157 (t −4,9).
- Gap'i TUR'un açıkladığı kısım ve artık olarak ayırınca: açıklanan kısım −1,89 (t −5,2), artık −0,20. TUR'un gün-içi etkisi (−0,103) gap etkisinin (+0,055) ~2 katı. Net cc_t etkisi negatif.
- Bu bir gap-fade değil. Ayrıca müzayede gürültüsü TUR'dan bağımsız olduğu için bid-ask etkisi bu korelasyonu üretemez.
- ENKAI kendi cc_{t-1} ve XU100 cc_{t-1} kontrolünde: TUR −0,143 (t −4,4).

**Piyasa geneli mi?**
- XU100 intra: −0,062 (t −2,5; OOS −3,0). 47 hissenin 8'inde t<−3. ENKAI en uç (1/47).
- XU030 hedge'li ENKAI: −0,088 (t −4,7). ENKAI'ye özgü bir pay da var.

**(c) ile aynı kanal**
- ENKAI intra ~ TUR + USD: IS'te TUR +0,03, USD +0,22 (t 4,0); OOS'ta TUR −0,144 (t −4,0), USD +0,13 (t 1,3).
- Tüm kontrollerle tam dönem: TUR t −0,9, USD t 2,0.
- corr(TUR_{t-1}, USD_{t-1}): 2011–2020 arası −0,64…−0,78; 2023–24 −0,12…−0,16 (KKM/yönetilen kur dönemi).
- Mekanizma: ENKAI USD varlıklı bir şirket. Açılışta piyasa betasıyla fiyatlanıyor, gün içinde kur-hedge karakterine göre düzeliyor. Makul ama kanıtlanmadı.

**Backtest (−TUR, 8 bps)**
- z>1: IS +1,6 (t 0,2, n 483), OOS +23,4 (t 1,77, n 307). İddia +17,3 (t 1,3). Fark küçük ve hizadan kaynaklanıyor.
- 2021–22 hariç OOS +0,9. Kriz bağımlılığı z>1'de doğrulandı.
- Eşik ızgarası (IS / OOS, bps): z>0.5 −0,5 / +10; z>1 +1,6 / +23; z>1.5 +7,5 / +65; z>2 +28 (t 1,4) / +132 (t 4,5, n 57); z>2.5 +69 (t 2,3) / +171. Her iki dönemde de eşikle monoton artıyor.
- z>2 OOS yılları: 2021 +100, 2022 +146, 2023 +228, 2024 −7, 2025 +76, 2026 +180. Her yıl 6–13 işlem.
- Uyarılar:
  - Eşik sonradan seçildi.
  - z>2 günlerinde maliyetsiz OOS getirisi 47/47 hissede pozitif (ortalama +76 bps). Etki ENKAI'ye özgü değil, piyasa geneli.
  - XU030 (endeks vadelisi, 3 bps) z>2: OOS +65 (t 1,7), IS +7.
  - XU030 hedge'li ENKAI z>2 (11 bps): OOS +87 (t 3,75), IS +19 (t 1,0).
  - z>1 OOS'ta en büyük 10 gün kârın %49'u.
- 2023-11+ h1: TUR → ENKAI o→07:30 ≈ 0, 07:30→kapanış −0,067 (t −1,85). Etki varsa açılış dakikalarında değil, gün boyunca. Bu işlenebilirlik açısından olumlu.

## 4. (c) ENKAI – USDTRY_{t-1} (03_enkai.py, x_fxcmp.py, x_fxext.py, 04_hourly.py, 05_bt.py)

**Yeniden üretim**
- Benim hizam (P00(t)/P00(t_prev), ham): corr +0,106, t 4,30 (IS 5,22 / OOS 2,46).
- İddianın hizası ve 12σ temizliğiyle: t 3,30 / 4,21 / 1,37 — birebir.
- 12σ temizliğinin sildiği 4 gün (FX günü): 10.08.2018 (+%20,5), 20.12.2021 (KKM, −%20,9), 07.06.2023 (+%6), 19.03.2025 (+%3,5).

**Uç değer hassasiyeti**
- En büyük 4 |USD| günü atılınca: t 3,78 (OOS 1,7).
- 20 gün atılınca: t 5,06 (OOS 3,8).
- Spearman korelasyonu: tam 0,063, IS 0,074, OOS 0,052.
- Winsor %1: t 5,04.
- sign(USD): t 0,67. Etki hareketin büyüklüğünden geliyor, yönünden değil.

**Mekanik mi?**
- Egap kontrolünde USD +0,196 (t 3,9).
- USD→ENKAI gap ilişkisi IS'te −0,13: kur yükselince ENKAI piyasayla birlikte düşük açılıp gün içinde toparlanıyor. Ancak gap kontrolünde de etki kalıyor.
- XU030 hedge'li: +0,088 (t 4,3; OOS 3,0).
- 47 hisse: medyan t 1,78; ENKAI en yüksek (t 4,3).

**Taramadaki yeri:** holding taramasında ENKAI–TRY=X intra1 için padj 0,285 (FDR'yi geçmiyor, 6.546 test). Temizlenmemiş t 4,30 olsaydı sınırda kalırdı (p 1,7e-5).

**Son dönem**
- 2023-11+: corr −0,024.
- h1 ayrıştırması (2024+): seans içi kısmın (U_sess) ve seans sonrası kısmın (U_post) ikisi de ≈0 (n≈600). Hangi kısmın işe yaradığı bu dönemde test edilemiyor, çünkü etki yok.

**Backtest (z>1, 8 bps)**
- IS +11,5 (t 1,6, n 438), OOS +50,1 (t 2,7, n 152). İddia OOS +28,8 (t 1,5, n 188).
- 2021: +88 bps (62 işlem).
- En büyük 10 OOS günü toplamın %64'ü.
- 2021–22 hariç OOS +22,8 (t 1,2).
- z>2: IS +71, OOS +30 (t 0,7). z>2.5: OOS −12. Eşikte tutarsız.
- Kaydırılmış null OOS: ortalama −16, %5–%95 aralığı [−41, +8].

## 5. TradingView
- Spot hisseler: BIST:KCHOL, BIST:TUPRS, BIST:FROTO, BIST:YKBNK, BIST:ARCLK, BIST:TOASO, BIST:AYGAZ, BIST:OTKAR, BIST:TTRAK, BIST:ENKAI.
- Sürücüler: **NASDAQ:TUR** (Yahoo meta: NasdaqGM; iddiadaki AMEX:TUR düzeltilmeli), FX:USDTRY, FX:EURTRY.
- Hedge: BIST:XU030D1! (VİOP endeks vadelisi).
- VİOP pay vadelisi TV kodları doğrulanmadı ('?').

## 6. Sınırlamalar / açık sorular
- 2023 öncesinde gün-içi veri yok. (a)'nın "ilk dakikalarda kapanma" bulgusu yalnızca 2023-11 sonrasında (~725 gün) ve m5'te (60 gün) gösterildi.
- Kullanılabilecek bir yol: teorik açılış fiyatıyla müzayedeye katılmak ya da VİOP vadelisinin 06:30–07:00 fiyatı. Veri yok.
- (b)'nin z>2 kuralı ex-post seçildi ve tüm piyasaya yayılıyor. İleriye dönük doğrulama (2027) olmadan ORTA'ya yükseltilmemeli.
- Mekanizma ("açılış piyasa betasıyla fiyatlanır, kur-hedge karakteri gün içinde yansır") yalnız çıkarım; emir akışı/yabancı payı verisiyle test edilmedi.
- VİOP ENKAI ve KCHOL pay vadelilerinde gerçek spread ve derinlik ölçülmedi. 8–15 bps varsayımı kriz günlerinde (kârın yoğunlaştığı günler) iyimser olabilir.
