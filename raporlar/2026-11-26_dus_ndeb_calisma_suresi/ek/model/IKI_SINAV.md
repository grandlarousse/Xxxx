# İki sınav uzantısı: DUS + Virtual OSCE

h3 = 6 ve 7, 1.000'er çekim (tohum 101), 162 hücre × 75 seçenek, hesap 78 s. Sayılar `cikti/iki_sinav/` altındaki CSV'lerden.

## 1. Ana sonuç

Aynı günlük yükle Virtual OSCE koşulunu da tutturmanın DUS sınav günü P'sine maliyeti olurlu hücrelerde küçüktür: K2 yükü ve orta aktarımda S1'de %0,20–0,70, S2'de %0,31–1,27, S3'te %0,0; en kötü hücrede %13,8 (S3, K1, h3 = 7, düşük aktarım). S3 (önce DUS, 29 gün sonra Virtual OSCE) 54 karşılaştırmanın 36 tanesinde DUS'tan en az götüren sıralamadır ve 36 hücrede maliyeti sıfırdır; ama DUS öncesi pay 0 iken koşulun tuttuğu çekim oranı %80–99 arasında, %90 eşiğinin iki yanındadır ve eşiğin altında kalan 18 hücrenin (K1–düşük, K1–orta, K2–düşük) hepsinde S3 en pahalı sıralamadır (kayıp %1,9–13,8). S1 (1 Mart) 18 hücrede hiçbir payla olurlu değildir (K1: açık 0,15 ve 0,30; K2: açık 0,30); boş gün bütün olurlu hücrelerde 0 seçilmiştir.

**Kullanılan yükler (kaynak: yukler.csv; ana_tablo.csv, amaç b1, 360 gün).** K1 politikası K0 ile aynıdır.

| h3 | yük | hA + hB | gün/hafta | hafif hafta | haftalık saat |
|---|---|---|---|---|---|
| 6 | K1 | 3,5 + 0,0 | 7 | yok | 24,5 |
| 6 | K2 | 4,0 + 0,0 | 7 | 6 haftada bir | 26,0 |
| 6 | K3 | 5,0 + 0,0 | 7 | yok | 35,0 |
| 7 | K1 | 3,5 + 0,0 | 7 | yok | 24,5 |
| 7 | K2 | 4,5 + 0,0 | 7 | 6 haftada bir | 29,0 |
| 7 | K3 | 5,5 + 0,0 | 7 | yok | 38,5 |

## 2. Sıralama karşılaştırması

**Tablo 1 — K2 yükü, orta aktarım (kaynak: hucreler.csv).** Pay: Virtual OSCE payı. Gün-B: aynı kaybı veren "DUS'tan önceki son k gün hiç çalışılmasa"; gün-A: "DUS k gün erkene alınsa".

