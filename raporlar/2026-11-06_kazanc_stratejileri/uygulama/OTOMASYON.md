# Otomasyon: her akşam "bugün ne yapılır" raporu

_08.11.2026. Amaç şu: PLAN_BIST, PLAN_ABD ve PRATIK_LISTE'deki uzun kural listelerini her iş günü bir makine uygulasın. Size yalnız ertesi seansın emir kâğıdı ve tetiğe yaklaşan seviyeler kalsın. Bilgi amaçlıdır, yatırım tavsiyesi değildir._

## 1. Mimari

```
 hafta içi ~21:05 TSİ (VİOP bülteni 20:28–20:49'da çıkar)
 ┌──────────────────────────────────────────────────────────────────────┐
 │ Bulut oturumu (Claude Code, bu ortam)                                │
 │   python3 kod/gunluk_oneri.py --cikti gunluk --veri <geçici klasör>  │
 │     ├─ İş Yatırım ChartData   : BIST endeks ve hisse kapanışları     │
 │     ├─ Borsa İstanbul         : VİOP bülteni (2 gün), pay bülteni    │
 │     │                           (60 gün → likidite sırası)          │
 │     ├─ KAP                    : BIST100 / BIST50 listesi             │
 │     ├─ FRED + CBOE            : S&P 500, Nasdaq-100, VIX, VIX3M      │
 │     ├─ gunluk/makro.json      : elle girilen makro (okunur)          │
 │     └─ gunluk/durum.json      : ABD sayaçları, açık pozisyonlar,     │
 │                                 son tetikler (okunur + yazılır)      │
 │   çıktı: gunluk/oneri_YYYYMMDD.md, gunluk/SON.md, gunluk/BILDIRIM.txt│
 │   → dal claude/borsa-kazanc-stratejileri-rfxr81'e commit             │
 │   → telefona anlık bildirim (BILDIRIM.txt metni, ≤ ~600 karakter)    │
 └──────────────────────────────────────────────────────────────────────┘
 TradingView alarmları (TRADINGVIEW_ALARMLARI.md)
   ~10:00 TUPRS sinyali · 17:45–18:10 Koza / altın / SAHOL-AKBNK canlı · 18:08–18:15 XU030 bazı · ~00:00 ABD rejimi
 Siz
   21:10 bildirimi okuyun → SON.md §0 → ertesi gün 17:45–18:10 emir penceresi
   (K1 ve XU030 bazı alarm seviyelerini rapordan güncelleyin, 2–3 dk)
```

**Neden iki parça?** Rapor 21:05'te çıkar, oysa bazı kuralların karar anı daha erkendir:
- **Koza, altın ve SAHOL/AKBNK PRATİK:** karar o günün uzlaşma penceresinde (18:00–18:10) verilir.
- **XU030 bazı:** karar 18:10–18:15'te verilir.
- **TUPRS:** sinyal ABD'nin bir önceki gece kapanışından gelir. ABD tekil hisse verisinin meşru bir kaynağı da yok. Yahoo bu ortamda HTTP 429 veriyor ve kullanılmıyor.

Bu yüzden rapor iki iş yapar:
1. Ertesi gün kapanışta işlenecek kuralları (K1, K4, açık pozisyon çıkışları) ve yarının **tetik fiyatlarını** hesaplar.
2. Canlı kararları TradingView alarmlarına bırakır.

**Çıktılar nerede?** `uygulama/gunluk/`:
- `SON.md`: en son rapor.
- `oneri_YYYYMMDD.md`: arşiv.
- `BILDIRIM.txt`: bildirim metni.

GitHub mobil uygulamasında dal `claude/borsa-kazanc-stratejileri-rfxr81` → `raporlar/2026-11-06_kazanc_stratejileri/uygulama/gunluk/SON.md`.

## 2. Elle çalıştırma

```bash
cd raporlar/2026-11-06_kazanc_stratejileri/uygulama
python3 kod/gunluk_oneri.py --cikti gunluk --veri /tmp/gunluk_veri
```

