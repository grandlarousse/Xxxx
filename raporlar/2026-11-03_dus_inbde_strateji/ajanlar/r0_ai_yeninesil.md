# R0 – Yapay zekâ araçları ve yeni nesil platformlar

**Tarih:** 3 Kasım 2026 · **Boyut:** LLM'lerin DUS/TUS/INBDE performansı, AI ile çalışmanın kanıta dayalı ve riskli kullanımları, Türkiye'deki yeni nesil/AI'lı DUS uygulamaları, aralıklı tekrar araçları, uluslararası hazırlık yaklaşımları, somut iş akışı.

**Etiketler:** [hakemli] hakemli dergi · [ön baskı] hakemsiz arXiv · [resmi] kurum belgesi · [satıcı iddiası] firma beyanı · [topluluk anekdotu] App Store yorumu, forum · [analiz] bu ajanın çıkarımı · [doğrulanamadı] birincil metne ulaşılamadı.

**Yöntem notu:** Bu ajan başladığında tüm ajanların paylaştığı web arama bütçesi bitmişti. WebSearch hiç kullanılamadı. Çalışma şu kanallardan yürütüldü:
- DOI/PMID ile doğrudan kayıt okuma: Crossref, OpenAlex, Europe PMC makale uç noktası.
- Yayıncı ve PMC sayfaları.
- Başkan ve ark. 2026 (PLOS ONE) makalesinin kaynakçasından kartopu yöntemi.
- Kardeş ajanların indirdiği App Store sayfalarında görünen bağlantılı uygulama sayfaları.

Arama motoru sorgusu yapılmadı. Bu yüzden Türkçe Anki desteleri, X/Ekşi yorumları ve yeni AI platformlarının tam listesi gibi tarama gerektiren konular eksik kaldı. Bunlar §8'de açık soru olarak duruyor. DUS takvimini 1 numaralı ajan doğruluyor. Bu dosya 2027 DUS'u (24 Ekim 2027, tek oturum) **doğrulanmamış** kabul ediyor.

---

## 0. Yönetici özeti

1. **Güncel LLM'ler geçmiş DUS sorularında kullanıcının çok üstünde.** Ancak bu sonuç kısmen "ezber" olabilir. 2025–2026 çalışmalarında en iyi modeller Türkçe DUS sorularında %80–98 doğruluk aldı:
   - o1 ve Gemini 2.0 Advanced: 2020–21 DUS'ta yaklaşık %97,5–97,9.
   - Gemini 2.5 Pro: endodontide %90,6.
   - Grok-4: ortodontide %86,8.

   Kullanıcının 120 soruda 61 neti, boş ve yanlış dağılımına göre yaklaşık %51–61 doğru oranına karşılık geliyor. Öte yandan sorular 2012–2021 arasında kamuya açık. Bu yüzden yazarlar eğitim verisine sızma (kontaminasyon) uyarısı yapıyor. [hakemli + analiz]
2. **Model ve branş farkı çok büyük.** Aynı modelin skoru çalışmadan çalışmaya da değişiyor:
   - ChatGPT-4o endodontide bir çalışmada %61,4, başka bir çalışmada %82,8 aldı.
   - Gemini, protetikte %46,1'de kaldı.
   - Gemini 1.5 Flash endodontide %57 aldı.

   "AI'a sor" dediğimizde hangi modelin, hangi sürümün kullanıldığı sonucu belirliyor. [hakemli]
3. **Görselli sorular zayıf nokta olmaya devam ediyor.**
   - Ortodontinin görselli sorularında ChatGPT-4o ve Gemini 2.5 Pro %45,5, Grok-4 %63,6 aldı.
   - 2020–21 DUS'taki 7 görselli soruda GPT-4 3/7 bildi. Gemini Advanced hiçbirini bilemedi.
   - Görselli sorularda öğrenmek için AI açıklamasına güvenilmemeli. [hakemli]
4. **Türkçe cezası küçük ama gerçek.** GPT-4o 1.504 DUS sorusunda İngilizcede %87,8, Türkçede %84,0 aldı (p<0,001). Çok ülkeli meta-analizde GPT-4, İngilizce konuşulan ülkelerin sınavlarında daha iyiydi. [hakemli]
5. **INBDE tarzı sorularda eski modellerin hata oranı hâlâ yüksekti.**
   - INBDE Bootcamp, ITDOnline ve JCNDE sorularında GPT-4 %76,9, GPT-3.5 %61,3 aldı.
   - INBDE'nin vaka sorularında başarı %66–69'du.
   - Bootcamp AI ve Booster AI gibi asistanların "anında doğru cevap" iddiası bağımsız olarak doğrulanmadı. [hakemli + satıcı iddiası]
6. **AI öğrenmeyi hem hızlandırabilir hem de zayıflatabilir.** Belirleyici olan araç değil, kullanım biçimi.
   - Türkiye'de yaklaşık 1.000 lise öğrencisiyle yapılan RCT'de serbest GPT-4 pratikte notları %48 artırdı. Erişim kalkınca performans kontrol grubunun %17 altına düştü. İpucu veren, cevabı söylemeyen "GPT Tutor" bu zararı büyük ölçüde önledi.
   - Harvard'daki RCT'de yapılandırılmış AI öğretmen anlık testte 0,63 SD üstünlük sağladı. Gecikmeli bellek testi yapılmadı. [hakemli]
7. **"Yerine koyma" ile "tamamlama" farklı sonuç veriyor.** LLM'i çözüm ürettirmek için kullananlar daha çok konu gördü ama her konuyu daha az anladı. Açıklama için kullananlar daha derin anladı. Bu bulgu ön baskı düzeyinde. AI'a duyulan güven arttıkça eleştirel düşünme azalıyor (CHI 2025, 319 kişi). [ön baskı + hakemli]
8. **AI ile soru üretmek mümkün ama ayıklama şart.** Türk diş hekimliği öğrencileriyle yapılan çalışmada ChatGPT-4'ün ürettiği soruların %44'ü şu nedenlerle elendi:
   - zayıf çeldirici,
   - tekrar,
   - yanlılık,
   - olgu hatası.

   Elemeyi geçenler, eğitmen sorularıyla benzer zorlukta ve ayırt edicilikteydi. [hakemli]
