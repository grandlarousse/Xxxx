"""elib.py — ortak değerlendirme kütüphanesi (YONTEM.md + ek/YONTEM_EK.md'nin uygulaması).

Kullanım:
    import sys; sys.path.insert(0, '<.../kod/ortak>')
    import elib
    P = elib.load('<.../panel_is>')
    sig = (P['ret_cc'] > 0.05)                 # bool, tarih×hisse: t kapanışında bilinen bilgiyle "pozisyon aç"
    row = elib.evaluate(sig, P, h=1, side='long', measure='own', name='ornek', family='A4')
    elib.to_csv([row, ...], yol)

Sözleşme:
- sig[t, i] = True  →  t günü kapanışında i hissesinde pozisyon açılır (yalnız t kapanışına kadarki bilgiyle kurulmuş olmalı).
- Getiri: giriş c(t), çıkış c(t+h). Uzun pozisyonda çıkış günü hisse tabanda kilitliyse çıkış ilk kilitsiz kapanışa kayar (en çok +5 gün).
- 'dolabilir' (P['fill_long'] / P['fill_short']): tradable ve t günü tavanda (kısa için tabanda) kapanmamış.
  tradable = veri var & hacim > 0 & halka arzdan beri > 20 gün & ilk tavansız kapanış görülmüş.
- Fazla getiri ölçüleri (karar ölçüsü kural türüne göre önceden bellidir):
    own : f − hedefin t'den önce tamamlanmış son 250 günlük ortalama f_h'i          → zamanlama kuralları
    sec : f − aynı gün, hedef hariç, DOLABİLİR sektör üyelerinin eşit ağırlıklı f_h'i → kesit (hisse seçimi) kuralları
    mkt : f − β·f_XU100 (β: 250 günlük, 1 gün gecikmeli; en az 60 gün, yoksa 1)       → bilgi
- t-istatistiği: önce gün içi eşit ağırlıklı ortalama (tarih kümelemesi), sonra takvim serisinde HAC (gecikme h−1).
- Giriş gecikmesi sınaması: 'acilis1' (t+1 açılışından giriş), 'kapanis1' (t+1 kapanışından giriş), gece payı.
"""
import os
import numpy as np
import pandas as pd

IS_END = pd.Timestamp('2022-12-30')
OOS1_START = pd.Timestamp('2023-01-02')
OOS1_END = pd.Timestamp('2025-06-30')
KASA_START = pd.Timestamp('2025-07-01')
VIOP = ['AKSEN', 'ENJSA', 'ODAS']
VIOP_START = {'ENJSA': '2018-12-14', 'ODAS': '2021-04-22', 'AKSEN': '2022-11-01'}
XELKT = ('A1YEN AHGAZ AKENR AKFYE AKSEN AKSUE ALFAS ARFYE AYDEM AYEN BESTE BIOEN BIGEN CONSE CWENE CANTE CATES '
         'ARASE ECOGR ENDAE ENJSA ENERY ESEN GWIND HUNER ENTRA IZENR KLYPV LYDYE MAGEN MASFN METEN MOGAN NTGAZ '
         'NATEN ODAS PAMEL SMRTG TATEN VEYAS ZEDUR ZOREN').split()
KOMSU = ['ASTOR', 'ALARK', 'EUPWR', 'GESAN']
BIG = ['ENJSA', 'AKSEN', 'ZOREN', 'AYDEM', 'AHGAZ']

# gidiş-dönüş maliyet (bps). 'spot' değerine ayrıca yarım fiyat adımı eklenir.
COST = {
    'dusuk': {'spot': 10, 'AKSEN': 8, 'ENJSA': 10, 'ODAS': 25},
    'temel': {'spot': 25, 'AKSEN': 15, 'ENJSA': 18, 'ODAS': 35},
    'muhafazakar': {'spot': 50, 'AKSEN': 25, 'ENJSA': 25, 'ODAS': 45},
}
# BIST Pay Piyasası fiyat adımı tablosu (Pay Piyasası Prosedürü rev. 54, Tablo-7): (üst sınır, adım)
TICK_TABLE = [(20, 0.01), (50, 0.02), (100, 0.05), (250, 0.10), (500, 0.25), (1000, 0.50), (2500, 1.0), (1e12, 2.5)]
# Pay vadelisi fiyat adımı (VİOP Prosedürü rev. 70)
TICK_TABLE_FUT = [(100, 0.01), (500, 0.05), (1000, 0.10), (2500, 0.25), (1e12, 0.50)]


