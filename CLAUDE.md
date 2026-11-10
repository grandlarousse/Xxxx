# Araştırma protokolü (kota verimliliği)

Bu depo kullanıcının araştırma çalışma alanıdır. Kullanıcının haftalık kullanım kotası sınırlıdır ve çoğu hafta dolmadan bitiyor. Bu yüzden iki kural aynı anda geçerlidir:

1. **Kalite düşmez.** Yanıtın doğruluğu, kapsamı ve kullanılabilirliği pazarlık konusu değildir.
2. **Token maliyeti her zaman bir kısıttır.** Ultracode ya da yüksek efor ayarı açık olsa bile aşağıdaki sınırlar geçerlidir. İş akışı (Workflow) kuracaksan bu sınırların içinde kur.

Tasarruf sürecin şişkinliğinden yapılır, sonucun kalitesinden değil: daha az ama iyi tanımlanmış ajan, kısa araç döngüleri, işe uygun model, hedefli doğrulama, tek ve okunur rapor.

## 1. Önce seviye seç

Hiçbir ajan başlatmadan önce işi bir seviyeye yerleştir ve ilk mesajında tek satırla bildir. Örnek: `Seviye M · 5 araştırmacı (sonnet) + 2 doğrulayıcı (opus) · 2 dalga`.

| Seviye | Ne zaman | Alt ajan | Ajan başına araç çağrısı | Doğrulama |
|---|---|---|---|---|
| **S** | Tek soru, tek alan: tanım, olgu, kısa açıklama, küçük içerik işi | 0 (gerekirse 1–2) | ana ajan toplam ≤ 15 | Ana ajan kritik iddiaları kaynağından kendisi kontrol eder |
| **M** | Çok yönlü araştırma, karşılaştırma, strateji; 3–8 alt soru | 3–6 üretici + 1–2 doğrulayıcı | üretici ≤ 20, doğrulayıcı ≤ 15 | Yük taşıyan iddialar için 1 bağımsız doğrulama turu |
| **L** | Büyük külliyat, çok sayıda öğe (kitap, eyalet, hisse), veri ve backtest | toplam ≤ 18 üretici + ≤ 6 doğrulayıcı; dalga başına ≤ 8 | üretici ≤ 25, doğrulayıcı ≤ 20, kod/veri ajanı ≤ 40 | Huni: ucuz eleme, sonra yalnızca ayakta kalanlara tam doğrulama |

- Kullanıcı mesajında `Seviye: S`, `M` ya da `L` yazıyorsa onu kullan.
- Yazmıyorsa sen seç. Kararsızsan alt seviyeden başla; ilk dalganın sonunda karara etki eden bir eksik kaldıysa yükselt ve bunu söyle.
- L gerektiğini düşünüyorsan ve kullanıcı L demediyse: başlamadan önce tek mesajla planı ver (kaç ajan, hangi model, kaç dalga) ve onay iste.
- Sınırların üstüne yalnızca kullanıcı o mesajda açıkça isterse çık (“sınırsız”, “L+”). O durumda da 2–6. bölümler geçerlidir.
- “İhtiyacın kadar ajan kullan”, “gazı ver”, “full bütçe” = seviyeyi işe göre sen seç, en fazla L. “Kotam az”, “ekonomik” = S kuralları. Bunların hiçbiri teslim edilen raporun özenini düşürmez.
- Çok öğeli işlerde (N kitap, eyalet, hisse) öğeleri 3–5'li gruplar hâlinde dağıt: ajan sayısı yaklaşık N/4. Öğe başına bir ajan açma.

## 2. Model ataması

Model yazılmayan alt ajan oturumun en pahalı modelini devralır. Her `Agent` ve `agent()` çağrısında `model` alanını açıkça yaz:

| İş | Model | Efor |
|---|---|---|
| Arama, sayfa okuma, alıntı ve sayı çıkarma, link toplama, veri indirme, biçimlendirme | `haiku` | low |
| Kaynak değerlendirmesi gerektiren araştırma, metin yazımı, kod ve backtest | `sonnet` | medium |
| Yük taşıyan iddiaların doğrulanması, yöntem denetimi, hakemlik | `opus` | high |
| Plan, sentez, nihai rapor | ana ajan (sen) | — |

Bir alt görev gerçekten zor akıl yürütme istiyorsa (yöntem tasarımı, istatistiksel çıkarım, hukuki yorum) üst modele çıkar ve nedenini tek cümleyle yaz. Varsayılan yön aşağıdır.

## 3. Alt ajan görev tanımı

Her görev tanımında şunlar bulunur:

- **Dar soru.** Tek alt soru. “X hakkında her şeyi araştır” yok.
- **Bildiklerin.** Kendi bilginden aday yanıtları, hipotezleri ve olası kaynakları yaz. Ajan sıfırdan keşfetmez; doğrular ve eksikleri tamamlar.
- **Araç bütçesi.** “En fazla N araç çağrısı; say. N−3'e geldiğinde aramayı bırak, elindekiyle yanıtla, kontrol edemediklerini ‘açık kalanlar’ başlığına yaz.”
- **Durma kuralı.** Art arda 3 arama yeni bilgi getirmediyse dur.
- **Dönüş biçimi.** Şemalı ve kısa: en çok 400 kelime özet ve bir **iddia defteri** (`iddia | kaynak URL | birebir alıntı ya da sayı | güven: yüksek/orta/düşük`). Uzun ham malzeme dosyaya yazılır; sana yalnızca özet ve dosya yolu döner.

## 4. Bağlam ekonomisi

- Arama özeti yetiyorsa sayfayı açma. Açarsan yalnızca ilgili bölümü al.
- Aynı aramayı iki ajan yapmasın: önceki dalganın kaynak listesini sonraki dalgaya ver.
- Sayısal ve tekrarlı işi ajanlara dağıtma. Veriyi bir kez indir, tek betikle hesapla; ajanlar yöntemi denetler ve sonucu yorumlar. Yöntem denetimi hesaptan önce yapılır.
- Ajan çıktılarının tamamını bağlamına okuma. Özetle çalış; ayrıntı gerekince dosyanın ilgili kısmını oku.
- Dalgalar hâlinde ilerle: 1. dalga geniş ve ucuz, sonra boşlukları kendin değerlendir, 2. dalga yalnızca karara etki eden boşluklara. M'de en çok 2, L'de en çok 3 dalga.
- Çalışan bir iş akışını yarıda durdurup baştan başlatma; gerekiyorsa kaldığı yerden sürdür.

## 5. Doğrulama: kısılmaz, hedeflenir

- Doğrulanacaklar: sonucun dayandığı iddialar, şaşırtıcı iddialar, raporda yer alacak her sayı, tarih, alıntı ve link.
- Doğrulayıcı iddia defterinden çalışır: önce gösterilen kaynağı kontrol eder, yalnızca en kritik ya da şüpheli iddialar için bağımsız arama yapar.
- Oran: yaklaşık 3 üreticiye 1 doğrulayıcı. Üretici başına bir doğrulayıcı açma.
- Çift doğrulama (yeniden üretim ve çürütme) yalnızca para, sağlık ya da hukuki sonuç doğuran ve ilk elemeden geçmiş iddialar için.
- “Tartışın” = tek eleştirmen turu: bir eleştirmen taslağın en zayıf noktalarına itiraz eder, sen karara bağlarsın. Çok turlu ya da çok kişilikli tartışma yalnızca gerçekten ihtilaflı sorularda ve L seviyesinde.
- Doğrulanamayan iddia sessizce silinmez; “doğrulanamadı” etiketiyle kalır ya da gerekçesiyle çıkarılır.

## 6. Teslim

- **Tek ana rapor**: `raporlar/YYYY-AA-GG_konu/RAPOR.md`. Sıra: kısa yanıt (en çok 6 satır), ne yapmalıyım (somut adımlar), gerekçe ve kanıt, emin olunmayanlar, kaynaklar.
- Uzunluk: S ≤ 800, M ≤ 2.500, L ≤ 5.000 kelime. Kullanıcı açıkça uzun metin isterse (örneğin kitap özetleri) uzun bölümler ayrı dosyalarda durur, ana rapor yine kısa kalır.
- Sade Türkçe. Terim ilk geçtiği yerde açıklanır. Kullanıcı raporu telefonda okuyor.
- Ana raporu sohbette `SendUserFile` ile gönder. Yalnızca dosya yolunu yazıp bırakma.
- Ham ajan çıktıları `ek/` klasöründe durur. Kullanıcı istemedikçe ajan başına ayrı rapor üretme.
- Son satırda maliyet özeti ver: seviye, ajan sayısı (modele göre), dalga sayısı, aşılan sınır varsa nedeni.
- Ekonomi sürece uygulanır, teslimata değil: en düşük seviyede de rapor eksiksiz, düzenli ve sunulabilir olur.

## 7. Oturum

- Araştırma bittikten sonra kullanıcı ilgisiz yeni bir iş isterse isteneni yap ve sonuna tek cümle ekle: “Bunu yeni oturumda açmak belirgin biçimde daha az kota harcar.”
- Raporun başına 5 satırlık bir devam notu koy (ne bulundu, hangi dosyalar), böylece yeni bir oturum yalnızca o dosyayı okuyarak sürdürebilsin.

## 8. Alt ajansan

Bu dosyayı bir alt ajan olarak okuyorsan: görev tanımındaki araç bütçesi ve dönüş biçimi bağlayıcıdır. Kendi alt ajanını başlatma. Görev dışına çıkma. Uzun metni dosyaya yaz; kısa ve şemalı dön.
