#!/usr/bin/env python3
"""Her kitabin ilk yazarini tam adiyla bkmkitap.com aramasinda tarar (tukenmis kitaplari da gosterir).
Sayfadaki JSON-LD ItemList'ten ad, yazar, yayinevi, sayfa, ISBN ve tanitimin basini alir; soyadi tutanlari saklar.
Cikti: ek/dogrulama/turkce_bkm.json {dosya: [{ad,yazar,yayinevi,sayfa,isbn,url,tanitim}]}"""
import json, os, re, sys, time, unicodedata, urllib.parse, urllib.request
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

def f(s):
    s = (s or "").replace("ı", "i").replace("İ", "i")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()

def getir(q, sayfa=1):
    u = "https://www.bkmkitap.com/arama?q=" + urllib.parse.quote(q) + ("&pg=%d" % sayfa if sayfa > 1 else "")
    for d in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30)
            return r.read().decode("utf-8", "ignore")
        except Exception as e:
            time.sleep(3 + 3 * d)
    return ""

def urunler(html):
    out = []
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S):
        try: j = json.loads(m.group(1))
        except Exception: continue
        for g in ([y for x in (j if isinstance(j, list) else [j]) for y in (x.get("@graph", [x]) if isinstance(x, dict) else [])]):
            for el in g.get("itemListElement", []) if isinstance(g, dict) else []:
                it = el.get("item", {})
                if not it.get("name"): continue
                a = it.get("author"); a = a.get("name", "") if isinstance(a, dict) else ", ".join(x.get("name", "") for x in a) if isinstance(a, list) else ""
                p = it.get("publisher"); p = p.get("name", "") if isinstance(p, dict) else ""
                out.append({"ad": it["name"], "yazar": a, "yayinevi": p, "sayfa": it.get("numberOfPages", ""),
                            "isbn": it.get("isbn", ""), "url": it.get("url", ""), "tanitim": (it.get("description") or "")[:220]})
    return out

def ilk_yazar(y):
    y = re.sub(r"\(.*?\)", "", y)
    y = re.split(r"\s+ve\s+|,|&|\s+and\s+", y)[0]
    return re.sub(r"\b[A-Z]\.\s*", "", y).strip()

liste = json.load(open(K + "/parcalar/kitap_listesi.json"))
if len(sys.argv) > 1: liste = [b for b in liste if b["dosya"][:4] in sys.argv[1:]]
cikti = K + "/dogrulama/turkce_bkm.json"
sonuc = json.load(open(cikti)) if os.path.exists(cikti) else {}
for b in liste:
    ad = ilk_yazar(b["yazar"]); soy = f(b["soyad"]).split()[-1] if b["soyad"] else f(ad).split()[-1]
    sorgular = [ad] + ([b["turkce_ad"]] if b.get("turkce_ad") else [])
    bul, gor = [], set()
    for q in sorgular:
        for x in urunler(getir(q)):
            if not re.search(r"\b" + re.escape(soy) + r"\b", f(x["yazar"])): continue
            k = x["url"] or x["ad"]
            if k in gor: continue
            gor.add(k); bul.append(x)
        time.sleep(1.5)
    sonuc[b["dosya"]] = {"sorgu": sorgular, "bulunan": bul[:12]}
    json.dump(sonuc, open(cikti, "w"), ensure_ascii=False, indent=1)
    print(b["dosya"], len(bul), flush=True)
print(sum(1 for v in sonuc.values() if v["bulunan"]), "/", len(sonuc))
