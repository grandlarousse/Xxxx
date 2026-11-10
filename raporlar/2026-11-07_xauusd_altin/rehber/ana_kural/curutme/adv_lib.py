"""Şüpheci hakem — bağımsız kütüphane. Ana ajanın kodundan fonksiyon kopyalanmadı.
Kural: e_d = r_GDX − b_GLD·r_GLD − b_SPY·r_SPY ; x = son k ABD gününün e toplamı (t-1 ABD kapanışında biter)."""
import numpy as np, pandas as pd, statsmodels.api as sm
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
OUT = S + "/out/net_adv"

def yahoo(tk, col="adjclose"):
    d = pd.read_parquet(f"{S}/panel/yahoo/{tk}.parquet")
    d.index = pd.to_datetime(d.index)
    return d[col].astype(float)

def us_returns(tickers=("GDX", "GLD", "SPY"), col="adjclose"):
    px = pd.concat({k: yahoo(k, col) for k in tickers}, axis=1).dropna()
    return np.log(px).diff().iloc[1:]

def rolling_resid(R, y="GDX", xs=("GLD", "SPY"), win=250, minobs=60, fixed=None):
    """Gün d artığı: betalar [d-win, d-1] penceresinden (sabitli OLS). fixed={'GLD':2.0,...} verilirse sabit beta."""
    Y = R[y].values; X = R[list(xs)].values; n = len(R)
    e = np.full(n, np.nan); B = np.full((n, len(xs)), np.nan)
    if fixed is not None:
        b = np.array([fixed[k] for k in xs]); e = Y - X @ b; B[:] = b
        return pd.Series(e, R.index), pd.DataFrame(B, R.index, columns=list(xs))
    for d in range(minobs, n):
        a = max(0, d - win)
        Z = np.column_stack([np.ones(d - a), X[a:d]])
        coef, *_ = np.linalg.lstsq(Z, Y[a:d], rcond=None)
        B[d] = coef[1:]
        e[d] = Y[d] - X[d] @ coef[1:]
    return pd.Series(e, R.index), pd.DataFrame(B, R.index, columns=list(xs))

def viop():
    pv = pd.read_parquet(f"{S}/panel/panel_viop.parquet"); pv.index = pd.to_datetime(pv.index)
    return pv

def map_us_to_viop(ser, vidx, extra_lag=0, same_day=False):
    """VİOP günü t → tarihi KESİN OLARAK t'den küçük son ABD gününün değeri (same_day=True → ≤ t : İLERİYE BAKAN, yalnız test için).
    extra_lag: ek ABD günü gecikmesi."""
    s = ser.dropna()
    d = s.index.values
    pos = np.searchsorted(d, vidx.values, side="right" if same_day else "left") - 1 - extra_lag
    out = np.where(pos >= 0, s.values[np.clip(pos, 0, len(s) - 1)], np.nan)
    used = np.where(pos >= 0, d[np.clip(pos, 0, len(s) - 1)], np.datetime64("NaT"))
    return pd.Series(out, vidx), pd.Series(used, vidx)

def fwd(r, h, skip=0):
    """t+1+skip .. t+h+skip log getirilerinin toplamı (t günü uzlaşmasında giriş)."""
    c = r.cumsum()
    return c.shift(-(h + skip)) - c.shift(-skip)

def nw_diff(y, s, L):
    d = pd.concat([y.rename("y"), s.rename("s")], axis=1).dropna()
    if d.s.sum() < 5 or d.s.sum() > len(d) - 5: return dict(diff=np.nan, t=np.nan, n1=int(d.s.sum()), N=len(d), m1=np.nan, m0=np.nan)
    m = sm.OLS(d.y, sm.add_constant(d.s)).fit(cov_type="HAC", cov_kwds={"maxlags": L})
    return dict(diff=m.params["s"] * 100, t=m.tvalues["s"], n1=int(d.s.sum()), N=len(d), m1=d.y[d.s > 0].mean() * 100, m0=d.y[d.s == 0].mean() * 100, mall=d.y.mean() * 100)

def position(sig, H):
    """pos[t]=1: t uzlaşmasında pozisyon taşınıyor (son H günde sinyal var)."""
    s = pd.Series(sig, dtype=float).fillna(0)
    return (s.rolling(H, min_periods=1).max() > 0).astype(float)

def pnl(pos, r, cost_bps):
    """Günlük basit getiri; maliyet: her bacakta cost/2 bps, işlemin yapıldığı uzlaşmayı izleyen güne yazılır."""
    simp = np.exp(r) - 1
    p = pos.shift(1) * simp
    turn = pos.diff().abs().fillna(pos.abs())
    p = p - turn.shift(1).fillna(0) * cost_bps / 2e4
    return p.iloc[1:]

def sharpe(p):
    p = p.dropna(); return p.mean() / p.std() * np.sqrt(252) if p.std() > 0 else np.nan

def trades(pos, r, cost_bps=0.0):
    """Her kesintisiz pozisyon bloğu = 1 işlem. Giriş: bloğun ilk günü uzlaşması; çıkış: bloğun son gününden sonraki günün uzlaşması."""
    pv = pos.values; rr = r.values; idx = pos.index; out = []
    i = 0; n = len(pv)
    while i < n:
        if pv[i] > 0:
            j = i
            while j + 1 < n and pv[j + 1] > 0: j += 1
            # tutulan getiriler: günler i+1 .. j+1
            if j + 1 < n:
                seg = rr[i + 1:j + 2]
                cum = np.cumsum(seg)
                out.append(dict(entry=idx[i], exit=idx[j + 1], days=j + 1 - i, ret=np.exp(seg.sum()) - 1 - cost_bps / 1e4,
                                mae=np.exp(min(cum.min(), 0)) - 1, mfe=np.exp(max(cum.max(), 0)) - 1, open_=False))
            else:
                seg = rr[i + 1:n]
                out.append(dict(entry=idx[i], exit=pd.NaT, days=n - 1 - i, ret=(np.exp(seg.sum()) - 1) if len(seg) else 0.0,
                                mae=np.nan, mfe=np.nan, open_=True))
            i = j + 1
        else:
            i += 1
    return pd.DataFrame(out)

def alpha(p, bh, L=5):
    d = pd.concat([p.rename("p"), bh.rename("b")], axis=1).dropna()
    m = sm.OLS(d.p, sm.add_constant(d.b)).fit(cov_type="HAC", cov_kwds={"maxlags": L})
    return m.params["const"] * 252 * 100, m.tvalues["const"], m.params["b"]

def maxdd(p):
    c = (1 + p.fillna(0)).cumprod(); return (c / c.cummax() - 1).min()
