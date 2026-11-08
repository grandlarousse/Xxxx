"""Tarım / geniş emtia ve lead-lag ek testleri.
  * CANE <- petrol (leadlag_sweep'te FDR geçen tek gecikmeli öncü): işlem kuralına çevirip maliyetli backtest.
    Mekanizma adayı: ICE şeker 11 vadelisi 13:00 ET'de kapanır; ETF 16:00 ET kapanışı sonrası petrol hareketini ertesi gün yakalar.
  * XOP/XLE <- UNG (sweep'te |t|~2, FDR yok): kurala çevirme.
  * Tarım ETF'leri için petrolün kendi gecikmesine EK katkısı (NW regresyon, kendi getirisi kontrollü).
Çalıştırma: python3 -I kod/ajan_enerji_tarim/h_tarim_leadlag.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak as O, lib

pd.set_option("display.width", 250)
idx = lib.load("SPY").index
R = {s: O.logret(s).reindex(idx) for s in ["CANE", "DBA", "CORN", "WEAT", "SOYB", "BNO", "USO", "USL", "XLE", "XOP", "UNG", "SPY", "PDBC"]}
res, reg_rows = [], []

def z1(s, n=60):
    r = R[s]; return r / r.rolling(n).std()

# 1) CANE <- BNO: büyük petrol yükselişi günü kapanışında CANE long
zb = z1("BNO")
res.append(O.grid("LL_CANE_BNOz1", "CANE", zb >= 1.0, "z1(BNO)>=+1 -> CANE long", hs=(1,)))
res.append(O.grid("LL_CANE_BNOz1n", "CANE", zb <= -1.0, "z1(BNO)<=-1 -> CANE long (beklenen -)", hs=(1,), modes=("C0",), sign=-1))
# 2) XOP <- UNG
zu = z1("UNG")
res.append(O.grid("LL_XOP_UNGz2", "XOP", zu >= 2.0, "z1(UNG)>=+2 -> XOP long", hs=(1,)))
# 3) tarım ETF'leri: fwd1 ~ own + USO + SPY (NW)
for T in ["CANE", "DBA", "CORN", "WEAT", "SOYB"]:
    for L in ["USO", "SPY"]:
        y = O.fwd(R[T], 1)
        d = pd.DataFrame({"y": y, "own": R[T], "x": R[L]}).dropna()
        for nm, m in (("tum", np.ones(len(d), bool)), ("is", d.index <= lib.IS_END), ("oos", d.index > lib.IS_END)):
            dd = d[m]
            b, t = O.nw_t(dd["y"].values, np.column_stack([np.ones(len(dd)), dd["own"].values, dd["x"].values]), 1)
            reg_rows.append({"hedef": T, "oncu": L, "donem": nm, "n": len(dd), "b": b[2], "t": t[2], "bp_per_sd": b[2] * dd["x"].std() * 1e4,
                             "maliyet_bp": O.cost(T)})
            if nm == "tum":
                O.REG.append({"hyp": "LL_tarim_reg", "sym": T, "desc": f"fwd1 ~ own + {L}", "mode": "-", "h": 1, "kind": "regresyon",
                              "sign": 0, "n": len(dd), "t": t[2], "p1": O.p_one(abs(t[2]), len(dd), +1) * 2})

G = pd.concat(res); G.to_csv(os.path.join(O.OUT, "leadlag_kural_testleri.csv"), index=False)
RG = pd.DataFrame(reg_rows); RG.to_csv(os.path.join(O.OUT, "tarim_oncu_regresyon.csv"), index=False)
O.save_registry("tarim_leadlag")
print("== Kural testleri (2.500 $ maliyetli)")
for (hyp, sym), g in G.groupby(["hyp", "sym"], sort=False):
    print("--", hyp, sym, "|", g["desc"].iloc[0])
    print(O.fmt(g, ["mode", "h", "n", "mean_gross_bp", "mean_net_bp", "t", "win", "pf", "is_net_bp", "oos_net_bp", "years_pos_frac", "worst_bp", "edge_bp",
                    "net_bp_1000", "net_bp_10000"]))
print("\n== Tarım: öncünün kendi gecikmesine ek katkısı"); print(RG.round(3).to_string(index=False))
