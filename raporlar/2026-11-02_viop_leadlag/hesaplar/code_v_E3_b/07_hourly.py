import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b")
"""07: Giriş zamanı gerçekçiliği (saatlik 2023-11+ ve 5 dk son 60 gün). Çıkış: günlük kapanış (Yahoo daily c, kapanış seansı)."""
import vb, numpy as np, pandas as pd
F = pd.read_parquet(vb.RES + "/F.parquet"); s = F["A_USREF"]
z = vb.zsig(s.dropna(), 250)
cal = F.index; tu = vb.bist_dec("TUPRS.IS", cal); xu = vb.bist_dec("XU100.IS", cal)
def hb(sym):
    h = vb.raw(sym, "h1").copy(); h.index = pd.DatetimeIndex(h.index).tz_convert("UTC")
    h["d"] = h.index.tz_localize(None).normalize(); h["hm"] = h.index.strftime("%H:%M"); return h
H = hb("TUPRS.IS"); HX = hb("XU100.IS")
def at(h, hm):  # o barının kapanışı
    g = h[h.hm == hm]; return pd.Series(g.c.values, index=g.d.values)
W = pd.DataFrame(index=pd.DatetimeIndex(sorted(H.d.unique())))
W = W[W.index.isin(cal)]
W["o"] = tu.o.reindex(W.index); W["c"] = tu.c.reindex(W.index)
W["p0730"] = at(H, "06:30").reindex(W.index); W["p0830"] = at(H, "07:30").reindex(W.index); W["p1030"] = at(H, "09:30").reindex(W.index)
W["xo"] = xu.o.reindex(W.index); W["xc"] = xu.c.reindex(W.index); W["x0730"] = at(HX, "06:30").reindex(W.index); W["x0830"] = at(HX, "07:30").reindex(W.index)
W["E0"] = np.log(W.c / W.o); W["E1"] = np.log(W.c / W.p0730); W["E2"] = np.log(W.c / W.p0830); W["E3"] = np.log(W.c / W.p1030)
W["S01"] = np.log(W.p0730 / W.o); W["S12"] = np.log(W.p0830 / W.p0730)
W["H0"] = W.E0 - np.log(W.xc / W.xo); W["H1"] = W.E1 - np.log(W.xc / W.x0730); W["H2"] = W.E2 - np.log(W.xc / W.x0830)
W["z"] = z.reindex(W.index); W["sig"] = s.reindex(W.index)
W = W.dropna(subset=["E0", "E1", "z"])
print("örneklem:", W.index.min().date(), "->", W.index.max().date(), "gün", len(W))
pos = np.sign(W.z).where(W.z.abs() > 1, 0.0); a = pos != 0
for k in ["E0", "E1", "E2", "E3", "S01", "S12", "H0", "H1", "H2"]:
    p = (pos * W[k])[a & W[k].notna()]
    legs = 2 if k.startswith("H") else 1
    _, t, n = vb.nw(W[k], W[["sig"]])
    print(f"  {k}: |z|>1 brüt {1e4*p.mean():6.1f} bps (t {vb.tstat(p):.2f}, n {len(p)}), net 8x{legs}: {1e4*p.mean()-8*legs:6.1f}, net 15x{legs}: {1e4*p.mean()-15*legs:6.1f} | regresyon NW t {t['sig']:.2f} (n {n})")
# 5 dk: son 60 gün, açılış payı
M = vb.raw("TUPRS.IS", "m5").copy(); M.index = pd.DatetimeIndex(M.index).tz_convert("UTC"); M["d"] = M.index.tz_localize(None).normalize(); M["hm"] = M.index.strftime("%H:%M")
def m5(hm): g = M[M.hm == hm]; return pd.Series(g.c.values, index=g.d.values)
Q = pd.DataFrame({"o": tu.o, "c": tu.c}).reindex(pd.DatetimeIndex(sorted(M.d.unique())))
Q["auc"] = m5("06:55")
for hm in ["07:00", "07:10", "07:25", "07:55"]: Q["p" + hm] = m5(hm)
Q["z"] = z.reindex(Q.index); Q = Q.dropna()
print("\n5 dk örneklem gün:", len(Q), "| Yahoo daily o == 06:55 müzayede barı kapanışı oranı:", round((np.isclose(Q.o, Q.auc, rtol=1e-4)).mean(), 3))
pq = np.sign(Q.z).where(Q.z.abs() > 1, 0.0); aq = pq != 0
for hm in ["07:00", "07:10", "07:25", "07:55"]:
    r = np.log(Q.c / Q["p" + hm]); print(f"  giriş {hm} barı kapanışı (+5dk): |z|>1 brüt {1e4*(pq*r)[aq].mean():.1f} bps n {aq.sum()} | açılıştan: {1e4*(pq*np.log(Q.c/Q.o))[aq].mean():.1f}")
