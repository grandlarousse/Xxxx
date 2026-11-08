"""STRATEJİ uluslararasi_S1 — "ABD sert düşüşü, Asya ETF'i SPY'dan fazla düştü -> ertesi gün kısmi dönüş" (UL03, Levy & Lieberman 2013).
Kural (önceden sabit, hipotezler.csv UL03): t günü SPY günlük getirisi <= -%1,5 VE Asya ülke ETF'inin günlük getirisi <= SPY'ınki
  -> o ETF'i t kapanışında (C0) al; birincil çıkış t+1 kapanışı (h=1); h=2 varyant.
Sepet: EWJ, EWY, EWT, FXI, EWA, EWH (hipotez listesi). Genişletilmiş kontrol: INDA, EWS, ASHR, CQQQ, EIDO, VNM.
Maliyet: lib.cost_bp (2.500$: 12 bp komisyon + kademeli makas). Çalıştır: python3 -I kod/ajan_uluslararasi/strateji_S1_ul03_asya.py"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak, lib

SEPET = ["EWJ", "EWY", "EWT", "FXI", "EWA", "EWH"]
EK = ["INDA", "EWS", "ASHR", "CQQQ", "EIDO", "VNM"]
D = {}
def L(s):
    if s not in D: D[s] = lib.load(s)
    return D[s]
r_spy = L("SPY")["c"].pct_change()

def sinyal(s, under=None, thr=-0.015):
    u = under or s
    r = L(u)["c"].pct_change(); rs = r_spy.reindex(L(u).index)
    m = ((rs <= thr) & (r <= rs)).reindex(L(s).index).fillna(False)
    m.iloc[:200] = False
    return m

def islemler(syms, h, mode, pos=lib.POS_USD, under=None, excl_year=None):
    out = []
    for s in syms:
        df = L(s); c = ortak.cost_for(df, pos)
        sg = sinyal(s, under=(under or {}).get(s))
        if excl_year: sg &= ~pd.Series(sg.index.year == excl_year, index=sg.index)
        tr = lib.trades(df, sg, h, mode, None, c)
        if len(tr): tr["sym"] = s; out.append(tr)
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()

def satir(trs, h, ad):
    r = ortak.pooled(trs, h); r["set"] = ad; return r

def main():
    res = {}
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
    cols = ["set", "n_dates", "n_trades", "mean_gross_bp", "mean_net_bp", "per_trade_net_bp", "win_dates", "pf", "t_nw", "is_n", "is_net_bp", "is_t",
            "oos_n", "oos_net_bp", "oos_t", "years_pos_frac", "maxdd", "worst_date_bp"]
    rows = []
    for h in (1, 2):
        for mode in ("C0", "O1", "C1"):
            rows.append(satir(islemler(SEPET, h, mode), h, f"S1 sepet6 {mode} h={h}"))
    for pos in (1000, 2500, 10000):
        rows.append(satir(islemler(SEPET, 1, "C0", pos=pos), 1, f"S1 sepet6 C0 h=1 poz={pos}$"))
    rows.append(satir(islemler([s for s in SEPET if s != "EWY"], 1, "C0"), 1, "S1 EWY hariç C0 h=1"))
    rows.append(satir(islemler(SEPET, 1, "C0", excl_year=2020), 1, "S1 2020 hariç C0 h=1"))
    rows.append(satir(islemler(EK, 1, "C0"), 1, "Aynı kural, listede olmayan 6 Asya ETF'i C0 h=1"))
    rows.append(satir(islemler(EK, 2, "C0"), 2, "Aynı kural, listede olmayan 6 Asya ETF'i C0 h=2"))
    P = pd.DataFrame(rows)
    print("=== uluslararasi_S1: havuz (sinyal günü sepeti; gün-kümeli Newey-West t) ===")
    print(P[cols].round(2).to_string(index=False))
    # ETF bazında
    E = []
    for s in SEPET + EK:
        for mode in ("C0", "O1", "C1"):
            st, tr = ortak.full_stats(L(s), sinyal(s), 1, mode, label="S1", sym=s)
            E.append({k: st.get(k) for k in ["sym", "mode", "n", "mean_gross_bp", "mean_net_bp", "net_1000_bp", "net_10000_bp", "win", "pf", "t",
                                             "is_net_bp", "oos_net_bp", "years_pos_frac", "maxdd", "worst_bp", "cost_bp"]})
    E = pd.DataFrame(E)
    print("\n=== ETF bazında (h=1) ===")
    print(E.round(2).to_string(index=False))
    # Kaldıraçlı uygulama: dayanak sinyali -> kaldıraçlı ETF
    K = []
    for lev, und in (("KORU", "EWY"), ("YINN", "FXI"), ("CWEB", "KWEB"), ("EDC", "EEM")):
        for h in (1, 2):
            for mode in ("C0", "O1", "C1"):
                st, tr = ortak.full_stats(L(lev), sinyal(lev, under=und), h, mode, label="S1lev", sym=lev)
                K.append({"arac": lev, "dayanak": und, "mode": mode, "h": h, **{k: st.get(k) for k in ["n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp",
                          "oos_net_bp", "years_pos_frac", "maxdd", "worst_bp", "cost_bp"]}})
    K = pd.DataFrame(K)
    print("\n=== Kaldıraçlı uygulama (sinyal dayanaktan) ===")
    print(K.round(2).to_string(index=False))
    # yıllık
    tr = islemler(SEPET, 1, "C0")
    d = tr.groupby("sig_date")["net"].mean()
    y = d.groupby(d.index.year).agg(["count", "mean", "sum"]); y["mean"] *= 1e4; y["sum"] *= 1e4
    print("\n=== Yıllık (sepet, C0 h=1; net bp) ===")
    print(y.round(1).to_string())
    # son sinyaller
    last = tr.sort_values("sig_date").tail(12)[["sig_date", "sym", "gross", "net"]]
    last["gross"] *= 1e4; last["net"] *= 1e4
    print("\n=== Son 12 işlem ===")
    print(last.round({"gross": 1, "net": 1}).to_string(index=False))
    P.to_csv(os.path.join(ortak.OUT, "S1_havuz.csv"), index=False); E.to_csv(os.path.join(ortak.OUT, "S1_etf.csv"), index=False)
    K.to_csv(os.path.join(ortak.OUT, "S1_kaldiracli.csv"), index=False)
    return P, E, K

if __name__ == "__main__":
    main()
