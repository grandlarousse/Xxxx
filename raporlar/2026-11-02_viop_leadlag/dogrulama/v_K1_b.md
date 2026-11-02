# v_K1_b — İkinci bağımsız doğrulama (çürütme): K1 açılış gap-fade

Kod: `/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b/` (kb.py kendi yükleyicim; ll.py ve v_K1_a/vk.py import EDİLMEDİ). b1..b15 betikleri, res_b*.csv çıktıları.
Tanım: cc=log(adj/adj₋₁), intra=log(c/o), gap=cc−intra. Fiyat bazında ±%10,5 dışı (cc veya gap) → atılır; v=0 ve o∉[l,h] → atılır. **2023-02-08 satırı silindi** (bkz. veri tuzakları). Strateji: |gap|>%1 → −sign(gap)×getiri − maliyet. IS 2014–20, OOS 2021–26, NW(5) t.

## Hüküm: DÜZELT — güven DÜŞÜK (işlenebilir iddia için)
Açılış müzayedesi fiyatıyla ölçülen etki gerçek ve 1. aşamanın sandığından daha sağlam. Ama "VİOP ile işlenebilir hisseye özgü etki" kısmı çürüyor. 10:30 girişli CIMSA kârının yaklaşık yarısı tesadüfi XU030 hareketinden geliyor. Hedge'lenince t 1,2.

## 1. Yeniden üretim (iddia ile birebir)
| | CIMSA | OYAKC |
|---|---|---|
| IS 14–20 net10 | +28,0 (t2,54, n287) | +37,5 (t2,09) |
| IS 16–20 | +54,4 (t2,89) | +45,6 (t1,76) |
| OOS 21–26 | **+62,5 (t3,22, n230)**, medyan +47,6, isabet %55 | **+39,7 (t2,19)**, medyan +9,5, isabet %51,5 |
| Pozitif yıl | 12/13 (2014 +0,3 / 2015 +1,1: bozuk açılış yılları) | 12/13 |

## 2. 1. aşamaya düzeltme: uç değer bağımlılığı abartılmış
1. aşamanın "en iyi 10 işlem atılınca t 1,25" testi asimetrik: sadece kazananları atıyor. Simetrik kırpma şöyle:
- CIMSA OOS: 10+10 kırpma **+51 (t2,91)**, 20+20 kırpma +44,5 (t3,03), winsor 1/99 +43,6 (t2,47).
- OYAKC OOS: 10+10 kırpma +32 (t2,26), winsor +29,7 (t1,89).

Açılış versiyonu birkaç işleme bağlı değil (CIMSA'da medyan da +48).

## 3. Plasebolar
- Gün karıştırma (yıl içi, 2.000 tekrar): CIMSA p=0,000, OYAKC p=0,0045.
- Başka hissenin gap'i → CIMSA intra (46 hisse): hiçbiri CIMSA'nın kendi gap'ine ulaşmıyor; medyan −12,8.
- Bayat sinyal gap₍t−1₎: CIMSA OOS +35,6 (t1,74), kısmen pozitif. Çok günlük dönüş rejimi ya da yüksek oynaklık dönemi etkisi olabilir. gap₍t−2₎: −18.
- Dairesel kaydırma, 47 hisse ortak (OOS max-t): CIMSA p=0,02, OYAKC p=0,27.
- Ortak faktör (açılış versiyonu): idio gap + XU030 hedge OOS'ta CIMSA +60,6 (t2,38), OYAKC +42,7 (t1,69). Piyasa gap işareti tek başına +13 (t0,5). **Açılış etkisi hisseye özgü.**

## 4. Bid-ask / açılış gürültüsü testi
Saatlik veri, 2023-12..2026-10, 47 hisse, 32.926 hisse-gün:

| Eğim (gap üzerine) | Hepsi | Düşük lik. | Yüksek lik. |
|---|---|---|---|
| açılış→10:30 (r1) | −0,049 (t−4,4) | −0,072 (t−3,2) | −0,029 (t−1,7) |
| 10:30→kapanış (r2) | −0,034 (t−1,7) | **−0,078 (t−2,5)** | −0,012 |
| r2 ~ gap + r1: gap | −0,029 (t−1,5) | −0,074 (t−2,4) | −0,008 |
| r2 ~ gap + r1: r1 | **+0,096 (t5,8)** | +0,046 | +0,148 (t4,9) |

- İlk 30 dakika devam ediyor, geri sekmiyor (gün-içi momentum). Bu bid-ask sıçramasının tersi.
- Yüksek likiditede açılış fade'i **−20 bps** (gap momentumu). Mekanik gürültü evrensel olsaydı burada da ≥0 olurdu.
- Spearman corr(gap, intra), 2021+: medyan **+0,019**, sadece 14/47 negatif. Pearson medyanı −0,048 (44/47 negatif). Negatif korelasyon kuyruklardan (büyük gap dönüşleri) geliyor; kütlede tik düzeyinde sıçrama yok.
- **Ama illikit hisselerde müzayede gürültüsü var.** 5 dk verisinde (Ağu–Eki 2026, 2.788 hisse-gün) düşük likidite tercilinde müzayede→10:05 Fama-MacBeth eğimi −0,33 (t−5,1). Brüt 26,6 bps fade'in 18,5 bps'i ilk 5 dakikada. Saatlik veride düşük likidite fade'inin ~%40'ı 10:30'dan önce. Bu kısım VİOP için işlenemez. Not: 60 gün kısa ve fon krizi dönemini içeriyor; orta/yüksek likiditede bu dönemde hiç dönüş yok.
- Koordinatör aralığı yanlış, 1. aşama haklı: Pearson 2021+ −0,116..+0,030, medyan −0,048.

## 5. İşlenebilir versiyon (10:30 TSİ girişi) — çürüyen kısım
| | CIMSA | OYAKC | Düşük lik. havuzu (listeli günler) | 47 hisse havuzu |
|---|---|---|---|---|
| net10 | +58,6 (t2,52); listeleme sonrası +61,5 (t2,65, n89) | +33,6 (t2,49) | +15,1 (t1,47) | +5,8 (t0,8) |
| net15 | +56,5 (t2,43) | +28,6 (t2,12) | +10,1 (t0,98) | +0,8 |
| net10 + 1 tik aleyhte | +55,0 (t2,37) | +25,9 (t1,91) | +6,6 (t0,65) | −2,3 |
| 17:30 çıkış (kapanış müzayedesi yok) | +49 (t2,08) | +34,7 (t2,53) | +5 | −0,5 |
| **XU030 hedge'li, β=1, net13** | **+25,6 (t1,20)** | **+6,3 (t0,37)** | +7,6 (t0,86) | +1,6 |

- İşlem günlerinde −sgn(gap)×XU030 katkısı CIMSA'da 29 bps (brüt 69'un içinde), OYAKC'de 24 bps (brüt 44'ün içinde).
- XU030'un kendi gap'i 10:30 sonrasını öngörmüyor (|gap|>%1: +11,8, t0,86; >%0,5: −10, t−0,9). Yani bu katkı beklenen değer değil, tesadüf.
- Yön karışımı (net short eğilimi) sadece 4 bps açıklıyor.
- 47 hissede 10:30 girişi:
  - Ham: 20/47 pozitif, medyan −2,5. Dairesel kaydırma max-t p: CIMSA 0,25, OYAKC 0,26.
  - Hedge'li: 22/47 pozitif, CIMSA p=0,80.
  - BH'yi geçen yok.
