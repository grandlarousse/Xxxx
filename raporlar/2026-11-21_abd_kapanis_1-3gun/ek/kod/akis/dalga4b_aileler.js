export const meta = {
  name: 'abd-kapanis-dalga4b-aileler',
  description: 'L+ dalga 4: sinyal ailelerinin backtesti (opus; sistematik tarama fable). Ortak motor, önce IS, sonra OOS, sonra kilitli son dönem. args: {gorevler:[...], ek_not:"..."}',
  phases: [
    { title: 'Backtest', detail: 'aile başına bir kod ajanı; standart şemayla sonuç tablosu', model: 'opus' },
  ],
}

const SP = '/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad'
const RAPOR = '/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun'
const KOD = RAPOR + '/ek/kod'
const VERI = RAPOR + '/ek/veri'
const AJ = RAPOR + '/ek/ajanlar'
const A = (args && !Array.isArray(args)) ? args : {}
const EK_NOT = A.ek_not ? ('\nANA AJANDAN EK NOT (motor denetimi ve veri hakkında; bağlayıcı):\n' + A.ek_not + '\n') : ''

const cp = (n) => `Kontrol noktası ${n} araç çağrısı; say. ${n}'de dur ve kendine sor: iş bitti mi, sonuca etki eden bir eksik var mı? Yoksa bitir. Varsa ve son 5 çağrın ilerleme sağladıysa devam et; her 10 çağrıda yeniden sor. Üst sınır ${2 * n}.`

const PROFIL = `YATIRIMCI PROFİLİ: Türkiye'de yerleşik bireysel yatırımcı; gün içi işlem yapmıyor. ABD kapanışında (16:00 ET) bilinen sinyalle pozisyon açıyor, 1–3 işlem günü taşıyor. Lead-lag ilişkilerine bakıyor. Riski kabul ediyor, ciddi kazanç arıyor (kaldıraçlı/ters ETF, oynak hisse dahil). Sonuçlar gerçek parayla kullanılacak: yanlış pozitif, kaçırılmış bir sinyalden çok daha pahalıdır.
BUGÜN: 20 Kasım 2026 kapanışı itibarıyla S&P 500 6.910 (7 gün üst üste düşüş, 6 Ekim zirvesinden −%10'dan fazla), Nasdaq zirveden −%18, NVDA −%47,5, VIX 35,9. Fed faiz artırıyor (sonraki toplantı 8–9 Aralık).`

const BELGELER = (aileMetni, rDosyalari) => `BAĞLAYICI BELGELER (önce oku)
1. ${RAPOR}/ek/YONTEM.md — yöntem (sürüm 2). Eşikleri, dönemleri ve karar ölçütlerini değiştirme.
2. ${KOD}/MOTOR.md — ortak backtest motorunun kullanımı; ${KOD}/ornek_kural.py çalışan örnek. Getiri, maliyet, istatistik ve sınıflama hesaplarını motorla yap; bunları yeniden yazma. Sinyal serisini üretmek senin işin.
3. ${VERI}/hipotezler.csv — önceden yazılı kurallar. Senin payın: ${aileMetni}. Kural ayrıntıları ve kaynak sayıları: ${rDosyalari.map((d) => AJ + '/' + d).join(' ; ')} içindeki "Sınanacak kurallar" tabloları.
4. Veri tuzakları: ${AJ}/d2_D.md (Notlar, Kalite özeti) ve varsa ${AJ}/d4_D2.md. Kapanış saati sınıfı SONRA olan seriler (kripto, döviz, vadeli, ^VIX ailesi) sinyalde yalnız 1 gün gecikmeli kullanılır; motorun "güvenli girdi" işlevini kullan.`

