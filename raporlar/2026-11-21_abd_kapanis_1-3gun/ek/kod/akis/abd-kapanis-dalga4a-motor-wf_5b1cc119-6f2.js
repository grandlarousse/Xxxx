export const meta = {
  name: 'abd-kapanis-dalga4a-motor',
  description: 'Backtest motoru (fable) → bağımsız kod denetimi (fable); paralelde ek veri (opus): 60 dakikalık veri, kripto 16:00 fiyatı, kapanış saati tablosu, FOMC/temettü',
  phases: [
    { title: 'Motor', detail: 'YONTEM.md v2 kurallarını uygulayan ortak backtest motoru ve testleri', model: 'fable' },
    { title: 'Kod denetimi', detail: 'ileriye bakma ve istatistik hatası avı; bağımsız testler', model: 'fable' },
    { title: 'Ek veri', detail: 'saatlik veri, kripto 16:00 ET, kapanış saati tablosu, takvim verileri', model: 'opus' },
  ],
}

const SP = '/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad'
const RAPOR = '/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun'
const KOD = RAPOR + '/ek/kod'
const VERI = RAPOR + '/ek/veri'

const cp = (n) => `Kontrol noktası ${n} araç çağrısı; say. ${n}'de dur ve kendine sor: iş bitti mi, sonuca etki eden bir eksik var mı? Yoksa bitir. Varsa ve son 5 çağrın ilerleme sağladıysa devam et; her 10 çağrıda yeniden sor. Üst sınır ${2 * n}.`

const ORTAM = `ORTAM
- python3, pandas 3.0, numpy, scipy (varsa; yoksa numpy ile yaz, paket kurma), requests, bs4, lxml. Makine 4 çekirdek, 15 GB bellek; aynı anda başka ajanlar da çalışıyor, hesapları vektörel yaz.
- Panel yükleme: import sys; sys.path.insert(0, "${KOD}"); from yukle import panel, bilanco, dix_gex, kalite; P = panel()  → anahtarlar: open high low close adjclose adjopen volume evren. Satırlar 5.507 NYSE işlem günü (2005-01-03 → 2026-11-20), 470 sütun.
- Veri tuzakları için önce şunu oku: ${RAPOR}/ek/ajanlar/d2_D.md (Notlar ve Kalite özeti bölümleri).
- Panel ${SP}/panel/ altında (depoya girmez). Betikler ${KOD}/ altına, küçük sonuç tabloları ${VERI}/ altına yazılır. İndirilen dosyaları okuyan Python'u -I ile çalıştır. git commit/push yapma.
- Kendi alt ajanını başlatma. Görev dışına çıkma.`

