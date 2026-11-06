"""Adım 1: halkarz.com yıllık arşiv sayfalarından (k/halka-arz/YYYY/page/N/) 2020-2026 halka arz listesini
ve her şirketin detay sayfasını indirir (önbellek: data/halka_arz/raw_web). robots.txt bu yollara izin veriyor.
Kullanım: python3 -I a01_liste_indir.py"""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import RAW_WEB, polite_get
from bs4 import BeautifulSoup

YEARS = range(2020, 2027)


def year_pages(y):
    items = []
    n = 1
    while True:
        fp = os.path.join(RAW_WEB, "years", f"{y}_p{n}.html")
        if not os.path.exists(fp):
            url = f"https://halkarz.com/k/halka-arz/{y}/" + (f"page/{n}/" if n > 1 else "")
            r = polite_get(url, sleep=1.2)
            if r is None or r.status_code != 200:
                break
            open(fp, "w", encoding="utf-8").write(r.text)
        s = BeautifulSoup(open(fp, encoding="utf-8").read(), "lxml")
        arts = s.find_all("article", class_="index-list")
        for a in arts:
            kod = a.find("h2", class_="il-bist-kod")
            h3 = a.find("h3", class_="il-halka-arz-sirket")
            link = h3.find("a")["href"] if h3 and h3.find("a") else None
            items.append(dict(year=y, kod=kod.get_text(strip=True) if kod else "", ad=h3.get_text(strip=True) if h3 else "", url=link))
        nxt = [x["href"] for x in s.find_all("a", href=True) if f"/{y}/page/{n+1}/" in x["href"]]
        if not arts or not nxt:
            break
        n += 1
    return items


def main():
    allit = []
    for y in YEARS:
        it = year_pages(y)
        print(y, len(it), flush=True)
        allit += it
    json.dump(allit, open(os.path.join(RAW_WEB, "liste.json"), "w"), ensure_ascii=False, indent=0)
    for i, it in enumerate(allit):
        if not it["url"]:
            continue
        slug = it["url"].rstrip("/").split("/")[-1]
        fp = os.path.join(RAW_WEB, "pages", slug + ".html")
        if os.path.exists(fp):
            continue
        r = polite_get(it["url"], sleep=1.2)
        if r is not None and r.status_code == 200:
            open(fp, "w", encoding="utf-8").write(r.text)
        if i % 20 == 0:
            print("detay", i, len(allit), flush=True)


if __name__ == "__main__":
    main()