- Gereken kütüphaneler: python3, requests, pandas, numpy.
- `python3 -I` kullanmayın. Bu ortamda pandas kullanıcı site-packages'ında kurulu, `-I` onu görmez.
- `--veri` ham veri önbelleğidir. Depoya konmaz. Verilmezse geçici klasör kullanılır.
- Aynı akşam ikinci çalıştırma önbellekten hızlanır.
- **Commit edilecekler** (bulut çalışması): `gunluk/oneri_YYYYMMDD.md`, `gunluk/SON.md`, `gunluk/BILDIRIM.txt`, `gunluk/durum.json`, `gunluk/makro.json`.
  - `kod/__pycache__/` ve `--veri` klasörü commit edilmez.
  - durum.json her çalışmada değişir. Bir sonraki taze konteyner ABD sayaçlarını buradan sürdürür, bu yüzden **commit edilmesi şarttır**.

Seçenekler:

| Seçenek | Ne yapar |
|---|---|
| `--tarih YYYY-MM-DD` | BIST kesim tarihi. Geçmiş bir günü yeniden üretmek için kullanılır. ABD bölümü durum.json'daki son duruma göre kalır |
| `--cevrimdisi` | Hiç istek atmaz, önbellekten okur (deneme) |
| `--durum-yazmadan` | durum.json'u değiştirmez (deneme) |
| `--bekle 0.4` | İstekler arası bekleme (sn) |
| `--butce 540` | İş Yatırım indirmesi için zaman bütçesi (sn, çalışma başından; aşılırsa kalan seriler önbellekten) |
| `--isy-son 360` | İş Yatırım kapalıysa ~60 sn'de bir **tek istekle** yoklamanın son zamanı (sn, çalışma başından). `0` = yoklama yok |

- **Seans saati:** Komut hafta içi 18:20'den önce çalışırsa bugünün bitmemiş barı atılır, rapor dünkü kapanışa göre çıkar.
- **VİOP bülteni:** 20:50'den önce çalışırsa bülten dünkü olur ve tazelik tablosunda "BAYAT" yazar. 21:15'te yeniden çalıştırın.

## 3. Rapor bölümleri

