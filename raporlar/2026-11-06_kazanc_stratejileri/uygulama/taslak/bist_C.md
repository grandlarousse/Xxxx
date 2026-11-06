# BIST / VİOP swing planı C: "Önce risk, kanıt minimalisti" (başlangıç Pazartesi 9.11.2026)

Taslak, Cuma 06.11.2026 ~14:00 TSİ. Veriler 05.11.2026 kapanışına göre; 06.11 kapanışıyla yeniden hesaplanmalı. Yatırım tavsiyesi değildir. Kaldıraçlı VİOP pozisyonlarında teminatın tamamı ve teminat tamamlama yoluyla fazlası kaybedilebilir.

**Bu planın tezi tek cümle:** Doğrulamadan sonra mevcut rejimde TL engelini (net ~%31–36) güvenilir biçimde aşan bir yüksek getiri kuralı yok. Bu yüzden sermayenin büyük bölümü engel varlığında durur. Risk yalnız gerçekçi giriş gecikmesiyle (1 gün) ayakta kalan küçük kenarlara verilir. Boyut, kanıt birikip rejim dönünce büyür, önce değil.

**Kaynak kısaltmaları** (dosya + bölüm; doğrulama dosyaları raporlarla çeliştiğinde doğrulama esas alındı):

| Kısaltma | Dosya |
|---|---|
| [VB] | `dogrulama/v_bist.md` |
| [VC] | `dogrulama/v_capraz.md` |
| [VD] | `dogrulama/v_dalga.md` |
| [VP] | `dogrulama/v_profesyonel.md` |
| [BT] | `ajanlar/bist_test.md` |
| [BS] | `ajanlar/bist_swing_kenarlar.md` |
| [DB] | `ajanlar/dalga_bist.md` |
| [TM] | `ajanlar/tr_makro_engel.md` |
| [TP] | `ajanlar/tr_profesyonel.md` |
| [SE] | `ajanlar/seytan_taban_oranlar.md` |
| [KK] | `ajanlar/bist_kim_kazaniyor.md` |
| [HA] | `ajanlar/olay_halka_arz.md` |
| [HZ] | `uygulama/bist_hafta_hazirlik.md` |
| [TR] | `uygulama/tarama/bist_tarama_20261105.md` (`.csv`, `_viop.csv`) |
| [KO] | `raporlar/2026-10-28_viop_komite_raporu.md` |
| [PL] | `raporlar/2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md` |
| [C] | Bu taslağın kendi hesabı. İş Yatırım verisinin oturum önbelleği (05.11 kapanışı), Borsa İstanbul `viop_20261105.csv` ve SPK bültenleri 2026/55–78'in indirilmiş metinleri kullanıldı. Yöntem Ek A'da. |

Yazım anında `ajanlar/olay_bedelsiz.md`, `ajanlar/olay_akis_rejim.md` ve `dogrulama/v_olay.md` yoktu. Bu dosyalara dayanan kural yazılmadı. `hesaplar/olay_akis_rejim/cikti/` altındaki ara tablolar raporlanmamış ve doğrulanmamış; yalnız §2.8'deki "içeriden alım kolu yok" kararında yön bilgisi olarak anıldı.

---

## 0. Tek paragraf karar

- **Çekirdek:** Hesabın **%85'i** engel varlığında durur: büyük banka 32 günlük mevduat merdiveni, banka iştiraki PPF ve stopajı yazılı teyit edilirse kısa vadeli DİBS. Uydu kolları için ayrılan **%15** de kullanılana kadar PPF'de bekler.
- **Uydu kolları:** Altı kol var; yedinci kol (K7, endeks) yalnız rejim dönünce açılır. Dördü kanıtla ayakta kalan kenarlar:
  - SAHOL↔AKBNK oran dönüşü (VİOP)
  - KCHOL↔iştirak sepeti oran dönüşü (VİOP, yarım boy, ≥5 mn TL hesap)
  - Temettü hak kullanımı öncesi 5 gün (spot)
  - Likit hisselerde küçük boyutlu 52 hafta kırılımı (bugün yalnız "sonda" boyutunda)

  İkisi koşullu:
  - Özel durumlar (ZPAT/satma hakkı): yalnız KAP teyidiyle
  - TL carry: rezerv kapısı açılırsa, ≤%10 nominal
- **Bugün (06.11):** Rejim **KAPALI**. Yönlü endeks pozisyonu yok. Açık risk tavanı hesabın **%2,5**'i.
- **Pazartesi'nin büyük olasılıkla işlemi:** Yalnız çekirdeğin kurulması ve aracı kuruma yazılı soruların gönderilmesi. KCHOL↔sepet sinyali (z = +2,23) KCHOL bilançosu açıklanmadan alınmaz. En erken giriş 11.11.
- **Dürüst beklenti:** Bu rejimde uydu katmanından engelin üstüne merkezde yılda **+1,5 puan** bekleniyor. %80 aralığı yaklaşık **−2 ile +5 puan**. Rejim dönerse +4…+8 puan, ancak 2022 tipi bir yılda iki haneli. Toplam hesap getirisi net nominal TL'de ~%33–39 bandında.

---

## 1. Sermaye dağılımı kararı

### 1.1 Engel nedir? (vergi sonrası, birey)

| Kalem | Değer | Kaynak |
|---|---|---|
| Politika faizi / koridor | %36 / %34,5–39; sonraki PPK 10.12 (anket %35) | [VC] §1 #1; [HZ] §0 m.7 |
| TLREF | %35,85 (5.11) | [HZ] §4c |
| PPF medyanı, son 1 yıl | Brüt %45,5 → %17,5 stopajla net ≈ **%37,5** | [VB] §1 #13, §2.1 |
| 32 gün mevduat, banka ortalaması (6.11, 100 bin TL) | Brüt %39,52 → aylık yenilemeyle net bileşik ≈ **%37,9** (faiz sabitse) | [VC] §1 #4 |
| İleriye dönük 12 ay net engel | Faiz sabitse ~%36–38; anket patikasında ~%31–33; [TM] §1.3 tablosu %28–35 | [VC] §1 #4, §2 m.11; [TM] §1.3 |
| Reel karşılığı | ~%5–8 (ex-post reel politika faizi %4,8; ex-ante %9,8 iyimser) | [VC] §1 #3 |
| Vergi | BIST spot pay ve pay/endeks VİOP %0; F_USDTRY ve diğer VİOP %10; PPF ve ≤6 ay mevduat %17,5; doğrudan DİBS'te %0 yalnız 30.06.2026'ya kadar alınanlar için GİB metniyle teyitli, 31.12.2026 uzatması tek ikincil kaynakta | [VC] §1 #6, #7, #8; [VB] §1 #15 |

**Plan içinde engel tanımı:** Uydu kollarının ölçütü, aynı dönemde çekirdekte fiilen kazanılan vergi sonrası getiridir; XU100 değildir. Pratikte bu, kullanılan PPF'nin günlük fiyatıdır. Sabit bir %36 değil.

### 1.2 Çekirdek adayları: vergi sonrası karşılaştırma (5.11 fiyatlarıyla, 56 günlük pencere = Aralık vadesine kadar)

| Araç | 56 günde net getiri | Yıllık karşılık | Risk / not | Hüküm |
|---|---|---|---|---|
| 32 gün mevduat merdiveni (brüt %39,52, stopaj %17,5) | ≈ %5,06 | ≈ %37,9 bileşik | Banka kredi riski; vade bozulursa faiz kaybı; oran her yenilemede indirime göre düşer | **Evet, çekirdeğin en büyük parçası** |
| Banka iştiraki PPF (TLREF %35,85 günlük bileşik ≈ %43,1 brüt, ~%1 ücret, %17,5 stopaj) | ≈ %4,54 | ≈ %34–35 | Günlük likidite. Tasfiyedeki 15 PPF'nin 4'ü −%95…−%99,9 kaybetti; yalnız banka iştiraki fon ve ters repo teminatında grup ihracı olmayan fon seçilmeli | **Evet, likidite ve VİOP teminat kaynağı** [VB] §3 m.3; [VP] §3 m.2 |
| Kısa vadeli DİBS (2 yıllık gösterge bileşik ~%39,2; kısa uç Pazartesi ekrandan okunmalı) | ≈ %5,2 (2 yıllık; fiyat riski hariç) | ~%39 (stopaj %0 ise) | Stopajın %0 olduğu yazılı teyit edilmedikçe kullanılmaz. Süre (duration) riski var: ≤12 ay vadeli kâğıt seçilmeli. Takasbank'ta teminat olarak kullanılabilirliği teyit edilmeli | **Koşullu** [TM] §1.1; [VC] §1 #8 |
| XU030 nakit-taşıma (spot sepet/BYF uzun + F_XU0301226 kısa). Resmi uzlaşma 14.734 / spot 14.101 | %4,49 brüt, vergisiz; sepet/BYF ve komisyon maliyeti sonrası ≈ %4,25–4,35 | ≈ %29,3 basit / ~%33 bileşik, vergisiz | Bireyin vergi sonrası PPF/mevduat getirisini geçmiyor. Takip hatası, kısa vadeli teminatı, temettü | **Hayır (şimdilik)**. Ancak zımni basit yıllık faiz, net PPF basit oranını (≈ TLREF × 0,825 ≈ %29,6) **3 puan aşarsa** yeniden değerlendirilir. [VP] T12; [VC] §2 m.1 |
| Kısa F_USDTRY (carry) | Beklenen fazla getiri nominalin ~%8–12'si/yıl; stopaj %10; USD teminat ~%0 kazanır | — | Negatif çarpık. 2010–26 Sharpe −0,51, MaxDD −%90; tek ayda −%25…−%35. Prim daralıyor: 28 → 22 → 17 → ~13 puan | **Çekirdek değil**. Engel varlığı değil, satılmış kuyruk opsiyonu. Koşullu uydu K6, §2.6. [BS] §8.1; [TM] §4.3; [VC] #19 |

Not (vadeli fiyatlama): F_XU030'un TLREF'e göre "~%1 ucuz" olması **brüt** faize göredir. Teminatını %17,5 stopajlı PPF'de tutan birey için uzun vadeli + PPF, spot pay almakla kabaca aynı maliyettedir. Bu bir avantaj kaynağı değildir. Hesap: 14.734 / 14.101 − 1 = %4,49 (56 gün) karşı PPF net %4,54. [VP] T12; [KO] §2 hüküm 3.

### 1.3 Karar: çekirdeğin bileşimi (hesabın yüzdesi)

| Parça | Rejim KAPALI (bugün) | Koşul |
|---|---|---|
| Büyük banka 32 gün mevduat merdiveni (4 dilim, haftada bir dilim yenilenir) | %45 | En az 2 farklı büyük banka |
| Banka iştiraki PPF (en az 2 fon) | %25 + uydu kovası %15 = **%40** | PPF portföy raporunda ters repo karşı tarafı ve teminatı kontrol edilir; yönetim ücreti düşük olan seçilir |
| ≤12 ay vadeli DİBS | %15 | **Yalnız** aracı kurum/banka 9–30.11 arası alımlarda stopajın %0 olduğunu yazılı teyit ederse. Teyit yoksa bu %15 PPF'ye gider |
| Uydu kollarının kullandığı spot sermaye | 0–%15 (uydu kovasından) | §2, §5 limitleri |

