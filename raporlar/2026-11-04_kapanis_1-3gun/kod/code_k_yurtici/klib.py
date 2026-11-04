"""k_yurtici ortak yardımcılar: kapanıştan kapanışa (VİOP uzlaşmasından uzlaşmaya) 1–3 gün testleri.
Çalıştırma: cd out/code_k_yurtici && nice -n 10 python3 <betik>.py
Kurallar:
- Giriş E0 = VİOP uzlaşma_t (≈18:00–18:10 VWAP), çıkış uzlaşma_{t+h}; h ∈ {1,2,3,5} iş günü.
- E1 = VİOP son işlem (kapanış)_t ile giriş (uzlaşma yerine), çıkış uzlaşma_{t+h}.
- E2 = sinyal t, giriş uzlaşma_{t+1} (1 gün gecikmeli; ileriye bakma riski sıfır), çıkış uzlaşma_{t+1+h}.
- Sözleşme seçimi: t'de ön vade (c1); c1 vadesi çıkış gününden önce doluyorsa ya da t vade günüyse c2. Tutma süresince sözleşme sabit, roll yok.
- Getiri: aynı sözleşmenin günlük log(uzlaşma/önceki uzlaşma) zinciri (bültende önceki uzlaşma = dünkü uzlaşma, %100).
- Kurumsal işlem günleri (spot fiyat oranı ile düzeltilmiş oran ≥%3 ayrışır VE vadeli fiyat oranını izler) ile limit üstü sıçramalar NaN.
- Spot: adj (temettü düzeltmeli) kapanıştan kapanışa; ll._bad (rejime bağlı ±%20,5/±%10,5) ve bayat gün temizliği.
- Maliyet: pay vadelisi bacak başına gidiş-dönüş 8 ve 15 bps; XU030 vadelisi 3 bps.
- IS/OOS: VİOP 2017–2021 / 2022–2026; spot 2014–2020 / 2021–2026.
"""
import os, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
S = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
sys.path.insert(0, S + '/code'); import ll  # noqa
HERE = os.path.dirname(os.path.abspath(__file__))
RES = HERE + '/res'; os.makedirs(RES, exist_ok=True)
VIOP47 = list(ll.VIOP)
H = [1, 2, 3, 5]
COSTS = [8, 15]
IDX_COST = 3
V_IS_END = pd.Timestamp('2021-12-31'); S_IS_END = pd.Timestamp('2020-12-31')
REG = pd.Timestamp('2020-03-13')

# ---------------- VİOP ----------------
def _viop_raw():
    F = pd.read_parquet(S + '/data/viop_panel.parquet',
                        columns=['date', 'code', 'und', 'segment', 'ctype', 'expiry', 'settle', 'prev_settle', 'open', 'high', 'low', 'close', 'vwap',
                                 'value_tl', 'trades', 'oi'])
    for c in ['code', 'und', 'segment', 'ctype']: F[c] = F[c].astype(str)
    F = F[((F.segment == 'SSF') & F.und.isin(VIOP47)) | ((F.und == 'XU030') & (F.ctype == 'D_IX_FUT'))].copy()
    F = F.drop_duplicates(['code', 'date'], keep='last')
    for c in ['settle', 'prev_settle', 'open', 'high', 'low', 'close', 'vwap']:
        F[c] = F[c].where(F[c] > 0)
    F['date'] = pd.to_datetime(F['date']); F['expiry'] = pd.to_datetime(F['expiry'])
    F = F[F.expiry >= F.date]
    return F

def viop_cal():
    F = pd.read_parquet(S + '/data/viop_panel.parquet', columns=['date'])
    return pd.DatetimeIndex(sorted(pd.to_datetime(F['date']).unique()))

def spot_wide():
    """177 hisse + endeksler: dict o,h,l,c,adj,v (geniş), bayat gün NaN."""
    p = S + '/out/code_y_akis/_panel_ohlc.parquet'
    P = pd.read_parquet(p)
    out = {k: P[k].copy() for k in ['o', 'h', 'l', 'c', 'adj', 'v']}
    for ix in ['XU100', 'XU030', 'XBANK', 'XHOLD']:
        try:
            d = ll.raw(ix + '.IS').copy(); d.index = pd.DatetimeIndex(d['ldate'].values); d = d[~d.index.duplicated(keep='last')]
            for k in out: out[k][ix] = d[k].reindex(out[k].index) if k in d else np.nan
        except Exception as e:
            print('idx yok', ix, e)
    st = (out['v'].fillna(0) <= 0) & (out['h'] == out['l'])
    for ix in ['XU100', 'XU030', 'XBANK', 'XHOLD']: st[ix] = False
    for k in ['o', 'h', 'l', 'c', 'adj']: out[k] = out[k].where(~st)
    return out

