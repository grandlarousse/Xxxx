"""(C) Faiz dongusu ve bankalar. Olaylar onceden tanimli:
  DONUS (politika faizi): yonu bir onceki degisikligin tersi olan ilk degisiklik (TCMB 1 Hafta Repo tablosu, 2010-05 sonrasi).
  FIILI DONUS: politika faizi degismeden fonlama ile yapilan ani donusler: 2025-03-20 (O/N %46, ara PPK), 2026-03-01 (repo ihalelerine ara, AOFM %37->%40),
               2026-08-23 (repo ihaleleri yeniden, AOFM %40->%37). AOFM algoritmik donus (5g ort, son donusten bu yana uc noktadan >=150bp) ayrica.
  SURPRIZ (piyasa bazli): PPK gunu 2Y getiri degisimi (TCMB gosterge degerlerinden kurulan 2Y, t-1 kapanis -> t). En sahin %10 / en guvercin %10.
Giris: karar gunu kapanisi (karar 14:00'te; olaganustu/aksam kararlarinda sonraki islem gunu). Ufuk 21/42/63 islem gunu.
Ciktilar: XBANK/XU100 ve IHRACATCI/YURTICI (esit agirlikli, onceden secilmis sepetler) goreli getirileri; placebo: ayni ufuktaki tum gunlerin dagilimi
ve ayni sayida rastgele tarihle bootstrap p. 2Y oncu sinyal: gecmis 20g Delta2Y (t-1 degeri) -> ileri goreli XBANK getirisi (NW t), tercile ve alt donemler."""
import numpy as np, pandas as pd, statsmodels.api as sm
import ortak as O
rng = np.random.default_rng(7)
TK = O.islem_gunleri(); TK = TK[(TK >= "2009-06-01") & (TK <= "2026-11-05")]   # 06.11 gun ici (kismi) -> haric
xu = O.endeks("XU100").reindex(TK).ffill(); xb = O.endeks("XBANK").reindex(TK).ffill()
IHR = "FROTO TOASO ARCLK VESTL EREGL KRDMD SISE BRISA OTKAR KORDS AKSA EGEEN".split()
YUR = "BIMAS MGROS SOKM TTKOM TCELL EKGYO ENJSA DOAS AYGAZ AEFES".split()
def sepet(ks):
    R = pd.concat({k: O.hisse(k, fetch=False).r.reindex(TK) for k in ks if O.hisse(k, fetch=False) is not None}, axis=1)
    R = R.clip(-0.5, 0.5)
    ew = R.mean(axis=1, skipna=True).fillna(0); n = R.notna().sum(axis=1)
    return (1 + ew).cumprod(), n
ihr, nih = sepet(IHR); yur, nyu = sepet(YUR)
xusin = O.endeks("XUSIN").reindex(TK).ffill(); xuhiz = O.endeks("XUHIZ").reindex(TK).ffill()
P = pd.DataFrame({"XU100": xu, "XBANK": xb, "IHR": ihr, "YUR": yur, "XUSIN": xusin, "XUHIZ": xuhiz})
P["BANK_REL"] = P.XBANK / P.XU100; P["IHR_YUR"] = P.IHR / P.YUR; P["SIN_HIZ"] = P.XUSIN / P.XUHIZ
y2 = pd.read_parquet(O.MY + "/tcmb/y2.parquet").y2.reindex(TK).ffill(limit=3)
aofm = pd.read_parquet(O.MY + "/tcmb/aofm.parquet").TP_APIFON4.reindex(TK).ffill(limit=5)
P["y2"] = y2; P["aofm"] = aofm
# politika faizi (yururluk tarihleri, TCMB 1 hafta repo tablosu)
PF = [("2010-05-20", 7.00), ("2010-12-17", 6.50), ("2011-01-21", 6.25), ("2011-08-05", 5.75), ("2012-12-19", 5.50), ("2013-04-17", 5.00), ("2013-05-17", 4.50),
      ("2014-01-29", 10.00), ("2014-05-23", 9.50), ("2014-06-25", 8.75), ("2014-07-18", 8.25), ("2015-01-21", 7.75), ("2015-02-25", 7.50), ("2016-11-25", 8.00),
      ("2018-06-01", 16.50), ("2018-06-08", 17.75), ("2018-09-14", 24.00), ("2019-07-26", 19.75), ("2019-09-13", 16.50), ("2019-10-25", 14.00), ("2019-12-13", 12.00),
      ("2020-01-17", 11.25), ("2020-02-20", 10.75), ("2020-03-18", 9.75), ("2020-04-23", 8.75), ("2020-05-22", 8.25), ("2020-09-25", 10.25), ("2020-11-20", 15.00),
      ("2020-12-25", 17.00), ("2021-03-19", 19.00), ("2021-09-24", 18.00), ("2021-10-22", 16.00), ("2021-11-19", 15.00), ("2021-12-17", 14.00), ("2022-08-19", 13.00),
      ("2022-09-23", 12.00), ("2022-10-21", 10.50), ("2022-11-25", 9.00), ("2023-02-24", 8.50), ("2023-06-23", 15.00), ("2023-07-21", 17.50), ("2023-08-25", 25.00),
      ("2023-09-22", 30.00), ("2023-10-27", 35.00), ("2023-11-24", 40.00), ("2023-12-22", 42.50), ("2024-01-26", 45.00), ("2024-03-22", 50.00), ("2024-12-27", 47.50),
      ("2025-01-24", 45.00), ("2025-03-07", 42.50), ("2025-04-18", 46.00), ("2025-07-25", 43.00), ("2025-09-12", 40.50), ("2025-10-24", 39.50), ("2025-12-12", 38.00),
      ("2026-01-23", 37.00), ("2026-10-23", 36.00)]
