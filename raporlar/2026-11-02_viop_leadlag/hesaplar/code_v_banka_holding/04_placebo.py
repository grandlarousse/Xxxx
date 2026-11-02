# -*- coding: utf-8 -*-
"""Plasebo / ortak faktor testleri:
(a) KCHOL ve SAHOL'un 46 diger VIOP hissesiyle XU100-kontrollu pc dagilimi (istirakler gercekten ayrisiyor mu?)
(b) Mekanik icerme olmadan: esit agirlikli VIOP sepeti (cift ve grup sirketleri haric) kontrol
(c) 47 VIOP hissesinin USDTRY pc dagilimi (ENKAI'nin yeri)
(d) B1/B3 uzun orneklem (gunluk vekil): XBANK gap_{t+1} ~ TUR_t / ES_t | XU100_t, XBANK_t ; yillik istikrar
(e) B5 kompozisyon: 2025-11..2026-10 penceresinde Brent ile BIST icindeki rotasyon"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import vb
OUT = os.path.dirname(os.path.abspath(__file__)) + '/res'
V47 = 'AEFES AKBNK AKSEN ALARK ARCLK ASELS ASTOR BIMAS BRSAN CIMSA DOAS DOHOL EKGYO ENJSA ENKAI EREGL FROTO GARAN GUBRF HALKB HEKTS ISCTR KCHOL KRDMD MGROS ODAS OYAKC PETKM PGSUS SAHOL SASA SISE SOKM TAVHL TCELL THYAO TKFEN TOASO TRALT TRMET TSKB TTKOM TUPRS ULKER VAKBN VESTL YKBNK'.split()
R = {s: vb.ret(s + '.IS') for s in V47}
R = pd.DataFrame(R)
X = vb.ret('XU100.IS').rename('XU100').to_frame()
KOC = {'KCHOL', 'ARCLK', 'FROTO', 'TOASO', 'TUPRS', 'YKBNK'}
SAB = {'SAHOL', 'AKBNK', 'ENJSA', 'CIMSA'}
P = {'full2010': ('2010-01-01', '2026-12-31'), 'IS14_20': ('2014-01-01', '2020-12-31'), 'OOS21_26': ('2021-01-01', '2026-12-31'), 'last3y': ('2023-10-31', '2026-12-31')}

def ew_ex(excl):
    cols = [c for c in V47 if c not in excl]
    return R[cols].mean(axis=1).rename('EWex')

def table(hold, group):
    rows = []
    ew = ew_ex(group)  # holding grubu tamamen haric esit agirlikli sepet
    for s in V47:
        if s == hold: continue
        rec = dict(hold=hold, other=s, group=s in group)
        for k, (a, b) in P.items():
            d = vb.pc(vb.per(R[hold], a, b), vb.per(R[s], a, b), vb.per(X, a, b))
            rec[f'{k}_pc'] = d['pc']; rec[f'{k}_t'] = d['t']
        d = vb.pc(vb.per(R[hold], '2010-01-01', '2026-12-31'), vb.per(R[s], '2010-01-01', '2026-12-31'),
                  vb.per(pd.concat([X, ew], axis=1), '2010-01-01', '2026-12-31'))
        rec['full_pc_X+EWex'] = d['pc']; rec['full_t_X+EWex'] = d['t']
        d = vb.pc(R[hold], R[s], ew.to_frame()) if s not in group else vb.pc(R[hold], R[s], ew.to_frame())
        rec['full_pc_EWex_only'] = d['pc']
        rows.append(rec)
    T = pd.DataFrame(rows).sort_values('full2010_pc', ascending=False)
    T['rank'] = np.arange(1, len(T) + 1)
    return T

pd.set_option('display.width', 250)
for hold, grp in [('KCHOL', KOC), ('SAHOL', SAB)]:
    T = table(hold, grp)
    T.to_csv(f'{OUT}/placebo_{hold}.csv', index=False)
    print(f'\n=== {hold}: diger 46 VIOP hissesiyle pc | XU100 (2010+) — ilk 15 ===')
    print(T.head(15)[['rank', 'other', 'group', 'full2010_pc', 'full2010_t', 'IS14_20_pc', 'OOS21_26_pc', 'last3y_pc', 'full_pc_X+EWex', 'full_pc_EWex_only']].round(3).to_string(index=False))
    ng = T[~T.group]
    print(f'  grup DISI {len(ng)} hisse: pc medyan={ng.full2010_pc.median():+.3f}, p90={ng.full2010_pc.quantile(.9):+.3f}, max={ng.full2010_pc.max():+.3f} ({ng.iloc[0].other}); X+EWex medyan={ng["full_pc_X+EWex"].median():+.3f} p90={ng["full_pc_X+EWex"].quantile(.9):+.3f}')
    print('  grup ICI:', ' '.join(f"{r.other}:{r.full2010_pc:+.3f}(EWex {r['full_pc_X+EWex']:+.3f}, rank {r['rank']})" for _, r in T[T.group].iterrows()))

# (c) USDTRY pc dagilimi
fx = vb.ret('TRY=X')
rows = []
for s in V47:
    rec = dict(stock=s)
    for k, (a, b) in P.items():
        d = vb.pc(vb.per(R[s], a, b), vb.per(fx, a, b), vb.per(X, a, b))
        rec[f'{k}_pc'] = d['pc']; rec[f'{k}_t'] = d['t']; rec[f'{k}_n'] = d['n']
    rows.append(rec)
F = pd.DataFrame(rows).sort_values('full2010_pc', ascending=False)
F.to_csv(f'{OUT}/placebo_fx_pc.csv', index=False)
print('\n=== 47 VIOP hissesi ~ USDTRY | XU100 (2010+) ===')
print(F[['stock', 'full2010_pc', 'full2010_t', 'IS14_20_pc', 'OOS21_26_pc', 'last3y_pc', 'full2010_n']].round(3).to_string(index=False))

# (d) B1/B3 uzun orneklem gunluk vekil
print('\n=== (d) Gunluk vekil: XBANK gap_{t+1} ~ surucu_t | XU100_t, XBANK_t (BIST kapanisinda zaten fiyatlanmis kismi kontrol) ===')
dx = vb.bist_rets('XBANK.IS'); d1 = vb.bist_rets('XU100.IS')
gap1 = dx['gap'].shift(-1); intra1 = dx['intra'].shift(-1)
Zc = pd.concat([d1['cc'].rename('X'), dx['cc'].rename('B')], axis=1)
for drv in ['TUR', 'ES=F', 'EEM']:
    s = vb.ret(drv)
    yrs = []
    for yr in range(2014, 2027):
        a, b = f'{yr}-01-01', f'{yr}-12-31'
        g = vb.pc(vb.per(gap1, a, b), vb.per(s, a, b), vb.per(Zc, a, b))
        i = vb.pc(vb.per(intra1, a, b), vb.per(s, a, b), vb.per(Zc, a, b))
        yrs.append((yr, g['pc'], i['pc']))
    full_g = vb.pc(vb.per(gap1, '2014-01-01', '2026-12-31'), vb.per(s, '2014-01-01', '2026-12-31'), vb.per(Zc, '2014-01-01', '2026-12-31'))
    full_i = vb.pc(vb.per(intra1, '2014-01-01', '2026-12-31'), vb.per(s, '2014-01-01', '2026-12-31'), vb.per(Zc, '2014-01-01', '2026-12-31'))
    isg = vb.pc(vb.per(gap1, '2014-01-01', '2020-12-31'), vb.per(s, '2014-01-01', '2020-12-31'), vb.per(Zc, '2014-01-01', '2020-12-31'))
    oog = vb.pc(vb.per(gap1, '2021-01-01', '2026-12-31'), vb.per(s, '2021-01-01', '2026-12-31'), vb.per(Zc, '2021-01-01', '2026-12-31'))
    pos = np.mean([v[1] > 0 for v in yrs])
    print(f"  {drv:5s} gap: pc={full_g['pc']:+.3f} t={full_g['t']:+.1f} n={full_g['n']} | IS {isg['pc']:+.3f} OOS {oog['pc']:+.3f} | pozitif yil orani {pos:.2f} | intra pc={full_i['pc']:+.3f} t={full_i['t']:+.1f}")
    print('     yillik gap pc:', ' '.join(f"{y}:{g:+.2f}" for y, g, _ in yrs))
    print('     yillik intra pc:', ' '.join(f"{y}:{i:+.2f}" for y, _, i in yrs))

# (e) B5 kompozisyon
print('\n=== (e) B5: 2025-11..2026-10, surucu ~ BIST hissesi | XU100 ===')
a, b = '2025-11-01', '2026-10-30'
bz = vb.per(vb.ret('BZ=F'), a, b); Xw = vb.per(X, a, b)
rows = []
for s in V47 + ['XBANK', 'XUSIN', 'XU030']:
    r = R[s] if s in R else vb.ret(s + '.IS')
    d = vb.pc(vb.per(r, a, b), bz, Xw)
    rows.append((s, d['pc'], d['t']))
rows.sort(key=lambda z: z[1])
print('  en negatif:', ' '.join(f"{s}:{p:+.2f}" for s, p, t in rows[:10]))
print('  en pozitif:', ' '.join(f"{s}:{p:+.2f}" for s, p, t in rows[-10:]))
ew_nb = R[[c for c in V47 if c not in {'AKBNK', 'GARAN', 'YKBNK', 'ISCTR', 'HALKB', 'VAKBN', 'TSKB', 'SAHOL'}]].mean(axis=1)
xb = vb.ret('XBANK.IS')
for name, Z in [('XU100', Xw), ('EW banka-disi VIOP', vb.per(ew_nb, a, b).to_frame()),
                ('XU100+TUPRS+ASELS+THYAO', vb.per(pd.concat([X, R[['TUPRS', 'ASELS', 'THYAO']]], axis=1), a, b))]:
    for drv in ['BZ=F', 'SAN.MC', 'EMB', 'BBVA.MC']:
        d = vb.pc(vb.per(xb, a, b), vb.per(vb.ret(drv), a, b), Z)
        print(f"  XBANK~{drv:8s} | {name:26s} pc={d['pc']:+.3f} t={d['t']:+.1f} n={d['n']}")