| h3 | açık | sıralama | pay D1 / D2 | boş gün | Virtual OSCE net saat | hafta | DUS kaybı % | gün-B | gün-A | koşulun tuttuğu çekim % |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 0,05 | S1 | 0,5 / 1 | 0 | 226,0 | 13,6 | 0,44 | 1,1 | 59 | 90,6 |
| 6 | 0,05 | S2 | 0,25 / 1 | 0 | 237,5 | 25,0 | 0,85 | 2,1 | 92 | 91,5 |
| 6 | 0,05 | S3 | 0 / 0 | 0 | 105,0 | 4,1 | 0,00 | 0,0 | 0 | 91,9 |
| 6 | 0,15 | S1 | 1 / 1 | 0 | 349,0 | 13,6 | 0,70 | 1,7 | 84 | 90,3 |
| 6 | 0,15 | S2 | 0,5 / 0,75 | 0 | 346,5 | 25,0 | 1,10 | 2,7 | 106 | 90,8 |
| 6 | 0,15 | S3 | 0 / 0 | 0 | 105,0 | 4,1 | 0,00 | 0,0 | 0 | 91,7 |
| 6 | 0,30 | S1 | olurlu değil | – | – | – | – | – | – | en iyi 86,0 |
| 6 | 0,30 | S2 | 0,5 / 1 | 0 | 372,0 | 25,0 | 1,27 | 3,1 | 115 | 90,5 |
| 6 | 0,30 | S3 | 0 / 0 | 0 | 105,0 | 4,1 | 0,00 | 0,0 | 0 | 91,2 |
| 7 | 0,05 | S1 | 0,25 / 0,75 | 0 | 156,0 | 13,6 | 0,20 | 0,5 | 42 | 90,0 |
| 7 | 0,05 | S2 | 0 / 0,75 | 0 | 87,0 | 4,3 | 0,31 | 0,8 | 54 | 90,8 |
| 7 | 0,05 | S3 | 0 / 0 | 0 | 118,0 | 4,1 | 0,00 | 0,0 | 0 | 94,2 |
| 7 | 0,15 | S1 | 0,5 / 1 | 0 | 254,5 | 13,6 | 0,34 | 0,8 | 58 | 90,2 |
| 7 | 0,15 | S2 | 0 / 1 | 0 | 116,0 | 4,3 | 0,42 | 1,0 | 67 | 91,0 |
| 7 | 0,15 | S3 | 0 / 0 | 0 | 118,0 | 4,1 | 0,00 | 0,0 | 0 | 94,2 |
| 7 | 0,30 | S1 | olurlu değil | – | – | – | – | – | – | en iyi 89,8 |
| 7 | 0,30 | S2 | 0,25 / 0,75 | 0 | 238,0 | 25,0 | 0,57 | 1,4 | 85 | 90,0 |
| 7 | 0,30 | S3 | 0 / 0 | 0 | 118,0 | 4,1 | 0,00 | 0,0 | 0 | 94,0 |

Gün-A büyüktür, çünkü modelde DUS bilgisi son aylarda doygundur: temel koşuda son 100 gün P'ye yalnız 0,4–0,8 puan katar, sınavdan önceki tek boş gün ise 0,24–0,32 puan götürür (temel_egri.csv). Kaybın küçüklüğü bu varsayımın sonucudur; güvenilecek ölçü yüzde kayıptır.

**Tablo 2 — En az götüren sıralama ve aktarımın erimesi (K2, orta aktarım; kaynak: siralama_karsilastirma.csv).** Aktarım: Virtual OSCE çalışmasının gD'ye kattığı puan, OSCE günü → DUS günü.

| h3 | açık | en az götüren | ikinciye fark, yüzde puanı | en kötüye fark | S1 aktarım | S2 aktarım | yalnız unutmayla kalan, S1 / S2 % |
|---|---|---|---|---|---|---|---|
| 6 | 0,05 | S3 | 0,44 (S1) | 0,85 | 10,2 → 0,17 | 5,9 → 0,33 | 35 / 49 |
| 6 | 0,15 | S3 | 0,70 (S1) | 1,10 | 23,0 → 0,33 | 7,8 → 0,49 | 35 / 49 |
| 6 | 0,30 | S3 | 1,27 (S2) | 1,27 | olurlu değil | 9,9 → 0,58 | – / 49 |
| 7 | 0,05 | S3 | 0,20 (S1) | 0,31 | 5,0 → 0,07 | 2,5 → 0,10 | 34 / 48 |
| 7 | 0,15 | S3 | 0,34 (S1) | 0,42 | 10,6 → 0,14 | 3,7 → 0,15 | 34 / 48 |
| 7 | 0,30 | S3 | 0,57 (S2) | 0,57 | olurlu değil | 4,4 → 0,22 | – / 48 |

gD'ye aktarılan katkının DUS gününe yalnız %1–6 kadarı kalır; yalnız unutma işleseydi %34–49 kalırdı. Fark, sonraki DUS çalışmasının aynı bilgiyi zaten kazandıracak olmasındandır. gN'nin sonraki düşüşü sonuca girmez.

## 3. Pay tablosu

