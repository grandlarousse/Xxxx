# A8 — Birleşik model (yalnız IS; ileriye dönük tahminler 2012-01 → 2022-12)

**Sonuç: birincil kural dondurulmadı.** Model sıralaması istatistiksel olarak gerçek ama küçük; kazanç “kaçınma” tarafında. En iyi spot AL kuralı temel maliyetle tam başabaş (net +0,01 bps), diğerleri eksi. 4 ikincil kural donduruldu.

## Ne tarandı
23 özellik; her ay başında son 750 işlem günüyle (en az 500) eğitim, hedefler h+5 gün ambargolu. Önceden yazılı ızgara (`scan.py` başlığı): kesit (`sec` f1–f3) 30 yapılandırma (ridge 12, lasso 12, LightGBM 6) ve 14 kıyas modeli, her biri en üst ve en alt beşte birlik; sahte etki 12 satır; zamanlama (`own`) 27; tek hisse 6; keşif 5; 4 kaydırma testi.

**Toplam 138 değerlendirme satırı; 60'ı aday türü.**

## IS bulguları
1. **IC:** ridge(lam=1) 0,030 (t 4,3); LightGBM(d3, yaprak 500) 0,043 (t 6,2); 11 yılın 10'unda pozitif; yarılar 0,037 / 0,059.
2. **Kaynak kısa vadeli dönüş değil:** yalnız rel1 IC −0,004; dönüş grubu 0,003; dönüş dışı grup 0,042 (t 5,9). Hacim şoku ve 20 günlük oynaklık katsayıları yeniden eğitimlerin %98 ve %90'ında negatif. Modelsiz rel1 dönüşü 2020 sonrası kayboluyor (IC 0,035 → −0,005).
3. **Öngörü alt uçta:** en alt beşte birlik −10,8 bps (t −2,7; dönüş dışı ridge −18,5, t −4,1); en üst +3,8 bps (t 1,1), net −37,6. Spotta açığa satış yok; üç VİOP hissesinde SAT tarafı ~0 bps.
4. **Kararsızlık:** girdiler 1 bps'e yuvarlanınca LightGBM üst dilimi 6,6 → 3,8 bps oldu, IC değişmedi. Kaydırma sıfırı p = 0,26.
5. **Sahte etki:** en likit 15: 4,6 bps; fiyat ≥ 5 TL: 7,3 (731 gün, t 0,7); üçte birlik 5,5 (t 2,2); gece payı 0,7 bps; t+1 kapanış girişi 5,0.
6. **Zamanlama:** 24 satırın 23'ü brüt pozitif; 22'si net eksi, biri başabaş. Yalnız sektör r(t): 4–6 bps (t ≤ 1,05). Katkı: sektör medyan hacim şoku, genişlik, XU030 3 günlük. BH (q = 0,10) brüt etkide 4 satırı geçiriyor.

## DONDURULMUŞ KURAL 1 (ikincil) — `A8_kesit_lgbm_d3_m500_h1_ust20`
Girdi: 23 özellik (`rules.py: features`). LightGBM: derinlik 3, 8 yaprak, min 500 gözlem, 80 ağaç, öğrenme 0,05, L2 10, tohum 7. Hedef: `sec` f1, ±%10 kırpılmış. Evren: dolabilir XELKT üyeleri (≥ 5). Tahmini en yüksek tavan(n/5) hisse AL; giriş t kapanışı, çıkış t+1 kapanışı. IS: 2.763 gün, +3,8 bps (t 1,09), net −37,6. Mekanizma: hacim/oynaklık patlaması yaşayanlardan kaçınma.

## DONDURULMUŞ KURAL 2 (ikincil) — `A8_zaman_ridge_l1_h2_e25`
Girdi: sec1, sec3, xu1, xu3, xres, big1, nlimup, dow_mon, dow_fri, secvol20, breadth, vsh_med. Ridge, ceza 1·n, standart X (±5σ). Hedef: dolabilir üyelerin `own` f2 ortalaması. Tahmin > +25 bps ve ≥ 5 dolabilir üye → hepsi AL, 2 gün. IS: 402 gün (293 bağımsız), 40,3 bps (t 2,77), başabaş 43,05, maliyet 43,04; yarılar 50,7 / 25,1; 9/11 yıl pozitif (2021: −110); t+1 girişi 24,9. Birincil yapılmadı: net sıfır ve komşular (10–32 bps) net eksi; lam=10'da IC ≈ 0. Mekanizma: yüksek hacimli, geniş katılımlı sektör hareketinin devamı.

## DONDURULMUŞ KURAL 3 (ikincil) — `A8_zaman_ridge_l1_h3_e0`
Aynı model, hedef f3, eşik 0, 3 gün. IS: 1.445 gün (626 bağımsız), 24,8 bps (t 2,34), net −14,3; yarılar 26,9 / 18,9.

## DONDURULMUŞ KURAL 4 (ikincil, KEŞİF) — `A8_kesif_3hisse_lgbm_d3_m500_h1_ust20_long_viop_own`
Kural 1'in üst diliminde AKSEN/ENJSA/ODAS varsa VİOP AL, 1 gün. IS: 373 gün, 28,4 bps (t 1,98), net +4,8; vadeli fiyatlarıyla 23,8 bps (t 1,53), net −8,7; %69 ENJSA.

## Elenenler
Ridge/lasso üst dilimleri (−14 … +6 bps); LightGBM h2/h3 (h3 yarıları ters işaretli); tek hisse eşikli kurallar (121 gün, %85 ENJSA).

## Öz-denetim
`self_check_causal` (kesim 2021-06-30 ve 2018-09-14): dört kural 0,0. İki build aynı; süre 6 sn.

## Bilinen zayıflıklar
- 2019'a kadar ~10 hisse: beşte birlik 2 hisse; hayatta kalma yanlılığı.
- Hiperparametre tam IS yürüyen IC'siyle seçildi.
- SAPMA: BIG sepeti adv60'a göre ilk 5; tavan özelliği “dün tavan” + “bugün tavana dokundu”.
- panel_dev ile karşılaştırılamadı: LightGBM'de küçük sayısal fark olasılığı sıfır değil.
