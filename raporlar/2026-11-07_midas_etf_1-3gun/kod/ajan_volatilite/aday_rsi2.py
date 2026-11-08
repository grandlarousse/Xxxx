"""Aday: kısa-vol ETF'sinde RSI(2) dibi + 200 günlük ortalama üstü (genel kütüphane: MR_rsi2_lt10_ust200).
Kural: t kapanışında RSI2(SVXY) < 10 ve SVXY kapanışı > SMA200(SVXY) -> SVXY long; çıkış h işlem günü sonra kapanışta.
Çalıştırma: python3 -I kod/ajan_volatilite/aday_rsi2.py
Çıktılar: sonuclar/aile_volatilite/aday_rsi2_ozet.csv, aday_rsi2_komsu.csv, aday_rsi2_islemler_SVXY.csv (ekrana da basar)

Araçlar: SVXY (2018-09+), SVIX (2022-03+), SVXY_EK (VIXY'den -0.5x sentetik 2017-07..2018-09 + SVXY),
VEKIL_S05 / VEKIL_S1 (VIX vade yapısı vekili, 2009-09+; yalnız C0/C1), ayna: VXX/VIXY'de RSI2>90 & < SMA200 (long VXX = beklenen negatif).
Not: RSI2 ve SMA200 ETF'nin kendi kapanışından -> 16:00 ET'de bilinir; C0'da kapanıştan dakikalar önceki fiyatla hesaplanmalı."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd
import vlib, lib

def sig_rsi2(df, thr=10, ma=200):
    c = df["c"]
    s = (lib.rsi(c, 2) < thr) & (c > lib.sma(c, ma))
    s.iloc[:ma] = False
    return s.fillna(False)

def sig_mirror(df, thr=90, ma=200):
    c = df["c"]
    s = (lib.rsi(c, 2) > thr) & (c < lib.sma(c, ma))
    s.iloc[:ma] = False
    return s.fillna(False)

def vehicles():
    return {
        "SVXY": (lib.load("SVXY"), None, True),
        "SVIX": (lib.load("SVIX"), None, True),
        "SVXY_EK": (vlib.stitched_svxy(), lib.load("SVXY"), True),
        "VEKIL_S05": (vlib.synth_proxy(-0.5), lib.load("SVXY"), False),
        "VEKIL_S1": (vlib.synth_proxy(-1.0), lib.load("SVIX"), False),
    }

def run(verbose=True):
    rows = []; trades_svxy = None
    for vn, (df, cdf, has_open) in vehicles().items():
        sig = sig_rsi2(df)
        if vn == "SVIX":   # SVIX'te 200 gün ısınma örneği çok kısaltır: SMA200 yerine dayanak SVXY'nin SMA200 filtresi
            sv = lib.load("SVXY")
            filt = (sv["c"] > lib.sma(sv["c"], 200)).reindex(df.index).fillna(False)
            sig = ((lib.rsi(df["c"], 2) < 10) & filt).fillna(False)
        for mode in (["C0", "O1", "C1"] if has_open else ["C0", "C1"]):
            for h in (1, 2, 3):
                s, tr = vlib.ev(df, sig, h, mode, cost_df=cdf, label="rsi2_lt10_ust200")
                s["arac"] = vn
                rows.append(s)
                if vn == "SVXY" and mode == "C0" and h == 2: trades_svxy = tr.copy()
    # ayna testi (uzun vol): beklenen negatif
    for vn in ["VXX", "VIXY"]:
        df = lib.load(vn); sig = sig_mirror(df)
        for mode in ["C0", "O1", "C1"]:
            for h in (1, 2, 3):
                s, tr = vlib.ev(df, sig, h, mode, label="ayna_rsi2_gt90_alt200"); s["arac"] = vn + "_ayna"; rows.append(s)
    R = pd.DataFrame(rows)
    cols = ["arac", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "net_1000_bp", "net_10000_bp", "edge_bp", "t", "p", "win", "pf",
            "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp", "oos_t", "years_pos_frac", "n_years", "maxdd", "worst_bp", "cost_bp", "first", "last"]
    R = R[cols]
    R.to_csv(os.path.join(vlib.OUT, "aday_rsi2_ozet.csv"), index=False)
    if trades_svxy is not None:
        trades_svxy.to_csv(os.path.join(vlib.OUT, "aday_rsi2_islemler_SVXY_C0h2.csv"), index=False)
    # komşu parametreler (SVXY_EK ve VEKIL_S05; IS = <=2021, OOS = 2022+), O1/C0/C1 h=2
    nb = []
    for vn in ["SVXY_EK", "VEKIL_S05"]:
        df, cdf, has_open = vehicles()[vn]
        for thr in (5, 10, 15, 20):
            for ma in (100, 200, 0):
                c = df["c"]
                s = lib.rsi(c, 2) < thr
                if ma: s = s & (c > lib.sma(c, ma))
                s = s.fillna(False); s.iloc[:200] = False
                for mode in (["C0", "O1", "C1"] if has_open else ["C0", "C1"]):
                    st, tr = vlib.ev(df, s, 2, mode, cost_df=cdf)
                    nb.append({"arac": vn, "rsi_esik": thr, "sma": ma, "mode": mode, "h": 2, "n": st["n"],
                               "net_bp": st.get("mean_net_bp"), "t": st.get("t"), "is_net_bp": st.get("is_net_bp"), "is_t": st.get("is_t"),
                               "oos_net_bp": st.get("oos_net_bp"), "oos_t": st.get("oos_t")})
    NB = pd.DataFrame(nb); NB.to_csv(os.path.join(vlib.OUT, "aday_rsi2_komsu.csv"), index=False)
    if verbose:
        pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)
        print("=== RSI2<10 & >SMA200: araç x mod x h ===")
        print(R.round(2).to_string())
        print("\n=== Komşu parametreler (h=2) ===")
        print(NB.round(2).to_string())
        if trades_svxy is not None:
            tr = trades_svxy
            print("\nSVXY C0 h2 yıllık net toplam (bp):")
            print((tr.groupby(tr.sig_date.dt.year)["net"].sum() * 1e4).round(0).to_string())
            print("Kuyruk dönemleri:", vlib.tail_report(tr))
            print("En kötü 5 işlem:"); print(tr.nsmallest(5, "net").to_string())
    return R, NB

if __name__ == "__main__":
    run()
