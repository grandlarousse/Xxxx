#!/usr/bin/env python3
"""Adım 3: A1-LOWMOM-h1 / h5 bağımsız yeniden hesap. Çalıştır: python3 -W ignore r3_lowmom.py"""
import sys, json, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a1_zaman_serisi_rep")
from rutil import *
B, SP = load()
HALF = pd.to_datetime(pd.read_csv(f"{OUT}/half_days.csv").iloc[:, 0])
r_v = B.v_ret
# --- spot takviminde öznitelikler (hepsi gün t 15:00 UTC'ye kadar) ---
lp, r = SP.lp, SP.r
rv20 = r.rolling(20).std()
q = exp_pct(rv20)
def mom(k): return lp - lp.shift(k)
def lowmom(k=5, thr=1/3): return np.sign(mom(k)).where(q < thr, 0.0).where(q.notna())
print("rv20 yıllık eşik (tam örneklem 1/3 kantil):", round(float(np.nanquantile(rv20.dropna(), 1/3) * np.sqrt(252)), 4),
      "| son gün rv20 yıllık:", round(float(rv20.iloc[-1] * np.sqrt(252)), 3), "q_son:", round(float(q.iloc[-1]), 3),
      "| 2026 q<1/3 gün payı:", round(float((q[q.index.year == 2026] < 1/3).mean()), 3))
# eşiğin zaman içinde genişleyen değeri (q=1/3 sınırı) — 2017 ve 2026 başı
for d in ["2017-03-06", "2021-12-31", "2026-11-06"]:
    h_ = rv20[:d].dropna(); print("  genişleyen 1/3 eşiği", d, round(float(np.quantile(h_, 1/3) * np.sqrt(252)), 4))
V = lambda x: asof_to(pd.DataFrame({"x": x}), B.index).x
base = V(lowmom(5))
print("VİOP günlerinde pozisyon NaN:", int(base.isna().sum()), "| bayat (spot günü yok) VİOP günü:", int((~B.index.isin(SP.index)).sum()))
ROWS = []
for h in [1, 3, 5]:
    o = bt_split(base, r_v, h); ROWS.append(row("LOWMOM_k5", h, o))
    for k in [1, 3, 10, 20]: ROWS.append(row(f"LOWMOM_k{k}", h, bt_split(V(lowmom(k)), r_v, h)))
    # yarım gün (arife/28 Ekim, uzlaşma ≈09:30 UTC < 15:00) pozisyonları sıfırla
    ROWS.append(row("LOWMOM_k5_noHALF", h, bt_split(base.where(~base.index.isin(HALF), 0.0), r_v, h)))
    # VİOP serisiyle t (kapanışta hesaplanan) ve t-1 (temiz)
    Pv = r_v.fillna(0).cumsum(); qv = V(q)
    ROWS.append(row("LOWMOM_viop_t", h, bt_split(np.sign(Pv - Pv.shift(5)).where(qv < 1/3, 0.0).where(qv.notna()), r_v, h)))
    ROWS.append(row("LOWMOM_viop_t1", h, bt_split(np.sign(Pv - Pv.shift(5)).shift(1).where(qv.shift(1) < 1/3, 0.0).where(qv.notna()), r_v, h)))
    # 1 gün bayat spot sinyali
    ROWS.append(row("LOWMOM_k5_lag1", h, bt_split(base.shift(1), r_v, h)))
    roll_near = B.roll.rolling(3, center=True, min_periods=1).max().astype(bool)
    ROWS.append(row("LOWMOM_k5_exRoll", h, bt_split(base, r_v.where(~roll_near), h)))
    EXT = ((B.index >= "2020-03-01") & (B.index <= "2020-04-30")) | ((B.index >= "2026-01-01") & (B.index <= "2026-03-31"))
    ROWS.append(row("LOWMOM_k5_exExt", h, bt_split(base, r_v.where(~EXT), h)))
    lo_, hi_ = r_v.quantile([0.01, 0.99]); ROWS.append(row("LOWMOM_k5_winsor", h, bt_split(base, r_v.clip(lo_, hi_), h)))
    bh = bt(pd.Series(1.0, index=r_v.index), r_v, 1, 0.0)