def tick_of(price, table=None):
    p = np.asarray(price, dtype=float)
    out = np.full(p.shape, np.nan)
    lo = 0.0
    for hi, t in (table or TICK_TABLE):
        out[(p >= lo) & (p < hi)] = t
        lo = hi
    return out


def load(panel_dir):
    """Panel klasöründeki matrisleri sözlük olarak yükler; tradable ve dolum maskelerini YONTEM_EK E4'e göre kurar."""
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
    R = P['ret_cc']
    for n in ['lim_up', 'lim_dn', 'lim_up_touch', 'lim_dn_touch', 'zero_vol', 'ca_day', 'tradable']:
        if n in P:
            P[n] = P[n].reindex_like(R).fillna(False).astype(bool)
    if 'tradable' not in P:
        P['tradable'] = R.notna()
    lu = P.get('lim_up', pd.DataFrame(False, index=R.index, columns=R.columns))
    ld = P.get('lim_dn', pd.DataFrame(False, index=R.index, columns=R.columns))
    P['lim_up'], P['lim_dn'] = lu, ld
    trad = P['tradable'] & R.notna()
    if 'ipo_n' in P:
        trad &= (P['ipo_n'].reindex_like(R) > 20).fillna(False)
    first_free = ((~lu) & R.notna()).cumsum() > 0          # ilk tavansız kapanış görüldü mü
    trad &= first_free
    P['tradable'] = trad
    P['fill_long'] = trad & ~lu
    P['fill_short'] = trad & ~ld
    P['dir'] = panel_dir
    P['_cache'] = {}
    return P


def sector_cols(P, extra=False):
    cols = [c for c in XELKT if c in P['ret_cc'].columns]
    if extra:
        cols += [c for c in KOMSU if c in P['ret_cc'].columns]
    return cols


def adv60(P, win=60, minp=20):
    """t−1'e kadarki 60 günlük medyan TL hacim (büyüklük/likidite sıralaması için; geleceği içermez)."""
    return P['vol_tl'].rolling(win, min_periods=minp).median().shift(1)


def ew_basket(P, cols=None, ex=None, fillable_only=True, min_n=3):
    """t günü eşit ağırlıklı sektör getirisi (GİRDİ olarak): tradable üyelerin r_cc ortalaması. ex: hariç tutulacak hisse(ler)."""
    cols = cols or sector_cols(P)
    if ex is not None:
        ex = [ex] if isinstance(ex, str) else list(ex)
        cols = [c for c in cols if c not in ex]
    X = P['ret_cc'][cols].where(P['tradable'][cols]) if fillable_only else P['ret_cc'][cols]
    m = X.mean(axis=1)
    return m.where(X.notna().sum(axis=1) >= min_n)


def level(ret):
    """Getiriden düzey serisi (ilk geçerli gözlemden önce NaN)."""
    L = (1 + ret.fillna(0)).cumprod()
    first = ret.notna().cumsum() > 0
    return L.where(first | first.shift(-1, fill_value=False))


def fwd_simple(ret, h):
    """f_h(t) = c(t+h)/c(t) − 1 (kilit kaydırması yok)."""
    L = level(ret)
    return L.shift(-h) / L - 1


def fwd_exec(P, h, side='long', cols=None, max_delay=5):
    """Dolum kurallı ileri getiri (uzun yönlü ham getiri olarak). Dönen: (f, fillable, delayed)
    Uzun: çıkış günü tabanda kilitliyse çıkış ilk kilitsiz kapanışa kayar. Kısa: tavanda kilitliyse kayar."""
    ret = P['ret_cc'] if cols is None else P['ret_cc'][cols]
    cols = list(ret.columns)
    L = level(ret)
    lock_exit = (P['lim_dn'] if side == 'long' else P['lim_up'])[cols]
    Lv = L.values
    lk = lock_exit.values
    n, m = Lv.shape
    exit_idx = np.minimum(np.arange(n)[:, None] + h, n - 1) * np.ones((1, m), dtype=int)
    valid = (np.arange(n)[:, None] + h <= n - 1) * np.ones((1, m), dtype=bool)
    delayed = np.zeros((n, m), dtype=bool)
    for _ in range(max_delay):
        e = exit_idx
        locked = np.take_along_axis(lk, e, axis=0) & valid
        can = locked & (e + 1 <= n - 1)
        exit_idx = np.where(can, np.minimum(e + 1, n - 1), e)
        delayed |= can
        valid &= ~(locked & ~can)
    f = np.take_along_axis(Lv, exit_idx, axis=0) / Lv - 1
    f[~valid] = np.nan
    f = pd.DataFrame(f, index=ret.index, columns=cols)
    fillable = (P['fill_long'] if side == 'long' else P['fill_short'])[cols]
    return f, fillable, pd.DataFrame(delayed, index=ret.index, columns=cols)


