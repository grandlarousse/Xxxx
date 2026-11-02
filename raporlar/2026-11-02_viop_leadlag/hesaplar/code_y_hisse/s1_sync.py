"""Adım 1: Senkron yapı — 47 VİOP hissesinin XU100 artıkları: korelasyon matrisi, hiyerarşik kümeleme, PCA, zaman içinde istikrar.
Çıktı: res/resid_corr_full.csv, res/clusters.csv, res/pca.txt, res/cluster_stability.csv, res/cluster_year_corr.csv
"""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hdata
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from scipy.special import comb
def adjusted_rand_score(a, b):
    a = np.asarray(a); b = np.asarray(b)
    ct = pd.crosstab(a, b).values
    sij = comb(ct, 2).sum(); sa = comb(ct.sum(1), 2).sum(); sb = comb(ct.sum(0), 2).sum(); n2 = comb(len(a), 2)
    exp = sa * sb / n2; mx = 0.5 * (sa + sb)
    return (sij - exp) / (mx - exp) if mx != exp else 1.0
D = hdata.load(); cc = D["cc"]; TGT = hdata.VIOP
m = cc["XU100"]
LEAD = [c for c in cc.columns if c not in hdata.IDX]

def resid(df, mk, start=None, end=None):
    x = df.copy(); mm = mk.copy()
    if start: x = x[x.index >= pd.Timestamp(start)]; mm = mm[mm.index >= pd.Timestamp(start)]
    if end: x = x[x.index <= pd.Timestamp(end)]; mm = mm[mm.index <= pd.Timestamp(end)]
    out = {}
    for c in x:
        d = pd.concat([x[c], mm], axis=1).dropna()
        if len(d) < 120: out[c] = pd.Series(np.nan, index=x.index); continue
        b = np.cov(d.iloc[:, 0], d.iloc[:, 1])[0, 1] / d.iloc[:, 1].var()
        a = d.iloc[:, 0].mean() - b * d.iloc[:, 1].mean()
        out[c] = x[c] - a - b * mm
    return pd.DataFrame(out)

def clusters(Cm, thr=0.86, k=None):
    names = [c for c in Cm.index if Cm.loc[c].notna().sum() > 5]
    C = Cm.loc[names, names].fillna(0).values.copy(); np.fill_diagonal(C, 1)
    Dm = np.clip(1 - C, 0, 2); np.fill_diagonal(Dm, 0)
    Z = linkage(squareform(Dm, checks=False), "average")
    lab = fcluster(Z, k, "maxclust") if k else fcluster(Z, thr, "distance")
    return pd.Series(lab, index=names), Z

def name_clusters(lab, Cm):
    rows = []
    for g, mem in lab.groupby(lab):
        mm = list(mem.index)
        if len(mm) > 1:
            sub = Cm.loc[mm, mm].values; iu = np.triu_indices(len(mm), 1); avg = np.nanmean(sub[iu])
        else: avg = np.nan
        rows.append({"cl": g, "size": len(mm), "avg_resid_corr": round(avg, 3), "members": " ".join(mm)})
    return pd.DataFrame(rows).sort_values("size", ascending=False)

