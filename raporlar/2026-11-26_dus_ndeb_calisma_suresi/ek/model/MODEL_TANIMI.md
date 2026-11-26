# Model tanımı (taslak v1, yöntem denetimine gidecek)

Bu model **kanıt değil, varsayımları tutarlı bir programa çeviren bir hesap aracıdır**. Bütün parametreler "örnekleyici"dir: literatürden gelen dayanak noktalarıyla sınırlanmış aralıklardan çekilir, kişiye özgü değildir. Amaç tek bir sayı bulmak değil; (1) optimumun ufka ve amaca göre hangi yöne kaydığını, (2) sonucu en çok hangi parametrenin oynattığını, (3) kalibrasyonda neyin ölçülmesi gerektiğini göstermektir.

## 1. Zaman ve karar değişkenleri

Adım: gün. Ufuk H gün; sınav H+1. günün sabahı.

Politika π:
- `hA`: tam çalışma gününde yüksek talepli net saat (yeni konu, soru/vaka çözme, aktif geri çağırma). Izgara 1–10, adım 0,5.
- `hB`: aynı gün düşük talepli net saat (video, okuma, hafif tekrar). Izgara 0–4, adım 1.
- `d`: haftada çalışma günü: 5, 6, 7.
- `n`: hafif hafta sıklığı: yok, 6, 4, 3 haftada bir; hafif haftada yük oranı φ = 0,5.
- `T`: taper uzunluğu: 0, 3, 7, 14 gün; taperde yük oranı ψ = 0,5.

## 2. Gün içi üretim

Günün u. net saatinin marjinal verimi: `m(u) = 1 / (1 + (u/u50)^s)`.
- `u50`: marjinal verimin yarıya düştüğü saat. `s`: eğrinin dikliği.
- Etkili saat: `E_A = ∫_0^hA m(u) du`, `E_B = eB · ∫_hA^(hA+hB) m(u) du`. `eB`: pasif çalışmanın göreli verimi.

Günlük yük (yorgunluk girdisi): `W = ∫_0^hA c(u) du + cB · ∫_hA^(hA+hB) c(u) du`, `c(u) = 1 + γ · max(0, u − uθ)`. Geç saatler daha pahalıdır. `cB`: pasif çalışmanın göreli yükü.

## 3. Yorgunluk: iki bölmeli, basamaklı

- Akut: `F1(t+1) = (F1(t) + κ1 · max(0, W(t) − Wθ)) · exp(−1/τ1)`
- Kronik: `F2(t+1) = F2(t) · exp(−1/τ2) + κ2 · max(0, F1(t+1) − F1tol)`
- Ertesi günün verim çarpanı: `q(t) = 1 / (1 + β1·F1(t) + β2·F2(t))`
- **Uçurum:** `F2 ≥ Fcrit` olursa çöküş durumu: q, `qc` ile çarpılır, τ2 üç katına çıkar, yük zorunlu olarak yarıya iner; durum F2 < 0,3·Fcrit olana kadar sürer.

Mantık: `Wθ` altındaki günlük yük hiç taşınmaz. Üstündeki yük akut yorgunluk üretir; akut yorgunluk dinlenme günüyle temizlenmezse kronik bölmeye akar.

## 4. Bilgi

Ustalık oranı g ∈ [0,1] (sınav kapsamının geri çağrılabilir kısmı):
`g(t+1) = g(t) − g(t)/τG + (q(t) · (E_A + E_B) / S) · (1 − g(t))`
- `S`: kapsamın büyüklüğü (bir kez ustalaşmak için gereken etkili saat).
- `τG`: saklama zaman sabiti (aralıklı tekrar sürdürülürken).
- `(1 − g)`: sonlu kapsam, doygunluk.

## 5. Amaçlar

- (a) Toplam öğrenme: `Σ_t q(t)·(E_A+E_B)` (doygunluk ve unutma hariç brüt öğrenme).
- (b1) DUS: sınav günü performansı `P = g(H) · (1 − ε1·F1(H) − ε2·F2(H))` en yüksek.
- (b2) Virtual OSCE: `Pr(geçme) = Φ((P − Pgeç)/σP)`. Önce Pr(geçme) ≥ 0,95 koşulu, sonra en düşük toplam net saat; eşitlikte en düşük tepe F2. Başlangıç düzeyi `g0` ve `Pgeç` senaryo parametresidir (küçük / orta / büyük açık).

## 6. K seviyelerinin işlemsel tanımı

Bir parametre çekimi ve politika için, sınavsız sürekli rejimde:
- **K0:** her sabah F1 ≤ tol ve F2 = 0 (günlük yük ≤ Wθ).
- **K1:** haftalık dinlenme gününün ertesi sabahı F1 ≤ tol; F2 ≤ tol.
- **K2:** her hafif haftanın ertesi sabahı F2 ≤ tol; arada F2 < 0,5·Fcrit.
- **K3:** sınav gününe kadar F2 < 0,8·Fcrit (uçurumun altında güvenlik payıyla); sıfırlama şartı yok.

Her K için, o kısıtı sağlayan politikalar içinde amaca göre en iyisi seçilir. Kısıtsız en iyi politikanın hangi K'ya düştüğü ayrıca raporlanır.

