"""(B) Yabanci (yurt disi yerlesik) haftalik net hisse alimi -> XU100 / XBANK ileri getirileri (TL ve USD), YAYIN GECIKMESI ile.
Veri: TCMB EVDS3 (c01_tcmb_veri.py). Arsiv TP.PYUK3 (2005-01..2020-09-04) + yeni TP.MKNETHAR.M7 (2020-09-11..). Stok: PYUK1 / M1.
Hafta w = Cuma biten hafta. Yayin: izleyen Persembe 14:30 (w+6 gun). Giris: yayin gunu KAPANIS (Persembe tatilse sonraki islem gunu).
Sinyaller (hepsi yayin aninda bilinen): akim/stok (bp), z52 = (F_w - ort_52)/ss_52 (onceki 52 hafta), 4 haftalik toplam z, seri (ardisik + / - hafta).
Testler: (1) ileri getiri regresyonu h = 1,2,4,8 hafta (Newey-West, lag=h), (2) z beslisi -> ileri getiri, (3) seri >=3/>=4 giris/cikis, (4) ters yon:
akim_w ~ getiri_{w}, getiri_{w-1}, getiri_{w-4..w-1} (takip mi ediyor?), (5) gecikmesiz (Cuma kapanisi) 'hileli' surum ile karsilastirma,
(6) alt donemler. Cikti: cikti/B_tablolar.md"""
import numpy as np, pandas as pd, statsmodels.api as sm
import ortak as O
T = O.MY + "/tcmb"
a = pd.read_parquet(T + "/akim_arsiv.parquet"); b = pd.read_parquet(T + "/akim_yeni.parquet")
a = a.rename(columns={"TP_PYUK3": "F", "TP_PYUK1": "STK", "TP_PYUK4": "FD"}).dropna(subset=["F"])
b = b.rename(columns={"TP_MKNETHAR_M7": "F", "TP_MKNETHAR_M1": "STK", "TP_MKNETHAR_M8": "FD"}).dropna(subset=["F"])
ov = a.join(b, lsuffix="_a", rsuffix="_b", how="inner")
uyum = (len(ov), ov[["F_a", "F_b"]].corr().iloc[0, 1], (ov.F_a - ov.F_b).abs().median(), ov[["STK_a", "STK_b"]].corr().iloc[0, 1])
W = pd.concat([a[a.index < b.index[0]], b]).sort_index()
W = W[~W.index.duplicated(keep="last")]
W["kaynak"] = np.where(W.index < b.index[0], "arsiv", "yeni")
W["Fs"] = W.F / W.STK.shift(1) * 1e4                       # bp of foreign equity stock
mu = W.F.shift(1).rolling(52, min_periods=40).mean(); sd = W.F.shift(1).rolling(52, min_periods=40).std()
W["z"] = (W.F - mu) / sd
F4 = W.F.rolling(4).sum(); W["z4"] = (F4 - F4.shift(1).rolling(52, min_periods=40).mean()) / F4.shift(1).rolling(52, min_periods=40).std()
sgn = np.sign(W.F); grp = (sgn != sgn.shift()).cumsum(); W["seri"] = sgn * sgn.groupby(grp).cumcount().add(1)
xu = O.endeks("XU100"); xb = O.endeks("XBANK"); fx = O.endeks("USDTRY")
TK = xu.index
P = pd.DataFrame({"XU100": xu, "XBANK": xb.reindex(TK), "USD": fx.reindex(TK).ffill()}).ffill()
P["XU100_USD"] = P.XU100 / P.USD; P["XBANK_USD"] = P.XBANK / P.USD; P["XBANK_REL"] = P.XBANK / P.XU100
def ilk_gun(d):
    i = TK.searchsorted(d); return TK[i] if i < len(TK) else None
