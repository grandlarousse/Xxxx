"""V4 çürütme (S3, T1/T2, K1/K2) — ortak yardımcılar. Kasa AÇIK: panel_full kullanılır. Yalnız betimleme/çürütme; kural dondurmaz."""
import os
import sys
import importlib.util
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KOD = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(KOD, 'ortak'))
import elib  # noqa: E402

PER = {'IS': (None, pd.Timestamp('2022-12-30')), 'OOS1': (pd.Timestamp('2023-01-02'), pd.Timestamp('2025-06-30')),
       'KASA': (pd.Timestamp('2025-07-01'), None), 'HAVUZ': (pd.Timestamp('2023-01-02'), None)}
ROWS = []


def pm(idx, per):
    a, b = PER[per]
    m = np.ones(len(idx), dtype=bool)
    if a is not None:
        m &= idx >= a
    if b is not None:
        m &= idx <= b
    return m


def tt(x):
    """Basit ortalama (bps), t, n."""
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 3:
        return (1e4 * x.mean() if n else np.nan, np.nan, n)
    return 1e4 * x.mean(), x.mean() / (x.std(ddof=1) / np.sqrt(n)), n


def hac(p, h):
    """p: takvim serisi (sinyal olmayan gün NaN). elib ile aynı HAC (Bartlett, gecikme h−1)."""
    d = p.notna().values.astype(float)
    x = p.fillna(0).values
    mu, t = elib._hac_mean(x, d, max(h - 1, 0))
    return (1e4 * mu if mu == mu else np.nan), t, int(d.sum())


def indep_pos(p, h):
    """Aralarında ≥ h işlem günü olan olaylar (açgözlü); dönen: seçilen tarihler."""
    pos = np.where(p.notna().values)[0]
    out, last = [], -10 ** 9
    for i in pos:
        if i - last >= h:
            out.append(i)
            last = i
    return p.index[out]


def load_rules(agent):
    spec = importlib.util.spec_from_file_location('r_' + agent, os.path.join(KOD, agent, 'rules.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def add(bulgu, test, donem, n, ort, t, notu=''):
    ROWS.append({'bulgu': bulgu, 'test': test, 'donem': donem, 'n': n,
                 'ort_bps': None if ort is None or ort != ort else round(float(ort), 1),
                 't': None if t is None or t != t else round(float(t), 2), 'not': notu})
    print(f'{bulgu:5s} | {test:58s} | {donem:10s} | n={n!s:>6} | {ort if ort is None or ort != ort else round(float(ort), 1)!s:>8} | '
          f't={t if t is None or t != t else round(float(t), 2)!s:>6} | {notu}')


def save(name):
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    pd.DataFrame(ROWS).to_csv(os.path.join(HERE, 'out', name), index=False)
