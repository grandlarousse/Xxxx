"""1) İşlenebilirlik + kopya grupları + bayat fiyat (stale close) kontrolü.
Çalıştır: python3 -I kod/ajan_tahvil_doviz/01_islenebilirlik.py
Çıktılar: sonuclar/aile_tahvil_doviz/islenebilirlik.csv, kopya_gruplari.csv, bayat_fiyat.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import td, lib

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 200)
scr = pd.read_csv(os.path.join(td.ROOT, "sonuclar", "tarama.csv"))
tv = pd.read_csv(os.path.join(td.ROOT, "sonuclar", "tv_etf.csv"))
x = scr[scr.sym.isin(td.FAM)].merge(tv[["sym", "tv", "durum"]], on="sym", how="left")
x["grup"] = x.sym.map(td.SYM2GRP)
x["cost_vol"] = x.cost_rt_bp / x.vol_1d_bp
# 3 günlük medyan mutlak hareket / maliyet
x["abs3d_over_cost"] = x.med_abs_3d_bp / x.cost_rt_bp
R = td.rets()
last = R[R.index >= R.index[-252 * 3]]

# bayat fiyat göstergeleri (son 3 yıl): sıfır getirili gün oranı, sıfır/çok düşük hacimli gün oranı,
# likit referansa göre gecikmeli korelasyon (illikit seri, likit seriyi bir gün geriden izliyor mu?)
ref = {"FXE": "UUP", "FXF": "UUP", "FXB": "UUP", "FXA": "UUP", "FXC": "UUP", "FXY": "UUP", "UDN": "UUP", "CEW": "UUP",
       "EUO": "UUP", "ULE": "UUP", "YCS": "FXY", "YCL": "FXY", "UUP": "FXE",
       "UBT": "TLT", "TBT": "TLT", "TMV": "TLT", "TMF": "TLT", "EDV": "TLT", "ZROZ": "TLT", "TLH": "TLT"}
rows = []
for s in td.FAM:
    d = lib.load(s); d = d[d.index >= d.index[-min(len(d), 756)]]
    r = np.log(d["c"]).diff().dropna()
    rec = {"sym": s, "zero_ret_frac": float((d["raw_c"].diff() == 0).mean()), "low_vol_days_frac": float((d["v"] * d["raw_c"] < 2e5).mean()),
           "med_volume_shares": float(d["v"].median())}
    rf = ref.get(s, "SPY")
    if rf in last:
        a = last[s]; b = last[rf]
        rec["ref"] = rf
        rec["corr0"] = a.corr(b)
        rec["corr_lead_ref"] = a.corr(b.shift(1))   # ref(t-1) ile ETF(t): >0 ise ETF geriden izliyor (bayat)
        rec["corr_lag_ref"] = a.shift(1).corr(b)
        sp = last["SPY"]
        rec["corr_spy_t_minus1"] = a.corr(sp.shift(1))
        rec["ac1"] = a.corr(a.shift(1))
    rows.append(rec)
st = pd.DataFrame(rows)
x = x.merge(st, on="sym", how="left")

# kopya grupları: grup içi korelasyon (son 3 yıl)
cg = []
for g, ss in td.GROUPS.items():
    ss = [s for s in ss if s in last]
    if len(ss) < 2: continue
    c = last[ss].corr()
    for i in range(len(ss)):
        for j in range(i + 1, len(ss)):
            a, b = ss[i], ss[j]
            beta = last[a].cov(last[b]) / last[b].var()
            cg.append({"grup": g, "a": a, "b": b, "corr_3y": c.loc[a, b], "beta_a_on_b": beta})
# gruplar arası önemli yakınlıklar
for a, b in [("TLT", "IEF"), ("TLT", "AGG"), ("IEF", "AGG"), ("AGG", "LQD"), ("LQD", "VCIT"), ("TLT", "LQD"), ("TIP", "IEF"),
             ("HYG", "SPY"), ("HYG", "BKLN"), ("EMB", "HYG"), ("UUP", "FXE"), ("FXE", "FXF"), ("UUP", "FXY"), ("FXB", "FXE"),
             ("FXA", "FXC"), ("CEW", "FXA"), ("SHY", "IEF"), ("MUB", "AGG"), ("TLT", "TMF"), ("TLT", "TMV")]:
    cg.append({"grup": "gruplar_arasi", "a": a, "b": b, "corr_3y": last[a].corr(last[b]),
               "beta_a_on_b": last[a].cov(last[b]) / last[b].var()})
cg = pd.DataFrame(cg)
cg.to_csv(os.path.join(td.OUT, "kopya_gruplari.csv"), index=False)

cols = ["sym", "grup", "tv", "lev", "price", "med_dollar_vol_m", "spread_bp", "cost_rt_bp", "vol_1d_bp", "cost_vol", "med_abs_3d_bp",
        "abs3d_over_cost", "gap_share", "worst_1d_1y", "zero_ret_frac", "low_vol_days_frac", "ref", "corr0", "corr_lead_ref",
        "corr_lag_ref", "corr_spy_t_minus1", "ac1", "first", "n"]
x = x[cols].sort_values(["grup", "med_dollar_vol_m"], ascending=[True, False])
x.to_csv(os.path.join(td.OUT, "islenebilirlik.csv"), index=False)
print(x.round(3).to_string(index=False))
print()
print(cg.round(3).to_string(index=False))
