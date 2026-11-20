araç: 17/40

**Özet (D1 — günlük spot + endeks paneli)**

Panel kuruldu, doğrulamanın beş maddesi de çalıştırıldı. Bu alt ajan Fable 5.2 (`claude-fable-5-2`) ile çalıştı.

- **Kapsam:** 46 hisse (42 XELKT + 4 komşu), 7 endeks, 2010-01-04 → 2026-11-20, 4.238 işlem günü, 72.948 hisse-gün. `panel_dev` 2025-06-30'da kesik: 3.886 gün, 40 hisse (ARFYE, BESTE, ECOGR, MASFN, METEN, VEYAS sonradan halka arz, dev'de yok).
- **Yarım deneme:** `raw/d1` silinip baştan indirildi. Eski indirmede XU100 4.302 satırdı, yenisinde 6.740; indiriciye endeks bütünlük kontrolü eklendi. `d1_fetch.py` silindi. D2'ye ait klasör ve betiklere dokunulmadı.
- **Kaynak kararı:** kapanış, yüksek/düşük, TL hacim, piyasa değeri İş Yatırım'dan; yalnız açılış Yahoo'dan (ham ölçeğe çevrilip İş Yatırım gün aralığıyla doğrulanıyor, %1,05 boş). Düzeltilmiş kapanış, ham kapanışın İş Yatırım ham/düzeltilmiş oranının parça parça sabit medyanına bölünmesiyle kuruldu (temettü + bedelsiz + bedelli).
- **(a) Yahoo–İş Yatırım:** |fark| > %1 olan 2.223 hisse-gün (2020+ 734, 2023+ 135). Dağılım: 762 Yahoo'nun piyasa geneli hatalı günü, 237 bayat/tatil satırı, 1.195 tekil kapanış farkı, 15 Yahoo kapanışı gün aralığı dışında, 14 kurumsal işlem günü. Kurumsal işlem günlerinin 5'inde Yahoo getirisi marj dışı, İş Yatırım hepsinde marj içinde. XELKT hakem alındığında İş Yatırım daha tutarlı; tek istisna 13 günlük "aralık dışı" grubu, küçük örneklem. Karar: her yerde İş Yatırım.
- **İş Yatırım delikleri:** hacmi 0 görünen ama Yahoo'da işlem olan 39 hisse-gün Yahoo'dan yamalandı (2010–13 yarım günleri, LYDYE 2012-10-30/31 ve 2024-10-01). 115 gerçek işlemsiz gün `zero_vol` ile bayraklı.
- **(b)** |getiri| > marj + %0,6 kalan tek gün: AKSUE 2015-06-01 +%21,6. Kurumsal işlem günü değil; çift seans dönemi, Yahoo aynı getiriyi veriyor.
- **(c)** Eşit ağırlıklı sepet–XELKT korelasyonu yıllara göre 0,72–0,98 (tüm dönem 0,89; 2021+ 0,94). Piyasa değeri ağırlıklı sepetle 2013+ her yıl 0,97–0,99; 2010–12'de 0,86–0,93 (o yılların üyeleri evrende yok).
- **(d)** Tavan/taban kapanışları 2020 öncesinde yılda 0–25, 2020+ yılda 143–382 tavan ve 25–249 taban. 2020-03-13 sonrası 1.611 tavan kapanışının 1.581'i, 697 tabanın 673'ü hesaplanan sınır fiyatına tam eşit. Ham veriden 5 örnek elle kontrol edildi: 4'ü tam sınırda, BIGEN 2026-10-28 sınırın 3 adım üstünde gün dibinde kapanmış (kural gereği bayraklı).
- **(e)** `panel_dev`'de tüm dosyalarda son tarih 2025-06-30; dev–full getiri farkı en çok 6,4e-7.

**Görev tanımından sapmalar ve ekler**
- Tavan toleransı max(%0,6; bir fiyat adımı): düşük fiyatlı hisselerde sınır %9,4'ün altına yuvarlanabiliyor.
- Ek dosyalar: `lim_up_exact`, `lim_dn_exact`, `div_day` (nakit temettü; `ca_day` yalnız sermaye işlemleri), `ca_events.csv`, `dogrulama_d1.txt`, `yahoo_isy_fark.csv`.
- Fiyat adımı tablosu tarih duyarlı: 250 TL üstü yeni adımlar veride 2023-11-06'da başlıyor.
- `VERI_NOTU_D1.md` (465 kelime) `panel_dev`'e de kopyalandı.

