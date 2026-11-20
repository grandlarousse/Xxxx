"""A8 birleşik model — özellikler, yürüyen pencereli (walk-forward) modeller ve dondurulmuş kurallar.

Sözleşme (YONTEM_EK E1): build(P) -> kural sözlükleri listesi. P = elib.load(panel_klasoru).
Nedensellik: bütün özellikler shift/rolling ile t kapanışına kadarki veriden kurulur. Model her ayın ilk işlem
günü (s) yeniden eğitilir; eğitim satırları [s-750, s-1-h-5] aralığındadır (hedefin çıkışı, kilit kaydırması dâhil,
s-1'de tamamlanmıştır) ve o ayın bütün günleri bu modelle tahmin edilir. Hiperparametreler sabit sayıdır.
Deterministik: ridge kapalı form; lasso döngüsel koordinat inişi; LightGBM tek iş parçacığı, sabit tohum, örnekleme yok.
"""
import os
import sys
import math
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ortak'))
import elib  # noqa: E402

WIN, MINWIN, EMB_EXTRA = 750, 500, 5      # eğitim penceresi, en az geçmiş (işlem günü), kilit kaydırma payı
SEED = 7
STOCK_FEATS = ['r0', 'r1', 'r3', 'r5', 'r20', 'rel1', 'rel3', 'rel5', 'volshock', 'limup_prev', 'limup_touch',
               'limdn', 'vol20', 'liqrank']
DAY_FEATS = ['sec1', 'sec3', 'xu1', 'xu3', 'xres', 'big1', 'nlimup', 'dow_mon', 'dow_fri']
DAY_EXTRA = ['secvol20', 'breadth', 'vsh_med']
FSETS = {
    'rel1': ['rel1'],
    'donus': ['r0', 'r1', 'r3', 'r5', 'r20', 'rel1', 'rel3', 'rel5'],
    'donusdisi': ['volshock', 'limup_prev', 'limup_touch', 'limdn', 'vol20', 'liqrank'] + DAY_FEATS,
    'sec1': ['sec1'],
}
LGB_BASE = dict(objective='regression', learning_rate=0.05, lambda_l2=10.0, feature_fraction=1.0,
                bagging_fraction=1.0, bagging_freq=0, max_bin=63, min_gain_to_split=0.0, seed=SEED,
                deterministic=True, force_row_wise=True, num_threads=1, verbose=-1)


# --------------------------------------------------------------------------------------------- özellikler
def month_starts(dates):
    ym = np.asarray(dates.year) * 12 + np.asarray(dates.month)
    return np.flatnonzero(np.r_[True, ym[1:] != ym[:-1]])


def _csum(x, k):
    return x.rolling(k, min_periods=k).sum()


