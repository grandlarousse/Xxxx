"""r4: ek kontroller — işlem/yıl sayımında NaN etkisi, havuzlanmış spot 2010–2026 IC, ABD-takvimi C1 backtest, 2017-2026 yıllık IC."""
import sys, numpy as np, pandas as pd
OUT = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz_rep"; sys.path.insert(0, OUT)
from rep_util import *
d = pd.read_parquet(f"{OUT}/r1_viop.parquet"); sp = pd.read_parquet(f"{OUT}/r1_spot.parquet"); idx = d.index
YRS = (idx[-1] - idx[0]).days / 365.25
def zsc(r, win=120, minp=60): return r / r.rolling(win, min_periods=minp).std().shift(1)
def beta(a, b, win, minp): return (a.rolling(win, min_periods=minp).cov(b) / b.rolling(win, min_periods=minp).var()).shift(1)
def rz(df, c):
    rm = np.log(df[c]).diff(); rg = np.log(df.y_GLD).diff(); return zsc(rm - beta(rm, rg, 60, 40) * rg)
zc2 = zsc((d.ust_nom10 - d.ust_nom2).diff(5))
p_nf = (zc2 / 2).clip(-1, 1)
print("C2 işlem/yıl: NaN hariç sıfırdan farklı", round(((p_nf != 0) & p_nf.notna()).sum() / YRS, 1), "| NaN'ı sıfırdan farklı sayan", round((p_nf != 0).sum() / YRS, 1),
      "| z tam 0 gün:", int((zc2 == 0).sum()))
z1 = rz(d, "y_GDXJ")
for nm, a, b in (("2010-2016", "2010", "2016-12-31"), ("2017-2026", "2017-03", "2026-12-31"), ("2010-2026 havuz", "2010", "2026-12-31")):
    zs = rz(sp, "y_GDXJ"); m = (sp.index >= a) & (sp.index <= b); s = ic_t(zs[m], sp.sfwd3[m], 5)
    print(f"C1 spot {nm}: ic={s['ic']:.4f} t={s['t']:.2f} n={s['n']}")
s = split(z1, d.fwd3, 3); print("C1 VİOP yıllık IC:", s["by_year"])
# 2017 hariç IS; 2025–2026 son dönem
for nm, a, b in (("IS 2018-2021 (2017 hariç)", "2018-01-01", "2021-12-31"), ("2017 yalnız", "2017-01-01", "2017-12-31"), ("2025-2026", "2025-01-01", "2026-12-31")):
    m = (idx >= a) & (idx <= b); s = ic_t(z1[m], d.fwd3[m], 5)
    pos = np.sign(z1).where(z1.abs() > 0.43, 0.0).fillna(0)
    print(f"C1 {nm}: ic={s['ic']:.4f} t={s['t']:.2f} n={s['n']}  BT Sharpe5={bt(pos[m], d.v_ret[m], 3)['sharpe']:.2f}")
# ABD takvimi kurulumu ile backtest
P = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/panel"
def yh(tk):
    y = pd.read_parquet(f"{P}/yahoo/{tk}.parquet"); y.index = pd.to_datetime(y.index); return np.log(y.adjclose).diff()
gj, gl = yh("GDXJ"), yh("GLD"); zu = zsc(gj - beta(gj, gl, 60, 40) * gl)
src = pd.DataFrame({"D": zu.index, "zu": zu.values}); src["cl"] = (src.D + pd.Timedelta(hours=16)).dt.tz_localize("America/New_York").dt.tz_convert("UTC").dt.tz_localize(None)
m = pd.merge_asof(pd.DataFrame({"cut": idx + pd.Timedelta(hours=15)}), src.sort_values("cl"), left_on="cut", right_on="cl", allow_exact_matches=False)
zU = pd.Series(m.zu.values, index=idx); Dm = pd.Series(m.D.values, index=idx); zU = zU.where(Dm != Dm.shift(1), 0.0)  # tekrar eden bayat değer → 0 (analistle aynı muamele)
s = split(zU, d.fwd3, 3); print(f"C1 ABD-takvimi (bayat=0): ic={s['ic']:.4f} t={s['t']:.2f} IS={s['t_is']:.2f} OOS={s['t_oos']:.2f} yıl={s['yrs']}")
pU = np.sign(zU).where(zU.abs() > 0.43, 0.0).fillna(0); ISM = idx <= IS_END
for nm, mm in (("IS", ISM), ("OOS", ~ISM)):
    print(f"  ABD-takvimi tercile BT {nm}: Sharpe5={bt(pU[mm], d.v_ret[mm], 3)['sharpe']:.2f} dm={bt(pU[mm], d.v_ret[mm], 3, demean=True)['sharpe']:.2f} 10bps={bt(pU[mm], d.v_ret[mm], 3, cost_bps=10)['sharpe']:.2f}")
