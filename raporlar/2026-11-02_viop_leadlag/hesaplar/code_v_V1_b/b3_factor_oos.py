"""b3: (1) ortak faktör kontrolü, (2) başka piyasa plasebosu (TR olay tarihleri diğer GOP'lara), (3) 2000-2013 gerçek örneklem dışı olaylar, (4) görünüm olayları."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vb import *
cal = bist_cal(); N = len(cal)
def lc(sym, col='c'):
    d = load(sym); s = d[col] if col in d else d['c']; return np.log(s.where(s > 0))
XU = {s: (np.log(load(s).o.reindex(cal)).values, lc(s).reindex(cal).values) for s in ['XU100.IS', 'XU030.IS', 'XBANK.IS']}
ev = ev_load(('rating',))
def mk(df):
    df = df.copy(); df['i0'] = [react_idx(cal, a, f) for a, f in zip(df.ann, df.after_close)]
    return df.drop_duplicates('i0').reset_index(drop=True)
post = mk(ev[ev.period == 'post']); pre = mk(ev[ev.period == 'pre'])
COST = 15e-4

print('=== (1) Ortak faktör kontrolü: XU100 c[t0]->c[t+2] (işlenebilir kapanış girişi) ve c[t0-1]->c[t+2] ===')
fac = {}
for f in ['^STOXX50E', 'EEM', 'ES=F']:
    s = lc(f, 'adj' if f == 'EEM' else 'c'); s = s.reindex(s.index.union(cal)).ffill().reindex(cal)
    fac[f] = np.diff(s.values, prepend=np.nan)
rX = np.diff(XU['XU100.IS'][1], prepend=np.nan)
def fac_adj(i0s, dirs, a, b, lab):
    """pencere: gün a..b (dahil) cc getirileri, kontrol: STOXX_t, EEM_t, EEM_{t-1}; beta [i-260, i-6]"""
    out = []
    for i, dr in zip(i0s, dirs):
        y = rX[i - 260:i - 5]
        Z = np.column_stack([np.ones(len(y)), fac['^STOXX50E'][i - 260:i - 5], fac['EEM'][i - 260:i - 5], fac['EEM'][i - 261:i - 6]])
        m = np.isfinite(y) & np.isfinite(Z).all(1); bb = np.linalg.lstsq(Z[m], y[m], rcond=None)[0]
        days = np.arange(i + a, i + b + 1)
        pred = bb[1] * np.nansum(fac['^STOXX50E'][days]) + bb[2] * np.nansum(fac['EEM'][days]) + bb[3] * np.nansum(fac['EEM'][days - 1])
        raw = np.nansum(rX[days]); out.append((-dr * raw, -dr * (raw - pred), -dr * pred))
    o = np.array(out)
    print(fmt(o[:, 0] - COST, f'{lab} ham')); print(fmt(o[:, 1] - COST, f'{lab} faktör-ayarlı')); print(fmt(o[:, 2], f'{lab} faktörün açıkladığı kısım'))
fac_adj(post.i0.values, post.dir.values, 1, 2, 'close->t+2')
fac_adj(post.i0.values, post.dir.values, 0, 2, 'pc->t+2')

print('\n--- TUR (USD) vs EEM aynı saat: Pzt açılış -> Çar kapanış, beta 250g ---')
def us_win(sym, i0s, h=2, col='adj'):
    d = load(sym); o = np.log(d.o * (d.adj / d.c)); c = np.log(d.adj); idx = d.index; res = []
    for i in i0s:
        j = idx.searchsorted(cal[i]);
        if j + h >= len(idx): res.append(np.nan); continue
        res.append(c.iloc[j + h] - o.iloc[j])
    return np.array(res)
def us_beta(sym, fsym, i0s):
    a = np.log(load(sym).adj).diff(); f = np.log(load(fsym).adj).diff(); df = pd.concat([a, f], axis=1, keys=['a', 'f']).dropna(); out = []
    for i in i0s:
        w_ = df[(df.index < cal[i]) & (df.index >= cal[i] - pd.Timedelta(days=365))]
        out.append(np.cov(w_.a, w_.f)[0, 1] / w_.f.var())
    return np.array(out)
tur = us_win('TUR', post.i0.values); eem = us_win('EEM', post.i0.values); bt = us_beta('TUR', 'EEM', post.i0.values)
d_ = post.dir.values
print(fmt(-d_ * tur - COST, 'TUR ham')); print(fmt(-d_ * (tur - bt * eem) - COST, 'TUR - beta*EEM')); print(fmt(-d_ * eem, 'EEM (TR yönüyle işaretli)'))
print('ortalama beta TUR/EEM', bt.mean().round(2))

print('\n=== (2) Başka piyasa plasebosu: TR olay tarihleri/yönleri diğer piyasalara (Pzt açılış -> t+2 kapanış, brüt) ===')
rows = []
for sym in ['EEM', 'EZA', 'EWZ', 'EWW', 'EWY', 'EPOL', 'GREK', 'EWI', 'EWG', 'SPY', '^BVSP', '^MXX', '^J203.JO', '^JKSE', '^STOXX50E', '^GDAXI', 'FTSEMIB.MI']:
    try:
        d = load(sym); o = np.log(d.o.where(d.o > 0)); c = np.log(d.c.where(d.c > 0)); idx = d.index; v = []
        for i, dr in zip(post.i0.values, post.dir.values):
            j = idx.searchsorted(cal[i]);
            v.append(-dr * (c.iloc[j + 2] - o.iloc[j]) if j + 2 < len(idx) else np.nan)
        v = np.array(v); t, n = tstat(v); rows.append(dict(sym=sym, mean_bps=1e4 * np.nanmean(v), t=t, n=n))
    except Exception as e: rows.append(dict(sym=sym, err=str(e)[:40]))
R = pd.DataFrame(rows); print(R.round(2).to_string(index=False)); R.to_csv(HERE + '/res_b3_other_markets.csv', index=False)

print('\n=== (3) GERÇEK ÖRNEKLEM DIŞI: 2000-2013 not değişiklikleri (1. turda hiç kullanılmadı; açılış verisi bozuk -> kapanış girişleri) ===')
print(pre.assign(react=cal[pre.i0].date)[['ann', 'agency', 'dir', 'react', 'note']].to_string(index=False))
oC = XU['XU100.IS'][1]
def cwin(Cv, i0s, a, b): i0s = np.asarray(i0s); return Cv[i0s + b] - Cv[i0s + a]
for lab, df in [('PRE 2000-13', pre), ('PRE 2003-13 (2001 krizi hariç)', pre[pre.ann >= '2003-01-01']), ('PRE 2009-13', pre[pre.ann >= '2009-01-01']), ('POST 2016-25', post)]:
    i0s, dr = df.i0.values, df.dir.values
    print(f'-- {lab}: n={len(df)}, indirim {int((dr<0).sum())}, artırım {int((dr>0).sum())}')
    for nm, a, b in [('A: c[t0]->c[t+2] (kesin işlenebilir)', 0, 2), ('A5: c[t0]->c[t+5]', 0, 5), ('pc: c[t0-1]->c[t+2]', -1, 2), ('B: c[ann günü]->c[+2] (saat bilinmiyor)', -1, 1), ('t0 tepki c[t0-1]->c[t0]', -1, 0)]:
        for s in ['XU100.IS', 'XBANK.IS']:
            v = -dr * cwin(XU[s][1], i0s, a, b) - (COST if nm[0] in 'AB' or nm[:2] == 'pc' else 0)
            print('   ' + fmt(v, f'{s[:5]} {nm}'))
# 2000-13 placebo (tarih kaydırma) for A
rng = np.random.default_rng(7)
i0s, dr = pre.i0.values, pre.dir.values
real = (-dr * cwin(oC, i0s, 0, 2)).mean()
ks = np.r_[-52:-2, 3:53]; pl = []
for b in range(5000):
    I = np.array([int(cal.searchsorted(cal[i] + pd.Timedelta(days=7 * k))) for i, k in zip(i0s, rng.choice(ks, len(i0s)))])
    pl.append(np.nanmean(-dr * cwin(oC, I, 0, 2)))
pl = np.array(pl); print(f'PRE A plasebo: gerçek {1e4*real:+.1f} bps brüt, plasebo ort {1e4*pl.mean():+.1f}, p(tek yönlü)={(pl>=real).mean():.3f}')
# Yahoo TUR for 2009-13 pre events
p9 = pre[pre.ann >= '2009-01-01']
tv = us_win('TUR', p9.i0.values); print(fmt(-p9.dir.values * tv - COST, 'TUR (USD) PRE 2009-13 açılış->t+2'))
# tümü: pre + post (A tanımı)
allv = np.r_[-pre.dir.values * cwin(oC, pre.i0.values, 0, 2), -post.dir.values * cwin(oC, post.i0.values, 0, 2)] - COST
print(fmt(allv, 'TÜM 2000-2025 A: c[t0]->c[t+2]'))
T = pd.concat([pre.assign(per='pre'), post.assign(per='post')])
T['react'] = cal[T.i0]; T['A_bps'] = 1e4 * (-T.dir * (oC[T.i0 + 2] - oC[T.i0]))
T['react_bps'] = 1e4 * (-T.dir * (oC[T.i0] - oC[T.i0 - 1]))
T[['ann', 'agency', 'dir', 'per', 'react', 'react_bps', 'A_bps', 'note']].to_csv(HERE + '/res_b3_events_all.csv', index=False)
print(T[T.per == 'pre'][['ann', 'agency', 'dir', 'react', 'react_bps', 'A_bps']].round(0).to_string(index=False))

print('\n=== (4) Görünüm / izleme olayları (mekanizma testi) ===')
ol = ev_load(('outlook', 'review')); ol = mk(ol)
v = -ol.dir.values * (XU['XU100.IS'][1][ol.i0 + 2] - XU['XU100.IS'][0][ol.i0]) - COST
print(fmt(v, 'görünüm: açılış->t+2 kontraryen')); print(fmt(-ol.dir.values * cwin(oC, ol.i0.values, -1, 0), 'görünüm: t0 tepki (işaretli, kontra)'))
print(fmt(-post.dir.values * cwin(oC, post.i0.values, -1, 0), 'not değişikliği: t0 tepki c->c (işaretli, kontra)'))
