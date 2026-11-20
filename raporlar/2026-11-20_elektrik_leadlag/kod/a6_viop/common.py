"""a6_viop ortak yardımcılar. Yalnız t ve öncesini kullanan seriler üretir (shift/rolling)."""
import os, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'ortak'))
import elib  # noqa: E402

TRIO = ['AKSEN', 'ENJSA', 'ODAS']


def front_wide(P, col, unds=None):
    """viop_front'tan tarih×dayanak geniş matris (spot takvimine oturtulmuş)."""
    vf = P['viop_front']
    if unds is not None:
        vf = vf[vf['und'].isin(unds)]
    W = vf.assign(date=pd.to_datetime(vf['date'])).pivot_table(index='date', columns='und', values=col, aggfunc='last')
    W.columns = [str(c) for c in W.columns]
    return W.reindex(P['ret_cc'].index)


def ca_mask(P, cols):
    """Kurumsal işlem / temettü günü (t) bayrağı: baz değişimi o gün anlamsız."""
    px = P['px']
    x = px[px['ca'].notna() & (px['ca'].astype(str) != '') & px['sym'].isin(cols)]
    M = pd.DataFrame(False, index=P['ret_cc'].index, columns=cols)
    for d, s in zip(pd.to_datetime(x['date']), x['sym']):
        if d in M.index:
            M.loc[d, s] = True
    return M


def dbaz(P, kind='settle'):
    """Δbaz(t) = ln(1+vadeli getirisi(t)) − ln(1+spot r_cc(t)); aynı kontrat, düzeltilmiş spot. Sütunlar: TRIO'dan panelde olanlar + XU030."""
    col = 'ret_settle' if kind == 'settle' else 'ret_last'
    cols = [c for c in TRIO if c in P['ret_cc'].columns]
    F = front_wide(P, col, cols + ['XU030'])
    out = pd.DataFrame(index=P['ret_cc'].index)
    cm = ca_mask(P, cols)
    for c in cols:
        if c in F.columns:
            d = np.log1p(F[c]) - np.log1p(P['ret_cc'][c])
            out[c] = d.where(~cm[c])
        else:
            out[c] = np.nan
    if 'XU030' in F.columns:
        out['XU030'] = np.log1p(F['XU030']) - np.log1p(P['idx_ret']['XU030'].reindex(out.index))
    else:
        out['XU030'] = np.nan
    return out


def zlag(x, win, minp):
    """x(t) / (t−1'e kadarki win günlük std)."""
    return x / x.shift(1).rolling(win, min_periods=minp).std()


def spike(x, k=3.0, win=20, minp=15):
    """x(t) > k × (t−1'e kadarki win günlük medyan)."""
    med = x.shift(1).rolling(win, min_periods=minp).median()
    return (x > k * med) & (med > 0)


def bcast(flag, cols, P):
    """Zaman serisi bayrağını (Series) hisse sütunlarına yay."""
    idx = P['ret_cc'].index
    f = flag.reindex(idx).fillna(False).astype(bool)
    return pd.DataFrame({c: f for c in cols}, index=idx)
