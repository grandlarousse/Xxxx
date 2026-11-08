"""Adım 8: tek değişkenli taramada en yüksek |t|'li birkaç sinyalin işlem kuralı karşılığı (yeni hipotez DEĞİL; 01'de kayıtlı
IC testlerinin ekonomik büyüklüğü). Kural: pos_t = sign(işaret × x_t) (x sıfır merkezli değişimler), t uzlaşmasında gir, h gün tut, kademeli.
VİOP 2017-03.. (IS ≤2021, OOS 2022+), spot 2011–2016 erken dönem (s_ret)."""
from common import *
from features import build

Xs, XV, info, s, d = build()
SIG = {"rt_curve_2s10s_d5": (+1, 1), "xa_gdx_rel1": (+1, 3), "seg_last1h": (+1, 5), "xa_aud_d5": (-1, 1), "cot_mm_z52": (-1, 5), "rt_nom2_d5": (-1, 1)}
rows = []
for f, (sg, h) in SIG.items():
    for hh in sorted({1, 3, 5}):
        x = XV[f] * sg; pos = np.sign(x)
        r = dict(feature=f, sign=sg, h=hh)
        for pn, (a, b) in {"FULL": ("2017-03-01", "2026-12-31"), "IS": ("2017-03-01", "2021-12-31"), "OOS": ("2022-01-01", "2026-12-31")}.items():
            rr = d.v_ret.loc[a:b].dropna(); bb = bt_block(pos.reindex(rr.index).fillna(0), rr, hh)
            r.update({f"{pn}_sh": bb["sharpe"], f"{pn}_shdm": bb["sharpe_dm"], f"{pn}_long": bb["long_sharpe"], f"{pn}_short": bb["short_sharpe"], f"{pn}_bh": bb["bh_sharpe"], f"{pn}_turn": bb["turnover"]})
            b10 = backtest(pos.reindex(rr.index).fillna(0), rr, hh, 10.0); r[f"{pn}_sh10"] = round(b10["sharpe"], 3)
        ys = yearly_sharpe(pos.reindex(d.index).fillna(0), d.v_ret, hh); r["yrs_pos"] = f"{sum(v > 0 for v in ys.values())}/{len(ys)}"
        st = split_stats(x, d[f"fwd{hh}"], hh); r.update(ic=st["ic"], t=st["t"], t_is=st["t_is"], t_oos=st["t_oos"], yrs_ic=f"{st['yrs_same_sign']}/{st['yrs']}")
        xe = Xs[f].loc["2011":"2016"] * sg; re_ = s.s_ret.loc["2011":"2016"].dropna()
        be = bt_block(np.sign(xe).reindex(re_.index).fillna(0), re_, hh); ie = ic(xe, s[f"sfwd{hh}"].loc["2011":"2016"], max(hh, 5))
        r.update(early_sh=be["sharpe"], early_shdm=be["sharpe_dm"], early_ic=ie["ic"], early_t=ie["t"])
        rows.append(r)
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/univ_bt.csv", index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_columns", 60)
print(R[["feature", "sign", "h", "ic", "t", "t_is", "t_oos", "yrs_ic", "FULL_sh", "FULL_shdm", "FULL_long", "FULL_short", "FULL_bh", "IS_sh", "OOS_sh", "OOS_shdm", "OOS_sh10", "FULL_turn", "yrs_pos", "early_ic", "early_t", "early_sh", "early_shdm"]].round(3).to_string(index=False))