def spot_ret(W=None):
    """Günlük spot log getiri (adj), rejime bağlı temizlik. Geniş DataFrame."""
    if W is None: W = spot_wide()
    a = W['adj']
    r = np.log(a / a.ffill().shift(1))  # bayat gün sonrası: son geçerli kapanıştan
    r = r.where(a.notna())
    idx = r.index; pre = np.asarray(idx < REG)[:, None]
    up = np.where(pre, np.log(1.205), np.log(1.105)); dn = np.where(pre, np.log(0.795), np.log(0.895))
    bad = (r.values > up) | (r.values < dn)
    r = r.mask(bad)
    return r

def fwd_sum(r, h):
    """r: geniş günlük getiri; t'den t+h'ye (t+1..t+h toplam). NaN varsa NaN."""
    return r[::-1].rolling(h, min_periods=h).sum()[::-1].shift(-1)

def build_fut(force=False):
    """Uzun panel: date, und, c1 bilgileri, r_set (c1 uzlaşma getirisi t), limit bayrakları, ileri getiriler f0_h (uzlaşma_t→uzlaşma_t+h), f1_h (kapanış_t→uzlaşma_t+h)."""
    p = RES + '/_fut.parquet'
    if os.path.exists(p) and not force: return pd.read_parquet(p)
    F = _viop_raw(); cal = viop_cal(); pos = pd.Series(np.arange(len(cal)), index=cal)
    W = spot_wide()
    out = []
    for u, g in F.groupby('und'):
        g = g.sort_values(['date', 'expiry'])
        g['r'] = np.log(g['settle'] / g['prev_settle'])
        # limit üstü / kurumsal işlem
        pre = g['date'] < REG
        lim = np.where(pre, np.log(1.205), np.log(1.105)); limd = np.where(pre, np.log(0.795), np.log(0.895))
        g.loc[(g['r'] > lim) | (g['r'] < limd), 'r'] = np.nan
        if u in W['c'].columns:
            c = W['c'][u]; a = W['adj'][u]
            pr = np.log(c / c.ffill().shift(1)); ar = np.log(a / a.ffill().shift(1))
            ca = ((pr - ar).abs() > 0.03)  # temettü/bedelsiz günü
            cad = set(ca[ca].index)
            m = g['date'].isin(cad)
            if m.any():
                prd = g.loc[m, 'date'].map(pr); ard = g.loc[m, 'date'].map(ar)
                # vadeli fiyat oranını izliyorsa (bedelsiz düzeltmesi) NaN; düzeltilmiş oranı izliyorsa (temettü) dokunma
                follow_price = (g.loc[m, 'r'] - prd).abs() < (g.loc[m, 'r'] - ard).abs()
                g.loc[m[m].index[follow_price.values], 'r'] = np.nan
        Rw = g.pivot(index='date', columns='code', values='r').reindex(cal)
        listed = g.pivot(index='date', columns='code', values='settle').reindex(cal).notna()
        exp = g.groupby('code')['expiry'].first()
        # c1, c2 her gün
        gg = g.copy(); gg['rk'] = gg.groupby('date').cumcount()
        c1 = gg[gg.rk == 0].set_index('date'); c2 = gg[gg.rk == 1].set_index('date')
        D = pd.DataFrame(index=c1.index)
        for col in ['code', 'expiry', 'settle', 'prev_settle', 'open', 'high', 'low', 'close', 'vwap', 'value_tl', 'trades', 'oi', 'r']:
            D['c1_' + col] = c1[col]
        D['c2_code'] = c2['code'].reindex(D.index); D['c2_expiry'] = c2['expiry'].reindex(D.index)
        D['c2_settle'] = c2['settle'].reindex(D.index); D['c2_close'] = c2['close'].reindex(D.index); D['c2_trades'] = c2['trades'].reindex(D.index)
        D['tot_value'] = g.groupby('date')['value_tl'].sum(); D['tot_trades'] = g.groupby('date')['trades'].sum()
        D['und'] = u
        D['raw_r'] = np.log(D['c1_settle'] / D['c1_prev_settle'])
        rr = np.exp(D['raw_r']) - 1; pre = D.index < REG
        thr = np.where(pre, 0.195, 0.097)
        D['lock_up'] = rr >= thr; D['lock_dn'] = rr <= -thr
        ip = pos.reindex(D.index).values
        for h in H + [6]:
            FS = fwd_sum(Rw, h)  # geniş: t'den t+h'ye
            ex_date = pd.Series([cal[i + h] if i + h < len(cal) else pd.NaT for i in ip], index=D.index)
            use_c1 = (D['c1_expiry'] >= ex_date) & (D['c1_expiry'] > D.index.to_series())
            code = np.where(use_c1, D['c1_code'], D['c2_code'])
            col_idx = {c: j for j, c in enumerate(FS.columns)}
            row_idx = pos.reindex(D.index).values
            vals = FS.values
            f = np.array([vals[ri, col_idx[c]] if (isinstance(c, str) and c in col_idx) else np.nan for ri, c in zip(row_idx, code)])
            D[f'f0_{h}'] = f
            # E1: kapanıştan giriş
            st = np.where(use_c1, D['c1_settle'], D['c2_settle']); cl = np.where(use_c1, D['c1_close'], D['c2_close'])
            D[f'f1_{h}'] = f + np.log(st.astype(float) / cl.astype(float))
            D[f'code_{h}'] = code
        out.append(D.reset_index().rename(columns={'index': 'date'}))
    P = pd.concat(out, ignore_index=True)
    P['date'] = pd.to_datetime(P['date'])
    P.to_parquet(p, index=False)
    return P

