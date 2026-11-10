# Önkayıt planı v2 — VİOP "öncü oynadı, hedef oynamadı" kuralı (10.11.2026)

Bu dosya hesaptan ÖNCE yazıldı. v1 bağımsız bir yöntem denetçisine verildi; 14 düzeltmesi hesap başlamadan işlendi (en altta değişiklik notu). Çift listesi `ciftler_onkayit.csv`. Sonuçlara bakarak değiştirilmez.

## 0. Kullanıcının kuralı (birebir)
- Karar anı: BIST kapanışına ~10 dk kala (17:50 TSİ = 14:50 UTC).
- Sinyal: ilgili varlık (öncü) o gün belirgin oynamış, hedef varlık oynamamış.
- Giriş: aynı gün VİOP kapanışında (uzlaşma fiyatı), öncünün yönünde.
- Taşıma: 1–3 iş günü, kapanıştan kapanışa. Hedef farkı kapatınca ("doyunca") çıkış.
- Araç: VİOP vadelileri. Evren (09.11.2026 bülteni): 47 pay vadelisi + XU030, XLBNK + USDTRY + XAUUSD, XAGUSD, XAUTRY.

## 1. Dizinler ve kurallar
- Veri (depoya girmez): `VERI=/tmp/claude-0/-home-user-Xxxx/b52fa442-3316-551a-bdd2-9e9f754166e0/scratchpad/veri` → `raw/`, `panel/`. Sözlük: `ek/README_veri.md` (önce bunu oku). Panel dosyalarını DEĞİŞTİRME; ek veri gerekiyorsa `raw/ek_<ajan>/` ve `panel/ek_<ajan>_*.parquet` altına yaz.
- Kod: `/home/user/Xxxx/raporlar/2026-11-10_viop_leadlag_islem/kod/` · Sonuç: `.../ek/`
- Python: `python3 -I betik.py`; betik kod klasöründe durur. Eksik paket `pip install` ile kurulabilir (scipy vb.).
- Yalnız açık uçlar (Yahoo chart API, Borsa İstanbul bülteni, İş Yatırım). TradingView'ın iç websocket'i ya da erişim kısıtını aşan yöntem KULLANILMAZ. İsteklerde kişisel bilgi yok. Ek Yahoo sembolü için `kod/veri_yahoo.py` örnek alınır.

