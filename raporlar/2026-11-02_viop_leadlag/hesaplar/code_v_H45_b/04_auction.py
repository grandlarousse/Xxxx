"""04: (a) mekanizma testi — KCHOL spot müzayede fiyatı, KENDİ vadelisinin (06:30'dan beri sürekli işlem gören) ima ettiği fiyattan sapıyor mu?
dev_t = ln(o_t) - [ln(Fo_t) - basis_{t-1}],  basis_{t-1} = ln(Fs_{t-1}/c_{t-1}) (önceki günün vadeli-spot farkı; açılıştan önce bilinir).
Fo_t = günün ilk vadeli işlemi (2024-11-19 sonrası kesin 06:30+ UTC; öncesinde akşam seansı olasılığı -> ayrı rapor).
Ayrıca: piyasa kontrolü olarak Koç-dışı 30 likit hissenin kendi müzayede gap'lerinden (endeks açılışı bayat olabilir) piyasa gap'i.
"""
import sys; sys.path.insert(0, '/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_H45_b')
from blib import *
import importlib.util
def _imp(n, f):
    s = importlib.util.spec_from_file_location(n, OUT + '/' + f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
r01 = _imp('r01', '01_repro.py'); f02 = _imp('f02', '02_futaudit.py')
W, basket_gap = r01.W, r01.basket_gap

K = bist('KCHOL'); nav = basket_gap(W); sig = nav - K['gap']
X30 = bist('XU030')
# Koç-dışı piyasa (VİOP hisseleri, eşit ağırlık)
NONKOC = ['AKBNK', 'GARAN', 'ISCTR', 'HALKB', 'VAKBN', 'SAHOL', 'THYAO', 'PGSUS', 'BIMAS', 'EREGL', 'KRDMD', 'SISE', 'ASELS', 'TCELL', 'TTKOM',
          'PETKM', 'SASA', 'EKGYO', 'ENKAI', 'TAVHL', 'TKFEN', 'ULKER', 'MGROS', 'AEFES', 'DOHOL', 'VESTL', 'ALARK', 'CIMSA', 'DOAS', 'GUBRF']
MG = pd.concat({s: bist(s)['gap'] for s in NONKOC}, axis=1); MI = pd.concat({s: bist(s)['intra'] for s in NONKOC}, axis=1)
mkg = MG.mean(1).where(MG.notna().sum(1) >= 15); mki = MI.mean(1).where(MI.notna().sum(1) >= 15)

print('=== endeks açılışı bayat mı? ===')
r = reg(X30['intra'], {'x30gap': X30['gap'], 'mkgap': mkg}, T0)
print('X30intra ~ X30gap + (hisse-bazlı) mkgap:', {k: f"{r['b'][k]:+.3f}({r['t'][k]:+.1f})" for k in r['b']})
r = reg(mki, {'mkgap': mkg}, T0)
print('mkintra ~ mkgap (hisse ort.):', {k: f"{r['b'][k]:+.3f}({r['t'][k]:+.1f})" for k in r['b']})
r = reg(X30['intra'], {'nav': nav, 'x30gap': X30['gap']}, T0)
print('X30intra ~ NAVgap + X30gap:', {k: f"{r['b'][k]:+.3f}({r['t'][k]:+.1f})" for k in r['b']})

print('\n=== (a) hisse-bazlı piyasa kontrolüyle ===')
for nm, Xd in {'nav+kgap+mkgap': {'nav': nav, 'kgap': K['gap'], 'mkg': mkg},
               '+mkintra (eşzamanlı ayrıştırma)': {'nav': nav, 'kgap': K['gap'], 'mkg': mkg, 'mki': mki}}.items():
    for lab, a, b in [('ALL', T0, None), ('IS', T0, SPLIT), ('OOS', SPLIT, None)]:
        r = reg(K['intra'], Xd, a, b)
        print(f'  {nm:32s} {lab:3s} n {r["n"]} ' + ' '.join(f'{k} {r["b"][k]:+.3f}({r["t"][k]:+.1f})' for k in Xd))

print('\n=== vadeli-ima sapması ===')
F = f02.front('KCHOL')
j = F.join(K[['o', 'c', 'gap', 'intra']], how='inner').join(sig.rename('sig')).join(nav.rename('nav'))
j['basis1'] = np.log(j.Fs / j.c).shift(1)
# önceki gün aynı kontrat değilse (roll) basis atlaması olur -> kontrat değişim günlerini at
j['roll'] = j['code'] != j['code'].shift(1)
j['dev'] = np.log(j.o) - (np.log(j.Fo) - j.basis1)
j['futgap_spot_eq'] = np.log(j.Fo / j.Fps)  # vadeli 'gap' (06:30 ilk işlem / önceki uzlaşma)
j = j[~j['roll']]
for per, a, b in [('2020-01..2024-11-18', '2020-01-01', '2024-11-19'), ('2024-11-19+', '2024-11-19', '2099'), ('2021+', '2021-01-01', '2099')]:
    jj = j[(j.index >= a) & (j.index < b)].dropna(subset=['sig', 'dev', 'intra'])
    jj = jj[jj.dev.abs() < 0.05]
    print(f'\n-- {per} n {len(jj)}; medyan |dev| {1e4*jj.dev.abs().median():.0f} bps; sd(dev) {1e4*jj.dev.std():.0f}; sd(sig) {1e4*jj.sig.std():.0f}')
    print('   corr(dev, sig) %+.3f | corr(dev, -Kgap) %+.3f | corr(dev, NAVgap) %+.3f' % (jj.dev.corr(jj.sig), jj.dev.corr(-jj.gap), jj.dev.corr(jj.nav)))
    c1 = ct(jj.intra, jj.sig); c2 = ct(jj.intra, -jj.dev)
    print(f'   Kintra ~ sig: {c1[0]:+.3f} (t {c1[1]:+.2f}) | Kintra ~ -dev: {c2[0]:+.3f} (t {c2[1]:+.2f})')
    r = reg(jj.intra, {'sig': jj.sig, 'negdev': -jj.dev})
    print('   Kintra ~ sig + (-dev):', {k: f"{r['b'][k]:+.3f}({r['t'][k]:+.1f})" for k in r['b']})
    r = reg(jj.intra, {'nav': jj.nav, 'kgap': jj.gap, 'negdev': -jj.dev})
    print('   Kintra ~ NAVgap + Kgap + (-dev):', {k: f"{r['b'][k]:+.3f}({r['t'][k]:+.1f})" for k in r['b']})
    # vadeli hedef: ilk vadeli işlemden (06:30) kapanışa
    fo_c = np.log(jj.Fc / jj.Fo)
    r = reg(fo_c, {'sig': jj.sig})
    print('   vadeli Fo->Fc ~ sig:', {k: f"{r['b'][k]:+.3f}({r['t'][k]:+.1f})" for k in r['b']})
    # sinyalin 'müzayede öncesi bilinebilir' versiyonu: vadeli-ima KCHOL gap'i yerine
    # sigF = NAVgap - (Fo/Fps) : NAV müzayededen, KCHOL vadeliden (vadeli 06:30-06:55 fiyatı)
    sigF = jj.nav - jj.futgap_spot_eq
    c3 = ct(jj.intra, sigF); c4 = ct(np.log(jj.Fc / jj.Fvw), sigF)
    print(f'   sigF=NAVgap-Fgap -> Kintra {c3[0]:+.3f}(t {c3[1]:+.2f}); -> vadeli VWAP->kapanış {c4[0]:+.3f}(t {c4[1]:+.2f})')
