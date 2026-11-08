"""İddia 3 (kış 14->15 UTC -> fwd1), 4 (C_pre -> fwd3), 5 (büyük S5 -> fwd5) saldırısı.
Alt dönemler (spot panel 2010-16 dahil), komşu parametreler, maliyet, bacaklar, drift, çoklu test."""
from adv_common import *
from scipy import stats as st
v = load_viop(); s = load_spot()
sv = A2.segments(v); ss = A2.segments(s)
def uk_winter(idx): return pd.Series([pd.Timestamp(t.date()).tz_localize("Europe/London").dst() == pd.Timedelta(0) for t in idx], index=idx)
def us_winter(idx): return pd.Series([pd.Timestamp(t.date()).tz_localize("America/New_York").dst() == pd.Timedelta(0) for t in idx], index=idx)
wv, ws = uk_winter(v.index), uk_winter(s.index); uv = us_winter(v.index)
# birleşik hedef: 2010-16 spot sfwd, 2017+ VİOP fwd  (alt dönem tablosu için)
def combo(xv, xs, h):
    out = {}
    for k, (a, b) in SUBP.items():
        if k == "2010-16":
            m = (xs.index >= a) & (xs.index <= b); r = ic(xs[m], s[f"sfwd{h}"][m], max(h, 5))
        else:
            m = (xv.index >= a) & (xv.index <= b); r = ic(xv[m], v[f"fwd{h}"][m], max(h, 5))
        out[k] = (round(r["ic"], 3), round(r["t"], 2), r["n"])
    return out
print("=== İDDİA 3: kış fiks öncesi saat")
r1415v = np.log(v.xau_p15 / v.xau_p14); r1415s = np.log(s.xau_p15 / s.xau_p14)
r1314v = np.log(v.xau_p14 / v.xau_p13); r1314s = np.log(s.xau_p14 / s.xau_p13)
r1315v = np.log(v.xau_p15 / v.xau_p13); r1315s = np.log(s.xau_p15 / s.xau_p13)
r1215v = np.log(v.xau_p15 / v.xau_p12)
base = r1415v.where(wv)
r = ic(base, v.fwd1, 5); print(f"yeniden üretim: IC {r['ic']:.4f} t {r['t']:.2f} n {r['n']}")
print("alt dönemler (2010-16 spot):", combo(base, r1415s.where(ws), 1))
rows = []
for nm, xv, msk in [("kış 14->15 (UK)", r1415v, wv), ("kış 14->15 (ABD DST)", r1415v, uv), ("kış 13->14", r1314v, wv), ("kış 13->15", r1315v, wv), ("kış 12->15 (S5)", r1215v, wv),
                    ("yaz 13->14 (=yaz fiks öncesi)", r1314v, ~wv), ("yaz 14->15", r1415v, ~wv), ("tüm yıl 14->15", r1415v, pd.Series(True, index=v.index))]:
    for h in (1, 3, 5):
        rr = ic(xv.where(msk), v[f"fwd{h}"], max(h, 5)); rows.append(dict(sinyal=nm, h=h, ic=round(rr["ic"], 4), t=round(rr["t"], 2), n=rr["n"]))
print(pd.DataFrame(rows).pivot(index="sinyal", columns="h", values="t").to_string())
# erken dönem komşular
for nm, xs_, msk in [("kış 14->15", r1415s, ws), ("kış 13->14", r1314s, ws), ("kış 13->15", r1315s, ws)]:
    m = s.index < "2017-01-01"; rr = ic(xs_.where(msk)[m], s.sfwd1[m], 5); print(f"  ERKEN {nm} -> sfwd1: IC {rr['ic']:.4f} t {rr['t']:.2f}")
# spot hedefle 2017+ (VİOP yerine) aynı sinyal
m = s.index >= "2017-03-01"; rr = ic(r1415s.where(ws)[m], s.sfwd1[m], 5); print(f"  spot hedef 2017+: IC {rr['ic']:.4f} t {rr['t']:.2f}")
pos = np.sign(base).fillna(0)
for c in (5, 10):
    b = bt_summary(pos, v.v_ret, 1, c)
    print(f"  işaret kuralı cost {c}: full {b['full']['sharpe']} IS {b['is']['sharpe']} OOS {b['oos']['sharpe']} OOS_dm {b['oos']['sharpe_demeaned']}")
