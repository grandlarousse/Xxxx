"""v_YG2_a / 5: UZUN ÖRNEKLEM VEKİLİ (2017-2026) — kapanış fiyatındaki geçici sapma ertesi açılışta dönüyor mu?
CA (P15:00) yalnız h1 döneminde (2023-11+) var. 2014-2020 IS testi doğrudan YAPILAMAZ. Vekil:
  ex_t = Δ[log(SSF_uzlaşma_t / C_t)]  (aynı sözleşme, t-1'e göre), gün içi kesitsel ortalaması çıkarılmış.
  v2'de h1 döneminde ex_t ≈ -0,585·CA_t (t -22): SSF uzlaşması müzayede hareketinin yalnız ~%41'ini izliyor.
  Spot C_t geçici olarak düşükse ex_t > 0  -> ertesi gap pozitif beklenir.
UYARI: bu sinyal İŞLENEMEZ (uzlaşma 18:15'te kesinleşir, spot kapanış fiyatından işlemler 18:10'da biter); yalnız mekanizma
kanıtı. Ayrıca SSF uzlaşması 18:05-18:15 küresel bilgisini de taşır (kesitsel arındırma piyasa bileşenini atar).
Spot temizlik: bayat gün (v==0 & h==l) NaN; kurumsal işlem eşiği 2020-03-13 öncesi ±%20,5, sonrası ±%10,5.
Yahoo açılışı 2014 öncesi bozuk -> burada 2017+ (bülten başlangıcı).
"""
import numpy as np, pandas as pd, vcommon as v
pd.set_option("display.width", 250)
V47 = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
ALIAS = {"TRALT": ["TRALT", "KOZAL"], "TRMET": ["TRMET", "KOZAA"]}
cal = pd.read_parquet(v.SCR + "/data/daily/XU030.IS.parquet"); cal = pd.DatetimeIndex(cal.ldate).normalize().unique().sort_values()
cal = cal[cal >= "2017-03-01"]
nxt = dict(zip(cal[:-1], cal[1:])); prv = dict(zip(cal[1:], cal[:-1]))
F = pd.read_parquet(v.SCR + "/data/viop_panel.parquet", columns=["date", "code", "root", "segment", "expiry", "settle", "trades"])
F = F[F.segment == "SSF"].copy(); F["date"] = pd.to_datetime(F.date).dt.normalize(); F["expiry"] = pd.to_datetime(F.expiry).dt.normalize()
F["nextday"] = F.date.map(nxt)
fr = F[F.expiry > F.nextday].sort_values(["root", "date", "expiry"]).groupby(["root", "date"]).head(1)[["root", "date", "code", "settle", "trades"]]
fr["prevday"] = fr.date.map(prv)
f0 = F[["code", "date", "settle"]].rename(columns={"date": "prevday", "settle": "settle0"})
fr = fr.merge(f0, on=["code", "prevday"], how="left")
rows = []
for s in V47:
    try:
        d = pd.read_parquet(f"{v.SCR}/data/daily/{s}.IS.parquet")
    except FileNotFoundError:
        continue
    d.index = pd.DatetimeIndex(d.ldate).normalize(); d = d[~d.index.duplicated(keep="last")].sort_index()
    d = d[["o", "h", "l", "c", "v"]].astype(float)
    d.loc[(d.v.fillna(0) == 0) & (d.h == d.l), :] = np.nan
    d = d.reindex(cal)
    lim = np.where(d.index < "2020-03-13", 0.205, 0.105)
    C0 = d.c.shift(1); O1 = d.o.shift(-1); C1 = d.c.shift(-1)
    def lgl(a, b, lim_):
        x = np.log(a / b); x[np.abs(np.exp(x) - 1) > lim_] = np.nan; return x
    out = pd.DataFrame(index=d.index)
    out["C"] = d.c; out["C0"] = C0
    out["gap1"] = lgl(O1, d.c, np.r_[lim[1:], 0.105]); out["cc1"] = lgl(C1, d.c, np.r_[lim[1:], 0.105]); out["intra1"] = out.cc1 - out.gap1
    out["cc"] = lgl(d.c, C0, lim)
    roots = ALIAS.get(s, [s])
    ff = fr[fr.root.isin(roots)].drop_duplicates("date").set_index("date")
    out = out.join(ff[["settle", "settle0", "trades"]])
    out["ex"] = np.log(out.settle / out.C) - np.log(out.settle0 / out.C0)
    out.loc[out.ex.abs() > 0.05, "ex"] = np.nan  # temettü/bölünme düzeltme günleri
    out.loc[out.cc.isna(), "ex"] = np.nan
    out["stock"] = s; out["date"] = out.index
    rows.append(out.reset_index(drop=True))
L = pd.concat(rows, ignore_index=True)
for c in ["ex", "gap1", "cc1", "intra1", "cc"]:
    L[c + "_dm"] = L[c] - L.groupby("date")[c].transform("mean")
L["year"] = L.date.dt.year
res = []
def reg(lab, m, y="gap1_dm"):
    d = L[m][[y, "ex_dm", "cc_dm", "date"]].dropna()
    if len(d) < 300: return
    b, se, n, G = v.ols_cl(d[y].values, d[["ex_dm", "cc_dm"]].values, d.date.values)
    # portföy: +sign(ex) |ex|>25 bps, getiri kesitsel arındırılmış gap
    dd = d[d.ex_dm.abs() > 0.0025]; pnl = np.sign(dd.ex_dm) * dd[y] * 1e4; pd_ = pnl.groupby(dd.date).mean(); m_, t_, nd = v.nw_t(pd_)
    res.append(dict(sub=lab, y=y, n=n, days=G, b_ex=b[1], t_ex=b[1] / se[1], port_bps=m_, port_t=t_, port_days=nd))
for y in ["gap1_dm", "intra1_dm", "cc1_dm"]:
    reg("ALL 2017-2026", L.date >= "2017-03-01", y)
    reg("IS 2017-2020", L.date < "2021-01-01", y)
    reg("OOS 2021-2026", L.date >= "2021-01-01", y)
    reg("h1 dönemi 2023-12+", L.date >= "2023-12-01", y)
for yr in range(2017, 2027):
    reg(str(yr), L.year == yr, "gap1_dm")
reg("2017-03..2022-09 (SSF seans sonu 18:10)", L.date < "2022-09-23", "gap1_dm")
reg("2022-09-23+ (SSF seans sonu 18:15)", L.date >= "2022-09-23", "gap1_dm")
R = pd.DataFrame(res); R.to_csv(v.RES + "/v5_longproxy.csv", index=False)
print(R.round(3).to_string())
