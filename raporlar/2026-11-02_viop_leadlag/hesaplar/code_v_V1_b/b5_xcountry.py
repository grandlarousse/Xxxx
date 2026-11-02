"""b5: dış geçerlilik — başka ülkelerin not değişiklikleri sonrası aynı kontraryen kural (Pzt açılış -> t+2 kapanış) çalışıyor mu?
ZA (^J203.JO, EZA), GR (GD.AT, GREK), IT (FTSEMIB.MI, EWI), BR (^BVSP, EWZ). Takvimli (AB CRA Cuma) vs takvim dışı."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vb import *
E = pd.read_csv(HERE + '/events_xc.csv', parse_dates=['ann'])
MK = {'ZA': ('^J203.JO', 'EZA'), 'GR': ('GD.AT', 'GREK'), 'IT': ('FTSEMIB.MI', 'EWI'), 'BR': ('^BVSP', 'EWZ')}
eem = load('EEM'); eo = np.log(eem.o * eem.adj / eem.c); ec = np.log(eem.adj)
def series(sym, etf):
    d = load(sym); d = d[(d.c > 0)]
    if etf: o, c = np.log(d.o * d.adj / d.c), np.log(d.adj)
    else: o, c = np.log(d.o.where(d.o > 0)), np.log(d.c)
    bad_open = ((d.o - d.c.shift()).abs() / d.c.shift() < 1e-6).mean()
    return o, c, d.index, bad_open
def beta(c_etf, i_date):
    a = c_etf.diff(); f = ec.diff(); df = pd.concat([a, f], axis=1, keys=['a', 'f'], sort=True).dropna()
    w_ = df[(df.index < i_date) & (df.index >= i_date - pd.Timedelta(days=365))]; return np.cov(w_.a, w_.f)[0, 1] / w_.f.var()
rows = []
for cty, (loc, etf) in MK.items():
    Lo, Lc, Li, lb = series(loc, False); Eo, Ec, Ei, _ = series(etf, True)
    print(f'{cty}: {loc} açılış==önceki kapanış oranı {lb:.3f}')
    for _, e in E[E.country == cty].iterrows():
        r = dict(country=cty, ann=e.ann.date(), agency=e.agency, dir=e.dir, sched=e.sched, fri=e.ann.dayofweek == 4)
        j = Li.searchsorted(e.ann, side='right')
        if j + 2 < len(Li):
            r['loc_react'] = Li[j].date(); r['loc_open_t2'] = -e.dir * (Lc.iloc[j + 2] - Lo.iloc[j]); r['loc_close_t2'] = -e.dir * (Lc.iloc[j + 2] - Lc.iloc[j])
            r['loc_t0'] = -e.dir * (Lc.iloc[j] - Lc.iloc[j - 1])
        k = Ei.searchsorted(e.ann, side='right')
        if k + 2 < len(Ei) and Ei[0] < e.ann:
            m = eem.index.searchsorted(Ei[k]); b = beta(Ec, Ei[k])
            x = Ec.iloc[k + 2] - Eo.iloc[k]; f = ec.iloc[m + 2] - eo.iloc[m]
            r.update(etf_open_t2=-e.dir * x, etf_ab=-e.dir * (x - b * f), eem=-e.dir * f, etf_close_t2=-e.dir * (Ec.iloc[k + 2] - Ec.iloc[k]))
        rows.append(r)
R = pd.DataFrame(rows); R.to_csv(HERE + '/res_b5_xcountry.csv', index=False)
C15 = 15e-4
def rep(df, lab):
    print(f'-- {lab}: n={len(df)} (indirim {int((df.dir<0).sum())}, artırım {int((df.dir>0).sum())})')
    for c in ['loc_open_t2', 'loc_close_t2', 'etf_open_t2', 'etf_ab', 'eem', 'loc_t0']:
        if c in df: print('   ' + fmt(df[c].dropna() - (0 if c in ('eem', 'loc_t0') else C15), c))
for cty in MK:
    D_ = R[R.country == cty]
    rep(D_[D_.sched == 1], f'{cty} takvimli'); rep(D_[D_.sched == 0], f'{cty} takvim dışı')
rep(R[(R.sched == 1) & (R.country != 'BR')], 'HAVUZ takvimli (ZA+GR+IT)')
rep(R[(R.sched == 1) & (R.country != 'BR') & (R.dir < 0)], 'HAVUZ takvimli indirimler')
rep(R[(R.sched == 1) & (R.country != 'BR') & (R.dir > 0)], 'HAVUZ takvimli artırımlar')
rep(R[R.sched == 0], 'HAVUZ takvim dışı (BR dahil)')
# Yunanistan 2015 kriz dönemi hariç
G = R[(R.country == 'GR') & (R.sched == 1) & (pd.to_datetime(R.ann).dt.year != 2015)]; rep(G, 'GR takvimli, 2015 hariç')
# yıl kümeli
P = R[(R.sched == 1) & (R.country != 'BR')].dropna(subset=['loc_open_t2']).copy(); P['yr'] = pd.to_datetime(P.ann).dt.year
g = P.groupby(['country', 'yr']).loc_open_t2.mean(); t, n = tstat(g); print(f'havuz takvimli, ülke-yıl kümeli ortalama {1e4*g.mean():+.1f} bps, t {t:.2f}, n küme {n}')
print(R.assign(**{c: (1e4 * R[c]).round(0) for c in ['loc_open_t2', 'loc_close_t2', 'etf_open_t2', 'etf_ab', 'eem', 'loc_t0']}).to_string(index=False))
