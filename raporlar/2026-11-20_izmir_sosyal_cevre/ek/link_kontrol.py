#!/usr/bin/env python3
"""defter.json'daki kaynak URL'lerini toplu kontrol eder (HTTP durum kodu). Sonuc: link_durum.json (onbellekli).
Kullanim: python3 link_kontrol.py"""
import json, os, subprocess, re
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "defter.json"), encoding="utf-8"))
cp = os.path.join(HERE, "link_durum.json")
cache = json.load(open(cp)) if os.path.exists(cp) else {}
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
urls = sorted({r["kaynak"].split()[0] for r in rows if re.match(r"https?://", r.get("kaynak", ""))})
todo = [u for u in urls if u not in cache or cache[u] in ("000",)]
def chk(u):
    p = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "25", "-A", UA, "-o", "/dev/null", "-w", "%{http_code}", u], capture_output=True)
    return u, (p.stdout.decode() or "000")[-3:]
with ThreadPoolExecutor(12) as ex:
    for u, c in ex.map(chk, todo):
        cache[u] = c
json.dump(cache, open(cp, "w"), indent=0)
from collections import Counter
cnt = Counter(cache[u] for u in urls)
print(f"{len(urls)} tekil URL; yeni kontrol {len(todo)}; durumlar: {dict(cnt)}")
nourl = [r["id"] for r in rows if not re.match(r"https?://", r.get("kaynak", ""))]
print("URL'siz satir:", len(nourl), nourl[:15])
