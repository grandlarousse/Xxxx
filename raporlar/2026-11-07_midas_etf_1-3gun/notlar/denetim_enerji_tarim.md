# Denetim: enerji_tarim ailesi (2026-11-07)

**Sonuç.** Ajanın iki adayının (S1, S2) sayılarını, `lib.trades` / `lib.evaluate` / `ortak.full` kullanmayan kendi simülatörümle (`kod/denetim_enerji_tarim/dsim.py`) **birebir yeniden ürettim**. İleriye bakma, yanlış gün ya da maliyet hatası bulmadım. Ajanın ana yargıları da doğru: birleşik BH-FDR'yi geçen strateji yok, kabul/yedek ETF'ler için doğrulanmış gecikmeli öncü yok.

İki aday da **zayıf**. İkisi de doğrulanmış strateji olarak sunulmamalı:

- **S1 (KOLD, EIA arifesi, Kas-Mar):** Sonuç kuyruk işlemlerine bağlı; en iyi 10 işlem çıkarılınca net 22 bp, t 0,58 kalıyor. Kış/yaz ayrımı istatistiksel olarak desteklenmiyor: fark t 1,78, aylar arası ANOVA p 0,67. 1.000 $ pozisyonda t 1,84'e düşüyor.
- **S2 (USO alt Bollinger, C1 h2):**
  - Yalnız 1 günlük gecikmede çalışıyor; sivri bir tepe.
  - Aynı kural 312 ETF'lik evrende ortalama t −0,98 veriyor.
  - Yalnız IS'e bakılsaydı 8.149 satır içinde 386. sırada olurdu ve seçilmezdi.
  - 2025-2026'daki son 7 işlemin ortalaması net −32 bp.

İki aday da PTP ürünlerinde işlem görüyor. %10 brüt stopaj uygulanırsa ikisinin de beklentisi negatife döner.

Kod: `kod/denetim_enerji_tarim/`. Tablolar ve çıktılar: `sonuclar/aile_enerji_tarim/denetim/`. JSON: `sonuclar/aile_enerji_tarim/denetim.json`.

---

## 1. Yöntem

**Simülatör (`dsim.py`):**
- Giriş/çıkış: C0 = t kapanışı → t+h kapanışı; O1 = t+1 açılışı → t+h kapanışı; C1 = t+1 kapanışı → t+1+h kapanışı.
- Pozisyon açıkken gelen sinyal yok sayılır.
- Maliyet: 2 × 1,5 $ / pozisyon + tarama.csv'deki makas.
- Fiyatlar `lib.load` ile okundu.

**Sinyaller sıfırdan yazıldı:**
- S1: EIA takvim dosyasından rapor günü bulunur, KOLD dizininde bir önceki işlem günü sinyal günüdür.
- S2: Bollinger bandı pandas rolling ile hesaplandı (örneklem std, ddof=1). İlk 200 gün kapalı; ajanla aynı.

**Sağlamlık testleri:**
- Mod/ufuk ızgarası
- Maliyet: 1.000 / 2.500 / 10.000 $
- Yıl yıl sonuçlar
- Alt örneklemler: 2020 hariç, 2022 hariç, en iyi 5/10 hariç, winsorize
- Permütasyon, R = 5.000
- Parametre komşuluğu
- Giriş gecikmesi taraması
- Aynı kuralın evrende ve ailede sonucu
- Seçim yanlılığı yürüyüşü: IS'e göre seç, OOS'ta bak

Bu denetimde yaklaşık 150 kontrol testi çalıştı. Bunlar yeni aday değil, sağlamlık kontrolüdür.

## 2. S1 — EIA doğalgaz raporu arifesi KOLD long (yalnız Kas-Mar)

**Yeniden üretim (C0 h1, 2.500 $):** ajanla birebir aynı.

| Ölçü | Değer |
|---|---|
| n | 216 |
| Brüt / net | 116,5 / 100,5 bp |
| t | 2,24 |
| Kazanma | %58 |
| PF | 1,53 |
| IS net (t) | 113 bp (1,97) |
| OOS net (t) | 86 bp (1,22) |
| Pozitif yıl | 7/11 |
| maxDD | −%41,7 |
| En kötü | −1.664 bp |

