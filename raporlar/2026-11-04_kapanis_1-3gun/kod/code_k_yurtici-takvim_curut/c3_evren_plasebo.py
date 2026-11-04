"""Plasebo evreni: aynı göreli momentum (k3, |z|>1.5, h2) ve aynı Z20>2 dönüş kuralı VİOP47'nin tüm sıralı çiftlerinde.
Amaç: Koza (TRMET/TRALT) ve TCELL–TTKOM sonuçları evren içinde ne kadar sıra dışı? E0'daki genel 'uzlaşma gecikmesi' momentumu var mı?"""
from curlib import *
import itertools
cal = vcal()
FW = pd.read_parquet(RES + '/_fwd_cache.parquet'); SR = pd.read_parquet(RES + '/_spot_ret.parquet')
L = pd.read_csv(S + '/out/y_viop_likidite.csv'); U = [u for u in L.und if u in SR.columns and f'{u}|2|E0' in FW]
U = [u for u in U if u not in ('XU030',)]
def beta(y, x, w=250, mp=120):
    return (y.rolling(w, min_periods=mp).cov(x) / x.rolling(w, min_periods=mp).var()).shift(1)
def fast_t(dates_idx, x, lag):
    # dates_idx: takvim pozisyonları (sıralı, tekil), x: getiri; NW(lag) gün serisi üzerinde (her gün tek işlem)
    ok = np.isfinite(x); x = x[ok]; p = dates_idx[ok]; n = len(x)
    if n < 30: return np.nan, np.nan, n
    m = x.mean(); e = x - m; Uf = np.zeros(p.max() - p.min() + 1); Uf[p - p.min()] = e
    v = Uf @ Uf
    for l in range(1, lag + 1): v += 2 * (1 - l / (lag + 1)) * (Uf[l:] @ Uf[:-l])
    return m * 1e4, m / (np.sqrt(v) / n), n
R = SR.reindex(cal)
rows = []
F2 = {(u, e): FW[f'{u}|2|{e}'].values for u in U for e in ['E0', 'E2']}
F3 = {(u, e): FW[f'{u}|3|{e}'].values for u in U for e in ['E0', 'E2']}
Lg = {u: np.log(np.exp(SR[u].fillna(0).cumsum())).reindex(cal).values for u in U}  # log fiyat (adj) yaklaşığı
for a, b in itertools.permutations(U, 2):
    ya, yb = R[a], R[b]
    bb = beta(ya, yb).clip(0.3, 2.0)
    uu = ya - bb * yb
    z3 = uu.rolling(3, min_periods=3).sum() / (uu.rolling(60, min_periods=40).std() * np.sqrt(3))
    on = (z3.abs() > 1.5).values
    pos = np.where(on)[0]
    if len(pos) < 30: continue
    sd = np.sign(z3.values[pos]); bv = np.nan_to_num(bb.values[pos], nan=1.0)
    rec = dict(a=a, b=b)
    for e in ['E0', 'E2']:
        x = sd * (F2[(a, e)][pos] - bv * F2[(b, e)][pos]) / (1 + bv)
        m, t, n = fast_t(pos, x, 2); rec[f'mom_{e}_g'] = m; rec[f'mom_{e}_t'] = t; rec['n_mom'] = n
    # Z20>2 dönüş (log fiyat yayılımı), h3
    sp = pd.Series(Lg[a] - np.nan_to_num(bb.values, nan=1.0) * Lg[b], index=cal)
    zz = (sp - sp.rolling(20, min_periods=20).mean()) / sp.rolling(20, min_periods=20).std()
    on2 = (zz.abs() > 2).values; p2 = np.where(on2)[0]
    if len(p2) >= 30:
        sd2 = -np.sign(zz.values[p2]); bv2 = np.nan_to_num(bb.values[p2], nan=1.0)
        for e in ['E0', 'E2']:
            x = sd2 * (F3[(a, e)][p2] - bv2 * F3[(b, e)][p2]) / (1 + bv2)
            m, t, n = fast_t(p2, x, 3); rec[f'rev_{e}_g'] = m; rec[f'rev_{e}_t'] = t; rec['n_rev'] = n
    rows.append(rec)
D = pd.DataFrame(rows); D.to_csv(RES + '/evren_plasebo.csv', index=False)
print('çift sayısı', len(D))
for c in ['mom_E0_t', 'mom_E2_t', 'rev_E0_t', 'rev_E2_t']:
    s = D[c].dropna(); print(f'{c}: ort {s.mean():+.2f} medyan {s.median():+.2f} sd {s.std():.2f} | >2: {(s > 2).mean():.3f} >2,5: {(s > 2.5).mean():.3f} >3: {(s > 3).mean():.3f} | max {s.max():.2f}')
for c in ['mom_E0_g', 'mom_E2_g', 'rev_E0_g', 'rev_E2_g']:
    s = D[c].dropna(); print(f'{c}: ort {s.mean():+.1f} bps medyan {s.median():+.1f}')
for a, b in [('TRMET', 'TRALT'), ('TRALT', 'TRMET'), ('TCELL', 'TTKOM'), ('TTKOM', 'TCELL')]:
    r = D[(D.a == a) & (D.b == b)]
    if len(r):
        r = r.iloc[0]
        rk = {c: float((D[c] >= r[c]).mean()) for c in ['mom_E0_t', 'mom_E2_t', 'rev_E0_t', 'rev_E2_t']}
        print(a, b, {c: round(float(r[c]), 2) for c in ['mom_E0_g', 'mom_E0_t', 'mom_E2_g', 'mom_E2_t', 'rev_E0_g', 'rev_E0_t', 'rev_E2_g', 'rev_E2_t']}, 'üst kuyruk payı', {k: round(v, 3) for k, v in rk.items()})
print('En yüksek mom_E2_t 10 çift:'); print(D.sort_values('mom_E2_t').tail(10)[['a', 'b', 'mom_E0_g', 'mom_E0_t', 'mom_E2_g', 'mom_E2_t', 'n_mom']].round(2).to_string())
print('En yüksek rev_E2_t 10 çift:'); print(D.sort_values('rev_E2_t').tail(10)[['a', 'b', 'rev_E0_g', 'rev_E0_t', 'rev_E2_g', 'rev_E2_t', 'n_rev']].round(2).to_string())
