"""Kontrol: NAV sinyali yerine holdingin XU030'a göre kendi göreli fiyat sapması (z of cumsum(H - b*XU030)). NAV bilgi katıyor mu?
Ayrıca iki sinyal birlikte (regresyon: hedef ~ zNAV + zREL)."""
from gx import *
src = open(HERE + '/09_bt.py').read().split('rows = []')[0]
exec(src.replace('from gx import *', ''))
rows = []
for h in ['KCHOL', 'SAHOL', 'AGHOL', 'TRENJ', 'AEFES', 'ECZYT', 'VESTL', 'DOHOL', 'ALARK', 'ISCTR', 'TKFEN', 'ENKAI', 'THYAO', 'GARAN', 'BIMAS', 'EREGL', 'TUPRS', 'AKBNK']:
    dh = DC(h); bm = (R(h).rolling(250, min_periods=120).cov(XR) / XR.rolling(250, min_periods=120).var()).shift(1)
    rel = (R(h) - bm * XR); Srel = rel.fillna(0).cumsum()
    g = dh['gap'] - bm * XD['gap']; i = dh['intra'] - bm * XD['intra']
    for win in [60, 250]:
        zr = (Srel - Srel.rolling(win, min_periods=win // 2).mean()) / Srel.rolling(win, min_periods=win // 2).std()
        pnl, pos = persistent(zr, g, i, 8, 2, thr=1.0); st = stats(pnl, pos)
        o = dict(h=h, win=win, sig='REL(H-XU030)', mIS=st['IS'].get('mean_bps'), tIS=st['IS'].get('t'), mOOS=st['OOS'].get('mean_bps'), tOOS=st['OOS'].get('t'))
        rows.append(o)
        try:
            nv = pd.read_parquet(HERE + f'/nav_{h}.parquet'); D_ = nv['D']; zn = (D_ - D_.rolling(win, min_periods=win // 2).mean()) / D_.rolling(win, min_periods=win // 2).std()
            pnl, pos = persistent(zn, g, i, 8, 2, thr=1.0); st = stats(pnl, pos)
            rows.append(dict(h=h, win=win, sig='NAV', mIS=st['IS'].get('mean_bps'), tIS=st['IS'].get('t'), mOOS=st['OOS'].get('mean_bps'), tOOS=st['OOS'].get('t'), corr_z=zn.corr(zr)))
            # ortak regresyon: ertesi 5 gün göreli getiri ~ zNAV + zREL
            f5 = rel.shift(-1).rolling(5).sum().shift(-4)
            X = pd.concat([zn.rename('zn'), zr.rename('zr')], axis=1)
            for lab, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
                yy = f5[(f5.index >= pd.Timestamp(lo)) & (f5.index < pd.Timestamp(hi))]
                r = nwreg(yy, X, lags=10); rows[-1][f'reg_tNAV_{lab}'] = r[0].tvalues[1]; rows[-1][f'reg_tREL_{lab}'] = r[0].tvalues[2]
        except FileNotFoundError: pass
D = pd.DataFrame(rows); D.to_csv(HERE + '/res_nav_placebo.csv', index=False)
pd.set_option('display.width', 220); pd.set_option('display.max_rows', 100)
print(D.round(2).to_string())
