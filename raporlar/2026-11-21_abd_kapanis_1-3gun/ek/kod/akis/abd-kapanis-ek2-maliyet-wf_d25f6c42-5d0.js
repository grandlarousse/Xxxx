export const meta = {
  name: 'abd-kapanis-ek2-maliyet',
  description: 'Ek 2: maliyet duyarlılığı. Dokuz aile, kapanış müzayedesi emri senaryosuyla (yalnız komisyon) yeniden elenir: önce IS, sonra OOS (opus, 2 ajan)',
  phases: [
    { title: 'Maliyet duyarlılığı', detail: 'aynı kurallar, müzayede emri maliyetiyle; ön kayıtlı ölçütler', model: 'opus' },
  ],
}

const SP = '/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad'
const RAPOR = '/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun'
const KOD = RAPOR + '/ek/kod'
const VERI = RAPOR + '/ek/veri'
const AJ = RAPOR + '/ek/ajanlar'

const gorev = (ad, aileler, not) => `Kontrol noktası 40 araç çağrısı; say. 40'ta dur ve kendine sor: iş bitti mi, sonuca etki eden bir eksik var mı? Yoksa bitir. Varsa ve son 5 çağrın ilerleme sağladıysa devam et; her 10 çağrıda yeniden sor. Üst sınır 80.

GÖREV ${ad} — Ek 2: maliyet duyarlılığı (kapanış müzayedesi emri senaryosu)
Bağlayıcı belge: ${RAPOR}/ek/YONTEM.md, özellikle sonundaki "Ek 2" (senaryo, kapsam, sıra ve karar ölçütleri orada; bu senaryoyla hiçbir sonuç hesaplanmadan önce yazıldı ve depoya kaydedildi) ile 4., 7., 9. bölümler ve "Sapmalar". Ölçütleri, kuralları ya da varyantları değiştirme; yeni kural ekleme.
Arka plan: birincil analizde (piyasa emrine göre kurulu maliyet modeli) on backtest ailesinden örneklem dışı dönemi geçen ve çoklu test düzeltmesinden kalan kural çıkmadı. Bu görev o sonucu çürütmeye çalışır: aynı kurallar, kapanış/açılış müzayedesi emrinin maliyetiyle (bacak başına yalnız 1,5 bps komisyon) yeniden elenir.

Senin payın: ${aileler.map((a) => 'aile_' + a + '.py').join(', ')} (betikler ${KOD}/ altında; sonuç ve özetleri ${AJ}/d4_<aile>.md ve ${VERI}/sonuc_<aile>.csv).
${not}

Yapılacaklar
1. ${KOD}/MOTOR.md dosyasını oku (özellikle sonundaki "Ana ajan düzeltmeleri": motora "muzayede" komisyon senaryosu eklendi; degerlendir(..., komisyon=("muzayede",)) ile istenir; işlem listelerinde net_muzayede sütunu var).
2. Her aile betiği için: betiğin kural üretimini AYNEN kullan (aynı sinyaller, aynı varyantlar, aynı h ve çıkışlar). Özgün betikleri DEĞİŞTİRME; gerekiyorsa ${KOD}/ek2_<aile>.py adıyla kopyala ya da modül olarak içe aktarıp sinyal işlevlerini çağır. Tek fark: eleme ve değerlendirme "muzayede" komisyon senaryosuyla yapılır.
3. ÖNCE YALNIZ IS (2010–2019; "yeni yapı" hattındaki kurallar için 2020–2023): aday = net > 0 ve ilgili t ≥ 2 (tek hedefli kuralda t_olcekli; çok hedefli kuralda t_kume; tek yönlü kuralda ayrıca t_anormal ≥ 2). Aday listesini OOS'a bakmadan ÖNCE ${VERI}/aday_ek2_${ad}.csv dosyasına yaz. Her aile için birincil analizdeki aday sayısını da (d4_<aile>.md'den) yanına not et.
4. SONRA OOS (2020–2023; yeni yapı hattında 2024–2026), yalnız adaylar, bootstrap=True. Her aday için: OOS net, ilgili t, t_anormal (tek yönlüyse), p_bootstrap (hesaplanamazsa 1,0), işlem sayısı.
5. OOS'ta aynı yön ve ilgili t ≥ 2 olan her kural için Ek 2'deki ölçütleri tek tek hesapla: (b) OOS t ≥ 2,5 mi; (c) son dönem (2024–2026-11-20) net ve t; (d) kapanış gerçekçiliği: Giriş A (ertesi açılış) net ve t; ayrıca yukle.saatlik() ile son 730 günde sinyali kapanış yerine 15:30 fiyatıyla hesaplayıp aynı günlerde tetiklenme örtüşmesi ve kazancın korunan payı; (e) en iyi %5 işlem çıkarılınca net; (f) net ≥ 10 bps ve net/σ ≥ 0,10. Ayrıca: uzun ve kısa bacak ayrı, VIX > 30 bölümleri, yıllara göre net, birincil maliyetle ('hisse') aynı satır (karşılaştırma için). (a) maddesindeki aileler arası BH'yi ana ajan yapacak: bütün adayların OOS p-değerlerini döndür.
6. Bütün satırları motorun standart şemasıyla ${VERI}/sonuc_ek2_${ad}.csv dosyasına yaz.
7. OOS'tan geçen kural varsa: 20 Kasım 2026 kapanışında sinyal açık mı; 23 Kasım kapanışı için tetik koşulu (fiyat/eşik olarak).
Dürüstlük: sonuç "bu senaryoda da geçen yok" ise bunu yaz; bu da bir bulgudur. Bir sonuç inanılmayacak kadar iyiyse (işlem başına > 100 bps, t > 6) önce ileriye bakma ya da veri hatası ara (m.bakis_testi). motor.py ve yukle.py dosyalarına dokunma. Motorun önbellekten döndürdüğü nesneleri yerinde değiştirme. git commit/push yapma. Kendi alt ajanını başlatma. Görev dışına çıkma.
Ortam: python3, pandas 3.0, numpy; makine 4 çekirdek, başka bir ajan da aynı anda çalışıyor: OMP_NUM_THREADS=1 kullan, tek komutu 8 dakikadan uzun kurma, uzun işleri parçalara böl ve ara sonuçları ${SP}/ek2/ altına kaydet. Panel: import sys; sys.path.insert(0, "${KOD}"); from yukle import panel.

DÖNÜŞ BİÇİMİ (StructuredOutput alanları)
- arac: "araç: <kullandığın>/40".
- ozet: en çok 350 kelime: bu senaryoda ne değişti, ne ayakta kaldı, en önemli çekince.
- aile_tablosu: aile başına bir satır: aile | sınanan varyant | birincil maliyetle IS adayı | müzayede maliyetiyle IS adayı | OOS'ta aynı yön ve t ≥ 2 | Ek 2 ölçütlerinin hepsini (a hariç) sağlayan.
- adaylar: en çok 30 satır (önce OOS'ta t ≥ 2 olanlar, sonra en yakınlar): kural_id, aile, ad, hedef, yon, h, cikis, korunma, is_net_bps, is_t, oos_net_bps, oos_n, oos_t, oos_t_anormal, oos_p, son_net_bps, son_t, girisA_oos_net_bps, girisA_oos_t, en_iyi5suz_bps, saatlik_1530 (kısa metin), birincil_oos_net_bps, olcutler (b–f için "b+ c− d+ e+ f+" gibi), gerekce.
- bugun: madde 7.
- dosyalar: tam yollar.
- sapmalar: Ek 2'den ya da özgün betikten her sapma (yoksa "yok").
- notlar: sorunlar, şüpheli sonuçlar.
Hatırlatma: kontrol noktası 40 araç çağrısı, üst sınır 80.`