for k, (a, bb) in list(SUBP.items())[1:]:
    mm = (v.index >= a) & (v.index <= bb); bt = backtest(pos[mm], v.v_ret[mm], 1, 10); btd = backtest(pos[mm], v.v_ret[mm], 1, 10, demean=True)
    print(f"   {k} 10bps Sharpe {bt['sharpe']:.2f} dm {btd['sharpe']:.2f}")
# kısa bacak demeaned
for nm, p in [("uzun", pos.clip(lower=0)), ("kısa", pos.clip(upper=0))]:
    b = bt_summary(p, v.v_ret, 1, 10); print(f"  {nm} bacak 10bps: full {b['full']['sharpe']} (dm {b['full']['sharpe_demeaned']}) IS {b['is']['sharpe']} OOS {b['oos']['sharpe']} (dm {b['oos']['sharpe_demeaned']})")

print("\n=== İDDİA 4: C_pre -> fwd3")
x4 = sv.C_pre; r = ic(x4, v.fwd3, 5); print(f"yeniden üretim: IC {r['ic']:.4f} t {r['t']:.2f}")
print("alt dönemler h=3:", combo(x4, ss.C_pre, 3))
for nm in ("C_pre", "C_day", "S3_asia", "S4_lon", "S5_nyam", "C_full"):
    print(f"  {nm}: " + " ".join(f"h{h} t {ic(sv[nm], v[f'fwd{h}'], max(h,5))['t']:.2f}" for h in (1, 3, 5)) + " | erken h3 t " + f"{ic(ss[nm][s.index<'2017-01-01'], s.sfwd3[s.index<'2017-01-01'], 5)['t']:.2f}")
pos4 = np.sign(x4).fillna(0)
for c in (5, 10):
    b = bt_summary(pos4, v.v_ret, 3, c); print(f"  işaret kuralı h3 cost {c}: full {b['full']['sharpe']} (dm {b['full']['sharpe_demeaned']}) IS {b['is']['sharpe']} OOS {b['oos']['sharpe']} (dm {b['oos']['sharpe_demeaned']})")
for nm, p in [("uzun", pos4.clip(lower=0)), ("kısa", pos4.clip(upper=0))]:
    b = bt_summary(p, v.v_ret, 3, 10); print(f"  {nm} bacak 10bps: full {b['full']['sharpe']} (dm {b['full']['sharpe_demeaned']}) OOS {b['oos']['sharpe']} (dm {b['oos']['sharpe_demeaned']})")
bh = bt_summary(pd.Series(1.0, index=v.index), v.v_ret, 1, 0); print("  B&H VİOP: full", bh["full"]["sharpe"], "IS", bh["is"]["sharpe"], "OOS", bh["oos"]["sharpe"])
for k, (a, bb) in list(SUBP.items())[1:]:
    mm = (v.index >= a) & (v.index <= bb); bt = backtest(pos4[mm], v.v_ret[mm], 3, 10); btd = backtest(pos4[mm], v.v_ret[mm], 3, 10, demean=True)
    print(f"   {k} 10bps Sharpe {bt['sharpe']:.2f} dm {btd['sharpe']:.2f}")

print("\n=== İDDİA 5: büyük S5 hareketi -> fwd5")
x5 = sv.S5_nyam; xs5 = ss.S5_nyam
grid = []
for q in (0.75, 0.8, 0.85, 0.9, 0.95):
    thr = x5[x5.index <= IS_END].abs().quantile(q); big = x5.where(x5.abs() > thr)
    thr_s = xs5[xs5.index < "2017-01-01"].abs().quantile(q); bigs = xs5.where(xs5.abs() > thr_s)
    for h in (1, 3, 5, 10):
        rr = ic(big, v[f"fwd{h}"], max(h, 5))
        ri = ic(big[big.index <= IS_END], v[f"fwd{h}"][v.index <= IS_END], max(h, 5)); ro = ic(big[big.index > IS_END], v[f"fwd{h}"][v.index > IS_END], max(h, 5))
        me = s.index < "2017-01-01"; re = ic(bigs[me], s[f"sfwd{h}"][me], max(h, 5)) if h != 10 or "sfwd10" in s else dict(t=np.nan)
        grid.append(dict(q=q, h=h, ic=round(rr["ic"], 3), t=round(rr["t"], 2), t_is=round(ri["t"], 2), t_oos=round(ro["t"], 2), t_erken=round(re["t"], 2), n=rr["n"]))
