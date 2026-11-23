#!/usr/bin/env python3
"""Kitap listesindeki her yazarin Turkce kitaplarini D&R ve Kitapsec kataloglarinda tarar.
Girdi: ek/parcalar/kitap_listesi.json  [{"dosya": "K01_...", "yazar": "...", "soyad": "...", "turkce_ad": "..."}]
Cikti: ek/dogrulama/turkce_katalog.json  {dosya: [{"ad","yazar","yayinevi"}...]}  (yazarin katalogdaki butun Turkce kitaplari; hangisinin
o kitap oldugunu yazar ajan secer)."""
import json, os, re, sys, time
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(K, "araclar", "tr_pazar_tara.py")).read()
exec(src[:src.index("import sys\nANAHTAR")])   # f(), ara(), ara_ks(), UA, onbellek
liste = json.load(open(K + "/parcalar/kitap_listesi.json"))
if len(sys.argv) > 1: liste = [b for b in liste if b["katman"] in sys.argv[1:]]
cikti = K + "/dogrulama/turkce_katalog.json"
sonuc = json.load(open(cikti)) if os.path.exists(cikti) else {}
for b in liste:
    soy = b["soyad"]; fs = f(soy)
    bulunan, gor = [], set()
    sorgular = [soy] + ([b["turkce_ad"]] if b.get("turkce_ad") else [])
    for q in sorgular:
        for x in ara(q) + ara_ks(q):
            if not x.get("kitap_mi", True): continue
            ok = fs in f(x.get("yazar", "")) or (b.get("turkce_ad") and q == b["turkce_ad"] and f(b["turkce_ad"])[:12] in f(x["ad"]))
            if not ok: continue
            an = (re.sub(r"[^a-z0-9]", "", f(x["ad"]))[:28], f(x.get("yayinevi", "")))
            if an in gor: continue
            gor.add(an); bulunan.append({"ad": x["ad"], "yazar": x.get("yazar", ""), "yayinevi": x.get("yayinevi", "")})
    sonuc[b["dosya"]] = bulunan[:15]
    if b is liste[-1] or len(sonuc) % 5 == 0:
        json.dump(sonuc, open(cikti, "w"), ensure_ascii=False, indent=1)
    json.dump(sonuc, open(cikti, "w"), ensure_ascii=False, indent=1)
print(sum(1 for v in sonuc.values() if v), "/", len(sonuc), "kitap icin katalogda yazarin en az bir Turkce kitabi")
