#!/usr/bin/env python3
"""Kesif dosyalarindan (kesif_D1..D7.json) ayrintili anlatilmayan kitaplarin envanterini cikarir.

Kullanim: python3 envanter.py [--liste]   # --liste: yalnizca sikistirilmis kontrol listesi basar
"""
import json, re, sys, unicodedata, glob, os

K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ayrintili anlatilan kitaplari taniyan anahtarlar (yazar soyadi parcasi, baslik parcasi) - kucuk harf, aksansiz
AYRINTILI = [
 ("greene","seduction"),("greene","33 strategies"),("greene","50th law"),("greene","human nature"),("greene","mastery"),("greene","daily laws"),
 ("machiavelli","principe"),("machiavelli","discorsi"),("guicciardini","ricordi"),("gracian","oraculo"),("gracian","heroe"),("gracian","discreto"),("gracian","politico"),
 ("castiglione","cortegiano"),("mazarin","breviarium"),("chesterfield","letters"),("stanhope","letters"),("rochefoucauld","maxim"),
 ("sun","sunzi"),("sunzi","sunzi"),("anonim","sanshiliu"),("senger","strateg"),("han fei","han feizi"),("li zongwu",""),("chin-ning chu","thick face"),
 ("kautilya","artha"),("mukaffa","kalila"),("sarma","pancatantra"),("nizamulmulk",""),("yusuf has hacib",""),
 ("pfeffer","power: why"),("pfeffer","7 rules"),("pfeffer","managing with power"),("korda","power!"),("siu","craft of power"),
 ("alinsky","rules for radicals"),("bueno de mesquita","dictator's handbook"),("matthews","hardball"),("luttwak","coup"),
 ("cialdini","influence"),("cialdini","pre-suasion"),("carnegie","how to win"),("schopenhauer","eristische"),("bernays","propaganda"),
 ("ibn haldun",""),("weber","politik als beruf"),("elias","hofische"),("russell","power"),
 ("holiday","trust me"),("haley","power tactics"),("francesco","charlatan"),("scharfstein","amoral"),("bloodworth","chinese machiavelli"),
 ("botero","ragion"),("naude","coups"),("richelieu","testament"),("friedrich","anti-machiavel"),("accetto","dissimulazione"),("bacon","essay"),
 ("refuge","traicte"),("callieres","negocier"),("knigge","umgang"),("joly","dialogue"),("zweig","fouche"),
 ("ksenophon","kyrou"),("cicero","commentariolum"),("thukydides",""),("aristoteles","politika"),("aristoteles","rhetor"),("frontinus","strategemata"),("polyainos","strategemata"),
 ("hobbes","leviathan"),("boetie","servitude"),("nietzsche","genealogie"),("nietzsche","wille zur macht"),("burnham","machiavellians"),("michels","soziologie"),("mills","power elite"),
 ("shang yang",""),("guiguzi",""),("liu xiang","zhanguo"),("musashi","gorin"),("clausewitz","vom kriege"),("jullien","efficacite"),
 ("canakya","niti"),("sahte aristoteles","sirr"),("ibn zafer",""),("keykavus",""),("gazali","nasihat"),("anonim","raqa"),
 ("turtusi",""),("timur","tuzukat"),("lutfi pasa",""),("ali","nushat"),("koci bey",""),("defterdar",""),
 ("jay","management and machiavelli"),("bing","what would machiavelli"),("rubin","princessa"),("'v'","mafia manager"),("gruenfeld","acting with power"),
 ("powell","new machiavelli"),("morris","new prince"),("riordon","plunkitt"),("neustadt","presidential power"),("riker","political manipulation"),("caro","power broker"),
 ("malaparte","coup"),("sharp","from dictatorship"),("popovic","blueprint"),("scott","domination"),("guriev","spin dictators"),
 ("keltner","power paradox"),("klaas","corruptible"),("battilana","power, for all"),("waal","chimpanzee"),("christie","machiavellianism"),("babiak","snakes"),
 ("joule","manipulation"),("simon","sheep"),("hadnagy","social engineering"),("maurer","big con"),("konnikova","confidence"),
 ("le bon","foules"),("hoffer","true believer"),("ellul","propagandes"),("herman","manufacturing"),("lifton","thought reform"),("milgram","obedience"),
 ("lukes","radical view"),("foucault","surveiller"),("arendt","on violence"),("canetti","masse"),("popitz","phanomene"),("galbraith","anatomy"),
]

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()

def ayrintili_mi(b):
    y, a = norm(b["yazar"]), norm(b["ozgun_ad"])
    return any(p in y and t in a for p, t in AYRINTILI)

kayit = {}
for p in sorted(glob.glob(K + "/parcalar/kesif_D*.json")):
    d = json.load(open(p))
    dilim = os.path.basename(p)[6:8]
    for b in d["kitaplar"]:
        if ayrintili_mi(b):
            continue
        ad = norm(re.sub(r"\(.*?\)", "", b["ozgun_ad"]))
        anahtar = (norm(b["yazar"]).split(",")[0].split(" ve ")[0].split()[-1] if norm(b["yazar"]) else "") + "|" + ad[:22]
        e = kayit.get(anahtar)
        if e is None or b["yakinlik"] > e["yakinlik"]:
            b = dict(b); b["dilim"] = dilim
            if e and not b.get("turkce_ad") and e.get("turkce_ad"):
                b["turkce_ad"] = e["turkce_ad"]
            kayit[anahtar] = b

liste = sorted(kayit.values(), key=lambda b: (b.get("tur", ""), -b["yakinlik"], norm(b["yazar"])))
if "--liste" in sys.argv:
    for b in liste:
        print(f"{b['dilim']}|{b['yakinlik']}|{b.get('tur','')[:10]}|{b['yazar'][:34]}|{b['ozgun_ad'][:52]}|{b['yil'][:10]}")
    print(len(liste), "kayit")
else:
    json.dump(liste, open(K + "/parcalar/envanter_ham.json", "w"), ensure_ascii=False, indent=1)
    print(len(liste), "kayit yazildi")
