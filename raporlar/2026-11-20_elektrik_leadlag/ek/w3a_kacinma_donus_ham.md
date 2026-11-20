araç: 28/40

## Özet
Üç kural donduruldu: iki spot kaçınma, bir VİOP SAT (izleme). Dördüncü yuva boş bırakıldı. Kasa açılmadı; yalnız `panel_dev` kullanıldı. Kütüphane hatası görülmedi. Tarama 490 satır (388 spot, 102 vadeli fiyatlı); rakam çiftleri IS / OOS-1, bps.

- **Kural 1 – tavana değdi, tavanda kapanmadı (kaçınma, own, h=1):** −99 (t −2,6) / −82 (t −2,8). 2018–2024'ün her yılı eksi. Kaybın %42'si gecede; ertesi gün açılışta almak da kötü (−52). Zayıflık 2.–3. günde sürüyor. Likit üçte birlikte işaret aynı ama t düşük.
- **Kural 2 – sektörden ≥ 5 puan geride kapanan, taban dâhil (kaçınma, sec, h=1):** −120 (t −3,8) / −148 (t −4,8). Doz-tepki tek yönlü (%3 → %5 → %7). Kayıp çoğunlukla gecede; kapanışta almayan kaçınır. Uyarı: IS'te etkinin çekirdeği tabanda kapananlar; taban hariç −11 (t −0,4) / −91 (t −3,0).
- **Kural 3 – sektör sepeti z ≤ −1 iken direnen AKSEN/ENJSA/ODAS → vadelide SAT, 1 gün:** vadeli fiyatıyla +38 (t 0,9) / +74 (t 1,3), net +15 / +19. Spot tam geçmişte güçlü (−90, t −4,1 / −103, t −2,0). Kasada ~21 olay, güç %13: büyük olasılıkla “güç yetersiz” çıkar.

Kural 3 için iki uyarı:
- Eşik −1,5 yerine −1 seçildi (olay sayısı için; SAPMA). −1,5 komşusu +37 / +92.
- `A2_ewx_zm15_geciken_viop_sat_h1` ile akraba; kasada ikisi bağımsız kanıt sayılmamalı.

Dondurulmayanlar:
- **K3 (tabanda kapandı):** −449 / −320; kural 2'nin alt kümesi, ayrı kural kopya olurdu.
- **K2 (tabana değdi, kapanmadı):** −94 (t −1,5) / −128 (t −2,1); IS zayıf, kural 2 ile örtüşüyor.
- **K5 bütün hisselerde:** own −61 / +2, tutarsız.
- **K6:** işaret değişimini 2023 taşıyor (−185; 29 olay). Mutlak eşikle (sepet ≥ +%3) +21 / −2. Rejim kanıtı yok; iki yönde de kural çıkmıyor.
- **Vadeli SAT'ın geri kalanı:** iki dönemde de beklenen yönde ve |t| ≥ 2 olan vadeli satır yok. K4 %3 SAT −43 / +84, K6 SAT −59 / +85. K1'in vadeli sürümü 6 + 8 olay ve A4'te zaten dondurulmuş.

Süzgeç etkisi: K1 ∪ K2 ∪ K4 %5 hisse-günlerin %4,8 / %4,9'unu eler; rastgele alıcının ertesi gün ortalaması +4,7 / +5,9 bps iyileşir.

Öz-denetim: `self_check_causal` dört kesimde üç kural için 0,0; `build()` 0,17 sn, deterministik. `run.sh` baştan sona çalıştı (yaklaşık 1 dakika).

Dosyalar:
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3a_kacinma/rules.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3a_kacinma/scan.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3a_kacinma/finalize.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/w3a_kacinma/run.sh
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/w3a_kacinma_sonuc.csv
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/w3a_kacinma.md

## İddia defteri
Dosya yolu kısaltması: CSV = /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/w3a_kacinma_sonuc.csv (`sinyal_tanimi` sütunu). Sayılar IS / OOS-1.

