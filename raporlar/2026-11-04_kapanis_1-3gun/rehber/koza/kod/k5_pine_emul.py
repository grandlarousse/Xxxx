"""(4b) koza.pine mantığının Python'da bar-bar öykünmesi (sözdizimi değil, ALGORİTMA doğrulaması).
Pine: döngülü NaN-atlayan cov/var/std, shift(1) = [1], son geçerli fiyata göre getiri, bayat/limit maskesi.
İki girdi: (a) Yahoo 'adj' (araştırmayla aynı olmalı), (b) Yahoo 'c' (TradingView'ın temettüsüz kapanışına vekil)."""
import numpy as np, pandas as pd
import kl

SY = ['TRMET', 'TRALT', 'TRENJ', 'XU030']
D = {s: kl.spot_fresh(s) for s in SY}
# TradingView BIST tatillerinde bar göstermez -> takvim = en az bir geçerli getirisi olan gün (araştırmadaki dropna(how='all'))
cal = pd.DataFrame({s: kl.spot_ret_fresh(s) for s in SY}).dropna(how='all').index


def emul(field):
    px = {s: D[s][field].reindex(cal).values for s in ['TRMET', 'TRALT', 'TRENJ']}
    n = len(cal); R = {}
    for s, p in px.items():
        r = np.full(n, np.nan); last = np.nan
        for i in range(n):
            if np.isfinite(p[i]):
                if np.isfinite(last): r[i] = np.log(p[i] / last)
                last = p[i]
        pre = cal < kl.C.REG
        up = np.where(pre, np.log(1.205), np.log(1.105)); dn = np.where(pre, np.log(0.795), np.log(0.895))
        r[(r > up) | (r < dn)] = np.nan
        R[s] = r
    y, h, e = R['TRMET'], R['TRALT'], R['TRENJ']
    grp = np.where(np.isfinite(h) & np.isfinite(e), (h + e) / 2, np.nan)

    def fbeta(yv, xv, w=250, mp=120):
        out = np.full(n, np.nan)
        for t in range(n):
            a = max(0, t - w + 1); xs = xv[a:t + 1]; ys = yv[a:t + 1]
            mx = np.isfinite(xs); mxy = mx & np.isfinite(ys)
            nx, nxy = mx.sum(), mxy.sum()
            if nxy >= mp and nx >= mp and nxy > 1:
                cv = (np.sum(xs[mxy] * ys[mxy]) / nxy - xs[mxy].mean() * ys[mxy].mean()) * nxy / (nxy - 1)
                vx = xs[mx].var(ddof=1)
                if vx > 0: out[t] = cv / vx
        return out

    def fstd(xv, w=60, mp=40):
        out = np.full(n, np.nan)
        for t in range(n):
            xs = xv[max(0, t - w + 1):t + 1]; xs = xs[np.isfinite(xs)]
            if len(xs) >= mp: out[t] = xs.std(ddof=1)
        return out

    bG = np.r_[np.nan, fbeta(y, grp)[:-1]]; bG = np.clip(bG, 0.2, 2.0)
    u = y - bG * grp
    sd = fstd(u)
    z3 = (u + np.r_[np.nan, u[:-1]] + np.r_[np.nan, np.nan, u[:-2]]) / (sd * np.sqrt(3))
    return pd.Series(z3, index=cal)


R = pd.DataFrame({s: kl.spot_ret_fresh(s) for s in SY})
ref = kl.koza_signal(R, 'TRMET').z3
for f in ['adj', 'c']:
    z = emul(f); c = ref.dropna().index.intersection(z.dropna().index)
    c = c[c >= '2015-01-01']
    a0 = ref.reindex(c).abs() > 1.5; a1 = z.reindex(c).abs() > 1.5
    print(f"Pine öykünmesi [{f}] 2015+: ortak gün {len(c)}, maks |Δz3| {(ref.reindex(c) - z.reindex(c)).abs().max():.4f}, "
          f"ort |Δz3| {(ref.reindex(c) - z.reindex(c)).abs().mean():.4f}, |Δz3|>0,05 gün {int(((ref.reindex(c) - z.reindex(c)).abs() > 0.05).sum())}, "
          f"sinyal uyumu {(a0 == a1).mean():.4f} (farklı {int((a0 != a1).sum())} gün)")
    if f == 'c':
        dd = (ref.reindex(c) - z.reindex(c)).abs().sort_values(ascending=False).head(5)
        print('   en büyük farklar (temettü günleri olmalı):', ', '.join(f'{k.date()} {v:.2f}' for k, v in dd.items()))
        print('   son 5 gün z3 (adj / c):', ', '.join(f'{k.date()} {ref[k]:+.2f}/{z[k]:+.2f}' for k in c[-5:]))
