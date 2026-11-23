#!/usr/bin/env python3
"""Elestirmen sonrasi ikinci katmani (B) yeniden kurar. A katmani (K001-K040) aynen kalir.
Eski katalog sonuclari korunur (soyad + ad eslesmesiyle tasinir); yeni kitaplar 'yeni' diye isaretlenir."""
import json, os, re, unicodedata, glob
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
exec(open(os.path.join(K, "araclar", "liste_kur.py")).read().split("# (grup, kod")[0])  # f(), kesif, bul()
eski = json.load(open(K + "/parcalar/kitap_listesi_eski.json"))
eski_kat = json.load(open(K + "/dogrulama/turkce_katalog_eski.json"))
A = [b for b in eski if b["katman"] == "A"]
gruplar = {g: v for g, v in json.load(open(K + "/parcalar/gruplar.json")).items() if v["katman"] == "A"}
def eski_bul(soy, oad):
    for b in eski:
        if b["katman"] == "B" and f(soy) == f(b["soyad"]) and f(oad)[:15] == f(b["ozgun_ad"])[:15]:
            return b
    return None
eski_g = json.load(open(K + "/parcalar/gruplar.json"))
def eski_ipucu(dosya):
    for g in eski_g.values():
        for x in g["kitaplar"]:
            if x["dosya"] == dosya: return x["ipucu"]
    return ""
