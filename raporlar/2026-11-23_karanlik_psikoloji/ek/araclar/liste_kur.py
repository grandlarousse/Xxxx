#!/usr/bin/env python3
"""Ayrintili yazilacak kitap listesini kurar: ek/parcalar/kitap_listesi.json ve gruplar.json.
Ipucu metinleri kesif dosyalarindaki 'gerekce' alanlarindan ve elle eklenen notlardan derlenir."""
import glob, json, os, re, unicodedata
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def f(s):
    s = (s or "").replace("ı", "i").replace("İ", "I")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
kesif = []
for p in glob.glob(K + "/parcalar/kesif_D*.json"):
    kesif += json.load(open(p))["kitaplar"]
def bul(soyad, baslik):
    for b in kesif:
        if f(soyad) in f(b["yazar"]) and f(baslik) in f(b["ozgun_ad"]):
            return b
    return None
# (grup, kod, soyad, yazar, ozgun ad, yil, baslik anahtari, ek not)
G = {
 "A1": ("Karanlık kişiliğin bilimi", "A", [
  ("Zeigler-Hill", "Virgil Zeigler-Hill ve David K. Marcus (ed.)", "The Dark Side of Personality: Science and Practice in Social, Personality, and Clinical Psychology", "2016", "dark side of personality", "APA yayını derleme; 'karanlık' özelliklerin ayrımcı ve uyumlu yanları; bölüm yazarlarını ve kısımları ver."),
  ("Lyons", "Minna Lyons", "The Dark Triad of Personality: Narcissism, Machiavellianism, and Psychopathy in Everyday Life", "2019", "dark triad of personality", "Liverpool'da psikolog; karanlık üçlünün aile, iş, eş seçimi, çevrimiçi davranışta görünümü; Academic Press."),
  ("Bereczkei", "Tamás Bereczkei", "Machiavellianism: The Psychology of Manipulation", "2018", "machiavellianism", "Pécs Üniversitesi; makyavelizmin bilişsel ve duygusal temeli, 'zihin okuma' becerisi tartışması, Routledge."),
  ("Baron-Cohen", "Simon Baron-Cohen", "Zero Degrees of Empathy: A New Theory of Human Cruelty (ABD: The Science of Evil)", "2011", "zero degrees", "Cambridge; 'kötülük' yerine 'empati erozyonu'; empati devresi; sıfır-negatif (psikopati, sınırda, narsisizm) ve sıfır-pozitif (otizm) ayrımı; eleştiriler."),
 ]),
 "A2": ("Kötülüğün psikolojisi", "A", [
  ("Baumeister", "Roy F. Baumeister", "Evil: Inside Human Violence and Cruelty", "1997", "evil", "Kötülüğün dört kökü: maddi kazanç, tehdit altındaki benlik saygısı (egotizm), idealizm, sadizm; 'büyüklük boşluğu' (magnitude gap): fail ile kurbanın algı farkı; benlik saygısı mitine itiraz."),
  ("Zimbardo", "Philip Zimbardo", "The Lucifer Effect: Understanding How Good People Turn Evil", "2007", "lucifer", "Stanford Hapishane Deneyi (1971) ve Abu Ghraib; durumsal güçler, sistem; Le Texier 2018 ve diğer eleştiriler (deneyin yönlendirilmiş olduğu); 'kahramanlığın sıradanlığı'. Milgram önceki raporda."),
  ("Browning", "Christopher R. Browning", "Ordinary Men: Reserve Police Battalion 101 and the Final Solution in Poland", "1992", "ordinary men", "101. Yedek Polis Taburu, Józefów 1942; reddetme fırsatına karşın katılım; uyma, kariyer, grup baskısı; Goldhagen ile tartışma (Hitler's Willing Executioners 1996). Türkçesi: Sıradan Adamlar."),
  ("Arendt", "Hannah Arendt", "Eichmann in Jerusalem: A Report on the Banality of Evil", "1963", "eichmann", "Kötülüğün sıradanlığı; düşünememe; Eichmann'ın Sassen kayıtlarıyla ortaya çıkan ideolojik yanı (Stangneth 2011) ve eleştiriler. Önceki raporda Arendt'in On Violence'ı anlatıldı."),
 ]),
 "A3": ("Psikopati klasikleri", "A", [
  ("Cleckley", "Hervey Cleckley", "The Mask of Sanity", "1941", "mask of sanity", "16 klinik ölçüt; vaka portreleri; son baskı 1976 (5. baskı); 'akıl sağlığı maskesi'; Hare'in PCL'sine temel."),
  ("Hare", "Robert D. Hare", "Without Conscience: The Disturbing World of the Psychopaths Among Us", "1993", "without conscience", "PCL-R'nin yaratıcısı; psikopatinin popüler anlatımı; duygusal-kişilerarası ve yaşam tarzı belirtileri; 'beyaz yakalı psikopatlar'; korunma ve hayatta kalma rehberi bölümü."),
  ("Stout", "Martha Stout", "The Sociopath Next Door", "2005", "sociopath next door", "Harvard Tıp'ta klinik psikolog; '25 kişide 1' iddiası ve dayanağı; vicdanın doğası; sosyopatı tanımanın 13 kuralı; acıma oyunu; eleştiriler (sayı)."),
  ("Raine", "Adrian Raine", "The Anatomy of Violence: The Biological Roots of Crime", "2013", "anatomy of violence", "Nörokriminoloji; prefrontal korteks, amigdala, düşük dinlenme kalp hızı, beslenme; etik ve hukuk tartışması; Türkçesi var mı katalogdan bak."),
 ]),
 "A4": ("Psikopati: popüler bilim ve korunma", "A", [
  ("Dutton", "Kevin Dutton", "The Wisdom of Psychopaths: What Saints, Spies, and Serial Killers Can Teach Us About Success", "2012", "wisdom of psychopaths", "Oxford; 'psikopati sürgüsü' (dial); 'yedi öldürücü kazanma' (ruthlessness, charm, focus, mental toughness, fearlessness, mindfulness, action); meslek listesi (CEO, avukat, cerrah); eleştiriler."),
  ("Ronson", "Jon Ronson", "The Psychopath Test: A Journey Through the Madness Industry", "2011", "psychopath test", "Gazeteci; Hare'in kursu, Broadmoor'daki 'Tony', Al Dunlap; teşhis koymanın kolaylığı ve 'delilik endüstrisi'; Hare'in tepkisi. Türkçesi 'Psikopat Testi'."),
  ("Kiehl", "Kent A. Kiehl", "The Psychopath Whisperer: The Science of Those Without Conscience", "2014", "psychopath whisperer", "Mobil MR ile cezaevlerinde binlerce tarama; paralimbik sistem; gençlerde tedavi (Mendota Juvenile Treatment Center) ve umut; hukuki sonuçlar."),
  ("MacKenzie", "Jackson MacKenzie", "Psychopath Free: Recovering from Emotionally Abusive Relationships with Narcissists, Sociopaths, and Other Toxic People", "2012", "psychopath free", "PsychopathFree.com forumunun kurucusu; idealize-değersizleştir-terk döngüsü, kurtulma aşamaları; ilk baskı 2012 kendi yayını, 2015 Berkley; bilimsel dayanağı zayıf, kurtulanların deneyimi."),
 ]),
 "A5": ("Narsisizm: kuram ve kültür", "A", [
  ("Kernberg", "Otto F. Kernberg", "Borderline Conditions and Pathological Narcissism", "1975", "borderline conditions", "Nesne ilişkileri kuramı; patolojik büyüklenmeci kendilik; kötücül narsisizm kavramına uzanış (1984); Kohut ile tartışma; Türkçe baskı var mı katalogdan."),
  ("Lasch", "Christopher Lasch", "The Culture of Narcissism: American Life in an Age of Diminishing Expectations", "1979", "culture of narcissism", "Tarihçi; toplumsal eleştiri; terapötik kültür, ünlülük, rekabet; Carter'ın 'malaise' konuşmasına etkisi; Türkçesi 'Narsisizm Kültürü'."),
  ("Twenge", "Jean M. Twenge ve W. Keith Campbell", "The Narcissism Epidemic: Living in the Age of Entitlement", "2009", "narcissism epidemic", "NPI puanlarının kuşaklar arası artışı iddiası; eleştiriler (Trzesniewski ve Donnellan; Wetzel ve ark. 2017 tersi bulgu); Türkçesi 'Asrın Vebası: Narsisizm İlleti' (Kaknüs)."),
  ("Miller", "Alice Miller", "Das Drama des begabten Kindes und die Suche nach dem wahren Selbst", "1979", "drama des begabten", "Çocuğun ebeveynin narsisistik ihtiyaçlarına göre şekillenmesi; 'yetenekli çocuk'; sahte benlik; depresyon ve büyüklenme; sonradan psikanalizden ayrılması. Türkçesi 'Yetenekli Çocuğun Dramı'."),
 ]),
 "A6": ("Narsisizm: popüler bilim ve korunma", "A", [
  ("Malkin", "Craig Malkin", "Rethinking Narcissism: The Bad—and Surprising Good—About Feeling Special", "2015", "rethinking narcissism", "Harvard'da klinik psikolog; narsisizm yelpazesi (0–10), sağlıklı narsisizm, 'echoism' kavramı; Türkçesi 'Narsisizme Yeni Bir Bakış' olabilir."),
  ("Durvasula", "Ramani Durvasula", "It's Not You: Identifying and Healing from Narcissistic People", "2024", "it's not you", "Klinik psikolog; 'narsisistik istismar' çerçevesi; ilişkiden çıkma ve iyileşme; önceki kitapları Should I Stay or Should I Go? (2015) ve Don't You Know Who I Am? (2019) bir paragrafla an; sosyal medya etkisi ve eleştirisi."),
  ("McBride", "Karyl McBride", "Will I Ever Be Good Enough? Healing the Daughters of Narcissistic Mothers", "2008", "will i ever be good enough", "Aile terapisti; narsisistik anne tipleri; kızlarda iz; iyileşme programı; bilimsel dayanak: klinik deneyim ve anketler."),
  ("Behary", "Wendy T. Behary", "Disarming the Narcissist: Surviving and Thriving with the Self-Absorbed", "2008", "disarming the narcissist", "Şema terapisi; narsisistik kişinin 'yalnız çocuk' ve 'kendini yücelten' kipleri; empatik yüzleşme; ilişkide kalanlar için."),
 ]),
 "A7": ("Psikolojik istismar ve zorlayıcı denetim", "A", [
  ("Bancroft", "Lundy Bancroft", "Why Does He Do That? Inside the Minds of Angry and Controlling Men", "2002", "why does he do that", "İstismarcı erkek programlarında 15 yılı aşkın deneyim; istismarcı tipleri; istismarın değerlerden ve hak iddiasından doğduğu tezi (öfke sorunu değil); çocuklar; değişimin işaretleri."),
  ("Stark", "Evan Stark", "Coercive Control: How Men Entrap Women in Personal Life", "2007", "coercive control", "Sosyolog ve sosyal hizmet uzmanı; şiddet odaklı modelin eleştirisi; özgürlüğün kısıtlanması; İngiltere 2015 yasasına etkisi."),
  ("Herman", "Judith Lewis Herman", "Trauma and Recovery: The Aftermath of Violence—From Domestic Abuse to Political Terror", "1992", "trauma and recovery", "Harvard psikiyatr; karmaşık TSSB önerisi; tutsaklık durumu; esir alanın taktikleri (Amnesty'nin zorlama şeması); iyileşmenin üç evresi. Türkçesi 'Travma ve İyileşme'."),
  ("Hirigoyen", "Marie-France Hirigoyen", "Le harcèlement moral: la violence perverse au quotidien", "1998", "harcelement moral", "Fransız psikiyatr; 'pervers narcissique' kavramını yaygınlaştırdı; çift ve iş yerinde manevi taciz; Fransa'da 2002 iş yasasına etkisi; Türkçesi var mı katalogdan."),
 ]),
 "A8": ("Gaslighting, şantaj, sözel istismar ve korkunun armağanı", "A", [
  ("Stern", "Robin Stern", "The Gaslight Effect: How to Spot and Survive the Hidden Manipulation Others Use to Control Your Life", "2007", "gaslight effect", "Yale Duygusal Zekâ Merkezi; gaslighting'in üç evresi (inanmama, savunma, depresyon); üç gaslighter tipi (iyi adam, cazibeli, korkutan); 2018 yeni baskı."),
  ("Forward", "Susan Forward ve Donna Frazier", "Emotional Blackmail: When the People in Your Life Use Fear, Obligation, and Guilt to Manipulate You", "1997", "emotional blackmail", "FOG kavramı; şantajcının dört tipi (cezalandırıcı, kendini cezalandırıcı, acı çeken, kışkırtıcı); altı aşama; karşılık stratejileri. Türkçesi 'Duygusal Şantaj'."),
  ("Evans", "Patricia Evans", "The Verbally Abusive Relationship: How to Recognize It and How to Respond", "1992", "verbally abusive", "Sözel istismarın kategorileri (alıkoyma, karşı çıkma, küçümseme, şaka kılıfı, engelleme, suçlama vb.); iki 'gerçeklik' (Reality I ve II); yanıtlar."),
  ("de Becker", "Gavin de Becker", "The Gift of Fear: Survival Signals That Protect Us from Violence", "1997", "gift of fear", "Güvenlik danışmanı; sezgi ve tehlike işaretleri (zorla ekip oluşturma, cazibe, fazla ayrıntı, 'hayır'ı yok sayma, istenmeyen söz verme vb.); ısrarlı takip; eleştiriler (anekdotlara dayanma)."),
 ]),
 "A9": ("Tarikat ve zihin denetimi", "A", [
  ("Hassan", "Steven Hassan", "Combating Cult Mind Control", "1988", "combating cult mind control", "Eski Birleşme Kilisesi üyesi; BITE modeli (davranış, bilgi, düşünce, duygu denetimi); 'çıkış danışmanlığı'; 'deprogramming' tartışması; sonraki Freedom of Mind (2012) bir cümleyle; eleştiriler (beyin yıkama kavramının akademik itirazları)."),
  ("Singer", "Margaret Thaler Singer ve Janja Lalich", "Cults in Our Midst: The Hidden Menace in Our Everyday Lives", "1995", "cults in our midst", "Klinik psikolog; düşünce reformu programının altı koşulu; APA'nın DIMPAC raporunu reddetmesi (1987) ve mahkemelerdeki 'beyin yıkama' tanıklıklarının çöküşü (Fishman davası 1990); 1996 genişletilmiş baskı."),
  ("Meerloo", "Joost A. M. Meerloo", "The Rape of the Mind: The Psychology of Thought Control, Menticide, and Brainwashing", "1956", "rape of the mind", "Hollandalı psikiyatr; 'menticide' kavramı; Kore Savaşı ve totaliter rejimler; Türkçesi 'Zihne Saldırı - Totaliter Rejimlerde Beyin Yıkama' katalogda var."),
  ("Taylor", "Kathleen Taylor", "Brainwashing: The Science of Thought Control", "2004", "brainwashing", "Oxford nörobilimci; beyin yıkamanın 'ethereal ideas' ve sinirbilimiyle açıklanması; inançların değişmesinin mekanizmaları; 2017 genişletilmiş baskı."),
 ]),
 "A10": ("Aldatma ve popüler karanlık psikoloji", "A", [
  ("Ekman", "Paul Ekman", "Telling Lies: Clues to Deceit in the Marketplace, Politics, and Marriage", "1985", "telling lies", "Duygu ifadeleri araştırmacısı; sızıntı ipuçları, mikro ifadeler, 'Othello hatası'; SPOT programı ve Lie to Me dizisi; Bond ve DePaulo 2006 ve Vrij eleştirileri; Türkçesi 'Yalan Söylediğimi Nasıl Anladın?' olabilir."),
  ("Levine", "Timothy R. Levine", "Duped: Truth-Default Theory and the Social Science of Lying and Deception", "2019", "duped", "Alabama'da iletişim profesörü; doğruluk varsayılanı kuramı (truth-default theory); çoğu insan çoğu zaman dürüsttür; 'birkaç üretken yalancı'; yalan tespitinde bağlam ve kanıtın sözel ipuçlarından önemli olması."),
  ("Bandler", "Richard Bandler ve John Grinder", "Frogs into Princes: Neuro Linguistic Programming", "1979", "frogs into princes", "NLP'nin popüler giriş kitabı (atölye dökümleri); 'The Structure of Magic' (1975) ile kuruluş; temsil sistemleri, göz erişim ipuçları, çapalama, yeniden çerçeveleme; Milton Erickson ve Virginia Satir'in modellenmesi; bilimsel değerlendirme (Sharpley 1987, Witkowski 2010, Wiseman 2012); 'gizli ikna' ve pickup kültürüne etkisi."),
  ("Cooper", "Kendi-yayını 'Dark Psychology' kitapları (William Cooper, Jonathan Mind, Michael Pace, Steven Turner, Edward Benedict, Arthur Horn ve diğerleri)", "Dark Psychology (tür profili)", "2015 sonrası", "dark psychology", "TEK BİR KİTAP DEĞİL, TÜR PROFİLİ: en çok satan ve en çok yorum alan 5–6 kitabı adlarıyla tanıt (Goodreads ve Amazon sayfaları); ortak içindekiler; yazarların gerçekliği (takma ad, yazar biyografisi yokluğu); kaynakları (Cialdini, Greene, NLP, Carnegie); yinelenen yanlış ya da abartılı iddialar; yapay zekâ üretimi kaygısı; Türkçeye çevrilenler (Tristan Cole 'İnsan Hackerlığı', Don Barlow 'Gaslighting', Sarah Davies ve diğerleri katalogda var). Şablonun 'Yapısı' bölümünde tipik içindekiler; 'Bilimsel dayanağı' bölümünde ayrıntılı değerlendirme."),
 ]),
}
B = {
 "B1": ("Karanlık kişilik: akademik derlemeler ve kavramlar", [
  ("Kowalski", "Robin M. Kowalski (ed.)", "Aversive Interpersonal Behaviors", "1997", "aversive interpersonal", ""),
  ("Jonason", "Peter K. Jonason (ed.)", "Shining Light on the Dark Side of Personality: Measurement Properties and Theoretical Advances", "2022", "shining light", ""),
  ("Miller", "Joshua D. Miller ve Donald R. Lynam (ed.)", "The Handbook of Antagonism: Conceptualizations, Assessment, Consequences, and Treatment of the Low End of Agreeableness", "2019", "handbook of antagonism", "Karanlık üçlünün çekirdeğinin düşük uyumluluk (antagonizm) olduğu tezi."),
  ("Furnham", "Adrian Furnham", "The Elephant in the Boardroom: The Causes of Leadership Derailment", "2010", "elephant in the boardroom", "Hogan Gelişim Envanteri'nin 11 'karanlık' eğilimi; liderlikte raydan çıkma."),
  ("McCarthy-Jones", "Simon McCarthy-Jones", "Spite: The Upside of Your Dark Side", "2020", "spite", ""),
  ("Bandura", "Albert Bandura", "Moral Disengagement: How People Do Harm and Live with Themselves", "2016", "moral disengagement", "Sekiz ahlaki bağlantısızlık mekanizması."),
 ]),
 "B2": ("Kötülük: soykırımdan gündelik hayata", [
  ("Staub", "Ervin Staub", "The Roots of Evil: The Origins of Genocide and Other Group Violence", "1989", "roots of evil", ""),
  ("Waller", "James Waller", "Becoming Evil: How Ordinary People Commit Genocide and Mass Killing", "2002", "becoming evil", ""),
  ("Shaw", "Julia Shaw", "Evil: The Science Behind Humanity's Dark Side (İngiltere: Making Evil)", "2019", "evil", "Türkçesi 'Kötülük' olabilir."),
  ("Smith", "David Livingstone Smith", "Less Than Human: Why We Demean, Enslave, and Exterminate Others", "2011", "less than human", ""),
  ("Peck", "M. Scott Peck", "People of the Lie: The Hope for Healing Human Evil", "1983", "people of the lie", "Türkçesi 'Yalanın İnsanları' olabilir; dinî çerçeve ve 'kötü insan' tanısı tartışması."),
  ("Fromm", "Erich Fromm", "The Anatomy of Human Destructiveness", "1973", "anatomy of human destructiveness", "Kötücül saldırganlık, sadizm ve nekrofili; Hitler ve Himmler vaka çözümlemeleri; Türkçesi 'İnsandaki Yıkıcılığın Kökenleri'."),
 ]),
 "B3": ("Psikopati: akademik eserler", [
  ("Patrick", "Christopher J. Patrick (ed.)", "Handbook of Psychopathy", "2006", "handbook of psychopathy", "2. baskı 2018."),
  ("Blair", "James Blair, Derek Mitchell, Karina Blair", "The Psychopath: Emotion and the Brain", "2005", "psychopath: emotion", "Amigdala işlev bozukluğu ve bütünleşik duygu sistemleri modeli."),
  ("Lykken", "David T. Lykken", "The Antisocial Personalities", "1995", "antisocial personalities", "Korkusuzluk kuramı; sosyopat ile psikopat ayrımı (ebeveynlik ile mizaç)."),
  ("Meloy", "J. Reid Meloy", "The Psychopathic Mind: Origins, Dynamics, and Treatment", "1988", "psychopathic mind", ""),
  ("McCord", "William McCord ve Joan McCord", "The Psychopath: An Essay on the Criminal Mind", "1964", "psychopath", ""),
  ("Viding", "Essi Viding", "Psychopathy: A Very Short Introduction", "2019", "very short introduction", "Çocuklarda duygusuz-soğuk özellikler; UCL."),
 ]),
 "B4": ("Psikopati: anılar, beyin ve iş dünyası", [
  ("Marsh", "Abigail Marsh", "The Fear Factor: How One Emotion Connects Altruists, Psychopaths, and Everyone In-Between", "2017", "fear factor", ""),
  ("Fallon", "James Fallon", "The Psychopath Inside: A Neuroscientist's Personal Journey into the Dark Side of the Brain", "2013", "psychopath inside", ""),
  ("Thomas", "M. E. Thomas (takma ad)", "Confessions of a Sociopath: A Life Spent Hiding in Plain Sight", "2013", "confessions of a sociopath", ""),
  ("Gagne", "Patric Gagne", "Sociopath: A Memoir", "2024", "sociopath", ""),
  ("Boddy", "Clive R. Boddy", "Corporate Psychopaths: Organizational Destroyers", "2011", "corporate psychopaths", "Babiak ve Hare önceki raporda."),
  ("Samenow", "Stanton E. Samenow", "Inside the Criminal Mind", "1984", "inside the criminal mind", "Yochelson ile 'The Criminal Personality' (1976) bir cümleyle."),
 ]),
 "B5": ("Psikopatiden korunma ve popüler anlatılar", [
  ("Stout", "Martha Stout", "Outsmarting the Sociopath Next Door: How to Protect Yourself Against a Ruthless Manipulator", "2020", "outsmarting", ""),
  ("Brown", "Sandra L. Brown", "Women Who Love Psychopaths: Inside the Relationships of Inevitable Harm", "2005", "women who love psychopaths", ""),
  ("Erikson", "Thomas Erikson", "Omgiven av psykopater (Surrounded by Psychopaths)", "2017", "omgiven av psykopater", "Türkçesi 'Etrafım Psikopatlarla Dolu' katalogda; DISC renk modeline dayanır; bilimsel eleştirisi (İsveç'te sahte bilim ödülü)."),
  ("Łobaczewski", "Andrew M. Łobaczewski", "Political Ponerology: A Science on the Nature of Evil Adjusted for Political Purposes", "1998", "political ponerology", "Yazılış 1980'ler; hakemli bilim değil; sonradan komplo çevrelerinde popülerliği."),
  ("Oakley", "Barbara Oakley", "Evil Genes: Why Rome Fell, Hitler Rose, Enron Failed, and My Sister Stole My Mother's Boyfriend", "2007", "evil genes", ""),
  ("Navarro", "Joe Navarro ve Toni Sciarra Poynter", "Dangerous Personalities: An FBI Profiler Shows You How to Identify and Protect Yourself from Harmful People", "2014", "dangerous personalities", "Dört kişilik (narsisistik, duygusal olarak dengesiz, paranoyak, yırtıcı); kontrol listeleri; eleştiri."),
 ]),
 "B6": ("Narsisizm: klinik ve bilimsel eserler", [
  ("Kohut", "Heinz Kohut", "The Analysis of the Self", "1971", "analysis of the self", "Kendilik psikolojisi; ayna ve idealleştirme aktarımları; Türkçesi 'Kendiliğin Çözümlenmesi'."),
  ("Lowen", "Alexander Lowen", "Narcissism: Denial of the True Self", "1983", "narcissism", "Biyoenerjetik analiz; Türkçesi 'Narsisizm: Gerçek Benliğin İnkârı'."),
  ("Ronningstam", "Elsa F. Ronningstam", "Identifying and Understanding the Narcissistic Personality", "2005", "identifying and understanding", ""),
  ("Campbell", "W. Keith Campbell ve Carolyn Crist", "The New Science of Narcissism: Understanding One of the Greatest Psychological Challenges of Our Time—and What You Can Do About It", "2020", "new science of narcissism", "Üç yönlü (trifurcated) model: hak iddiası/antagonizm çekirdeği, büyüklenmeci (agentic), kırılgan."),
  ("Vaknin", "Sam Vaknin", "Malignant Self-Love: Narcissism Revisited", "1999", "malignant self-love", "Yazar kendini narsist olarak tanıtır; akademik itibarı tartışmalı; 'narsisistik arz' kavramını yaygınlaştırdı."),
  ("Dombek", "Kristin Dombek", "The Selfishness of Others: An Essay on the Fear of Narcissism", "2016", "selfishness of others", "Narsisizm söylemine eleştirel deneme."),
 ]),
 "B7": ("Narsisizm: aile, partner ve iyileşme", [
  ("Durvasula", "Ramani Durvasula", "Don't You Know Who I Am? How to Stay Sane in an Era of Narcissism, Entitlement, and Incivility", "2019", "don't you know who i am", ""),
  ("Hotchkiss", "Sandy Hotchkiss", "Why Is It Always About You? The Seven Deadly Sins of Narcissism", "2002", "why is it always about you", "Yedi ölümcül günah: utanmazlık, büyülü düşünce, kibir, haset, hak iddiası, sömürü, sınır tanımama."),
  ("Golomb", "Elan Golomb", "Trapped in the Mirror: Adult Children of Narcissists in Their Struggle for Self", "1992", "trapped in the mirror", ""),
  ("Burgo", "Joseph Burgo", "The Narcissist You Know: Defending Yourself Against Extreme Narcissists in an All-About-Me Age", "2015", "narcissist you know", ""),
  ("Arabi", "Shahida Arabi", "Power: Surviving and Thriving After Narcissistic Abuse", "2017", "power", "Becoming the Narcissist's Nightmare (2016) bir cümleyle; katalogda 'Narsist ve Psikopatlarla Travma Bağlarını Koparmak' var: hangi kitabın çevirisi olduğunu bul."),
  ("Bouchoux", "Jean-Charles Bouchoux", "Les pervers narcissiques", "2009", "pervers narcissiques", "Fransız psikanalist; Racamier ve Hirigoyen geleneği; Türkçesi 'Narsist Sapkınlar' katalogda."),
 ]),
 "B8": ("İstismar: aile içi şiddet ve tehlike", [
  ("Hill", "Jess Hill", "See What You Made Me Do: Power, Control and Domestic Abuse", "2019", "see what you made me do", "Avustralya; Stella Ödülü 2020."),
  ("Snyder", "Rachel Louise Snyder", "No Visible Bruises: What We Don't Know About Domestic Violence Can Kill Us", "2019", "no visible bruises", "Boğma (strangulation) ve ölümcüllük riski; yüksek risk ekipleri."),
  ("Monckton Smith", "Jane Monckton Smith", "In Control: Dangerous Relationships and How They End in Murder", "2021", "in control", "Cinayete giden sekiz aşama."),
  ("Fontes", "Lisa Aronson Fontes", "Invisible Chains: Overcoming Coercive Control in Your Intimate Relationship", "2015", "invisible chains", ""),
  ("Walker", "Lenore E. Walker", "The Battered Woman", "1979", "battered woman", "Şiddet döngüsü (gerilim, patlama, balayı) ve 'öğrenilmiş çaresizlik'; sonraki eleştiriler."),
  ("Dutton", "Donald G. Dutton", "The Abusive Personality: Violence and Control in Intimate Relationships", "1998", "abusive personality", ""),
 ]),
 "B9": ("İstismar: aile, iş yeri ve ihanet", [
  ("Forward", "Susan Forward ve Craig Buck", "Toxic Parents: Overcoming Their Hurtful Legacy and Reclaiming Your Life", "1989", "toxic parents", "Türkçesi 'Zehirli Ana Babalar' olabilir."),
  ("Forward", "Susan Forward ve Joan Torres", "Men Who Hate Women and the Women Who Love Them", "1986", "men who hate women", ""),
  ("Leymann", "Heinz Leymann", "Mobbing: Psychoterror am Arbeitsplatz und wie man sich dagegen wehren kann", "1993", "mobbing", "İş yerinde mobbingin 45 davranışı (LIPT) ve beş aşaması."),
  ("Namie", "Gary Namie ve Ruth Namie", "The Bully at Work: What You Can Do to Stop the Hurt and Reclaim Your Dignity on the Job", "2000", "bully at work", ""),
  ("Carnes", "Patrick J. Carnes", "The Betrayal Bond: Breaking Free of Exploitive Relationships", "1997", "betrayal bond", "Travma bağı; kontrol listesi."),
  ("Freyd", "Jennifer J. Freyd ve Pamela J. Birrell", "Blind to Betrayal: Why We Fool Ourselves We Aren't Being Fooled", "2013", "blind to betrayal", "İhanet travması kuramı; DARVO ile bağlantı."),
 ]),
 "B10": ("Gaslighting ve manipülasyondan korunma", [
  ("Abramson", "Kate Abramson", "On Gaslighting", "2024", "on gaslighting", "Princeton University Press; ahlak felsefesi; Türkçesi katalogda (Timaş olabilir)."),
  ("Sarkis", "Stephanie Moulton Sarkis", "Gaslighting: Recognize Manipulative and Emotionally Abusive People—and Break Free", "2018", "gaslighting", ""),
  ("Braiker", "Harriet B. Braiker", "Who's Pulling Your Strings? How to Break the Cycle of Manipulation and Regain Control of Your Life", "2004", "who's pulling your strings", ""),
  ("Engel", "Beverly Engel", "The Emotionally Abusive Relationship: How to Stop Being Abused and How to Stop Abusing", "2002", "emotionally abusive relationship", ""),
  ("Bernstein", "Albert J. Bernstein", "Emotional Vampires: Dealing with People Who Drain You Dry", "2001", "emotional vampires", ""),
  ("Mirza", "Debbie Mirza", "The Covert Passive-Aggressive Narcissist: Recognizing the Traits and Finding Healing After Hidden Emotional and Psychological Abuse", "2017", "covert passive", "Türkçesi 'Gizli Pasif-Agresif Narsist' katalogda; kendi yayını, koç; bilimsel dayanağı zayıf."),
 ]),
 "B11": ("Tarikatlar ve beyin yıkama tartışması", [
  ("Schein", "Edgar H. Schein, Inge Schneier ve Curtis H. Barker", "Coercive Persuasion: A Socio-Psychological Analysis of the 'Brainwashing' of American Civilian Prisoners by the Chinese Communists", "1961", "coercive persuasion", "Çözme-değiştirme-yeniden dondurma modeli."),
  ("Lalich", "Janja Lalich", "Bounded Choice: True Believers and Charismatic Cults", "2004", "bounded choice", "Heaven's Gate ve Demokratik İşçi Partisi vakaları; 'sınırlı seçim' kavramı."),
  ("Barker", "Eileen Barker", "The Making of a Moonie: Choice or Brainwashing?", "1984", "making of a moonie", "Beyin yıkama tezine ampirik itiraz: atölyeye katılanların çoğu katılmadı."),
  ("Stein", "Alexandra Stein", "Terror, Love and Brainwashing: Attachment in Cults and Totalitarian Systems", "2017", "terror, love", "Bağlanma kuramı; 'korku içinde sevgi' ve yalıtılmış ilişki ağı."),
  ("Montell", "Amanda Montell", "Cultish: The Language of Fanaticism", "2021", "cultish", "Dilbilimci; tarikat dilinin gündelik yerlerde (fitness, MLM, sosyal medya) kullanımı."),
  ("Sargant", "William Sargant", "Battle for the Mind: A Physiology of Conversion and Brain-Washing", "1957", "battle for the mind", "Pavlov'cu açıklama; tartışmalı psikiyatri uygulamaları."),
 ]),
 "B12": ("Türkiye'den: Türkçe yazılmış kitaplar ve Türkçe pazar", [
  ("Tülüce", "Hicran Tülüce", "Karanlık Empat: Narsist, Psikopat, Makyavelist", "doğrulanmadı", "karanlik empat", "Psikolog (Bianet'te yazıları); katalogda en çok sorguda çıkan kitap; yayınevini ve yılını katalogdan ya da kitap sayfasından bul."),
  ("Tarhan", "Nevzat Tarhan", "Kötülük Psikolojisi ve Toksik İlişkiler", "doğrulanmadı", "kotuluk psikolojisi", "Psikiyatr, Üsküdar Üniversitesi kurucu rektörü; Timaş; kötülüğün nörobiyolojisi ve toksik ilişkiler; dinî-ahlaki çerçeve."),
  ("Özakkaş", "Tahir Özakkaş", "Narsisizm Üzerine Konuşmalar ve Olgu Sunumu", "doğrulanmadı", "narsisizm uzerine", "Psikiyatr ve psikanalist; Kohut ve Kernberg geleneğinin Türkçe anlatımı."),
  ("Tınaz", "Pınar Tınaz", "İşyerinde Psikolojik Taciz (Mobbing)", "2006", "isyerinde psikolojik taciz", "Akademisyen; Beta; Türkiye'de mobbing yazınının ilk kitaplarından; TBK 417 öncesi ve sonrası."),
  ("Efendi", "Emin Efendi", "Karanlık Psikoloji - Manipülasyon ve Manipülasyon Oyunları - Karanlık Psikoloji", "doğrulanmadı", "karanlik psikoloji", "Türkçe yazılmış popüler 'karanlık psikoloji' kitapları; yazarın kim olduğu (takma ad mı?) doğrulanmadı; içerik ve kaynak kalitesini değerlendir."),
  ("Cole", "Türkçeye çevrilen kendi-yayını kitaplar ve diziler (Gece Kitaplığı 'Karanlık Psikoloji ile...' dizisi, Akıl İzi 'Karanlık Psikoloji' seti, Tristan Cole, Don Barlow, Osman Kutlu ve diğerleri)", "Türkçe 'Karanlık Psikoloji' rafı (tür profili)", "2020 sonrası", "karanlik psikoloji", "TEK KİTAP DEĞİL, TÜRKÇE RAF PROFİLİ: ${K}/ek/parcalar/tr_pazar_temiz.json dosyasını tek python3 komutuyla özetle; dizileri ve en çok görünen başlıkları adlarıyla say; yazar ve özgün künye bilgisinin yokluğunu, çevirilerin kaynağını, kapak vaatlerini değerlendir; okura seçim ölçütleri ver. 'Yapısı' bölümünde raftaki alt türler (ikna ve etkileme, narsist kitapları, gaslighting, beden dili, zihin kontrolü)."),
 ]),
 "B13": ("Aldatma, kanma ve dolandırıcılık", [
  ("Vrij", "Aldert Vrij", "Detecting Lies and Deceit: The Psychology of Lying and the Implications for Professional Practice", "2000", "detecting lies", "2. baskı 2008; sözel ve sözsüz ipuçlarının zayıflığı; bilişsel yük yaklaşımı."),
  ("Simons", "Daniel Simons ve Christopher Chabris", "Nobody's Fool: Why We Get Taken In and What We Can Do About It", "2023", "nobody's fool", "Dört alışkanlık (odak, öngörü, bağlılık, verimlilik) ve dört kanca (tutarlılık, aşinalık, kesinlik, güçlü etki)."),
  ("Greenspan", "Stephen Greenspan", "Annals of Gullibility: Why We Get Duped and How to Avoid It", "2009", "annals of gullibility", "Yazarın Madoff'a yatırım yapıp kaybetmesi ironisi."),
  ("Dove", "Martina Dove", "The Psychology of Fraud, Persuasion and Scam Techniques: Understanding What Makes Us Vulnerable", "2020", "psychology of fraud", ""),
  ("Ariely", "Dan Ariely", "The (Honest) Truth About Dishonesty: How We Lie to Everyone—Especially Ourselves", "2012", "honest", "Sonraki veri skandalı (2021 araba sigortası verisi; Data Colada) mutlaka anılmalı."),
  ("Rowland", "Ian Rowland", "The Full Facts Book of Cold Reading", "1998", "cold reading", "Barnum ifadeleri, Gökkuşağı Hilesi, Rainbow Ruse; şarlatanlığın tekniği."),
 ]),
 "B14": ("Gizli ikna, NLP mirası, pickup ve popüler manipülasyon", [
  ("Strauss", "Neil Strauss", "The Game: Penetrating the Secret Society of Pickup Artists", "2005", "the game", "Gazeteci; Mystery ve Project Hollywood; sonraki 'The Truth' (2015) ve pişmanlık; eleştiriler."),
  ("Hogan", "Kevin Hogan ve James Speakman", "Covert Persuasion: Psychological Tactics and Tricks to Win the Game", "2006", "covert persuasion", ""),
  ("Hughes", "Chase Hughes", "The Ellipsis Manual: Analysis and Engineering of Human Behavior", "2017", "ellipsis manual", "Kendi yayını; 'eski askerî davranış uzmanı' iddiası; bilimsel dayanağı zayıf."),
  ("Markovik", "Erik von Markovik (Mystery) ve Chris Odom", "The Mystery Method: How to Get Beautiful Women Into Bed", "2007", "mystery method", "Negging teriminin popülerleştiricisi."),
  ("Tomassi", "Rollo Tomassi", "The Rational Male", "2013", "rational male", "Manosphere ve 'red pill'; eleştiriler (Laura Bates 'Men Who Hate Women' 2020)."),
  ("Kirschner", "Josef Kirschner", "Manipulieren – aber richtig: Die acht Gesetze der Menschenbeeinflussung", "1974", "manipulieren", "Avusturyalı yazar; Türkçesi katalogda 'Manipülasyon Ama Nasıl?' olabilir; 'sekiz yasa'."),
 ]),
}
liste, gruplar = [], {}
n = 0
for gid, (ad, kat, kit) in G.items():
    gruplar[gid] = {"ad": ad, "katman": "A", "kitaplar": []}
    for soy, yazar, oad, yil, anahtar, not_ in kit:
        n += 1; kod = f"K{n:03d}"
        b = bul(soy, anahtar)
        ip = (b["gerekce"] + " " if b else "") + not_
        if b and b.get("turkce_ad"): ip += f" Keşif ajanına göre Türkçe adı: {b['turkce_ad']}."
        dosya = f"{kod}_{re.sub(r'[^a-z0-9]+', '_', f(soy))[:18]}"
        gruplar[gid]["kitaplar"].append({"dosya": dosya, "kunye": f"{yazar} — {oad} ({yil})", "ipucu": ip.strip()})
        liste.append({"dosya": dosya, "grup": gid, "katman": "A", "yazar": yazar, "soyad": soy, "ozgun_ad": oad, "yil": yil, "turkce_ad": (b or {}).get("turkce_ad", "")})
