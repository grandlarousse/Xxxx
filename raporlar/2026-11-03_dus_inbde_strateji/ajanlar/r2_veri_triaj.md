# R2 – Veri ve triaj mühendisi: çapraz sorgu, oylar ve revizyon

Tarih: 3 Kasım 2026 · Rol: veri ve triaj mühendisi · Okunanlar: r1_kurumsal_reformcu, r1_aktif_hatirlama, r1_kariyer_takvim, r1_seytanin_avukati (tam), kendi r1 dosyam, r2_kurumsal_reformcu (bana yöneltilen eleştiri için), r0_dus_sinav §2.3.
Bu turun hesapları: `/tmp/claude-0/-home-user-Xxxx/eb62f538-fa87-5a4c-809f-e9032ba91072/scratchpad/r2/calc2.py` [analiz, kaba binom ve normal yaklaşım].

---

## 0. Kısa özet

- Önerdiğim iki şeyi geri çekiyorum ya da düzeltiyorum: RapiDUS tipi sıkıştırılmış çekirdek (O2) ve ham lift testi.
- Bu turun yeni bulgusu şu: komitedeki ara ölçüm kapıları (+6 net, +10 net) tek ölçümle uygulanırsa yazı tura gibi çalışıyor. Bunların yerine davranış ve mekanizma metrikleri koyuyorum.
- Yönteme ilişkin ortak çekirdek (soru önce, arşiv, kart, cezalı deneme) dayanıklı. AİS teşhisi planın yönünü çok az değiştiriyor. Asıl belirlediği şeyler üç: A tipinin (materyalde yok) payı, strateji/okuma/süre hataları ve kişisel TBT/KBT hata oranı.

---

## 1. Diğer stratejistlere somut eleştiriler