def bench_own(f, h, win=250, minp=120):
    """Hedefin kendi geçmiş ortalama h-günlük getirisi; t anında yalnız çıkışı t'den önce bitmiş gözlemler."""
    return f.shift(h).rolling(win, min_periods=minp).mean()


def beta_lagged(ret, mkt, win=250, minp=60):
    cov = ret.rolling(win, min_periods=minp).cov(mkt)
    var = mkt.rolling(win, min_periods=minp).var()
    return cov.div(var, axis=0).shift(1).fillna(1.0)


def sec_bench(P, h, min_others=4):
    """Aynı gün dolabilir sektör üyelerinin eşit ağırlıklı f_h'i için toplam ve sayı (hedef hariç tutmak üzere)."""
    key = ('secb', h)
    if key not in P['_cache']:
        sc = sector_cols(P)
        f, fl, _ = fwd_exec(P, h, 'long', sc)
        X = f.where(fl)
        P['_cache'][key] = (X.sum(axis=1, min_count=1), X.notna().sum(axis=1), X)
    return P['_cache'][key]


def excess_measures(P, h, side='long', cols=None, entry='close'):
    """Ham ve üç fazla getiri ölçüsü (pozisyon yönünde): dict(raw, own, sec, mkt), fillable.
    entry: 'close' (t kapanışı) | 'open1' (t+1 açılışı; f = açılış(t+1) → kapanış(t+h))."""
    cols = list(P['ret_cc'].columns) if cols is None else list(cols)
    key = ('ex', h, side, tuple(cols), entry)
    if key in P['_cache']:
        return P['_cache'][key]
    f, fillable, _ = fwd_exec(P, h, side, cols)
    if entry == 'open1':
        g = P['ret_co'][cols].shift(-1)
        f = (1 + f) / (1 + g) - 1
    own = f - bench_own(f, h)
    S, N, X = sec_bench(P, h)
    if entry == 'open1':
        sc = list(X.columns)
        Xo = ((1 + X) / (1 + P['ret_co'][sc].shift(-1)) - 1)
        S, N, X = Xo.sum(axis=1, min_count=1), Xo.notna().sum(axis=1), Xo
    sec = pd.DataFrame(index=f.index, columns=cols, dtype=float)
    for c in cols:
        if c in X.columns:
            own_in = X[c].notna()
            s = S - X[c].fillna(0)
            n = N - own_in.astype(int)
        else:
            s, n = S, N
        sec[c] = f[c] - (s / n).where(n >= 4)
    mk = P['idx_ret']['XU100'].reindex(f.index)
    f_mkt = fwd_simple(mk.to_frame('m'), h)['m']
    beta = beta_lagged(P['ret_cc'][cols], mk)
    mkt = f - beta.mul(f_mkt, axis=0)
    sgn = 1.0 if side == 'long' else -1.0
    out = ({'raw': f * sgn, 'own': own * sgn, 'sec': sec * sgn, 'mkt': mkt * sgn}, fillable)
    P['_cache'][key] = out
    return out


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


def day_series(sig, F, fillable=None, min_n=1):
    """Sinyal günlerinde eşit ağırlıklı günlük portföy getirisi. Dönen: (p_t, işlem sayısı, işlem matrisi)."""
    S = sig.reindex_like(F).fillna(False).astype(bool)
    if fillable is not None:
        S = S & fillable.reindex_like(F).fillna(False)
    X = F.where(S)
    n = X.notna().sum(axis=1)
    if min_n > 1:
        X = X.where(n >= min_n, np.nan)
        n = X.notna().sum(axis=1)
    return X.mean(axis=1), n, X


