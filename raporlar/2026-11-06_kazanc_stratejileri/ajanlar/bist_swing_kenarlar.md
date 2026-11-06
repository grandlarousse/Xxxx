# BIST ve VİOP: swing ufkunda (birkaç gün – ~3 ay) belgelenmiş getiri düzenlilikleri

Tarih: 06.11.2026. Ajan raporu (ham çıktı). Yatırım tavsiyesi değildir.

Kapsam: 1–3 günlük lead-lag mikro kenarlarının ötesinde, BIST spot ve VİOP'ta gün–3 ay ufkunda belgelenmiş düzenlilikler. Her başlıkta kanıt türü, dönem, etki büyüklüğü, yayın/örneklem dışı davranış, maliyet, kapasite ve bir Türk bireysel yatırımcının uygulayabilirliği.

**Yöntem ve sınırlar (önce okunmalı)**

1. İki kaynak türü var: (a) literatür (DergiPark, Borsa Istanbul Review, SSRN, tezler), (b) bu rapor için yapılan **kendi testlerim**. Kendi testlerim İş Yatırım'ın herkese açık günlük fiyat uç noktasından indirilen düzeltilmiş kapanışlarla yapıldı (`HisseTekil`, 2005-01-03 → 2026-11-05; XU100 ve USDTRY aynı kaynaktan), TL nakit getirisi TCMB'nin 1 hafta repo tarih tablosundan (tcmb.gov.tr "Merkez Bankası Faiz Oranları / 1 Hafta Repo") kuruldu.
2. **Hayatta kalma yanlılığı (survivorship) ciddi.** İş Yatırım uç noktası yalnız bugün işlem gören kodları veriyor (KOZAL/KOZAA/IPEKE gibi eski kodlar boş döndü). Evren, benim seçtiğim 248 hisse (VİOP'taki 47 pay + BIST100/BIST Tüm'den likit adlar + 2020–24 halka arzları). Batan/kottan çıkan hisse yok. Bu, kayıp portföylerinin (losers) getirisini yukarı, eşit ağırlıklı evren getirisini yukarı iter. Momentum farkını (kazanan–kaybeden) büyük ihtimalle **küçültür**; kısa vadeli devam (losers keep losing) bulgusunu da **küçültür**; ama "VİOP-47 içinde momentum" sonucunu **büyütür** (bugün VİOP'ta olanlar geçmişin kazananlarıdır).
3. Çoklu test: ~10 sinyal × 3–4 dönem × birkaç parametre denendi. Tek bir parametre setinin en iyi sonucu değil, **sinyaller arası tutarlılık** ve **alt dönem kararlılığı** esas alındı. Raporladığım en iyi kombinasyonlara %30–50 "backtest iskontosu" uygulanmalı.
4. Web arama bütçesi (oturum başına 200 arama, tüm ajanlar ortak) iş ortasında bitti. Mevsimsellik, temettü duyurusu, MSCI/FTSE dengelemesi, kredi notu, faiz kararı günü, VBTS tedbirleri, spin-off, TEFAS akımı ve XU030 opsiyon VRP başlıklarında yeni literatür taraması yapılamadı; bunlarda ya kendi testim var ya da "kanıt bulunamadı/test edilmedi" yazıyor. Devam için kullanıcı yeni mesajla aramayı sürdürtebilir.
5. TL nakit serisi politika faizinin yıllık efektif kabulüyle kuruldu; 2017–18'de geç likidite penceresi (%12,75) ve Mart–Nisan 2025'te gecelik borç verme (%46) ile düzeltildi. Gerçek PPF getirisinden biraz düşüktür (2024'te seri %49,1, Kuveyt Türk'e göre PPF ortalaması ~%53). Yani "nakit" engeli **muhafazakar düşük**; stratejiler lehine hafif yanlı.

---

## 0. Kısa cevap

1. **Engel nominaldir, reel değil.** Politika faizi %36, TÜFE %29,7 → reel ~%5. PPF brüt ~%37–40, bireyde %17,5 stopaj sonrası ~%31–33; BIST pay ve pay/endeks VİOP kazancı %0 stopaj. Hisse riski için makul hedef vergi sonrası %45–50+.
2. **BIST'te büyük swing getirisinin baskın kaynağı rejimdir.** Negatif reel faizde (2021–23) XU100 TL'de +%26/+%197/+%36; pozitif reel faizde (2024–26) her yıl TL nakdin 12–23 puan gerisinde. Basit rejim kuralı (XU100 12 ay getirisi > 12 ay TL nakdi) 2011–18'de işe yaramadı ama 2019–26'da long/nakit %48 (nakit %25), XU030 vadeli L/S %55. **Bugün kapalı** (12 ay +%3,3 vs nakit +%37,3).
3. **Hisse seçiminde tek sağlam fiyat sinyali 52-hafta zirvesine yakınlık.** 248 likit hisse, 2016–26: Q5−Q1 +%1,5/ay (t≈2,2–2,3), 2021–26 +%3,2/ay (t≈3,3–3,7). Klasik 12-1 momentum ve rezidüel momentum evren genişledikçe çöktü (t 2,6 → 0,8): kırılgan.
4. **Kısa vadeli dönüş yok; 2016'dan beri devam var.** Haftalık kaybedenler sonraki hafta EW'nin 30–70 bps altında (t −2,9…−3,9). "Düşeni al" BIST'te para kaybettirdi.
5. **En iyi uzun-hisse yapısı:** 52-hafta Q5 (12–20 hisse) + rejim filtresi: 2016–26 CAGR %49–52 (nakit %21), MaxDD −%19…−%26; ama **2024, 2025, 2026'da nakdi geçemedi** (getiri 2017/2020/2022/2023'te). Survivorship ve seçim iskontosu sonrası beklenti: nakit +8…+15 puan/yıl, −%25…−%35 düşüş.
6. **Olaylar:** temettü hak kullanımından önceki 5 gün +%1,2 (t=7,8, n=1.109), 20 gün +%2,4; bedelsiz öncesi 20 gün +%2,8 (t=3,7, n=410), sonrası 5 gün −%2,0, 60 gün medyan −%5,3 ("bedelsiz sonrası yükselir" folkloru verilerde yok). İçeriden alım taklidi yıllık ~%6,6 anormal (Avcı 2024). PEAD L/S %2,9/60 gün. Halka arzda kazanç tahsis+seride; seri bittikten sonra alan 20 günde medyan −%5,5.
7. **TL carry (short USDTRY vadeli):** 07/2023'ten beri Sharpe 2,2, en kötü ay −%3,4; 2x notional ile TL toplam 2024 +%106, 2025 +%83. Ama 2010–26 tümünde Sharpe −0,5, MaxDD −%90 (2018, 2021, 2023'te tek ayda −%25…−%35). Rejime bağlı satılmış kuyruk opsiyonu.
8. **Piyasa-nötr göreli değer:** KCHOL ↔ iştirak sepeti ve SAHOL ↔ AKBNK oranında |z|≥2 dönüşü 20 günde +%2,1…+%3,9/işlem (t 2,8–3,8, iki bağımsız alt dönemde). Küçük ama rejimden bağımsız.
9. **Kanıtı olmayanlar:** AKD/takas "büyük kurum topluyor" takibi (hakemli kanıt yok; PIN öngörmüyor), kredili işlem uç değerleri, Ramazan/Ocak/tatil öncesi, A/B pay oranları, düşük vol, opsiyon satışı (veri yok).
10. **Dürüst sonuç:** Tek başına %36–40'ın belirgin üstünü veren düşük riskli bir kenar yok. Ortalamada engeli aşmanın yolu rejim filtresi + 52-hafta seçimi + olay katmanları + piyasa-nötr çiftler + koşullu carry kombinasyonu; iyi yıllarda nakit +20…+40 puan, normal yıllarda +5…+15, kötü yıllarda nakdin altında.

---

## 1. Engel (hurdle) doğru tanımlanmalı

