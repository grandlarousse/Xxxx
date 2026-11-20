araç: 23/40

## Özet

S1, S2 ve S3'ün üçü de ham İş Yatırım verisinden kendi kodumla **YENİDEN ÜRETİLDİ**. Hiçbir satırda 10 bps'yi aşan fark ya da işaret farkı yok. Ortak kütüphane ve panel yalnız son adımda karşılaştırma için açıldı.

- **Ham veri:** yeniden indirilen 8 hisse ve XELKT ham dosyalarla satır satır aynı. XU030'da tek fark son günün yuvarlaması. XU100 yeniden indirmesinde 94 tarih eksik geldi (93'ü 2010 öncesi, biri 2026-11-20); ortak tarihlerde değer aynı.
- **Sinyal tarihleri:** S1 ve S3'te bütün dönemlerde %100 örtüşüyor. S2'de IS 442/444, sonrası %100. Eksik iki gün (2010-12-21, 2011-08-29) İş Yatırım'da hacmi 0 görünen günler; bunlar D1 notunda Yahoo'dan yamalandığı yazılan gün sınıfına uyuyor, kaynak sütununu ayrıca kontrol etmedim.
- **Tek anlamlı fark kasada:** S1 +7,3 bps, S2 +8,0 bps (benim rakamım daha yüksek). Sinyal günleri ve ham getiri aynı; fark kıyastan geliyor.
- **Nedeni bir kütüphane sapması:** `elib.fwd_exec` çıkış kaymasını 5 günle sınırlıyor (`max_delay=5`). Uzun taban serilerinde 5 günün sonunda hâlâ kilitli kapanıştan çıkılmış sayıyor. Yöntem ise "ilk kilitsiz kapanış" diyor.
- **Etkisi:** yönteme uygun hesapta BIGEN'in kasa kıyası −360 yerine −579 bps; LYDYE ve MAGEN yaklaşık 37 bps daha düşük. Kütüphaneyi taklit eden sürümüm ana rakamları kasada 0,05 bps içinde veriyor. Ana ajanın `per` rakamları bu yüzden temkinli taraftadır.
- **Panel düzeyi:** takvim aynı (4.238 gün); dolabilir hücrelerde 51 fark (yaklaşık 63.300 içinde); getirisi %0,1'den fazla ayrışan 13 hücre (en büyüğü LYDYE 2024-10-02).

Ek sağlamlık, 2023+ havuzu:

| Kural | Blok önyükleme %90 GA (bps) | Kaydırma p |
|---|---|---|
| S1 | +31 … +136 | 0,002 |
| S2 | +21 … +127 | 0,012 |
| S3 | +77 … +247 | 0,005 |

Görevde istenmeyen ama öneriyi etkileyen iki bulgu:

1. **`per` kasada çöküş hisselerine duyarlı.** BIGEN, LYDYE ve MAGEN hedef ve kıyastan çıkarılınca S1 kasa +93 → +59 (t 1,7), havuz +85 → +67 (t 2,2); S2 kasa +103 → +82 (t 2,1), havuz +73 → +62 (t 2,0). Etki kaybolmuyor ama kasadaki büyüklüğün yaklaşık üçte biri bu üç hissenin sıradan gün zararından geliyor.
2. **"Maliyet sonrası +40" `per` üzerinden hesaplanmış.** Yalnız AL yapanın eline geçen ham getiri − maliyettir. Kasada S1 sinyal günü ham ortalaması +48 bps; ana tablodaki ~35 bps temel maliyetle yaklaşık +13 bps kalıyor (havuzda yaklaşık +39). Kasada sinyal dışı günlerde sepet −65 bps (3 günlük).

S3 kasada tek başına anlamsız (16 gün; GA −40 … +139; p 0,32); havuz sonucu OOS-1'e dayanıyor.

Dosyalar:
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v1_yeniden_momentum.md
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v1_yeniden_momentum.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/v1_yeniden_momentum/run.sh

## İddia defteri

Aksi yazılmadıkça kaynak: /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v1_yeniden_momentum.csv ("v1 csv").