const K0 = `${cp(40)}

GÖREV K0 — Ortak backtest motoru (bütün sinyal aileleri bunu kullanacak)
Bağlayıcı belge: ${RAPOR}/ek/YONTEM.md (sürüm 2). Önce onu baştan sona oku; oradaki her kural motorun davranışıdır. Bir kuralı uygulayamıyorsan ya da belirsiz buluyorsan en muhafazakâr yorumu seç ve MOTOR.md'de "yorumlar" başlığına yaz.
Bu motorun tek bir hatası (özellikle ileriye bakma) bütün araştırmayı geçersiz kılar. Senden sonra bağımsız bir denetçi kodu kırmaya çalışacak ve dokuz ajan bu motorla sinyal sınayacak.

Yazılacak dosyalar (${KOD}/):
1. motor.py — işlevler (adlar öneridir; tutarlı ve belgeli olsun):
   - Sabitler: dönemler (STRES 2005–2009, IS 2010–2019, OOS 2020–2023, SON 2024-01-01–2026-11-20; "yeni yapı" hattı için IS2 2020–2023, OOS2 2024–2026).
   - Güvenli girdi: bir kodun sinyalde kullanılacak serisi; evren.csv'deki kapanis_sinifi SONRA ve VIX1615 olanlar 1 gün gecikmeli döner; aynı gün ^VIX ancak açıkça "sizintili=True" denirse.
   - Getiriler: kapanıştan kapanışa, gece (kapanış→açılış), gün içi (açılış→kapanış); adjclose/adjopen ile.
   - İleri getiri: giriş K (t kapanışı), A (t+1 açılışı), G (t+1 kapanışı); çıkış t+h kapanışı (h=1,2,3) ya da t+1 açılışı (gece tutma). Sinyal günü t'ye hizalı.
   - β: 250 ve 60 günlük, yalnız t−1'e kadar veriyle. Korunmalı ileri getiri: r_Y − β·r_M (aynı giriş/çıkış), M = SPY ya da verilen kod.
   - Rejim tablosu: VIX(t−1) kovası (<20, 20–30, >30) × SPY(t−1) 200 günlük ortalamanın üstünde/altında; VIX > 30 bölüm kimlikleri (aralarında 20 günden az boşluk olan günler tek bölüm), 2005–2026.
   - Koşulsuz taban ve anormal getiri: aynı varlığın aynı dönem ve aynı VIX kovasındaki koşulsuz h günlük ortalaması.
   - Maliyet: YONTEM 8. bölüm aynen (hacim kademesi evren.csv maliyet_bps; 0,5 sent/fiyat tabanı; üç komisyon senaryosu; VIX(t−1) > 30'da ×2; açığa satış ödünç ücreti; uzun pozisyondan nakit faizi (^IRX, 1 gün gecikmeli, yıllık yüzde/252); temettü günü kesintisi için temettü tablosu varsa kullan, yoksa atla ve not düş). Başabaş maliyeti.
   - İşlem listesi: {-1,0,+1} sinyal serisinden (ya da çok hedefli sinyal tablosundan) örtüşmeyen işlemler; her işlem için giriş/çıkış tarihi, brüt, net, anormal, oynaklığa ölçeklenmiş getiri (hedefin t−1'e kadar 20 günlük σ'sı), rejim, bölüm.
   - Günlük takvim-zamanı kâr/zarar serisi: aynı gün açık pozisyonlar eşit ağırlıklı, en çok 5 eşzamanlı pozisyon (fazlası sinyal gücüne göre).
   - Anlamlılık: durağan blok bootstrap p-değeri (ortalama blok 10 gün, 5.000 tekrar, sabit tohum), ölçeklenmiş getirinin t'si, Wilcoxon işaretli sıra, tarihe göre kümelenmiş standart hata (havuzlanmış olaylar için).
   - Sağlamlık: en iyi %5 işlem (en az 3) çıkarılınca; en iyi takvim ayı çıkarılınca; maliyet ×2; pozitif takvim yılı oranı; OOS'tan 2020, 2022 ve Şubat–Nisan 2020 çıkarılınca.
   - degerlendir(...): bir kural için standart sonuç satırlarını (dönem × rejim × h × giriş × korunma × komisyon senaryosu) üreten tek çağrı; bootstrap isteğe bağlı bayrakla. Bootstrapsız tek kural değerlendirmesi birkaç saniyeyi geçmesin.
   - Standart sonuç şeması (bütün aileler aynı sütunlarla CSV yazacak): kural_id, aile, ad, girdi, hedef, yon, h, giris, cikis, korunma, komisyon, donem, rejim, n_islem, yillik_islem, brut_bps, net_bps, anormal_bps, isabet, medyan_bps, sigma_bps, net_sigma, t_olcekli, t_kume, p_bootstrap, p_wilcoxon, basabas_bps, en_kotu_bps, mdd_pct, yillik_net_pct, en_iyi5suz_bps, en_iyi_aysiz_bps, maliyet2x_net_bps, pozitif_yil_orani, uzun_bps, kisa_bps, uzun_n, kisa_n, bolum_sayisi, bolum_pozitif_orani, notlar.
   - Çoklu test: Benjamini–Hochberg.
   - Tarama yardımcıları: çok sayıda (X,Y) için YONTEM 7. bölümdeki regresyon istatistiğini (Y'nin korunmalı ileri getirisi ~ X'in artık getirisi + r_Y,t + r_SPY,t) vektörel hesaplayan işlev; IS verisiyle kümeleme (≤ 60 sepet) yardımcı işlevi; plasebo için blok permütasyon (20 günlük bloklar, aynı yıl ve aynı VIX kovası içinde, bütün Y'lere aynı permütasyon) ve dairesel kaydırma (+40…+250 gün).
   - Dönem başı evreni: 01.01.2010, 01.01.2020, 01.01.2024 öncesindeki 250 günün dolar hacmine göre ilk 150 hisse → ${VERI}/evren_donem_basi.csv. Hedef süzgeci: 60 günlük dolar hacmi 20 milyon $ altındaki günler hedef olamaz.
   - Genişleyen pencereli yüzdelik eşik işlevi (yalnız t−1'e kadar veri).
2. test_motor.py — tek komutla çalışan testler (pytest gerekmesin). En az:
   - Sentetik veriyle ekilmiş lead-lag (Y_{t+1} = 0,3·X_t + gürültü) Giriş K, h=1'de bulunuyor; Giriş G'de kayboluyor.
   - İleriye bakmama: T0'dan sonraki veriyi rastgele boz; T0−5'ten önceki bütün sinyal, β, eşik ve işlem sonuçları bit düzeyinde aynı kalmalı. Bunu motorun her girdi yolu için yap (güvenli girdi, β, rejim, genişleyen yüzdelik, ölçekleme σ'sı, maliyet).
   - SONRA/VIX1615 gecikmesi; ileri getiri hizası (elle hesaplanmış 6 satırlık örnek); maliyet aritmetiği; en çok 5 pozisyon kuralı; bootstrap p-değerinin sıfır hipotezi altında yaklaşık tekdüze, ekilmiş etkide küçük çıkması; BH; blok permütasyonun yıl ve VIX kovası sınırlarını koruması.
3. MOTOR.md — en çok 500 kelime: işlevler, bir kuralın 15 satırda nasıl sınanacağı, yorumlar, bilinen sınırlar.
4. ornek_kural.py — uçtan uca çalışan örnek: "SPY günlük getirisi ≤ −%2 ise kapanışta SPY al, 1/2/3 gün tut" kuralını degerlendir ile sına, standart şemayla ${VERI}/ornek_sonuc.csv yaz.

Testleri çalıştır; geçmeyen test varken bitirme.

${ORTAM}

DÖNÜŞ BİÇİMİ (StructuredOutput alanları)
- arac: "araç: <kullandığın>/40".
- ozet: en çok 300 kelime: ne yazıldı, test sonucu (kaç test, hepsi geçti mi), örnek kuralın sonucu (SPY −%2 kuralı: IS/OOS/SON net bps ve işlem sayısı, Giriş K ve A).
- dosyalar: tam yollar.
- yorumlar: YONTEM.md'de belirsiz bulup yorumladığın noktalar.
- sinirlar: motorun yapmadığı ya da yaklaşık yaptığı şeyler.
Hatırlatma: kontrol noktası 40 araç çağrısı, üst sınır 80.`

