"""Adim 4: (b) SHFE HRC (HC) / RB -> KRDMD (ve EREGL) zamanlama denetimi.
Sina gunluk bar (tarih t) = gece seansi (t-1 aksami 21:00-23:00 Pekin = 13:00-15:00 UTC t-1) + gunduz seansi (09:00-15:00 Pekin = 01:00-07:00 UTC t).
  -> 60 dk veriyle dogrulandi: gunluk o_t = gece seansi acilisi, c_t = 15:00 Pekin kapanisi.
Ana kontrat: t-1 gunu max OI (yalniz ileri). 60 dk barlar (Sina getFewMinLine, ~2023-08+) ana kontrat uzerinden eklenir.
Sinyaller (BIST gunu t; SHFE t gunu islem gormeli):
  FULL  = log c_t / c_{t-1}                (orijinal; 07:00 UTC t-1 -> 07:00 UTC t)
  NIGHT = log gece_kapanis / c_{t-1}       (07:00 -> 15:00 UTC t-1; BIST t-1 seansiyla ESZAMANLI kisim dahil)
  DAY   = log c_t / gece_kapanis           (15:00 UTC t-1 -> 07:00 UTC t; tamamen BIST t-1 kapanisi sonrasi, t acilisi oncesi)
  PRE   = log P(<=14:30 Pekin) / c_{t-1}   (-> 06:15 UTC t; BIST acilisindan 45 dk once bilinir)
  LAST  = log c_t / P(<=14:30 Pekin)       (06:15 -> 07:00 UTC; BIST acilis muzayedesiyle cakisan son dilim)
  Gunluk tam donem: GAPD = log o_t / c_{t-1} (07:00->13:00 UTC t-1), OCD = log c_t / o_t (13:00 UTC t-1 -> 07:00 UTC t).
Hedefler: KRDMD acilis->kapanis (gunluk); KRDMD 07:30->kapanis ve acilis->07:30 (h1, 2023-11-30+)."""
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a")
import vlib as V, numpy as np, pandas as pd
pd.set_option("display.width", 250)
OUT = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a/"
C = V.cal()

def intraday_signals(code):
    m = V.shfe_main(code)          # gun t: main (t-1 max OI), r_cc, r_gap, r_oc
    Cd, P, O, cols = V.shfe_contracts(code)
    rows = []
    cache = {}
    for t, nm in m["main"].items():
        if nm not in cache: cache[nm] = V.sina60(nm)
        h = cache[nm]
        if h is None: continue
        dd = Cd[nm].dropna()
        if t not in dd.index: continue
        i = dd.index.get_loc(t)
        if i == 0: continue
        tprev = dd.index[i - 1]
        # t gunune ait barlar: (tprev 15:00, t 15:00]
        lo = tprev + pd.Timedelta(hours=15); hi = t + pd.Timedelta(hours=15)
        b = h[(h.index > lo) & (h.index <= hi)]
        if len(b) < 3: continue
        night = b[(b.index.hour >= 20) | (b.index < t)]   # gece barlari (takvim gunu t'den once)
        day = b[(b.index >= t)]
        pre = day[day.index <= t + pd.Timedelta(hours=14, minutes=30)]
        if len(day) == 0 or len(pre) == 0: continue
        c_prev = dd.iloc[i - 1]; c_t = dd.iloc[i]
        # 60dk kapanisi gunluk kapanisla tutarli mi
        chk = abs(np.log(day["c"].iloc[-1] / c_t))
        rows.append({"d": t, "main": nm, "FULL": np.log(c_t / c_prev),
                     "NIGHT": np.log(night["c"].iloc[-1] / c_prev) if len(night) else np.nan,
                     "DAY": np.log(c_t / night["c"].iloc[-1]) if len(night) else np.nan,
                     "PRE": np.log(pre["c"].iloc[-1] / c_prev), "LAST": np.log(c_t / pre["c"].iloc[-1]), "chk": chk,
                     "pre_label": pre.index[-1].strftime("%H:%M")})
    X = pd.DataFrame(rows).set_index("d")
    return X

