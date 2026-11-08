"""(f) Aday sinyallerin derin sağlamlık analizi: placebo, kontrol değişkenli NW regresyon, roll/uç-dönem dışlama, işlem kuralı (uzun/kısa bacak,
buy&hold, demeaned, 5/10 bps), yıllık Sharpe. Aday listesi ve kural yönü yalnız ilk taramadaki IS işaretine göre (OOS'a bakmadan) sabitlendi.
Önce a_..e_ betikleri çalışmış olmalı (özellik CSV'leri).
"""
from common import *

rd = lambda f: pd.read_csv(f"{OUT}/{f}", index_col=0, parse_dates=True)
A = rd("c_asia_features.csv"); Ev = rd("e_viop_features_t1.csv"); B = rd("b_shfe_features.csv"); G = rd("d_gpr_features.csv"); C = rd("a_cot_features_daily.csv")
for X_ in (A, Ev, B, G, C): X_.index = pd.to_datetime(X_.index)

# kontrol değişkenleri (hepsi gün t 15:00 UTC'de bilinir)
s_r1 = np.log(D.xau_p15 / D.xau_p15_prev)                     # spot 15:00(t-1) -> 15:00(t)
s_r5 = np.log(D.xau_p15 / D.xau_p15.shift(5))
s_r07_15 = np.log(D.xau_p15 / D.xau_p07)                       # gün t Londra/NY sabah hareketi
v_r1_lag = D.v_ret.shift(1)                                     # VİOP t-1 uzlaşma getirisi
CTRL = pd.concat([s_r1.rename("s_r1"), s_r5.rename("s_r5"), s_r07_15.rename("s_r07_15"), v_r1_lag.rename("v_r1_lag")], axis=1)

# Aday: (ad, seri, ufuklar, IS işareti, aile, bilgi zamanı)
CANDS = [
    ("cn_gold_res_comp", A["cn_gold_res_comp"], (3, 5), "asia", "07:00/08:10 UTC gün t (SSE/HKEX kapanışı)"),
    ("res600547_SS", A["res600547_SS"], (3, 5), "asia", "07:00 UTC gün t"),
    ("res1818_HK", A["res1818_HK"], (3, 5), "asia", "08:10 UTC gün t"),
    ("oi_d5_x_sgnret5", Ev["oi_d5_x_sgnret5"], (1, 5), "viop_pos", "t-1 VİOP bülteni (t-1 ~16:00 UTC)"),
    ("ag_dprem1", B["ag_dprem1"], (1,), "shfe", "07:00 UTC gün t"),
    ("r_HSI", A["r_HSI"], (1, 3), "asia", "08:10 UTC gün t"),
    ("gpr_z250", G["gpr_z250"], (3, 5), "gpr", "D ≤ t-2 (varsayım)"),
    ("g_swap_z52", C["g_swap_z52"], (5,), "cot", "Cuma 21:00 UTC -> Pzt"),
]

