# BIST planı, kırmızı takım 1: ön-ölüm (pre-mortem)

- **Hazırlanma:** Cuma 06.11.2026, ~15:30 TSİ. İncelenen sürüm: `uygulama/PLAN_BIST.md` (06.11, ~15:00).
- **Kaynak kısaltmaları:** Planınkiyle aynı ([VB], [VC], [VP], [TM], [TP], [HZ], [BT], [PL], [SE], [OB], [KK]). `dogrulama/v_olay.md` bu not yazılırken de yoktu.
- **Etiketler:** [D] doğrulanmış; [DM] doğrulanmamış ajan bulgusu; [TE] test edilmemiş risk kontrolü; [Ö] öznel tahmin.
- **Yöntem:** Önce planın 9.11.2026–9.2.2027 arasında "risk sermayesinin" %15–25'ini kaybettiği varsayıldı. Sonra her kural, bu kaybı üretebilecek yollara karşı tek tek denendi. Fiyat ve oranlar plandan ya da plandaki kaynak dosyalardan alındı. Yeni veri çekilmedi.

---

## 0. Varsayım ve hüküm

**Risk sermayesi.** KAPALI rejimde uydu bütçesi, spotta hesabın en çok %15'i ve VİOP teminatında en çok %15'idir. Stres tavanı %6'dır. Planın frenleri şunlardır ([plan] §5):
- aylık −%2,5: yeni giriş durur;
- birikimli −%4: boylar yarıya iner;
- birikimli −%6: uydu kapanır.

**%15–25 kaybın hesaptaki karşılığı:**
- Spot uydu (%15) esas alınırsa hesabın **%2,3–3,8'i**: 1 / 5 / 20 mn TL'de 23–38 bin / 113–188 bin / 0,45–0,75 mn TL.
- Spot ve VİOP birlikte (%30) esas alınırsa hesabın %4,5–7,5'i.

**Hüküm**
1. **Plan kurallara uyulduğu sürece hesabın tamamının %15–25'ini TL nominalde kaybedemez.** Çekirdek %85–100 mevduat ve banka PPF'sidir, kredili işlem yoktur, mevduat dilimleri bozulmaz.
2. **Uydu bütçesinin %15–25'i 3 ayda kaybedilebilir.** Bunun dört yolu var:
   - (A) kullanıcı planın dışına çıkar;
   - (B) sahte bir GEÇİŞ sinyali gelir, ardından kırılma olur ve çıkış emirleri dolmaz;
   - (C) teminat oranı artar, mevduat kilitli olduğu için aracı kurum pozisyonu zorla kapatır;
   - (D) aracı kurumda bir olay olur.
   Bu yolların ikisi KRİTİK kural açıklarından geçiyor (B1, B2).
3. **S4'te (kur +%15–30; öznel olasılık %10) hesap USD bazında −%10…−%21 kaybeder.** Bu planın bilinçli tasarımıdır, ama planın hiçbir yerinde sayıyla yazılmamıştır (B8).
4. **Pazartesi (9.11) uygulamasını değiştiren düzeltme yok.** Pazartesi yalnız çekirdek kuruluyor. B7 (aracı kurum seçimi) ve aracı kuruma iki ek soru Pazartesi'den önce yapılmalı. B4, 12.11'deki planlı K4 girişlerini erteliyor.

---

## 1. Ön-ölüm yolları

Olasılıklar öznel [Ö]. Kayıplar hesabın yüzdesidir.

