# A1 — hisse → hisse ikili öncülük (yalnız IS: 2010-01-04 → 2022-12-30)

**Sonuç: birincil kural yok.** Dört ikincil (izleme) kuralı donduruldu.

## Ne tarandı, kaç test
- T1 doğrusal: 420 sıralı çift (≥ 250 ortak gün), h = 1, 2, 3 → 1.259 regresyon; sektör kontrolsüz 1.259. T2 olay: 3.948 test. Yarı dönem, gece/gün içi, çift farkı: 10.117. Kural ızgarası 102 satır, aday denetimi 38. Toplam ≈ 16.700 test (sıfır dağılımı hesapları hariç).

## IS bulguları
- T1: |t| ≥ 2 oranı %5,7 (sektör kontrolsüz %9,8; fark sektör geneli otokorelasyon). BH geçen: h=1'de 0; h=2 ve 3'te 1 (AYEN → ZOREN, t = 3,8). En büyük |t| için kaydırma p = 0,39 / 0,09 / 0,09.
- T2: BH geçen 10 testin 10'u negatif; AL yönünde kullanılamaz. Kaydırma p = 0,86 / 0,12 / 0,11.
- Kalıcılık (çiftin iki yarısı): ilk yarıda anlamlı 26 bağın %54'ü ikinci yarıda aynı işarette, hiçbiri yeniden anlamlı değil. Lider skoru sıra korelasyonu −0,18 (takvim bölmesinde 0,19; 11 hisse).
- Önceden yazılı çiftler (NATEN–ESEN–MAGEN, ODAS–CANTE): |t| ≥ 2,5 yok. AHGAZ–ENERY, güneş kümesi, ASTOR IS'te sınanamadı. Büyükler → diğerleri: havuz t = −0,29. Çift farkı dönüşü: |t| ≤ 1,8. Küme içi bağ oranı %9,6, kümeler arası %3,8.
- Bayat fiyat değil: ortalama t düşük likiditeli hedefte 0,03, yüksekte 0,44; katsayının medyan %10'u gece.

## DONDURULMUŞ KURAL 1 (ikincil) — A1_LN_W250_c2.0_th1.5_h1
- Girdi: `ret_cc`, `tradable`, `fill_long`. z_j(t) = r_cc / 60 günlük, 1 gün gecikmeli std (±4 kırpılı). ez_i = (r_i − diğer tradable XELKT üyelerinin eşit ağırlıklı ortalaması) / kendi 60 günlük gecikmeli std'si.
- Lider istatistiği t_ji(t): son 250 satırda z_j(s−1)·ez_i(s) çarpımlarının (s ≤ t; i, s−1'de dolabilir; ≥ 120 gözlem) ortalamasının t'si.
- Sinyal: Σ_j işaret(t_ji)·1{|t_ji| ≥ 2}·z_j(t) / √K ≥ 1,5 (K = etkin lider sayısı ≥ 1). Kaynak: XELKT + ASTOR, ALARK, EUPWR, GESAN. Hedef: dolabilir XELKT üyesi. t kapanışında AL, t+1 kapanışında çık.
- IS: 562 gün, 777 işlem; fazla getiri +33,6 bps (t = 3,06; kaydırma p = 0,002). İşlem başına brüt 30,0, maliyet 41,8, net −11,8. Yarılar +31 / +38; 12 yılın 10'u pozitif; en iyi 10 gün hariç +17; t+1 kapanışından giriş +25; gece payı 0,23; en yoğun hisse %15.
- Mekanizma: bilginin geçmiş liderlerden kademeli yayılması.

## DONDURULMUŞ KURAL 2 (ikincil) — A1_LN_W250_c2.0_th1.5_h2
Kural 1'in sinyali; çıkış t+2 kapanışı. IS: +54,0 bps (t = 3,08; p = 0,002); brüt 42,8, net +1,0; yarılar +77 / +13; en iyi 10 gün hariç +20.

## DONDURULMUŞ KURAL 3 (ikincil) — A1_LN_W500_c1.5_th1.5_h2
Kural 1'in formülü; pencere 500, |t_ji| ≥ 1,5, skor ≥ 1,5, çıkış t+2. IS: +30,0 bps (t = 2,45; p = 0,014); brüt 30,1, net −12,7; yarılar +43 / +2; 2021–22 negatif.

## DONDURULMUŞ KURAL 4 (ikincil, çifte özgü) — A1_FL_th2.0_h1
Sabit liste: ODAS, AYEN → ZOREN; ODAS → AKSEN. Σ z_j(t) / √K ≥ 2 → hedefte AL, 1 gün. IS: 211 gün; +33,6 bps (t = 2,31; p = 0,02); brüt 34,9, net −13,3; ZOREN payı %57. Liste IS'te seçildi: rakam yanlıdır, yeni hisselere genellenemez. Mekanizma: ODAS hareketinin ertesi gün büyüklere yayılması.

## Neden birincil yok, elenenler
- 102 satırın hiçbiri (i)–(v) ölçütlerini birlikte karşılamadı. Lider ağının 36 satırının 36'sında brüt pozitif (0,9–45,7 bps) ama maliyet ~42 bps; net yalnız 2 satırda > 0 ve komşuları negatif.
- Grup çifti olayı (30 satır): yukarı olay negatif; aşağı olay pozitif ama kaydırma p ≈ 0,2, en iyi 10 gün çıkınca ≈ 0.
- Grup çifti farkı (18), küme farkı (9): yetişme yok.

## Bilinen zayıflıklar
- Düşük maliyet senaryosunda (10 bps) net +2…+16 bps; muhafazakârda negatif.
- 2023+ evreni 40'tan fazla hisse; yeni listelenenlerde IS işlemi az (55 işlem, −0,5 bps).
- Öz-denetim: `self_check_causal` dört kural için 0,0; ızgaradaki 102 kural için 0. `build` 0,3 sn.
- KÜTÜPHANE NOTU: `top10_haric_bps` en iyi max(10, %5) günü çıkarıyor (Kural 1: −3,5). Tam 10 gün için `en_iyi_10_gun_haric_bps` sütunu eklendi. `gece_payi` 'own' ölçüsüyle hesaplanıyor.
