"""A3: Veri güdümlü tarama. 5 hisse x panel_ret_bistcal'daki TÜM semboller (+ek indirilenler).
Testler (2014-01-01+): (1) senkron kısmi korelasyon | XU100, (2) d_{t-1} -> gap_t, (3) d_{t-1} -> intra_t,
(4) d_{t-1} -> intra artığı (XU100 intra'ya göre; hisseye özgü işlenebilir öncülük). Newey-West(5) t, BH-FDR q=0.05 (aile bazında ve tümü).
IS (2014-2020) / OOS (2021-2026) korelasyonları da yazılır. Çıktı: a3_scan.csv"""
from common import *
import glob
def nw_t_fast(x, y, L=5):
    m = ~(np.isnan(x) | np.isnan(y)); x = x[m]; y = y[m]; n = len(x)
    if n < 250: return np.nan, np.nan, n
    x = (x - x.mean()) / x.std(); y = (y - y.mean()) / y.std()
    b = (x * y).sum() / (x * x).sum(); u = y - b * x; g = x * u
    S = (g * g).sum()
    for l in range(1, L + 1):
        w = 1 - l / (L + 1); S += 2 * w * (g[l:] * g[:-l]).sum()
    se = np.sqrt(S) / (x * x).sum()
    return float(np.corrcoef(x, y)[0, 1]), float(b / se), n
P = panel().copy()
P = P[P.index >= START]
# ek semboller (panelde olmayan, bu ajanın indirdikleri)
for s in ["MAD=X", "PKR=X", "UZS=X", "IQD=X"]:
    if s not in P.columns:
        try: P[s] = win(ll.ret(s), START)
        except Exception as e: print("skip", s, e)
cat = pd.read_csv(SCR + "/data/catalog.csv").set_index("sym")
xu = P["XU100.IS"]; XD = DEC("XU100")
rows = []
for s in STOCKS:
    y = P[s + ".IS"]; dd = win(DEC(s), START)
    # artıklar
    ry, _ = resid(y, xu); ry = ry.reindex(P.index)
    ri, _ = resid(dd["intra"], XD["intra"]); ri = ri.reindex(P.index)
    gap = dd["gap"].reindex(P.index); intra = dd["intra"].reindex(P.index)
    isA = (P.index < SPLIT)
    for d in P.columns:
        if d in (s + ".IS", "XU100.IS"): continue
        b = P[d].copy()
        if not ll.is_bist(d): b[b == 0] = np.nan
        if b.notna().sum() < 500: continue
        rb, _ = resid(b, xu); rb = rb.reindex(P.index)
        o = {"stock": s, "driver": d, "group": cat["group"].get(d, "extra")}
        o["pc_sync"], o["t_sync"], o["n_sync"] = nw_t_fast(ry.values, rb.values)
        o["pc_IS"] = nw_t_fast(ry.values[isA], rb.values[isA])[0]; o["pc_OOS"] = nw_t_fast(ry.values[~isA], rb.values[~isA])[0]
        b1 = b.shift(1).values
        o["c_gap"], o["t_gap"], _ = nw_t_fast(gap.values, b1)
        o["c_intra"], o["t_intra"], o["n_intra"] = nw_t_fast(intra.values, b1)
        o["c_intra_IS"] = nw_t_fast(intra.values[isA], b1[isA])[0]; o["c_intra_OOS"] = nw_t_fast(intra.values[~isA], b1[~isA])[0]
        o["c_iresid"], o["t_iresid"], _ = nw_t_fast(ri.values, b1)
        o["c_iresid_IS"] = nw_t_fast(ri.values[isA], b1[isA])[0]; o["c_iresid_OOS"] = nw_t_fast(ri.values[~isA], b1[~isA])[0]
        rows.append(o)
    print(s, len(rows), flush=True)
df = pd.DataFrame(rows)
for fam in ["sync", "gap", "intra", "iresid"]:
    p = ll.t_to_p(df["t_" + fam].values)
    rej, padj = ll.fdr(p, 0.05); df["q_" + fam] = padj; df["fdr_" + fam] = rej
allp = np.concatenate([ll.t_to_p(df["t_" + f].values) for f in ["sync", "gap", "intra", "iresid"]])
rej, padj = ll.fdr(allp, 0.05); n = len(df)
for i, f in enumerate(["sync", "gap", "intra", "iresid"]): df["qall_" + f] = padj[i * n:(i + 1) * n]
df.to_csv(CODE + "/a3_scan.csv", index=False)
print("n tests per family:", n, " total:", 4 * n)
for f in ["sync", "gap", "intra", "iresid"]:
    print(f, "FDR(aile) geçen:", int(df["fdr_" + f].sum()), " FDR(tümü) geçen:", int((df["qall_" + f] < 0.05).sum()))
