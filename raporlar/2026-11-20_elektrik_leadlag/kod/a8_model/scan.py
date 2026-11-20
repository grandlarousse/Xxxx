"""A8 tarama: önceden yazılı ızgara (aşağıda), yalnız IS paneli. Çıktı: out/scan_rows.pkl, out/ic_yillik.csv, out/onem.csv.

ÖNCEDEN YAZILI IZGARA (hesaptan önce):
  Kesit hedefi ('sec' fazla f_h, h = 1, 2, 3), tüm özellikler:
    ridge  lam ∈ {0.01, 0.1, 1, 10} (ceza = lam·n, standartlaştırılmış X)          → 12 yapılandırma
    lasso  alpha ∈ {0.005, 0.01, 0.02, 0.04} (standartlaştırılmış X ve y)          → 12
    lgbm   (derinlik, min_yaprak) ∈ {(2,200), (2,500), (3,200), (3,500)}, h = 1; IC'si en yüksek olan h = 2, 3'te → 6
  Kıyas (tek özellik / grup): ridge lam=1 {yalnız rel1, dönüş grubu, dönüş dışı} × h; lgbm(en iyi) {dönüş, dönüş dışı} h=1;
    modelsiz en düşük rel1 beşte birliği × h                                          → 14
  Her yapılandırma: en üst beşte birlik AL (aday) + en alt beşte birlik (bilgi).
  Sahte etki (aile başına IC'si en yüksek h=1 yapılandırması + h∈{2,3} en iyi t): fiyat ≥ 5 TL, en likit 15, üçte birlik.
  Zamanlama hedefi (dolabilir sektör sepeti 'own' fazla f_h): ridge lam ∈ {1, 10}, lasso alpha=0.05, lgbm(d2, m60) × h × eşik {0, 25 bps};
    kıyas: yalnız sec1 ridge lam=1 × h, eşik 0.
  Tek hisse (AKSEN/ENJSA/ODAS): kesit + zamanlama tahmini toplamı, eşik {25, 50 bps}, AL/SAT, h=1 (viop) + spot AL.
"""
import os
import sys
import time
import pickle
import warnings
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
import elib  # noqa: E402
import rules as RU  # noqa: E402

warnings.filterwarnings('ignore')
PANEL = sys.argv[1]
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)
P = elib.load(PANEL)
assert P['ret_cc'].index.max() <= elib.IS_END, 'kör protokol: yalnız IS paneli'
T0 = time.time()
fe = RU.features(P)
sc = fe['sc']
cache = {}
H1, H2 = pd.Timestamp('2019-12-31'), pd.Timestamp('2020-01-01')
print('panel', P['ret_cc'].index.min().date(), P['ret_cc'].index.max().date(), 'hisse', len(sc), 'satır', fe['X'].shape,
      'ay', int((fe['starts'] >= RU.MINWIN).sum()), flush=True)

YSEC, FILL = {}, {}
for h in (1, 2, 3):
    Mx, fl = elib.excess_measures(P, h, 'long', sc)
    YSEC[h] = Mx['sec'].where(fl)
    FILL[h] = fl
YDAY = {h: (lambda O: O.mean(axis=1).where(O.notna().sum(axis=1) >= 3))(elib.excess_measures(P, h, 'long', sc)[0]['own'].where(FILL[h]))
        for h in (1, 2, 3)}


def daily_ic(pred, y, min_n=5):
    m = pred.notna() & y.notna()
    a = pred.where(m).rank(axis=1)
    b = y.where(m).rank(axis=1)
    a = a.sub(a.mean(axis=1), axis=0)
    b = b.sub(b.mean(axis=1), axis=0)
    den = np.sqrt((a * a).sum(axis=1) * (b * b).sum(axis=1))
    ic = ((a * b).sum(axis=1) / den).where((m.sum(axis=1) >= min_n) & (den > 0))
    return ic.dropna()


def ic_extra(pred, h):
    ic = daily_ic(pred, YSEC[h])
    mu, t = elib._hac_mean(ic.values, np.ones(len(ic)), h - 1)
    return {'ic_ort': mu, 'ic_t': t, 'ic_yari1': ic[ic.index <= H1].mean(), 'ic_yari2': ic[ic.index >= H2].mean(),
            'ic_gun': len(ic)}, ic


