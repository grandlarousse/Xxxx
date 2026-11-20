#!/usr/bin/env python3
"""Sayfa okuyucu: URL'yi indirir, metne cevirir, istenirse yalnizca anahtar kelime cevresini basar.
Kullanim: python3 oku.py URL [anahtar1 anahtar2 ...] [--max 6000]
Cikti: baslik, meta aciklama, JSON-LD etkinlikleri (ad/tarih/yer), sonra metin (ya da anahtar kelime pencereleri)."""
import sys, subprocess, json, re

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return 2
    mx = 6000
    if "--max" in args:
        i = args.index("--max"); mx = int(args[i + 1]); del args[i:i + 2]
    url, keys = args[0], [k.lower() for k in args[1:]]
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    p = subprocess.run(["curl", "-sL", "--compressed", "--max-time", "25", "-A", ua,
                        "-H", "Accept-Language: tr-TR,tr;q=0.9,en;q=0.8",
                        "-w", "\n__HTTP__%{http_code}", url], capture_output=True)
    raw = p.stdout.decode("utf-8", "replace")
    code = "000"
    m = re.search(r"\n__HTTP__(\d+)$", raw)
    if m:
        code = m.group(1); raw = raw[:m.start()]
    if code != "200" or not raw.strip():
        print(f"HATA: http={code} bayt={len(raw)} url={url}"); return 1
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(raw, "lxml")
    out = []
    t = soup.title.string.strip() if soup.title and soup.title.string else ""
    out.append(f"BASLIK: {t}")
    for name in ("description", "og:description", "og:title"):
        tag = soup.find("meta", attrs={"name": name}) or soup.find("meta", attrs={"property": name})
        if tag and tag.get("content"):
            out.append(f"META {name}: {tag['content'].strip()[:400]}")
    ev = []
    def walk(o):
        if isinstance(o, dict):
            ty = o.get("@type")
            ty = ty if isinstance(ty, list) else [ty]
            if any(isinstance(x, str) and "Event" in x for x in ty):
                loc = o.get("location") or {}
                if isinstance(loc, list): loc = loc[0] if loc else {}
                ln = loc.get("name", "") if isinstance(loc, dict) else str(loc)
                ev.append(f"- {str(o.get('name',''))[:110]} | {o.get('startDate','')} | {str(ln)[:70]}")
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    for s in soup.find_all("script", type="application/ld+json"):
        try: walk(json.loads(s.string or ""))
        except Exception: pass
    if ev:
        seen = []
        for e in ev:
            if e not in seen: seen.append(e)
        out.append("JSON-LD ETKINLIKLER:\n" + "\n".join(seen[:40]))
    for tag in soup(["script", "style", "noscript", "svg", "header", "footer", "nav", "form", "iframe"]):
        tag.decompose()
    text = re.sub(r"[ \t\r\f\v]+", " ", soup.get_text("\n"))
    text = re.sub(r"\n\s*\n+", "\n", text).strip()
    if keys:
        low = text.lower(); spans = []
        for k in keys:
            for m in re.finditer(re.escape(k), low):
                spans.append((max(0, m.start() - 250), min(len(text), m.end() + 350)))
        spans.sort(); merged = []
        for a, b in spans:
            if merged and a <= merged[-1][1]: merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
            else: merged.append((a, b))
        body = "\n[...]\n".join(text[a:b] for a, b in merged) if merged else "(anahtar kelime bulunamadi; metnin basi:)\n" + text[:1500]
    else:
        body = text
    res = "\n".join(out) + "\nMETIN:\n" + body
    print(res[:mx] + ("\n[kesildi]" if len(res) > mx else ""))
    return 0

sys.exit(main())
