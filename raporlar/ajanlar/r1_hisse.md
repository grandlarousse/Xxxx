# HİSSE — 1. Tur (28.10.2026) — Pay vadeli / sektör / pair

Etiketler: **[D]** doğrulanmış (kaynaklı), **[H]** benim hesabım, **[T]** tahmin/varsayım.
Fiyat serisi: Yahoo Finance günlük kapanış, 1 yıl (`query1.finance.yahoo.com/v8/finance/chart/<KOD>.IS`). XU100 28.10 kapanışı 11.165,44, Endeks24 ile birebir aynı. [D]

## 0. Baseline düzeltmeleri
- 27.10 BIST100 kapanışı **11.151,03** (cnbce ve Yahoo). BloombergHT'nin verdiği 11.117,13 aslında 23.10 kapanışına denk geliyor, muhtemelen bayat veri. [D] https://www.cnbce.com/borsa/borsa-istanbul-canli-piyasalarda-yeni-yukselis-beklentisi-27-ekim-2026-h40399
- 14.09→28.10 değişimi: **XU030 −%17,9** (17.011,8→13.960,9), **XU100 −%21,6** [H/Yahoo]. Baseline'daki "−%19,5 / −%23,2" rakamları kapanış serisiyle tutmuyor; muhtemelen gün içi dip ya da farklı uç tarih kullanılmış.
- "XBANK 22–23 Ekim'de −%8,69" rakamı gün içi değer. Kapanıştan kapanışa 21→23.10 düşüş **−%5,1** (15.926,7→15.107,2). [H]