const SIRA = (X) => `ÇALIŞMA SIRASI (sırayı bozma)
1. Kuralları tek tek sinyal serisine çevir. Kuralda açık bırakılmış parametre varsa YONTEM'deki ızgarayı kullan (eşik |z| > 1 ve > 2; pencere 60 ve 250 gün; h = 1, 2, 3); başka parametre arama. Verisi panelde olmayan kuralı "veri yok" diye işaretle ve geç.
2. ÖNCE YALNIZ IS (2010–2019): bütün kural × varyantları değerlendir. Aday = IS'te net > 0 ve ölçeklenmiş t ≥ 2. Aday listesini OOS'a bakmadan ÖNCE dosyaya yaz: ${VERI}/aday_${X}.csv.
3. SONRA OOS (2020–2023): yalnız adaylar. OOS'tan geçenler (aynı yön, t ≥ 2) için: kilitli son dönem (2024–2026-11-20), Giriş A ve Giriş G, "çıkış t+1 açılış", korunmasız ve korunmalı, üç komisyon senaryosu, rejim kırılımı ve VIX > 30 bölümleri, bootstrap, sağlamlık testleri.
4. 2020 sonrası doğan araçlara dayanan kurallar "yeni yapı" hattına girer (IS 2020–2023, OOS 2024–2026, eşik OOS t ≥ 3; en çok KOŞULLU).
5. Kaynağı olan kurallarda yalnız yayın sonrası dönem doğrulama sayılır; yayın yılını sonuç satırına yaz.
6. Her kural için YONTEM 9. bölüme göre sınıf öner (UYGUN / KOŞULLU / DÜŞÜK / ELENDİ) ve tek cümle gerekçe yaz. Aileler arası çoklu test düzeltmesini ana ajan yapacak; bu yüzden bütün adayların OOS p-değerlerini döndür.
7. Bugünkü durum: OOS'tan geçen kurallarda 20 Kasım 2026 kapanışında sinyal açık mı; 23 Kasım kapanışında hangi koşulda tetiklenir (seviye ya da eşik olarak)?
Bütün sonuç satırlarını (elenenler dahil) motorun standart şemasıyla ${VERI}/sonuc_${X}.csv dosyasına yaz. Betiğin ${KOD}/aile_${X}.py olsun; tek komutla yeniden çalışsın. Ham veriyi depoya yazma. git commit/push yapma.
DÜRÜSTLÜK: Sınadığın her varyantı say ve raporla. Sonucu güzelleştirmek için kural, dönem ya da eşik değiştirme. "Hiçbiri geçmedi" de bir bulgudur. Bir sonuç inanılmayacak kadar iyiyse (işlem başına > 100 bps, t > 6, isabet > %70) önce ileriye bakma ya da veri hatası ara; bulduğunu bildir. Motorda hata bulursan motor.py'yi DEĞİŞTİRME (başka ajanlar aynı anda kullanıyor); sorunu ve geçici çözümünü notlara yaz.`

const ORTAM = `ORTAM: python3, pandas 3.0, numpy, scipy (varsa). Makine 4 çekirdek, 15 GB; aynı anda başka backtest ajanları çalışıyor: hesapları vektörel yaz, bootstrap'i yalnız adaylarda çalıştır, tek bir komutu 8 dakikadan uzun sürecek biçimde kurma. Panel: import sys; sys.path.insert(0, "${KOD}"); from yukle import panel. Panel dosyaları ${SP}/panel/ altında. Kendi alt ajanını başlatma. Görev dışına çıkma.`

const DONUS = (n) => `DÖNÜŞ BİÇİMİ (StructuredOutput alanları)
- arac: "araç: <kullandığın>/${n}" (geçtiysen nedeni).
- ozet: en çok 400 kelime, sade Türkçe: ne sınandı, ne ayakta kaldı, ne elendi, en önemli çekince.
- test_sayisi: sınanan kural × varyant sayısı. aday_sayisi: IS'ten geçen aday sayısı. oos_gecen: OOS'tan geçen sayısı.
- tablo: en çok 25 satır (önce OOS'tan geçenler, sonra en bilgilendirici elenenler). Alanlar: kural_id, ad, hedef, yon, h, giris, korunma, is_net_bps, oos_net_bps, oos_n, oos_t, oos_p, son_net_bps, son_t, girisA_oos_net_bps, basabas_bps, vix30 (bölüm sayısı ve pozitif oranı, kısa metin), sinif, gerekce.
- elenenler: elenen kuralların kısa listesi ve nedenleri (tek paragraf ya da madde madde).
- bugun: 20 Kasım 2026 kapanışındaki sinyal durumu ve 23 Kasım için tetikler.
- dosyalar: yazdığın dosyaların tam yolları.
- sapmalar: YONTEM'den her sapma (yoksa "yok").
- notlar: motor ya da veriyle ilgili sorunlar, şüpheli sonuçlar, ana ajanın bilmesi gerekenler.
Hatırlatma: kontrol noktası ${n} araç çağrısı, üst sınır ${2 * n}.`

