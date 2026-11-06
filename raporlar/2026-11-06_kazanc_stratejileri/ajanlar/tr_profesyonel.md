# Türk profesyonel pratiği: fonlar gerçekte ne yapıyor, kim para piyasasını yendi, 2026 fon krizi neyi gösterdi

Ajan anahtarı: `tr_profesyonel`. Tarih: Cuma 06.11.2026. Yatırım tavsiyesi değildir.

## 0. Özet

1. **Doğrudan BIST hissesi taşıyan yurt içi fonlar Temmuz 2023'ten beri para piyasası fonunu (PPF) yenemedi.** Yurt içi hisse senedi yoğun fonlarda (HSYF) medyan getiri şöyle: 1 yıl +%10,7, 3 yıl +%83,5. Aynı dönemde PPF medyanı 1 yılda +%45,5, 3 yılda +%258,7. 3 yıllık verisi olan 91 HSYF'den yalnızca biri PPF'yi yendi; o da tasfiyedeki Pardus'un BIH fonu. Yalnızca 5 yıllık getiride hisse fonları önde (medyan +%916, PPF +%447). Bu farkın neredeyse tamamı Kasım 2021 ile Kasım 2023 arasındaki negatif reel faiz döneminden geliyor.
2. **Üç alt dönemin üçünde de PPF'yi yenen fon yok.** Dönemler: Kas21–Kas23, Kas23–Kas25, Kas25–Kas26. 5 yıllık verisi olan 183 hisse, serbest ve değişken fondan hiçbiri üçünü birden kazanmadı. Son iki dönemin ikisinde de PPF'yi yenen tasfiye dışı iki fon var, ikisinin de farkı küçük:
   - BV Portföy İstatistiksel Arbitraj (BVZ): +%6,2 ve +%0,9.
   - Azimut DMR (FDV): +%1,5 ve +%3,6.
3. **Profesyonellerin elde edebildiği pozitif "alfa" küçük ve yapısal kaynaklardan geldi.** Üç kaynak görünüyor:
   - Spot–vadeli baz ve TL carry hasadı. Örneğin NBH, 31.10.2026 itibarıyla fon değerinin %327'si kadar kısa USDTRY vadelisi taşıyordu.
   - Net uzun ama hedge'li hisse pozisyonu ve yanında nakit tamponu. FDV'de yaklaşık %59 hisse, %31 kısa vadeli fon ve %19 kısa tekil vadeli var.
   - Yabancı/USD teması (blockchain ve teknoloji değişken fonları).
4. **Yüksek "TL getirileri"nin en büyük bölümü sahte çıktı.** Tera Birinci Serbest (TLY) şu rakamları raporladı: 1 yılda +%669, 3 yılda +%71.787, 5 yılda +%762.829. Buna karşın NAV oynaklığı %21,4, 1 yıllık en derin düşüşü yalnızca −%4,2. Varlıkların %89'u on hissedeydi, likit VİOP-47 hisselerinin payı %1'di. Bu ağırlıkların bir kısmı grup şirketlerindeydi (TEHOL ve TRHOL). Kriz öncesi değerlenen hisseler bugün 52 haftalık zirvelerinin %82–98 altında.
5. **Kriz ölçeği:** 31.08'de 1.233 milyar TL olan tasfiye kapsamındaki fon varlığı 30.09'da 652 milyar TL'ye indi (Gedik). 131 fon tasfiyeye alındı. BIST100, 11.09–30.10 arasında %25,6 düştü ve 1987'den beri ilk kez 7 hafta üst üste geriledi. 31.10'da Borsa İstanbul Genel Müdürü gözaltına alındı.
6. **Hisse arz baskısı (overhang) üç kaynaktan sürüyor:**
   - Tasfiye satışları. Azami süre 6 ay, yani yaklaşık Mart 2027 ortasına kadar.
   - Fon rehberindeki yoğunlaşma sınırları. BIST30 dışı hisselerde tam uyum için son tarih **31.01.2027**.
   - BIST30 paylarının fonlara blok devri. Fiyat 03.11 kapanışı, alan fonlar 3 ay borsada satamıyor; kilit yaklaşık Şubat 2027 başında açılıyor.
7. **Pazartesi (09.11.2026) için öneri.** Hedef (hurdle) TL'de PPF olmalı, XU100 değil. Pozisyon ancak sinyal olduğunda açılmalı ve VİOP-47 likiditesinde kalmalı. Tasfiyedeki fonların (tasfiye fonları) taşıdığı ve fiili dolaşımına oranla fon payı yüksek hisselerden uzak durulmalı. KAP'taki haftalık serbest fon raporları ve MKK'nın %3 eşik bildirimleri yoğunlaşma (crowding) ve arz baskısı radarı olarak kullanılabilir.

## 1. Veri ve yöntem

- **Getiriler:** fonveri.com'un TEFAS kapanış sıralamaları kullanıldı ("Föy 06.11.2026", veri 05.11.2026). 32+20+13 sayfa robots.txt'e uyularak ve varsayılan başlıklarla çekildi. Toplam 956 fonda 1, 3 ve 5 yıllık getiri var.
  - TEFAS'ın kendi API'si "Request Rejected" (WAF) döndü. Aşılmaya çalışılmadı.
- **Bitiş tarihi farkı:** Görev Ekim sonunu istiyordu, veri 5 Kasım'a ait. 30.10–05.11 arasında XU100 %5,3 yükseldi (10.759 → 11.333), PPF ise yaklaşık %0,6 kazandı. Hisse fonları Ekim sonu bazına göre yaklaşık 5 puan iyimser görünüyor. Bu fark sonucu değiştirmiyor.
- **PPF ölçütü:** 47 TL para piyasası fonunun medyanı alındı. Uç değerler (TP2 gibi tasfiyedekiler) bu yüzden etkilemiyor.

  | Dönem | PPF medyanı |
  |---|---|
  | 1 yıl | +%45,48 |
  | 3 yıl | +%258,69 |
  | 5 yıl | +%446,64 |

  Bunlardan türetilen alt dönemler:

  | Alt dönem | Kümülatif çarpan | Yıllık |
  |---|---|---|
  | Kas21–Kas23 | ×1,524 | ~%23,4 |
  | Kas23–Kas25 | ×2,466 | ~%57,0 |
  | Kas25–Kas26 | ×1,455 | — |

- **Alt dönem getirisi:** (1+3y)/(1+1y) ve (1+5y)/(1+3y) formülleriyle türetildi.
- **Endeks vekili:** XU100 için Deniz BIST100 Endeks Fonu (DZE): 1y +%8,4, 3y +%61,5, 5y +%717. BIST30 endeks fonları: 1y +%19–26, 3y +%85–103, 5y +%740–1.010.
- **USD karşılaştırması:** USDTRY 1 yılda +%18,8 arttı (fon.org.tr). Buna göre USD bazında getiriler:

  | Varlık | USD bazında 1y |
  |---|---|
  | PPF | ≈ +%22,5 |
  | HSYF medyanı | ≈ −%6,8 |
  | DZE | ≈ −%8,7 |

  TL carry geçen yıl USD bazında da hisseyi ezdi.
