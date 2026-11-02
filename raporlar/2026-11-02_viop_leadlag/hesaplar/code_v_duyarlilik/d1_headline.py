"""v_duyarlilik ana hesap: başlık rakamlarını ll v1..v4 temizliğiyle yan yana hesaplar.
Çıktı: res/d1_long.csv (madde, hisse, sürücü, metrik, dönem, v1..v4), res/d1_beta.csv, res/d1_fade_stock.csv, res/d1_es_stock.csv
Çalıştır: cd code_v_duyarlilik && nice -n 10 python3 d1_headline.py
"""
import vers, numpy as np, pandas as pd, statsmodels.api as sm
L = vers.L; VERS = ["v1", "v2", "v3", "v4"]; STK = vers.VIOP
FULL0 = pd.Timestamp("2010-01-01"); IS0, IS1, OOS0 = pd.Timestamp("2014-01-01"), pd.Timestamp("2020-12-31"), pd.Timestamp("2021-01-01")
PAIRS = [("THYAO.IS", "LHA.DE"), ("PGSUS.IS", "EZJ.L"), ("TUPRS.IS", "CRAK"), ("TUPRS.IS", "BZ=F"), ("TRALT.IS", "GC=F"), ("EREGL.IS", "MT.AS"),
         ("TCELL.IS", "TKC"), ("AEFES.IS", "CCOLA.IS"), ("SAHOL.IS", "AKBNK.IS"), ("EREGL.IS", "ISDMR.IS")]
BANKS = ["XBANK.IS", "AKBNK.IS", "GARAN.IS", "YKBNK.IS", "ISCTR.IS", "HALKB.IS", "VAKBN.IS", "TSKB.IS"]
SASA_PEERS = ["XU100.IS", "HEKTS.IS", "KMPUR.IS", "SMRTG.IS", "PETKM.IS", "AKSA.IS", "KORDS.IS", "BZ=F", "CL=F", "IVL.BK", "1326.TW", "CT=F", "ES=F", "TRY=X"]
SYMS = sorted(set([s + ".IS" for s in STK] + ["XU100.IS", "XU030.IS"] + [p for pr in PAIRS for p in pr] + BANKS + SASA_PEERS))
LONG = []
def rec(item, stock, driver, metric, period, vals, note=""):
    LONG.append(dict(item=item, stock=stock, driver=driver, metric=metric, period=period, **{v: vals.get(v, np.nan) for v in VERS}, note=note))

def win(df, period, last):
    if period == "full": return df[df.index >= FULL0]
    if period == "3y": return df[df.index >= last - pd.DateOffset(years=3)]
    if period == "1y": return df[df.index >= last - pd.DateOffset(years=1)]
    if period == "IS": return df[(df.index >= IS0) & (df.index <= IS1)]
    if period == "OOS": return df[df.index >= OOS0]
    raise ValueError(period)
def pc(df):  # df: a, b, m
    if len(df) < 30: return np.nan
    C = np.column_stack([np.ones(len(df)), df["m"].values])
    ra = df["a"].values - C @ np.linalg.lstsq(C, df["a"].values, rcond=None)[0]
    rb = df["b"].values - C @ np.linalg.lstsq(C, df["b"].values, rcond=None)[0]
    return float(np.corrcoef(ra, rb)[0, 1])
def beta(df):
    if len(df) < 30: return np.nan
    return float(np.cov(df["a"], df["b"])[0, 1] / np.var(df["b"], ddof=1))
def nw_mean(x, lags=5):
    x = pd.Series(x).dropna()
    if len(x) < 20: return np.nan, np.nan, len(x)
    m = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags}); return float(m.params[0]), float(m.tvalues[0]), len(x)

# ---------------- veri: her sürüm için getiriler ve ayrıştırmalar
R = {v: {} for v in VERS}; D = {v: {} for v in VERS}
for v in VERS:
    for s in SYMS: R[v][s] = L[v].ret(s)
    for s in [x + ".IS" for x in STK] + ["XU030.IS", "XU100.IS"]: D[v][s] = L[v].decomp(s)
LAST = R["v4"]["XU100.IS"].dropna().index.max()
print("son tarih", LAST.date())