| Yol | Ne olur | Planın hangi kuralı tutmuyor | Plana göre kayıp | 3 ayda olasılık [Ö] | Bulgu |
|---|---|---|---|---|---|
| **A. Davranış** | Rejim KAPALI ve uydu haftalarca boş. Kullanıcı "yüksek getiri" ister ve küme sever. Bankalar 1 haftada +%6,8 yapmış ve 50 GHO'ya dayanmış ([HZ] §0 m.2). Kullanıcı Blok 1'e (banka, holding, havacılık; korelasyon 0,77–0,79) plan dışı pozisyon açar ya da carry'ye girer. **Örnek 1:** %25 nominal banka vadelisi, S4'te bankalar TL bazında −%20…−%25 → **−%5…−%6**. **Örnek 2:** 0,5x short F_USDTRY, Mart 2025 tipi gün içi +%11,5 kur sıçraması ([VC] §2 m.4) → tek günde **−%5,8** | Tek kontrol günlükteki `kural_sapmasi` alanı (§8.2). Ne sınırı ne yaptırımı var | Sınırsız. Örneklerde −%5…−%6, yani uydunun %35–40'ı | **En yüksek:** %20–35 | B2 |
| **B. Sahte şafak + kırılma** | 26.11'de GEÇİŞ (M1 + T3 + M5). Aralık'ta 4 K4 yarım boy (toplam nominal ~%11,7) ve K1. Ocak–Şubat'ta 31.01 fon uyumu, ~3.2 blok kilidi, Şubat MSCI ve rezerv erimesi üst üste gelir: S3/S4 | ×0,94 çıkış limiti, kilit olmadan "kanayan" günlerde dolmuyor (B1). KRİZ kesicisi mevcut pozisyona dokunmuyor (B5) | K4: −%15 stop + −%7…−%20 taşma → −%2,6…−%4,1. K1 tek bacak −%15 → −%1,1. Toplam **−%3,7…−%5,2** | %5–8 | B1, B5, B6 |
| **C. Teminat zinciri** | K1 açıkken kurum teminat oranı %33,3'ten %100'e çıkar ya da Takasbank aşırı hareket parametresi devreye girer. Teminat %5'ten %15'e çıkar. "Serbest ≥ 2×" kuralı %45 ister, ama 30.11'den sonra PPF %40'tır ve mevduat bozulmaz | §1.3 ve §5'teki teminat tavanları kendi içinde çelişiyor (B3) | Kurum kilitli ya da şok gününde zorla kapatır: **−%0,5…−%1,5** artı kenar kaybı | %5–10 | B3 |
| **D. Aracı kurum** | Hesap dondurulur, pozisyondan çıkılamaz. Aracı kurumdaki nakit mevduat sigortası kapsamında değildir | Kurum seçimine dair hiçbir kural yok (B7). Emsal: Tera Yatırım'ın lisansları 26–27.10.2026'da iptal edildi | Belirsiz, büyük olabilir | < %2 | B7 |
| **E. TL şoku, USD ölçüsüyle** | Kur birkaç haftada +%15–30. Çekirdek ayda ~%2,6–3 TL kazanır | Ölçü birimi yazılı değil (B8) | USD bazında **−%10…−%21**. TL engeli yine geçilebilir | %10 (S4); S3'te ~0 | B8 |

**Düzeltmelerden sonra:**
- Yol A, K9 kolunun freniyle hesabın −%1,5'iyle sınırlanır.
- Yol B'nin kuyruğu ~1 puan küçülür: −%2,4…−%4,3. Kalan kayıp kilit günlerinden gelir ve çözümsüzdür; ona karşı koruma boyuttur.
- Yol C ortadan kalkar.
- Yol D'nin etkisi aracı kurumdaki varlıkla sınırlanır.

---

## 2. Bulgular

### B1. KRİTİK: Spot çıkış limiti (önceki kapanış × 0,94) stopları tam kriz günlerinde devre dışı bırakıyor ve test edilen kuraldan sapıyor

**Nerede:** §3 "Ortak kurallar"; K4 E1; K3 "Satış"; §6.2 "Spot çıkış".

**Sorun:**
- Kapanış seansı tek fiyatlıdır. Müzayede fiyatı önceki kapanışın %6'sından fazla aşağıdaysa satış emri **dolmaz.**
- Hisse tabanda kilitli değilse "taban kilidinde her gün yenilenir" hükmü de devreye girmez.
- Test bunu varsaymadı. [BT] §1 "Bilinen biaslar" m.3: çıkış yalnız gün ≤ −%9,5 ise ertelendi; yani −%6…−%9,5 günlerinde testin çıkışı doldu. Planın çıkışı testten kötü, üstelik tam zorunlu satış ve kriz günlerinde.