- **Portföyler:** fon.org.tr'nin KAP aylık/haftalık portföy dağılım raporu dökümleri kullanıldı (rapor tarihleri 30.06–31.10.2026). Hisse ve vadeli satırları ayrıştırıldı. Hesaplanan ölçüler: ilk 10 hisse ağırlığı, VİOP pay vadelisi olan 47 hissenin (likit büyük hisse vekili) payı, BIST100 payı ve vadeli yönü (Kısa/Uzun).
- **Devir hızı (turnover):** Standart belgelerde yayımlanmıyor. Tek bir vekil hesaplandı (GHS, aşağıda).
- **Sınırlamalar:**
  - **Hayatta kalma yanlılığı (survivorship):** 2026 öncesinde kapanan fonlar listelerde yok.
  - Tasfiyedeki fonların TEFAS fiyatları bayat ya da sıfır olabilir. TLY, fonveri'de 0,0 görünüyor.
  - fon.org.tr'nin "Fon Müdürü" alanında birçok fon için aynı isim (Engin Döğenci) çıkıyor. Bu alan güvenilir değil, kullanılmadı.

## 2. Kim kazandı: kategori tablosu ve "tutarlılık" testi

**Kategori medyanları (05.11.2026):**

| Grup | n (1y) | 1y | 3y | 5y | 1y'de PPF'yi yenen | 3y'de PPF'yi yenen |
|---|---|---|---|---|---|---|
| PPF medyanı | 47 | +45,5 | +258,7 | +446,6 | — | — |
| Yurt içi HSYF | 150 | +10,7 | +83,5 | +916,1 | 3, üçü de Pardus (tasfiyede) | 91'den 1 (BIH, Pardus) |
| "Hisse" adlı serbest fonlar | 87 | +2,1 | +85,6 | +670,4 | 3 (IJI, LPH, KPF) | 33'ten 1 (DDF) |
| Değişken fonlar | 134 | +28,4 | +158,8 | +592,8 | 10 | 98'den 4 (çoğu blockchain/teknoloji, yabancı) |
| Hisse + serbest + değişken (döviz, altın, PPF ve borçlanma hariç) | 487 | — | — | — | 30 | 299'dan 10 |

