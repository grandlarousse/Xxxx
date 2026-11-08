import sys; sys.path.insert(0, ".")
from adv_common import *
P = s.s_p15.astype(float)
ma20 = P.rolling(20).mean(); sd20 = P.rolling(20).std(); bbz = (P - ma20) / sd20
ma50 = P.rolling(50).mean()
vr, q = lowmom_spot(5, mode="volreg")
hi_leg, _ = lowmom_spot(5, thr=2/3, mode="hi_rev")
lo_leg, _ = lowmom_spot(5)
SIG = {
 "VOLREG_5": vr, "VOLREG_hi_leg": hi_leg,
 "TAILMOM_bb2": pd.Series(np.where(bbz > 2, 1.0, np.where(bbz < -2, -1.0, 0.0)), index=P.index).where(bbz.notna()),
 "BB_REV": pd.Series(np.where(bbz < -2, 1.0, np.where(bbz > 2, -1.0, 0.0)), index=P.index).where(bbz.notna()),
 "PMA_50": np.sign(P - ma50).where(ma50.notna()),
}
z1 = r_s / r_s.rolling(20, min_periods=15).std().shift(1)
SIG["SIG2_REV"] = pd.Series(np.where(z1 > 2, -1.0, np.where(z1 < -2, 1.0, 0.0)), index=P.index).where(z1.notna())
SIG["REV_1"] = -np.sign(r_s)
EXT = ((d.index >= "2020-03-01") & (d.index <= "2020-04-30")) | ((d.index >= "2026-01-01") & (d.index <= "2026-03-31"))
def row(nm, pc, h):
    pv = asof_to_viop(pc); o = dict(sig=nm, h=h)
    for per in ["FULL", "IS", "OOS", "2017-19", "2020-21", "2022-23", "2024-26"]:
        a, b = PER[per]; m = (r_v.index >= a) & (r_v.index <= b)
        net = bt(pv[m], r_v[m], h, 5, demean=True); o[per] = f"{sh(net):.2f}({tstat(net):.2f})"
    n = bt(pv, r_v, h, 5, demean=True, demean_mode="year"); o["FULL_yrdm"] = round(sh(n), 2)
    n = bt(pv, r_v.where(~EXT), h, 5, demean=True); o["exEXT"] = round(sh(n), 2)
    n = bt(pv, r_v, h, 10, demean=True); o["10bps"] = round(sh(n), 2)
    n = bt(pv.clip(lower=0), r_v, h, 5, demean=True); o["long"] = round(sh(n), 2)
    n = bt(pv.clip(upper=0), r_v, h, 5, demean=True); o["short"] = round(sh(n), 2)
    me = (s.index >= "2010-01-01") & (s.index <= "2016-12-31"); n = bt(pc[me], r_s[me], h, 5, demean=True); o["E10-16"] = f"{sh(n):.2f}({tstat(n):.2f})"
    o["expo"] = round(float(pv.abs().mean()), 2)
    return o
R = []
for nm, pc in SIG.items():
    for h in ([5, 3] if nm.startswith("VOLREG") else [1]):
        R.append(row(nm, pc, h))
R = pd.DataFrame(R); pd.set_option("display.width", 250); print(R.to_string())
# VOLREG k komşuluğu (h5)
for k in [2, 3, 4, 5, 6, 7, 8, 10]:
    p, _ = lowmom_spot(k, mode="volreg"); pv = asof_to_viop(p)
    a = bt(pv, r_v, 5, 5, demean=True); m = r_v.index <= IS_END; b = bt(pv[m], r_v[m], 5, 5, demean=True)
    me = (s.index >= "2010-01-01") & (s.index <= "2016-12-31"); e = bt(p[me], r_s[me], 5, 5, demean=True)
    print("VOLREG k", k, "h5 FULL", round(sh(a), 2), "IS", round(sh(b), 2), "E", round(sh(e), 2))
# TAILMOM eşik komşuluğu
for thr in [1.5, 1.75, 2.0, 2.25, 2.5]:
    p = pd.Series(np.where(bbz > thr, 1.0, np.where(bbz < -thr, -1.0, 0.0)), index=P.index).where(bbz.notna()); pv = asof_to_viop(p)
    a = bt(pv, r_v, 1, 5, demean=True); me = (s.index >= "2010-01-01") & (s.index <= "2016-12-31"); e = bt(p[me], r_s[me], 1, 5, demean=True)
    print("TAILMOM_bb thr", thr, "h1 FULL", round(sh(a), 2), round(tstat(a), 2), "E", round(sh(e), 2))
for n_ in [20, 50, 100, 200]:
    ma = P.rolling(n_).mean(); p = np.sign(P - ma).where(ma.notna()); pv = asof_to_viop(p)
    o = []
    for per in ["IS", "OOS", "FULL"]:
        a, b = PER[per]; m = (r_v.index >= a) & (r_v.index <= b); o.append(round(sh(bt(pv[m], r_v[m], 1, 5, demean=True)), 2))
    me = (s.index >= "2010-01-01") & (s.index <= "2016-12-31"); e = bt(p[me], r_s[me], 1, 5, demean=True)
    print("PMA", n_, "h1 IS/OOS/FULL", o, "E", round(sh(e), 2), " yr-dm FULL", round(sh(bt(pv, r_v, 1, 5, demean=True, demean_mode='year')), 2))
