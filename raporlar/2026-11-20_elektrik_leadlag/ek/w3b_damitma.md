# W3-B — A8 kesit modelinin çözümlenmesi ve sade kurala indirgenmesi

**Sonuç.** Üst dilimin fazla getirisi gerçek, ama al-sat stratejisi değil: temel maliyetle (~38 bps) eksi. Değeri “hangi elektrik hissesini seçmeli, hangisinden kaçınmalı” süzgecinde. 2 kural donduruldu; kasada doğrulanmadan öneri değildir.

## Ne sınandı
169 satır (`ek/w3b_damitma_sonuc.csv`), hepsi `elib.evaluate`, ölçü `sec`, h = 1; rakamlar IS / OOS-1, bps. “Ek” kırılımlar (gece, medyan, devir) elib'in iç fonksiyonlarıyla. SAPMA: kurallar iki dönem birlikte görülerek seçildi; tek geçerli sınama kasadır.

## Bulgular
1. **Neden 4 → 23?** Tahmin beşte birlikleri: IS −10,8 / −1,2 / +5,7 / +5,6 / +6,1; OOS-1 −42,2 / −1,6 / −1,4 / +24,6 / +24,9. IS'te yalnız kaçınma var; OOS-1'de üst iki dilim de artıda. Yıllar: 2023 +38, 2024 +12, 2025 +14 (IS −15 … +19). Evren 10 → 30 hisse. Eski hisseler içinde +21 (t 3,3), yeniler içinde +25 (t 4,4); fiyat ≥ 5 TL +23 (t 5,2). Likidite üçte birlikleri tutarsız: IS +2 / +8 / +13, OOS-1 +27 / +34 / +11. `own` ≈ 0 yanıltıcı: OOS-1'de bütün sektörün `own` değeri −22 (2022 rallisi kıyası şişirdi); seçilenlerin olağan kayması evrenden yalnız 1 bps/gün yüksek.
2. **Gece / gün içi.** OOS-1: gece +7,3 (t 4,8), t+1 açılış → kapanış +15,2 (t 3,7); IS 0,7 / 3,1. “Açılıştan girişte 5 bps kalıyor” IS + OOS-1 havuzudur; OOS-1'de açılış girişi kazancın üçte ikisini korur. Kapanıştan kapanışa net: OOS-1 düşük −2, temel −17, muhafazakâr −42; IS −18 / −33 / −58. h = 2: +17,6 (net −22); h = 3: +20,2 (net −20). Fazla getiri ilk günde; üst dilimin %69'u her gün değişiyor.
3. **Üst mü, alt mı?** İki dönemde de sağlam olan alt uç: en alt onda birlik −32 (t −2,9) / −60 (t −6,8). Üst dilim sektör ortalamasını günlerin %48 / %46'sında geçiyor. Medyana göre +22 / +48, ama getiriler sağa çarpık: alt dilim bile IS'te medyanın 9 bps üstünde.
4. **Taşıyan özellikler.** Kazanç payı (OOS-1): günlük göreli getiri 0,19, hacim şoku 0,13, 20 günlük oynaklık 0,11; bayraklar 0. Tek sıralamalar: oynaklık en üst beşte birlik −15 (t −3,7) / −24 (t −4,1); hacim şoku en üst −9 / −29; günün en kötüleri −8 / −26; oynaklık en alt +4 / +10; günün en iyileri 0 / −1. Kaçınma listesi (bayrak ya da bu üç beşte birlikten biri; sektörün ~%45'i): −5,6 (t −2,4) / −16,9 (t −6,1); kalan “temiz” hisseler +3,8 / +13,0.

## DONDURULMUŞ KURAL 1 — `W3B_sade_sakin_guclu_h1` (model yok)
- Evren: dolabilir XELKT üyeleri (o gün ≥ 6).
- Koşullar, t kapanışında: (a) gün içinde tavana ya da tabana değmemiş; (b) son 20 günün günlük getiri standart sapması sektörün alt yarısında; (c) günlük getirisi sektörün en üst üçte birliğinde.
- AL, spot; giriş t kapanışı, çıkış t+1 kapanışı; ölçü `sec`; beklenen işaret +1.
- IS: 2.548 gün, +10,5 (t 2,71), isabet %47, net temel −25. OOS-1: 616 gün, +17,1 (t 3,03), isabet %45, net −24. 15 yılın 11'i artı; en iyi 10 gün hariç +8,3; kaydırma p 0,020 / 0,007; açılış girişi +9,2 / +11,8. 18 komşunun hepsi iki dönemde artı. Zayıflık: en likit üçte birlikte −3 / +4.
- Kasa: ~350 gün, ~1.600 işlem; standart hata ≈ 7,5. %80 güç için ≥ 24 bps (α = 0,01); beklenen 10–17'de güç %18–48.

## DONDURULMUŞ KURAL 2 — `W3B_lgbm_tahmin20_temiz_h1`
- Girdi: A8 LightGBM h1 tahmini (`kod/a8_model/rules.py`, değiştirilmeden).
- Koşullar: dolabilir; bayraksız; günlük getiride en alt, hacim şokunda (ln[TL hacim / önceki 20 günün medyanı]) ve 20 günlük oynaklıkta en üst beşte birlikte değil; tahmin > +20 bps.
- AL, spot, 1 gün, `sec`, beklenen işaret +1.
- IS: 1.118 gün, +23,0 (t 3,79), net temel −9,4, düşük +5,6. OOS-1: 507 gün, +24,7 (t 3,17), net −8,0, düşük +7,0. 14 yılın 11'i artı (2024: −4); en iyi 10 gün hariç +16,8; kaydırma p 0,007 / 0,003. Eşik 10 / 30 bps: IS +12 / +28, OOS-1 +19 / +27.
- Kasa: ~290 gün, ~1.100 işlem; standart hata ≈ 10. %80 güç ≥ 33 bps; beklenen ~24'te güç ~%50.

## Elenenler
Üst onda birlik (IS t 1,3); süzgeçsiz tahmin eşikleri (IS t < 1); 250 günlük momentum, halka arz yaşı, likidite (işaret tutarsız); düşük hacim şoku (IS −3); 2–3 gün tutma.

## Kullanıcı için
- Bu kurallarla al-sat yapılmaz.
- Zaten elektrik hissesi alacaksan önce kaçın: o gün tavana/tabana değen, günün en kötüleri, hacmi patlayan, son 20 günü en oynak olanlar (günde ~13 hisse). Kalanlardan sakin ve o gün sektörden iyi olanı seç (~5 hisse). Beklenen fark günde 15–35 bps. İsabet yazı-turadan iyi değil; kazanç büyük kayıplardan kaçınmaktan geliyor.
- TradingView tarayıcısı: “Değişim %” (üst üçte bir), “Oynaklık (ay)” (alt yarı; vekil), gün içi en yüksek/düşük ile ±%10 sınırı.

## Öz-denetim
`self_check_causal` (kesim 2018-09-14, 2021-06-30, 2024-06-28): iki kural 0,0. `build()` 9 sn, deterministik; `run.sh` 99 sn.
