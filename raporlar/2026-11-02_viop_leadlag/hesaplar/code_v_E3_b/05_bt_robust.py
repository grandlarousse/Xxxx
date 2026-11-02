import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b")
"""05: Backtest, alt dönem, uç değer bağımlılığı, robust regresyon, yavaş bileşen kontrolü."""
import vb, numpy as np, pandas as pd, statsmodels.api as sm
from scipy import stats as st
F = pd.read_parquet(vb.RES + "/F.parquet")
s = F["A_USREF"]; G = F[F.index >= "2014-01-01"]
PER = [("ALL", "2014", "2027"), ("IS", "2014", "2021"), ("OOS", "2021", "2027"), ("14-17", "2014", "2018"), ("18-20", "2018", "2021"), ("21-23", "2021", "2024"), ("24-26", "2024", "2027")]
def pstats(pnl, pos, cost):
    out = {}
    for pk, a, b in PER:
        m = (pnl.index >= a) & (pnl.index < b); p = pnl[m]; q = pos[m]; act = q != 0
        if act.sum() < 10: continue
        net = p[act] - cost / 1e4
        ann = net.mean() * 252 * act.mean(); vol = (p - cost / 1e4 * q.abs()).std() * np.sqrt(252)
        out[pk] = dict(n=int(act.sum()), bps=1e4 * net.mean(), t=vb.tstat(net), sh=ann / vol, hit=(net > 0).mean())
    return out
rows = []
for tgt in ["y_h", "y_raw"]:
    for thr in [0.0, 0.5, 1.0, 1.5]:
        for win in [60, 120, 250, 500]:
            pnl, pos = vb.bt(s, F[tgt], thr, "z", 0.0, win); pnl = pnl[pnl.index >= "2014"]; pos = pos[pos.index >= "2014"]
            for cost in [0, 8, 15, 19 if tgt == "y_h" else 11]:
                for pk, d in pstats(pnl, pos, cost).items():
                    rows.append(dict(tgt=tgt, thr=thr, win=win, cost=cost, per=pk, **d))
B = pd.DataFrame(rows); B.to_csv(vb.RES + "/05_bt_grid.csv", index=False)
pd.set_option("display.width", 250)
print("Ana varyant |z|>1, pencere 250: brüt / net (bps, t, Sharpe)")
m = (B.thr == 1.0) & (B.win == 250)
print(B[m].pivot_table(index=["tgt", "cost"], columns="per", values="bps").round(1)[[p[0] for p in PER]].to_string())
print(B[m].pivot_table(index=["tgt", "cost"], columns="per", values="t").round(2)[[p[0] for p in PER]].to_string())
print(B[m].pivot_table(index=["tgt", "cost"], columns="per", values="sh").round(2)[[p[0] for p in PER]].to_string())
print(B[m & (B.cost == 0)][["tgt", "per", "n", "hit"]].pivot_table(index="tgt", columns="per", values="n").to_string())
print("\nIzgara (eşik x pencere = 16 varyant), net Sharpe>0 oranı:")
for tgt, c in [("y_raw", 8), ("y_raw", 15), ("y_h", 8), ("y_h", 19)]:
    g = B[(B.tgt == tgt) & (B.cost == c)]
    print(f"  {tgt} maliyet {c}: " + ", ".join(f"{pk} {(g[g.per == pk].sh > 0).mean():.2f} (medyan Sh {g[g.per == pk].sh.median():.2f})" for pk in ["IS", "OOS", "14-17", "18-20", "21-23", "24-26"]))
