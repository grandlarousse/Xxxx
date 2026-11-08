"""Adım 3: kontroller, aday sinyallerin sağlamlığı, backtest (bacak ayrımı), erken dönem tekrarı. a5_02'den sonra çalıştır (kayda ekler).
Çıktı: controls.csv, robust.csv, backtests.csv, early.csv, placebo.csv"""
from a5_lib import *
import statsmodels.api as sm

sig = pd.read_parquet(f"{OUT}/signals_spot.parquet")
vp = load_viop(); sp = load_spot()
Y = {h: vp[f"fwd{h}"] for h in (1, 3, 5)}
V = lambda s: s.reindex(vp.index)
crow = []


def reg(fam, tid, pred, x, y, h, note=""):
    st = split_stats(x, y, h); register(AGENT, fam, tid, pred, h, st, note)
    crow.append(dict(fam=fam, test_id=tid, pred=pred, h=h, note=note, **{k: v for k, v in st.items() if k != "by_year"}, by_year=st["by_year"]))
    return st


def partial_t(y, X, h):
    d = pd.concat([y.rename("y"), X], axis=1).dropna()
    Z = (d - d.mean()) / d.std()
    m = sm.OLS(Z.y, sm.add_constant(Z.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": max(h, 5)})
    return m.params.drop("const").round(4).to_dict(), m.tvalues.drop("const").round(2).to_dict(), len(d)


# ---------- 1) Kontroller ----------
xag1 = np.log(sp.dk_XAGUSD_p15).diff()
for h in (1, 3, 5):
    reg("K_control", f"K_g12_h{h}", "g12 (altın 12->15 kendi getirisi)", V(sig.g12), Y[h], h)
    reg("K_control", f"K_g07_h{h}", "g07 (altın 07->15 kendi getirisi)", V(sig.g07), Y[h], h)
    reg("K_control", f"K_xag1_h{h}", "gümüş 15->15 getirisi (1 gün)", V(xag1), Y[h], h)
    reg("K_control", f"K_xag5_h{h}", "gümüş 15->15 getirisi (5 gün)", V(xag1.rolling(5).sum()), Y[h], h)
part = []
for h in (1, 3):
    for W in (60, 250):
        p, t, n = partial_t(Y[h], pd.concat([V(sig[f"I12_MACRO3_W{W}"]).rename("resid12"), V(sig.g12).rename("g12"), V(sig.g).rename("g1")], axis=1), h)
        part.append(dict(model=f"fwd{h} ~ I12_MACRO3_W{W} + g12 + g1", coef=p, t=t, n=n))
        register(AGENT, "K_control", f"K_partial_I12_MACRO3_W{W}_h{h}", "I12 artığı | g12, g1", h, dict(ic=p["resid12"], t=t["resid12"], n=n), "kısmi regresyon")
for h in (1, 3, 5):
    g5 = sig.g.rolling(5).sum(); s5 = xag1.rolling(5).sum()
    p, t, n = partial_t(Y[h], pd.concat([V(g5).rename("gold5"), V(s5).rename("silver5")], axis=1), h)
    part.append(dict(model=f"fwd{h} ~ gold5 + silver5", coef=p, t=t, n=n))
    register(AGENT, "K_control", f"K_partial_g5_s5_h{h}", "gold5 | silver5", h, dict(ic=p["gold5"], t=t["gold5"], n=n), "kısmi regresyon (gold5 katsayısı)")
pd.DataFrame(part).to_csv(f"{OUT}/partials.csv", index=False)

# ---------- 2) Adaylar ----------
# (etiket, sütun, h, seçim türü). 'IS' = kendi ailesinde IS |t| ile seçildi; 'posthoc' = tam dönem tablosundan göze çarpan (seçim yanlılığı var)
f60 = V(sig["I12F_MACRO3_W60"]); thr60 = f60.abs()[f60.index <= IS_END].quantile(0.8)
cond60 = V(sig["I12_MACRO3_W60"]).where(f60.abs() > thr60)
f250 = V(sig["I12F_MACRO3_W250"]); thr250 = f250.abs()[f250.index <= IS_END].quantile(0.8)
cond250 = V(sig["I12_MACRO3_W250"]).where(f250.abs() > thr250)
cands = [
    ("C1_I12c_MACRO3_W60_h3", cond60, "I12_MACRO3_W60", 3, "IS (C ailesi h=3)", dict(cond="W60")),
    ("C2_I12c_MACRO3_W250_h1", cond250, "I12_MACRO3_W250", 1, "IS (C ailesi h=1)", dict(cond="W250")),
    ("C3_I12_MACRO3_W60_h1", V(sig["I12_MACRO3_W60"]), "I12_MACRO3_W60", 1, "posthoc (koşulsuz)", {}),
    ("C4_I07_MACRO3_W60_h1", V(sig["I07_MACRO3_W60"]), "I07_MACRO3_W60", 1, "posthoc", {}),
    ("B1_GSRD_k5_h1", V(sig["GSRD_k5"]), "GSRD_k5", 1, "posthoc (B tam dönem en iyi)", {}),
    ("B2_GSRD_k3_h3", V(sig["GSRD_k3"]), "GSRD_k3", 3, "posthoc", {}),
    ("A1_MACRO3_W250_k3_h1", V(sig["R_MACRO3_W250_k3"]), "R_MACRO3_W250_k3", 1, "posthoc (A tam dönem)", {}),
    ("A2_USDJPY_W60_k3_h1", V(sig["R_USDJPY_W60_k3"]), "R_USDJPY_W60_k3", 1, "posthoc (A tam dönem en iyi)", {}),
    ("A3_EURUSD_W60_k1_h1", V(sig["R_EURUSD_W60_k1"]), "R_EURUSD_W60_k1", 1, "IS (A ailesi h=1)", {}),
    ("A4_BTC_W250_k3_h5", V(sig["R_BTC_W250_k3"]), "R_BTC_W250_k3", 5, "IS (A ailesi h=5)", {}),
    ("A5_BTC_W250_k5_h3", V(sig["R_BTC_W250_k5"]), "R_BTC_W250_k5", 3, "IS (A ailesi h=3)", {}),
]
code = vp.v_code
roll_in = lambda h: pd.concat([(code.shift(-j) != code.shift(-j + 1)) for j in range(1, h + 1)], axis=1).any(axis=1)
extreme = ((vp.index >= "2020-03-01") & (vp.index <= "2020-03-31")) | ((vp.index >= "2026-01-01") & (vp.index <= "2026-02-28"))
rob, bts, plc = [], [], []
for lab, x, col, h, sel, extra in cands:
    y = Y[h]; base = split_stats(x, y, h); sgn = np.sign(base["ic_is"])
    r = dict(cand=lab, sel=sel, h=h, n=base["n"], ic=base["ic"], t=base["t"], t_is=base["t_is"], t_oos=base["t_oos"], ic_oos=base["ic_oos"],
             yrs=f'{base["yrs_same_sign"]}/{base["yrs"]}', by_year=base["by_year"], sgn_is=sgn)
    # spot hedef (2016+) ve 1 saat atlamalı spot hedef; pre-2017-03 alt dönem
    xs = sig[col] if not extra else sig[col].where(sig[f"I12F_MACRO3_{extra['cond']}"].abs() > (thr60 if extra["cond"] == "W60" else thr250))
    for nm, yy in [("spot", sig[f"sfwd{h}"]), ("skip1h", sig[f"skip{h}"])]:
        st = split_stats(xs, yy, h); r[f"t_{nm}"] = st["t"]; r[f"ic_{nm}"] = st["ic"]; r[f"t_oos_{nm}"] = st["t_oos"]
        register(AGENT, "R_robust", f"{lab}_{nm}", col, h, st, f"hedef={nm}")
    pre = xs.index < "2017-03-06"
    st = ic(xs[pre], sig[f"skip{h}"][pre], max(h, 5)); r["ic_pre2017"] = st["ic"]; r["t_pre2017"] = st["t"]; r["n_pre2017"] = st["n"]
    if st["n"] >= 30: register(AGENT, "R_robust", f"{lab}_pre2017", col, h, st, "2016-01..2017-03 spot skip hedefi")
    # roll penceresi hariç, uç dönemler hariç, winsorize
    for nm, xx in [("noroll", x.where(~roll_in(h))), ("noextreme", x.where(~extreme)),
                   ("winsor", x.clip(x[x.index <= IS_END].quantile(0.01), x[x.index <= IS_END].quantile(0.99)))]:
        st = split_stats(xx, y, h); r[f"t_{nm}"] = st["t"]; r[f"t_oos_{nm}"] = st["t_oos"]
        register(AGENT, "R_robust", f"{lab}_{nm}", col, h, st, nm)
    pl = placebo_lead(x, vp.v_ret, h); plc.append(dict(cand=lab, **{f"shift{k}": v for k, v in pl.items()}))
    rob.append(r)
    # backtest: her zaman pozisyonda (işaret) ve eşikli (|z|>1); yön = IS IC işareti
    for rule, pos in [("sign", sgn * np.sign(x).fillna(0)), ("thr1", sgn * np.sign(x).where(x.abs() > 1, 0).fillna(0))]:
        if rule == "thr1" and extra:  # koşullu sinyalde zaten seçici; eşik |z|>0.5
            pos = sgn * np.sign(x).where(x.abs() > 0.5, 0).fillna(0)
        res = legs_bt(pos, vp.v_ret.fillna(0), h)
        bts.append(dict(cand=lab, rule=rule, h=h, **flat_bt(res)))
R = pd.DataFrame(rob); R.to_csv(f"{OUT}/robust.csv", index=False)
B = pd.DataFrame(bts); B.to_csv(f"{OUT}/backtests.csv", index=False)
PL = pd.DataFrame(plc); PL.to_csv(f"{OUT}/placebo.csv", index=False)
C = pd.DataFrame(crow); C.to_csv(f"{OUT}/controls.csv", index=False)

# ---------- 3) Erken dönem (2010-01..2017-03) gümüş oranı, Yahoo t-1 sürümü; aynı sürüm 2017+ VİOP ----------
early = []
pre = sig.index < "2017-03-06"
for k in (1, 3, 5):
    for h in (1, 3, 5):
        x = sig[f"GSYD_k{k}"]
        st_e = split_stats(x[pre], sig[f"sfwd{h}"][pre], h)
        register(AGENT, "B_early", f"BE_GSYD_k{k}_h{h}_2010_2017", f"GSYD_k{k}", h, st_e, "Yahoo GC/SI t-1, spot hedef 2010-01..2017-03")
        st_v = split_stats(V(x), Y[h], h)
        register(AGENT, "B_early", f"BE_GSYD_k{k}_h{h}_viop", f"GSYD_k{k}", h, st_v, "Yahoo GC/SI t-1, VİOP hedef 2017+")
        early.append(dict(sig=f"GSYD_k{k}", h=h, ic_2010_17=st_e["ic"], t_2010_17=st_e["t"], n_2010_17=st_e["n"], ic_viop=st_v["ic"], t_viop=st_v["t"],
                          t_is=st_v["t_is"], t_oos=st_v["t_oos"], by_year_early=split_stats(x[pre], sig[f"sfwd{h}"][pre], h)["by_year"]))
E = pd.DataFrame(early); E.to_csv(f"{OUT}/early.csv", index=False)

pd.set_option("display.width", 250)
print(C[["test_id", "ic", "t", "t_is", "t_oos", "yrs_same_sign", "yrs"]].round(3).to_string())
print(pd.DataFrame(part).to_string())
print(R.drop(columns=["by_year"]).round(2).T.to_string())
print(PL.to_string())
cols = ["cand", "rule", "sh_is", "sh_oos", "sh10_oos", "sh_dm_is", "sh_dm_oos", "long_sh_oos", "long_dm_oos", "short_sh_oos", "short_dm_oos", "bh_is", "bh_oos", "turn_full", "expo_full", "long_frac_full"]
print(B[cols].to_string())
print(E.drop(columns=["by_year_early"]).round(3).to_string())
