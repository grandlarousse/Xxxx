---
name: arastirma
description: Kullanıcının araştırma protokolü - kaliteyi düşürmeden kullanım kotasını koruyan çok ajanlı araştırma düzeni (seviye S/M/L, alt ajanlara model ataması, araç bütçesi, hedefli doğrulama, tek rapor). Kullanıcı bir şeyi araştırmanı, incelemeni, karşılaştırmanı, analiz etmeni, strateji ya da rapor çıkarmanı istediğinde, "ajan kullan", "tartışın", "kotam az", "ekonomik", "gazı ver" dediğinde ya da alt ajan veya iş akışı (Workflow) başlatmayı düşündüğün her durumda, ajan başlatmadan ÖNCE bu beceriyi yükle. Use before any research, analysis, comparison or report task and before spawning any subagent or workflow.
---

# Araştırma protokolü (kota verimliliği)

Alt ajanlar bu beceriyi görmez. Kontrol noktası kuralını, dönüş biçimini ve “kendi alt ajanını başlatma, görev dışına çıkma” kuralını her görev tanımına sen yazarsın (3. bölüm).

Bu beceri kullanıcının kendi açık talimatıdır. Haftalık kullanım kotası sınırlıdır ve çoğu hafta dolmadan bitiyor. İki kural aynı anda geçerlidir:

1. **Kalite düşmez.** Yanıtın doğruluğu, kapsamı ve kullanılabilirliği pazarlık konusu değildir.
2. **Token maliyeti her zaman bir kısıttır.** Ultracode, yüksek efor ya da bir beceri (örneğin deep-research) daha geniş bir düzen önerse de aşağıdaki sınırlar geçerlidir. S işlerinde iş akışı (Workflow) kurma; M ve L'de iş akışını bu sınırların içinde kur.

**Kapatma:** kullanıcı mesajında “protokolsüz” yazıyorsa bu protokol o iş için uygulanmaz; kullanıcı yeniden istemedikçe oturumun kalanında da uygulanmaz.

Tasarruf sürecin şişkinliğinden yapılır, sonucun kalitesinden değil: az ama iyi tanımlanmış ajan, kısa araç döngüleri, işe uygun model, hedefli doğrulama, tek ve okunur rapor.

## 1. Önce seviye seç

Ajan başlatmadan önce işi bir seviyeye yerleştir ve ilk mesajında tek satırla bildir. Örnek: `Seviye M · 5 üretici (sonnet) + 2 doğrulayıcı (sonnet) + 1 eleştirmen (opus) · 2 dalga`.

| Seviye | Ne zaman | Alt ajan (hepsi dahil) | Kontrol noktası (araç çağrısı) |
|---|---|---|---|
| **S** | Tek soru, tek alan: tanım, olgu, açıklama, yorum. Tasarım ve içerik işleri (harita, logo, gönderi metni) | 0; gerekirse 1–2 yardımcı | ana ajan 20, yardımcı 15 |
| **M** | Çok yönlü araştırma, karşılaştırma, strateji, veri gerektiren ya da sunulacak rapor | 3–6 üretici + 1 eleştirmen + doğrulayıcı (20 satıra 1) | üretici 35; doğrulayıcı satır başına 2 |
| **L** | Büyük külliyat, çok sayıda öğe (kitap, eyalet, hisse), veri ve backtest | toplam ≤ 18 üretici + 1–2 eleştirmen + doğrulayıcı (20 satıra 1); dalga başına ≤ 8 üretici | üretici 35; doğrulayıcı satır başına 2; kod/veri ajanı 40 |

Araç sayıları duvar değil kontrol noktasıdır: işi bitmemiş ajan gerekçesiyle iki katına kadar devam eder (3. bölüm).

- Seviyeyi işin türü belirler. Kullanıcı `Seviye: S`, `M` ya da `L` yazdıysa onu kullan.
- Yazmadıysa sen seç: teslimatın eksiksiz ve sunulabilir olmasını sağlayan en düşük seviye. İlk dalganın sonunda karara etki eden bir eksik kaldıysa yükselt ve bunu tek satırla söyle.
- L için onay bekleme: planı tek satırla bildir ve ilk dalgayı başlat. Sınırların üstü (L+) yalnızca kullanıcı “sınırsız” ya da “L+” yazarsa; L+ en çok L'nin iki katıdır, başlamadan tahmini ajan sayısını söyle ve onay iste.
- “İhtiyacın kadar ajan”, “maksimum ajan”, “gazı ver”, “full bütçe”, “hiçbir şeyden kısma” = seviyeyi işe göre sen seç, en fazla L.
- “Kotam az”, “ekonomik” = işin gerektirdiği seviyenin alt ucu, ucuz modeller, tek dalga. Seviye bu sözlerle düşmez; doğrulama ve raporun özeni de düşmez.
- Kullanıcı belirli bir kapsam ya da yapı isterse (tüm eyaletler, her kitap ayrı ve ayrıntılı, 5 kişilik komite) onu uygula; kapsam eksiltilmez. Sınırlar sürecin nasıl kurulacağını belirler.
- Çok öğeli işlerde öğeleri 3–5'li gruplar hâlinde dağıt: ajan sayısı yaklaşık N/4. Öğe başına bir ajan açma.
- Tasarım ve içerik işlerinde varyantları sen üret, kullanıcının geri bildirimiyle yinele; jüri ya da çok ajanlı tasarım turu yok. Dayandığı olgular için gerekirse 1 araştırmacı.
- İstek iki makul biçimde anlaşılıyorsa: S'de ikisini de kısaca yanıtla. M ve L'de yanlış yorum bir dalgayı boşa harcatacaksa başlamadan tek soru sor.