**Tablo 3 — Orta aktarım (kaynak: hucreler.csv).** Hücre: D1 / D2 · Virtual OSCE net saati · DUS kaybı %.

| h3 | yük | açık | S1 | S2 | S3 |
|---|---|---|---|---|---|
| 6 | K1 | 0,05 | 0,75 / 1 · 273,0 s · %0,62 | 0,25 / 1 · 229,5 s · %0,94 | 0 / 0,25 · 124,5 s · %1,91 |
| 6 | K1 | 0,15 | olurlu değil (en iyi %89,3) | 0,5 / 0,75 · 330,5 s · %1,22 | 0 / 0,25 · 124,5 s · %1,91 |
| 6 | K1 | 0,30 | olurlu değil (en iyi %84,2) | 0,5 / 1 · 356,0 s · %1,41 | 0,25 / 0 · 363,0 s · %2,82 |
| 6 | K2 | 0,05 | 0,5 / 1 · 226,0 s · %0,44 | 0,25 / 1 · 237,5 s · %0,85 | 0 / 0 · 105,0 s · %0,00 |
| 6 | K2 | 0,15 | 1 / 1 · 349,0 s · %0,70 | 0,5 / 0,75 · 346,5 s · %1,10 | 0 / 0 · 105,0 s · %0,00 |
| 6 | K2 | 0,30 | olurlu değil (en iyi %86,0) | 0,5 / 1 · 372,0 s · %1,27 | 0 / 0 · 105,0 s · %0,00 |
| 6 | K3 | 0,05 | 0 / 0,75 · 109,5 s · %0,11 | 0 / 0,25 · 36,5 s · %0,09 | 0 / 0 · 141,5 s · %0,00 |
| 6 | K3 | 0,15 | 0,25 / 1 · 227,5 s · %0,21 | 0 / 0,5 · 73,0 s · %0,17 | 0 / 0 · 141,5 s · %0,00 |
| 6 | K3 | 0,30 | 0,75 / 1 · 390,0 s · %0,38 | 0 / 0,75 · 109,5 s · %0,27 | 0 / 0 · 141,5 s · %0,00 |
| 7 | K1 | 0,05 | 0,75 / 1 · 273,0 s · %0,60 | 0,25 / 1 · 229,5 s · %0,94 | 0,25 / 0 · 363,0 s · %2,86 |
| 7 | K1 | 0,15 | olurlu değil (en iyi %88,8) | 0,5 / 1 · 356,0 s · %1,39 | 0,25 / 0 · 363,0 s · %2,86 |
| 7 | K1 | 0,30 | olurlu değil (en iyi %84,5) | 0,75 / 0,75 · 457,5 s · %1,74 | 0 / 0,5 · 150,0 s · %4,05 |
| 7 | K2 | 0,05 | 0,25 / 0,75 · 156,0 s · %0,20 | 0 / 0,75 · 87,0 s · %0,31 | 0 / 0 · 118,0 s · %0,00 |
| 7 | K2 | 0,15 | 0,5 / 1 · 254,5 s · %0,34 | 0 / 1 · 116,0 s · %0,42 | 0 / 0 · 118,0 s · %0,00 |
| 7 | K2 | 0,30 | olurlu değil (en iyi %89,8) | 0,25 / 0,75 · 238,0 s · %0,57 | 0 / 0 · 118,0 s · %0,00 |
| 7 | K3 | 0,05 | 0 / 0,5 · 80,5 s · %0,05 | 0 / 0 · 0,0 s · %0,00 | 0 / 0 · 155,5 s · %0,00 |
| 7 | K3 | 0,15 | 0 / 0,75 · 120,5 s · %0,08 | 0 / 0 · 0,0 s · %0,00 | 0 / 0 · 155,5 s · %0,00 |
| 7 | K3 | 0,30 | 0,25 / 1 · 250,5 s · %0,17 | 0 / 0,25 · 40,0 s · %0,07 | 0 / 0 · 155,5 s · %0,00 |