def fut_wide(col, P=None):
    if P is None: P = build_fut()
    return P.pivot(index='date', columns='und', values=col)

# ---------------- istatistik ----------------
def nw_t(x, lags=5):
    x = pd.Series(x).dropna().values; n = len(x)
    if n < 8: return np.nan, np.nan, n
    m = x.mean(); e = x - m; v = e @ e / n
    for l in range(1, min(lags, n - 1) + 1): v += 2 * (1 - l / (lags + 1)) * (e[l:] @ e[:-l]) / n
    return m, (m / np.sqrt(v / n) if v > 0 else np.nan), n

def p_from_t(t):
    from scipy import stats
    return float(2 * (1 - stats.norm.cdf(abs(t)))) if np.isfinite(t) else np.nan

def cl_t(d, ret, date, lags):
    """İşlem ağırlıklı ortalama; tarih kümelemeli + NW (lags iş günü) SE. d: DataFrame."""
    x = d[ret].values; N = len(x)
    if N < 5: return np.nan, np.nan
    m = x.mean(); e = x - m
    U = pd.Series(e).groupby(d[date].values).sum()
    idx = pd.bdate_range(U.index.min(), U.index.max()); U = U.reindex(idx).fillna(0).values
    v = U @ U
    for l in range(1, lags + 1):
        v += 2 * (1 - l / (lags + 1)) * (U[l:] @ U[:-l])
    se = np.sqrt(v) / N
    return m, (m / se if se > 0 else np.nan)

