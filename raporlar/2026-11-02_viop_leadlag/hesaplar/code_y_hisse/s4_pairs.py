"""Adım 4: Ekonomik bağlantılı çiftler (tedarik zinciri / rakip / grup): senkron vs öncülük, iki yön.
Her yönlü çift a->b: senkron (corr tam/3y/1y, XU100 kısmi, beta, yıllık işaret tutarlılığı), öncülük a_{t-k}->b_t (cc/gap/intra; tarama ile aynı kontroller),
IS/OOS/PRE, hacim filtresi, basit backtest (a_{t-1} işareti -> b gün-içi; IS'den yön), likidite oranı.
Çıktı: res/pairs.csv, res/pairs.txt
"""
import sys, os, itertools, numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata, hreg
sys.path.insert(0, hdata.SCR + "/code"); import ll
D = hdata.load(); cc, gap, intra, liq, tov = D["cc"], D["gap"], D["intra"], D["liq"], D["tov"]
ccL = pd.read_parquet(os.path.join(hdata.CACHE, "cc_long.parquet"))
idx = cc.index; SPLIT = pd.Timestamp(hdata.SPLIT)
XUSIN_X = set(hdata.XUSIN_MEM) | {"ISDMR", "AKCNS", "NUHCM", "BUCIM", "BAGFS", "OTKAR", "TTRAK", "AYGAZ", "EUPWR", "GESAN", "CWENE", "KRDMA", "KRDMB", "VESBE", "BRYAT", "CCOLA", "KCAER"}
BANKX = set(hdata.BANKS) | {"ALBRK", "SKBNK", "QNBTR", "ICBCT"}
def sec(j): return "XBANK" if j in BANKX else ("XUSIN" if j in XUSIN_X else None)

GROUPS = {
    "havacilik": ["THYAO", "PGSUS", "TAVHL", "CLEBI", "DOCO"],
    "rafineri": ["TUPRS", "AYGAZ", "PETKM"],
    "celik": ["EREGL", "KRDMD", "ISDMR", "BRSAN"],
    "banka": ["GARAN", "AKBNK", "YKBNK", "ISCTR", "HALKB", "VAKBN", "TSKB"],
    "otomotiv": ["FROTO", "TOASO", "DOAS", "OTKAR", "TTRAK"],
    "enerji-ekipman": ["ASTOR", "EUPWR", "GESAN", "CWENE"],
    "perakende": ["BIMAS", "MGROS", "SOKM"],
    "gubre": ["GUBRF", "BAGFS", "HEKTS"],
    "cimento": ["CIMSA", "OYAKC", "AKCNS", "NUHCM", "BUCIM"],
    "telekom": ["TCELL", "TTKOM"],
    "madencilik": ["TRALT", "TRMET", "TRENJ"],
    "icecek": ["AEFES", "CCOLA", "AGHOL"],
}
EXTRA = [("ASELS", "OTKAR", "savunma"), ("KCHOL", "SAHOL", "holding"), ("SAHOL", "AKBNK", "grup"), ("KCHOL", "YKBNK", "grup"), ("KCHOL", "FROTO", "grup"),
         ("KCHOL", "TUPRS", "grup"), ("KCHOL", "ARCLK", "grup"), ("KCHOL", "TOASO", "grup"), ("TKFEN", "ENKAI", "insaat"), ("VESTL", "VESBE", "grup"),
         ("BRSAN", "BRYAT", "grup"), ("ARCLK", "VESTL", "rakip"), ("HEKTS", "SASA", "grup"), ("ASELS", "SDTTR", "savunma"), ("ASELS", "ALTNY", "savunma"),
         ("ISCTR", "SISE", "grup"), ("ISCTR", "TSKB", "grup"), ("THYAO", "ASELS", "?"), ("DOHOL", "TKFEN", "?"), ("ALARK", "ENJSA", "enerji"),
         ("AKSEN", "ODAS", "enerji"), ("AKSEN", "ENJSA", "enerji"), ("EKGYO", "OYAKC", "insaat"), ("SAHOL", "ENJSA", "grup"), ("SAHOL", "CIMSA", "grup"),
         ("KCHOL", "AYGAZ", "grup"), ("EREGL", "KRDMA", "celik"), ("TUPRS", "THYAO", "yakit")]
PAIRS = []
for g, mem in GROUPS.items():
    for a, b in itertools.combinations(mem, 2): PAIRS.append((a, b, g))
PAIRS += EXTRA

