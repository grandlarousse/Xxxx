"""S3: Zamanlama denetimi.
 (1) Bileşenlerin gerçek kapanış saati (h1 son bar) ve günlük 'c' = son h1 bar kapanışı mı?
 (2) BIST h1 ilk bar (06:30-07:30 UTC) kapanışı ile giriş: intra_alt = log(c_günlük / c_ilkbar). Aynı pencerede açılış-girişi ile karşılaştırma.
Çıktı: res_s3_close_times.csv, res_s3_alt_entry.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v, numpy as np, pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
JP_AU = ["5411.T", "5401.T", "6301.T", "FMG.AX", "BHP.AX"]
# ---------- (1) kapanış saatleri ----------
rows = []
for s in JP_AU + ["^N225"]:
    h = v.raw(s, "h1").copy(); h["ld"] = pd.DatetimeIndex(h["ldate"].values)
    last = h.groupby("ld").apply(lambda x: pd.Series({"last_start": x.index[-1], "last_c": x["c"].iloc[-1]}))
    d = v.raw(s); dc = pd.Series(d["c"].values, index=pd.DatetimeIndex(d["ldate"].values))
    dc = dc[~dc.index.duplicated(keep="last")]
    last["daily_c"] = dc.reindex(last.index)
    last["eq"] = np.isclose(last["last_c"].astype(float), last["daily_c"].astype(float), rtol=5e-4)
    last["hm"] = pd.DatetimeIndex(last["last_start"]).strftime("%H:%M")
    last["per"] = np.where(last.index < pd.Timestamp("2024-11-05"), "<2024-11-05", ">=2024-11-05")
    last["mon"] = last.index.month
    for (per, hm), g in last.groupby(["per", "hm"]):
        rows.append({"sym": s, "period": per, "last_bar_start_utc": hm, "days": len(g), "daily_c_eq_lastbar": round(g["eq"].mean(), 3),
                     "months": ",".join(map(str, sorted(g["mon"].unique())))})
CT = pd.DataFrame(rows); CT = CT[CT.days >= 5]; CT.to_csv(os.path.join(v.OUT, "res_s3_close_times.csv"), index=False)
print(CT.to_string())

# ---------- (2) alternatif giriş ----------
comp = v.composite(JP_AU)
out = []
for st in ["EREGL.IS", "KRDMD.IS", "BRSAN.IS", "XU100.IS"]:
    h = v.raw(st, "h1").copy(); h["ld"] = pd.DatetimeIndex(h["ldate"].values)
    h = h[h.index.strftime("%H:%M") == "06:30"]  # ilk bar [06:30, 07:30) UTC -> kapanış ~07:30 UTC = 10:30 TSİ
    fb = pd.Series(h["c"].values, index=h["ld"].values); fb = fb[~fb.index.duplicated(keep="last")]
    fo = pd.Series(h["o"].values, index=h["ld"].values); fo = fo[~fo.index.duplicated(keep="last")]
    d = v.decomp(st)
    win = d[d.index >= fb.index.min()].copy()
    win["fb"] = fb.reindex(win.index); win["fo"] = fo.reindex(win.index)
    win["o_match"] = np.isclose(win["fo"], win["o"], rtol=1e-4)
    win["alt"] = np.log(win["c"] / win["fb"]); win["first30"] = np.log(win["fb"] / win["o"])
    win.loc[win["intra"].isna(), ["alt", "first30"]] = np.nan
    print(f"\n{st}: h1 penceresi {win.index.min().date()}..{win.index.max().date()}  gün={win['alt'].notna().sum()}  h1 ilk bar açılışı=günlük o oranı={win['o_match'].mean():.3f}")
    for tname in ["intra", "alt", "first30"]:
        c, t, n = v.corr_t(win[tname], comp)
        r = {"stock": st, "target": tname, "corr": c, "t_corr": t, "n_days": n}
        for cost in (0, 8, 15):
            res, pnl, pos = v.bt(comp, win[tname], cost=cost, mode="z", thr=1.0)
            # z-skoru uzun geçmişten gelmeli: sinyali tam tarihte hesaplayıp pencereye kes
            pos_full, _ = v.positions(comp, d["intra"], "z", 1.0)
            pw = pos_full.reindex(win.index).fillna(0); y = win[tname]
            p = (pw * y - cost / 1e4 * pw.abs())[(pw != 0) & y.notna()]
            m, tt, nn = v.nw_mean_t(p)
            r[f"bps_c{cost}"] = 1e4 * m; r[f"t_c{cost}"] = tt; r["n_trades"] = nn
        out.append(r)
        print(f"  {tname:8s} corr={c:.3f} (t {t:.2f}, n {n}) | |z|>1 brüt {r['bps_c0']:.1f} bps (t {r['t_c0']:.2f}) | 8bps {r['bps_c8']:.1f} | 15bps {r['bps_c15']:.1f} (t {r['t_c15']:.2f}) n_işlem={r['n_trades']}")
A = pd.DataFrame(out); A.to_csv(os.path.join(v.OUT, "res_s3_alt_entry.csv"), index=False)
