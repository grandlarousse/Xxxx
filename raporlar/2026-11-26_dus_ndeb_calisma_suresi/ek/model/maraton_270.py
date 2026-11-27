import sys, numpy as np, csv
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim
H = 270
HA = [3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0]
HB = [0.0, 1.0, 2.0]
const = [(a, b, 6, 0, 0, 1.0) for a in HA for b in HB]
# sprint: taban a (hB=0), son S gun a+D
spr = [(a, 0.0, 6, 0, S, (a + D) / a) for a in (4.0, 4.5, 5.0, 5.5, 6.0) for S in (28, 42) for D in (1.0, 1.5)]
pols = const + spr
out = {}
for h3 in (5, 6, 7, 8):
    for lam in (0.0, 0.02):
        Es, Cs = [], []
        for seed in (101, 202):
            pr, _ = sim.sample_params(h3, seed, 1000); prd = sim.derive(pr, h3)
            r = sim.ref_sim(prd, pols, H, lam=lam)
            Es.append(r['sumE']); Cs.append(r['ever'])
        out[(h3, lam)] = (np.vstack(Es), np.vstack(Cs))
rows = []
for (h3, lam), (E, C) in out.items():
    for j, p in enumerate(pols):
        rows.append(dict(h3=h3, lam=lam, hA=p[0], hB=p[1], sprint_gun=p[4], sprint_saat=round(p[0] * p[5], 2) if p[4] else '',
                         cikti_ort=E[:, j].mean(), cokus=C[:, j].mean()))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cikti', 'maraton_270.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
nc = len(const)
def ozet(keys, baslik):
    E = np.vstack([out[k][0] for k in keys]); C = np.vstack([out[k][1] for k in keys])
    m = E[:, :nc].mean(axis=0); c = C[:, :nc].mean(axis=0)
    print('\n###', baslik)
    for b in HB:
        idx = [i for i, p in enumerate(const) if p[1] == b]
        best = max(idx, key=lambda i: m[i]); mb = m[best]
        print(' DT=%.0f |' % b, ' '.join('%.1f:%3.0f%%/%3.0f' % (const[i][0], 100 * m[i] / m.max(), 100 * c[i]) for i in idx))
    ib = int(np.argmax(m)); 
    tot = lambda i: const[i][0] + const[i][1]
    print(' optimum (ort. çıktı en yüksek): %.1f + %.0f = %.1f net; çöküş %.0f%%' % (const[ib][0], const[ib][1], tot(ib), 100 * c[ib]))
    ok95 = [i for i in range(nc) if m[i] >= 0.95 * m[ib] and c[i] <= 0.001]
    if ok95:
        i = min(ok95, key=lambda i: (tot(i), -m[i])); print(' dengeli (çıktının >=%%95, çöküş 0, en az saat): %.1f + %.0f = %.1f; çıktı %%%.0f' % (const[i][0], const[i][1], tot(i), 100 * m[i] / m[ib]))
    for thr, ad in ((0.05, 'üst sınır (çöküş <=%5)'), (0.50, 'agresif bandın sonu (çöküş <=%50)'), (0.95, 'maksimum (çöküş <%95)')):
        ok = [i for i in range(nc) if c[i] <= thr]
        iA = max([i for i in ok if const[i][1] == 0], key=lambda i: const[i][0])
        iT = max(ok, key=lambda i: (tot(i), m[i]))
        print(' %s: yalnız YT %.1f (çıktı %%%.0f); toplam net en çok %.1f + %.0f = %.1f (çıktı %%%.0f)' % (ad, const[iA][0], 100 * m[iA] / m[ib], const[iT][0], const[iT][1], tot(iT), 100 * m[iT] / m[ib]))
    return E, C, m, ib
for lam in (0.0, 0.02):
    for h3 in (5, 6, 7, 8):
        ozet([(h3, lam)], 'tavan %d, yavaş birikim %s' % (h3, lam))
    ozet([(h, lam) for h in (6, 7)], 'tavan 6-7 karışık, yavaş birikim %s' % lam)
    ozet([(h, lam) for h in (5, 6, 7, 8)], 'tavan 5-8 karışık (tavan bilinmiyor), yavaş birikim %s' % lam)
print('\n### SPRINT: sabit düzeye göre toplam çıktı değişimi % / çöküş % (taban, son S gün, sprint saati)')
for lam in (0.0, 0.02):
    for h3 in (6, 7):
        E, C = out[(h3, lam)]
        print(' tavan %d, λ=%s' % (h3, lam))
        for j in range(nc, len(pols)):
            a, _, _, _, S, psi = pols[j]
            jc = [i for i, p in enumerate(const) if p[0] == a and p[1] == 0][0]
            print('   taban %.1f, son %d gün %.1f: çıktı %+5.1f%%, çöküş %3.0f%% (sabit taban çöküş %3.0f%%)' % (a, S, a * psi, 100 * (E[:, j].mean() / E[:, jc].mean() - 1), 100 * C[:, j].mean(), 100 * C[:, jc].mean()))
