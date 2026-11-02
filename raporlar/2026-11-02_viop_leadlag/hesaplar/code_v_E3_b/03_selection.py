import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b")
"""03: Seçim yanlılığı / veri madenciliği.
(a) TÜM günlük semboller (n>=750, zero_frac<=0,25) için lag1 sinyal matrisi -> TUPRS y_h üzerinde YALNIZ IS (2014-2020) taraması: VLO/sepet IS'de kaçıncı?
(b) Yürüyen seçim: IS'de en iyi k sürücü -> OOS t (işaret IS'ye göre hizalı). 47 VİOP hissesinin her biri için aynı prosedür (meta-null).
(c) 9 ABD rafinerisinden tüm 4'lü sepetler (126) -> IS/OOS t dağılımı; seçilen sepetin yeri.
(d) Rastgele 4'lü ABD hisse sepetleri (katalogdaki NYSE/Nasdaq hisseleri, 5000 çekiliş) -> TUPRS y_h t dağılımı."""
import vb, numpy as np, pandas as pd, itertools, os
rng = np.random.default_rng(7)
cat = pd.read_csv(vb.D + "/catalog.csv")
cal = vb.bist_cal("2013-01-01")
ok = cat[(cat.zero_frac <= 0.25) & (cat.n >= 750)].sym.tolist() + ["CVI", "PARR", "CLMT", "VDE", "IXC"]
ok = [s for s in dict.fromkeys(ok) if os.path.exists(f"{vb.D}/daily/{s.replace('/', '_')}.parquet")]
VIOP = ["AEFES","AKBNK","AKSEN","ALARK","ARCLK","ASELS","ASTOR","BIMAS","BRSAN","CIMSA","DOAS","DOHOL","EKGYO","ENJSA","ENKAI","EREGL","FROTO","GARAN","GUBRF","HALKB","HEKTS","ISCTR","KCHOL","KRDMD","MGROS","ODAS","OYAKC","PETKM","PGSUS","SAHOL","SASA","SISE","SOKM","TAVHL","TCELL","THYAO","TKFEN","TOASO","TRALT","TRMET","TSKB","TTKOM","TUPRS","ULKER","VAKBN","VESTL","YKBNK"]
sig = {}
for s in ok:
    try:
        if s.endswith(".IS"):
            d = vb.bist_dec(s, cal); sig[s] = d.cc.shift(1)
        else:
            fld = "c" if ("=" in s or s.startswith("^")) else "adj"
            sig[s] = vb.sig(s, cal, "A", fld)
    except Exception as e:
        pass
M = pd.DataFrame(sig, index=cal)
M = M[M.index >= "2014-01-01"]
M = M.loc[:, M.notna().sum() >= 750]
print("sürücü sayısı:", M.shape[1])
xu = vb.bist_dec("XU100.IS", cal).intra
T = {}
for s in VIOP:
    d = vb.bist_dec(s + ".IS", cal); T[s] = (d.intra - xu)
T = pd.DataFrame(T).reindex(M.index)
F = pd.read_parquet(vb.RES + "/F.parquet").reindex(M.index)
M["USREF"] = F["A_USREF"]; M["OUTREF"] = F["A_OUT"]

def colcorr(y, X):
    Xv = X.values; yv = y.values[:, None]
    m = ~np.isnan(Xv) & ~np.isnan(yv)
    n = m.sum(0)
    Y = np.where(m, yv, np.nan); Z = np.where(m, Xv, np.nan)
    Ym = Y - np.nanmean(Y, 0); Zm = Z - np.nanmean(Z, 0)
    c = np.nansum(Ym * Zm, 0) / np.sqrt(np.nansum(Ym ** 2, 0) * np.nansum(Zm ** 2, 0))
    t = c * np.sqrt(n - 2) / np.sqrt(1 - c ** 2)
    return pd.Series(t, X.columns), pd.Series(n, X.columns)
isn = M.index < vb.SPLIT
res = {}
for s in VIOP:
    tI, nI = colcorr(T[s][isn], M[isn]); tO, nO = colcorr(T[s][~isn], M[~isn]); tA, nA = colcorr(T[s], M)
    res[s] = pd.DataFrame({"t_is": tI, "n_is": nI, "t_oos": tO, "n_oos": nO, "t_all": tA})
