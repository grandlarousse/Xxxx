"""A3: veri güdümlü tarama. 6 hisse x panel_ret_bistcal'deki tüm semboller (2014-01-01..2026-10-30).
Testler: sync_pc (XU100 cc kontrollü), gap_l1 (ham + XU100 gap kontrollü), intra_l1 (ham + XU100 intra kontrollü), rev_l1 (hisse_{t-1}->sürücü_t).
p: iid yaklaşık t; BH-FDR (q=0.05) TÜM testler üzerinde. Sağ kalanlar için NW-t, IS/OOS, yıllık işaret tutarlılığı.
Çıktı: res_scan_all.csv, res_scan_fdr.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kc import *
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__))
P = pd.read_parquet(SCR + "/data/panel_ret_bistcal.parquet")
CAT = pd.read_csv(SCR + "/data/catalog.csv").set_index("sym")
D = pd.read_parquet(SCR + "/data/panel_decomp_bist.parquet")
ST = "2014-01-01"
P = P[P.index >= ST]; D = D[D.index >= ST]
idx = D.index
P = P.reindex(idx)
XU = D["XU100"]

# sürücü filtresi
keep = []
for c in P.columns:
    if c in [s + ".IS" for s in STOCKS] or c in ("XU100.IS", "^XU100", "XUTUM.IS"): continue
    zf = CAT.zero_frac.get(c, 0); n = P[c].notna().sum()
    z_in = (P[c] == 0).mean()
    if n < 750 or z_in > 0.30: continue
    keep.append(c)
print("sürücü sayısı:", len(keep))


def pc_fast(y, x, c):
    m = ~(np.isnan(y) | np.isnan(x) | np.isnan(c))
    n = m.sum()
    if n < 250: return np.nan, n
    yy, xx, cc = y[m], x[m], c[m]
    C = np.column_stack([np.ones(n), cc])
    Q, _ = np.linalg.qr(C)
    ry = yy - Q @ (Q.T @ yy); rx = xx - Q @ (Q.T @ xx)
    return float(np.dot(ry, rx) / np.sqrt(np.dot(ry, ry) * np.dot(rx, rx))), n


def c_fast(y, x):
    m = ~(np.isnan(y) | np.isnan(x)); n = m.sum()
    if n < 250: return np.nan, n
    return float(np.corrcoef(y[m], x[m])[0, 1]), n


rows = []
for s in STOCKS:
    y_cc = D[(s, "cc")].values; y_gap = D[(s, "gap")].values; y_in = D[(s, "intra")].values
    x_cc = XU["cc"].values; x_gap = XU["gap"].values; x_in = XU["intra"].values
    y_ccl1 = D[(s, "cc")].shift(1).values
    for c in keep:
        d = P[c].values; dl = P[c].shift(1).values
        r1, n1 = pc_fast(y_cc, d, x_cc)
        r2, n2 = c_fast(y_gap, dl); r2p, _ = pc_fast(y_gap, dl, x_gap)
        r3, n3 = c_fast(y_in, dl); r3p, _ = pc_fast(y_in, dl, x_in)
        r4, n4 = c_fast(d, y_ccl1)
        for test, r, n in [("sync_pc", r1, n1), ("gap_l1", r2, n2), ("gap_l1_pc", r2p, n2), ("intra_l1", r3, n3), ("intra_l1_pc", r3p, n3), ("rev_l1", r4, n4)]:
            rows.append((s, c, CAT.group.get(c, "?"), test, r, n))
df = pd.DataFrame(rows, columns=["stock", "driver", "group", "test", "r", "n"]).dropna()
df["t"] = df.r * np.sqrt((df.n - 2) / (1 - df.r ** 2))
df["p"] = 2 * (1 - stats.norm.cdf(df.t.abs()))
rej, padj = ll.fdr(df.p.values, 0.05)
df["fdr_rej"] = rej; df["p_adj"] = padj
df.to_csv(os.path.join(HERE, "res_scan_all.csv"), index=False)
print("toplam test:", len(df), " FDR geçen:", int(rej.sum()))
print(df[df.fdr_rej].groupby(["stock", "test"]).size().unstack(fill_value=0))

# Sağ kalanların sağlamlık kontrolü
surv = df[df.fdr_rej].copy()
out = []
for _, r in surv.iterrows():
    s, c, test = r.stock, r.driver, r.test
    d = P[c]
    if test == "sync_pc":
        y, x, ctl = D[(s, "cc")], d, XU["cc"]
    elif test.startswith("gap"):
        y, x, ctl = D[(s, "gap")], d.shift(1), (XU["gap"] if test.endswith("pc") else None)
    elif test.startswith("intra"):
        y, x, ctl = D[(s, "intra")], d.shift(1), (XU["intra"] if test.endswith("pc") else None)
    else:
        y, x, ctl = d, D[(s, "cc")].shift(1), None
    if ctl is not None:
        ry = resid(y, [ctl]); rx = resid(x, [ctl]); dfp = pd.concat([ry.rename("a"), rx.rename("b")], axis=1).dropna()
    else:
        dfp = pd.concat([y.rename("a"), x.rename("b")], axis=1).dropna()
    t_nw = nwt_corr(dfp.a, dfp.b)
    cIS = dfp[dfp.index < SPLIT].corr().iloc[0, 1]; cOOS = dfp[dfp.index >= SPLIT].corr().iloc[0, 1]
    c3 = dfp[dfp.index >= "2023-10-30"].corr().iloc[0, 1]
    by = dfp.groupby(dfp.index.year).apply(lambda g: g.a.corr(g.b) if len(g) > 60 else np.nan).dropna()
    same = float((np.sign(by) == np.sign(r.r)).mean())
    out.append({**r.to_dict(), "t_nw": t_nw, "c_IS": cIS, "c_OOS": cOOS, "c_3y": c3, "yrs_same": same})
S = pd.DataFrame(out)
S["robust"] = (S.t_nw.abs() >= 3) & (np.sign(S.c_IS) == np.sign(S.c_OOS)) & (S.yrs_same >= 0.75)
S.to_csv(os.path.join(HERE, "res_scan_fdr.csv"), index=False)
print("FDR + sağlam (|t_nw|>=3, IS/OOS aynı işaret, yılların>=%75'i):", int(S.robust.sum()))