const satir = {
  type: 'object',
  properties: {
    kural_id: { type: 'string' }, ad: { type: 'string' }, hedef: { type: 'string' }, yon: { type: 'string' }, h: { type: 'string' }, giris: { type: 'string' }, korunma: { type: 'string' },
    is_net_bps: { type: 'number' }, oos_net_bps: { type: 'number' }, oos_n: { type: 'number' }, oos_t: { type: 'number' }, oos_p: { type: 'number' },
    son_net_bps: { type: 'number' }, son_t: { type: 'number' }, girisA_oos_net_bps: { type: 'number' }, basabas_bps: { type: 'number' },
    vix30: { type: 'string' }, sinif: { type: 'string' }, gerekce: { type: 'string' },
  },
  required: ['kural_id', 'ad', 'hedef', 'h', 'giris', 'sinif', 'gerekce'],
}
const SEMA = {
  type: 'object',
  properties: {
    arac: { type: 'string' }, ozet: { type: 'string' }, test_sayisi: { type: 'number' }, aday_sayisi: { type: 'number' }, oos_gecen: { type: 'number' },
    tablo: { type: 'array', maxItems: 25, items: satir },
    elenenler: { type: 'string' }, bugun: { type: 'string' }, dosyalar: { type: 'array', items: { type: 'string' } }, sapmalar: { type: 'string' }, notlar: { type: 'string' },
  },
  required: ['arac', 'ozet', 'test_sayisi', 'aday_sayisi', 'oos_gecen', 'tablo', 'elenenler', 'bugun', 'dosyalar', 'sapmalar', 'notlar'],
}

const kur = (X, baslik, govde, aileMetni, rDosyalari) => [cp(40), '', `GÖREV ${X} — ${baslik}`, govde, '', PROFIL, EK_NOT, BELGELER(aileMetni, rDosyalari), '', SIRA(X), '', ORTAM, '', DONUS(40)].join('\n')

const KUMELER = `Önceden yazılı tema kümeleri (lider → takipçiler). Bunların dışında küme kurma:
- yarı iletken: NVDA, TSM, AVGO → AMD, MU, MRVL, AMAT, LRCX, KLAC, ASML, ON, MCHP, SMCI, SOXX, SMH
- kripto: IBIT (2024'ten) ya da 16:00 ET Bitcoin fiyatı → MSTR, COIN, MARA, RIOT, CLSK, IREN, HUT, WULF, CIFR, HOOD
- elektrikli araç: TSLA → RIVN, LCID, NIO, XPEV, LI
- nükleer/elektrik: CCJ, CEG, VST → OKLO, SMR, UEC, LEU, NNE, BWXT, URA
- kuantum: IONQ → RGTI, QBTS, QUBT
- uzay: RKLB → ASTS, LUNR, PL
- yapay zekâ yazılımı: PLTR → AI, SOUN, BBAI
- bankalar: JPM → BAC, C, WFC, KRE
- enerji: XOM → OXY, DVN, SLB, HAL, XOP
- Çin: BABA → PDD, JD, BIDU, KWEB, FXI
- havayolu: DAL → UAL, AAL, LUV, JETS
- konut: DHI → LEN, PHM, TOL, XHB, ITB
- kilo ilacı: LLY → NVO, VKTX, HIMS
2015 sonrası halka açılan ya da bugünkü tema nedeniyle seçilen hisseler "tema" sınıfıdır (en çok DÜŞÜK); 2020 sonrası araçlar "yeni yapı" hattına girer.`