iddia | dosya yolu ya da URL | sayı ya da birebir kısa alıntı | güven
---|---|---|---
S1 IS yeniden üretildi | v1 csv | ana 43,50 (t 2,83) → V1 42,90 (t 2,78); 569 gün, 278 olay, 6.510 işlem; ham 93,4; isabet 0,48 | yüksek
S1 OOS-1 | v1 csv | ana 84,67 (t 1,81) → V1 83,61 (t 1,78); 93 gün, 46 olay; ham 96,8; isabet 0,52 | yüksek
S1 kasa | v1 csv | ana 86,24 (t 2,47) → V1 93,48 (t 2,65); 81 gün, 36 olay; ham 47,7; isabet 0,58 | yüksek
S1 havuz 2023+ | v1 csv | ana 82,58 (t 2,75) → V1 85,14 (t 2,84; blok t 2,67); 174 gün, 82 olay; ham 73,9; isabet 0,54 | yüksek
S2 IS | v1 csv | ana 52,53 (t 3,21) → V1 52,97 (t 3,22); 442 gün (ana 444), 329 olay; ham 99,7; isabet 0,49 | yüksek
S2 OOS-1 | v1 csv | ana 53,02 (t 1,21) → V1 53,12 (t 1,21); 96 gün, 66 olay; ham 66,2; isabet 0,50 | yüksek
S2 kasa | v1 csv | ana 95,24 (t 2,29) → V1 103,25 (t 2,44); 50 gün, 39 olay; ham 57,4; isabet 0,57 | yüksek
S2 havuz | v1 csv | ana 70,27 (t 2,19) → V1 73,40 (t 2,28); 146 gün, 105 olay; ham 63,2; isabet 0,53 | yüksek
S3 IS | v1 csv | ana 64,21 (t 2,42) → V1 64,26 (t 2,41); 145 gün, 129 olay, 295 işlem; ham 107,0; isabet 0,54 | yüksek
S3 OOS-1 | v1 csv | ana 220,60 (t 2,99) → V1 220,98 (t 2,94); 29 gün, 25 olay; ham 227,2; isabet 0,64 | yüksek
S3 kasa | v1 csv | ana 41,31 (t 0,79) → V1 41,33 (t 0,77); 16 gün, 14 olay; ham 85,9; isabet 0,54 | yüksek
S3 havuz | v1 csv | ana 156,68 (t 3,01) → V1 156,93 (t 2,98); 45 gün, 39 olay; ham 176,9; isabet 0,61 | yüksek
Sinyal tarihleri örtüşmesi | v1 csv (tarih_ortusme_jaccard) | S1, S3: 1,000 bütün dönemler; S2 IS 0,9955 (yalnız ana: 2010-12-21, 2011-08-29), sonrası 1,000 | yüksek
S2'nin iki eksik gününde İş Yatırım hacmi sıfır | /tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/el/data/raw/d1/isy_hisse/AKENR.json | 21-12-2010 ve 29-08-2011: HG_HACIM 0.0 (AKENR, AKSUE, AYEN, ZOREN, AKSEN) | yüksek
Bu günlerin panelde Yahoo yaması olduğu | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/VERI_NOTU_D1.md | "39 hisse-gün Yahoo'dan yamalandı (`kaynak=yahoo_yama`; 2010–13 yarım günleri" — eşleşme çıkarım, kaynak sütununa bakılmadı | orta
Kasa farkının nedeni: kütüphane çıkış kaymasını 5 günle sınırlıyor | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/ortak/elib.py (fwd_exec) | "def fwd_exec(P, h, side='long', cols=None, max_delay=5)" | yüksek
Kütüphane taklidi ana rakamı veriyor | v1 csv (v1B_kutuphane_taklidi_bps) | S1 kasa 86,26 (ana 86,24); S2 kasa 95,29 (ana 95,24); S1 havuz 82,09; S2 havuz 70,34 | yüksek
Kasa kıyası, hisse bazında (V1 / kütüphane taklidi, bps) | /tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/v1out/v1_f3A.pkl ve v1_f3B.pkl | BIGEN −578,5 / −360,3; LYDYE −364,0 / −325,6; MAGEN −191,7 / −155,2; ESEN −200,2 / −196,3 | yüksek
Çıkış kaymasından etkilenen dolabilir hücre sayısı | aynı dosyalar | IS 5, OOS-1 0, kasa 49 | yüksek
Kasada en uzun taban serileri (V1 bayrağıyla) | /tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/v1out/v1_taban.pkl | BIGEN 29, LYDYE 14, MAGEN 13 | yüksek
Blok önyükleme (blok 5, 2.000 tekrar), havuz %90 GA | v1 csv | S1 +31,4 … +136,5; S2 +20,9 … +126,8; S3 +76,7 … +247,2 | yüksek
Rastgele kaydırma (≥ 30 gün, 1.000 tekrar), havuz p | v1 csv | S1 0,002; S2 0,012; S3 0,005 (bütün kaydırmalarla 0,002 / 0,008 / 0,004) | yüksek
Kasa tek başına: GA ve p | v1 csv | S1 +32 … +147, p 0,013; S2 +34 … +167, p 0,034; S3 −40 … +139, p 0,32 | yüksek
OOS-1 tek başına GA sıfırı içeriyor (S1, S2) | v1 csv | S1 −7,7 … +162, p 0,019; S2 −25,7 … +123, p 0,065 | yüksek
Çöküş hisseleri (BIGEN, LYDYE, MAGEN) hariç | v1 csv (v1C_*) | S1 kasa 59,3 (t 1,67), havuz 66,6 (t 2,16); S2 kasa 82,1 (t 2,11), havuz 62,3 (t 1,96); S3 değişmez | yüksek
Kasada sinyal dışı günlerde sepetin ham 3 günlük getirisi | v1 csv (v1_sinyal_disi_gun_ham_bps) | S1 −64,9; S2 −54,9; havuzda −23,0 / −17,8 | yüksek
"Maliyet sonrası +40" per tabanlı | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/tum_oos_sonuc.csv | S1: basabas_OOS 75,23 − maliyet_temel 35,13 = net_temel 40,10; ham − maliyet: kasa 47,7 − 35,1 ≈ +13, havuz 73,9 − 35,1 ≈ +39 | yüksek
Yeniden indirme, hisseler ve XELKT | https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil | 8 hisse + XELKT: "farkli_satir=0 yalniz_ham=0 yalniz_yeni=0" | yüksek
Yeniden indirme, XU030 ve XU100 | https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/ChartData.aspx/IndexHistoricalAll | XU030: 1 fark (2026-11-20: 13957,13 / 13957,12988); XU100: yeni dosyada 94 tarih eksik, ortak 6.646 tarihte fark 0 | yüksek
Panel düzeyi fark | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/v1_yeniden_momentum/02_karsilastir.py çıktısı | tradable 64.629 / 64.661; dolabilir 63.276 / 63.299; tavan 1.353 / 1.362; taban 598 / 610; getiri farkı > 1e-3: 13 hücre, maks 0,11 (LYDYE 2024-10-02) | yüksek