Y = "YENİ"   # eski listede olmayan
B = {
 "B1": ("Karanlık kişilik: akademik derlemeler ve kavramlar", [
  ("Jonason", "Peter K. Jonason (ed.)", "Shining Light on the Dark Side of Personality: Measurement Properties and Theoretical Advances", "2022", ""),
  ("Miller", "Joshua D. Miller ve Donald R. Lynam (ed.)", "The Handbook of Antagonism: Conceptualizations, Assessment, Consequences, and Treatment of the Low End of Agreeableness", "2019", ""),
  ("Furnham", "Adrian Furnham", "The Elephant in the Boardroom: The Causes of Leadership Derailment", "2010", ""),
  ("McCarthy-Jones", "Simon McCarthy-Jones", "Spite: The Upside of Your Dark Side", "2020", ""),
  ("Bandura", "Albert Bandura", "Moral Disengagement: How People Do Harm and Live with Themselves", "2016", "Open Library 2015 gösteriyor; yılı doğrula."),
  ("Campbell", "W. Keith Campbell ve Carolyn Crist", "The New Science of Narcissism: Understanding One of the Greatest Psychological Challenges of Our Time—and What You Can Do About It", "2020", ""),
 ]),
 "B2": ("Narsisizm: klinik bilim, tartışmalı sesler ve eleştiri", [
  ("Ronningstam", "Elsa F. Ronningstam", "Identifying and Understanding the Narcissistic Personality", "2005", ""),
  ("Vaknin", "Sam Vaknin", "Malignant Self-Love: Narcissism Revisited", "1999", "Basılı ilk baskı 2001 olarak da geçer; doğrula."),
  ("Dombek", "Kristin Dombek", "The Selfishness of Others: An Essay on the Fear of Narcissism", "2016", ""),
  ("Burgo", "Joseph Burgo", "The Narcissist You Know: Defending Yourself Against Extreme Narcissists in an All-About-Me Age", "2015", ""),
  ("Durvasula", "Ramani Durvasula", "Don't You Know Who I Am? How to Stay Sane in an Era of Narcissism, Entitlement, and Incivility", "2019", "Aynı yazarın It's Not You (2024) kitabı çekirdek katmanda ayrıca anlatılıyor; onu yineleme."),
  ("Golomb", "Elan Golomb", "Trapped in the Mirror: Adult Children of Narcissists in Their Struggle for Self", "1992", ""),
 ]),
 "B3": ("Gaslighting, narsisistik istismar ve korunma", [
  ("Arabi", "Shahida Arabi", "Power: Surviving and Thriving After Narcissistic Abuse", "2017", ""),
  ("Bouchoux", "Jean-Charles Bouchoux", "Les pervers narcissiques", "2009", ""),
  ("Abramson", "Kate Abramson", "On Gaslighting", "2024", ""),
  ("Sarkis", "Stephanie Moulton Sarkis", "Gaslighting: Recognize Manipulative and Emotionally Abusive People—and Break Free", "2018", ""),
  ("Braiker", "Harriet B. Braiker", "Who's Pulling Your Strings? How to Break the Cycle of Manipulation and Regain Control of Your Life", "2004", ""),
  ("Engel", "Beverly Engel", "The Emotionally Abusive Relationship: How to Stop Being Abused and How to Stop Abusing", "2002", ""),
 ]),
 "B4": ("Psikopati: akademik eserler", [
  ("Patrick", "Christopher J. Patrick (ed.)", "Handbook of Psychopathy", "2006", ""),
  ("Blair", "James Blair, Derek Mitchell, Karina Blair", "The Psychopath: Emotion and the Brain", "2005", ""),
  ("Lykken", "David T. Lykken", "The Antisocial Personalities", "1995", ""),
  ("Meloy", "J. Reid Meloy", "The Psychopathic Mind: Origins, Dynamics, and Treatment", "1988", ""),
  ("Viding", "Essi Viding", "Psychopathy: A Very Short Introduction", "2019", ""),
  ("Samenow", "Stanton E. Samenow", "Inside the Criminal Mind", "1984", ""),
 ]),
 "B5": ("Psikopati ve kötülük: anılar ve popüler bilim", [
  ("Marsh", "Abigail Marsh", "The Fear Factor: How One Emotion Connects Altruists, Psychopaths, and Everyone In-Between", "2017", ""),
  ("Fallon", "James Fallon", "The Psychopath Inside: A Neuroscientist's Personal Journey into the Dark Side of the Brain", "2013", ""),
  ("Thomas", "M. E. Thomas (takma ad)", "Confessions of a Sociopath: A Life Spent Hiding in Plain Sight", "2013", ""),
  ("Gagne", "Patric Gagne", "Sociopath: A Memoir", "2024", ""),
  ("Shaw", "Julia Shaw", "Evil: The Science Behind Humanity's Dark Side (İngiltere: Making Evil)", "2019", ""),
  ("Peck", "M. Scott Peck", "People of the Lie: The Hope for Healing Human Evil", "1983", ""),
 ]),
 "B6": ("Psikopatlar iş yerinde ve ilişkide: korunma", [
  ("Boddy", "Clive R. Boddy", "Corporate Psychopaths: Organizational Destroyers", "2011", ""),
  ("Stout", "Martha Stout", "Outsmarting the Sociopath Next Door: How to Protect Yourself Against a Ruthless Manipulator", "2020", ""),
  ("Brown", "Sandra L. Brown", "Women Who Love Psychopaths: Inside the Relationships of Inevitable Harm", "2009", "İlk baskı büyük olasılıkla 2009; 2005 yazarın How to Spot a Dangerous Man kitabının yılı olabilir; doğrula."),
  ("Łobaczewski", "Andrew M. Łobaczewski", "Political Ponerology: A Science on the Nature of Evil Adjusted for Political Purposes", "1998", "Lehçe elyazması 1984, İngilizce ilk basım 1998; yayıncısı Red Pill Press (Cassiopaea grubuyla bağlantılı); hakemli bilim değil, sözde bilim olarak değerlendirilir; bunu açıkça yaz."),
  ("Navarro", "Joe Navarro ve Toni Sciarra Poynter", "Dangerous Personalities: An FBI Profiler Shows You How to Identify and Protect Yourself from Harmful People", "2014", ""),
  ("Carnes", "Patrick J. Carnes", "The Betrayal Bond: Breaking Free of Exploitive Relationships", "1997", ""),
 ]),
 "B7": ("Kötülük: soykırım, failler ve karşı sesler", [
  ("Staub", "Ervin Staub", "The Roots of Evil: The Origins of Genocide and Other Group Violence", "1989", ""),
  ("Waller", "James Waller", "Becoming Evil: How Ordinary People Commit Genocide and Mass Killing", "2002", ""),
  ("Smith", "David Livingstone Smith", "Less Than Human: Why We Demean, Enslave, and Exterminate Others", "2011", ""),
  ("Fromm", "Erich Fromm", "The Anatomy of Human Destructiveness", "1973", ""),
  ("Stangneth", "Bettina Stangneth", "Eichmann vor Jerusalem: Das unbehelligte Leben eines Massenmörders", "2011", Y + " Tarih felsefecisi; Sassen görüşmeleri ve Arjantin dönemi belgeleriyle Eichmann'ın ideolojik bağlılığını gösterir; Arendt'in 'kötülüğün sıradanlığı' tezine en güçlü itiraz (Arendt'in kitabı çekirdek katmanda anlatılıyor). İngilizcesi Eichmann Before Jerusalem (2014)."),
  ("Lower", "Wendy Lower", "Hitler's Furies: German Women in the Nazi Killing Fields", "2013", Y + " Tarihçi; Doğu'daki Alman kadınların (hemşire, sekreter, eş) soykırıma katılımı; National Book Award finalisti; kadın failler konusunda temel eser."),
 ]),
 "B8": ("İstismar: aile içi şiddet, denetim ve tehlike", [
  ("Hill", "Jess Hill", "See What You Made Me Do: Power, Control and Domestic Abuse", "2019", ""),
  ("Snyder", "Rachel Louise Snyder", "No Visible Bruises: What We Don't Know About Domestic Violence Can Kill Us", "2019", ""),
  ("Monckton Smith", "Jane Monckton Smith", "In Control: Dangerous Relationships and How They End in Murder", "2021", ""),
  ("Fontes", "Lisa Aronson Fontes", "Invisible Chains: Overcoming Coercive Control in Your Intimate Relationship", "2015", ""),
  ("Walker", "Lenore E. Walker", "The Battered Woman", "1979", ""),
  ("Dutton", "Donald G. Dutton", "The Abusive Personality: Violence and Control in Intimate Relationships", "1998", ""),
 ]),
 "B9": ("Aile, iş yeri, çocuklar ve cinsel manipülasyon", [
  ("Forward", "Susan Forward ve Craig Buck", "Toxic Parents: Overcoming Their Hurtful Legacy and Reclaiming Your Life", "1989", ""),
  ("Leymann", "Heinz Leymann", "Mobbing: Psychoterror am Arbeitsplatz und wie man sich dagegen wehren kann", "1993", ""),
  ("Freyd", "Jennifer J. Freyd ve Pamela J. Birrell", "Blind to Betrayal: Why We Fool Ourselves We Aren't Being Fooled", "2013", ""),
  ("Salter", "Anna C. Salter", "Predators: Pedophiles, Rapists, and Other Sex Offenders: Who They Are, How They Operate, and How We Can Protect Ourselves and Our Children", "2003", "Klinik psikolog; failin hazırlama (grooming) ve aldatma taktikleri; failin kendi anlatımlarından alıntılar; çocuk koruma."),
  ("Winters", "Georgia M. Winters ve Elizabeth L. Jeglic", "Sexual Grooming: Integrating Research, Practice, Prevention, and Policy", "2022", Y + " Springer; hazırlamanın beş aşamalı modeli (Sexual Grooming Model: kurban seçimi, erişim ve yalıtma, güven ve bağ, cinsel içeriğe alıştırma, sonrasının sürdürülmesi; doğrula); ölçek (SGS); önleme; Türkçe okur için çocuk koruma uyarısı."),
  ("O'Neill", "Rachel O'Neill", "Seduction: Men, Masculinity and Mediated Intimacy", "2018", "Sosyolog; Londra'daki baştan çıkarma (pickup) endüstrisinin etnografisi; pickup kılavuzlarına (The Game, Mystery Method) eleştirel bakış; bu kitaplar listede Strauss ile temsil ediliyor."),
 ]),
 "B10": ("Tarikatlar ve beyin yıkama tartışması", [
  ("Schein", "Edgar H. Schein, Inge Schneier ve Curtis H. Barker", "Coercive Persuasion: A Socio-Psychological Analysis of the 'Brainwashing' of American Civilian Prisoners by the Chinese Communists", "1961", ""),
  ("Lalich", "Janja Lalich", "Bounded Choice: True Believers and Charismatic Cults", "2004", "Tarikattan sonra iyileşme için Lalich ve Tobias'ın Take Back Your Life (2006) kitabını bir paragrafla an."),
  ("Barker", "Eileen Barker", "The Making of a Moonie: Choice or Brainwashing?", "1984", ""),
  ("Stein", "Alexandra Stein", "Terror, Love and Brainwashing: Attachment in Cults and Totalitarian Systems", "2017", ""),
  ("Montell", "Amanda Montell", "Cultish: The Language of Fanaticism", "2021", ""),
  ("Sargant", "William Sargant", "Battle for the Mind: A Physiology of Conversion and Brain-Washing", "1957", ""),
 ]),
 "B11": ("Sorgu, dezenformasyon ve dijital manipülasyon", [
  ("Gudjonsson", "Gisli H. Gudjonsson", "The Psychology of Interrogations and Confessions: A Handbook", "2003", "İzlanda kökenli adli psikolog; Reid tekniği eleştirisi; telkine yatkınlık ölçeği (GSS); sahte itiraf türleri; Guildford Dörtlüsü gibi davalar."),
  ("Kassin", "Saul Kassin", "Duped: Why Innocent People Confess—and Why We Believe Their Confessions", "2022", "Levine'in aynı adlı (çekirdek katmandaki) kitabıyla karıştırma; sahte itiraf araştırmasının kurucularından."),
  ("Rid", "Thomas Rid", "Active Measures: The Secret History of Disinformation and Political Warfare", "2020", ""),
  ("van der Linden", "Sander van der Linden", "Foolproof: Why Misinformation Infects Our Minds and How to Build Immunity", "2023", "Aşılama kuramı (prebunking) ve Bad News oyunu; eleştiriler (etki büyüklüğü, ölçüm)."),
  ("Wylie", "Christopher Wylie", "Mindf*ck: Cambridge Analytica and the Plot to Break America", "2019", Y + " Cambridge Analytica'nın eski veri bilimcisi ve ihbarcısı; Facebook verisiyle kişilik (OCEAN) profillemesi ve psikografik hedefleme; etkinliğinin abartılı olabileceği eleştirisi (doğrula)."),
  ("Brignull", "Harry Brignull", "Deceptive Patterns: Exposing the Tricks Tech Companies Use to Control You", "2023", Y + " 'Dark patterns' terimini 2010'da ortaya atan UX tasarımcısı; aldatıcı arayüz örüntüleri (gizli maliyet, roach motel, confirmshaming, sahte aciliyet); AB ve ABD düzenlemeleri; Türkiye'de Ticaret Bakanlığı ya da KVKK düzenlemesi varsa an (doğrula)."),
 ]),
 "B12": ("Aldatma, kanma ve dolandırıcılığın bilimi", [
  ("Vrij", "Aldert Vrij", "Detecting Lies and Deceit: The Psychology of Lying and the Implications for Professional Practice", "2000", ""),
  ("Simons", "Daniel Simons ve Christopher Chabris", "Nobody's Fool: Why We Get Taken In and What We Can Do About It", "2023", ""),
  ("Greenspan", "Stephen Greenspan", "Annals of Gullibility: Why We Get Duped and How to Avoid It", "2009", ""),
  ("Dove", "Martina Dove", "The Psychology of Fraud, Persuasion and Scam Techniques: Understanding What Makes Us Vulnerable", "2020", ""),
  ("Ariely", "Dan Ariely", "The (Honest) Truth About Dishonesty: How We Lie to Everyone—Especially Ourselves", "2012", "Kitapta anlatılan 'formu en üstte imzalama' çalışması uydurulmuş veri nedeniyle 2021'de geri çekildi (Data Colada); bunu mutlaka ve ayrıntılı yaz."),
  ("Rowland", "Ian Rowland", "The Full Facts Book of Cold Reading", "1998", ""),
 ]),
 "B13": ("Dolandırıcılık türleri, sosyal mühendislik ve gizli ikna", [
  ("Mitnick", "Kevin D. Mitnick ve William L. Simon", "The Art of Deception: Controlling the Human Element of Security", "2002", "Hadnagy'nin Social Engineering'i önceki raporda; bu kitap öykülerle anlatım."),
  ("Shadel", "Doug Shadel", "Outsmarting the Scam Artists: How to Protect Yourself from the Most Clever Cons", "2012", Y + " AARP Fraud Watch; yaşlıları hedefleyen dolandırıcılık; dolandırıcıların 'ganimet' tetikleyicileri (phantom riches, kaynak itibarı, sosyal kanıt, karşılıklılık, kıtlık); Pratkanis ile Weapons of Fraud (2005) bir cümleyle."),
  ("Holmes", "Becky Holmes", "Keanu Reeves Is Not in Love with You: The Murky World of Online Romance Fraud", "2023", Y + " Romantik dolandırıcılık (romance scam); yazarın dolandırıcılarla yazışmaları ve kurban hikâyeleri; love bombing ve aciliyet taktikleri; mizahi ama ciddi."),
  ("Hogan", "Kevin Hogan ve James Speakman", "Covert Persuasion: Psychological Tactics and Tricks to Win the Game", "2006", ""),
  ("Hughes", "Chase Hughes", "The Ellipsis Manual: Analysis and Engineering of Human Behavior", "2017", ""),
  ("Strauss", "Neil Strauss", "The Game: Penetrating the Secret Society of Pickup Artists", "2005", "Mystery Method ve Rollo Tomassi gibi pickup ve manosphere kitaplarını bir paragrafla an; eleştirel bakış için O'Neill (bu listede)."),
 ]),
 "B14": ("Türkiye'den: Türkçe yazılmış kitaplar ve Türkçe pazar", [
  ("Tülüce", "Hicran Tülüce", "Karanlık Empat: Narsist, Psikopat, Makyavelist", "doğrulanmadı", ""),
  ("Tarhan", "Nevzat Tarhan", "Kötülük Psikolojisi ve Toksik İlişkiler", "doğrulanmadı", "Kitap var (Üsküdar Üniversitesi haberi: uskudar.edu.tr), yayınevi Timaş; yılı doğrula."),
  ("Özakkaş", "Tahir Özakkaş", "Narsisizm Üzerine Konuşmalar ve Olgu Sunumu", "doğrulanmadı", ""),
  ("Tınaz", "Pınar Tınaz", "İşyerinde Psikolojik Taciz (Mobbing)", "2006", ""),
  ("Cole", "Türkçeye çevrilen ve Türkçe yazılan popüler 'karanlık psikoloji' kitapları (Gece Kitaplığı 'Karanlık Psikoloji ile...' dizisi, Akıl İzi seti, Emin Efendi, Tristan Cole, Don Barlow, Osman Kutlu ve diğerleri)", "Türkçe 'Karanlık Psikoloji' rafı (tür profili)", "2020 sonrası", "Emin Efendi'nin Karanlık Psikoloji - Manipülasyon kitabı (2023, 160 s.) eski sevgiliyi geri kazanma taktikleri anlatıyor (eleştirmen notu; doğrula)."),
  ("Kirschner", "Josef Kirschner", "Manipulieren – aber richtig: Die acht Gesetze der Menschenbeeinflussung", "1974", ""),
 ]),
}
liste = list(A); yeni_kat = {k: v for k, v in eski_kat.items() if k[:4] <= "K040"}
n = 40; yeniler = []
for gid, (ad, kit) in B.items():
    gruplar[gid] = {"ad": ad, "katman": "B", "kitaplar": []}
    for soy, yazar, oad, yil, not_ in kit:
        n += 1; dosya = f"K{n:03d}_{re.sub(r'[^a-z0-9]+', '_', f(soy))[:18]}"
        eb = eski_bul(soy, oad)
        if eb:
            ip = eski_ipucu(eb["dosya"])
            if not_ and not_ not in ip: ip = (ip + " " + not_).strip()
            yeni_kat[dosya] = eski_kat.get(eb["dosya"], [])
            tr = eb.get("turkce_ad", "")
        else:
            b = bul(soy, oad.split(":")[0][:20])
            ip = ((b["gerekce"] + " ") if b else "") + not_.replace(Y, "").strip()
            tr = (b or {}).get("turkce_ad", ""); yeniler.append(dosya)
        gruplar[gid]["kitaplar"].append({"dosya": dosya, "kunye": f"{yazar} — {oad} ({yil})", "ipucu": ip.replace("${K}", K)})
        liste.append({"dosya": dosya, "grup": gid, "katman": "B", "yazar": yazar, "soyad": soy, "ozgun_ad": oad, "yil": yil, "turkce_ad": tr, "yeni": dosya in yeniler})
json.dump(liste, open(K + "/parcalar/kitap_listesi.json", "w"), ensure_ascii=False, indent=1)
json.dump(gruplar, open(K + "/parcalar/gruplar.json", "w"), ensure_ascii=False, indent=1)
json.dump(yeni_kat, open(K + "/dogrulama/turkce_katalog.json", "w"), ensure_ascii=False, indent=1)
print(len(liste), "kitap; B:", sum(1 for x in liste if x["katman"] == "B"), "; yeni (katalog taranacak):", len(yeniler), yeniler)
