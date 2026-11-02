"""s7: Ileriye-yuruyen (walk-forward) bilesen secimi: her yil Y icin 2014..Y-1 verisiyle 'acilis-oncesi Asya' evreninden
(.T/.KS/.AX + N225/KS11/AXJO) hedefin gun-ici getirisiyle en yuksek korelasyonlu k sembol secilir, Y yilinda islem yapilir.
Bu, kaynak ajanin tam-orneklem secim yanliligini ortadan kaldiran durust test."""
import sys, os, glob; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vb, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
c = vb.cal()
U = sorted([os.path.basename(p)[:-8] for p in glob.glob(os.path.join(vb.DATA, "daily", "*.parquet"))
            if any(os.path.basename(p)[:-8].endswith(x) for x in (".T", ".KS", ".AX")) or os.path.basename(p)[:-8] in ("^N225", "^KS11", "^AXJO")])
print("evren:", len(U))
Z = pd.DataFrame({s: vb.zpast(vb.dret(s)).reindex(c) for s in U})
rows, picks = [], []
for tgt in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS", "POOL"]:
    if tgt == "POOL":
        Y = {s: vb.bist(s).intra.reindex(c) for s in ["EREGL.IS", "KRDMD.IS"]}
    else:
        Y = {tgt: vb.bist(tgt).intra.reindex(c)}
    for k in (3, 5, 10):
        pos_all = {s: [] for s in Y}
        for yr in range(2017, 2027):
            tr = (c >= "2014-01-01") & (c < f"{yr}-01-01")
            sc = sum(Z[tr].corrwith(y[tr]) for y in Y.values()) / len(Y)
            nobs = Z[tr].notna().sum(); sc[nobs < 500] = np.nan
            sel = sc.sort_values(ascending=False).dropna().index[:k].tolist()
            picks.append(dict(target=tgt, k=k, year=yr, picks=",".join(sel)))
            comp = Z[sel].mean(axis=1)
            zz = vb.zpast(comp.dropna()).reindex(c)
            p = np.sign(zz).where(zz.abs() > 1, 0).fillna(0)
            m = (c >= f"{yr}-01-01") & (c < f"{yr+1}-01-01")
            for s in Y: pos_all[s].append(p[m])
        for s, y in Y.items():
            p = pd.concat(pos_all[s]); yy = y.reindex(p.index)
            pnl = (p * yy - 15e-4 * p.abs()).where(yy.notna() & (p != 0)).dropna()
            for lab, msk in [("2017-26", pnl.index >= "2017-01-01"), ("2017-20", pnl.index < "2021-01-01"), ("2021-26", pnl.index >= "2021-01-01"), ("2024-26", pnl.index >= "2024-01-01")]:
                g = pnl[msk]
                rows.append(dict(select_on=tgt, stock=s, k=k, period=lab, n=len(g), net15_bps=1e4 * g.mean(), t=vb.nwt(g)))
R = pd.DataFrame(rows); P = pd.DataFrame(picks)
R.to_csv(os.path.join(vb.OUT, "res_s7_walkforward.csv"), index=False); P.to_csv(os.path.join(vb.OUT, "res_s7_picks.csv"), index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 120)
print(R.pivot_table(index=["select_on", "stock", "k"], columns="period", values="net15_bps").round(1).to_string())
print(R.pivot_table(index=["select_on", "stock", "k"], columns="period", values="t").round(2).to_string())
print(P[(P.k == 5)].to_string())
# referans: sabit JP_AU ayni pencerelerde
cA, _ = vb.comp(vb.JP_AU)
for s in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS"]:
    o = vb.bt(cA, vb.bist(s).intra, start="2017-01-01"); a = o[o.pos != 0]
    print("JP_AU sabit", s, "2017-26", round(1e4 * a.pnl.mean(), 1), round(vb.nwt(a.pnl), 2))
