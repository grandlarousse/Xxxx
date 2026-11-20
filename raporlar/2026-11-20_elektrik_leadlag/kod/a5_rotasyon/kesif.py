"""A5 ek tablolar ve tanılar (IS): otokorelasyon / çapraz otokorelasyon tablosu, aday kuralların tanıları.
Kullanım: python3 -I kesif.py <panel_is> <otokor.csv> [tanı]"""
import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
import elib  # noqa: E402
import rules  # noqa: E402

pd.set_option('display.width', 250); pd.set_option('display.max_rows', 500); pd.set_option('display.max_columns', 40)


def series(P):
    """Günlük seriler. Sepet getirileri t−1 günü dolabilir üyelerle kurulur (alınabilir sepetin t günü getirisi)."""
    sc = elib.sector_cols(P)
    R = P['ret_cc'][sc]
    fl = P['fill_long'][sc].shift(1, fill_value=False)
    lm = rules.liquid_mask(P).shift(1, fill_value=False)
    v3 = [c for c in rules.VIOP3 if c in sc]
    X = pd.DataFrame({'XELKT': P['idx_ret']['XELKT'], 'XU030': P['idx_ret']['XU030']}).reindex(R.index)
    s = R.where(fl); X['sepet'] = s.mean(axis=1).where(s.notna().sum(axis=1) >= 5)
    s = R.where(lm); X['likit10'] = s.mean(axis=1).where(s.notna().sum(axis=1) >= 5)
    s = R[v3].where(fl[v3]); X['viop3'] = s.mean(axis=1)
    return X


def otokor(P, out):
    X = series(P)
    pairs = [('XELKT', 'XELKT'), ('XU030', 'XU030'), ('XU030', 'XELKT'), ('XELKT', 'XU030'), ('XELKT', 'sepet'),
             ('XELKT', 'likit10'), ('XELKT', 'viop3'), ('XU030', 'sepet'), ('XU030', 'likit10'), ('XU030', 'viop3'),
             ('sepet', 'sepet'), ('likit10', 'likit10'), ('viop3', 'viop3')]
    pers = {'IS': (None, None), '<=2019': (None, '2019-12-31'), '2020-2022': ('2020-01-01', None)}
    for y in sorted(set(X.index.year)):
        pers[str(y)] = (f'{y}-01-01', f'{y}-12-31')
    rows = []
    for a, b in pairs:
        for k in (1, 2, 3):
            d = pd.concat([X[a].shift(k).rename('x'), X[b].rename('y')], axis=1).dropna()
            for pn, (s, e) in pers.items():
                dd = d.loc[s:e]
                if len(dd) < 60:
                    continue
                c = dd['x'].corr(dd['y'])
                rows.append({'donem': pn, 'onceki': a, 'sonraki': b, 'gecikme': k, 'korelasyon': round(c, 4),
                             'n': len(dd), 't_yaklasik': round(c * np.sqrt(len(dd) - 2) / np.sqrt(1 - c * c), 2)})
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    df.to_csv(out, index=False)
    m = df[df.donem.isin(['IS', '<=2019', '2020-2022'])]
    pv = m.pivot_table(index=['onceki', 'sonraki'], columns=['donem', 'gecikme'], values='korelasyon')
    print(pv.round(3).to_string())
    yl = df[(df.gecikme == 1) & ~df.donem.isin(['IS', '<=2019', '2020-2022']) &
            df.onceki.eq('XELKT') & df.sonraki.isin(['XELKT', 'likit10', 'viop3'])]
    print(yl.pivot(index='donem', columns='sonraki', values='korelasyon').round(3).T.to_string())
    for b in ['XELKT', 'sepet', 'likit10', 'viop3']:
        r = elib.ts_reg(X[b], pd.DataFrame({'XELKT_1': X['XELKT'].shift(1), 'XU030_1': X['XU030'].shift(1)}), lag=3)
        print('reg', b, '~ XELKT(t-1) + XU030(t-1):', r.round(3).to_dict('index'))
    return X


