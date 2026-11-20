araç: 32/40

## Özet

Dört araç ve çıktı notu üretildi; `sinyal.py` kural kodlarıyla birebir aynı sonucu veriyor. Hepsi `/home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/` altında.

**Doğrulama (son 400 işlem günü, 2025-04-17 → 2026-11-20):** S1 86 gün, S2 58 gün, S3 19 gün; kural kodlarıyla fark 0. Hem panelin ham dosyalarıyla hem şimdi indirilen veriyle sınandı. Hisse düzeyi listelerde de fark 0 (sepet, 5 puan geride, en kötü beşte birlik, tabana değen, T2). Varsayılan 450 günlük indirme penceresi uzun pencereyle aynı sonucu veriyor.

**Listede olmayan önemli bulgu:** İş Yatırım'ın günlük endeks serisi son gün için güvenilmez. Aynı istek 20.11 için XELKT'de 537,06 / 539,06 / 539,83 / 545,14 döndürdü; 8 XU030 isteğinin 5'inde gün hiç yoktu. İlk canlı doğrulama koşusu bu yüzden son günü kaçırdı (S1/S2/S3 farkı çıkmadı, hisse listeleri son gün boş kaldı). Düzeltme: betik son 10 günü saatlik serinin 18:00 damgalı kapanışıyla doğrular, farklıysa onu kullanır ve NOT satırı yazar. Saatlik değer 14 yinelenen istekte değişmedi ve son 400 günün 395'inde günlük kapanışla aynı. Düzeltmeden sonra canlı koşu birebir tuttu. Panelin son günü doğru (XELKT 537,06). Hisse ucu üç indirmede aynıydı.

**Bugünün sinyali (2026-11-20):** S1, S2, S3 üçü de HAYIR. XELKT 537,06 (−%2,33, z −1,11); XU030 13.957,13 (z −1,29). Yarın için tetik: S1 XELKT ≥ 571,59; S2 XELKT ≥ 548,31; S3 XU030 ≥ 14.220,17 ve XELKT < 542,68. Dolabilir 40 hisse (CATES ve BIGEN tavanda kapandı). Kaçınma: MAGEN (sektörden −8,1 puan, tabanda kapandı). Son sinyaller: S2 12.11, S1 13.11 ve 16.11.

**Görev tanımından sapmalar:**
- Betik XU100'ü de çeker (takvim panelle aynı olsun diye) ve saatlik endeks serisini ekler: toplam 48 istek, bir koşu 20–50 saniye.
- İstenmeyen ama eklenen seçenekler: `--gecmis N` (Pine'ı karşılaştırmak için son günlerin dökümü), `--ham`, `--kaydet`.
- Pine derlenmedi; iki kez satır satır gözden geçirildi, uyarı notu iki dosyanın başında.

**Pine ile betik arasındaki bilinen farklar:** Pine'da S2'nin "en az 5 dolabilir hisse" koşulu yok. `hisse_sektor_fark.pine` kıyas olarak XELKT'yi kullanıyor; araştırmadaki kıyas eşit ağırlıklı sepet (20.11'de XELKT −%2,33, sepet −%1,87).

## İddia defteri

