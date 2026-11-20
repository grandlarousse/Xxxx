"""V2 bagimsiz yeniden uretim (kesit kurallari T2, K1, K2) - ortak kutuphane (elib) ve hazir paneller KULLANILMAZ.
Ham kaynak: Is Yatirim HisseTekil JSON'lari (raw/d1/isy_hisse) + XU100 takvimi (raw/d1/isy_endeks/XU100.json).
Tanimlar YONTEM.md / YONTEM_EK.md (E2, E4) metninden ve rules.py dosyalarinin okunmasindan yeniden yazildi."""
import json
import os
import numpy as np
import pandas as pd

# evren: YONTEM.md bolum 1 (KAP, 20.11.2026); sira = kural dosyalarindaki esitlik bozma sirasi
XELKT = ('A1YEN AHGAZ AKENR AKFYE AKSEN AKSUE ALFAS ARFYE AYDEM AYEN BESTE BIOEN BIGEN CONSE CWENE CANTE CATES '
         'ARASE ECOGR ENDAE ENJSA ENERY ESEN GWIND HUNER ENTRA IZENR KLYPV LYDYE MAGEN MASFN METEN MOGAN NTGAZ '
         'NATEN ODAS PAMEL SMRTG TATEN VEYAS ZEDUR ZOREN').split()
START = pd.Timestamp('2010-01-04')
MARJ10 = pd.Timestamp('2020-03-13')
TICK_CHG = pd.Timestamp('2023-11-06')
IS_END = pd.Timestamp('2022-12-30')
OOS1 = (pd.Timestamp('2023-01-02'), pd.Timestamp('2025-06-30'))
KASA_START = pd.Timestamp('2025-07-01')
PERIODS = {'IS': (None, IS_END), 'OOS1': OOS1, 'KASA': (KASA_START, None), 'HAVUZ2023': (OOS1[0], None)}


def tick(p, dates):
    """BIST pay piyasasi fiyat adimi (VERI_NOTU_D1: 2023-11-06 oncesi >= 100 TL icin 0,10)."""
    p = np.asarray(p, dtype=float)
    new = np.select([p < 20, p < 50, p < 100, p < 250, p < 500, p < 1000, p < 2500], [0.01, 0.02, 0.05, 0.10, 0.25, 0.50, 1.0], 2.5)
    old = np.select([p < 20, p < 50, p < 100], [0.01, 0.02, 0.05], 0.10)
    return np.where(np.asarray(pd.DatetimeIndex(dates) >= TICK_CHG), new, old)


def calendar(raw):
    x = json.load(open(os.path.join(raw, 'isy_endeks', 'XU100.json')))['data']
    d = (pd.to_datetime([r[0] for r in x], unit='ms') + pd.Timedelta(hours=3)).normalize()
    d = pd.DatetimeIndex(sorted(set(d)))
    d = d[(d >= START) & (d != pd.Timestamp('2013-01-01'))]      # bayat yilbasi satiri
    return d


def read_stock(raw, sym, sub='isy_hisse'):
    v = json.load(open(os.path.join(raw, sub, sym + '.json')))['value']
    d = pd.DataFrame(v)
    d.index = pd.to_datetime(d['HGDG_TARIH'], format='%d-%m-%Y')
    d = d[~d.index.duplicated(keep='last')].sort_index()
    return pd.DataFrame({'c': d['HG_KAPANIS'], 'h': d['HG_MAX'], 'l': d['HG_MIN'], 'v': d['HG_HACIM'],
                         'ca': d['HGDG_KAPANIS']}).astype(float)


def adj_factor(a):
    """F = ham/duzeltilmis oranin parca parca sabit kestirimi. Kirilma: gunluk oran degisimi, HGDG'nin 4 hane
    yuvarlama payini asiyorsa. Parca ici medyan; medyani onceki parcadan < 3e-4 ayrisan parca birlestirilir."""
    q = (a.c / a.ca).where((a.c > 0) & (a.ca > 0)).ffill().bfill()
    tol = 1.5 * (0.5e-4 / a.ca.ffill().bfill() + 0.5e-4 / a.ca.ffill().bfill().shift(1)) + 1e-4
    brk = ((q / q.shift(1) - 1).abs() > tol).fillna(False).values
    seg = np.cumsum(brk)
    med = q.groupby(seg).median()
    keep = {0: 0}
    cur = 0
    for k in range(1, len(med)):
        if abs(med.iloc[k] / med.iloc[cur] - 1) > 3e-4:
            cur = k
        keep[k] = cur
    seg2 = np.array([keep[s] for s in seg])
    F = q.groupby(seg2).transform('median')
    return F


