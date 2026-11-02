"""BT1 sağlamlık: NAV iskontosu z penceresi/eşik duyarlılığı (KCHOL, SAHOL, AGHOL, ECZYT, TRENJ, VESTL) – hedef H - b*XU030 ve spread."""
from gx import *
src = open(HERE + '/09_bt.py').read().split('rows = []')[0]
exec(src.replace('from gx import *', ''))
rows = []
for h in ['KCHOL', 'SAHOL', 'AGHOL', 'ECZYT', 'TRENJ', 'VESTL', 'AEFES']:
    nv = pd.read_parquet(HERE + f'/nav_{h}.parquet'); dh = DC(h); ng, ni, nc = nav_decomp(h)
    bm = (R(h).rolling(250, min_periods=120).cov(XR) / XR.rolling(250, min_periods=120).var()).shift(1); b = nv['beta_nav']
    for win in [60, 120, 250, 500]:
        D_ = nv['D']; z = (D_ - D_.rolling(win, min_periods=win // 2).mean()) / D_.rolling(win, min_periods=win // 2).std()
        for thr in [0.5, 1.0, 1.5]:
            for tn, g, i in [('H-bXU030', dh['gap'] - bm * XD['gap'], dh['intra'] - bm * XD['intra']), ('spread', dh['gap'] - b * ng, dh['intra'] - b * ni)]:
                pnl, pos = persistent(z, g, i, 8, 2, thr=thr); st = stats(pnl, pos)
                rows.append(dict(h=h, win=win, thr=thr, tgt=tn, mIS=st['IS'].get('mean_bps'), tIS=st['IS'].get('t'), mOOS=st['OOS'].get('mean_bps'), tOOS=st['OOS'].get('t'), shOOS=st['OOS'].get('sharpe'), yrs=st['yrs_pos']))
D = pd.DataFrame(rows); D.to_csv(HERE + '/res_nav_robust.csv', index=False)
pd.set_option('display.width', 220); pd.set_option('display.max_rows', 400)
print(D.groupby(['h', 'tgt'])[['tIS', 'tOOS']].agg(['mean', 'min', 'max']).round(2).to_string())
print(D[(D.h == 'KCHOL')].round(2).to_string())
