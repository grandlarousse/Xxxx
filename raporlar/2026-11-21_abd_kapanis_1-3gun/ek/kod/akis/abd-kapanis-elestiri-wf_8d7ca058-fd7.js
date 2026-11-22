export const meta = {
  name: 'abd-kapanis-elestiri',
  description: 'Rapor taslağının iki fable eleştirmeni: (1) sayı ve çıkarım denetimi, (2) okur gözüyle kullanılabilirlik ve ana sonuca itiraz',
  phases: [
    { title: 'Eleştiri', detail: 'taslak rapor iki bağımsız mercekle eleştirilir; düzeltmeyi ana ajan yapar', model: 'fable' },
  ],
}

const SP = '/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad'
const RAPOR = '/home/user/Xxxx/raporlar/2026-11-21_abd_kapanis_1-3gun'

const ORTAK = `Dosyalar: taslak rapor ${RAPOR}/RAPOR.md ; yöntem ve ön kayıtlar ${RAPOR}/ek/YONTEM.md (Sapmalar, Ek 1, Ek 2 dahil) ; ajan özetleri ${RAPOR}/ek/ajanlar/ (d4_K*.md backtest aileleri, d5_KF1.md 1993–2004 sınavı, d5_RF1a.md ve d5_RF1b.md maliyet senaryosu, d4_KD.md motor denetimi, d2_M.md yöntem denetimi, d3_R*.md araştırma defterleri) ; doğrulama sonuçları ${RAPOR}/ek/dogrulama/ ; sonuç tabloları ${RAPOR}/ek/veri/ (sonuc_K*.csv büyük dosyalardır; tamamını okuma, pandas ile süz).
Okur: Türkiye'de yerleşik bireysel yatırımcı. BIST VİOP'ta lead-lag sinyalleriyle, kapanışta girip 1–3 gün taşıyarak işlem yapıyor; aynı yöntemi ABD'de uygulayıp "riskini kabul ederek ciddi kazanç" elde edebileceği ETF ve hisseleri sordu. Raporu telefonda okuyacak ve buna göre para kararı verecek. Önceki çalışması (biçim ve beklenti için): /home/user/Xxxx/raporlar/2026-11-04_kapanis_1-3gun/PRATIK_LISTE.md .
Raporu DEĞİŞTİRME; dosya yazma. Bulgularını döndür, düzeltmeyi ana ajan yapacak. Kendi alt ajanını başlatma. Görev dışına çıkma.`

const E1 = `Kontrol noktası 30 araç çağrısı; say. 30'da dur ve kendine sor: raporun bütün sayıları ve çıkarımları denetlendi mi? Denetlenmediyse ve son 5 çağrın yeni bulgu getirdiyse devam et; her 10 çağrıda yeniden sor. Üst sınır 60.

GÖREV E1 — Sayı ve çıkarım denetimi (eleştirmen)
${ORTAK}
Tek soru: Bu rapordaki sayılar kaynak dosyalarla tutuyor mu ve sonuçlar kanıttan gerçekten çıkıyor mu? Varsayılan tutumun şüphe.
Yapılacaklar:
1. Rapordaki her sayıyı (tablolar dahil) kaynağıyla karşılaştır: aile tablosu (3.2), en yakın adaylar (3.3), rejim ve 1993–2004 sınavı (3.4), maliyet senaryosu (3.5), kaldıraçlı ETF tablosu (3.7), risk tablosu (3.8). Ajan özetleriyle yetinme: en az 12 sayıyı sonuç CSV'lerinden kendin yeniden hesapla (python3 -I; pandas). Uyuşmayan her sayıyı doğru değeriyle bildir.
2. Çıkarım denetimi: (a) "kullanılabilir kural yok" hükmü, yöntemin kendi ölçütlerine göre doğru mu; ölçütlerin haksız yere elediği güçlü bir kural var mı (özellikle 2010–2019 keşif eleğinin sakin dönem olması, tek yönlü kurallardaki anormal getiri şartı, 5 pozisyon tavanı, maliyet modeli)? Sonuç CSV'lerinde "keşifte elendi ama 2020–2023 VE 2024–2026'da güçlü" olan kuralları ara ve en çarpıcı 5 tanesini sayılarıyla listele; bunların neden kanıt sayılamayacağını ya da raporda neden anılması gerektiğini söyle. (b) Aileler arası çoklu test düzeltmesi hükmü doğru mu? (c) 3.6'daki "lead-lag neden çalışmıyor" açıklaması kanıtın ötesine geçiyor mu? (d) 3.12'deki izleme listesi, elenmiş kuralları önermekle raporun kendi mantığıyla çelişiyor mu? (e) "Ne yapmalıyım" 6. madde (VİOP yönü) bu çalışmanın kanıtıyla destekleniyor mu, yoksa açıkça çıkarım olarak mı etiketlenmeli?
3. Eksik çekince: rapora girmesi gereken ama girmemiş, kararı etkileyen sınır ya da bulgu var mı (ajan özetlerindeki "Notlar" ve "Sapmalar" bölümlerine bak)?
4. Yanıltma riski: okurun yanlış bir işleme girmesine yol açabilecek cümle var mı (ör. betimsel bir tablonun sinyal gibi okunması)?

DÖNÜŞ BİÇİMİ (StructuredOutput alanları)
- arac: "araç: <kullandığın>/30".
- karar: tek paragraf: rapor bu hâliyle teslim edilebilir mi; hangi düzeltmeler şart.
- bulgular: en çok 20 satır; onem (kritik / önemli / küçük) | yer (bölüm ve cümle) | sorun | duzeltme (rapora aynen yazılabilecek metin ya da doğru sayı) | kanit (dosya ve hesap).
- yeniden_hesap: kendin yeniden hesapladığın sayıların listesi (rapordaki değer, bulduğun değer, dosya).
- gozden_kacan: keşifte elenmiş ama sonraki iki dönemde güçlü kurallar ve değerlendirmen.
Hatırlatma: kontrol noktası 30 araç çağrısı, üst sınır 60.`

