#!/usr/bin/env python3
"""Bir web sayfasini indirip duz metne cevirir (ajanlarin baglamini korumak icin kisaltir).

Kullanim:
  python3 -I sayfa.py URL                      # sayfanin ilk 6000 karakteri
  python3 -I sayfa.py URL --ara "Law 12|Lustig" # yalnizca eslesen yerlerin cevresi
  python3 -I sayfa.py URL --max 9000 --baglam 600
"""
import argparse
import re
import subprocess
import sys

from bs4 import BeautifulSoup

p = argparse.ArgumentParser()
p.add_argument("url")
p.add_argument("--ara", default=None, help="duzenli ifade; buyuk/kucuk harf duyarsiz")
p.add_argument("--max", type=int, default=6000)
p.add_argument("--baglam", type=int, default=400)
a = p.parse_args()

r = subprocess.run(
    ["curl", "-sL", "--max-time", "25", "-A", "Mozilla/5.0 (X11; Linux x86_64)", "-w", "\n%{http_code}", a.url],
    capture_output=True,
)
raw = r.stdout.decode("utf-8", "replace")
html, _, kod = raw.rpartition("\n")
if not html.strip() or not kod.startswith("2"):
    print("ERISILEMEDI (http %s, %d bayt)" % (kod, len(html)))
    sys.exit(1)

soup = BeautifulSoup(html, "lxml")
for t in soup(["script", "style", "noscript", "nav", "footer", "svg", "form"]):
    t.decompose()
for t in soup.find_all(["p", "li", "h1", "h2", "h3", "h4", "h5", "tr", "br", "div", "blockquote", "dd", "dt"]):
    t.append("\n")
text = soup.get_text(" ")
text = re.sub(r"\[\s*\d+\s*\]|\[\s*edit\s*\]", "", text)
text = re.sub(r"[ \t\xa0]+", " ", text)
text = re.sub(r" ?\n[\s]*", "\n", text)

if a.ara:
    out, last, total = [], -1, 0
    for m in re.finditer(a.ara, text, flags=re.I):
        s = max(0, m.start() - a.baglam, last)
        e = min(len(text), m.end() + a.baglam)
        if e <= s:
            continue
        out.append(text[s:e])
        last = e
        total += e - s
        if total > a.max:
            break
    text = "\n[...]\n".join(out) if out else "ESLESME YOK (sayfa %d karakter)" % len(text)
print(text[: a.max])
