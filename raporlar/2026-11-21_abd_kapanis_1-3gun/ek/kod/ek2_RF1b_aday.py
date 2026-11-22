# -*- coding: utf-8 -*-
"""ek2_RF1b_aday.py - Ek 2 (gorev RF1b): IS tarama ciktilarindan (K4a, K4b, K5, K6, K9) muzayede adaylarini
OOS'a bakmadan once aday_ek2_RF1b.csv'ye yazar. Birincil (hisse) aday bayragi ayni varyant icin yanina."""
import glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import ek2_ortak_RF1b as E

D = pd.concat([pd.read_pickle(f) for f in sorted(glob.glob(os.path.join(E.SCR, "is_*.pkl")))], ignore_index=True)
D.to_pickle(os.path.join(E.SCR, "is_hepsi.pkl"))
anah = ["aile_g", "anahtar", "h", "giris", "cikis", "korunma"]
H = D[D.komisyon == "hisse"][anah + ["aday", "net_bps", "t_karar"]].rename(
    columns={"aday": "birincil_aday", "net_bps": "birincil_net_bps", "t_karar": "birincil_t_karar"})
Mz = D[D.komisyon == "muzayede"].merge(H, on=anah, how="left")
oz = Mz.groupby("aile_g").agg(varyant=("aday", "size"), aday_muzayede=("aday", "sum"),
                              aday_birincil=("birincil_aday", "sum"))
print(oz)
A = Mz[Mz.aday].copy()
A["birincil_aday_sayisi_aile"] = A.aile_g.map(oz.aday_birincil)
A["muzayede_aday_sayisi_aile"] = A.aile_g.map(oz.aday_muzayede)
A["sinanan_varyant_aile"] = A.aile_g.map(oz.varyant)
sut = ["aile_g", "anahtar", "ki", "kural_id", "ad", "hedef", "yon", "h", "giris", "cikis", "korunma", "komisyon",
       "donem", "oos_donem", "n_islem", "brut_bps", "net_bps", "anormal_bps", "t_olcekli", "t_kume", "t_anormal",
       "t_karar", "cok", "tek_yon", "birincil_aday", "birincil_net_bps", "birincil_t_karar",
       "sinanan_varyant_aile", "birincil_aday_sayisi_aile", "muzayede_aday_sayisi_aile"]
A[sut].to_csv(E.F_ADAY, index=False)
oz.to_csv(os.path.join(E.SCR, "aile_ozet_is.csv"))
pd.set_option("display.width", 250)
print(A[["aile_g", "anahtar", "hedef", "yon", "h", "cikis", "korunma", "n_islem", "net_bps", "t_karar", "t_anormal",
         "birincil_aday", "birincil_net_bps"]].round(2).to_string(index=False))
print(f"-> {E.F_ADAY} ({len(A)})")
