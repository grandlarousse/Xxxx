"""SPK haftalik bultenleri: liste sayfalari -> (bulten no, yayim tarihi, pdf url, yukleme zamani [ObjectId zaman damgasi]) ;
PDF indir -> pdftotext -layout. Varsayilan basliklar, tek tek, 1 sn bekleme.
Kullanim: python3 f05_spk_bulten.py liste | python3 f05_spk_bulten.py pdf
Cikti: <CACHE>/spk/bulten_liste.csv , <CACHE>/spk/pdf/<no>.pdf , <CACHE>/spk/txt/<no>.txt"""
import os, sys, re, time, html, subprocess, requests, pandas as pd
CACHE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/bedelsiz/spk"
S = requests.Session()
AY = {"Ocak": 1, "Şubat": 2, "Mart": 3, "Nisan": 4, "Mayıs": 5, "Haziran": 6, "Temmuz": 7, "Ağustos": 8, "Eylül": 9, "Ekim": 10, "Kasım": 11, "Aralık": 12}
def sayfa(url):
    r = S.get(url, timeout=60); time.sleep(1.0); t = html.unescape(r.text)
    out = []
    for m in re.finditer(r'<a href="(https://spk\.gov\.tr/data/(\w{24})/[^"]+\.pdf)" class="link">.*?Bülten No\s*:\s*([\d/ ]+).*?Yayımlanma\s*:\s*(\d+)\s+(\w+)\s+(\d{4})', t, re.S):
        u, oid, no, g, a, y = m.groups()
        out.append({"no": no.strip(), "tarih": pd.Timestamp(int(y), AY.get(a, 0) or 1, int(g)), "url": u,
                    "yukleme_utc": pd.Timestamp(int(oid[:8], 16), unit="s")})
    for m in re.finditer(r'<td>(\d\d)\.(\d\d)\.(\d{4})</td>\s*<td>\s*(\d{4})\s*/\s*(\d+)\s*</td>\s*<td><a href="(https://spk\.gov\.tr/data/\w{24}/[^"]+\.pdf)"', t):
        g, a, y, ny, nn, u = m.groups()   # eski yillar: tablo bicimi (ObjectId yukleme zamani yayim zamani DEGIL)
        out.append({"no": f"{ny}/{nn}", "tarih": pd.Timestamp(int(y), int(a), int(g)), "url": u, "yukleme_utc": pd.NaT})
    sayfalar = sorted(set(int(x) for x in re.findall(r'\?s=(\d+)', t)))
    return out, sayfalar
def liste():
    rows = []
    for y in range(2014, 2027):
        base = (f"https://spk.gov.tr/spk-bultenleri/{y}-yili-spk-bultenleri" if y >= 2025 else
                f"https://spk.gov.tr/spk-bultenleri/gecmis-yillara-ait-bultenler/{y}-yili-spk-bultenleri")
        o, ss = sayfa(base); rows += o
        for s in [x for x in ss if x > 1]:
            o2, _ = sayfa(base + f"?s={s}"); rows += o2
        print(y, len(rows), flush=True)
    df = pd.DataFrame(rows).drop_duplicates("url"); df.to_csv(f"{CACHE}/bulten_liste.csv", index=False); print(len(df))
def pdfs():
    df = pd.read_csv(f"{CACHE}/bulten_liste.csv")
    os.makedirs(f"{CACHE}/pdf", exist_ok=True); os.makedirs(f"{CACHE}/txt", exist_ok=True)
    for i, r in df.iterrows():
        k = os.path.basename(r.url)[:-4].replace(" ", "_"); p = f"{CACHE}/pdf/{k}.pdf"; tx = f"{CACHE}/txt/{k}.txt"
        if not os.path.exists(p):
            try:
                x = S.get(r.url, timeout=120)
                if x.status_code == 200 and x.content[:4] == b"%PDF": open(p, "wb").write(x.content)
                else: print("bad", r.no, x.status_code, flush=True)
            except Exception as e: print("err", r.no, e, flush=True)
            time.sleep(1.0)
        if os.path.exists(p) and not os.path.exists(tx):
            subprocess.run(["pdftotext", "-layout", p, tx], capture_output=True)
        if i % 50 == 0: print(i, r.no, flush=True)
if __name__ == "__main__":
    os.makedirs(CACHE, exist_ok=True)
    liste() if sys.argv[1] == "liste" else pdfs()