# yıllık
pnl, pos = vb.bt(s, F["y_raw"], 1.0); pnl = pnl[pnl.index >= "2014"]; pos = pos[pos.index >= "2014"]; act = pos != 0
yb = (1e4 * pnl[act].groupby(pnl[act].index.year).agg(["mean", "count"])).round(1); yb["count"] /= 1e4
pnh, poh = vb.bt(s, F["y_h"], 1.0); pnh = pnh[pnh.index >= "2014"]; poh = poh[poh.index >= "2014"]; ah = poh != 0
yb["y_h_mean"] = (1e4 * pnh[ah].groupby(pnh[ah].index.year).mean()).round(1)
print("\nYıllık brüt bps/işlem (|z|>1): y_raw (tek bacak, TUPRS vadeli) ve y_h (XU100 hedge'li):"); print(yb.T.to_string())
# Uç değer bağımlılığı (y_raw ve y_h)
print("\nUç değer bağımlılığı (brüt, |z|>1):")
for nm, pn, ac in [("y_raw", pnl, act), ("y_h", pnh, ah)]:
    p = pn[ac]
    for pk, a, b in PER[:3]:
        q = p[(p.index >= a) & (p.index < b)]
        top = q.sort_values(ascending=False)
        r10 = q.drop(top.index[:10]); r20 = q.drop(top.index[:20])
        both = q.drop(top.index[:10]).drop(top.index[-10:])
        w = q.clip(q.quantile(0.01), q.quantile(0.99))
        med = q.median()
        print(f"  {nm} {pk}: tam {1e4*q.mean():.1f} (t {vb.tstat(q):.2f}) | en iyi 10 hariç {1e4*r10.mean():.1f} (t {vb.tstat(r10):.2f}) | en iyi 20 hariç {1e4*r20.mean():.1f} (t {vb.tstat(r20):.2f}) | iki uçtan 10 {1e4*both.mean():.1f} (t {vb.tstat(both):.2f}) | %1 winsor {1e4*w.mean():.1f} (t {vb.tstat(w):.2f}) | medyan {1e4*med:.1f} | isabet {(q>0).mean():.3f} (binom p {st.binomtest(int((q>0).sum()), len(q), 0.5, alternative='greater').pvalue:.3f}) n {len(q)}")
    # en iyi 10 günün tarihleri
    print("   en iyi 10 gün:", ", ".join(f"{d.date()}:{1e4*v:.0f}" for d, v in pn[ac].sort_values(ascending=False).head(10).items()))
    print("   en kötü 10 gün:", ", ".join(f"{d.date()}:{1e4*v:.0f}" for d, v in pn[ac].sort_values().head(10).items()))
# Regresyon robustluğu: Spearman, Huber, winsor
print("\nRegresyon robustluğu (hedef y_h ve y_raw, sinyal A_USREF):")
for tgt in ["y_h", "y_raw"]:
    for pk, a, b in PER:
        g = G[(G.index >= a) & (G.index < b)][[tgt, "A_USREF"]].dropna()
        rho, pr = st.spearmanr(g.A_USREF, g[tgt])
        hub = sm.RLM(g[tgt].values, sm.add_constant(g.A_USREF.values), M=sm.robust.norms.HuberT()).fit()
        gw = g.copy(); gw[tgt] = gw[tgt].clip(gw[tgt].quantile(0.01), gw[tgt].quantile(0.99)); gw["A_USREF"] = gw.A_USREF.clip(gw.A_USREF.quantile(0.01), gw.A_USREF.quantile(0.99))
        _, tw, _ = vb.nw(gw[tgt], gw[["A_USREF"]])
        # en etkili 10 gözlem (|x*y| en büyük) hariç
        infl = (g.A_USREF - g.A_USREF.mean()).abs() * (g[tgt] - g[tgt].mean()).abs()
        gd = g.drop(infl.sort_values(ascending=False).index[:10])
        _, td, _ = vb.nw(gd[tgt], gd[["A_USREF"]])
        print(f"  {tgt} {pk:6s}: Spearman {rho:.3f} (t≈{rho*np.sqrt(len(g)):.2f}) | Huber t {hub.tvalues[1]:.2f} | winsor NW t {tw['A_USREF']:.2f} | en etkili 10 hariç NW t {td['A_USREF']:.2f} | n {len(g)}")
# Yavaş bileşen kontrolü: USREF_{t-2..t-21} ortalaması ve TUPRS y_h geçmiş 20g ortalaması
print("\nYavaş bileşen kontrolü (y_h ~ USREF_{t-1} + mean USREF_{t-2..t-21} + mean y_h_{t-1..t-20}):")
G2 = F.copy(); G2["slowref"] = F.A_USREF.shift(1).rolling(20).mean(); G2["slowy"] = F.y_h.shift(1).rolling(20).mean()
G2["sum2_6"] = F.A_USREF.shift(1).rolling(5).sum()
G2 = G2[G2.index >= "2014"]
for pk, a, b in PER:
    g = G2[(G2.index >= a) & (G2.index < b)]
    p, t, n = vb.nw(g.y_h, g[["A_USREF", "slowref", "slowy"]]); p2, t2, _ = vb.nw(g.y_h, g[["A_USREF", "sum2_6"]])
    print(f"  {pk:6s}: USREF t {t['A_USREF']:.2f} | slowref t {t['slowref']:.2f} | slowy t {t['slowy']:.2f} || USREF t {t2['A_USREF']:.2f}, toplam(t-2..t-6) t {t2['sum2_6']:.2f}")
