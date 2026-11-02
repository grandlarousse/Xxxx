import json, sys, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "genel.json")
DOM = json.load(open(sys.argv[1])) if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else {}

meta = {
    "asof": "Veri 30.10.2026 kapanışına kadar · 47 VİOP pay vadelisi dayanağı · yatırım tavsiyesi değildir",
    "lede": ("Borsa İstanbul'da pay vadelisi olan 47 şirketin hangi uluslararası ve yurt içi sürücüyle birlikte hareket ettiği, "
             "hangisinin gerçekten önden gittiği ve bunun işlem maliyetinden sonra kullanılabilir olup olmadığı. "
             "Yaklaşık 1,1 milyon test, 30'dan fazla analiz ajanı, her güçlü iddia için bağımsız yeniden üretim ve çürütme turu."),
    "verdicts": [
        ["Küresel etki küçük ve dolaylı", "Medyan hissede günlük varyansın ~%2'si doğrudan küresel faktörlerden; XU100 ~%20, sektör/küme ~%20, hisseye özgü ~%58. Küresel etki çoğunlukla XU100 üzerinden gelir ve rejime göre %5–24 arasında değişir."],
        ["Öncülüğün çoğu saat farkı", "ABD, Brent, altın ve TUR'un BIST kapanışından sonraki hareketi ertesi açılış gap'ini açıklar (korelasyon 0,36–0,58) ama açılıştan sonra kalıntı yoktur. Pay vadelilerinin akşam seansı olmadığı için işlenemez."],
        ["Gerçek ama küçük gün-içi öncülük", "Sektöre özgü yabancı emsal bilgisi açılışta ~%22 fiyatlanır, gün içinde yavaş yansır (t 7,1). En net: ABD enerji→TUPRS, havayolları→THYAO/PGSUS/TAVHL, Japon çelik ve FMG→EREGL/KRDMD, TKC→TCELL. Brüt 3–11 bps; maliyet sonrası tek başına strateji değil."],
        ["Yurt içi bağlar daha güçlü", "Sektör/grup kümeleri (bankalar, Koza grubu, çelik, çimento, trafo, perakende), DİBS faizi ve VİOP USDTRY dış sürücülerden güçlü. Günlük hisse→hisse ve endeks→hisse öncülüğü yok (≈170 bin test, FDR 0)."],
    ],
}

def li(items): return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

