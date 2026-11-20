"""elib.py — ortak değerlendirme kütüphanesi (YONTEM.md'nin uygulaması).

Kullanım:
    import sys; sys.path.insert(0, '<.../kod/ortak>')
    import elib
    P = elib.load('<.../panel_dev>')
    sig = (P['ret_cc'] > 0.05)                 # bool, date×sym: t kapanışında bilinen bilgiyle "pozisyon aç"
    row = elib.evaluate(sig, P, h=1, side='long', name='ornek', family='A4')
    # row: sonuç tablosu satırı (dict). elib.to_csv([row,...], yol)

Sözleşme:
- sig[t, i] = True  →  t günü kapanışında i hissesinde pozisyon açılır (yalnız t kapanışına kadarki bilgiyle kurulmuş olmalı).
- Getiri: giriş c(t), çıkış c(t+h). Uzun pozisyonda çıkış günü hisse tabanda kilitliyse çıkış ilk kilitsiz kapanışa kayar (en çok +5 gün).
- 'dolabilir': uzun için t günü tavanda kapanmamış, kısa için tabanda kapanmamış, tradable=True.
- Fazla getiri ölçüleri:
    own : f − hedefin kendi geçmiş 250 günlük ortalama h-günlük getirisi (ileriye bakmaz)
    sec : f − aynı gün işlem görebilir elektrik hisselerinin eşit ağırlıklı ortalama f'si
    mkt : f − β·f_XU100 (β: 250 günlük, 1 gün gecikmeli)
  Karar ölçüsü varsayılan olarak 'own'; sektör zamanlaması olmayan (hisse seçimi) sinyallerde 'sec' de raporlanır.
- t-istatistiği: önce gün içi eşit ağırlıklı ortalama (tarih kümelemesi), sonra takvim serisi üzerinde HAC (gecikme h−1).
"""
import os
import numpy as np
import pandas as pd

IS_END = pd.Timestamp('2022-12-30')
OOS1_START = pd.Timestamp('2023-01-02')
OOS1_END = pd.Timestamp('2025-06-30')
KASA_START = pd.Timestamp('2025-07-01')
VIOP = ['AKSEN', 'ENJSA', 'ODAS']
XELKT = ('A1YEN AHGAZ AKENR AKFYE AKSEN AKSUE ALFAS ARFYE AYDEM AYEN BESTE BIOEN BIGEN CONSE CWENE CANTE CATES '
         'ARASE ECOGR ENDAE ENJSA ENERY ESEN GWIND HUNER ENTRA IZENR KLYPV LYDYE MAGEN MASFN METEN MOGAN NTGAZ '
         'NATEN ODAS PAMEL SMRTG TATEN VEYAS ZEDUR ZOREN').split()
KOMSU = ['ASTOR', 'ALARK', 'EUPWR', 'GESAN']

# gidiş-dönüş maliyet (bps). 'spot' değerine ayrıca yarım fiyat adımı eklenir (tick_bps/2).
COST = {
    'dusuk': {'spot': 10, 'AKSEN': 8, 'ENJSA': 10, 'ODAS': 25},
    'temel': {'spot': 25, 'AKSEN': 15, 'ENJSA': 18, 'ODAS': 35},
    'muhafazakar': {'spot': 50, 'AKSEN': 25, 'ENJSA': 25, 'ODAS': 45},
}

# BIST Pay Piyasası fiyat adımı tablosu (üst sınır, adım). 1. dalga doğrulamasına göre güncellenir.
TICK_TABLE = [(20, 0.01), (50, 0.02), (100, 0.05), (250, 0.10), (500, 0.25), (1000, 0.50), (2500, 1.0), (1e12, 2.5)]


def tick_of(price):
    p = np.asarray(price, dtype=float)
    out = np.full(p.shape, np.nan)
    lo = 0.0
    for hi, t in TICK_TABLE:
        out[(p >= lo) & (p < hi)] = t
        lo = hi
    return out