const DENETIM = (k0) => `${cp(30)}

GÖREV KD — Backtest motorunun bağımsız kod denetimi
Dosyalar: ${KOD}/motor.py, ${KOD}/test_motor.py, ${KOD}/MOTOR.md, ${KOD}/yukle.py. Bağlayıcı belge: ${RAPOR}/ek/YONTEM.md (sürüm 2).
Motoru yazan ajanın kendi raporu (güvenme, doğrula): ${JSON.stringify(k0 || {}).slice(0, 3000)}

Tek soru: Bu motor YONTEM.md'yi doğru uyguluyor mu; ileriye bakma, hizalama, maliyet ya da istatistik hatası var mı? Varsayılan tutumun şüphe: hata olduğunu varsay ve bul.
Yapılacaklar:
1. Kodu satır satır oku. Özellikle: shift yönleri; kayan pencerelerin t günü verisini içerip içermediği; SONRA/VIX1615 gecikmesi; Giriş A'da açılış fiyatının doğru günü; çıkış gününün işlem günü takvimine göre sayılması; NaN'ların sessizce sıfıra dönmesi; örtüşmeyen işlem mantığı; korunma bacağının aynı giriş/çıkışla hesaplanması; anormal getirinin taban hesabı; maliyetin iki bacakta ve iki yönde düşülmesi; bootstrap'in ortalamayı doğru sıfırlaması; blok permütasyonun sinyal–getiri bağını gerçekten koparması; BH uygulaması; dönem sınırlarında (IS sonu/OOS başı) işlem sızıntısı.
2. Motorun testlerinden bağımsız, kendi karşı testlerini yaz (${KOD}/test_denetim.py) ve çalıştır. En az: (a) gerçek panelde rastgele 5 kural için motorun işlem listesini elle (motoru kullanmadan, düz pandas ile) yeniden hesapla ve işlem işlem karşılaştır; (b) gelecekten sızıntı testi: sinyali kasıtlı olarak 1 gün ileri kaydır (hileli sinyal) ve motorun bunu devasa bir kenar olarak gösterdiğini, dürüst sinyalde ise göstermediğini doğrula; (c) saf gürültü sinyalleriyle 300 kural üret: p-değerlerinin dağılımı tekdüze mi, %5 düzeyinde yanlış pozitif oranı %5 civarı mı; (d) bilinen bir olguyu yeniden üret: SPY'nin gece (kapanış→açılış) ve gün içi getirilerinin 2005–2026 toplamı, panelden doğrudan hesapla ve motorla karşılaştır.
3. Açık ve küçük hataları yerinde düzelt (motor.py), testleri yeniden çalıştır. Tasarım düzeyindeki sorunları düzeltme; raporla.

${ORTAM}

DÖNÜŞ BİÇİMİ (StructuredOutput alanları)
- arac: "araç: <kullandığın>/30".
- karar: "kullanılabilir" / "düzeltmelerle kullanılabilir" / "kullanılamaz" ve tek paragraf gerekçe.
- bulgular: en çok 15 satır; onem (kritik/önemli/küçük) | yer (işlev ya da satır) | sorun | durum (düzeltildi / açık) | etkisi.
- testler: yazdığın karşı testlerin sonucu (sayılarla).
- acik_kalanlar: ana ajanın karar vermesi gerekenler.
Hatırlatma: kontrol noktası 30 araç çağrısı, üst sınır 60.`