def _indep(dates_idx, h):
    """Aralarında en az h işlem günü olan olay günü sayısı (açgözlü sayım). dates_idx: sıralı tamsayı konumlar."""
    c, last = 0, -10 ** 9
    for i in dates_idx:
        if i - last >= h:
            c += 1
            last = i
    return c


def stats_block(p, ntr, X, h, start=None, end=None):
    pos = np.arange(len(p))
    m = np.ones(len(p), dtype=bool)
    if start is not None:
        m &= (p.index >= start)
    if end is not None:
        m &= (p.index <= end)
    p2, X2 = p[m], X[m]
    d = p2.notna().values.astype(float)
    x = p2.fillna(0).values
    mu, t = _hac_mean(x, d, max(h - 1, 0))
    vals = X2.values[np.isfinite(X2.values)]
    return {
        'n_gun': int(d.sum()), 'n_islem': int(ntr[m].sum()), 'n_bagimsiz': _indep(pos[m][d > 0], h),
        'ort_gun_bps': 1e4 * mu if mu == mu else np.nan, 't': t,
        'ort_islem_bps': 1e4 * vals.mean() if len(vals) else np.nan,
        'medyan_islem_bps': 1e4 * np.median(vals) if len(vals) else np.nan,
        'isabet': float((vals > 0).mean()) if len(vals) else np.nan,
    }


def cost_bps(P, sig, senaryo='temel'):
    """Spot işlem başına ortalama gidiş-dönüş maliyet (bps): komisyon + yarım fiyat adımı (sinyal günü ham fiyatına göre)."""
    c = COST[senaryo]
    cr = P['close_raw'].reindex_like(sig)
    tick = pd.DataFrame(tick_of(cr.values), index=cr.index, columns=cr.columns)
    tb = (1e4 * tick / cr).where(sig.fillna(False).astype(bool))
    v = tb.values[np.isfinite(tb.values)]
    return float(c['spot'] + 0.5 * (v.mean() if len(v) else 0.0))


def _p_one_sided(t):
    from math import erf, sqrt
    if t != t:
        return np.nan
    return float(1 - 0.5 * (1 + erf(t / sqrt(2))))


def periods_of(P):
    last = P['ret_cc'].index.max()
    per = {'IS': (None, IS_END)}
    if last >= OOS1_START:
        per['OOS1'] = (OOS1_START, OOS1_END)
    if last >= KASA_START:
        per['KASA'] = (KASA_START, None)
    return per


