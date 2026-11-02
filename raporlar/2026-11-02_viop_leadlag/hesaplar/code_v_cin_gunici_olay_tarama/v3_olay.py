"""V2 FOMC gecesi gap betası; V3 negatif siyasi şoklar; V5 XAUTRY kısmi korelasyonları."""
import numpy as np, pandas as pd
from vcore import *
log = open(f"{OUT}/v3_olay.log", "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); log.write(s + "\n"); log.flush()
c = cal()
# ---------------- V2 FOMC ----------------
# Kendi FOMC listem (planlı toplantıların 2. günü; Fed takvimi, hafızadan). Kaynak listeyle karşılaştırılır.
MY = """2014-01-29 2014-03-19 2014-04-30 2014-06-18 2014-07-30 2014-09-17 2014-10-29 2014-12-17
2015-01-28 2015-03-18 2015-04-29 2015-06-17 2015-07-29 2015-09-17 2015-10-28 2015-12-16
2016-01-27 2016-03-16 2016-04-27 2016-06-15 2016-07-27 2016-09-21 2016-11-02 2016-12-14
2017-02-01 2017-03-15 2017-05-03 2017-06-14 2017-07-26 2017-09-20 2017-11-01 2017-12-13
2018-01-31 2018-03-21 2018-05-02 2018-06-13 2018-08-01 2018-09-26 2018-11-08 2018-12-19
2019-01-30 2019-03-20 2019-05-01 2019-06-19 2019-07-31 2019-09-18 2019-10-30 2019-12-11
2020-01-29 2020-04-29 2020-06-10 2020-07-29 2020-09-16 2020-11-05 2020-12-16
2021-01-27 2021-03-17 2021-04-28 2021-06-16 2021-07-28 2021-09-22 2021-11-03 2021-12-15
2022-01-26 2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14
2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26 2023-09-20 2023-11-01 2023-12-13
2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-10-29 2025-12-10
2026-01-28 2026-03-18 2026-04-29 2026-06-17 2026-07-29 2026-09-16 2026-10-28""".split()
MY = pd.DatetimeIndex(MY)
EV = pd.read_csv(f"{S}/out/olay_tarihleri.csv", parse_dates=["date", "react_date"])
src = pd.DatetimeIndex(EV[(EV.type == "FOMC") & (EV["sub"] == "scheduled")]["date"])
P("FOMC: benim liste", len(MY), "kaynak", len(src), "| fark (kaynakta var bende yok):", sorted(set(src.date) - set(MY.date)), "| (bende var kaynakta yok):", sorted(set(MY.date) - set(src.date)))
# tepki günü = karar gününden sonraki ilk BIST günü (karar 18/19 UTC > BIST kapanışı 15:10 UTC)
react = pd.DatetimeIndex([c[c.searchsorted(d, side="right")] for d in MY if c.searchsorted(d, side="right") < len(c)])
# ES günlük getiri (BIST takviminde, ~21 UTC kapanış), d günü -> d+1 satırına
es = ret("ES=F", "c")
es_l = es.shift(1)  # BIST t satırında t-1 BIST günündeki ES getirisi (t-1 günü ~21 UTC'ye kadar)
g100 = decomp("XU100.IS"); gx = decomp("XBANK.IS"); g30 = decomp("XU030.IS")
isF = pd.Series(c.isin(react), index=c)
# karar günü BIST günü olmalı (FOMC günü BIST açık): karar günü c'de mi
P("tepki günleri BIST takviminde:", int(isF.sum()))
def beta_corr(y, x, m):
    df = pd.concat([y[m], x[m]], axis=1).dropna()
    b, th, to = hc_t(df.iloc[:, 0], df.iloc[:, 1])
    return dict(beta=b, corr=df.corr().iloc[0, 1], tHC=th, n=len(df))
for nm, G in [("XU100", g100), ("XBANK", gx), ("XU030", g30)]:
    for w, (a, b) in [("tam", WIN["tam"]), ("IS", WIN["IS"]), ("OOS", WIN["OOS"])]:
        m = (c >= a) & (c <= b)
        F_ = beta_corr(G["gap"], es_l, isF.values & m); N_ = beta_corr(G["gap"], es_l, (~isF.values) & m)
        # etkileşim testi
        df = pd.DataFrame({"y": G["gap"], "x": es_l, "f": isF.astype(float)})[m].dropna(); df["xf"] = df.x * df.f
        X = np.column_stack([np.ones(len(df)), df.x, df.f, df.xf]); bb = np.linalg.lstsq(X, df.y, rcond=None)[0]; e = df.y - X @ bb
        XtXi = np.linalg.inv(X.T @ X); V = XtXi @ (X.T * e.values ** 2) @ X @ XtXi
        P(f"{nm} {w:4s}: FOMC gecesi β {F_['beta']:.3f} r {F_['corr']:.3f} (n {F_['n']}) | normal β {N_['beta']:.3f} r {N_['corr']:.3f} (n {N_['n']}) | fark β {bb[3]:.3f} tHC {bb[3]/np.sqrt(V[3,3]):.2f}")
    absr = G["gap"].abs()
    P(f"   |gap| FOMC sonrası / normal = {absr[isF].mean() / absr[~isF].mean():.2f}; medyan oranı {absr[isF].median() / absr[~isF].median():.2f}; |intra| oranı {G['intra'].abs()[isF].mean() / G['intra'].abs()[~isF].mean():.2f}")
# ES günlük getirisinin ne kadarı BIST kapanışı sonrası? (h1 2024-06+): FOMC vs diğer günler
sn = snap("ES=F", ["15:00", "21:00"])
post = np.log(sn["21:00"] / sn["15:00"])
esd = es.reindex(post.index)
dd = pd.DataFrame({"post": post, "full": esd}).dropna()
dd["F"] = dd.index.isin(MY)
P(f"ES (h1, 2024-06+): kapanış sonrası 15->21 UTC hareketin günlük ES getirisine oranı (var payı): FOMC {np.var(dd[dd.F].post)/np.var(dd[dd.F].full):.2f} (n {dd.F.sum()}) | diğer {np.var(dd[~dd.F].post)/np.var(dd[~dd.F].full):.2f}")
# Plasebo: FOMC olmayan Çarşamba geceleri
wed = pd.Series(c.weekday == 3, index=c) & ~isF  # Perşembe tepki günleri (Çarşamba gecesi)
for nm, G in [("XU100", g100)]:
    W_ = beta_corr(G["gap"], es_l, wed.values); P(f"plasebo {nm} FOMC-dışı Çarşamba gecesi β {W_['beta']:.3f} r {W_['corr']:.3f} n {W_['n']}")
# 2020 hariç ve en büyük 3 olay hariç
m = isF.values & ~((c >= "2020-01-01") & (c <= "2020-12-31"))
P("XU100 FOMC β 2020 hariç:", round(beta_corr(g100["gap"], es_l, m)["beta"], 3))
df = pd.concat([g100["gap"][isF.values], es_l[isF.values]], axis=1).dropna(); df.columns = ["y", "x"]
top = df.x.abs().nlargest(3).index
d2 = df.drop(top); b, th, _ = hc_t(d2.y, d2.x); P(f"XU100 FOMC β en büyük |ES| 3 olay hariç: {b:.3f} (t {th:.2f}); çıkarılanlar {[str(t.date()) for t in top]}")
# yıllar: FOMC β - normal β işareti
yrs = []
for yr in range(2014, 2027):
    m = (c.year == yr)
    try:
        yrs.append((yr, beta_corr(g100["gap"], es_l, isF.values & m)["beta"], beta_corr(g100["gap"], es_l, (~isF.values) & m)["beta"]))
    except Exception: pass
Y = pd.DataFrame(yrs, columns=["yil", "bF", "bN"]); P("yıllara göre (FOMC β > normal β):", int((Y.bF > Y.bN).sum()), "/", len(Y), Y.round(2).to_dict("list"))

# ---------------- V3 siyasi şoklar ----------------
P("\nV3: siyasi şoklar (kaynak liste, dir=-1)")
pol = EV[EV.type == "POLITICAL"].copy()
xu = decomp("XU100.IS"); xb = decomp("XBANK.IS")
rows = []
for _, e in pol.iterrows():
    t = e.react_date
    if t not in c: t = c[c.searchsorted(t)]
    rows.append(dict(date=e.date.date(), react=t.date(), dir=e.dir, timing=e.timing, sub=e["sub"], note=e.note[:45],
                     xu_gap=xu.gap.get(t) * 1e4, xu_intra=xu.intra.get(t) * 1e4, xu_cc=xu.cc.get(t) * 1e4, xb_cc=xb.cc.get(t) * 1e4, xb_gap=xb.gap.get(t) * 1e4))
E = pd.DataFrame(rows); E.round(0).to_csv(f"{OUT}/v3_political.csv", index=False)
P(E.round(0).to_string(index=False))
sd_gap = xu.gap.loc["2014":].std() * 1e4
for lab, sub in [("dir=-1 tümü", E[E.dir == -1]), ("dir=-1 seans dışı (weekend/night/pre_open)", E[(E.dir == -1) & (E.timing != "in_session")]),
                 ("dir=-1 in_session", E[(E.dir == -1) & (E.timing == "in_session")]), ("dir=+1", E[E.dir == 1])]:
    g = sub.xu_gap.dropna()
    P(f"{lab:45s} n {len(g)} XU100 gap ort {g.mean():.0f} bps medyan {g.median():.0f} t {g.mean()/(g.std(ddof=1)/np.sqrt(len(g))):.2f} negatif {int((g<0).sum())}/{len(g)} | XBANK cc ort {sub.xb_cc.mean():.0f} (t {sub.xb_cc.mean()/(sub.xb_cc.std()/np.sqrt(sub.xb_cc.notna().sum())):.2f}) | XU100 cc ort {sub.xu_cc.mean():.0f}")
g = E[E.dir == -1].xu_gap.dropna()
P(f"  en büyük 2 negatif gap hariç ort {g.drop(g.nsmallest(2).index).mean():.0f} bps (t {g.drop(g.nsmallest(2).index).mean()/(g.drop(g.nsmallest(2).index).std()/np.sqrt(len(g)-2)):.2f}); normal gün gap std {sd_gap:.0f} bps; tüm günler ort gap {xu.gap.loc['2014':].mean()*1e4:.1f}")
# bootstrap/permütasyon: rastgele 18 gün (2014+) ortalama gap dağılımı
rng = np.random.default_rng(0); gg = xu.gap.loc["2014":].dropna().values
sims = np.array([rng.choice(gg, len(g), replace=False).mean() for _ in range(20000)]) * 1e4
P(f"  permütasyon p(ort <= {g.mean():.0f}) = {(sims <= g.mean()).mean():.4f}")
# kesit: XU100'e göre göreli cc (bankalar vs döviz gelirliler)
neg = pd.DatetimeIndex([pd.Timestamp(x) for x in E[E.dir == -1].react])
rel = {}
for s in ["VAKBN", "HALKB", "YKBNK", "GARAN", "ISCTR", "AKBNK", "TAVHL", "ENKAI", "TKFEN", "TUPRS", "TRALT", "CIMSA", "THYAO", "FROTO"]:
    d = decomp(s + ".IS")
    rr = (d.cc - xu.cc).reindex(neg).dropna() * 1e4
    rel[s] = (round(rr.mean()), round(rr.mean() / (rr.std() / np.sqrt(len(rr))), 2), len(rr))
P("  göreli cc (hisse − XU100), bps (ort, t, n):", rel)
# t+1..5 sürüklenme
fw = []
for t in neg:
    i = c.get_loc(pd.Timestamp(t)); fw.append(xu.cc.iloc[i + 1:i + 6].sum() * 1e4 if i + 6 <= len(c) else np.nan)
fw = pd.Series(fw).dropna(); P(f"  t+1..5 XU100 cc ort {fw.mean():.0f} bps t {fw.mean()/(fw.std()/np.sqrt(len(fw))):.2f} n {len(fw)}")

# ---------------- V5 XAUTRY ----------------
P("\nV5: XAUTRY (GC=F × USDTRY düzeltilmiş) kısmi korelasyonları")
gc = px("GC=F", "c"); usd = px("TRY=X", "c")
gcc = on_cal(gc); usc = on_cal(usd)
xau = np.log(gcc * usc).diff().rename("xau")
r_gc = np.log(gcc).diff().rename("gc"); r_usd = np.log(usc).diff().rename("usd")
x100 = ret("XU100.IS", "c").rename("xu"); eem = ret("EEM").rename("eem")
for s in ["TRALT", "TRMET", "GUBRF", "PETKM", "XBANK"]:
    y = ret(s + ".IS") if s != "XBANK" else ret("XBANK.IS", "c")
    for lab, x, ctrl in [("XAUTRY|XU100", xau, x100.to_frame()), ("XAUTRY|XU100+USD+EEM", xau, pd.concat([x100, r_usd, eem], axis=1)),
                         ("GC|XU100+USD", r_gc, pd.concat([x100, r_usd], axis=1)), ("USD|XU100", r_usd, x100.to_frame()),
                         ("XAUTRY ham", xau, None)]:
        rows_, yr, same, tot = full_report(y, x, ctrl)
        P(f"{s:6s} {lab:22s} {fmt(rows_, yr, same, tot)}")
    P("       yıllar (XAUTRY|XU100): " + ", ".join(f"{k}:{v:+.2f}" for k, v in by_year(y, xau, x100.to_frame()).items()))
# eşzamanlı 15:00 UTC XAUTRY (h1, 2023-11+)
sn = snap("GC=F", ["15:00"])["15:00"]; su = snap("TRY=X", ["15:00"])["15:00"]
xs = np.log((sn * su).reindex(c)).diff().rename("xs")
P("Eşzamanlı (15:00 UTC) XAUTRY, 2023-12+:")
for s in ["TRALT", "TRMET", "GUBRF"]:
    y = ret(s + ".IS")
    a = pc(y, xs, x100.to_frame(), ("2023-12-01", "2026-12-31")); b = pc(y, xau, x100.to_frame(), ("2023-12-01", "2026-12-31"))
    c2 = pc(y, xs, pd.concat([x100, r_usd], axis=1), ("2023-12-01", "2026-12-31"))
    P(f"  {s}: pc(15:00 XAUTRY|XU100) {a['r']:+.3f} (t {a['t']:.2f}, n {a['n']}) vs günlük-kapanış XAUTRY aynı dönem {b['r']:+.3f}; 15:00 XAUTRY|XU100+USD {c2['r']:+.3f}")
log.close()
