"""H45(b) ENKAI: TUR_{t-1} -> ENKAI gün-içi (negatif = açılış aşırı tepkisi geri döner)
H45(c) ENKAI: USDTRY_{t-1} -> ENKAI gün-içi (pozitif)
Bağımsız hizalama (vlib.us_prev / vlib.fx_prev), kontroller, gap-fade ayrıştırması, genellik (47 hisse), yıllar."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlib as V, numpy as np, pandas as pd
pd.set_option('display.width', 250)
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]

E = V.decomp('ENKAI'); X100 = V.decomp('XU100'); X30 = V.decomp('XU030')
TUR, TUR_same = V.us_prev('TUR')
USD = V.fx_prev('TRY=X')
EUR = V.fx_prev('EURTRY=X')
rows = []

def line(lab, y, x):
    c, t, n = V.corr_t(y, x); ci, ti, _ = V.corr_t(y, x, V.IS0, V.SPLIT); co, to, _ = V.corr_t(y, x, V.SPLIT)
    yr = V.by_year(y, x); same = (np.sign(yr.dropna()) == np.sign(c)).mean()
    ex = y.copy(); ex[(ex.index >= '2021-01-01') & (ex.index < '2023-01-01')] = np.nan
    ce, te, _ = V.corr_t(ex, x)
    print(f'{lab:52s} corr {c:+.3f} t {t:+.2f} n {n} | IS {ci:+.3f} t {ti:+.2f} | OOS {co:+.3f} t {to:+.2f} | 2021-22 hariç {ce:+.3f} t {te:+.2f} | yıl aynı {same:.2f}')
    print('      yıllar: ' + ' '.join(f'{k}:{v:+.2f}' for k, v in yr.items()))
    rows.append({'test': lab, 'c': c, 't': t, 'n': n, 'c_IS': ci, 't_IS': ti, 'c_OOS': co, 't_OOS': to, 'c_ex2122': ce, 't_ex2122': te,
                 'yr_same': same, 'by_year': json.dumps(yr.round(3).to_dict())})

def reg(lab, y, Xs, names, periods=(('ALL', V.IS0, None), ('IS', V.IS0, V.SPLIT), ('OOS', V.SPLIT, None))):
    for pl, s0, s1 in periods:
        f = lambda z: z[(z.index >= s0) & ((z.index < s1) if s1 is not None else True)]
        r = V.ols(f(y), [f(x) for x in Xs], names=names)
        print(f'   {lab:60s} {pl:4s} n={r["n"]:4d} ' + ' '.join(f'{k}={r["b"][k]:+.3f}(t{r["t"][k]:+.2f})' for k in names))
        rows.append({'test': f'REG {lab} {pl}', **{f'b_{k}': r['b'][k] for k in names}, **{f't_{k}': r['t'][k] for k in names}, 'n': r['n']})

print('==================== (b) TUR_{t-1} ====================')
line('B1 TUR_{t-1} -> ENKAI gap_t', E['gap'], TUR)
line('B1 TUR_{t-1} -> ENKAI intra_t', E['intra'], TUR)
line('B1 TUR_{t-1} -> XU100 intra_t', X100['intra'], TUR)
line('B1 TUR_{t-1} -> XU100 gap_t', X100['gap'], TUR)
bE = V.ols(E['intra'], [X30['intra']])['b'].iloc[1]
line(f'B1 TUR_{{t-1}} -> ENKAI intra - {bE:.2f}*XU030 intra', E['intra'] - bE * X30['intra'], TUR)
print('  Kontrollü regresyonlar (ENKAI intra_t):')
reg('Eintra ~ TUR', E['intra'], [TUR], ['TUR'])
reg('Eintra ~ TUR + Egap', E['intra'], [TUR, E['gap']], ['TUR', 'Egap'])
reg('Eintra ~ TUR + Ecc_{t-1} + X100cc_{t-1}', E['intra'], [TUR, E['cc'].shift(1), X100['cc'].shift(1)], ['TUR', 'Ecc1', 'Xcc1'])
reg('Eintra ~ TUR + Egap + X100gap', E['intra'], [TUR, E['gap'], X100['gap']], ['TUR', 'Egap', 'Xgap'])
reg('Eintra ~ TUR + USD', E['intra'], [TUR, USD], ['TUR', 'USD'])
reg('Eintra ~ TUR + USD + Egap + Ecc1 + Xcc1', E['intra'], [TUR, USD, E['gap'], E['cc'].shift(1), X100['cc'].shift(1)], ['TUR', 'USD', 'Egap', 'Ecc1', 'Xcc1'])
reg('Eintra ~ TUR + X30intra (tanı: piyasa gün-içi aynı anda)', E['intra'], [TUR, X30['intra']], ['TUR', 'X30i'])
# gap-fade ayrıştırması: Egap = a + b*TUR + u ;  Eintra ~ fitted + u
df = pd.concat([E['gap'].rename('g'), TUR.rename('x')], axis=1).dropna()
r = V.ols(df['g'], [df['x']], names=['x']); fit = r['b']['const'] + r['b']['x'] * df['x']; res = df['g'] - fit
print(f"  Egap ~ TUR: b={r['b']['x']:.3f} t={r['t']['x']:.2f} R2={r['r2']:.3f}")
reg('Eintra ~ Egap_fit(TUR) + Egap_resid', E['intra'], [fit, res], ['fit', 'resid'])

print('\n==================== (c) USDTRY_{t-1} (00:00 UTC t - 00:00 UTC t_prev) ====================')
line('C1 USD_{t-1} -> ENKAI gap_t', E['gap'], USD)
line('C1 USD_{t-1} -> ENKAI intra_t', E['intra'], USD)
line('C1 USD_{t-1} -> ENKAI cc_t', E['cc'], USD)
line('C1 USD_{t-1} -> XU100 intra_t', X100['intra'], USD)
line(f'C1 USD_{{t-1}} -> ENKAI intra - {bE:.2f}*XU030 intra', E['intra'] - bE * X30['intra'], USD)
line('C1 EURTRY_{t-1} -> ENKAI intra_t', E['intra'], EUR)
reg('Eintra ~ USD', E['intra'], [USD], ['USD'])
reg('Eintra ~ USD + Egap', E['intra'], [USD, E['gap']], ['USD', 'Egap'])
reg('Eintra ~ USD + Ecc1 + Xcc1', E['intra'], [USD, E['cc'].shift(1), X100['cc'].shift(1)], ['USD', 'Ecc1', 'Xcc1'])
reg('Eintra ~ USD + X30intra (tanı)', E['intra'], [USD, X30['intra']], ['USD', 'X30i'])
# uç gün etkisi: |USD| en büyük %1 günleri hariç
q = USD.abs().quantile(0.99)
u2 = USD.where(USD.abs() <= q)
line(f'C2 USD_{{t-1}} -> ENKAI intra (|USD|>%{100*q:.2f} uç %1 hariç)', E['intra'], u2)
w = USD.clip(USD.quantile(0.01), USD.quantile(0.99))
line('C2 USD_{t-1} winsor %1 -> ENKAI intra', E['intra'], w)
line('C2 sign(USD_{t-1}) -> ENKAI intra', E['intra'], np.sign(USD).where(USD != 0))

print('\n==================== Genellik: 47 hisse, TUR_{t-1} ve USD_{t-1} -> intra_t ====================')
g = []
for s in VIOP:
    try: d = V.decomp(s)
    except Exception: continue
    o = {'stock': s}
    for nm, x in [('TUR', TUR), ('USD', USD)]:
        c, t, n = V.corr_t(d['intra'], x); co, to, _ = V.corr_t(d['intra'], x, V.SPLIT)
        rr = V.ols(d['intra'], [x, d['gap']], names=['x', 'g'])
        o.update({f'{nm}_c': c, f'{nm}_t': t, f'{nm}_tOOS': to, f'{nm}_t_ctrlgap': rr['t']['x'] if rr else np.nan})
    g.append(o)
G = pd.DataFrame(g)
print(G.sort_values('TUR_t').round(3).to_string(index=False))
for nm in ['TUR', 'USD']:
    print(f"{nm}: medyan t {G[nm + '_t'].median():.2f}; t<-3: {(G[nm + '_t'] < -3).sum()}, t>3: {(G[nm + '_t'] > 3).sum()}; ENKAI t {G.set_index('stock').loc['ENKAI', nm + '_t']:.2f}, sıra(küçükten) {list(G.sort_values(nm + '_t').stock).index('ENKAI') + 1}/{len(G)}")
G.to_csv(os.path.join(V.CODE, 'res_generic_enkai.csv'), index=False)
pd.DataFrame(rows).to_csv(os.path.join(V.CODE, 'res_enkai.csv'), index=False)