**Bu günler sık mı?**
- XU100 21.05.2026'da tek günde −%6 yaptı ([TM] §4.3).
- 31.08–30.10 arasında BIST100 −%24,9; Ekim'de medyan hisse −%12,8 ([KK] §3).
- XHARZ 3 ayda −%62 ([HZ] §3).

**Örnek:** Kilitsiz 5 gün üst üste −%7.
- ×0,94 limitiyle emir hiç dolmaz → **−%30,4.**
- Taban limitiyle ilk gün dolar → −%7.
- K4 sondasında fark ~1,5R.

**Yan etkiler:**
- **K3:** Gün −1'de %6'dan fazla düşüşte satış dolmaz. Pozisyon hak gününe taşınır; bu, planın "Asla" listesine aykırıdır. %5 üstü verimde hak sonrası 5 gün −%2,1'dir ([OB] §8).
- **Stres formülü:** "2 taban = −%19" ve "en kötü hafta" (§5) yalnız çıkışlar dolarsa geçerlidir.

**Düzeltme (§3 ortak kurallar ve §6.2'ye aynen):**
> "Risk azaltan bütün spot çıkışlar kapanış seansına **limit = o günün alt fiyat limiti (taban fiyatı)** ile girilir. Bunlar: K4 E1/E3/E4/E6; K3 gün −1 satışı ve stopu; K5 çıkışı; A3, A4, KRİZ ve dışlama çıkışları. Kapanış seansı tek fiyatlı olduğu için emir müzayede fiyatından dolar. Dolmamışsa hisse tabanda kilitlidir ve emir ertesi gün aynı kuralla yenilenir. ×0,94 limiti yalnız acil olmayan çıkışta (K4 E2, süre) kalır."
>
> "VİOP çıkışları (K1, K2, K6, K7): 17:55'te karşı en iyi fiyat ± %0,3; 18:05'te ± %1; 18:08'de günlük fiyat limiti. Kilitte ertesi gün aynı sıra."

**Aracı kuruma 11. soru:** "Kapanış seansına taban fiyatlı satış emri kabul ediliyor mu, sabahtan girilebiliyor mu?"

**Beklenen etki [TE]:**
- Normal günde maliyet 0 (müzayede fiyatından dolar).
- Kriz ve kanama dizilerinde etkilenen işlem başına +1…+2R kayıp önlenir.
- İnce hissede düşük müzayede fiyatı riski var. Evren ilk 75 olduğu için kabul edilebilir.

### B2. KRİTİK: Plan dışı işlem için ne bütçe ne fren var; en olası kayıp yolu bu

**Sorun:**
- Planın kendi beklentisi engel + 1,5…2,5 puan. Rejim 0/7; uydu büyük olasılıkla Aralık'a kadar boş (§2.3, §9.4).
- Kullanıcının istediği "yüksek getiri" ve "stratejik küme". Bugünün göz alıcı adayları tam Blok 1: banka ve havacılıkta RS kırılımı ([HZ] §0 m.2; [VD] B12).
- Planın tek kontrolü günlükteki `kural_sapmasi` alanı (§8.2).
- Taban oranlar aleyhte: 3 yılda hisse fonlarının neredeyse hiçbiri PPF'yi geçmedi ([VP] T1–T2). Bireysel kaldıraçlı işlemde kaybeden oranı çok yüksek ([SE] §1.1).

**Düzeltme (yeni kol, §3'e K9 olarak):**
> "**K9 serbest kol.** Kullanıcının plan dışındaki bütün fikirleri için tek kanal: küme ve banka RS kırılımı, haber, sezgi.
> - **Araç:** Yalnız VİOP-47 spot ya da 1x pay/endeks vadelisi. F_USDTRY, opsiyon ve kredili işlem yok.
> - **Boyut:**
>   - İşlem başı risk: KAPALI'da ≤ %0,25, GEÇİŞ ve AÇIK'ta ≤ %0,5.
>   - Nominal ≤ %5; eşzamanlı en çok 2.
>   - Açık risk ve stres hesabına girer; Blok 1 sayımına K4 ile birlikte dahildir.
> - **Süreç:** Fikir kartı (mekanizma, giriş, stop, çıkış) 18:45'e kadar günlüğe yazılır. Emir ertesi gün kapanış seansında verilir. Stop zorunludur (B1 kuralıyla).
> - **Fren:**
>   - K9'un birikimli kaybı hesabın %1,5'ine ulaşırsa K9 6 ay kapanır.
>   - K1–K9 dışındaki tek bir işlem (kural_sapmasi = E): bütün uydu 1 ay kâğıda geçer. İkinci kez olursa 3 ay.
> - **Carry:** K6 kapısı kapalıyken hiçbir kolda short F_USDTRY yok.
> - **Eski lead-lag sinyalleri:** 6.11 itibarıyla açık pozisyonlar kendi çıkış kuralıyla kapanır. Yeni sinyal yalnız §3.11'deki %0,5'lik bütçeyle açılır."

**Beklenti:** K9'un R_fazla'sı ≤ 0 [Ö]. Amaç getiri değil, plan dışı kaybı hesabın %1,5'iyle sınırlamak. Yol A'nın kuyruğu −%5…−%6'dan −%1,5'e iner.

### B3. ÖNEMLİ: Teminat ve likidite kuralları birbirini tutmuyor; teminat artışında zorla kapatma riski var

**Sorun:** §1.3 PPF içinden spot uydu ve VİOP teminatı ayırıyor. §5 "serbest teminat ≥ 2 × kullanılan başlangıç teminatı" istiyor. §1.3 m.3'e göre mevduat dilimi bozulmuyor. Tavanlarda toplam şöyle:

| Rejim | Spot | VİOP teminatı | Serbest teminat (2×) | Toplam ihtiyaç | Eldeki PPF |
|---|---|---|---|---|---|
| KAPALI | %15 | %15 | %30 | %60 | %40 |
| GEÇİŞ | %25 | %20 | %40 | %85 | %50 |
| AÇIK | %40 | %25 | %50 | %115 | %70 |

**Teminat neden birden artabilir:**
- K1'in teminatı QNB oranında 2 × %7,5 × %33,3 = **%5.** Bir pay QNB'nin %100 sınıfına alınırsa (3.11'de ASTOR/HALKB/VESTL; [VB] #16) **%15** olur.
- Takasbank parametrelerinde aşırı hareket çarpanı 3; sürdürme teminatı başlangıcın %75'i ([HZ] §5).

**Düzeltme (§1.3 ve §5'e):**
> "**L1 (her kapanış):** VİOP başlangıç teminatı (kurum oranıyla) ≤ (PPF − spot uydu nominali) / 3. Bu kural, oranların 3 katına çıkmasını mevduat bozmadan karşılar. §1.3 ve §5'teki %15 / %20 / %25 tavanları üst sınır olarak kalır; bağlayıcı olan L1'dir.
>
> **L2:** L1 bozulursa (oran artışı ya da zarar) ertesi kapanışta VİOP pozisyonları orantılı küçültülür. Sıra: K6 → K7 → K2 → K1. K1'in iki bacağı birlikte küçültülür. Teminat için spot uydu satılmaz, mevduat bozulmaz.
>
> **L3:** Teminat tamamlama PPF'den yapılır. Satış emri PPF'nin saat sınırından (çoğunda 13:30; izahnameden teyit) önce verilir. VİOP hesabında her zaman ≥ 1 × başlangıç teminatı kadar fazla teminat durur: PPF teminat olarak kabul ediliyorsa PPF; edilmiyorsa nakit, bu durumda Kural 0 gereği boy yarıya iner."

**Örnek, 1 mn TL, KAPALI:**
- PPF 400 bin, spot uydu 100 bin → VİOP teminatı ≤ 100 bin.
- K1 QNB oranında 50 bin: sığar.
- Oran %100 olursa K1 150 bin ister → K1 2/3'e indirilir.

### B4. ÖNEMLİ: 12.11'deki K4 sondaları kredili işlem uçurumundan bir gün önce ve SPK kararından önce açılıyor; uzatma uçurumu ortadan kaldırmıyor, erteliyor; açık pozisyonlar için kural yok

**Sorun:**
- §7.2 ve §10'da Salı/Çarşamba sinyalleri Perşembe 12.11 18:00'de açılıyor. SPK bülteni ise 12.11 ya da 13.11 akşamı çıkıyor ([HZ] §1a).
- A4'e göre esneklik uzatılmazsa 16–20.11 arasında K4 girişi yok. Oysa 12.11 girişi doğrudan bu pencereye düşüyor.
- "Uzatılırsa değişiklik yok" hükmü eksik. Üç uzatmanın üçünde de (2026/60, /68, /78; [VB] #7) yeni bir bitiş tarihi geldi.
- Zorla satış en çok kredili pozisyonu yüksek orta-küçük ölçekli hisselerde beklenir ([HZ] §0 m.3, §3). AHGAZ ve ENERY VİOP-47 dışında. BIST'te haftalık kaybedenler kaybetmeye devam ediyor ([BT] §4).

**Düzeltme (A2 ve A4'e):**
> "**A2:** 11.11, 12.11 ve 13.11 kapanışlarında yeni K3, K4, K5 ve K9 girişi yok. İlk giriş, SPK kararının bilindiği günden sonraki ilk kapanıştadır:
> - Uzatıldıysa o gün (13.11 ya da 16.11).
> - Uzatılmadıysa ya da 13.11 seans sonuna kadar karar yoksa: K4 için 23.11, VİOP-47 dışı long için 30.11.
>
> **A4:**
> - Her yeni bitiş tarihine aynen uygulanır; uzatma yalnız takvimi kaydırır.
> - Oran kısmen artırılırsa (ör. %20 → %25–30) da uygulanır.
> - Uzatılmazsa, 13.11 kapanışında açık olan VİOP-47 dışı spot pozisyonlar: zarardaysa B1 kuralıyla satılır; kârdaysa iz-stop 27.11'e kadar %10'dur [TE]."

**Maliyet:** En çok 2 sonda (%0,25 risk) 1–2 hafta gecikir. Beklenen değer kaybı ~0.

### B5. ÖNEMLİ: KRİZ kesicisi ve zarar frenleri yalnız yeni girişi durduruyor; tetikler doğrulanmamış CDS'e dayanıyor, rezerv ve kur kaçışı ölçülmüyor; 5–6.11 küresel şoku planda yok

**Sorun:**
- **Mevcut pozisyonlar:** KRİZ (§2.2) yeni girişi 5 gün durduruyor ve K6'yı kapatıyor. Gerisi için "mevcut stoplar işler" diyor, ama B1 nedeniyle stoplar krizde dolmayabilir.
- **Belirsiz fren:** §5'teki "−%4 → boylar yarıya" yeni girişleri mi, açık pozisyonları mı kapsıyor, belli değil.
- **CDS:** M4, K6 kapısı ve KRİZ CDS'e bağlı. 248 değeri teyitsiz ([VC] §1 sonu; plan §11.2 m.7) ve 18:15'te birincil bir kaynaktan okunamıyor.
- **Gözlenebilir ölçüler zaten kaynakta var** ([TM] §5.1):
  - swap hariç net rezerv için "< 0 ya da 2 hafta üst üste ≤ −5 mlr $";
  - "1 aylık USDTRY vadelisinin zımni faizi politika faizini 5 puan aşarsa kaçış fiyatlanıyor" (5.11'de ~%34, politika %36).
- **Rezerv yakın tetik:** Swap hariç net rezerv son hafta −6,5 mlr $ ve "bu hızla 4 haftada sıfır" ([TM] §4.3). 12.11 verisi bir hafta daha ≤ −5 mlr $ gösterirse bu tetik ateşlenir.
- **Küresel şok:** 5.11'de Nasdaq-100 −%6,4; 6.11'de Nikkei −%6, KOSPI −%6/−%8 ([HZ] §0 m.9). Planda hiç geçmiyor.

**Düzeltme (§2.2 KRİZ satırına):**
> "**Tetikler (herhangi biri):**
> - (a) XU100'ün son 5 işlem günü kapanıştan kapanışa değişimi ≤ −%8;
> - (b) USDTRY için (S_t / S_{t−10})^(252/10) − 1 > %35;
> - (c) CDS > 300 (yalnız teyitli veriyle);
> - (d) swap hariç net rezerv 2 hafta üst üste ≤ −5 mlr $ ya da seviye < 0;
> - (e) F_USDTRY ön ay ima basit faizi > politika faizi + 5 puan ([BÜL] uzlaşması, §1.5 formülü);
> - (f) MSCI'ın Türkiye için sınıflandırma danışması açması.
>
> **K6 kapısında** (e), CDS koşulunun yerine geçer.
>
> **Açık pozisyonlar için eylem (ertesi kapanış):**
> - Hedgesiz K3 pozisyonları kapanır. Olay başına kenar +%0,5…+%0,7 ([VB] #26), kriz haftasının beta riskinden küçük.
> - K4, K5 ve K9'da stop = max(iz-stop, KRİZ günü kapanışı × 0,90).
> - K1 sürer. Bir bacak kilitliyse diğer bacak kapatılmaz.
>
> **§5 −%4 kuralı:** Açık yönlü pozisyonlar ertesi kapanışta yarıya iner; K1'in iki bacağı birlikte."

**Ek:** 6.11 kapanış rutinine küresel şok notu eklenir. Notun rejim kararına etkisi yok; KAPALI zaten kapalı.

### B6. ÖNEMLİ: MSCI kuralı yalnız Kasım'ı kapsıyor; Şubat 2027 gözden geçirmesi ve olası danışma duyurusu 3 aylık ufkun içinde; A4 sermayeyi MSCI'a en açık isimlere yönlendiriyor

**Sorun:**
- A3 yalnız 12.11 duyurusunu ve 30.11 yürürlüğünü kapsıyor.
- Yalnız ağırlık azaltmaları uygulanıyor, bu yüzden pasif akış net negatif ([VC] #17). Büyüklüğü hiç ölçülmedi ([VC] §2 m.7).
- "Danışmanın öne çekilmesi" bir kırılma yolu ([TM] §4.3 m.6). Plan §7.4 Haziran 2027 için yalnız "yeniden değerlendirilir" diyor.
- A4, VİOP-47 dışında long'u yasaklıyor. Böylece yeni long'lar yabancı payı ve MSCI ağırlığı en yüksek isimlere gidiyor.

**Düzeltme (A3'ün yerine):**
> "**A3:** Bu kural her MSCI gözden geçirmesine (sonraki: Şubat 2027; duyuru ve yürürlük tarihleri 1.12'de MSCI takviminden günlüğe yazılır) ve Türkiye hakkındaki her ad hoc MSCI duyurusuna uygulanır.
> - **Duyurudan önceki kapanış:** Yeni giriş yok.
> - **Silinen ya da ağırlığı azaltılan hisse:** Yürürlük kapanışına kadar alınmaz. K4, K7 ya da K9'da tutuluyorsa duyuru günü kapanışında B1 kuralıyla satılır.
> - **K1'de:** Bu hisse yürürlüğe kadar yalnız short bacak olabilir. Long bacak gerekiyorsa giriş yok.
> - **FIF/NOS listesi kamuya açık değilse** yalnız silinenler uygulanır ve günlüğe not edilir.
> - **Danışma duyurusu:** KRİZ (f) tetiklenir. MSCI kararına kadar Blok 1 yönlü hakkı 0, K7 kapalı ve K4'teki VİOP-47 önceliği askıda."

### B7. ÖNEMLİ: Aracı kurum karşı taraf riski hiç ele alınmamış

**Sorun:**
- Tera Yatırım'ın lisansları 26–27.10.2026'da iptal edildi ([TP] §4.1 takvim). TRHOL dosyasında 24 lisans iptal edildi ([KK] §2.4).
- Tera, aracı kurum sektör kârının %35'ini yapıyordu ([VB] #3).
- Plan aracı kuruma 10 soru soruyor ama hangi kurumla çalışılacağına dair hiçbir kural koymuyor.

**Düzeltme (§6.1'e):**
> "**Aracı kurum:**
> - Mevduat bankası iştiraki ya da SPK tedbiri altında olmayan büyük bir kurum olmalı.
> - Mevduat dilimleri doğrudan bankada tutulur, aracı kurumda değil.
> - PPF banka kanalından alınır. 20 mn TL hesapta PPF en az 2 kurumda tutulur.
> - Aracı kurumda yalnız L1'in gerektirdiği VİOP teminatı ve açık spot pozisyonlar durur. Boştaki nakit gece aracı kurumda kalmaz, PPF'ye geçer.
> - 20 mn TL hesapta spot ve VİOP iki ayrı kurumda tutulur.
>
> **12. soru:** Yatırımcı Tazmin Merkezi kapsamı nedir; nakit bakiye nerede ve hangi hesapta tutuluyor?"

### B8. ÖNEMLİ: S4'te USD ve reel ölçüdeki kayıp yazılmamış; ölçü birimi kullanıcıya seçtirilmemiş

**Sorun:** §9.2'deki S4 satırı yalnız "USD bazında belirgin negatif" diyor.

**Hesap:**
- Çekirdek ayda ~%2,6–3 TL kazanır; kur birkaç haftada +%15–30 çıkar → USD bazında **−%10…−%21.**
- S3'te (kurun artış hızı ayda %2,5–3; [TM] §5.2) USD bazında ~0.

**Düzeltme:**
> "§0 m.9 ve §9.2'ye 'USD karşılığı' sütunu eklenir. Kullanıcı ölçü birimini yazılı seçer: TL engeli ya da USD.
>
> USD seçilirse plan yanlış ölçüte göre kurulmuş demektir. Koruma iki yolla alınabilir, ikisi de pahalı:
> - korunan nominal üzerinden yılda ~13 puan carry primi ([TM] §4.3);
> - OTM USDTRY call: Aralık C56000 nominalin %0,56–0,80'i ([TM] §4.3: 'pahalı').
>
> Planın kendi kanıtı korumayı önermez. Risk bilinçli olarak kabul edildi diye yazılır."

### B9. KÜÇÜK: K1'de tek bacakla gece taşınabiliyor

**Sorun:**
- §3 K1'e göre 18:08'de yalnız bir bacak dolmuşsa o bacak ertesi gün kapatılır. Bu, bir gece ve bir gün boyunca yönlü %7,5 nominal taşımak demektir.
- Tek bacak çoğunlukla diğer bacak limitte kilitliyken oluşur. Spot kilit günlerinin %83'ünde VİOP da kilitli ([PL] §2).

**Düzeltme:**
> "(i) 17:50'de bacaklardan biri günlük ±%9 ya da daha fazla hareket etmişse o gün giriş yapılmaz. Sinyal ertesi kapanışta yeniden değerlendirilir.
>
> (ii) 18:08'de yalnız bir bacak dolmuşsa, 18:10'a kadar dolan bacağın β × nominali kadar ters yönde F_XU030 açılır. Bu hedge bankalarda ve SAHOL'de 1–3 günlük varyansı ~%41–44 azaltır ([PL] §3). Ertesi gün 17:55'te bacak ve hedge birlikte kapatılır."

### B10. KÜÇÜK: KAPALI rejimde spot uydu tavanı ile kolların azami boyları çelişiyor

**Sorun:**
- Spot uydu tavanı %15.
- Oysa kolların azamileri toplanınca ~%24–28 ediyor: K3 3 × %3,5 = %10,5 (5 mn TL ve üstünde 3 × %5 = %15), K4 2 × %1,67 = %3,3, K5 ≤ %10.
- §5'teki öncelik sırası yalnız risk bütçesi için yazılmış, nominal tavanı için değil.

**Düzeltme:**
> "Yeni bir giriş spot uydu nominal tavanını aşacaksa, giriş §5'teki öncelik sırasına göre reddedilir. Açık pozisyon küçültülmez."

### B11. KÜÇÜK: Uygulanamayan ya da belirsiz maddeler

| # | Madde | Sorun | Düzeltme |
|---|---|---|---|
| a | §10: "Bilanço açıklamayan bir isimde K4 tetiği gelirse Salı kapanışına emir" | 9.11 18:15'e kadar bilançosu gelmemiş isim o gece açıklar. Madde ortak bilanço kuralına aykırı | "Bilançosunu 9.11 18:00'den önce KAP'ta açıklamış isim." AHGAZ ve ENERY A1 listesinde yok; durumları KAP'tan teyit edilir |
| b | A9: "fon payı / fiili dolaşım ≥ %8" | %8 sınırı fon başınadır (aynı kurucuda 2 kat); toplam pay uyum satışı anlamına gelmez ([VP] T7). Veri kaynağı yazılmamış | Kaynak: fonoloji/spk-tasfiye ve KAP pay sahipliği ([TP] §4.5(b)). Rapor yayımlamayan fonlarda ~24,9 mr TL bilinmeyen pozisyon var. Bu yüzden VİOP-47 dışı bir isimde veri yoksa sonda yarım boy |
| c | A9: gerekçe "SAHOL arzı" | Blok listesinde SAHOL yok. AKBNK 2,28 mr TL ile listede, sermayenin %1'inin altında ([TP] §4.5(b)) | Kural kalır, gerekçe düzeltilir |
| d | K1 Kasım bacakları "en geç 25.11" | Doğru. Ama 21–23.12 Aralık devri ile 31.12 stopaj değişikliği aynı haftaya düşüyor | Takvime "Aralık bacakları 23.12 kapanışına kadar Ocak/Şubat'a devredilir ya da kapanır" yazılır (§7.4'te var; A10'a da eklenir) |

---

## 3. Testi geçen kurallar (değiştirilmemeli)

- **Kural 0:** Faizsiz teminatla VİOP kolu açılmaz.
- **Mevduat dilimleri bozulmaz; kredili spot hiçbir rejimde yok.** Yol A ve C'nin en ucuz frenleri bunlar.
- **K6 kapısı ve "brüt rezerv ≥ 160" koşulu:** Pazartesi carry açılmaması doğru. 0,10x boyutla +%30 kur şoku hesabın ~%3'ü.
- **Dışlama listesi** (SPK suç duyurusu, fon payı > %20, Tera/Pusula/Hedef grubu, VBTS): Yol B'deki pump kuyruğunu keser ([VB] #28).
- **Ölçü ve tavanlar:** R_fazla ölçü birimi; stres tavanı; Blok 1 sayımı; KAPALI'da K4'ün yalnız sonda olması.
- **Çift kollarının piyasa-nötr sayılması:** SAHOL ve AKBNK aynı korelasyon kümesinde (ρ ~0,83, [PL] §3). Çift, bloğun içinde doğal bir hedge.

## 4. Pazartesi'ye etkisi

| Ne zaman | Yapılacak |
|---|---|
| Cuma akşamı / hafta sonu | B7'ye göre aracı kurum seçimi teyit edilir; aracı kuruma 11. ve 12. sorular eklenir; eski sinyallerde açık pozisyon varsa kapanış takvimi yazılır (B2) |
| Pazartesi 9.11 | Değişiklik yok: yalnız çekirdek |
| Salı 10.11 | Sinyal varsa giriş Perşembe 12.11 değil, SPK kararından sonraki ilk kapanış (B4) |
| 12.11 14:30 | Rezerv verisi B5 (d) tetiğiyle de okunur: ikinci hafta ≤ −5 mlr $ ise KRİZ |