- Politika faizi 22.10.2026 PPK'da %37 → %36 (−100 bp); koridor %34,5–39 ([QNB Invest](https://www.qnbinvest.com.tr/investodak/qnbarastirma/tcmb-ekim-ayi-faiz-kararini-acikladi-politika-faizi-36ya-indirildi)). TCMB tablosunda yürürlük 23.10.2026.
- Eylül 2026 TÜFE %29,73 y/y → ex-post **reel politika faizi ≈ 1,36/1,2973 − 1 ≈ %4,8**. "Reel faiz %40–50" algısı yanlış; %36–40 **nominal**.
- Bireysel yatırımcı için PPF/fon kazancı stopajı **%17,5**; 05.09.2026 Cumhurbaşkanı Kararı (11734) yalnız kurumsal yatırımcının PPF stopajını %0 → %10 yaptı ([PwC bülten 2026/03](https://www.pwc.com.tr/tr/sektorler/bankacilik-sermaye-piyasalari/bultenler/2026/kurumsal-yatirimcilarin-para-piyasasi-fonu-kazanclarinda-tevkifat-orani-yuzde-10a-yukseltildi.html), [İş Portföy Eylül 2026](https://www.isportfoy.com.tr/medya-ve-blog/para-piyasasi-fonlarinda-kurumlara-uygulanan-stopaj-duzenlemesi-hakkinda-eylul-2026)).
- VİOP'ta pay ve pay endeksine dayalı sözleşmelerde bireysel stopaj **%0**, diğer (USDTRY, altın dahil) **%10** ([Borsa İstanbul VİOP vergilendirme](https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/vergilendirme)). BIST pay alım-satım kazancı da bireyde %0.
- Sonuç: PPF brüt ~%37–40 (TCMB 1 hafta repo %36, efektif bileşik daha yüksek), stopaj sonrası **~%31–33**. Pay/endeks stratejisi vergi sonrası bununla kıyaslanır. Ama hisse riski (yıllık vol %30+, −%30 düşüşler) için makul hedef: **vergi sonrası %45–50+**. USD hedefi: T-bill ~%3,75–4 (Fed 16.09.2026 +25 bp, kontrol edilmedi) ve TL carry fırsat maliyeti.
- Tarihsel tablo (kendi hesabım, XU100 fiyat endeksi, temettü hariç):

| Yıl | XU100 TL % | TL nakit % | USDTRY % | XU100 USD % | TL nakit USD % | XU100 − nakit % |
|---|---|---|---|---|---|---|
| 2010 (Haz–) | 21.2 | 4.0 | -2.7 | 24.5 | 6.9 | 16.5 |
| 2011 | -22.3 | 6.0 | 22.8 | -36.8 | -13.7 | -26.8 |
| 2012 | 52.6 | 5.8 | -5.9 | 62.1 | 12.4 | 44.2 |
| 2013 | -13.3 | 4.8 | 19.5 | -27.4 | -12.3 | -17.3 |
| 2014 | 26.4 | 8.6 | 9.2 | 15.8 | -0.5 | 16.4 |
| 2015 | -16.3 | 7.6 | 25.4 | -33.3 | -14.2 | -22.2 |
| 2016 | 8.9 | 7.5 | 20.6 | -9.7 | -10.8 | 1.3 |
| 2017 | 47.6 | 12.4 | 7.2 | 37.7 | 4.9 | 31.3 |
| 2018 | -20.9 | 17.5 | 40.0 | -43.5 | -16.1 | -32.7 |
| 2019 | 25.4 | 20.5 | 12.5 | 11.5 | 7.2 | 4.0 |
| 2020 | 29.1 | 10.2 | 24.9 | 3.3 | -11.8 | 17.1 |
| 2021 | 25.8 | 17.7 | 79.7 | -30.0 | -34.5 | 6.8 |
| 2022 | 196.6 | 12.9 | 40.3 | 111.4 | -19.5 | 162.8 |
| 2023 | 35.6 | 17.9 | 57.4 | -13.9 | -25.1 | 15.0 |
| 2024 | 31.6 | 49.1 | 19.8 | 9.8 | 24.4 | -11.7 |
| 2025 | 14.6 | 43.5 | 21.4 | -5.7 | 18.1 | -20.2 |
| 2026 (–5 Kas) | 0.6 | 30.6 | 16.6 | -13.7 | 12.0 | -22.9 |

Yorum: 2024'ten beri pozitif reel faiz rejiminde XU100 her yıl TL nakdin **gerisinde** (2024 −%11,7, 2025 −%20,2, 2026 YTD −%22,9). 2021–23'teki büyük nominal getiriler negatif reel faiz rejiminin ürünüydü. Bu tek bulgu, "BIST'te kazananlar nasıl kazandı" sorusunun en büyük parçasıdır: **rejim (reel faizin işareti) > hisse seçimi**.

---

## 2. Sıralama (kanıt kalitesi × maliyet sonrası büyüklük × swing ufkuna uyum)

| # | Düzenlilik | Kanıt türü | Maliyet sonrası büyüklük | Dönem / bozulma | Uygulama (birey) | Ufuk | Hüküm |
|---|---|---|---|---|---|---|---|
| 1 | Piyasa rejimi: XU100 12 ay getirisi > TL nakit 12 ay ise risk açık; XU030 vadeli long/short | Kendi testim; küresel TSMOM literatürü | 2010–26 L/nakit %25,8 vs nakit %16,9 (MaxDD −%39); 2023–26 L/S %52,8 vs %36,7 | 2011–18 nakdin altında; 2024–26 yıllık sonuçlar kurala çok duyarlı | XU030 vadeli PSR %20, stopaj %0 | aylar | Çekirdek filtre |
| 2 | 52-hafta zirvesine yakınlık (Q5 al, Q1'den kaçın) | Kendi testim (248 hisse); MAKÜ 2007–16 anlamsız | Q5−EW +%0,64…+%1,31/ay; Q5−Q1 +%1,5…+%3,3/ay | 2016 sonrası; 2007–15 zayıf; 2022 ağırlıklı | Spot long; Q1 short yalnız VİOP-47 | 1 ay | En sağlam hisse seçimi |
| 3 | 2 + 1 birleşimi (long-only, rejim kapalıyken nakit) | Kendi testim | 2010–26 %33–36 vs nakit %16; 2016–26 %49–52 vs %21; MaxDD −%19…−%26 | 2024–26 nakdin altında | Spot, aylık yenileme | 1–3 ay | Engeli ortalamada aşabilen tek uzun-hisse yapısı |
| 4 | TL carry: short USDTRY vadeli + teminat PPF | Kendi hesabım; pratisyen | 1x fazla: 2024 +%18,3, 2025 +%13,5, 2026 YTD +%8,6 | 07/2023–26 Sharpe 2,2; 2010–26 Sharpe −0,5, MaxDD −%90 | VİOP PSR %33,3; stopaj %10 | haftalar–aylar | Koşullu, kuyruk hedge'li ve ≤1x |
| 5 | Kısa vadeli devam (haftalık/aylık kaybedenler düşmeye devam) | Kendi testim | Kaybedenler −30…−70 bps/hafta (EW'ye göre); 1 ay devam Q5−Q1 +%0,7…+%1,3/ay | 2016 sonrası; önce zayıf dönüş | Kaçınma kuralı; short yalnız VİOP-47 | 1–4 hafta | "Düşeni alma" kuralı |
| 6 | Holding/iştirak (KCHOL↔sepet) ve SAHOL↔AKBNK oran dönüşü | Kendi testim (+önceki çalışma) | +%2,1…+%3,9/20 gün işlem, isabet %64–76 | İki alt dönemde tekrar ediyor | VİOP 2–7 bacak | 10–60 gün | Küçük ama piyasa-nötr |
| 7 | Temettü hak kullanımı öncesi koşu | Kendi testim (n=1.109) | +%1,2 (5 gün, t=7,8); +%2,4 (20 gün) | 2010–26 sağlam | Spot | 1–4 hafta | Güvenilir, sezonluk overlay |
| 8 | Bedelsiz hak kullanımı öncesi koşu, sonrası zayıflık | Kendi testim (n=410) + 3 hakemli | Öncesi +%1,2 (5g)…+%2,8 (20g); sonrası 5 gün −%2,0; 60 gün medyan −%5,3 | 2018 sonrası daha güçlü | Spot (öncesi); sonrası short zayıf | 1–4 hafta | Overlay; "tut" değil "sat" |
| 9 | İçeriden/büyük ortak alımlarını izleme | Hakemli (Avcı 2024, EJF) | 1 yılda %6,58 anormal (brüt) | 2008–2019 | Spot, KAP bildirimi | haftalar–1 yıl | Filtre |
| 10 | Bilanço sonrası sürüklenme | Hakemli (Ahlatçıoğlu & Okay 2021, BIR) | L/S %2,9/60 gün (yılda ~%12 brüt) | 2007–2018 | Spot long; short kısıtlı | 60 gün | Küçük; filtre |
| 11 | BIST30/100 çıkış öncesi zayıflık, girişten sonra dönüş | YL tezi (Aslan 2019), hakemli (Aydıner & Altay 2020) | Çıkış öncesi 10 gün −%4,1; giriş sonrası 10 gün −%2,2 | 2009–2017, sonrası test yok | VİOP-47'de short | 2 hafta | Küçük |
| 12 | Halka arz: tahsis + tavan serisi; seri sonrası alma | Kendi testim (n=69) + hakemli | Seri sonrası 20 gün medyan −%5,5, 250 gün −%9,5 | 2020–24 | Spot; kapasite çok küçük | günler | Tahsis kazancı gerçek, ölçeklenmez |
| 13 | Ay dönümü, tatil öncesi, Ocak, Ramazan | Kendi testim + hakemli | Ay dönümü +16 bps/gün (t=2,0) → 2016 sonrası t=0,9 | Zayıflıyor | — | gün | Strateji değil |
| — | Kanıtsız/olumsuz: klasik 12-1 momentum (evrene kırılgan), rezidüel momentum (2016 sonrası), düşük vol, KRDMA/B/D oranı, TRALT/TRMET oranı dönüşü, AKD/takas takibi, kredili işlem uç değerleri, opsiyon satışı | | | | | | Kullanılmamalı / kanıt bekliyor |

---

## 3. Kesitsel fiyat düzenlilikleri

### 3.1 Literatür: BIST'te momentum karışık, uzun ufukta dönüş baskın

| Çalışma | Tür | Dönem | Bulgu |
|---|---|---|---|
| Bildik & Gülay (2007), *International Review of Finance* 7(1-2) [IDEAS](https://ideas.repec.org/a/bla/irvfin/v7y2007i1-2p61-87.html) | hakemli | 1991–2000 | Zıtlık (kaybedenleri al, kazananları sat) ~%15/yıl anormal; 1–36 ay tutuşta karlı; aylık %1,14 (Ünal 2021 özetinden) |
| Kandır & İnan (2011) (Ünal 2021 özetinden) | hakemli | 2000–2010 | Yalnız 12 ay oluşum/12 ay tutuşta kazananlar > kaybedenler; 3/6/9 ayda anlamsız |
| Ersoy & Ünlü (2013) (Ünal 2021 özetinden) | hakemli | 1995–2010 | 6 ay oluşum/6 ay tutuşta momentum var, tüm büyüklük gruplarında |
| Kaldırım (2017) (Ünal 2021 özetinden) | tez/makale | 2008–2015, BIST100 | 9–12 ay oluşum/tutuşta anlamlı; en iyi 12/12 ~%50 anormal (kümülatif); düşük fiyatlılarda daha güçlü |
| Alper & Aydoğan (2017), *Muhasebe ve Finansman Dergisi* [DergiPark](https://dergipark.org.tr/tr/download/article-file/428034) | hakemli | 2001–2015, 122 hisse | 1–5 yıl oluşum: kaybedenler izleyen 12 ayda kazananları %29 geçti (uzun ufuk zıtlık) |
| Ünal (2021), *Uluslararası Yönetim İktisat ve İşletme Dergisi* ICAFR özel [DergiPark](https://dergipark.org.tr/en/download/article-file/1419417) | hakemli | 1997–2020, tüm hisseler, eşit ağırlık | En yüksek %20 (6 ay oluşum) izleyen 12 ayda %29,7; diğer dilimler %37–41 (t=7,3). Kazananlar 6–60 ay boyunca geride. "Spekülatif şişen hisse" etkisi |
| Gökçen, "Factor investing in the Turkish equity market", *Borsa Istanbul Review* (2026) [SSRN 4588551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4588551), [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2214845026001043) | hakemli (WP 2023→2026) | 1994–2024, survivorship'siz | En güçlü faktör değer (B/M): >%17/yıl prim (WP), yayın özetinde değer alfa %12–13/yıl; momentum, boyut, karlılık **yalnız 2005 sonrası** anlamlı; düşük risk > yüksek risk; çok faktörlü portföy EM endeksini USD'de geçiyor. Momentum rakamı tam metinde, doğrulanmadı |
| Chui, Titman & Wei (2010), *JF* 65(1) [IDEAS](https://ideas.repec.org/a/bla/jfinan/v65y2010i1p361-392.html) | hakemli | 41 ülke 1980–2003 | Bireycilik endeksi düşük ülkelerde momentum zayıf; Türkiye bu grupta (Türkiye özel rakamı doğrulanmadı) |
| Demirer, Yüksel & Yüksel (2017), *RIBAF* 42 [EconPapers](https://econpapers.repec.org/RePEc:eee:riibaf:v:42:y:2017:i:c:p:1445-1454) | hakemli | BIST | Kısa vadeli dönüş getirisi piyasa durumuna bağlı; negatif piyasa durumunda "kaliteye kaçış" hisselerinde güçlü; petrol getirisi makro değişkenlerin öngörü gücünü emiyor. Büyüklük rakamı ücretli metinde |
| George & Hwang 52-hafta: "Gross profitability and 52-week high", *MAKÜ İİBF* (2021) [DergiPark DOI](https://dx.doi.org/10.30798/makuiibf.790900) | hakemli | 2007–2016 | 52-hafta zirvesi primi pozitif ama **anlamsız**; brüt karlılık primi anlamlı |

Ortak payda: eşit ağırlıklı, filtresiz tüm-hisse örneklemlerinde (mikro-cap ve manipülatif hareketler dahil) orta vadeli momentum ya yok ya da tersine dönüyor; 2005 sonrası ve likidite filtreli örneklemlerde momentum ortaya çıkıyor.

### 3.2 Kendi testim: likit evrende momentum, 52-hafta zirvesi, rezidüel momentum, kısa vadeli devam

Kurulum: her ay sonu, son 60 günlük medyan TL hacmine göre en likit **N** hisse (≥250 gün geçmiş), sinyale göre beşli dilim, eşit ağırlık, 1 ay tutuş. Q5 = en yüksek sinyal. Maliyet: tek yön %0,15 × dilim devri (yalnız long-only Q5 net getirisine uygulandı). Formasyon: MOM12_1 = t−12…t−1 getiri (son ay atlanır); H52 = fiyat/252 gün zirvesi; RESMOM = 36 ay XU100 betasına göre rezidüel getirilerin t−12…t−1 toplamı / std; MOM1 = son 1 ay; LOWVOL = −60 gün vol.

**N = 60 (en likit 60 hisse; Q5 ≈ 12 hisse)**

| sinyal | dönem | ay | Q5−Q1 %/ay | t | Q5−EW %/ay | t  | Q5 net CAGR % | EW CAGR % | nakit % | Q5 MaxDD % | devir % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MOM12_1 | 2007-15 | 108 | 1.16 | 1.89 | 0.25 | 0.61 | 15.8 | 13.6 | 4.1 | -54.5 | 27.9 |
| MOM12_1 | 2016-26 | 130 | 0.54 | 0.77 | 0.05 | 0.11 | 28.2 | 32.0 | 21.4 | -55.0 | 27.8 |
| MOM12_1 | 2021-26 | 70 | 0.22 | 0.21 | -0.36 | -0.56 | 25.8 | 37.1 | 28.5 | -55.0 | 28.0 |
| MOM6_1 | 2007-15 | 108 | 0.74 | 1.10 | 0.36 | 0.85 | 16.5 | 13.6 | 4.1 | -50.3 | 40.7 |
| MOM6_1 | 2016-26 | 130 | 0.43 | 0.61 | 0.07 | 0.15 | 28.4 | 32.0 | 21.4 | -54.8 | 38.5 |
| MOM6_1 | 2021-26 | 70 | 0.85 | 0.82 | 0.06 | 0.10 | 32.2 | 37.1 | 28.5 | -54.8 | 38.2 |
| MOM3_1 | 2007-15 | 108 | 1.39 | 2.15 | 0.62 | 1.41 | 19.4 | 13.6 | 4.1 | -50.9 | 56.0 |
| MOM3_1 | 2016-26 | 130 | -0.30 | -0.50 | -0.18 | -0.43 | 24.6 | 32.0 | 21.4 | -54.0 | 56.5 |
| MOM3_1 | 2021-26 | 70 | -0.69 | -0.77 | -0.58 | -0.96 | 22.4 | 37.1 | 28.5 | -54.0 | 58.2 |
| H52 | 2007-15 | 108 | 1.08 | 1.65 | 0.23 | 0.56 | 15.2 | 13.6 | 4.1 | -51.0 | 49.1 |
| H52 | 2016-26 | 130 | 1.56 | 2.22 | 0.64 | 1.60 | 37.4 | 32.0 | 21.4 | -41.3 | 52.6 |
| H52 | 2021-26 | 70 | 3.26 | 3.29 | 1.23 | 2.10 | 50.3 | 37.1 | 28.5 | -41.3 | 55.0 |
| MOM1 | 2007-15 | 108 | -0.58 | -0.90 | -0.26 | -0.77 | 7.2 | 13.6 | 4.1 | -56.5 | 80.5 |
| MOM1 | 2016-26 | 130 | 1.29 | 1.94 | 0.52 | 1.27 | 34.3 | 32.0 | 21.4 | -38.6 | 77.5 |
| MOM1 | 2021-26 | 70 | 1.87 | 1.94 | 0.62 | 1.06 | 40.1 | 37.1 | 28.5 | -37.4 | 77.9 |
| LOWVOL60 | 2007-15 | 108 | 0.71 | 1.12 | 0.26 | 0.92 | 16.0 | 13.6 | 4.1 | -51.7 | 35.1 |
| LOWVOL60 | 2016-26 | 130 | 0.63 | 0.80 | 0.03 | 0.10 | 31.8 | 32.0 | 21.4 | -27.0 | 33.6 |
| LOWVOL60 | 2021-26 | 70 | 1.86 | 1.56 | 0.55 | 1.22 | 45.2 | 37.1 | 28.5 | -27.0 | 33.6 |
| RESMOM12_1 | 2007-15 | 97 | 1.03 | 1.61 | 0.82 | 1.90 | 21.3 | 11.7 | 4.6 | -54.6 | 29.4 |
| RESMOM12_1 | 2016-26 | 130 | 0.33 | 0.48 | 0.23 | 0.60 | 33.2 | 32.7 | 21.4 | -53.3 | 30.4 |
| RESMOM12_1 | 2021-26 | 70 | -0.99 | -0.95 | -0.48 | -0.85 | 27.8 | 38.5 | 28.5 | -53.3 | 30.5 |

**N = 100 (daha geniş, daha az likit; Q5 ≈ 20 hisse)**

| sinyal | dönem | ay | Q5−Q1 %/ay | t | Q5−EW %/ay | t  | Q5 net CAGR % | EW CAGR % | nakit % | Q5 MaxDD % | devir % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MOM12_1 | 2007-15 | 108 | 0.85 | 1.47 | 0.15 | 0.42 | 15.9 | 14.5 | 4.1 | -51.7 | 26.0 |
| MOM12_1 | 2016-26 | 130 | 0.77 | 1.25 | 0.15 | 0.39 | 33.3 | 34.7 | 21.4 | -53.0 | 26.5 |
| MOM12_1 | 2021-26 | 70 | 0.66 | 0.75 | -0.07 | -0.12 | 29.8 | 36.4 | 28.5 | -53.0 | 27.1 |
| MOM6_1 | 2007-15 | 108 | 0.32 | 0.53 | 0.16 | 0.44 | 15.3 | 14.5 | 4.1 | -51.3 | 36.9 |
| MOM6_1 | 2016-26 | 130 | 0.84 | 1.41 | 0.14 | 0.34 | 32.9 | 34.7 | 21.4 | -55.5 | 36.6 |
| MOM6_1 | 2021-26 | 70 | 1.66 | 1.90 | 0.40 | 0.62 | 36.8 | 36.5 | 28.5 | -55.5 | 36.5 |
| MOM3_1 | 2007-15 | 108 | 0.83 | 1.59 | 0.30 | 0.90 | 16.8 | 14.5 | 4.1 | -52.2 | 55.3 |
| MOM3_1 | 2016-26 | 130 | 0.44 | 0.83 | 0.07 | 0.20 | 31.9 | 34.7 | 21.4 | -51.6 | 55.0 |
| MOM3_1 | 2021-26 | 70 | 0.64 | 0.80 | 0.05 | 0.09 | 31.8 | 36.5 | 28.5 | -51.6 | 56.0 |
| H52 | 2007-15 | 108 | 0.92 | 1.57 | 0.11 | 0.33 | 15.0 | 14.5 | 4.1 | -49.8 | 46.8 |
| H52 | 2016-26 | 130 | 1.46 | 2.31 | 0.66 | 1.89 | 41.3 | 34.7 | 21.4 | -41.3 | 50.6 |
| H52 | 2021-26 | 70 | 3.24 | 3.67 | 1.31 | 2.56 | 52.4 | 36.5 | 28.5 | -41.3 | 52.8 |
| MOM1 | 2007-15 | 108 | 0.16 | 0.33 | 0.06 | 0.20 | 12.6 | 14.5 | 4.1 | -57.0 | 78.2 |
| MOM1 | 2016-26 | 130 | 0.73 | 1.33 | 0.23 | 0.69 | 33.0 | 34.7 | 21.4 | -42.3 | 78.2 |
| MOM1 | 2021-26 | 70 | 1.27 | 1.58 | 0.15 | 0.30 | 32.6 | 36.5 | 28.5 | -42.3 | 78.7 |
| LOWVOL60 | 2007-15 | 108 | 0.40 | 0.83 | 0.03 | 0.14 | 13.9 | 14.5 | 4.1 | -52.0 | 36.5 |
| LOWVOL60 | 2016-26 | 130 | 0.63 | 0.90 | -0.06 | -0.19 | 33.4 | 34.7 | 21.4 | -27.9 | 30.6 |
| LOWVOL60 | 2021-26 | 70 | 1.62 | 1.48 | 0.57 | 1.24 | 45.7 | 36.5 | 28.5 | -27.9 | 30.5 |
| RESMOM12_1 | 2007-15 | 97 | 0.99 | 1.95 | 0.73 | 2.11 | 22.6 | 13.5 | 4.6 | -47.5 | 26.9 |
| RESMOM12_1 | 2016-26 | 130 | 0.71 | 1.32 | 0.14 | 0.45 | 35.6 | 35.8 | 21.4 | -50.5 | 29.2 |
| RESMOM12_1 | 2021-26 | 70 | -0.18 | -0.23 | -0.24 | -0.56 | 31.2 | 37.3 | 28.5 | -50.5 | 28.0 |

**Yalnız VİOP pay vadelisi olan 47 hisse (N=40)** — burada short bacak VİOP ile gerçekten uygulanabilir; ama bugünkü VİOP listesi geçmişin kazananlarından oluştuğu için yukarı yanlı.

| sinyal | dönem | ay | Q5−Q1 %/ay | t | Q5−EW %/ay | t  | Q5 net CAGR % | EW CAGR % | nakit % | Q5 MaxDD % | devir % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MOM12_1 | 2007-15 | 108 | 0.84 | 1.34 | 0.27 | 0.64 | 18.9 | 16.0 | 4.1 | -48.3 | 25.7 |
| MOM12_1 | 2016-26 | 130 | 1.35 | 1.97 | 1.02 | 2.42 | 54.3 | 40.2 | 21.4 | -27.9 | 23.9 |
| MOM12_1 | 2021-26 | 70 | 0.82 | 0.88 | 0.62 | 1.04 | 56.7 | 49.1 | 28.5 | -27.9 | 24.1 |
| MOM6_1 | 2007-15 | 108 | 0.34 | 0.47 | 0.38 | 0.88 | 19.4 | 16.0 | 4.1 | -50.9 | 36.7 |
| MOM6_1 | 2016-26 | 130 | 0.67 | 1.04 | 0.65 | 1.71 | 48.2 | 40.2 | 21.4 | -32.7 | 35.0 |
| MOM6_1 | 2021-26 | 70 | 0.83 | 0.90 | 0.55 | 1.02 | 55.9 | 49.1 | 28.5 | -32.7 | 36.4 |
| MOM3_1 | 2007-15 | 108 | 1.52 | 2.15 | 0.79 | 1.98 | 25.0 | 16.0 | 4.1 | -49.8 | 56.1 |
| MOM3_1 | 2016-26 | 130 | 0.16 | 0.26 | 0.04 | 0.11 | 37.4 | 40.2 | 21.4 | -31.4 | 53.5 |
| MOM3_1 | 2021-26 | 70 | 0.20 | 0.23 | -0.27 | -0.47 | 40.7 | 49.1 | 28.5 | -31.4 | 54.1 |
| H52 | 2007-15 | 108 | 0.38 | 0.56 | 0.04 | 0.09 | 15.3 | 16.0 | 4.1 | -49.3 | 48.9 |
| H52 | 2016-26 | 130 | 0.70 | 1.09 | 0.26 | 0.71 | 40.7 | 40.2 | 21.4 | -26.4 | 52.3 |
| H52 | 2021-26 | 70 | 1.50 | 1.67 | 0.50 | 0.93 | 52.5 | 49.1 | 28.5 | -24.0 | 54.3 |
| MOM1 | 2007-15 | 108 | -0.90 | -1.55 | -0.43 | -1.20 | 7.7 | 16.0 | 4.1 | -50.1 | 81.4 |
| MOM1 | 2016-26 | 130 | 0.77 | 1.27 | 0.40 | 1.05 | 41.3 | 40.2 | 21.4 | -30.4 | 76.2 |
| MOM1 | 2021-26 | 70 | 0.53 | 0.60 | -0.15 | -0.28 | 40.2 | 49.1 | 28.5 | -30.4 | 77.1 |
| LOWVOL60 | 2007-15 | 108 | 0.33 | 0.70 | 0.27 | 1.00 | 18.3 | 16.0 | 4.1 | -54.0 | 32.5 |
| LOWVOL60 | 2016-26 | 130 | -1.10 | -1.85 | -0.29 | -1.09 | 34.3 | 40.2 | 21.4 | -22.1 | 33.7 |
| LOWVOL60 | 2021-26 | 70 | -0.15 | -0.19 | -0.02 | -0.06 | 47.1 | 49.1 | 28.5 | -21.3 | 33.6 |
| RESMOM12_1 | 2007-15 | 97 | 1.33 | 1.98 | 0.93 | 2.18 | 26.6 | 14.7 | 4.6 | -42.6 | 29.8 |
| RESMOM12_1 | 2016-26 | 130 | 1.30 | 2.14 | 0.81 | 2.13 | 51.7 | 40.7 | 21.4 | -38.9 | 27.7 |
| RESMOM12_1 | 2021-26 | 70 | 0.64 | 0.71 | 0.42 | 0.78 | 54.4 | 49.4 | 28.5 | -38.9 | 27.9 |

Yıllara göre (N=60) Q5−EW ve Q5−Q1 farkı (yüzde puan, yıllık bileşik getiri farkı):

| yıl | MOM12_1 Q5−EW | MOM12_1 Q5−Q1 | H52 Q5−EW | H52 Q5−Q1 | RESMOM12_1 Q5−EW | RESMOM12_1 Q5−Q1 | MOM1 Q5−EW | MOM1 Q5−Q1 |
|---|---|---|---|---|---|---|---|---|
| 2007 | +20 | +40 | +3 | +14 | +5 | +7 | +12 | +10 |
| 2008 | +6 | +19 | +3 | +9 | +9 | +15 | -3 | +4 |
| 2009 | -35 | -96 | -10 | -45 | -10 | +30 | +15 | +5 |
| 2010 | -2 | +7 | +5 | +8 | +15 | +6 | -8 | -19 |
| 2011 | +2 | +20 | -2 | +18 | +20 | +17 | -3 | -15 |
| 2012 | -2 | +16 | +1 | +29 | +14 | -21 | -19 | -17 |
| 2013 | +9 | +25 | +17 | +33 | +11 | +26 | +5 | +10 |
| 2014 | -0 | +19 | +5 | +35 | -6 | +8 | -11 | +7 |
| 2015 | +3 | +9 | -1 | +5 | +9 | +11 | -9 | -29 |
| 2016 | -7 | -30 | -1 | -12 | -4 | -0 | +41 | +41 |
| 2017 | +45 | +81 | +19 | +13 | +57 | +94 | +44 | +67 |
| 2018 | -13 | -10 | -7 | -8 | -5 | +1 | -10 | -15 |
| 2019 | +23 | +16 | -1 | -19 | +17 | +11 | -15 | +1 |
| 2020 | +7 | +32 | -7 | +16 | +35 | +54 | -15 | -20 |
| 2021 | -19 | +1 | +2 | +33 | +3 | +25 | +5 | +16 |
| 2022 | -25 | -72 | +121 | +192 | -43 | -129 | +19 | +76 |
| 2023 | +44 | +68 | +37 | +18 | -3 | +6 | -21 | -15 |
| 2024 | -13 | -3 | +16 | +40 | +25 | +40 | +17 | +22 |
| 2025 | +11 | +37 | +12 | +45 | -10 | -57 | +28 | +54 |
| 2026 | -22 | -23 | -9 | +23 | -23 | -29 | -2 | +22 |

Okuma:
- **Evrene duyarlılık (en önemli uyarı):** İndirme sürerken üç kez çalıştırdım. N=60, 2016–26, MOM12_1 Q5−Q1: 106 hisseyle +%1,82/ay (t=2,57) → 181 hisseyle +%0,67 (t=0,95) → 248 hisseyle +%0,54 (t=0,77). Rezidüel momentum da aynı şekilde çöktü (t 3,0 → 0,5). Klasik 12-1 momentum BIST'te evren bileşimine kırılgan; literatürle tutarlı (Ünal 2021: kazananlar geride; Gökçen: yalnız 2005 sonrası).
- **52-hafta zirvesi (H52) korunan tek sinyal:** 248 hisse, N=60: 2016–26 Q5−Q1 +%1,56/ay (t=2,22), Q5−EW +%0,64 (t=1,60); 2021–26 +%3,26 (t=3,29), Q5−EW +%1,23 (t=2,10). N=100: 2016–26 +%1,46 (t=2,31) / +%0,66 (t=1,89); 2021–26 +%3,24 (t=3,67) / +%1,31 (t=2,56). Evren 106 → 181 → 248 iken işaret ve büyüklük korundu.
- Yıllık tabloda H52 Q5−Q1 2016–26'nın 11 yılından 8'inde pozitif (2016, 2018, 2019 negatif); 2022 (+192 puan) çok ağırlıklı. 2022 hariç 2021–26 ortalaması Q5−Q1 ≈ +32, Q5−EW ≈ +12 puan/yıl.
- Q5−Q1 farkının Q5−EW'nin ~2 katı olması, kazancın yarısının **52-hafta zirvesinden uzak (derin düşmüş) hisseleri tutmamaktan** geldiğini gösteriyor. Long-only uygulamada bile "Q1'den kaçın" kuralı değerli.
- MOM1 (1 aylık devam): 2016–26 N=60 +%1,29/ay (t=1,94), N=100 +%0,73 (t=1,33); 2007–15'te negatif. Bildik & Gülay'ın (1991–2000) kısa vadeli zıtlık bulgusunun tersine.
- Rezidüel momentum 2007–15'te çalışıyordu (Q5−EW +%0,73…+%0,82/ay, t≈2), 2016 sonrası sönük, 2021–26 negatif. Düşük vol anlamsız (2021–26 t≈1,5; VİOP-47'de ters).
- VİOP-47 içinde MOM12_1 2016–26 Q5−EW +%1,02/ay (t=2,42), RESMOM +%0,81 (t=2,13): görünüşte iyi, ama bugünkü VİOP listesinin seçim yanlılığına en açık sonuç. H52 VİOP-47 içinde zayıf (t≈1). Yani "VİOP ile kaldıraçlı H52 sepeti" kanıtla desteklenmiyor; H52'nin gücü daha geniş likit evrenden geliyor.
- Long-only, maliyet sonrası: H52 Q5 net CAGR 2016–26 %37–41 (EW %32–35, nakit %21,4); 2021–26 %50–52 (EW %37, nakit %28,5); MaxDD −%41.

### 3.3 Haftalık kısa vadeli dönüş yok; 2016 sonrası **devam** var (kaybedenler kaybetmeye devam ediyor)

Kurulum: her cuma, son 1/2/4 haftalık getiriye göre beşli dilim (en likit N), izleyen hafta getirisi. "Ters" = kaybedenler − kazananlar.

| N | geriye bakış (hafta) | dönem | ters (kaybeden−kazanan) bps/hafta | t | kaybeden−EW bps | kazanan−EW bps | hafta sayısı |
|---|---|---|---|---|---|---|---|
| 60 | 1 | 2007-15 | 24 | 1.67 | 14 | -10 | 469 |
| 60 | 1 | 2016-26 | -54 | -3.27 | -40 | 14 | 565 |
| 60 | 1 | 2021-26 | -86 | -3.40 | -70 | 16 | 304 |
| 60 | 2 | 2007-15 | 8 | 0.53 | 5 | -2 | 469 |
| 60 | 2 | 2016-26 | -62 | -3.87 | -39 | 23 | 565 |
| 60 | 2 | 2021-26 | -88 | -3.65 | -66 | 22 | 304 |
| 60 | 4 | 2007-15 | 6 | 0.41 | 2 | -5 | 469 |
| 60 | 4 | 2016-26 | -50 | -3.05 | -34 | 16 | 565 |
| 60 | 4 | 2021-26 | -71 | -2.86 | -54 | 17 | 304 |
| 100 | 1 | 2007-15 | 8 | 0.70 | 5 | -4 | 469 |
| 100 | 1 | 2016-26 | -51 | -3.80 | -37 | 14 | 565 |
| 100 | 1 | 2021-26 | -71 | -3.51 | -58 | 14 | 304 |
| 100 | 2 | 2007-15 | -12 | -0.99 | -9 | 4 | 469 |
| 100 | 2 | 2016-26 | -46 | -3.41 | -30 | 16 | 565 |
| 100 | 2 | 2021-26 | -59 | -2.90 | -52 | 7 | 304 |
| 100 | 4 | 2007-15 | -15 | -1.17 | -10 | 4 | 469 |
| 100 | 4 | 2016-26 | -51 | -3.73 | -34 | 17 | 565 |
| 100 | 4 | 2021-26 | -60 | -2.89 | -48 | 12 | 304 |

Yorum: 2007–15'te 1 haftalık zayıf dönüş vardı (N=60: +24 bps, t=1,67); 2016 sonrası işaret döndü ve bütün geriye bakış/N kombinasyonlarında t −2,9…−3,9. Asimetri önemli: farkın çoğu **kaybedenlerin EW'nin altında kalmasından** geliyor (−30…−70 bps/hafta), kazananların üstünlüğü küçük (+7…+23 bps). Survivorship bu bulguyu zayıflatma yönünde çalışır (batan kaybedenler örneklemde yok), yani gerçek etki muhtemelen daha güçlü. Mekanik açıklama: ±%10 fiyat limiti (taban serileri), kredili pozisyonların zorunlu kapanışı (kredili işlem faizi %100'e yaklaşan dönemlerde: [Bloomberg HT 12.10.2024](https://www.bloomberght.com/borsayi-kredisi-yuksek-yatirimci-dagitti-2362224)), fon çıkışları (2026'da fon tasfiyeleri). Limit günlerinde işlem yapılamaması modellenmedi; gerçek uygulanabilir fark daha küçük olabilir. Ölçek fikri: 2026'da ODINE 42, PASEU 39, PEKGY 31, MAGEN 24, KONTR 18 gün taban (−%10) kapattı (kendi verim); taban serisinde satış emri karşılanmaz, yani devamın bir kısmı mekanik ve bu hisselerde short da yok. Uygulama: **düşeni "ucuzladı" diye haftalık almak 2016 sonrası BIST'te para kaybettirdi.** Short tarafı yalnız VİOP-47'de mümkün (çoğunda PSR %33,3; ASTOR/HALKB/VESTL %100).

### 3.4 Sektör/endüstri momentumu

BIST sektör endekslerinde endüstri momentumunu doğrudan test eden çalışma bulunamadı (Moskowitz & Grinblatt 1999 ABD'de bireysel momentumun büyük kısmını endüstriye bağlıyor; [Quantpedia özeti](https://quantpedia.com/strategies/sector-momentum-rotational-system)). Sektör eşlemesi gerektirdiği için test etmedim. Kullanıcının "stratejik kümelenme" yaklaşımı pratikte tema/sektör momentumu; 3.2'deki rezidüel momentum ve 52-hafta sonuçları bu yaklaşımın hisse düzeyindeki karşılığıdır.

---

## 4. Endeks düzeyi trend takibi / zaman serisi momentumu (XU100, XU030 vadeli vekili)

Kurulum: XU100 kapanışında sinyal, ertesi gün uygulanır. Pozisyon vadeli gibi modellendi: teminat TL nakitte, getiri = nakit + w×(XU100 − nakit) (vadeli ≈ spot×(1+r), temettü ihmal). Short taraf (L/S) vadeli short: 2×nakit − endeks. Yön değişimi başına %0,10 maliyet. vt25 = 20 gün gerçekleşen vol ile %25 hedef, kaldıraç ≤1,5.

| kural | yön | vol hedef | 2010-26 CAGR | 2010-26 MaxDD | 2010-26 Sharpe | 2011-18 CAGR | 2011-18 MaxDD | 2019-26 CAGR | 2019-26 MaxDD | 2023-26 CAGR | 2023-26 MaxDD | 2023-26 Sharpe |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SMA200 | L/nakit | - | 18.0 | -45.9 | 0.15 | 3.2 | -45.9 | 34.5 | -22.3 | 24.6 | -22.3 | -0.23 |
| SMA200 | L/S | - | 12.9 | -69.5 | -0.02 | -1.6 | -69.5 | 29.2 | -36.2 | 26.6 | -23.1 | -0.13 |
| SMA100 | L/nakit | - | 19.1 | -36.5 | 0.19 | 3.3 | -36.5 | 36.7 | -21.0 | 25.6 | -21.0 | -0.26 |
| SMA100 | L/S | - | 14.4 | -57.3 | 0.04 | -1.4 | -57.3 | 32.2 | -32.0 | 26.8 | -32.0 | -0.12 |
| SMA50x200 | L/nakit | - | 19.0 | -31.8 | 0.19 | 8.3 | -24.2 | 30.4 | -31.8 | 20.7 | -22.3 | -0.34 |
| SMA50x200 | L/S | - | 15.3 | -47.4 | 0.07 | 8.7 | -36.3 | 22.0 | -47.4 | 19.4 | -26.4 | -0.34 |
| TSMOM252 | L/nakit | - | 25.8 | -38.8 | 0.49 | 6.3 | -38.8 | 48.2 | -22.3 | 38.0 | -22.3 | 0.15 |
| TSMOM252 | L/nakit | vt25 | 24.8 | -49.5 | 0.44 | 6.1 | -49.5 | 46.1 | -26.1 | 30.2 | -20.9 | -0.16 |
| TSMOM252 | L/S | - | 27.5 | -56.8 | 0.47 | 4.4 | -56.8 | 54.9 | -27.1 | 52.8 | -27.1 | 0.53 |
| TSMOM252 | L/S | vt25 | 26.2 | -67.2 | 0.42 | 4.0 | -67.2 | 52.5 | -36.8 | 42.2 | -36.8 | 0.28 |
| TSMOM126 | L/nakit | - | 22.0 | -31.6 | 0.33 | 6.1 | -31.6 | 39.8 | -24.7 | 26.1 | -24.7 | -0.27 |
| TSMOM126 | L/S | - | 19.7 | -48.8 | 0.22 | 3.8 | -48.8 | 37.5 | -47.1 | 27.2 | -47.1 | -0.11 |
| TSMOM63 | L/nakit | - | 21.3 | -29.1 | 0.30 | 5.3 | -29.1 | 39.1 | -20.8 | 33.6 | -20.8 | -0.03 |
| TSMOM63 | L/S | - | 17.9 | -48.6 | 0.16 | 2.2 | -48.6 | 35.6 | -34.4 | 41.3 | -34.4 | 0.26 |
| Donchian55_20 | L/nakit | - | 21.9 | -20.9 | 0.36 | 7.5 | -20.9 | 37.8 | -20.8 | 34.2 | -16.7 | -0.04 |
| Donchian55_20 | L/S | - | 18.4 | -38.8 | 0.17 | 5.9 | -38.8 | 32.0 | -33.4 | 40.9 | -22.2 | 0.25 |
| USD_SMA200 | L/nakit | - | 13.1 | -27.6 | -0.13 | 9.1 | -24.5 | 17.0 | -27.6 | 10.2 | -27.6 | -0.87 |
| USD_SMA200 | L/S | - | 2.3 | -71.2 | -0.42 | 9.5 | -48.4 | -4.3 | -71.2 | -2.7 | -59.9 | -1.06 |
| BuyHold | L/nakit | - | 20.7 | -34.3 | 0.25 | 5.0 | -34.3 | 38.2 | -31.8 | 20.8 | -28.9 | -0.29 |

Nakit (TL politika faizi) CAGR: 2010-26 %16.9, 2011-18 %8.9, 2019-26 %25.4, 2023-26 %36.7

Yıllık (TL, %):

| yıl | TSMOM252 L/nakit | TSMOM252 L/S | Donchian L/S | XU100 | nakit |
|---|---|---|---|---|---|
| 2017 | 43.5 | 39.2 | 6.0 | 47.6 | 12.4 |
| 2018 | 2.0 | 26.6 | 33.1 | -20.9 | 17.5 |
| 2019 | 26.1 | 21.7 | 4.2 | 25.4 | 20.5 |
| 2020 | 38.7 | 43.7 | 23.9 | 29.1 | 10.2 |
| 2021 | 20.8 | 15.8 | 7.1 | 25.8 | 17.7 |
| 2022 | 196.6 | 196.6 | 69.9 | 196.6 | 12.9 |
| 2023 | 38.0 | 40.1 | 38.7 | 35.6 | 17.9 |
| 2024 | 63.9 | 98.3 | 18.6 | 31.6 | 49.1 |
| 2025 | 43.5 | 69.5 | 25.9 | 14.6 | 43.5 |
| 2026 | 5.2 | 6.7 | 78.3 | 0.6 | 30.6 |

Okuma:
- **Rejime çok bağımlı.** 2011–18'de (düşük nominal faiz, sık yön değişimi) TL bazlı hiçbir kural TL nakdi (%8,9) geçemedi (en iyi SMA50x200 %8,3–8,7); yalnız USD bazlı SMA200 kılpayı geçti (%9,1–9,5). 2019–26'da 12 aylık TSMOM long/nakit %48,2 (nakit %25,4, al-tut %38,2), L/S %54,9.
- **2023–26 (pozitif reel faiz):** al-tut %20,8 ile nakdin (%36,7) 16 puan altında. Nakdi belirgin geçenler yalnız L/S sürümler: 12 aylık TSMOM L/S (%52,8, MaxDD −%27, Sharpe 0,53), TSMOM63 L/S (%41,3) ve Donchian 55/20 L/S (%40,9). Sebep: short vadeli + teminat PPF = 2×nakit − endeks (bkz. 8.2). Yani 2024–26'da "kazanan" trend takipçisi aslında **çoğu zaman nakitte/shortta oturan** kişiydi.
- Vol hedefsiz 18 kural varyantından 2023–26'da nakdi geçen 4 tane var (TSMOM252 L/nakit ve L/S, TSMOM63 L/S, Donchian L/S); medyan varyant nakdin ~10 puan altında. Tek bir kuralın (TSMOM252) seçilmesi örneklem içi seçimdir; ama 12 ay TSMOM'un küresel literatürde de ana spesifikasyon olması (Moskowitz-Ooi-Pedersen 2012) veri madenciliği riskini azaltıyor.
- Yıllık kırılım 2024–26'nın ne kadar oynak olduğunu gösteriyor: TSMOM252 L/S 2024 +%98 (nakit %49), 2025 +%70 (nakit %44), 2026 YTD +%7 (nakit %31; Nisan–Haziran sahte sinyal); Donchian L/S 2026 YTD +%78 ama 2024'te +%19. Kurallar arası dağılım büyük → tek kurala güvenmek yerine 2–3 kuralın ortalaması.
- Vol hedefleme (%25) BIST'te getiriyi artırmadı, MaxDD'yi de düşürmedi (gap riski ve limitli günler; 20 günlük vol gecikmeli).
- USD bazlı trend (XU100/USDTRY > SMA200) TL'de anlamsız; USD yatırımcısı için ayrı soru.
- **Bugünkü durum (05.11.2026):** XU100 11.333; 12 aylık getiri +%3,3, aynı dönem TL nakdi +%37,3; SMA200 = 13.572. Rejim filtresi Temmuz 2026'dan beri **kapalı** (2025'in tamamında kapalı, 2026'da yalnız Nisan–Haziran açık).

Literatür: Ülkü (2009), *ISE Review* 11(41): Brock-Lakonishok-LeBaron kuralları DJIA'da kayboldu, ISE-100'de daha iyi; 22 günlük SMA ISE-100'de **maliyet sonrası anlamlı pozitif** ([IDEAS](https://ideas.repec.org/a/bor/iserev/v11y2009i41p25-44.html)). 2023 tarihli 41 endeksli SPP testi: tek yön ≥20 bps maliyette yalnız 4 gelişmekte olan piyasada anlamlı kural kaldı ([Springer FMPM 2023](https://link.springer.com/10.1007/s11408-023-00433-2)). Küresel TSMOM kanıtı (Moskowitz-Ooi-Pedersen; "Trends Everywhere" brüt Sharpe 1,6 çoklu varlık) Türkiye'yi ayrı raporlamıyor ([Quantpedia](https://quantpedia.com/time-series-momentum-works-everywhere/)).

### 4.1 Kombinasyon: hisse seçimi (momentum/52-hafta) + piyasa rejim filtresi

En umut verici bulgu bu. Ay sonu XU100'ün 12 aylık getirisi aynı dönemin TL nakit getirisini aşıyorsa (TSMOM12) ya da XU100 > SMA200 ise Q5'e (N=60 ≈ 12 hisse; N=100 ≈ 20 hisse) gir, değilse nakit. Rejim geçişinde ek %0,3 maliyet.

| N | sinyal | rejim filtresi | dönem | CAGR % | nakit % | EW evren % | MaxDD % | Sharpe (nakit üstü) | en kötü ay % |
|---|---|---|---|---|---|---|---|---|---|
| 60 | MOM12_1 | yok | 2010-26 | 23.6 | 16.2 | 25.1 | -55.0 | 0.35 | -38.0 |
| 60 | MOM12_1 | yok | 2016-26 | 28.2 | 21.4 | 32.0 | -55.0 | 0.33 | -38.0 |
| 60 | MOM12_1 | yok | 2023-26 | 9.1 | 36.2 | 15.7 | -55.0 | -0.31 | -38.0 |
| 60 | MOM12_1 | TSMOM12 | 2010-26 | 29.5 | 16.2 | 25.1 | -25.7 | 0.55 | -17.6 |
| 60 | MOM12_1 | TSMOM12 | 2016-26 | 42.0 | 21.4 | 32.0 | -25.7 | 0.67 | -17.6 |
| 60 | MOM12_1 | TSMOM12 | 2023-26 | 43.2 | 36.2 | 15.7 | -21.0 | 0.30 | -12.2 |
| 60 | MOM12_1 | SMA200 | 2010-26 | 25.3 | 16.2 | 25.1 | -38.0 | 0.40 | -38.0 |
| 60 | MOM12_1 | SMA200 | 2016-26 | 29.1 | 21.4 | 32.0 | -38.0 | 0.34 | -38.0 |
| 60 | MOM12_1 | SMA200 | 2023-26 | 22.8 | 36.2 | 15.7 | -38.0 | -0.07 | -38.0 |
| 60 | H52 | yok | 2010-26 | 30.1 | 16.2 | 25.1 | -41.3 | 0.50 | -31.0 |
| 60 | H52 | yok | 2016-26 | 37.4 | 21.4 | 32.0 | -41.3 | 0.51 | -31.0 |
| 60 | H52 | yok | 2023-26 | 22.3 | 36.2 | 15.7 | -41.3 | -0.08 | -31.0 |
| 60 | H52 | TSMOM12 | 2010-26 | 33.3 | 16.2 | 25.1 | -26.2 | 0.67 | -13.2 |
| 60 | H52 | TSMOM12 | 2016-26 | 48.8 | 21.4 | 32.0 | -26.2 | 0.83 | -12.8 |
| 60 | H52 | TSMOM12 | 2023-26 | 49.7 | 36.2 | 15.7 | -26.2 | 0.45 | -12.8 |
| 60 | H52 | SMA200 | 2010-26 | 29.3 | 16.2 | 25.1 | -35.1 | 0.50 | -31.0 |
| 60 | H52 | SMA200 | 2016-26 | 34.4 | 21.4 | 32.0 | -35.1 | 0.45 | -31.0 |
| 60 | H52 | SMA200 | 2023-26 | 26.2 | 36.2 | 15.7 | -35.1 | -0.01 | -31.0 |
| 60 | RESMOM12_1 | yok | 2010-26 | 30.2 | 16.2 | 25.7 | -53.3 | 0.51 | -29.7 |
| 60 | RESMOM12_1 | yok | 2016-26 | 33.2 | 21.4 | 32.7 | -53.3 | 0.43 | -29.7 |
| 60 | RESMOM12_1 | yok | 2023-26 | 9.0 | 36.2 | 17.9 | -53.3 | -0.43 | -29.7 |
| 60 | RESMOM12_1 | TSMOM12 | 2010-26 | 32.1 | 16.2 | 25.7 | -28.6 | 0.67 | -18.0 |
| 60 | RESMOM12_1 | TSMOM12 | 2016-26 | 46.0 | 21.4 | 32.7 | -28.0 | 0.83 | -14.9 |
| 60 | RESMOM12_1 | TSMOM12 | 2023-26 | 40.8 | 36.2 | 17.9 | -14.9 | 0.25 | -10.3 |
| 60 | RESMOM12_1 | SMA200 | 2010-26 | 29.6 | 16.2 | 25.7 | -35.9 | 0.54 | -29.7 |
| 60 | RESMOM12_1 | SMA200 | 2016-26 | 32.6 | 21.4 | 32.7 | -35.9 | 0.43 | -29.7 |
| 60 | RESMOM12_1 | SMA200 | 2023-26 | 19.5 | 36.2 | 17.9 | -35.9 | -0.24 | -29.7 |
| 100 | MOM12_1 | yok | 2010-26 | 29.0 | 16.2 | 27.4 | -53.0 | 0.48 | -40.1 |
| 100 | MOM12_1 | yok | 2016-26 | 33.3 | 21.4 | 34.7 | -53.0 | 0.43 | -40.1 |
| 100 | MOM12_1 | yok | 2023-26 | 11.7 | 36.2 | 17.4 | -53.0 | -0.26 | -40.1 |
| 100 | MOM12_1 | TSMOM12 | 2010-26 | 31.1 | 16.2 | 27.4 | -26.0 | 0.61 | -17.3 |
| 100 | MOM12_1 | TSMOM12 | 2016-26 | 42.1 | 21.4 | 34.7 | -26.0 | 0.68 | -17.3 |
| 100 | MOM12_1 | TSMOM12 | 2023-26 | 38.9 | 36.2 | 17.4 | -25.5 | 0.20 | -14.0 |
| 100 | MOM12_1 | SMA200 | 2010-26 | 30.2 | 16.2 | 27.4 | -40.1 | 0.54 | -40.1 |
| 100 | MOM12_1 | SMA200 | 2016-26 | 33.5 | 21.4 | 34.7 | -40.1 | 0.45 | -40.1 |
| 100 | MOM12_1 | SMA200 | 2023-26 | 22.6 | 36.2 | 17.4 | -40.1 | -0.06 | -40.1 |
| 100 | H52 | yok | 2010-26 | 33.3 | 16.2 | 27.4 | -41.3 | 0.59 | -34.2 |
| 100 | H52 | yok | 2016-26 | 41.3 | 21.4 | 34.7 | -41.3 | 0.60 | -34.2 |
| 100 | H52 | yok | 2023-26 | 26.6 | 36.2 | 17.4 | -41.3 | -0.00 | -34.2 |
| 100 | H52 | TSMOM12 | 2010-26 | 35.7 | 16.2 | 27.4 | -21.4 | 0.76 | -12.6 |
| 100 | H52 | TSMOM12 | 2016-26 | 52.3 | 21.4 | 34.7 | -19.1 | 0.94 | -12.6 |
| 100 | H52 | TSMOM12 | 2023-26 | 52.3 | 36.2 | 17.4 | -18.4 | 0.52 | -10.9 |
| 100 | H52 | SMA200 | 2010-26 | 33.6 | 16.2 | 27.4 | -34.2 | 0.63 | -34.2 |
| 100 | H52 | SMA200 | 2016-26 | 39.5 | 21.4 | 34.7 | -34.2 | 0.57 | -34.2 |
| 100 | H52 | SMA200 | 2023-26 | 31.9 | 36.2 | 17.4 | -34.2 | 0.10 | -34.2 |
| 100 | RESMOM12_1 | yok | 2010-26 | 32.7 | 16.2 | 28.4 | -50.5 | 0.59 | -32.8 |
| 100 | RESMOM12_1 | yok | 2016-26 | 35.6 | 21.4 | 35.8 | -50.5 | 0.50 | -32.8 |
| 100 | RESMOM12_1 | yok | 2023-26 | 11.3 | 36.2 | 18.6 | -50.5 | -0.41 | -32.8 |
| 100 | RESMOM12_1 | TSMOM12 | 2010-26 | 33.6 | 16.2 | 28.4 | -27.9 | 0.75 | -14.2 |
| 100 | RESMOM12_1 | TSMOM12 | 2016-26 | 45.5 | 21.4 | 35.8 | -27.9 | 0.84 | -14.2 |
| 100 | RESMOM12_1 | TSMOM12 | 2023-26 | 34.6 | 36.2 | 18.6 | -14.8 | 0.06 | -10.1 |
| 100 | RESMOM12_1 | SMA200 | 2010-26 | 30.9 | 16.2 | 28.4 | -37.1 | 0.59 | -32.8 |
| 100 | RESMOM12_1 | SMA200 | 2016-26 | 33.7 | 21.4 | 35.8 | -37.1 | 0.47 | -32.8 |
| 100 | RESMOM12_1 | SMA200 | 2023-26 | 18.2 | 36.2 | 18.6 | -37.1 | -0.29 | -32.8 |

Yıllık (TL, %; N=100 ve N=60, 52-hafta + TSMOM12 rejim filtresi):

| yıl | H52+rejim N100 | H52 filtresiz N100 | EW evren N100 | H52+rejim N60 | nakit | rejim açık ay N100 |
|---|---|---|---|---|---|---|
| 2010 | 4.8 | 30.5 | 27.9 | 4.8 | 4.8 | 0 |
| 2011 | 4.8 | -2.1 | -5.7 | 7.6 | 6.0 | 2 |
| 2012 | 17.7 | 30.8 | 36.4 | 19.9 | 5.7 | 5 |
| 2013 | -1.3 | -9.3 | -15.0 | 0.5 | 4.8 | 9 |
| 2014 | 17.4 | 63.6 | 51.1 | 6.1 | 8.9 | 4 |
| 2015 | 5.2 | -3.2 | -2.0 | 5.2 | 7.5 | 4 |
| 2016 | 12.8 | 9.3 | 24.6 | 13.7 | 7.8 | 1 |
| 2017 | 44.2 | 53.4 | 47.5 | 47.8 | 12.7 | 11 |
| 2018 | -7.0 | -30.3 | -19.2 | -6.1 | 18.4 | 3 |
| 2019 | 32.3 | 69.8 | 64.4 | 22.4 | 19.5 | 1 |
| 2020 | 101.1 | 82.4 | 68.8 | 64.2 | 10.5 | 6 |
| 2021 | 24.1 | 24.1 | 23.4 | 24.7 | 17.6 | 12 |
| 2022 | 280.9 | 280.9 | 169.0 | 299.1 | 12.5 | 12 |
| 2023 | 108.5 | 108.5 | 78.6 | 102.0 | 20.9 | 12 |
| 2024 | 44.3 | 25.3 | 6.0 | 37.4 | 49.2 | 7 |
| 2025 | 42.6 | 53.0 | 36.3 | 42.6 | 42.6 | 0 |
| 2026 | 17.0 | -38.3 | -28.4 | 18.6 | 27.2 | 3 |

- **Rejim filtresi işin çoğunu yapıyor.** H52 filtresiz 2023–26'da %22–27 (nakit %36,2'nin altında, MaxDD −%41); TSMOM12 filtreli %50–52 (MaxDD −%18…−%26). SMA200 filtresi belirgin kötü (2023–26 %26–32): filtre seçimine duyarlılık var.
- 2010–26: H52 + TSMOM12 %33–36 CAGR (nakit %16,2, EW evren %25–27); 2016–26 %49–52 (nakit %21,4), Sharpe 0,83–0,94. MOM12_1 + TSMOM12 %42 (2016–26); RESMOM + TSMOM12 %45–46.
- **Getiri birkaç rejim-açık yılda yoğun** (N=100: 2017 +%44, 2020 +%101, 2022 +%281, 2023 +%109). **2024, 2025, 2026'da nakdi geçemedi** (2024 %44,3 vs %49,2; 2025 tamamen nakitte %42,6; 2026 YTD %17,0 vs %27,2). Pozitif reel faiz rejiminde en iyi uzun-hisse kombinasyonu bile nakit kadar ya da altında.
- 2026'da rejim Nisan–Haziran açıldı ve kaybettirdi (sahte sinyal); EW evren 2026'da −%28 (fon tasfiyesi kaynaklı küçük/orta ölçek satışı ile tutarlı), XU100 ise ~%0.
- Backtest iskontosu: 3 sinyal × 3 filtre × 2 N = 18 kombinasyondan seçim; survivorship; 12–20 hisselik eşit ağırlıklı sepet aylık yenileme. Gerçekçi beklenti: rejim açık yıllarda nakit +20…+60 puan, kapalı yıllarda nakit −0…−10 puan; uzun dönem ortalaması nakit +8…+15 puan; MaxDD −%25…−%35.

---

## 5. Olaylar

### 5.1 Bedelsiz sermaye artırımı

Literatür:
- Küçüksille & Mizrahi (2015), *Sosyal ve Beşeri Bilimler Araştırmaları Dergisi* 35, 2012–2014, olay penceresi (−5,+5): duyuru sonrası anlamlı pozitif AAR yok; ≥%100 bedelsizlerde +4. gün anlamlı negatif; pencere içinde bazı alt aralıklarda pozitif KAAR ([DergiPark](https://dergipark.org.tr/en/download/article-file/452850)).
- Işıker & Taş (2021), *Journal of Capital Markets Studies* 5(1): iç kaynaklardan (sermaye düzeltmesi/emisyon primi) bedelsiz duyuruları, geçmiş yıl karından yapılanlardan daha yüksek duyuru getirisi; büyük oranlar daha iyi karşılanıyor; KAP 2010 öncesi veri yok ([IDEAS](https://ideas.repec.org/a/eme/jcmspp/jcms-03-2021-0008.html)). Rakamlar tam metinde, doğrulanmadı.
- SPK onay tarihli çalışma (2016–2017): onay sonrası 2., 3. ve 5. günlerde anlamlı negatif KAAR (arama özetinden; [DergiPark sobbiad 412528](https://dergipark.org.tr/en/pub/sobbiad/issue/36421/412528) ile eşleşmesi doğrulanmadı).

Kendi testim (bölünme/hak kullanım günü; fiyat düzeltme faktörü k = (ham/düzeltilmiş)ₜ₋₁ / (ham/düzeltilmiş)ₜ ≥ 1,15 olan günler "sermaye artırımı hak kullanımı"; bedelli de içerebilir ama likit adlarda çoğu bedelsiz; piyasa-düzeltmeli = hisse − XU100):

Ortalama:

| grup | n | [-20,-1] ort % | [-5,-1] ort % | [0] ort % | [+1,+5] ort % | [+1,+20] ort % | [+1,+60] ort % | [0,+60] ort % |
|---|---|---|---|---|---|---|---|---|
| SA tumu | 410 | 2.8 | 1.2 | 2.4 | -2.0 | -1.1 | -0.5 | 1.5 |
| SA 2010-17 | 114 | 0.6 | 0.3 | 8.1 | -1.7 | -1.5 | -4.2 | 2.2 |
| SA 2018-22 | 121 | 4.9 | 0.7 | 0.7 | -2.6 | -2.0 | -2.6 | -1.9 |
| SA 2023-26 | 175 | 2.8 | 2.2 | -0.1 | -1.8 | -0.2 | 3.6 | 3.3 |
| SA k<2 (<%100) | 196 | 2.9 | 0.8 | 0.6 | -1.2 | -0.0 | 0.4 | 1.0 |
| SA k 2-5 | 152 | 3.7 | 2.1 | 2.3 | -3.6 | -2.9 | 1.1 | 1.9 |
| SA k>=5 (>=%400) | 62 | 0.6 | 0.5 | 8.5 | -0.8 | 0.3 | -7.4 | 2.1 |
| SA likit ust yari | 205 | 2.5 | 0.9 | -0.0 | -0.8 | 1.0 | 2.7 | 2.7 |

Medyan:

| grup | [-20,-1] medyan % | [-5,-1] medyan % | [0] medyan % | [+1,+5] medyan % | [+1,+20] medyan % | [+1,+60] medyan % | [0,+60] medyan % |
|---|---|---|---|---|---|---|---|
| SA tumu | 1.4 | 0.5 | -0.4 | -2.6 | -4.1 | -5.3 | -4.7 |
| SA 2010-17 | 0.4 | 0.1 | 0.0 | -2.4 | -4.3 | -4.9 | -3.8 |
| SA 2018-22 | 2.4 | 0.7 | -0.2 | -2.7 | -4.3 | -5.6 | -6.7 |
| SA 2023-26 | 2.6 | 0.8 | -0.9 | -2.9 | -3.9 | -5.6 | -4.8 |
| SA k<2 (<%100) | 0.7 | 0.2 | -0.2 | -1.5 | -2.0 | -3.4 | -2.7 |
| SA k 2-5 | 2.6 | 1.1 | -0.9 | -3.4 | -6.0 | -5.6 | -4.3 |
| SA k>=5 (>=%400) | 1.5 | 0.8 | -0.4 | -4.9 | -6.0 | -14.0 | -14.7 |
| SA likit ust yari | 1.9 | -0.1 | -0.9 | -2.2 | -3.6 | -5.6 | -5.6 |

t-istatistiği (ortalama):

| grup | [-20,-1] t | [-5,-1] t | [0] t | [+1,+5] t | [+1,+20] t | [+1,+60] t | [0,+60] t |
|---|---|---|---|---|---|---|---|
| SA tumu | 3.68 | 2.92 | 1.69 | -3.23 | -0.76 | -0.23 | 0.62 |
| SA 2010-17 | 0.54 | 0.46 | 1.60 | -0.97 | -0.46 | -2.16 | 0.46 |
| SA 2018-22 | 2.87 | 0.83 | 1.23 | -3.42 | -1.17 | -0.95 | -0.66 |
| SA 2023-26 | 2.53 | 3.22 | -0.21 | -2.41 | -0.07 | 0.89 | 0.83 |
| SA k<2 (<%100) | 3.02 | 1.72 | 1.39 | -1.96 | -0.02 | 0.15 | 0.34 |
| SA k 2-5 | 2.47 | 2.53 | 1.14 | -4.42 | -1.94 | 0.32 | 0.55 |
| SA k>=5 (>=%400) | 0.31 | 0.41 | 1.07 | -0.25 | 0.05 | -1.76 | 0.21 |
| SA likit ust yari | 2.15 | 1.53 | -0.02 | -0.73 | 0.37 | 0.77 | 0.75 |

- 410 olay (2010–26). Hak kullanımından önceki 20 gün ortalama +%2,8 (t=3,7; medyan +%1,4), son 5 gün +%1,2 (t=2,9); 2023–26'da son 5 gün +%2,2 (t=3,2).
- Hak kullanımı sonrası 5 gün −%2,0 (t=−3,2; medyan −%2,6); 60 günde medyan −%5,3 (ortalama −%0,5, sağa çarpık). %100–400 arası bedelsizlerde +1…+5 gün −%3,6 (t=−4,4); ≥%400'lerde 60 gün medyan −%14.
- Likit üst yarıda öncesi koşu var (+%2,5, t=2,2), sonrası düşüş zayıf (−%0,8, t=−0,7): sonrası düşüş ağırlıkla sığ hisselerde; VİOP short ile hasat güvenilir değil.
- [0] günü ortalamaları (ör. ≥%400'de +%8,5) düzeltme artefaktı olabilir; medyanlar ~0. Bu sütun yorumlanmamalı.
- Uygulama: hak kullanım tarihi ilan edilince al, hak kullanım gününden önceki kapanışta sat; brüt ~%1–3/olay, maliyet ~%0,3. **"Bedelsiz sonrası yükselir" folkloru verilerde yok**: medyan hisse sonraki 1–3 ayda piyasanın gerisinde.
- Asıl popüler işlem (YK kararı → SPK onayı arası) test edilmedi; literatür orada da anlamlı pozitif sürüklenme bulmuyor (Küçüksille & Mizrahi 2015) ve SPK onayından sonraki günlerde negatif KAAR buluyor (2016–17).

### 5.2 Bedelli sermaye artırımı
Arama özetinde 2017–2022 bedelli artırımlarında negatif KAAR bulan bir çalışma görüldü; tam metin ve rakam doğrulanmadı. Kendi testimde bedelli ve bedelsiz ayrılamadı. Hüküm: kanıt zayıf, ticari kenar olarak kullanılmamalı.

### 5.3 Temettü (hak kullanım günü etrafı)

Kendi testim (1,02 < k < 1,15, temettü kaynaklı düzeltme):

| grup | n | [-20,-1] ort % | [-5,-1] ort % | [0] ort % | [+1,+5] ort % | [+1,+20] ort % | [+1,+60] ort % | [0,+60] ort % | [-20,-1] medyan % | [-5,-1] medyan % | [0] medyan % | [+1,+5] medyan % | [+1,+20] medyan % | [+1,+60] medyan % | [0,+60] medyan % | [-20,-1] t | [-5,-1] t | [0] t | [+1,+5] t | [+1,+20] t | [+1,+60] t | [0,+60] t |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| temettu k>1.02 | 1109 | 2.4 | 1.2 | 0.2 | -0.6 | -0.4 | 1.3 | 1.5 | 1.4 | 0.8 | 0.3 | -0.8 | -0.8 | -1.4 | -0.7 | 7.18 | 7.81 | 3.07 | -3.91 | -1.60 | 2.33 | 2.77 |

- 1.109 olay (1,02 < k < 1,15). Hak kullanımından önceki 20 gün +%2,4 (t=7,2; medyan +%1,4), son 5 gün +%1,2 (t=7,8; medyan +%0,8); sonraki 5 gün −%0,6 (t=−3,9). Test ettiğim en yüksek t-istatistikli olay düzenliliği.
- Uygulama: temettü tarihleri genel kurul/KAP ile haftalar önce bilinir. 5–20 gün önce al, hak kullanım gününden önceki kapanışta sat (temettü stopajını ve hak kullanım düşüşünü almamak için) → brüt +%1,2…+%2,4/olay, maliyet ~%0,3. Nisan–Haziran'da yoğun; sermaye yılın ancak bir bölümünde çalışır. Portföy katkısı kabaca +%3–6/yıl.
- Duyuru tarihi etkisi için literatür taraması bütçe nedeniyle yapılamadı.

### 5.4 Pay geri alım duyuruları
- Ayan Civelek & Konak, BIST Sınai, 34 şirket, 01.2014–01.2020: duyuru günü ve +1 günde pozitif AAR (~+%0,55/+%0,56), sonrasında belirgin eğilim yok; duyuru öncesi 20 günde ağırlıkla negatif AAR (geri alımlar düşüş sonrası geliyor) ([DergiPark PDF](https://dergipark.org.tr/en/download/article-file/2325701)). Tabloda t-istatistikleri ile p-değerleri tutarsız; kalite düşük.
- Torun & Karan (2023), 2018–2021, 74 duyuru: fiyat etkisi var; Arsoy (2010–2015): anlamlı KAAR yok ([AGÜ GCRIS](https://gcris.agu.edu.tr/items/20b376f3-fd7e-4eb6-9977-ddf61abc2b3b)).
- Hüküm: 1–2 günlük duyuru tepkisi; swing ufkunda kenar yok. Kriz dönemlerinde (piyasa −%20) toplu geri alım ilanları dip sinyali gibi algılanıyor ama sistematik test bulunamadı.

### 5.5 İçeriden alım (KAP pay alım-satım bildirimi)
- Avcı (2024), *European Journal of Finance* 30(6): 2008–2019, ~65.000 içeriden işlem; içeriden işlemi izleyen 1 yılda **%6,58 anormal kâr**; yöneticiler, büyük ortaklar ve kurumlar daha fazla; alım ve satım ikisi de karlı; **bilgisiz yatırımcı içeriden portföyü taklit ederek piyasayı yenebilir**; düzenleme değişiklikleri kârı azaltmamış ([Sabancı repo](https://research.sabanciuniv.edu/id/eprint/50115), DOI 10.1080/1351847X.2023.2216730). Çalışma kağıdı: (0,5) penceresinde %1,56 ([Scribd SSRN 3896937 kopyası](https://www.scribd.com/document/532198970/SSRN-id3896937)).
- METU tezi: net içeriden alımı izlemek genelde güvenilir pozitif anormal getiri vermiyor, kısa pencerelerde küçük kazanç; net satış portföyleri uzun tutuşta anlamlı negatif ([METU](https://open.metu.edu.tr/handle/11511/19162)).
- Hüküm: BIST'te belgelenmiş en iyi "bilgi" kenarlarından biri, ama yıllık ~%6,6 anormal (brüt), olay başı küçük; swing ufkunda tek başına engelin üstüne taşımaz, filtre/kümelenme kriteri olarak değerli (özellikle büyük ortak alımları + momentum).

### 5.6 Halka arz sonrası (tavan serisi ve dönüş)
Literatür (arama özetlerinden; hangi bulgunun hangi makaleye ait olduğu tam metinden doğrulanmadı): 1993–2020, 347 halka arz: kısa vadede düşük fiyatlama, 36 ayda negatif aşırı getiri; 2010–01/2020 uzun dönem kümülatif piyasa-düzeltmeli getiri XU100'e göre −%10,56, XU30'a göre −%12; 2020 kohortunda ilk gün AAR >%10, 7 günlük KAAR ~%70 ([Beykent](https://earsiv.beykent.edu.tr/items/1c99c9a6-3232-4866-8de0-10434a562ce6/full), [Bakırhan & Sayılgan, Ankara SBF erken görünüm](https://sbfdergi.ankara.edu.tr/dergi/erken_gorunum/2028---Cafer-Bakirhan---Guven-Sayilgan.pdf)). Tam metinden doğrulanan: 65 halka arzda düşük fiyatlama ile 3 yıllık getiri arasında −%29,5 korelasyon, 3 yılda düşük performans, 4. yılda toparlanma eğilimi (*Paradoks* 16(1), 2020, [DergiPark](https://dergipark.org.tr/en/download/article-file/1042951)). Tütüncü & Uzunel (2020): 2010–2017 halka arzları faaliyet performansında eşlenik şirketlerin gerisinde ([DergiPark](https://dergipark.org.tr/en/download/article-file/1271957)).

Kendi testim (2020–2024'te kote olan ve hâlâ işlem gören 69 hisse; seçim benim, yanlı): "tavan serisi" = 2. günden itibaren ardışık ≥%9,5 günler.

| pencere (XU100'e göre) | n | ort % | medyan % | pozitif % |
|---|---|---|---|---|
| 1. gün kapanış → +20 gün | 69 | 57.4 | 27.9 | 72.5 |
| 1. gün → +60 | 69 | 70.1 | 36.3 | 68.1 |
| 1. gün → +250 | 69 | 82.1 | 23.3 | 59.4 |
| tavan serisi bitişi → +20 | 69 | 0.5 | -5.5 | 36.2 |
| seri bitişi → +60 | 69 | 11.7 | -2.6 | 46.4 |
| seri bitişi → +120 | 69 | 14.0 | -5.0 | 47.8 |
| seri bitişi → +250 | 69 | 13.6 | -9.5 | 40.6 |

Tavan serisi uzunluğu: medyan 4 gün, ort 4.2; seri boyunca 1. gün kapanışından medyan getiri %35.

- Seçim yanlılığı büyük: bugün hâlâ işlem gören ve benim listeme giren 69 halka arz; başarısız ve az bilinenler eksik. Buna rağmen tablo net: **seri bitince alan kaybediyor.** Tavan serisi bittikten sonra 20 günde medyan −%5,5 (yalnız %36'sı pozitif), 250 günde medyan −%9,5 (yalnız %41'i pozitif); ortalama pozitif çünkü birkaç dev kazanan (ALFAS, SMRTG, KONTR, ASTOR) var.
- 2020–24'te bireyin halka arzdan gerçek kazancı **tahsisten** (eşit dağıtım) ve serinin kendisinden geldi (1. gün kapanışından seri sonuna medyan +%35; arz fiyatından 1. gün +%10 ilave). Bu, kapasitesi çok sınırlı (hesap başına küçük lot) bir getiri kaynağı. Listemde 05/2024 sonrası arz yok; 2025–26 kohortu test edilmedi.
- Short imkanı yok (VİOP'ta yok, açığa satış yeni arzlarda pratikte yok). Uygulanabilir kural: **tahsisle gir, seri bozulduğu ilk gün çık; seri sonrası alma.** Kilit (lock-up) bitişlerini test edemedim (tarih verisi yok).

### 5.7 Endeks giriş/çıkışları (BIST30/BIST100)
- Aslan (2019), Boğaziçi YL tezi, 2009–2017, BIST100'de 296, BIST30'da 96 değişiklik: girişlerde pozitif ama anlamsız; **çıkışlarda anlamlı negatif**. BIST30'dan çıkanlarda duyuru öncesi 10 gün KAAR **−%4,07 (t=−2,73)**, yürürlükten sonraki gün +%1,1 (t=2,04) geri dönüş; BIST30'a girenlerde yürürlükten sonraki 10 günde **−%2,22 (t=−2,25)** ([Boğaziçi](https://digitalarchive.library.bogazici.edu.tr/items/56f8a94f-66bd-4cd6-a1e8-ba13f5278565)).
- Aydıner & Altay (2020), *Ankara Üniv. SBF Dergisi* 75(4): BIST30/50/100/Temettü değişikliklerinde çıkış duyurusu ve çıkış negatif, giriş pozitif; fiyat baskısı hipotezi ([DergiPark](https://dergipark.org.tr/en/pub/ausbf/article/571826)).
- Hüküm: büyüklük %2–4, olay sayısı yılda birkaç düzine; dönem değişiklikleri önceden tahmin edilebildiği için (piyasa değeri/dolaşım sıralaması) "beklenen çıkışı önceden short (VİOP-47 içindeyse) / beklenen girişi yürürlükten sonra sat" kuralı mantıklı ama 2017 sonrası test yok. MSCI/FTSE dengelemeleri için BIST'e özgü kanıt bulunamadı (arama bütçesi).

### 5.8 Bilanço sonrası sürüklenme (PEAD)
Ahlatçıoğlu & Okay (2021), *Borsa Istanbul Review* 21: 2007–2018, 6.471 firma-çeyrek; yüksek−düşük sürpriz farkı **+2,9%** (zaman serisi SUE) / +2,2% (duyuru getirisi) [2,61] gün; analist örnekleminde +2,9%; çok faktörlü modeller açıklamıyor; küçük firmada daha güçlü ([Boğaziçi tezi](https://digitalarchive.library.bogazici.edu.tr/handle/123456789/16829), [EconBiz](https://www.econbiz.de/Record/post-earnings-announcement-drift-evidence-from-turkey-ahlatc%C4%B1o%C4%9Flu-aykut/10012816435)). Long-short ~%2,9/60 gün → yılda 4 çeyrekle brüt ~%12 (short bacak çoğu hissede yok). Long-only versiyonda yarısı kalır. Swing ufkuna uyumlu ama tek başına küçük; momentum ile birleştirilebilir.

### 5.9 Kredi notu değişiklikleri, PPK günleri, SPK/Borsa tedbirleri (VBTS, brüt takas, kredili işlem yasağı)
Bu başlıklarda arama bütçesi bittiği için literatür taranamadı; kendi testim de yok (olay tarihleri gerekiyor). Borsa İstanbul'un volatilite dönemlerinde tekil hisselere açığa/kredili işlem yasağı getirdiği biliniyor ([CNBC-e örneği](https://www.cnbce.com/borsa/borsa-istanbuldan-uc-hisseye-kredili-islem-yasagi-g33738)). Hüküm: test edilmedi; mekanizma olarak tedbir sonrası likidite düşer, kredili alıcı çekilir → kısa vadeli negatif sürüklenme beklenir, ama kanıt yok.

---

## 6. Akımlar

- **Yabancı akımı:** Ülkü & İkizlerli (2012), *Emerging Markets Review*: yabancılar İMKB'de aylık frekansta **negatif geri besleme** (yerel getiri düşünce alıyor), yalnız yükselen piyasada ve makro istikrarsızlıkta; **net yabancı akımı piyasa getirisini öngörüyor ama tekil hisse getirisini öngörmüyor**; fiyat etkileri kalıcı ([EconBiz](https://www.econbiz.de/Record/the-interaction-between-foreigners-trading-and-emerging-stock-returns-evidence-from-turkey/10009676059)). Ülkü & Weber (2011): günlük frekansta pozitif, aylıkta negatif geri besleme. Hüküm: endeks düzeyinde zamanlama girdisi olabilir; hisse seçimi için değil. Kendi testim yok (MKK/Borsa yabancı payı serisi indirilmedi).
- **AKD / takas izleme:** Tiniç & Salih (2019), *Applied Economics* 52(13), 03.2005–04.2017 tüm hisseler: bilgili işlem olasılığı (PIN) ile gelecek getiri arasında **anlamsız** ilişki ([TEDÜ Avesis](https://avesis.tedu.edu.tr/yayin/addb0698-c56a-492c-b751-360645ffdf84/informed-trading-order-flow-shocks-and-the-cross-section-of-expected-returns-in-borsa-istanbul)). Aracı kurum ağ merkeziliği ile beklenen getiri (Tiniç, Şensoy, Demir, Nguyen 2026, *Annals of OR*): 03.2005–11.2015, iki tarafı kurum kimlikli işlem verisi; merkezi yatırımcılar bilgi olaylarında erken işlem yapıyor ([Springer](https://link.springer.com/article/10.1007/s10479-026-07082-4); ayrıntı doğrulanmadı). **Kamuya açık gün sonu AKD/takas verisini "büyük kurum topluyor" diye izlemenin karlı olduğunu gösteren hakemli kanıt bulamadım.** Bu iddia anekdot düzeyinde; survivorship ve sonradan anlatı ("şu kurum topladı, yükseldi") yanlılığına çok açık.
- **Kredili işlem:** TSPB verisine göre kredili işlem hacmi 2018 1,8 → 2020 6,8 → 2021 11,4 → 2022 sonu 28 mlr TL ([Ekonomi Gazetesi](https://www.ekonomigazetesi.com/finans/kredili-islem-hacminde-2022de-rekor-kirildi-4637)); kredili işlem faizi %80–85'e, dönem dönem %100'e yaklaştı. Öngörü gücünü test eden çalışma bulunamadı. Mekanizma olarak zorunlu kapanışlar düşüşleri derinleştiriyor (3.3'teki kısa vadeli devamın bir kaynağı).
- **TEFAS hisse fonu akımları:** test edilmedi. Not: 15.09.2026 Pusula Portföy temerrüdü ve ~131 fonun tasfiyesi sonrası 5–9 Ekim 2026 haftasında PPF şemsiye ortalaması −%3,02 oldu; tasfiye sürecindeki üç PPF (Pardus AC4 −%99,95, Bulls BPZ −%99,91, A1 Capital PAB −%99,47) ortalamayı aşağı çekti ([Borsagündem 5–9 Ekim](https://www.borsagundem.com.tr/gectigimiz-hafta-en-cok-kazandiran-fonlar-3)); 12–16 Ekim haftasında PPF ortalaması +%0,83 ([Borsagündem 12–16 Ekim](https://www.borsagundem.com.tr/yatirim-fonlarinda-haftalik-hacimler-en-cok-kazandiranlar)). Yani "risksiz" engelin kendisi de 2026'da tam risksiz değil.

---

## 7. Mevsimsellik (kendi testim, XU100 log getiri, 2005–2026)

| dönem | etki | gün | içeride ort bps | dışarıda ort bps | fark t | pozitif gün % |
|---|---|---|---|---|---|---|
| 2005-26 | ToM(son+ilk3) | 1052 | 16.1 | 4.7 | 1.99 | 55.5 |
| 2005-26 | Bayram/tatil oncesi gun | 141 | -9.5 | 7.4 | -1.38 | 50.4 |
| 2005-26 | Tatil sonrasi gun | 141 | 34.1 | 6.2 | 1.43 | 58.9 |
| 2005-26 | Ramazan ayi | 453 | 5.1 | 7.1 | -0.23 | 52.1 |
| 2005-26 | Ocak | 460 | 14.1 | 6.3 | 0.95 | 59.1 |
| 2005-26 | Aralik | 457 | 12.7 | 6.4 | 0.80 | 58.0 |
| 2005-26 | Pazartesi | 1099 | 11.9 | 5.7 | 1.01 | 55.3 |
| 2005-26 | Cuma | 1093 | 6.3 | 7.1 | -0.14 | 54.3 |
| 2005-15 | ToM(son+ilk3) | 528 | 16.7 | 0.7 | 1.85 | 55.7 |
| 2005-15 | Bayram/tatil oncesi gun | 66 | 19.9 | 3.4 | 1.07 | 54.5 |
| 2005-15 | Tatil sonrasi gun | 65 | 39.5 | 2.9 | 1.08 | 63.1 |
| 2005-15 | Ramazan ayi | 225 | 7.3 | 3.4 | 0.29 | 53.8 |
| 2005-15 | Ocak | 224 | -0.3 | 4.1 | -0.36 | 54.9 |
| 2005-15 | Aralik | 237 | 6.0 | 3.5 | 0.22 | 54.4 |
| 2005-15 | Pazartesi | 555 | 2.8 | 4.0 | -0.13 | 54.6 |
| 2005-15 | Cuma | 551 | 3.5 | 3.8 | -0.04 | 52.1 |
| 2016-26 | ToM(son+ilk3) | 524 | 15.6 | 8.9 | 0.90 | 55.3 |
| 2016-26 | Bayram/tatil oncesi gun | 75 | -35.4 | 11.5 | -2.58 | 46.7 |
| 2016-26 | Tatil sonrasi gun | 76 | 29.4 | 9.6 | 0.90 | 55.3 |
| 2016-26 | Ramazan ayi | 228 | 3.0 | 10.8 | -0.68 | 50.4 |
| 2016-26 | Ocak | 236 | 27.7 | 8.5 | 1.75 | 63.1 |
| 2016-26 | Aralik | 220 | 19.9 | 9.3 | 0.94 | 61.8 |
| 2016-26 | Pazartesi | 544 | 21.2 | 7.4 | 1.61 | 56.1 |
| 2016-26 | Cuma | 542 | 9.3 | 10.4 | -0.16 | 56.5 |

Ay dönümü günlerinde endeks, diğer günler nakit (vadeli ile, yön değişimi %0,05):

- 2010-26 ToM-L/nakit CAGR 19.5% MaxDD -15.5% Sharpe 0.31 | BH CAGR 20.4% | nakit 16.3% | piyasada 19%
- 2016-26 ToM-L/nakit CAGR 24.5% MaxDD -12.6% Sharpe 0.27 | BH CAGR 29.2% | nakit 21.6% | piyasada 19%
- 2023-26 ToM-L/nakit CAGR 32.9% MaxDD -11.7% Sharpe -0.16 | BH CAGR 20.8% | nakit 36.7% | piyasada 20%

Literatür: Białkowski, Etebari & Wisniewski (2012), *JBF*: 14 Müslüman ülke 1989–2007, Ramazan'da getiri yüksek ve oynaklık düşük ([UNH](https://findscholars.unh.edu/display/publication90138)); Özkan & Akbalık (2018): İslami takvim etkileri hesaba katılınca BIST'te anormal getiri elde etmek güçleşmiş ([DergiPark jyasar](https://dergipark.org.tr/tr/pub/jyasar/article/306186)). Benim testimde Ramazan etkisi yok (2016–26: 3 bps vs 11 bps dışarıda).

Hüküm: ay dönümü (son gün + ilk 3 gün) 2005–26'da t≈2,0, 2016 sonrası t≈0,9; tek başına strateji olarak 2023–26'da nakdin altında. Tatil (bayram) öncesi gün 2016 sonrası **negatif** (−35 bps, t=−2,6, n=75; çoklu test riski yüksek). Mevsimsellik strateji düzeyinde getiri kaynağı değil; en fazla giriş-çıkış zamanlaması ayarı.

---

## 8. VİOP'a özgü

### 8.1 USDTRY vadeli short (TL carry) — 2023 ortasından beri en yüksek risk-ayarlı getiri, tarihsel olarak en büyük kuyruk riski

Kendi hesabım: aylık yenilenen kısa USDTRY vadeli; vadeli fiyatı = spot × (1+r_TL)/(1+r_USD) (r_TL = TCMB politika faizi; VİOP'ta gerçekleşen örtük faiz bundan farklı olabilir), r_USD ≈ Fed funds yıllık ortalama. "1x fazla" = TL'nin USD'ye karşı carry getirisi (notional başına). "Toplam TL Lx" = teminat TL nakitte + L kat notional.

| yıl | kısa USDTRY 1x fazla % | toplam TL 1x % | toplam TL 2x % | toplam TL 3x % | TL nakit % |
|---|---|---|---|---|---|
| 2010 | 5.0 | 8.6 | 13.1 | 16.9 | 3.4 |
| 2011 | -15.3 | -10.1 | -25.2 | -38.9 | 6.0 |
| 2012 | 11.2 | 17.6 | 29.5 | 41.5 | 5.8 |
| 2013 | -13.2 | -8.9 | -21.7 | -33.3 | 4.8 |
| 2014 | -1.9 | 6.6 | 3.2 | -1.6 | 8.6 |
| 2015 | -15.2 | -8.7 | -23.2 | -36.0 | 7.6 |
| 2016 | -12.9 | -6.2 | -19.9 | -33.2 | 7.5 |
| 2017 | 2.1 | 14.7 | 15.0 | 13.1 | 12.4 |
| 2018 | -29.3 | -16.5 | -55.5 | -95.2 | 17.5 |
| 2019 | 3.5 | 24.7 | 27.3 | 28.3 | 20.5 |
| 2020 | -14.3 | -5.5 | -21.0 | -35.7 | 10.2 |
| 2021 | -44.3 | -33.7 | -74.0 | -102.8 | 17.7 |
| 2022 | -22.4 | -12.1 | -32.9 | -50.0 | 12.9 |
| 2023 | -33.5 | -21.3 | -53.3 | -78.8 | 17.9 |
| 2024 | 18.3 | 75.5 | 105.6 | 139.8 | 49.1 |
| 2025 | 13.5 | 62.3 | 83.2 | 106.5 | 43.5 |
| 2026 | 8.6 | 41.5 | 53.3 | 65.9 | 30.6 |

| dönem | ay | aylık ort % | aylık std % | Sharpe (yıllık) | en kötü ay % | en kötü ay | MaxDD % | pozitif ay % |
|---|---|---|---|---|---|---|---|---|
| 2010-26 | 197 | -0.75 | 5.13 | -0.51 | -35.2 | 2021-11-30 | -89.9 | 52.3 |
| 2019-26 | 95 | -0.86 | 5.37 | -0.56 | -35.2 | 2021-11-30 | -76.3 | 56.8 |
| 2023-07→26 | 41 | 0.85 | 1.31 | 2.24 | -3.4 | 2023-07-31 | -3.7 | 82.9 |

- **Rejim koşullu bir getiri kaynağı.** 07/2023–11/2026 (ortodoks para politikası): aylık ort +%0,85, std %1,31, yıllık Sharpe 2,24, pozitif ay %83, en kötü ay −%3,4, MaxDD −%3,7. 2x notional ile TL toplam: 2024 +%106, 2025 +%83, 2026 YTD +%53 (nakit +%49/+%44/+%31).
- **Tüm örneklemde felaket:** 2010–26 Sharpe −0,51, MaxDD −%90; en kötü aylar Kas 2021 −%35, Ağu 2018 −%32, Haz 2023 −%25; tek günde USDTRY +%27 (13.08.2018). 2x kaldıraçta 2018 −%56, 2021 −%74, 2023 −%53; 3x'te sermaye sıfırlanır.
- Mekanizma: TL carry, "kontrollü değer kaybı" taahhüdü sürdükçe ödeme yapan bir **satılmış kuyruk opsiyonu**. Getiri, politika değiştiği güne kadar düzgün; sonra birkaç yıllık kazanç haftalar içinde gider.
- Şu anki carry: %36 TL − ~%3,9 USD ≈ %32 yıllık fark; USDTRY 2026'da ~%16,6 (10 ayda) arttı → yıllık ~%20 değer kaybı temposu → beklenen fazla ~%8–12/yıl/1x (2026 YTD gerçekleşen +%8,6). Faiz indirimi (Ekim −100 bp, Aralık PPK 10.12.2026) farkı daraltıyor; fon krizi, Brent >115 $, MSCI uyarısı kuyruk riskini artırıyor.
- VİOP: USDTRY vadeli PSR %33,3 (03.11.2026 itibarıyla, [QNB Invest](https://www.qnbinvest.com.tr/duyuru/viop-psr-oran-guncellemesi-03112026)); stopaj %10. Hesaptaki vadeli fiyatı politika faiziyle kurdum; VİOP'ta işlem gören örtük faiz farklıysa (genelde politika faizinin biraz altında) getiri daha düşük.
- Hüküm: Engelin üstüne çıkmanın **en kolay** yolu (1x short USDTRY + teminat PPF ≈ nakit + %8–15), ama kuyruk riski hisse riskinden büyük. Ancak (a) reel faiz pozitif, (b) TCMB rezervleri artıyor, (c) USDTRY örtük vol düşük iken; notional ≤1x, ve OTM USDTRY call ya da XAUTRY ile kuyruk korumasıyla.

Dış kaynaklar: Kuveyt Türk Portföy: 2024'te TL PPF ortalaması ~%53, TL USD'ye karşı ~%19,7 değer kaybı → net USD getiri ~%28; 2025'in ilk 4 ayında fon %13,2, TL −%8,8 → net ~%4,1 ([Kuveyt Türk Portföy](https://www.kuveytturkportfoy.com.tr/en/blog-news/finance/wealth-insights-q3-2025-outlook-views-from-kuveyt-turk-portfoy-on-the-carry-tra/)). Bloomberg: Ocak 2025'e kadar 6 ayda USD fonlamalı TL carry ortalaması %15, en yakın rakibin (ARS) ~2 katı ([BNN Bloomberg](https://bnnbloomberg.ca/business/2025/01/08/best-em-carry-trade-boosted-by-turkeys-inflation-proofed-lira)). Mart 2025 şokunda Barclays: TL long pozisyonlarda 4 aydan fazla getiri 24 saatte silindi ([IFR](https://www.ifre.com/rates/2248088/investors-suffer-heavy-losses-in-popular-turkey-carry-trade)). 28.02.2026'da başlayan İran savaşı sonrası Mart'ın ilk iki haftasında ~12 mlr $ carry çıkışı, Ocak sonunda carry pozisyonları >60 mlr $ (arama özeti; muhtemel kaynak [AGBI 04/2026](https://www.agbi.com/analysis/markets/2026/04/turkey-back-on-carry-trade-radar/), sayfa erişimi engelli, doğrulanmadı); Ekim 2026'da TL ~50/$ rekor düşük, TCMB müdahaleyle kontrollü değer kaybı ([Trading Economics](https://tradingeconomics.com/turkey/currency/news/594227); ikincil kaynak, tarih tutarsızlıkları var).

### 8.2 Endeks vadeli baz / short'un taşıma avantajı
Yüksek faizde XU030 vadelisi spot×(1+r) civarında fiyatlanır. Bu nedenle **vadeli short pozisyonu nakit getirisi + (nakit − endeks) kazanır**: 2024–26'da endeks nakdin gerisinde kaldığı için short vadeli + teminat PPF, "2×nakit − endeks" getirisi verdi. 4. bölümdeki L/S trend sonuçlarının 2023–26'daki üstünlüğü büyük ölçüde bu taşıma etkisi. Önceki çalışmadaki baz sıçraması dönüşü +14–20 bps/işlem ile mikro düzeyde kaldı. Takvim yayılımı (yakın/uzak vade) saf faiz beklentisi pozisyonudur; ayrı test yapılmadı.

### 8.3 XU030 opsiyon volatilite risk primi
BIST30 opsiyonlarında örtük–gerçekleşen vol primini ölçen çalışma bulunamadı (yalnız model karşılaştırmaları: METU tezleri, [Akyapı & Küçükşenel 2014](https://open.metu.edu.tr/handle/11511/23613)). Opsiyon fiyat geçmişi elimde yok, test edilmedi. Uygulama riski: düşük likidite, piyasa yapıcı spreadi, ±%10 limitli gap'ler; Eylül 2026'daki %22'lik düşüş gibi olaylarda çıplak put satıcısı birkaç yıllık primi tek ayda verir. Hüküm: bireysel için **satış tarafı önerilmez**; alım tarafı (kriz hedge'i) pahalı ama portföy düzeyinde carry/trend pozisyonlarını korumak için anlamlı olabilir.

### 8.4 Altın vadelileri
Ayrı test yapılmadı. Önceki çalışmada TRALT ← altın öncülüğü test edilmişti. XAUTRY vadelisi TL faizini içinde taşır (long altın vadeli + teminat PPF = altın TL getirisi); XAUUSD vadelisi %10 stopajlı. Altın, TL carry pozisyonunun doğal kuyruk hedge'i (TL şoklarında XAUTRY yükselir).

---

## 9. Göreli değer

### 9.1 Holding iskontosu / holding–iştirak oranı ortalamaya dönüş (kendi testim)

Kurulum: log(holding) − log(iştirak sepeti, günlük eşit ağırlık); z = (oran − L günlük ortalama)/std; |z| ≥ 2'de karşı yönde gir, H gün tut, örtüşmesiz. Getiri = göreli log getiri (brüt).

| çift | L (z penceresi) | H (gün) | dönem | işlem | ort bps | medyan bps | isabet % | t | en kötü işlem % |
|---|---|---|---|---|---|---|---|---|---|
| KCHOL~sepet(TUPRS,FROTO,TOASO,ARCLK,YKBNK,AYGAZ) | 60 | 20 | 2010-18 | 51 | 212 | 163 | 73 | 3.23 | -8.1 |
| KCHOL~sepet(TUPRS,FROTO,TOASO,ARCLK,YKBNK,AYGAZ) | 60 | 20 | 2019-26 | 39 | 244 | 259 | 64 | 2.82 | -8.5 |
| KCHOL~sepet(TUPRS,FROTO,TOASO,ARCLK,YKBNK,AYGAZ) | 250 | 20 | 2010-18 | 31 | 255 | 173 | 65 | 3.00 | -4.4 |
| KCHOL~sepet(TUPRS,FROTO,TOASO,ARCLK,YKBNK,AYGAZ) | 250 | 20 | 2019-26 | 32 | 185 | 213 | 59 | 1.85 | -13.9 |
| SAHOL~sepet(AKBNK,ENJSA,CIMSA,BRISA) | 60 | 20 | 2010-18 | 50 | 125 | 101 | 64 | 1.49 | -18.8 |
| SAHOL~sepet(AKBNK,ENJSA,CIMSA,BRISA) | 60 | 20 | 2019-26 | 41 | 61 | 38 | 56 | 0.60 | -13.2 |
| SAHOL~sepet(AKBNK,ENJSA,CIMSA,BRISA) | 250 | 20 | 2010-18 | 30 | 169 | 160 | 67 | 1.68 | -16.3 |
| SAHOL~sepet(AKBNK,ENJSA,CIMSA,BRISA) | 250 | 20 | 2019-26 | 32 | 7 | -133 | 41 | 0.05 | -26.7 |
| SAHOL~AKBNK | 60 | 20 | 2010-18 | 50 | 250 | 269 | 76 | 3.75 | -5.8 |
| SAHOL~AKBNK | 60 | 20 | 2019-26 | 41 | 388 | 495 | 66 | 3.65 | -8.3 |
| SAHOL~AKBNK | 250 | 20 | 2010-18 | 30 | 142 | 214 | 73 | 1.60 | -14.6 |
| SAHOL~AKBNK | 250 | 20 | 2019-26 | 32 | 150 | 178 | 53 | 1.19 | -12.0 |
| KCHOL~SAHOL | 60 | 20 | 2010-18 | 49 | 133 | 184 | 71 | 1.44 | -27.0 |
| KCHOL~SAHOL | 60 | 20 | 2019-26 | 45 | 70 | 45 | 51 | 0.78 | -11.0 |
| KCHOL~SAHOL | 250 | 20 | 2010-18 | 33 | 141 | 81 | 64 | 1.34 | -17.7 |
| KCHOL~SAHOL | 250 | 20 | 2019-26 | 29 | 89 | 152 | 52 | 0.66 | -11.0 |
| KRDMA~KRDMD | 60 | 20 | 2010-18 | 51 | 2 | 45 | 57 | 0.02 | -15.6 |
| KRDMA~KRDMD | 60 | 20 | 2019-26 | 40 | -56 | 25 | 50 | -0.29 | -30.0 |
| KRDMA~KRDMD | 250 | 20 | 2010-18 | 31 | 20 | -1 | 48 | 0.21 | -13.7 |
| KRDMA~KRDMD | 250 | 20 | 2019-26 | 30 | 131 | 136 | 60 | 0.48 | -30.0 |
| KRDMB~KRDMD | 60 | 20 | 2010-18 | 53 | 36 | -90 | 43 | 0.19 | -22.6 |
| KRDMB~KRDMD | 60 | 20 | 2019-26 | 42 | -156 | 61 | 60 | -0.81 | -60.8 |
| KRDMB~KRDMD | 250 | 20 | 2010-18 | 28 | -181 | -166 | 32 | -0.89 | -30.5 |
| KRDMB~KRDMD | 250 | 20 | 2019-26 | 31 | -249 | 88 | 61 | -1.18 | -51.6 |
| DOHOL~XU100 | 60 | 20 | 2010-18 | 41 | -84 | -19 | 46 | -0.55 | -34.3 |
| DOHOL~XU100 | 60 | 20 | 2019-26 | 38 | 324 | 295 | 66 | 2.47 | -14.1 |
| DOHOL~XU100 | 250 | 20 | 2010-18 | 23 | 461 | -19 | 48 | 1.33 | -15.3 |
| DOHOL~XU100 | 250 | 20 | 2019-26 | 26 | 238 | -20 | 50 | 1.41 | -13.4 |
| ALARK~XU100 | 60 | 20 | 2010-18 | 46 | 18 | -104 | 43 | 0.16 | -14.5 |
| ALARK~XU100 | 60 | 20 | 2019-26 | 39 | -254 | -406 | 31 | -1.69 | -24.6 |
| ALARK~XU100 | 250 | 20 | 2010-18 | 32 | 125 | 53 | 56 | 0.93 | -12.1 |
| ALARK~XU100 | 250 | 20 | 2019-26 | 27 | -255 | -635 | 37 | -1.19 | -22.4 |
| TRALT~TRMET | 60 | 20 | 2010-18 | 48 | -44 | 48 | 52 | -0.25 | -45.2 |
| TRALT~TRMET | 60 | 20 | 2019-26 | 39 | 83 | 150 | 69 | 0.54 | -28.6 |
| TRALT~TRMET | 250 | 20 | 2010-18 | 25 | -168 | 161 | 56 | -0.55 | -40.4 |
| TRALT~TRMET | 250 | 20 | 2019-26 | 23 | -147 | 41 | 52 | -0.84 | -28.6 |

(H=10 ve H=60 sonuçları `rv.csv`'de; özet yorumda kullanıldı.)

- **KCHOL ↔ iştirak sepeti** (TUPRS, FROTO, TOASO, ARCLK, YKBNK, AYGAZ; AYGAZ dışında hepsinin VİOP vadelisi var): L=60, |z|≥2, H=20: 2010–18 +212 bps/işlem (t=3,2, n=51, isabet %73), 2019–26 +244 bps (t=2,8, n=39, isabet %64). H=10 ve H=60'ta da iki alt dönemde pozitif ve t>2. Yılda ~5 işlem → çift notional'ı üzerinden ~%10–12/yıl brüt; 7 bacaklı VİOP maliyeti işlem başına ~%0,3–0,6.
- **SAHOL ↔ AKBNK:** L=60, H=20: 2010–18 +250 bps (t=3,8, isabet %76), 2019–26 +388 bps (t=3,7, isabet %66). Önceki çalışmadaki 1–3 günlük +30–50 bps bulgusunun swing ufkundaki karşılığı ve daha büyük. SAHOL ↔ geniş Sabancı sepeti 2019–26'da zayıf (t≈0–1,1).
- KCHOL ↔ SAHOL: anlamlı değil (t 0,7–1,6).
- DOHOL ve ALARK'ın XU100'e göre oranı: istikrarlı değil (ALARK 2019–26'da negatif).
- Çoklu test: 9 çift × 2 pencere × 3 ufuk × 2 dönem = 108 hücre; t>2,5 olan hücrelerin neredeyse tamamı KCHOL-sepet ve SAHOL-AKBNK'tan geliyor ve iki bağımsız alt dönemde tekrar ediyor. Holding iskontosunun sınırlı arbitrajla sabitlenmesi ekonomik açıklama sağlıyor.
- Hüküm: güvenilir ama küçük. Strateji düzeyinde katkı: portföyün %20–30'u kadar notional ile yılda +%2–4 portföy getirisi; piyasa yönünden bağımsız olduğu için rejim kapalıyken bile çalışır.

Not: Bu NAV iskontosu değil, holding fiyatının iştirak fiyatlarına göre kısa vadeli sapması. Gerçek NAV iskontosu (KCHOL/SAHOL/DOHOL/ALARK) için aracı kurum NAV serileri gerekiyor; arama bütçesi bittiği için bulunamadı. Gökçen (2026) değer faktörünün BIST'in en güçlü faktörü olduğunu bulduğu için yüksek iskontolu holdingler yavaş (6–24 ay) bir değer pozisyonu; swing ufkuna değil, kümelenme çekirdeğine uygun.

### 9.2 A/B pay sınıfları (KRDMA/KRDMB/KRDMD) ve grup hisseleri
KRDMA/KRDMD ve KRDMB/KRDMD oranlarında ortalamaya dönüş **yok** (tabloda t mutlak değeri < 1,3; en kötü işlemler −%30…−%66). KRDMB trend yapıyor; A ve B sınıfları sığ, oran kalıcı kayıyor. TRALT/TRMET oranında 20–60 gün ufkunda istikrarlı dönüş yok (önceki çalışmadaki göreli momentum bulgusuyla tutarlı: Koza grubunda oran trend yapıyor, dönmüyor).

---

## 10. Dürüst hüküm: hangisi %36–40 TL engelinin belirgin üstüne çıkabilir?

**Kısa cevap:** Tek başına %36–40 TL engelinin belirgin üstünü sürekli veren, düşük riskli bir BIST/VİOP kenarı bulamadım. Engel, birkaç bağımsız kaynağın birleşimiyle **ortalamada** aşılabilir; her yıl değil.

**1. Kanıta göre "kazananlar" nasıl kazandı**
- **Rejimi doğru okudular.** 2021–23 negatif reel faizde hisse long (XU100 2022 +%197); 2024–26 pozitif reel faizde nakit/carry/short vadeli. Benim testlerimde 2024–25'te nakdi belirgin geçenler: short USDTRY (1x fazla +%18,3 / +%13,5) ve XU030 vadeli L/S trend (TSMOM252 2024 +%98 vs nakit %49, 2025 +%70 vs %44; ama 2026 YTD +%7 vs %31). Piyasa-nötr çiftler (2019–26 alt dönemi) ve olay katmanları (2023–26 alt örneklemi) pozitif ama yıl yıl ayrıca test edilmedi. **Uzun-hisse momentum/52-hafta dahil hiçbir uzun-hisse yapısı 2024, 2025 ya da 2026'da nakdi geçmedi.**
- **Liderlere bindiler, düşeni almadılar.** 52-hafta zirvesine yakın hisseler 2016 sonrası EW'yi ayda ~%0,6–1,3 geçti; derin düşenler ve haftalık kaybedenler geride kaldı.
- **Olay akışını topladılar.** Temettü/bedelsiz öncesi koşu, halka arz tahsisi (seri bitince satış).
- **Bilgiye yakın olanı izlediler.** İçeriden ve büyük ortak işlemleri 1 yılda ~%6,6 anormal; dışarıdan taklit mümkün (Avcı 2024).
- **Bireyin karşı tarafında oldular.** Haftalık kaybedenlerin devamı ve seri sonrası halka arz düşüşü, dip alan / geç binen bireyin sistematik olarak kaybeden tarafta olduğunu gösteriyor (manipülasyon kanıtı değil, ama tutarlı).

**2. Strateji düzeyinde gerçekçi beklenti (backtest → iskonto)**

| Bileşen | Backtest | İskonto sonrası beklenti (nakit üstü, yıllık) | Kötü senaryo |
|---|---|---|---|
| Rejim + 52-hafta sepeti (12–20 hisse, spot) | 2010–26 %33–36 vs nakit %16; 2016–26 %49–52 vs %21 | +8…+15 puan (rejim açık yıllarda +20…+60, kapalıda 0…−10) | MaxDD −%25…−%35; 2018 tipi yıl nakit −25 puan |
| Piyasa-nötr çiftler (KCHOL↔sepet, SAHOL↔AKBNK), %20–30 notional | +%2,1…+%3,9/işlem, ~5 işlem/yıl/çift | portföye +2…+4 puan | tek işlem −%8…−%20 |
| Temettü + bedelsiz öncesi overlay | +%1,2…+%2,8/olay | portföye +3…+6 puan (sezonluk) | olay başı −%5…−%10 kuyruk |
| TL carry 0,5–1x notional (yalnız rejim uygunsa) | 07/2023–26 Sharpe 2,2 | +4…+12 puan | tek ayda −%12…−%35 (1x) |

Toplam: iyi yılda nakit +20…+40 puan, normal yılda +5…+15, kötü yılda (TL şoku + hisse çöküşü) nakdin 20–40 puan altında. Yani hedef "%36–40 + 10–15 puan" gerçekçi; "her yıl %100" gerçekçi değil.

**3. Bugünkü durum (06.11.2026), mekanik okuma**
- Rejim filtresi **kapalı**: XU100 11.333, 12 ay +%3,3 vs TL nakit +%37,3; endeks SMA200'ün (13.572) ~%16 altında. Kural "hisse long değil, nakit; L/S sürümünde XU030 short" diyor. Yeniden açılması için XU100'ün 12 ay önceki seviyesinin ~%37 üstüne çıkması (bugünkü baza göre ~15.000; baz her ay değişir) ya da faizlerin belirgin düşmesi gerekir.
- Rejimden bağımsız olarak çalışabilecekler: piyasa-nötr çiftler, temettü/bedelsiz öncesi overlay (sezon dışı), içeriden alım filtresi.
- Carry: fark ~%32 (TL %36 − USD ~%3,9), yıllık ~%20 değer kaybı temposu → beklenen fazla ~%8–12/1x; ama fon krizi, Brent >115 $, MSCI uyarısı, indirim döngüsü kuyruk riskini artırıyor. Bu ortamda ≤0,5x ve OTM USDTRY call/XAUTRY korumasıyla.

**4. Mevcut mikro kenarların yeri**
Önceki çalışmadaki 3–4 kenar (+14…+50 bps/işlem) bu tablonun içinde "overlay" sınıfında. Onların sık başarısız olmasının bir nedeni rejim: pozitif reel faiz ve fon krizi döneminde hisse tarafındaki kısa vadeli düzenlilikler (özellikle dönüş tipi olanlar) zayıflıyor; 2016 sonrası BIST'in baskın kısa vadeli özelliği dönüş değil devam. SAHOL/AKBNK kenarı 20 günlük ufukta daha büyük ve daha sağlam (+%2,5…+%3,9/işlem).

---

## 11. Doğrulayıcı için açık noktalar ve sınırlamalar

1. **Survivorship:** İş Yatırım uç noktası kottan çıkmış kodları vermiyor (KOZAL/KOZAA/IPEKE boş döndü; yeni kodlar TRALT/TRENJ/TRMET tam geçmişle geliyor). Evren 2026'da işlem gören, benim seçtiğim isimler. Momentum ve kısa vadeli devam bulgularında bu yanlılık sonucu zayıflatır yönde; "VİOP-47 içinde momentum" ve EW evren CAGR'ında güçlendirir yönde. Ayrıca evren genişledikçe (106 → 181 → 248 hisse) 12-1 momentum ve rezidüel momentum zayıfladı; 52-hafta ve 1 ay/1 hafta devam bulguları sağlam kaldı. **Bu kırılganlık doğrulanmalı.**
2. Endeks XU100 fiyat endeksi (temettü yok); vadeli modeli temettü ve baz sapmasını ihmal ediyor. XU030 vadeli gerçek serisiyle tekrar edilmeli.
3. Nakit = TCMB politika faizi yıllık efektif; PPF gerçekleşen getirisinden 2024'te ~4 puan düşük, stopaj hesaba katılmadı. Hisse/endeks VİOP kazancı %0 stopaj, PPF %17,5 olduğundan vergi sonrası karşılaştırmada stratejiler lehine ~5–7 puan ek fark var.
4. Maliyet: hisse tek yön %0,15, endeks vadeli yön değişimi %0,10, rejim geçişi %0,3. Küçük/sığ hisselerde gerçek kayma daha yüksek; limit (tavan/taban) günlerinde işlem yapılamaması modellenmedi (özellikle 1 hafta devam bulgusunda önemli).
5. Bedelsiz testi hak kullanım tarihine göre; yönetim kurulu kararı ve SPK onay tarihleri (asıl popüler işlem) test edilmedi. k≥1,15 eşiği bedelli artırımları da içerebilir.
6. Olay tarihleri gerektiren başlıklar (endeks dönem değişikliği, MSCI/FTSE, kredi notu, PPK, VBTS/brüt takas, lock-up, içeriden alım) kendi testimde yok; yalnız literatür.
7. Web arama bütçesi bitti: Gökçen (2026) momentum rakamı, Bildik-Gülay tablosu, Ahlatçıoğlu-Okay örneklem ayrıntıları, Avcı (2024) taklit portföyü getirisi tam metinden doğrulanamadı.
8. Kod ve ara çıktılar oturum karalama dizininde (`scratchpad/bsk/kod`, `scratchpad/bsk/sonuc`); proje klasörüne yazılmadı (görev yalnız bu dosyayı yazmayı istedi).

---

## 12. Kaynaklar (kullanılanlar)

Veri ve resmi:
- İş Yatırım günlük pay verisi (kendi testlerin girdisi): `https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/HisseTekil?hisse=THYAO&startdate=01-01-2005&enddate=05-11-2026` (düzeltilmiş/ham kapanış, hacim, sermaye, XU100, USDTRY alanları)
- TCMB 1 hafta repo tarih tablosu: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Temel+Faaliyetler/Para+Politikasi/Merkez+Bankasi+Faiz+Oranlari/1+Hafta+Repo
- PPK 22.10.2026: https://www.qnbinvest.com.tr/investodak/qnbarastirma/tcmb-ekim-ayi-faiz-kararini-acikladi-politika-faizi-36ya-indirildi
- Stopaj: https://www.pwc.com.tr/tr/sektorler/bankacilik-sermaye-piyasalari/bultenler/2026/kurumsal-yatirimcilarin-para-piyasasi-fonu-kazanclarinda-tevkifat-orani-yuzde-10a-yukseltildi.html ; https://www.isportfoy.com.tr/medya-ve-blog/para-piyasasi-fonlarinda-kurumlara-uygulanan-stopaj-duzenlemesi-hakkinda-eylul-2026 ; https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/vergilendirme
- VİOP PSR 03.11.2026: https://www.qnbinvest.com.tr/duyuru/viop-psr-oran-guncellemesi-03112026

Hakemli / çalışma kağıdı / tez:
- Bildik & Gülay 2007: https://ideas.repec.org/a/bla/irvfin/v7y2007i1-2p61-87.html
- Ünal 2021: https://dergipark.org.tr/en/download/article-file/1419417 (özet: https://dergipark.org.tr/tr/pub/ijmeb/article/832584)
- Alper & Aydoğan 2017: https://dergipark.org.tr/tr/download/article-file/428034
- Gökçen 2026: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4588551 ; https://www.sciencedirect.com/science/article/pii/S2214845026001043 ; özet: https://paperswithbacktest.com/strategies/factor-investing-in-the-turkish-equity-market
- Chui, Titman & Wei 2010: https://ideas.repec.org/a/bla/jfinan/v65y2010i1p361-392.html
- Demirer, Yüksel & Yüksel 2017: https://econpapers.repec.org/RePEc:eee:riibaf:v:42:y:2017:i:c:p:1445-1454
- 52-hafta/brüt karlılık (MAKÜ): https://dx.doi.org/10.30798/makuiibf.790900
- Ülkü 2009 (teknik kurallar): https://ideas.repec.org/a/bor/iserev/v11y2009i41p25-44.html
- Teknik kurallar SPP testi 2023: https://link.springer.com/10.1007/s11408-023-00433-2
- TSMOM özeti: https://quantpedia.com/time-series-momentum-works-everywhere/ ; sektör momentumu: https://quantpedia.com/strategies/sector-momentum-rotational-system
- Küçüksille & Mizrahi 2015 (bedelsiz): https://dergipark.org.tr/en/download/article-file/452850
- Işıker & Taş 2021 (bedelsiz): https://ideas.repec.org/a/eme/jcmspp/jcms-03-2021-0008.html
- SPK onaylı bedelsiz (2016–17): https://dergipark.org.tr/en/pub/sobbiad/issue/36421/412528 (eşleşme doğrulanmadı)
- Ayan Civelek & Konak (geri alım): https://dergipark.org.tr/en/download/article-file/2325701 ; Torun & Karan: https://gcris.agu.edu.tr/items/20b376f3-fd7e-4eb6-9977-ddf61abc2b3b
- Avcı 2024 (içeriden işlem): https://research.sabanciuniv.edu/id/eprint/50115 ; WP: https://www.scribd.com/document/532198970/SSRN-id3896937 ; METU tezi: https://open.metu.edu.tr/handle/11511/19162
- Halka arz: https://dergipark.org.tr/en/download/article-file/1042951 ; https://earsiv.beykent.edu.tr/items/1c99c9a6-3232-4866-8de0-10434a562ce6/full ; https://dergipark.org.tr/en/download/article-file/1271957
- Endeks etkisi: https://digitalarchive.library.bogazici.edu.tr/items/56f8a94f-66bd-4cd6-a1e8-ba13f5278565 ; https://dergipark.org.tr/en/pub/ausbf/article/571826
- PEAD: https://digitalarchive.library.bogazici.edu.tr/handle/123456789/16829 ; https://www.econbiz.de/Record/post-earnings-announcement-drift-evidence-from-turkey-ahlatc%C4%B1o%C4%9Flu-aykut/10012816435
- Yabancı akımı: https://www.econbiz.de/Record/the-interaction-between-foreigners-trading-and-emerging-stock-returns-evidence-from-turkey/10009676059
- PIN: https://avesis.tedu.edu.tr/yayin/addb0698-c56a-492c-b751-360645ffdf84/informed-trading-order-flow-shocks-and-the-cross-section-of-expected-returns-in-borsa-istanbul ; aracı kurum ağı: https://link.springer.com/article/10.1007/s10479-026-07082-4
- Ramazan: https://findscholars.unh.edu/display/publication90138 ; https://dergipark.org.tr/tr/pub/jyasar/article/306186
- BIST30 opsiyon modelleri (METU): https://open.metu.edu.tr/handle/11511/23613

Pratisyen / haber (ikincil, düşük kanıt):
- Kuveyt Türk Portföy carry: https://www.kuveytturkportfoy.com.tr/en/blog-news/finance/wealth-insights-q3-2025-outlook-views-from-kuveyt-turk-portfoy-on-the-carry-tra/
- BNN Bloomberg 08.01.2025: https://bnnbloomberg.ca/business/2025/01/08/best-em-carry-trade-boosted-by-turkeys-inflation-proofed-lira
- IFR: https://www.ifre.com/rates/2248088/investors-suffer-heavy-losses-in-popular-turkey-carry-trade
- Trading Economics TL: https://tradingeconomics.com/turkey/currency/news/594227
- Kredili işlem: https://www.ekonomigazetesi.com/finans/kredili-islem-hacminde-2022de-rekor-kirildi-4637 ; https://www.bloomberght.com/borsayi-kredisi-yuksek-yatirimci-dagitti-2362224 ; https://www.cnbce.com/borsa/borsa-istanbuldan-uc-hisseye-kredili-islem-yasagi-g33738
- Fon getirileri Ekim 2026: https://www.borsagundem.com.tr/gectigimiz-hafta-en-cok-kazandiran-fonlar-3 ; https://www.borsagundem.com.tr/yatirim-fonlarinda-haftalik-hacimler-en-cok-kazandiranlar
