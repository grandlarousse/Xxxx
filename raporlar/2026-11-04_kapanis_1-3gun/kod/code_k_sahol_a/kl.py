"""k_sahol_a ortak kütüphane: SAHOL/AKBNK oran ortalamaya dönüşü -> kapanıştan kapanışa VİOP işlem planı.
Sinyal: kaynak (code_y_grup/09_bt.py BT3) ile birebir: r = ll.ret (adj log getiri, BIST takvimi, rejime bağlı ±%20,5/±%10,5 temizlik),
beta = rolling250(min120) cov/var, shift(1); S = cumsum(rA - beta*rB); z = (S - mean60)/std60 (min 30).
P&L: VİOP ön vade uzlaşma fiyatı (settle). Giriş/çıkış = sinyal günü uzlaşması (lag=0).
Devir: vadeye R iş günü kala (bdl<=R olunca) uzlaşmadan yeni vadeye geçiş; maliyet = her bacakta tam gidiş-dönüş (eski kapat + yeni aç = 2 yarım spread).
"""
import sys, os, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
SCR = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
sys.path.insert(0, SCR + '/code')
import ll
NEW = SCR + '/dl_k_sahol_a'
HERE = SCR + '/out/code_k_sahol_a'
SPLIT = pd.Timestamp('2021-01-01')
LAST_SHARED = pd.Timestamp('2026-10-30')
A, B = 'SAHOL', 'AKBNK'

# ---------------------------------------------------------------- spot
def use_new_data():
    """ll'yi güncel indirmeye (dl_k_sahol_a/daily + 03.11 son satır) yönlendirir. Ortak veriye dokunmaz."""
    ll.BASE = NEW; ll._cache.clear()
    extra = NEW + '/daily_last.parquet'
    if os.path.exists(extra):
        E = pd.read_parquet(extra); E['v'] = E['v'].fillna(0).clip(lower=1)   # endeks barında v=0 gelebiliyor; takvim (v>0) için yer tutucu
        for sym, g in E.groupby('sym'):
            d = ll.raw(sym).copy(); g = g.drop(columns='sym')
            d = d[~d['ldate'].isin(g['ldate'])]
            ll._cache[(sym, 'daily')] = pd.concat([d, g]).sort_index()

