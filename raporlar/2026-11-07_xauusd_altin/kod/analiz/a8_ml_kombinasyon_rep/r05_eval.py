"""Adım 5: walk-forward tahminlerinin bağımsız değerlendirmesi (kendi metrik kodum).
Kullanım: python3 r05_eval.py mine|analyst
 - mine: kendi r04 tahminlerim (mypreds_V*.parquet)
 - analyst: analistin preds_V*.parquet çıktıları (yalnız tahmin dosyası okunur; analistin kodu çalıştırılmaz) → değerlendirme katmanının doğrulaması
Ölçütler: CT R² (tarihsel ortalama ybar'a karşı: r2_hm; sıfıra karşı: r2_0), Clark–West NW t (lag max(h,5)), zamanlama IC NW t,
zamanlama pozisyonu sign(ŷ − ybar_w) (C1/C2: sign(skor)) ile kademeli net 5 bps Sharpe, demeaned, uzun/kısa, B&H, 10 bps, devir.
Ek: yarım gün (arife) satırları dışlanarak OOS."""
import sys, numpy as np, pandas as pd
from rep_stats import nw_t_mean, ic_test, bt, bt_full
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"; OUT = f"{S}/out/a8_ml_kombinasyon_rep"
WHO = sys.argv[1]
v = pd.read_parquet(f"{OUT}/base_viop.parquet"); sp = pd.read_parquet(f"{OUT}/base_spot.parquet")
hd = pd.read_parquet(f"{OUT}/halfday_flag.parquet").index
ML = ["ridge", "lasso", "enet", "hgb", "rf"]
rows, yrs = [], []
for V in ("V1", "V2", "V3"):
    f = f"{OUT}/mypreds_{V}.parquet" if WHO == "mine" else f"{S}/out/a8_ml_kombinasyon/preds_{V}.parquet"
    try: P = pd.read_parquet(f)
    except Exception as e: print("yok", f); continue
    P["date"] = pd.to_datetime(P.date)
    ens = P[P.model.isin(ML)].groupby(["date", "h"]).agg(yhat=("yhat", "mean"), ybar=("ybar", "first"), ybar_w=("ybar_w", "first")).reset_index(); ens["model"] = "ens_ml"
    P = pd.concat([P, ens], ignore_index=True)
    tgt, ret = (sp, sp.s_ret) if V == "V3" else (v, v.ret)
    pers = {"EARLY": ("2013-01-01", "2016-12-31")} if V == "V3" else {"ALL": ("2020-01-01", "2026-12-31"), "VAL": ("2020-01-01", "2021-12-31"), "OOS": ("2022-01-01", "2026-12-31")}
    for m in [x for x in P.model.unique() if not x.endswith("_score")]:
        for h in (1, 3, 5):
            q = P[(P.model == m) & (P.h == h)].set_index("date").sort_index()
            if q.empty: continue
            y = (sp if V == "V3" else v)[f"{'sfwd' if V == 'V3' else 'fwd'}{h}"]
            if m.startswith(("c1", "c2")):
                tim = P[(P.model == m + "_score") & (P.h == h)].set_index("date").sort_index().yhat
            else:
                tim = q.yhat - q.ybar_w
            tim = tim.where(tim.abs() > 1e-9, 0.0); pos = np.sign(tim)
            for pn, (a, b) in pers.items():
                d = pd.concat([y.rename("y"), q.yhat.rename("f"), q.ybar.rename("b")], axis=1).loc[a:b].dropna()
                em, eb, e0 = (d.y - d.f) ** 2, (d.y - d.b) ** 2, d.y ** 2
                L = max(h, 5)
                r2hm = 1 - em.sum() / eb.sum(); r20 = 1 - em.sum() / e0.sum()
                cw = eb - (em - (d.b - d.f) ** 2)
                icd = ic_test(tim.loc[a:b], y.loc[a:b], L)
                rr = ret.loc[a:b].dropna()
                B = bt_full(pos.reindex(rr.index).fillna(0), rr, h)
                row = dict(V=V, model=m, h=h, period=pn, n=len(d), r2_hm=r2hm, r2_0=r20, cw_t=nw_t_mean(cw, L), ic=icd["ic"], ic_t=icd["t"],
                           frac_zero=float((pos.loc[a:b] == 0).mean()), **{f"tim_{k}": val for k, val in B.items()})
                if pn == "OOS":
                    pz = pos.copy(); pz[pz.index.isin(hd)] = 0
                    row["tim_sh_no_halfday"] = bt_full(pz.reindex(rr.index).fillna(0), rr, h)["sh"]
                    t2 = tim.copy(); t2[t2.index.isin(hd)] = np.nan
                    row["ic_t_no_halfday"] = ic_test(t2.loc[a:b], y.loc[a:b], L)["t"]
                rows.append(row)
            per = ("2013-01-01", "2016-12-31") if V == "V3" else ("2020-01-01", "2026-12-31")
            rr = ret.loc[per[0]:per[1]].dropna(); z = bt(pos.reindex(rr.index).fillna(0), rr, h)
            if z:
                g = z["pnl"].groupby(z["pnl"].index.year)
                yrs.append(dict(V=V, model=m, h=h, **{f"sh{k}": round(float(x.mean() / x.std() * np.sqrt(252)), 2) for k, x in g}))
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/eval_{WHO}.csv", index=False); pd.DataFrame(yrs).to_csv(f"{OUT}/eval_yearly_{WHO}.csv", index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_rows", 400); pd.set_option("display.max_columns", 40)
cols = ["V", "model", "h", "period", "r2_hm", "r2_0", "cw_t", "ic", "ic_t", "tim_sh", "tim_sh_dm", "tim_long", "tim_short", "tim_bh", "tim_sh10", "tim_turn", "frac_zero"]
for pn in ("VAL", "OOS", "ALL", "EARLY"):
    X = R[R.period == pn]
    if X.empty: continue
    print("=====", pn); print(X[cols].round(4).to_string(index=False))
