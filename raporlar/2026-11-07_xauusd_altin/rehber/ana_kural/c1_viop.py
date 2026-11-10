"""Ek kontrol (10.11.2026): 'madenciler 10 gündür altından güçlü' sinyalinin (E2-C1) VİOP F_XAUUSD hedefine aktarımı.
Sinyal ham Yahoo'dan bağımsız kuruldu (hakem serisi kullanılmadı). Bilgi zamanı: t-1 ABD kapanışı; giriş gün t VİOP uzlaşması."""
import pandas as pd, numpy as np, statsmodels.api as sm, sys
S = sys.argv[1]
def yh(k):
    d = pd.read_parquet(f"{S}/panel/yahoo/{k}.parquet"); d.index = pd.to_datetime(d.index); return d["adjclose"]
px = pd.DataFrame({k: yh(k) for k in ["GDX", "GLD", "SPY"]}).dropna()
R = np.log(px).diff().dropna()
Y = R["GDX"].values; X = R[["GLD", "SPY"]].values
e = np.full(len(R), np.nan)
for i in range(60, len(R)):
    lo = max(0, i - 250); A = np.column_stack([np.ones(i - lo), X[lo:i]])
    b = np.linalg.lstsq(A, Y[lo:i], rcond=None)[0]
    e[i] = Y[i] - b[1] * X[i, 0] - b[2] * X[i, 1]
