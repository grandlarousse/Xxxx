"""Bağımsız lead-lag kontrolü: altın z (VİOP uzlaşma) -> TRALT hedge'li (vadeli) getiri, lag 0..3; NW regresyonu (kendi aynı gün hareketi + XU030 kontrollü)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/rehber/altin/denetim/kod")
import numpy as np, pandas as pd, dlib
c = dlib.cal(); gV, sdV, zV = dlib.viop_gold_z()
fT = dlib.front("TRALT"); fX = dlib.front("XU030"); rT = fT["r"].copy(); rX = fX["r"].copy()
sp = np.log(dlib.ydaily("TRALT.IS")["adj"]).diff().reindex(c)
lim = pd.Series(np.where(c < dlib.REG, np.log(1.22), np.log(1.115)), index=c); rT[rT.abs() > lim] = np.nan; rT[((rT - sp).abs() > 0.08) & sp.notna()] = np.nan
m = rT.notna() & rX.notna(); b = (rT.where(m).rolling(250, min_periods=100).cov(rX.where(m)) / rX.where(m).rolling(250, min_periods=100).var()).shift(1)
hed = rT - b * rX; zh = hed / hed.rolling(250, min_periods=100).std().shift(1); zx = rX / rX.rolling(250, min_periods=100).std().shift(1)
st = c >= pd.Timestamp("2018-12-17")
print("corr(z_altın_t, TRALT hedge'li_{t+k}):", {k: round(pd.concat([zV, hed.shift(-k)], axis=1)[st].dropna().corr().iloc[0, 1], 3) for k in range(0, 4)})
print("corr(TRALT hedge'li_t, z_altın_{t+k}) (ters yön):", {k: round(pd.concat([hed, zV.shift(-k)], axis=1)[st].dropna().corr().iloc[0, 1], 3) for k in range(1, 4)})
def nw(y, X, L):
    df = pd.concat([y.rename("y")] + [X[k].rename(k) for k in X], axis=1)[st].dropna(); n = len(df)
    A = np.column_stack([np.ones(n), df.drop(columns="y").values]); yy = df["y"].values
    iA = np.linalg.pinv(A.T @ A); bb = iA @ A.T @ yy; e = yy - A @ bb; u = A * e[:, None]; Sm = u.T @ u
    for l in range(1, L + 1): G = u[l:].T @ u[:-l]; Sm += (1 - l / (L + 1)) * (G + G.T)
    se = np.sqrt(np.diag(iA @ Sm @ iA)); return pd.DataFrame({"b": bb, "t": bb / se}, index=["sabit"] + list(X)), n
for h in (1, 2, 3):
    y = sum(hed.shift(-i) for i in range(1, h + 1)) * 1e4
    o, n = nw(y, {"z_altin": zV, "z_TRALT_kendi": zh, "z_XU030": zx}, h + 1)
    o2, _ = nw(y, {"z_altin": zV, "z_altin_t1": zV.shift(1), "z_altin_t2": zV.shift(2)}, h + 1)
    print(f"h{h} n={n} | " + " ; ".join(f"{k} b={o.loc[k,'b']:+.1f} t={o.loc[k,'t']:+.2f}" for k in o.index[1:]) + " || gecikmeli: " + " ; ".join(f"{k} t={o2.loc[k,'t']:+.2f}" for k in o2.index[1:]))