genel = f"""
<h2>Net cevap</h2>
<p>Bu 47 hissenin günlük hareketini belirleyen şey ağırlıkla Türkiye'nin kendisi: piyasa geneli (XU100), sektör ve grup kümeleri ve hisseye özgü haberler. Uluslararası endeks, emtia ve şirketlerin <b>hisseye özgü</b> etkisi, XU100 ve kur kontrol edildikten sonra çoğu hissede 0,05–0,20 kısmi korelasyon düzeyinde kalıyor; 20 hissede ise sağlam bir küresel sürücü hiç yok. Görünen "lead-lag"in büyük kısmı saat farkından doğan açılış gap'i ve bu gap pay vadelisiyle işlenemiyor. Gerçek, gün içine taşan öncülük var ama küçük ve sektöre özgü.</p>

<h3>1. Ne kadar küresel? (varyans ayrıştırması, Shapley)</h3>
{li([
 "Medyan VİOP hissesi, 2014–2026: küresel 8 faktör %1,9 · TR makro %0,4 · XU100 %20,2 · sektör/küme %19,7 · hisseye özgü %58,2.",
 "XU100 varyansında küresel pay rejime bağlı: 2014–17 %15 · 2018–20 %22 · 2021–23 %5,5 · 2024–26 %11 · son 1 yıl %20 · 2026 Ocak–Ağustos %24. USD bazlı XU100'ün EEM betası 2014–17'de 0,85, 2023'te 0,15, 2026'da 0,60.",
 "En küresel (2024–26): TUPRS, GUBRF, TAVHL, PGSUS, THYAO, TRALT. En yerli: SASA, ULKER, BRSAN, ALARK, ENJSA.",
 "Krizler zıt yönde çalışıyor: küresel krizlerde (2015 Çin, COVID) BIST'in dışarıdan aldığı spillover artıyor; yerel krizlerde (KKM, Mart 2025, 2026 fon krizi) azalıyor ve iç bağ artıyor. Krizlerde korelasyon artışı büyük ölçüde oynaklık etkisi (Forbes–Rigobon düzeltmesiyle kayboluyor)."
])}

<h3>2. Zaman: hangi bilgi ne zaman fiyatlanıyor?</h3>
{li([
 "BIST kapanışı 18:00 TSİ (15:00 UTC). ABD 23:00/24:00 TSİ'de, Brent uzlaşması ~22:00, altın ~21:00 TSİ'de kapanıyor. Bu yüzden ABD/vadeli sürücülerin 'dünkü' getirisi BIST'in bugünkü getirisini öngörüyor gibi görünüyor.",
 "Ölçülen bağlar: ES gece → XU030 gap 0,45–0,47 (47 hisse medyanı 0,35; bankalar 0,44–0,52) · TUR kapanış sonrası → XBANK gap 0,36 (13/13 yıl) · Brent → TUPRS gap 0,58 · altın gece → TRALT gap 0,42 (çoğu 2026) · TKC → TCELL gap t 4,3. Hepsinde açılıştan sonraki gün-içi kalıntı ≈0 (612 gün-içi testte 0 FDR; 5 dakikalık veride gecikme yok).",
 "VİOP akşam seansı (19:00–23:00 TSİ) yalnız endeks vadelileri (XU030, XLBNK, X10XB, XSD25), ons altın/gümüş/platin/paladyum ve bakır için var; <b>pay vadelileri ve USD/TL yok</b> (BIST duyuru 30572). Akşam seansı kapanışında gece bilgisinin yalnız ~%24 (spot gap) ile %44 (vadeli gece) arası bilinir.",
 "Pratik anlam: bu gap bilgisi alfa değil, açılış beklentisi ve risk bilgisidir (limit emir, stop, pozisyon büyüklüğü ayarı). Pay vadelisi 09:20–09:30 açılış seansında spot gap'in β≈0,64'ünü zaten fiyatlıyor.",
 "Asya: Tokyo, Seul, Tayvan ve Sidney BIST açılışından önce kapanır (aynı gün bilgisi gerçekten önceden bilinir). Şanghay 10:00, Hong Kong 11:00 TSİ'de, yani BIST açıldıktan sonra kapanır; aynı günlük HK/Şanghay getirisini BIST gün-içi ile eşlemek ileriye bakmadır (1787.HK→TRALT iddiası bu nedenle düşürüldü)."
])}

<h3>3. Gerçek öncülük: sektöre özgü bilgi yavaş fiyatlanıyor</h3>
<p>Hakem ajanı, sonuçlara bakmadan önceden kaydedilmiş sektör emsal sepetleriyle 47 hissenin tamamını test etti: BIST kapanışından sonra gelen <b>sektöre özgü</b> yabancı emsal bilgisinin yalnız ~%22'si açılışta fiyatlanıyor, kalanı gün boyunca yansıyor (havuzlanmış 4,6 bps/σ, t 7,1; gerçek VİOP vadeli fiyatlarında 7,2 bps/σ, t 7,1). <b>Piyasa geneli</b> bilgi ise açılışta tamamen fiyatlanıyor. Etki metal, havacılık, rafineri, altın ve otomotivde güçlü; banka ve holdinglerde yok. Ekonomik değeri düşük: pozisyon başına brüt 3–11 bps, 8–15 bps maliyetin altında. Tek başına işlem stratejisi değil; filtre veya ağırlık olarak kullanılabilir. Bu bulgu, kaba kuvvet taramasının "gün-içi öncülük yok" sonucuyla çelişmiyor: tek sürücülü 48 bin testlik bir aile, küçük ama yaygın bir etkiyi istatistiksel olarak görünmez kılıyordu.</p>

<h3>4. Hisseye özgü en güçlü dış bağlar (senkron, XU100 kontrollü, doğrulandı)</h3>
{li([
 "TCELL ↔ NYSE:TKC (aynı şirketin ADR'ı) kısmi 0,61 · YÜKSEK.",
 "THYAO/PGSUS ↔ Avrupa havayolları (XETR:LHA 0,18, LSE:EZJ 0,16–0,17, LSE:IAG 0,15); ortak faktörler kontrol edilince 0,17–0,20 · YÜKSEK. TAVHL ↔ EURONEXT:ADP 0,13 · ORTA.",
 "TUPRS ↔ Brent 0,16 (haftalık 0,27, aylık USD 0,35, 2026'da güçlü) · YÜKSEK; ↔ ABD/Avrupa rafinerileri 0,12–0,19 (CRAK'ın ~%30'u mekanik, çünkü fon TUPRS tutuyor) · ORTA.",
 "TRALT ↔ altın (COMEX:GC1!) 0,15–0,22, 17/17 yıl pozitif ama 2023Y2–2024Y2'de bağ yok · YÜKSEK (rejime bağlı). 'SHFE altını COMEX'ten üstün' iddiası çürütüldü.",
 "EREGL ↔ Avrupa çeliği günlük 0,13 (son 1 yılda ≈0), aylıkta SLX/MT 0,33–0,41 · günlük ORTA, aylık YÜKSEK.",
 "ASELS ↔ Avrupa savunması: 2014–21 ≈0,02 → 2022–26 ≈0,11–0,13; büyük savunma haber günlerine bağlı · ORTA.",
 "AEFES ↔ küresel bira 0,06–0,09 (haftalıkta 0,20–0,25) · ORTA. TOASO ↔ Avrupa otomotiv 0,07–0,10 ama Avrupa piyasası kontrol edilince 0,02–0,04 · DÜŞÜK.",
 "Bankalar ↔ USDTRY (TL değer kaybında bankalar piyasanın gerisinde): XBANK kısmi −0,16 tam dönemde, kur krizi yıllarında güçlü, 2025–26'da ≈0 · ORTA. BBVA ↔ GARAN hisseye özgü bağ yok (0,02).",
 "Sağlam küresel sürücüsü olmayan 20 hisse: AKSEN, ALARK, DOHOL, EKGYO, ENKAI, HALKB, HEKTS, ISCTR, ODAS, SASA, SISE, TCELL (ADR hariç), TKFEN, TTKOM, ULKER, VAKBN, VESTL, TSKB, BIMAS, SOKM · olumsuz bulgu YÜKSEK."
])}

<h3>5. Yurt içi bağlar</h3>
{li([
 "Sektör faktörü (hisse-hariç sektör endeksiyle, XU100 kontrollü): YKBNK 0,76, ISCTR 0,74, TRMET 0,74, AKBNK 0,71, GARAN 0,70, TRALT 0,63, VAKBN 0,56, PGSUS 0,53, CIMSA 0,46, OYAKC 0,41, ASTOR 0,40, KRDMD 0,39. 29/47 hissede ≥0,15. Uyarı: ham sektör endeksi R²'si mekanik içerme yüzünden şişik (TCELL–XILTM 0,97 → hisse-hariç 0,38).",
 "Grup ve küme: TRMET–TRENJ 0,74–0,78, TRMET–TRALT 0,62, KRDMA/B/D 0,58–0,66, THYAO–PGSUS 0,50, EREGL–ISDMR 0,39–0,45, CIMSA–çimento kümesi 0,22–0,40, ASTOR–EUPWR 0,37 (zayıflıyor), MGROS–SOKM 0,31, AKBNK–GARAN 0,69, SAHOL–AKBNK 0,24, AEFES–CCOLA 0,22, KCHOL–ARCLK/FROTO/TOASO 0,12–0,16.",
 "Faiz: DİBS getirisi ↑ ↔ BIST ↓ (10 yıllık ile XU100 −0,30, son 1y −0,39; XBANK kısmi −0,16). En güçlü yurt içi makro faktör. Veri Borsa İstanbul kesin alım-satım bülteninden kuruldu.",
 "Kur: BIST kapanışına hizalı VİOP USDTRY ↔ bankalar −0,20, SISE +0,17, ENKAI +0,12. Yahoo'nun gece yarısı kapanışlı kuru bu kanalı neredeyse tamamen gizliyor (1y korelasyon −0,08). Yönetilen kur döneminde vadeli USDTRY'nin baz bileşeni bir faiz/risk göstergesine dönüştü.",
 "Gram altın ↔ TRALT/TRMET aynı gün 0,20–0,30. Yabancı akışı getiriye öncülük etmiyor, getiriyi takip ediyor (corr 0,32, 22/22 yıl).",
 "Öncülük yok: günlük hisse→hisse 157 bin test, endeks→hisse 12,7 bin test, saatlik 1.482 test → FDR'den geçen 0. Liderlik sıralaması yıldan yıla korunmuyor. 5 dakikada XU030 → illikit hisseler 5–15 dk gecikme var (HEKTS, SASA, ODAS); yarısı tik büyüklüğü/bayat fiyat, maliyeti karşılamıyor."
])}

<h3>6. Karşı argümanlar ve sınırlamalar</h3>
{li([
 "Çoklu test: birincil test sayısı ≈1,12 milyon. Küresel Bonferroni eşiği |t|≥5,5. Senkron bulguların çoğu bu eşiği geçiyor; işlenebilir gün-içi iddiaların tek tek çoğu geçmiyor. Geçen tek genel öncülük kanıtı, önceden kaydedilmiş havuzlanmış sektör testi (t 7,1).",
 "Örneklem içi seçim: ajanlar iddialarını 2021–26'yı da içeren veriyle buldu; 'OOS tutarlı' etiketi çoğunlukla gerçek bir dışarıda bırakılmış örneklem değil, alt dönem istikrarı.",
 "Veri: Yahoo Finance (BIST, ABD, Avrupa, Asya), İş Yatırım (BIST endeksleri), Borsa İstanbul VİOP ve BAP bültenleri, EPİAŞ PTF, Sina (Çin). Türkiye CDS'inin halka açık günlük tarihsel serisi bulunamadı. TradingView'da Türkiye CDS kodu da yok.",
 "Maliyet: VİOP spread'i doğrudan gözlenmedi, modelle tahmin edildi (küçük emirde medyan ~7 bps gidiş-dönüş, 1 mn TL emirde ~19 bps; düşük fiyatlı paylarda tik büyüklüğü SASA ~43, HEKTS ~36 bps). Açılış/kapanış müzayedesi derinliği sığ; açılış fiyatından dolum varsayan kârlar üst sınırdır.",
 "Rejim: Türkiye'nin küresel bağı 2021–23'te koptu, 2026'da geri geldi; Eylül–Ekim 2026 fon krizi son bir yılın korelasyonlarını bozuyor (43 gün, düşük güven). Bir ilişkinin geçmişte tutması gelecekte tutacağı anlamına gelmez.",
 "Korelasyon nedensellik değildir. Mekanizması olan bağlar (ADR, ortaklık, ürün fiyatı) bile kısa vadede başka faktörlerle örtülebilir."
])}

<h3>7. Hangi varsayım yanlış çıkarsa sonuç çöker?</h3>
{li([
 "Pay vadelilerine akşam seansı açılırsa ABD seansı bilgisinin bir kısmı işlenebilir hâle gelir; gap bulguları o zaman değer kazanır.",
 "TL serbest dalgalanmaya dönerse kur kanalı (bankalar −, ihracatçılar +) 2018–2023'teki gücüne geri döner.",
 "Gerçek VİOP kotasyon verisi spread'i bu çalışmadaki tahminden genişse, sınırda pozitif görünen tüm işlem adayları negatife döner.",
 "Yabancı payı ve küresel fon akışları kalıcı olarak artarsa küresel pay %20'nin üzerinde kalabilir; o durumda küresel sürücüler daha önemli hâle gelir."
])}

<h3>Sonuç</h3>
<p>Bu hisseler için küresel piyasaları izlemenin en büyük değeri açılış beklentisini ve riski önceden bilmek; günlük alfa kaynağı değil. Doğrulanmış en güçlü dış bağlar hisseye ve sektöre özgü (ADR, havayolu emsalleri, Brent ve rafineriler, altın, çelik), etkileri küçük ve rejime bağlı. Yurt içi kümeler, faiz ve kur daha belirleyici. İşlem maliyetinden sonra güvenle önerilebilecek tek başına bir lead-lag stratejisi bulunamadı; doğrulamadan geçen en sağlam aday SAHOL/AKBNK oranının ortalamaya dönüşü (ilişki YÜKSEK, VİOP'ta 2021–26 t 2,3–2,9; işlem ORTA) ve XU030'un öğleden sonra düşüşü (ORTA). Kapanış müzayedesi dönüşü yalnız spotta ve sığ kapasiteyle; tavan/taban ve temettü olguları gerçek ama VİOP'ta işlenemiyor. Bunlar ileriye dönük izlenmeye değer, ama yatırım tavsiyesi değildir.</p>
"""

