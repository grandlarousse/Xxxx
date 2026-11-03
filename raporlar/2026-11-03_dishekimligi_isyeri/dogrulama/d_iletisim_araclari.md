# Bağımsız doğrulama: r1_iletisim_araclari.md (nazik ama boyun eğmeyen iletişim araç kutusu)

Tarih: 03.11.2026. Doğrulayıcı: bağımsız doğrulama ajanı. Araştırma dosyası değiştirilmedi.

**Yöntem notu.** Bu turda ortak web arama bütçesi (200 WebSearch çağrısı) dolmuştu. İlk üç arama reddedildi. Arama motoru kullanılmadı. Doğrulama, kimliği bilinen kayıtlar doğrudan açılarak yapıldı:
- OpenAlex kayıtları (DOI ile; özet metni dahil),
- Europe PMC REST kayıtları (yalnız tam DOI ile; özet ve O'Donovan tam metni),
- Semantic Scholar kaydı (yalnız Ranehill için; diğerlerinde hız sınırı),
- Resmî Gazete'nin kendi HTML metinleri (2022 ve 2023),
- CCOHS sayfası, Wikipedia ve Carney'nin açıklama PDF'i (metne çevrilip okundu).

Araştırmacı çoğunlukla PubMed, PMC ve Crossref kullanmıştı. Burada ağırlık OpenAlex ve Europe PMC'de. Springer, SAGE, AOM ve JSTOR sayfaları 403 verdi ya da açılmadı. Bu yüzden Ferrari 2019 ve Ashford & Tsui 1991 özetleri tam okunamadı.

**Özet:** 20 iddia incelendi: 15'i istenen liste, 5'i ek kontrol. Sonuç: 10 DOĞRU, 8 KISMEN, 0 YANLIŞ, 2 DOĞRULANAMADI. Ancak iki KISMEN maddenin içinde doğrudan YANLIŞ birer alt iddia var: Okuyama'ya dayandırılan "en çok engelleyen" sıralaması ve Bohns'tan çıkarılan "hayır demenin bedeli abartılır" sonucu. Uydurma atıf **bulunmadı**. Bütün künyeler (yazar, yıl, dergi, cilt, sayfa) tutuyor. Sorunlar künyede değil. Sorun, bazı bulguların **abartılması ya da ters okunması**.

---

## A. Atılganlık ve söz alma eğitimi

### 1. Omura ve ark. 2017 (*Int J Nurs Stud* 76:120-128): az sayıda, heterojen, düşük kaliteli çalışma; hasta sonucuna etki gösterilmemiş; "kanıt zayıf ve tutarsız"
- **Hüküm: KISMEN**
- **Doğrusu:** Künye doğru. Özet bu kez okundu.
  - 11 makale değerlendirildi, 8'i derlemeye alındı (ABD, Avustralya, İrlanda, Tayvan). Tarama aralığı 2001–2016, yalnız İngilizce. "Az sayıda" doğru.
  - Ama derlemenin vardığı sonuç raporun yazdığından **daha olumlu**. Özetteki sonuç cümlesi şu: girişimler "deneyimli anestezistler dışında tüm hedef gruplarda bir ölçüde etkili" bulundu. Bu tek istisna, Raemer RKÇ'sindeki gruptur (madde 4).
  - Davranış değişimi **simülasyonda gözlemci ölçeğiyle** ölçüldü. Bilgi ve tutum ise geçerli ölçeklerle ölçüldü. Yani "davranışa etki gösterilmemiş" demek yanlış. Doğrusu: gerçek klinikte ve uzun vadede gösterilmemiş.
  - Hasta güvenliği sonucu ölçülmemiş. Yazarlar bunu gelecek araştırmaya bırakıyor. "Hasta sonucuna etki gösterilmemiş" doğru.
  - "Heterojen, düşük kaliteli, tutarsız" nitelemeleri özette **yok**. Tam metinde olabilir, ama bu oturumda teyit edilmedi.
  - Etkili bulunan unsurlar: yüz yüze ve çok yöntemli program, lider desteği, takım becerisi eğitimi, havacılıktan uyarlanmış teknikler.
  - Rapordaki "bir derleme zayıf diyor, öbürü kanıta dayalı diyor" çelişkisi bu yüzden abartılı (bkz. madde 2).
- **Kaynak:** https://europepmc.org/article/MED/28964979 ; https://api.openalex.org/works/doi:10.1016/j.ijnurstu.2017.09.001

### 2. Speed, Goldstein, Goldfried 2018 (*Clin Psychol Sci Pract* 25(1):e12216): atılganlık eğitimini "unutulmuş kanıta dayalı tedavi" sayan anlatı derlemesi; eski RKÇ'lere dayanıyor
- **Hüküm: DOĞRU** (RKÇ ayrıntısı doğrulanamadı)
- **Doğrusu:** Başlık birebir doğru: "Assertiveness training: A forgotten evidence-based treatment". Çevrim içi yayın 2017, basılı cilt 25(1), 2018. Anlatı (sistematik olmayan) derleme. Tarihçeyi ve "erken araştırma kanıtını" yeniden ele alıyor. Atılganlık eğitimini "değerli, tanılar arası bir müdahale" sayıyor.
  - Bağlam önemli. Derleme **psikoterapi ve klinik hasta grupları** hakkında, sağlık çalışanları hakkında değil. Bu, raporun "fark örneklemden geliyor" açıklamasını destekliyor.
  - Hangi RKÇ'lere dayandığı özette yok. Bu oturumda doğrulanamadı.
- **Kaynak:** https://api.openalex.org/works/doi:10.1111/cpsp.12216

### 3. Okuyama, Wagner, Bijnen 2014 (*BMC Health Serv Res* 14:61): 26 çalışma / 27 makale; altı etken kategorisi; "eğitim söz almayı iyileştirir"
- **Hüküm: KISMEN** (ana bulgu DOĞRU; rapordaki bir çıkarım YANLIŞ)
- **Doğrusu:**
  - 26 çalışma / 27 makale: DOĞRU.
  - Altı kategori DOĞRU: motivasyon, bağlam, bireysel etkenler, algılanan etki, algılanan güvenlik, taktik ve hedefler. "Yetersiz görünme kaygısı" güvenlik kategorisinde geçiyor. Olgu toplamak ve olumlu niyet göstermek de taktikler arasında var.
  - "Eğitim söz almayı iyileştirir": özet temkinli. Doğru ifade şu: "**bazı çalışmalar** eğitimin söz almayı iyileştirebileceğini gösterdi." Rapordaki 4. bölüm cümlesi ("Okuyama eğitimin söz almayı iyileştirdiğini bildiriyor") bu kaydı düşürmüş.
  - **YANLIŞ alt iddia.** Rapor 2. bölümde "Söz almayı en çok engelleyen şey 'yetersiz görünme' korkusu" diyor. Okuyama etkenleri sıralamıyor. Özetin son cümlesi tersini söylüyor: "etkenlerin göreli önemini araştırmak için daha fazla araştırma gerekiyor." Raemer ve ark. 2016 nitel analizinde en sık beş engel başka: konudan emin olmamak, ekipteki kalıp yargılar, kişiyle tanışıklık, deneyime saygı, beklenen misilleme. "Yetersiz görünme" bu beşin arasında yok.
  - "Doğru kişiyi seçmek": özette "selecting the person who has spoken up" yazıyor. Raporun yorumu ("söz alınacak kişiyi seçmek") makul, ama lafzı belirsiz.
- **Kaynak:** https://api.openalex.org/works/doi:10.1186/1472-6963-14-61 ; Raemer özeti: https://api.openalex.org/works/doi:10.1097/ACM.0000000000001033

### 4. O'Donovan & McAuliffe 2020: 14 müdahale, sonuçlar karışık; Raemer ve ark. RKÇ'sinde söz almada anlamlı değişim yok
- **Hüküm: DOĞRU**
- **Doğrusu:**
  - 14 müdahale, beş kategori, "karışık sonuçlar". Etki sınırlı, çünkü nesnel ölçüm az ve **eğitim tek başına** köklü davranışı değiştirmekte yetersiz. PROSPERO CRD42018100659.
  - Tam metinde (Europe PMC XML) şu cümle var: "Pian-Smith ve arkadaşları iyileşme buldu, ama Raemer ve arkadaşları istatistiksel olarak anlamlı değişim bulmadı."
  - Raemer'in kendi özeti de bunu doğruluyor. Raemer DB, Kolbe M, Minehart RD. *Acad Med* 2016;91(4):530-539. Simülasyonla yapılmış RKÇ. Katılımcılar eğitimde olmayan, çalışan anestezistler. Müdahale n=35, kontrol n=36. Üç olayın hiçbirinde anlamlı fark yok. Sonuç cümlesi: "Eğitim müdahalesi tek başına etkisizdi."
  - Eksik: Raemer raporun kaynakçasında yok. Eklenmeli.
  - Ek bilgi: kendi anestezist meslektaşına söz alanların oranı yalnız %25.
- **Kaynak:** https://europepmc.org/article/PMC/PMC7011517 (tam metin XML: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7011517/fullTextXML) ; https://doi.org/10.1097/ACM.0000000000001033

### 5. Müller ve ark. 2018 (*BMJ Open* 8(8):e022202): SBAR üzerine 11 çalışma (8 öncesi-sonrası, 3 kontrollü); orta düzey kanıt; en çok telefon iletişiminde
- **Hüküm: DOĞRU** (bir ifade düzeltmesiyle)
- **Doğrusu:**
  - 8 öncesi-sonrası çalışma ve 3 kontrollü klinik çalışma.
  - 26 hasta sonucu ölçülmüş. 8'inde anlamlı iyileşme var. 11'inde iyileşme bildirilmiş ama istatistik testi yok. 6'sında değişim yok.
  - Sonuç: SBAR ile hasta güvenliğinin arttığına dair **orta düzey kanıt** var, özellikle telefonda. Yüksek kaliteli araştırma eksik.
  - Düzeltme: Rapor bulgu 5'te "hasta güvenliğinde **orta düzey iyileşme** buldu" diyor. Doğrusu "iyileşmeye dair **orta düzey kanıt**". "Orta düzey", etkinin büyüklüğünü değil, kanıtın gücünü anlatıyor.
- **Kaynak:** https://api.openalex.org/works/doi:10.1136/bmjopen-2018-022202

### 6. Wacker & Dziobek 2018: ŞİD eğitimi sağlık çalışanlarında empatik sıkıntıyı ve sosyal stresörleri azalttı; desen?
- **Hüküm: KISMEN**
- **Doğrusu:**
  - Desen: **kontrol gruplu, öncesi-sonrası saha çalışması.** Üç günlük eğitim verildi. Anketler eğitimden önce ve 3 ay sonra dolduruldu. Sonuçlar eğitim almayan bir kontrol grubuyla karşılaştırıldı. Özet rastgele atamadan söz etmiyor; büyük olasılıkla RKÇ değil. Raporun "yarı deneysel" etiketi bu yüzden makul. Örneklem büyüklüğü özette yok. Davranış gözlemi yalnız eğitim grubunda yapıldı.
  - Empatik sıkıntı azaldı: DOĞRU.
  - Sosyal stresörler "azaldı" demek **yanlış**. Özette şöyle yazıyor: "duyguyu sözle ifade etme arttığı için sosyal stresörlerdeki **artış önlendi**". Bu bir aracı (mediasyon) bulgusu, doğrudan bir azalma değil.
  - Künye: çevrim içi 2016, basılı 2018, 23(1):141-150. Kurum: Freie Universität Berlin, yani Alman kamu sağlık kurumu.
- **Kaynak:** https://europepmc.org/article/MED/27977228 ; https://api.openalex.org/works/doi:10.1037/ocp0000058

---

## B. Beden dili ve ses: güç pozu, duruş, perde

### 7. Carney, Cuddy, Yap 2010: son örneklem n=42; Ranehill 2015: yaklaşık 200
- **Hüküm: DOĞRU**
- **Doğrusu:**
  - n=42 iki kaynakta doğrulandı. (a) Simmons & Simonsohn 2017 özeti: "katılımcılar (N=42)". Bu, araştırmacının kaynağından farklı. (b) Carney'nin 2016 açıklaması: "Son örneklem büyüklüğü N = 42."
  - Ranehill: N=200. Bu bir ikincil kaynaktan geliyor: Wikipedia "Amy Cuddy" maddesi, dipnot 25: "orijinal deneyde 42 kişi (koşul başına 21), Ranehill ve arkadaşlarında 200." Birincil özet bu oturumda açılamadı (SAGE 403, Europe PMC ve PubMed kaydında özet yok).
  - Ranehill'in başlığı da "erkek ve kadınlardan oluşan **büyük örneklemde** hormon ve risk toleransına etki yok" diyor.
  - Eksik nüans: Ranehill **öznel güç hissi** (manipülasyon kontrolü) üzerinde anlamlı etki buldu (Data Colada [37]). Bu, Cuddy 2018'in savunusuyla tutarlı. Rapor bunu Ranehill'e bağlamamış.
  - Orijinal poz "1'er dakikalık iki poz" idi. Rapordaki "iki dakikalık poz" doğru.
- **Kaynak:** https://api.openalex.org/works/doi:10.1177/0956797616658563 ; https://en.wikipedia.org/wiki/Amy_Cuddy ; https://datacolada.org/37 ; https://faculty.haas.berkeley.edu/dana_carney/pdf_My%20position%20on%20power%20poses.pdf

### 8. Elkjær ve ark. 2022: 73 çalışma; büzülmüş ve nötr karşılaştırması g=0,45; genişleyici ve nötr karşılaştırması g=0,06
- **Hüküm: DOĞRU**
- **Doğrusu:** 5.819 kayıttan 73 çalışma çıktı. Duygulanım ve açık davranışta genişleyici ile büzülmüş duruş arasında sağlam fark var. Etki, büzülmüş duruşun **yokluğundan** geliyor (büzülmüş ve nötr karşılaştırması g=0,45). Genişleyici duruşun varlığı etki yaratmıyor (genişleyici ve nötr karşılaştırması g=0,06). Çevrim içi 2020, basılı 2022, 17(1):276-304.
  - Not: Özet bu sonucu duygulanım ve davranış için veriyor. Hormon etkisini desteklemiyor; yazarlar farklı hormon ölçüm yöntemleri öneriyor. Raporun "kamburlaşma" önerisi bu bulguya uyuyor.
- **Kaynak:** https://api.openalex.org/works/doi:10.1177/1745691620919358

### 9. Cheng ve ark. 2016: ilk dakikalarda perdeyi düşürenler daha yüksek rütbe kazandı. Ko ve ark. 2015: yüksek rütbede perde daha yüksek, perde dalgalanması daha az
- **Hüküm: DOĞRU**
- **Doğrusu:**
  - Cheng: Çalışma 1 yüz yüze grup etkileşimi. Etkileşimin başında perdeyi **yükseltmek** daha düşük rütbeyi, **düşürmek** daha yüksek rütbeyi yordadı. Çalışma 2'de perde deneysel olarak değiştirildi; bu, rütbe ve güç algısını değiştirdi. "Baskın algılandı" kısmı Çalışma 2'den geliyor; orada değerlendirenler ayrı bir dinleyici grubu.
  - Ko: Deney 1'de yüksek rütbe koşulunda perde daha yüksek, gürlük değişkenliği daha fazla, perde değişkenliği daha az. Deney 2'de dinleyiciler yüksek perde, gürlük ve gürlük değişkenliğine bakarak rütbeyi doğru tahmin etti.
  - Raporun "basit 'sesini kalınlaştır' kuralı tutarsız" sonucu doğru. Ama önerdiği "titremeyen, duyulur ses" doğrudan bu iki çalışmanın bulgusu değil; bir sentez. Uzman görüşü diye etiketlenmeli.
- **Kaynak:** https://api.openalex.org/works/doi:10.1037/xge0000166 ; https://api.openalex.org/works/doi:10.1177/0956797614553009

---

## C. Duygu düzenleme ve öz-şefkat

### 10. Webb, Miles, Sheeran 2012 etki büyüklükleri
- **Hüküm: DOĞRU**
- **Doğrusu:** 306 deneysel karşılaştırma. Uyaranı yeniden değerlendirme d=0,36. Bakış açısı alma d=0,45. İfadeyi bastırma d=0,32. Yaşantıyı bastırma d=−0,04. Düşünceyi bastırma d=−0,12. Dikkat dağıtma d=0,27. Yoğunlaşma d=−0,26. Rakamların hepsi tutuyor.
  - Eksik bağlam: Raporda olmayan iki rakam var. Dikkat yönlendirme genel olarak sıfır etkili (d=0,00). Duygusal **yanıtı** yeniden değerlendirme daha zayıf (d=0,23).
  - Rapor d=0,32'yi "ifadeyi azaltıyor" diye okumuş. Oysa bu değer yaşantı, davranış ve fizyoloji ölçümlerinin birleşik etkisi. İfade bastırmanın sosyal bedeli ayrı bir bulgu: Butler 2003 bunu kadın çiftlerde, uyum ve kan basıncı üzerinden gösterdi. Raporun "bastırma uyumu bozar" cümlesi doğru.
- **Kaynak:** https://api.openalex.org/works/doi:10.1037/a0027600 ; https://api.openalex.org/works/doi:10.1037/1528-3542.3.1.48

### 11. Ferrari ve ark. 2019 (*Mindfulness* 10(8):1455-1473): 27 RKÇ; öz-eleştiri, ruminasyon, stres, depresyon
- **Hüküm: DOĞRULANAMADI** (künye DOĞRU)
- **Doğrusu:** Başlık, yazarlar, dergi, cilt ve sayfa doğru: "Self-Compassion Interventions and Psychosocial Outcomes: a Meta-Analysis of RCTs" (Ferrari, Hunt, Harrysunker, Abbott, Beath, Einstein). Yayıncı özeti OpenAlex, Semantic Scholar ve Crossref'e vermiyor. Springer sayfası bot kontrolüne takıldı. RKÇ sayısı (27) ve sonuç alanları bu oturumda **doğrulanamadı**. Raporun kendi [K] etiketi yerinde. Sentezde rakam verilmemeli.
- **Kaynak:** https://api.openalex.org/works/doi:10.1007/s12671-019-01134-6

---

## D. Geri bildirim, rica, belge

### 12. Ashford & Tsui 1991: olumsuz geri bildirim istemek yönetici etkinliği algısını artırdı, olumlu geri bildirim istemek azalttı
- **Hüküm: DOĞRULANAMADI** (kısmen teyit)
- **Doğrusu:** Künye doğru: *AMJ* 34(2):251-280. Bir **saha çalışması**. 387 yöneticinin geri bildirim arayışını amirleri, astları ve eşitleri değerlendirdi. Erişilebilen özet "yöneticilerin olumsuz geri bildirim arama eğilimi…" diye başlayıp kesiliyor. AOM ve JSTOR sayfaları açılmadı. "Olumlu geri bildirim istemek etkinlik algısını azalttı" kısmı bu oturumda teyit edilmedi.
  - Çıkarım uyarısı: Bulgu, 1991'de ABD'li orta düzey yöneticilerden gelen ilişkisel bir bulgu. Karşı taraf düşmanca davranan bir hocaysa, "Nerede hata yaptım?" sorusu yeni azar malzemesi olabilir. Bu soru **iyi niyetli ve uzman** kişiye sorulmalı. Rapor bunu "uzman bir kişiden" diye sınırlamış; doğru.
- **Kaynak:** https://api.openalex.org/works/doi:10.2307/256442

### 13. Bohns 2016: 14.000'den fazla rica; kabul olasılığı ortalama %48 küçümsendi
- **Hüküm: KISMEN** (rakamlar DOĞRU; rapordaki çıkarım YANLIŞ)
- **Doğrusu:**
  - Rakamlar doğru. Katılımcılar 14.000'den fazla **yabancıya** rica etti. Rica edenler kabul olasılığını ortalama %48 küçümsedi. Neden: rica edenler "hayır" demenin **karşı taraf için** ne kadar zor olduğunu hesaba katmıyor. Etkiyi güçlendiren, zayıflatan ve **tersine çeviren** koşullar da var.
  - **Yanlış çıkarım.** Bulgu 18'in başlığı "Hayır demenin bedeli genellikle abartılır". Kanada cümlesi 27'nin gerekçesi "hayır demek beklenenden az zarar verir". Bohns bunu **göstermiyor**. Bohns'un bulgusu neredeyse tersi: hayır demek zordur ve garip hissettirir; insanlar bu yüzden evet der. Bulgu, reddetmenin ilişkiye ya da kariyere bedelini ölçmüyor.
  - Doğru kullanım: "Karşı taraf istemeyi sürdürür, çünkü hayır demek zordur ve istemek çoğunlukla işe yarar. Bu yüzden önceden hazırlanmış bir 'hayır + alternatif' cümlesi garipliği azaltır." Raporun "Çıkarım" kısmı bununla uyumlu. Yanlış olan başlık ve 27. madde gerekçesi.
  - Reddetmenin sosyal bedelinin beklenenden küçük olduğuna dair ayrı bir literatür olabilir. Örneğin davet reddi üzerine Givi & Kirk, *JPSP* 2024. Bu künye bu oturumda **doğrulanamadı**; arama yapılamadı.
- **Kaynak:** https://api.openalex.org/works/doi:10.1177/0963721415628011

### 14. CCOHS "Bullying in the Workplace": 20.10.2026 güncelleme; belge tutma önerileri
- **Hüküm: DOĞRU**
- **Doğrusu:**
  - Sayfadaki "Date modified": 2026-10-20.
  - Önerilenler: olayların olgusal günlüğü (tarih, saat, ayrıntılı anlatım, tanıklar, sonuç; örüntü ve niyet önemlidir), mektup, not ve e-posta kopyaları, politikadaki kişiye ya da amire bildirim (ciddiye alınmazsa bir üst kademe), destek ağı ve çalışan destek programı.
  - Yapılmaması gerekenler: misilleme (sizi fail gibi gösterebilir), kendini suçlamak, rahatsız edici sohbete girmek ("I'm not comfortable discussing this" deyip çekilmek), çarpık ifadelere katılmak ya da itiraz etmek.
  - Raporda olmayan iki öneri var:
    - (a) İlk adım, kişiye davranışın kabul edilemez olduğunu **doğrudan söyleyip durmasını istemek**. İsterseniz yanınızda güvendiğiniz biri (amir, sendika temsilcisi) olabilir.
    - (b) Sağlık etkilenirse belirtileri, hekim ve psikolog ziyaretlerini ve tedavileri belgelemek.
  - Sınır: Sayfa tarihi ancak sayfanın kendisinden doğrulanabilir. Kaynak araştırmacınınkiyle aynı.
- **Kaynak:** https://www.ccohs.ca/oshanswers/psychosocial/bullying.html

### 15. TUEY (03.09.2022, RG 31942): angarya yasağı ve gerekçeli kanaat notu
- **Hüküm: DOĞRU** (iki nüansla)
- **Doğrusu:**
  - RG 03.09.2022, sayı 31942. Md. 11/4: "Uzmanlık öğrencileri, uzmanlık eğitimi uygulamasından sayılmayan işlerde görevlendirilemez."
  - Kanaat notu md. 17/2-ç'de. Altı ayda bir, "belgesi ve gerekçesiyle birlikte yazılı olarak" oluşturulur. Olumsuz notta 15 iş günü içinde yazılı uyarı yapılır. Sonuçları md. 16/4-c'de: üst üste iki olumsuz notta program değişir ve süreye bir yıl eklenir.
  - **Nüans 1, istisna:** Deprem, sel ya da salgın gibi olağandışı hallerde öğrenci aynı ildeki hekimlik görevine verilebilir. Bir seferde en çok 3 ay, toplam en çok 6 ay.
  - **Nüans 2, 07.10.2023 değişikliği (RG 32332):** Kanaati artık **birim eğitim sorumlusu** yazar, **kurum eğitim sorumlusu** onaylar. Öğrencinin müfredata uygun eğitim isteme hakkı da artık "akademik kurul"a değil, "**uzmanlık eğitimi kurulu**"na karşı (md. 11/6). Talep reddedilir ya da öğrenci itiraz ederse, kurum durumu 15 iş günü içinde Bakanlığa bildirir.
  - Rapordaki 5. örnek cümle "eğitim sorumlumuzla planlayalım" diyor. Doğru unvan "birim eğitim sorumlusu" (ya da gündelik dilde "eğitim sorumlusu hocamız").
- **Kaynak:** https://www.resmigazete.gov.tr/eskiler/2022/09/20220903-2.htm ; https://www.resmigazete.gov.tr/eskiler/2023/10/20231007-2.htm

---

## E. Ek kontroller (raporda geçen, karar etkileyen)

### 16. Ünal 2012 (*Contemporary Nurse* 43(1):90-98): "Türkiye'de hemşirelerle bir müdahale çalışması"; "yarı deneysel"
- **Hüküm: KISMEN**
- **Doğrusu:** Türkiye doğru: Satı Ünal, Gazi Üniversitesi Sağlık Bilimleri Fakültesi, Ankara. Ama katılımcılar **hemşire değil, ikinci sınıf hemşirelik öğrencisi** (n=79). Başlıktaki "nurses" kelimesi yanıltıcı. Desen **tek gruplu ön test–son test**, kontrol grubu yok. Bu, yarı deneyselden de zayıf bir desen. Ders 14 hafta, haftada 3 saat sürdü. Atılganlık (Rathus) ve benlik saygısı (Coopersmith) puanları arttı.
- **Kaynak:** https://api.openalex.org/works/doi:10.5172/conu.2012.43.1.90

### 17. Williams & Tiedens 2016 (rapor 2. bölüm): kadınlarda açık baskınlık beğeni kaybı getirir; "sakin ses, hazırlık, yapılandırılmış sunum gibi örtük sinyaller cezalandırılmıyor"
- **Hüküm: KISMEN**
- **Doğrusu:**
  - Beğeni cezası küçük: d=−0,19, k=63. Açık baskınlıkta, örneğin doğrudan taleplerde, d=−0,28.
  - Örtük baskınlıkta beğeni cezası yok: d=0,03. Ama özetteki **tek örnek göz teması**. "Sakin ses, hazırlık, yapılandırılmış sunum" meta-analizin test ettiği örnekler değil; raporun genellemesi.
  - Raporun atladığı en önemli rakam: **işe alınabilirlik cezası d=−0,58** (k=20). Bu orta büyüklükte bir etki.
  - Yetkinlik algısında cinsiyet farkı yok: d=0,02.
  - Not: Çevrim içi 2015, basılı 2016, *Psychol Bull* 142(2):165-197. Aynı düzeltme d_psikoloji ve d_egitim_istismari dosyalarında da var. Bu oturumda özet ayrıca okunarak teyit edildi.
- **Kaynak:** https://api.openalex.org/works/doi:10.1037/bul0000039

### 18. Tiedens & Fragale 2003 (rapor 2. bölüm): uzun özür "tamamlayıcı (küçülen) yanıt"tır ve baskın davranışı farkında olmadan ödüllendirebilir
- **Hüküm: KISMEN** (kanıtın ötesinde bir çıkarım)
- **Doğrusu:** Çalışmada katılımcılar bir yardımcı deneyciyle etkileşti. Deneyci ya duruşunu genişletti ya da büzdü. Baskın deneyci karşısında katılımcı küçüldü, boyun eğen deneyci karşısında genişledi. Tamamlayıcı yanıt veren katılımcılar karşısındakini **daha çok sevdi ve daha rahat hissetti**.
  - Ölçülen şey **sözsüz duruş**, sözlü özür değil. "Baskın kişiyi ödüllendirmek" ya da baskın davranışın artması ölçülmedi.
  - Bulgunun dürüst bir yan sonucu var: Tamamlayıcı olmayan, küçülmeyen bir yanıt etkileşimi bir süre **daha rahatsız** hissettirebilir. Raporun "KOP döngüyü keser" iddiası test edilmemiş bir öneri; uzman görüşü diye etiketlenmeli.
- **Kaynak:** https://api.openalex.org/works/doi:10.1037/0022-3514.84.3.558

### 19. Kolbe ve ark. 2012 ve Pian-Smith ve ark. 2009 (bulgu 4): söz alma simüle anestezi ekiplerinde daha iyi performansla ilişkili; iki itiraz kuralı simülasyonla öğretildi
- **Hüküm: KISMEN**
- **Doğrusu:**
  - Kolbe: 31 hemşire ve 31 asistan; prospektif gözlemsel çalışma. Teknik ekip performansını yalnız **hemşirelerin** söz alması yordadı (R²=0,18; p=0,017). **Asistanlarınki anlamlı değildi** (p=0,053). Kullanıcının konumu asistana daha yakın, bu yüzden bu ayrıntı önemli.
  - Pian-Smith: 40 anestezi asistanı, simüle obstetrik vakalar. Tek gruplu öncesi-sonrası desen. Debriefing'den sonra hekim **üstlere** yöneltilen itirazların sıklığı ve kalitesi arttı. **Hemşirelere** yöneltilen itirazlar artmadı. Öğretilen teknik "savunma + soru" (advocacy-inquiry): gözlemini söyle, karşı tarafın gerekçesini sor.
- **Kaynak:** https://api.openalex.org/works/doi:10.1213/ANE.0b013e318269cd32 ; https://api.openalex.org/works/doi:10.1097/SIH.0b013e31818cffd3

### 20. Brooks, Gino, Schweitzer 2015 (bulgu 14, Kanada cümlesi 28): tavsiye istemek yetkinlik algısını artırır
- **Hüküm: DOĞRU** (kullanımda bir sınırla)
- **Doğrusu:** Tavsiye isteyen kişi daha yetkin görüldü. Üç düzenleyici var: görev **zor** olmalı (kolay görevde değil), tavsiye değerlendiren kişinin **kendisinden** istenmeli, ve o kişi **uzman** olmalı. Rapor bunu doğru aktarıyor.
  - Ancak 28. cümle ("sigorta kodu nasıl işliyor, bir kez gösterir misiniz?") kolay ve idari bir konu. Gerekçe olarak Brooks zayıf kalır. Cümle yine de makul. Gerekçe "yerel sistemi öğrenme isteği" olmalı.
- **Kaynak:** https://api.openalex.org/works/doi:10.1287/mnsc.2014.2054

**Hızlı kontrol edilen ve sorun bulunmayanlar** (künye ve özet tutuyor): Querstret & Cropley 2013 (19 çalışma; bilinçli farkındalık ve BDT ruminasyonu ve kaygıyı azaltabilir), Chen ve ark. 2013 (videoyla iki çalışma; göz teması karşı görüşteki dinleyicide ikna olmayı azalttı), Price & Baker 2012 (11 makale, yedi tema), Ayyala ve ark. 2019 (23 görüşme: 12 sponsor, 11 korunan), Anseel ve ark. 2015 (geri bildirim arama ile performans ilişkisi küçük), Ames & Flynn 2007 (ters U), Ames & Wazlawek 2014 ("çizgiyi aşma yanılgısı"; 4 çalışma), Gross & John 2003, Watkins 2008, Pattni ve ark. 2019 (31 çalışmalık anlatı sentezi).

---

## Hüküm tablosu

| # | İddia | Hüküm |
|---|---|---|
| 1 | Omura 2017: kanıt zayıf/tutarsız | KISMEN |
| 2 | Speed 2018: "unutulmuş kanıta dayalı tedavi" | DOĞRU |
| 3 | Okuyama 2014: 26/27, altı kategori; "en çok engelleyen yetersiz görünme" | KISMEN (alt iddia YANLIŞ) |
| 4 | O'Donovan 2020 + Raemer RKÇ | DOĞRU |
| 5 | Müller 2018 SBAR | DOĞRU |
| 6 | Wacker & Dziobek 2018 ŞİD | KISMEN |
| 7 | Carney n=42; Ranehill n≈200 | DOĞRU |
| 8 | Elkjær 2022: 73; g=0,45 / 0,06 | DOĞRU |
| 9 | Cheng 2016; Ko 2015 | DOĞRU |
| 10 | Webb 2012 etki büyüklükleri | DOĞRU |
| 11 | Ferrari 2019: 27 RKÇ | DOĞRULANAMADI |
| 12 | Ashford & Tsui 1991 | DOĞRULANAMADI |
| 13 | Bohns 2016 | KISMEN (çıkarım YANLIŞ) |
| 14 | CCOHS 20.10.2026 | DOĞRU |
| 15 | TUEY angarya + gerekçeli kanaat | DOĞRU |
| 16 | Ünal 2012 "hemşireler" | KISMEN |
| 17 | Williams & Tiedens 2016 örtük sinyaller | KISMEN |
| 18 | Tiedens & Fragale 2003 "ödüllendirir" | KISMEN |
| 19 | Kolbe 2012 / Pian-Smith 2009 | KISMEN |
| 20 | Brooks 2015 | DOĞRU |

Uydurma atıf: **yok**. Doğrudan YANLIŞ olan iki alt iddia var: Okuyama'ya dayandırılan "en çok engelleyen" sıralaması ve Bohns'tan çıkarılan "hayır demenin bedeli abartılır" sonucu.

---

## Raporu okuyanların bilmesi gereken kritik düzeltmeler

1. **"Hayır demek beklenenden az zarar verir" Bohns'tan çıkmaz.** Bohns 2016'nın bulgusu şu: rica edenler, hayır demenin karşı taraf için ne kadar zor olduğunu küçümsüyor. Reddetmenin bedeli ölçülmedi. Bulgu 18'in başlığı ve Kanada cümlesi 27'nin gerekçesi düzeltilmeli. Önerilen ifade: "Karşı taraf istemeyi sürdürür, çünkü hayır demek zordur. Hazır bir 'hayır + alternatif' cümlesi bu zorluğu azaltır." Cümle kütüphanesinin kendisi (hayır + alternatif) korunabilir. Değişmesi gereken yalnız gerekçe.

2. **"Söz almayı en çok engelleyen şey yetersiz görünme korkusu" desteksiz.** Okuyama etkenleri sıralamıyor; göreli önemin bilinmediğini açıkça yazıyor. Raemer'in nitel verisinde en sık engeller şunlar: konudan emin olmamak, kalıp yargılar, tanışıklık, deneyime saygı, misilleme beklentisi. 2. bölümdeki "nazik kişide eksik olan olgu ve doğru kişidir" çıkarımı makul bir hipotez olarak kalabilir. Ama "en çok" ifadesi çıkarılmalı.

3. **Atılganlık eğitimi kanıtı raporun yazdığından daha olumlu.** Omura 2017 özeti, eğitimin deneyimli anestezistler dışında tüm gruplarda "bir ölçüde etkili" olduğunu söylüyor. Davranış simülasyonda ölçülmüş. Eksik olan şunlar: gerçek klinikte etki, kalıcılık ve hasta sonucu. "Zayıf ve tutarsız" yerine şu ifade kullanılmalı: "kısa vadede ve simülasyonda umut verici; gerçek klinik ve hasta sonucu kanıtı yok." Asıl sınırlılık bundan sonra geliyor: Raemer RKÇ'sine göre **eğitim tek başına**, deneyimli hekimlerde davranışı değiştirmedi. Raporun "cümle kalıbı gerekli ama yeterli değil; kurum ve amir seçimi daha büyük kaldıraç" çıkarımı doğru ve korunmalı.

4. **SBAR'da "orta düzey" kanıtın gücünü anlatır, etkinin büyüklüğünü değil.** 11 çalışma, 26 sonuç ölçümü. 8 sonuçta anlamlı iyileşme var, 11'inde test yapılmamış.

5. **ŞİD çalışması sosyal stresörleri azaltmadı, artışını önledi.** Desen kontrol gruplu öncesi-sonrası; randomizasyon belirtilmemiş. Empatik sıkıntı azaldı. Kanıt düzeyi: tek, rastgele olmayan saha çalışması.

6. **Ünal 2012 hemşirelerle değil, hemşirelik öğrencileriyle yapıldı** (n=79). Desen tek gruplu ön test–son test, kontrol yok. "Türkiye'de sağlık çalışanında atılganlık eğitimi kanıtı" diye sunulmamalı.

7. **Kadın kullanıcı için ceza beğenide küçük, işe alınabilirlikte orta** (Williams & Tiedens: d=−0,19'a karşı d=−0,58). "Örtük sinyaller cezalandırılmıyor" bulgusunun özetteki tek örneği göz teması. "Sakin ses, hazırlık" bu bulgunun kapsamında değil. Bu, raporun genellemesi. Kanada'da iş görüşmesi ve ortaklık kararlarında bu ayrım önemli.

8. **"Uzun özür baskın kişiyi ödüllendirir" test edilmemiş bir çıkarım.** Tiedens & Fragale, sözsüz duruşta tamamlayıcılığın rahatlık ve beğeni getirdiğini gösterdi. Bunun bir yan sonucu da var: küçülmeyen yanıt kısa vadede etkileşimi daha gergin hissettirebilir. KOP formülü makul bir öneri, ama "döngüyü keser" diye kanıtlanmış gibi sunulmamalı. Uzman görüşü diye etiketlenmeli.

9. **Kolbe 2012'de performansı yalnız hemşirelerin söz alması yordadı.** Asistanlarınki anlamlı değildi (p=0,053). Pian-Smith'te eğitim, üst hekime yöneltilen itirazları artırdı; hemşireye yöneltilenleri artırmadı. DUS'taki kullanıcı için ders şu: kalıp eğitimi hiyerarşinin bir yönünde işe yarayıp diğerinde yaramayabilir.

10. **TUEY örnek cümleleri 2023 sonrası unvanlarla yazılmalı.** Kanaati **birim eğitim sorumlusu** yazar, **kurum eğitim sorumlusu** onaylar. Eğitim talebi **uzmanlık eğitimi kurulu**na yapılır (RG 07.10.2023/32332). Angarya yasağının afet ve salgın istisnası var: bir seferde en çok 3 ay, toplam en çok 6 ay.

11. **CCOHS'un ilk önerisi rapordan düşmüş:** davranışın kabul edilemez olduğunu kişiye doğrudan söylemek ve durmasını istemek. İsterseniz yanınızda güvendiğiniz biri olabilir. Sağlık etkilenirse belirtileri ve tedavileri de belgelemek öneriliyor. Bunlar Kanada senaryosunda eklenmeli.

12. **Doğrulanamayanlar ikincil sayılmalı.** Ferrari 2019'un "27 RKÇ" ve sonuç alanları ile Ashford & Tsui'nin "olumlu geri bildirim istemek etkinlik algısını azaltır" yarısı bu oturumda teyit edilmedi. Sentezde rakam vermeden, "bir meta-analiz / bir saha çalışması" diye anılmalı.

13. **Doğrulama sınırı.** Bu turda web arama kotası dolmuştu. 2020–2026 tarihli atılganlık ve söz alma meta-analizleri ile Türkçe literatür **aranamadı**. Bu, araştırmacının da yazdığı boşluk. Kullanıcı isterse takip mesajıyla bu aramalar yapılabilir.
