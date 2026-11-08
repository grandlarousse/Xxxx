#!/usr/bin/env python3
"""Adım 5: ek bağımsız kontroller — yüzdelik tanımı duyarlılığı, IS'te k seçimi, NW t, ham bacaklar, kayıt FDR'ı."""
import sys, numpy as np, pandas as pd, warnings
from scipy import stats as sst
warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a1_zaman_serisi_rep")
from rutil import *
B, SP = load(); r_v = B.v_ret; lp = SP.lp; r = SP.r
rv20 = r.rolling(20).std(); q = exp_pct(rv20)
V = lambda x: asof_to(pd.DataFrame({"x": x}), B.index).x
mom = lambda k: lp - lp.shift(k)
ism = r_v.index <= IS_END
def summ(nm, pc, hs=(1, 5)):
    out = []
    for h in hs:
        o = bt_split(V(pc), r_v, h)
        out.append(f"h{h}: tam {o['full_dm']['sharpe']:.2f} (t {o['full_dm']['t']:.2f}) IS {o['is_dm']['sharpe']:.2f} OOS {o['oos_dm']['sharpe']:.2f} (t {o['oos_dm']['t']:.2f}, NW {o['oos_dm']['t_nw']:.2f}) expo {o['full_dm']['expo']:.2f}")
    m = (SP.index <= "2016-12-31"); e = [round(bt(pc[m], r[m], h, 5.0, demean=True)["sharpe"], 2) for h in hs]
    print(f"{nm:34s}", " | ".join(out), "| erken", e)
print("== LOWMOM: oynaklık yüzdeliği tanımına duyarlılık ==")
summ("genişleyen (taban)", np.sign(mom(5)).where(q < 1/3, 0.0).where(q.notna()))
for w in [250, 500, 750, 1250]:
    qr = rv20.rolling(w, min_periods=int(0.8 * w)).rank(pct=True)
    summ(f"kayan {w} gün", np.sign(mom(5)).where(qr < 1/3, 0.0).where(qr.notna()))
for thr in [0.10, 0.12, 0.14, 0.16]:
    a = rv20 * np.sqrt(252); summ(f"sabit rv20<{thr:.0%}", np.sign(mom(5)).where(a < thr, 0.0).where(a.notna() & (SP.index >= "2011-01-01")))
for t_ in [0.25, 0.5]:
    summ(f"genişleyen q<{t_}", np.sign(mom(5)).where(q < t_, 0.0).where(q.notna()))
print("\n== IS'te k seçimi (LOWMOM, drift çıkarılmış IS Sharpe) ==")
for h in [1, 3, 5]:
    res = {k: (round(bt(V(np.sign(mom(k)).where(q < 1/3, 0.0).where(q.notna()))[ism], r_v[ism], h, 5.0, demean=True)["sharpe"], 2),
               round(bt(V(np.sign(mom(k)).where(q < 1/3, 0.0).where(q.notna()))[~ism], r_v[~ism], h, 5.0, demean=True)["sharpe"], 2)) for k in [1, 2, 3, 5, 10, 20]}
    best = max(res, key=lambda k: res[k][0]); print(f"h{h} (IS, OOS):", res, "→ IS en iyi k =", best, "OOS", res[best][1])
print("\n== VOLREG IS seçimi k∈{1,5,20} ==")
def volreg(k):
    sg = np.sign(mom(k)); return pd.Series(np.where(q < 1/3, sg, np.where(q > 2/3, -sg, 0.0)), index=SP.index).where(q.notna() & sg.notna())
for h in [1, 3, 5]:
    print(f"h{h}", {k: (round(bt(V(volreg(k))[ism], r_v[ism], h, 5.0, demean=True)["sharpe"], 2), round(bt(V(volreg(k))[~ism], r_v[~ism], h, 5.0, demean=True)["sharpe"], 2)) for k in [1, 5, 20]})
print("\n== LOWMOM OOS ham (drift çıkarılmamış) bacaklar ve buy&hold ==")
pv = V(np.sign(mom(5)).where(q < 1/3, 0.0).where(q.notna()))
for h in [1, 5]:
    rr = r_v[~ism]; pp = pv[~ism]
    print(f"h{h}: ham net {bt(pp, rr, h)['sharpe']:.2f} | uzun ham {bt(pp.clip(lower=0), rr, h)['sharpe']:.2f} | kısa ham {bt(pp.clip(upper=0), rr, h)['sharpe']:.2f} | "
          f"yıllık getiri {bt(pp, rr, h)['ann']*100:.1f}% | B&H OOS {bt(pd.Series(1.0, index=rr.index), rr, 1, 0.0)['sharpe']:.2f} yıllık {bt(pd.Series(1.0, index=rr.index), rr, 1, 0.0)['ann']*100:.1f}%")
    # B&H'a koşullu: yalnız aktif günlerde uzun (rejimde her zaman uzun) — sinyalin yön katkısı
    act = (pp != 0).astype(float); print(f"     rejim günlerinde hep uzun (drift çıkarılmış): {bt(act, rr, h, demean=True)['sharpe']:.2f}")
# aktif gün sayısı OOS
print("OOS aktif gün:", int((pv[~ism] != 0).sum()), "/", int((~ism).sum()), "| IS aktif gün:", int((pv[ism] != 0).sum()), "/", int(ism.sum()))
print("\n== Kayıt (analistin registry dosyası) üzerinde kendi BH-FDR hesabım ==")
G = pd.read_csv(f"{S}/out/registry/a1_zaman_serisi.csv")
G["p2"] = 2 * sst.norm.sf(G.t.abs())
def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); qq = p[o] * n / np.arange(1, n + 1); qq = np.minimum.accumulate(qq[::-1])[::-1]; out = np.empty(n); out[o] = np.minimum(qq, 1); return out
prim = G[~G.family.str.startswith("robust")]
print("toplam", len(G), "birincil", len(prim), "sağlamlık", len(G) - len(prim), "| p<0.05:", int((G.p2 < 0.05).sum()), "| |t|>=3:", int((G.t.abs() >= 3).sum()),
      "| min q birincil:", round(float(bh(prim.p2.fillna(1)).min()), 3), "| min q tümü:", round(float(bh(G.p2.fillna(1)).min()), 3), "| t NaN:", int(G.t.isna().sum()))
# kaç test aslında aynı sinyalin tekrarı? (bt ve IC aynı hipotez)
print("en küçük p 5:", prim.sort_values("p2").head(5)[["family", "test_id", "t", "p2"]].to_string(index=False))
