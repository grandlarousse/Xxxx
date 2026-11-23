#!/usr/bin/env python3
"""Kotasiz yedek arama: Vikipedi arama API'si (en/tr/de/fr) ve Open Library kitap aramasi.
Kullanim:
  python3 -I ara.py viki "dark triad personality" [--dil en] [--n 6]   # madde basligi + kisa ozet
  python3 -I ara.py kitap "gaslight effect stern" [--n 6]               # yazar, ad, ilk yayin yili, dil
Kitap kunyesi ve madde bulmak icin; iddia icin ilgili sayfayi sayfa.py ile ac."""
import argparse, json, re, subprocess, urllib.parse
p = argparse.ArgumentParser(); p.add_argument("tur", choices=["viki", "kitap"]); p.add_argument("q")
p.add_argument("--dil", default="en"); p.add_argument("--n", type=int, default=6); a = p.parse_args()
def al(url):
    import time
    for deneme in range(3):
        r = subprocess.run(["curl", "-s", "-L", "--max-time", "25", "-A", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36", url], capture_output=True)
        try:
            return json.loads(r.stdout.decode("utf-8", "replace"))
        except Exception:
            time.sleep(3)
    print("YANIT ALINAMADI (3 deneme)"); return {}
if a.tur == "viki":
    u = f"https://{a.dil}.wikipedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "list": "search", "srsearch": a.q, "srlimit": a.n, "format": "json"})
    for x in al(u).get("query", {}).get("search", []):
        oz = re.sub(r"<.*?>", "", x.get("snippet", ""))
        print(f"- {x['title']} | https://{a.dil}.wikipedia.org/wiki/{urllib.parse.quote(x['title'].replace(' ', '_'))} | {oz[:220]}")
else:
    u = "https://openlibrary.org/search.json?" + urllib.parse.urlencode({"q": a.q, "limit": a.n, "fields": "title,author_name,first_publish_year,language,edition_count,key"})
    for d in al(u).get("docs", []):
        print(f"- {', '.join(d.get('author_name', [])[:3])} | {d.get('title')} | ilk yayın {d.get('first_publish_year')} | baskı {d.get('edition_count')} | dil {','.join((d.get('language') or [])[:6])} | https://openlibrary.org{d.get('key')}")
