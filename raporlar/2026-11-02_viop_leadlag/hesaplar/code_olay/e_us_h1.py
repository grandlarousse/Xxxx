"""ABD 8:30 ET verisi (yaz 12:30 UTC=15:30 TSİ, kış 13:30 UTC=16:30 TSİ) BIST seansı İÇİNDE. ES h1 2024-06+.
ES barları :00'da, BIST barları :30'da başlar -> ES penceresi [R-30dk, R+30dk], BIST tepki penceresi [R, R+60dk], devam: [R+60dk, kapanış]."""
from olib import *
ev = EV[EV.type == 'USDATA']; dd = dict(zip(ev.date, ev['sub']))
def us_rel(D):
    y = D.year; m2 = pd.Timestamp(y,3,1); s = m2 + pd.Timedelta(days=(6-m2.weekday())%7 + 7); n1 = pd.Timestamp(y,11,1); e = n1 + pd.Timedelta(days=(6-n1.weekday())%7)
    return 12 if s <= D < e else 13
es = {f'{h}:{m}': ll.snap_daily('ES=F', f'{h:02d}:{m}') for h in (11,12,13,14) for m in ('00',)}
rows = []
for sym in ['XU030.IS', 'XBANK.IS'] + [v + '.IS' for v in ['AKBNK','THYAO','ASELS','TUPRS','KCHOL','EREGL','SASA','BIMAS','ASTOR','TCELL']]:
    bs = {f'{h:02d}:30': ll.snap_daily(sym, f'{h:02d}:30') for h in (11,12,13,14)}
    dc = ll.daily(sym, 'c', on_bist_cal=False)
    for D in dc.index[dc.index >= '2024-06-10']:
        H = us_rel(D)
        try:
            e0, e1 = es[f'{H-1}:00'].get(D), es[f'{H}:00'].get(D)   # ES [R-30, R+30]
            b0, b1, b2 = bs[f'{H:02d}:30'].get(D), bs[f'{H+1:02d}:30'].get(D), dc.get(D)  # BIST R, R+60, kapanış
            bpre = bs[f'{H-1:02d}:30'].get(D)
        except KeyError: continue
        if any(pd.isna(x) for x in [e0, e1, b0, b1, b2, bpre]): continue
        rows.append(dict(sym=sym, date=D, ev=dd.get(D, 'none'), es=np.log(e1/e0), pre=np.log(b0/bpre), react=np.log(b1/b0), post=np.log(b2/b1)))
U = pd.DataFrame(rows); U.to_csv('res_usdata_h1.csv', index=False)
out = []
for sym, g in U.groupby('sym'):
    for lab, m in [('NFP+CPI', g.ev.isin(['NFP','CPI'])), ('NFP', g.ev=='NFP'), ('CPI', g.ev=='CPI'), ('none', g.ev=='none')]:
        S = g[m]
        if len(S) < 8: continue
        v = np.sign(S.es) * S.post
        out.append(dict(sym=sym, grp=lab, n=len(S), corr_sync=S[['es','react']].corr().iloc[0,1], beta_sync=np.polyfit(S.es, S.react, 1)[0],
                        corr_lead=S[['es','post']].corr().iloc[0,1], cont_bps=1e4*v.mean(), cont_t=tstat(v)[0], abs_react_bps=1e4*S.react.abs().mean(), abs_pre_bps=1e4*S.pre.abs().mean()))
O = pd.DataFrame(out); O.to_csv('res_usdata_summary.csv', index=False)
print(O[O.sym.isin(['XU030.IS','XBANK.IS'])].round(3).to_string(index=False))
print(O[(O.grp=='NFP+CPI')].sort_values('beta_sync')[['sym','n','corr_sync','beta_sync','corr_lead','cont_bps','cont_t']].round(2).to_string(index=False))
# backtest: veri günlerinde sign(ES penceresi) ile XU030'u R+60'ta al, kapanışta kapat; IS (2024-06..2025-06) / OOS (2025-07..)
S = U[(U.sym=='XU030.IS') & U.ev.isin(['NFP','CPI'])].set_index('date')
for cost in [8, 15]:
    p = np.sign(S.es) * S.post - cost/1e4
    for lab, m in [('IS', p.index < '2025-07-01'), ('OOS', p.index >= '2025-07-01'), ('ALL', p.index.notna())]:
        print('BT cont XU030', cost, lab, round(1e4*p[m].mean(),1), round(tstat(p[m])[0],2), int(m.sum()))
