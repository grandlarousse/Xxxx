#!/usr/bin/env python3
"""125 kitabin Turkce baskilarini D&R kataloğunda toplu arar (arama motoru kullanmadan).
Cikti: ek/dogrulama/turkce_baski_katalog.json  {dosya: [{"ad","yazar","yayinevi"}...]}
Not: katalog yalnizca satistaki baskilari gosterir; 'bulunamadi' = D&R'da su an yok."""
import json, os, re, subprocess, sys, time, unicodedata, urllib.parse
from bs4 import BeautifulSoup

K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

def f(s):
    s = (s or "").replace("ı", "i").replace("İ", "I")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()

# dosya on eki -> (sorgular, yazar filtresi, baslik filtresi (regex, aksansiz kucuk harf))
S = {
 "A01": (["robert greene"], "greene", r"bastan cikarma"), "A02": (["robert greene", "33 stratejide savaş"], "", r"33 strateji"),
 "A03": (["robert greene", "iktidarın 50. yasası"], "", r"50\. yasa"), "A04": (["robert greene", "insan doğasının yasaları"], "", r"insan dogasinin yasa"),
 "B01": (["robert greene", "ustalık robert greene"], "", r"^ustalik$|her gune bir yasa"),
 "A05": (["machiavelli hükümdar", "machiavelli prens"], "machiavelli", r"hukumdar|prens"),
 "A06": (["machiavelli söylevler"], "machiavelli", r"soylev"), "A07": (["guicciardini"], "guicciardini", ""),
 "A08": (["gracian"], "gracian", ""), "B14": (["gracian"], "gracian", r"kahraman|sagduyulu|siyaset"),
 "A09": (["castiglione"], "castiglione", ""), "A10": (["mazarin"], "", r"politika|breviar|el kitabi"),
 "A11": (["chesterfield"], "chesterfield", ""), "A12": (["la rochefoucauld"], "rochefoucauld", ""),
 "A13": (["sun tzu savaş sanatı"], "", r"savas sanati"), "A14": (["36 strateji", "otuz altı strateji"], "", r"36 strateji|otuz alti"),
 "A15": (["han fei"], "han fei", ""), "A16": (["kalın yüz kara yürek", "chin-ning chu"], "", r"kalin yuz"),
 "A17": (["arthaşastra", "kautilya"], "", r"artha"), "A18": (["kelile ve dimne"], "", r"kelile"),
 "A19": (["nizamülmülk siyasetname"], "", r"siyaset"), "A20": (["kutadgu bilig"], "", r"^kutadgu bilig"),
 "A21": (["jeffrey pfeffer"], "pfeffer", r"^guc\b"), "A22": (["jeffrey pfeffer", "gücün 7 kuralı"], "", r"7 kural|yedi kural"),
 "B50": (["jeffrey pfeffer"], "pfeffer", r"yonetim"), "A23": (["michael korda"], "korda", ""),
 "A24": (["craft of power siu"], "siu", ""), "A25": (["alinsky", "radikaller için kurallar"], "", r"radikaller icin kural"),
 "A26": (["diktatörün el kitabı", "bueno de mesquita"], "", r"diktatorun el kitabi"), "A27": (["chris matthews"], "matthews", ""),
 "A28": (["luttwak"], "luttwak", r"darbe"), "A29": (["cialdini"], "cialdini", r"ikna"), "B72": (["cialdini"], "cialdini", r"on|pre"),
 "A30": (["dale carnegie dost kazanma"], "carnegie", r"dost kazanma"), "A31": (["schopenhauer eristik", "schopenhauer haklı çıkma"], "schopenhauer", r"eristik|hakli cikma"),
 "A32": (["bernays"], "bernays", ""), "A33": (["ibn haldun mukaddime"], "", r"mukaddime"),
 "A34": (["weber meslek olarak siyaset"], "weber", r"siyaset"), "A35": (["norbert elias"], "elias", r"saray"),
 "A36": (["bertrand russell iktidar", "bertrand russell"], "", r"^iktidar"), "B02": (["ryan holiday"], "holiday", r"yalan|guven"),
 "B03": (["jay haley"], "haley", r"isa|guc taktik"), "B04": (["grete de francesco"], "francesco", ""), "B05": (["scharfstein"], "scharfstein", ""),
 "B06": (["bloodworth"], "bloodworth", ""), "B07": (["botero"], "botero", r"devlet"), "B08": (["gabriel naude"], "naud", ""),
 "B09": (["richelieu"], "richelieu", ""), "B10": (["anti makyavel", "anti machiavel"], "", r"anti.?mak|anti.?mach"),
 "B11": (["accetto"], "accetto", ""), "B12": (["francis bacon denemeler"], "bacon", r"deneme"),
 "B13": (["eustache de refuge"], "refuge", ""), "B15": (["callieres"], "callieres", ""), "B16": (["knigge"], "", r"insanlarla"),
 "B17": (["maurice joly"], "joly", ""), "B18": (["zweig fouche"], "zweig", r"fouche"),
 "B19": (["ksenophon kyros"], "", r"kyros"), "B20": (["quintus tullius cicero"], "cicero", r"secim|siyaset sanati"),
 "B21": (["thukydides"], "", r"peloponnes"), "B22": (["aristoteles politika"], "", r"^politika"),
 "B23": (["aristoteles retorik"], "", r"^retorik$|^retorik.hasan"), "B24": (["frontinus"], "frontinus", ""),
 "B25": (["hobbes leviathan"], "hobbes", r"leviathan"), "B26": (["la boetie"], "", r"gonullu (kulluk|kolelik)"),
 "B27": (["nietzsche ahlakın soykütüğü"], "nietzsche", r"soykutu"), "B28": (["james burnham"], "burnham", ""),
 "B29": (["robert michels"], "michels", ""), "B30": (["wright mills iktidar seçkinleri"], "mills", r"iktidar"),
 "B31": (["shang yang", "lord shang"], "", r"lord shang|shang yang|shang jun"), "B32": (["guiguzi"], "", r"guiguzi|hayalet vadisi"),
 "B33": (["savaşan devletler"], "", r"savasan devletler"), "B34": (["musashi"], "musashi", ""),
 "B35": (["clausewitz"], "clausewitz", r"savas"), "B36": (["françois jullien"], "jullien", r"etkil"),
 "B37": (["çanakya", "chanakya"], "", r"canakya|chanakya"), "B38": (["sırrü'l esrar", "sırru'l-esrar"], "", r"sirr"),
 "B39": (["ibn zafer", "devletin ölümsüzlük iksiri"], "", r"sulvan|iksir"), "B40": (["kabusname"], "", r"kabus"),
 "B41": (["gazali nasihatül müluk", "gazali yöneticilere"], "gazali", r"muluk|yonetic|nasihat"),
 "B42": (["hileler kitabı"], "", r"hileler kitabi"), "B43": (["siracü'l-müluk", "turtuşi", "siracül müluk"], "", r"sirac.{0,6}muluk"),
 "B44": (["timur tüzükat", "timur'un günlüğü"], "", r"tuzukat|timur'?un gunlugu"), "B45": (["asafname"], "", r"asafname"),
 "B46": (["nushatü's-selatin", "gelibolulu mustafa ali"], "", r"nushat|nasihat.*selatin"), "B47": (["koçi bey risalesi"], "", r"koci bey"),
 "B48": (["devlet adamlarına öğütler"], "", r"devlet adamlarina"), "B49": (["antony jay"], "jay", r"machiavelli|makyavel"),
 "B51": (["stanley bing"], "bing", r"machiavelli|makyavel"), "B52": (["harriet rubin"], "rubin", ""), "B53": (["mafia manager", "mafya yöneticisi"], "", r"mafia manager|mafya yonetici"),
 "B54": (["gruenfeld"], "gruenfeld", ""), "B55": (["jonathan powell"], "powell", r"machiavelli|makyavel"), "B56": (["dick morris"], "morris", r"prens"),
 "B57": (["plunkitt"], "", r"plunkitt"), "B58": (["neustadt"], "neustadt", ""), "B59": (["william riker"], "riker", ""),
 "B60": (["robert caro"], "caro", ""), "B61": (["malaparte"], "malaparte", r"darbe|hukumet devirme"),
 "B62": (["gene sharp"], "sharp", ""), "B63": (["srdja popovic", "popovic devrim"], "popovic", ""),
 "B64": (["james scott tahakküm"], "scott", r"tahakkum"), "B65": (["guriev"], "guriev", ""), "B66": (["keltner"], "keltner", ""),
 "B67": (["brian klaas"], "klaas", r"corrupt|yozlas|iktidar|guc"), "B68": (["battilana"], "battilana", ""), "B69": (["frans de waal"], "waal", r"sempanze"),
 "B70": (["richard christie machiavellianism"], "christie", ""), "B71": (["babiak"], "babiak", ""),
 "B73": (["beauvois"], "beauvois", ""), "B74": (["george simon"], "simon", r"koyun|manipul"), "B75": (["hadnagy"], "hadnagy", r"sosyal muhendislik"),
 "B76": (["david maurer"], "maurer", ""), "B77": (["konnikova"], "konnikova", r"confidence|guven|dolandir"),
 "B78": (["le bon kitleler psikolojisi"], "le bon", r"kitle"), "B79": (["eric hoffer"], "hoffer", r"kesin inanc"),
 "B80": (["jacques ellul"], "ellul", r"propaganda"), "B81": (["rızanın imalatı"], "", r"rizanin"), "B82": (["robert jay lifton"], "lifton", ""),
 "B83": (["stanley milgram"], "milgram", r"itaat|deney"), "B84": (["steven lukes", "iktidar radikal bir görüş"], "", r"radikal bir gorus"),
 "B85": (["foucault hapishanenin doğuşu"], "foucault", r"hapishane"), "B86": (["arendt şiddet üzerine"], "", r"^siddet uzerine$|^siddet uzerine secme"),
 "B87": (["canetti kitle ve iktidar"], "canetti", r"kitle"), "B88": (["popitz"], "popitz", ""),
 "B89": (["galbraith iktidarın anatomisi"], "galbraith", r"iktidar"),
}

