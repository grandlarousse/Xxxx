# r7 – Olay takvimi (2017-01-01 … 2026-12-31)

Hazırlanma: 2026-11-07/08. Amaç: F_XAUUSD (VİOP) için 1-3-5 günlük, uzlaşmadan uzlaşmaya lead-lag ve olay çalışmalarında kullanılacak olay takvimi.

Bütün dosyalar `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/data/events/` altında. UTF-8, başlıklı CSV. Kaynak listesi `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/data/events/KAYNAKLAR.md` dosyasında. Ham indirmeler `data/events/raw/` altında. Betikler `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/scripts_events/build_events.py` ve `/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/scripts_events/build_jeo.py`. İkisi de yeniden çalıştırılabilir.

**Not:** Bu turda web arama bütçesi (WebSearch) bitti. Doğrulamaları birincil sitelere doğrudan curl/WebFetch ile yaptım. CME sitesi 403/503 döndü, BLS curl'e 403 verdi (WebFetch ile okundu).

## 0. Zaman eşlemesi (VİOP uzlaşmasına göre)

VİOP günlük uzlaşma penceresi tam günde 18:00–18:10 TSİ = **15:00–15:10 UTC**, yarım günde 12:30–12:40 TSİ = **09:30–09:40 UTC** (r1 raporu; BIST prosedürü). Geçmiş yıllarda seans bitişinin farklı olup olmadığını doğrulamadım.

| Olay | Yerel saat | UTC (ABD yaz saati / kış) | Uzlaşmaya göre |
|---|---|---|---|
| ABD CPI, NFP | 08:30 ET | 12:30 / 13:30 | **Önce** (aynı gün uzlaşmasına girer). Yarım günde **sonra** |
| TCMB PPK (planlı) | 14:00 TSİ | 11:00 | Önce. Yarım günde sonra |
| FOMC (planlı) | 14:00 ET | 18:00 / 19:00 | **Sonra** (tepki ertesi VİOP gününe) |
| FOMC plansız 3.3.2020 | 10:00 EST | 15:00 | Uzlaşma penceresiyle çakışıyor |
| FOMC plansız 15.3.2020 (Pazar) | 17:00 EDT | 21:00 | Pazartesi'ye |

Türkiye yaz saati uygulamıyor. ABD saati değiştiğinde (Mart'ın 2. Pazarı, Kasım'ın 1. Pazarı) ABD verileri TSİ'de 1 saat kayıyor. 2017–2026'da CPI'ların 78'i 12:30, 41'i 13:30 UTC'de. NFP'lerin 76'sı 12:30, 43'ü 13:30 UTC'de.

## 1. fomc.csv (88 satır)

Sütunlar: tarih (açıklama günü), toplanti_gunleri, toplanti_tipi (planlı/plansız/notasyon oyu/iptal), karar_saati_et, karar_saati_utc, sep_var_mi, basin_toplantisi, faiz_karari, degisim_bps, hedef_alt, hedef_ust, viop_uzlasma_oncesi_mi, not, aciklama_url, takvim_url.

- **80 faiz kararı**: 19 artırım, 11 indirim, 50 sabit. Ayrıca 6 kararsız açıklama (11.10.2019 rezerv yönetimi; 2020'de 19, 23, 31 Mart notasyon oyları; 27.08.2020 ve 22.08.2025 strateji bildirimi revizyonları), 1 iptal toplantı (17-18 Mart 2020) ve 1 gelecek toplantı (8-9 Aralık 2026, SEP'li).
- Kaynak: Fed takvim sayfaları ve her toplantının bülteni. Saat, bültenin "For release at" satırından okundu. Faiz kararı "decided to raise/lower/maintain … target range" cümlesinden okundu.
- **Çapraz kontrol**: Fed'in "Open Market Operations" tablosundaki 30 değişikliğin 30'u eşleşti (tablo yürürlük tarihini, yani karar + 1 günü gösteriyor).
- 2026: Ocak, Mart, Nisan, Haziran ve Temmuz'da %3,50–3,75'te sabit kaldı. **16.09.2026'da +25 bps artırımla %3,75–4,00** oldu. 28.10.2026'da sabit kaldı (10–2 oy). 2026 Eylül artırımı Aralık 2025'ten sonraki ilk değişiklik, Temmuz 2023'ten sonraki ilk artırım.
- SEP'li toplantı: 39 (8-9 Aralık 2026 dahil; Mart 2020 SEP'i iptal toplantıyla birlikte yapılmadı). 2017–2018'de basın toplantısı sadece SEP'li toplantılarda var. 2019'dan itibaren her planlı toplantıda var.
- VİOP için: Planlı FOMC'lerin tamamı uzlaşmadan sonra açıklanıyor. Dört FOMC günü Türkiye'de tatile denk geliyor: 01.05.2019, 04.05.2022, 01.05.2024, 29.10.2025. Bu günlerde tepki bir sonraki VİOP gününe kayıyor.

