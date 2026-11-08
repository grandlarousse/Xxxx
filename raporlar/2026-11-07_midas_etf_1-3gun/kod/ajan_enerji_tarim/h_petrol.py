"""Petrol / enerji hisse hipotezleri: EN04 WPSR günü, EN05 USO roll, EN06 petrol->enerji hissesi yetişme (ve tersi),
EN07 OVX rejimi, EN08 enerji IBS, USO/USL eğri vekili, BNO-USO (Brent-WTI) yayılımı ortalamaya dönüş.
Çalıştırma: python3 -I kod/ajan_enerji_tarim/h_petrol.py  -> sonuclar/aile_enerji_tarim/petrol_*.csv, testler_petrol.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak as O, lib

pd.set_option("display.width", 250)
uso = lib.load("USO"); idx = uso.index
R = {s: O.logret(s).reindex(idx) for s in ["USO", "BNO", "USL", "UCO", "SCO", "XLE", "XOP", "OIH", "PDBC", "DBC"]}
desc_rows, res, reg_rows = [], [], []

def describe(name, mask, s, x=None):
    x = (R[s] if x is None else x).reindex(idx); m = mask.reindex(idx).fillna(False)
    a, b = x[m].dropna(), x[~m].dropna()
    t, p = O.ttest_diff(a, b); tv, pv = O.ttest_diff(a.abs(), b.abs())
    ti, _ = O.ttest_diff(a[a.index <= lib.IS_END], b[b.index <= lib.IS_END])
    to, _ = O.ttest_diff(a[a.index > lib.IS_END], b[b.index > lib.IS_END])
    rec = {"test": name, "seri": s, "n_olay": len(a), "ort_olay_bp": a.mean() * 1e4, "ort_diger_bp": b.mean() * 1e4, "t_fark": t, "p_fark": p,
           "t_fark_is": ti, "t_fark_oos": to, "abs_olay_bp": a.abs().mean() * 1e4, "abs_diger_bp": b.abs().mean() * 1e4,
           "abs_oran": a.abs().mean() / b.abs().mean(), "t_abs": tv, "p_abs": pv}
    desc_rows.append(rec)
    O.REG.append({"hyp": name, "sym": s, "desc": "olay günü ort. fark (tanımlayıcı)", "mode": "-", "h": 0, "kind": "tanimlayici",
                  "sign": 0, "n": len(a), "net_bp": a.mean() * 1e4, "t": t, "p1": p, "is_t": ti, "oos_t": to})

def nwreg(name, y, X, cols, h, sign):
    d = pd.concat([y.rename("y")] + [X[c].rename(c) for c in cols], axis=1).dropna()
    for nm, m in (("tum", np.ones(len(d), bool)), ("is", d.index <= lib.IS_END), ("oos", d.index > lib.IS_END)):
        dd = d[m]
        b, t = O.nw_t(dd["y"].values, np.column_stack([np.ones(len(dd))] + [dd[c].values for c in cols]), max(1, h))
        rec = {"test": name, "h": h, "donem": nm, "n": len(dd)}
        for i, c in enumerate(cols):
            rec[f"b_{c}"] = b[i + 1]; rec[f"t_{c}"] = t[i + 1]; rec[f"bp_per_sd_{c}"] = b[i + 1] * dd[c].std() * 1e4
        reg_rows.append(rec)
        if nm == "tum":
            O.REG.append({"hyp": name, "sym": "-", "desc": f"NW regresyon h={h}, son değişken", "mode": "-", "h": h, "kind": "regresyon",
                          "sign": sign, "n": len(dd), "t": t[-1], "p1": O.p_one(t[-1], len(dd), sign)})

# ---------- EN04: EIA WPSR günü ----------
wpsr = O.events("eia_petroleum")["date"]
wd = O.on_dates(idx, wpsr)
for s in ["USO", "BNO", "XLE", "XOP"]:
    describe("EN04_WPSR_gunu", wd, s)
res.append(O.grid("EN04_WPSR_USO", "USO", O.day_before(idx, wpsr), "WPSR öncesi gün USO long (beklenen 0)", hs=(1,), modes=("C0", "O1")))

# ---------- EN05: USO roll ----------
roll = O.events("ung_uso_roll"); ur = roll[roll.event == "USO_roll"]["date"]
rd = O.on_dates(idx, ur)
pre20 = pd.Series(idx < pd.Timestamp("2020-05-01"), index=idx)
describe("EN05_USO_roll_gunu", rd, "USO")
describe("EN05_USO_roll_USO-USL", rd, "USO-USL", R["USO"] - R["USL"])
describe("EN05_USO_roll_USO-USL_2020once", rd & pre20, "USO-USL", (R["USO"] - R["USL"]).where(pre20))
describe("EN05_USO_roll_USO-USL_2020sonra", rd & ~pre20, "USO-USL", (R["USO"] - R["USL"]).where(~pre20))
describe("EN05_USO_roll_USO-BNO", rd, "USO-BNO", R["USO"] - R["BNO"])

# ---------- EN06: petrol -> enerji hissesi yetişme ----------
def resid(y, x, n=60):
    """res_t = y_t - beta60(y~x)_t * x_t ; beta ve sigma t'ye kadar bilinen (t dahil 60 g)."""
    beta = y.rolling(n).cov(x) / x.rolling(n).var()
    res_ = y - beta * x
    sd = res_.rolling(n).std().shift(1)
    return res_, sd

