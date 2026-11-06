"""rapor_sablon.md icindeki {{yer_tutucu}} alanlarini cikti/ altindaki tablolarla doldurur -> ajanlar/abd_test.md"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
from ortak import OUT, md_table

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.abspath(os.path.join(HERE, "..", "..", "ajanlar", "abd_test.md"))


def blocks(fname):
    t = open(os.path.join(OUT, fname)).read()
    parts = re.split(r"\n(?=#### )", "\n" + t)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        head, _, body = p.partition("\n")
        out.append((head.replace("#### ", "").strip(), body.strip()))
    return out


def find(fname, key):
    return [f"**{h}**\n\n{b}" for h, b in blocks(fname) if key in h]


def cell(r):
    return f"{100 * r.CAGR:.1f} / {100 * r.MaxDD:.0f} / {r.Sharpe:.2f}"


def t2_compact(lag):
    S = pd.read_csv(os.path.join(OUT, "t2_ozet.csv"))
    sub = S[(S.Spread == 0.01) & (((S.Strateji == "BH") & (S.Maliyet == 0) & (S.Lag == 0)) |
                                  ((S.Strateji != "BH") & (S.Maliyet == 0.001) & (S.Lag == lag)))].copy()
    sub["c"] = sub.apply(cell, axis=1)
    pv = sub.pivot_table(index=["Dayanak", "L", "Strateji"], columns="Donem", values="c", aggfunc="first").reset_index()
    cols = ["Dayanak", "L", "Strateji"] + [c for c in ["1926-2026 (tam)", "1950-2026", "1986-2026 (tam)", "1986-2026", "2010-2026", "2020-2026"] if c in pv.columns]
    return md_table(pv[cols].fillna(""), pct_cols=(), num_cols=())


def pivot_csv(fname, cols):
    T = pd.read_csv(os.path.join(OUT, fname))
    T["c"] = T.apply(cell, axis=1)
    pv = T.pivot_table(index="Strateji", columns="Donem", values="c", aggfunc="first")
    pv = pv.reindex(list(dict.fromkeys(T.Strateji))).reset_index()
    return md_table(pv[["Strateji"] + cols], pct_cols=(), num_cols=())


R = {
    "t6a": "\n\n".join(find("t6_tablolar.md", "(a)")),
    "t2k0": t2_compact(0),
    "t2k1": t2_compact(1),
    "t2full": "\n\n".join(find("t2_tablolar.md", "ana sonuclar")),
    "t2grid": "\n\n".join(find("t2_tablolar.md", "robustluk")),
    "t2crisis": "\n\n".join(find("t2_tablolar.md", "kriz")),
    "t7": "\n\n".join(b for _, b in blocks("t7_tablolar.md")),
    "t1k": pivot_csv("t1_ozet.csv", ["1927-2026 (tam)", "1950-2026", "2000-2026", "2010-2026", "2020-2026"]),
    "t1grid": blocks("t1_tablolar.md")[1][1],
    "t1diff": blocks("t1_tablolar.md")[2][1],
    "t1crash": blocks("t1_tablolar.md")[3][1],
    "t1dec": blocks("t1_tablolar.md")[4][1],
    "t6k": pivot_csv("t6_kombine.csv", ["1927-2026", "1950-2026", "2000-2026", "2010-2026", "2020-2026"]),
    "t3all": blocks("t3_tablolar.md")[0][1],
    "t3fam": blocks("t3_tablolar.md")[1][1],
    "t3top": blocks("t3_tablolar.md")[2][1],
    "t3pead": blocks("t3_tablolar.md")[3][1],
    "t3pub": "\n\n".join(f"**{h}**\n\n{b}" for h, b in blocks("t3_tablolar.md")[4:6]),
    "t6c": "\n\n".join(find("t6_tablolar.md", "(c)")),
    "t5": "\n\n".join(f"**{h}**\n\n{b}" for h, b in blocks("t5_tablolar.md")),
}
s = open(os.path.join(HERE, "rapor_sablon.md")).read()
for k, v in R.items():
    s = s.replace("{{" + k + "}}", "\n" + v + "\n")
left = re.findall(r"\{\{\w+\}\}", s)
assert not left, left
open(DEST, "w").write(s)
print(DEST, len(s))
