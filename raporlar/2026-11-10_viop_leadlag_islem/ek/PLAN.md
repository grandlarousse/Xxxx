# Önkayıt planı — VİOP "öncü oynadı, hedef oynamadı" kuralı (10.11.2026)

Bu dosya hesaptan ÖNCE yazıldı. Çift listesi `ciftler_onkayit.csv`. Sonuçlara bakarak değiştirilmez; değişiklik olursa en alta tarihli not düşülür.

## 0. Kullanıcının kuralı (birebir)
- Karar anı: BIST kapanışına ~10 dk kala (17:50 TSİ = 14:50 UTC).
- Sinyal: ilgili varlık (öncü) o gün belirgin oynamış, hedef varlık oynamamış.
- Giriş: aynı gün VİOP kapanışında (uzlaşma fiyatı), öncünün yönünde.
- Taşıma: 1–3 iş günü, kapanıştan kapanışa. Hedef farkı kapatınca ("doyunca") çıkış.
- Araç: VİOP vadelileri. Evren (09.11.2026 bülteni): 47 pay vadelisi + XU030, XLBNK + USDTRY + XAUUSD, XAGUSD, XAUTRY.

## 1. Dizinler
- Veri (depoya girmez): `VERI=/tmp/claude-0/-home-user-Xxxx/b52fa442-3316-551a-bdd2-9e9f754166e0/scratchpad/veri` → `raw/` (indirilen), `panel/` (temiz).
- Kod: `/home/user/Xxxx/raporlar/2026-11-10_viop_leadlag_islem/kod/`
- Sonuç: `/home/user/Xxxx/raporlar/2026-11-10_viop_leadlag_islem/ek/`
- Python: indirilen dosyayı okuyan her betik `python3 -I betik.py` ile çalışır; betik kod klasöründe durur, veri klasöründe asla. Kardeş modül gerekiyorsa betik `sys.path.insert(0, <kod klasörü>)` yapar.
- Yalnız açık uçlar: Yahoo chart API, Borsa İstanbul VİOP bülteni (`https://www.borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv`, cp1254, `;`), İş Yatırım. TradingView'ın iç websocket'i ya da erişim kısıtını aşan hiçbir yöntem KULLANILMAZ. İsteklerde kullanıcıya ait bilgi yok; User-Agent genel.

## 2. Veri panelleri (veri ajanı üretir; `panel/README_veri.md` sözlüğüyle)
1. `viop_gunluk`: 2017-03 → 2026-11-10 bütün vadeli (F_) satırları: date, code, und, expiry, settle, prev_settle, open, high, low, close(son işlem), vwap, value_tl, volume, trades, oi.
2. `fut_ret` (tarih × dayanak): ön vade uzlaşmadan uzlaşmaya log getiri, AYNI kontrat `ln(settle/prev_settle)`; vadeye < 2 iş günü kalınca sonraki vade. Yanında `fut_settle`, `fut_value_tl`, `fut_trades`, `fut_code`.
   - Pay vadelisinde |getiri| > fiyat marjı (2020-03-13 öncesi ln(1,205), sonrası ln(1,105)) → NaN. Bedelsiz/bölünme günü → NaN.
   - `fut_limit` bayrağı: |getiri| ≥ marjın %93'ü (kilit; o gün giriş/çıkış yapılamaz sayılır).
3. `spot_gunluk`: Yahoo günlük OHLCV + düzeltilmiş kapanış, 2014 → bugün: 47 dayanak + çift listesindeki bütün `.IS` kodları + XU030.IS, XU100.IS, XBANK.IS + keşif taraması için BIST100'ün kalan likit üyeleri.
4. `dis_gunluk`: çift listesindeki bütün yabancı semboller + bölge endeksleri (^GSPC, ^STOXX50E, ^AXJO, ^N225, ^KS11), 2014 → bugün. Yahoo `=X` kur serisi KULLANILMAZ (günlük kapanışı 00:00 UTC, bir gün kayık).
5. `saatlik`: Yahoo 1h, 730 gün, UTC zaman damgalı: 47 dayanak + listede geçen `.IS` + XU030.IS + bütün yabancı semboller + SPY, EXW1.DE (ya da ^STOXX50E), BZ=F, GC=F, ES=F.
6. `dk5`: Yahoo 5m, 60 gün: 47 dayanak + listede geçen `.IS` + XU030.IS.
- Bilinen tuzaklar: SASA hacmi 2025-06'dan beri günlerin ~%42'sinde 0 ama fiyat işliyor (silme); saatlik veride temettü düzeltmesi yok; Yahoo'da XU030/XU100/XBANK dışı BIST endeks geçmişi bozuk.