**Zamanlama kontrolü:**
- Takvim önceden biliniyor.
- Rapor günlerinin hepsi KOLD dizininde var.
- Giriş arife kapanışında, çıkış rapor günü kapanışında; doğru günler.
- KOLD ~ UNG yıllık betası her yıl −1,64..−1,93. Kaldıraç değişikliği yok.

**En büyük 5 kazanç** (hepsi gerçek doğalgaz çöküş günü; veri hatası yok):

| Tarih | KOLD net |
|---|---|
| 2018-11-15 | +4.233 bp (UNG −%19) |
| 2024-11-27 | +1.694 bp |
| 2022-02-03 | +1.687 bp |
| 2020-12-03 | +1.635 bp |
| 2023-01-05 | +1.570 bp |

**Sağlamlık:**

| Test | Sonuç |
|---|---|
| En iyi 5 hariç | net 51,6 bp, t 1,34 |
| En iyi 10 hariç | net 21,6 bp, t 0,58, OOS −18 |
| %2,5 winsorize (iki yan) | net 88 bp, t 2,27 |
| Medyan işlem / işaret testi | +114 bp brüt / p 0,004 |
| 2020 hariç | t 1,84 |
| 2022 hariç | t 2,55 |
| 2020 ve 2022 hariç | t 2,13 |
| Kasım 2018 hariç | t 1,96 |
| Maliyet (1.000 / 2.500 / 10.000 $) | 82,5 (t 1,84) / 100,5 (2,24) / 109,5 (2,44) bp |
| Permütasyon, tüm günler | p 0,005 |
| Permütasyon, Kas-Mar günleri | p 0,023 |
| Permütasyon, Kas-Mar arife dışı günler | p 0,006 |
| Mod: O1 h1 | net 64,5 bp, t 2,13; kapanışa bağımlı değil |
| Mod: C1 h1 | −26 bp; etki rapor gününde, beklenen sonuç |

**Post-hoc mevsim ayrımı:**
- Önceden belirlenmiş tam yıl versiyonu: net 43 bp, t 1,65. Eşik altı.
- Kış−yaz farkı: t 1,78 (p 0,076).
- Aylar arası heterojenlik: ANOVA p 0,67, Kruskal p 0,76.
- Ay ay brüt: Kasım +212, Şubat +186, Ocak +97, Mart +50, Aralık +45; Nisan +49, Haziran +83, Eylül +49, Ekim +63; Mayıs −23, Temmuz −13, Ağustos −70.
- IS'te kış seçilseydi: OOS kış brüt 101 bp (t 1,44), OOS yaz 44 bp (t 0,83).
- Veri, "her ay ~60 bp + gürültü" modeliyle de uyumlu.
- **Bu yüzden dürüst tahmin tam yıl tahminidir (t 1,65). Kış ayrımı bir hipotez olarak kalmalı.**

**Haftanın günü karışması:** Kış aylarında ertesi gün Pazartesi olan günler (Cuma kapanışı → Pazartesi kapanışı) de +92 bp veriyor (t 1,34). Tatil kaymalı raporlar (Çarşamba n=13, Cuma n=9) ve rapor olmayan Perşembeler (n=11) etkiyi haftanın gününden ayırmaya yetmiyor.

**FDR:** tek yönlü p 0,013. 8.635 testte ilk sıra eşiği 1,2e-5; geçmiyor. Yalnız aileye özel 319 test içinde eşik 3,1e-4; o da geçmiyor.

**Aile içi:** UNG / BOIL / UNL aynı günlerde negatif. Bunlar aynı dayanağın aynası, bağımsız kanıt değil.

**Midas:**
- KOLD bir PTP ürünü (ProShares Trust II). %10 brüt satış kesintisi uygulanırsa beklenti ≈ −900 bp/işlem.
- KOLD'un Midas'ta bulunurluğu doğrulanamadı.
- C0 girişi MOC olmadığı için TR 23:45-23:59'da piyasa emriyle yapılmalı.

**Takvim düzeltmesi:**
- 24 Ara 2026 Perşembe raporu NYSE erken kapanış günü (13:00 ET = TR 21:00). Çıkış bu kapanışta.
- Noel arifesi için federal kapanış kararnamesi çıkarsa rapor 23 Ara Çarşamba 12:00 ET'ye kayar. O durumda giriş 22 Ara olur.
- Ajanın strateji metninde bu uyarı yok, yalnız olay dosyasında var.

