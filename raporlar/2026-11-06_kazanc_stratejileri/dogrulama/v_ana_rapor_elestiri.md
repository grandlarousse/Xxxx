# Ana rapor eleştirisi: tamlık ve tutarlılık (06.11.2026)

Denetlenen: `RAPOR.md`. Karşılaştırılan: `uygulama/PLAN_BIST.md`, `uygulama/PLAN_ABD.md` (nihai planlar), `dogrulama/*.md` (6 dosya, tamamı okundu), `ajanlar/*.md` (16 dosya; özet bölümleri ve RAPOR'daki rakamların kaynak satırları tarandı). RAPOR.md değiştirilmedi. Dış kaynak çekilmedi. Yatırım tavsiyesi değildir.

## 0. Özet hüküm

- **Soruları cevaplıyor.** Dört alt soru (BIST'te kazananlar / sen; ABD'de kazananlar / sen) ayrı bölümlerde, temel bilgi anlatmadan cevaplanıyor. Çıta düzeltmesi (§0), taban oranlar ve "çekirdek çıtada, uydu küçük, rejim dönüşüne hazır ol" sonucu planlarla uyumlu.
- **Ama §5 "Ortak sonuç"un iki maddesi planlarla çelişiyor ve kullanıcıyı fazla riske itebilir:**
  - m.3'teki risk sınırları (küme %1,5, toplam %3/%5/%6, aylık %6) iki planın da bugünkü sınırları değil. Ajan önerisinden (`abd_profesyonel.md` satır 73) geliyor ve ABD planının Faz 2–3 sınırlarına denk düşüyor; ABD'de bugünkü sınırların ~2–2,5 katı.
  - m.4 "zorunlu satıcıların karşısında dur" planlarda alfa değil, kaçınma kuralı. Fon tasfiyesi hisseleri dışlama listesinde.
- §1.5 m.2 ("faiz indirim döngüsü" bir tetik, "bankalar ve VİOP üzerinden kaldıraç") hem raporun kendi §1.4 bulgusuyla hem BIST planıyla çelişiyor.
- **Dürüst belirsizlik eksik kalmış:**
  - BIST'te çıtanın altında kalma olasılığı (~%35–45) ve USD sonucu yazılmamış.
  - ABD'de ağırlıklı merkezin USD nakdin bile altında olduğu yazılmamış.
  - ABD şampiyonlarının +0,4–0,6R beklentisi doğrulanmamış girdilerden geliyor; rapor bunu kesin bilgi gibi sunuyor.
- **Servet düzeyinde iki kural raporda yok:**
  - ABD planının döviz anahtarı. Planın kendi ifadesiyle "toplam riski en çok etkileyen kural" bu.
  - Pazartesi sabahki TL→USD SWIFT. Bu yüzden "Pazartesi yapılacak tek finansal işlem" ifadesi eksik.
- Raporun §0'daki "burada yalnız doğrulamadan geçen ya da düzeltilmiş rakamlar var" iddiası tam doğru değil (§3'te örnekler).

---

## 1. Sorulara cevap ve eksik / az ağırlıklı bulgular

### 1.1 Cevap kalitesi

| Soru | Cevap var mı | Not |
|---|---|---|
| BIST'te kazananlar nasıl kazanıyor | Evet (§1.1–1.3) | Katman tablosu iyi. Eksik: 2025–26'nın meşru büyük kazançları emtia/kıymetli maden fonlarından ve krizde nakit/döviz/kısa pozisyondan geldi (aşağıda). |
| Sen BIST'te nasıl kazanırsın | Evet (§1.4–1.5, §2) | Net mesaj: "bu rejimde çıta + 1–2 puan, kalanı rejim dönüşünde". İyi. Ama §1.5 m.2 ve §5 m.3–4 bu mesajla çelişen, daha agresif bir tarif veriyor. |
| ABD'de kazananlar nasıl kazanıyor | Evet (§3) | Taban oranlar, sağ kuyruk, anomali çürümesi ve kaldıraçlı beta ayrımı doğru. Şampiyonların beklenti sayıları fazla kesin (§3). |
| Sen ABD'de nasıl kazanırsın | Kısmen (§4) | Kurallar doğru özetlenmiş. Eksikler: 1. yılın beklenen değeri USD nakdin altında; servete maliyeti var; faz kapıları yanlış özetlenmiş; döviz anahtarı ve vergi kalemleri (hayalet vergi, 2026 kısa vergi yılı, veraset) yok. |
| Temel bilgi yok | Uygun | Kavram anlatımı yok. |
| Dürüst belirsizlik | Kısmen | §6 iyi, ama olasılık ve kötü kuyruk rakamları planlarda olup raporda yok. |

