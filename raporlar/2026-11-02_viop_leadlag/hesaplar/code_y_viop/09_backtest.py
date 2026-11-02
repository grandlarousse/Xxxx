"""Görev 6: Backtestler (look-ahead yok; maliyet = y_viop_likidite.csv'deki hisse bazlı gidiş-dönüş tahmini).
IS = 2017-04..2022-12, OOS = 2023-01..2026-10.
BT1 Baz anomalisi (kesitsel, hisse vadelileri): sinyal anom_dev_t (t akşamı bilinir) -> t+1 09:30 açılış seansında gir (emir önceden
    verilebilir), t+1 kapanışında çık. Hedef: vadeli gün-içi (L_r_intra) ve alternatif spot gün-içi (09:55 açılış müzayedesi -> kapanış).
    Üst %20 long / alt %20 short (eşit ağırlık). Maliyet: her gün her pozisyon için RT.
BT2 AP/hacim (kesitsel): 07_oi.py'de en güçlü FM sinyali (vsur -> spot gün-içi negatif / gap pozitif); vadeli gün-içi hedefle aynı kurulum.
BT3 XU030 vadeli gün-içi/gece ayrışması (zaman serisi): (a) 09:30 açılışta short, 18:15 kapanışta kapat; (b) 18:15 kapanışta long, ertesi 09:30 açılışta kapat.
BT4 Vadeli açılış gap'i (09:30) -> spot gün-içi tersine dönüş: |gF|>eşik ise spot açılış müzayedesinde (09:40-09:55) ters yönde gir, kapanışta çık.
BT5 XU030 baz anomalisi -> XU030 vadeli (yakınsama), t+1 açılış->kapanış ve kapanış->kapanış.
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from vcommon import *
LQ = pd.read_csv(OUT + "/y_viop_likidite.csv").set_index("und")
COST = LQ["rt_cost_small_bps"].to_dict(); COSTC = LQ["rt_cost_cons_bps"].to_dict()
SPLIT = pd.Timestamp("2023-01-01")
def stats(p, name, extra=None):
    p = p.dropna()
    res = dict(bt=name)
    for per, x in [("ALL", p), ("IS", p[p.index < SPLIT]), ("OOS", p[p.index >= SPLIT])]:
        if len(x) < 40: res.update({f"{per}_n": len(x)}); continue
        m, t, n = ll.nw_t(x)
        sh = x.mean() / x.std() * np.sqrt(252) if x.std() > 0 else np.nan
        res.update({f"{per}_n": n, f"{per}_mean_bps": 1e4 * m, f"{per}_t": t, f"{per}_sharpe": sh, f"{per}_hit": (x > 0).mean()})
    yr = (1e4 * p.groupby(p.index.year).mean()).round(1)
    res["by_year_bps"] = yr.to_dict(); res["years_pos_frac"] = (yr > 0).mean()
    if extra: res.update(extra)
    return res
def cs_ls(P, sig, tgt, q=0.2, min_names=10, sign=1, cost=COST, liq=None):
    d = P[["date", "und", sig, tgt]].replace([np.inf, -np.inf], np.nan).dropna()
    if liq is not None: d = d[d["und"].map(LQ["liq_class"]).isin(liq)]
    d["c"] = d["und"].map(cost) / 1e4
    d = d[d.groupby("date")[sig].transform("count") >= min_names]
    d["rk"] = d.groupby("date")[sig].rank(pct=True)
    L = d[d["rk"] > 1 - q]; S_ = d[d["rk"] <= q]
    if sign < 0: L, S_ = S_, L
    gl = L.groupby("date").agg(r=(tgt, "mean"), c=("c", "mean")); gs = S_.groupby("date").agg(r=(tgt, "mean"), c=("c", "mean"))
    j = gl.join(gs, lsuffix="_l", rsuffix="_s", how="inner")
    gross = j["r_l"] - j["r_s"]; net = gross - (j["c_l"] + j["c_s"])
    return gross, net, j
rows = []
# ---------- BT1: baz anomalisi ----------
# Yön IS (2017-2022) FM işaretinden alınır: anom_dev -> vadeli gün-içi NEGATİF => pahalı vadeliyi SAT, ucuzu AL (sign=-1).
B = pd.read_parquet(RES + "/basis_panel.parquet").sort_values(["und", "date"])
Dd = pd.read_parquet(RES + "/daily_all.parquet")[["und", "date", "L_vwap", "L_open", "L_settle", "L_code"]]
B = B.merge(Dd[["und", "date", "L_vwap", "L_open"]], on=["und", "date"], how="left")
B["ndays"] = B.groupby("und")["date"].shift(-1) - B["date"]
for c in ["L_r_intra", "sp_intra", "sp_cc", "L_r_set"]:
    B[f"y_{c}"] = B.groupby("und")[c].shift(-1); B.loc[B["ndays"] > pd.Timedelta(days=5), f"y_{c}"] = np.nan
# VWAP(t+1) -> VWAP(t+2), aynı sözleşme (L kodu t+1'de); açılış(t+1) -> uzlaşma(t+1)
B["nx_code"] = B.groupby("und")["L_code"].shift(-1); B["nx2_code"] = B.groupby("und")["L_code"].shift(-2)
B["vw1"] = B.groupby("und")["L_vwap"].shift(-1); B["vw2"] = B.groupby("und")["L_vwap"].shift(-2)
B["y_vwap"] = np.log(B["vw2"] / B["vw1"]).where(B["nx_code"] == B["nx2_code"])
B["y_open_set"] = np.log(B.groupby("und")["L_settle"].shift(-1) / B.groupby("und")["L_open"].shift(-1))
for c in ["y_vwap", "y_open_set"]:
    B.loc[(B["ndays"] > pd.Timedelta(days=5)) | (B[c].abs() > 0.2), c] = np.nan
B.to_parquet(RES + "/bt1_panel.parquet", index=False)
BS = B[B["und"].isin(STOCKS)]
for tgt, sg in [("y_L_r_intra", -1), ("y_open_set", -1), ("y_vwap", -1), ("y_sp_intra", 1)]:
    for liq in [None, ["A", "B"], ["A"]]:
        for q in [0.2, 0.1]:
            if q == 0.1 and liq is not None: continue
            g, n, j = cs_ls(BS, "anom_dev", tgt, q=q, sign=sg, liq=liq)
            lab = f"BT1 baz anomalisi ({'pahalıyı SAT' if sg < 0 else 'pahalı vadelide spotu AL'}) q={q} -> {tgt} ({'tümü' if liq is None else '/'.join(liq) + ' likit'})"
            rows.append(stats(g, lab + " BRÜT")); rows.append(stats(n, lab + " NET", dict(avg_cost_bps=1e4 * (j['c_l'] + j['c_s']).mean())))
            if liq is None and q == 0.2:
                _, nc, jc = cs_ls(BS, "anom_dev", tgt, q=q, sign=sg, cost=COSTC, liq=liq)
                rows.append(stats(nc, lab + " NET (muhafazakâr maliyet)", dict(avg_cost_bps=1e4 * (jc['c_l'] + jc['c_s']).mean())))
# ---------- BT2: AP/hacim ----------
P = pd.read_parquet(RES + "/oi_panel.parquet")
P["y_L_r_intra"] = P.groupby("und")["L_r_intra"].shift(-1)
PS = P[P["und"].isin(STOCKS)]
for sig, sg in [("vsur", -1), ("dOI_z", -1)]:
    for tgt in ["y_L_r_intra", "y_sp_intra"]:
        g, n, j = cs_ls(PS, sig, tgt, sign=sg)
        lab = f"BT2 {sig} ({'+' if sg > 0 else '-'}) L/S -> {tgt}"
        rows.append(stats(g, lab + " BRÜT")); rows.append(stats(n, lab + " NET", dict(avg_cost_bps=1e4 * (j['c_l'] + j['c_s']).mean())))
# ---------- BT3: XU030 gün-içi / gece ----------
D = pd.read_parquet(RES + "/daily_all.parquet")
x = D[D["und"] == "XU030"].set_index("date").sort_index()
cX = COST["XU030"] / 1e4
intra = x["L_r_intra"]; on = x["L_r_on"]  # açılış/önceki kapanış (aynı sözleşme)
rows.append(stats(-intra - cX, "BT3a XU030 vadeli: 09:30 açılışta SAT, 18:15 kapanışta kapat NET", dict(gross_mean_bps=-1e4 * intra.mean())))
rows.append(stats(on - cX, "BT3b XU030 vadeli: 18:15 kapanışta AL, ertesi 09:30 açılışta kapat NET", dict(gross_mean_bps=1e4 * on.mean())))
rows.append(stats(-intra, "BT3a XU030 BRÜT")); rows.append(stats(on, "BT3b XU030 BRÜT"))
xl = D[D["und"] == "XLBNK"].set_index("date").sort_index()
rows.append(stats(-xl["L_r_intra"] - COST["XLBNK"] / 1e4, "BT3c XLBNK vadeli: açılışta SAT, kapanışta kapat NET", dict(gross_mean_bps=-1e4 * xl["L_r_intra"].mean())))
# ---------- BT4: vadeli açılış gap'i -> spot gün-içi (fade) ----------
O = pd.read_parquet(RES + "/openclose_panel.parquet")
OS = O[O["und"].isin(STOCKS)].copy()
for thr in [0.0, 0.01, 0.02]:
    OS["pos"] = -np.sign(OS["gF"]).where(OS["gF"].abs() > thr, 0)
    OS["c"] = OS["und"].map(COST) / 1e4
    OS["pnl"] = OS["pos"] * OS["sp_intra"] - OS["pos"].abs() * OS["c"]
    OS["gpnl"] = OS["pos"] * OS["sp_intra"]
    act = OS[OS["pos"] != 0]
    pn = act.groupby("date")["pnl"].mean(); pg = act.groupby("date")["gpnl"].mean()
    rows.append(stats(pg, f"BT4 vadeli açılış gap'i fade (|gF|>{thr:.0%}) -> spot gün-içi, eşit ağırlık BRÜT", dict(avg_names=act.groupby('date').size().mean())))
    rows.append(stats(pn, f"BT4 vadeli açılış gap'i fade (|gF|>{thr:.0%}) -> spot gün-içi NET"))
# ---------- BT5: XU030 baz anomalisi ----------
bx = B[B["und"] == "XU030"].set_index("date")
for tgt in ["y_L_r_intra", "y_L_r_set"]:
    s = bx["anom_dev"]; pos = -np.sign(s)  # pahalı vadeli -> sat
    pnl = pos * bx[tgt] - cX * pos.abs()
    rows.append(stats(pnl, f"BT5 XU030 baz anomalisi (pahalıysa sat) -> {tgt} NET", dict(gross_mean_bps=1e4 * (pos * bx[tgt]).mean())))
R = pd.DataFrame(rows)
R.to_csv(RES + "/backtests.csv", index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_colwidth", 90)
cols = ["bt", "ALL_n", "ALL_mean_bps", "ALL_t", "ALL_sharpe", "IS_mean_bps", "IS_t", "IS_sharpe", "OOS_mean_bps", "OOS_t", "OOS_sharpe", "years_pos_frac", "avg_cost_bps", "gross_mean_bps"]
print(R[[c for c in cols if c in R]].round(2).to_string(index=False))
