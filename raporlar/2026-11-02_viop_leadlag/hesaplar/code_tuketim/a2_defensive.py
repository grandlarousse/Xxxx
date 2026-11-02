"""A2: Defansiflik / koşullu beta. Olay günlerinde hissenin XU100'e göre göreli getirisi (cc/gap/intra), IS/OOS,
asimetrik (aşağı/yukarı) beta, olay sonrası t+1..t+5 göreli sürüklenme, USDTRY (aylık) hedge davranışı.
Çıktı: a2_events.csv, a2_betas.csv, a2_fx_monthly.csv"""
from common import *
import statsmodels.api as sm
S5 = STOCKS + ["CCOLA"]
X = DEC("XU100"); xcc = win(R("XU100"), START)
spx = zero_mask(R("^GSPC")); vix = zero_mask(R("^VIX")); sx5 = zero_mask(R("^STOXX50E")); fx = zero_mask(R("TRY=X"))
EV = {
 "US_riskoff_t-1 (SPX<=-2%)": spx.shift(1) <= np.log(0.98),
 "VIX_jump_t-1 (>=+20%)": vix.shift(1) >= np.log(1.20),
 "EU_riskoff_t (SX5E<=-2%, senkron)": sx5 <= np.log(0.98),
 "BIST_selloff_t (XU100<=-3%)": xcc <= np.log(0.97),
 "BIST_rally_t (XU100>=+3%)": xcc >= np.log(1.03),
 "TL_shock_t (USDTRY>=+1.5%)": fx >= np.log(1.015),
 "TL_shock_t-1 (USDTRY>=+1.5%)": fx.shift(1) >= np.log(1.015),
}
def tstat(x):
    x = x.dropna()
    if len(x) < 8: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
rows = []
for s in S5:
    d = DEC(s); a = win(R(s), START)
    rel = {"cc": a - xcc, "gap": d["gap"] - X["gap"], "intra": d["intra"] - X["intra"]}
    # beta-düzeltilmiş göreli (cc): a - b*xcc, b tam dönem
    b_full = beta(a, xcc)[0]
    rel["cc_badj"] = a - b_full * xcc
    fwd5 = sum((a - xcc).shift(-k) for k in range(1, 6))
    for en, ev in EV.items():
        ev = ev.reindex(a.index).fillna(False)
        for k, r in rel.items():
            for per, (st, en_) in {"ALL": (START, None), "IS": (START, SPLIT), "OOS": (SPLIT, None)}.items():
                x = win(r[ev.reindex(r.index).fillna(False)], st, en_).dropna()
                rows.append({"stock": s, "event": en, "leg": k, "period": per, "n": len(x), "mean_bps": 1e4 * x.mean() if len(x) else np.nan,
                             "t": tstat(x), "hit": float((x > 0).mean()) if len(x) else np.nan})
        x = win(fwd5[ev.reindex(fwd5.index).fillna(False)], START).dropna()
        rows.append({"stock": s, "event": en, "leg": "rel_fwd_t+1..t+5", "period": "ALL", "n": len(x), "mean_bps": 1e4 * x.mean(), "t": tstat(x), "hit": float((x > 0).mean())})
E = pd.DataFrame(rows); E.to_csv(CODE + "/a2_events.csv", index=False)
# --- koşullu / asimetrik beta
brow = []
for s in S5:
    a = win(R(s), START)
    for per, (st, en_) in {"ALL": (START, None), "IS": (START, SPLIT), "OOS": (SPLIT, None)}.items():
        df = pd.concat([win(a, st, en_).rename("y"), xcc.rename("m"), sx5.rename("eu"), spx.shift(1).rename("us1")], axis=1).dropna()
        up = df["m"].clip(lower=0); dn = df["m"].clip(upper=0)
        m = sm.OLS(df["y"], sm.add_constant(pd.concat([up.rename("up"), dn.rename("dn")], axis=1))).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        bfull = sm.OLS(df["y"], sm.add_constant(df["m"])).fit().params["m"]
        # kuyruk betası: XU100 <= -2% günleri
        tail = df[df["m"] <= np.log(0.98)]
        bt = sm.OLS(tail["y"], sm.add_constant(tail["m"])).fit().params["m"] if len(tail) > 20 else np.nan
        # global risk-off günlerinde (EU senkron <=-2%) XU100 betası
        g = df[df["eu"] <= np.log(0.98)]
        bg = sm.OLS(g["y"], sm.add_constant(g["m"])).fit().params["m"] if len(g) > 20 else np.nan
        # Wald: up==dn
        w = m.t_test("up - dn = 0")
        brow.append({"stock": s, "period": per, "beta": bfull, "beta_up": m.params["up"], "beta_dn": m.params["dn"], "t_up_minus_dn": float(np.ravel(w.tvalue)[0]),
                     "beta_tail_xu100<=-2%": bt, "n_tail": len(tail), "beta_on_EU_riskoff_days": bg, "n_eu": len(g)})
B = pd.DataFrame(brow); B.to_csv(CODE + "/a2_betas.csv", index=False)
# --- USDTRY hedge: aylık (21g) örtüşmesiz getiriler; TL ve USD bazlı; XU100 kontrollü
frow = []
fxa = R("TRY=X")
for s in S5 + ["XU100"]:
    a = win(R(s), START)
    df = pd.concat([a.rename("a"), win(R("XU100"), START).rename("m"), fxa.rename("fx")], axis=1).dropna()
    mo = df.resample("ME").sum()
    mo = mo[mo.index < "2026-11-01"]
    c = mo["a"].corr(mo["fx"]); pc = ll.partial_corr(mo["a"], mo["fx"], [mo["m"]])[0] if s != "XU100" else np.nan
    bb = beta(mo["a"], mo["fx"])
    # TL değer kaybının yüksek olduğu aylar (fx >= +3%) göreli performans
    big = mo[mo["fx"] >= np.log(1.03)]
    frow.append({"stock": s, "n_months": len(mo), "corr_monthly_fx": c, "pcorr_monthly_fx_xu100": pc, "beta_fx": bb[0], "beta_fx_t": bb[1],
                 "n_big_dev": len(big), "rel_vs_xu100_bigdev_pct": 100 * (big["a"] - big["m"]).mean() if s != "XU100" else np.nan,
                 "usd_ret_bigdev_pct": 100 * (big["a"] - big["fx"]).mean(), "usd_ret_all_pct": 100 * (mo["a"] - mo["fx"]).mean()})
F = pd.DataFrame(frow); F.to_csv(CODE + "/a2_fx_monthly.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
print(B.round(3).to_string()); print(F.round(3).to_string())
piv = E[(E.period == "ALL")].pivot_table(index=["event", "leg"], columns="stock", values="mean_bps").round(1)
print(piv.to_string())
piv = E[(E.period == "ALL")].pivot_table(index=["event", "leg"], columns="stock", values="t").round(2)
print(piv.to_string())
print(E[(E.leg == "cc") & (E.period == "ALL")].groupby("event")["n"].max())
