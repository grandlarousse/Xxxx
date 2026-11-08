"""s5: C1 (madenci artığı → altın) tanıları: kontrollerin tek tek etkisi, bileşen ayrıştırması, β penceresi/ölçüt duyarlılığı,
ileri gün profili (t+1..t+5 tek tek), 2010–2016 spot erken dönem (GDX, GDXJ, RING), büyük olay asimetrisi."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz")
from a4_common import *

reg_reset("s5_")
d = load_viop(); sp = load_spot(); idx = d.index
y3 = d["fwd3"]
def resid(df, m, bw=60, bench="y_GLD", extra=None):
    rm = np.log(df[m]).diff(); rg = np.log(df[bench]).diff()
    if extra is None:
        b = rm.rolling(bw, min_periods=int(bw * .67)).cov(rg).shift(1) / rg.rolling(bw, min_periods=int(bw * .67)).var().shift(1)
        return zscale(rm - b * rg)
    rs = np.log(df[extra]).diff()
    # 2 faktör: geçmiş-yalnız yuvarlanan çoklu regresyon (kovaryans matrisleri)
    c = lambda a, b_: a.rolling(bw, min_periods=int(bw * .67)).cov(b_).shift(1)
    vg, vs, cgs, cmg, cms = c(rg, rg), c(rs, rs), c(rg, rs), c(rm, rg), c(rm, rs)
    det = vg * vs - cgs ** 2
    bg = (cmg * vs - cms * cgs) / det; bs = (cms * vg - cmg * cgs) / det
    return zscale(rm - bg * rg - bs * rs)

x = resid(d, "y_GDXJ")
rows = []
def rec(name, s, h=3, fam="s5_tani"):
    reg(fam, f"s5_{name}_h{h}", name, h, s)
    rows.append(dict(test=name, h=h, ic=s.get("ic"), t=s.get("t"), t_is=s.get("t_is"), t_oos=s.get("t_oos"), yrs=f"{s.get('yrs_same_sign')}/{s.get('yrs')}"))

# 1) kontroller tek tek
C = gold_controls(d)
C["spx"] = zscale(np.log(d["y__GSPC"]).diff()); C["vix"] = zscale(np.log(d["y__VIX"]).diff())
C["gld1"] = zscale(np.log(d["y_GLD"]).diff()); C["gdxj1"] = zscale(np.log(d["y_GDXJ"]).diff())
for cc in ["g1", "g5", "spx", "vix", "gld1"]:
    rec(f"kismi_tek_{cc}", partial_stats(x, y3, C[[cc]], 3))
# 2) bileşenler: fwd3 ~ z(r_GDXJ) + z(r_GLD)
for nm, xx, cc in (("bilesen_GDXJ|GLD", C["gdxj1"], ["gld1"]), ("bilesen_GLD|GDXJ", C["gld1"], ["gdxj1"])):
    rec(nm, partial_stats(xx, y3, C[cc], 3))
# 3) duyarlılık
for bw in (20, 120, 250):
    rec(f"beta{bw}", split_stats(resid(d, "y_GDXJ", bw), y3, 3))
rec("bench_GC_F", split_stats(resid(d, "y_GDXJ", 60, bench="y_GC_F"), y3, 3))
rec("2faktor_GLD_SPY", split_stats(resid(d, "y_GDXJ", 60, extra="y__GSPC"), y3, 3))
rec("ham_oran_d1", split_stats(zscale(np.log(d.y_GDXJ / d.y_GLD).diff()), y3, 3))
# 4) ileri gün profili
for k in range(1, 6):
    rec(f"gun_t+{k}", split_stats(x, d["v_ret"].shift(-k), 1), h=1)
# 5) erken dönem spot (2010–2016) ve 2017+ spot, h=1,3,5, üç madenci
for m in ["y_GDX", "y_GDXJ", "y_RING"]:
    xs = resid(sp, m)
    for h in (1, 3, 5):
        for per, a, b in (("erken", "2010-01-01", "2016-12-31"), ("geç", "2017-03-01", "2026-12-31")):
            msk = (sp.index >= a) & (sp.index <= b)
            st = ic(xs[msk], sp[f"sfwd{h}"][msk], max(h, 5))
            yr = yearly_sign_table(xs[msk], sp[f"sfwd{h}"][msk])
            s = dict(ic=st["ic"], t=st["t"], n=st["n"], yrs_same_sign=int((np.sign(yr) == np.sign(st["ic"])).sum()), yrs=int(yr.notna().sum()))
            rec(f"spot_{per}_{m}", s, h=h, fam="s5_erken")
# 6) olay asimetrisi kompozit değil GDXJ: üst/alt %10 (IS kantilleri)
q_lo, q_hi = x[idx <= IS_END].quantile([0.1, 0.9])
for nm, dm in (("ust10", (x > q_hi)), ("alt10", (x < q_lo))):
    e = event_stats(dm.astype(float).where(x.notna()), y3, 3)
    rec(f"olay_{nm}", e)
res = pd.DataFrame(rows); res.to_csv(f"{OUT}/s5_c1_tani.csv", index=False)
pd.set_option("display.width", 250); print(res.round(3).to_string())
print("IS kantilleri:", round(q_lo, 2), round(q_hi, 2))
