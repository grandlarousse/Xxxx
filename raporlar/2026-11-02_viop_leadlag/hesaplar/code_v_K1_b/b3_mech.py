"""Mekanik açıklama testleri (h1 dönemi 2023-12+): gap'in r1 (açılış->10:30), r12 (10:30->11:30), r3 (11:30->kapanış) üzerine eğimi;
r2 ~ gap + r1 (gap bilgisi r1'den sonra da kalıyor mu?); fade P&L varyantları; likidite tercili ve hisse bazında."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_K1_b")
from kb import *
P = pd.read_parquet(OUT + "/panel_b.parquet")
H = P[P.p1030.notna() & P.gap.notna() & P.intra.notna()].copy()
print("h1 örneklemi:", H.date.min().date(), H.date.max().date(), "gözlem", len(H))
# --- Havuz regresyonları: günlük kesit ortalaması yerine gözlem bazlı; t için gün kümelemesi yerine Fama-MacBeth benzeri günlük eğim yok -> basit: hisse-gün havuz, NW lag5 üzerinde tarih sıralı
def pooled(df, y, X):
    df = df.sort_values("date")
    b, t, n = ols_nw(df[y].values, [df[x].values for x in X]); return b, t, n
out = []
for grp, df in [("hepsi", H)] + [(g, H[H.liqT == g]) for g in ["dusuk", "orta", "yuksek"]] + [("CIMSA", H[H.sym == "CIMSA"]), ("OYAKC", H[H.sym == "OYAKC"])]:
    for y, X in [("intra", ["gap"]), ("r1", ["gap"]), ("r2", ["gap"]), ("r12", ["gap"]), ("r3", ["gap"]), ("r2", ["gap", "r1"]), ("r3", ["gap", "r1", "r12"])]:
        b, t, n = pooled(df, y, X)
        out.append(dict(grp=grp, y=y, X="+".join(X), b_gap=round(b[1], 4), t_gap=round(t[1], 2), b_2=round(b[2], 4) if len(b) > 2 else np.nan, t_2=round(t[2], 2) if len(b) > 2 else np.nan, n=n))
R = pd.DataFrame(out); print(R.to_string()); R.to_csv(OUT + "/res_b3_reg.csv", index=False)

# --- Fade P&L varyantları, |gap|>%1, gün bazında eşit ağırlıklı portföy (havuz) ve hisse bazında
H["sg"] = -np.sign(H.gap); sel = H.gap.abs() > 0.01
V = {"acilis(o->c)": H.intra, "10:30->c": H.r2, "10:30->17:30": H.r2x, "11:30->c": H.r3,
     "10:30->c, 1 tik aleyhte": H.r2}
rows = []
for name, r in V.items():
    pnl = (H.sg * r * 1e4 - 10 - (H.reltick if "tik" in name else 0)).where(sel)
    H["_p"] = pnl
    for grp in ["hepsi", "dusuk", "orta", "yuksek"]:
        df = H if grp == "hepsi" else H[H.liqT == grp]
        port = df.groupby("date")._p.mean().dropna()
        m, t, n = nwt(port.values)
        rows.append(dict(var=name, grp=grp, port_mean=round(m, 1), t=round(t, 2), ndays=n, ntr=int(df._p.notna().sum())))
    for s in ["CIMSA", "OYAKC"]:
        z = H[H.sym == s]._p.dropna(); m, t, n = nwt(z.values)
        rows.append(dict(var=name, grp=s, port_mean=round(m, 1), t=round(t, 2), ndays=n, ntr=n))
F = pd.DataFrame(rows); print(F.pivot(index="var", columns="grp", values="port_mean").to_string())
print(F.pivot(index="var", columns="grp", values="t").to_string())
F.to_csv(OUT + "/res_b3_fade.csv", index=False)
# --- Hisse bazında: açılış vs 10:30 giriş net-10 ortalama ve BH
ps = []
from scipy import stats
for s, df in H[sel].groupby("sym"):
    a = df.sg * df.intra * 1e4 - 10; b_ = df.sg * df.r2 * 1e4 - 10
    ma, ta, na = nwt(a.values); mb, tb, nb = nwt(b_.values)
    ps.append(dict(sym=s, n=na, open_net=round(ma, 1), t_open=round(ta, 2), d1030_net=round(mb, 1), t_1030=round(tb, 2),
                   reltick=round(df.reltick.median(), 1), liq=round(df.liqrank.median(), 2)))
Q = pd.DataFrame(ps)
Q["p1030"] = 2 * (1 - stats.t.cdf(Q.t_1030.abs(), Q.n - 1)); Q["bh1030"] = bh(Q.p1030.values)
Q["popen"] = 2 * (1 - stats.t.cdf(Q.t_open.abs(), Q.n - 1)); Q["bhopen"] = bh(Q.popen.values)
print(Q.sort_values("d1030_net", ascending=False).to_string())
print("açılış>0:", (Q.open_net > 0).sum(), " 10:30>0:", (Q.d1030_net > 0).sum(), " medyan açılış", Q.open_net.median(), " medyan 10:30", Q.d1030_net.median())
print("BH geçen (açılış):", Q[Q.bhopen].sym.tolist(), " BH geçen (10:30):", Q[Q.bh1030].sym.tolist())
print("kesit korelasyon: open_net~reltick", round(Q.open_net.corr(Q.reltick, method='spearman'), 3), " d1030~reltick", round(Q.d1030_net.corr(Q.reltick, method='spearman'), 3),
      " open~liq", round(Q.open_net.corr(Q.liq, method='spearman'), 3), " d1030~liq", round(Q.d1030_net.corr(Q.liq, method='spearman'), 3))
Q.to_csv(OUT + "/res_b3_stock.csv", index=False)