# (a) TUPRS
R = res["TUPRS"].copy(); R = R[(R.n_is >= 500) & (R.n_oos >= 500)]
R["rank_is_abs"] = R.t_is.abs().rank(ascending=False); R["rank_all_abs"] = R.t_all.abs().rank(ascending=False)
R = R.merge(cat[["sym", "group", "name"]].set_index("sym"), left_index=True, right_index=True, how="left")
R.to_csv(vb.RES + "/03_tuprs_scan.csv")
print("\nTUPRS y_h tarama: n sürücü =", len(R))
print("IS'de |t| sıralaması (1 = en iyi):"); print(R.loc[["VLO", "MPC", "PSX", "PBF", "DINO", "DK", "CRAK", "XLE", "USREF", "OUTREF", "BZ=F", "ES=F"], ["t_is", "rank_is_abs", "t_oos", "t_all", "rank_all_abs"]].round(2).to_string())
print("\nIS'de en iyi 25 (|t_is|):"); print(R.reindex(R.t_is.abs().sort_values(ascending=False).index).head(25)[["group", "t_is", "t_oos", "t_all"]].round(2).to_string())
# IS'de |t|>2 sayısı vs şans
print("IS'de |t|>2 oranı:", round((R.t_is.abs() > 2).mean(), 3), " |t|>3:", int((R.t_is.abs() > 3).sum()))
# (b) yürüyen seçim, meta-null
rows = []
for s in VIOP:
    r = res[s]; r = r[(r.n_is >= 500) & (r.n_oos >= 300)].drop(index=["USREF", "OUTREF"], errors="ignore")
    r = r.drop(index=[s + ".IS"], errors="ignore")
    o = list(r.t_is.abs().sort_values(ascending=False).index)
    if len(o) < 20: continue
    for k in (1, 5, 20):
        top = r.loc[o[:k]]
        al = (np.sign(top.t_is) * top.t_oos)
        rows.append(dict(stock=s, k=k, max_t_is=r.t_is.abs().max(), mean_aligned_t_oos=al.mean(), frac_oos_same_sign_sig=(al > 1.96).mean(), best=o[0]))
W = pd.DataFrame(rows); W.to_csv(vb.RES + "/03_walkforward.csv", index=False)
pd.set_option("display.width", 220)
w1 = W[W.k == 1].set_index("stock"); w20 = W[W.k == 20].set_index("stock")
print("\n(b) Her hisse için IS'de en iyi sürücü -> OOS t (IS işaretine hizalı):")
print(w1[["best", "max_t_is", "mean_aligned_t_oos"]].sort_values("mean_aligned_t_oos", ascending=False).round(2).head(15).to_string())
print("TUPRS k=1:", w1.loc["TUPRS", ["best", "max_t_is", "mean_aligned_t_oos"]].tolist(), " k=20 ort OOS t:", round(w20.loc["TUPRS", "mean_aligned_t_oos"], 2), " frac OOS t>1,96:", w20.loc["TUPRS", "frac_oos_same_sign_sig"])
print("47 hisse k=1 OOS t dağılımı: medyan", round(w1.mean_aligned_t_oos.median(), 2), " >1,96 olan:", int((w1.mean_aligned_t_oos > 1.96).sum()))
print("47 hisse k=20 ort OOS t dağılımı: medyan", round(w20.mean_aligned_t_oos.median(), 2), " TUPRS sırası:", int(w20.mean_aligned_t_oos.rank(ascending=False)["TUPRS"]))
print("k=20, OOS'ta t>1,96 tutan oran, ilk 10 hisse:"); print(w20.frac_oos_same_sign_sig.sort_values(ascending=False).head(10).to_string())
# (c) rafineri 4'lü alt kümeler
REF = ["VLO", "MPC", "PSX", "PBF", "DINO", "DK", "CVI", "PARR", "CLMT"]
SG = pd.DataFrame({r: F["A_" + r] if ("A_" + r) in F else M[r] for r in REF})
y = F["y_h"]
rows = []
for comb in itertools.combinations(REF, 4):
    b = SG[list(comb)].mean(axis=1)
    out = {"comb": "+".join(comb)}
    for pk, m in [("IS", b.index < vb.SPLIT), ("OOS", b.index >= vb.SPLIT), ("ALL", b.index >= "1900")]:
        _, t, n = vb.nw(y[m], b[m].rename("b")); out["t_" + pk] = t["b"]
    rows.append(out)