PF = pd.DataFrame(PF, columns=["yururluk", "faiz"]); PF["yururluk"] = pd.to_datetime(PF.yururluk)
PF["karar"] = [TK[TK.searchsorted(d) - 1] for d in PF.yururluk]
PF.loc[PF.yururluk == "2014-01-29", "karar"] = pd.Timestamp("2014-01-28")
PF["d"] = PF.faiz.diff()
PPK = pd.read_csv(O.MY + "/tcmb/ppk_tarihleri.csv", parse_dates=["karar"]).karar
ACIL = {pd.Timestamp("2014-01-28"), pd.Timestamp("2011-08-04"), pd.Timestamp("2018-05-23")}   # aksam/olaganustu: giris ertesi gun
def giris(d):
    d = pd.Timestamp(d); i = TK.searchsorted(d)
    if i >= len(TK): return None
    if TK[i] != d or d in ACIL: return TK[min(i + (1 if TK[i] == d else 0), len(TK) - 1)]
    return TK[i]
H = (21, 42, 63)
def ileri(col, t0, h):
    i = P.index.get_loc(t0)
    return P[col].iloc[i + h] / P[col].iloc[i] - 1 if i + h < len(P) else np.nan
def gun0(col, t0, onceki):
    i = P.index.get_loc(t0); j = P.index.get_loc(onceki)
    return P[col].iloc[i] / P[col].iloc[j] - 1
# --- PPK kararlarinin siniflandirmasi
rows = []
prev_dir = 0
for d in PPK:
    m = PF[PF.karar == d]
    dlt = float(m.d.iloc[0]) if len(m) and pd.notna(m.d.iloc[0]) else 0.0
    if d < pd.Timestamp("2010-05-18"): dlt = 0.0
    t0 = giris(d)
    if t0 is None: continue
    onc = TK[TK.searchsorted(d) - 1]
    r = {"karar": d, "t0": t0, "dfaiz": dlt, "yon": np.sign(dlt), "donus": bool(dlt != 0 and prev_dir != 0 and np.sign(dlt) != prev_dir)}
    if dlt != 0: prev_dir = np.sign(dlt)
    r["dy2_gun0"] = (P.y2.loc[t0] - P.y2.loc[onc]) if pd.notna(P.y2.get(t0)) and pd.notna(P.y2.get(onc)) else np.nan
    for c in ["BANK_REL", "IHR_YUR", "XU100"]:
        r[f"{c}_g0"] = gun0(c, t0, onc)
        for h in H: r[f"{c}_{h}"] = ileri(c, t0, h)
    i0 = P.index.get_loc(onc); r["BANK_REL_on63"] = P.BANK_REL.iloc[i0] / P.BANK_REL.iloc[i0 - 63] - 1 if i0 >= 63 else np.nan
    rows.append(r)
K = pd.DataFrame(rows)
# fiili donusler
FIILI = [("2025-03-20", 1, "O/N borc verme %46 (ara PPK), politika faizi sabit"), ("2026-03-02", 1, "1 Mart 2026 (Pazar) repo ihalelerine ara: AOFM %37->%40"),
         ("2026-08-24", -1, "23 Agustos 2026 (Pazar) repo ihaleleri yeniden: AOFM %40->%37")]
