"""Adım 4: permütasyon önemi. Statik model: V1 (VİOP, set B) 2017-03..2021-12 (ambargo h) eğitimi, 2022-01.. testi.
Grup düzeyinde (fiyat, seans, çapraz varlık, faiz, oynaklık, COT, Şanghay, takvim, VİOP t-1, dk 15:00, GPR) ve öznitelik düzeyinde
MSE artışı ve Spearman IC düşüşü. Önem 'OOS performansına katkı' demektir; OOS R² negatifse önem de anlamsızdır."""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
from common import *
from features import build, feature_sets
from models import standardize, _select_linear
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor

Xs, XV, info, s, d = build(); A, B = feature_sets(info)
grp = info.set_index("feature").group
rng = np.random.default_rng(0)
rows, frows, base = [], [], []
for h in (1, 3, 5):
    y = d[f"fwd{h}"]; idx = XV.index
    T0 = pd.Timestamp("2022-01-03"); p0 = idx.searchsorted(T0); tr = idx[(idx >= "2017-03-01") & (idx <= idx[p0 - 1 - h])]
    te = idx[(idx >= T0)]; te = te[y.reindex(te).notna().values]
    m_ = y.reindex(tr).notna().values
    Ztr, Zte = standardize(XV.loc[tr, B][m_], XV.loc[te, B]); ytr = y.reindex(tr)[m_]
    lo, hi = ytr.quantile([.01, .99]); yw = ytr.clip(lo, hi).values; yte = y.reindex(te).values; ybar = float(ytr.mean())
    Z0 = Ztr.fillna(0).values; T_ = Zte.fillna(0)
    a = _select_linear(lambda a: Ridge(alpha=a), list(np.logspace(0, 5.5, 12)), Z0, yw, h)
    amax = np.max(np.abs(Z0.T @ (yw - yw.mean()))) / len(Z0)
    ae = _select_linear(lambda a: ElasticNet(alpha=a, l1_ratio=0.5, max_iter=5000), list(amax / 0.5 * np.logspace(-2.5, 0, 10)), Z0, yw, h)
    mods = {"ridge": (Ridge(alpha=a).fit(Z0, yw), True),
            "enet": (ElasticNet(alpha=ae, l1_ratio=0.5, max_iter=5000).fit(Z0, yw), True),
            "hgb": (HistGradientBoostingRegressor(max_iter=150, learning_rate=0.03, max_depth=3, min_samples_leaf=50, l2_regularization=1.0, early_stopping=False, random_state=0).fit(Ztr.values, yw), False),
            "rf": (RandomForestRegressor(n_estimators=200, max_depth=5, min_samples_leaf=50, max_features=0.33, n_jobs=1, random_state=0).fit(Z0, yw), True)}
    for nm, (mdl, fill) in mods.items():
        Xt = (T_ if fill else Zte).copy()
        pred0 = mdl.predict(Xt.values)
        mse0 = np.mean((yte - pred0) ** 2); r2hm = 1 - mse0 / np.mean((yte - ybar) ** 2); r20 = 1 - mse0 / np.mean(yte ** 2)
        ic0 = pd.Series(pred0).corr(pd.Series(yte), method="spearman")
        base.append(dict(h=h, model=nm, oos_r2_hm=r2hm, oos_r2_0=r20, oos_ic=ic0, alpha=a if nm == "ridge" else (ae if nm == "enet" else np.nan)))
        groups = {g: [c for c in Xt.columns if grp.get(c) == g] for g in sorted(set(grp[c] for c in Xt.columns))}
        for g, cols in groups.items():
            dm, di = [], []
            for rep in range(10):
                Xp = Xt.copy(); perm = rng.permutation(len(Xp))
                Xp[cols] = Xp[cols].values[perm]  # grup içi satırları birlikte karıştır (grup içi korelasyon korunur)
                pp = mdl.predict(Xp.values)
                dm.append(np.mean((yte - pp) ** 2) - mse0); di.append(ic0 - pd.Series(pp).corr(pd.Series(yte), method="spearman"))
            rows.append(dict(h=h, model=nm, group=g, n_feat=len(cols), d_mse_1e6=np.mean(dm) * 1e6, d_mse_sd=np.std(dm) * 1e6, d_ic=np.mean(di)))
        if nm in ("ridge", "hgb"):
            for c in Xt.columns:
                dm = []
                for rep in range(5):
                    Xp = Xt.copy(); Xp[c] = Xp[c].values[rng.permutation(len(Xp))]
                    dm.append(np.mean((yte - mdl.predict(Xp.values)) ** 2) - mse0)
                frows.append(dict(h=h, model=nm, feature=c, group=grp.get(c), d_mse_1e6=np.mean(dm) * 1e6))
    print("h", h, "bitti", flush=True)
BASE = pd.DataFrame(base); G = pd.DataFrame(rows); Fi = pd.DataFrame(frows)
BASE.to_csv(f"{OUT}/permimp_base.csv", index=False); G.to_csv(f"{OUT}/permimp_groups.csv", index=False); Fi.to_csv(f"{OUT}/permimp_features.csv", index=False)
pd.set_option("display.width", 250)
print(BASE.round(4).to_string(index=False))
print(G.pivot_table(index="group", columns=["model", "h"], values="d_mse_1e6").round(2).to_string())
for (h, m), g in Fi.groupby(["h", "model"]):
    print(h, m, g.sort_values("d_mse_1e6", ascending=False).head(8)[["feature", "d_mse_1e6"]].round(3).values.tolist())
