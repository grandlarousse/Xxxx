"""Saatlik öncülük işlenebilir mi? lider artığı_{h-1} (XU100'e göre) -> takipçi h barı. Pozisyon bar başında, bar sonunda kapanır. Maliyet 8 bps/işlem (tek bacak)."""
from gx import *
import importlib.util
spec = importlib.util.spec_from_file_location('h5', HERE + '/05_hourly.py'); h5 = importlib.util.module_from_spec(spec); spec.loader.exec_module(h5)
rows = []
for x, y in [('AEFES', 'AGHOL'), ('KRDMA', 'KRDMB'), ('TUPRS', 'AYGAZ'), ('TUPRS', 'KCHOL'), ('EREGL', 'ISDMR'), ('VESBE', 'ZOREN'), ('AKBNK', 'SAHOL'), ('ALCAR', 'ALARK'), ('AKBNK', 'GARAN')]:
    X, Y, M = h5.hb(x), h5.hb(y), h5.hb('XU100')
    df = pd.concat([Y['r'].rename('y'), X['r'].shift(1).rename('x1'), M['r'].shift(1).rename('m1'), Y['day'].rename('d'), Y['day'].shift(1).rename('d1')], axis=1)
    df = df[df.d == df.d1].dropna(); df.index = df.index.tz_convert(None)
    bx = df['x1'].rolling(500, min_periods=200).cov(df['m1']) / df['m1'].rolling(500, min_periods=200).var()
    s = df['x1'] - bx.shift(1) * df['m1']
    for thr in [1.0, 2.0]:
        res, pnl = ll.backtest(s, df['y'], cost_bps=8, mode='z', thr=thr, split='2025-05-01', z_window=500)
        r0, _ = ll.backtest(s, df['y'], cost_bps=0, mode='z', thr=thr, split='2025-05-01', z_window=500)
        rows.append(dict(x=x, y=y, thr=thr, gross_bps=r0['ALL'].get('mean_bps'), net8_bps=res['ALL'].get('mean_bps'), t_net=res['ALL'].get('t'), n=res['ALL'].get('n'), net_h2=res['OOS'].get('mean_bps')))
D = pd.DataFrame(rows); D.to_csv(HERE + '/res_hourly_bt.csv', index=False); print(D.round(2).to_string())
