"""v_YG2_a / 4: alternatif giriş/çıkış + maliyet duyarlılığı + kapasite.
Girişler: C_t (kapanış fiyatından işlemler, 18:08-18:10) | ertesi gün açılış müzayedesi O_{t+1} | ertesi gün ilk bar tipik fiyatı (VW30 vekili)
          | SSF uzlaşma (18:05-18:15 VWAP) | SSF son işlem (close)
Çıkışlar: 07:30_{t+1} (10:30 TSİ) | ilk bar tipik fiyatı | 08:30 | C_{t+1}
Maliyet (gidiş-dönüş, işlem başına): taban 8/15/30 bps + tik/fiyat (SSF tiki 0,01 TL; spot tik tablosu ayrıca). Kademeli: likit23 8, illikit24 20.
"""
import numpy as np, pandas as pd, vcommon as v
pd.set_option("display.width", 260); pd.set_option("display.max_columns", 40)
P = v.load()
V47 = [s for s in P.stock.unique() if s not in ("XU030", "XU100")]
X = P[P.stock == "XU030"].set_index("date")
S = P[P.stock.isin(V47)].copy()
g = S.groupby("stock")
S["O1"] = g["O"].shift(-1); S["P7_1"] = g["P0730"].shift(-1); S["P8_1"] = g["P0830"].shift(-1); S["C1"] = g["C"].shift(-1)
S["VW1"] = (g["fb_h"].shift(-1) + g["fb_l"].shift(-1) + S["P7_1"]) / 3
S["y_o_730"] = v.lg(S.P7_1, S.O1); S["y_o_c1"] = v.lg(S.C1, S.O1); S["y_vw_830"] = v.lg(S.P8_1, S.VW1); S["y_vw_c1"] = v.lg(S.C1, S.VW1)
S["y_c730_id"] = S["y_c730"] - S["date"].map(X["y_c730"]); S["CAid"] = S["CA"] - S["date"].map(X["CA"])
Z = pd.read_parquet(v.RES + "/v2_ssf_panel.parquet")[["stock", "date", "basis", "basis1", "y_ssf730"]]
S = S.merge(Z, on=["stock", "date"], how="left")
days = np.sort(P.date.unique()); half = days[len(days) // 2]
LQ = v.liquidity(S); rk = LQ.rank(ascending=False); liq = set(rk[rk <= 23].index)
S["liq"] = S.stock.isin(liq)
S["tick_ssf_bps"] = 1e4 * 0.01 / S["C"]
S["tick_spot_bps"] = 1e4 * v.tick_spot(S["C"]) / S["C"]
rows = []
def run(lab, sig, y, thr, m, cost_kind):
    d = S[m & S[sig].notna() & S[y].notna()]
    d = d[d[sig].abs() > thr]
    gross = -np.sign(d[sig]) * d[y] * 1e4
    r = dict(test=lab, thr_bps=thr * 1e4, n_tr=len(d))
    for per, mm in [("ALL", d.date >= days[0]), ("H1", d.date < half), ("H2", d.date >= half)]:
        gd = gross[mm].groupby(d.date[mm]).mean(); m_, t_, n_ = v.nw_t(gd)
        r[f"{per}_gross"] = m_; r[f"{per}_t"] = t_
    tk = d[cost_kind]
    for c in [8, 15, 30]:
        net = (gross - c - tk).groupby(d.date).mean(); m_, t_, n_ = v.nw_t(net); r[f"net{c}+tik"] = m_; r[f"t{c}"] = t_
    tier = np.where(d.liq, 8, 20)
    net = (gross - tier - tk).groupby(d.date).mean(); m_, t_, n_ = v.nw_t(net); r["net_kademeli"] = m_; r["t_kad"] = t_
    r["ort_tik_bps"] = tk.mean(); r["ort_|sig|_bps"] = 1e4 * d[sig].abs().mean(); r["n_days"] = d.date.nunique()
    rows.append(r)

base = S.CA.notna()
for thr in [0.0025, 0.005, 0.0075, 0.01]:
    run("A spot: C_t -> 07:30_{t+1}", "CA", "y_c730", thr, base, "tick_ssf_bps")
run("A' spot (spot tiki)", "CA", "y_c730", 0.0025, base, "tick_spot_bps")
run("A' spot (spot tiki)", "CA", "y_c730", 0.005, base, "tick_spot_bps")
run("A likit23", "CA", "y_c730", 0.0025, base & S.liq, "tick_ssf_bps")
run("A illikit24", "CA", "y_c730", 0.0025, base & ~S.liq, "tick_ssf_bps")
run("A likit23", "CA", "y_c730", 0.005, base & S.liq, "tick_ssf_bps")
run("A illikit24", "CA", "y_c730", 0.005, base & ~S.liq, "tick_ssf_bps")
run("B spot: C_t -> VW30_{t+1} (ilk bar tipik)", "CA", "y_cvw", 0.0025, base, "tick_ssf_bps")
run("C spot: C_t -> C_{t+1}", "CA", "y_cc", 0.0025, base, "tick_ssf_bps")
run("D hisseye özgü (XU030 hedge; +3 bps hedge ayrıca düşülmeli)", "CAid", "y_c730_id", 0.0025, S.CAid.notna(), "tick_ssf_bps")
run("D hisseye özgü", "CAid", "y_c730_id", 0.005, S.CAid.notna(), "tick_ssf_bps")
run("E ertesi açılış O_{t+1} -> 07:30", "CA", "y_o_730", 0.0025, base, "tick_ssf_bps")
run("E ertesi açılış O_{t+1} -> 07:30", "CA", "y_o_730", 0.005, base, "tick_ssf_bps")
run("F ertesi açılış O_{t+1} -> C_{t+1}", "CA", "y_o_c1", 0.0025, base, "tick_ssf_bps")
run("G ertesi VW30 -> 08:30", "CA", "y_vw_830", 0.0025, base, "tick_ssf_bps")
run("G ertesi VW30 -> 08:30", "CA", "y_vw_830", 0.005, base, "tick_ssf_bps")
run("H SSF: uzlaşma_t -> 07:30_{t+1} vekili", "CA", "y_ssf730", 0.0025, base & S.basis.notna(), "tick_ssf_bps")
run("H SSF: uzlaşma_t -> 07:30_{t+1} vekili", "CA", "y_ssf730", 0.005, base & S.basis.notna(), "tick_ssf_bps")
R = pd.DataFrame(rows); R.to_csv(v.RES + "/v4_entry_cost.csv", index=False)
print(R.round(1).to_string())

# kapasite: m5'te (60 gün) müzayede+kapanış fiyatından işlem hacim payı = 1 - Σ sürekli bar hacmi / günlük hacim
cap = []
for s in V47:
    try:
        m = pd.read_parquet(f"{v.SCR}/data/m5/{s}.IS.parquet"); m = m[~m.index.duplicated(keep="last")]
    except FileNotFoundError: continue
    t = m.index.tz_convert("UTC"); hm = t.hour * 100 + t.minute; day = pd.DatetimeIndex(t.tz_localize(None).normalize())
    cont = pd.Series(m["v"].values * ((hm >= 700) & (hm <= 1455)), index=day).groupby(level=0).sum()
    dl = pd.read_parquet(f"{v.SCR}/data/daily/{s}.IS.parquet"); dl.index = pd.DatetimeIndex(dl.ldate).normalize(); dl = dl[~dl.index.duplicated(keep="last")]
    j = pd.concat([cont.rename("cont"), dl["v"].rename("dv"), dl["c"].rename("c")], axis=1).dropna()
    j = j[(j.dv > 0) & (j.cont > 0)]
    sh = 1 - j.cont / j.dv
    cap.append(dict(stock=s, auction_share_med=sh.median(), daily_TL_mn=(j.dv * j.c).median() / 1e6, auction_TL_mn=(sh.clip(lower=0) * j.dv * j.c).median() / 1e6, n=len(j)))
CP = pd.DataFrame(cap).sort_values("daily_TL_mn"); CP.to_csv(v.RES + "/v4_capacity.csv", index=False)
print(CP.round(3).to_string())
print("medyan müzayede (açılış+kapanış+kapanış fiyatından) hacim payı:", round(CP.auction_share_med.median(), 4))
