# Bağımsız doğrulama: r1_psikoloji.md (nezaket, statü, zorbalıkta hedef seçimi)

Doğrulayıcı: bağımsız doğrulama ajanı (çürütme amaçlı) · Tarih: 03.11.2026
Doğrulanan dosya: `/home/user/Xxxx/raporlar/2026-11-03_dishekimligi_isyeri/ajanlar/r1_psikoloji.md` (dosya değiştirilmedi)

## Yöntem notu (önemli)

- Bu turda web araması kotası (tüm ajanların paylaştığı 200 arama) baştan dolmuştu. **Hiç WebSearch yapılamadı.**
- Bunun yerine bilinen DOI ve PMID'lerle **birincil kayıtlar doğrudan çekildi**: OpenAlex (özet metni dahil), Crossref (dergi sayı listeleri), PubMed, Hofstede'nin resmi veri dosyası. Bunlar araştırmacının kullandığı kaynaklardan farklıdır.
- Özetlerin çoğu, OpenAlex'in kelime dizininden kelime kelime yeniden kuruldu. İstatistikler (r, d, k, %) özet metninden alındı.
- Tam metne erişilemeyen yerlerde hüküm "DOĞRULANAMADI" olarak verildi. Kendi arka plan bilgim yalnızca "doğrulanmamış not" olarak eklendi.

Hüküm ölçeği: DOĞRU / KISMEN / YANLIŞ / DOĞRULANAMADI.

---

## 1. Nielsen, Glasø, Einarsen 2017: kişilik ve tacize maruz kalma meta-analizi