## 2. us_cpi.csv ve 3. us_nfp.csv (120'şer satır)

Sütunlar: referans_ay, yayim_tarihi, yayim_saati_et, yayim_saati_utc, yaz_saati, hafta_gunu, durum, not, kaynak.

- Yayım tarihleri BLS arşiv sayfalarındaki dosya adlarından alındı (`cpi_MMDDYYYY.htm`, `empsit_MMDDYYYY.htm`). İleri tarihler BLS takviminden.
- **2025 kapanması**: Ekim 2025 CPI ve Ekim 2025 Employment Situation **yayımlanmadı** (BLS notu: "Not published because of 2025 lapse in federal government appropriations"). Eylül 2025 CPI 24.10.2025'te, Eylül NFP 20.11.2025'te, Kasım NFP 16.12.2025'te, Kasım CPI 18.12.2025'te yayımlandı.
- Ocak 2026: NFP 11.02.2026 (Çarşamba), CPI 13.02.2026 (Cuma). Normal takvim dışı. Nedenini birincil kaynakta görmedim.
- Kalan 2026 takvimi: CPI Ekim 2026 → **10.11.2026**, Kasım → **10.12.2026**. NFP Kasım 2026 → **04.12.2026**. Saat 08:30 ET = 13:30 UTC.
- **Kesişmeler**:
  - Kutsal Cuma'da NFP (NYSE ve COMEX kapalı, VİOP açık): 02.04.2021, 07.04.2023, 03.04.2026. Kutsal Cuma'da CPI: 14.04.2017, 10.04.2020.
  - VİOP kapalıyken NFP: 01.09.2017, 06.06.2025. VİOP kapalıyken CPI: 13.08.2019, 10.04.2024, 15.07.2025.
  - VİOP yarım günündeki veri: NFP 08.07.2022 ve CPI 12.05.2021. İkisinde de veri 12:30 UTC'de, yani uzlaşmadan **sonra** geldi.
- NFP Cuma dışı: 02.07.2020, 03.07.2025, 02.07.2026 (Perşembe, 4 Temmuz nedeniyle) ve üç olağan dışı tarih (20.11.2025 Perşembe, 16.12.2025 Salı, 11.02.2026 Çarşamba).

## 4. tcmb_ppk.csv (107 satır)

101 PPK kararı, 1 gelecek toplantı (10.12.2026) ve 5 PPK dışı bilgi satırı.

Sütunlar: tarih, toplanti_tipi, karar_saati_tsi, karar_saati_utc, etkin_faiz_tanimi, onceki_faiz, yeni_faiz, karar, degisim_bps, repo_1h, glp_borc_verme, koridor_degisimi, cerceve_notu, viop_uzlasma_oncesi_mi, kaynak.

- **Etkin faiz tanımı**: 1 Haziran 2018 öncesinde fiili fonlama Geç Likidite Penceresi (GLP) borç verme faiziyle yapılıyordu. 1 hafta repo %8'de sabitti. O dönemin kararları GLP'ye göre kodlandı:
  - 24.01.2017: %10 → %11 (+100). Aynı gün marjinal fonlama %8,5 → %9,25.
  - 16.03.2017: %11 → %11,75 (+75).
  - 26.04.2017: %11,75 → %12,25 (+50).
  - 14.12.2017: %12,25 → %12,75 (+50).
  - 25.04.2018: %12,75 → %13,5 (+75).
  - **23.05.2018 ara toplantı**: %13,5 → %16,5 (+300).
  - 1 Haziran 2018'den itibaren 1 hafta repo politika faizi oldu (%16,5).
