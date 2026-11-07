"""Midas destek makalelerinin (indirilmiş .txt) gövdesini çıkarır.

Kullanım:
    python -I extract_destek.py <klasor> [cikti.md]

Her .txt için başlık + "Kayıt Ol" sonrası ile "Sorununu çözemedin mi?" arası
metni alır; index.tsv'den URL ve indirme zamanını ekler.
"""
import sys
import os


def body(txt: str) -> str:
    lines = [l.strip() for l in txt.splitlines()]
    try:
        start = max(i for i, l in enumerate(lines[:80]) if l == "Kayıt Ol") + 1
    except ValueError:
        start = 0
    end = len(lines)
    for i, l in enumerate(lines):
        if l.startswith("Sorununu çözemedin mi?"):
            end = i
            break
    return "\n".join(l for l in lines[start:end] if l)


def main():
    d = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    meta = {}
    idx = os.path.join(d, "index.tsv")
    if os.path.exists(idx):
        for row in open(idx, encoding="utf-8"):
            p = row.rstrip("\n").split("\t")
            if len(p) >= 6:
                meta[p[5]] = (p[0], p[1], p[3], p[4])
    chunks = []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".txt"):
            continue
        name = fn[:-4]
        txt = open(os.path.join(d, fn), encoding="utf-8").read()
        ts, st, url, final = meta.get(name, ("?", "?", "?", "?"))
        chunks.append(f"### {name}\nURL: {final} (indirme: {ts}, HTTP {st})\n\n{body(txt)}\n")
    res = "\n".join(chunks)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(res)
    else:
        print(res)


if __name__ == "__main__":
    main()
