"""V1 sağlamlık, plasebo, IS/OOS, maliyet. v1.py'deki kendi motorumu kullanır (ll.py yok)."""
import sys
sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_V1_a')
from v1 import *
from scipy import stats

rat = EV[EV.kind == 'rating'].copy()
r1 = rat[rat.react.isin(R1)].copy()
olk = EV[EV.kind.isin(['outlook', 'review'])].copy()
SETS = {'R1_19': r1, 'DUZ_20': rat}
out_rows = []
def rec(tag, v, cost=15, **kw):
    d = dict(tag=tag, **kw, **summarize(v, cost)); out_rows.append(d); return d

print('=== (c1) GİRİŞ / ÇIKIŞ DUYARLILIĞI (XU100, 15 bps) ===')
grid = []
for setn, ev in SETS.items():
    for sym in IDX:
        for entry in ['prevclose', 'open', 'close0', 'open1']:
            for k in [0, 1, 2, 3, 5, 10]:
                if entry in ('open1',) and k < 1: continue
                v = signed_returns(ev, sym, entry, k)
                d = summarize(v, 15 if entry != 'prevclose' else 0)
                grid.append(dict(set=setn, sym=sym, entry=entry, exit_k=k, **d))
G = pd.DataFrame(grid); G.to_csv(OUT + '/res_c1_entry_exit_grid.csv', index=False)
piv = G[(G.set == 'DUZ_20')].pivot_table(index=['sym', 'entry'], columns='exit_k', values='mean_bps')
print(piv.round(0).to_string())
pivt = G[(G.set == 'DUZ_20')].pivot_table(index=['sym', 'entry'], columns='exit_k', values='t')
print(pivt.round(2).to_string())

print('\n=== (c2) SAATLİK GİRİŞ (ilk bar kapanışı ≈10:30 TSİ) vs AÇILIŞ, 2024+ olaylar ===')
sub = rat[rat.react >= '2023-12-01']
for sym in IDX:
    a = signed_returns(sub, sym, 'open', 2); b = signed_returns(sub, sym, 'h1', 2)
    print(sym, 'açılış:', summarize(a), '| ilk saat:', summarize(b))
    print('   olay bazında (bps, maliyetsiz) açılış/ilksaat:', list(zip((1e4 * a).round(0).astype(int), (1e4 * b).round(0).astype(int))))
    rec('h1_entry_2024+', b, sym=sym)

print('\n=== (c3) USD bazlı ve XBANK - XU100 fazlası (açılış -> t+2) ===')
for setn, ev in SETS.items():
    print(setn, 'XU100 USD:', summarize(signed_returns(ev, 'XU100.IS', usd=True)))
    print(setn, 'XBANK-XU100 fazla:', summarize(signed_returns(ev, 'XBANK.IS', excess='XU100.IS'), 0))

print('\n=== (c4) ALT KÜMELER (DUZ_20, XU100, açılış->t+2, 15 bps) ===')
v = signed_returns(rat, 'XU100.IS')
meta = rat.set_index('react')
subsets = {
    'hepsi': v.index.notna(),
    'sadece Cuma açıklaması': (meta.wd == 'Fri').reindex(v.index).values,
    'hafta içi (takvim dışı)': (meta.wd != 'Fri').reindex(v.index).values,
    'indirimler (uzun)': (meta.dir == -1).reindex(v.index).values,
    'artırımlar (kısa)': (meta.dir == 1).reindex(v.index).values,
    'S&P': meta.agency.str.contains('SP').reindex(v.index).values,
    'Moody\'s': meta.agency.str.contains('MOODYS').reindex(v.index).values,
    'Fitch': meta.agency.str.contains('FITCH').reindex(v.index).values,
    '2016-07 ve 2018-08 hariç': ~v.index.isin(pd.to_datetime(['2016-07-21', '2018-08-20'])),
    't0-t2 arası tatil yok (2 takvim günü)': np.array([(CAL[int(i) + 2] - CAL[int(i)]).days == 2 for i in rat.react_i]),
}
for nm, m in subsets.items():
    print(f'{nm:40s}', summarize(v[m])); rec('subset', v[m], sub=nm)
# en iyi/kötü olay çıkarılınca
loo = [summarize(v.drop(d))['t'] for d in v.index]
print('leave-one-out t aralığı:', min(loo), max(loo))
vv = v - 15e-4
print('Wilcoxon p (iki yönlü):', round(stats.wilcoxon(vv).pvalue, 4), '| işaret testi p:', round(stats.binomtest(int((vv > 0).sum()), len(vv)).pvalue, 4))
bs = [rng.choice(vv.values, len(vv)).mean() for _ in range(20000)]
print('bootstrap %95 GA (bps):', np.round(1e4 * np.percentile(bs, [2.5, 97.5]), 0))
# en büyük 3 olayın payı
srt = vv.sort_values(ascending=False)
print('en büyük 3 olay (bps):', (1e4 * srt.head(3)).round(0).to_dict(), '| bunlar hariç ort:', round(1e4 * srt.iloc[3:].mean(), 1), 't', round(tstat(srt.iloc[3:])[0], 2))

