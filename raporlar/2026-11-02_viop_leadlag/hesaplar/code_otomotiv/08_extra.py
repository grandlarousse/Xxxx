"""(A) Tarama sürprizleri mekanizma testleri, (B) Asya lag0 -> gün-içi etkisi BIST geneli mi? (47 hisse),
(C) Ek backtestler: z-eşikli, çok günlük (açılış t -> kapanış t+4), XU100-hedge'li gün-içi, yıllara göre kırılım.
Çıktı: res/surprise.csv, res/asia_bistwide.csv, res/bt_extra.csv"""
from common import *
import importlib.util
xg = D('XU100')['gap']; xi = D('XU100')['intra']; spx1 = R('^GSPC').shift(1)
raw_zero = lambda s: float((ll.raw(s)['c'].diff() == 0).mean())

# ---- (A) sürprizler ----
S = []
def add(name, y, x, ctrls, note=''):
    c0, t0, n = corr_t(y, x)
    pc, pt, _ = pcorr(y, x, ctrls)
    sp, is0 = split_for(y, x)
    _, tI, _ = pcorr(y, x, ctrls, start=is0, end=sp); _, tO, _ = pcorr(y, x, ctrls, start=sp)
    df = pd.concat([y.rename('y'), x.rename('x')], axis=1).dropna()
    g = df.groupby(df.index.year).apply(lambda q: q['y'].corr(q['x']) if len(q) > 60 else np.nan).dropna()
    S.append({'test': name, 'n': n, 'r': c0, 't': t0, 'pc_ctrl': pc, 'pc_t': pt, 't_IS': tI, 't_OOS': tO,
              'yr_same_sign': float((np.sign(g) == np.sign(c0)).mean()) if len(g) else np.nan, 'note': note})
for s in ['CSG.AS', 'GWLLY', 'KRDMB.IS']:
    try: print(s, 'ilk tarih', ll.raw(s)['ldate'].min().date(), 'n', len(ll.raw(s)), 'sıfır değişim payı', round(raw_zero(s), 3))
    except Exception as e: print(s, e)
dT = D('TOASO'); dF = D('FROTO'); dD = D('DOAS'); dA = D('ARCLK')
add('CSG.AS sync TOASO | XU100', R('TOASO'), R('CSG.AS'), [M()], 'kısa örneklem')
add('GWLLY_{t-1} -> FROTO intra | XU100gap,gap,SPX1,EEM1', dF['intra'], R('GWLLY').shift(1), [xg, dF['gap'], spx1, R('EEM').shift(1)], 'OTC bayat')
add('GWLLY_{t-1} -> FROTO intra | +2333.HK_t (HK lag0 seansla çakışır)', dF['intra'], R('GWLLY').shift(1), [xg, dF['gap'], spx1], '')
add('XHB_{t-1} -> DOAS intra | XU100gap,gap', dD['intra'], R('XHB').shift(1), [xg, dD['gap']], '')
add('XHB_{t-1} -> DOAS intra | +SPX1,IWM1,EEM1', dD['intra'], R('XHB').shift(1), [xg, dD['gap'], spx1, R('IWM').shift(1), R('EEM').shift(1)], '')
add('XHB_{t-1} -> XU100 intra | XU100gap (piyasa geneli mi?)', xi, R('XHB').shift(1), [xg], '')
add('ITB_{t-1} -> DOAS intra | +SPX1,IWM1,EEM1', dD['intra'], R('ITB').shift(1), [xg, dD['gap'], spx1, R('IWM').shift(1), R('EEM').shift(1)], '')
add('KRDMB_{t-1} -> ARCLK intra | XU100gap,gap', dA['intra'], R('KRDMB.IS').shift(1), [xg, dA['gap']], '')
add('KRDMB_{t-1} -> ARCLK intra | +XU100_{t-1},ARCLK_{t-1},KRDMD_{t-1}', dA['intra'], R('KRDMB.IS').shift(1),
    [xg, dA['gap'], M().shift(1), R('ARCLK').shift(1), R('KRDMD').shift(1)], '')
add('ON_{t-1} -> FROTO intra | XU100gap,gap', dF['intra'], R('ON').shift(1), [xg, dF['gap']], '')
add('ON_{t-1} -> FROTO intra | +SPX1,SOX1', dF['intra'], R('ON').shift(1), [xg, dF['gap'], spx1, R('^SOX').shift(1)], '')
add('EREGL_{t-1} -> FROTO intra | XU100gap,gap', dF['intra'], R('EREGL').shift(1), [xg, dF['gap']], '')
add('EREGL_{t-1} -> FROTO intra | +XU100_{t-1},FROTO_{t-1}', dF['intra'], R('EREGL').shift(1), [xg, dF['gap'], M().shift(1), R('FROTO').shift(1)], '')
add('^TWII_t -> FROTO intra | XU100gap,gap,SPX1', dF['intra'], R('^TWII'), [xg, dF['gap'], spx1], '')
add('^TWII_t -> FROTO intra | +ES=F gece (ABD vadeli 06:30?) yok -> +EEM1,SOX1', dF['intra'], R('^TWII'), [xg, dF['gap'], spx1, R('EEM').shift(1), R('^SOX').shift(1)], '')
add('^KS11_t -> TOASO intra | +EEM1,SOX1,KRW?', dT['intra'], R('^KS11'), [xg, dT['gap'], spx1, R('EEM').shift(1), R('^SOX').shift(1)], '')
add('^KS11_t -> XU100 intra | XU100gap,SPX1 (BIST geneli)', xi, R('^KS11'), [xg, spx1], '')
SS = pd.DataFrame(S); SS.to_csv(os.path.join(RES, 'surprise.csv'), index=False)
print(SS.drop(columns='note').round(3).to_string(index=False))