- **İddia:** PAID 104:195-206; 36 örneklem, N=13.896; nevrotiklik r=0,25, uyumluluk r=-0,17, dışadönüklük ve sorumluluk r=-0,10, açıklık r=0,04.
- **Hüküm: DOĞRU.**
- **Doğrusu:** Künye doğru (çevrim içi Ağustos 2016, baskı Ocak 2017). Özet: 36 bağımsız örneklem, 13.896 katılımcı, 101 etki büyüklüğü (Ocak 2015'e kadar). Nevrotiklik r=0,25 (k=32); dışadönüklük r=-0,10 (k=17); uyumluluk r=-0,17 (k=19); sorumluluk r=-0,10 (k=22); açıklık r=0,04 (k=11, ilişkisiz). Ölçüm yöntemi, taciz türü ve ülke bazı ilişkileri düzenliyor. Abartı yok: araştırmacı nedensellik kurulamayacağını doğru belirtmiş.
- **Kaynak:** https://api.openalex.org/works/doi:10.1016/j.paid.2016.08.015 ; https://api.crossref.org/works/10.1016/j.paid.2016.08.015

## 2. Dhanani, Main, Pueschel 2020: kurban hızlandırma meta-analizi

- **İddia:** JOB 41(8):706-721; tutarlı kurban özelliği yalnızca olumsuz duygulanım; durumsal etkenler daha fazla varyans açıklıyor.
- **Hüküm: DOĞRU.**
- **Doğrusu:** Başlık "Do you only have yourself to blame? A meta-analytic test of the victim precipitation model"; DOI 10.1002/job.2413; 41(8):706-721. Özet: yalnızca olumsuz duygulanım "tutarlı biçimde" yaşanan kötü muameleyle ilişkili. Durumsal öncüller kurban eğilimlerinden "daha fazla varyans açıkladı". Kurban hızlandırma modeline destek "görece zayıf". Küçük not: araştırmacının parantezde verdiği durumsal etken örnekleri (iş ortamı, liderlik, rol çatışması) özette sayılmıyor; bunlar araştırmacının örnekleri. Aynı sayıda Hershcovis, Cortina, Robinson'un "Context matters" (bağlam önemlidir) giriş yazısı da var (s. 699-705).
- **Kaynak:** https://api.crossref.org/journals/1099-1379/works?filter=from-print-pub-date:2020-10,until-print-pub-date:2020-10 ; https://api.openalex.org/works/doi:10.1002/job.2413

## 3. Aquino & Lamertz 2004: dört rolün adları

- **İddia:** JAP 89(6):1023-1034; rollerin adları ("baskın fail, tepkisel fail, itaatkâr kurban, kışkırtıcı kurban") birincil metinden doğrulanamadı.
- **Hüküm: DOĞRULANAMADI** (künye ve model DOĞRU).
- **Doğrusu:** Künye doğru (PMID 15584839). Özet: çalışanlar "dört arketip sosyal rolden" birinde; ikili etkileşimler geçici ya da kurumsallaşmış mağduriyete dönüşebilir; bu, güç farkı, örgüt kültürü ve sosyal sermayeye erişimle bağlantılı. Özet rollerin adını vermiyor. Açık erişimli tam metin yok. Doğrulanmamış not: kendi arka plan bilgim de aynı dört adı (dominating perpetrator, reactive perpetrator, submissive victim, provocative victim) içeriyor, ama bu kez birincil metinle teyit edilemedi. Araştırmacının "doğrulanamadı" uyarısı yerinde; rapor bu adları kesin bilgi gibi sunmamalı.
- **Kaynak:** https://api.openalex.org/works/doi:10.1037/0021-9010.89.6.1023 ; https://pubmed.ncbi.nlm.nih.gov/15584839

## 4. Judge, Livingston, Hurst 2012: uyumluluk ve gelir

- **İddia:** JPSP 102(2):390-407; uyumluluk-gelir ilişkisi erkeklerde güçlü negatif, kadınlarda zayıf ya da yok; "%18 / 9.770 $" basından.
- **Hüküm: KISMEN.**
- **Doğrusu:** Künye doğru (çevrim içi 28.11.2011, baskı 2012). Dört çalışma var: Çalışma 1-3 ilişkiyi gösteriyor ve tekrarlıyor (Çalışma 2 öbür Büyük Beş özelliklerini kontrol ediyor); Çalışma 4 deneysel ve "uyumlu erkeklere karşı tepki" (backlash) açıklamasını destekliyor. Özet, uyumluluk-gelir ilişkisinin "kadınlara göre erkeklerde anlamlı biçimde daha negatif" olduğunu söylüyor. Kadınlarda farkın **daha küçük** olduğunu söylüyor; **"yok"** demiyor. Bu nedenle "zayıf ya da yok" ifadesinin "yok" kısmı desteklenmiyor. "%18 / 9.770 $" rakamı bu doğrulamada ikinci bağımsız bir kaynakla teyit edilemedi (arama kotası). Doğrulanmamış not: bu rakamlar yaygın olarak Notre Dame basın bültenine atfedilir; aynı bültende kadınlar için yaklaşık %5 fark verilir. Raporda kullanılacaksa "basın bülteni rakamı" diye etiketlenmeli.
- **Kaynak:** https://api.openalex.org/works/doi:10.1037/a0026021

## 5. Williams & Tiedens 2016: kadınların açık ve örtük baskınlığına ceza

- **İddia:** Psych Bull 142(2):165-197; çalışma sayısı 63 ya da 71; kadınların baskın davranışı yetkinliği düşürmedi, beğeniyi düşürdü; örtük baskınlık (geniş duruş, sakin ses, göz teması) cezalandırılmadı.
- **Hüküm: KISMEN.** Künye doğru; ama bulgunun özeti eksik ve öneri kısmında genişletilmiş.
- **Doğrusu:**
  - Künye: "The subtle suspension of backlash: A meta-analysis of penalties for women's implicit and explicit dominance behavior", DOI 10.1037/bul0000039, 142(2):165-197.
  - **"63" toplam çalışma sayısı değil.** 63, beğeni analizine giren etki sayısıdır (k=63). Özet toplam çalışma sayısını vermiyor. "63 ya da 71" çelişkisi büyük olasılıkla bu karışıklıktan doğuyor. 71 rakamı doğrulanamadı.
  - Bulgular **erkeklere göre** ek cezayı ölçüyor: baskınlık kadınların beğenilirliğini erkeklere göre düşürüyor (küçük etki, d=-0,19, k=63).
  - **Araştırmacının atladığı bulgu:** daha sonraki sonuçlarda ceza daha büyük. İşe alınabilirlik d=-0,58 (k=20).
  - Yetkinlik algısı: baskınlığın kadın ve erkeğin algılanan yetkinliğine etkisi farklı değil (d=0,02, k=31). Yani "yetkinliği düşürmedi" ifadesi kesin değil; doğru ifade "yetkinlik algısında kadın-erkek farkı yok".
  - Açık baskınlık (ör. doğrudan talep) kadınların beğenilirliğini düşürdü (d=-0,28). Örtük baskınlık (özetteki tek örnek: göz teması) düşürmedi (d=0,03). Bu bulgu **beğeni** için; işe alınabilirlik için örtük/açık ayrımı özette verilmiyor.
  - "Geniş beden duruşu, sakin ses" özette örnek olarak geçmiyor. Raporun 3.0 bölümündeki "yavaş konuşma, cümleyi soru tonuyla bitirmeme, hazırlıklı gelme" ise meta-analizin test ettiği kategoriler değil; araştırmacının çıkarımı. Öyle etiketlenmeli.
- **Kaynak:** https://api.crossref.org/journals/0033-2909/works?filter=from-pub-date:2015-09,until-pub-date:2016-02 ; https://api.openalex.org/works/doi:10.1037/bul0000039

## 6. Ames & Wazlawek 2014: "çizgiyi aşma yanılgısı" ve "stratejik gücenme"

- **İddia:** PSPB 40(6):775-790; line-crossing illusion ve strategic umbrage; yanılgıya düşenler daha kötü anlaşmayı kabul etti; örneklem "çoğu MBA + 500 ABD'li yetişkin".
- **Hüküm: KISMEN.** Dergi, künye ve kavramlar DOĞRU; sonuç yönü ve örneklem ayrıntısı DOĞRULANAMADI.
- **Doğrusu:** "Pushing in the Dark", PSPB 40(6):775-790, çevrim içi 28.02.2014. Dergi Psychological Science değil, PSPB (araştırmacı doğru). Dört çalışma. Çalışma 1: düşük ve aşırı atılgan olanlar kendilerini "uygun atılgan" görüyor. Karşı tarafça uygun atılgan görülen birçok kişi, yanlışlıkla aşırı atılgan göründüğünü sanıyor: "line crossing illusion". Yazarlar "orkestre edilmiş rahatsızlık gösterileri"nin (strategic umbrage) kısmen sorumlu olabileceğini "tahmin ettiklerini" yazıyor (Çalışma 2 gerçek müzakerelerde yaygın olduğunu, Çalışma 3 yanılgıyla bağını gösteriyor). Çalışma 4: yanılgı çok turlu müzakerede "sonuçları yordadı". **Özet, sonucun yönünü ("daha kötü anlaşma", "taviz") söylemiyor.** Bu ayrıntı tam metinden teyit edilemedi. "Çoğu MBA + 500 ABD'li yetişkin" örneklem bilgisi özette yok; doğrulanamadı.
- **Kaynak:** https://api.openalex.org/works/doi:10.1177/0146167214525474

## 7. Brooks, Dai, Schweitzer: "I'm sorry about the rain"

- **İddia:** SPPS 5(4), 2014 (çevrim içi 2013); saha çalışmasında %47'ye karşı %9; BPS saha çalışmasını ciddi kusurlu buldu; aynı kişiye sık tekrarlanınca etki azalıyor.
- **Hüküm: KISMEN.**
- **Doğrusu:** Çevrim içi yayın 26.09.2013; baskı SPPS 5(4):467-474, 2014. Atıfta "2014" doğru; sayfa eklenmeli. Özet: dört çalışmada gereksiz özür, özür dileyene güveni artırdı; etkiye empatik ilgi aracılık etti. Saha çalışması (BPS Research Digest'e göre): yağmurlu bir günde tren istasyonunda bir erkek oyuncu 65 yabancıdan telefon istedi; özürle %47, özürsüz %9. BPS yazısı saha çalışmasını gerçekten "seriously flawed" (ciddi kusurlu) diye niteliyor ve gerekçe olarak "uygun bir kontrol koşulu olmadığını" yazıyor: etkinin özre mi, herhangi bir açılış cümlesine mi bağlı olduğu bilinmiyor. Yani araştırmacının "ciddi kusurlu" ifadesi abartı değil. **"Aynı kişiye sık tekrarlanınca etki azalıyor" iddiası ne özette ne BPS yazısında var; DOĞRULANAMADI.** Rakamlar yalnızca araştırmacının kullandığı BPS kaynağında görüldü; farklı ikinci bir kaynakla teyit edilemedi.
- **Kaynak:** https://api.openalex.org/works/doi:10.1177/1948550613506122 ; https://bps.org.uk/research-digest/want-people-trust-you-try-apologising-rain (yalnızca abartı kontrolü için)

## 8. Çolak ve ark. 2026: Türkiye'de diş hekimliği öğrencilerinde zorbalık

- **İddia:** EJDE, doi:10.1111/eje.70216; 414 öğrenci; %99,3 en az bir zorbalıkla ilişkili davranış (geniş tanım).
- **Hüküm: DOĞRU.**
- **Doğrusu:** Yazarlar: Sefa Çolak, Aras Erdil, Göksal Keldal, İremnur Olgun Çolak, Aslı Başal, Beyza Dal. Çevrim içi 14.06.2026; cilt/sayfa henüz yok. İki merkezli kesitsel anket; Türkiye'de iki üniversiteden 414 dördüncü ve beşinci sınıf öğrenci. 30 maddelik zorbalık anketi (AbuAlula ve ark.'dan uyarlanmış) ve DASS-21. %99,3 en az bir zorbalıkla ilişkili davranış bildirdi. En az hafif düzey belirti: depresyon %70,3, kaygı %82,1, stres %57,7. Zorbalık puanı yaş, cinsiyet, sınıf ve üniversite düzeltmesinden sonra da üç ölçekle bağımsız ilişkili (p<0,001). Yazarların kendi uyarısı: geniş tanım nedeniyle bu oran "süreğen, ağır ya da tekrarlayan" zorbalık yaygınlığı olarak okunmamalı. Araştırmacı bu uyarıyı doğru aktarmış. Özet zorbalığın kaynağını (hoca/akran/hasta) ayırmıyor.
- **Kaynak:** https://api.openalex.org/works/doi:10.1111/eje.70216

## 9. Fnais ve ark. 2014: tıp eğitiminde taciz ve ayrımcılık

- **İddia:** Academic Medicine; %59,4 (%95 GA 52,0-66,7); en sık kaynak kıdemli hekimler; meta-analizde 51, derlemede 59 çalışma.
- **Hüküm: DOĞRU.**
- **Doğrusu:** Academic Medicine 89(5):817-827, 2014 (çevrim içi 25.03.2014). Derlemede 59 çalışma (57 kesitsel, 2 kohort); meta-analizde 51. Havuzlanmış yaygınlık %59,4 (%95 GA %52,0-%66,7). En sık tür sözlü taciz: %63,0 (%95 GA 54,8-71,2). En sık kaynak kıdemli/uzman hekimler ("consultants", %34,4). **Araştırmacının atladığı ve senaryolar için önemli bulgu:** ikinci sık kaynak hastalar ve hasta yakınları (%21,9). Yazarlar yaygınlığın zamanla azalmadığını belirtiyor.
- **Kaynak:** https://api.openalex.org/works/pmid:24667512

## 10. Rowland ve ark. 2010: diş hekimliği fakültelerinde yıldırma

- **İddia:** International Dental Journal; beş ülkede yedi fakülte; %34,6 kötü muamele.
- **Hüküm: DOĞRU** (bağlam uyarısıyla).
- **Doğrusu:** Int Dent J 60(2):106-112, Nisan 2010, PMID 20476716. Yedi fakülte, beş ülke (Romanya, Güney Afrika, Avustralya, ABD, Malezya; üç fakülte Malezya'da). Birinci sınıf öğrenciler, en az altı ay sonra, **2005-06'da** anket. %34,6 eğitmenlerden yıldırma/kötü muamele bildirdi; %17 akranlardan zorbalık. Eğitmen kaynaklı oran fakülteden fakülteye anlamlı fark gösterdi. Uyarı: veri 20 yıllık ve birinci sınıf öğrencilerden; Türkiye yok. Okul farkı bulgusu, "kurum seçimi önemli" önerisini destekliyor.
- **Kaynak:** https://pubmed.ncbi.nlm.nih.gov/20476716/ ; https://api.crossref.org/journals/0020-6539/works?filter=from-pub-date:2010-01,until-pub-date:2010-12

## 11. Herrmann, Thöni, Gächter 2008: antisosyal ceza ve İstanbul

- **İddia:** Science 319:1362-1367; 16 havuzda antisosyal ceza; zayıf işbirliği normu ve zayıf hukuk düzeniyle ilişkili; İstanbul'a özgü düzey birincil metinden doğrulanmadı.
- **Hüküm: DOĞRULANAMADI** (İstanbul ayrıntısı). Genel bulgu DOĞRU.
- **Doğrusu:** Science 319(5868):1362-1367, 06.03.2008. Özet: 16 karşılaştırılabilir katılımcı havuzunda kamu malı deneyleri; bazı havuzlar yüksek katkı verenleri düşük katkı verenler kadar cezalandırdı; bazı havuzlarda antisosyal ceza, cezanın işbirliğini artıran etkisini ortadan kaldırdı; zayıf sivil işbirliği normları ve zayıf hukuk düzeni anlamlı yordayıcılar. İstanbul'un havuzlardan biri olduğu ve oradaki düzey bu doğrulamada tam metinden teyit edilemedi. **Ek not:** araştırmacının verdiği umass.edu PDF bağlantısı bugün 404 hatası veriyor; açık kopya olarak St. Gallen deposu listeleniyor. Katılımcılar üniversite öğrencisi; işyerine genelleme zayıf (araştırmacı da öyle demiş).
- **Kaynak:** https://api.openalex.org/works/doi:10.1126/science.1153808 ; https://www.alexandria.unisg.ch/handle/20.500.14171/78586

## 12. Hofstede güç mesafesi: Türkiye 66, Kanada 39

- **İddia:** Türkiye 66, Kanada 39 (ikincil ders kitabı tablosundan).
- **Hüküm: DOĞRU** (bir ek ayrıntıyla).
- **Doğrusu:** Hofstede'nin resmi veri dosyasında (6-dimensions-for-website-2015-08-16.csv): Türkiye PDI 66, Kanada PDI 39. **Ek ayrıntı:** aynı dosyada "Canada French" (Fransızca konuşan Kanada) ayrı satır ve PDI **54**. Kullanıcı Quebec'te çalışırsa fark küçülür. Veri temelde 1960-70'lerin IBM anketlerine dayanır; ülke ortalamasıdır, bireyi ya da tek bir kliniği tanımlamaz.
- **Kaynak:** https://geerthofstede.com/wp-content/uploads/2016/08/6-dimensions-for-website-2015-08-16.csv ; https://geerthofstede.com/research-and-vsm/dimension-data-matrix/

## 13. Tepper, Moss, Duffy 2011: istismarcı yönetimin yordayıcıları

- **İddia:** AMJ 54(2):279-294; derin düzey farklılık, ilişki çatışması ve düşük performans algısı üzerinden istismarcı yönetim.
- **Hüküm: DOĞRU.**
- **Doğrusu:** Künye doğru (DOI 10.5465/amj.2011.60263085). Ahlaki dışlama kuramı; amir-ast ikilileri, iki zaman noktası, yol analizi. Amirin algıladığı ilişki çatışması ve ast performansı, algılanan derin düzey farklılık ile istismarcı yönetim arasında aracı. Ek ayrıntı: ilişki çatışması yolu, amir astı **düşük performanslı** gördüğünde işliyor (koşullu aracılık). Yazarlar kurban hızlandırma kuramına da dayanıyor.
- **Kaynak:** https://api.openalex.org/works/doi:10.5465/amj.2011.60263085

## 14. Maner & Mead 2010: güç istikrarsızken baskınlık güdülü lider

- **İddia:** JPSP 99(3):482-497; beş deney; gücü istikrarsız, baskınlık güdüsü yüksek liderler bilgiyi sakladı, yetenekli üyeyi dışladı, etkisini engelledi; dış rakip varken kayboldu; replikasyon bulunamadı.
- **Hüküm: DOĞRU.**
- **Doğrusu:** Künye ve beş deney doğru. Liderler çoğu durumda grup çıkarına davrandı; kendi çıkarını, **hem** güç istikrarsız **hem** baskınlık güdüsü yüksekken öne koydu. Davranışlar: değerli bilgiyi saklama, çok yetenekli üyeyi dışlama, yetkin üyenin etkisini engelleme. Dış grupla rekabette bu davranış kayboldu. Bağımsız replikasyon için arama yapılamadı; "replikasyon bulunamadı" notu korunmalı. Doğrulanmamış not: aynı laboratuvardan kavramsal uzantılar (ör. Case & Maner 2014) bildiğim kadarıyla var; bunlar bağımsız tekrar sayılmaz. Laboratuvar deneyleri, atanmış liderler; kliniğe genelleme bir çıkarımdır.
- **Kaynak:** https://api.openalex.org/works/doi:10.1037/a0018559

## 15. Nielsen & Knardahl 2015: iki yıllık izlem

- **İddia:** Work & Stress 29(2):128-149; n=3.066; iki yıllık izlem; kişilik hem öncül hem sonuç.
- **Hüküm: DOĞRU.**
- **Doğrusu:** 3.066 Norveçli çalışan, iki ölçüm arası iki yıl. Doğrudan analizde nevrotiklik sonraki zorbalığı yordadı. Rol çatışması ve rol belirsizliği düzeltilince tek anlamlı yordayıcı sorumluluk oldu. Ters yönde: başlangıçtaki zorbalık, izlemdeki uyumluluk, sorumluluk ve açıklıkla ilişkili. Küçük düzeltme: araştırmacı "zorbalık sonraki kişilik puanlarını **etkiledi**" diyor; özet "ilişkiliydi" diyor. Nedensel dil yumuşatılmalı.
- **Kaynak:** https://api.openalex.org/works/doi:10.1080/02678373.2015.1032383

## 16. Glasø ve ark. 2007: "435 sağlık çalışanı" atfı

- **İddia (bulgu 9):** "435 sağlık çalışanında kişilik, hedefleri hedef olmayanlardan kolayca ayırt etmedi (Glasø ve ark. 2007, Scand J Psychol 48(4):313-319)". Verilen bağlantı: econtent.hogrefe.com/doi/10.1027/1016-9040.14.3.231.
- **Hüküm: YANLIŞ (atıf karışıklığı).**
- **Doğrusu:** İki ayrı çalışma birleştirilmiş.
  - **435 sağlık çalışanı** bulgusu Glasø 2007'ye değil, **Lind, Glasø, Pallesen, Einarsen 2009, European Psychologist 14(3):231-237**'ye ait (araştırmacının verdiği DOI budur). 435 sağlık çalışanı, 42 hedef. Hedefler beş boyuttan yalnızca ikisinde farklı: **sorumlulukta daha yüksek, uyumlulukta daha düşük.** Alt küme yok; yazarlar farkları "minimal" sayıyor; "kişilik hedefleri kolayca ayırt etmiyor".
  - **Glasø, Matthiesen, Nielsen, Einarsen 2007, Scand J Psychol 48(4):313-319** ise 144 kişilik (72 kurban, 72 eşleştirilmiş karşılaştırma) ayrı bir çalışma. Kurbanlar beş boyuttan **dördünde** farklı: duygusal olarak daha dengesiz, daha az uyumlu, daha az sorumlu, daha az dışadönük. Kümeleme analizinde kurbanların yaklaşık %64'ü kurban olmayanlardan farklı değil. Sonuç: "genel bir kurban kişilik profili yok".
  - İki çalışmada da hedefler **daha az uyumlu** çıkıyor. Bu, "nezaket taciz çekmez" ana yorumunu destekliyor; ama atıf düzeltilmeli.
- **Kaynak:** https://api.openalex.org/works/doi:10.1027/1016-9040.14.3.231 ; https://api.openalex.org/works/doi:10.1111/j.1467-9450.2007.00554.x

## 17. Coyne, Seigne, Randall 2000: "n=60, daha kaygılı ve itaatkâr"

- **İddia (bulgu 9):** Küçük eski bir çalışma (n=60) hedefleri daha kaygılı ve itaatkâr buldu.
- **Hüküm: KISMEN.**
- **Doğrusu:** EJWOP 9(3):335-349. 60 kurban ve işe ve kişisel ölçütlere göre eşleştirilmiş, zorbalığa uğramamış bir karşılaştırma grubu (sayı büyük olasılıkla 60; toplam yaklaşık 120). İrlanda'da iki büyük kurum. Kurbanlar "daha az bağımsız, daha az dışadönük, daha az dengeli ve daha sorumlu" bulundu. "İtaatkâr" kelimesi "daha az bağımsız" bulgusunun serbest çevirisi; "daha sorumlu" bulgusu atlanmış. "n=60" toplam örneklemi küçük gösteriyor.
- **Kaynak:** https://api.openalex.org/works/doi:10.1080/135943200417957

## Ek kontrol (sayıma katılmadı)

- **Pallesen ve ark. 2017, Frontiers in Psychology 8:1045:** künye doğru. 242 öğrenci gözlemciyle vinyet deneyi: hedefler en nevrotik ve en az dışadönük, zorbalar en az uyumlu diye puanlandı. Araştırmacının "gözlemciler bir kurban kalıbı taşıyor" özeti doğru. https://api.openalex.org/works/doi:10.3389/fpsyg.2017.01045
- **Aycan ve ark. 2013:** künye JIBS 44(9):962-969. "6 ülke, 1.272 çalışan" rakamı özet olmadığı için doğrulanamadı. https://api.openalex.org/works/doi:10.1057/jibs.2013.48

---

## Özet tablo

| # | İddia | Hüküm |
|---|---|---|
| 1 | Nielsen ve ark. 2017 meta-analiz rakamları | DOĞRU |
| 2 | Dhanani ve ark. 2020: yalnızca olumsuz duygulanım; durum daha çok açıklıyor | DOĞRU |
| 3 | Aquino & Lamertz 2004 rol adları | DOĞRULANAMADI |
| 4 | Judge ve ark. 2012: kadınlarda "zayıf ya da yok"; %18/9.770 $ | KISMEN |
| 5 | Williams & Tiedens 2016: 63/71; yetkinlik; örtük baskınlık | KISMEN |
| 6 | Ames & Wazlawek 2014: yanılgı, "daha kötü anlaşma", örneklem | KISMEN |
| 7 | Brooks ve ark.: yıl, %47/%9, tekrarda azalma | KISMEN |
| 8 | Çolak ve ark. 2026: 414 öğrenci, %99,3 | DOĞRU |
| 9 | Fnais ve ark. 2014: %59,4, 51/59 çalışma | DOĞRU |
| 10 | Rowland ve ark. 2010: %34,6 | DOĞRU |
| 11 | Herrmann ve ark. 2008: İstanbul ayrıntısı | DOĞRULANAMADI |
| 12 | Hofstede: Türkiye 66, Kanada 39 | DOĞRU |
| 13 | Tepper ve ark. 2011 | DOĞRU |
| 14 | Maner & Mead 2010 | DOĞRU |
| 15 | Nielsen & Knardahl 2015 | DOĞRU |
| 16 | "435 sağlık çalışanı" = Glasø 2007 | YANLIŞ |
| 17 | Coyne ve ark. 2000: n=60, "kaygılı ve itaatkâr" | KISMEN |

Toplam: 9 DOĞRU, 5 KISMEN, 1 YANLIŞ, 2 DOĞRULANAMADI.

Uydurma atıf bulunmadı. Kontrol edilen tüm künyeler (yazar, yıl, dergi, cilt, sayfa) gerçek kayıtlarla eşleşiyor. Tek yanlış, iki gerçek çalışmanın birbirine karıştırılması.

---

## Raporu okuyanların bilmesi gereken kritik düzeltmeler

1. **Bulgu 9'daki atıf yanlış.** "435 sağlık çalışanı" çalışması Glasø ve ark. 2007 değil, Lind, Glasø, Pallesen, Einarsen 2009 (European Psychologist 14(3):231-237). Bu çalışmada hedefler uyumlulukta **daha düşük**, sorumlulukta **daha yüksek**. Glasø 2007 ise 144 kişilik ayrı bir çalışma; kurbanlar dört boyutta farklı ama %64'ü profil olarak kurban olmayanlardan ayırt edilemiyor. Ana sonuç değişmiyor: "nazik kişi daha çok hedef olur" diye bir kanıt yok.

2. **Williams & Tiedens 2016 eksik aktarılmış.** Kadınların baskınlığı için asıl büyük ceza beğenide değil, **işe alınabilirlikte** (d=-0,58; beğenide d=-0,19). Bulgular erkeklere göre ek cezayı ölçüyor. "Örtük baskınlık cezalandırılmadı" bulgusu **beğeni** içindir ve özetteki tek örnek **göz teması**dır. "Yavaş konuşma, soru tonu kullanmama, hazırlık" önerileri bu meta-analizden değil, araştırmacının çıkarımından geliyor. "63" toplam çalışma sayısı değil, bir analizdeki etki sayısı (k).

3. **Ames & Wazlawek 2014'te sonucun yönü teyit edilmedi.** Özet, yanılgının çok turlu müzakerede "sonuçları yordadığını" söylüyor; "daha kötü anlaşmayı kabul ettiler" ifadesi özette yok. Öneri ("ilk net cümleden sonra geri çekilme") makul, ama "kanıtlanmış zarar" gibi sunulmamalı.

4. **"Gereksiz özrün etkisi tekrarlanınca azalır" iddiası kaynaksız.** Ne makale özetinde ne BPS yazısında var. Çıkarılmalı ya da "uzman görüşü/çıkarım" diye etiketlenmeli. Saha çalışmasının (%47'ye karşı %9) kontrol koşulu olmadığı için kusurlu olduğu doğru.

5. **Judge ve ark. 2012: kadınlarda etki "yok" değil, "daha küçük".** Basın rakamı (%18 / 9.770 $) birincil makalede doğrulanmadı; kullanılacaksa "basın bülteni" diye etiketlenmeli.

6. **Fnais ve ark. 2014'ün ikinci sık kaynağı hastalar ve yakınları (%21,9).** Bu, kötü muamelenin yalnızca hocadan gelmediğini gösterir. Aile kliniği ve Kanada senaryolarında hastadan gelen kötü davranış için de plan gerekir.

7. **Kanada için Hofstede tek sayı değil.** İngilizce konuşan Kanada 39, Fransızca konuşan Kanada 54. Kullanıcı Quebec'te çalışırsa güç mesafesi farkı küçülür. Veri eski ve ülke ortalamasıdır.

8. **Rowland ve ark. 2010 verisi 2005-06 yılından ve birinci sınıf öğrencilerinden.** Güncel Türkiye verisi için Çolak ve ark. 2026 (çevrim içi 14.06.2026) kullanılmalı; ama %99,3 "en az bir davranış" oranıdır, ağır zorbalık yaygınlığı değildir. Rowland çalışmasında eğitmen kaynaklı kötü muamelenin fakülteler arasında anlamlı fark göstermesi, "kurum ve danışman seçimi en büyük kaldıraç" önerisini destekliyor.

9. **Nedensel dil yumuşatılmalı.** Nielsen & Knardahl 2015 "zorbalık kişiliği etkiledi" demiyor, "ilişkili" diyor. Tepper ve ark. 2011 ve Maner & Mead 2010 bulgularının kliniğe ve fakülteye aktarımı çıkarımdır.

10. **Herrmann ve ark. 2008 için verilen umass.edu bağlantısı artık çalışmıyor (404).** İstanbul'a özgü bir sonuç rapordan çıkarılmalı ya da "doğrulanmadı" olarak kalmalı.

11. **Yöntem sınırı.** Bu doğrulamada web araması yapılamadı (kota dolu). Kontroller birincil kayıtlar (OpenAlex, Crossref, PubMed, Hofstede veri dosyası) üzerinden yapıldı. Bağımsız replikasyon taraması (Maner & Mead, Brooks ve ark., Grant) yapılamadı; bu boşluklar raporda "replikasyon bulunamadı" olarak kalmalı, "replikasyon yok" diye yazılmamalı.