if __name__ == "__main__":
    out = []
    R = resid(cc[TGT], m)
    Cf = R.corr(min_periods=250)
    Cf.round(4).to_csv(os.path.join(hdata.RES, "resid_corr_full.csv"))
    # ham korelasyon da
    cc[TGT].corr(min_periods=250).round(4).to_csv(os.path.join(hdata.RES, "raw_corr_full.csv"))
    iu = np.triu_indices(len(TGT), 1)
    out.append(f"Ham getiri ort. ikili korelasyon: {np.nanmean(cc[TGT].corr(min_periods=250).values[iu]):.3f}; XU100 artığı ort.: {np.nanmean(Cf.values[iu]):.3f}")
    # en yüksek artık korelasyonlu 40 çift
    pr = []
    for a in range(len(TGT)):
        for b in range(a + 1, len(TGT)):
            pr.append((TGT[a], TGT[b], Cf.iloc[a, b]))
    pr = pd.DataFrame(pr, columns=["a", "b", "rc"]).sort_values("rc", ascending=False)
    pr.to_csv(os.path.join(hdata.RES, "resid_pairs.csv"), index=False)
    out.append("En yüksek 40 artık korelasyon:\n" + pr.head(40).round(3).to_string(index=False))
    out.append("En düşük 15:\n" + pr.tail(15).round(3).to_string(index=False))
    # kümeleme (tam dönem)
    for thr in [0.80, 0.86, 0.90]:
        lab, Z = clusters(Cf, thr)
        out.append(f"\nKümeler (ortalama bağlantı, 1-rho eşik {thr}): {lab.nunique()} küme\n" + name_clusters(lab, Cf).to_string(index=False))
    labF, ZF = clusters(Cf, 0.86)
    labF.rename("cl").to_csv(os.path.join(hdata.RES, "clusters_full.csv"))
    # IS-only kümeleme (backtest için look-ahead'siz)
    RI = resid(cc[TGT], m, end="2020-12-31"); CI = RI.corr(min_periods=250)
    labI, _ = clusters(CI, 0.86)
    labI.rename("cl").to_csv(os.path.join(hdata.RES, "clusters_is.csv"))
    out.append("\nIS (2014–2020) kümeleri (eşik 0,86):\n" + name_clusters(labI, CI).to_string(index=False))
    # pencere istikrarı
    W = [("2014-01-01", "2017-12-31"), ("2018-01-01", "2020-12-31"), ("2021-01-01", "2023-12-31"), ("2024-01-01", "2026-12-31")]
    Cw, Lw = {}, {}
    for s, e in W:
        Rw = resid(cc[TGT], m, s, e); Cw[s[:4]] = Rw.corr(min_periods=200); Lw[s[:4]], _ = clusters(Cw[s[:4]], 0.86)
    rows = []
    ks = list(Cw)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, b = ks[i], ks[j]
            com = [c for c in TGT if c in Lw[a].index and c in Lw[b].index]
            ua = Cw[a].loc[com, com].values[np.triu_indices(len(com), 1)]; ub = Cw[b].loc[com, com].values[np.triu_indices(len(com), 1)]
            ok = np.isfinite(ua) & np.isfinite(ub)
            rows.append({"w1": a, "w2": b, "n_stock": len(com), "ARI": adjusted_rand_score(Lw[a][com], Lw[b][com]),
                         "corr_of_corr": np.corrcoef(ua[ok], ub[ok])[0, 1], "mean_rc_w1": np.nanmean(ua), "mean_rc_w2": np.nanmean(ub)})
    st = pd.DataFrame(rows); st.to_csv(os.path.join(hdata.RES, "cluster_stability.csv"), index=False)
    out.append("\nPencere istikrarı (ARI = küme etiket uyumu; corr_of_corr = artık korelasyon matrislerinin üst üçgen korelasyonu):\n" + st.round(3).to_string(index=False))
    for k in ks:
        out.append(f"\nKümeler {k}:\n" + name_clusters(Lw[k], Cw[k]).to_string(index=False))
    # tam dönem kümelerinin yıllara göre ortalama küme-içi artık korelasyonu
    yrs = range(2014, 2027); yr_rows = []
    for g, mem in labF.groupby(labF):
        mm = list(mem.index)
        if len(mm) < 2: continue
        rr = {"cl": g, "members": " ".join(mm)}
        for y in yrs:
            Ry = resid(cc[mm], m, f"{y}-01-01", f"{y}-12-31"); Cy = Ry.corr(min_periods=100).values
            rr[y] = np.nanmean(Cy[np.triu_indices(len(mm), 1)])
        yr_rows.append(rr)
    yc = pd.DataFrame(yr_rows); yc.to_csv(os.path.join(hdata.RES, "cluster_year_corr.csv"), index=False)
    out.append("\nKüme-içi ort. artık korelasyon, yıllara göre:\n" + yc.round(2).to_string(index=False))
    # PCA (ortak örneklem: tüm 47 hisse, 2023-02+)
    Rc = resid(cc[TGT], m, "2023-02-01").dropna()
    Z = (Rc - Rc.mean()) / Rc.std()
    ev, evec = np.linalg.eigh(np.corrcoef(Z.values.T)); o = np.argsort(ev)[::-1]; ev = ev[o]; evec = evec[:, o]
    out.append(f"\nPCA (XU100 artıkları, 2023-02..2026-10, n={len(Rc)}, 47 hisse): ilk 8 özdeğer payı: " + ", ".join(f"{100*v/ev.sum():.1f}%" for v in ev[:8])
               + f"  (rastgele matris MP üst sınırı λ+≈{(1+np.sqrt(47/len(Rc)))**2:.2f}; özdeğerler: " + ", ".join(f"{v:.2f}" for v in ev[:8]) + ")")
    for k in range(6):
        l = pd.Series(evec[:, k], index=TGT)
        if l.abs().max() == -l.min(): l = -l
        l = l.sort_values()
        out.append(f"PC{k+1}: + " + ", ".join(f"{a}:{v:.2f}" for a, v in l[::-1].head(8).items()) + " | − " + ", ".join(f"{a}:{v:.2f}" for a, v in l.head(6).items()))
    # ham PCA (piyasa faktörü)
    Rr = cc[TGT].loc[Rc.index].dropna(); Zr = (Rr - Rr.mean()) / Rr.std()
    evr = np.sort(np.linalg.eigvalsh(np.corrcoef(Zr.values.T)))[::-1]
    out.append(f"Ham getiri PCA: PC1 payı {100*evr[0]/evr.sum():.1f}%, PC2 {100*evr[1]/evr.sum():.1f}%, PC3 {100*evr[2]/evr.sum():.1f}%")
    # PCA tam dönem (2018-06+, ASTOR/ISDMR hariç ortak örneklem)
    t2 = [c for c in TGT if c not in ("ASTOR",)]
    Rc2 = resid(cc[t2], m, "2018-06-01").dropna(); Z2 = (Rc2 - Rc2.mean()) / Rc2.std()
    ev2, evec2 = np.linalg.eigh(np.corrcoef(Z2.values.T)); o = np.argsort(ev2)[::-1]; ev2 = ev2[o]; evec2 = evec2[:, o]
    out.append(f"\nPCA (2018-06..2026-10, n={len(Rc2)}, 46 hisse, ASTOR hariç): ilk 6 pay " + ", ".join(f"{100*v/ev2.sum():.1f}%" for v in ev2[:6]))
    for k in range(5):
        l = pd.Series(evec2[:, k], index=t2)
        if l.abs().max() == -l.min(): l = -l
        l = l.sort_values()
        out.append(f"PC{k+1}: + " + ", ".join(f"{a}:{v:.2f}" for a, v in l[::-1].head(8).items()) + " | − " + ", ".join(f"{a}:{v:.2f}" for a, v in l.head(5).items()))
    # mekanik içerme sağlamlık: piyasa = eşit ağırlıklı 177 hisse (hedef hariç değil ama 1/177 ağırlık)
    ew = cc[LEAD].mean(axis=1)
    Re = resid(cc[TGT], ew); Ce = Re.corr(min_periods=250)
    labE, _ = clusters(Ce, 0.86)
    com = [c for c in labE.index if c in labF.index]
    out.append(f"\nSağlamlık: piyasa=EW(177) artıklarıyla kümeleme ARI vs XU100 artıkları = {adjusted_rand_score(labF[com], labE[com]):.3f}; "
               f"üst-üçgen korelasyon = {np.corrcoef(Cf.values[iu], Ce.values[iu])[0,1]:.3f}")
    # 47 hedefin 177 hisse içindeki en yakın senkron eşleri (artık korelasyonu) — öncülük testinde referans
    RA = resid(cc[LEAD], m); CA = RA.corr(min_periods=250)
    CA.round(4).to_parquet(os.path.join(hdata.RES, "resid_corr_all177.parquet"))
    nb = []
    for t in TGT:
        s = CA[t].drop(t).sort_values(ascending=False).head(5)
        nb.append(f"{t}: " + ", ".join(f"{a} {v:.2f}" for a, v in s.items()))
    out.append("\n47 hedefin 177 hisse içindeki en yüksek 5 artık-korelasyonlu eşi (tam dönem):\n" + "\n".join(nb))
    txt = "\n".join(out); open(os.path.join(hdata.RES, "sync.txt"), "w").write(txt); print(txt)