print('\n=== (c5) GÖRÜNÜM/İZLEME olayları ve tümü (aynı tepki gününde yönler toplanır) ===')
def collapse(ev):
    g = ev.groupby('react').agg(dir=('dir', 'sum'), react_i=('react_i', 'first'), n=('dir', 'size')).reset_index()
    g['dir'] = np.sign(g['dir']); return g[g.dir != 0]
for nm, ev in [('görünüm/izleme', olk), ('görünüm (1.turdaki 13)', olk[~olk.note.str.contains('1. turda yok')]), ('not+görünüm', EV)]:
    ev2 = collapse(ev)
    for sym in ['XU100.IS', 'XBANK.IS']:
        for k in [0, 2, 5]:
            s = signed_returns(ev2, sym, 'open', k)
            d = summarize(s); print(f'{nm:24s} {sym} t+{k}:', d, '| IS', summarize(s[s.index < '2021'])['mean_bps'], 'OOS', summarize(s[s.index >= '2021'])['mean_bps'])
            rec('outlook_sets', s, sub=nm, sym=sym, k=k)

print('\n=== (d) YILLARA GÖRE (DUZ_20, XU100 ve XBANK, açılış->t+2, 15 bps) ===')
for sym in ['XU100.IS', 'XBANK.IS']:
    s = signed_returns(rat, sym) - 15e-4
    print(sym, (1e4 * s.groupby(s.index.year).agg(['mean', 'size'])).round(0).assign(size=lambda x: (x['size'] / 1e4).astype(int)).T.to_string())

# ---------------------------------------------------------------- PLASEBO
print('\n=== (b/c6) PLASEBO: aynı yön etiketleri, olay günü ±k hafta kaydırılmış (aynı haftanın günü), XU100 açılış->t+2 ===')
def shifted_mean(ev, sym, weeks, k=2):
    vals = []
    for _, e in ev.iterrows():
        target = e.react + pd.Timedelta(weeks=weeks)
        p = CAL.searchsorted(target)
        if p + k >= len(CAL) or p < 6: return np.nan
        vals.append(-e.dir * trade(sym, p, 'open', k))
    return np.nanmean(vals)
for sym in ['XU100.IS', 'XBANK.IS']:
    for setn, ev in SETS.items():
        act = signed_returns(ev, sym).mean()
        pl = pd.Series({w: shifted_mean(ev, sym, w) for w in list(range(-52, -2)) + list(range(3, 53))}).dropna()
        p = (pl >= act).mean()
        print(f'{sym} {setn}: gerçek {1e4*act:.0f} bps brüt | plasebo ort {1e4*pl.mean():.0f}, sd {1e4*pl.std():.0f}, %95 {1e4*pl.quantile(.95):.0f} | p(plasebo>=gerçek)={p:.3f} (n_shift={len(pl)})')
        rec('placebo', pd.Series([act]), 0, sym=sym, set=setn, placebo_mean=round(1e4 * pl.mean(), 1), placebo_p=round(p, 3))
# rastgele bağımsız kaydırma (her olaya ayrı rastgele kayma, ±3..52 hafta) bootstrap
print('--- bağımsız rastgele kaydırma (10.000 çekiliş) ---')
for sym in ['XU100.IS', 'XBANK.IS']:
    ev = rat
    # her olay için tüm kaydırmaların getirilerini önceden hesapla
    W = list(range(-52, -2)) + list(range(3, 53))
    M = np.full((len(ev), len(W)), np.nan)
    for a, (_, e) in enumerate(ev.iterrows()):
        for b, w in enumerate(W):
            p = CAL.searchsorted(e.react + pd.Timedelta(weeks=w))
            if 6 <= p < len(CAL) - 2: M[a, b] = -e.dir * trade(sym, p, 'open', 2)
    act = signed_returns(ev, sym).mean()
    draws = []
    for _ in range(10000):
        idx = rng.integers(0, len(W), len(ev)); x = M[np.arange(len(ev)), idx]; draws.append(np.nanmean(x))
    draws = np.array(draws)
    print(f'{sym} DUZ_20: gerçek {1e4*act:.0f} | plasebo ort {1e4*draws.mean():.0f} | p={np.mean(draws>=act):.4f}')
    # IS ve OOS ayrı
    for lab, m in [('IS', (ev.react < '2021').values), ('OOS', (ev.react >= '2021').values)]:
        a_ = signed_returns(ev[m], sym).mean(); Mm = M[m]
        dr = np.array([np.nanmean(Mm[np.arange(m.sum()), rng.integers(0, len(W), m.sum())]) for _ in range(10000)])
        print(f'    {lab}: gerçek {1e4*a_:.0f} | plasebo ort {1e4*dr.mean():.0f} | p={np.mean(dr>=a_):.4f}')