def signal(last=None, win=60, bwin=250, beta1=False):
    rA, rB = ll.ret(A), ll.ret(B)
    if last is not None: rA, rB = rA[rA.index <= last], rB[rB.index <= last]
    idx = rA.index.intersection(rB.index); rA, rB = rA.reindex(idx), rB.reindex(idx)
    beta = pd.Series(1.0, index=idx) if beta1 else (rA.rolling(bwin, min_periods=bwin // 2).cov(rB) / rB.rolling(bwin, min_periods=bwin // 2).var()).shift(1)
    s = rA - beta * rB; S = s.fillna(0).cumsum()
    z = (S - S.rolling(win, min_periods=win // 2).mean()) / S.rolling(win, min_periods=win // 2).std()
    return pd.DataFrame({'rA': rA, 'rB': rB, 'beta': beta, 'S': S, 'z': z})

def spot_px(sym, last=None):
    d = ll.raw(ll.T(sym)).copy(); d.index = pd.DatetimeIndex(d['ldate'].values); d = d[~d.index.duplicated(keep='last')]
    if last is not None: d = d[d.index <= last]
    return d

def bist_tick(p):
    """BIST pay piyasası fiyat adımı (2014+ tablo)."""
    p = np.asarray(p, float)
    return np.select([p < 20, p < 50, p < 100, p < 250, p < 500, p < 1000, p < 2500], [0.01, 0.02, 0.05, 0.10, 0.25, 0.50, 1.00], 2.50)

# ---------------------------------------------------------------- VİOP
_P = None
def panel():
    global _P
    if _P is None:
        cols = ['date', 'code', 'root', 'ctype', 'expiry', 'settle', 'prev_settle', 'open', 'close', 'vwap', 'value_tl', 'qty', 'trades', 'oi']
        p = pd.read_parquet(SCR + '/data/viop_panel.parquet', columns=cols)
        if os.path.exists(NEW + '/viop_new.parquet'):
            q = pd.read_parquet(NEW + '/viop_new.parquet', columns=cols); q = q[q.date > p.date.max()]
            p = pd.concat([p.astype({c: str for c in ['code', 'root', 'ctype']}), q.astype({c: str for c in ['code', 'root', 'ctype']})], ignore_index=True)
        for c in ['code', 'root', 'ctype']: p[c] = p[c].astype(str)
        p = p[p.ctype == 'D_EQ_FPD'].copy(); p['date'] = pd.to_datetime(p.date); p['expiry'] = pd.to_datetime(p.expiry)
        _P = p
    return _P

def cont(root, R=1):
    """Sürekli seri: t kapanışında tutulacak sözleşme = vadeye > R iş günü olan en yakın vade.
    Çıktı (index=VİOP günleri): hold (t kapanışından itibaren tutulan kod), F (hold'un t uzlaşması),
    r (t-1'de tutulan sözleşmenin t getirisi = log settle_t/settle_{t-1}), dF (TL fark), roll (hold_t != hold_{t-1}), value_tl/trades (hold sözleşmesi)."""
    p = panel(); DATES = np.array(sorted(p.date.unique()))
    d = p[(p.root == root) & (p.expiry >= p.date)].copy()
    # panel sonundan sonraki vadeler için takvimi hafta içi günlerle uzat (aksi halde son günlerde bdl küçük çıkar)
    ext = pd.bdate_range(pd.Timestamp(DATES[-1]) + pd.Timedelta(days=1), max(d.expiry.max(), pd.Timestamp(DATES[-1]))).values.astype(DATES.dtype)
    CAL = np.concatenate([DATES, ext])
    d['bdl'] = np.searchsorted(CAL, d.expiry.values) - np.searchsorted(CAL, d.date.values)
    px = d.set_index(['date', 'code'])['settle']
    pv = d.set_index(['date', 'code'])['prev_settle']
    h = d[d.bdl > R].sort_values(['date', 'expiry']).groupby('date').head(1).set_index('date')
    h = h.reindex(pd.DatetimeIndex(DATES)).dropna(subset=['code'])
    out = pd.DataFrame(index=h.index)
    out['hold'] = h['code']; out['F'] = h['settle']; out['value_tl'] = h['value_tl']; out['trades'] = h['trades']; out['expiry'] = h['expiry']
    prev_code = out['hold'].shift(1)
    keys = list(zip(out.index, prev_code))
    s_now = np.array([px.get(k, np.nan) if isinstance(k[1], str) else np.nan for k in keys])
    s_prev = out['F'].shift(1).values
    # yedek: önceki gün uzlaşması bültende prev_settle olarak da var
    pv_now = np.array([pv.get(k, np.nan) if isinstance(k[1], str) else np.nan for k in keys])
    s_prev = np.where(np.isnan(s_prev), pv_now, s_prev)
    out['Fprev_held'] = s_prev; out['Fnow_held'] = s_now
    out['r'] = np.log(s_now / s_prev); out['dF'] = s_now - s_prev
    out.loc[(out['r'].abs() > np.log(1.25)), ['r', 'dF']] = np.nan   # bariz veri hatası
    out['roll'] = (out['hold'] != prev_code) & prev_code.notna()
    return out

# ---------------------------------------------------------------- kural motoru
def run_rule(z, rA, rB, beta, cA, cB, roll=None, thr=1.5, exit_z=1.5, maxN=None, hold=None, stop=None, lag=0, fixed_beta=True):
    """Kapanıştan kapanışa durum makinesi. Tüm seriler aynı index (gün t). z_t t kapanışında bilinir.
    rA/rB: t-1 -> t getirisi (bacak). cA/cB: bacak başına GİDİŞ-DÖNÜŞ maliyet (oran, ör. 0.0008) serisi.
    Her işlem bir 'bölüm'e (|z|>thr ve aynı işaretli kesintisiz günler) en fazla bir kez girer.
    Çıkış: side*z >= -exit_z (z eşiğe döndü) | gün>=maxN | gün==hold (sabit tutma; z yok sayılır) | kümülatif brüt <= -stop.
    lag=1: karar t'de, uygulama t+1 uzlaşmasında (z bir gün kaydırılır)."""
    z = z.shift(lag) if lag else z
    zz = z.values; ra = np.nan_to_num(rA.values); rb = np.nan_to_num(rB.values); bb = beta.ffill().values
    ca = cA.values; cb = cB.values; rl = roll.values if roll is not None else np.zeros(len(zz), bool)
    n = len(zz); ep = np.where(np.abs(zz) > thr, np.sign(zz), 0.0); ep[np.isnan(zz)] = 0
    epid = np.zeros(n, int); k = 0
    for i in range(n):
        if ep[i] != 0 and (i == 0 or ep[i] != ep[i - 1]): k += 1
        epid[i] = k if ep[i] != 0 else 0
    pos = np.zeros(n); bh = np.zeros(n); gross = np.zeros(n); cost = np.zeros(n); tid = np.full(n, -1)
    trades = []; side = 0.0; b = np.nan; last_ep = 0; held = 0; cum = 0.0; cur = -1
    for i in range(n):
        # 1) t-1'den taşınan pozisyonun t getirisi
        if side != 0:
            g = side * (ra[i] - b * rb[i]); gross[i] = g; cum += g; held += 1; tid[i] = cur
            trades[cur]['gross'] += g
            if rl[i]:
                c_ = (ca[i] + abs(b) * cb[i]); cost[i] += c_; trades[cur]['cost'] += c_; trades[cur]['nroll'] += 1   # devir: her bacakta tam gidiş-dönüş
        # 2) t kapanışında çıkış kararı
        if side != 0:
            ex = False; why = ''
            if hold is not None:
                if held >= hold: ex, why = True, 'sure'
            else:
                if not np.isnan(zz[i]) and side * zz[i] >= -exit_z: ex, why = True, 'z'
                if maxN is not None and held >= maxN and not ex: ex, why = True, 'maxN'
            if stop is not None and cum <= -stop and not ex: ex, why = True, 'stop'
            if ex:
                c_ = (ca[i] + abs(b) * cb[i]) / 2; cost[i] += c_; trades[cur]['cost'] += c_
                trades[cur].update(exit=i, days=held, why=why)
                side = 0.0
        # 3) giriş kararı
        if side == 0 and ep[i] != 0 and epid[i] != last_ep and not np.isnan(bb[i]):
            side = -ep[i]; b = bb[i]; last_ep = epid[i]; held = 0; cum = 0.0
            c_ = (ca[i] + abs(b) * cb[i]) / 2; cost[i] += c_; cur = len(trades)
            trades.append(dict(entry=i, side=side, beta=b, z_in=zz[i], gross=0.0, cost=c_, nroll=0))
        if not fixed_beta and side != 0: b = bb[i]
        pos[i] = side; bh[i] = b if side != 0 else np.nan
    idx = z.index
    D = pd.DataFrame({'pos': pos, 'beta_h': bh, 'gross': gross, 'cost': cost, 'tid': tid}, index=idx)
    D['net'] = D.gross - D.cost
    D['exp'] = (D.pos.shift(1).fillna(0) != 0) | (D.pos != 0)
    T = pd.DataFrame(trades)
    if len(T):
        if 'exit' not in T: T['exit'] = np.nan; T['days'] = np.nan; T['why'] = ''
        T['open'] = T['exit'].isna(); T['exit'] = T['exit'].fillna(n - 1).astype(int); T['days'] = T['days'].fillna(held)
        T['net'] = T['gross'] - T['cost']; T['entry_date'] = idx[T.entry.values]; T['exit_date'] = idx[T.exit.values]
    return D, T

# ---------------------------------------------------------------- istatistik
def nw_t(x, lags=5):
    x = pd.Series(x).dropna().values; n = len(x)
    if n < 10: return np.nan, np.nan
    m = x.mean(); e = x - m; s = (e @ e) / n
    for L in range(1, lags + 1): s += 2 * (1 - L / (lags + 1)) * (e[L:] @ e[:-L]) / n
    se = np.sqrt(s / n); return m, (m / se if se > 0 else np.nan)

def summ(D, T, lo, hi):
    lo, hi = pd.Timestamp(lo), pd.Timestamp(hi)
    d = D[(D.index >= lo) & (D.index < hi)]
    t = T[(T.entry_date >= lo) & (T.entry_date < hi) & (~T.open)] if len(T) else T
    yrs = max((d.index[-1] - d.index[0]).days / 365.25, 1e-9) if len(d) else np.nan
    if len(t) < 5: return dict(n=len(t))
    _, td = nw_t(d.net.values)
    tt = t.net.mean() / t.net.std() * np.sqrt(len(t))
    cum = d.net.cumsum(); mdd = (cum - cum.cummax()).min()
    los = (t.net < 0).astype(int).values; ms = 0; c = 0
    for v in los: c = c + 1 if v else 0; ms = max(ms, c)
    return dict(n=len(t), per_yr=len(t) / yrs, hold_mean=t.days.mean(), hold_med=t.days.median(),
                gross_bps=1e4 * t.gross.mean(), net_bps=1e4 * t.net.mean(), med_bps=1e4 * t.net.median(), hit=(t.net > 0).mean(),
                t_trade=tt, t_daily=td, ann_bps=1e4 * d.net.sum() / yrs, frac_exp=d.exp.mean(),
                mdd_bps=1e4 * mdd, worst_bps=1e4 * t.net.min(), best_bps=1e4 * t.net.max(), p5_bps=1e4 * t.net.quantile(0.05), max_lstreak=ms,
                sh=(d.net.mean() / d.net.std() * np.sqrt(252)) if d.net.std() > 0 else np.nan)
