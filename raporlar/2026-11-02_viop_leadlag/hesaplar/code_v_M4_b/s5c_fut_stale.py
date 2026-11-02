"""s5c: Vadeli acilis fiyati bayat mi? ABD t-1 (SPY/ES) ve kompozit -> vadeli o->c ve spot o->c; vadeli 'gap' (onceki uzlasma->acilis) kontrolu.
Ayrica ACILIS SEANSI alaninin varligi."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
A = pd.read_parquet(os.path.join(vb.OUT, "viop_rows.parquet"))
A = A[(A.open > 0) & (A.close > 0) & (A.value > 0)]
A = A.sort_values("value").groupby(["und", "date"]).tail(1).set_index(["und", "date"]).sort_index()
c = vb.cal(); cA, _ = vb.comp(vb.JP_AU)
def lagUS(sym):
    r = vb.dret(sym); s = pd.Series(np.nan, index=c); pos = r.index.searchsorted(c, side="left") - 1; ok = pos >= 0; s[ok] = r.values[pos[ok]]; return s
spy = lagUS("SPY"); es = lagUS("ES=F")
rows = []
for u in ["EREGL", "KRDMD", "XU030"]:
    F = A.loc[u].copy(); F["fi"] = np.log(F.close / F.open); F["fgap"] = np.log(F.open / F.psettle)
    F.loc[F.fi.abs() > 0.105, "fi"] = np.nan
    sp = vb.bist(u + ".IS"); F["si"] = sp.intra.reindex(F.index); F["sgap"] = sp.gap.reindex(F.index)
    F["open_minus_spotopen_bps"] = np.nan
    print(u, "ACILIS SEANSI fiyati dolu gun:", F.osp.notna().sum(), "ilk:", F.osp.dropna().index.min(), " osp==open orani:", (F.osp == F.open)[F.osp.notna()].mean().round(3))
    for per, a, e in [("2017-20", "2017-01-01", "2021-01-01"), ("2021-23", "2021-01-01", "2024-01-01"), ("2024-26", "2024-01-01", "2027-01-01")]:
        m = (F.index >= a) & (F.index < e)
        for tgt in ("fi", "si"):
            for sn, sg in [("SPY_t1", spy), ("ES_t1", es), ("comp_t", cA)]:
                r, t, n = vb.corr_t(sg, F[tgt][m]); rows.append(dict(und=u, period=per, target=tgt, signal=sn, corr=r, t=t, n=n))
        # kompozit, vadeli gap + SPY t-1 kontrollu
        X = pd.DataFrame({"comp": cA.reindex(F.index), "fgap": F.fgap, "spy": spy.reindex(F.index), "sgap": F.sgap})[m]
        res, n = vb.nwreg(F.fi[m], X); rows.append(dict(und=u, period=per, target="fi|fgap,sgap,spy", signal="comp_t", corr=np.nan, t=res.loc["comp", "t"], n=n))
        res, n = vb.nwreg(F.si[m], X); rows.append(dict(und=u, period=per, target="si|fgap,sgap,spy", signal="comp_t", corr=np.nan, t=res.loc["comp", "t"], n=n))
R = pd.DataFrame(rows); R.to_csv(os.path.join(vb.OUT, "res_s5c_fut_stale.csv"), index=False)
pd.set_option("display.width", 250)
print(R.pivot_table(index=["und", "target", "signal"], columns="period", values="t").round(2).to_string())
print(R.pivot_table(index=["und", "target", "signal"], columns="period", values="corr").round(3).to_string())
