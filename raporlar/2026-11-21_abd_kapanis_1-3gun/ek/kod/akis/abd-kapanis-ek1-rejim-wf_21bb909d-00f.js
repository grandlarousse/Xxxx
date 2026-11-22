export const meta = {
  name: 'abd-kapanis-ek1-rejim',
  description: 'Ek 1: rejime koşullu dönüş hipotezinin 1993–2004 verisinde, bağımsız kodla sınanması (fable)',
  phases: [
    { title: 'Ek 1 testi', detail: 'ön kayıtlı iki hipotez; dokunulmamış örneklem; bağımsız betik', model: 'fable' },
  ],
}

const SP = '/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad'
const RAPOR = '/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun'

const G = `Kontrol noktası 40 araç çağrısı; say. 40'ta dur ve kendine sor: iş bitti mi, sonuca etki eden bir eksik var mı? Yoksa bitir. Varsa ve son 5 çağrın ilerleme sağladıysa devam et; her 10 çağrıda yeniden sor. Üst sınır 80.

GÖREV KF1 — Ek 1: rejime koşullu kısa vadeli dönüş hipotezinin dokunulmamış örneklemde sınanması
Bağlayıcı belge: ${RAPOR}/ek/YONTEM.md dosyasının sonundaki "Ek 1" bölümü (hipotezler E1-a ve E1-b, örneklem, maliyet ve altı karar ölçütü orada; veriye bakılmadan önce yazıldı ve depoya kaydedildi). Önce o bölümü ve genel yöntem için 2., 4., 7. ve 9. bölümleri oku. Ölçütleri, eşikleri ya da hipotezleri değiştirme; yeni varyant ekleyip karara sokma.
Arka plan: ${RAPOR}/ek/ajanlar/d4_K4a.md (2005–2026'da aynı kuralların sonuçları; "Notlar" ve "Bugünkü durum" bölümleri).

Tek soru: VIX(t−1) > 30 ve SPY 200 günlük ortalamasının altındayken, RSI(2) < 10 (E1-a) ya da IBS < 0,2 (E1-b) kapanışında SPY alıp ertesi kapanışta satmak, 1993–2004 verisinde Ek 1'deki altı ölçütü sağlıyor mu?

Yapılacaklar
1. Veri: Yahoo chart API'den günlük veri indir (https://query1.finance.yahoo.com/v8/finance/chart/<KOD>?period1=<epoch>&period2=<epoch>&interval=1d&events=div%2Csplit ; User-Agent "Mozilla/5.0"; ^ için URL kodlaması): SPY (1993'ten), ^VIX (1990'dan), QQQ (1999'dan), DIA (1998'den), MDY (1995'ten), UPRO ve TQQQ (2010'dan). Ham dosyalar ${SP}/ek1_ham/ altına (depoya girmez). İndirilen dosyaları okuyan Python'u -I ile çalıştır.
2. Bağımsız betik: ${RAPOR}/ek/kod/ek1_rejim.py. Projenin motorunu (motor.py) KULLANMA; düz pandas/numpy ile yaz. Tanımlar:
   - Getiri düzeltilmiş kapanıştan; düzeltilmiş açılış = açılış × düzeltilmiş kapanış / kapanış.
   - RSI(2): Wilder yumuşatması, düzeltilmiş kapanıştan. IBS = (kapanış − düşük)/(yüksek − düşük), bölünme düzeltmeli fiyatlardan.
   - Rejim: VIX(t−1) > 30 (VIX 16:15'te kapanır; aynı gün değeri kullanma) ve SPY(t−1) kapanışı < SPY'nin t−1'e kadar 200 günlük ortalaması (temettüsüz kapanıştan).
   - İşlem: sinyal günü t kapanışında al, t+1 kapanışında sat. Örtüşme h = 1'de sorun değil; ikincil h = 2, 3'te açık pozisyon varken yeni sinyal alınmaz.
   - Bölüm: aralarında 20'den az VIX ≤ 30 günü olan VIX > 30 günleri tek bölümdür.
   - Anormal getiri: işlem getirisi − aynı örneklemde, aynı rejimdeki (VIX(t−1) > 30 ve 200 günlük ortalamanın altı) bütün günlerin koşulsuz 1 günlük ortalaması.
   - Oynaklığa ölçeklenmiş getiri: net getiri / SPY'nin t−1'e kadar 20 günlük günlük σ'sı.
3. Birincil test (karar): örneklem 1993-02-01 → 2004-12-31, yalnız E1-a ve E1-b, h = 1, SPY. Ek 1'deki altı ölçütü tek tek hesapla ve her birinin sağlanıp sağlanmadığını yaz; sınıfı (KOŞULLU / DÜŞÜK / ELENDİ) Ek 1 kuralına göre ver. İşlem sayısı azsa bunu açıkça yaz; ölçütleri yumuşatma.
4. Çapraz kontrol: aynı betikle 2005-01-03 → 2026-11-20'yi yeniden üret ve K4a'nın sayılarıyla karşılaştır (SPY RSI(2) < 10, h = 1, rejim "VIX > 30 ve 200 günlük ortalamanın altı": 61 işlem, yaklaşık +141 bps, t 2,8; IBS < 0,2: 102 işlem, yaklaşık +81 bps). Maliyet tanımı farklı olabilir; brüt ortalamayı ve işlem sayısını karşılaştır, farkı açıkla.
5. İkincil (karara girmez; betimsel): (a) h = 2, 3 ve ertesi açılışta giriş; (b) QQQ, DIA, MDY'de aynı kurallar (rejim yine VIX ve SPY'den); (c) rejim dışındaki günlerde aynı kurallar: etki rejime mi özgü; (d) bölüm tablosu, 1993–2026'nın tamamı: bölüm başına işlem sayısı, toplam, en kötü işlem, en uzun ardışık kayıp; 2000–2002 Nasdaq çöküşünde QQQ için ayrıca; (e) 2010 sonrasında aynı sinyalin UPRO ve TQQQ ile getirisi ve en kötü işlemler; (f) Ekim–Kasım 2026 bölümündeki işlemler tek tek (tarih, getiri); (g) 20 Kasım 2026 kapanışındaki durum ve 23 Kasım kapanışı için tetik seviyeleri (SPY fiyatı olarak): RSI(2) < 10 ve IBS < 0,2 hangi kapanışta sağlanır; VIX(t−1) ve 200 günlük ortalama koşulu.
6. Sonuç tabloları: ${RAPOR}/ek/veri/ek1_sonuc.csv (ölçütler ve ikincil satırlar), ${RAPOR}/ek/veri/ek1_islemler.csv (bütün işlemler: örneklem, kural, tarih, getiri, bölüm), ${RAPOR}/ek/veri/ek1_bolumler.csv.
Dürüstlük: sonuç "ELENDİ" ise bunu yaz; bu da bir bulgudur. Sonuç inanılmayacak kadar iyiyse önce ileriye bakma ya da veri hatası ara (VIX gecikmesi, 200 günlük ortalamanın t günü verisini içermesi, RSI'ın t+1 verisini kullanması). git commit/push yapma. Kendi alt ajanını başlatma. Görev dışına çıkma.
Ortam: python3, pandas 3.0, numpy; scipy yok (paket kurma). Ağ çıkışı vekil sunucu üzerinden; curl ortam değişkenleriyle çalışır.

DÖNÜŞ BİÇİMİ (StructuredOutput alanları)
- arac: "araç: <kullandığın>/40".
- karar_a: E1-a için sınıf (KOŞULLU / DÜŞÜK / ELENDİ) ve altı ölçütün her biri için sayı ve "sağlandı / sağlanmadı".
- karar_b: E1-b için aynısı.
- ozet: en çok 350 kelime: birincil sonuç, çapraz kontrol, ikincil bulguların en önemlileri, en büyük çekince.
- capraz_kontrol: 2005–2026 yeniden üretimi ile K4a sayılarının karşılaştırması.
- ikincil: (a)–(f) için kısa sayısal özet.
- bugun: (g) maddesi.
- dosyalar: tam yollar.
- notlar: veri sorunları, yorum gerektiren noktalar.
Hatırlatma: kontrol noktası 40 araç çağrısı, üst sınır 80.`

const SEMA = {
  type: 'object',
  properties: {
    arac: { type: 'string' }, karar_a: { type: 'string' }, karar_b: { type: 'string' }, ozet: { type: 'string' },
    capraz_kontrol: { type: 'string' }, ikincil: { type: 'string' }, bugun: { type: 'string' },
    dosyalar: { type: 'array', items: { type: 'string' } }, notlar: { type: 'string' },
  },
  required: ['arac', 'karar_a', 'karar_b', 'ozet', 'capraz_kontrol', 'ikincil', 'bugun', 'dosyalar', 'notlar'],
}
const opts = { label: 'KF1 · Ek 1 rejim testi', phase: 'Ek 1 testi', schema: SEMA, model: 'fable', effort: 'high' }
let r = await agent(G, opts)
if (!r) { log('KF1 sonuç döndürmedi; 1 yeniden deneme'); r = await agent(G, Object.assign({}, opts, { label: opts.label + ' (yeniden)' })) }
return { KF1: r }