# ---------------- (1a) 47 hisse XU100 betası
brow = []
for s in STK:
    for per in ["full", "3y", "1y", "IS", "OOS"]:
        bv = {}; cv = {}; nv = {}
        for v in VERS:
            df = pd.concat([R[v][s + ".IS"].rename("a"), R[v]["XU100.IS"].rename("b")], axis=1).dropna(); df = win(df, per, LAST)
            bv[v] = beta(df); cv[v] = df["a"].corr(df["b"]) if len(df) > 30 else np.nan; nv[v] = len(df)
        rec("1_beta", s, "XU100", "beta", per, bv); rec("1_beta", s, "XU100", "corr", per, cv); rec("1_beta", s, "XU100", "n", per, nv)
        brow.append(dict(stock=s, period=per, **{f"beta_{v}": bv[v] for v in VERS}, **{f"corr_{v}": cv[v] for v in VERS}, **{f"n_{v}": nv[v] for v in VERS}))
pd.DataFrame(brow).to_csv(vers.RES + "/d1_beta.csv", index=False)

# ---------------- (1b) çiftler: corr, kısmi korelasyon (XU100), beta, yıl-işaret, mekanik etiket
def label(m):
    big = (abs(m["corr_full"]) >= 0.30) or (abs(m["pc_full"]) >= 0.15)
    sig = lambda x, n: (not np.isnan(x)) and abs(x) * np.sqrt(max(n - 3, 1)) >= 2
    s0 = np.sign(m["pc_full"])
    same = (np.sign(m["pc_IS"]) == s0) and (np.sign(m["pc_OOS"]) == s0)
    if big and m["yr_share_pc"] >= 0.75 and same and sig(m["pc_IS"], m["n_IS"]) and sig(m["pc_OOS"], m["n_OOS"]): return "YÜKSEK"
    if sig(m["pc_full"], m["n_full"]) and np.sign(m["pc_OOS"]) == s0: return "ORTA"
    return "DÜŞÜK"
prow = []
for a, b in PAIRS:
    M = {}
    for v in VERS:
        df = pd.concat([R[v][a].rename("a"), R[v][b].rename("b"), R[v]["XU100.IS"].rename("m")], axis=1).dropna()
        m = {}
        for per in ["full", "3y", "1y", "IS", "OOS"]:
            w = win(df, per, LAST); m[f"corr_{per}"] = w["a"].corr(w["b"]) if len(w) > 30 else np.nan; m[f"pc_{per}"] = pc(w); m[f"n_{per}"] = len(w)
            m[f"beta_{per}"] = beta(w[["a", "b"]])
        w = win(df, "full", LAST); yrs = w.groupby(w.index.year)
        ypc = pd.Series({y: pc(g) for y, g in yrs if len(g) > 60})
        yc = pd.Series({y: g["a"].corr(g["b"]) for y, g in yrs if len(g) > 60})
        m["yr_share_pc"] = float((np.sign(ypc) == np.sign(m["pc_full"])).mean()); m["yr_share_corr"] = float((np.sign(yc) == np.sign(m["corr_full"])).mean())
        m["label_mech"] = label(m); M[v] = m
    for k in M["v4"]:
        if k == "label_mech": continue
        per = k.split("_")[-1] if k.split("_")[-1] in ["full", "3y", "1y", "IS", "OOS"] else "full"
        rec("1_pair", a, b, k.rsplit("_", 1)[0] if per != "full" or k.endswith("_full") else k, per, {v: M[v][k] for v in VERS})
    rec("1_pair", a, b, "label_mech", "full", {v: M[v]["label_mech"] for v in VERS})
    prow.append(dict(stock=a, driver=b, **{f"{k}_{v}": M[v][k] for v in VERS for k in M[v]}))
pd.DataFrame(prow).to_csv(vers.RES + "/d1_pairs.csv", index=False)

# ---------------- (2) bankalar – USDTRY kısmi korelasyonu
for bk in BANKS:
    for per in ["full", "IS", "OOS", "1y"]:
        vals = {}; cvals = {}; nv = {}
        for v in VERS:
            df = pd.concat([R[v][bk].rename("a"), R[v]["TRY=X"].rename("b"), R[v]["XU100.IS"].rename("m")], axis=1).dropna(); w = win(df, per, LAST)
            vals[v] = pc(w); cvals[v] = w["a"].corr(w["b"]) if len(w) > 30 else np.nan; nv[v] = len(w)
        rec("2_bank_usdtry", bk, "TRY=X", "pc_xu100", per, vals); rec("2_bank_usdtry", bk, "TRY=X", "corr", per, cvals); rec("2_bank_usdtry", bk, "TRY=X", "n", per, nv)

