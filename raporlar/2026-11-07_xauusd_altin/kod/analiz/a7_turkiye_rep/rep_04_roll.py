"""Adım 4: roll zamanlaması duyarlılığı — t uzlaşmasında alınan kontrat a_t (t-1 OI ile seçilen) t+1'de de tutulursa (t'nin OI'si henüz bilinmeden)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye_rep")
from rep_lib import *
D = pd.read_parquet(f"{OUT}/rep_series.parquet"); idx = D.index; V = viop_long()
st = V[V.root == "XAUUSD"].pivot_table(index="date", columns="code", values="settle", aggfunc="first").reindex(idx)
hold = pd.Series([np.log(st.iloc[i + 1][c] / st.iloc[i][c]) if i + 1 < len(idx) and pd.notna(st.iloc[i + 1].get(c, np.nan)) else np.nan for i, c in enumerate(D.x_code)], index=idx)
xr = hold.shift(1).fillna(D.x_ret)
print("XAUUSD: a_t tut sürümünde farklı gün:", int(((xr - D.x_ret).abs() > 1e-9).sum()), " max fark bps", round((xr - D.x_ret).abs().max() * 1e4, 1))
lfx = np.log(D.fx15)
sh = (lfx.diff().abs() > 0.025) | (D.xu_ret.shift(1) < -0.05)
oi = D.g_oi.replace(0, np.nan)
for nm, pos in [("C4", -np.sign(D.u_ret.shift(1)).fillna(0.0)), ("C5", -sh.astype(float)), ("C6", np.sign(np.log(oi).diff().shift(1)).fillna(0.0))]:
    for lab, r in [("panel tanımı", D.x_ret), ("a_t tut", xr)]:
        o = bt_seg(pos, r, 3, 5); od = bt_seg(pos, r, 3, 5, demean=True)
        print(f"  {nm} {lab:12s}: tam {o['full']['sharpe']:+.2f} IS {o['is']['sharpe']:+.2f} OOS {o['oos']['sharpe']:+.2f} (dm {od['oos']['sharpe']:+.2f})")
