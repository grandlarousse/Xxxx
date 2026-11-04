"""k_yurtici-takvim_curut: bağımsız yeniden hesaplama kütüphanesi (tarayıcının klib.py'si import EDİLMEZ).
Kurallar:
- VİOP sözleşme kimliği = (dayanak, vade). Aynı (dayanak, vade, gün) için birden çok kod (N1 düzeltmeli) varsa işlem sayısı en yüksek satır.
  Günlük getiri = log(settle / prev_settle) (bültende prev_settle = dünkü uzlaşma; bedelsiz günlerinde N1 kodunun prev_settle'ı düzeltilmiş).
  |r| limit + %0,5 üstü NaN (veri hatası).
- Sözleşme seçimi: sinyal günü t'de, vadesi ÇIKIŞ GÜNÜNDEN SONRA olan (vade > çıkış günü; kesin büyük) ve t'de listelenmiş en yakın vade.
  Tutma süresince sabit. (Tarayıcı vade ≥ çıkış kullandı; burada bilinçli olarak daha katı.)
- Giriş: E0 uzlaşma_t; E1 son işlem_t (close>0 ve trades>0); E2 uzlaşma_{t+1} (o gün yeniden seçilen sözleşme). Çıkış uzlaşma_{t+h} (E2'de t+1+h).
- Spot: Yahoo günlük 'adj' (bölünme+temettü düzeltmeli), bayat gün (v<=0 ya da h==l) NaN, limit üstü NaN.
- t: işlem başına ortalama; giriş tarihine göre kümelenmiş, Bartlett NW (gecikme = h) — tam takvim üzerinde.
"""
import os, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
S = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
OUT = S + '/out/code_k_yurtici-takvim_curut'
RES = OUT + '/res'; os.makedirs(RES, exist_ok=True)
REG = pd.Timestamp('2020-03-13')
_C = {}


def vcal():
    if 'vcal' not in _C:
        d = pd.read_parquet(S + '/data/viop_panel.parquet', columns=['date'])['date']
        _C['vcal'] = pd.DatetimeIndex(np.sort(pd.to_datetime(d).unique()))
    return _C['vcal']


def _panel():
    if 'panel' not in _C:
        F = pd.read_parquet(S + '/data/viop_panel.parquet', columns=['date', 'code', 'und', 'segment', 'ctype', 'expiry', 'settle', 'prev_settle',
                                                                      'close', 'vwap', 'trades', 'value_tl', 'oi'])
        for c in ['code', 'und', 'segment', 'ctype']: F[c] = F[c].astype(str)
        F = F[(F.segment == 'SSF') | ((F.und == 'XU030') & (F.ctype == 'D_IX_FUT'))]
        F['date'] = pd.to_datetime(F.date); F['expiry'] = pd.to_datetime(F.expiry)
        F = F[(F.expiry >= F.date) & (F.settle > 0)]
        F['trades'] = F.trades.fillna(0)
        F = F.sort_values(['und', 'expiry', 'date', 'trades']).drop_duplicates(['und', 'expiry', 'date'], keep='last')
        _C['panel'] = F
    return _C['panel']


