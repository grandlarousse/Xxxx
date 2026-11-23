#!/usr/bin/env python3
"""Envanterdeki (12_envanter.md) kitaplarin yilini Open Library aramasiyla toplu kontrol eder (yazar soyadi + ad -> ilk yayin yili).
Sonuc: parcalar/envanter_ol.json {satir: {"durum": "uyuyor|farkli|yok|hata|atlandi", "yil": .., "ol_yil": ..}}
Yalnizca 1800 sonrasi tek yilli kayitlar; +-1 yil fark uyuyor sayilir."""
import json, os, re, subprocess, time, urllib.parse
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sonuc = {}
for s in open(K + "/12_envanter.md", encoding="utf-8"):
    m = re.match(r"- \*\*(.+?) — (.+?)\*\* \((.*?)[;)]", s)
    if not m: continue
    yazar, ad, yil = m.groups(); anahtar = yazar + " | " + ad
    y = re.match(r"^\s*(1[89]\d\d|20\d\d)\b", yil)
    if not y: sonuc[anahtar] = {"durum": "atlandi", "yil": yil}; continue
    yil = int(y.group(1))
    baslik = re.sub(r"\(.*?\)", "", ad).split(":")[0].split(";")[0].strip()
    soyad = re.sub(r"\(.*?\)", "", yazar).split(",")[0].split(" ve ")[0].strip().split()[-1]
    q = urllib.parse.urlencode({"title": baslik, "author": soyad, "limit": 3, "fields": "title,author_name,first_publish_year"})
    docs = None
    for d in range(3):
        r = subprocess.run(["curl", "-s", "--max-time", "25", "-A", "Mozilla/5.0", "https://openlibrary.org/search.json?" + q], capture_output=True)
        try: docs = json.loads(r.stdout.decode("utf-8", "replace")).get("docs", []); break
        except Exception: time.sleep(4)
    if docs is None: sonuc[anahtar] = {"durum": "hata", "yil": yil}
    elif not docs or not any(x.get("first_publish_year") for x in docs): sonuc[anahtar] = {"durum": "yok", "yil": yil}
    else:
        ys = [x["first_publish_year"] for x in docs if x.get("first_publish_year")]
        sonuc[anahtar] = {"durum": "uyuyor" if any(abs(v - yil) <= 1 for v in ys) else "farkli", "yil": yil, "ol_yil": ys[0]}
    time.sleep(1)
json.dump(sonuc, open(K + "/parcalar/envanter_ol.json", "w"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(sonuc), Counter(v["durum"] for v in sonuc.values()))
