araç: 21/40

## Özet (A2 — endeks ↔ hisse, yalnız IS 2010 → 2022-12-30)

Önceden yazılı ızgaranın tamamı tarandı: 1.812 kural satırı (1.560'ı ≥ 30 olay günü), 29 keşif satırı, yaklaşık 700 regresyon. BH (q=0,10) geçen 10 satırın 9'u aşağı yönlü; AL yönünde yalnız 1 satır geçti.

**Beklentilerin ikisi de tutmadı.**
- XU030 → sektör ertesi gün gecikmesi yok: havuz katsayısı −0,05 (t=−1,6), sığ hisselerde −0,08. XU030 z ≥ 1,5 sonrası +4,5 bps.
- “Geciken yetişir” kuralı çalışmıyor: sert yükseliş günü hareket etmeyen hisse ertesi gün +10 bps (t=0,9), net −22 bps. Gecikenler akranlarını da geçmiyor.

**Bulunan etki sektörün kendi momentumu.** Sektör yükseldiği günün ardından 2–3 gün devam ediyor. Etki yalnız yukarı yönde, ertesi günün gün içi bölümünde ve en likit 10 hissede de var; bayat fiyat değil.

**Aşağı yön daha güçlü ama spotta işlenemez.** Sektör sert düştüğü gün düşmeyen hisse ertesi gün −66 bps (t=−3,6). Pratik anlamı: düşüş günü direnen hisse alınmaz.

**Dondurulan kurallar: 1 birincil, 6 ikincil.** Ölçütlerin tamamını karşılayan ve çoklu testten sonra ayakta kalan tek kural birincil yapıldı; zorlama yapılmadı.
- Birincil `A2_xelkt_z1_tum_h3`: z(XELKT) ≥ 1 → dolabilir bütün sektör hisseleri AL, 3 gün. Net +25 bps/işlem; muhafazakâr maliyette sıfır. 2020 ve 2021'de negatif.
- İkinciller: gecikenler alt kümesi (h=3), SPEC z ≥ 2 (h=3), XELKT z ≥ 1 ve XU100 z < 1 (keşif), KOMSU z ≥ 1,5 (h=2), KOMSU z ≥ 2 → AKSEN (h=1), sektör düşerken geciken VİOP'lu hissede vadeli SAT (keşif).

**Öz-denetim.** `self_check_causal` dört kesim tarihinde yedi kuralın hepsi için 0,0; `build` 0,1 s, deterministik. `run.sh` baştan sona iki kez çalıştırıldı.

**Dikkat: `elib.py` çalışmam sırasında iki kez değişti** (top10 tanımı; vadeli maliyetine fiyat adımı). Bütün tablolar son sürümle (md5 480053d3…) yeniden üretildi. Kütüphane yeniden değişirse `top10_haric_bps` ve vadeli net sütunları eskir.

**KÜTÜPHANE HATASI (küçük):** `elib.TICK_TABLE` 2023-11 sonrası adım tablosunu bütün tarihe uyguluyor. IS'te ham kapanışı ≥ 250 TL olan 296 hisse-günde yarım adım en çok ~3 bps fazla sayılıyor. Kendi tahminim: kurallarımın ortalama maliyetine etkisi 0,1 bps'nin altında; sonuç değişmiyor.

**SAPMA:**
- T4 koşulları yalnız |z| ≥ 1,5 ve hedef (a)/(b) için tarandı.
- Sepet kurallarına “o gün ≥ 5 dolabilir hisse” filtresi sinyale gömüldü.
- `regresyon.csv`'deki XU030 satırları XU100 kontrolüyle eşdoğrusal (katsayı −0,4…−1,2); doğru okuma `T1_havuz_XU100kontrolsuz` satırlarıdır.
- CSV'de `blok=DONDURULMUS` satırları, seçilen ızgara satırlarının `rules.py` üzerinden yeniden üretimidir (aynı kural iki kez görünür).

Dosyalar:
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a2_endeks/rules.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a2_endeks_sonuc.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a2_endeks.md
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a2_endeks_regresyon.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a2_endeks/ (run.sh, scan.py, checks.py, secim.py, a2lib.py, out/)

## İddia defteri

Kısaltmalar: SONUC = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a2_endeks_sonuc.csv; REG = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a2_endeks_regresyon.csv; OUT = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a2_endeks/out

iddia | dosya yolu | sayı | güven
---|---|---|---
Izgara test sayısı | SONUC | 1.812 satır; 1.560'ı ≥ 30 olay günü; 29 keşif | yüksek
Regresyon sayısı | REG | 302 satır; hisse bazındakilerle ~700 regresyon | yüksek
BH (q=0,10) geçen | SONUC (`bh_gecti`) | 10 satır; AL yönünde pozitif 1 | yüksek
(i)–(v) ölçütlerini geçen AL satırı (n ≥ 100) | SONUC | 81; t ≥ 2 olan 52 | yüksek
Birincil: z(XELKT) ≥ 1 → tümü, h=3 | SONUC (`A2_xelkt_z1_tum_h3`) | 443 gün, 330 bağımsız, 4.389 işlem; +57,0 bps; t=3,44 | yüksek
Birincil net | SONUC | işlem başına +66,2; maliyet 41,0; net temel +25,2; muhafazakâr +0,2 | yüksek
Birincil iki yarı | SONUC (`y1_*`, `y2_*`) | ≤2019 +75,3 (t=4,9); 2020–22 +17,8 (t=0,44) | yüksek
Birincil sağlamlık | SONUC | en iyi 10 gün hariç +38,4; t+1 kapanış girişi +23,0; gece payı 0,49; en yoğun hisse 0,10 | yüksek
Birincil yıllar | SONUC (`yillar_bps`) | 13 yılın 9'u pozitif; 2020 −16; 2021 −73; 2022 +105 | yüksek
Birincil komşular | SONUC | z ≥ 1,5: +51,1 (t=2,2); z ≥ 2: +23,5 (t=0,8); h=2: +39,2 (t=3,1); EWx: +40,8 (t=1,9) | yüksek
Birincil yer değiştirme testi | OUT/checks.txt | p=0,002; 126 AL kuralı için aile düzeltmeli p=0,010 | orta (200 kaydırma; tam ızgara değil)
İkincil: gecikenler h=3 | SONUC (`A2_xelkt_z1_geciken_h3`) | 432 gün; +64,0; t=3,27; net +34,9; yarılar +84,7 / +20,9 | yüksek
İkincil: SPEC z ≥ 2 h=3 | SONUC (`A2_spec_z2_tum_h3`) | 114 gün; +61,1; t=2,10; net +61,5; en iyi 10 gün hariç +4,9 | yüksek
İkincil keşif: XELKT ≥ 1 ve XU100 < 1, h=3 | SONUC (`A2_xelkt_z1_xu100alt_tum_h3`) | 247 gün; +62,8; t=2,95; net +41,8; yarılar +65,0 / +58,3 | orta (ızgara dışı)
İkincil: KOMSU z ≥ 1,5 h=2 | SONUC (`A2_komsu_z15_tum_h2`) | 248 gün; +37,0; t=2,50; net +8,5 | yüksek
KOMSU bağımsız değil | SONUC (KESIF satırları) | XELKT z < 1 günlerinde +22,4 (t=1,4), net −17,1; XELKT z ≥ 1 günlerinde +63,1 | orta
İkincil: KOMSU z ≥ 2 → AKSEN h=1 | SONUC (`A2_komsu_z2_aksen_h1`) | 102 olay; +69,0; t=2,77; net +31,5; yarılar +57,3 / +95,8 | orta (378 tek hisse testinden)
İkincil keşif: vadeli SAT, vadeli fiyatıyla | OUT/dondurulmus_is.csv | 28 gün; +91,7; t=1,84; net +62,9 | düşük (olay az)
Aynı kural, spot tam geçmiş (bilgi) | SONUC (KESIF) | 105 gün; +100,4; t=3,5; yarılar +67,4 / +175,8 | orta
Sektör momentumu, doğrusal | REG (`T1_havuz`) | EWx → f1 0,109 (t=3,14); f3 0,247 (t=3,48); XELKT → f1 0,086 (t=2,56) | yüksek
Yukarı/aşağı asimetri | REG (`T4_havuz_asimetri`) | EWx f1: pozitif kısım 0,164 (t=3,7); negatif 0,046 (t=0,7) | yüksek
Bayat fiyat değil | REG (`BAYAT_*`) | EWx f1: gece 0,028 (t=1,6); gün içi 0,092 (t=3,1); en likit 10: 0,099 (t=2,7); sığ: 0,136 (t=2,2) | yüksek
XU030 → hisse yok | REG (`T1_havuz_XU100kontrolsuz`) | f1 −0,049 (t=−1,65); sığ −0,084 (t=−1,6) | yüksek
XU030 eşikli | SONUC | z ≥ 1,5, tümü, h=1: +4,5 bps (t=0,5); net −44,7 | yüksek
“Geciken yetişir” tutmuyor | SONUC | XELKT z ≥ 1,5, gecikenler, h=1: +10,1 (t=0,9); net −22,0 | yüksek
Gecikenler akranlarını geçmiyor | OUT/checks.txt | yukarı yön 63 satırda `sec` ortalaması +0,7 bps | orta
Aşağı yön: geciken düşer | SONUC | XELKT z ≤ −1,5, gecikenler, h=1: −65,5 bps (t=−3,6) | yüksek
T3 büyük hisse → sektör yok | REG (`T3_ters`) | katsayılar −0,05…+0,02; hepsinde \|t\| < 1 | yüksek
Endeks düzeyi (bilgi) | REG (`ENDEKS_*`) | XU030 → XELKT f1 −0,061 (t=−2,0); XELKT → XU030 f1 0,032 (t=1,2) | yüksek
Öz-denetim | OUT/ozdenetim.txt | 4 kesim × 7 kural = 0,0; build 0,10 s; deterministik | yüksek

## açık kalanlar

- Birincil kuralın 2020–2022 yarısı zayıf (t=0,44; 2020 ve 2021 negatif). 2023 sonrası 40'tan fazla hisseli rejim bu yarıya daha çok benziyor; OOS'ta sönme olasılığı gerçek.
- Net +25 bps muhafazakâr maliyette sıfıra iniyor. Kural günde 20–40 hisse alımı gerektiriyor; kapasite ve kapanış seansı dolumu sınanmadı.
- Aile düzeltmeli p yalnız 126 AL-yönlü T2a/T2b kuralı üzerinden hesaplandı. T2c, T4 ve bayat satırlarını içeren tam ızgara düzeltmesi yapılmadı.
- Vadeli SAT keşif kuralında IS'te vadeli fiyatıyla 28 olay günü var; ENJSA ağırlıklı (pay 0,83). AKSEN vadelisi IS'te yalnız 2 ay.
- KOMSU sepeti IS'te fiilen ALARK (GESAN 2021-08'den sonra). OOS'ta ASTOR ve EUPWR eklenince girdi nitelik değiştirir.
- Hayatta kalma yanlılığı (evren bugünkü üyeler) ve VBTS tedbirleri ele alınmadı.
- `elib.py` yeniden değişirse `bash kod/a2_endeks/run.sh <panel_is>` ile tablolar yenilenmeli (yaklaşık 4 dakika).