def trade_stats(tr, ret='ret', date='date', h=1, legs=1, is_end=V_IS_END, costs=COSTS):
    """tr: işlem başına satırlar (date = giriş günü, ret = brüt log getiri, yön uygulanmış).
    Ortalama işlem ağırlıklı; t = tarih kümelemeli + NW(h) (aynı gün ve örtüşen pencerelerdeki işlemler bağımlı sayılır).
    t_day = gün ortalamaları serisinin NW t'si (her gün eşit ağırlık; kıyas)."""
    d = tr[[date, ret]].dropna()
    if len(d) == 0: return dict(n=0)
    m, t = cl_t(d, ret, date, max(h, 1))
    dm = d.groupby(date)[ret].mean(); md, td, nd = nw_t(dm, lags=max(h, 1))
    yrs = (d[date].max() - d[date].min()).days / 365.25
    o = dict(n=len(d), n_days=nd, per_yr=round(len(d) / max(yrs, 0.5), 1), gross=1e4 * m, t=t, hit=(d[ret] > 0).mean(),
             gross_daymean=1e4 * md, t_day=td)
    for c in costs: o[f'net{c}'] = o['gross'] - c * legs
    for c in costs: o[f't_net{c}'] = (t * (o['gross'] - c * legs) / o['gross']) if o['gross'] != 0 and np.isfinite(t) else np.nan
    for lab, sub in [('IS', d[d[date] <= is_end]), ('OOS', d[d[date] > is_end])]:
        if len(sub) >= 5:
            m2, t2 = cl_t(sub, ret, date, max(h, 1))
            o[f'{lab}_n'] = len(sub); o[f'{lab}_gross'] = 1e4 * m2; o[f'{lab}_t'] = t2
            o[f'{lab}_net8'] = 1e4 * m2 - 8 * legs
        else:
            o[f'{lab}_n'] = len(sub); o[f'{lab}_gross'] = np.nan; o[f'{lab}_t'] = np.nan; o[f'{lab}_net8'] = np.nan
    yy = d.groupby(d[date].dt.year)[ret].mean() * 1e4
    o['yrs_pos'] = f'{(yy > 0).sum()}/{len(yy)}'
    o['by_year'] = ' '.join(f'{k % 100:02d}:{v:+.0f}' for k, v in yy.items())
    o['p'] = p_from_t(t)
    return o

def bh(p, q=0.05):
    p = np.asarray(p, float); n = np.isfinite(p).sum(); out = np.zeros(len(p), bool)
    if n == 0: return out
    idx = np.where(np.isfinite(p))[0]; ps = p[idx]; o = np.argsort(ps)
    thr = q * np.arange(1, n + 1) / n; ok = ps[o] <= thr
    if ok.any():
        k = np.max(np.where(ok)[0]); out[idx[o[:k + 1]]] = True
    return out

def bh_q(p):
    """BH q-değerleri."""
    p = np.asarray(p, float); q = np.full(len(p), np.nan); idx = np.where(np.isfinite(p))[0]
    if len(idx) == 0: return q
    ps = p[idx]; o = np.argsort(ps); n = len(ps)
    qq = ps[o] * n / np.arange(1, n + 1); qq = np.minimum.accumulate(qq[::-1])[::-1]
    q[idx[o]] = np.minimum(qq, 1); return q

REGISTRY = []
def reg(block, name, inst, entry, h, st, extra=None):
    r = dict(block=block, name=name, inst=inst, entry=entry, h=h)
    r.update({k: (round(v, 2) if isinstance(v, float) else v) for k, v in st.items()})
    if extra: r.update(extra)
    REGISTRY.append(r); return r

def save_registry(block):
    D = pd.DataFrame([r for r in REGISTRY if r['block'] == block])
    D.to_csv(RES + f'/tests_{block}.csv', index=False)
    return D

def fmt(st, legs=1):
    if not st or st.get('n', 0) == 0: return 'n=0'
    return (f"n={st['n']} ({st['per_yr']}/yıl) brüt {st['gross']:+.1f} net8 {st.get('net8', np.nan):+.1f} net15 {st.get('net15', np.nan):+.1f} t {st['t']:.2f} "
            f"isabet {st['hit']:.2f} (gün-ağ. {st['gross_daymean']:+.1f}, t {st['t_day']:.2f}) | IS {st.get('IS_gross', np.nan):+.1f} (t {st.get('IS_t', np.nan):.2f}, n {st.get('IS_n')}) OOS {st.get('OOS_gross', np.nan):+.1f} (t {st.get('OOS_t', np.nan):.2f}, n {st.get('OOS_n')}) yıl+ {st['yrs_pos']}")

def beta_roll(r, m, w=250, mp=120):
    return (r.rolling(w, min_periods=mp).cov(m) / m.rolling(w, min_periods=mp).var()).shift(1)