# özetler
for V in ("V1", "V2", "V3"):
    for pn in ("VAL", "OOS", "EARLY"):
        X = R[(R.V == V) & (R.period == pn)]
        if X.empty: continue
        print(f"{V} {pn}: R2_hm>0 {int((X.r2_hm > 0).sum())}/{len(X)}  max R2_hm {X.r2_hm.max():.5f} ({X.loc[X.r2_hm.idxmax(), 'model']} h{X.loc[X.r2_hm.idxmax(), 'h']})"
              f"  CW t>1.645 {int((X.cw_t > 1.645).sum())}  max CW t {X.cw_t.max():.2f}  tim Sharpe>0 {int((X.tim_sh > 0).sum())}/{len(X)}")
# VAL'de seçim → OOS
sel = []
for h in (1, 3, 5):
    X = R[(R.period == "VAL") & (R.h == h) & R.V.isin(["V1", "V2"])].sort_values("cw_t", ascending=False)
    if X.empty: continue
    w = X.iloc[0]; o = R[(R.period == "OOS") & (R.h == h) & (R.V == w.V) & (R.model == w.model)].iloc[0]
    sel.append(dict(h=h, V=w.V, model=w.model, val_cw_t=w.cw_t, val_r2=w.r2_hm, oos_r2=o.r2_hm, oos_r2_0=o.r2_0, oos_cw_t=o.cw_t, oos_ic=o.ic, oos_ic_t=o.ic_t,
                    oos_sh=o.tim_sh, oos_sh_dm=o.tim_sh_dm, oos_bh=o.tim_bh, oos_turn=o.tim_turn, oos_frac_zero=o.frac_zero))
SEL = pd.DataFrame(sel); SEL.to_csv(f"{OUT}/selection_{WHO}.csv", index=False); print("===== VAL seçimi → OOS"); print(SEL.round(4).to_string(index=False))
