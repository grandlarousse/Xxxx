# Model tanımı (v2, yöntem denetiminden sonra)

Bu model **ölçüm değil, varsayımları tutarlı bir programa çeviren hesap aracıdır**. Bütün parametreler "örnekleyici"dir. Yöntem denetimi (E1) v1'de döngüsellik buldu: sürdürülebilir üst sınır girdiydi ve çıktı olarak geri geliyordu. v2'de bu sınır açık bir **senaryo ekseni**dir; raporda her sayının yanına onu doğuran girdi yazılır. Modelin kendi katkısı biçimdir: pişmanlık eğrisinin asimetrisi, amaçlar arası fark, kısa ufukta ne kadar yüklenilebildiği, hangi parametrenin ölçülmesi gerektiği.

## 1. Zaman ve politika

Adım: gün. Ufuk H; sınav H+1. günün sabahı. Ufuklar: 30, 90, 120, 150, 180, 270, 360.

Politika π = (hA, hB, d, n, T, ψ):
- `hA`: çalışma gününde yüksek talepli net saat (yeni konu, soru/vaka, aktif geri çağırma): 1–10, adım 0,5.
- `hB`: düşük talepli net saat (video, okuma, hafif tekrar): 0, 1, 2, 3.
- `d`: haftada çalışma günü: 5, 6, 7.
- `n`: hafif hafta: yok, 6, 4, 3 haftada bir; hafif haftada saatler × 0,5.
- Son dönem: `T` ∈ {0, 3, 7, 14} gün, saat çarpanı `ψ` ∈ {0,5; 0,75; 1,25} (T=0 ise ψ=1). ψ>1 son hızlanmadır.

## 2. Gün içi üretim ve yük

- Marjinal verim: `m(u) = 1/(1 + (u/u50)^s)`.
- Etkili saat: `E_A = ∫_0^hA m`, `E_B = eB · ∫_hA^(hA+hB) m`.
- Yük: `W = ∫_0^hA c + cB · ∫_hA^(hA+hB) c`, `c(u) = 1 + γ·max(0, u − h0)`.
- `L(h)`: yalnız yüksek talepli h saatin yükü (hB=0).

## 3. Yorgunluk (boyutsuz, gözlenebilir eşiklerle)

- Fazla yük: `x(t) = max(0, W(t) − L(h0))`.
- Akut: `f1(t+1) = (f1(t) + x(t)) · exp(−1/τ1)`.
- Kronik: `f2(t+1) = f2(t) · exp(−1/τ2) + max(0, f1(t+1) − a)`.
- Sabah verimi: `q(t) = 1/(1 + b1·f1(t) + b2·f2(t))`.

Ölçekler şu gözlenebilir eşiklerden türetilir (κ katsayıları yok):
- `h0`: hiç taşınmayan günlük yük.
- `h1 = h0 + v1·(h3 − h0)`: haftada 6 gün çalışırken kronik birikimin başladığı saat. `a`, 6 gün h1 + 1 gün dinlenme döngüsünün durağan hâlindeki en yüksek sabah f1 değeridir.
- `h3`: haftada 6 gün, hafif haftasız **süresiz** sürdürülebilen tavan. `Fcrit`, bu rejimin durağan en yüksek f2 değeridir. **Senaryo ekseni: h3 ∈ {5, 6, 7, 8}.**
- `q1`: f1 = a iken sabah verimi → `b1 = (1/q1 − 1)/a`.
- `qK`: f2 = Fcrit iken verim → `b2 = (1/qK − 1)/Fcrit`.

**Uçurum:** bir sabah f2 ≥ Fcrit ise çöküş: q × `qcol`, uygulanan saat planın yarısı, τ2 üç katı; f2 < 0,3·Fcrit olunca çıkılır.

**Yavaş birikim senaryosu (Y):** `f3(t+1) = f3(t)·exp(−1/120) + λ·f2(t+1)`; uçurum ve q hesabında f2 yerine f2+f3. λ ∈ {0 (temel), 0,02, 0,05}. Her λ için 90 ve 360 günlük sürdürülebilir tavan çıktı olarak raporlanır. λ=0'da model 90 günden sonra ufuk etkisi üretmez; bu bir varsayımdır.