const satir = {
  type: 'object',
  properties: {
    kural_id: { type: 'string' }, aile: { type: 'string' }, ad: { type: 'string' }, hedef: { type: 'string' }, yon: { type: 'string' }, h: { type: 'string' }, cikis: { type: 'string' }, korunma: { type: 'string' },
    is_net_bps: { type: 'number' }, is_t: { type: 'number' }, oos_net_bps: { type: 'number' }, oos_n: { type: 'number' }, oos_t: { type: 'number' }, oos_t_anormal: { type: 'number' }, oos_p: { type: 'number' },
    son_net_bps: { type: 'number' }, son_t: { type: 'number' }, girisA_oos_net_bps: { type: 'number' }, girisA_oos_t: { type: 'number' }, en_iyi5suz_bps: { type: 'number' },
    saatlik_1530: { type: 'string' }, birincil_oos_net_bps: { type: 'number' }, olcutler: { type: 'string' }, gerekce: { type: 'string' },
  },
  required: ['kural_id', 'aile', 'ad', 'hedef', 'h', 'gerekce'],
}
const SEMA = {
  type: 'object',
  properties: {
    arac: { type: 'string' }, ozet: { type: 'string' },
    aile_tablosu: { type: 'array', items: { type: 'object', properties: { aile: { type: 'string' }, varyant: { type: 'number' }, is_aday_birincil: { type: 'number' }, is_aday_muzayede: { type: 'number' }, oos_t2: { type: 'number' }, ek2_gecen: { type: 'number' } }, required: ['aile', 'varyant', 'is_aday_muzayede', 'oos_t2', 'ek2_gecen'] } },
    adaylar: { type: 'array', maxItems: 30, items: satir },
    bugun: { type: 'string' }, dosyalar: { type: 'array', items: { type: 'string' } }, sapmalar: { type: 'string' }, notlar: { type: 'string' },
  },
  required: ['arac', 'ozet', 'aile_tablosu', 'adaylar', 'bugun', 'dosyalar', 'sapmalar', 'notlar'],
}

