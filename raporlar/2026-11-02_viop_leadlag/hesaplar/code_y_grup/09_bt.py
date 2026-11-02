"""Backtestler (look-ahead yok; IS 2014-2020 / OOS 2021-2026; maliyet bacak başına gidiş-dönüş 8 ve 15 bps).
BT1 NAV iskontosu z250 (kapanış t'de bilinir) -> t+1 AÇILIŞTA giriş, kalıcı pozisyon: (a) H - b*NAV spread, (b) H - b*XU030 (yalnız holding bacağı, VİOP endeks hedge).
BT2 Açılış ayrışması: s_t = b*NAVgap_t - Hgap_t (açılıştan sonra bilinir) -> H gün-içi (ham ve XU030-hedge). ll.backtest(z, thr=1).
BT3 Oran ortalamaya dönüş: S = cumsum(r_A - b r_B) (pay grubu b=1), z60 -> t+1 açılış girişli kalıcı spread pozisyonu.
BT4 TVF stres dönüşü: XU100 < -%3 günü sonrası TVF sepeti - sektör kontrol (t+1 cc kapanış girişi [iyimser] ve t+1 gün-içi)."""
from gx import *
import importlib.util
spec = importlib.util.spec_from_file_location('n6', HERE + '/06_nav.py'); n6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(n6)
XD = DC('XU030'); XR = R('XU030')
def stats(pnl, pos, legs_turn=None):
    out = {}
    for lab, lo, hi in [('ALL', '2014-01-01', '2027-01-01'), ('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        p = pnl[(pnl.index >= pd.Timestamp(lo)) & (pnl.index < pd.Timestamp(hi))].dropna(); ps = pos.reindex(p.index).fillna(0)
        act = ps != 0; n = int(act.sum())
        if n < 20: out[lab] = {'n': n}; continue
        m_, t_, _ = ll.nw_t(p[act], lags=5); vol = p.std() * np.sqrt(252)
        out[lab] = {'n': n, 'mean_bps': 1e4 * p[act].mean(), 't': t_, 'sharpe': (p.mean() * 252) / vol if vol > 0 else np.nan, 'hit': float((p[act] > 0).mean()), 'ann_pct': 100 * p.mean() * 252}
    yb = (1e4 * pnl[pos != 0].groupby(pnl[pos != 0].index.year).mean()).round(1)
    out['yrs_pos'] = float((yb > 0).mean()) if len(yb) else np.nan; out['by_year'] = yb.to_dict()
    return out
def persistent(z, gap, intra, cost_bps, legs, thr=1.0):
    """z_t kapanışta bilinir; pozisyon t+1 açılışında alınır. pnl_t = pos_{t-2}*gap_t + pos_{t-1}*intra_t - maliyet(|Δpos| t açılışında)."""
    df = pd.concat([z.rename('z'), gap.rename('g'), intra.rename('i')], axis=1).dropna(subset=['g', 'i'])
    pos = (-np.sign(df['z'])).where(df['z'].abs() > thr, 0.0).fillna(0.0)
    p1 = pos.shift(1).fillna(0); p2 = pos.shift(2).fillna(0)
    pnl = p2 * df['g'] + p1 * df['i'] - (cost_bps / 1e4) / 2 * legs * (p1 - p2).abs() * 2 / 2  # |Δ|=1 -> yarım tur her bacak; tam tur = açılış+kapanış
    # not: |Δ|=2 (yön değişimi) -> 2 x yarım tur; giriş+çıkış toplamı = cost_bps*legs (gidiş-dönüş)
    return pnl, p1
def nav_decomp(h):
    W = n6.NAVW[h]; comps = [k for k in W if not k.endswith('=X')]
    w0 = pd.Series({k: W[k] for k in comps}); w0 = w0 / w0.sum()
    rr = pd.concat({k: R(k) for k in comps}, axis=1); rr = rr[rr.index >= '2010-01-01']
    lvl = np.exp(rr.fillna(0).cumsum()); avail = rr.notna().cumsum() > 0
    val = (lvl * w0).where(avail, 0.0); wt = val.shift(1).div(val.shift(1).sum(axis=1), axis=0)
    g = pd.concat({k: DC(k)['gap'] for k in comps}, axis=1).reindex(wt.index); i = pd.concat({k: DC(k)['intra'] for k in comps}, axis=1).reindex(wt.index)
    wg = wt.where(g.notna(), 0); wg = wg.div(wg.sum(axis=1), axis=0)
    return (wg * g.fillna(0)).sum(axis=1).where(wg.sum(axis=1) > 0), (wg * i.fillna(0)).sum(axis=1).where(wg.sum(axis=1) > 0), (wt * rr.fillna(0)).sum(axis=1)
rows = []
def add(bt, name, target, cost, st, extra=''):
    r = dict(bt=bt, name=name, target=target, cost=cost, n_IS=st['IS'].get('n'), mean_IS=st['IS'].get('mean_bps'), t_IS=st['IS'].get('t'), sh_IS=st['IS'].get('sharpe'),
             n_OOS=st['OOS'].get('n'), mean_OOS=st['OOS'].get('mean_bps'), t_OOS=st['OOS'].get('t'), sh_OOS=st['OOS'].get('sharpe'), hit_OOS=st['OOS'].get('hit'), yrs_pos=st['yrs_pos'], by_year=str(st['by_year']), extra=extra)
    rows.append(r)
# ---------- BT1 & BT2 ----------
for h in ['KCHOL', 'SAHOL', 'AGHOL', 'ECZYT', 'ISCTR', 'TRENJ', 'TRMET', 'VESTL', 'BRYAT', 'AEFES', 'ALARK', 'DOHOL']:
    nv = pd.read_parquet(HERE + f'/nav_{h}.parquet'); dh = DC(h)
    if h == 'DOHOL':
        ng, ni, nc = DC('GWIND')['gap'], DC('GWIND')['intra'], R('GWIND')
    else:
        ng, ni, nc = nav_decomp(h)
    b = nv['beta_nav']; bm = (R(h).rolling(250, min_periods=120).cov(XR) / XR.rolling(250, min_periods=120).var()).shift(1)
    sp_g = dh['gap'] - b * ng; sp_i = dh['intra'] - b * ni
    hx_g = dh['gap'] - bm * XD['gap']; hx_i = dh['intra'] - bm * XD['intra']
    for cost in [8, 15]:
        if h != 'DOHOL':
            pnl, pos = persistent(nv['z250'], sp_g, sp_i, cost, 2); add('BT1', h, 'spread H-bNAV (kalici, z250>1)', cost, stats(pnl, pos))
        pnl, pos = persistent(nv['z250'], hx_g, hx_i, cost, 2); add('BT1', h, 'H-bXU030 (kalici, z250>1)', cost, stats(pnl, pos))
        # BT2
        sig = (b * ng - dh['gap'])
        for tname, tgt, legs in [('H intra', dh['intra'], 1), ('H-bXU030 intra', hx_i, 2), ('spread intra', sp_i, 2)]:
            res, pnl = ll.backtest(sig, tgt, cost_bps=cost * legs, mode='z', thr=1.0)
            pos = pd.Series(1.0, index=pnl.index).where(pnl != 0, 0)
            add('BT2', h, f'NAVgap ayrisma -> {tname}', cost, {'IS': res['IS'], 'OOS': res['OOS'], 'yrs_pos': float((pd.Series(res['by_year_bps']) > 0).mean()), 'by_year': res['by_year_bps']})
# BT2b: tek lider -> takipçi gün içi (en güçlü g2i çiftleri)
for x, y in [('KRDMD', 'KRDMA'), ('KRDMD', 'KRDMB'), ('TUPRS', 'AYGAZ'), ('TRMET', 'TRENJ'), ('TRALT', 'TRENJ'), ('VAKBN', 'VAKFN'), ('KCHOL', 'TTRAK'), ('SOKM', 'GOZDE'), ('ALARK', 'ALCAR'),
             ('MGROS', 'AGHOL'), ('AEFES', 'AGHOL'), ('SISE', 'ISCTR'), ('ISCTR', 'SISE'), ('TUPRS', 'KCHOL'), ('AKBNK', 'SAHOL'), ('SAHOL', 'ENJSA'), ('EREGL', 'ISDMR'), ('CCOLA', 'AEFES'), ('AEFES', 'CCOLA'),
             ('MGROS', 'SOKM'), ('THYAO', 'PGSUS'), ('GARAN', 'AKBNK'), ('EREGL', 'KRDMD')]:
    dx, dy = DC(x), DC(y)
    b = (R(y).rolling(250, min_periods=120).cov(R(x)) / R(x).rolling(250, min_periods=120).var()).shift(1)
    sig = b * dx['gap'] - dy['gap']
    for cost in [8, 15]:
        res, pnl = ll.backtest(sig, dy['intra'], cost_bps=cost, mode='z', thr=1.0)
        add('BT2b', f'{x}->{y}', 'takipci gun-ici', cost, {'IS': res['IS'], 'OOS': res['OOS'], 'yrs_pos': float((pd.Series(res['by_year_bps']) > 0).mean()), 'by_year': res['by_year_bps']}, extra='VIOP' if y in ll.VIOP else 'spot')
# ---------- BT3 oran ortalamaya dönüş ----------
for a, bb, typ in [('KRDMA', 'KRDMD', 'cls'), ('KRDMB', 'KRDMD', 'cls'), ('KRDMB', 'KRDMA', 'cls'), ('ISBTR', 'ISCTR', 'cls'),
                   ('AEFES', 'CCOLA', 'b'), ('EREGL', 'ISDMR', 'b'), ('TRMET', 'TRALT', 'b'), ('TRENJ', 'TRMET', 'b'), ('VESTL', 'VESBE', 'b'), ('BRYAT', 'BRSAN', 'b'),
                   ('ECZYT', 'ECILC', 'b'), ('ISCTR', 'SISE', 'b'), ('CIMSA', 'AKCNS', 'b'), ('ODAS', 'CANTE', 'b'), ('AGHOL', 'AEFES', 'b'), ('SAHOL', 'AKBNK', 'b'), ('KCHOL', 'TUPRS', 'b'), ('AYGAZ', 'TUPRS', 'b'),
                   ('ISCTR', 'TSKB', 'b'), ('ANSGR', 'ANHYT', 'b'), ('ALARK', 'ALCAR', 'b'), ('DOHOL', 'GWIND', 'b'), ('ULKER', 'SOKM', 'b'), ('FROTO', 'TOASO', 'b')]:
    ra, rb = R(a), R(bb); da, db = DC(a), DC(bb)
    beta = pd.Series(1.0, index=ra.index) if typ == 'cls' else (ra.rolling(250, min_periods=120).cov(rb) / rb.rolling(250, min_periods=120).var()).shift(1)
    s = (ra - beta * rb); S_ = s.fillna(0).cumsum()
    for win in [60, 250]:
        z = (S_ - S_.rolling(win, min_periods=win // 2).mean()) / S_.rolling(win, min_periods=win // 2).std()
        sg = da['gap'] - beta * db['gap']; si = da['intra'] - beta * db['intra']
        for cost in [8, 15]:
            pnl, pos = persistent(z, sg, si, cost, 2, thr=1.5 if win == 60 else 1.0)
            add('BT3', f'{a}/{bb}', f'oran z{win} (kalici)', cost, stats(pnl, pos), extra=typ)
# ---------- BT4 TVF stres dönüşü ----------
dd = pd.read_parquet(HERE + '/tvf_basket.parquet')
tv_now = ['THYAO', 'HALKB', 'TCELL', 'TTKOM', 'VAKBN']; JOIN = {'THYAO': '2017-02-06', 'HALKB': '2017-02-06', 'TCELL': '2020-10-22', 'TTKOM': '2022-03-11', 'VAKBN': '2023-03-01'}
def bk(names, col, join=True):
    cs = []
    for k in names:
        x = DC(k)[col].copy() if col != 'cc' else R(k).copy()
        if join and k in JOIN: x[x.index < pd.Timestamp(JOIN[k])] = np.nan
        cs.append(x)
    return pd.concat(cs, axis=1).mean(axis=1)
ctrl = ['GARAN', 'AKBNK', 'YKBNK', 'ISCTR', 'PGSUS']
m = R('XU100')
for thr in [-0.02, -0.03]:
    sig = (m < thr).astype(float).where(m.notna())
    for col in ['cc', 'intra']:
        tgt = bk(tv_now, col) - bk(ctrl, col, join=False)
        tgt = tgt[tgt.index >= '2017-02-06']
        for cost in [8, 15]:
            res, pnl = ll.backtest(sig.shift(1), tgt, cost_bps=cost * 2, mode='sign', thr=0.5)
            add('BT4', f'TVF-sektor | XU100<{thr}', f't+1 {col}' + (' (kapanis girisi, iyimser)' if col == 'cc' else ''), cost,
                {'IS': res['IS'], 'OOS': res['OOS'], 'yrs_pos': float((pd.Series(res['by_year_bps']) > 0).mean()), 'by_year': res['by_year_bps']})
B = pd.DataFrame(rows); B.to_csv(HERE + '/res_bt.csv', index=False)
pd.set_option('display.width', 260); pd.set_option('display.max_rows', 400); pd.set_option('display.max_colwidth', 40)
print(B[B.cost == 8].drop(columns=['by_year']).round(2).to_string())
