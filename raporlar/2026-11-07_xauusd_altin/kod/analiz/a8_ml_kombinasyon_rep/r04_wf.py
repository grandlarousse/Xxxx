"""Adım 4: bağımsız walk-forward (aylık yeniden eğitim, genişleyen pencere, h günlük ambargo). Kullanım: python3 r04_wf.py V1|V2|V3
 V1: VİOP endeksi, set B (102 öznitelik), hedef kendi VİOP fwd_h, eğitim 2017-03'ten, test 2020-01..
 V2: spot endeksi set A (83), hedef spot sfwd_h (15:00→15:00), eğitim 2011-01'den; tahmin VİOP günlerinde (as-of öznitelikler), test 2020-01..
 V3: spot, set A, eğitim 2011-01.., test 2013-01..2016-12 (hedef sfwd_h).
Modeller rapordaki önceden sabit hiperparametrelerle, kendi kodumla: ridge, lasso, enet, hgb, rf, C1 (a priori), C2 (IC işareti all/sel).
n_jobs=1."""
import os, sys, time
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np, pandas as pd
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a8_ml_kombinasyon_rep"
V = sys.argv[1]
XS = pd.read_parquet(f"{OUT}/feat_spot.parquet"); XV = pd.read_parquet(f"{OUT}/feat_viop.parquet"); info = pd.read_csv(f"{OUT}/feat_info.csv")
sp = pd.read_parquet(f"{OUT}/base_spot.parquet"); vb = pd.read_parquet(f"{OUT}/base_viop.parquet")
A = info.feature[info.set == "A"].tolist(); B = info.feature.tolist()
C1 = {"px_r20": 1, "px_r250": 1, "xa_dxy_d5": -1, "rt_real10_d5": -1, "sh_prem_d5": 1, "cot_mm_z52": -1}
cfg = dict(V1=(XV[B], vb, "fwd{h}", XV[B], "2017-03-01", ("2020-01-01", "2026-12-31")),
           V2=(XS[A], sp, "sfwd{h}", XV[A], "2011-01-01", ("2020-01-01", "2026-12-31")),
           V3=(XS[A], sp, "sfwd{h}", XS[A], "2011-01-01", ("2013-01-01", "2016-12-31")))[V]
Xtr_all, ysrc, ycol, Xte_all, tstart, (ta, tb) = cfg
ONLY = sys.argv[2].split(",") if len(sys.argv) > 2 else None
SEED = int(os.environ.get("SEED", "1"))
HS = [int(x) for x in os.environ.get("HS", "1,3,5").split(",")]


def zscore(Xtr, Xte):
    keep = (Xtr.notna().mean() >= 0.5) & (Xtr.std() > 0)
    Xtr, Xte = Xtr.loc[:, keep], Xte.loc[:, keep]
    mu, sd = Xtr.mean(), Xtr.std()
    return ((Xtr - mu) / sd).clip(-5, 5), ((Xte - mu) / sd).clip(-5, 5)


def pick_alpha(make, grid, Z, y, h):
    n = len(Z); cut = int(0.75 * n); tr = np.arange(cut); va = np.arange(min(cut + h, n - 1), n)
    errs = []
    for a in grid:
        m = make(a).fit(Z[tr], y[tr]); errs.append(np.mean((y[va] - m.predict(Z[va])) ** 2))
    errs = np.array(errs); i = int(np.argmin(errs))
    return grid[i]


def composite(Ztr, Zte, signs):
    cs = {c: s for c, s in signs.items() if c in Ztr.columns}
    if not cs: return np.zeros(len(Zte)), np.zeros(len(Ztr))
    a = sum(Ztr[c].clip(-3, 3).fillna(0) * s for c, s in cs.items()) / len(cs)
    b = sum(Zte[c].clip(-3, 3).fillna(0) * s for c, s in cs.items()) / len(cs)
    return b.values, a.values