**Karar: ZAYIF.** Sonuç yeniden üretiliyor ve kapanışa bağımlı değil. Ancak:
- kış ayrımı post-hoc ve istatistiksel olarak desteklenmiyor,
- en iyi 10 işlem çıkarılınca sonuç kayboluyor,
- 2020 hariç t 1,84; 1.000 $ pozisyonda t 1,84,
- OOS t 1,22,
- FDR'yi geçmiyor,
- ürün PTP.

## 3. S2 — USO alt Bollinger(20, 2) kırılımı → t+1 kapanışında gir → t+3 kapanışında çık

**Yeniden üretim:** ajanla birebir aynı.

| Ölçü | Değer |
|---|---|
| n | 54 |
| Brüt / net | 135,4 / 121,4 bp |
| t | 2,95 |
| IS net (t) | 75 bp (1,13) |
| OOS net (t) | 167 bp (3,47) |
| Pozitif yıl | 7/9 |
| maxDD | −%9,3 |
| En kötü | −763 bp |

Ajanın "t+2 açılışında gir, h=2" iddiası da doğru: net 90 bp, t 3,14. Ancak aynı girişle h=3 tutulursa net 8 bp, t 0,12.

**En iyi 5 işlem** (hepsi gerçek olay; veri hatası yok):

| Giriş tarihi | Net |
|---|---|
| 2022-07-06 | +647 bp |
| 2020-03-09 (fiyat savaşı) | +630 bp |
| 2022-09-08 | +615 bp |
| 2021-07-20 | +558 bp |
| 2020-02-28 | +452 bp |

**Gecikme profili** (işlem açılan 54 sinyal, günlük ortalama getiri):

| Gün | Ortalama |
|---|---|
| t+1 | −128 bp (t −2,22) |
| t+2 | +86 bp (2,07) |
| t+3 | +53 bp (1,35) |
| t+4 | −64 bp (−1,41) |

**Giriş gecikmesi taraması** (t+d kapanışında gir, 2 gün tut): d=0 → −38; **d=1 → +102**; d=2 → +15; d=3 → −76; d=4 → −52; d=5 → −79 bp.

Sonuç: kâr yalnız t+2..t+3 penceresinde. Bu bir **sivri tepe**, plato değil. C0 ve O1 modlarında h1-h2 sonuçları negatif ya da sıfıra yakın.

**Parametre komşuluğu** (uzunluk 10-40 × çarpan 1,5-2,5, C1 h2; `s2_parametre_komsuluk.csv`):
- Tam örneklemde t ≥ 2 yalnız 6/35 hücrede, bir köşegen sırt boyunca: (16; 2,0) 3,34 · (20; 2,0) 2,95 · (20; 2,25) 2,89 · (24; 2,5) 2,51 · (14; 1,75) 2,40 · (24; 2,25) 2,26.
- IS net 24/35 hücrede negatif.
- OOS net 34/35 hücrede pozitif.
- Yorum: 2022-2024 petrolünde genel bir "düşüşten 1 gün sonra al" dönüşü var. Bu Bollinger'a özgü değil, rejime bağlı. 2025-2026'da da kayboluyor.

**Alt örneklemler:**

| Test | Sonuç |
|---|---|
| En iyi 5 hariç | net 74,6 bp, t 1,89 (IS 16,5) |
| 2022 hariç | t 1,99 |
| 2020 ve 2022 hariç | t 2,35 |
| Winsorize | t 3,18 |
| 1.000 $ pozisyon | net 103 bp, t 2,51 |
| Son 7 işlem (2025-2026) | ortalama net −32 bp (2025: −12; 2026: −149) |

**Permütasyon:** rastgele 54 gün, aynı t+1 → t+3 yapısı.
- Tüm günler: p 0,005.
- Düşüş rejimi (5 günlük z en düşük %15): p 0,005.

Ancak ~8.300 testlik bir taramada p 0,005 düzeyinde ~40 sonuç tesadüfen beklenir.

**Seçim yanlılığı (`d_secim_yanliligi.py`):**
- Aynı kural (MR_bb20_alt C1 h2) evrende 312 ETF'te ortalama t −0,98 veriyor. t > 2 oranı %1,3, yani şans düzeyinin (%2,3) altında. t < −2 oranı %11.
- Ailede IS t'sine göre seçilen en iyi 10 / 25 / 50 / 100 satırın OOS ortalaması: +4 / −40 / −32 / −24 bp; OOS'ta pozitif olanların oranı %18-30. Genel tarama bu ailede örneklem dışına taşınan bir bilgi taşımıyor.
- S2'nin IS t sırası: 8.149 satırda 386.
- S2'nin "OOS" gücü, seçim açısından örneklem dışı değil.

