# v_S2_a — Bağımsız doğrulama: TKC ADR parite sapması → TCELL ertesi gün gün-içi (S2)

Doğrulayıcı: v_S2_a. Kod: `out/code_v_S2_a/` (01–07, `vs.py` yardımcı modül; **ll.py import edilmedi**, ham parquet'ten kendi hizalama/temizlik). Loglar ve çıktılar: `out/code_v_S2_a/res/`.

## KARAR: DÜZELT — güven ORTA (ilişki), DÜŞÜK (iddia edilen |U|>50 bps backtest'in işlenebilirliği)

| Kontrol | İddia | Benim sonucum | Yorum |
|---|---|---|---|
| intra_{t+1} ~ D_t + gap_{t+1}, ALL | b 0,13, t 2,8 | b 0,129, t 2,76 (n 3.101) | birebir |
| IS 2014–20 | b 0,09, t 2,2 | b 0,075, t 1,91 | biraz zayıf, sınırda |
| OOS 2021–26 | b 0,15, t 2,4 | b 0,148, t 2,39 | birebir |
| BT \|U\|>50 bps, 8 bps, OOS | +19 bps, Sh 1,07 | +19,2 bps, t 2,55, Sh 1,07 (n 1.035); blok-bootstrap %95 GA [5,0; 34,1] | birebir |
| BT \|U\|>50, IS | ≈0 | +1,4 bps, Sh 0,11; GA [−7,7; 11,4] | IS'te kenar yok |
| Saatlik tk_post → TCELL 07:30→kapanış | β 0,30, t 2,75 | β 0,300, t 2,77 (n 695); BT \|>50\| +21,2 bps, Sh 1,18 | birebir, ama kırılgan (aşağıda) |

## (b) Zamanlama / ileriye bakma denetimi
1. **USDTRY zaman damgası (01_fx_align.py).** 2024+ saatlik veriyle: Yahoo günlük `c` (ldate D), D günü yaklaşık 23:00 UTC (D−1) ile 05:00 UTC arasındaki fiyata eşit. Medyan fark 2,8 bps. 06:00 UTC'den sonrası belirgin şekilde daha kötü eşleşiyor (D 21–24 UTC: 6,7–8 bps). Buna göre bar(t+1), BIST t+1 açılışından (06:55/07:00 UTC) önce. 2011–2023 için parite varyans testi yaptım: std(ΔP) her yıl k1'de (ldate>t ilk bar) en küçük. 2005–2010'da k0 en küçük, yani o dönemde barlar gün sonu. Bu, savunma kodundaki "2011 öncesi kaydırma yok" kuralıyla tutarlı. 2024–26'da k1≈k2 çıkıyor, çünkü kur hareketi parite gürültüsüne göre küçük.
2. **Seans içine taşma testi (06).** Kur bar(t+1) BIST t+1 seansını içerseydi, corr(dfx_t, XU100 gün-içi_{t+1}) pozitif kontroldeki gibi (−0,43…−0,14) negatif çıkardı. 2014–19'da ise pozitif (+0,07…+0,26). Bu, açılıştaki aşırı tepkinin geri dönüşüyle uyumlu. Taşma kanıtı yok.
3. **En katı varyant: kur t sabahından alındığında (D_k0, hiçbir konvansiyonda ileriye bakamaz)** etki yaklaşık yarıya iniyor. ALL b 0,068 (t 2,12), IS 0,022 (t 0,46), OOS 0,094 (t 2,17). BT U_k0 \|>50\| OOS +12,4 bps, Sh 0,68; IS −0,7 bps. Yani sinyalin bir kısmı BIST kapanışından sonraki gece kur hareketinden geliyor. Bu meşru bir bilgi (açılıştan önce biliniyor), ama hizalamaya duyarlı.
4. TKC günlük kapanışı ~20/21 UTC (saatlik son barla medyan 9 bps fark). TCELL günlük `o` son 60 günün tamamında 5 dk 06:55 açılış seansı barına eşit, yani gerçek açılış seansı fiyatı. Hedefte `adj` (cc) ile ham `o/c` (intra) karışık kullanılıyor; temettü etkisi gap'e gidiyor, bu doğru. Kapanış seansı gürültüsü (c / 15:00 sürekli) hiçbir şeyi tahmin etmiyor; D bu kontrolle de sağlam (t 2,2).
5. **Asıl işlenebilirlik sorunu: U = D − gap_{t+1}, açılış fiyatını kullanıyor.** Strateji, açılış fiyatı öğrenildikten sonra **aynı fiyattan** girmeyi varsayıyor.
   - Son 60 günde ilk sürekli işlem fiyatı açılış seansı fiyatına çok yakın: medyan \|fark\| 2,5 bps, ortalama +0,7. Bu yüzden 07:00 UTC'de giriş muhtemelen yakın bir dolum verir, ama örneklem küçük.
   - 2023-12+ dönemi, aynı günler, 8 bps maliyet:

     | Giriş | Sinyal | Net bps/işlem | Sharpe |
     |---|---|---|---|
     | Açılış | \|U\|>50 | +15,8 | 1,06 |
     | 07:30 | U_open | +7,5 | 0,58 |
     | 07:30 | sapma 07:30'da yeniden hesaplanmış (U_730) | **+0,9** | 0,07 |
     | 08:30 | U_830 | −3,5 | — |
     | Açılış seansı emri (MOO) | yalnız D (açılış bilgisi yok) | +7,7 (tüm günler) / +5,2 (\|D\|>50) | — |

   - Kenarın ~8 bps'i açılış→07:30 bacağında. "Kalan sapma" kavramı çalışmıyor: y_730 ~ D + gap + r(açılış→07:30) regresyonunda D'nin katsayısı 0,118 (t 2,3), diğer iki terim ≈0. Yani tahmin gücü D'den geliyor, U'nun içindeki açılış kısmından değil.

## (c) Sağlamlık
- **Tanımlar:** kapanış (adj değil) b 0,123; 10 günlük ortalama 0,144; 20 günlük medyan 0,118 — hepsi t ≈ 2,6–2,7. 60 günlük ortalama b 0,109, ama BT OOS yalnız +9,8 bps, Sh 0,57.
- **Kontroller:** Şu değişkenler kontrol edildi: XU100 gap_{t+1}, TCELL'in kendi lag'i, XU100 lag'i, ES(t). D değişmiyor (t 2,7–2,85). Senkron XU100 gün-içi kontrolüyle t 4,7.
- **Piyasa-nötr hedef** (TCELL gün-içi − β·XU100 gün-içi): b 0,118, t 4,26 (IS 2,44 / OOS 3,67). 13 yılın 12'sinde pozitif. Ham hedefte 13 yılın 11'inde pozitif.
- **Plasebo varlıklar:** XU100 (t 0,7), XU030 (t 0,9) ve TTKOM (t 0,6) gün-içini D tahmin etmiyor. Etki TCELL'e özgü, bu da ADR fiyat keşfi mekanizmasıyla tutarlı.
- **Plasebo zaman:** bir gün eski sinyal D_{t−1} anlamsız (t 1,0). Dairesel kaydırma null'u: gözlenen Sharpe 1,07; null ortalaması −0,08 (sd 0,34); p < 0,002. Yalnız D için p = 0,002.
- **Aykırı değerler:** %1 winsorize ile t 3,6. KKM dönemi (15.11.21–31.01.22) hariç: OOS b 0,090 (t 2,1), BT OOS +15,2 bps, Sh 0,88. **OOS kârının %51'i en iyi 10 işlemden** geliyor (1.035 işlemde 10.166 / 19.887 bps); bunların 4'ü Ara-21/Oca-22'de. En iyi 10 hariç ortalama +9,5 bps.
- **Yön yanlılığı:** U ortalaması negatif çünkü ortalama gap pozitif. Bu yüzden işlemlerin %56'sı kısa ve TCELL'in negatif gün-içi sürüklenmesinden (OOS −11,4 bps/gün) yararlanıyor. Gap ortalaması çıkarılmış U ile OOS +12,3 bps, Sh 0,67 (iddiadaki 19,2 / 1,07 yerine).
- **Uyarlamalı eşik** (\|D\|/geçmiş sd > z): IS brüt +6…+15 bps (t 1,2–1,8). Yani IS'te işaret doğru ama büyüklük maliyetin altında. OOS brüt +21…+78 bps. Doğrusal boyutlamada net Sharpe IS 0,10 / OOS 1,01.
- **XU030 ile hedge'li iki bacak** (maliyet 8 + ~3 bps): \|U\|>50 OOS +15,7 bps (t 2,9), Sh 1,21; IS −1,9 bps.

## (d) IS/OOS ve yıllar (\|U\|>50, net 8 bps, bps/işlem)
2014 −14,9 · 2015 −6,7 · 2016 +3,2 · 2017 +17,8 · 2018 +22,7 · 2019 −10,4 · 2020 −2,3 · 2021 +38,6 · 2022 +31,2 · 2023 +0,8 · 2024 +15,4 · 2025 +7,9 · 2026 +25,2. Pozitif yıl: 9/13.

Regresyon b_D yıllara göre: 2015, 2017, 2022, 2026'da t > 2; 2014'te negatif; 2019, 2020, 2023'te ≈0.

D'nin yıllık sd'si 58 bps (2014) ile 237 bps (2022) arasında değişiyor. Sabit 50 bps eşiği IS'te çok gevşek kalıyor.

## (e) Maliyet duyarlılığı (\|U\|>50; OOS / IS net bps, Sharpe)
| Maliyet | OOS | IS |
|---|---|---|
| 0 | +27,2 (Sh 1,52) | +9,4 (Sh 0,72) |
| 4 | +23,2 (1,30) | +5,4 (0,42) |
| 8 | +19,2 (1,07) | +1,4 (0,11) |
| 12 | +15,2 (0,85) | −2,6 |
| 15 | +12,2 (0,68) | −5,6 |
| 20 | +7,2 (0,40) | −10,6 |

Yalnız-D sinyali (açılış seansı emriyle uygulanabilir) OOS'ta 8 bps maliyetle Sh 0,52; 15 bps'de 0,13; 20 bps'de negatif.

VİOP F_TCELL ön vade 30.10.2026'da ~0,9–1,0 mlr TL işlem hacmine sahip; açılış seansı da var. 8 bps gidiş-dönüş makul. Hacim bilgisi VİOP bülteninden; spread doğrulanmadı.

## Saatlik alt iddia (tk_post = ln(TKC kapanış / TKC 15:30 UTC) → TCELL 07:30→kapanış)
- Birebir üretildi. Zamanlama temiz: TKC 15:30 değeri BIST kapanış seansından ~20 dk sonra; giriş t+1 10:30 TSİ.
- Kırılgan:
  - Dönem kırılımı: 2023-12→2024 b 0,53 (t 3,5); 2025 b 0,02 (t 0,1); 2026 b 0,24 (t 1,3).
  - ES kapanış-sonrası kontrolüyle t 1,91.
  - D ile birlikte konunca tk_post t 2,0 kalıyor, D anlamsızlaşıyor. Aynı bilgi olduğu için bağımsız ikinci bir kanıt sayılmaz.
  - 15 bps maliyette Sh 0,79 (\|>50\|).
- Güven: DÜŞÜK.

## Sonuç
- **Doğrulanan:** TKC'nin BIST kapanışından sonraki TL karşılığı sapması TCELL'in ertesi gün gün-içi (özellikle hisseye özgü) getirisini öngörüyor. İleriye bakma bulunmadı. İstatistik IS'te zayıf, OOS'ta orta; piyasa-nötr hedefte güçlü.
- **Düzeltilen:**
  1. "IS t 2,2" yerine 1,9. Kur t sabahından alınırsa IS t 0,5.
  2. +19 bps / Sh 1,07, açılış fiyatını bilip o fiyattan dolum varsayan bir üst sınır. Ayrıca kısa yanlılık ve 10 uç işlem (KKM) bu rakamı şişiriyor.
  3. Gerçekçi işlenebilir aralık:
     - Yalnız-D ile açılış seansı emri: OOS +8–9 bps, Sh ~0,5.
     - Gap ortalaması arındırılmış U: OOS +12 bps, Sh ~0,7.
     - 07:30'da giriş: ≈0–7 bps.
     - IS'te 8 bps maliyetle hiçbir varyant anlamlı kâr üretmiyor.
- TradingView: NYSE:TKC, BIST:TCELL, FX:USDTRY, hedge için BIST:XU030 / VİOP XU030 vadelisi ('?'). VİOP TCELL vadelisinin TV kodu '?'.
