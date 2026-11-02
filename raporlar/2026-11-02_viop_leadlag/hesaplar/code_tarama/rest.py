"""Görev 3 (piyasa düzeyi), 4 (hisse başına ilk 5 dış sürücü), 5 (sürprizler), 6 (backtest) + f_tarama.csv.
Çalıştır: nice -n 10 python3 rest.py  (önce matrix.py)"""
import os, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlib import *
import statsmodels.api as sm
import ll

P, DP = load_panels(); idx = P.index
M = pd.read_parquet(os.path.join(OUT, "tarama_matrix.parquet")); V = M[~M.is_index_row].copy()
dm = pd.read_parquet(os.path.join(CACHE, "driver_meta.parquet"))
dm["group"] = [regroup(s_, g_, n_) for s_, g_, n_ in zip(dm.index, dm.group, dm.name)]
M["group"] = M.driver.map(dm.group); V = M[~M.is_index_row].copy()

# ======================= GÖREV 3: piyasa düzeyi =======================
MK = ["EEM", "^GSPC", "ES=F", "^STOXX50E", "TRY=X", "^VIX", "BZ=F", "DX-Y.NYB", "^TNX", "EMB"]
REG = [("2014-2017", "2014-01-01", "2017-12-31"), ("2018 kur krizi", "2018-01-01", "2018-12-31"), ("2019-2020", "2019-01-01", "2020-12-31"),
       ("2021 (Aralık şoku)", "2021-01-01", "2021-12-31"), ("2022-May23 heterodoks", "2022-01-01", "2023-05-31"),
       ("Haz23-Mar25 ortodoks", "2023-06-01", "2025-03-18"), ("Mar25-Ara25 İmamoğlu sonrası", "2025-03-19", "2025-12-31"),
       ("2026 Oca-Ağu", "2026-01-01", "2026-08-31"), ("Eyl-Eki 2026 fon krizi", "2026-09-01", "2026-10-30"), ("son 1y", "2025-10-31", "2026-10-30"),
       ("TAM 2014-2026", "2014-01-01", "2026-10-30")]
def r2(y, X):
    d = pd.concat([y.rename("y"), X], axis=1).dropna()
    if len(d) < 30: return np.nan, len(d)
    m = sm.OLS(d["y"], sm.add_constant(d.drop(columns="y"))).fit(); return m.rsquared, len(d)
tgt = {"XU100": P["XU100.IS"], "XU030": P["XU030.IS"], "XU100_USD": P["XU100.IS"] - P["TRY=X"]}
gap = DP.reindex(idx)[("XU100", "gap")]; intra = DP.reindex(idx)[("XU100", "intra")]
Xs = P[MK]; Xs_noTRY = P[[c for c in MK if c != "TRY=X"]]
US = ["^GSPC", "ES=F", "EEM", "^VIX", "^TNX", "EMB", "DX-Y.NYB", "BZ=F"]
rows = []
def per(lab, a, b):
    m = (idx >= a) & (idx <= b); out = {"dönem": lab}
    for k, y in tgt.items():
        XX = Xs_noTRY if k == "XU100_USD" else Xs
        out[f"R2_sync_{k}"], out["n"] = r2(y[m], XX[m])
    out["R2_sync_XU100_yalnızTRY"] = r2(tgt["XU100"][m], P[["TRY=X"]][m])[0]
    out["R2_sync_XU100_yalnızEEM"] = r2(tgt["XU100"][m], P[["EEM"]][m])[0]
    out["R2_ABDlag1_gap"] = r2(gap[m], P[US].shift(1)[m])[0]
    out["R2_ABDlag1_intra"] = r2(intra[m], P[US].shift(1)[m])[0]
    out["R2_ABDlag1_cc"] = r2(tgt["XU100"][m], P[US].shift(1)[m])[0]
    # Dimson beta (lag0+lag1) USD bazlı XU100 ~ EEM ve ~ ^GSPC
    for f in ["EEM", "^GSPC"]:
        d = pd.concat([tgt["XU100_USD"][m].rename("y"), P[f][m].rename("x0"), P[f].shift(1)[m].rename("x1")], axis=1).dropna()
        if len(d) > 30:
            b = sm.OLS(d["y"], sm.add_constant(d[["x0", "x1"]])).fit().params
            out[f"beta_dimson_USD_{f}"] = b["x0"] + b["x1"]; out[f"corr0_USD_{f}"] = d["y"].corr(d["x0"])
    out["vol_XU100_USD_ann%"] = tgt["XU100_USD"][m].std() * np.sqrt(252) * 100
    return out