def load(panel_dir):
    """panel klasöründeki bütün geniş matrisleri sözlük olarak yükler."""
    P = {}
    names = ['ret_cc', 'ret_co', 'ret_oc', 'vol_tl', 'close_raw', 'lim_up', 'lim_dn', 'lim_up_touch', 'lim_dn_touch',
             'zero_vol', 'ipo_n', 'ca_day', 'tradable', 'idx', 'idx_ret', 'idx_open']
    for n in names:
        p = os.path.join(panel_dir, n + '.parquet')
        if os.path.exists(p):
            df = pd.read_parquet(p)
            df.index = pd.to_datetime(df.index)
            P[n] = df.sort_index()
    mp = os.path.join(panel_dir, 'meta.csv')
    if os.path.exists(mp):
        P['meta'] = pd.read_csv(mp)
    for n in ['viop_daily', 'viop_front', 'snap', 'px']:
        p = os.path.join(panel_dir, n + '.parquet')
        if os.path.exists(p):
            P[n] = pd.read_parquet(p)
    for n in ['lim_up', 'lim_dn', 'lim_up_touch', 'lim_dn_touch', 'zero_vol', 'ca_day', 'tradable']:
        if n in P:
            P[n] = P[n].reindex_like(P['ret_cc']).fillna(False).astype(bool)
    P['dir'] = panel_dir
    return P


def sector_cols(P, extra=False):
    cols = [c for c in XELKT if c in P['ret_cc'].columns]
    if extra:
        cols += [c for c in KOMSU if c in P['ret_cc'].columns]
    return cols


def level(ret):
    """Getiriden düzey serisi (ilk geçerli gözlemden önce NaN)."""
    L = (1 + ret.fillna(0)).cumprod()
    first = ret.notna().cumsum() > 0
    # ilk geçerli getiriden bir önceki günü de 1 kabul etmek için: maske ilk geçerli günden itibaren
    return L.where(first | first.shift(-1, fill_value=False))


def fwd_simple(ret, h):
    """f_h(t) = c(t+h)/c(t) − 1 (kilit kaydırması yok)."""
    L = level(ret)
    return L.shift(-h) / L - 1


def fwd_exec(P, h, side='long', cols=None, max_delay=5):
    """Dolum kurallı ileri getiri. Dönen: (f, fillable, delayed)
    f[t,i]: t kapanışında giriş, t+h kapanışında çıkış; çıkış günü kilitliyse ilk kilitsiz kapanışa kayar.
    side='short' için getiri işareti çevrilmiş verilir (kısa pozisyonun kazancı)."""
    ret = P['ret_cc'] if cols is None else P['ret_cc'][cols]
    cols = list(ret.columns)
    L = level(ret)
    lock_exit = (P['lim_dn'] if side == 'long' else P['lim_up'])[cols]
    lock_entry = (P['lim_up'] if side == 'long' else P['lim_dn'])[cols]
    Lv = L.values
    lk = lock_exit.values
    n, m = Lv.shape
    exit_idx = np.minimum(np.arange(n)[:, None] + h, n - 1) * np.ones((1, m), dtype=int)
    valid = (np.arange(n)[:, None] + h <= n - 1) * np.ones((1, m), dtype=bool)
    delayed = np.zeros((n, m), dtype=bool)
    for d in range(max_delay):
        e = exit_idx
        locked = np.take_along_axis(lk, e, axis=0) & valid
        nxt = np.minimum(e + 1, n - 1)
        can = locked & (e + 1 <= n - 1)
        exit_idx = np.where(can, nxt, e)
        delayed |= can
        valid &= ~(locked & ~can)
    Lexit = np.take_along_axis(Lv, exit_idx, axis=0)
    f = Lexit / Lv - 1
    f[~valid] = np.nan
    f = pd.DataFrame(f, index=ret.index, columns=cols)
    if side == 'short':
        f = -f
    trad = P['tradable'][cols] if 'tradable' in P else ret.notna()
    fillable = trad & ~lock_entry & ret.notna()
    return f, fillable, pd.DataFrame(delayed, index=ret.index, columns=cols)


def bench_own(f, h, win=250, minp=120):
    """Hedefin kendi geçmiş ortalama h-günlük getirisi; t anında yalnız çıkışı t'den önce bitmiş gözlemler kullanılır."""
    return f.shift(h).rolling(win, min_periods=minp).mean()


def beta_lagged(ret, mkt, win=250, minp=120):
    cov = ret.rolling(win, min_periods=minp).cov(mkt)
    var = mkt.rolling(win, min_periods=minp).var()
    return cov.div(var, axis=0).shift(1)


