"""Görev 4 ek: t5'te FDR'den geçen 'piyasa getirisi -> ertesi gün hisse (negatif katsayı)' bulgusunu işlem kuralına çevirip
maliyetli backtest (dayanak sentetik 2x, 9 hisse havuzu, 2016+; gerçek ETF kontrolü 2022+). Kurallar önceden sabit (ayar yok):
  LL1: QQQ 1 günlük getirisi z < -2 (lib.zret, 60 gün) -> 2x hisse ETF long
  LL2: SPY 1 günlük getirisi z < -2 -> 2x hisse ETF long
Çalıştırma: python3 -I kod/ajan_tek_hisse_kaldiracli/t5b_oncu_kural.py   Çıktı: oncu_kural_testleri.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import thk, lib, hrun

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
zq = lib.zret(lib.load("QQQ")["c"], 1); zs = lib.zret(lib.load("SPY")["c"], 1)
r1 = hrun.run("LL1_QQQ_z_lt_m2", lambda st, sdf: (zq < -2).reindex(sdf.index).fillna(False), thk.STOCKS, primary=("C0", 1), note="t5 öncü bulgusu -> kural")
r2 = hrun.run("LL2_SPY_z_lt_m2", lambda st, sdf: (zs < -2).reindex(sdf.index).fillna(False), thk.STOCKS, primary=("C0", 1), note="t5 öncü bulgusu -> kural")
R = pd.DataFrame(hrun.REG)
R.to_csv(os.path.join(thk.OUT, "oncu_kural_testleri.csv"), index=False)
cols = ["hipotez", "mode", "h", "n", "n_tarih", "mean_gross_bp", "mean_net_bp", "t", "edge_bp", "t_edge", "is_net_bp", "is_t", "oos_net_bp", "oos_t", "years_pos_frac", "hisse_pozitif"]
print(R[R.duzey == "havuz"][cols].round(2).to_string(index=False))
# gerçek ETF kontrolü (birincil ETF'ler)
for nm, z in (("LL1", zq), ("LL2", zs)):
    for m in ("C0", "O1"):
        df, _ = hrun.real_check(nm, lambda st, sdf, z=z: (z < -2).reindex(sdf.index).fillna(False), list(thk.PRIMARY.values()), m, 1)
        g = df[df.duzey == "gercek_havuz"].iloc[0]
        print(f"gerçek ETF {nm} {m} h1: n {g.n} tarih {g.n_tarih} net {g.mean_net_bp:.1f} t {g.t:.2f}")
