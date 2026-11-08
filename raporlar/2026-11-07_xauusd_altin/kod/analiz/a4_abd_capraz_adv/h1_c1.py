"""h1: C1 / C1b çürütme denemesi.
(a) ham Yahoo'dan bağımsız sinyal (ABD işlem günü bazlı), (b) alt dönemler, (c) 2017 hariç, (d) parametre ızgarası,
(e) backtest t, 10 bps, demeaned, uzun/kısa, (f) Pearson/aykırı değer etkisi, (g) spot hedefle aynı test, (h) GLD/GDXJ zaman kontrolü."""
import sys, json; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a4_abd_capraz_adv")
from adv_common import *
pd.set_option("display.width", 250)
d = load_viop(); sp = load_spot(); idx = d.index
ISM = idx <= IS_END; OOSM = ~ISM
x = miner_resid(d, "y_GDXJ"); pos = tercile(x)
y3 = d.fwd3
R = {}

# ---------- (a) bağımsız sinyal: ham Yahoo, ABD işlem günü getirisi, as-of t'den önceki son ABD günü
def raw(t):
    y = pd.read_parquet(f"{S}/panel/yahoo/{t}.parquet"); y.index = pd.to_datetime(y.index); return y["adjclose"]
g = raw("GDXJ"); l = raw("GLD")
us = pd.concat([g.rename("m"), l.rename("g")], axis=1).dropna()
rm = np.log(us.m).diff(); rg = np.log(us.g).diff()
e = rm - beta(rm, rg, 60, 40) * rg; zu = zscale(e)
# gün t için: tarih < t olan son ABD günü (16:00 ET kapanışı t 15:00 UTC'den önce)
D = pd.Series(us.index, index=us.index)
asof = D.reindex(idx - pd.Timedelta(days=1), method="ffill")
asof.index = idx
x_raw = pd.Series(zu.reindex(asof.values).values, index=idx)
# aynı ABD günü iki VİOP gününe denk gelirse ikinciyi sıfırla (yeni bilgi yok)
dup = asof.duplicated()
x_raw2 = x_raw.where(~dup.values, 0.0)
R["a_bagimsiz"] = dict(panel=split_stats(x, y3, 3), ham_ABDgunu=split_stats(x_raw, y3, 3), ham_tekrar0=split_stats(x_raw2, y3, 3),
                      corr_panel_ham=float(pd.concat([x, x_raw2], axis=1).dropna().corr().iloc[0, 1]))
for k in R["a_bagimsiz"]:
    if isinstance(R["a_bagimsiz"][k], dict): R["a_bagimsiz"][k].pop("by_year", None)
print("(a)", json.dumps(R["a_bagimsiz"], default=float, indent=0)[:1500])

# ---------- (b) alt dönemler: IC, Pearson, backtest
rows = []
for nm, a, b in SUBP + [("IS", "2017-01-01", "2021-12-31"), ("OOS", "2022-01-01", "2026-12-31"), ("full", "2017-01-01", "2026-12-31"),
                        ("2018-21 (2017 hariç IS)", "2018-01-01", "2021-12-31"), ("2018-26 (2017 hariç)", "2018-01-01", "2026-12-31")]:
    m = per_mask(idx, a, b)
    s = ic(x[m], y3[m], 5); p = ic(x[m], y3[m], 5, method="pearson")
    bt5 = bt_stats(pos[m], d.v_ret[m], 3); bt10 = bt_stats(pos[m], d.v_ret[m], 3, 10); dm = bt_stats(pos[m], d.v_ret[m], 3, demean=True)
    lg = bt_stats(pos[m].clip(lower=0), d.v_ret[m], 3); sh = bt_stats(pos[m].clip(upper=0), d.v_ret[m], 3)
    lgd = bt_stats(pos[m].clip(lower=0), d.v_ret[m], 3, demean=True); shd = bt_stats(pos[m].clip(upper=0), d.v_ret[m], 3, demean=True)
    bh = bt_stats(pd.Series(1.0, index=idx[m]), d.v_ret[m], 1, 0)
    rows.append(dict(donem=nm, n=s["n"], ic=round(s["ic"], 3), t=round(s["t"], 2), pear_ic=round(p["ic"], 3), pear_t=round(p["t"], 2),
                     sh5=bt5["sh"], t5=bt5["t"], sh10=bt10["sh"], sh_dm=dm["sh"], long_sh=lg["sh"], long_dm=lgd["sh"], short_sh=sh["sh"], short_dm=shd["sh"], bh_sh=bh["sh"]))
