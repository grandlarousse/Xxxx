"""Oran: GSRZ L120 h5 IC ve altın/platin (Yahoo GC=F/PL=F, t-1; Yahoo takviminde hesaplanıp spot gününe as-of eşlenir)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik_rep")
from rep_lib import *
D = pd.read_parquet(f"{OUT}/spot_snaps.parquet"); D = D[D.index >= "2010-01-01"]
va = pd.read_parquet(f"{OUT}/viop_rep.parquet"); V = lambda s: s.reindex(va.index); Y = {h: va[f"fwd{h}"] for h in (1, 3, 5)}
lr = np.log(D.XAU_p15 / D.XAG_p15)
z = (lr - lr.rolling(120, min_periods=96).mean()) / lr.rolling(120, min_periods=96).std()
st = stats(V(z), Y[5], 5); print(f"GSRZ L120 h5: ic {st['ic']:.3f} t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f} yıl {st['yrs']}")
gc = pd.read_parquet(f"{P}/yahoo/GC_F.parquet"); pl = pd.read_parquet(f"{P}/yahoo/PL_F.parquet")
y = pd.concat([gc.close.rename("gc"), pl.close.rename("pl")], axis=1).dropna(); y.index = pd.to_datetime(y.index)
r = np.log(y.gc / y.pl); dr = r.diff(); sdr = dr.rolling(120, min_periods=96).std().shift(1)
cal = va.index
def asof_prev(s):
    s = s.dropna(); i = s.index.searchsorted(cal, side="left") - 1
    return pd.Series(np.where(i >= 0, s.values[np.clip(i, 0, None)], np.nan), index=cal)
res = []
for L in (20, 60, 120):
    zz = asof_prev((r - r.rolling(L, min_periods=int(0.8 * L)).mean()) / r.rolling(L, min_periods=int(0.8 * L)).std())
    for h in (1, 3, 5):
        st = stats(zz, Y[h], h); res.append((f"GPTZ L{L} h{h}", st["t"], st["t_is"], st["t_oos"]))
for k in (1, 3, 5):
    zz = asof_prev(dr.rolling(k).sum() / (sdr * np.sqrt(k)))
    for h in (1, 3, 5):
        st = stats(zz, Y[h], h); res.append((f"GPTD k{k} h{h}", st["t"], st["t_is"], st["t_oos"]))
R = pd.DataFrame(res, columns=["test", "t", "t_is", "t_oos"]).round(2)
print(R.to_string()); print("platin 18 test maks |t|:", R.t.abs().max())