def build(raw, syms=None, sub='isy_hisse'):
    """Ham JSON -> takvim x hisse matrisleri (hepsi kendi kodumuz)."""
    cal = calendar(raw)
    syms = syms or XELKT
    out = {k: {} for k in ('ret', 'cadj', 'craw', 'vol', 'lu', 'ld', 'tu', 'td', 'ipo_n', 'has', 'caday', 'ldx')}
    pos = pd.Series(np.arange(len(cal)), index=cal)
    for s in syms:
        a0 = read_stock(raw, s, sub)
        a0 = a0[a0.c > 0]
        F0 = adj_factor(a0)
        a0['F'] = F0
        a0['cadj'] = a0.c / a0.F
        prev = a0.cadj.shift(1)
        a0['ret'] = a0.cadj / prev - 1                       # ilk satir (halka arz gunu) bos
        a0['ref'] = a0.c.shift(1) * a0.F / a0.F.shift(1)     # bugunun ham olceginde baz fiyat
        a0['caday'] = (a0.F / a0.F.shift(1) - 1).abs() > 1e-9
        a = a0[a0.index.isin(cal)]
        if len(a) == 0:
            continue
        first = a0.index[a0.index >= START][0] if a0.index[0] >= START else None
        idx = a.index
        m = np.where(idx >= MARJ10, 0.10, 0.20)
        hasv = (a.v > 0).values
        h = np.where(hasv, a.h.values, a.c.values)
        lo = np.where(hasv, a.l.values, a.c.values)
        c = a.c.values
        ref = a.ref.values
        upr = ref * (1 + m)
        dnr = ref * (1 - m)
        tku = tick(upr, idx)
        tkd = tick(dnr, idx)
        tavan = np.floor(upr / tku + 1e-6) * tku
        taban = np.ceil(dnr / tkd - 1e-6) * tkd
        eps = 1e-9
        tu = (h >= tavan - 2 * tku - eps) & hasv & np.isfinite(ref)
        td = (lo <= taban + 2 * tkd + eps) & hasv & np.isfinite(ref)
        lu = tu & (c >= tavan - 2 * tku - eps) & (c >= h - eps)             # E4: kapanis = gun ici en yuksek, tavana <= 2 adim
        ld = td & (c <= taban + 2 * tkd + eps) & (c <= lo + eps)
        ldx = (c <= taban + eps) & hasv & np.isfinite(ref)                  # tam taban fiyatinda kapanis
        ser = lambda x, fill: pd.Series(x, index=idx).reindex(cal, fill_value=fill)
        out['ret'][s] = a.ret.reindex(cal)
        out['cadj'][s] = a.cadj.reindex(cal)
        out['craw'][s] = a.c.reindex(cal)
        out['vol'][s] = a.v.reindex(cal).fillna(0.0)
        out['lu'][s] = ser(lu, False)
        out['ld'][s] = ser(ld, False)
        out['tu'][s] = ser(tu, False)
        out['td'][s] = ser(td, False)
        out['ldx'][s] = ser(ldx, False)
        out['has'][s] = ser(np.ones(len(idx), bool), False)
        out['caday'][s] = ser(a.caday.values, False)
        if first is None:
            ipo = pd.Series(10 ** 6, index=cal)                             # 2010 oncesi halka acik
        else:
            ipo = (pos - pos[first] + 1).clip(lower=0)
        out['ipo_n'][s] = ipo
    P = {k: pd.DataFrame(v)[[s for s in syms if s in v]] for k, v in out.items()}
    R, lu = P['ret'], P['lu']
    first_free = ((~lu) & R.notna()).cumsum() > 0                           # ilk tavansiz kapanis goruldu
    P['tr'] = P['has'] & (P['vol'] > 0) & (P['ipo_n'] > 20) & R.notna() & first_free
    P['fill'] = P['tr'] & ~lu
    return P


def fwd(P, h=1, shift=True, cap=5):
    """c(t) -> c(t+h). shift=True: cikis gunu tabanda kilitliyse ilk kilitsiz kapanisa kayar (en cok `cap` gun; None = sinirsiz).
    Kilit bitmeden veri biterse getiri bos."""
    L = P['cadj'].ffill().values
    lk = P['ld'].values
    n, m = L.shape
    ex = np.arange(n)[:, None] + h + np.zeros((1, m), dtype=int)
    valid = ex <= n - 1
    ex = np.minimum(ex, n - 1)
    if shift:
        k = 0
        while cap is None or k < cap:
            locked = np.take_along_axis(lk, ex, axis=0) & valid
            if not locked.any():
                break
            can = locked & (ex + 1 <= n - 1)
            valid &= ~(locked & ~can)
            ex = np.where(can, ex + 1, ex)
            k += 1
    f = np.take_along_axis(L, ex, axis=0) / L - 1
    f[~valid] = np.nan
    return pd.DataFrame(f, index=P['cadj'].index, columns=P['cadj'].columns)


