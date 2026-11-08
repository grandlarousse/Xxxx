"""Denetim D4: aile lead-lag iddialarının bağımsız yeniden hesabı.
r_T(t+1..t+h) = a + b*r_L(t) + c*r_T(t) + e   (kendi gecikmesi kontrollü, NW SE, gecikme=h)
Ayrıca: öncünün ek katkısı (b) ve basit eşik kuralı (öncü z>=+1 / <=-1 -> hedef al, C0) maliyet sonrası.
Çalıştır: python3 -I kod/denetim_uluslararasi/d4_leadlag.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import sim
from sim import L

def leader_series(name):
    if name == "VIX_dlog": return np.log(sim.lib.vol_index("VIX")).diff()
    if name == "DFII10_d": return sim.lib.fred("DFII10").diff()
    return L(name)["c"].pct_change()

def ols_nw(y, X, lags):
    n, k = X.shape
    XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ y; e = y - X @ b
    S = (X * e[:, None]).T @ (X * e[:, None]) / n
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1)
        G = (X[l:] * e[l:, None]).T @ (X[:-l] * e[:-l, None]) / n
        S += w * (G + G.T)
    V = n * XtX @ S @ XtX
    return b, b / np.sqrt(np.diag(V))

def test(target, leader, h):
    c = L(target)["c"]; rT = c.pct_change()
    fwd = (c.shift(-h) / c - 1)
    rL = leader_series(leader).reindex(c.index)
    d = pd.DataFrame({"y": fwd, "rL": rL, "rT": rT}).dropna()
    d = d.iloc[60:]
    out = {"target": target, "leader": leader, "h": h, "n": len(d)}
    for nm, part in (("", d), ("_is", d[d.index <= sim.IS_END]), ("_oos", d[d.index > sim.IS_END])):
        X = np.column_stack([np.ones(len(part)), part["rL"].to_numpy(), part["rT"].to_numpy()])
        b, t = ols_nw(part["y"].to_numpy(), X, h)
        out["b" + nm] = b[1]; out["t" + nm] = t[1]; out["own_t" + nm] = t[2]
        if nm == "": out["bp_per_sd"] = b[1] * part["rL"].std() * 1e4
    # ek katkı: yalnız kendi gecikmesi modeline göre R2 artışı (bilgi)
    return out

PAIRS = [("EWY", "TIP"), ("EWT", "TIP"), ("EWJ", "GDX"), ("EEM", "KWEB"), ("IEMG", "KWEB"), ("FXI", "EEM"), ("EWA", "IWM"),
         ("EWA", "VIX_dlog"), ("EWH", "LQD"), ("DXJ", "QQQ"), ("CWEB", "EEM"), ("EWY", "DFII10_d"), ("EWT", "DFII10_d"),
         ("ASHR", "XLE"), ("CQQQ", "XLE"), ("EWY", "SMH"), ("EWY", "SPY"), ("EWJ", "SPY"), ("EWT", "QQQ"), ("FXI", "KWEB")]

def rule(target, leader, z_thr, side):
    c = L(target)["c"]; rL = leader_series(leader).reindex(c.index)
    z = rL / rL.rolling(60).std()
    sg = (z >= z_thr) if side > 0 else (z <= -z_thr)
    sg = sg.fillna(False); sg.iloc[:200] = False
    tr = sim.sim(target, sg, 1, "C0")
    return sim.summarize(tr, 1, by_date=False)

def main():
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
    R = []
    for T, Ld in PAIRS:
        for h in (1, 3):
            R.append(test(T, Ld, h))
    R = pd.DataFrame(R)
    print("=== Gecikmeli regresyon (kendi gecikmesi kontrollü, NW) ===")
    print(R[["target", "leader", "h", "n", "t", "t_is", "t_oos", "own_t", "bp_per_sd"]].round(2).to_string(index=False))
    R.to_csv(os.path.join(sim.OUT, "d4_leadlag.csv"), index=False)
    # karşılaştırma: tarama dosyası
    sw = pd.read_csv(os.path.join(sim.ROOT, "sonuclar", "leadlag_sweep.csv"))
    m = sw.set_index(["target", "leader"])
    print("\nTarama ile karşılaştırma (lag_t_h1 / lag_t_h3):")
    for T, Ld in PAIRS:
        if (T, Ld) in m.index:
            a = m.loc[(T, Ld)]
            mine1 = R[(R.target == T) & (R.leader == Ld) & (R.h == 1)]["t"].iloc[0]; mine3 = R[(R.target == T) & (R.leader == Ld) & (R.h == 3)]["t"].iloc[0]
            print(f"  {T}<-{Ld}: tarama h1 {a['lag_t_h1']:.2f} / benim {mine1:.2f};  tarama h3 {a['lag_t_h3']:.2f} / benim {mine3:.2f}; cost {sim.cost(T):.0f} bp")
    # eşik kuralları (öncü sinyalinin işaretine göre)
    print("\n=== Eşik kuralı (öncü z, C0 h1, 2.500$) ===")
    K = []
    for T, Ld, side in (("EEM", "KWEB", +1), ("EEM", "KWEB", -1), ("EWY", "TIP", +1), ("EWT", "TIP", +1), ("EWA", "IWM", +1), ("EWA", "VIX_dlog", -1),
                        ("EWY", "DFII10_d", -1), ("FXI", "EEM", -1), ("DXJ", "QQQ", -1)):
        for zt in (1.0, 1.5, 2.0):
            r = rule(T, Ld, zt, side); r.update(target=T, leader=Ld, side=side, z=zt); K.append(r)
    K = pd.DataFrame(K)
    print(K[["target", "leader", "side", "z", "n_trades", "gross_bp", "net_bp", "t_simple", "is_net_bp", "oos_net_bp", "years_pos"]].round(2).to_string(index=False))
    K.to_csv(os.path.join(sim.OUT, "d4_leadlag_kural.csv"), index=False)
    # aile içi FDR (lag_t_h1 + lag_t_h3, iki yönlü, normal yaklaşım)
    import ortak_fam
    fam = sw[sw["target"].isin(ortak_fam.FAM)]
    from scipy import stats as st
    p = np.concatenate([2 * st.norm.sf(fam["lag_t_h1"].abs()), 2 * st.norm.sf(fam["lag_t_h3"].abs())])
    print(f"\nAile içi lag testleri: {len(p)} p; BH q=0.10 geçen: {int(sim.bh(p).sum())}; en küçük p {np.nanmin(p):.2e}; Bonferroni eşiği {0.05/len(p):.2e}")
    # IS ve OOS aynı işaretli ve |t|>=2 olanlar
    for hh in ("h1", "h3"):
        q = fam[(np.sign(fam[f"lag_t_{hh}_is"]) == np.sign(fam[f"lag_t_{hh}_oos"])) & (fam[f"lag_t_{hh}_is"].abs() >= 2) & (fam[f"lag_t_{hh}_oos"].abs() >= 2)]
        print(f"  {hh}: IS ve OOS'ta |t|>=2 ve aynı işaret: {len(q)} çift ->", q[["target", "leader", f"lag_t_{hh}", f"lag_bp_per_sd_{hh}"]].round(2).values.tolist()[:12])

if __name__ == "__main__":
    main()
