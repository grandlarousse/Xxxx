"""Çin hissesi iddiaları: analist örneklemi (2018-03+), placebo, kontrollü NW, spot hedef, 2010-2016 erken spot tekrarı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a6_akis_konum_cin_rep")
from r0_base import *
from r1_cn import stock_resid, daily_ret, STK
T = viop_target(); days = T.index; r = T.ret
F = pd.read_parquet(f"{OUT}/r1_features_viop.parquet"); M = pd.read_parquet(f"{OUT}/r3_mimic_features.parquet")
pd.set_option("display.width", 250)

print("== 1) Analist örneklemi (>=2018-03-20) üzerinde mimic ve benim inşam")
for k, h in [("comp", 5), ("res_600547.SS", 5), ("comp_sum5", 1)]:
    for lab, x in [("mimic", M[k]), ("mine", F[k])]:
        xx = x.where(x.index >= "2018-03-20"); st = split(xx, T[f"fwd{h}"], h)
        pos = np.sign(xx).fillna(0.0); o = periods(pos, r, h, 5.0)
        print(f"  {k:14s} h{h} {lab:5s} IC {st['ic']:.3f} t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f} yrs {st['yrs']}  ShIS {o['is']['LS']:.2f} ShOOS {o['oos']['LS']:.2f} dm {o['oos']['LS_dm']:.2f} BH_OOS {o['oos']['bh']:.2f}")

print("== 2) Placebo: x'i k gün kaydır (k>0 daha eski bilgi, k<0 gelecek)")
for k, h in [("comp", 1), ("comp", 5), ("res_600547.SS", 5)]:
    print(f"  {k} h{h}:", {s: round(ic_t(F[k].shift(s), T[f'fwd{h}'], max(h, 5))['ic'], 4) for s in (-1, 0, 1, 2, 3)})

print("== 3) Kontrollü NW regresyon: fwd_h ~ z(x) + spot r(15->15) + spot r(5g) + spot r(07->15, t) + VİOP r_{t-1} + spot r(07->07)")
G15 = pd.Series(gold_at(days + pd.Timedelta(hours=15)), index=days); G07 = pd.Series(gold_at(days + pd.Timedelta(hours=7)), index=days)
C = pd.DataFrame({"s_r1": np.log(G15 / G15.shift(1)), "s_r5": np.log(G15 / G15.shift(5)), "s_0715": np.log(G15 / G07), "v_r1": r.shift(1), "g0707": np.log(G07 / G07.shift(1))})
for k, h in [("comp", 5), ("res_600547.SS", 5)]:
    x = F[k]; xz = (x - x.mean()) / x.std()
    for lab, m in [("tam", days == days), ("IS", days <= IS_END), ("OOS", days > IS_END)]:
        d = pd.concat([T[f"fwd{h}"].rename("y"), xz.rename("x"), C], axis=1)[m].dropna()
        b, t, n = nw_t(d.y.values, np.column_stack([np.ones(len(d)), d.drop(columns="y").values]), max(h, 5))
        print(f"  {k} h{h} {lab}: b(x)={b[1]*1e4:.1f} bps/σ  t={t[1]:.2f} n={n}")
print("  corr(comp_t, spot 07->15 aynı gün) =", round(F.comp.corr(C.s_0715), 3), "| corr(comp_t, spot 15(t-1)->07(t)) =", round(F.comp.corr(np.log(G07 / G15.shift(1))), 3))

print("== 4) Spot hedef (VİOP günleri, spot 15:00->15:00 UTC)")
sret = np.log(G15 / G15.shift(1))
for k, h in [("comp", 5), ("res_600547.SS", 5), ("comp", 3)]:
    y = sum(sret.shift(-j) for j in range(1, h + 1)); st = split(F[k], y, h)
    print(f"  {k} h{h}: IC {st['ic']:.3f} t {st['t']:.2f} IS {st['t_is']:.2f} OOS {st['t_oos']:.2f}")

print("== 5) Erken dönem 2010-2016: spot takvim (Dukascopy 15:00 UTC fiyatı olan hafta içi günler)")
bd = pd.bdate_range("2009-06-01", "2017-01-31")
p15 = pd.Series(gold_at(bd + pd.Timedelta(hours=15), max_stale_h=1.0), index=bd).dropna()
sdays = p15.index; sr = np.log(p15).diff()
print("  spot gün sayısı 2010-2016:", int(((sdays >= "2010-01-01") & (sdays <= "2016-12-31")).sum()))
E = pd.DataFrame(index=sdays)
for tk in STK:
    e, d = stock_resid(tk); E[f"res_{tk}"] = e.reindex(sdays)
E["comp"] = E[[f"res_{tk}" for tk in STK]].mean(axis=1).where(E[[f"res_{tk}" for tk in STK]].notna().sum(axis=1) >= 2)
E["comp_sum5"] = E["comp"].rolling(5, min_periods=3).sum()
rH, _ = daily_ret("_HSI"); E["r_HSI"] = rH.reindex(sdays)
msk = (sdays >= "2010-01-01") & (sdays <= "2016-12-31")
for k, h in [("comp", 5), ("comp", 3), ("res_600547.SS", 5), ("comp_sum5", 1), ("r_HSI", 3), ("r_HSI", 1)]:
    y = sum(sr.shift(-j) for j in range(1, h + 1))
    st = ic_t(E[k][msk], y[msk], max(h, 5))
    d = pd.concat([E[k][msk].rename("x"), y[msk].rename("y")], axis=1).dropna()
    yr = d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y, method="spearman"))
    print(f"  {k:14s} h{h}: IC {st['ic']:.3f} t {st['t']:.2f} n {st['n']} yıllar {dict(yr.round(3))}")