def excess_measures(P, h, side='long', cols=None):
    """Ham ve üç fazla getiri ölçüsünü döndürür: dict(raw, own, sec, mkt), fillable."""
    f, fillable, delayed = fwd_exec(P, h, side, cols)
    cols = list(f.columns)
    sgn = 1.0 if side == 'long' else -1.0
    f_long = f * sgn                      # uzun yönlü ham getiri
    own = f_long - bench_own(f_long, h)
    sec_cols = [c for c in sector_cols(P) if c in P['ret_cc'].columns]
    f_sec, _, _ = fwd_exec(P, h, 'long', sec_cols)
    trad = P['tradable'][sec_cols] if 'tradable' in P else f_sec.notna()
    sec_mean = f_sec.where(trad).mean(axis=1)
    sec = f_long.sub(sec_mean, axis=0)
    mk = P['idx_ret']['XU100'].reindex(f.index)
    f_mkt = fwd_simple(mk.to_frame('m'), h)['m']
    beta = beta_lagged(P['ret_cc'][cols], mk)
    mkt = f_long - beta.mul(f_mkt, axis=0)
    out = {'raw': f, 'own': own * sgn, 'sec': sec * sgn, 'mkt': mkt * sgn}
    return out, fillable


def _hac_mean(x, d, lag):
    """x: takvim serisi (sinyal olmayan gün 0), d: sinyal göstergesi. Ortalama ve HAC t (Bartlett, gecikme=lag)."""
    nd = d.sum()
    if nd < 3:
        return np.nan, np.nan
    mu = x.sum() / nd
    u = (x - mu * d)
    s = (u * u).sum()
    for k in range(1, lag + 1):
        w = 1 - k / (lag + 1)
        s += 2 * w * (u[k:] * u[:-k]).sum()
    se = np.sqrt(max(s, 1e-30)) / nd
    return mu, mu / se


def day_series(sig, F, fillable=None):
    """Sinyal günlerinde eşit ağırlıklı günlük portföy getirisi. Dönen: (p_t Series [sinyal olmayan günler NaN], işlem sayısı Series)."""
    S = sig.reindex_like(F).fillna(False).astype(bool)
    if fillable is not None:
        S = S & fillable.reindex_like(F).fillna(False)
    X = F.where(S)
    return X.mean(axis=1), X.notna().sum(axis=1), X


def stats_block(p, ntr, X, h, start=None, end=None):
    if start is not None:
        p = p[p.index >= start]; ntr = ntr[ntr.index >= start]; X = X[X.index >= start]
    if end is not None:
        p = p[p.index <= end]; ntr = ntr[ntr.index <= end]; X = X[X.index <= end]
    d = p.notna().values.astype(float)
    x = p.fillna(0).values
    mu, t = _hac_mean(x, d, max(h - 1, 0))
    vals = X.values[np.isfinite(X.values)]
    return {
        'n_gun': int(d.sum()), 'n_islem': int(ntr.sum()),
        'ort_gun_bps': 1e4 * mu if mu == mu else np.nan, 't': t,
        'ort_islem_bps': 1e4 * vals.mean() if len(vals) else np.nan,
        'medyan_islem_bps': 1e4 * np.median(vals) if len(vals) else np.nan,
        'isabet': float((vals > 0).mean()) if len(vals) else np.nan,
    }


def cost_bps(P, sig, target='spot', senaryo='temel'):
    """İşlem başına ortalama gidiş-dönüş maliyet (bps). Spot: komisyon + yarım fiyat adımı (sinyal günü ham fiyatına göre)."""
    c = COST[senaryo]
    if target in VIOP and target != 'spot':
        return float(c[target])
    cr = P['close_raw'].reindex_like(sig)
    tick = pd.DataFrame(tick_of(cr.values), index=cr.index, columns=cr.columns)
    tb = (1e4 * tick / cr).where(sig.fillna(False).astype(bool))
    v = tb.values[np.isfinite(tb.values)]
    return float(c['spot'] + 0.5 * (v.mean() if len(v) else 0.0))


