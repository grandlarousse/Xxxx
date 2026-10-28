# OPSİYON — 1. Tur (28.10.2026) | Volatilite, opsiyon yapılandırma, risk/teminat

Etiketler: [D] kaynakta doğrulandı · [H] kendi hesabım (scriptler `viop/` altında) · [T] tahmin · [V] varsayım. Numaralar sondaki kaynaklara karşılık gelir.

**Hüküm:** BIST 30 opsiyonları uygulanabilir: Avrupa tipi, nakdi uzlaşmalı, ×10 TL çarpanlı. Aralık serisinde ATM civarında likidite yeterli. Pay opsiyonları ve Şubat vadesi pratikte işlem görmüyor. Uzlaşma fiyatlarından çıkan IV (~%24), 20 günlük gerçekleşen volatiliteden (RV20, %27) ve GARCH tahmininden (%31) düşük; **vol satmak için gerekçe yok**. 27–28.10'da Aralık opsiyonları ~%10–15 IV ile işlem gördü. Bu bir anomali, teyit gerekiyor; buna dayanan **koşullu long vol** fikri aşağıda.

## 0. Baseline düzeltmeleri
- "14 Eylül zirvesi 14.235,83" aslında 14.09 kapanışı. Yerel zirve 11.09'da 14.467, yılın zirvesi 11.05'te 15.134 [D,1]. 27.10 kapanışı 11.151; Investing'in 11.249 değeri hatalı.
- BIST 30: 11.09 → 27.10 −%19,2. 20.10'da XU030 +%3,15, 22.10'da −%3,18 [H,1].
- F_XU0301026, 27.10: uzlaşma 13.954, önceki uzlaşma **14.017** (14.048 değil) [D,2]. Vadeler: Ekim **30.10**, Aralık **31.12** [D,2]. PPK 10.12 [D,9].

## 1. Sözleşme ve likidite
| | BIST 30 endeks opsiyonu [D,3] | Pay opsiyonu [D,4] |
|---|---|---|
| Tip | Avrupa, nakdi | Avrupa, **fiziki teslimat** |
| Büyüklük | 10 × endeks; prim endeks puanıyla (1 puan = 10 TL) | 100 pay |
| Strike | 250 puan adım; vade başına 11 strike + esnek | 8 strike |
| Vade | Şub/Nis/Haz/Ağu/Eki/Ara; açık olanlar Eki-26, Ara-26, Şub-27 | her ay, en yakın 3 |
| Teminat | BISTECH (SPAN): fiyat tarama aralığı (PSR) %11,4, vol tarama aralığı (VSR) %32, kısa opsiyon asgari riski **8.180 TL/kontrat** [D,5] | PSR %13–16 |

**Likidite** (Borsa İstanbul günlük bülteni [D,2], `viop_parse.py`):

| Gün | BIST30 ops. kontrat | Nominal (mlr TL) | Prim (mn TL) | Açık poz. (AP) | BIST30 vadeli (mlr TL) |
|---|---|---|---|---|---|
| 20.10 | 15.590 | 2,4 | 57 | 128.418 | 52,8 |
| 23.10 | 85.667 | 12,2 | 165 | 155.938 | 97,2 |
| 26.10 | 22.495 | 3,3 | 83 | 163.622 | 109,6 |
| 27.10 | 88.457 | 13,2 | 486 | 211.894 | 91,1 |

- Opsiyon nominali vadeli hacminin %5–14'ü; AP bir haftada +%65 (hedge talebi). Hacim Ara-26'da ATM ±1.000 puanda yoğun; Şub-27'de yalnızca 10'luk lotlar.
- Pay opsiyonları ~2.500 seriye dağılmış, toplam prim hacmi günde 5–13 mn TL. **Pair işlemler opsiyonla kurulamaz.**
- Makas bültende yok. Seans sonrası ekran: Ara C16000 23/100, P14250 0/355 [D,6]; kanatlar tek taraflı. ATM makası tahminen %5–15 [T]; emir başına 10–50 kontrat uygulanabilir.

## 2. Volatilite rejimi
| Ölçü | Değer |
|---|---|
| RV10/20/60 (XU030, yıllık) | %30 / %27 / %28 [H,1] |
| RV20: 2 yıllık medyan / p90 / şu anki yüzdelik | %23 / %35 / 67. [H] |
| GARCH(1,1), 27.10: 1 gün / 1 ay | %31,4 / %32,1; yarı ömür 68 gün [D,7] |
| Ara-26 IV, uzlaşma fiyatlarından | ATM ~%24; 13.000P %27,5 (put çarpıklığı) [H,2] |
| Ara-26 IV, işlem fiyatlarından | 20–26.10: %15–25 · **27.10: %10–15** · 28.10 ekranı ~%11–13 [H,2,6] |