T = pd.DataFrame(ROWS)
print("\nbuy&hold VİOP (maliyetsiz) Sharpe tam/IS/OOS:", [round(bt(pd.Series(1.0, index=x.index), x, 1, 0.0)["sharpe"], 3) for x in [r_v, r_v[r_v.index <= IS_END], r_v[r_v.index > IS_END]]])
pd.set_option("display.width", 250)
print(T.drop(columns="by_year").to_string(index=False))
for _, rw in T[T.sig == "LOWMOM_k5"].iterrows(): print("yıl yıl (drift çıkarılmış, net) h", rw.h, rw.by_year)
T.to_csv(f"{OUT}/rep_lowmom_bt.csv", index=False)

# --- IC: x = ret5 yalnız q<1/3 günlerinde (sürekli), y = fwd_h ---
print("\nIC (Spearman, NW lag=max(h,5)):")
IC = []
x_lo = V(mom(5).where(q < 1/3))
for h in [1, 3, 5]:
    y = B[f"fwd{h}"]
    st = ic_split(x_lo, y, h); IC.append(dict(feat="ret5_loV", h=h, **{k: v for k, v in st.items()}))
    st2 = ic_split(x_lo.where(~x_lo.index.isin(HALF)), y, h); IC.append(dict(feat="ret5_loV_noHALF", h=h, **st2))
    st3 = ic_split(np.sign(x_lo), y, h); IC.append(dict(feat="sign_ret5_loV", h=h, **st3))
    # yalnız VİOP takviminde spot olan günler (bayat günler hariç)
    st4 = ic_split(x_lo.where(B.index.isin(SP.index)), y, h); IC.append(dict(feat="ret5_loV_freshonly", h=h, **st4))
ICD = pd.DataFrame(IC); print(ICD.drop(columns="by_year").round(3).to_string(index=False))
for _, rw in ICD[ICD.feat == "ret5_loV"].iterrows(): print("IC yıl yıl h", rw.h, rw.by_year)
ICD.to_csv(f"{OUT}/rep_lowmom_ic.csv", index=False)
# placebo: x'i kaydır
print("\nplacebo IC (s>0 = daha eski bilgi, s<0 = gelecek):")
for h in [1, 3, 5]:
    y = sum(r_v.shift(-k) for k in range(1, h + 1))
    print(h, {s: round(ic_nw(x_lo.shift(s), y, max(h, 5))["ic"], 4) for s in (-2, -1, 0, 1, 2, 3)})

# --- erken spot 2010-2016 ve tam spot dönem ---
print("\nSpot (15:00→15:00) backtest drift çıkarılmış, LOWMOM_k5:")
pc = lowmom(5); E = []
for h in [1, 3, 5]:
    for nm, a, b in [("2010-16", "2010-01-01", "2016-12-31"), ("2017-21", "2017-01-01", "2021-12-31"), ("2022-26", "2022-01-01", "2026-12-31"), ("2010-26", "2010-01-01", "2026-12-31")]:
        m = (SP.index >= a) & (SP.index <= b); o = bt(pc[m], r[m], h, 5.0, demean=True)
        E.append(dict(per=nm, h=h, shdm=round(o["sharpe"], 2), t=round(o["t"], 2)))
    o = bt(pc, r, h, 5.0, demean=True); g = o["pnl"].groupby(o["pnl"].index.year); ys = g.mean() / g.std() * np.sqrt(252)
    act = o["eff"].abs().groupby(o["eff"].index.year).mean()
    yy = {int(k): round(v, 2) for k, v in ys.items() if act.get(k, 0) > 0.05 and 2011 <= k <= 2025}
    print(f" h{h} spot yıl yıl 2011-2025 pozitif: {sum(v > 0 for v in yy.values())}/{len(yy)}", yy)
    # spot erken IC
    m = (SP.index >= "2010-01-01") & (SP.index <= "2016-12-31")
    sf = sum(r.shift(-k) for k in range(1, h + 1))
    print(f"  erken spot IC h{h}:", {k: round(v, 3) for k, v in ic_nw(mom(5).where(q < 1/3)[m], sf[m], max(h, 5)).items()})
print(pd.DataFrame(E).pivot(index="per", columns="h").to_string())
# aktif gün sayıları
act = (base != 0) & base.notna()
print("\nVİOP aktif gün payı yıl yıl:", act.groupby(act.index.year).mean().round(2).to_dict())
print("yarım gün ∩ aktif:", [str(d.date()) for d in HALF if act.get(d, False)])