## 2. Model ataması

Model yazılmayan alt ajan oturumun en pahalı modelini devralır. Her `Agent` ve `agent()` çağrısında `model` alanını açıkça yaz:

| İş | Model | Efor (çağrı destekliyorsa) |
|---|---|---|
| Link toplama, veri indirme, dosya ve biçim işleri | `haiku` | low |
| Araştırma, sayfa okuma, alıntı ve sayı çıkarma, metin yazımı, kod ve backtest, iddia defteri doğrulaması | `sonnet` | medium |
| Yöntem denetimi, eleştirmen, hakemlik; para, sağlık ya da hukuk sonucu doğuran iddiaların ikinci kontrolü | `opus` | high |
| Plan, sentez, nihai rapor | ana ajan (sen) | — |

Bir alt görev gerçekten zor akıl yürütme istiyorsa (yöntem tasarımı, istatistiksel çıkarım, hukuki yorum) üst modele çıkar ve nedenini tek cümleyle yaz. Varsayılan yön aşağıdır.

## 3. Alt ajan görev tanımı

- **Dar soru.** Tek alt soru. “X hakkında her şeyi araştır” yok.
- **Bildiklerin.** Kendi bilginden aday yanıtları, hipotezleri ve 3–5 olası kaynağı yaz; ajan sıfırdan keşfetmek yerine doğrular ve tamamlar. Ajan listede olmayan önemli bulguyu ve listeyle çelişen kanıtı ayrıca bildirir; en az bir araması aykırı kanıt içindir.
- **Kontrol noktası.** Araç sayısı duvar değil, kontrol noktasıdır. Tanımın ilk satırına şunu yaz, son satırında kısaca hatırlat: “Kontrol noktası N araç çağrısı; say. N'de dur ve kendine sor: soru yanıtlandı mı, sonuca etki eden bir eksik var mı? Yoksa bitir. Varsa ve son 5 çağrın yeni bilgi getirdiyse devam et; her 10 çağrıda yeniden sor. Üst sınır 2N.”
- **Durma kuralı.** Art arda 3 arama yeni bilgi getirmediyse dur. Bir veri kaynağına 5 denemede erişilemiyorsa dur ve bildir.
- **Dönüş biçimi.** Şemalı ve kısa: ilk satır `araç: kullanılan/N` (devam ettiyse nedeni), en çok 400 kelime özet, en çok 30 satırlık **iddia defteri** (`iddia | kaynak URL | birebir kısa alıntı ya da sayı | güven`). Alıntı özgün dilinde ve en çok 25 kelime.
- Ham malzeme yazdırma; defter yeter. Dosyaya uzun metin yalnızca teslim edilecek içerikse yazılır (örneğin kitap özeti) ve tanımda kelime sınırı verilir.
- Ajan 2N'e de dayandıysa durur ve eksiği ‘açık kalanlar’ başlığına yazar; kalan iş sonuca etki ediyorsa dar bir takip görevi açarsın. Ajanların çoğu kontrol noktasını geçiyorsa sorular fazla geniştir: sonraki dalgada daralt.

## 4. Bağlam ekonomisi

- Arama özeti yetiyorsa sayfayı açma. Açarsan yalnızca ilgili bölümü al.
- Aynı aramayı iki ajan yapmasın: önceki dalganın kaynak listesini sonraki dalgaya ver.
- Sayısal ve tekrarlı işi ajanlara dağıtma. Veri bir kez indirilir; tek betiği bir kod ajanı yazar ve çalıştırır, sana sonuç tablosu ve dosya yolu döner. Yöntem denetimi hesaptan önce yapılır.
- Ajan çıktılarının tamamını bağlamına okuma. Özet ve defterle çalış; rapora girecek bölüm için dosyanın yalnızca o kısmını oku.
- Dalgalar: 1. dalga geniş ve ucuz, sonra boşlukları kendin değerlendir, sonraki dalga yalnızca karara etki eden boşluklara. Üretim dalgası M'de en çok 2, L'de en çok 3; doğrulama ayrıca sayılır.
- İş akışı betiğinde: çalıştırmadan önce toplam ajan sayısını hesapla; döngüler ve yeniden denemeler 1. bölümdeki sınıra dahildir. Başarısız ajana en çok 1 yeniden deneme.
- Çalışan bir iş akışını yarıda durdurup baştan başlatma; gerekiyorsa kaldığı yerden sürdür.