**Dosyalar**
- /tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el/data/panel_full/
- /tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el/data/panel_dev/
- /tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el/data/raw/d1/
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/VERI_NOTU_D1.md
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/d1_veri/ (`run.sh <veri_klasörü>`, `01_indir.py`, `02_panel.py`, `03_dogrula.py`, `d1lib.py`, `universe.py`)

**İddia defteri** (PF = /tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el/data/panel_full)

iddia | kaynak | alıntı ya da sayı | güven
---|---|---|---
Panel boyutu (full) | PF/ret_cc.parquet | (4238, 46), 2010-01-04 → 2026-11-20 | yüksek
Panel boyutu (dev) | …/el/data/panel_dev/ret_cc.parquet | (3886, 40), son tarih 2025-06-30 | yüksek
Dev'de 2025-06-30 sonrası satır yok | PF/dogrulama_d1.txt | "dev son tarih tum dosyalarda 2025-06-30 : True" | yüksek
Dev–full getiri farkı ihmal edilebilir | PF/dogrulama_d1.txt | "ret_cc: full ile fark = 6.365298508281825e-07" | yüksek
Yahoo–İş Yatırım ayrışması | PF/dogrulama_d1.txt | "\|fark\|>%1: 2223 \| 2020+: 734 \| 2023+: 135" | yüksek
Ayrışmanın en büyük grubu Yahoo'nun piyasa geneli hatalı günleri | PF/yahoo_isy_fark.csv | 762 satır (kategori 3) | orta
XELKT hakemliğinde İş Yatırım daha tutarlı | PF/dogrulama_d1.txt | "RMSE Is Yatirim=0.00496 Yahoo ikameli=0.00725" (989 gün) | yüksek
Hakem istisnası: "aralık dışı" grubu | PF/dogrulama_d1.txt | 13 gün: İş Yatırım 0.00890, Yahoo 0.00762 | düşük (küçük örneklem)
Kurumsal işlem günlerinde İş Yatırım marj içinde | PF/dogrulama_d1.txt | NATEN 2023-11-29: ri −0.0918, ry +0.4267 | yüksek
Kurumsal işlem sayısı | PF/ca_events.csv | 139 satır (dev: 113) | yüksek
Yahoo bedelli/bedelsiz kaçırıyor | PF/ca_events.csv | AKSUE 2021-02-23 adım −0.46549, yahoo_split boş, sermaye +1.0 | yüksek
Yahoo bölünmeyi yanlış güne yazıyor | raw/d1/yahoo/CONSE.json, isy_hisse/CONSE.json | Yahoo ölçeği 2024-07-17'de değişiyor; İş Yatırım adımı 2024-07-25 | yüksek
İş Yatırım delikleri Yahoo'dan yamalandı | PF/dogrulama_d1.txt | 39 hisse-gün: '2013-10-14': 9, '2013-10-28': 9, '2024-10-01': 1 | yüksek
LYDYE 2024-10-01 İş Yatırım'da boş, Yahoo'da işlem var | raw/d1/isy_hisse/LYDYE.json, yahoo/LYDYE.json | İş Yatırım hacim 0, kapanış 9600; Yahoo c=10560, v=2708 | yüksek
Gerçek işlemsiz gün sayısı | PF/dogrulama_d1.txt | "sifir hacim (satir var): 115" (110'u LYDYE) | yüksek
Marj aşan tek gün | PF/dogrulama_d1.txt | AKSUE 2015-06-01 r=0.2158, ca=False | yüksek
Marj değişim tarihi veride görülüyor | PF/ret_cc.parquet | günlük max \|r\|: 2020-03-12 0.200, 2020-03-13 0.100 | yüksek
Fiyat adımı değişim tarihi | PF/px.parquet | ≥250 TL'de eski ızgarada son fiyat 2023-11-03; 2023-11-06'dan itibaren tümü 0,25 katı | orta (veriden çıkarım)
Tarih duyarlı tabloya uyum | PF/dogrulama_d1.txt | 2021+ ham kapanışların uyum oranı 1.0000 | yüksek
Tavan/taban kapanışlarının tam sınırda olma oranı | PF/dogrulama_d1.txt | "tavan_kap: 1611 … tam esit: 1581 \| taban_kap: 697 \| tam esit: 673" | yüksek
Tavan kapanışı yıllık sayıları | PF/dogrulama_d1.txt | 2020: 221, 2023: 382, 2025: 143, 2026: 267 | yüksek
Elle kontrol, tam sınır örneği | raw/d1/isy_hisse/AKENR.json | 2025-03-19: önceki 11.21, kapanış = düşük = 10.09, teorik 10.089 | yüksek
Elle kontrol, sınırın gerisinde örnek | raw/d1/isy_hisse/BIGEN.json | 2026-10-28: önceki 7.1, kapanış = düşük = 6.42, teorik 6.39 | yüksek
Eşit ağırlıklı sepet–XELKT korelasyonu | PF/dogrulama_d1.txt | "tum donem corr EW: 0.8903 … 2021+ EW: 0.9435"; en düşük 2019: 0.715 | yüksek
Piyasa değeri ağırlıklı sepet–XELKT | PF/dogrulama_d1.txt | 2013–2026 her yıl 0.972–0.994; 2012: 0.864 | yüksek
Açılış doluluğu | PF/px.parquet | 765 boş / 72.948 (%1,05); 2010: 0.936, 2023: 1.0 | yüksek
Açılışlar fiyat adımına oturuyor | PF/dogrulama_d1.txt | son düzeltmeden sonraki 20.461 günde oran 0.9963 | yüksek
Endeksler eksiksiz; Yahoo XBANK bozuk | PF/dogrulama_d1.txt | endeks eksik gün 0; XU100 farkı >%0,2: 0; XBANK corr=0.02997 | yüksek
Takvim ayıklaması | raw/d1/isy_endeks/XU100.json | 2013-01-01 satırı 2012-12-31 ile aynı değer (782.0844); 2023-02-08 XU100 boş | yüksek
VİOP hisseleri meta (full) | PF/meta.csv | AKSEN 63.80 TL, tick 0.05 (7.84 bps); ENJSA 111.60, 0.10; ODAS 4.35, 0.01 (22.99 bps) | yüksek

**açık kalanlar**
- 30.11.2015 öncesi çift seans nedeniyle tavan/taban bayrakları güvenilmez; o dönem için A4 olay testleri bu bayraklara dayanmamalı.
- `lim_up`/`lim_dn` kapsayıcı (yaklaşık %2'si tam sınırda değil). Dolum kuralında hangisinin kullanılacağı (`lim_*` ya da `lim_*_exact`) ana ajanın kararı; `elib.load` şu an `*_exact` ve `div_day` dosyalarını yüklemiyor.
- Açılış yalnız Yahoo'dan; bağımsız ikinci kaynakla doğrulanmadı. KLYPV'nin ilk 38, MOGAN'ın 35, MAGEN'in 22 gününde açılış yok; LYDYE, PAMEL, ZEDUR ve 2010–11'de de boşluklar var.
- Tekil kapanış farklarında (1.195 hisse-gün) ve "aralık dışı" 15 günde üçüncü kaynak yok; karar kural bazlı verildi, tek tek incelenenler yalnız en büyük 28 fark ve 14 kurumsal işlem günü.
- Halka arz ilk gün getirisi boş (halka arz fiyatı panelde yok); ilk gün tavan bayrağı bu yüzden hesaplanmıyor.
- `mcap_tl` toplam piyasa değeri; XELKT halka açık değer ağırlıklı olduğundan sepet–endeks farkının bir kısmı buradan.
- 2023-11-06 fiyat adımı değişikliği ve 250 TL üstü adımlar yalnız veriden çıkarıldı; resmî duyuruyla teyit edilmedi. 500–1000 TL dilimi (0,50) 2023 sonrası veride hiç gözlenmedi.
- ZEDUR 2011-05-31 için hiçbir kaynakta geçerli satır yok.
- `VERI_NOTU_D1.md` içinde kasa dönemine ait sonuç yok, yalnız kapsam tarihi var; `dogrulama_d1.txt` ve `yahoo_isy_fark.csv` kasa dönemi istatistikleri içerir, 2. dalgaya verilmemeli (yalnız `panel_full`'da duruyor).
- `panel_full` klasöründe D2'ye ait `h1`, `m5`, `viop_daily.parquet`, `viop_front.parquet` var; dokunulmadı.