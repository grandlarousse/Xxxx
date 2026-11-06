# BIST / VIOP — 9-13 Kasım 2026 haftası hazırlık notu

Hazırlanma: Cuma 06.11.2026, ~13:00 TSİ. Fiyat verisi: 05.11.2026 kapanışı (İş Yatırım ChartData); 06.11 gün içi değerler ayrıca belirtildi. Not: "8 Kasım Pazartesi" yok; 8 Kasım Pazar, ilk işlem günü **Pazartesi 9 Kasım 2026**. Cuma kapanışından sonra (18:20 TSİ sonrası) `kod/bist_tarama.py` yeniden çalıştırılıp tablo 06.11 kapanışıyla güncellenmeli.

---

## 0. Pazartesi öncesi 10 madde

1. **Rejim: AYI.** XU100 11.333 (5.11), 50 GHO'nun %10,7, 200 GHO'nun %16,5 altında; 14.09 zirvesinden (14.236) -%20,4, 30.10 dibinden (10.760) +%5,3 tepki. 100 hisselik evrende 50 GHO üstü oran %14, 200 GHO üstü %13, Minervini şablonunu tam geçen 4 hisse (%4). USD bazında XU100 3 ayda -%21,6.
2. **İstisna: bankalar.** XBANK 50 GHO'da (%0,0), 1 hafta +%6,8, 3 ay +%3,8 (USD bazında 3 ay -%1); XLBNK 50 GHO'nun %0,7 üstünde. Sektör sıralamasında 1.-2.: XBANK/XLBNK, XULAS (1h +%15,8: THY 3Ç + Brent çöküşü).
3. **13 Kasım Cuma seans sonu kritik:** SPK'nın kredili işlemlerde özkaynak koruma oranını %35 yerine %20 uygulatma esnekliği bu tarihte bitiyor (17.09'dan beri; son uzatma 2026/78 bülten, 30.10). Uzatılmazsa 16 Kasım'dan itibaren teminat tamamlama/zorla satış riski (en çok kredili pozisyonu yüksek orta-küçük ölçek). Karar büyük olasılıkla 12-13 Kasım SPK bülteninde.
4. **MSCI:** Kasım endeks gözden geçirme duyurusu **11 Kasım 23:00 CET = 12 Kasım 01:00 TSİ**, uygulama **30 Kasım kapanışı** (VIOP Kasım vade sonu ile aynı gün). MSCI 15.10.2026'da Türkiye'de FIF/NOS artışlarını, IMI'ye yeni eklemeyi ve yukarı göçü "ikinci duyuruya kadar" dondurdu → Türkiye'den ekleme beklenmez; çıkarma/ağırlık düşüşü hâlâ mümkün. Haziran 2027'ye kadar ilerleme yoksa statü (EM→Frontier/Standalone) gündeme gelebilir.
5. **Makro hafta:** Sal 10:00 Eylül sanayi üretimi; Sal 16:30 ABD Ekim TÜFE; Per 10:30 TCMB Enflasyon Raporu 2026-IV (Karahan); Per 14:30 rezervler + haftalık menkul kıymet (yabancı akımı); Cum 10:00 Eylül ödemeler dengesi. Kasım Piyasa Katılımcıları Anketi tarihi teyit edilemedi (Ekim anketi 16.10 Cuma çıktı; Kasım muhtemelen 13 veya 20 Kasım).
6. **Bilanço:** Konsolide 3Ç yasal son gün **9 Kasım Pazartesi** → Pazartesi akşamı KAP yoğun (planlı: KCHOL, BIMAS, PGSUS, TCELL, SOKM, DOAS, AKSEN, ALARK + son güne kalan sanayi şirketleri). Bugün (6.11) seans sonrası: TUPRS, ENKAI, ULKER, BRSAN (planlı). Bankalar konsolide son gün 19 Kasım.
7. **Faiz:** Politika faizi %36 (22.10'da 100 bp indirim; O/N %34,5-%39). TLREF %35,85 (5.11). Ekim PKA: Aralık PPK (10.12) beklentisi %35, 12 ay sonrası %29,0. VIOP USDTRY ima TL faizi ~%32-34 (TLREF'in altında = indirim fiyatlanıyor). Ekim TÜFE %29,77 y/y (aylık %2,58; beklenti %2,20) — 4 aylık düşüş serisi bitti.
8. **VIOP XU030 Aralık iskontolu:** 14.605 vs spot 14.101 → baz +%3,6 / 56 gün = yıllık ~%23,3; TLREF ile teorik ~14.880 → vadeli teorik değerin **~%1,8 altında** (Şubat 2027: -%2,5). Long görüşte spot yerine vadeli + kalan nakit TLREF'te ~%1,8 ek taşıma sağlıyor (baz kapanırsa).
9. **Küresel risk:** 5 Kasım Nasdaq-100 -%6,4 (Mart 2020'den beri en kötü gün; ABD ara seçimi sonrası AI düzenleme/capex endişesi), 6 Kasım Nikkei ~-%6, KOSPI -%6/-%8 (devre kesici). Bugün 16:30 ABD tarım dışı istihdam. Brent 4 Kasım'da -%10 (ABD-İran anlaşma umudu): 3.11 103,5$ → 5.11 97,3$ → 6.11 gün içi 95,5$. Fed 28.10'da 3,75-4,00'te tuttu (2 muhalif artırım istedi).
10. **Kısa taraf:** Spot açığa satış yalnız BIST50 paylarında, 22.09.2026'dan beri yukarı adım (uptick) kuralıyla. Diğer 47 VIOP dayanağında kısa pozisyon yalnız pay vadeli ile.

---

## 1. Takvim

### 1a. 9-13 Kasım 2026 (saatler TSİ)

| Gün | Saat | Olay | Not / önceki |
|---|---|---|---|
| Pzt 9.11 | gün boyu | **Konsolide 3Ç finansal tablo yasal son günü** (SPK/MKK; konsolide olmayan son gün 30.10 idi) | Planlı: KCHOL (KAP 16.10), BIMAS, PGSUS, TCELL, SOKM, DOAS, AKSEN, ALARK |
| Pzt 9.11 | ihale | Hazine: 672 gün (13.09.2028) ve 1.617 gün (16.04.2031) sabit kuponlu tahvil yeniden ihracı, valör 11.11 | Kasım: 123,4 mlr TL borçlanma / 122,7 mlr TL servis |
| Pzt 9.11 | 04:30 / 10:00 / 18:00 | Çin TÜFE-ÜFE; Almanya dış ticaret; Fed Goolsbee | |
| Sal 10.11 | **10:00** | **TÜİK Eylül sanayi üretimi** | Ağustos: aylık -%1,0, yıllık -%1,9 |
| Sal 10.11 | ihale | Hazine: 2.877 gün (27.09.2034) tahvil yeniden ihracı; 1.820 gün (05.11.2031) kira sertifikası doğrudan satış | |
| Sal 10.11 | 06:00 | Çin dış ticaret | |
| Sal 10.11 | **16:30** | **ABD Ekim TÜFE** | önceki yıllık %3,7 |
| Sal 10.11 | 21:00 | ABD 10 yıllık tahvil ihalesi | önceki %5,30 |
| Çar 11.11 | — | ABD Veterans Day (tahvil piyasası kapalı, hisse açık) | |
| Çar 11.11 | **23:00 CET (12.11 01:00 TSİ)** | **MSCI Kasım 2026 endeks gözden geçirme duyurusu** | Türkiye'de ekleme/FIF artışı donduruldu (15.10) |
| Per 12.11 | **10:30** | **TCMB Enflasyon Raporu 2026-IV** (Başkan Karahan sunumu) | yıl sonu ara hedef/tahmin revizyonu |
| Per 12.11 | **14:30** | TCMB haftalık rezervler + **Haftalık Menkul Kıymet İstatistikleri** (30.10-6.11 haftası yabancı akımı) | önceki hafta hisse -66,3 mn $, DİBS -750 mn $ |
| Per 12.11 | 16:30 / 21:00 | ABD işsizlik başvuruları; ABD 30y ihale | 30y önceki %5,618 |
| Per/Cum 12-13.11 | akşam | **SPK haftalık bülteni** (son dönemde haftada ~2 bülten, Perşembe/Cuma akşamı; 2026/78 = 30.10 Cuma). İzlenecek: kredili işlem esnetmesi uzatması, bedelli/bedelsiz onayları, halka arz onayı | 3 Eylül'den beri ilk halka arz onayı yok; bu hafta talep toplama yok |
| Cum 13.11 | **10:00** | **TCMB Eylül ödemeler dengesi** | Ağustos cari +4,05 mlr $; altın-enerji hariç +8,2 mlr $ |
| Cum 13.11 | seans sonu | **Kredili işlem özkaynak esnetmesi (%35→%20) bitiş** (uzatılmazsa) | 2026/78 bülten |
| Cum 13.11 | (teyitsiz) | TCMB Kasım Piyasa Katılımcıları Anketi | Ekim: 16.10 Cuma |

### 1b. Kasım sonuna kadar

| Tarih | Olay |
|---|---|
| 16.11 Pzt | TURSG 3Ç bilanço için SPK ek süresi son gün |
| 17.11 Sal | TÜİK Ekim konut-işyeri satışları, tarım ÜFE; TCMB KFE |
| 18.11 Çar | FOMC 27-28 Ekim tutanakları (tahmini, 22:00 TSİ; 3 hafta kuralı); TÜİK 3Ç işsizlik (bir takvimde 10:00, teyitsiz) |
| 19.11 Per | **Bankalar konsolide 3Ç son gün** (HALKB tarihi bulunamadı; AKBNK/GARAN/YKBNK/ISCTR/VAKBN/TSKB açıkladı) |
| 27.11 Cum | TCMB Finansal İstikrar Raporu-II; Plan-Bütçe 2027 bütçesini tamamlıyor |
| 29.11 Paz | OPEC+ toplantısı (1.11'de Aralık hedefleri sabit tutuldu) |
| **30.11 Pzt** | **VIOP Kasım vade sonu** (pay vadeli Kasım: fiziki teslimat, kesinleşme = spot kapanış; USDTRY Kasım); **MSCI değişiklikleri kapanışta**; TÜİK Ekim dış ticaret + işgücü |

### 1c. Aralık ve sonrası

| Tarih | Olay |
|---|---|
| 3.12 Per | Kasım TÜFE (10:00) |
| 8-9.12 | FOMC (karar 9.12 22:00 TSİ); piyasa Aralık'ta artırım olasılığını fiyatlıyor (kaynaklar ayrışık) |
| 10.12 Per | **PPK** (Ekim PKA medyanı %35, -100 bp) |
| Aralık ortası | BIST pay endeksleri 1.1-31.3.2027 dönemi listesi (geçen dönem duyurusu ~21.09; tarih teyitsiz) |
| **31.12 Per** | **VIOP XU030 Aralık**, USDTRY Aralık, pay vadeli Aralık vade sonu (XU030 kesinleşme: son 30 dk ZAOF %80 + kapanış %20) |
| ~Mart 2027 | Fon tasfiyesi azami 6 ay sınırı (20.09 uzatmasından) |
| Haziran 2027 | MSCI'nin Türkiye düzenleme/gözetim ilerleme değerlendirmesi |

Resmi tatil: 9-13 Kasım ve Kasım sonuna kadar BIST tatili yok.

---

## 2. 3Ç 2026 bilanço durumu (BIST30 / VIOP ağırlıklı)

| Durum | Şirketler (KAP tarihi) |
|---|---|
| Açıkladı | TAVHL (21.10), AKBNK (27.10; 3Ç net 11,6 mlr TL, ç/ç -%23,7, y/y -%17,5, beklentiye paralel), ASELS (27.10), GARAN (28.10), TSKB (28.10), YKBNK (3.11; 3Ç 10,7 mlr TL, 9A +%10), CCOLA (3.11; 9A 22,5 mlr TL +%23), SAHOL (4.11; 3Ç 5,1 mlr TL), THYAO (4.11; 3Ç 61,5 mlr TL, 9A 80,3 mlr TL, beklenti üstü), TTKOM (4.11), AEFES (4.11; 9A -%20), FROTO (5.11; 9A 19,3 mlr TL -%34), TOASO (5.11; 9A 11 mlr TL +%189), MGROS (5.11; 9A -%34), PETKM (5.11; 3Ç -572 mn TL zarar), ISCTR (5.11; solo 3Ç 10,4 mlr TL, beklenti üstü, y/y -%27), DOHOL (5.11), SISE (5.11; zarar), VAKBN (~5.11), SASA (zarar sürdü) |
| 6.11 (bugün, planlı) | TUPRS, ENKAI, ULKER, BRSAN |
| 9.11 (planlı / yasal son gün) | KCHOL, BIMAS, PGSUS, TCELL, SOKM, DOAS, AKSEN, ALARK; tarih bulunamayanlar (EREGL, ARCLK, KRDMD, ASTOR, GUBRF, HEKTS, OYAKC, CIMSA, ENJSA, TKFEN, TRALT, TRMET, EKGYO, VESTL, ODAS) en geç 9.11 akşamı |
| 16.11 / 19.11 | TURSG (ek süre); HALKB ve banka konsolideleri |

Yorum: Pazartesi seansı, Pazartesi akşamı gelecek ~10 VIOP dayanağı bilançosundan ÖNCE işler; Salı açılışı bilanço gap'i taşır. Pay vadelide 9.11 akşamı pozisyon taşıma = bilanço riski.

---

## 3. Fon krizi ve aktif düzenleyici tedbirler

| Konu | Durum (06.11.2026) |
|---|---|
| Kredili işlem | Tebliğde özkaynak koruma oranı ≥%35; tedbirle aracı kurumlar ≥%20 uygulayabiliyor (17.09'dan beri; 30.10 → **13.11.2026 seans sonu**'na uzatıldı, bülten 2026/78). |
| Açığa satış | Genel yasak 2.3-26.6.2026 (ABD/İsrail-İran savaşı; 9 kez uzatıldı) sona erdi. Şu an **yalnız BIST50 paylarında**; **22.09.2026'dan beri yukarı adım kuralı** "sonraki duyuruya kadar". |
| VBTS | Otomatik, hisse bazlı: 1. seviye açığa satış + kredili işlem yasağı, 2. seviye brüt takas (15 gün), üst seviyelerde tek fiyat/emir paketi. 2.1-25.9.2026 arası 180 hissede 301 tedbir. Güncel liste: KAP / GCM "Tedbirli Hisseler". Kasım tarihli tedbir haberi bulunamadı. |
| Fon portföy kuralları | 28.08.2026 rehber: BIST30 dışı tek paya %5, toplam %20; fiili dolaşım düzenlemesi; nitelikli yatırımcı eşiği 50 mn TL. |
| Tasfiye | 17.09: 7 PYŞ'nin 131 fonu tasfiye (455.758 yatırımcı) → 17.10: 65 fon → 30.10: 38 fon; ~72 bin hesaba 68 mlr TL ödendi; olağanüstü tasfiye (Tera, Pusula, Atlas) sürüyor, ≤1 mn TL ara ödemeler 30.10'da başladı; iade kapsamı 125 mlr TL; azami süre 6 ay. Varlık Fonu piyasada alıcı oldu. |
| Soruşturma / siyaset | 112 tutuklu (4.11); eski BIST GM tutuklandı (3.11); F. B. Sayan Kaya ve eski SPK Bşk. Gönül şüpheli ifadesi (5.11); SPK Bşk. Sütçü görevden alındı (20.10); 21.10'da 4 halka açık şirketle bağlantılı 31 gözaltı kararı. Haber akışı kısa vadeli başlık riski. |
| MSCI | 15.10.2026: FIF/NOS artışı yok, IMI'ye ekleme yok, yukarı göç yok (ikinci duyuruya kadar). |
| Siyaset (genel) | Olağan seçim 7.5.2028; CHP'de mutlak butlan (21.5.2026) sonrası bölünme; erken seçim/yeni anayasa tartışması var, takvim yok. |

Pratik sonuç: Fonla bağlantılı / düşük fiili dolaşımlı küçük hisselerde arz fazlası sürüyor (XFINK 3a -%85, XBLSM -%67, XAKUR -%57, XHARZ -%62). 13.11 kredili işlem kararı bu segment için ikili risk.

---

## 4. Mevcut durum (05.11.2026 kapanış, aksi belirtilmedikçe)

### 4a. Endeksler

| Endeks | Kapanış | 50 GHO uzaklık | 200 GHO uzaklık | 200 GHO eğimi (1 ay) | 1h | 1a | 3a | 6a | 12a | USD 3a | 20g gerçekleşen vol | 52h zirveye |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XU100 | 11.333,27 | -%10,7 | -%16,5 | düşüyor | +%1,5 | -%8,4 | -%17,8 | -%21,8 | +%3,8 | -%21,6 | %31,8 | -%25,1 |
| XU030 | 14.101,00 | -%8,8 | -%10,0 | hafif yükseliyor | +%1,0 | -%8,3 | -%9,6 | -%15,2 | +%19,2 | -%13,8 | %32,4 | -%18,4 |
| XBANK | 16.085,48 | %0,0 | -%5,1 | düşüyor | +%6,8 | -%0,6 | +%3,8 | -%2,5 | +%7,7 | -%1,0 | %35,9 | -%22,1 |
| XUTUM | 13.114,51 | -%15,4 | -%22,9 | düşüyor | +%1,8 | -%11,1 | -%26,9 | -%28,0 | -%7,1 | -%30,3 | %31,2 | -%31,0 |

6.11 gün içi (~12:40): XU100 ~11.290-11.316 (açılış 11.237, -%0,84), XU030 ~14.093, XU030 Aralık vadeli ~14.690.
Genişlik (100 hisse): 50 GHO üstü %14, 200 GHO üstü %13, 52h zirveye ≤%10 olan %3. Büyük-küçük ayrışması: XU030 3a -%9,6 vs XUTUM -%26,9.

### 4b. Yabancı akımı (TCMB haftalık menkul kıymet)

| Hafta | Hisse | DİBS | ÖST | Hisse stoku |
|---|---|---|---|---|
| 23.10 | -100,0 mn $ | -183,8 mn $ | -285,3 mn $ | 33,98 → 31,57 mlr $ |
| 30.10 | -66,3 mn $ | -750,4 mn $ | -62,3 mn $ | 31,57 → 31,32 mlr $ |
| Son 6 hafta | -334,5 mn $ (hisse) | | | |
| YBB (30.10) | +1,24 mlr $ (hisse) | | | |

Toplam (hisse+tahvil) 7 haftalık çıkış >3,6 mlr $. Sonraki veri: 12.11 14:30.

### 4c. Kur, faiz, VIOP fiyatlaması (5.11)

| Kalem | Değer | Not |
|---|---|---|
| USDTRY spot | 50,048 (6.11 gün içi 50,157) | EURTRY 56,09; ons altın 4.073 $ (6.11 gün içi) |
| VIOP USDTRY Kasım (30.11, 25 gün) | 51,016 → prim %1,93 | ima TL faizi ~%32,3 (USD %3,9 varsayımı) |
| VIOP USDTRY Aralık (31.12, 56 gün) | 52,295 → prim %4,49 | ima ~%33,4; 22.10'da 52,501 idi (düşüş = indirim fiyatlaması) |
| VIOP USDTRY Ocak (29.1, 85 gün) | 53,510 → prim %6,92 | ima ~%33,9; PKA yıl sonu USDTRY beklentisi 51,55 |
| TLREF | %35,85 | 22.10 öncesi ~%36,85 |
| Politika faizi | %36 (O/N borç verme %39, borç alma %34,5) | sonraki PPK 10.12; PKA beklentisi %35 |
| XU030 Aralık vadeli | 14.605 → baz +%3,57 (56 gün), yıllık ~%23,3 | teorik (TLREF, temettü ihmal) ~14.880 → **-%1,8 iskonto** |
| XU030 Şubat 2027 | 15.268 → baz +%8,28 (113 gün), yıllık ~%26,7 | teorik farkı -%2,5 |
| DİBS 2 yıl / 5 yıl / 10 yıl | %39,38 / %38,97 / %35,75 | doviz.com 6.11 (15 dk gecikmeli, saat belirtilmiyor); 1.10: 2y %40,06, 10y %35,51. DİBS bileşik getiri; %36 basit politika faizinin haftalık bileşiği ~%43 → 2y < bileşik politika = indirim fiyatlaması, ters eğri |
| XU030 opsiyon zımni vol | bulunamadı | vekil: XU030 20g gerçekleşen vol %32,4 |
| TÜFE (Ekim) | %29,77 y/y, aylık %2,58 (beklenti %2,20); B çekirdek %28,46 | PKA yıl sonu %29,63, 12 ay sonrası %23,89 |
| Brent | 95,5 $ (6.11 gün içi); 30.10 zirve ~117,6 $ | 4.11 -%10 (ABD-İran) |

Not: ChartData "USDTRY" spot zaman damgası VIOP uzlaşma saatiyle (18:10) aynı olmayabilir; ima faiz ±1-2 pp hatalı olabilir. XU030 temettü etkisi Kasım-Aralık'ta ihmal edilebilir.

---

## 5. VIOP pratik bilgiler

| Sözleşme | Büyüklük / çarpan | Fiyat adımı | Vadeler | Günlük limit | Takasbank PSR (2.11.2026) | Takasbank baz başlangıç teminatı (yaklaşık = PSR × nominal) | Uzlaşma |
|---|---|---|---|---|---|---|---|
| XU030 endeks vadeli | 10 TL × endeks (Aralık: 14.605 × 10 = 146.050 TL) | 1 puan = 10 TL | Şub-Nis-Haz-Ağu-Eki-Ara (en yakın 3 + Aralık) | Normal seans ±%10 (BIST 2020/20 duyurusuyla, şartnamede ±%15); akşam seansı ±%3 | %11,4 | ~16.650 TL/kontrat (aracı kurumda ×1,2-×2 → ~20-33 bin TL) | Nakdi, T+1; kesinleşme = son 30 dk ZAOF %80 + kapanış %20 |
| Pay vadeli (47 dayanak) | 100 pay | 0,01 (<100 TL), 0,05 (100-500), 0,10 (500-1.000), 0,25 (1.000-2.500) | Her ay; cari + 2 ay | ±%10 (şartnamede ±%20) | %12,7 (BIMAS) – %17,0 (HALKB); THYAO %13,4, GARAN %14,4, AKBNK %15,7, ASELS %15,8, TUPRS %14,3, YKBNK %16,1 | THYAO 297×100×%13,4 ≈ 3.980 TL; GARAN ≈ 2.045 TL; ASELS ≈ 5.200 TL; TUPRS ≈ 4.745 TL | **Fiziki teslimat**, T+2; kesinleşme = vade günü spot kapanış |
| USDTRY vadeli | 1.000 USD | 0,001 = 1 TL | Her ay; cari + 15 ay | ±%10 | %11,0 | Aralık: 52.295 × %11 ≈ 5.750 TL | Nakdi (ayrıca fiziki teslimatlı USDTRY sözleşmesi var) |
| XU030 endeks opsiyon | 10 × endeks (BIST İngilizce şartname) | prim 0,01 | Çift aylar, en yakın 3 + 180 güne kadar esnek | — | %11,4 (dayanak) | alıcı primi öder; yazan teminat yatırır | Avrupa tipi, nakdi T+1 |

- Vadeler arası yayılma teminatı (spread charge): XU030 7.880 TL, USDTRY 2.185 TL, THYAO 2.580 TL, GARAN 1.360 TL (GM 2176). Aşırı hareket çarpanı 3, kapsama %32.
- Sürdürme teminatı: VIOP'ta genel uygulama başlangıcın %75'i; aracı kurum ek teminat (×1,2-×3) uygulayabiliyor (İkon ×2, Vakıf +%20, Colendi bazı sözleşmelerde ×3).
- Kaynak: Takasbank Genel Mektup 2176 (27.10.2026), 02.11.2026 ilk risk hesaplamasından itibaren geçerli. Bir sonraki parametre güncellemesi duyurulmadı (genelde aylık/iki aylık; Mart, Haziran, Temmuz, Kasım 2026 güncellemeleri var).
- **Seans saatleri:** Pay piyasası: açılış seansı 09:40-09:55, sürekli işlem 10:00-18:00, kapanış seansı 18:00-18:10. VIOP normal seans 09:30-18:10/18:15 (emir toplama 09:20'den; kaynaklar ayrışık: GCM 09:20-18:10, İşCep 09:30-18:15; pay vadeli 18:10), **akşam seansı 19:00-23:00 yalnız endeks vadelileri (XU030, XBANK, XUSIN, XLBNK, X10XB) + kıymetli maden/bakır**; pay vadeli ve (GCM 20.10.2026 listesine göre) USDTRY akşam seansında yok. Vade günü ve yarım günlerde akşam seansı yok.
- **Ücretler:** Borsa payı endeks vadeli/opsiyon %0,004 (on binde 0,4), pay/döviz vadeli %0,003. Aracı kurum komisyonu pazarlığa açık; banka kurumlarının liste fiyatı on binde 8-10 (İş Yatırım 2024 kademeli tablo: günlük ort. 0-80 bin TL hacimde on binde 10), aktif bireysel müşteride on binde 1-4 tipik (teyitsiz) + komisyon üzerinden BSMV %5. Stopaj: pay ve endeks dayanaklı VIOP sözleşmelerinde %0 (döviz/emtia dayanaklıda farklı; aracı kurumdan teyit).
- **Spot kısa:** yalnız BIST50 + uptick; VIOP pay vadeli ile 47 dayanakta kısa mümkün. BIST50 (KAP, 6.11): AKBNK AKSEN ALARK AEFES ASELS ASTOR BTCIM BIMAS BRSAN CCOLA CVKMD CWENE CANTE CIMSA DOAS ECILC EKGYO ENERY ENKAI EREGL FROTO GUBRF GLRMK SAHOL HEKTS KRDMD KCHOL MAVI MGROS OYAKC PGSUS PETKM SASA TAVHL TOASO TRMET TCELL TUPRS TRALT THYAO GARAN HALKB ISCTR TSKB TURSG SISE VAKBN TTKOM ULKER YKBNK.
- TradingView kodları: sürekli kontrat `BIST:XU030D1!`, pay vadeli `BIST:<KOD>1!`; İş Yatırım ChartData vade kodları `F_XU0301226`, `F_USDTRY1226` (AAYY).

---

## 6. Tarama sonuçları (son veri 05.11.2026)

Dosyalar: `tarama/bist_tarama_20261105.csv`, `.md`, `_viop.csv`. Evren: 47 VIOP dayanağı ∪ güncel BIST100 (KAP) = 100 hisse + 27 sektör + 9 ana endeks.

- **Trend şablonunu tam geçen (5/5): AHGAZ (RS 98), ENERY (97), RYSAS (95), ENJSA (93, VIOP'lu).** Hepsi 52h zirveye ≤%12, 50 GHO üstünde. VIOP'ta tek aday ENJSA (stop 2×ATR~ ≈ 112,4).
- 4/5 puanlı: tek eksiği "fiyat > 50 GHO" olanlar TUPRS (RS 96), ISDMR (91), GLYHO (89), BIMAS (88), KRDMD (84), AYGAZ (82), RGYAS (76) → 50 GHO'yu geri alırsa şablona girer (izleme listesi). Ek olarak ortalama dizilimi bozuk: BRSAN, VAKBN (150<200), ASELS, TRGYO (50<150), MPARK (fiyat>50 ama 50<150<200).
- RS ilk 10: TKFEN 99, AHGAZ 98, ENERY 97, TUPRS 96, RYSAS 95, TCKRC 94, ENJSA 93, BRSAN 92, ISDMR 91, HALKB 90.
- 3-1/6-1/12-1 momentum bileşik ilk 10: TKFEN, TUPRS, AHGAZ, ENERY, ISDMR, TCKRC, KRDMD, RYSAS, BRSAN, AYGAZ.
- En zayıf (VIOP/BIST50 kısa havuzu): BTCIM (BIST50, 3a -%62), CWENE (BIST50), HEKTS (VIOP+BIST50), VESTL (VIOP), CANTE (BIST50); VIOP'suz/kısa yapılamayan: EUREN, KATMR, PAHOL, BINHO, ZOREN, OBAMS, ECZYT.
- **Sektör sırası (r1a, r3a, r6a, 50 GHO uzaklığı):** 1 XBANK, 2 XULAS, 3 XILTM, 4 XTCRT, 5 XUHIZ, 6 XMADN, 7 XKMYA, 8 XSPOR, 9 XUMAL, 10 XTRZM … son: XTEKS, XMESY, XAKUR, XBLSM, XFINK. Yalnız XLBNK ve XULAS 50 GHO üstünde; hiçbir sektör 200 GHO üstünde değil.
- VIOP dayanaklarında 2×ATR~ stop mesafeleri: düşük vol TCELL %3,6, SOKM %3,8, ULKER %4,0, KCHOL %4,6, BIMAS %6,0; yüksek vol ASTOR %15, GUBRF %13, VESTL %12, TKFEN %11, TRMET %11.

Kullanım (Cuma kapanışından sonra):
```
cd raporlar/2026-11-06_kazanc_stratejileri/uygulama/kod
python3 bist_tarama.py --veri ~/bist_veri --cikti ../tarama
```
İlk çalıştırma ~2-3 dk (137 kod, 0,7 sn bekleme), sonrakiler yalnız son 15 günü tamamlar. Seans içinde çalıştırılırsa bugünkü bitmemiş bar atılır (`--gunici` ile tutulur).

---

## 7. Veri notları ve çekinceler

- İş Yatırım ChartData: düzeltilmiş kapanış (temettü/bölünme/bedelsiz); gün içi yüksek/düşük yok → 52h zirve/dip ve ATR~ kapanış bazlı (gerçek ATR'den ~%10-30 düşük olabilir). Seans içinde son bar canlı fiyattır. Bağlantı zaman zaman koparıyor (proxy/WS reset) → betikte 4 deneme + geri çekilme var.
- RS 0-99 yüzdeliği yalnız bu 100 hisselik evren içinde (IBD'deki tüm piyasa değil). PAHOL < 252 gün veri → RS yok.
- Sektör endeksleri fiyat endeksi (getiri endeksi değil); XHOLD ve XUTUM fon krizi küçük hisselerini içerir.
- VIOP baz hesapları spot ile vadeli kapanış saatleri farkı ve USD faizi (%3,9) varsayımı içerir.
- Teyit edilemeyenler: Kasım PKA tarihi, HALKB bilanço tarihi, FOMC tutanak tarihi (18.11 tahmini), XU030 opsiyon zımni vol, güncel VBTS listesi, aracı kurum komisyonları, bazı şirketlerin bilanço günleri (planlı ≠ kesin; KAP esas).

---

## Kaynaklar (erişim 06.11.2026)

- KAP endeks üyeleri (BIST100/50/30): https://www.kap.org.tr/tr/Endeksler
- BIST100 1.10-31.12.2026 dönemi değişiklikleri: https://www.paraanaliz.com/haberler/borsa-istanbul-2026-4-ceyrek-endeks-degisikliklerini-acikladi-bist-30-bist-50-ve ; https://genelekonomi.com/2026/09/21/bist-30-bist-50-ve-bist-100-endekslerine-giren-ve-cikan-hisseler-aciklandi/
- Veri takvimi (Foreks, 05.11.2026): https://www.foreks.com/haber/detay/6aec5aac4b1852391445c546/FRKS/tr/ekonomik-veri-takvimi-9-kasim-2026-pazartesi-05-11-26/ ; https://www.foreks.com/haber/detay/6aec5aac95131d72027d749f/FRKS/tr/ekonomik-veri-takvimi-10-kasim-2026-sali-05-11-26/ ; https://www.foreks.com/haber/detay/6aec5aac4b1852391445c548/FRKS/tr/ekonomik-veri-takvimi-12-kasim-2026-persembe-05-11-26/
- Kasım takvimi (TCMB/TÜİK): https://istanbulticaretgazetesi.com/kasim-2026da-ekonomi-gundemi-yogun-gececek-gozler-4-kritik-tarihte
- Hazine ihaleleri: https://www.dunya.com/ekonomi/hazineden-pes-pese-4-borclanma-islemi-tarihler-belli-oldu-haberi-846685 ; https://www.diken.com.tr/hazinenin-uc-aylik-borclanma-takvimi-9124-milyar-lira-planlaniyor/
- Bilanço tarihleri/son günler: https://piyasadetay.com/2026-3-ceyrek-bilanco-takvimi-bist-sirketleri/ ; https://rotaborsa.com/2026-ucuncu-ceyrek-bilanco-tarihleri/ ; https://yatirimci.ai/son-bilancolar ; https://bankadunyasi.com/akbank-3-ceyrek-net-kar-2026/ ; https://bankadunyasi.com/is-bankasi-3-ceyrek-2026-net-kar/ ; https://finanshatti.com/koc-holding-kchol-3-ceyrek-bilanco-tarihi-aciklandi/ ; https://rotaborsa.com/sisecam-sise-2026-yili-3-ceyrek-bilancosunu-acikladi-iste-detaylar/ ; https://www.iscihaber.net/ekonomi/vakifbank-2026-yili-3-ceyrek-bilancosu-beklentileri-karsiladi-mi/279086 ; https://www.sondakika.com/ekonomi/haber-spk-turkiye-sigorta-ya-3-ceyrek-bilancosu-icin-16--20379529/
- MSCI: https://ir.msci.com/news-releases/news-release-details/msci-november-index-review-announcement-scheduled-november-11 ; https://gazeteoksijen.com/ekonomi/mscidan-turkiyeye-kritik-uyari-endeks-degisiklikleri-donduruldu-statu-dusurulebilir-292898 ; https://www.karar.com/guncel-haberler/fon-skandalinin-faturasi-buyuyor-msci-turkiye-endekslerini-dondurdu-2078701
- Kredili işlem esnetmesi 13.11'e: https://musavirlerkulubu.com.tr/makale/spk-kredili-islemlerde-ozkaynak-orani-suresi-30-ekim-2026ya-uzatildi ; https://www.endeks24.com/spk-kredili-islemlerdeki-esnekligi-30-ekime-kadar-uzatti
- Açığa satış: https://kulisborsa.com/borsa-istanbulda-aciga-satis-yasagi-kalkti ; https://borsaistanbul.com/files/yukar%C4%B1-adim-kurali-getirilmesi-hk-duyuru-22092026.pdf ; https://www.capital.com.tr/piyasalar/borsa/bist-50de-aciga-satis-islemlerinde-yukari-adim-kurali-uygulanacak
- VBTS: https://www.cnbce.com/borsa/borsa-istanbulda-bir-hisseye-daha-tedbir-aciga-satis-ve-kredili-islem-yasagi-h38068 ; https://www.endeks24.com/vbts-tedbirli-hisselerde-ortanca-kayip-2026
- Fon krizi zaman çizelgesi: https://www.haber7.com/guncel/haber/3674340-fatma-betul-sayan-kaya-ve-eski-spk-baskani-ibrahim-omer-gonul-supheli-sifatiyla-adliyede ; https://www.ekonomigazetesi.com/ekonomi/10-soruda-fon-krizi-ne-oldu-ne-olacak-90966 ; https://www.cumhuriyet.com.tr/ekonomi/spk-131-fonun-tasfiye-suresini-uzatti-yatirimcilarin-parasi-ne-zaman-yatirilacak-2539465
- SPK bülten / halka arz: https://mansethaber.com/haber/6-kasim-2026-temettu-bedelli-ve-halka-arz-takvimi ; https://www.endeks24.com/2026-halka-arz-takviminde-3-eylulden-beri-yeni-onay-yok ; https://finoloji.com/halka-arz-takvimi
- PPK ve PKA: https://www.ensonhaber.com/son-dakika-tcmb-ekim-2026da-politika-faizini-yuzde-36ya-indirdi-h1575946 ; https://bigpara.hurriyet.com.tr/haberler/ekonomi-haberleri/son-dakika-merkez-bankasi-faiz-kararini-acikladi_ID102274454/ ; https://www.aa.com.tr/tr/ekonomi/tcmbnin-ekim-ayi-piyasa-katilimcilari-anketi-yayimlandi/4090688
- Ekim TÜFE: https://www.cumhuriyet.com.tr/ekonomi/tuik-ekim-ayi-enflasyonunu-acikladi-2552715 ; https://www.bizimsivas.com.tr/ekim-ayi-enflasyonu-yuzde-2977-olarak-aciklandi
- Yabancı akımı: https://www.borsagundem.com.tr/yabanci-yatirimcilar-hisse-ve-tahvilde-satis-yapti ; https://www.habergo.com.tr/haber/tcmb-verileri-yabanci-yatirimci-23-ekim-haftasinda-hisse-ve-tahvil-satti ; https://www.tradingview.com/news/matriks:6878909:0/
- DİBS: https://www.doviz.com/tahvil ; https://cdn.gedik.com/cdn/bulletin/2026/10/01/DIBS_Bulten_01_10_2026_f177bad2.pdf
- BIST 5.11 kapanış / 6.11 açılış: https://www.bloomberght.com/piyasalarda-gunun-ozeti-5-kasim-2026-bist-100-de-degisimler-ve-doviz-fiyatlari-pkh-3793683 ; https://www.endeks24.com/bist-100-gune-yuzde-1-eksiyle-basladi-nikkei-225-ve-kospi-yuzde-6-dustu
- Küresel: https://tr.investing.com/news/stock-market-news/guney-kore-kospi-endeksi-yapay-zeka-kayplaryla-yuzde-8-dustu-4144046 ; https://www.haberturk.com/ekonomi/piyasalarda-yapay-zeka-depremi-abd-nin-ardindan-asya-piyasalarinda-da-sert-dusus-3925292 ; https://www.federalreserve.gov/monetarypolicy/files/monetary20261028a1.pdf ; https://www.advisorperspectives.com/dshort/updates/2026/10/28/feds-interest-rate-decision-october-28-2026 ; https://financefeeds.com/brent-crude-oil-price-93-iran-bull-105-bear-88/ ; https://financefeeds.com/oil-price-opec-holds-december-targets-for-a-third-month-as-brent-ends-october-at-113-43/ ; https://thriveinmarkets.com/calendar/dates/cpi-2026/
- Siyaset: https://www.solmedya.com/2026/11/06/kilicdaroglunun-kurmaylari-parti-kararini-acikladi-chp-her-turlu-secime-var ; https://www.cumhuriyet.com.tr/yazarlar/zulal-kalkandelen/erdogan-in-4-kez-adayligi-icin-kurulan-plan-2553087
- VIOP şartnameleri: https://www.borsaistanbul.com/en/markets/viop/futures/index-futures ; https://www.borsaistanbul.com/en/markets/viop/futures/single-stock-futures ; https://www.borsaistanbul.com/en/markets/viop/futures/fx-futures ; https://www.borsaistanbul.com/en/markets/viop/options/equity-index-options ; https://www.borsaistanbul.com/en/markets/viop/market-functioning/exchange-fee
- Akşam seansı: https://www.gcmyatirim.com.tr/egitim/makaleler/viop-aksam-seansi-rehberi
- Takasbank risk parametreleri (GM 2176, 27.10.2026; 02.11.2026 geçerli): https://www.ikonmenkul.com.tr/assets/upload/2176-a7dd95c4-3dec-453f-8106-05643d3da68e_(2).pdf ; https://www.ikonmenkul.com.tr/viop/viop-baslangic-teminatlari ; https://www.vakifyatirim.com.tr/viop-teminat-tutarlari ; https://www.borsadirekt.com/viop/xu030
- Komisyon: https://www.isbank.com.tr/viop ; stopaj: https://bullsyatirim.com/upload/files/arastirma/viop-bulteni/viop-bu-lten-15.06.2026-.pdf
- Fiyat verisi: İş Yatırım ChartData IndexHistoricalAll (XU100, XU030, XBANK, sektörler, hisseler, USDTRY, TLREF, BRENT, XAUUSD, F_XU0301226, F_XU0300227, F_USDTRY1126/1226/0127), 06.11.2026 ~12:40-13:00 TSİ çekim.