def sec_excess(f, bench_mask, kind='mean', min_others=4):
    """hisse - ayni gun, kendisi haric, bench_mask icindeki hisselerin esit agirlikli (ya da medyan) f'i."""
    X = f.where(bench_mask)
    if kind == 'mean':
        S = X.sum(axis=1, min_count=1)
        N = X.notna().sum(axis=1)
        own = X.notna()
        s = (-X.fillna(0)).add(S, axis=0)
        n = (-own.astype(int)).add(N, axis=0)
        b = (s / n).where(n >= min_others)
        return f - b
    # medyan: hedef haric
    Xv = X.values
    out = np.full(Xv.shape, np.nan)
    for i in range(Xv.shape[0]):
        row = Xv[i]
        ok = np.isfinite(row)
        if ok.sum() < min_others:
            continue
        for j in range(Xv.shape[1]):
            o = ok.copy()
            o[j] = False
            if o.sum() >= min_others:
                out[i, j] = np.median(row[o])
    return f - pd.DataFrame(out, index=f.index, columns=f.columns)


def stats(E, sig, start=None, end=None):
    """Gunluk esit agirlikli ortalama -> gunler arasi ortalama ve t. E: fazla getiri matrisi; sig: bool (dolabilirle kesilmis)."""
    X = E.where(sig)
    if start is not None:
        X = X[X.index >= start]
    if end is not None:
        X = X[X.index <= end]
    p = X.mean(axis=1).dropna()
    vals = X.values[np.isfinite(X.values)]
    n = len(p)
    if n < 3:
        return dict(n_gun=n, n_islem=len(vals), ort_bps=np.nan, t=np.nan, medyan_gun_bps=np.nan, medyan_islem_bps=np.nan,
                    isabet_islem=np.nan, isabet_gun=np.nan, ort_islem_bps=np.nan)
    mu = p.mean()
    se = p.std(ddof=1) / np.sqrt(n)
    return dict(n_gun=n, n_islem=int(len(vals)), ort_bps=1e4 * mu, t=mu / se, medyan_gun_bps=1e4 * p.median(),
                medyan_islem_bps=1e4 * np.median(vals), isabet_islem=float((vals > 0).mean()), isabet_gun=float((p > 0).mean()),
                ort_islem_bps=1e4 * vals.mean())


# ------------------------------------------------------------------ kurallar (rules.py okunarak yeniden yazildi)
def _bucket(score, uni, nb, min_n):
    S = score.where(uni)
    n = S.notna().sum(axis=1)
    rk = S.rank(axis=1, method='first')
    b = np.floor((rk - 1).mul(nb).div(n.where(n > 0), axis=0))
    b[(n < min_n).values] = np.nan
    return b


def rule_T2(P):
    """W3B_sade_sakin_guclu_h1: dolabilir & bayraksiz & oynaklik20 alt yari & r(t) en ust ucte birlik (>= 6 hisse)."""
    sc = sorted(P['ret'].columns)
    R = P['ret'][sc].round(4)
    fill, tr = P['fill'][sc], P['tr'][sc]
    valid = tr & R.notna()
    vol20 = R.rolling(20, min_periods=10).std().round(8).where(valid)
    low = _bucket(vol20, fill, 2, 6) == 0
    strong = _bucket(R.where(valid), fill, 3, 6) == 2
    lu, ld, tu, td = P['lu'][sc], P['ld'][sc], P['tu'][sc], P['td'][sc]
    flag = (tu & ~lu) | (td & ~ld) | ld
    return (fill & ~flag & low & strong)[P['ret'].columns]


def _rel1(P, min_n=8):
    R = P['ret'].where(P['tr'])
    n = R.notna().sum(axis=1)
    return R.sub(R.mean(axis=1).where(n >= min_n), axis=0), n


def rule_K1(P):
    """A3_rel1_alt5_h1_RED: 1 gunluk (hisse - EW tradable sektor) getirisinde en alt beste birlik (floor(n/5), en az 1; n >= 8)."""
    rel, n = _rel1(P)
    kq = np.floor(n * 0.2).clip(lower=1)
    r = rel.rank(axis=1, method='first', ascending=True)
    m = r.le(kq, axis=0) & rel.notna()
    return m & pd.DataFrame(np.repeat((n >= 8).values[:, None], rel.shape[1], axis=1), index=rel.index, columns=rel.columns)


def rule_K2(P):
    """W3A_sektorden_5puan_geride_KACIN_h1: rel1 <= -0,05 & tradable (n >= 8; tabanda kapananlar dahil)."""
    rel, n = _rel1(P)
    return ((rel <= -0.05) & P['tr']).fillna(False)
