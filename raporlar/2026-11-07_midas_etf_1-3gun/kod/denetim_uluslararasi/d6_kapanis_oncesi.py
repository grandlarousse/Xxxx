"""Denetim D6: 'kapanışa bağımlılık' vekil testleri (gün içi veri yok).
(a) Kapanıştan ~10 dk önce giriş vekili: giriş fiyatı = c + f*(h-l) (f = 0,03 / 0,05 / 0,10; kötümser simetrik kayma),
    S1 sepeti ve S2 (EWY) için.
(b) S1 kenarının sinyal günü IBS'ine göre dağılımı (kapanış gün dibinde mi?) — 12 Asya ETF'i.
Çalıştır: python3 -I kod/denetim_uluslararasi/d6_kapanis_oncesi.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import sim
from sim import L
from d1_s1_yeniden import SEPET, EK, s1
from d3_s2_ewy_ibs import s2, my_ibs

def reprice(tr, f):
    out = tr.copy(); g = []
    for _, r in tr.iterrows():
        df = L(r["sym"]); d = r["sig_date"]
        ep = min(df.at[d, "h"], df.at[d, "c"] + f * (df.at[d, "h"] - df.at[d, "l"]))
        g.append(df.at[r["exit"], "c"] / ep - 1)
    out["gross"] = g
    out["net"] = out["gross"] - out["sym"].map(lambda s: sim.cost(s)) / 1e4
    return out

def main():
    t1 = sim.basket(SEPET, s1(), 1, "C0")
    t2 = sim.sim("EWY", s2()("EWY"), 1, "C0")
    rows = []
    for f in (0.0, 0.03, 0.05, 0.10):
        a = sim.summarize(reprice(t1, f), 1); b = sim.summarize(reprice(t2, f), 1, by_date=False)
        rows.append({"f": f, "S1_net_bp": a["net_bp"], "S1_t": a["t_simple"], "S1_oos": a["oos_net_bp"], "S2_net_bp": b["net_bp"], "S2_t": b["t_simple"], "S2_is": b["is_net_bp"]})
        rr = []
    R = pd.DataFrame(rows)
    rng_bp = np.mean([(L(s).at[d, "h"] / L(s).at[d, "l"] - 1) * 1e4 for s, d in zip(t1["sym"], t1["sig_date"])])
    print(f"S1 sinyal günlerinde ort. gün içi aralık {rng_bp:.0f} bp")
    print("=== (a) Kapanış öncesi giriş vekili: giriş = c + f*(h-l) ===")
    print(R.round(2).to_string(index=False))
    R.to_csv(os.path.join(sim.OUT, "d6_kapanis_oncesi.csv"), index=False)
    # (b) IBS dağılımı, 12 Asya ETF'i
    t12 = sim.basket(SEPET + EK, s1(), 1, "C0")
    t12["ibs"] = [my_ibs(L(s)).get(d) for s, d in zip(t12["sym"], t12["sig_date"])]
    print("\n=== (b) S1 (12 Asya ETF) sinyal günü IBS'ine göre ===")
    for lo, hi in ((0, 0.1), (0.1, 0.3), (0.3, 0.6), (0.6, 1.01)):
        p = t12[(t12["ibs"] >= lo) & (t12["ibs"] < hi)]
        if len(p) > 2:
            print(f"  IBS [{lo},{hi}): n={len(p)} brüt {p['gross'].mean()*1e4:.1f} net {p['net'].mean()*1e4:.1f} t {sim.simple_t(p['net'].values):.2f} IS {p[p.sig_date<=sim.IS_END]['net'].mean()*1e4:.1f} OOS {p[p.sig_date>sim.IS_END]['net'].mean()*1e4:.1f}")

if __name__ == "__main__":
    main()

def post_hoc_ibs():
    """POST-HOC (denetimde görüldü, önceden belirlenmemiş): S1 ∩ IBS<0,3 — gün-kümeli; yalnız gelecekte test edilecek hipotez."""
    for nm, syms in (("sepet6", SEPET), ("asya12", SEPET + EK)):
        for mode in ("C0", "O1", "C1"):
            def f(s, base=s1()):
                return base(s) & (my_ibs(L(s)) < 0.3).reindex(L(s).index).fillna(False)
            t = sim.basket(syms, f, 1, mode); r = sim.summarize(t, 1)
            ex = t[~t["sig_date"].isin(t.groupby("sig_date")["net"].mean().nlargest(5).index)]; r2 = sim.summarize(ex, 1)
            print(f"  [post-hoc] {nm} S1&IBS<0.3 {mode} h1: gün {r['n_dates']} işlem {r['n_trades']} net {r['net_bp']:.1f} t {r['t_simple']:.2f} IS {r['is_net_bp']:.1f} OOS {r['oos_net_bp']:.1f} yıl+ {r['years_pos']:.2f} | en iyi 5 gün hariç net {r2['net_bp']:.1f} t {r2['t_simple']:.2f}")

if __name__ == "__main__":
    post_hoc_ibs()