- **Dürüst holdout.** Hisseler 2016-01..2023-11 açılış t-değerine göre seçilip 2023-12+ 10:30 girişte test edildi:
  - Kesit kalıcılığı gerçek: Spearman 0,40 (p=0,005). CIMSA pre dönemde 2. sıradaydı ve tuttu.
  - Ama BIMAS 1. sıradaydı ve tutmadı (−4,8).
  - Portföyler: üst 3 +19 (t1,29), üst 10 +14,4 (t1,57), üst 15 +13,9 (t1,70).
- Yarıyıl: CIMSA ham ve hedge'li 5/7 pozitif; OYAKC hedge'li 4/7; düşük likidite hedge'li 3/7.

## 6. VİOP kontrat gerçekliği (birincil kaynak: BIST viop_YYYYMMDD.csv bültenleri, 2.422 dosya)
- **CIMSA pay vadelisi ilk kez 09.02.2024'te işlem görüyor** (BIST/GCM duyurusu da 09.02.2024 diyor). İddianın OOS 2021–2024/01 kısmı VİOP'ta işlenemezdi.
- OYAKC 16.10.2020'den beri listeli. DOAS 09.02.2024, BRSAN 19.04.2024, ASTOR 17.07.2023, TRALT/TRMET 24.11.2025 (kod değişimi).
- Likidite: CIMSA ön-ay 2025–26 medyanı 134–136 mn TL/gün (5,3–6,1 bin işlem). OYAKC 143–172 mn TL/gün.
- Açılış müzayedesine katılım sadece spotta mümkün (gösterge fiyatla). Spot long (gap<−%1) OOS: CIMSA +143,6 (t3,83, n52), IS +25 (t1,3). Short taraf açığa satış kısıtına takılıyor. Bu spot bir strateji; VİOP stratejisi değil.

## 7. Veri tuzakları (yeni)
- **2023-02-08:** BIST'te işlemler iptal edildi, piyasa 15.02'ye kadar kapalı kaldı. Yahoo'da bu gün o=h=l=c ve hacim küçük olan sahte bir satır var. Koordinatör panelinde (panel_decomp_bist) CIMSA gap −8,4%, intra 0 olarak duruyor; 15.02 ise sahte kapanışa göre +19,6% hesaplandığı için atılmış. Doğrusu: 08.02 silinmeli, 15.02 07.02'ye göre hesaplanmalı (CIMSA +9,5%). Bütün BIST sembollerini etkiler.
- 2014–2015 Yahoo açılışlarında CIMSA o==c günlerin %21–25'i, OYAKC %24–39'u (2021 sonrası %1–3). o==h oranı %19–29. Bu yıllar bozuk ve IS'ten çıkarılmalı.
- Saatlik barlar: 06:30 bar kapanışı = m5 07:25 kapanışı (10:30 TSİ) doğrulandı. Günlük açılış = m5 06:55 müzayede barı (%100). Kışın 14:30 barı eksik; çıkış için günlük kapanış kullanıldı.

## Güven
- Açılış müzayedesi fiyatıyla etki: CIMSA **ORTA**, düşük likidite havuzu **ORTA**, OYAKC **DÜŞÜK**.
- VİOP'ta işlenebilir 10:30 versiyonu: CIMSA **DÜŞÜK** (hedge'li t1,2, 2,7 yıllık kontrat geçmişi), OYAKC **ÇOK DÜŞÜK**, havuz **DÜŞÜK**.