### 1.2 Korpustan eksik ya da az ağırlıklı bulgular

| # | Bulgu | Kaynak | Neden önemli |
|---|---|---|---|
| E1 | 5 yılda hisse fonlarının 75'inden 72'si PPF'yi geçti; 5 yıllık medyan hisse fonu +%838–916 (evrene göre), PPF +%447. Medyan aktif hisse fonu endeks fonunu 3 yılda ~22 puan (yılda ~4,4) geçti. DDF ve %81 hisseli TTL de PPF'yi geçti. | v_bist §3 m.2; v_profesyonel T1, eksik 3; tr_profesyonel §0 | Rapordaki "profesyoneller çıtayı aşamadı" rejime özgü. Seçim becerisi var; asıl sorun beta. Rejim dönüşü tezini güçlendiriyor. Ayrıca "91 fondan yalnız 1'i" ifadesini v_profesyonel "yanıltıcı" buldu. |
| E2 | **Değer faktörü hiç test edilmedi.** Hakemli BIST kanıtında en güçlü faktör (yılda %14–19 prim). MSCI Türkiye ileri F/K 6,66, EM 9,72. | v_bist §3 m.1, #20; v_capraz #18 | §6 "Sınırlar"da yok. Bütün testler fiyat tabanlı; en güçlü yerel kanıt kapsam dışı kaldı. |
| E3 | 2025–26'da meşru büyük kazançlar emtia rejim bahislerinden geldi: gümüş fon sepetleri 2025'te +%195–202 TL, petrol BYF sepeti 2026'da +%115 TL. 5 yılın en iyi fon kategorisi kıymetli madenler (+%982). Eylül–Ekim çöküşünü kazananlar nakit, döviz, petrol ve VİOP'ta kısa pozisyon taşıyanlar (XU030 kısa ≈ +%25, n=1). | bist_kim_kazaniyor §0 m.7–8; v_bist §3 m.2, #10 | "Kazananlar nasıl kazanıyor" sorusuna somut ve bireyin erişebildiği bir cevap. Raporda yalnız Koza/altın kümesi var. |
| E4 | 2027 stopaj takvimi: mevduat/PPF için %17,5 ve DİBS muafiyeti 31.12.2026'da bitiyor; engel 1–3 puan oynayabilir. | v_capraz §2 m.6; PLAN_BIST §1.1, §11.2 m.3 | Çıta tablosu (§0) 12 aylık ama bu riski söylemiyor. |
| E5 | MSCI asimetrisi: yalnız artışlar dondu, azaltmalar ve çıkarmalar sürüyor; Haziran 2027'ye kadar ilerleme yoksa Frontier/Standalone danışması. | v_capraz #17, §2 m.7 | Pasif akış net negatif. Raporda MSCI yalnız KRİZ ve kaçınma kuralında geçiyor. |
| E6 | Carry ile banka uzun pozisyonu aynı şokta birlikte kaybeder (S4: carry −%10/−%25, bankalar −%30/−%40). | v_capraz §2 m.8 | §5 m.3 kümelemeyi hisse düzeyinde anlatıyor; makro düzeydeki bu ortak kuyruk yok. |
| E7 | Carry geçmişi USD teminatın T-bill kazandığını varsayıyor. Türk aracı kurumunda USD teminat ~%0 kazanır; fark yılda 3,7–5 puan. | v_capraz #19 | §0'daki "+%20,8 USD/yıl" bu kadar şişik. |
| E8 | Backtest kör noktaları: 2020 öncesi fiyat limiti ±%20 iken ±%9,5 modellenmiş; çekilmeyen 99 kodda OZATD ve TEHOL var; kaldıraçlı ABD testinde 1 günlük gecikme 2000–02 düşüşünü −%89'dan −%75'e oynatıyor; NDX sonradan seçilmiş. | v_bist §2.2, §2.4; v_abd §2.1 | §6'da yalnız hayatta kalan yanlılığı var. |
| E9 | ABD şampiyonlarının girişi ve stopu çoğunlukla gün içi (açılış aralığı tepesi, günün dibi). Gün sonu uyarlaması test edilmedi; kapanış bazlı kopyada 1 ATR'lik stop kötü sonuç verdi. | v_profesyonel eksik 8, A12; PLAN_ABD §3.1, §9.5 | Rapor §4 "doğrulanmış şampiyonların yöntemi, gün içi ekransız" diyor. Yöntem doğrulanmış değil, yalnız sonuçlar. |
| E10 | VIX vade yapısındaki terslik tek günlük bir sıçrama (4.11'de VIX 16,61). Rejim hükmü 10 < 20 GHO yüzünden geçerli. | v_profesyonel A11; PLAN_ABD §2.8 | Rapor KIRMIZI'nın gerekçesi olarak VIX/VIX3M'yi öne koyuyor. Endeks düzeyinde filtre getiriyi de korumadı (PLAN_ABD §2.8). |
| E11 | Bedelsiz hak sonrası düşüş 2024–26'da zayıfladı (−%1,45, t −1,5). | v_olay §2.2 | §1.4'te tam dönem rakamı var, zayıflama yok. |
| E12 | ABD vergi ayrıntıları: hayalet vergi (USD getirisi sıfır olsa da pozisyondaki kur farkı vergilenir); 9.11–31.12 kısa vergi yılı ve 2026 zararının 2027'ye devretmemesi; 60 bin $ üstü US-situs veraset vergisi; 2026 tarifesi doğrulanamadı. | PLAN_ABD §1.2, §6.5; v_capraz #10–11; v_abd #36 | 250k $ ve üstü hesapta veraset riski gerçek. |
| E13 | Senaryo olasılıkları (öznel): S1 %35, S2 %40, S3 %15, S4 %10. S4'te hesap USD bazında şok anında −%10…−%21. | PLAN_BIST §9.2; tr_makro_engel §5 | Rapor yalnız "olasılıklar öznel" diyor, rakamları vermiyor. |

---

## 2. RAPOR ile nihai planlar arasındaki tutarsızlıklar

Ciddiyet: **Y** = karar ya da risk boyutunu değiştirir; **O** = yanlış kural ya da eksik koşul; **D** = küçük.

| # | RAPOR yeri | RAPOR diyor | Plan diyor | Ciddiyet |
|---|---|---|---|---|
| T1 | §5 m.3 | Küme başına risk ≤%1,5; toplam açık risk %3/%5/%6; ay içi zarar + açık risk %6'da yeni işlem yok | BIST: kümeden 1 yönlü pozisyon (KAPALI), toplam açık stop riski %2,5/%3,5/%5,5, aylık uydu kaybı −%2,5'te dur (§5). ABD Faz 1: küme ısısı ≤%0,75, toplam SARI %1,25 / YEŞİL %2,5, aylık devre kesici %3 (§5.1). Rapordaki rakamlar `abd_profesyonel.md` satır 73'ten geliyor ve ABD'de ancak Faz 2–3'te geçerli. | **Y** |
| T2 | §1.5 m.2 | Tetikler: "yabancı alımı", "faiz indirim döngüsü", "aylık TÜFE %2'nin altına inmesi"; "bankalar ve VİOP üzerinden kaldıraç" | Yabancı akımı **sayılmaz** (§2.1). Faiz indiriminden sonra bankalar yarım boy (A7; 6/6 döngü geride). TÜFE şartı 2 ay üst üste (M2). Kredili işlem hiçbir rejimde yok; K7 en çok 1x; AÇIK'ta net endeks betası ≤ +%40 (§1.3 m.4, K7, §5). | **Y** |
| T3 | §5 m.4 | Zorunlu satıcıların karşısında dur (MSCI, kredili tasfiye, fon tasfiye takvimi) | §3.10 başlığı: "zorunlu akış alfası değil, kayıptan kaçınma". MSCI'dan çıkarılan hisse yürürlüğe kadar alınmaz (A3). Kredili uçurumda "düşen hisse dipten alınmaz" (A4). Fon tasfiye hisseleri dışlama listesinde, en az 17.03.2027'ye kadar (§4.2, A9). Kısa vadeli dönüş BIST'te bilerek kullanılmıyor (§3.11). | **Y** |
| T4 | §4 (yok) | Döviz anahtarı geçmiyor | PLAN_ABD §1.5: 5 tetikten 2'si → servetin USD nakit payı %25–35, fazlası Türk bankasında döviz mevduatında. İlk tetiğin yarısı oluştu, ilk kontrol 12.11. **Planlar arası çelişki:** PLAN_BIST §9.2 kur korumasını reddediyor ("S4'teki USD kaybı bilinçli olarak kabul edilmiştir"). Rapor bunu çözmüyor. | **Y** |
| T5 | §2 Çekirdek satırı; §4 | "Pazartesi yapılacak tek finansal işlem" (BIST çekirdeği). ABD'de yalnız "canlı işlem yok" | PLAN_ABD §10: Pazartesi sabahı E'nin %40'ı SWIFT'le IBKR'ye, %10'u PPF'ye, %50'si 32 günlük mevduata. Planlar BIST "hesabı" ile ABD E'sinin servetteki payını birbirine bağlamıyor; rapor da bağlamıyor. | O |
| T6 | §4 son madde | 100 işlem, 12 ay, t ≥ 1,65 → risk %0,5–1 | Faz 2 (50 işlem, ≥4 ay, m ≥ +0,25R, t ≥ 1,0) → %0,5. Faz 3 (100 işlem, 12 ay, t ≥ 1,65, **EOD backtest**, KIRMIZI→YEŞİL döngüsü) → %0,75 (en çok %1). "Bu test geçilmeden risk %0,5'in üstüne çıkmaz." Faz 3'ün dürüst merkezi ~%8–16; %40+ için kenarın bulunma olasılığı ~%7–10 (§0 m.10, §8.3, §9.4–9.5). | O |
| T7 | §4 Dürüst beklenti | "Medyan −%2,5 ile +%6,5; TL'yi geçme olasılığı <%5" | Ayrıca: ağırlıklı merkez −%1,5…+%1,5, vergi sonrası −%2…+%1, "USD nakdin vergi sonrası getirisinin altında"; servete maliyet yılda ~%0,3–0,8 (§0 m.9, §9.3). | O |
| T8 | §2 Dürüst beklenti | Merkez +1…+2; toplam ~%33–37 | Ayrıca: P(engelin altında) ~%35–45; KAPALI sürerse +0,5…+1,5; USD ~+%10, S4'te şok anında −%10…−%21; ölçü birimi yazılı seçilir (§0 m.10, §9.2). | O |
| T9 | §2 K8 | "Tavan gün içinde ilk bozulduğunda sat" | "18:00'de son fiyat tavan değilse o günün kapanış seansında risk azaltan satış" (E kapanış satışı, medyan +%38). Gün içi izleme yok. 3 Eylül'den beri arz onayı yok → bugün 0 (K8). | O |
| T10 | §2 K1 | "20 günlük oran z-skoru \|z\|≥2" | z, son **60** günün ortalaması ve standart sapmasıyla; 20 gün **tutma süresi**. Ayrıca felaket stopu −%8, Kasım bacakları 25.11'de, Aralık 23.12'de devir (K1). | O |
| T11 | §2 K5 | "Zorunlu pay alım teklifi, satma ve ayrılma hakları" | Zorunlu tekliflerde kayıt tarihi kuralı varsayılır; sonradan alınan pay teklife verilemez → işlem yok. Yalnız gönüllü teklif ve satma hakkı kalır; katkı ~0 (K5). | O |
| T12 | §2 K3b | "+%6–7 fazla getiri"; "duyurunun ertesi kapanışında al"; "XU030 vadelisiyle hedgele" | Plan beklentisi olay başına **+%3…+%3,5** (%50 iskonto); evren 60 günlük hacim ≥ 20 mn TL; bildirim 17:00'den önceyse aynı gün kapanış seansı; 1 mn TL hesapta hedge genelde mümkün değil → hedgesiz; pilot boyu %1,25 (K3b). | O |
| T13 | §1.4 K3 satırı | Temettü öncesi 5 gün +%1,2 "işe yarayan" | +%1,2 **ham** getiri; piyasa ve maliyet sonrası olay başına +%0,2…+%0,5 (R2-6). Raporun kendi §2 satırı da +%0,2–0,5 diyor; iki rakam açıklamasız yan yana. | O |
| T14 | §1.4 kırılım satırı | "En büyük düşüş −%45/−%61" | −%45 S2'nin (raporda anlatılan kural) gerçekçi dolum düşüşü; **−%61 şablonsuz S1'e ait** (bist_test satır 202; PLAN_BIST K4). Ayrıca "medyan yılda %34,8" 36 varyantın 2010–26 medyanı; bunun "rf üstü +15,8" kısmı düzeltilmemiş rf ile hesaplandı. | D |
| T15 | §2 KRİZ satırı | "5 gün yeni giriş yok, açık pozisyonların stopu sıkılaşır" | Ayrıca hedgesiz K3/K3b kapanır, K6 kapanır, K4/K5/K9 stopu = max(iz-stop; KRİZ kapanışı × 0,90), K1 sürer. (d) tetiğinde "ya da seviye < 0" de var (§2.2). | D |
| T16 | §2 K6 | "Brüt rezerv kapısı 160 mlr $ (şu an 158,1)" | 6 koşulun 3'ü sağlanmıyor (net rezerv değişimi, yabancı DİBS, brüt rezerv); en erken değerlendirme 19.11. Rapor, yalnız 1,9 mlr $'lık bir açık kalmış izlenimi veriyor. | D |
| T17 | §1.5 m.1 | XU030 nakit-taşıma, çekirdek için verimli araçlar arasında (ima ~%29) | Bugün **HAYIR**: basit %29,3 < mevduat neti %32,6; açma eşiği %35,6 (§1.2, §1.5). | D |
| T18 | §2 Kaçınma takvimi | 11–13.11'de K3/K4/K5/K9'da yeni giriş yok | Ayrıca 11.11'de **hiçbir kolda** giriş yok; 9.11 18:00'den önce bilanço açıklamamış isimlerde giriş yok; bedelsiz hak sonrası 10 (oran ≥%500'de 20), yüksek verimli temettüde 5 işlem günü alış yok (§0 m.8, A1–A6). | D |
| T19 | §1.4 K7 satırı | "XU100 12 ayda +%3,3" | Plan +%3,8 (§0 m.1, T2). | D |
| T20 | §0 son paragraf | Çıta "~%31–36" | Raporun §1.2, §1.5 ve §5 m.2'si ile iki plan "~%31–38" diyor (faiz sabitse ~%36–38). | D |
| T21 | §5 m.2 | "Rejim kapalıyken agresif olmamak bir kenardır" | PLAN_BIST §2.1: "Rejim filtresi getiri kaynağı değil, risk kontrolüdür". PLAN_ABD §2.8: endeks düzeyinde filtre getiriyi korumadı (SARI+ günlerinde yıllık +%10,7, diğer günlerde +%19,1). | D |
| T22 | §0 tablo, ABD satırı | "~%20–28 USD/yıl" | Plan engeli hesap büyüklüğü ve maruziyete göre veriyor: u ≈ 0,3'te %12,7–19,5 / %15,6–23,3 / %17,5–25,9 (50k / 250k / 1m $); tam yatırımda ~%17–34; %20–28 doğrulanmış çapa. | D |
| T23 | §4 Erişim | "PDT kuralı (25 bin $) kalktı"; Midas "yalnız opsiyon alımı var" | PDT nakit hesaba zaten uygulanmaz; Reg T/free-riding sürer, aracı kurum geçişi 20.10.2027'ye kadar. Midas'ta call/put alımı **açık** ve teknik kilit yok; bu yüzden ≤500 $ dışında bakiye tutulmaz (§6.1). Rapordaki ifade tersinden okunabilir. | D |

---

## 3. Abartılı, yanıltıcı ya da fazla risk aldırabilecek ifadeler

1. **§5 m.3 ve §1.5 m.2 (T1, T2).** Kullanıcı bunları "ortak sonuç" diye okuyup ABD'de bugünkü planın ~2–2,5 katı risk alabilir ya da faiz indiriminde bankalara kaldıraçla girebilir. En yüksek öncelik.
2. **§5 m.4 (T3).** "Fon tasfiye takvimi" ve "kredili tasfiyeler" karşısında durmak, tam da dışlama listesindeki pump/tasfiye hisselerini dipten almak demek. BIST'te kısa vadeli dönüş yılda −%17,9; zorunlu akış tezi tek gözleme dayanıyor (v_bist §3 m.5). Atıf yapılan "reversal VIX ile artıyor" bulgusu ABD verisi.
3. **§3.3 "+0,4–0,6R" ve "stop dar: 1 ATR".** Luk'un işlem istatistikleri (v_abd #15) ve Minervini'nin isabet/oran rakamları (v_profesyonel A3) doğrulanamadı; Brandt'ın %54'ü onaylanmadı (A4). Beklenti tablosu zayıf kanıta dayanıyor (v_profesyonel eksik 10). Gün sonu uyarlamasında 1 ATR altı stop kötü sonuç verdi (A12). Planın kendi beklentisi +0,1R.
4. **§4 "Doğrulanmış üst dilimde yılda %40+ görülüyor".** Bağlamı (payda %8–17 kârlı; gün içi yöntem; %40+ için kenarın bulunma olasılığı ~%7–10; Faz 3 merkezi ~%8–16) olmadan hedef gibi okunabilir.
5. **§1.3 tablo.** Başlık "VİOP vadelilerinden hesaplandı" diyor, ama:
   - Koza, savunma ve rafineri satırları dalga etiketli **ex post** dip-tepe ölçüleri (v_dalga B11). Gerçekleştirilebilir getiri değiller.
   - GARAN +%91/+%73, YKBNK +%149 ve "pencerelerin %26'sı" bağımsız doğrulanamadı (v_capraz §1 sonu).
   - "Önceden görülebilen sinyal" sütunu sonradan okuma. Bankaların rejim dönüşündeki kazancı n=4 (PLAN_BIST §9.4).
6. **§1.4 "Bankalar son 63 günde +%26 koştu".** Bu, XU100'e **göre** +%26,3 (olay_akis_rejim satır 20, 187; v_olay §0). XU100 21.08'den bu yana −%22. Mutlak bir koşu gibi okunuyor.
7. **§1.4 sektör rotasyonu "uzun dönemde risksizin +11 puan üstü".** Bu rakam basit faizli, düşük rf serisiyle hesaplandı (v_bist §2.1, #23). 2024–26'da büyük sektör setinde rf'nin yılda **6–19 puan** gerisinde (bist_test satır 16). Rapor yalnız "altında" diyor.
8. **§1.4 K3b "12 yılın 12'si pozitif".** Bu, ajanın XU100 kıyaslı sonucu. v_olay muhafazakâr kıyasla yıl bazında doğrulamadı. Açık riskler de raporda yok: iptal edilen teklifler örnekte yok, kazanç açıklaması etkisi var, test önceden kayıtlı değil.
9. **§0 "Vergi avantajı çıtayı fiilen ~5–7 puan düşürür".** Tablonun sütunu zaten net çıta. Okuyucu 5–7 puanı %31–38'den bir daha düşebilir (çift sayım). Doğrusu: strateji getirisi vergisiz olduğu için doğrudan net çıtayla (%31–38) kıyaslanır.
10. **§3.1 SG Trend "en kötü 12 ayını yaşadı".** "En kötü" ifadesi doğrulanamadı (v_abd #7). §5 m.3'teki "yarı iletken–elektrik ekipmanı 0,72" ajanın kendi hesabı, tekrarlanmadı (v_profesyonel A14).
11. **§0 Yöntem "yalnız doğrulamadan geçen ya da düzeltilmiş rakamlar var".** 5, 8 ve 10. maddelerdeki örnekler bu iddiayla çelişiyor. Ayrıca AQR verisi diskte yoktu, TSMOM yeniden hesaplanmadı (v_abd #39).

---

## 4. Önerilen düzeltmeler (öncelik sırasıyla, en çok 8)

Her birinde "eski" metin RAPOR.md'den birebir alındı.

**1. §5 m.3: risk sınırları (T1).**
- Eski: `Küme başına risk ≤%1,5, toplam açık risk rejime göre %3/%5/%6. Ay içi zarar ile açık risk toplamı %6'ya ulaşınca o ay yeni işlem yok.`
- Yeni: `Bugün geçerli sınırlar planlardaki gibi. BIST: kümeden KAPALI'da 1, GEÇİŞ/AÇIK'ta 2 yönlü pozisyon, toplam açık stop riski KAPALI/GEÇİŞ/AÇIK'ta %2,5/%3,5/%5,5, aylık uydu kaybı −%2,5'te (AÇIK'ta −%3) o ay yeni giriş yok. ABD (ilk 50 işlem): küme ısısı ≤%0,75, toplam açık risk SARI %1,25 / YEŞİL %2,5, ay içi zarar + açık risk %3'te o ay yeni giriş yok. Küme %1,5 ve toplam %5–6 yalnız ABD'de Faz 2–3 kapılarından sonra.`

**2. §1.5 m.2: tetikler ve kaldıraç (T2).**
- Eski: `Tetikler: rezerv artışı, aylık TÜFE %2'nin altına inmesi, yabancı alımı, CDS 230'un altı, faiz indirim döngüsü. O zaman bankalar ve VİOP üzerinden kaldıraç.`
- Yeni: `Tetikler §2'deki rejim anahtarıdır (XU100 50/200 günlük, 3 hafta üst üste net rezerv artışı, 2 ay üst üste aylık TÜFE <%2, CDS <230 ve düşüyor, XBANK > 200 günlük). Yabancı alımı tetik değil, fiyatı izliyor. Faiz indirimi bankalar için alım tetiği değil, uyarı: indirimden sonraki 63 günde bankalar 6 döngünün 6'sında geride kaldı. Araç kaldıraç değil, rejimle büyüyen boy: kredili işlem hiç yok, endeks kolu en çok 1x, AÇIK'ta net endeks betası ≤ +%40.`

**3. §5 m.4: zorunlu satıcılar (T3).**
- Eski: `4. **Zorunlu satıcıların karşısında dur, ama hemen değil.** MSCI kararları, kredili tasfiyeler, fon tasfiye takvimi, satış yasaklarının bitişi. Stres anında likidite sağlamanın primi var (reversal getirisi VIX ile artıyor). Yalnız akış bittikten sonra ve likit hisselerde.`
- Yeni: `4. **Zorunlu satıcının önünden çekil; karşısında durmayı henüz kenar sayma.** MSCI kararları, kredili esnekliğin bitişi (13.11), fon uyumu (31.01.2027) ve tasfiye takvimi (~17.03.2027) planlarda kaçınma kuralı: etkilenen hisse yürürlüğe ya da takvim sonuna kadar alınmaz, düşen hisse "dipten" alınmaz. Likidite primi ABD verisinde var (reversal yalnız VIX>25'te pozitif); BIST'te kısa vadeli reversal yılda −%17,9 ve zorunlu akış tezi n=1. Denenecekse yalnız K9'dan, %0,25 riskle, yazılı fikir kartıyla.`

**4. §4 Sermaye: Pazartesi SWIFT ve döviz anahtarı (T4, T5).**
- Eski: `- Para TL'deyse ABD strateji sermayesi likit servetin **%10'u** (en çok %15'i). Bunun şimdilik %40'ı USD'ye çevrilip IBKR nakit hesabına gider, kalanı TL'de mevduat ve PPF'de bekler.`
- Yeni (iki madde):
  - `- Para TL'deyse ABD strateji sermayesi (E) likit servetin **%10'u** (en çok %15'i). E'nin %40'ı (servetin ~%4'ü) **Pazartesi sabahı** SWIFT'le IBKR nakit hesabına gider (önce küçük tutarla kur makası ölçülür); %10'u banka PPF'sinde, %50'si 32 günlük mevduatta bekler. Bu, Pazartesinin BIST çekirdeğinden sonraki ikinci finansal işlemi.`
  - `- **Döviz anahtarı (servet düzeyi):** beş tetikten ikisi oluşursa servetin USD nakit payı %25–35'e çıkar, fazlası Türk bankasında döviz mevduatında durur. Birinci tetiğin (net rezervde 2 hafta üst üste >5 mlr $ düşüş) yarısı oluştu; 12.11 verisi onu ve BIST KRİZ kesicisini birlikte tamamlayabilir. BIST planı kur korumasını reddediyor; hangisinin servetin tamamına uygulanacağını yazılı seç.`

**5. §3.3: şampiyonların beklentisi ve stop (madde 3.3).**
- Eski (iki satır):
  - `- İşlem başına risk sermayenin %0,25–1'i. Stop yapısal ve dar: 1 ATR ya da %7–10.`
  - `- İsabet %22–45, ortalama kazanç ortalama kaybın 2–5 katı. İşlem başına beklenti +0,4–0,6R.`
- Yeni (iki satır):
  - `- İşlem başına risk sermayenin %0,25–1'i. Stop yapısal ve dar (1 ATR ya da %7–10), ama giriş ve stop çoğunlukla gün içi (açılış aralığı tepesi, günün dibi). Kapanış bazlı kopyada 1 ATR altı stop kötü sonuç verdi; plan 1–2 ATR ve ≤%8 kullanıyor.`
  - `- İsabet %22–45, ortalama kazanç ortalama kaybın 2–5 katı (öz beyan; Luk ve Minervini istatistikleri doğrulanamadı). +0,4–0,6R bu girdilerden türetildi. Senin gün sonu uyarlaman hiç test edilmedi; planın beklentisi +0,1R (−0,2…+0,4R), öznel %50–60 olasılıkla sıfır ya da altı.`

**6. §4 Dürüst beklenti: merkez, maliyet ve faz kapıları (T6, T7, madde 3.4).**
- Eski: `- Yüksek getiri ancak kenar ispatlandıktan sonra gelir: 100 işlem, 12 ay ve t ≥1,65 gerekiyor. O noktada risk işlem başına %0,5–1'e çıkar. Doğrulanmış üst dilimde yılda %40+ görülüyor, medyan trader'da görülmüyor.`
- Yeni (iki madde):
  - `- Ağırlıklı merkez vergi öncesi −%1,5…+%1,5, vergi sonrası −%2…+%1: USD nakdin altında. TL'de kalmaya göre servete maliyeti yılda ~%0,3–0,8; karşılığı, ~%7–10 olasılıkla ölçeklenebilir bir kenarı ucuza keşfetmek.`
  - `- Kapılar: 50 işlem, ≥4 ay, ≥+0,25R ve t ≥1,0 → risk %0,5 (sermaye aynı). 100 işlem, 12 ay, t ≥1,65 ve hayatta kalma yanlılığından arındırılmış gün sonu backtest'i → %0,75 (en çok %1). O noktada da dürüst merkez yılda ~%8–16. Yılda %40+ ≥+0,3R kanıtlı kenar, yılda ≥150 işlem ve ~%5 olasılıkla −%45 düşüşü birlikte ister.`

**7. §2 Dürüst beklenti: olasılık ve USD (T8).**
- Eski: `- Merkez **+1…+2 puan**; %80 aralık −2…+5,5. Toplam net nominal getiri ~%33–37.`
- Yeni (iki madde):
  - `- Merkez **+1…+2 puan**; %80 aralık −2…+5,5. Toplam net nominal getiri ~%33–37 (reel ~%3–7); KAPALI sürerse yalnız +0,5…+1,5 puan. 12 ayda çıtanın altında kalma olasılığı ~%35–45.`
  - `- USD bazında ağırlıklı ~+%10 (çok belirsiz); kur kırılmasında (öznel %10) şok anında −%10…−%21. Plan bunu korumasız kabul ediyor; ölçü birimini (TL ya da USD) Pazartesiden önce yazılı seç.`

**8. §2 K8 satırı: gün içi kural (T9).**
- Eski: `| K8 Halka arz katılımı | Tavan gün içinde ilk bozulduğunda sat; seri bitince alma | İsteğe bağlı. Hesap başına yılda 8–22 bin TL, ölçeklenmiyor. |`
- Yeni: `| K8 Halka arz katılımı | Yalnız eşit dağıtımlı arza katıl; 18:00'de son fiyat tavan değilse o günün kapanış seansında sat (gün içi izleme yok; medyan +%38); seri bitince asla alma | İsteğe bağlı, risk bütçesi dışında. Hesap başına yılda 8–22 bin TL. 3 Eylül'den beri onay yok. |`

**Bu sekizin dışında kalan, düzeltilmesi önerilen kısa maddeler:**
- T10 (K1'de 60 günlük z, 20 gün tutma), T11 (K5 zorunlu teklif), T12 (K3b +%3–3,5 plan beklentisi), T13 (K3 ham +%1,2).
- §3 m.6 ("XU100'e göre +%26"), m.7 (sektör rotasyonunun 2024–26 açığı 6–19 puan), m.5 (§1.3 ex post ve doğrulanamayan satırlar), m.9 (vergi avantajı ifadesi).
- T20 (%31–36 → %31–38), T21 ("bir kenardır" → "bir risk kontrolüdür").
- §6 "Sınırlar"a E2 (değer faktörü), E4 (2027 stopajı), E8 (limit modeli, 1 günlük gecikme) ve E12 (ABD vergi kalemleri) eklenmeli.