res_oil, sd_oil = resid(R["USO"], R["XLE"])          # petrol, XLE'nin açıkladığından fazla hareket etti
z_oil = res_oil / sd_oil
for tsym in ["XLE", "XOP", "OIH"]:
    res.append(O.grid("EN06_USO_gt_XLE", tsym, z_oil >= 2, f"z(res USO|XLE)>=2 -> {tsym} long", hs=(1, 3)))
    res.append(O.grid("EN06_USO_lt_XLE", tsym, z_oil <= -2, f"z(res USO|XLE)<=-2 -> {tsym} long (beklenen -)", hs=(1,), modes=("C0",), sign=-1))
# tersi: enerji hissesi petrolden fazla hareket etti -> USO yetişir mi?
res_eq, sd_eq = resid(R["XLE"], R["USO"]); z_eq = res_eq / sd_eq
for tsym in ["USO", "BNO"]:
    res.append(O.grid("EN06r_XLE_gt_USO", tsym, z_eq >= 2, f"z(res XLE|USO)>=2 -> {tsym} long", hs=(1, 3)))
# sürekli regresyon (öncünün katkısı kendi gecikmesine karşı): fwd r_XLE ~ own r_XLE(t) + r_USO(t)
X = pd.DataFrame({"own_XLE": R["XLE"], "USO": R["USO"], "own_USO": R["USO"], "XLE": R["XLE"], "own_XOP": R["XOP"],
                  "gap_XLE": -res_eq, "gap_USO": -res_oil})
for h in (1, 3):
    nwreg("EN06_reg_XLE~own+USO", O.fwd(R["XLE"], h), X, ["own_XLE", "USO"], h, +1)
    nwreg("EN06_reg_XOP~own+USO", O.fwd(R["XOP"], h), X.assign(USO=R["USO"]), ["own_XOP", "USO"], h, +1)
    nwreg("EN06_reg_USO~own+XLE", O.fwd(R["USO"], h), X, ["own_USO", "XLE"], h, +1)
    # yetişme boşluğu (beta*r_USO - r_XLE) kendi getirisine EK katkı
    nwreg("EN06_reg_XLE~own+gap", O.fwd(R["XLE"], h), X.assign(gap=(R["USO"] * (R["XLE"].rolling(60).cov(R["USO"]) / R["USO"].rolling(60).var()) - R["XLE"])), ["own_XLE", "gap"], h, +1)

# ---------- EN07: OVX rejimi ----------
ovx = lib.vol_index("OVX").reindex(idx).ffill()
ovs = ovx >= 1.25 * ovx.rolling(20).mean()
for s in ["USO", "XLE"]:
    f3 = O.fwd(R[s], 3)
    describe("EN07_OVX_sicrama_fwd3", ovs, s + "_fwd3", f3)
    res.append(O.grid("EN07_OVX_long", s, ovs, f"OVX>=1.25*SMA20 -> {s} long", hs=(1, 3)))

# ---------- EN08: enerji IBS ----------
for s in ["XLE", "XOP", "USO", "BNO"]:
    d = lib.load(s); sig = (lib.ibs(d) < 0.15) & (d["c"] > lib.sma(d["c"], 200))
    res.append(O.grid("EN08_IBS015_ust200", s, sig, f"IBS<0.15 & C>SMA200 -> {s} long", hs=(1,)))

# ---------- USO/USL eğri vekili ----------
c20 = (np.log(uso["c"]).diff(20) - np.log(lib.load("USL")["c"]).diff(20)).reindex(idx)
res.append(O.grid("PT_c20_USO", "USO", c20 > 0, "c20=Δ20ln(USO)-Δ20ln(USL)>0 -> USO long", hs=(1, 3)))
for h in (1, 3):
    nwreg("PT_reg_USO~own+c20", O.fwd(R["USO"], h), pd.DataFrame({"own": R["USO"], "c20": c20}), ["own", "c20"], h, +1)

# ---------- BNO-USO yayılımı ----------
s_ = (np.log(lib.load("BNO")["c"]) - np.log(uso["c"])).reindex(idx)
zsp = (s_ - s_.rolling(20).mean()) / s_.rolling(20).std()
dsp = R["BNO"] - R["USO"]
for h in (1, 3):
    nwreg("PT_reg_spread_fwd~z", O.fwd(dsp, h), pd.DataFrame({"z": zsp}), ["z"], h, -1)
res.append(O.grid("PT_spread_BNOucuz", "BNO", zsp <= -2, "z(ln BNO/USO, 20g)<=-2 -> BNO long", hs=(1, 3)))
res.append(O.grid("PT_spread_USOucuz", "USO", zsp >= 2, "z(ln BNO/USO, 20g)>=2 -> USO long", hs=(1, 3)))

D = pd.DataFrame(desc_rows); D.to_csv(os.path.join(O.OUT, "petrol_tanimlayici.csv"), index=False)
G = pd.concat(res); G.to_csv(os.path.join(O.OUT, "petrol_stratejiler.csv"), index=False)
RG = pd.DataFrame(reg_rows); RG.to_csv(os.path.join(O.OUT, "petrol_regresyon.csv"), index=False)
O.save_registry("petrol")
print("== Tanımlayıcı"); print(D.round(3).to_string(index=False))
print("\n== Regresyonlar (NW)"); print(RG.round(4).to_string(index=False))
print("\n== Strateji ızgaraları (2.500 $ maliyetli)")
for (hyp, sym), g in G.groupby(["hyp", "sym"], sort=False):
    print("--", hyp, sym, "|", g["desc"].iloc[0])
    print(O.fmt(g, ["mode", "h", "n", "mean_gross_bp", "mean_net_bp", "t", "win", "pf", "is_net_bp", "oos_net_bp", "years_pos_frac", "worst_bp", "edge_bp"]))