def evaluate(sig, P, h=1, side='long', name='', family='', measure='own', instrument='spot', min_n=1, extra=None):
    """Bir sinyal matrisi için sonuç tablosu satırı (spot fiyatlarıyla).
    sig: bool DataFrame (tarih×hisse). measure: karar ölçüsü ('own' zamanlama | 'sec' kesit). min_n: günde en az pozisyon sayısı.
    instrument='viop' ise sütunlar AKSEN/ENJSA/ODAS ile sınırlanır ve maliyet kontrata göre alınır (getiri yine spot;
    vadeli fiyatlarıyla P&L için evaluate_viop kullan)."""
    cols = [c for c in sig.columns if c in P['ret_cc'].columns]
    if instrument == 'viop':
        cols = [c for c in cols if c in VIOP]
    sig = sig[cols].reindex(P['ret_cc'].index).fillna(False).astype(bool)
    if instrument == 'viop':
        for c in cols:
            sig.loc[sig.index < pd.Timestamp(VIOP_START[c]), c] = False
    M, fillable = excess_measures(P, h, side, cols)
    row = {'aile': family, 'sinyal_tanimi': name, 'hedef': ','.join(cols) if len(cols) <= 4 else f'{len(cols)} hisse',
           'yon': side, 'h': h, 'arac': instrument, 'karar_olcusu': measure}
    S_f = sig & fillable
    if instrument == 'viop':
        n_by = S_f.sum()
        tot = max(n_by.sum(), 1)
        cs = {s: float(sum(COST[s][c] * n_by[c] for c in cols) / tot) for s in COST}
    else:
        cs = {s: cost_bps(P, S_f, s) for s in COST}
    periods = periods_of(P)
    for fill_name, fl in [('dol', fillable), ('hepsi', None)]:
        for mname in ['raw', 'own', 'sec', 'mkt']:
            p, ntr, X = day_series(sig, M[mname], fl, min_n)
            for per, (a, b) in periods.items():
                st = stats_block(p, ntr, X, h, a, b)
                if fill_name == 'dol' and mname == measure:
                    row[f'n_gun_{per}'] = st['n_gun']; row[f'n_bagimsiz_{per}'] = st['n_bagimsiz']
                    row[f'n_islem_{per}'] = st['n_islem']
                    row[f'ort_fazla_{per}_bps'] = st['ort_gun_bps']; row[f't_{per}'] = st['t']
                    row[f'p_tek_{per}'] = _p_one_sided(st['t'])
                    row[f'basabas_{per}_bps'] = st['ort_islem_bps']; row[f'isabet_{per}'] = st['isabet']
                    for s in COST:
                        row[f'net_{s}_bps_{per}'] = st['ort_islem_bps'] - cs[s] if st['ort_islem_bps'] == st['ort_islem_bps'] else np.nan
                if fill_name == 'dol' or mname == measure:
                    row[f'{fill_name}_{mname}_{per}_bps'] = st['ort_gun_bps']; row[f'{fill_name}_{mname}_{per}_t'] = st['t']
                if fill_name == 'hepsi' and mname == measure:
                    row[f'n_islem_hepsi_{per}'] = st['n_islem']
    # --- geliştirme dönemi (IS + varsa OOS1; KASA hariç) özetleri
    p, ntr, X = day_series(sig, M[measure], fillable, min_n)
    p_all, ntr_all, _ = day_series(sig, M[measure], None, 1)
    dev_end = OOS1_END
    dev = p[p.index <= dev_end]
    row['dolabilir_oran'] = float(ntr[ntr.index <= dev_end].sum() / max(ntr_all[ntr_all.index <= dev_end].sum(), 1))
    dd = dev.dropna()
    yr = dd.groupby(dd.index.year)
    ym = yr.mean()[yr.count() >= 5]
    row['yil_sayisi'] = int(len(ym)); row['yil_pozitif_orani'] = float((ym > 0).mean()) if len(ym) else np.nan
    row['yillar_bps'] = ';'.join(f'{y}:{1e4 * v:.0f}' for y, v in ym.items())
    dv = dd.sort_values()
    # en iyi 10 GÜN hariç ortalama (YONTEM şart 5). Not: yoğun sinyallerde en iyi %5'i atmak ortalamayı mekanik olarak
    # eksiye çevirir; o yüzden %5 kırpma yalnız simetrik (iki uçtan) verilir.
    row['top10_haric_bps'] = 1e4 * dv.iloc[:-10].mean() if len(dv) > 15 else np.nan
    k5 = int(np.floor(0.05 * len(dv)))
    row['kirpilmis_ort_bps'] = 1e4 * (dv.iloc[k5:len(dv) - k5].mean() if len(dv) > 2 * k5 + 5 else np.nan)
    row['medyan_gun_bps'] = 1e4 * dv.median() if len(dv) else np.nan
    row['maliyet_temel_bps'] = cs['temel']
    Xd = X[X.index <= dev_end]
    cnt = Xd.notna().sum()
    row['en_yogun_hisse'] = cnt.idxmax() if cnt.sum() else ''
    row['en_yogun_pay'] = float(cnt.max() / max(cnt.sum(), 1))
    # --- eski/yeni listelenen hisseler (ilk veri < 2021 / ≥ 2021)
    first = P['ret_cc'][cols].apply(lambda s: s.first_valid_index())
    old = [c for c in cols if first[c] is not None and first[c] < pd.Timestamp('2021-01-01')]
    new = [c for c in cols if c not in old]
    for lab, cc in [('eski', old), ('yeni', new)]:
        v = Xd[cc].values if cc else np.array([])
        v = v[np.isfinite(v)] if len(cc) else v
        row[f'{lab}_islem_bps'] = 1e4 * v.mean() if len(v) else np.nan
        row[f'{lab}_n'] = int(len(v))
    # --- giriş gecikmesi sınaması (geliştirme dönemi, karar ölçüsüyle)
    try:
        Mo, _ = excess_measures(P, h, side, cols, entry='open1')
        po, _, _ = day_series(sig, Mo[measure], fillable, min_n)
        po = po[po.index <= dev_end]
        row['giris_acilis1_bps'] = 1e4 * po.mean()
        sig1 = sig.shift(1, fill_value=False)
        p1, _, _ = day_series(sig1, M[measure], fillable, min_n)
        p1 = p1[p1.index <= dev_end]
        row['giris_kapanis1_bps'] = 1e4 * p1.mean()
        row['giris_kapanis0_bps'] = 1e4 * dd.mean() if len(dd) else np.nan
        sgn = 1.0 if side == 'long' else -1.0
        g = P['ret_co'][cols].shift(-1)
        gex = (g - g.shift(1).rolling(250, min_periods=120).mean()) * sgn
        M1, _ = excess_measures(P, 1, side, cols)
        pg, _, _ = day_series(sig, gex, fillable, min_n)
        pf1, _, _ = day_series(sig, M1['own'], fillable, min_n)
        a, b = pg[pg.index <= dev_end].mean(), pf1[pf1.index <= dev_end].mean()
        row['f1_gece_bps'] = 1e4 * a; row['f1_toplam_bps'] = 1e4 * b
        row['gece_payi'] = float(a / b) if b and b == b and abs(b) > 1e-6 else np.nan
    except Exception as e:  # ret_co yoksa
        row['giris_not'] = f'giriş sınaması yapılamadı: {e}'
    if extra:
        row.update(extra)
    return row