## 7. Parametreler (geçici aralıklar; 1. dalga bulgularıyla güncellenecek)

| Parametre | Anlam | Geçici aralık | Dayanak türü |
|---|---|---|---|
| u50 | marjinal verimin yarılandığı net saat | 4–9 | dolaylı (bilinçli pratik, uzun saat çıktısı) |
| s | dikliği | 2–6 | görüş |
| eB | pasif çalışmanın göreli verimi | 0,3–0,6 | dolaylı (test etkisi, aktif öğrenme) |
| cB | pasif çalışmanın göreli yükü | 0,3–0,7 | görüş |
| Wθ | taşınmayan günlük yük (saat eşdeğeri) | 3–6 | dolaylı |
| uθ, γ | geç saatlerin ek maliyeti | uθ 3–6; γ 0,1–0,5 | görüş |
| τ1 | akut yorgunluk zaman sabiti | 1–3 gün | dolaylı (toparlanma çalışmaları) |
| τ2 | kronik yorgunluk zaman sabiti | 7–30 gün | dolaylı (Banister τ2, tatil etkisinin sönmesi) |
| κ1, κ2, F1tol | birikim katsayıları | ölçek; dayanak testleriyle sınırlanır | model |
| β1, β2 | yorgunluğun verime etkisi | q, uçurum eşiğinde 0,6–0,85 olacak biçimde | model |
| Fcrit, qc | uçurum eşiği ve çöküşte verim | qc 0,3–0,6 | dolaylı (aşırı yüklenme tanımları) |
| τG | saklama zaman sabiti | 60–400 gün | dolaylı (aralık etkisi) |
| S | kapsam büyüklüğü | DUS 400–1.500; V-OSCE 150–600 etkili saat | görüş |
| ε1, ε2 | sınav günü yorgunluk cezası | 0–0,15 | dolaylı (taper) |
| σP | sınav günü gürültüsü | 0,03–0,06 | dolaylı (ölçüm hatası) |

## 8. Dayanak testleri (çekim kabul ölçütleri)

Bir parametre çekimi şu davranışları üretmiyorsa atılır:
1. Günde 4 net yüksek talepli saat, haftada 6 gün, 360 gün: uçuruma hiç ulaşmaz.
2. Günde 7 net saat, haftada 6 gün, 6 hafta: uçuruma ulaşmaz (tıp öğrencilerinin yoğun hazırlık dönemleri).
3. Günde 12 net saat, haftada 7 gün: 12 hafta içinde uçuruma ulaşır.
4. Haftalık etkili çıktı, 6 günlük haftada günlük 10 net saatte, 8 net saattekinin en çok 1,15 katıdır (uzun saatlerde çıktı eğrisinin düzleşmesi).
5. Yük kesildiğinde F1 üç günde, uçurum altındaki F2 üç haftada başlangıcın %20'sinin altına iner; çöküşten çıkış en az 4 hafta sürer.

Bu testler de yargıya dayanır ve "örnekleyici" etiketini taşır.

## 9. Hesap ve raporlama

- Latin hiperküp ile en az 2.000 kabul edilmiş çekim.
- Her çekim × ufuk (30, 90, 120, 150, 180, 270, 360) × amaç × K için ızgarada en iyi politika.
- Raporlanan: optimum toplam net saatin (hA+hB) ortancası, çeyrekler arası aralığı, %5–95 aralığı; ayrıca **sağlam politika** (çekimler üzerinde beklenen pişmanlığı en küçük olan tek politika).
- Duyarlılık: her parametre ile optimum saat arasında kısmi sıra korelasyonu; sağlam politika için kasırga grafiği.
- Politika başına uçuruma düşme olasılığı (çekimler üzerinden); "uçurumun başladığı yer" = bu olasılığın %5'i geçtiği yük.

## 10. İki sınav uzantısı

- İki ustalık oranı: gD (DUS), gN (Virtual OSCE). Bir sınav için yapılan etkili saatin ω kadarı diğerine de yazılır (içerik örtüşmesi; aralık 0,2–0,6).
- İngilizce çalışma: verim çarpanı eL (0,75–0,95), yük çarpanı cL (1,0–1,2).
- Sıralamalar: önce DUS, önce Virtual OSCE, paralel (gün içi pay 0–1).
- Amaç: Pr(Virtual OSCE geçme) ≥ 0,95 koşuluyla DUS sınav günü performansı en yüksek. Yorgunluk bölmeleri ortaktır; ilk sınavın taperi ve sonrasındaki toparlanma ikinci sınavın rampasına yazılır.

## 11. Bilinen sınırlar

- Yapı spor bilimindeki uyarı–yanıt modelinden esinlenir; zaman sabitleri bilişsel iş için ölçülmemiştir.
- Gün içi verim eğrisi ile yorgunluk eşiği birbirinden bağımsız çekilir; gerçekte bağlı olabilirler.
- Uyku modelde örtüktür (τ1 içinde); uykudan çalınan saat ayrıca modellenmez.
- Çalışma türü yalnızca iki sınıfa ayrılır; deneme sınavı günleri ayrı modellenmez.