const ISLER = [
  { ad: 'RF1a', aileler: ['K1', 'K2', 'K3', 'K7'], not: 'Not: K1 (lider → takipçi), K2 (çiftler, artık ve kesitsel dönüş), K3 (çapraz varlık) ve K7 (bilanço) ailelerinde brüt etki var ama birincil maliyetin altında kalıyordu; duyarlılık en çok burada beklenir. K7 için bilinen kısıt: tepki günü uyuşmazlığı %12–20 olduğundan bu aile en çok KOŞULLU olabilir. K1 ve K2 betiklerindeki bakis_testi sütun kümesi notlarına (d4_K1.md, d4_K2.md "Notlar") dikkat et.' },
  { ad: 'RF1b', aileler: ['K4a', 'K4b', 'K5', 'K6', 'K9'], not: 'Not: K4a (uç hareket; 674 varyant, betik uzun sürebilir: parçalara böl), K4b (akış vekilleri, genişlik), K5 (takvim), K6 (volatilite ürünleri ve DIX/GEX; ödünç ücreti aynen kalır), K9 (gece–gündüz; burada maliyet belirleyiciydi: koşulsuz "kapanışta al, açılışta sat" kurallarında anormal getiri tanım gereği sıfırdır ve t_anormal şartı onları eler; bunu değiştirme, ama koşulsuz gece getirisinin bu senaryodaki netini betimsel olarak raporla). K4a ve K4b\'de "düşeni al" kuralları için ayrıca Ek 1 sonucu bilgin olsun: aynı kurallar 1993–2004 verisinde elendi (' + AJ + '/d5_KF1.md).' },
]
const sonuc = await parallel(ISLER.map((i) => async () => {
  const opts = { label: i.ad + ' · maliyet duyarlılığı', phase: 'Maliyet duyarlılığı', schema: SEMA, model: 'opus', effort: 'high' }
  const p = gorev(i.ad, i.aileler, i.not)
  let r = await agent(p, opts)
  if (!r) { log(i.ad + ' sonuç döndürmedi; 1 yeniden deneme'); r = await agent(p, Object.assign({}, opts, { label: opts.label + ' (yeniden)' })) }
  if (r) log(i.ad + ' bitti · ' + r.arac)
  return { ad: i.ad, sonuc: r }
}))
return sonuc
