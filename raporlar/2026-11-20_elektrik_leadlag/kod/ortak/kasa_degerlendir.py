"""kasa_degerlendir.py — kasa (holdout, 2025-07-01 →) için tek seferlik sınama (YONTEM_EK E7 ve E11).

Kullanım:
    python3 -I kasa_degerlendir.py <panel_dev> <panel_full> <cikti.csv> <ajan>:<kural_adi> [<ajan>:<kural_adi> ...]

- En çok 10 kural. Her kural panel_full ile kurulur; nedensellik için panel_dev ile kurulan sinyalle 2025-06-30'a kadar
  karşılaştırılır.
- Beklenen işaret: kural sözlüğündeki "beklenen_isaret" (+1 varsayılan; −1 = kaçınma kuralı, AL pozisyonu kaybettirir).
- Tek yönlü p (beklenen yönde), Holm düzeltmesi (alfa = 0,10).
- Sınıflama (kasaya bakılmadan önce yazıldı):
    doğrulandı   : işaret beklenen yönde ve Holm'den geçiyor
    çürütüldü    : işaret ters ve |t| ≥ 1; ya da işaret doğru ama kasa etkisi geliştirme etkisinin %25'inden küçük ve
                   geliştirme etkisi kasanın %90 güven aralığının dışında
    güç yetersiz : diğer bütün durumlar (kâğıt üstünde izleme)
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


def phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def main():
    panel_dev, panel_full, out = sys.argv[1], sys.argv[2], sys.argv[3]
    items = [a.split(':', 1) for a in sys.argv[4:]]
    assert len(items) <= 10, 'kasaya en çok 10 kural girer'
    P_dev, P_full = elib.load(panel_dev), elib.load(panel_full)
    cache = {}
    rows = []
    for ag, ad in items:
        if ag not in cache:
            cache[ag] = (load_rules(ag, P_dev), load_rules(ag, P_full))
        r_dev, r_full = cache[ag]
        rule = r_full[ad]
        # nedensellik: 2025-06-30'a kadar iki panelden aynı sinyal
        a, b = r_dev[ad]['sig'], rule['sig']
        idx = a.index[a.index <= elib.OOS1_END]
        cols = sorted(set(a.columns) | set(b.columns))
        x = a.reindex(index=idx, columns=cols).fillna(False).astype(bool)
        y = b.reindex(index=idx, columns=cols).fillna(False).astype(bool)
        d = (x != y)
        extra = [c for c in cols if c not in a.columns]
        if extra:
            d[extra] = d[extra] & P_full['tradable'].reindex(index=idx, columns=extra).fillna(False).astype(bool)
        ned = float(d.values.sum() / max(int(x.values.sum()), 1))
        res = elib.eval_rule(rule, P_full, family=ag, olcu_map={'own': 'per'})   # YONTEM_EK E12: dönem-nötr kıyas
        row = res[-1] if rule.get('arac') == 'viop' and len(res) > 1 else res[0]   # viop: vadeli fiyatlı satır
        row['ajan'] = ag
        row['beklenen_isaret'] = int(rule.get('beklenen_isaret', 1))
        row['nedensellik_oran'] = ned
        # geliştirme dönemi (IS+OOS1) birleşik etkisi: gün sayısıyla ağırlıklı
        n1, n2 = row.get('n_gun_IS', 0) or 0, row.get('n_gun_OOS1', 0) or 0
        e1, e2 = row.get('ort_fazla_IS_bps', np.nan), row.get('ort_fazla_OOS1_bps', np.nan)
        row['gelistirme_bps'] = np.nansum([n1 * e1, n2 * e2]) / max(n1 + n2, 1)
        rows.append(row)
    df = pd.DataFrame(rows)
    s = df['beklenen_isaret'].astype(float)
    t = df['t_KASA'].astype(float)
    df['p_tek_beklenen_KASA'] = [1 - phi(ti * si) if ti == ti else np.nan for ti, si in zip(t, s)]
    df['holm_KASA'] = elib.holm(df['p_tek_beklenen_KASA'].values, 0.10)
    eff = df['ort_fazla_KASA_bps'].astype(float)
    se = (eff / t).abs()
    dev = df['gelistirme_bps'].astype(float)
    sinif = []
    for i in range(len(df)):
        si, ei, ti, sei, di = s[i], eff[i], t[i], se[i], dev[i]
        if not (ei == ei and ti == ti):
            sinif.append('veri yok'); continue
        dogru_yon = (ei * si) > 0
        if dogru_yon and df['holm_KASA'][i]:
            sinif.append('doğrulandı')
        elif (not dogru_yon) and abs(ti) >= 1:
            sinif.append('çürütüldü')
        elif dogru_yon and abs(ei) < 0.25 * abs(di) and abs(di - ei) > 1.645 * sei:
            sinif.append('çürütüldü')
        else:
            sinif.append('güç yetersiz')
    df['kasa_sinifi'] = sinif
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    df.to_csv(out, index=False)
    c = ['ajan', 'sinyal_tanimi', 'arac', 'yon', 'h', 'karar_olcusu', 'beklenen_isaret', 'ort_fazla_IS_bps', 't_IS',
         'ort_fazla_OOS1_bps', 't_OOS1', 'n_gun_KASA', 'n_bagimsiz_KASA', 'ort_fazla_KASA_bps', 't_KASA',
         'p_tek_beklenen_KASA', 'holm_KASA', 'kasa_sinifi', 'nedensellik_oran']
    pd.set_option('display.width', 300); pd.set_option('display.max_colwidth', 48)
    print(df[[k for k in c if k in df.columns]].round(2).to_string(index=False))
    print('→', out)


if __name__ == '__main__':
    main()