sub = pd.DataFrame(rows); print("(b) alt dönemler\n", sub.to_string()); R["b_altdonem"] = sub.to_dict("records")

# ---------- (d) parametre ızgarası
grid = []
for bw in (20, 40, 60, 120, 250):
    for zw in (60, 120, 250):
        xx = miner_resid(d, "y_GDXJ", bw, zw)
        for h in (1, 2, 3, 4, 5, 7, 10):
            y = fwd(d.v_ret, h)
            s = split_stats(xx, y, h)
            grid.append(dict(bw=bw, zw=zw, h=h, ic=round(s["ic"], 3), t=round(s["t"], 2), t_is=round(s["t_is"], 2), t_oos=round(s["t_oos"], 2)))
G = pd.DataFrame(grid)
print("(d) ızgara t (bw=60,zw=120) h:", G[(G.bw == 60) & (G.zw == 120)][["h", "ic", "t", "t_is", "t_oos"]].to_string(index=False))
piv = G.pivot_table(index=["bw", "zw"], columns="h", values="t"); print("(d) tam t pivot\n", piv.round(2).to_string())
piv_is = G.pivot_table(index=["bw", "zw"], columns="h", values="t_is"); print("(d) IS t pivot\n", piv_is.round(2).to_string())
G.to_csv(f"{OUT}/h1_izgara.csv", index=False)
R["d_izgara_ozet"] = dict(n=len(G), frac_t_gt2=float((G.t > 2).mean()), frac_tis_gt2=float((G.t_is > 2).mean()),
                          h3_frac_t_gt2=float((G[G.h == 3].t > 2).mean()), h3_tis_min=float(G[G.h == 3].t_is.min()), h3_tis_max=float(G[G.h == 3].t_is.max()))
# eşik duyarlılığı (backtest), h=1..5
thr_rows = []
for thr in (0.0, 0.2, 0.3, 0.43, 0.6, 0.8, 1.0, 1.25, 1.5):
    for h in (1, 3, 5):
        p = tercile(x, thr)
        r_is = bt_stats(p[ISM], d.v_ret[ISM], h); r_oos = bt_stats(p[OOSM], d.v_ret[OOSM], h); r_f = bt_stats(p, d.v_ret, h)
        r10 = bt_stats(p[OOSM], d.v_ret[OOSM], h, 10)
        thr_rows.append(dict(thr=thr, h=h, sh_is=r_is["sh"], sh_oos=r_oos["sh"], sh_full=r_f["sh"], t_full=r_f["t"], sh_oos10=r10["sh"], turn=r_f["turn"]))
TH = pd.DataFrame(thr_rows); print("(d) eşik × h backtest\n", TH.to_string(index=False)); R["d_esik"] = TH.to_dict("records")

# komşu madenciler (aynı kural)
nb = []
for m in ["y_GDX", "y_GDXJ", "y_RING", "y_SIL", "y_NEM", "y_AEM", "y_B", "y_KGC", "y_FNV", "y_WPM", "y_RGLD"]:
    if m not in d: continue
    xx = miner_resid(d, m)
    s = split_stats(xx, y3, 3); p = tercile(xx)
    nb.append(dict(m=m, ic=round(s["ic"], 3), t=round(s["t"], 2), t_is=round(s["t_is"], 2), t_oos=round(s["t_oos"], 2),
                   sh_is=bt_stats(p[ISM], d.v_ret[ISM], 3)["sh"], sh_oos=bt_stats(p[OOSM], d.v_ret[OOSM], 3)["sh"]))
NB = pd.DataFrame(nb); print("(d) madenciler h3\n", NB.to_string(index=False)); R["d_madenci"] = NB.to_dict("records")

# ---------- (f) aykırı değer: en büyük |y3| günlerin katkısı (Pearson vs Spearman), x winsor
for q in (0.0, 0.01, 0.025, 0.05):
    yy = y3.clip(y3.quantile(q), y3.quantile(1 - q)) if q > 0 else y3
    xx = x.clip(-3, 3)
    s = ic(xx[ISM], yy[ISM], 5, "pearson"); s2 = ic(xx[OOSM], yy[OOSM], 5, "pearson")
    print(f"(f) winsor y q={q}: Pearson IS t={s['t']:.2f}, OOS t={s2['t']:.2f}")
