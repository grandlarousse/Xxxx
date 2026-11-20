# YONTEM_EK: denetim ve 1. dalga sonrası düzeltmeler (hesaptan önce)

Bu ek, `YONTEM.md` ile çelişen her noktada geçerlidir. Kaynak: `ek/M1_yontem_denetimi.md` (yöntem denetimi), `ek/maliyet.md` (piyasa kuralları), `ek/R3_xelkt_tv_ham.md`.

## E1. Kör protokol (en önemli değişiklik)

- 2. dalga analiz ajanları **yalnız IS dönemini** görür: `panel_is/` (son tarih 2022-12-30). OOS-1'i (2023-01-02 → 2025-06-30) ve kasayı (2025-07-01 →) görmezler.
- Her ajan en çok **4 birincil** ve en çok **6 ikincil** kuralı **dondurur** ve kod olarak teslim eder: `kod/<ajan>/rules.py` içinde `build(P)` fonksiyonu.
- OOS-1 sonuçlarını ana ajan tek ortak betikle (`kod/ortak/oos_degerlendir.py`) **bir kez** hesaplar. Kasa için de aynı betik kullanılır.
- Nedensellik denetimi otomatiktir: `build(panel_is)` ile `build(panel_dev)` IS tarihlerinde aynı sinyali üretmelidir. Üretmiyorsa kural geleceğe bakıyordur ve elenir.
- A7 (gün içi) aday üretmez: saatlik veri yalnız 2024 sonrasını kapsar. Görevi zamanlama ve dolum doğrulamasıdır; bulguları “keşif” etiketi taşır.

### `rules.py` sözleşmesi

```python
def build(P):
    """P = elib.load(panel_klasoru). Yalnız t ve öncesini kullan (shift/rolling; tam örneklem ortalaması, sıralaması, yüzdeliği YASAK).
    Eşik gibi IS'te seçilen sabitler sayı olarak koda yazılır; P'den yeniden kestirilmez."""
    return [
        {"ad": "A4_tavan_bulasma_h1",      # benzersiz kısa ad
         "sig": sig,                        # bool DataFrame, index=tarih, columns=hisse; True = t kapanışında pozisyon aç
         "h": 1,                            # 1, 2 ya da 3
         "yon": "long",                     # spot hedefte yalnız "long"; "short" yalnız AKSEN/ENJSA/ODAS ve arac="viop"
         "olcu": "own",                     # zamanlama kuralı: "own"; kesit (hisse seçimi) kuralı: "sec"
         "arac": "spot",                    # "spot" ya da "viop"
         "birincil": True,                  # en çok 4 birincil
         "aciklama": "tek cümle: girdi, eşik, hedef"},
    ]
```

## E2. Kıyas ölçütü tek ve önceden belli (Z1)

- **Kesit kuralları** (hisse seçimi: A1, A3, A8): kıyas = aynı gün, hedef hariç, **dolabilir** sektör üyelerinin eşit ağırlıklı f_h'i (`sec`).
- **Zamanlama kuralları** (sektör ya da tek hisse zamanlaması: A2, A4, A5, A6): kıyas = hedefin t'den önce tamamlanmış son 250 günlük ortalama f_h'i (`own`).
- İki ölçü de her satırda raporlanır; karar yukarıdaki eşlemeye göre verilir. Ham getiri yalnız bilgi içindir.

## E3. Geleceği içeren meta veri yasak (Z2)

- Büyüklük/hacim grupları t−1'e kadarki **60 günlük medyan TL hacim** ile kurulur (`elib.adv60(P)`). Bugünkü piyasa değeri, bugünkü fiyat ya da `xelkt_uyeler.csv`'deki ağırlıklar sıralama için kullanılamaz. Ana faaliyet kümeleri (dağıtım, termik, yenilenebilir…) sabit nitelik olduğu için kullanılabilir.
- Fiyat adımı maliyeti o günün ham fiyatından hesaplanır (kütüphane yapar).
- β için en az 60 gün; yoksa β = 1. VİOP bacağı kontratın listelendiği tarihte başlar (AKSEN 2022-11, ODAS 2021-04, ENJSA 2018-12).

## E4. Kilit, sepet ve halka arz (Z3)

- Kilit: ham kapanış = gün içi en yüksek ve fiyat o günkü tavan fiyatının en çok 2 adım altında (taban için simetrik). Marj 2020-03-13'ten itibaren ±%10, öncesi ±%20.
- Hedef sepetlerin ve kıyas sepetlerinin f_h'i **yalnız t günü dolabilir üyelerden** hesaplanır. Aksi hâlde tavanda kilitli üyenin ertesi güne taşan getirisi sahte öncülük üretir.
- Halka arz: hisse ilk 20 işlem günü **ve** ilk tavansız kapanışına kadar hedef, kaynak ve sepet dışıdır (`tradable` buna göre kurulur).
- XELKT endeksinin kendisi hedef olamaz (kilitli üyeleri içerir, alınıp satılamaz); yalnız girdi ve bilgi.

## E5. Giriş gecikmesi sınaması (Z4)