W["fri"] = [ilk_gun(d) if d in TK else TK[TK.searchsorted(d) - 1] for d in W.index]   # haftanin son islem gunu (<= Cuma)
W["pub"] = [ilk_gun(d + pd.Timedelta(days=6)) for d in W.index]                         # Persembe (veya sonraki islem gunu)
W = W.dropna(subset=["pub"])
HW = {1: 5, 2: 10, 4: 20, 8: 40}
seriler = ["XU100", "XBANK", "XU100_USD", "XBANK_USD", "XBANK_REL"]
def fwd(col, start_dates, n):
    idx = P.index.get_indexer(start_dates); out = np.full(len(idx), np.nan); v = P[col].values
    for j, i in enumerate(idx):
        if i >= 0 and i + n < len(v): out[j] = v[i + n] / v[i] - 1
    return out
for s in seriler:
    for h, n in HW.items():
        W[f"{s}_h{h}"] = fwd(s, W.pub, n)
        W[f"{s}_h{h}_hile"] = fwd(s, W.fri, n)        # yayin gecikmesi yok sayilirsa (look-ahead)
    # haftalik eszamanli ve gecmis getiriler (Cuma-Cuma)
    v = P[s].reindex(W.fri.values).values
    W[f"{s}_w0"] = v / np.r_[np.nan, v[:-1]] - 1
    W[f"{s}_wm1"] = W[f"{s}_w0"].shift(1)
    W[f"{s}_wm4"] = pd.Series(v, index=W.index).pct_change(4).shift(1).values
    W[f"{s}_gap"] = fwd(s, W.fri, 0)  # placeholder
    # Cuma kapanisi -> Persembe kapanisi arasi (yayindan once kacirilan kisim)
    i0 = P.index.get_indexer(W.fri); i1 = P.index.get_indexer(W.pub); vv = P[s].values
    W[f"{s}_ara"] = [vv[j1] / vv[j0] - 1 if j0 >= 0 and j1 >= 0 else np.nan for j0, j1 in zip(i0, i1)]
W = W[W.index >= "2006-01-01"]
W.to_pickle(O.MY + "/B_haftalik.pkl")
out = [f"Arsiv-yeni ortusme: {uyum[0]} hafta, akim korelasyonu {uyum[1]:.3f}, medyan mutlak fark {uyum[2]:.1f} mn$, stok korelasyonu {uyum[3]:.3f}",
       f"Orneklem: {W.index[0].date()} - {W.index[-1].date()}, {len(W)} hafta; son yayin girisi {W.pub.iloc[-1].date()}"]
def nw(y, x, lag):
    d = pd.concat([pd.Series(y).rename("y"), pd.Series(x).rename("x")], axis=1).dropna()
    if len(d) < 30: return np.nan, np.nan, len(d)
    m = sm.OLS(d.iloc[:, 0], sm.add_constant(d.iloc[:, 1:])).fit(cov_type="HAC", cov_kwds={"maxlags": max(lag, 1)})
    return m.params.iloc[1], m.tvalues.iloc[1], len(d)
# (1) ileri getiri regresyonlari
for per, sub in [("2006-2026", W), ("2006-2014", W.loc[:"2014"]), ("2015-2020", W.loc["2015":"2020"]), ("2021-2026", W.loc["2021":]), ("2024-2026", W.loc["2024":])]:
    rr = []
    for sig in ["z", "z4", "Fs"]:
        for s in ["XU100", "XU100_USD", "XBANK", "XBANK_USD", "XBANK_REL"]:
            row = {"sinyal": sig, "seri": s}
            for h in HW:
                bcoef, t, n = nw(sub[f"{s}_h{h}"], sub[sig], h)
                row[f"b_h{h}"] = 100 * bcoef * (1 if sig != "Fs" else 10); row[f"t_h{h}"] = t
            rr.append(row)
    out.append(f"\n#### (1) Ileri getiri ~ sinyal, {per} (b: z icin 1 ss basina %, Fs icin 10bp basina %; t Newey-West)\n\n" + O.md(pd.DataFrame(rr).set_index(["sinyal", "seri"]).round(2)))
