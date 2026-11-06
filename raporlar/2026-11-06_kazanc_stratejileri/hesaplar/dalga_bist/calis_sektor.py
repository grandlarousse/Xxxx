"""Hayatta kalan yanlılığına karşı kontrol: BIST SEKTÖR ENDEKSLERİ evreninde aynı rotasyon ızgarası.
Endeks bileşimleri BIST tarafından tarihsel olarak değiştiği için bu evrende üye seçimi yanlılığı yok. Endeksler FİYAT
endeksi (temettüsüz) -> kıyas aynı tür: sektör endekslerinin eşit ağırlıklı ortalaması (EW_sektor) ve XU100."""
import os, sys, itertools, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from veri import panel, rf_gunluk
import motor as M
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cikti")
SE = ["XBANK", "XHOLD", "XUTEK", "XELKT", "XGIDA", "XGMYO", "XKMYA", "XMADN", "XMANA", "XMESY", "XINSA", "XTAST", "XTEKS",
      "XTRZM", "XULAS", "XILTM", "XKAGT", "XSGRT", "XTCRT", "XFINK", "XBLSM", "XSPOR"]
P, R, sup = panel("2026-11-05")
EXCL = [x for x in os.environ.get("EXCL", "").split(",") if x]
SE = [s for s in SE if s in P and s not in EXCL]
SUF = ("_haric_" + "_".join(EXCL)) if EXCL else ""
C = R[SE].copy(); NU = C.notna().astype(int) * 9
rf, _ = rf_gunluk(C.index)
V = M.Veri(P, R, C, NU, rf, {s: [s] for s in SE}); usd = P["USDTRY"].ffill()
BAS, BAS24 = "2012-01-02", "2024-01-02"
ok = V.elig & (V.yas >= 130); Wb = np.where(ok, 1.0, 0.0); Wb = Wb / np.maximum(Wb.sum(1, keepdims=True), 1)
Wx = np.zeros_like(Wb); Wx[2:] = Wb[:-2]
ews = pd.Series((Wx * np.nan_to_num(V.C)).sum(1), index=V.cal)
one = pd.Series(1.0, index=V.cal); zero = pd.Series(0.0, index=V.cal)
oe = M.olcu(ews, one, zero, V, BAS, usd=usd); oe24 = M.olcu(ews, one, zero, V, BAS24, usd=usd)
print("EW_sektor", {k: round(v, 3) for k, v in oe.items()}, "\n 2024+", {k: round(v, 3) for k, v in oe24.items()})
rows = []
for skor, K, fr, absf, mktf, buf in itertools.product(["r21", "r63", "r126", "r252", "r252s21", "komp"], [2, 3], ["W", "M"], [0, 1], [0, 1], [0, 2]):
    r, inv, to, We = M.rotasyon(V, skor, K, fr, bool(absf), bool(mktf), False, buf, L=1, c=0.0025)
    o = M.olcu(r, inv, to, V, BAS, usd=usd); o24 = M.olcu(r, inv, to, V, BAS24, usd=usd)
    o1 = M.olcu(r, inv, to, V, BAS, "2018-12-31"); o2 = M.olcu(r, inv, to, V, "2019-01-01", "2023-12-31")
    rows.append(dict(kural=f"{skor}|K{K}|{fr}|abs{absf}|mkt{mktf}|buf{buf}", skor=skor, K=K, frekans=fr, absf=absf, mktf=mktf, buf=buf,
                     cagr=o["cagr"], a_ew=(1 + o["cagr"]) / (1 + oe["cagr"]) - 1, a_xu=o["a_xu"], a_rf=o["a_rf"], maxdd=o["maxdd"],
                     sharpe=o["sharpe"], cagr_usd=o["cagr_usd"], cagr_12_18=o1["cagr"], cagr_19_23=o2["cagr"],
                     cagr_24=o24["cagr"], a_ew_24=(1 + o24["cagr"]) / (1 + oe24["cagr"]) - 1, a_rf_24=o24["a_rf"], a_xu_24=o24["a_xu"]))
G = pd.DataFrame(rows); G.to_csv(os.path.join(OUT, f"izgara_sektor_rot{SUF}.csv"), index=False, float_format="%.4f")
pd.set_option("display.width", 250)
print(G.groupby("skor")[["cagr", "a_ew", "a_xu", "a_rf", "maxdd", "sharpe", "cagr_12_18", "cagr_19_23", "cagr_24", "a_ew_24", "a_rf_24"]].median().round(3).to_string())
print(G.groupby(["skor", "frekans"])[["cagr", "a_ew", "maxdd", "cagr_24", "a_ew_24"]].median().round(3).to_string())
print(G.groupby("mktf")[["cagr", "a_ew", "maxdd", "cagr_24", "a_ew_24"]].median().round(3).to_string())
print("EW_sektor'ü yenen pay:", (G.a_ew > 0).mean().round(2), "| 2024+:", (G.a_ew_24 > 0).mean().round(2))
print(G.sort_values("cagr", ascending=False).head(10).round(3).to_string(index=False))