def evaluate(sig, P, h=1, side='long', name='', family='', measure='own', instrument='spot', extra=None):
    """Bir sinyal matrisi için sonuç tablosu satırı üretir.
    sig: bool DataFrame (date×sym). instrument: 'spot' ya da 'viop' (yalnız AKSEN/ENJSA/ODAS sütunları; maliyet kontrata göre).
    measure: karar ölçüsü ('own' | 'sec' | 'mkt')."""
    cols = [c for c in sig.columns if c in P['ret_cc'].columns]
    sig = sig[cols].reindex(P['ret_cc'].index).fillna(False).astype(bool)
    M, fillable = excess_measures(P, h, side, cols)
    row = {'aile': family, 'sinyal_tanimi': name, 'hedef': ','.join(cols) if len(cols) <= 4 else f'{len(cols)} hisse',
           'yon': side, 'h': h, 'arac': instrument, 'karar_olcusu': measure}
    # maliyet
    if instrument == 'viop':
        cs = {s: np.mean([COST[s][c] for c in cols if c in VIOP]) for s in COST}
    else:
        cs = {s: cost_bps(P, sig & fillable, 'spot', s) for s in COST}
    last = P['ret_cc'].index.max()
    periods = {'IS': (None, IS_END), 'OOS1': (OOS1_START, OOS1_END)}
    if last >= KASA_START:
        periods['KASA'] = (KASA_START, None)
    for fill_name, fl in [('hepsi', None), ('dol', fillable)]:
        for mname in ['raw', measure] + [m for m in ['own', 'sec', 'mkt'] if m != measure]:
            p, ntr, X = day_series(sig, M[mname], fl)
            for per, (a, b) in periods.items():
                st = stats_block(p, ntr, X, h, a, b)
                if fill_name == 'dol' and mname == measure:
                    row[f'n_gun_{per}'] = st['n_gun']; row[f'n_islem_{per}'] = st['n_islem']
                    row[f'ort_fazla_{per}_bps'] = st['ort_gun_bps']; row[f't_{per}'] = st['t']
                    row[f'ort_islem_fazla_{per}_bps'] = st['ort_islem_bps']; row[f'isabet_{per}'] = st['isabet']
                    for s in COST:
                        row[f'net_{s}_bps_{per}'] = st['ort_islem_bps'] - cs[s] if st['ort_islem_bps'] == st['ort_islem_bps'] else np.nan
                else:
                    row[f'{fill_name}_{mname}_{per}_bps'] = st['ort_gun_bps']; row[f'{fill_name}_{mname}_{per}_t'] = st['t']
                    if fill_name == 'hepsi' and mname == measure:
                        row[f'n_islem_hepsi_{per}'] = st['n_islem']
    # dolabilir oran, yıllar, en iyi 10 hariç (IS+OOS1 birlikte; KASA hariç)
    p, ntr, X = day_series(sig, M[measure], fillable)
    p_all, ntr_all, _ = day_series(sig, M[measure], None)
    dev = p[p.index <= OOS1_END]
    row['dolabilir_oran'] = float(ntr[ntr.index <= OOS1_END].sum() / max(ntr_all[ntr_all.index <= OOS1_END].sum(), 1))
    yr = dev.dropna().groupby(dev.dropna().index.year)
    ym = yr.mean()[yr.count() >= 5]
    row['yil_sayisi'] = int(len(ym)); row['yil_pozitif_orani'] = float((ym > 0).mean()) if len(ym) else np.nan
    row['yillar_bps'] = ';'.join(f'{y}:{1e4 * v:.0f}' for y, v in ym.items())
    dv = dev.dropna().sort_values()
    k = max(10, int(np.ceil(0.05 * len(dv))))
    row['top10_haric_bps'] = 1e4 * dv.iloc[:-k].mean() if len(dv) > k + 5 else np.nan
    row['maliyet_temel_bps'] = cs['temel']
    # hisse yoğunlaşması: en çok işlem yapılan hissenin payı
    Xd = X[X.index <= OOS1_END]
    cnt = Xd.notna().sum()
    row['en_yogun_hisse'] = cnt.idxmax() if cnt.sum() else ''
    row['en_yogun_pay'] = float(cnt.max() / max(cnt.sum(), 1))
    if extra:
        row.update(extra)
    return row


