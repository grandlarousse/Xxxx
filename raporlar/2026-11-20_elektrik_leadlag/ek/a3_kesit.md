# A3 kesit: geride kalanın yetişmesi, büyük → küçük, hacim (yalnız IS, 2010–2022)

**Sonuç: birincil kural dondurulmadı.** Ana ızgaranın 108 satırından hiçbiri seçim ölçütlerini karşılamadı; BH (q = 0,10) geçen yok (en büyük t = 1,93). 5 ikincil kural bilgi amaçlı donduruldu.

## Ne tarandı, kaç test
- T1 Fama–MacBeth: 21 regresyon (rel1/3/5, hacim şoku, taban, tavan; h = 1–3).
- T2 beşte birlik sepetleri: 18 satır + 36 koşullu (sektör k günlük getirisi > +%2 / < −%2).
- T3 büyük → küçük, T4 yüksek → düşük hacim: 12 zaman serisi regresyonu, 54 kural satırı (z ∈ {1; 1,5; 2}).
- Kontroller: 108 satır (ham fiyat ≥ 5 TL; en likit 15). Ek: 45 satır (taban ayrıştırması, VİOP kısa yön, keşif).
- Toplam 294 istatistik. Tablolar: `a3_kesit_sonuc.csv`, `a3_kesit_regresyon.csv`, `a3_kesit_tanilama.txt`.

## IS bulguları
1. **Yetişme yok.** rel1 katsayısı +0,008 (t = 0,65). En geride kalan beşte birlik ertesi gün sektörün 18 bps altında (t = −3,07; yarılar −8 / −41). Bunun tamamı tabanda kapananlardan: 186 işlem, −434 bps; taban hariç −4,7 bps (t = −0,86).
2. Öne geçen geri dönmüyor: rel1 üst beşte birlik −3 bps (t = −0,5).
3. Büyük → küçük: R_big(t) katsayısı 0,036 (t = 1,1); 2020–22'de 0,029 (t = 0,5). Beklenen gecikme görülmedi. Büyükler z ≤ −1 düşünce küçükler ertesi gün −41 bps (own, t = −2,7).
4. Yüksek → düşük hacim: h = 2–3 katsayısı 0,075–0,109 (t = 2,2–2,5); eşikli kuralda t < 2.
5. Maliyet ~40 bps: temel maliyet sonrası artıda kalan 7/90 satırın hiçbirinde |t| ≥ 2 yok.

## Dondurulan kurallar (hepsi ikincil)
Ortak tanımlar: evren = paneldeki XELKT üyeleri, t günü `tradable`. r_k = k günlük bileşik getiri; rel_k = r_k − üyelerin eşit ağırlıklı r_k'sı (n ≥ 8). Beşte birlik = gün içi sırada floor(n/5) hisse. Hacim şoku = ln(TL hacim / önceki 20 günün medyanı). Üçte birlik = floor(n/3), n ≥ 9. Sepet z'si = sepetin eşit ağırlıklı r_cc(t)'si / önceki 60 günün std'si. Giriş t kapanışı, çıkış t+h kapanışı, yön AL.

### DONDURULMUŞ KURAL A3_rel5_ust5_h3
rel5 en üst beşte birlik; h = 3; ölçü sec. IS: 2.332 gün, +23,1 bps (t = 1,52), net −20,0; yarılar +12 / +47; t+1 girişte +33. Mekanizma: 5 günlük göreli güç sürüyor. Eleme nedeni: net ≤ 0.

### DONDURULMUŞ KURAL A3_vhi_z15_vlo_h3
Hacim şoku en yüksek üçte birliğin z'si ≥ 1,5 → en düşük üçte birlik; h = 3; ölçü own. IS: 294 gün, +48,4 bps (t = 1,89), net +18,2; yarılar +82 / +16; sec +20,5 (t = 1,2). Mekanizma: ilgi gören hisseler önce, ilgisizler 2–3 gün sonra fiyatlanıyor. Eleme: t < 2; ≥ 5 TL hisselerde +4,6 bps; 2021 −124.

### DONDURULMUŞ KURAL A3_big_z10_small_h3
`adv60` sırasında en büyük üçte birliğin z'si ≥ 1 → en küçük üçte birlik; h = 3; own. IS: 300 gün, +47,0 bps (t = 1,60), net +21,4; yarılar +81 / +5; en iyi 10 gün çıkınca −7,9. Mekanizma: Lo–MacKinlay gecikmesi.

### DONDURULMUŞ KURAL A3_rel1_alt5_viop_al_h1 (keşif)
rel1 en alt beşte birliğe düşen AKSEN/ENJSA/ODAS → vadelide AL; h = 1; sec. IS: 198 gün, +23,7 bps (t = 1,28), net −0,2; own +46,6 (t = 2,43); vadeli fiyatıyla +29,9 (t = 1,40). ENJSA payı %55; t+1 girişte −1,3.

### DONDURULMUŞ KURAL A3_rel1_alt5_h1_RED
rel1 en alt beşte birlik → AL; h = 1; sec. Alım kuralı değil: “yetişme” hipotezinin doğrudan sınaması, beklenen işaret negatif. IS: 2.376 gün, −18,4 bps (t = −3,07).

## Bilinen zayıflıklar
- Sıralama n ≥ 8 gerektirdiği için sonuçlar 2013 sonrasını kapsıyor; 2019'a kadar bir beşte birlik 2 hisse.
- `elib` `top10_haric_bps` en iyi max(10, %5) günü çıkarıyor; binlerce günlük kurallarda mekanik olarak negatif. Ek sütun: `top10gun_haric_bps`.
- Öz-denetim: `self_check_causal` beş kural için 0,0; `build()` 0,1 s, deterministik.