def tani(P):
    S = rules.signals(P)
    idx = P['ret_cc'].index
    r = P['idx_ret'][['XELKT', 'XU030']].reindex(idx)
    zE, zX = rules._z(r['XELKT']), rules._z(r['XU030'])
    cand = ['S3_zirve20', 'S4_mom_ge1', 'S2_gecikme_yukari_1', 'S1_RS1_ge2', 'S6_rel_1617_ge1p5', 'S6_rel_1417_ge1p5']
    D = pd.DataFrame({c: S[c] for c in cand}).astype(int)
    print('örtüşme (satır sinyali günlerinde sütun sinyalinin payı):')
    print((D.T.dot(D).div(D.sum(), axis=0)).round(2).to_string())
    # ortak regresyon: hedefin günlük own-fazla f_h'i ~ kuklalar
    for hedef in ['sepet', 'likit10', 'viop3']:
        allsig, mn = rules.target_sig(P, pd.Series(True, index=idx), hedef)
        cols = list(allsig.columns)
        for h in (1, 3):
            M, fl = elib.excess_measures(P, h, 'long', cols)
            y, _, _ = elib.day_series(allsig, M['own'], fl, mn)
            for nm, X in [('S1-S4', D[cand[:4]]), ('S6 dahil (2017+)', D.loc['2017-03-01':])]:
                rr = elib.ts_reg(1e4 * y, X, lag=h)
                print(hedef, 'h', h, nm, ' '.join(f'{k}={v.katsayi:.0f}({v.t:.1f})' for k, v in rr.iterrows()))
    # ızgara dışı (keşif) kontroller
    kes = {
        'K_XU030_ge1': zX >= 1, 'K_XU030_ge1_XELKT_ge0p5': (zX >= 1) & (zE >= 0.5),
        'K_zirve20_ve_mom_ge1': S['S3_zirve20'] & S['S4_mom_ge1'], 'K_zirve20_mom_yok': S['S3_zirve20'] & ~S['S4_mom_ge1'],
        'K_mom_ge1_zirve_yok': S['S4_mom_ge1'] & ~S['S3_zirve20'],
    }
    L = P['idx']['XELKT'].reindex(idx)
    for w in (10, 40, 60):
        kes[f'K_zirve{w}'] = L >= L.rolling(w, min_periods=w).max()
    rows = []
    for nm, s in kes.items():
        for hedef in ['sepet', 'viop3']:
            sig, mn = rules.target_sig(P, s.fillna(False), hedef)
            for h in (1, 3):
                rw = elib.evaluate(sig, P, h=h, measure='own', min_n=mn, name=f'{nm}|{hedef}|h{h}', family='kesif')
                rows.append({k: rw[k] for k in ['sinyal_tanimi', 'n_gun_IS', 'ort_fazla_IS_bps', 't_IS', 'net_temel_bps_IS',
                                                'top10_haric_bps', 'giris_kapanis1_bps']})
    print(pd.DataFrame(rows).round(1).to_string(index=False))
    # tek hisse kırılımı ve yıllar
    for sn, hs in [('S3_zirve20', (2, 3)), ('S2_gecikme_yukari_1', (3,)), ('S4_mom_ge1', (3,)), ('S6_rel_1617_ge1p5', (1, 3))]:
        for c in rules.VIOP3 + ['ZOREN', 'AKENR']:
            for h in hs:
                sig = pd.DataFrame({c: S[sn]})
                rw = elib.evaluate(sig, P, h=h, measure='own', name=f'{sn}|{c}|h{h}', family='kesif')
                print(f"{sn}|{c}|h{h}: n={rw['n_gun_IS']} ex={rw['ort_fazla_IS_bps']:.0f} t={rw['t_IS']:.1f} "
                      f"net={rw['net_temel_bps_IS']:.0f} x10={rw['top10_haric_bps']:.0f} | {rw['yillar_bps']}")
    # karar anı: sinyal 17:00 değeriyle (16:00 damgalı bar) hesaplansaydı kapanış sinyaliyle ne kadar örtüşürdü (2017+)
    H = rules.hourly(P)
    if H is not None:
        f = os.path.join(P['dir'], 'h1_isy', 'XELKT.parquet')
        d = pd.read_parquet(f); d['ts_tr'] = pd.to_datetime(d['ts_tr']); d['date'] = d['ts_tr'].dt.normalize()
        v17 = d[d['ts_tr'].dt.hour <= 16].groupby('date').c.last().reindex(idx)
        v18 = d[d['ts_tr'].dt.hour <= 17].groupby('date').c.last().reindex(idx)
        L = P['idx']['XELKT'].reindex(idx)
        sd = r['XELKT'].rolling(60, min_periods=40).std().shift(1)
        for lab, v in [('17:00', v17), ('~18:00 (sürekli işlem sonu)', v18)]:
            hi = v >= pd.concat([L.shift(1).rolling(19, min_periods=19).max(), v], axis=1).max(axis=1)
            mo = (v / L.shift(1) - 1) / sd >= 1
            for nm, a, b in [('zirve20', hi, S['S3_zirve20']), ('mom_ge1', mo, S['S4_mom_ge1'])]:
                m = v.notna()
                a, b = a[m], b[m]
                print(f'karar anı {lab} {nm}: kapanış sinyali {int(b.sum())} gün; erken sinyal {int(a.sum())}; '
                      f'kapanış sinyalinin erken görülen payı {(a & b).sum() / b.sum():.2f}; erken sinyalin yanlış payı {(a & ~b).sum() / a.sum():.2f}')
    # yer değiştirme (dairesel kaydırma) sıfır dağılımı
    for sn, hedef, h in [('S3_zirve20', 'viop3', 3), ('S3_zirve20', 'sepet', 3), ('S4_mom_ge1', 'sepet', 3),
                         ('S2_gecikme_yukari_1', 'viop3', 3), ('S6_rel_1617_ge1p5', 'sepet', 1),
                         ('S6_rel_1617_ge1p5', 'likit10', 3), ('S1_RS1_ge2', 'likit10', 3)]:
        sig, mn = rules.target_sig(P, S[sn], hedef)
        st = '2017-03-01' if sn.startswith('S6') else None
        real, pv, null = elib.shift_null(sig, P, h=h, n=300, start=st)
        print(f'kaydırma testi {sn}|{hedef}|h{h}: gerçek={real:.0f} bps, p={pv:.3f}, sıfır %95={np.nanpercentile(null, 95):.0f}')


if __name__ == '__main__':
    P = elib.load(sys.argv[1])
    otokor(P, sys.argv[2])
    if len(sys.argv) > 3:
        tani(P)