summ, bts, yrs, plac = [], [], [], []
for name, x, hs, fam, info in CANDS:
    x = x.reindex(D.index)
    for h in hs:
        y = D[f"fwd{h}"]
        st = split_stats(x, y, h)
        sgn = np.sign(st["ic_is"])                                 # kural yönü = IS işareti
        # 1) placebo
        pl = placebo_lead(x, R, h); pl.update(cand=name, h=h); plac.append(pl)
        # 2) kontrollü NW regresyon (x z-skor)
        xz = (x - x.mean()) / x.std()
        ctrl = CTRL.copy()
        if name.startswith(("res", "cn_gold")):
            ctrl["g_win"] = np.log(D.xau_p07 / D.xau_p07.shift(1))
        reg = nw_ols(y, pd.concat([xz.rename("x"), ctrl], axis=1), lags=max(h, 5))
        regI = nw_ols(y[y.index <= IS_END], pd.concat([xz.rename("x"), ctrl], axis=1)[y.index <= IS_END], lags=max(h, 5))
        regO = nw_ols(y[y.index > IS_END], pd.concat([xz.rename("x"), ctrl], axis=1)[y.index > IS_END], lags=max(h, 5))
        register(AG, fam + "_robust", f"deep_{name}_ctrl", f"{name} + kontroller (spot r1,r5,07-15, VİOP r_t-1)", h,
                 dict(ic=reg["b"], t=reg["t"], n=reg["n"], t_is=regI["t"], t_oos=regO["t"]), "NW OLS, b = z-skor başına getiri")
        # 3) roll±1 / uç dönem / sıfır hacim (yok) dışlama
        rx = T(x, fam + "_robust", f"deep_{name}_exroll_ext", f"{name} roll±1 ve Mart-Nis 2020, Oca-Şub 2026 hariç", hs=(h,), y_mask=(ROLL_NEAR | EXTREME), note="robust")[0]
        # 4) kurallar
        pos_sign = (sgn * np.sign(x)).fillna(0)
        q1, q2 = x[x.index <= IS_END].quantile([1 / 3, 2 / 3])
        pos_terc = pd.Series(np.where(x > q2, sgn, np.where(x < q1, -sgn, 0.0)), index=D.index).where(x.notna(), 0.0)
        for rule, pos in [("sign", pos_sign), ("tercile_IS", pos_terc)]:
            tb = legs_table(pos, h, f"{name}|{rule}"); bts.append(tb)
            rs = rule_stats(pos, h); register(AG, fam + "_rule", f"deep_{name}_{rule}", f"{name} kural {rule} (IS yönü {int(sgn):+d})", h, rs, "aktif günlerde pos×fwd (bps)")
            rsd = rule_stats(pos, h, demean=True)
            yp = yearly_pnl(pos, h);
            if yp is not None: yrs.append(dict(cand=name, h=h, rule=rule, **{str(k): v for k, v in yp.items()}))
            g = lambda leg, per, col: tb[(tb.leg == leg) & (tb.period == per) & (tb.cost_bps == 5)][col].iloc[0]
            g10 = lambda leg, per, col: tb[(tb.leg == leg) & (tb.period == per) & (tb.cost_bps == 10)][col].iloc[0]
            chg = float((pos.diff().abs() > 0).sum() / len(pos) * 252)
            summ.append(dict(cand=name, fam=fam, info=info, h=h, rule=rule, is_sign=int(sgn), ic=st["ic"], t_full=st["t"], t_is=st["t_is"], t_oos=st["t_oos"], yrs=f'{st["yrs_same_sign"]}/{st["yrs"]}',
                             t_ctrl=reg["t"], t_ctrl_is=regI["t"], t_ctrl_oos=regO["t"], t_exroll=rx["t"], t_exroll_oos=rx["t_oos"],
                             rule_bps=rs["ic"], rule_t=rs["t"], rule_t_oos=rs["t_oos"], rule_bps_dm=rsd["ic"], rule_t_dm=rsd["t"],
                             sh_full=g("LS", "full", "sharpe"), sh_is=g("LS", "is", "sharpe"), sh_oos=g("LS", "oos", "sharpe"), sh_oos_dm=g("LS", "oos", "sharpe_dm"), sh_full_dm=g("LS", "full", "sharpe_dm"),
                             sh_oos_10bps=g10("LS", "oos", "sharpe"), long_oos=g("long_leg", "oos", "sharpe"), long_oos_dm=g("long_leg", "oos", "sharpe_dm"),
                             short_oos=g("short_leg", "oos", "sharpe"), short_oos_dm=g("short_leg", "oos", "sharpe_dm"), bh_oos=tb[(tb.leg == "buyhold") & (tb.period == "oos")]["sharpe"].iloc[0],
                             turnover=g("LS", "full", "turnover"), sig_changes_yr=round(chg, 1), exposure=g("LS", "full", "exposure")))

S_ = pd.DataFrame(summ); S_.to_csv(f"{OUT}/f_deep_summary.csv", index=False)
pd.concat(bts).to_csv(f"{OUT}/f_deep_backtests.csv", index=False)
pd.DataFrame(yrs).to_csv(f"{OUT}/f_deep_yearly_sharpe.csv", index=False)
pd.DataFrame(plac).to_csv(f"{OUT}/f_deep_placebo.csv", index=False)
with pd.option_context("display.width", 300, "display.max_columns", 50):
    print(S_[["cand", "h", "rule", "t_full", "t_is", "t_oos", "yrs", "t_ctrl", "t_ctrl_is", "t_ctrl_oos", "t_exroll", "rule_bps", "rule_t", "rule_bps_dm", "rule_t_dm"]].round(2).to_string(index=False))
    print(S_[["cand", "h", "rule", "sh_full", "sh_is", "sh_oos", "sh_oos_dm", "sh_full_dm", "sh_oos_10bps", "long_oos", "long_oos_dm", "short_oos", "short_oos_dm", "bh_oos", "sig_changes_yr"]].to_string(index=False))
    print(pd.DataFrame(plac).to_string(index=False))
    print(pd.DataFrame(yrs).to_string(index=False))
