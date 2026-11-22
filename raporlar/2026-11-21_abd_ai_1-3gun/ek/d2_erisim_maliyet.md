araç: 40/30 (kontrol noktası geçildi: SPK bülteni ve GİB rehberi PDF olarak geldi, metin çıkarma gerekti; SPK'nın Haziran 2026 banka kararı yeni ve sonuca etkili bir bulguydu)

# D2 · Türkiye'den ABD hisse/ETF erişimi: kanallar, maliyet, kısıtlar, vergi

## Özet

**Kanallar.** Türkiye'de yerleşik bir kişi ABD hisse ve ETF'lerine üç yoldan ulaşır: (1) SPK yetkili aracı kurum (Midas Menkul, İş Yatırım TMI (Saxo altyapısı), Garanti BBVA Yatırım, Dinamik Menkul (Interactive Brokers TWS altyapısı) vb.); (2) banka uygulamaları, ama **SPK 17.06.2026 tarihli ilke kararıyla bankalar yurt dışı pay emirlerine artık doğrudan aracılık edemiyor**; banka yalnız yetkili aracı kuruma hesap açtırabiliyor ya da emri ona iletebiliyor; (3) yurt dışı kurumda kendi girişimiyle hesap (ör. Interactive Brokers). Üçüncü yolda SPK lisansı ve Türk yatırımcı koruması yok. Hesap açılabildiğine dair kanıt yalnızca ikincil kaynaklardan geliyor (çelişkili kullanıcı deneyimleri var). IBKR'ye özel bir SPK erişim engeli bulunamadı. SPK'nın engelleri kaldıraçlı forex/CFD ve kripto sitelerine yönelik.

**Maliyet (gidiş-dönüş, komisyon).** Bu oturumda görülen tarifeler:
| Kanal | Komisyon | 5.000 $ | 20.000 $ |
|---|---|---|---|
| Midas | 1,5 $ işlem başı, sabit | 6 bps | 1,5 bps |
| IBKR Pro Fixed (doğrudan ya da Dinamik) | 0,005 $/hisse, asgari 1 $, en çok %1 | ~2–4 bps* | ~2 bps* |
| İş Yatırım TMI | %0,25 (asgari borsaya göre); seans dışı +0,5 ¢/hisse | 50 bps | 50 bps |
| Garanti BBVA Yatırım | binde 3, ABD'de asgari 0 $ | 60 bps | 60 bps |
| Banka kanalları (İşCep vb.) | 06/2026'dan sonra aracı kuruma yönlendirme | doğrulanmadı | doğrulanmadı |
*50 $'lık hisse varsayımı (kendi hesabım). Dinamik Menkul'ün kendi tarifesi görülmedi.

Bunlara alış-satış makası eklenir. Kendi tahminim, doğrulanmadı: büyük ETF ve dev hisselerde 1–3 bps, SOXL'de 2–5 bps. VIX 35 civarında bu makas 2–3 katına çıkabilir. **Kur çevirme makası işlem başına değil, para hesaba girerken ve çıkarken bir kez ödenir.** Dolar hesapta tutulursa 1–3 günlük işlemlerin maliyetine girmez. Hiçbir kurumda TL↔USD makas oranı yayımlanmış bulunamadı.

**Backtest varsayımları.** 5.000 $ pozisyonda Midas ile 10 bps (dev şirket ve büyük ETF) gerçekçi, hatta biraz cömert (6 bps komisyon + makas). Ancak çok oynak kapanışlarda dar kalabilir; 15 bps duyarlılık testi önerilir. 20 ve 40 bps makul. "Oransal +50 bps" İş Yatırım ile tutarlı. Garanti'de bu rakam 60 bps.

**Emir türleri.** Midas'ta piyasa, limit, stop ve stop-limit emirleri ile seans öncesi/sonrası işlem var. MOC/LOC (kapanış müzayedesi emri) için Midas'ta kanıt bulunamadı. IBKR'de MOC/LOC var (kendi bilgim, bu oturumda sayfa açılamadı, 403). Kaldıraçlı ETF'ler (SOXL, SOXS, TQQQ, NVDL): SPK ETF'leri kaldıraçlı işlem tebliği kapsamı dışında tutuyor (kripto dayalı olanlar hariç). Yine de her kurumdaki listeleme ve uygunluk testi teyit edilemedi.

**Vergi (GİB 2026 rehberi).** Yurt dışı borsada hisse/ETF alım-satım kazancı GVK mükerrer 80 kapsamında değer artışı kazancıdır. Tutarı ne olursa olsun yıllık beyannameyle bildirilir: menkul kıymete istisna yok (2026 genel istisnası 150.000 TL, menkul kıymetlere uygulanmıyor). Yİ-ÜFE artışı %10 ve üzerindeyse maliyet endekslenir. Aynı yıl içinde zarar kârdan düşülebilir; diğer gelirlerden düşülemez. Kur farkı TL kazanca dahildir. ABD temettü stopajı: IRS anlaşma tablosuna göre genel oran %20, nitelikli doğrudan iştirak için %15. Midas örneğindeki %15 bireyler için yanıltıcı.

## İddia defteri

| # | iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven |
|---|---|---|---|---|
| 1 | Midas ABD işlem ücreti sabit 1,5 $ | https://www.getmidas.com/ucretler/ | "1,5 USD*" | yüksek |
| 2 | Midas'ta 1 $ altı hisselerde ek ücret | https://www.getmidas.com/ucretler/ | "300 adet üstü alım ve satımlarda" her ek adet 0,005 $ | yüksek |
| 3 | Midas'ta kesirli hisse var, hesap işletim ücreti yok | https://www.getmidas.com/ucretler/ | "Parça Hisse … Var"; hesap işletimi ücretsiz | yüksek |
| 4 | Midas ACATS çıkış ücreti (iki sayfa çelişiyor) | https://www.getmidas.com/ucretler/ | "tam veya kısmi ACATS transferleri için 25 USD" (destek sayfası özeti 100 $ diyor) | orta |
| 5 | Midas piyasa/limit fark etmeksizin emir başı 1,5 $ | https://www.getmidas.com/destek/amerikan-borsalari/alim-satim-islemleri-ve-emirler | piyasa ya da limit "her bir emir için yalnızca 1,5 dolar" | orta (arama özeti) |
| 6 | Midas'ta piyasa kapalıyken piyasa emrine %3 marj (tampon) | https://www.getmidas.com/destek/amerikan-borsalari/alim-satim-islemleri-ve-emirler/abd-borsalari-piyasa-emirlerindeki-marj-kurali-nedir | piyasa kapalıyken %3, stop emirde %2,5 | orta (arama özeti) |
| 7 | Midas'ta seans öncesi/sonrası işlem var | https://www.getmidas.com/midas-akademi/abd-acilis-oncesi-islemler-ve-kapanis-sonrasi-pre-market-post-market-nedir/ | "Midas'ta açılış öncesi ve kapanış sonrası işlemler yapabilirsin." | orta (arama özeti) |
| 8 | İş Yatırım TMI ABD pay komisyonu %0,25, asgari borsaya göre | https://www.isyatirim.com.tr/tr-tr/destek/Documents/pdf/komisyon-ve-masraf-tarifesi.pdf | "%0,25 (onbinde yirmi beş) oranında komisyon tahsil edilir" | yüksek |
| 9 | İş TMI'da seans dışı/ALGO emre ek hisse başı ücret | aynı | "pay adedi başına 0,5 (onda beş) cent üçüncü kişi kurum masrafı" | yüksek |
| 10 | İş TMI yurt dışı işlemleri Saxo Bank üzerinden | https://www.isyatirim.com.tr/tr-tr/Sayfalar/SSS.aspx | TMI işlemleri "Saxo Bank aracılığı ile" | orta (arama özeti) |
| 11 | İş tarifesinin tarihi 28.08.2026 | aynı PDF | "KMT-28082026-20" | orta (kod yorumu benim) |
| 12 | Garanti BBVA Yatırım ABD komisyonu binde 3, asgari yok | https://www.garantibbvayatirim.com.tr/tr/ucret-ve-komisyonlar | ABD binde 3, minimum 0 USD | orta (arama özeti) |
| 13 | Garanti ürün sayfası: ABD'de asgari komisyon yok | https://www.garantibbva.com.tr/yatirim/yurt-disi-hisse-senedi-islemleri | "ABD Borsalarında Minimum Komisyon Ücreti Yok" | orta |
| 14 | IBKR Pro Fixed: 0,005 $/hisse, asgari 1 $, en çok %1 | https://www.interactivebrokers.com/en/pricing/commissions-home.php | USD 0.005/share, min USD 1.00, max 1% of trade value | orta (sayfa 403, arama özeti) |
| 15 | Dinamik Menkul, IBKR TWS üzerinden yurt dışı işlem sunuyor | https://www.dinamikmenkul.com.tr/page/islem-platformlari/interactive-brokers | "Interactive Brokers, müşterilere işlem aracılığı ve takas hizmetleri sunar" | orta |
| 16 | SPK: bankalar yurt dışı pay emrine doğrudan aracılık edemez | https://spk.gov.tr/data/6a3300ca8f95db19fcfc205f/2026-39.pdf | "Mevduat veya katılım bankaları yurt dışında paylar … için emir iletimine aracılık faaliyetinde bulunamazlar." | yüksek |
| 17 | Kararın künyesi | aynı | "i-SPK.37.9 (17/06/2026 tarih ve 37/1118 s.k.)" | yüksek |
| 18 | Banka, yetkili aracı kuruma hesap açtırabilir ya da emir iletebilir | aynı | "hesap açmalarına aracılık etmeleri ya da bu kurumlara emir iletmeleri mümkündür" | yüksek |
| 19 | Yabancı ETF işlemleri "Tebliğ" kapsamı dışında; kripto dayalılar saklı | aynı | "yabancı borsalarda işlem gören borsa yatırım fonlarına ilişkin alım satım işlemlerinin Tebliğ kapsamında olmadığı" | yüksek (hangi tebliğ: doğrulanmadı) |
| 20 | SPK erişim engelleri izinsiz kaldıraçlı işlem sitelerine yönelik | https://t24.com.tr/ekonomi/spk-16-siteye-erisim-engeli-getirdi,1255552 | yurt dışında izinsiz kaldıraçlı işlem yapan 16 site | orta |
| 21 | Yurt dışı borsa kazancı değer artışı olarak beyan edilir | https://intvrg.gib.gov.tr/hazirbeyan/assets/pdf/DUYURU_UNIVERSAL_2026_Diger_Kazanc_ve_Iratlar_2026.pdf | "değer artışı kazancı olarak yıllık gelir vergisi beyannamesi ile beyan edilmesi gerekmektedir" | yüksek |
| 22 | Menkul kıymete değer artışı istisnası yok; 2026 genel istisna 150.000 TL | aynı | "Menkul kıymet … hariç … 2026 takvim yılı için istisna tutarı 150.000 TL" | yüksek |
| 23 | Yİ-ÜFE endekslemesi için artış %10 ve üzeri olmalı | aynı | "artış oranının %10 veya üzerinde olması gerektiği" | yüksek |
| 24 | Aynı yıl içinde menkul kıymet zararı kârdan düşülür | aynı | "beyan edilecek kazancın hesabında zararın kardan mahsup edilmesi mümkündür" | yüksek |
| 25 | Değer artışı zararı diğer gelir unsurlarından düşülemez | aynı | "diğer gelir unsurlarından … mahsubu ise mümkün bulunmamaktadır" | yüksek |
| 26 | 2025 gelirleri 1–31 Mart 2026'da beyan edildi | aynı | "1-31 Mart 2026 Tarihleri Arasında" | yüksek |
| 27 | Alış ve satış o günün kuruyla TL'ye çevrilir; kur farkı vergilenir; beyan sınırı yok | https://www.yapikredi.com.tr/medium/file/yabanci-hisse-senedi-gelirlerinde-2026-yili-vergi-durumu_71999/view | "Kur farkları vergiye tabidir." / "herhangi bir vergi istisna tutarı veya yıllık beyan haddi aşılması şartı yoktur" | orta (banka notu, resmî değil) |
| 28 | Yabancı temettü beyan sınırı 2026'da 22.000 TL | aynı | "beyan sınırı 2026 yılı itibarıyla 22.000 TL'dir" | orta (banka notu) |
| 29 | ABD–Türkiye anlaşması temettü stopajı: genel %20, nitelikli %15 | https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf | Turkey … Dividends General "20", Direct "15" (Rev. May 2023) | yüksek |
| 30 | ABD stopajı Türkiye'de mahsup edilir; 1042-S apostil gerekir | https://www.getmidas.com/destek/amerikan-borsalari/vergilendirme/amerikan-borsalarindaki-temettu-odemelerinde-amerikada-kesilen-stopaji-turkiyede-vergi-beyan-ederken-mahsup-edebilir-miyim | "1042-S vergi belgesinin apostil veya tasdik işlemlerinin yapılması gerekmektedir" | orta |

## Listede olmayan önemli bulgular

- **SPK 17.06.2026 banka kararı (defter 16–18).** Garanti BBVA'nın banka uygulaması, İşCep ve Yapı Kredi'nin banka kanalı gibi yollar artık yalnızca yetkili aracı kuruma yönlendirme yapabilir. Kanal listesinde "banka" değil "aracı kurum" esas alınmalı. Global Menkul de yurt dışı emir iletimi yetkisi için SPK'ya başvurdu (arama özeti, doğrulanmadı).
- **Dinamik Menkul, IBKR altyapısını SPK lisanslı kurum çatısı altında sunuyor.** Doğrudan yabancı hesaba göre düzenleyici açıdan daha güvenli bir MOC/LOC yolu olabilir. Dinamik'in kendi komisyonu görülmedi.
- **Kripto dayalı ETF'ler (ör. spot bitcoin ETF) SPK kararında saklı tutuluyor.** Yani muhtemelen yasak; kaldıraçlı hisse ETF'leri kapsam dışında.
- **Midas'ta piyasa kapalıyken verilen piyasa emrine %3 tampon blokesi uygulanıyor.** Kapanışa yakın tam bakiye kullanımını etkiler.
- **Kur farkı vergisi.** TL bazlı kazançta kur farkı da vergilenir. Dolar bazında zarar edilse bile TL bazında vergi çıkabilir.

## Listeyle çelişen kanıt

- **Garanti BBVA Yatırım "oransal, asgari tutarlı" değil.** Resmî sayfalarda ABD için asgari 0 $ yazıyor; yalnızca karekod.org blogu 15 $ asgari diyor.
- **Midas ACATS ücreti iki resmî sayfada farklı:** 25 $ ve 100 $.
- **Midas destek örneğinde ABD temettü stopajı %15 kabul ediliyor; IRS tablosu bireyler için genel oranı %20 veriyor.** Not: IRS tablosu Mayıs 2023 tarihli.
- **"Yabancı hisseye beyan sınırı/istisna var" düşüncesi yanlış.** GİB rehberine göre menkul kıymet kazancına istisna yok; her tutar beyan edilir.

## Açık kalanlar

- **MOC/LOC:** Midas, İş TMI (Saxo) ve Garanti'de verilip verilemediği doğrulanmadı. IBKR'de var (kendi bilgim, sayfa 403 döndü).
- **SOXL, SOXS, TQQQ, NVDL ve yeni halka arzlar:** Midas, İş ve Garanti'de listelenip listelenmediği doğrulanmadı. Uygunluk testi ya da karmaşık ürün kısıtı da bilinmiyor.
- **Kesirli hisse, açığa satış ve marj:** Midas dışındaki kurumlarda doğrulanmadı. Midas yurt içi açığa satış sayfasının ABD tarafına uygulanıp uygulanmadığı okunmadı.
- **Kur makası:** Hiçbir kurumun TL↔USD makası bulunamadı.
- **Alış-satış makası tahminleri:** Kendi tahminim.
- **SEC/FINRA satış ücretleri:** Doğrulanmadı.
- **IBKR'nin Türkiye'den hesap kabulü:** Resmî kanıtı yok, yalnız ikincil kaynaklar var.
- **IBKR'nin SPK açısından durumu:** SPK'nın bu konudaki tutumu (yerleşik kişinin kendi girişimiyle hesap açması) resmî metinden okunmadı.
- **Diğer kurumlar:** Ak Yatırım, Yapı Kredi Yatırım, Gedik, Deniz ve Ziraat tarifeleri bu turda açılmadı.
- **Değer artışı zararının sonraki yıla devri:** Rehberde açık hüküm görülmedi; devredilemediği yaygın görüş ama doğrulanmadı.
- **Gelir vergisi tarifesi:** 2026 dilimleri doğrulanmadı.