- **Anomali gerçek mi?** Put-call paritesi işlem fiyatlarında tutuyor: ima edilen vadeli 14.620–14.720, piyasadaki vadeli 14.643 [H]. Yani veri hatası değil.
- **Olası kaynak:** Aynı gün tek büyük akış: P15500 AP 1.643 → 24.959, C14250 159 → 10.059 [D,2]; muhtemelen yapılandırılmış pozisyon [T]. Uzlaşma fiyatları model fiyatı gibi davranıyor; şartname buna izin veriyor [3].
- **Sonuç:** IV ≤ RV ≤ GARCH. Çıplak put, short strangle ve risk reversal'ın put bacağı negatif beklenen değerli. Ayrıca düşük işlem fiyatından satılan pozisyon %24 IV ile değerlenir; bu hemen teminat açığı yaratır.

## 3. Fiyatlama ve TL faizinin etkisi [H: `structures.py`, `ideas.py`]
- **Teorik vadeli:** F = 13.900·e^(0,36·0,175) = **14.806** (+%6,5).
- **Piyasa vadelisi:** Aralık 14.644, spot 13.961 (+%4,9). İma edilen taşıma %27,2; vadeli teorik değerin ~%1,5 altında. Muhtemel neden: hedge talebi ve arbitrajı engelleyen açığa satış kısıtları [T]. **Fiyatlamada spot+r değil, vadeli fiyatın kendisi (Black-76) kullanılmalı.**
- **Spot-ATM opsiyonlara etkisi (σ=%24):** C14000, r=0'da 511 puan; piyasa F ile 853. P14000 611'den 309'a iner. Spot-ATM call pahalı, put ucuz; "ATM" strike ~14.650. Call spread başabaşındaki +%6,4'ün %4,9'u yalnızca taşıma.

Aralık vadesi, F=14.580 (S=13.900), puan:

| Yapı | σ=%20 | σ=%24 | σ=%32 | 27.10 uzlaşma / kapanış [D,2] | Maks kâr / zarar (σ24) | Başabaş | Δ |
|---|---|---|---|---|---|---|---|
| (a) +C14500/−C15500 | 334 | 350 | 368 | 380 / 269 | +650 / −350 | 14.850 | +0,24 |
| (b) +P14000/−P13000 | 185 | 227 | 289 | 156 / 35 | +773 / −227 | 13.775 | −0,20 |
| (c) −P13250/+C15500 | 91 | 116 | 156 | 101 / 20 | sınırsız / −%20'de −2.250 | 15.620 | +0,42 |
| (d) +C14500/+P14500 | 914 | 1.096 | 1.460 | 1.110 / 510 | sınırsız / −1.096 | 13.405 / 15.600 | +0,08 |

(c) **önerilmez**: put bacağı crash çarpıklığına açık ve kısa opsiyon asgari riski nedeniyle teminat tamamlama çağrısı yaratır.

## 4. FİKİR 1 — Koşullu long vol: Aralık 14.500 straddle
- **Enstrüman ve yön:** Al O_XU030E1226C14500.00 + Al O_XU030E1226P14500.00 (1:1), vade 31.12.2026.
- **Giriş koşulu:** 2–6.11 arasında toplam prim **≤800 puan** (IV ≤ ~%17,5) ise limit emirle gir. Karşılaştırma: uzlaşmaya göre adil değer 1.110, 27.10 kapanışı 510 [D]. Prim >900 ise işlem yok.
- **Maks zarar:** prim (≤8.000 TL/straddle). **Maks kâr:** yukarıda sınırsız, aşağıda 13.700 puan.
- **Başabaş:** 13.700 / 15.300 (vadeliye göre −%6,4 / +%4,5).
- **Greek'ler (σ17):** Δ ≈ +0,1; vega ≈ 455 TL/vol puanı; theta ≈ −50 TL/gün.
- **Olasılık ve beklenen değer [H/T]:**
  - Kâr olasılığı (risk-nötr): σ=%24'te ~%58, RV %17'ye düşerse ~%44.
  - Beklenen değer (bugünkü değer, straddle başına): gerçekleşen vol %24'te +300 puan, %27'de +440, %17'de ≈0.
- **Büyüklük:** Risk sermayenin %0,8'i: 10 mn TL için 10 straddle. Teminat yok (prim peşin). P14500 günlük hacmi 20–930 kontrat olduğundan tek seferde ≤50 kontrat.
- **Yönetim:**
  - IV ≥%23'e dönerse yarısını sat (~+250 puan).
  - |Δ| >0,35 olursa vadeliyle nötrle.
  - Değer ≤400 puana inerse kapat.
  - 15.12'de kapat.