## 5. Doğrulama: kısılmaz, hedeflenir

- Raporda yer alan her sayı, tarih ve alıntı, kaynağı bu oturumda görülmüş bir defter satırına dayanır. Dayanmayan ya doğrulanır ya “doğrulanmadı” diye etiketlenir.
- Tam doğrulama: sonucun dayandığı iddialar ve şaşırtıcı iddialar. Diğer satırlardan örneklem alınır. Örneklemde yaklaşık onda birden fazlası hatalı çıkarsa o üreticinin defterinin tamamı kontrol edilir.
- Doğrulayıcı defterden çalışır: önce gösterilen kaynağı kontrol eder, yalnızca en kritik ya da şüpheli iddialar için bağımsız arama yapar. Doğrulayıcının kontrol noktası satır başına 2 çağrıdır; doğrulayıcı başına en çok 20 satır, satır çoksa doğrulayıcı ekle. Satırları kaynağa göre grupla: aynı sayfa bir kez açılır.
- Araç sayısı doğrulama kapsamını daraltma gerekçesi değildir. Tam doğrulanması gereken satırlar bitmeden rapor teslim edilmez; kalan satırlar için ek doğrulayıcı (sonnet) aç, pahalı ana modelle tek tek kontrol etme.
- Linkler ajanla değil tek betikle toplu kontrol edilir.
- Sayısal sonuç ve backtest doğrulaması: betiğin bağımsız yeniden çalıştırılması, örneklem dışı dönem, işlem maliyeti, çoklu test düzeltmesi. Geçemeyen sinyal “kullanılamaz” diye raporlanır.
- Çift doğrulama (yeniden üretim ve çürütme) yalnızca kullanıcının para yatıracağı, başvuracağı ya da sağlık kararı vereceği somut öneriler için ve ilk elemeden geçtikten sonra.
- “Tartışın” = tek eleştirmen turu: bir eleştirmen taslağın en zayıf noktalarına itiraz eder, sen karara bağlarsın. Çok turlu tartışma yalnızca gerçekten ihtilaflı sorularda ve L'de.
- Düzeltici ajan açma: doğrulayıcı teslim dosyasını yerinde düzeltir ya da sen sentezde düzeltirsin.
- Rapora doğrulama kapsamını yaz: kaç iddia kontrol edildi, kaçı düzeltildi, neler açık kaldı.

## 6. Teslim

- **S:** yanıt sohbette. Dosya yalnızca kullanıcı isterse ya da metin uzunsa. “Ne yapmalıyım” bölümü yalnızca soru bir karar ya da uygulama sorusuysa.
- **M ve L: tek ana rapor**, `raporlar/YYYY-AA-GG_konu/RAPOR.md`. Sıra: kısa yanıt (en çok 6 satır), ne yapmalıyım (somut adımlar), gerekçe ve kanıt, emin olunmayanlar ve doğrulama kapsamı, kaynaklar, devam notu.
- Gövde uzunluğu: M ≤ 2.500, L ≤ 5.000 kelime; tablolar, kaynaklar ve ekler sayılmaz. Kararın dayandığı tablo (sinyal, eyalet, ürün tablosu) ana raporda durur. Kapsam sığmıyorsa ayrıntı ek dosyalara gider, ana rapor kısa kalır.
- Çıktının nerede kullanılacağı belliyse (sunum, gönderi, başvuru) biçimi ona göre seç.
- Sade Türkçe. Terim ilk geçtiği yerde açıklanır. Kullanıcı telefonda okuyor.
- Ana raporu sohbette `SendUserFile` ile gönder. Yalnızca dosya yolunu yazıp bırakma.
- Ham ajan çıktıları `ek/` klasöründe durur. Kullanıcı istemedikçe ajan başına ayrı rapor üretme.
- Kullanıcının bir varsayımı yanlışsa raporda açıkça düzelt.
- Son satırda maliyet özeti: seviye, ajan sayısı (modele göre), dalga sayısı, kontrol noktasını geçen ajan ve nedeni, aşılan sınır varsa nedeni.
- Ekonomi sürece uygulanır, teslimata değil: en düşük seviyede de yanıt eksiksiz, düzenli ve sunulabilir olur.

## 7. Oturum

- Devam notu raporun sonunda 5 satırdır (ne bulundu, hangi dosyalar); yeni bir oturum yalnızca o dosyayı okuyarak sürdürebilsin.
- M ve L teslim mesajı şu cümleyle biter: “Bir saatten uzun ara verirsen ya da konu değişirse yeni oturum aç; devam notu raporun sonunda.”
- Bağlam çok büyükken (yaklaşık 300 bin token üstü) ilgisiz yeni bir iş istenirse isteneni yap ve aynı cümleyi ekle.