e = pd.Series(e, index=R.index)
E10 = e.rolling(10, min_periods=10).sum()          # gün d kapanışında biten 10 günlük artık
thr = float(E10[:"2017-12-31"].dropna().quantile(0.8))   # eşik yalnız 2008-2017'den
print("eşik (IS %80 kantil) %", round(thr * 100, 3))
pv = pd.read_parquet(f"{S}/panel/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index)
# VİOP günü t için: tarihi < t olan son ABD kapanışının E10'u
dates = E10.dropna().index
idx = np.searchsorted(dates.values, pv.index.values, side="left") - 1
x = pd.Series(np.where(idx >= 0, E10.dropna().values[np.clip(idx, 0, None)], np.nan), index=pv.index)
sig = (x > thr).astype(float)
r = pv.v_ret
def fwd(h, lag=0): return sum(r.shift(-k - lag) for k in range(1, h + 1))
def nw(y, s, L):
    d = pd.concat([y.rename("y"), s.rename("s")], axis=1).dropna()
    m = sm.OLS(d.y, sm.add_constant(d.s)).fit(cov_type="HAC", cov_kwds={"maxlags": L})
    return m.params["s"] * 100, m.tvalues["s"], int(d.s.sum()), len(d)
print("\nfark (sinyal günleri − diğer günler), NW t:")
for h in (1, 3, 5):
    for nm, a, b in [("2017-26", None, None), ("2017-21", None, "2021-12-31"), ("2022-26", "2022-01-01", None), ("2018-26 (eşik OOS)", "2018-01-01", None), ("2026 hariç", None, "2025-12-31")]:
        y = fwd(h)[a:b]; d, t, n, N = nw(y, sig[a:b], max(h, 5))
        print(f"  h{h} {nm:20s} fark {d:+.3f}%  t {t:5.2f}  sinyal günü {n}/{N}")
print("\nyıl yıl h=3 ve h=5: sinyal sonrası ortalama − tüm günler ortalaması (%):")
f3, f5 = fwd(3) * 100, fwd(5) * 100
yy = pd.DataFrame({"n": sig.groupby(sig.index.year).sum(), "h3_sin": f3[sig > 0].groupby(f3[sig > 0].index.year).mean(), "h3_tum": f3.groupby(f3.index.year).mean(),
                   "h5_sin": f5[sig > 0].groupby(f5[sig > 0].index.year).mean(), "h5_tum": f5.groupby(f5.index.year).mean()}).round(2)
print(yy.T.to_string())
print("\nplacebo: sinyal kaydırma (gün) → h3 fark t:")
for s in (-3, -1, 0, 1, 2, 5, 10):
    d, t, n, N = nw(fwd(3), sig.shift(s), 5); print(f"  kaydırma {s:+d}: fark {d:+.3f}% t {t:.2f}")
print("\neşik duyarlılığı (h3 / h5 fark t):")
for q in (0.6, 0.7, 0.75, 0.8, 0.85, 0.9):
    th = float(E10[:"2017-12-31"].dropna().quantile(q)); s2 = (x > th).astype(float)
    print(f"  q{q}: eşik %{th*100:.2f}  h3 t {nw(fwd(3), s2, 5)[1]:.2f}  h5 t {nw(fwd(5), s2, 5)[1]:.2f}  n {int(s2.sum())}")
print("\npencere duyarlılığı k (q80, h5 t):")
for k in (5, 8, 10, 12, 15, 20):
    Ek = e.rolling(k, min_periods=k).sum().dropna(); th = float(Ek[:"2017-12-31"].quantile(0.8))
    ii = np.searchsorted(Ek.index.values, pv.index.values, side="left") - 1
    xk = pd.Series(np.where(ii >= 0, Ek.values[np.clip(ii, 0, None)], np.nan), index=pv.index); sk = (xk > th).astype(float)
    print(f"  k{k}: h3 t {nw(fwd(3), sk, 5)[1]:.2f}  h5 t {nw(fwd(5), sk, 5)[1]:.2f}")
# sade işlem: sinyal günü uzlaşmada AL, son sinyalden H gün sonra SAT; yalnız uzun
def trade(H, cost_bps):
    pos = pd.Series(0.0, index=pv.index); left = 0
    for i, s in enumerate(sig.values):
        if s > 0: left = H
        pos.iloc[i] = 1.0 if left > 0 else 0.0
        left -= 1
    pnl = pos.shift(1) * (np.exp(r) - 1) - (pos - pos.shift(1)).abs().shift(1).fillna(0) * cost_bps / 2e4
    return pos, pnl.dropna()
def sh(p): return p.mean() / p.std() * np.sqrt(252) if p.std() > 0 else np.nan
bh = (np.exp(r) - 1).dropna()
print("\nsade işlem (yalnız AL; son sinyalden H gün sonra sat):")
for H in (3, 5):
    for c in (5, 22):
        pos, p = trade(H, c)
        ep = (pos.diff() > 0).sum()
        al = sm.OLS(p, sm.add_constant(bh.reindex(p.index))).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        print(f"  H={H} maliyet {c} bps: Sharpe tam {sh(p):.2f} | 2017-21 {sh(p[:'2021']):.2f} | 2022-26 {sh(p['2022':]):.2f} | 2026 {sh(p['2026':]):.2f} | yıllık %{p.mean()*252*100:.1f} | piyasada %{pos.mean()*100:.0f} | giriş/yıl {ep/(len(pos)/252):.0f} | B&H'ye göre alfa %{al.params['const']*252*100:.1f} (t {al.tvalues['const']:.2f}) | maks düşüş %{((1+p).cumprod()/(1+p).cumprod().cummax()-1).min()*100:.1f}")
print(f"  B&H: Sharpe tam {sh(bh):.2f} | 2017-21 {sh(bh[:'2021']):.2f} | 2022-26 {sh(bh['2022':]):.2f} | 2026 {sh(bh['2026':]):.2f} | yıllık %{bh.mean()*252*100:.1f} | maks düşüş %{((1+bh).cumprod()/(1+bh).cumprod().cummax()-1).min()*100:.1f}")
# işlem bazında (H=5): her giriş-çıkış bölümü
pos, p = trade(5, 5); g = (pos.diff().fillna(pos) > 0).cumsum()[pos > 0]
tr = (np.exp(r) - 1).reindex(pos.index); seg = pd.DataFrame({"g": g, "ret": tr.shift(-1)[g.index]}).dropna()
T = seg.groupby("g").ret.agg(lambda z: (1 + z).prod() - 1); L = seg.groupby("g").size()
print(f"\nişlem bazında (H=5): {len(T)} işlem, ort süre {L.mean():.1f} gün, ort getiri %{T.mean()*100:.2f}, medyan %{T.median()*100:.2f}, kazanan %{(T>0).mean()*100:.0f}, en kötü %{T.min()*100:.1f}, en iyi %{T.max()*100:.1f}")
T.index = [seg[seg.g == k].index[0] for k in T.index]
print("yıllara göre işlem sayısı / ort %:", T.groupby(T.index.year).agg(["size", "mean"]).assign(mean=lambda z: (z["mean"] * 100).round(2)).T.to_dict())
print("\nson 12 VİOP günü x% ve sinyal:"); print(pd.DataFrame({"x_pct": (x * 100).round(2), "sinyal": sig}).tail(12).T.to_string())
pd.DataFrame({"x": x, "sig": sig}).to_parquet(f"{S}/out/net/c1_viop_sig.parquet")
