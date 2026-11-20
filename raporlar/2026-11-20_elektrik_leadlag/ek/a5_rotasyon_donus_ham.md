araç: 23/40

## Özet (A5 — XELKT / XU030 rotasyonu, yalnız panel_is, 2010-01-04 → 2022-12-30)

**Taranan:** 96 tarih düzeyi sinyal (S1 24, S2 6, S3 4, S4 8, S5 6, S6 48) × 3 hedef (sepet, likit10, AKSEN/ENJSA/ODAS üçlüsü) × h 1–3 AL + üçlüde vadeli SAT = **1.152 ızgara testi**; ayrıca yaklaşık 95 keşif testi (pencere 10/40/60, kontroller, tek hisse, kaydırma, vadeli fiyat). Toplam yaklaşık 1.250. Bütün satırlar `elib.evaluate(measure='own')` ile üretildi.

**Sonuç orta-zayıf:** IS'te BH-FDR'den (q = 0,10) geçen AL testi yok. Aile düzeyi kaydırma testinde en iyi sonucun şansla çıkma olasılığı 0,082. Yine de ölçütlerin (i–vii) hepsini karşılayan 3 kural var; bunlar birincil donduruldu, 6 ikincil eklendi.

**Birincil (3):**
1. `A5_zirve20_viop3_h3`: XELKT 20 günlük en yüksek kapanış → üçlü spot AL, 3 gün. 69 bps (t 3,5), net temel +31, yarılar 73 / 63.
2. `A5_zirve20_sepet_h3`: aynı sinyal → sektör sepeti. 46 bps (t 2,9), net +20.
3. `A5_mom1_sepet_h3`: XELKT z(r_cc) ≥ 1 → sepet, 3 gün. 60 bps (t 3,5), net +27; 2020–22'de yalnız 18 bps (maliyetin altında).

**İkincil (6):** ilk iki sinyalin likit10 sürümleri; gecikme (XU030 z ≥ 1, XELKT z < 0,5 → üçlü h3); 16:00→17:00 göreli güç z ≥ 1,5 (sepet h1, üçlü h3); 14:00→17:00 göreli zayıflık z ≤ −1,5 → üçlü vadeli SAT h1 (yalnız izleme).

**Beklentilere karşı:**
- XELKT gecikme-1 otokorelasyonu pozitif (0,066): doğrulandı. "Likit sepette kaybolur": **doğrulanmadı** (likit10 0,084; üçlü 0,048).
- Göreli güçte 1 günlük devam zayıf (t 1,9); 5–10 günlük dönüş **yok**. S5 (oran ortalamaya dönüş) tamamen boş.
- h = 1'de S1–S5'in hiçbiri maliyeti geçmiyor; etki 2–3 güne yayılıyor.
- "Gecikme" kuralı sektörün yetişmesi değil, piyasa momentumu gibi görünüyor (XU030 korumalı fark t 1,5; sepette koşul bilgi eklemiyor).
- Aşağı yön sinyalleri AL için negatif, vadeli SAT için maliyeti geçmiyor.

**Öz-denetim:** `self_check_causal` 9 kuralın hepsinde 0,0; `build()` 0,1 sn, deterministik; `eval_rule` çıktısı tarama satırlarıyla aynı. `run.sh` baştan sona 2 dk 23 sn.

**Sapma / not:** kütüphanenin `mkt` ölçüsü XU100 kullanıyor (hata değil); görevdeki XU030 korumalı sürümü `aile.py` içinde ayrıca hesapladım. KÜTÜPHANE HATASI yok.

**Dosyalar**
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a5_rotasyon/rules.py
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/kod/a5_rotasyon/run.sh (tara.py, kesif.py, aile.py)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a5_rotasyon_sonuc.csv (1.152 satır; `secim`, `not`)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a5_rotasyon_otokor.csv (EK tablo: gecikme 1–3, iki yarı, yıllar)
- /home/user/Xxxx/raporlar/2026-11-20_elektrik_leadlag/ek/a5_rotasyon.md (549 kelime)