fr = []
for d, yon, ac in FIILI:
    t0 = pd.Timestamp(d); onc = TK[TK.searchsorted(t0) - 1]
    r = {"karar": t0, "t0": t0, "dfaiz": np.nan, "yon": yon, "donus": True, "fiili": ac, "dy2_gun0": P.y2.loc[t0] - P.y2.loc[onc]}
    for c in ["BANK_REL", "IHR_YUR", "XU100"]:
        r[f"{c}_g0"] = gun0(c, t0, onc)
        for h in H: r[f"{c}_{h}"] = ileri(c, t0, h)
    fr.append(r)
FK = pd.DataFrame(fr)
# AOFM algoritmik donusler
a5 = P.aofm.rolling(5).mean().dropna(); st = 0; ext = a5.iloc[0]; alg = []
for t, v in a5.items():
    if st >= 0:  # yukari ya da baslangic: tepe izle, dususe bak
        if v > ext and st == 1: ext = v
        if st == 0: ext = v; st = 1 if False else st
    if st == 0:
        lo = a5.loc[:t].min(); hi = a5.loc[:t].max()
        if v >= lo + 1.5: st, ext = 1, v; alg.append((t, 1))
        elif v <= hi - 1.5: st, ext = -1, v; alg.append((t, -1))
        continue
    if st == 1:
        ext = max(ext, v)
        if v <= ext - 1.5: st, ext = -1, v; alg.append((t, -1))
    else:
        ext = min(ext, v)
        if v >= ext + 1.5: st, ext = 1, v; alg.append((t, 1))
AR = []
for t, yon in alg:
    i = P.index.get_loc(t); t0 = P.index[min(i + 1, len(P) - 1)]   # AOFM ertesi sabah bilinir -> t+1 kapanis
    r = {"karar": t, "t0": t0, "yon": yon, "aofm": P.aofm.loc[t]}
    for c in ["BANK_REL", "IHR_YUR", "XU100"]:
        for h in H: r[f"{c}_{h}"] = ileri(c, t0, h)
    AR.append(r)
AR = pd.DataFrame(AR)
# placebo: tum gunler
def plac(col, h):
    v = P[col].values; x = v[h:] / v[:-h] - 1; x = x[np.isfinite(x)]; return x
def boot_p(vals, col, h, nrep=20000):
    x = plac(col, h); m = np.nanmean(vals); n = np.isfinite(vals).sum()
    if n == 0: return np.nan
    sims = rng.choice(x, size=(nrep, n)).mean(axis=1)
    return float((np.abs(sims - x.mean()) >= abs(m - x.mean())).mean())
out = []
def tab(D, baslik):
    rr = []
    for c in ["BANK_REL", "IHR_YUR"]:
        for h in H:
            v = D[f"{c}_{h}"].values.astype(float)
            rr.append({"seri": c, "h": h, "n": int(np.isfinite(v).sum()), "ort%": 100 * np.nanmean(v), "medyan%": 100 * np.nanmedian(v),
                       "isabet%": 100 * np.nanmean(v[np.isfinite(v)] > 0) if np.isfinite(v).any() else np.nan,
                       "placebo_ort%": 100 * plac(c, h).mean(), "placebo_ss%": 100 * plac(c, h).std(), "boot_p": boot_p(v, c, h)})
    out.append(f"\n#### {baslik}\n\n" + O.md(pd.DataFrame(rr).set_index(["seri", "h"]).round(3)))
def liste(D, baslik, extra=()):
    cols = ["karar", "t0", "dfaiz", "dy2_gun0", "BANK_REL_g0", "BANK_REL_21", "BANK_REL_42", "BANK_REL_63", "IHR_YUR_21", "IHR_YUR_63", "XU100_63"] + list(extra)
    cols = [c for c in cols if c in D.columns]; L = D[cols].copy()
    for c in L.columns:
        if c.startswith(("BANK", "IHR", "XU100")): L[c] = (100 * L[c]).round(1)
    if "dy2_gun0" in L: L["dy2_gun0"] = (100 * L.dy2_gun0).round(0)
    L["karar"] = L.karar.dt.date; L["t0"] = L.t0.dt.date
    out.append(f"\n{baslik} (getiriler %, dy2_gun0 bp)\n\n" + O.md(L.set_index("karar")))