def features(P):
    """Hisse-gün özellik matrisi (yalnız t kapanışında bilinen). Dönen sözlük: sc, dates, X, pos, col, names, day..."""
    sc = sorted(elib.sector_cols(P))
    R = P['ret_cc'][sc].round(4)          # 1 bps'e yuvarla: paneller arası <1e-6 düzeltme farkı modele sızmasın
    dates = R.index
    T, M = R.shape
    trad = P['tradable'][sc]
    fill = P['fill_long'][sc]
    Rt = R.where(trad)
    n_tr = Rt.notna().sum(axis=1)
    ew = Rt.mean(axis=1).where(n_tr >= 3)
    F = {'r0': R, 'r1': R.shift(1), 'r3': _csum(R, 3), 'r5': _csum(R, 5), 'r20': _csum(R, 20)}
    for k in (1, 3, 5):
        F[f'rel{k}'] = _csum(R, k).sub(_csum(ew, k), axis=0)
    V = P['vol_tl'][sc]
    med20 = V.rolling(20, min_periods=10).median().shift(1)
    vsh = np.log((V / med20).clip(lower=0.05, upper=20.0))
    F['volshock'] = vsh
    lu = P['lim_up'][sc]
    F['limup_prev'] = lu.shift(1, fill_value=False).astype(float)
    F['limup_touch'] = (P['lim_up_touch'][sc] if 'lim_up_touch' in P else lu).astype(float)
    F['limdn'] = P['lim_dn'][sc].astype(float)
    F['vol20'] = R.rolling(20, min_periods=10).std()
    adv = elib.adv60(P)[sc].where(trad)
    F['liqrank'] = adv.rank(axis=1, pct=True)
    I = P['idx_ret'].reindex(dates)
    xu = I['XU030'].round(4)
    xe = I['XELKT'].round(4)
    beta = (xe.rolling(250, min_periods=60).cov(xu) / xu.rolling(250, min_periods=60).var()).shift(1).fillna(1.0)
    top5 = adv.rank(axis=1, ascending=False, method='first') <= 5
    Rb = Rt.where(top5)
    have = R.notna().sum(axis=1).clip(lower=1)
    D = pd.DataFrame(index=dates)
    D['sec1'] = ew
    D['sec3'] = _csum(ew, 3)
    D['xu1'] = xu
    D['xu3'] = _csum(xu, 3)
    D['xres'] = xe - beta * xu
    D['big1'] = Rb.mean(axis=1).where(Rb.notna().sum(axis=1) >= 3)
    D['nlimup'] = (lu & R.notna()).sum(axis=1) / have
    D['dow_mon'] = (dates.dayofweek == 0).astype(float)
    D['dow_fri'] = (dates.dayofweek == 4).astype(float)
    D['secvol20'] = ew.rolling(20, min_periods=10).std()
    D['breadth'] = (Rt > 0.02).sum(axis=1) / n_tr.clip(lower=1)
    D['vsh_med'] = vsh.where(trad).median(axis=1)
    D = D.round(8)
    names = STOCK_FEATS + DAY_FEATS
    X3 = np.empty((T, M, len(names)))
    for j, f in enumerate(STOCK_FEATS):
        X3[:, :, j] = F[f].values
    for j, f in enumerate(DAY_FEATS):
        X3[:, :, len(STOCK_FEATS) + j] = D[f].values[:, None]
    valid = (trad & F['r0'].notna() & F['rel1'].notna()).values
    rows = valid.ravel()
    pos = np.repeat(np.arange(T), M)[rows]
    col = np.tile(np.arange(M), T)[rows]
    X = np.round(X3.reshape(T * M, len(names))[rows], 8)
    return dict(sc=sc, dates=dates, T=T, M=M, X=X, pos=pos, col=col, names=names, day=D, fill=fill, trad=trad,
                starts=month_starts(dates), price=P['close_raw'][sc], adv=adv, rel1=F['rel1'])


# --------------------------------------------------------------------------------------------- modeller
def _standardize(Xtr, Xte):
    with np.errstate(all='ignore'):
        mu = np.nanmean(Xtr, axis=0)
        sd = np.nanstd(Xtr, axis=0)
    mu = np.where(np.isfinite(mu), mu, 0.0)
    sd = np.where(np.isfinite(sd) & (sd > 1e-12), sd, 1.0)
    Ztr = np.clip((Xtr - mu) / sd, -5, 5)
    Zte = np.clip((Xte - mu) / sd, -5, 5)
    Ztr[~np.isfinite(Ztr)] = 0.0
    Zte[~np.isfinite(Zte)] = 0.0
    return Ztr, Zte