const D2 = `${cp(40)}

GÖREV D2 — Ek veri (yöntem denetçisinin istediği parçalar)
Tek iş: Aşağıdaki veri parçalarını indir, kur ve yükleme işlevlerini ${KOD}/yukle.py dosyasına EKLE (mevcut işlevleri bozma; başka bir ajan aynı anda motor.py yazıyor, o dosyaya dokunma). Yorum ya da sinyal testi yapma.
Öncelik sırasıyla:
1. KAPANIŞ SAATİ TABLOSU → ${VERI}/kapanis_saatleri.csv: evrendeki her kod için Yahoo chart API meta bilgisinden (exchangeTimezoneName, currentTradingPeriod.regular.end) günlük çubuğun ET ile kapanış saati. Kural: 15:45 ET'den sonra kapanan her seri SONRA sınıfıdır. evren.csv içindeki kapanis_sinifi sütununu buna göre güncelle: ^VIX ailesi (VIX1615) SONRA olur; ^TNX/^FVX/^TYX/^IRX tabloya göre ONCE ya da SONRA. Dış endekslerde panel tarihinin borsanın yerel günü olduğunu 3 örnekle doğrula (ör. ^N225, ^HSI, ^GDAXI: belirli bir günün kapanışı ham veriyle aynı mı).
2. 60 DAKİKALIK VERİ: Yahoo chart API interval=60m, range=730d (çubuklar 09:30, 10:30, …, 15:30 ET başlar). evren.csv'de kapanis_sinifi ABD16 ve adv60_usd ≥ 50 milyon $ olan ETF ve hisseler için. Çıktı (${SP}/panel/): saatlik_1530.pkl (her işlem günü için 15:30 çubuğunun açılış fiyatı), saatlik_kapanis.pkl (aynı kaynaktan günün son çubuğunun kapanışı), saatlik_onceki_kapanis.pkl gerekmez (kaydırmayla bulunur). Yarım günleri (13:00 kapanış) ayrı işaretle. yukle.py'ye saatlik() işlevi ekle. Amaç: "15:30'da hesaplanan sinyal" ile "16:00 kapanış sinyali"ni karşılaştırmak. Yaz/kış saatini doğru ele al. Kaç kod, kaç gün geldiğini raporla.
3. KRİPTO 16:00 ET FİYATI: BTC-USD ve ETH-USD (varsa SOL-USD) için saatlik mumlardan, her NYSE işlem gününde 16:00 ET'deki fiyat (15:00–16:00 ET mumunun kapanışı), 2015'ten bugüne (ETH 2016'dan). Kaynak sırası: Coinbase Exchange (https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=3600&start=...&end=..., istek başına 300 mum), olmazsa Bitstamp (https://www.bitstamp.net/api/v2/ohlc/btcusd/?step=3600&limit=1000&start=...), olmazsa Kraken/Binance. Çıktı: ${SP}/panel/kripto_1600.pkl ve yukle.py'ye kripto_1600() işlevi. Yahoo BTC-USD günlük kapanışıyla (00:00 UTC) farkını 5 günde göster.
4. TEMETTÜ TABLOSU: ham Yahoo JSON'larındaki (${SP}/ham/) events.dividends kayıtlarından tarih × kod temettü tutarı → ${SP}/panel/temettu.pkl ve yukle.py'ye temettu() işlevi.
5. FOMC TARİHLERİ → ${VERI}/fomc_tarihleri.csv: 2005–2026 arası planlı FOMC toplantılarının karar günü (iki günlük toplantıların ikinci günü), basın toplantısı var mı, olağanüstü toplantılar ayrı işaretli. Kaynak: federalreserve.gov (fomccalendars.htm ve fomc_historical_year.htm sayfaları).
6. MAKRO YAYIN TARİHLERİ (elinden geldiği kadar) → ${VERI}/makro_tarihleri.csv: TÜFE (CPI) ve İstihdam Raporu yayın günleri 2005–2026. Kaynak adayları: alfred.stlouisfed.org yayın tarihleri (curl --http1.1 dene), bls.gov arşiv takvimleri. 5 denemede olmazsa bırak ve bildir.
7. XIV 2018: Yahoo'da XIV serisi var mı dene. Yoksa XIV'in 5 Şubat 2018 ve 6 Şubat 2018 kapanışlarını (ve yüzde kaybı) kaynaklı olarak bul → ${VERI}/xiv_2018.csv (tarih, kapanış, kaynak URL).
8. İKİNCİ KAYNAK ARACI: ${KOD}/ikinci_kaynak.py — Nasdaq API'sinden (https://api.nasdaq.com/api/quote/<KOD>/historical?assetclass=stocks ya da etf&fromdate=YYYY-MM-DD&todate=YYYY-MM-DD&limit=..., tarayıcı benzeri User-Agent ve Accept: application/json) bir kodun düzeltilmemiş günlük kapanışlarını çeken işlev. SPY ve NVDA'nın son 20 gününde Yahoo close ile farkı (bps) raporla.
Sayfa okumak için: python3 -I ${SP}/oku.py "URL" "regex" --ctx 300 --max 4000 . Arama gerekirse WebSearch (listende yoksa ToolSearch ile "select:WebSearch").
Durma kuralı: bir veri kaynağına 5 denemede erişemiyorsan o parçayı bırak, bildir, sıradakine geç.

${ORTAM}

DÖNÜŞ BİÇİMİ (StructuredOutput alanları)
- arac: "araç: <kullandığın>/40".
- ozet: en çok 300 kelime: hangi parçalar üretildi, kapsam (kod ve gün sayıları).
- dosyalar: tam yollar.
- yukleme_ornegi: yeni işlevlerin 5 satırlık kullanım örneği (denediğin hâliyle).
- basarisiz: üretilemeyen parçalar ve nedeni.
- notlar: sonraki ajanların bilmesi gereken tuzaklar (özellikle kapanış saati sınıfı değişiklikleri ve saatlik verinin düzeltme/bölünme durumu).
Hatırlatma: kontrol noktası 40 araç çağrısı, üst sınır 80.`

