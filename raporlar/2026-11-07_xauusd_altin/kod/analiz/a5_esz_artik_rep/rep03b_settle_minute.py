"""Dakika verisiyle uzlaşma zamanı: ardışık VİOP günleri için std(v_ret - Δlog spot(HH:MM)) minimumu, yıl yıl."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a5_esz_artik_rep")
from rep_lib import *
va = pd.read_parquet(f"{OUT}/viop_rep.parquet")
m = pd.read_parquet(f"{P}/duka_min_XAUUSD.parquet"); m.index = pd.to_datetime(m.index)
print(m.columns.tolist(), m.head(2))
col = "c" if "c" in m.columns else m.columns[-1]
days = sorted(set(m.index.normalize()))
print("dakika günleri:", len(days))
grid = [f"{h:02d}:{mm:02d}" for h in (14, 15) for mm in range(0, 60, 5)] + ["16:00"]
L = {}
for d in days:
    s = m.loc[d + pd.Timedelta(hours=14): d + pd.Timedelta(hours=16, minutes=1), col]
    row = {}
    for g in grid:
        t = d + pd.Timedelta(hours=int(g[:2]), minutes=int(g[3:]))
        w = s[:t]
        row[g] = w.iloc[-1] if len(w) and (t - w.index[-1]) <= pd.Timedelta(minutes=3) else np.nan
    L[d] = row
L = pd.DataFrame(L).T
L = np.log(L)
vd = va.reindex(L.index)
# ardışık VİOP günleri (bir önceki VİOP günü de dakika verisinde)
prev = pd.Series(va.index, index=va.index).shift(1).reindex(L.index)
ok = prev.isin(L.index) & vd.ret.notna() & ~vd.roll.fillna(True).astype(bool)
print("ardışık çift:", int(ok.sum()))
res = {}
for g in grid:
    dl = L[g] - L[g].reindex(prev.values).values
    dd = (vd.ret - dl)[ok]
    res[g] = dd.groupby(dd.index.year).std() * 1e4
R = pd.DataFrame(res).round(1)
R["n"] = ok[ok].groupby(ok[ok].index.year).size()
print(R.to_string())
