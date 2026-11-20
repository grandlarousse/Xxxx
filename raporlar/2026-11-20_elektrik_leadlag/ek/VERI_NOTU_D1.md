# VERİ NOTU D1 — günlük spot + endeks paneli

**Kapsam.** 46 hisse (42 XELKT üyesi + ASTOR, ALARK, EUPWR, GESAN) ve 7 endeks; 2010-01-04 → 2026-11-20, 4.238 işlem günü. Takvim: İş Yatırım'da XU100'ün işlem gördüğü günler (bayat 2013-01-01 satırı ve iptal edilen 2023-02-08 seansı hariç). `panel_dev` aynı dosyaların 2025-06-30'da kesilmiş hâlidir (40 hisse): ham veri önce kesilir, panel sonra kurulur; düzeltme çarpanı kesim gününe göre normalize edilir.

**Dosyalar**
- `px.parquet` (uzun): date, sym, o/h/l/c (düzeltilmiş), c_raw, o_raw/h_raw/l_raw, vol_tl, vol_adet (≈ vol_tl / ağırlıklı ortalama fiyat), mcap_tl, adjf (ham/düzeltilmiş çarpanı), ca (boş/div/cap), kaynak.
- Geniş matrisler (date × sym): `ret_cc`, `ret_co`, `ret_oc`, `vol_tl`, `close_raw`.
- Bayraklar: `lim_up`, `lim_dn` (kapanış günün ucunda ve baz fiyata göre getiri ≥ marj − max(%0,6; bir fiyat adımı)); `lim_up_touch`, `lim_dn_touch`; `lim_up_exact`, `lim_dn_exact` (kapanış hesaplanan sınır fiyatına tam eşit); `zero_vol`; `ipo_n` (ilk işlem günü 1, öncesi 0); `ca_day` (bölünme/bedelsiz/bedelli); `div_day` (nakit temettü); `tradable` (ipo_n > 20, hacim > 0, veri var).
- `idx`, `idx_ret` (7 endeks, İş Yatırım); `idx_open` (XU030, XU100: Yahoo açılış/kapanış oranı × İş Yatırım kapanışı).
- `meta.csv`, `ca_events.csv`; yalnız panel_full'da `dogrulama_d1.txt`, `yahoo_isy_fark.csv`.

**Kaynak seçimi.** Kapanış, en yüksek/düşük, TL hacim, piyasa değeri: İş Yatırım HisseTekil (HG_* ham alanlar). Açılış: Yahoo; ham ölçeğe çevrilir, İş Yatırım'ın gün aralığına düşmüyorsa boş bırakılır (satırların %1'i boş). Yahoo kapanışı kullanılmaz: iki kaynağın günlük getirisi 2.223 hisse-günde %1'den fazla ayrışıyor; XELKT hakem alındığında İş Yatırım daha tutarlı.

**Düzeltme kuralları**
- Çarpan = HG_KAPANIS/HGDG_KAPANIS oranının kurumsal işlemler arasındaki medyanı (parça parça sabit); c = c_raw/çarpan. Temettü, bedelsiz ve bedelli düzeltilmiştir; kurumsal işlem olmayan günde getiri ham getiriye eşittir.
- Baz fiyat = önceki ham kapanış × çarpan oranı. Marj 2020-03-13 öncesi ±%20, sonrası ±%10 (veride doğrulandı). Tavan/taban günleri silinmez.
- Fiyat adımı: <20 TL 0,01; <50 0,02; <100 0,05; <250 0,10; 2023-11-06'dan itibaren <500 0,25; <1000 0,50; <2500 1,00; üstü 2,50 (öncesinde ≥100 TL için 0,10; veriden saptandı).
- İş Yatırım'da hacmi 0 görünen ama Yahoo'da işlem olan 39 hisse-gün Yahoo'dan yamalandı (`kaynak=yahoo_yama`; 2010–13 yarım günleri, LYDYE 2012-10-30/31 ve 2024-10-01). Kalan 115 işlemsiz günde fiyat taşınır, h = l = c, `zero_vol` doğrudur.
- Halka arzın ilk günü getirisi boştur (halka arz fiyatı panelde yok).

**Bilinen sorunlar**
- 30.11.2015 öncesi çift seans vardı; sınır kapanışa göre tanımlı değildi. O dönemin tavan/taban bayrakları güvenilmez (AKSUE 2015-06-01 +%21,6 gerçek bir gündür).
- `lim_up`/`lim_dn` kapsayıcıdır: 2020-03-13 sonrası bayraklı günlerin yaklaşık %98'i tam sınır fiyatında; kalanı sınırın birkaç adım gerisinde, günün ucunda kapanıştır. Kilit ayrımı için `*_exact` kullanılabilir.
- Açılış eksikleri: KLYPV, MOGAN, MAGEN'in ilk 22–38 günü (Yahoo geç başlıyor); LYDYE, PAMEL, ZEDUR; 2010–11. Yahoo'nun bölünmeyi yanlış güne yazdığı birkaç günde de açılış boştur.
- 2010–2012'de üye sepeti ile XELKT korelasyonu düşüktür (0,86–0,93): o yılların endeks üyeleri evrende yok (hayatta kalma yanlılığı).
- `mcap_tl` toplam piyasa değeridir, halka açık kısım değil.
- Kurumsal işlem günlerinde dev ve full getirileri 1e-6'dan az ayrışır.
- ZEDUR 2011-05-31 için satır yok.

Yeniden üretim: `bash kod/d1_veri/run.sh <veri_klasörü>`.
