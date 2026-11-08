"""(b) Gece (kapanış t-1 16:00 ET -> açılış t 09:30 ET) ve gün içi (09:30 -> 16:00 ET) ayrışımı. Yahoo günlük açılış (resmî açılış baskısı).
Gece = toplam (adjclose) - gün içi (close/open) -> temettü gece bacağına yazılır.
Gerçekçi dolum: saatlik (son 730 gün) ilk saat kapanışı 10:30 ET ve 5 dk (son 60 gün) 09:35 ET; ön seans 5 dk verisinden.
"""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim")
from e1_common import *
reset("b_")
TK = ["GLD", "IAU", "GLDM", "GDX", "GDXJ", "SLV", "UGL", "NUGT", "JNUG", "GLL", "DUST"]
ND = {t: night_day(t) for t in TK}
pd.set_option("display.width", 250)

# 1) Yıllık ayrışım (yıllık toplam log getiri, %): gece, gün içi, toplam
yr_rows = []
for t in TK:
    n, d, tot = ND[t]
    df = pd.DataFrame({"gece": n, "gun_ici": d, "toplam": tot}).dropna()
    g = df.groupby(df.index.year).sum() * 100
    g["n"] = df.groupby(df.index.year).size()
    for y, r in g.iterrows(): yr_rows.append(dict(etf=t, yil=y, gece=round(r.gece, 1), gun_ici=round(r.gun_ici, 1), toplam=round(r.toplam, 1), n=int(r.n)))
YR = pd.DataFrame(yr_rows); YR.to_csv(f"{O}/b_yillik_gece_gunici.csv", index=False)
for t in ["GLD", "GDX"]:
    print(t); print(YR[YR.etf == t].set_index("yil")[["gece", "gun_ici", "toplam"]].T.to_string())

# 2) Ortalama testleri (her ETF): gece ortalaması, gün içi ortalaması, fark; IS/OOS/2022+
sm = []
for t in TK:
    n, d, tot = ND[t]
    for nm, s in [("gece", n), ("gun_ici", d), ("gece-gun_ici", n - d)]:
        s = s.dropna()
        out = {}
        for k in PERIODS:
            q = sl(s, k)
            if len(q) < 100: out[k] = (np.nan, np.nan); continue
            r = nw_ols(q, pd.Series(1.0, index=q.index), lags=5, add_const=False)
            out[k] = (q.mean() * 252 * 100, r["t"])
        yrm = s.groupby(s.index.year).mean(); sg = np.sign(s.mean())
        st = dict(ic=float(s.mean()), t=out["full"][1], n=len(s), t_is=out["is"][1], t_oos=out["oos"][1], yrs_same_sign=int((np.sign(yrm) == sg).sum()), yrs=int(yrm.notna().sum()))
        reg("b_mean", f"b_mean|{t}|{nm}", f"ortalama {nm} getirisi", 0, st, "ic sütunu = günlük ortalama log getiri")
        sm.append(dict(etf=t, seg=nm, ann_full=round(out["full"][0], 1), t_full=round(out["full"][1], 2), ann_is=round(out["is"][0], 1) if pd.notna(out["is"][0]) else None, t_is=round(out["is"][1], 2) if pd.notna(out["is"][1]) else None,
                       ann_oos=round(out["oos"][0], 1), t_oos=round(out["oos"][1], 2), ann_22=round(out["p22"][0], 1), t_22=round(out["p22"][1], 2), yrs=f"{st['yrs_same_sign']}/{st['yrs']}", n=len(s)))
SM = pd.DataFrame(sm); SM.to_csv(f"{O}/b_ortalama_testleri.csv", index=False); print(SM.to_string())

# 3) Strateji: kapanışta al, açılışta sat (CO) / açılışta al kapanışta sat (OC) / al-tut; maliyet senaryoları
st_rows = []
for t in ["GLD", "IAU", "GLDM", "GDX", "GDXJ", "SLV", "UGL", "NUGT", "JNUG"]:
    n, d, tot = ND[t]
    df = pd.DataFrame({"n": np.expm1(n), "d": np.expm1(d), "bh": np.expm1(tot)}).dropna()
    for c in [0, 2, 5, 10, 20, 40]:
        for k in PERIODS:
            q = sl(df, k)
            if len(q) < 100: continue
            for nm, col in [("CO_kapanista_al_acilista_sat", "n"), ("OC_acilista_al_kapanista_sat", "d")]:
                p = q[col] - c / 1e4
                st_rows.append(dict(etf=t, strateji=nm, maliyet_bps_RT=c, period=k, **perf(p)))
            if c == 0: st_rows.append(dict(etf=t, strateji="al_tut", maliyet_bps_RT=0, period=k, **perf(q.bh)))
ST = pd.DataFrame(st_rows); ST.to_csv(f"{O}/b_strateji_CO_OC.csv", index=False)
print(ST[(ST.period.isin(["full", "oos", "p22"])) & (ST.maliyet_bps_RT.isin([0, 10, 20]))].pivot_table(index=["etf", "strateji", "maliyet_bps_RT"], columns="period", values="ann").to_string())
# başabaş maliyet (bps RT): ortalama gece basit getirisi
be = []
for t in ["GLD", "IAU", "GLDM", "GDX", "GDXJ", "SLV", "UGL", "NUGT", "JNUG"]:
    n, d, tot = ND[t]; x = np.expm1(n).dropna()
    be.append(dict(etf=t, **{f"basabas_bps_{k}": round(sl(x, k).mean() * 1e4, 2) for k in PERIODS}))