## 2. Veri temizliği (backtest ajanları uygular)
- Hedef işlem getirisi: `fut_ret` (ön vade, aynı kontrat, uzlaşmadan uzlaşmaya). `fut_limit`=1 günü giriş/çıkış yapılamaz.
- Likidite: giriş ya da çıkış günü hedef vadelisinde `fut_trades` < 20 ya da `fut_value_tl` < 1 mn TL ise işlem atlanır.
- Roll: tutma penceresinde `fut_code` değişiyorsa işlem `roll=1` işaretlenir, bu işlemlere bir ek gidiş-dönüş maliyeti yazılır, ayrıca raporlanır.
- 2020-07-27 (endekslerden iki sıfır atıldı): XU030/XLBNK vadeli ve XU030.IS/XBANK.IS spot getirisinde |r| > 0,5 olan gün NaN.
- Spot öncü/hedef: düzeltilmiş kapanış (`adj`) getirisi; `bolunme_gunleri.csv` günleri NaN; |r| > marj (2020-03-13 öncesi ln(1,205), sonrası ln(1,105)) NaN; bayat satır (hacim 0 VE yüksek = düşük) NaN. Hacim 0 tek başına silme nedeni değil (SASA).
- Saatlik/5 dk veride temettü-bölünme düzeltmesi yok: ex-temettü ve bölünme günleri NaN (ex-gün = ham kapanış getirisi ile düzeltilmiş getirinin 50 bps'ten fazla ayrıştığı gün).
- VIOP:USDTRY öncü getirisi = fut_ret − son 20 iş gününün ortalaması (taşıma kayması çıkarılır).

## 3. Zamanlama (ileriye bakma yasağı)
- İşlem: giriş uzlaşma_t (**E0**), çıkış uzlaşma_{t+h}.
- **Sinyal değişkenleri (z_L, z_T, piyasa artığı) aynı saat damgalı SPOT fiyatlardan kurulur**: hedef pay vadelisi için hedefin spotu, piyasa için XU030.IS. `fut_ret` yalnız işlem getirisidir. Spotu olmayan hedeflerde vekil: XU030 → XU030.IS, XLBNK → XBANK.IS; USDTRY, XAUUSD, XAGUSD, XAUTRY için fut_ret (bu satırlar "vekilsiz" diye işaretlenir).
- `YURTICI` öncü: spot kapanıştan kapanışa (t). Bu 17:50 bilgisinin vekilidir; üç sağlamlık testi zorunlu:
  (i) **E2**: sinyal t, giriş uzlaşma_{t+1}.
  (ii) **KATI_1730** (saatlik veri dönemi, 2023-11 →): öncü ve hedef spot getirisi = ln(17:30 TSİ'de bilinen fiyat_t / günlük HAM kapanış_{t−1}). "17:30'da bilinen fiyat": o gün 14:30 UTC barı varsa 13:30 UTC barının kapanışı; yoksa 12:30 UTC barının kapanışı. β ve σ ana tanımla aynı. Giriş uzlaşma_t.
  (iii) **1750 uyumu** (5 dk, son 60 gün): 14:45 UTC barının kapanışıyla kurulan sinyal ile kapanış sinyalinin uyum oranı (yalnız adaylar için).
- `VIOP_T` öncü: günlük sürümde VİOP uzlaşma getirisi (t). Uzlaşma 17:50'de bilinmediği için KATI_1730 vekili zorunlu: XAUUSD → GC=F, XAGUSD → SI=F (14:00 UTC'de biten saatlik barın kapanışı / önceki BIST gününün aynı anı), XU030 → XU030.IS, XLBNK → XBANK.IS. USDTRY'nin güvenilir saatlik vekili yok: USDTRY öncülü satırlar yalnız E2 sonucuyla aday olabilir.
- `ASYA_T`: Tokyo/Sidney/Seul günlük kapanışı; önceki BIST gününden sonraki bütün dış seanslar toplanır (önceki BIST günü < tarih ≤ t).
- `DIS`: iki sürüm ayrı çalışır:
  - `GUNLUK_T1` (2017+, birincil): öncü getirisi = P(tarihi ≤ t−1 olan son dış kapanış) / P(tarihi ≤ t−2 olan son dış kapanış); t−1 ve t−2 BIST işlem günleridir (BIST tatillerinde arada kalan dış günler toplanmış olur). Hedef koşulu iki günlük: z_T(t−1:t) = (e_T,t−1 + e_T,t)/(√2·σ_T).
  - `SAAT_1450` (saatlik veri dönemi, ikincil): öncü getirisi = 14:50 UTC'de bilinen son fiyat_t / önceki BIST gününün 14:50 UTC'de bilinen son fiyatı. Bilinen fiyat = bitiş anı ≤ 14:50 olan son barın kapanışı, yoksa başlamış barın açılışı; 60 dakikadan eskiyse NaN. ABD yaz/kış saati dönemleri ayrı raporlanır (kışın ABD için yalnız açılış fiyatı bilinir).
- β ve σ: yalnız geçmiş veriden, 1 gün gecikmeli (β 250 gün, σ 120 gün).

## 4. Sinyal tanımları
- Artık getiri: e_X = r_X − β_X·r_endeks. Yurt içi için endeks XU030.IS; yabancı hisse için bölge endeksi (uzantısız = ABD: günlük ^GSPC, saatlik SPY; `.AX` = ^AXJO; `.T` = ^N225; `.KS` = ^KS11; diğer Avrupa uzantıları = günlük ^STOXX50E, saatlik EXW1.DE). Emtia/ETF (`=F`, CRACK321, TUR, EEM) ve VİOP öncüleri ham.
- Sepet: bileşen artıklarının eşit ağırlıklı ortalaması (en az yarısı mevcutsa). F1_GRUP'ta 3+ bileşenli NAV sepetlerinde birincil ağırlık **REG**: holding spot getirisinin bileşen getirilerine 250 günlük, sabitsiz, negatif olmayan en küçük kareler regresyonu (1 gün gecikmeli katsayılar, toplamı 1'e ölçekli); eşit ağırlık ikincil satır.
- z_L = e_L/σ_L, z_T = e_T/σ_T (ikisi de spot). ρ = `isaret`. d = ρ·sign(z_L).
- **S_KUL (kullanıcının kuralı, birincil):** |z_L| ≥ 1 ve d·z_T ≤ 0,25 → hedef vadelisinde d yönünde pozisyon. İki alt parça ayrıca: **YATAY** (−0,5 ≤ d·z_T ≤ 0,25) ve **TERS** (d·z_T < −0,5; bu yarı hedefin kendi dönüşüne yakındır).
- **S_ONCU:** |z_L| ≥ 1 (hedefe bakılmaz). **S_IKISI:** |z_L| ≥ 1 ve d·z_T > 0,25.
- **S_HAM:** S_KUL'un ham getirili sürümü (ekranda görülen): |r_L|/σ(r_L) ≥ 1 ve d·r_T/σ(r_T) ≤ 0,25.
- **Kontroller:**
  - **KAYDIR** (asıl kontrol): öncü z_L serisi takvimde en az 250 gün dairesel kaydırılır (500 tekrar, tohum 20261110), z_T ve hedef getirileri aynen kalır. İstatistik: S_KUL sinyal günlerinde ileri h=2 getirinin d yönündeki ortalaması (örtüşmeye izin var; gerçek ve kaydırılmış aynı biçimde). p_kaydır = kaydırılmış ortalamanın gerçek ortalamayı aştığı oran.
  - **S_KENDI:** öncü yok; z_T ≤ −1 → al, z_T ≥ +1 → sat.
  - **BAZSIZ:** hedefin baz değişimi Δb_T = fut_ret_T − spot düzeltilmiş getirisi_T, z120. S_KUL, |z_Δb| ≥ 1 günleri çıkarılarak ayrıca raporlanır.
  - **PIYASA ailesi:** 47 hisse için öncü = XU030.IS ham getirisi, hedef ham spot getirisi ("piyasa oynadı, hisse oynamadı").
