import sys, numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim
H = 332
LV = [4.0, 4.5, 5.0, 5.5, 6.0]
pols = [(h, 0.0, 6, 0, 3, 0.75) for h in LV]
rows = []
for h3 in (5, 6, 7, 8):
    for seed in (101, 202):
        pr, _ = sim.sample_params(h3, seed, 1000)
        prd = sim.derive(pr, h3)
        for lam in (0.0, 0.02):
            r = sim.ref_sim(prd, pols, H, lam=lam)
            P = r['P']; E = r['sumE']; ev = r['ever']; kl = r['klev']
            best = P.max(axis=1, keepdims=True)
            for j, h in enumerate(LV):
                rows.append(dict(h3=h3, seed=seed, lam=lam, h=h,
                    cokus=ev[:, j].mean(),
                    P_ort=P[:, j].mean(), P_goreli_4=(P[:, j] / P[:, 0]).mean() - 1,
                    P_p05_goreli_4=np.quantile(P[:, j] / P[:, 0], 0.05) - 1,
                    E_goreli_4=(E[:, j] / E[:, 0]).mean() - 1,
                    en_iyi_pay=(P[:, j] >= best[:, 0] - 1e-12).mean(),
                    pisman_ort=(1 - P[:, j] / best[:, 0]).mean(),
                    pisman_p95=np.quantile(1 - P[:, j] / best[:, 0], 0.95),
                    K0=(kl[:, j] <= 0).mean(), K1=(kl[:, j] <= 1).mean(), K2=(kl[:, j] <= 2).mean(), K3=(kl[:, j] <= 3).mean(),
                    klmax=int(kl.max()), klmin=int(kl.min())))
import csv
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cikti', 'kiyas_4_6.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
def agg(h3, lam, h, k):
    v = [r[k] for r in rows if r['h3'] == h3 and r['lam'] == lam and r['h'] == h]
    return sum(v) / len(v), max(v) - min(v)
print('klev aralığı', rows[0]['klmin'], max(r['klmax'] for r in rows))
for lam in (0.0, 0.02):
    print('\n=== lam', lam, '(6 gün/hafta, hB=0, son 3 gün x0,75, ufuk 332)')
    for h3 in (5, 6, 7, 8):
        print('-- tavan', h3)
        print(' saat  hafta  çöküş%  P(4sa göre)%  P p05%  öğrenme(4sa göre)%  en iyi olduğu çekim%  pişman ort%  p95%   K0   K1   K2   K3  | tohum farkı (çöküş, P)')
        for h in LV:
            g = lambda k: agg(h3, lam, h, k)
            print(' %3.1f   %4.0f   %5.1f   %+6.1f      %+6.1f      %+6.1f            %5.1f            %5.1f     %5.1f  %4.0f %4.0f %4.0f %4.0f  | %.3f %.3f' % (
                h, 6 * h, 100 * g('cokus')[0], 100 * g('P_goreli_4')[0], 100 * g('P_p05_goreli_4')[0], 100 * g('E_goreli_4')[0],
                100 * g('en_iyi_pay')[0], 100 * g('pisman_ort')[0], 100 * g('pisman_p95')[0],
                100 * g('K0')[0], 100 * g('K1')[0], 100 * g('K2')[0], 100 * g('K3')[0], g('cokus')[1], g('P_goreli_4')[1]))
