"""İşlenebilirlik taraması + veri kalitesi.
Çıktı: sonuclar/tarama.csv, sonuclar/veri_kalitesi.csv"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import lib, universe

LEV = {  # nominal kaldıraç (işaretli)
 "TQQQ":3,"SQQQ":-3,"UPRO":3,"SPXU":-3,"SPXL":3,"SPXS":-3,"SSO":2,"SDS":-2,"QLD":2,"QID":-2,"UDOW":3,"SDOW":-3,
 "TNA":3,"TZA":-3,"SH":-1,"PSQ":-1,"URTY":3,"SRTY":-3,"SOXL":3,"SOXS":-3,"TECL":3,"TECS":-3,"FAS":3,"FAZ":-3,
 "LABU":3,"LABD":-3,"ERX":2,"ERY":-2,"GUSH":2,"DRIP":-2,"NAIL":3,"DFEN":3,"FNGU":3,"FNGD":-3,"CURE":3,"RETL":3,"UTSL":3,
 "NVDL":2,"TSLL":2,"MSTU":2,"CONL":2,"NVDU":2,"TSLQ":-1,"NVDS":-1.5,"AAPU":2,"AMZU":2,"METU":2,"MSFU":2,"GGLL":2,
 "UGL":2,"GLL":-2,"AGQ":2,"ZSL":-2,"NUGT":2,"DUST":-2,"JNUG":2,"JDST":-2,"UCO":2,"SCO":-2,"BOIL":2,"KOLD":-2,
 "TMF":3,"TMV":-3,"TBT":-2,"UBT":2,"YCS":-2,"YCL":2,"EUO":-2,"ULE":2,"UVXY":1.5,"SVXY":-0.5,"UVIX":2,"SVIX":-1,
 "BITX":2,"BITI":-1,"ETHU":2,"SBIT":-2,"BITU":2,"YINN":3,"YANG":-3,"EDC":3,"EDZ":-3,"EURL":3,"BRZU":2,"INDL":2,
 "MEXX":3,"KORU":3,"CHAU":2,"CWEB":2,
}

def main():
    mt = lib.meta()
    rows = []; dq = []
    for sym in lib.available():
        df = lib.load(sym)
        if len(df) < 60: continue
        r = df["c"].pct_change()
        t = df.tail(252)
        rt = t["c"].pct_change()
        gap = (t["o"] / t["c"].shift(1) - 1).abs()
        r3 = (t["c"].shift(-3) / t["c"] - 1).abs()
        dv = float(np.nanmedian(t["dv"]))
        sp = lib.spread_bp_tier(df); cost = lib.cost_bp(df)
        vol_d = float(rt.std() * 1e4)
        m = mt.get(sym, {})
        rows.append({
            "sym": sym, "cat": universe.CAT.get(sym), "name": m.get("name"), "exchange": m.get("exchange"),
            "first": str(df.index[0].date()), "n": len(df), "price": float(df["raw_c"].iloc[-1]),
            "med_dollar_vol_m": dv / 1e6, "spread_bp": sp, "cost_rt_bp": cost,
            "vol_1d_bp": vol_d, "ann_vol": float(rt.std() * math.sqrt(252)),
            "med_abs_1d_bp": float(rt.abs().median() * 1e4), "med_abs_3d_bp": float(r3.median() * 1e4),
            "med_abs_gap_bp": float(gap.median() * 1e4), "gap_share": float((gap ** 2).sum() / (rt ** 2).sum()) if (rt ** 2).sum() > 0 else np.nan,
            "pct_days_gt2pct": float((rt.abs() > 0.02).mean()), "worst_1d_1y": float(rt.min()),
            "lev": LEV.get(sym, 1), "cost_over_1d_vol": cost / vol_d if vol_d > 0 else np.nan,
            "ret_1y": float(t["c"].iloc[-1] / t["c"].iloc[0] - 1),
        })
        # veri kalitesi: aşırı hareketler
        sd = r.rolling(60).std().shift(1)
        big = r[(r.abs() > 0.25) | ((r.abs() > 8 * sd) & (r.abs() > 0.08))]
        for d, v in big.items():
            dq.append({"sym": sym, "date": str(d.date()), "ret": float(v), "z": float(v / sd.get(d, np.nan)) if sd.get(d, np.nan) else np.nan,
                       "raw_c_prev": float(df["raw_c"].shift(1).get(d)), "raw_c": float(df["raw_c"].get(d))})
        # ham OHLC tutarsızlığı
        raw = pd.read_parquet(os.path.join(lib.DATA, "etf", sym + ".parquet"))
        bad_o = int(((raw["o"] <= 0) | raw["o"].isna()).sum())
        if bad_o: dq.append({"sym": sym, "date": "NA", "ret": np.nan, "z": np.nan, "raw_c_prev": np.nan, "raw_c": np.nan, "note": f"bozuk açılış {bad_o} gün"})
    out = pd.DataFrame(rows).sort_values(["cat", "med_dollar_vol_m"], ascending=[True, False])
    os.makedirs(os.path.join(lib.ROOT, "sonuclar"), exist_ok=True)
    out.to_csv(os.path.join(lib.ROOT, "sonuclar", "tarama.csv"), index=False)
    pd.DataFrame(dq).to_csv(os.path.join(lib.ROOT, "sonuclar", "veri_kalitesi.csv"), index=False)
    print(out.shape, len(dq))

if __name__ == "__main__":
    main()
