"""k_sahol_b: bagimsiz yeniden hesap kutuphanesi (k_sahol_a kodu import EDILMEZ).
Spot: dl_k_sahol_b/daily (03.11 kapanisi h1 15:00 barindan eklenir).
VIOP: data/viop_panel.parquet + dl_k_sahol_b/viop/*.csv (02.11, 03.11 kendi ayristiricim).
"""
import os, glob
import numpy as np, pandas as pd

S = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
DL = S + '/dl_k_sahol_b'
REG = pd.Timestamp('2020-03-13')
TICK = 0.01


# ---------------------------------------------------------------- spot
def spot(sym, add_last=True):
    d = pd.read_parquet(f'{DL}/daily/{sym}.IS.parquet')
    d = d.set_index(pd.DatetimeIndex(d['ldate']).normalize())[['o', 'h', 'l', 'c', 'adj', 'v']]
    d = d[~d.index.duplicated(keep='last')]
    # Yahoo tatil dolgusu: hacim 0 ve h==l -> at
    d = d[~((d.v == 0) & (d.h == d.l))]
    hp = f'{DL}/h1/{sym}.IS.parquet'
    if add_last and os.path.exists(hp):
        h = pd.read_parquet(hp)
        h['t'] = h.index.strftime('%H:%M')
        x = h[h.t == '15:00']
        for _, r in x.iterrows():
            dd = pd.Timestamp(r.ldate).normalize()
            if dd not in d.index and dd > d.index[-1]:
                d.loc[dd] = [np.nan, np.nan, np.nan, r.c, r.c, np.nan]
    return d.sort_index()


def hourly(sym):
    h = pd.read_parquet(f'{DL}/h1/{sym}.IS.parquet')
    h['t'] = h.index.strftime('%H:%M')
    h['ldate'] = pd.DatetimeIndex(h['ldate']).normalize()
    return h


def clean_ret(adj):
    r = np.log(adj).diff()
    simple = np.exp(r) - 1
    thr = np.where(adj.index < REG, 0.205, 0.105)
    r[np.abs(simple) > thr] = np.nan
    return r


def pair_frame(a, b, start='2003-01-01'):
    A = spot(a); B = spot(b)
    idx = A.index.intersection(B.index)
    idx = idx[idx >= start]
    A = A.loc[idx]; B = B.loc[idx]
    df = pd.DataFrame({'ca': A.c, 'cb': B.c, 'pa': A.adj, 'pb': B.adj}, index=idx)
    df['ra'] = clean_ret(df.pa); df['rb'] = clean_ret(df.pb)
    return df


def zsig(df, bw=250, bmin=125, zw=60, lag=1):
    ra, rb = df.ra, df.rb
    m = ra.notna() & rb.notna()
    ra2, rb2 = ra.where(m), rb.where(m)
    cov = ra2.rolling(bw, min_periods=bmin).cov(rb2)
    var = rb2.rolling(bw, min_periods=bmin).var()
    beta = (cov / var).shift(lag)
    e = (ra.fillna(0) - beta * rb.fillna(0))
    e = e.where(beta.notna(), 0.0)
    Sx = e.cumsum()
    mu = Sx.rolling(zw).mean(); sd = Sx.rolling(zw).std()
    z = (Sx - mu) / sd
    out = df.copy()
    out['beta'] = beta; out['S'] = Sx; out['z'] = z
    return out


def z_intraday(sig, pa_alt, pb_alt, zw=60):
    """Gun-ici fiyatla (pa_alt, pb_alt: ham fiyat, tarih indexli) z: gecmis kapanis S, son gun alt fiyat.
    Temettu duzeltmesi: adj/c orani degisimi eklenir."""
    fa = sig.pa / sig.ca; fb = sig.pb / sig.cb
    ea = np.log(pa_alt / sig.ca.shift(1)) + np.log(fa / fa.shift(1))
    eb = np.log(pb_alt / sig.cb.shift(1)) + np.log(fb / fb.shift(1))
    e_alt = ea - sig.beta * eb
    S_alt = sig.S.shift(1) + e_alt
    # pencere: S_{t-59..t-1} + S_alt_t
    s1 = sig.S.shift(1).rolling(zw - 1).sum(); q1 = (sig.S.shift(1) ** 2).rolling(zw - 1).sum()
    n = zw
    mu = (s1 + S_alt) / n
    var = (q1 + S_alt ** 2 - n * mu ** 2) / (n - 1)
    z = (S_alt - mu) / np.sqrt(var)
    return z


