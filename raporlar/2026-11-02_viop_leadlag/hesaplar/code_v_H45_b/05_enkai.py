"""05: (b) ENKAI–TUR_{t-1} ve (c) ENKAI–USDTRY_{t-1} -> ENKAI gün-içi: çürütme testleri."""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_H45_b')
from blib import *
import importlib.util
def _imp(n, f):
    s = importlib.util.spec_from_file_location(n, OUT + '/' + f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
f02 = _imp('f02', '02_futaudit.py')

E = bist('ENKAI'); X100 = bist('XU100')
tur, tui, tun = us_lag('TUR')
usd, usd0 = fx_lag('TRY=X')
NONKOC = ['AKBNK', 'GARAN', 'ISCTR', 'HALKB', 'VAKBN', 'SAHOL', 'THYAO', 'PGSUS', 'BIMAS', 'EREGL', 'KRDMD', 'SISE', 'ASELS', 'TCELL', 'TTKOM',
          'PETKM', 'SASA', 'EKGYO', 'KCHOL', 'TAVHL', 'TKFEN', 'ULKER', 'MGROS', 'AEFES', 'DOHOL', 'VESTL', 'ALARK', 'CIMSA', 'DOAS', 'GUBRF',
          'TUPRS', 'FROTO', 'YKBNK', 'ARCLK', 'TOASO']
MG = pd.concat({s: bist(s)['gap'] for s in NONKOC}, axis=1); MI = pd.concat({s: bist(s)['intra'] for s in NONKOC}, axis=1)
mkg = MG.mean(1).where(MG.notna().sum(1) >= 15); mki = MI.mean(1).where(MI.notna().sum(1) >= 15)
cv = E['intra'].rolling(250, min_periods=100).cov(mki).shift(1); vv = mki.rolling(250, min_periods=100).var().shift(1)
eh = E['intra'] - (cv / vv) * mki  # piyasa-hedge'li ENKAI gün-içi (hisse-bazlı piyasa, kayan beta)

def P(name, y, x):
    print(f'{name:60s} {ct3(y, x)}')
def R(name, y, Xd, periods=(('ALL', T0, None), ('IS', T0, SPLIT), ('OOS', SPLIT, None))):
    for lab, a, b in periods:
        r = reg(y, Xd, a, b)
        if r is None: continue
        print(f'  {name:44s} {lab:3s} n {r["n"]} ' + ' '.join(f'{k} {r["b"][k]:+.3f}({r["t"][k]:+.1f})' for k in Xd))

print('=== 1. temel ===')
P('(b) TUR_{t-1} -> Eintra', E['intra'], tur)
P('(c) USD_{t-1} -> Eintra', E['intra'], usd)
P('(b) TUR -> piyasa-hedge\'li Eintra (hisse-bazlı)', eh, tur)
P('(c) USD -> piyasa-hedge\'li Eintra', eh, usd)
P('(b) TUR -> mkintra (35 hisse ort.)', mki, tur)
P('(c) USD -> mkintra', mki, usd)

print('\n=== 2. TUR ayrıştırması: ABD seansı (o->c, BIST kapanışı sonrası ağırlıklı) vs gece (c_prev->o, BIST seansını içerir) ===')
P('TUR US-seans_{t-1} -> Eintra', E['intra'], tui)
P('TUR gece_{t-1} -> Eintra', E['intra'], tun)
R('Eintra ~ TURus + TURnight', E['intra'], {'us': tui, 'night': tun})
R('Eintra ~ TURus + TURnight + X100cc1 + Ecc1', E['intra'], {'us': tui, 'night': tun, 'x100cc1': X100['cc'].shift(1), 'ecc1': E['cc'].shift(1)})
P('X100 cc_{t-1} -> Eintra', E['intra'], X100['cc'].shift(1))

print('\n=== 3. gap-fade kontrolleri ===')
R('Eintra ~ TUR + Egap', E['intra'], {'tur': tur, 'egap': E['gap']})
R('Eintra ~ TUR + Egap + Egap^2 + |Egap|>1% + mkgap', E['intra'], {'tur': tur, 'egap': E['gap'], 'egap2': E['gap'] ** 2,
   'big': (E['gap'].abs() > 0.01).astype(float).where(E['gap'].notna()), 'mkg': mkg})
R('Eintra ~ USD + Egap + Egap^2 + |Egap|>1% + mkgap', E['intra'], {'usd': usd, 'egap': E['gap'], 'egap2': E['gap'] ** 2,
   'big': (E['gap'].abs() > 0.01).astype(float).where(E['gap'].notna()), 'mkg': mkg})
small = E['gap'].abs() < 0.005
P('(b) yalnız |Egap|<%0,5 günleri', E['intra'].where(small), tur)
P('(c) yalnız |Egap|<%0,5 günleri', E['intra'].where(small), usd)
P('(b) ENKAI müzayede gap\'i (Egap) -> Eintra (kendi gap-fade)', E['intra'], -E['gap'])
P('(b) Egap kalıntısı (TUR\'dan bağımsız) -> Eintra', E['intra'], -(E['gap'] - 0.0))
R('Eintra ~ TUR + USD + Egap + mkgap + X100cc1 + Ecc1', E['intra'], {'tur': tur, 'usd': usd, 'egap': E['gap'], 'mkg': mkg,
   'x100cc1': X100['cc'].shift(1), 'ecc1': E['cc'].shift(1)})

print('\n=== 4. FX momentumu kanalı (USD_t eşzamanlı, işlenemez; yalnız ayrıştırma) ===')
P('USD_{t-1} -> USD_t (FX otokorelasyonu)', usd0, usd)
P('USD_t -> Eintra (eşzamanlı)', E['intra'], usd0)
R('Eintra ~ USD_{t-1} + USD_t', E['intra'], {'usd1': usd, 'usd0': usd0})
R('Eintra ~ TUR_{t-1} + USD_t', E['intra'], {'tur': tur, 'usd0': usd0})
P('TUR_{t-1} -> USD_t', usd0, tur)

print('\n=== 5. plasebolar ===')
for s in ['EWZ', 'EZA', 'EWW', 'EEM', 'TKC']:
    x, _, _ = us_lag(s)
    P(f'{s}_(t-1) -> Eintra', E['intra'], x)
    if s != 'TKC':
        R(f'Eintra ~ TUR + {s}', E['intra'], {'tur': tur, s: x}, periods=(('ALL', T0, None),))
P('TUR_{t-2} -> Eintra (zaman plasebosu)', E['intra'], tur.shift(1))
P('TUR_{t} (BIST kapanışı SONRASI, gelecek) -> Eintra', E['intra'], tur.shift(-1))
for s in ['ZAR=X', 'BRL=X', 'MXN=X', 'EURTRY=X']:
    x, _ = fx_lag(s)
    P(f'{s}_(t-1) -> Eintra', E['intra'], x)
# diğer 'USD varlıklı / ihracatçı' VİOP hisseleri: aynı kanal genel mi?
print('\n47 hisse taraması (TUR_{t-1} ve USD_{t-1} -> hisse intra; t):')
V47 = ['AEFES','AKBNK','AKSEN','ALARK','ARCLK','ASELS','ASTOR','BIMAS','BRSAN','CIMSA','DOAS','DOHOL','EKGYO','ENJSA','ENKAI','EREGL','FROTO','GARAN','GUBRF','HALKB','HEKTS','ISCTR','KCHOL','KRDMD','MGROS','ODAS','OYAKC','PETKM','PGSUS','SAHOL','SASA','SISE','SOKM','TAVHL','TCELL','THYAO','TKFEN','TOASO','TRALT','TRMET','TSKB','TTKOM','TUPRS','ULKER','VAKBN','VESTL','YKBNK']
rows = []
for s in V47:
    try:
        B = bist(s)
    except Exception:
        continue
    a = ct(B['intra'], tur, T0); b = ct(B['intra'], usd, T0); ao = ct(B['intra'], tur, SPLIT); bo = ct(B['intra'], usd, SPLIT)
    rows.append((s, a[1], ao[1], b[1], bo[1], a[2]))
sc = pd.DataFrame(rows, columns=['sym', 't_tur', 't_tur_oos', 't_usd', 't_usd_oos', 'n']).sort_values('t_tur')
print(sc.round(2).to_string(index=False))
sc.to_csv(OUT + '/res_scan47.csv', index=False)

print('\n=== 6. alt dönem / uç değer ===')
for nm, x in [('TUR', tur), ('USD', usd)]:
    df = pd.concat([E['intra'].rename('y'), x.rename('x')], axis=1).dropna(); df = df[df.index >= T0]
    print(f'-- {nm}: Spearman {df.y.corr(df.x, "spearman"):+.3f}')
    for a in range(2014, 2027, 2):
        d2 = df[(df.index.year >= a) & (df.index.year < a + 2)]
        print(f'   {a}-{a+1}: corr {d2.y.corr(d2.x):+.3f} t {ct(d2.y, d2.x)[1]:+.2f} n {len(d2)}')
    for q in (0.99, 0.95):
        thr = df.x.abs().quantile(q); d2 = df[df.x.abs() <= thr]
        print(f'   |x|<=q{int(q*100)}: corr {d2.y.corr(d2.x):+.3f} t {ct(d2.y, d2.x)[1]:+.2f}')
    d2 = df[~df.index.year.isin([2021, 2022])]
    print(f'   2021-22 hariç: corr {d2.y.corr(d2.x):+.3f} t {ct(d2.y, d2.x)[1]:+.2f}; OOS(2023+) {ct(d2[d2.index>=SPLIT].y, d2[d2.index>=SPLIT].x)[1]:+.2f}')
    jk = {y: round(ct(df[df.index.year != y].y, df[df.index.year != y].x)[1], 2) for y in sorted(df.index.year.unique())}
    print('   jackknife t:', jk)
