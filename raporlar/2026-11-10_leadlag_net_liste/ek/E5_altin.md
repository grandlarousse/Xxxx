# E5_altin — çıkarım defteri (ham ajan çıktısı)

araç: 24/30

## Özet

Kök dizin: /tmp/claude-0/-home-user-Xxxx/de86f2d4-7ae4-5e17-8990-d3414798bf14/scratchpad/src (kaynak sütunlarında "xau/..." ve "altinpanel/..." bunun altındadır).

Genel hüküm: Altın külliyatında C0 düzenine teknik olarak uyan 13 kural var. Hiçbiri çoklu test düzeltmesi ve maliyetten sonra "kesin işe yarar" değil. VİOP'ta 2.621 birincil testin hiçbiri düzeltmeyi geçmiyor (en küçük q 0,29). Klasik "öncü yükseldi, hedef yükselmedi, hedefi al" (yetişme) kalıbı altında YOK: a5_yetisme_YOK, işaret ters, yani hareket sürüyor.

En sağlam iz ETF'te: altın 15:00 ET'ye kadar düştüyse GDXJ ertesi gün toparlıyor (E3-1; IC t −5,3; Bonferroni'yi geçen tek ilişki). Ama maliyet sonrası al-tut'a göre fazla getiri anlamsız (10 bps'te t 1,4; 20 bps'te 0,54).

(a) Kapanıştan ~10 dk önce hesaplanıp aynı kapanışta girilebilenler. Kesin: A4-C1 (t-1 ABD kapanışı), çeyrek sonu ve tatil öncesi GDX (takvim), C2j, C2, C1 (dünkü kapanış). E3-1 için 15:00 ET fiyatı yeterli; emir 15:50–15:58 ET (MOC yok). Yaklaşık: LOWMOM ve son saat (A8-3) 15:00 UTC spotuna bakar; 17:50 TSİ'de ön-izleme yaklaşıktır, eşiğe yakınsa 18:00–18:02'de yeniden bakılmalı. LOWMOM 2026'da hiç tetiklenmedi.

(b) "Madenci artığı": madencinin getirisinden GLD (ve SPY) betası çıkarılır. ETF'te yalnız uzun, 250 günlük yuvarlanan OLS, t-1 kapanışı. GDXJ artığı > ≈+%0,667 ise GDXJ al (3 gün); GDX 3 günlük artığı > ≈+%0,806 ise GDX al (3 gün); GDX 10 günlük artığı > ≈+%2,515 ise GLD al (5 gün). VİOP sürümünde yalnız GLD betası; z > 0,43 uzun, z < −0,43 kısa. Eşikler 2008–2017'de donduruldu. C1, C2, C2j aynı fenomen, tek sinyal sayın.

(c) Diğer öncüler: dolar, faiz, reel faiz, S&P, VIX, petrol, BTC, gümüş → altın: YOK (240 IC testinin %2,1'i |t|≥2; şans %4,6). Şanghay/Asya: Asya madenci artığı → GLD yalnız DÜŞÜK (HAKEM); Şanghay primi ve SHFE yok. Altın → gümüş: ayakta kalan kural yok. Altın → madenci: yalnız E3-1.

(d) TRALT ← altın: 04.11 rehberi hedge'li +35,5 bps (t 2,2), hedge'siz +25 (t 1,3) demişti. 10.11 denetimi bireysel maliyetle (23 bps) hedge'siz +11,5 (t 0,58), hedge'li +23,9 (t 1,41) buldu. Önceden konan ölçüt geçilmedi; 2021–23 üç yıl zarar; yıllık beklenti 20 bin USD'de +1.117, aralık −8.002…+10.395, zararlı yıl %42.

(e) Kaldıraçlı altın ETF'leri (NUGT, JNUG, UGL): kullanma. 2×GLD'ye göre yıllık −%6,9, NUGT −%20 aşınma; Midas'ta listelendiği teyit edilmedi.

## Sinyal defteri

### E3-1 altın gün içi düşüşü -> GDXJ ertesi gün toparlanır

- **sinif:** ABD-ETF
- **tur:** leadlag
- **oncu:** TVC:GOLD (ya da OANDA:XAUUSD; çalışma Dukascopy spot altın kullandı)
- **hedef:** AMEX:GDXJ
- **kural:** m = ln(spot altın 15:00 ET bugün / spot altın 16:00 ET dün). m < 0 ise GDXJ'yi bugünkü kapanışta (16:00 ET) al, ertesi kapanışta sat (koşul sürerse koru); m >= 0 nakit. Yalnız uzun. ABD yarım günlerinde yeni pozisyon yok. Karar anı 15:00 ET.
- **sinyal_saati:** 15:00 ET (kışın 23:00 TSİ); emir 15:50-15:58 ET (23:50-23:58 TSİ)
- **giris_orijinal:** aynı kapanış (t 16:00 ET)
- **c0_uyumu:** evet
- **c0_notu:** Girdi 15:00 ET'de bilinir; kapanıştan kapanışa; Midas'ta yalnız uzun yeterli. MOC yok, emir 15:50-15:58 ET. Küçük hesapta komisyon kenarı yer (~3.000 USD altı).
- **tutma:** 1 gün (koşul sürerse uzar)
- **yon:** UZUN (yalnız; kısa bölge nakit)
- **n:** n verilmedi; yılda ~66 gidiş-dönüş
- **net_bp:** brüt +18,0 bps/aktif gün (OOS 20,8); yıllık net %19,9 (1x, beta dahil); net bps/işlem verilmedi
- **t:** IC t -5,3 (m ile madenci ters yön); Bonferroni p 0,0002; alan içi q 0,0001
- **is_oos:** t IS -4,80 / OOS -2,77; OOS net Sharpe 0,72 (10 bps) ve 0,51 (20 bps) vs B&H 0,54
- **son_donem:** 2022+ Sharpe 0,79 vs B&H 0,71; 2026 Sharpe 0,47. Zayıflatan: maliyet sonrası B&H'ye göre OOS alfa %10,6, t 1,41 (10 bps), t 0,54 (20 bps); etki 2013-17'de yoğun; GDX'te 2008 -%48,7; doğrusal etki zayıf; yılda ~66 gidiş-dönüş.
- **maliyet:** 10 bps gidiş-dönüş (stres 20); Midas 1,5 USD/emir + açıklanmamış TL-USD makası
- **hukum:** ORTA (HAKEM son etiket; analist YÜKSEK demişti). İstatistik gerçek, maliyet sonrası net alfa anlamsız.
- **guven:** ORTA
- **kaynak:** xau/raporlar/2026-11-07_xauusd_altin/RAPOR.md §5.2 satır 287; sentez/HAKEM.md §1.3 (satır 111-113) ve §2.1 (satır 184); analiz/e2_etf_leadlag.md §3b
- **alinti:** m < 0 ise GDXJ'yi kapanışta al, ertesi kapanışta sat (koşul sürerse koru)

### A4-C1 GDXJ artığı -> VİOP ons altın

- **sinif:** Altin-VIOP
- **tur:** leadlag
- **oncu:** AMEX:GDXJ ve AMEX:GLD (t-1 ABD kapanışı)
- **hedef:** BIST:XAUUSD1! (F_XAUUSD, uzlaşma fiyatı)
- **kural:** e = r_GDXJ - β60·r_GLD (t-2'den t-1'e ABD kapanışı, log adjclose; β önceki 60 gün cov/var). z = e / std(e, önceki 120 gün). z > +0,43 UZUN, z < -0,43 KISA; her gün sermayenin 1/3'ü ile yeni dilim, 3 gün kademeli. Giriş t uzlaşmasında.
- **sinyal_saati:** t-1 16:00 ET ABD kapanışı (VİOP girişinden 18-19 saat önce bilinir)
- **giris_orijinal:** aynı uzlaşma (t, 18:00-18:10 TSİ penceresi)
- **c0_uyumu:** evet
- **c0_notu:** Girdi dünkü ABD kapanışı, giriş 18:00-18:10 TSİ uzlaşma penceresi; emir pencereye yayılmalı. Midas'ta F_XAUUSD yok.
- **tutma:** 3 gün kademeli
- **yon:** UZUN ve KISA
- **n:** n verilmedi; yılda ~34 gidiş-dönüş
- **net_bp:** brüt +12,1 bps/aktif gün (OOS 16,9); yıllık net %3,9 (1x nominal)
- **t:** IC t 3,53; kural P&L t 1,64 (IS 0,53)
- **is_oos:** IC t IS 2,53 / OOS 2,63; OOS net Sharpe 0,72 (B&H 0,62); 10 bps'te OOS 0,53, IS -0,04
- **son_donem:** 2022+ 0,71; 2026 0,39; 2025-26 IC t 0,86; 2010-16 spotta IC 0,016 (t 0,63); Pearson IS t 0,74; ABD takvimiyle kurunca OOS 0,52; q 0,29 (HAKEM), global q 0,43 (a4), aile içi q 0,013; kısa bacak OOS Sharpe 0,09.
- **maliyet:** 5 bps gidiş-dönüş (stres 10); pazarlıklı komisyon varsayımı. Varsayılan perakende tarife 22-25 bps bunu zarara çevirir.
- **hukum:** DÜŞÜK; çoklu test düzeltmesini geçmiyor, ayakta kalan 4 VİOP kuralından biri (küçük sepet/filtre)
- **guven:** DÜŞÜK
- **kaynak:** xau/raporlar/2026-11-07_xauusd_altin/RAPOR.md §4.3 satır 238; sentez/HAKEM.md §2.1 satır 178; analiz/a4_abd_capraz.md §0 madde 5 ve §5 C1 (satır 158-205)
- **alinti:** GDXJ'nin GLD'ye göre 1 günlük beta-artığı (t-1 ABD kapanışları) VİOP 3 günlük getirisini öngörüyor

### E2-C2j GDXJ'nin kendi artığı sürer (3 gün)

- **sinif:** ABD-ETF
- **tur:** goreli-momentum
- **oncu:** AMEX:GDXJ'nin AMEX:GLD ve AMEX:SPY'ye göre artığı
- **hedef:** AMEX:GDXJ
- **kural:** e = r_GDXJ - b_GLD·r_GLD - b_SPY·r_SPY (250 günlük yuvarlanan OLS, beta t-1'de; getiriler t-2'den t-1 kapanışa). e(t-1) > IS (2008-17) %70 kantili (≈ +%0,667) ise t kapanışında GDXJ al, 3 gün kademeli; aksi nakit. Yalnız uzun (JDST'li ters sürüm kullanılmaz).
- **sinyal_saati:** t-1 16:00 ET kapanışı (~23 saat önce); emir t 15:50-15:58 ET
- **giris_orijinal:** aynı kapanış (t 16:00 ET); sinyal dünkü kapanıştan
- **c0_uyumu:** evet
- **c0_notu:** Zamanlama uygun, ama kuralın şekli 'hedef kendi artığıyla sürer'; 'öncü yükseldi, hedef yükselmedi' yetişmesi değil. 3 gün kademeli. Mevcut durumda (09.11) sinyal AKTİF uzun (e=+%3,67) ama 2026'da zayıf.
- **tutma:** 3 gün kademeli (her gün 1/3)
- **yon:** UZUN (yalnız)
- **n:** n verilmedi; yılda ~17 gidiş-dönüş
- **net_bp:** brüt +48,5 bps/aktif gün (OOS 53,1); yıllık net %13,1 (1x, beta dahil)
- **t:** IC t 3,47 (tam); alfa t 3,3
- **is_oos:** t IS 1,90 / OOS 3,04; OOS Sharpe 0,81 basit (0,64 log) vs B&H 0,54 (0,31 log); stres 0,70
- **son_donem:** 2022+ 0,90 vs B&H 0,71; 2026 Sharpe 0,21; 2025-26 IC 0,028 (t 0,6); geniş ızgarada dürüst IS seçimi OOS'u ≈0'a indiriyor; Bonferroni'de elenir; q 0,056; OOS alfa %6,8 (t 1,95).
- **maliyet:** 10 bps (stres 20) gidiş-dönüş
- **hukum:** ORTA (HAKEM; analist YÜKSEK demişti). A4-C1 ile aynı fenomen (sıra korelasyonu 0,87).
- **guven:** ORTA
- **kaynak:** xau/raporlar/2026-11-07_xauusd_altin/RAPOR.md §5.2 satır 288; sentez/HAKEM.md §2.1 satır 181; analiz/e2_etf_leadlag.md §3a, §4, §5; sinyal/KULLANIM.md §4 satır 106
- **alinti:** GDXJ artığı (GLD+SPY, 250g OLS) > +%0,667 ise GDXJ

### E2-C1 madenciler altına öncü: GDX 10 günlük artığı -> GLD

- **sinif:** ABD-ETF
- **tur:** leadlag
- **oncu:** AMEX:GDX (artık: GLD ve SPY'ye göre)
- **hedef:** AMEX:GLD
- **kural:** GDX'in GLD+SPY'ye göre 10 günlük artık toplamı (t-1'de biter) > IS %80 kantili (≈ +%2,515) ise GLD uzun, 5 gün kademeli; aksi nakit. Kaplama sürümü: GLD tutuyorsan artık < %20 kantil (≈ -%4,02) olan günün 1/5 dilimi nakde geç, öbür günler GLD.
- **sinyal_saati:** t-1 16:00 ET kapanışı
- **giris_orijinal:** aynı kapanış (t 16:00 ET)
- **c0_uyumu:** kismen
- **c0_notu:** Girdi/giriş zamanı uygun ama tutuş 5 gün (1-3 günü aşıyor). En pratik kullanım GLD tutanlar için risk filtresi (kaplama).
- **tutma:** 5 gün kademeli
- **yon:** UZUN (yalnız)
- **n:** n verilmedi; yılda ~5,6 gidiş-dönüş
- **net_bp:** brüt +58,4 bps/aktif dilim (OOS 55,3); yıllık net %5,4 (1x)
- **t:** IC t 3,93; alfa t 2,8; alan içi q 0,019
- **is_oos:** t IS 3,46 / OOS 1,94 (2022+ 2,63); OOS Sharpe 0,78 basit vs B&H 0,81; kaplama OOS 0,90 vs 0,72 (maks. düşüş -%22,8 vs -%33,2)
- **son_donem:** 2022+ 0,84 vs B&H 0,95; 2026 Sharpe 1,16; 2018-24 IC ≈0 (2018-21 -0,017; 2022-24 0,026); yalnız uzun sürüm B&H'yi geçmiyor; kaplamanın üstünlüğü 2026 Oca-Şub çöküşüne dayanıyor; OOS alfa %2,2 (t 1,3). Literatür tersini söylüyor (altın madencilere öncü).
- **maliyet:** 10 bps (stres 20)
- **hukum:** ORTA (HAKEM); alfa zayıf, yüksek oynaklık rejimlerinde çalışıyor (2008, 2013-17, 2025-26)
- **guven:** ORTA
- **kaynak:** xau/raporlar/2026-11-07_xauusd_altin/RAPOR.md §5.2 satır 290; sentez/HAKEM.md §2.1 satır 183; analiz/e2_etf_leadlag.md §3a, §4 (kaplama tablosu)
- **alinti:** GDX 10g artığı > +%2,515 ise GLD

### E2-C2 GDX'in 3 günlük artığı sürer

- **sinif:** ABD-ETF
- **tur:** goreli-momentum
- **oncu:** AMEX:GDX'in AMEX:GLD ve AMEX:SPY'ye göre 3 günlük artığı
- **hedef:** AMEX:GDX
- **kural:** GDX'in GLD+SPY'ye göre 3 günlük artık toplamı (t-1'de biter) > IS %70 kantili (≈ +%0,806) ise GDX uzun 3 gün (kademeli); aksi nakit.
- **sinyal_saati:** t-1 16:00 ET kapanışı
- **giris_orijinal:** aynı kapanış (t 16:00 ET)
- **c0_uyumu:** evet
- **c0_notu:** Zamanlama uygun; kural 'hedef kendi artığıyla sürer' biçimi. C2j ile birlikte tek fenomen say.
- **tutma:** 3 gün kademeli
- **yon:** UZUN (yalnız)
- **n:** n verilmedi; yılda ~17,5 gidiş-dönüş
- **net_bp:** brüt +38,1 bps/aktif dilim (OOS 44,3); yıllık net %10,5 (1x, beta dahil)
- **t:** IC t 3,29; alfa t 2,2; q 0,069
- **is_oos:** t IS 2,24 / OOS 2,34; OOS Sharpe 0,71 basit (0,58 log) vs B&H 0,60 (0,41 log)
- **son_donem:** 2022+ 0,69 vs B&H 0,77 (HAKEM, basit; e2'de log 0,58 vs 0,57); 2026 Sharpe 0,23; OOS alfa %5,3 (t 1,3); ızgara IS medyanı ≈0; 20 bps'te marjinal; C2j ile aynı fenomen.
- **maliyet:** 10 bps (stres 20)
- **hukum:** ORTA (HAKEM; e2 analisti bilerek bir kademe indirmişti); 2022+ al-tut'u geçmiyor
- **guven:** ORTA
- **kaynak:** xau/raporlar/2026-11-07_xauusd_altin/RAPOR.md §5.2 satır 289; sentez/HAKEM.md §2.1 satır 182; analiz/e2_etf_leadlag.md §5 satır 278
- **alinti:** GDX 3g artığı > +%0,806 ise GDX

### E1-C2 tatil öncesi GDX

- **sinif:** ABD-ETF
- **tur:** takvim
- **oncu:** yok (takvim: NYSE tatili)
- **hedef:** AMEX:GDX
- **kural:** NYSE tatilinden önceki son işlem gününden bir önceki kapanışta GDX al, tatil öncesi günün kapanışında sat. Yalnız uzun.
- **sinyal_saati:** takvim (önceden bilinir)
- **giris_orijinal:** aynı kapanış
- **c0_uyumu:** evet
- **c0_notu:** Takvim kuralı, lead-lag değil. Sinyal önceden bilinir; MOC yok, 15:50-15:58 ET emri.
- **tutma:** 1 gün
- **yon:** UZUN
- **n:** yılda ~9 işlem (olay sayısı verilmedi)
- **net_bp:** brüt +47,3 bps/olay (diğer günler -0,2); yıllık net %3,6 (1x); alfa %3,3 (t 2,3)
- **t:** IS t 1,71
- **is_oos:** t IS 1,71 / OOS 2,45; OOS Sharpe 0,75 (10 bps) vs B&H 0,60
- **son_donem:** 2022+ 0,79 vs 0,77; 2026 Sharpe 0,36; global q 0,52 (alan içi 0,126); aynı gün GLD+SPY kontrolüyle 20 bps (t 2,0); ortalamanın 2/3'ü en iyi 10 günden; 1983-2007 madenci sepetinde 35 bps (t 2,16) kısmi teyit. Sonraki giriş 24.11.2026 kapanışı.
- **maliyet:** 10 bps (stres 20)
- **hukum:** ORTA (HAKEM); tek başına zayıf IS kanıtı, küçük kenar
- **guven:** ORTA
- **kaynak:** xau/raporlar/2026-11-07_xauusd_altin/RAPOR.md §5.2 satır 291; sentez/HAKEM.md §2.1 satır 180 ve §2.2 satır 245
- **alinti:** NYSE tatilinden önceki son işlem gününden bir önceki kapanışta GDX al

### TRALT <- altının o günkü hareketi (R1, hedge'siz) [04.11 rehberi kuralı, 10.11 denetimi]

- **sinif:** BIST-VIOP
- **tur:** leadlag
- **oncu:** TVC:GOLD (17:55'ten dünkü 17:55'e); testte aynı gün F_XAUUSD uzlaşma getirisi (BIST:XAUUSD1!)
- **hedef:** TRALT1! (BIST VİOP pay vadelisi, panel kodu; borsa öneki dosyada yazılı değil)
- **kural:** g = altının günlük getirisi, z = g/σ250 (1 gün gecikmeli). |z| > 1 (≈ ±%1,7-1,8) ise aynı yönde gir (z>1 TRALT uzun, z<-1 kısa), 2 gün sonra çık (k=2, örtüşmesiz). Kilit/limit günlerinde giriş yok, kilitli çıkış en çok 3 gün ertelenir. Hedge'siz.
- **sinyal_saati:** 17:55 TSİ
- **giris_orijinal:** aynı kapanış/uzlaşma (VİOP 18:00-18:10)
- **c0_uyumu:** kismen
- **c0_notu:** Saat uygun (17:55, aynı uzlaşma), ama sinyal uzlaşma getirisinden ölçüldü; 17:55 ölçümüne geçince önceki çalışmada işlem başı 4-13 bps gidiyordu, dolum-uzlaşma farkı ölçülmedi. Sinyali 17:55'ten 17:55'e ölç.
- **tutma:** 2 gün
- **yon:** UZUN ve KISA (bireysel net uzun +11,1 / kısa +12,1 bps)
- **n:** 408 (≈52,4/yıl)
- **net_bp:** brüt 34,5; net düşük maliyet 26,5; net bireysel maliyet 11,5 bps/işlem
- **t:** t 1,34 (düşük maliyet); 0,58 (bireysel)
- **is_oos:** IS/OOS ayrımı yok; dönemler (bireysel net): 2019-20 +52,6 / 2021-23 -66,5 / 2024-26 +49,9 bps/işlem
- **son_donem:** 2021-23 üç yıl zarar (toplam -9.117 bps); en iyi %2 işlem (9) çıkınca -12,7; 2026 toplam +6.542 bps; 05.11 sonrası gerçek işlem 0. Bootstrap (20 bin USD, yıllık): ort +1.117, %5-%95 -8.002...+10.395, zararlı yıl %42. Bağımsız hesap V1: brüt 33,3, bireysel net 10,3 (t 0,53). 04.11 rehberi: hedge'siz +25 bps (t 1,3).
- **maliyet:** TRALT gidiş-dönüş bireysel varsayım 23 bps (muhtemelen üst sınır), düşük 8 bps; fiyat kayması eklenmedi
- **hukum:** Önceden konan 'kazandırır' ölçütünü geçmedi (bireysel maliyetle t>=2, en iyi %2 hariç pozitif); beklenti sıfırdan ayırt edilemiyor. Hedge'siz ve bireysel maliyetle güven DÜŞÜK.
- **guven:** DÜŞÜK
- **kaynak:** altinpanel/raporlar/2026-11-10_altin_panel_denetimi/RAPOR.md §Kısa yanıt ve §3 (satır 93-117); ek/K2_strateji_beklentisi.md satır 19-29 ve 43-58; ek/V1_bagimsiz_hesap.md satır 9-20; ek/00_yontem.md satır 9
- **alinti:** beklenen kazanç sıfır dolayında; işareti veriden bilinemiyor

### TRALT - β·XU030 (hedge'li; 04.11 rehberinin ana kuralı)

- **sinif:** BIST-VIOP
- **tur:** leadlag
- **oncu:** TVC:GOLD (aynı gün altın z > ±1)
- **hedef:** TRALT1! uzun/kısa + XU030D1! karşı bacak (β ≈ TRALT'ın piyasa betası ~1,25 olarak anılıyor)
- **kural:** R1 ile aynı sinyal (altın z > ±1, 2 gün); TRALT pozisyonu β·XU030 vadelisiyle hedge edilir. 20 bin USD TRALT için ≈8 F_XU030 kontratı.
- **sinyal_saati:** 17:55 TSİ
- **giris_orijinal:** aynı kapanış/uzlaşma
- **c0_uyumu:** kismen
- **c0_notu:** Zaman uygun ama üçüncü araç (XU030), ek teminat ve maliyet. Kullanıcının tek-bacak düzenine tam uymuyor; hedge kazanç için değil risk için (işlem başı oynaklık 401'den 342 bps'e).
- **tutma:** 2 gün
- **yon:** UZUN ve KISA
- **n:** 408
- **net_bp:** brüt 53,7; net düşük maliyet +43,2; net bireysel +23,9 bps/işlem (04.11 rehberi: +35,5)
- **t:** t 2,55 (düşük maliyet); 1,41 (bireysel)
- **is_oos:** dönemler (bireysel): 2019-20 +48,1 / 2021-23 -33,5 / 2024-26 +56,3
- **son_donem:** En iyi %2 işlem çıkınca +2,8 (R1 -12,7). Hedge'li sürümün fazladan 19,2 bps'i XU030 bacağının kendi kazancından (t 1,67; çoğu 2021-23). Düşük maliyetli net, bu sıfırlanınca +24 (t 1,42). Eylül-Ekim 2026 fon krizinde 7 işlem ort. -82 bps. Yıllık (20 bin USD): ort +2.463, %5-%95 -4.879...+10.548, zararlı yıl %34. Rehber sayısı yeniden üretildi: n 408, +43 bps, t 2,55 (V1: +42,6).
- **maliyet:** TRALT 23 bps + XU030 bacağı β×8 bps (bireysel); düşük TRALT 8
- **hukum:** Kaldı (bireysel maliyetle t<2); hedge yalnız riski düşürür, kazanç katkısı kanıtsız
- **guven:** DÜŞÜK
- **kaynak:** altinpanel/raporlar/2026-11-10_altin_panel_denetimi/RAPOR.md §3 (satır 99-120); ek/K2_strateji_beklentisi.md satır 27 ve 56; ek/V1_bagimsiz_hesap.md satır 11; ek/00_yontem.md satır 9
- **alinti:** Hedge'in kalıcı faydası oynaklığı düşürmesi.

### E2-C5 Asya madenci artığı -> GLD

- **sinif:** ABD-ETF
- **tur:** leadlag
- **oncu:** Zijin 2899.HK, Zhaojin 1818.HK, Shandong 600547.SS (Yahoo kodları; TradingView kodu dosyada yok)
- **hedef:** AMEX:GLD
- **kural:** Gün t Asya madenci artığı (aynı penceredeki altın 07 UTC ve yerel endekse göre) > IS q0,7 ise GLD uzun 3 gün. Bilgi t 07:00-08:10 UTC (10:00-11:10 TSİ).
- **sinyal_saati:** t 07:00-08:10 UTC, kapanıştan 11-12 saat önce
- **giris_orijinal:** aynı kapanış (t 16:00 ET)
- **c0_uyumu:** evet
- **c0_notu:** Bilgi gün içi erken bilinir; C1 için bağımsız teyit değerinde, tek başına zayıf.
- **tutma:** 3 gün
- **yon:** UZUN (yalnız)
- **n:** n verilmedi; yılda ~35 gidiş-dönüş
- **net_bp:** net bps verilmedi
- **t:** IC t 3,29
- **is_oos:** t IS 2,08 / OOS 2,48; yalnız uzun OOS Sharpe 0,84 vs B&H 0,72
- **son_donem:** 2022+ 1,29 vs 0,85 (yalnız uzun); 12/19 yıl (<%70); stres maliyette ideal OOS 0,06; ızgara IS medyanı 0,09; 2018-21 IC 0; 20 bps'te B&H altında; takvim hizasına duyarlı. Kısmi testte Asya t 1,95, ABD artığı t 2,54.
- **maliyet:** 10 bps (stres 20)
- **hukum:** DÜŞÜK (HAKEM SON; analist ORTA demişti); izleme/teyit sinyali
- **guven:** DÜŞÜK
- **kaynak:** xau/raporlar/2026-11-07_xauusd_altin/sentez/HAKEM.md §2.2 satır 253; analiz/e2_etf_leadlag.md §3a satır 109, §4 ve §5 satır 280
- **alinti:** Asya'da tekrar (s7). Zijin (2899.HK), Zhaojin (1818.HK) ve Shandong (600547.SS)

### A8-3 son saat momentumu

- **sinif:** Altin-VIOP
- **tur:** mikroyapi
- **oncu:** yok (kendi sinyali: OANDA:XAUUSD 1 saatlik grafik, 17:00-18:00 TSİ mumu)
- **hedef:** BIST:XAUUSD1!
- **kural:** pos = sign(ln(spot 15:00 UTC / spot 14:00 UTC)); t uzlaşmasında gir, 5 gün kademeli; TR yarım günleri hariç; spot kapalı VİOP günlerinde yeni dilim 0.
- **sinyal_saati:** t 15:00 UTC = 18:00 TSİ
- **giris_orijinal:** aynı uzlaşma
- **c0_uyumu:** kismen
- **c0_notu:** Saatlik mum 18:00'de tamamlanır; kapanıştan 10 dk önce bakınca ön-izleme yaklaşık (GC=F bazlı), tutuş 5 gün.
- **tutma:** 5 gün kademeli
- **yon:** UZUN ve KISA
- **n:** n verilmedi; yılda ~25 gidiş-dönüş
- **net_bp:** brüt +10,3 bps/aktif gün (OOS 13,7); yıllık net %3,9 (1x)
- **t:** alfa t 1,5; IS IC t 1,32
- **is_oos:** t IS 1,32 / OOS 2,05; OOS Sharpe 0,66 vs B&H 0,62
- **son_donem:** 2024 Sharpe -2,31; 2026 Sharpe 1,93 (kazanç 2026'ya yığılı); 2010-16'da h1-h3'te yok; kısa bacak her dönemde zarar; 309 testten seçildi; q 0,50.
- **maliyet:** 5 bps (stres 10)
- **hukum:** DÜŞÜK
- **guven:** DÜŞÜK
- **kaynak:** xau/raporlar/2026-11-07_xauusd_altin/RAPOR.md §4.3 satır 239; sentez/HAKEM.md §2.1 satır 179; sinyal/KULLANIM.md §6 satır 163
- **alinti:** sign(ln(spot 15:00 / spot 14:00 UTC)) yönünde gir, 5 gün kademeli

### A1-LOWMOM sakin piyasa momentumu

- **sinif:** Altin-VIOP
- **tur:** kendi-sinyali
- **oncu:** yok (kendi sinyali: OANDA:XAUUSD spot 15:00 UTC, 5 günlük getiri ve 20 günlük oynaklık)
- **hedef:** BIST:XAUUSD1!
- **kural:** P = spot XAUUSD 15:00 UTC; x = ln(P_t/P_t-5); rv20 = son 20 günlük günlük log getiri std; q = rv20'nin 2010'dan beri genişleyen yüzdeliği. q < 1/3 (≈ yıllık %11,7) ise sign(x) yönünde 1 birim aç, ertesi uzlaşmada kapat; aksi nakit. Varyant h5 (5 gün kademeli).
- **sinyal_saati:** t 15:00 UTC = 18:00 TSİ
- **giris_orijinal:** aynı uzlaşma
- **c0_uyumu:** evet
- **c0_notu:** Ön-izleme yaklaşık; eşiğe yakınsa 18:00-18:02'de yeniden. Şu an yapısal olarak pasif.
- **tutma:** 1 gün (h5 varyantı 5 gün)
- **yon:** UZUN ve KISA
- **n:** n verilmedi; yılda ~22 gidiş-dönüş
- **net_bp:** brüt +8,1 bps/aktif gün (OOS 14,9); yıllık net %7,2 (1x); alfa %7,1 (t 2,9)
- **t:** IS t 2,38
- **is_oos:** t IS 2,38 / OOS 2,68; OOS Sharpe 1,35 (dm 1,31) vs B&H 0,62
- **son_donem:** 2026'da hiç tetiklenmedi (rv20 %21 vs eşik %11,7); 2017-19'da etki yok; ızgara tepesi (280 komşunun 99. yüzdeliği, medyan ≈0,4); en iyi 20 gün PnL'in %66-75'i; q 0,33. h5 varyantı IS t 0,64.
- **maliyet:** 5 bps (stres 10)
- **hukum:** DÜŞÜK; kendi sinyali (rejim momentumu), lead-lag değil
- **guven:** DÜŞÜK
- **kaynak:** xau/raporlar/2026-11-07_xauusd_altin/RAPOR.md §4.3 satır 236; sentez/HAKEM.md §2.1 satır 175-176
- **alinti:** q<1/3 (≈yıllık %11,7) ise 5 günlük spot getirisinin işaretinde 1 birim

### A3_QEND çeyrek sonu

- **sinif:** Altin-VIOP
- **tur:** takvim
- **oncu:** yok (takvim)
- **hedef:** BIST:XAUUSD1! (aktif vade)
- **kural:** Mar/Haz/Eyl/Ara'nın sondan 2. VİOP işlem günü uzlaşmasında UZUN gir, 3 VİOP günü sonra (yeni çeyreğin 2. günü) kapat; diğer günler nakit.
- **sinyal_saati:** takvim
- **giris_orijinal:** aynı uzlaşma
- **c0_uyumu:** evet
- **c0_notu:** Takvim kuralı, lead-lag değil; çok düşük devir.
- **tutma:** 3 gün
- **yon:** UZUN
- **n:** 39 olay (yılda 4)
- **net_bp:** brüt +76,7 bps/olay (diğer günler +8,3); yıllık net %1,0 (maruziyet %1,6)
- **t:** alfa t 2,75; BH q 0,06
- **is_oos:** t IS 2,13 / OOS 2,26; OOS Sharpe 1,00 vs B&H 0,62
- **son_donem:** 2026 Sharpe 1,21; 2017-19 ve 2022-23 ≈0; Mar/Haz/Eyl 2010-16'da yok (t 0,61); mekanizma belirsiz; q 0,33 (HAKEM). Sonraki giriş 30.12.2026 (0227 kontratında).
- **maliyet:** 5 bps
- **hukum:** DÜŞÜK
- **guven:** DÜŞÜK
- **kaynak:** xau/raporlar/2026-11-07_xauusd_altin/RAPOR.md §4.3 satır 237; sentez/HAKEM.md §2.1 satır 177
- **alinti:** Mar/Haz/Eyl/Ara'nın sondan 2. VİOP günü UZUN

### UST2 5 günlük değişim -> GLD ertesi gün (DXY/faiz grubundan tek IS-OOS aynı işaretli iz)

- **sinif:** ABD-ETF
- **tur:** leadlag
- **oncu:** ABD 2 yıllık faiz 5 günlük değişimi (TradingView kodu dosyada yok)
- **hedef:** AMEX:GLD
- **kural:** UST2'nin 5 günlük değişimi -> GLD h1 (ters yön; IC -0,044). Eşik ve tam kural metni okunan kısımda verilmedi.
- **sinyal_saati:** t-1 22:00 UTC
- **giris_orijinal:** aynı kapanış
- **c0_uyumu:** evet
- **c0_notu:** Girdi önceki gün bilinir; ancak kural olarak test edilip ayakta bırakılmadı.
- **tutma:** 1 gün
- **yon:** UZUN/nakit (işaret negatif: faiz yükselince GLD düşük)
- **t:** t -2,92
- **is_oos:** t IS -2,16 / OOS -2,10
- **son_donem:** Ekonomik büyüklük küçük; 504 testten 19'u |t|>=2, IS ve OOS'ta aynı işaretli tek test bu.
- **maliyet:** 10 bps (e2 varsayımı)
- **hukum:** DÜŞÜK
- **guven:** DÜŞÜK
- **kaynak:** xau/raporlar/2026-11-07_xauusd_altin/analiz/e2_etf_leadlag.md §3c satır 126 ve §5 satır 283
- **alinti:** UST2 5 günlük değişim → GLD h1, t −2,92 (IS −2,16, OOS −2,10, IC −0,044)

## Elenenler

- **Ons altın vadelisi <- panel girdileri (GLD, PHYS, COMEX GC, GDX, GDXJ, TRMET, USDTRY, bant) 1-3 gün:** 66 testte 0 geçen; altının o günkü hareketi kendi sonraki 2 gününü öngörmüyor (-0,6 bps, t -0,13). 1.800+ gün, hüküm sağlam. _( altinpanel/.../RAPOR.md §2; ek/K1_panel_testleri.md satır 5-8, 32 )_
- **R2: TRALT - b·ons altın:** Bireysel maliyetle +2,6 bps, t 0,13; bacaklar akşam seansında eşleşmiyor (ons açık, TRALT kapalı). Yıllık zarar olasılığı %50. _( ek/K2_strateji_beklentisi.md satır 22, 51 )_
- **R3a ons altın 'altını izle' / R3b tersine gir:** R3a net -1,8 bps (t -0,23); R3b net -18,2 bps (t -2,35); brüt 8,2 bps maliyeti karşılamıyor. _( ek/K2_strateji_beklentisi.md satır 23-24 )_
- **eGDXJ (GDXJ'nin GDX'e göre artığı) -> TRALT, k=3:** V1: kırılgan, muhtemelen sahte. ≥2022 t 1,5; ilgisiz XU030 hedefinde aynı sinyal t 4,02; d*-1 plaseboda sönmüyor; 19x3x3 testten Bonferroni geçmez. Bireysel net +47 bps (t 1,47), en iyi %2 hariç +12. _( ek/V1_bagimsiz_hesap.md satır 22-43; ek/K1_panel_testleri.md satır 5, 26, 44-49 )_
- **GDX / GDXJ / GLD / PHYS son ABD seansı -> TRALT (+26,3 t 2,34; +32,6 t 2,47; +14,5; +15,1):** FDR eşiğini geçmedi (q 0,12>0,10). ABD seansı BIST'ten sonra kapanıyor; öncülük ertesi sabah açılış boşluğunda fiyatlanıyor, kapanıştan kapanışa kullanılamaz. Ayrıca ekrandaki % farklı saatlerden ölçülüyor. _( altinpanel/.../RAPOR.md §2 ve §5 )_
- **TRALT 'bağ güçlüyken işlem yap' süzgeci (120g korelasyon > 0,20) ve 'son 20 işlem kârdaysa devam' süzgeci:** 2021-23'te süzgecin açık dediği 50 işlem ort. -135 bps; pencereye göre t 0,5-2,2; 'son 20 işlem' süzgeci tersine çalışıyor. Rejim süzgeci tek kodla yapıldı, doğrulanmadı. _( altinpanel/.../RAPOR.md §4 satır 126-128 )_
- **Dolar (DXY, UUP), 10y nominal/reel faiz, başabaş, 2y, eğri, S&P, Nasdaq, VIX, GVZ, MOVE, HY, petrol, bakır, gümüş, platin, BTC, EEM, FXI, TUR -> VİOP altın (t-1 ABD kapanışı):** 240 IC testinin %2,1'i |t|>=2 (şans %4,6). DXY Δ1 t 2,76 ama etki VİOP girişinden önceki 18 saatte biter (t-1 20:00'den t 15:00'e); t->t+h'ye kalmıyor. DXY Δ5 h3/h5 IS 2,5-2,75, OOS -0,7/-0,85. DXY sapması (C3) OOS t -1,65; eğri dikleşmesi (C2) 2013-16'da ters (t -2,09), DÜŞÜK. _( xau/.../analiz/a4_abd_capraz.md §0 (satır 9-14), §7 (satır 270-286); HAKEM.md §2.2 satır 216-219 )_
- **Yetişme kuralı: 'altın makroya (dolar, T-bond, S&P, USDJPY, USDCNH, BTC, gümüş) göre geride kaldı, yetişir' (a5_yetisme_YOK):** IS t -2,21, OOS t -0,98: işaret ters, yetişme yok sürme var. 297 testte |t|>2 oranı %2. ETF tarafında 114 gün içi göreli değer testi OOS 2022+'da çöktü (72 testin hiçbiri tutmadı). Reel faiz+dolar model artığı: OOS demeaned Sharpe 0,06. _( xau/.../sentez/HAKEM.md §2.2 satır 223-224; analiz/e2_etf_leadlag.md §3b satır 112-117; a4_abd_capraz.md satır 140-143 )_
- **BTC -> altın:** YOK (tahvil ETF'leri ve kripto: TLT, TIP, BTC). _( xau/.../analiz/a4_abd_capraz.md §7 madde 6 (satır 278) )_
- **Gümüş -> altın, altın/gümüş oranı z-skoru, altın -> gümüş (SLV~GLD, SIL~SLV artığı):** Oran z-skoru IS'te t 2,4-2,5, OOS -0,21/+0,16; a5_B1_altin_gumus_5g IS t -0,68, OOS -2,82 (post-hoc). SLV~GLD ve SIL~SLV her k ve h için çoğunlukla |t|<2. Altın->gümüş yönünde ayakta kalan kural yok. _( xau/.../analiz/a4_abd_capraz.md satır 137-139, 276, 280; e2_etf_leadlag.md satır 101; HAKEM.md satır 222, 514 )_
- **Şanghay / Asya -> altın: Şanghay primi, SHFE primi, Hang Seng, Nikkei, KOSPI, ASX, Çin ETF primi; Çin madenci artığı -> VİOP (a6_cn_gold_res_comp_h5):** Şanghay primi en iyi |t| 1,99, IS'te ters; SHFE/Çin ETF primi ve Avrupa/Asya endeksleri -> GLD YOK. a6_hsi_h3 spot altın kontrolüyle kayboluyor (OOS t 0,56). Çin madenci artığı VİOP h5: IS t 0,37, OOS 3,40 (OOS'ta bulunmuş, 2024-26'ya yığılı) DÜŞÜK, izleme listesi. Tek ayakta kalan Asya izi E2-C5 (DÜŞÜK). _( xau/.../HAKEM.md §2.2 satır 226-228, §6.1 satır 513; analiz/e2_etf_leadlag.md §3c satır 127 )_
- **Altın gün içi -> GDX ertesi gün ters (C3 / E3-2):** IC anlamlı (t -3,84) ama maliyet sonrası işlem değeri yok: yılda 105 gidiş-dönüş, ideal stres Sharpe -0,23, yalnız uzun < B&H (0,37 vs 0,41); E3-2 OOS t -1,87, B&H'ye eşit. E3-1'in GDXJ sürümü bu yüzden ayakta kaldı. _( xau/.../analiz/e2_etf_leadlag.md §3b satır 118, §5 satır 282; HAKEM.md §2.2 satır 255, 257 )_
- **Platin 5 günlük -> GDX ters (C4):** t -4,18, OOS -3,87 ama mekanizma yok, veri kirli (PL=F 2008-09), 2013-17'de işaret ters, 500 testin en üstü (veri madenciliği); DÜŞÜK. _( xau/.../analiz/e2_etf_leadlag.md §3c satır 129-131, §5 satır 281 )_
- **Kaldıraçlı/ters altın ETF'leri: NUGT, JNUG, UGL, 2×GLD, 3x; GLL, DUST, JDST, ZSL:** 1-5 günde nominal kaldıracı izliyor (UGL 2,00-2,02) ama 2×GLD'ye göre yılda -%6,9, NUGT -%20, 3x -%53 aşınma; Sharpe'ı iyileştirmiyor. NUGT VaR99 2026'da 1 gün %16,9 / 5 gün %27,4; en kötü 5 gün -%79. Ters ETF aşınması yıllık: DUST -%35, JDST -%49, ZSL -%40 (GLL -%2). JDST'li C2j 2020'de -%62,2. Kısa bacak OOS Sharpe negatif (JDST -0,50). UGL/AGQ/GLL/ZSL K-1 ortaklık; Midas'ta listelendiği teyit edilmedi. JNUG yalnız E3-1 fenomeninin test hedefi (d2_zm_JNUG_h1 t -4,01, OOS -1,72). _( xau/.../RAPOR.md §5.3 satır 303 ve §9 satır 501; analiz/e2_etf_leadlag.md §2 (satır 74-83), §4 satır 241; HAKEM.md §1.3 satır 118 )_
- **Araç seçimi kuralları E3-3 (PHYS vs GLD) ve E3-4 (CEF):** Yönlü sinyal ve lead-lag değil; geçiş stratejisi OOS'ta başarısız (IR -0,29 / 0,07); PHYS fiyat adımı 3-9 bps; Midas'ta PHYS/CEF listelendiği teyit edilmedi. Prim 3-5 bps maliyetin altında. _( xau/.../HAKEM.md §2.1 satır 185-186; RAPOR.md §5.2 satır 292 )_
- **E1-C1 madenci takvim sepeti (ay başı+tatil öncesi, t 4,25/3,41) ve E1-C3 GDX 5 gün düşüş sonrası al:** Sepet sonradan kurulmuş (144 test), ayın ilk günü etkisinin yarısı aynı gün GLD kontrolüyle kayboluyor (1983-2007'de t 0,99). E1-C3: 1.046 testin beklenen maksimumu, eşik 4/6'da çöküyor, GDXJ'de yok. _( xau/.../HAKEM.md §2.2 satır 244, 246; RAPOR.md §5.3 satır 301 )_
- **Dönüş, trend ve seans kuralları: RSI(2), Connors, Bollinger, 2σ dip alma, MA/Donchian/TSMOM, gece etkisi (kapanışta al, açılışta sat), haftanın günü, FOMC, CPI, COT, ETF akışı, ML:** Dönüş kuralları ters işaretli, 3 dönemde zarar (drift çıkarılmış Sharpe -0,4...-0,7). Trend drift çıkınca ≈0. Gece etkisi (+3 bps/gün, t 6,6) gerçek ama kapanıştan kapanışa yakalanmıyor; başabaş 4-7 bps, 10 bps'te yılda -%10. COT ve akış fiyatı takip ediyor. ML 27 kombinasyonun hiçbirinde OOS R²>0. 2σ düşüş sonrası GDXJ ertesi gün ort. -72 bps (dönüş yok, devam). _( xau/.../RAPOR.md §3 (satır 160-182), §5.3; HAKEM.md §6.1 (satır 502-518) )_
- **A3_NFP_MOM (h1/h3) ve diğer yalnız-OOS bulunan VİOP kuralları:** NFP momentumu IS t 0,55 (h1) / 0,99 (h3), OOS t 3,46 / 2,64; 2010-21 sıfır/ters, en iyi 5 olay çıkınca etki kayboluyor, CPI'da ters. DÜŞÜK, izleme listesi. _( xau/.../HAKEM.md §2.2 satır 209-210, §2.1 satır 164 )_
- **VİOP'a özgü: USDTRY carry (a7_C1), gram altın sentetik primi ortalamaya dönüş (a7_C3), gram altın vadelisinde uzun kalmak:** a7_C1 altın sinyali değil (hedef F_USDTRY; kâr carry'den). a7_C3 t -5,8/-6,1 çok güçlü ama 3 bacak maliyetiyle net zarar (OOS Sharpe -0,77). Gram vadeli uzun, TL carry nedeniyle spot sentetiğin seans başına ≈%0,17 gerisinde. Türkiye'ye özgü hiçbir değişken ons altını öngörmüyor (120 testte 9 p<0,05, beklenen 6; en küçük q 0,65). _( xau/.../analiz/a7_turkiye.md §0 (satır 8-13); HAKEM.md §2.2 satır 232-234; RAPOR.md §7.4 )_
- **VİOP mikro yapı ve gün içi segmentler: uzlaşma-kapanış, baz dönüşü (a2_c2), akşam seansı gecesi (a2_c1):** a2_c1: brüt ≈3 bps ≈ maliyet, kapanıştan kapanışa değil, İŞLENEMEZ. a2_c2 baz dönüşü: istatistik gerçek (t -3,08) ama OOS kârı taşıma drift'i, göreli işlem (spot bacak gerekir). Uzlaşma-kapanış t -2,9 ileriye bakma artefaktı (temiz sürüm t 0,1). _( xau/.../HAKEM.md §2.2 satır 203-204; RAPOR.md §4.4 satır 267 )_

## Çelişkiler

- Etiket farkı: e2 analisti C2j ve E3-1'i YÜKSEK etiketledi; HAKEM (SON = min(REP, ADV)) ikisini ORTA'ya indirdi. RAPOR HAKEM'i izliyor.
- ORTA etiketi ile çoklu test uyuşmuyor: 5 ETF kuralının yalnız E3-1 Bonferroni'yi geçiyor (q 0,0001). C1 q 0,019, C2j 0,056, C2 0,069, E1-C2 0,126 (global 0,52). RAPOR 'ETF'te 5 kural ORTA' derken bunu özetliyor ama dörde 'sağlam' denemez.
- Sharpe sayıları getiri tanımına göre değişiyor (log vs basit): C2j OOS 0,64 log / 0,81 basit; B&H 0,31 / 0,54. C2 e2'de log 0,58 vs B&H 0,41, HAKEM basit 0,71 vs 0,60; 2022+ e2 0,58 vs 0,57, HAKEM 0,69 vs 0,77. E3-1 OOS Sharpe RAPOR 0,71 vs HAKEM tablosu 0,72 (basit getiri). Sentez basit getiriyle yapıldı.
- A4-C1 için üç ayrı q: HAKEM alan içi 0,29 ('VİOP'ta hiçbiri geçmiyor'), a4 global 0,43 (1.071 test), aile içi 0,013. Kayıt dosyasındaki global q 0,07-0,10 varyant tekrarından yapay, kanıt sayılmamalı. OOS Sharpe de 0,72 (Yahoo adjclose) ile 0,52 (ABD takvimiyle kurunca) arasında oynuyor.
- Literatür çelişkisi: literatür 'altın madencilere öncülük eder' (Lucey-O'Connor 2017) diyor; kütüphanede madenci artığı altına (C1, A4-C1) öncü çıkıyor. 2010-16 spotta etki yok (IC 0,016): etki dönemsel olabilir.
- Panel denetimi (10.11) 'ons altın için sinyal yok (66 testte 0)' derken XAU raporu (07.11) VİOP için A4-C1 (GDXJ artığı, t 3,53) ve LOWMOM'u ayakta bırakıyor. Kapsam farkı olası: K1'deki eGDXJ GDXJ'nin GDX'e göre artığı, A4-C1 ise GLD'ye göre; 2 günlük vs 3 günlük ufuk; 2018-12 sonrası panel. K1'de eGDXJ -> ons altın satırı okunan kısımda ayrıca verilmedi.
- Altının gün içi hareketi hedefe göre ters işaretli: GDXJ'yi ertesi gün ters öngörüyor (E3-1) ama TRALT'ı aynı yönde (+25,7 bps/σ, t 2,40; FDR geçmedi) ve ons altını hiç öngörmüyor (t -0,13).
- 04.11 rehberi ile 10.11 denetimi: rehber hedge'li +35,5 bps (t 2,2), hedge'siz +25 (t 1,3) demişti; 10.11'de düşük maliyetle hedge'li +43,2 (t 2,55), hedge'siz +26,5 (t 1,34), bireysel maliyetle +23,9 (t 1,41) ve +11,5 (t 0,58). Rehberin +35,5 rakamının maliyet varsayımı okunan dosyalarda yok. Hedge'li kuralın fazlasının 19,2 bps'i XU030 bacağının kendi kazancı (t 1,67).
- Panel denetimi iç tutarsızlıkları: K1 eGDXJ->TRALT'ı 'geçti' (q 0,086) saydı, V1 aynı bulguyu 'kırılgan, muhtemelen sahte' diye düşürdü (RAPOR V1'i izliyor). V1: K1/K2 çıkış ertelemesi şartnamede yok, n=408 min_periods ile hedefe uydurulmuş; ertelemeyle brüt 33,3'ten 34,5'e çıkıyor.
- Saat farkı ve ileriye bakma payı: RAPOR 'VİOP'ta ABD verisi 18 saatte fiyatlanıyor, öncülük saat farkı' diyor; yine de A4-C1 (t-1 ABD kapanışı) ayakta. TRALT'ta sinyal uzlaşma getirisinden ölçüldü, kullanıcı 17:55'te ölçecek (önceki çalışmada 4-13 bps/işlem fark; panel K1 g-GC korelasyonu 0,85, eski çalışmada 0,98).

## Açık kalanlar

- 04.11 rehberleri (raporlar/2026-11-04_kapanis_1-3gun/rehber/altin/REHBER_altin.md, koza/REHBER_koza.md) ve TRALT.md karti okunmadı; 04.11 sayıları yalnız ek/00_yontem.md satır 9'daki özetten.
- HAKEM.md tamamı okunmadı: §3 örtüşme, §4 birleşim tabloları, §5 Pazartesi durumu, §7 risk ayrıntıları ve sentez/sinyal_tablosu.csv (kural metinlerinin hakem sütunları) okunmadı; ETF kurallarının net bps/işlem değeri hiçbir okunan dosyada verilmiyor (yalnız brüt bps/aktif gün ve yıllık net).
- Olay sayısı (n) E3-1, C2j, C2, C1, A4-C1, LOWMOM, A8-3 için okunan dosyalarda yok; yalnız yılda gidiş-dönüş sayısı var.
- TradingView kodları: AMEX:GLD/GDX/GDXJ/SPY, TVC:GOLD, OANDA:XAUUSD, BIST:XAUUSD1! dosyada doğrulanmış. TRALT1!, XU030D1!, Asya madencileri (2899.HK, 1818.HK, 600547.SS) ve ABD 2 yıllık faiz için TradingView önekli kod dosyalarda yok.
- a4_abd_capraz.md §3 tek değişkenli tablolar (satır 69-119) ve a7_turkiye.md satır 40 sonrası okunmadı; DXY/faiz/BTC sonuçları §0 ve §7 özetlerinden.
- ek/V2_defter_dogrulama.md okunmadı: panel RAPOR'a göre 20 iddianın 14'ünün kaynağı oturumda görülemedi (rapora girmedi ya da 'doğrulanmadı').
- K1 FDR/plasebo bölümü ve K1'de eGDXJ -> ons altın (B1) sonucu okunmadı; XAU A4-C1 ile panel eGDXJ çelişkisi bu yüzden kesin çözülemedi.
- Midas'ta NUGT/JNUG/UGL ve PHYS/CEF listelemesi, kur makası ve %10 VİOP stopajının 2026 teyidi dosyalarda 'doğrulanmadı' olarak duruyor; E3-1 canlı örneklem dışı doğrulaması yok (tüm sonuçlar geçmiş veri, binlerce testten seçilmiş).
