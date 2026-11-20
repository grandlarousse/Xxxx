araç: 29/40

## Özet (A1 — hisse → hisse ikili öncülük, yalnız IS 2010-01-04 → 2022-12-30)

**BİRİNCİL KURAL DONDURULMADI.** 102 satırlık kural ızgarasında birincil ölçütlerin (i)–(v) tamamını karşılayan satır yok. 4 İKİNCİL (izleme) kuralı donduruldu; hepsi `olcu='sec'`, spot, long.

- **T1 doğrusal:** 420 sıralı çift (27 hisse; ASTOR, EUPWR, ENERY IS'te yok; AHGAZ 0, ALFAS 13 işlem günü). |t| ≥ 2 oranı %5,7; sektör kontrolsüz %9,8 (fark sektör geneli otokorelasyon). BH geçen: h=1'de 0, h=2 ve h=3'te 1'er (AYEN → ZOREN). Ailenin en büyük |t|'si için dairesel kaydırma p = 0,39 / 0,09 / 0,09 (200 tekrar, 420 çiftin tamamı).
- **T2 olay:** 3.948 test; BH geçen 10 testin 10'u negatif (AL yönünde kullanılamaz); kaydırma p = 0,86 / 0,12 / 0,11.
- **Kalıcılık:** çiftin iki yarısında, ilk yarıda anlamlı 26 bağın %54'ü aynı işarette, hiçbiri yeniden anlamlı değil. Takvim bölmesinde (100 çift) 6 bağın %83'ü aynı işarette, yine 0 yeniden anlamlı. Lider skoru sıra korelasyonu 0,19 (takvim) / −0,18 (çift bölmesi).
- **Önceden yazılı hipotezler:** NATEN–ESEN–MAGEN ve ODAS–CANTE'de |t| ≥ 2,5 yok. Büyükler → diğerleri havuz t = −0,29. Çift farkı dönüşü |t| ≤ 1,8, işaretler tutarsız. AHGAZ–ENERY, güneş kümesi, ASTOR sınanamadı.
- **Bayat fiyat:** bağlar düşük likiditeli hedeflerde değil (ortalama t 0,03; yüksek likiditede 0,44); anlamlı bağlarda katsayının medyan %10'u gece.
- **Lider ağı kuralı:** 36 satırın 36'sında brüt pozitif (0,9–45,7 bps) ama maliyet ~42 bps; net yalnız 2 satırda > 0 ve komşuları negatif. En iyi satır t = 3,08, kaydırma p = 0,002; net +1 bps (≥ +15 bps şartının çok altında). Öz momentum değil (kontrol: öz z ≥ 1,5 → −7 bps).
- **Grup çifti olay kuralı:** "kardeş ≤ −%3 → AL" t ≈ 2,1 görünüyordu; kaydırma p ≈ 0,2 ve en iyi 10 gün çıkınca ≈ 0 → elendi.

**Test sayısı:** gerçek veri üzerinde ≈ 16.700 (T1 1.259 + sektörsüz 1.259 + yarı 4.077 + gece/gün içi 838 + T2 3.948 + T2 yarı 5.151 + çift farkı 48 + havuz 3 + ızgara 102 + aday denetimi 38); ayrıca 1.041.400 sıfır dağılımı hesabı.

**Öz-denetim:** `elib.self_check_causal(build, P)` 4 kural için 0,0 (kesim 2021-06-30 ve 2018-06-29); ızgaradaki 102 kural için de 0. `build` 0,3 sn, deterministik. `run.sh` baştan sona 2 dk 12 sn.

**KÜTÜPHANE NOTU (hata değil, tasarım):** `top10_haric_bps` en iyi max(10, %5) günü çıkarıyor; 562 günlük kuralda 29 gün düşüyor ve (iii) ölçütü brüt ~30 bps altındaki her kural için mekanik olarak başarısız. Kendi hesabım (tam 10 gün) `en_iyi_10_gun_haric_bps` sütununda. `gece_payi` karar ölçüsüyle değil 'own' ile hesaplanıyor; payda sıfıra yakınken anlamsız değer veriyor (ör. 204,98).

**Protokol:** yalnız `panel_is` kullanıldı; veri indirilmedi. `xelkt_uyeler.csv` ilk bakışta bütün sütunlarıyla ekrana basıldı; hesapta yalnız `ana_faaliyet` kullanıldı.

## İddia defteri
iddia | dosya yolu | sayı | güven
T1 çift sayısı ve regresyon | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a1_ikili/out/scan_log.txt | 420 çift; 1.259 regresyon | yüksek
T1 \|t\|≥2 oranı h=1, sektör kontrollü / kontrolsüz | aynı | %5,7 / %9,8 | yüksek
T1 BH geçen (h=1/2/3) | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a1_ikili/out/t1_cift.csv | 0 / 1 / 1 (AYEN→ZOREN t=3,84; 3,79) | yüksek
T1 max\|t\| kaydırma p (h=1/2/3) | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a1_ikili/out/scan_ozet.json | 0,39 / 0,09 / 0,09 (gerçek 3,29 / 3,84 / 3,79; sıfır medyan ≈3,2) | yüksek
T2 test sayısı, BH geçen | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a1_ikili/out/t2_olay.csv | 3.948; 10 geçen, 10'u negatif | yüksek
T2 max\|t\| kaydırma p | scan_ozet.json (yukarıdaki) | 0,86 / 0,12 / 0,11 | yüksek
Kalıcılık, çift kronolojik bölme h=1 | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a1_ikili/out/kalicilik.csv | 26 anlamlı; %53,8 aynı işaret; 0 yeniden anlamlı; çift t sıra kor. 0,006 | yüksek
Kalıcılık, takvim bölmesi h=1 | aynı | 100 çift; 6 anlamlı; %83 aynı işaret; lider skoru kor. 0,19; izleyici 0,64 | orta (n=11)
Önceden yazılı çiftlerde en büyük \|t\| | scan_log.txt | NATEN→ESEN −2,06 (h=1); eşik 2,5 aşılmadı | yüksek
Büyükler → diğerleri havuz regresyonu h=1 | scan_log.txt | t = −0,29; küçük sepet öz otokorelasyon t = 3,88 | yüksek
Çift farkı dönüşü | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a1_ikili/out/cift_farki.csv | 24 regresyon; \|t\| ≤ 1,80 | yüksek
Küme içi / arası \|t\|≥2 oranı h=1 | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a1_ikili/out/kume.csv | %9,6 (146 çift) / %3,8 (234 çift); BH 0 | yüksek
Bayat fiyat: hedef likiditesine göre ort. t | scan_log.txt | düşük 0,03; orta 0,30; yüksek 0,44 | yüksek
Anlamlı bağlarda gece payı | scan_log.txt | medyan 0,10 (24 bağ); \|t_gunici\|≥2 %62, \|t_gece\|≥2 %8 | yüksek
Izgara satırı / ölçüt i–v tamam | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a1_ikili_sonuc.csv | 102 / 0 | yüksek
Seçim dağılımı | aynı | birincil 0; ikincil 4; elendi 98 | yüksek
Lider ağı: brüt pozitif satır, net pozitif satır | aynı | 36/36; 2/36; brüt 0,9–45,7 bps; ort. t 1,53 | yüksek
A1_LN_W250_c2.0_th1.5_h1 IS | aynı | 562 gün, 777 işlem; +33,6 bps; t=3,06; brüt 30,0; maliyet 41,8; net −11,8; yarılar +30,9/+38,5 | yüksek
A1_LN_W250_c2.0_th1.5_h2 IS | aynı | +54,0 bps; t=3,08; brüt 42,8; net +1,0; yarılar +76,8/+12,9 | yüksek
A1_LN_W500_c1.5_th1.5_h2 IS | aynı | 925 gün; +30,0 bps; t=2,45; net −12,7; yarılar +42,7/+1,7 | yüksek
A1_FL_th2.0_h1 IS (IS seçimli) | aynı | 211 gün; +33,6 bps; t=2,31; net −13,3; ZOREN payı %57 | orta (seçim yanlı)
Kaydırma p (aday kurallar, 500 tekrar) | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a1_ikili/out/aday_denetim.csv | LN W250 h1 0,002; h2 0,002; W500 h2 0,014; FL 0,020; GP aşağı h2/h3 0,22/0,21 | yüksek
En iyi 10 gün hariç (kendi hesabım) / kütüphane ölçüsü, LN W250 h1 | aynı | +17,4 / −3,5 bps | yüksek
LN W250 h1 likidite üçte birlikleri | aynı | düşük +44,6; orta +11,5; yüksek +34,8 bps (t=2,34) | yüksek
LN W250 h1 yeni listelenenler | aynı | 55 işlem, −0,5 bps (eski: 722 işlem, +32,3) | orta
Düşük maliyet senaryosunda net | a1_ikili_sonuc.csv | +3,2 / +16,0 / +2,3 / +1,7 bps (4 ikincil) | yüksek
Öz-denetim | /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a1_ikili/out/grid_log.txt | 4 kural 0,0; ızgara 102 kuralda 0 hatalı; build 0,3 sn | yüksek
Toplam test | scan_ozet.json + ızgara + denetim | ≈16.700 gerçek veri testi; 1.041.400 sıfır dağılımı hesabı | yüksek

Teslim dosyaları:
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a1_ikili/rules.py (build; FROZEN listesi, 4 ikincil)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a1_ikili_sonuc.csv (102 satır; secim, not, aday_mi, en_iyi_10_gun_haric_bps, yarı sütunları)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a1_ikili.md
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a1_ikili/run.sh (scan.py → grid.py → check.py; `bash run.sh <panel_is>`), notlar.json, out/

## açık kalanlar
- AHGAZ–ENERY, SMRTG–ALFAS–EUPWR ve ASTOR → güneş/ekipman hipotezleri IS'te sınanamadı (hisseler yok ya da < 250 gün). `gp_signal`/`ps_signal` üreticileri bu çiftleri kapsıyor ama IS kanıtı olmadığı için dondurulmadı; 2023+ için yalnız "keşif" olarak bakılabilir.
- Lider ağı 2023+ evreninde (40+ hisse) sınanmadı; IS'te yeni listelenenlerde yalnız 55 işlem var. Yeni hisse sinyale listelenmeden yaklaşık 6 ay sonra girer (≥ 120 gözlem şartı).
- Kural ızgarasının tamamı için aile düzeyi sıfır dağılımı yapılmadı; kaydırma p'leri tek kural içindir (36 lider ağı satırı için Bonferroni ile 0,002 → ≈ 0,07).
- panel_dev ile IS tarihlerinde birebir aynılık denenmedi (kör protokol); düzeltme çarpanı farkı (< 1e-6 getiri) eşik sınırındaki tekil sinyalleri değiştirebilir.
- `top10_haric_bps` tanımı (max(10, %5)) bütün aileleri etkiler; ana ajanın ortak ölçüyü buna göre yorumlaması gerekir.