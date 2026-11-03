# Doğrulama: Sağlık eğitiminde ve asistanlıkta kötü muamele (r1 dosyası)

Doğrulayıcı: bağımsız doğrulayıcı (çürütmeye çalışan). Tarih: 03.11.2026.
Doğrulanan dosya: `ajanlar/r1_egitim_istismari.md` (değiştirilmedi).

## Yöntem notu (önemli)

- Bu turda web arama kotası ilk sorguda doldu. Hiç WebSearch sonucu alınamadı.
- Bu yüzden doğrulama, bilinen kayıtların doğrudan çekilmesiyle yapıldı: Europe PMC REST kayıtları ve tam metinleri, OpenAlex ve Crossref meta verisi, dergi sayfası (MJA), Resmî Gazete'nin kendi PDF'i ve CDHA'nın PDF'i.
- Araştırmacı çoğunlukla PubMed/PMC ve ikincil sitelere dayanmıştı. Burada aynı çalışmaların kayıtları başka bir dizinden (Europe PMC, OpenAlex) ayrıca çekildi. Özet metni aynı yayıncıdan geldiği için bu tam bağımsız bir kaynak sayılmaz. Ama atıf künyesi, rakamlar ve tam metin tabloları ayrıca okundu.
- Genelge için araştırmacının açamadığı Resmî Gazete metni bu kez **doğrudan okundu**.
- CDHA için başka kaynak bulunamadı. Aynı birincil PDF metne çevrilip satır satır okundu.
- Uydurma atıf bulunamadı. Bütün künyeler (yazar, yıl, dergi, cilt) gerçek kayıtlarla eşleşti.

---

## İddialar

### 1. Fnais ve ark. 2014 (Acad Med 89(5):817-27)
- **İddia:** 51 çalışma. Havuzlanmış yaygınlık %59,4 (GA %52,0–66,7). En sık tür sözlü taciz, %63,0. Zamanla azalma yok.
- **Hüküm:** DOĞRU
- **Doğrusu:** Rakamların hepsi doğru. Sözlü tacizin GA'sı %54,8–71,2. Ek bilgi: en sık kaynak kıdemli hekimler/hocalar (%34,4), sonra hasta ve yakınları (%21,9). Sayfa aralığı 817-827. DOI: 10.1097/ACM.0000000000000200. Çalışmaların çoğu kesitsel. Tanımlar farklı.
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:24667512%20AND%20SRC:MED&resultType=core&format=json ; https://doi.org/10.1097/ACM.0000000000000200

### 2. Bahji ve Altomare 2020 (Can Med Educ J)
- **İddia:** 52 çalışma, 63.378 asistan. Genel yaygınlık %64,1 (GA %51,0–77,1). Kaynaklar: hasta yakınları %50,7, hemşireler %47,8, hastalar %41,7, kadrolu hekimler %39,0, diğer asistanlar %35,8. Sözlü %61,5, tekrarlayan %52,1, ceza olarak iş %26,9, akademik %26,5. Kadınlar ve görünür azınlıklar daha çok etkileniyor. I²=%99,96.
- **Hüküm:** DOĞRU
- **Doğrusu:** Tam metinde hepsi aynen var. Künye: Can Med Educ J 2020;11(1):e97-e123. İki ayrıntı: (a) Toplam 63.378 asistan, ama genel yaygınlık tahmini 22.549 asistanın verisine dayanıyor. (b) Kadın ve azınlık farkı **post hoc** analizden geliyor. Kaynak yüzdeleri toplamı 100 olan paylar değil. Her biri o kaynağı ölçen çalışmaların ayrı havuzlanmış oranı. Heterojenlik çok yüksek, yani kesin rakam gibi okunmamalı.
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7082478/fullTextXML ; https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=PMCID:PMC7082478&resultType=core&format=json

