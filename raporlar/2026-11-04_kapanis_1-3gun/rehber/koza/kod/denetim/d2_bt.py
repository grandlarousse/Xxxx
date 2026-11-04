"""(2) BAĞIMSIZ pratik kural backtest'i (curlib/kl/k2 import EDİLMEZ). VİOP bülten uzlaşmaları; sinyal bag.py.
Kural (REHBER §1.2 metninden): pozisyon yokken |z3|>thr -> yön; giriş t uzlaşması; planlı çıkış t+h; çıkış günü aynı yönde aktifse +h uzat
(toplam ≤ maxh); ters sinyalde çık+çevir; cap dolunca çık ve bant içine dönene dek aynı yöne girme; kilit günü giriş yok.
Vade: segment başında, vadesi segment sonundan KESİN sonra olan en yakın listelenmiş vade; değişirse devir (+1 gidiş-dönüş maliyet)."""
import sys, numpy as np, pandas as pd
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/denetim_koza/kod')
import bag
S = '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad'
OUT = S + '/denetim_koza'
cols = ['date', 'code', 'und', 'segment', 'expiry', 'settle', 'prev_settle', 'high', 'low', 'close', 'trades', 'oi']
A = pd.read_parquet(S + '/data/viop_panel.parquet', columns=cols); Bn = pd.read_parquet(S + '/dl_k_sahol_a/viop_new.parquet', columns=cols)
for X in (A, Bn):
    for c in ['code', 'und', 'segment']: X[c] = X[c].astype(str)
    X['date'] = pd.to_datetime(X.date); X['expiry'] = pd.to_datetime(X.expiry)
CAL = pd.DatetimeIndex(sorted(set(A.date) | set(Bn.date)))
P = pd.concat([A, Bn[Bn.date > A.date.max()]], ignore_index=True)
P = P[P.und.isin(['TRMET', 'TRALT']) & (P.segment == 'SSF') & (P.settle > 0) & (P.expiry >= P.date)]
P = P.sort_values(['und', 'expiry', 'date', 'oi', 'trades']).drop_duplicates(['und', 'expiry', 'date'], keep='last')
P['r'] = np.log(P.settle / P.prev_settle)
N = len(CAL); ci = {d: k for k, d in enumerate(CAL)}


class Leg:
    def __init__(self, und):
        g = P[P.und == und]
        self.ex = np.array(sorted(g.expiry.unique()))
        self.ST = g.pivot(index='date', columns='expiry', values='settle').reindex(index=CAL, columns=self.ex).values
        self.R = g.pivot(index='date', columns='expiry', values='r').reindex(index=CAL, columns=self.ex).values
        # ön vade (vade >= gün) günlük basit getiri -> kilit vekili
        fr = np.full(N, np.nan)
        for k in range(N):
            j = np.searchsorted(self.ex, CAL.values[k], side='left')
            while j < len(self.ex) and not np.isfinite(self.ST[k, j]): j += 1
            if j < len(self.ex): fr[k] = self.R[k, j]
        self.front_r = fr

    def pick(self, i, end):
        j = np.searchsorted(self.ex, CAL.values[end], side='right')  # vade > çıkış (kesin)
        while j < len(self.ex) and not np.isfinite(self.ST[i, j]): j += 1
        return j if j < len(self.ex) else -1

    def seg(self, i, end, j):
        rr = self.R[i + 1:end + 1, j]
        return rr.sum() if np.all(np.isfinite(rr)) else np.nan, int(np.isfinite(rr).sum())


LM, LA = Leg('TRMET'), Leg('TRALT')


def lock_vec(kind='builder'):
    if kind == 'builder':   # |log r| > ln 1,095 (alt eşik ≈ −%8,7)
        return (np.abs(LM.front_r) > np.log(1.095)) | (np.abs(LA.front_r) > np.log(1.095))
    if kind == 'simetrik':  # basit getiri ±%9,5
        f = lambda r: (np.exp(r) - 1 >= 0.095) | (np.exp(r) - 1 <= -0.095)
        return f(LM.front_r) | f(LA.front_r)
    return np.zeros(N, bool)


