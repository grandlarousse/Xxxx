"""04: Veri güdümlü tarama. ASELS/TCELL/TTKOM x panel_ret_bistcal.parquet'teki TÜM semboller (yeniden üretilmiş panel; FX düzeltilmiş).
Metrikler (2014-01-01+): sync corr, pc_sync (XU100 kontrollü), gap_l1 corr(gap_t, d_{t-1}), intra_l1 corr(intra_t, d_{t-1}) [işlenebilir],
intra_l0_pre (yalnızca BIST açılışından önce kapanan piyasalar: .KS .T .AX ^KS11 ^N225 ^AXJO -> lag0 zaten önceden bilinir).
NW t; BH-FDR (q=0.05) her (hisse, metrik) ailesi içinde. Sonra FDR'den geçen işlenebilir sinyaller için IS/OOS ve ES/TUR lag1 kontrolü."""
from sv import *
import statsmodels.api as sm
P = pd.read_parquet(SCR + "/data/panel_ret_bistcal.parquet"); P.index = pd.DatetimeIndex(P.index)
P = P[P.index >= "2014-01-01"]
cat = pd.read_csv(SCR + "/data/catalog.csv").set_index("sym")
m = P["XU100.IS"]
PRE = lambda s: s.endswith((".KS", ".T", ".AX")) or s in ("^KS11", "^N225", "^AXJO")
def nwt(y, x):
    z = pd.concat([y.rename("y"), x.rename("x")], axis=1).dropna()
    if len(z) < 500 or z.x.std() == 0: return np.nan, np.nan, len(z)
    zy = (z.y - z.y.mean()) / z.y.std(); zx = (z.x - z.x.mean()) / z.x.std()
    mm = sm.OLS(zy.values, sm.add_constant(zx.values)).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    return mm.params[1], mm.tvalues[1], len(z)
rows = []
for st in ["ASELS", "TCELL", "TTKOM"]:
    a = P[st + ".IS"]; dd = ll.decomp(st); dd = dd[dd.index >= "2014-01-01"]
    # stok kalıntısı (XU100'e göre)
    z = pd.concat([a.rename("a"), m.rename("m")], axis=1).dropna(); ba = np.polyfit(z.m, z.a, 1); ra = (a - ba[0] * m)
    for s in P.columns:
        if s in (st + ".IS",): continue
        d = P[s]
        if d.notna().sum() < 500 or (d == 0).mean() > 0.5: continue
        o = {"stock": st, "driver": s, "group": cat.group.get(s, "?"), "name": str(cat.name.get(s, ""))[:40]}
        o["c_sync"], o["t_sync"], o["n"] = nwt(a, d)
        # kısmi: sürücüyü de XU100'e göre arındır
        zz = pd.concat([d.rename("d"), m.rename("m")], axis=1).dropna()
        if len(zz) > 500 and s != "XU100.IS":
            bd = np.polyfit(zz.m, zz.d, 1); rd = d - bd[0] * m
            o["pc_sync"], o["t_pc"], _ = nwt(ra, rd)
        o["gap_l1"], o["t_gap_l1"], _ = nwt(dd["gap"], d.shift(1))
        o["intra_l1"], o["t_intra_l1"], _ = nwt(dd["intra"], d.shift(1))
        if PRE(s): o["intra_l0_pre"], o["t_intra_l0_pre"], _ = nwt(dd["intra"], d)
        rows.append(o)
S = pd.DataFrame(rows)
ntest = 0
for st in S.stock.unique():
    for met in ["sync", "pc", "gap_l1", "intra_l1", "intra_l0_pre"]:
        idx = (S.stock == st) & S["t_" + met].notna()
        p = ll.t_to_p(S.loc[idx, "t_" + met].values); rej, padj = ll.fdr(p, 0.05)
        S.loc[idx, "fdr_" + met] = rej; S.loc[idx, "padj_" + met] = padj; ntest += idx.sum()
S.to_csv(RES + "/04_scan.csv", index=False)
print("toplam test:", ntest, " sürücü sayısı/hisse:", S.groupby("stock").size().to_dict())
for st in ["ASELS", "TCELL", "TTKOM"]:
    x = S[S.stock == st]
    print(f"\n=== {st}: FDR geçen sayısı:", {k: int(x['fdr_' + k].fillna(False).sum()) for k in ['sync', 'pc', 'gap_l1', 'intra_l1', 'intra_l0_pre']})
    nb = x[~x.driver.str.endswith(".IS")]
    print(" en yüksek |pc_sync| (BIST dışı):", nb.reindex(nb.pc_sync.abs().sort_values(ascending=False).index).head(12)[["driver", "group", "pc_sync", "t_pc"]].round(3).values.tolist())
    print(" en yüksek |pc_sync| (BIST içi):", x[x.driver.str.endswith(".IS")].reindex(x[x.driver.str.endswith(".IS")].pc_sync.abs().sort_values(ascending=False).index).head(6)[["driver", "pc_sync"]].round(3).values.tolist())
    y = x[x.fdr_intra_l1.fillna(False)].sort_values("t_intra_l1", key=abs, ascending=False)
    print(" intra_l1 FDR geçen:", y.head(15)[["driver", "group", "intra_l1", "t_intra_l1", "padj_intra_l1"]].round(4).values.tolist())
    y = x[x.fdr_intra_l0_pre.fillna(False)].sort_values("t_intra_l0_pre", key=abs, ascending=False)
    print(" intra_l0_pre FDR geçen:", y.head(10)[["driver", "intra_l0_pre", "t_intra_l0_pre"]].round(4).values.tolist())
    y = x.sort_values("t_gap_l1", key=abs, ascending=False)
    print(" en güçlü gap_l1:", y.head(8)[["driver", "gap_l1", "t_gap_l1"]].round(3).values.tolist())