- Kütüphane her kural için üç giriş verir: t kapanışı (ana), t+1 açılışı, t+1 kapanışı.
- f_1'in gece (t kapanışı → t+1 açılışı) payı %70'i aşıyorsa kural “kapanış dolumuna bağımlı” etiketi alır; 3. dalgada kapanış seansı hacmiyle dolum gösterilmeden öneriye dönüşmez.
- Kesit geri dönüş kurallarında (A3) t+1 kapanışı girişinde işaret korunmalıdır; korunmuyorsa etki alış-satış sıçraması sayılır.

## E6. Çoklu test (Z6) ve olay sayısı (Ö2, Ö3)

- Birincil kurallar bütün aileler birlikte en çok 28'dir (7 aile × 4). Benjamini–Hochberg (q = 0,10) OOS-1 p-değerlerine **aileler birlikte** uygulanır (tek yönlü; yön IS'te dondurulmuştur).
- Çift düzeyi ızgaralar (A1) ve model taramaları (A8) keşiftir; ajan bunlardan en çok 4 birincil kural damıtır. A8'de her model yapılandırması bir kural sayılır.
- Aday için en az **100 bağımsız olay günü** (IS + OOS-1; aralarında ≥ h gün), bunların en az 30'u OOS-1'de. 40–100 arası olay “izleme listesi”nden öteye geçemez.
- Sepet kurallarında günde en az 5 dolabilir hisse aranır. Sonuçlar 2021 öncesi ve sonrası listelenen hisseler için ayrı da verilir.

## E7. Kasa protokolü (Z7)

- Kasaya en çok 10 kural girer; tek çalıştırma, tek yönlü test, Holm düzeltmesi.
- Güç (σ ≈ %3 günlük varsayımıyla, %80 güç için gereken olay sayısı): brüt 40 bps → ~350 olay; 75 bps → ~100; ~40 olayla ancak ≥ ~120 bps saptanır.
- Sonuç üç sınıftan biridir: **doğrulandı**, **güç yetersiz** (kâğıt üstünde izleme), **çürütüldü**.

## E8. VİOP (Z9) ve doğrulanan piyasa kuralları

- VİOP normal seansı **18:10**'da biter (18:15 değil). Pay vadelilerinde akşam seansı yok. Spot kapanış fiyatı ~18:05'te belli olur: vadelide işlem için 4–5 dakikalık pencere kalır.
- Günlük uzlaşma = 18:00–18:10 işlemlerinin miktar ağırlıklı ortalaması (10'dan az işlemde son 10 işlem). Uzlaşma bir işlem fiyatı değildir: vadeli P&L hem uzlaşmadan uzlaşmaya hem son fiyattan son fiyata verilir, karar **ikisinin kötüsüne** göre.
- Vadeli o gün hiç işlem görmediyse ya da ±%10 limitindeyse giriş dolmaz.
- Baz sinyalleri (A6) mekanik gecikme içerir (uzlaşma, spot kapanış hareketinin tamamını yansıtmaz); iki fiyat tanımında da pozitif olmayan baz kuralı aday olamaz.
- Spot: kapanış emir toplama 18:01–18:05, fiyat 18:05, kapanış fiyatından işlemler 18:08–18:10 (yalnız karşı tarafta bekleyen emir varsa). Tavanda kapanan hissede kapanışta alım dolmaz varsayılır.
- Vadeli fiyat adımı: 100 TL altı 0,01; 100–500 TL 0,05.
- Açığa satış yasakları (06/02/2023–01/01/2025; 24/03–29/08/2025; 02/03–26/06/2026) spot kısa pozisyonu zaten dışlıyor; VİOP kısa bacağı etkilenmez.

## E9. Maliyet (Ö1)

- Senaryolar (gidiş-dönüş, bps): spot 10 / **25** / 50; VİOP AKSEN 8 / **15** / 25, ENJSA 10 / **18** / 25, ODAS 25 / **35** / 45. Spot için ayrıca yarım fiyat adımı.
- Her kural için **başa baş maliyet** (işlem başına fazla getiri) verilir; kullanıcı kendi komisyonuyla karşılaştırır. Karar temel senaryoya göre; muhafazakâr senaryoda da ayakta kalanlar ayrıca işaretlenir.
- Kapasite: pozisyon hedefin 20 günlük medyan TL hacminin %1'ini aşmaz varsayılır.

## E10. Ek hipotezler (İ1) ve düzeltmeler

- A1'e: ana ortaklık/grup çiftleri önceden yazılı (NATEN–ESEN–MAGEN, ODAS–CANTE, AHGAZ–ENERY) ve çift farkının ortalamaya dönüşü (hata düzeltme).
- A4'e: tavan serisinin bittiği gün (art arda ≥ 2 tavandan sonra ilk tavansız kapanış) → akranlar; yeni bir elektrik halka arzının ilk işlem günü → akranlar.
- A7'ye (keşif): kapanış seansı göreli sapması, (kapanış / 17:50 fiyatı − 1) − sektör ortalaması → ertesi gün dönüş.
- Düzeltme: XELKT'yi izleyen bir fon var (Garanti Portföy Enerji Şirketleri Hisse Senedi Fonu, TEFAS kodu GNS); borsa yatırım fonu ve vadelisi yok.
- Bilinen sınır (Ö5): VBTS tedbirleri (brüt takas vb.) altındaki hisselerde h = 1 çıkışı yapılamayabilir. Tedbir tarihleri veri olarak yok; sınır olarak raporlanır.
