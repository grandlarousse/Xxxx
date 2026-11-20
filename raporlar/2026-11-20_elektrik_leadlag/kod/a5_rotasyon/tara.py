"""A5 IS taraması: önceden yazılı ızgara × hedef × h. Kullanım: python3 -I tara.py <panel_is> <çıktı.csv>"""
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

SPLIT = pd.Timestamp('2019-12-31')


def halves(sig, P, h, side, min_n):
    """IS'in iki yarısında karar ölçüsü (own, dolabilir) günlük ortalaması. ≤2019 / 2020+; ≤2019'da sinyal günlerinin
    %15'inden azı varsa sinyal günleri kronolojik ikiye bölünür."""
    cols = [c for c in sig.columns if c in P['ret_cc'].columns]
    M, fl = elib.excess_measures(P, h, side, cols)
    p, _, _ = elib.day_series(sig[cols], M['own'], fl, min_n)
    p = p[p.index <= elib.IS_END].dropna()
    if len(p) < 6:
        return {'yari1_bps': np.nan, 'yari2_bps': np.nan, 'yari1_n': 0, 'yari2_n': 0, 'yari_tanimi': ''}
    a, b = p[p.index <= SPLIT], p[p.index > SPLIT]
    tan = '<=2019|2020+'
    if len(a) < 0.15 * len(p) or len(b) < 0.15 * len(p):
        k = len(p) // 2
        a, b = p.iloc[:k], p.iloc[k:]
        tan = f'kronolojik yari (kesim {p.index[k].date()})'
    return {'yari1_bps': 1e4 * a.mean(), 'yari2_bps': 1e4 * b.mean(), 'yari1_n': len(a), 'yari2_n': len(b),
            'yari_tanimi': tan}


def main(panel, out):
    P = elib.load(panel)
    S = rules.signals(P)
    rows = []
    for sn, s in S.items():
        fam = sn.split('_')[0]
        for hedef in ['sepet', 'likit10', 'viop3']:
            sig, min_n = rules.target_sig(P, s, hedef)
            for h in (1, 2, 3):
                ex = {'sinyal': sn, 'hedef_adi': hedef, 'n_sinyal_gun': int(s.sum())}
                ex.update(halves(sig, P, h, 'long', min_n))
                rows.append(elib.evaluate(sig, P, h=h, side='long', measure='own', instrument='spot', min_n=min_n,
                                          name=f'{sn}|{hedef}|long|h{h}', family='A5_' + fam, extra=ex))
                if hedef == 'viop3':
                    ex = {'sinyal': sn, 'hedef_adi': 'viop3', 'n_sinyal_gun': int(s.sum())}
                    ex.update(halves(sig, P, h, 'short', 1))
                    rows.append(elib.evaluate(sig, P, h=h, side='short', measure='own', instrument='viop', min_n=1,
                                              name=f'{sn}|viop3|short|h{h}', family='A5_' + fam, extra=ex))
    df = pd.DataFrame(rows)
    df = mark(df)
    df = elib.to_csv(df.to_dict('records'), out)
    print('test sayısı:', len(df), '| sinyal:', len(S), '|', df['secim'].value_counts().to_dict())
    check(P, df)
    return df


MANUEL = [  # (sinyal_tanimi ön eki, not) — otomatik ölçütleri geçip dondurulmayanlar
    ('S1_RS1_ge2', 'S4_mom_ge1 ile %76 örtüşür; ortak regresyonda ek katkısı yok; sepette en iyi 10 gün hariç ≈ 0'),
    ('S1_RS10', 'beklenen (dönüş) yönünün tersi; yalnız VİOP üçlüsünde, sepet/likit doğrulamıyor (t ≤ 1,5)'),
    ('S1_RS3', 'yalnız VİOP üçlüsünde ve tek h; sepet/likit doğrulamıyor'),
    ('S2_gecikme_yukari_1|', 'dondurulan A5_gecikme1_viop3_h3 komşusu; sepet/likitte gecikme koşulu ek bilgi taşımıyor'),
    ('S3_zirve20_yalniz', 'S3_zirve20 alt kümesi: daha az olay, ek bilgi yok'),
    ('S3_zirve20|', 'dondurulan h3 kuralının komşusu (h2 net 13 bps < 15)'),
    ('S4_mom_ge1', 'dondurulan S4_mom_ge1 h3 kurallarının komşusu (eşik 1,5 / h2 / VİOP üçlüsünde 2020+ zayıf)'),
    ('S6_rel_1617_ge1p5', 'dondurulan S6_rel_1617_ge1p5 kurallarının komşusu (kural sayısı sınırı)'),
    ('S6_', 'tek noktada: komşu pencere/eşik aynı gücü vermiyor; S6 ailesinde 576 test, aile düzeyinde anlamlı değil'),
]


