"""Donem-bazli secim motoru (sektor rotasyonu ve kesitsel hisse testleri ortak).
Sinyal tarihi s_t (hafta/ay sonu kapanisi) -> islem e_t = s_t'den sonraki ilk islem gunu kapanisi -> donem getirisi e_t -> e_{t+1}."""
import numpy as np, pandas as pd
from ortak import calendar, period_engine, stats, to_usd, yearly

def exec_dates(sig_dates):
    cal = calendar(); pos = cal.searchsorted(sig_dates, side="right")
    ok = pos < len(cal)
    return pd.DatetimeIndex(sig_dates[ok]), pd.DatetimeIndex(cal[pos[ok]])

def period_R(px, ex):
    """px: gunluk duzeltmeli fiyat paneli (ffill'li). R[t] = px(e_{t+1})/px(e_t)-1"""
    v = px.reindex(ex)
    return (v.shift(-1) / v - 1).iloc[:-1]

def select(score, avail, k=None, q=None, bottom=False):
    """score/avail: (donem x varlik) numpy; her donem icin secilen sutun indeksleri"""
    out = []
    for t in range(score.shape[0]):
        s = score[t].copy(); ok = avail[t] & ~np.isnan(s)
        idx = np.flatnonzero(ok)
        if len(idx) == 0: out.append(np.array([], int)); continue
        n = k if k is not None else max(1, int(round(len(idx) * q)))
        n = min(n, len(idx))
        order = np.argsort(s[idx]) if bottom else np.argsort(-s[idx])
        out.append(idx[order[:n]])
    return out

def apply_regime(sel, regime):
    return [s if regime[t] else np.array([], int) for t, s in enumerate(sel)]

def placebo(sel, avail, R, cost_side, rf_p, n=300, seed=1, ls_bench=None):
    """Ayni donemlerde, ayni sayida ve ayni yenileme oranli rastgele secimler."""
    rng = np.random.default_rng(seed); res = []
    rep = []; prev = set()
    for s in sel:
        cur = set(map(int, s)); rep.append(len(cur - prev) if prev else len(cur)); prev = cur
    for _ in range(n):
        ps = []; held = []
        for t, s in enumerate(sel):
            k = len(s)
            if k == 0: ps.append(np.array([], int)); held = []; continue
            pool = np.flatnonzero(avail[t] & ~np.isnan(R[t]))
            held = [h for h in held if avail[t][h]]
            keep_n = max(0, min(len(held), k - rep[t]))
            keep = list(rng.choice(held, keep_n, replace=False)) if keep_n > 0 else []
            cand = np.setdiff1d(pool, keep)
            add = list(rng.choice(cand, min(k - len(keep), len(cand)), replace=False)) if len(cand) else []
            held = keep + add; ps.append(np.array(held, int))
        r, _ = period_engine(ps, R, cost_side, rf_p, ls_bench=ls_bench)
        res.append(r)
    return np.array(res)

def sharpe(r, rf, ppy):
    ex = np.asarray(r) - np.asarray(rf)
    return ex.mean() / ex.std() * np.sqrt(ppy) if ex.std() > 0 else np.nan
