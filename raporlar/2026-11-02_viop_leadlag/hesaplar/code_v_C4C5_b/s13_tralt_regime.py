"""s13: 2024-09+ TRALT gün-içi: 2899 06:30 sinyali, ABD t-1 altın/EM sinyalleri ve TRALT kendi gecikmesiyle birlikte (rejim etkisi mi, HK'ye özgü mü?)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
exec(open(sys.path[0] + "/s09_viop_test.py").read().split("OUT = []")[0])
def snap_loc(sym, hhmm):
    h = raw(sym, "h1").copy(); h["ld"] = pd.to_datetime(h["ldate"]); h["end"] = h.index + pd.Timedelta(minutes=60)
    hh, mm = map(int, hhmm.split(":")); lim = h.index.normalize() + pd.Timedelta(hours=hh, minutes=mm)
    return h[h["end"] <= lim].groupby("ld")["c"].last()
def preopen(sym, hhmm="06:30"):
    p = snap_loc(sym, hhmm); pc = daily_local(sym)["c"].shift(1); return to_bist(np.log(p / pc.reindex(p.index)), "zero")
tr = bist_dec("TRALT.IS"); a = active("TRALT")
idx = tr.index[tr.index >= "2024-09-01"]
X = pd.DataFrame({"z2899": preopen("2899.HK").reindex(idx), "z1787": preopen("1787.HK").reindex(idx),
                  "GDX_l1": to_bist(loc_ret("GDX", "adj"), "zero").shift(1).reindex(idx), "GC_l1": to_bist(loc_ret("GC=F", "c"), "zero").shift(1).reindex(idx),
                  "EEM_l1": to_bist(loc_ret("EEM", "adj"), "zero").shift(1).reindex(idx), "tr_cc_l1": tr.cc.shift(1).reindex(idx), "tr_gap": tr.gap.reindex(idx)})
for tgt_nm, tgt in [("spot", tr.intra.reindex(idx)), ("VİOP", a.fint.reindex(idx))]:
    for cols in [["z2899"], ["z2899", "GDX_l1", "GC_l1", "EEM_l1"], ["z2899", "GDX_l1", "GC_l1", "EEM_l1", "tr_cc_l1", "tr_gap"], ["z1787", "GDX_l1", "GC_l1", "EEM_l1", "tr_cc_l1", "tr_gap"]]:
        r, n = ols_nw(tgt, X[cols]); print(f"{tgt_nm} n={n} " + " | ".join(f"{i}: {v.b:+.3f} (t {v.t:+.2f})" for i, v in r.iterrows()))
# 2899'un ABD t-1 sinyalleriyle korelasyonu (bilgi örtüşmesi)
print("corr(z2899, GDX_l1)", round(X.z2899.corr(X.GDX_l1), 3), " corr(z2899, GC_l1)", round(X.z2899.corr(X.GC_l1), 3))