D = K[K.donus]
liste(D[D.yon < 0], "Politika faizi DONUS: ilk INDIRIM (artirimlardan sonra)"); tab(D[D.yon < 0], "Ilk indirim donusleri — ozet")
liste(D[D.yon > 0], "Politika faizi DONUS: ilk ARTIRIM (indirimlerden sonra)"); tab(D[D.yon > 0], "Ilk artirim donusleri — ozet")
liste(FK, "Fiili (fonlama) donusler", ["fiili"])
cut_all = pd.concat([D[D.yon < 0], FK[FK.yon < 0]]); hike_all = pd.concat([D[D.yon > 0], FK[FK.yon > 0]])
tab(cut_all, "Gevseme donusleri (politika + fiili) — ozet"); tab(hike_all, "Sikilasma donusleri (politika + fiili) — ozet")
# AOFM algoritmik
ARl = AR.copy(); ARl["karar"] = ARl.karar.dt.date; ARl["t0"] = ARl.t0.dt.date
for c in [c for c in ARl.columns if c.startswith(("BANK", "IHR", "XU100"))]: ARl[c] = (100 * ARl[c]).round(1)
out.append("\nAOFM algoritmik donusler (5g ort AOFM, son uc noktadan >=150bp; giris t+1)\n\n" + O.md(ARl.set_index("karar")[["t0", "yon", "aofm", "BANK_REL_21", "BANK_REL_42", "BANK_REL_63", "IHR_YUR_63"]]))
tab(AR[AR.yon < 0], "AOFM gevseme donusleri — ozet"); tab(AR[AR.yon > 0], "AOFM sikilasma donusleri — ozet")
# tum PPK: yon bazinda (devam eden indirim/artirim/sabit)
for nm, m in [("Tum indirimler", K.yon < 0), ("Tum artirimlar", K.yon > 0), ("Sabit", K.yon == 0)]:
    tab(K[m], f"{nm} (n={int(m.sum())})")
# surprizler: piyasa bazli
Ks = K.dropna(subset=["dy2_gun0"]).copy()
q10, q90 = Ks.dy2_gun0.quantile([.1, .9])
liste(Ks[Ks.dy2_gun0 >= q90].sort_values("dy2_gun0", ascending=False), f"SAHIN surpriz (PPK gunu 2Y degisimi >= {100*q90:.0f}bp, en ust %10)")
tab(Ks[Ks.dy2_gun0 >= q90], "Sahin surpriz — ozet")
liste(Ks[Ks.dy2_gun0 <= q10].sort_values("dy2_gun0"), f"GUVERCIN surpriz (PPK gunu 2Y degisimi <= {100*q10:.0f}bp, en alt %10)")
tab(Ks[Ks.dy2_gun0 <= q10], "Guvercin surpriz — ozet")
# surpriz olcusu ile banka tepkisi: regresyon
d = Ks[["dy2_gun0", "BANK_REL_g0", "BANK_REL_21", "BANK_REL_63"]].dropna()
for y in ["BANK_REL_g0", "BANK_REL_21", "BANK_REL_63"]:
    m = sm.OLS(d[y] * 100, sm.add_constant(d.dy2_gun0 * 100)).fit(cov_type="HC1")
    out.append(f"PPK gunu: {y} (%) = a + b * dy2 (puan): b = {m.params.iloc[1]:.2f}, t = {m.tvalues.iloc[1]:.2f}, n = {len(d)}")
# dongu (cycle) duzeyi: ardisik ayni yonlu kararlar bir dongu; her dongude kararlarin ortalamasi -> donguler arasi t
Kc = K[K.yon != 0].copy(); Kc["dongu"] = (Kc.yon != Kc.yon.shift()).cumsum()
rr = []
for yon, nm in [(-1, "indirim donguleri"), (1, "artirim donguleri")]:
    g = Kc[Kc.yon == yon].groupby("dongu").agg(bas=("karar", "min"), son=("karar", "max"), n=("karar", "size"), on63=("BANK_REL_on63", "mean"),
                                                 b21=("BANK_REL_21", "mean"), b63=("BANK_REL_63", "mean"), i63=("IHR_YUR_63", "mean"))
    L = g.copy(); L["bas"] = L.bas.dt.date; L["son"] = L.son.dt.date
    for c in ["on63", "b21", "b63", "i63"]: L[c] = (100 * L[c]).round(1)
    out.append(f"\n{nm}: dongu basina karar-ortalamasi (BANK_REL on63 = karar oncesi 63g, b21/b63 = sonrasi, i63 = IHR/YUR 63g; %)\n\n" + O.md(L.reset_index(drop=True)))
    x = g.b63.dropna(); out.append(f"{nm}: dongu sayisi {len(x)}, b63 ort {100*x.mean():.2f}%, medyan {100*x.median():.2f}%, dongu-arasi t {x.mean()/(x.std(ddof=1)/np.sqrt(len(x))):.2f}, pozitif dongu {int((x>0).sum())}/{len(x)}; karar oncesi 63g ort {100*g.on63.mean():.2f}%")