# (2) z beslisi
for s in ["XU100", "XU100_USD", "XBANK_REL"]:
    rr = []
    q = pd.qcut(W.z, 5, labels=[1, 2, 3, 4, 5])
    for k in [1, 2, 3, 4, 5]:
        g = W[q == k]; row = {"z_besli": k, "n": len(g), "z_ort": g.z.mean()}
        for h in HW: row[f"h{h}%"] = 100 * g[f"{s}_h{h}"].mean(); row[f"isabet_h{h}%"] = 100 * (g[f"{s}_h{h}"] > 0).mean()
        rr.append(row)
    row = {"z_besli": "hepsi", "n": len(W), "z_ort": W.z.mean()}
    for h in HW: row[f"h{h}%"] = 100 * W[f"{s}_h{h}"].mean(); row[f"isabet_h{h}%"] = 100 * (W[f"{s}_h{h}"] > 0).mean()
    rr.append(row)
    out.append(f"\n#### (2) z beslisine gore ileri {s} getirisi (giris = yayin Persembesi kapanisi)\n\n" + O.md(pd.DataFrame(rr).set_index("z_besli").round(2)))
# (3) seriler
rr = []
for nm, m in [("giris serisi >=3", W.seri >= 3), ("giris serisi >=4", W.seri >= 4), ("cikis serisi >=3", W.seri <= -3), ("cikis serisi >=4", W.seri <= -4),
              ("z >= +1.5", W.z >= 1.5), ("z <= -1.5", W.z <= -1.5), ("hepsi", W.z.notna())]:
    g = W[m]; row = {"kosul": nm, "n": len(g)}
    for s in ["XU100", "XU100_USD", "XBANK_REL"]:
        for h in (2, 4, 8):
            row[f"{s}_h{h}%"] = 100 * g[f"{s}_h{h}"].mean()
    # ortusmeyi azaltmak icin 8 haftalik bloklarda bagimsiz t: blok = yil-ceyrek
    if not m.all(): bcoef, t, n = nw(W["XU100_h4"].rename("y"), m.astype(float).rename("x"), 4); row["t_XU100_h4_fark"] = t
    rr.append(row)
out.append("\n#### (3) Ardisik giris/cikis serileri ve asiri z (ileri %, t = kosul kuklasinin NW t'si, h=4)\n\n" + O.md(pd.DataFrame(rr).set_index("kosul").round(2)))
# (4) ters yon: akim getiriyi mi takip ediyor?
rr = []
for per, sub in [("2006-2026", W), ("2021-2026", W.loc["2021":])]:
    for s in ["XU100", "XU100_USD"]:
        d = sub[["z", f"{s}_w0", f"{s}_wm1", f"{s}_wm4"]].dropna()
        m = sm.OLS(d.z, sm.add_constant(d[[f"{s}_w0", f"{s}_wm1", f"{s}_wm4"]] * 100)).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
        rr.append({"donem": per, "seri": s, "b_esz": m.params.iloc[1], "t_esz": m.tvalues.iloc[1], "b_w-1": m.params.iloc[2], "t_w-1": m.tvalues.iloc[2],
                   "b_w-4..-1": m.params.iloc[3], "t_w-4..-1": m.tvalues.iloc[3], "R2": m.rsquared, "kor(z,esz)": d.z.corr(d[f"{s}_w0"])})
out.append("\n#### (4) z_w ~ ayni hafta getirisi + gecmis getiriler (b: getirideki 1 puan basina z degisimi)\n\n" + O.md(pd.DataFrame(rr).set_index(["donem", "seri"]).round(3)))
# (5) gecikme etkisi: z'nin Cuma->Persembe arasi getiriyle iliskisi ve 'hileli' ileri getiri
rr = []
for s in ["XU100", "XU100_USD", "XBANK_REL"]:
    b1, t1, n1 = nw(W[f"{s}_ara"], W.z, 1)
    row = {"seri": s, "Cuma->Persembe b%": 100 * b1, "t": t1}
    for h in (1, 4):
        bb, tt, _ = nw(W[f"{s}_h{h}_hile"], W.z, h); row[f"hileli_h{h} b%"] = 100 * bb; row[f"hileli_h{h} t"] = tt
        bb, tt, _ = nw(W[f"{s}_h{h}"], W.z, h); row[f"durust_h{h} b%"] = 100 * bb; row[f"durust_h{h} t"] = tt
    rr.append(row)
