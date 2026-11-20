araç: 33/40

**ÖZET (A8 birleşik model, yalnız IS; ileriye dönük tahminler 2012-01 → 2022-12)**

Sonuç: **birincil kural dondurulmadı**; 4 ikincil kural donduruldu. Birleşik modelin sıralama gücü istatistiksel olarak gerçek ama küçük, kazanç “kaçınma” (alt uç) tarafında ve spotta işlenebilir değil.

- Tarama: önceden yazılı ızgara, 138 değerlendirme satırı (60'ı aday türü: 30 kesit üst dilim + 24 zamanlama + 6 tek hisse), 4 kaydırma testi. Hepsi elib.evaluate ile.
- Kesit IC: ridge 0,030 (t 4,3), LightGBM(d3, yaprak 500) 0,043 (t 6,2), 11 yılın 10'unda pozitif. Beklentinin tersine kaynak kısa vadeli dönüş DEĞİL: yalnız rel1 IC −0,004, dönüş grubu 0,003; dönüş dışı grup (hacim şoku, 20g oynaklık, tavan/taban, likidite) 0,042.
- En üst beşte birlik AL: +3,8 bps (t 1,09), maliyet 42,6 → net −37,6. En alt beşte birlik −10,8 bps (t −2,7). Üst dilim sonucu kırılgan: girdiler 1 bps'e yuvarlanınca 6,6 → 3,8 bps (IC aynı kaldı); kaydırma p = 0,26.
- Zamanlama: 24 satırın 23'ü brüt pozitif; en iyisi ridge(lam=1) h2 eşik 25 bps: 40,3 bps (t 2,77), başabaş 43,05 − maliyet 43,04 = net +0,01. Komşu parametreler brüt 10–32 bps, hepsi net eksi; bu yüzden bilinçli olarak ikincil bırakıldı.
- BH (q = 0,10): 4 satır brüt etkide geçiyor, hiçbiri maliyeti anlamlı aşmıyor.
- Öz-denetim: self_check_causal iki kesim tarihinde dört kural için 0,0; iki build aynı; build 6 sn (IS).

**Bilmen gerekenler**
1. `elib.py` çalışmam sırasında iki kez değişti (top10 tanımı + vadeli adım maliyeti; sonra tarihli fiyat adımı). Bütün satırlar son sürümle (md5 78ef520d…, 21:35:01) yeniden üretildi; son değişiklik maliyeti en çok 0,06 bps oynattı ve zamanlama kuralının netini −0,01'den +0,01'e çevirdi.
2. KÜTÜPHANE HATASI bulmadım.
3. SAPMA: BIG sepeti elib.BIG yerine adv60'a göre ilk 5 (isim gömmemek için); “kendi tavan bayrağı” yerine “dün tavan” + “bugün tavana dokundu” (dolabilir satırlarda tavan bayrağı hep 0); tavan sayısı oran olarak.
4. Keşif kuralı (ızgara dışı, VİOP) yalnız ikincil; vadeli fiyatlarıyla net eksi.
5. Hiçbir şey commit etmedim. panel_is dışında veri açmadım.

**İDDİA DEFTERİ** (iddia | dosya yolu | sayı | güven)
toplam değerlendirme satırı | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a8_model_sonuc.csv | 138 (+1 vadeli satırı = 139 satır); aday türü 60 | yüksek
dondurulan kural | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a8_model/rules.py | 0 birincil, 4 ikincil | yüksek
self_check_causal (kesim 2021-06-30 ve 2018-09-14) | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a8_model/out/final_ozet.txt | dört kural 0,0; deterministik True | yüksek
build süresi (IS paneli) | aynı dosya | 6 sn | yüksek
ridge(lam=1) kesit IC h1 | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a8_model/out/scan_log.txt | 0,0305; t 4,29; yarılar 0,022 / 0,052 | yüksek
LightGBM(d3,m500) kesit IC h1 | aynı | 0,0433; t 6,15; yarılar 0,037 / 0,059; 10/11 yıl pozitif | yüksek
yalnız rel1 modeli IC h1 | aynı | −0,0041 (t −0,56) | yüksek
dönüş grubu / dönüş dışı grup IC h1 (ridge) | aynı | 0,0027 (t 0,37) / 0,0419 (t 5,91) | yüksek
modelsiz rel1 dönüşü IC yarılar | aynı | 0,035 / −0,005 | yüksek
A8_kesit_lgbm_d3_m500_h1_ust20 | a8_model_sonuc.csv | 2.763 gün; +3,78 bps; t 1,09; maliyet 42,59; net −37,60 | yüksek
aynı kural, en alt beşte birlik | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a8_model/out/diag_log.txt | −10,8 bps; t −2,7; yarılar −8,2 / −17,7 | yüksek
dönüş dışı ridge, en alt beşte birlik h1 | aynı | −18,5 bps; t −4,1 | yüksek
kesit üst dilim aralığı (30 ızgara satırı) | a8_model_sonuc.csv | −14,4 … +9,0 bps; hepsi net eksi | yüksek
LightGBM üst dilim kırılganlığı (5 → 4 ondalık yuvarlama) | ilk koşu günlüğü (dosyada yok) | h1 6,6 → 3,8; h3 15,2 → 6,8 bps | orta
kaydırma sıfırı, LightGBM h1 üst dilim | scan_log.txt | p = 0,259 | yüksek
sahte etki, LightGBM h1: en likit 15 / fiyat ≥ 5 TL / üçte birlik | scan_log.txt | 4,6 (t 1,28) / 7,3 (731 gün, t 0,72) / 5,5 (t 2,15) bps | yüksek
LightGBM h1 üst dilim: gece payı ve t+1 kapanış girişi | scan_log.txt | 0,7 bps gece; 5,0 bps | orta
A8_zaman_ridge_l1_h2_e25 | a8_model_sonuc.csv | 402 gün (293 bağımsız); 40,25 bps; t 2,77; başabaş 43,05; maliyet 43,04; net +0,01 | yüksek
aynı kural sağlamlık | final_ozet.txt | yarılar 50,7 / 25,1; top10 hariç 23,0; t+1 girişi 24,9; 9/11 yıl pozitif; 2021: −110 | yüksek
A8_zaman_ridge_l1_h3_e0 | a8_model_sonuc.csv | 1.445 gün (626 bağımsız); 24,83 bps; t 2,34; net −14,25 | yüksek
zamanlama komşuları (h2 e0, h1 e25, h3 e25, lam=10, lasso, lgbm) | scan_log.txt | brüt 10–32 bps; hepsi net eksi; lam=10 IC ≈ 0 | yüksek
zamanlama kıyası: yalnız sektör r(t) | scan_log.txt | 4,2 / 6,3 / 6,4 bps; t ≤ 1,05 | yüksek
zamanlama katsayıları | diag_log.txt | sektör medyan hacim şoku yeniden eğitimlerin %99–100'ünde pozitif | yüksek
BH (q = 0,10; 60 aday satır) | final_ozet.txt | 4 satır geçiyor (lgbm_d2_m200_h1, zaman ridge h1_e0, h2_e25, lasso h2_e0) | yüksek
tek hisse VİOP AL (eşik 25, ızgara) | scan_log.txt | 121 gün; 33,9 bps; t 1,60; %85 ENJSA; eşik 50'de −32,5 | yüksek
keşif kuralı (3 hisse üst dilim, VİOP AL) | a8_model_sonuc.csv | 373 gün; 28,4 bps; t 1,98; net +4,85; vadeli fiyatlarıyla 23,8 bps, t 1,53, net −8,67 | orta
ortalama temel maliyet (bütün satırlar) | a8_model_sonuc.csv | 41,2 bps (18,0–46,9) | yüksek
not dosyası | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a8_model.md | wc ile 605 (başlık imleri dahil) | yüksek
baştan sona çalıştırma | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a8_model/run.sh | ~4 dakika | yüksek

## açık kalanlar
- **Karar sende:** `A8_zaman_ridge_l1_h2_e25` net +0,01 bps ile kâğıt üstünde (i)'yi geçiyor; komşuları geçmediği için ikincil bıraktım. Birincile almak istersen `rules.py` içindeki FROZEN listesinde o satırın `'birincil'` alanını True yapman yeter.
- **panel_dev denetimi:** kör protokol gereği panel_dev ile karşılaştıramadım. Paneller arası <1e-6 getiri farkına karşı girdileri 1 bps'e yuvarladım; yine de LightGBM kurallarında (kural 1 ve 4) çok küçük, sıfır olmayan bir fark çıkarsa bu sayısal kaynaklıdır, ileriye bakma değil. Ridge kurallarında fark beklemiyorum.
- build süresi daha uzun/çok hisseli panelde ölçülmedi (IS'te 6 sn; 5 dakikanın çok altında kalması beklenir).
- Hiperparametreler tam IS yürüyen IC'siyle seçildi; ayrı bir doğrulama dilimi yok.
- 2019'a kadar ~10 hisse olduğundan beşte birlik 2 hisseydi; 2023+ evreninde (40+ hisse) davranış farklı olabilir.
- Alt uçtaki −11 … −19 bps'lik kaçınma etkisi spotta kullanılamıyor; üç VİOP hissesinde SAT sürümü IS'te ~0 bps (keşif satırları CSV'de).