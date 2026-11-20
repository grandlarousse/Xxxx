# M1 yöntem denetimi (hesap öncesi)

Veri görülmedi; "doğrulanmalı" notlu olgular piyasa yapısı ajanınındır.

## ZORUNLU

**Z1 Kıyas ölçütü tek olsun (§3).** "Ya da" seçim serbestliği veriyor; tam örneklem ortalaması geleceği içeriyor, kayma da dönemden döneme değişiyor.
Ekle: "Kesit sinyalleri (A1, A3, A8): kıyas aynı gün, hedef hariç, dolabilir üyelerin eşit ağırlıklı f_h'i. Zamanlama sinyalleri (A2, A4, A5, A6): kıyas hedefin t−1'e kadarki 250 günlük ortalama f_h'i. Spot AL için ham net getiri eksi TLREF de raporlanır."

**Z2 Meta veride gelecek (§1, §4).** Bugünkü piyasa değeri, hacim ve fiyat adımıyla geçmişi sıralamak ileriye bakmadır.
Ekle: "Büyüklük/hacim grupları t−1'e kadarki 60 günlük medyan TL hacimle kurulur. tick_bps o günün düzeltilmemiş fiyatından hesaplanır. VİOP bacağı kontratın listelendiği tarihte başlar. β için en az 60 gün; yoksa β=1."

**Z3 Kilit tespiti ve sepetler (§3).** Düzeltilmiş fiyat ve sabit %10 kilidi yanlış saptar; kilitli üyenin kesilen getirisi ertesi güne taşıp sepette sahte öncülük üretir.
Ekle: "Kilit: düzeltilmemiş kapanış gün içi en yükseğe eşit ve getiri o tarihteki marjın en çok 2 adım altında. Tarihsel marj değişiklikleri (2020 öncesi; doğrulanmalı) tabloya yazılır. |r| > marj günleri kurumsal işlem/veri hatası sayılır, elenir. Hedef sepet f_h'i yalnız t'de dolabilir üyelerden hesaplanır. Halka arz hisseleri ilk 20 gün ya da ilk tavansız kapanışa kadar (hangisi geçse) hedef, kaynak ve sepet dışıdır."

**Z4 Giriş gecikmesi testi (§3, §5).** Sinyal kapanış fiyatını içeriyor; bayat fiyat ve alış-satış sıçraması bu kurguda sahte öncülük ve dönüş üretir.
Ekle: "Her aday t+1 açılışı ve t+1 kapanışı girişiyle de verilir. f1'in %70'inden fazlası gece boşluğundaysa kural 'kapanış dolumuna bağımlı' etiketlenir; A7'de kapanış seansı hacmiyle dolum gösterilmeden aday olamaz. A3'te t+1 kapanışı varyantında işaret korunmalıdır."

**Z5 OOS-1 sızıntısı (§2).** Sekiz ajan OOS-1'i görürse şart 2 ikinci seçim turuna döner; boş kural aynı yön ve t≥1,5'i ~%7 olasılıkla geçer.
Ekle: "panel_dev, panel_is ve panel_oos1 olarak ayrılır. Ajanlar yalnız IS'i görür, en çok 5 dondurulmuş kural yazar. OOS-1 tek ortak betikle (kod/ortak/) bir kez hesaplanır. Dolum, kıyas, kümeleme ortak kütüphaneden gelir."

**Z6 Birincil hipotez sayısı (§5).** A1 ızgarası ~60 bin test; önceki çalışmada 157 bin testten geçen olmadı.
Ekle: "Tüm ailelerde toplam en çok 30 önceden yazılı, havuzlanmış birincil test vardır; BH bunlara aileler birlikte uygulanır. Çift düzeyi ızgara keşif amaçlıdır. A8'de her model yapılandırması bir test sayılır; hiperparametre yalnız IS'te seçilir."

**Z7 Kasa protokolü ve güç (§2).** ~350 günde seyrek sinyal doğrulanamaz; başarısızlık güçsüzlükten ayrılmalı.
Ekle: "Kasaya en çok 10 kural girer: tek çalıştırma, tek yönlü test, Holm düzeltmesi. %80 güç için yaklaşık olay sayısı (σ≈%3 varsayımıyla): brüt 40 bps → ~350, 75 bps → ~100; ~40 olayla ancak ≥ ~120 bps saptanır. Sonuç: doğrulandı, güç yetersiz (kâğıt izleme) ya da çürütüldü."

**Z8 A7 verisi kasayla örtüşüyor (§6).** Son ~2 yılın saatlik verisi 2025-07 sonrasını içerir.
Ekle: "Saatlik panel 2025-06-30'da kesilir. A7 aday üretmez; zamanlama ve dolumu doğrular."

**Z9 VİOP uzlaşması işlem fiyatı değil (§3, A6).** Önceki çalışmada uzlaşma kapanış hareketinin ~%50'sini izledi; baz sinyali mekanik "öngörü" üretir.
Ekle: "VİOP girişi spot kapanışı belli olduktan sonraki son işlem fiyatıdır (saat doğrulanmalı); o gün hacim yoksa ya da kontrat limitteyse dolmaz."

## ÖNERİLİR

**Ö1 Maliyet (§4).** Önceki notta bireysel VİOP komisyonu bacak başına ~22 bps; temel 15–18 bps bununla çelişiyor.
Ekle: "Karar senaryosu kullanıcının gerçek komisyonudur; bilinmiyorsa muhafazakâr sütun. Pozisyon 20 günlük medyan TL hacmin %1'ini aşmaz."

**Ö2 Olay sayısı (şart 4).** 40 olayda standart hata ~47 bps; yalnız şişkin etkiler geçer.
Ekle: "En az 100 bağımsız olay günü (aralarında ≥ h gün), en az 30'u OOS-1'de. Küme sayısı 50'den azsa p-değeri permütasyondan alınır."

**Ö3 Eşit olmayan panel (§5).** IS'te üyelerin çoğu henüz halka açık değil; kural başka bir evrende seçiliyor.
Ekle: "Günler eşit ağırlıklıdır; günde en az 5 dolabilir hisse aranır. Sonuçlar 2021 öncesi ve sonrası listelenenler için ayrı verilir."

**Ö4 Yön (§6).** Spotta açığa satış yok.
Ekle: "Spot hedefte yalnız AL kuralları aday ailesine girer; SAT yalnız AKSEN/ENJSA/ODAS vadelisinde."

**Ö5 VBTS tedbirleri (§3).** Brüt takasta alınan pay takas bitmeden satılamaz, h=1 çıkışı olmaz (doğrulanmalı).
Ekle: "Tedbir tarihleri bulunursa o hisse-günler dolmaz sayılır; bulunamazsa sınır olarak yazılır."

## İSTEĞE BAĞLI

**İ1 Eksik aileler:** (a) ana ortaklık/grup çiftleri, ~10 önceden yazılı çift, hata düzeltme (örn. NATEN–ESEN–MAGEN, ODAS–CANTE, AHGAZ–ENERY; KAP'tan doğrulanmalı); (b) tavan serisinin bitişi ve yeni elektrik halka arzının ilk günü → akranlar; (c) kapanış seansı göreli sapması: (kapanış/17:55 − 1) − sektör → ertesi gün dönüş.
