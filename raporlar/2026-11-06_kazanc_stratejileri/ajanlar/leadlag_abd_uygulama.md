# ABD Tier A lead-lag haritası, isim isim: BDX, EHC, TW, ACGL, MAR (kısaca TMO, RPRX, CME, MRSH, HLT, SN)

_Hazırlanma: Pazar 08.11.2026. Kapsam: `uygulama/NET_LISTE_ABD.md` (NL) §1'deki Tier A ve yedekleri._

**Veri ve kod**
- Veri: Ken French 49 sektör günlük VW ve FF3 günlük (CRSP 202609, son gün **30.09.2026**), FRED DGS10 ve DCOILWTICO, CBOE VIX.
- Yahoo ve Stooq kullanılmadı. Bu yüzden ABD'de **tek hisse fiyat serisi yok**: bütün testler sektör portföyü düzeyinde.
- Kod: `hesaplar/leadlag_uygulama/abd/`. İçinde `ortak.py`, `t01_endustri_leadlag.py`, `t02_saglamlik_sezon.py`, `tv_kod_kontrol.py`, `ll_z_filtre.pine` ve `ABD_TierA_izleme.txt` var.
- Sonuç tabloları `abd/cikti/` altında. Ham veri scratchpad'de: `data/leadlag2/abd/`.

**Kısaltmalar ve etiketler**
- Kaynak işaretleri: [H] bu dosyanın hesabı, [L] literatür, [Ö] öneri (plan kuralı değil). PLAN = `uygulama/PLAN_ABD.md`.
- **KENAR:** test edildi, bu kullanıcının zamanlamasında maliyetten sonra yaşıyor.
- **FILTRE:** gerçek ilişki ama tek başına kenar değil; sıralama, zamanlama ya da kaçınma için kullanılır.
- **RISK:** yalnız gap ya da risk bilgisi.
- **YOK:** test edildi, bir şey çıkmadı.
- **TEST EDİLMEDİ:** veri ya da kanıt yok.

**TradingView kodları:** Bu dosyadaki her kod iki yoldan biriyle doğrulandı:
- `2026-11-02_viop_leadlag/tradingview_kodlari.csv` içinde var (CSV), ya da
- 07.11.2026'da TradingView sembol sayfası varsayılan istekle okundu (`cikti/tv_kod_kontrol.csv`; 200 ve başlıkta aynı kod).

Oran grafiği sözdizimi: sembol kutusuna `PAY/PAYDA` yazılır, örneğin `NYSE:BDX/AMEX:IHI`.

---

## 0. Hüküm

1. **ABD Tier A için KENAR yok [H].**
   - Önceden yazılmış 150 sektör testinin hiçbiri BH-FDR'den (q 0,10) geçmedi. En düşük q: kapanış-kapanışta 0,24, bir gün atlamalı testte 0,31.
   - |t| ≥ 1,96 olan test sayısı 12. Şansla beklenen 7,5.
2. **Geniş taramada (1.320 test) FDR'den 4 test geçti [H].** Hepsi FF49 Fin sektörünün ertesi gününe ait (h = 1): Insur −, Food −, Paper −, Hardw +.
   - Bir gün atlanınca hepsi sıfıra iniyor (q ≥ 0,60).
   - OOS'ta uygun kuyruğun ortalaması 1–9 bps. Bu rakam t+1 gecesinin de kazanıldığı varsayımıyla bile 10 bps maliyetin altında.
   - TW ve CME için hüküm: **YOK**.
3. **Tek kullanılabilir ilişki: hastaneler → medtech (BDX) [H].**
   - Tanım: Hlth sektörünün 5 günlük piyasa artığı, MedEq'in sonraki 3–5 gününü öngörüyor.
   - Önceden yazılmış bir müşteri→tedarikçi testi. t 2,82 (bir gün atlamalı 2,38).
   - IS ve OOS aynı işarette; 17 yılın 14'ünde pozitif; komşu parametrelerde (L 3–5, h 3–5) aynı sonuç.
   - FDR'den geçmiyor (q 0,24 / 0,43). Etki yalnız z > +1 kuyruğunda: 5 günde +25 bps artık getiri (IS +30, OOS +18).
   - 20 bps maliyetle OOS net ≈ −2 bps. Etiket **FILTRE**: sağlık kümesinde BDX'e öncelik verir, giriş sinyali değildir.
4. **Kasırga sezonu (Ağu–Eki) FF49 Insur'da görünmüyor [H].** Fark +1,7 bps/gün, t 0,75. Etiket **YOK**. Ama vekil kötü: içinde BRK, UNH, PGR ve hayat sigortacıları var. ACGL'nin afet riski bu yüzden ayrıca **RISK** etiketiyle duruyor.
5. **Piyasa, büyük-küçük ve VIX hiçbir hedef sektöre öncülük etmiyor [H].** MKT, SMB, ΔVIX ve sektörün kendi geçmişi için etiket **YOK**.
6. **Hisseye özgü kanallar TEST EDİLMEDİ.** Hisse ve olay verisi yok. Kanallar:
   - emsal bilanço okuması,
   - TW/CME ↔ MOVE ve VIX,
   - ACGL ↔ afet ve reasürans fiyatı,
   - MAR/HLT ↔ RevPAR ve TSA,
   - EHC ↔ CMS kuralları.
   Etiketleri mekanizmaya ve literatüre göre verildi: FILTRE ya da RISK (§3).