**Aile içi** (`s2_aile.csv`):
- ETF kendi bandıyla:
  - WTI fonları pozitif: UCO 288 bp (t 4,19; ajanın tablosunda yok), DBO 85 (2,37), USL 61 (1,85).
  - Brent fonu zayıf: BNO 40 (0,90).
  - Enerji hisseleri negatif: XLE −20, XOP −42, OIH −36, GUSH −155. PDBC ≈ 0.
- Sonuç: tek bir bağımsız küme (WTI fonları).
- XOP, USO sinyaliyle: yalnız C1 h2'de +131 bp (t 2,49). C1 h1 −4, C1 h3 −6 bp. Kırılgan.

**Midas:**
- USO (USCF) ve UCO (ProShares Trust II) PTP ürünleri. %10 brüt kesinti uygulanırsa beklenti negatife döner.
- **UCO artık "2x USO" değil.** UCO ~ USO betası 2016-2019'da 1,94-1,97 iken 2024'te 1,64, 2025'te 1,56, 2026'da **1,13** (korelasyon 0,91). UCO, USL'ye göre hâlâ 1,99 betalı. Yani USO 2026'da ön aya yakın, çok oynak bir fon gibi davranıyor (günlük oynaklık 340 bp).
- Giriş zamanı (t+1 kapanışına yakın, TR 23:45) kullanıcının akşam kontrol düzenine uygun.
- TradingView çarpanı 2,05 doğru: popülasyon std ile 2 × √(20/19).

**Karar: ZAYIF.** Kâğıt üzerindeki eşikleri geçiyor ve yeniden üretiliyor. Ancak:
- genel taramadan seçildi; IS'te anlamsız, IS sırası 386,
- yalnız 1 günlük gecikmede çalışıyor,
- evrende tekrar etmiyor,
- son iki yılda negatif,
- PTP.

Çürütülmüş sayılmaz, ama işlem kuralı olarak önerilemez.

## 4. Lead-lag

**leadlag_sweep'te FDR bayrağı olan satırlar.** Aile hedefli 1.195 satırdan 6'sında FDR bayrağı var; hiçbiri kabul/yedek bir ETF'e ait değil. Kabul/yedek hedeflerde "FDR + IS/OOS aynı işaret + bp/sd > maliyet" ölçütünü geçen satır sayısı **0**. Ajanın "doğrulanmış gecikmeli öncü yok" yargısı **doğrulandı**.

**FDR bayraklı satırlar:**
- **CANE ← BNO / USL / XLE / T10YIE:** kendi 2 gecikmesi kontrollü, Newey-West yeniden hesapta h1 t 3,43 (IS 2,02 / OOS 2,84), 10 bp/sd. Maliyet 27 bp, likidite 2,5 mn$.
  - Bayat fiyat artefaktı değil: etki yüksek hacimli günlerde (t 3,74; düşük hacimli günlerde 1,28) ve t+1'in açılış boşluğunda değil gün içi kısmında (gün içi t 3,31; boşluk t 1,17).
  - Gerçek ama ekonomik olarak kullanışsız. Red kararı doğru.
- **DBO ← BNO yetişme h3:** OOS t 1,03; DBO bir USO kopyası. Çürütüldü.
- **ERX ← XLE lag h3:** IS −5,06 / OOS +0,76. ERX 2020 Nisan'da 3x'ten 2x'e geçti (yıllık beta 2,99 → 1,99). Muhtemel artefakt. Çürütüldü.

**FDR'siz adaylar (zayıf):**
- KWEB → XLE / UNG / PDBC h3: t 2,6-2,9, ekonomik gerekçe yok.
- CPER → UCO h3: IS t 1,21.
- XOP ← UNG: OOS h1 t 0,51.
- VVIX → BNO / USO / SCO / XOP h3: t −2,4..−2,9. **Not:** VVIX kapanışı 16:15 ET'de, yani ETF kapanışından 15 dk sonra. C0 girişiyle kullanılamaz; ajan bunu belirtmemiş.