Koşul hiçbir seçenekte bütün çekimlerde tutmaz: hücrelerin en iyi seçeneğinde oran %84,2–99,6. Eşik tavana yakın olduğundan paylar eşiğe duyarlıdır.

## 4. Aktarım (ω) etkisi

**Tablo 4 — K2 yükü; düşük → orta → yüksek (kaynak: omega_etkisi.csv).**

| h3 | sıralama | açık | Virtual OSCE net saat | DUS kaybı % | gün-B |
|---|---|---|---|---|---|
| 6 | S1 | 0,05 | 287,5 → 226,0 → 77,5 | 0,65 → 0,44 → 0,13 | 1,6 → 1,1 → 0,3 |
| 6 | S1 | 0,15 | 349,0 → 349,0 → 349,0 | 0,82 → 0,70 → 0,55 | 2,0 → 1,7 → 1,4 |
| 6 | S1 | 0,30 | yok → yok → yok | yok → yok → yok | yok → yok → yok |
| 6 | S2 | 0,05 | 372,0 → 237,5 → 0,0 | 1,47 → 0,85 → 0,02 | 3,5 → 2,1 → 0,0 |
| 6 | S2 | 0,15 | 481,0 → 346,5 → 26,0 | 1,88 → 1,10 → 0,11 | 4,3 → 2,7 → 0,3 |
| 6 | S2 | 0,30 | 506,5 → 372,0 → 77,5 | 2,11 → 1,27 → 0,30 | 4,8 → 3,1 → 0,7 |
| 6 | S3 | 0,05 | 660,0 → 105,0 → 105,0 | 7,17 → 0,00 → 0,00 | 15,0 → 0,0 → 0,0 |
| 6 | S3 | 0,15 | 660,0 → 105,0 → 105,0 | 7,17 → 0,00 → 0,00 | 15,0 → 0,0 → 0,0 |
| 6 | S3 | 0,30 | 660,0 → 105,0 → 105,0 | 7,17 → 0,00 → 0,00 | 15,0 → 0,0 → 0,0 |
| 7 | S1 | 0,05 | 254,5 → 156,0 → 0,0 | 0,39 → 0,20 → 0,01 | 1,0 → 0,5 → 0,0 |
| 7 | S1 | 0,15 | 323,5 → 254,5 → 127,0 | 0,51 → 0,34 → 0,13 | 1,3 → 0,8 → 0,3 |
| 7 | S1 | 0,30 | yok → yok → yok | yok → yok → yok | yok → yok → yok |
| 7 | S2 | 0,05 | 267,0 → 87,0 → 0,0 | 0,79 → 0,31 → 0,02 | 2,0 → 0,8 → 0,0 |
| 7 | S2 | 0,15 | 389,5 → 116,0 → 0,0 | 1,04 → 0,42 → 0,02 | 2,6 → 1,0 → 0,0 |
| 7 | S2 | 0,30 | 418,5 → 238,0 → 0,0 | 1,21 → 0,57 → 0,02 | 3,0 → 1,4 → 0,0 |
| 7 | S3 | 0,05 | 151,0 → 118,0 → 118,0 | 2,21 → 0,00 → 0,00 | 5,0 → 0,0 → 0,0 |
| 7 | S3 | 0,15 | 430,5 → 118,0 → 118,0 | 2,68 → 0,00 → 0,00 | 5,9 → 0,0 → 0,0 |
| 7 | S3 | 0,30 | 430,5 → 118,0 → 118,0 | 2,68 → 0,00 → 0,00 | 5,9 → 0,0 → 0,0 |

İki uçta da olurlu 48 hücrede düşükten yükseğe geçişte ortalama değişim: Virtual OSCE net saati −291,5, DUS kaybı −2,60 yüzde puanı, gün-B −5,9 gün.

## 5. S3'ün olurluğu

**Tablo 5 — DUS öncesi pay 0 iken koşulun sağlandığı çekim oranı, % (kaynak: pay0_olurluk.csv).** Eşik 90.

