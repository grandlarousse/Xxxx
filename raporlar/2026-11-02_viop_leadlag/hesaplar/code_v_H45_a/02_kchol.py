"""H45(a) KCHOL açılış NAV ayrışması -> KCHOL gün-içi. Bağımsız yeniden üretim + mekanik (kendi gap'i / bid-ask) ayrıştırma + plasebo.
sig_t = NAVgap_t - KCHOLgap_t  (açılış müzayedesinden sonra bilinir) ; hedef KCHOL intra_t = ln(c_t/o_t)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vlib as V, numpy as np, pandas as pd
pd.set_option('display.width', 250)
rng = np.random.default_rng(45)
W = {'TUPRS': .33, 'FROTO': .20, 'YKBNK': .24, 'ARCLK': .07, 'TOASO': .04, 'AYGAZ': .03, 'OTKAR': .02, 'TTRAK': .03}
KOC = {'KCHOL', 'TUPRS', 'FROTO', 'YKBNK', 'ARCLK', 'TOASO', 'AYGAZ', 'OTKAR', 'TTRAK'}
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]


def basket_gap(D, w, need=None):
    G = pd.DataFrame({s: D[s]['gap'] for s in w})
    ws = pd.Series(w)
    M = G.notna().mul(ws, axis=1)
    out = (G.fillna(0) * ws).sum(axis=1) / M.sum(axis=1)
    ok = M.sum(axis=1) >= 0.6 * ws.sum()
    if need: ok &= G[need].notna().all(axis=1)
    return out.where(ok)


def line(lab, y, x):
    c, t, n = V.corr_t(y, x); ci, ti, ni = V.corr_t(y, x, V.IS0, V.SPLIT); co, to, no = V.corr_t(y, x, V.SPLIT)
    yr = V.by_year(y, x); same = (np.sign(yr.dropna()) == np.sign(c)).mean()
    print(f'{lab:58s} corr {c:+.3f} t {t:+.2f} n {n} | IS {ci:+.3f} t {ti:+.2f} | OOS {co:+.3f} t {to:+.2f} | yıl aynı işaret {same:.2f}')
    return {'test': lab, 'c': c, 't': t, 'n': n, 'c_IS': ci, 't_IS': ti, 'c_OOS': co, 't_OOS': to, 'yr_same': same,
            'by_year': json.dumps(yr.round(3).to_dict())}


rows = []
for strict in [False, True]:
    print(f'\n######## strict açılış filtresi = {strict} ########')
    K = V.decomp('KCHOL', strict); D = {s: V.decomp(s, strict) for s in W}
    X30 = V.decomp('XU030', strict); X100 = V.decomp('XU100', strict)
    nav = basket_gap(D, W, ['TUPRS', 'FROTO', 'YKBNK'])
    sig = nav - K['gap']
    tag = ' [strict]' if strict else ''
    rows.append(line('A1 sig=NAVgap-Kgap -> Kintra' + tag, K['intra'], sig))
    rows.append(line('A1b sig -> Kintra (2016+, 2014-15 bozuk açılış hariç)' + tag, K['intra'][K.index >= '2016-01-01'], sig))
    rows.append(line('A2 -Kgap (sadece kendi gap fade) -> Kintra' + tag, K['intra'], -K['gap']))
    rows.append(line('A3 NAVgap (tek başına) -> Kintra' + tag, K['intra'], nav))
    rows.append(line('A4 XU030gap - Kgap (plasebo sepet) -> Kintra' + tag, K['intra'], X30['gap'] - K['gap']))
    rows.append(line('A5 XU100gap - Kgap (plasebo) -> Kintra' + tag, K['intra'], X100['gap'] - K['gap']))
    # piyasa-nötr hedef (XU030 vadelisiyle hedge): Kintra - b*XU030intra (b geçmiş 250g yerine tam dönem beta; tanı amaçlı)
    b = V.ols(K['intra'], [X30['intra']])['b'].iloc[1]
    rows.append(line(f'A6 sig -> Kintra - {b:.2f}*XU030intra (hedge)' + tag, K['intra'] - b * X30['intra'], sig))
    # Regresyon ayrıştırması
    print('  Regresyonlar (NW t, katsayılar intra birimi):')
    for nm, Xs, names in [('Kintra ~ NAVgap + Kgap', [nav, K['gap']], ['NAVgap', 'Kgap']),
                          ('Kintra ~ NAVgap + Kgap + XU030gap', [nav, K['gap'], X30['gap']], ['NAVgap', 'Kgap', 'X30gap']),
                          ('Kintra ~ sig + Kgap', [sig, K['gap']], ['sig', 'Kgap']),
                          ('Kintra ~ (NAVgap-X30gap) + (X30gap-Kgap) + X30gap', [nav - X30['gap'], X30['gap'] - K['gap'], X30['gap']], ['NAVx', 'X30-K', 'X30gap'])]:
        for lab, s0, s1 in [('ALL', V.IS0, None), ('IS', V.IS0, V.SPLIT), ('OOS', V.SPLIT, None), ('2016+', pd.Timestamp('2016-01-01'), None)]:
            y = K['intra']; m = (y.index >= s0) & ((y.index < s1) if s1 is not None else True)
            r = V.ols(y[m], [x[m] for x in Xs], names=names)
            print(f'   {nm:55s} {lab:5s} n={r["n"]:4d} ' + ' '.join(f'{k}={r["b"][k]:+.3f}(t{r["t"][k]:+.2f})' for k in names))
            rows.append({'test': f'REG {nm} {lab}{tag}', **{f'b_{k}': r['b'][k] for k in names}, **{f't_{k}': r['t'][k] for k in names}, 'n': r['n']})

# ---------------- plasebo: rastgele Koç-dışı sepetler ----------------
print('\n######## Plasebo: Koç-dışı VİOP hisselerinden rastgele 8\'li sepetler (aynı ağırlık vektörü) ########')
K = V.decomp('KCHOL'); X30 = V.decomp('XU030')
pool = [s for s in VIOP if s not in KOC]
DP = {}
for s in pool:
    try:
        d = V.decomp(s)
        if d['gap'].notna().sum() > 1500: DP[s] = d
    except Exception as e:
        pass
pool = list(DP)
nav = basket_gap({s: V.decomp(s) for s in W}, W, ['TUPRS', 'FROTO', 'YKBNK'])
def stats(bg):
    s = bg - K['gap']
    c, t, n = V.corr_t(K['intra'], s)
    r = V.ols(K['intra'], [bg, K['gap']], names=['B', 'K'])
    co, to, _ = V.corr_t(K['intra'], s, V.SPLIT)
    return t, r['t']['B'], r['b']['B'], to
real = stats(nav)
wv = list(W.values())
res = []
for i in range(300):
    pick = list(rng.choice(pool, 8, replace=False))
    bg = basket_gap(DP, dict(zip(pick, wv)))
    res.append(stats(bg))
R = pd.DataFrame(res, columns=['t_sig', 't_Bgap_ctrlK', 'b_Bgap_ctrlK', 't_sig_OOS'])
print(f'Gerçek Koç NAV: t_sig={real[0]:.2f}, NAVgap katsayısı (Kgap kontrollü) b={real[2]:.3f} t={real[1]:.2f}, OOS t_sig={real[3]:.2f}')
print('Rastgele 300 sepet dağılımı:'); print(R.describe(percentiles=[.05, .5, .95]).round(3).to_string())
print(f'Gerçek NAV t_sig yüzdeliği: {(R.t_sig < real[0]).mean():.3f}; Kgap-kontrollü sepet t yüzdeliği: {(R.t_Bgap_ctrlK < real[1]).mean():.3f}; OOS t_sig yüzdeliği: {(R.t_sig_OOS < real[3]).mean():.3f}')
R.to_csv(os.path.join(V.CODE, 'res_placebo_baskets.csv'), index=False)

# ---------------- genel olgu: 47 hisse için (XU030gap - kendi gap) -> kendi intra ----------------
print('\n######## Genellik: her VİOP hissesi için sig_S = XU030gap - Sgap -> S intra ve Sintra ~ X30gap + Sgap ########')
g = []
for s in VIOP:
    try: d = DP.get(s) if s in DP else V.decomp(s)
    except Exception: continue
    c, t, n = V.corr_t(d['intra'], X30['gap'] - d['gap'])
    co, to, _ = V.corr_t(d['intra'], X30['gap'] - d['gap'], V.SPLIT)
    r = V.ols(d['intra'], [X30['gap'], d['gap']], names=['X30', 'S'])
    if r is None: continue
    g.append({'stock': s, 'c': c, 't': t, 't_OOS': to, 'b_X30gap_ctrlS': r['b']['X30'], 't_X30gap_ctrlS': r['t']['X30'], 'b_Sgap': r['b']['S'], 't_Sgap': r['t']['S'], 'n': n})
G = pd.DataFrame(g).sort_values('t', ascending=False)
print(G.round(3).to_string(index=False))
print(f"Özet: t>3 olan hisse {int((G.t > 3).sum())}/{len(G)}; medyan t {G.t.median():.2f}; X30gap (Sgap kontrollü) t>2: {int((G.t_X30gap_ctrlS > 2).sum())}; KCHOL sırası {list(G.stock).index('KCHOL') + 1}")
G.to_csv(os.path.join(V.CODE, 'res_generic_gapdiv.csv'), index=False)
pd.DataFrame(rows).to_csv(os.path.join(V.CODE, 'res_kchol.csv'), index=False)