# ---------------------------------------------------------------- VIOP
def _parse_bulletin(fp):
    x = pd.read_csv(fp, sep=';', skiprows=[1], dtype=str)
    x.columns = [c.strip() for c in x.columns]
    x = x[x['SOZLESME KODU'].notna() & x['SOZLESME KODU'].str.startswith('F_')]
    o = pd.DataFrame({
        'date': pd.to_datetime(x['TARIH']), 'code': x['SOZLESME KODU'],
        'expiry': pd.to_datetime(x['VADE TARIHI']),
        'settle': pd.to_numeric(x['UZLASMA FIYATI'], errors='coerce'),
        'prev_settle': pd.to_numeric(x['ONCEKI UZLASMA FIYATI'], errors='coerce'),
        'value_tl': pd.to_numeric(x['ISLEM HACMI'], errors='coerce'),
        'qty': pd.to_numeric(x['ISLEM MIKTARI'], errors='coerce'),
        'oi': pd.to_numeric(x['ACIK POZISYON'], errors='coerce'),
        'und_raw': x['DAYANAK VARLIK']})
    o['root'] = o.code.str.slice(2, -4)
    return o


_PANEL = None
def panel():
    global _PANEL
    if _PANEL is None:
        p = pd.read_parquet(S + '/data/viop_panel.parquet',
                            columns=['date', 'code', 'root', 'expiry', 'settle', 'prev_settle', 'value_tl', 'qty', 'oi', 'ctype'])
        for c in ['root', 'code', 'ctype']:
            p[c] = p[c].astype(object).fillna('').astype(str)
        p = p[p.code.str.startswith('F_')]
        p = p[~p.ctype.str.contains('OPT')]
        new = [_parse_bulletin(f) for f in sorted(glob.glob(DL + '/viop/viop_*.csv'))]
        new = pd.concat(new) if new else pd.DataFrame()
        new = new[new.date > p.date.max()]
        p = pd.concat([p.drop(columns='ctype'), new[p.columns.drop('ctype')]], ignore_index=True)
        p['date'] = pd.to_datetime(p.date); p['expiry'] = pd.to_datetime(p.expiry)
        _PANEL = p
    return _PANEL


def fut_series(root, roll_bdays=1):
    """Tutulan sozlesme (vadeye roll_bdays'ten fazla is gunu kalan en yakin vade) ve gunluk TL fiyat degisimi.
    Satir d: tutulan c(d); F0 = settle_c(d) (d gunu); dF = settle_c(d') - settle_c(d) (d -> sonraki VIOP gunu)."""
    p = panel()
    q = p[(p.root == root) & p.settle.notna() & (p.settle > 0)].copy()
    cal = pd.DatetimeIndex(sorted(p.date.unique()))
    piv = q.pivot_table(index='date', columns='code', values='settle', aggfunc='last').reindex(cal)
    val = q.pivot_table(index='date', columns='code', values='value_tl', aggfunc='last').reindex(cal)
    exp = q.groupby('code').expiry.first()
    pos = {d: i for i, d in enumerate(cal)}
    rows = []
    for i, d in enumerate(cal[:-1]):
        nxt = cal[min(i + roll_bdays, len(cal) - 1)]
        cands = exp[(exp > nxt)]
        listed = piv.columns[piv.loc[d].notna()]
        cands = cands[cands.index.isin(listed)]
        if len(cands) == 0:
            rows.append((d, None, np.nan, np.nan, np.nan, pd.NaT)); continue
        c = cands.sort_values().index[0]
        f0 = piv.at[d, c]; f1 = piv.at[cal[i + 1], c] if c in piv.columns else np.nan
        rows.append((d, c, f0, f1 - f0, val.at[d, c], exp[c]))
    f = pd.DataFrame(rows, columns=['date', 'code', 'F0', 'dF', 'val', 'expiry']).set_index('date')
    f['roll'] = f.code != f.code.shift(1)
    return f


# ---------------------------------------------------------------- islem motoru
def gen_trades(z, entry=1.5, exit_=1.5, maxhold=None, fixed=None, stop=None, pnl_path=None, side='both'):
    """z: np.array (karar gunu kapanisi). Doner: list of (i0, i1, sgn). i1 = cikis gunu indeksi (uzlasma).
    sgn = +1 LONG spread (z<-entry), -1 SHORT spread (z>entry). Her bolume bir kez."""
    n = len(z); out = []
    pos = 0; i0 = None
    armS = False; armL = False
    for i in range(n):
        zt = z[i]
        if np.isnan(zt):
            continue
        if pos != 0:
            h = i - i0
            ex = False
            if fixed is not None:
                ex = h >= fixed
            else:
                if pos == -1 and zt <= exit_: ex = True
                if pos == 1 and zt >= -exit_: ex = True
                if maxhold is not None and h >= maxhold: ex = True
            if ex:
                out.append((i0, i, pos)); pos = 0
        if zt <= entry: armS = True
        if zt >= -entry: armL = True
        if pos == 0:
            if zt > entry and armS and side in ('both', 'short'):
                pos = -1; i0 = i; armS = False
            elif zt < -entry and armL and side in ('both', 'long'):
                pos = 1; i0 = i; armL = False
    return out  # acik islem dahil edilmez


