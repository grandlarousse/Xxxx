"""Model tanımları (hiperparametreler ÖNCEDEN sabit; ridge/lasso/EN cezası yalnız eğitim penceresi içinde, ambargolu iç doğrulamayla seçilir)."""
import numpy as np, pandas as pd
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor

MODELS = ["ridge", "lasso", "enet", "hgb", "rf", "c1_apriori", "c2_icsign_all", "c2_icsign_sel"]
# Önceden belirlenmiş basit sinyaller ve a priori işaretleri (literatür / mekanizma; veriden SEÇİLMEDİ)
C1 = {"px_r20": +1,      # 1 aylık zaman serisi momentumu
      "px_r250": +1,     # 12 aylık momentum
      "xa_dxy_d5": -1,   # dolar güçlenmesi → altın zayıf (yetersiz tepki varsayımı)
      "rt_real10_d5": -1,  # reel faiz artışı → altın zayıf
      "sh_prem_d5": +1,  # Şanghay primi artışı = Çin fiziki talebi
      "cot_mm_z52": -1}  # spekülatif pozisyon aşırılığı → ters yön


def standardize(Xtr, Xte, min_cov=0.5):
    keep = (Xtr.notna().mean() >= min_cov) & (Xtr.std() > 0)
    Xtr = Xtr.loc[:, keep]; Xte = Xte.loc[:, keep]
    mu = Xtr.mean(); sd = Xtr.std()
    Ztr = ((Xtr - mu) / sd).clip(-5, 5); Zte = ((Xte - mu) / sd).clip(-5, 5)
    return Ztr, Zte


def _val_split(n, h, frac=0.75):
    cut = int(n * frac)
    return np.arange(cut), np.arange(min(cut + h, n - 1), n)


def _select_linear(make, grid, Z, y, h):
    tr, va = _val_split(len(Z), h)
    best, ba = np.inf, grid[-1]
    for a in grid:
        m = make(a).fit(Z[tr], y[tr]); e = np.mean((y[va] - m.predict(Z[va])) ** 2)
        if e < best - 1e-18: best, ba = e, a
    return ba


def fit_predict(Xtr, ytr, Xte, h, models=MODELS):
    Ztr, Zte = standardize(Xtr, Xte)
    lo, hi = ytr.quantile([0.01, 0.99]); yw = ytr.clip(lo, hi).values
    Z0 = Ztr.fillna(0).values; T0 = Zte.fillna(0).values
    n = len(Z0); out, diag = {}, {}
    if "ridge" in models:
        grid = list(np.logspace(0, 5.5, 12))
        a = _select_linear(lambda a: Ridge(alpha=a), grid, Z0, yw, h)
        out["ridge"] = Ridge(alpha=a).fit(Z0, yw).predict(T0); diag["ridge_alpha"] = a
    yc = yw - yw.mean(); amax = np.max(np.abs(Z0.T @ yc)) / n
    for nm, l1 in (("lasso", 1.0), ("enet", 0.5)):
        if nm in models:
            grid = list(amax / l1 * np.logspace(-2.5, 0, 10))
            a = _select_linear(lambda a: ElasticNet(alpha=a, l1_ratio=l1, max_iter=5000), grid, Z0, yw, h)
            m = ElasticNet(alpha=a, l1_ratio=l1, max_iter=5000).fit(Z0, yw)
            out[nm] = m.predict(T0); diag[f"{nm}_nnz"] = int((np.abs(m.coef_) > 0).sum())
    if "hgb" in models:
        m = HistGradientBoostingRegressor(max_iter=150, learning_rate=0.03, max_depth=3, min_samples_leaf=50, l2_regularization=1.0,
                                          early_stopping=False, random_state=0)
        out["hgb"] = m.fit(Ztr.values, yw).predict(Zte.values)
    if "rf" in models:
        m = RandomForestRegressor(n_estimators=200, max_depth=5, min_samples_leaf=50, max_features=0.33, n_jobs=1, random_state=0)
        out["rf"] = m.fit(Z0, yw).predict(T0)

    def comp(cols_signs):
        cs = {c: s for c, s in cols_signs.items() if c in Ztr.columns}
        if not cs: return np.zeros(len(T0)), np.zeros(n)
        str_ = sum(Ztr[c].clip(-3, 3).fillna(0) * s for c, s in cs.items()) / len(cs)
        ste = sum(Zte[c].clip(-3, 3).fillna(0) * s for c, s in cs.items()) / len(cs)
        return ste.values, str_.values

    def to_fc(sc_te, sc_tr):
        v = np.var(sc_tr)
        b = max(np.cov(sc_tr, yw)[0, 1] / v, 0.0) if v > 0 else 0.0  # a priori işaret: eğim negatifse 0'a kırp
        return yw.mean() + b * sc_te, sc_te
    if "c1_apriori" in models:
        out["c1_apriori"], out["c1_apriori_score"] = to_fc(*comp(C1))
    if "c2_icsign_all" in models or "c2_icsign_sel" in models:
        r = pd.DataFrame(Z0, columns=Ztr.columns).rank().corrwith(pd.Series(yw).rank())
        sg = np.sign(r).fillna(0)
        out["c2_icsign_all"], out["c2_icsign_all_score"] = to_fc(*comp(sg[sg != 0].to_dict()))
        tt = r.abs() * np.sqrt(n / max(h, 1))
        sel = sg[(tt > 2) & (sg != 0)]
        diag["c2_nsel"] = int(len(sel)); diag["c2_sel"] = ",".join(sel.index[:20])
        out["c2_icsign_sel"], out["c2_icsign_sel_score"] = to_fc(*comp(sel.to_dict())) if len(sel) else (np.full(len(T0), yw.mean()), np.zeros(len(T0)))
    diag["n_train"] = n; diag["n_feat"] = Ztr.shape[1]
    return out, diag, float(ytr.mean()), float(yw.mean())
