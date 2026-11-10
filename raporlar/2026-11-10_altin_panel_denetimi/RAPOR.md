# TRALT ve ons altın vadelisi: panel ve strateji denetimi (10.11.2026)

Yatırım tavsiyesi değildir. Veri: Borsa İstanbul VİOP günlük bültenleri (17.12.2018 → 09.11.2026) ve Yahoo Finance. Varsayımlarım: "TRALT futures" Türk Altın İşletmeleri pay vadelisi; "sinyal ajanları" paneldeki izleme araçları ve 04.11 tarihli rehberlerdeki sinyaller; işlemler hedge'siz (karşı pozisyonsuz) yapılıyor.

Terimler: **bps** = baz puan, %0,01 (100 bps = %1). **z** = bir hareketin kendi olağan oynaklığının kaç katı olduğu. **t** = bir ortalamanın şanstan ayırt edilebilirliği; kabaca 2'nin altı "ayırt edilemiyor" demek. **Uzlaşma** = VİOP'un gün sonu resmi fiyatı.

## Kısa yanıt

1. **Panel kusurlu.** Sekiz izleme satırının beşi aynı şeyi (altın fiyatını), ikisi aynı madenci sepetini gösteriyor. Yüzdeler farklı saatlerden ölçüldüğü için yan yana okunamıyor: bugünkü ekranında GDX −%0,96 yazıyor, gerçek düşüş −%4,6 idi.
2. **Ons altın için sinyal yok.** Paneldeki hiçbir şey ons altın vadelisinin sonraki 1–3 gününü öngörmüyor (66 testte 0).
3. **TRALT için tek dayanak altının o günkü hareketi; o da zayıf** ve önceden koyduğumuz ölçütü geçmiyor.
4. **Para kazandırdığı kanıtlı değil.** Hedge'siz ve bireysel maliyetle işlem başı beklenti sıfırdan ayırt edilemiyor. 20 bin USD'lik pozisyonda bir yılın sonucu geçmişe göre −8 bin ile +10 bin USD arasında, zararlı yıl olasılığı %42. 2021–23'te üç yıl üst üste zarar etti.
5. **Kazandıran bir düzeltme bulamadım.** Riski azaltan ve paneli doğrultan adımlar var; aşağıda.

## Ne yapmalıyım

