"""V1 bağımsız yeniden üretim kütüphanesi. elib ve panel_full'un ret_/lim_/tradable/px dosyaları KULLANILMAZ.
Girdi yalnız raw/d1/isy_hisse/*.json ve raw/d1/isy_endeks/*.json (İş Yatırım ham JSON)."""
import json, os
import numpy as np
import pandas as pd

SEKTOR = ("A1YEN AHGAZ AKENR AKFYE AKSEN AKSUE ALFAS ARFYE AYDEM AYEN BESTE BIOEN BIGEN CONSE CWENE CANTE CATES "
          "ARASE ECOGR ENDAE ENJSA ENERY ESEN GWIND HUNER ENTRA IZENR KLYPV LYDYE MAGEN MASFN METEN MOGAN NTGAZ "
          "NATEN ODAS PAMEL SMRTG TATEN VEYAS ZEDUR ZOREN").split()
VIOP3 = ['AKSEN', 'ENJSA', 'ODAS']
START, END = pd.Timestamp('2010-01-04'), pd.Timestamp('2026-11-20')
MARJ_TARIH = pd.Timestamp('2020-03-13')
ADIM_TARIH = pd.Timestamp('2023-11-06')
DONEM = {'IS': (START, pd.Timestamp('2022-12-30')),
         'OOS1': (pd.Timestamp('2023-01-02'), pd.Timestamp('2025-06-30')),
         'KASA': (pd.Timestamp('2025-07-01'), END),
         'HAVUZ': (pd.Timestamp('2023-01-02'), END)}


def endeks(raw, kod):
    d = json.load(open(os.path.join(raw, 'isy_endeks', kod + '.json')))['data']
    s = pd.Series({pd.Timestamp(int(x[0]), unit='ms', tz='UTC').tz_convert('Europe/Istanbul').tz_localize(None).normalize(): float(x[1])
                   for x in d})
    return s.sort_index()


def takvim(raw):
    """XU100'ün işlem gördüğü günler; bayat 2013-01-01 ve iptal edilen 2023-02-08 hariç."""
    x = endeks(raw, 'XU100')
    ix = x.index[(x.index >= START) & (x.index <= END)]
    return ix.difference(pd.DatetimeIndex(['2013-01-01', '2023-02-08']))


def adim(p, tarih_yeni):
    """Fiyat adımı (VERI_NOTU_D1'deki tablo). p: ndarray, tarih_yeni: bool ndarray (>= 2023-11-06)."""
    t = np.where(p < 20, 0.01, np.where(p < 50, 0.02, np.where(p < 100, 0.05, 0.10)))
    t2 = np.where(p < 250, t, np.where(p < 500, 0.25, np.where(p < 1000, 0.50, np.where(p < 2500, 1.00, 2.50))))
    return np.where(tarih_yeni, t2, t)


def hisse(raw, kod, cal):
    """Bir hissenin takvime oturtulmuş günlük tablosu: düzeltilmiş getiri, kilit bayrakları, dolabilirlik."""
    v = json.load(open(os.path.join(raw, 'isy_hisse', kod + '.json')))['value']
    d = pd.DataFrame(v)[['HGDG_TARIH', 'HG_KAPANIS', 'HGDG_KAPANIS', 'HG_MIN', 'HG_MAX', 'HG_HACIM', 'HGDG_HACIM']]
    d['date'] = pd.to_datetime(d['HGDG_TARIH'], format='%d-%m-%Y')
    d = d.drop_duplicates('date').set_index('date').sort_index()
    d = d[d.HG_KAPANIS.notna() & (d.HG_KAPANIS > 0)]
    ilk = d.index.min()                                   # ilk işlem günü (ham dosyanın ilk satırı)
    # --- düzeltme çarpanı: F = ham/düzeltilmiş; sıçrama günleri arasında parça parça sabit (medyan)
    f = (d.HG_KAPANIS / d.HGDG_KAPANIS).astype(float)
    gurultu = 0.00005 / d.HGDG_KAPANIS                    # 4 ondalık yuvarlama
    tol = np.maximum(0.002, 4 * np.maximum(gurultu, gurultu.shift(1).fillna(0)))
    sic = ((f / f.shift(1) - 1).abs() > tol).fillna(False)
    seg = sic.cumsum()
    F = f.groupby(seg).transform('median')
    d['F'] = F
    d['ca'] = sic
    # --- takvime oturt
    g = d.reindex(cal)
    var = g.HG_KAPANIS.notna()
    c = g.HG_KAPANIS.ffill(); Fz = g.F.ffill()
    cadj = c / Fz                                          # kendi düzeltilmiş kapanışım (taşınmış)
    out = pd.DataFrame(index=cal)
    out['var'] = var
    out['c_raw'] = g.HG_KAPANIS; out['h_raw'] = g.HG_MAX; out['l_raw'] = g.HG_MIN
    out['cadj'] = cadj
    out['hacim'] = g.HG_HACIM.fillna(0)
    # --- baz fiyat ve kilit
    baz = c.shift(1) * (Fz / Fz.shift(1))
    marj = np.where(cal >= MARJ_TARIH, 0.10, 0.20)
    yeni = np.asarray(cal >= ADIM_TARIH)
    tav_h = (baz * (1 + marj)).values; tab_h = (baz * (1 - marj)).values
    a_tav = adim(np.nan_to_num(tav_h), yeni); a_tab = adim(np.nan_to_num(tab_h), yeni)
    tavan = np.floor(tav_h / a_tav + 1e-6) * a_tav
    taban = np.ceil(tab_h / a_tab - 1e-6) * a_tab
    cr, hr, lr = out.c_raw.values, out.h_raw.values, out.l_raw.values
    with np.errstate(invalid='ignore'):
        out['tavan'] = var.values & (np.abs(cr - hr) < 1e-9) & (cr >= tavan - 2 * a_tav - 1e-9)
        out['taban'] = var.values & (np.abs(cr - lr) < 1e-9) & (cr <= taban + 2 * a_tab + 1e-9)
    # --- halka arz: ilk 20 işlem günü ve ilk tavansız kapanışa kadar dışarıda
    n = var.cumsum()                                       # takvimde görülen kendi işlem günü sayısı
    if ilk < cal[0]:
        n = n + 10000                                      # panel başlamadan önce listelenmiş
        tavansiz_gordu = pd.Series(True, index=cal)
    else:
        ilk_gun = (n == 1) & var
        tavansiz = var & ~out['tavan'] & ~ilk_gun          # ilk günün bazı (halka arz fiyatı) yok: tavansız sayılmaz
        tavansiz_gordu = tavansiz.cumsum() > 0
    out['ipo_n'] = n
    out['tradable'] = var & (out.hacim > 0) & (n > 20) & tavansiz_gordu
    out['fill'] = out.tradable & ~out.tavan
    return out


