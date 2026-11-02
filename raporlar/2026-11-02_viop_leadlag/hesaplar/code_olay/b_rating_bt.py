"""Not değişikliği sonrası KONTRARİAN (sell-the-news) backtest: react günü açılışta -dir yönünde gir, t+5 kapanışta çık."""
from olib import *
T = pd.read_csv('res_rating_events.csv', parse_dates=['react'])
T = T[T.kind.isin(['downgrade', 'upgrade'])].drop_duplicates('react')
cc, it = comp('cc'), comp('intra'); f15 = fwd_cc(cc, 1, 5); f12 = fwd_cc(cc, 1, 2)
rows = []
for c in ['XU100', 'XBANK', 'XU030']:
    for hold_nm, F in [('intra', None), ('intra+t1..2', f12), ('intra+t1..5', f15)]:
        r = []
        for _, e in T.iterrows():
            d = e.react; x = it.at[d, c] + (F.at[d, c] if F is not None else 0)
            r.append((d, -e.dir * x))
        s = pd.Series(dict(r)).dropna()
        for cost in [8, 15]:
            p = s - cost / 1e4
            for lab, m in [('IS', p.index < '2021-01-01'), ('OOS', p.index >= '2021-01-01'), ('ALL', p.index.notna())]:
                q = p[m]; t, n = tstat(q)
                rows.append(dict(idx=c, hold=hold_nm, cost=cost, sample=lab, mean_bps=1e4 * q.mean(), t=t, n=n, hit=(q > 0).mean()))
R = pd.DataFrame(rows); R.to_csv('res_rating_contrarian_bt.csv', index=False)
print(R[(R.cost == 15)].round(2).to_string(index=False))
print(T[['react', 'sub', 'dir', 'XU100_pre5', 'XU100_gap', 'XU100_intra', 'XU100_f1_5']].round(4).to_string(index=False))
# Sağlamlık: nominal TL sürüklenmesini çıkar (her gün için 3 günlük getiri - [t-250, t-1] ortalama 3g getiri) ve ±60g merkezli ortalama
print('--- drift-düzeltmeli (intra+t1..2, 15bps) ---')
for c in ['XU100', 'XBANK']:
    x3 = it[c] + f12[c]
    trail = cc[c].rolling(250, min_periods=120).mean().shift(1) * 3
    cent = cc[c].rolling(121, center=True, min_periods=60).mean() * 3
    for nm, adj in [('trail250', trail), ('centered121', cent)]:
        v = pd.Series({e.react: -e.dir * (x3.at[e.react] - adj.at[e.react]) for _, e in T.iterrows()}).dropna() - 15e-4
        for lab, m in [('IS', v.index < '2021-01-01'), ('OOS', v.index >= '2021-01-01'), ('ALL', v.index.notna())]:
            t, n = tstat(v[m]); print(c, nm, lab, round(1e4 * v[m].mean(), 1), round(t, 2), n)
# USD bazlı (TL enflasyon sürüklenmesini kaldırmak için) XU100: r_TL - r_USDTRY (ll düzeltilmiş FX)
fx = ll.ret('TRY=X').reindex(cc.index)
usd3 = (cc['XU100'] - fx).shift(-1) + (cc['XU100'] - fx).shift(-2)
v = pd.Series({e.react: -e.dir * (it.at[e.react, 'XU100'] + usd3.at[e.react]) for _, e in T.iterrows()}).dropna() - 15e-4
print('USD-bazlı t1..2 (+intra TL)', round(1e4 * v.mean(), 1), round(tstat(v)[0], 2), len(v))