class Fut:
    """Bir dayanak için vade x gün matrisleri ve ileri getiri hesaplayıcı."""
    def __init__(self, und):
        F = _panel(); g = F[F.und == und].copy(); cal = vcal()
        self.und = und
        g['r'] = np.log(g.settle / g.prev_settle)
        pre = g.date < REG
        lim = np.where(pre, np.log(1.205), np.log(1.105)); limd = np.where(pre, np.log(0.795), np.log(0.895))
        if und != 'XU030':
            g.loc[(g.r > lim) | (g.r < limd), 'r'] = np.nan
        self.exps = np.array(sorted(g.expiry.unique()), dtype='datetime64[ns]')
        def piv(col):
            return g.pivot(index='date', columns='expiry', values=col).reindex(index=cal, columns=self.exps)
        self.R = piv('r'); self.ST = piv('settle'); self.CL = piv('close'); self.TR = piv('trades')
        self.CL = self.CL.where((self.CL > 0) & (self.TR > 0))
        Rv = self.R.values
        self.cs = np.vstack([np.zeros((1, Rv.shape[1])), np.nancumsum(Rv, axis=0)])  # cs[i] = sum r[0..i-1]
        self.cn = np.vstack([np.zeros((1, Rv.shape[1])), np.cumsum(np.isfinite(Rv), axis=0)])
        self.listed = self.ST.notna().values
        self.cal = cal

    def choose(self, i, h):
        """t indeksi i, ufuk h: vade > cal[i+h] olan, i'de listelenmiş en yakın vade sütunu (yoksa -1)."""
        n = len(self.cal)
        out = np.full(len(i), -1)
        ok = (i >= 0) & (i + h < n)
        ex = np.full(len(i), np.datetime64('NaT'), dtype='datetime64[ns]')
        ex[ok] = self.cal.values[i[ok] + h]
        j0 = np.searchsorted(self.exps, ex, side='right')
        for k in np.where(ok)[0]:
            j = j0[k]
            while j < len(self.exps) and not self.listed[i[k], j]:
                j += 1
                if j - j0[k] > 2: break
            if j < len(self.exps) and self.listed[i[k], j]: out[k] = j
        return out

    def fwd(self, dates, h, entry='E0'):
        """dates: giriş/sinyal günleri (VİOP takviminde). Döner: log getiri dizisi (yön uygulanmamış)."""
        dates = pd.DatetimeIndex(dates)
        i = self.cal.get_indexer(dates)
        if entry == 'E2':
            i = np.where(i >= 0, i + 1, -1); i = np.where(i < len(self.cal), i, -1)
        j = self.choose(i, h)
        r = np.full(len(i), np.nan)
        ok = (i >= 0) & (j >= 0) & (i + h < len(self.cal))
        a = i[ok] + 1; b = i[ok] + h + 1; jj = j[ok]  # r[i+1..i+h] = cs[i+h+1]-cs[i+1]
        s = self.cs[b, jj] - self.cs[a, jj]; c = self.cn[b, jj] - self.cn[a, jj]
        r[ok] = np.where(c == h, s, np.nan)
        if entry == 'E1':
            st = np.full(len(i), np.nan); cl = np.full(len(i), np.nan)
            st[ok] = self.ST.values[i[ok], jj]; cl[ok] = self.CL.values[i[ok], jj]
            r = r + np.log(st / cl)
        return r

    def front_series(self, col='settle', min_dte=2):
        """Her gün en yakın vade (vade − gün ≥ min_dte takvim günü) değerleri + sözleşme sütunu."""
        cal = self.cal; M = {'settle': self.ST, 'close': self.CL, 'trades': self.TR}[col].values
        res = np.full(len(cal), np.nan); jj = np.full(len(cal), -1)
        for k, d in enumerate(cal.values):
            j = np.searchsorted(self.exps, d + np.timedelta64(min_dte, 'D'), side='left')
            while j < len(self.exps) and not self.listed[k, j]: j += 1
            if j < len(self.exps): res[k] = M[k, j]; jj[k] = j
        return pd.Series(res, index=cal), pd.Series(jj, index=cal)


_FUT = {}
def fut(und):
    if und not in _FUT: _FUT[und] = Fut(und)
    return _FUT[und]


def spot(sym, field='adj'):
    """Yahoo günlük; index = ldate. Bayat gün NaN."""
    d = pd.read_parquet(S + f'/data/daily/{sym}.IS.parquet'); d.index = pd.DatetimeIndex(d.ldate); d = d[~d.index.duplicated(keep='last')]
    if not sym.startswith('XU'):
        st = (d.v <= 0) | (d.h == d.l)
        d.loc[st, ['o', 'h', 'l', 'c', 'adj']] = np.nan
    return d


def spot_ret(sym):
    d = spot(sym); a = d['adj']
    r = np.log(a / a.ffill().shift(1)).where(a.notna())
    pre = r.index < REG
    up = np.where(pre, np.log(1.205), np.log(1.105)); dn = np.where(pre, np.log(0.795), np.log(0.895))
    if not sym.startswith('XU'):
        r = r.mask((r > up) | (r < dn))
    return r


def spot_fwd(r, h):
    """t+1..t+h toplamı; eksik varsa NaN."""
    return r.rolling(h, min_periods=h).sum().shift(-h)


# ------------------ istatistik ------------------
def clnw(dates, x, lag):
    """İşlem ortalaması ve giriş tarihine göre kümelenmiş + Bartlett NW t (tam iş günü takvimi)."""
    d = pd.DataFrame({'d': pd.DatetimeIndex(dates), 'x': np.asarray(x, float)}).dropna()
    N = len(d)
    if N < 8: return np.nan, np.nan, N
    m = d.x.mean(); e = d.x - m
    U = e.groupby(d.d).sum()
    idx = vcal()
    idx = idx[(idx >= U.index.min()) & (idx <= U.index.max())]
    U = U.reindex(idx.union(U.index)).fillna(0).values
    v = U @ U
    for l in range(1, lag + 1): v += 2 * (1 - l / (lag + 1)) * (U[l:] @ U[:-l])
    se = np.sqrt(v) / N
    return m * 1e4, (m / se if se > 0 else np.nan), N


def pval(t):
    from scipy.stats import norm
    return float(2 * norm.sf(abs(t))) if np.isfinite(t) else np.nan


