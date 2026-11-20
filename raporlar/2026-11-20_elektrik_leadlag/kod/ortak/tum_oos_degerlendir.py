"""tum_oos_degerlendir.py — 2. dalgada (yalnız IS ile) dondurulan BÜTÜN kuralların, IS sonrası dönemin tamamında
(2023-01-02 → veri sonu; OOS-1 + kasa birlikte) tek seferlik havuz sınaması (YONTEM_EK E12).

Kullanım:
    python3 -I tum_oos_degerlendir.py <panel_is> <panel_full> <cikti.csv> <ajan1> <ajan2> ...

- Seçim yok: verilen ajanların build() ile döndürdüğü kuralların tamamı girer.
- Zamanlama kuralları dönem-nötr kıyasla ('per'), kesit kuralları 'sec' ile değerlendirilir.
- Tek yönlü p (pozisyon yönünde; "RED" kuralında ters yön), Benjamini–Hochberg q = 0,10: (a) birinciller, (b) bütün kurallar.
"""
import importlib.util
import os
import sys
from math import erf, sqrt

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import elib  # noqa: E402

KOD = os.path.dirname(HERE)
elib.PERIOD_MODE = 'havuz'


def load_rules(agent, P):
    path = os.path.join(KOD, agent, 'rules.py')
    spec = importlib.util.spec_from_file_location(f'rules_{agent}_{id(P)}', path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(path))
    try:
        spec.loader.exec_module(mod)
        return {r['ad']: r for r in mod.build(P)}
    finally:
        sys.path.pop(0)


def main():
    panel_is, panel_full, out = sys.argv[1], sys.argv[2], sys.argv[3]
    agents = sys.argv[4:]
    P_is, P_full = elib.load(panel_is), elib.load(panel_full)
    rows = []
    for ag in agents:
        r_is, r_full = load_rules(ag, P_is), load_rules(ag, P_full)
        for ad, rule in r_full.items():
            a, b = r_is[ad]['sig'], rule['sig']
            idx = a.index[a.index <= elib.IS_END]
            cols = sorted(set(a.columns) | set(b.columns))
            x = a.reindex(index=idx, columns=cols).fillna(False).astype(bool)
            y = b.reindex(index=idx, columns=cols).fillna(False).astype(bool)
            d = (x != y)
            extra = [c for c in cols if c not in a.columns]
            if extra:
                d[extra] = d[extra] & P_full['tradable'].reindex(index=idx, columns=extra).fillna(False).astype(bool)
            res = elib.eval_rule(rule, P_full, family=ag, olcu_map={'own': 'per'})
            row = res[-1] if rule.get('arac') == 'viop' and len(res) > 1 else res[0]
            row['ajan'] = ag
            row['nedensellik_oran'] = float(d.values.sum() / max(int(x.values.sum()), 1))
            row['beklenen_isaret'] = -1 if ad.endswith('_RED') else int(rule.get('beklenen_isaret', 1))
            rows.append(row)
    df = pd.DataFrame(rows)
    phi = lambda v: 0.5 * (1 + erf(v / sqrt(2)))
    df['p_tek_beklenen_OOS'] = [1 - phi(t * s) if t == t else np.nan for t, s in zip(df['t_OOS'], df['beklenen_isaret'])]
    df['bh_birincil_OOS'] = False
    m = df['birincil'].astype(bool)
    df.loc[m, 'bh_birincil_OOS'] = elib.bh_fdr(df.loc[m, 'p_tek_beklenen_OOS'].values, 0.10)
    df['bh_tum_OOS'] = elib.bh_fdr(df['p_tek_beklenen_OOS'].values, 0.10)
    df['holm_tum_OOS'] = elib.holm(df['p_tek_beklenen_OOS'].values, 0.10)
    df.to_csv(out, index=False)
    c = ['sinyal_tanimi', 'arac', 'yon', 'h', 'karar_olcusu', 'birincil', 'n_bagimsiz_IS', 'ort_fazla_IS_bps', 't_IS',
         'n_bagimsiz_OOS', 'ort_fazla_OOS_bps', 't_OOS', 'p_tek_beklenen_OOS', 'net_temel_bps_OOS', 'bh_birincil_OOS',
         'bh_tum_OOS', 'holm_tum_OOS']
    pd.set_option('display.width', 320); pd.set_option('display.max_colwidth', 46); pd.set_option('display.max_rows', 100)
    print(df[[k for k in c if k in df.columns]].sort_values('p_tek_beklenen_OOS').round(
        {'ort_fazla_IS_bps': 0, 't_IS': 1, 'ort_fazla_OOS_bps': 0, 't_OOS': 2, 'p_tek_beklenen_OOS': 4, 'net_temel_bps_OOS': 0}).to_string(index=False))
    print('→', out)


if __name__ == '__main__':
    main()
