"""KAP bildirim detay sayfasi (https://www.kap.org.tr/tr/Bildirim/<index>) -> govde metni ('|' ayracli etiket/deger) + bagli bildirim OID.
Varsayilan basliklar, tek tek, 3 sn bekleme (ilk denemede 1 sn ile ~100 istekte 429 alindi). 429/666 gelirse Retry-After kadar ya da 2-8 dk bekler, 4 ardisik hatada durur.
Kullanim: python3 f04_kap_detay.py <index_listesi.txt>   Cikti: <CACHE>/kap_detay.jsonl (ekleme; var olanlari atlar)"""
import os, sys, re, json, time, gzip, requests
CACHE = "/tmp/claude-0/-home-user-Xxxx/2b39f18c-e376-5597-93ec-e2162312364a/scratchpad/data/bedelsiz"
OUT = f"{CACHE}/kap_detay.jsonl"
RAW = f"{CACHE}/kap_html"; os.makedirs(RAW, exist_ok=True)
S = requests.Session()
PAUSE = float(os.environ.get("KAP_PAUSE", "3.0"))   # 429 sonrasi: istekler arasi 3 sn
def parse(t):
    """Govde: "disclosureBody":["$NN"] -> RSC parcasi 'NN:T<hex>,' sonrasindaki HTML."""
    m = re.search(r'disclosureBody\\?"\s*:\s*\[\s*\\?"\$(\w+)', t)
    body = None
    if m:
        mk = re.search(r'(?<![0-9a-f])' + m.group(1) + r':T[0-9a-f]+,', t)
        if mk:
            e = len(t)
            for stop in ['self.__next_f.push', '"])</script>']:
                k = t.find(stop, mk.end())
                if 0 < k < e: e = k
            body = t[mk.end():e]
    if body is not None: t = body + " CLIENT_BASE_URL " + t[-200000:]
    u = t.replace('\\u003c', '<').replace('\\u003e', '>').replace('\\u0026', '&').replace('\\"', '"').replace('\\n', ' ')
    i = 0 if body is not None else max(0, u.find('Özet Bilgi')); j = -1
    for end in ['Eklenen Dökümanlar', '"$L42"', 'CLIENT_BASE_URL']:
        j = u.find(end, i)
        if j > 0: break
    seg = u[i:j if j > 0 else i + 60000]
    txt = re.sub(r'<[^>]+>', '|', seg); txt = re.sub(r'(\s*\|\s*)+', '|', txt); txt = re.sub(r'[ \t\r\f\v]+', ' ', txt)
    rel = re.search(r'"relatedDisclosureOid":"?(\w+|null)', u); pub = re.search(r'"publishDate":"([\d\. :]+)"', u)
    did = re.search(r'"disclosureId":"(\w+)"', u)
    return {"txt": txt[:40000], "rel": rel.group(1) if rel else None, "pub": pub.group(1) if pub else None, "oid": did.group(1) if did else None}
if __name__ == "__main__":
    ids = [int(x) for x in open(sys.argv[1]).read().split()]
    done = set()
    if os.path.exists(OUT):
        for l in open(OUT):
            try: done.add(json.loads(l)["idx"])
            except Exception: pass
    todo = [i for i in ids if i not in done]; print("todo", len(todo), flush=True)
    fails = 0; f = open(OUT, "a")
    for n, idx in enumerate(todo):
        try:
            r = S.get(f"https://www.kap.org.tr/tr/Bildirim/{idx}", timeout=60)
            if r.status_code != 200:
                fails += 1; ra = r.headers.get("Retry-After")
                w = int(ra) if (ra and ra.isdigit()) else 120 * fails
                print("status", r.status_code, idx, "retry-after", ra, "bekle", w, flush=True); time.sleep(w)
                if fails >= 4: print("STOP"); break
                continue
            fails = 0; gzip.open(f"{RAW}/{idx}.html.gz", "wt").write(r.text)
            d = parse(r.text); d["idx"] = idx; f.write(json.dumps(d, ensure_ascii=False) + "\n"); f.flush()
        except Exception as e:
            print("err", idx, e, flush=True); time.sleep(10)
        if n % 100 == 0: print(n, idx, flush=True)
        time.sleep(PAUSE)
