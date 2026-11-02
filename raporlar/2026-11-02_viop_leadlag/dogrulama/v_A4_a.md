# v_A4_a — Bağımsız doğrulama: İddia A4 (havayolu sepeti t-1 → THYAO/PGSUS/TAVHL gün-içi)

Doğrulayıcı: v_A4_a (1. aşama: bağımsız yeniden üretim + zamanlama). Tarih 02.11.2026, veri sonu 30.10.2026.
Kod: `out/code_v_A4_a/` (vcore.py, v0..v5; loglar v0_timing_checks.log, v1.log … v5.log; sonuç dosyaları res/).
ll.py ve h.py import EDİLMEDİ. Ham parquet'ten kendi hizalama, temizlik ve backtest kodumu yazdım. Tanımları kaynak koddan (a3_multi.signals, a5b_attrib "AIR_only(eu+us)") okudum.

## 0. Karar özeti
**DÜZELT.** İstatistiksel ilişki gerçek ve rakamlar ondalığına kadar yeniden üretildi. Zamanlamada ileriye bakma yok. Ancak iddianın "işlenebilir 20–25 bps/işlem" kısmı iyimser:
1. Getiri 15 bps maliyette OOS'ta anlamsızlaşıyor (t 1,5–2,0).
2. Açılış müzayedesinden sonra (10:30 TSİ) girilirse THYAO ve TAVHL'de brüt kazancın %30–60'ı kayboluyor.
3. 2024+ döneminde PGSUS ve TAVHL'de net getiri t≈1,1–1,2.
4. IS anlamlılığının çoğu COVID 2020'den geliyor.
5. TUR bacağı son 3 yılda zarar ettiriyor.
6. "XU100'de ≈0" sadece NET bazda doğru. Brüt etki 6–8 bps (t 1,0–1,5).

**Güven:** İlişki için THYAO/PGSUS ORTA, TAVHL DÜŞÜK. Net işlenebilirlik DÜŞÜK–ORTA. COMBO (TUR'lu) DÜŞÜK.

## 1. Yeniden üretim (a)
Tanım:
- Sepetler: EU = LHA, AF, IAG, RYA, EZJ, WIZZ, JET2; US = DAL, UAL, AAL, LUV, ALK, JBLU. Her sepet, üyelerin log getirilerinin ortalamasıdır (en az 2 üye; sıfır getiri NaN sayılır).
- Artık: EU − β·STOXX600, US − β·SPX. β 250 günlük kayan pencereden hesaplanıyor (min 120 gün, shift 1).
- z-skor: 250 günlük ortalama ve standart sapma, shift 1, ±3'te kırpılmış.
- AIR = zEU + zUS. Sinyal t-1'de alınır; |AIR| > 1 ise sign(AIR) yönünde pozisyon açılır.
- Hedef: log(c/o) t (Yahoo açılışı → kapanış). Maliyet: işlem başına gidiş-dönüş.

Kendi sinyal serilerim kaynaktakilerle birebir aynı (corr 1,000000, en büyük fark 0). Bu, kaynaktaki hesabın kodlama hatası içermediğini gösteriyor; aynı zamanda tanımı aynen kopyaladığım anlamına geliyor.

| 8 bps net | IS 2014–2020 bps (t_NW) | OOS 2021–2026 bps (t_NW) | OOS t (iid) | OOS brüt | İddia |
|---|---|---|---|---|---|
| THYAO | 17,6 (2,33) n=783 | **20,3 (2,77)** n=675 | 2,30 | 28,3 | 20,3 (2,77) ✓ |
| PGSUS | 22,0 (2,24) | **24,5 (2,78)** | 2,58 | 32,5 | 24,5 (2,78) ✓ |
| TAVHL | 9,0 (1,04) | **20,8 (2,31)** | 2,23 | 28,8 | 20,8 (2,3) ✓ |
| XU100 | −0,5 (−0,10); brüt 7,5 (1,53) | −2,1 (−0,38); brüt 5,9 (1,06) | | | "≈0" yalnız net bazda |
| COMBO→THYAO | 23,2 (3,27) | **25,8 (3,66)** | 2,99 | 33,8 | 25,8 (3,66) ✓ |
| TUR_{t-1}→THYAO gün-içi corr | IS −0,085 (t −2,88) | OOS −0,137 (t −3,89) | Tümü −0,110 (t −4,61) | | ✓ |

Not: NW-t, iid t'den yüksek çıkıyor (THYAO OOS 2,77'ye karşı 2,30). Muhafazakâr değer iid t'dir.