9. **Kaynağa dayalı (RAG) kullanım doğruluğu artırıyor.** ChatGPT-4 ABD protetik sınavında temel modelle %62,7, kaynaklarla ince ayar yapıldığında %73,6 aldı. NotebookLM yapısı Kasım 2026'da Google yardım sayfasında "Gemini Notebook" adıyla geçiyor ve yanıtları yüklenen kaynaklara satır içi alıntıyla bağlıyor. [hakemli + resmi/satıcı]
10. **Türkiye'de 2025–2026'da çok sayıda küçük, yeni nesil DUS uygulaması çıktı.** Bunlar arasında DUSPort, DUS PRİME, DusNote, DUS Club, Dentomino, Soru Bang ve TUSDATA'nın EasyDUS'u var.
    - Hiçbiri bağımsız doğruluk ya da sonuç verisi yayımlamıyor.
    - DusNote'ta bir kullanıcı içeriğin "yapay zekâ anlatımı olduğunun çok belli" olduğunu ve "doğruluğunun kesin olmadığını" yazmış.
    - AI ile üretilmiş Türkçe soru bankaları uzman denetimi olmadan risklidir. [satıcı iddiası + topluluk anekdotu]
11. **Anki'nin kendi kanıtı gözlemsel, ama araç olgun.** FSRS (Anki 23.10+) ve yerleşik görsel kapatma (Image Occlusion) DUS'a doğrudan uyarlanabilir. USMLE'de yaklaşık 1.700 benzersiz kart yaklaşık 1 puanla ilişkili bulundu. Bu çalışma gözlemsel. Herkese açık, kalitesi bilinen bir Türkçe DUS Anki destesi bu turda **doğrulanamadı**. [resmi + hakemli]
12. **Sık atıf alan olumlu bir ChatGPT meta-analizi geri çekildi.** Wang & Fan 2025 (g=0,867) "RETRACTED" durumda. "AI öğrenmeyi büyük ölçüde artırır" iddiasının önemli bir dayanağı düştü. [resmi kayıt]

---

## 1. (a) LLM'lerin diş hekimliği sınavlarındaki performansı (2023–2026)

### 1.1 DUS ve TUS çalışmaları (hepsi [hakemli])

