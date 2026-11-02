"""A4: Backtestler (IS 2014-2020 / OOS 2021-2026, maliyet 8 ve 15 bps gidiş-dönüş) + TRALT olay çalışması + yıllık korelasyonlar.
Sinyaller pozisyondan ÖNCE bilinir: ABD/Avrupa kapanışı t-1 (BIST açılışı t'den önce), Japonya/Avustralya kapanışı t (06:00-06:30 UTC < BIST sürekli işlem 07:00 UTC).
Hedef: intra_t (açılış->kapanış). 'hedged' = intra_t - beta*XU100 intra_t (hisseye özgü kısım; beta tam dönem, küçük look-ahead -> yalnız atıf amaçlı).
Çıktı: res/bt.csv, res/events.csv, res/byyear.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mh, ll, pandas as pd, numpy as np

def z(r):  # geçmiş pencere z-skoru (look-ahead yok)
    mu = r.rolling(250, min_periods=60).mean().shift(1); sd = r.rolling(250, min_periods=60).std().shift(1)
    return (r - mu) / sd
def comp(syms, lag):
    zs = [z(mh.R(s).where(mh.R(s) != 0)).shift(lag) for s in syms]
    return pd.concat(zs, axis=1).mean(axis=1, skipna=True)
def hedged(stock):
    a = mh.D(stock)["intra"]; m = mh.D("XU100")["intra"]
    df = pd.concat([a, m], axis=1).dropna(); b = np.polyfit(df.iloc[:, 1], df.iloc[:, 0], 1)[0]
    return a - b * m

EU_STEEL = ["MT.AS", "SSAB-A.ST", "VOE.VI", "SZG.DE", "AAL.L"]
JP_AU = ["5411.T", "5401.T", "6301.T", "FMG.AX", "BHP.AX"]
TESTS = [
 ("B1 GC=F(t-1) -> TRALT intra", lambda: mh.R("GC=F").where(mh.R("GC=F") != 0).shift(1), "TRALT"),
 ("B1b SI=F(t-1) -> TRALT intra", lambda: mh.R("SI=F").where(mh.R("SI=F") != 0).shift(1), "TRALT"),
 ("B1c NEM(t-1) -> TRALT intra", lambda: mh.R("NEM").where(mh.R("NEM") != 0).shift(1), "TRALT"),
 ("B2 AvrupaÇelik(t-1) -> EREGL intra", lambda: comp(EU_STEEL, 1), "EREGL"),
 ("B2b AvrupaÇelik(t-1) -> KRDMD intra", lambda: comp(EU_STEEL, 1), "KRDMD"),
 ("B3 JP/AU açılış-öncesi(t) -> EREGL intra", lambda: comp(JP_AU, 0), "EREGL"),
 ("B3b JP/AU açılış-öncesi(t) -> KRDMD intra", lambda: comp(JP_AU, 0), "KRDMD"),
 ("B4 SLX(t-1) -> EREGL intra", lambda: mh.R("SLX").where(mh.R("SLX") != 0).shift(1), "EREGL"),
 ("B4b ABDçelik NUE/STLD/CLF/MT(t-1) -> EREGL intra", lambda: comp(["NUE", "STLD", "CLF", "MT"], 1), "EREGL"),
 ("B5 TS(t-1) -> BRSAN intra", lambda: mh.R("TS").where(mh.R("TS") != 0).shift(1), "BRSAN"),
 ("B6 TRALT cc(t-1) -> TRMET intra (ters işaret)", lambda: -mh.R("TRALT").shift(1), "TRMET"),
 ("B7 TIO=F(t-1) -> EREGL intra", lambda: mh.R("TIO=F").where(mh.R("TIO=F") != 0).shift(1), "EREGL"),
]
if __name__ == "__main__":
    rows = []
    for name, sigf, st in TESTS:
        sig = sigf()
        for tgt_name, tgt in [("intra", mh.D(st)["intra"]), ("hedged", hedged(st))]:
            for cost in (8, 15):
                for mode, thr in [("sign", 0.0), ("z", 1.0)]:
                    s_ = sig if mode == "sign" or "comp" in name else sig
                    res, pnl = ll.backtest(s_.reindex(tgt.index), tgt, cost_bps=cost, mode=mode, thr=thr)
                    r = {"test": name, "stock": st, "target": tgt_name, "cost": cost, "mode": f"{mode}{thr}"}
                    for k in ("IS", "OOS"):
                        for f in ("n", "mean_bps", "t", "sharpe", "hit"): r[f"{k}_{f}"] = res[k].get(f, np.nan)
                    yb = res["by_year_bps"]; r["yrs_pos"] = f"{sum(v > 0 for v in yb.values())}/{len(yb)}"
                    r["by_year"] = ";".join(f"{k}:{v}" for k, v in yb.items())
                    rows.append(r)
    B = pd.DataFrame(rows); B.to_csv(os.path.join(mh.RES, "bt.csv"), index=False)
    # yıllık korelasyonlar
    yr = {}
    for st, d in [("TRALT", "GC=F"), ("TRMET", "GC=F"), ("TRMET", "TRALT"), ("EREGL", "MT.AS"), ("EREGL", "TIO=F"), ("KRDMD", "EREGL"), ("BRSAN", "TS")]:
        a = mh.R(st); b = mh.R(d); b = b.where(b != 0)
        w = pd.concat([mh.weekly(a), mh.weekly(b)], axis=1).dropna()
        yr[f"{st}~{d}(haftalık)"] = w.groupby(w.index.year).apply(lambda x: x.iloc[:, 0].corr(x.iloc[:, 1]) if len(x) > 20 else np.nan)
    Y = pd.DataFrame(yr).round(2); Y.to_csv(os.path.join(mh.RES, "byyear.csv"))
    # TRALT/TRMET olay çalışması: XU100'e göre anormal getiri (kümülatif log), [-1,+1], [0,+20], ve altına göre (GC=F) piyasa-altın modeli
    EV = {"2015-09-01 Koza-İpek baskını": "2015-09-01", "2015-10-27 kayyum ataması": "2015-10-27", "2016-09-01 TMSF kayyum": "2016-09-01",
          "2024-11-20 birleşme planı": "2024-11-20", "2025-11-24 isim/kod değişikliği (TRALT/TRMET)": "2025-11-24",
          "2025-03-19 İmamoğlu şoku": "2025-03-19"}
    erows = []
    for st in ("TRALT", "TRMET"):
        a = mh.R(st); m = mh.R("XU100"); g = mh.R("GC=F")
        ab = (a - m).dropna()
        for k, d in EV.items():
            d = pd.Timestamp(d); idx = ab.index
            i0 = idx.searchsorted(d)
            if i0 >= len(idx) or i0 < 5: continue
            w1 = ab.iloc[max(i0 - 1, 0): i0 + 2].sum(); w20 = ab.iloc[i0: i0 + 21].sum()
            raw20 = a.reindex(idx).iloc[i0: i0 + 21].sum(); g20 = g.reindex(idx).iloc[i0: i0 + 21].sum()
            sd = ab.iloc[max(0, i0 - 260): i0 - 10].std()
            erows.append({"stock": st, "event": k, "date": idx[i0].date(), "car_m1p1_pct": 100 * w1, "car_0_20_pct": 100 * w20, "raw_0_20_pct": 100 * raw20,
                          "gold_0_20_pct": 100 * g20, "z_m1p1": w1 / (sd * np.sqrt(3)), "z_0_20": w20 / (sd * np.sqrt(21))})
    E = pd.DataFrame(erows); E.to_csv(os.path.join(mh.RES, "events.csv"), index=False)
    print("bt", len(B), "events", len(E))