for lab, a, b in REG: rows.append(per(lab, a, b))
for y in range(2014, 2027): rows.append(per(str(y), f"{y}-01-01", f"{y}-12-31"))
MKT = pd.DataFrame(rows); MKT.round(3).to_csv(os.path.join(CACHE, "market_level.csv"), index=False)
# tek değişkenli senkron R2 (tam / son 1y)
uni = []
for f in MK + ["TUR", "^GDAXI", "GC=F", "^N225", "^KS11", "^HSI"]:
    for lab, a, b in [("full", "2014-01-01", "2026-10-30"), ("1y", "2025-10-31", "2026-10-30")]:
        m = (idx >= a) & (idx <= b)
        uni.append({"driver": f, "win": lab, "corr_XU100": tgt["XU100"][m].corr(P[f][m]), "corr_XU100_USD": tgt["XU100_USD"][m].corr(P[f][m]),
                    "corr_gap_lag1": gap[m].corr(P[f].shift(1)[m]), "corr_intra_lag1": intra[m].corr(P[f].shift(1)[m])})
pd.DataFrame(uni).round(3).to_csv(os.path.join(CACHE, "market_univariate.csv"), index=False)

# ======================= GÖREV 4: hisse başına ilk 5 =======================
SECT = {"AKBNK": "bank", "GARAN": "bank", "HALKB": "bank", "ISCTR": "bank", "VAKBN": "bank", "YKBNK": "bank", "TSKB": "bank",
        "KCHOL": "hold", "SAHOL": "hold", "DOHOL": "hold", "ALARK": "hold", "THYAO": "air", "PGSUS": "air", "TAVHL": "airport",
        "AKSEN": "util", "ENJSA": "util", "ODAS": "util", "EREGL": "steel", "KRDMD": "steel", "BRSAN": "steel", "TRALT": "gold", "TRMET": "metal",
        "PETKM": "chem", "SASA": "chem", "HEKTS": "agro", "GUBRF": "agro", "SISE": "glass", "TUPRS": "oil", "FROTO": "auto", "TOASO": "auto",
        "DOAS": "auto", "ARCLK": "white", "VESTL": "white", "ASTOR": "eleq", "ASELS": "def", "BIMAS": "retail", "MGROS": "retail", "SOKM": "retail",
        "ULKER": "food", "AEFES": "bev", "CIMSA": "cement", "OYAKC": "cement", "ENKAI": "constr", "TKFEN": "constr", "EKGYO": "re", "TCELL": "tel", "TTKOM": "tel"}
EXP = {"bank": {"bank", "re"}, "hold": {"bank", "auto", "oil", "util", "cons", "cement"}, "air": {"air", "oil"}, "airport": {"air"}, "util": {"util"},
       "steel": {"steel", "cement", "auto"}, "gold": {"steel"}, "metal": {"steel"}, "chem": {"chem", "oil"}, "agro": {"chem"}, "glass": {"chem", "cement", "cons"},
       "oil": {"oil"}, "auto": {"auto"}, "white": {"auto", "cons"}, "eleq": {"auto", "util"}, "def": {"def"}, "retail": {"cons"}, "food": {"cons"},
       "bev": {"cons"}, "cement": {"cement"}, "constr": {"cement", "util", "oil", "chem"}, "re": {"re", "cement", "bank"}, "tel": {"tel"}}
MACRO = {"idx", "etf", "fx", "vol", "rates", "cmd"}
def mech(stock, drv, grp):
    s = SECT.get(stock, "?")
    if drv in MIRROR or grp == "tr_abroad": return "TR-ayna (mekanik)"
    if grp in EXP.get(s, set()): return f"sektör emsali ({grp})"
    if grp in MACRO: return f"makro/emtia ({grp})"
    return f"BEKLENMEYEN ({grp})"
