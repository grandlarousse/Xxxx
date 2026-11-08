import sys; sys.path.insert(0, ".")
from adv_common import *
pc, q = lowmom_spot(5)
pv = asof_to_viop(pc)
p15 = d.xau_p15.astype(float); p16 = d.xau_p16.astype(float); p14 = d.xau_p14.astype(float)
sp15 = np.log(p15).diff()          # VİOP takviminde 15:00->15:00 (bir önceki VİOP günü)
sp16 = np.log(p16).diff()
resid = r_v - sp15
print("NaN p15:", p15.isna().sum(), " p16:", p16.isna().sum())
print("resid std bps", (resid.std()*1e4).round(1), " v_ret std", (r_v.std()*1e4).round(1))
def rep(nm, ret, h=1):
    o = {}
    for per in ["IS", "OOS", "FULL", "2017-19", "2020-21", "2022-23", "2024-26"]:
        a, b = PER[per]; m = (ret.index >= a) & (ret.index <= b)
        net = bt(pv[m], ret[m], h, 0, demean=True)
        o[per] = f"{sh(net):.2f}({tstat(net):.2f})"
    print(f"{nm:28s} h{h}", o)
for h in [1, 5]:
    rep("VIOP v_ret (0bps)", r_v, h)
    rep("spot 15->15 on VIOP cal", sp15, h)
    rep("spot 16->16 on VIOP cal", sp16, h)
    rep("resid = v_ret - sp15", resid, h)
# korelasyon: pos_t * resid_{t+1}: resid_{t+1} = e_{t+1}-e_t ; e_t'nin sinyalle korelasyonu
e = np.log(d.v_settle) - np.log(p15)
same = d.v_code == d.v_code.shift(-1)
x5 = asof_to_viop(lp - lp.shift(5)); r1s = asof_to_viop(r_s)
print("corr(e_t - e_{t-1} [gun t 15:00->15:10 + baz], ret1 spot t):", np.corrcoef(*pd.concat([resid, r1s], axis=1).dropna().values.T)[0,1].round(3))
dd = pd.concat([resid.shift(-1), np.sign(x5).where(pv != 0)], axis=1).dropna()
print("aktif günlerde corr(resid_{t+1}, sign ret5):", np.corrcoef(dd.values.T)[0,1].round(3), len(dd))