# ---------------- (3) ES=F t-1 -> gap / gün-içi
erow = []
for v in VERS:
    es1 = R[v]["ES=F"].shift(1).rename("es1")  # BIST takviminde bir önceki gün
    for s in [x + ".IS" for x in STK] + ["XU030.IS"]:
        d = D[v][s]
        for col in ["gap", "intra", "cc"]:
            df = pd.concat([d[col].rename("y"), es1], axis=1).dropna()
            for per in ["IS", "OOS"]:
                w = win(df, per, LAST)
                erow.append(dict(ver=v, stock=s, col=col, period=per, corr=w["y"].corr(w["es1"]) if len(w) > 60 else np.nan, n=len(w)))
E = pd.DataFrame(erow); E.to_csv(vers.RES + "/d1_es_stock.csv", index=False)
E47 = E[E.stock != "XU030.IS"]
for col in ["gap", "intra", "cc"]:
    for per in ["IS", "OOS"]:
        x = E47[(E47.col == col) & (E47.period == per)]
        rec("3_es_lag1", "47 medyan", "ES=F(t-1)", f"corr_{col}", per, x.groupby("ver")["corr"].median().to_dict())
        rec("3_es_lag1", "47 pozitif payı", "ES=F(t-1)", f"share_pos_{col}", per, x.groupby("ver")["corr"].apply(lambda c: float((c > 0).mean())).to_dict())
        y = E[(E.stock == "XU030.IS") & (E.col == col) & (E.period == per)].set_index("ver")["corr"].to_dict()
        rec("3_es_lag1", "XU030", "ES=F(t-1)", f"corr_{col}", per, y)
for s in ["SASA.IS"]:
    for col in ["gap", "intra"]:
        for per in ["IS", "OOS"]:
            x = E[(E.stock == s) & (E.col == col) & (E.period == per)].set_index("ver")["corr"].to_dict(); rec("5_sasa", s, "ES=F(t-1)", f"corr_{col}", per, x)

# ---------------- (4) |gap|>%1 fade, açılış girişi (E0): pos=-sign(gap), getiri=intra (log c/o)
LQ = pd.read_csv(vers.OUT + "/code_y_gunici_y/res/a0_liq.csv").set_index("stock")
liquid = [s for s in LQ.index[LQ["liq_rank"] <= 23]]; illiq = [s for s in LQ.index[LQ["liq_rank"] > 23]]
frow = []
for v in VERS:
    gaps = pd.DataFrame({s: D[v][s + ".IS"]["gap"] for s in STK}); gaps = gaps[gaps.index >= IS0]
    intra = pd.DataFrame({s: D[v][s + ".IS"]["intra"] for s in STK}).reindex(gaps.index)
    pos = -np.sign(gaps).where(gaps.abs() > 0.01, 0.0)
    g = (pos * intra).where((pos != 0) & intra.notna())
    for s in STK:
        for per in ["IS", "OOS"]:
            x = win(g[[s]], per, LAST)[s].dropna(); m, t, n = nw_mean(x)
            frow.append(dict(ver=v, stock=s, period=per, mean_bps=1e4 * m if n >= 15 else np.nan, t=t, n=n))
    for uni, cols in [("47", STK), ("likit23", liquid), ("illikit24", illiq)]:
        pp = g[cols].mean(axis=1)
        for per in ["IS", "OOS"]:
            x = win(pp.to_frame("p"), per, LAST)["p"].dropna(); m, t, n = nw_mean(x)
            ntr = int(win(g[cols], per, LAST).notna().sum().sum())
            rec("4_gapfade_E0", f"portföy {uni}", "own gap>%1", "mean_bps", per, {v: 1e4 * m}) if False else None
            frow.append(dict(ver=v, stock=f"PORT_{uni}", period=per, mean_bps=1e4 * m, t=t, n=ntr, n_days=n))
