"""Denetim D7: S1 kural metni ('çıkış günü yeniden sinyal varsa pozisyon korunur') ile backtest (yeniden giriş, ek maliyet) farkı.
hold=True sürümünün sağlamlığı. Çalıştır: python3 -I kod/denetim_uluslararasi/d7_hold.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import sim
from d1_s1_yeniden import SEPET, s1

def rep(nm, t, h=1):
    r = sim.summarize(t, h)
    print(f"{nm}: gün {r['n_dates']} işlem {r['n_trades']} brüt {r['gross_bp']:.1f} net {r['net_bp']:.1f} t_basit {r['t_simple']:.2f} t_nw {r['t_nw']:.2f} IS {r['is_net_bp']:.1f} OOS {r['oos_net_bp']:.1f} (t {r['oos_t']:.2f}) yıl+ {r['years_pos']:.2f} en kötü {r['worst_bp']:.0f}")
    return r

for hold in (False, True):
    t = sim.basket(SEPET, s1(), 1, "C0", hold=hold)
    d = t.groupby("sig_date")["net"].mean()
    rep(f"hold={hold} tam", t)
    rep(f"hold={hold} en iyi 5 gün hariç", t[~t["sig_date"].isin(d.nlargest(5).index)])
    rep(f"hold={hold} 2020+2026 hariç", t[~t["sig_date"].dt.year.isin([2020, 2026])])
    rep(f"hold={hold} Mart 2020 hariç", t[~((t["sig_date"].dt.year == 2020) & (t["sig_date"].dt.month == 3))])
    rep(f"hold={hold} 1.000$", sim.basket(SEPET, s1(), 1, "C0", pos=1000, hold=hold))
    ext = t[(t["exit"] - t["entry"]).dt.days > 4]
    print(f"   uzatılan işlem sayısı (takvim >4 gün): {len(ext)}")
