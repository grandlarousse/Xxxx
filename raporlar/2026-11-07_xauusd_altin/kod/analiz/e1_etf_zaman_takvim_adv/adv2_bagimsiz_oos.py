"""Adv2: Gerçek bağımsız örneklem dışı. Madenci takvim etkileri (ayın ilk günü, tatil öncesi, sepet) ve GDX 5 gün düşüş kuralı
2008 öncesi ABD listeli madenci hisselerinde (eşit ağırlık sepet: NEM, AEM, GFI, KGC, CDE, HL, RGLD, HMY, AU, PAAS, SSRM) ve
2008 sonrası seçimde kullanılmamış madenci ETF'lerinde (SIL, SILJ, RING, GOEX, SGDM, GOAU, SLVP). NYSE takvimi = ^GSPC günleri.
Ayrıca SPY/^GSPC kontrolü ve GLD/altın aynı gün kontrolü."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e1_etf_zaman_takvim_adv")
from adv_common import *
pd.set_option("display.width", 250)
gs = yahoo("_GSPC"); NY = gs.index[(gs.index >= "1981-01-01")]
# ^GSPC günleri NYSE işlem günleri mi? hafta içi kapalı gün sayısı yıl başına
bd = pd.bdate_range(NY.min(), NY.max()); cl = bd.difference(NY)
print("yıl başına hafta içi kapalı:", pd.Series(cl.year).value_counts().sort_index().to_dict())
M = cal_masks(NY)
STK = ["NEM", "AEM", "GFI", "KGC", "CDE", "HL", "RGLD", "HMY", "AU", "PAAS", "SSRM"]
RR = {}
for t in STK:
    y = yahoo(t).reindex(NY)
    r = np.log(y.adjclose).diff()
    r[(y.volume.fillna(0) <= 0)] = np.nan       # hacimsiz/bayat gün
    r[r.abs() > 0.5] = np.nan                    # veri hatası
    RR[t] = r
RR = pd.DataFrame(RR)
EW = RR.mean(axis=1, skipna=True).where(RR.notna().sum(axis=1) >= 3)
spx = np.log(gs.adjclose.reindex(NY)).diff()
gc = np.log(yahoo("GC_F").adjclose).diff().reindex(NY)   # 2000-08+
print("sepet üye sayısı (yıl ort):", RR.notna().sum(axis=1).groupby(NY.year).mean().round(1).to_dict())
rows = []
def addrow(series_name, r, m_name, m, a, b):
    e = ev(m, r, a, b); rows.append(dict(seri=series_name, olay=m_name, donem=f"{a[:4]}-{b[:4]}", **e))
for nm, r in [("madenci_EW", EW), ("NEM", RR.NEM), ("AEM", RR.AEM), ("GFI", RR.GFI), ("KGC", RR.KGC), ("HL", RR.HL), ("CDE", RR.CDE), ("^GSPC", spx), ("GC=F", gc)]:
    for mn, m in [("ilk_gun", M["first"]), ("tatil_oncesi", M["pre"]), ("sepet", M["first"] | M["pre"])]:
        for a, b in [("1983-01-01", "2007-12-31"), ("1983-01-01", "1995-12-31"), ("1996-01-01", "2007-12-31"), ("2001-01-01", "2007-12-31"), ("2008-01-01", "2026-12-31")]:
            addrow(nm, r, mn, m, a, b)
T = pd.DataFrame(rows); print(T.to_string()); T.to_csv(f"{O}/adv2_oncesi_2008.csv", index=False)

# madenci EW için SPX kontrollü regresyon 1983-2007
dd = pd.concat([EW.rename("y"), spx.rename("s"), M["first"].astype(float).rename("first"), M["pre"].astype(float).rename("pre")], axis=1).dropna()
for a, b in [("1983", "2007"), ("1996", "2007"), ("2008", "2026")]:
    q = dd.loc[a:b]
    m = sm.OLS(q.y, sm.add_constant(q[["s", "first", "pre"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    print(f"madenci_EW {a}-{b} SPX kontrollü: first {m.params['first']*1e4:.1f} bps t={m.tvalues['first']:.2f} | pre {m.params['pre']*1e4:.1f} bps t={m.tvalues['pre']:.2f} | beta {m.params.s:.2f}")

# Yıl yıl sepet (1983-2007) madenci EW ve 5 gün düşüş kuralı
sgn = np.sign(EW); stk = sgn.groupby((sgn != sgn.shift()).cumsum()).cumsum()
rows = []
for nm, r in [("madenci_EW", EW), ("NEM", RR.NEM), ("AEM", RR.AEM), ("GFI", RR.GFI), ("KGC", RR.KGC), ("HL", RR.HL)]:
    s = np.sign(r); k = s.groupby((s != s.shift()).cumsum()).cumsum()
    for thr in [3, 4, 5, 6]:
        sig = (k.shift(1) <= -thr)        # t-1'e kadar >=thr düşüş → gün t kapanışında al → t+1 getirisi
        # olay maskesi getiri günü cinsinden: getiri günü D = sinyal günü+1
        mday = sig.shift(1).fillna(False).astype(bool)
        for a, b in [("1983-01-01", "2007-12-31"), ("2008-01-01", "2026-12-31")]:
            e = ev(mday, r, a, b); rows.append(dict(seri=nm, kural=f"seri<=-{thr}->h1", donem=f"{a[:4]}-{b[:4]}", **e))
S5 = pd.DataFrame(rows); print(S5.to_string()); S5.to_csv(f"{O}/adv2_seri_oncesi_2008.csv", index=False)

# 2008 sonrası seçimde kullanılmamış madenci ETF'leri (panel takvimi)
Mp = cal_masks(idx)
rows = []
for t in ["GDX", "GDXJ", "SIL", "SILJ", "RING", "GOEX", "SGDM", "GOAU", "SLVP", "NEM", "AEM", "GFI", "KGC", "AU"]:
    y = yahoo(t).reindex(idx); r = np.log(y.adjclose).diff()
    for mn, m in [("ilk_gun", Mp["first"]), ("tatil_oncesi", Mp["pre"]), ("sepet", Mp["first"] | Mp["pre"])]:
        for a, b in [("2008-01-01", "2017-12-31"), ("2018-01-01", "2026-12-31"), ("2008-01-01", "2026-12-31")]:
            e = ev(m, r, a, b); rows.append(dict(seri=t, olay=mn, donem=f"{a[:4]}-{b[:4]}", **e))
    s = np.sign(r); k = s.groupby((s != s.shift()).cumsum()).cumsum()
    mday = (k.shift(1) <= -5).shift(1).fillna(False).astype(bool)
    for a, b in [("2008-01-01", "2017-12-31"), ("2018-01-01", "2026-12-31"), ("2008-01-01", "2026-12-31")]:
        e = ev(mday, r, a, b); rows.append(dict(seri=t, olay="seri<=-5", donem=f"{a[:4]}-{b[:4]}", **e))
P = pd.DataFrame(rows); P.to_csv(f"{O}/adv2_diger_etf.csv", index=False)
print(P.pivot_table(index=["olay", "seri"], columns="donem", values="t").round(2).to_string())
print(P.pivot_table(index=["olay", "seri"], columns="donem", values="ev_bps").round(1).to_string())
