"""8) Son 730 gün saatlik veriyle sepet: kapanış->kapanış vs 15:30 ET -> 15:30 ET (kapanış öncesi emir yaklaşımı)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_rep")
from rep_lib import *
ix = pd.Series(SESS, index=SESS); ym = ix.dt.to_period("M"); FIRST = ym != ym.shift(1)
H = regular_holidays(); nxt = ix.shift(-1)
PRE = pd.Series([((H.index > d) & (H.index < n)).any() if pd.notna(n) else False for d, n in zip(SESS, nxt)], index=SESS)
BAS = FIRST | PRE
for t in ["GDXJ", "GDX", "GLD"]:
    hh = pd.read_parquet(f"{S}/panel/yahoo_h/{t}.parquet"); hh.index = pd.to_datetime(hh.index)
    e = hh.index.tz_convert("America/New_York"); hh["d"] = e.normalize().tz_localize(None); hh["hm"] = e.strftime("%H:%M")
    p1530 = hh[hh.hm == "15:30"].set_index("d").open      # ~15:30 ET fiyatı
    y = yahoo(t); c = y.close.reindex(SESS)
    d = pd.DataFrame({"c": c, "p": p1530.reindex(SESS)}).dropna()
    d = d[d.index.isin(SESS)]
    rcc = np.log(d.c).diff(); rpp = np.log(d.p).diff()
    m = BAS.reindex(d.index)
    for nm, r in [("kapanis->kapanis", rcc), ("15:30->15:30", rpp)]:
        q = pd.concat([r.rename("y"), m.astype(float).rename("x")], axis=1).dropna()
        b, tv = nw_ols(q.y.values, q.x.values, 5)
        print(f"{t} {nm}: n={len(q)} olay={int(q.x.sum())} olay ort={q.y[q.x==1].mean()*1e4:.1f} bps diğer={q.y[q.x==0].mean()*1e4:.1f} t={tv[1]:.2f}  ({q.index.min().date()}..{q.index.max().date()})")