# beklenen devam kararlari (ilk karar degil, |dy2_gun0| < 25bp): Aralik 2026'ya en yakin analog
for yon, nm in [(-1, "devam eden INDIRIM, surprizsiz (|dy2|<25bp, donus degil)"), (1, "devam eden ARTIRIM, surprizsiz")]:
    m = (K.yon == yon) & (~K.donus) & (K.dy2_gun0.abs() < 0.25)
    tab(K[m], f"{nm} (n={int(m.sum())})")
# --- 2Y oncu sinyal
S = pd.DataFrame(index=P.index)
S["y2l"] = P.y2.shift(1)                      # t-1 degeri: TCMB gosterge degeri gun sonu yayinlanir
S["dy20"] = S.y2l - S.y2l.shift(20); S["dy60"] = S.y2l - S.y2l.shift(60)
S["spread"] = S.y2l - P.aofm.shift(1)
for h in H:
    S[f"f{h}"] = P.BANK_REL.shift(-h) / P.BANK_REL - 1; S[f"fi{h}"] = P.IHR_YUR.shift(-h) / P.IHR_YUR - 1
S["gecmis20"] = P.BANK_REL / P.BANK_REL.shift(20) - 1
S["esz20"] = P.BANK_REL / P.BANK_REL.shift(20) - 1   # ayni pencere (eszamanli)
def nwreg(y, X, lag):
    d = pd.concat([y, X], axis=1).dropna()
    m = sm.OLS(d.iloc[:, 0], sm.add_constant(d.iloc[:, 1:])).fit(cov_type="HAC", cov_kwds={"maxlags": lag}); return m, len(d)
rr = []
for per, a, b in [("2010-2026", "2010-01-01", "2026-12-31"), ("2010-2017", "2010-01-01", "2017-12-31"), ("2018-2022", "2018-01-01", "2022-12-31"), ("2023-2026", "2023-01-01", "2026-12-31"), ("2024-2026", "2024-01-01", "2026-12-31")]:
    s = S.loc[a:b]
    for sig in ["dy20", "dy60", "spread"]:
        row = {"donem": per, "sinyal": sig}
        for h in H:
            m, n = nwreg(s[f"f{h}"] * 100, s[[sig]], h); row[f"b_h{h}"] = m.params.iloc[1]; row[f"t_h{h}"] = m.tvalues.iloc[1]
        m2, _ = nwreg(s["f63"] * 100, s[[sig, "gecmis20"]], 63); row["t_h63_kontrollu(gecmis20)"] = m2.tvalues.iloc[1]
        row["n"] = n; rr.append(row)