const S_K0 = { type: 'object', properties: { arac: { type: 'string' }, ozet: { type: 'string' }, dosyalar: { type: 'array', items: { type: 'string' } }, yorumlar: { type: 'string' }, sinirlar: { type: 'string' } }, required: ['arac', 'ozet', 'dosyalar', 'yorumlar', 'sinirlar'] }
const S_KD = {
  type: 'object',
  properties: {
    arac: { type: 'string' }, karar: { type: 'string' },
    bulgular: { type: 'array', maxItems: 15, items: { type: 'object', properties: { onem: { type: 'string', enum: ['kritik', 'önemli', 'küçük'] }, yer: { type: 'string' }, sorun: { type: 'string' }, durum: { type: 'string' }, etkisi: { type: 'string' } }, required: ['onem', 'yer', 'sorun', 'durum', 'etkisi'] } },
    testler: { type: 'string' }, acik_kalanlar: { type: 'string' },
  },
  required: ['arac', 'karar', 'bulgular', 'testler', 'acik_kalanlar'],
}
const S_D2 = { type: 'object', properties: { arac: { type: 'string' }, ozet: { type: 'string' }, dosyalar: { type: 'array', items: { type: 'string' } }, yukleme_ornegi: { type: 'string' }, basarisiz: { type: 'string' }, notlar: { type: 'string' } }, required: ['arac', 'ozet', 'dosyalar', 'yukleme_ornegi', 'basarisiz', 'notlar'] }

