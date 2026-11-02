"""Kur volatilite rejimine göre koşullu betalar (senkron, XU100 kontrollü) + öncülük (USDTRY_{t-1} -> gün-içi) rejim kırılımı.
Rejim: USDTRY (Yahoo, FX_FIX) 20 günlük gerçekleşmiş vol, t-1'e kadar; eşikler GENİŞLEYEN pencere tercilleri (look-ahead yok, 2010+ veri, ilk 500 gün ısınma).
Ayrıca tarihsel rejimler. Çıktı: res/regime_beta.csv"""
import numpy as np, pandas as pd
import mlib as M, ll
mac = pd.read_parquet(M.RES + "/macro_daily.parquet")
fx = mac["y_usd"]; xu = mac["xu100"]
vol = fx.rolling(20, min_periods=15).std().shift(1)
q1 = vol.expanding(500).quantile(1 / 3).shift(1); q2 = vol.expanding(500).quantile(2 / 3).shift(1)
reg = pd.Series(np.where(vol > q2, "H", np.where(vol > q1, "M", "L")), index=vol.index).where(q1.notna())
reg.to_frame("reg").assign(vol=vol, q1=q1, q2=q2).to_parquet(M.RES + "/fx_regime.parquet")
NAMED = {"2014-2017": ("2014-01-01", "2018-03-31"), "2018 kriz": ("2018-04-01", "2018-12-31"), "2019-2020": ("2019-01-01", "2021-03-19"),
         "2021 Mar-Ara": ("2021-03-22", "2021-12-20"), "KKM 2022-23H1": ("2021-12-21", "2023-06-07"), "carry 2023H2-2025Q1": ("2023-06-08", "2025-03-18"),
         "2025-03 sonrası": ("2025-03-19", "2026-12-31")}
rows = []
for s in M.STOCKS + ["XBANK", "XUSIN", "XU030"]:
    r = M.cc(s).reindex(fx.index); it = M.dec(s, "intra").reindex(fx.index); xui = M.dec("XU100", "intra").reindex(fx.index)
    for lab in ["L", "M", "H"]:
        m = (reg == lab) & (reg.index >= "2014-01-01")
        q = M.ols(r[m], pd.DataFrame({"x": fx[m], "m": xu[m]}))
        pc, n = M.pcorr(r[m], fx[m], [xu[m]])
        ql = M.ols(it[m], pd.DataFrame({"x": fx.shift(1)[m], "own": r.shift(1)[m], "mi": xui[m]}))
        rows.append({"stock": s, "regime": "vol_" + lab, "beta_x": q[0]["x"] if q else np.nan, "t": q[1]["x"] if q else np.nan, "pc": pc, "n": n,
                     "lead_intraX_b": ql[0]["x"] if ql else np.nan, "lead_intraX_t": ql[1]["x"] if ql else np.nan})
    for lab, (a, b) in NAMED.items():
        m = (fx.index >= a) & (fx.index <= b)
        q = M.ols(r[m], pd.DataFrame({"x": fx[m], "m": xu[m]})); pc, n = M.pcorr(r[m], fx[m], [xu[m]])
        rows.append({"stock": s, "regime": lab, "beta_x": q[0]["x"] if q else np.nan, "t": q[1]["x"] if q else np.nan, "pc": pc, "n": n})
R = pd.DataFrame(rows); R.to_csv(M.RES + "/regime_beta.csv", index=False)
pd.set_option("display.width", 250)
print(reg[reg.index >= "2014"].value_counts())
print(R.pivot_table(index="stock", columns="regime", values="pc").round(2).to_string())
print(R.pivot_table(index="stock", columns="regime", values="beta_x").round(2).to_string())
print(R[R.regime.str.startswith("vol")].pivot_table(index="stock", columns="regime", values="lead_intraX_t").round(1).to_string())