def legs_viop(ra_root, rb_root, idx):
    fa = fut_series(ra_root).reindex(idx); fb = fut_series(rb_root).reindex(idx)
    return fa, fb


def eval_trades(tr, idx, FA0, dFA, FB0, dFB, rollA, rollB, beta, cA=8.0, cB=8.0, tick=True, tickA=TICK, tickB=TICK,
                ratio='beta', nS=None):
    """Sabit miktarli P&L, SAHOL(A) bacak nominaline gore bps. Dizi argumanlari np.array (idx hizali).
    Maliyet: bacak basina gidis-donus c bps (+1 tik/fiyat); her devirde tekrar.
    ratio: 'beta' (TL beta agirlikli), 'eq' (esit TL), 'int' (tam sayi, nS SAHOL kontrati)."""
    res = []
    n = len(idx)
    daily = np.zeros(n)
    for (i0, i1, s) in tr:
        if i1 >= n: continue
        b = beta[i0]
        a0 = FA0[i0]; b0 = FB0[i0]
        if np.isnan(a0) or np.isnan(b0) or np.isnan(b): continue
        if ratio == 'beta': w = b
        elif ratio == 'eq': w = 1.0
        elif ratio == 'int':
            NA = max(1, int(round(nS * b * a0 / b0))); w = NA * b0 / (nS * a0)
        sa = np.nansum(dFA[i0:i1]) / a0
        sb = np.nansum(dFB[i0:i1]) / b0
        if np.isnan(dFA[i0:i1]).any() or np.isnan(dFB[i0:i1]).any():
            bad = True
        else:
            bad = False
        gross = s * (sa - w * sb) * 1e4
        nroll = int(np.sum(rollA[i0 + 1:i1] | rollB[i0 + 1:i1]))
        one = cA + w * cB + ((tickA / a0 + w * tickB / b0) * 1e4 if tick else 0.0)
        cost = one * (1 + nroll)
        net = gross - cost
        for k in range(i0, i1):
            daily[k + 1] += s * (np.nan_to_num(dFA[k]) / a0 - w * np.nan_to_num(dFB[k]) / b0) * 1e4
        daily[i0] -= one / 2 * 1; daily[i1] -= one / 2
        if nroll:
            for k in range(i0 + 1, i1):
                if rollA[k] or rollB[k]: daily[k] -= one
        res.append(dict(d0=idx[i0], d1=idx[i1], sgn=s, hold=i1 - i0, beta=b, w=w, gross=gross, cost=cost, net=net,
                        nroll=nroll, bad=bad))
    return pd.DataFrame(res), pd.Series(daily, index=idx)


def nw_t(x, L=None):
    x = np.asarray(x, float); x = x[~np.isnan(x)]
    n = len(x)
    if n < 10: return np.nan
    if L is None: L = int(np.floor(4 * (n / 100) ** (2 / 9)))
    m = x.mean(); u = x - m
    g0 = (u * u).sum() / n; s = g0
    for l in range(1, L + 1):
        s += 2 * (1 - l / (L + 1)) * (u[l:] * u[:-l]).sum() / n
    return m / np.sqrt(s / n)


def summ(T, daily=None, a=None, b=None):
    if a is not None:
        T = T[(T.d0 >= a) & (T.d0 <= b)]
    if len(T) == 0:
        return dict(n=0)
    yrs = None
    o = dict(n=len(T), mean_net=T.net.mean(), med_net=T.net.median(), mean_gross=T.gross.mean(),
             t=T.net.mean() / (T.net.std(ddof=1) / np.sqrt(len(T))) if len(T) > 2 else np.nan,
             hit=(T.net > 0).mean(), hold_mean=T.hold.mean(), hold_med=T.hold.median(), worst=T.net.min(),
             p5=T.net.quantile(0.05), sum_net=T.net.sum())
    if daily is not None:
        d = daily
        if a is not None: d = d[(d.index >= a) & (d.index <= b)]
        o['t_nw'] = nw_t(d.values)
        eq = d.cumsum(); dd = eq - eq.cummax(); o['maxdd'] = dd.min()
        years = (d.index[-1] - d.index[0]).days / 365.25
        o['per_year'] = len(T) / years; o['ann_bps'] = d.sum() / years
        o['sharpe'] = d.mean() / d.std() * np.sqrt(252) if d.std() > 0 else np.nan
    return o


def fmt(o, keys=('n', 'mean_net', 't', 'hit', 'hold_mean', 'hold_med')):
    s = []
    for k in keys:
        v = o.get(k, np.nan)
        if isinstance(v, (float, np.floating)):
            s.append(f'{k}={v:.2f}')
        else:
            s.append(f'{k}={v}')
    return ' '.join(s)