7. **Kod düzeltmesi:** Hilton'un kodu `NASDAQ:HLT`. `NYSE:HLT` TradingView'de 404 veriyor.
   - NL'deki `NASDAQ:MAR/NYSE:HLT` ve `NYSE:HLT/AMEX:XRT` yanlış.
   - NL'de "teyit et" yazan şu kodların sayfası artık okundu: `NYSE:BDX`, `NYSE:EHC`, `NASDAQ:TW`, `NASDAQ:ACGL`, `NYSE:TMO`, `NASDAQ:RPRX`, `NASDAQ:CME`, `NYSE:MRSH`, `NYSE:SN`, `AMEX:XLV`, `AMEX:IHI`, `AMEX:IHF`, `CBOE:VIX3M`, `INDEX:S5FI`, `INDEX:S5TH`, `NASDAQ:NDX`, `AMEX:SPY`.
   - `NYSE:SEM` ve `NASDAQ:SEM` sayfası yok; kullanılmadı.
8. **Pratik sonuç.** ABD tarafında lead-lag bu kullanıcı için üç işe yarar:
   - (a) BDX önceliği,
   - (b) olay takvimi (emsal bilanço, CMS, aylık hacim raporları, afet),
   - (c) PLAN'ın rejim anahtarı.
   Rejim KIRMIZI ya da TURUNCU iken bunların hiçbiri işlem açtırmaz (PLAN §2.2). Bugünkü durum KIRMIZI; ilk pilot en erken Pt 16.11, 16:45–17:15 TSİ.

---

## 1. Yöntem [H]

### 1.1 Sektör eşlemesi (FF49 tanımları Ken French `Siccodes49` dosyasından okundu)