## İddia defteri
iddia | dosya yolu | sayı | güven
--- | --- | --- | ---
Izgara testi sayısı | ek/a5_rotasyon_sonuc.csv | 1.152 satır (birincil 3, ikincil 6, elendi 1.143) | yüksek
BH-FDR q=0,10 geçen AL testi | kod/a5_rotasyon/aile.py çıktısı | 0 / 864 (tek yönlü) | yüksek
Aile içi en iyi sonucun şansla çıkma olasılığı | kod/a5_rotasyon/aile.py çıktısı | 0,082 (basit t 4,35; sıfır %95 eşiği 4,61) | orta
zirve20 → üçlü h3 | ek/a5_rotasyon_sonuc.csv | 547 gün, 266 bağımsız; 68,8 bps; t 3,46; net temel +30,6; muhafazakâr +5,6 | yüksek
zirve20 → üçlü h3, yarılar / en iyi 10 hariç / t+1 kapanış girişi | ek/a5_rotasyon_sonuc.csv | 72,7 / 63,2; 25,4; 64,2 | yüksek
zirve20 → üçlü h3, tek hisse | kod/a5_rotasyon/kesif.py çıktısı | ODAS 114 (t 3,2); AKSEN 49 (2,1); ENJSA 24 (0,8) | yüksek
zirve20 pencere duyarlılığı (üçlü h3; keşif) | kod/a5_rotasyon/kesif.py çıktısı | 10 gün 62; 40 gün 67; 60 gün 68 bps | yüksek
zirve20 → üçlü h3, vadeli fiyatıyla (2018-12+) | kod/a5_rotasyon/aile.py çıktısı | 263 gün; 70 bps; t 2,1; 2021: −98 | orta
zirve20 → sepet h3 | ek/a5_rotasyon_sonuc.csv | 45,5 bps; t 2,90; net +20,4; yarılar 32,5 / 64,5; top10 hariç 11,1; muhafazakâr −4,6 | yüksek
mom1 → sepet h3 | ek/a5_rotasyon_sonuc.csv | 428 gün, 318 bağımsız; 60,2 bps; t 3,53; net +26,6 | yüksek
mom1 → sepet h3, yarılar ve yıllar | ek/a5_rotasyon_sonuc.csv | 81,0 / 17,8; 2020: −16, 2021: −73, 2022: +105 | yüksek
mom1 → sepet h3, giriş gecikmesi | ek/a5_rotasyon_sonuc.csv | t+1 kapanış girişi 25,7 bps; gece payı 0,44 | yüksek
zirve20 → likit10 h3 | ek/a5_rotasyon_sonuc.csv | 50,1 bps; t 2,87; net +9,3 | yüksek
mom1 → likit10 h3 | ek/a5_rotasyon_sonuc.csv | 57,0 bps; t 3,08; net +17,7; yarılar 77,6 / 15,3 | yüksek
gecikme (XU030 z≥1, XELKT z<0,5) → üçlü h3 | ek/a5_rotasyon_sonuc.csv | 140 gün; 79,8 bps; t 2,90; net +60,3 | yüksek
gecikme: XU030 korumalı fark | kod/a5_rotasyon/aile.py çıktısı | 36 bps; t 1,5 | orta
gecikme kontrolü: XU030 z≥1 koşulsuz → sepet h3 (keşif) | kod/a5_rotasyon/kesif.py çıktısı | 31,7 bps (t 2,4); gecikme koşuluyla 34 bps (t 1,8) | yüksek
gün sonu 16→17 göreli z≥1,5 → sepet h1 | ek/a5_rotasyon_sonuc.csv | 85 gün; 49,9 bps; t 2,37; net +16,7; t+1 açılış girişi 47,5; t+1 kapanış girişi 9,2 | yüksek
gün sonu 16→17 göreli z≥1,5 → üçlü h3 | ek/a5_rotasyon_sonuc.csv | 121,3 bps; t 2,45; net +94,8; 2021: −262 | orta
16:00→kapanış sürümü (aynı eşik) → sepet h1 | ek/a5_rotasyon_sonuc.csv | 2 bps; t 0,1 (komşu doğrulamıyor) | yüksek
14→17 göreli z≤−1,5 → üçlü vadeli SAT h1 | ek/a5_rotasyon_sonuc.csv | 60 gün; 57,7 bps; t 1,99; top10 hariç −12,8; vadeli fiyatıyla 55 (t 1,6) | orta
Aynı sinyalde sepet AL h1 | ek/a5_rotasyon_sonuc.csv | −58,8 bps; t −2,9 | yüksek
XELKT gecikme-1 otokorelasyonu | ek/a5_rotasyon_otokor.csv | IS 0,066; ≤2019 0,053; 2020–22 0,075 | yüksek
likit10 ve üçlü gecikme-1 otokorelasyonu | ek/a5_rotasyon_otokor.csv | 0,084; 0,048 (üçlü 2020–22: 0,016) | yüksek
XU030(t−1) → XELKT(t) korelasyonu | ek/a5_rotasyon_otokor.csv | 0,013 (t 0,76) | yüksek
Regresyon XELKT(t) ~ XELKT(t−1) + XU030(t−1) | kod/a5_rotasyon/kesif.py çıktısı | +0,103 (t 3,3); −0,061 (t −2,1) | yüksek
XU030 korumalı fark (sinyal günü − bütün günler) | kod/a5_rotasyon/aile.py çıktısı | zirve20 üçlü +85 (t 4,5); zirve20 sepet +55 (3,6); mom1 sepet +52 (3,7) | orta
Sinyal örtüşmesi | kod/a5_rotasyon/kesif.py çıktısı | mom1 günlerinin %51'i zirve20 günü; RS1 z≥2 günlerinin %76'sı mom1 günü | yüksek
Karar anı: 17:00 değeriyle kapanış sinyalinin görülen payı (2017+) | kod/a5_rotasyon/kesif.py çıktısı | zirve20 %89 (yanlış %13); mom1 %73 (yanlış %18); ~18:00'de %97 / %90 | orta
Nedensellik öz-denetimi | kod/a5_rotasyon/tara.py çıktısı | 9 kuralın hepsi 0,0; build 0,1 sn | yüksek