const E2 = `Kontrol noktası 15 araç çağrısı; say. 15'te dur ve kendine sor: eleştiri tamam mı? Değilse ve son 5 çağrın yeni bulgu getirdiyse devam et. Üst sınır 30.

GÖREV E2 — Okur gözüyle eleştiri ve ana sonuca itiraz (eleştirmen)
${ORTAK}
İki iş:
A) Okur gözüyle: raporu baştan sona, telefonda okuyan ve finans akademisyeni olmayan bir yatırımcı gibi oku.
 - İlk 6 satır soruyu yanıtlıyor mu? Okur "peki ben ne yapacağım" sorusunun yanıtını 2. bölümde somut ve uygulanabilir buluyor mu?
 - Açıklanmadan kullanılan terim, kısaltma ya da içeriden etiket var mı (ör. RSI(2), IBS, MOC, bps, plasebo, çoklu test, korunma, kuyruk, keşif dönemi)? Hangi cümleler iki kez okunmadan anlaşılmıyor?
 - Telefonda sorun çıkaracak tablo (çok sütunlu, uzun hücreli) var mı?
 - Rapor okuru küçümsüyor ya da hayal kırıklığını geçiştiriyor mu; "sonuç olumsuz" haberini dürüst ama yararlı biçimde veriyor mu? Okurun asıl isteğine ("ciddi kazanç") yanıt olarak eksik kalan, ama kanıtla desteklenebilecek bir şey var mı?
 - Biçim kuralları: sıra kısa yanıt → ne yapmalıyım → gerekçe ve kanıt → emin olunmayanlar ve doğrulama kapsamı → kaynaklar → devam notu; kısa yanıt en çok 6 satır; devam notu 5 satır; sade Türkçe.
B) Ana sonuca itiraz ("tartışın" turu): raporun ana hükmüne ("ABD'de bu yöntemle kullanılabilir kural yok") en güçlü üç itirazı kur ve her birini kanıta karşı sına. Örnek yönler: yöntem fazla katı olduğu için gerçek kenarları eledi mi; evren ve kural seçimi yanlış yerlere mi baktı (ör. gün içi olmayan ama kapanışta bilinen başka bilgi türleri, opsiyon piyasası, ADR/yerel piyasa farkı, haber/duyuru sonrası); 2020 sonrası rejim değişimi keşif dönemini geçersiz mi kılıyor. Her itiraz için: itiraz kanıt karşısında ayakta kalıyor mu; kalıyorsa raporda nasıl anılmalı (tek cümle).
Dosyaları okumak dışında araç kullanman gerekmeyebilir; gerekirse küçük kontroller yapabilirsin.

DÖNÜŞ BİÇİMİ (StructuredOutput alanları)
- arac: "araç: <kullandığın>/15".
- karar: tek paragraf: rapor okur için bu hâliyle yeterli mi; en önemli üç değişiklik.
- bulgular: en çok 20 satır; onem (kritik / önemli / küçük) | yer | sorun | duzeltme (rapora aynen yazılabilecek metin).
- itirazlar: üç itiraz; her biri için itiraz, kanıt karşısındaki durumu, raporda anılma biçimi.
Hatırlatma: kontrol noktası 15 araç çağrısı, üst sınır 30.`

const bulgu = { type: 'object', properties: { onem: { type: 'string', enum: ['kritik', 'önemli', 'küçük'] }, yer: { type: 'string' }, sorun: { type: 'string' }, duzeltme: { type: 'string' }, kanit: { type: 'string' } }, required: ['onem', 'yer', 'sorun', 'duzeltme'] }
const S1 = { type: 'object', properties: { arac: { type: 'string' }, karar: { type: 'string' }, bulgular: { type: 'array', maxItems: 20, items: bulgu }, yeniden_hesap: { type: 'string' }, gozden_kacan: { type: 'string' } }, required: ['arac', 'karar', 'bulgular', 'yeniden_hesap', 'gozden_kacan'] }
const S2 = { type: 'object', properties: { arac: { type: 'string' }, karar: { type: 'string' }, bulgular: { type: 'array', maxItems: 20, items: bulgu }, itirazlar: { type: 'string' } }, required: ['arac', 'karar', 'bulgular', 'itirazlar'] }

const [e1, e2] = await parallel([
  async () => {
    const o = { label: 'E1 · sayı ve çıkarım denetimi', phase: 'Eleştiri', schema: S1, model: 'fable', effort: 'high' }
    let r = await agent(E1, o)
    if (!r) { log('E1 sonuç döndürmedi; 1 yeniden deneme'); r = await agent(E1, Object.assign({}, o, { label: o.label + ' (yeniden)' })) }
    return r
  },
  async () => {
    const o = { label: 'E2 · okur gözü ve itiraz', phase: 'Eleştiri', schema: S2, model: 'fable', effort: 'high' }
    let r = await agent(E2, o)
    if (!r) { log('E2 sonuç döndürmedi; 1 yeniden deneme'); r = await agent(E2, Object.assign({}, o, { label: o.label + ' (yeniden)' })) }
    return r
  },
])
return { E1: e1, E2: e2 }