**Maliyet 15 bps (OOS):** THYAO 13,3 (t 1,81), PGSUS 17,5 (1,99), TAVHL 13,8 (1,54). IS: 10,6 (1,41) / 15,0 (1,53) / 2,0 (0,23). Başabaş maliyet (OOS brüt) 28–32 bps.

## 2. Zamanlama / ileriye bakma denetimi (b) — GEÇTİ
- Kapanış saatlerini saatlik veriyle doğruladım (v0):
  - ABD (DAL, UAL, AAL, TUR, ^GSPC): son bar 19:30/20:30 başlangıçlı, yani kapanış 20:00 UTC (yaz) / 21:00 UTC (kış). Günlük c ile h1 son bar kapanışı %87–99 oranında 10 bp içinde.
  - AB (LHA, AF, IAG, ^STOXX): son sürekli işlem barı 15:00/16:00'da başlıyor; kapanış 15:30/16:30 UTC. Günlük c, kapanış müzayedesi fiyatı (h1 barından medyan 15–24 bp farklı).
  - Tüm bileşenler t-1 akşamı, BIST açılış müzayedesinden (06:55–07:00 UTC) en az 14 saat önce kapanıyor.
  - Sepette Asya bileşeni yok, dolayısıyla "BIST açılışından sonra kapanan aynı gün Asya piyasası" sorunu doğmuyor.
- β ve z yalnızca t-1'e kadarki veriyi kullanıyor (shift 1). Kırpma (clip) ileriye bakma yaratmıyor.
- Varyant B: kendi zaman damgası hizalamamı da kurdum ("takvim tarihi < t olan son kapanış"; shift yok; BIST tatilinden sonra daha taze bilgi). Varyant A ile corr 0,964, pozisyon uyumu %96,5. Sonuçlar aynı (OOS THYAO 18,2 t 2,56; PGSUS 21,3 t 2,47; TAVHL 20,0 t 2,28; COMBO-THYAO 27,3 t 3,90).
- **BIST açılışı:** Yahoo günlük o, 2023-11 sonrasında günlerin %99,9'unda h1 06:30 barının açılışına eşit; son 60 günde de 5 dk 06:55 müzayede barına %100 eşit. Yani o = açılış müzayedesi fiyatı. Günlük c = kapanış müzayedesi fiyatı (h1 son barından medyan 9–16 bp farklı; h1'de 15:00 kapanış barı neredeyse hiç yok). 2014–2022 için bunu doğrulayamadım; o == önceki c oranı %3–13 ile doğal düzeyde.
- Sinyal gap'te HİÇ fiyatlanmıyor: AIR → gap brüt THYAO −1,3 / +0,5 bps (IS/OOS); PGSUS 2,1 / 4,7; TAVHL −0,5 / 0,9. Etkinin tamamı açılıştan sonra, gün içinde ortaya çıkıyor. İşlenebilirlik açısından bu olumlu.
- Temizlik duyarlılığı: ±%10,5 dışı günler (THYAO 4, PGSUS 7, TAVHL 3; ör. 2016-07-18, 2020-03-12, 2023-02-15) gün-içi hedefte tutulsa da sonuç değişmiyor (OOS 19,9 / 24,2 / 20,3).

## 3. Sağlamlık (c)
**Alternatif giriş (h1, 2023-11-30..2026-10-30, n≈354 işlem)** — en önemli zayıflık:

| brüt bps (t) | açılış→kapanış | ilk saat (açılış→10:30 TSİ) | 10:30→kapanış | 11:30→kapanış | 10:30 giriş net 8 / 15 bps |
|---|---|---|---|---|---|
| THYAO | 23,0 (3,11) | 6,5 (2,0) | 16,5 (2,39) | 13,7 (2,23) | 8,5 (1,23) / 1,5 |
| PGSUS | 19,5 (2,07) | −0,1 | 19,6 (2,35) | 10,3 (1,39) | 11,6 (1,39) / 4,6 |
| TAVHL | 19,3 (2,06) | 11,5 (2,2) | 7,8 (0,92) | 7,5 (1,00) | −0,2 / −7,2 |
| XU030 | 8,2 (1,25) | 1,4 | 6,9 (1,15) | | |