# ---- (B) Asya etkisi BIST geneli mi? ----
from universe import VIOP
rows = []
for s in VIOP:
    try: d = D(s)
    except Exception: continue
    for a in ['^KS11', '^TWII', '^N225']:
        pc, pt, n = pcorr(d['intra'], R(a), [xg, d['gap'], spx1])
        rows.append({'stock': s, 'asia': a, 'pc': pc, 't': pt, 'n': n})
BW = pd.DataFrame(rows); BW.to_csv(os.path.join(RES, 'asia_bistwide.csv'), index=False)
pv = BW.pivot(index='stock', columns='asia', values='t')
print('47 hisse Asya lag0->intra pc t: medyan', pv.median().round(2).to_dict(), '| t>2 olan hisse sayısı', (pv > 2).sum().to_dict())
print('FROTO/TOASO sırası (KS11 t):', pv['^KS11'].rank(ascending=False)[['FROTO', 'TOASO', 'DOAS', 'ARCLK', 'VESTL', 'ASTOR']].to_dict())

# ---- (C) ek backtestler ----
def basket(syms, L): return pd.concat([R(s).shift(L) for s in syms], axis=1).mean(axis=1, skipna=False)
def fwd_hold(st, k=4):  # açılış t -> kapanış t+k
    d = D(st); a = R(st); return d['intra'] + sum(a.shift(-j) for j in range(1, k + 1))
grid = basket(['267260.KS', '298040.KS', '010120.KS'], 0)
gridg = pd.concat([R(s).shift(1) for s in ['SU.PA', 'ABBN.SW', 'ETN', 'SIE.DE']], axis=1).mean(axis=1, skipna=False)
T = [
 ('F_{t-1} -> FROTO intra |z|>1', R('F').shift(1), D('FROTO')['intra'], 'z', 1.0, None),
 ('F_{t-1} -> FROTO intra |z|>2', R('F').shift(1), D('FROTO')['intra'], 'z', 2.0, None),
 ('EXV5_{t-1} -> TOASO intra |z|>1', R('EXV5.DE').shift(1), D('TOASO')['intra'], 'z', 1.0, None),
 ('EXV5_{t-1} -> TOASO-XU100 intra (hedge) sign', R('EXV5.DE').shift(1), D('TOASO')['intra'] - xi, 'sign', 0.0, None),
 ('STLAM_{t-1} -> TOASO-XU100 intra (hedge) sign', R('STLAM.MI').shift(1), D('TOASO')['intra'] - xi, 'sign', 0.0, None),
 ('F_{t-1} -> FROTO-XU100 intra (hedge) sign', R('F').shift(1), D('FROTO')['intra'] - xi, 'sign', 0.0, None),
 ('WHR_{t-1} -> ARCLK intra |z|>1', R('WHR').shift(1), D('ARCLK')['intra'], 'z', 1.0, None),
 ('Kore şebeke_t -> ASTOR intra |z|>1', grid, D('ASTOR')['intra'], 'z', 1.0, 'mid'),
 ('Kore şebeke_t -> ASTOR-XU100 intra (hedge) sign', grid, D('ASTOR')['intra'] - xi, 'sign', 0.0, 'mid'),
 ('Avrupa/ABD şebeke_{t-1} -> ASTOR intra sign', gridg, D('ASTOR')['intra'], 'sign', 0.0, 'mid'),
 ('Avrupa/ABD şebeke_{t-1} -> ASTOR intra, sadece 2025+', gridg[gridg.index >= '2025-01-01'], D('ASTOR')['intra'], 'sign', 0.0, '2026-01-01'),
 ('^TWII_t -> FROTO intra |z|>1', R('^TWII'), D('FROTO')['intra'], 'z', 1.0, None),
 ('^KS11_t -> TOASO-XU100 intra (hedge) sign', R('^KS11'), D('TOASO')['intra'] - xi, 'sign', 0.0, None),
 ('ÇOK GÜNLÜK F_{t-1} |z|>2 -> FROTO açılış t..kapanış t+4', R('F').shift(1), fwd_hold('FROTO'), 'z', 2.0, None),
 ('ÇOK GÜNLÜK EXV5_{t-1} |z|>2 -> TOASO açılış t..kapanış t+4', R('EXV5.DE').shift(1), fwd_hold('TOASO'), 'z', 2.0, None),
 ('ÇOK GÜNLÜK Kore şebeke_t |z|>2 -> ASTOR açılış t..kapanış t+4', grid, fwd_hold('ASTOR'), 'z', 2.0, 'mid'),
 ('ÇOK GÜNLÜK EURTRY_{t-1} |z|>2 -> FROTO açılış t..kapanış t+4', R('EURTRY=X').shift(1), fwd_hold('FROTO'), 'z', 2.0, None),
]
rows = []
for name, sig, tgt, mode, thr, sp in T:
    if sp == 'mid': sp = str(split_for(tgt, sig)[0].date())
    sp = sp or SPLIT
    res = bt(sig, tgt, costs=(0, 8, 15), mode=mode, thr=thr, split=sp, start='2014-01-01')
    for c in (0, 8, 15):
        r = bt_row(name, res, c); r['split'] = sp; rows.append(r)
BX = pd.DataFrame(rows); BX.to_csv(os.path.join(RES, 'bt_extra.csv'), index=False)
print(BX[BX.cost_bps == 8][['test', 'IS_n', 'IS_mean_bps', 'IS_t', 'OOS_n', 'OOS_mean_bps', 'OOS_t', 'OOS_sharpe', 'split']].round(2).to_string(index=False))
print('brüt (0 bps) OOS ort.:', BX[BX.cost_bps == 0].set_index('test')['OOS_mean_bps'].round(1).to_dict())