**TradingView kodları:** ajanın kullandığı ETF ve öncü kodları `tv_etf.csv` / `tv_dogrulama.csv`'de 'dogrulandi' ya da 'dogrulandi_kanonik' durumunda: NYMEX:CL1!, NYMEX:CL2!, NYMEX:NG1!, NYMEX:NG2!, ICEEUR:BRN1!, ICEENDEX:TFM1!, TVC:DXY, CME_MINI:ES1!, COMEX:GC1!, COMEX:HG1!, CBOT:ZC1!. Sorun yok.

## 5. "Kaçın" kuralı (UNG/BOIL long'u EIA gününe taşıma)

Arife kapanışından rapor günü kapanışına:
- UNG brüt −28 bp (t −1,97), 11 yılın 9'unda negatif; 2018-2026 arası her yıl negatif.
- BOIL −66 bp (t −2,50).

İddia doğrulandı. Kanıt sınırda, ama bu kuralı uygulamanın maliyeti sıfır. Risk kuralı olarak kabul edilebilir.

**OVX boyut kuralı (EN07)** da doğrulandı (`d_ovx.py`). OVX ≥ 1,25 × SMA20 olduktan sonra, OVX'in 16:15 kapanışı nedeniyle t+1'den ölçülen USO 3 günlük |hareketi| 655 bp; diğer günlerde 289 bp. Oran 2,27, t 5,7 (IS 2,89 / OOS 1,69). Yön bilgisi vermez, yalnız boyut kuralıdır.

## 6. İzleme listesine itirazlar

1. **KOLD 'kabul' → 'yedek (koşullu)' olmalı.** Tek dayanağı S1, o da zayıf (post-hoc, en iyi 10 hariç t 0,58, 1.000 $'da t 1,84). Ayrıca PTP, Midas'ta bulunurluğu doğrulanmadı ve −2x bozulma var.
2. **USO 'kabul'**, PTP kesintisi doğrulanana kadar yalnız 'izleme/referans' olmalı. PTP'siz ana araç XLE / XOP.
3. **XOP**, XLE'den daha düşük maliyet/oynaklık oranına sahip (0,074'e karşı 0,093) ve likiditesi yeterli (532 mn$). 1-3 günlük işlem için en az XLE kadar uygun; kabul edilebilir.
4. **UCO 'yedek'** "2x USO" diye tanımlanmamalı. 2026'da USO'ya göre betası 1,13; USL'ye göre 2.
5. **BOIL 'yedek' → 'red'.** Long stratejisi yok, koşulsuz bozulma büyük, rapor günü negatif. Elde yalnız bir kaçın kuralı var.

## 7. Kaçırılanlar

- **UCO kendi bandıyla C1 h2:** net 288 bp, t 4,19 (IS 2,54 / OOS 3,42; en iyi 5 hariç t 3,18; 2020 hariç t 3,58). Ailenin en güçlü satırı (p ≈ 5e-5) ama BH eşiği 1,2e-5; geçmiyor. 2025: −24 bp, 2026: −217 bp. Ajan "kendi bandıyla" tablosunda bunu göstermemiş. Etki WTI fonlarında (USO, UCO, DBO, USL) tutarlı, Brent'te ve enerji hisselerinde değil. Yine tek bir küme ve PTP.
- **UCO / USO yapısal ayrışması (2026):** yukarıda. Kaldıraçlı araç seçimini ve iki fonun sinyal günlerinin örtüşmesini etkiler.
- **S1'de 24 Ara 2026:** NYSE erken kapanış ve olası federal kapanış kararnamesi riski.
- **VVIX'in 16:15 ET zamanlaması:** lead-lag notlarında belirtilmemiş.

## 8. Tekrar üretim

Proje kökünden çalıştırılır:

```
python3 -I kod/denetim_enerji_tarim/d_s1_eia_kold.py
python3 -I kod/denetim_enerji_tarim/d_s1_ek.py
python3 -I kod/denetim_enerji_tarim/d_s2_uso_bb.py
python3 -I kod/denetim_enerji_tarim/d_secim_yanliligi.py
python3 -I kod/denetim_enerji_tarim/d_leadlag.py
python3 -I kod/denetim_enerji_tarim/d_ek_kontroller.py
python3 -I kod/denetim_enerji_tarim/d_kacin_ve_kaldirac.py
python3 -I kod/denetim_enerji_tarim/d_kucuk.py
python3 -I kod/denetim_enerji_tarim/d_ovx.py
python3 -I kod/denetim_enerji_tarim/d_json.py
```