## 1. VİOP pay vadeli: kontrat, teminat, likidite
- 1 kontrat = **100 pay**. Uzlaşma **fiziki teslimat**: vadeye kalan short bacak pay teslim etmek zorunda kalır. Vade, ayın son iş günü (yarım güne denk gelirse bir önceki iş günü). Buna göre **Aralık vadesi 31.12.2026** [D] (Borsa İstanbul kılavuzu https://www.borsaistanbul.com/data/kilavuzlar/VIOP_vadeli_islem_sozlesmeleri.pdf). 50 civarı pay kontratı listede; AKBNK, GARAN, YKBNK, ISCTR, VAKBN, HALKB, THYAO, ASELS, KCHOL, SAHOL, EREGL, TUPRS, BIMAS, SISE, PGSUS, ASTOR, SASA, GUBRF dahil [D] https://www.gcmyatirim.com.tr/viop/viop-sozlesmeleri/hisse-sozlesme
- Yüzdesel teminat (01.10.2026'dan itibaren geçerli): XU030 %11,4 · AKBNK %15,7 · GARAN %14,4 · YKBNK %15,8 · ISCTR %13,5 · THYAO %13,4 · ASELS %15,8 · KCHOL %12,8 · SAHOL %13,2 · EREGL %14 · TUPRS %14,3 · BIMAS %12,7 [D] https://www.denizyatirim.com/Teminatlar. **Takasbank 02.11'de risk parametrelerini güncelliyor**; artış ihtimali var [D] https://www.foreks.com/haber/detay/6ae0c15f58b1b941c20921a0/FRKS/tr/takasbank-risk-parametrelerini-guncelledi-27-10-26/. Bazı kurumlar bazı kontratlarda Takasbank teminatının 2 katını uyguluyor [D].
- Likidite sıralaması **AKBNK ≫ YKBNK ≈ GARAN ≈ ISCTR > SAHOL** [T]. Tek veri noktası Fintables'ta AKBNK 952 bin, ASELS 168 bin kontrat (tarihsiz). Resmi aylık istatistikten doğrulamadım.
- Baz [T]: Aralık vadeli ≈ spot×(1+r·t). r≈%36,5 ve 62 günle baz ≈ **+%6,2**. Pair'de net long nominal üzerinden ≈%6/2 ay taşıma maliyeti P&L'de görünür (nakit faiz kazanıyorsa ekonomik olarak nötr). Kâr payı: bu bankalar ve SAHOL Mart–Nisan'da öder, Aralık vadesine kadar düzeltme beklemiyorum [T].

## 2. Sektör ayrışması (14.09 → 28.10, kapanış) [H/Yahoo]
| Hisse | Getiri | β250 (XU030) | β60 | Korelasyon250 |
|---|---|---|---|---|
| ASELS | −3,8% | 1,24 | 1,40 | 0,63 |
| GARAN | −5,4% | 1,06 | 0,98 | 0,74 |
| YKBNK | −5,9% | 1,24 | 1,03 | 0,73 |
| XBANK | −10,7% | 1,15 | 1,03 | 0,79 |
| KCHOL | −11,4% | 0,94 | 0,90 | 0,76 |
| SAHOL | −12,3% | 1,07 | 0,87 | 0,78 |
| ISCTR | −12,4% | 1,12 | 1,19 | 0,75 |
| AKBNK | −13,2% | 1,23 | 1,04 | 0,74 |
| THYAO / TUPRS | −14,6% / −14,6% | 0,87 / 0,47 | 0,78 / 0,83 | 0,71 / 0,31 |
| BIMAS | −15,1% | 0,79 | 0,76 | 0,60 |
| SISE / PGSUS / EREGL | −22,1% / −22,4% / −19,7% | ~1,0 | | |
| **XU030** | **−17,9%** | | | |

En çok düşenler (14.09→23.10): ASTOR −%49, SASA −%46, GUBRF −%38, TRALT −%31, TRMET −%25 [H, Endeks24 tablosundan] https://www.endeks24.com/bist-30-astor-zirveden-yuzde-59-dustu
**Yorum:** XU030'un düşüşünü büyük ölçüde fona ya da perakende yatırımcıya yoğun maruz isimler sürükledi (DSTKF 01.10'da endeksten çıktı [D] https://www.endeks24.com/bist-30-endeksinde-dstkfnin-yerini-trmet-aldi). Büyük bankalar ve ASELS endeksten iyi gitti. Faiz indiriminden sonra tablo tersine döndü: 21→28.10 arasında XBANK −%5,4, XU030 −%3,5. Yılbaşından beri XBANK −%8,9, XU030 +%14,2 [H].
**Fon bağlantısı:** Tasfiyedeki fonlarda yoğunlaşma küçük ve orta ölçekli paylarda: TEHOL'de fiili dolaşımdaki payın %78'i, ANELE'de %68'i, PEKGY'de %55'i fonlarda. BIST30 payları (THYAO, ASELS, KCHOL, TUPRS, GARAN, AKBNK, SAHOL…) fonların portföyünde var ama dolaşımdaki paya oranları "çok daha düşük"; lot sayısı yayımlanmadı [D] https://www.borsaningundemi.com/haber/iste-tasfiye-karari-verilen-fonlarin-elindeki-hisseler-1908618. En çok fonda tutulan BIST30 payı SAHOL (15 fon), ardından AKBNK (13) geliyor; bu bir fon sayımı, tutar değil [D] https://www.sonhaberler.com/fon-krizi-hangi-hisseleri-vurdu-tam-liste-131-fon-bistte-one-cikan-hisseler-ve-sorusturmadaki-isimler-haber-913111

## 3. Bankalar ve 3Ç sezonu
- **AKBNK (27.10, açıklandı):** Net kâr 11,6 mlr TL; konsensüs 11,6, çeyreklik −%24. Swap düzeltmeli NIM %2,03 (çeyreklik −100bp). Risk maliyeti 142bp. Çeyreklik ROE %14,2. Yönetim yıl sonu NIM, ücret ve ROE hedeflerine ulaşmanın "zorlaştığını" söyledi; Ekim başı marj ~%3,2, 2027'ye ~%3,5 bekliyor. F/DD ≈1,0 [D] https://arastirma.isyatirim.com.tr/2026/10/28/akbnk-is-akbank-3c-2026-kar-analizi/. Hisse 28.10'da −%2,0 (63,00).
- **Medyan konsensüsler:** GARAN 32,3 mlr (yıllık +%6, çeyreklik büyüyen tek banka, **bu akşam açıklıyor**). YKBNK 10,49 mlr (yıllık −%30), 3 Kasım. ISCTR 9,57 mlr (yıllık −%33), 5 Kasım. VAKBN 14,3 mlr, 5 Kasım [D] https://www.yatirimx.com.tr/piyasa/bankalarin-3-ceyrek-kr-beklentileri-devler-arasinda-buyuk-ayrisma/26866
- **Aktif kalitesi:** Sektörde sorunlu kredi hacmi 3Ç'de çeyreklik %50'nin üzerinde arttı (+145 mlr TL, toplam 917 mlr TL; artış kamu bankalarında daha belirgin). Risk maliyeti ~300bp'ye yaklaşıyor. 9 aylık ROE beklentileri: GARAN ~%27, YKBNK %15, ISCTR "düşük onlu" [D] Ak Yatırım 19.10 https://yatirim.akbank.com/_layouts/15/AkbankYatirimciPortali/Rapor/Download.aspx?ID=11378
- **Fonlama:** Sektör mevduat maliyeti Haziran sonunda %49,2 iken 16.10'da %43,2. TL kredi-mevduat makası bir haftada 11,67'den 8,87'ye daraldı. Takipteki kredi oranı %3,19. İleriye dönük F/K 3,4, F/DD 0,72 [D] (PhillipCapital, aktaran Paratic) https://paratic.com/bankacilikta-mevduat-maliyetleri-geriledi-takipteki-krediler-artti/
- **Fon krizinin kredi kanalı:** Tarfin ve Alnus 21.10'da ÖSBA ödemelerinde temerrüde düştü, notları TR D [D] https://www.endeks24.com/tarfin-tarim-ve-alnus-temerrude-dustu-notlari-tr-d-oldu. TCMB, yıl sonuna kadar vadesi dolan özel sektör borçlanma araçlarını çevirmek için kullanılan kredileri büyüme sınırından muaf tuttu [D] https://www.endeks24.com/bist-100-11151-puandan-kapatti-bankalar-yukseldi. Bu, şirketlerin refinansmanının bankalara kaydığını ve kredi riskinin arttığını gösteriyor.
- **MSCI (15.10):** Türkiye için FIF/NOS artışları ve yeni eklemeler donduruldu. Haziran 2027'ye kadar yeterli ilerleme olmazsa statü indirimi gündeme gelebilir. Yabancı sahipliği en yüksek grup olan bankalar en açıkta [D] https://www.ekonomim.com/ekonomi/msci-turkiye-endekslerinde-degisiklikleri-dondurdu-haberi-925037
- **ASELS (27.10):** Net kâr 11,23 mlr TL, beklenti 8,87 mlr (+%26,5); bakiye sipariş 30,7 mlr $. Hisse 28.10'da +%5,2 [D] https://www.bloomberght.com/aselsan-in-ucuncu-ceyrek-net-kari-beklentileri-asti-3792704. XU030'a göre z-skoru +3,4 (60g) [H]; peşinden koşmayı önermiyorum.
- **Takvim:** PPK özeti 30.10. Ekim TÜFE 3.11. Enflasyon Raporu 12.11. PPK 10.12 [D] https://www.bloomberght.com/tcmb-2026-yili-toplanti-takvimini-acikladi-3764909

**Değerleme [H]:**
| Banka | F/DD | 9 aylık ROE |
|---|---|---|
| GARAN | 1,02–1,09 (4,2 mlr pay; özkaynak 2Ç gerçekleşen 487 mlr, 3Ç tahmini 522 mlr) | ~%27 |
| YKBNK | 0,98–1,02 | %15 |
| AKBNK | 0,99 | %19 (3Ç tek başına %14) |

ROE'ye göre düzeltilmiş F/DD'de en ucuzu GARAN, en pahalısı YKBNK.

---

## FİKİR 1 (ana): Long F_GARAN1226 / Short F_YKBNK1226 — "kalite vs faize kaldıraçlı fiyatlama"
- **Ön koşul:** Garanti'nin 28.10 akşamki açıklaması. Net kâr ≥30 mlr TL ve NIM en az yatay gelmeli. Net kâr <29 mlr gelirse fikir **iptal**. 30.10 açılışında GARAN/YKBNK oranı 3,75'in üzerindeyse (28.10 spot oranı 3,675; +%2) peşinden koşma.
- **Hedge oranı:** Uzun 1 TL GARAN'a karşı **0,85 TL YKBNK** nominal açığa satış. Hesap: β250 oranı 1,06/1,24 = 0,85; β60 oranı 0,98/1,03 = 0,95; GARAN'ın YKBNK'ye regresyon betası 0,70–0,78 (korelasyon 0,89–0,90) [H]. Net XU030 betası β250 ile ≈0, β60 ile ≈+0,1.
- **Örnek büyüklük (1 mn TL sermaye, risk %1):** Aralık vadesi [T] GARAN ~134,6, YKBNK ~36,6. **18 GARAN** (nominal ≈242 bin TL) / **56 YKBNK** (≈205 bin TL). Toplam teminat ≈67 bin TL, sermayenin %6,7'si (2x çarpanla %13,5). Brüt nominal sermayenin 0,45 katı; teminata göre kaldıraç ~7x.
- **Giriş / çıkış:** Giriş bölgesi oran 3,62–3,75.
  - Zarar-kes: pair −%4 (long nominal üzerinden) ≈ oran **3,52** → ≈−9,7 bin TL (sermayenin %0,97'si).
  - Hedef: pair +%6 ≈ oran **3,90** → ≈+14,5 bin TL. Getiri/risk 1,5.
  - Süre: en geç 4 Aralık'ta (PPK'dan önce) kapat. Vadeye kesinlikle kalma (fiziki teslimat).
- **Olasılık [T]:** Pair'in 40 günlük empirik dağılımı (h=0,8, 1 yıl): 5./50./95. persentiller −%7,5 / −%1,6 / +%5,4, σ≈%4. Drift'siz bir yürüyüşte +1,5σ hedefin −1σ stop'tan önce gelme olasılığı %40. Temel üstünlük varsayımıyla bunu **%45 hedef / %40 stop / %15 zaman çıkışı** alıyorum. Beklenen değer ≈ +%1,2 nominal ≈ +2,9 bin TL. Yıllık bazda YKBNK GARAN'dan iyi gitti (yılbaşından beri pair −%7,3), yani momentum aleyhte.
- **Tez zinciri:**
  - (A) Faiz indirimi yavaş (100bp) ve risk maliyeti artıyor, sorunlu kredi hacmi +%50.
  - → (B) NIM toparlanması gecikiyor. Akbank'ın swap düzeltmeli NIM'i −100bp ile bunun ilk kanıtı.
  - → (C) Faize en duyarlı banka YKBNK'nin (Gedik: "marja en hızlı yansıtan") 3Ç'si 3.11'de; konsensüs çeyreklik yatay ama yıllık −%30.
  - → (D) ROE farkı 12 puan iken aynı F/DD ile fiyatlanma daralmaz, açılır.
  - → GARAN/YKBNK oranı +%6.
- **Karşı argüman / en büyük risk:** Ekim TÜFE düşük gelir ve piyasa Aralık'ta 150–200bp indirim fiyatlarsa YKBNK yüksek betasıyla pair'i ezer. **Tezin çöktüğü varsayım:** "piyasa 5 hafta boyunca faiz duyarlılığını değil ROE ve aktif kalitesini ödüllendirecek." Ek riskler: YKBNK 3.11 gap'i stop'u atlayabilir (kötü senaryo ~%1,5 sermaye kaybı); 02.11 teminat güncellemesi; net long ~37 bin TL için ≈2,3 bin TL baz erimesi.
- **Yanlışlama:**
  - GARAN 3Ç'de NIM daralması ya da beklenti altı kâr.
  - YKBNK 3Ç'de swap düzeltmeli NIM ≥+30bp ve risk maliyeti stabil.
  - Ekim TÜFE ≤%1,5 aylık ve bunun üstüne swap eğrisinde sert düşüş [T eşik].
  - Oran 3,52'yi kapanışta kırarsa.
- **Güven: 5/10.**

## FİKİR 2 (uydu, küçük): Long F_SAHOL1226 / Short F_AKBNK1226 — "Akbank-nötr holding iskontosu"
- **Veri:**
  - SAHOL NAV iskontosu %60; 1 yıllık ortalama %58, 3 yıllık %50. İş Yatırım 20.10'da model portföyünde AKBNK'yi çıkarıp SAHOL'u ekledi [D] https://www.yatirimx.com.tr/piyasa/is-yatirimdan-portfoy-revizyonu-akbank-portfoyden-cikarildi/26818
  - 16.10'da geri alım programı başladı: en fazla 42 mn nominal pay (~%2), 7 mlr TL, 3 yıl. 2021'deki geri alımda iskonto ~%50'den ~%20'ye inmişti [D] https://www.foreks.com/haber/detay/6ad20486422c786f3f7a4589/FRKS/tr/analiz-sabanci-holding-pay-geri-alim-programi-degerlendirmesi-deniz-yatirim-16-10-26/
- **Hedge oranı:** Uzun 1 TL SAHOL'a karşı **0,70 TL AKBNK** açığa satış. Hesap: SAHOL'un AKBNK'ye regresyon betası 0,66–0,73 (korelasyon ~0,80). %40,75 Akbank payı SAHOL piyasa değerinin ~%76'sına denk [H; pay adedi varsayımı ~2,1 mlr].
- **Büyüklük (risk %0,5):** **14 SAHOL** (≈124 bin TL) / **13 AKBNK** (≈87 bin TL). Teminat ≈30 bin TL (%3). Net β ≈ +0,1–0,2.
- **Giriş / çıkış:** Giriş: oran ≤1,35 (spot 1,321).
  - Zarar-kes: −%4 ≈ oran 1,27 → −5 bin TL.
  - Hedef: +%6 ≈ oran 1,40 → +7,4 bin TL. Getiri/risk 1,5.
  - Süre: ≤5 hafta.
  - Empirik 40 günlük dağılım: 5./50./95. persentiller −%5,7 / +%0,2 / +%7,6 [H].
- **Olasılık [T]:** %42 hedef / %40 stop. Beklenen değer pozitif ama ince; taşıma maliyeti (~2,3 bin TL) beklenen kârın büyük kısmını yiyor.
- **Tez zinciri:**
  - (A) Akbank'ta kötü haber fiyatlandı.
  - → (B) SAHOL'un Akbank dışı varlıkları (Enerjisa, sigorta, sanayi) için iskonto geri alım desteğiyle daralır.
  - → (C) Akbank betası hedge'lendiği için getiri yalnızca iskonto hareketinden gelir.
- **En büyük risk:** SAHOL tasfiyedeki fonlarda en sık bulunan BIST30 payı. Tasfiye memurlarının likit paylardan başlayıp satış yapması iskontoyu açabilir. Ayrıca SAHOL piyasa değerinin Akbank payına oranı şu an 1,31; 1 yıllık medyan 1,27 [H]. Yani Akbank'a göre ucuz değil. **Tezin çöktüğü varsayım:** "geri alım ve kurum talebi, tasfiye arzını karşılar."
- **Yanlışlama:** SAHOL yüksek hacimle AKBNK'den kötü gider (oran <1,29), ya da geri alım bildirimleri KAP'ta durur.
- **Güven: 3/10.**

## Komiteye notlar
- **ENDEKS:** F_XU030'u açığa satmak, içindeki fon krizinden etkilenmiş ve sert sıçrayabilen isimleri (ASTOR 26.10'da +%9,96) de açığa satmak demek. Pay–pay pair'ler bu riski taşımıyor.
- **MAKRO:** Fikir 1 dolaylı olarak "yavaş indirim" bahsi; Ekim TÜFE ve Aralık PPK tahminin belirleyici.
- **OPSİYON:** SPAN'da kontratlar arası mahsup varsaymadım (muhafazakâr).
- **Kombine:** İki fikir birlikte long GARAN+SAHOL / short YKBNK+AKBNK; toplam risk sermayenin %1,5'i.
