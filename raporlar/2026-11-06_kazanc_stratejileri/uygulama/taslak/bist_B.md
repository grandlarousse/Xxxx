# Plan B: Rejim + carry + zorunlu akış olayları (BIST spot ve VİOP, başlangıç Pazartesi 9.11.2026)

Taslak, Cuma 06.11.2026, ~14:00 TSİ. Fiyatlar aksi yazmadıkça 05.11.2026 kapanışı ve resmi VİOP uzlaşması (`viop_20261105.csv`). Yatırım tavsiyesi değildir. Kaldıraçlı türevlerde sermayenin tamamı, teminat tamamlamayla daha fazlası kaybedilebilir. Olasılıkların hepsi öznel tahmindir.

**Kaynak kısaltmaları.** Yollar `raporlar/2026-11-06_kazanc_stratejileri/` klasörüne göredir.

| Kısaltma | Dosya |
|---|---|
| [MAKRO] | `ajanlar/tr_makro_engel.md` |
| [SWING] | `ajanlar/bist_swing_kenarlar.md` |
| [TEST] | `ajanlar/bist_test.md` |
| [DALGA] | `ajanlar/dalga_bist.md` |
| [PROF] | `ajanlar/tr_profesyonel.md` |
| [KİM] | `ajanlar/bist_kim_kazaniyor.md` |
| [ŞEYTAN] | `ajanlar/seytan_taban_oranlar.md` |
| [ARZ] | `ajanlar/olay_halka_arz.md` |
| [V-BIST] | `dogrulama/v_bist.md` |
| [V-ÇAP] | `dogrulama/v_capraz.md` |
| [V-DAL] | `dogrulama/v_dalga.md` |
| [V-PROF] | `dogrulama/v_profesyonel.md` |
| [HAZ] | `uygulama/bist_hafta_hazirlik.md` |
| [TARAMA] | `uygulama/tarama/bist_tarama_20261105.md` / `.csv` |
| [KOMİTE] | `../2026-10-28_viop_komite_raporu.md` |
| [PRATİK] | `../2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md` |
| [BÜLTEN] | Borsa İstanbul VİOP günlük bülteni 05.11.2026, https://www.borsaistanbul.com/data/vadeli/viop_20261105.csv (bu taslak için ayrıştırıldı) |
| [SPK] | SPK bültenleri 2026/58, 2026/59, 2026/71, 2026/78 (doğrulama ajanının indirdiği metinler, bu taslak için okundu) |

Doğrulama dosyaları raporlarla çeliştiğinde doğrulama esas alındı. `olay_bedelsiz.md`, `olay_akis_rejim.md` ve `v_olay.md` bu taslak yazılırken klasörde yoktu. Geldiklerinde §2-K5 ve §3 güncellenmeli.

---

## 0. Özet: plan tek tabloda

**Mantık.** 2024–26'nın pozitif reel faiz rejiminde hiçbir uzun hisse yapısı vergi sonrası TL nakdi geçemedi. Kanıtlar:
- [SWING §10]: 2024, 2025 ve 2026'da hiçbir uzun hisse yapısı nakdi geçmedi.
- [DALGA §0.4]: 456 küme kuralının 0'ı geçti.
- [TEST §0]: 36 kırılım varyantının 2024–26 medyanı rf'ye eşit. [V-BIST §2.1]'deki düzeltilmiş rf serisiyle 2–8 puan altında.
- [PROF §0]: 3 yılda 91 hisse fonundan 1'i PPF'yi yendi.

Bu yüzden Plan B'de sermayenin çoğu **engeli kazanan araçta** durur. Risk yalnız şu üç durumda alınır:
1. Rejim tetikleri ateşlendiğinde.
2. Önceden görülebilen zorunlu akış veya takvim olayı geldiğinde.
3. Opsiyon fiyatı gerçekleşen oynaklığın belirgin altındaysa.

Para piyasası fonu (PPF) dahil "risksiz" engel aracı gerçekten risksiz değil (§1.2). Engeli kazanan çekirdeğin üstündeki her kol, **sıfırın üstünde fazla getiri** üretmek zorunda [ŞEYTAN §3.1].

