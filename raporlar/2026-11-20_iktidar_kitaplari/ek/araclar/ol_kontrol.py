#!/usr/bin/env python3
"""Envanter kayitlarini Open Library aramasiyla toplu kontrol eder (yazar + ad -> ilk yayin yili).
Sonuc: parcalar/envanter_ol.json  {anahtar: {"durum": "uyuyor|farkli|yok|atlandi", "ol_yil": ...}}
Yalnizca 1800 sonrasi tek yilli kayitlar kontrol edilir; klasikler icin Open Library yili guvenilmez."""
import json, os, re, subprocess, time, urllib.parse
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
kayitlar = json.load(open(K + "/parcalar/envanter_ham.json")) + json.load(open(K + "/parcalar/envanter_ek.json"))
sonuc = {}
for b in kayitlar:
    anahtar = b["yazar"] + " | " + b["ozgun_ad"]
    m = re.match(r"^\s*(1[89]\d\d|20\d\d)\b", b["yil"])
    if not m:
        sonuc[anahtar] = {"durum": "atlandi"}; continue
    yil = int(m.group(1))
    baslik = re.sub(r"\(.*?\)", "", b["ozgun_ad"]).split(":")[0].split(";")[0].strip()
    soyad = re.sub(r"\(.*?\)", "", b["yazar"]).split(",")[0].split(" ve ")[0].strip().split()[-1]
    q = urllib.parse.urlencode({"title": baslik, "author": soyad, "limit": 3, "fields": "title,author_name,first_publish_year"})
    r = subprocess.run(["curl", "-s", "--max-time", "20", "https://openlibrary.org/search.json?" + q], capture_output=True)
    try:
        docs = json.loads(r.stdout.decode("utf-8", "replace")).get("docs", [])
    except Exception:
        docs = None
    if docs is None:
        sonuc[anahtar] = {"durum": "hata"}
    elif not docs:
        sonuc[anahtar] = {"durum": "yok"}
    else:
        yillar = [d.get("first_publish_year") for d in docs if d.get("first_publish_year")]
        if any(abs(y - yil) <= 1 for y in yillar):
            sonuc[anahtar] = {"durum": "uyuyor", "ol_yil": yil}
        else:
            sonuc[anahtar] = {"durum": "farkli", "ol_yil": yillar[:3], "bizim": yil, "ol_ad": docs[0].get("title")}
    time.sleep(0.4)
json.dump(sonuc, open(K + "/parcalar/envanter_ol.json", "w"), ensure_ascii=False, indent=1)
from collections import Counter
print(Counter(v["durum"] for v in sonuc.values()))
for k, v in sonuc.items():
    if v["durum"] in ("farkli", "yok", "hata"):
        print(v["durum"], "|", k[:90], "|", v.get("bizim"), v.get("ol_yil"), (v.get("ol_ad") or "")[:40])