| h3 | yük | açık | düşük ω, boş 0 | orta ω, boş 0 | yüksek ω, boş 0 | orta ω, boş 3 | orta ω, boş 7 |
|---|---|---|---|---|---|---|---|
| 6 | K1 | 0,05 | 81,3 | 89,4 | 94,7 | 87,8 | 84,0 |
| 6 | K1 | 0,15 | 81,2 | 89,2 | 94,7 | 87,6 | 84,0 |
| 6 | K1 | 0,30 | 81,1 | 89,1 | 94,6 | 87,2 | 83,8 |
| 6 | K2 | 0,05 | 83,7 | 91,9 | 95,9 | 90,9 | 88,9 |
| 6 | K2 | 0,15 | 83,5 | 91,7 | 95,7 | 90,7 | 88,7 |
| 6 | K2 | 0,30 | 83,1 | 91,2 | 95,5 | 90,3 | 88,4 |
| 6 | K3 | 0,05 | 90,7 | 96,2 | 98,9 | 95,4 | 93,5 |
| 6 | K3 | 0,15 | 90,3 | 96,2 | 98,8 | 95,4 | 93,3 |
| 6 | K3 | 0,30 | 90,0 | 96,2 | 98,7 | 95,2 | 93,1 |
| 7 | K1 | 0,05 | 80,3 | 88,2 | 93,4 | 85,7 | 82,7 |
| 7 | K1 | 0,15 | 80,2 | 87,9 | 93,4 | 85,4 | 82,6 |
| 7 | K1 | 0,30 | 79,9 | 87,6 | 93,4 | 84,9 | 82,2 |
| 7 | K2 | 0,05 | 87,1 | 94,2 | 97,8 | 93,3 | 91,5 |
| 7 | K2 | 0,15 | 86,9 | 94,2 | 97,8 | 93,1 | 91,4 |
| 7 | K2 | 0,30 | 86,7 | 94,0 | 97,8 | 93,0 | 91,4 |
| 7 | K3 | 0,05 | 93,3 | 97,5 | 98,8 | 97,1 | 95,6 |
| 7 | K3 | 0,15 | 93,0 | 97,5 | 98,8 | 97,0 | 95,5 |
| 7 | K3 | 0,30 | 92,8 | 97,5 | 98,8 | 96,9 | 95,5 |

Açık düzeyi oranı en çok 0,7 puan oynatır. Eşiği her h3 ve açıkta geçen yükler: düşük aktarımda K3; orta aktarımda K2, K3; yüksek aktarımda K1, K2, K3.

## 6. Duyarlılık

**Tablo 6 — K2, orta aktarım; hücre: D1 / D2 · net saat · DUS kaybı % (kaynak: duyarlilik.csv).**

