araç: 20/30

# VS — simülasyonun bağımsız yeniden çalıştırılması ve denetimi

Denetlenen: `ek/model/sim.py` (sha256 6acc43f9…), `test_sim.py`, `cikti/*.csv`, `SONUC.md`; ölçüt `MODEL_TANIMI.md` v2, bölüm 1–8 ve 10. İki sınav uzantısı (bölüm 9) denetlenmedi. Bütün çalıştırmalar kopyada yapıldı: `/tmp/claude-0/-home-user-Xxxx/cce2406f-a3f2-53d7-8989-fb436572b9df/scratchpad/vs/` (`a/`: aynı tohumlar, `b/`: tohum 303 ve 404, `bagimsiz.py`, `denetim.py`). Bu klasör geçicidir.

## 1. Hükümler

| # | Madde | Hüküm | Sayılar |
|---|---|---|---|
| 1 | Yeniden çalıştırma | geçti | 20 CSV'nin 19'u bayt bayt aynı; istenen 5 dosyada 0 farklı hücre. Tek fark `sure.csv` (duvar süresi 276 s, depoda 287 s). pytest: 31 sınama, 24 geçti, 7 kaldı; SONUC.md ile aynı |
| 2 | Farklı tohum (303, 404) | kısmen | Sağlam hA 336 hücrenin 322'sinde aynı, 8'inde 0,5 saat, 6'sında 0,5 saatten fazla değişti. (a, b1) 224 hücrede 1; yalnız (a) 112 hücrede 0. Başlık hücresi h3 = 8: 6,0 → 6,5 |
| 3 | Tanımla karşılaştırma | geçti (notlarla) | Bölüm 2–4 denklemlerinde ve sırasında sapma yok. 13 yorum kararı; 11'i SONUC.md'de açıklanmış, 2'si açıklanmamış, ikisi de düşük etkili (2. tablo) |
| 4 | Bağımsız yeniden yazım | geçti | 45 çift (9 politika × 5 çekim), 180 gün. En büyük mutlak fark: f1 3e-15, f2 5e-14, q 4e-16, e 7e-12, g 2e-13. En büyük göreli fark 1,4e-12. Çöküş günleri 45/45 çiftte aynı |
| 5 | Özet denetimi | geçti | 94 sayı karşılaştırıldı, tutmayan 0 |
| 6 | Yorum denetimi | kısmen | Üç cümlenin sayıları CSV ile tutuyor, üçü de olduğundan kesin yazılmış. 7 gün ve hB = 0 yapı sonucu, hata değil |
| 7 | (b2) kuralı | geçti | Fark, %90'lık dilim ile ortanca arasındaki farktır: sağlam/ortanca 2,5–3,0; sağlam/p90 1,0–1,4 |

## 2. Ayrıntı

**Madde 2.** Betik tohumu tek sabitten alıyor (`SEEDS`); kopyada değiştirildi. 0,5 saatten fazla değişen 6 hücrenin hepsi h3 = 8, K1'de (4,5 → 3,5; gün 6 → 7; beşi e = 0 referansı). h3 = 5, 6, 7'de 252 hücrenin hiçbiri değişmedi. Önemli olan başlık hücresi: 180 gün, K3, (a), h3 = 8'de sağlam hA 6,0'dan 6,5'e, haftalık saat 42,5'ten 45,5'e çıktı. İki koşuda sağlam politikanın beklenen pişmanlığı 0,033 ve 0,032; kısıtı çiğneyen tek çekim 2000 çekimde 0,0005 eklediğinden seçim birkaç çekime bağlı (çıkarım). Koşu içi iki tohum sınaması bunu yakalamıyor: özgün koşuda ikisi de 6,0, yeni koşuda ikisi de 6,5. Öbür çıktılar: 1 saat aşağıda çıktı kaybı %10,9 / %9,3; +1 saatte uçurum %99 / %63 (özgün %56); 30 günlük tavan oranı 1,025 / 1,025 / 1,034 / 1,056; (b2) sağlam saat ortanca %2, en çok %21 değişti, 84 hücrenin 1'inde karar K değişti; Y senaryosu aynı.

**Madde 4.** Yeniden yazım yalnız `math` kullanır: m ve c Simpson ile, a ve Fcrit kapalı biçimle değil 6 + 1 günlük döngü durağanlığa kadar yürütülerek bulundu (200 çekimde kapalı biçimle göreli fark en çok 4e-15). sim.py'nin hızlı motoru değiştirilmedi; sabah ve gün sonu durumları izleme kancasıyla okundu. Çiftlerin 22'si çöküşe giriyor (1–9 giriş-çıkış), 5'i h3 rejimi, 20'si hafif haftalı, 15'i son dönemli (14 g × 1,25; 7 g × 0,5; 3 g × 0,75).

