# v_YG2_a — Bağımsız doğrulama: Kapanış müzayedesi dönüşü (iddia YG2, kaynak ry_gunici_y.md bulgu 10)
Tarih: 02.11.2026 · Doğrulayıcı: v_YG2_a · Kod: `out/code_v_YG2_a/` (ll.py import edilmedi; ham parquet → kendi temizlik/hizalama)
Çalıştırma: `nice -n 10 python3 v0_data.py && v1_replicate.py && v2_ssf.py && v2b_ssf_more.py && v3_robust.py && v3b_season.py && v4_entry_cost.py && v5_longproxy.py && v6_basis_arb.py && v7_stock_fdr.py` (çıktılar `res/`).

## 0. Karar: DÜZELT. İlişki ORTA güvende; VİOP pay vadelisiyle işlenebilirlik DÜŞÜK

| İddia parçası | Benim sonucum | Durum |
|---|---|---|
| Ertesi gap b −0,157 (t −3,7) | −0,151 (t −3,5); 19.299 gözlem, 423 gün, gün kümelenmiş SE | ✔ |
| O→07:30 b −0,192 (t −3,8) | −0,195 (t −3,9). Toplam C→07:30 −0,350 (t −6,1); 07:30→C +0,04 (t 0,5) | ✔ |
| ~%35 geri dönüş | %35 (07:30'a kadar); C→C_{t+1} −0,31 (t −2,9); gün sabit etkili −0,38 (t −10,7) | ✔ |
| Portföy |CA|>25 bps, C→07:30: IS 11,7 / OOS 16,4 (t 4,1) | 11,3 (t 2,4) / 16,0 (t 4,0); tümü 14,1 (t 4,6), 5.873 işlem | ✔ ama **etiket yanlış** (aşağıda) |
| İllikit 18,7 / likit 7,7 bps | 18,1 (t 5,1) / 9,3 (t 2,0) (kendi ciro sıralamam) | ✔ |
| XU030'da yok | b −0,13 (t −0,5), SE ~0,3. Yalnız 31 gün |CA|>25. Kesit ortalaması CA → ortalama getiri b −0,06 (t −0,1) | ✔ "kanıt yok". Etki tamamen hisseye özgü; endeks testinin gücü düşük |
| ~425 yaz günü | 425 yaz günü (7 yarım gün hariç 422 kullanılabilir) | ✔ |
| Giriş için spot 18:08–18:10 'kapanış fiyatından işlemler' gerekiyor | Doğru. **SSF bunun yerine geçemiyor** (bkz. 2) | ✔ + düzeltme |
| (Raporda) "SSF normal seansı 18:10'da bitiyor" | **Güncel değil.** 23.09.2022'den beri 18:15 (BIST duyurusu, 05.05.2022 taslağında 18:10→18:15) | ✘ |

**IS/OOS etiketi:** İddiadaki "IS/OOS", h1 örnekleminin ortanca güne göre iki yarısı: ≤15.05.2025 (yaz 2024 + Nis–May 2025) ve sonrası. 2014–2020 / 2021–2026 ayrımı CA için YAPILAMAZ, çünkü P15:00 yalnız 2023-11'den beri (h1) var. Uzun örneklem vekili 5. bölümde.

## 1. Veri ve zamanlama doğrulaması
- h1 yapısı: yaz günlerinde 14:30 barının c'si = m5 14:55 barının c'si (59/59 gün, fark 0,0 bps). 06:30 barının c'si = m5 07:25 barının c'si (60/60, 0,0 bps). Kışın ilk barın açılışı günlük 'o' ile %99,3 aynı, son bar 13:30. Yani kışın 14:30–15:00 parçası eksik; etiket kayması yok.
- Temizlik:
  - bayat gün (v==0 ve h==l) NaN;
  - her getiri parçasında ±%10,5 kurumsal işlem eşiği (h1 dönemi tamamen 2020-03-13 sonrası; uzun vekilde 2020-03-13 öncesi ±%20,5);
  - yarım günlerde CA NaN.
- **Zaman çizelgesi (TSİ):**
  - 18:00 sürekli işlem biter (P15:00 UTC).
  - 18:00–18:05 kapanış emir toplama, 18:05 fiyat belirleme.
  - 18:08–18:10 kapanış fiyatından işlemler (QNB, Garanti BBVA).
  - SSF 18:15'e kadar işlem görür.
  - SSF günlük uzlaşma = son 10 dk (18:05–18:15) işlemlerinin miktar ağırlıklı ortalaması; 10 işlemden azsa son 10 işlem (BIST kılavuzu ve GCM).
- Sonuç: CA = log(C/P15:00) 18:05'te biliniyor. C'den giriş look-ahead içermiyor, ama dolum yalnız spotun 2 dakikalık kapanış fiyatından işlemler penceresinde mümkün.

## 2. VİOP pay vadelisi (SSF) ile işlenebilirlik: YOK (yeni ve olumsuz bulgu)
- Aynı sözleşmenin uzlaşma bazı değişimi Δlog(F_uzl/C) ~ CA: **−0,585 (t −22,6)**. SSF uzlaşması müzayede hareketinin yalnız ~%41'ini izliyor.
  - Hisse bazında eğim 47/47 hissede −0,33 … −0,94. SSF işlem sayısı tercillerinde fark yok (−0,51 / −0,61 / −0,54).
  - SSF son işlem fiyatı (close) −0,43 eğimli, o da C'yi izlemiyor.
  - Ertesi gün baz normale dönüyor (+0,56, t 21,6).
- Yorum: SSF piyasası kapanış müzayedesi fiyatını zaten "geçici" sayıyor ve adil değere yakın fiyatlıyor. Spotun ertesi sabahki dönüşü SSF'ye yansımıyor.
- SSF stratejisi (−sign(CA), uzlaşmadan giriş, 07:30 vekiliyle çıkış): **−10,0 bps (t −3,3)**. Uzlaşmadan uzlaşmaya −8,7 (t −1,5).
- Sonuç: Bulgu VİOP pay vadelisiyle işlenemez. Yalnız spotta C'den dolumla mümkün.

## 3. Alternatif giriş/çıkış (|CA|>25 bps, bps/gün-portföy, NW t)
| Giriş → çıkış | Brüt | Not |
|---|---|---|
| C → 07:30_{t+1} (baz) | 14,1 (4,6) | |
| C → ertesi ilk bar tipik fiyatı (VW30 vekili) | 13,1 (5,0) | çıkış gerçekçi |
| C → 08:30_{t+1} | 12,3 (3,5) | |
| C → C_{t+1} | 11,9 (2,1) | |
| Ertesi açılış O_{t+1} → 07:30 | 8,2 (3,6); |CA|>50: 16,8 (4,1) | açılış müzayedesinden dolum iyimser |
| Ertesi VW30 → 08:30 | **−0,9 (−0,5)** | gerçekçi sabah girişi hiçbir şey yakalamıyor |
| Hisseye özgü: CA−CA_XU030, getiri XU030 hedge'li | 17,2 (**9,1**); H1 18,1 (6,2) / H2 16,7 (6,6); |CA_id|>50: 27,1 (6,5) | en temiz tanım; hedge maliyeti ~3 bps ayrıca |
| Yalnız uzun ayak (CA<0, C'den al) | 27,7 (5,1) | **Yanıltıcı.** Koşulsuz C→07:30 kayması hisse-gün başına 17,1 bps. Kayma düzeltmeli uzun 11,9, kısa 17,6 |
| SSF uzlaşmasından | −10,0 (−3,3) | bkz. 2 |

**Hipotez: spot–SSF baz yakınsaması** (`v6`):
- İşlem: CA<0 iken spotu C'den al ve SSF'yi uzlaşma civarında sat (CA>0 iken tersi).
- Brüt sonuç, gözlenen fiyatlarla C/F_uzl → C_{t+1}/F_uzl,{t+1}, taşıma (θ ≈ 11,5 bps/gün) düşülmüş:
  - |CA|>25: 21,6 bps (t 23);
  - |CA|>50: 31,9 bps (t 13).
- 4 bacak maliyetinden sonra (spot 4 bps + yarım tik, SSF 8 veya 15 bps + tik):
  - |CA|>25: +0,6 / −6,4;
  - |CA|>50: +10,9 (t 4,2) / +3,9 (t 1,5); H2'de +6,8 / −0,3.
- Kısıtlar: işlemlerin yarısı spot açığa satış gerektiriyor; SSF'de uzlaşma (VWAP) dolumu varsayılıyor; aynı 2 dakikalık spot penceresine bağlı.
- Güven: DÜŞÜK.

## 4. Dayanıklılık (baz: |CA|>25, C→07:30)
| Test | Sonuç (bps, t) |
|---|---|
| Tik ayrıklığı | 1 tiklik hareketler yalnız 251 işlem; ≥3 tik 13,3 (4,4); tik/fiyat ≤10 bps 12,7 (4,1) → tik kaynaklı değil |
| Aykırı | en iyi 5 gün hariç 11,5 (4,2); %1/%99 kırpılmış 14,5 (5,1); günlük medyan 16,7 |
| Vade sonu / çeyrek sonu hariç | 14,2 (4,5) / 14,5 (4,7) |
| Toplu müzayede günleri | ort|CA| üst %5 (22 gün: MSCI/FTSE/çeyrek dönemleri vb.) hariç 12,5 (4,1); bu 22 gün tek başına 42,7 (5,2) |
| Plasebo: son 30 dk sürekli işlem (L30) işareti | 7,2 (1,9); |CA|≤5 bps günlerinde 4,5 (1,0) |
| Bir hisse hariç | 13,0–14,8 |
| Hisse bazında (v7) | gap: %81 negatif, BH-FDR(5%) 6/47 (BIMAS, ENJSA, ENKAI, TRMET, VAKBN, VESTL). C→07:30: %87 negatif, 8/47 |
| Hisse P&L | en güçlüler ODAS, TOASO, ENJSA, TKFEN, BRSAN, FROTO, HEKTS (30–43 bps). Büyük bankalar sıfır/negatif (YKBNK −23, AKBNK −5, ISCTR −2) |
| Yıllar (yaz) | 2024 12,2 (2,2) / 2025 16,4 (3,5) / 2026 13,6 (2,5) → 3/3 pozitif |
| Eyl–Eki 2026 fon krizi | 4,7 (0,4); işlem başına −6,4 → son 2 ayda zayıf |
| **KIŞ VEKİLİ (uyarı)** | LH = log(C/P17:30 TSİ) yıl boyu ölçülebiliyor. Yaz: portföy 10,7 (3,1), b −0,11 (t −2,0); beklenen −0,35·var(CA)/var(LH) ≈ −0,08. **Kış: 0,16 (0,04), b +0,02 (t 0,3).** Kış sezonları: 2023/24 10,2 (2,3), 2024/25 −2,0, 2025/26 −5,9. Fark ~2 SE. Ya etki mevsime/döneme bağlı ya da kışın müzayede başka davranıyor; ayrıştırılamıyor |

## 5. Uzun örneklem vekili (IS 2017–2020 / OOS 2021–2026) — yalnız mekanizma kanıtı, İŞLENEMEZ
- Vekil sinyal: ex_t = Δlog(F_uzl/C). h1 döneminde ex_t ≈ −0,585·CA. Kesitsel arındırılmış ertesi gap üzerine regresyon, cc_t kontrollü:
  - 2017–2026: b 0,124 (t 12,4);
  - IS 2017–2020: 0,135 (t 11,5);
  - OOS 2021–2026: 0,115 (t 7,9);
  - 10/10 yıl pozitif. Zayıf yıllar: 2017 t 1,0, 2021 t 1,6, 2023 t 1,2.
  - SSF seansı 18:10 iken (≤09.2022) 0,133 (t 10,5); 18:15 iken 0,114 (t 7,0).
- Kapanış fiyatının SSF'ye göre geçici sapmasının ertesi açılışta dönmesi uzun dönemde istikrarlı görünüyor.
- Ama sinyal 18:15'te kesinleşiyor, spot penceresi 18:10'da kapanıyor. Ayrıca SSF uzlaşması 18:05–18:15 arasındaki haberi de taşıyor (kesitsel arındırma piyasa bileşenini atıyor, hisse haberini atmıyor).

## 6. Maliyet duyarlılığı (gidiş-dönüş, işlem başına; tik = 0,01 TL/fiyat, ortalama 4,4 bps; spot tik tablosuyla ortalama 8,9 bps)
| Varyant | Brüt | 8+tik | 15+tik | 30+tik | Kademeli (likit 8 / illikit 20)+tik |
|---|---|---|---|---|---|
| |CA|>25 | 14,1 | +1,7 (0,5) | −5,3 | −20,3 | −5,7 |
| |CA|>25, spot tiki | 14,1 | −2,9 | −9,9 | −24,9 | −10,2 |
| |CA|>50 | 23,0 | +10,6 (1,8) | +3,6 | −11,4 | +2,3 |
| |CA|>100 (284 işlem / 140 gün) | 46,7 | +34,7 (2,5) | +27,7 | +12,7 (0,9) | +25,6 |
| İllikit24 |CA|>50 | 24,1 | +12,2 (2,0) | +5,2 | −9,8 | +0,2 |
| Likit23 |CA|>50 | 14,7 | +0,4 | −6,6 | −21,6 | +0,4 |
| Hisseye özgü |CA_id|>50 (−3 bps hedge ayrıca) | 27,1 | +13,9 (3,3) | +6,9 | −8,1 | +5,3 |

Başabaş eşiği yaklaşık |CA| ≈ maliyet/0,35. 15 bps için |CA| ≳ 45 bps, 30 bps için ≳ 85 bps gerekiyor.

Kapasite (m5, 60 gün):
- Açılış + kapanış müzayedesi + kapanış fiyatından işlemlerin toplam hacim payı medyanı günlük hacmin %3,0'ı.
- Etkinin yoğunlaştığı illikit hisselerde bu toplam 3–8 mn TL/gün; 2 dakikalık pencere bunun yalnız bir kısmı. Kapasite çok küçük.

## 7. Düzeltilmiş iddia
Spot kapanış müzayedesi hareketi (CA = log(C/P18:00 TSİ)) ertesi gün 10:30 TSİ'ye kadar ~%35 geri dönüyor:
- havuz b −0,35 (t −6,1);
- gap −0,15, O→07:30 −0,195;
- gün sabit etkili −0,38 (t −10,7);
- piyasa bileşeninde dönüş yok, etki hisseye özgü.

Portföy (|CA|>25, C→07:30):
- 14,1 bps (t 4,6); h1 yarıları 11,3 (t 2,4) / 16,0 (t 4,0); yazlar 2024/25/26 12/16/14;
- XU030 hedge'li 17,2 (t 9,1).

Sınırlar:
- 425 yaz günüyle sınırlı. Kış vekili tutmuyor (0,2 bps). Eyl–Eki 2026'da zayıf.
- Uzun dönem SSF baz vekili mekanizmayı 2017–2026 boyunca destekliyor (IS t 11,5 / OOS t 7,9) ama işlenemiyor.

İşlenebilirlik:
- Yalnız spotta 18:08–18:10 kapanış fiyatından işlemlerle mümkün. Bu pencere sığ ve hacmin <%3'ü.
- **VİOP pay vadelisiyle uygulanamaz.** SSF uzlaşması (18:05–18:15) müzayede hareketinin yalnız %41'ini izliyor; SSF girişi −10 bps (t −3,3).
- Maliyetten sonra (|CA|>25): 8 bps+tik ile +1,7 (t 0,5), 15 bps'te −5. |CA|>50 için +10,6 / +3,6 / −11 (8/15/30).

Güven: ilişki ORTA; VİOP'ta net kâr DÜŞÜK.

## 8. Açık sorular
1. Kış vekilinin başarısızlığı: kış m5 verisi (Kasım–Mart) birikince doğrudan CA ile test edilmeli.
2. Kapanış fiyatından işlemler penceresinde gerçek dolum oranı: BIST emir defteri/işlem verisi gerekiyor. C'de dengesizlik tarafında kalan emirler var mı?
3. Baz yakınsaması (spot C + SSF karşı pozisyon): gerçek SSF 18:05–18:15 tik verisi ve açığa satış kısıtlarıyla test edilmeli.

Kaynaklar:
- [QNB Invest işlem saatleri](https://www.qnbinvest.com.tr/hisse-senedi-islem-saatleri)
- [Garanti BBVA BIST işlem saatleri](https://www.garantibbva.com.tr/borsa-hisse-senetleri/bist-islem-saatleri)
- [BIST duyuru 14431 (21.09.2022)](https://borsaistanbul.com/duyuru/14431/viopta-acilis-seansi-uygulamasi-ve-pay-vadeli-islem-ve-opsiyon-sozlesmelerinin-seans-sonu-saati-degisikligi-hk)
- [BIST taslak duyuru 05.05.2022, metin okundu](https://www.borsaistanbul.com/files/viop-acilis-seansi-ve-pay-vis-ops-seans-sonu-deg-hk-duyuru.pdf)
- [İşbank VİOP eğitimi 2024](https://www.isbank.com.tr/contentmanagement/Documents/sozlesme-ve-formlar/2024/iscep-viop-egitimi-22.02.2024.pdf)
- [GCM: VİOP uzlaşma fiyatı](https://www.gcmyatirim.com.tr/egitim/makaleler/viop-ta-gunluk-uzlasma-fiyati-ve-teminat-tamamlama-cagrisi)
- [BIST VİOP vadeli sözleşmeler kılavuzu](https://www.borsaistanbul.com/data/kilavuzlar/VIOP_vadeli_islem_sozlesmeleri.pdf)