# ---------------------------------------------------------------- genel kısa vadeli geri dönüş (olay dışı)
print('\n=== (c7) OLAYDAN BAĞIMSIZ GERİ DÖNÜŞ: her Pazartesi (ve her gün) açılışta -sign(önceki 5g) yönünde gir, t+2 kapanış ===')
xu = DLY['XU100.IS']
o, c = xu['o'].values, xu['c'].values
i_all = np.arange(6, len(CAL) - 2)
pre5 = np.log(c[i_all - 1] / c[i_all - 6]); fwd = np.log(c[i_all + 2] / o[i_all])
df = pd.DataFrame({'pre5': pre5, 'fwd': fwd}, index=CAL[i_all])
df = df[df.index >= '2014-01-01']
df['rev'] = -np.sign(df.pre5) * df.fwd
for nm, m in [('tüm günler', df.index.notna()), ('Pazartesiler', df.index.dayofweek == 0)]:
    for lab, mm in [('ALL', df.index.notna()), ('IS', df.index < '2021'), ('OOS', df.index >= '2021')]:
        x = df.rev[m & mm]
        print(f'{nm:12s} {lab}: ort {1e4*x.mean():.1f} bps brüt, t {tstat(x)[0]:.2f}, n {len(x)}, isabet {(x>0).mean():.2f}')
# büyük hareket sonrası (|pre5| > %3)
x = df.rev[(df.pre5.abs() > 0.03) & (df.index.dayofweek == 0)]
print(f'Pazartesi & |pre5|>3%: ort {1e4*x.mean():.1f}, t {tstat(x)[0]:.2f}, n {len(x)}')
# olay örnekleminde: kontraryen getiri, pre5 yönüyle uyumlu olanlar vs olmayanlar
tb = pd.read_csv(OUT + '/res_event_table.csv', parse_dates=['react'])
tb['agree'] = np.sign(tb.xu100_pre5) == tb.dir
print('olaylarda pre5 not yönünde olanlar:', summarize(tb.loc[tb.agree, 'xu100_strat']), '| olmayanlar:', summarize(tb.loc[~tb.agree, 'xu100_strat']))
# pre5 kontrollü regresyon: strat = a + b * (-dir*pre5)   (a = olay etkisi, b = geri dönüş)
X = np.c_[np.ones(len(tb)), -tb.dir * tb.xu100_pre5]; y = tb.xu100_strat.values
beta, res_, *_ = np.linalg.lstsq(X, y, rcond=None); resid = y - X @ beta
s2 = resid @ resid / (len(y) - 2); se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
print('regresyon strat = a + b*(-dir*pre5): a=%.0f bps (t %.2f), b=%.2f (t %.2f)' % (1e4 * beta[0], beta[0] / se[0], beta[1], beta[1] / se[1]))
# genel geri dönüş katsayısı aynı tanımla tüm Pazartesilerde
mon = df[df.index.dayofweek == 0]
Xg = np.c_[np.ones(len(mon)), -mon.pre5]; yg = mon.fwd.values  # yön: -pre5 işaretli değil; doğrusal geri dönüş
bg = np.linalg.lstsq(Xg, yg, rcond=None)[0]
print('tüm Pazartesiler: fwd = a + b*(-pre5): b=%.3f' % bg[1], '-> olaylarda beklenen geri dönüş katkısı ort %.0f bps' % (1e4 * bg[1] * (tb.dir * tb.xu100_pre5).mean()))

# ---------------------------------------------------------------- (e) maliyet
print('\n=== (e) MALİYET DUYARLILIĞI (DUZ_20, açılış->t+2) ===')
for sym in IDX:
    v = signed_returns(rat, sym)
    row = {c: summarize(v, c)['mean_bps'] for c in [0, 2, 4, 8, 15, 25, 50, 100]}
    tt = {c: summarize(v, c)['t'] for c in [0, 4, 15, 50]}
    print(sym, 'ort bps:', row, '| t:', tt, '| başabaş maliyet ~', round(1e4 * v.mean(), 0), 'bps; t=2 için max maliyet', round(1e4 * (v.mean() - 2 * v.std() / np.sqrt(len(v))), 0))
# tek pozisyon başına senelik katkı (yılda ~2-3 olay)
print('yılda ortalama olay sayısı (2016-2025):', round(len(rat) / 10, 1))
pd.DataFrame(out_rows).to_csv(OUT + '/res_b_robust.csv', index=False)
