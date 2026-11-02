"""s14: IS (2014-2020) / OOS (2021-2026) korelasyon t'leri ve maliyet duyarlılığı — temiz uzun dönem sinyaller."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
tr = bist_dec("TRALT.IS"); kr = bist_dec("KRDMD.IS")
for nm, sig, y in [("600547.SS cc -> TRALT intra", to_bist(loc_ret("600547.SS", "adj"), "zero"), tr.intra), ("518880.SS cc -> TRALT intra", to_bist(loc_ret("518880.SS", "adj"), "zero"), tr.intra),
                   ("SHFE HC cc -> KRDMD intra", to_bist(sina_roll("HC")["cc"], "zero"), kr.intra), ("1787.HK gap(01:30) -> TRALT intra", None, tr.intra)]:
    if sig is None:
        d = daily_local("1787.HK"); sig = to_bist(np.log(d.o / d.c.shift(1)), "zero")
    out = []
    for a, b in [("2014-01-01", "2021-01-01"), ("2021-01-01", "2027-01-01")]:
        m = (y.index >= a) & (y.index < b); r, t, n = nw_t(y[m], sig.reindex(y.index)[m]); out.append(f"{a[:4]}-{int(b[:4])-1}: r={r:+.3f} t={t:+.2f} n={n}")
    costs = []
    for c in [0, 8, 10, 15]:
        rr, _, _ = bt(sig, y, c); costs.append(f"c{c}: {rr['ALL'].get('bps', np.nan):+.1f}")
    print(f"{nm:34s} " + " | ".join(out) + " || " + " ".join(costs))
