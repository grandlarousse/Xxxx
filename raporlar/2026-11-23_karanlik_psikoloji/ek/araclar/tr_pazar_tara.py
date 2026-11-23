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


import sys
ANAHTAR = sys.argv[1:] or ["karanlık psikoloji", "manipülasyon", "narsist", "narsisizm", "psikopat", "sosyopat", "gaslighting", "duygusal istismar",
  "toksik ilişki", "zihin kontrolü", "beyin yıkama", "ikna teknikleri", "beden dili", "yalanı yakalamak", "makyavelizm", "kötülük psikolojisi", "tarikat", "dolandırıcılık psikolojisi"]
gor = {}
for q in ANAHTAR:
    for x in ara(q) + ara_ks(q):
        if not x.get("kitap_mi", True): continue
        an = (re.sub(r"[^a-z0-9]", "", f(x["ad"]))[:30], f(x["yazar"])[:20])
        e = gor.setdefault(an, {"ad": x["ad"], "yazar": x["yazar"], "yayinevi": set(), "sorgu": set()})
        if x.get("yayinevi"): e["yayinevi"].add(x["yayinevi"])
        if x.get("yazar") and not e["yazar"]: e["yazar"] = x["yazar"]
        e["sorgu"].add(q)
out = sorted(gor.values(), key=lambda e: (-len(e["sorgu"]), f(e["yazar"]), f(e["ad"])))
json.dump([dict(e, yayinevi=sorted(e["yayinevi"]), sorgu=sorted(e["sorgu"])) for e in out], open(K + "/parcalar/tr_pazar_tarama.json", "w"), ensure_ascii=False, indent=1)
print(len(out), "kayit")