def mark(df):
    """'secim' (birincil / ikincil / elendi), 'not', 'bh_gecti', 'aday_mi' sütunları."""
    fro = {f'{sn}|{hed}|{yon}|h{h}': (ad, b) for ad, sn, hed, h, yon, arac, b, _ in rules.FROZEN}
    df['bh_gecti'] = elib.bh_fdr(elib.t_to_p(df['t_IS'].values), 0.10)
    sec, notes = [], []
    for _, r in df.iterrows():
        k = r['sinyal_tanimi']
        fails = []
        if not r['t_IS'] >= 2: fails.append('t<2')
        if not r['net_temel_bps_IS'] > 0: fails.append('temel maliyet sonrası ≤0')
        if not (r['yari1_bps'] > 0 and r['yari2_bps'] > 0): fails.append('iki yarıda aynı (pozitif) işaret yok')
        if not r['top10_haric_bps'] > 0: fails.append('en iyi 10 gün hariç ≤0')
        if not r['giris_kapanis1_bps'] > 0: fails.append('t+1 kapanış girişinde kayboluyor')
        if not r['n_bagimsiz_IS'] >= 40: fails.append('bağımsız olay <40')
        if r['en_yogun_pay'] > (0.6 if r['hedef_adi'] == 'viop3' else 0.25): fails.append('tek hisseye yoğun')
        if k in fro:
            sec.append('birincil' if fro[k][1] else 'ikincil')
            notes.append(f'DONDURULDU: {fro[k][0]}' + (' | zayıflık: ' + '; '.join(fails) if fails else ''))
        else:
            sec.append('elendi')
            if fails:
                notes.append('; '.join(fails))
            else:
                notes.append(next((n for p, n in MANUEL if k.startswith(p)), 'otomatik ölçütleri geçiyor; komşusu donduruldu'))
    df['secim'] = sec; df['not'] = notes; df['aday_mi'] = df['secim'] != 'elendi'
    return df


def check(P, df):
    """Dondurulmuş kurallar: build(P) → eval_rule tarama satırıyla aynı mı; nedensellik öz-denetimi."""
    import time
    t0 = time.time()
    R = rules.build(P)
    print(f'build(): {len(R)} kural, {time.time() - t0:.1f} sn; birincil = {sum(r["birincil"] for r in R)}')
    d = df.set_index('sinyal_tanimi')
    for (ad, sn, hed, h, yon, arac, b, _), r in zip(rules.FROZEN, R):
        row = elib.eval_rule(r, P, family='A5')[0]
        ref = d.loc[f'{sn}|{hed}|{yon}|h{h}']
        assert abs(row['ort_fazla_IS_bps'] - ref['ort_fazla_IS_bps']) < 1e-6 and row['n_gun_IS'] == ref['n_gun_IS'], ad
        print(f"  {ad}: n_gun={row['n_gun_IS']} bağımsız={row['n_bagimsiz_IS']} fazla={row['ort_fazla_IS_bps']:.1f} bps "
              f"t={row['t_IS']:.2f} net_temel={row['net_temel_bps_IS']:.1f} (tarama satırıyla aynı)")
    sc = elib.self_check_causal(rules.build, P)
    print('self_check_causal:', sc)
    assert all(v == 0 for v in sc.values())
    a = rules.build(P); b = rules.build(P)
    print('deterministik:', all(x['sig'].equals(y['sig']) for x, y in zip(a, b)))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