out.append("\n#### (5) Yayin gecikmesinin etkisi (z 1 ss basina %)\n\n" + O.md(pd.DataFrame(rr).set_index("seri").round(2)))
# (6) basit kural: z4 > 0 iken XU100 (yoksa nakit=0), h=1 hafta yeniden dengeleme, ortusmesiz
rr = []
for per, sub in [("2006-2026", W), ("2021-2026", W.loc["2021":]), ("2024-2026", W.loc["2024":])]:
    for sig in ["z", "z4"]:
        for s in ["XU100", "XU100_USD"]:
            r = sub[f"{s}_h1"]; inn = sub[sig] > 0
            rr.append({"donem": per, "sinyal": sig, "seri": s, "hafta": int(r.notna().sum()), "piyasada%": 100 * inn.mean(),
                       "icerde_ort_haftalik%": 100 * r[inn].mean(), "disarida_ort_haftalik%": 100 * r[~inn].mean(),
                       "fark_t": nw(r, inn.astype(float), 1)[1]})
out.append("\n#### (6) Kural: sinyal > 0 haftalarinda endeks, degilse disarida (haftalik, ortusmesiz)\n\n" + O.md(pd.DataFrame(rr).set_index(["donem", "sinyal", "seri"]).round(3)))
# guncel durum
L = W.tail(10)[["F", "STK", "Fs", "z", "z4", "seri", "pub"]]
out.append("\n#### Son 10 hafta (F mn$, STK mn$, Fs bp, z, z4, seri, yayin gunu)\n\n" + O.md(L.round(2)))
open(O.OUTD + "/B_tablolar.md", "w").write("\n".join(out)); print("\n".join(out))
# (7) epizot duzeyi (ortusmesiz): seri ilk kez <=-4 (cikis) ya da >=+4 (giris) oldugu hafta; yayin Persembesi kapanisindan ileri getiri
rr = []; ep = []
for nm, cond in [("cikis serisi 4. hafta", W.seri == -4), ("cikis serisi 5. hafta", W.seri == -5), ("giris serisi 4. hafta", W.seri == 4), ("giris serisi 5. hafta", W.seri == 5)]:
    for per, sub in [("2006-2026", W), ("2015-2026", W.loc["2015":]), ("2021-2026", W.loc["2021":])]:
        g = sub[cond.reindex(sub.index)]
        row = {"kosul": nm, "donem": per, "epizot": len(g)}
        for s in ["XU100", "XU100_USD", "XBANK_REL"]:
            for h in (4, 8):
                x = g[f"{s}_h{h}"].dropna(); base = sub[f"{s}_h{h}"].dropna()
                row[f"{s}_h{h}%"] = 100 * x.mean(); row[f"{s}_h{h}_fark%"] = 100 * (x.mean() - base.mean())
                if s == "XU100" and h == 8: row["t_fark_h8"] = (x.mean() - base.mean()) / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan; row["isabet_h8%"] = 100 * (x > 0).mean()
        rr.append(row)
        if per == "2006-2026" and nm.startswith("cikis serisi 5"):
            ep = g[["F", "z4", "XU100_h4", "XU100_h8", "XU100_USD_h8", "XBANK_REL_h8"]].copy()
out.append("\n#### (7) Epizot duzeyi (ortusmesiz): serinin 4./5. haftasi yayinlandiginda ileri getiri; fark = kosulsuz ortalamadan fark\n\n" + O.md(pd.DataFrame(rr).set_index(["kosul", "donem"]).round(2)))
ep2 = ep.copy()
for c in ["XU100_h4", "XU100_h8", "XU100_USD_h8", "XBANK_REL_h8"]: ep2[c] = (100 * ep2[c]).round(1)
out.append("\n5 haftalik cikis serisi epizotlari (2006-2026)\n\n" + O.md(ep2.round(2)))
open(O.OUTD + "/B_tablolar.md", "w").write("\n".join(out)); print("\n".join(out[-2:]))
