"""VİOP bülteninden sürekli (vadesi en yakın, vadeye <=2 iş günü kala bir sonrakine geçen) vadeli serisi."""
import numpy as np, pandas as pd
P = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/viop_panel.parquet'
_p = None
def panel():
    global _p
    if _p is None:
        p = pd.read_parquet(P, columns=['date', 'code', 'root', 'ctype', 'expiry', 'settle', 'prev_settle', 'open', 'close', 'vwap', 'value_tl', 'qty', 'trades', 'oi'])
        p = p[p.ctype.astype(str).isin(['D_EQ_FPD', 'D_IX_FUT'])]
        p['root'] = p['root'].astype(str); _p = p
    return _p
def cont(root, roll_bd=2):
    p = panel(); d = p[p.root == root].copy()
    d = d[d.expiry >= d.date]
    dates = np.sort(d.date.unique())
    # iş günü cinsinden vadeye kalan
    pos = {dt: i for i, dt in enumerate(dates)}
    exp_idx = d['expiry'].map(lambda e: np.searchsorted(dates, np.datetime64(e)))
    d['bd_left'] = exp_idx.values - d['date'].map(pos).values
    d = d[d.bd_left > roll_bd].sort_values(['date', 'expiry'])
    f = d.groupby('date').head(1).set_index('date')
    f['r'] = np.log(f['settle'] / f['prev_settle'])
    f.loc[(f['prev_settle'] <= 0) | (f['settle'] <= 0), 'r'] = np.nan
    f.loc[f['r'].abs() > np.log(1.105), 'r'] = np.nan
    f['ro_in'] = np.where((f['open'] > 0) & (f['trades'] > 0), np.log(f['settle'] / f['open']), np.nan)  # açılış(ilk işlem)->uzlaşma
    f['ro_gap'] = f['r'] - f['ro_in']
    f.index = pd.DatetimeIndex(f.index)
    return f