def ctrl(j, k=1, df=None):
    df = cc if df is None else df; s = sec(j)
    base = [df[j].shift(1), df["XU100"].shift(1)] + ([df[s].shift(1)] if s else [])
    if k == 1: return pd.concat(base, axis=1)
    if k == "c5": add = [df[x].rolling(5, min_periods=5).sum().shift(1) for x in [j, "XU100"] + ([s] if s else [])]
    else: add = [df[x].shift(k) for x in [j, "XU100"] + ([s] if s else [])]
    return pd.concat(base + add, axis=1)

def reg1(y, x, C, mask=None, min_n=250):
    yv = y.values.copy()
    if mask is not None: yv[~mask] = np.nan
    r = hreg.nw_batch(yv, x.values.reshape(-1, 1), C.values, min_n=min_n)
    return r["b"][0], r["t"][0], r["pc"][0], int(r["n"][0])

def resid(s, mk):
    d = pd.concat([s, mk], axis=1).dropna(); b = np.cov(d.iloc[:, 0], d.iloc[:, 1])[0, 1] / d.iloc[:, 1].var()
    return s - b * mk

lowv = None
def lowvol():
    global lowv
    if lowv is None:
        med = tov.rolling(60, min_periods=20).median().shift(1); lowv = (tov.fillna(0) < 0.3 * med) | (tov.fillna(0) <= 0)
    return lowv

def pair_dir(a, b, grp):
    r = {"leader": a, "target": b, "group": grp}
    last = idx[-1]
    for lab, st in [("full", None), ("3y", last - pd.DateOffset(years=3)), ("1y", last - pd.DateOffset(years=1))]:
        d = pd.concat([cc[b], cc[a]], axis=1).dropna()
        if st is not None: d = d[d.index >= st]
        r[f"corr_{lab}"] = d.iloc[:, 0].corr(d.iloc[:, 1]) if len(d) > 60 else np.nan
    r["pcorr_xu100"], _ = ll.partial_corr(cc[b], cc[a], [cc["XU100"]])
    d = pd.concat([cc[b], cc[a], cc["XU100"]], axis=1).dropna(); d.columns = ["b", "a", "m"]
    import statsmodels.api as sm
    r["beta"] = sm.OLS(d["b"], sm.add_constant(d[["a"]])).fit().params["a"]
    ra = resid(cc[a], cc["XU100"]); rb = resid(cc[b], cc["XU100"])
    yc = pd.concat([ra, rb], axis=1).dropna(); yc = yc.groupby(yc.index.year).apply(lambda x: x.iloc[:, 0].corr(x.iloc[:, 1]) if len(x) > 60 else np.nan).dropna()
    r["sync_years_pos_share"] = float((np.sign(yc) == np.sign(r["pcorr_xu100"])).mean()); r["sync_years"] = len(yc)
    pIS = idx < SPLIT
    rIS = pd.concat([ra, rb], axis=1).dropna(); r["pc_IS"] = rIS[rIS.index < SPLIT].corr().iloc[0, 1]; r["pc_OOS"] = rIS[rIS.index >= SPLIT].corr().iloc[0, 1]
    # öncülük
    for dn, dd in [("cc", cc), ("gap", gap), ("intra", intra)]:
        for k in [1, 2, 3, 4, 5, "c5"]:
            x = cc[a].rolling(5, min_periods=5).sum().shift(1) if k == "c5" else cc[a].shift(k)
            if dn != "cc" and k not in (1, "c5"): continue
            bb, tt, pc, n = reg1(dd[b], x, ctrl(b, k))
            r[f"{dn}_l{k}_b"] = bb; r[f"{dn}_l{k}_t"] = tt; r[f"{dn}_l{k}_pc"] = pc
            if k == 1:
                r[f"{dn}_l1_n"] = n
                for pn, pm in [("IS", pIS), ("OOS", ~pIS)]:
                    _, r[f"{dn}_l1_t_{pn}"], r[f"{dn}_l1_pc_{pn}"], _ = reg1(dd[b], x, ctrl(b, 1), pm)
    # intra | gap_t
    C2 = pd.concat([ctrl(b, 1), gap[b], gap["XU100"]], axis=1)
    r["intra_g_l1_b"], r["intra_g_l1_t"], _, _ = reg1(intra[b], cc[a].shift(1), C2)
    # PRE
    pre = ccL[ccL.index < pd.Timestamp("2014-01-01")]
    try:
        _, r["cc_l1_t_PRE"], r["cc_l1_pc_PRE"], _ = reg1(pre[b], pre[a].shift(1), ctrl(b, 1, pre))
    except Exception: r["cc_l1_t_PRE"] = np.nan
    # yıllık işaret (cc lag1 ve intra lag1)
    for dn, dd in [("cc", cc), ("intra", intra)]:
        ys = []
        for yr in range(2014, 2027):
            _, tt, _, n = reg1(dd[b], cc[a].shift(1), ctrl(b, 1), idx.year == yr, min_n=120)
            ys.append(tt)
        ys = np.array(ys, float); ref = np.sign(r[f"{dn}_l1_t"])
        r[f"{dn}_l1_years_same_sign"] = float(np.nanmean(np.sign(ys) == ref)); r[f"{dn}_l1_t_by_year"] = " ".join("nan" if not np.isfinite(v) else f"{v:.1f}" for v in ys)
    # hacim filtresi
    lv = lowvol(); m = ~(lv[b] | lv[b].shift(1).fillna(True).astype(bool) | lv[a].shift(1).fillna(True).astype(bool)).values
    _, r["cc_l1_t_volf"], _, _ = reg1(cc[b], cc[a].shift(1), ctrl(b, 1), m)
    _, r["intra_l1_t_volf"], _, _ = reg1(intra[b], cc[a].shift(1), ctrl(b, 1), m)
    # likidite
    r["liq_ratio"] = liq.loc[a, "tov_med_oos_mnTL"] / liq.loc[b, "tov_med_oos_mnTL"]
    r["tov_leader"] = liq.loc[a, "tov_med_oos_mnTL"]; r["tov_target"] = liq.loc[b, "tov_med_oos_mnTL"]
    r["target_viop"] = b in hdata.VIOP; r["leader_viop"] = a in hdata.VIOP
    # backtest: a_{t-1} işareti (yön IS t'sinden) -> b gün-içi_t ; ayrıca rölatif (a_{t-1}-b_{t-1})
    sgn = np.sign(r["intra_l1_t_IS"]) if np.isfinite(r["intra_l1_t_IS"]) else 1.0
    for nm, sig in [("bt", sgn * cc[a].shift(1)), ("btrel", cc[a].shift(1) - cc[b].shift(1))]:
        if nm == "btrel":
            # rölatif için yön IS'den
            dd = pd.concat([sig, intra[b]], axis=1).dropna(); dd = dd[dd.index < SPLIT]
            s2 = np.sign(dd.iloc[:, 0].corr(dd.iloc[:, 1])) if len(dd) > 100 else 1.0; sig = s2 * sig
        for cost in [8, 15]:
            res, _ = ll.backtest(sig, intra[b], cost_bps=cost)
            r[f"{nm}{cost}_oos_sharpe"] = res["OOS"].get("sharpe", np.nan); r[f"{nm}{cost}_oos_bps"] = res["OOS"].get("mean_bps", np.nan)
            r[f"{nm}{cost}_is_sharpe"] = res["IS"].get("sharpe", np.nan)
        r[f"{nm}0_oos_bps"] = ll.backtest(sig, intra[b], cost_bps=0)[0]["OOS"].get("mean_bps", np.nan)
    return r

