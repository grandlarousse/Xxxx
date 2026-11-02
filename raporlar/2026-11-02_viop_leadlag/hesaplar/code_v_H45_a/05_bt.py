"""Backtestler (bağımsız): IS 2014-2020 / OOS 2021-2026, maliyet 0/8/15 bps (pay vadelisi), hedge'li varyant (+3 bps XU030 vadelisi).
z-skor: sinyalin geçmiş 250 gözlemine göre (t günü hariç). Kaydırılmış-sinyal null dağılımı (k=20..120 gün)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlib as V, numpy as np, pandas as pd
pd.set_option('display.width', 250)
W = {'TUPRS': .33, 'FROTO': .20, 'YKBNK': .24, 'ARCLK': .07, 'TOASO': .04, 'AYGAZ': .03, 'OTKAR': .02, 'TTRAK': .03}
X30 = V.decomp('XU030')


def nav_sig(strict=False):
    K = V.decomp('KCHOL', strict); D = {s: V.decomp(s, strict) for s in W}
    G = pd.DataFrame({s: D[s]['gap'] for s in W}); ws = pd.Series(W); M = G.notna().mul(ws, axis=1)
    nav = ((G.fillna(0) * ws).sum(axis=1) / M.sum(axis=1)).where((M.sum(axis=1) >= 0.6) & G[['TUPRS', 'FROTO', 'YKBNK']].notna().all(axis=1))
    return nav - K['gap'], K


def hedged(y, win=250):
    """y - beta_{t-1} * XU030 intra ; beta geçmiş 250 günden (look-ahead yok)."""
    df = pd.concat([y.rename('y'), X30['intra'].rename('x')], axis=1).dropna()
    cov = df['y'].rolling(win, min_periods=120).cov(df['x']).shift(1); var = df['x'].rolling(win, min_periods=120).var().shift(1)
    b = (cov / var).clip(0, 2)
    return (df['y'] - b * df['x']).reindex(y.index)


rows = []
def run(name, pos, tgt, costs=(0, 8, 15)):
    for c in costs:
        o, pnl = V.bt(pos, tgt, c)
        print(f'{name:58s} c={c:4.1f} ' + V.fmt_bt(o))
        if c == 8: print(f'{"":58s}        yıllar (bps/işlem): {o["by_year"]}  işlem sayısı: {o["n_by_year"]}')
        rows.append({'test': name, 'cost': c, **{f'{k}_{f}': o[k].get(f, np.nan) for k in ['IS', 'OOS', 'ALL'] for f in ['n', 'mean_bps', 't', 'hit', 'sharpe']},
                     'by_year': json.dumps(o['by_year'])})


def shift_null(sig, thr, tgt, cost=8, ks=range(20, 121, 5)):
    out = []
    for k in ks:
        o, _ = V.bt(V.zpos(sig.shift(k), thr), tgt, cost)
        out.append(o['OOS'].get('mean_bps', np.nan))
    return np.array(out)


print('==================== (a) KCHOL açılış NAV ayrışması ====================')
sig, K = nav_sig(False)
pos = V.zpos(sig, 0.5)
run('A z>0.5 sig -> KCHOL intra (müzayede girişi, iddia)', pos, K['intra'])
run('A z>0.5 sig -> KCHOL intra hedge (XU030), +3bps', pos, hedged(K['intra']), costs=(3, 11, 18))
run('A z>1.0 sig -> KCHOL intra', V.zpos(sig, 1.0), K['intra'])
run('A sign(sig) -> KCHOL intra', np.sign(sig).fillna(0), K['intra'])
run('A z>0.5 sadece kendi gap fade (-Kgap) -> KCHOL intra', V.zpos(-K['gap'], 0.5), K['intra'])
sigS, KS = nav_sig(True)
run('A [strict açılış] z>0.5 sig -> KCHOL intra', V.zpos(sigS, 0.5), KS['intra'])
nul = shift_null(sig, 0.5, K['intra'])
print(f'   kaydırılmış-sinyal null (OOS, 8 bps): ort {np.nanmean(nul):+.1f}, %5-%95 [{np.nanpercentile(nul, 5):+.1f}, {np.nanpercentile(nul, 95):+.1f}] bps')

print('\n==================== (b) ENKAI -TUR_{t-1} ====================')
E = V.decomp('ENKAI'); TUR, _ = V.us_prev('TUR'); USD = V.fx_prev('TRY=X')
p_b = V.zpos(-TUR, 1.0)
run('B z>1 -TUR_{t-1} -> ENKAI intra', p_b, E['intra'])
run('B z>1 -TUR_{t-1} -> ENKAI intra hedge (XU030), +3bps', p_b, hedged(E['intra']), costs=(3, 11, 18))
run('B z>0.5 -TUR_{t-1} -> ENKAI intra', V.zpos(-TUR, 0.5), E['intra'])
run('B z>2 -TUR_{t-1} -> ENKAI intra', V.zpos(-TUR, 2.0), E['intra'])
ex = E['intra'].copy(); ex[(ex.index >= '2021-01-01') & (ex.index < '2023-01-01')] = np.nan
run('B z>1 -TUR_{t-1} -> ENKAI intra (2021-22 HARİÇ)', p_b, ex)
nul = shift_null(-TUR, 1.0, E['intra'])
print(f'   kaydırılmış-sinyal null (OOS, 8 bps): ort {np.nanmean(nul):+.1f}, %5-%95 [{np.nanpercentile(nul, 5):+.1f}, {np.nanpercentile(nul, 95):+.1f}] bps')
# ENKAI-özgü mü? aynı sinyal XU030 intra üzerinde (endeks vadelisi, 3 bps)
run('B kontrol: z>1 -TUR_{t-1} -> XU030 intra (endeks vadelisi)', p_b, X30['intra'], costs=(0, 3))

print('\n==================== (c) ENKAI USDTRY_{t-1} ====================')
p_c = V.zpos(USD, 1.0)
run('C z>1 USD_{t-1} -> ENKAI intra', p_c, E['intra'])
run('C z>1 USD_{t-1} -> ENKAI intra hedge (XU030), +3bps', p_c, hedged(E['intra']), costs=(3, 11, 18))
run('C z>2 USD_{t-1} -> ENKAI intra', V.zpos(USD, 2.0), E['intra'])
run('C z>1 USD_{t-1} -> ENKAI intra (2021-22 HARİÇ)', p_c, ex)
nul = shift_null(USD, 1.0, E['intra'])
print(f'   kaydırılmış-sinyal null (OOS, 8 bps): ort {np.nanmean(nul):+.1f}, %5-%95 [{np.nanpercentile(nul, 5):+.1f}, {np.nanpercentile(nul, 95):+.1f}] bps')

print('\n==================== (b)+(c) birleşik: z(-TUR)+z(USD) ====================')
def z(s):
    s2 = s.dropna(); mu = s2.rolling(250, min_periods=60).mean().shift(1); sd = s2.rolling(250, min_periods=60).std().shift(1)
    return ((s2 - mu) / sd).reindex(s.index)
comb = (z(-TUR).fillna(0) + z(USD).fillna(0)) / 2
pc = np.sign(comb).where(comb.abs() > 1.0, 0.0).fillna(0)
run('BC z_ort>1 -> ENKAI intra', pc, E['intra'])
pd.DataFrame(rows).to_csv(os.path.join(V.CODE, 'res_bt.csv'), index=False)

# korelasyon TUR vs USD (aynı bilgi mi?)
d = pd.concat([TUR.rename('TUR'), USD.rename('USD')], axis=1).dropna()
print('\ncorr(TUR_{t-1}, USD_{t-1}) yıllara göre:', d.groupby(d.index.year).apply(lambda g: round(g.TUR.corr(g.USD), 2)).to_dict())