### 3. Hu ve ark. 2019 (NEJM 381:1741-52), rakamlar
- **İddia:** 7.409 cerrahi asistanı, yanıt %99,3. Cinsiyet ayrımcılığı %31,9 (kadınlarda %65,1). Sözlü/fiziksel istismar %30,3. Cinsel taciz %10,3. Haftalık tükenmişlik %38,5. İstismarın kaynağı en sık kadrolu cerrahlar, ayrımcılığınki hasta ve yakınları.
- **Hüküm:** DOĞRU
- **Doğrusu:** Künye: NEJM 2019;381(18):1741-1752, 262 programın tamamı. Rakamlar doğru. Dikkat: %30,3 ve %10,3 **tüm asistanlar** için. Görev metnindeki "kadınlarda ... istismar %30,3, cinsel taciz %10,3" okuması yanlış olur. Kadınlarda cinsel taciz **%19,9**. İstismarın kaynağı %51,9 kadrolu cerrah. Cinsel tacizinki %27,2 kadrolu cerrah. Ayrımcılığınki hasta ve yakınları (cinsiyet %43,6, ırk %47,4). Yıllık intihar düşüncesi %4,5.
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1056/NEJMsa1903759&resultType=core&format=json

### 4. Hu ve ark. 2019: "doz-yanıt, tükenmişlik basamak basamak artıyor" (B3 başlığı)
- **İddia:** Kötü muamele sıklaştıkça tükenmişlik kademeli artıyor.
- **Hüküm:** DOĞRULANAMADI
- **Doğrusu:** Özet tek bir karşılaştırma veriyor: ayda birkaç kez veya daha sık maruz kalanlar ile hiç maruz kalmayanlar. Tükenmişlik OR 2,94 (GA 2,58–3,36). İntihar düşüncesi OR 3,07 (GA 2,25–4,19). Kademeli artış özette yok. Tam metin (NEJM) açılamadı. Kesitsel veri olduğu için neden-sonuç da kurulamaz. Başlık "maruziyet sıklığı arttıkça tükenmişlik oranı da yüksek" diye yumuşatılmalı.
- **Kaynak:** aynı Europe PMC kaydı (yukarıda).

### 5. Hill ve ark. 2020 (JAMA Intern Med 180(5):653-665)
- **İddia:** AAMC Mezuniyet Anketi, 27.504 öğrenci. Kötü muamele kadınlarda %40,9, erkeklerde %25,2. LGB öğrencilerde %43,5, heteroseksüellerde %23,6. Az temsil edilen gruplar daha çok ırk ayrımcılığı bildiriyor.
- **Hüküm:** DOĞRU
- **Doğrusu:** Hepsi doğru. 2016–2017 mezunları, ABD mezunlarının %72,1'i. Irka göre herhangi bir kötü muamele: URM %38,0, beyaz %24,0. Irk ayrımcılığı: URM %23,3, beyaz %3,8. Kadınlarda cinsiyet ayrımcılığı %28,2, erkeklerde %9,4.
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1001/jamainternmed.2020.0030&resultType=core&format=json

### 6. Dyrbye, Satele, West 2021 (JAMA Netw Open)
- **İddia:** 14.126 öğrenci. 2. yılda %22,9 kötü muamele. Bunlarda 4. yılda kariyer pişmanlığı olasılığı %35 daha yüksek.
- **Hüküm:** KISMEN
- **Doğrusu:** Künye: JAMA Netw Open 2021;4(8):e2119110, 140 fakülte. 14.126 ve %22,9 doğru. Ama "%35" eksik ve yanlış anlaşılabilir:
  - OR 1,35 (GA 1,12–1,63) **bir kez** kötü muamele bildirenler için.
  - **Birden fazla kez** bildirenlerde OR 1,87 (GA 1,56–2,23). Yani asıl ilişki doz-yanıtlı. Rapor bunu atlıyor.
  - Bu bir **odds oranı**. "Olasılık %35 daha yüksek" demek teknik olarak doğru değil. Doğru ifade: "kariyer pişmanlığı odds'u yaklaşık 1,35 kat (birden çok kez maruz kalanlarda 1,87 kat)".
  - Model çok değişkenli, 2. yıldaki pişmanlık dahil düzeltilmiş. Kariyer pişmanlığı tanımı: "Yeniden seçseydin hekim olur muydun?" sorusuna "hayır/muhtemelen hayır".
  - Tasarım iki dalgalı gözlemsel kohort. "Güven: yüksek" ilişki için makul, neden-sonuç için değil.
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8353540/fullTextXML ; https://doi.org/10.1001/jamanetworkopen.2021.19110