## 4. Bilgi

`g(t+1) = g(t) − g(t)/τG + (e(t)/S)·(1 − g(t))`, `e(t) = q(t)·(E_A+E_B)` (uygulanan saatlerle).
- S ve τG birlikte kabul edilir: hA=6, d=6, q=1, g0=0,3 ile 180 günde g ∈ [0,65; 0,90] olmalı.
- Virtual OSCE kapsamı: `S_N = κN·S`.
- Yorgunluk ve e(t) bilgiye bağlı değildir; bir kez hesaplanır, g ayrı yürütülür.

## 5. Amaçlar

- (a) `Σ e(t)`.
- (b1) DUS: `P = g(H)·exp(−(e1·f1(H)/a + e2·f2(H)/Fcrit))` en yüksek. Ayrıca e1=e2=0 referans koşusu.
- (b2) Virtual OSCE: `Pr = Φ((P − Pgeç)/σP)`. Pr ≥ 0,95 sağlayan politikalar içinde **önce en düşük K, sonra en az toplam saat, sonra en düşük tepe f2**. Ek karar değişkeni: başlangıç gecikmesi D ∈ {0, H/4, H/2, 3H/4}. Açık senaryoları: Pgeç − g0 = 0,05 / 0,15 / 0,30. Çıktı: "açık → gereken toplam net saat ve günlük saat" tablosu.

## 6. K seviyeleri (toparlanma süresiyle; tol = 0,02, duyarlılık 0,01 ve 0,05)

- **K0:** her sabah q ≥ 1 − tol.
- **K1:** haftalık dinlenme gününün ertesi sabahı q ≥ 1 − tol (d ≤ 6).
- **K2:** her hafif haftanın ertesi sabahı q ≥ 1 − tol (n sonlu), çöküş yok.
- **K3:** sınava kadar çöküş yok ve en yüksek (f2+f3) ≤ 0,8·Fcrit.

Kümeler iç içedir (K0 ⊂ K1 ⊂ K2 ⊂ K3). Her K için: kısıtı sağlayan en yüksek toplam saat (tavan) ve amaca göre en iyi politika.

## 7. Parametreler (hepsi örnekleyici)

| Parametre | Anlam | Aralık | Dayanak |
|---|---|---|---|
| h3 | süresiz sürdürülebilen tavan (6 gün/hafta) | senaryo: 5, 6, 7, 8 | dolaylı: müzikte günde 3,5 saat yalnız pratik (alt uç); 6–7 saatlik laboratuvar günleri; baro ve USMLE'de 8–11 brüt saatlik haftalar süren dönemler (üst uç) |
| h0 | taşınmayan günlük yük | 3 – min(5,5; h3−1) | dolaylı: 3'e karşı 6 saatlik iş yükü deneyi |
| v1 | h1'in h0–h3 arasındaki yeri | 0,25–0,75 | görüş |
| u50, s | gün içi verim eğrisi | 4–10; 2–6 | zayıf; dayanak testleri bağlamıyor |
| eB, cB | pasif çalışmanın göreli verimi ve yükü | 0,3–0,7; 0,3–0,8 | dolaylı (test etkisi 1,5–2 kat; yük için veri yok) |
| γ | geç saatlerin ek yükü | 0–0,4 | görüş |
| τ1 | akut zaman sabiti | 0,5–2 gün | dolaylı (tek gecelik uykusuzluk 1–2 gecede düzelir) |
| τ2 | kronik zaman sabiti | 7–28 gün | dolaylı (tatil etkisi 1–4 haftada söner; spor modellerinde 1–20 gün) |
| q1, qK, qcol | eşiklerde verim | 0,93–0,99; 0,6–0,9; 0,3–0,6 | görüş |
| τG | saklama zaman sabiti | 90–400 gün | dolaylı |
| S | kapsam | öğrenme dayanağıyla kabul | görüş |
| κN | Virtual OSCE kapsamı / DUS kapsamı | 0,25–0,6 | görüş |
| e1, e2 | sınav günü kaybı (eşikte) | 0–0,03; 0–0,10 | dolaylı |
| Pgeç | geçmek için gereken doğru oranı | 0,64–0,69 | resmî (NDEB 2024 teknik raporu) |
| σP | sınav günü gürültüsü | 0,03–0,05 | görüş |

