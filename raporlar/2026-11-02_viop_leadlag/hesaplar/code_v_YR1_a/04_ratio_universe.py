"""YR1-A plasebo/seçim yanlılığı: 47 VİOP hissesinin TÜM yönlü çiftlerinde aynı kural (z60>1,5, t+1 açılış, 8 bps)."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_YR1_a')
from vlib import *
V = ['AEFES','AKBNK','AKSEN','ALARK','ARCLK','ASELS','ASTOR','BIMAS','BRSAN','CIMSA','DOAS','DOHOL','EKGYO','ENJSA','ENKAI','EREGL','FROTO','GARAN','GUBRF','HALKB','HEKTS','ISCTR','KCHOL','KRDMD','MGROS','ODAS','OYAKC','PETKM','PGSUS','SAHOL','SASA','SISE','SOKM','TAVHL','TCELL','THYAO','TKFEN','TOASO','TRALT','TRMET','TSKB','TTKOM','TUPRS','ULKER','VAKBN','VESTL','YKBNK']
cal = raw('XU100').index; cal = cal[cal >= pd.Timestamp('2010-01-01')]
D = {s: dec(s).reindex(cal) for s in V}
CC = pd.DataFrame({s: D[s]['cc'] for s in V}); GP = pd.DataFrame({s: D[s]['gap'] for s in V}); IN = pd.DataFrame({s: D[s]['intra'] for s in V})
def one(A, B, w=60, thr=1.5, cost=8):
    beta = roll_beta(CC[A], CC[B])
    S = (CC[A] - beta * CC[B]).fillna(0).cumsum()
    z = zscore(S, w)
    # yeterli veri: her iki bacakta da gerçek getiri olmayan dönemlerde z üretme
    ok = CC[A].notna().rolling(60).sum().ge(50) & CC[B].notna().rolling(60).sum().ge(50)
    z = z.where(ok)
    pos = positions(z, thr)
    sim = simulate(pos, GP[A] - beta * GP[B], IN[A] - beta * IN[B], CC[A] - beta * CC[B], 1 + beta.abs(), 'open', cost)
    o = {}
    for per, lo, hi in [('IS', '2014-01-01', SPLIT), ('OOS', SPLIT, '2027-01-01')]:
        st = summarize(sim, lo, hi); o[f'{per}_m'] = st['mean_bps']; o[f'{per}_t'] = st['t_all']; o[f'{per}_n'] = st['n_act']
    return o
rows = []
corr = CC[CC.index >= '2014-01-01'].corr()
for A in V:
    for B in V:
        if A == B: continue
        o = one(A, B); rows.append(dict(A=A, B=B, corr=corr.loc[A, B], **o))
R = pd.DataFrame(rows); R.to_csv(HERE + '/res_ratio_universe.csv', index=False)
R = R[(R.IS_n >= 150) & (R.OOS_n >= 150)]
print('çift sayısı (yönlü, iki dönemde de >=150 aktif gün):', len(R))
for lab, sub in [('tüm', R), ('corr>=0,5', R[R['corr'] >= 0.5]), ('corr>=0,6', R[R['corr'] >= 0.6])]:
    print(f'{lab:10s} n={len(sub):4d} IS t ort {sub.IS_t.mean():.2f} sd {sub.IS_t.std():.2f} | OOS t ort {sub.OOS_t.mean():.2f} sd {sub.OOS_t.std():.2f} | IS&OOS t>2: {((sub.IS_t>2)&(sub.OOS_t>2)).mean()*100:.1f}% | IS&OOS t>3: {((sub.IS_t>3)&(sub.OOS_t>3)).mean()*100:.2f}% | corr(IS_t,OOS_t) {sub.IS_t.corr(sub.OOS_t):.2f}')
R['minT'] = R[['IS_t', 'OOS_t']].min(axis=1)
R = R.sort_values('minT', ascending=False)
print('min(IS t, OOS t) sıralaması, ilk 25:'); print(R.head(25).round(2).to_string())
sa = R[(R.A == 'SAHOL') & (R.B == 'AKBNK')]; print('SAHOL/AKBNK sıra:', int((R.minT > sa.minT.iloc[0]).sum()) + 1, '/', len(R))
print('SAHOL içeren çiftler (A=SAHOL):'); print(R[R.A == 'SAHOL'].sort_values('corr', ascending=False).head(12).round(2).to_string())
print('B=AKBNK, A=diğer:'); print(R[R.B == 'AKBNK'].sort_values('minT', ascending=False).head(8).round(2).to_string())