Çekirdek kuralları:
1. Kredili işlem (spot kaldıraç) **hiç** kullanılmaz. Örtük maliyet ≈ %60 [VB] §1 #3.
2. VİOP teminatı mümkünse PPF payı veya DİBS ile verilir. Nakit teminatın getirisi aracı kurumdan **yazılı** öğrenilir. Nakit teminat TLREF'in %80'inden az kazanıyorsa VİOP kollarının boyutu yarıya iner [SE] §5.1 sıra 0. Gerekçe §2.1'deki teminat sürtünmesi hesabıdır.
3. Hesap toplamı haftada bir (Cuma kapanışı) çekirdek ve uydu olarak ikiye ayrılır. Uydu performansı, uydu kovasının PPF'de kalsaydı kazanacağı getiriye göre ölçülür.

### 1.4 Barbell oranları rejime göre

| | KAPALI (bugün) | GEÇİŞ | AÇIK |
|---|---|---|---|
| Çekirdek (engel varlığı) | ≥ %85 | ≥ %75 | ≥ %60 |
| Uydu spot sermayesi azami | %15 | %25 | %40 |
| VİOP brüt nominal azami | %35 | %50 | %70 |
| Toplam açık stop riski azami | %2,5 | %3,5 | %5,0 |
| Net endeks betası (β × nominal toplamı) azami | +%10 | +%25 | +%40 |

Rejim tanımları §3.1'de.

### 1.5 Örnek hesaplar: 1 mn / 5 mn / 20 mn TL (rejim KAPALI)

Fiyatlar 5.11 kapanışı ve uzlaşmaları. Pazartesi fiyatlarıyla yeniden hesaplanmalı. Kontrat = 100 pay (pay vadeli), 10 TL × endeks (XU030), 1.000 $ (USDTRY) [HZ] §5.

| Kalem | 1 mn TL | 5 mn TL | 20 mn TL |
|---|---|---|---|
| Mevduat merdiveni %45 | 450 bin (4 × 112,5 bin) | 2,25 mn | 9 mn |
| PPF %25 + uydu kovası %15 | 400 bin | 2 mn | 8 mn |
| DİBS %15 (teyitliyse) | 150 bin | 750 bin | 3 mn |
| K1 SAHOL↔AKBNK, bacak başına %7,5 nominal | 75 bin: SAHOL ~9, AKBNK ~11 kontrat | 375 bin: 44 / 56 | 1,5 mn: 176 / 223 |
| K1 teminat (aracı kurum %33,3 varsayımıyla) | ~50 bin (%5) | ~250 bin | ~1 mn |
| K2 KCHOL↔sepet, bacak %5 (yalnız ≥5 mn) | — (kontrat tamsayısı uymuyor) | KCHOL 12; sepet 5 × 50 bin: TUPRS 1–2, FROTO 7–8, TOASO 2, ARCLK 7, YKBNK 13–14 | KCHOL 49; TUPRS 6, FROTO 30, TOASO 9, ARCLK 28, YKBNK 54 |
| K3 temettü, olay başına %3,5 | 35 bin | 175 bin | 700 bin |
| K4 kırılım sondası, risk %0,25 → pozisyon %1,67 | risk 2,5 bin / pozisyon 16,7 bin | 12,5 bin / 83 bin | 50 bin / 333 bin |
| K4 rejim AÇIK, risk %0,5 → pozisyon %3,33 | 5 bin / 33 bin | 25 bin / 167 bin | 100 bin / 667 bin |
| K6 carry, kapı açılırsa ≤%10 nominal | 2 kontrat (104,6 bin) | 9 kontrat | 38 kontrat |
| K6 stres (+%30 kur) | −31 bin (−%3,1) | −141 bin | −596 bin |
| Aylık zarar limiti (−%2,5) | 25 bin | 125 bin | 500 bin |

Kapasite: 20 mn TL'de K1'in Aralık kontratları sığ kalabilir (SAHOL Aralık 5.11 işlem hacmi 22 mn TL). Bu durumda Kasım kontratı kullanılır ve vadeden önce devredilir (§2.1). K4'te pozisyon, hissenin 60 günlük medyan TL hacminin %2'sini aşamaz.

---

## 2. Uydu kolları

Ortak kurallar:
- Her sinyal kapanış verisiyle (18:10 sonrası) hesaplanır. İşlem **ertesi gün** yapılır. Bu, doğrulamadaki gerçekçi gecikme varsayımıdır [VB] §1 #25, §2.5.
- Spot girişler ve çıkışlar kapanış seansına (18:00–18:10) limitli emirle verilir. VİOP'ta limitli emir kullanılır; piyasa emri kullanılmaz [PL] §5.
- Kollarda piramit yok. Hiçbir test piramitli değil; yalnız K7 rejime göre iki dilimle açılır.

### 2.1 K1: SAHOL↔AKBNK oran dönüşü (VİOP pay vadelisi), 20 gün tutma

**Kanıt:**
- [BS] §9.1: L=60, |z|≥2, H=20. Aynı kapanışta giriş: 2010–18 +250 bps (t 3,75, isabet %76); 2019–26 +388 bps (t 3,65, isabet %66). En kötü işlem −%5,8 / −%8,3.
- [VB] §1 #25: Bir gün gecikmeyle **+160 / +310 bps (t 2,4 / 2,8)**. 20 bps maliyet sonrası ≈ +140 / +290 bps. Seçim yanlılığı var: çift önceki çalışmadan seçilmişti.
- [C] Kontrol: Örtüşen tüm |z|≥2 günlerinde 1 gün gecikmeli 20 günlük getiri 2010–18 +133 bps (n=244, isabet %65), 2019–26 +280 bps (n=216, %64). Yani "sinyal her gün değil, ilk kesişimde alınmalı" diye bir zorunluluk görünmüyor. Bu gözlemler örtüştüğü için t-istatistiği verilmedi.
- Komitenin uyarısı [KO] §1: SAHOL tasfiyedeki fonlarda en sık tutulan BIST30 payıydı. Bu paylar 03.11'de 3 ay satış yasaklı blok olarak devredildi [TP] §4.5c. Kilit ~03.02.2027'de açılıyor ve o tarih çevresi arz riski taşıyor.

**Sinyal (her işlem günü 18:15 sonrası):**
1. Düzeltilmiş kapanışlarla (İş Yatırım `HGDG_KAPANIS`) x_t = ln(SAHOL) − ln(AKBNK).
2. m = son 60 günün ortalaması, s = son 60 günün standart sapması (bugün dahil). z = (x_t − m) / s.
3. z ≥ +2: SAHOL pahalı → **F_SAHOL SAT, F_AKBNK AL**. z ≤ −2: tersi.
4. Aynı çiftte açık işlem varken yeni giriş yok.

**Giriş (t+1):**
- 09:30'da iki bacak için GÜN geçerli limitli emir girilir. Limit = t uzlaşması ± %0,5 (alınan bacak ≤ uzlaşma × 1,005, satılan bacak ≥ uzlaşma × 0,995).
- 17:50'de kontrol: İki bacak da dolduysa işlem yok. Tek bacak dolduysa eksik bacak 18:05'e kadar karşı fiyata yakın limitle tamamlanır. Tamamlanmazsa dolan bacak aynı gün kapatılır ve işlem "dolum hatası" diye kaydedilir.
- TL nominaller eşit tutulur (test log oranında 1:1).