## 8. Hesap planı

- Latin hiperküp, senaryo başına en az 1.000 kabul edilmiş çekim; iki tohum.
- Maliyet: (çekim, taban politika) başına 360 günlük tek koşu; her ufuk ve son dönem seçeneği, o koşunun H−T günündeki durumundan devam ettirilir.
- Hücre = ufuk × amaç × K × h3 senaryosu.

**Raporlanacaklar**
1. Başlık: **sağlam politika** (çekimler üzerinde beklenen pişmanlığı en küçük; pişmanlık = 1 − J/J*), hA ve hB ayrı, d, n, T, ψ.
2. Pişmanlık eğrisi: sağlam politikanın −2 … +2 saat çevresinde ortalama ve %95'lik pişmanlık.
3. Çekim başına optimumun ortancası ve çeyrekler arası aralığı; adı "varsayım aralığı". Hassasiyet 0,5 saat.
4. Politika başına uçuruma düşme olasılığı.
5. Duyarlılık: kısmi sıra korelasyonu ve her parametrenin alt/üst yarısında optimum.
6. Önsel ile kabul edilen çekimlerin marjinalleri, kabul oranları.
7. Marjinal sınama: sağlam politikada ufkun ortasındaki bir güne +0,5 saat; "aynı gün kazanç / sonraki kayıp".
8. (a) ile (b1) en iyi politikalarının örtüşme oranı; e=0 referansı.
9. (b2) açık tablosu ve karar kuralı.
10. Y senaryosunda 90 ve 360 günlük tavan.

**Şart sınamalar:** W ≤ L(h0) ise f ≡ 0 ve q ≡ 1; s=2'de E = u50·arctan(h/u50); durağan f1'in kapalı biçimi; g'nin durağan değeri; K0 ≤ K1 ≤ K2 ≤ K3; 0,25 saatlik ızgarada yakınsama; ızgara sınırına yapışan optimum oranı; iki tohumun uyumu.

## 9. İki sınav uzantısı (ayrı koşu)

- Tarihler (bugün 26.11.2026): Virtual OSCE 1 Mart 2027 (95. gün), 20 Mayıs 2027 (175. gün), 22 Kasım 2027 (361. gün); DUS 24 Ekim 2027 (332. gün).
- Sıralamalar: S1 = OSCE 95 → DUS 332; S2 = OSCE 175 → DUS 332; S3 = DUS 332 → OSCE 361.
- İki ustalık oranı gD, gN. Bir sınav için yapılan etkili saatin ω kadarı ötekine de yazılır; ω senaryo: 0,2 / 0,4 / 0,6.
- İngilizce çalışma verim çarpanı eL = 0,83 (ikinci dilde çalışma yaklaşık %20 uzun sürer; Felemenkçe–İngilizce verisi).
- Dönem başına Virtual OSCE payı: 0, 0,25, 0,5, 0,75, 1.
- Amaç: Pr(Virtual OSCE geçme) ≥ 0,95 koşuluyla DUS sınav günü P en yüksek. Yorgunluk ortaktır.

## 10. Bilinen sınırlar

- Uçurumun yeri girdidir, bulgu değildir.
- λ=0'da 90 günden sonra ufuk etkisi yoktur; uzun ufuktaki temkin literatürden ve Y senaryosundan gelir.
- Uyku modelde yok: bütün sonuçlar yeterli uyku (yaklaşık 8 saat ve üstü yatak süresi) koşuluna bağlıdır.
- Deneme sınavı günleri, rampa ve tekrar yükünün g ile büyümesi modellenmez.
- Zaman sabitleri bilişsel iş için ölçülmemiştir.
- Pr ≥ 0,95 yalnız sınav günü gürültüsünü kapsar; parametre belirsizliğini değil.