### 1.1 Kurumsal reformcu
1. **K1 katmanı kamp PDF'lerinden kurulamaz.** "Ne Çıktı Ne Çıkacak" spotları şıkları ayıklanmış, sıkıştırılmış cümleler. "Tüm şıklar" ilkesi (eski çeldirici sonraki sınavda kök olur) orijinal maddeyi gerektiriyor. Spot okumak yeniden okumadır, yani düşük faydalı bir teknik. K1 doğrudan arşivden çalışılmalı. NÇNÇ PDF'inin asıl değeri başka: kullanıcının elindeki **sınavdan önce kayda geçmiş tek vurgu listesi** bu. Bu yüzden lift testi için tarafsız bir payda olarak kullanılmalı (r2_kurumsal_reformcu'nun önerisi; benimsiyorum).
2. **Sprintin 1. haftasında tek denemeden "branş × hata tipi matrisi" çıkmaz.** Bu nokta aktif hatırlama için de geçerli. 120 soruda branş başına ~7 madde düşüyor, bu da doğruluk oranında ±19 puanlık standart hata demek. Branş matrisi arşivden kurulmalı: ~165 madde/branşla standart hata ~4 puana iner.

### 1.2 Aktif hatırlama
1. **Hacim hedefi kalite riskini büyütüyor.** ≥8.000 benzersiz sorunun ≥%75'i Türkçe olacaksa ÖSYM (~2.640) ve TUS (~1.000) dışında ~4.500–5.000 soru, doğruluğu ölçülmemiş Türkçe bankalardan gelecek. Anahtar hatası %3–7 ise 5.000 soru, 150–350 yanlış "bilgi" demek. Önerilen döngüde her hata karta dönüştüğü için sistem yanlış anahtarı **çoğaltıyor**. "30 soruda hata >%5" eşiği de ölçülemez: tek hata bile %3,3 ediyor. **Kural:** Bankadan gelen bir yanlış, kitapta doğrulanmadan karta dönüşmez.
2. **Kodlama şemaları çakışıyor.** Onların B'si (hatırlamadım) benim C'me, onların C'si (karıştırdım) benim D'me karşılık geliyor; kurumsal a/b/c kullanıyor. O3 bile iki şemayı karıştırıyor. Nihai rapor kullanıcıya tek bir şema vermeli (önerim §2.3'te).

### 1.3 Kariyer ve takvim
1. **20 Kasım kesim tarihi bilgiden önce geliyor.** İlk geri dönüşsüz harcama ~10 Aralık'taki JCNDE başvurusu (1.325 $). Vize başvurusu ucuz ve 2028 yolu için de işe yarıyor. Doğru kural şu: başvuru hemen yapılır; kapı JCNDE ödemesinde uygulanır (28 Şubat'tan önce mülakat tarihi var mı?). Erken iptal para kazandırmıyor, yalnızca opsiyonu yakıyor.
2. **Dal A için önsel olasılık düşük.** Bulgularda Türkiye'den adı geçen tek CODA akrediteli fakülte Yeditepe (başka okul olup olmadığı taranmadı) ve bu statü yalnız 1 Şubat 2024 ve sonrasındaki diplomaları kapsıyor. "Arkadaşlar 2 aydır INBDE'ye hazırlanıyor" ipucu düz iyimserlikle de uyumlu. Okul doğrulanmadan plan Dal A'ya yaslanmamalı.

### 1.4 Şeytanın avukatı
1. **+6 net kapısı (O7) gürültünün içinde.** İki deneme farkının SD'si ≈8,9 net. Gerçek kazanç sıfırsa kapı %25 olasılıkla geçiliyor; gerçek kazanç +6 ise %50 olasılıkla kaçırılıyor. Üçer denemenin ortalamaları karşılaştırılsa da sonuç değişmiyor: gerçek +6'yı kaçırma olasılığı yine %50. Kapının davranış ayağı ("arşiv turu bitti mi?") ise gürültüsüz; o ayak korunmalı.
2. **Mart'taki +10 kapısı (O8) hem gürültülü hem gereksiz.** Gerçek +5 kazançta kapı %29 olasılıkla geçiliyor, gerçek +15'te %29 olasılıkla kaçırılıyor. Daha önemlisi, branş tercihi sonuç geldikten sonra yapılıyor (Kasım 2027). Branşa bağlı tek çalışma kararı T puanlı dallar için TBT ağırlığı.
3. **Yüzdelik farkı testi (O4) zayıf ayırıyor.** Toplam net SD'si ≈18,4 olduğundan dağılımın ortasında 20 yüzdelik puan ≈9–10 net ediyor. 4 deneme ortalaması tek bir ÖSYM sonucuyla karşılaştırıldığında, gerçek fark sıfır olsa bile ≥20 puanlık fark %9 olasılıkla görülüyor. Gerçek 10 netlik bir sınav günü etkisi ise ancak %55 olasılıkla yakalanıyor. Norm grubunun yanlılığı da bunun üstüne ekleniyor.
4. **Haftada 10–12 saat bakım gerekenden fazla.** İki tur için hesabım ~7–8 saat/hafta (§4). Fazla saat taahhüdü, kendi uyardığı buharlaşma riskini artırıyor.

---

## 2. Bana yöneltilen en güçlü karşı argüman ve cevabım

### 2.1 Argüman
Bu argüman r2_kurumsal_reformcu ve şeytanın avukatından geliyor. Üç parçası var:
- (a) Lift = Kapsam_Ç / h oranının mekanik bir tavanı var: 1/h. Kitaplar "doldurulduysa" h 0,6–0,9 olur, lift en fazla 1,11–1,67 çıkar. Bu durumda benim "≤1,2 ise çizdirme değersiz" kuralım triajı kendiliğinden mahkûm eder ve dershaneyi değil kullanıcının çizme alışkanlığını ölçer.
- (b) RapiDUS'un lift ≈3,4'ü okuma maliyetini ölçüyor. "Önce soru" iş akışında maliyet sayfa sayısıyla değil bakılan madde sayısıyla artar. Tam set bu iş akışında bir şey kaybettirmez; sıkıştırılmış set ise ayrıntı kaybettirir ve yeni bir harcamadır.
- (c) Ölçüm aparatının kendisi moral bozukluğu yaşayan bir kullanıcı için zaman yutucu bir kaçış olabilir.

### 2.2 Cevabım
- **(a) Kabul.** Testi üç şekilde düzeltiyorum.
  - **Normalize lift:** L* = (Kapsam_Ç − h) / (1 − h). Rastgele vurgu 0, kusursuz vurgu 1 verir. Lift'i 1,5 olan iyi bir triaj h = 0,4'te L* ≈ 0,33 verir.
  - **Tarafsız vurgu seti:** h kullanıcının kendi işaretlerinden değil, önceden kayda geçmiş setlerden ölçülür: NÇNÇ spotları (K1 sütunu), kitabın kendi "önemli/kutu" işaretleri ya da hocanın çizdirdiği renk.
  - **Asıl hüküm koşullu doğruluktan:** acc_Ç ile acc_G karşılaştırılır.
  - Dürüst sınır: 120 maddede lift 1,5'in %95 aralığı kabaca 1,1–2,1. Bu test yalnız kaba bir başarısızlığı gösterebilir. Karar ağırlığını düşürüyorum.
- **(b) Kabul; O2'yi geri çekiyorum.** Başvuru kaynağı kullanıcının kendi tam seti olur ve dizin olarak açılır. Sıkıştırmanın tek gerçek kullanımı 11–24 Ekim hafifletme dönemindeki okuma. Bunun için de yeni ürün alınmaz: arşiv ve hataların işaret ettiği "isabet sayfaları" toplanarak kendi çekirdeğin kurulur.
- **(c) Kısmen kabul.** Ölçüm yükü ≈40 saat: AİS 8, etiket 15, panel 16, örneklem 1. Bu, yıllık ~780 saatin ~%5'i. Kural: ölçüm sürenin %5'ini geçmez. Haftalık panel üç sayıya iner: yeni soru, son 300 sorudaki ilk-görüş doğruluk, gecikmeli düzeltme oranı. Etiket yalnız konu_L1 düzeyinde, açılır listeden (~20 sn). Bilgi noktası yalnız hatalarda yazılır.

### 2.3 Tek kodlama şeması (öneri)
- **A:** Materyalde yok.
- **B:** Var ama geçiştirilmiş ve çalışılmamış.
- **C:** Çalışılmış, hatırlanmamış.
- **D:** Karıştırma.
- **E:** Okuma.
- **F:** Strateji (boş/tahmin).
- **G:** Süre.
- **Doğrulama:** "Y" ve "G" kodları sayfa numarasıyla doğrulanır. Dizinde 3 dakika aranıp bulunamayan madde "?" kodu alır. Hesap verebilirlik ortağı maddelerin %20'sini kör kodlar.

---

## 3. Oylar

| Önerme | Oy | Güven | Gerekçe / koşul |
|---|---|---|---|
| O1 | katılıyorum | yüksek | Kitaplar elde; değerli kalemler ucuz. Bir Türkçe soru kampı **zorunlu**, çünkü ≥8.000 benzersiz soru hedefine karşı ÖSYM ve TUS birlikte ~3.600 soru veriyor. Kamp 60 soruluk denetimden geçmeli. 25 bin TL bir tavan, hedef değil |
| O2 | katılmıyorum | orta | Geri çekiyorum (§2.2-b). Tam set dizin olarak kullanılır; hafifletme dönemi için kendi isabet sayfalarından çekirdek kurulur; yeni harcama yok |
| O3 | koşullu | orta | Koşullar: A ve B ayrı kodlanır; hüküm kayıp paylarından değil tam paydalı acc_Ç/acc_G karşılaştırmasından verilir; sayfa numarasıyla doğrulama yapılır; ±14 puanlık gri bölge kabul edilir (~50 kayıp maddede payın %95 yarı genişliği). Öngörüm: C+D ≥%50, A ≤%15, B %15–30. B'nin çözümü de soru hacmidir, yani plan aynı kalır; yalnız A yeni kaynak gerektirir |
| O4 | koşullu | düşük | Yüzdelik farkı tek başına zayıf bir sinyal (§1.4-3). Dal ancak AİS imzasıyla birlikte açılır: boş ≥20 ya da E+F+G ≥ kayıpların %25'i ya da son 30 maddede doğruluk ≥15 puan düşük. Koşul: ≥4 süreli deneme. O durumda bile arşiv haftada ≥4 saatle sürer |
| O5 | koşullu | orta | Yalnız 2027'de INBDE'ye gerçekten girilecekse (Dal A ya da ABD birincil). ÖSYM TBT arşivi haftada ≥3 saat sürmeli ve boş bırakma davranışı aylık cezalı ÖSYM bloğuyla izlenmeli. Dal B'de DUS birincilse hayır |
| O6 | koşullu | orta | 1 tam tur + 1 hedefli tur (yanlışlar, şanslı doğrular ve tüm şıklar; maddelerin ~%40'ı) ≈200 saat, yani ~7–8 sa/hafta. Tam ikinci tur yalnız AİS'te tanıdık maddelerde doğruluk <%75 ise. Mart dalında tek tur |
| O7 | koşullu | orta | Davranış ayağı (30 Nisan'da arşiv turu bitti mi) korunur. +6 net ayağının yerine şunlar gelir: ≥150 yeniden sorulmuş maddede gecikmeli düzeltme <%70 ya da planlanan saatin <%75'i gerçekleşmiş. Süre ayrıca AİS hata tipine bağlanır |
| O8 | koşullu | orta | +20 merkez ve +30 üst kuyruk planlama varsayımı olarak doğru. Mart +10 kapısı kaldırılmalı (§1.4-2). Branşa bağlı tek karar T puanlı dallar için TBT ağırlığı |
| O9 | katılıyorum | yüksek | DUS yılda tek atış. Mart dalı 150–250 saatlik Türkçe arşiv işini sprint öncesinden çıkarıyor. ABD yolunda 1 yıllık gecikme, 2–3 yıllık advanced standing yolunda küçük bir bedel |
| O10 | katılmıyorum | orta | "Hiçbir dalda" fazla katı. Dal A ya da ABD birincilse Mayıs, önceden konmuş "kalırsan tekrar DUS'tan sonra" kuralıyla kabul edilebilir. Dal B ve DUS birincilse soru O9 ile zaten ortadan kalkıyor |
| O11 | koşullu | orta | Koşullar: CODA statüsü yazılı olarak doğrulanmış, vize/TRV Ocak ortasına kadar elde, JCNDE'nin 39 örnek sorusu süreli çözülüp İngilizce hız yeterli bulunmuş, zirve sırasında DUS TBT'ye haftada ≥3 saat ayrılmış, iki zirve arasında 2 hafta dinlenme. %7,2 Türk mezunu için iyimser bir oran |
| O12 | koşullu | orta | Vize başvurusu hemen yapılır. Kapı ~10 Aralık'taki JCNDE ödemesinde: 28 Şubat'tan önce mülakat tarihi yoksa Mart düşer. ECE yalnız 2028'de de ABD gerçek bir hedefse ödenir |
| O13 | katılıyorum | orta | Fikrimi değiştirdim. Hata sonrası açıklama ihtiyacı ≈58 saat, yani yıllık sürenin ~%7'si; %10 bunu karşılıyor. Fazlası geri çağırmanın yerine geçme işareti. Asıl koruma "önce kendi cevabın" kuralı |
| O14 | katılmıyorum | orta | AFK sprintin 6. haftasına düşüyor (~1 haftalık kayıp ≈ sprintin %6'sı). İlk girişte geçme oranı %49,6. Kanada ikincilse aceleye gerek yok. Dal A'da CDA–CODA karşılıklılığı AFK'yı gereksiz kılabilir |
| O15 | koşullu | düşük | Önsel olarak en büyük pay seçilimde, ama ayırt edici veri yok. Not ortalamaları eşitse ve fark ≥15 net olup derslere yayılmışsa çürür. Karar iki durumda da aynı: aracı değil davranışı kopyala |
| O16 | koşullu | orta | Boş ≤25 ise 3–5 net (20 boşun yarısı iki şıkka inmişse ≈4). Boş ≥30 ve iki şıkta isabet ~%60 ise 6–8 net; o zaman O4 dalı açılır |

---

## 4. Fikrimi değiştirdiğim noktalar

1. **O2 geri çekildi.** Sayfa başına getiri, okumanın ölçüsü. "Önce soru" iş akışında belirleyici değil.
2. **Lift testi:** Ham oran yerine normalize L*, tarafsız vurgu seti (NÇNÇ/K1) ve koşullu doğruluk. Testin karar ağırlığı da düştü.
3. **Dallanma kuralı:** "A+B ≥%40 ise kapsam genişlet" kuralını değiştirdim. B'nin çözümü de alt başlıkların tamamına yayılan soru hacmi, yani aynı rejim. Plan A payına, E/F/G'ye ve kişisel TBT/KBT hata oranına göre dallanır.
4. **Bakım dozu:** 6–8 saat ve tek tur yerine ~8 saat, 1 tam ve 1 hedefli tur. Hesap: tur 1 110 saat, hedefli tur 2 35 saat, TUS 25 saat, kart 28 saat; toplam ≈198 saat / 26 hafta ≈ 7,6 sa/hafta.
5. **AI tavanı:** %15–20'den ≤%10'a.
6. **Platform denetimi:** 30 soru ve ≥2 hata yerine 60 soru ve ≥3 hata. Eski eşik %7 hatalı bir bankayı %37 olasılıkla geçiriyordu. Yeni eşik %7'lik bankayı %80, %10'luk bankayı %95 olasılıkla yakalıyor; %3'lük bankayı ise yalnız %27 olasılıkla yanlışlıkla eliyor.
7. **Soru kampı:** "Kampa para yok" ifadem yanlış anlaşılmaya açıktı. Tahmin kampına para yok; denetimden geçmiş bir Türkçe **soru** kampı ise hacim kısıtı yüzünden gerekli.
8. **Dal B ve DUS birincil:** Mart yok (O9). "Kapılar geçilirse Mart" önerimi bu dal için bırakıyorum.

**Değiştirmediklerim:**
- Tam payda kuralı. Doğru maddeler de kodlanmazsa koşullu doğruluk hesaplanamaz.
- %20 tahmin kuralı.
- Haftalık ölçünün deneme neti olmaması. Bu turdaki kapı hesapları bu görüşü güçlendirdi.
- Lift'ini ya da zaman damgalı isabetini yayımlamayan "çıkacak" ürününe para verilmemesi.

---

## 5. Revize S1–S13

- **S1 [orta]:**
  - 11 Kasım'a kadar 120 maddenin tamamı tek şemayla kodlanır.
  - Kasım–Haziran: 2012–2026 arşivinin etiketli tam turu, ardından hedefli ikinci tur ve filtreli TUS temel bilim çıkmışları; ~8 sa/hafta.
  - 5 Temmuz – 24 Ekim sprint: denetlenmiş Türkçe soru kampı, arşivin 3. turu ve cezalı denemeler.
  - Önce soru, sonra tam sette yalnız ilgili sayfa. Anki FSRS yalnız kendi hatalarından. Tek tablo.
- **S2 [orta]:** Altyapı olarak faydalı: arşiv, deneme normu, kapsam sınırı ve kayda geçmiş tahmin listesi. Yöntem olarak düşük faydalı. Etkisi ölçülmemiş. Harcama ≤25 bin TL.
- **S3 [orta]:**
  - Kapsamı (recall) yüksek. İsabeti (precision) ve kaldıracı (lift) yayımlanmıyor. Nokta düzeyinde "çıkacak" isabeti <%1.
  - Afiş okuma kuralı: payda, zaman damgası ya da rakiple kıyas yoksa afiş yalnız bir kapsam ölçüsü.
  - Kendi testin: normalize L* ile acc_Ç/acc_G karşılaştırması. 120 maddeyle yalnız kaba bir başarısızlık görülebilir.
- **S4 [orta]:**
  - Değişecekler: girdi yerine çıktı metrikleri, soru önce yöntemi, tahmin kuralı.
  - Neyle: lisanslı arşiv, bir Türkçe soru kampı, deneme serisi.
  - Yeni nesil platform: 60 soruluk denetimden ve soru bazında dışa aktarım şartından geçerse.
  - AI: ≤%10, yalnız kendi cevabından sonra ve öğretici modda.
  - ABD uygulaması: yalnız INBDE'ye 2027'de gerçekten girilecekse.
  - Kiminle: maddelerin %20'sini kör kodlayan bir hesap verebilirlik ortağı.
- **S5 [orta]:** 16 hafta.
  - AİS'te E/F/G baskınsa 14, A ≥%25 ise 18 hafta.
  - 30 Nisan'da arşiv turu bitmemişse ya da planlanan saatin <%75'i gerçekleşmişse sprint 7 Haziran'da başlar.
- **S6 [orta]:**
  - INBDE: test spesifikasyonu hazır bir triaj haritası. Tek banka 2–3 tur; FK bazında ilk-görüş doğruluk izlenir. JCNDE'nin 39 örnek sorusu ve 2 simülasyon ankraj olarak kullanılır. Hatırlanan soru PDF'leri yasak. CODA statüsü yazılı olarak doğrulanır.
  - Kanada: NDEB'in 100 soruluk öz değerlendirmesi. Kanada birincil değilse AFK 2028'de.
- **S7 [düşük]:**
  - DUS: lisanslı Tüm DUS uygulaması (960–1.680 TL), Anki, tablo ve denetlenmiş bir Türkçe kamp.
  - INBDE: Booster ya da Bootcamp, ücretsiz denemeyle seçilir. Booster'ın iade garantisi uluslararası adayı da kapsıyor.
  - Seçim ölçütü: dışa aktarım ve analitik.
- **S8 [yüksek]:** Bağımsız ölçülmüş bir başarı oranı yok. Satıcı yüzdeleri paydasız ve birbiriyle çelişiyor. Puanla ilişkili olan sistem değil davranış: yeni soru, aralıklı tekrar, geri bildirim.
- **S9 [orta]:**
  - Toplam ~750–800 saat: bakım ~200–230, sprint ~500–550. Sprintte günde 5–6 saat. ≥8.000 benzersiz soru.
  - Ölçüm yükü ≤%5.
  - İlk-görüş doğruluk 3 hafta yatay kalırsa daha fazla saat değil, hafif bir hafta.
- **S10 [orta]:**
  - Dal B ve DUS birincilse: INBDE DUS'tan sonra.
  - Dal A ya da ABD birincilse: Mart. Kapı 10 Aralık'ta: 28 Şubat'tan önce mülakat tarihi olmalı.
  - 1 Şubat'ta Mart'a hazır değilse Mayıs, ancak "kalırsan DUS'tan sonra" kuralıyla.
- **S11 [orta]:** İçerik olarak DUS sorularının ~%55–65'ine dokunur; yöntem tam aktarılır. Yalnız DUS hedefleyen biri için marjinal fayda küçük. Ölçmek için INBDE soruları DUS branşlarına etiketlenir.
- **S12 [orta]:** ~60 net (47–73). Eksikler: K1, TBT ayrıntısı, ceza ve öncüllü format, Türkçe terim. Cezasızlık boş bırakma davranışını bozar; bu, aylık cezalı blokta "güven 2" isabetiyle izlenir.
- **S13 [düşük]:**
  - Etkenlerin karışımı; önsel olarak en büyük pay seçilimde.
  - Dört imza testi: not ortalaması, farkın ders bazında dağılımı, boş sayısı, çözülen soru sayısı.
  - Duyulma yanlılığına karşı deneysel girenlerin hepsinin netleri istenmeli.
  - Hangisi çıkarsa çıksın kopyalanacak olan araç değil, davranış.
