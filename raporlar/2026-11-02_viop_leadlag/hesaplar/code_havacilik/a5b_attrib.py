"""A5b: COMBO sinyalinin atfı (hangi bacak çalışıyor?) + piyasa (XU100/XU030) kıyası + yıllık kırılım + rastgele-sinyal/sahte (placebo) kontrolü.
Çıktı: res/a5b_summary.txt"""
from h import *
from a5_backtest import zs, SG

if __name__ == "__main__":
    tv = {st: D(st) for st in STOCKS + ["XU100", "XU030"]}
    eu = zs(SG["EUAIR_X"]).clip(-3, 3); us = zs(SG["USAIR_X"]).clip(-3, 3); tu = zs(SG["TUR"]).clip(-3, 3)
    fx = R("TRY=X").where(R("TRY=X") != 0)
    sigs = {"COMBO": eu + us - tu, "AIR_only(eu+us)": eu + us, "minusTUR_only": -tu, "EU_only": eu, "US_only": us,
            "AIR_minus_STOXXSPX": zs(SG["EUAIR"]).clip(-3, 3) + zs(SG["USAIR"]).clip(-3, 3) - zs(SG["STOXX"]).clip(-3, 3) - zs(SG["SPX"]).clip(-3, 3),
            "USDTRY": zs(fx).clip(-3, 3), "COMBO+USDTRY": eu + us - tu + zs(fx).clip(-3, 3)}
    rows = []; yrs = []
    for nm, s in sigs.items():
        for st in STOCKS + ["XU100", "XU030"]:
            thr = 1.0
            r, pnl = ll.backtest(s.shift(1), tv[st]["intra"], cost_bps=8, mode="sign", thr=thr)
            rows.append({"sig": nm, "target": st, **{f"{p}_{k}": r[p].get(k, np.nan) for p in ["IS", "OOS"] for k in ["n", "mean_bps", "t", "sharpe"]}})
            if nm in ["COMBO", "AIR_only(eu+us)", "USDTRY"] and st in STOCKS:
                yrs.append({"sig": nm, "target": st, **r["by_year_bps"]})
    T = pd.DataFrame(rows)
    # placebo: sinyali 1 gün daha geç kullan (t-2 bilgisi) -> etkinin bayatlaması gerekir
    pl = []
    for st in STOCKS:
        for lag in [1, 2, 3]:
            r, _ = ll.backtest(sigs["COMBO"].shift(lag), tv[st]["intra"], cost_bps=8, mode="sign", thr=1.0)
            pl.append({"target": st, "signal_lag": lag, "IS_bps": r["IS"].get("mean_bps"), "IS_t": r["IS"].get("t"), "OOS_bps": r["OOS"].get("mean_bps"), "OOS_t": r["OOS"].get("t")})
    # yön ayrımı (long vs short)
    ls = []
    for st in STOCKS:
        s = sigs["COMBO"].shift(1); y = tv[st]["intra"]
        df = pd.concat([s.rename("s"), y.rename("y")], axis=1).dropna()
        for side, msk in [("long(s>1)", df.s > 1), ("short(s<-1)", df.s < -1), ("flat", df.s.abs() <= 1)]:
            for per, m2 in [("IS", df.index < SPLIT), ("OOS", df.index >= SPLIT)]:
                x = df.y[msk & m2]
                ls.append({"target": st, "side": side, "per": per, "n": len(x), "mean_intra_bps": 1e4 * x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan})
    txt = "ATIF (thr=1, maliyet 8 bps)\n" + T.round(2).to_string(index=False)
    txt += "\n\nPLACEBO (sinyal gecikmesi)\n" + pd.DataFrame(pl).round(2).to_string(index=False)
    txt += "\n\nYÖN AYRIMI (brüt gün-içi ortalama)\n" + pd.DataFrame(ls).round(2).to_string(index=False)
    txt += "\n\nYILLAR (bps/işlem net)\n" + pd.DataFrame(yrs).round(1).to_string(index=False)
    open(RES + "/a5b_summary.txt", "w").write(txt); T.to_csv(RES + "/a5b_attrib.csv", index=False)
    print("ok")