| h3 | sıralama | açık | ana (eL = 0,83) | eL = 1,0 | κN alt yarı | κN üst yarı |
|---|---|---|---|---|---|---|
| 6 | S1 | 0,05 | 0,5 / 1 · 226,0 s · %0,44 | 0 / 1 · 103,0 s · %0,20 | 0 / 0,25 · 26,0 s · %0,06 | olurlu değil (en iyi %89,2) |
| 6 | S1 | 0,15 | 1 / 1 · 349,0 s · %0,70 | 0,5 / 0,75 · 200,5 s · %0,33 | 0 / 0,75 · 77,5 s · %0,16 | olurlu değil (en iyi %81,4) |
| 6 | S1 | 0,30 | olurlu değil (en iyi %86,0) | 0,75 / 1 · 287,5 s · %0,51 | 0,25 / 1 · 164,5 s · %0,32 | olurlu değil (en iyi %75,4) |
| 6 | S2 | 0,05 | 0,25 / 1 · 237,5 s · %0,85 | 0 / 0,75 · 77,5 s · %0,34 | 0 / 0 · 0,0 s · %0,02 | 0,75 / 1 · 506,5 s · %1,81 |
| 6 | S2 | 0,15 | 0,5 / 0,75 · 346,5 s · %1,10 | 0 / 1 · 103,0 s · %0,45 | 0 / 0 · 0,0 s · %0,02 | 1 / 0,75 · 615,5 s · %2,25 |
| 6 | S2 | 0,30 | 0,5 / 1 · 372,0 s · %1,27 | 0,25 / 0,75 · 212,0 s · %0,63 | 0 / 0 · 0,0 s · %0,02 | 1 / 1 · 641,0 s · %2,48 |
| 6 | S3 | 0,05 | 0 / 0 · 105,0 s · %0,00 | 0 / 0 · 105,0 s · %0,00 | 0 / 0 · 105,0 s · %0,00 | 0,5 / 0 · 660,0 s · %6,18 |
| 6 | S3 | 0,15 | 0 / 0 · 105,0 s · %0,00 | 0 / 0 · 105,0 s · %0,00 | 0 / 0 · 105,0 s · %0,00 | 0,5 / 0 · 660,0 s · %6,18 |
| 6 | S3 | 0,30 | 0 / 0 · 105,0 s · %0,00 | 0 / 0 · 105,0 s · %0,00 | 0 / 0 · 105,0 s · %0,00 | 0,5 / 0 · 660,0 s · %6,18 |
| 7 | S1 | 0,05 | 0,25 / 0,75 · 156,0 s · %0,20 | 0 / 0,75 · 87,0 s · %0,12 | 0 / 0 · 0,0 s · %0,01 | 0,75 / 1 · 323,5 s · %0,43 |
| 7 | S1 | 0,15 | 0,5 / 1 · 254,5 s · %0,34 | 0 / 1 · 116,0 s · %0,16 | 0 / 0 · 0,0 s · %0,01 | olurlu değil (en iyi %88,8) |
| 7 | S1 | 0,30 | olurlu değil (en iyi %89,8) | 0,75 / 0,5 · 265,5 s · %0,30 | 0,25 / 0,25 · 98,0 s · %0,12 | olurlu değil (en iyi %79,8) |
| 7 | S2 | 0,05 | 0 / 0,75 · 87,0 s · %0,31 | 0 / 0,5 · 58,0 s · %0,19 | 0 / 0 · 0,0 s · %0,02 | 0,5 / 0,75 · 389,5 s · %0,88 |
| 7 | S2 | 0,15 | 0 / 1 · 116,0 s · %0,42 | 0 / 0,75 · 87,0 s · %0,28 | 0 / 0 · 0,0 s · %0,02 | 0,5 / 1 · 418,5 s · %1,02 |
| 7 | S2 | 0,30 | 0,25 / 0,75 · 238,0 s · %0,57 | 0 / 0,75 · 87,0 s · %0,28 | 0 / 0 · 0,0 s · %0,02 | 0,75 / 1 · 570,0 s · %1,45 |
| 7 | S3 | 0,05 | 0 / 0 · 118,0 s · %0,00 | 0 / 0 · 118,0 s · %0,00 | 0 / 0 · 111,5 s · %0,00 | 0 / 0,25 · 151,0 s · %1,98 |
| 7 | S3 | 0,15 | 0 / 0 · 118,0 s · %0,00 | 0 / 0 · 118,0 s · %0,00 | 0 / 0 · 111,5 s · %0,00 | 0 / 0,25 · 151,0 s · %1,98 |
| 7 | S3 | 0,30 | 0 / 0 · 118,0 s · %0,00 | 0 / 0 · 118,0 s · %0,00 | 0 / 0 · 111,5 s · %0,00 | 0 / 0,25 · 151,0 s · %1,98 |

Dil yükü kalkınca (eL = 1) olurlu hücre sayısı 144 → 162; ikisinde de olurlu hücrelerde ortanca değişim −40,0 saat ve −0,10 yüzde puanı. κN'nin alt yarısında (Virtual OSCE kapsamı küçük) 162, üst yarısında 117 hücre olurlu; üst yarı ortanca 389,5 saat ve 0,87 yüzde puanı daha pahalı.