def fit_predict(cfg, Xtr, ytr, Xte, collect=None):
    m = cfg['model']
    if m == 'lgbm':
        import lightgbm as lgb
        prm = dict(LGB_BASE, max_depth=cfg['depth'], num_leaves=2 ** cfg['depth'], min_data_in_leaf=cfg['leaf'])
        bst = lgb.train(prm, lgb.Dataset(Xtr, ytr, params={'max_bin': 63, 'verbose': -1}), num_boost_round=cfg.get('n', 80))
        if collect is not None:
            collect.append(bst.feature_importance('gain'))
        return bst.predict(Xte)
    Ztr, Zte = _standardize(Xtr, Xte)
    yb = float(ytr.mean())
    if m == 'ridge':
        k = Ztr.shape[1]
        b = np.linalg.solve(Ztr.T @ Ztr + cfg['lam'] * len(ytr) * np.eye(k), Ztr.T @ (ytr - yb))
        if collect is not None:
            collect.append(b)
        return yb + Zte @ b
    if m == 'lasso':
        from sklearn.linear_model import Lasso
        ys = float(ytr.std()) or 1.0
        mdl = Lasso(alpha=cfg['alpha'], fit_intercept=False, max_iter=5000, tol=1e-6, selection='cyclic')
        mdl.fit(Ztr, (ytr - yb) / ys)
        if collect is not None:
            collect.append(mdl.coef_.copy())
        return yb + ys * (Zte @ mdl.coef_)
    raise ValueError(m)


def walk_forward(pos, X, y, T, starts, h, cfg, min_rows, collect=None):
    """Her ay başında (s) [s-WIN, s-1-h-EMB_EXTRA] satırlarıyla eğit, [s, sonraki ay başı) satırlarını tahmin et."""
    pred = np.full(len(pos), np.nan)
    emb = h + EMB_EXTRA
    for j, s in enumerate(starts):
        if s < MINWIN:
            continue
        e = starts[j + 1] if j + 1 < len(starts) else T
        a = np.searchsorted(pos, s - WIN, 'left')
        b = np.searchsorted(pos, s - emb, 'left')
        t0 = np.searchsorted(pos, s, 'left')
        t1 = np.searchsorted(pos, e, 'left')
        if t1 <= t0 or b <= a:
            continue
        ok = np.isfinite(y[a:b])
        if ok.sum() < min_rows:
            continue
        pred[t0:t1] = fit_predict(cfg, X[a:b][ok], y[a:b][ok], X[t0:t1], collect)
    return pred


def cfg_tag(cfg):
    m = cfg['model']
    if m == 'ridge':
        t = f"ridge_l{cfg['lam']:g}"
    elif m == 'lasso':
        t = f"lasso_a{cfg['alpha']:g}"
    elif m == 'lgbm':
        t = f"lgbm_d{cfg['depth']}_m{cfg['leaf']}"
    else:
        t = 'naif'
    if cfg.get('fset'):
        t += '_' + cfg['fset']
    return t


def _cols_of(names, cfg):
    fs = FSETS[cfg['fset']] if cfg.get('fset') else names
    return [names.index(f) for f in fs]


def predict_sec(P, fe, h, cfg, cache, collect=None):
    """Kesit modeli: hedef = dolabilir hisse-günlerde 'sec' fazla f_h (±%10·√h kırpılmış). Dönen: tarih×hisse tahmin."""
    key = ('sec', cfg_tag(cfg), h)
    if key in cache:
        return cache[key]
    T, M = fe['T'], fe['M']
    first = [s for s in fe['starts'] if s >= MINWIN]
    if cfg['model'] == 'naive':
        pred = -fe['rel1'].values[fe['pos'], fe['col']]
        if first:
            pred = np.where(fe['pos'] >= first[0], pred, np.nan)
        else:
            pred = np.full(len(pred), np.nan)
    else:
        Mx, fl = elib.excess_measures(P, h, 'long', fe['sc'])
        c = 0.10 * math.sqrt(h)
        y = np.round(np.clip(Mx['sec'].where(fl).values, -c, c), 4)[fe['pos'], fe['col']]
        pred = walk_forward(fe['pos'], fe['X'][:, _cols_of(fe['names'], cfg)], y, T, fe['starts'], h, cfg, 1500, collect)
    A = np.full((T, M), np.nan)
    A[fe['pos'], fe['col']] = pred
    cache[key] = pd.DataFrame(A, index=fe['dates'], columns=fe['sc'])
    return cache[key]


