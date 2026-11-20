araç: 21/40

## Özet

**Birincil kural dondurulmadı.** Ana ızgaranın 108 satırından hiçbiri seçim ölçütlerini karşılamadı; BH (q = 0,10) geçen yok, en büyük t = 1,93. Bilgi amaçlı 5 ikincil kural donduruldu. `self_check_causal` beş kural için 0,0; `build()` 0,1 s ve deterministik; `run.sh` baştan sona çalıştı (yaklaşık 100 s). Yalnız `panel_is` kullanıldı.

**Test sayısı: 294 istatistik.** 108 ana ızgara satırı, 33 regresyon (21 Fama–MacBeth, 12 zaman serisi), 108 kontrol tekrarı (ham fiyat ≥ 5 TL; en likit 15), 45 ek satır (taban ayrıştırması, VİOP kısa yön, ızgara dışı keşif).

**Bulgular (IS):**
- **Yetişme yok, beklenti doğrulanmadı.** rel1 katsayısı +0,008 (t = 0,65); 2020–22'de +0,046 (t = 2,0), yani geri dönüş değil devam. En geride kalan beşte birlik ertesi gün sektörün 18 bps altında (t = −3,07). Bunun tamamı tabanda kapananlardan geliyor: 186 işlem, −434 bps. Taban hariç −4,7 bps (t = −0,86).
- Öne geçen de geri dönmüyor: rel1 üst beşte birlik −3 bps.
- **Büyük → küçük gecikmesi görülmedi.** R_big(t) katsayısı 0,036 (t = 1,1); 2020–22'de 0,029 (t = 0,5). Büyükler z ≤ −1 düşünce küçükler ertesi gün −41 bps (own, t = −2,7): alım değil, kaçınma bilgisi.
- **Yüksek → düşük hacim:** regresyonda h = 2–3 için t = 2,2–2,5. Eşikli kuralda yalnız own ölçüsünde artı (z ≥ 1,5, h = 3: +48 bps, t = 1,89, net +18). Karar ölçüsü sec'te net −18. Ham fiyatı ≥ 5 TL hisselerde +4,6 bps'ye düşüyor.
- Maliyet (~40 bps) sonrası artıda kalan 7/90 satırın hiçbirinde |t| ≥ 2 yok.

**İkincil kurallar:** `A3_rel5_ust5_h3` (sec), `A3_vhi_z15_vlo_h3` (own), `A3_big_z10_small_h3` (own), `A3_rel1_alt5_viop_al_h1` (keşif, VİOP), `A3_rel1_alt5_h1_RED`.

**Dikkat:** `A3_rel1_alt5_h1_RED` alım kuralı değildir. “Geride kalanı al” hipotezinin doğrudan sınamasıdır ve beklenen işareti NEGATİFTİR; ortak betiğin tek yönlü testi bu satırda ters okunmalı.

**KÜTÜPHANE NOTU (hata değil, yorum farkı):** `elib.evaluate` içindeki `top10_haric_bps` en iyi max(10, %5) günü çıkarıyor. Binlerce sinyal günü olan kesit kurallarında 100'den fazla gün atılıyor ve sonuç mekanik olarak negatif (örnek: +23,1 → −62,7). Kendi hesabım `top10gun_haric_bps` sütununda (yalnız en iyi 10 gün). Kütüphaneden bağımsız sağlamam aynı işareti verdi (−12,5 bps; fark, taban kilidinde çıkışın kaydırılmasından).

**SAPMA:** VİOP satırları ve `K_` önekli satırlar ızgara dışıdır, “keşif” etiketlidir. İstenen dosyalara ek olarak regresyon tablosu ve tanılama günlüğü yazıldı.

**Dosyalar:**
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a3_kesit/rules.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a3_kesit/run.sh (scan.py, scan2.py, finalize.py)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a3_kesit_sonuc.csv (261 satır)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a3_kesit.md (591 kelime)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a3_kesit_regresyon.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a3_kesit_tanilama.txt

## İddia defteri

Yollar `/home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/` altındadır.