- **Tez:**
  - A) RV %27 ve takvim dolu: 30.10 vade + SPK esnekliğinin bitişi; 2.11 Takasbank parametreleri [8]; 3.11 TÜFE; ~11–12.11 MSCI/Enflasyon Raporu; 10.12 PPK.
  - B) Komite yönde bölünmüş; endeks karar noktasında.
  - C) Opsiyonlar ~%11–15 vol fiyatlıyor.
  - → Yön bilmeden ±%5'lik hareketten ucuza kazanılır.
- **Karşı argüman:** Fiyatlar tek seferlik akışın izi olabilir; IV %24'e dönerse işlem açılmaz.
- **En büyük risk:** Sessiz toparlanma; RV %15–17'ye iner, endeks 14.000–15.000 bandında kalır. **Tezin dayandığı varsayım:** 2 ay boyunca gerçekleşen vol ≥%18.
- **Yanlışlama:** 15.11'e kadar 10 günlük RV <%15 ve endeks 14.200–15.000 içinde → kapat.
- **Güven: 6/10** (koşul sağlanırsa). Koşulun sağlanma olasılığı ~%40 [T].

## 5. FİKİR 2 — Tanımlı riskli dip avı / sıkışma sigortası: Aralık 14.500/15.500 boğa call spread
- **Enstrüman ve yön:** Al O_XU030E1226C14500.00 / Sat O_XU030E1226C15500.00.
- **Prim:** uzlaşma 380, kapanış 269 [D]; model değeri σ=%17–32'de 338–380 [H]. **Limit ≤340 puan**; ≥380 ise girme.
- **Getiri profili:** maks zarar 3.400 TL, maks kâr 6.600 TL, getiri/risk ~1,9. Başabaş ~14.840 (spota göre +%6,3). Δ +0,24–0,33.
- **Olasılık [H]:**
  - Kâr olasılığı: risk-nötr ~%41; spot nominal olarak yatay kalırsa %19–25.
  - Maks kâr (≥15.500) olasılığı: %20–27.
  - Öznel ~%35 [T]; adil fiyattan beklenen değer ≈0, avantaj indirimli girişte.
- **Büyüklük:** Risk %0,5 (güven düşük): 10 mn TL için 14 spread; delta 3,4–4,6 vadeli eşdeğeri.
- **Teminat:** Kısa C15500 bacağındaki 8.180 TL/kontratlık asgari risk uzun bacakla netleşmeyebilir. ~115 bin TL tampon ayır ve aracı kurumla teyit et [D/V].
- **Giriş:** 2–6.11.
- **Çıkış:**
  - Spread ≥700 → kapat.
  - Spread ≤170 → kapat.
  - BIST 30 iki gün üst üste 13.500 altında kapanırsa → kapat.
  - 10.12'den sonra spot <14.200 ise → kapat.
- **Tez:**
  - A) Düşüşün büyük kısmı zorunlu satıştan geldi.
  - B) BIST 30'da likit satış büyük ölçüde geride (ENDEKS); TCMB indirim patikası sürüyor.
  - C) Düşüşün %38–50'si geri alınırsa 15.200–15.600 seviyesi gelir.
  - → Aralık sonunda endeks ≥14.840.
- **Komiteye katkısı:** ENDEKS ve ŞEYTAN'ın "rallide short" fikirleri için yukarı yönlü gap sigortası. 14.500–15.500 arasında short vadelinin kaybını puan puan karşılar.
- **Karşı argüman:** Spot yatay kalırsa taşıma nedeniyle kayıp. Fon krizinin ikinci dalgası; MSCI'nin 2027 sınıflandırma riski [12].
- **Tezin dayandığı varsayım:** "Zorunlu satış BIST 30'da bitti."
- **Yanlışlama:** İki gün üst üste 13.500 altı kapanış, ya da 30.10'da SPK esnekliğinin uzatılmaması ve teminat çağrılarının sıçraması.
- **Güven: 4/10.**

## 6. Risk çerçevesi
- **Kaldıraç [D,5]:** Aralık vadelide 1 kontrat ≈146 bin TL nominal, ≈16,7 bin TL teminat; kaldıraç ~8,8×. Sürdürme teminatı %75 olduğundan ~%2,85'lik ters hareket (≈417 puan) teminat çağrısı doğurur. Pay vadelilerinde PSR %13–16, USDTRY'de %11. 2.11'de parametreler güncelleniyor; artış olası [D,8/T].
- **Gap:** XU030'un 2 yıldaki en kötü 1/3 günü −%8,9 / −%17,5 (Mart 2025) [H]; ikincisi tam kaldıraçlı vadelide teminatın 1,5 katı.
- **Devre kesici ve limitler:** BIST 100 −%6'da EBDKS ile 20 dakika ara [D,10]. Endeks vadeli limiti ±%10; şartnamede ±%15 yazıyor, teyit gerekli [D,11]. Limit kilitlenirse stop emri çalışmaz.
- **Korelasyon [H]:** XU030–XBANK ρ 0,80; XU030–USDTRY günlük ρ −0,13 ama Mart 2025'te birlikte kaybettirdi.

