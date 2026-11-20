# A2 — endeks ↔ hisse (yalnız IS: 2010 → 2022-12-30)

**Ne tarandı.** Girdiler (t kapanışı): XELKT, EWx (hisse hariç eşit ağırlıklı sepet), BIG, XU030, XU100, SPEC (XELKT − β·XU030; β 250 günlük, gecikmeli), KOMSU. T1 doğrusal, T2 eşikli (z ≥ / ≤ ±1; ±1,5; ±2 → tümü, gecikenler, AKSEN/ENJSA/ODAS), T3 ters yön, T4 koşullu, bayat fiyat (en likit 10; gece/gün içi). h=1, 2, 3.

**Test sayısı.** 1.812 ızgara satırı (1.560'ı ≥ 30 olay günü), 29 keşif satırı, yaklaşık 700 regresyon. BH (q=0,10) geçen 10 satır: 9'u aşağı yönlü, AL yönünde yalnız 1.

**Bulgular.**
- Sektörün kendi yükselişi sürüyor: havuz katsayısı EWx → f1 0,11 (t=3,1), f3 0,25 (t=3,5). Yalnız yukarı yönde (pozitif kısım 0,16, t=3,7; negatif 0,05, t=0,7); ertesi günün gün içinde (gece 0,03; gün içi 0,09); en likit 10 hissede de var (0,10; t=2,7). Bayat fiyat değil.
- Beklenti tutmadı: XU030(t) → hisse f1 −0,05 (t=−1,6); XU030 z ≥ 1,5 → +4,5 bps (t=0,5).
- “Geciken yetişir mi?” Hayır: XELKT z ≥ 1,5 günü gecikenler h=1 +10 bps (t=0,9), net −22; akranlarını geçmiyorlar (sec ≈ +1).
- Aşağı yön güçlü: XELKT z ≤ −1,5 günü düşmeyen hisse ertesi gün −66 bps (t=−3,6): düşüş günü direnen hisse alınmaz.
- T3 büyük hisse → sektör: yok (|t| < 1).

**Ortak tanımlar.** z(X) = X(t) / std(X; t−60…t−1; en az 40 gün). Evren: paneldeki XELKT üyeleri; hedef o gün `tradable` ve tavanda kapanmamış; sepet kurallarında ≥ 5 dolabilir hisse. Giriş t kapanışı, çıkış t+h kapanışı. Geciken: |r_i| < 0,5·|girdi| ya da ters işaret. Rakamlar: gün ortalaması fazla getiri (`own`), bps; net = işlem başına, temel maliyet sonrası.

## DONDURULMUŞ KURAL 1 — birincil: `A2_xelkt_z1_tum_h3`
z(XELKT) ≥ 1 → dolabilir bütün XELKT hisseleri AL (spot), 3 gün. IS: 443 gün (330 bağımsız), +57 (t=3,44); maliyet 41, net +25 (muhafazakâr +0,2). ≤2019 +75 (t=4,9); 2020–22 +18 (t=0,4). En iyi 10 gün hariç +38; t+1 girişi +23; gece payı 0,49. Komşular: z ≥ 1,5 +51; h=2 +39; EWx +41. Yer değiştirme p=0,002; 126 AL kuralı için düzeltilmiş p=0,01. Mekanizma: sektör haberinin yavaş yayılması, tema momentumu.

## DONDURULMUŞ KURAL 2 — ikincil: `A2_xelkt_z1_geciken_h3`
Kural 1 günü, yalnız gecikenler; 3 gün. 432 gün, +64 (t=3,27), net +35; yarılar +85 / +21. Kural 1'in alt kümesi.

## DONDURULMUŞ KURAL 3 — ikincil: `A2_spec_z2_tum_h3`
z(SPEC) ≥ 2 → tümü AL, 3 gün. 114 gün, +61 (t=2,1), net +62; yarılar +36 / +128. En iyi 10 gün hariç +5; z ≥ 1,5 komşusu +24 (sivri).

## DONDURULMUŞ KURAL 4 — ikincil, KEŞİF: `A2_xelkt_z1_xu100alt_tum_h3`
z(XELKT) ≥ 1 ve z(XU100) < 1 → tümü AL, 3 gün. 247 gün, +63 (t=2,95), net +42; yarılar +65 / +58. Izgara dışı.

## DONDURULMUŞ KURAL 5 — ikincil: `A2_komsu_z15_tum_h2`
KOMSU (ASTOR, ALARK, EUPWR, GESAN; mevcut olanlar) z ≥ 1,5 → tümü AL, 2 gün. 248 gün, +37 (t=2,5), net +8. XELKT z < 1 günlerinde +22, net −17: bağımsız değil.

## DONDURULMUŞ KURAL 6 — ikincil: `A2_komsu_z2_aksen_h1`
z(KOMSU) ≥ 2 → AKSEN AL, 1 gün. 102 olay, +69 (t=2,77), net +31; yarılar +57 / +96. 378 tek hisse testinden seçildi.

## DONDURULMUŞ KURAL 7 — ikincil, KEŞİF: `A2_ewx_zm15_geciken_viop_sat_h1`
z(EWx) ≤ −1,5 ve AKSEN/ENJSA/ODAS o gün geciken → vadelide SAT, 1 gün. Vadeli fiyatıyla 28 gün, +92 (t=1,8), net +63; spot tam geçmiş (bilgi) 105 gün, +100 (t=3,5). Olay az.

**Elenenler.** XU030/XU100 kuralları (net ≤ +4); BIG (z ≥ 1,5 h=1: +25, t=2,7; net −40); T3; T4 (AL yönünde BH geçen yok); ENJSA/ODAS vadeli SAT ızgarası (işaret tutarsız); bütün h=1 sepet kuralları (brüt 5–35 < maliyet 40).

**Zayıflıklar.** Kural 1: 2020 (−16) ve 2021 (−73) negatif; muhafazakâr maliyette sıfır; günde 40 hisse alımı gerekir. KOMSU IS'te fiilen ALARK. Hayatta kalma yanlılığı. `elib.py` çalışma sırasında iki kez güncellendi; tablolar son sürümle yeniden üretildi.

**Öz-denetim.** `self_check_causal` dört kesimde yedi kural için 0,0; `build` 0,1 s; deterministik. Regresyonlar: `a2_endeks_regresyon.csv`.
