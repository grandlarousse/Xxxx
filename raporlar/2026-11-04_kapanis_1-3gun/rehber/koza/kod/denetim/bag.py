"""Denetim: BAĞIMSIZ sinyal (sinyal_koza.py / curlib / kl import EDİLMEZ). numpy pencere döngüleriyle.
Tanım (kullanıcıya verilen kural metninden): log getiri adj; bayat (v<=0 | h==l) fiyat yok; son geçerli fiyata göre getiri;
|r| limit üstü NaN (13.03.2020 öncesi ln1,205/ln0,795, sonrası ln1,105/ln0,895; XU030 hariç);
takvim = 4 serinin tarih birleşimi, en az bir getirisi olan gün; grp=ort(TRALT,TRENJ) ikisi de gerekli;
β = cov/var 250 pencere, min 120 (cov ortak geçerli çift, var x'in kendi geçerlileri), dünkü değere kadar; clip.
u = y − β_g grp ; z3 = Σ3 u (üçü de geçerli) / (std60 (min 40, ddof1) √3)."""
import numpy as np, pandas as pd
V = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/denetim_koza/veri/'
REG = pd.Timestamp('2020-03-13')

def load(sym, upto=None):
    d = pd.read_parquet(V + sym + '.IS.parquet')
    d = d[d.c.notna()].drop_duplicates('d', keep='last').set_index('d')
    if upto is not None: d = d[d.index <= pd.Timestamp(upto)]
    return d

def rets(d, sym):
    a = d.adj.values.astype(float).copy()
    if sym != 'XU030':
        st = (d.v.values <= 0) | (d.h.values == d.l.values)
        a[st] = np.nan
    r = np.full(len(a), np.nan); last = np.nan
    for i in range(len(a)):
        if np.isfinite(a[i]):
            if np.isfinite(last): r[i] = np.log(a[i] / last)
            last = a[i]
    s = pd.Series(r, index=d.index)
    if sym != 'XU030':
        pre = s.index < REG
        up = np.where(pre, np.log(1.205), np.log(1.105)); dn = np.where(pre, np.log(0.795), np.log(0.895))
        s[(s > up) | (s < dn)] = np.nan
    return s

def wbeta(y, x, w=250, mp=120):
    n = len(y); out = np.full(n, np.nan)
    for t in range(n):
        a = max(0, t - w + 1); xs = x[a:t+1]; ys = y[a:t+1]
        mx = np.isfinite(xs); mb = mx & np.isfinite(ys)
        if mb.sum() >= mp and mx.sum() >= mp:
            X = xs[mb]; Y = ys[mb]
            cv = np.sum((X - X.mean()) * (Y - Y.mean())) / (len(X) - 1)
            vx = np.var(xs[mx], ddof=1)
            if vx > 0: out[t] = cv / vx
    return np.r_[np.nan, out[:-1]]  # dünkü bilgiye kadar

def wstd(x, w=60, mp=40):
    n = len(x); out = np.full(n, np.nan)
    for t in range(n):
        xs = x[max(0, t - w + 1):t+1]; xs = xs[np.isfinite(xs)]
        if len(xs) >= mp: out[t] = np.std(xs, ddof=1)
    return out

def signal(upto=None, target='TRMET', tail=None):
    D = {s: load(s, upto) for s in ['TRMET', 'TRALT', 'TRENJ', 'XU030']}
    R = pd.DataFrame({s: rets(D[s], s) for s in D})
    R = R[R.notna().any(axis=1)]
    if tail: R = R.iloc[-tail:]
    hed = 'TRALT' if target == 'TRMET' else 'TRMET'
    y = R[target].values; h = R[hed].values; e = R.TRENJ.values
    grp = np.where(np.isfinite(h) & np.isfinite(e), 0.5 * (h + e), np.nan)
    bg = np.clip(wbeta(y, grp), 0.2, 2.0)
    u = y - bg * grp
    sd = wstd(u)
    s3 = u + np.r_[np.nan, u[:-1]] + np.r_[np.nan, np.nan, u[:-2]]
    z3 = s3 / (sd * np.sqrt(3))
    bH = np.clip(wbeta(y, h), 0.3, 2.0)
    out = pd.DataFrame({'r_y': y, 'r_h': h, 'r_e': e, 'grp': grp, 'b_g': bg, 'u': u, 'sd60': sd, 'z3': z3, 'bH': bH}, index=R.index)
    out['sig'] = np.where(np.isfinite(z3) & (np.abs(z3) > 1.5), np.sign(z3), 0)
    return out, D
