"""(7) Ay dönümü XU030D1! ve (6) temettü öncesi (spot ve VİOP) — bağımsız yeniden hesap."""
from curlib import *
cal = vcal(); FW = pd.read_parquet(RES + '/_fwd_cache.parquet'); SR = pd.read_parquet(RES + '/_spot_ret.parquet')
def fw(u, h, e): return FW[f'{u}|{h}|{e}']
out = []
# ================= Ay dönümü =================
c = cal.to_series()
me = c.groupby([c.index.year, c.index.month]).max().values  # VİOP takviminde ayın son işlem günü
me = pd.DatetimeIndex(me); me = me[me < cal[-1]]
for h in [1, 2, 3]:
    for e in ['E0', 'E1', 'E2']:
        x = fw('XU030', h, e).reindex(me).values
        o = summary(me, x, h, cost=4.8); reg('ay', 'Ay sonu AL XU030D1!', h, e, o); out.append(f'Ay sonu AL XU030D1! {e} h{h}: {fmt(o)}')
# plasebo: diğer tüm günler ve rastgele 1000 set
yy = fw('XU030', 1, 'E0')
others = cal.difference(me); others = others[(others >= me.min()) & (others <= me.max())]
print(f'Diğer günler ort h1 E0: {np.nanmean(yy.reindex(others)) * 1e4:+.1f} bps; ay sonu: {np.nanmean(yy.reindex(me)) * 1e4:+.1f}')
pb = placebo_dates(me, np.ones(len(me)), lambda q: yy.reindex(q).values, others, nrep=2000, seed=5)
print(f'Plasebo rastgele gün (n={len(me)}): %95 {np.percentile(pb, 95):+.1f} %99 {np.percentile(pb, 99):+.1f}; p={np.mean(pb >= np.nanmean(yy.reindex(me)) * 1e4):.3f}')
# komşu günler (ME−2..ME+2) — tekil gün mü, dönem mi?
pos = cal.get_indexer(me)
for k in [-3, -2, -1, 0, 1, 2]:
    dd = cal[np.clip(pos + k, 0, len(cal) - 1)]
    o = summary(dd, yy.reindex(dd).values, 1); out.append(f'ME{k:+d} günü al (h1 E0): brüt {o["gross"]:+.1f} t {o["t"]:.2f} yıl+ {o["yrs"]} top10 hariç {o.get("ex_top10", np.nan):+.1f}')
    reg('ay', f'ME{k:+d} h1', 1, 'E0', o)
# spot XU100 2005+ (bilgi; spot kapanış dolumu kullanıcıya geçersiz)
rx = spot_ret('XU100'); sc_ = rx.index.to_series(); mes = pd.DatetimeIndex(sc_.groupby([sc_.index.year, sc_.index.month]).max().values)
mes = mes[(mes >= '2005-01-01') & (mes < rx.index[-1])]
o = summary(mes, spot_fwd(rx, 1).reindex(mes).values, 1, is_end='2020-12-31'); reg('ay', 'SPOT XU100 ay sonu', 1, 'S', o)
out.append(f'SPOT XU100 ay sonu (2005+) h1: {fmt(o)}')
# ================= Temettü =================
L = pd.read_csv(S + '/out/y_viop_likidite.csv'); U = [u for u in L.und if u != 'XU030']
ev = []
for u in U:
    try: d = spot(u)
    except Exception: continue
    k = (d['adj'] / d['c']).dropna()
    ratio = (k.shift(1) / k)  # ex-gününde k sıçrar: k_{ex-1}/k_ex = 1 − D/P
    y = 1 - ratio
    ex = y[(y > 0.002) & (y < 0.5)]
    for dt, yy_ in ex.items(): ev.append(dict(und=u, ex=dt, yld=yy_))
EV = pd.DataFrame(ev); EV = EV[EV.ex >= '2010-01-01']
print('temettü olayı', len(EV), 'yüksek verim (≥%4)', int((EV.yld >= 0.04).sum()))
rx = SR['XU100']
def spot_window(u, ex, a, b):
    r = SR[u]; idx = r.index; i = idx.get_indexer([ex])[0]
    if i < 0 or i + b >= len(idx) or i + a < 0: return np.nan
    return r.iloc[i + a + 1:i + b + 1].sum() - rx.reindex(idx[i + a + 1:i + b + 1]).sum()
for lab, sub in [('tümü', EV), ('verim≥%4', EV[EV.yld >= 0.04])]:
    # spot: E−4 kapanış -> E−1 kapanış (fazla getiri XU100)
    xs = np.array([spot_window(r.und, r.ex, -4, -1) for r in sub.itertuples()])  # r[i-3..i-1] = E−4 kapanışından E−1 kapanışına
    ds = pd.DatetimeIndex(sub.ex)
    o = summary(ds, xs, 3, is_end='2020-12-31'); reg('tem', f'SPOT temettü öncesi {lab}', 3, 'S', o); out.append(f'SPOT E−4→E−1 {lab}: {fmt(o)}')
    s17 = ds >= '2017-01-01'; o = summary(ds[s17], xs[s17], 3, is_end='2021-12-31'); reg('tem', f'SPOT temettü öncesi {lab} 2017+', 3, 'S', o); out.append(f'SPOT E−4→E−1 {lab} 2017+: {fmt(o)}')
    # VİOP: E−4 uzlaşma -> E−1 uzlaşma (h=3), sinyal tarihi = E−4 (VİOP takviminde)
    pos = cal.get_indexer(ds, method='bfill'); okp = (pos >= 4)
    dE4 = cal[pos[okp] - 4]; uu = sub.und.values[okp]
    xv = np.array([fw(u_, 3, 'E0').get(d_, np.nan) for u_, d_ in zip(uu, dE4)])
    o = summary(dE4, xv, 3); reg('tem', f'VİOP temettü öncesi {lab}', 3, 'E0', o); out.append(f'VİOP E−4→E−1 {lab}: {fmt(o)}')
for o_ in out: print(o_)
save('ay'); save('tem')
