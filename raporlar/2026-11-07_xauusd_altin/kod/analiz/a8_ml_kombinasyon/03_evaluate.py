"""Adım 3: walk-forward tahminlerini değerlendir (CT R² hm/0, Clark–West, isabet, net Sharpe ham/demeaned, uzun/kısa bacak, B&H, yıllar).
Dönemler: VAL = 2020-01..2021-12 (takvim olarak IS; model seçimi burada), OOS = 2022-01.. (tek sefer), ALL = 2020-01..
V3 (erken dönem tekrarı): 2013-01..2016-12 spot hedefi.
Her (varyant, model, h) bir hipotez testi olarak 'a8_ml_<V>' ailesine kaydedilir."""
from common import *

clear_family(["a8_ml_V1", "a8_ml_V2", "a8_ml_V3"])
d = load_viop(); s = load_spot()
ML = ["ridge", "lasso", "enet", "hgb", "rf"]
res, yearly = [], []
for V in ("V1", "V2", "V3"):
    P_ = pd.read_parquet(f"{OUT}/preds_{V}.parquet"); P_["date"] = pd.to_datetime(P_["date"])
    # ML topluluğu (eşit ağırlıklı ortalama) — önceden belirlenmiş ek aday
    ens = P_[P_.model.isin(ML)].groupby(["date", "h"]).agg(yhat=("yhat", "mean"), ybar=("ybar", "first"), ybar_w=("ybar_w", "first")).reset_index(); ens["model"] = "ens_ml"
    P_ = pd.concat([P_, ens], ignore_index=True)
    src, ycol, rcol = (s, "sfwd{h}", "s_ret") if V == "V3" else (d, "fwd{h}", "v_ret")
    models = [m for m in P_.model.unique() if not m.endswith("_score")]
    for h in (1, 3, 5):
        y = src[ycol.format(h=h)]; ret = src[rcol]
        for m in models:
            q = P_[(P_.model == m) & (P_.h == h)].set_index("date")
            yhat, ybar = q.yhat, q.ybar
            if m.startswith("c1") or m.startswith("c2"):
                sc = P_[(P_.model == m + "_score") & (P_.h == h)].set_index("date").yhat
                timing = sc
            else:
                timing = yhat - q.ybar_w  # modelin kendi tabanına göre (winsorize ortalama); sıfır öznitelikli model → 0 = pozisyon yok
            pos_raw = np.sign(yhat); timing = timing.where(timing.abs() > 1e-9, 0.0); pos_tim = np.sign(timing)  # sayısal gürültü ±1e-19 → 0
            periods = {"EARLY": ("2013-01-01", "2016-12-31")} if V == "V3" else {"ALL": ("2020-01-01", "2026-12-31"), "VAL": ("2020-01-01", "2021-12-31"), "OOS": ("2022-01-01", "2026-12-31")}
            for pn, (a, b) in periods.items():
                yy = y.loc[a:b]; rr = ret.loc[a:b].dropna()
                fm = forecast_metrics(yy, yhat.loc[a:b], ybar.loc[a:b], h)
                icd = ic(timing.loc[a:b], yy, max(h, 5))
                row = dict(V=V, model=m, h=h, period=pn, ic=icd["ic"], ic_t=icd["t"], **fm)
                for pk, pos in (("raw", pos_raw), ("tim", pos_tim)):
                    bb = bt_block(pos.reindex(rr.index).fillna(0), rr, h)
                    row.update({f"{pk}_{k}": v for k, v in bb.items()})
                    b10 = backtest(pos.reindex(rr.index).fillna(0), rr, h, 10.0)
                    row[f"{pk}_sharpe_10bps"] = round(b10["sharpe"], 3) if b10 else np.nan
                res.append(row)
            # yıl yıl
            per = ("2013-01-01", "2016-12-31") if V == "V3" else ("2020-01-01", "2026-12-31")
            rr = ret.loc[per[0]:per[1]].dropna()
            ysh = yearly_sharpe(pos_tim.reindex(rr.index).fillna(0), rr, h)
            dd_ = pd.concat([timing.rename("x"), y.rename("y")], axis=1).loc[per[0]:per[1]].dropna()
            yic = dd_.groupby(dd_.index.year).apply(lambda g: g.x.corr(g.y, method="spearman")).round(3).to_dict()
            yearly.append(dict(V=V, model=m, h=h, **{f"sh{k}": v for k, v in ysh.items()}, **{f"ic{k}": v for k, v in yic.items()}))
            # kayıt
            if V == "V3":
                st = ic(timing.loc[per[0]:per[1]], y.loc[per[0]:per[1]], max(h, 5))
                register(AGENT, f"a8_ml_{V}", f"{V}_{m}_h{h}", f"{m} tahmini (zamanlama)", h, dict(ic=st["ic"], t=st["t"], n=st["n"]), note="spot 2013-2016 erken dönem")
            else:
                st = split_stats(timing.loc[per[0]:], y.loc[per[0]:], h)
                fm_all = [r_ for r_ in res if r_["V"] == V and r_["model"] == m and r_["h"] == h and r_["period"] == "ALL"][0]
                register(AGENT, f"a8_ml_{V}", f"{V}_{m}_h{h}", f"{m} tahmini (zamanlama)", h, st,
                         note=f"IS=2020-21 doğrulama, OOS=2022+; R2hm={fm_all.get('r2_hm', np.nan):.4f} CWt={fm_all.get('cw_t_hm', np.nan):.2f}")
R = pd.DataFrame(res); R.to_csv(f"{OUT}/eval_all.csv", index=False)
Y = pd.DataFrame(yearly); Y.to_csv(f"{OUT}/eval_yearly.csv", index=False)

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 500)
cols = ["V", "model", "h", "period", "ic", "ic_t", "r2_hm", "r2_0", "cw_t_hm", "cw_t_0", "hit", "hit_base_long", "hit_timing", "raw_sharpe", "raw_sharpe_dm", "tim_sharpe", "tim_sharpe_dm", "tim_long_sharpe", "tim_short_sharpe", "tim_bh_sharpe", "tim_turnover"]
for pn in ("VAL", "OOS", "ALL", "EARLY"):
    print("=====", pn); print(R[R.period == pn][cols].round(4).to_string(index=False))

# Seçim: her h için VAL dönemindeki CW t (tarihsel ortalamaya karşı) en yüksek aday (V1+V2) → OOS tek sefer
sel = []
for h in (1, 3, 5):
    v = R[(R.period == "VAL") & (R.h == h) & (R.V.isin(["V1", "V2"]))].sort_values("cw_t_hm", ascending=False).iloc[0]
    o = R[(R.period == "OOS") & (R.h == h) & (R.V == v.V) & (R.model == v.model)].iloc[0]
    sel.append(dict(h=h, V=v.V, model=v.model, val_cw_t=v.cw_t_hm, val_r2_hm=v.r2_hm, oos_r2_hm=o.r2_hm, oos_r2_0=o.r2_0, oos_cw_t_hm=o.cw_t_hm, oos_cw_t_0=o.cw_t_0,
                    oos_ic=o.ic, oos_ic_t=o.ic_t, oos_tim_sharpe=o.tim_sharpe, oos_tim_sharpe_dm=o.tim_sharpe_dm, oos_raw_sharpe=o.raw_sharpe, oos_bh=o.tim_bh_sharpe))
SEL = pd.DataFrame(sel); SEL.to_csv(f"{OUT}/selection_val_to_oos.csv", index=False)
print("===== VAL'de seçilen → OOS"); print(SEL.round(4).to_string(index=False))
