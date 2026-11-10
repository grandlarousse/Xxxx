# VİOP'ta "öncü oynadı, hedef oynamadı" kuralı: hangi çiftlerde çalışıyor? (10.11.2026)

_Veri 10.11.2026 kapanışına kadar. Yatırım tavsiyesi değildir; kaldıraçlı üründe sermayenin tamamı kaybedilebilir._

## Kısa yanıt

- **Kuralın genel hâli para kazandırmıyor.** 126 önceden belirlenmiş öncü→hedef çiftinde ve 4.275 çiftlik hipotezsiz taramada "öncü oynadı, hedef oynamadı → hedefi al" işleminin ortalama brüt kazancı birkaç bps'i geçmiyor (yurt içi çiftlerde +6, yurt dışı emsallerde +9; bps = baz puan, 100 bps = %1). Tek işlemin maliyeti 22–26 bps.
- **Kuralının birebir çalıştığı tek çift: Koç iştirakleri → KCHOL.**
- Yanına üç kural daha konabilir: SAHOL/AKBNK oranı, ABD rafinerileri → TUPRS, XU030 vadeli–spot farkı.
- Dördü de doğrulamadan "küçük boyutla, önce izleyerek" notuyla çıktı. "Kesin çalışan" bir öncü-takipçi çifti yok.
- 04.11 listesinden iki kural düştü: Koza grubu momentumu ve USDTRY → THYAO.

## Ne yapmalıyım

**1. Her akşam yalnız şu dört kurala bak.** Sektör arkadaşı yükseldi diye geride kalanı alma (aşağıda "Yapma" listesi).

### Kural 1 — Koç iştirakleri → KCHOL (senin kuralın)

