"""V1: S1, S2, S3 zamanlama kurallarının ham veriden bağımsız yeniden üretimi.
Kullanım: python3 -I 01_main.py <raw_d1> <cikti_klasoru>
Sürümler:  A = görev tanımı (çıkış ilk kilitsiz kapanış, sınırsız kayma)  -> ANA
           B = ortak kütüphane taklidi (kayma en çok 5 gün; dönemde < 60 dolabilir günü olan hisse dışarıda) -> fark teşhisi
           C = A, çöküş serisi hisseleri (BIGEN, LYDYE, MAGEN) hedef ve kıyas dışı -> duyarlılık"""
import sys, os
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v1lib as L

raw, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
P = L.panel(raw)
cal = P['cal']
print('takvim', len(cal), cal[0].date(), cal[-1].date())
print('dolabilir hisse-gün', int(P['fill'].values.sum()), 'tavan kilidi', int((P['tavan'] & P['tradable']).values.sum()),
      'taban kilidi', int((P['taban'] & P['tradable']).values.sum()))
H = 3
S = L.sinyaller(P)
pos_all = np.arange(len(cal))
COKUS = ['BIGEN', 'LYDYE', 'MAGEN']


def degerlendir(F, surum, min_days=0, haric=(), boot=False):
    rng = np.random.default_rng(20261120)
    rows, gun = [], []
    for ad, (sig, cols, min_n) in S.items():
        cols = [c for c in cols if c not in haric]
        f = F[cols]; fl = P['fill'][cols] & f.notna()
        for dn, (a, b) in L.DONEM.items():
            m = (cal >= a) & (cal <= b)
            flm = fl[m]
            fm = f[m].where(flm)
            bench = fm.mean().where(flm.sum() >= max(min_days, 1))   # hissenin dönem içi dolabilir günlerinin ortalaması
            ex = fm - bench
            n = ex.notna().sum(axis=1)
            d = pd.DataFrame({'ham': fm.where(ex.notna()).mean(axis=1), 'per': ex.mean(axis=1), 'n': n,
                              'sig': sig[m] & (n >= min_n), 'pos': pos_all[m]})
            ev = d[d.sig]
            tr = ex[d.sig.values].stack().dropna()
            r = {'surum': surum, 'kural': ad, 'donem': dn, 'n_gun': len(ev), 'n_bagimsiz': L.bagimsiz(ev.pos.values, H),
                 'n_islem': int(ev.n.sum()), 'fazla_bps': ev.per.mean() * 1e4,
                 't_nw2': L.nw_t(ev.per.values, ev.pos.values, 2), 'ham_bps': ev.ham.mean() * 1e4,
                 'isabet_islem_per': float((tr > 0).mean()), 'isabet_gun_per': float((ev.per > 0).mean()),
                 'isabet_gun_ham': float((ev.ham > 0).mean())}
            d2 = d[d.n >= min_n]
            r['her_gun_per_bps'] = d2.per.mean() * 1e4; r['her_gun_ham_bps'] = d2.ham.mean() * 1e4
            r['sinyal_disi_gun_ham_bps'] = d2.ham[~d2.sig].mean() * 1e4
            if boot:
                # (a) blok önyükleme: blok 5 gün, 2000 tekrar; dairesel bloklar, olay günleri ortalaması (oran kestiricisi)
                x = np.where(d2.sig, d2.per, 0.0); s = d2.sig.values.astype(float); T = len(d2); B = 5
                nb = int(np.ceil(T / B))
                st = rng.integers(0, T, size=(2000, nb))
                ix = ((st[:, :, None] + np.arange(B)[None, None, :]) % T).reshape(2000, -1)[:, :T]
                num = x[ix].sum(axis=1); den = s[ix].sum(axis=1)
                bs = np.where(den > 0, num / np.maximum(den, 1), np.nan)
                r['bs_se_bps'] = np.nanstd(bs) * 1e4
                r['t_blok'] = r['fazla_bps'] / r['bs_se_bps']
                r['bs_ga90_alt'] = np.nanpercentile(bs, 5) * 1e4; r['bs_ga90_ust'] = np.nanpercentile(bs, 95) * 1e4
                r['bs_pay_negatif'] = float(np.nanmean(bs <= 0))
                # (b) rastgele dairesel kaydırma: >= 30 gün, 1000 tekrar (+ olası bütün kaydırmalar)
                ks = rng.integers(30, T - 30 + 1, size=1000)
                pv, sv = d2.per.values, d2.sig.values
                null = np.array([pv[np.roll(sv, k)].mean() for k in ks])
                tum = np.array([pv[np.roll(sv, k)].mean() for k in range(30, T - 30 + 1)])
                obs = ev.per.mean()
                r['kaydirma_p'] = float((1 + (null >= obs).sum()) / 1001)
                r['kaydirma_p_tum'] = float((1 + (tum >= obs).sum()) / (1 + len(tum)))
                r['kaydirma_n_tum'] = len(tum)
                r['sifir_ort_bps'] = null.mean() * 1e4; r['sifir_std_bps'] = null.std() * 1e4
                r['sifir_q95_bps'] = np.percentile(null, 95) * 1e4
            rows.append(r)
            if dn != 'HAVUZ':
                g = d[d.sig][['ham', 'per', 'n']].copy(); g.insert(0, 'donem', dn); g.insert(0, 'kural', ad); g.insert(0, 'surum', surum)
                gun.append(g)
    return pd.DataFrame(rows), pd.concat(gun)


FA = L.ileri(P, H); FB = L.ileri(P, H, max_delay=5)
RA, GA = degerlendir(FA, 'A', boot=True)
RB, GB = degerlendir(FB, 'B', min_days=60)
RC, GC = degerlendir(FA, 'C', haric=COKUS)
R = pd.concat([RA, RB, RC], ignore_index=True)
R.to_csv(os.path.join(outdir, 'v1_sonuc.csv'), index=False)
pd.concat([GA, GB]).rename_axis('date').to_csv(os.path.join(outdir, 'v1_gunluk.csv'))
for k in ['fill', 'tavan', 'taban', 'tradable', 'cadj']:
    P[k].to_pickle(os.path.join(outdir, f'v1_{k}.pkl'))
FA.to_pickle(os.path.join(outdir, 'v1_f3A.pkl')); FB.to_pickle(os.path.join(outdir, 'v1_f3B.pkl'))
pd.set_option('display.width', 280); pd.set_option('display.max_columns', 40)
print(R.round(2).to_string())