### 7. Scott ve ark. 2015 (Med J Aust 203(4), BMJ değil)
- **İddia:** 146 son sınıf öğrencisi, iki fakülte. %74 aşağılayarak öğretmeyi yaşamış, %83,6 görmüş. Yaşayan veya görenlerin "yarıya yakını" bunu öğrenmeye faydalı bulmuş.
- **Hüküm:** KISMEN
- **Doğrusu:**
  - Dergi düzeltmesi doğru: Medical Journal of Australia. Sayfa 185e.1-6.
  - %74,0 ve %83,6 yalnız **erişkin klinik rotasyonları** için. Pediatride yaşayan %28,8, gören %45,1. Rapor bunu belirtmiyor.
  - Görme oranı özette %83,1 (118 kişi), bulgular bölümü ve Tablo 1'de %83,6 (122 kişi). Makale içinde tutarsızlık var. Araştırmacının rakamı tabloyla uyuşuyor.
  - "Yarıya yakını faydalı buldu" abartılı. Makale "yaklaşık %30–50" diyor. Alt gruplara göre %32,0 (erişkinde gören) ile %50,0 (pediatride yaşayan) arası. Doğru ifade: "üçte biri ile yarısı arası".
  - 151 davetliden 146 yanıt (%96,7). Pilot çalışma.
- **Kaynak:** https://www.mja.com.au/journal/2015/203/4/teaching-humiliation-and-mistreatment-medical-students-clinical-rotations-pilot (tablolar okundu) ; https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%22teaching%20by%20humiliation%22%20AND%20AUTH:%22Scott%20KM%22&resultType=core&format=json

### 8. Rowland ve ark. 2010 (Int Dent J 60(2):106-112)
- **İddia:** Beş ülke, yedi fakülte, birinci sınıf. Hocalardan yıldırma %34,6, akran zorbalığı %17. Hoca yıldırması fakülteler arasında anlamlı farklı, akran zorbalığı değil.
- **Hüküm:** DOĞRU
- **Doğrusu:** Hepsi doğru. Dergi düzeltmesi de doğru (International Dental Journal). Yazarlar: Rowland ML, Naidoo S, AbdulKadir R, Moraru R, Huang B, Pau A. Sınır: veri eski (2010), yalnız birinci sınıf ve klinik öncesi döneme yakın. Örneklem büyüklüğü kayıtta yok.
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=AUTH:%22Rowland%20ML%22%20AND%20intimidation%20AND%20dental&resultType=core&format=json

### 9. Baniulyte ve ark. 2023 (BDJ 235(11):859-863)
- **İddia:** 215 yanıt (Temmuz–Ekim 2022). %73,2 sorun görüyor. %88 kıdemli fail. En sık davranış küçümseme. %66 konuyu açmakta rahatsız, %30 desteklenmemiş, %9 işlem yapılacağına güveniyor.
- **Hüküm:** DOĞRU
- **Doğrusu:** Rakamlar doğru. DOI: 10.1038/s41415-023-6553-7. İki küçük ifade farkı: "%88" = katılımcıların %88'i faili kıdemli meslektaş olarak tanımladı. "%9" = bildirimden sonra işlem **yapıldığına** güvenenler. Pilot, kendi seçen örneklem. Yaygınlık tahmini olarak kullanılmamalı.
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:38066139%20AND%20SRC:MED&resultType=core&format=json ; https://doi.org/10.1038/s41415-023-6553-7