# ----------------------------------------------------------------------------------------------------
# VİOP: vadeli fiyatlarıyla P&L (yakın vade sürekli seri; aynı kontrat içinde getiri)
# ----------------------------------------------------------------------------------------------------
def viop_returns(P, kind='settle'):
    """Yakın vade vadeli günlük getirisi (tarih×dayanak). kind: 'settle' (uzlaşmadan uzlaşmaya) | 'last' (son fiyattan son fiyata).
    viop_front.parquet sütunları: date, und, ret_settle, ret_last, hacim_tl, (varsa) limitte."""
    vf = P['viop_front'].copy()
    vf['date'] = pd.to_datetime(vf['date'])
    col = 'ret_settle' if kind == 'settle' else 'ret_last'
    W = vf.pivot_table(index='date', columns='und', values=col, aggfunc='last')
    W.columns = [str(c).replace('.E', '') for c in W.columns]
    return W.reindex(P['ret_cc'].index)


def viop_volume(P):
    vf = P['viop_front'].copy()
    vf['date'] = pd.to_datetime(vf['date'])
    W = vf.pivot_table(index='date', columns='und', values='hacim_tl', aggfunc='sum')
    W.columns = [str(c).replace('.E', '') for c in W.columns]
    return W.reindex(P['ret_cc'].index)


