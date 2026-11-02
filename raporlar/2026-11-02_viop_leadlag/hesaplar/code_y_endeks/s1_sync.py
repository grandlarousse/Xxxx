"""GÖREV 1: Senkron beta/korelasyon/R²; hangi endeks hisseyi en iyi açıklıyor; mekanik içerme (hisse-hariç endeks)."""
from ye_common import *
IDXS = [k for k in IDX_DESC if os.path.exists(f"{ISY}/d/{k}.parquet")]
m = idx_ret("XU100")
rows = []
for s in VIOP:
    rs = stk_ret(s); last = rs.dropna().index.max()
    for I in IDXS:
        ri = idx_ret(I)
        df = frame({"s": rs, "i": ri, "m": m}).dropna()
        if len(df) < 120: continue
        r = {"stock": s, "idx": I, "n": len(df), "start": df.index[0].date()}
        for lab, st in [("full", None), ("3y", last - pd.DateOffset(years=3)), ("1y", last - pd.DateOffset(years=1)), ("IS", None), ("OOS", SPLIT)]:
            d = df if st is None else df[df.index >= st]
            if lab == "IS": d = df[df.index < SPLIT]
            if len(d) < 60: continue
            r[f"corr_{lab}"] = d["s"].corr(d["i"])
        b, t, n, r2 = ols_nw(df["s"].values, df["i"].values); r["beta"] = b[1]; r["r2"] = r2
        if I != "XU100":
            r["pcorr_xu100"], _ = ll.partial_corr(df["s"], df["i"], [df["m"]])
            b2, t2, n2, r2b = ols_nw(df["s"].values, df[["m", "i"]].values); r["r2_2f"] = r2b; r["beta_i_2f"] = b2[2]; r["t_i_2f"] = t2[2]
        # mekanik içerme: hisse-hariç endeks
        w = weight_series(I, s, df.index); r["w_mean"] = w.mean(); r["w_last"] = w.iloc[-1]
        if w.max() > 0.005:
            ex = ex_ret(I, s, ri, rs).reindex(df.index)
            d2 = pd.concat([df["s"], ex.rename("ex"), df["m"]], axis=1).dropna()
            r["corr_ex"] = d2["s"].corr(d2["ex"]); r["r2_ex"] = r["corr_ex"] ** 2
            d3 = d2[d2.index >= last - pd.DateOffset(years=3)]; r["corr_ex_3y"] = d3["s"].corr(d3["ex"])
            bb, _, _, _ = ols_nw(d2["s"].values, d2["ex"].values); r["beta_ex"] = bb[1]
        rows.append(r)
    print(s, flush=True)
S = pd.DataFrame(rows); S.to_csv(RES + "/sync.csv", index=False)