### 10. Reknes ve ark. 2016 (Ind Health 54:421-432)
- **İddia:** 1.582 Norveçli hemşire, bir yıllık izlem. Aktif, hedefe yönelik başa çıkma sadece çok düşük maruziyette faydalı. Yüksek maruziyet başa çıkma tarzından bağımsız olarak sonraki kaygıyı artırıyor.
- **Hüküm:** DOĞRU (bulgu); yorum genellemesi abartılı
- **Doğrusu:** Künye 54(5):421-432. Başlangıçta 2.059 hemşire, 1.582'si ikinci dalgada. Bulgu aynen böyle. Ama sınırlar önemli:
  - Test edilen tek şey **genel bir başa çıkma tarzı** (aktif, hedefe yönelik). Belgeleme, müttefik bulma, bildirme, ortam değiştirme gibi somut adımlar test edilmedi.
  - Sonuç değişkeni yalnız kaygı belirtisi. Kariyer, not, misilleme gibi sonuçlar ölçülmedi.
  - Örneklem hemşireler, eğitim ortamı değil.
  - Raporun "bazı kişilere karşı hiçbir bireysel strateji yeterli değil" cümlesi bu çalışmanın gösterdiğinden geniş. Doğru ifade: "Yoğun zorbalıkta kişinin genel başa çıkma tarzı kaygıyı önlemeye yetmiyor. Bu yüzden yapısal adımlar (mesafe, belgeleme, kurumsal kanal, yer değiştirme) öne çıkıyor." Yapısal adımların işe yaradığı da bu çalışmada test edilmedi; o kısım uzman görüşü.
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=AUTH:%22Reknes%20I%22%20AND%20coping%20AND%20anxiety&resultType=core&format=json