- 101 kararın dağılımı: 22 artırım, 27 indirim, 52 sabit. 2018-06 sonrası 43 değişikliğin 43'ü TCMB'nin "1 Hafta Repo" tarihçe tablosuyla eşleşti.
- Plansız toplantılar: 23.05.2018, 20.03.2025. 20.03.2025'te politika faizi %42,5'te sabit kaldı, O/N borç verme %44 → %46 oldu. 17.03.2020 toplantısı 19 Mart'tan öne çekildi (duy2020-14). 2024'te 25 Temmuz ve 22 Ağustos toplantıları 23 Temmuz ve 20 Ağustos'a alındı (duy2024-34).
- Koridor ve çerçeve: 22.10.2020'de GLP ile O/N borç verme farkı 300 bps yapıldı. 21.03.2024'te O/N marjı ±300 bps, 26.12.2024'te ±150 bps oldu. 2025-04'ten itibaren O/N oranları duyuruda ayrıca yazılıyor.
- 2026: 22.01'de %38 → %37 (−100). 12.03, 22.04, 11.06, 23.07 ve 10.09'da sabit. 22.10'da %37 → %36 (−100). Aynı gün O/N borç verme %40 → %39, borçlanma %35,5 → %34,5.
- **PPK dışı, kritik**: TCMB **01.03.2026'da (Pazar) 1 hafta vadeli repo ihalelerine ara verdi** (duy2026-11). Aynı gün TL uzlaşmalı vadeli döviz satımını başlattı (duy2026-10). Fonlama fiilen O/N %40'tan yapıldı, yani politika %37 iken yaklaşık +300 bps fiili sıkılaşma oldu. İhaleler **23.08.2026'da (Pazar) yeniden başladı** (duy2026-35). 17.09.2026'da likidite gevşetme tedbirleri geldi (duy2026-41). F_XAUTRY bazı ve TL taşıma maliyeti çalışmalarında bu dönem ayrıca işaretlenmeli.
- **Karar saati**: TCMB sayfalarında saat yazmıyor. Planlı toplantılar için 14:00 TSİ = 11:00 UTC verildi. Ampirik dayanak: 101 PPK gününde Dukascopy USDTRY saatlik barlarında 11:00–12:00 UTC barının medyan |getirisi| 15,3 bps. Diğer saatlerde bu değer 3,1–9,3 bps arasında. Bu bar 101 günün 41'inde 06:00–15:00 UTC aralığının en büyük barı. 23.05.2018 ara kararında en büyük hareket 16:00–17:00 UTC'de (−511 bps; ~19:00–20:00 TSİ). 17.03.2020 ve 20.03.2025 için saat doğrulanamadı. Güven: orta.

## 5. tatiller.csv (516 satır)

Sütunlar: tarih, ulke_piyasa, tip (kapalı / yarım gün / kapalı (VİOP açık) / akşam seansı yok / akşam bülteni yok), aciklama, dogrulama, kaynak.

**Türkiye / VİOP**
- 2017-03-06 … 2026-11-06 arasında her hafta içi gün için Borsa İstanbul VİOP bülteninin varlığı kontrol edildi. Bülten olmayan (HTTP 404) **98 hafta içi gün** var. Hepsi resmi tatil (Kanun 2429 + bayramlar). XIST takvimiyle ters yönde uyumsuzluk yok.
- **21 yarım gün** var (bayram arifeleri ve 28 Ekim). 2020-01-17'den sonraki 16 yarım günün 16'sında akşam seansı bülteni yok. Bu, "yarım günde akşam seansı yapılmaz" kuralını veriyle doğruluyor. Yıl sonu son işlem günlerinde de akşam bülteni yok.
- Nedeni bilinmeyen, akşam bülteni olmayan üç tam gün: 24.07.2020, 04.08.2023, 29.11.2024.
- **8–14 Şubat 2023 (deprem)**: XIST takviminde Pay Piyasası kapalı, ama VİOP bültenleri var. Bu günler "kapalı (VİOP açık)" diye işaretlendi.
- Akşam seansı: r1 raporu doğruladı. Dolar/Ons Altın akşam seansına BIST duyurusu 12590 (18.09.2020) ile alındı. **Duyuru 30572 (19.11.2024) altına özgü değil, bakır vadelisiyle ilgili.** Ekindeki Prosedür md.7 tablosu ons altının akşam seansı listesinde olduğunu gösteriyor. Akşam seansı 19:00–23:00 TSİ = 16:00–20:00 UTC. Uzlaşmaya girmiyor.

**ABD (NYSE + COMEX)**: 96 kapanış ve 22 erken kapanış (13:00 ET). İçinde iki yas günü var: 05.12.2018 (G.H.W. Bush) ve 09.01.2025 (Carter). 2026 listesi NYSE sitesiyle birebir aynı. COMEX'in federal tatillerdeki kısaltılmış seans ve uzlaşma uygulamasını CME'den doğrulayamadım. Bu bilgi açıklama sütununda "doğrulanmadı" diye işaretli.

**Çin (SGE/SHFE, SSE takvimi)**: 181 kapanış. Çin Yeni Yılı her yıl 5–6 iş günü, Ekim Altın Haftası 5–6 iş günü. SHFE (Sina AU0) gün boşluklarıyla tek uyumsuzluk 22.04.2019 (veri boşluğu).

**Birleşik Krallık (LBMA fix yok)**: 83 banka tatili. 2022'de 2 Jübile günü ve Kraliçe'nin cenazesi, 2023'te taç giyme töreni var. gov.uk ile XLON 2019–2026'da tam uyumlu. VİOP vade sonu uzlaşması LBMA PM'e bağlı olduğu için bu günler vade haftasında önemli.

## 6. comex_altin_opsiyon_vade.csv (120 satır; opsiyon ayı 2017-02 … 2027-01)