def panel(raw):
    cal = takvim(raw)
    H = {k: hisse(raw, k, cal) for k in SEKTOR}
    W = lambda col: pd.DataFrame({k: H[k][col] for k in SEKTOR})
    P = {'cal': cal, 'cadj': W('cadj'), 'tavan': W('tavan').fillna(False), 'taban': W('taban').fillna(False),
         'tradable': W('tradable').fillna(False), 'fill': W('fill').fillna(False), 'var': W('var').fillna(False)}
    E = pd.DataFrame({k: endeks(raw, k).reindex(cal) for k in ['XELKT', 'XU030']})
    P['idx'] = E
    P['idx_ret'] = E / E.shift(1) - 1
    return P


def ileri(P, h, max_delay=None):
    """f_h: giriş t kapanışı, çıkış t+h kapanışı; çıkış günü tabanda kilitliyse ilk kilitsiz kapanış (ANA tanım, max_delay=None).
    max_delay=k: çıkış en çok k gün kayar, k günün sonunda hâlâ kilitliyse o kilitli kapanıştan çıkılmış sayılır
    (ortak kütüphanenin davranışını taklit etmek için; yalnız fark teşhisinde kullanılır)."""
    c = P['cadj']; tb = P['taban'].values; cv = c.values
    T, N = cv.shape
    out = np.full((T, N), np.nan)
    if max_delay is None:
        nxt = np.full((T, N), np.nan)
        last = np.full(N, np.nan)
        for t in range(T - 1, -1, -1):
            last = np.where(~tb[t], cv[t], last)
            nxt[t] = last
        out[:T - h] = nxt[h:] / cv[:T - h] - 1
    else:
        e = np.minimum(np.arange(T)[:, None] + h, T - 1) * np.ones((1, N), dtype=int)
        valid = (np.arange(T)[:, None] + h <= T - 1) * np.ones((1, N), dtype=bool)
        for _ in range(max_delay):
            locked = np.take_along_axis(tb, e, axis=0) & valid
            can = locked & (e + 1 <= T - 1)
            valid &= ~(locked & ~can)
            e = np.where(can, e + 1, e)
        out = np.take_along_axis(cv, e, axis=0) / cv - 1
        out[~valid] = np.nan
    return pd.DataFrame(out, index=c.index, columns=c.columns)


def z60(r):
    return r / r.rolling(60, min_periods=40).std().shift(1)


def sinyaller(P):
    L, r = P['idx'], P['idx_ret']
    zE, zX = z60(r['XELKT']), z60(r['XU030'])
    s1 = L['XELKT'] >= L['XELKT'].rolling(20, min_periods=20).max()
    s2 = zE >= 1.0
    s3 = (zX >= 1.0) & (zE < 0.5)
    f = lambda s: s.fillna(False).astype(bool)
    return {'S1': (f(s1), SEKTOR, 5), 'S2': (f(s2), SEKTOR, 5), 'S3': (f(s3), VIOP3, 1)}


def nw_t(x, pos, lag=2):
    """Olay günleri ortalamasının HAC t'si: yalnız takvimde <= lag gün arayla düşen olay çiftleri kovaryansa girer (Bartlett)."""
    x = np.asarray(x, float); pos = np.asarray(pos); n = len(x)
    if n < 3:
        return np.nan
    e = x - x.mean()
    v = (e * e).sum()
    for k in range(1, lag + 1):
        w = 1 - k / (lag + 1)
        # takvim konumu tam k gün sonra olan olaylar
        idx = {p: i for i, p in enumerate(pos)}
        s = sum(e[i] * e[idx[p + k]] for i, p in enumerate(pos) if (p + k) in idx)
        v += 2 * w * s
    v = max(v, 1e-18) / n ** 2 * n / (n - 1)
    return x.mean() / np.sqrt(v)


def bagimsiz(pos, h):
    k, son = 0, -10 ** 9
    for p in pos:
        if p - son >= h:
            k += 1; son = p
    return k
