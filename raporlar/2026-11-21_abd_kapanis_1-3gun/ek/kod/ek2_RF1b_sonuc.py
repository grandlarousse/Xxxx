# -*- coding: utf-8 -*-
"""ek2_RF1b_sonuc.py - Ek 2 (gorev RF1b): IS + aday OOS satirlarini standart semayla sonuc_ek2_RF1b.csv'ye,
aday basina OOS ayrintisini ek2_RF1b_oos_ayrinti.csv'ye yazar."""
import glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import motor as M
import ek2_ortak_RF1b as E

IS = pd.read_pickle(os.path.join(E.SCR, "is_hepsi.pkl"))
OS = pd.concat([pd.read_pickle(f) for f in sorted(glob.glob(os.path.join(E.SCR, "oossema_K*.pkl")))], ignore_index=True)
R = pd.concat([IS, OS], ignore_index=True)
R["notlar"] = R["notlar"].fillna("").astype(str) + "; ek2_RF1b aile=" + R["aile_g"].astype(str) + \
    " anahtar=" + R["anahtar"].astype(str)
M.yaz_sonuc(R, E.F_SONUC)
print("sonuc:", len(R), E.F_SONUC)

AD = pd.read_csv(E.F_ADAY)
O = pd.concat([pd.read_pickle(f) for f in sorted(glob.glob(os.path.join(E.SCR, "oos_K*.pkl")))], ignore_index=True)
O = O.drop(columns=["ki"]).merge(AD, on=["aile_g", "anahtar", "h", "cikis"], how="left", suffixes=("", "_is"))
rows = []
for _, r in O.iterrows():
    od = r["oos_donem"]
    sd = "OOS2" if od == "OOS2" else "SON"
    g = r["giris"]
    G = lambda c: r.get(c, np.nan)
    p = G(f"{g}_{od}_muzayede_p")
    t = G(f"{g}_{od}_muzayede_t")
    net = G(f"{g}_{od}_muzayede_net")
    rows.append(dict(aile=r.aile_g, kural_id=r.kural_id, anahtar=r.anahtar, ad=r.ad, hedef=r.hedef, yon=r.yon,
                     h=r.h, giris=g, cikis=r.cikis,
                     korunma=r.korunma if isinstance(r.korunma, str) else r.get("korunma_is"), is_donem=r.donem, oos_donem=od,
                     is_n=r.n_islem, is_net_bps=r.net_bps, is_t=r.t_karar, is_t_anormal=r.t_anormal,
                     birincil_is_aday=r.birincil_aday,
                     oos_n=G(f"{g}_{od}_muzayede_n"), oos_net_bps=net, oos_t=t, oos_t_anormal=G(f"{g}_{od}_muzayede_tan"),
                     oos_p=p if np.isfinite(p) else 1.0, oos_net_sigma=G(f"{g}_{od}_muzayede_ns"),
                     oos_gecer_t2=bool(G(f"{g}_{od}_muzayede_gecer")),
                     birincil_oos_net_bps=G(f"{g}_{od}_hisse_net"), birincil_oos_t=G(f"{g}_{od}_hisse_t"),
                     son_n=G(f"{g}_{sd}_muzayede_n") if sd != od else np.nan,
                     son_net_bps=G(f"{g}_{sd}_muzayede_net") if sd != od else np.nan,
                     son_t=G(f"{g}_{sd}_muzayede_t") if sd != od else np.nan,
                     girisA_oos_net_bps=G(f"A_{od}_muzayede_net"), girisA_oos_t=G(f"A_{od}_muzayede_t"),
                     en_iyi5suz_bps=G(f"{od}_en_iyi5suz_bps"), uzun_net=G(f"{od}_uzun_net_bps"),
                     kisa_net=G(f"{od}_kisa_net_bps"), v30_n=G(f"{od}_v30_n"), v30_net=G(f"{od}_v30_net_bps"),
                     yillar=G(f"{od}_yillar")))
T = pd.DataFrame(rows)
T["oos_bh_q_bu5aile"] = M.bh(T.oos_p.to_numpy(), 0.10)[1]
T = T.sort_values(["oos_gecer_t2", "oos_t"], ascending=[False, False])
f = os.path.join(E.VERI, "ek2_RF1b_oos_ayrinti.csv")
T.to_csv(f, index=False)
pd.set_option("display.width", 300)
print(T.drop(columns=["ad", "yillar", "anahtar"]).round(2).to_string(index=False))
print(T[["anahtar", "h", "yillar"]].to_string(index=False))
print("->", f)
B = pd.read_csv(os.path.join(E.SCR, "betim_K9_gece.csv"))
B.to_csv(os.path.join(E.VERI, "ek2_RF1b_K9_gece_betim.csv"), index=False)