| Çalışma | Soru seti | Modeller ve doğruluk | Önemli not |
|---|---|---|---|
| Kinikoglu 2025, *Cureus* ([DOI](https://doi.org/10.7759/cureus.77292)) | DUS 2020+2021, 238 soru (Türkçe, görseller platforma yüklendi) | o1 **%97,46**, Gemini 2.0 Adv **%97,90**, Gemini 1.5 Pro %91,60, GPT-4o %88,66 | 2021'deki 6 görselli soruda GPT-4o 4 hata yaptı. o1 ve Gemini 2.0 birer hata yaptı |
| Sismanoglu & Capan 2025, *BMC Med Educ* ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11809121/)) | DUS 2020+2021, Türkçe | GPT-4.0 %83,3 / %80,5. Gemini Adv %65 / %60,2 | Makalenin DUS puanı hesabında GPT-4 65,5 / 65,6 aldı, yıl birincisi 68,5 / 72,3 aldı. 7 görselli soruda GPT-4 3/7 bildi, Gemini 0/7 (3'ü boş). En zayıf branşlar endodonti (%45/%50) ve ortodonti |
| Dündar Sarı & Sezer 2025, *Essentials of Dentistry* ([Avesis](https://avesis.comu.edu.tr/yayin/f7645273-4ebe-4e29-818d-713fa9e096f8/chatgpt-4-omnis-accuracy-in-multiple-choice-dentistry-questions-a-multidisciplinary-and-bilingual-assessment)) | DUS 2012–2021, 1.504 soru, TR ve EN | GPT-4o EN **%87,8**, TR **%84,0** (p<0,001) | Anatomi, fizyoloji, periodontoloji, endodonti ve pedodontide İngilizce daha iyiydi. Radyolojide Türkçe daha iyiydi |
| Başkan ve ark. 2026, *PLOS ONE* ([makale](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0350457)) | 127 endodonti sorusu, 2012–2021, Türkçe | Gemini 2.5 Pro **%90,6**, Grok 4 %84,3, Claude 4 %83,5, DeepSeek V3 %82,7, ChatGPT-5 %78,7, Perplexity %77,2, LLaMA 4 %71,7, GPT-4o **%61,4** | Yazarlar kontaminasyon, tek sorgu, web arayüzü ve sıcaklık kontrolü olmaması gibi sınırlılıkları açıkça yazıyor |
| Turan Gökduman ve ark. 2025, *BMC Oral Health* ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12781317/)) | 122 endodonti sorusu, 2012–2021 | GPT-4o %82,8, Gemini Adv %83,6, Claude %82,8, Copilot %77,9 | Copilot ve Claude 2012–2015 sorularında 2016–2021'e göre anlamlı derecede daha başarılıydı |
| Çekiç & Tavşan 2025, *BMC Med Educ* ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12492805/)) | 151 endodonti sorusu, Türkçe, 8 LLM | En yüksek GPT-4o **%81,5**, en düşük Gemini 1.5 Flash **%57** | Kombinasyon tipi sorularda ("hangileri doğru") başarı düşüyor |
| Özden & Erener 2026, *Lokman Hekim Health Sci* ([Avesis](https://avesis.inonu.edu.tr/yayin/9967045f-41fe-4913-8e63-0c766e68d295/comparative-evaluation-of-chatgpt-4o-gemini-2-5-pro-and-grok-4-in-answering-orthodontics-questions-from-the-dentistry-specialty-examination)) | 129 ortodonti sorusu, 13 oturum | Grok-4 %86,8, Gemini 2.5 Pro %82,9, GPT-4o %78,3 | **Görselli sorular:** %45,5 / %45,5 / %63,6. **2018 DUS'ta** tüm modeller %30–50'ye düştü |
| Tosun & Yilmaz 2025, *J Dent Sci* ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12254736/)) | 128 protetik sorusu | En yüksek GPT-4 %75,8, en düşük Gemini **%46,1** (yanlışı doğrusundan fazla) | Vaka sorularında bilgi sorularına göre daha zayıf |
| Eraslan ve ark. 2025, *BMC Med Educ* ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11869545/)) | 126 protetik sorusu (İngilizceye çevrildi) | Copilot %73, Gemini %63,5, GPT-3.5 %61,1, Claude Pro %57,9, Perplexity %54,8 | Hareketli bölümlü protezde başarı en düşük (%50,8) |
| Yilmaz ve ark. 2025, *BMC Oral Health* ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11998383/)) | 100 oral patoloji sorusu | o1 96, Claude 3.5 84, Gemini 2 82, DeepSeek 82, Gemini 1.5 81, GPT-4o 79, GPT-4 69, Copilot 61 | Görselli soru test edilmedi |
| Öztermeli & Öztermeli 2023, *Medicine* ([DOI](https://doi.org/10.1097/MD.0000000000034673)) | TUS, 5 oturum, 1.177 soru | GPT-3.5 %54,3–70,9 | En iyi oturumda 22.214 aday arasında 1.787. sıraya denk geldi |

### 1.2 INBDE / ABD ve diğer ülkeler

| Çalışma | Soru seti | Sonuç |
|---|---|---|
| Danesh ve ark. 2023, *JADA* ([PubMed](https://pubmed.ncbi.nlm.nih.gov/37676187/)) [hakemli] | **INBDE Bootcamp**, ITDOnline ve JCNDE örnek soruları. Görselliler çıkarıldı. 3 deneme ortalaması | GPT-3.5 **%61,3**, GPT-4 **%76,9**. Yazarlar ChatGPT'nin "ana kaynak değil, tamamlayıcı" olarak kullanılmasını öneriyor |
| Dashti ve ark. 2024, *Imaging Sci Dent* ([DOI](https://doi.org/10.5624/isd.20240037)) [hakemli] | 49 INBDE, 80 ADAT, 124 DAT sorusu. Görselliler çıkarıldı | INBDE bilgi sorularında iki model de %80. Vaka sorularında %66 (3.5) ve %69 (4) |
| Chau ve ark. 2024, *Int Dent J* ([DOI](https://doi.org/10.1016/j.identj.2023.12.007)) [hakemli] | ABD ve İngiltere lisans soru kitaplarından 1.461 soru | GPT-4 ABD %80,7, İngiltere %62,7 (ikisini de geçti). GPT-3.5 %68,3 ve %43,3 (kaldı) |
| Danesh ve ark. 2024, *J Periodontol* ([PubMed](https://pubmed.ncbi.nlm.nih.gov/38197146/)); Sabri ve ark. 2024, *J Periodontal Res* ([DOI](https://doi.org/10.1111/jre.13323)) [hakemli] | AAP in-service sınavı | GPT-4 %73,6 (311 soru). Diğer çalışmada GPT-4 %79,6 (1.312 soru) ile asistanları geçti |
| Chan-Chia Lin ve ark. 2025, *J Dent Sci* ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12485390/)) [hakemli] | Tayvan lisans sınavı, 2.699 soru (Çince) | Claude2 %54,9, GPT-3.5 %49,3, Gemini %44,6. Hiçbiri geçemedi. Eski modeller, İngilizce dışı dil |
| Liu ve ark. 2024, *JMIR* meta-analizi ([DOI](https://doi.org/10.2196/60807)) [hakemli] | 45 çalışma, tıp lisans sınavları | GPT-4 genel %81 (%95 GA 78–84), GPT-3.5 %58. GPT-4 İngilizce konuşulan ülkelerin sınavlarında daha iyi (p=0,02) |
| Özbay ve ark. 2025, *BMC Oral Health* ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12039063/)) [hakemli] | 40 açık uçlu endodonti sorusu | En düşük yanlış bilgi oranı GPT-4'te. **Tüm modeller** değişen oranlarda eksik ya da yanlış yanıt verdi |

### 1.3 Yorum [analiz]

- **Kullanıcı açısından:** Bugünün üst düzey modelleri DUS'taki bilgi sorularının büyük çoğunluğunda kullanıcıdan daha isabetli. Açıklayıcı olarak işe yararlar. Ama %3–20 hata oranı, branşa göre %40–50'ye çıkan dilimler (görselli, vaka, kombinasyon tipi) ve model farkları var. Bu yüzden doğrulanmadan "öğretmen" olamazlar.
- **Kontaminasyon:** Tüm DUS çalışmaları 2012–2021 sorularını kullandı ve bu sorular kamuya açık. 2022–2026 sorularıyla, yani eğitim verisinde olmama ihtimali yüksek sorularla yapılmış bir çalışma bulunamadı. Turan Gökduman'da eski yılların daha iyi yapılması ezber hipotezine uyuyor. Ama sınavın zamanla değişmesi de aynı sonucu doğurabilir.
- **Triaj için çıkarım:** Bazı oturumlarda, örneğin 2018 ortodontide, en iyi modeller bile %30–50'de kaldı. Bu, ÖSYM'nin bazı oturumlarda standart uluslararası bilginin dışına çıkan, kitaba özgü ya da belirsiz sorular sorduğunu düşündürüyor. Bu tür soruları ne dershane ne AI öngörebilir. "AI ile çıkacak konu tahmini" diye bir yöntemi destekleyen hiçbir yayın bulunamadı.
- **Görsel ağırlığı:** Sismanoglu'na göre 2 yılda yalnızca 7 görselli soru vardı. AI'ın görsel zayıflığı toplam puan açısından küçük, ama radyoloji ve ortodonti öğrenimi açısından önemli.

---

## 2. (b) AI ile çalışma: kanıta dayalı ve riskli kullanımlar

### 2.1 Öğrenme çıktısına etki: kanıt tablosu

| Çalışma | Tasarım | Bulgu | Etiket |
|---|---|---|---|
| Bastani ve ark. 2025, *PNAS* ([DOI](https://doi.org/10.1073/pnas.2422633122), [Wharton özeti](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education)) | Türkiye, yaklaşık 1.000 lise öğrencisi, saha deneyi | GPT Base pratikte notları %48 artırdı, GPT Tutor %127 artırdı. Erişim kalkınca GPT Base grubu kontrolden **%17 daha kötü** yaptı. İpuçlu ve cevapsız GPT Tutor zararı büyük ölçüde önledi. Öğrenciler GPT'yi "koltuk değneği" olarak kullandı | [hakemli] |
| Kestin ve ark. 2025, *Sci Rep* ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)) | Harvard fizik, çapraz RCT, N=194 | AI öğretmen, sınıf içi aktif öğrenmeye göre 0,63 SD üstündü (kantil regresyonla 0,73–1,3). Medyan süre 49 dk, sınıfta 60 dk. **Gecikmeli test yok.** Hazır yazılmış çözümlere dayanıyor | [hakemli] |
| Lehmann, Cornelius, Sting 2024/25 ([arXiv](https://arxiv.org/abs/2409.09047)) | Ön kayıtlı 2 laboratuvar deneyi ve saha | Genel etki yok. LLM'i **yerine koyanlar** (çözüm ürettirenler) daha çok konu gördü ama daha az anladı. **Tamamlayanlar** (açıklama isteyenler) daha iyi anladı. Ön bilgi farkını büyütüyor | [ön baskı] |
| Lee ve ark. 2025, *CHI* ([DOI](https://doi.org/10.1145/3706598.3713778)) | 319 bilgi çalışanı anketi | GenAI'a güven arttıkça eleştirel düşünme azalıyor. Kendine güven arttıkça artıyor | [hakemli, öz bildirim] |
| Gerlich 2025, *Societies* ([DOI](https://doi.org/10.3390/soc15010006)) | 666 katılımcı, karma yöntem | Sık AI kullanımı ile eleştirel düşünme arasında negatif ilişki var. Aracı değişken bilişsel yükün dışarı aktarılması (offloading) | [hakemli, korelasyonel] |
| Kosmyna ve ark. 2025 ([arXiv](https://arxiv.org/abs/2506.08872)) | Kompozisyon yazma, EEG, n=54 | LLM grubunda nöral bağlantısallık en zayıftı. Katılımcılar kendi metinlerinden alıntı yapmakta zorlandı | [ön baskı, küçük örneklem] |
| Wang & Fan 2025, *HSSC* ([DOI](https://doi.org/10.1057/s41599-025-04787-y)) | Meta-analiz, g=0,867 | **GERİ ÇEKİLDİ** (OpenAlex: is_retracted=true). Kanıt olarak kullanılmamalı | [resmi kayıt] |
| Deng ve ark. 2025, *Computers & Education* ([DOI](https://doi.org/10.1016/j.compedu.2024.105224)) | ChatGPT deneylerinin meta-analizi | Künye doğrulandı. Özete erişilemedi, etki büyüklükleri **doğrulanamadı** | [hakemli, içerik doğrulanamadı] |

### 2.2 AI ile soru ve kart üretimi

| Çalışma | Bulgu | Etiket |
|---|---|---|
| Özer ve ark. 2025, *Eur J Dent Educ* ([DOI](https://doi.org/10.1111/eje.70034)) | Oral diagnoz-radyoloji dersi. ChatGPT-4 30 dakikada 36 soru üretti. **%44'ü elendi** (zayıf çeldirici, tekrar, yanlılık, olgu hatası). Kalan 20 soru, eğitmenin sorularıyla benzer zorlukta (0,42'ye karşı 0,41) ve ayırt edicilikteydi (0,32'ye karşı 0,30) | [hakemli] |
| Laupichler ve ark. 2024, *Acad Med* ([DOI](https://doi.org/10.1097/ACM.0000000000005626)) | LLM sorularının ayırt ediciliği insan sorularından düşük (0,24'e karşı 0,36). Zorluk benzer | [hakemli] |
| Cheung ve ark. 2023, *PLOS ONE* ([DOI](https://doi.org/10.1371/journal.pone.0290691)) | Ders kitabına dayalı 50 soru. Kalite insanla benzer, yalnızca "ilgililik" alanında AI düşük. Hazırlık süresi 20 dk'ya karşı 211 dk | [hakemli] |
| Kıyak & Emekli 2024, *Postgrad Med J* ([DOI](https://doi.org/10.1093/postmj/qgae065)) | 23 çalışmanın derlemesi. Doğruluk karışık. "Uzman incelemesi olmadan kullanmayın" | [hakemli derleme] |
| Dashti ve ark. 2025, *BMC Med Educ* ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12102979/)) | ABD protetik sınavı: temel GPT-4 %62,7, kaynaklarla ince ayarlı model %73,6 | [hakemli] |
| Tozuka ve ark. 2024, *Jpn J Radiol* ([DOI](https://doi.org/10.1007/s11604-024-01705-1)) | NotebookLM'in (RAG) akciğer kanseri evrelemesinde kullanımı. Künye doğrulandı, **özete erişilemedi** | [hakemli, içerik doğrulanamadı] |

LLM'le **Anki kartı** üretiminin öğrenme etkisini ölçen hakemli bir çalışma bu turda bulunamadı. Soru üretimi verisi kart için de "ayıklama şart" sonucuna işaret ediyor. [analiz]

### 2.3 Kullanım matrisi

| Kullanım | Kanıt yönü | Ana risk | Kontrol |
|---|---|---|---|
| **Kendi denemenden sonra yanlış cevabı açıklatmak** | Olumlu. Tamamlayıcı kullanım (Lehmann, Kestin) | Halüsinasyon, özellikle sayılar ve sınıflamalar | Kitapla doğrula. Model "emin değilim" diyebilsin. Çelişki varsa ikinci model |
| **Sokratik / öğretici mod** | Olumlu (Bastani GPT Tutor, Kestin) | Kullanıcı modu kapatıp cevaba atlayabilir | Claude "learning mode" (2 Nisan 2025) ([Anthropic](https://www.anthropic.com/news/introducing-claude-for-education)) [resmi]. Gemini "Guided Learning" (6 Ağustos 2025) ([Google](https://blog.google/outreach-initiatives/education/guided-learning/)) [resmi]. ChatGPT "study mode" ([OpenAI](https://openai.com/index/chatgpt-study-mode/)): sayfa 403 döndü, **doğrulanamadı** |
| **Cevabı önce AI'a sormak, kendin denememek** | **Olumsuz** (Bastani'de −%17) | Koltuk değneği. Akıcılık yanılsaması | Kural: soru, AI kapalıyken çözülür |
| **Notlardan soru ürettirmek** | Karışık (Özer'de %44 elendi) | Yanlış anahtar, zayıf çeldirici | Yalnızca kendi kaynağından (RAG) ürettir. Kaynak alıntısı iste. Şüpheliyi at |
| **Anki kartı ürettirmek** | Doğrudan kanıt yok | Hatalı ve şişkin deste | Kartı kendin yaz. AI sadece biçimi eleştirsin ya da cloze'a çevirsin. Hata başına 1–3 kart |
| **NotebookLM / Gemini Notebook** | RAG doğruluğu artırıyor (Dashti 2025) | Alıntı yanlış yere işaret edebilir. Telif ve gizlilik | Alıntıya tıklayıp doğrula. Dershane PDF'lerini yüklemeden önce kullanım şartlarına bak |
| **Hata defteri analizi** | Doğrudan kanıt yok. Düşük risk | Model örüntü uydurabilir | Ham sayımları sen yap (pivot), yorumu AI'a sor |
| **Çalışma planı** | Kanıt yok | Plan gerçek dışı olabilir | Takvimi ÖSYM kılavuzundan, yükü kendi verinden belirle |
| **Görselli soru öğrenmek** | Olumsuz (%45–64) | Yanlış görsel yorum | AI kullanma. Atlas ve kitap kullan |
| **"Çıkacak konu" tahmini** | Kanıt yok | Yanlış güven, kapsam kaybı | Kullanma |

---

## 3. (c) Türkiye'de yeni nesil ve AI'lı DUS platformları (2024–2026)

Kaynak: App Store TR sayfaları, 3 Kasım 2026'da okundu. Tümü [satıcı iddiası]. Yorumlar [topluluk anekdotu].

| Uygulama (geliştirici) | Satıcının söylediği | AI iddiası | Puan (oy) | Dikkat çeken yorum/not |
|---|---|---|---|---|
| **EasyDUS** (TUSDATA A.Ş.) ([link](https://apps.apple.com/tr/app/easydus/id6757461997)) | "Yapay zekâ destekli eğitim asistanı": soru üretme, anlık yanıt, akıllı sohbet | Evet | Yeterli oy yok | Doğruluk verisi yok. DUSDATA ekosisteminin AI denemesi |
| **DusNote** (Göktuğ Yersel) ([link](https://apps.apple.com/tr/app/dusnote/id6757265879)) | 14 derste 13.000+ soru, spot bilgi, flashcard, hata bankası, düello | Evet: Premium'da "AI Asistan", günde 10 soru (sürüm 3.0) | 4,5 (18) | "Hepsinin yapay zekâ anlatımı olduğu çok belli ve bilgilerin doğruluğu kesin değil… doğru bilgiler ders kitaplarından alınarak eklenmeli" |
| **DUSPort** (Derya Ortaç) ([link](https://apps.apple.com/tr/app/dusport/id6756510967)) | 15 derste 1.700+ soru, açıklamalı. Zorluk seviyeleri, PvP düello, XP, yanlış analizi | Yok | 4,7 (242) | Olumlu: tekrar sayısı ve yanlış takibi. Olumsuz: ücretliye geçiş tepkisi (Eylül 2026) |
| **DUS PRİME** (Yusuf F. Taşkın) ([link](https://apps.apple.com/tr/app/dus-pri-me/id6800597533)) | 10.000+ DUS/TUS sorusu, konu PDF'leri, "hafıza algoritmalarıyla optimize" kartlar, canlı çalışma odaları | Belirsiz | 4,7 (25) | 2026 yaz ve sonbaharında sık sürüm. Sorular kimin yazdığı belirsiz |
| **DUS Club** (Oğuzhan Arslan) ([link](https://apps.apple.com/tr/app/dus-club-dusa-haz%C4%B1rl%C4%B1k/id6756817138)) | Pomodoro kronometre, soru havuzu, yanlış defteri, kendi ve **topluluk** flashcard'ları, çalışma ekibi | Yok | 4,8 (25) | "Soru sayısı az geldi". Topluluk kartlarının kalitesi denetlenmiyor olabilir |
| **Dentomino** (Emir Balaban) ([link](https://apps.apple.com/tr/app/dentomino/id6796009719)) | Öğren modu, "CaseStream" vaka, vaka odası | Yok | 3,0 (2) | Çok yeni |
| **Soru Bang** (Münirhan Kaynak) ([link](https://apps.apple.com/tr/app/soru-bang/id6771569353)) | Yanlış soruları fotoğraflayıp arşivleme. Aylık tekrar seansı, 3 gün–1 ay hatırlatma | Yok | 5,0 (1) | Kâğıt hata defterini dijitalleştirmek için uygun |
| **TML** (TML Eğitim) ([link](https://apps.apple.com/tr/app/id1483926334)) | "Hızlı tekrar kartları". Az bilinen kart daha sık geliyor (Leitner benzeri). Ders bazlı eksik grafiği | Yok | 4,1 (89) | Kurum içeriği |
| **DUS Master** (Ahmet Ay) ([link](https://apps.apple.com/us/app/dus-master/id6474985706)) | Kronometre, takvim, çalışma grupları, tercih simülasyonu | Yok | 4,8 (231) | 2025 yorumu: geliştirici "puan düşük" diye kapatmayı tartışmış. Süreklilik riski |
| **Quadro Analyse** (TUSDATA) ([link](https://apps.apple.com/tr/app/quadro-analyse/id6804218697)) | Deneme sonuçlarını soru soru ve branş branş analiz | Yok | Oy yok | Yalnızca kendi denemeleri için |
| **My DUSDATA** ([link](https://apps.apple.com/tr/app/my-dusdata/id1510360764)) | Kursiyer soru bankası | Yok | 3,6 (94) | "Ne soruların altında açıklama var ne hangi soruyu çözdüğün belli" (2025) |
| DUSTIME 3,3 (67), Dentomy 2,5 (2), Tıp Akademisi 1,6 (20) | Video ve deneme | Yok | — | Video ve ses senkronu, eksik video şikâyetleri |
| Dus Akademisi "ÇÇDS App" | — | — | — | Sitede "Yakında" ([ÇÇDS sayfası](https://dusakademisi.com/egitim-setleri/ccds-ckms-soru-cozum-paketi-dus-tus-eus-14-brans)) |
| Seduss | "AI ile kişiselleştirilmiş test" | ? | — | Site erişilemedi. Kardeş ajanın notuna göre **doğrulanamadı** |

**Gözlemler [analiz]:**
- Pazarın yeni nesil kısmı 2025–2026'da büyük ölçüde bireysel geliştiricilerin oyunlaştırılmış soru ve kart uygulamalarından oluşuyor. Geliştiricilerin bir kısmının diş hekimi olduğu anlaşılıyor.
- "AI destekli" etiketi taşıyan iki ürünün (EasyDUS, DusNote AI Asistan) yayımlanmış bir doğruluk testi yok.
- AI ile üretildiği izlenimi veren Türkçe açıklamalar §1'deki hata oranlarını miras alır. Model yanıtı tek seferlik ve denetimsizse, branşa göre %10–40 hatalı açıklama beklenebilir. Bu bir çıkarım, ölçülmedi.
- **Türkçe Anki destesi:** Herkese açık ve kalitesi bilinen bir DUS destesi bulunamadı. Kardeş ajan da bulamadı. AnkiWeb'de tarama yapılamadı. Uygulama içi kart sistemleri (DUS Club, DusNote, DUS PRİME, TML) var, ama dışa aktarım ve FSRS gibi özellikleri yok ya da doğrulanamadı.

---

## 4. (d) Aralıklı tekrar ve soru bankası araçları

| Araç | Nitelik | Kaynak |
|---|---|---|
| **Anki** | Masaüstü, AnkiDroid ve AnkiWeb ücretsiz. **FSRS** Anki 23.10+ ile geliyor (AnkiDroid'de 2.17'den itibaren). Hedef hatırlama varsayılanı %90. Kılavuz %97'nin üstünü önermiyor. Optimizasyon için birkaç yüz tekrar gerekiyor. **Görsel kapatma** 23.10+ ile yerleşik ("hepsini gizle, birini sor"). Cloze, iç içe cloze | [resmi] [Deck options](https://docs.ankiweb.net/deck-options.html), [Editing](https://docs.ankiweb.net/editing.html) |
| **RemNote** | PDF üzerine not, tek tıkla AI kart ve test, AI Tutor Chat, sınav tarihi planlayıcı. Algoritma adı verilmiyor. Ücretsiz planda kart ve PDF notu var | [satıcı iddiası] [remnote.com](https://www.remnote.com/) |
| **Quizlet** | Bu turda incelenmedi | — |
| **Soru bankası ve Anki kanıtı** | Deng 2015 (n=72, gözlemsel): +445 soru veya +1.700 benzersiz kart ≈ +1 Step 1 puanı ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4673073/)). Burk-Rafel 2017 (n=274): erken başlamak, ek kitap turu ve fazla soru çözmek daha yüksek puanla ilişkili (düzeltilmiş R²=0,56; [DOI](https://doi.org/10.1097/ACM.0000000000001916)). Her ikisi de nedensellik kurmuyor | [hakemli, gözlemsel] |

**DUS'a uyarlama [analiz]:**
- **Kartın kaynağı:** Yalnızca kendi yanlışların, ÖSYM çıkmışları ve kitapta "iki kez karıştırdığın" yerler. Konu kitabının tamamı karta dökülmemeli. Kitaplar zaten dolu ve kapsama değil geri çağırma eksik.
- **Kart tipleri:**
  - Sınıflamalar, sayılar ve ilaç dozları için cloze.
  - Radyoloji, anatomi, sefalometri ve histopatoloji görselleri için görsel kapatma.
  - "X ile Y'nin farkı nedir" tipi karşılaştırma kartları (karıştırma çiftleri).
- **Yük:** Günde 20–30 yeni kart, 45–60 dakikalık tekrar tavanı. Sprintin son 4 haftasında yeni kart sınırlanır.
- **Ayarlar ve etiketler:** FSRS açık, hedef hatırlama 0,90. Kartlar `branş::konu::ÖSYM_yılı` biçiminde etiketlenir.

---

## 5. (e) Uluslararası diğer hazırlık yaklaşımları ve kanıt düzeyi

| Yaklaşım | Ne biliniyor | Kanıt düzeyi |
|---|---|---|
| Kurs dışı, öğrencinin kurduğu "paralel müfredat" (soru bankası, özet kitap, kart) | USMLE'de bu davranışlar puanla ilişkili (Burk-Rafel 2017) | Orta. Gözlemsel, tek kurum [hakemli] |
| Soru bankası + Anki | Deng 2015 ve kardeş ajanın topladığı Parry 2019, Cooper 2023 (Anki'de etki yok) | Orta-düşük. Tutarsız [hakemli] |
| AI öğretmen (öğretici modda) | Kestin 2025 (anlık kazanç), Bastani 2025 (koruma bariyeri şart) | Orta. Kısa vadeli, DUS'a özgü veri yok [hakemli] |
| INBDE platformlarının AI asistanları (Bootcamp AI™ Tutor, Booster AI™) | Satıcı: "Booster AI: instant, accurate answers" ([Booster](https://boosterprep.com/inbde/upgrade), [Bootcamp](https://bootcamp.com/inbde/upgrade)). Bağımsız test yok. GPT-4 Bootcamp sorularında %76,9 aldı (Danesh 2023) | Düşük [satıcı iddiası + hakemli dolaylı] |
| Çalışma grupları, Discord, "study with me", canlı çalışma odaları | DUS Master, DUS Club ve DUS PRİME'ın bu özellikleri sunması talep olduğunu gösteriyor. Sınav puanına etkisini ölçen hakemli çalışma bu turda **bulunamadı**. Olası mekanizma hesap verebilirlik, risk zaman kaybı | Çok düşük [topluluk anekdotu + analiz] |
| Koçluk ve özel ders | Kardeş ajan: SAT koçluğunda bağımsız tasarımlarda etki küçük. DUS koçluğu için sonuç verisi yok | Düşük [hakemli dolaylı] |
| Orijinal İngilizce ders kitapları | Doğrudan kanıt yok. LLM'lerin büyük ölçüde İngilizce verilerle DUS'ta %80+ yapması, DUS bilgisinin büyük kısmının uluslararası standart bilgi olduğunu düşündürüyor. Kontaminasyon bu çıkarımı zayıflatıyor. Türkçe ÖSYM terminolojisi ayrıca çalışılmalı | Düşük [analiz] |

---

## 6. (f) Bu kullanıcı için "AI + soru bankası + aralıklı tekrar" iş akışı

**Varsayımlar:**
- Konu kitapları dolu ve 61 net var.
- Bir sonraki DUS'un 24 Ekim 2027 olduğu doğrulanmadı.
- Kardeş ajanın önerdiği 14–18 haftalık yoğun sprint esas alındı.

**Koşullu ayarlar:**
- Kullanıcı çalışıyorsa bloklar küçültülür.
- İngilizcesi iyiyse ve INBDE'ye de hazırlanıyorsa AI açıklamaları İngilizce istenebilir. Dündar Sarı'ya göre İngilizcede doğruluk yaklaşık 4 puan daha yüksek. Ama kart ve terim Türkçe kalmalı.

### 6.1 Faz 0 – Teşhis ve kalibrasyon (Kasım–Aralık 2026, 2–3 hafta)

1. **Kendi sınavının hata dökümü.** ÖSYM'nin yayımladığı 2026 kitapçıkları ve cevap anahtarıyla soru soru bir tablo hazırla. Sütunlar: branş, konu, hata türü (bilmiyordum / karıştırdım / yanlış okudum / süre / riskli tahmin), güven 1–3. *Araç:* tablo (Sheets/Excel) veya Soru Bang. *Risk kontrolü:* Sayımları AI'a yaptırma, pivotla kendin yap.
2. **AI kalibrasyon testi.** Kullanacağın modele, cevabını kesin bildiğin 50 ÖSYM sorusunu sor. Branş branş hata oranını not et. Hata oranı %10'u aşan branşta o modelin açıklamasını yalnızca kitapla birlikte kullan. *Gerekçe:* §1'de model ve branş farkı %46 ile %98 arasında. *Ek kontrol:* Aynı soruyu iki ayrı sohbette sor. Cevap değişiyorsa o konuda modele güvenme.

### 6.2 Faz 1 – Bakım (Ocak–Mayıs/Haziran 2027, düşük doz, INBDE ile paralel olabilir)

- Günde 30–45 dakika Anki (yalnızca Faz 0'daki yanlışlardan).
- Haftada 1 branş için 40–60 soruluk mini blok.
- AI yalnızca blok sonrası açıklama için.

### 6.3 Faz 2 – Sprint (14–18 hafta) günlük döngü

| Adım | Araç | Risk kontrolü |
|---|---|---|
| 1. 40–60 soruluk süreli karışık blok, AI kapalı | ÖSYM çıkmışları ya da açıklamaları insanlar tarafından yazılmış bir Türkçe soru bankası. Kullanmadan önce banka bir branşta kitapla örneklem kontrolünden geçmeli | Açıklamaları "AI kokan" ya da kaynaksız bankayı yalnızca soru kaynağı olarak kullan |
| 2. Yanlış ve şanslı doğruları kaydet | Tablo, Soru Bang ya da Anki notu | Hata türünü her zaman işaretle |
| 3. Önce kitapta doğrula | Kendi dolu konu kitabın, başvuru kaynağı olarak | Kitapla AI çelişirse ÖSYM anahtarı ve standart ders kitabı esas alınır |
| 4. AI ile Sokratik açıklama | Claude learning mode, Gemini Guided Learning ya da ChatGPT study mode. Üst düzey bir akıl yürütme modeli | Şablon P1 (aşağıda). Görselli sorularda AI yok. Sayı ve sınıflama kitaptan |
| 5. Kartı kendin yaz | Anki (FSRS 0,90, görsel kapatma) | AI yalnızca şablon P2 ile biçimi eleştirir. Hata başına en fazla 3 kart |
| 6. Günlük tekrar, 45–60 dk tavan | Anki | Tekrar birikiyorsa yeni kartı durdur |
| 7. Haftalık analiz (30 dk) | Tablonun özeti ve şablon P3 | AI'ın konu önemi yorumunu "tahmin" olarak işaretle. Konu ağırlığı için hakemli dağılım makalelerine ve ÖSYM verisine bak (kardeş ajan dosyaları) |
| 8. Kaynaklı test (isteğe bağlı) | Gemini Notebook (NotebookLM): kendi notların, hata tablosu, ÖSYM kitapçıkları | Şablon P4. Her alıntıya tıkla. Telifli dershane PDF'lerini yüklemeden önce şartları kontrol et |
| 9. Haftalık tam simülasyon (sprintin 2. yarısı) | ÖSYM formatında 120 soru, 150 dk | Simülasyondan sonraki 2–3 saati adım 2–5'e ayır |

**AI'ın payı [analiz]:** Toplam sürenin %15–20'sini geçmemeli. AI çözme süresini değil, analiz süresini kısaltmak için var.

### 6.4 İstem şablonları

- **P1 – Yanlış analizi:** "Bu DUS sorusunda ben C'yi seçtim, resmi anahtar E. Cevabı hemen söyleme. Önce bana doğru şıkka ulaşmam için en fazla 2 ipucu sorusu sor. Ben yanıtladıktan sonra her şıkkın neden doğru ya da yanlış olduğunu tek cümleyle yaz. Emin olmadığın yerde 'emin değilim' de. Hangi standart ders kitabı bölümüne bakmam gerektiğini söyle ama sayfa numarası uydurma."
- **P2 – Kart eleştirisi:** "Yazdığım Anki kartlarını yalnızca biçim açısından değerlendir: tek bilgi ilkesi, belirsizlik, cevabı ele veren ipucu. Yeni bilgi ekleme. Gerekirse cloze'a çevir."
- **P3 – Hata defteri:** "Bu tabloda (tarih, branş, konu, hata türü, güven) en sık 5 konu ve hata türü kombinasyonunu, tekrar eden karışıklık çiftlerini ve gelecek haftanın 3 önceliğini çıkar. Sayıları yalnızca tablodan al."
- **P4 – Kaynaklı test:** "Yalnızca yüklediğim kaynaklara dayanarak [konu] hakkında 10 soruluk, 5 şıklı DUS tarzı test hazırla. Her sorunun altına kaynak alıntısını koy. Kaynakta olmayan bilgiyi kullanma."

---

## 7. Kullanıcının sorularına bu boyuttan yanıtlar

- **Q1/Q4 (DUS'a nasıl ve ne ile, neyi farklı yapmalı):** AI ancak yardımcı bir araç olabilir, ana yöntem olamaz. Ana yöntem süreli soru çözmek, kendi hatalarından aralıklı tekrar yapmak ve kitabı başvuru kaynağı olarak kullanmak. AI yalnızca denemeden sonra öğretici modda ve doğrulanarak kullanılmalı. Yeni nesil uygulamalar ucuz ve iyi bir pratik kaynağı, ama soru ve açıklama kalitesi denetlenmeli.
- **Q2/Q3 (dershane ve triaj):** Bu boyutun verisi doğrudan cevap vermiyor. Yine de en iyi modellerin bile bazı oturumlarda %30–50'ye düşmesi, sorulacak konuların bir kısmının prensipte öngörülemez olduğunu gösteriyor. "AI ile çıkacak konu" diye bir kanıt da yok.
- **Q5 (sprint):** AI sprint süresini değiştirmez. Analiz süresini kısaltabilir. Faz 0'daki kalibrasyon 2–3 hafta.
- **Q7 (INBDE uygulamaları):** Bootcamp ve Booster'ın AI asistanları satıcı iddiası. Eski modellerle INBDE tarzı sorularda yaklaşık 4–5 sorudan biri yanlıştı (Danesh 2023). Vaka sorularında başarı %66–69'du (Dashti 2024).
- **Q11/Q12 (ABD çalışmasının DUS'a faydası):** LLM'ler İngilizce bilgiyle Türkçe DUS'ta yalnızca yaklaşık 4 puan kaybediyor. Bu, bilgi tabanının büyük ölçüde ortak olduğunu düşündürüyor. Ama bu bir analiz ve kontaminasyonla zayıflıyor. INBDE uygulamalarıyla DUS'a girmek, DUS formatında Türkçe pratik ve terminoloji eksiği bırakır.
- **Arkadaşların yüksek neti:** Bu boyuttan katkı küçük. Uygulamalar hazır geri bildirim ve analitik sunuyor. Bu, "tamamlayıcı" kullanım koşullarına yakın. Ama seçim yanlılığı kardeş ajanın asıl açıklaması.

---

## 8. Çelişkili noktalar ve açık sorular

**Çelişkili:**
- Aynı model (GPT-4o) endodontide %61,4 ile %82,8 arasında değişiyor. Prompt, tarih, arayüz ve soru alt kümesi farkları belirleyici. Tek bir "AI doğruluğu" sayısı yok.
- Yüksek DUS doğruluğu iki şekilde okunabiliyor. (i) DUS bilgisi uluslararası standart bilgi, dolayısıyla INBDE çalışması DUS'a taşınır. (ii) Kontaminasyon nedeniyle ezber. 2022–2026 sorularıyla yapılmış test yok.
- Olumlu AI meta-analizlerinden biri geri çekildi. Kalan RCT'ler kısa vadeli ve gecikmeli test yok. AI'ın uzun dönemli bellek etkisi bilinmiyor.

**Açık:**
- AnkiWeb'de Türkçe DUS destesi var mı, kalitesi ne? Kullanıcı AnkiWeb'in paylaşılan desteler bölümünde "DUS" araması yapmalı.
- EasyDUS'un ve DusNote AI Asistan'ın gerçek doğruluğu nedir? Bunu Faz 0'daki kalibrasyon testiyle kişisel olarak ölçmek mümkün.
- X, Ekşi ve Telegram'daki AI ile DUS çalışma deneyimleri bu turda taranamadı (arama bütçesi).
- ChatGPT "study mode" duyuru sayfası doğrulanamadı (403).
- NotebookLM'in "Gemini Notebook" adına geçişinin tarihi ve kapsamı belirsiz.
- Deng 2025 ve Tozuka 2024'ün etki büyüklükleri okunamadı.
