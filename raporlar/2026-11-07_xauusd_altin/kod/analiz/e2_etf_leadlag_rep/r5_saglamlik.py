"""r5: NW lag duyarliligi, ortusmeyen ornekleme (h adimli, h ofset) t'leri; C4 temiz PL esikleriyle strateji."""
import sys, json
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag_rep")
from rep_lib import *
Z = pd.read_pickle(f"{OUT}/r1_signals.pkl"); SIG, R, LP, W, cal = Z["SIG"], Z["R"], Z["LP"], Z["W"], Z["cal"]
C = {"E2-C2j": (SIG[("GDXJres", 1, 60)], "GDXJ", 3), "E2-C2": (SIG[("GDXres", 3, 60)], "GDX", 3), "E2-C1": (SIG[("GDXres", 10, 60)], "GLD", 5),
     "E2-C5": (SIG["asia1"], "GLD", 3), "E2-C4": (SIG["PL_d5"], "GDX", 3), "E2-C3": (SIG["gi"], "GDX", 1)}
out = {}
for cid, (x, und, h) in C.items():
    y = fwd_ret(LP[und], h); o = {}
    for L in (5, 10, 20):
        o[f"t_L{L}"] = round(ic_t(x, y, L)[1], 2)
        o[f"t_oos_L{L}"] = round(ic_t(x[x.index > IS_END], y[y.index > IS_END], L)[1], 2)
    # ortusmeyen: her h'inci gun, h farkli ofset; NW lag 2
    tt = []; to = []
    for off in range(h):
        xs = x.iloc[off::h]; ys = y.iloc[off::h]
        tt.append(ic_t(xs, ys, 2)[1]); to.append(ic_t(xs[xs.index > IS_END], ys[ys.index > IS_END], 2)[1])
    o["t_nonoverlap_by_offset"] = [round(v, 2) for v in tt]; o["t_oos_nonoverlap_by_offset"] = [round(v, 2) for v in to]
    out[cid] = o
# C4: bayat PL gunleri haric esik ve sinyal
pl = yahoo("PL_F"); ip = pl.index.searchsorted(cal, side="left") - 1
gap = pd.Series((cal - pl.index[ip]).days, index=cal); stale = gap.rolling(6, min_periods=1).max() > 5
xc = SIG["PL_d5"].where(~stale)
p0, h0, l0 = positions(SIG["PL_d5"], -1, 0.8); p1, h1, l1 = positions(xc, -1, 0.8)
out["C4_esik_orijinal"] = (round(h0, 4), round(l0, 4)); out["C4_esik_temiz"] = (round(h1, 4), round(l1, 4))
out["C4_IS_sifir_d5_orani"] = float((SIG["PL_d5"][SIG["PL_d5"].index <= IS_END] == 0).mean())
r = R["GDX"].fillna(0); valid = R["GDX"].notna()
for nm, p in (("orijinal", p0), ("temiz", p1)):
    pn = bt(p, r, 3, 10.0)[0]; pl_ = bt(p.clip(lower=0), r, 3, 10.0)[0]
    m_is = (r.index <= IS_END) & valid; m_o = (r.index > IS_END) & valid
    out[f"C4_{nm}"] = dict(is_ideal=round(sharpe(pn[m_is]), 3), oos_ideal=round(sharpe(pn[m_o]), 3), is_long=round(sharpe(pl_[m_is]), 3), oos_long=round(sharpe(pl_[m_o]), 3))
# C4 2010-2017 IC
y3 = fwd_ret(LP["GDX"], 3); i_, t_, n_ = sub_ic(SIG["PL_d5"], y3, 3, "2010-01-01", "2017-12-31"); out["C4_ic_2010_2017"] = (round(i_, 3), round(t_, 2), n_)
json.dump(out, open(f"{OUT}/r5_saglamlik.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