yontem = f"""
<h2>Nasıl yapıldı</h2>
{li([
 "Evren: Borsa İstanbul VİOP bülteninden (30.10.2026) pay vadelisi olan 47 dayanak. KOZAL artık TRALT, KOZAA artık TRMET.",
 "Veri: ~1.250 sembol günlük (2000+), ~240 sembol saatlik (2023-11+), 5 dakikalık (son 60 gün); İş Yatırım'dan 49 BIST endeksi; VİOP bülteni 2017-03 → 2026-10 (2.422 gün); BAP DİBS getirileri (2013+); TLREF; EPİAŞ PTF; TCMB haftalık yabancı akışı; Sina Çin vadelileri.",
 "Zamanlama: tüm seriler BIST takvimine oturtuldu; her sürücünün kapanış saati saatlik veriyle doğrulandı; gap (önceki kapanış→açılış) ve gün-içi (açılış→kapanış) ayrı test edildi. İşlenebilirlik için sinyalin pozisyondan önce tamamen bilinmesi şartı arandı.",
 "Ajanlar: 1. tur 14 uzman (banka, holding, havacılık, enerji, metal, kimya, otomotiv, savunma, tüketim, kaba kuvvet tarama, gün-içi, Çin alternatifleri, TradingView doğrulama, olaylar); yurt içi turu 8 uzman (endeks, hisse-hisse, gün-içi, grup, makro, VİOP, akış, ağ/spillover); doğrulama turu 5 iş akışı (her işlenebilir iddia için bağımsız yeniden üretim + çürütme, toplu senkron doğrulama, hakem, TradingView denetimi, metodoloji eleştirmeni, temizlik duyarlılığı); kart turu 8 kurucu + 8 tamlık denetçisi.",
 "Güven etiketi: YÜKSEK = mekanizma + anlamlı büyüklük + yılların ≥%75'inde aynı işaret + IS ve OOS aynı işaret ve anlamlı (+FDR). ORTA = mekanizma var, tam dönem anlamlı, OOS aynı işaret ama zayıf/istikrarsız. DÜŞÜK = istatistik zayıf ya da mekanizma şüpheli ya da kısa örneklem. ÇOK DÜŞÜK = hipotez/test başarısız ama dışlanamıyor. Hiçbir fikir elenmedi; zayıflar etiketle listede.",
])}
<h3>Analiz sırasında bulunan ve düzeltilen veri/kod hataları</h3>
{li([
 "Yahoo '=X' kur serilerinin günlük kapanışı aslında o günün 00:00 UTC fiyatı (bir gün geç). Banka ve holding ajanları bağımsız buldu, koordinatör doğruladı. Düzeltilmeden kur 'öncülükleri' ve 'ters yön' bulguları sahteydi (ör. USDTRY → ihracatçı gün-içi t 4,7). Not: bu davranış 22.09.2010'dan beri geçerli.",
 "Temizlik kuralı −%10 taban günlerini siliyor, tavanları tutuyordu (olay ajanı). Simetrik hâle getirildi.",
 "BIST fiyat marjı 2020-03-13 öncesi ±%20'ydi; ±%10,5 eşiği 2016–2019'daki gerçek büyük hareketleri siliyordu (akış ajanı). Eşik rejime bağlandı.",
 "SASA'da Yahoo hacmi 2025-06'dan beri günlerin %42'sinde 0 ama fiyat işliyordu; bu günler siliniyordu. SASA'nın son 1 yıl rakamları tamamen değişti (XU100 betası 0,28 → 1,29).",
 "Yahoo'da XU030/XU100/XBANK/XUSIN dışındaki BIST endekslerinin geçmişi tek satır; İş Yatırım verisiyle değiştirildi.",
 "Metodoloji denetimi ek kalıntı riskleri buldu: BIST dışı serilerdeki 12σ filtresi bazı kur şoku günlerini siliyor (kur kaynaklı öncülükler ORTA'nın üzerine çıkarılmadı); saatlik verilerde temettü düzeltmesi yok; tatil sonrası pencere kayması gap korelasyonlarını ~%10 eksik ölçüyor (muhafazakâr yönde).",
 "Doğrulayıcılar ortak kütüphaneyi kullanmadan, ham veriden kendi kodlarını yazdı; bu sayede kütüphane düzeyindeki hatalar da sınandı.",
])}
<h3>TradingView kodları hakkında</h3>
{li([
 "1.212 sembolün 1.165'i TradingView'daki kendi sayfası okunarak doğrulandı; denetim turunda 943 benzersiz kodun hepsi yeniden kontrol edildi. 11 hatalı kod düzeltildi (ör. AMEX:TUR yok → NASDAQ:TUR; NASDAQ:SSRM; LSE:BA.).",
 "Tuzaklar: NYSE:IAG = IAMGOLD (havayolu IAG = LSE:IAG); NYSE:GOLD Barrick değil (Barrick = NYSE:B); NYSE:HEI = HEICO (Heidelberg = XETR:HEI).",
 "VİOP: pay vadelisi sürekli kontrat BIST:&lt;KOD&gt;1! (ör. BIST:THYAO1!), endeks vadelisi BIST:XU030D1!, BIST:XLBNKD1!; belirli vade BIST:XU030DZ2026. Ücretsiz kullanımda BIST/VİOP 15 dk, CME/ICE 10 dk gecikmeli; ICE/SGX gerçek zamanlı paketleri ücretli.",
 "Çin borsası kodu (SSE, SZSE, SHFE, DCE, ZCE, CFFEX, INE, GFEX) hiçbir yerde verilmedi; HKEX kodları 'açılmayabilir' notuyla ve ABD/OTC/ETF alternatifiyle verildi.",
])}
"""

