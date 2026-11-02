"""BT3 sağlamlık: SAHOL/AKBNK ve KCHOL NAV sinyalinin parametre duyarlılığı + grup dışı yüksek korelasyonlu çiftlerde aynı oran-MR (plasebo)."""
from gx import *
import importlib.util
spec = importlib.util.spec_from_file_location('b9', HERE + '/09_bt.py')
src = open(HERE + '/09_bt.py').read().split('# ---------- BT1 & BT2 ----------')[0]
exec(src.replace('from gx import *', ''))
def ratio_bt(a, bb, win, thr, cost=8, beta1=False):
    ra, rb = R(a), R(bb); da, db = DC(a), DC(bb)
    beta = pd.Series(1.0, index=ra.index) if beta1 else (ra.rolling(250, min_periods=120).cov(rb) / rb.rolling(250, min_periods=120).var()).shift(1)
    S_ = (ra - beta * rb).fillna(0).cumsum()
    z = (S_ - S_.rolling(win, min_periods=win // 2).mean()) / S_.rolling(win, min_periods=win // 2).std()
    pnl, pos = persistent(z, da['gap'] - beta * db['gap'], da['intra'] - beta * db['intra'], cost, 2, thr=thr)
    return stats(pnl, pos)
rows = []
for a, bb, g in [('SAHOL', 'AKBNK', 'grup'), ('KCHOL', 'YKBNK', 'grup'), ('KCHOL', 'FROTO', 'grup'), ('AGHOL', 'MGROS', 'grup'), ('ISCTR', 'SISE', 'grup'), ('ISCTR', 'ISMEN', 'grup'), ('EREGL', 'ISDMR', 'grup'), ('VESTL', 'VESBE', 'grup'), ('TRMET', 'TRALT', 'grup'), ('AEFES', 'CCOLA', 'grup'),
                 ('GARAN', 'AKBNK', 'dis'), ('YKBNK', 'AKBNK', 'dis'), ('ISCTR', 'AKBNK', 'dis'), ('ISCTR', 'GARAN', 'dis'), ('VAKBN', 'HALKB', 'dis'), ('THYAO', 'PGSUS', 'dis'), ('EREGL', 'KRDMD', 'dis'),
                 ('MGROS', 'SOKM', 'dis'), ('BIMAS', 'MGROS', 'dis'), ('KCHOL', 'SAHOL', 'dis'), ('CIMSA', 'OYAKC', 'dis'), ('TCELL', 'TTKOM', 'dis'), ('FROTO', 'DOAS', 'dis'), ('TUPRS', 'PETKM', 'dis'), ('SAHOL', 'GARAN', 'dis'), ('SAHOL', 'YKBNK', 'dis'), ('KCHOL', 'AKBNK', 'dis'), ('DOHOL', 'AKBNK', 'dis'), ('SAHOL', 'XBANK', 'dis')]:
    for win, thr in [(20, 1.5), (40, 1.5), (60, 1.0), (60, 1.5), (60, 2.0), (120, 1.5)]:
        st = ratio_bt(a, bb, win, thr)
        rows.append(dict(a=a, b=bb, g=g, win=win, thr=thr, mIS=st['IS'].get('mean_bps'), tIS=st['IS'].get('t'), mOOS=st['OOS'].get('mean_bps'), tOOS=st['OOS'].get('t'), shOOS=st['OOS'].get('sharpe'), yrs=st['yrs_pos']))
D = pd.DataFrame(rows); D.to_csv(HERE + '/res_ratio_robust.csv', index=False)
pd.set_option('display.width', 220); pd.set_option('display.max_rows', 300)
P = D[(D.win == 60) & (D.thr == 1.5)]
print(P.round(2).to_string())
print(D[D.a.isin(['SAHOL']) & D.b.isin(['AKBNK'])].round(2).to_string())
print('ortalama tOOS (60,1.5): grup', round(P[P.g == 'grup'].tOOS.mean(), 2), ' dis', round(P[P.g == 'dis'].tOOS.mean(), 2))
