# Backtest protokolü (bağlayıcı, 21.11.2026)

Kod ajanları birebir uygular. Parametre taramak yasak. Burada yazmayan her test `birincil=0` sayılır ve geçemez.

## 1. Profil ve getiri
1. Giriş: sinyal günü t kapanışı. Çıkış: t+h kapanışı. **Birincil ufuk h=1** (aksi yazmadıkça); h=2, h=3 ve t+1 açılışı ikincil sütun.
2. Getiri basit, bps, düzeltilmiş (A*) fiyatlardan. Negatif alfa beklenen sinyal "uzak dur"dur; ters ETF yalnız araç tablosunda.
3. Araç başına tek pozisyon: açıkken gelen sinyal yok sayılır. Her işleme tam gidiş-dönüş maliyeti yazılır.
4. `ham` = ileri getiri. `artik` = ileri getiri − β × SMH ileri getirisi (β: t'ye kadar 250 günlük, en az 120 gün).

## 2. Veri
1. Bozuk satır (High < max(Open,Close), Low > min(Open,Close), High = Low) sinyal üretmez.
2. Sinyal koşulu: fiyat ≥ 3 $, 20 günlük medyan günlük ciro ≥ 20 milyon $, 250 günlük geçmiş.
3. **Zaman damgası.** Kapanışı 16:00 ET'den sonra olan öncüller (BTC-USD, ETH-USD: bar 00:00 UTC'de kapanır; `=F`, `=X`, DX-Y.NYB) yalnız **t−1 barıyla** kullanılır; t barı geleceğe bakıştır. Asya/Avrupa aynı takvim günü t barıyla; yerel tatilde sinyal yok. VIX ailesi (16:15) t barıyla; sağ kalan sinyal t−1 ile yeniden sınanır.
4. Bilanço tepki günü: duyuru 16:00'dan sonraysa ertesi işlem günü, açılıştan önceyse aynı gün; saat yoksa iki adaydan göreli hacmi büyük olan. F1–F5, F10, LL1–LL4'te tepki günü [t, t+h] içine düşen işlem atılır.
5. Evrenler: **T (temiz)** = SMH, SOXX, QQQ, XLK, SPY, IWM. **Ç (çekirdek)** = ilk verisi ≤ 2016-01-01 olan hedef hisseler. **YENİ** = diğer hedefler. **ARAÇ** = kaldıraçlı/ters ETF'ler.
6. Dönemler: P1 2010–2019, P2 2020–2022, P3 2023-01-01 → 2026-11-20; ayrıca son 12 ay.

## 3. Örneklem tasarımı
1. Çıkarım yalnız Ç ve T havuzlarında, tam dönemde. Parametreler sabit; dönemler birbirine örneklem dışıdır. Gerekçe: P3 tek başına ancak 27 bps'yi ayırt ediyor.
2. YENİ ve ARAÇ için anlamlılık testi yok: ADAY/GEÇTİ kural aynen uygulanır; `tasima` tablosunda ortalama, %90 aralık, n.
3. Kaldıraçlı ETF getirisi kendi fiyatından (ücret, finansman, aşınma içinde); sentetik geçmiş yok.
4. LL6: keşif 2010 → 2023-12-29 (çiftte ≥ 750 ortak gün), doğrulama 2024-01-02 → 2026-11-20.