const G = {
  K1: kur('K1', 'Aile A: lider → takipçi',
    `Tek soru: Bir liderin (hisse, sepet ya da sektör) t günü hareketi, takipçilerin sonraki 1–3 günlük korunmalı getirisini maliyet sonrası öngörüyor mu?
Kapsam: hipotezler.csv'de aile = A olan kurallar (R2-05, R2-07, R2-12, R4-01…R4-08, R6-05, R6-07, R6-08) ve aşağıdaki tema kümeleri. Her kümede iki biçim: (i) liderin artık getirisi (lider − β·SPY) z > 1 ve > 2 iken takipçi sepeti aynı yönde; (ii) takipçinin lidere göre aynı gün "eksik kalması" (takipçi − β·lider) → ertesi günlerde yakalama. İki yönü de sına (devam ve dönüş).
${KUMELER}
Büyük → küçük (SPY → IWM) kuralını iki yönde ve 2008 öncesi/sonrası ayrı raporla. Bilançoya dayalı kurallar (R6-05, R6-07, R6-08) için yukle.bilanco() ve YONTEM 2. bölümdeki tepki günü tanımını kullan.`,
    'aile = A satırları', ['d3_R4.md', 'd3_R2.md', 'd3_R6.md']),

  K2: kur('K2', 'Aile B: göreli gecikme, çiftler, artık ve kesitsel dönüş',
    `Tek soru: Bir hissenin ya da ETF'in benzerine/sektörüne göre 1–5 günlük sapması sonraki 1–3 günde maliyet sonrası geri dönüyor mu (ya da sürüyor mu); hangi tanım ve hangi rejimde?
Kapsam: hipotezler.csv'de aile = B olan kurallar (R2-03, R2-06, R4-10, R4-11, R5-01…R5-06, R5-09…R5-11). Ek (yöntem denetçisinin istediği): kesitsel sıralama sepetleri — (a) 11 SPDR sektör ETF'i ve (b) dönem başı evrenindeki 150 hisse için 1, 3 ve 5 günlük artık getiriye göre en kötü beşte birlik uzun, en iyi beşte birlik kısa; sektör-nötr; h = 1, 2, 3; VIX kovasına göre.
Bilanço günlerini (yukle.bilanco) içeren sapmaları ayrı raporla (R5 bulgusu: bilanço içeren sapma dönmez, sürüklenir). Uzun ve kısa bacakları ayrı raporla; yalnız uzun bacağı çalışan kural en çok KOŞULLU.`,
    'aile = B satırları', ['d3_R5.md', 'd3_R4.md', 'd3_R2.md']),

  K3: kur('K3', 'Aile C: çapraz varlık → endeks ve sektör',
    `Tek soru: Kredi, faiz, dolar, emtia ve kripto hareketleri ilgili sektör ETF'lerinin ve hisselerin sonraki 1–3 günlük getirisini maliyet sonrası öngörüyor mu, yoksa yansıma aynı gün içinde mi bitiyor?
Kapsam: hipotezler.csv'de aile = C olan kurallar (R2-01, R2-02, R2-04, R2-08…R2-11, R2-13, R2-14, R8-09). Ek: yüksek beta/düşük oynaklık farkı (SPHB − SPLV) → SPY; ülke ETF'lerinde (EWJ, FXI, KWEB, EWZ, EWT, EWY, INDA, TUR) ABD seansı hareketinin ertesi açılışta dönüşü (giriş K, çıkış t+1 açılış ve t+1 kapanış).
Sinyal girdisi olarak 16:00'da kapanan ETF vekillerini kullan (USO/BNO, GLD/SLV, CPER, UUP, TLT/IEF, HYG/LQD); vadeli ve döviz serileri yalnız 1 gün gecikmeli. Araştırma ajanının beklentisi "günlük ufukta kanıt yok"; bunu doğrulamak da bir sonuçtur.`,
    'aile = C satırları', ['d3_R2.md', 'd3_R8.md']),

  K4a: kur('K4a', 'Aile D (1): kendi serisinde uç hareket ve kısa vadeli dönüş, rejimle',
    `Tek soru: Endeks ETF'lerinde (SPY, QQQ, IWM, DIA), sektör ETF'lerinde (özellikle SMH/SOXX, XBI, KRE, XLE) ve dönem başı evrenindeki büyük hisselerde, kapanışta bilinen uç hareket sinyalleri sonraki 1–3 günü maliyet sonrası öngörüyor mu; VIX ve trend rejimine göre nasıl değişiyor?
Kapsam: hipotezler.csv'den R8-01…R8-08, R1-03, R1-04, R1-11, R1-14, R7-10. Ek (yöntem denetçisi): kapanışın gün içi aralıktaki yeri IBS = (kapanış − düşük)/(yüksek − düşük) < 0,2 ve > 0,8; RSI(2) < 10 ve > 90; üst üste 3, 5, 7 düşüş günü; günlük getiri ≤ −2σ ve ≤ −3σ (σ: t−1'e kadar 20 günlük).
Her sinyal için kaldıraçlı ETF uygulama satırı da üret (aynı sinyal, gerçek ETF fiyatıyla): SPY → UPRO/SPXU, SSO/SDS; QQQ → TQQQ/SQQQ, QLD/QID; SOXX → SOXL/SOXS; IWM → TNA/TZA.
Rejim raporu zorunlu: VIX(t−1) kovası × 200 günlük ortalama; VIX > 30 bölümleri tek tek (2008–09 dahil): bölüm başına işlem sayısı, toplam ve en kötü işlem. "Düşeni al" kurallarının felaket dönemlerindeki (Eylül–Kasım 2008, Şubat–Mart 2020, 2022) ardışık kayıplarını ayrıca yaz. Bugünkü durum (7 gün üst üste düşüş, VIX 35,9, endeks 200 günlük ortalamaya göre nerede) için: tarihte aynı koşulların sağlandığı günlerin listesi ve sonraki 1, 2, 3, 5 günlük getirileri (ortalama, medyan, isabet, en kötü).`,
    'R8-01…R8-08, R1-03, R1-04, R1-11, R1-14, R7-10', ['d3_R8.md', 'd3_R1.md', 'd3_R7.md']),

  K4b: kur('K4b', 'Aile D (2): akış vekilleri, kapitülasyon/genişlik ve kaldıraçlı ETF yolu',
    `Tek soru: Gün sonu mekanik akışların (kaldıraçlı ETF dengelemesi, gama korunması) günlük veriden kurulan vekilleri ve kapitülasyon/genişlik göstergeleri sonraki 1–3 günü maliyet sonrası öngörüyor mu?
Kapsam: hipotezler.csv'den R3-01…R3-04, R3-11, R8-10, R8-11. Ek (yöntem denetçisi): (a) VIX − 20 günlük gerçekleşen oynaklık (VIX 1 gün gecikmeli ya da VIXY ile); VIX'in tek günde sert sıçraması (VIXY günlük getirisi ≥ +%10 ve ≥ +%20); (b) evrenden hesaplanan genişlik: dönem başı evrenindeki hisselerden 20 günlük ortalamasının üstünde olanların payı < %10 ve < %20; hisselerin %90'ının düştüğü gün; (c) büyük hareket günü vekili: |günlük getiri| ≥ %2 ve kapanış konumu (IBS) uçta → ertesi gün dönüş/devam; aynı şey tek hisse kaldıraçlı ürünlerin dayanaklarında (NVDA, TSLA, MSTR, COIN; "yeni yapı" hattı).
R8-10 (kaldıraçlı ETF yol testi): TQQQ, SOXL, UPRO ve terslerinde 1, 2, 3 günlük tutmada gerçekleşen getirinin "kaldıraç × endeks getirisi"nden sapması, VIX kovasına göre (oynaklık aşınması 1–3 günde ne kadar?).
R3-11 (kapanış girişi kayma testi): kapanış fiyatından giriş ile ertesi açılıştan giriş arasındaki fark, dönüş sinyallerinde ne kadar kenar götürüyor?`,
    'R3-01…R3-04, R3-11, R8-10, R8-11', ['d3_R3.md', 'd3_R8.md']),

  K5: kur('K5', 'Aile E: takvim ve olay etkileri',
    `Tek soru: Takvim ve duyuru günlerine bağlı kurallardan hangileri 2010 sonrasında, özellikle yayımlandıktan sonra, maliyet sonrası 1–3 günlük (ya da tanımlı pencerelik) kazanç bırakıyor?
Kapsam: hipotezler.csv'de aile = E olan kurallar (R7-01, R7-02, R7-04…R7-09, R7-11, R6-09, R8-12) ve R7-03 (60/40 ay sonu yeniden dengeleme sinyali). Ek (yöntem denetçisi): makro duyuru primi (TÜFE, istihdam raporu ve FOMC gününden önceki kapanışta giriş, duyuru günü kapanışında çıkış; FOMC sonrası 1–3 gün); tahvilde ay sonu/ay başı (TLT); yılın son 5 ve ilk 2 günü; Şükran Günü haftası.
Veri: FOMC tarihleri ${VERI}/fomc_tarihleri.csv, makro tarihleri ${VERI}/makro_tarihleri.csv (varsa; yoksa o kuralı "veri yok" işaretle). Tatiller ve yarım günler panel takviminden çıkarılır. Opsiyon vadesi = ayın üçüncü cuması. Endeks dengeleme tarihleri için veri yoksa kuralı "veri yok" işaretle.
Hedefler: SPY, QQQ, IWM, TLT; ilgili yerlerde kaldıraçlı karşılıkları. Pencere tanımları R7 tablosundaki gibi (ör. ay dönümü: sondan ikinci işlem günü kapanışı → yeni ayın 3. işlem günü kapanışı). Takvim kurallarında olay sayısı azdır: yılda işlem sayısını ve bölüm bağımlılığını açık yaz.
Bugün için: 23 Kasım 2026 – 15 Ocak 2027 arasında OOS'tan geçen kuralların tarihli takvimi (giriş ve çıkış günleri).`,
    'aile = E satırları ve R7-03', ['d3_R7.md', 'd3_R6.md', 'd3_R8.md']),

  K6: kur('K6', 'Aile F ve H: volatilite ürünleri ve konumlanma verisi',
    `Tek soru: VIX vade yapısı ve varyans risk primi sinyalleri volatilite ürünlerinde (VIXY, VXX, UVXY, SVXY) ve SPY/QQQ'da; DIX/GEX konumlanma verisi SPY/QQQ'da sonraki 1–3 (ve kaynakta tanımlı 5) günde maliyet sonrası kazanç bırakıyor mu?
Kapsam: hipotezler.csv'de aile = F olan kurallar (R1-01, R1-02, R1-05…R1-10, R1-12, R1-13, R4-09, R5-12, R8-03) ve DIX/GEX kuralları (R3-05, R3-06, R3-07). R3-08, R3-09, R3-10 için veri panelde yok: "veri yok" işaretle.
Zorunlu kurallar (YONTEM 6. bölüm F): ^VIX ailesi sinyalde 1 gün gecikmeli (ya da VIXY/VXX fiyatından türetilmiş vekil); aynı gün ^VIX yalnız "sızıntılı üst sınır" satırı. Birincil araç VIXY. SVXY ve UVXY 28.02.2018 öncesi ve sonrası ayrı araçtır. Kısa volatilite sonuçlarına XIV'in 5–6 Şubat 2018 kaybı elle eklenir (${VERI}/xiv_2018.csv varsa oradan; yoksa SVXY'nin aynı günkü kaybını kullan ve not düş): "olay dahil / hariç" iki satır. VIX vadeli verisi yok: Simon-Campasano roll kuralı VIX3M/VIX oranıyla vekil olarak sınanır ve "vekil" diye işaretlenir.
DIX/GEX kapanıştan sonra yayımlanır: giriş ertesi açılış (Giriş A). Veri: yukle.dix_gex().
Kısa volatilite stratejilerinde sol kuyruğu açık yaz: en kötü 5 işlem, en büyük düşüş, Şubat 2018 ve Mart 2020. Bugünkü durum (VIX 35,9; vade yapısı ters mi?) için kuralların ne dediğini yaz.`,
    'aile = F satırları ve R3-05, R3-06, R3-07', ['d3_R1.md', 'd3_R3.md', 'd3_R8.md']),

  K7: kur('K7', 'Aile G: bilanço etrafında 1–3 günlük kurallar',
    `Tek soru: Bilanço açıklamasının ilk tepki günü kapanışında bilinen bilgiyle hissenin kendisinde ve emsallerinde, ve bilanço öncesi günlerde, maliyet sonrası 1–3 günlük kazanç bırakan kural var mı?
Kapsam: hipotezler.csv'den R6-01…R6-04, R6-06, R5-07, R5-08. Ek (yöntem denetçisi): bilanço öncesi prim (açıklamadan 1–3 gün önce al, açıklamadan önce çık).
Veri: yukle.bilanco() (SEC 8-K 2.02 kabul damgaları; 212 hisse). Tepki günü tanımı YONTEM 2. bölümdeki gibi: kabul damgasının gösterdiği gün ile komşu iki günden, hacmi 20 günlük ortalamaya oranı en yüksek olan gün; iki yöntem uyuşmuyorsa olayı at. 50 olaylık rastgele örneklemle uyuşmazlık oranını raporla; %5'i aşarsa aile KOŞULLU'nun üstüne çıkamaz. Beklenti (analist tahmini) verisi yok: sürpriz, tepki günü anormal getirisi ve hacmiyle tanımlanır.
Havuzlanmış olaylarda standart hatayı tarihe göre kümele; dönem başı evrenini kullan (hayatta kalma yanlılığı). Büyük hisse ve küçük/tema hisse ayrı raporlansın. Uzun ve kısa yön ayrı.
Bugün için: 23 Kasım – 18 Aralık 2026 arasında evrendeki hisselerin beklenen bilanço günleri (son dört çeyreğin tarih örüntüsünden tahmin; "tahmini" diye işaretle) ve geçen kuralların bunlara nasıl uygulanacağı.`,
    'R6-01…R6-04, R6-06, R5-07, R5-08', ['d3_R6.md', 'd3_R5.md']),

  K8: kur('K8', 'Aile S: sistematik lead-lag taraması ve boru hattı plasebosu',
    `Tek soru: Önceden yazılı hipotezlerin dışında, evrendeki sepetler ve kodlar arasında günlük lead-lag ilişkisi var mı; taramanın bulduğu "keşifler" plaseboyu aşıyor mu?
Bu görev istatistiksel olarak en riskli olanıdır (milyonlarca örtük test). YONTEM 7. bölümdeki "Sistematik tarama (S)" kurallarını harfiyen uygula:
1. Korelasyonu > 0,98 olan kodları teke indir. Hedef Y: yalnız 60 günlük dolar hacmi ≥ 200 milyon $ ve sıfır hacimli günü olmayan ABD16 kodları.
2. Test istatistiği: Y'nin korunmalı ileri getirisinin (h = 1, 2, 3), X'in artık getirisine (X − β·SPY − β·sektör) regresyonundaki katsayı; Y'nin ve SPY'nin t günü getirisi kontrol değişkeni.
3. Evreni yalnız IS (2010–2019) verisiyle ≤ 60 sepete kümele; tarama sepet → sepet ve sepet → üye düzeyinde. Sinyal girdisi X için kapanış saati sınıfına uy (SONRA sınıfı 1 gün gecikmeli; ONCE sınıfı dış endeksler aynı gün kullanılabilir).
4. IS: |t| ≥ 3,5 olanların en yüksek 200'ü aday (aday listesini OOS'a bakmadan önce dosyaya yaz). OOS: aynı yön ve 200 aday üzerinde BH %10.
5. Boru hattı plasebosu: IS seçimi → OOS onayı zincirinin tamamını ≥ 200 kez yeniden çalıştır; hedef getiri matrisi bütün Y'ler için aynı permütasyonla, 20 günlük bloklar hâlinde, aynı yıl ve aynı VIX kovası içinde yer değiştirir; X sinyalleri yerinde kalır. İkinci plasebo: sinyal +40…+250 gün dairesel kaydırma. Raporla: gerçek OOS geçen sayısı, plasebo medyanı ve %95'liği. Gerçek sayı plasebo %95'liğini aşmıyorsa taramayı "başarısız" ilan et; o zaman hiçbir tarama sinyali DÜŞÜK'ün üstüne çıkamaz.
6. Tarama başarılıysa: OOS'tan geçenleri motorun degerlendir işleviyle işlem bazında sına (maliyet, Giriş A, son dönem, rejim) ve ekonomik tabanı uygula. Geçenlerin ekonomik bir açıklaması var mı (aynı sektör, tedarik zinciri, bayat fiyat)? Bayat fiyat/eşzamansız işlem şüphesi olanları işaretle.
Motorun tarama ve plasebo yardımcılarını kullan (MOTOR.md). Hesap bütçesi: tek komut 8 dakikayı geçmesin; plaseboyu parçalara böl ve ara sonuçları ${SP}/tarama/ altına kaydet.
"ÇALIŞMA SIRASI" başlığındaki 1–3. adımlar bu görevde yukarıdaki 1–6 ile değişir; 6–7. adımlar ve dosya adları (${VERI}/aday_K8.csv, ${VERI}/sonuc_K8.csv, ${KOD}/aile_K8.py) aynı kalır.`,
    'yok (tarama); karşılaştırma için aile = A ve B satırlarına bak', ['d3_R4.md', 'd3_R5.md']),

  K9: kur('K9', 'Aile N: gece–gündüz ayrışması, çıkış varyantları ve risk/boyut tablosu',
    `İki iş (ikisi de aynı veriden):
(1) Gece–gündüz: likit araçlarda (geniş endeks, sektör, kaldıraçlı/ters ETF'ler, dönem başı evrenindeki hisseler, tema hisseleri) kapanış→açılış ve açılış→kapanış getirilerinin dönem (IS/OOS/son) ve rejim (VIX kovası × 200 günlük ortalama) kırılımı. Sınanacak kurallar: (a) koşulsuz "kapanışta al, açılışta sat" (maliyet sonrası; NY Fed'e göre 2021'den beri sıfıra yakın, doğrula); (b) satış günü sonrası koşullu gece dönüşü (R7-10: günlük getiri ≤ −%1, ≤ −%2 ve kapanış günün dibine yakınken → gece uzun); (c) yüksek VIX'te gece ile gündüz payı; (d) kaldıraçlı ETF'lerde gece tutmanın getirisi ve riski. Sonuçlar ${VERI}/sonuc_K9.csv (standart şema).
(2) Risk ve boyut tablosu → ${VERI}/risk_ve_boyut_tablosu.csv: 60 günlük dolar hacmi ≥ 100 milyon $ olan ABD16 kodları için: SPY betası (250 ve 60 gün), 1, 2 ve 3 günlük σ (son 60 gün ve son 250 gün), 1 ve 3 günlük %1 ve %99 kuyruk (2010'dan bugüne ve VIX > 30 günlerinde ayrı), gece riskinin toplam günlük varyanstaki payı, en kötü 1 ve 3 günlük getiri (tarihleriyle), maliyet sınıfı (bps), kaldıraç ve dayanak, korelasyon kümesi (son 250 gün, |ρ| ≥ 0,7), 10.000 $ sermayenin %1'ini (100 $) riske atan pozisyon büyüklüğü (1 günlük ve 3 günlük 1σ ve %99 kuyruğa göre, $ olarak). Ayrıca: SPY ile korunmanın 1–3 günlük varyansı ne kadar azalttığı (kod başına), hangi kodlarda işe yaramadığı.
Bu görevde "aday/OOS" sırası yalnız (1)'deki kurallar için geçerlidir. Özet ve tabloda en önemli 25 satırı ver; (2) için tablonun yolunu ve 10 örnek satırı (SPY, QQQ, TQQQ, SQQQ, SOXL, SOXS, NVDA, TSLA, MSTR, IBIT) notlara yaz.`,
    'R7-10 ve gece–gündüz kuralları', ['d3_R7.md', 'd3_R9.md']),
}

const MODEL = { K8: 'fable' }
const secim = (A.gorevler && A.gorevler.length) ? A.gorevler : Object.keys(G)
log('Dalga 4b backtest: ' + secim.join(', ') + ' · başarısız ajana en çok 1 yeniden deneme')

const sonuc = await parallel(secim.map((id) => async () => {
  const opts = { label: id + ' · backtest', phase: 'Backtest', schema: SEMA, model: MODEL[id] || 'opus', effort: 'high' }
  let r = await agent(G[id], opts)
  let yeniden = false
  if (!r) {
    log(id + ' sonuç döndürmedi; 1 yeniden deneme')
    yeniden = true
    r = await agent(G[id], Object.assign({}, opts, { label: id + ' · backtest (yeniden)' }))
  }
  if (r) log(id + ' bitti · ' + r.arac + ' · test ' + r.test_sayisi + ' · aday ' + r.aday_sayisi + ' · OOS geçen ' + r.oos_gecen)
  return { id, yeniden, sonuc: r }
}))
const cikti = {}
secim.forEach((id, i) => { cikti[id] = sonuc[i] ? sonuc[i] : { id, sonuc: null } })
return cikti