V["mech"] = [mech(s, d, g) for s, d, g in zip(V.stock, V.driver, V.group)]
cand = V[~V["sparse"] & ~V.mirror & V.pc_xt_full.notna()].copy(); cand["a"] = cand.pc_xt_full.abs()
top5 = cand.sort_values("a", ascending=False).groupby("stock").head(5).sort_values(["stock", "a"], ascending=[True, False])
keep = ["stock", "driver", "group", "bucket", "tv", "mech", "pc_xt_full", "t_pc_xt_full", "q_pc_xt_full", "pc_xt_is", "pc_xt_oos", "pc_xt_1y",
        "pc_glob_full", "q_pc_glob_full", "sync_full", "sync_3y", "sync_1y", "beta_sync_full", "n_sync_full"]
top5[keep].round(4).to_csv(os.path.join(CACHE, "top5_per_stock.csv"), index=False)

# ======================= GÖREV 5: sürprizler =======================
sur = V[(V.q_pc_xt_full < 0.05) & ~V["sparse"] & V.mech.str.startswith("BEKLENMEYEN")].copy()
sur["rep_oos"] = (np.sign(sur.pc_xt_is) == np.sign(sur.pc_xt_oos)) & (sur.p_pc_xt_oos < 0.05)
sur["glob_survives"] = sur.q_pc_glob_full < 0.05
sur = sur.sort_values("t_pc_xt_full", key=np.abs, ascending=False)
sur[["stock", "driver", "group", "bucket", "pc_xt_full", "t_pc_xt_full", "pc_xt_is", "pc_xt_oos", "pc_glob_full", "q_pc_glob_full", "rep_oos", "glob_survives", "zero_frac_2014"]].round(4).to_csv(os.path.join(CACHE, "surprises.csv"), index=False)
# lead ailelerinde FDR (kova içi) geçen sürprizler
lead_sur = []
for f, bks in [("intra_l1", ["asia_pre", "during", "us", "eu", "asia_mid"]), ("cum25", ["asia_pre", "during", "us", "eu", "asia_mid"]), ("intra_l0", ["asia_pre"])]:
    for b in bks:
        g = V[(V.bucket == b)].copy(); r, _ = bh(g[f"p_{f}_full"].values, 0.05); g = g[r]
        for _, x in g.iterrows(): lead_sur.append({"fam": f, "bucket": b, "stock": x.stock, "driver": x.driver, "group": x.group, "corr": x[f"{f}_full"], "t": x[f"t_{f}_full"], "t_is": x[f"t_{f}_is"], "t_oos": x[f"t_{f}_oos"], "mech": x.mech})
LS = pd.DataFrame(lead_sur); LS.round(4).to_csv(os.path.join(CACHE, "lead_bucket_fdr.csv"), index=False)

# ======================= GÖREV 6: backtest =======================
def shifted(s, k): return s.shift(k)
INTRA = {s: DP[(s, "intra")] for s in VIOP + ["XU030", "XU100"]}
CCs = {s: P[s + ".IS"] for s in VIOP + ["XU030", "XU100"]}
pool = []
for f in ["intra_l1", "cum25", "intra_l0"]:
    g = M[(~M["sparse"]) & M[f"t_{f}_is"].notna() & M.stock.isin(VIOP + ["XU030", "XU100"])].copy()
    if f == "intra_l0": g = g[g.bucket == "asia_pre"]
    g["fam"] = f; g["t_is_"] = g[f"t_{f}_is"]; g["c_is_"] = g[f"{f}_is"]; pool.append(g[["stock", "driver", "group", "bucket", "tv", "fam", "t_is_", "c_is_"]])
pool = pd.concat(pool); pool["a"] = pool.t_is_.abs(); pool = pool.sort_values("a", ascending=False)
sel = pool.drop_duplicates("driver").head(10)
ref = pd.DataFrame([{"stock": "XU030", "driver": d, "fam": "intra_l1"} for d in ["^GSPC", "ES=F", "TUR", "EEM", "^VIX"]] +
                   [{"stock": "XU030", "driver": d, "fam": "intra_l0"} for d in ["^N225", "^KS11"]])