BE = pd.DataFrame(be); BE.to_csv(f"{O}/b_basabas_maliyet.csv", index=False); print(BE.to_string())

# 3b) Hafta sonu gecesi vs hafta içi
wk = []
for t in ["GLD", "GDX", "SLV"]:
    n, d, tot = ND[t]; n = n.dropna()
    gap = pd.Series(n.index, index=n.index).diff().dt.days
    for lab, m in [("hafta_sonu/tatil (>1 gün)", gap > 1), ("hafta_ici (1 gün)", gap == 1)]:
        q = n[m]; r = nw_ols(q, pd.Series(1.0, index=q.index), lags=5, add_const=False)
        wk.append(dict(etf=t, gece=lab, ort_bps=round(q.mean() * 1e4, 2), t=round(r["t"], 2), n=len(q),
                       ort_oos_bps=round(q[q.index > IS_END].mean() * 1e4, 2)))
    # fark testi
    s = (gap > 1).astype(float).where(n.notna()); st = rstats(s, n, 1)
    reg("b_weekend", f"b_weekend|{t}", "hafta sonu gecesi kuklası", 0, st)
WK = pd.DataFrame(wk); WK.to_csv(f"{O}/b_haftasonu_gece.csv", index=False); print(WK.to_string())

# 4) Gerçekçi dolum: resmî açılış vs 10:30 ET (saatlik ilk bar kapanışı) vs 09:35 ET (5 dk), ön seans
fill = []
for t in ["GLD", "IAU", "GLDM", "GDX", "GDXJ", "SLV", "NUGT", "UGL"]:
    fh = f"{S}/panel/yahoo_h/{t}.parquet"
    if not os.path.exists(fh): continue
    hh = pd.read_parquet(fh); hh.index = pd.to_datetime(hh.index)
    et = hh.index.tz_convert("America/New_York"); hh["d"] = et.normalize().tz_localize(None); hh["hm"] = et.strftime("%H:%M")
    first = hh[hh.hm == "09:30"].set_index("d")
    y = yahoo(t)
    df = pd.DataFrame({"pc": y.close.shift(1), "o": y.open, "c": y.close}).reindex(first.index).dropna()
    df["o_h"] = first.open.reindex(df.index); df["c1030"] = first.close.reindex(df.index)
    df = df.dropna()
    a = np.log(df.o / df.pc); b = np.log(df.c1030 / df.pc); a2 = np.log(df.o_h / df.pc)
    row = dict(etf=t, n_gun=len(df), bas=str(df.index.min().date()), gece_resmi_acilis_bps=round(a.mean() * 1e4, 2), gece_saatlik_bar_acilis_bps=round(a2.mean() * 1e4, 2),
               gece_1030ET_cikis_bps=round(b.mean() * 1e4, 2), gun_ici_resmi_bps=round(np.log(df.c / df.o).mean() * 1e4, 2), t_gece=round(a.mean() / a.std() * np.sqrt(len(a)), 2))
    f5 = f"{S}/panel/yahoo_5m/{t}.parquet"
    if os.path.exists(f5):
        m = pd.read_parquet(f5); m.index = pd.to_datetime(m.index); e5 = m.index.tz_convert("America/New_York")
        m["d"] = e5.normalize().tz_localize(None); m["hm"] = e5.strftime("%H:%M")
        o930 = m[m.hm == "09:30"].set_index("d"); pre = m[(m.hm >= "08:00") & (m.hm < "09:30")].groupby("d").close.last()
        q = pd.DataFrame({"pc": y.close.shift(1), "o": y.open}).reindex(o930.index)
        q["c935"] = o930.close; q["o930"] = o930.open; q["pre0925"] = pre.reindex(q.index); q = q.dropna()
        row.update(n_5dk=len(q), gece_resmi_5dk_bps=round(np.log(q.o / q.pc).mean() * 1e4, 2), gece_0935_bps=round(np.log(q.c935 / q.pc).mean() * 1e4, 2),
                   gece_onseans_son_bps=round(np.log(q.pre0925 / q.pc).mean() * 1e4, 2), acilis_vs_0935_mutlak_fark_bps=round((np.log(q.c935 / q.o)).abs().mean() * 1e4, 1))
    fill.append(row)
FL = pd.DataFrame(fill); FL.to_csv(f"{O}/b_dolum_gercekcilik.csv", index=False); print(FL.T.to_string())

# 5) Öngörü: gece ve gün içi bileşenler ileri h günü öngörüyor mu? (gece_t = gün t açılış boşluğu, 09:30 ET'de bilinir; *_lag = t-1)
pr = []
for t in ["GLD", "GDX", "GDXJ", "SLV"]:
    n, d, tot = ND[t]
    preds = {"gece_t(acilis_boslugu)": n, "gece_t-1": n.shift(1), "gun_ici_t-1": d.shift(1)}
    for nm, x in preds.items():
        for h in [1, 3, 5]:
            st = split_stats(x, fwd(R[t], h), h); reg("b_pred", f"b_pred|{t}|{nm}|h{h}", nm, h, st)
            pr.append(dict(etf=t, pred=nm, h=h, ic=round(st["ic"], 3), t=round(st["t"], 2), t_is=round(st["t_is"], 2), t_oos=round(st["t_oos"], 2), yrs=f"{st['yrs_same_sign']}/{st['yrs']}"))
PR = pd.DataFrame(pr); PR.to_csv(f"{O}/b_ongoru.csv", index=False); print(PR.to_string())
