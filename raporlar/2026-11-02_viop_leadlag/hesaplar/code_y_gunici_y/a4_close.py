"""GÖREV 4: KAPANIŞ -> ERTESİ GÜN.
Günlük değişkenler (h1, 2023-12..2026-10):  CA = log(C/P1500) kapanış müzayedesi (yalnız AB yaz saati günleri: 14:30 barı var),
  L30 = log(P1500/P1430) son 30 dk sürekli işlem (yaz), LH = log(C/P1430) son 30 dk + müzayede (yıl boyu), DAY = log(P1430/O).
Ertesi gün: gap_{t+1} (ll.decomp), r1_{t+1} (O->07:30), intra_{t+1}, rest_{t+1} (07:30->C).
VİOP vade sonu = her ayın son BIST iş günü (bültende VADE TARIHI ile doğrulandı: 2026-10-30, 2026-11-30, 2026-12-31). Çeyrek sonu (Mar/Haz/Eyl/Ara) = endeks dönem değişimi ile çakışır.
Uzun örneklem (günlük 2014+): ayın son iş günü cc getirisi ve ertesi gün gap/intra (kapanış müzayedesi ayrıştırılamaz).
m5 (60 gün): müzayede hacim payı = 1 - Σ(m5 hacim)/günlük hacim (açılış müzayedesi dahil), vade sonu günlerinde vs diğer.
Çıktı: res/a4_stock.csv, res/a4_pooled.csv, res/a4_expiry.csv, res/a4_daily_eom.csv, res/a4_auction_vol.csv
"""
import numpy as np, pandas as pd, c_common as c
ll = c.ll; TG = c.VIOP
D = c.h1_days(); days = D.index
cal = ll.bist_cal(); cal = cal[cal >= "2013-01-01"]
calS = pd.Series(cal, index=cal)
eom = calS.groupby([cal.year, cal.month]).max().values  # ayın son iş günü
EOM = pd.DatetimeIndex(eom)
QEND = EOM[EOM.month.isin([3, 6, 9, 12])]

def nxt(s):  # t+1 değerini t'ye getir (BIST takvimi)
    return s.shift(-1)

