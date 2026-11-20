#!/usr/bin/env python3
"""Raporda kullanılan kaynak bağlantılarını toplu kontrol eder.

Kullanım: python3 link_kontrol.py <taslak.md> <defter.json> <cikti.csv>

Her bağlantı için HTTP durum kodunu yazar. 401/403/429 çoğu zaman yayıncının
otomatik isteği engellemesidir (bağlantı tarayıcıda açılır); 404/410 ve bağlantı
hatası gerçek sorun adayıdır.
"""
import csv
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

taslak, defter_yolu, cikti = sys.argv[1:4]
defter = {s["id"]: s for s in json.load(open(defter_yolu, encoding="utf-8"))}
metin = open(taslak, encoding="utf-8").read()
kimlikler = []
for m in re.finditer(r"\[((?:K\d{2}-\d{2})(?:\s*,\s*K\d{2}-\d{2})*)\]", metin):
    for k in re.split(r"\s*,\s*", m.group(1)):
        if k in defter and k not in kimlikler:
            kimlikler.append(k)
urller = {}
for k in kimlikler:
    urller.setdefault(defter[k]["url"].strip(), []).append(k)


def bak(url):
    if not url.lower().startswith("http"):
        return url, "geçersiz", ""
    komut = ["curl", "-s", "-L", "-o", "/dev/null", "-m", "25", "--max-redirs", "8",
             "-A", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
             "-w", "%{http_code} %{url_effective}", url]
    try:
        r = subprocess.run(komut, capture_output=True, text=True, timeout=40)
        kod, _, son = r.stdout.strip().partition(" ")
        return url, kod or "000", son
    except Exception as e:  # noqa: BLE001
        return url, "hata", str(e)[:80]


with ThreadPoolExecutor(max_workers=12) as havuz:
    sonuc = list(havuz.map(bak, urller))

say = {}
with open(cikti, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["durum", "url", "son_adres", "defter_satirlari"])
    for url, kod, son in sorted(sonuc, key=lambda x: x[1]):
        say[kod] = say.get(kod, 0) + 1
        w.writerow([kod, url, son, " ".join(urller[url])])
print("bağlantı:", len(urller), "| durumlar:", dict(sorted(say.items())))