def halves(sig, h, measure, side='long'):
    Mx, fl = elib.excess_measures(P, h, side, list(sig.columns))
    p, _, _ = elib.day_series(sig, Mx[measure], fl)
    a, b = p[p.index <= H1].dropna(), p[p.index >= H2].dropna()
    return {'yari1_bps': 1e4 * a.mean() if len(a) else np.nan, 'yari2_bps': 1e4 * b.mean() if len(b) else np.nan,
            'yari1_gun': len(a), 'yari2_gun': len(b)}


def night_sec(sig):
    """f_1'in gece payı 'sec' ölçüsüyle: seçilenlerin r_co(t+1)'i − aynı gün diğer dolabilir üyelerin ortalaması."""
    g = P['ret_co'][sc].shift(-1)
    G = g.where(fe['fill'])
    S, N = G.sum(axis=1).values[:, None], G.notna().sum(axis=1).values[:, None]
    oth = (S - G.fillna(0).values) / np.maximum(N - G.notna().values, 1)
    ex = (g - oth).where(sig & fe['fill'] & (N - G.notna().values >= 4))
    d = ex.mean(axis=1).dropna()
    return 1e4 * d.mean() if len(d) else np.nan


rows, ICY, IMP = [], {}, {}


def run_sec(sp, grup, collect_name=None):
    col = [] if collect_name else None
    pred = RU.predict_sec(P, fe, sp['h'], sp['cfg'], cache, col)
    if collect_name and col:
        IMP[collect_name] = np.array(col)
    sig = RU.rule_sig(P, fe, sp, cache)
    name = RU.spec_name(sp)
    ex, ic = ic_extra(pred, sp['h'])
    ex.update(halves(sig, sp['h'], 'sec'))
    ex.update({'grup': grup, 'model': RU.cfg_tag(sp['cfg']), 'dilim': ('alt' if sp.get('bottom') else 'ust'),
               'filtre': sp.get('filt') or '', 'gece_sec_bps': night_sec(sig) if sp['h'] == 1 else np.nan})
    row = elib.evaluate(sig, P, h=sp['h'], side='long', measure='sec', name=name, family='A8', extra=ex)
    rows.append(row)
    if not sp.get('bottom') and not sp.get('filt') and sp.get('frac', 0.2) == 0.2:
        ICY[name] = ic.groupby(ic.index.year).mean()
    return row


def pr(r):
    print(f"{r['sinyal_tanimi'][:52]:52s} n={r.get('n_gun_IS', 0):5d} fz={r.get('ort_fazla_IS_bps', np.nan):7.1f} t={r.get('t_IS', np.nan):6.2f} "
          f"net={r.get('net_temel_bps_IS', np.nan):7.1f} y1={r.get('yari1_bps', np.nan):6.1f} y2={r.get('yari2_bps', np.nan):6.1f} "
          f"top10={r.get('top10_haric_bps', np.nan):6.1f} kap1={r.get('giris_kapanis1_bps', np.nan):6.1f} own={r.get('dol_own_IS_bps', np.nan):6.1f} "
          f"pay={r.get('en_yogun_pay', np.nan):.2f} ic={r.get('ic_ort', np.nan):.4f}/{r.get('ic_t', np.nan):.2f} "
          f"[{r.get('ic_yari1', np.nan):.3f},{r.get('ic_yari2', np.nan):.3f}] gece={r.get('gece_sec_bps', np.nan):.1f}", flush=True)


def both(cfg, h, grup, collect_name=None):
    r = run_sec({'kind': 'sec', 'cfg': cfg, 'h': h, 'frac': 0.2}, grup, collect_name)
    pr(r)
    run_sec({'kind': 'sec', 'cfg': cfg, 'h': h, 'frac': 0.2, 'bottom': True}, grup)
    return r


# ------------------------------------------------------------------ 1) kesit ızgarası
best = {}
print('--- ridge', flush=True)
for lam in (0.01, 0.1, 1, 10):
    for h in (1, 2, 3):
        r = both({'model': 'ridge', 'lam': lam}, h, 'izgara', f'ridge_l{lam:g}_h{h}')
        best.setdefault(('ridge', h), []).append((r['ic_ort'], {'model': 'ridge', 'lam': lam}, r))
