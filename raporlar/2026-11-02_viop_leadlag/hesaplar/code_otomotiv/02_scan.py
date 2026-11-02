"""Veri güdümlü tarama: 6 hisse x panel_ret_bistcal'deki TÜM semboller.
Aileler (her biri ayrı BH-FDR, q=0.05):
  F1 sync_pc : corr(hisse_t, sürücü_t | XU100_t)            2010+
  F2 lead_gap: corr(gap_t, sürücü_{t-L})                       2014+
  F3 lead_intra: corr(intra_t, sürücü_{t-L})                   2014+
  F4 lead_intra_pc: corr(intra_t, sürücü_{t-L} | XU100 gap_t, kendi gap_t)  2014+  (işlenebilir; açılış bilgisi kontrol)
L = 0 (Kore/Japonya/Tayvan: BIST açılışından önce kapanır), 1 (diğer; BIST sürücüleri dahil).
p-değerleri iid yaklaşımı (tarama); FDR'den geçenler için Newey-West t ve IS/OOS ayrıca hesaplanır.
Çıktı: res/scan_all.csv, res/scan_fdr_hits.csv"""
from common import *
from scipy import stats

P = pd.read_parquet('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/panel_ret_bistcal.parquet')
cat = pd.read_csv('/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/data/catalog.csv').set_index('sym')
for c in P.columns:
    if not c.endswith('.IS'): P[c] = P[c].where(P[c] != 0)
m = P['XU100.IS']
xg = D('XU100')['gap']

def pc_vec(y, X, ctrl):
    """y: Series, X: DataFrame of drivers, ctrl: DataFrame controls. Her sütun için ortak örneklemde kısmi korelasyon."""
    out = []
    for c in X.columns:
        df = pd.concat([y.rename('y'), X[c].rename('x'), ctrl], axis=1).dropna()
        n = len(df)
        if n < 150 or df['x'].std() == 0: out.append((c, np.nan, n)); continue
        if ctrl.shape[1]:
            C = np.column_stack([np.ones(n), df[ctrl.columns].values])
            ry = df['y'].values - C @ np.linalg.lstsq(C, df['y'].values, rcond=None)[0]
            rx = df['x'].values - C @ np.linalg.lstsq(C, df['x'].values, rcond=None)[0]
        else:
            ry = df['y'].values; rx = df['x'].values
        out.append((c, float(np.corrcoef(ry, rx)[0, 1]), n))
    return pd.DataFrame(out, columns=['driver', 'r', 'n']).set_index('driver')

def p_of(r, n):
    t = r * np.sqrt((n - 2) / np.maximum(1 - r ** 2, 1e-12)); return 2 * stats.t.sf(np.abs(t), n - 2), t

rows = []
for st in STOCKS:
    sym = st + '.IS'
    a = P[sym]; a = a[a.index >= '2010-01-01']
    drivers = [c for c in P.columns if c not in (sym, 'XU100.IS')]
    X = P[drivers]
    d = D(st); d = d[d.index >= '2014-01-01']
    # lead matrisi: sürücüye göre L
    L = pd.Series({c: lead_lag(c) for c in drivers})
    XL = pd.concat([X[c].shift(L[c]) for c in drivers], axis=1); XL.columns = drivers
    f1 = pc_vec(a, X, m.to_frame('m'))
    f0 = pc_vec(a, X, pd.DataFrame(index=a.index))
    f2 = pc_vec(d['gap'], XL, pd.DataFrame(index=d.index))
    f3 = pc_vec(d['intra'], XL, pd.DataFrame(index=d.index))
    f4 = pc_vec(d['intra'], XL, pd.concat([xg.rename('xg'), d['gap'].rename('og')], axis=1))
    for fam, f in [('sync_raw', f0), ('sync_pc', f1), ('lead_gap', f2), ('lead_intra', f3), ('lead_intra_pc', f4)]:
        g = f.copy(); g['stock'] = st; g['family'] = fam; g['L'] = L.reindex(g.index).values
        g['p'], g['t_iid'] = p_of(g['r'], g['n'])
        rows.append(g.reset_index())
    print(st, 'scanned', flush=True)

S = pd.concat(rows, ignore_index=True)
S['group'] = S['driver'].map(cat['group']); S['name'] = S['driver'].map(cat['name'])
S['fdr_rej'] = False; S['p_bh'] = np.nan
for fam in S.family.unique():
    i = S.family == fam
    rej, pa = ll.fdr(S.loc[i, 'p'].values, q=0.05)
    S.loc[i, 'fdr_rej'] = rej; S.loc[i, 'p_bh'] = pa
S.to_csv(os.path.join(RES, 'scan_all.csv'), index=False)

# FDR'den geçenler için NW t + IS/OOS (yalnız F1, F3, F4)
H = S[S.fdr_rej & S.family.isin(['sync_pc', 'lead_intra', 'lead_intra_pc'])].copy()
ext = []
for idx, r in H.iterrows():
    st, dr, fam = r['stock'], r['driver'], r['family']
    sym = st + '.IS'; b = P[dr]; d = D(st)
    if fam == 'sync_pc':
        y = P[sym]; x = b; ctrl = [m]
    elif fam == 'lead_intra':
        y = d['intra']; x = b.shift(int(r['L'])); ctrl = []
    else:
        y = d['intra']; x = b.shift(int(r['L'])); ctrl = [xg, d['gap']]
    sp, is0 = split_for(y, x)
    if not ctrl:
        c_is, t_is, _ = corr_t(y, x, start=is0, end=sp); c_oos, t_oos, _ = corr_t(y, x, start=sp); _, t_nw, _ = corr_t(y, x, start='2010-01-01')
    else:
        c_is, t_is, _ = pcorr(y, x, ctrl, start=is0, end=sp); c_oos, t_oos, _ = pcorr(y, x, ctrl, start=sp); _, t_nw, _ = pcorr(y, x, ctrl, start='2010-01-01')
    ext.append({'idx': idx, 't_nw': t_nw, 'r_IS': c_is, 't_IS': t_is, 'r_OOS': c_oos, 't_OOS': t_oos, 'split': str(sp.date())})
E = pd.DataFrame(ext).set_index('idx'); H = H.join(E)
H.to_csv(os.path.join(RES, 'scan_fdr_hits.csv'), index=False)
print('test sayısı/aile:', S.groupby('family').size().to_dict())
print('FDR geçen/aile:', S[S.fdr_rej].groupby(['family', 'stock']).size().unstack(fill_value=0).to_string())
