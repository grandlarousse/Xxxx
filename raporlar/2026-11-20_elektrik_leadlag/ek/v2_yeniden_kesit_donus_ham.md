araç: 23/40

## Özet

T2, K1 ve K2 ham İş Yatırım JSON'larından, ortak kütüphane ve hazır paneller kullanılmadan yeniden üretildi; üçü de **YENİDEN ÜRETİLDİ**. Ana ajanla en büyük fark 3,1 bps (K2 IS), işaret farkı yok. Ancak T2'nin (ve T1'in) kasa rakamı kıyas kirlenmesiyle yaklaşık üç-dört kat şişmiş.

- **Veri:** 8 hisse (AKSEN, ENJSA, ODAS, BIGEN, LYDYE, MAGEN, ZOREN, AYEN) İş Yatırım'dan yeniden indirildi, ham dosyalarla fark sıfır. Benim panelimle panel_full arasında 65.497 getiri hücresinin 15'i farklı (panelin Yahoo yamaları).
- **(a) Kıyas kirlenmesi var ve kasada büyük.** Kasada kıyas sepetinin ertesi gün getirisi ortak tanımda −29,8 bps/gün; tabanda kapananlar çıkarılınca −3,2. T2 bu hisseleri bayrak süzgeci yüzünden seçemiyor, kıyas ise içeriyor.
- **T2 temiz kıyasla:** kıyastan tabanda kapananlar çıkınca IS +8,2 / OOS-1 +13,6 / kasa +9,7 (t 1,6); kıyas yalnız bayraksız hisseler olunca kasa +7,8 (t 1,3). T2, IS ve OOS-1 görülerek dondurulduğu için tek bağımsız sınavı kasaydı; orada anlamlılığı kaybediyor.
- **Medyan kıyası** her dönemde yukarı yanlı (IS +29, OOS-1 +42, kasa +32); temiz bir sınama değil.
- **(b) Çıkış kaydırması yok:** T2 kasa +14,1 (t 2,3); K1 kasa −49 (t −7,0), havuz −34; K2 kasa −270 (t −9,8). İşaretler korunuyor, kasa büyüklüklerinin yarıdan fazlası kaydırmadan geliyor.
- **(c) T2 ham getiri:** kasada seçilenler +6,3 bps (25 bps temel maliyetin altında), seçilmeyenler −37,4; kaydırmasız seçilmeyenler −10,5. OOS-1'de +15,8'e karşı −2,2.
- **(d) T1'de sızıntı yok.** Model her ayın ilk günü s'de eğitiliyor; son eğitim satırı s−7, etiketinin çıkışı en geç s−1. Tahmin gününün etiketi eğitime girmiyor.
- **T1 kasa rakamı da kirli.** Ana ajanın T1 sinyalini kendi getirilerimle okudum (görev tanımının bir adım ötesi; model yeniden yazılmadı): ortak kıyasla kasa +40,6 ana ajanla aynı, tabansız kıyasla +13,2 (t 3,1), ayrıca kaydırmasız +10,0 (t 2,4). OOS-1 sağlam kalıyor (+21 ile +25 arası, t ≈ 5).

Yazılan dosyalar:
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v2_yeniden_kesit.md
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v2_yeniden_kesit.csv (fark tablosu ve bütün sürümler)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v2_yeniden_kesit_T2_ham.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/v2_yeniden_kesit_T1_kiyas.csv
- Kod: /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/v2_yeniden_kesit/ (run.sh, v2lib.py, 01_kurallar.py, 02_indir_dogrula.py, 03_panel_karsilastir.py, 04_T1_denetim.py). Dört betik ayrı ayrı çalıştırıldı; run.sh'in yalnız sözdizimi denetlendi, baştan sona koşulmadı.

## İddia defteri

iddia | dosya yolu ya da URL | sayı ya da birebir kısa alıntı | güven
---|---|---|---
T2 IS: v2 +10,67 (t 2,75), ana +10,51 | ek/v2_yeniden_kesit.csv | 2541 gün, 4450 işlem; medyan işlem −10,8; isabet 0,473 | yüksek
T2 OOS-1: v2 +16,15 (t 2,88), ana +17,16 | ek/v2_yeniden_kesit.csv | 618 gün, 2845 işlem (ana 2832); isabet 0,449 | yüksek
T2 kasa: v2 +36,98 (t 4,67), ana +37,98 | ek/v2_yeniden_kesit.csv | 351 gün, 2026 işlem (ana 2024); isabet 0,508 | yüksek
T2 havuz 2023+: v2 +23,69 (t 5,15); ana tabloda yok | ek/v2_yeniden_kesit.csv | 969 gün, 4871 işlem | yüksek
K1 IS: v2 −18,67 (t −3,11), ana −18,37 | ek/v2_yeniden_kesit.csv | 2375 gün, 4250 işlem; isabet 0,454 | yüksek
K1 OOS-1: v2 −29,02 (t −5,39), ana −28,77 | ek/v2_yeniden_kesit.csv | 619 gün, 3596 işlem | yüksek
K1 havuz 2023+: v2 −63,97 (t −8,86), ana −63,81 | ek/v2_yeniden_kesit.csv | 970 gün, 6113 işlem (ana ile aynı) | yüksek
K1 kasa: v2 −125,6 (t −7,35); ana tabloda yok | ek/v2_yeniden_kesit.csv | 351 gün, 2517 işlem; kaydırmasız −49,2 (t −6,99) | yüksek
K2 IS: v2 −122,82 (t −3,85), ana −119,76 | ek/v2_yeniden_kesit.csv | 537 gün, 675 işlem (aynı); fark −3,06 | yüksek
K2 OOS-1: v2 −147,31 (t −4,75), ana −148,30 | ek/v2_yeniden_kesit.csv | 306 gün, 440 işlem | yüksek
K2 kasa: v2 −626,74 (t −8,59), ana −626,75 | ek/v2_yeniden_kesit.csv | 229 gün, 471 işlem (aynı); isabet 0,310 | yüksek
K2 tabanda kapananlar hariç: IS −16,5 / OOS-1 −91,4 / kasa −80,9 (t −2,7) | ek/v2_yeniden_kesit.csv | ana ajan −13 / −91 / −74; farkın nedeni muhtemelen bayrak tanımı | orta
Kasada kıyas sepeti aşağı çekiliyor | kod/v2_yeniden_kesit/01_kurallar.py çıktısı | ortak −29,8; tabansız −3,2; kaydırmasız −7,6 bps/gün | yüksek
Kasada kıyasta 230 taban kapanışı var | kod/v2_yeniden_kesit/01_kurallar.py çıktısı | 230 / 13.191 dolabilir hisse-gün; BIGEN 29, LYDYE 14, MAGEN 13 gün art arda | yüksek
T2, kıyasta tabanda kapanan yok | ek/v2_yeniden_kesit.csv | IS +8,19 (2,14); OOS-1 +13,61 (2,46); kasa +9,71 (1,56); havuz +12,19 (2,91) | yüksek
T2, kıyas yalnız bayraksız hisseler | ek/v2_yeniden_kesit.csv | IS +7,79; OOS-1 +12,64; kasa +7,75 (1,26); havuz +10,87 (2,61) | yüksek
T2, medyan kıyası (yukarı yanlı) | ek/v2_yeniden_kesit.csv | IS +28,97; OOS-1 +41,84; kasa +31,78 | yüksek
T2, çıkış kaydırması yok | ek/v2_yeniden_kesit.csv | IS +9,33 (2,44); OOS-1 +15,38 (2,81); kasa +14,14 (2,29); havuz +14,93 (3,61) | yüksek
K2, çıkış kaydırması yok | ek/v2_yeniden_kesit.csv | IS −78,1; OOS-1 −118,1; kasa −270,0 (t −9,83) | yüksek
Kütüphane kaydırmayı +5 günle sınırlıyor; sınırsızda sonuç büyüyor | kod/ortak/elib.py (fwd_exec, max_delay=5); ek/v2_yeniden_kesit.csv | T2 kasa +45,26; K1 kasa −154,6; K2 kasa −730,4 | yüksek
T2 ham getiri, kasa | ek/v2_yeniden_kesit_T2_ham.csv | seçilen +6,3; seçilmeyen −37,4 (fark 43,6; t 4,75); kaydırmasız −10,5 (fark 16,7; t 2,38) | yüksek
T2 ham getiri, OOS-1 | ek/v2_yeniden_kesit_T2_ham.csv | seçilen +15,8; seçilmeyen −2,2 (fark 18,0; t 2,87) | yüksek
T1 eğitim penceresi yalnız geçmişi kullanıyor | kod/a8_model/rules.py satır 152–166 | "b = np.searchsorted(pos, s - emb, 'left')", emb = h + 5 = 6; son etiket çıkışı s−1 | yüksek
T1 kesme sınaması: fark sıfır | kod/v2_yeniden_kesit/04_T1_denetim.py çıktısı | "farkli hucre 0 / sinyal 10717"; tahmin maks fark 0 | yüksek
`nedensellik_oran` 0,059 sızıntı değil, sayısal kırılganlık | ek/kasa_sonuc.csv; 04_T1_denetim.py çıktısı | panel_dev ile panel_full: 630 / 10.717 sinyal farklı; ret_cc'de 10 hücre < 6,4e-7 ayrışıyor, 9'unda yuvarlama dönüyor | yüksek (mekanizma orta)
T1 sinyali, ortak kıyas, benim getirilerim | ek/v2_yeniden_kesit_T1_kiyas.csv | IS +4,53 (1,35); OOS-1 +24,97 (5,88); kasa +40,55 (7,33) | yüksek
T1 sinyali, kıyasta tabanda kapanan yok | ek/v2_yeniden_kesit_T1_kiyas.csv | OOS-1 +22,44 (5,32); kasa +13,24 (3,07); havuz +19,11 (6,14) | yüksek
T1 sinyali, kaydırmasız | ek/v2_yeniden_kesit_T1_kiyas.csv | kasa +19,30 (4,49); kaydırmasız ve tabansız kıyas +10,00 (2,36) | yüksek
Yeniden indirme ham dosyalarla aynı | https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil | 8 hisse; kapanış, yüksek/düşük, hacim, düzeltilmiş kapanış maks fark 0,0 | yüksek
Benim panelim ile panel_full | kod/v2_yeniden_kesit/03_panel_karsilastir.py çıktısı | getiri 15 / 65.497 hücre farklı; tradable 32 hücre; taban kapanışı 634'e karşı 647 | yüksek

## açık kalanlar

- **T2 ve T1'in kasa "doğrulandı" sınıfı yeniden değerlendirilmeli.** Temiz kıyasla T2 kasa t 1,3–1,6 (Holm'dan geçmez), T1 kasa +10 ile +19 arası (t 2,4–4,5). İkisi de temel maliyetin (25 bps) altında. Hangi kıyasın karar ölçüsü olacağı ana ajanın kararı; E2'deki tanım kasadan önce yazıldı, yani ortak rakam protokole uygun ama yanıltıcı.
- **Aynı kirlenme S1/S2 zamanlama kurallarına ('per') bulaşıyor mu, bakılmadı.** Sepet tabanda kapanan hisseleri aldığı için yön ters olabilir; bu görev dışıydı.
- **`nedensellik_oran` 0,059, oos_degerlendir.py'deki 0,005 eşiğinin üstünde ve kasa tablosunda işaretsiz duruyor.** Sızıntı olmadığı kesme sınamasıyla gösterildi, ama T1'in sinyalleri panel sürümüne göre yaklaşık %6 değişiyor. Ana tablodaki IS +3,8'e karşı +4,6 farkı buradan geliyor.
- **K2 "tabanda kapananlar hariç" kasa rakamı 7 bps ayrışıyor** (benim −81, ana ajan −74). Ana ajanın bu rakamı hangi kodla ürettiğini görmedim; büyük olasılıkla panelin daha kapsayıcı taban bayrağı (2023 sonrası 15 hücre fazla).
- **Küçük sayım farkları tek tek izlenmedi** (T2 IS 2541'e karşı 2548 gün, OOS-1 2845'e karşı 2832 işlem). Değme bayrağı tanımı (E4'teki 2 adım, panelde %0,6 pay) ve 32 Yahoo yamalı hücreyle uyumlu; etkisi en çok 1 bps.
- **Bilinen sınırlar aynen geçerli:** T1 modeli yeniden yazılmadı; evren bugünkü üyeler; 2015-12 öncesi bayraklar güvenilmez.