print('--- lasso  (%.0f sn)' % (time.time() - T0), flush=True)
for al in (0.005, 0.01, 0.02, 0.04):
    for h in (1, 2, 3):
        r = both({'model': 'lasso', 'alpha': al}, h, 'izgara', f'lasso_a{al:g}_h{h}')
        best.setdefault(('lasso', h), []).append((r['ic_ort'], {'model': 'lasso', 'alpha': al}, r))
print('--- lgbm  (%.0f sn)' % (time.time() - T0), flush=True)
for d, m in ((2, 200), (2, 500), (3, 200), (3, 500)):
    r = both({'model': 'lgbm', 'depth': d, 'leaf': m}, 1, 'izgara', f'lgbm_d{d}_m{m}_h1')
    best.setdefault(('lgbm', 1), []).append((r['ic_ort'], {'model': 'lgbm', 'depth': d, 'leaf': m}, r))
lg_best = max(best[('lgbm', 1)], key=lambda x: x[0])[1]
for h in (2, 3):
    r = both(lg_best, h, 'izgara', f"lgbm_d{lg_best['depth']}_m{lg_best['leaf']}_h{h}")
    best.setdefault(('lgbm', h), []).append((r['ic_ort'], lg_best, r))
print('--- kıyas  (%.0f sn)' % (time.time() - T0), flush=True)
for fs in ('rel1', 'donus', 'donusdisi'):
    for h in (1, 2, 3):
        both({'model': 'ridge', 'lam': 1, 'fset': fs}, h, 'kiyas')
for fs in ('donus', 'donusdisi'):
    both(dict(lg_best, fset=fs), 1, 'kiyas')
for h in (1, 2, 3):
    both({'model': 'naive'}, h, 'kiyas')

# ------------------------------------------------------------------ 2) sahte etki (finalistler)
print('--- sahte etki  (%.0f sn)' % (time.time() - T0), flush=True)
finalists = []
for fam in ('ridge', 'lasso', 'lgbm'):
    finalists.append((max(best[(fam, 1)], key=lambda x: x[0])[1], 1))
cand = [(x[2]['t_IS'], x[1], h) for (fam, h), lst in best.items() if h > 1 for x in lst]
tb = max(cand, key=lambda x: x[0])
finalists.append((tb[1], tb[2]))
NULLS = {}
for cfg, h in finalists:
    for extra in ({'filt': 'fiyat5'}, {'filt': 'lik15'}, {'frac': 1 / 3}):
        sp = dict({'kind': 'sec', 'cfg': cfg, 'h': h, 'frac': 0.2}, **extra)
        pr(run_sec(sp, 'sahte_etki'))
    sp = {'kind': 'sec', 'cfg': cfg, 'h': h, 'frac': 0.2}
    real, pv, _ = elib.shift_null(RU.rule_sig(P, fe, sp, cache), P, h=h, measure='sec', n=200, seed=1)
    NULLS[RU.spec_name(sp)] = pv
    print('  kaydırma sıfırı', RU.spec_name(sp), f'{real:.1f} bps p={pv:.3f}', flush=True)

# ------------------------------------------------------------------ 3) zamanlama
print('--- zamanlama  (%.0f sn)' % (time.time() - T0), flush=True)


def run_day(cfg, h, thr, grup):
    pd_ = RU.predict_day(P, fe, h, cfg, cache)
    sp = {'kind': 'day', 'cfg': cfg, 'h': h, 'thr': thr}
    sig = RU.rule_sig(P, fe, sp, cache)
    y = YDAY[h]
    ok = pd_.notna() & y.notna()
    rho = pd_[ok].rank().corr(y[ok].rank())
    tr = elib.ts_reg(y[ok], pd_[ok].to_frame('pred'), lag=h - 1)
    ex = {'grup': grup, 'model': RU.cfg_tag(cfg), 'ic_ort': rho, 'ic_t': float(tr.loc['pred', 't']) if tr is not None else np.nan,
          'ic_gun': int(ok.sum()), 'sinyal_gun_orani': float((pd_[ok] > thr).mean())}
    ex.update(halves(sig, h, 'own'))
    row = elib.evaluate(sig, P, h=h, side='long', measure='own', name=RU.spec_name(sp), family='A8', extra=ex)
    rows.append(row)
    pr(row)
    return row


DAYCFG = [{'model': 'ridge', 'lam': 1}, {'model': 'ridge', 'lam': 10}, {'model': 'lasso', 'alpha': 0.05},
          {'model': 'lgbm', 'depth': 2, 'leaf': 60, 'n': 60}]
