# Yöntem planı (hesaptan önce yazıldı) — ABD piyasası, kapanış sinyali, 1–3 gün taşıma

Sürüm 2 (21.11.2026). Sürüm 1, yöntem denetçisinin (`ajanlar/d2_M.md`) 15 itirazıyla yeniden yazıldı; itirazların hepsi kabul edildi. Bu sürüm hesaptan önce kilitlendi. Sonuçlar görüldükten sonra eşik değiştirilmez; değişiklik olursa "Sapmalar" başlığına yazılır.

## 1. Profil ve soru

- Yatırımcı gün içi işlem yapmıyor. Karar ABD kapanışında (16:00 ET; TSİ 00:00 kış, 23:00 yaz) veriliyor, pozisyon 1–3 işlem günü taşınıyor.
- Soru: ABD ETF ve hisselerinde, kapanışta bilinen bir sinyalle (özellikle lead-lag) maliyet sonrası anlamlı ve **uygulanabilir** kazanç bırakan kurallar var mı; hangi araçla?
- Ölçü: işlem başına net beklenti (bps ve getiri/σ), yılda işlem sayısı, başabaş maliyeti, en kötü işlem, günlük kâr/zarar serisinin en büyük düşüşü.

## 2. Veri

- Günlük açılış/yüksek/düşük/kapanış/hacim ve düzeltilmiş kapanış, Yahoo chart API, 2005-01-03 → 2026-11-20, 470 kod (`veri/evren.csv`). Düzeltilmiş açılış = açılış × düzeltilmiş kapanış / kapanış. İleri doldurma yok.
- Tarih, borsanın yerel takvim günüdür. **Kapanış saati tablosu** hesaptan önce çıkarılır (her serinin günlük çubuğu ET ile kaçta kapanıyor). Sınıflar:
  - `ABD16`: 16:00 ET. Sinyal girdisi olarak aynı gün kullanılır.
  - `ONCE`: 15:45 ET'den önce kapananlar (Asya/Avrupa endeksleri; CBOE faiz endeksleri tabloyla doğrulanırsa). Aynı gün kullanılır.
  - `SONRA`: 15:45 ET'den sonra kapananlar (kripto, döviz, vadeli; **^VIX ailesi dahil, 16:15**). Sinyalde **yalnız 1 gün gecikmeli**. Aynı gün bilgisi için 16:00'da kapanan vekiller: VIXY (volatilite), UUP/FXE/FXY, USO/BNO, GLD/SLV, CPER, TLT/IEF, IBIT (2024'ten). GBTC 2024 öncesi vekil sayılmaz. Kripto için 16:00 ET anlık fiyatı saatlik mumlardan kurulur.
  - Aynı gün ^VIX yalnız "sızıntılı üst sınır" satırıdır. Rejim kovası VIX(t−1) ile atanır.
- Bütün yüzdelik/çeyreklik eşikler genişleyen pencereyle, yalnız t−1'e kadar veriyle hesaplanır. Kayan β ve z-skoru pencereleri t−1'de biter (z'nin payındaki t günü getirisi hariç).
- Bilanço günü: SEC 8-K 2.02 kabul damgasının gösterdiği gün ile komşu iki günden, hacmi 20 günlük ortalamaya oranı en yüksek olan gündür; iki yöntem uyuşmuyorsa olay atılır. 50 olaylık örneklemle hata oranı raporlanır; %5'i aşarsa bilanço ailesi KOŞULLU'nun üstüne çıkamaz.
- Konumlanma (DIX/GEX) kapanıştan sonra yayımlanır: giriş ertesi açılış.
- Tek kaynak Yahoo: ayakta kalanların sinyal günleri ikinci bir kaynakla karşılaştırılır; farkı > 10 bps olan gün oranı raporlanır. Fiyat düzeyi kullanan sinyaller (RSI, hareketli ortalama) yalnız bölünme düzeltmeli fiyattan da hesaplanır; tetiklenme günleri %95'ten az örtüşüyorsa not düşülür.

## 3. Evren ve hayatta kalma yanlılığı

- Panel bugünün listesinden kuruldu; iflas eden ya da borsadan çıkan hisseler ve kapanan ETF'ler yok. Bu, uzun yönlü "düşeni al", çift dönüşü ve bilanço sonuçlarını şişirir.
- Hisse evreni dönem başı bilgisiyle kurulur: IS için 01.01.2010, OOS için 01.01.2020, son dönem için 01.01.2024 öncesindeki 250 günün dolar hacmine göre ilk 150 hisse.
- Birincil ölçü **anormal getiri**: koşullu ortalama − aynı varlığın aynı dönem ve aynı VIX kovasındaki koşulsuz h günlük ortalaması.
- Hissede yalnız uzun yönde çalışan, kısa yönde karşılığı olmayan sinyal en çok KOŞULLU; uzun−kısa farkı ayrıca raporlanır.
- Bugünkü tema nedeniyle seçilen ya da 2015 sonrası halka açılan hisseler "tema" sınıfıdır: en çok DÜŞÜK.
- Birleşme öncesi kabuk dönemleri (QUBT, WULF, MARA, CLSK, LEU, KEEL) kesilir; 60 günlük dolar hacmi 20 milyon $ altındaki günler hedef olarak kullanılmaz.

## 4. Giriş, çıkış ve korunma

- Giriş K: t kapanışı. Giriş A: t+1 açılışı. Giriş G: t+1 kapanışı (bir gün gecikme).
- Çıkış: t+h kapanışı, h ∈ {1,2,3}. Ek varyant: çıkış t+1 açılışı (gece tutma). Ek çıkış kuralları (ilk kârlı kapanış, zaman durdurması) ayrı varyanttır ve test sayısına katılır.
- **Kapanış gerçekçiliği:** kapanış emri kesimi NYSE 15:50, Nasdaq 15:55. Bu yüzden UYGUN için (a) Giriş A'da net > 0 ve t ≥ 1,5, ya da (b) 60 dakikalık veride (son ~730 gün) 15:30 çubuğunun açılış fiyatıyla hesaplanan sinyal, ≥ 30 olayda, Giriş K kazancının ≥ %70'ini koruyor. Dönüş aileleri (B, D, F) için (a) zorunlu. İkisi de yoksa en çok KOŞULLU ve "yalnız kapanışta giren için, doğrulanmadı" notu.
- Korunma: her ayakta kalan için üç uygulama satırı: (i) korunmasız, (ii) SPY/sektör ETF'i açığa satışıyla, (iii) ters ETF ya da mikro vadeli ile. UYGUN etiketi yatırımcının uygulayabileceği satıra göre verilir; yalnız (ii)'de geçen "açığa satış gerektirir" notuyla KOŞULLU. β hem 250 hem 60 günlük pencereyle hesaplanır; işaret değişiyorsa sinyal elenir. Kaldıraçlı ETF satırı gerçek ETF fiyatından hesaplanır.

## 5. Dönemler ve rejim

- Ana hat: IS 2010–2019, OOS 2020–2023, son dönem (kilitli) 2024-01-01 – 2026-11-20. 2005–2009 stres dönemi.
- Ek ölçüt: IS + OOS takvim yıllarının ≥ %65'inde net pozitif; OOS'tan 2020 ve 2022 ayrı ayrı çıkarılınca işaret korunuyor; OOS Şubat–Nisan 2020 hariç tutulunca da.
- **"Yeni yapı" hattı** (2020 sonrası doğan yapılar: spot kripto ETF'leri, tek hisse kaldıraçlı ürünler, yapay zekâ teması, günlük vadeli opsiyonlar): yalnız önceden yazılı hipotezler, IS 2020–2023, OOS 2024–2026, eşik OOS t ≥ 3 ve BH %5; en çok KOŞULLU; ayrı tabloda.
- Rejim iki boyutludur ve önceden yazılıdır: VIX(t−1) kovası (< 20, 20–30, > 30) × SPY'nin t−1'de 200 günlük ortalamasının üstünde/altında olması. Rejim kovaları test sayısına katılır.
- VIX > 30 analizi 2005–2026'nın tamamını kullanır ve **bölüm** bazında raporlanır (bölüm: aralarında 20 günden az boşluk olan VIX > 30 günleri). "Bugünkü rejimde destekli" etiketi: ≥ 4 bölüm, bölümlerin ≥ %70'inde aynı işaret, en büyük bölüm çıkarılınca işaret korunuyor, maliyet ×2 ile net > 0. Aksi hâlde "bugünkü rejimde sınanmadı" ya da "bugün kullanma". Raporda iki sütun: genel karar ve bugünkü rejim kararı.

## 6. Sinyal aileleri (önceden yazılı)

| Aile | Tanım |
|---|---|
| A. Lider → takipçi | X'in t günü (artık) getirisi Y'nin sonraki h gününü aynı yönde öngörür; dev şirket bilançosunun ertesi gün sektör ETF'ine etkisi dahil |
| B. Göreli gecikme, çift, kesitsel dönüş | Y'nin benzerine/sektörüne göre 1–5 günlük artığı; çift z-skoru; sektör-nötr sıralama sepetleri (en kötü beşte birlik uzun, en iyi kısa) |
| C. Çapraz varlık → endeks/sektör | Kredi, faiz, dolar, petrol, altın, bakır, kripto; büyük → küçük şirket gecikmesi; yüksek beta/düşük oynaklık farkı; ülke ETF'leri |
| D. Kendi serisi ve kapitülasyon | Büyük düşüş/yükseliş, üst üste k gün, RSI(2), kapanışın gün içi aralıktaki yeri (IBS), VIX sıçraması, VIX − gerçekleşen oynaklık, evrenden hesaplanan genişlik |
| E. Takvim/olay | Ay dönümü, FOMC ve makro duyuru günleri, opsiyon vadesi, tatil öncesi, yıl sonu (vergi zararı satışı, Ocak dönüşü), endeks dengelemeleri, ay/çeyrek sonu yeniden dengeleme, tahvil ay sonu |
| F. Volatilite ürünleri | VIX vade yapısı → VIXY (birincil), SVXY/UVXY. SVXY ve UVXY 28.02.2018 öncesi ve sonrası ayrı araçtır. Kısa volatilite sonuçlarına XIV'in 5–6 Şubat 2018 kaybı elle eklenir; "olay dahil / hariç" iki satır |
| G. Bilanço | İlk tepki günü kapanışında giriş (hissenin kendisi ve henüz açıklamamış emsalleri); bilanço öncesi prim |
| H. Konumlanma | DIX, GEX → SPY/QQQ; giriş ertesi açılış |
| N. Gece–gündüz | Kapanışta gir, ertesi açılışta çık; bütün ailelere "çıkış: t+1 açılış" varyantı |
| S. Sistematik tarama | Aşağıdaki özel kural |

Kaynağı olan her kural için yayın yılı yazılır; yalnız yayın sonrası dönem doğrulama sayılır. Kurallar `veri/hipotezler.csv` dosyasında hesaptan önce listelenir.

## 7. İstatistik

- Her kuralın **günlük takvim-zamanı kâr/zarar serisi** kurulur: aynı gün açık pozisyonlar eşit ağırlıklı tek portföy, en çok 5 eşzamanlı pozisyon (fazlası sinyal gücüne göre seçilir).
- Anlamlılık bu seriden ve işlem listesinden: (1) durağan blok bootstrap p-değeri (ortalama blok 10 gün, 5.000 tekrar); (2) oynaklığa ölçeklenmiş işlem getirisinin (getiri / hedefin t−1'e kadar 20 günlük σ'sı) t'si; (3) Wilcoxon işaretli sıra testi ve medyan. UYGUN için üçü aynı yönde, en az ikisi p < 0,05. Havuzlanmış olaylarda standart hata tarihe göre kümelenir.
- Sağlamlık: en iyi %5 işlem (en az 3) çıkarılınca; en iyi takvim ayı çıkarılınca; maliyet ×2; komşu parametreler (eşik ±0,5, pencere ±%50).
- **Önceden yazılı ailelerde çoklu test:** IS'te aynı yön ve t ≥ 2 → aday; OOS'ta bütün adaylar (aileler birleşik) üzerinde Benjamini–Hochberg %10.
- **Sistematik tarama (S):**
  1. Korelasyonu > 0,98 olan kodlar teke indirilir. Hedef Y yalnız 60 günlük hacmi ≥ 200 milyon $ ve sıfır hacimli günü olmayan kodlar.
  2. Test istatistiği: Y'nin korunmalı ileri getirisinin, X'in artık getirisine (X − β·SPY − β·sektör) regresyonundaki katsayı; Y'nin ve SPY'nin t günü getirisi kontrol değişkenidir (piyasanın kendi gecikmesi ve hedefin kendi dönüşü ayıklanır).
  3. Evren yalnız IS verisiyle ≤ 60 sepete kümelenir; tarama sepet → sepet ve sepet → üye düzeyinde yapılır.
  4. IS: |t| ≥ 3,5 olanların en yüksek 200'ü aday. OOS: aynı yön ve 200 aday üzerinde BH %10.
  5. **Boru hattı plasebosu:** IS seçimi → OOS onayı zincirinin tamamı yeniden çalıştırılır. Hedef getiri matrisi bütün Y'ler için aynı permütasyonla, 20 günlük bloklar hâlinde, aynı yıl ve aynı VIX kovası içinde yer değiştirir; X sinyalleri yerinde kalır; ≥ 200 tekrar. İkinci plasebo: sinyal +40…+250 gün dairesel kaydırılır. Gerçek OOS geçen sayısı plasebo %95'liğini aşmıyorsa tarama "başarısız" ilan edilir ve taramadan gelen hiçbir sinyal DÜŞÜK'ün üstüne çıkamaz. Tekil p-değerleri plasebodaki en yüksek |t| dağılımına göre verilir.
- **Portföy düzeyi:** ayakta kalanların günlük kâr/zarar serileri arasındaki korelasyon ve aynı gün tetiklenme oranı raporlanır; korelasyonu > 0,5 olanlar tek sinyal sayılır, en basit kural tutulur. Her ayakta kalan üç genel faktöre regresyonla sınanır: SPY'nin 1 günlük dönüşü, "VIX > 30'da düşüş gününden sonra al", gece sürüklenmesi. Kalan alfa t < 2 ise "genel faktörün türevi" etiketi alır. Birleşik portföyün en büyük düşüşü ve en kötü 5 günü verilir.
- Bağımsız çürütme: ayakta kalan her sinyal, motoru kullanmayan ayrı bir kodla yeniden üretilir.

## 8. Maliyet

- Bacak maliyeti = max(hacim kademesi, 0,5 sent / fiyat) + komisyon. Hacim kademesi (60 günlük dolar hacmi): > 1 milyar $: 1,5 bps; 200 milyon–1 milyar: 3; 50–200 milyon: 7; < 50 milyon: 15; kaldıraçlı/ters ETF'ye +1.
- Komisyon üç senaryo: hisse başı 0,005 $ (en az 1 $; 10.000 $'lık emir), emir başı sabit 1,5 $ (10.000 $'lık emir), oransal 20 bps.
- VIX(t−1) > 30 günlerinde maliyet ×2. Açığa satışta ödünç: yıllık %0,5 (genel), zor ödünç alınanlarda %10 ayrıca.
- Uzun pozisyon getirilerinden nakit faizi (3 aylık Hazine bonosu) düşülür. Temettü gününü kapsayan uzun pozisyonda temettünün %30'u düşülür.
- Her sinyal için **başabaş maliyeti** (brüt ortalama / bacak sayısı) raporlanır.

## 9. Karar ölçütleri (önceden)

- **UYGUN:** IS ve OOS aynı yön; OOS t ≥ 2,5 ve BH %10'dan geçiyor; OOS'ta ≥ 30 işlem; 7. bölümdeki üç anlamlılık ölçüsü; 4. bölümdeki kapanış gerçekçiliği; son dönemde net > 0 (t ≥ 1,0); sağlamlık testleri; bağımsız kod aynı sonucu veriyor; **ekonomik taban:** başabaş maliyeti varsayılan maliyetin ≥ 3 katı, net beklenti ≥ 10 bps/işlem, işlem başına net/σ ≥ 0,10, yıllık beklenen net (işlem sayısı × net) ≥ %3.
- **KOŞULLU:** OOS t 2,0–2,5 ya da bir ölçütte eksik; gerekçesi tek sözcükle etiketlenir: zayıflama / rejim / az olay / uygulama.
- **DÜŞÜK:** IS ve OOS aynı yön ama t < 2 ya da işlem sayısı az; "tema" sınıfı; başarısız taramadan gelenler.
- **ELENDİ:** diğerleri; ekonomik tabanı sağlamayan "anlamlı ama önemsiz" diye elenir. Elenenler nedenleriyle raporlanır.

## 10. Bilinen sınırlar

- Hayatta kalma yanlılığı tam giderilemez (borsadan çıkan hisselerin verisi yok).
- 60 dakikalık veri yalnız son ~730 günü kapsar; kapanış gerçekçiliği testinin (b) şıkkı tek rejime yakın bir dönemdir.
- Yatırımcının aracı kurumu ve tipik emir büyüklüğü bilinmiyor; üç komisyon senaryosu da verilir.
- Geçmiş performans geleceği garanti etmez; kenarlar yayımlandıkça ve kalabalıklaştıkça erir.

## Sapmalar

(boş)
