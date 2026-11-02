"""Senkron kısmi korelasyonun (sektör | XU100, hisse-hariç sektör) yıllık işaret istikrarı ve IS/OOS."""
from ye_common import *
S1 = pd.read_csv(RES + "/sync_best.csv").set_index("stock"); m = idx_ret("XU100")
rows = []
for s in VIOP:
    rs = stk_ret(s)
    for I in set([S1.loc[s, "own_sector"], S1.loc[s, "best_2f_idx"], "XYUZO", "XU030"]):
        ri = idx_ret(I); ex = ex_ret(I, s, ri, rs)
        df = frame({"s": rs, "i": ri, "ex": ex, "m": m}).dropna()
        yr = {}
        for y, g in df.groupby(df.index.year):
            if len(g) < 60: continue
            yr[y] = ll.partial_corr(g["s"], g["ex"], [g["m"]])[0]
        pis = ll.partial_corr(df.s[df.index < SPLIT], df.ex[df.index < SPLIT], [df.m[df.index < SPLIT]])[0] if (df.index < SPLIT).sum() > 60 else np.nan
        poos = ll.partial_corr(df.s[df.index >= SPLIT], df.ex[df.index >= SPLIT], [df.m[df.index >= SPLIT]])[0]
        pfull = ll.partial_corr(df.s, df.ex, [df.m])[0]; last = df.index.max()
        d3 = df[df.index >= last - pd.DateOffset(years=3)]; d1 = df[df.index >= last - pd.DateOffset(years=1)]
        v = np.array(list(yr.values()))
        rows.append({"stock": s, "idx": I, "pc_ex_full": pfull, "pc_ex_IS": pis, "pc_ex_OOS": poos, "pc_ex_3y": ll.partial_corr(d3.s, d3.ex, [d3.m])[0], "pc_ex_1y": ll.partial_corr(d1.s, d1.ex, [d1.m])[0],
                     "frac_years_same_sign": np.mean(np.sign(v) == np.sign(pfull)) if len(v) else np.nan, "n_years": len(v)})
Y = pd.DataFrame(rows); Y.to_csv(RES + "/sync_pc_years.csv", index=False); print(Y.round(3).to_string())