dbest = []
for cfg in DAYCFG:
    for h in (1, 2, 3):
        for thr in (0.0, 0.0025):
            r = run_day(cfg, h, thr, 'zamanlama')
            if h == 1 and thr == 0.0:
                dbest.append((r['ic_ort'], cfg))
for h in (1, 2, 3):
    run_day({'model': 'ridge', 'lam': 1, 'fset': 'sec1'}, h, 0.0, 'zamanlama_kiyas')

# ------------------------------------------------------------------ 4) tek hisse (AKSEN/ENJSA/ODAS)
print('--- tek hisse  (%.0f sn)' % (time.time() - T0), flush=True)
cfg_s = finalists[0][0]
cfg_d = max(dbest, key=lambda x: x[0])[1]
for thr in (0.0025, 0.005):
    for side in ('long', 'short'):
        sp = {'kind': 'viop', 'cfg': cfg_s, 'cfg_day': cfg_d, 'h': 1, 'thr': thr, 'side': side}
        sig = RU.rule_sig(P, fe, sp, cache)
        row = elib.evaluate(sig, P, h=1, side=side, measure='own', instrument='viop', name=RU.spec_name(sp), family='A8',
                            extra=dict(halves(sig, 1, 'own', side), grup='tek_hisse', model=RU.cfg_tag(cfg_s) + '+' + RU.cfg_tag(cfg_d)))
        rows.append(row)
        pr(row)
    sp = {'kind': 'viop', 'cfg': cfg_s, 'cfg_day': cfg_d, 'h': 1, 'thr': thr, 'side': 'long', 'arac': 'spot'}
    sig = RU.rule_sig(P, fe, sp, cache)
    row = elib.evaluate(sig, P, h=1, side='long', measure='own', instrument='spot', name=RU.spec_name(sp), family='A8',
                        extra=dict(halves(sig, 1, 'own'), grup='tek_hisse', model=RU.cfg_tag(cfg_s) + '+' + RU.cfg_tag(cfg_d)))
    rows.append(row)
    pr(row)

# ------------------------------------------------------------------ 5) özellik önemleri, yıllık IC, kayıt
imp_rows = []
for nm, A in IMP.items():
    if A.shape[1] != len(fe['names']):
        continue
    if nm.startswith('lgbm'):
        sh = A / np.maximum(A.sum(axis=1, keepdims=True), 1e-30)
        for j, f in enumerate(fe['names']):
            imp_rows.append({'model': nm, 'ozellik': f, 'ort': sh[:, j].mean(), 'isaret_pay': np.nan, 'tur': 'kazanc_payi'})
    else:
        for j, f in enumerate(fe['names']):
            imp_rows.append({'model': nm, 'ozellik': f, 'ort': A[:, j].mean() * 1e4, 'isaret_pay': float((A[:, j] > 0).mean()),
                             'tur': 'std_katsayi_bps'})
imp = pd.DataFrame(imp_rows)
imp.to_csv(os.path.join(OUT, 'onem.csv'), index=False)
pd.DataFrame(ICY).T.to_csv(os.path.join(OUT, 'ic_yillik.csv'))
pickle.dump({'rows': rows, 'nulls': NULLS, 'finalists': finalists, 'cfg_day': cfg_d, 'lg_best': lg_best},
            open(os.path.join(OUT, 'scan_rows.pkl'), 'wb'))
print('\nTOPLAM satır (test):', len(rows), ' süre %.0f sn' % (time.time() - T0))
print('finalistler:', finalists, '| zamanlama en iyi:', cfg_d)
for nm in [f"ridge_l{finalists[0][0].get('lam', 0):g}_h1", f"lasso_a{finalists[1][0].get('alpha', 0):g}_h1",
           f"lgbm_d{lg_best['depth']}_m{lg_best['leaf']}_h1"]:
    s = imp[imp.model == nm].set_index('ozellik')
    if len(s):
        print('\nönem', nm)
        print(' '.join(f"{k}:{v['ort']:.3g}" + (f"({v['isaret_pay']:.2f})" if v['isaret_pay'] == v['isaret_pay'] else '') for k, v in s.iterrows()))
print('\nyıllık IC (en üst beşte birlik satırları, h=1):')
icy = pd.DataFrame(ICY).T
print(icy[[i.endswith('h1_ust20') for i in icy.index]].round(3).to_string())