G = pd.DataFrame(grid); print(G.to_string()); G.to_csv(f"{OUT}/adv3_bigmove_grid.csv", index=False)
thr = x5[x5.index <= IS_END].abs().quantile(0.9); big = x5.where(x5.abs() > thr)
print("alt dönemler q90 h5:", combo(big, xs5.where(xs5.abs() > xs5[xs5.index < '2017-01-01'].abs().quantile(0.9)), 5))
pos5 = np.sign(big).fillna(0)
for c in (5, 10):
    b = bt_summary(pos5, v.v_ret, 5, c); print(f"  kural h5 cost {c}: full {b['full']['sharpe']} (dm {b['full']['sharpe_demeaned']}) IS {b['is']['sharpe']} OOS {b['oos']['sharpe']} (dm {b['oos']['sharpe_demeaned']})")
for nm, p in [("uzun", pos5.clip(lower=0)), ("kısa", pos5.clip(upper=0))]:
    b = bt_summary(p, v.v_ret, 5, 10); print(f"  {nm} bacak 10bps: full {b['full']['sharpe']} (dm {b['full']['sharpe_demeaned']}) IS {b['is']['sharpe']} OOS {b['oos']['sharpe']} (dm {b['oos']['sharpe_demeaned']})")
print("  sinyal sayısı/yıl:", round((pos5 != 0).groupby(v.index.year).sum().mean(), 1), " uzun/kısa oranı OOS:", int((pos5[pos5.index > IS_END] > 0).sum()), "/", int((pos5[pos5.index > IS_END] < 0).sum()))
# 2026 hariç (çöküş)
m = v.index < "2026-01-01"; rr = ic(big[m], v.fwd5[m], 5); print(f"  2026 hariç: IC {rr['ic']:.3f} t {rr['t']:.2f}")
mm = ~(((v.index >= "2020-03-01") & (v.index <= "2020-03-31")) | ((v.index >= "2026-01-01") & (v.index <= "2026-02-28")))
rr = ic(big[mm], v.fwd5[mm], 5); print(f"  uç dönemler hariç: IC {rr['ic']:.3f} t {rr['t']:.2f}")

print("\n=== Çoklu test")
reg = pd.concat([pd.read_csv(f) for f in __import__("glob").glob(f"{S}/out/registry/*.csv")], ignore_index=True)
reg = reg[np.isfinite(reg.p)]
N = len(reg); print("toplam proje test sayısı (p sonlu):", N, " | a2:", int((reg.agent == "a2_seans_gunici").sum()))
reg["q_global"] = bh_fdr(reg.p.values)
a2 = reg[reg.agent == "a2_seans_gunici"].copy(); a2["q_a2"] = bh_fdr(a2.p.values)
ids = ["b_mean_S2_late", "c_ebr_tm1_rel_h5", "c_ebr_tm1_rel_h3", "d_rpre_kis_h1", "a_C_pre_h3", "a_S5big_h5"]
for i in ids:
    rr = a2[a2.test_id == i].iloc[-1]; g = reg.loc[rr.name]
    print(f"  {i}: t {rr.t:.2f} p {rr.p:.2e} | Bonf a2 (x{len(a2)}) {min(1, rr.p*len(a2)):.3g} | BH a2 q {rr.q_a2:.3g} | Bonf global (x{N}) {min(1, rr.p*N):.3g} | BH global q {g.q_global:.3g}")
print("  Bonferroni %5 eşiği |t|: a2", round(st.norm.ppf(1 - 0.025 / len(a2)), 2), " global", round(st.norm.ppf(1 - 0.025 / N), 2))
