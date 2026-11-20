# W3-A — kaçınma ve SAT sinyalleri (geliştirme paneli: IS + OOS-1)

**Veri:** yalnız `panel_dev`; kasa açılmadı. Satırlar `elib.evaluate` / `evaluate_viop` çıktısı (bps, dolabilir). Rakam çiftleri **IS / OOS-1**. İki döneme de bakıldı: hepsi keşiftir, hüküm kasada. Kütüphane hatası görülmedi.

**Taranan:** 490 satır (388 spot, 102 vadeli fiyatlı). İki dönemde de beklenen yönde ve |t| ≥ 2: spot satırlarının 103'ü, vadeli SAT satırlarının **hiçbiri**.

## Bulgular (AL pozisyonunun 1 günlük fazla getirisi)

| Tetik | own (t) | sec |
|---|---|---|
| K1 tavana değdi, kapanmadı | −99 (−2,6) / −82 (−2,8) | −62 / −60 |
| K2 tabana değdi, kapanmadı | −94 (−1,5) / −128 (−2,1) | −58 / −86 |
| K3 tabanda kapandı | −449 (−4,2) / −320 (−4,1) | −448 / −323 |
| K4 sektörden ≥ %5 geride | −130 (−3,9) / −188 (−5,3) | −120 / −148 |
| K6 sektör z ≥ 1,5 | +25 (2,2) / −91 (−1,8) | — |

- **K1** (hisse-günlerin %1,3 / %2,0'si): 2018–2024'ün her yılı eksi. Tavana yakın kapanış (< %2) daha kötü (−144 / −148); hacim > 2× medyan −114 / −117. Kaybın %42'si gecede: ertesi gün açılışta almak da kötü (−52). 2. ve 3. gün −32 / −40, −26 / −50. Likit üçte birlik −86 / −93 (t −1,0 / −1,7): zayıf.
- **K4 %5** (%3,0 / %2,4): doz-tepki tek yönlü (%3: −46 / −101; %7: −248 / −343); üç likidite diliminde eksi; fiyat ≥ 5 TL −157 / −146. Kayıp gecede (sektöre göre gece −143 / −84, gün içi +56 / −34): kapanışta almayan kaçınır. 2.–3. gün −73 / −76, −62 / −89. **Uyarı:** IS'te çekirdek tabanda kapananlar; taban hariç −11 (t −0,4) / −91 (t −3,0).
- **K6:** OOS-1 eksisini 2023 taşıyor (−185; 2024 −37; 2025 +47; 29 olay). Mutlak eşikle (sepet ≥ +%3) +21 / −2. Rejim kanıtı yok; iki yönde de kural çıkmaz.
- **Süzgeç etkisi:** K1 ∪ K2 ∪ K4 %5 hisse-günlerin %4,8 / %4,9'unu eler; rastgele alıcının ertesi gün ortalaması +4,7 / +5,9 bps iyileşir.
- **VİOP SAT:** üç dayanakta tetikler seyrek (K1: 6 + 8 olay). K4 %3 SAT −43 / +84, K6 SAT −59 / +85: tutarsız. İki dönemde de artı kalan tek aile “sektör düşerken direnen”.

## DONDURULMUŞ KURAL 1 — `W3A_tavana_degdi_kapanmadi_KACIN_h1`
Girdi: `lim_up_touch`, `lim_up`, `tradable` (2015-12-01 sonrası). Koşul: hisse t günü tavan fiyatına değdi, tavanda kapanmadı. Evren: tradable XELKT üyeleri. Sınama: t kapanışında AL, t+1 kapanışında çık; own; **beklenen işaret −1**. IS 208 olay, −99 (t −2,6); OOS-1 241 olay, −82 (t −2,8); yer değiştirme p = 0,003. Kasa: ~136 olay; güç %69 (α = 0,05), Holm'ün en sıkı adımında %42. Mekanizma: tutunamayan talebin çözülmesi.

## DONDURULMUŞ KURAL 2 — `W3A_sektorden_5puan_geride_KACIN_h1`
Girdi: `ret_cc`, `tradable`. Formül: rel1 = r_i(t) − tradable üyelerin eşit ağırlıklı r(t)'si (n ≥ 8). Koşul: rel1 ≤ −0,05 (tabanda kapananlar dâhil). Sınama: AL, 1 gün; sec; **beklenen işaret −1**. IS 537 olay, −120 (t −3,8); OOS-1 305 olay, −148 (t −4,8); 12 yılın 10'u eksi; p = 0,003. Kasa: ~172 olay; güç %89, Holm %72. Mekanizma: bitmemiş satış kuyruğu, ertesi sabah aşağı boşluk.

## DONDURULMUŞ KURAL 3 — `W3A_sektor_dustu_direnen_VIOP_SAT_h1` (izleme)
Girdi: `ret_cc`, `tradable`. Formül: sepet = tradable üyelerin eşit ağırlıklı r(t)'si (n ≥ 5); z = sepet / std(sepet; t−60…t−1; ≥ 40 gün). Koşul: z ≤ −1 ve r_i > 0,5·sepet; i ∈ AKSEN/ENJSA/ODAS. İşlem: aynı hissenin vadelisinde SAT, t kapanışı → t+1; **beklenen işaret +1**. Vadeli fiyatıyla: IS 45 olay, +38 (t 0,9), net +15; OOS-1 38 olay, +74 (t 1,3), net +19. Spot, tam geçmiş, AL yönünden: −90 (t −4,1; 176 olay) / −103 (t −2,0; 39 olay). Komşu z ≤ −1,5: +37 / +92 (25 / 13 olay). Kasa: ~21 olay, güç **%13**: büyük olasılıkla “güç yetersiz”. ENJSA payı %65. SAPMA: olay sayısı için eşik −1,5 yerine −1 seçildi. A2'nin 7. kuralıyla akraba; bağımsız kanıt değil.

Öz-denetim: `self_check_causal` dört kesimde üç kural için 0,0; `build()` 0,2 sn, deterministik.

## Elenenler
K2 (IS t −1,5; kural 2 ile örtüşür) · K3 (kural 2'nin alt kümesi) · beşte birlik (sec −18 / −29) ve 3 günlük göreli getiri (zayıf doz) · K5 bütün hisselerde (own −61 / +2) · K6 · K1'in vadeli sürümü (A4'te dondurulmuş) · vadeli birleşimler (%3'lü olanlar IS'te eksi; K1 ∪ K5 +38 / +109, kural 3'ün kopyası).

## Pratik anlam
- Kapanışta almadan önce iki soru: hisse bugün tavana değip geri mi düştü? Sektör ortalamasının 5 puan gerisinde mi kapandı (taban dâhil)? Biri evetse alma; zayıflık 2–3 gün sürüyor.
- Öneriye dönüşmeleri kasaya bağlı.
- Vadeli SAT için güvenilir kural çıkmadı; kural 3 kâğıt üstünde izlenir.
