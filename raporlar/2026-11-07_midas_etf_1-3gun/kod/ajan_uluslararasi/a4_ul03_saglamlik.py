"""UL03 (ABD'de sert düşüş günü, Asya ülke ETF'i SPY'dan daha çok düşmüş -> ertesi gün(ler) kısmi dönüş) sağlamlık analizi.
Kural önceden sabit (hipotezler.csv UL03): r_SPY,t <= -1.5% ve r_ETF,t <= r_SPY,t -> ETF long.
Burada: ETF bazında sonuçlar, plasebo (eşzamanlı Amerika ETF'leri, Avrupa, SPY'ın kendisi), ayrıştırma (ETF > SPY tümleyeni),
komşu eşikler (-1.0/-2.0; seçim için DEĞİL, yalnız rapor), 2020 hariç, genişletilmiş Asya evreni, kaldıraçlı uygulama.
Çalıştır: python3 -I kod/ajan_uluslararasi/a4_ul03_saglamlik.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak, lib

D = {}
def L(s):
    if s not in D: D[s] = lib.load(s)
    return D[s]
spy = L("SPY"); r_spy = spy["c"].pct_change()

def sig_ul03(s, thr=-0.015, rel="le", under=None):
    u = under or s
    r = L(u)["c"].pct_change()
    rs = r_spy.reindex(L(u).index)
    m = (rs <= thr)
    if rel == "le": m &= (r <= rs)
    elif rel == "gt": m &= (r > rs)
    m = m.reindex(L(s).index).fillna(False)
    m.iloc[:200] = False
    return m

ASYA6 = ["EWJ", "EWY", "EWT", "FXI", "EWA", "EWH"]
ASYA_GENIS = ["EWJ", "EWY", "EWT", "FXI", "EWA", "EWH", "INDA", "EWS", "ASHR", "CQQQ", "EIDO", "VNM"]
AMERIKA = ["EWZ", "EWW", "EWC", "ILF", "ECH", "ARGT"]
AVRUPA = ["VGK", "EWG", "EWU", "EWQ", "EWI", "EWP", "EWL", "EPOL", "EZA", "KSA"]

def pool(name, targets, fn, modes=("C0", "O1", "C1"), hs=(1, 2, 3), excl=None):
    rows = []
    for mode in modes:
        for h in hs:
            trs = []
            for s in targets:
                sg = fn(s)
                if excl is not None: sg = sg & ~pd.Series(sg.index.year == excl, index=sg.index)
                tr = lib.trades(L(s), sg, h, mode, None, lib.cost_bp(L(s)))
                if len(tr): tr["sym"] = s; trs.append(tr)
            trs = pd.concat(trs, ignore_index=True) if trs else pd.DataFrame()
            r = ortak.pooled(trs, h); r.update({"set": name, "mode": mode, "h": h})
            rows.append(r)
    return rows

def main():
    out = []
    out += pool("UL03_Asya6", ASYA6, sig_ul03)
    out += pool("UL03_Asya6_2020haric", ASYA6, sig_ul03, excl=2020)
    out += pool("tumleyen_ETF>SPY_Asya6", ASYA6, lambda s: sig_ul03(s, rel="gt"))
    out += pool("yalniz_SPY<=-1.5_Asya6", ASYA6, lambda s: sig_ul03(s, rel=None))
    out += pool("komsu_esik_-1.0_Asya6", ASYA6, lambda s: sig_ul03(s, thr=-0.010))
    out += pool("komsu_esik_-2.0_Asya6", ASYA6, lambda s: sig_ul03(s, thr=-0.020))
    out += pool("UL03_Asya_genis12", ASYA_GENIS, sig_ul03)
    out += pool("UL03_Asya_genis_disi6", [s for s in ASYA_GENIS if s not in ASYA6], sig_ul03)
    out += pool("plasebo_Amerika", AMERIKA, sig_ul03)
    out += pool("plasebo_Avrupa", AVRUPA, sig_ul03)
    out += pool("plasebo_SPY_kendisi(SPY<=-1.5)", ["SPY"], lambda s: sig_ul03(s, rel=None))
    out += pool("EEM", ["EEM"], sig_ul03)
    P = pd.DataFrame(out)
    P.to_csv(os.path.join(ortak.OUT, "ul03_saglamlik_havuz.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
    cols = ["set", "mode", "h", "k_etf", "n_dates", "n_trades", "mean_gross_bp", "mean_net_bp", "t_nw", "is_net_bp", "is_t", "oos_net_bp", "oos_t",
            "years_pos_frac", "pf", "maxdd", "worst_date_bp"]
    print(P[cols].round(2).to_string(index=False))
    # ETF bazında (kaldıraçlılar dayanak sinyaliyle)
    E = []
    for s in ASYA_GENIS + AMERIKA + ["KORU", "YINN", "CWEB", "EDC"]:
        under = ortak.UNDERLYING.get(s, s)
        if s == "CWEB": under = "KWEB"
        for mode in ("C0", "O1", "C1"):
            for h in (1, 2, 3):
                sg = sig_ul03(s, under=under)
                st, tr = ortak.full_stats(L(s), sg, h, mode, label="UL03", sym=s)
                st["dayanak"] = under; E.append(st)
    E = pd.DataFrame(E)
    E.to_csv(os.path.join(ortak.OUT, "ul03_etf.csv"), index=False)
    c2 = ["sym", "dayanak", "mode", "h", "n", "mean_gross_bp", "mean_net_bp", "net_1000_bp", "net_10000_bp", "win", "pf", "t", "is_net_bp", "is_t",
          "oos_net_bp", "oos_t", "years_pos_frac", "maxdd", "worst_bp", "cost_bp", "edge_bp"]
    print(E[(E["h"].isin([1, 2]))][c2].round(2).to_string(index=False))

if __name__ == "__main__":
    main()