def simulate(sig, legs=(LM, LA), thr=1.5, h=2, maxh=6, extend=True, lag=0, lock='builder', start='2018-12-17'):
    z = sig.z3.reindex(CAL).values.copy(); b = sig.bH.reindex(CAL).values.copy()
    if lag: z = np.r_[np.full(lag, np.nan), z[:-lag]]; b = np.r_[np.full(lag, np.nan), b[:-lag]]
    act = np.where(np.isfinite(z) & (np.abs(z) > thr), np.sign(z), 0)
    L = lock_vec(lock); i0 = int(np.searchsorted(CAL.values, np.datetime64(start)))
    trades = []; pos = None; block = 0
    for i in range(i0, N):
        if pos is not None and i == pos['end']:
            if extend and act[i] == pos['s'] and (pos['end'] - pos['i0']) + h <= maxh and i + h < N:
                pos['segs'].append(i); pos['end'] = i + h; continue
            pos['cap'] = bool(act[i] == pos['s']); trades.append(pos)
            block = pos['s'] if pos['cap'] else 0; pos = None
        if pos is None:
            if block and act[i] != block: block = 0
            if act[i] != 0 and act[i] != block and i + h < N and not L[i] and np.isfinite(b[i]):
                pos = dict(i0=i, s=act[i], b=b[i], z=z[i], segs=[i], end=i + h)
    open_pos = pos
    rows = []
    for p in trades:
        bb = p['b']; tot1 = tot2 = 0.0; nroll = 0; jprev = None; segr = []; miss = 0
        for k, s0 in enumerate(p['segs']):
            e = p['segs'][k + 1] if k + 1 < len(p['segs']) else p['end']
            j1, j2 = legs[0].pick(s0, e), legs[1].pick(s0, e)
            if j1 < 0 or j2 < 0: tot1 = np.nan; break
            if jprev is not None and (j1, j2) != jprev: nroll += 1
            jprev = (j1, j2)
            r1, _ = legs[0].seg(s0, e, j1); r2, _ = legs[1].seg(s0, e, j2)
            if not (np.isfinite(r1) and np.isfinite(r2)): miss += 1
            tot1 += r1; tot2 += r2; segr.append(p['s'] * (r1 - bb * r2) / (1 + bb) * 1e4)
        j1, j2 = legs[0].pick(p['i0'], p['segs'][1] if len(p['segs']) > 1 else p['end']), legs[1].pick(p['i0'], p['segs'][1] if len(p['segs']) > 1 else p['end'])
        P1 = legs[0].ST[p['i0'], j1] if j1 >= 0 else np.nan; P2 = legs[1].ST[p['i0'], j2] if j2 >= 0 else np.nan
        g = p['s'] * (tot1 - bb * tot2) / (1 + bb) * 1e4
        tick = 2 * (0.01 / P1 / (1 + bb) + bb * 0.01 / P2 / (1 + bb)) * 1e4 * (1 + nroll)
        rows.append(dict(entry=CAL[p['i0']], exit=CAL[p['end']], days=p['end'] - p['i0'], side=p['s'], beta=bb, z=p['z'], gross=g,
                         nroll=nroll, tick=tick, cap=p['cap'], segs=segr, miss=miss, P1=P1, P2=P2))
    T = pd.DataFrame(rows)
    T['net8'] = T.gross - 8 * (1 + T.nroll); T['net15'] = T.gross - 15 * (1 + T.nroll)
    T['net8t'] = T.net8 - T.tick; T['net15t'] = T.net15 - T.tick
    return T, open_pos


