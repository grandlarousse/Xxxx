"""Denetim D5: kaçırılan fırsat/risk testleri.
(1) S1'in göreli kenarı (ETF<=SPY olanlar, SPY'a göre) açığa satış olmadan ters ETF (SH) ile korunarak yakalanabilir mi?
    Sinyal günü: seçilen Asya ETF'leri (her biri 2.500$) + tek SH emri (toplam long tutarı kadar). t kapanışı -> t+1 kapanışı.
(2) S1 h=2 varyantının sağlamlığı (yoğunlaşma; en iyi 5 gün; 2020+2026 hariç).
(3) Sinyal gününden sonraki günlerde ardışık tetiklenme (kriz kümelenmesi) ve aynı anda açık pozisyon/sermaye ihtiyacı.
Çalıştır: python3 -I kod/denetim_uluslararasi/d5_kacirilan.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import sim
from sim import L
from d1_s1_yeniden import SEPET, s1, r_spy

def main():
    pd.set_option("display.width", 250)
    tr = sim.basket(SEPET, s1(), 1, "C0")
    sh = L("SH")["c"]; sh1 = (sh.shift(-1) / sh - 1)
    spy1 = (L("SPY")["c"].shift(-1) / L("SPY")["c"] - 1)
    g = tr.groupby("sig_date").agg(gross=("gross", "mean"), net=("net", "mean"), k=("sym", "count"))
    g["sh"] = sh1.reindex(g.index); g["spy1"] = spy1.reindex(g.index)
    for pos in (2500, 10000):
        cl = {s: sim.cost(s, pos) for s in SEPET}
        net_long = tr.assign(n2=tr["gross"] - tr["sym"].map(cl) / 1e4).groupby("sig_date")["n2"].mean()
        sh_cost = (2 * 1.5 / (g["k"] * pos) * 1e4 + sim.spread("SH")) / 1e4
        hedged = (net_long + g["sh"] - sh_cost) / 2       # sermaye: long + SH (2x); getiri toplam sermayeye göre
        hedged_on_long = net_long + g["sh"] - sh_cost      # long tutarına göre (SH için ayrı nakit)
        x = hedged_on_long.dropna()
        print(f"(1) SH korumalı S1, poz {pos}$: n={len(x)} brüt göreli {(g['gross']+g['sh']).mean()*1e4:.1f} bp, net (long tutarına göre) {x.mean()*1e4:.1f} bp, "
              f"t {sim.simple_t(x.values):.2f}, IS {x[x.index<=sim.IS_END].mean()*1e4:.1f} / OOS {x[x.index>sim.IS_END].mean()*1e4:.1f}, "
              f"yıl+ {(x.groupby(x.index.year).sum()>0).mean():.2f}, en kötü gün {x.min()*1e4:.0f} bp (korumasız {g['net'].min()*1e4:.0f}); 2020+2026 hariç {x[~x.index.year.isin([2020,2026])].mean()*1e4:.1f} (t {sim.simple_t(x[~x.index.year.isin([2020,2026])].values):.2f})")
    print(f"    SPY ertesi gün (sinyal günlerinde) ort {g['spy1'].mean()*1e4:.1f} bp; korumasız sepet brüt {g['gross'].mean()*1e4:.1f} bp; std korumasız {g['net'].std()*1e4:.0f} / korumalı {(g['gross']+g['sh']).std()*1e4:.0f} bp")

    # (2) h=2 sağlamlık
    t2 = sim.basket(SEPET, s1(), 2, "C0")
    d2 = t2.groupby("sig_date")["net"].mean()
    def rep(nm, t):
        r = sim.summarize(t, 2)
        print(f"(2) h=2 {nm}: n_g={r['n_dates']} net {r['net_bp']:.1f} t_basit {r['t_simple']:.2f} t_nw {r['t_nw']:.2f} IS {r['is_net_bp']:.1f} OOS {r['oos_net_bp']:.1f} yıl+ {r['years_pos']:.2f}")
    rep("tam", t2)
    rep("en iyi 5 gün hariç", t2[~t2["sig_date"].isin(d2.nlargest(5).index)])
    rep("2020+2026 hariç", t2[~t2["sig_date"].dt.year.isin([2020, 2026])])
    t2o = sim.basket(SEPET, s1(), 2, "O1"); rep("O1", t2o)
    t2o = sim.basket(SEPET, s1(), 2, "C0", pos=1000); rep("C0 1.000$", t2o)

    # (3) kümelenme ve sermaye
    days = g.index
    cal = L("SPY").index
    pos_i = np.searchsorted(cal, days)
    consec = np.sum(np.diff(pos_i) == 1)
    print(f"(3) {len(days)} sinyal gününün {consec}'i bir önceki sinyal gününün hemen ertesi (ardışık tetik). k (aynı gün ETF sayısı) dağılımı: {g['k'].value_counts().sort_index().to_dict()}")
    print(f"    Mart 2020 sinyal günleri: {[str(d.date()) for d in days if d.year==2020 and d.month==3]}")
    mx = g["k"].max()
    print(f"    Aynı anda en fazla {mx} ETF -> 2.500$ başına {mx*2500:,.0f} $; 1.000$ başına {mx*1000:,.0f} $")
    # (4) en son sinyaller (izleme için)
    print("Son 6 sinyal günü:", [(str(d.date()), int(k), round(v * 1e4, 0)) for d, k, v in zip(g.index[-6:], g["k"][-6:], g["net"][-6:])])

if __name__ == "__main__":
    main()
