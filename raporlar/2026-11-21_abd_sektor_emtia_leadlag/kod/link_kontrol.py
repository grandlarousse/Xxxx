"""Rapordaki bütün bağlantıları toplu kontrol eder (ajan değil, tek betik). Çıktı: ek/dogrulama/link_kontrol.csv"""
import csv, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dosya = sys.argv[1] if len(sys.argv) > 1 else os.path.join(KOK, "RAPOR.md")
urls = sorted(set(u.rstrip(").,;") for u in re.findall(r"https?://[^\s|)]+", open(dosya).read())))
def bak(u):
    for yontem in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(u, method=yontem, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-client", "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return u, r.status, ""
        except urllib.error.HTTPError as e:
            kod = e.code
            if yontem == "HEAD" and kod in (403, 405, 400, 501):
                continue
            return u, kod, ""
        except Exception as e:  # noqa: BLE001
            son = f"{type(e).__name__}: {str(e)[:60]}"
    return u, 0, son
with ThreadPoolExecutor(6) as ex:
    sonuc = list(ex.map(bak, urls))
with open(os.path.join(KOK, "ek", "dogrulama", "link_kontrol.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["url", "durum", "not"]); w.writerows(sonuc)
ok = [s for s in sonuc if s[1] == 200]
print(len(urls), "bağlantı;", len(ok), "tamam (200);", len(urls) - len(ok), "sorunlu")
for u, k, n in sonuc:
    if k != 200:
        print(f"  {k} {n} {u}")