| Kol | Ne | Bugünkü durum (5–6.11 verisi) | Pazartesi 9.11 eylemi | Tavan (sermayenin %'si) | Dürüst beklenti |
|---|---|---|---|---|---|
| **Çekirdek** | 32 gün TL mevduat + banka iştiraki PPF; VİOP teminatı faizli araçla | Engel, net nominal ~%31–36 | Mevduat ve PPF yerleşimi; VİOP teminatını faizli araca çevir | ≥ %85 (bugün ~%90) | Net ~%31–36/yıl (faiz patikasına bağlı) |
| **K1 TL carry** | Short F_USDTRY1226 | **SARI** (3 sarı gösterge) | 0,05x nominal (1 mn TL'de 1 kontrat). 12.11 verisinden sonra 0,10x'e tamamlanır | 0,10x (SARI), 0,20x (YEŞİL), 0 (KIRMIZI) | 0,10x'te +0,4…+0,8 puan/yıl; şok ayında −2,5…−3,5 puan |
| **K2 Rejim tetikli long BIST** | Önce bankalar: F_XLBNK veya banka pay vadelileri, piramitle | **KAPALI** (8 tetikten 2'si) | Yok | 3 dilim × %1,25 risk; nominal ≤ 0,5x | Tetiklenir ve S1 gelirse +4…+12 puan; yanlış tetikte −1,25…−3,75 puan |
| **K3 Opsiyon (tanımlı risk)** | XU030 Aralık strangle (olay oynaklığı); tetikte call spread; K2 açıkken put spread | Zımni vol ~%18–21, gerçekleşen %32 | **O3:** P14000 + C15500 strangle ≤ 320 puan, ~%0,3 prim | Opsiyon prim bütçesi yılda ≤ %1,5 | Olay strangle'ı: zarar en fazla prim; gerçekleşen vol ≥ %21 kalırsa pozitif beklenti; güven düşük-orta |
| **K4 Zorunlu akış ve takvim** | MSCI 12.11, kredili esneklik 13.11, fon takvimi, bilanço, vade | Olay haftası | Önce kaçınma kuralları; işlemler koşullu | Olay başına ≤ %0,5 risk | Asıl değer kayıptan kaçınma; alfa n=1, kanıtsız |
| **K5 Spot olaylar** | Temettü öncesi 5 gün, bedelsiz öncesi, halka arz katılımı | Sezon dışı (temettü Mart–Haziran) | KAP taraması | Olay başına ≤ %7 sermaye | Olay başına +%0,4 fazla (temettü); halka arz yılda 10–27 bin TL/hesap |
| **K6 Mevcut mikro kenarlar** | 4 lead-lag sinyali [PRATİK] | Zayıflıyor | Sürdürülebilir, küçük | İşlem başına ≤ %0,5 risk | Plan beklentisine katılmadı |

**Plan B'nin bugün söylediği:** Hisse long yok. Küçük carry var, ama yalnız VİOP teminatı faiz kazanıyorsa. Ucuz opsiyonla olay oynaklığı alınır. Olay haftasında kaçınma kuralları geçerli.

**Beklenen sonuç (12 ay, TL, vergi sonrası; §8):** Engel artı yaklaşık 0 ile +4 puan arası. Kötü %10'luk kuyrukta engelin 5–7 puan altı. İyi %10'luk kuyrukta (S1 rejim dönüşü yakalanırsa) 12–16 puan üstü. Engelin altında kalma olasılığı ~%35–45. Engele göre beklenen en büyük düşüş −%6 ile −%10 arası. Bu plan "yüksek getiri"yi ancak S1 senaryosu (%35, öznel) gelirse ve tetikler zamanında ateşlenirse verir. Diğer senaryolarda amaç, engeli kaybetmeden opsiyonelliği korumaktır.

---

## 1. Sermaye dağılımı kararı

### 1.1 Engel ve vergi çerçevesi

| Kalem | Değer | Dayanak |
|---|---|---|
| Politika faizi / koridor | %36 / %34,5–39 (23.10'dan geçerli); sonraki PPK 10.12 | [V-ÇAP #1], [V-BIST #14] |
| Ekim TÜFE | Yıllık %29,77, aylık %2,58 (beklenti ~%2,2) | [V-ÇAP #2] |
| Reel faiz | Savunulabilir bant %5–8 (anket ex-ante %9,8 iyimser) | [V-ÇAP #3] |
| İleriye dönük net TL engeli | **~%31–36**. Faiz sabit kalırsa üst uç (32 gün mevduat roll ~%37,9); anket patikasında ~%31–33 | [V-ÇAP #4], [MAKRO §1.3] |
| Stopaj, birey | BIST spot pay ile pay/endeks VİOP %0. F_USDTRY ve diğer VİOP %10 (sözleşme sona erince). TL mevduat (≤6 ay) ve PPF %17,5. DİBS %0 yalnız 22.12.2021–30.6.2026 arası alımlar için resmi; 31.12.2026 uzatması yalnız ikincil kaynakta | [V-ÇAP #6, #7, #8], [V-BIST #15] |
| 2027 vergi riski | %17,5 mevduat/PPF ve %0 DİBS 31.12.2026'da bitiyor. Stopaj indirimi haberi teyitsiz | [V-ÇAP §2.6] |

### 1.2 Çekirdek araç karşılaştırması (5–6.11 fiyatlarıyla, birey, vergi sonrası)

| Araç | Brüt | Net (birey) | Likidite | VİOP teminatı olur mu? | Risk | Hüküm |
|---|---|---|---|---|---|---|
| **32 gün TL mevduat** (banka ortalaması, 100 bin TL) | %39,52 basit | %32,6 basit. Aylık roll ve sabit faizle bileşik ~%37,9 | Vade sonu; bozulursa faiz yanar | Hayır | Banka riski; TMSF sigorta limiti var (limit bankadan teyit edilmeli); faiz indirimiyle düşer | **Ana çekirdek** |
| **Banka iştiraki PPF** | TLREF %35,85 − ücret ~1–1,5 puan → bileşik ~%41 | ~%34 (1 yıl tutuş, stopaj bir kez); anket patikasında ~%31 | T+0/T+1 | Aracı kuruma göre (yazılı teyit) | 15 tasfiye PPF'sinden 4'ü −%95…−%99,9 kaybetti. **Yalnız büyük banka iştiraki portföy şirketi.** Tasfiyedeki 7 PYŞ (Pardus, Hedef, Atlas, Bulls, Pusula, A1, Tera) asla | **Likidite çekirdeği**: VİOP ve olay nakdi burada |
| **DİBS (2 yıl gösterge)** | %39,38 bileşik (6.11) | Stopaj %0 ise %39,4; %10 ise ~%35,4 | İkincil piyasa makası | Takasbank kabul ediyor, kesintili (aracı kurumdan teyit) | Süre riski: +300 bp ≈ −%4,5 fiyat. S4'te carry ve bankalarla aynı yönde kaybeder | **Varsayılan %0.** İsteğe bağlı ≤ %15, yalnız %0 stopaj yazılı teyitliyse ve vade ≤ 2 yılsa (bir faiz görüşüdür, engel aracı değil) |
| **XU030 cash-and-carry** (BIST30 BYF veya sepet long + short F_XU0301226) | Zımni %29,3 basit (14.734 / 14.101, 56 gün) | %29,3 (iki bacak %0 stopaj). Maliyet (~1,5–2 puan yıllık) ve boştaki teminat (aracı kurum PSR'si %20 ise ~%24) düşülmeli | Orta | — | Takip hatası; temettü | **Şu an HAYIR.** Mevduat netinin (%32,6) altında. Kural §1.5 |
| **Short F_USDTRY (carry)** | Fonlanmamış overlay; fiyatlanan yıllık kur artışı %29,3 (52,296 / 50,048) | Fazla getiri ≈ fiyatlanan − gerçekleşen kur artışı ≈ +5…+9 puan/yıl (1x); %10 stopajla +4,5…+8 | Çok likit (Aralık açık pozisyonu 1,36 mn kontrat) | — | Negatif çarpık: 2010–26 Sharpe −0,51, MaxDD −%90; 2018, 2021, 2023'te tek ayda −%25…−%35 | **Çekirdek değil, K1 overlay'i** |

Dayanaklar:
- Mevduat ve PPF rakamları: [V-ÇAP #4].
- PPF'nin riskleri: [V-BIST §3.3], [V-PROF eksik 2].
- DİBS: [HAZ §4c], [V-ÇAP #8].
- XU030 cash-and-carry: [BÜLTEN], [V-PROF T12]. Tarama dosyasındaki %23,3 rakamı **yanlış** fiyattan hesaplandı.
- Carry: [V-ÇAP #19, #5], [MAKRO §4], [SWING §8.1].

**Ters yön önemli: vadeli ucuz.** Spot hisse tutan biri için "long vadeli + nakit mevduatta" daha ucuz. Örnek bankalar, Kasım vadesi:
- GARAN: 144,45 / 142,00, 25 gün → zımni ~%25.
- AKBNK: 68,41 / 67,20 → ~%26.
- YKBNK: 37,22 / 36,52 → ~%28.

Mevduat netinin (%32,6) 5–8 puan altında [BÜLTEN]. **K2'deki bütün long pozisyonlar vadeliyle kurulur; spot hisse yalnız K5'te.**

### 1.3 Kural 0: VİOP teminatı faiz kazanmalı (bütün VİOP kollarının ön koşulu)

- **Kural.** Pazartesi 10:00'dan önce aracı kurumdan **yazılı** cevap alın:
  - (a) Kabul edilen teminat türleri: TL nakit ve nemalandırma oranı, PPF/BYF katılma payı, DİBS, hisse; her birinin kesinti oranı.
  - (b) Kurumun kendi PSR oranları: F_USDTRY, F_XU030, F_XLBNK, banka pay vadelileri, XU030 opsiyon yazımı.
  - (c) Sunucu taraflı şartlı (stop) emir var mı?
  - (d) Opsiyonda strateji/kombine emir var mı?
  - (e) Komisyon (on binde) ve BSMV.
- **Karar:**
  - Faizli teminatın getirisi politika faizinin %80'inden azsa VİOP'ta yalnız gereken teminat ve %100 tampon tutulur.
  - Teminat hiç faiz kazanmıyorsa **K1 carry açılmaz.**
  - Gerekçe: 0,10x carry'nin beklentisi yılda +0,4…+0,8 puan. QNB tipi %33,3 PSR ile boştaki teminatın fırsat maliyeti 0,033 × %33 ≈ 1,1 puan; beklentiyi aşıyor.
- **Dayanak:** [ŞEYTAN §5.1 sıra 0] (oran politika faizinin %80'inin altındaysa yapı değiştirilmeli). [V-ÇAP §2.2] (teminat nemalandırma teyit edilmeli). [V-BIST #16] (QNB 3.11: XU030 %20, pay vadelilerinin çoğu %33,3, ASTOR/HALKB/VESTL %100, GUBRF %50, USDTRY %33,3).
- **Takasbank asgari PSR:** XU030 %11,4, USDTRY %11,0, GARAN %14,4, AKBNK %15,7 (2.11'den geçerli parametreler; [HAZ §5] GM 2176, [KOMİTE] GM 2174 diyor; aracı kurumdan teyit edilmeli).

### 1.4 Dağılım (duruma göre)

| Durum | Mevduat (32 gün, ≥2 bankaya bölünmüş) | Banka PPF (likidite + olay nakdi) | VİOP hesabı (faizli teminat + tampon) | Spot olay hesabı (K5) | Risk kolları (nominal) |
|---|---|---|---|---|---|
| **Bugün** (K2 KAPALI, K1 SARI) | %55 | %30 | %10 | 0–%7 (olay yoksa PPF'de) | K1 0,05x → 0,10x; O3 ~%0,3 prim |
| **K2 PİLOT** | %55 | %30 | %10 | 0–%14 | K1 ≤ 0,10x; O1 call spread ≤ %0,5 prim |
| **K2 TAM** | %45 | %30 | %20 | 0–%14 | K2 ≤ 0,5x (3 dilim); K1 ≤ 0,05x (aynı bahis, §5); O2 put spread ≤ %0,25 |
| **Carry YEŞİL, K2 KAPALI** | %55 | %25 | %15 | 0–%14 | K1 0,20x |

- Mevduat vadeleri haftalık merdivenle (4 parça) bölünür. Böylece her hafta bir parça serbest kalır ve K2'ye geçişte faiz yanmaz.
- **Dayanak:** [SWING §10] (rejim > hisse seçimi), [MAKRO §5.3] (taban küme: küçük carry; tetikli küme: bankalar), [V-PROF eksik 1–2].

### 1.5 XU030 cash-and-carry açma kuralı (çekirdeğe alternatif)

- Her akşam bültenden hesaplanır: `i = (F_XU030 uzlaşma / XU030 spot kapanış − 1) × 365 / gün`.
- **Aç:** `i ≥ (32 gün mevduat brüt × 0,825) + 3 puan` ve teminat faizliyse. BIST30 BYF ya da 10+ hisselik BIST30 sepeti alınır, aynı kapanışta F_XU030 satılır, vadede kapanır.
- **Bugün:** i = %29,3 < %32,6 + 3 = %35,6 → **açma.**
- **Dayanak:** [V-ÇAP §2.1] (vergisiz carry kanalı ölçülmemişti), [V-PROF T12] (gerçek fark ~6,5 puan vadelinin lehine), [KOMİTE §2.3] (baz bir "avantaj" değil, TL faizinin kendisi; zımni finansman 2026'da %24–33 bandında, yapısal).
- **Beklenti:** Ancak vadeli pahalı fiyatlandığında mevduat üstüne +1…+3 puan. Yılda birkaç hafta açık kalır ya da hiç açılmaz.

### 1.6 Sermaye örnekleri

Kontrat büyüklükleri:
- F_USDTRY: 1.000 $ ≈ 52.300 TL nominal.
- F_XLBNK: 10 TL × endeks ≈ 152.400 TL (bültenden türetildi: işlem hacmi / adet / fiyat = 10).
- F_XU030: 10 TL × endeks ≈ 147.300 TL.
- XU030 opsiyon: 1 puan = 10 TL (bültenden türetildi).
- GARAN pay vadelisi: 100 pay ≈ 14.800 TL.

| Kalem | 1 mn TL | 5 mn TL | 20 mn TL |
|---|---|---|---|
| Mevduat %55 | 550 bin | 2,75 mn | 11 mn |
| Banka PPF %30 | 300 bin | 1,5 mn | 6 mn |
| VİOP hesabı %10 (faizli teminat) | 100 bin | 500 bin | 2 mn |
| **K1 Pzt 0,05x** | **1 kontrat** F_USDTRY1226 (0,052x) | **5** | **19** |
| K1 12.11 sonrası 0,10x (KIRMIZI yoksa) | 2 kontrat | 10 | 38 |
| K1 teminatı (QNB %33,3 / Takasbank %11) | 34,8 bin / 11,5 bin (2 kontrat) | 174 bin / 57,5 bin | 661 bin / 218 bin |
| K1 stresi (USDTRY +%30), 0,10x | −31 bin (−%3,1) | −157 bin (−%3,1) | −597 bin (−%3,0) |
| **O3 strangle** P14000 + C15500, ≤ 320 puan (3.200 TL/adet) | **1 adet** (%0,32) | **5** (%0,32) | **20** (%0,32) |
| K2 dilim (%1,25 risk, %8 stop): F_XLBNK | 1 kontrat (risk ~12,2 bin = %1,22) ya da 10 × F_GARAN1226 | 5 kontrat | 20 kontrat |
| K2 en çok 3 dilim | 3 F_XLBNK (~0,46x) | 15 (~0,46x) | 60 (~0,46x; Aralık hacmi 6.617, açık pozisyon 4.857 → girişi 2–3 güne yayın) |
| O1 pilot call spread (≤ %0,5; 250 puanlık spread) | 2 adet | 10 | 40 |
| O2 koruma put spread (≤ %0,25; ~75 puan) | 3 adet | 16 | 66 |
| K5 olay pozisyonu (≤ %7) | 70 bin | 350 bin | 1,4 mn (≤ 20 günlük ortalama hacmin %2'si) |
| Halka arz (hesap başına, sermayeden bağımsız) | yılda 10–27 bin TL ≈ %1–2,7 | %0,2–0,5 | %0,05–0,13 |

Not: 1 mn TL'de kontratlar tam sayılı olduğu için risk yüzdeleri tam tutmaz. K2 ve opsiyonlarda **aşağı yuvarlanır**. K1'de en yakın tam sayıya yuvarlanır (tavanın en çok %10 üstü). [KOMİTE §7.5]'e göre 1 F_XU030 ≈ %0,45–0,56 stop riski.

---

## 2. Kollar: giriş, çıkış, stop, boyut, piramit, emir

Ortak kurallar:
- Bütün kararlar **kapanışta** verilir. Kontrol penceresi 17:40–18:08 TSİ, günde ~20 dakika; gün içi ekran yok.
- Veri, Cuma akşamı ve her akşam resmi VİOP bülteninden alınır: `viop_YYYYMMDD.csv`, ~18:30 sonrası.
- Tarama dosyasındaki VİOP fiyatlama tablosu **kullanılmaz** (Ek A).

### K1. TL carry: short F_USDTRY (boyutu rejime bağlı, kuyruk stoplu)

**Ön koşul:** Kural 0 (§1.3) sağlanmış olmalı.

| Öğe | Kural |
|---|---|
| Araç | F_USDTRY1226 (vade 31.12). Kasım kontratı kullanılmaz: 30.11 MSCI ve vade aynı gün |
| Boyut | Gösterge A'ya göre (§3.1): KIRMIZI 0; ≥2 SARI ise tavan 0,10x; 1 SARI 0,15x; hepsi YEŞİL 0,20x. K2 TAM açıkken tavan 0,05x (§5). Kontrat = sermaye × x / (F × 1.000), en yakın tam sayıya yuvarlanır; sonuç tavanı en çok %10 aşabilir |
| Prim filtresi | P = (F/S − 1) × 365/gün − (son 63 işlem gününün yıllıklandırılmış USDTRY artışı, TCMB gösterge kuru). P ≥ 5 puan → tam boy; 2–5 → yarım; < 2 → açma. **Bugün:** fiyatlanan %29,3, gerçekleşen tempo ~%21–24 (Mayıs'tan beri) → P ≈ 5–8 → geçiyor |
| Giriş | Kapanış penceresinde (17:55–18:08) **limit satış**: son işlem fiyatı veya en iyi alış; önceki uzlaşmanın 0,03 TL altına kovalanmaz. Dolmazsa ertesi gün aynı kural. Pazartesi yarım boy, ikinci yarım 12.11 Perşembe 14:30 rezerv/akım verisinden sonra Gösterge A'da KIRMIZI yoksa |
| Stop (uzlaşma bazlı) | (1) Uzlaşma ≥ giriş × 1,025 ise (52,30 girişte 53,61) ertesi değil **aynı gün** 17:55–18:08'de kapat; 17:45'te son fiyat ≥ eşikse kapatma emri ver. (2) Gösterge A'da herhangi bir KIRMIZI → o gün kapanışta kapat. (3) Aracı kurum destekliyorsa felaket stopu: giriş × 1,045'te sunucu taraflı şartlı alış (günlük limit ±%10 olduğundan gap'i engellemez) |
| Hedef / çıkış | Hedef yok; vadeye kadar taşınır. 21–23.12 arasında en yüksek açık pozisyonlu bir sonraki kontrata roll (vadeler arası emir) |
| Piramit | Yok. Boyutu yalnız gösterge belirler, kâr/zarar değil |
| Yeniden giriş | Stop sonrası Gösterge A 2 hafta üst üste KIRMIZI'sız olmalı |
| Kuyruk koruması | USDTRY call yalnız prim, 2 aylık beklenen fazla getirinin %50'sinden azsa. Komitede Aralık C56000 nominalin %0,56–0,80'iydi, yani pahalı. **Bugün almayın.** XU030 put spread 2021 tipi şoku (TL çöker, nominal BIST yükselir) korumaz |
| Vergi | %10 stopaj, sözleşme sona erince (aracı kurum keser). Zarar, %0 stopajlı hisse kazancından düşülemez |

**Dayanak:**
- Ortodoks dönem (07/2023–10/2026): yıllık %20,8 USD, Sharpe ~2,2, 10/10 pozitif ay (2026) [V-ÇAP #19], [SWING §8.1].
- Tüm dönem: Sharpe −0,51, MaxDD −%90 [SWING §8.1].
- Prim daralıyor: fiyatlanan − gerçekleşen = 28 → 22 → 17 → ~13 puan [MAKRO §4.3].
- Kırılma yolları ve göstergeler [MAKRO §4.3, §5.1]; çıkış/yanlışlama listesi [KOMİTE §4.2].
- Teminat ve aylık roll gerçeği: USD teminat ~%0 kazanır, uzak vadeler likit değil [V-ÇAP §2.3–2.4].
- Boyut: stres kaybı (−%30 kur şoku) toplam sermayenin ≤ %5–10'u [ŞEYTAN §5.1 sıra 5].

**Beklenti:**
- 1x nominal başına fazla getiri yılda +5…+9 puan vergi öncesi, +4,5…+8 vergi sonrası. 0,10x'te portföye **+0,4…+0,8 puan/yıl**; 0,20x'te +0,9…+1,6.
- İsabet: ortodoks dönemde 64 günlük pencerelerin %88'i pozitif. Ancak çöküşsüz sicil SR hakkında bilgi vermez [ŞEYTAN §3.5].
- Kuyruk: 2018/2021/2023 tipi ayda −%25…−%35 (1x) → 0,10x'te −2,5…−3,5 puan. Stop limit-kilitli günlerde çalışmayabilir.
- **Güven: ORTA** (rejim sürerse). Rejim kırılırsa geçmiş Sharpe anlamsız.

### K2. Rejim tetikli long BIST, VİOP üzerinden (önce bankalar)

| Öğe | Kural |
|---|---|
| Tetik | Gösterge B (§3.2). **PİLOT:** (L1 veya L2) ve 8 tetikten ≥ 4'ü → yalnız O1 call spread. **TAM:** L1 ve L2 ve 8 tetikten ≥ 5'i → vadeli dilimler. Bugün: 2/8 → **KAPALI** |
| Araç önceliği | (1) F_XLBNK1226 (≥ 5 mn TL için). (2) 1 mn TL için eşit ağırlıkla F_GARAN, F_YKBNK, F_AKBNK, F_ISCTR Aralık vadesi. HALKB hariç: QNB'de %100 teminat. (3) 3. dilimde, havacılığın RS kırılımı sürüyorsa TAVHL veya THYAO. Holding (KCHOL/SAHOL) yalnız banka likiditesi yetmezse; SAHOL tasfiye fonlarında en çok tutulan BIST30 payı [KOMİTE §1] |
| Giriş | Tetik günü kapanış penceresinde limit alış (son fiyat + en fazla %0,2), dolmazsa ertesi gün. Spot değil vadeli (§1.2: vadeli 5–8 puan ucuz). Nakit mevduat/PPF'de kalır |
| İlk stop | Giriş × 0,92 (−%8 ≈ 3,5 günlük ATR; XBANK rv20 %35,9). 17:45'te son fiyat ≤ stop → 17:55–18:08 kapat. Sunucu taraflı felaket stopu: giriş × 0,88 |
| Boyut | Dilim başına risk sermayenin %1,25'i: kontrat = floor(sermaye × %1,25 / (F × çarpan × %8)) |
| Piramit | **Dilim 2:** pozisyon +1R (≥ +%8) ve gösterge hâlâ TAM ise ekle; dilim 1'in stopu başabaşa çekilir. **Dilim 3:** ilk girişten +2R ve XU100 kapanışı 50 GHO üstündeyse ekle. Toplam nominal ≤ 0,5x, açık risk ≤ %3,75 |
| İz süren stop | Her dilimde en yüksek uzlaşmadan %15 iz-stop (kazananı koştur) |
| Zaman stopu | 40 işlem gününde +1R'ye ulaşmayan dilim kapatılır |
| Rejim çıkışı | L1–L4'ten ≥ 2'si 2 hafta üst üste tersine dönerse bütün dilimler kapanır |
| Roll | Aralık → Şubat 2027 (F_XLBNK0227 veya ilgili pay vadelisi): 21–23.12 arasında vadeler arası emirle. Pay vadelilerinde Kasım vadesi **kullanılmaz** (30.11'de fiziki teslimat) |
| Koruma | K2 TAM açıkken O2 put spread (≤ %0,25 prim) |
| Opsiyonel karşı ağırlık | Bankalar long iken TUPRS vadelisi long, banka nominalinin 1/3'ü kadar; yalnız TUPRS 50 GHO'yu geri almışsa. Fazla getiri korelasyonu banka ile −0,42. **Test edilmiş bir kural değil; güven düşük** |

**Dayanak:**
- Rejim kırılma anlarında bankalar dolar bazında 3–5 ayda +%40…+%90 (n=4). Hareketin yarısı ilk 4–8 haftada. Öncül sinyaller: reel faiz sıçraması, BIST $ döngü dibi, CDS dönüşü, yabancı payı dipte [MAKRO §2.1, §2.3].
- Ortodoks dönem betaları: AKBNK 1,38, GARAN 0,99, YKBNK 1,03 [MAKRO §3.3].
- Koşulsuz dip avcılığı reddedildi: 22 benzer olayda 63 gün medyanı +%2,9, carry'nin altında [KOMİTE §2.2], [MAKRO §5.3].
- %15 iz-stop ile kazananı koşturma [TEST §5.1]: işlem başına rastgele hisseye göre +%5,3, t 5,1; kârın %70'i en iyi %5 işlemde. Bu tekil hisse kanıtı; endeks vadelisine uyarlama varsayım.
- Banka/holding/havacılık tek risk bloğu, korelasyon 0,77–0,79 [DALGA §5], [V-DAL B12].

**Beklenti:**
- Tetik doğru ve S1 gerçekleşirse: tetik gecikmesiyle ilk %5–10 kaçar; ortalama 0,3–0,47x nominalle **+4…+12 puan**.
- Yanlış tetik: 1 dilim stop = −1,25 puan, 3 dilim = −3,75 puan.
- İsabet ölçülmedi. n=4 tarihsel örnek; hayatta kalan ve dönem seçimi yanlılığı yüksek. **Güven: DÜŞÜK-ORTA.**

### K3. Tanımlı riskli XU030 opsiyonları (likit seriler)

**Likidite kuralı:** Yalnız açık pozisyonu ≥ 1.000 olan ve önceki gün ≥ 5 işlem görmüş seriler. Limit fiyat ≤ önceki uzlaşma. Bültende alış/satış makası yok, kovalanmaz. Bacaklar ayrı limit emirle girilir:
1. Önce **alınan** bacak.
2. Spread ise sonra satılan bacak.
3. Satılan bacak aynı gün dolmazsa ertesi gün tamamlanır. Sonuç pozisyon her zaman tanımlı risklidir.

Opsiyonlar Avrupa tipi ve nakdi uzlaşmalıdır. Vade sonu kesinleşme fiyatı: son 30 dakikanın ağırlıklı ortalaması × %80 + kapanış × %20 [HAZ §5].

**5.11 durumu [BÜLTEN; bu taslağın Black-76 hesabı, F = 14.734, TLREF %35,85]:**
- Uzlaşma fiyatlarının zımni vol'ü %17–22. İşlem kapanışlarının zımni vol'ü %12–21 (eşzamansız, gürültülü).
- XU030 20 günlük gerçekleşen vol %32,4 [TARAMA].
- Açık pozisyonu yüksek seriler: C14250 28.039, C14500 16.598, C15000 8.482, P15500 23.800, P15000 15.144, P13250 3.651, P14000 1.860 (5.11'de 1.052 adet işlem).

| Yapı | Ne zaman | Seri (bugünkü örnek) | Fiyat sınırı | Boyut | Çıkış | Dayanak | Beklenti |
|---|---|---|---|---|---|---|---|
| **O3 olay oynaklığı strangle** | **Bugün koşul sağlanıyor:** strangle fiyatının zımni σ'sı ≤ %21 ve XU030 RV20 ≥ %28 | Long P14000 + long C15500, Aralık | Toplam ≤ 320 puan (uzlaşma 137,4 + 174,1 = 311,6). Ayrı ayrı P ≤ 140, C ≤ 180 | Sermayenin ~%0,3'ü (1 / 5 / 20 adet) | Değer ≥ 640 (2×) → yarısını sat. Değer ≤ 160 → hepsini kapat. **En geç 15.12 kapanışı** (10.12 PPK sonrası, zaman değeri çöküşünden önce). Emir 12.11 kapanışına kadar geçerli, dolmazsa iptal | [KOMİTE §2.4, §4.1]: vol satmak için gerekçe yok, ≤ 800 puanlık straddle'da avantaj ~%25–35; Black-76 ile adil değer bu taslakta σ %25'te ~490, %32'de ~750, %18'de ~250 puan. Karşı kanıt: ABD'de opsiyon alıcısının ortalaması negatif [V-PROF A6]; BIST'te vol primi test edilmedi [SWING §8.3] | Zarar en fazla prim (%0,3). Önümüzdeki 5 haftada gerçekleşen σ ≥ ~%21 olursa pozitif. Katalizörler: 12.11 MSCI ve TCMB raporu, 13.11 kredili esneklik, 3.12 TÜFE, 10.12 PPK. **Güven: DÜŞÜK-ORTA** |
| **O1 pilot call spread** | Gösterge B = PİLOT | Vade ≥ 45 gün. 15.11'den önce: Aralık C15000/C16000 (uzlaşma 243 puan, en çok 1.000 → 4,1:1). Sonrası: Şubat C15750/C17250 (uzlaşma ~399, en çok 1.500 → 3,8:1). Uzun bacak forward'ın ~%2 üstü, kısa bacak ~%9–12 üstü | ≤ uzlaşma | ≤ %0,5 prim | Değer, azami değerin %70'ine ulaşınca kapat. Vadeye 10 gün kala kapat. Gösterge TAM'a geçerse vadeli dilime dönüştürme serbest | [MAKRO §5.2] (S1'e "call spread tercih"), [KOMİTE §1] (makro kapılı long F_XU030 tetiklenirse call spread) | Tetik doğruysa prim × 2–4, yanlışsa −%0,5. **Güven: DÜŞÜK-ORTA** |
| **O2 koruma put spread** | Yalnız K2 TAM açıkken (bugün değil) | Spotun ~%1 altı / ~%7 altı. Bugünkü örnek: Aralık P14000/P13250 (uzlaşma 75 puan, en çok 750 → 10:1) | ≤ uzlaşma | ≤ %0,25 prim; aylık yenilenir | Vadeye kadar ya da K2 kapanınca | [KOMİTE §4.3] (put spread gap, limit ve sıkışma riskinden korur), [V-ÇAP §2.8] (carry ve tetikli banka aynı kuyrukta) | Sigorta: K2'nin −%20'lik gap stresinin ~1/4'ünü karşılar. Beklenen değeri negatif |
| **Yapılmayacaklar** | — | Çıplak opsiyon satışı, kısa vadeli OTM call (piyango), USDTRY call (pahalı) | — | 0 | — | [SWING §8.3], [ŞEYTAN §5.1] (SEBI'de opsiyon alıcıları en kötü grup, 0DTE), [KOMİTE §4.2] | — |

**Yıllık opsiyon prim bütçesi ≤ %1,5.** Bütçe aşılırsa yıl sonuna kadar yeni opsiyon alınmaz.

### K4. Zorunlu akış ve takvim olayları

Bu kolun asıl getirisi **kaçınılan kayıptır**. Zorunlu satıcının karşısında olmak literatürde yüksek getirili (Coval-Stafford [ŞEYTAN §5.1 sıra 2]). Ancak BIST'te tek gözlem var (28.08 kuralı → XU030 −%20, n=1; [V-BIST #10], [KİM §5]). Kısa vadede "düşeni almak" BIST'te para kaybettiriyor: REV, EW'ye göre yılda −%17,9 [TEST §4]; haftalık kaybedenler 30–70 bps/hafta geride [SWING §3.3]. Bu yüzden olay sonrası **dip alımı yok**; işlem kuralları koşullu.

| Olay | Tarih ve saat (TSİ) | Mekanizma | Kural | Dayanak | Beklenti / güven |
|---|---|---|---|---|---|
| **Konsolide 3Ç son günü** | Pzt 9.11 akşamı KAP (KCHOL, BIMAS, PGSUS, TCELL, SOKM, DOAS, AKSEN, ALARK; tarihsizler EREGL, ARCLK, KRDMD, ASTOR, GUBRF, HEKTS, OYAKC, CIMSA, ENJSA, TKFEN, TRALT, TRMET, EKGYO, VESTL, ODAS). Bankalar konsolide 19.11 | Salı açılışında bilanço gap'i | (1) 9.11 akşamı, açıklama yapacak isimlerde pay vadelisi veya spot taşınmaz (K6 dahil). (2) PEAD yalnız kâğıt üstünde kayda alınır: sürpriz yönü, Salı kapanış fiyatı ve 60 gün sonraki fark | [HAZ §2], [SWING §5.8] (PEAD L/S %2,9/60 gün, doğrulanamadı [V-BIST #21]) | Kaçınma. PEAD gerçek parayla yok |
| **MSCI Kasım gözden geçirme** | Duyuru Per 12.11 01:00; yürürlük Pzt 30.11 kapanışı | Artışlar donduruldu, azaltmalar ve çıkarmalar sürüyor → pasif akış asimetrik negatif | (1) 12.11 sabahı MSCI bülteninde Türkiye bölümü okunur. (2) Çıkarılan veya FIF/NOS'u düşürülen VİOP-47 hissesi "30.11 kapanışına kadar long yok" listesine girer; K2'de tutuluyorsa 12.11 kapanışında çıkılır. (3) Kâğıt üstünde: çıkarılan likit isimler 30.11 kapanış seansında alınır, 3–5 gün tutulur (literatür: BIST30'dan çıkanlarda yürürlük sonrası +%1,1, t 2,04, 2009–17, doğrulanamadı) | [V-ÇAP #17], [HAZ §0.4], [SWING §5.7], [V-BIST #21] | Kaçınma. Çıkış dönüşü yalnız kâğıt üstünde, n ≥ 10 olunca değerlendirilir |
| **Kredili işlem esnekliğinin bitişi** (özkaynak %20 → %35) | Cum 13.11 seans sonu. Karar 12–13.11 SPK bülteninde | Uzatılmazsa 16.11'den itibaren teminat tamamlama ve zorla satış; orta-küçük ölçek. Komite tahmini 2,8–8,5 mlr TL, günlük hacmin %3–8'i | Uzatma 3/3 kez geldi: 02.10, 30.10, 13.11 [V-BIST #7]. **Uzatılırsa:** eylem yok. **Uzatılmazsa:** (1) 27.11'e kadar BIST30 dışı spot long yok (K5 dahil). (2) 16–20.11'de düşen hisse alınmaz. (3) Gösterge B'de L6 = ✗; XUTUM'un 5 günlük getirisi 10 iş günü boyunca −%7'nin altına inmezse ✓ | [SPK 2026/78], [KOMİTE §3], [TEST §4], [SWING §3.3] | Kaçınma. Alfa iddiası yok |
| **BIST30 blok satışları** | 03.11 kapanış fiyatıyla fonlara devir; alıcıya 3 ay satış ve türev yasağı → kilit ~03.02.2027'de açılıyor | Şubat başına kadar BIST30'da arz azalır, sonra arz riski | K2 TAM açık ve L3 (yabancı alımı) ✓ değilse, 29.01.2027 kapanışına kadar Blok 1 nominali yarıya iner. Fonolojiye göre likit tasfiye kalemleri: YKBNK 3,10, THYAO 3,07, AKBNK 2,28, ASELS 2,26, TUPRS 1,90, EREGL 1,58 mlr TL | [PROF §4.5(b)–(c)], [V-PROF T8] | Kaçınma; etki ölçülmedi |
| **Fon yoğunlaşma uyumu** | Tek son tarih 31.01.2027 (SPK 75/1897) | BIST30 dışı paylarda fon başına %8/%6/%4/%2 sınırı → uyum satışı | 31.01.2027'ye kadar evren BIST30 ve VİOP-47 ile sınırlı (K5 dahil). İstisna: fon payı / fiili dolaşım < %8 olduğu KAP/MKK verisiyle gösterilen hisse | [PROF §4.5(c)], [V-PROF T7] (sınır fon başına; toplam %8'i aşmak tek başına uyum satışı demek değil) | Kaçınma |
| **Tasfiye azami süresi** | ~17.03.2027 | Likit olmayan tasfiye hisselerinde arz | Dışlama listesi (§4.2) en az bu tarihe kadar geçerli | [PROF §4.5], [V-PROF T5] (bilinen pozisyon 46,4 mr TL) | Kaçınma |
| **VİOP Kasım vadesi** | Pzt 30.11 (pay vadelilerinde fiziki teslimat, kesinleşme spot kapanış) | Teslimat ve MSCI aynı gün | Plan B Kasım vadeli taşımaz. K6'da Kasım pay vadelisi varsa 26.11 kapanışına kadar kapatılır ya da roll edilir | [HAZ §1b, §5] | Kaçınma |
| **Zorunlu pay alım teklifi (ZPAT)** | Ağu–Eki bültenlerinde 13 atıf | Türk uygulamasında teklif, kontrol devrinin **kamuya açıklandığı tarihte pay sahibi olanlara** yapılıyor (PEKGY kararlarındaki ifade; SPK 2026/58, 2026/71). Sonradan alan hak kazanmaz | **İşlem yok.** AKCNS'de SPK 2026/59 (16.09) Heidelberg'in 260,25 TL ile 5,627434 $ karşılığının yükseği üzerinden ZPAT bilgi formunu onayladı. Hisse 176–190 TL'de. Fark büyük olasılıkla bu hak sahipliği kuralından ve/veya takvimden kaynaklanıyor. KAP'taki bilgi formunda "kimler katılabilir" ve tarihler okunmadan işlem yok. Karşı taraf riski: Tera, PEKGY ZPAT'ını yerine getirmedi (SPK 2026/64, 2026/71) | [SPK], [V-BIST §3.4] | Çalışılmadı; yok sayılır. Gönüllü teklifler (ör. SPK 2026/56'da Atlantis için 104 TL) yalnız kâğıt üstünde |

### K5. Spot olaylar (yalnız spot; VİOP temettüyü fiyatlıyor)

| Olay | Giriş | Çıkış | Filtre | Boyut | Dayanak | Beklenti |
|---|---|---|---|---|---|---|
| **Temettü öncesi** | Hak kullanım gününden 5 işlem günü önce, **kapanış seansında** (18:00–18:10) limit alış: son fiyat +%1 (tek fiyattan eşleşir) | Hak kullanımından önceki gün kapanış seansında limit satış (son fiyat −%1). Temettü alınmaz. Kuyruk çıkışı: kapanış ≤ giriş × 0,93 ise ertesi kapanışta sat | BIST100 üyesi; dışlama listesinde değil; brüt temettü verimi ≥ %2 (testteki k > 1,02); pozisyon ≤ 20 günlük ortalama hacmin %2'si | ≤ %7 sermaye/olay; aynı anda ≤ 3 olay (%21). ≥ 5 mn TL'de isteğe bağlı β × nominal F_XU030 short ile piyasa riski atılır (aynı hissenin vadelisiyle değil) | [SWING §5.3] (n=1.109, [−5,−1] +%1,2, t 7,8; [+1,+5] −%0,6), [V-BIST #26] (haftalık kümelemede t 6,5; 17 yılın hepsinde ortalama pozitif; medyan 2014 ve 2026'da negatif; maliyet sonrası ≈ %0,9), [PRATİK §2] (VİOP'ta yok) | Olay başına brüt +%1,2, medyan +%0,8, maliyet sonrası ~+%0,9. 5 günlük engel kaybı (~%0,5) düşülünce **~+%0,4 fazla**. Sezon Mart–Haziran; Kasım–Aralık'ta az olay. Yılda +0,3…+0,8 puan. **Güven: ORTA-YÜKSEK** (büyüklük küçük) |
| **Bedelsiz öncesi** | SPK onayının bültende yayımlandığı günden sonraki ilk kapanış seansı; hak kullanımına ≥ 3 işlem günü varsa | Hak kullanımından önceki gün kapanış seansı. **Asla sonrasına taşınmaz** | Likit üst yarı (20 günlük ortalama hacim ≥ 100 mn TL); dışlama listesinde değil; oran ≥ %100 | ≤ %5 sermaye/olay | [SWING §5.1]: n=410; [−20,−1] +%2,8 (t 3,7); [−5,−1] +%1,2 (t 2,9); 2023–26 [−5,−1] +%2,2 (t 3,2); likit üst yarı [−20,−1] +%2,5 (t 2,2), [−5,−1] +%0,9 (t 1,5); [+1,+5] −%2,0; 60 gün medyan −%5,3 | Likit isimlerde olay başına brüt +%0,5…+%1,5. "Bedelsiz sonrası yükselir" folkloru verilerde yok. **Güven: DÜŞÜK-ORTA** |
| **Halka arz katılımı** | Yalnız eşit dağıtımlı arzlar; talep PPF teminatıyla (bloke 2–3 gün) | Her akşam: hisse tavanda (kilitli) **kapanmadıysa** ertesi sabah açılış seansına (09:40–09:55) limit satış (önceki kapanış −%3). Seri sürüyorsa tut | Kilit dışı; dışlama yok | Hesap başına; aile hesapları doğrusal ölçekler | [ARZ §0, §3b]: arz başına medyan +%45, yılda 10–27 bin TL/hesap. 3 Eylül'den beri yeni onay yok [HAZ §1a] | 1 mn TL'de yılda +1…+2,7 puan, 20 mn TL'de ~0. **Seri bittikten sonra alım yok:** 21 gün medyanı −%11 [ARZ §0]; 2025–26'da 53 arzın ~50–52'si düştü [V-BIST #11]. Kilit bitişinde etki yok [ARZ §7] |

### K6. Mevcut mikro kenarlar (overlay; plan beklentisine katılmadı)

[PRATİK §1]'deki dört sinyal (XU030 baz sıçraması, SAHOL/AKBNK, Koza göreli momentum, ABD rafinerileri → TUPRS) şu sınırlarla sürdürülebilir:
- İşlem başına risk ≤ %0,5.
- K6 toplam açık risk ≤ %1.
- Bilanço günü kuralı (K4) geçerli.
- Kasım pay vadelisi 26.11'e kadar kapatılır.

Dördü de 2024–26'da zayıflıyor [PRATİK §5]. SAHOL/AKBNK'nın 20 günlük sürümü bir gün gecikmeli girişle işlem başına +160/+310 bps (t 2,4/2,8); maliyet sonrası 88–290 bps [V-BIST #25]. Öldürme kuralları [PRATİK] ve §7 ile aynı.

### 2.7 Plan B'nin bilerek yapmadıkları

| Yapılmayan | Neden |
|---|---|
| Kesitsel 12-1 momentum, kısa vadeli dönüş, "düşeni al" | BIST'te başarısız: MOM EW'ye göre −%5,6/yıl, REV −%17,9/yıl [TEST §4] |
| Endeks SMA trend kuralları | Değer katmıyor; placebo 0,18–0,52 [TEST §2] |
| Koşulsuz long ya da short endeks (çıplak short F_XU030 dahil) | Komite her iki yönü de reddetti [KOMİTE §8]. TSMOM L/S 2026'da +%7'ye karşı nakit %31 [SWING §4] |
| Sektör rotasyonu, küme RS rotasyonu, kırılım portföyü | 2024–26 her yıl rf'nin altında [TEST §3], [V-DAL §5]. Kırılımda kârın %70'i pump hisselerinden [V-BIST #28]. Plan A'nın konusu; B'de yalnız aday filtresi olarak (§4.3) |
| Kredili spot | Örtük maliyet ≈ %60 [V-BIST #3] |
| Opsiyon satışı | Veri yok; çöküşte yıkıcı [SWING §8.3] |
| Overhang/pump hisselerinde "dipten tepki" | Negatif çarpık; arz Mart 2027'ye kadar [PROF §6] |

---

## 3. Rejim anahtarı: eşikler, bugünkü okuma, gün gün plan

Değerlendirme takvimi:
- Göstergeler **her Perşembe 14:30** TCMB verisinden (rezerv ve haftalık menkul kıymet), **her ayın 3'ü 10:00** TÜFE'den ve her ay sonunda güncellenir.
- CDS ve USDTRY her akşam bakılır.
- Eylem aynı günün kapanış penceresinde alınır.

### 3.1 Gösterge A: TL istikrarı (K1 carry boyutu)

| # | Gösterge (veri kaynağı) | YEŞİL | SARI | KIRMIZI | 5–6.11 değeri | Bugün |
|---|---|---|---|---|---|---|
| A1 | Swap hariç net rezerv, haftalık (TCMB Per 14:30) | Değişim > 0 | Tek hafta ≤ −5 mlr $ | Seviye < 0 **veya** 2 hafta üst üste ≤ −5 mlr $ | 24,3 mlr $ (önceki hafta 30,8 → −6,5) | **SARI** |
| A2 | Yabancı DİBS, haftalık (TCMB menkul kıymet) | > −250 mn $ | −250 mn $ … −1 mlr $ | 2 hafta üst üste ≤ −1 mlr $ | −750,4 mn $ (Nisan'dan beri en büyük) | **SARI** |
| A3 | Brüt rezerv | ≥ 160 mlr $ | < 160 mlr $ | Haftada > −10 mlr $ düşüş | 158,1 mlr $ (önceki hafta 162,2) | **SARI** |
| A4 | CDS 5 yıl | < 250 | 250–300 | > 300 | ~248 | YEŞİL (sınırda) |
| A5 | USDTRY 10 iş günlük tempo, yıllık (TCMB gösterge kuru) | < %25 | %25–35 | > %35 | ~%21–24 (Mayıs'tan beri; son 3 hafta ~%24) | YEŞİL (sınırda; Pazartesi TCMB XML'den hesaplanmalı) |
| A6 | 1 aylık F_USDTRY zımni TL faizi − politika faizi | < +2 puan | +2…+5 | > +5 (kaçış fiyatlanıyor) | Kasım ~%32,3 − %36 = −3,7 | YEŞİL |
| A7 | Siyasi/hukuki şok: erken seçim kararı, butlan davasının yeni aşaması, TCMB yönetim değişikliği, haftalık repo ihalesinin durdurulması | Yok | — | Herhangi biri → açılışta değil, o günün kapanışında çık | Yok | YEŞİL |

**Kural:** Herhangi bir KIRMIZI → 0. ≥ 2 SARI → 0,10x. 1 SARI → 0,15x. Hepsi YEŞİL → 0,20x.
**Bugün:** 3 SARI → tavan **0,10x**. Pazartesi 0,05x açılır, kalanı 12.11 verisine bağlı.

Dayanak: [MAKRO §5.1] gösterge panosu (carry'den çık tetikleri), [KOMİTE §4.2] (brüt rezerv < 160, 10 günlük kur hızı > %35, repo ihalesi, CDS > 300, siyasi şok), [V-ÇAP #18] (rezerv ve akım rakamları).

### 3.2 Gösterge B: long BIST (K2)

| # | Tetik | Eşik (✓ için) | 5–6.11 değeri | Bugün |
|---|---|---|---|---|
| **L1** (zorunlu, TAM için) | Swap hariç net rezerv | 3 hafta üst üste artış | Düşüyor (30,8 → 24,3) | ✗ |
| **L2** (zorunlu, TAM için) | Aylık TÜFE | < %2,0 (son açıklanan) | %2,58 (Ekim); sonraki 3.12 | ✗ |
| L3 | Yabancı hisse akımı | 2 hafta üst üste net alım ve toplam ≥ +200 mn $ | Son 6 haftada −334,5 mn $ | ✗ |
| L4 | CDS 5 yıl | < 230 ve 20 günlük ortalamasının altında | ~248 | ✗ |
| L5 | Fiyat | XLBNK **ve** XU100 kapanışı 50 GHO üstünde | XLBNK +%0,7 ✓; XU100 −%10,7 ✗ | ✗ |
| L6 | Akış/regülasyon | Kredili esneklik uzatıldı ya da bitişinden sonraki 10 iş günü XUTUM'un 5 günlük getirisi −%7'nin altına inmedi; son 4 haftada yeni fon temerrüdü veya SPK kapsam genişletmesi yok | 13.11 bekleniyor | ✗ (beklemede) |
| L7 | Reel faiz | Ex-ante reel faiz > +%5 ve TCMB baskısız kademeli indiriyor | +%9,8 anket (savunulabilir %5–8); Ekim'de −100 bp | ✓ |
| L8 | Değerleme/döngü | BIST100 dolar bazında < 240 (2023–26 bandının dibi) | ~226,5 (bant 215–340) | ✓ |

**Kural:**
- **PİLOT** = (L1 veya L2) ve ≥ 4/8 → yalnız O1.
- **TAM** = L1 ve L2 ve ≥ 5/8 → K2 dilim 1.
- **ÇIKIŞ:** L1–L4'ten ≥ 2'si 2 hafta tersine dönerse.

**Bugün: 2/8 → KAPALI.**
- En erken PİLOT: 26.11. Koşul: 12.11, 19.11 ve 26.11 rezervlerinin üçü de artış göstermeli ve 2 tetik daha eklenmeli.
- En erken TAM: 3.12 kapanışı (Kasım TÜFE < %2,0 ve L1).

Arka plan göstergeleri:
- XU100 TSMOM12: 12 ay +%3,8'e karşı nakit +%37 → **KAPALI**. Açılması için XU100'ün ~15.000'e çıkması gerekir; haftalar içinde ilgisiz.
- Küme filtresi: BANKA ve HAVACILIK'ta 126 günlük RS zirvesi var, ama hiçbir kümede mutlak momentum (6 ay TL > rf) yok; filtreli kurallar nakitte.

Dayanak:
- [MAKRO §5.1–5.3] (9 tetikten ≥ 4; rezerv artışı ve TÜFE < %2 zorunlu).
- [V-ÇAP #3] (reel faiz bandı), [V-ÇAP #20] (BIST $), [SWING §4] (TSMOM12 kapalı), [DALGA §5], [V-DAL B12] (küme durumu).
- Senaryolar ve öznel olasılıklar: S1 sönümlenme %35, S2 yatay kanama %40, S3 kontrollü hızlanma %15, S4 kırılma %10 [MAKRO §5.2].

### 3.3 Bugünkü hüküm

| Kol | Durum | Pazartesi |
|---|---|---|
| Çekirdek | Engel ~%31–36 net | Yerleştir (§1.4) |
| K1 | SARI (A1, A2, A3) | 0,05x; 12.11'de en çok 0,10x |
| K2 | KAPALI (2/8) | Yok |
| K3 | O3 koşulu ✓ (σ ~%20 ≤ %21; RV20 %32,4 ≥ %28) | Strangle ≤ 320 puan, ~%0,3 |
| K4 | Olay haftası | Kaçınma kuralları |
| K5 | Sezon dışı | KAP taraması |
| K6 | Zayıflıyor | ≤ %0,5 risk/işlem |

### 3.4 Gün gün: 9–13 Kasım (TÜFE'siz hafta)

**Hazırlık, Cuma 6.11 akşamı ve hafta sonu:**
1. 18:30'dan sonra `viop_20261106.csv` indirilir. Kaydedilecek uzlaşmalar: F_XU0301226, F_USDTRY1226, F_XLBNK1226, O_XU030E1226P14000, C15500, C15000, C16000, P13250 (komut Ek A'da). Zımni oranlar ve O3 strangle fiyat sınırı güncellenir: sınır = min(320, P14000 uzlaşması + C15500 uzlaşması + 10).
2. Tarama yeniden çalıştırılır: `python3 bist_tarama.py --veri ~/bist_veri --cikti ../tarama`. VİOP tablosu yerine bülten kullanılır.
3. Aracı kuruma Kural 0 soruları (§1.3) e-postayla gönderilir.
4. En az 2 bankadan 32 günlük mevduat teklifi alınır. Banka iştiraki PPF'nin ücreti ve izahnamedeki ters repo karşı tarafı kontrol edilir.
5. KAP taranır: (a) hak kullanımı 16.11–11.12 arasında olan temettüler; (b) SPK bülteninde bedelsiz onayları; (c) halka arz talep takvimi.

**Pazartesi 9.11. Konsolide bilanço son günü**
- 09:30–10:00: Çekirdek emirleri (mevduat, PPF). VİOP hesabına faizli teminat transferi.
- Gün içi: ekran yok.
- 17:40: Gösterge A ve B (Cuma verisiyle) → A: 3 SARI, B: KAPALI.
- 17:55–18:08:
  - (1) **K1:** F_USDTRY1226 limit satış, 1 / 5 / 19 kontrat. Prim filtresi P ≥ 5 kontrol edilir. Kural 0 sağlanmadıysa K1 yok.
  - (2) **O3:** P14000 limit ≤ 140 ve C15500 limit ≤ 180 alış (toplam ≤ 320). Emir 12.11 18:10'a kadar geçerli (tarihli ya da günlük olarak yenilenir).
  - (3) 9.11 akşamı bilanço açıklayacak hiçbir isimde pay vadelisi ve spot pozisyon yok.
- Akşam: KAP bilançoları → PEAD kâğıt kaydı (sürpriz yönü). Günlük kaydı yazılır.

**Salı 10.11**
- 10:00 Eylül sanayi üretimi; 16:30 ABD Ekim TÜFE. Eylem yok: ABD veri günlerinde 1–3 günlük risk artmıyor [PRATİK §2].
- 17:45: K1 stopu (uzlaşma ≥ giriş × 1,025?). O3 emir durumu. Dolmadıysa limit korunur, fiyat kovalanmaz.
- Bilanço gap'leri yalnız kaydedilir.

**Çarşamba 11.11**
- MSCI öncesi yeni pozisyon yok. K1 ve O3 tutulur.
- 17:45: Rutin stop kontrolü.

**Perşembe 12.11. MSCI + TCMB raporu + rezervler**
- 01:00: MSCI duyurusu. Sabah okunur, K4 kuralı uygulanır: çıkarılan ve FIF'i düşürülen VİOP-47 isimleri yasak listeye.
- 10:30: TCMB Enflasyon Raporu 2026-IV. Yıl sonu tahmini kaydedilir (L7 notu).
- 14:30: Rezerv ve haftalık menkul kıymet → A1, A2, A3, L1, L3 güncellenir.
- 17:45 karar:
  - (a) Gösterge A'da KIRMIZI yok → K1'i 0,10x'e tamamla (+1 / +5 / +19 kontrat).
  - (b) KIRMIZI var → K1'in tamamını 17:55–18:08'de kapat.
  - (c) O3 dolmamışsa emri iptal et; strangle bu kez alınmaz.
- Akşam: SPK bülteni → kredili esneklik kararı.

**Cuma 13.11. Kredili esnekliğin son günü**
- 10:00 Eylül ödemeler dengesi (eylem yok).
- 17:30'a kadar SPK kararı:
  - **Uzatıldıysa** eylem yok; L6 ✓ adayı.
  - **Uzatılmadıysa:** 27.11'e kadar BIST30 dışı spot long yok; 16–20.11'de düşen alınmaz; L6 = ✗ (10 iş günü izleme).
- Kasım Piyasa Katılımcıları Anketi bu gün çıkarsa (teyitsiz; 20.11 de olabilir) L7 güncellenir.
- Haftalık değerlendirme: günlük kayıt, teminat kullanımı, göstergeler, aylık zarar limiti sayacı.

### 3.5 16–30 Kasım

| Tarih | Eylem |
|---|---|
| 16–20.11 | Esneklik bittiyse zorla satış haftası: alım yok, yalnız izleme (XUTUM 5 günlük getiri, L6) |
| Per 19.11 14:30 | Rezerv (2. hafta) → A1/L1. Banka konsolide 3Ç son günü (HALKB) |
| Per 26.11 14:30 | Rezerv (3. hafta) → L1 olası ✓. **PİLOT kontrolü:** (L1 veya L2) ve ≥ 4/8 → O1 call spread (Şubat serisi) 26.11 kapanış penceresinde. K6'daki Kasım pay vadelilerinin kapatma/roll son günü |
| Cum 27.11 | TCMB Finansal İstikrar Raporu. Not alınır |
| Pzt 30.11 | VİOP Kasım vadesi (Plan B'de Kasım kontratı yok). MSCI değişiklikleri kapanışta → kâğıt üstü çıkış dönüşü alımı. **Ay sonu:** tarama yeniden çalıştırılır; küme 12 ay RS sıralaması (A kuralı) güncellenir; Gösterge A/B ay sonu okuması; aylık rapor (§7.3) |

### 3.6 Aralık ve 1. çeyrek 2027 takvimi

| Tarih | Olay | Plan B eylemi |
|---|---|---|
| Per 3.12 10:00 | Kasım TÜFE | **L2.** < %2,0 ve L1 ✓ ve ≥ 5/8 ise **K2 TAM, dilim 1** o günün kapanışında. K1 tavanı 0,05x'e iner |
| Per 10.12 | PPK (anket %35) | Baskıyla sert indirim olursa (ex-ante reel < +%3) A7 değerlendirilir |
| Sal 15.12 | O3 strangle'ın en geç kapanışı | Kapat |
| 21–23.12 | Roll haftası | K1: F_USDTRY Aralık → en likit sonraki vade. K2: Aralık → Şubat. Vergi: 31.12.2026'da biten stopaj oranlarına göre çekirdek yeniden değerlendirilir [V-ÇAP §2.6] |
| Per 31.12 | Aralık vadesi (XU030, USDTRY, pay vadelileri, XU030 opsiyonları) | Roll edilmeyen her şey kapanmış olmalı |
| 29.01.2027 | BIST30 blok kilidinden önceki son hafta | K2 Blok 1 nominali yarıya (L3 ✓ değilse) |
| 31.01.2027 | Fon yoğunlaşma uyumu son tarihi | 01.02'den itibaren BIST30 dışı evren kısıtı gözden geçirilir |
| ~03.02.2027 | BIST30 blok satış kilidinin açılışı | Arz riski: K2'de yeni dilim yok (1 hafta) |
| ~17.03.2027 | Tasfiye azami süresi | Dışlama listesi gözden geçirilir |
| Mart–Haziran 2027 | Temettü sezonu | K5 en aktif dönem |
| Haziran 2027 | MSCI sınıflandırma değerlendirmesi | A7/L-göstergeleri; Mayıs'ta yeniden değerlendirme |

---

## 4. Evren, dışlama listesi, kümeler, adaylar

### 4.1 Evren

| Kol | Evren |
|---|---|
| K1 | F_USDTRY (en likit 2 vade) |
| K2 | F_XLBNK (Likit Banka endeks vadelisi; 5.11'de Aralık hacmi 6.617 kontrat, açık pozisyon 4.857), F_XU030 ve VİOP-47 pay vadelileri. Banka pay vadelilerinde Aralık açık pozisyonları: GARAN 3.431, AKBNK 16.098, YKBNK 31.925, ISCTR 41.736, VAKBN 7.960. Kasım vadesi çok likit ama 30.11'de fiziki teslimat [BÜLTEN] |
| K3 | O_XU030 Aralık 2026 ve Şubat 2027 serileri (likidite kuralı §2-K3) |
| K5 | BIST100 eksi dışlama listesi. 31.01.2027'ye kadar BIST30/VİOP-47 dışında fon payı / fiili dolaşım ≥ %8 olan hisse yok |

VİOP-47 dayanakları [TARAMA (e)]: TKFEN, TUPRS, ENJSA, BRSAN, HALKB, BIMAS, ASELS, GARAN, ALARK, KRDMD, KCHOL, VAKBN, YKBNK, SOKM, TAVHL, THYAO, ISCTR, AKBNK, SAHOL, EREGL, ENKAI, TRALT, TRMET, AEFES, PETKM, EKGYO, CIMSA, TSKB, TTKOM, TCELL, OYAKC, DOHOL, AKSEN, SISE, TOASO, ASTOR, PGSUS, ULKER, MGROS, FROTO, DOAS, ODAS, GUBRF, ARCLK, SASA, HEKTS, VESTL.

### 4.2 Dışlama listesi (bütün kollar, en az 17.03.2027'ye kadar)

| Grup | Hisseler | Dayanak |
|---|---|---|
| Fon payı / fiili dolaşım > %20 (QNB, fonoloji) | PASEU, KTLEV, ANELE, TEHOL, TRHOL, OZATD, GUNDG, DSTKF, PEKGY, SKYLP, SELEC, KARCL, IEYHO, TMPOL, ODINE, ISVEA, MAGEN, BALSU, ISKPL, DAGI, INFO | [PROF §4.5, §6], [V-PROF T6] |
| SPK suç duyurusu yapılan 13 hisse | KTLEV, GUNDG, DSTKF, OZATD, TRHOL, ODINE, VSNMD, IEYHO, ALKLC, ANELE, PASEU, SELEC, MANAS | [PROF §4.3], [V-PROF T10] |
| Tera / Pusula / Hedef grubu ve TMSF kayyumlular | TERA, TEHOL, TRHOL, HEDEF, HDFGS, DSTKF, BIGEN | [PROF §4.4, §6] |
| Özel uyarı | GLRMK (Pusula payı fiili dolaşımın %22'si) | [PROF §6] |
| 2025–26 halka arzları (tavan serisi sonrası) | İlk işlemden itibaren 250 işlem günü dolmadan | [ARZ §0], [KİM §0.5] |
| VBTS tedbirli hisseler | KAP/GCM "Tedbirli Hisseler" listesi, her akşam | [HAZ §3] |
| Yalnız VİOP kolları için | Aracı kurum PSR'si ≥ %50 olanlar (QNB 3.11: ASTOR, HALKB, VESTL %100, GUBRF %50) | [V-BIST #16] |

### 4.3 Kümeler ve bloklar

Küme tanımları [DALGA §1]: 24 küme, eşit ağırlıklı, bugün likit üyeler.

Korelasyon blokları [DALGA §5], [V-DAL B12]:
- **Blok 1 (büyük sermaye ve finans):** BANKA, HOLDİNG, HAVACILIK, TELEKOM, GYO. Günlük korelasyon 0,70–0,79. **Tek risk bütçesi.**
- **Blok 2 (küçük-orta tema):** ELK_EKİPMAN, YENİLENEBİLİR, TEKNOLOJİ, ELK_ÜRETİM. Fon krizi satışının merkezi. Plan B'de **yok**.
- **Blok 3 (sanayi):** ÇİMENTO, OTO_YAN, KİMYA, CAM, BEYAZ_EŞYA, SAĞLIK. Plan B'de yok.
- **Ayrıştırıcılar:** RAFİNERİ (fazla getiri korelasyonu banka ile −0,42, havacılık ile −0,31), SAVUNMA (banka ile −0,35), KOZA_ALTIN (~0).
- **TL bloğu (Plan B'ye özgü):** K1 carry, S4'te Blok 1 ile birlikte kaybeder [V-ÇAP §2.8]. Bu yüzden ortak stres bütçesine girer (§5).

Güncel küme durumu [DALGA §5]:
- 12 ay RS ilk 3: RAFİNERİ, HOLDİNG, KOZA_ALTIN.
- 126 günlük RS kırılımı: BANKA, HAVACILIK.
- Mutlak momentum hiçbir kümede yok.
- Düşen piyasada RS liderliği düşük beta demek (RAFİNERİ β 0,55).

### 4.4 K2 adayları (TAM tetikte kullanılacak sıra; 5.11 kapanışı, [TARAMA (e)])

| Hisse / araç | Küme | 50 GHO'ya uzaklık | 200 GHO'ya uzaklık | RS | 3 ay | Teknik durum | Plan B durumu |
|---|---|---|---|---|---|---|---|
| F_XLBNK (endeks) | BANKA | +%0,7 | −%3,4 | — | +%5,7 | 50 GHO üstü | **Makro kapı bekliyor** (1. tercih, ≥ 5 mn TL) |
| GARAN | BANKA | +%8,5 | +%5,8 | 86 | +%11,8 | Nitelikli (50 ve 200 üstü) | Makro kapı bekliyor (1 mn TL sepetinde) |
| YKBNK | BANKA | +%1,9 | −%0,6 | 77 | +%7,3 | 50 üstü | Makro kapı bekliyor |
| ISCTR | BANKA | +%1,0 | −%5,6 | 71 | +%5,6 | 50 üstü | Makro kapı bekliyor |
| AKBNK | BANKA | −%2,5 | −%7,5 | 70 | −%0,3 | 50 altı | Bekliyor (50 GHO'yu geri almalı) |
| VAKBN | BANKA | −%3,9 | −%4,4 | 81 | +%3,4 | 50 altı | Bekliyor |
| HALKB | BANKA | −%10,6 | −%5,2 | 90 | +%8,3 | — | **Hariç** (QNB'de %100 teminat) |
| TAVHL | HAVACILIK | +%7,8 | +%1,5 | 74 | +%6,3 | Nitelikli | Yalnız 3. dilim (Aralık vadesi sığ: açık pozisyon 518) |
| THYAO | HAVACILIK | +%4,4 | −%2,3 | 72 | −%3,0 | 50 üstü | Yalnız 3. dilim |
| PGSUS | HAVACILIK | −%0,1 | −%17,4 | 37 | −%8,9 | — | Bekliyor |
| KCHOL / SAHOL / ALARK | HOLDİNG | −%4,2 / −%4,0 / −%4,5 | +%0,8 / −%8,9 / +%0,3 | 83 / 67 / 85 | — | 50 altı | Bekliyor (SAHOL'de fon tutma notu) |
| TUPRS | RAFİNERİ | −%12,9 | +%16,2 | 96 | +%4,4 | 50 altı | Opsiyonel karşı ağırlık; 50 GHO'yu geri alınca |

Tarama listesindeki trend şablonunu geçenler (AHGAZ, ENERY, RYSAS spot; ENJSA VİOP'lu) Plan B'nin konusu değil. Kırılım/şablon kanıtı [TEST §5] Plan A'ya ait. Plan B'de kullanılmaz.

---

## 5. Risk limitleri

| Limit | Değer | Dayanak / gerekçe |
|---|---|---|
| İşlem başına risk (stop + 1 limit günü gap) | K2 dilimi ≤ %1,25; K5 olayı ≤ %0,5 (%7 boy × %7 kuyruk çıkışı); opsiyon yapısı ≤ %0,5 prim (O3 %0,35); K6 ≤ %0,5 | [ŞEYTAN §3.3, §5.3] (tıraşlanmış SR'nin ≤ ¼ Kelly'si; pozitif çarpık sistemde işlem başına ~%0,25–1) |
| K1 stresi (USDTRY +%30) | SARI ≤ %3, YEŞİL ≤ %6 sermaye | [ŞEYTAN §5.1 sıra 5] (≤ %5–10) |
| Küme: Blok 1 | Açık risk ≤ %3,75; nominal ≤ 0,5x | [ŞEYTAN §3.6] (ρ 0,8'de 5 pozisyon ≈ 1,19 bahis; risk küme düzeyinde verilir) |
| **Ortak stres** (USDTRY +%30, XU030 −%25, bankalar −%35, 2 limit kilidi günü; stoplar −%20'de dolar varsayımı) | ≤ %10 sermaye. Formül: 0,20 × Blok 1 nominali + 0,30 × K1 nominali − put spread azami ödemesi | [V-ÇAP §2.8] (taban carry ve tetikli banka aynı kuyrukta). Bu yüzden K2 TAM'da K1 ≤ 0,05x |
| Toplam açık risk (stop riskleri + opsiyon primi) | ≤ %5 | [KOMİTE §5] (fikir başına ≤ %1, toplam ≤ %4, ortak stres ≤ %7). Plan B'de ortak stres sınırı %10, gerekçesi yukarıda |
| Aylık zarar limiti (kollar, engele göre fazla) | −%3 → ay sonuna kadar yeni risk yok. Başlangıçtan −%5 → bütün boylar yarıya. −%8 → bütün kollar kapanır, 1 ay ara ve mekanizma incelemesi | [ŞEYTAN §5.2.8] (−%25/−%35 eşikleri daha oynak planlar için; düşük oynaklıklı plan B'ye ölçeklendi) |
| VİOP teminat kullanımı | Aracı kurum başlangıç teminatı ≤ %20 sermaye; serbest teminat ≥ başlangıç teminatının 2 katı | [PRATİK §3] (teminat değil risk bağlayıcıdır; kaldıraç tuzağı) |
| Kaldıraç | Brüt vadeli nominali ≤ 0,6x (K1 dahil); net hisse betası ≤ 0,5x | Ortak stres sınırından türetildi |
| Limit kilidi | Endeks ve pay vadelilerinde günlük limit ±%10 (normal seans), akşam ±%3. Tek isimde pay vadelisi nominali ≤ %10 sermaye (2 kilit günü ≈ −%2) | [HAZ §5], [PRATİK §3] (kilit riskli hisselerde %99 kuyruğa göre boyut) |
| Hafta sonu / tatil | Yeni K2 dilimi Cuma kapanışında açılmaz (Pazartesi kapanışına ertelenir) | Gap riski |

---

## 6. Uygulama, maliyet, vergi, kayıt

### 6.1 Seans ve karar penceresi

| Piyasa | Saatler (TSİ) |
|---|---|
| Pay piyasası | Açılış seansı 09:40–09:55; sürekli işlem 10:00–18:00; kapanış seansı 18:00–18:10 (tek fiyat) |
| VİOP normal seans | 09:30–18:10/18:15 |
| VİOP akşam seansı | 19:00–23:00, yalnız endeks vadelileri (XU030, XBANK, XUSIN, XLBNK, X10XB) ve kıymetli maden/bakır. Pay vadelisi ve USDTRY akşamda yok |

Kaynak: [HAZ §5].

**Plan B'nin gün içi ekran süresi sıfır.** Günlük iş 17:40–18:08 arası: gösterge ve stop kontrolü, ardından emir.

### 6.2 Emir tipleri

| Durum | Emir |
|---|---|
| VİOP giriş/çıkış (K1, K2, K6) | 17:55–18:08 arası limit emir: en iyi alış/satış ya da son fiyat ± 1 adım. Kovalama yok. Dolmazsa ertesi gün aynı kural. "Piyasadan limite" emir yalnız stop çıkışında |
| Stoplar | Uzlaşma ya da son fiyat bazlı; 17:45'te kontrol, aynı gün kapanış penceresinde çıkış. Aracı kurum **sunucu taraflı** şartlı emir sunuyorsa ek felaket stopu (K1: giriş × 1,045; K2: giriş × 0,88). Yoksa gap riski boyutta hesaba katılmıştır (§5) |
| Spot olaylar (K5) | Kapanış seansına limit emir: alışta son fiyatın %1 üstü, satışta %1 altı. Tek fiyattan eşleşir. Halka arz satışında açılış seansı limit emri |
| Opsiyonlar (K3) | Bacak bacak limit emir ≤ uzlaşma; tarihli/İKG geçerlilik. Kombine emir varsa o kullanılır |
| Roll | Vadeler arası (takvim yayılımı) emir. Yayılma teminatı düşüktür: XU030 7.880 TL, USDTRY 2.185 TL [HAZ §5] |

### 6.3 Maliyetler (tahmini; aracı kurumdan teyit)

| Kalem | Değer | Kola etkisi |
|---|---|---|
| Borsa payı | Endeks vadeli/opsiyon on binde 0,4; pay ve döviz vadeli on binde 0,3 | İhmal edilebilir |
| Aracı kurum komisyonu | Banka kurumu liste fiyatı on binde 8–10; aktif bireyde on binde 1–4 (teyitsiz); üzerine BSMV %5 | K1 yılda ~0,05 puan; K2 dilim başına ~%0,05–0,1; K5 olay başına ~%0,2–0,3 (gidiş-dönüş, spot) |
| Makas ve kayma | USDTRY 1 adım (0,001); XLBNK/XU030 1–2 puan; opsiyonlarda belirsiz (bültende yok), uzlaşmadan alım varsayılır | Opsiyonda asıl maliyet |
| Teminatın fırsat maliyeti | Faizsiz nakitse yılda teminat × ~%33 | **Kural 0** |
| Vergi | Pay ve pay endeksi VİOP %0; F_USDTRY %10 (sözleşme sonunda); spot pay %0; temettü stopajı (alınmıyor, K5 hak kullanımı öncesi satıyor); mevduat/PPF %17,5; DİBS %0 ya da %10 (teyit) | Stopajlı gelirler için ayrıca beyan gerekip gerekmediği muhasebeciyle teyit edilmeli (GVK geçici 67, süre 31.12.2030'a uzatıldı [V-ÇAP #9]) |

### 6.4 Kayıt (günlük ve aylık)

Her işlem için **hipotez kartı** önceden yazılır ve değiştirilmez [ŞEYTAN §5.3.1]. Kart içeriği:
- Kol ve kural numarası.
- Mekanizma (kim, neden zorla işlem yapıyor).
- Beklenen E[R], isabet, kazanç/kayıp oranı.
- Giriş, çıkış ve stop.

**Günlük kayıt alanları:**

| Alan | Açıklama |
|---|---|
| Tarih/saat, kol, kart no | Örnek: K1-SARI-0,05x |
| Gösterge okuması | A1–A7, L1–L8 değerleri ve rengi |
| Araç, yön, adet, nominal (TL ve sermaye %'si) | — |
| Sinyal fiyatı / dolum fiyatı / kayma (bps) | Uygulama farkı ölçümü |
| Başlangıç riski R (TL) | K1: nominal × %2,5; K2: nominal × %8; opsiyon: prim; K5: boy × %7 |
| Stop, iz-stop, zaman stopu | — |
| Teminat (aracı kurum / Takasbank), teminat türü ve faizi | Kural 0 izleme |
| Çıkış tarihi, fiyat, neden | Stop / hedef / zaman / gösterge / kural ihlali |
| Brüt K/Z, komisyon, BSMV, stopaj | — |
| **Engele göre fazla K/Z** | K/Z − (bağlanan nakit × engel oranı × gün/365). Vadeli için bağlanan nakit = faiz kazanmayan teminat |
| R katı, MAE, MFE, tutma süresi | — |
| Kural ihlali (E/H) ve not | — |

Belgeler: aracı kurum ekstreleri, MKK e-Yatırımcı dökümü, stopaj kesinti belgeleri, KAP/SPK bülten ekran görüntüleri (olay işlemleri için).

---

## 7. Öldürme kriterleri ve ileri ölçüm protokolü

### 7.1 Öldürme kriterleri (önceden yazılı)

| Kol | Kriter | Eylem |
|---|---|---|
| Plan geneli | Engele göre fazla K/Z başlangıçtan −%5 / −%8 | Boylar yarıya / bütün kollar kapanır, 1 ay ara [ŞEYTAN §5.2.8] |
| K1 | Tek kayıp > planlanan stop kaybının 1,5 katı (gap) | Gösterge 4 hafta YEŞİL olana kadar kapalı. 3 ay içinde 2 kez KIRMIZI olursa çeyrek boyunca kapalı [ŞEYTAN §5.2.6] |
| K1 | Kural 0 bozulur (teminat faizi < politika faizinin %80'i) | Kapalı |
| K2 | 4 TAM dönem sonunda toplam R ≤ 0 | Askıya al, göstergeyi yeniden incele |
| K2 | Canlı ile kural farkı: tetik günü dolum kayması > %1 (ortalama) | Emir yöntemini değiştir |
| K3 | Yıllık prim bütçesi %1,5 dolarsa | Yıl sonuna kadar yeni opsiyon yok. 10 ardışık O3/O1 yapısı değersiz biterse ve aynı dönemde gerçekleşen vol zımni vol'den düşük kaldıysa O3 tipi öldürülür |
| K4 | Her olay türü kartla önceden kaydedilir. 20 olaydan sonra ortalama fazla getiri ≤ 0 | O türü öldür [ŞEYTAN §5.1 sıra 2] |
| K5 | Tür başına 20 olaydan sonra engele göre ortalama fazla ≤ 0 ya da ortalama kayma > beklenen kenarın %50'si | O türü öldür [ŞEYTAN §5.2.3] |
| K6 | [PRATİK] ve [ŞEYTAN §5.2.4]: 50 işlemde canlı ortalama < backtest'in %50'si → boy yarıya; 100 işlemde < 0 → öldür | — |
| Mekanizma | Gerekçe ortadan kalkarsa (ör. TCMB ortodoks politikadan döner; MSCI statüsü değişir; SPK kuralı değişir) | t-istatistiğine bakılmadan kapat [ŞEYTAN §5.2.5] |

### 7.2 Ölçek büyütme kuralları

- **K1:** Boyutu kâr belirlemez, yalnız gösterge belirler. Çöküşsüz sicil SR hakkında bilgi vermez [ŞEYTAN §3.5].
- **K2:** Yılda en çok 1–3 dönem; n küçük. Boyut sabit kalır, kâra göre büyütülmez.
- **K5:** Tür başına ≥ 20 olay ve ≥ 12 ay olmadan olay başına boy %7'yi aşmaz.
- **K3:** Bütçe sabit.
- **Genel kural:** 12 ay ve kol başına yeterli örnek (K5'te 20 olay, K6'da 100 işlem) olmadan büyütme yok. Yalnız öldürme kararı verilebilir [ŞEYTAN §5.3.4].

### 7.3 Aylık rapor (ay sonu, 30.11'den başlayarak)

- Kol bazında engele göre fazla K/Z (TL ve sermayenin %'si); R cinsinden E[R]; isabet; kazanç/kayıp oranı.
- Net kârın en iyi işleme düşen payı.
- Uygulama farkı (bps).
- XU030 ve USDTRY'ye beta/korelasyon. 12 ayda korelasyon > 0,7 ve kalıntı alfa ≤ 0 ise kol "beta"dır, ucuz endeks pozisyonuyla değiştirilir [ŞEYTAN §5.2.7].
- Gösterge A/B geçmişi.
- Teminat kullanımı ve teminat faizi.
- Kıyas: (a) mevduat/PPF; (b) XU030 vadelisi; (c) basit 12 aylık trend kuralı [ŞEYTAN §5.3.6].

---

## 8. Beklenen sonuç aralıkları (12 ay, TL, vergi ve maliyet sonrası)

Varsayımlar ve çekinceler:
- Senaryo olasılıkları [MAKRO §5.2]'den alındı ve **öznel**.
- K2 kanıtı n=4.
- K1'in Sharpe'ı örneklem içi (rejim başlangıcı bilinerek seçildi [V-BIST §2.6]).
- O3'ün BIST'e özgü kanıtı yok.
- Çekirdek getirisi faiz patikasına bağlı. S4'te faiz artışıyla yükselir; mevduat 32 günlük olduğu için gecikmeli.

| Bileşen (sermayenin puanı) | S1 sönümlenme (%35) | S2 yatay kanama (%40) | S3 kontrollü hızlanma (%15) | S4 kırılma (%10) |
|---|---|---|---|---|
| Çekirdek | %31–33 (indirimler) | %33–36 | %34–36 | %36–40 |
| K1 carry (ortalama 0,05–0,15x) | +1,0…+1,5 | +0,5…+1,2 | −1,0…+0,3 | −2,5…−4,0 |
| K2 long BIST | +4…+12 (tetik zamanında ateşlenirse) | −2,5…0 (yanlış tetik) | −1,5…0 | −2…0 |
| K3 opsiyon | +0,5…+2 (O1 kazanır) | −0,5…+0,3 | −0,3…+0,5 | +0,5…+2 (O2/O3) |
| K5 olaylar (halka arz hariç) | +0,5…+1 | +0,5…+1 | +0,3…+0,6 | −0,5…0 |
| Maliyet | −0,3…−0,5 | −0,2…−0,4 | −0,2…−0,4 | −0,3…−0,5 |
| **Toplam (yaklaşık)** | **%37–49** | **%31–38** | **%32–37** | **%31–37** |
| Engele göre | +6…+16 | −2…+2,5 | −2,5…+1 | −6…−1,5 |

**Özet:**
- Ağırlıklı beklenen fazla getiri ≈ **+0…+4 puan/yıl**. Merkez ~+2–3; K2'nin S1'de zamanında ateşlenmesi varsayımına çok duyarlı.
- Dağılım:
  - p10: engelin ~5–7 puan altı.
  - p50: engelin ~0–2 puan üstü.
  - p90: engelin ~12–16 puan üstü.
- **P(12 ayda engelin altında) ≈ %35–45.**
- Engele göre beklenen en büyük düşüş −%6…−%10. Tek kötü ay (S4 + K2 açık) −%5…−%8.
- Halka arz eklentisi: 1 mn TL'de +1…+2,7 puan; 5 mn'de +0,2…+0,5; 20 mn'de ~0.
- Kıyas: Plan A tipi kırılım portföyünün 36 varyant medyanı %34,8 TL, MaxDD −%41 [TEST §5.2]. 2024–26'da düzeltilmiş engelin 2–8 puan altı [V-BIST §2.1]. Plan B daha düşük oynaklıkla engel civarında kalır; büyük kazancı yalnız rejim dönüşünde arar.
- **Dürüst sonuç:** Bu plan "her yıl yüksek getiri" vermez. Plan, rejim kırıldığında (S1) bankalardan büyük getiri alacak, olmazsa engeli koruyacak şekilde kuruldu. Önceki 3 yılın galibi carry'nin primi daralıyor (28 → ~13 puan). Rezerv göstergeleri bozulduğu için carry kasıtlı olarak küçük tutuluyor.

---

## 9. Pazartesi 9.11.2026 kontrol listesi (tek sayfa)

**Cuma akşamı / hafta sonu**
- [ ] `viop_20261106.csv` indir. Uzlaşmalar: F_XU0301226, F_USDTRY1226, F_XLBNK1226; Aralık P14000, C15500, C15000, C16000, P13250. O3 sınırı = min(320, P14000 + C15500 + 10)
- [ ] Taramayı yeniden çalıştır; VİOP tablosu yerine bülteni kullan
- [ ] Aracı kuruma yazılı sorular: teminat türleri ve faiz, kurum PSR'leri, sunucu taraflı stop, kombine opsiyon emri, komisyon. **Teminat faizsizse K1 yok**
- [ ] 2 bankadan 32 gün mevduat teklifi; banka iştiraki PPF (tasfiyedeki 7 PYŞ'den değil)
- [ ] KAP: 16.11–11.12 arası temettü hak kullanımları; SPK bedelsiz onayları; halka arz talepleri
- [ ] Dışlama listesini (§4.2) emir ekranında "yasak listesi" olarak kaydet

**Pazartesi 09:30–10:00**
- [ ] Mevduat %55 (4 haftalık merdiven) / PPF %30 / VİOP faizli teminat %10 yerleşimi

**Pazartesi 17:40 (göstergeler, Cuma verisi)**
- [ ] Gösterge A: A1 SARI, A2 SARI, A3 SARI, A4–A7 YEŞİL mi? (KIRMIZI varsa K1 yok)
- [ ] USDTRY 10 günlük tempo (TCMB XML) < %25 mi? Prim filtresi P ≥ 5 mi?
- [ ] Gösterge B: 2/8 → KAPALI (değiştiyse not al; Pazartesi K2 açılmaz)
- [ ] O3 koşulu: strangle fiyatının zımni σ'sı ≤ %21 ve RV20 ≥ %28?

**Pazartesi 17:55–18:08 (emirler)**
- [ ] K1: F_USDTRY1226 **limit satış** 1 / 5 / 19 kontrat (1 / 5 / 20 mn TL). Önceki uzlaşmanın 0,03 TL altına kovalanmaz. Stop eşiğini yaz: giriş × 1,025
- [ ] O3: P14000 alış ≤ 140, C15500 alış ≤ 180 (toplam ≤ 320) → 1 / 5 / 20 adet. Geçerlilik 12.11 18:10. Çıkış kuralını karta yaz: 2× → yarısı; ≤ 160 → hepsi; en geç 15.12
- [ ] Bilanço açıklayacak isimlerde pay vadelisi veya spot **yok** (KCHOL, BIMAS, PGSUS, TCELL, SOKM, DOAS, AKSEN, ALARK, EREGL, ARCLK, KRDMD, ASTOR, GUBRF, HEKTS, OYAKC, CIMSA, ENJSA, TKFEN, TRALT, TRMET, EKGYO, VESTL, ODAS)
- [ ] Hisse long yok (K2 KAPALI). Düşen hisse alımı yok

**Pazartesi akşam**
- [ ] Günlük kaydı yaz (her işlem için hipotez kartı, R, teminat, sinyal/dolum fiyatı)
- [ ] KAP bilançoları → PEAD kâğıt kaydı

**Hafta içi hatırlatıcılar**
- [ ] Per 12.11 sabah: MSCI Türkiye değişiklikleri → çıkarılanlar 30.11'e kadar yasak
- [ ] Per 12.11 14:30: rezerv ve akım → KIRMIZI yoksa K1'i 0,10x'e tamamla (+1 / +5 / +19); KIRMIZI varsa K1'i kapat. O3 dolmadıysa iptal
- [ ] Cum 13.11: SPK kredili esneklik kararı → uzatılmadıysa 27.11'e kadar BIST30 dışı spot long yok; L6 izleme
- [ ] Her akşam 17:45: K1 stopu (uzlaşma ≥ giriş × 1,025) ve A7 şok kontrolü

**Limitler (her emirden önce)**
- [ ] Toplam açık risk ≤ %5; ortak stres ≤ %10; teminat kullanımı ≤ %20; aylık zarar sayacı > −%3

---

## Ek A. Hesaplar ve veri komutları

**Resmi VİOP bülteni** (varsayılan başlıklarla; tarama dosyasındaki ChartData vadeli fiyatı yerine bu kullanılır):

```
G=20261106
curl -s -o viop_$G.csv https://www.borsaistanbul.com/data/vadeli/viop_$G.csv
awk -F';' '$2~/^(F_XU0301226|F_USDTRY1226|F_XLBNK1226|O_XU030E1226P14000.00|O_XU030E1226C15500.00|O_XU030E1226C15000.00|O_XU030E1226C16000.00|O_XU030E1226P13250.00)$/ {print $2, "uzlasma="$10, "kapanis="$16, "adet="$20, "islem="$21, "acikpoz="$22}' viop_$G.csv
```

Sütunlar: 2 = sözleşme kodu, 10 = uzlaşma, 16 = kapanış, 20 = işlem miktarı, 21 = işlem sayısı, 22 = açık pozisyon.

**Formüller:**
- Zımni basit faiz (XU030, XLBNK, pay vadelisi): `i = (F/S − 1) × 365 / gün`.
  - 5.11: XU030 (14.734 / 14.101, 56 gün) = **%29,3**.
  - XLBNK (15.237 / 14.563,5) = %30,1.
  - GARAN Kasım (144,45 / 142,00, 25 gün) = %25,2.
- USDTRY fiyatlanan yıllık kur artışı: `(F/S − 1) × 365 / gün` = (52,296 / 50,048 − 1) × 365/56 = **%29,3**. Zımni TL faizi (USD %3,9 ile) ≈ %33,4.
- Prim filtresi: `P = fiyatlanan − son 63 işlem gününün yıllıklandırılmış gerçekleşen artışı` (TCMB gösterge kuru: `https://www.tcmb.gov.tr/kurlar/YYYYMM/GGAAYYYY.xml`).
- Mevduat neti: `brüt × 0,825` (basit). Aylık roll ile bileşik: `(1 + brüt × 0,825 × 32/365)^(365/32) − 1`. 5.11'de: %39,52 → %32,6 basit / %37,9 bileşik.
- Engele göre fazla K/Z: `K/Z − bağlanan_nakit × engel × gün/365`. Engel: işlem tarihindeki 32 günlük mevduat neti.
- K2 kontrat sayısı: `floor(sermaye × 0,0125 / (F × çarpan × 0,08))`. Çarpan: F_XLBNK ve F_XU030 için 10 TL; pay vadelisi için 100 pay.
- Opsiyon: 1 puan = 10 TL (bülten: O_XU030E1226C15000 işlem değeri 38,4 mn TL / 256 adet = 150.000 = 15.000 × 10).
- Black-76 kontrolü (bu taslak, F = 14.734, T = 52/365, r = %35,85):

| σ | P14000 + C15500 strangle | ATM 14.750 straddle | C15000/C16000 | P14000/P13250 |
|---|---|---|---|---|
| %18 | 250 | 759 | 216 | 98 |
| %20 | 315 | 844 | 234 | 117 |
| %25 | 491 | 1.054 | 270 | 157 |
| %32 | 754 | 1.349 | 302 | 199 |

  Uzlaşma fiyatlarında çarpıklık var: P13250'nin zımni vol'ü %22, P14000'ninki %18. Bu yüzden put spread uzlaşmada 75 puan, düz σ hesabındaki değerden ucuz.

## Ek B. Bu taslakta ilk kez yapılan kontroller

1. **Resmi bülten ayrıştırması (05.11):**
   - XU030 Aralık opsiyonlarında açık pozisyon ve işlem. Uzlaşma fiyatlarının zımni vol'ü %17–22.
   - XLBNK ve XU030 vadelilerinin çarpanı 10 TL (işlem değeri / adet / fiyat).
   - Banka pay vadelilerinin Kasım ve Aralık likiditesi.
   - Banka pay vadelilerinin zımni faizi %25–28, TLREF'in altında.
2. **SPK bülten metinleri:**
   - 2026/59: AKCNS ZPAT fiyatı 260,25 TL ile 5,627434 $ karşılığının yükseği.
   - 2026/58 ve 2026/71: ZPAT'ın "iktisabın kamuya açıklandığı tarihte pay sahibi olan diğer ortaklara" yapılması; Tera'nın PEKGY ZPAT'ını yerine getirmemesi.
   - 2026/78: kredili esnekliğin 13.11 seans sonuna uzatılması.
3. **Teyit edilemeyenler** (aracı kurum veya bankadan teyit edilmeli):
   - VİOP teminat nemalandırma oranı.
   - Opsiyon alış/satış makası.
   - Sunucu taraflı stop emri.
   - DİBS'in 2026 sonu stopaj durumu.
   - TMSF mevduat sigorta limiti.
   - Kasım PKA tarihi.
   - Güncel VBTS listesi.
   - BIST30 BYF kodu ve likiditesi.