def predict_day(P, fe, h, cfg, cache, collect=None):
    """Zamanlama modeli: hedef = dolabilir sektör sepetinin 'own' fazla f_h'i (günlük seri). Dönen: tarih serisi tahmin."""
    key = ('day', cfg_tag(cfg), h)
    if key in cache:
        return cache[key]
    names = DAY_FEATS + DAY_EXTRA
    D = fe['day'][names]
    Mx, fl = elib.excess_measures(P, h, 'long', fe['sc'])
    O = Mx['own'].where(fl)
    y = O.mean(axis=1).where(O.notna().sum(axis=1) >= 3)
    c = 0.10 * math.sqrt(h)
    y = np.round(np.clip(y.values, -c, c), 4)
    valid = (D['sec1'].notna() & D['xu1'].notna()).values
    pos = np.flatnonzero(valid)
    X = D.values[valid][:, _cols_of(names, cfg)]
    pred = walk_forward(pos, X, y[valid], fe['T'], fe['starts'], h, cfg, 300, collect)
    out = pd.Series(np.nan, index=fe['dates'])
    out.iloc[pos] = pred
    cache[key] = out
    return out


# --------------------------------------------------------------------------------------------- sinyaller
def top_signal(pred, uni, frac=0.2, min_n=5, bottom=False):
    """Evren (uni) içinde tahmine göre en üst (bottom=True ise en alt) frac dilim; k = tavan(n·frac); n < min_n ise sinyal yok."""
    Pm = pred.where(uni)
    n = Pm.notna().sum(axis=1)
    k = np.ceil(n * frac - 1e-9)
    rk = Pm.rank(axis=1, ascending=bottom, method='first')
    sig = rk.le(k, axis=0) & Pm.notna()
    sig[(n < min_n).values] = False
    return sig.astype(bool)


def spec_name(sp):
    if sp['kind'] == 'sec':
        s = f"A8_kesit_{cfg_tag(sp['cfg'])}_h{sp['h']}_{'alt' if sp.get('bottom') else 'ust'}{int(round(sp.get('frac', 0.2) * 100))}"
        return s + (f"_{sp['filt']}" if sp.get('filt') else '')
    if sp['kind'] == 'sec3':
        return f"A8_kesif_3hisse_{cfg_tag(sp['cfg'])}_h{sp['h']}_ust{int(round(sp.get('frac', 0.2) * 100))}_long_viop_own"
    if sp['kind'] == 'day':
        return f"A8_zaman_{cfg_tag(sp['cfg'])}_h{sp['h']}_e{int(round(sp['thr'] * 1e4))}"
    if sp['kind'] == 'viop':
        return (f"A8_tekhisse_{cfg_tag(sp['cfg'])}+{cfg_tag(sp['cfg_day'])}_h{sp['h']}_{sp['side']}_e{int(round(sp['thr'] * 1e4))}"
                f"_{sp.get('arac', 'viop')}")
    raise ValueError(sp['kind'])


def rule_sig(P, fe, sp, cache):
    """Kural tanımından sinyal matrisi (bool, tarih×hisse)."""
    fill = fe['fill']
    if sp['kind'] == 'sec':
        pred = predict_sec(P, fe, sp['h'], sp['cfg'], cache)
        uni = fill.copy()
        if sp.get('filt') == 'fiyat5':            # ham kapanış ≥ 5 TL
            uni = uni & (fe['price'] >= 5.0)
        elif sp.get('filt') == 'lik15':           # adv60 sırası ilk 15
            uni = uni & (fe['adv'].rank(axis=1, ascending=False, method='first') <= 15)
        return top_signal(pred, uni, sp.get('frac', 0.2), 5, bool(sp.get('bottom')))
    if sp['kind'] == 'sec3':                      # kesit en üst dilimi, yalnız VİOP'u olan hisseler (AKSEN/ENJSA/ODAS)
        sig = top_signal(predict_sec(P, fe, sp['h'], sp['cfg'], cache), fill, sp.get('frac', 0.2), 5, False)
        return sig[[c for c in elib.VIOP if c in sig.columns]]
    if sp['kind'] == 'day':
        pd_ = predict_day(P, fe, sp['h'], sp['cfg'], cache)
        on = (pd_ > sp['thr']) & (fill.sum(axis=1) >= 5)
        return fill & on.values[:, None]
    if sp['kind'] == 'viop':
        ps = predict_sec(P, fe, sp['h'], sp['cfg'], cache)
        pd_ = predict_day(P, fe, sp['h'], sp['cfg_day'], cache)
        cols = [c for c in elib.VIOP if c in ps.columns]
        comb = ps[cols].add(pd_, axis=0)
        if sp['side'] == 'long':
            return (comb > sp['thr']) & P['fill_long'][cols]
        return (comb < -sp['thr']) & P['fill_short'][cols]
    raise ValueError(sp['kind'])