signals_note = ("Her satır bağımsız yeniden üretim ve çürütme aşamalarından geçti. 'İstatistik' ilişkinin gerçekliğini, 'İşlem' ise gerçekçi giriş ve "
                "maliyetle (VİOP pay vadelisi 8–15 bps, endeks vadelisi 2–4 bps) kâr bırakma ihtimalini gösterir. Hiçbiri yatırım tavsiyesi değildir.")
signals = [
 {"name": "Sektör emsal sepeti t-1 → hisse gün-içi (genel anomali)", "def": "BIST kapanışından sonra gelen sektöre özgü yabancı emsal getirisi (emsal − bölge endeksi) → ertesi gün açılış→kapanış.", "target": "47 hisse (metal, havacılık, rafineri, altın, otomotiv)", "result": "Havuzlanmış 4,6 bps/σ (t 7,1), VİOP vadelisinde 7,2 bps/σ; bilginin ~%22'si açılışta fiyatlanıyor. Brüt 3–11 bps < maliyet.", "stat": "YUKSEK", "trade": "DUSUK", "tv": ""},
 {"name": "ABD enerji/rafineri hisseleri t-1 → TUPRS gün-içi", "def": "NYSE:VLO, MPC, PSX, PBF sepeti; |z|>1.", "target": "TUPRS (F_TUPRS)", "result": "Hedge'li t 4,3–5,3, 145 hisse içinde 1. sırada, gerçek F_TUPRS'ta t 3,5. 2014–17'de yok. Tek bacak net 8 bps: t 1,7. F_XU030 hedge'li 2020+ net 28 bps (t 3,0) ama açılış seansı derinliği 3–15 kontrat.", "stat": "ORTA", "trade": "DUSUK", "tv": "NYSE:VLO, NYSE:MPC, NYSE:PSX, NYSE:PBF, BIST:TUPRS1!"},
 {"name": "Avrupa+ABD havayolu sepeti t-1 → THYAO/PGSUS/TAVHL gün-içi", "def": "XETR:LHA, LSE:IAG, NASDAQ:RYAAY, LSE:EZJ, LSE:WIZZ, NYSE:DAL, NASDAQ:UAL… artığı; |z|>1.", "target": "THYAO, PGSUS, TAVHL", "result": "159 hisse içinde ilk 3; 2008–13'te de tekrar ediyor (t≈2). Brüt 21–32 bps/işlem; 15 bps maliyette 10–14 bps (t<1,7), hedge'li 4–8 bps.", "stat": "ORTA", "trade": "DUSUK", "tv": "XETR:LHA, LSE:IAG, LSE:EZJ, NASDAQ:RYAAY, BIST:THYAO1!, BIST:PGSUS1!"},
 {"name": "Japon çelik/makine + ASX madencileri aynı gün → EREGL/KRDMD gün-içi", "def": "TSE:5411, TSE:5401, TSE:6301, ASX:FMG, ASX:BHP (BIST açılışından önce kapanır).", "target": "EREGL, KRDMD, BRSAN", "result": "r 0,07–0,09, NW t 3,9–4,9, IS ve OOS ayrı ayrı anlamlı; FMG tek başına t 4,0–4,3. Bileşenler sonradan seçildi; artıklaştırılınca OOS net 8–18 bps (t ≤1,2), hedge'li negatif.", "stat": "ORTA", "trade": "DUSUK", "tv": "ASX:FMG, TSE:5411, TSE:5401, BIST:EREGL1!, BIST:KRDMD1!"},
 {"name": "TKC (NYSE ADR) parite sapması → TCELL gün-içi", "def": "ln(TKC×USDTRY / 2,5×TCELL) − 20 günlük ortalama.", "target": "TCELL", "result": "Gerçek b 0,09–0,11, XU100 arındırılmış t 4,2; yalnız TCELL'de var. OOS +19 bps üst sınır (KKM dönemi ağırlıklı); IS ≈0; açılış seansı emriyle +8–9 bps.", "stat": "ORTA", "trade": "DUSUK", "tv": "NYSE:TKC, FX:USDTRY, BIST:TCELL1!"},
 {"name": "XU030 öğleden sonra düşüşü", "def": "XU030 vadelisini ~11:00 TSİ'de sat, 18:10 kapanışta kapat (lead-lag değil, gün-içi mevsimsellik).", "target": "BIST:XU030D1!", "result": "11:00→kapanış −11,2 bps/gün (t 4,7), 12 yılın 11'i; spot vekili 2017–26 +11,1 bps (OOS t 3,1), 2–4 bps sonrası +7…+9 bps. Vadeli verisiyle doğrudan test yalnız 2023+; son 12 ay zayıf.", "stat": "ORTA", "trade": "ORTA", "tv": "BIST:XU030D1!"},
] + DOM.get("signals", []) + [
 {"name": "Kredi notu kararı sonrası ters pozisyon", "def": "Not kademe değişikliği sonrası ilk seans açılışında tersine gir, t+2 kapanışta çık.", "target": "XU100 / F_XU030", "result": "2016–2025'te +208 bps/olay (n=20) ama 2000–2013 Türkiye ve Güney Afrika/Yunanistan/İtalya'da (39 olay) çalışmıyor.", "stat": "DUSUK", "trade": "DUSUK", "tv": "BIST:XU030D1!"},
 {"name": "KCHOL açılış NAV ayrışması", "def": "İştiraklerin açılış gap'i − KCHOL gap'i → KCHOL gün-içi.", "target": "KCHOL", "result": "İstatistik t 4,9–5,6 ama fark ilk ~15 dakikada kapanıyor; gerçek KCHOL vadelisinde VWAP girişiyle OOS −6 bps.", "stat": "ORTA", "trade": "COK_DUSUK", "tv": "BIST:KCHOL1!"},
 {"name": "ENKAI'nin TL/Türkiye riskine gecikmeli tepkisi", "def": "NASDAQ:TUR veya USDTRY t-1 → ENKAI gün-içi (ters yön).", "target": "ENKAI", "result": "t −5,2 / 3,3–4,3 ama yalnız 2020–2023 rejiminde; 2024 sonrası ≈0; vadeli 2021–23 arası yoktu.", "stat": "ORTA", "trade": "DUSUK", "tv": "NASDAQ:TUR, FX:USDTRY, BIST:ENKAI1!"},
 {"name": "Çin altın/çelik → TRALT/KRDMD", "def": "1787.HK / 600547.SS → TRALT; SHFE HRC → KRDMD.", "target": "TRALT, KRDMD", "result": "HK sinyali BIST açılışından sonra kapandığı için ileriye bakıyor; açılıştan önce bilinen kısmı zayıf (t 1,9–2,4). SHFE gündüz seansı KRDMD'yi öngörmüyor (t 0,1). TradingView'da açılan işlenebilir vekil yok.", "stat": "DUSUK", "trade": "COK_DUSUK", "tv": "COMEX:GC1!, NASDAQ:GDX"},
 {"name": "VİOP baz anomalisi", "def": "Vadeli − teorik baz sapması → ertesi spot gap / vadeli gün-içi.", "target": "47 pay vadelisi", "result": "Kesitsel t 8–12 (IS ve OOS), ama kenar 09:30 açılış fiyatında; VWAP girişte net −11 bps.", "stat": "YUKSEK", "trade": "DUSUK", "tv": ""},
]
cin_note = ("Kullanıcının TradingView hesabında Çin borsaları açılmıyor. Orijinal seriler Yahoo ve Sina'dan alınıp alternatiflerle karşılaştırıldı. "
            "Endeks vekilleri güçlü (CSI300 ↔ AMEX:ASHR / CBOE:CNYA haftalık r 0,87–0,92; HSI/HSCEI ↔ AMEX:FXI, NASDAQ:MCHI 0,85–0,90). "
            "Emtiada durum zayıf: COMEX:TIO1! aylık ortalama kontrat olduğu için ay sonunda hareketsizleşiyor (TIO2!, SGX:FEF2! ya da ASX:FMG tercih edilmeli). "
            "PTA/MEG, cam, soda külü, üre ve PVC için açılabilen iyi bir vekil yok; BIST hisseleriyle bu Çin emtiaları arasında zaten ilişki bulunmadı.")
tv_note = ("Tüm kodlar TradingView'daki sembol sayfası okunarak doğrulandı (durum sütunu). Kodlara tıklayınca kopyalanır. "
           "VİOP pay vadelisi için BIST:<KOD>1!, endeks vadelisi için BIST:XU030D1! kullanın. HKEX ve ücretli ICE/SGX akışları hesabınızda açılmayabilir.")
json.dump({"meta": meta, "genel_html": genel, "yontem_html": yontem, "signals": signals, "signals_note": signals_note, "cin_note": cin_note, "tv_note": tv_note},
          open(OUT, "w"), ensure_ascii=False, indent=1)
print("ok", len(signals))