# ---------------- olay yardımcıları ----------------
_CACHE = {}
def ctx():
    """Önbellekli bağlam: VİOP paneli, geniş vadeli ileri getiriler, spot getiri, spot ileri getiriler, betalar."""
    if 'P' in _CACHE: return _CACHE
    P = build_fut(); _CACHE['P'] = P
    vcal = viop_cal(); _CACHE['vcal'] = vcal
    _CACHE['F'] = {f'f{e}_{h}': P.pivot(index='date', columns='und', values=f'f{e}_{h}').reindex(vcal) for e in [0, 1] for h in H + [6]}
    for c in ['lock_up', 'lock_dn', 'raw_r', 'c1_trades', 'tot_value', 'c1_settle', 'c1_close', 'c1_vwap']:
        _CACHE[c] = P.pivot(index='date', columns='und', values=c).reindex(vcal)
    W = spot_wide(); r = spot_ret(W); _CACHE['W'] = W; _CACHE['r'] = r
    _CACHE['scal'] = r.index
    _CACHE['SF'] = {h: fwd_sum(r, h) for h in H + [6, 10, 20]}
    # beta: spot 250g vs XU030 (t-1'e kadar)
    m = r['XU030']
    _CACHE['beta'] = pd.DataFrame({c: beta_roll(r[c], m) for c in r.columns if c not in ['XU100', 'XU030', 'XBANK', 'XHOLD']})
    return _CACHE

def fut_trade(und, d_entry, h, side=1, entry='E0', hedge=False):
    """Tek işlem: VİOP uzlaşma girişli brüt log getiri (yön uygulanmış). d_entry VİOP takviminde olmalı."""
    C = ctx(); key = f"f{'1' if entry == 'E1' else '0'}_{h}"
    try: x = C['F'][key].at[d_entry, und]
    except KeyError: return np.nan
    if hedge:
        b = C['beta'][und].asof(d_entry) if und in C['beta'] else 1.0
        if not np.isfinite(b): b = 1.0
        xm = C['F'][f'f0_{h}'].at[d_entry, 'XU030'] if d_entry in C['F'][f'f0_{h}'].index else np.nan
        x = x - b * xm
    return side * x

def vectorized_fut(ev, h, entry='E0', hedge=False, und='und', date='date', side='side'):
    """ev: DataFrame (und, date=giriş günü VİOP takviminde, side). Döner: brüt getiri dizisi."""
    C = ctx(); key = f"f{'1' if entry == 'E1' else '0'}_{h}"
    Fm = C['F'][key]
    ri = Fm.index.get_indexer(ev[date]); ci = Fm.columns.get_indexer(ev[und])
    ok = (ri >= 0) & (ci >= 0)
    x = np.full(len(ev), np.nan); x[ok] = Fm.values[ri[ok], ci[ok]]
    if hedge:
        Bm = C['beta']; bri = Bm.index.get_indexer(ev[date], method='ffill'); bci = Bm.columns.get_indexer(ev[und])
        b = np.full(len(ev), 1.0); okb = (bri >= 0) & (bci >= 0); b[okb] = Bm.values[bri[okb], bci[okb]]
        b = np.where(np.isfinite(b), b, 1.0)
        xm = np.full(len(ev), np.nan); xc = Fm.columns.get_loc('XU030'); xm[ri >= 0] = Fm.values[ri[ri >= 0], xc]
        x = x - b * xm
    return ev[side].values * x

def vectorized_spot(ev, h, excess='XU100', und='und', date='date', side='side'):
    C = ctx(); Fm = C['SF'][h]
    ri = Fm.index.get_indexer(ev[date]); ci = Fm.columns.get_indexer(ev[und])
    ok = (ri >= 0) & (ci >= 0)
    x = np.full(len(ev), np.nan); x[ok] = Fm.values[ri[ok], ci[ok]]
    if excess:
        xc = Fm.columns.get_loc(excess); xm = np.full(len(ev), np.nan); xm[ri >= 0] = Fm.values[ri[ri >= 0], xc]
        x = x - xm
    return ev[side].values * x

def shift_date(dates, k, cal):
    """dates'i cal takviminde k iş günü kaydır (dates cal'da yoksa: k>=0 ise sonraki ilk gün baz alınır)."""
    cal = pd.DatetimeIndex(cal); dates = pd.DatetimeIndex(dates); i = cal.searchsorted(dates)
    # takvim dışı (ör. vadeli öncesi) tarihleri ele: en yakın sonraki işlem günü ≤5 takvim günü uzakta olmalı
    ic = np.clip(i, 0, len(cal) - 1)
    near = (i < len(cal)) & ((cal.values[ic] - dates.values) <= np.timedelta64(5, 'D')) & (dates.values >= cal.values[0])
    j = i + k; out = np.full(len(j), np.datetime64('NaT'), dtype='datetime64[ns]')
    ok = near & (j >= 0) & (j < len(cal)); out[ok] = cal.values[j[ok]]
    return pd.DatetimeIndex(out)
