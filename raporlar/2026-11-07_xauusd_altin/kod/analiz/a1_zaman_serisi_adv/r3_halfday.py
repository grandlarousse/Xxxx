import sys; sys.path.insert(0, ".")
from adv_common import *
ls = np.log(d.v_settle.astype(float))
base = (ls - np.log(d.xau_p15)).rolling(21, center=True, min_periods=5).median()
dev = {H: (ls - np.log(d[f"xau_p{H}"].astype(float)) - base) * 1e4 for H in ["07", "12", "13", "14", "15", "16"]}
D = pd.DataFrame(dev)
D["best"] = D[["07","12","13","14","15","16"]].abs().fillna(1e9).idxmin(axis=1)
D["vol"] = d.v_volume
cand = D[(D["15"].abs() > 25) & (D[["07", "12", "13"]].abs().min(axis=1) < D["15"].abs() / 2)]
print(len(cand)); print(cand.round(1).to_string())