## açık kalanlar

- **XU100 yeniden indirmesi** ham dosyadan 94 tarih eksik döndü; nedenine bakmadım. Sonuca etkisi yok: takvim ham dosyadan kuruldu, V1 takvimi panelle aynı.
- **Kilit bayrakları** panelde benimkinden biraz daha kapsayıcı (2023+: 11 tavan, 15 taban hücresi yalnız panelde). Sonuca etkisi 0,5 bps'nin altında; hücre hücre incelemedim.
- **`max_delay=5` sınırı diğer kuralları da etkiler.** Bu görevde yalnız S1–S3'e baktım. `per` ya da `sec` kullanan ve taban serilerine yakın çalışan kurallarda (özellikle K2 ve T1/T2'nin kasa rakamları) etkisi ölçülmedi.
- **2015-11-30 öncesi** çift seans döneminde tavan/taban bayrakları iki hesapta da güvenilmez; IS rakamları bu sınırla okunmalı.
- **Çöküş hisseleri duyarlılığı** yalnız BIGEN, LYDYE, MAGEN için yapıldı. ESEN de kasada 25 taban günü taşıyor (kıyası −200 bps); dahil edilirse `per` biraz daha düşebilir.
- **z-skoru** panelle aynı başlangıçtan (2010-01-04) kuruldu; 2010 öncesi endeks geçmişi kullanılırsa 2010'un ilk iki ayında birkaç sinyal günü eklenir, denenmedi.