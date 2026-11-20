# A6 — VİOP (AKSEN, ENJSA, ODAS pay vadelileri; XU030 vadelisi) — yalnız IS (→ 2022-12-30)

**Ne tarandı.** Önceden yazılı ızgara, 234 kural (= test): V1 kendi baz sıçraması (Δbaz = ln(1+vadeli getirisi) − ln(1+spot getirisi); z = Δbaz / 120 günlük gecikmeli std; uzlaşma ve son fiyat; z ∈ {1; 1,5; 2}; iki yön; h ∈ {1,2,3}) 72; V2 vadeli hacim / açık pozisyon sıçraması 18; V3 XU030 vadelisi bazı 72; V4 çapraz 72. Ayrıca 17 keşif testi. Kod: `kod/a6_viop/run.sh`.

**Sonuç.** BH (q = 0,10) geçen kural yok; t > 2 olan 11 kural var. Aile içi en iyi kuralın yer değiştirme p-değeri 0,28: 234 testin en iyisi şansla açıklanabilir. “Baz geri döner” etkisi yok: baz yukarı sıçrayınca spot da vadeli de aynı yönde sürüyor (zayıf). V3 bütünüyle olumsuz.

**Vadelinin gerçek maliyeti** (`ek/a6_viop_likidite.csv`): işlemsiz gün yok. Fiyat adımı ODAS'ta medyan 47 bps (2022: 32), ENJSA 10, AKSEN 2: ODAS'ta tek adımlık makas temel senaryodaki 35 bps'ye yakın ya da üstünde. Uzlaşma − son fiyat mutlak farkı 22–37 bps. Uzun vadeli pozisyon spota göre günde 9 (ENJSA), 14 (ODAS), 15 (AKSEN) bps taşıma öder (yıllık %20–30). Vadeli hacmi spotun %17–44'ü.

## DONDURULMUŞ KURAL 1 (BİRİNCİL): `A6_V4_akran_vadeli_getiri_z1_spotAL_h2`
- Girdi: `viop_front.ret_settle` (hacmi en yüksek vade, aynı kontrat), AKSEN/ENJSA/ODAS.
- Formül: z_j(t) = ret_settle_j(t) / std(ret_settle_j, t−60…t−1; en az 40 gün). Hedef i için sinyal: j ≠ i olan en az bir üyede z_j ≥ 1.
- Evren: hedef yalnız üçlü, dolabilir. Giriş t kapanışı spot AL, çıkış t+2 kapanışı.
- IS: 159 bağımsız olay, fazla getiri +85 bps (t = 3,09), temel maliyet sonrası +47; yarılar +107 / +64; yıllar 2019–2022: 181, 103, 61, 56 (azalıyor); en iyi 10 gün hariç +38; t+1 kapanışından giriş +71; gece payı 0,2; en yoğun hisse payı 0,5, üç hedef de pozitif. Komşular: z 1,5 t = 2,5; z 2 t = 1,8. Kontrollü regresyonda (kendi getirisi, XU100) +67 bps, t = 2,4.
- Mekanizma: sektör haberi önce bir üyede fiyatlanır, diğerleri 1–2 gün gecikir. **Vadeliye özgü değil:** aynı kural spot getirisiyle +53 bps (t = 2,7) veriyor; A1/A2 kurallarıyla örtüşebilir.

## DONDURULMUŞ KURAL 2–7 (İKİNCİL)
2. `A6_V4_…_spotAL_h3`: aynı sinyal, 3 gün. +105 bps, t = 2,8, net +65.
3. `A6_V4_…_viopAL_h2`: aynı sinyal, hedefin vadelisi AL. 82 olay, +41, t = 0,9, net +5: IS'te kanıt yok (2021-04+).
4. `A6_V1_dbaz_uzl_z1.5_yuk_spotAL_h2`: kendi Δbaz (uzlaşma) z ≥ 1,5 → spot AL, 2 gün. 37 olay, +160 bps, t = 3,0; son fiyat tanımında net +23; en iyi 10 hariç +5.
5. `A6_V1_dbaz_uzl_z1_yuk_spotAL_h3`: z ≥ 1, 3 gün. 91 olay, +88, t = 2,0; kontrolde t = 1,3; ağırlık ODAS'ta.
6. `A6_V2_vadeli_hacim3x_yuk_spotAL_h3`: vadeli toplam TL hacmi > 3 × 20 günlük gecikmeli medyan ve vadeli getirisi > 0 → spot AL, 3 gün. 53 olay, +143, t = 2,1; en iyi 10 hariç +11.
7. `A6_V4K_kesif_…`: kural 1 ve hedefin kendi getirisi / std60 < 1. 147 olay, +111, t = 3,8. **Keşif** (sonuç görüldükten sonra tanımlandı).

**Öz-denetim.** `elib.self_check_causal` yedi kuralın hepsinde 0,0 (kesim 2021-06-30 ve 2022-06-30); build 0,1 sn, deterministik.

**Elenenler.** V1 aşağı yön ve vadeli bacakları; V2 açık pozisyon; V3'ün tamamı; V4 Δbaz kaynağı ve aşağı yön. Kısa (SAT) yönde ölçütleri geçen kural yok. Nedenler: `ek/a6_viop_sonuc.csv`, `not` sütunu.

**Bilinen zayıflıklar.** (1) IS fiilen ENJSA (2019-03+) ve ODAS (2021-07+); AKSEN vadelisi 44 gün, sinyal üretmedi. (2) Sinyal uzlaşmayı kullanır (18:10), spot kapanışı 18:05'te oluşur: t kapanışında giriş yaklaşık hesap ister; t+1 girişi de pozitif. (3) Birincil kuralın etkisi yıldan yıla azalıyor; ENJSA kaynaklı kol 2022'de −17 bps. (4) ODAS'ta fiyat adımı maliyeti temel senaryoda eksik.
