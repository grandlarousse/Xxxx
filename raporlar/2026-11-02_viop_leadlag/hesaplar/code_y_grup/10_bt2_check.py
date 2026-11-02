"""BT2/BT2b sağlamlık: (a) sinyal ayrıştırma: lider gap'i tek başına / takipçinin KENDİ gap'i (fade) tek başına / birleşik;
(b) gerçekçi giriş: açılış yerine ilk saatlik barın kapanışı (10:30 TSİ) -> kapanış (h1 verisi 2023-12+); aynı örneklemde açılış girişiyle kıyas.
(c) regresyon: y_intra ~ b*x_gap + y_gap + XU_gap (kendi gap kontrollü lider katsayısı) IS/OOS."""
from gx import *
import importlib.util
spec = importlib.util.spec_from_file_location('b9', HERE + '/09_bt.py')
H1 = SCR + '/data/h1/'
def first_bar_close(sym):
    d = pd.read_parquet(H1 + S(sym) + '.parquet'); d = d[(d.index.hour == 6) & (d.index.minute == 30)]
    s = pd.Series(d['c'].values, index=pd.DatetimeIndex(d['ldate'].values)); return s[~s.index.duplicated()]
def nav_gap(h):
    import importlib.util as iu
    sp = iu.spec_from_file_location('n6', HERE + '/06_nav.py'); n6 = iu.module_from_spec(sp); sp.loader.exec_module(n6)
    W = n6.NAVW[h]; comps = [k for k in W if not k.endswith('=X')]
    w0 = pd.Series({k: W[k] for k in comps}); w0 /= w0.sum()
    rr = pd.concat({k: R(k) for k in comps}, axis=1); rr = rr[rr.index >= '2010-01-01']
    lvl = np.exp(rr.fillna(0).cumsum()); avail = rr.notna().cumsum() > 0
    val = (lvl * w0).where(avail, 0.0); wt = val.shift(1).div(val.shift(1).sum(axis=1), axis=0)
    g = pd.concat({k: DC(k)['gap'] for k in comps}, axis=1).reindex(wt.index)
    wg = wt.where(g.notna(), 0); wg = wg.div(wg.sum(axis=1), axis=0)
    return (wg * g.fillna(0)).sum(axis=1).where(wg.sum(axis=1) > 0), (wt * rr.fillna(0)).sum(axis=1)
CASES = [('KRDMD', 'KRDMA'), ('KRDMD', 'KRDMB'), ('TUPRS', 'AYGAZ'), ('TRMET', 'TRENJ'), ('TRALT', 'TRENJ'), ('VAKBN', 'VAKFN'), ('ALARK', 'ALCAR'), ('AEFES', 'CCOLA'),
         ('MGROS', 'AGHOL'), ('AEFES', 'AGHOL'), ('NAV', 'AGHOL'), ('NAV', 'ALARK'), ('NAV', 'TRENJ'), ('NAV', 'ECZYT'), ('NAV', 'SAHOL'), ('NAV', 'KCHOL'), ('NAV', 'BRYAT'), ('NAV', 'AEFES'),
         ('SAHOL', 'ENJSA'), ('KCHOL', 'TTRAK'), ('EREGL', 'ISDMR'), ('MGROS', 'SOKM'), ('SOKM', 'GOZDE'), ('GARAN', 'AKBNK'), ('THYAO', 'PGSUS')]
rows = []
XG = DC('XU100')['gap']
for x, y in CASES:
    dy = DC(y)
    if x == 'NAV':
        xg, xc = nav_gap(y)
    else:
        xg, xc = DC(x)['gap'], R(x)
    b = (R(y).rolling(250, min_periods=120).cov(xc) / xc.rolling(250, min_periods=120).var()).shift(1)
    lead = b * xg; own = -dy['gap']; comb = lead + own
    o = dict(leader=x, follower=y, viop=y in ll.VIOP, liq_y=liq(y)[0])
    for nm, sig in [('lead', lead), ('own', own), ('comb', comb)]:
        res, pnl = ll.backtest(sig, dy['intra'], cost_bps=8, mode='z', thr=1.0)
        o[f'{nm}_IS'] = res['IS'].get('mean_bps'); o[f'{nm}_OOS'] = res['OOS'].get('mean_bps'); o[f'{nm}_tOOS'] = res['OOS'].get('t')
    # regresyon: kendi gap ve XU gap kontrollü lider katsayısı
    X = pd.concat([lead.rename('L'), dy['gap'].rename('G'), XG.rename('M')], axis=1)
    for lab, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        yy = dy['intra'][(dy['intra'].index >= pd.Timestamp(lo)) & (dy['intra'].index < pd.Timestamp(hi))]
        r = nwreg(yy, X); o[f'regL_t_{lab}'] = r[0].tvalues[1] if r else np.nan; o[f'regG_t_{lab}'] = r[0].tvalues[2] if r else np.nan
    # gerçekçi giriş (h1)
    try:
        fb = first_bar_close(y); c = px(y)['c']; op = px(y)['o']
        late = np.log(c / fb.reindex(c.index)); early = np.log(c / op)
        late[late.abs() > 0.15] = np.nan  # h1-günlük birim uyumsuzluğu (bölünme/bedelsiz) koruması
        idx = late.dropna().index
        for nm, sig in [('lead', lead), ('comb', comb)]:
            for en, tgt in [('open', early.reindex(idx)), ('1030', late.reindex(idx))]:
                # z için geçmiş tam seriyi kullan, sonra örnekle
                df = pd.concat([sig.rename('s'), tgt.rename('y')], axis=1)
                mu = df['s'].rolling(250, min_periods=60).mean().shift(1); sd = df['s'].rolling(250, min_periods=60).std().shift(1)
                z = (df['s'] - mu) / sd; pos = np.sign(z).where(z.abs() > 1, 0)
                p = (pos * df['y'] - 8e-4 * pos.abs()).reindex(idx).dropna(); ps = pos.reindex(p.index)
                act = ps != 0
                o[f'h1_{nm}_{en}_bps'] = 1e4 * p[act].mean() if act.sum() > 10 else np.nan; o[f'h1_{nm}_{en}_t'] = ll.nw_t(p[act])[1] if act.sum() > 30 else np.nan; o['h1_n'] = int(act.sum())
    except Exception as e:
        o['h1_err'] = str(e)[:40]
    rows.append(o); print(x, y, {k: (round(v, 1) if isinstance(v, float) else v) for k, v in o.items() if k not in ('leader', 'follower')}, flush=True)
D = pd.DataFrame(rows); D.to_csv(HERE + '/res_bt2_check.csv', index=False)