onbellek = {}
def ara(q):
    if q in onbellek:
        return onbellek[q]
    url = "https://www.dr.com.tr/search?q=" + urllib.parse.quote(q)
    for deneme in range(3):
        r = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A", UA, url], capture_output=True)
        html = r.stdout.decode("utf-8", "replace")
        if "product-card" in html or "sonuç bulunamadı" in html.lower() or len(html) > 50000:
            break
        time.sleep(2)
    out = []
    for c in BeautifulSoup(html, "lxml").select("div.product-card"):
        inf = c.select_one("div.prd-infos") or c
        t = inf.select_one("h3 a:not(.who)")
        y = inf.select_one("a.who")
        p = inf.find("a", href=re.compile(r"/[Yy]ayinevi/|/yayinevi/|/marka/")) or inf.select_one("a.prd-publisher, .prd-publisher a")
        if t:
            out.append({"ad": t.get_text(" ", strip=True), "yazar": y.get_text(" ", strip=True) if y else "", "yayinevi": p.get_text(" ", strip=True) if p else "",
                        "kitap_mi": "/kitap/" in (t.get("href") or "").lower()})
    onbellek[q] = out
    time.sleep(0.7)
    return out

def ara_ks(q):
    an = "ks:" + q
    if an in onbellek:
        return onbellek[an]
    url = "https://www.kitapsec.com/Arama/index.php?a=" + urllib.parse.quote(q.encode("iso-8859-9", "ignore"))
    r = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A", UA, url], capture_output=True)
    html = r.stdout.decode("iso-8859-9", "replace")
    def adlar(tip):
        out = set()
        for m in re.finditer(r'"KatAdi":"((?:[^"\\]|\\.)*)","KatID":"\d+","Toplam":"\d+","YYTip":"%s"' % tip, html):
            try: out.add(json.loads('"' + m.group(1) + '"'))
            except Exception: pass
        return sorted(out, key=len, reverse=True)
    yay, yaz = adlar("1"), adlar("2")
    sp = BeautifulSoup(html, "lxml")
    for t in sp(["script", "style"]): t.decompose()
    txt = re.sub(r"\s+", " ", sp.get_text(" "))
    out = []
    for blob in re.findall(r"Sepete At Hemen Al (.*?) \d[\d.]*\.\d\d TL", txt):
        blob = blob.strip(); yv = ""; yz = ""
        for p_ in yay:
            if blob.endswith(p_): yv = p_; blob = blob[: -len(p_)].strip(); break
        for a_ in yaz:
            if blob.endswith(a_): yz = a_; blob = blob[: -len(a_)].strip(); break
        if blob: out.append({"ad": blob, "yazar": yz, "yayinevi": yv, "kitap_mi": True})
    onbellek[an] = out
    time.sleep(0.7)
    return out