1. **Ons altın vadelisinde bu panelle 1–3 günlük yön işlemini bırak.** Öngörü yok; maliyet ve kazançta %10 stopaj (kaynakta kesilen vergi; 2026 teyidi eksik) var. Uzun süre altın tutmak ayrı bir konu, burada test edilmedi.
2. **TRALT'ta en dürüst seçenek önce kâğıt üzerinde işlem.** 05.11'den beri kurala göre açılan işlem sayısı sıfır; elde gerçek sınav yok.
3. **Gerçek parayla sürdüreceksen boyutu kayıptan geriye hesapla.**
   - Son 12 ayda TRALT vadelisinin 2 günlük tipik oynaması %5,8, kötü %1'lik gün −%13,4.
   - 20 bin USD pozisyonda bu, işlem başına tipik ±1.150 USD, kötü günde −2.700 USD demek.
   - Geçmişte hedge'siz sürümün en kötü birikimli düşüşü pozisyon büyüklüğünün yaklaşık 1,1 katıydı: sabit 20 bin USD pozisyonla ~22 bin USD.
   - Başlamadan önce "toplam şu kadar USD kaybedersem bırakırım" tutarını yaz. Tavan/taban kilidi günlerinde (2026'da 6 gün) çıkış yapılamayabilir.
4. **Sinyali aynı saatten ölç.** 17:55'te spot altın (TVC:GOLD) fiyatını dünkü 17:55 fiyatına böl. Eşik bugünlerde yaklaşık ±%1,7–1,8 (z = ±1). Satırlardaki günlük yüzdeyi kullanma. Örnek: bugünkü ekranında VİOP altını −%1,68, yani z ≈ −0,95; eşiğin altında, kurala göre sinyal yok.
5. **XU030 vadelisiyle hedge'i risk için düşün, kazanç için değil.** İşlem başı oynaklığı 401'den 342 bps'e, en kötü düşüşü yaklaşık yarıya indiriyor. Kazancı artırdığı kanıtlı değil (bkz. 3. bölüm). 20 bin USD TRALT için yaklaşık 8 kontrat F_XU030 eder; üçüncü bir araç, ek teminat ve ek maliyet demektir.
6. **Maliyetini öğren.** Aracı kurumundan VİOP komisyonunu yazılı al. Hedge'siz kuralın brüt getirisi işlem başı 34,5 bps; gidiş-dönüş maliyetin (komisyon + borsa payı + alış-satış farkı) ne kadar yüksekse o kadarı gidiyor.
7. **Paneli sadeleştir** (tablo 1. bölümde): GLD, PHYS, COMEX GC ve GDXJ'yi çıkar; XU030 vadelisini ve TRENJ'i ekle.
8. **Her işlemi kaydet:** tarih, 17:55 z değeri, emrin gerçekleştiği fiyat, o günün uzlaşması, maliyet. Dolum ile uzlaşma arasındaki fark hiç ölçülmedi; kenarı en çok o eritir.
9. **Olay günü girme.** Sabah KAP'ta TRALT, TRMET, TRENJ haberine bak.

## Gerekçe ve kanıt

### 1. Panelin kusurları

**Tekrar.** 2024-06'dan beri aynı saatte ölçülen günlük değişimlerde GLD–PHYS korelasyonu 0,99, GDX–GDXJ 0,99. Dört altın satırının (VİOP ons, COMEX, GLD, PHYS) ortak bileşeni değişimin %91,5'ini açıklıyor. Yani panel üç ayrı bilgi taşıyor: altın, madenci sepeti, Koza grubu.

**Yüzdeler karşılaştırılamıyor.** Ekran görüntün (bugün, yaklaşık 17:40):

| Satır | Ekranda | Önceki kapanışa göre gerçek |
|---|---|---|
| GLD | −%0,12 | −%2,3 |
| PHYS | −%0,15 | −%2,4 |
| GDX | −%0,96 | −%4,6 |
| GDXJ | −%1,40 | −%5,3 |
| Spot altın | −%2,30 | (kendi gün dönümüne göre) |
| VİOP ons altın | −%1,68 | (dünkü uzlaşmaya göre) |
| COMEX altın | −%1,58 | (dünkü COMEX uzlaşmasına göre) |

Aynı varlık üç satırda üç ayrı yüzde gösteriyor, çünkü her satır başka bir saatten ölçüyor. ETF satırları ise önceki kapanışa göre değil, açılışa yakın bir fiyata göre hesaplanmış görünüyor (nedenini doğrulayamadım). Bu ekrana bakan biri "madenciler altından iyi dayanıyor" der; gerçekte altının iki katı düşmüşlerdi.

**Zamanlama.** ABD seansı kışın 17:30, yazın 16:30'da açılıyor (veriden doğrulandı). 17:55'te ETF'lerde bugünün yalnız 25–85 dakikası var. Tamamlanmış son ABD seansının değişimi ile VİOP altınının bugünkü değişimi arasındaki korelasyon yalnız 0,17–0,21.

**Eksikler.** TRALT'ın en büyük sürücüleri panelde yok: BIST 30 (önceki rehbere göre TRALT'ın piyasa betası ~1,25) ve Koza grubu haberi. Ana grafikteki bant ve ortalama da test edildi; 1–3 gün için öngörü yok (t 0,2–0,3).

| Satır | Durum | Karar |
|---|---|---|
| TRALT1! | İşlem aracı | Kalsın; bandı sinyal sayma |
| XAUUSD1! | İşlem aracı | Kalsın |
| TVC:GOLD | Tek sinyal girdisi | Kalsın; 17:55'ten 17:55'e ölç |
| GLD, PHYS | Altının kopyası | Çıkar |
| COMEX GC | Altının kopyası | Çıkar |
| GDX | Ek bilgi ölçütü geçmedi | İstersen bağlam; işlem yok |
| GDXJ | GDX'in kopyası | Çıkar |
| TRMET1! | Grup ve olay bağlamı | Kalsın; sinyal değil |
| USDTRY | Öngörü yok | Bağlam |
| XU030D1! | Piyasa yönü, hedge | Ekle |
| TRENJ | Grup haberi | Ekle |

### 2. Sinyaller ne öngörüyor

Yöntem: her araç için "17:55'te bilinen hâli, altının o günkü hareketinin ötesinde sonraki 1–3 günü öngörüyor mu?" sorusu soruldu. 222 test; çok sayıda test yapıldığı için eşik sıkılaştırıldı (FDR düzeltmesi).

Sonraki 2 gün, 1σ'lık hareket başına etki:

| Öngörücü | TRALT (bps / t) | Ons altın (bps / t) |
|---|---|---|
| Altının o günkü hareketi | +25,7 / 2,40 | −0,6 / −0,13 |
| GDX, son ABD seansı | +26,3 / 2,34 | +3,3 / 0,78 |
| GDXJ, son ABD seansı | +32,6 / 2,47 | +3,6 / 0,90 |
| GLD, son ABD seansı | +14,5 / 1,44 | −2,5 / −0,60 |
| PHYS, son ABD seansı | +15,1 / 1,43 | −3,2 / −0,78 |
| TRMET'in göreli hareketi | +6,9 / 0,52 | +5,6 / 1,53 |
| USDTRY vadelisi | −7,9 / −0,55 | −1,2 / −0,50 |
| Bant konumu (%b) | +3,2 / 0,21 | +4,4 / 0,80 |

- **Ons altın:** hiçbir satır geçmedi. Altının bugünkü hareketi kendi sonraki iki gününü de öngörmüyor. Bu testler güçlü (1.800+ gün); "öngörü yok" hükmü sağlam.
- **TRALT:** altın ve madenci satırları t 2,3–2,5 bandında ama çoklu test eşiğini geçemedi (q 0,12 > 0,10). Altın sinyali de buna dahil.
- **Tek geçen:** GDXJ'nin GDX'e göre farkı (t 3,38). Çürütme testinde düştü: aynı sinyal hiç ilgisi olmayan BIST 30'u da "öngörüyor" (t 4,02) ve 2022'den beri anlamsız (t 1,5). Muhtemelen sahte; kullanma.
- Saatlik veriye dayanan testler (altının gece/gündüz ayrımı, GDX'in o ana kadarki hareketi) yalnız 2 yıllık veriyle yapılabildi; sonuç "yetersiz güç", yani ne var ne yok denebiliyor.

Literatür aynı yönde (özet düzeyinde görüldü, ikinci kontrol yapılmadı): GLD–GDX farkı sonraki haftayı açıklamıyor (CXO, 2006–2016); altın vadelisinde teknik kurallar maliyet sonrası kâr üretmiyor (Anderson & Faff; Marshall ve ark.); belgelenen momentum aylık ufukta, günlük değil.

### 3. Strateji para kazandırır mı

Kural: altın z'si ±1'i aşınca aynı yönde gir, 2 gün sonra çık. 408 işlem, yılda ~52. Bireysel maliyet varsayımı TRALT için gidiş-dönüş 23 bps, ons altın için 10 bps; düşük maliyet 8 ve 3 bps. Senin gerçek maliyetin bu ikisinin arasında bir yerde olmalı.

| Kural | Brüt | Net, düşük maliyet (t) | Net, bireysel (t) | En iyi %2 işlem hariç |
|---|---|---|---|---|
| TRALT, hedge'siz | 34,5 | 26,5 (1,34) | 11,5 (0,58) | −12,7 |
| TRALT − ons altın | 31,9 | 22,0 (1,14) | 2,6 (0,13) | −17,4 |
| Ons altın, sinyali izle | 8,2 | 5,2 | −1,8 (−0,23) | −13,4 |
| Ons altın, tersine gir | −8,2 | −11,2 | −18,2 (−2,35) | −27,0 |
| TRALT − β·XU030 (kıyas) | 53,7 | 43,2 (2,55) | 23,9 (1,41) | +2,8 |

- **Hiçbiri önceden konan "kazandırır" ölçütünü geçmedi** (bireysel maliyetle t ≥ 2, en iyi %2 işlem çıkınca hâlâ pozitif, üç dönemin en az ikisinde pozitif).
- **Sonuç birkaç büyük işleme bağlı.** En iyi 9 işlemi çıkarınca hedge'siz kural negatife dönüyor.
- **Döneme bağlı.** Hedge'siz kural, bireysel maliyetle işlem başı: 2019–20 +52,6; 2021–23 −66,5; 2024–26 +49,9 bps. 20 bin USD'lik pozisyonla 2021, 2022 ve 2023 sırasıyla yaklaşık −7,1, −6,4 ve −4,8 bin USD.
- **Bu yıl çok iyi gitti** (2026: +6.542 bps toplam). Altın–TRALT bağı şu an güçlü (120 günlük korelasyon 0,50). 2020 de böyleydi; ardından 2021 geldi. Yıl içinde de düz gitmedi: önceki rehbere göre Eylül–Ekim 2026'daki fon krizinde hedge'li kuralın 7 işlemi ortalama −82 bps kaybetti.
- **Yıllık beklenti** (geçmiş yarıyılların rastgele yeniden örneklenmesi, 20 bin USD, bireysel maliyet):

| Kural | Ortalama | %5 – %95 | Zararlı yıl olasılığı |
|---|---|---|---|
| TRALT, hedge'siz | +1.117 USD | −8.002 … +10.395 | %42 |
| TRALT − ons altın | +306 USD | −8.662 … +9.157 | %50 |
| TRALT − β·XU030 | +2.463 USD | −4.879 … +10.548 | %34 |

- **Bu rakamlar iyimser tarafta.** Sinyal uzlaşma fiyatından ölçüldü, sen 17:55'te ölçüyorsun (önceki çalışmada bu fark işlem başı 4–13 bps götürüyordu). Fiyat kayması eklenmedi. Kural da aynı veriye bakılarak seçildi. Dürüst özet: **beklenen kazanç sıfır dolayında; işareti veriden bilinemiyor.**
- **Likidite sorun değil.** 20 bin USD = 246 TRALT kontratı (günlük miktarın %0,09'u) ya da ~5 ons altın kontratı.

**Hedge'li sürüm neden daha iyi görünüyor?** İşlem listesini iki bacağa ayırdım. Hedge'li sürümün fazladan 19,2 bps'i TRALT'tan değil, XU030 bacağının kendi kazancından geliyor (t 1,67; şanstan ayırt edilemiyor, çoğu 2021–23'te). Bu kısım sıfır sayılırsa hedge'li sürümün düşük maliyetli neti +24 bps'e (t 1,42) iniyor. Hedge'in kalıcı faydası oynaklığı düşürmesi.

**Taban oran.** Hindistan'da bireysel vadeli/opsiyon yatırımcılarının %93'ü üç yılda zarar etti (SEBI, 2024). Brezilya'da 300 günden fazla gün içi vadeli işlem yapanların %97'si zarar etti (Chague ve ark.). Bunlar başka ülkeler ve daha kısa vadeli işlemler; yine de kısa vadeli bireysel vadeli işlemde çoğunluğun kaybettiğini gösteriyor. VİOP için resmî bir istatistik bulunamadı.

### 4. İyileştirme denemeleri

- **XU030 hedge'i:** riski azaltır; kazanç katkısı kanıtsız (yukarıda).
- **"Bağ güçlüyken işlem yap" süzgeci** (keşif hesabı, doğrulanmadı): TRALT–altın 120 günlük korelasyonu 0,20'nin üstündeyken işlem. Ortalamayı yükseltiyor (bireysel net +38,6, t 1,19) ama asıl sorunu çözmüyor: 2021–23'te süzgecin "açık" dediği 50 işlem ortalama −135 bps kaybetti. Pencere ve eşik değişince sonuç t 0,5 ile 2,2 arasında oynuyor. Kullanılamaz.
- **"Son 20 işlem kârdaysa devam et" süzgeci:** işe yaramıyor; tersine, kötü serilerden sonraki işlemler daha iyi.
- **GDXJ/GDX farkı:** çürütüldü (2. bölüm).
- **Ons altın bacağıyla hedge (TRALT − altın):** getiriyi sıfırlıyor. Ayrıca akşam seansında (19:00–23:00) ons altın açık, TRALT kapalı; iki bacak gece eşleşmiyor.

### 5. Düzeltilen varsayımlar

- **"Çok altın aracı izlersem daha çok sinyalim olur."** Hayır; aynı fiyatın kopyaları.
- **"Bu araçlar ertesi günü öncülüyor."** ABD seansı BIST'ten sonra kapanıyor. Önceki çalışmada bulunan öncülükler (madenciler ve gece altını → TRALT) ertesi sabahın açılış boşluğunda fiyatlanıyor. Kapanıştan kapanışa işlem yapan bunu sinyal olarak kullanamıyor.
- **"TRALT vadelisi bir altın kontratı."** Bir hisse vadelisi. Altınla günlük korelasyonu 0,33; TRMET ile 0,76. Grup haberi ve BIST altından daha belirleyici.
- **Önceki araştırma ajanının notu:** pay vadelisinde günlük limit ±%20 değil. Bültende Nisan 2020'den beri fiyatlar tam ±%10'da kesiliyor.

## Emin olunmayanlar ve doğrulama kapsamı

**Yapılan doğrulama**
- Hesap: karara temel olan 5 sayı bağımsız bir kodla ham veriden yeniden üretildi. Farklar ≤ 2 bps; fark kaynağı (kilit günü çıkışın ertelenmesi) eklenince birebir. Kodlarda ileriye bakma (geleceği görme hatası) bulunmadı. İki kod ajanı veriyi ayrı ayrı hazırladı.
- Önceki araştırma kuralı (hedge'li, düşük maliyet) bu çalışmada iki bağımsız kodla yeniden üretildi: n 408, +43 bps, t 2,55.
- Yöntem hesaptan önce denetlendi (12 düzeltme uygulandı); taslak sonuçlara 8 itiraz geldi, hepsi rapora işlendi. En önemlileri: "sıfıra yakın pozitif" yerine "sıfırdan ayırt edilemiyor"; hedge yalnız risk için; işlem başı beklenti rakamı verilmedi.
- İddia defteri: 20 iddia kontrol edildi. 4'ü doğru, 2'si düzeltildi, 14'ü için kaynak bu oturumda görülemedi (birinde aritmetik düzeltildi); bunlar rapora girmedi ya da "doğrulanmadı" diye etiketlendi.

**Doğrulanmadı ya da açık**
- Gerçek bireysel maliyet. Tek bir aracı kurum tarifesi görüldü (yalnız komisyon, gidiş-dönüş ~4–6 bps; borsa payı, vergi ve alış-satış farkı hariç). 23 bps muhtemelen üst sınır.
- %10 stopajın 2026'da geçerliliği (Borsa İstanbul sayfasıyla tutarlı; 2026 tarihli karar görülmedi) ve zararla mahsubu.
- ETF satırlarındaki yüzdenin neden farklı çıktığı. Kendi ekranında GLD yüzdesini izleme listesindeki yüzdeyle karşılaştır.
- Uzlaşma yerine 17:55 fiyatıyla sinyal ve gerçek dolum kayması bu çalışmada ölçülmedi.
- Saatlik testler yetersiz güçte. 05.11 sonrası gerçek örneklem dışı işlem yok.
- Rejim süzgeci hesabı tek kodla yapıldı, bağımsız tekrar edilmedi.
- Literatür satırları özet düzeyinde; ikinci kontrol yapılamadı.

## Kaynaklar

- Borsa İstanbul VİOP günlük bültenleri: `borsaistanbul.com/data/vadeli/viop_YYYYAAGG.csv` (2.012 gün).
- Yahoo Finance grafik verisi (günlük, saatlik, 5 dk).
- Borsa İstanbul, VİOP vergilendirme: https://borsaistanbul.com/piyasalar/viop/piyasa-isleyisi/vergilendirme
- VİOP akşam seansı: https://www.gcmyatirim.com.tr/egitim/makaleler/viop-aksam-seansi-rehberi
- Komisyon örneği: https://strateji.com.tr/wp-content/uploads/2025/12/Ucret-Masraf-ve-Komisyon-Bilgilendirilmesi-2025-12-04.pdf
- SEBI, Eylül 2024: https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html
- Chague, De-Losso, Giovannetti, "Day Trading for a Living?": https://papers.ssrn.com/abstract_id=3423101
- CXO Advisory, GLD–GDX: https://www.cxoadvisory.com/technical-trading/simple-gold-gold-stock-fund-pair-trading
- TradingView, çubuk değişim değerleri: https://www.tradingview.com/blog/en/bar-change-values-added-9502
- Önceki çalışmalar: `raporlar/2026-11-04_kapanis_1-3gun/rehber/altin/REHBER_altin.md`, `rehber/koza/REHBER_koza.md`, `raporlar/2026-11-02_viop_leadlag/hisse_kartlari/TRALT.md`.
- Ekler: `ek/` (yöntem, ajan çıktıları, doğrulama), `kod/`, `hesap/` (tablolar, işlem listeleri).

## Devam notu

1. Bulgu: panel tekrarlı ve yüzdeleri yanıltıcı; ons altın için öngörü yok; TRALT'ta altın sinyali zayıf (t 2,4, ölçütü geçmedi); hedge'siz ve bireysel maliyetle beklenti sıfırdan ayırt edilemiyor.
2. Dosyalar: bu rapor; `ek/00_yontem.md` (şartname), `ek/K1_panel_testleri.md`, `ek/K2_strateji_beklentisi.md`, `ek/V1_bagimsiz_hesap.md`, `ek/V2_defter_dogrulama.md`.
3. Hesap: `kod/K1`, `kod/K2`, `kod/V1`, `kod/ana/rejim_kesif.py`; çıktılar `hesap/`. Ham veri depoda yok; `kod/00_indir.py` ile yeniden iner.
4. Açık: gerçek komisyon, 17:55 dolum kayması, stopajın 2026 teyidi, ETF yüzdesinin nedeni.
5. Sıradaki mantıklı iş: kullanıcının gerçek işlem kaydıyla (dolum, maliyet) 2–3 ay sonra yeniden ölçüm.

Maliyet özeti: Seviye M · 8 alt ajan: 7 sonnet (3 araştırma, 2 kod, 2 doğrulayıcı) + 1 opus (yöntem denetimi ve eleştirmen, aynı ajan iki tur) · 1 üretim dalgası (araştırma ve hesap iki adımda) + doğrulama · bütçesini aşan ajan yok · aşılan sınır yok.