- Saatlik katkı profili gün boyuna yayılmış. Tek bir yoğun pencere yok; THYAO'da son dilim (14:30→kapanış) +5,4 bps (t 2,0).
- **VİOP pay vadelisi bülteni** (en yüksek hacimli kontrat, açılış→kapanış; 2023 + 2025–26, n=225 işlem):
  - Brüt: THYAO 26,0 (t 2,00), PGSUS 18,6 (1,30), TAVHL 9,2 (0,51).
  - 8 bps net: 18,1 / 10,6 / 1,2.
  - corr(vadeli gün-içi, spot gün-içi) 0,90–0,94.
  - Medyan günlük işlem hacmi: THYAO ~1,9 milyar TL, PGSUS ~470 milyon TL, TAVHL ~260 milyon TL.
  - VİOP açılış seansı işlemleri çok ince (ör. 30.10'da THYAO 9 kontrat). Açılış fiyatından dolum iyimser bir varsayım.
- **Eşik:** |AIR| > 0,5 de çalışıyor (OOS 18,4 / 23,3 / 17,4). Eşik 0'da THYAO IS 3,2 bps (t 0,6). Eşik 1,5–2'de THYAO OOS 13,0 / 10,5 (t ≤ 1,5).
- **Tanım:**
  - Artıksız ham sepet: THYAO OOS 9,6 (t 1,27), IS 4,1 (0,57). THYAO sonucu artıklaştırmaya bağlı.
  - β 120 günlük pencere: 16,8 / 20,6 / 15,1 (OOS). β 500 günlük pencere: 18,8 / 21,1 / 20,6.
  - Tek bacak (eşik 0,5): yalnız EU OOS 14,1 / 20,7 / 9,9; yalnız US 18,0 / 21,5 / 19,0. IS'te tek bacaklar zayıf (THYAO EU 4,0, US 9,7).
  - Üye-dışarıda (13 varyant), OOS: THYAO 17,1–22,9, PGSUS 20,1–30,6, TAVHL 18,8–25,3. Tek üyeye bağımlı değil. IS'te EZJ veya RYA çıkarılınca THYAO 9,6–11,5 (t 1,2–1,5).
- **Sürekli regresyon** (gün-içi_t ~ AIR_{t-1}, standartlaştırılmış, NW):
  - THYAO t 4,42 (IS 3,09 / OOS 3,20); PGSUS 4,51 (3,31 / 3,10); TAVHL 3,23 (1,76 / 2,89).
  - Kendi cc_{t-1}, XU100 cc_{t-1}, kendi gap_t ve XU100 gap_t kontrol edilince değişmiyor (THYAO 4,38; PGSUS 3,87; TAVHL 3,12).
  - XU100 gün-içi_t (eşzamanlı) kontrolüyle THYAO t 5,37: etki hisseye özgü.
  - Eşzamanlı EU_X_t ve US_X_t eklenince katsayı 0,085'ten 0,070'e düşüyor, t 3,5. Sürücü momentumu (corr(AIR_{t-1}, EU_X_t) = 0,098) etkinin yalnız küçük bir kısmını açıklıyor.
- **XU030 hedge'li hedef** (hisse − β·XU030 gün-içi): brüt OOS 20,6 (t 3,35) / 25,2 (3,23) / 21,2 (2,97). İki bacak için 16 bps maliyetle 4,6 / 9,2 / 5,2 (t < 1,2). Hisseye özgü kısım gerçek ama hedge'li işlem kârsız.
- **Dairesel kaydırma null'u** (1.000 kaydırma): gözlenen tüm dönem değerleri (18,9 / 23,1 / 14,5 bps) null dağılımının %99'unu (5–8 bps) aşıyor; p < 0,001.
- **Plasebo:** AIR t-2 → OOS 6,2 / 8,5 / 1,3 (t < 0,9); t-3 ve t-5'te ≈0 veya negatif. ✓
- **Uzun/kısa:** IS'te uzun +4 bps, kısa −47 bps, düz −11 bps; OOS'ta uzun +33, kısa −23, düz −11 (THYAO). Düz günlere göre iki taraf da katkı veriyor; IS'te kısa taraf, OOS'ta uzun taraf baskın.
- **Çoklu test:** Kaynakta yaklaşık 14 sinyal varyantı × 3 hisse denendi. OOS backtest t 2,77 için Bonferroni(14) p ≈ 0,08 (42 test için 0,23); TAVHL için 0,29. Sürekli regresyon t 4,4 / 4,5 düzeltmeden sonra da geçiyor; TAVHL t 3,2 sınırda (Bonferroni 42 test için 0,05).

## 4. IS/OOS ve yıllar (d)
Yıllık net değerler, 8 bps, bps/işlem:

| | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| THYAO | 0,4 | −13,0 | 9,9 | 17,8 | 10,2 | 25,9 | 66,0 | 44,1 | 12,1 | 12,5 | 21,7 | 13,9 | 17,4 |
| PGSUS | 2,6 | −8,6 | 13,4 | 19,1 | −0,4 | 17,4 | 98,9 | 66,5 | 28,5 | 19,4 | 22,4 | 8,3 | 2,9 |
| TAVHL | −8,3 | −10,2 | −14,6 | 7,1 | −8,3 | 2,8 | 83,2 | 78,5 | 2,8 | 13,8 | 29,1 | 6,2 | −4,7 |

- Pozitif yıl sayısı: THYAO 12/13, PGSUS 11/13, TAVHL 8/13 (2014–2018 arası çoğunlukla negatif).
- Alt dönemler (THYAO): 2014–2017/6 −1,1 (t −0,15); 2017/7–2020 35,6 (2,85); 2021–2023 22,9 (1,78); 2024–2026 17,7 (2,48). PGSUS 2024+ 11,4 (1,18); TAVHL 2024+ 10,4 (1,09).
- COVID (2020-02..2021-06) hariç: IS THYAO 9,4 (t 1,24), PGSUS 8,3 (0,94), TAVHL −5,6. OOS 18,1 (2,45) / 20,8 (2,35) / 16,9 (1,91). IS anlamlılığının büyük kısmı COVID'den geliyor.

## 5. TUR ve COMBO
- TUR_{t-1} → THYAO gün-içi negatif ilişki 13 yılın 10'unda görülüyor (2019, 2020 ve 2024 pozitif). PGSUS ve TAVHL'de IS'te sıfır veya pozitif, yalnız OOS'ta negatif (yaklaşık −0,10).
- −TUR tek başına THYAO'da 2024 / 2025 / 2026 net −22 / −22 / −16 bps.
- COMBO'nun TUR bacağı sonradan eklendi ve son dönemde zarar ettiriyor. 2024+ THYAO: COMBO 12,5 (t 1,76), AIR 17,7 (2,48). 15 bps'te COMBO 2024+ için THYAO 5,5, PGSUS 2,4, TAVHL 0,1.
- COMBO'nun OOS 25,8 (t 3,66) değeri gerçek bir holdout değil. Güven: DÜŞÜK.

## 6. Düzeltilmiş iddia
Avrupa+ABD havayolu artık sepeti (AIR) t-1'de |z| > 1 olduğunda, ertesi gün BIST gün-içi getirisi aynı yönde. Bu etki istatistiksel olarak sağlam, ileriye bakma yok, gap'te fiyatlanmıyor ve hisseye özgü:
- Sürekli regresyon t: THYAO 4,4, PGSUS 4,5, TAVHL 3,2.
- Brüt OOS getiri: 28 / 32 / 29 bps/işlem.
- 8 bps maliyette OOS net 20,3 / 24,5 / 20,8 (iid t 2,3 / 2,6 / 2,2). 15 bps'te 13 / 17 / 14 (t 1,5–2,0).

Gerçekçi uygulamada zayıflıyor:
- 10:30 TSİ girişte (2023-11..2026-10) 8 bps net THYAO 8,5 (t 1,2), PGSUS 11,6 (t 1,4), TAVHL ≈0.
- VİOP vadeli bülteninde (n=225 işlem) brüt THYAO 26 (t 2,0), PGSUS 19 (1,3), TAVHL 9 (0,5).
- 2024+ döneminde PGSUS ve TAVHL'de 8 bps net yaklaşık 11 bps (t ≈1,1).

İşlenebilirlik sırası THYAO ≥ PGSUS >> TAVHL. Net kenar, açılış müzayedesinde ya da açılıştan hemen sonra düşük maliyetle (≤8–10 bps) girebilmeye bağlı.

## 7. Sınırlamalar
- 2014–2022 için açılış fiyatının müzayede fiyatı olduğunu doğrulayamadım; yalnız 2023-11 sonrası doğrulandı.
- Saatlik ve VİOP örneklemleri kısa (~350 ve 225 işlem). 10:30 giriş sonucundaki belirsizlik büyük; ±1 standart hata yaklaşık ±7 bps.
- Kaynak tanımını aynen kopyaladım. Sepet üyeleri ve eşik, tam dönem bakılarak seçilmiş olabilir. Kendi varyant ızgaram da aynı veride çalıştığı için gerçek bir holdout yok.
- VİOP vadeli maliyetine baz, tik ve kayma dahil değil. VİOP açılış seansı çok ince.

TradingView adayları: BIST:THYAO, BIST:PGSUS, BIST:TAVHL; XETR:LHA, EURONEXT:AF, LSE:IAG, LSE:EZJ, LSE:WIZZ, LSE:JET2, NASDAQ:RYAAY (Ryanair ADR; RYA.IR için Euronext Dublin kodu ?), NYSE:DAL, NASDAQ:UAL, NASDAQ:AAL, NYSE:LUV, NYSE:ALK, NASDAQ:JBLU, AMEX:JETS (vekil), TVC:SXXP veya STOXX:SXXP (?), SP:SPX, NASDAQ:TUR. VİOP pay vadelisi TV kodu belirsiz (?).
