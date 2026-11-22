"""ALFRED yayin tarihleri (rid=10 CPI, rid=50 Istihdam Raporu) -> makro_tarihleri.csv (2005-2026).
Kullanim: python3 -I makro_kur.py <dizin>  (dizinde r10.txt, r50.txt: https://alfred.stlouisfed.org/release/downloaddates?rid=<id>&ff=txt)"""
import sys, os, re
import pandas as pd
D = sys.argv[1]
KOD = os.path.dirname(os.path.abspath(__file__)); VERI = os.path.join(os.path.dirname(KOD), "veri")
rows = []
for rid, ad in [(10, "CPI"), (50, "ISTIHDAM")]:
    metin = open(os.path.join(D, f"r{rid}.txt")).read()
    bolum = metin.split("Release Dates")[-1] if "Release Dates" in metin else metin
    for t in re.findall(r"^\s*(\d{4}-\d{2}-\d{2})\s*$", bolum, flags=re.M):
        rows.append(dict(tarih=pd.Timestamp(t), yayin=ad, saat_et="08:30",
                         kaynak=f"https://alfred.stlouisfed.org/release/downloaddates?rid={rid}"))
M = pd.DataFrame(rows).drop_duplicates(["tarih", "yayin"]).sort_values(["tarih", "yayin"])
M = M[(M.tarih >= "2005-01-01") & (M.tarih <= "2026-12-31")]
gun = pd.read_pickle(os.environ.get("PANEL_DIZIN", "/tmp/claude-0/-home-user-Xxxx/b23916bf-451a-5d36-8905-d1866417ce1f/scratchpad/panel") + "/close.pkl").index
M["islem_gunu"] = M.tarih.isin(gun)
# ALFRED bazen ayni ay icinde ikinci yayin tarihi listeler (yillik revizyon/benchmark ya da gecikmeli yayin); isaretle
# Ikisi de isaretlenir: hangisinin ana yayin oldugu dogrulanmadi (Subat CPI'da genelde erken tarih mevsimsel faktor revizyonu)
M["ayda_birden_fazla"] = M.groupby(["yayin", M.tarih.dt.to_period("M")]).tarih.transform("size") > 1
M.to_csv(os.path.join(VERI, "makro_tarihleri.csv"), index=False, date_format="%Y-%m-%d")
print(M.groupby([M.tarih.dt.year, "yayin"]).size().unstack().T.to_string())
print("ayni ayda 2.:", M[M.ayda_birden_fazla][["tarih", "yayin"]].to_string(index=False))
print("islem gunu olmayan:", M[~M.islem_gunu][["tarih", "yayin"]].to_string(index=False))