## 4. İstatistik
1. Zamanlama alfası α = işlem ortalaması (getiri − aracın o dönemdeki günlük ortalaması × taşınan gün): araç × dönem sabit etkisi. Gerekçe: yalnız araç etkisi P3 sürüklenmesini sinyale yazar.
2. Standart hata giriş tarihine (h=1) ya da haftasına (h ≥ 2) göre kümeli. Gerekçe: benzetimde kümesiz t %30 yanlış alarm verdi (ikili korelasyon 0,37); kümeli %1–4.
3. `t_takvim`: açık pozisyonların günlük fazla getirilerinin eşit ağırlıklı serisi, Newey-West 5.
4. `p_perm`: sinyal matrisi bütün araçlarda aynı rastgele miktarda (≥ 60 gün) dairesel kaydırılır; 500 tekrar.
5. Havuz esastır. Araç bazlı satırlar betimseldir (istisna: F11).
6. Getiri türü: F1–F9, F11, LL1, LL4 `ham`; kesitsel aileler F10, LL2, LL3, LL5, LL6 `artik` ve ham α işareti aynı olmalı.
7. "Eğim" testlerinde `p_birincil` panel eğiminden (öncülün 60 günlük z-skoru başına bps; hedefin ve SMH'nin t getirisi kontrol). Ayrıca z ≥ +1 olay testi yazılır; net α > 0 olmalı. Diğerlerinde `p_birincil = p_kume`.

## 5. Güç (benzetim, %80 güç)
| Durum | Saptanabilir en küçük kenar, bps (t=2 / t=3) |
|---|---|
| Tek hisse σ %3,6; 100 işlem | 102 / 138 |
| SMH σ %2,3; 850 işlem | 22 / 30 |
| SOXL σ %7,4; 250 işlem | 133 / 180 |
| Ç havuzu, P3, ham | 27 / 36 |
| Ç havuzu, P3, artık | 11 / 15 |
| Ç havuzu, 2010+, ham | 11 / 15 |
| 120 olay (σ %4) | 103 / 139 |

h=3 için × 1,7. Karar: hisse ailelerinde havuz şart; tek hisse ve tek kaldıraçlı ETF testi yok. n_islem < 100 ya da n_gun < 60 → GÜÇSÜZ. Her satıra `mde_bps = 2,84 × se`.

## 6. Çoklu test
1. Sayılan: aşağıdaki **61 birincil test** (B1 21, B2 27, B3 13).
2. Tek havuzda Benjamini-Hochberg %10. Ek eşik: |t| ≥ 2,5 (`kaynak=lit`), ≥ 3,0 (`kaynak=turev`).
3. LL6 ayrı havuz: keşifte BH %10; doğrulamada aynı işaret, tek yönlü t ≥ 2 ve BH %10. Şansla beklenen = 0,10 × keşif sayısı.
4. Sınanmaz (israf): haftanın günü, vade haftası, tatil öncesi, RSI(2) < 5, lider olarak SMH/QQQ.

## 7. 15:30 testi
1. Saatlik veri (730 gün). P1530 = 15:30 barının açılışı; H/L 09:30–14:30 barlarından; yarım günler atılır. Sentetik kapanış = AClose × P1530 / 15:30 barının kapanışı.
2. F1–F5 ve F10 birincil sinyalleri için: A = sinyal ve giriş kapanışta; B = sinyal 15:30'da, giriş kapanışta; C = ikisi de 15:30'da.
3. Ölçüt: B > 0 ve B ≥ 0,5 × A. 15:50 sınanmaz (veri 60 gün); 15:30 daha zor koşul.
4. `B1_1530.csv`: test_id, n_A, n_B, uyum_A_B, uyum_B_A, A_bps, B_bps, C_bps, son30dk_bps, oran_B_A.

## 8. Maliyet
1. Varsayım: kapanış müzayedesi emri yok; 15:55–15:59'da limit ya da piyasa emri. Kapanıştan sapma maliyetin içindedir.
2. Gidiş-dönüş, 5.000 $ pozisyon, işlem başı 1,5 $ komisyon dahil: **M1 = 10 bps** (NVDA AMD AVGO TSM MU MSFT GOOGL META AMZN AAPL TSLA; T evreni; SOXL SOXS TQQQ SQQQ). **M2 = 20 bps** (son 250 günde medyan ciro ≥ 300 milyon $). **M3 = 40 bps** (kalanlar, tek hisse kaldıraçlı ETF'ler).
3. Ayrıca 2× maliyetle net; oransal komisyon senaryosu (+50 bps) ekonomi tablosunda.

## 9. Test listesi
**B1 — `kod/b1_fiyat.py` (21).** Her biri Ç ve T'de (2 test), aksi yazmadıkça.
- F1a: IBS = (C−L)/(H−L) < 0,2 → al. lit
- F1b: F1a ve C > 200 günlük ortalama. lit
- F1c: IBS > 0,8 → uzak dur. lit
- F1d: F1a alfasının VIX ≥ 25 eksi VIX < 25 farkı, Ç+T birlikte (1). lit
- F2: Wilder RSI(2) < 10 → al; C > 5 günlük ortalama olunca ya da 3. gün çık. lit
- F3: üst üste 3 düşük kapanış → al. lit
- F4a: r < −2σ (t−1'e kadar 60 gün) → al. F4b: r > +2σ → al. lit
- F5a: C = son 20 kapanışın en yükseği ve hacim > 1,5 × önceki 20 gün ortalaması. F5b: hacim ≤ 1,5 ×. turev
- F10a: z < −2 → al; F10b: z > +2 → uzak dur; yalnız Ç. z = 5 günlük birikimli artık / (60 günlük artık σ × √5). lit
- F6 (tanı): araç ve dönem başına kapanış→açılış ve açılış→kapanış payı.

**B2 — `kod/b2_leadlag.py` (27).**
- LL1 (5, eğim, lit): öncülün t günü yerel getirisinin, hedef grubunun t−1 getirisine göre artığı → hedef havuzu. a) 2330.TW → TSM, NVDA, SMH. b) 000660.KS + 005930.KS → MU, WDC, STX. c) 8035.T + ASML.AS → AMAT, LRCX, KLAC. d) 6857.T → TER, NVDA. e) 9984.T → ORCL.
- LL2 (10, lit): lider NVDA, TSM, AVGO, MU, MSFT, GOOGL, META, AMZN; takipçi lider dışı Ç. Lider başına eğim (8). Olay: herhangi bir liderin artık z'si ≥ +2 → al (1); ≤ −2 → uzak dur (1).
- LL3 (3, lit): kendisi hariç eşit ağırlıklı sepet. a) sepetin t getirisi, eğim. b) sepetin 3 günlük getirisi, eğim. c) sepet ≥ +%2 iken sepete göre farkı alt üçte birde olanı al.
- LL4 (7, turev): hedef QQQ + SMH; eğimler: ^TNX değişimi (t), DX-Y.NYB, JPY=X, HG=F (t−1), HYG'nin SPY'a göre artığı (t). BTC-USD → IREN, CIFR, WULF, APLD, CORZ, WGMI (istisna havuz, P2–P3): günlük eğim; Pazartesi olayı (Perşembe barı → Pazar barı ≥ +%5 → al).
- LL5 (2, lit): lider (LL2 listesi + ASML) tepki günü getirisi ≥ +%3 → tepki kapanışında Ç'yi al; ≤ −%3 → uzak dur.
- LL6 (ayrı): 43 öncül × (Ç + T), 1 gün gecikmeli eğim.
- Sepetler: çip {NVDA AMD AVGO MRVL TSM INTC ARM QCOM MPWR}; ekipman {ASML AMAT LRCX KLAC TER ONTO CAMT}; bellek {MU SNDK WDC STX P NTAP}; ağ {ANET CRDO ALAB COHR LITE CIEN AAOI FN}; altyapı {CLS SMCI DELL HPE VRT ETN GEV BE VST CEG OKLO}; yazılım {ORCL PLTR APP MSFT GOOGL META AMZN AAPL TSLA SNOW NOW CRM ADBE}; neocloud {CRWV NBIS IREN CIFR WULF APLD CORZ}.