## açık kalanlar
- IS kanıtı çoklu test düzeltmesini geçmiyor; birincil kuralların değeri OOS-1 sınamasına bağlı. Üç birincil kural birbirine bağımlı (aynı "sektör yukarı trend" teması), bağımsız üç kanıt sayılmamalı.
- Sinyaller resmi kapanış değeriyle kurulu. Kullanıcı kapanıştan birkaç dakika önce karar verdiği için mom1 sinyallerinin yaklaşık dörtte biri 17:00'de henüz görünmüyor; 17:00 değeriyle kurulan sürüm ayrı kural olarak sınanmadı.
- S6 kuralları panel klasöründe `h1_isy/` arar; OOS panelinde yoksa boş sinyal üretir (hata vermez). OOS'ta yaklaşık 35 olay beklenir: E6'nın "en az 30" sınırında.
- Sepet kuralları sözlükte `min_n = 5` taşır; ortak OOS betiği `eval_rule` kullanmıyorsa bu alan dikkate alınmalı.
- `A5_gunsonu1417_asagi_viop3_sat_h1` işlemlerinin %70'i ENJSA (VİOP başlangıç tarihleri nedeniyle) ve en iyi 10 gün çıkınca negatif: yalnız izleme.
- VBTS tedbirleri ve kapanış seansı dolum hacmi sınanmadı. Sepet hedefi 2023+ döneminde 40'tan fazla hisse demek; uygulanabilir sürüm likit10 (net getirisi daha düşük).
- Veri notu: `idx_ret` içindeki XBANK sütununda bozuk değer var (en büyük 101); A5'te kullanılmadı.
- `kod/a5_rotasyon/__pycache__` ve tam çalıştırma günlüğü (/tmp/claude-0/-home-user-Xxxx/4917622c-a1fc-5288-a182-a19cca9a4438/scratchpad/a5/run.log) temizlenmedi/kalıcı değil.