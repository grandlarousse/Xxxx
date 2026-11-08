"""s6: aday stratejiler — parametre IS'te (2008-2017) seçilir, OOS (2018+) bir kez değerlendirilir.
Pozisyon: x > IS q-kantili -> +işaret, x < IS (1-q)-kantili -> -işaret (işaret IS IC'sinden), gün t 16:00 ET kapanışında alınır, h gün kademeli tutulur.
Sürümler: ideal (±1 dayanak; açığa satış varsayımsal), yalnız uzun (değilse nakit), uzun + kısa yön ters ETF (GLL/DUST/JDST/ZSL ≈ -1x ağırlık = 1/|geçmiş beta|).
Maliyet: dayanak 10/20 bps, ters ETF 20/40 bps gidiş-dönüş.
"""
from e2_common import *
d = load()
R = {t: ret_of(d, t) for t in ["GLD", "GDX", "GDXJ", "SLV", "SPY"]}
SIG1 = pd.read_pickle(f"{OUT}/s1_signals.pkl"); FEAT3 = pd.read_pickle(f"{OUT}/s3_signals.pkl"); SIG2 = pd.read_pickle(f"{OUT}/s2_signals.pkl"); SIGA = pd.read_pickle(f"{OUT}/s7_signals.pkl")
gi = np.log(d["xau_cut"]) - np.log(d["xau_close"].shift(1))
CANDS = {
    "C1_madenci_oncu_GLD": dict(und="GLD", sign=+1, grid=[(("GDX~GLD+SPY", k), h, q) for k in (5, 10) for h in (3, 5) for q in (0.7, 0.8)], src=SIG1),
    "C1j_madenciJ_oncu_GLD": dict(und="GLD", sign=+1, grid=[(("GDXJ~GLD+SPY", k), h, q) for k in (5, 10) for h in (3, 5) for q in (0.7, 0.8)], src=SIG1),
    "C2_artik_momentum_GDX": dict(und="GDX", sign=+1, grid=[(("GDX~GLD+SPY", k), h, q) for k in (1, 3) for h in (1, 3) for q in (0.7, 0.8)], src=SIG1),
    "C2j_artik_momentum_GDXJ": dict(und="GDXJ", sign=+1, grid=[(("GDXJ~GLD+SPY", k), h, q) for k in (1, 3) for h in (1, 3) for q in (0.7, 0.8)], src=SIG1),
    "C3_gunici_altin_GDX_donus": dict(und="GDX", sign=-1, grid=[("gi", 1, q) for q in (0.7, 0.8, 0.9)], src={"gi": gi}),
    "C4_platin5_GDX_donus": dict(und="GDX", sign=-1, grid=[(("PLATIN", "d5"), h, q) for h in (3, 5) for q in (0.7, 0.8)], src=FEAT3),
    "C5_asya_madenci_GLD": dict(und="GLD", sign=+1, grid=[(k, h, q) for k in (1, 5) for h in (3, 5) for q in (0.7, 0.8)], src=SIGA),
    "C5g_asya_madenci_GDX": dict(und="GDX", sign=+1, grid=[(k, h, q) for k in (1, 5) for h in (3, 5) for q in (0.7, 0.8)], src=SIGA),
}
allrows = []; chosen = {}; yearly = {}; extremes = {}
for cn, c in CANDS.items():
    best = None; grid_rows = []
    for key, h, q in c["grid"]:
        x = c["src"][key]
        pos = pos_from_signal(x, c["sign"], q)
        o = strat(d, pos, c["und"], h, "base", None, "2017-12-31")
        sh = o["ideal"]["sharpe"] if o["ideal"] else np.nan
        grid_rows.append(dict(cand=cn, key=str(key), h=h, q=q, is_sharpe_ideal=round(sh, 3), is_sharpe_long=round(o["long"]["sharpe"], 3) if o["long"] else None))
        if best is None or sh > best[0]: best = (sh, key, h, q)
    pd.DataFrame(grid_rows).to_csv(f"{OUT}/s6_grid_{cn}.csv", index=False)
    _, key, h, q = best; chosen[cn] = dict(key=str(key), h=h, q=q, und=c["und"], sign=c["sign"])
    x = c["src"][key]; pos = pos_from_signal(x, c["sign"], q)
    tab, yr, ext = full_report(d, pos, c["und"], h, cn)
    allrows.append(tab); yearly[cn] = yr; extremes[cn] = ext
    st = test("s6_strateji", f"s6_{cn}_secilen", x * c["sign"], R[c["und"]], h, f"{cn} IS-seçilen {key} h={h} q={q}", note="IS-seçilen konfigürasyon IC (tekrar)")
    chosen[cn].update({k: (round(float(st[k]), 3) if isinstance(st[k], (float, int, np.floating)) else st[k]) for k in ["ic", "t", "t_is", "t_oos", "t_22", "yrs_same_sign", "yrs"]})
    yv = fwd(R[c["und"]], h); xs = x * c["sign"]
    for a_, b_ in [("2008-01-01", "2012-12-31"), ("2013-01-01", "2017-12-31"), ("2018-01-01", "2021-12-31"), ("2022-01-01", "2024-12-31"), ("2025-01-01", "2026-12-31")]:
        r_ = sub_ic(xs, yv, h, a_, b_); chosen[cn][f"ic_{a_[:4]}_{b_[:4]}"] = (round(r_["ic"], 3) if np.isfinite(r_["ic"]) else None, round(r_["t"], 2) if np.isfinite(r_["t"]) else None)
    o = strat(d, pos, c["und"], h, "base"); chosen[cn]["trades_per_year_ideal"] = round(o["ideal"]["turnover_per_yr"] / 2, 1)
    print(cn, chosen[cn])
T = pd.concat(allrows)
T.to_csv(f"{OUT}/s6_strateji_ozet.csv", index=False)
pd.set_option("display.width", 260); pd.set_option("display.max_columns", 30)
print(T[["label", "cost", "period", "sh_ideal", "sh_ideal_dm", "sh_long", "sh_long_dm", "sh_long_inv", "sh_short_ideal", "sh_short_inv", "sh_bh", "ann_long", "ann_long_inv", "ann_bh", "expo_long", "turn_ideal"]].to_string())
for cn, yr in yearly.items():
    print(cn); print((yr * 100).round(1).T.to_string())
    yr.to_csv(f"{OUT}/s6_yillik_{cn}.csv")
json.dump(dict(chosen=chosen, extremes=extremes), open(f"{OUT}/s6_secim_uc.json", "w"), indent=1, default=str)
print(json.dumps(extremes, indent=0))