# sign-only accuracy: P(sign(fwd3)=sign(x)) where |x|>0.43
mm = (x.abs() > 0.43) & y3.notna()
hit = (np.sign(x[mm]) == np.sign(y3[mm])).groupby(idx[mm] <= IS_END).mean(); print("(f) isabet (IS True/OOS False):", hit.round(3).to_dict())

# ---------- (g) spot hedef (15:00→15:00 UTC) aynı dönemde ve erken dönem yıllık; spot backtest alt dönem
xs = miner_resid(sp, "y_GDXJ"); ps = tercile(xs)
srow = []
for nm, a, b in [("2010-12", "2010-01-01", "2012-12-31"), ("2013-16", "2013-01-01", "2016-12-31"), ("2010-16", "2010-01-01", "2016-12-31")] + SUBP:
    m = per_mask(sp.index, a, b)
    s = ic(xs[m], sp.sfwd3[m], 5); p = ic(xs[m], sp.sfwd3[m], 5, "pearson"); b5 = bt_stats(ps[m], sp.s_ret[m], 3)
    srow.append(dict(donem=nm, n=s["n"], ic=round(s["ic"], 3), t=round(s["t"], 2), pear_t=round(p["t"], 2), sh5=b5["sh"], t5=b5["t"]))
SP = pd.DataFrame(srow); print("(g) spot\n", SP.to_string(index=False)); R["g_spot"] = SP.to_dict("records")

# ---------- C1b kompozit alt dönem
def miner_comp(df):
    zs = [miner_resid(df, m) for m in ["y_GDX", "y_GDXJ", "y_RING"]]
    bn = ["y_NEM", "y_AEM", "y_B", "y_KGC", "y_FNV", "y_WPM", "y_RGLD"]
    rb = np.log(df[[c for c in bn if c in df]]).diff().mean(axis=1); rg = np.log(df["y_GLD"]).diff()
    zs.append(zscale(rb - beta(rb, rg, 60, 40) * rg))
    return pd.concat(zs, axis=1).mean(axis=1)
xc = miner_comp(d); pc = np.sign(xc).fillna(0.0)
crow = []
for nm, a, b in SUBP + [("IS", "2017-01-01", "2021-12-31"), ("OOS", "2022-01-01", "2026-12-31"), ("full", "2017-01-01", "2026-12-31")]:
    m = per_mask(idx, a, b)
    s = ic(xc[m], y3[m], 5); p = ic(xc[m], y3[m], 5, "pearson")
    crow.append(dict(donem=nm, ic=round(s["ic"], 3), t=round(s["t"], 2), pear_t=round(p["t"], 2), sh5=bt_stats(pc[m], d.v_ret[m], 3)["sh"], t5=bt_stats(pc[m], d.v_ret[m], 3)["t"],
                     sh10=bt_stats(pc[m], d.v_ret[m], 3, 10)["sh"], sh_dm=bt_stats(pc[m], d.v_ret[m], 3, demean=True)["sh"],
                     long_sh=bt_stats(pc[m].clip(lower=0), d.v_ret[m], 3)["sh"], short_sh=bt_stats(pc[m].clip(upper=0), d.v_ret[m], 3)["sh"]))
CB = pd.DataFrame(crow); print("C1b alt dönem\n", CB.to_string(index=False)); R["c1b_altdonem"] = CB.to_dict("records")
# C1b eşleme duyarlılığı
for nmap, pp in (("isaret", pc), ("tercile", tercile(xc)), ("zkirp", (xc / 2).clip(-1, 1).fillna(0))):
    print("C1b eşleme", nmap, "IS", bt_stats(pp[ISM], d.v_ret[ISM], 3), "OOS", bt_stats(pp[OOSM], d.v_ret[OOSM], 3), "OOS10", bt_stats(pp[OOSM], d.v_ret[OOSM], 3, 10))
xcs = miner_comp(sp)
for nm, a, b in [("2010-16", "2010-01-01", "2016-12-31"), ("2017-26", "2017-03-01", "2026-12-31")]:
    m = per_mask(sp.index, a, b); s = ic(xcs[m], sp.sfwd3[m], 5); print("C1b spot", nm, round(s["ic"], 3), round(s["t"], 2))

json.dump(R, open(f"{OUT}/h1_c1.json", "w"), indent=1, default=float)