# --------------------------------------------------------------------------------------------- dondurulmuş kurallar
# IS (2010-01-04 → 2022-12-30) taramasından sonra doldurulur; sayılar sabittir, P'den yeniden kestirilmez.
_LGB = {'model': 'lgbm', 'depth': 3, 'leaf': 500}       # 80 ağaç, öğrenme oranı 0.05, lambda_l2 10, max_bin 63 (LGB_BASE)
_RDG = {'model': 'ridge', 'lam': 1}                    # ceza = 1·n, standartlaştırılmış X
# BİRİNCİL KURAL YOK: IS'te hiçbir yapılandırma temel maliyet sonrası pozitif değil (bkz. ek/a8_model.md).
FROZEN = [
    {'spec': {'kind': 'sec', 'cfg': _LGB, 'h': 1, 'frac': 0.2}, 'olcu': 'sec', 'arac': 'spot', 'birincil': False,
     'aciklama': 'LightGBM(d3, yaprak≥500) aylık yürüyen pencere, 23 özellik → sec fazla f1 tahmini; dolabilir XELKT üyelerinde en üst beşte birlik AL, 1 gün'},
    {'spec': {'kind': 'sec', 'cfg': _LGB, 'h': 3, 'frac': 0.2}, 'olcu': 'sec', 'arac': 'spot', 'birincil': False,
     'aciklama': 'Aynı LightGBM, hedef sec fazla f3; en üst beşte birlik AL, 3 gün'},
    {'spec': {'kind': 'day', 'cfg': _RDG, 'h': 2, 'thr': 0.0025}, 'olcu': 'own', 'arac': 'spot', 'birincil': False,
     'aciklama': 'Ridge(lam=1) zamanlama modeli, 12 gün-düzeyi özellik → sektör sepeti own fazla f2 tahmini > +25 bps ise dolabilir bütün XELKT üyeleri AL, 2 gün'},
    {'spec': {'kind': 'day', 'cfg': _RDG, 'h': 3, 'thr': 0.0}, 'olcu': 'own', 'arac': 'spot', 'birincil': False,
     'aciklama': 'Aynı ridge zamanlama modeli, f3 tahmini > 0 ise dolabilir bütün XELKT üyeleri AL, 3 gün'},
    {'spec': {'kind': 'sec3', 'cfg': _LGB, 'h': 1, 'frac': 0.2}, 'olcu': 'own', 'arac': 'viop', 'birincil': False,
     'aciklama': 'KEŞİF (ızgara dışı): AKSEN/ENJSA/ODAS, LightGBM h1 kesit tahmininde en üst beşte birlikteyse VİOP AL, 1 gün'},
]


def build(P):
    fe = features(P)
    cache = {}
    out = []
    for fr in FROZEN:
        sp = fr['spec']
        out.append({'ad': fr.get('ad') or spec_name(sp), 'sig': rule_sig(P, fe, sp, cache), 'h': sp['h'],
                    'yon': sp.get('side', 'long'), 'olcu': fr['olcu'], 'arac': fr.get('arac', 'spot'),
                    'birincil': bool(fr.get('birincil', False)), 'aciklama': fr['aciklama']})
    return out