| İsim | SIC (EDGAR'dan bu oturumda teyit edilmedi) | FF49 | Gerekçe ve vekil kalitesi |
|---|---|---|---|
| BDX | 3841 | **MedEq** (3840–3849) | İyi: ISRG, SYK, BSX, MDT, EW, BDX |
| TMO | 3826 | **LabEq** (3826 "Lab analytical"); MedEq değil | Orta: DHR, A, WAT, MTD ve endüstriyel ölçüm şirketleri |
| EHC | 8060 | **Hlth** (8000–8099) | İyi: HCA, UHS, THC, LH, DGX, DVA, EHC. Yönetilen sağlık (UNH, ELV, CI; SIC 6324) burada değil, Insur'da |
| TW, CME | 6211 / 6200 | **Fin** (6200–6299) | Zayıf: GS, MS, SCHW, BX, KKR, ICE, CME. Ayrıca **REIT'ler (6798) de Fin'de** |
| ACGL | 6331 | **Insur** | Zayıf: BRK, UNH/ELV/CI, PGR, CB, hayat sigortacıları. Reasürans payı küçük |
| MRSH | 6411 | **Insur** | Aynı |
| MAR, HLT | 7011 | **Meals** (7010–7019) | Orta: restoranlar (MCD, SBUX, CMG), oteller ve 7011'deki kumarhaneler |
| RPRX | 6794 (teyit et) | SIC'e göre **Fin** (6794 "patent sahipleri"). Ekonomik olarak **Drugs** ile test edildi | Zayıf |
| SN | 3634 | **Hshld** (3630–3639); ElcEq değil | Zayıf: ağırlık PG, CL, KMB'de |

### 1.2 Tasarım (sonuçlara bakmadan yazıldı; `t01_endustri_leadlag.py` başlığı)

- **Hedef:** hedef sektörün piyasa artığı, y = Σ (r − β_t · MKT).
  - β_t 252 günlük kayan betadır; t dahil, yani t'de bilinir.
  - Toplam t+1..t+h üzerinden alınır; bps cinsinden.
- **Sinyal:** öngörücünün t'de bilinen L günlük değeri.
  - Öngörücü bir sektörse onun piyasa artığı kullanılır; böylece yalnız sektöre özgü bilgi kalır.
  - 252 günlük kayan z-skoru alınır.
- **(L, h) kombinasyonları:** (1,1), (1,3), (5,5).
- **Ortak öngörücüler (her hedefte):** MKT, SMB (büyük-küçük), kendi artığı, ΔVIX.

**Ekonomik bağ öngörücüleri:**

| Hedef | Öngörücüler | Mekanizma |
|---|---|---|
| MedEq | Hlth, Drugs, LabEq | Hastane prosedür hacmi (müşteri→tedarikçi; Menzly–Ozbas 2010, Cohen–Frazzini 2008 [L]) |
| Hlth | Insur, MedEq | Ödeyici: yönetilen sağlıkta "yüksek kullanım" haberi sağlayıcının lehine, ödeyicinin aleyhine |
| Fin | Banks, \|ΔDGS10\| | Faiz oynaklığı → işlem hacmi (MOVE vekili; MOVE izinli kaynaklarda yok) |
| Insur | ΔDGS10, Fin | Yatırım geliri, finansal sektör bilgisi |
| Meals | Trans, Rtail, ΔWTI | Seyahat talebi (havayolu), tüketici, yakıt |
| LabEq | Drugs, MedEq | İlaç ve biyotek Ar-Ge harcaması (müşteri) |
| Drugs | Hlth, Insur, ΔDGS10 | Ödeyici politikası; RPRX'in duration'ı |
| Hshld | Rtail | Perakendeci müşteriler |

**Zamanlama:**
- Sinyal ABD kapanışında (t) bilinir, yani TSİ t+1 günü 00:00'da. Kullanıcının ilk emri t+1'de 16:45–17:15 TSİ, işlem ABD açılışında.
- **Varyant A** (t+1..t+h kapanış-kapanış) üst sınırdır, çünkü t+1 gecesini de sayar.
- **Varyant B** (t+2..t+h+1) t+1'i tamamen atlar; muhafazakârdır.
- Açılış fiyatı yok. Gerçek getiri (t+1 açılışından t+h kapanışına) ikisinin arasında kalır.
- BIST bulgusunun aynısı burada da geçerli: piyasa geneli bilgi büyük ölçüde açılışta fiyatlanıyor (`2026-11-02_viop_leadlag/RAPOR.md` §2–3).

**İstatistik:**
- OLS ve Newey-West HAC (lag = h + L, B'de +1). BH-FDR aile içinde.
- IS 2010–2020, OOS 2021–09/2026; yaklaşık 4.200 gün.
- **İşlem kontrolü:** Yön IS eğiminin işaretinden alınır. OOS'ta z uygun yönde 1'i aşınca h gün long tutulur. Artık getiriden 10 ve 20 bps gidiş-dönüş maliyeti düşülür.
  - Maliyet varsayımı: IBKR'de büyük hisse, limit emirle ~10 bps. Stop kayması dahil ~20 bps (PLAN §6.4: kayma tek yönde %0,05–0,15).
  - Yüzdesel komisyon alan bir Türk kurumunda maliyet daha yüksek.

---

## 2. Sonuçlar [H]

### 2.1 Birincil aile (150 test): her hedefte en güçlü test

| Hedef (isim) | Test | En güçlü (L,h) | b (bps/σ) | t (A) | q (A) | IS t / OOS t (A) | t (B) | Etiket |
|---|---|---|---|---|---|---|---|---|
| MedEq (BDX) | 21 | **Hlth (5,5)** | +11,4 | 2,82 | 0,24 | 1,95 / 2,02 | 2,38 | **FILTRE** (§2.3) |
| Hlth (EHC) | 18 | MKT (1,1) | +3,4 | 2,15 | 0,55 | 2,19 / 0,59 | 0,42 | YOK |
| Fin (TW, CME) | 18 | SMB (5,5) | +8,2 | 2,17 | 0,55 | 1,53 / 1,65 | 2,03 | YOK |
| Insur (ACGL, MRSH) | 18 | kendi (5,5) | −10,9 | −2,54 | 0,42 | −2,52 / −1,03 | −2,65 | YOK |
| Meals (MAR, HLT) | 21 | Trans (1,3) | +3,8 | 2,02 | 0,55 | 1,05 / 1,99 | 0,61 | YOK (t+1'de fiyatlanıyor) |
| LabEq (TMO) | 18 | MKT (5,5) | −11,5 | −2,89 | 0,24 | −2,54 / −1,55 | −2,27 | YOK |
| Drugs (RPRX) | 21 | kendi (1,1) | +3,9 | 3,07 | 0,24 | 2,60 / 1,75 | −0,05 | YOK (yalnız ertesi gün) |
| Hshld (SN) | 15 | kendi (5,5) | −11,6 | −2,01 | 0,55 | −1,75 / −0,99 | −1,35 | YOK |

- **Kalan bağ testlerinin hepsinde, her (L,h) için A ve B'de |t| < 2:** MedEq ← Drugs/LabEq; Hlth ← Insur/MedEq; Fin ← Banks/\|ΔDGS10\|/ΔVIX; Insur ← ΔDGS10/Fin; Meals ← Rtail/ΔWTI; LabEq ← Drugs/MedEq; Drugs ← Hlth/Insur/ΔDGS10; Hshld ← Rtail. Tablo: `cikti/t01_birincil.csv`.
- **İşlem kuralı taraması (OOS, B, 20 bps sonrası > 0 ve t ≥ 1,96):** 150 testte 1 tane çıktı (Hshld ← SMB). Regresyonu anlamsız (t −1,1), yani gürültü.

### 2.2 Geniş tarama (1.320 test: 48 diğer sektör ve 7 faktör/makro × 8 hedef × 3 kombinasyon)

- **A:** 4 test FDR'den geçti. Hepsi Fin hedefinde ve ertesi güne ait: Insur (t −4,30), Hardw (+4,19), Food (−3,72), Paper (h 3, −3,66).
  - Okuma: Fin portföyü (broker, varlık yöneticisi ve REIT) büyüme/savunma eksenindeki günlük harekete bir gün geç uyuyor.
  - B'de hepsi kayboluyor (en düşük q 0,60). OOS uygun kuyruk 1–9 bps; 10 bps maliyetle net −1 ile −9 bps. **YOK.**
- **|t| ≥ 1,96:** A'da 92 test (şansla beklenen 66), B'de 84.
- **IS ve OOS'ta aynı işaretle ikisi de anlamlı:** A'da 8, B'de 1 (Meals ← Autos; 20 bps sonrası net −10 bps).
- **OOS kuyruk kuralı (20 bps sonrası > 0, t ≥ 1,96):** 29 test. Şansla beklenen yaklaşık 33 (tek yön %2,5). Gürültü. Tablo: `cikti/t01_kesif.csv`.

### 2.3 MedEq ← Hlth ayrıntısı (`t02_saglamlik_sezon.py`; komşu parametreler sonradan bakıldı)

| (L,h), varyant B | t tam | t IS | t OOS |
|---|---|---|---|
| (3,3) | 2,06 | 1,72 | 1,17 |
| (3,5) | 2,66 | 1,79 | 1,99 |
| (5,3) | 2,69 | 1,80 | 1,99 |
| **(5,5)** | **2,38** | 1,05 | **2,33** |
| (5,10) / (10,5) | 0,97 / 1,02 | −0,2 | 1,69 |
| (10,10) / (20,10) | −0,23 / −0,72 | — | — |

- **Ufuk:** Etki 3–5 günlük sinyal ve 3–5 günlük ufukta. 10 günde kayboluyor. Bu, S1/S2'nin "ilk 3–4 seans" penceresiyle örtüşüyor.
- **Yıllar:** 17 yılın 14'ünde eğim pozitif. Negatif yıllar: 2016, 2017, 2018.

**Kuyruklar (B, 5 günlük MedEq artığı, bps):**

| Dönem | z < −1 | orta | z > +1 |
|---|---|---|---|
| Tam (n 581 / 3.012 / 612) | −5,7 | −7,3 | **+25,0** |
| IS 2010–20 | +8,3 | +3,0 | +29,6 |
| OOS 2021–26 | −26,9 | −29,0 | +17,5 |

- **Asimetri:** z < −1 kuyruğu ortadan farklı değil. Yani bu ilişki bir **kaçınma** sinyali değil, bir **öncelik** sinyali.
- **Net (z > +1 kuyruğu):**
  - OOS: +17,5 − 10 = +7,5 bps; 20 bps maliyetle −2,5 bps.
  - IS: 20 bps maliyetle +9,6 bps.
- **Hisseye çeviri:** Bu sonuçlar sektör portföyüne ait. BDX'in MedEq artığına duyarlılığı 1'in altında ve hisseye özgü gürültüsü büyük, bu yüzden hissede etki daha küçük ve daha gürültülü olur.
- **Hüküm: FILTRE.**

### 2.4 Sigorta sezonu (önceden yazılmış tek test)

- FF49 Insur artığı, 2010–09/2026, günlük ortalamalar: Ağu–Eki +1,65 bps, Kas–Oca −0,47 bps, Şub–Tem +0,16 bps.
- Ağu–Eki farkı +1,69 bps/gün (HAC t 0,75). IS t 0,30, OOS t 0,70.
- Ağu–Eki kümülatif artığı 17 yılın 8'inde pozitif. 2017'de (Harvey, Irma, Maria) +163 bps.
- **YOK** (sektör düzeyinde). ACGL'ye özgü afet etkisi: TEST EDİLMEDİ.

---

## 3. İsim kartları

Her kartın sırası aynı: ilişki tablosu, TradingView teyit seti, işlem usulü. Giriş, stop, boyut ve çıkış PLAN ile NL §1'deki ortak emir kartından gelir; bu dosya onlara yalnız **öncelik, erteleme ve risk** notu ekler.

### 3.1 BDX · `NYSE:BDX` · sağlık süper-kümesi (K1 medtech) · FF49 MedEq

| İlişki | Mekanizma | TV kodu | Kanıt | Etiket | Kullanım (TSİ) |
|---|---|---|---|---|---|
| Hastanelerin 5 günlük piyasa artığı → BDX'in sonraki 3–5 günü | Prosedür hacmi; müşteri→tedarikçi yayılımı | `NYSE:HCA` grafiğinde `LL_z` (L 5, payda `SP:SPX`). İkinci kontrol: `NYSE:UHS` | §2.3: sektörde t 2,4–2,8, FDR yok, OOS 20 bps'te ≈ 0 | **FILTRE** | 00:30–01:00 ya da 08:00–09:00 bloğunda oku. BDX'te S1/S2 hazır **ve** LL_z(HCA) > +1 ise sağlık kümesinin tek hakkını BDX'e ver (EHC ve TMO yerine) [Ö]. LL_z ≤ +1 ise PLAN §4.4 #6 sırası geçerli. Tek başına giriş sebebi değil |
| Medtech emsal bilançosu: MDT 24.11 BMO | Sektör içi bilgi aktarımı (Foster 1981 [L]). Thomas–Zhang (2008, JAR) [L]: geç açıklayanın emsal haberine tepkisi kendi açıklamasında kısmen geri dönüyor | `NYSE:MDT`, `NYSE:BDX/NYSE:MDT` | Hisse verisi yok | **RISK** (24.11 açılış gap'i) | Açık BDX varsa 23.11 kapanış bloğunda gap-ayarlı ısıya bak (NL §4c). 24.11 sabahına yeni S1 tetiği koyma; MDT tepkisinden sonraki seansa bırak [Ö] |
| Diğer medtech bilançoları (SYK, BSX, ISRG, EW; Ocak sonu) | Aynı | `NYSE:SYK`, `NYSE:BSX`, `NASDAQ:ISRG`, `NYSE:EW` | — | **RISK** | Ocak takvimine yaz. BDX'in kendi bilançosu Oca sonu–Şub 2027 (IR'den teyit et) |
| MedEq ← Drugs, LabEq, MKT, SMB, ΔVIX, kendi geçmişi | — | — | §2.1: \|t\| < 2,1, FDR yok | **YOK** | Kullanma |
| Güçlü dolar → çevrim kaybı | Yurt dışı gelir | `TVC:DXY` | Test ailesine alınmadı | **TEST EDİLMEDİ** / RISK | Yalnız çeyrek rehberi bağlamı |

**TradingView teyit seti:**
- `NYSE:BDX/AMEX:IHI` ve `AMEX:IHI/SP:SPX`: ikisi de 50 GHO'nun üstünde olmalı (NL).
- `NYSE:BDX/SP:SPX`: ABD_RJ'nin RS / 52H satırı. S1 için ≥ 0,97, S2 için ≥ 0,95.
- `NYSE:HCA` grafiğine `LL_z` eklenir.

### 3.2 EHC · `NYSE:EHC` · sağlık süper-kümesi (K3 hizmet) · FF49 Hlth

| İlişki | Mekanizma | TV kodu | Kanıt | Etiket | Kullanım |
|---|---|---|---|---|---|
| Ödeyici → sağlayıcı (yönetilen sağlık haberi, ters işaret beklenir) | Payer'ın "kullanım yüksek" haberi sağlayıcının lehine | `NYSE:UNH` | Hlth ← Insur: \|t\| ≤ 1,4 (A ve B) | **YOK** (günlük) | UNH/ELV/CI bilanço günleri olay günüdür: **RISK** |
| Hlth ← MedEq, MKT, SMB, ΔVIX, kendi geçmişi | — | — | En iyisi MKT (1,1): t 2,15, OOS 0,59 | **YOK** | — |
| Hastane emsal bilançoları (HCA, UHS, THC; Oca sonu–Şub) | Hacim ve payer karması | `NYSE:HCA`, `NYSE:UHS`, `NYSE:THC` | Hisse verisi yok | **RISK** / FILTRE | Bilanço haftasında yeni giriş ertele [Ö] |
| CMS IRF PPS kuralları (taslak genelde Nisan, nihai Temmuz sonu–Ağustos başı) ve Medicare Advantage oran duyuruları | Fiyat kararı | — (TV'de yok) | — | **RISK** (ikili olay, PLAN §3.1) | Tarihleri IR'den ve CMS'ten al. Olaydan önceki 10 seansta giriş yok |
| Hastaneler güçlüyken EHC | EHC zaten Hlth'in içinde. §2.3'teki filtre **BDX'i** öne alır, EHC'yi değil | — | — | — | LL_z(HCA) > +1 ise sağlık hakkı BDX'e, değilse RS sırası |

**TradingView teyit seti:**
- **Asıl ölçüt** `NYSE:EHC/NYSE:HCA` ve `NYSE:EHC/AMEX:XLV`.
- NL'deki `NYSE:EHC/AMEX:IHF` dikkatli kullanılmalı: IHF'nin en büyük payları yönetilen sağlıkta (UNH ve diğerleri; teyit et), yani IHF EHC'nin emsali değil.
- `AMEX:XLV/SP:SPX`.

### 3.3 TW · `NASDAQ:TW` · K4 borsalar · FF49 Fin

| İlişki | Mekanizma | TV kodu | Kanıt | Etiket | Kullanım |
|---|---|---|---|---|---|
| Faiz oynaklığı → hacim → TW | Gelir ≈ hacim × ücret | `TVC:MOVE` (CSV), vekil `TVC:US10Y` | Sektörde Fin ← \|ΔDGS10\| ve ΔVIX: \|t\| ≤ 1,4. MOVE izinli kaynaklarda yok. Hissede TEST EDİLMEDİ | **FILTRE** (yalnız bağlam) | MOVE'un 50 GHO'nun üstünde olması çeyrek hacmini destekler. MOVE ve VIX çökerken TW ve CBOE geride kalabilir (PLAN §4.2). Günlük giriş sinyali değil |
| Aylık hacim raporu (TW, MKTX, ICE, CME; ayın ilk iş günleri) | Hacim sürprizi | `NASDAQ:TW`, `NASDAQ:MKTX`, `NYSE:ICE`, `NASDAQ:CME` | — | **RISK** (1 günlük gap) / FILTRE | Rapor gününden önceki kapanışta yeni S1 tetiği koyma [Ö]. Aralık tarihleri IR'den |
| Fin'in ertesi günü ← büyüme/savunma ekseni (tarama) | Portföy kirli (broker + REIT) | — | §2.2: A'da FDR geçiyor, B'de 0; maliyetin altında | **YOK** | — |
| Fin ← Banks, MKT, SMB, kendi geçmişi | — | — | §2.1 | **YOK** | — |

**TradingView teyit seti:**
- `NASDAQ:TW/AMEX:XLF` (NL).
- Küme ölçütü olarak daha uygun: `NASDAQ:TW/AMEX:IAI` (broker-dealer ve borsa ETF'i) ve `AMEX:IAI/SP:SPX`.
- Küme içi: `NASDAQ:TW/NASDAQ:MKTX`.
- Bağlam: `TVC:MOVE`, `TVC:US02Y`, `CBOT:ZN1!`.

### 3.4 ACGL · `NASDAQ:ACGL` · K5 sigorta · FF49 Insur

| İlişki | Mekanizma | TV kodu | Kanıt | Etiket | Kullanım |
|---|---|---|---|---|---|
| Kasırga sezonu (1.6–30.11, zirve Ağu–Eki) | Afet zararı belirsizliği | — | Sektörde YOK (§2.4). ACGL'de TEST EDİLMEDİ | **YOK** (sektör) / **RISK** (hisse) | Sezon 30.11'de bitiyor; risk azalan tarafta |
| Büyük afet olayı (kasırga, deprem, yangın) | Zarar tahmini; ilk tepki gap'tir | — | — | **RISK** | NL §1: ikili olay say. Haberden sonraki ilk seans yeni giriş yok; açık pozisyonda gap-ayarlı ısı |
| 1 Ocak reasürans yenilemeleri, fiyat yorumları (Aralık) ve Ocak ROL endeksleri | Fiyat yumuşarsa çarpan daralır | — | — | **FILTRE** / TEST EDİLMEDİ | Aralık'ta broker ve reasürör yorumlarını oku; yumuşama varsa K5'te boyut küçült [Ö] |
| Emsal bilanço: BRK-B 07.11 (ilk tepki Pt 9.11) | P&C ve reasürans okuması | `NYSE:BRK.B` | — | **RISK** / FILTRE | NL: 9.11 tepkisini K5 notu olarak yaz |
| Insur ← ΔDGS10, Fin, ΔVIX, MKT, SMB; kendi 5 günlük dönüşü | — | — | §2.1: kendi (5,5) IS −2,5, OOS −1,0 | **YOK** | — |

**TradingView teyit seti:**
- `NASDAQ:ACGL/AMEX:XLF` (NL).
- Daha uygun ölçütler: `NASDAQ:ACGL/AMEX:KIE` ve `NASDAQ:ACGL/NASDAQ:KBWP` (P&C).
- Reasürans içi: `NASDAQ:ACGL/NYSE:RNR`.
- Emsaller: `NYSE:EG`, `NYSE:CB`, `NYSE:TRV`; ipotek sigortası `NYSE:MTG`.

### 3.5 MAR · `NASDAQ:MAR` · K8 konaklama · FF49 Meals

| İlişki | Mekanizma | TV kodu | Kanıt | Etiket | Kullanım |
|---|---|---|---|---|---|
| Havayolu ve seyahat → otel | Seyahat talebi | `NYSE:DAL` (CSV), `AMEX:JETS` (CSV) | Meals ← Trans (1,3): A'da t 2,02, B'de 0,61. Bilgi t+1'de fiyatlanıyor | **YOK** (işlenebilir değil) / RISK | Yalnız ertesi açılış beklentisi |
| RevPAR (STR/CoStar haftalık ABD otel verisi), TSA yolcu sayıları | Doğrudan gelir göstergesi | TV'de yok | — | **TEST EDİLMEDİ** / FILTRE (bağlam) | Haftalık okuma; zayıf RevPAR haftasında yeni giriş ertele [Ö] |
| Tüketici emsalleri: HD 17.11; TGT, TJX, LOW 18.11; WMT 19.11 BMO | Tüketici talebi | `NYSE:TGT`, `NASDAQ:WMT` | — | **RISK** | PLAN: 17.11 genel yasak; 18.11 kuralı |
| Online seyahat ve havayolu bilançoları (DAL Oca ortası; BKNG, EXPE, ABNB Şubat) | Talep okuması | `NASDAQ:BKNG`, `NASDAQ:EXPE`, `NASDAQ:ABNB` | — | **RISK** | Takvim |
| Meals ← Rtail, ΔWTI, MKT, SMB, kendi geçmişi | — | `TVC:USOIL` | §2.1 | **YOK** | — |

**TradingView teyit seti:**
- `NASDAQ:MAR/AMEX:XRT` (NL).
- Daha uygun ölçüt: `NASDAQ:MAR/AMEX:PEJ` (eğlence ve seyahat ETF'i) ve `AMEX:PEJ/SP:SPX`.
- Küme içi: `NASDAQ:MAR/NASDAQ:HLT` (kod düzeltildi).
- Emsaller: `NYSE:H`, `NYSE:IHG`, `NYSE:WH`.
- PLAN kuralı: tetik FTD ya da S&P 10 > 20.

### 3.6 Yedekler (kısa)

| İsim · FF49 | Test edilen (sektör) | Hisseye özgü kanal ve etiket | TV teyit seti |
|---|---|---|---|
| **TMO** `NYSE:TMO` · LabEq | LabEq ← Drugs, MedEq: YOK. LabEq ← MKT (5,5) t −2,9 (OOS −1,6): YOK | Emsal bilançolar (`NYSE:DHR`, `NYSE:A`, `NYSE:WAT`, `NYSE:MTD`, `NYSE:IQV`; Ocak sonu): RISK. Biyotek fonlaması `AMEX:XBI`, NIH bütçesi, Çin: FILTRE, TEST EDİLMEDİ | `NYSE:TMO/AMEX:XLV`, `NYSE:TMO/NYSE:DHR`, `AMEX:XBI/SP:SPX` |
| **RPRX** `NASDAQ:RPRX` · SIC'e göre Fin, ekonomik olarak Drugs | Drugs ← ΔDGS10, Hlth, Insur: YOK. Kendi (1,1) t 3,07 ama B'de 0: YOK | Uzun vadeli telif nakit akışı → `TVC:US10Y`: FILTRE (bağlam), TEST EDİLMEDİ. Ortak ilaçlarının klinik ve onay haberleri (ör. `NASDAQ:VRTX`): RISK | `NASDAQ:RPRX/AMEX:XLV`, `NASDAQ:RPRX/NASDAQ:IBB` |
| **CME** `NASDAQ:CME` · Fin | TW ile aynı: YOK | ADV ↔ oynaklık (`CBOE:VIX`, `TVC:MOVE`, `CME:SR31!`, `CBOT:ZN1!`): FILTRE (bağlam). Aylık ADV raporu (ayın ilk iş günleri; IR): RISK | `NASDAQ:CME/AMEX:IAI`, `NASDAQ:CME/NYSE:ICE`, `NASDAQ:CME/AMEX:XLF` |
| **MRSH** `NYSE:MRSH` · Insur | Insur testleri: YOK | P&C fiyat döngüsü yumuşarsa broker'ın organik büyümesi düşer: FILTRE, TEST EDİLMEDİ. Emsal bilançolar (`NYSE:AON`, `NYSE:AJG`, `NASDAQ:WTW`, `NYSE:BRO`): RISK | `NYSE:MRSH/AMEX:KIE`, `NYSE:MRSH/NYSE:AON`, `NYSE:MRSH/AMEX:XLF` |
| **HLT** `NASDAQ:HLT` · Meals | MAR ile aynı: YOK | MAR ile aynı | `NASDAQ:HLT/AMEX:PEJ`, `NASDAQ:HLT/NASDAQ:MAR` |
| **SN** `NYSE:SN` · Hshld | Hshld ← Rtail: YOK. Kendi (5,5): YOK | Müşteri bilançoları (TGT 18.11, WMT 19.11 BMO, `NYSE:BBY` 24.11 BMO, `NASDAQ:AMZN`): RISK ve olay FILTRE'si (müşteri momentumu aylık; Cohen–Frazzini [L]). Tarife (Çin ve Vietnam üretimi): RISK | `NYSE:SN/AMEX:XLY`, `NYSE:SN/AMEX:XRT`; emsaller `NYSE:WHR`, `NASDAQ:HELE` |

---

## 4. TradingView kurulumu ve günlük akış

### 4.1 Rejim göstergesi (PLAN §2.1–2.2 ve §2.7; değişiklik yok)

- `SP:SPX` günlük grafiğine `ABD_RJ` eklenir (`uygulama/kod/abd_rejim_ve_sablon.pine`). Betik derlenmedi; ilk kullanımda 05.11 değerleriyle karşılaştır.
- **KIRMIZI:** herhangi biri yeter:
  - `CBOE:VIX/CBOE:VIX3M` son iki kapanıştan birinde ≥ 1,00,
  - `SP:SPX` 2 kapanış üst üste 200 GHO'nun altında,
  - `INDEX:S5FI` < 50 **ve** `INDEX:S5TH` < 60.
- **SARI:** şu şartlar 3 kapanış üst üste sağlanmalı: KIRMIZI değil, S&P > 200 GHO ve tetik (FTD ya da S&P 10 > 20).
  - `NASDAQ:NDX` 10 > 20 tek başına yalnız K9'u açar.
  - Yakın bölge (S&P / 200 GHO < 1,02): en çok 1 açık pozisyon.
- **YEŞİL:** SARI şartlarına ek olarak S&P > 50 GHO, NDX 10 > 20 ve ikisi de yükseliyor, VIX/VIX3M < 0,95, S5FI ≥ 50 ve FTD sağlam.
- **Gece vadelileri** (`CME_MINI:ES1!`, `CME_MINI:NQ1!`) yalnız gap ve risk bilgisi verir. CPI (10.11) ve PPI (13.11) günlerinde vadeli 16:45'te ±%1,5'ten fazla oynadıysa o gün yeni giriş yok.

### 4.2 `LL_z` filtresi (`hesaplar/leadlag_uygulama/abd/ll_z_filtre.pine`; **derlenmedi, test edilmedi**)

- **Ne hesaplar:** Öncü sembolün günlük log getirisinden 252 günlük kayan betayla piyasa payı çıkarılır. Kalan artık L gün toplanır ve 252 günlük z-skoruna çevrilir. Bu, `t01`'deki sinyalin hisse vekili.
- **Kullanım:** BDX için öncü `NYSE:HCA`, L = 5. HCA, Hlth içindeki en büyük şirket [Ö]. Sektör portföyü yerine tek hisse kullanıldığı için sinyal daha gürültülü.
- **Okuma:** z > +1 (yeşil sütun) → sonraki 3–5 seansta BDX lehine öncelik. Diğer durumlarda bilgi yok.

### 4.3 İzleme listesi

- `hesaplar/leadlag_uygulama/abd/ABD_TierA_izleme.txt` TradingView'deki "Listeyi içe aktar" biçiminde.
- Bölümler: REJIM, BDX, EHC, TW, ACGL, MAR, YEDEK.
- Oran grafikleri listede yok. Grafikte sembol kutusuna §3'teki gibi aynen yazılır.

### 4.4 Akış (TSİ)

| Saat | İş |
|---|---|
| 00:30–01:00 ya da 08:00–09:00 | ABD_RJ durumu. `LL_z(HCA)` oku. Emsal ve olay takvimini kontrol et: MDT 24.11, tüketici günleri 17–19.11, aylık hacim raporları, CMS, afet haberleri |
| 16:45–17:15 | PLAN emirleri. Lead-lag bilgisi yalnız iki karar için kullanılır: sağlık kümesinde BDX önceliği ve olay günü ertelemesi |
| 17:30–00:00 | Emir değişikliği yok (PLAN kritik ihlal) |

---

## 5. Sınırlar ve dürüstlük notları

- **Hisse düzeyi yok.** Tek hisse ABD fiyatı izinli kaynaklarda yok. "TEST EDİLMEDİ" etiketlerinin hepsi bu yüzden. Sektör portföyünde bulunan etki hissede daha zayıf olur.
- **Açılış fiyatı yok.** A üst sınır, B muhafazakâr. Kullanıcının gerçek getirisi ikisinin arasında.
- **Veri 30.09.2026'da bitiyor.** Ekim–Kasım 2026 çöküşü örneklemde yok.
- **Vekil kirlenmesi.** FF49 Fin'de REIT'ler, Insur'da UNH ve BRK var. TW, CME, ACGL ve MRSH için sektör testleri zayıf vekil üzerinde.
- **Çoklu test.** Toplam 1.471 test yapıldı. "Aday" sözü yalnız MedEq ← Hlth için kullanıldı, çünkü önceden yazılmış ve ekonomik gerekçesi vardı. Komşu parametre kontrolü sonradan yapıldı.
- **Literatür aylık ufukta.** Menzly–Ozbas (2010, JF) ve Cohen–Frazzini (2008, JF; aylık > 150 bp alfa, v_dalga DOĞRU) aylık ufukta çalışır. Hou (2007, RFS)'un sektör içi büyük→küçük öncülüğü hedef portföyler VW ve büyük şirket olduğu için burada geçersiz. Hong–Torous–Valkanov (2007) zayıf ve kırılgan (DLG §2). Yayın sonrası aşınma (McLean–Pontiff 2016) beklenmeli.
- **Kaynak ayrımı.** SIC kodları EDGAR'dan okunmadı (bu oturumda erişilmedi); FF49 tanımları Ken French'ten okundu. TradingView sayfasının var olması kullanıcının planında grafiğin açılacağını garanti etmez.
- **Yatırım tavsiyesi değildir.**