PER = [('2017-19', '2017-01-01', '2019-12-31'), ('2020-21', '2020-01-01', '2021-12-31'), ('2022-23', '2022-01-01', '2023-12-31'),
       ('2024-26', '2024-01-01', '2026-12-31'), ('fon_krizi', '2026-09-01', '2026-12-31')]


def summary(dates, x, h, cost=0.0, is_end='2021-12-31', top=10, per=True):
    dates = pd.DatetimeIndex(dates); x = np.asarray(x, float)
    ok = np.isfinite(x); dates = dates[ok]; x = x[ok]
    m, t, n = clnw(dates, x, h)
    o = dict(n=n, gross=m, t=t, net=m - cost if np.isfinite(m) else np.nan, p=pval(t))
    if n == 0: return o
    yrs = max((dates.max() - dates.min()).days / 365.25, 0.5); o['per_yr'] = n / yrs
    o['hit'] = float((x > 0).mean())
    ie = pd.Timestamp(is_end)
    mi, ti, ni = clnw(dates[dates <= ie], x[dates <= ie], h); mo, to, no = clnw(dates[dates > ie], x[dates > ie], h)
    o.update(IS=mi, IS_t=ti, IS_n=ni, OOS=mo, OOS_t=to, OOS_n=no)
    if per:
        for lab, a, b in PER:
            msk = (dates >= a) & (dates <= b)
            mm, tt, nn = clnw(dates[msk], x[msk], h) if msk.sum() >= 8 else (np.nanmean(x[msk]) * 1e4 if msk.sum() else np.nan, np.nan, int(msk.sum()))
            o[f'{lab}'] = mm; o[f'{lab}_t'] = tt; o[f'{lab}_n'] = nn
    yy = pd.Series(x, index=dates).groupby(dates.year).mean() * 1e4
    o['yrs'] = f'{(yy > 0).sum()}/{len(yy)}'; o['by_year'] = ' '.join(f'{k % 100:02d}:{v:+.0f}' for k, v in yy.items())
    if n > top + 8:
        k = np.argsort(x)[::-1][top:]
        mt, tt, _ = clnw(dates[k], x[k], h); o['ex_top10'] = mt; o['ex_top10_t'] = tt
    return o


def fmt(o):
    if not o or o.get('n', 0) < 8: return f"n={o.get('n', 0)}"
    s = (f"n={o['n']} ({o['per_yr']:.0f}/yıl) brüt {o['gross']:+.1f} t {o['t']:.2f} isabet {o['hit']:.2f} | IS {o['IS']:+.1f} (t {o['IS_t']:.2f}, n {o['IS_n']}) "
         f"OOS {o['OOS']:+.1f} (t {o['OOS_t']:.2f}, n {o['OOS_n']}) | yıl+ {o['yrs']} | top10 hariç {o.get('ex_top10', np.nan):+.1f} (t {o.get('ex_top10_t', np.nan):.2f})")
    pp = ' | '.join(f"{lab} {o.get(lab, np.nan):+.0f} (t {o.get(lab + '_t', np.nan):.1f}, n {o.get(lab + '_n', 0)})" for lab, _, _ in PER)
    return s + '\n      dönemler: ' + pp + '\n      yıllar: ' + o['by_year']


def bh_q(p):
    p = np.asarray(p, float); q = np.full(len(p), np.nan); idx = np.where(np.isfinite(p))[0]
    if len(idx) == 0: return q
    ps = p[idx]; o = np.argsort(ps); n = len(ps)
    qq = ps[o] * n / np.arange(1, n + 1); qq = np.minimum.accumulate(qq[::-1])[::-1]
    q[idx[o]] = np.minimum(qq, 1); return q


REGISTRY = []
def reg(block, name, h, entry, o, **kw):
    r = dict(block=block, name=name, h=h, entry=entry, n=o.get('n'), gross=o.get('gross'), t=o.get('t'), p=o.get('p'),
             IS=o.get('IS'), IS_t=o.get('IS_t'), OOS=o.get('OOS'), OOS_t=o.get('OOS_t'), ex_top10=o.get('ex_top10'), yrs=o.get('yrs'))
    r.update(kw); REGISTRY.append(r); return r


def save(block):
    D = pd.DataFrame([r for r in REGISTRY if r['block'] == block]); D.to_csv(RES + f'/tests_{block}.csv', index=False); return D


def placebo_dates(dates, sides, x_fun, pool, nrep=500, seed=0):
    """Rastgele tarih plasebosu: aynı sayıda tarih pool'dan çekilir, yönler korunur. Döner: plasebo ortalamaları (bps)."""
    rng = np.random.default_rng(seed); pool = pd.DatetimeIndex(pool); n = len(dates); res = []
    for _ in range(nrep):
        d = pool[rng.choice(len(pool), n, replace=False)]
        v = sides * x_fun(d); res.append(np.nanmean(v) * 1e4)
    return np.array(res)
