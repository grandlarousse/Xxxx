# -*- coding: utf-8 -*-
"""B5 icin secim yanliligi / null dagilimi: XBANK ~ surucu | XU100 kismi korelasyonu, tum BIST-disi semboller,
her 12 aylik pencere (Kasim->Ekim). 2025-11..2026-10 penceresi tarihsel olarak olagan disi mi?"""
import sys, os, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import vb
OUT = os.path.dirname(os.path.abspath(__file__)) + '/res'
cat = pd.read_csv(vb.D + '/catalog.csv')
syms = sorted(os.path.basename(p)[:-8] for p in glob.glob(vb.D + '/daily/*.parquet'))
syms = [s for s in syms if not s.endswith('.IS')]
TRISH = {'TUR', 'TKC', 'AKBTY', 'TKGBY', 'TRY=X', 'EURTRY=X', 'TRYUSD=X', 'GBPTRY=X', 'JPYTRY=X'}
R = {}
for s in syms:
    try:
        r = vb.ext_ret(s)
    except Exception as e:
        continue
    r = r[r.index >= '2010-11-01']
    if r.notna().sum() < 500: continue
    R[s] = r
M = pd.DataFrame(R)
print('surucu sayisi', M.shape)
y = vb.ret('XBANK.IS').reindex(M.index); x = vb.ret('XU100.IS').reindex(M.index)

def window_pc(a, b):
    m = (M.index >= a) & (M.index <= b)
    Y = y[m]; X = x[m]; D = M[m]
    ok = Y.notna() & X.notna()
    Y = Y[ok]; X = X[ok]; D = D[ok]
    # sifir getiri orani (tatil/bayat) filtresi
    zf = (D == 0).mean()
    nn = D.notna().sum()
    keep = (zf < 0.3) & (nn >= 0.8 * len(Y))
    D = D.loc[:, keep]
    # XU100 uzerine artiklastir (her sutun icin kendi ortak orneklemi: NaN -> sutun ortalamasi yerine maske)
    Xc = X - X.mean(); bx = (Y * Xc).sum() / (Xc ** 2).sum(); ey = (Y - Y.mean()) - bx * Xc
    out = {}
    Dm = D.notna()
    for c in D.columns:
        mm = Dm[c].values
        d = D[c].values[mm]; xc = X.values[mm] - X.values[mm].mean(); yy = Y.values[mm] - Y.values[mm].mean()
        ed = (d - d.mean()) - ((d - d.mean()) @ xc / (xc @ xc)) * xc
        e_y = yy - (yy @ xc / (xc @ xc)) * xc
        out[c] = np.corrcoef(e_y, ed)[0, 1]
    return pd.Series(out), len(Y)

rows = []
allpc = {}
for yr in range(2011, 2026):
    a, b = f'{yr}-11-01', f'{yr+1}-10-31'
    s, n = window_pc(a, b)
    allpc[f'{yr}-11..{yr+1}-10'] = s
    s2 = s.drop([c for c in s.index if c in TRISH], errors='ignore')
    rows.append(dict(window=f'{yr}-11..{yr+1}-10', n_days=n, n_drv=len(s2), p50_abs=s2.abs().median(), p95_abs=s2.abs().quantile(.95),
                     p99_abs=s2.abs().quantile(.99), max_abs=s2.abs().max(), n_abs_gt_020=int((s2.abs() > 0.20).sum()), n_abs_gt_025=int((s2.abs() > 0.25).sum()),
                     top=' '.join(f"{k}:{v:+.2f}" for k, v in s2.reindex(s2.abs().sort_values(ascending=False).index[:6]).items()),
                     BZ=s.get('BZ=F', np.nan), SAN=s.get('SAN.MC', np.nan), EMB=s.get('EMB', np.nan), BBVA=s.get('BBVA.MC', np.nan)))
W = pd.DataFrame(rows)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 120)
print(W[['window', 'n_days', 'n_drv', 'p50_abs', 'p95_abs', 'p99_abs', 'max_abs', 'n_abs_gt_020', 'n_abs_gt_025', 'BZ', 'SAN', 'EMB', 'BBVA']].round(3).to_string())
print()
for _, r in W.iterrows(): print(r.window, r.top)
last = allpc['2025-11..2026-10'].drop([c for c in TRISH], errors='ignore')
n_drv = len(last); ss = last.abs().sort_values(ascending=False)
print('\nSon pencere: surucu', n_drv, '; BZ sirasi', list(ss.index).index('BZ=F') + 1, 'SAN', list(ss.index).index('SAN.MC') + 1, 'EMB', list(ss.index).index('EMB') + 1, 'BBVA.MC', list(ss.index).index('BBVA.MC') + 1)
# null: n=249 icin |pc| > 0.226 olasiligi ~ 2*(1-Phi(0.226*sqrt(247)))
from math import erf, sqrt
for thr in [0.20, 0.226, 0.26, 0.289]:
    z = thr * sqrt(247); p = 2 * (1 - 0.5 * (1 + erf(z / sqrt(2))))
    print(f'  |pc|>{thr}: bagimsiz null p={p:.2e}; beklenen yanlis-pozitif sayisi (n_drv={n_drv}) = {p*n_drv:.2f}; gozlenen = {(last.abs()>thr).sum()}')
W.to_csv(f'{OUT}/b5_window_scan.csv', index=False)
pd.DataFrame(allpc).to_csv(f'{OUT}/b5_window_pc_all.csv')