iddia | dosya yolu | sayı | güven
---|---|---|---
Birincil kural yok; 5 ikincil | a3_kesit_tanilama.txt | birincil: 0, ikincil: 5 | yüksek
Ana ızgarada BH geçen yok | a3_kesit_tanilama.txt | 0/108; en büyük t 1,93, en küçük −3,07 | yüksek
Nedensellik öz-denetimi temiz | a3_kesit_tanilama.txt | 5 kural için 0,0 (kesim 2021-06-30) | yüksek
rel1 FM katsayısı, h=1 | a3_kesit_regresyon.csv | +0,0084, t 0,65, 2.370 gün | yüksek
rel1 FM yarılar | a3_kesit_regresyon.csv | ≤2019 −0,0088 (t −0,57); 2020–22 +0,0458 (t 2,01) | yüksek
Taban kapanışı FM, h=1 | a3_kesit_regresyon.csv | −0,0029, t −4,13; 2020–22 −0,0082 | yüksek
T2_rel1_alt5_h1 (geride kalan AL) | a3_kesit_sonuc.csv | −18,4 bps, t −3,07, net −65,6; yarılar −7,9 / −41,0 | yüksek
Aynı satır, yalnız tabanda kapananlar | a3_kesit_sonuc.csv | 186 işlem, −434,4 bps, t −4,24 | yüksek
Aynı satır, taban hariç | a3_kesit_sonuc.csv | −4,7 bps, t −0,86 | yüksek
Bağımsız sağlama (kütüphanesiz) | a3_kesit_tanilama.txt | −12,5 bps, 2.376 gün | yüksek
T2_rel1_ust5_h1 (öne geçen) | a3_kesit_sonuc.csv | −3,1 bps, t −0,49 | yüksek
T2_rel5_ust5_h3 (ikincil) | a3_kesit_sonuc.csv | +23,1 bps, t 1,52, net −20,0; yarılar +12,3 / +47,3; t+1 giriş +33,2 | yüksek
T2_rel5_ust5_h3 kaydırma testi | a3_kesit_tanilama.txt | p 0,047 | orta
T3 R_big → küçük, h=1 | a3_kesit_regresyon.csv | 0,036, t 1,12; 2020–22 0,029, t 0,51 | yüksek
T3_big_z10_yukari_small_h3_own (ikincil) | a3_kesit_sonuc.csv | +47,0 bps, t 1,60, net +21,4; yarılar +81,3 / +5,1; en iyi 10 gün hariç −7,9 | yüksek
Aynı kural sec ölçüsüyle | a3_kesit_sonuc.csv | −5,9 bps, t −0,26 | yüksek
T3_big_z10_asagi_small_h1_own | a3_kesit_sonuc.csv | −41,3 bps, t −2,74; yarılar −28,0 / −71,8 | yüksek
T4 R_vhi → düşük hacim, h=2 / h=3 | a3_kesit_regresyon.csv | 0,075 (t 2,24) / 0,109 (t 2,48) | yüksek
T4_vhi_z15_yukari_vlo_h3_own (ikincil) | a3_kesit_sonuc.csv | +48,4 bps, t 1,89, net +18,2; yarılar +81,6 / +15,7; t+1 giriş +35,9 | yüksek
Aynı kural sec ölçüsüyle | a3_kesit_sonuc.csv | +20,5 bps, t 1,20, net −18,2 | yüksek
Aynı kural, ham fiyat ≥ 5 TL | a3_kesit_sonuc.csv | own +4,6 bps, t 0,2 | yüksek
Aynı kural, en likit 15 | a3_kesit_sonuc.csv | own +62,5 bps, t 2,3, net +31,0 | yüksek
Aynı kural, 2021 yılı | a3_kesit_sonuc.csv | −124 bps | yüksek
K_rel1_alt5_viop_al_h1 (ikincil, keşif) | a3_kesit_sonuc.csv | 198 gün, sec +23,7 (t 1,28), net −0,2; own +46,6 (t 2,43); ENJSA payı 0,55; t+1 giriş −1,3 | orta
Aynı kural vadeli fiyatıyla | a3_kesit_sonuc.csv | 155 gün, +29,9 bps, t 1,40 | orta
Alt beşte birlik ∩ büyük üçte birlik (keşif) | a3_kesit_sonuc.csv | −20,1 bps, t −1,83 | yüksek
Maliyet sonrası artıda kalan ana ızgara satırı | a3_kesit_sonuc.csv | 7/90; hiçbirinde abs(t) ≥ 2 yok | yüksek
Temel maliyet (IS ortalaması) | a3_kesit_sonuc.csv | satıra göre 37–45 bps; ≥ 5 TL süzgecinde ~30 | yüksek
Kütüphanenin top10_haric_bps tanımı | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/ortak/elib.py (satır 360) | k = max(10, ceil(0,05·gün)) | yüksek

## açık kalanlar

- `build(panel_is)` ile `build(panel_dev)` karşılaştırması kör protokol gereği yapılmadı. Kesik panel öz-denetimi 0,0 verdi. Beklenen tek risk, dev panelinde getirilerin 1e-6 düzeyindeki farkının sıralama eşitliklerini oynatması.
- Sıralama günde en az 8 işlem görebilir üye istediği için sonuçlar fiilen 2013 sonrasını kapsıyor. 2019'a kadar bir beşte birlik 2 hisse. 40'tan fazla hisseli 2023+ döneminde sepetler 8 hisseye çıkar; IS bunu temsil etmiyor.
- T4'teki etkinin 5 TL altı hisselere bağlı olması 2023+ için olumsuz işaret. O dönemde ham fiyatların dağılımına bakmadım.
- Tabanda kapanan hissenin ertesi gün düşmeye devam etmesi (−434 bps) bu ailenin en güçlü sayısı ama A4 (olay) ailesinin konusu. Kural olarak dondurmadım; A4 ile çakışma kontrolü ana ajanda.
- `A3_rel1_alt5_h1_RED` için ortak OOS betiğinin tek yönlü p-değeri ters yönde okunmalı.
- VİOP keşif kuralı 198 güne ve %55 ENJSA'ya dayanıyor; AKSEN vadelisi IS'te yalnız 2022-11'den beri var.