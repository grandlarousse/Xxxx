"""Denetim D1: uluslararasi_S1 (UL03) bağımsız yeniden üretim + zamanlama kontrolleri + en büyük işlemler.
Çalıştır: python3 -I kod/denetim_uluslararasi/d1_s1_yeniden.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import sim
from sim import L

SEPET = ["EWJ", "EWY", "EWT", "FXI", "EWA", "EWH"]
EK = ["INDA", "EWS", "ASHR", "CQQQ", "EIDO", "VNM"]
spy = L("SPY")["c"]; r_spy = spy / spy.shift(1) - 1

def s1(thr=-0.015, rel="le", k=1.0, warm=200, under=None):
    def f(s):
        u = under.get(s, s) if under else s
        c = L(u)["c"]; r = c / c.shift(1) - 1
        rs = r_spy.reindex(c.index)
        m = rs <= thr
        if rel == "le": m &= r <= k * rs
        elif rel == "gt": m &= r > k * rs
        m = m.reindex(L(s).index).fillna(False)
        m.iloc[:warm] = False
        return m
    return f

def main():
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300); pd.set_option("display.max_columns", 40)
    rows = []
    for h in (1, 2, 3):
        for mode in ("C0", "O1", "C1"):
            tr = sim.basket(SEPET, s1(), h, mode)
            r = sim.summarize(tr, h); r.update(set="sepet6", h=h, mode=mode); rows.append(r)
    for pos in (1000, 2500, 10000):
        tr = sim.basket(SEPET, s1(), 1, "C0", pos=pos)
        r = sim.summarize(tr, 1); r.update(set=f"sepet6 poz={pos}", h=1, mode="C0"); rows.append(r)
    # tutuşu koru varyantı (kural metni: 'çıkış günü yeniden sinyal varsa pozisyon korunur')
    tr = sim.basket(SEPET, s1(), 1, "C0", hold=True)
    r = sim.summarize(tr, 1); r.update(set="sepet6 hold=True", h=1, mode="C0"); rows.append(r)
    # stres makası: tetik günlerinde makas 2x/ +10 bp
    for ex in (10, 20):
        tr = sim.basket(SEPET, s1(), 1, "C0", extra_bp=ex)
        r = sim.summarize(tr, 1); r.update(set=f"sepet6 +{ex}bp stres makas", h=1, mode="C0"); rows.append(r)
    # işlem bazlı (kümelemesiz) t
    tr = sim.basket(SEPET, s1(), 1, "C0")
    r = sim.summarize(tr, 1, by_date=False); r.update(set="sepet6 islem-bazli (kumelemesiz)", h=1, mode="C0"); rows.append(r)
    P = pd.DataFrame(rows)
    cols = ["set", "mode", "h", "n_dates", "n_trades", "gross_bp", "net_bp", "t_simple", "t_nw", "win", "pf", "maxdd", "worst_bp",
            "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp", "oos_t", "years_pos"]
    print("=== D1: S1 bağımsız yeniden üretim (gün-kümeli) ===")
    print(P[cols].round(2).to_string(index=False))
    P.to_csv(os.path.join(sim.OUT, "d1_s1_yeniden.csv"), index=False)

    # ETF bazında
    E = []
    for s in SEPET + EK + ["EEM"]:
        for mode in ("C0", "O1", "C1"):
            tr = sim.sim(s, s1()(s), 1, mode)
            r = sim.summarize(tr, 1, by_date=False); r.update(sym=s, mode=mode); E.append(r)
    E = pd.DataFrame(E)
    print("\n=== ETF bazında h=1 ===")
    print(E[["sym", "mode", "n_trades", "gross_bp", "net_bp", "t_simple", "is_net_bp", "oos_net_bp", "years_pos", "worst_bp"]].round(2).to_string(index=False))
    E.to_csv(os.path.join(sim.OUT, "d1_s1_etf.csv"), index=False)

    # Ayrıştırma: gece boşluğu (c_t -> o_t+1) ve gün içi (o_t+1 -> c_t+1)
    tr = sim.basket(SEPET, s1(), 1, "C0")
    gap, intr = [], []
    for _, x in tr.iterrows():
        df = L(x["sym"]); i = df.index.get_loc(x["sig_date"])
        gap.append(df["o"].iloc[i + 1] / df["c"].iloc[i] - 1); intr.append(df["c"].iloc[i + 1] / df["o"].iloc[i + 1] - 1)
    tr["gap"] = gap; tr["intra"] = intr
    print("\nAyrıştırma (işlem ort., bp): gece boşluğu %.1f, ertesi gün içi %.1f, toplam brüt %.1f" % (
        tr["gap"].mean() * 1e4, tr["intra"].mean() * 1e4, tr["gross"].mean() * 1e4))

    # Zamanlama kontrolleri: giriş tarihi = sinyal tarihi (C0), çıkış = sonraki işlem günü
    bad = 0
    for _, x in tr.iterrows():
        df = L(x["sym"]); i = df.index.get_loc(x["sig_date"])
        if x["entry"] != x["sig_date"] or x["exit"] != df.index[i + 1]: bad += 1
    print("Zamanlama hatası olan işlem sayısı:", bad)
    # SPY ve ETF takvim uyumu: ETF'te olup SPY'da olmayan gün?
    for s in SEPET:
        miss = L(s).index.difference(spy.index)
        if len(miss): print("  takvim farkı", s, len(miss), list(miss[:5]))
    # Ham kapanış (düzeltilmemiş) ile sinyal: temettü ex-günü artefaktı var mı?
    nd = 0; diff_days = []
    for s in SEPET:
        df = L(s); rr = df["raw_c"] / df["raw_c"].shift(1) - 1; ra = df["c"] / df["c"].shift(1) - 1
        rs = r_spy.reindex(df.index); rsr = (L("SPY")["raw_c"] / L("SPY")["raw_c"].shift(1) - 1).reindex(df.index)
        a = (rs <= -0.015) & (ra <= rs); b = (rsr <= -0.015) & (rr <= rsr)
        a.iloc[:200] = False; b.iloc[:200] = False
        dd = df.index[(a != b)]
        nd += len(dd); diff_days += [(s, str(d.date()), bool(a[d]), bool(b[d])) for d in dd]
    print("Düzeltilmiş vs ham fiyatla sinyal farkı (gün):", nd, diff_days[:12])

    # En büyük 5 kazanç ve en kötü 5 işlem, veri kalitesi dosyalarıyla
    vk = pd.read_csv(os.path.join(sim.ROOT, "sonuclar", "veri_kalitesi.csv"), parse_dates=["date"])
    vd = pd.read_csv(os.path.join(sim.ROOT, "sonuclar", "veri_duzeltmeleri.csv"))
    print("\nveri_duzeltmeleri.csv sütunları:", vd.columns.tolist())
    fixed = vd[vd.iloc[:, 0].isin(SEPET + ["SPY"])]
    print("Sepet/SPY için veri düzeltmesi:", fixed.to_string(index=False) if len(fixed) else "yok")
    top = tr.sort_values("net", ascending=False).head(8).copy(); worst = tr.sort_values("net").head(5).copy()
    for nm, T in (("EN BÜYÜK KAZANÇLAR", top), ("EN KÖTÜ İŞLEMLER", worst)):
        T = T.copy()
        T["spy_t"] = [r_spy.get(d) * 1e4 for d in T["sig_date"]]
        T["etf_t"] = [(L(s)["c"].loc[d] / L(s)["c"].shift(1).loc[d] - 1) * 1e4 for s, d in zip(T["sym"], T["sig_date"])]
        T["vk_flag"] = [bool(((vk["sym"] == s) & ((vk["date"] == d) | (vk["date"] == e))).any()) for s, d, e in zip(T["sym"], T["sig_date"], T["exit"])]
        for c in ("gross", "net", "gap", "intra"): T[c] = T[c] * 1e4
        print(f"\n{nm}:"); print(T[["sig_date", "exit", "sym", "spy_t", "etf_t", "gross", "net", "gap", "intra", "vk_flag"]].round(1).to_string(index=False))
    # gün bazında en iyi 5 sinyal günü
    d = tr.groupby("sig_date").agg(net=("net", "mean"), k=("sym", "count")).sort_values("net", ascending=False)
    print("\nEn iyi 5 sinyal günü (sepet ort. net bp):"); print((d.head(5).assign(net=lambda x: x.net * 1e4)).round(1).to_string())
    tr.to_csv(os.path.join(sim.OUT, "d1_s1_islemler.csv"), index=False)

if __name__ == "__main__":
    main()