ref = ref.merge(M[M.stock == "XU030"][["stock", "driver", "group", "bucket", "tv", "intra_l1_is", "intra_l0_is", "t_intra_l1_is", "t_intra_l0_is"]], on=["stock", "driver"], how="left")
ref["c_is_"] = np.where(ref.fam == "intra_l1", ref.intra_l1_is, ref.intra_l0_is); ref["t_is_"] = np.where(ref.fam == "intra_l1", ref.t_intra_l1_is, ref.t_intra_l0_is)
BT = []
for kind, S in [("IS-seçilmiş top10", sel), ("referans XU030", ref)]:
    for _, x in S.iterrows():
        d = P[x.driver]; sg = np.sign(x.c_is_) if np.isfinite(x.c_is_) else 1.0
        if x.fam == "intra_l1": sig, y = d.shift(1), INTRA[x.stock]
        elif x.fam == "intra_l0": sig, y = d, INTRA[x.stock]
        else: sig, y = d.shift(2) + d.shift(3) + d.shift(4) + d.shift(5), CCs[x.stock]
        for cost in [8, 15]:
            for mode, thr in [("sign", 0.0), ("z", 1.0)]:
                res, pnl = ll.backtest(sg * sig, y, cost_bps=cost, mode=mode, thr=thr)
                BT.append({"set": kind, "stock": x.stock, "driver": x.driver, "fam": x.fam, "bucket": x.bucket, "tv": x.tv, "t_is_sel": x.t_is_, "cost": cost, "mode": f"{mode}{thr:g}",
                           "IS_sharpe": res["IS"].get("sharpe"), "IS_bps": res["IS"].get("mean_bps"), "IS_t": res["IS"].get("t"), "OOS_sharpe": res["OOS"].get("sharpe"),
                           "OOS_bps": res["OOS"].get("mean_bps"), "OOS_t": res["OOS"].get("t"), "OOS_hit": res["OOS"].get("hit"), "OOS_n": res["OOS"].get("n"),
                           "by_year": str(res["by_year_bps"]) if cost == 8 and mode == "sign" else ""})
BT = pd.DataFrame(BT); BT.round(3).to_csv(os.path.join(CACHE, "backtest.csv"), index=False)

# ======================= f_tarama.csv =======================
def isoos(ci, co, po):
    if not (np.isfinite(ci) and np.isfinite(co)): return ""
    return ("aynı işaret" if np.sign(ci) == np.sign(co) else "TERS işaret") + (", OOS p<0.05" if po < 0.05 else ", OOS anlamsız")
def conf_sync(x):
    pc = abs(x.pc_xt_full); rep = np.sign(x.pc_xt_is) == np.sign(x.pc_xt_oos) and x.p_pc_xt_oos < 0.05 and x.p_pc_xt_is < 0.05
    plaus = not x.mech.startswith("BEKLENMEYEN")
    if x.q_pc_xt_full < 0.05 and pc >= 0.15 and rep and plaus: return "YÜKSEK"
    if x.q_pc_xt_full < 0.05 and np.sign(x.pc_xt_is) == np.sign(x.pc_xt_oos) and plaus: return "ORTA"
    if x.q_pc_xt_full < 0.05 or plaus: return "DÜŞÜK"
    return "ÇOK DÜŞÜK"
F = []
t5 = top5
for _, x in t5.iterrows():
    F.append({"stock": x.stock, "driver_yahoo": x.driver, "driver_desc": dm.loc[x.driver, "name"], "tv_ticker": x.tv, "relation": "sync", "lag": 0,
              "corr_full": x.sync_full, "corr_3y": x.sync_3y, "corr_1y": x.sync_1y, "pcorr_xu100": x.pc_xt_full, "beta": x.beta_sync_full, "t_stat": x.t_pc_xt_full,
              "gap_corr": x.gap_l1_full, "intra_corr": x.intra_l1_full, "is_oos": f"pc_xt IS {x.pc_xt_is:.3f} / OOS {x.pc_xt_oos:.3f}: " + isoos(x.pc_xt_is, x.pc_xt_oos, x.p_pc_xt_oos),
              "bt_oos_sharpe": "", "bt_oos_mean_bps": "", "n": x.n_sync_full, "confidence": conf_sync(x), "mechanism": x.mech,
              "notes": f"pcorr=XU100+USDTRY kontrollü; q={x.q_pc_xt_full:.2g}; küresel-10 faktör sonrası pc={x.pc_glob_full:.3f} (q={x.q_pc_glob_full:.2g}); kova={x.bucket}"})