iddia | dosya yolu | sayı | güven
---|---|---|---
K1 own h1 | CSV: K1_AL_h1_own | −99,3 (t −2,56; 208 olay) / −81,8 (t −2,83; 241) | yüksek
K1 sec h1 | CSV: K1_AL_h1_sec | −62,5 (t −1,7) / −60,0 (t −2,3) | yüksek
K1 yıllar | CSV: yillar_bps | 2018 −576; 2019 −348; 2020 −139; 2021 −169; 2022 −1; 2023 −89; 2024 −112; 2025 +14 | yüksek
K1 tavana < %2 yakın kapanış | CSV: K1_yakin2_AL_h1_own | −144 (t −2,1) / −148 (t −2,4) | orta
K1 hacim > 2× medyan / olağan | CSV: K1_hacim2x_AL_h1_own, K1_hacim_olagan_AL_h1_own | −114 / −117; −45 / −20 | orta
K1 gece payı, t+1 açılış girişi | CSV: K1_AL_h1_own (gece_payi, giris_acilis1_bps) | 0,42; −52 | orta
K1 2. ve 3. gün | CSV: K1_gecikme1/2_AL_h1_own | −32 / −40; −26 / −50 | orta
K1 likit üçte birlik | CSV: K1_likit_AL_h1_own | −86 (t −1,0) / −93 (t −1,7) | orta
K4 %5 sec h1 | CSV: K4a5_AL_h1_sec | −119,8 (t −3,77; 537) / −148,3 (t −4,77; 305) | yüksek
K4 %5 own h1 | CSV: K4a5_AL_h1_own | −130 (t −3,9) / −188 (t −5,3) | yüksek
K4 doz-tepki (own) | CSV: K4a3 / K4a4 / K4a7_AL_h1_own | %3: −46 / −101; %4: −92 / −146; %7: −248 / −343 | yüksek
K4 %5 taban hariç (sec) | CSV: K4a5_tabansiz_AL_h1_sec | −10,6 (t −0,4) / −91,4 (t −3,0) | yüksek
K4 %5 gece / gün içi (sektöre göre) | CSV: ek_gece_*, ek_gunici_* (tetik K4a5) | gece −143 / −84; gün içi +56 / −34 | orta (ek hesap)
K4 %5 2. ve 3. gün (sec) | CSV: K4a5_gecikme1/2_AL_h1_sec | −73 / −76; −62 / −89 | orta
K4 %5 fiyat ≥ 5 TL (sec) | CSV: K4a5_px5_AL_h1_sec | −157 / −146 | orta
K3 tabanda kapandı own | CSV: K3_AL_h1_own | −449 (t −4,2; 143) / −320 (t −4,1; 80); gece payı 1,1 | yüksek
K2 own | CSV: K2_AL_h1_own | −94 (t −1,5; 118) / −128 (t −2,1; 94) | orta
En kötü beşte birlik sec; taban hariç | CSV: K4q_AL_h1_sec, K4q_tabansiz_AL_h1_sec | −18,3 (t −3,1) / −28,8 (t −5,3); −4,2 / −17,4 | yüksek
K5 bütün hisseler own; sec | CSV: K5_AL_h1_own, K5_AL_h1_sec | −61 (t −3,5) / +2 (t 0,1); −21 / −56 | yüksek
K6 own h1 ve yıllar | CSV: K6_AL_h1_own | +24,6 (t 2,2; 216) / −91,1 (t −1,8; 29); 2023 −185, 2024 −37, 2025 +47 | yüksek
K6 mutlak eşik (sepet ≥ +%3) | CSV: K6abs3_AL_h1_own | +21 (t 1,0) / −2 (t 0,0) | orta
Süzgeç kapsamı ve iyileşme | CSV: ek_kapsam_*, ek_iyilesme_* (tetik B_K1_K2_K4a5) | kapsam %4,77 / %4,93; +4,7 / +5,9 bps | orta (ek hesap)
Kural 3 vadeli fiyatla | CSV: W3A_sektor_dustu_direnen_VIOP_SAT_h1 (viop_vadeli) | +37,6 (t 0,87; 45) / +74,2 (t 1,31; 38); net temel +15,3 / +19,3 | yüksek
Kural 3 spot tam geçmiş (AL yönünden) | CSV: K5z10_3hisse_spotAL_h1_own | −90 (t −4,1; 176) / −103 (t −2,0; 39); 15 yılın 14'ü eksi | yüksek
Kural 3 komşu eşik z ≤ −1,5 (vadeli) | CSV: K5_VIOP_SAT_h1 | +37 (t 0,9; 25) / +92 (t 1,4; 13) | orta
K4 %3 ve K6 vadeli SAT | CSV: K4a3_VIOP_SAT_h1, K6_VIOP_SAT_h1 | −43 / +84; −59 / +85 | yüksek
K1 vadeli SAT | CSV: K1_VIOP_SAT_h1 | +17 (6 olay) / +182 (8 olay) | düşük (olay az)
Kasa beklentisi ve güç (α 0,05 / Holm en sıkı adım) | CSV: kasa_beklenen_olay, guc_a05, guc_holm10 | K1: 136 olay, %69 / %42; K4 %5: 172 olay, %89 / %72; kural 3: 21 olay, %13 / %3 | orta (σ OOS-1'den, etki iki dönemin küçüğü)
Yer değiştirme sınaması (300 kaydırma, bütün geliştirme dönemi) | CSV: yer_degistirme_p | üç kuralda p = 0,0033 (alt sınır) | orta
Nedensellik öz-denetimi | kod/w3a_kacinma/finalize.py çıktısı | 4 kesim × 3 kural: 0,0; build 0,17 sn | yüksek

## açık kalanlar
- Kural 2'nin taban dışındaki kısmı IS'te yok sayılacak kadar zayıf. Kasada kural doğrulansa bile “taban hariç” ayrımı ayrıca raporlanmalı; bu satır dondurulmadı, bilgi satırı olur.
- Kural 3 kasada büyük olasılıkla “güç yetersiz” sınıfına düşer (yaklaşık 21 olay). Olayların %65'i ENJSA.
- Güç hesabı 40 hisselik OOS-1 olay sıklığına dayanıyor; kasada evren 42 hisse, olay sayısı biraz daha yüksek olabilir.
- Gece / gün içi ayrımı ile kapsam ve iyileşme rakamları `scan.py` içindeki ek hesaptır (elib matrisleriyle); `evaluate` çıktısı değildir.
- VBTS tedbirleri ve hayatta kalma yanlılığı sınırları burada da geçerli; kaçınma kurallarını etkileyip etkilemediği sınanmadı.
- Not dosyası 700 kelime sınırında: düz sayımda 730 (tablo çizgileri ve bölü işaretleri dâhil), ayraçlar hariç 692.