sonuc = {}
dosyalar = sorted(x[:-3] for x in os.listdir(K + "/kitaplar") if x.endswith(".md"))
for d in dosyalar:
    kod = d[:3]
    if kod not in S:
        sonuc[d] = None; continue
    sorgular, yazar, baslik = S[kod]
    bulunan, gorulen = [], set()
    for q in sorgular:
        for x in ara(q) + ara_ks(q):
            if not x["kitap_mi"]: continue
            if yazar and x["yazar"] and yazar not in f(x["yazar"]): continue
            if yazar and not x["yazar"] and not baslik and len(q.split()) > 2: continue
            if baslik and not re.search(baslik, f(x["ad"])): continue
            an = (re.sub(r"[^a-z0-9]", "", f(x["ad"]))[:28], f(x["yayinevi"]))
            if an in gorulen or (not x["yayinevi"] and any(g[0] == an[0] for g in gorulen)): continue
            gorulen.add(an); bulunan.append({k: x[k] for k in ("ad", "yazar", "yayinevi")})
    bulunan.sort(key=lambda x: (not x["yayinevi"], x["ad"])); sonuc[d] = bulunan[:8]
os.makedirs(K + "/dogrulama", exist_ok=True)
json.dump(sonuc, open(K + "/dogrulama/turkce_baski_katalog.json", "w"), ensure_ascii=False, indent=1)
dolu = [d for d in dosyalar if sonuc[d]]
print(len(dolu), "/", len(dosyalar), "kitap icin katalogda en az bir Turkce baski bulundu")
print("BOS:", " ".join(d[:3] for d in dosyalar if not sonuc[d]))
for d in dosyalar:
    v = sonuc[d] or []
    if v and "--tam" in sys.argv: print(d[:3], len(v), "|", " ; ".join(f"{x['ad'][:34]} [{x['yayinevi'][:16]}]" for x in v[:5]))