## 3. Zamanlama kuralları (ileriye bakma yasağı)
- Hedef getirisi: `fut_ret`. İşlem: giriş uzlaşma_t, çıkış uzlaşma_{t+h}.
- `YURTICI` öncü: spot kapanıştan kapanışa (t). Bu, 17:50 bilgisinin yaklaşık vekilidir; bu yüzden üç sağlamlık testi zorunlu:
  (i) **E2**: sinyal t, giriş uzlaşma_{t+1} (plasebo; kapanış anı mikro yapısını ayıklar).
  (ii) **KATI_1700**: son 730 günde sinyal, öncü ve hedef spotun 14:00 UTC'de (17:00 TSİ) BİLİNEN fiyatıyla (önceki günün 14:00 UTC fiyatına göre getiri) kurulur; giriş yine uzlaşma_t.
  (iii) **1750 uyumu**: son 60 günde 14:50 UTC fiyatıyla kurulan sinyal ile kapanış sinyalinin işaret/eşik uyum oranı.
- `VIOP_T` öncü: VİOP ön vade uzlaşma getirisi (t). Aynı üç test uygulanabildiği kadar (E2 her zaman).
- `ASYA_T`: Tokyo/Sidney/Seul günlük kapanışı t (BIST kapanışından önce biter).
- `DIS`: iki sürüm ayrı ayrı çalışır:
  - `SAAT_1500` (son 730 gün): öncü getirisi = 15:00 UTC'de bilinen son fiyat / önceki BIST gününün 15:00 UTC'de bilinen son fiyatı. ABD hisselerinde bu fiilen 14:30 UTC açılış sonrası ilk barlardır. Kış/yaz saati kayması UTC ile çalışıldığı için sorun değil.
  - `GUNLUK_T1` (2017+): öncünün t−1 tam gün getirisi (ABD/Avrupa kapanışı BIST t−1 kapanışından sonra oluşur); hedefin "oynamadı" koşulu t günü getirisiyle.
- β ve σ: yalnız geçmiş veriden, 1 gün gecikmeli (β 250 gün, σ 120 gün).

## 4. Sinyal tanımları
- Artık getiri: e_X = r_X − β_X·r_endeks. Yurt içi için endeks XU030 spot; yabancı hisse için kendi bölge endeksi (uzantıya göre: uzantısız=ABD ^GSPC/SPY, `.AX`=^AXJO, `.T`=^N225, `.KS`=^KS11, diğer Avrupa uzantıları=^STOXX50E/EXW1.DE); emtia/ETF (`=F`, TUR, EEM) ve VİOP öncüleri ham.
  Hedefte: e_T = fut_ret − β_T·XU030 vadeli getirisi (pay vadelisi için); endeks/kur/metal hedeflerinde ham.
- Sepet: bileşen artıklarının eşit ağırlıklı ortalaması (en az yarısı mevcutsa).
- z_L = e_L/σ_L, z_T = e_T/σ_T. `isaret` sütunu ρ: beklenen ilişkinin yönü. d = ρ·sign(z_L).
- **S_KUL (kullanıcının kuralı):** |z_L| ≥ 1 ve d·z_T ≤ 0,25 → hedefte d yönünde pozisyon.
- **S_ONCU:** |z_L| ≥ 1 (hedefe bakılmaz).
- **S_IKISI:** |z_L| ≥ 1 ve d·z_T > 0,25 (hedef de oynamış; kullanıcının koşulunun tümleyeni).
- **S_HAM:** S_KUL'un ham getirili sürümü: r_L/σ(r_L) ≥ 1 (mutlak) ve d·r_T/σ(r_T) ≤ 0,25. Ekranda görülen budur.
- **Kontroller:** (a) S_KENDI: öncü yok; z_T ≤ −1 → al, z_T ≥ +1 → sat (hedefin kendi dönüşü). (b) PLASEBO: her hedefe mekanizma bağı olmayan 5 rastgele öncü (sabit tohum) ile S_KUL. (c) PIYASA ailesi: 47 hisse için öncü = XU030 spot ham getirisi, hedef ham getirisi ("piyasa oynadı, hisse oynamadı").
- Eşik duyarlılığı (yalnız adaylar için): |z_L| ≥ 0,75 / 1,5 / 2; hedef eşiği 0 / 0,5.

