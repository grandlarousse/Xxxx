"""evren.csv kapanis_sinifi'ni kapanis_saatleri.csv'ye gore gunceller ve kapanis_et sutunu ekler.
Kural: ET 15:45 sonrasi kapanan -> SONRA. VIX ailesi (Cboe 16:15 ET) -> SONRA. ^TNX/^FVX/^TYX/^IRX (Cboe 15:00 ET) -> ONCE.
^BVSP: B3 kapanisi ET'ye gore mevsimle 15:00-16:10 arasi gezer -> temkinli SONRA. ^MOVE: ICE gun sonu degeri -> SONRA."""
import os, pandas as pd
KOD = os.path.dirname(os.path.abspath(__file__)); VERI = os.path.join(os.path.dirname(KOD), "veri")
ev = pd.read_csv(os.path.join(VERI, "evren.csv"), dtype={"kod": str})
T = pd.read_csv(os.path.join(VERI, "kapanis_saatleri.csv"), dtype={"kod": str}).set_index("kod")
eski = ev.kapanis_sinifi.copy()
ev["kapanis_et"] = ev.kod.map(T.et_kapanis)
vix = ev.kapanis_sinifi.eq("VIX1615")
ev.loc[vix, "kapanis_et"] = "16:15"          # Cboe VIX ailesi 16:15 ET'de kapanir (Yahoo meta 16:00 gosterse de)
ev.loc[vix, "kapanis_sinifi"] = "SONRA"
ev.loc[vix, "not"] = ev.loc[vix, "not"].fillna("").str.cat(["eski_sinif=VIX1615"] * vix.sum(), sep=";").str.strip(";")
faiz = ev.kod.isin(["^TNX", "^FVX", "^TYX", "^IRX"])
ev.loc[faiz, "kapanis_sinifi"] = "ONCE"       # 14:00 CT = 15:00 ET
ev.loc[ev.kod.eq("^BVSP"), "not"] = "B3 kapanisi 15:00 ET (kis) - 16:00+ ET (ABD yaz saati); temkinli SONRA"
ev.loc[ev.kod.eq("^MOVE"), "not"] = "ICE gun sonu degeri; temkinli SONRA"
ev.to_csv(os.path.join(VERI, "evren.csv"), index=False)
d = ev[eski != ev.kapanis_sinifi]
print("degisen:", d[["kod"]].assign(eski=eski[d.index], yeni=d.kapanis_sinifi).to_string(index=False))
print(ev.kapanis_sinifi.value_counts())
