araç: 13/40

**ÖZET**

A8 üst beşte birliğinin OOS-1'deki 23 bps'i gerçek bir kesit etkisi, ama al-sat stratejisi değil. Temel maliyetle eksi; değeri hisse seçme / kaçınma süzgecinde. 2 kural donduruldu; ikisi de `self_check_causal` = 0,0.

1. **Neden 4 → 23:** IS'te yalnız kaçınma var (beşte birlikler −10,8 / −1,2 / +5,7 / +5,6 / +6,1). OOS-1'de üst iki dilim de artıda (−42,2 / −1,6 / −1,4 / +24,6 / +24,9).
   - Yıllar: 2023 +38, 2024 +12, 2025 +14.
   - Yeni halka arzlardan gelmiyor: eski hisseler içinde +21, yeniler içinde +25. Fiyat ≥ 5 TL'de +23.
   - Likidite üçte birlikleri iki dönemde tutarsız.
   - `own` ≈ 0 yanıltıcı: OOS-1'de bütün sektörün `own` değeri −22 bps/gün (2022 rallisi kıyası şişirdi). Seçilenlerin olağan kayması evrenden yalnız 1 bps/gün yüksek; model yüksek kaymalı hisse seçmiyor.
2. **Gece / gün içi (düzeltme):** "açılıştan girişte 5 bps kalıyor" rakamı IS + OOS-1 havuzudur. OOS-1'de gece +7,3, açılış → kapanış +15,2: boşluk kazancın üçte biri.
   - Kapanıştan kapanışa net (OOS-1): düşük −2, temel −17, muhafazakâr −42.
   - h = 2 ve 3 brüt +17,6 / +20,2 (net −22 / −20): fazla getiri ilk günde.
   - Üst dilimin %69'u her gün değişiyor.