## 7. Yorum kararları

- sim.py'den `sample_params`, `derive`, `Mint`, `Lload`, `ref_sim` içe aktarıldı; `ref_sim` tek sınavlı takvim kurduğundan gün döngüsü `yurut` içinde aynı kurallarla yinelendi.
- Boş günler ilk sınav gününden başlar (0 = sınav günü de çalışılır); hafif hafta takvimi 0. güne bağlıdır; ana tablodaki T ve ψ kullanılmadı.
- e(t) ve net saat aynı payla bölünür; gN0 = Pgeç − açık.
- Eşitlikte sıra: ortalama DUS P, olurluk oranı, daha çok boş gün.
- Kayıp = 1 − ort. P / ort. P(temel); hafta = payın sıfırdan büyük olduğu günlerin takvim aralığı.
- "Kaç güne denk" iki biçimde okunabildiğinden ikisi de verildi; gün-A, K2'de 42 günlük hafif hafta döngüsünün aynı evresinde okundu.
- κN yarıları ortancadan bölündü; karar kuralı her yarıda yeniden uygulandı.

## 8. Sınamalar (kaynak: sinamalar.csv)

| sınama | sonuç | sayı | eşik | ne sınandı |
|---|---|---|---|---|
| motor_ref_sim_esitligi | geçti | 0 | <1e-9 | yurut ile sim.ref_sim: temel takvimde e(t), f1, f2 farkı |
| pay0_omega0_gD_temel | geçti | 4,7e-15 | <1e-9 | bütün paylar 0, ω = 0: gD ve P temel koşuyla aynı |
| S3_pay00_P_temel | geçti | 4,7e-15 | <1e-9 | S3, DUS öncesi pay 0: DUS P = temel |
| pay1_omegaND0_gD_yalniz_unutma | geçti | 2,5e-16 | <1e-9 | pay 1, ωND = 0: gD(332) = 0,3·(1 − 1/τG)^332 |
| omega1_eL1_SN_esit_S_iki_stok_ayni | geçti | 0 | <1e-9 | ω = 1, eL = 1, S_N = S: iki stok aynı ilerler |
| yorgunluk_ve_e_paydan_bagimsiz | geçti | 0 | =0 | e(t), f1, f2 paylardan önce bir kez hesaplanır; pay koşularından sonra diziler değişmedi |
| net_saat_korunumu | geçti | 0 | <1e-9 | pay 1 iken Virtual OSCE net saati = toplam net saat |
| gun_esdegeri_egrisi_k0 | geçti | 4,7e-15 | <1e-9 | k = 0 iken iki gün eğrisi de temel P |
| olurluk_payla_azalmaz | geçti | 0 | =0 | pay artınca olurluk oranı düşen seçenek sayısı |
| olurluk_omegayla_azalmaz | geçti | 0 | =0 | ω artınca olurluk oranı düşen seçenek sayısı |
| cokus_orani | geçti | 0 | bilgi | herhangi bir takvimde çöküşe giren çekim oranı |
| K1_K0_ayni_politika | geçti | 1 | bilgi | K1 sağlam politikası K0 ile aynı mı (1 = evet) |
| kabul_sayisi | geçti | 1000 | >=1000 | h3 başına kabul edilmiş çekim (tohum 101) |

## 9. Sunum cümlesi

"Bu tablo ölçüm değil: aynı günlük yük iki sınava bölünürse, varsayılan aktarım ve kapsam oranlarıyla DUS'tan ne gittiğini söyleyen bir hesap. Güvenilecek kısım yöndür: erken sapma geç sapmadan ucuzdur; önce DUS sıralamasının bedava olup olmadığını aktarım oranı ile DUS sonrası 29 günün yetip yetmediği belirler, ikisi de ölçülmemiştir. Kaybın küçüklüğü modelin doygunluk varsayımından gelir; sıralama sınavında küçük bir P farkının değerini model söylemez."