**Madde 6 (i) "0,67".** Sayı uç nokta eğimidir: (6,0 − 4,0)/3, 0,5 saatlik ızgarada; basamaklar +1,0, +0,5, +0,5. Öbür tohum çiftinde 0,83. K3 hücrelerinde 0,67 ya da 0,83; K0–K2'de 0,17–0,50. Haftalık ölçü daha açık: K3 sağlam haftalık saat, girdideki haftalık tavanın (6 × h3) 0,87–1,05 katı, ortanca 0,93. Öneri: "K3'te 1 saate 0,7–0,8; haftalık saat girdi tavanının yaklaşık %93'ü".

**Madde 6 (ii) "%11 / %9; %99 ve %56".** Üç kayıt gerekir. (1) Sayılar yalnız (a) amacı, K3 ve yedi ufkun ortalamasıdır; (b1) sınav günü ölçüsünde 1 saat aşağısı %3 / %2, 1 saat yukarısı %21 / %5 kayıptır (SONUC Tablo 3). (2) h3 = 6'daki %99 tanımın geri gelişidir: 5,0 + 1 = 6,0 saat × 7 gün = 42 saat, tanımda uçurumun kenarı olan 6 × 6 = 36 saatin üstündedir. h3 = 7'deki %56, ufuklara göre 0,56 / 1,00 / 0,47–0,48 değerlerinin ortalamasıdır (90 günlük hücrede 7 günlük hızlanma var). (3) Kaybın büyüklüğü (%45) çöküş kuralının görüş parametrelerinden gelir. Sağlam kalan sol taraftır: ufuklara göre çıktı oranı 0,88–0,94.

**Madde 6 (iii) "yalnız ×1,02".** Oran çok kipli bir dağılımın ortancasıdır. h3 = 6'da çekimlerin %23'ünde 1,000, %29'unda 1,023–1,025, %38'inde 1,05 ve üstü; ortalama 1,040, p90 1,08. h3 = 7'de ortanca 1,04, h3 = 8'de 1,05. 1,023 kümesi, 3 günlük × 1,25 hızlanmanın 30 güne ve 360 güne bölünmesinin aritmetiğidir; taban saat aynıdır. Altı günlük düzende K3'ün en yüksek hA'sı çekimlerin %55'inde 30 günde 0,5 saat yüksektir. Öneri: "30 günde tavan %0–8, ortalama %4 yükselir; çoğu son hızlanmanın payıdır". Yön doğru, tek sayı fazla kesin.

**Madde 6, 7 gün ve hB = 0.** h3 = 6, 180 gün, K3, (a): çekim başına optimumların %100'ü 7 gün. En iyi 6 günlük politikanın beklenen pişmanlığı 0,148, 7 günlüğün 0,028. hB > 0 çekim başına optimumların %35'inde; en iyi hB > 0 politika (4,5 + 1) 0,047. Yani 7 gün güçlü, hB = 0 zayıf bir sonuçtur. Neden: yorgunluğa yalnız günlük eşiği (h0) aşan yük yazılır ve sönüm çalışılan günde de aynıdır; boş günün kendine özgü değeri yoktur, boş gün h0 kadar bedelsiz saati kullanmamak demektir. Gösterim (ortanca parametreler, bağımsız kod), ikisi de haftada 35 saat:

| Düzen | Haftalık fazla yük | Tepe f2 / Fcrit | Haftalık etkili saat |
|---|---|---|---|
| 5,0 saat × 7 gün | 5,6 | 0,00 | 32,3 |
| 5,83 saat × 6 gün | 11,0 | 0,79 | 24,6 |

hB = 0 ise ihlalde pişmanlık 1 kuralından gelir: B saati yük başına çekimlerin yalnız %40'ında (eB > cB) daha verimli; 5,0 + 1 çekimlerin %33'ünde K3'ü çiğniyor.

**Madde 7.** h3 = 6, 19 hücre: sağlam kural / çekim başına ortanca 2,5–3,0. Aynı K için çekim başına saatin %90'lık dilimi ortancanın 2,1–2,5 katı (180 gün, açık 0,05: p50 112, p90 280, sağlam 303). Geri kalan 1,0–1,4 kat, tek bir (politika, gecikme) çiftinin kaba ızgarada bütün çekimlere yetmesi şartından gelir. Saati S (PRCC 0,97), κN (0,93) ve τG (−0,83) belirler. İki sayı farklı sorulara yanıttır; rapora ikisi de girmeli: çekim başına ortanca ve çeyrekler **"tipik varsayımda gereken en az saat"**, sağlam kural **"varsayımların %90'ında yeten tek plan (temkinli plan)"** adıyla. Başlıkta aralık verilmeli (180 gün, açık 0,05: yaklaşık 110 [80–175], temkinli 300 saat). İkisi de S önselinin ürünüdür; ölçüm değildir.

