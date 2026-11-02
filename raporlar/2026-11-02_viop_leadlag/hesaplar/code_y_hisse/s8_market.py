"""Adım 8: Piyasa düzeyi öncülük — hisse taramasında 'çok hedefli lider' görünen etkiler aslında tek bir piyasa zamanlaması mı?
(a) 177 lider cc_{t-1} -> XU030 (cc/gap/intra)_t | XU030_{t-1}, XU100_{t-1}; lag 1-2; BH; 50 kaydırma null'u.
(b) Küçük/bireysel faktör: (EW177 - XU100)_{t-k}, k=1..5 -> XU030 gap/intra/cc.
(c) Backtest (XU030 vadelisi, endeks vadelisi maliyeti 3 ve 8 bps): THYAO idiosenkratik_{t-1} -> XU030 gün-içi_t; IS-seçimli lider -> OOS.
Çıktı: res/market.txt
"""
import sys, os, numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata, hreg
sys.path.insert(0, hdata.SCR + "/code"); import ll
D = hdata.load(); cc, gap, intra = D["cc"], D["gap"], D["intra"]
LEAD = [c for c in cc.columns if c not in hdata.IDX]; idx = cc.index; T = len(idx); SPLIT = pd.Timestamp(hdata.SPLIT)
EW = cc[LEAD].mean(axis=1)
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)
per = {"FULL": np.ones(T, bool), "IS": idx < SPLIT, "OOS": idx >= SPLIT}
tg = "XU030"
C1 = pd.concat([cc[tg].shift(1), cc["XU100"].shift(1)], axis=1).values
res = []
for dn, dd in [("cc", cc), ("gap", gap), ("intra", intra)]:
    for k in [1, 2]:
        C = C1 if k == 1 else np.column_stack([C1, cc[tg].shift(k).values])
        for pn, pm in per.items():
            r = hreg.nw_batch(np.where(pm, dd[tg].values, np.nan), cc[LEAD].shift(k).values, C)
            res.append(pd.DataFrame({"leader": LEAD, "dep": dn, "lag": k, "period": pn, "b": r["b"], "t": r["t"], "n": r["n"]}))
R = pd.concat(res); W = R.pivot_table(index=["leader", "dep", "lag"], columns="period", values="t").reset_index()
W["p"] = 2 * stats.norm.sf(W.FULL.abs())
for dn in ["cc", "gap", "intra"]:
    for k in [1, 2]:
        m = (W.dep == dn) & (W.lag == k) & W.FULL.notna()
        rej, _ = ll.fdr(W.loc[m, "p"].values, 0.05); W.loc[m, "bh"] = rej
# null: 50 kaydırma, lag1
rng = np.random.default_rng(3); offs = rng.integers(250, T - 250, 50)
Lv = cc[LEAD].values
nul = {dn: [] for dn in ["cc", "gap", "intra"]}
for o in offs:
    X = pd.DataFrame(np.roll(Lv, o, axis=0), index=idx).shift(1).values
    for dn, dd in [("cc", cc), ("gap", gap), ("intra", intra)]:
        t = hreg.nw_batch(dd[tg].values, X, C1)["t"]; nul[dn].append(t)
P(f"(a) 177 lider cc_t-1 -> {tg} (kontrol {tg}_t-1, XU100_t-1). Aile başına 177 test.")
for dn in ["cc", "gap", "intra"]:
    x = W[(W.dep == dn) & (W.lag == 1)]; nt = np.array(nul[dn])
    P(f"  {dn}: |t|>3 gerçek {int((x.FULL.abs()>3).sum())} / null ort {np.mean((np.abs(nt)>3).sum(1)):.2f}; p<0,05 gerçek {int((x.p<0.05).sum())} / null {np.mean((2*stats.norm.sf(np.abs(nt))<0.05).sum(1)):.1f}; "
      f"BH05 {int(x.bh.sum())}; null'da max|t| ort {np.mean(np.nanmax(np.abs(nt),1)):.2f}")
    xx = x.reindex(x.FULL.abs().sort_values(ascending=False).index).head(8)
    P("   en güçlü: " + "; ".join(f"{a} t={b:.2f} (IS {c:.2f}, OOS {d:.2f})" for a, b, c, d in zip(xx.leader, xx.FULL, xx.IS, xx.OOS)))
    if dn == "intra":
        thy = np.array(nul[dn])[:, LEAD.index("THYAO")]
        P(f"   THYAO intra t gerçek {x.set_index('leader').loc['THYAO','FULL']:.2f}; aynı ofsetlerde THYAO null t dağılımı: ort {np.nanmean(thy):.2f}, sd {np.nanstd(thy):.2f}; "
          f"null'da herhangi bir liderin |t|>=gerçek THYAO olma olasılığı {np.mean(np.nanmax(np.abs(nt),1) >= abs(x.set_index('leader').loc['THYAO','FULL'])):.2f}")
for k in [2]:
    for dn in ["gap"]:
        x = W[(W.dep == dn) & (W.lag == k)]
        P(f"  lag{k} {dn}: |t|>3 {int((x.FULL.abs()>3).sum())}, BH05 {int(x.bh.sum())}, ort t {x.FULL.mean():.2f}")
