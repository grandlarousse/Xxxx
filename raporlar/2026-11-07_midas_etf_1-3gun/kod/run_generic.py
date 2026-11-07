"""Genel strateji kütüphanesini tüm ETF'lerde çalıştırır.
Çıktı: sonuclar/genel_tum.csv (ETF x sinyal x h x mod), sonuclar/genel_islemler/<SYM>.parquet (yalnız seçilenler için ayrıca)
Kullanım: python3 -I kod/run_generic.py [SYM ...]"""
import os, sys, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from multiprocessing import Pool
import lib, strategies as S, universe

OUT = os.path.join(lib.ROOT, "sonuclar"); os.makedirs(OUT, exist_ok=True)
CTX = None

def ctx():
    global CTX
    if CTX is None:
        CTX = {"VIX": lib.vol_index("VIX"), "VIX3M": lib.vol_index("VIX3M")}
    return CTX

def run_one(sym):
    try:
        df = lib.load(sym)
    except Exception as e:
        return []
    if len(df) < 500: return []
    cost = lib.cost_bp(df)
    rows = []
    x = ctx()
    for name, fn in S.LIB.items():
        try:
            sig = fn(df, x).reindex(df.index).fillna(False).astype(bool)
        except Exception as e:
            continue
        # ısınma: ilk 200 gün dışarıda
        sig.iloc[:200] = False
        nsig = int(sig.sum())
        for mode in ("C0", "O1", "C1"):
            for h in (1, 2, 3):
                s, tr = lib.evaluate(df, sig, h, mode, cost, label=name)
                s.update({"sym": sym, "sig": name, "exit": "sabit", "n_sig_days": nsig})
                rows.append(s)
            if name in S.EXITS:
                ex = S.EXITS[name](df)
                s, tr = lib.evaluate(df, sig, 3, mode, cost, exit_sig=ex, label=name)
                s.update({"sym": sym, "sig": name, "exit": "kural_max3", "n_sig_days": nsig})
                rows.append(s)
    for r in rows:
        r["p"] = lib.t_to_p(r.get("t", np.nan), r.get("n", 0))
        r["p_edge"] = lib.t_to_p(r.get("t_edge", np.nan), r.get("n", 0))
        r["cat"] = universe.CAT.get(sym)
    return rows

if __name__ == "__main__":
    syms = sys.argv[1:] or lib.available()
    with Pool(max(2, os.cpu_count() - 1)) as p:
        allrows = []
        for rows in p.imap_unordered(run_one, syms, chunksize=2):
            allrows += rows
    res = pd.DataFrame(allrows)
    fn = os.path.join(OUT, "genel_tum.csv" if len(sys.argv) == 1 else "genel_parca.csv")
    res.to_csv(fn, index=False)
    print("yazıldı", fn, res.shape)