out.append("\n#### 2Y getiri -> ileri XBANK/XU100 (%; b = sinyalin 1 puani basina ileri goreli getiri; NW t)\n\n" + O.md(pd.DataFrame(rr).set_index(["donem", "sinyal"]).round(2)))
# ortusmesiz kontrol: her 63 gunde bir ornek (h63) ve her 21 gunde bir (h21)
rr = []
for per, a in [("2010-2026", "2010"), ("2018-2026", "2018"), ("2023-2026", "2023")]:
    for h, step in [(21, 21), (63, 63)]:
        for off in [0, step // 3, 2 * step // 3]:
            s_ = S.loc[a:].iloc[off::step]
            d = s_[["dy60", f"f{h}"]].dropna()
            m = sm.OLS(d[f"f{h}"] * 100, sm.add_constant(d.dy60)).fit(cov_type="HC1")
            rr.append({"donem": per, "h": h, "kaydirma": off, "n": len(d), "b": m.params.iloc[1], "t": m.tvalues.iloc[1]})
out.append("\n#### Ortusmesiz orneklem: ileri XBANK/XU100 ~ dy60 (her h gunde bir gozlem; 3 farkli baslangic kaydirmasi)\n\n" + O.md(pd.DataFrame(rr).set_index(["donem", "h", "kaydirma"]).round(2)))
# basit kural: her 21 gunde bir, dy60 > +100bp ise 21 gun banka-uzun/XU100-kisa; dy60 < -100bp ise ters; aksi halde yok
rr = []
for per, a in [("2010-2026", "2010"), ("2018-2026", "2018"), ("2023-2026", "2023")]:
    for off in [0, 7, 14]:
        s_ = S.loc[a:].iloc[off::21].dropna(subset=["dy60", "f21"])
        pos = np.where(s_.dy60 > 1, 1, np.where(s_.dy60 < -1, -1, 0)); ret = pos * s_.f21 - np.abs(pos) * 0.0030
        act = pos != 0
        rr.append({"donem": per, "kaydirma": off, "ay": len(s_), "aktif_ay": int(act.sum()), "ort_aktif%": 100 * ret[act].mean(), "isabet%": 100 * (ret[act] > 0).mean(),
                   "yillik_toplam%": 100 * ret.sum() / (len(s_) / 12), "t": ret[act].mean() / (ret[act].std(ddof=1) / np.sqrt(act.sum()))})
out.append("\n#### Kural (aylik, ortusmesiz): dy60>+100bp -> 21g XBANK uzun/XU100 kisa, dy60<-100bp -> ters; 30bp maliyet\n\n" + O.md(pd.DataFrame(rr).set_index(["donem", "kaydirma"]).round(2)))
last = S.dropna(subset=["dy20"]).iloc[-1]
out.append(f"\nSon sinyal ({S.dropna(subset=['dy20']).index[-1].date()}): y2(t-1) = {last.y2l:.2f}, dy20 = {100*last.dy20:.0f}bp, dy60 = {100*last.dy60:.0f}bp, 2Y-AOFM = {100*last.spread:.0f}bp")
# eszamanli iliski
c = S[["dy20", "esz20"]].dropna(); e = (P.y2 - P.y2.shift(20)).reindex(c.index)
out.append(f"\nEszamanli: 20g Delta2Y ile ayni 20g XBANK/XU100 korelasyonu = {e.corr(P.BANK_REL.pct_change(20).reindex(c.index)):.2f}; gecikmeli (t-1 sinyal, ileri 21g) = {S[['dy20','f21']].dropna().corr().iloc[0,1]:.2f}")
# tercile
rr = []
for per, a in [("2010-2026", "2010"), ("2023-2026", "2023")]:
    s = S.loc[a:].dropna(subset=["dy20", "f21", "f63"])
    q = pd.qcut(s.dy20, 3, labels=["dusen 2Y", "orta", "yukselen 2Y"])
    for k, g in s.groupby(q, observed=True):
        rr.append({"donem": per, "dy20_uclu": k, "n_gun": len(g), "dy20_ort_bp": 100 * g.dy20.mean(), "XBANK_rel_21%": 100 * g.f21.mean(), "XBANK_rel_63%": 100 * g.f63.mean(),
                   "isabet63%": 100 * (g.f63 > 0).mean(), "IHR_YUR_63%": 100 * g.fi63.mean()})
out.append("\n#### 2Y 20g degisim ucluleri -> ileri goreli getiri (ortusen gunluk gozlemler; t icin yukaridaki NW tablosu)\n\n" + O.md(pd.DataFrame(rr).set_index(["donem", "dy20_uclu"]).round(2)))
# guncel durum
G = pd.DataFrame({"y2": P.y2, "aofm": P.aofm, "XBANK/XU100": P.BANK_REL, "IHR/YUR": P.IHR_YUR}).dropna().iloc[[-130, -65, -42, -21, -10, -5, -1]]
G["XBANK/XU100"] = G["XBANK/XU100"] / G["XBANK/XU100"].iloc[-1] * 100; G["IHR/YUR"] = G["IHR/YUR"] / G["IHR/YUR"].iloc[-1] * 100
out.append("\n#### Guncel (son gun = 100)\n\n" + O.md(G.round(2)))
out.append(f"\nSepet uye sayisi (son gun): ihracatci {int(nih.iloc[-1])}/{len(IHR)}, yurt ici {int(nyu.iloc[-1])}/{len(YUR)}; 2010 basi: {int(nih.loc['2010-01-04'])}, {int(nyu.loc['2010-01-04'])}")
K.to_pickle(O.MY + "/C_ppk.pkl"); S.to_pickle(O.MY + "/C_sinyal.pkl"); AR.to_pickle(O.MY + "/C_aofm_donus.pkl")
open(O.OUTD + "/C_tablolar.md", "w").write("\n".join(out)); print("\n".join(out))
