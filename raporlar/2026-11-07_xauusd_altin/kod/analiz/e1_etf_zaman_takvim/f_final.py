"""(f) Son adaylar: uygulanabilir sürümler (yalnız uzun / ters ETF / kaldıraçlı), yıl yıl P&L, uç dönem sağlamlığı
(2008; Nisan 2013; Mart 2020; Ocak–Şubat 2026 hariç ve içinde), 2022+ alt dönem; SPY kontrolü; tatil türüne göre ayrım."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim")
from e1_common import *
reset("f_")
pd.set_option("display.width", 260)
F = pd.read_pickle(f"{O}/a_feats.pkl"); MK = pd.read_pickle(f"{O}/c_masks.pkl")
EXT = {"2008": ("2008-01-01", "2008-12-31"), "2013-04": ("2013-04-01", "2013-04-30"), "2020-03": ("2020-03-01", "2020-03-31"), "2026-01/02": ("2026-01-01", "2026-02-28")}
def entry(mask):  # getiri günü maskesi -> giriş günü pozisyonu (önceki işlem günü kapanışında al, 1 gün tut)
    return mask.reindex(IDX).fillna(False).astype(float).shift(-1).fillna(0)

CAND = {
    "madenci_tatil_oncesi": (["GDX", "GDXJ"], 1, entry(MK["pre_hol"])),
    "madenci_ayin_ilk_gunu": (["GDX", "GDXJ"], 1, entry(MK["first"])),
    "madenci_takvim_sepeti(tatil_oncesi|ilk_gun)": (["GDX", "GDXJ"], 1, entry(MK["pre_hol"] | MK["first"])),
    "GDX_4gun_dusus_sonrasi_al_h3": (["GDX"], 3, (F[("GDX", "strict", "streak")] <= -4).astype(float)),
    "GDX_5gun_dusus_sonrasi_al_h1": (["GDX"], 1, (F[("GDX", "strict", "streak")] <= -5).astype(float)),
    "GLD_Ocak": (["GLD"], 1, entry(pd.Series(IDX.month == 1, index=IDX))),
    "GLD_tatil_oncesi": (["GLD"], 1, entry(MK["pre_hol"])),
    "GLD_BollZ<-2_h5": (["GLD"], 5, (F[("GLD", "strict", "bbz")] < -2).astype(float)),
}
tabs = []; yrs = []; ext = []; regs = []
for nm, (tks, h, pos) in CAND.items():
    for t in tks:
        df = strat_table(pos, h, t, nm); tabs.append(df)
        # yıl yıl net P&L (yalnız uzun, temel maliyet) ve kaldıraçlı
        net, tr = bt2(pos, h, t, cost=COST[t])
        bh = RS[t].reindex(net.index)
        y = net.groupby(net.index.year).sum() * 100
        yrs.append(pd.DataFrame({"strateji": nm, "etf": t, "yil": y.index, "net_pct": y.round(2).values,
                                 "al_tut_pct": (bh.groupby(bh.index.year).sum() * 100).round(1).reindex(y.index).values}))
        # uç dönemler
        for k, (a, b) in EXT.items():
            m = (net.index >= a) & (net.index <= b)
            ex = net[~m]
            ext.append(dict(strateji=nm, etf=t, donem=k, donem_ici_net_pct=round(net[m].sum() * 100, 2), haric_sh=perf(ex)["sh"], haric_sh_oos=perf(ex[ex.index > IS_END])["sh"], tum_sh=perf(net)["sh"]))
        allm = np.zeros(len(net), bool)
        for k, (a, b) in EXT.items(): allm |= (net.index >= a) & (net.index <= b)
        ex = net[~allm]; ext.append(dict(strateji=nm, etf=t, donem="hepsi_haric", donem_ici_net_pct=round(net[allm].sum() * 100, 2), haric_sh=perf(ex)["sh"], haric_sh_oos=perf(ex[ex.index > IS_END])["sh"], tum_sh=perf(net)["sh"]))
        # kayıt: strateji düzeyi (getiri günü kuklası testi = rstats)
        st = rstats(pos.where(R[t].notna()), fwd(R[t], h), h)
        reg("f_final", f"f_final|{nm}|{t}|h{h}", nm, h, st, "son aday; yalnız uzun bacak")
        regs.append(dict(strateji=nm, etf=t, h=h, t=round(st["t"], 2), t_is=round(st["t_is"], 2), t_oos=round(st["t_oos"], 2), t_22=round(st["t_22"], 2), yrs=f"{st['yrs_same_sign']}/{st['yrs']}"))
T = pd.concat(tabs); T.to_csv(f"{O}/f_final_strateji.csv", index=False)
Y = pd.concat(yrs); Y.to_csv(f"{O}/f_final_yillik.csv", index=False)
X = pd.DataFrame(ext); X.to_csv(f"{O}/f_final_uc_donem.csv", index=False)
RG = pd.DataFrame(regs); RG.to_csv(f"{O}/f_final_testler.csv", index=False)
print(RG.to_string())
q = T[(T.cost == "temel")].pivot_table(index=["strategy", "base", "version"], columns="period", values="sh", aggfunc="first")[["full", "is", "oos", "p22"]]
print(q.to_string())
q2 = T[(T.period == "oos")].pivot_table(index=["strategy", "base", "version"], columns="cost", values=["sh", "ann", "rt_yr", "bh_sh", "mdd"], aggfunc="first")
print(q2.to_string())
print(X.to_string())
print(Y.pivot_table(index="yil", columns=["strateji", "etf"], values="net_pct").round(1).to_string())

# Ek kontroller: (1) tatil öncesi etkisi SPY aynı gün getirisi kontrolüyle; (2) tatil türüne göre; (3) GDXJ ilk gün SPY kontrolü
import statsmodels.api as sm
spy = np.log(D.c_SPY).diff()
for t in ["GDX", "GDXJ", "GLD"]:
    d = pd.concat([R[t].rename("r"), spy.rename("s"), MK["pre_hol"].astype(float).rename("pre"), MK["first"].astype(float).rename("first")], axis=1).dropna()
    for sub, dd in [("tum", d), ("OOS", d[d.index > IS_END])]:
        m = sm.OLS(dd.r, sm.add_constant(dd[["s", "pre", "first"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        print(t, sub, "SPY kontrollü: pre b=%.1f bps t=%.2f | first b=%.1f bps t=%.2f" % (m.params.pre * 1e4, m.tvalues.pre, m.params["first"] * 1e4, m.tvalues["first"]))
hol = pd.read_csv(f"{S}/out/a3_takvim_olay/events_tatiller.csv", parse_dates=["date"]); hol = hol[hol.market == "NYSE"]
pre_days = IDX[MK["pre_hol"].values]
rows = []
for d0 in pre_days:
    nx = hol[(hol.date > d0) & (hol.date <= d0 + pd.Timedelta(days=4))]
    rows.append(dict(gun=d0, tatil=nx.name.iloc[0] if len(nx) else "2008/bilinmiyor", GDX=R.GDX.get(d0), GDXJ=R.GDXJ.get(d0), GLD=R.GLD.get(d0), SPY=spy.get(d0)))
H = pd.DataFrame(rows); H.to_csv(f"{O}/f_tatil_oncesi_gunler.csv", index=False)
g = (H.groupby("tatil")[["GDX", "GDXJ", "GLD", "SPY"]].mean() * 1e4).round(1); g["n"] = H.groupby("tatil").size(); print(g.to_string())
