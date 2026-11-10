"""Ana ajan keşif hesabı (doğrulanmadı): 'altın–TRALT bağı açıkken işlem yap' süzgeci geriye dönük ne yapardı?
Girdi: K1 günlük paneli (r_TRALT, r_XAU) ve K2 işlem listesi. Önceden sabit: pencere 120 gün, eşik 0,20; diğerleri yalnız duyarlılık.
Kullanım: python3 rejim_kesif.py <S>"""
import sys, numpy as np, pandas as pd
S = sys.argv[1]
P = pd.read_pickle(S + "/k1_panel.pkl")
t = pd.read_csv("hesap/K2/islemler_k2_tralt.csv", parse_dates=["date", "exit"])
def tt(x):
    x = np.asarray(x, float)
    return (x.mean(), x.mean() / (x.std(ddof=1) / np.sqrt(len(x))), len(x)) if len(x) > 2 else (np.nan, np.nan, len(x))
rows = []
for w in (60, 120, 250):
    c = P["r_TRALT"].rolling(w, min_periods=int(w * 0.6)).corr(P["r_XAU"]).shift(1)   # girişten önceki güne kadar
    for th in (0.10, 0.20, 0.30):
        for rule in ("R1", "A2"):
            d = t[t.rule == rule].copy(); d["c"] = c.reindex(d["date"]).values
            d = d.dropna(subset=["c"])
            on, off = d[d.c >= th], d[d.c < th]
            for nm, g in (("acik", on), ("kapali", off)):
                m, s, n = tt(g["gross"])
                mb, sb, _ = tt(g["gross"] - g["c_bireysel"])
                yrs = g.groupby(g["date"].dt.year)["gross"].sum()
                rows.append(dict(pencere=w, esik=th, kural=rule, durum=nm, n=n, brut=round(m, 1), t_brut=round(s, 2),
                                 net_bireysel=round(mb, 1), t_bireysel=round(sb, 2),
                                 ex2=round(np.sort(g["gross"].values)[:max(1, int(len(g) * 0.98))].mean(), 1) if n > 20 else np.nan,
                                 net21_23=round((g[(g.date.dt.year >= 2021) & (g.date.dt.year <= 2023)]["gross"] - g[(g.date.dt.year >= 2021) & (g.date.dt.year <= 2023)]["c_bireysel"]).mean(), 1),
                                 n21_23=int(((g.date.dt.year >= 2021) & (g.date.dt.year <= 2023)).sum())))
R = pd.DataFrame(rows); R.to_csv("hesap/ana/rejim_kesif.csv", index=False)
pd.set_option("display.width", 220)
print(R[(R.pencere == 120) & (R.esik == 0.20)].to_string(index=False))
print("\nDuyarlılık (R1, 'acik'):"); print(R[(R.kural == "R1") & (R.durum == "acik")].to_string(index=False))
print("\nDuyarlılık (A2, 'acik'):"); print(R[(R.kural == "A2") & (R.durum == "acik")][["pencere", "esik", "n", "brut", "t_brut", "net_bireysel", "t_bireysel", "ex2", "net21_23", "n21_23"]].to_string(index=False))
# 120 günlük korelasyonun yıllara göre ortalaması ve 'açık' gün payı
c = P["r_TRALT"].rolling(120, min_periods=72).corr(P["r_XAU"]).shift(1)
print("\n120g korelasyon yıllık ort / açık gün payı (eşik 0,20):"); print(pd.DataFrame({"ort": c.groupby(c.index.year).mean().round(2), "acik_pay": (c >= 0.2).groupby(c.index.year).mean().round(2)}).T.to_string())
print("son değer:", round(c.iloc[-1], 2))
# öz sermaye eğrisi süzgeci: son 20 işlemin brüt toplamı > 0 ise işlem
for rule in ("R1", "A2"):
    d = t[t.rule == rule].sort_values("date").copy(); d["eqc"] = d["gross"].rolling(20).sum().shift(1)
    for nm, g in (("son20>0", d[d["eqc"] > 0]), ("son20<=0", d[d["eqc"] <= 0])):
        print(rule, nm, "n %d brüt %.1f (t %.2f) | bireysel net %.1f (t %.2f)" % (len(g), *tt(g["gross"])[:2], *tt(g["gross"] - g["c_bireysel"])[:2]))