rows = []; pool = []
for s in TG + ["XU030"]:
    H = c.h1_panel(s); dd = ll.decomp(s).reindex(days)
    X = pd.DataFrame(index=days)
    X["CA"] = H["ca"]; X["L30"] = H["r9a"]; X["LH"] = H["r9"]; X["DAY"] = np.log(H["P1430"] / H["O"])
    X["gap1"] = nxt(dd["gap"]); X["r1_1"] = nxt(H["r1"]); X["intra1"] = nxt(H["intra"]); X["rest1"] = nxt(np.log(H["C"] / H["P0730"]))
    X["eom"] = X.index.isin(EOM); X["qend"] = X.index.isin(QEND)
    X["stock"] = s; X["date"] = X.index
    if s != "XU030": pool.append(X)
    half = days[len(days) // 2]
    for y in ["gap1", "r1_1", "intra1", "rest1"]:
        for xs, lab in [(["CA", "L30", "DAY"], "summer"), (["LH", "DAY"], "allyear")]:
            for per, m in [("all", X.index >= days[0]), ("is", X.index < half), ("oos", X.index >= half)]:
                df = X[m][[y] + xs].dropna()
                if len(df) < 80: continue
                b, se, cov, r2, n = c.ols_cl(df[y].values, df[xs].values, np.arange(len(df)) // 3)
                o = dict(stock=s, y=y, spec=lab, period=per, n=n, r2=r2)
                for i, x in enumerate(xs): o[f"b_{x}"] = b[1 + i]; o[f"t_{x}"] = b[1 + i] / se[1 + i]
                rows.append(o)
ST = pd.DataFrame(rows)
for (y, sp, per, ), g in ST.groupby(["y", "spec", "period"]):
    key = "t_CA" if sp == "summer" else "t_LH"
    rej, padj = ll.fdr(ll.t_to_p(g[key].values)); ST.loc[g.index, "fdr"] = rej
ST.to_csv(c.RES + "/a4_stock.csv", index=False)

PO = pd.concat(pool)
rows = []
for y in ["gap1", "r1_1", "intra1", "rest1"]:
    for xs, lab in [(["CA", "L30", "DAY"], "summer"), (["LH", "DAY"], "allyear")]:
        for sub, m in [("all", np.ones(len(PO), bool)), ("eom", PO["eom"].values), ("non_eom", ~PO["eom"].values), ("qend", PO["qend"].values)]:
            df = PO[m][[y, "date"] + xs].dropna()
            if len(df) < 200: continue
            b, se, cov, r2, n = c.ols_cl(df[y].values, df[xs].values, df["date"].values)
            o = dict(y=y, spec=lab, sub=sub, n=n, ndays=df["date"].nunique(), r2=r2)
            for i, x in enumerate(xs): o[f"b_{x}"] = b[1 + i]; o[f"t_{x}"] = b[1 + i] / se[1 + i]
            rows.append(o)
pd.DataFrame(rows).to_csv(c.RES + "/a4_pooled.csv", index=False)
print(pd.DataFrame(rows).round(4).to_string())

# vade sonu günleri: müzayede büyüklüğü ve işaret
rows = []
for s in TG + ["XU030"]:
    H = c.h1_panel(s)
    ca = H["ca"].dropna(); e = ca.index.isin(EOM)
    rows.append(dict(stock=s, n_eom=int(e.sum()), n_other=int((~e).sum()), absCA_eom_bps=1e4 * ca[e].abs().mean(), absCA_other_bps=1e4 * ca[~e].abs().mean(),
                     CA_eom_bps=1e4 * ca[e].mean(), CA_other_bps=1e4 * ca[~e].mean(),
                     LH_eom_bps=1e4 * H["r9"][H.index.isin(EOM)].mean(), LH_other_bps=1e4 * H["r9"][~H.index.isin(EOM)].mean()))
EX = pd.DataFrame(rows); EX.to_csv(c.RES + "/a4_expiry.csv", index=False)
print(EX.describe().round(2).to_string())

# günlük uzun örneklem: ay sonu günü ve ertesi gün
rows = []
for s in TG + ["XU030"]:
    d = ll.decomp(s); d = d[d.index >= "2014-01-01"]
    e = d.index.isin(EOM); f = pd.Series(e, d.index).shift(1).fillna(False).astype(bool).values  # ayın ilk günü
    # ay sonu kapanış hareketi -> ertesi gün gap: corr(cc_t, gap_{t+1}) ay sonu vs diğer
    g1 = d["gap"].shift(-1); i1 = d["intra"].shift(-1)
    for per, m in [("all", np.ones(len(d), bool)), ("is", d.index < "2021-01-01"), ("oos", d.index >= "2021-01-01")]:
        x = d[m]; ee = e[m]; ff = f[m]
        rows.append(dict(stock=s, period=per, cc_eom_bps=1e4 * x["cc"][ee].mean(), intra_eom_bps=1e4 * x["intra"][ee].mean(), gap_eom_bps=1e4 * x["gap"][ee].mean(),
                         cc_other_bps=1e4 * x["cc"][~ee & ~ff].mean(), gap_first_bps=1e4 * x["gap"][ff].mean(), intra_first_bps=1e4 * x["intra"][ff].mean(),
                         corr_intra_eom_gapnext=pd.concat([x["intra"][ee], g1[m][ee]], axis=1).corr().iloc[0, 1],
                         corr_intra_oth_gapnext=pd.concat([x["intra"][~ee], g1[m][~ee]], axis=1).corr().iloc[0, 1], n_eom=int(ee.sum())))
pd.DataFrame(rows).to_csv(c.RES + "/a4_daily_eom.csv", index=False)

# m5: müzayede hacim payı
rows = []
for s in TG:
    P = c.m5_panel(s); days5 = P["days"]
    share = 1 - np.nansum(P["V"], axis=1) / P["dV"]
    ca5 = np.log(P["dC"] / P["C"][:, -1])
    e = days5.isin(EOM)
    rows.append(dict(stock=s, auc_share_eom=np.nanmean(share[e]), auc_share_other=np.nanmedian(share[~e]), absCA5_eom_bps=1e4 * np.nanmean(np.abs(ca5[e])),
                     absCA5_other_bps=1e4 * np.nanmean(np.abs(ca5[~e])), eom_days=",".join(str(x.date()) for x in days5[e])))
pd.DataFrame(rows).to_csv(c.RES + "/a4_auction_vol.csv", index=False)
print("bitti")
