"""Veri güdümlü tarama: 6 hisse x panel_ret_bistcal'deki TÜM semboller.
Metrikler: senkron corr, XU100 kontrollü kısmi corr (pc), lag1 gap, lag1 intra, lag1 intra (XU100 intra kontrollü),
Asya sembolleri için lag0->intra, ters yön (hisse_{t-1} -> X_t). IS/OOS. NW(5) t. BH-FDR her metrik ailesi içinde.
Çıktı: code_holding/res_scan.csv (+ özet yazdırır)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hc, ll, numpy as np, pandas as pd

def nwt(y, x, L=5):
    """y = a + b x OLS, Newey-West t (hızlı numpy)."""
    m = ~(np.isnan(y) | np.isnan(x)); y = y[m]; x = x[m]; n = len(y)
    if n < 250: return np.nan, np.nan, n
    xc = x - x.mean(); yc = y - y.mean(); sxx = (xc * xc).sum()
    if sxx <= 0: return np.nan, np.nan, n
    b = (xc * yc).sum() / sxx; u = yc - b * xc; s = xc * u
    S = (s * s).sum()
    for l in range(1, L + 1):
        S += 2 * (1 - l / (L + 1)) * (s[l:] * s[:-l]).sum()
    t = b / np.sqrt(S / sxx ** 2)
    c = np.corrcoef(x, y)[0, 1]
    return c, t, n

def resid(y, X):
    m = ~(np.isnan(y) | np.isnan(X).any(1)); out = np.full(len(y), np.nan)
    if m.sum() < 250: return out
    C = np.column_stack([np.ones(m.sum()), X[m]]); out[m] = y[m] - C @ np.linalg.lstsq(C, y[m], rcond=None)[0]
    return out

P = hc.panel(); P = P[P.index >= hc.START]
cat = pd.read_csv(hc.SCR + '/data/catalog.csv').set_index('sym')
DP = pd.read_parquet(hc.SCR + '/data/panel_decomp_bist.parquet')
STOCKS = ['KCHOL', 'SAHOL', 'DOHOL', 'ALARK', 'ENKAI', 'EKGYO']
ASIA = ('Asia/Tokyo', 'Asia/Seoul', 'Australia/Sydney', 'Asia/Shanghai', 'Asia/Hong_Kong', 'Asia/Taipei', 'Asia/Singapore', 'Asia/Jakarta', 'Asia/Kuala_Lumpur', 'Asia/Bangkok', 'Pacific/Auckland', 'Asia/Manila')
idx = P.index
m = P['XU100.IS'].values
dm = DP['XU100'].reindex(idx)
isx = (idx >= hc.IS0) & (idx < hc.SPLIT); oos = idx >= hc.SPLIT
FXS = set(cat.index[(cat['type'].astype(str) == 'CURRENCY') | cat.index.str.endswith('=X')])
for _s in FXS:
    pass  # panel artık ll.FX_FIX ile üretildi (koordinatör, 01.11.2026) -> ek kaydırma YOK
syms = [s for s in P.columns if s in cat.index and cat.loc[s, 'n'] >= 750 and cat.loc[s, 'zero_frac'] < 0.30]
print('sembol sayısı:', len(syms))
rows = []
for st in STOCKS:
    a = P[st + '.IS'].values
    d = DP[st].reindex(idx); gap = d['gap'].values; intra = d['intra'].values
    ra = resid(a, m[:, None])
    ri = resid(intra, dm['intra'].values[:, None])
    for x in syms:
        if x in (st + '.IS',): continue
        b = P[x].values; b1 = np.r_[np.nan, b[:-1]]; a1 = np.r_[np.nan, a[:-1]]
        o = {'stock': st, 'sym': x, 'group': cat.loc[x, 'group'], 'tz': cat.loc[x, 'tz'], 'zero_frac': cat.loc[x, 'zero_frac']}
        o['c0'], o['t0'], o['n'] = nwt(a, b)
        rb = resid(b, m[:, None])
        o['pc'], o['pc_t'], _ = nwt(ra, rb)
        o['pc_IS'], o['pc_IS_t'], _ = nwt(ra[isx], rb[isx])
        o['pc_OOS'], o['pc_OOS_t'], _ = nwt(ra[oos], rb[oos])
        o['gap1'], o['gap1_t'], _ = nwt(gap, b1)
        o['intra1'], o['intra1_t'], o['n_intra'] = nwt(intra, b1)
        o['intra1_IS_t'] = nwt(intra[isx], b1[isx])[1]; o['intra1_OOS_t'] = nwt(intra[oos], b1[oos])[1]
        o['ipc1'], o['ipc1_t'], _ = nwt(ri, b1)
        o['ipc1_IS_t'] = nwt(ri[isx], b1[isx])[1]; o['ipc1_OOS_t'] = nwt(ri[oos], b1[oos])[1]
        if str(o['tz']) in ASIA:  # Asya kapanışı BIST açılışından önce/başında -> lag0 -> intra
            o['intra0'], o['intra0_t'], _ = nwt(intra, b)
            o['ipc0'], o['ipc0_t'], _ = nwt(ri, b)
        o['rev'], o['rev_t'], _ = nwt(b, a1)
        rows.append(o)
R = pd.DataFrame(rows)
for fam in ['pc', 'gap1', 'intra1', 'ipc1', 'intra0', 'ipc0', 'rev']:
    tt = R[fam + '_t'] if fam + '_t' in R else None
    if tt is None: continue
    p = ll.t_to_p(tt.values.astype(float)); rej, padj = ll.fdr(p, 0.05)
    R[fam + '_padj'] = padj; R[fam + '_fdr'] = rej
R.to_csv(os.path.join(hc.CODE, 'res_scan.csv'), index=False)
print('toplam çift:', len(R), ' aile başına test:', len(R))
for fam in ['pc', 'gap1', 'intra1', 'ipc1', 'ipc0', 'rev']:
    if fam + '_fdr' in R:
        print(fam, 'FDR geçen:', int(R[fam + '_fdr'].sum()), ' / test', int(R[fam + '_t'].notna().sum()))