| Bölüm | İçerik | Ne yaparsınız |
|---|---|---|
| **0. BUGÜN NE YAPILIR** | En çok 10 satır, öncelik sırasıyla. Takvim ve KRİZ engelleri; açık pozisyonların çıkışları (durum.json'a yazdıklarınız); K4/K1 girişleri; gecikmeli Koza girişi (E2); kâğıt kayıtları; canlı alarm seviyeleri; ABD izni. Emir yoksa ilk satır **"İşlem yok"** ve kısa neden. Altta **Yarın tetiklenebilecekler**: tetiğe ≤ %3 kalan enstrümanlar, kesin tetik fiyatı, tetiklenirse yapılacak işlem ve zamanı | Ertesi günün emir kâğıdına geçirin. "Canlı" satırlar için TradingView alarmına bakın |
| 1. BIST rejimi ve KRİZ | T1–T3, M1–M5; AÇIK / GEÇİŞ / KAPALI; K4 r₀ ve K9 riski; KRİZ (a)–(f) | Rejim ertesi günden geçerlidir |
| 2. Plan kuralları | K1/K2 z ve tetikler (TradingView oran alarmı seviyeleri dahil); K4 nitelikli ve bekleme listesi; küme RS; VİOP ima oranları; K6 kapısı | `bist_sinyal.py` ile aynı tanımlar |
| 3. PRATİK 1–3 gün | SAHOL/AKBNK artık z, Koza z3, altın → TRALT (F_XAUUSD uzlaşma vekili), XU030 bazı (bülten kapanış fiyatı), TUPRS (yalnız TradingView). Her biri için bugünkü değer, yarının tetiği ve tetiklenirse işlem | PLAN_BIST'te K9 kanalı: risk ≤ %0,25 (KAPALI), en çok 2 |
| 4. Takvim | Önümüzdeki 14 gün, statik tablo (PLAN_BIST §3.10/§7, PLAN_ABD §7) | Temettü, bedelsiz ve ZPAT pencereleri **otomatik değil**: Cuma KAP taraması elle |
| 5. ABD rejimi | KIRMIZI / TURUNCU / SARI / YEŞİL; ralli denemesi gün sayısı, FTD, SARI 3 kapanış sayacı, en erken pilot tarihi | FTD'nin hacim teyidi ve S5FI/S5TH elle |
| 6. Veri tazeliği | Her kaynak için son tarih ve OK / ÖNBELLEK / BAYAT / EKSİK / YOK | BAYAT ya da YOK satırı olan bölümü kullanmayın |

## 4. Kaynaklar ve süre

| Kaynak | Ne için | İstek | Not |
|---|---|---|---|
| İş Yatırım ChartData | 163 seri (5 endeks/gösterge + 158 hisse), 2023-06'dan beri düzeltilmiş kapanış | 163 | Varsayılan başlık, istekler arası 0,4 sn |
| Borsa İstanbul pay bülteni (`thbYYYYMMDD1.zip`) | 60 günlük medyan TL hacim (K4 evreni, RS evreni, %2 hacim sınırı); İş Yatırım düşerse yedek kapanış | 60 (~15 MB) | İş Yatırım HisseTekil ile aynı sonuç: 06.11'de medyan oran 1,000, sıra korelasyonu 0,9999, ilk 75 aynı |
| Borsa İstanbul VİOP bülteni | Uzlaşma, kapanış, önceki uzlaşma (son 2 gün) | 2–4 | — |
| KAP | BIST100 / BIST50 listesi | 1 | Olmazsa betikteki yedek liste |
| FRED | SP500, NASDAQ100 | 2 | FRED ~1 iş günü gecikmeli; rapor kullandığı tarihi yazar |
| CBOE | VIX, VIX3M geçmişi | 2 | — |
| TCMB | (yalnız kod hazır, şu an kullanılmıyor) | 0 | — |

**Ölçülen süre:**
- Boş önbellekle (taze konteyner) **178 sn**, 08.11 01:55'te ölçüldü. Bunun 109 sn'si 163 fiyat serisi, ~60 sn'si 60 pay bülteni (~15 MB).
- İş Yatırım kapalıyken yedek kipte 114 sn.
- Dolu önbellekle ~90 sn. Bunun ~60 sn'si pay bültenleri.

**İş Yatırım bağlantısı aralıklı koptu.** 07–08.11 gecesi, bu ortamdan İş Yatırım bağlantıları dakikalarca "connection reset" verdi, sonra yeniden açıldı. Betik bunun için:
- **Devre kesici:** Hiç başarı yokken 2 bağlantı hatası, ya da 3 ardışık başarısız kod, o kaynağı "kapalı" sayar. Böylece dakikalarca beklenmez.
- **İkinci tur:** Pay bültenleri indirilince (~1 dk sonra) eksik serileri bir kez daha dener.
- **Yoklama (denetim 08.11):** Hâlâ kapalıysa diğer kaynaklar bittikten sonra ~60 sn'de bir **tek** istekle yoklar (`--isy-son`, varsayılan çalışmanın 360. sn'sine kadar). Açılırsa eksik serileri indirir. Hiç açılmazsa çalışma ~7 dk sürer ve rapor yedek kipte çıkar.
- **Kısaltılmış geçmiş koruması (denetim 08.11):** İş Yatırım zaman zaman istenenden **kısa** geçmiş döndürüyor (07.11 gecesi GARAN yalnız son 1 yıl, MPARK/ULKER/ODAS/OTKAR 2024-03'ten). GARAN'ın kısa gelmesi BANKA kümesinin 12 ay RS'ini +%3,9 yerine +%4,5, KCHOL RS'ini 84 yerine 85 gösterdi ve GARAN'ı K4 taramasından düşürdü. Betik artık ilk tarihi istenen başlangıçtan > 30 gün sonra gelen seriyi bir kez daha ister ve uzun olanı alır (yeni halka arzlarda iki cevap aynıdır; ~14 ek istek). Önbellekteki daha uzun geçmiş, örtüşen günler tutuyorsa korunur; artımlı güncellemede örtüşen günler %0,2'den fazla farklıysa (temettü/bölünme düzeltmesi) seri baştan indirilir.

## 5. Hata durumları

| Durum | Raporda ne görünür | Ne yapılır |
|---|---|---|
| İş Yatırım kapalı, önbellek boş (taze konteynerde tipik) | Betik ~6 dk boyunca yoklar. Açılmazsa §1–3 "veri yok". §0'da "BIST verisi yok → yeni giriş yok". **Yedek kip:** son başarılı çalışmanın tetikleri (durum.json `bist.tetikler`: K4, K1, PRATİK, Koza; %10 içindekiler) pay bülteni kapanışıyla kontrol edilir; tetiklenen ya da %3 içinde kalanlar bildirime de yazılır | Zamanlanmış oturum ya da siz komutu 30–60 dk sonra yeniden çalıştırın (aynı akşam, aynı komut). Açık pozisyonları dünkü stoplarla yönetin |
| İş Yatırım yarıda koptu | §6'da "x/163 seri; bulunamayan: …". Eksik hisse K4 taramasından düşer | Bulunamayan listesi kısaysa rapor kullanılabilir. XU100, XBANK, SAHOL ya da AKBNK eksikse BIST bölümü çıkmaz |
| VİOP bülteni yayımlanmadı | §6 "BAYAT" (dünkü bülten) | İma oranları, altın ve baz satırları dünkü değerdir. 21:15 sonrası yeniden çalıştırın |
| FRED ya da CBOE yok | §5 "veri yok", son durum durum.json'dan | Sayaçlar ilerlemez. Bir sonraki başarılı çalışmada kaçırılan ABD günleri sırayla işlenir |
| makro.json 7 günden eski | Üstte uyarı, §6'da BAYAT | Perşembe 14:30 rezervini girin (§6) |
| Bulut çalışması hiç olmadı | Bildirim gelmez; SON.md eski tarihli | §2 komutunu elle çalıştırın |
| Pine derleme hatası | — | O sinyal için yalnız raporu kullanın; satır numarasını not edin |

## 6. `gunluk/makro.json` nasıl düzenlenir

Dosya ilk çalışmada 05.11 plan değerleriyle oluşturuldu. Her güncellemede **`guncellendi`** alanına tarihi yazın. 7 günden eski ise rapor uyarır.

| Alan | Ne zaman | Örnek / not |
|---|---|---|
| `net_rezerv_swap_haric` | **Her Perşembe 14:30** (TCMB) | Listenin sonuna `["2026-11-12 yayini", 19.0]` ekleyin; eski → yeni sıralı. M1 = son 3 değişim artı. KRİZ (d) = son 2 haftalık değişimin ikisi de ≤ −5 ya da seviye < 0. **12.11'de değişim yine ≤ −5 ise KRİZ (d) tetiklenir** |
| `brut_rezerv` | Perşembe | mlr $; K6 kapısı ≥ 160 |
| `yabanci_dibs_hafta_mn_usd` | Perşembe | mn $; K6 kapısı ≥ −500 |
| `tufe_aylik` | Ayın 3'ü 10:00 | `["2026-11", 2.10]` ekleyin; M2 = son 2 ay < 2 |
| `politika_faizi`, `mevduat_32g_brut` | PPK ve dilim günleri | %; mevduat neti = brüt × 0,825 |
| `cds5y`, `cds5y_20g_once`, `cds_teyitli` | İsteğe bağlı | Teyitsiz CDS M4 ve KRİZ (c) için sayılmaz |
| `msci_danisma` | MSCI duyurusu | true ise KRİZ (f) |
| `kural0`, `komisyon_viop_bps` | Aracı kurum yazılı cevabı gelince | K1 ve XU030 nakit-taşıma kapısı: kural0 = true ve komisyon ≤ 5 |
| `bilanco_aciklayanlar_9_11` | 9.11 akşamı | KAP'ta bilançosunu açıklayan isimler. A1 engeli kalkar |
| `msci_cikarilanlar` | 12.11 sabahı | Çıkarılan hisseler 30.11'e kadar K4'te "dışlama" olur |
| `kredili_esneklik_uzatildi`, `ppk_10_12_surprizsiz_indirim` | 12–13.11, 10.12 | Bilgi alanı (A4, A7). Rapor takvim satırında hatırlatır |

## 7. `gunluk/durum.json` nasıl düzenlenir

Betik her çalışmada bu dosyayı okur ve yazar. Elle değiştirebileceğiniz alanlar:

- **`ayarlar.hesap_tl`**: boyutların hesaplandığı hesap büyüklüğü (varsayılan 1.000.000).
- **`ayarlar.pratik_sahol_akbnk`**: `"kagit"` (varsayılan; PLAN_BIST K1 öncelikli) ya da `"canli"`.
- **`acik_pozisyonlar`**: gerçek pozisyonlarınız. Rapor her biri için çıkış kuralını hesaplar:
  - K4: iz-stop (E1) = girişten beri en yüksek kapanış × 0,85; `giris_fiyati` yazılıysa ve en yüksek kapanış girişin 2 katına ulaştıysa × 0,90 (E5); 120. iş günü süre çıkışı (E2). Yalnız "tut" gerektiren pozisyon bildirimde "İzle" satırına, stop/çıkış "İŞLEM" satırına yazılır.
  - K1: 20. iş günü, felaket stopu.
  - PRATIK_SAHOL: |z| ≤ 1,5.
  - KOZA, ALTIN, TUPRS: t+2 ve uzatma.
  - XU030_BAZ: ertesi gün.
  - 9.11'de bilançosu gelmemiş isimde "gece taşınmaz" uyarısı.
  ```json
  "acik_pozisyonlar": [
    {"kol": "K4", "enstruman": "ENJSA", "yon": "AL", "giris_tarihi": "2026-11-10", "giris_fiyati": 127.5, "adet": 100},
    {"kol": "KOZA", "enstruman": "TRMET/TRALT", "yon": "AL", "giris_tarihi": "2026-11-16"}
  ]
  ```
  Kapattığınız pozisyonu listeden silin.
- **`abd`** bloğu (PLAN_ABD §2.3–2.4 sayaçları):
  - `ftd_hacim_teyit`: FTD adayı çıktığında SPY ya da QQQ hacmine bakın. `true` ya da `false` yazın. `false` FTD'yi iptal eder. FRED'de hacim olmadığı için betik bunu bilemez.
  - `ftd.gun_dibi` (isteğe bağlı): FTD gününün gün içi en düşüğü (TradingView SP:SPX ya da NASDAQ:NDX). Yazılırsa ve sonraki bir kapanış bunun altına inerse YEŞİL olunmaz (PLAN_ABD §2.2). `ftd.olustu_1020` betik tarafından yazılır: FTD'den sonraki 15 seans içinde S&P ya da NDX'te 10 > 20 bir kez oluştuysa FTD geçerli kalır.
  - `pilot_freni`: bir SARI bölümünde ≥ 2 pilot 10 seans içinde stop olduysa `true`.
  - `manuel.s5fi`, `manuel.s5th`, `manuel.tarih`: TradingView INDEX:S5FI ve INDEX:S5TH. 3 günden eskiyse kullanılmaz. KIRMIZI (c) ve YEŞİL için gerekir.
  - `ralli`, `ftd`, `sari_sayac`, `son_tarih`: yalnız hata düzeltmek için değiştirin. Örnek: bir ABD günü yanlış sayıldıysa `son_tarih`'i bir önceki güne alın, `ralli` değerlerini o günkü hale getirin. Sonraki çalışma eksik günleri FRED'den sırayla yeniden işler.
  - `teyitsiz`: başlangıçta 06.11 S&P kapanışı (7.376,86) haber kaynağından alındı. FRED aynı günü yayımlayınca karşılaştırılır. Fark %0,1'i aşarsa raporda uyarı çıkar.
- **`bist`** bloğu: son başarılı BIST hesabının özeti ve yedek kip için tetikler. Elle değiştirmeyin.

Başlangıç durumu: `tarama/abd_rejim_20261106.md`.
- Ralli denemesinin 1. günü 06.11 (S&P ve NDX).
- S&P dip kapanışı 7.353,73 (05.11), NDX dibi 26.629,81.
- FTD yok, SARI sayacı 0, durum KIRMIZI.
- VIX/VIX3M: 05.11'de 1,10; resmi 06.11 kapanışı 25,64 / 24,60 = **1,04**. Abd_rejim notundaki gün ortası 23,67 değil.

## 8. Maliyetler

- **Veri:** ücretsiz kamu kaynakları (İş Yatırım, Borsa İstanbul, KAP, FRED, CBOE). Ücretli API yok.
- **Bulut çalışması:** her iş günü bir kısa Claude Code oturumu açılır. İş tek komut, commit ve bildirimden ibarettir. Kullanım Claude planınızın kotasından düşer, ayrı bir ücret yoktur. Komutun kendisi ~3 dk sürer ve hesaplama yükü küçüktür.
- **TradingView:**
  - Asgari 9 alarm için ücretli plan gerekir (Essential ya da üstü).
  - Koza, SAHOL/AKBNK ve XU030 bazı için BIST pay ve VİOP **gerçek zamanlı veri** paketi gerekir. Yoksa 15 dk gecikme olur ve bu üç sinyal aracı kurum ekranına bağlı kalır.
  - Güncel fiyatları TradingView'dan teyit edin.
- **İşlem maliyeti:** komisyon bacak ve yön başına ≤ 5 bps değilse K1 kâğıttır. Bireysel ~22 bps komisyonla PRATİK kenarların yarısı gider (PRATIK_LISTE §5).

## 9. Bilinen sınırlar

- **Sabit ölçekler:** Altın σ = %1,70 (rehber, 250 gün) ve XU030 baz σ = 50 bps (araştırma, 120 gün) sabittir. Yeniden hesaplamak için 120–250 bülten gerekir; her akşam indirmek pahalı.
- **Bayat gün filtresi yok:** İş Yatırım ChartData'da hacim, yüksek ve düşük yok. Bu yüzden PRATİK sinyallerde "bayat gün" (hacim 0, yüksek = düşük) filtresi uygulanamaz. Yalnız limit filtresi var.
  - Düzeltilmiş kapanış Yahoo 'adj' ile birebir aynı değildir; temettü günlerinde küçük farklar olabilir.
  - 06.11 değerleri: SAHOL/AKBNK z −0,63; Koza z3 0,71, σ60 195 bps, β_TA 0,69. Rehberdeki 04.11 değerleriyle (σ60 ≈ 194, β_TA 0,69) tutarlı.
- **Model durumları kendi geçmişinden kurulur:** K1, Koza ve SAHOL/AKBNK "model pozisyonu" geçmiş veriden yeniden oynatılır. Sizin gerçek pozisyonunuz değildir. Gerçek pozisyonları `acik_pozisyonlar`'a yazın.
- **Takvim statiktir.** Tablo 05.02.2027'ye kadar dolu. 2027 bayram tatilleri tahminidir; yıl başında BIST takviminden teyit edip `TATIL_BIST` listesini güncelleyin. KAP olayları otomatik değil: temettü, bedelsiz, ZPAT, TVF/birleşme, tedbir.
- **ABD rejimi:** FTD hacmi, FTD günü dibi ve S5FI/S5TH elle girilir. Bir ABD günü yalnız FRED S&P, CBOE VIX/VIX3M ve FRED NDX'in üçü de o günü yayımlayınca işlenir; biri gecikirse gün bir sonraki çalışmaya kalır (raporda not düşülür; denetim 08.11'den önce VIX'i geç gelen gün SARI sayacını sıfırlıyordu). Pilot freni gerçek işlemlere bağlıdır, elle girilir.
- **Tetik fiyatları:** K1 (z = ±2) ve Koza (z3 = ±1,5) tetikleri yarının penceresiyle kesin çözülür (denetim 08.11). `bist_sinyal.py`, `sinyal_koza.py` ve `koza.pine` yaklaşık değer verir: 06.11'de K1 93,06 / 84,09 (rapor 93,03 / 84,05), Koza 116,76 / 105,54 (rapor 116,92 / 105,16). PRATİK SAHOL/AKBNK ve K4 tetikleri zaten kesindi.
- **TUPRS ← ABD rafinerileri:** ABD tekil hisse verisi meşru ve ücretsiz bir kaynaktan yok. Yalnız TradingView alarmıyla izlenir.
- **XU030 bazı:** rapordaki değer bülten kapanış fiyatıyla hesaplanır ve yalnız bilgidir. Kural canlı 18:10 fiyatı ister.
- **Pine dosyaları** (`koza_alarm.pine`, `tuprs_alarm.pine` ve mevcutlar) derlenmedi.