if __name__ == "__main__":
    rows = []
    for a, b, g in PAIRS:
        for x, y in [(a, b), (b, a)]:
            try: rows.append(pair_dir(x, y, g))
            except Exception as e: print("hata", x, y, e)
        print(a, b, flush=True)
    R = pd.DataFrame(rows); R.to_csv(os.path.join(hdata.RES, "pairs.csv"), index=False)
    # tüm çiftler için BH (cc lag1, intra lag1, gap lag1 ayrı aileler)
    for dn in ["cc", "gap", "intra"]:
        p = 2 * stats.norm.sf(R[f"{dn}_l1_t"].abs()); R[f"{dn}_l1_bh"] = ll.fdr(p, 0.05)[0]
    R.to_csv(os.path.join(hdata.RES, "pairs.csv"), index=False)
    cols = ["leader", "target", "group", "corr_full", "pcorr_xu100", "pc_IS", "pc_OOS", "cc_l1_t", "cc_l1_t_IS", "cc_l1_t_OOS", "cc_l1_t_PRE", "gap_l1_t", "intra_l1_t", "intra_g_l1_t",
            "cc_lc5_t", "cc_l1_t_volf", "cc_l1_years_same_sign", "bt8_oos_sharpe", "btrel8_oos_sharpe", "liq_ratio"]
    pd.set_option("display.width", 250)
    txt = R[cols].round(2).to_string(index=False); open(os.path.join(hdata.RES, "pairs.txt"), "w").write(txt); print(txt)
