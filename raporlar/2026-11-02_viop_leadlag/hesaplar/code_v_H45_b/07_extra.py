"""07: ek çürütme testleri — seçim yanlılığı (SAHOL NAV), ihracatçı ortak faktörü, 2014-2019 alt dönemi, yıllık korelasyonlar."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_H45_b')
from blib import *
import importlib.util
def _imp(n, f):
    s = importlib.util.spec_from_file_location(n, OUT + '/' + f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
r01 = _imp('r01', '01_repro.py')

def bg(w):
    G = pd.concat({k: bist(k)['gap'] for k in w}, axis=1); wv = pd.Series(w)
    num = (G.fillna(0) * wv).sum(1); den = (G.notna() * wv).sum(1)
    return (num / den).where(den >= 0.7 * wv.sum())

print('=== seçim yanlılığı: aynı kurgu diğer holdinglerde ===')
import os
SW = {k: v for k, v in {'AKBNK': .45, 'ENJSA': .10, 'CIMSA': .03, 'BRISA': .03, 'KORDS': .03, 'AKGRT': .03}.items()
      if os.path.exists(f'{DATA}/daily/{k}.IS.parquet')}
print('SAHOL sepet:', SW)
S = bist('SAHOL'); snav = bg(SW)
print('SAHOL NAVgap - own gap -> intra:', ct3(S['intra'], snav - S['gap']))
r = reg(S['intra'], {'nav': snav, 'gap': S['gap']}, T0); print('   SAHOL intra ~ nav + gap:', {k: f"{r['b'][k]:+.3f}({r['t'][k]:+.1f})" for k in r['b']})
# KCHOL'un yalnız tek iştirakle versiyonları (hangi iştirak sürüklüyor?)
K = bist('KCHOL')
for s in ['TUPRS', 'YKBNK', 'FROTO', 'ARCLK', 'TOASO']:
    g = bist(s)['gap']
    r = reg(K['intra'], {'sub': g, 'kgap': K['gap']}, T0)
    print(f'  KCHOL intra ~ {s}gap + Kgap: sub {r["b"]["sub"]:+.3f}({r["t"]["sub"]:+.1f})')
# tüm iştirakler birlikte
Xd = {s: bist(s)['gap'] for s in ['TUPRS', 'YKBNK', 'FROTO', 'ARCLK', 'TOASO']}; Xd['kgap'] = K['gap']
r = reg(K['intra'], Xd, T0); print('  çoklu:', {k: f"{r['b'][k]:+.3f}({r['t'][k]:+.1f})" for k in Xd})

print('\n=== (b)/(c) ihracatçı/USD-gelirli ortak faktör ===')
E = bist('ENKAI'); tur, _, _ = us_lag('TUR'); usd, _ = fx_lag('TRY=X')
EXP = ['THYAO', 'SISE', 'FROTO', 'TKFEN', 'EREGL', 'ALARK', 'PGSUS', 'ARCLK', 'TOASO', 'ASELS']
XI = pd.concat({s: bist(s)['intra'] for s in EXP}, axis=1).mean(1)
NONEXP = ['AKBNK', 'GARAN', 'ISCTR', 'HALKB', 'VAKBN', 'YKBNK', 'BIMAS', 'MGROS', 'SOKM', 'TCELL', 'TTKOM', 'EKGYO', 'ULKER', 'AEFES']
NI = pd.concat({s: bist(s)['intra'] for s in NONEXP}, axis=1).mean(1)
print('TUR -> ihracatçı sepeti intra :', ct3(XI, tur))
print('TUR -> iç talep/banka sepeti  :', ct3(NI, tur))
print('TUR -> ihracatçı - iç talep   :', ct3(XI - NI, tur))
print('USD -> ihracatçı - iç talep   :', ct3(XI - NI, usd))
for nm, x in [('TUR', tur), ('USD', usd)]:
    r = reg(E['intra'], {nm: x, 'xi': XI}, T0); r2 = reg(E['intra'], {nm: x, 'xi': XI, 'ni': NI}, T0)
    print(f'  Eintra ~ {nm} + ihracatçı intra (eşzamanlı): {nm} {r["b"][nm]:+.3f}({r["t"][nm]:+.1f}); + iç talep: {nm} {r2["b"][nm]:+.3f}({r2["t"][nm]:+.1f})')
    for lab, a, b in [('IS', T0, SPLIT), ('OOS', SPLIT, None)]:
        r2 = reg(E['intra'], {nm: x, 'xi': XI, 'ni': NI}, a, b)
        print(f'     {lab}: {nm} {r2["b"][nm]:+.3f}({r2["t"][nm]:+.1f})')

print('\n=== alt dönemler ===')
for nm, x in [('TUR', tur), ('USD', usd)]:
    for a, b in [('2014', '2020'), ('2014', '2021'), ('2020', '2024'), ('2023-06-01', '2099'), ('2024', '2099')]:
        c = ct(E['intra'], x, a, b)
        print(f'  {nm} -> Eintra {a}..{b}: corr {c[0]:+.3f} t {c[1]:+.2f} n {c[2]}')
    print('  yıllık:', yearly(E['intra'], x).round(3).to_dict())
W = r01.W; nav = r01.basket_gap(W); sig = nav - K['gap']
for a, b in [('2014', '2020'), ('2020', '2024'), ('2023-06-01', '2099'), ('2024', '2099')]:
    c = ct(K['intra'], sig, a, b); print(f'  (a) {a}..{b}: corr {c[0]:+.3f} t {c[1]:+.2f} n {c[2]}')
