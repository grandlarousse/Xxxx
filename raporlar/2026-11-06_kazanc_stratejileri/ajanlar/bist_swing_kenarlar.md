# BIST ve VİOP: swing ufkunda (birkaç gün – ~3 ay) belgelenmiş getiri düzenlilikleri

Tarih: 06.11.2026. Ajan raporu (ham çıktı). Yatırım tavsiyesi değildir.

Kapsam: 1–3 günlük lead-lag mikro kenarlarının ötesinde, BIST spot ve VİOP'ta gün–3 ay ufkunda belgelenmiş düzenlilikler. Her başlıkta kanıt türü, dönem, etki büyüklüğü, yayın/örneklem dışı davranış, maliyet, kapasite ve bir Türk bireysel yatırımcının uygulayabilirliği.

**Yöntem ve sınırlar (önce okunmalı)**

1. İki kaynak türü var: (a) literatür (DergiPark, Borsa Istanbul Review, SSRN, tezler), (b) bu rapor için yapılan **kendi testlerim**. Kendi testlerim İş Yatırım'ın herkese açık günlük fiyat uç noktasından indirilen düzeltilmiş kapanışlarla yapıldı (`HisseTekil`, 2005-01-03 → 2026-11-05; XU100 ve USDTRY aynı kaynaktan), TL nakit getirisi TCMB'nin 1 hafta repo tarih tablosundan (tcmb.gov.tr "Merkez Bankası Faiz Oranları / 1 Hafta Repo") kuruldu.
2. **Hayatta kalma yanlılığı (survivorship) ciddi.** İş Yatırım uç noktası yalnız bugün işlem gören kodları veriyor (KOZAL/KOZAA/IPEKE gibi eski kodlar boş döndü). Evren, benim seçtiğim {{EVREN_N}} hisse (VİOP'taki 47 pay + BIST100/BIST Tüm'den likit adlar + 2020–24 halka arzları). Batan/kottan çıkan hisse yok. Bu, kayıp portföylerinin (losers) getirisini yukarı, eşit ağırlıklı evren getirisini yukarı iter. Momentum farkını (kazanan–kaybeden) büyük ihtimalle **küçültür**; kısa vadeli devam (losers keep losing) bulgusunu da **küçültür**; ama "VİOP-47 içinde momentum" sonucunu **büyütür** (bugün VİOP'ta olanlar geçmişin kazananlarıdır).
3. Çoklu test: ~10 sinyal × 3–4 dönem × birkaç parametre denendi. Tek bir parametre setinin en iyi sonucu değil, **sinyaller arası tutarlılık** ve **alt dönem kararlılığı** esas alındı. Raporladığım en iyi kombinasyonlara %30–50 "backtest iskontosu" uygulanmalı.
4. Web arama bütçesi (oturum başına 200 arama, tüm ajanlar ortak) iş ortasında bitti. Mevsimsellik, temettü duyurusu, MSCI/FTSE dengelemesi, kredi notu, faiz kararı günü, VBTS tedbirleri, spin-off, TEFAS akımı ve XU030 opsiyon VRP başlıklarında yeni literatür taraması yapılamadı; bunlarda ya kendi testim var ya da "kanıt bulunamadı/test edilmedi" yazıyor. Devam için kullanıcı yeni mesajla aramayı sürdürtebilir.
5. TL nakit serisi politika faizinin yıllık efektif kabulüyle kuruldu; 2017–18'de geç likidite penceresi (%12,75) ve Mart–Nisan 2025'te gecelik borç verme (%46) ile düzeltildi. Gerçek PPF getirisinden biraz düşüktür (2024'te seri %49,1, Kuveyt Türk'e göre PPF ortalaması ~%53). Yani "nakit" engeli **muhafazakar düşük**; stratejiler lehine hafif yanlı.

---

## 0. Kısa cevap

{{OZET}}

---

## 1. Engel (hurdle) doğru tanımlanmalı

- Politika faizi 22.10.2026 PPK'da %37 → %36 (−100 bp); koridor %34,5–39 ([QNB Invest](https://www.qnbinvest.com.tr/investodak/qnbarastirma/tcmb-ekim-ayi-faiz-kararini-acikladi-politika-faizi-36ya-indirildi)). TCMB tablosunda yürürlük 23.10.2026.
- Eylül 2026 TÜFE %29,73 y/y → ex-post **reel politika faizi ≈ 1,36/1,2973 − 1 ≈ %4,8**. "Reel faiz %40–50" algısı yanlış; %36–40 **nominal**.
- Bireysel yatırımcı için PPF/fon kazancı stopajı **%17,5**; 05.09.2026 Cumhurbaşkanı Kararı (11734) yalnız kurumsal yatırımcının PPF stopajını %0 → %10 yaptı ([PwC bülten 2026/03](https://www.pwc.com.tr/tr/sektorler/bankacilik-sermaye-piyasalari/bultenler/2026/kurumsal-yatirimcilarin-para-piyasasi-fonu-kazanclarinda-tevkifat-orani-yuzde-10a-yukseltildi.html), [İş Portföy Eylül 2026](https://www.isportfoy.com.tr/medya-ve-blog/para-piyasasi-fonlarinda-kurumlara-uygulanan-stopaj-duzenlemesi-hakkinda-eylul-2026)).
- VİOP'ta pay ve pay endeksine dayalı sözleşmelerde bireysel stopaj **%0**, diğer (USDTRY, altın dahil) **%10** ([Borsa İstanbul VİOP vergilendirme](https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/vergilendirme)). BIST pay alım-satım kazancı da bireyde %0.
- Sonuç: PPF brüt ~%37–40 (TCMB 1 hafta repo %36, efektif bileşik daha yüksek), stopaj sonrası **~%31–33**. Pay/endeks stratejisi vergi sonrası bununla kıyaslanır. Ama hisse riski (yıllık vol %30+, −%30 düşüşler) için makul hedef: **vergi sonrası %45–50+**. USD hedefi: T-bill ~%3,75–4 (Fed 16.09.2026 +25 bp, kontrol edilmedi) ve TL carry fırsat maliyeti.
- Tarihsel tablo (kendi hesabım, XU100 fiyat endeksi, temettü hariç):

{{YILLIK_TABLO}}

Yorum: 2024'ten beri pozitif reel faiz rejiminde XU100 her yıl TL nakdin **gerisinde** (2024 −%11,7, 2025 −%20,2, 2026 YTD −%22,9). 2021–23'teki büyük nominal getiriler negatif reel faiz rejiminin ürünüydü. Bu tek bulgu, "BIST'te kazananlar nasıl kazandı" sorusunun en büyük parçasıdır: **rejim (reel faizin işareti) > hisse seçimi**.

---

## 2. Sıralama (kanıt kalitesi × maliyet sonrası büyüklük × swing ufkuna uyum)

{{SIRALAMA}}

---

## 3. Kesitsel fiyat düzenlilikleri

### 3.1 Literatür: BIST'te momentum karışık, uzun ufukta dönüş baskın

| Çalışma | Tür | Dönem | Bulgu |
|---|---|---|---|
| Bildik & Gülay (2007), *International Review of Finance* 7(1-2) [IDEAS](https://ideas.repec.org/a/bla/irvfin/v7y2007i1-2p61-87.html) | hakemli | 1991–2000 | Zıtlık (kaybedenleri al, kazananları sat) ~%15/yıl anormal; 1–36 ay tutuşta karlı; aylık %1,14 (Ünal 2021 özetinden) |
| Kandır & İnan (2011) (Ünal 2021 özetinden) | hakemli | 2000–2010 | Yalnız 12 ay oluşum/12 ay tutuşta kazananlar > kaybedenler; 3/6/9 ayda anlamsız |
| Ersoy & Ünlü (2013) (Ünal 2021 özetinden) | hakemli | 1995–2010 | 6 ay oluşum/6 ay tutuşta momentum var, tüm büyüklük gruplarında |
| Kaldırım (2017) (Ünal 2021 özetinden) | tez/makale | 2008–2015, BIST100 | 9–12 ay oluşum/tutuşta anlamlı; en iyi 12/12 ~%50 anormal (kümülatif); düşük fiyatlılarda daha güçlü |
| Alper & Aydoğan (2017), *Muhasebe ve Finansman Dergisi* [DergiPark](https://dergipark.org.tr/tr/download/article-file/428034) | hakemli | 2001–2015, 122 hisse | 1–5 yıl oluşum: kaybedenler izleyen 12 ayda kazananları %29 geçti (uzun ufuk zıtlık) |
| Ünal (2021), *Uluslararası Yönetim İktisat ve İşletme Dergisi* ICAFR özel [DergiPark](https://dergipark.org.tr/en/download/article-file/1419417) | hakemli | 1997–2020, tüm hisseler, eşit ağırlık | En yüksek %20 (6 ay oluşum) izleyen 12 ayda %29,7; diğer dilimler %37–41 (t=7,3). Kazananlar 6–60 ay boyunca geride. "Spekülatif şişen hisse" etkisi |
| Gökçen, "Factor investing in the Turkish equity market", *Borsa Istanbul Review* (2026) [SSRN 4588551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4588551), [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2214845026001043) | hakemli (WP 2023→2026) | 1994–2024, survivorship'siz | En güçlü faktör değer (B/M): >%17/yıl prim (WP), yayın özetinde değer alfa %12–13/yıl; momentum, boyut, karlılık **yalnız 2005 sonrası** anlamlı; düşük risk > yüksek risk; çok faktörlü portföy EM endeksini USD'de geçiyor. Momentum rakamı tam metinde, doğrulanmadı |
| Chui, Titman & Wei (2010), *JF* 65(1) [IDEAS](https://ideas.repec.org/a/bla/jfinan/v65y2010i1p361-392.html) | hakemli | 41 ülke 1980–2003 | Bireycilik endeksi düşük ülkelerde momentum zayıf; Türkiye bu grupta (Türkiye özel rakamı doğrulanmadı) |
| Demirer, Yüksel & Yüksel (2017), *RIBAF* 42 [EconPapers](https://econpapers.repec.org/RePEc:eee:riibaf:v:42:y:2017:i:c:p:1445-1454) | hakemli | BIST | Kısa vadeli dönüş getirisi piyasa durumuna bağlı; negatif piyasa durumunda "kaliteye kaçış" hisselerinde güçlü; petrol getirisi makro değişkenlerin öngörü gücünü emiyor. Büyüklük rakamı ücretli metinde |
| George & Hwang 52-hafta: "Gross profitability and 52-week high", *MAKÜ İİBF* (2021) [DergiPark DOI](https://dx.doi.org/10.30798/makuiibf.790900) | hakemli | 2007–2016 | 52-hafta zirvesi primi pozitif ama **anlamsız**; brüt karlılık primi anlamlı |

Ortak payda: eşit ağırlıklı, filtresiz tüm-hisse örneklemlerinde (mikro-cap ve manipülatif hareketler dahil) orta vadeli momentum ya yok ya da tersine dönüyor; 2005 sonrası ve likidite filtreli örneklemlerde momentum ortaya çıkıyor.

### 3.2 Kendi testim: likit evrende momentum, 52-hafta zirvesi, rezidüel momentum, kısa vadeli devam

Kurulum: her ay sonu, son 60 günlük medyan TL hacmine göre en likit **N** hisse (≥250 gün geçmiş), sinyale göre beşli dilim, eşit ağırlık, 1 ay tutuş. Q5 = en yüksek sinyal. Maliyet: tek yön %0,15 × dilim devri (yalnız long-only Q5 net getirisine uygulandı). Formasyon: MOM12_1 = t−12…t−1 getiri (son ay atlanır); H52 = fiyat/252 gün zirvesi; RESMOM = 36 ay XU100 betasına göre rezidüel getirilerin t−12…t−1 toplamı / std; MOM1 = son 1 ay; LOWVOL = −60 gün vol.

**N = 60 (geniş evren)**

{{XS60}}

**N = 100 (daha geniş, daha az likit)**

{{XS100}}

**Yalnız VİOP pay vadelisi olan 47 hisse (N=40)** — burada short bacak VİOP ile gerçekten uygulanabilir; ama bugünkü VİOP listesi geçmişin kazananlarından oluştuğu için yukarı yanlı.

{{XSVIOP}}

Yıllara göre (N=60) Q5−EW farkı (puan, yıllık bileşik farkı):

{{XS_YIL}}

Okuma:
{{XS_YORUM}}

### 3.3 Haftalık kısa vadeli dönüş yok; 2016 sonrası **devam** var (kaybedenler kaybetmeye devam ediyor)

Kurulum: her cuma, son 1/2/4 haftalık getiriye göre beşli dilim (en likit N), izleyen hafta getirisi. "Ters" = kaybedenler − kazananlar.

{{WK}}

Yorum: 2007–15'te zayıf dönüş (1 haftada +21 bps, t=1,5) vardı; 2016 sonrası işaret döndü. Asimetri önemli: getiri farkının büyük kısmı **kaybedenlerin eşit ağırlıklı evrenin altında kalmasından** geliyor (−27…−66 bps/hafta), kazananların üstünlüğü küçük (+11…+28 bps). Survivorship bu bulguyu zayıflatma yönünde çalışır (batan kaybedenler örneklemde yok), yani gerçek etki muhtemelen daha güçlü. Mekanik açıklama: ±%10 fiyat limiti, kredili pozisyonların zorunlu kapanışı (kredili işlem faizi %100'e yaklaşan dönemlerde "kredisi yüksek yatırımcı" satışları: [Bloomberg HT 12.10.2024](https://www.bloomberght.com/borsayi-kredisi-yuksek-yatirimci-dagitti-2362224)), fon çıkışları. Uygulama: **düşeni "ucuzladı" diye haftalık almak 2016 sonrası BIST'te para kaybettirdi.** Short tarafı yalnız VİOP-47'de mümkün (çoğunda PSR %33,3; ASTOR/HALKB/VESTL %100).

### 3.4 Sektör/endüstri momentumu

BIST sektör endekslerinde endüstri momentumunu doğrudan test eden çalışma bulunamadı (Moskowitz & Grinblatt 1999 ABD'de bireysel momentumun büyük kısmını endüstriye bağlıyor; [Quantpedia özeti](https://quantpedia.com/strategies/sector-momentum-rotational-system)). Sektör eşlemesi gerektirdiği için test etmedim. Kullanıcının "stratejik kümelenme" yaklaşımı pratikte tema/sektör momentumu; 3.2'deki rezidüel momentum ve 52-hafta sonuçları bu yaklaşımın hisse düzeyindeki karşılığıdır.

---

## 4. Endeks düzeyi trend takibi / zaman serisi momentumu (XU100, XU030 vadeli vekili)

Kurulum: XU100 kapanışında sinyal, ertesi gün uygulanır. Pozisyon vadeli gibi modellendi: teminat TL nakitte, getiri = nakit + w×(XU100 − nakit) (vadeli ≈ spot×(1+r), temettü ihmal). Short taraf (L/S) vadeli short: 2×nakit − endeks. Yön değişimi başına %0,10 maliyet. vt25 = 20 gün gerçekleşen vol ile %25 hedef, kaldıraç ≤1,5.

{{TREND}}

Okuma:
{{TREND_YORUM}}

Literatür: Ülkü (2009), *ISE Review* 11(41): Brock-Lakonishok-LeBaron kuralları DJIA'da kayboldu, ISE-100'de daha iyi; 22 günlük SMA ISE-100'de **maliyet sonrası anlamlı pozitif** ([IDEAS](https://ideas.repec.org/a/bor/iserev/v11y2009i41p25-44.html)). 2023 tarihli 41 endeksli SPP testi: tek yön ≥20 bps maliyette yalnız 4 gelişmekte olan piyasada anlamlı kural kaldı ([Springer FMPM 2023](https://link.springer.com/10.1007/s11408-023-00433-2)). Küresel TSMOM kanıtı (Moskowitz-Ooi-Pedersen; "Trends Everywhere" brüt Sharpe 1,6 çoklu varlık) Türkiye'yi ayrı raporlamıyor ([Quantpedia](https://quantpedia.com/time-series-momentum-works-everywhere/)).

### 4.1 Kombinasyon: hisse seçimi (momentum/52-hafta) + piyasa rejim filtresi

En umut verici bulgu bu. Ay sonu XU100'ün 12 aylık getirisi aynı dönemin TL nakit getirisini aşıyorsa (TSMOM12) ya da XU100 > SMA200 ise Q5'e (N=60, ~12 hisse) gir, değilse nakit. Rejim geçişinde ek %0,3 maliyet.

{{COMBO}}

{{COMBO_YORUM}}

---

## 5. Olaylar

### 5.1 Bedelsiz sermaye artırımı

Literatür:
- Küçüksille & Mizrahi (2015), *Sosyal ve Beşeri Bilimler Araştırmaları Dergisi* 35, 2012–2014, olay penceresi (−5,+5): duyuru sonrası anlamlı pozitif AAR yok; ≥%100 bedelsizlerde +4. gün anlamlı negatif; pencere içinde bazı alt aralıklarda pozitif KAAR ([DergiPark](https://dergipark.org.tr/en/download/article-file/452850)).
- Işıker & Taş (2021), *Journal of Capital Markets Studies* 5(1): iç kaynaklardan (sermaye düzeltmesi/emisyon primi) bedelsiz duyuruları, geçmiş yıl karından yapılanlardan daha yüksek duyuru getirisi; büyük oranlar daha iyi karşılanıyor; KAP 2010 öncesi veri yok ([IDEAS](https://ideas.repec.org/a/eme/jcmspp/jcms-03-2021-0008.html)). Rakamlar tam metinde, doğrulanmadı.
- SPK onay tarihli çalışma (2016–2017): onay sonrası 2., 3. ve 5. günlerde anlamlı negatif KAAR (arama özetinden; [DergiPark sobbiad 412528](https://dergipark.org.tr/en/pub/sobbiad/issue/36421/412528) ile eşleşmesi doğrulanmadı).

Kendi testim (bölünme/hak kullanım günü; fiyat düzeltme faktörü k = (ham/düzeltilmiş)ₜ₋₁ / (ham/düzeltilmiş)ₜ ≥ 1,15 olan günler "sermaye artırımı hak kullanımı"; bedelli de içerebilir ama likit adlarda çoğu bedelsiz; piyasa-düzeltmeli = hisse − XU100):

{{BEDELSIZ}}

{{BEDELSIZ_YORUM}}

### 5.2 Bedelli sermaye artırımı
Arama özetinde 2017–2022 bedelli artırımlarında negatif KAAR bulan bir çalışma görüldü; tam metin ve rakam doğrulanmadı. Kendi testimde bedelli ve bedelsiz ayrılamadı. Hüküm: kanıt zayıf, ticari kenar olarak kullanılmamalı.

### 5.3 Temettü (hak kullanım günü etrafı)

Kendi testim (1,02 < k < 1,15, temettü kaynaklı düzeltme):

{{TEMETTU}}

Duyuru tarihi etkisi için literatür taraması bütçe nedeniyle yapılamadı.

### 5.4 Pay geri alım duyuruları
- Ayan Civelek & Konak, BIST Sınai, 34 şirket, 01.2014–01.2020: duyuru günü ve +1 günde pozitif AAR (~+%0,55/+%0,56), sonrasında belirgin eğilim yok; duyuru öncesi 20 günde ağırlıkla negatif AAR (geri alımlar düşüş sonrası geliyor) ([DergiPark PDF](https://dergipark.org.tr/en/download/article-file/2325701)). Tabloda t-istatistikleri ile p-değerleri tutarsız; kalite düşük.
- Torun & Karan (2023), 2018–2021, 74 duyuru: fiyat etkisi var; Arsoy (2010–2015): anlamlı KAAR yok ([AGÜ GCRIS](https://gcris.agu.edu.tr/items/20b376f3-fd7e-4eb6-9977-ddf61abc2b3b)).
- Hüküm: 1–2 günlük duyuru tepkisi; swing ufkunda kenar yok. Kriz dönemlerinde (piyasa −%20) toplu geri alım ilanları dip sinyali gibi algılanıyor ama sistematik test bulunamadı.

### 5.5 İçeriden alım (KAP pay alım-satım bildirimi)
- Avcı (2024), *European Journal of Finance* 30(6): 2008–2019, ~65.000 içeriden işlem; içeriden işlemi izleyen 1 yılda **%6,58 anormal kâr**; yöneticiler, büyük ortaklar ve kurumlar daha fazla; alım ve satım ikisi de karlı; **bilgisiz yatırımcı içeriden portföyü taklit ederek piyasayı yenebilir**; düzenleme değişiklikleri kârı azaltmamış ([Sabancı repo](https://research.sabanciuniv.edu/id/eprint/50115), DOI 10.1080/1351847X.2023.2216730). Çalışma kağıdı: (0,5) penceresinde %1,56 ([Scribd SSRN 3896937 kopyası](https://www.scribd.com/document/532198970/SSRN-id3896937)).
- METU tezi: net içeriden alımı izlemek genelde güvenilir pozitif anormal getiri vermiyor, kısa pencerelerde küçük kazanç; net satış portföyleri uzun tutuşta anlamlı negatif ([METU](https://open.metu.edu.tr/handle/11511/19162)).
- Hüküm: BIST'te belgelenmiş en iyi "bilgi" kenarlarından biri, ama yıllık ~%6,6 anormal (brüt), olay başı küçük; swing ufkunda tek başına engelin üstüne taşımaz, filtre/kümelenme kriteri olarak değerli (özellikle büyük ortak alımları + momentum).

### 5.6 Halka arz sonrası (tavan serisi ve dönüş)
Literatür: 1993–2020, 347 halka arz: kısa vadede düşük fiyatlama, 36 ayda negatif aşırı getiri; 2010–01/2020 uzun dönem kümülatif piyasa-düzeltmeli getiri XU100'e göre −%10,56, XU30'a göre −%12; 2020 kohortunda ilk gün AAR >%10, 7 günlük KAAR ~%70 (arama özetleri: [DergiPark](https://dergipark.org.tr/en/download/article-file/1042951), [Beykent](https://earsiv.beykent.edu.tr/items/1c99c9a6-3232-4866-8de0-10434a562ce6/full)). 65 halka arzda düşük fiyatlama ile 3 yıllık getiri arasında −%29,5 korelasyon (Paradoks 2020, aynı DergiPark PDF). Tütüncü & Uzunel (2020): 2010–2017 halka arzları faaliyet performansında eşlenik şirketlerin gerisinde ([DergiPark](https://dergipark.org.tr/en/download/article-file/1271957)).

Kendi testim (2020–2024'te kote olan ve hâlâ işlem gören {{IPO_N}} hisse; seçim benim, yanlı): "tavan serisi" = 2. günden itibaren ardışık ≥%9,5 günler.

{{IPO}}

{{IPO_YORUM}}

### 5.7 Endeks giriş/çıkışları (BIST30/BIST100)
- Aslan (2019), Boğaziçi YL tezi, 2009–2017, BIST100'de 296, BIST30'da 96 değişiklik: girişlerde pozitif ama anlamsız; **çıkışlarda anlamlı negatif**. BIST30'dan çıkanlarda duyuru öncesi 10 gün KAAR **−%4,07 (t=−2,73)**, yürürlükten sonraki gün +%1,1 (t=2,04) geri dönüş; BIST30'a girenlerde yürürlükten sonraki 10 günde **−%2,22 (t=−2,25)** ([Boğaziçi](https://digitalarchive.library.bogazici.edu.tr/items/56f8a94f-66bd-4cd6-a1e8-ba13f5278565)).
- Aydıner & Altay (2020), *Ankara Üniv. SBF Dergisi* 75(4): BIST30/50/100/Temettü değişikliklerinde çıkış duyurusu ve çıkış negatif, giriş pozitif; fiyat baskısı hipotezi ([DergiPark](https://dergipark.org.tr/en/pub/ausbf/article/571826)).
- Hüküm: büyüklük %2–4, olay sayısı yılda birkaç düzine; dönem değişiklikleri önceden tahmin edilebildiği için (piyasa değeri/dolaşım sıralaması) "beklenen çıkışı önceden short (VİOP-47 içindeyse) / beklenen girişi yürürlükten sonra sat" kuralı mantıklı ama 2017 sonrası test yok. MSCI/FTSE dengelemeleri için BIST'e özgü kanıt bulunamadı (arama bütçesi).

### 5.8 Bilanço sonrası sürüklenme (PEAD)
Ahlatçıoğlu & Okay (2021), *Borsa Istanbul Review* 21: 2007–2018, 6.471 firma-çeyrek; yüksek−düşük sürpriz farkı **+2,9%** (zaman serisi SUE) / +2,2% (duyuru getirisi) [2,61] gün; analist örnekleminde +2,9%; çok faktörlü modeller açıklamıyor; küçük firmada daha güçlü ([Boğaziçi tezi](https://digitalarchive.library.bogazici.edu.tr/handle/123456789/16829), [EconBiz](https://www.econbiz.de/Record/post-earnings-announcement-drift-evidence-from-turkey-ahlatc%C4%B1o%C4%9Flu-aykut/10012816435)). Long-short ~%2,9/60 gün → yılda 4 çeyrekle brüt ~%12 (short bacak çoğu hissede yok). Long-only versiyonda yarısı kalır. Swing ufkuna uyumlu ama tek başına küçük; momentum ile birleştirilebilir.

### 5.9 Kredi notu değişiklikleri, PPK günleri, SPK/Borsa tedbirleri (VBTS, brüt takas, kredili işlem yasağı)
Bu başlıklarda arama bütçesi bittiği için literatür taranamadı; kendi testim de yok (olay tarihleri gerekiyor). Borsa İstanbul'un volatilite dönemlerinde tekil hisselere açığa/kredili işlem yasağı getirdiği biliniyor ([CNBC-e örneği](https://www.cnbce.com/borsa/borsa-istanbuldan-uc-hisseye-kredili-islem-yasagi-g33738)). Hüküm: test edilmedi; mekanizma olarak tedbir sonrası likidite düşer, kredili alıcı çekilir → kısa vadeli negatif sürüklenme beklenir, ama kanıt yok.

---

## 6. Akımlar

- **Yabancı akımı:** Ülkü & İkizlerli (2012), *Emerging Markets Review*: yabancılar İMKB'de aylık frekansta **negatif geri besleme** (yerel getiri düşünce alıyor), yalnız yükselen piyasada ve makro istikrarsızlıkta; **net yabancı akımı piyasa getirisini öngörüyor ama tekil hisse getirisini öngörmüyor**; fiyat etkileri kalıcı ([EconBiz](https://www.econbiz.de/Record/the-interaction-between-foreigners-trading-and-emerging-stock-returns-evidence-from-turkey/10009676059)). Ülkü & Weber (2011): günlük frekansta pozitif, aylıkta negatif geri besleme. Hüküm: endeks düzeyinde zamanlama girdisi olabilir; hisse seçimi için değil. Kendi testim yok (MKK/Borsa yabancı payı serisi indirilmedi).
- **AKD / takas izleme:** Tiniç & Salih (2019), *Applied Economics* 52(13), 03.2005–04.2017 tüm hisseler: bilgili işlem olasılığı (PIN) ile gelecek getiri arasında **anlamsız** ilişki ([TEDÜ Avesis](https://avesis.tedu.edu.tr/yayin/addb0698-c56a-492c-b751-360645ffdf84/informed-trading-order-flow-shocks-and-the-cross-section-of-expected-returns-in-borsa-istanbul)). Aracı kurum ağ merkeziliği ile beklenen getiri (Tiniç, Şensoy, Demir, Nguyen 2026, *Annals of OR*): 03.2005–11.2015, iki tarafı kurum kimlikli işlem verisi; merkezi yatırımcılar bilgi olaylarında erken işlem yapıyor ([Springer](https://link.springer.com/article/10.1007/s10479-026-07082-4); ayrıntı doğrulanmadı). **Kamuya açık gün sonu AKD/takas verisini "büyük kurum topluyor" diye izlemenin karlı olduğunu gösteren hakemli kanıt bulamadım.** Bu iddia anekdot düzeyinde; survivorship ve sonradan anlatı ("şu kurum topladı, yükseldi") yanlılığına çok açık.
- **Kredili işlem:** TSPB verisine göre kredili işlem hacmi 2018 1,8 → 2020 6,8 → 2021 11,4 → 2022 sonu 28 mlr TL ([Ekonomi Gazetesi](https://www.ekonomigazetesi.com/finans/kredili-islem-hacminde-2022de-rekor-kirildi-4637)); kredili işlem faizi %80–85'e, dönem dönem %100'e yaklaştı. Öngörü gücünü test eden çalışma bulunamadı. Mekanizma olarak zorunlu kapanışlar düşüşleri derinleştiriyor (3.3'teki kısa vadeli devamın bir kaynağı).
- **TEFAS hisse fonu akımları:** test edilmedi. Not: 15.09.2026 Pusula Portföy temerrüdü ve ~131 fonun tasfiyesi sonrası Ekim 2026'nın ilk haftasında PPF şemsiye ortalaması −%3,02 (fiyatlama anomalisi; bir fonda −%99,9) görüldü ([Borsagündem haftalık tablo](https://www.borsagundem.com.tr/yatirim-fonlarinda-haftalik-hacimler-en-cok-kazandiranlar)). Yani "risksiz" engelin kendisi de 2026'da tam risksiz değil.

---

## 7. Mevsimsellik (kendi testim, XU100 log getiri, 2005–2026)

{{SEASON}}

Literatür: Białkowski, Etebari & Wisniewski (2012), *JBF*: 14 Müslüman ülke 1989–2007, Ramazan'da getiri yüksek ve oynaklık düşük ([UNH](https://findscholars.unh.edu/display/publication147703)); Özkan & Akbalık (2018): İslami takvim etkileri hesaba katılınca BIST'te anormal getiri elde etmek güçleşmiş ([DergiPark jyasar](https://dergipark.org.tr/tr/pub/jyasar/article/306186)). Benim testimde Ramazan etkisi yok (2016–26: 3 bps vs 11 bps dışarıda).

Hüküm: ay dönümü (son gün + ilk 3 gün) 2005–26'da t≈2,0, 2016 sonrası t≈0,9; tek başına strateji olarak 2023–26'da nakdin altında. Tatil (bayram) öncesi gün 2016 sonrası **negatif** (−35 bps, t=−2,6, n=75; çoklu test riski yüksek). Mevsimsellik strateji düzeyinde getiri kaynağı değil; en fazla giriş-çıkış zamanlaması ayarı.

---

## 8. VİOP'a özgü

### 8.1 USDTRY vadeli short (TL carry) — 2023 ortasından beri en yüksek risk-ayarlı getiri, tarihsel olarak en büyük kuyruk riski

Kendi hesabım: aylık yenilenen kısa USDTRY vadeli; vadeli fiyatı = spot × (1+r_TL)/(1+r_USD) (r_TL = TCMB politika faizi; VİOP'ta gerçekleşen örtük faiz bundan farklı olabilir), r_USD ≈ Fed funds yıllık ortalama. "1x fazla" = TL'nin USD'ye karşı carry getirisi (notional başına). "Toplam TL Lx" = teminat TL nakitte + L kat notional.

{{CARRY}}

{{CARRY_YORUM}}

Dış kaynaklar: Kuveyt Türk Portföy: 2024'te TL PPF ortalaması ~%53, TL USD'ye karşı ~%19,7 değer kaybı → net USD getiri ~%28; 2025'in ilk 4 ayında fon %13,2, TL −%8,8 → net ~%4,1 ([Kuveyt Türk Portföy](https://www.kuveytturkportfoy.com.tr/en/blog-news/finance/wealth-insights-q3-2025-outlook-views-from-kuveyt-turk-portfoy-on-the-carry-tra/)). Bloomberg: Ocak 2025'e kadar 6 ayda USD fonlamalı TL carry ortalaması %15, en yakın rakibin (ARS) ~2 katı ([BNN Bloomberg](https://bnnbloomberg.ca/business/2025/01/08/best-em-carry-trade-boosted-by-turkeys-inflation-proofed-lira)). Mart 2025 şokunda Barclays: TL long pozisyonlarda 4 aydan fazla getiri 24 saatte silindi ([IFR](https://www.ifre.com/rates/2248088/investors-suffer-heavy-losses-in-popular-turkey-carry-trade)). Mart 2026'da İran savaşı sonrası ilk iki haftada ~12 mlr $ carry çıkışı; Ekim 2026'da TL ~50/$ rekor düşük, TCMB müdahaleyle kontrollü değer kaybı ([Trading Economics](https://tradingeconomics.com/turkey/currency/news/594227); ikincil kaynak, tarih tutarsızlıkları var).

### 8.2 Endeks vadeli baz / short'un taşıma avantajı
Yüksek faizde XU030 vadelisi spot×(1+r) civarında fiyatlanır. Bu nedenle **vadeli short pozisyonu nakit getirisi + (nakit − endeks) kazanır**: 2024–26'da endeks nakdin gerisinde kaldığı için short vadeli + teminat PPF, "2×nakit − endeks" getirisi verdi. 4. bölümdeki L/S trend sonuçlarının 2023–26'daki üstünlüğü büyük ölçüde bu taşıma etkisi. Önceki çalışmadaki baz sıçraması dönüşü +14–20 bps/işlem ile mikro düzeyde kaldı. Takvim yayılımı (yakın/uzak vade) saf faiz beklentisi pozisyonudur; ayrı test yapılmadı.

### 8.3 XU030 opsiyon volatilite risk primi
BIST30 opsiyonlarında örtük–gerçekleşen vol primini ölçen çalışma bulunamadı (yalnız model karşılaştırmaları: METU tezleri, [Akyapı & Küçükşenel 2014](https://open.metu.edu.tr/handle/11511/23613)). Opsiyon fiyat geçmişi elimde yok, test edilmedi. Uygulama riski: düşük likidite, piyasa yapıcı spreadi, ±%10 limitli gap'ler; Eylül 2026'daki %22'lik düşüş gibi olaylarda çıplak put satıcısı birkaç yıllık primi tek ayda verir. Hüküm: bireysel için **satış tarafı önerilmez**; alım tarafı (kriz hedge'i) pahalı ama portföy düzeyinde carry/trend pozisyonlarını korumak için anlamlı olabilir.

### 8.4 Altın vadelileri
Ayrı test yapılmadı. Önceki çalışmada TRALT ← altın öncülüğü test edilmişti. XAUTRY vadelisi TL faizini içinde taşır (long altın vadeli + teminat PPF = altın TL getirisi); XAUUSD vadelisi %10 stopajlı. Altın, TL carry pozisyonunun doğal kuyruk hedge'i (TL şoklarında XAUTRY yükselir).

---

## 9. Göreli değer

### 9.1 Holding iskontosu / holding–iştirak oranı ortalamaya dönüş (kendi testim)

Kurulum: log(holding) − log(iştirak sepeti, günlük eşit ağırlık); z = (oran − L günlük ortalama)/std; |z| ≥ 2'de karşı yönde gir, H gün tut, örtüşmesiz. Getiri = göreli log getiri (brüt).

{{RV}}

{{RV_YORUM}}

Not: Bu NAV iskontosu değil, holding fiyatının iştirak fiyatlarına göre kısa vadeli sapması. Gerçek NAV iskontosu (KCHOL/SAHOL/DOHOL/ALARK) için aracı kurum NAV serileri gerekiyor; arama bütçesi bittiği için bulunamadı. Gökçen (2026) değer faktörünün BIST'in en güçlü faktörü olduğunu bulduğu için yüksek iskontolu holdingler yavaş (6–24 ay) bir değer pozisyonu; swing ufkuna değil, kümelenme çekirdeğine uygun.

### 9.2 A/B pay sınıfları (KRDMA/KRDMB/KRDMD) ve grup hisseleri
KRDMA/KRDMD ve KRDMB/KRDMD oranlarında ortalamaya dönüş **yok** (tabloda t mutlak değeri < 1,3; en kötü işlemler −%30…−%66). KRDMB trend yapıyor; A ve B sınıfları sığ, oran kalıcı kayıyor. TRALT/TRMET oranında 20–60 gün ufkunda istikrarlı dönüş yok (önceki çalışmadaki göreli momentum bulgusuyla tutarlı: Koza grubunda oran trend yapıyor, dönmüyor).

---

## 10. Dürüst hüküm: hangisi %36–40 TL engelinin belirgin üstüne çıkabilir?

{{HUKUM}}

---

## 11. Doğrulayıcı için açık noktalar ve sınırlamalar

{{SINIR}}

---

## 12. Kaynaklar (kullanılanlar)

{{KAYNAK}}