def evaluate_viop(sig, P, h=1, side='long', name='', family='', extra=None):
    """Vadeli fiyatlarıyla değerlendirme (AKSEN/ENJSA/ODAS). Fazla getiri = pozisyon getirisi − vadelinin kendi geçmiş
    250 günlük ortalama h-günlük getirisi (taşıma dâhil kayma). Hem uzlaşma hem son fiyat tanımı; karar ikisinin kötüsü.
    Dolum: o gün vadelide hacim > 0 ve |getiri| < %9,5 (limit) ve spot dolabilir."""
    cols = [c for c in sig.columns if c in VIOP]
    sig = sig[cols].reindex(P['ret_cc'].index).fillna(False).astype(bool)
    row = {'aile': family, 'sinyal_tanimi': name, 'hedef': ','.join(cols), 'yon': side, 'h': h, 'arac': 'viop_vadeli',
           'karar_olcusu': 'own_vadeli'}
    vol = viop_volume(P)[cols]
    sgn = 1.0 if side == 'long' else -1.0
    res = {}
    for kind in ['settle', 'last']:
        r = viop_returns(P, kind)[cols]
        L = level(r)
        f = L.shift(-h) / L - 1
        own = (f - bench_own(f, h)) * sgn
        lim = (r.abs() >= 0.095)
        fillable = (vol > 0) & r.notna() & ~lim & (P['fill_long'] if side == 'long' else P['fill_short'])[cols]
        S_f = sig & fillable
        n_by = S_f.sum(); tot = max(n_by.sum(), 1)
        cs = {s: float(sum(COST[s][c] * n_by[c] for c in cols) / tot) for s in COST}
        p, ntr, X = day_series(sig, own, fillable)
        pr, _, _ = day_series(sig, f * sgn, fillable)
        res[kind] = {}
        for per, (a, b) in periods_of(P).items():
            st = stats_block(p, ntr, X, h, a, b)
            str_ = stats_block(pr, ntr, X, h, a, b)
            res[kind][per] = st
            row[f'{kind}_n_gun_{per}'] = st['n_gun']; row[f'{kind}_n_bagimsiz_{per}'] = st['n_bagimsiz']
            row[f'{kind}_fazla_{per}_bps'] = st['ort_gun_bps']; row[f'{kind}_t_{per}'] = st['t']
            row[f'{kind}_ham_{per}_bps'] = str_['ort_gun_bps']
            row[f'{kind}_basabas_{per}_bps'] = st['ort_islem_bps']
            row[f'{kind}_net_temel_{per}_bps'] = st['ort_islem_bps'] - cs['temel'] if st['ort_islem_bps'] == st['ort_islem_bps'] else np.nan
        dd = p[p.index <= OOS1_END].dropna()
        yr = dd.groupby(dd.index.year); ym = yr.mean()[yr.count() >= 5]
        row[f'{kind}_yillar_bps'] = ';'.join(f'{y}:{1e4 * v:.0f}' for y, v in ym.items())
        row[f'{kind}_maliyet_temel_bps'] = cs['temel']
    for per in periods_of(P):
        a, b = res['settle'][per], res['last'][per]
        worse = a if (a['ort_gun_bps'] if a['ort_gun_bps'] == a['ort_gun_bps'] else 1e9) <= (b['ort_gun_bps'] if b['ort_gun_bps'] == b['ort_gun_bps'] else 1e9) else b
        row[f'n_gun_{per}'] = worse['n_gun']; row[f'n_bagimsiz_{per}'] = worse['n_bagimsiz']
        row[f'ort_fazla_{per}_bps'] = worse['ort_gun_bps']; row[f't_{per}'] = worse['t']
        row[f'p_tek_{per}'] = _p_one_sided(worse['t']); row[f'basabas_{per}_bps'] = worse['ort_islem_bps']
    if extra:
        row.update(extra)
    return row


# ----------------------------------------------------------------------------------------------------
# İstatistik yardımcıları
# ----------------------------------------------------------------------------------------------------
def bh_fdr(pvals, q=0.10):
    p = np.asarray(pvals, dtype=float)
    out = np.zeros(len(p), dtype=bool)
    idx = np.where(np.isfinite(p))[0]
    if len(idx) == 0:
        return out
    order = idx[np.argsort(p[idx])]
    m = len(idx)
    passed = p[order] <= q * (np.arange(1, m + 1)) / m
    if passed.any():
        out[order[:np.where(passed)[0].max() + 1]] = True
    return out


def holm(pvals, alpha=0.10):
    p = np.asarray(pvals, dtype=float)
    out = np.zeros(len(p), dtype=bool)
    idx = np.where(np.isfinite(p))[0]
    order = idx[np.argsort(p[idx])]
    m = len(idx)
    for k, i in enumerate(order):
        if p[i] <= alpha / (m - k):
            out[i] = True
        else:
            break
    return out


def t_to_p(t):
    from math import erf, sqrt
    t = np.abs(np.asarray(t, dtype=float))
    return 2 * (1 - 0.5 * (1 + np.vectorize(erf)(t / sqrt(2))))


def shift_null(sig, P, h=1, side='long', measure='own', n=300, min_shift=30, seed=0, end=IS_END, start=None):
    """Yer değiştirme (dairesel kaydırma) sıfır dağılımı: sinyal matrisi zamanda rastgele kaydırılır.
    Dönen: (gerçek ortalama bps, tek yönlü p-değeri, sıfır dağılımı)."""
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
        pm = F.where(Sx & fl).mean(axis=1).dropna()
        return 1e4 * pm.mean() if len(pm) else np.nan
    real = stat(S)
    rng = np.random.default_rng(seed)
    T = len(F)
    null = []
    for _ in range(n):
        k = int(rng.integers(min_shift, T - min_shift))
        null.append(stat(pd.DataFrame(np.roll(S.values, k, axis=0), index=S.index, columns=S.columns)))
    null = np.array(null)
    pval = float((np.sum(null >= real) + 1) / (np.sum(np.isfinite(null)) + 1))
    return real, pval, null


