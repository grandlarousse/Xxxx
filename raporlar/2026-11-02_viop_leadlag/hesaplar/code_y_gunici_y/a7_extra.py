"""Ek kontroller:
(a) 5 dk XU030->hisse lag-1: likit (ciro sırası ≤23) vs illikit; bayat-fiyat alt örneklemleri özet (pz/pnz, va/vl, oc/jump).
(b) Açılış penceresi (hedef slot 07:05..07:30) vs gün geri kalanı: havuzlanmış XU030_{t-1} -> hisse_t (std getiri), gün kümelenmiş.
(c) Gap fade giriş kayması: -sign(gap)*log(P_giriş/O) ortalaması (|gap|>1%): m5 (ilk 5 dk TP, 07:05, 15 dk VWAP) ve h1 (30 dk TP, 07:30).
(d) Gap fade E2 (h1) hisse bazında BH-FDR.
Çıktı: res/a7_*.csv"""
import numpy as np, pandas as pd, c_common as c
ll = c.ll; TG = c.VIOP
LQ = pd.read_csv(c.RES + "/a0_liq.csv").set_index("stock")
P = pd.read_csv(c.RES + "/a1_m5_pairs.csv"); f = P[(P.dir == "fwd") & (P.leader == "XU030")].set_index("target")
f["liq"] = np.where(LQ.reindex(f.index)["liq_rank"] <= 23, "likit23", "illikit24")
cols = ["corr0", "std_b1", "std_t1", "oc_b1", "jump_b1", "pz_b1", "pnz_b1", "va_b1", "vl_b1", "delay_share", "adj_min90"]
A = f.groupby("liq")[cols].median(); A["n_fdr"] = f.groupby("liq")["std_fdr"].sum(); A["n"] = f.groupby("liq").size()
A.to_csv(c.RES + "/a7_m5_liq_split.csv"); print(A.round(3).to_string())
from scipy.stats import spearmanr
sp = {v: spearmanr(LQ.reindex(f.index)[v], f["std_b1"])[0] for v in ["ret0_frac", "tick_bps", "turnover_mnTL", "sd5m_bps"]}
print("spearman(lag-1 katsayısı, x):", {k: round(v, 2) for k, v in sp.items()})
pd.Series(sp).to_csv(c.RES + "/a7_m5_spearman.csv")

# (b) açılış penceresi
R = {s: c.m5_ret(s) for s in TG + ["XU030"]}
def stdz(X):
    sd = np.nanstd(X, axis=0, keepdims=True); sd[sd == 0] = np.nan; return X / sd
RS = {s: stdz(R[s]) for s in R}
nd, nb = R["XU030"].shape; day_id = np.repeat(np.arange(nd), nb).reshape(nd, nb); slot = np.tile(np.arange(nb), (nd, 1))
xl = c.lagmat(np.nan_to_num(RS["XU030"]), 1); xl2 = c.lagmat(np.nan_to_num(RS["XU030"]), 2)
rows = []
for win, m in [("07:05-07:30", (slot >= 1) & (slot <= 6)), ("07:30-14:55", slot >= 7)]:
    for grp, mem in [("47", TG), ("likit23", [s for s in TG if LQ.loc[s, "liq_rank"] <= 23]), ("illikit24", [s for s in TG if LQ.loc[s, "liq_rank"] > 23])]:
        Y = []; X = []; G = []
        for s in mem:
            y = RS[s]; yl = c.lagmat(np.nan_to_num(y), 1)
            mm = m & ~np.isnan(y)
            Y.append(y[mm]); X.append(np.column_stack([xl[mm], xl2[mm], yl[mm]])); G.append(day_id[mm] * 100 + slot[mm])
        Y = np.concatenate(Y); X = np.vstack(X); G = np.concatenate(G)
        b, se, cov, r2, n = c.ols_cl(Y, X, G // 100)
        rows.append(dict(window=win, group=grp, b_xu030_lag1=b[1], t=b[1] / se[1], b_lag2=b[2], t2=b[2] / se[2], b_own1=b[3], n=n))
B = pd.DataFrame(rows); B.to_csv(c.RES + "/a7_open_window.csv", index=False); print(B.round(3).to_string())

# (c) giriş kayması
rows = []
for s in TG:
    Pm = c.m5_panel(s); days = Pm["days"]; dec = ll.decomp(s).reindex(days)
    O = Pm["dO"]; g = dec["gap"].values
    tp5 = (Pm["H"][:, 1] + Pm["L"][:, 1] + Pm["C"][:, 1]) / 3; c705 = Pm["C"][:, 1]
    tpm = (Pm["H"][:, 1:4] + Pm["L"][:, 1:4] + Pm["C"][:, 1:4]) / 3; vv = Pm["V"][:, 1:4]; vw15 = np.nansum(tpm * vv, 1) / np.nansum(vv, 1)
    for nm, px in [("m5_TP5", tp5), ("m5_0705", c705), ("m5_VWAP15", vw15), ("m5_close", Pm["dC"])]:
        v = -np.sign(g) * np.log(px / O); m = np.abs(g) > 0.01
        rows.append(dict(stock=s, src=nm, n=int(np.sum(m & ~np.isnan(v))), mean_bps=1e4 * np.nanmean(v[m]) if m.any() else np.nan))
    H = c.h1_panel(s); raw = ll.raw(ll.T(s), "h1"); raw = raw[~raw.index.duplicated(keep="last")]
    fb = raw[(raw.index.hour == 6) & (raw.index.minute == 30)].copy(); fb.index = pd.DatetimeIndex(fb.index.tz_convert(None).normalize())
    tp30 = ((fb["h"] + fb["l"] + fb["c"]) / 3).reindex(H.index)
    g = H["gap"]; m = (g.abs() > 0.01) & H["intra"].notna()
    for nm, px in [("h1_TP30", tp30), ("h1_0730", H["P0730"]), ("h1_close", H["C"])]:
        v = (-np.sign(g) * np.log(px / H["O"]))[m]
        rows.append(dict(stock=s, src=nm, n=int(v.notna().sum()), mean_bps=1e4 * v.mean()))
SL = pd.DataFrame(rows); SL.to_csv(c.RES + "/a7_entry_slippage.csv", index=False)
print(SL.groupby("src").agg(med=("mean_bps", "median"), mean=("mean_bps", "mean"), n=("n", "sum")).round(1).to_string())

# (d) E2 FDR
A2 = pd.read_csv(c.RES + "/a3_fade_h1.csv")
for (thr, en), g in A2.groupby(["thr", "entry"]):
    rej, padj = ll.fdr(ll.t_to_p(g["all_t"].values)); A2.loc[g.index, "fdr"] = rej; A2.loc[g.index, "padj"] = padj
A2.to_csv(c.RES + "/a7_fade_h1_fdr.csv", index=False)
print(A2[(A2.thr == "0.01")].groupby("entry")["fdr"].sum())
print(A2[(A2.thr == "0.01") & (A2.fdr == 1)][["stock", "entry", "all_n", "all_bps", "all_t", "is_bps", "oos_bps", "padj"]].round(2).to_string())