iddia | dosya yolu ya da URL | sayı ya da birebir kısa alıntı | güven
S1 günleri kural koduyla aynı | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/dogrulama_sonucu.txt | "S1: kural kodu 86 gün, sinyal.py 86 gün, FARK 0" | yüksek
S2 günleri aynı | aynı dosya | "S2: kural kodu 58 gün, sinyal.py 58 gün, FARK 0" | yüksek
S3 günleri aynı | aynı dosya | "S3: kural kodu 19 gün, sinyal.py 19 gün, FARK 0" | yüksek
Canlı indirmede de birebir | aynı dosya | "SONUÇ canli: S1/S2/S3 sinyal günleri BİREBİR AYNI" | yüksek
Sepet (dolabilir) hücreleri aynı | aynı dosya | "sepet: kural kodu 14880 hücre, sinyal.py 14880 hücre, FARK 0" | yüksek
5 puan geride listesi aynı | aynı dosya | "k5: kural kodu 518 hücre ... FARK 0" | yüksek
En kötü beşte birlik aynı | aynı dosya | "kq: kural kodu 2863 hücre ... FARK 0" | yüksek
Tabana değen aynı | aynı dosya | "taban: kural kodu 390 hücre ... FARK 0" | yüksek
T2 aynı | aynı dosya | "t2: kural kodu 2268 hücre ... FARK 0" | yüksek
450 günlük pencere yeterli | aynı dosya | son 150 gün: bütün fark sayıları 0; en büyük z farkı 1,1e-13 | yüksek
Günlük endeks ucunun son günü tutarsız (XELKT) | https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll (period=1440) | 20.11 için 537,06 / 539,06 / 539,83 / 545,14 | yüksek (oturumda gözlendi)
Aynı tutarsızlık XU030'da | aynı uç nokta | 13.957,13 / 13.976,42 / 14.010,74; 8 isteğin 5'inde 20.11 yok | yüksek
Aynı tutarsızlık XU100'de | aynı dosya (dogrulama_sonucu.txt) | "günlük seride 11.166,39, saatlik 18:00 kapanışı 11.131,32 kullanıldı" | yüksek
Saatlik uç yinelenen isteklerde sabit | aynı uç nokta (period=60) | 14 istekte XELKT 18:00 = 537,06; XU030 18:00 = 13.957,13 | orta (tek gece)
Saatlik 18:00 değeri = günlük kapanış | dogrulama_sonucu.txt | "son 400 günün 395'inde 18:00 damgası var; ... ayrışan gün 0" | yüksek
Hisse ucu kararlı | HisseTekil; üç indirme karşılaştırması | 12.106 ortak satır, 0 farklı | orta (tek gece)
Panelin son günü doğru | panel_full/idx.parquet ve saatlik 18:00 | XELKT 537,06; XU030 13.957,13; XU100 11.131,32 | yüksek
Bugün sinyal yok | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/ornek_cikti_2026-11-20.txt | S1 HAYIR, S2 HAYIR, S3 HAYIR | yüksek
Bugünkü z'ler | aynı dosya | XELKT z −1,11; XU030 z −1,29 | yüksek
Yarının S1 tetiği | aynı dosya | "S1: XELKT >= 571,59 (%+6,43)" | yüksek
Yarının S2 tetiği | aynı dosya | "S2: XELKT >= 548,31 (%+2,09)" | yüksek
Yarının S3 tetiği | aynı dosya | "XU030 >= 14.220,17 ... ve XELKT < 542,68" | yüksek
Bugün dolabilir hisse sayısı | aynı dosya | 40; sepet dışı CATES, BIGEN (tavanda kapandı) | yüksek
Bugünkü kaçınma | aynı dosya | "Sektörden >= 5 puan geride: MAGEN (-8,1)"; tabanda kapandı | yüksek
XELKT ile eşit ağırlıklı sepet ayrışıyor | aynı dosya | XELKT −%2,33; sepet −%1,87 | yüksek
İzleme listesindeki kodların hepsi doğrulanmış | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/izleme_listesi.txt | 3 endeks + 4 vadeli + 42 hisse; doğrulanmamış kod 0 | yüksek
Pine derlenmedi | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/elektrik_sinyal.pine | "TradingView'da derlenip test edilmedi; ilk kullanımda sinyal.py çıktısıyla karşılaştırın." | yüksek
Belge uzunlukları sınırın altında | KULLANIM.md; /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v7_araclar.md | 376 kelime; 295 kelime (çıktı bloğu hariç) | yüksek

## Dosyalar

- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/sinyal.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/dogrula.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/dogrulama_sonucu.txt
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/elektrik_sinyal.pine
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/hisse_sektor_fark.pine
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/izleme_listesi.txt
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/KULLANIM.md
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/ornek_cikti_2026-11-20.txt
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/araclar/ornek_hisse_2026-11-20.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v7_araclar.md

Doğrulamayı yeniden çalıştırma: `python3 -I araclar/dogrula.py --panel <panel_full> --kod <kod> --ham <data/raw/d1> --canli` (ham dosyalar `raw/` altında değil `raw/d1/` altında).

## Açık kalanlar

- Pine kodları TradingView'da derlenmedi ve çalıştırılmadı. İlk kullanımda işaretler `sinyal.py --gecmis 20` dökümüyle karşılaştırılmalı (beklenen: S2 12.11, S1 13.11 ve 16.11).
- Uç noktaların seans içindeki ve 18:10'daki davranışı sınanmadı; bütün koşular gece 01:10–01:25 arasında yapıldı. Hisse ucunun günün satırını ne zaman yayımladığı ve saatlik serinin 18:00 damgasının ne zaman oluştuğu bilinmiyor.
- Seans içinde saatlik seride bugün var, hisse verisinde yoksa betik dünü raporlar ama "son günün endeks kapanışı kesin değil" uyarısını yine de basar; uyarı o durumda yanıltıcıdır. Düzeltilmedi (sınanamayan yol).
- Günlük endeks ucundaki tutarsızlığın nedeni bilinmiyor (olası: bayat önbellekli sunucular). Saatlik ucun kararlılığı tek gecede 14 istekle görüldü; başka günlerde de izlenmeli.
- Yarım günlerde 18:00 damgası yok: betik son saatlik değeri kullanır ve uyarır; bu yol gerçek bir yarım günde sınanmadı.
- `--gunici` yalnız endeks sinyallerini günceller; hisse listeleri son kapanışa göre kalır (17:50 hisse fiyatı çekilmiyor).
- Betik panelin Yahoo yamalarını ve Yahoo temettü/bölünme tarihlerini kullanmaz. Son 400 günde fark doğurmadı; ileride küçük bir temettü ya da İş Yatırım'da hacmi 0 görünen bir gün fark yaratabilir.
- Üye listesi koda gömülü (20.11.2026, 42 hisse); endeks üyeliği değişirse elle güncellenmeli.
- T1 (LightGBM modeli) araçlarda yok.