const dene = async (prompt, opts) => {
  let r = await agent(prompt, opts)
  if (!r) { log(opts.label + ' sonuç döndürmedi; 1 yeniden deneme'); r = await agent(prompt, Object.assign({}, opts, { label: opts.label + ' (yeniden)' })) }
  return r
}

const [motorSonuc, d2] = await parallel([
  async () => {
    const k0 = await dene(K0, { label: 'K0 · backtest motoru', phase: 'Motor', schema: S_K0, model: 'fable', effort: 'high' })
    log('K0 bitti · ' + (k0 ? k0.arac : 'sonuç yok'))
    const kd = await dene(DENETIM(k0), { label: 'KD · motor kod denetimi', phase: 'Kod denetimi', schema: S_KD, model: 'fable', effort: 'high' })
    log('KD bitti · ' + (kd ? kd.karar.slice(0, 80) : 'sonuç yok'))
    return { k0, kd }
  },
  async () => {
    const r = await dene(D2, { label: 'D2 · ek veri', phase: 'Ek veri', schema: S_D2, model: 'opus', effort: 'high' })
    log('D2 bitti · ' + (r ? r.arac : 'sonuç yok'))
    return r
  },
])
return { K0: motorSonuc ? motorSonuc.k0 : null, KD: motorSonuc ? motorSonuc.kd : null, D2: d2 }