3. **Üst mü alt mı:** iki dönemde de sağlam olan alt uç (en alt onda birlik −32 / −60). Üst dilim sektör ortalamasını günlerin %48 / %46'sında geçiyor. Medyan kıyası çarpıklık yüzünden yanıltıcı.
4. **Taşıyan özellikler:** günlük göreli getiri, hacim şoku, 20 günlük oynaklık; bayrakların model önemi 0.
   - Kaçınma listesi (bayrak, ya da günün en kötü, hacim şoku en yüksek, oynaklığı en yüksek beşte birliği; sektörün ~%45'i): −5,6 / −16,9.
   - Kalan "temiz" hisseler: +3,8 / +13,0.
5. **Dondurulan kurallar** (`sec`, long, spot, h = 1, beklenen_isaret +1):
   - **K1 `W3B_sade_sakin_guclu_h1`** (model yok): dolabilir, gün içinde tavana/tabana değmemiş, 20 günlük oynaklığı sektörün alt yarısında, günlük getirisi en üst üçte birlikte. IS +10,5 (t 2,71), OOS-1 +17,1 (t 3,03); net temel −25 / −24. 18 komşunun hepsi iki dönemde artı.
   - **K2 `W3B_lgbm_tahmin20_temiz_h1`**: A8 tahmini > +20 bps ve hisse temiz. IS +23,0 (t 3,79), OOS-1 +24,7 (t 3,17); net temel −9 / −8, düşük maliyetle +6 / +7.
6. **Kasa gücü sınırlı:** K1'de %80 güç için ≥ 24 bps, K2'de ≥ 33 bps gerekir (α = 0,01). Beklenen etkide güç K1 %18–48, K2 ~%50; olası sonuç "güç yetersiz".

SAPMA: kurallar IS ve OOS-1 birlikte görülerek seçildi (169 satır tarandı). İki dönemdeki t değerleri bağımsız doğrulama sayılmaz.

KÜTÜPHANE HATASI (küçük): `elib.evaluate` içindeki `giris_acilis1_bps`, `giris_kapanis1_bps` ve `gece_payi` dönem ayırmadan IS + OOS-1 havuzunda hesaplanıyor. `gece_payi` kesit kurallarında da `own` ölçüsüyle hesaplanıyor (lgbm_ust20 için −1,3, anlamsız). E5 etiketi `sec` kurallarında güvenilmez.

Not: `kod/ortak/elib.py` çalışmam sırasında başka bir süreççe değişti (`per` ölçüsü eklendi); ben dokunmadım. `sec` satırlarım etkilenmedi: CSV'nin md5'i değişiklikten önce ve sonra aynı.

**İDDİA DEFTERİ** (iddia | dosya yolu | sayı | güven) — CSV = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/w3b_damitma_sonuc.csv; günlükler = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3b_damitma/out/

A8 üst %20 yeniden üretildi | CSV: lgbm_ust20 | IS +3,8 (t 1,09); OOS-1 +22,8 (t 5,43) | yüksek
Tahmin beşte birlikleri | CSV: lgbm_dilim1..5/5 | IS −10,8/−1,2/+5,7/+5,6/+6,1; OOS-1 −42,2/−1,6/−1,4/+24,6/+24,9 | yüksek
En alt onda birlik | CSV: lgbm_ondalik1/10 | IS −31,7 (t −2,85); OOS-1 −59,9 (t −6,75) | yüksek
Yıllara göre üst %20 | CSV: lgbm_ust20, yillar_bps | 2023:38; 2024:12; 2025:14; IS −15…+19 | yüksek
Eski / yeni hisseler içinde sıralı | CSV: lgbm_ust20_eski_icinde_sirali, _yeni_ | OOS-1 +21,2 (t 3,26) / +25,2 (t 4,38) | yüksek
Fiyat ≥ 5 TL | CSV: lgbm_ust20_fiyat5_icinde_sirali | IS +7,3 (t 0,73); OOS-1 +22,6 (t 5,16) | yüksek
Likidite üçte birlikleri (içinde sıralı; düşük/orta/yüksek) | CSV: lgbm_ust20_lik_*_icinde_sirali | IS +2,3/+8,2/+13,0; OOS-1 +27,4/+34,3/+10,9 | yüksek
`own` üst %20 | CSV: lgbm_ust20_own | IS +1,1; OOS-1 −1,2 | yüksek
Sektörün tamamının `own` değeri OOS-1'de | CSV: TABAN_tum_eski / TABAN_tum_yeni, dol_own_OOS1 | −22,4 / −21,3 bps/gün | yüksek
Seçilenlerin olağan kayması − evren (ek) | günlükler: s1_log.txt | IS +1,9; OOS-1 +1,0 bps/gün | orta
Gece / gün içi, üst %20 (ek) | günlükler: s1_log.txt | OOS-1 gece +7,3 (t 4,76), açılış→kapanış +15,2 (t 3,73); IS 0,7 / 3,1 | orta
"5 bps" havuz rakamıdır | CSV: lgbm_ust20, giris_acilis1_bps / giris_kapanis0_bps | 5,3 / 7,3 (IS+OOS-1) | yüksek
Net, üst %20 (düşük/temel/muhafazakâr) | CSV: lgbm_ust20 | IS −17,8/−32,8/−57,8; OOS-1 −1,9/−16,9/−41,9 | yüksek
Tutma 2 ve 3 gün | CSV: lgbm_ust20_tut2, _tut3 | OOS-1 +17,6 (net −21,8), +20,2 (net −19,6); IS +8,4, +6,9 | yüksek
Devir (ek) | günlükler: s1_log.txt | günlük yeni pozisyon payı IS %59, OOS-1 %69 | orta
İsabet, üst %20 (sektör ortalamasına karşı) | CSV: lgbm_ust20 | 0,476 / 0,462 | yüksek
Özellik önemi, OOS-1 kazanç payı | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3b_damitma/out/onem.csv | rel1 0,188; volshock 0,131; vol20 0,111; r20 0,088; bayraklar 0 | yüksek
Oynaklık en üst / en alt beşte birlik | CSV: tek_vol20_ust20, _alt20 | −15,4 (t −3,72) / −23,7 (t −4,10); +4,2 (t 1,61) / +10,3 (t 2,44) | yüksek
Hacim şoku en üst; günün en kötüleri | CSV: tek_volshock_ust20, tek_rel1_alt20 | −8,5 / −29,1; −8,0 / −25,7 | yüksek
Kaçınma listesi (4 koşul) | CSV: KACIN_bayrak\|rel1alt20\|hacim\|oynaklikust20 | günde 4,4 / 13,4 hisse; −5,6 (t −2,38) / −16,9 (t −6,09) | yüksek
Temiz hisseler | CSV: TEMIZ4_+oynaklik_ust20degil | +3,8 (t 2,26) / +13,0 (t 5,73) | yüksek
K1 sonuç | CSV: W3B_sade_sakin_guclu_h1 | IS 2.548 gün +10,5 (t 2,71) net −25,3; OOS-1 616 gün +17,1 (t 3,03) net −23,5; günde 1,7 / 4,6 hisse | yüksek
K1 sağlamlık | günlükler: s4_log.txt | 15 yılın 11'i artı; en iyi 10 gün hariç +8,3; kaydırma p 0,020 / 0,007; açılış girişi +9,2 / +11,8 | yüksek
K1 zayıflık: en likit üçte birlik | CSV: W3B_sade_sakin_guclu_h1\|lik_yuksek | −3,0 / +3,8 | yüksek
K1 komşuları (18 hücre) | CSV: sade_V25/V33/V50 × R33/R50/Rpoz/Rpoz1/RXpoz/RXpoz1 | IS +3,6…+12,3; OOS-1 +3,5…+18,4; hepsi artı | yüksek
K2 sonuç | CSV: W3B_lgbm_tahmin20_temiz_h1 | IS 1.118 gün +23,0 (t 3,79) net −9,4 (düşük +5,6); OOS-1 507 gün +24,7 (t 3,17) net −8,0 (düşük +7,0) | yüksek
K2 sağlamlık | günlükler: s4_log.txt | 14 yılın 11'i artı; en iyi 10 gün hariç +16,8; kaydırma p 0,007 / 0,003; açılış girişi +18,0 / +15,9 | yüksek
K2 komşu eşikler (10 / 30 bps, temiz) | CSV: lgbm_tahmin>10bps_ve_TEMIZ4, >30bps_ | IS +12,1 / +28,2; OOS-1 +19,3 / +27,1 | yüksek
İki kural aynı hisseyi işaretlerse (dondurulmadı) | CSV: iki_kural_birlikte | IS +34,0 (t 3,19); OOS-1 +38,8 (t 3,14); net −3,4 / +1,1 | orta
Öz-denetim ve yeniden üretim | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3b_damitma/rules.py; günlükler: s4_log.txt | self_check_causal 0,0 (kesim 2018-09-14, 2021-06-30, 2024-06-28); build 9,1 sn; run.sh 99 sn, CSV md5 aynı | yüksek

Teslim dosyaları:
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3b_damitma/rules.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/w3b_damitma_sonuc.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/w3b_damitma.md (700 kelime)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3b_damitma/run.sh (common.py, s1_tani.py, s2_tarama.py, s3_aday.py, s4_son.py; kullanım: `bash run.sh <panel_dev>`)

**açık kalanlar**
- Kasa gün sayısı (352) hesapla bulundu: VERI_NOTU_D1'deki 4.238 gün eksi panel_dev'in 3.886 günü. panel_full açılmadı. Olay sayıları (K1 ~350 gün / ~1.600 işlem; K2 ~290 gün / ~1.100 işlem) OOS-1 sıklığından tahmindir.
- K2, `kod/a8_model/rules.py` dosyasına (LightGBM) bağımlı; o dosya değişirse K2 de değişir. İnsan eliyle uygulanamaz; TradingView'de yalnız K1 ve kaçınma listesi uygulanabilir.
- K1'de TradingView'in "Oynaklık (ay)" sütunu 20 günlük standart sapmanın vekilidir; ikisinin sıralama uyumu sınanmadı.
- İki kuralda da `birincil: True` yazdım. Kasadaki Holm ailesine nasıl gireceklerine ana ajan karar vermeli.
- Kaçınma listesi AL kuralı olmadığı için dondurulmadı (görev sınırı: 2 kural, beklenen işaret +1). W3-A ile örtüşüyor olabilir.
- 2019'a kadar evren ~10 hisse (beşte birlik 2 hisse) ve hayatta kalma yanlılığı var; IS rakamları buna göre okunmalı.
- VBTS tedbirli hisselerde 1 günlük çıkış yapılamayabilir; veri yok.