- **İzle:** BIST:TUPRS, BIST:FROTO, BIST:YKBNK, BIST:TOASO, BIST:ARCLK (tam sürümde ayrıca BIST:OTKAR, BIST:TTRAK, BIST:AYGAZ), BIST:XU030, BIST:KCHOL
- **İşlem:** BIST:KCHOL1!
- **17:50 koşulu (elle):** beş iştirakin günlük % değişimlerinin ortalaması, XU030'un % değişiminden en az **0,9 puan** yukarıdaysa ve KCHOL'ün XU030'a göre farkı **+0,35 puanı geçmemişse → AL.** Tersi (iştirakler 0,9 puan geride, KCHOL −0,35'in altına inmemiş) → SAT.
- **Giriş:** aynı gün kapanışı (uzlaşma fiyatı, yani VİOP'un gün sonu fiyatı). Ertesi güne bırakma: 2022'den beri bir gün geç girenin kazancı sıfıra yakın (+7 bps).
- **Çıkış:** 17:30'da bakınca KCHOL açığın yarısını kapatmışsa o kapanışta; kapatmadıysa en geç 3. gün kapanışında.
- **Beklenti:**
  - Tam sürüm (8 iştirak, piyasa etkisi ayıklanmış), 2017–2026: işlem başına brüt +65…+72 bps, yılda ~20 işlem. Maliyet sonrası +39…+46.
  - Aynı kural 17:30 fiyatlarıyla, son 3 yıl: +104…+113 bps (yaklaşık 60 işlem).
  - Elle sürüm (5 iştirak) daha zayıf: 2017–2026 +20 bps (2018–2022 zararda), 2022'den beri +54, son 2 yıl +141; 17:30 sürümü +51.
- **Zayıf yanları:** kârın ~%60'ı en iyi 10 işlemden geliyor (onlar çıkınca +26…+33). Çoklu test eşiğini sınırda kaçırdı. XU030 vadelisiyle korunursan maliyet sonrası kazanç kalmıyor (+2); yani kazancın yarısı piyasa yönünden.
- **Güven:** ORTA–DÜŞÜK.

### Kural 2 — SAHOL/AKBNK oranı (iki bacaklı)

- **İzle:** BIST:SAHOL, BIST:AKBNK (oran grafiği: `BIST:SAHOL/BIST:AKBNK`)
- **İşlem:** BIST:SAHOL1! ve BIST:AKBNK1!
- **17:50 koşulu:** oran son 60 günlük ortalamasından yaklaşık **%3,6** uzaklaşınca. SAHOL ucuz kaldıysa SAHOL1! AL + AKBNK1! SAT; pahalıysa tersi. Her 5 SAHOL kontratına 4 AKBNK kontratı. Kesin hesap için 04.11 klasöründeki gösterge ve betik (`kod/sahol_akbnk_z.pine`, `kod/sinyal.py`).
- **Çıkış:** oran %3,6'lık bandın içine dönünce, o kapanışta.
- **Beklenti:** brüt +71…+74 bps, yılda ~14 işlem. 17:30 fiyatlarıyla son 3 yıl +74…+82. Son 2 yıl +111.
- **Zayıf yanları:**
  - İki bacağın maliyeti 45–53 bps; maliyet sonrası +21…+28 kalıyor. Komisyonun düşükse anlamlı, değilse sınırda.
  - 1–3 günlük bir işlem değil: yarısı 2 günde kapanıyor, dörtte biri 5 günü aşıyor. 8 gün ve daha uzun süren 19 işlemin ortalaması −338 bps.
  - Süre sınırı koymak da çözmüyor: 3 günde kesince maliyet sonrası −6…−13, 5 günde +1.
- **Güven:** ORTA (ilişki sağlam, kazanç maliyete duyarlı).

### Kural 3 — ABD rafinerileri → TUPRS (hedefe bakmadan)

- **İzle:** NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF, TVC:SPX
- **İşlem:** BIST:TUPRS1!
- **Koşul:** bir önceki ABD seansında dört rafinerinin ortalama % değişimi S&P 500'den en az **2,8 puan** yukarıdaysa → AL. Sinyal sabah bellidir. Yalnız AL tarafını kullan; SAT tarafı son 2 yılda kazandırmadı.
- **TUPRS'un o gün oynayıp oynamadığına bakma.** "Oynamadı" şartını ekleyince sonuç bozuluyor (+28…+31 bps, son 2 yıl −20).
- **Giriş:** o günün kapanışı. **Çıkış:** 2 gün sonraki kapanış.
- **Beklenti (iki yön birlikte ölçüldü):**
  - Bu karttaki sade kural: 2017–2026 brüt +43 bps, yılda ~47 işlem, maliyet sonrası +18. Son 2 yıl brüt +52, maliyet sonrası +27.
  - Piyasa etkisi ayıklanmış tam sürüm: brüt +51 (10 yılın 8'i artıda), maliyet sonrası +26. Son 2 yıl brüt +37, maliyet sonrası +13.
- **Zayıf yanları:** zayıflıyor; son 2 yılın kazancı birkaç işleme ve PBF'ye bağlı. Hareketin bir kısmı sen girmeden oluşuyor: son 2 yılda ~46 bps kapanıştan önce, ~28 bps sonra.
- **Güven:** ORTA–DÜŞÜK.

### Kural 4 — XU030 vadeli–spot farkı (öncü-takipçi değil, kapanış rutini)

- **İzle:** BIST:XU030 (18:10 kapanışı) ve BIST:XU030D1! (son fiyat)
- **Koşul:** fark = vadeli son fiyat / spot kapanış. Bugünkü fark dünküne göre **67 bps'ten fazla** düştüyse (vadeli ucuz kapandı) → AL; o kadar arttıysa → SAT.
- **Giriş:** 18:10–18:15 arası. **Çıkış:** ertesi gün kapanış. Bir gün geç girenin kazancı sıfır.
- **Beklenti:** brüt +20…+25 bps, yılda ~65 işlem, maliyet sonrası ~+14. Son 2 yıl +30.
- **Güven:** ORTA.

**2. Boyut.** Dört kuralda da olağan riskinin en çok üçte biriyle başla ya da 2–3 ay tek kontratla izle. Kontrat sayısı için 04.11 klasöründeki `risk_ve_boyut_tablosu.csv`.

**3. Komisyonunu öğren.** Maliyet sonrası rakamlar pay vadelisinde gidiş-dönüş 22–26 bps (komisyon + alım-satım farkı) varsayımıyla. Seninki düşükse fark doğrudan kazanca eklenir.

**4. Yapma listesi (test edildi, kazandırmadı):**

| Fikir | Sonuç (brüt, işlem başına) |
|---|---|
| Bankalar yükseldi, bir banka geride → onu al | bir gün geç girişte AKBNK −45, ISCTR −67, TSKB −60; 17:30 sürümünde −130, −67, −25 |
| THYAO ↔ PGSUS, TCELL ↔ TTKOM | sıfır ya da eksi (−31…+6) |
| Otomotiv, çelik, çimento, perakende arkadaşları | artı ama şanstan ayırt edilemiyor (en iyisi BIMAS ← MGROS+SOKM +53; 17:30 sürümünde +22) |
| Piyasa yükseldi, hisse geride → al (47 hissede) | +6…+9; maliyet sonrası ~−23 |
| Koza grubu: TRALT oynadı → TRMET | −23; grup momentumu da son 2 yılda söndü |
| Petrol düştü → THYAO/PGSUS al | işaret ters çıktı (−43, −69) |
| TKC (ABD) → TCELL | +23, 2022'den beri 0 |
| Altın → TRALT (tek bacak) | +6…+31, anlamsız |
| USDTRY → THYAO, ENKAI | kur vadelisinin taşıma etkisi ve piyasa yönü; ayıklanınca yok |

**5. 10.11.2026 kapanışındaki durum:**

- **KCHOL:** tetik yok. İştirak farkı −0,16 puan (eşik ±0,86). KCHOL bugün XU030'un 3 puan gerisinde kapandı ama iştirakler oynamadığı için bu, kuralın sinyali değil.
- **SAHOL/AKBNK:** eşiğe çok yakın (oran ortalamanın %3,3 altında, eşik %3,6). 11.11'de, diğeri sabitken AKBNK 71,09 üstünde ya da SAHOL 86,98 altında kapanırsa: SAHOL1! AL + AKBNK1! SAT.
- **TUPRS:** tetik yok. 9 Kasım'da rafineriler ortalama +%3,48, S&P 500 +%2,35; fark 1,14 puan (eşik 2,8).
- **XU030 farkı:** −6 bps (eşik ±67), tetik yok.

## Gerekçe ve kanıt

**Nasıl test edildi.** Çift listesi ve kurallar hesaptan önce yazıldı; bağımsız bir denetçi planı inceledi, 14 düzeltmesi işlendi, sonra hesap çalıştırıldı.

- Evren: 47 pay vadelisi, XU030, XLBNK, USDTRY, ons altın, gümüş, gram altın.
- Öncüler: grup/ortaklık bağları, sektör arkadaşları, yurt dışı emsaller (rafineri, havayolu, çelik, altın, savunma, bira, otomotiv, beyaz eşya, gübre, çimento), kur.
- Kural birebir senin kuralın: öncü kendi olağan günlük oynaklığının en az 1 katı oynamış, hedef 0,25 katını geçmemiş → aynı kapanışta hedef vadelisine gir, 2 gün tut.
- Her çiftte ayrıca: hedefe bakmayan sürüm, bir gün geç giriş, 17:30 fiyatlarıyla kurulan sürüm (17:50'de gerçekten görülebilir mi?), öncü serisini takvimde kaydırarak şans dağılımı, 2022 sonrası ve son 2 yıl.

**Genel sonuç.**

- 126 çiftte senin kuralın: %5 düzeyinde anlamlı görünen 15 çiftin 8'i artı, 7'si eksi yönde. Çoklu test düzeltmesinden (aynı anda çok şey denendiğinde şansla çıkanları ayıklayan düzeltme) geçen tek çift FROTO ← USDTRY; o da aşağıdaki nedenlerle işlem listesine girmedi.
- Temiz ölçümle (bir gün geç giriş) yurt içi çiftlerin havuz ortalaması +6 bps/işlem.
- "Hedef oynamadı" şartı sonucu ne iyileştiriyor ne kötüleştiriyor (fark +0,1 bps). Öncünün oynaması tek başına biraz bilgi taşıyor: yurt dışı emsallerde ortalama brüt +19,5 bps. Bu da maliyetin altında.
- Hipotezsiz tarama (92 öncü × 47 hedef): 2017–2022'de iyi görünen 15 çiftten 2023–2026'da ayakta kalan 0. Şansla beklenen de 0–1.

**Dört kuralın kanıtı.** Sayılar iki ayrı kodla hesaplandı; aralıklar iki hesabı gösterir.

| Kural | İşlem sayısı | Brüt bps | 2022+ | Son 2 yıl | 17:30 sürümü | Bir gün geç |
|---|---|---|---|---|---|---|
| KCHOL (tam) | 197–208 | 65–72 | 74–79 | 122 | 104–113 | 43 (2022+: 7) |
| SAHOL/AKBNK | 135–136 | 71–74 | 80–85 | 111 | 74–82 | 63–65 |
| TUPRS | 457 | 51 | 62 | 37 | sinyal sabah belli | 42 |
| XU030 farkı | 625 | 20–25 | 21 | 30 | yok (18:10 işi) | −1 |

- 17:50'de görülebilirlik (son 59 gün, 5 dakikalık veri): SAHOL/AKBNK'da 59 günün 58'inde 17:50 görüntüsü kapanışla aynı. KCHOL'de kapanış sinyallerinin 5/8'i (elle sürümde 9/11) 17:50'de oluşmuştu, ters yönlü hiç yok.
- KCHOL'de "doyunca çık" (karar 17:30 fiyatıyla, o kapanışta çıkış), son 3 yıl: işlem başına +139 bps, ortalama 2,3 gün (68 işlem).
- KCHOL yıl yıl (tam sürüm): 2019 +62, 2020 +66, 2021 +27, 2022 −68, 2023 +132, 2024 +164, 2025 +147, 2026 +85. Hem alış (+68) hem satış (+60) tarafı artıda.

**İzlemeye değer ama işlem listesine girmeyenler.**

- **EREGL ← ASX:FMG + ASX:BHP** (Sidney kapanışı, ASX200'e göre ±1,3 puan; 3 gün): brüt +55, son 2 yıl +103; ama 2022+ zayıf (+34) ve bir gün geç girince sıfır.
- **TRALT ← VİOP ons altın** (BIST:XAUUSD1! günlük ±%1,8): yalnız XU030 ile korunmuş hâliyle +44…+48, son 2 yıl +94. İki bacak maliyetinden sonra +14…+17.
- **FROTO ← VİOP USDTRY:** istatistik güçlü (+125…+132, 8 yılın 8'i artı). Ama kazanç sinyalden 2–4 gün sonra geliyor, 2024–26'da tetikleyen kur hareketi çok küçük (medyan 41 bps, 2026'da 21) ve aynı günlerde başka hisseler de yükselmiş. Açıklayan bir mekanizma yok.

## Emin olunmayanlar ve doğrulama kapsamı

**Düzeltilenler.**

- **Varsayımın:** "ilgili varlık yükseldi, ana varlık yükselmedi, öyleyse yakalar" VİOP hisselerinde genel olarak doğru çıkmadı. Yakalama yalnız holding–iştirak bağında (KCHOL, kısmen SAHOL) görülüyor.
- **Benim ara mesajım:** "hedef oynamadı koşulu daha kötü sonuç veriyor" demiştim. Hakem bunun ölçüm hatası olduğunu gösterdi: vadeli gün sonu fiyatı, hissenin kapanış seansındaki hareketini geriden izliyor ve aynı gün girişli ölçümü çarpıtıyor. Bir gün geç girişle fark yok.
- **04.11 listesi:** Koza momentumu son 2 yılda +22 (anlamsız), 2026'da eksi. USDTRY → THYAO taşıma etkisi ayıklanınca son 2 yılda −149. İkisi listeden çıktı. SAHOL/AKBNK için o raporda yazan maliyet sonrası +30…+50 beklentisi bireysel maliyetle +21…+28'e indi.

**Doğrulama kapsamı.**

- Yeniden üretim: iki ajan adayları ilk kodu görmeden yeniden yazdı. 39 sayı kümesinin 34'ü tolerans içinde tuttu, 3'ü sınırda kaldı, 1'i tutmadı (TOASO ← USDTRY son 2 yıl; listede yok), 1'i yeniden hesaplanmadı (TRALT'ın 17:30 sürümü).
- Çürütme: hakem 5 iddiayı inceledi. Dört kural "zayıfladı, yalnız izle" hükmü aldı; ENKAI ← USDTRY çürüdü; "genel kural çalışmıyor" ayakta kaldı.
- Bulunan kod kusurları: SAHOL/AKBNK'da çıkış kararı aynı kapanış fiyatıyla veriliyordu (bu yüzden 17:30 sürümünü esas aldım). FROTO'nun çoklu test değeri bir gün geç girişten hesaplanmıştı.
- Benim hükmüm hakemden biraz daha yumuşak: dört kuralı "küçük boyutla denenebilir" diye bıraktım, çünkü 17:30 sürümleri ve son 2–3 yıl olumlu. Hakemin itirazları kartlarda "zayıf yanları" olarak duruyor.

**Açık kalanlar.**

- 17:30 sürümleri yalnız Kasım 2023 sonrasını kapsıyor (saatlik veri o kadar); bu, kuralların en iyi dönemi.
- Gerçek komisyonun ve VİOP'taki anlık alım-satım farkı gözlenmedi; maliyet tahmindir.
- Elle (5 hisseli) KCHOL kuralı, test edilen tam sürümden zayıf. Tam sürümü her gün hesaplayan bir betik henüz yok.
- Kapanış fiyatından dolum varsayıldı; uzlaşma fiyatı son dakikaların ağırlıklı ortalamasıdır, birebir tutmayabilir.
- Faiz (DİBS) öncülü bu turda test edilmedi. Hipotezsiz tarama hakemce ayrıca incelenmedi.
- 10.11 fiyatları Yahoo'nun gün sonu satırından; ertesi gün küçük farkla güncellenebilir.

## Kaynaklar

- Borsa İstanbul VİOP günlük bülteni, 06.03.2017–10.11.2026, 2.429 gün (`borsaistanbul.com/data/vadeli/viop_YYYYMMDD.csv`).
- Yahoo Finance: günlük (2014+), saatlik (Kasım 2023+), 5 dakikalık (son 60 gün) fiyatlar; 112 BIST ve 71 yabancı sembol.
- Önceki çalışmalar: `raporlar/2026-11-02_viop_leadlag/`, `raporlar/2026-11-04_kapanis_1-3gun/`.
- Bu klasör: `ek/PLAN.md` (önkayıt), `ek/ciftler_onkayit.csv` (140 çift), `ek/ozet_birlesik_fdr.csv` (bütün çiftlerin sonucu), `ek/dogrulama_d1.md`, `ek/dogrulama_d2.md`, `kod/`.

## Devam notu

1. Sonuç: genel "öncü oynadı, hedef oynamadı" kuralı VİOP'ta çalışmıyor; küçük boyutla izlenecek dört kural KCHOL ← Koç iştirakleri, SAHOL/AKBNK oranı, TUPRS ← ABD rafinerileri, XU030 vadeli–spot farkı.
2. Rapor `raporlar/2026-11-10_viop_leadlag_islem/RAPOR.md`; TradingView listesi `izleme_listesi.txt`; plan ve çiftler `ek/PLAN.md`, `ek/ciftler_onkayit.csv`.
3. Sonuç tabloları `ek/ozet_birlesik_fdr.csv`, `ek/eski_b4.csv`, `ek/d1_sonuc.csv`, `ek/d2_tum_sonuclar.csv`; kod `kod/b1…b4`, `d1`, `d2`, `e_`.
4. Veri depoda yok; `kod/veri_indir.py`, `veri_yahoo.py`, `veri_panel.py` ile yeniden kurulur (sözlük `ek/README_veri.md`).
5. Sıradaki iş: dört kuralı her gün 17:40'ta hesaplayan tek betik ve 2–3 aylık ileriye dönük izleme kaydı.

_Maliyet: Seviye L (alt uç) · 9 alt ajan: 7 sonnet (1 veri, 4 backtest, 2 yeniden üretim) + 2 opus (yöntem denetimi, çürütme) · 2 üretim dalgası + doğrulama · bütçesini aşan ajan yok · aşılan sınır yok._