Sütunlar: opsiyon_kontrat_ayi, og_son_islem_4_is_gunu, og_son_islem_cuma_tatil_kurali, kural_farki, gc_aktif_ay, gc_ilk_pozisyon_gunu, gc_ilk_ihbar_gunu, gc_son_islem_gunu, not, kaynak.

- Kural: Opsiyon kontrat ayından önceki ayın sondan 4. iş günü. Bu gün Cuma ya da tatil arifesiyse bir önceki iş günü.
- **CME'den doğrulayamadım** (rulebook ve fact card 403/503). Bu yüzden iki varyantı da verdim. 120 ayın 16'sında iki varyant farklı.
- Cuma kuralıyla son işlem günleri hiçbir zaman Cuma'ya düşmüyor: 50 Salı, 32 Perşembe, 22 Pazartesi, 16 Çarşamba.
- GC aktif aylar Şubat, Nisan, Haziran, Ağustos, Ekim ve Aralık. İlk ihbar günü önceki ayın son iş günü. İlk pozisyon günü bir gün öncesi. Son işlem teslim ayının sondan 3. iş günü.
- Örnek: 2026-12 opsiyonu 24.11.2026'da sona eriyor. GC Aralık 2026 ilk ihbar günü 30.11.2026.
- Önceki a3 çalışmasının OG tarihleriyle 120 ayın 120'si aynı. Bu bağımsız bir kaynak değil, aynı kuralın ikinci uygulaması.

## 7. jeopolitik.csv (59 satır)

Sütunlar: olay_tarihi, tepki_gunu, hafta_gunu, kategori, olay, gc_getiri_tepki_gunu_yuzde, gc_getiri_ertesi_gun_yuzde, gc_z_skoru, spot_15utc_getiri_yuzde, usdtry_15utc_getiri_yuzde, belirgin_altin_hareketi, kaynak.

- 59 olay var: 23 jeopolitik, 2 jeopolitik+Fed, 8 Türkiye, 6 Fed, 3 makro/Fed, 6 ticaret, 6 pandemi, 2 banka krizi, 1 siyaset, 2 piyasa şoku.
- Tepki günü: hafta sonu ya da ABD kapanışından sonra gelen olaylarda bir sonraki işlem günü.
- Getiriler bizim verimizden: GC=F kapanıştan kapanışa ve Dukascopy spot 15:00 UTC (VİOP uzlaşma anı). 2017+ GC günlük std = %1,078.
- 39 olayda XAUUSD tepki günü ya da ertesi gün |getiri| ≥ %1,5. 15 olayda tepki < %1,5. 5 Türkiye olayında XAUUSD tepkisi küçük ama USDTRY ≥ %1,5. Örnekler: 10.08.2018 +%14,8; 22.03.2021 +%9,0; 21.12.2021 (KKM) −%35,4 log; 19.03.2025 +%3,3.
- En büyük günlük GC hareketleri:
  - 30.01.2026 **−%11,41** (Warsh adaylığı)
  - 19.03.2026 −%6,12 (enerji altyapısı saldırıları + FOMC; WGC "reel faiz sıçramasına aşırı tepki" diyor)
  - 21.10.2025 −%5,91
  - 23.03.2020 +%5,44 (ertesi gün +%5,78)
  - 09.11.2020 −%5,11
  - 17.06.2021 −%4,76
- **Betimsel gözlem (test edilmedi, seçim yanlılığı var)**: 25 jeopolitik olayın 19'unda ilk tepki pozitif. Bunlarda ertesi gün ortalaması −%0,71. %58'inde ertesi gün negatif. Örnekler: 24.02.2022 +0,83 / −2,03; 08.03.2022 +2,35 / −2,73; 19.04.2024 +0,66 / −2,83; 02.03.2026 +1,21 / −3,60.

## 8. Eksik kalanlar ve güven

- Tam kapsam: FOMC, CPI, NFP ve PPK (2017–2026, gelecek tarihler planlı diye işaretli).
- Kısmi kapsam:
  - VİOP bülten taraması 2017-01-01…03-05 ve 2026-11-07…12-31 dönemlerini kapsamıyor (XIST'e dayanıyor).
  - 2017–2019 yarım günleri yalnız XIST'e dayanıyor.
  - COMEX tatil uygulaması ve OG kuralı CME'den doğrulanmadı.
  - SGE kendi duyurularından okunmadı.
  - LBMA'nın 24 ve 31 Aralık uygulaması dosyada yok.
- Jeopolitik liste seçimdir. Olay günleri fiyat verisine bakılarak da seçildi. Bu yüzden olay çalışmasında "seçim sonrası" yanlılık var. Test için olay tarihlerini fiyat verisinden bağımsız ölçütle seçin (ör. GPR endeksi sıçramaları; `data/misc/gpr_daily.xls`).
