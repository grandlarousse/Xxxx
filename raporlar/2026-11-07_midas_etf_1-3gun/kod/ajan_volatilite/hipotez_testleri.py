"""Volatilite ailesi: önceden belirlenmiş hipotezlerin testi (parametre taraması YOK; eşikler literatür/yönlendirme).
Çalıştırma: python3 -I kod/ajan_volatilite/hipotez_testleri.py
Çıktı: sonuclar/aile_volatilite/hipotez_testleri.csv (+ ekranda özet)

Araçlar:
  gerçek ETF'ler: SVXY, SVIX (kısa vol, long işlem), VXX, VIXY, UVXY, UVIX, VIXM (uzun vol)
  SVXY_EK   : 2017-07..2018-09 arası VIXY'den -0.5x sentetik + gerçek SVXY (Şubat 2018'i bugünkü yapıyla içerir)
  VEKIL_S05 / VEKIL_S1 / VEKIL_L1 : VIX vade yapısından türetilmiş kısa vade endeks vekili (2009-09+), -0.5x/-1x/+1x;
              açılış verisi yok -> yalnız C0 ve C1. Katsayılar yalnız 2017-07..2021 VIXY'ye uyduruldu.
Sinyaller t kapanışında bilinir (VIX 16:15 ET -> C0 hafif iyimser)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd
import vlib, lib

def signals(x, df):
    """x: ctx (df.index'e hizalı). df: işlem aracının fiyatı (yalnız fiyat tabanlı sinyaller için)."""
    R, R9, V = x["R3M"], x["R9D"], x["VIX"]
    S = {
        "H_kont09": R < 0.90,
        "H_VO01_kont09_vixaltSMA10": (R < 0.90) & (V < x["VIX_SMA10"]),
        "H_backw100": R >= 1.00,
        "H_backw105": R >= 1.05,
        "H_VO04_backw_donus": (R.shift(1) >= 1.00) & (R < 1.00),
        "H_rejim_backw_giris": (R.shift(1) < 1.00) & (R >= 1.00),
        "H_9d_kont090": R9 < 0.90,
        "H_9d_backw100": R9 > 1.00,
        "H_vix_sicrama15": x["VIX_chg"] >= 0.15,
        "H_vix_sicrama20": x["VIX_chg"] >= 0.20,
        "H_vix_gerilme120": V >= 1.20 * x["VIX_SMA10"],
        "H_vvix_gerilme110": x["VVIX"] >= 1.10 * x["VVIX_SMA10"],
        "H_vvix_sicrama10": x["VVIX_chg"] >= 0.10,
    }
    return {k: v.fillna(False).astype(bool) for k, v in S.items()}

# Hangi sinyal hangi yönde test edilir (önceden belirlendi): 'S' = kısa vol aracı long (SVXY/SVIX), 'L' = uzun vol aracı long
DIR = {
    "H_kont09": ["S"], "H_VO01_kont09_vixaltSMA10": ["S"], "H_backw100": ["S", "L"], "H_backw105": ["L"],
    "H_VO04_backw_donus": ["S"], "H_rejim_backw_giris": ["L"], "H_9d_kont090": ["S"], "H_9d_backw100": ["S", "L"],
    "H_vix_sicrama15": ["S", "L"], "H_vix_sicrama20": ["S", "L"], "H_vix_gerilme120": ["S", "L"],
    "H_vvix_gerilme110": ["S"], "H_vvix_sicrama10": ["S"],
}
EXIT_R1 = {"H_VO01_kont09_vixaltSMA10", "H_kont09", "H_9d_kont090"}   # erken çıkış: VIX/VIX3M >= 1.00

def vehicles():
    V = {}
    for s in ["SVXY", "SVIX"]: V[s] = ("S", lib.load(s), None, True)
    for s in ["VXX", "VIXY", "UVXY", "UVIX", "VIXM"]: V[s] = ("L", lib.load(s), None, True)
    V["SVXY_EK"] = ("S", vlib.stitched_svxy(), lib.load("SVXY"), True)
    V["VEKIL_S05"] = ("S", vlib.synth_proxy(-0.5), lib.load("SVXY"), False)
    V["VEKIL_S1"] = ("S", vlib.synth_proxy(-1.0), lib.load("SVIX"), False)
    V["VEKIL_L1"] = ("L", vlib.synth_proxy(1.0), lib.load("VXX"), False)
    return V

def main():
    rows = []
    V = vehicles()
    for vn, (side, df, cdf, has_open) in V.items():
        x = vlib.ctx(df.index)
        S = signals(x, df)
        ex = (x["R3M"] >= 1.00).fillna(False)
        modes = ["C0", "O1", "C1"] if has_open else ["C0", "C1"]
        for sn, sig in S.items():
            if side not in DIR[sn]: continue
            for mode in modes:
                for h in (1, 2, 3):
                    s, tr = vlib.ev(df, sig, h, mode, cost_df=cdf, label=sn)
                    s.update({"arac": vn, "taraf": side, "sig": sn, "exit": "sabit", "n_sig_days": int(sig.sum())})
                    rows.append(s)
                if sn in EXIT_R1:
                    s, tr = vlib.ev(df, sig, 3, mode, exit_sig=ex, cost_df=cdf, label=sn)
                    s.update({"arac": vn, "taraf": side, "sig": sn, "exit": "R3M>=1_max3", "n_sig_days": int(sig.sum())})
                    rows.append(s)
    # VO05: backwardation >= 1.05 -> SPY/QQQ long (aile hipotezi, araç aile dışı)
    for vn in ["SPY", "QQQ"]:
        df = lib.load(vn); x = vlib.ctx(df.index)
        sig = (x["R3M"] >= 1.05).fillna(False)
        for mode in ["C0", "O1", "C1"]:
            for h in (1, 2, 3):
                s, tr = vlib.ev(df, sig, h, mode, label="VO05")
                s.update({"arac": vn, "taraf": "endeks", "sig": "H_VO05_backw105_endeks", "exit": "sabit", "n_sig_days": int(sig.sum())})
                rows.append(s)
    R = pd.DataFrame(rows)
    real = R["arac"].isin(vlib.FAM + ["SPY", "QQQ"])
    R["fdr10_gercek"] = False
    R.loc[real, "fdr10_gercek"] = lib.bh_fdr(R.loc[real, "p"].values, 0.10)
    R["fdr10_tum"] = lib.bh_fdr(R["p"].values, 0.10)
    cols = ["arac", "taraf", "sig", "mode", "h", "exit", "n", "mean_gross_bp", "mean_net_bp", "net_1000_bp", "net_10000_bp",
            "edge_bp", "t", "t_edge", "p", "win", "pf", "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp", "oos_t",
            "years_pos_frac", "maxdd", "worst_bp", "cost_bp", "first", "last", "n_sig_days", "fdr10_gercek", "fdr10_tum"]
    R = R[cols]
    R.to_csv(os.path.join(vlib.OUT, "hipotez_testleri.csv"), index=False)
    print(f"Toplam test: {len(R)}  (gerçek ETF+SPY/QQQ: {real.sum()}, vekil/sentetik: {(~real).sum()})")
    print(f"BH-FDR q=0.10 geçen (gerçek ETF kümesi içinde): {R['fdr10_gercek'].sum()}, tüm küme: {R['fdr10_tum'].sum()}")
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 500)
    show = ["arac", "sig", "mode", "h", "exit", "n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac", "maxdd", "worst_bp", "fdr10_gercek"]
    pos = R[(R["mean_net_bp"] > 0) & (R["t"] >= 2)]
    print("\nNet>0 ve t>=2 olanlar:"); print(pos[show].round(2).to_string())
    print("\nFDR (gerçek) geçenler:"); print(R[R["fdr10_gercek"]][show].round(2).to_string())

if __name__ == "__main__":
    main()
