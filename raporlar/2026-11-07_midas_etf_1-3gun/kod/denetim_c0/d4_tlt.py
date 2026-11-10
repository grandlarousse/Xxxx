"""Görev 3a/3c/3d: TLT z>=2 -> QQQ/SPY/SMH al (C0), 1-3 gün. Bağımsız uygulama + sağlamlık."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *
pd.set_option("display.width", 250)

spy = px("SPY").index
X = leaders(spy)
IS_END = pd.Timestamp("2021-12-31")

def run(T, sigser, h, pos=2500.0, mode="C0", drop_years=(), drop_top=0, label=""):
    df = px(T); c = df["c"].values.astype(float); idx = df.index
    sig = sigser.reindex(idx).fillna(False).astype(bool).values.copy(); sig[:80] = False
    cost = my_cost(df, pos) / 1e4
    if mode == "C0":
        ent, g = sim_greedy(sig, c, h)
    else:  # C1: t+1 kapanışında gir, t+1+h'de çık
        s2 = np.zeros_like(sig); s2[1:] = sig[:-1]
        ent, g = sim_greedy(s2, c, h)
    net = g - cost
    d = idx[ent] if mode == "C0" else idx[ent - 1]
    keep = ~np.isin(d.year, list(drop_years))
    net = net[keep]; g = g[keep]; d = d[keep]
    if drop_top:
        o = np.argsort(net)[:-drop_top]; net = net[np.sort(o)]; d = d[np.sort(o)]
    isn = net[d <= IS_END]; oos = net[d > IS_END]
    # koşulsuz: aynı dönemde her günün h-günlük brüt getirisi
    u = (c[h:] / c[:-h] - 1)[80:]
    return {"etiket": label, "hedef": T, "h": h, "n": len(net), "net_bp": net.mean() * 1e4, "t": tstat(net),
            "medyan_bp": np.median(net) * 1e4, "kazanma": (net > 0).mean(), "maliyet_bp": cost * 1e4,
            "kosulsuz_brut_bp": u.mean() * 1e4, "IS_n": len(isn), "IS_bp": isn.mean() * 1e4 if len(isn) else np.nan, "IS_t": tstat(isn),
            "OOS_n": len(oos), "OOS_bp": oos.mean() * 1e4 if len(oos) else np.nan, "OOS_t": tstat(oos)}

zT = zsc(X["TLT"])
rows = []
print("== (a) Bağımsız uygulama: TLT z>=2, C0, 2.500 $")
for T in ("QQQ", "SPY", "SMH"):
    for h in (1, 2, 3):
        rows.append(run(T, zT >= 2, h, label="TLT z>=2"))
a = pd.DataFrame(rows); print(a.round(2).to_string(index=False)); a.to_csv(os.path.join(HERE, "d4_a.csv"), index=False)

print("\n== (c) Eşik komşuluğu, Hazine eşdeğeri, 2020 hariç, en iyi 5 hariç; (d) 1.000 $; C1 karşılaştırması")
d10 = pd.read_parquet(os.path.join(DATA, "treasury", "nominal.parquet"))["10 Yr"].astype(float)
dgs_orig = zsc(d10.reindex(spy).diff())                      # taramadaki tanım (tatil NaN'leri pencereyi bozuyor)
dd = d10.diff(); dgs_own = zsc(dd).reindex(spy)              # Hazine'nin kendi takviminde z, sonra SPY günlerine
d30 = pd.read_parquet(os.path.join(DATA, "treasury", "nominal.parquet"))["30 Yr"].astype(float)
d30_own = zsc(d30.diff()).reindex(spy)
variants = [("TLT z>=1.5", zT >= 1.5, {}), ("TLT z>=2", zT >= 2, {}), ("TLT z>=2.5", zT >= 2.5, {}),
            ("DGS10 dz<=-2 (tarama tanımı)", dgs_orig <= -2, {}), ("DGS10 dz<=-2 (Hazine takvimi)", dgs_own <= -2, {}),
            ("DGS30 dz<=-2 (Hazine takvimi)", d30_own <= -2, {}),
            ("TLT z>=2, 2020 hariç", zT >= 2, {"drop_years": (2020,)}), ("TLT z>=2, en iyi 5 hariç", zT >= 2, {"drop_top": 5}),
            ("TLT z>=2, 2020 hariç + en iyi 5 hariç", zT >= 2, {"drop_years": (2020,), "drop_top": 5}),
            ("TLT z>=2, 1.000 $", zT >= 2, {"pos": 1000.0}), ("TLT z>=2, C1 (ertesi kapanış)", zT >= 2, {"mode": "C1"})]
rows = []
for lab, s, kw in variants:
    for T in ("QQQ", "SPY", "SMH"):
        for h in (1, 2, 3):
            rows.append(run(T, s, h, label=lab, **kw))
c_ = pd.DataFrame(rows)
piv = c_.pivot_table(index=["etiket"], columns=["hedef", "h"], values="net_bp", sort=False).round(0)
pivt = c_.pivot_table(index=["etiket"], columns=["hedef", "h"], values="t", sort=False).round(2)
pivn = c_.pivot_table(index=["etiket"], columns=["hedef", "h"], values="n", sort=False)
print("net bp:\n", piv.to_string()); print("t:\n", pivt.to_string()); print("n:\n", pivn.to_string())
c_.to_csv(os.path.join(HERE, "d4_c.csv"), index=False)

print("\n== Yıllara göre (QQQ ve SMH, h=3, TLT z>=2): toplam net bp ve işlem sayısı")
for T in ("QQQ", "SMH"):
    df = px(T); c = df["c"].values; sig = (zT >= 2).reindex(df.index).fillna(False).values.copy(); sig[:80] = False
    ent, g = sim_greedy(sig, c, 3); net = g - my_cost(df) / 1e4
    y = pd.Series(net, index=df.index[ent]).groupby(lambda d: d.year).agg(["size", "sum"])
    y["sum"] = (y["sum"] * 1e4).round(0)
    print(T, y.T.to_string())
    s = pd.Series(net * 1e4, index=df.index[ent]).sort_values(ascending=False)
    print("  en iyi 5:", s.head(5).round(0).to_dict()); print("  toplam net bp:", round(s.sum()), " en iyi 5 payı:", round(s.head(5).sum() / s.sum(), 2))

print("\n== Hisse düşüş günü vekili mi? (QQQ ve SMH, h=3)")
spyr = np.log(px("SPY")["c"]).diff()
for T in ("QQQ", "SMH"):
    df = px(T); rT = np.log(df["c"]).diff(); zTT = zsc(rT)
    spy_dn = (spyr < 0).reindex(spy)
    out = []
    for lab, s in (("TLT z>=2 & SPY<0", (zT >= 2) & spy_dn), ("TLT z>=2 & SPY>=0", (zT >= 2) & ~spy_dn),
                   (f"{T} kendi z<=-1", zTT <= -1), (f"{T} kendi z<=-1.5", zTT <= -1.5), (f"{T} kendi z<=-2", zTT <= -2),
                   (f"{T} kendi z<=-1 & TLT z<1", (zTT <= -1) & (zT.reindex(df.index) < 1)),
                   (f"{T} kendi z<=-1 & TLT z>=1", (zTT <= -1) & (zT.reindex(df.index) >= 1)),
                   ("SPY z<=-1.5", zsc(spyr) <= -1.5)):
        r = run(T, s, 3, label=lab); out.append({k: r[k] for k in ("etiket", "n", "net_bp", "t", "IS_t", "OOS_t")})
    print(T); print(pd.DataFrame(out).round(2).to_string(index=False))

print("\n== Regresyon: QQQ/SMH ileri 3g getiri ~ TLT z>=2 kuklası + kendi getirisi(t) + SPY getirisi(t) (tüm günler, HAC lag 3)")
def nw(y, Xm, L=3):
    xtx = np.linalg.inv(Xm.T @ Xm); b = xtx @ Xm.T @ y; e = y - Xm @ b; u = Xm * e[:, None]; S = u.T @ u
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); G = u[l:].T @ u[:-l]; S += w * (G + G.T)
    V = xtx @ S @ xtx; return b, b / np.sqrt(np.diag(V))
for T in ("QQQ", "SPY", "SMH"):
    df = px(T); lc = np.log(df["c"]); f3 = (lc.shift(-3) - lc); rT = lc.diff()
    D = pd.DataFrame({"f3": f3, "d": (zT >= 2).astype(float).reindex(df.index), "r": rT, "s": spyr.reindex(df.index), "zt": zT.reindex(df.index)}).dropna().iloc[80:]
    b, t = nw(D.f3.values, np.column_stack([np.ones(len(D)), D.d.values, D.r.values]))
    b2, t2 = nw(D.f3.values, np.column_stack([np.ones(len(D)), D.d.values]))
    print(f"  {T}: kukla katsayısı yalın {b2[1]*1e4:.0f} bp (t {t2[1]:.2f});  kendi getirisi kontrollü {b[1]*1e4:.0f} bp (t {t[1]:.2f}), kendi getirisi b={b[2]:.2f} (t {t[2]:.2f})")