**Alt dönem testi (PPF'ye göre göreli, %):**

| Kod | Fon (kurucu) | Kas21–Kas23 | Kas23–Kas25 | Kas25–Kas26 | Not |
|---|---|---|---|---|---|
| BVZ | BV Portföy İstatistiksel Arbitraj | — | **+6,2** | **+0,9** | Gün sonu açık pozisyon taşımıyor; vol %1,5 |
| FDV | Azimut DMR Serbest | — | **+1,5** | **+3,6** | Net uzun + hedge; vol %9,2 |
| DDF | Deniz Dinamo HS Serbest | +36,0 | +6,0 | −2,3 | 12 hisse; ilk 10 ağırlığı %95,5; fon değeri yalnızca 48 mn TL |
| TTL | Tacirler Kartopu Serbest | +166,5 | +28,5 | −15,6 | 14 hisse, orta ölçek eğilimli |
| TPP | TEB Portföy Pusula Serbest (Pusula Portföy değil) | +251,7 | −4,3 | +0,9 | Makro: EURUSD ve gümüş vadelisi, DİBS, yabancı teknoloji |
| NBH | Neo Algoritmik | +50,9 | −20,5 | +15,5 | Kısa USDTRY vadelisi; rejime bağlı |
| PPD | Perform HS Serbest | +637,3 | −28,3 | −10,1 | 5 yılın lideri; son 3 yılda geride |
| AK3 | Ak Portföy HS (7,35 mr TL) | +263,5 | −19,2 | −15,5 | En büyük aktif HSYF'lerden |
| DZE | BIST100 endeks fonu | +231,9 | −39,6 | −25,5 | Ölçüt |

**Yanıt:**
- **Çok yıllı ve tutarlı biçimde PPF'yi yenen tek bir hisse yöneticisi yok.**
- Son 3 yılda "tutarlı" yenenler iki piyasa nötr/hedge'li fon: BVZ ve FDV. Fark kümülatif +%5–7, yıllık yaklaşık +%1,7–2,3.
- DDF ve RPT kıl payı geçiyor (sırasıyla 3 yılda +%3,6 ve +%1,2). RPT'nin %70'i mevduatta, fiilen mevduat artısı bir ürün.
- 5 yıllık liderlerin tümü (PPD, IIH, TTL, AK3) Kas21–Kas23 hisse balonundan beslendi. Son üç yılda PPF'ye karşı kümülatif %30–45 geri kaldılar.
  - Resmi doğrulama için Garanti Portföy GHS performans sunum raporuna bakıldı. Yıllık getiriler (karşılaştırma ölçütü parantez içinde):

    | Yıl | GHS | Ölçüt |
    |---|---|---|
    | 2021 | +%40,3 | +%29,0 |
    | 2022 | **+%223,5** | +%187,2 |
    | 2023 | +%62,0 | +%37,4 |
    | 2024 | +%53,8 | +%37,9 |
    | 2025 | +%16,5 | +%20,7 |
    | 2026 1. yarı | +%20,0 | +%26,4 |

    Kaynak: [GHS PSR 30.06.2026](https://garantibbvaportfoy.com.tr/assets/ghs_perf_sunm_20260630.pdf). Tür: fonun bağımsız denetimden geçen performans sunum raporu.

## 3. Tasfiye dışı ilk 15: ne tutuyorlar, ne yapıyorlar

KAP portföy raporları fon.org.tr üzerinden alındı. "VİOP47" sütunu, hisse kısmının VİOP pay vadelisi olan 47 büyük hissedeki payıdır. Vadeli yönü raporlardaki "Futures › Kısa/Uzun" satırlarından okundu.

| Kod | Rapor | Fon büyüklüğü | 1y/3y/5y (PPF farkı) | Hisse sayısı / hisse payı / ilk 10 | VİOP47 / BIST100 payı | VİOP kullanımı | Nakit | Vol / 1y en derin düşüş (MDD) | 3 ay (05.08–05.11) |
|---|---|---|---|---|---|---|---|---|---|
| PPD | 31.07 | 1,94 mr | 30,8 (−10) / 131 (−35) / 2.499 (+375) | 23 / %90,6 / %60,5 | %67 / %90 | Kısa F_XU030 (%5,2), uzun F_SASA ve F_HEKTS (%4,7) | PPP payı %6,7, VİOP teminatı %2,6 | %22,6 / −%16,9 | −%6,7 |
| IIH | 31.07 | 1,19 mr | 12,6 (−23) / 107 (−42) / 1.490 (+191) | 26 / %90 / %56 | %74 / %88 | Uzun F_AKBNK (%2,2) | Fon payları %9,4 | %22,2 / −%18,0 | −%8,6 |
| TTL | 31.10 | 0,26 mr | 22,7 (−16) / 289 (+8) / 1.479 (+189) | 14 / %81 / %64 | %47 / %80; ORGE, MPARK, ASTOR | Uzun F_ISCTR + F_GARAN (%12,5), yani kaldıraçlı | Finansman bonosu %15,8 | %19,9 / −%14,8 | −%7,2 |
| AK3 | 31.10 | 7,35 mr | 22,9 (−16) / 145 (−32) / 1.257 (+148) | 27 / %81 / %61 | %97 / %100 | Kısa %9,6 (F_XU030 ve tekil) | Ters repo %11,5 | %22,0 / −%19,3 | −%7,8 |
| TI2 | 31.10 | 2,77 mr | 6,2 (−27) / 102 (−44) / 1.212 (+140) | 56 / %94 / %50 | %64 / %81 | Uzun %10,1, kısa %8,6 | ~%4 | %23,2 / −%23,1 | −%9,8 |
| HVS | 30.09 | 2,01 mr | 15,4 (−21) / 101 (−44) / 1.201 (+138) | 28 / %93 / %57 | %84 / %96 | Teminat %3,1 | Takasbank para piyasası (TPP) %4,4 | %24,5 / −%20,9 | −%9,9 |
| KPC (katılım) | 31.10 | 3,68 mr | 28,8 (−12) / 131 (−36) / 1.154 (+130) | 29 / %86 / %57 | %51 / %81; MPARK, ALBRK | Yok; Taahhütlü İşlem Pazarı satımı %7,3 | GSYF %3,4 | %20,5 / −%20,1 | −%8,1 |
| GL1 | 30.09 | 0,94 mr | 19,3 (−18) / 115 (−40) / 1.080 (+116) | 19 / %87 / %61 | %87 / %99; **GLRMK %2,9** | Teminat %3,4 | Fon payları %8,1 | %22,1 / −%20,3 | −%8,8 |
| GAF | 30.09 | 0,16 mr | 18,8 (−18) / 118 (−39) / 1.108 (+121) | 26 / %91 / %54 | %98 / %98 | Teminat %2 | %4 | %27,3 / −%23,7 | −%8,6 |
| FDV | 31.10 | 1,50 mr | 50,7 (+3,6) / 277 (+5,1) / — | 23 / %59 / %48 | %89 / %91 | **Kısa tekil vadeli %18,7** (AKBNK, THYAO, SAHOL, ASTOR, HALKB…) | Kısa vadeli fon (KVS) %22,8, diğer fonlar %8 | %9,2 / −%4,3 | **+%4,0** |
| BVZ | 31.08 | 0,95 mr | 46,8 (+0,9) / 285 (+7,2) / — | 47 / %24 / — | %98 | Kısa %11,6, uzun %8,0 (F_XU030 ve tekil) | **Ters repo %70**, finansman bonosu %20 | %1,5 / −%0,05 | +%9,6 |
| DDF | 30.09 | 0,05 mr | 42,2 (−2,3) / 272 (+3,6) / 670 (+41) | 12 / %105 (borçlanmalı) / **%95,5** | %85 / %100; YKBNK %14,5, AKBNK %11, ENTRA %10,5 | Yok | Yok | %28,7 / −%16,4 | −%2,2 |
| NBH | 31.10 | 4,14 mr | 68,0 (+15,5) / 230 (−8) / 658 (+39) | 46 / %1,3 / — | — | **Kısa F_USDTRY %327 NAV**; tekil vadeliler %0–1 | VİOP teminatı %97 | %2,2 / −%0,06 | +%14,6 |
| LPH (Statech) | 31.10 | 2,50 mr | 60,0 (+10) / — / — | 45 / %86 / %64 | %100 | **Kısa %87,1** (tekil ve F_XU030); spot uzun + vadeli kısa | Teminat %11,3 | %3,4 / −%0,5 | +%9,4 |
| TPP (TEB) | 30.09 | 1,60 mr | 46,8 (+0,9) / 246 (−3,5) / 1.756 (+240) | Yerli hisse %4, yabancı %15 (SK Hynix, Samsung, Prosus) | — | Uzun EURUSD %54,8, uzun XAGUSD %7,9, SLV call'lar | DİBS %46 (VİOP teminatı), mevduat %20, GSYF %9,8 | %14,0 / −%7,1 | −%2,1 |

**Arketipler ve kullanıcıya etkisi:**

- **(A) Banka/büyük kurum HSYF'leri (AK3, TI2, HVS, GAF, GL1, KPC):**
  - 20–56 hisse taşıyorlar, ilk 10 ağırlığı %50–61. Hisse kısmının %64–98'i VİOP-47 büyük likit hisselerinde. Hisse oranı %81–97, nakit/ters repo %2–12.
  - VİOP taktik amaçlı kullanılıyor: F_XU030 ile %2–10 kısmi hedge ya da nakdi hisseye eşitleme. Tekil vadeliler bir hisseye fazla ağırlık (overweight) vermek için açılıyor.
  - Yönetim ücreti %2,5–3,4. 3 yılda PPF'ye karşı kümülatif −%32 ile −%44 arası geride kaldılar.
  - Kasım 2026 en derin düşüşleri −%19 ile −%26 arası. 3 aylık kayıpları −%8–10; XU100 −%17,8, XU030 −%9,6, XUTUM −%26,9. Yani büyük hisse eğilimi (BIST30 tilt) krizde koruma sağladı.
  - "BIST100 dışı" fonlar (GOH, ZJL) 3 ayda −%19 kaybetti, 1 yılda negatif.
- **(B) Yoğunlaşmış stok seçicileri (TTL, DDF, PPD):**
  - 12–23 hisse, ilk 10 ağırlığı %60–95. TTL vadeliyle kaldıraç kullanıyor, PPD kısmi XU030 hedge'i yapıyor.
  - Kas21–Kas25 arasında büyük kazandılar, son yılda PPF'nin 10–16 puan gerisinde kaldılar.
  - Kullanıcı için en "kopyalanabilir" yaklaşım bu ama getirisi büyük ölçüde rejime bağlı.
- **(C) Piyasa nötr / baz hasadı (BVZ, LPH, KPF, DPI, TTV):**
  - Spot hisse uzun, tekil veya endeks vadeli kısa; hedge oranı %71–92. Volatilite %1,5–3,4, en derin düşüş ~%0,5.
  - Getirileri PPF ±%5–10 bandında. Krizde (3 ayda +%9–10) PPF gibi davrandılar.
  - **Uyarı:** Repo içindeki tarama F_XU0301226'nın ima ettiği TL faizini %23,3, TLREF'i %35,8 buluyor ([bist_tarama_20261105.md](/home/user/Xxxx/raporlar/2026-11-06_kazanc_stratejileri/uygulama/tarama/bist_tarama_20261105.md); repo içi hesap, bağımsız doğrulanmadı). Bu doğruysa endeks bazında spot uzun / vadeli kısa işlem şu an PPF'nin altında getiri verir. Tersine, uzun vadeli + PPF ile kurulan sentetik uzun spottan ucuz kalır.
- **(D) TL carry / FX:**
  - NBH, 31.10.2026 itibarıyla fon değerinin %327'si kadar kısa USDTRY vadelisi taşıyordu. Bu, TL faiz farkını kaldıraçla toplamak demek. Rejim lehte iken (Kas25–Kas26) PPF'yi +15,5 puan yendi, Kas23–Kas25'te −20,5 puan geride kaldı.
  - GZM (Global MD Duru) aynı yapıyı kullanıyor: kısa USDTRY %306, uzun THYAO spot %55 ve kısa THYAO vadeli %57. 1y +%67, 3y +%66,5.
- **(E) Makro/USD (TPP):** Euro, gümüş, yabancı yarı iletken hisseleri ve DİBS taşıyor. 5 yıllık getirisinin büyük kısmı kur ve emtiadan geliyor.

**Devir hızı vekili:** GHS'nin aracılık komisyonu 2026'nın ilk yarısında 1,98 mn TL, ortalama fon büyüklüğü 3,12 mr TL. Bu oran %0,064/yarıyıl, yani yıllık ~%0,13 ediyor. Kurumsal komisyon tarafı ~%0,02–0,04 varsayılırsa yıllık işlem hacmi fon değerinin 3–6 katı eder. Bu da yaklaşık 1,5–3 tam tur devir demek. Bu bir kaba tahmin.

## 4. 2026 fon krizinin anatomisi

### 4.1 Takvim

Kaynaklar resmi bülten, haber ve hukuk derlemesidir.

| Tarih | Olay |
|---|---|
| 2025 4. çeyrek | SPK düşük fiili dolaşımlı paylarda olağan dışı fiyat hareketleri gözledi |
| 04.11.2025 | Hazine ve Maliye Bakanı "bazı fonlarda manipülasyon bilindiğini" söyledi |
| 18.12.2025 | Nitelikli yatırımcı eşiği 1 mn TL'den 10 mn TL'ye çıktı |
| Aralık 2025 | Pusula fonlarının KTLEV payı sermayenin %25,59'una ulaştı |
| 18.08.2026 | Pusula fonlarının GUNDG payı %38,67 oldu |
| 19.08.2026 | İstanbul Cumhuriyet Başsavcılığı SPK'ya gizli yazı gönderdi |
| 28.08.2026 | Yeni fon rehberi (karar 52/1589) yayımlandı; çıkışlar başladı |
| 15.09.2026 | Pusula temerrüt açıkladı |
| 16.09.2026 | Tera TP2 ve THF temerrüdü; KTLEV, GUNDG ve DSTKF için suç duyurusu |
| 17.09.2026 | 131 fon tasfiyeye alındı, 170 fon alım satıma kapatıldı. Kredili işlemlerde özkaynak oranı geçici olarak %20'ye indi |
| 19–22.09.2026 | Tera ve Pusula yönetimi (E. Tezmen, S. Turhan, E. ve K. Alkin, A. Öztürk) gözaltına alındı, ardından tutuklandı |
| 20.09.2026 | Tera'ya yaklaşık 300 mr TL iade talebi geldi |
| 30.09.2026 | Ara ödeme (1 mn TL/fon) kararı; TMSF üç yatırım bankası ve iki faktoring şirketinde ortaklık haklarını kullanmaya başladı |
| 26–27.10.2026 | Tera ve Pusula PYŞ'lerinin faaliyeti durduruldu, 7596 sayılı Kanun yayımlandı, Tera Yatırım'ın lisansları iptal edildi |
| 31.10.2026 | Borsa İstanbul Genel Müdürü rüşvet ve örgüt iddiasıyla gözaltına alındı |
| 03.11.2026 | 100 fonda 247.839 yatırımcıya toplam 97,3 mr TL ödendi; tasfiyede 38 fon kaldı (28.10 itibarıyla) |

Kaynaklar: [BloombergHT 17.09](https://www.bloomberght.com/spk-dan-yeni-piyasa-tedbirleri-3788617) (haber), [Euronews 17.09](https://tr.euronews.com/2026/09/17/turk-piyasalarinda-fon-skandali-tam-olarak-ne-oldu-ve-sirketler-neyle-suclaniyor) (haber), [Pega Hukuk kronoloji](https://pegahukuk.com/fon-krizi-nedir/) (hukuk derlemesi, ikincil), [Karar](https://www.karar.com/ekonomi-haberleri/fon-skandalinin-faturasi-agirlasiyor-borsada-40-yil-sonra-bir-ilk-2081849) (haber), [Paratic / SPK Bülteni 2026/59](https://paratic.com/spkdan-3-hissede-sert-karar-cok-sayida-kisiye-islem-yasagi/) (haber, resmi bülten aktarımı).

### 4.2 Ölçek

Kaynak: [Gedik Yatırım, 05.10.2026](https://cdn.gedik.com/media/media/tvmjp14x/gedik_yatirim_tasfiye_fonlari_degerlendirme_05102026.pdf) (aracı kurum raporu; TEFAS, KAP ve Finnet verisi).

- **Fon varlığı:**
  - Tasfiye kapsamındaki fonlar: 31.08'de 1.233,2 mr TL, 15.09'da 992,5 mr TL, 30.09'da 652,3 mr TL. Fonlar işleme kapalıyken 15–30.09 arasında %34,3 eridi.
  - Kapalı fonlarla birlikte toplam: 1.470 mr TL'den 756 mr TL'ye.
- **Yoğunlaşma:** Kapsamdaki varlığın %76,5'i Tera'nın 6 fonunda. Yalnızca TLY (243,6 mr TL) ve TP2 (224,4 mr TL) toplamın %72'si.
- **Likiditesi sınırlı varlık oranı:**
  - Tüm kapsamda %58,6, yaklaşık 334 mr TL.
  - Tera'nın üç fonu hariç %23,2.
  - Hisse ve serbest fonlarda %80,1.
- **Değerleme ile nakit girişi farkı:** İhraçtan bu yana net giriş 322 mr TL, fonlama maliyetiyle bugünkü değeri yaklaşık 497 mr TL. 30.09'daki fon büyüklüğü bunun yaklaşık 156 mr TL üzerinde. Fon değerlerinin önemli bir bölümü nakitten değil, portföy değerlemesinden geliyor.
- **İlişkili taraf:** İzleme listesindeki ÖST pozisyonlarının yaklaşık %89'u kurucunun kendi grubunun ihracı (en büyük PYŞ'de 26,1 mr TL). En büyük PPF'de ters repo teminatı olarak alınan 28,4 mr TL'lik kıymetin tamamı aynı grubun ihracı.
- **Likiditesi sınırlı 123 hisse:**
  - Pozisyon değeri 146,5 mr TL, ilk 10 hisse bunun %86'sı. Son bir ayda pozisyon ağırlıklı ortalama getiri −%58.
  - Ortalama günlük hacmin %20'si ile satılırsa pozisyonların %45'i 60 işlem gününden uzun sürer.
  - En büyük 6 pozisyon toplam 106,2 mr TL. Satışları 27–126 işlem günü sürer; bu hisseler bir ayda %44–71 düştü.

### 4.3 Mekanizma: "yüksek getiri" nereden geldi?

Kaynaklar resmi suç duyurusu, haber ve aracı kurum analizidir.

1. **Düşük fiili dolaşımlı hisselerde fon payı fiili dolaşımı aştı.** KTLEV'de Pusula payı sermayenin %25,6'sından %32,9'una çıktı. PASEU'da fon payı/fiili dolaşım oranı QNB'ye göre %198, fonoloji'ye göre %266. Fonların alımı fiyatı yükseltti. Bu, NAV'ı ve getiri sıralamasını (ör. Tera'nın "serbest fonlar arasında lider" paylaşımları) yukarı taşıdı. Bu da yeni para getirdi ve yeni para aynı hisselere girdi.
   - Tera'nın kendi X paylaşımları: TLY, 12.08.2025 itibarıyla 6 ayda +%499,7; 07.11.2025 itibarıyla 1 ayda +%61,4 (pazarlama metni).
2. **Grup ve ilişkili taraf varlıkları.** Grup şirketlerinin portföydeki payı:

   | Fon | Rapor | TERA | TRHOL | TEHOL | Toplam |
   |---|---|---|---|---|---|
   | THF | 31.08 | %7,7 | %5,9 | %4,3 | ≈%17,9 |
   | DOH | 31.08 | %9,2 | %4,3 | %3,8 | ≈%17,3 |
   | TLY | 31.08 | %0,9 | %8,3 | %14,1 | ≈%23 |

   TERA, TRHOL ve TEHOL Tera grubu şirketleri. TLY ayrıca DSTKF'de %24,8 taşıyordu; Tera Yatırım'ın kendi DSTKF payı da 16.09'da %10,4'e çıktı. Ek olarak PPF'lerde grup ÖST'leri ve repo teminatları vardı.
3. **İmkânsız istatistik.** TLY %87 hisse taşırken yıllık oynaklığı %21, en derin düşüşü −%4,2 ve 3 yıllık getirisi +%71.787 çıkıyor. Bu, likit olmayan pozisyonların "işaretlenmiş" fiyatla değerlendiğinin imzası.
   - Gedik'in bulgusu da bunu destekliyor: likiditesi sınırlı hisselerin medyan 1 aylık getirisi −%39,8 ve 70 hisse bir ayda %50'den fazla düştü. Önceki fiyatlar piyasa derinliğini yansıtmıyordu.
4. **Kredi ve teminat döngüsü.** Hisseler teminat gösterilerek borçlanıldı. Yeni rehber (28.08) yoğunlaşmayı sınırladı ve satış başladı. Satış fiyatı düşürdü, fiyat düşüşü iadeleri artırdı; iade gelince temerrüt geldi.
5. **SPK suç duyurusu yapılan 13 hisse (SPKn m.107/1):** KTLEV, GUNDG, DSTKF, OZATD, TRHOL, ODINE, VSNMD, IEYHO, ALKLC, ANELE, PASEU, SELEC, MANAS. Ayrıca 41 hissede inceleme sürüyor.
   - Kaynak: [Pega Hukuk hisse listesi](https://pegahukuk.com/fon-krizi-hisseleri/) (hukuk derlemesi; SPK bültenleri 2026/59–77).

**Sonuç:** 2024–2026 boyunca BIST'te tabloların tepesinde görünen "%200–700" fon getirilerinin büyük kısmı üç şeyden geldi: likidite yanılsaması, kendi alımıyla fiyatı yükseltme (dairesel alım) ve ilişkili taraf değerlemesi. Gerçek, nakde çevrilebilir getiri değildi. Gerçek profesyonel getiri yukarıdaki yapısal %0–5'lik fazla getirilerdir.

### 4.4 Fiyat çöküşü (fvt.com.tr, önceki kapanış ≈ 05.11.2026)

| Hisse | 52 haftalık zirve → son | Zirveden | Fiili dolaşım | Piyasa değeri | Not |
|---|---|---|---|---|---|
| DSTKF | 3.960 → 68,85 | −%98,3 | %14,2 | 23,2 mr | 01.10'da BIST30'dan çıkarıldı. TMSF kayyum. Destek Holding'in %73,8'lik payının satışı istendi |
| OZATD | 5.115 → 126 | −%97,5 | %15,2 | 7,3 mr | TLY'de %19,8 |
| TEHOL | 52,5 → 1,25 | −%97,6 | %46,0 | 2,4 mr | Tera grubu; TMSF kayyum |
| TRHOL | 4.502,5 → 140,1 | −%96,9 | %29,2 | 3,4 mr | Tera grubu; 37 kişiye suç duyurusu |
| TERA | 401,25 → 11,82 | −%97,1 | %31,7 | 7,5 mr | Aracı kurum lisansları iptal |
| GUNDG | 2.707,5 → 59,65 | −%97,8 | %15,2 | 2,7 mr | Pusula'nın %38,7 payı |
| ODINE | 3.512,5 → 52,95 | −%98,5 | %20,3 | 6,2 mr | Suç duyurusu |
| ANELE | 229,4 → 5,69 | −%97,5 | %21,2 | 1,6 mr | TLY'de yaklaşık %15 (sermaye) |
| BIGEN | 195,9 → 5,12 | −%97,4 | %23,4 | 3,6 mr | THF'de %7,4 |
| IEYHO | 234,9 → 5,84 | −%97,5 | %31,9 | 3,3 mr | Suç duyurusu |
| PEKGY | 19,94 → 0,80 | −%96,0 | %51,6 | 4,8 mr | Fon payı sermayenin %33,5'i |
| KTLEV | 69,0 → 4,02 | −%94,2 | %33,2 | 31,2 mr | Pusula'nın payı sermayenin %32,9'u |
| MANAS | 40,42 → 1,85 | −%95,4 | %64,1 | 0,7 mr | Tera Yatırım'ın payı %15,5 |
| PASEU | 268 → 25,34 | −%90,5 | %9,8 | 18,2 mr | Fon payı fiili dolaşımın %198–266'sı |
| KARCL | 233 → 28,6 | −%87,7 | %13,4 | 27,7 mr | Tera'nın payı sermayenin %5,8'i |
| SELEC | 402,5 → 72,15 | −%82,1 | %12,9 | 45,4 mr | Tera'nın payı sermayenin %5,3'ü; suç duyurusu |
| ALKLC | 524,5 → 17,81 | −%96,6 | %37,3 | 2,2 mr | Suç duyurusu |
| VSNMD | 85,69 → 18,40 | −%78,5 | %21,2 | 3,6 mr | Suç duyurusu |

Kaynak: fvt.com.tr hisse sayfaları (veri sitesi; BIST verisi, gecikmeli). TEHOL için ayrıca [USC Markets](https://www.uscmarkets.com/borsa-istanbul/tehol) var: zirve 51,85 TL (19.08.2026). [Endeks24](https://www.endeks24.com/borsa-istanbul-neden-dusuyor-fon-krizinden-bugune-tablo) ise TEHOL'un Ekim'de %96,5 düştüğünü yazıyor.

### 4.5 Hâlâ arz baskısı altındaki hisseler

**(a) QNB Invest tablosu (18.09.2026, o günkü fiyatlarla):** Olası satış tutarı ve fon payının fiili dolaşıma oranı. Kaynak: [BorsanınGündemi](https://www.borsaningundemi.com/haber/fon-tasfiyesinde-satis-baskisi-hangi-hisselerde-1908730) (haber; aracı kurum hesabı).

| Hisse | Olası satış | Fon payı / fiili dolaşım |
|---|---|---|
| PASEU | 12,4 mr TL | %198 |
| KTLEV | 57,2 mr TL | %124 |
| ANELE | 7,8 mr TL | %95 |
| TEHOL | 35,7 mr TL | %87 |
| TRHOL | 26,0 mr TL | %71 |
| OZATD | 52,2 mr TL | %69 |
| GUNDG | 2,5 mr TL | %68 |
| DSTKF | 70,2 mr TL | %66 |
| PEKGY | 17,7 mr TL | %63 |
| SKYLP | 0,3 mr TL | %47 |

BIST30'da etki sınırlı görülüyordu: AKBNK'ta 1,1 mr TL (fiili dolaşımın %0,6'sı), THYAO'da 0,9 mr TL (%0,5).

**(b) fonoloji (05.11.2026 güncellemesi, KAP pay sahipliği bildirimleriyle):** Tasfiyedeki fonların bilinen hisse pozisyonu 30 fonda 169 hisse, 46,6 mr TL. Ek olarak rapor yayımlamayan fonlarda yaklaşık 24,9 mr TL bilinmeyen pozisyon var. Kaynak: [fonoloji/spk-tasfiye](https://fonoloji.com/spk-tasfiye) (veri sitesi; KAP ve MKK verisi).

En büyük kalemler:

| Hisse | Kurucu | Lot | Sermaye payı | Fiili dolaşıma oranı | Tutar |
|---|---|---|---|---|---|
| PASEU | Pusula | 175,5 mn | %26,1 | %266 | 4,85 mr TL |
| KTLEV | Pusula | 683 mn | %32,9 | — | 3,04 mr TL |
| SELEC | Tera | 32,7 mn | %5,3 | %41 | 2,41 mr TL |
| DSTKF | Tera | 34,0 mn | %10,2 | %72 | 2,35 mr TL |
| **GLRMK** | Pusula | 17,8 mn | %5,5 | %22 | 2,08 mr TL |
| KARCL | Tera | 48,1 mn | %5,8 | %43 | 1,61 mr TL |
| PEKGY | — | 1,7 mr | %33,5 | %65 | 1,61 mr TL |

Likit BIST30 kalemleri de var ama hepsi sermayenin %1'inin altında: YKBNK 3,10 mr, THYAO 3,07 mr, AKBNK 2,28 mr, ASELS 2,26 mr, TUPRS 1,90 mr, EREGL 1,58 mr TL.

**(c) Satış yöntemleri:**
- **BIST30 payları:** Tasfiyedeki fonların BIST30 payları borsa dışında hızlandırılmış blok satışla PYŞ yatırım fonlarına ve emeklilik fonlarına devrediliyor. Satış 20 eşit paket halinde, 03.11.2026 kapanışı esas alınarak yapılıyor. Alıcı fonlar bu payları **3 ay boyunca borsada satamıyor ve türevle dolaylı satış yapamıyor.**
  - Kaynak: [Türkiye'de İş Dünyası, 04.11.2026, TSPB yazısı](https://turkiyedeisdunyasi.com/tasfiye-surecindeki-fonlardan-30-portfoy-icin-satis-esaslari-netlesti-145857/) (haber).
- **Likit olmayan paylar:** 7596 sayılı Kanun hâkim ortağa satış, geri alım, toptan satış ve Kurul onaylı borsa dışı satış yollarını açtı (hukuk derlemesi). Gedik ise likit olmayan paylar için kredili işlem imkânı ve rekabetçi ihale öneriyor.
- **Ayrı bir ikinci arz baskısı kaynağı, tasfiye dışındaki fonlar:** Yeni rehbere göre serbest fon başına sınır, şirketin fiili dolaşım oranına göre kademeli:

  | Fiili dolaşım oranı | Fon başına azami pay |
  |---|---|
  | <%25 | %8 |
  | %25–50 | %6 |
  | %50–75 | %4 |
  | >%75 | %2 |

  Aynı kurucunun fonları toplamda bunun 2 katını tutabiliyor. Ayrıca 5/20 kuralı var: tek tek %5'i aşan pozisyonların toplamı fonun %20'sini geçemiyor. BIST30 bu sınırlardan muaf.
  - Kademeli uyum takvimi (31.10: aşımın 1/3'ü, 30.11: 2/3'ü) kaldırıldı. **Tek son tarih 31.01.2027** (SPK 75/1897, 26.10.2026).
  - Kaynaklar: [Sözcü 30.08](https://www.sozcu.com.tr/fonlarda-oyunun-kurallari-degisti-p353815) (haber), [BloombergHT uyum takvimi](https://www.bloomberght.com/spk-fon-rehberi-nde-uyum-takvimini-guncelledi-3792508) (haber), [Endeks24](https://www.endeks24.com/spk-fon-rehberinde-uyum-tarihi-31-ocak-2027) (haber).

**Arz baskısı takvimi:**

| Tarih | Olay |
|---|---|
| 09.11.2026 | İlk işlem günü |
| ~03.02.2027 | BIST30 blok devrinde alıcı fonların satış kilidi açılıyor (03.11 + 3 ay) |
| 31.01.2027 | BIST30 dışı hisselerde yoğunlaşma sınırına tam uyum |
| ~17.03.2027 | Azami tasfiye süresi doluyor (17.09 + 6 ay) |

## 5. Yöneticiler ne diyor? (doğrulanabilir süreçler)

- **Doğrulanabilir kayıtlı ve swing ufkundaki süreci anlatan röportaj neredeyse yok.** Aramalarda Perform (H. Gökçe), Tacirler (T. Koyuncu), Global MD (B. Subaşar), Neo, Azimut ve BV yöneticilerinin süreç anlatan bir röportajı bulunamadı. Bu, bulgunun kendisi: Türk fon yöneticileri süreçlerini kamuya pek anlatmıyor. En güvenilir kanıt, KAP'taki izahname metinleri ve portföy raporlarından okunan davranış.
- **[Ekonomist, 18.01.2026, "Şampiyon fon yöneticilerinden 2026 stratejileri"](https://www.ekonomist.com.tr/makale/sampiyon-fon-yoneticilerinden-2026-stratejileri-70123)** (röportaj derlemesi):
  - Pardus'tan Furkan Açar, BDS fonu için "BIST30 dışı, %85–90 hisse, çarpan ve nakit üretimi odaklı, kademeli pozisyon, uzun vade" diyor. **Pardus 9 ay sonra tasfiyede.** "Şampiyon" etiketi süreç kalitesini kanıtlamıyor.
  - Ak Portföy'den Emre Tayfur, yabancı hisse fonu için "bilanço kalitesi ve nakit akışı" vurgusu yapıyor.
  - TEB Portföy'den Emre Karakurum gümüşte fon, ETF ve vadeli seçimi yapıyor. Bu kişi TPP'nin de yöneticisi; KAP'ta 2010'dan beri görevde.
  - Garanti'den Mehmet Kapudan, emeklilik fonunda yerli/yabancı teknoloji ağırlığını ve TL ağırlığını aktif yönetiyor (2025: +%44, BIST100 +%14,6).
- **KAP izahnamesindeki stratejiler (resmi belge):**
  - **FDV:** Portföyün en az %51'i BIST hissesi. "Portföy yöneticisi net uzun hisse pozisyonu taşımayı hedeflemektedir." Vadeli, opsiyon ve swap ile uzun ve kısa pozisyon, arbitraj ve piyasa nötr işlemler serbest. Eşik değer: %51 BIST100 getiri endeksi + %49 (1 aylık mevduat endeksi + 100 baz puan). Risk değeri 4. Kaynak: [KAP FDV](https://kap.org.tr/tr/fon-bilgileri/genel/fdv-azimut-portfoy-dmr-serbest-fon).
  - **BVZ:** Spot ve türev arasındaki arbitraj fırsatlarını kullanıyor, "gün sonunda açık pozisyon taşımıyor". Eşik değer: mevduat endeksi ×1,10. Kaynak: [BV Portföy](https://www.bvportfoy.com/tr/fon/tr-istatistiksel-arbitraj-serbest-fon-bvz) (kurucu sayfası, pazarlama).
  - **DPI:** Spot ile VİOP arasındaki fiyat uyumsuzluklarını gün içinde algoritmayla değerlendiriyor (kurucu sayfası).
  - **NBH:** "Yapay zekâ ve derin öğrenme algoritmaları" diyor; fiilen kaldıraçlı kısa USDTRY vadelisi taşıyor (KAP portföy raporu). Pazarlama metni ile pozisyon arasındaki farka dikkat.
- **Prop trader'lar:** Türkiye'de denetlenmiş ya da bağımsız doğrulanmış prop/bireysel trader kaydı bulunamadı. Sosyal medyadaki iddialar anekdot düzeyinde. Krizde 246 hesaba erişim engeli getirildi ve 16 kişi tutuklandı; "fenomen" kaynaklar kirli ([Euronews 20.09](https://tr.euronews.com/2026/09/20/borsa-sorusturmasi-tera-ve-pusula-yoneticileri-gozaltina-alindi)).

## 6. Pazartesi için pratik dersler

**Kopyalanacaklar:**
1. **Ölçüt disiplini.** Her fikir PPF'ye (≈%36 yıllık; politika faizi %36) ve USD bazında yaklaşık %4 artı TL carry'ye karşı ölçülmeli. Profesyonellerin 3 yıllık kaydı, yön tahminine dayalı BIST hissesinin bu ölçütü geçmediğini gösteriyor. Varsayılan pozisyon nakit/PPF olmalı, hisse riski ancak sinyal varken alınmalı.
2. **FDV tipi yapı.** Bu, son iki alt dönemin ikisinde de PPF'yi yenen tek "hisse" fonu. Yapı şöyle:
   - Net uzun ~%40–60.
   - Likit büyük hisseler: FDV'nin hisse kısmının %89'u VİOP-47'de.
   - Tekil vadeli kısa ile hedge.
   - Portföyün ~%30'u kısa vadeli fonda.
   - Hedef volatilite ~%9, en derin düşüş ~%4.
3. **Likidite filtresi.** Kurumların hisse kısmının %64–100'ü VİOP-47'de. Bireysel trader için de pozisyonun ADV'nin küçük bir kesri olması ve fon/kurum payı fiili dolaşıma oranla düşük hisse seçilmesi gerekiyor.
4. **Vadeli yapısını kullanmak.**
   - Kurumlar F_XU030'u %2–10 hedge ve nakdi hisseye eşitlemek için kullanıyor.
   - Repo içi tarama F_XU0301226'yı ima edilen TL faizi açısından TLREF'in yaklaşık 12 puan altında gösteriyor (doğrulanmadı).
   - Bu doğruysa uzun pozisyonu spot yerine "F_XU030 uzun + nakit PPF'de" ile kurmak daha ucuz. Kısa hedge ise pahalı.
   - Pazartesi açılıştan önce baz yeniden hesaplanmalı.

**Kaçınılacaklar:**
- 13 suç duyurulu hisse ile Tera, Pusula ve Hedef grup şirketleri (TERA, TEHOL, TRHOL, HEDEF, HDFGS, DSTKF). Bunlar ya TMSF kayyumu altında ya da hâkim ortak satışı bekliyor.
- QNB ve fonoloji listesinde fon payı fiili dolaşımın %20'sini aşan hisseler: PASEU, KTLEV, ANELE, TEHOL, TRHOL, OZATD, GUNDG, DSTKF, PEKGY, SKYLP, SELEC, KARCL.
  - Zirveden %82–98 düşmüş olsalar bile Gedik'in hesabına göre ADV'nin %20'siyle satış 27–126 işlem günü sürüyor. Arz Mart 2027'ye kadar devam edebilir.
  - "Dipten tepki" işlemi negatif çarpıklıklı (negatively skewed); yapılacaksa yalnızca çok küçük boyutla.
- **GLRMK özel uyarı.** BIST100 üyesi, zirveden −%52, 3 ayda −%31. Pusula'nın payı sermayenin %5,5'i, fiili dolaşımın %22'si. Ayrıca PPD, GL1, KPC ve TPP de taşıyor. Hem tasfiye arzı hem kalabalık pozisyon var.
- **31.01.2027'ye kadar** fon payı yüksek BIST30 dışı küçük ve orta ölçekli hisseler (yoğunlaşma sınırı satışı). Halka arz endeksi XHARZ 3 ayda −%62, XFINK −%85.
- Tasfiye fonu değil ama aynı PYŞ'lere ait kapalı fonların (170 fon, 103,7 mr TL) yeniden açılışı yeni iade dalgası getirebilir. Fon payları bu fonlarda yüksek olan hisseler bu yüzden izlenmeli.

**Kamuya açık fon verisini sinyal olarak kullanmak:**
1. **Yoğunlaşma oranı.** Her hisse için şu oran hesaplanır: (TEFAS fonlarının toplam payı) / (fiili dolaşımdaki pay).
   - Veri: KAP'ta serbest fonların haftalık portföy raporları (3 iş günü içinde yayımlanıyor) ve aylık HSYF raporları; pratikte fonoloji, fon.org.tr ve fvt.com.tr gibi dökümler.
   - %20'nin üzeri kırmızı bayrak: likidite yanılsaması ve zorunlu satış riski. %8'in üzeri, rehber sınırı açısından uyum satışı adayı.
2. **MKK eşik bildirimleri.** 11.09.2026'dan beri alt eşik %3. KAP'ta günlük yayımlanıyor.
   - Fon ya da grup hesabının eşiği aşağı geçmesi tasfiye satışının izidir. Fonlar arası transfer (ör. 16.09 DSTKF'de fon → Tera Yatırım) hileli el değiştirme işareti.
3. **Fon akımı.** fonveri'nin "para akımı" sayfası (TEFAS günlük büyüklük ve yatırımcı verisi): bir PYŞ'nin fonlarından çıkış, o fonların en büyük hisse pozisyonlarındaki satıştan önce geliyor.
4. **Konsensüs ve kalabalık.** Tasfiye dışı iyi fonların ortak çekirdeği şu hisseler: ASELS, TUPRS, BIMAS, AKBNK, YKBNK, THYAO, SAHOL. Bunlar likit; kalabalık riski düşük ama bilgi değeri de düşük.
   - Asıl sinyal, düşük likiditeli bir isimde birden fazla fonun aynı anda büyümesi. 2025–2026'da bu, dolandırıcılığın öncü göstergesiydi.

## 7. Karşı argümanlar ve belirsizlikler

- PPF'nin baskın olduğu 3 yıl, %40–50 politika faizi dönemiydi. Faiz düşüş patikasında (şimdi %36) hisse primi geri dönebilir. Kas21–Kas23 tam olarak bunun örneği. Yani "hisse kaybeder" rejime bağlı bir sonuç, sabit değil.
- fonveri ve fon.org.tr birincil kaynak değil. Kritik rakamlar KAP ve TEFAS'tan teyit edilmeli: TLY'nin getirileri, NBH'nin USDTRY pozisyonu, overhang tutarları.
- QNB ve fonoloji'nin fiili dolaşım oranları farklı yöntemlere dayanıyor (11.09'dan itibaren yeni hesaplama yöntemi). PASEU için %198 ile %266 arası fark bu yüzden.
- Tasfiyedeki Pardus fonlarının "getirileri" (BIH 3y +%750) güvenilmez. Fiyatlama bayat olabilir; değerlendirme dışı bırakıldı.
- BIST yönetiminde (Genel Müdür gözaltında) ve SPK'da yaşanan süreç, beklenmedik düzenleme ve şok riskini artırıyor. Hafta sonu ve gece taşınan pozisyonların boyutu küçültülmeli.

## 8. Kaynaklar (tür etiketiyle)

- **Resmi veya resmi belge aktarımı:**
  - SPK bültenleri 2026/59–77, aktaran: [Paratic](https://paratic.com/spkdan-3-hissede-sert-karar-cok-sayida-kisiye-islem-yasagi/), [Pega Hukuk](https://pegahukuk.com/fon-krizi-hisseleri/).
  - [SPK ara ödeme duyurusu](https://spk.gov.tr/duyurular/basin-duyurulari/2026/tasfiyedeki-fonlara-iliskin-ara-odeme-duyurusu).
  - [KAP FDV fon bilgisi](https://kap.org.tr/tr/fon-bilgileri/genel/fdv-azimut-portfoy-dmr-serbest-fon).
  - [Garanti GHS performans sunum raporu 30.06.2026](https://garantibbvaportfoy.com.tr/assets/ghs_perf_sunm_20260630.pdf) (denetimden geçen).
- **Aracı kurum raporu:**
  - [Gedik Yatırım 05.10.2026](https://cdn.gedik.com/media/media/tvmjp14x/gedik_yatirim_tasfiye_fonlari_degerlendirme_05102026.pdf).
  - QNB Invest overhang tablosu, aktaran: [BorsanınGündemi 18.09](https://www.borsaningundemi.com/haber/fon-tasfiyesinde-satis-baskisi-hangi-hisselerde-1908730).
- **Veri siteleri (TEFAS, KAP ve BIST'ten türetilmiş, ikincil):**
  - [fonveri 5 yıl sıralaması](https://fonveri.com/tum-fonlar?grup=yatirim&donem=getiri_5y), ayrıca 1y ve 3y sıralamaları.
  - [fon.org.tr fon sayfaları](https://fon.org.tr/fon/PPD) (ör. /fon/TLY, /fon/NBH, /fon/FDV).
  - [fonoloji SPK tasfiye](https://fonoloji.com/spk-tasfiye).
  - fvt.com.tr hisse sayfaları (/hisseler/yerli/DSTKF vb.).
- **Haber:**
  - [BloombergHT 17.09](https://www.bloomberght.com/spk-dan-yeni-piyasa-tedbirleri-3788617), [Euronews 17.09](https://tr.euronews.com/2026/09/17/turk-piyasalarinda-fon-skandali-tam-olarak-ne-oldu-ve-sirketler-neyle-suclaniyor), [Euronews 20.09](https://tr.euronews.com/2026/09/20/borsa-sorusturmasi-tera-ve-pusula-yoneticileri-gozaltina-alindi).
  - [Karar (7 hafta düşüş, BIST Genel Müdürü)](https://www.karar.com/ekonomi-haberleri/fon-skandalinin-faturasi-agirlasiyor-borsada-40-yil-sonra-bir-ilk-2081849).
  - [Sözcü fon rehberi 30.08](https://www.sozcu.com.tr/fonlarda-oyunun-kurallari-degisti-p353815), [BloombergHT uyum takvimi](https://www.bloomberght.com/spk-fon-rehberi-nde-uyum-takvimini-guncelledi-3792508).
  - [Türkiye'de İş Dünyası (blok satış)](https://turkiyedeisdunyasi.com/tasfiye-surecindeki-fonlardan-30-portfoy-icin-satis-esaslari-netlesti-145857/).
  - [Ekonomist şampiyon yöneticiler](https://www.ekonomist.com.tr/makale/sampiyon-fon-yoneticilerinden-2026-stratejileri-70123).
- **Pazarlama:**
  - [Tera Portföy X paylaşımı: TLY "1 ayda %61,36"](https://x.com/TeraPortfoy/status/1986799915041685618).
  - [BV Portföy BVZ sayfası](https://www.bvportfoy.com/tr/fon/tr-istatistiksel-arbitraj-serbest-fon-bvz).
- **Hukuk derlemesi (ikincil):** [Pega Hukuk kronoloji](https://pegahukuk.com/fon-krizi-nedir/).
