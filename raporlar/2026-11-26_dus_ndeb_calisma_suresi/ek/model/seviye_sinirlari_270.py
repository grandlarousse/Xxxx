import sys, numpy as np, csv
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim
H = 270
LV = [3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5]
rows = []
for h3 in (5, 6, 7, 8):
    acc = {}
    for seed in (101, 202):
        pr, _ = sim.sample_params(h3, seed, 1000); prd = sim.derive(pr, h3)
        for lam in (0.0, 0.02):
            for n in (0, 4):
                pols = [(h, 0.0, 6, n, 3, 0.75) for h in LV]
                r = sim.ref_sim(prd, pols, H, lam=lam)
                kl = r['klev']; ev = r['ever']; P = r['P']
                for j, h in enumerate(LV):
                    a = acc.setdefault((lam, n, h), dict(K0=[], K1=[], K2=[], K3=[], cok=[], P=[]))
                    a['K0'].append((kl[:, j] <= 0).mean()); a['K1'].append((kl[:, j] <= 1).mean())
                    a['K2'].append((kl[:, j] <= 2).mean()); a['K3'].append((kl[:, j] <= 3).mean())
                    a['cok'].append(ev[:, j].mean()); a['P'].append(P[:, j])
    for (lam, n, h), a in acc.items():
        rows.append(dict(h3=h3, lam=lam, hafif_hafta=n, h=h, K0=np.mean(a['K0']), K1=np.mean(a['K1']), K2=np.mean(a['K2']),
                         K3=np.mean(a['K3']), cokus=np.mean(a['cok']), P_ort=float(np.concatenate(a['P']).mean())))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cikti', 'seviye_sinirlari_270.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
def lim(h3, lam, n, k, thr):
    v = [r['h'] for r in rows if r['h3'] == h3 and r['lam'] == lam and r['hafif_hafta'] == n and r[k] >= thr]
    return max(v) if v else None
print('270 gün, 6 gün/hafta, yalnız YT. Sınır = varsayımların en az %50 (ve %90) kadarında o seviyede kalınan en yüksek saat')
for lam in (0.0, 0.02):
    print('\nyavaş birikim λ =', lam)
    print('tavan |  K0 %50/%90 | K1 %50/%90 | K2 (4 haftada hafif) %50/%90 | K3 %50/%90 | çöküşsüz en yüksek (%95) | en yüksek ort. sınav günü P')
    for h3 in (5, 6, 7, 8):
        best = max((r for r in rows if r['h3'] == h3 and r['lam'] == lam and r['hafif_hafta'] == 0), key=lambda r: r['P_ort'])['h']
        nc = max([r['h'] for r in rows if r['h3'] == h3 and r['lam'] == lam and r['hafif_hafta'] == 0 and r['cokus'] <= 0.05])
        print('  %d   |  %s / %s  |  %s / %s  |  %s / %s  |  %s / %s  |  %s  |  %s' % (h3,
              lim(h3, lam, 0, 'K0', .5), lim(h3, lam, 0, 'K0', .9), lim(h3, lam, 0, 'K1', .5), lim(h3, lam, 0, 'K1', .9),
              lim(h3, lam, 4, 'K2', .5), lim(h3, lam, 4, 'K2', .9), lim(h3, lam, 0, 'K3', .5), lim(h3, lam, 0, 'K3', .9), nc, best))
