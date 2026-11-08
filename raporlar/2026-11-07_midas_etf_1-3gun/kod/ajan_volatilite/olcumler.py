"""Volatilite ailesi: ölçüm tipi hipotezler (VO02 kuyruk, VO03 koşulsuz kayıp, VO06 kaldıraç kaybı) + hafta günü ayrışımı.
Çalıştırma: python3 -I kod/ajan_volatilite/olcumler.py
Çıktılar: sonuclar/aile_volatilite/olcum_*.csv (ekrana da basar)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd
import vlib, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)

def fwd(c, h):
    return c.shift(-h) / c - 1

def tstat(x):
    x = pd.Series(x).dropna()
    return x.mean() / (x.std(ddof=1) / math.sqrt(len(x))) if len(x) > 2 else np.nan

def nw_t_mean(x, lags):
    """Örtüşen h-günlük getiriler için Newey-West t (ortalama)."""
    x = pd.Series(x).dropna().values; n = len(x)
    if n < 10: return np.nan
    e = x - x.mean(); s = (e @ e) / n
    for l in range(1, lags + 1):
        s += 2 * (1 - l / (lags + 1)) * (e[l:] @ e[:-l]) / n
    return x.mean() / math.sqrt(s / n)

def vo02_vo03():
    rows = []
    for sym in ["SVXY", "SVIX", "VXX", "VIXY", "UVXY", "UVIX", "VIXM", "SVXY_EK", "VEKIL_S05", "VEKIL_L1"]:
        if sym == "SVXY_EK": df = vlib.stitched_svxy()
        elif sym == "VEKIL_S05": df = vlib.synth_proxy(-0.5)
        elif sym == "VEKIL_L1": df = vlib.synth_proxy(1.0)
        else: df = lib.load(sym)
        x = vlib.ctx(df.index)
        for h in (1, 3):
            f = fwd(df["c"], h)
            for nm, m in [("tum", pd.Series(True, index=df.index)), ("R3M<0.95", x["R3M"] < 0.95),
                          ("0.95<=R3M<1", (x["R3M"] >= 0.95) & (x["R3M"] < 1.0)), ("R3M>=1", x["R3M"] >= 1.0)]:
                y = f[m.fillna(False)].dropna()
                if len(y) < 10: continue
                rows.append({"arac": sym, "h": h, "kosul": nm, "n_gun": len(y), "ort_bp": y.mean() * 1e4,
                             "t_NW": nw_t_mean(y, h), "std_bp": y.std() * 1e4, "q05_bp": y.quantile(0.05) * 1e4,
                             "q01_bp": y.quantile(0.01) * 1e4, "en_kotu_bp": y.min() * 1e4, "en_iyi_bp": y.max() * 1e4,
                             "en_kotu_tarih": str(y.idxmin().date())})
    R = pd.DataFrame(rows)
    R.to_csv(os.path.join(vlib.OUT, "olcum_vo02_vo03_rejim.csv"), index=False)
    print("=== VO02/VO03: rejime göre ileri h-gün kapanış-kapanış getirisi (örtüşen; t Newey-West) ===")
    print(R.round(1).to_string())
    return R

def vo06():
    rows = []
    vxx = lib.load("VXX")["c"]
    for sym, k in [("UVXY", 1.5), ("UVIX", 2.0), ("SVXY", -0.5), ("SVIX", -1.0), ("VIXY", 1.0)]:
        c = lib.load(sym)["c"]
        idx = c.index.intersection(vxx.index)
        c = c.reindex(idx); v = vxx.reindex(idx)
        sg2 = np.log(v).diff().rolling(20).var()
        for h in (1, 2, 3):
            e = fwd(c, h) - k * fwd(v, h)
            pred = 0.5 * (k - k * k) * h * sg2   # Cheng-Madhavan: e ≈ (k - k^2)/2 * h * σ²  (günlük)
            d = pd.DataFrame({"e": e, "pred": pred}).dropna()
            rows.append({"arac": sym, "k": k, "h": h, "n": len(d), "ort_e_bp": d["e"].mean() * 1e4, "t_NW": nw_t_mean(d["e"], h),
                         "ort_tahmin_bp": d["pred"].mean() * 1e4, "medyan_e_bp": d["e"].median() * 1e4,
                         "yuksek_vol_ort_e_bp": d.loc[d["pred"].abs() > d["pred"].abs().quantile(0.8), "e"].mean() * 1e4})
    R = pd.DataFrame(rows)
    R.to_csv(os.path.join(vlib.OUT, "olcum_vo06_kaldirac.csv"), index=False)
    print("\n=== VO06: kaldıraç/ters ürün sapması e_h = r_ETF(h) - k*r_VXX(h) ===")
    print(R.round(1).to_string())
    return R

def hafta_gunu():
    rows = []
    for sym in ["SVXY", "SVIX", "VXX", "VIXM"]:
        df = lib.load(sym)
        ovn = df["o"] / df["c"].shift(1) - 1; intr = df["c"] / df["o"] - 1; cc = df["c"].pct_change()
        for dname, dw in zip(["Pzt", "Sal", "Car", "Per", "Cum"], range(5)):
            m = df.index.dayofweek == dw
            for part, s in [("gece", ovn), ("gun_ici", intr), ("kapanis_kapanis", cc)]:
                for per, pm in [("tum", np.ones(len(df), bool)), ("IS", df.index <= lib.IS_END), ("OOS", df.index > lib.IS_END)]:
                    y = s[m & pm].dropna()
                    if len(y) < 20: continue
                    rows.append({"arac": sym, "gun": dname, "parca": part, "donem": per, "n": len(y), "ort_bp": y.mean() * 1e4, "t": tstat(y)})
    R = pd.DataFrame(rows)
    R.to_csv(os.path.join(vlib.OUT, "olcum_hafta_gunu.csv"), index=False)
    p = R[R.arac.isin(["SVXY", "VXX"])].pivot_table(index=["arac", "gun"], columns=["parca", "donem"], values="ort_bp")
    print("\n=== Hafta günü ayrışımı (ort bp; gece = önceki kapanış->açılış) ===")
    print(p.round(1).to_string())
    pt = R[R.arac.isin(["SVXY", "VXX"])].pivot_table(index=["arac", "gun"], columns=["parca", "donem"], values="t")
    print(pt.round(1).to_string())
    return R

def tail_table():
    rows = []
    for sym in vlib.FAM:
        df = lib.load(sym)
        for h in (1, 2, 3):
            w, d = vlib.worst_hday(df, h)
            rows.append({"arac": sym, "h": h, "en_kotu_bp": w, "tarih": d})
        for k, (a, b) in vlib.TAIL.items():
            seg = df.loc[a:b, "c"]
            if len(seg) > 1:
                r = seg.pct_change()
                rows.append({"arac": sym, "h": "donem:" + k, "en_kotu_bp": r.min() * 1e4, "tarih": str(r.idxmin().date()),
                             "donem_toplam_bp": (seg.iloc[-1] / seg.iloc[0] - 1) * 1e4, "donem_maxdd": float((seg / seg.cummax() - 1).min())})
        dd = (df["c"] / df["c"].cummax() - 1).min()
        rows.append({"arac": sym, "h": "al_tut_maxdd", "en_kotu_bp": dd * 1e4, "tarih": str((df["c"] / df["c"].cummax() - 1).idxmin().date())})
    R = pd.DataFrame(rows)
    R.to_csv(os.path.join(vlib.OUT, "olcum_kuyruk.csv"), index=False)
    print("\n=== Kuyruk tablosu (ETF'nin kendi en kötü 1-3 günlük getirisi ve olay dönemleri) ===")
    print(R.round(1).to_string())
    return R

if __name__ == "__main__":
    vo02_vo03(); vo06(); hafta_gunu(); tail_table()
