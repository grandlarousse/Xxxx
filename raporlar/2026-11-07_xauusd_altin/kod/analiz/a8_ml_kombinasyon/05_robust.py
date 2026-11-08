"""Adım 5: sağlamlık. Ana adaylar (her V1/V2 modeli) için:
 (a) uç dönemler dışarıda (Mart 2020, Ocak–Şubat 2026), (b) vadesinde roll (v_code değişimi) içeren girişler sıfırlanır,
 (c) COT gecikmeli yayın dönemi (01.10.2025–31.12.2025) dışarıda, (d) sıfır hacimli günler (sayım), (e) 10 bps maliyet (eval_all'da),
 (f) h=1 için örtüşmeyen alt örneklem gerek yok; h=3/5 için her h günde bir giriş (bağımsız örnekleme) R² ve isabet.
Kayıt: her (V, model, h, kontrol) bir test ('a8_robust')."""
from common import *

clear_family(["a8_robust"])
d = load_viop()
ML = ["ridge", "lasso", "enet", "hgb", "rf"]
roll = (d.v_code != d.v_code.shift(1)).astype(int)
print("sıfır hacimli aktif kontrat günleri:", int((d.v_volume == 0).sum()), " roll günleri:", int(roll.sum()))
out = []
for V in ("V1", "V2"):
    P_ = pd.read_parquet(f"{OUT}/preds_{V}.parquet"); P_["date"] = pd.to_datetime(P_["date"])
    ens = P_[P_.model.isin(ML)].groupby(["date", "h"]).agg(yhat=("yhat", "mean"), ybar=("ybar", "first"), ybar_w=("ybar_w", "first")).reset_index(); ens["model"] = "ens_ml"
    P_ = pd.concat([P_, ens], ignore_index=True)
    for h in (1, 3, 5):
        y = d[f"fwd{h}"]; ret = d.v_ret.loc["2020-01-01":]
        roll_ahead = sum(roll.shift(-k) for k in range(1, h + 1)).fillna(0) > 0
        for m in [x for x in P_.model.unique() if not x.endswith("_score")]:
            q = P_[(P_.model == m) & (P_.h == h)].set_index("date")
            tim = P_[(P_.model == m + "_score") & (P_.h == h)].set_index("date").yhat if m.startswith("c") else q.yhat - q.ybar_w
            fc = q.yhat
            tim = tim.where(tim.abs() > 1e-9, 0.0)
            masks = {
                "base": pd.Series(True, index=q.index),
                "uc_haric": ~(((q.index >= "2020-03-01") & (q.index <= "2020-03-31")) | ((q.index >= "2026-01-01") & (q.index <= "2026-02-28"))),
                "roll_haric": ~roll_ahead.reindex(q.index).fillna(False),
                "cot_gecikme_haric": ~((q.index >= "2025-10-01") & (q.index <= "2025-12-31")),
            }
            for nm, mk in masks.items():
                mk = pd.Series(mk, index=q.index)
                fm = forecast_metrics(y.reindex(q.index)[mk], fc[mk], q.ybar[mk], h)
                st = split_stats(tim[mk], y.reindex(q.index)[mk], h)
                pos = np.sign(tim).where(mk, 0)
                rr = ret.copy()
                if nm == "uc_haric":
                    rr = rr[~(((rr.index >= "2020-03-01") & (rr.index <= "2020-03-31")) | ((rr.index >= "2026-01-01") & (rr.index <= "2026-02-28")))]
                bb = bt_block(pos.reindex(rr.index).fillna(0), rr, h)
                bo = bt_block(pos.reindex(rr.loc["2022":].index).fillna(0), rr.loc["2022":], h)
                out.append(dict(V=V, model=m, h=h, check=nm, ic=st["ic"], t=st["t"], t_is=st["t_is"], t_oos=st["t_oos"], r2_hm=fm.get("r2_hm"), r2_0=fm.get("r2_0"), cw_t_hm=fm.get("cw_t_hm"),
                                tim_sharpe_all=bb["sharpe"], tim_sharpe_dm_all=bb["sharpe_dm"], tim_sharpe_oos=bo["sharpe"], tim_sharpe_dm_oos=bo["sharpe_dm"]))
                if nm != "base" and m in ("ens_ml", "c1_apriori", "ridge", "rf"):
                    register(AGENT, "a8_robust", f"rob_{V}_{m}_h{h}_{nm}", f"{m} zamanlama, {nm}", h, st, note=f"R2hm={fm.get('r2_hm', np.nan):.4f}")
            # bağımsız örnekleme (h>1): her h günde bir
            if h > 1:
                for off in range(h):
                    ii = q.index[off::h]
                    fm = forecast_metrics(y.reindex(ii), fc.reindex(ii), q.ybar.reindex(ii), 1)
                    out.append(dict(V=V, model=m, h=h, check=f"bagimsiz_off{off}", r2_hm=fm.get("r2_hm"), r2_0=fm.get("r2_0"), cw_t_hm=fm.get("cw_t_hm"),
                                    ic=pd.concat([tim.reindex(ii), y.reindex(ii)], axis=1).dropna().corr(method="spearman").iloc[0, 1]))
O = pd.DataFrame(out); O.to_csv(f"{OUT}/robust.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 600)
print(O[~O.check.str.startswith("bagimsiz")].round(4).to_string(index=False))
print(O[O.check.str.startswith("bagimsiz")].groupby(["V", "model", "h"])[["r2_hm", "r2_0", "ic"]].mean().round(4).to_string())