def bh_fdr(pvals, q=0.10):
    p = np.asarray(pvals, dtype=float)
    ok = np.isfinite(p)
    out = np.zeros(len(p), dtype=bool)
    idx = np.where(ok)[0]
    if len(idx) == 0:
        return out
    order = idx[np.argsort(p[idx])]
    m = len(idx)
    thr = q * (np.arange(1, m + 1)) / m
    passed = p[order] <= thr
    if passed.any():
        kmax = np.where(passed)[0].max()
        out[order[:kmax + 1]] = True
    return out


def t_to_p(t):
    from math import erf, sqrt
    t = np.abs(np.asarray(t, dtype=float))
    return 2 * (1 - 0.5 * (1 + np.vectorize(erf)(t / sqrt(2))))


def shift_null(sig, P, h=1, side='long', measure='own', n=300, min_shift=30, seed=0, end=IS_END, start=None):
    """Yer değiştirme (dairesel kaydırma) sıfır dağılımı: sinyal matrisi zamanda rastgele kaydırılır.
    Dönen: (gerçek ortalama bps, p-değeri [tek yönlü, gerçek ≥], sıfır dağılımı)."""
    cols = [c for c in sig.columns if c in P['ret_cc'].columns]
    M, fillable = excess_measures(P, h, side, cols)
    F = M[measure]
    if end is not None:
        F = F[F.index <= end]
    if start is not None:
        F = F[F.index >= start]
    S = sig[cols].reindex(F.index).fillna(False).astype(bool)
    fl = fillable.reindex(F.index).fillna(False)

    def stat(Sx):
        X = F.where(Sx & fl)
        pm = X.mean(axis=1).dropna()
        return 1e4 * pm.mean() if len(pm) else np.nan
    real = stat(S)
    rng = np.random.default_rng(seed)
    T = len(F)
    null = []
    for _ in range(n):
        k = int(rng.integers(min_shift, T - min_shift))
        Sx = pd.DataFrame(np.roll(S.values, k, axis=0), index=S.index, columns=S.columns)
        null.append(stat(Sx))
    null = np.array(null)
    pval = float((np.sum(null >= real) + 1) / (np.sum(np.isfinite(null)) + 1))
    return real, pval, null


def fama_macbeth(y, xs, min_n=8, lag=0):
    """Günlük kesit regresyonu: y[t,i] ~ a_t + Σ b_k,t x_k[t,i]. Dönen: DataFrame(ortalama katsayı, t, n_gun).
    y, xs: date×sym DataFrame'ler (xs: dict ad→DataFrame). Kesit sayısı min_n'den azsa gün atlanır."""
    names = list(xs.keys())
    rows = []
    for dt in y.index:
        yy = y.loc[dt]
        XX = pd.concat([xs[k].loc[dt] for k in names], axis=1, keys=names)
        ok = yy.notna() & XX.notna().all(axis=1)
        if ok.sum() < max(min_n, len(names) + 3):
            continue
        A = np.column_stack([np.ones(ok.sum()), XX[ok].values])
        try:
            b = np.linalg.lstsq(A, yy[ok].values, rcond=None)[0]
        except Exception:
            continue
        rows.append([dt] + list(b[1:]))
    B = pd.DataFrame(rows, columns=['date'] + names).set_index('date')
    out = {}
    for k in names:
        x = B[k].values
        d = np.ones(len(x))
        mu, t = _hac_mean(x, d, lag)
        out[k] = {'katsayi': mu, 't': t, 'n_gun': len(x)}
    return pd.DataFrame(out).T, B


def ts_reg(y, X, lag=0):
    """Zaman serisi OLS + Newey–West. y: Series, X: DataFrame. Dönen: DataFrame(katsayı, t)."""
    import statsmodels.api as sm
    df = pd.concat([y.rename('y'), X], axis=1).dropna()
    if len(df) < X.shape[1] + 20:
        return None
    m = sm.OLS(df['y'], sm.add_constant(df.drop(columns='y'))).fit(cov_type='HAC', cov_kwds={'maxlags': max(lag, 1)})
    return pd.DataFrame({'katsayi': m.params, 't': m.tvalues, 'n': len(df)})


def to_csv(rows, path):
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return df
