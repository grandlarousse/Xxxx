"""Denetim D3: uluslararasi_S2 (EWY IBS<0,10 ve düşüş günü -> C0 al, t+1 kapanışı sat) bağımsız yeniden üretim + sağlamlık.
IBS kendi hesabım (lib.ibs değil). Ham h/l verisinin kalitesi (eksik/0/kapanışa eşit) kontrol edilir.
Çalıştır: python3 -I kod/denetim_uluslararasi/d3_s2_ewy_ibs.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import sim
from sim import L

rng = np.random.default_rng(7)

def my_ibs(df):
    r = df["h"] - df["l"]
    return ((df["c"] - df["l"]) / r.where(r > 0)).clip(0, 1)

def s2(thr=0.10, down=True, warm=200):
    def f(s):
        df = L(s); m = my_ibs(df) < thr
        if down: m &= df["c"] < df["c"].shift(1)
        m = m.fillna(False); m.iloc[:warm] = False
        return m
    return f

def main():
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
    # ham veri kalitesi
    raw = pd.read_parquet(os.path.join(sim.ROOT, "data", "etf", "EWY.parquet"))
    print("EWY ham satır:", len(raw), " h/l eksik ya da 0:", int(((raw["h"] <= 0) | raw["h"].isna() | (raw["l"] <= 0) | raw["l"].isna()).sum()),
          " l==c:", int((raw["l"] == raw["c"]).sum()), " h==l:", int((raw["h"] == raw["l"]).sum()))
    df = L("EWY"); ib = my_ibs(df)
    sg = s2()("EWY")
    print("Sinyal günlerinde IBS==0 (kapanış=dip) oranı:", round(float((ib[sg] == 0).mean()), 3))
    rows = []
    for h in (1, 2, 3):
        for mode in ("C0", "O1", "C1"):
            tr = sim.sim("EWY", sg, h, mode); r = sim.summarize(tr, h, by_date=False); r.update(sym="EWY", h=h, mode=mode); rows.append(r)
    for pos in (1000, 10000):
        tr = sim.sim("EWY", sg, 1, "C0", pos=pos); r = sim.summarize(tr, 1, by_date=False); r.update(sym=f"EWY poz={pos}", h=1, mode="C0"); rows.append(r)
    for ex in (5, 10):
        tr = sim.sim("EWY", sg, 1, "C0", extra_bp=ex); r = sim.summarize(tr, 1, by_date=False); r.update(sym=f"EWY +{ex}bp kayma", h=1, mode="C0"); rows.append(r)
    P = pd.DataFrame(rows)
    cols = ["sym", "mode", "h", "n_trades", "gross_bp", "net_bp", "t_simple", "win", "pf", "maxdd", "worst_bp", "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp", "oos_t", "years_pos"]
    print("\n=== S2 yeniden üretim ==="); print(P[cols].round(2).to_string(index=False))
    P.to_csv(os.path.join(sim.OUT, "d3_s2_yeniden.csv"), index=False)

    tr = sim.sim("EWY", sg, 1, "C0")
    y = tr.groupby(tr["sig_date"].dt.year)["net"].agg(["count", "mean", "sum"]); y[["mean", "sum"]] *= 1e4
    print("\nYıl yıl:"); print(y.round(1).to_string())
    A = []
    def add(nm, t):
        r = sim.summarize(t, 1, by_date=False); r["set"] = nm; A.append(r)
    add("tam", tr)
    for ex in ([2020], [2022], [2026], [2020, 2022], [2020, 2026]):
        add(f"{ex} hariç", tr[~tr["sig_date"].dt.year.isin(ex)])
    add("en iyi 5 hariç", tr.drop(tr["net"].nlargest(5).index))
    add("en iyi 10 hariç", tr.drop(tr["net"].nlargest(10).index))
    A = pd.DataFrame(A)
    print("\n=== Alt örnekler ==="); print(A[["set", "n_trades", "gross_bp", "net_bp", "t_simple", "is_net_bp", "oos_net_bp", "years_pos"]].round(2).to_string(index=False))
    A.to_csv(os.path.join(sim.OUT, "d3_s2_altornek.csv"), index=False)
    # en büyük 5 kazanç
    T = tr.sort_values("net", ascending=False).head(6).copy()
    T["r_t"] = [(df["c"].loc[d] / df["c"].shift(1).loc[d] - 1) * 1e4 for d in T["sig_date"]]
    T["gap"] = [(df["o"].shift(-1).loc[d] / df["c"].loc[d] - 1) * 1e4 for d in T["sig_date"]]
    T["koru_x"] = [(L("KORU")["c"].shift(-1).loc[d] / L("KORU")["c"].loc[d] - 1) * 1e4 if d in L("KORU").index else np.nan for d in T["sig_date"]]
    T["gross"] *= 1e4; T["net"] *= 1e4
    print("\nEn büyük kazançlar (KORU aynı gün getirisi ~3x tutarlılık kontrolü):"); print(T[["sig_date", "exit", "r_t", "gross", "net", "gap", "koru_x"]].round(1).to_string(index=False))

    # komşuluk
    G = []
    for thr in (0.05, 0.075, 0.10, 0.125, 0.15, 0.20):
        for down in (True, False):
            t2 = sim.sim("EWY", s2(thr, down)("EWY"), 1, "C0"); r = sim.summarize(t2, 1, by_date=False); r.update(thr=thr, down=down); G.append(r)
    G = pd.DataFrame(G)
    print("\n=== Komşuluk (EWY C0 h1) ==="); print(G[["thr", "down", "n_trades", "gross_bp", "net_bp", "t_simple", "is_net_bp", "oos_net_bp", "years_pos"]].round(2).to_string(index=False))
    G.to_csv(os.path.join(sim.OUT, "d3_s2_komsuluk.csv"), index=False)

    # permütasyon: (a) rastgele gün, (b) yalnız düşüş günlerinden rastgele (aynı sayı)
    nxt = (df["c"].shift(-1) / df["c"] - 1 - sim.cost("EWY") / 1e4)
    elig = nxt.iloc[200:-1].dropna()
    dn = elig[(df["c"] < df["c"].shift(1)).reindex(elig.index)]
    obs = tr["net"].mean(); n = len(tr); NP = 5000
    pa = (np.sum([rng.choice(elig.values, n, replace=False).mean() >= obs for _ in range(NP)]) + 1) / (NP + 1)
    pb = (np.sum([rng.choice(dn.values, n, replace=False).mean() >= obs for _ in range(NP)]) + 1) / (NP + 1)
    # (c) yıl içi permütasyon: sinyal sayısını yıl başına koru (2026 oynaklığını kontrol eder)
    cnt = tr.groupby(tr["sig_date"].dt.year).size()
    pcs = []
    for _ in range(NP):
        v = []
        for yr, k in cnt.items():
            pool = dn[dn.index.year == yr].values
            v.append(rng.choice(pool, min(k, len(pool)), replace=False))
        pcs.append(np.concatenate(v).mean())
    pcs = np.array(pcs); pc = (np.sum(pcs >= obs) + 1) / (NP + 1)
    print(f"\nPermütasyon (EWY C0 h1, net {obs*1e4:.1f} bp, n={n}): (a) rastgele gün p={pa:.4f}; (b) düşüş günlerinden p={pb:.4f}; (c) yıl-tabakalı düşüş günleri p={pc:.4f} (sim ort {pcs.mean()*1e4:.1f})")
    pd.DataFrame({"perm": ["a_rastgele", "b_dusus_gunu", "c_yil_tabakali_dusus"], "p": [pa, pb, pc], "obs_bp": obs * 1e4}).to_csv(os.path.join(sim.OUT, "d3_s2_permutasyon.csv"), index=False)

    # aynı kural diğer Asya ETF'lerinde ve kopya KORU
    O = []
    for s in ["EWT", "EWJ", "FXI", "EWA", "EWH", "INDA", "EEM", "EWZ", "VGK", "EFA", "ASHR", "CQQQ", "EWS", "KWEB", "SPY", "QQQ"]:
        try:
            t2 = sim.sim(s, s2()(s), 1, "C0"); r = sim.summarize(t2, 1, by_date=False); r.update(sym=s); O.append(r)
        except Exception as e:
            print("atla", s, e)
    O = pd.DataFrame(O)
    print("\n=== Aynı kural diğer ETF'lerde (C0 h1) ==="); print(O[["sym", "n_trades", "gross_bp", "net_bp", "t_simple", "is_net_bp", "oos_net_bp"]].round(2).to_string(index=False))
    O.to_csv(os.path.join(sim.OUT, "d3_s2_diger.csv"), index=False)
    # S1 ile örtüşme
    s1tr = pd.read_csv(os.path.join(sim.OUT, "d1_s1_islemler.csv"), parse_dates=["sig_date"])
    ov = set(s1tr[s1tr["sym"] == "EWY"]["sig_date"]) & set(tr["sig_date"])
    print(f"\nS2 ile S1(EWY) aynı gün sinyali: {len(ov)} / S2 {len(tr)}; örtüşmeyen S2 işlemleri net {tr[~tr['sig_date'].isin(ov)]['net'].mean()*1e4:.1f} bp (t {sim.simple_t(tr[~tr['sig_date'].isin(ov)]['net'].values):.2f})")
    # EWY oynaklık rejimi: 2026 1g oynaklık
    r = df["c"].pct_change()
    print("EWY yıllık 1g oynaklık (bp):", (r.groupby(r.index.year).std() * 1e4).round(0).to_dict())

if __name__ == "__main__":
    main()