## 3. Bulunan hata ve sapmalar

| Ne | Nerede | Açıklanmış mı | Etki | Nasıl sınandı | Düzeltme ya da rapor notu |
|---|---|---|---|---|---|
| Kısıtı çiğneyen çekimde pişmanlık 1; sağlam politika fiilen "hiçbir çekimde kısıtı çiğnemeyen en yüksek saat" oluyor (ihlal 0; +0,5 saatte %57) | sim.py 353–355, 570; SONUC §2 | evet | yüksek | Tablo 3; tohum değişimi | "Sağlam"ı bu anlamıyla tanımla; h3 = 8 için 6,0–6,5 yaz |
| Haftada 7 gün yapı sonucu | tanım §3 | evet (model sınırı) | yüksek (sunum) | bağımsız kod; d = 6 pişmanlığı 0,148 | Saatleri haftalık toplam olarak ver; "7 gün çalış" önerisi çıkarma |
| "×1,02", "0,67", "%99 / %56" fazla kesin | SONUC §1, §4, §11 | hayır | orta | madde 6 | Yukarıdaki önerilen cümleler |
| K3 "tavanı" B saatlerini ve 7. günü sayar: h3 = 6'da 45,5 saat/hafta, 6 × h3 = 36 | sim.py 364; SONUC §4 | kısmen | orta (sunum) | CSV | h3 ile karıştırılmasın |
| (b2) açık ekseni uzun ufukta etkisiz: 360 günde 452 → 459 saat | tanım §4 (unutma sıfıra doğru) ve gecikme seçeneği | hayır | orta | b2_karar.csv | "Açık az önemli" diye okunmasın |
| S önseli log-tekdüze 30–1000 | sim.py 106 | evet | (b2) için yüksek, hA için düşük | PRCC | (b2) saatleri "örnek" etiketiyle |
| K kümeleri birleşimle iç içe; d = 7'de K1 = K0 | sim.py 158–167 | evet | düşük–orta | sinamalar.csv | K1 ayrı bulgu gibi sunulmasın |
| ψ hafif haftanın yerine geçer; son dönemde hafif hafta kontrolü yok | sim.py 202–204, 405, 435 | evet | düşük | bağımsız kod | — |
| Uçurum karşılaştırmasında 1e-9 pay | sim.py 265, 461 | hayır | düşük | Pay kaldırıldı: h3 rejimi 360 günde çekimlerin %6,7 (h3 = 6) ve %7,6'sında (h3 = 8) yuvarlamayla çöküyor; K3 tavanı ve K3 hA 1000/1000 çekimde aynı | SONUC §10'a not; tanım eşitlikte bıçak sırtı |
| (b2) sağlam kuralda eşitlik bozucu tepe f2 değil hA + hB | sim.py 785 | hayır | düşük | kod okuma | not |
| Koşu düzeyi 7 sınama kalıyor: hB = 3 sınırı çekim başına optimumların %13,2'sinde bağlayıcı; 0,25 ızgara J* +%1,6 | sinamalar.csv | evet | düşük–orta | pytest | — |
| "7 günden az hücre 3" yalnız (a, b1) için; e = 0 ile 10 | SONUC §2 | kısmen | düşük | ana_tablo.csv | — |

Hesap hatası bulunmadı.

## Rapora bu sonuçlar hangi kayıtla girebilir

Hesap yeniden üretilebilir ve tanımdaki dinamiği doğru uyguluyor; rapora "ölçüm değil, varsayım hesabı" etiketiyle girebilir. Saatler h3 senaryosuyla birlikte ve haftalık toplam olarak verilmeli (h3 = 6 için yaklaşık 35 saat/hafta; h3 = 8 için 42,5–45,5); "haftada 7 gün" ve "pasif saat 0" öneri olarak değil, model sınırı olarak anılmalı. Üç cümle düzeltilmeli: eğim 0,7–0,8; +1 saatteki uçurum olasılığı tanımdan gelir, sağlam kalan kısım 1 saat aşağıda etkili saat kaybının yaklaşık %10, sınav günü ölçüsünde %2–3 olmasıdır; 30 günlük ufuk tavanı %0–8 yükseltir. (b2) saatleri iki adla ("tipik" ve "temkinli plan") ve S önselinin ürünü olduğu söylenerek verilmeli. Uçurumun yerinin girdi olduğu ve yeterli uyku koşulu notları korunmalı.
