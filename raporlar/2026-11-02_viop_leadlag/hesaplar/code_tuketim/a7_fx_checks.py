"""A7: USDTRY aylık hedge davranışının IS/OOS kararlılığı + TRY=X ters-yön (BIST_{t-1}->TRY=X_t) zamanlama artefaktı kontrolü. Çıktı: a7_fx.csv"""
from common import *
fx = R("TRY=X"); xu = R("XU100"); rows = []
for s in ["ULKER", "AEFES", "BIMAS", "MGROS", "SOKM", "CCOLA"]:
    df = pd.concat([win(R(s), START).rename("a"), xu.rename("m"), fx.rename("fx")], axis=1).dropna()
    mo = df.resample("ME").sum(); mo = mo[mo.index < "2026-11-01"]
    for per, (a_, b_) in {"ALL": (None, None), "IS": (None, SPLIT), "OOS": (SPLIT, None)}.items():
        x = win(mo, a_, b_)
        pc = ll.partial_corr(x["a"], x["fx"], [x["m"]])[0]
        pc1 = ll.partial_corr(x["a"], x["fx"].shift(1), [x["m"]])[0]
        b, t = beta(x["a"] - x["m"], x["fx"])
        rows.append({"stock": s, "period": per, "n_m": len(x), "pc_month_fx": pc, "pc_month_fx_lag1": pc1, "beta_rel_on_fx": b, "t": t})
    # ters yön günlük
    c, t, n = nwcorr(fx, win(R(s), START).shift(1)); rows.append({"stock": s, "period": "rev_daily", "pc_month_fx": c, "t": t, "n_m": n})
c, t, n = nwcorr(fx, win(xu, START).shift(1)); rows.append({"stock": "XU100", "period": "rev_daily", "pc_month_fx": c, "t": t, "n_m": n})
pc = ll.partial_corr(fx, win(R("MGROS"), START).shift(1), [xu.shift(1)])[0]; rows.append({"stock": "MGROS|XU100", "period": "rev_daily_partial", "pc_month_fx": pc})
F = pd.DataFrame(rows); F.to_csv(CODE + "/a7_fx.csv", index=False); print(F.round(3).to_string(index=False))
