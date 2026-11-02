"""s12: KRDMD VİOP: HC sinyalinin vadeli fazlası (fint - sint) ve ABD t-1 sinyalleriyle vadeli açılış bayatlığı plasebosu; TRALT için de ABD t-1 plasebosu."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
exec(open(sys.path[0] + "/s09_viop_test.py").read().split("OUT = []")[0])
R = sina_roll("HC")
US = {s: to_bist(loc_ret(s, "adj" if s not in ("GC=F", "HG=F", "ES=F") else "c"), "zero").shift(1) for s in ["SLX", "MT", "GDX", "GC=F", "HG=F", "ES=F", "EEM", "TUR"]}
for und, own in [("KRDMD", {"HC": to_bist(R["cc"], "zero")}), ("TRALT", {"600547": to_bist(loc_ret("600547.SS", "adj"), "zero")})]:
    a = active(und); sp = bist_dec(und + ".IS")
    for st in ["2021-01-01", "2024-09-01"]:
        aa = a[a.index >= st]; df = pd.DataFrame({"fint": aa.fint, "sint": sp.intra.reindex(aa.index)}); df["exc"] = df.fint - df.sint
        for nm, s in {**own, **US}.items():
            s = s.reindex(df.index)
            o = [nw_t(df[k], s) for k in ["fint", "sint", "exc"]]
            print(f"{und} {st[:7]}+ {nm:7s} -> VİOP r={o[0][0]:+.3f} t={o[0][1]:+.2f} | spot r={o[1][0]:+.3f} t={o[1][1]:+.2f} | fazla r={o[2][0]:+.3f} t={o[2][1]:+.2f}")
