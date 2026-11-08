"""Volatilite ailesi: ölçüm tablolarından doğan EK (post-hoc) testler. Bunlar önceden belirlenmedi; test sayısına eklenir.
  E1 'gergin bölge' : 0.95 <= VIX/VIX3M < 1.00 (eşikler hipotezler.csv VO02/VO03'ten; ayarlanmadı) -> SVXY long
  E2 'Pazartesi gün içi': Pazartesi (haftanın ilk işlem günü) açılışta SVXY al, aynı gün kapanışta sat
     (lib.trades: sinyal = haftanın son işlem günü, mod O1, h=1). Ayna: VXX.
Çalıştırma: python3 -I kod/ajan_volatilite/ek_testler.py
Çıktı: sonuclar/aile_volatilite/ek_testler.csv"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, pandas as pd
import vlib, lib

def last_day_of_week(idx):
    s = pd.Series(idx, index=idx)
    nxt = s.shift(-1)
    # sonraki işlem günü farklı ISO haftasındaysa bu gün haftanın son işlem günüdür
    wk = idx.isocalendar().week.values; yr = idx.isocalendar().year.values
    nwk = pd.Series(wk, index=idx).shift(-1); nyr = pd.Series(yr, index=idx).shift(-1)
    return pd.Series((nwk.values != wk) | (nyr.values != yr), index=idx) & nxt.notna()

def main(verbose=True):
    rows = []
    V = {"SVXY": (lib.load("SVXY"), None, True), "SVIX": (lib.load("SVIX"), None, True),
         "SVXY_EK": (vlib.stitched_svxy(), lib.load("SVXY"), True),
         "VEKIL_S05": (vlib.synth_proxy(-0.5), lib.load("SVXY"), False), "VEKIL_S1": (vlib.synth_proxy(-1.0), lib.load("SVIX"), False)}
    for vn, (df, cdf, ho) in V.items():
        x = vlib.ctx(df.index)
        sig = ((x["R3M"] >= 0.95) & (x["R3M"] < 1.00)).fillna(False)
        for mode in (["C0", "O1", "C1"] if ho else ["C0", "C1"]):
            for h in (1, 2, 3):
                s, tr = vlib.ev(df, sig, h, mode, cost_df=cdf); s.update({"test": "E1_gergin_bolge", "arac": vn}); rows.append(s)
    for vn in ["SVXY", "SVIX", "VXX", "VIXY", "UVXY", "VIXM"]:
        df = lib.load(vn)
        sig = last_day_of_week(df.index)
        s, tr = vlib.ev(df, sig, 1, "O1"); s.update({"test": "E2_pazartesi_gun_ici", "arac": vn}); rows.append(s)
        if vn in ("SVXY", "VXX") and verbose:
            oos = tr[tr.sig_date > lib.IS_END]
            g = oos["gross"]
            print(f"{vn} Pazartesi gün içi OOS: n={len(g)} ort={g.mean()*1e4:.1f} bp, medyan={g.median()*1e4:.1f}, "
                  f"%1-%99 kırpılmış ort={g.clip(g.quantile(.01), g.quantile(.99)).mean()*1e4:.1f}, en büyük 3: {(g.nlargest(3)*1e4).round(0).tolist()}")
            print("  yıllara göre brüt ort (bp):", (tr.groupby(tr.sig_date.dt.year)['gross'].mean() * 1e4).round(1).to_dict())
    R = pd.DataFrame(rows)
    cols = ["test", "arac", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "net_1000_bp", "net_10000_bp", "edge_bp", "t", "p", "win", "pf",
            "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp", "oos_t", "years_pos_frac", "maxdd", "worst_bp", "cost_bp", "first", "last"]
    R = R[cols]; R.to_csv(os.path.join(vlib.OUT, "ek_testler.csv"), index=False)
    if verbose:
        pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)
        print(R.round(2).to_string())
    return R

if __name__ == "__main__":
    main()
