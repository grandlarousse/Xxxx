"""A3: (i) sepetler ve çok değişkenli öncülük regresyonu (gün-içi hedef), (ii) Brent rejim analizi (yıllık, 250g kayan),
(iii) THYAO<->PGSUS yurt içi lead-lag, (iv) USDTRY / EURUSD kesit karşılaştırması (47 VİOP hissesi içinde sıralama).
Çıktı: res/a3_*.csv + res/a3_summary.txt"""
from h import *
from h import _nwcorr, _corr
import statsmodels.api as sm
from universe import VIOP

EU_AIR = ["LHA.DE", "AF.PA", "IAG.L", "RYA.IR", "EZJ.L", "WIZZ.L", "JET2.L"]
US_AIR = ["DAL", "UAL", "AAL", "LUV", "ALK", "JBLU"]
AIRPORT = ["ADP.PA", "FRA.DE", "AENA.MC", "FHZN.SW"]

def basket(syms):
    X = pd.concat([R(s).where(R(s) != 0) for s in syms], axis=1)
    return X.mean(axis=1, skipna=True).where(X.notna().sum(1) >= 2)

def rolling_resid(y, x, w=250):
    """y - beta_roll*x, beta geçmiş pencereden (look-ahead yok)."""
    df = pd.concat([y.rename("y"), x.rename("x")], axis=1)
    cov = df["y"].rolling(w, min_periods=120).cov(df["x"]); var = df["x"].rolling(w, min_periods=120).var()
    b = (cov / var).shift(1)
    return (df["y"] - b * df["x"])

def signals():
    eu = basket(EU_AIR); us = basket(US_AIR); ap = basket(AIRPORT)
    sx = R("^STOXX").where(R("^STOXX") != 0); sp = R("^GSPC").where(R("^GSPC") != 0)
    out = pd.DataFrame({"EUAIR": eu, "USAIR": us, "AIRPORT": ap, "STOXX": sx, "SPX": sp,
                        "EUAIR_X": rolling_resid(eu, sx), "USAIR_X": rolling_resid(us, sp), "AIRPORT_X": rolling_resid(ap, sx),
                        "TUR": R("TUR").where(R("TUR") != 0), "XU100": R("XU100"), "BZ": R("BZ=F").where(R("BZ=F") != 0),
                        "VIX": R("^VIX").where(R("^VIX") != 0), "JETS": R("JETS").where(R("JETS") != 0)})
    return out

