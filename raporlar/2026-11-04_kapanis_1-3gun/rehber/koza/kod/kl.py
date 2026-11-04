"""Rehber (koza) ortak yardımcıları.
- VİOP paneli = ortak panel (2017-03 → 2026-10-30) + 02–03.11.2026 bültenleri (dl_k_sahol_a/viop_new.parquet). Ortak dosyalar değiştirilmez;
  birleşik panel curlib'in önbelleğine (_C) enjekte edilir, böylece Fut/choose/fwd mantığı araştırmayla birebir aynı kalır.
- Spot: taze Yahoo günlüğü (dl_rehber_koza/daily), curlib.spot_ret ile aynı temizlik (bayat gün v<=0 ya da h==l -> NaN, limit üstü NaN).
  Bugünün tamamlanmamış barı (TSİ 18:15 öncesi) atılır."""
import sys, os, datetime as dt
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_k_yurtici-takvim_curut')
import curlib as C
import numpy as np, pandas as pd
S = C.S
DL = S + '/dl_rehber_koza'
OUT = S + '/out/rehber/koza'


def now_tsi():
    return pd.Timestamp.now(tz='Europe/Istanbul')


def ext_panel():
    """Ortak panel + yeni bültenler; curlib _panel ile aynı filtreler."""
    p = DL + '/viop_panel_ext.parquet'
    if not os.path.exists(p):
        cols = ['date', 'code', 'und', 'segment', 'ctype', 'expiry', 'settle', 'prev_settle', 'close', 'vwap', 'trades', 'value_tl', 'oi']
        A = pd.read_parquet(S + '/data/viop_panel.parquet', columns=cols)
        B = pd.read_parquet(S + '/dl_k_sahol_a/viop_new.parquet', columns=cols)
        for c in ['code', 'und', 'segment', 'ctype']:
            A[c] = A[c].astype(str); B[c] = B[c].astype(str)
        A['date'] = pd.to_datetime(A.date); B['date'] = pd.to_datetime(B.date)
        B = B[B.date > A.date.max()]
        F = pd.concat([A, B], ignore_index=True)
        F['expiry'] = pd.to_datetime(F.expiry)
        F.to_parquet(p, index=False)
    return pd.read_parquet(p)


def use_ext_panel():
    """curlib'i birleşik panelle çalıştır (Fut önbelleği sıfırlanır)."""
    F = ext_panel()
    C._C.clear(); C._FUT.clear()
    C._C['vcal'] = pd.DatetimeIndex(np.sort(pd.to_datetime(F['date']).unique()))
    for c in ['code', 'und', 'segment', 'ctype']: F[c] = F[c].astype(str)
    F = F[(F.segment == 'SSF') | ((F.und == 'XU030') & (F.ctype == 'D_IX_FUT'))]
    F = F[(F.expiry >= F.date) & (F.settle > 0)]
    F['trades'] = F.trades.fillna(0)
    F = F.sort_values(['und', 'expiry', 'date', 'trades']).drop_duplicates(['und', 'expiry', 'date'], keep='last')
    C._C['panel'] = F
    return C.vcal()


def spot_fresh(sym):
    d = pd.read_parquet(f'{DL}/daily/{sym}.IS.parquet'); d.index = pd.DatetimeIndex(d.ldate); d = d[~d.index.duplicated(keep='last')]
    nt = now_tsi(); today = pd.Timestamp(nt.date())
    if nt.hour * 60 + nt.minute < 18 * 60 + 15:
        d = d[d.index < today]
    if not sym.startswith('XU'):
        st = (d.v <= 0) | (d.h == d.l)
        d.loc[st, ['o', 'h', 'l', 'c', 'adj']] = np.nan
    return d


def spot_ret_fresh(sym):
    a = spot_fresh(sym)['adj']
    r = np.log(a / a.ffill().shift(1)).where(a.notna())
    pre = r.index < C.REG
    up = np.where(pre, np.log(1.205), np.log(1.105)); dn = np.where(pre, np.log(0.795), np.log(0.895))
    if not sym.startswith('XU'):
        r = r.mask((r > up) | (r < dn))
    return r


def beta(y, x, w=250, mp=120):
    return (y.rolling(w, min_periods=mp).cov(x) / x.rolling(w, min_periods=mp).var()).shift(1)


def zk(u, k, sdw=60):
    return u.rolling(k, min_periods=k).sum() / (u.rolling(sdw, min_periods=40).std() * np.sqrt(k))


def koza_signal(r, target='TRMET'):
    """r: TRMET, TRALT, TRENJ, XU030 spot log getirileri (DataFrame). target='TRMET' ana kural, 'TRALT' ters kural."""
    r = r[['TRMET', 'TRALT', 'TRENJ', 'XU030']].dropna(how='all')
    if target == 'TRMET':
        y, hedge, other = r.TRMET, r.TRALT, r.TRENJ
    else:
        y, hedge, other = r.TRALT, r.TRMET, r.TRENJ
    grp = pd.concat([hedge, other], axis=1).mean(axis=1, skipna=False)
    b_g = beta(y, grp).clip(0.2, 2.0)
    u = y - b_g * grp
    bH = beta(y, hedge).clip(0.3, 2.0)
    sd60 = u.rolling(60, min_periods=40).std()
    z3 = zk(u, 3)
    return pd.DataFrame({'u': u, 'grp': grp, 'b_g': b_g, 'bH': bH, 'sd60': sd60, 'z3': z3})


def lock_series(und, cal):
    """Sinyal günü ön vade uzlaşma getirisinin ±%9,5'i aşması (limit kilidi vekili) — c2 ile aynı."""
    F = C.fut(und); fs, jj = F.front_series('settle', min_dte=0)
    r = pd.Series(np.nan, index=cal); ok = jj.values >= 0
    r[ok] = F.R.values[np.arange(len(cal))[ok], jj.values[ok]]
    return r.abs() > np.log(1.095)