def fama_macbeth(y, xs, min_n=8, lag=0):
    """Günlük kesit regresyonu: y[t,i] ~ a_t + Σ b_k,t x_k[t,i]. Dönen: (özet DataFrame, günlük katsayılar)."""
    names = list(xs.keys())
    rows = []
    for dt in y.index:
        yy = y.loc[dt]
        XX = pd.concat([xs[k].loc[dt] for k in names], axis=1, keys=names)
        ok = yy.notna() & XX.notna().all(axis=1)
        if ok.sum() < max(min_n, len(names) + 3):
            continue
        A = np.column_stack([np.ones(ok.sum()), XX[ok].values.astype(float)])
        try:
            b = np.linalg.lstsq(A, yy[ok].values.astype(float), rcond=None)[0]
        except Exception:
            continue
        rows.append([dt] + list(b[1:]))
    B = pd.DataFrame(rows, columns=['date'] + names).set_index('date')
    out = {}
    for k in names:
        x = B[k].values
        mu, t = _hac_mean(x, np.ones(len(x)), lag)
        out[k] = {'katsayi': mu, 't': t, 'n_gun': len(x)}
    return pd.DataFrame(out).T, B


def ts_reg(y, X, lag=0):
    """Zaman serisi OLS + Newey–West. y: Series, X: DataFrame. Dönen: DataFrame(katsayı, t, n)."""
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


def truncate(P, end):
    """Paneli 'end' tarihinde keser (nedensellik öz-denetimi için): build(truncate(P, t)) ile build(P) t'ye kadar aynı sinyali vermeli."""
    end = pd.Timestamp(end)
    Q = {}
    for k, v in P.items():
        if k == '_cache':
            continue
        if isinstance(v, pd.DataFrame) and isinstance(v.index, pd.DatetimeIndex):
            Q[k] = v[v.index <= end]
        elif isinstance(v, pd.DataFrame) and 'date' in v.columns:
            Q[k] = v[pd.to_datetime(v['date']) <= end]
        else:
            Q[k] = v
    Q['_cache'] = {}
    return Q


def self_check_causal(build, P, cut='2021-06-30'):
    """rules.py öz-denetimi: kesik panelle üretilen sinyaller tam panelle üretilenlerle kesim tarihine kadar aynı mı?
    Dönen: {kural adı: fark oranı}. 0 olmalı."""
    full = {r['ad']: r['sig'] for r in build(P)}
    part = {r['ad']: r['sig'] for r in build(truncate(P, cut))}
    out = {}
    for ad, a in part.items():
        b = full[ad]
        idx = a.index[a.index <= pd.Timestamp(cut)]
        cols = sorted(set(a.columns) | set(b.columns))
        x = a.reindex(index=idx, columns=cols).fillna(False).astype(bool)
        y = b.reindex(index=idx, columns=cols).fillna(False).astype(bool)
        out[ad] = float((x != y).values.sum() / max(int(x.values.sum()), 1))
    return out


def eval_rule(rule, P, family=''):
    """rules.py sözleşmesindeki bir kural sözlüğünü değerlendirir (spot; arac='viop' ise ayrıca vadeli fiyatlarıyla)."""
    kw = dict(h=rule['h'], side=rule.get('yon', 'long'), name=rule['ad'], family=family)
    arac = rule.get('arac', 'spot')
    row = evaluate(rule['sig'], P, measure=rule.get('olcu', 'own'), instrument=arac, min_n=rule.get('min_n', 1), **kw)
    row['birincil'] = bool(rule.get('birincil', False)); row['aciklama'] = rule.get('aciklama', '')
    rows = [row]
    if arac == 'viop' and 'viop_front' in P:
        rv = evaluate_viop(rule['sig'], P, **kw)
        rv['birincil'] = row['birincil']; rv['aciklama'] = row['aciklama']
        rows.append(rv)
    return rows