**Çıkış:**
- **Zaman çıkışı:** Girişten sonraki 20. işlem günü kapanışında, z ne olursa olsun.
- **Felaket stopu:** Bir kapanışta çift P&L'i bacak nominalinin −%8'i veya altındaysa (2019–26'nın en kötü işlemi −%8,3) ertesi gün çıkılır. Bu stop testte yoktu; yalnız kuyruk sigortası.
- **Kurumsal olay:** Sabancı–Akbank pay yapısında değişiklik, birleşme, pay alım teklifi gibi bir KAP açıklaması gelirse ertesi gün çıkılır ve kol askıya alınır.
- **Vade:** Pay vadelisi **fiziki teslimatlı**. Kasım kontratları en geç **26.11 kapanışında** kapatılır veya takvim yayılımı emriyle Aralık'a devredilir. 20 gün kuralı 30.11'i aşacaksa giriş Aralık kontratıyla yapılır; şart, Aralık alış-satış makasının ≤ %0,3 olması. Aralık 5.11 işlem hacmi SAHOL 22 mn, AKBNK 118 mn TL [C, viop_20261105.csv].

**Boyut:**
- Bacak başına hesabın %7,5'i nominal (KAPALI). Felaket stopunda risk ≈ %0,6.
- Gap stresi: bacak nominali −%15 ≈ hesabın −%1,1'i.
- GEÇİŞ veya AÇIK rejimde boyut değişmez. Bu kol rejimden bağımsız ve büyümesi yalnız §7.4'teki istatistiğe bağlı.

**Beklenti (dürüst):**
- İşlem başına net +80…+180 bps. Backtest 140–290 bps'ye %40 çürüme ve seçim iskontosu uygulandı.
- İsabet %60–70; yılda ~5 işlem (2019–26'da 41 işlem / 7,8 yıl).
- Hesaba katkı merkezde **+0,4 puan/yıl**, aralık 0…+0,9.
- **Teminat sürtünmesi:** Teminat faizsiz nakitse ~0,6 puan/yıl kaybedilir (2 × %7,5 × %33 teminat × %40 piyasada kalma × %30 net faiz), ve katkı ~0'a iner. Bu kolun yaşaması teminat sorusuna bağlı (§6.3).
- **Komisyon duyarlılığı:** Bacak/yön başına 22 bps [PL] §5 ile gidiş-dönüş 88 bps olur ve kenarın yarısı gider. **Kural:** VİOP pay vadelisinde komisyon yön başına > 15 bps ise K1 kapalı.

**Bugün [C]:**
- z = **−0,72** (05.11). Sinyal yok.
- 05.11 penceresiyle yaklaşık tetikler, diğer bacak sabitken: z=+2 için SAHOL ≥ 90,85 veya AKBNK ≤ 62,94; z=−2 için SAHOL ≤ 82,52 veya AKBNK ≥ 69,30. 60 günlük pencere kaydığı için her akşam yeniden hesaplanır.
- Eski 1–3 günlük SAHOL/AKBNK sürümü [PL] §1 #2 bu kolla çakıştığı için **emekliye ayrılır**. Aynı çiftte iki ayrı sinyal çalıştırılmaz.

### 2.2 K2: KCHOL↔iştirak sepeti oran dönüşü (VİOP), yarım boy

**Kanıt:**
- [BS] §9.1: Sepet TUPRS, FROTO, TOASO, ARCLK, YKBNK, AYGAZ. L=60, |z|≥2, H=20. 2010–18 +212 bps (t 3,2), 2019–26 +244 bps (t 2,8).
- [VB] §1 #25: 1 gün gecikmeyle **+128 / +175 bps (t 2,1 / 2,1)**. 40 bps maliyetle ≈ +88 / +135 bps.
- [C]: Örtüşen tüm |z|≥2 günleri, gecikmeli, brüt: 2010–18 +62 bps (isabet %55), 2019–26 +128 bps (%57). Uzun süredir |z|≥2'de kalan "kalıcı" sinyaller karışık: 2010–18 −53 bps (n=35), 2019–26 +272 bps (n=26).
- Bu bir NAV iskontosu değil; holding fiyatının iştirak fiyatlarına göre kısa vadeli sapması [BS] §9.1 notu. 1–3 günlük ufukta "KCHOL NAV" çürütmede düşmüştü [PL] §2. Yani kenar yalnız 20 günlük ufukta var ve K1'den zayıf.

**Sinyal:**
- Sepet endeksi B_t = exp(Σ ortalama günlük log getirisi; 6 hisse, eşit ağırlık, günlük yeniden dengeli).
- x_t = ln(KCHOL) − ln(B_t). z, K1'deki gibi 60 günlük pencereyle hesaplanır.
- z ≥ +2 → F_KCHOL SAT + 5 sepet vadelisi AL (eşit TL). z ≤ −2 → tersi.
- AYGAZ'ın VİOP'u yok. Sinyal 6 hisseyle hesaplanır, işlem 5 bacakla yapılır. Bu takip hatası kabul edilir ve günlükte işaretlenir.

**Giriş/çıkış/vade:** K1 ile aynı: t+1 limitli emir, 17:50 kontrolü, 20. gün çıkışı, −%8 felaket stopu, 26.11 devir kuralı. Ek kural: KCHOL veya bir sepet hissesinin bilançosu ertesi işlem gününe kadar açıklanacaksa giriş ertelenir. Bu kural test edilmedi; yalnız gap riskini azaltmak için var.

**Boyut:**
- Yalnız ≥5 mn TL hesapta. 1 mn TL'de kontrat tamsayısı sepet ağırlıklarını bozuyor.
- KCHOL bacağı %5, sepet toplamı %5 (5 × %1). Felaket stopu riski ≈ %0,4.
- Komisyon yön başına > 8 bps ise kol kapalı. 6 bacakta gidiş-dönüş maliyeti kenarı yiyor.

**Beklenti:**
- İşlem başına net +40…+90 bps; isabet %55–60; yılda ~5 işlem.
- Katkı merkezde **+0,15 puan/yıl**, aralık −0,2…+0,4. Kanıtın en zayıf ayakta kalan kolu; 20 işlemden sonra §7.3'teki eşiği geçemezse ilk kapatılacak kol bu.

**Bugün [C]:**
- z = **+2,23** (05.11): KCHOL sepete göre pahalı. Sinyal 20.10'dan beri büyük ölçüde açık (kalıcı sinyal; kanıt karışık).
- KCHOL ve ARCLK 3Ç bilançosu en geç **9.11 akşamı** geliyor [HZ] §2. Pazartesi giriş yok.
- 10.11 kapanışında z ≥ 2 ise 11.11'de yarım boyla giriş. z < 2 ise bekle.

### 2.3 K3: Temettü hak kullanımı öncesi 5 gün (yalnız spot)

**Kanıt:**
- [BS] §5.3: 1.109 olay (2010–26, temettü/fiyat 1,02–1,15), piyasa düzeltmeli. [−5,−1] penceresinde ortalama +%1,2 (t 7,8), medyan +%0,8.
- [VB] §1 #26: **DOĞRU**. Haftalık kümelemeyle t 6,5. Ortalama 17 yılın hepsinde pozitif; medyan 2014 ve 2026'da negatif. Maliyet sonrası ≈ +%0,9.
- VİOP vadesi temettüyü önceden fiyatlıyor; kenar yalnız spotta var [PL] §2.

**Kural:**
- **Evren:** 60 günlük medyan hacme göre ilk 100 hisse (§4.1 dışlama listesi hariç). KAP'ta brüt temettünün kapanış fiyatına oranı ≥ %2 olan "Kâr Payı Dağıtım İşlemlerine İlişkin Bildirim".
- **Takvim:** Gün 0 = hak kullanım günü, temettüsüz ilk işlem günü. **Alış:** gün −6'nın kapanış seansında limitli emir (limit = gün −7 kapanışı × 1,04). **Satış:** gün −1'in kapanış seansında; hak kullanımına girilmez, temettü alınmaz.
- **Stop:** Pencere içinde kapanış girişin −%8 altındaysa ertesi kapanışta çıkılır.
- **Boyut:** Olay başına %3,5; eşzamanlı en çok 3 olay (%10,5). Aynı kümeden en çok 2 olay.
- **Piyasa riskini kaldırma (isteğe bağlı):** Toplam temettü pozisyonu ≥ 1 F_XU030 kontrat nominali / β olduğunda (≈147 bin TL / β) β × nominal kadar F_XU030 satılır. TUPRS, PETKM ve ASELS'te XU030 hedge'i işe yaramıyor [PL] §3. 1 mn TL hesapta hedge pratik değil.

**Beklenti:**
- Olay başına net +%0,5…+%0,7 (backtest +%0,9 / %30 iskonto). İsabet %55–65 (medyan +%0,8'den çıkarım; doğrudan ölçülmedi). Olay kuyruğu −%5…−%10.
- Olaylar Nisan–Haziran'da yoğun. Katkı merkezde **+0,6 puan/yıl**, aralık 0…+1,3.
- Kasım–Aralık'ta olay sayısı az. Bu kol Kasım'da büyük olasılıkla boş kalır; her Cuma KAP'tan önümüzdeki 30 günün hak kullanım tarihleri kontrol edilir.

### 2.4 K4: 52 hafta kırılımı + trend şablonu + %15 iz-stop (likit hisse, küçük boy)

**Kanıt:**
- [BT] §5.1: S2 (B52 + TT) iz %15: 2.073 işlem, ortalama net +%11,4, medyan −%2,9, isabet %45, kazanç/kayıp 3,3. Aynı gün rastgele likit hisseye göre **+%5,3** (ay-kümeli t 5,1); 17 yılın 15'inde pozitif.
- [VB] §1 #28: Yeniden üretildi. En iyi %5 işlem kârın %69,6'sı. En büyük kazançlar 2026'da −%93…−%98 çöken pump hisseleri (KTLEV, ODINE, HEDEF, PEKGY).
- [VB] §2.1: Düzeltilmiş risksiz faizle 2024–26 portföy medyanı engelin 2–8 puan **altında**.
- [BT] §5.2: Top75 evreninde S2 iz15 CAGR %35,4, MaxDD −%27. Gerçekçi dolumda MaxDD −%45.
- [BT] §5.1: S5 (S2 + XU100 > SMA200) S2'den iyi: +%5,7, t 5,4; [BT] §6'da CAGR +1…+6 puan ve MaxDD daha düşük.
- [C] kaba türetim: S2 ile S5 farkından, XU100 < SMA200 iken açılan ~218 işlemin rastgele hisseye göre fazlası ≈ +%1,9/işlem. Test değil, tablodan aritmetik.

**Neden "sonda" boyutu:** En iyi test edilmiş varyant (S5) bugün işlem açmıyor (XU100, SMA200'ün %16,5 altında). Rejim kapalıyken açılan kırılımların küçük bir rastgele hisse üstünlüğü var, ama mutlak getirisi bu rejimde büyük olasılıkla çekirdeğin altında. Bu yüzden KAPALI rejimde yalnız ölçüm amaçlı sonda açılır.

**Sinyal (t kapanışı):**
- B52: kapanış > önceki 252 işlem gününün en yüksek kapanışı.
- TT: P > SMA50 > SMA150 > SMA200; SMA200 > 21 gün önceki SMA200; P ≥ 1,25 × 52 hafta dibi; P ≥ 0,75 × 52 hafta zirvesi; RS yüzdeliği ≥ 80 (tarama [TR] (b) "rs" sütunu).
- Evren: §4.1. Ek olarak hisse §4.3'teki son 6 kümeden olmayacak.

**Giriş:**
- t+1'in kapanış seansında limitli alış; limit = t kapanışı × 1,06.
- t+1'de hisse tavana (≥ +%9,5) kilitliyse işlem atlanır (testteki "gerçekçi dolum" kuralı).

**Çıkış:**
- Her kapanışta iz-stop = girişten beri en yüksek kapanış × 0,85. Kapanış iz-stopun altındaysa ertesi günün kapanış seansında satış.
- Taban kilidinde emir her gün yenilenir.
- Azami tutma 120 işlem günü. Hedef fiyat yok; kazanan koşturulur.

**Boyut:**

| Rejim | İşlem başı risk | Pozisyon | Azami açık | Not |
|---|---|---|---|---|
| KAPALI | %0,25 | %1,67 | 2 | Sonda |
| GEÇİŞ | %0,5 | %3,33 | 5 | |
| AÇIK | %0,5 | %3,33 | 8 | |

- Piramit yok.
- Tek hissede azami %3,5 (3 ardışık taban ≈ −%27 → ≤ −%0,95).

**Beklenti:**
- **KAPALI:** Sonda katkısı ≈ 0 (−0,3…+0,3 puan). Amaç veri toplamak ve rejim dönüşünde ilk lideri tutmak.
- **AÇIK:** Rastgele hisseye göre işlem başı +%1…+%3 (backtest +%5,3 / ~%50 iskonto; pump isimleri dışlandığı için daha da düşük olabilir). Çekirdeğe göre işlem başı ≈ 0…+0,3R; isabet %40–45; işlemlerin çoğu küçük kayıp.
- Katkı kırılım kovası %26 doluyken −2…+6 puan, sağ kuyruklu. Kârın büyük bölümü birkaç işlemden gelir. 50 işlemlik bir dizinin toplamının negatif çıkma olasılığı gerçek bir kenarda bile ~%26 [SE] §3.5.

**Bugün [C]:**
- Şablonu tam geçen 4 hissenin hiçbiri B52 kapanışında değil. Tetik seviyeleri, düzeltilmiş kapanış ve önceki 252 günün zirvesi:
  - AHGAZ > **48,70** (son 46,00)
  - ENERY > **14,60** (13,80)
  - ENJSA > **127,00** (119,30; VİOP'lu)
  - RYSAS > **30,28** (26,68; likidite sırası teyit edilmedi)
- AHGAZ ve ENERY aynı alt tema (doğalgaz dağıtımı) ve risk açısından tek küme sayılır.

### 2.5 K5: Özel durumlar (ZPAT, satma hakkı, ayrılma hakkı), yalnız KAP teyidiyle

**Kanıt:**
- Bu alan **çalışılmadı** [VB] §3 m.4. Ağustos–Ekim bültenlerinde 13 ZPAT atfı var.
- **Karşı taraf riski:** Tera Holding, PEKGY ZPAT yükümlülüğünü yerine getirmedi (SPK 2026/64, 2026/71).
- Coval-Stafford tipi "zorunlu akışın karşısında durmak" mantığı [SE] §2.3 ile uyumlu, ama BIST'te test yok. Bu yüzden boyut küçük ve kural tamamen sözleşme metnine bağlı.

**Kural (bir işlemin açılması için hepsi gerekli):**
1. SPK bülteninde onaylı **pay alım teklifi bilgi formu** var. KAP'ta teklifin başlangıç ve bitiş tarihleri, fiyatı (TL veya "USD karşılığı, hangisi yüksekse"), aracı kurumu ve ödeme günü açıklanmış.
2. Teklif sahibi grup dışı, mali gücü belgelenmiş bir kuruluş (yabancı sanayi şirketi, banka vb.). Fon krizindeki grup içi teklifler (Tera/PEKGY tipi) **hariç**.
3. Teklif penceresi **fiilen başlamış**.
4. Spot fiyat ≤ teklif fiyatı × (1 − toplam maliyet − PPF net faizi × kalan gün/365 − %2 güvenlik payı).
5. Pozisyon teklif süresi içinde aracı kuruma verilen "pay alım teklifine katılım" talimatıyla teklif edilir. Teklif sonrası tutulmaz.

**Boyut:** Olay başına ≤ %5, toplam ≤ %10. Teklif iptali senaryosunda −%20 varsayımıyla olay riski ≤ %1.

**Beklenti:** Olay başına +%2…+%8 (spread − finansman). Yılda 0–3 olay. Katkı 0…+0,5 puan; merkez +0,1.

**Bugün [C]:**
- SPK 2026/59 (16.09) Heidelberg Materials'ın AKCNS için 1 TL nominal başına **260,25 TL veya 5,627434 $'ın TL karşılığı (hangisi yüksekse)** ZPAT bilgi formunu onayladı. Bülten metninden birebir okundu.
- AKCNS 5.11'de 184,5 TL. İş Yatırım verisinde halka açık piyasa değeri 24.09–07.10 arasında kademeli olarak 8,1 mlr TL'den 2,2 mlr TL'ye düştü. Bu, teklifin uygulanmış olmasıyla da MKK fiili dolaşım tanımının değişmesiyle de (SPK 2026/57) tutarlı.
- **Teklifin bugün açık olup olmadığı KAP'tan teyit edilmedi.** Teyit yoksa işlem yok. Fark büyük olasılıkla kapanmış bir teklifi ya da bir koşulu yansıtıyor.
- Diğer bulunanlar:
  - Atlantis Yatırım Holding için 104 TL gönüllü teklif (SPK 2026/56, 03.09): tarih ve durum teyitsiz.
  - PEKGY (Tera): yükümlülük yerine getirilmedi.
- **Bugün K5'te nitelikli olay yok.**

### 2.6 K6 (koşullu, varsayılan KAPALI): TL carry, kısa F_USDTRY, ≤%10 nominal

**Kanıt:**
- [VC] #19: 07/2023–10/2026 yıllık %20,8 USD, bağımsız yeniden hesapla doğru. Ama 2018 −%11,4, 2021 −%30,3; en kötü aylar −%24,1 / −%24,6. USD teminat Türk aracı kurumda ~%0 kazanır; stopaj %10.
- [TM] §4.3: Prim ~13 puana daraldı. Beklenti vergi öncesi ~%10–12/yıl USD.
- [SE] §3.5: Çöküşsüz bir sicil SR hakkında bilgi vermez. [VC] §2 m.8: Carry ile banka long'u aynı şokta birlikte kaybeder.

**Açılış kapısı (hepsi):**
1. TCMB swap hariç net rezervin son 2 haftalık değişimi ≥ −2 mlr $ ve seviye ≥ 20 mlr $.
2. Son haftada yabancı DİBS akımı ≥ −500 mn $.
3. CDS 5 yıl ≤ 275.
4. USDTRY'nin son 10 iş günündeki artış hızı, yıllıklandırılmış ≤ %30.

**Kapanış (herhangi biri; ertesi gün çıkış):**
- Swap hariç net rezerv < 15 mlr $ veya haftalık değişim ≤ −5 mlr $
- Yabancı DİBS akımı ≤ −1 mlr $/hafta
- CDS > 300
- 10 günlük hız > %35 (komite eşiği [KO] §4.2)
- Uzlaşma ≥ giriş × 1,04 (stop)
- Siyasi/hukuki şok: ilk seansta çık

**Boyut ve vade:**
- ≤ %10 nominal (1 mn TL'de 2 kontrat). +%30 şokta kayıp ≈ %3.
- Teminat PPF/DİBS ile verilir. Bir sonraki ayın kontratı kullanılır; vadeden 2 iş günü önce devredilir.

**Beklenti:**
- Kapı açıkken nominalin ~%8–11'i/yıl (vergi sonrası). Hesaba +0,3…+0,6 puan (yılın yarısı açık varsayımıyla).
- Şok yılında −%3 civarı.
- Merkez katkı +0,3 puan; aralık −3,0…+0,6.

**Bugün:**
- 30.10 haftasında swap hariç net rezerv 30,8'den 24,3 mlr $'a, yani −6,5 mlr $ düştü. Yabancı DİBS satışı −750 mn $ [VC] #18. Kapı koşulları 1 ve 2 sağlanmıyor → **KAPALI**.
- İlk yeniden değerlendirme 12.11 14:30 verisi. Kapı en erken iki olumlu haftalık veriden sonra (≥ 19.11) açılabilir.

### 2.7 K7 (yalnız rejim AÇIK/GEÇİŞ): endeks rejim kolu, uzun F_XU030 + PPF teminatı

**Kanıt:**
- [BT] §2: XU100 12 aylık TSMOM, 2010–26 rf üstü +6,8 puan, MaxDD al-tut ile aynı. Ama placebo yüzdeliği 0,86–0,88, yani anlamlı değil; 2024–26'da rf'nin −3…−6 puan altında.
- [BS] §4: 2019–26'da güçlü; **bugün kapalı** (12 ay +%3,3 karşı nakit +%37,3).
- SMA200 ve 50/200 kuralları endekste değer katmıyor [BT] §7. Bu yüzden SMA200 burada getiri kuralı değil, yalnız izin kapısı.

**Kural:**
1. GEÇİŞ'te ve en az 3 makro tetik açıkken (§3.1): %15 nominal uzun F_XU030.
2. AÇIK'ta (TSMOM12 açık ve XU100 > SMA200): %30 nominal.
3. Çıkış: ay sonunda TSMOM12 kapanırsa ya da XU100 SMA200'ün altında 3 ardışık kapanış yaparsa ertesi gün.
4. Girişler kapanışa yakın limitli emirle yapılır. Akşam seansı kullanılmaz.

**Beklenti:** AÇIK olduğu yıllarda nominalin +%4…+%7'si (rf üstü), yani %30 nominalde +1…+2 puan. Sahte sinyal yıllarında −2…−4 puan (2026 Nisan–Haziran örneği [BS] §4).

**Bugün:** KAPALI. Açılması için XU100'ün ~13.572'yi (SMA200, düşüyor; +%19,8) ve TSMOM12 için ~15.000'i [BS] §10 m.3 geçmesi gerekir.

### 2.8 Bu planda kullanılmayanlar (gerekçeli)

| Fikir | Neden yok | Kaynak |
|---|---|---|
| Eski 4 lead-lag kenarı: XU030 baz sıçraması, SAHOL/AKBNK 1–3 gün, Koza göreli momentum, ABD rafinerileri → TUPRS | Dördü de 2024–26'da zayıf (t 1,0–1,2). XU030 baz kenarı 18:10–18:15 arası ekran gerektiriyor; Koza'nın mekanizması belirsiz. **Hepsi kâğıt üzerinde izlemeye alınır; canlı işlem yok** | [PL] §1, §5 |
| 52 hafta zirvesine yakınlık sıralaması (H52 Q5) | 2022 çıkarılınca anlamsız (t 1,50 / 0,85) | [VB] §1 #24 |
| 12 ay küme RS rotasyonu (getiri kuralı olarak) | Yanlılıktan arındırılmış hali EW'ye göre +5±5 puan; 2024–26'da 456 yapılandırmanın hiçbiri rf'yi geçmedi. **Yalnız filtre olarak** kullanılıyor (§4.3) | [VD] §5 m.1; [DB] §0 m.4 |
| Sektör endeksi rotasyonu | 2024–26'da her yıl rf altında; endeksler doğrudan alınamıyor | [BT] §3 |
| Kesitsel 12-1 momentum, kısa vadeli dönüş ("düşeni al") | Başarısız; haftalık kaybedenler kaybetmeye devam ediyor | [BT] §4; [BS] §3.3 |
| Halka arz serisi sonrası alım | 52/53 düştü, medyan −%55; seri sonrası 21 günde medyan −%11 | [KK] §0 m.5; [HA] §0 |
| Halka arz katılımı | Pozitif (medyan +%45/arz), ama hesap başına yılda 10–27 bin TL. İsteğe bağlı, risk bütçesi dışında | [HA] §0, §3b |
| Bedelsiz öncesi koşu | Kendi testi var (öncesi +%2,8 / 20 gün, t 3,7) ama ayrı doğrulama ve `olay_bedelsiz` raporu yok. **Kâğıt üzerinde izleme.** Kaçınma kuralı canlı: bedelsiz hak kullanımından sonraki 5 günde ve %100'ün üzerindeki bedelsizlerde 60 gün içinde hiçbir kolda yeni alış yok (−%2,0 / 5 gün, t −3,2; 60 gün medyan −%5,3) | [BS] §5.1 |
| İçeriden alım taklidi | Literatür +%6,6/yıl brüt, 2008–19 [VB] #18. Kendi ara tablosu (doğrulanmamış, `hesaplar/olay_akis_rejim/cikti/A_kontrol.md`): KAP "alış" bildirimlerinden sonra 60 günlük kontrol düzeltmeli getiri −%3,35 (t −1,73, n=233). Kanıt çelişkili → kol yok | [BS] §5.5 |
| PEAD | Literatür, doğrulanamadı | [VB] #21 |
| Opsiyon satışı / straddle | Bu açının kanıt eşiğini geçen bir test yok; derinlik sığ | [BS] §8.3; [KO] §4.1 |
| MSCI ve kredili işlem kaynaklı zorunlu akış "işlemi" | Takvim belli, ama BIST'te büyüklük ve yön testi yok (n=1). Yalnız risk kuralı olarak kullanılıyor (§3.3) | [VC] §2 m.7; [VB] §3 m.5 |

---

## 3. Rejim anahtarı, bugünkü okuma ve takvim planı

### 3.1 Eşikler (her Cuma kapanışında; TSMOM12 ay sonu kapanışında)

| Kod | Gösterge | Eşik (1 = açık) | 05.11 değeri | Durum |
|---|---|---|---|---|
| T1 | XU100 kapanış > SMA200 | evet | 11.333 karşı 13.572 (−%16,5) | 0 |
| T2 | XU100 12 ay getirisi > aynı dönem TL nakit getirisi (TSMOM12, ay sonu) | evet | +%3,8 karşı ~+%37 | 0 |
| M1 | Swap hariç net rezerv 3 hafta üst üste artış | evet | 30,8 → 24,3 mlr $ (düşüş) | 0 |
| M2 | Aylık TÜFE < %2,0 | evet | Ekim %2,58 | 0 |
| M3 | Yabancı hisse net alımı 2 hafta üst üste ve toplam > +200 mn $ | evet | −66,3 mn $; 6 hafta −334,5 mn $ | 0 |
| M4 | CDS 5 yıl < 230 | evet | ~248 | 0 |

Makro tetikler [TM] §5.1'den alındı. 4 tarihi örnekten türetilmiş öznel eşikler; hayatta kalan yanlılığı ve rejim bağımlılığı yüksek [TM] §5.3. Rejim filtresi bir getiri kaynağı değil, risk kontrolü [BT] §6.

**Durumlar:**
- **KAPALI:** T1 = 0 ve T2 = 0, ve makro tetiklerin < 3'ü açık. **Bugünkü durum.**
- **GEÇİŞ:** T1 = 1, ya da makro tetiklerin ≥ 3'ü açık (M1 zorunlu).
- **AÇIK:** T1 = 1 ve T2 = 1.
- **KRİZ kesicisi** (her durumun üstünde): Aşağıdakilerden biri olursa 5 işlem günü yeni giriş yok, K6 kapanır, mevcut stoplar işler.
  - XU100 bir haftada ≥ %8 düşer
  - USDTRY 10 günlük hızı > %35 (yıllıklandırılmış)
  - CDS > 300

**Bugün ne diyor:** KAPALI, 6 göstergenin 0'ı açık. İzinler:
- Çekirdek ≥ %85; açık risk ≤ %2,5.
- K1, K2, K3 ve K5 serbest. Bu kollar rejimden bağımsız ya da piyasa düzeltmeli.
- K4 yalnız sonda; K6 kapıya bağlı (şu an kapalı); K7 kapalı.
- En erken değişebilecek göstergeler: M1 ve M3 (12.11 14:30), M2 (3.12 Kasım TÜFE), T2 (30.11 ay sonu; matematiksel olarak çok uzak).

### 3.2 9–13 Kasım, gün gün (saatler TSİ)

| Gün | Olay [HZ] §1a | Yapılacak (karar kapanışta veya önceden girilmiş emirle) | Yapılmayacak |
|---|---|---|---|
| **Cuma 6.11, 18:20 sonrası** | TUPRS, ENKAI, ULKER, BRSAN bilançoları | (1) `kod/bist_tarama.py` 06.11 kapanışıyla çalıştırılır. (2) `viop_20261106.csv` resmi bülteni indirilir; XU030 baz ve USDTRY zımni oranı uzlaşmayla yeniden hesaplanır (tarama 14.605 kullanmıştı ve yanlıştı [VP] T12). (3) K1/K2 z-skorları ve K4 tetik seviyeleri güncellenir. (4) KAP: önümüzdeki 30 günün temettü hak kullanım tarihleri ve açık ZPAT'lar. (5) Aracı kuruma §6.3 soruları e-postayla gider | — |
| **Pzt 9.11** (konsolide 3Ç son gün; KCHOL, BIMAS, PGSUS, TCELL, SOKM, DOAS, AKSEN, ALARK, ARCLK ve diğerleri akşam) | Hazine tahvil ihaleleri | **Sabah:** Çekirdek kurulur. Mevduat 1. dilimi (%11,25), PPF %40, DİBS yalnız stopaj teyidiyle. **Kapanış (18:15):** z-skorları ve K4 tetikleri. K1'de |z| ≥ 2 olursa Salı girişi planlanır. K4'te tetik gelirse Salı kapanış seansına sonda emri. | Bilançosu akşam gelecek hisselerde yeni pozisyon yok. K2 girişi yok (KCHOL, ARCLK). Bilanço gecesi pozisyon taşıma kararı tahminle verilmez |
| **Sal 10.11** | 10:00 sanayi üretimi; 16:30 ABD TÜFE | Açılış gap'lerine dokunulmaz. **Kapanış:** K2 için temiz z (bilanço sonrası). z ≥ 2 ise Çarşamba yarım boy giriş emri hazırlanır. Mevduat 2. dilimi | Sabah bilanço tepkisi "kovalanmaz" (kısa vadeli devam ve dönüş kanıtı aleyhte [BS] §3.3) |
| **Çar 11.11** | ABD tatili (hisse açık); **12.11 01:00 MSCI Kasım duyurusu** | K2 girişi (koşul sağlandıysa): 09:30 limitli emirler, 17:50 kontrol. Kapanış rutini | — |
| **Per 12.11** | 10:30 TCMB Enflasyon Raporu; **14:30 rezerv + haftalık menkul kıymet**; akşam SPK bülteni olası | **Sabah, MSCI sonucu:** Türkiye'den çıkarılan veya ağırlığı düşen hisseler 30.11 kapanışına kadar K3 ve K4 evreninden çıkarılır (artışlar dondurulmuş, azaltmalar uygulanıyor [VC] #17). **14:30 sonrası:** M1, M3 ve K6 kapısı güncellenir (1. olumlu hafta sayılır mı?). Mevduat 3. dilimi | MSCI akışına karşı işlem yok (test yok) |
| **Cum 13.11** | 10:00 ödemeler dengesi; **seans sonunda kredili işlem esnekliği (%20 → %35) bitiyor**, uzatılmazsa | SPK bülteni (12–13.11) okunur. **Uzatılmazsa** 16–20.11 arası: yeni K4 sondası yok; ilk 100 dışı hisselerde hiçbir kolda alış yok; satış baskısında "dipten alım" yapılmaz. **Uzatılırsa** değişiklik yok. 18:30 haftalık gözden geçirme (§7.5); mevduat 4. dilimi | Zorla satış dalgasına "likidite sağlayıcı" olarak girilmez; BIST'te kısa vadeli dönüş kanıtı yok [BT] §4 |

### 3.3 Kasım sonuna kadar

| Tarih | Olay | Kural |
|---|---|---|
| 16–20.11 | Esneklik uzatılmadıysa olası teminat tamamlama satışları | §3.2'deki kısıtlar sürer. K1/K2 normal (VİOP-47, likit) |
| 19.11 | Bankalar konsolide 3Ç son gün [HZ] §1b | Bilançosu ertesi güne kadar gelecek bacakta yeni K1/K2 girişi yok |
| 19.11 ve 26.11 Perşembe 14:30 | Rezerv / akım | M1, M3 ve K6 kapısı. Kapı en erken 19.11'de açılabilir |
| **26.11 kapanış** | Kasım pay vadelilerinin son güvenli günü (fiziki teslimat 30.11) | Açık K1/K2 bacakları Aralık'a devredilir ya da kapatılır. Vade günü pozisyon yok |
| 27.11 | TCMB Finansal İstikrar Raporu | Bilgi |
| **30.11** | VİOP Kasım vadesi; MSCI değişiklikleri kapanışta; TSMOM12 ay sonu | T2 hesaplanır. Aylık rapor (§7.5). MSCI çıkarma listesi 01.12'de evrene geri döner |

**Aralık ve sonrası** (plan sürer; takvim [HZ] §1c, [TP] §4.5):
- 3.12 Kasım TÜFE (M2)
- 10.12 PPK: çekirdek faizini etkiler
- 31.12 XU030 ve pay vadelileri Aralık vadesi. **31.12 mevduat/PPF %17,5 stopaj ve DİBS stopaj düzenlemelerinin süresi doluyor** [VC] §2 m.6: 2027 çekirdek araçları Aralık'ın son haftasında yeniden seçilir.
- 31.01.2027 fon yoğunlaşma uyumu: BIST30 dışı fon payı yüksek hisseler dışlamada kalır.
- ~03.02.2027 BIST30 blok kilidi açılıyor: K1'de SAHOL arzı izlenir.
- ~17.03.2027 tasfiye azami süresi.

---

## 4. Evren, dışlama listesi, kümeler, güncel adaylar

### 4.1 Evren

- **K1/K2:** Yalnız ilgili VİOP kontratları.
- **K3:** Tarama evreni [TR] (VİOP-47 ∪ BIST100 = 100 hisse) içinde 60 günlük medyan TL hacme göre ilk 100.
- **K4:** Aynı evrende **ilk 75** (test evreni top75 MaxDD −%27 [BT] §5.2), ≥ 252 işlem günü geçmişi olanlar.
- **Hepsinde:** Fiyat verisi düzeltmeli kapanış (İş Yatırım).

[C] 60 günlük medyan hacim sırası (248 hisselik önbellek evreni): ENERY 36, ENJSA 48, AHGAZ 63 → K4'e uygun. ISDMR 106 ve GLYHO 136 → K4 dışında. RYSAS hesaplanamadı; Pazartesi tarama verisiyle kontrol edilmeli.

### 4.2 Dışlama listesi (hiçbir kolda uzun pozisyon yok; açılırsa ertesi gün kapatılır)

1. **SPK suç duyurulu 13 hisse:** KTLEV, GUNDG, DSTKF, OZATD, TRHOL, ODINE, VSNMD, IEYHO, ALKLC, ANELE, PASEU, SELEC, MANAS [VP] T10.
2. **Fon payı / fiili dolaşım > %20:**
   - [VP] T6: PASEU, KTLEV, ANELE, TEHOL, DSTKF, IEYHO, TMPOL, ODINE, ISVEA, MAGEN, BALSU, ISKPL, DAGI, INFO
   - [TP] §4.5: TRHOL, OZATD, GUNDG, PEKGY, SKYLP, SELEC, KARCL, GLRMK
3. **Tera / Pusula / Hedef grubu:** TERA, TEHOL, TRHOL, HEDEF, HDFGS, DSTKF; ayrıca BIGEN [TP] §4.4, §6.
4. Borsa'nın **VBTS tedbiri** altındaki hisseler (açığa satış/kredili yasağı, brüt takas, tek fiyat). Liste her Cuma KAP/aracı kurumdan okunur [HZ] §3.
5. **Halka arzdan bu yana < 252 işlem günü** geçmiş hisseler [HA] §0.
6. Son 60 işlem gününde **≥ 3 kez ±%9,5'te kapanan** hisseler (kilit/pump vekili; [VB] #27'deki taban serileri bu filtreye takılır).
7. **MSCI Kasım duyurusunda** çıkarılan veya ağırlığı azaltılan hisseler, 30.11 kapanışına kadar.
8. Bedelsiz hak kullanımı son 5 işlem gününde olmuş hisseler. %100'ün üzerindeki bedelsizlerde 60 gün [BS] §5.1.
9. VİOP'ta işlem dışı tutulanlar (teminat %100 ve kilit riski): ASTOR, HALKB, VESTL [VB] #16. Ayrıca kilit riski yüksek olarak işaretlenen GUBRF, TKFEN, SASA, BRSAN, HEKTS [PL] §3. Bu hisseler K4'te spot olarak uygun olabilir; VİOP pozisyonu açılmaz.

### 4.3 Küme tanımları (risk sayımı için) [DB] §1, §5

| Blok (risk sayımında tek küme) | Kümeler ve VİOP'lu ana üyeler |
|---|---|
| **Blok 1: büyük finans ve beta** (günlük korelasyon 0,70–0,79) | BANKA (AKBNK, GARAN, YKBNK, ISCTR, VAKBN, HALKB, TSKB), HOLDİNG (KCHOL, SAHOL, DOHOL, ALARK, TKFEN; AGHOL, GLYHO), HAVACILIK (THYAO, PGSUS, TAVHL), TELEKOM (TCELL, TTKOM), GYO (EKGYO) |
| **Blok 2: küçük-orta tema** | ELK_EKİPMAN (ASTOR…), YENİLENEBİLİR, TEKNOLOJİ, ELK_ÜRETİM (AKSEN, ENJSA, ODAS) |
| **Blok 3: sanayi** | ÇİMENTO (CIMSA, OYAKC), OTO_YAN, KİMYA (SASA), CAM (SISE), BEYAZ_EŞYA (ARCLK, VESTL), SAĞLIK |
| **Ayrıştırıcılar** (her biri ayrı küme) | RAFİNERİ (TUPRS, PETKM; AYGAZ): bankayla fazla getiri korelasyonu −0,42. SAVUNMA (ASELS): bankayla −0,35. KOZA_ALTIN (TRALT, TRMET): ~0 |
| Diğer (ayrı küme) | ÇELİK (EREGL, KRDMD; ISDMR), PERAKENDE (BIMAS, MGROS, SOKM), OTOMOTİV (FROTO, TOASO, DOAS), GIDA (ULKER, AEFES, CCOLA), GÜBRE (GUBRF, HEKTS) |
| Bu planın eklediği | DOĞALGAZ DAĞITIM (AHGAZ, ENERY): kümelerde tanımlı değil; tek küme sayılır |

K1 ve K2 piyasa-nötr oldukları için Blok 1 kümesi sayımına girmez. Ama ikisi aynı anda açıksa Blok 1'in yönlü pozisyon hakkı (K4 ve K3) yarıya iner, çünkü bacaklar aynı haber riskini taşıyor.

**Küme filtresi (12 ay RS, [DB] §5; 30.11'de yenilenir):**
- İlk 3: **RAFİNERİ, HOLDİNG, KOZA_ALTIN**. Filtreli kural (B) nakitte.
- 126 gün RS kırılımı: **BANKA, HAVACILIK**.
- **Son 6** (K4'te yeni giriş yok): CAM_SERAMİK, BEYAZ_EŞYA, KİMYA, GÜBRE, YENİLENEBİLİR, OTO_YAN.

Not: Düşen piyasada RS liderliği büyük ölçüde düşük beta demek. RAFİNERİ'nin betası 0,55; klasik bir momentum dalgası değil [DB] §5.

### 4.4 Güncel adaylar: nitelikli olan ve bekleyen (05.11 kapanışı)

| Kol | Nitelikli (giriş koşulu sağlanmış) | Bekleyen (tetik / koşul) |
|---|---|---|
| K1 SAHOL↔AKBNK | — (z −0,72) | |z| ≥ 2. Yaklaşık tetikler §2.1 |
| K2 KCHOL↔sepet | **Sinyal var** (z +2,23); bilanço nedeniyle ertelendi | 10.11 kapanışında z ≥ 2 → 11.11 giriş (≥5 mn TL hesap, yarım boy) |
| K3 temettü | — (KAP kontrolü bekliyor) | Hak kullanımı ≤ 30 gün içinde, temettü verimi ≥ %2, ilk 100 hissede |
| K4 kırılım (sonda) | — | ENJSA > 127,00; ENERY > 14,60; AHGAZ > 48,70 (ENERY ve AHGAZ aynı küme, en çok 1 sonda); RYSAS > 30,28 (likidite teyidiyle). Şablonun 4/5'inde olup fiyatı 50 GHO altında kalanlar (izleme): TUPRS (50 GHO 381,0; zirve 409,9), BIMAS (402,1; 433,75), KRDMD (43,18; 47,48), AYGAZ (297,8; 337,0). Hiçbiri yakın değil |
| K5 özel durum | — | AKCNS ZPAT'ın KAP durumu; yeni SPK bülteni onayları |
| K6 carry | — (kapı kapalı) | 12.11 ve 19.11 rezerv verileri |
| K7 endeks | — | T1 / makro tetikler |

---

## 5. Risk limitleri

| Limit | KAPALI | GEÇİŞ | AÇIK | Gerekçe |
|---|---|---|---|---|
| İşlem başı risk (stopta) | K4 %0,25; K1 ~%0,6; K2 ~%0,4; K3 olay ~%0,28 | K4 %0,5 | K4 %0,5 | Gerçek SR tahminin yarısıysa tam Kelly büyümeyi sıfırlar; tıraşlanmış SR'nin ≤ ¼ Kelly'si [SE] §3.3, §5.3 m.3 |
| Tek hisse spot azami | %3,5 | %3,5 | %3,5 | 3 ardışık taban (−%27) ≤ hesabın %1'i |
| Küme başına açık risk | %1,0 | %1,25 | %1,5 | Küme tek bahis; ρ 0,6–0,8'lik 5 pozisyon SR'yi yalnız %9–21 artırır [SE] §3.6 |
| Blok 1 toplamı (yönlü) | %1,0 | %1,5 | %2,0 | Banka, holding, havacılık korelasyonu 0,77–0,79 [DB] §5 |
| Toplam açık stop riski | **%2,5** | %3,5 | %5,0 | |
| Stres kaybı tavanı (tüm pozisyonlar) | **%6** | %8 | %10 | Senaryo: hisseler 2 taban (−%19), USDTRY +%30, çift spreadleri −%15. Her Cuma hesaplanır; tavan aşılırsa en düşük öncelikli koldan küçültülür |
| VİOP brüt nominal | %35 | %50 | %70 | |
| VİOP başlangıç teminatı kullanımı | ≤ %15 | ≤ %20 | ≤ %25 | Serbest teminat her zaman ≥ 2 × kullanılan başlangıç teminatı. 2 limit hareketinde zorla kapatılmamak için |
| Net endeks betası | +%10 | +%25 | +%40 | |
| Aylık zarar limiti (uydu, çekirdeğe göre) | **−%2,5** → ay sonuna kadar yeni giriş yok | aynı | aynı | |
| Uydu tepe-dip düşüşü (çekirdeğe göre, birikimli) | −%4 → tüm uydu boyutları yarıya, 3 ay. −%6 → tüm uydu kapanır, 3 ay kâğıt üzerinde | aynı | aynı | [SE] §5.2 m.8'in küçük ölçekli uyarlaması |
| Kredili işlem / opsiyon satışı | Yok | Yok | Yok | [VB] #3; [BS] §8.3 |

**Bütçe bağlayınca öncelik:** K1 > K3 > K5 > K2 > K4 > K6. K7 yalnız AÇIK/GEÇİŞ'te ve en sonda.

**Limit kilidi ve boşluk riski:**
- Pay ve VİOP günlük limiti ±%10 [HZ] §5. Taban serisinde stop emri dolmaz; 2026'da ODINE 29 ardışık taban yaptı [VB] #27.
- Bu yüzden koruma **boyutla** yapılır, stopla değil: tek hisse ≤ %3,5, dışlama listesi, likidite filtresi.
- Pay vadelisinde akşam seansı yok [HZ] §5. Gece ve hafta sonu boşluğu kapanış riskinin bir parçası; rutin gece hedge'i yapılmaz, çünkü 1–3 günlük riskin yalnız ~%11'i gecede oluşuyor [PL] §3.

---

## 6. Uygulama ve maliyetler

### 6.1 Emir tipleri ve saatler [HZ] §5

| İş | Seans | Emir | Ne zaman girilir |
|---|---|---|---|
| Spot giriş/çıkış (K3, K4, K5) | Kapanış seansı 18:00–18:10 | Limitli. Giriş limiti t kapanışı × 1,04 (K3) veya × 1,06 (K4); çıkışta limit t kapanışı × 0,94 (taban kilidinde ertesi gün yenilenir) | Aracı kurum kapanış seansı için önceden emir kabul ediyorsa sabah girilir. Etmiyorsa 17:50–17:59 arası, 10 dakikalık tek ekran penceresi (aracı kurumla teyit) |
| VİOP çift girişi (K1, K2) | 09:30–18:10 | GÜN geçerli limitli, uzlaşma ± %0,5 | 09:30'da girilir. 17:50 kontrolü yalnız tek bacak dolduysa eylem gerektirir |
| VİOP zaman çıkışı ve devir | Aynı | Limitli. Devir için takvim yayılımı (Kasım/Aralık) emri, varsa | Çıkış günü 09:30 |
| K6/K7 | Normal seans | Limitli, kapanışa yakın | 17:30–18:00 |
| Şartlı/stop emirleri | — | Kullanılmaz. Kurallar kapanış bazlı; gün içi stop testteki dağılımı değiştirir | — |
| Piyasa emri | — | **Kullanılmaz** [PL] §5 | — |

**Günlük rutin (18:15–18:45, ~20–30 dk):**
1. Tarama ve İş Yatırım verisini güncelle.
2. K1/K2 z-skorları; K4 iz-stoplar ve yeni B52 tetikleri; K3 takvimi.
3. Ertesi günün emirlerini hazırla.
4. Günlüğe yaz.

**Haftalık rutin (Cuma 18:30, ~45 dk):** §3.1 rejim tablosu, stres testi, dışlama listesi (VBTS, MSCI, bedelsiz), çekirdek dilimleri.

### 6.2 Maliyetler (aracı kurumla teyit edilecek; aşağıdakiler dosyalardaki değerler)

| Kalem | Değer | Kaynak / not |
|---|---|---|
| Borsa payı | Endeks vadeli on binde 0,4; pay/döviz vadeli on binde 0,3 | [HZ] §5 |
| Aracı kurum komisyonu | Banka liste fiyatı on binde 8–10; aktif bireyde on binde 1–4 tipik (teyitsiz); komisyon üzerine BSMV %5 | [HZ] §5 |
| Bireysel VİOP komisyonu, kötü durum | Bacak başına ~22 bps → SAHOL/AKBNK kenarının yarısı gider | [PL] §5 |
| Test maliyet varsayımları | K1 20 bps, K2 40 bps (gidiş-dönüş, tüm bacaklar); K4 25 bps (stres 50 bps: −1,4 puan/yıl); K3 ~30 bps | [VB] #25, §2.6; [BS] §5.3 |
| **Komisyon eşikleri (kol kapatma)** | VİOP pay vadelisinde yön başına > 15 bps → K1 kapalı; > 8 bps → K2 kapalı. Spot yön başına > 15 bps → K3 kapalı (olay başına +%0,9'un üçte biri gider) | Bu plan |
| Makas | BIST30 / VİOP-47 Kasım kontratları dar; Aralık kontratları sığ (5.11 hacim SAHOL 22 mn, KCHOL 30 mn, AKBNK 118 mn TL) | [C] viop_20261105.csv |
| Vergi | Spot pay alım-satım kazancı ve pay/endeks VİOP stopajı %0. F_USDTRY %10 (sözleşme kapanışında tevkif). PPF ve ≤6 ay mevduat %17,5. DİBS %0 yalnız teyitle. Temettü alınmıyor (K3 hak kullanımından önce satar) | [VC] #6, #7, #8 |

### 6.3 Aracı kuruma yazılı sorular (Pazartesi öncesi; cevap gelmeden ilgili kol açılmaz)

1. VİOP **nakit teminat** nemalandırılıyor mu? Oranı ne (TLREF'in yüzdesi)?
2. **PPF payı ve DİBS VİOP teminatı** olarak kabul ediliyor mu? Kesinti (haircut) oranları ne?
3. Kurum teminat oranları (house PSR):
   - F_SAHOL, F_AKBNK, F_KCHOL, F_TUPRS, F_FROTO, F_TOASO, F_ARCLK, F_YKBNK, F_XU030, F_USDTRY
   - SAHOL–AKBNK ve KCHOL–sepet için çift (spread) teminat mahsubu var mı? Takasbank asgarisi XU030 %11,4, pay vadelileri %12,7–17,0; QNB örneğinde XU030 %20, tekil %33,3 [VB] #16; [HZ] §5.
4. Komisyon tarifesi: spot ve VİOP, yön başına; BSMV dahil mi? Hedef: VİOP ≤ on binde 1,5, spot ≤ on binde 2.
5. **Kapanış seansı için önceden emir** girilebiliyor mu? Takvim yayılımı (vade devri) emri var mı?
6. Bu ay alınacak DİBS'te **stopaj %0 mı**? (GİB metni 30.06.2026'ya kadar alınanlar için %0 diyor; 31.12.2026 uzatması yalnız ikincil kaynakta [VC] #8.)
7. Pay vadelisinde vade öncesi zorunlu kapatma/fiziki teslimat süreci ve son işlem günü.
8. F_USDTRY'de %10 stopaj zararla nasıl mahsup ediliyor (yıl içi, aynı tür)?
9. ZPAT'a katılım talimatı nasıl veriliyor (kanal, son saat)?

### 6.4 Kayıt tutma

- **Günlük işlem defteri** (tek elektronik tablo; alanlar §7.2).
- **Günlük NAV** iki satır halinde: çekirdek ve uydu.
- **Aylık rapor:** uydu getirisi − uydu kovasının PPF getirisi, kol bazında.
- **Hipotez kartları** (§7.1) ilk işlemden önce tarihli olarak dosyalanır. Kart değişirse yeni hipotez sayılır.
- Aracı kurum ekstreleri ve stopaj belgeleri ay sonunda arşivlenir. Genel kural olarak GVK geçici 67 kapsamındaki yurt içi BIST/VİOP kazançlarında ve çekirdek faiz/fon gelirlerinde stopaj nihai vergidir. Bu planın bunu bağımsız teyidi yok; beyan yükümlülüğü mali müşavirle teyit edilir.

---

## 7. Öldürme kriterleri ve ileriye dönük ölçüm protokolü

### 7.1 Hipotez kartları (önceden kayıtlı beklentiler; canlı kıyas bunlara göre)

| Kol | Mekanizma | Beklenen net / işlem | İsabet | İşlem/yıl | 1R tanımı | Beklenen R | Denenen varyant (N) |
|---|---|---|---|---|---|---|---|
| K1 | Holding–iştirak fiyat sapmasının sınırlı arbitrajla kapanması | +80…+180 bps (bacak nominali) | %60–70 | ~5 | Bacak nominali × %8 | +0,10…+0,22R | 9 çift × 2 pencere × 3 ufuk × 2 dönem = 108 hücre [BS] §9.1 |
| K2 | Aynı | +40…+90 bps | %55–60 | ~5 | Bacak nominali × %8 | +0,05…+0,11R | aynı 108 hücre |
| K3 | Temettü öncesi talep / yatırımcı tercihi | +%0,5…+%0,7 (piyasa düzeltmeli) | %55–65 | 25–40 | Pozisyon × %8 | +0,06…+0,09R | az (tek pencere, 2–3 eşik) |
| K4 | Zirve kırılımında gecikmeli tepki; kazananı koşturma | Çekirdeğe göre 0…+0,3R (AÇIK); ≈0 (KAPALI) | %40–45 | KAPALI 3–10, AÇIK 20–40 | Pozisyon × %15 | 0…+0,3R | 25 kombinasyon, 4 evren [BT] §5 |
| K5 | Zorunlu teklifle sabitlenen fiyat | +%2…+%8 | %80–90 | 0–3 | Pozisyon × %20 | +0,1…+0,4R | test yok |
| K6 | Carry primi (satılmış kuyruk) | Nominalin ~%0,7–0,9'u/ay | aylık %80+ | sürekli | Nominal × %4 | — | 1 kural |

### 7.2 Günlük alanları (her işlem için)

1. İşlem no; kol; hipotez kartı no
2. Sinyal tarihi ve sinyal değeri (z, B52 seviyesi, hak kullanım günü, teklif fiyatı); rejim durumu (KAPALI/GEÇİŞ/AÇIK) ve T1–M4 değerleri
3. Amaçlanan giriş fiyatı (sinyal kapanışı veya uzlaşma) ve gerçekleşen dolum; **kayma (bps)**; dolum hatası var mı
4. Miktar (lot/kontrat), TL nominal, hesabın %'si, kullanılan teminat
5. İlk stop seviyesi, risk TL'si (= 1R)
6. Çıkış tarihi, çıkış nedeni (zaman / iz-stop / felaket stopu / kurumsal olay / rejim / manuel sapma), çıkış fiyatı
7. Brüt P&L, komisyon ve BSMV, stopaj, **net P&L**, **R-katı**
8. MAE ve MFE (kapanış bazlı)
9. Tutma süresi (gün)
10. Aynı dönemde XU030 getirisi ve aynı dönemde çekirdek (PPF) getirisi → **çekirdeğe göre fazla getiri**
11. Kural sapması (evet/hayır ve neden); not

### 7.3 Öldürme kriterleri (sayısal, önceden yazılı)

| Kriter | Eşik | Sonuç | Kaynak |
|---|---|---|---|
| Mekanizma kırılması | K1/K2'de pay yapısı değişikliği, birleşme, ZPAT; K3'te temettü vergisi veya hak kullanım kuralı değişikliği | Kol hemen kapanır; t-istatistiğine bakılmaz | [SE] §5.2 m.5 |
| Uygulama farkı | Ortalama kayma + maliyet > backtest brüt kenarının %50'si (K1 için > ~75 bps, K2 > ~45 bps, K3 > %0,45) | Kol kapanır veya emir yöntemi değişir | [SE] §5.2 m.3 |
| Erken uyarı | K1/K2: 10 işlemde ortalama < 0 ve ≥ 7 kayıp. K3: 15 olayda ortalama ≤ −%0,5. K4: 30 işlemde ortalama ≤ −0,2R | Boyut yarıya | [SE] §5.2 m.4 |
| Beklenti testi | K1/K2: 20 işlemden sonra; K3: 40 olaydan sonra; K4: 100 işlemden sonra. Ortalama net getirinin bootstrap %90 güven aralığının üst sınırı < tahmini maliyet | Kol kapanır | [SE] §5.2 m.2 |
| Tek işlem kuyruğu | K1/K2'de tek işlem bacak nominalinin −%12'sini aşarsa (backtest en kötüsü −%8,3) | Kol askıya alınır, inceleme | Bu plan |
| Kol düşüşü | K4'te kol bazında −8R; K1+K2 toplamında −4R | Kol 3 ay kâğıt üzerinde | [SE] §5.2 m.1 uyarlaması |
| Negatif çarpık kol | K6'da tek kayıp > hesabın %3'ü | K6 kalıcı olarak kapanır | [SE] §5.2 m.6 |
| Beta sızıntısı | K1/K2'nin 12 aylık getirisinin XU030 ile korelasyonu > 0,5 | Kol beta taşıyor; hedge oranı gözden geçirilir | [SE] §5.2 m.7 |
| Toplam uydu | Aylık −%2,5 / birikimli −%4 / −%6 (§5) | Dur / yarıya / hepsini kapat | §5 |

### 7.4 Ölçekleme istatistiği: ne zaman büyütülür?

Gerçekçi işlem sayılarıyla kanıt yavaş birikir:
- İşlem başı SR 0,1 olan bir kenarın t = 2'ye ulaşması **400 işlem** ister [SE] §3.7.
- +0,2R'lik kırılım sisteminde sıralı test (SPRT) medyan **~390 işlem** ister. Gerçek kenar backtest'in yarısıysa ~1.700 işlem.
- K1 için işlem başı SR ≈ 0,4–0,5 varsayılırsa (ortalama ~%2, sd ~%4–5) t ≈ 2 için **16–25 işlem** gerekir.

Kurallar:
1. **12 ay dolmadan ve aşağıdaki minimum işlem sayısına ulaşmadan boyut artırılmaz.** Bu sürede yalnız küçültme ve kapatma kararı verilebilir [SE] §5.3 m.4.

   | Kol | Minimum | Süre |
   |---|---|---|
   | K1 | 20 işlem | ~4 yıl |
   | K2 | 20 işlem | ~4 yıl |
   | K3 | 60 olay | ~2 sezon |

2. **Artış koşulları (hepsi birlikte):**
   - Canlı ortalama net > 0
   - t ≥ 1,5
   - Canlı ortalama ≥ backtest beklentisinin %50'si
   - Ortalama kayma, kenarın %30'unun altında
   - Kol düşüşü simülasyon bandının içinde
3. **Artış adımı:** En çok **1,5×**, yılda en çok bir kez. Toplam en çok 2× (KAPALI tablosuna göre).
4. **K4 istatistikle büyütülmez.** Pratik ufukta 390 işlem birikmez. K4'ün boyutu yalnız rejime bağlıdır (§2.4 tablosu) ve işlem başı risk %0,5'i hiç aşmaz.
5. Pazartesi'den itibaren eski 4 kenar ve bedelsiz öncesi için **kâğıt üzerinde** aynı günlük alanları doldurulur. Kâğıttan canlıya geçiş için ilgili doğrulama raporu ve 30 kâğıt işlem gerekir.

### 7.5 Gözden geçirme takvimi

| Sıklık | İş |
|---|---|
| Her kapanış | Günlük rutin (§6.1) |
| Cuma | Rejim tablosu, stres testi, açık risk, dışlama listesi, K6 kapısı |
| Ay sonu (30.11 ilk) | T2; kol bazında R dağılımı, kayma, çekirdeğe göre fazla getiri; aylık limit kontrolü |
| Her 10 işlem/olay (kol bazında) | §7.3 erken uyarı |
| 3 ayda bir | Hipotez kartlarıyla kıyas; uydu düşüşü simülasyon bandı (ilk çeyrekte [SE] §3.4 yöntemiyle kurulur) |
| 12 ay (Kasım 2027) | Ölçekleme kararı (§7.4) |

---

## 8. Beklenen sonuç aralıkları (engele göre) ve dürüst belirsizlik

### 8.1 Kol bazında (rejim KAPALI, 12 ay, maliyet ve vergi sonrası, çekirdeğe göre fazla getiri)

| Kol | Hesaba katkı, merkez | Aralık (yaklaşık %80) | Belirsizliğin ana kaynağı |
|---|---|---|---|
| K1 SAHOL↔AKBNK | +0,4 puan | 0…+0,9 | Teminat faizi, komisyon, yılda ~5 işlemin gürültüsü |
| K2 KCHOL↔sepet (≥5 mn) | +0,15 | −0,2…+0,4 | Zayıf kenar, 6 bacak maliyeti, takip hatası |
| K3 Temettü | +0,6 | 0…+1,3 | Sezon dışı ay sayısı, olay kuyruğu |
| K4 Kırılım sondası | 0 | −0,3…+0,3 | Rejim |
| K5 Özel durum | +0,1 | 0…+0,5 | Olay bulunup bulunmaması |
| K6 Carry (kapıya bağlı) | +0,3 | −3,0…+0,6 | Kur şoku (negatif çarpık) |
| **Toplam KAPALI** | **≈ +1,5 puan/yıl** | **−2…+3** | |
| Rejim AÇIK olursa ek (K4 tam + K7) | +2…+5 | −4…+15 | Sağ kuyruk; 2022 tipi yılda çok daha fazla, sahte sinyalde negatif |

### 8.2 Senaryo bazında (12 ay; olasılıklar öznel, [TM] §5.2)

| Senaryo | Olasılık | Çekirdek net (nominal) | Uydu fazla getirisi | Hesap toplamı (nominal net) |
|---|---|---|---|---|
| S1 Sönümlenme, rejim 2–6 ay içinde döner | %35 | %30–33 (hızlı indirim) | +2…+6 | %33–38 |
| S2 Yatay kanama, carry kazanır | %40 | %33–36 | 0…+2,5 | %33–38 |
| S3 Kontrollü kur hızlanması | %15 | %35–38 | −1…+1,5 | %34–39 |
| S4 Kırılma (kur +%15–30, acil faiz artışı) | %10 | %38–45 (nominal) | −4…−1 | %34–44 nominal; USD bazında belirgin negatif |
| **Ağırlıklı** | | ~%33–35 | **≈ +1,7 puan** (%80 aralık ≈ −2…+5) | **≈ %35–37** |

TL karşılıkları (merkez +1,5–2 puan; aralık −2…+5):

| Hesap | Merkez | Aralık |
|---|---|---|
| 1 mn TL | +15–20 bin TL/yıl | −20 bin…+50 bin |
| 5 mn TL | +75–100 bin | −100…+250 bin |
| 20 mn TL | +300–400 bin | −400 bin…+1 mn |

Kapasite 20 mn TL'ye kadar bağlayıcı değil. Tek istisna K2/K1 Aralık kontrat derinliği.

### 8.3 Sorunun açık cevabı: "Engelin üstüne gerçekçi olarak ne kadar bekleyebilirim?"

1. **Bu rejimde yılda +1 ile +3 puan, merkez ~+1,5–2.** Yani hesabın toplam getirisi net nominal TL'de ~%33–37. Reel olarak ~+%3–8.
   - Getirinin %90'ından fazlası çekirdekten gelir.
   - Uydu katmanının asıl değeri bugün getiri değil. Rejim dönüşüne hazır, ölçülmüş ve maliyeti bilinen bir süreç bırakmak.
2. **Rejim dönerse yılda +4 ile +8 puan.** Bunlar S1 tetikleri (rezerv artışı, aylık TÜFE < %2, yabancı alımı, CDS < 230) ya da XU100 > SMA200 olur ve kırılım + endeks kolu açılırsa geçerli.
   - Tarihsel referans: rejim kırılmalarından sonra bankalar 3–6 ayda dolar bazında +%40–90 kazandı, ama **n = 4** [TM] §2.3.
   - 2022 tipi bir yılda iki haneli fazla getiri mümkün, ama planlanamaz.
3. **+10–20 puan isteniyorsa:** Bunun yolu bu planın 3–5 katı açık risk (%8–12), engele göre −%25…−%40 düşüş toleransı ve sağ kuyruğa bağımlılık [SE] §5.1. Bu, C açısının dışında. Kanıt da bu rejimde onu desteklemiyor: kırılım portföyü 2024–26'da engelin 2–8 puan altında [VB] §2.1; hiçbir küme kuralı rf'yi geçmedi [DB] §0 m.4.
4. **Ölçülebilirlik:** İlk 12 ayda yaklaşık 10 çift işlemi, 25–40 temettü olayı ve birkaç sonda birikir. Bu sayılarla uydu fazla getirisinin sıfırdan istatistiksel olarak ayrışma olasılığı düşük (< %30). 12 ay sonunda bilinen şeyler daha çok kayma, maliyet, kurala uyum ve kuyruk davranışı olacak; "kenar kanıtlandı" denemeyecek [SE] §3.7.

### 8.4 Bu planı yanıltabilecek şeyler

- **Çekirdeğin kendisi:** Banka veya fon riski (tasfiyedeki PPF'ler −%95…−%99,9 kaybetti) → en az 2 banka, banka iştiraki fon.
- **2027 vergi değişikliği** (%17,5 stopajın süresi 31.12.2026'da doluyor): net engel 1–3 puan oynayabilir [VC] §2 m.6.
- **Faizin hızlı düşüşü:** Çekirdek getirisi %28'e iner. Bu durumda S1 olasılığı ve K4/K7'nin önemi artar.
- **Aracı kurum yanıtları:** Teminat faizsizse ve komisyon yüksekse K1/K2'nin katkısı sıfıra iner. Bu durumda plan pratikte "çekirdek + temettü + sonda" olur ve beklenti +0,5…+1 puana düşer.
- **Ortak kör nokta:** Tüm kanıt aynı İş Yatırım verisinden ve hayatta kalan hisse evreninden geliyor [VB] §2.4; [BT] §1.

---

## 9. Pazartesi 9.11.2026: tek sayfa kontrol listesi

**Cuma 6.11 akşamı / hafta sonu**
- [ ] 18:20 sonrası `bist_tarama.py` (06.11 kapanışı); `viop_20261106.csv` resmi bültenini indir; XU030 zımni faizini **uzlaşma fiyatıyla** hesapla (tarama değeri değil).
- [ ] K1/K2 z-skorlarını 06.11 kapanışıyla yeniden hesapla (05.11: SAHOL↔AKBNK −0,72; KCHOL↔sepet +2,23).
- [ ] K4 tetik seviyelerini güncelle (05.11: ENJSA 127,00; ENERY 14,60; AHGAZ 48,70; RYSAS 30,28) ve RYSAS'ın likidite sırasını kontrol et.
- [ ] KAP: 30 gün içindeki temettü hak kullanımları (verim ≥ %2, ilk 100 hisse); açık ZPAT'lar; AKCNS teklif durumu.
- [ ] Aracı kuruma §6.3'teki 9 soruyu yazılı gönder. **Cevap gelmeden K1, K2, K6 açılmaz.**
- [ ] Dışlama listesini (§4.2) emir ekranında "yasaklı" olarak işaretle.
- [ ] Günlük şablonunu (§7.2) ve hipotez kartlarını (§7.1) tarihli kaydet.

**Pazartesi sabah (09:30–10:00, tek seferlik)**
- [ ] Çekirdeği kur:
  - Mevduat 1. dilim (%11,25), 32 gün, büyük banka
  - PPF %40 (2 banka iştiraki fon; uydu kovası %15 dahil)
  - DİBS %15 yalnız stopaj %0 yazılıysa; değilse bu tutar PPF'ye
- [ ] Bilançosu bu akşam gelecek hisselerde (KCHOL, BIMAS, PGSUS, TCELL, SOKM, DOAS, AKSEN, ALARK, ARCLK, EREGL ve diğerleri) **yeni emir yok**.
- [ ] Açık uydu pozisyonu yok. Bekleyen emir yok (Cuma kapanışında tetik çıkmadıysa).

**Pazartesi kapanış (18:15–18:45)**
- [ ] Rejim: KAPALI mı? (T1, T2, M1–M4; §3.1)
- [ ] K1: |z| ≥ 2 ise Salı 09:30 limitli emirler (uzlaşma ± %0,5), eşit TL; vade seçimi (20 gün 30.11'i aşıyorsa Aralık).
- [ ] K2: Giriş yok; 10.11 kapanışında temiz z.
- [ ] K4: B52 + TT kapanışı varsa Salı kapanış seansına sonda emri (risk %0,25, limit × 1,06). Aynı kümeden en çok 1.
- [ ] Açık risk ≤ %2,5; stres ≤ %6; VİOP teminatı ≤ %15.
- [ ] Günlük kaydı.

**Hafta içi hatırlatmalar**
- Sal 10.11 kapanış: K2 z (bilanço sonrası).
- Çar 11.11: K2 girişi (koşul varsa).
- Per 12.11: 01:00 MSCI listesi → dışlama; 14:30 rezerv/akım → M1, M3, K6 kapısı.
- 12–13.11 SPK bülteni: kredili işlem esnekliği uzatıldı mı? Uzatılmadıysa 16–20.11'de yeni K4 sondası yok.
- Cum 13.11 18:30: haftalık gözden geçirme.
- **26.11 kapanış:** Kasım pay vadelisi bacaklarını devret veya kapat.

**Hiçbir koşul tetiklenmezse:** Pozisyonsuz kal. Çekirdekte beklemek bu planın varsayılan ve meşru sonucu [KO] §8.

---

## Ek A. Bu taslaktaki kendi hesaplar [C]: yöntem ve sınırlar

- **Veri:** Oturum önbelleğindeki İş Yatırım günlük düzeltilmiş kapanışları (`scratchpad/bsk/panel`, `scratchpad/data/snapshot_bist/`, `scratchpad/veri/*.json`), son gün 05.11.2026. Yeni veri çekilmedi.
- **Çift z-skorları:** [VB]'nin `rv_lag.py` tanımıyla birebir:
  - Günlük getirilerde |r| > %60 maskelenir.
  - Sepet, günlük log getirilerin eşit ağırlıklı ortalamasından kurulur.
  - L = 60, z = (x − ort60) / std60.
  - Örtüşen-gün ve "kalıcı sinyal" kırılımları bu taslakta eklendi. Örtüşen gözlemler bağımsız değil; t-istatistiği bu yüzden verilmedi.
- **Tetik seviyeleri:** Diğer bacak sabit ve 60 günlük pencere 05.11'deki haliyle varsayıldı. Pencere her gün kaydığı için seviyeler yaklaşık.
- **B52 seviyeleri:** 05.11 hariç önceki 252 işlem gününün en yüksek düzeltilmiş kapanışı. SMA50, SMA150, SMA200 ve TT koşulları aynı seriden. RS yüzdeliği taramadan [TR] alındı.
- **Likidite sırası:** 248 hisselik önbellek evreninde 60 günlük medyan `HGDG_HACIM`. Tüm piyasa sırası değil.
- **AKCNS:** ZPAT metni SPK 2026/59'un indirilmiş metninden okundu. Fiyat ve halka açık piyasa değeri İş Yatırım `HisseTekil` önbelleğinden. Teklif dönemi ve sonucu KAP'tan **teyit edilmedi**.
- **S2–S5 farkından türetilen "rejim kapalıyken +%1,9/işlem":** [BT] §5.1 tablosundaki toplamların aritmetik farkı. Ayrı bir test değil.
- **Çekirdek karşılaştırması (§1.2):**
  - PPF: TLREF %35,85 günlük bileşik, %1 ücret, %17,5 stopaj.
  - Mevduat: %39,52 brüt, 32 günlük yenileme.
  - Nakit-taşıma: 14.734 / 14.101, 56 gün.
  - Faizler sabit varsayıldı; 10.12 PPK'da indirim olursa PPF ve mevduat getirisi düşer.