def daily_signals(code):
    m = V.shfe_main(code)
    return m[["r_cc", "r_gap", "r_oc"]].rename(columns={"r_cc": "FULLD", "r_gap": "GAPD", "r_oc": "OCD"})

def bist_h1_targets(sym):
    B = V.bist_daily(sym)
    h = V.rawd(sym, "h1").copy(); h["day"] = pd.DatetimeIndex(h["ldate"].values); h["hm"] = h.index.strftime("%H:%M")
    p0730 = h[h.hm == "06:30"].groupby("day")["c"].last().reindex(B.index)
    o_h1 = h[h.hm == "06:30"].groupby("day")["o"].last().reindex(B.index)
    T = pd.DataFrame(index=B.index)
    T["oc"] = B["intra"]; T["e0730"] = np.log(B["c"] / p0730); T["first30"] = np.log(p0730 / B["o"])
    T["ochk"] = 1e4 * np.log(o_h1 / B["o"])
    T["gap"] = B["gap"]; T["cc"] = B["cc"]
    return T

rows = []
def run(drv, sig, tgt, sname, tname, start=None, cost=10):
    df = pd.concat([sig.rename("s"), tgt.rename("y")], axis=1).dropna()
    if start: df = df[df.index >= start]
    if len(df) < 40: return
    c, t, n = V.zt(df.y, df.s); r, _ = V.bt(df.s, df.y, cost); r0, _ = V.bt(df.s, df.y, 0)
    rows.append({"driver": drv, "signal": sname, "target": tname, "start": str(df.index[0].date()), "end": str(df.index[-1].date()), "n": n, "corr": c, "t": t,
                 "gross_all": r0["ALL"].get("mean_bps"), "net10_all": r["ALL"].get("mean_bps"), "sh_all": r["ALL"].get("sharpe"), "bt_t_all": r["ALL"].get("t"),
                 "sh_IS": r["IS"].get("sharpe"), "net10_IS": r["IS"].get("mean_bps"), "sh_OOS": r["OOS"].get("sharpe"), "net10_OOS": r["OOS"].get("mean_bps")})

if __name__ == "__main__":
    for code in ["HC", "RB"]:
        X = intraday_signals(code); D = daily_signals(code)
        print(code, "60dk ornek:", X.index[0].date(), "->", X.index[-1].date(), "n", len(X), "| 60dk-gunluk kapanis uyumsuz (>1bp) oran:", round((X.chk > 1e-4).mean(), 3),
              "| PRE etiketi:", X.pre_label.value_counts().to_dict())
        X.to_csv(OUT + f"s04_{code}_intraday_signals.csv")
        # sadece BIST gunleri (SHFE t ile ayni tarih), taze
        X = X[X.index.isin(C)]; D = D[D.index.isin(C)]
        for stock in ["KRDMD.IS", "EREGL.IS"]:
            T = bist_h1_targets(stock)
            st = stock.split(".")[0]
            for s in ["FULLD", "GAPD", "OCD"]:
                run(code, D[s], T["oc"], s, st + "_oc[tum]")
                run(code, D[s].shift(1), T["oc"], s + "_lag1", st + "_oc[tum]") if s == "FULLD" else None
            for s in ["FULL", "NIGHT", "DAY", "PRE", "LAST"]:
                run(code, X[s], T["oc"], s, st + "_oc[60dk ornek]")
            for s in ["FULL", "DAY", "PRE"]:
                run(code, X[s], T["e0730"], s, st + "_0730->kap[h1]", "2023-11-30")
                run(code, X[s], T["first30"], s, st + "_acilis->0730[h1]", "2023-11-30")
                run(code, X[s], T["oc"], s, st + "_oc[h1 ornek]", "2023-11-30")
            if stock == "KRDMD.IS":
                print("KRDMD acilis kontrolu (h1 vs gunluk, bps):", T["ochk"].describe().round(1).to_dict())
    R = pd.DataFrame(rows); R.round(4).to_csv(OUT + "s04_shfe_timing.csv", index=False)
    print(R.round(3).to_string())