**Komite risk bütçesi (öneri) [V]:**

| Kural | Limit |
|---|---|
| Fikir başına stop-bazlı zarar (opsiyonda primin tamamı) | ≤%1 (güven ≤4 ise ≤%0,5) |
| Fikir başına stres zararı (stop çalışmadan BIST −%12 / USDTRY +%8) | ≤%2,5 |
| Komite toplam stop-bazlı risk | ≤%4 |
| Ortak stres (BIST −%15, banka −%18, USDTRY +%8 aynı anda) | ≤%7 |
| ρ>0,6 olan ya da aynı enstrüman ve yöndeki fikirler | tek kova, ≤%2 |
| Teminat kullanımı | ≤%20; PSR'de +%30 artışa dayanıklı |
| Net TR-hisse delta | ≤ sermayenin %50'si |
| Çıplak kısa opsiyon | yasak |
| Opsiyon emri | ≤ 5 günlük ort. hacmin %10'u ve AP'nin %5'i; yalnızca Ara-26; limit emir |

**Diğer ajanlara notlar:**
- **ENDEKS ve ŞEYTAN:** İkisi de short F_XU0301226 öneriyor; tek kova sayılmalı, birleşik risk ≤%1. Short vadeliye long C15500 eklemek sentetik put yaratır (kapanış 60, uzlaşma 247 puan).
- **MAKRO:** O_USDTRYKE1226C57000 (uzlaşma 246,7 TL/1.000$, IV ~%17) işlem görmüyor; AP 25. Daha likit C56000 ise beklenen carry'nin tamamını yer [H,2].
- **Toplam risk:** Teklifler toplamı ≈%5,05 (ENDEKS 0,75 + ŞEYTAN 1 + MAKRO 0,5 + HİSSE 1,5 + OPSİYON 1,3) ve %4 sınırını aşıyor. ENDEKS ile ŞEYTAN birleştirilirse ~%4,3'e iner. Fikir 2 short'ları dengelediği için net stres katkısı negatif.

## Kaynaklar
1. Yahoo günlük veri (XU030.IS, XU100.IS, XBANK.IS, TRY=X): https://query1.finance.yahoo.com/v8/finance/chart/XU030.IS?range=2y&interval=1d
2. Borsa İstanbul VİOP günlük bülteni: https://www.borsaistanbul.com/data/vadeli/viop_20261027.csv (20/22/23/26.10 aynı kalıpta)
3. https://borsaistanbul.com/piyasalar/viop/opsiyon-sozlesmeleri/pay-endeks-opsiyon-sozlesmeleri
4. https://borsaistanbul.com/piyasalar/viop/opsiyon-sozlesmeleri/pay-opsiyon-sozlesmeleri
5. Takasbank GM 2174 (15.10'dan geçerli): https://www.isyatirim.com.tr/tr-tr/Resmi-Duyurular/Documents/GenelMektup2174.pdf · GM 2171: https://www.isyatirim.com.tr/tr-tr/Resmi-Duyurular/Documents/GenelMektup-2171.pdf
6. Foreks, 28.10: https://www.foreks.com/sembol-detay/VXU0302/fxu030-2/xu030-31-ara-26-vadeli/ · https://www.foreks.com/sembol-detay/H966392/o-xu030e1226p1450000/xu030-31-ara-26-satim-opsiyonu/ · https://www.foreks.com/sembol-detay/H967190/o-xu030e1226c1550000/xu030-31-ara-26-alim-opsiyonu/ · https://www.foreks.com/sembol-detay/H966150/o-xu030e1226c1600000/xu030-31-ara-26-alim-opsiyonu/
7. https://vlab.stern.nyu.edu/volatility/VOL.XU030:IND-R.GARCH
8. https://www.foreks.com/haber/detay/6ae0c15f58b1b941c20921a0/FRKS/tr/takasbank-risk-parametrelerini-guncelledi-27-10-26/
9. https://www.cnbce.com/faiz/turkiye-cumhuriyet-merkez-bankasi-2026-yili-para-politikasi-kurulu-ppk-toplantilari-ve-rapor-takvimini-acikladi-h22037
10. https://www.capital.com.tr/piyasalar/borsa/borsa-istanbul-devre-kesici-kurallarini-yeniledi-yeni-donem-1-eylulde-basliyor
11. https://www.borsaistanbul.com/files/20221215-13341_viopta-bist-surdur.25-endeksi-vis-isl-acilmasi.pdf · https://borsaistanbul.com/piyasalar/viop/vadeli-islem-sozlesmeleri/endeks-vadeli-islem-sozlesmeleri
12. https://www.bloomberght.com/msci-turk-hisselerine-yonelik-endeks-degisikliklerini-dondurdu-3791527
