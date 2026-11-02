"""02: TKC (NYSE ADR, 1 ADS = 2,5 TCELL hissesi) -> TCELL / TTKOM.
A) Günlük parite primi P_t = ln(TKC_t * USDTRY_t / (2.5 * TCELL_t)); USDTRY = hizalı (≈00:00 UTC t+1, ABD kapanışına yakın).
   Sapma D_t = P_t - ortalama(P_{t-20..t-1}) (adj fiyatlarla; temettü tarihi farkını temizler). D_t ≈ BIST kapanışından sonra ADR'nin TL karşılığındaki hareket.
   Test: TCELL gap_{t+1}, intra_{t+1}  ~ D_t ; P'nin kapanma (mean reversion) hızı ve hangi bacağın kapattığı.
B) Saatlik (2023-12+): TKC post-close getirisi = ln(TKC_kapanış / TKC_15:30 UTC) (+ kur post-close) -> TCELL gap/intra/ilk saat.
"""
from sv import *
pd.set_option("display.width", 220)
out = {}

def lvl(sym, field):
    d = ll.raw(sym); s = pd.Series(d[field].values, index=pd.DatetimeIndex(d["ldate"].values)).astype(float)
    return s[~s.index.duplicated(keep="last")]

cal = ll.bist_cal(); cal = cal[cal >= "2008-01-01"]
# FX seviye (hizalı): bar D -> önceki iş günü
fxr = ll.raw("TRY=X"); fx = pd.Series(fxr["c"].values, index=pd.DatetimeIndex(fxr["ldate"].values)).astype(float)
fx = fx[~fx.index.duplicated(keep="last")]
fx.index = fx.index.where(fx.index < "2011-01-01", fx.index - pd.offsets.BDay(1)); fx = fx[~fx.index.duplicated(keep="last")]
tk_a = lvl("TKC", "adj"); tc_a = lvl("TCELL.IS", "adj"); tk_c = lvl("TKC", "c"); tc_c = lvl("TCELL.IS", "c")
tcv = lvl("TCELL.IS", "v")
df = pd.DataFrame(index=cal)
df["tk"] = tk_a.reindex(cal); df["tc"] = tc_a[tcv.reindex(tc_a.index).fillna(0) > 0].reindex(cal); df["fx"] = fx.reindex(cal)
df["tkc"] = tk_c.reindex(cal); df["tcc"] = tc_c.reindex(cal)
# yalnızca TKC, TCELL ve kur aynı gün işlem görmüşse
df["P"] = np.log(df.tk * df.fx / (2.5 * df.tc))
df["Praw"] = np.log(df.tkc * df.fx / (2.5 * df.tcc))
df["D"] = df.P - df.P.shift(1).rolling(20, min_periods=10).mean()
dd = ll.decomp("TCELL"); dt = ll.decomp("TTKOM")
df["gap1"] = dd["gap"].shift(-1).reindex(cal); df["intra1"] = dd["intra"].shift(-1).reindex(cal); df["cc1"] = dd["cc"].shift(-1).reindex(cal)
df["tt_gap1"] = dt["gap"].shift(-1).reindex(cal); df["tt_intra1"] = dt["intra"].shift(-1).reindex(cal)
xu = ll.decomp("XU100") if False else None
x100 = R("XU100"); df["xu_cc1"] = x100.shift(-1).reindex(cal)
# XU100 gap (endeks açılış verisi) yerine TUR post-close proxy yok; kontrol olarak TUR_t getirisi
df["tur"] = R("TUR").reindex(cal)
df.to_parquet(RES + "/02_tkc_daily.parquet")

print("Prim seviyesi (Praw, c fiyatları) yıllık medyan %:"); print((100 * df.Praw.groupby(df.index.year).median()).round(2).to_dict())
q = df[df.index >= "2014-01-01"].dropna(subset=["D", "gap1"])
q = q[q.D.abs() < 0.15]
rows = []
for lab, s, e in [("ALL", "2014-01-01", "2026-12-31"), ("IS", "2014-01-01", "2020-12-31"), ("OOS", "2021-01-01", "2026-12-31"), ("3y", "2023-10-30", "2026-12-31")]:
    z = q[(q.index >= s) & (q.index <= e)]
    for y in ["gap1", "intra1", "cc1", "tt_gap1", "tt_intra1"]:
        b, t, n = ll.nw_t(z[y], z["D"]); c = z[[y, "D"]].dropna().corr().iloc[0, 1]
        rows.append((lab, y, round(c, 3), round(b, 3), round(t, 2), n))
A = pd.DataFrame(rows, columns=["per", "y", "corr", "beta", "t", "n"]); A.to_csv(RES + "/02_tkc_daily_D.csv", index=False)
print(A.to_string(index=False))
# yıllara göre gap1 ~ D ve intra1 ~ D
yr = q.groupby(q.index.year).apply(lambda z: pd.Series({"c_gap": z.gap1.corr(z.D), "b_gap": np.polyfit(z.D, z.gap1, 1)[0] if len(z) > 30 else np.nan,
                                                         "c_intra": z[["intra1", "D"]].dropna().corr().iloc[0, 1], "sdD_bps": 1e4 * z.D.std()}))
yr.to_csv(RES + "/02_tkc_byyear.csv"); print(yr.round(3).to_string())
# Kalan (açılışta bilinen) sapma: U = D_t - gap_{t+1} (TCELL'in açılışta kapatmadığı kısım) -> intra_{t+1}
q2 = q.dropna(subset=["intra1"]).copy(); q2["U"] = q2.D - q2.gap1
for lab, s, e in [("ALL", "2014", "2027"), ("IS", "2014", "2021"), ("OOS", "2021", "2027")]:
    z = q2[(q2.index >= s) & (q2.index < e)]
    b, t, n = ll.nw_t(z.intra1, z.U); print("intra_{t+1} ~ U=D-gap", lab, "beta", round(b, 3), "t", round(t, 2), "n", n)
# Mean reversion: P sapmasının yarı ömrü; hangi bacak kapatıyor (TCELL cc_{t+1} vs TKC_{t+1}+FX)
df["dP1"] = df.P.shift(-1) - df.P
df["tkfx1"] = (np.log(df.tk * df.fx)).shift(-1) - np.log(df.tk * df.fx)
z = df[df.index >= "2014"].dropna(subset=["D", "dP1", "cc1", "tkfx1"]); z = z[z.D.abs() < 0.15]
for y in ["dP1", "cc1", "tkfx1"]:
    b, t, n = ll.nw_t(z[y], z.D); print("Kapanma:", y, "~ D  beta", round(b, 3), "t", round(t, 2))