b8 = BT[(BT.cost == 15) & (BT["mode"] == "sign")]
for _, x in b8.iterrows():
    r = M[(M.stock == x.stock) & (M.driver == x.driver)].iloc[0]; f = x.fam
    rel = {"intra_l1": "lead_intra", "intra_l0": "lead_intra", "cum25": "lead_multiday"}[f]
    ok = (x.OOS_t or 0) > 2 and (x.IS_t or 0) > 2
    F.append({"stock": x.stock, "driver_yahoo": x.driver, "driver_desc": dm.loc[x.driver, "name"] if x.driver in dm.index else "", "tv_ticker": x.tv, "relation": rel,
              "lag": {"intra_l1": 1, "intra_l0": 0, "cum25": "2-5"}[f], "corr_full": r.sync_full, "corr_3y": r.sync_3y, "corr_1y": r.sync_1y, "pcorr_xu100": r.pc_xu_full,
              "beta": r.beta_sync_full, "t_stat": r[f"t_{f}_full"], "gap_corr": r.gap_l1_full, "intra_corr": r[f"{f}_full"] if f != "cum25" else r.intra_l1_full,
              "is_oos": f"{f} t_IS {r[f't_{f}_is']:.2f} / t_OOS {r[f't_{f}_oos']:.2f}", "bt_oos_sharpe": x.OOS_sharpe, "bt_oos_mean_bps": x.OOS_bps, "n": r[f"n_{f}_full"],
              "confidence": "ORTA" if ok else ("DÜŞÜK" if (x.OOS_t or 0) > 0 else "ÇOK DÜŞÜK"), "mechanism": f"{x.set}; {f}",
              "notes": f"15 bps, sign modu; FDR(tüm aile) GEÇMEDİ: {f} ailesinde 0 çift FDR q<0.05; seçim IS |t| ile ({x.t_is_sel:.2f})"})
for _, x in MKT[MKT["dönem"].isin([r_[0] for r_ in REG])].iterrows():
    F.append({"stock": "XU100", "driver_yahoo": "EEM", "driver_desc": "Dimson beta (USD bazlı XU100 ~ EEM lag0+lag1)", "tv_ticker": "AMEX:EEM", "relation": "regime", "lag": "0+1",
              "corr_full": x.get("corr0_USD_EEM"), "beta": x.get("beta_dimson_USD_EEM"), "n": x.n, "confidence": "ORTA",
              "mechanism": "küresel EM risk iştahı", "notes": f"{x['dönem']}: R2 sync(10 makro) TL={x.R2_sync_XU100:.3f}, USD={x.R2_sync_XU100_USD:.3f}; ABD lag1->gap R2={x.R2_ABDlag1_gap:.3f}, ->intra R2={x.R2_ABDlag1_intra:.3f}"})
FD = pd.DataFrame(F)
for c in ["corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr", "bt_oos_sharpe", "bt_oos_mean_bps"]:
    FD[c] = pd.to_numeric(FD[c], errors="coerce").round(4)
FD.to_csv(os.path.join(CACHE, "f_tarama_basic.csv"), index=False)

# ---- kısa özet ----
print(MKT[MKT["dönem"].isin([r_[0] for r_ in REG])][["dönem", "n", "R2_sync_XU100", "R2_sync_XU100_USD", "R2_sync_XU100_yalnızEEM", "R2_ABDlag1_gap", "R2_ABDlag1_intra", "beta_dimson_USD_EEM", "corr0_USD_EEM", "beta_dimson_USD_^GSPC"]].round(3).to_string(index=False))
print("top5 güven:", FD[FD.relation == "sync"].confidence.value_counts().to_dict(), "| top5 mech:", top5.mech.str.split(" ").str[0].value_counts().to_dict())
print("sürpriz (pc_xt FDR + BEKLENMEYEN):", len(sur), "OOS rep:", int(sur.rep_oos.sum()), "küresel sonrası FDR:", int(sur.glob_survives.sum()))
print("lead kova-içi FDR geçen:", LS.groupby(["fam", "bucket"]).size().to_dict() if len(LS) else 0)
print(BT[(BT.cost == 15)][["set", "stock", "driver", "fam", "mode", "t_is_sel", "IS_sharpe", "OOS_sharpe", "OOS_bps", "OOS_t"]].round(2).to_string(index=False))