C = pd.DataFrame(rows).sort_values("t_IS", ascending=False).reset_index(drop=True); C.to_csv(vb.RES + "/03_ref_subsets.csv", index=False)
sel = C[C.comb == "VLO+MPC+PSX+PBF"]
print("\n(c) 126 rafineri 4'lüsü: IS t medyan", round(C.t_IS.median(), 2), "min", round(C.t_IS.min(), 2), "| OOS t medyan", round(C.t_OOS.median(), 2), "min", round(C.t_OOS.min(), 2))
print("Seçilen sepet IS sırası:", int(sel.index[0]) + 1, "/126", sel.round(2).to_dict("records"))
print("VLO içermeyen 4'lüler: IS t medyan", round(C[~C.comb.str.contains("VLO")].t_IS.median(), 2), " OOS medyan", round(C[~C.comb.str.contains("VLO")].t_OOS.median(), 2))
for r in REF:
    _, tI, _ = vb.nw(y[y.index < vb.SPLIT], SG[r][SG.index < vb.SPLIT].rename("b")); _, tO, _ = vb.nw(y[y.index >= vb.SPLIT], SG[r][SG.index >= vb.SPLIT].rename("b"))
    print(f"  {r:5s} IS t {tI['b']:.2f}  OOS t {tO['b']:.2f}  n_is {SG[r][SG.index < vb.SPLIT].notna().sum()}")
# (d) rastgele 4'lü ABD hisse sepeti
us = cat[cat.exch.isin(["NYSE", "NasdaqGS", "NasdaqGM"]) & (cat.type == "EQUITY")].sym
us = [u for u in us if u in M.columns and M[u].notna().sum() > 2800]
print("\n(d) ABD hisse havuzu:", len(us))
U = M[us].values; yv = y.values; isv = M.index < vb.SPLIT
def tfast(x, yy):
    mm = ~np.isnan(x) & ~np.isnan(yy); c = np.corrcoef(x[mm], yy[mm])[0, 1]; n = mm.sum(); return c * np.sqrt(n - 2) / np.sqrt(1 - c * c)
tI = []; tO = []; ener = []
oilset = set(cat[cat.group == "oil"].sym)
for i in range(5000):
    idx = rng.choice(len(us), 4, replace=False)
    b = np.nanmean(U[:, idx], axis=1)
    tI.append(tfast(b[isv], yv[isv])); tO.append(tfast(b[~isv], yv[~isv])); ener.append(sum(us[j] in oilset for j in idx))
tI = np.array(tI); tO = np.array(tO); ener = np.array(ener)
b0 = F["A_USREF"].values
t0I = tfast(b0[isv], yv[isv]); t0O = tfast(b0[~isv], yv[~isv])
print(f"USREF iid t: IS {t0I:.2f} OOS {t0O:.2f}")
print("Rastgele sepet IS t >= USREF oranı:", round((tI >= t0I).mean(), 4), " OOS:", round((tO >= t0O).mean(), 4), " her ikisi:", round(((tI >= t0I) & (tO >= t0O)).mean(), 4))
print("Enerji hissesi içermeyen sepetler: IS %95 üst", round(np.percentile(tI[ener == 0], 95), 2), " OOS %95 üst", round(np.percentile(tO[ener == 0], 95), 2), " max IS", round(tI[ener == 0].max(), 2))
print("IS t dağılımı: ort", round(tI.mean(), 2), "sd", round(tI.std(), 2), "| OOS ort", round(tO.mean(), 2), "sd", round(tO.std(), 2))
pd.DataFrame({"t_is": tI, "t_oos": tO, "n_energy": ener}).to_csv(vb.RES + "/03_random_baskets.csv", index=False)
