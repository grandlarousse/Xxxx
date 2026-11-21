"""Bir web sayfasını ya da PDF'i indirip temiz metin basar (bağlam ekonomisi için).

Kullanım: python3 kod/sayfa.py URL ["anahtar1|anahtar2"] [en_cok_karakter]
- Anahtar verilirse yalnız eşleşen yerlerin çevresi (±600 karakter, en çok 8 pencere) basılır.
- Verilmezse metnin başı basılır (varsayılan 5000 karakter).
"""
import html, io, re, sys, urllib.request

def metin(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) research-client", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=40) as r:
        ham, tip = r.read(), r.headers.get("Content-Type", "")
    if "pdf" in tip.lower() or ham[:4] == b"%PDF":
        from pypdf import PdfReader
        rd = PdfReader(io.BytesIO(ham))
        return " ".join((p.extract_text() or "") for p in rd.pages[:60])
    t = ham.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return t

def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    url = sys.argv[1]
    anahtar = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].isdigit() else None
    sinir = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 5000
    try:
        t = re.sub(r"\s+", " ", metin(url))
    except Exception as e:
        print(f"HATA: {type(e).__name__}: {str(e)[:200]}"); return
    if not anahtar:
        print(t[:sinir]); return
    out, son = [], -1
    for m in re.finditer(anahtar, t, flags=re.I):
        if m.start() < son: continue
        a, b = max(0, m.start() - 600), min(len(t), m.end() + 600)
        out.append("... " + t[a:b] + " ..."); son = b
        if len(out) >= 8: break
    print("\n\n".join(out)[:sinir * 2] if out else f"(eşleşme yok; metin uzunluğu {len(t)})")

if __name__ == "__main__":
    main()