for gid, (ad, kit) in B.items():
    gruplar[gid] = {"ad": ad, "katman": "B", "kitaplar": []}
    for soy, yazar, oad, yil, anahtar, not_ in kit:
        n += 1; kod = f"K{n:03d}"
        b = bul(soy, anahtar)
        ip = (b["gerekce"] + " " if b else "") + not_
        if b and b.get("turkce_ad"): ip += f" Keşif ajanına göre Türkçe adı: {b['turkce_ad']}."
        dosya = f"{kod}_{re.sub(r'[^a-z0-9]+', '_', f(soy))[:18]}"
        gruplar[gid]["kitaplar"].append({"dosya": dosya, "kunye": f"{yazar} — {oad} ({yil})", "ipucu": (ip.strip() or "Keşif notu yok; künyeyi ve içeriği kaynaktan kur.").replace("${K}", K)})
        liste.append({"dosya": dosya, "grup": gid, "katman": "B", "yazar": yazar, "soyad": soy, "ozgun_ad": oad, "yil": yil, "turkce_ad": (b or {}).get("turkce_ad", "")})
json.dump(liste, open(K + "/parcalar/kitap_listesi.json", "w"), ensure_ascii=False, indent=1)
json.dump(gruplar, open(K + "/parcalar/gruplar.json", "w"), ensure_ascii=False, indent=1)
eksik = [x["dosya"] for g in gruplar.values() for x in g["kitaplar"] if x["ipucu"].startswith("Keşif notu yok")]
print(len(liste), "kitap,", len(gruplar), "grup; A:", sum(1 for x in liste if x["katman"] == "A"), "B:", sum(1 for x in liste if x["katman"] == "B"))
print("kesif notu bulunamayan:", eksik)
