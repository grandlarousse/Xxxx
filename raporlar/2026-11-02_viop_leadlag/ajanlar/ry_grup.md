# RY — YURT İÇİ GRUP / İŞTİRAK / ORTAKLIK ajanı (grup)
Veri: 30.10.2026 kapanışına kadar (02.11 kısmi barları atıldı). Senkron analiz 2010+, gap/gün-içi analiz 2014+, saatlik veri 2023-12+ (TR grubu 2025-11+). IS = 2014–2020, OOS = 2021–2026. t değerleri Newey-West. Maliyet her bacak için gidiş-dönüş 8 bps ve 15 bps.
Çıktılar: `out/f_y_grup.csv` (197 satır), `out/y_ortaklik.csv` (78 ortaklık satırı), `out/code_y_grup/` (00→16 sırayla çalışır, 98/99 dosyaları tabloları üretir; ara sonuçlar res_*.csv).
1. tur (R1) KCHOL/SAHOL bulguları tekrarlanmadı, yalnızca referans verildi ve genişletildi.

## 1. Net bulgular tablosu
| # | Hisse | Sürücü (TV) | İlişki | Rakamlar | Güven |
|---|---|---|---|---|---|
| 1 | SAHOL | AKBNK (BIST:AKBNK) | Oran ortalamaya dönüş (pairs), iki bacak da VİOP'ta | log(SAHOL/AKBNK) z60>1,5 iken t+1 açılışta spread pozisyonu. IS +18 bps/gün (t 3,1), OOS +27 bps (t 3,5), 15 bps maliyette OOS +25. 13 yılın 12'si pozitif. 6 parametre setinin hepsinde IS ve OOS t 2,5–4,3. Grup bağı olmayan 19 benzer çiftte ortalama OOS t 0,24 | YÜKSEK |
| 2 | KCHOL | Koç NAV sepeti (TUPRS/FROTO/YKBNK/ARCLK…) | NAV iskontosu ortalamaya dönüş, KCHOL − β·XU030 kalıcı pozisyon | z250>1, t+1 açılış girişi. IS +6,9 bps (t 1,9), OOS +19 bps (t 3,0), Sharpe 1,09. 12 pencere×eşik kombinasyonunun hepsinde OOS t 1,7–3,7. Plasebo (KCHOL'ün kendi göreli fiyat z'si) OOS t ≈0. Ortak regresyonda NAV OOS t −3,1, plasebo 0,0 | ORTA |
| 3 | Grup çiftleri genel | lider hisse açılış gap'i (BIST:…) | lead_auction: aynı gün lider gap ayrışması → takipçi gün içi | Grup çiftlerinin %23'ünde t>2. Plaseboda (500 rastgele çift) bu oran %5,2, sektör emsallerinde benzer. pc ve likidite kontrollü grup primi +0,42 t (z 4,2). En güçlüleri: KRDMD→KRDMB/A t 5,8/5,5; TUPRS→AYGAZ 5,1; VAKBN→VAKFN 4,5; KCHOL→TTRAK 4,5; TRMET→TRENJ 4,3. **Ancak 10:30 TSİ girişte lider bileşenin getirisi ≈0 (−20…+20 bps)**: bilgi açılıştan sonraki ilk 30 dakikada fiyatlanıyor | ORTA (istatistik) / ÇOK DÜŞÜK (işlem) |
| 4 | Pay grubu ve ana–yavru senkronu | TRENJ–TRMET–TRALT, KRDMA/B/D, BRYAT–BRSAN, ECZYT–ECILC, VESTL–VESBE, EREGL–ISDMR | Senkron (XU100 kontrollü) | pc 0,74 / 0,62 / 0,62–0,66 / 0,56 / 0,55 / 0,46 / 0,45. Yılların %91–100'ünde aynı işaret, IS ve OOS ikisi de ≥0,28 | YÜKSEK (bilinen, mekanik) |
| 5 | Holding–iştirak senkronu | AGHOL–AEFES/MGROS/CCOLA, ALARK–ALCAR/ALGYO, ULKER–SOKM–GOZDE, AEFES–CCOLA, CIMSA–AKCNS, FROTO–TOASO, AYGAZ–TUPRS | Senkron | pc 0,23/0,18/0,13, 0,15/0,21, 0,19/0,18, 0,22, 0,40, 0,31, 0,28. Yılların ≥%82'sinde aynı işaret | YÜKSEK / ORTA |
| 6 | ISCTR | SISE, ANSGR, ANHYT, ISMEN… | Senkron, iştirak bağı XU100 kontrolünde yok | ISCTR–SISE pc −0,06; XBANK ve XUSIN de kontrol edilince +0,08. ANSGR, ANHYT, ISGSY için ≈0. ISCTR iştirak sepetini değil banka faktörünü izliyor (NAV/gap backtestleri ≈0) | ORTA (olumsuz bulgu) |
| 7 | AGHOL | AEFES_(h−1) (BIST:AEFES) | Saatlik öncülük | t 3,6 (FDR'den geçer). İki yarı: 3,5 / 1,5. Saatlik backtest brüt +5–9 bps, 8 bps maliyetle −3…+1 bps. KRDMB→KRDMA t 3,9 (FDR), brüt negatif | ORTA (istatistik) / ÇOK DÜŞÜK (işlem) |
| 8 | TVF hisseleri | TVF ortak faktörü (THYAO, HALKB, TCELL, TTKOM, VAKBN) | Senkron / DiD | Farklı sektördeki TVF–TVF çiftlerinde pc −0,02 (TVF dışında −0,003). Çift düzeyi "ikisi de TVF" katsayısı 0,014 (t 0,9). TVF'ye katılım öncesi/sonrası DiD −0,10…+0,06. Stres sonrası rebound (XU100<−%3, ertesi gün TVF − sektör): OOS +56 bps, t 1,5, n=49 | ÇOK DÜŞÜK (faktör) / DÜŞÜK (stres) |
| 9 | KCHOL / SAHOL / AEFES | YKBNK_{t−1} / AKBNK_{t−1} / AGHOL_{t−1} | lead_intra (günlük, kendi gecikmesi ve XU100 kontrollü) | t 2,7 / 3,6 / 3,2. OOS t 2,0 / 2,6 / 2,1. 712 testte yalnızca AKBNK→SAHOL ve 1 çift daha FDR'den geçti | DÜŞÜK–ORTA |
| 10 | Olaylar (2024–2026) | TVF devri, Koza birleşmesi, OYAK–Tekfen, Zorlu yapılandırması, Alarko–Carrier, Tera fon krizi | event | Koza → TVF (20.08.2024): TRALT AR0 +%10,6, ardından 2.–10. günlerde −8…−14. Koza birleşmesinin iptali (28.07.2025): TRMET/TRENJ −%10. Tekfen devrinin tamamlanması (24.07.2026): TKFEN CAR[2,10] +%34 (t 3,9), EREGL −%12. Zorlu yapılandırma başvurusu (29.06.2026): VESTL/VESBE +%10,4 (taban sonrası tavan), ardından ZOREN–VESTL pc 0,43→0,67. Tera (16.09.2026): TERA/TEHOL/PEKGY 20 günde ≈−%88 | DÜŞÜK (tek olay) |

### Önemli olumsuz bulgular (eleme yok; CSV'de ÇOK DÜŞÜK/DÜŞÜK olarak duruyor)
- **İştirak sepeti gap ayrışması → ana gün içi (R1'in KCHOL sinyali):** AGHOL, ALARK, TRENJ ve ECZYT'de açılış girişiyle OOS +29…+68 bps görünüyor. Ayrıştırınca kazancın neredeyse tamamı holdingin KENDİ açılış gap'inin geri dönmesinden geliyor (AGHOL'de lider tek başına OOS +4 bps, kendi gap'i +55 bps). 10:30 girişte AGHOL −3, KCHOL −6,5, AEFES −6 bps. ISCTR ve DOHOL'de sinyal hiç yok. Bu, grup sinyali olarak işlenebilir değil. R1'deki OOS zayıflaması diğer holdinglerde de teyit edildi.
- **Pay grubu oranı ortalamaya dönüş (KRDMA/KRDMB/KRDMD):** Kısa vadede (z60/z250) kaybettiriyor. KRDMB/KRDMD OOS −24 bps (t −1,8). Oran 2026'da trend/balon davranışı gösterdi: B/D Ocak 1,09 → Haziran 3,48 → 30.10 1,29. A/D Haziran 2025'te 1,87'ye çıkıp 0,89'a döndü. ADF p (2021+) 0,13–0,67.
- **Ana/yavru oranı ortalamaya dönüş:** SAHOL/AKBNK dışındaki 23 çiftte OOS ya anlamsız ya negatif. ANSGR/ANHYT'de ters yönde: oran momentumu (MR IS t −3,2 / OOS −1,8).
- **Saatlik öncülük işlenemiyor:** Grup çiftlerinde %t>2 oranı 9,5, sektör emsallerinde 9,8; fark yok. Brüt beklenen getiri 0–12 bps, net getiri negatif.
- **TVF ortak bir faktör değil.** DOHOL'ün NAV'ı büyük ölçüde nakit/USD ve halka açık olmayan varlıklardan oluşuyor; GWIND bağlantısı pc 0,04.
- **Yeni gruplar ve bağlantısız durumlar:** OYAK–Tekfen'in birlikte fiyatlanmaya başladığına dair henüz iz yok (devirden sonra 107 gün: TKFEN–EREGL pc −0,15, TKFEN–OYAKC 0,06). BORLS–BRSAN ≈0. GLYHO–PASEU bağı doğrulanamadı (pc 0,05).

## 2. Ortaklık yapısı (özet; tamamı `y_ortaklik.csv`)
- **İş Bankası:** SISE %51,6 (piyasadan alımlarla %52+). TSKB %47,7 doğrudan, grupla birlikte ~%50+. ISMEN %65,7, ANHYT %63,9, ISGYO %52,1. ANSGR'ye Milli Re (%87,6) üzerinden sahip. 2024'te iştirakleri TİBAŞ Holding'e kısmi bölünmeyle devretme kararı alındı; tescil doğrulanamadı. ISKPL İş grubuna ait değil (Işık Plastik). ISATR işlem görmüyor, ISBTR illikit; fiyat oranında birim uyumsuzluğu olduğu için analiz dışı bırakıldı.
- **Anadolu Grubu:** AGHOL→AEFES %43,05 (KAP, 30.06.2026); AB InBev %24. AEFES, AGHOL NAV'ının ~%43'ü. AEFES→CCOLA ~%50,3. AGHOL→MGROS ~%49 (teyit edilmedi).
- **OYAK:** HEKTS %50,95. Haziran 2026'da %8,5 satıldı, 14.10.2026 bedelli artışla pay tekrar yükseldi. OYAKC'de TCC-OYAK Amsterdam %80,05. **TKFEN: ON Investment BV (OYAK ortaklı) %42,8 (24.07.2026).** Libco (Cevahir) ARY'nin %32,08'ini satın alıyor; birlikte hareket edenlerin payı ~%36,7. EREGL ~%49 (teyit edilmedi).
- **Zorlu:** VESTL→VESBE %77,3. Bir KAP tablosu Zorlu Holding'i %52,8 ile gösteriyor; kaynaklar çelişkili. 28–29.06.2026'da finansal yeniden yapılandırma başvurusu yapıldı.
- **Doğan:** GWIND %70. Ditaş 2025'te satıldı (%68,24).
- **Alarko:** ALCAR %42,03. Carrier'ın payının devralınmasıyla %84,06'ya çıkacak (07.08.2026; tamamlanması 4Ç26'da bekleniyor).
- **Eczacıbaşı:** ECZYT→ECILC %30,62 (Eczacıbaşı Holding %50,62), ECZYT→INTEM %46,21.
- **Yıldız:** SOKM'de Turkish Retail Inv. %24,27 ve Gözde %23,66.
- **TVF:** THYAO %49,12, HALKB ~%91,5, TCELL %26,2, TTKOM %61,68, VAKBN %73,26 (Eylül 2025'te %1,53 satış), TURSG (Mayıs 2026'da %5 satış). Koza grubu (TRALT/TRMET/TRENJ) 20.08.2024'ten beri TVF'de.
- **Tera:** Tera Portföy fonları TEHOL'de %17,05 (06/2026) ve TERA'nın da TEHOL payı var. Fonlar 17.09.2026'da tasfiyeye alındı.
- **Bağ yok / doğrulanamadı:** GUBRF–BAGFS (sektör emsali), DOCO (Doğuş grubu değil; THY ile ortak girişim Turkish DO&CO), Kibar (BIST'te şirketi bulunamadı), PASEU–GLYHO.
- Koç ve Sabancı oranları R1'den alındı. "hafıza" etiketli satırlar KAP'tan teyit edilmedi (CSV'de işaretli).

## 3. Yöntem
- **01_liq:** 101 sembol için likidite tablosu: 1 yıllık medyan TL hacim ve sıfır getiri oranı. Eksik 25 günlük ve 21 saatlik seri `ydl.fetch` ile indirildi (KERVT Yahoo'da yok).
- **02_pairs:** 89 çift (ana–yavru, kardeş, pay grubu, ortak girişim, kontrol).
  - Senkron: corr (tam/3y/1y), XU100 kontrollü pc (tam/3y/1y/IS/OOS/yıllık), betalar (a~b+XU100 ve tersi), BH-FDR.
  - Öncülük, iki yönde (yavru→ana ve ana→yavru): y_{k,t} ~ x_{cc,t−1} + y_{cc,t−1} + XU100_{t−1}, k = cc/gap/intra.
  - Aynı gün testi (g2i): y_intra,t ~ x_gap,t + y_gap,t + XU100_gap,t.
  - Toplam 712 öncülük testi, BH-FDR aile bazında uygulandı.
- **03_placebo:** Grup bağı olmayan 500 rastgele BIST çifti. Lag-1 testlerinde null dağılım ≈N(0,1) (%|t|>2 = 4,4–6,2). g2i'de ortalama t 0,36, 99. yüzdelik 2,8.
- **04_peers:** 110 yönlü sektör emsali çifti (banka–banka, çimento, perakende vb.) eklendi. Ardından g2i_t ~ pc + log(likidite oranı) + grup + pay_grubu regresyonu kuruldu.
- **05_hourly:** h1 barlarında y_h ~ x_{h−1} + y_{h−1} + XU100_{h−1}. Yalnızca gün içi barlar kullanıldı (gece gap'i hariç). Likit bar alt örneklemi ve iki yarı ayrıca test edildi. 218 test, FDR uygulandı.
- **06_nav:** Piyasa değeri bazlı yaklaşık NAV. Referans ağırlıklarla al-tut sepeti kuruldu (KCHOL/SAHOL R1'den; AGHOL: AEFES .43, MGROS .33, ASUZU .03, ADEL .01; ECZYT: ECILC .70, INTEM .05; DOHOL: GWIND .12 + USD nakit .45; ISCTR "iştirak sepeti").
  - D = log P_H − log NAV (sabit hariç).
  - Hesaplananlar: yarı ömür, ADF, z250 → ertesi gün gün içi / 5 gün / göreli 5 gün getiri.
- **08_tvf:** 47 hissenin XU100 artıkları alındı (kayan β, look-ahead yok).
  - Çift düzeyi pc regresyonu (dönemlere göre).
  - TVF'ye katılım tarihleri etrafında DiD.
  - Stres günleri ve aşağı/yukarı betalar.
  - TVF sepeti artığı_{t−1} → üye.
- **09_bt:**
  - BT1: NAV z → kalıcı pozisyon. Sinyal kapanışta biliniyor, giriş t+1 açılışta; pnl = pos_{t−2}·gap + pos_{t−1}·intra.
  - BT2/2b: açılış ayrışması → gün içi.
  - BT3: oran z → kalıcı spread.
  - BT4: TVF stres dönüşü.
- **10_bt2_check:** Sinyal üç parçaya ayrıldı (lider gap / kendi gap fade / birleşik). Gerçekçi giriş testi: h1 ilk barının kapanışı (10:30 TSİ) → gün sonu.
- **11/12/13:** Parametre duyarlılığı, grup dışı oran plasebosu, NAV yerine holdingin kendi göreli fiyat z'si (plasebo).
- **14_events:** 12 olay, XU100 piyasa modeli AR/CAR.
- **15_hourly_bt:** Saatlik işlenebilirlik.
- **16_classes:** Pay grubu oran istatistikleri.

## 4. Kanıt ve yorum
**Senkron.** Ortaklık bağı, ancak yavru holding NAV'ında büyük bir paya sahipse ya da iki hisse aynı şirketin talepleriyse XU100 ötesinde anlamlı:
- Pay grupları: pc 0,58–0,66.
- Zincir iştirakler: TRENJ→TRMET→TRALT 0,51–0,74.
- Yatırım şirketleri: BRYAT→BRSAN 0,56; ECZYT→ECILC 0,55.
- Holding–iştirak: AGHOL–AEFES pc 0,23 ve son 3 yılda 0,50'ye çıktı. SAHOL–AKBNK XBANK kontrollü 0,15. KCHOL–YKBNK XBANK kontrollü 0,16.

Küçük iştirakler (SAHOL–KORDS/BRISA/TKNSA, ISCTR–ANSGR/ANHYT) XU100 kontrolünde sıfır ya da negatif. Bunun sebebi "banka–sanayi rotasyonu" faktörü. Kontrol kümesi: THYAO–PGSUS (grup dışı) pc 0,50. Yani grup bağı, sektör benzerliğinden daha güçlü bir senkronizasyon kaynağı değil.

**Kriz rejimi.** Zorlu grubunun pc'si yapılandırma başvurusundan sonra sıçradı: VESTL–VESBE 0,72→0,85, ZOREN–VESTL 0,43→0,67 (n=88). Tera grubunda fon krizinden sonra TEHOL–TERA 0,01→0,58 (n=32). Grup bağı, kredi ya da likidite stresi anında ortak faktöre dönüşüyor.

**Günlük öncülük (dünün getirisi → bugün).** Grup çiftlerinde lag-1 test istatistikleri plasebodan pek farklı değil: grup %|t|>2 oranı cc 9,0 / gap 5,6 / intra 8,4, plaseboda 5,4 / 6,2 / 4,4. FDR'den yalnızca 2 intra test geçti; biri AKBNK→SAHOL (R1 bulgusu).
- Tutarlı ama zayıf diğer sinyaller: AGHOL_{t−1}→AEFES gün içi (IS 2,4 / OOS 2,1); TRENJ_{t−1}→TRMET gün içi negatif (IS −4,4 / OOS −1,3; zincirdeki aşırı tepki geri dönüyor); OYAKC→TKFEN (yalnızca OOS).
- Likidite oranı lag-1 etkisini açıklıyor (regresyon katsayısı 0,08, z 4,7). Grup kuklası anlamsız (z 1,35).

**Aynı gün açılış ayrışması.** En güçlü istatistiksel bulgu bu, ama işlenebilir değil:
- Grup bağı etkiyi biraz artırıyor (+0,42 t, z 4,2; pc ve likidite kontrollü).
- Etki açılıştan sonraki ilk 30 dakikada tükeniyor. Açılış girişiyle lider sinyali +40–48 bps veriyor; 10:30 girişte KRDMA −7, KRDMB −6, AYGAZ −20, AGHOL −6 bps.
- Kalan kazanç illikit takipçinin kendi açılış fiyatının geri dönmesinden (own-gap fade) geliyor: ALCAR, KRDMB, ENJSA, CCOLA. Bu da grup etkisi değil, açılış seansı mikro yapısı. Ayrıca bu hisselerin çoğu VİOP'ta yok, spot spread'leri 15 bps'yi aşabilir.

**SAHOL/AKBNK oranı.** Holdingin en büyük iştirakiyle oranı 1–4 haftalık ufukta ortalamaya dönüyor; iki bacak da VİOP'ta işlenebilir.
- Karşı kontroller: SAHOL/YKBNK OOS t 1,7, SAHOL/XBANK 1,96, SAHOL/GARAN 0,5; diğer holdinglerin ana iştiraklerinde ≈0. Etkinin bir kısmı "SAHOL'ün banka faktörüne gecikmeli uyumu".
- R1'de AKBNK_{t−1}→SAHOL lead_intra t 3,6 bulunmuştu; bu bulguyla tutarlı.

**KCHOL NAV iskontosu.** Holdingin kendi fiyat MR'ından bağımsız bilgi taşıyor (plasebo ≈0). Etki OOS'ta IS'ten güçlü (2022–2026 yıllık +14…+40 bps/gün). D'nin yarı ömrü ~14 gün. SAHOL'de etki IS'te çok güçlü (t 5,0), OOS'ta kayboluyor. AGHOL'de yalnızca OOS'ta var.

**NAV iskontosu seviyeleri (log değişim, yaklaşık):**
| Holding | 2025 | 2026 YTD | Not |
|---|---|---|---|
| KCHOL | −9 | +11 | |
| SAHOL | −14 | +8 | |
| AGHOL | +6 | +1 | |
| ECZYT | −17 | −4 | |
| ISCTR (iştirak sepetine göre) | +14 | +16 | |
| AEFES/CCOLA | −19 | −23 | iskonto açılıyor |
| BRYAT/BRSAN | | −68 | BRSAN rallisi |
| ALARK | | +49 | Carrier devri |

**TVF.** Ortak sahiplik, getirilerde ortak bir faktör üretmiyor. 2024–26 döneminde katsayı +0,033 (t 1,6); bunu büyük ölçüde TRALT–TRMET çifti sürüklüyor, o da zaten Koza grubu. Stres günlerinde TVF sepetinin aşağı betası 1,09 ve yukarı betası 1,10; sektör kontrolünden farkı yok. Ertesi gün rebound +55 bps (t 2,2, n=74) ama backtestte 15 bps maliyetle t ~1,1. DÜŞÜK.

## 5. Karşı argümanlar ve sınırlamalar
- NAV ağırlıkları yaklaşık ve sabit başlangıç ağırlıklı (al-tut). Pay oranlarındaki değişimler (AGHOL'ün Migros payı, Koç'un YKB payı 2019–22, Sabancı) modellenmedi; D'nin uzun vadeli trendi bu nedenle kısmen yapay. Sinyal z-skoruyla (sapma) kullanıldı.
- Kalıcı pozisyon backtestinde maliyet yalnızca pozisyon değiştiğinde alındı. Bps değerleri aktif gün başına; yıllık getiri yaklaşık aktif gün oranı × 252 × ortalama. Açılış dolumu iyimser.
- g2i'nin "10:30 girişte kaybolması" yalnızca 2023-12 sonrası saatlik örnekleme dayanıyor (n=36–157 işlem). Eski yıllarda etki daha yavaş tükenmiş olabilir.
- Plasebo ve emsal kümeleri likiditeyle eşleştirilmedi; bunun yerine regresyonla kontrol edildi.
- Olay çalışmaları tek olaya dayanıyor; OYAK–Tekfen için 3 ay, Tera için 32 günlük veri var.
- Yahoo verisi: XHOLD günlük serisi bozuk (tek satır), XSGRT eksik. Bazı hisselerde (CCOLA, VAKFN) h1 ve günlük birimleri uyumsuz; |r|>%15 olan günler atıldı. ISATR/ISBTR fiyat oranı anlamsız.
- XU100 her iki hisseyi de içeriyor (mekanik içerme). Büyük hisselerde pc biraz bastırılmış olabilir, yani pc tahminleri muhafazakâr.

## 6. Açık sorular
- SAHOL/AKBNK sinyalinin gerçek VİOP spread ve derinliğiyle uygulanması: SAHOL VİOP likiditesi hangi seviyede?
- KRDMB primi 2026'da neden 3,5×'e çıktı? Fon krizi mi, imtiyaz/kontrol spekülasyonu mu? Tasfiyedeki fonların KRDMB pozisyonu KAP'tan kontrol edilmeli.
- OYAK–Tekfen grubu ileride ortak fiyatlanmaya geçecek mi? 2027'de tekrar test edilmeli.
- TİBAŞ bölünmesi tescil edilirse ISCTR–iştirak bağı değişecek mi?

## Kaynaklar
[İş Bankası iştirakleri TİBAŞ (Dünya)](https://www.dunya.com/sirketler/turkiye-is-bankasidan-tibas-holding-hamlesi-haberi-722134) · [İş Bankası Şişecam payı](https://paratic.com/sisecamda-hisse-alimi-is-bankasi-kontrolu-guclendiriyor/) · [KAP İş Bankası yeniden yapılanma](https://www.kap.org.tr/tr/Bildirim/720502) · [AEFES ortaklık tablosu KAP 2026](https://kap.org.tr/tr/api/file/download/4028328c9f52dc40019ff20542c44484) · [GCM AGHOL 4Ç25](https://www.gcmyatirim.com.tr/arastirma-analiz/ozel-raporlar/2026-03-09-anadolu-grubu-holding-aghol-2025-4-ceyrek-bilanco-analizi) · [DOHOL yatırımcı sunumu Mart 2026](https://www.doganholding.com.tr/media/sgrngxxw/dohol_yatirimci-sunumu_mart-2026.pdf) · [GWIND ortaklık (vkyanaliz)](https://www.vkyanaliz.com/rap/GWIND_2026-09-02_113656.pdf) · [Koza grubu TVF'ye devri](https://www.cnbce.com/piyasalar/koza-anadolu-metal-koza-altin-ve-ipek-dogal-enerji-turkiye-varlik-fonuna-devredildi-h3059) · [Koza birleşmesi sonlandırıldı](https://www.bloomberght.com/koza-grubu-birlesme-kararini-sonlandirdi-3753457) · [Tekfen OYAK devri](https://www.cnbce.com/borsa/tekfen-holdingde-ortaklik-degisimi-oyak-bagli-sirket-paylarin-yuzde-428ini-devraldi-h33805) · [ARY–Libco](https://gazeteoksijen.com/ekonomi/kapa-bildirildi-ary-holding-tekfen-holdingdeki-yuzde-32lik-payini-libco-insaata-devrediyor-280361) · [Hektaş OYAK payı](https://www.borsaningundemi.com/etiket/hekts) · [OYAKC ortaklık](https://www.vkyanaliz.com/rap/OYAKC_2026-07-28_97197.pdf) · [TVF Vakıfbank satışı](https://www.bloomberght.com/turkiye-varlik-fonundan-vakifbankta-hisse-satisi-3757278) · [TVF Türk Telekom/Turkcell](https://webrazzi.com/2022/03/11/turkiye-varlik-fonu-nun-turkcell-ve-turk-telekom-daki-konumu/) · [THY ve Halkbank TVF'ye](https://medyascope.tv/2017/02/06/turkiye-varlik-fonuna-bugun-eklenen-sirketler-thy-ve-halkbank/) · [Vestel/VESBE ortaklık](https://cdn.gedik.com/media/media/f3rnnviq/1c25_finanasal-degerlendirme_vesbe_20250502.pdf) · [Alarko–Carrier](https://www.bloomberght.com/alarko-carrierda-ortaklik-paylari-degisiyor-3785057) · [EYH faaliyet raporu 31.03.2026](https://www.eczacibasi.com.tr/assets/eyh-faaliyet-raporu-31032026.pdf) · [Şok ortaklık KAP](https://kap.org.tr/tr/api/file/download/4028328c9f0a0859019f18a4ebf33e5b) · [Tera fonu TEHOL alımı](https://www.cnbce.com/borsa/tera-portfoyden-tera-yatirim-teknoloji-holdingde-tehol-hisse-alis-aciklamasi-h30866) · [Fon krizi Tera (Evrensel)](https://www.evrensel.net/haber/6000845/pusula-portfoyun-ardindan-simdi-de-tera-portfoy-krizi) · [Kardemir pay grupları (TradingView kullanıcı yazısı)](https://tr.tradingview.com/chart/KRDMA/M4AVG59d/) · [Odaş–Çan2](https://paratic.com/odas-cante-pay-satislarindan-3-milyar-tl-kaynak-sagladi/) · [BRYAT faaliyet raporu 2023](https://borusanyatirim.com/_File/tr/FaaliyetRaporlari/BorusanYatirim/BRYAT-YK-Faaliyet-Raporu-31122023.pdf)
