"""v5: temizlik duyarlılığı — gün-içi hedefi cc temizliğinden bağımsız tut (sadece bozuk açılış + |intra|>%10,5 at)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_a")
from vcore import *
SA = pd.read_parquet(OUTD + "/v1_signals_A.parquet")
for s in ["THYAO.IS", "PGSUS.IS", "TAVHL.IS"]:
    d = raw(s).copy(); d.index = pd.DatetimeIndex(d.ldate); d = d[~d.index.duplicated(keep="last")]; d = d[d.v.fillna(0) > 0]
    intra = np.log(d.c / d.o); bad_o = (d.o <= 0) | ((d.h == d.l) & (d.o == d.c.shift(1))); intra[bad_o] = np.nan
    intra[(intra > UP) | (intra < DN)] = np.nan; intra = intra[intra.index >= "2014-01-01"]
    for cost in [8, 15]:
        o, _, _ = bt(SA.AIR.shift(1), intra, cost, 1.0)
        print(s, cost, {p: {k: round(float(o[p].get(k, np.nan)), 2) for k in ["n", "bps", "t_nw", "gross_bps"]} for p in ["IS", "OOS"]})
