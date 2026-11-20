#!/usr/bin/env python3
"""ek/ klasöründeki .md dosyalarında ve RAPOR.md'de geçen bağlantıları toplu kontrol eder.

Kullanım: python3 link_kontrol.py [klasör]  ->  link_kontrol.csv yazar, özet basar.
Bağlantılar ajanla değil bu betikle kontrol edilir (protokol 5. bölüm).
"""
import csv
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KOK = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
URL_RE = re.compile(r"https?://[^\s|)>\]\"'`]+")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def topla():
    bulunan = {}
    for dosya in sorted(KOK.rglob("*.md")):
        for url in URL_RE.findall(dosya.read_text(encoding="utf-8", errors="ignore")):
            url = url.rstrip(".,;:*")
            bulunan.setdefault(url, set()).add(dosya.name)
    return bulunan


def kontrol(url):
    komut = ["curl", "-sS", "-L", "-o", "/dev/null", "-m", "25", "-A", UA,
             "-w", "%{http_code} %{url_effective}", url]
    try:
        cikti = subprocess.run(komut, capture_output=True, text=True, timeout=40)
        govde = cikti.stdout.strip()
        kod, _, son = govde.partition(" ")
        hata = cikti.stderr.strip().splitlines()[-1][:120] if cikti.returncode else ""
        return url, kod or "000", son, hata
    except subprocess.TimeoutExpired:
        return url, "000", "", "zaman aşımı"


def main():
    bulunan = topla()
    with ThreadPoolExecutor(max_workers=16) as havuz:
        sonuc = list(havuz.map(kontrol, sorted(bulunan)))
    hedef = KOK / "ek" / "link_kontrol.csv"
    with hedef.open("w", newline="", encoding="utf-8") as f:
        yaz = csv.writer(f)
        yaz.writerow(["url", "http_kodu", "son_url", "hata", "dosyalar"])
        for url, kod, son, hata in sonuc:
            yaz.writerow([url, kod, son, hata, ";".join(sorted(bulunan[url]))])
    sayim = {}
    for _, kod, _, _ in sonuc:
        sayim[kod] = sayim.get(kod, 0) + 1
    print(f"toplam {len(sonuc)} bağlantı -> {hedef}")
    for kod in sorted(sayim):
        print(f"  {kod}: {sayim[kod]}")


if __name__ == "__main__":
    main()