def run(Xtr, ytr, Xte, h):
    Ztr, Zte = zscore(Xtr, Xte)
    lo, hi = np.quantile(ytr.values, [0.01, 0.99]); yw = np.clip(ytr.values, lo, hi)
    Z0, T0 = Ztr.fillna(0).values, Zte.fillna(0).values; n = len(Z0); out = {}; dg = {}
    want = lambda m: ONLY is None or m in ONLY
    if want("ridge"):
        a = pick_alpha(lambda a: Ridge(alpha=a), list(np.logspace(0, 5.5, 12)), Z0, yw, h)
        out["ridge"] = Ridge(alpha=a).fit(Z0, yw).predict(T0); dg["ridge_alpha"] = a
    amax = np.max(np.abs(Z0.T @ (yw - yw.mean()))) / n
    for nm, l1 in (("lasso", 1.0), ("enet", 0.5)):
        if want(nm):
            grid = list(amax / l1 * np.logspace(-2.5, 0, 10))
            a = pick_alpha(lambda a: ElasticNet(alpha=a, l1_ratio=l1, max_iter=5000), grid, Z0, yw, h)
            m = ElasticNet(alpha=a, l1_ratio=l1, max_iter=5000).fit(Z0, yw); out[nm] = m.predict(T0); dg[f"{nm}_nnz"] = int((m.coef_ != 0).sum())
    if want("hgb"):
        out["hgb"] = HistGradientBoostingRegressor(max_iter=150, learning_rate=0.03, max_depth=3, min_samples_leaf=50, l2_regularization=1.0,
                                                   early_stopping=False, random_state=SEED).fit(Ztr.values, yw).predict(Zte.values)
    if want("rf"):
        out["rf"] = RandomForestRegressor(n_estimators=200, max_depth=5, min_samples_leaf=50, max_features=0.33, n_jobs=1,
                                          random_state=SEED).fit(Z0, yw).predict(T0)
    def fc(te, tr_):
        vv = np.var(tr_); bb = max(np.cov(tr_, yw)[0, 1] / vv, 0.0) if vv > 0 else 0.0
        return yw.mean() + bb * te
    if want("c1_apriori"):
        te, tr_ = composite(Ztr, Zte, C1); out["c1_apriori"] = fc(te, tr_); out["c1_apriori_score"] = te
    if want("c2_icsign_sel") or want("c2_icsign_all"):
        rk = pd.DataFrame(Z0, columns=Ztr.columns).rank().corrwith(pd.Series(yw).rank())
        sg = np.sign(rk).fillna(0)
        te, tr_ = composite(Ztr, Zte, sg[sg != 0].to_dict()); out["c2_icsign_all"] = fc(te, tr_); out["c2_icsign_all_score"] = te
        sel = sg[(rk.abs() * np.sqrt(n / max(h, 1)) > 2) & (sg != 0)]
        if len(sel):
            te, tr_ = composite(Ztr, Zte, sel.to_dict()); out["c2_icsign_sel"] = fc(te, tr_); out["c2_icsign_sel_score"] = te
        else:
            out["c2_icsign_sel"] = np.full(len(T0), yw.mean()); out["c2_icsign_sel_score"] = np.zeros(len(T0))
        dg["c2_nsel"] = len(sel)
    dg.update(n_train=n, n_feat=Ztr.shape[1])
    return out, dg, float(ytr.mean()), float(yw.mean())


rows, diags = [], []; t0 = time.time()
tr_idx = Xtr_all.index; te_idx = Xte_all.index
test_days = te_idx[(te_idx >= ta) & (te_idx <= tb)]
for h in HS:
    y_all = ysrc[ycol.format(h=h)]
    for M in test_days.to_period("M").unique():
        td = test_days[test_days.to_period("M") == M]; T0 = td[0]
        p0 = tr_idx.searchsorted(T0); last = p0 - 1 - h
        if last < 100: continue
        tr = tr_idx[(tr_idx >= tstart) & (tr_idx <= tr_idx[last])]
        yt = y_all.reindex(tr); ok = yt.notna().values
        out, dg, ybar, ybw = run(Xtr_all.loc[tr][ok], yt[ok], Xte_all.loc[td], h)
        for k, val in out.items():
            rows.append(pd.DataFrame({"date": td, "h": h, "model": k, "yhat": val, "ybar": ybar, "ybar_w": ybw}))
        diags.append(dict(h=h, month=str(M), train_end=str(tr[-1].date()), **dg))
    print(V, "h", h, round(time.time() - t0), "s", flush=True)
suffix = ("" if ONLY is None else "_" + "_".join(ONLY)) + ("" if SEED == 1 else f"_s{SEED}") + ("" if HS == [1, 3, 5] else "_h" + "".join(map(str, HS)))
pd.concat(rows, ignore_index=True).to_parquet(f"{OUT}/mypreds_{V}{suffix}.parquet")
pd.DataFrame(diags).to_csv(f"{OUT}/mydiag_{V}{suffix}.csv", index=False)
print("bitti", V, round(time.time() - t0), "s")