# (b) EW-XU100 faktörü
P("\n(b) Küçük/bireysel faktör F=(EW177 - XU100)_{t-k} -> XU030 (kontrol XU030_{t-1..t-k}, XU100_{t-1})")
F = EW - cc["XU100"]
for dn, dd in [("gap", gap), ("intra", intra), ("cc", cc)]:
    s = []
    for k in range(1, 6):
        C = np.column_stack([C1] + [cc[tg].shift(i).values for i in range(2, k + 1)])
        tt = [hreg.nw_batch(np.where(pm, dd[tg].values, np.nan), F.shift(k).values.reshape(-1, 1), C)["t"][0] for pm in per.values()]
        bb = hreg.nw_batch(dd[tg].values, F.shift(k).values.reshape(-1, 1), C)["b"][0]
        s.append(f"k={k}: b={bb:.3f} t={tt[0]:.2f} (IS {tt[1]:.2f}/OOS {tt[2]:.2f})")
    P(f"  {dn}: " + " | ".join(s))
# (c) backtest XU030 vadelisi
P("\n(c) Backtest: XU030 gün-içi (VİOP XU030 vadelisi açılış->kapanış yaklaşığı; endeks vadelisi maliyeti 3 ve 8 bps)")
def idio(L):
    d = pd.concat([cc[L], cc["XU100"]], axis=1).dropna(); dI = d[d.index < SPLIT]
    b = np.cov(dI.iloc[:, 0], dI.iloc[:, 1])[0, 1] / dI.iloc[:, 1].var(); return cc[L] - b * cc["XU100"]
for L in ["THYAO", "PGSUS"]:
    sig = idio(L).shift(1)
    for c in [0, 3, 8]:
        r, p = ll.backtest(sig, intra[tg], cost_bps=c)
        P(f"  {L} idio_t-1 işareti -> {tg} gün-içi, maliyet {c}: IS {r['IS'].get('mean_bps',np.nan):.1f}bps SR {r['IS'].get('sharpe',np.nan):.2f} | OOS {r['OOS'].get('mean_bps',np.nan):.1f}bps SR {r['OOS'].get('sharpe',np.nan):.2f} t {r['OOS'].get('t',np.nan):.2f}")
    r, p = ll.backtest(sig, intra[tg], cost_bps=3, mode="z", thr=1.0)
    P(f"  {L} z>1 filtresi maliyet 3: IS {r['IS'].get('mean_bps',np.nan):.1f}bps SR {r['IS'].get('sharpe',np.nan):.2f} | OOS {r['OOS'].get('mean_bps',np.nan):.1f}bps SR {r['OOS'].get('sharpe',np.nan):.2f}; yıllar {r['by_year_bps']}")
# IS seçimli lider (en yüksek IS |t|, intra) -> OOS
x = W[(W.dep == "intra") & (W.lag == 1)].dropna(subset=["IS"]); best = x.reindex(x.IS.abs().sort_values(ascending=False).index).head(5)
P("  IS'de en iyi 5 lider (intra): " + ", ".join(f"{a}({b:.2f}->OOS {c:.2f})" for a, b, c in zip(best.leader, best.IS, best.OOS)))
sig = sum(np.sign(t) * idio(L).shift(1) / idio(L)[idx < SPLIT].std() for L, t in zip(best.leader, best.IS))
for c in [3, 8]:
    r, _ = ll.backtest(sig, intra[tg], cost_bps=c)
    P(f"  IS-seçimli 5 lider sepeti -> {tg} gün-içi maliyet {c}: OOS {r['OOS'].get('mean_bps',np.nan):.1f}bps SR {r['OOS'].get('sharpe',np.nan):.2f} t {r['OOS'].get('t',np.nan):.2f}")
W.to_csv(os.path.join(hdata.RES, "market_leaders.csv"), index=False)
open(os.path.join(hdata.RES, "market.txt"), "w").write("\n".join(out))
# (d) F_{t-2} -> XU030 gap_t: gece pozisyonu (VİOP XU030 vadelisi t-1 kapanışında al, t açılışında sat — akşam seansı var; yaklaşık)
P("\n(d) F=(EW177-XU100)_{t-2} işareti -> XU030 gap_t (gece taşıma)")
g = gap[tg]; s = F.shift(2)
for nm, pos in [("her gece long", pd.Series(1.0, index=idx)), ("F>0 ise long, değilse nakit", (s > 0).astype(float)), ("işaret (long/short)", np.sign(s))]:
    for c in [0, 3]:
        pnl = (pos * g - c / 1e4 * pos.abs()).where(g.notna() & s.notna())
        r = {nm2: pnl[m].dropna() for nm2, m in [("IS", idx < SPLIT), ("OOS", idx >= SPLIT)]}
        P(f"  {nm:28s} maliyet {c}: " + " | ".join(f"{k}: {1e4*v[v!=0].mean():.1f}bps/aktif gün SR={v.mean()/v.std()*np.sqrt(252):.2f} t={ll.nw_t(v[v!=0])[1]:.2f}" for k, v in r.items()))
open(os.path.join(hdata.RES, "market.txt"), "w").write("\n".join(out))