def ols_nw(y, X, lags=5):
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    if len(df) < 100: return None
    Z = (df - df.mean()) / df.std()
    m = sm.OLS(Z["y"], sm.add_constant(Z.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
    return m, len(df)

if __name__ == "__main__":
    SG = signals(); SG.to_parquet(RES + "/signals.parquet")
    L = []
    txt = []
    # (i) çok değişkenli: intra_t ~ sinyaller_{t-1}
    specs = {"M1": ["EUAIR_X", "USAIR_X", "STOXX", "SPX", "TUR", "XU100", "BZ"],
             "M2": ["EUAIR", "USAIR", "TUR", "XU100"],
             "M3": ["EUAIR_X", "USAIR_X", "STOXX", "SPX", "TUR", "XU100", "BZ", "OWN", "AIRPORT_X"]}
    for st in STOCKS:
        dd = D(st)
        for nm, cols in specs.items():
            X = SG.copy(); X["OWN"] = R(st)
            X = X[cols].shift(1)
            for per, a, b in [("ALL", "2015-06-01", "2027"), ("IS", "2015-06-01", "2021-01-01"), ("OOS", "2021-01-01", "2027")]:
                y = dd["intra"]; y = y[(y.index >= a) & (y.index < b)]
                r = ols_nw(y, X)
                if r is None: continue
                m, n = r
                for c in cols:
                    L.append({"stock": st, "spec": nm, "period": per, "var": c, "coef_std": m.params[c], "t": m.tvalues[c], "n": n, "r2": m.rsquared})
    MV = pd.DataFrame(L); MV.to_csv(RES + "/a3_multivar.csv", index=False)
    piv = MV[MV.spec == "M1"].pivot_table(index=["stock", "var"], columns="period", values="t").round(2)
    txt.append("== M1 çok değişkenli intra_t ~ X_{t-1} (NW t) ==\n" + piv.to_string())
    piv = MV[MV.spec == "M3"].pivot_table(index=["stock", "var"], columns="period", values="t").round(2)
    txt.append("== M3 (+OWN, AIRPORT_X) ==\n" + piv.to_string())
    # gap için de aynı
    L2 = []
    for st in STOCKS:
        X = SG[specs["M1"]].shift(1)
        r = ols_nw(D(st)["gap"][D(st).index >= "2015-06-01"], X)
        m, n = r
        for c in specs["M1"]: L2.append({"stock": st, "var": c, "coef_std": m.params[c], "t": m.tvalues[c], "r2": m.rsquared})
    txt.append("== M1 gap_t ~ X_{t-1} ==\n" + pd.DataFrame(L2).pivot_table(index="var", columns="stock", values="t").round(2).to_string())
    # (ii) Brent rejim
    rows = []
    m = R("XU100")
    for st in STOCKS:
        a = R(st); b = SG["BZ"]
        df = pd.concat([a.rename("a"), b.rename("b"), m.rename("m")], axis=1).dropna()
        for y, g in df.groupby(df.index.year):
            if len(g) < 60: continue
            pc, _ = ll.partial_corr(g["a"], g["b"], [g["m"]])
            rows.append({"stock": st, "year": y, "corr": g["a"].corr(g["b"]), "pc": pc, "n": len(g)})
        # 2026 alt dönemler
        for lab, a0, b0 in [("2026_Q1_prewar", "2026-01-01", "2026-03-01"), ("2026_war_Mar-Oct", "2026-03-01", "2026-11-01"), ("2025H2", "2025-07-01", "2026-01-01")]:
            g = df[(df.index >= a0) & (df.index < b0)]
            if len(g) > 20:
                pc, _ = ll.partial_corr(g["a"], g["b"], [g["m"]])
                rows.append({"stock": st, "year": lab, "corr": g["a"].corr(g["b"]), "pc": pc, "n": len(g)})
    BR = pd.DataFrame(rows); BR.to_csv(RES + "/a3_brent_regime.csv", index=False)
    txt.append("== Brent senkron corr / kısmi corr yıllara göre ==\n" + BR.pivot_table(index="year", columns="stock", values=["corr", "pc"]).round(2).to_string())
    # Brent'in XU100 ile ilişkisi (rejim: petrol = Türkiye risk faktörü mü?)
    xb = pd.concat([m.rename("m"), SG["BZ"].rename("b")], axis=1).dropna()
    txt.append("== corr(XU100, Brent) yıllara göre ==\n" + xb.groupby(xb.index.year).apply(lambda g: g["m"].corr(g["b"])).round(2).to_string())
    # 250g kayan
    rc = {st: ll.rolling_corr(R(st), SG["BZ"], 250) for st in STOCKS}
    pd.DataFrame(rc).to_csv(RES + "/a3_brent_roll250.csv")
    # (iii) THYAO <-> PGSUS
    th = D("THYAO"); pg = D("PGSUS"); tv = D("TAVHL")
    rows = []
    def add(lab, y, x, lags=5):
        c, t, n = _nwcorr(y, x, lags=lags); rows.append({"test": lab, "corr": c, "t": t, "n": n})
    for (A_, B_, an, bn) in [(th, pg, "THYAO", "PGSUS"), (pg, th, "PGSUS", "THYAO"), (th, tv, "THYAO", "TAVHL"), (tv, th, "TAVHL", "THYAO"), (pg, tv, "PGSUS", "TAVHL"), (tv, pg, "TAVHL", "PGSUS")]:
        add(f"{an}_cc(t-1) -> {bn}_cc(t)", B_["cc"], A_["cc"].shift(1))
        add(f"{an}_cc(t-1) -> {bn}_gap(t)", B_["gap"], A_["cc"].shift(1))
        add(f"{an}_cc(t-1) -> {bn}_intra(t)", B_["intra"], A_["cc"].shift(1))
        add(f"{an}_intra(t-1) -> {bn}_intra(t)", B_["intra"], A_["intra"].shift(1))
        sp = (A_["cc"] - B_["cc"]).shift(1)
        add(f"spread({an}-{bn})_cc(t-1) -> {bn}_intra(t)", B_["intra"], sp)
        add(f"spread({an}-{bn})_cc(t-1) -> {bn}_cc t..t+4", sum(B_["cc"].shift(-k) for k in range(0, 5)), sp, lags=10)
        for per, a0, b0 in [("IS", "2014", "2021-01-01"), ("OOS", "2021-01-01", "2027")]:
            c, t, n = _nwcorr(B_["intra"], A_["cc"].shift(1), start=a0, end=b0); rows.append({"test": f"{an}_cc(t-1) -> {bn}_intra(t) [{per}]", "corr": c, "t": t, "n": n})
    # kısmi: PGSUS intra ~ THYAO_cc(t-1) + PGSUS_cc(t-1) + XU100(t-1) + EUAIR_X + USAIR_X + TUR
    X = pd.concat([th["cc"].rename("THY"), pg["cc"].rename("PGS"), R("XU100").rename("XU"), SG["EUAIR_X"], SG["USAIR_X"], SG["TUR"]], axis=1).shift(1)
    r_ = ols_nw(pg["intra"][pg.index >= "2015-06-01"], X)
    txt.append("== PGSUS intra_t ~ [THYAO_cc, PGSUS_cc, XU100, EUAIR_X, USAIR_X, TUR]_{t-1} (std coef, NW t) ==\n" + pd.DataFrame({"coef": r_[0].params, "t": r_[0].tvalues}).round(3).to_string())
    X2 = pd.concat([pg["cc"].rename("PGS"), th["cc"].rename("THY"), R("XU100").rename("XU"), SG["EUAIR_X"], SG["USAIR_X"], SG["TUR"]], axis=1).shift(1)
    r_ = ols_nw(th["intra"][th.index >= "2015-06-01"], X2)
    txt.append("== THYAO intra_t ~ [...]_{t-1} ==\n" + pd.DataFrame({"coef": r_[0].params, "t": r_[0].tvalues}).round(3).to_string())
    TP = pd.DataFrame(rows); TP.to_csv(RES + "/a3_thy_pgs.csv", index=False)
    txt.append("== Yurt içi lead-lag ==\n" + TP.round(3).to_string(index=False))
    # (iv) USDTRY ve EURUSD kesit sıralaması
    rows = []
    fx = R("TRY=X").where(R("TRY=X") != 0); eu = R("EURUSD=X").where(R("EURUSD=X") != 0)
    for s in VIOP:
        try:
            a = R(s)
        except Exception:
            continue
        a = a[a.index >= "2014-01-01"]
        p1, n = ll.partial_corr(a, fx, [m]); p2, _ = ll.partial_corr(a, eu, [m, fx])
        p1o, _ = ll.partial_corr(a[a.index >= SPLIT], fx, [m])
        df = pd.concat([a.rename("a"), fx.rename("f"), m.rename("m")], axis=1).dropna()
        Z = sm.add_constant(df[["m", "f"]]); bb = sm.OLS(df["a"], Z).fit().params
        rows.append({"sym": s, "pc_usdtry|xu100": p1, "pc_usdtry_OOS": p1o, "beta_usdtry|xu100": bb["f"], "pc_eurusd|xu100,usdtry": p2, "n": n})
    FX = pd.DataFrame(rows).sort_values("pc_usdtry|xu100", ascending=False); FX["rank"] = range(1, len(FX) + 1)
    FX.to_csv(RES + "/a3_fx_cross.csv", index=False)
    txt.append("== USDTRY kısmi corr | XU100 kesit (2014+), ilk 10 ve havacılık ==\n" + FX.head(10).round(3).to_string(index=False) + "\n...\n" + FX[FX.sym.isin(STOCKS)].round(3).to_string(index=False))
    FE = FX.sort_values("pc_eurusd|xu100,usdtry", ascending=False); FE["rank_eur"] = range(1, len(FE) + 1)
    txt.append("== EURUSD kısmi corr | XU100,USDTRY: ilk 8 + havacılık ==\n" + FE.head(8)[["sym", "pc_eurusd|xu100,usdtry", "rank_eur"]].round(3).to_string(index=False) + "\n" + FE[FE.sym.isin(STOCKS)][["sym", "pc_eurusd|xu100,usdtry", "rank_eur"]].round(3).to_string(index=False))
    open(RES + "/a3_summary.txt", "w").write("\n\n".join(txt))
    print("ok")