def tt(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan


def streak(x):
    m = c = 0
    for v in x:
        c = c + 1 if v < 0 else 0; m = max(m, c)
    return m


def stats(T, label=''):
    nan_n = int(T.gross.isna().sum()); T = T.dropna(subset=['gross'])
    yrs = (T.exit.max() - T.entry.min()).days / 365.25
    cs = T.net15t.cumsum().values; dd = cs - np.maximum.accumulate(np.r_[0, cs])[1:]
    cs8 = T.net8.cumsum().values; dd8 = cs8 - np.maximum.accumulate(np.r_[0, cs8])[1:]
    o = dict(label=label, n=len(T), nan=nan_n, per_yr=len(T) / yrs, days=T.days.mean(), ext=(T.days > T.days.min()).mean() if len(T) else np.nan,
             gross=T.gross.mean(), t=tt(T.gross), hit=(T.gross > 0).mean(), sd=T.gross.std(), net8=T.net8.mean(), net15=T.net15.mean(),
             tick=T.tick.mean(), net8t=T.net8t.mean(), net15t=T.net15t.mean(), rolls=int(T.nroll.sum()),
             worst=T.gross.min(), worst_d=T.loc[T.gross.idxmin(), 'entry'].date(), best=T.gross.max(), mdd8=dd8.min(), mdd15t=dd.min(), streak=streak(T.gross.values))
    for lab, a, b in [('IS', '2019', '2021-12-31'), ('OOS', '2022', '2026-12-31'), ('y2426', '2024', '2026-12-31')]:
        m = (T.entry >= a) & (T.entry <= b)
        o[lab] = T.gross[m].mean(); o[lab + '_t'] = tt(T.gross[m]); o[lab + '_n'] = int(m.sum()); o[lab + '_n15t'] = T.net15t[m].mean()
    k = T.gross.sort_values(ascending=False).index[10:]; o['ex10'] = T.gross[k].mean(); o['ex10_t'] = tt(T.gross[k])
    yy = T.groupby(T.entry.dt.year).agg(g=('gross', 'mean'), n=('gross', 'size'), n15=('net15t', 'mean'))
    o['years'] = ' '.join(f"{y % 100:02d}:{r.g:+.0f}/{r.n15:+.0f}(n{r.n})" for y, r in yy.iterrows()); o['yrs_pos'] = f"{(yy.g > 0).sum()}/{len(yy)}"
    return o


def show(o):
    print(f"{o['label']}: n={o['n']} (NaN {o['nan']}) {o['per_yr']:.1f}/yıl tutma {o['days']:.2f} uzatma %{100*o['ext']:.0f} | brüt {o['gross']:+.1f} (t {o['t']:.2f}) isabet {o['hit']:.2f} σ {o['sd']:.0f} | "
          f"net8 {o['net8']:+.1f} net15 {o['net15']:+.1f} tik {o['tick']:.1f} net8t {o['net8t']:+.1f} net15t {o['net15t']:+.1f} devir {o['rolls']}\n"
          f"   IS {o['IS']:+.1f} (t {o['IS_t']:.2f}, n {o['IS_n']}) OOS {o['OOS']:+.1f} (t {o['OOS_t']:.2f}, n {o['OOS_n']}) 2024–26 {o['y2426']:+.1f} (t {o['y2426_t']:.2f}, n {o['y2426_n']}, net15t {o['y2426_n15t']:+.1f}) | "
          f"ex10 {o['ex10']:+.1f} (t {o['ex10_t']:.2f}) | en kötü {o['worst']:+.0f} ({o['worst_d']}) en iyi {o['best']:+.0f} | MDD net8 {o['mdd8']:.0f} net15t {o['mdd15t']:.0f} | kayıp serisi {o['streak']}\n"
          f"   yıllar brüt/net15t: {o['years']} (+{o['yrs_pos']})")


if __name__ == '__main__':
    SIG, _ = bag.signal(upto='2026-11-03')
    SIGA, _ = bag.signal(upto='2026-11-03', target='TRALT')
    print('VİOP takvimi', CAL[0].date(), '→', CAL[-1].date(), 'gün', N)
    res = []
    T0L, op = simulate(SIG); o = stats(T0L, 'P0L ana (kilit: kurucu vekili)'); show(o); res.append(o)
    T0L.to_csv(OUT + '/islemler_P0L_denetim.csv', index=False)
    print('   açık pozisyon (03.11 itibarıyla):', None if op is None else (CAL[op['i0']].date(), op['s']))
    # kurucu ile işlem bazında karşılaştırma
    K = pd.read_csv(S + '/out/rehber/koza/kod/islemler_P0L.csv', parse_dates=['entry', 'exit']).dropna(subset=['gross'])
    m = T0L.merge(K, on=['entry', 'exit', 'side'], how='outer', suffixes=('', '_k'), indicator=True)
    print('   kurucu P0L ile: ortak işlem', (m._merge == 'both').sum(), 'yalnız denetim', (m._merge == 'left_only').sum(), 'yalnız kurucu', (m._merge == 'right_only').sum(),
          '| ortak işlemde maks |Δbrüt|', f"{(m.gross - m.gross_k).abs().max():.3f}", 'maks |Δtik|', f"{(m.tick - m.tick_k).abs().max():.3f}")
    if ((m._merge != 'both')).any(): print(m[m._merge != 'both'][['entry', 'exit', 'side', 'gross', 'gross_k', '_merge']])
    # uzatma segmentleri
    seg1 = np.array([s[0] for s in T0L.segs]); later = np.array([v for s in T0L.segs for v in s[1:]])
    later_d = [T0L.entry[k] for k, s in enumerate(T0L.segs) for v in s[1:]]
    print(f'   ilk segment ort {np.nanmean(seg1):+.1f}; uzatma sonrası segmentler {np.nanmean(later):+.1f} (t {tt(later):.2f}, n {len(later)}, isabet {(later > 0).mean():.2f}); '
          f'uzatılmayan işlemler {T0L.gross[T0L.days == 2].mean():+.1f} (n {(T0L.days == 2).sum()})')
    for nm, kw in [('P0 (kilit kuralı yok)', dict(lock='none')), ('P0L simetrik ±%9,5 kilit vekili', dict(lock='simetrik')),
                   ('P1 sabit h2', dict(extend=False)), ('P2 gecikmeli (uzatmalı)', dict(lag=1)), ('P2b gecikmeli sabit h2', dict(lag=1, extend=False))]:
        T, _ = simulate(SIG, **kw); o = stats(T, nm); show(o); res.append(o)
    T, _ = simulate(SIGA, legs=(LA, LM)); o = stats(T, 'TERS P0L (TRALT artığı)'); show(o); res.append(o)
    T, _ = simulate(SIGA, legs=(LA, LM), lock='none'); o = stats(T, 'TERS P0 (kilitsiz)'); show(o); res.append(o)
    T, _ = simulate(SIGA, legs=(LA, LM), lag=1); o = stats(T, 'TERS P2 gecikmeli'); show(o); res.append(o)
    print('\n--- DUYARLILIK (P0L kilit kuralıyla) eşik × tutma; uzatmalı: +h uzat, en fazla 3h; sabit: uzatmasız ---')
    rows = []
    for thr in [1.25, 1.5, 1.75]:
        for h in [1, 2, 3]:
            for ext in [True, False]:
                T, _ = simulate(SIG, thr=thr, h=h, maxh=3 * h, extend=ext); o = stats(T, f'thr {thr} h{h} {"uzat" if ext else "sabit"}')
                rows.append(o)
                print(f"thr {thr:.2f} h{h} {'uzat≤'+str(3*h) if ext else 'sabit  '}: n {o['n']:3d} tutma {o['days']:.2f} brüt {o['gross']:+6.1f} (t {o['t']:.2f}) net15t {o['net15t']:+6.1f} | "
                      f"2024–26 {o['y2426']:+6.1f} (t {o['y2426_t']:.2f}) net15t {o['y2426_n15t']:+6.1f} | ex10 {o['ex10']:+6.1f} | MDD15t {o['mdd15t']:6.0f} | yıl+ {o['yrs_pos']}")
    pd.DataFrame(res + rows).drop(columns=[]).to_csv(OUT + '/res_denetim_bt.csv', index=False)
