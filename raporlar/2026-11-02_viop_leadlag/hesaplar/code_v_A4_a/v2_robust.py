"""v2: Sağlamlık — eşik, tanım (beta penceresi, ham sepet, tek bacak, üye-dışarıda), hedge'li hedef, sürekli regresyon + kontroller,
mekanizma (sürücü momentumu?), uzun/kısa, dönem/yıl, dairesel kaydırma null'u. Çıktı: res/v2_*.csv, v2.log"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_a")
from vcore import *
pd.set_option("display.width", 250)
ST = ["THYAO.IS", "PGSUS.IS", "TAVHL.IS"]
D = {s: bist_day(s) for s in ST + ["XU100.IS", "XU030.IS"]}
SA = pd.read_parquet(OUTD + "/v1_signals_A.parquet")

def ols_nw(y, X, lags=5):
    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    Z = (df - df.mean()) / df.std()
    Xm = np.column_stack([np.ones(len(Z)), Z.drop(columns="y").values]); yv = Z.y.values
    b = np.linalg.lstsq(Xm, yv, rcond=None)[0]; e = yv - Xm @ b
    n = len(yv); XtX_inv = np.linalg.inv(Xm.T @ Xm)
    u = Xm * e[:, None]; Sg = u.T @ u
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1); G = u[L:].T @ u[:-L]; Sg += w * (G + G.T)
    V = XtX_inv @ Sg @ XtX_inv
    return pd.DataFrame({"coef": b, "t": b / np.sqrt(np.diag(V))}, index=["const"] + list(Z.drop(columns="y").columns)), n

def summ(o):
    return {f"{p}_{k}": o[p].get(k, np.nan) for p in ["IS", "OOS"] for k in ["n", "bps", "t_nw"]}

if __name__ == "__main__":
    rows = []
    # 1) Eşik duyarlılığı
    for thr in [0.0, 0.5, 1.0, 1.5, 2.0]:
        for s in ST:
            o, _, _ = bt(SA.AIR.shift(1), D[s].intra, 8, thr); rows.append({"grp": "thr", "var": f"AIR thr={thr}", "target": s, **summ(o)})
    # 2) Tanım varyantları
    defs = {}
    defs["AIR_raw(artıksız)"] = SA.AIR_raw
    for w in [120, 500]:
        x = build_signals(drv_ret_cal, w_beta=w); defs[f"AIR beta{w}"] = x.AIR
    defs["EU_only"] = SA.zEU; defs["US_only"] = SA.zUS
    defs["AIR eşit ağırlık z ortalama (zEU+zUS)/2"] = (SA.zEU + SA.zUS) / 2
    # z'siz: artık getirilerin toplamı (yüzde) -> sign, eşik 0
    defs["EU_X+US_X ham (thr0)"] = (SA.EU_X + SA.US_X)
    # üye-dışarıda (leave-one-out)
    for m in EU_AIR:
        e2 = [x for x in EU_AIR if x != m]; x = build_signals(drv_ret_cal, eu=e2); defs[f"LOO -{m}"] = x.AIR
    for m in US_AIR:
        u2 = [x for x in US_AIR if x != m]; x = build_signals(drv_ret_cal, us=u2); defs[f"LOO -{m}"] = x.AIR
    # sadece 'büyük' üyeler (LHA, AF, IAG, RYA / DAL, UAL, AAL)
    x = build_signals(drv_ret_cal, eu=["LHA.DE", "AF.PA", "IAG.L", "RYA.IR"], us=["DAL", "UAL", "AAL"]); defs["büyük üyeler"] = x.AIR
    for nm, sig in defs.items():
        thr = 0.0 if "thr0" in nm else (0.5 if nm in ["EU_only", "US_only", "AIR eşit ağırlık z ortalama (zEU+zUS)/2"] else 1.0)
        for s in ST:
            o, _, _ = bt(sig.shift(1), D[s].intra, 8, thr); rows.append({"grp": "def", "var": f"{nm} thr={thr}", "target": s, **summ(o)})
    R = pd.DataFrame(rows); R.to_csv(OUTD + "/v2_variants.csv", index=False)
    print("=== Eşik ve tanım varyantları (8 bps net) ===")
    print(R.set_index(["grp", "var", "target"]).round(2).to_string())
    # özet: varyantlar arasında OOS bps dağılımı
    print("\nLOO dağılımı (OOS bps net): ", R[R["var"].str.startswith("LOO")].groupby("target").OOS_bps.describe().round(1).to_string())

    # 3) Hedge'li hedef: intra - beta*XU030 intra (beta 250g kayan, shift1), maliyet 16 (iki bacak)
    rows = []
    xi = D["XU030.IS"].intra
    for s in ST:
        y = D[s].intra; df = pd.concat([y.rename("y"), xi.rename("x")], axis=1).dropna()
        b = (df.y.rolling(250, min_periods=120).cov(df.x) / df.x.rolling(250, min_periods=120).var()).shift(1)
        hed = (df.y - b * df.x)
        for cost in [0, 16, 24]:
            o, _, _ = bt(SA.AIR.shift(1), hed, cost, 1.0); rows.append({"var": f"AIR -> hedged intra cost{cost}", "target": s, **summ(o)})
    # 4) Covid hariç (2020-02..2021-06), ve alt dönemler
    for s in ST:
        sig = SA.AIR.shift(1); y = D[s].intra
        m = ~((y.index >= "2020-02-01") & (y.index < "2021-07-01"))
        o, _, _ = bt(sig, y[m], 8, 1.0); rows.append({"var": "AIR, COVID 2020-02..2021-06 hariç", "target": s, **summ(o)})
        for a, b_ in [("2014", "2017-07-01"), ("2017-07-01", "2021-01-01"), ("2021-01-01", "2024-01-01"), ("2024-01-01", "2027")]:
            o, _, _ = bt(sig, y, 8, 1.0, start=a, end=b_); d = o["ALL"]
            rows.append({"var": f"AIR alt-dönem {a}..{b_}", "target": s, "IS_n": d.get("n"), "IS_bps": d.get("bps"), "IS_t_nw": d.get("t_nw")})
    H = pd.DataFrame(rows); H.to_csv(OUTD + "/v2_hedge_periods.csv", index=False)
    print("\n=== Hedge'li hedef / COVID hariç / alt dönemler (alt dönemde IS_* = o dönemin tümü) ===")
    print(H.set_index(["var", "target"]).round(2).to_string())

    # 5) Uzun / kısa / düz günler (brüt gün-içi ort.), ve demeaned spread
    rows = []
    for s in ST + ["XU100.IS"]:
        df = pd.concat([SA.AIR.shift(1).rename("s"), D[s].intra.rename("y")], axis=1).dropna()
        for per, m in [("IS", df.index < SPLIT), ("OOS", df.index >= SPLIT)]:
            g = df[m]
            for side, k in [("long", g.s > 1), ("short", g.s < -1), ("flat", g.s.abs() <= 1)]:
                x = g.y[k]; rows.append({"target": s, "per": per, "side": side, "n": len(x), "mean_bps": 1e4 * x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x))})
    LS = pd.DataFrame(rows); print("\n=== Uzun/kısa/düz brüt gün-içi ortalama ===\n" + LS.round(2).to_string(index=False))

    # 6) Sürekli regresyon: intra_t ~ AIR_{t-1} + kontroller (std katsayı, NW t)
    print("\n=== Sürekli regresyon (std katsayı, NW t) ===")
    rows = []
    for s in ST:
        dd = D[s]; xu = D["XU100.IS"]
        base = pd.DataFrame({"AIR_l1": SA.AIR.shift(1)})
        specs = {
            "S0: AIR": base,
            "S1: +own cc(t-1), XU100 cc(t-1)": base.assign(own_cc_l1=dd.cc.shift(1), xu_cc_l1=xu.cc.shift(1)),
            "S2: S1 + own gap(t), XU100 gap(t) [açılışta bilinir]": base.assign(own_cc_l1=dd.cc.shift(1), xu_cc_l1=xu.cc.shift(1), own_gap=dd.gap, xu_gap=xu.gap),
            "S3: S2 + TUR(t-1)": base.assign(own_cc_l1=dd.cc.shift(1), xu_cc_l1=xu.cc.shift(1), own_gap=dd.gap, xu_gap=xu.gap, TUR_l1=SA.TUR.shift(1)),
            "M1: S2 + XU100 intra(t) [eşzamanlı, işlenemez: hisseye özgü mü?]": base.assign(own_cc_l1=dd.cc.shift(1), xu_cc_l1=xu.cc.shift(1), own_gap=dd.gap, xu_gap=xu.gap, xu_intra=xu.intra),
            "M2: S2 + EU_X(t), US_X(t) [eşzamanlı sürücü: mekanizma=sürücü momentumu mu?]": base.assign(own_cc_l1=dd.cc.shift(1), xu_cc_l1=xu.cc.shift(1), own_gap=dd.gap, xu_gap=xu.gap, EU_X_t=SA.EU_X, US_X_t=SA.US_X),
        }
        for nm, X in specs.items():
            for per, a, b_ in [("ALL", "2014", "2027"), ("IS", "2014", "2021-01-01"), ("OOS", "2021-01-01", "2027")]:
                y = dd.intra[(dd.intra.index >= a) & (dd.intra.index < b_)]
                r, n = ols_nw(y, X)
                rows.append({"target": s, "spec": nm, "per": per, "n": n, "AIR_coef": r.loc["AIR_l1", "coef"], "AIR_t": r.loc["AIR_l1", "t"],
                             **({"TUR_t": r.loc["TUR_l1", "t"]} if "TUR_l1" in r.index else {}),
                             **({"EU_X_t_t": r.loc["EU_X_t", "t"], "US_X_t_t": r.loc["US_X_t", "t"]} if "EU_X_t" in r.index else {}),
                             **({"own_gap_t": r.loc["own_gap", "t"]} if "own_gap" in r.index else {})})
    RG = pd.DataFrame(rows); RG.to_csv(OUTD + "/v2_regress.csv", index=False)
    print(RG.round(3).to_string(index=False))
    # sürücü otokorelasyonu
    print("\n=== Sürücü otokorelasyonu: corr(AIR_{t-1}, EU_X_t / US_X_t) ===")
    for c in ["EU_X", "US_X"]:
        j = pd.concat([SA.AIR.shift(1), SA[c]], axis=1).dropna(); print(c, round(j.iloc[:, 0].corr(j.iloc[:, 1]), 4), len(j))
    j = pd.concat([SA.EU_X.shift(1), SA.EU_X], axis=1).dropna(); print("EU_X AR1", round(j.iloc[:, 0].corr(j.iloc[:, 1]), 4))
    j = pd.concat([SA.US_X.shift(1), SA.US_X], axis=1).dropna(); print("US_X AR1", round(j.iloc[:, 0].corr(j.iloc[:, 1]), 4))

    # 7) Dairesel kaydırma null'u (sinyal serisini 60..N-60 gün kaydır; otokorelasyon korunur). OOS ve ALL bps dağılımı.
    print("\n=== Dairesel kaydırma null'u (1000 kaydırma) ===")
    rng = np.random.default_rng(7)
    for s in ST:
        df = pd.concat([SA.AIR.shift(1).rename("s"), D[s].intra.rename("y")], axis=1).dropna()
        sv = df.s.values; yv = df.y.values; N = len(sv); oos = df.index >= SPLIT
        def stat(sig):
            pos = np.sign(sig) * (np.abs(sig) > 1); a = pos != 0
            p = pos * yv - 8e-4 * np.abs(pos)
            return 1e4 * p[a].mean(), 1e4 * p[a & oos].mean()
        obs = stat(sv)
        sims = np.array([stat(np.roll(sv, k)) for k in rng.integers(60, N - 60, 1000)])
        print(s, "gözlenen ALL/OOS bps:", np.round(obs, 2), " null %95/%99 ALL:", np.round(np.percentile(sims[:, 0], [95, 99]), 2),
              " p(ALL)=", round(float((sims[:, 0] >= obs[0]).mean()), 4), " p(OOS)=", round(float((sims[:, 1] >= obs[1]).mean()), 4))
    print("ok")