### 11. Nielsen, Glasø, Einarsen 2017 (PAID 104:195-206)
- **İddia:** 36 örneklem, 13.896 kişi. Nevrotiklik r=0,25. Uyumluluk r=−0,17. Dışadönüklük ve sorumluluk r=−0,10.
- **Hüküm:** DOĞRU (rakamlar); "nezaket risk faktörü değil" yorumu fazla ileri
- **Doğrusu:** Rakamlar özetle birebir aynı. Ek: açıklık ilişkisiz (r=0,04). 101 kesitsel etki büyüklüğü, Ocak 2015'e kadar yayınlar. Yazarlar ilişkilerin ölçüm yöntemine ve çalışmanın coğrafyasına göre değiştiğini söylüyor. Yorum uyarıları:
  - r=−0,17 küçük bir etki (varyansın yaklaşık %3'ü).
  - Uyumluluk bir kişilik özelliği. Bir hiyerarşide gösterilen nazik davranışla aynı şey değil.
  - Hepsi kesitsel. Nielsen ve Knardahl 2015'e göre zorbalık kişiliği de değiştiriyor.
  - Nevrotiklik en güçlü ilişki. Yani "kaygılı, kırılgan görünme" ile maruziyet arasında bağ olabilir; yönü belirsiz.
  - Raporun "Nezaket risk faktörü değil" cümlesi "Nezaketin tek başına risk faktörü olduğuna dair kanıt yok; uyumluluk özelliği hafifçe daha az tacizle ilişkili" diye yumuşatılmalı.
- **Kaynak:** https://api.openalex.org/works/doi:10.1016/j.paid.2016.08.015 ; https://api.crossref.org/works/10.1016/j.paid.2016.08.015

### 12. CDHA 2018 anketi (3.780 hijyenist)
- **İddia:** Kariyer boyu diş hekimlerinden %42, hastalardan %49. %60'ında politika yok (%42) ya da bilinmiyor (%18). %52 bırakmayı düşünmüş, %30 bırakmış. Son bir yılda %35. Bildirmeyenlerin %70'i misilleme, %68'i iş güvencesi kaygısı.
- **Hüküm:** DOĞRU
- **Doğrusu:** Birincil PDF'te hepsi aynen var. Anket 13 Kasım–17 Aralık 2018. 3.780 üye, üyeliğin %22'si. Ek: iş arkadaşları %37, ofis yöneticileri %36. Son bir yılda hastalardan taciz/zorbalık %32, diş hekimlerinden %21. Dikkat: (a) %70 ve %68, "her zaman bildirmiyorum" diyen %32'lik grubun içindeki oranlar. (b) %52 ve %30'un paydası metinde net değil ("katılımcılar"). (c) Yanıt oranı düşük, kendi seçen örneklem. (d) Veri 2018; 2020 sonrası tekrar bulunamadı (arama yapılamadı).
- **Kaynak:** https://files.cdha.ca/Career/HealthyWorkplace/Healthy_Respectful_Workplace_Highlights_FINAL_web.pdf (başka bağımsız kaynak bulunamadı)

### 13. 2025/3 sayılı Cumhurbaşkanlığı Genelgesi
- **İddia:** Resmî Gazete 06.03.2025, sayı 32833. 2011/2 sayılı Genelge yürürlükten kaldırıldı. Birincil sorumluluk işveren ve yöneticilerde. Başvuru yolları: kurum, CİMER, TBMM Dilekçe Komisyonu, ALO 170 ve diğerleri. Gizlilik ilkesi var.
- **Hüküm:** DOĞRU (Resmî Gazete metni bu kez doğrudan okundu)
- **Doğrusu:**
  - Başlık: "İş Yerlerinde Psikolojik Tacizin (Mobbing) Önlenmesi", Genelge 2025/3. İmza tarihi 5 Mart 2025, yayım 6 Mart 2025 Perşembe, sayı 32833.
  - Metnin son maddesi aynen: "2011/2 sayılı Genelge yürürlükten kaldırılmıştır."
  - Madde 3: "İş yerlerinde psikolojik tacizle mücadele öncelikle işveren ve yöneticilerin sorumluluğunda olup..."
  - Başvuru yolları metinde tam olarak: çalışılan kurum/kuruluş, CİMER, TBMM Dilekçe Komisyonu, ALO 170 aracılığıyla veya doğrudan Çalışma ve Sosyal Güvenlik Bakanlığı, Türkiye İnsan Hakları ve Eşitlik Kurumu (TİHEK), Kamu Denetçiliği Kurumu. Raporun "diğer kurumlar" dediği yer TİHEK ve Kamu Denetçiliği Kurumu.
  - Madde 5: gizlilik, kişilerin özel hayatının korunması, asılsız iddialara karşı itibarın korunması, sürecin "ivedilikle" yürütülmesi.
  - Madde 7: ALO 170'te görevli psikologlar bilgilendirme ve destek verir.
  - Madde 1: Psikolojik Tacizle Mücadele Kurulu ÇSGB bünyesinde yeniden oluşturuldu.
  - Uyarı (bu oturumda ayrıca doğrulanmadı, uzman bilgisi): Genelge esasen idareye yönelik bir talimat. Özel bir aile kliniğinde işverenin bağlayıcı yükümlülüğü asıl olarak Türk Borçlar Kanunu md. 417'den gelir. Kamu Denetçiliği Kurumu yalnız kamu idaresi hakkındaki şikâyetlere bakar; özel klinik için uygun kanal değildir. DUS asistanı kamu kurumunda çalıştığı için Genelge ona daha doğrudan uygulanır.
- **Kaynak:** https://www.resmigazete.gov.tr/eskiler/2025/03/20250306-5.pdf (birincil metin, okundu) ; https://www.resmigazete.gov.tr/eskiler/2025/03/20250306.htm (sayı içeriği)

### 14. Williams ve Tiedens 2016 (Psychol Bull 142(2))
- **İddia:** Açık baskınlıkta kadınların sevilirliği d=−0,28. Örtük baskınlıkta d=0,03. Yetkinlik algısı etkilenmiyor (d=0,02). "Backlash etkisi küçük (d=−0,19 ile −0,28)."
- **Hüküm:** KISMEN
- **Doğrusu:** Künye: Psychol Bull 2016;142(2):165-197 (çevrimiçi Aralık 2015). Verilen d değerleri doğru. Genel sevilirlik cezası d=−0,19 (k=63). Ama rapor önemli bir bulguyu atlıyor: **işe alınabilirlik (hireability) cezası d=−0,58 (k=20)**. Bu küçük değil, orta büyüklükte. Yani "backlash etkisi küçük" genellemesi eksik. Bu, Kanada'daki associate/DSO iş görüşmeleri ve aile kliniğinde terfi/ortaklık gibi "işe alma" kararları için doğrudan önemli. Örtük baskınlık örneği olarak özette göz teması geçiyor; "dik duruş, sakin ses" tam metinden geliyor olabilir, burada doğrulanmadı.
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1037/bul0000039&resultType=core&format=json ; https://doi.org/10.1037/bul0000039

### 15. ten Cate ve Chen 2020 (Med Teach) — "A RICH" beş özelliği
- **İddia:** 13 nitel çalışmanın sentezi. Beş özellik: Yetenek, Dürüstlük, Güvenilirlik, Alçakgönüllülük, Proaktiflik. "Yetenek ana önkoşul, güvenilirlik neredeyse tüm çalışmalarda önemli." Kanıt düzeyi: sistematik derleme.
- **Hüküm:** KISMEN
- **Doğrusu:** Künye: Med Teach 2020;42(12):1413-1420. Beş özellik ve tanımları özette aynen var: Capability (bilgi, beceri, deneyim, durum farkındalığı), Integrity (doğru sözlü, iyi niyetli, hasta merkezli), Reliability (sorumluluk bilinci, öngörülebilir, hesap verebilir), Humility (sınırını bilir, yardım ister, geri bildirime açık), Agency (işe, ekibe, güvenliğe, kendi gelişimine proaktif). "A RICH" kısaltması baş harflerle uyuşuyor (Agency, Reliability, Integrity, Capability, Humility) ve başlıktaki kelime oyununa uyuyor, ama özette geçmiyor; tam metin açılamadı. "Yetenek önkoşul" ve "güvenilirlik neredeyse tüm çalışmalarda" ifadeleri: DOĞRULANAMADI. Kanıt düzeyi etiketi abartılı: yazarlar "anahtar nitel çalışmaların tematik analizi" diyor; sistematik arama tarif edilmiyor. "Nitel çalışmaların anlatı/tematik sentezi" olarak etiketlenmeli.
- **Kaynak:** https://api.openalex.org/works/doi:10.1080/0142159X.2020.1817348 ; https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:33016803%20AND%20SRC:MED&resultType=core&format=json

### 16. Kennedy ve ark. 2008 (Acad Med 83(10 Suppl):S89-92) — dört güvenilirlik alanı
- **İddia:** Gözlem ve görüşmeye dayalı nitel çalışma. Eğiticiler güvenilirliği dört alanda tartıyor: bilgi/beceri, sınırını bilme, doğruluk, sorumluluk bilinci.
- **Hüküm:** DOĞRU
- **Doğrusu:** Özet aynen: "knowledge/skill, discernment of limitations, truthfulness, and conscientiousness". Tasarım: iki aşamalı, temellendirilmiş kuram. 88 ekip üyesi, 216 saat gözlem, 65 kısa görüşme, 36 derinlemesine görüşme (video vinyetli). İç hastalıkları ve acil tıp. Raporun "eğiticiler dil ipuçlarını güven kanıtı olarak kullandı" cümlesi özette yok; doğrulanamadı.
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=AUTH:%22Kennedy%20TJ%22%20AND%20AUTH:%22Lingard%20L%22%20AND%20trustworthiness&resultType=core&format=json

### 17. Çolak ve ark. 2026 (Eur J Dent Educ, doi 10.1111/eje.70216)
- **İddia:** İki merkezli Türk çalışması. %99,3 en az bir zorbalık davranışı bildirdi. Zorbalık depresyon, kaygı, stresle bağımsız ilişkili. Oran tanıma bağlı olabilir.
- **Hüküm:** DOĞRU
- **Doğrusu:** Çalışma gerçek. Yazarlar: Çolak S, Erdil A, Keldal G, Çolak İO, Başal A, Dal B. Merkezler: Tokat Gaziosmanpaşa Üniversitesi ve Uşak Üniversitesi. 414 dördüncü ve beşinci sınıf öğrencisi. Araç: AbuAlula ve ark.'tan uyarlanan 30 maddelik anket ve DASS-21. Araştırmacının şüphesi yerinde: yazarların kendisi %99,3'ün geniş tanımdan geldiğini, sürekli/ağır zorbalık yaygınlığı olmadığını yazıyor. En az hafif belirti: depresyon %70,3, kaygı %82,1, stres %57,7. Çevrimiçi 14 Haziran 2026; cilt/sayfa henüz yok.
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1111/eje.70216&resultType=core&format=json

### 18. McCarthy ve McEvoy 2015 (JAMA) — araştırmacının "URL doğrulanmadı" dediği atıf
- **İddia:** "Pimping in medical education: lacking evidence and under threat", JAMA 2015.
- **Hüküm:** DOĞRU
- **Doğrusu:** JAMA 2015;314(22):2347-2348. DOI: 10.1001/jama.2015.13570. Bir görüş yazısı (uzman görüşü), ampirik çalışma değil. Aynı yazarların 2016 yanıt mektubu da var (JAMA 315(20):2236-2237).
- **Kaynak:** https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=AUTH:%22McCarthy%20CP%22%20AND%20pimping&resultType=core&format=json ; https://doi.org/10.1001/jama.2015.13570

---

## Özet tablo

| # | İddia | Hüküm |
|---|---|---|
| 1 | Fnais 2014 | DOĞRU |
| 2 | Bahji ve Altomare 2020 | DOĞRU |
| 3 | Hu 2019 rakamlar | DOĞRU |
| 4 | Hu 2019 "doz-yanıt" | DOĞRULANAMADI |
| 5 | Hill 2020 | DOĞRU |
| 6 | Dyrbye 2021 "%35" | KISMEN |
| 7 | Scott 2015 | KISMEN |
| 8 | Rowland 2010 | DOĞRU |
| 9 | Baniulyte 2023 | DOĞRU |
| 10 | Reknes 2016 | DOĞRU (yorum abartılı) |
| 11 | Nielsen 2017 | DOĞRU (yorum abartılı) |
| 12 | CDHA 2018 | DOĞRU |
| 13 | 2025/3 Genelge | DOĞRU |
| 14 | Williams ve Tiedens 2016 | KISMEN |
| 15 | ten Cate ve Chen 2020 | KISMEN |
| 16 | Kennedy 2008 | DOĞRU |
| 17 | Çolak 2026 | DOĞRU |
| 18 | McCarthy ve McEvoy 2015 | DOĞRU |

Toplam: 13 DOĞRU, 4 KISMEN, 0 YANLIŞ, 1 DOĞRULANAMADI. Uydurma atıf yok.

---

## Raporu okuyanların bilmesi gereken kritik düzeltmeler

1. **Atıflar sağlam, uydurma yok.** 18 kontrolün hiçbirinde yazar/yıl/dergi uyuşmazlığı çıkmadı. Brifteki iki dergi düzeltmesi (Scott → MJA, Rowland → Int Dent J) doğru.

2. **Genelge artık birincil kaynaktan doğrulandı.** 2025/3 sayılı Genelge, RG 06.03.2025, sayı 32833. Son cümlesi: "2011/2 sayılı Genelge yürürlükten kaldırılmıştır." Başvuru yolları tam olarak: kurum, CİMER, TBMM Dilekçe Komisyonu, ALO 170 / ÇSGB, TİHEK, Kamu Denetçiliği Kurumu. ALO 170'te psikolog desteği var. Uyarı: Genelge idari talimat. Özel aile kliniğinde bağlayıcı yükümlülük asıl olarak TBK md. 417'den gelir. Kamu Denetçiliği Kurumu özel klinik için kanal değildir (bu iki nokta uzman bilgisi; bu oturumda ayrıca doğrulanmadı).

3. **"Backlash küçük" yanlış genelleme.** Williams ve Tiedens'te sevilirlik cezası küçük (d=−0,19; açık baskınlıkta −0,28). Ama **işe alınabilirlik cezası d=−0,58**, orta büyüklükte. Kullanıcı kadınsa, iş görüşmesi ve ortaklık/terfi gibi kararlarda açık baskınlığın bedeli daha yüksek olabilir. Aşırı düzeltme uyarısı bu yüzden güçlendirilmeli; örtük yetkinlik sinyalleri önerisi yerinde.

4. **Dyrbye "%35 daha yüksek olasılık" ifadesi düzeltilmeli.** Bu bir odds oranı (OR 1,35) ve yalnız **bir kez** kötü muamele görenler için. Birden çok kez görenlerde OR 1,87. Asıl mesaj doz-yanıt: ne kadar sık, o kadar çok pişmanlık.

5. **Scott: "yarıya yakını faydalı buldu" abartılı.** Doğrusu %30–50. Ayrıca %74 ve %83,6 yalnız erişkin rotasyonları; pediatride %28,8 ve %45,1. Yani aynı öğrenciler bölüme göre çok farklı muamele görmüş. Bu, "kurum/bölüm kültürü belirleyici" mesajını aslında güçlendiriyor.

6. **"Nezaket risk faktörü değil" cümlesi kanıtın ötesinde.** Nielsen 2017'de uyumluluk özelliği tacizle hafif ters ilişkili (r=−0,17, varyansın yaklaşık %3'ü), kesitsel ve iki yönlü. Uyumluluk kişilik özelliği; nazik davranışla aynı şey değil. En güçlü ilişki nevrotiklikte (r=0,25). Doğru ifade: "Nezaketin risk faktörü olduğuna dair kanıt yok. Ama nezaket kötü niyetli kişiyi durdurmaya da yetmiyor." Kullanıcının asıl kontrol alanı, kaygılı/belirsiz görünmeyi azaltan yapı ve netlik.

