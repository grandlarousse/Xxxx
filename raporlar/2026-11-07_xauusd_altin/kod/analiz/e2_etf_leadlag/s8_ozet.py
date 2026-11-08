"""s8: kayıt sayımı, ajan içi BH-FDR, aday güven etiketleri, 'uzun-varsayılan' kaplama sürümü, placebo tablosu."""
from e2_common import *
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ"]}
reg = pd.read_csv(f"{lib_altin.REG_DIR}/{AGENT}.csv")
reg["q_fdr"] = bh_fdr(reg["p"].fillna(1).values)
reg.to_csv(f"{OUT}/s8_kayit_fdr.csv", index=False)
print("toplam kayıtlı test:", len(reg)); print(reg.groupby("family").size().to_string())
print("p<0.05:", int((reg.p < 0.05).sum()), " q<0.10:", int((reg.q_fdr < 0.10).sum()), " q<0.05:", int((reg.q_fdr < 0.05).sum()))
pd.set_option("display.width", 250)
print(reg.sort_values("p").head(30)[["family", "test_id", "h", "ic", "t", "t_is", "t_oos", "yrs_same_sign", "yrs", "q_fdr"]].round(4).to_string())
J = json.load(open(f"{OUT}/s6_secim_uc.json")); T = pd.read_csv(f"{OUT}/s6_strateji_ozet.csv")
MECH = {"C1_madenci_oncu_GLD": True, "C1j_madenciJ_oncu_GLD": True, "C2_artik_momentum_GDX": True, "C2j_artik_momentum_GDXJ": True,
        "C3_gunici_altin_GDX_donus": True, "C4_platin5_GDX_donus": False, "C5_asya_madenci_GLD": True, "C5g_asya_madenci_GDX": True}
lab = {}
for cn, c in J["chosen"].items():
    oos = T[(T.label == cn) & (T.cost == "base") & (T.period == "oos")].iloc[0]
    st = dict(t=c["t"], t_is=c["t_is"], t_oos=c["t_oos"], yrs=c["yrs"], yrs_same_sign=c["yrs_same_sign"])
    L = label_conf(st, MECH[cn], oos_sh_long=oos.sh_long, oos_sh_any=oos.sh_ideal, oos_bh=oos.sh_bh, oos_long_dm=oos.sh_long_dm)
    lab[cn] = dict(label=L, oos_sh_long=oos.sh_long, oos_sh_ideal=oos.sh_ideal, oos_sh_ideal_dm=oos.sh_ideal_dm, oos_sh_long_inv=oos.sh_long_inv, oos_bh=oos.sh_bh, **c)
    print(cn, L, {k: lab[cn][k] for k in ["t", "t_is", "t_oos", "t_22", "yrs_same_sign", "yrs", "oos_sh_long", "oos_sh_ideal_dm", "oos_sh_long_inv", "oos_bh"]})
json.dump(lab, open(f"{OUT}/s8_etiketler.json", "w"), indent=1, default=str)
# 'uzun-varsayılan' kaplama: GLD/GDX tut, yalnız ayı sinyalinde nakit (C1, C5)
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl"); SIGA = pd.read_pickle(f"{OUT}/s7_signals.pkl")
rows = []
for cn, x, und, h, q in [("C1_madenci_oncu_GLD", SIG1[("GDX~GLD+SPY", 10)], "GLD", 5, 0.8), ("C5_asya_madenci_GLD", SIGA[int(eval(J["chosen"]["C5_asya_madenci_GLD"]["key"]))], "GLD", J["chosen"]["C5_asya_madenci_GLD"]["h"], J["chosen"]["C5_asya_madenci_GLD"]["q"])]:
    p = pos_from_signal(x, +1, q); ov = pd.Series(1.0, index=p.index); ov[p < 0] = 0.0
    r = R[und]
    for nm, s, e in [("full", None, None), ("is", None, "2017-12-31"), ("oos", "2018-01-01", None), ("2022+", "2022-01-01", None)]:
        rr = r.copy()
        if s: rr = rr[rr.index >= s]
        if e: rr = rr[rr.index <= e]
        rr = rr.dropna()
        a = backtest(ov.reindex(rr.index), rr, h, COST["base"]); b = backtest(pd.Series(1.0, index=rr.index), rr, 1, 0)
        a2 = backtest(ov.reindex(rr.index), rr, h, COST["base"], demean=True)
        rows.append(dict(cand=cn, period=nm, sh_overlay=round(a["sharpe"], 3), ann_overlay=round(a["ann_ret"] * 100, 2), vol_overlay=round(a["ann_vol"] * 100, 2),
                         sh_bh=round(b["sharpe"], 3), ann_bh=round(b["ann_ret"] * 100, 2), vol_bh=round(b["ann_vol"] * 100, 2), expo=round(a["exposure"], 2),
                         maxdd_overlay=round(float((a["pnl"].cumsum() - a["pnl"].cumsum().cummax()).min() * 100), 1),
                         maxdd_bh=round(float((b["pnl"].cumsum() - b["pnl"].cumsum().cummax()).min() * 100), 1)))
ov = pd.DataFrame(rows); ov.to_csv(f"{OUT}/s8_uzun_varsayilan.csv", index=False); print(ov.to_string())
# placebo tablosu
F3 = pd.read_pickle(f"{OUT}/s3_signals.pkl")
gi = np.log(d["xau_cut"]) - np.log(d["xau_close"].shift(1))
pl = {}
for nm, x, und, h in [("C1", SIG1[("GDX~GLD+SPY", 10)], "GLD", 5), ("C2", SIG1[("GDX~GLD+SPY", 3)], "GDX", 3), ("C2j", SIG1[("GDXJ~GLD+SPY", 1)], "GDXJ", 3),
                      ("C3", -gi, "GDX", 1), ("C4", -F3[("PLATIN", "d5")], "GDX", 3), ("C5", SIGA[1], "GLD", 3)]:
    pl[nm] = placebo_lead(x, R[und], h)
pl = pd.DataFrame(pl).T; pl.to_csv(f"{OUT}/s8_placebo.csv"); print(pl.to_string())