**B3 — `kod/b3_takvim.py` (13).**
- F7 (4, lit): a) VIX > VIX3M → al. b) VIX günlük ≥ +%20 → al. Ç ve T.
- F11 (2, lit): ^SOX ≤ −%3 → SMH al; ≥ +%3 → SMH al.
- F8 (3, lit, T): a) S−4 kapanışında al, S−1'de sat (S = ayın son işlem günü). b) S'de al, S+3'te sat. c) planlı FOMC karar gününden önceki kapanışta al, karar günü sat.
- F9 (4, lit, Ç; A = duyurudan önceki son kapanış): a) A−3'te al, A'da sat. b) A'da al, tepki günü kapanışında sat. c) tepki günü getirisi ≥ +%5 → al, h=3. d) ≤ −%5 → al, h=1.
- Olay listesi: SMH ≤ −%8 günleri ve sonraki 1/2/3 günlük SMH, SOXL, NVDA getirisi.

## 10. Rejim ve bugünkü durum
1. Her birincil testte hücreler: QQQ 200 günlük ortalamanın üstü/altı; VIX < 15, 15–20, 20–30, ≥ 30.
2. Önceden tanımlı: **STRES** = VIX ≥ 30 (257 gün, 21 epizot). **BUGÜN** = VIX ≥ 30 ve SMH 250 günlük en yüksek kapanışının ≥ %25 altında (57 gün; P3'te 12).
3. Hücrede t ve p yok. Verilen: n_islem, n_gun, n_epizot (arada ≥ 10 işlem günü), ortalama, medyan, isabet, en kötü işlem, epizot yeniden örneklemeli %90 aralık, büzülmüş tahmin = w × hücre + (1−w) × genel α; w = n_epizot/(n_epizot+20).
4. n_epizot < 8 → "yalnız betimsel". Hücre geçme ölçütü değildir.

## 11. Ekonomik çeviri
|t| ≥ 2 olan her alım sinyali için, P3 ve tam dönem ayrı:
1. Tek araçta sermayenin tamamı; havuzda en çok 3 eşzamanlı pozisyon (1/3'er), fazlaysa en uç 3 sinyal.
2. `_ekonomi.csv`: test_id, arac, donem, yillik_islem, piyasada_gun_orani, islem_net_bps, isabet, kazanc_kayip, ybbo_net, oynaklik, sharpe, en_buyuk_dusus, en_kotu_islem, en_kotu_yil, yil_p5, yil_p50, yil_p95, p_zarar_yil, kelly_tam, kelly_ceyrek, al_tut_ybbo, rastgele_p95_ybbo, ybbo_net_50bps.
3. Yıl dağılımı: 20 günlük bloklarla 2.000 yeniden örnekleme. `rastgele_p95`: aynı sıklıkta rastgele giriş, 1.000 tekrar.
4. Kelly f = μ_b / σ²; μ_b = net ortalama × max(0, 1 − 1/t²). Öneri çeyrek Kelly; üst sınır 1× (2× ETF'de 0,5; 3× ETF'de 0,33). f/4 < 0,1 → "ekonomik olarak anlamsız".

## 12. Geçme ölçütü
GEÇTİ (hepsi): (1) n_islem ≥ 100, n_gun ≥ 60; (2) madde 6.2; (3) sınıf maliyetiyle net α > 0 ("uzak dur"da aranmaz); (4) P3'te ve üç dönemin en az ikisinde işaret doğru (n < 50 dönem sayılmaz); (5) en iyi %1 işlem (en az 10) ve en iyi 5 giriş günü çıkınca işaret korunur; (6) t_takvim ≥ 1,5 ve p_perm ≤ 0,05; (7) F1–F4, F10'da T havuzunda işaret aynı (seçim yanlılığına karşı); (8) madde 7.3; (9) bağımsız yeniden kodlamada n_islem ±%1, α ±1 bps.
ADAY: |t| ≥ 2 ve (1), (3), (4). Kalanı KULLANILAMAZ. Son 12 ayda α < 0 ve t < −1 → "soluyor" notu.

## 13. İş bölümü
1. **Adım 0 (B1, önce):** `kod/ortak.py` ve öz sınaması (rastgele sinyalde yanlış alarm ≤ %7; ekilmiş 20 bps kenar geri bulunur). B2 ve B3 sonra başlar, ortak.py'yi değiştirmez. ortak.py yokken başlayan ajan aynı imzalarla `kod/ortak_<ajan>.py` yazar.
2. İmzalar: `fiyat(kod)`, `evren(ad)`, `ileri(kod,h,cikis)`, `artik(kod,h)`, `maliyet(kod)`, `bilanco(kod)`, `fomc()`, `islemler(sinyal,h)`, `test(islemler,**kimlik)`, `rejim(islemler)`, `ekonomi(islemler,arac)`, `kaydet(ajan,satirlar)`, `birlestir()`.
3. Çıktılar `veri/sonuc/`: `<AJAN>_sonuc.csv`, `_islemler.csv` (test_id, kod, giris, cikis, getiri_bps, alfa_bps), `_rejim.csv`, `_ekonomi.csv`, `_tasima.csv`; ayrıca `B1_1530.csv`, `B2_tarama.csv`, `B3_olaylar.csv`.
4. `_sonuc.csv` sütunları: test_id, ajan, aile, varyant, birincil, kaynak, evren, h, cikis, getiri_turu, n_islem, n_gun, n_arac, ilk_tarih, son_tarih, ort_bps, kosulsuz_bps, alfa_bps, se_bps, t_kume, p_kume, egim_bps, t_egim, p_birincil, t_takvim, p_perm, mde_bps, maliyet_bps, alfa_net_bps, alfa_net_2x_bps, mutlak_net_bps, medyan_bps, isabet, alfa_ust1suz_bps, alfa_5gunsuz_bps, alfa_h2_bps, alfa_h3_bps, alfa_acilis_bps, alfa_/t_/n_ × P1, P2, P3, alfa_son12, n_son12, alfa_temiz, q_bh, etiket, not.
5. test_id örneği: `F1a_C_h1`. `q_bh` ve `etiket` yalnız `birlestir()` ile doldurulur.
6. Ajan dönüşü: koşulan birincil test sayısı, GÜÇSÜZ sayısı, her sapma.