- **Sürüklenme düzeltmesi:** işlem getirisi − d·h·(hedefin aynı takvim yılındaki ortalama günlük fut_ret'i). Uzun/kısa sinyal payı yıl yıl raporlanır.
- Eşik duyarlılığı (yalnız adaylar): |z_L| ≥ 0,75 / 1,5 / 2; hedef eşiği 0 / 0,5.

## 5. İşlem kuralları ve ölçüm
- Tek bacak (birincil): hedef vadelisi. İkincil (adaylar): hedef − β_T·XU030 vadelisi.
- Tutma: h = 1, 2, 3 (sabit). **DOYGUN** (adaylar): fark = max(0, |z_L| − d·z_T)·σ_T; birikimli getiri d yönünde hedefin artığıyla (hedge'siz bacakta ham getiri ve ham σ) ölçülür; ≥ 0,5·fark olunca çıkılır, en geç 3. gün. İki uygulanabilir sürüm: **DOYGUN_K1** (karar uzlaşma_k ile, çıkış uzlaşma_{k+1}) ve **DOYGUN_1730** (saatlik dönem; karar 17:30 spot fiyatıyla, çıkış uzlaşma_k). Karar ve çıkışı aynı uzlaşmada sayan sürüm yalnız bilgi amaçlıdır.
- Çift başına örtüşmeyen işlemler. Adaylarda ayrıca **E1** (giriş vadelinin son işlem fiyatı, `viop_gunluk.close`).
- Maliyet (gidiş-dönüş, bacak başına): pay vadelisi 8 ve 15 bps; bireysel: hissenin `rt_cost_retail_bps` değeri (`raporlar/2026-11-02_viop_leadlag/veri_ozet/y_viop_likidite.csv`; yoksa 22); XU030/XLBNK 3 (bireysel 6); USDTRY/metal 3 (bireysel 8).
- İstatistik (işlem getirileri, bps): n, yıllık işlem, ortalama brüt, net8, net15, net_bireysel, t, isabet, medyan, en iyi 10 işlem çıkınca ortalama ve t, yıl yıl ortalama ve pozitif yıl sayısı, sürüklenme düzeltmeli ortalama, uzun işlem payı.
- Dönemler: TAM 2017-03→2026-11; IS 2017–2021; OOS 2022–2026; SON2Y 2024-11-10→2026-11-10; ayrıca 2020-01+.
- **Birincil test (çift başına tek p-değeri): S_KUL, tek bacak, E0, h=2, TAM.** DIS çiftlerinde birincil zamanlama GUNLUK_T1. BH-FDR **tek aile**: F1_GRUP, F2_SEKTOR, F3_DIS, F4_MAKRO, F5_VIOP'un bütün birincil testleri (kontrol aileleri F1_KONTROL, F5_OZDESLIK, PIYASA hariç). Aile bazında q yalnız betimleyicidir.
- Havuz testleri (aile ve toplam): takvim zamanı portföyü (her gün açık işlemlerin eşit ağırlıklı getirisi), Newey-West gecikmesi h+1. S_KUL − S_IKISI farkı ve YATAY/TERS ayrımı raporlanır.
- **F6 keşif taraması (hipotezsiz):** öncü ∈ {47 dayanak spot + panelde olan diğer BIST hisseleri + XU030.IS + XBANK.IS}, hedef ∈ 47 pay vadelisi, S_KUL h=2 E0. Dışarıda: öncü = hedefin kendi spotu, aynı şirketin pay grupları (KRDMA/KRDMB–KRDMD), %50'den fazla sahip olunan bağlı ortaklık (ISDMR–EREGL). Seçim yalnız 2017-03→2022-12'de (t ≥ 3, n ≥ 40); değerlendirme 2023-01→2026-11. "Şansla beklenen" = aynı seçim ve değerlendirmenin 200 dairesel kaydırmalı tekrarındaki sayıların medyanı ve %95'liği (süre 15 dakikayı aşarsa 100 tekrar).
- **F5_OZDESLIK özel sinyali:** s = ln XAUTRY − ln(XAUUSD·USDTRY/31,1035) (ön vade uzlaşmaları); z120(s − 20 günlük ortalama) > 1 → XAUTRY sat, < −1 → al; h=1–3. Kontrol olarak raporlanır.

## 6. Aday ölçütü (önkayıtlı, hepsi birlikte)
n ≥ 40 · TAM brüt t ≥ 2,5 · net_bireysel ortalama TAM ve SON2Y'de > 0 · OOS brüt ortalama > 0 ve t ≥ 1,5 · sürüklenme düzeltmeli OOS ortalama > 0 · E2 ortalama > 0 ve E2 ≥ E0/3 · en iyi 10 işlem çıkınca ortalama > 0 · p_kaydır ≤ 0,05 · tek aile BH-FDR q ≤ 0,10 · YURTICI ve VIOP_T satırlarında KATI_1730 ortalaması > 0 ve aynı dönemdeki E0 ortalamasının en az yarısı (KATI n < 30 ise en çok İZLE) · USDTRY öncülü satırlarda bütün ölçütler E2 sonucuyla.
- Hepsini geçen **ADAY**. En çok iki ölçütten kalan ve TAM t ≥ 2,0 olan **İZLE**. Diğerleri **ELENDİ** (nedeniyle).
- S_ONCU sürümü aynı ölçütlerle ayrıca değerlendirilir ("hedef oynamadı" koşulu olmadan çalışan öncüler).

## 7. Çıktı şeması
- `ek/sonuc_<ajan>.csv`, satır = çift × zamanlama × sinyal × giriş × tutma × dönem:
`aile;hedef;oncu;isaret;zamanlama;agirlik;sinyal;giris;tutma;donem;n;yillik_n;brut;net8;net15;net_bireysel;t;isabet;medyan;brut_ilk10haric;t_ilk10haric;poz_yil;yil_say;brut_suruklenme_duz;uzun_pay`
  (`sinyal` ∈ S_KUL, S_KUL_YATAY, S_KUL_TERS, S_KUL_BAZSIZ, S_ONCU, S_IKISI, S_HAM, S_KENDI; `giris` ∈ E0, E2, KATI)
- `ek/ozet_<ajan>.csv`: çift × zamanlama başına tek satır, 6. bölümdeki her ölçütün değeri ve geç/kal sütunu, p_kaydir, q_fdr, karar (ADAY/İZLE/ELENDİ) ve neden.
- `ek/havuz_<ajan>.csv` (aile × sinyal × tutma) ve adaylar ile İZLE'lerin işlem listesi `ek/islemler_<ajan>.csv` (çift, giriş tarihi, yön, z_L, z_T, çıkış tarihi, brüt bps, roll).
- **Ortak kalibrasyon satırı:** her backtest ajanı `SAHOL ← AKBNK.IS`, S_KUL, E0, h=2, tek bacak, TAM dönem için n, brüt ortalama ve t'yi dönüşünde ayrıca bildirir.

## 8. Önceki çalışmadan güncellenecek kurallar (ESKI ailesi)
`raporlar/2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md` 1. bölümdeki kurallar aynı veriyle 10.11.2026'ya kadar yeniden hesaplanır: XU030 baz sıçraması, SAHOL/AKBNK z60 dönüşü, Koza z3 momentumu (TRMET/TRALT), ABD rafinerileri t−1 → TUPRS (h2), VİOP altın → TRALT (hedge'li h2), FMG+BHP → EREGL (hedge'li h3), VİOP USDTRY 5g → THYAO (h3). Rapor: TAM, OOS, SON2Y, sürüklenme düzeltmeli, E2 ve son 10 işlem günündeki sinyal durumu. **Bu yeniden hesap bağımsız kanıt değildir** (30.10 sonrası yalnız ~7 yeni gün var); amaç aynı yöntemle güncel sayı ve bugünkü durumdur.

## Değişiklik notu (10.11.2026, hesaptan önce)
v1 → v2, yöntem denetçisinin (bağımsız, üst model) 14 maddesi üzerine: (1) sinyal değişkenleri spot fiyattan, baz kontrolü eklendi; (2) KATI_1700 → KATI_1730, aday ölçütüne girdi; (3) VIOP_T öncüleri için saatlik vekil, USDTRY yalnız E2; (4) DOYGUN formülü ve uygulanabilir sürümleri; (5) PLASEBO → KAYDIR kontrolü, YATAY/TERS ayrımı; (6) USDTRY taşıma kayması ve yıl sürüklenmesi düzeltmesi; (7) aday ölçütü sıkılaştı (bireysel maliyet, E2 ≥ E0/3, tek aile FDR); (8) GUNLUK_T1 iki günlük hedef koşulu ve tatil toplaması; (9) SAAT_1500 → SAAT_1450, yaz/kış ayrımı (bayatlık sınırı denetçinin önerdiği 30 dk yerine 60 dk: Avrupa ve emtia barları tam saatte bittiği için 30 dk bütün gözlemleri silerdi); (10) likidite süzgeci, E1; (11) havuzda takvim zamanı portföyü; (12) çift listesi: mekanizmasız "holding → iştirak" satırları F1_KONTROL, özdeşlikler F5_OZDESLIK, NAV sepetlerinde regresyon ağırlığı (denetçinin önerdiği sahiplik × piyasa değeri ağırlığı yerine: sahiplik/pay sayısı verisi yok, regresyon ağırlığı aynı amaca dışarıdan olgu taşımadan hizmet eder); (13) F6'da kendi spotu/pay grupları dışarıda, şans dağılımı kaydırmayla; (14) 2020-07-27, spot öncü temizliği, roll işareti, ESKI ailesi notu, yeni çiftler (ISCTR NAV sepeti, CRACK321, HRC=F, AKGRT).