F = pd.DataFrame(frow); F.to_csv(vers.RES + "/d1_fade_stock.csv", index=False)
for per in ["IS", "OOS"]:
    x = F[(~F.stock.str.startswith("PORT")) & (F.period == per)]
    rec("4_gapfade_E0", "47 medyan", "own |gap|>%1", "mean_bps_gross", per, x.groupby("ver")["mean_bps"].median().to_dict())
    rec("4_gapfade_E0", "47 OOS>0 payı", "own |gap|>%1", "share_pos", per, x.groupby("ver")["mean_bps"].apply(lambda c: float((c > 0).mean())).to_dict())
    rec("4_gapfade_E0", "47 |t|>=2 sayısı", "own |gap|>%1", "n_t2", per, x.groupby("ver")["t"].apply(lambda c: int((c >= 2).sum())).to_dict())
    rec("4_gapfade_E0", "47 işlem sayısı", "own |gap|>%1", "n_trades", per, x.groupby("ver")["n"].sum().to_dict())
    for uni in ["47", "likit23", "illikit24"]:
        y = F[(F.stock == f"PORT_{uni}") & (F.period == per)].set_index("ver")
        rec("4_gapfade_E0", f"portföy {uni}", "own |gap|>%1", "mean_bps_gross", per, y["mean_bps"].to_dict())
        rec("4_gapfade_E0", f"portföy {uni}", "own |gap|>%1", "t_nw", per, y["t"].to_dict())
        rec("4_gapfade_E0", f"portföy {uni}", "own |gap|>%1", "net8_bps", per, (y["mean_bps"] - 8).to_dict())
for per in ["IS", "OOS"]:
    for s in ["SASA", "CIMSA", "OYAKC", "TRMET", "TRALT", "VESTL", "DOHOL"]:
        y = F[(F.stock == s) & (F.period == per)].set_index("ver")
        rec("4_gapfade_E0" if s != "SASA" else "5_sasa", s + ".IS", "own |gap|>%1", "mean_bps_gross", per, y["mean_bps"].to_dict())
        rec("4_gapfade_E0" if s != "SASA" else "5_sasa", s + ".IS", "own |gap|>%1", "n_trades", per, y["n"].to_dict())

# ---------------- (5) SASA: beta, korelasyonlar (tam/3y/1y), kısmi korelasyon, sıfır getiri günleri
for b in SASA_PEERS:
    for per in ["full", "3y", "1y"]:
        cv, pv, bv, nv = {}, {}, {}, {}
        for v in VERS:
            df = pd.concat([R[v]["SASA.IS"].rename("a"), R[v][b].rename("b"), R[v]["XU100.IS"].rename("m")], axis=1).dropna(); w = win(df, per, LAST)
            cv[v] = w["a"].corr(w["b"]) if len(w) > 30 else np.nan; pv[v] = pc(w) if b != "XU100.IS" else np.nan; bv[v] = beta(w[["a", "b"]]); nv[v] = len(w)
        rec("5_sasa", "SASA.IS", b, "corr", per, cv); rec("5_sasa", "SASA.IS", b, "beta", per, bv); rec("5_sasa", "SASA.IS", b, "n", per, nv)
        if b != "XU100.IS": rec("5_sasa", "SASA.IS", b, "pc_xu100", per, pv)
for per in ["1y", "3y"]:
    z = {}; nn = {}; sd = {}
    for v in VERS:
        w = win(R[v]["SASA.IS"].to_frame("a"), per, LAST)["a"]; z[v] = int((w == 0).sum()); nn[v] = int(w.notna().sum()); sd[v] = float(w.std() * np.sqrt(252))
    rec("5_sasa", "SASA.IS", "-", "zero_return_days", per, z); rec("5_sasa", "SASA.IS", "-", "n_valid", per, nn); rec("5_sasa", "SASA.IS", "-", "ann_vol", per, sd)
    w = {v: int(win(D[v]["SASA.IS"]["gap"].to_frame("g"), per, LAST)["g"].notna().sum()) for v in VERS}; rec("5_sasa", "SASA.IS", "-", "n_gap_days", per, w)

LG = pd.DataFrame(LONG); LG.to_csv(vers.RES + "/d1_long.csv", index=False)
print("satır", len(LG))