7. **"Yoğun kötü muamelede hiçbir bireysel strateji yetmez" cümlesi fazla geniş.** Reknes 2016 yalnız bir genel başa çıkma tarzını ve yalnız kaygı sonucunu test etti, hemşirelerde. Belgeleme, müttefik, kurumsal kanal, yer değiştirme gibi yapısal adımlar test edilmedi. Bu adımları önermek mantıklı ama kanıt düzeyi **uzman görüşü**.

8. **Hu 2019 "basamak basamak artış" doğrulanamadı.** Özet yalnız "ayda birkaç kez ve üstü" ile "hiç" karşılaştırmasını veriyor (tükenmişlik OR 2,94). Kesitsel; neden-sonuç yok. Ayrıca %30,3 istismar ve %10,3 cinsel taciz **tüm asistanlar** için; kadınlarda cinsel taciz %19,9.

9. **ten Cate ve Chen'in kanıt düzeyi düşürülmeli.** "Sistematik derleme" değil, 13 anahtar nitel çalışmanın tematik sentezi. Beş özellik doğru. "Yetenek önkoşul" ve "güvenilirlik neredeyse tüm çalışmalarda" iddiaları doğrulanamadı.

10. **Yaygınlık rakamlarını "kesin" okumayın.** Bahji'de I²=%99,96; Çolak'ta %99,3 geniş tanımdan geliyor (yazarlar da söylüyor); Baniulyte ve CDHA kendi seçen örneklemler (CDHA yanıt %22). Doğru okuma: "kötü muamele sağlık eğitiminde yaygın", rakam değil.

11. **Doğrulama sınırı.** Bu turda web arama kotası doldu. Doğrulama, bilinen kayıtların doğrudan çekilmesiyle yapıldı. 2020 sonrası CDHA tekrarı, Türkiye'de DUS asistanlarına özgü mobbing verisi ve TBK md. 417 metni bu oturumda ayrıca aranamadı. Daha fazla bağımsız arama gerekirse kullanıcı takip mesajıyla devam ettirebilir.