## 5. İşlem kuralları ve ölçüm
- Tek bacak (birincil; kullanıcının yaptığı): hedef vadelisi. İkincil: hedef − β_T·XU030 vadelisi (hedge'li).
- Tutma: h = 1, 2, 3 (sabit) ve **DOYGUN**: ilk k ≤ 3 gününde hedefin girişten beri d yönündeki birikimli getirisi ≥ 0,5·|z_L − d·z_T|·σ_T olursa o günün uzlaşmasında çık, olmazsa 3. gün çık.
- Çift başına örtüşmeyen işlemler (pozisyondayken yeni sinyal alınmaz). Giriş ya da çıkış günü `fut_limit` ise işlem atlanır/çıkış ertesi güne kayar (raporla).
- Maliyet (gidiş-dönüş, bacak başına): pay vadelisi 8 ve 15 bps; bireysel 22 bps senaryosu; XU030/XLBNK 3; USDTRY/metal 3. Hisse bazlı tahmin için `raporlar/2026-11-02_viop_leadlag/veri_ozet/y_viop_likidite.csv` (`rt_cost_small_bps`, `rt_cost_retail_bps`).
- İstatistik (işlem getirileri, bps): n, yıllık işlem, ortalama brüt, net8, net15, net22, t (havuzda tarih kümelemeli), isabet oranı, medyan, en iyi 10 işlem çıkınca ortalama ve t, yıl yıl ortalama ve pozitif yıl sayısı.
- Dönemler: TAM 2017-03→2026-11; IS 2017–2021; OOS 2022–2026; SON2Y 2024-11-10→2026-11-10.
- **Birincil test (çift başına tek p-değeri): S_KUL, tek bacak, E0, h=2.** Önkayıtlı F1–F5 çiftleri üzerinde BH-FDR (q). DIS çiftlerinde birincil zamanlama GUNLUK_T1 (uzun örneklem); SAAT_1500 ikincil.
- Havuz testleri (aile bazında ve toplam): bütün çiftlerin işlemleri birlikte, tarih kümelemeli t. S_KUL − S_IKISI farkı ("hedef oynamadı" koşulu değer katıyor mu?) ve S_KUL − S_KENDI − PLASEBO karşılaştırması ayrıca raporlanır.
- **F6 keşif taraması (hipotezsiz):** öncü ∈ {47 dayanak spot + BIST100'ün diğer likit üyeleri + XU030 + XBANK}, hedef ∈ 47 pay vadelisi, S_KUL h=2. Seçim yalnız 2017-03→2022-12'de (t ≥ 3, n ≥ 40); değerlendirme 2023-01→2026-11. Raporla: seçilen çift sayısı, OOS'ta aynı işaretle t ≥ 2 olanların sayısı, şansla beklenen sayı.

## 6. Aday ölçütü (önkayıtlı)
Bir çift/sinyal ancak şunların hepsini sağlarsa "ADAY" olur ve doğrulamaya gider:
n ≥ 40 · TAM brüt t ≥ 2,5 · net15 ortalama > 0 · OOS brüt ortalama > 0 ve t ≥ 1,5 · SON2Y ortalama > 0 · E2 ortalama ≥ 0 · en iyi 10 işlem çıkınca ortalama > 0 · aile içi FDR q ≤ 0,10.
Geçemeyen "ELENDİ" olarak nedeni ile listelenir. Sınırda kalanlar "İZLE".

## 7. Çıktı şeması (bütün backtest ajanları aynı şemayı kullanır)
`ek/sonuc_<ajan>.csv`, satır = çift × zamanlama × sinyal × giriş × tutma × bacak:
`aile;hedef;oncu;isaret;zamanlama;sinyal;giris;tutma;bacak;donem;n;yillik_n;brut;net8;net15;net22;t;isabet;medyan;brut_ilk10haric;t_ilk10haric;poz_yil;yil_say;q_fdr`
Ayrıca `ek/havuz_<ajan>.csv` (aile × sinyal × tutma), `ek/adaylar_<ajan>.csv` (6. bölüm ölçütlerinin tek tek geç/kal sütunları) ve adayların işlem listesi `ek/islemler_<ajan>.csv` (çift, giriş tarihi, yön, z_L, z_T, çıkış tarihi, getiri bps).
**Ortak kalibrasyon satırı:** her backtest ajanı `SAHOL ← AKBNK.IS`, S_KUL, E0, h=2, tek bacak, TAM dönem sonucunu ayrıca bildirir (iki uygulamanın aynı sayıyı üretip üretmediğini görmek için).

## 8. Önceki çalışmadan güncellenecek kurallar (ESKI ailesi)
`raporlar/2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md` 1. bölümdeki kurallar aynı veriyle 10.11.2026'ya kadar yeniden hesaplanır: XU030 baz sıçraması, SAHOL/AKBNK z60 dönüşü, Koza z3 momentumu (TRMET/TRALT), ABD rafinerileri t−1 → TUPRS (h2), VİOP altın → TRALT (hedge'li h2), FMG+BHP → EREGL (hedge'li h3), VİOP USDTRY 5g → THYAO (h3). Rapor: TAM, OOS, SON2Y ve son 10 işlem günü için sinyal durumu.
