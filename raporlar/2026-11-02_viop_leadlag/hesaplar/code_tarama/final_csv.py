"""out/f_tarama.csv üretimi (rest.py + fdr_null.py + asia_check.py sonrası).
Satır blokları: (A) aile özetleri: test sayısı, FDR geçen, null'da beklenen sahte; (B) SAĞLAM KÜME: pc_glob FDR q<0.05 + IS/OOS replike;
(C) pc_xt FDR q<0.05 + replike + |pc|>=0.08; (D) hisse başına ilk 5 (cache/top5); (E) öncülük: kova-içi FDR geçenler + Asya lag1 endeks bulgusu
+ IS-seçilmiş 10 backtest; (F) gap (işlenemez) endeks referansı; (G) rejim satırları."""
import os, sys, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tlib import *
P, DP = load_panels(); idx = P.index
M = pd.read_parquet(os.path.join(OUT, "tarama_matrix.parquet"))
dm = pd.read_parquet(os.path.join(CACHE, "driver_meta.parquet"))
dm["group"] = [regroup(s, g, n) for s, g, n in zip(dm.index, dm.group, dm.name)]
M["group"] = M.driver.map(dm.group)
M["mech"] = [mech(s, d, g) for s, d, g in zip(M.stock, M.driver, M.group)]
V = M[~M.is_index_row & ~M["sparse"]].copy()
FS = pd.read_csv(os.path.join(CACHE, "fdr_summary.csv")); NS = pd.read_csv(os.path.join(CACHE, "null_summary.csv"))

# yıllık işaret tutarlılığı (XU100+USDTRY artıkları üzerinde)
xt = np.column_stack([P["XU100.IS"].values, P["TRY=X"].values])
def year_share(pairs):
    out = {}
    stocks = sorted({s for s, _ in pairs}); drvs = sorted({d for _, d in pairs})
    RS = pd.DataFrame(resid(P[[s + ".IS" for s in stocks]].values, xt), index=idx, columns=stocks)
    RD = pd.DataFrame(resid(P[drvs].values, xt), index=idx, columns=drvs)
    for s, d in pairs:
        df = pd.concat([RS[s], RD[d]], axis=1).dropna()
        yc = df.groupby(df.index.year).apply(lambda x: x.iloc[:, 0].corr(x.iloc[:, 1]) if len(x) > 60 else np.nan).dropna()
        full = df.iloc[:, 0].corr(df.iloc[:, 1])
        out[(s, d)] = (float((np.sign(yc) == np.sign(full)).mean()) if len(yc) else np.nan, len(yc))
    return out

def conf(x, ys):
    plaus = not x.mech.startswith("BEKLENMEYEN")
    rep = (np.sign(x.pc_xt_is) == np.sign(x.pc_xt_oos)) and x.p_pc_xt_is < 0.05 and x.p_pc_xt_oos < 0.05
    big = abs(x.pc_xt_full) >= 0.15 or abs(x.sync_full) >= 0.30
    if plaus and big and rep and ys >= 0.75 and x.q_pc_xt_full < 0.05: return "YÜKSEK"
    if plaus and x.q_pc_xt_full < 0.05 and np.sign(x.pc_xt_is) == np.sign(x.pc_xt_oos): return "ORTA"
    if (plaus and x.p_pc_xt_full < 0.05) or (x.q_pc_xt_full < 0.05 and rep): return "DÜŞÜK"
    return "ÇOK DÜŞÜK"

rows = []
def row(**k):
    base = {c: "" for c in ["stock", "driver_yahoo", "driver_desc", "tv_ticker", "relation", "lag", "corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat",
                            "gap_corr", "intra_corr", "is_oos", "bt_oos_sharpe", "bt_oos_mean_bps", "n", "confidence", "mechanism", "notes"]}
    base.update(k); rows.append(base)

# (A) aile özetleri
REL = {"sync": "sync", "sync_usd": "sync", "pc_xu": "sync", "pc_xt": "sync", "pc_glob": "sync", "gap_l1": "lead_gap", "intra_l1": "lead_intra", "intra_l0": "lead_intra", "cum25": "lead_multiday", "rev": "reverse"}
g = FS[FS.label == "GERCEK"].set_index("fam"); nm = NS.groupby("fam")[["p<0.05", "bh05"]].mean()
for f, x in g.iterrows():
    row(stock="TÜMÜ(47)", driver_yahoo="TÜMÜ(1024)", driver_desc=f"AİLE ÖZETİ: {f}", relation=REL[f], lag={"gap_l1": 1, "intra_l1": 1, "intra_l0": 0, "cum25": "2-5", "rev": -1}.get(f, 0),
        n=int(x.n_tests), confidence="—", mechanism="çoklu test özeti",
        notes=(f"test={int(x.n_tests)}; p<0.05={int(x['p<0.05'])} (null ort. {nm.loc[f,'p<0.05']:.0f}); BH q0.05={int(x.bh05)}, q0.01={int(x.bh01)}; null BH q0.05 ort.={nm.loc[f,'bh05']:.2f}; "
               f"beklenen sahte (BH üst sınırı) ≈{0.05*x.bh05:.0f}; IS BH05 keşif={int(x.is_bh05)}, OOS replikasyon={x.rep_rate if pd.notna(x.rep_rate) else 'yok'} (null≈0.025); IS top200 rep={x.top200_rep_rate}"))

def pair_row(x, rel, block, ys, nys):
    row(stock=x.stock, driver_yahoo=x.driver, driver_desc=str(dm.loc[x.driver, "name"])[:60], tv_ticker=x.tv, relation=rel, lag=0,
        corr_full=x.sync_full, corr_3y=x.sync_3y, corr_1y=x.sync_1y, pcorr_xu100=x.pc_xu_full, beta=x.beta_sync_full, t_stat=x.t_pc_xt_full,
        gap_corr=x.gap_l1_full, intra_corr=x.intra_l1_full,
        is_oos=f"pc_xt IS {x.pc_xt_is:.3f} / OOS {x.pc_xt_oos:.3f} (p_OOS={x.p_pc_xt_oos:.2g}); yılların %{100*ys:.0f}'i aynı işaret ({nys} yıl)",
        n=int(x.n_sync_full), confidence=conf(x, ys), mechanism=x.mech,
        notes=f"[{block}] pc_xt={x.pc_xt_full:.3f} q={x.q_pc_xt_full:.2g}; pc_glob={x.pc_glob_full:.3f} q={x.q_pc_glob_full:.2g}; pc_xt_1y={x.pc_xt_1y:.3f}; kova={x.bucket}; grup={x.group}")

rep = lambda d, f: (np.sign(d[f + "_is"]) == np.sign(d[f + "_oos"])) & (d["p_" + f + "_oos"] < 0.05)
B = V[(V.q_pc_glob_full < 0.05) & rep(V, "pc_glob") & ~V.mirror].copy()
C = V[(V.q_pc_xt_full < 0.05) & rep(V, "pc_xt") & (V.pc_xt_full.abs() >= 0.08) & ~V.mirror].copy()
T5 = pd.read_csv(os.path.join(CACHE, "top5_per_stock.csv"))[["stock", "driver"]]
D5 = V.merge(T5, on=["stock", "driver"])
pairs = set(zip(B.stock, B.driver)) | set(zip(C.stock, C.driver)) | set(zip(D5.stock, D5.driver))
YS = year_share(sorted(pairs)); seen = set()
for block, S in [("SAĞLAM: pc_glob FDR+replike", B), ("pc_xt FDR+replike |pc|≥0.08", C), ("hisse başına ilk 5", D5)]:
    S = S.assign(a=S.pc_xt_full.abs()).sort_values(["stock", "a"], ascending=[True, False])
    for _, x in S.iterrows():
        if (x.stock, x.driver) in seen: continue
        seen.add((x.stock, x.driver)); ys, nys = YS[(x.stock, x.driver)]; pair_row(x, "sync", block, ys, nys)

# (E) öncülük
L = pd.read_csv(os.path.join(CACHE, "lead_bucket_fdr.csv"))
for _, x in L.iterrows():
    r = M[(M.stock == x.stock) & (M.driver == x.driver)].iloc[0]; f = x.fam
    row(stock=x.stock, driver_yahoo=x.driver, driver_desc=str(dm.loc[x.driver, "name"])[:60], tv_ticker=r.tv, relation="lead_multiday" if f == "cum25" else "lead_intra",
        lag={"intra_l1": 1, "intra_l0": 0, "cum25": "2-5"}[f], corr_full=r.sync_full, corr_3y=r.sync_3y, corr_1y=r.sync_1y, pcorr_xu100=r.pc_xu_full, beta=r.beta_sync_full,
        t_stat=r[f"t_{f}_full"], gap_corr=r.gap_l1_full, intra_corr=r[f"{f}_full"], is_oos=f"t_IS {r[f't_{f}_is']:.2f} / t_OOS {r[f't_{f}_oos']:.2f}", n=int(r[f"n_{f}_full"]),
        confidence="DÜŞÜK", mechanism=f"{x.mech}; Asya/Hindistan EM-akış difüzyonu?",
        notes=f"kova-içi BH q<0.05 ({x.bucket}); tüm-aile BH'de 0 geçiş; |r|~0.07 → maliyet sonrası kâr beklenmez")
AB = pd.read_csv(os.path.join(CACHE, "asia_bt.csv")); AC = pd.read_csv(os.path.join(CACHE, "asia_check.csv"))
for drv in ["^KS11", "^N225", "^TWII"]:
    a = AC[(AC.target == "XU030") & (AC.x == drv + "_{t-1}")].set_index("win"); r = M[(M.stock == "XU030") & (M.driver == drv)].iloc[0]
    b4 = AB[(AB.driver == drv) & (AB.target == "XU030") & (AB.cost == 4) & (AB["mode"] == "z1")].iloc[0]
    b8 = AB[(AB.driver == drv) & (AB.target == "XU030") & (AB.cost == 8) & (AB["mode"] == "z1")].iloc[0]
    row(stock="XU030", driver_yahoo=drv, driver_desc=f"{drv} lag1 -> XU030 gün-içi", tv_ticker=tv(drv), relation="lead_intra", lag=1, corr_full=r.sync_full, corr_1y=r.sync_1y,
        pcorr_xu100="", beta=r.beta_sync_full, t_stat=a.loc["full", "t_raw"], gap_corr=r.gap_l1_full, intra_corr=a.loc["full", "corr"],
        is_oos=f"corr IS {a.loc['is','corr']:.3f} / OOS {a.loc['oos','corr']:.3f} / 1y {a.loc['1y','corr']:.3f}; BIST kendi gecikmeleri+ABD lag1-2 kontrollü t={a.loc['full','t_ctrl']:.2f}",
        bt_oos_sharpe=b8.OOS_sharpe, bt_oos_mean_bps=b8.OOS_mean_bps, n=int(a.loc["full", "n"]),
        confidence="DÜŞÜK" if drv == "^KS11" else "ÇOK DÜŞÜK", mechanism="EM'e özgü bilgi (ABD'den arındırılmış Asya) BIST'e 1 gün gecikmeyle yayılıyor?; ABD lag1 ise gün-içinde hafif TERS (gap aşırı tepkisi)",
        notes=f"z>1 modu: 8bps OOS Sharpe {b8.OOS_sharpe:.2f} (t={b8.OOS_t:.2f}, n={int(b8.OOS_n)}); 4bps {b4.OOS_sharpe:.2f} (t={b4.OOS_t:.2f}); sign modu 8bps OOS<0. Yıllık corr çoğunlukla +, 2023 ve 2025 negatif")
BT = pd.read_csv(os.path.join(CACHE, "backtest.csv"))
for (st, dr, fm), gg in BT[BT.set == "IS-seçilmiş top10"].groupby(["stock", "driver", "fam"], sort=False):
    r = M[(M.stock == st) & (M.driver == dr)].iloc[0]; b15 = gg[(gg.cost == 15) & (gg["mode"] == "sign0")].iloc[0]; b8 = gg[(gg.cost == 8) & (gg["mode"] == "sign0")].iloc[0]
    bz = gg[(gg.cost == 8) & (gg["mode"] == "z1")].iloc[0]
    row(stock=st, driver_yahoo=dr, driver_desc=str(dm.loc[dr, "name"])[:60], tv_ticker=r.tv, relation="lead_multiday" if fm == "cum25" else "lead_intra",
        lag={"intra_l1": 1, "intra_l0": 0, "cum25": "2-5"}[fm], corr_full=r.sync_full, corr_1y=r.sync_1y, pcorr_xu100=r.pc_xu_full, t_stat=r[f"t_{fm}_full"],
        gap_corr=r.gap_l1_full, intra_corr=r[f"{fm}_full"], is_oos=f"t_IS {r[f't_{fm}_is']:.2f} / t_OOS {r[f't_{fm}_oos']:.2f}",
        bt_oos_sharpe=b15.OOS_sharpe, bt_oos_mean_bps=b15.OOS_bps, n=int(r[f"n_{fm}_full"]), confidence="ÇOK DÜŞÜK", mechanism=f"IS-seçilmiş backtest adayı ({fm})",
        notes=f"15bps sign: IS Sh {b15.IS_sharpe:.2f}, OOS Sh {b15.OOS_sharpe:.2f}; 8bps sign OOS Sh {b8.OOS_sharpe:.2f}; 8bps z>1 OOS Sh {bz.OOS_sharpe:.2f} (t={bz.OOS_t:.2f}); yıllar(8bps,bps): {b8.by_year}")

# (F) gap referansı (işlenemez)
for st in ["XU030", "XU100"]:
    for dr in ["^GSPC", "ES=F", "TUR", "EEM", "^VIX", "TRY=X"]:
        r = M[(M.stock == st) & (M.driver == dr)].iloc[0]
        row(stock=st, driver_yahoo=dr, driver_desc=str(dm.loc[dr, "name"])[:60], tv_ticker=r.tv, relation="lead_gap", lag=1, corr_full=r.sync_full, corr_3y=r.sync_3y, corr_1y=r.sync_1y,
            beta=r.beta_sync_full, t_stat=r.t_gap_l1_full, gap_corr=r.gap_l1_full, intra_corr=r.intra_l1_full,
            is_oos=f"gap corr IS {r.gap_l1_is:.3f} / OOS {r.gap_l1_oos:.3f} / 1y {r.gap_l1_1y:.3f}", n=int(r.n_gap_l1_full),
            confidence="YÜKSEK" if abs(r.t_gap_l1_full) >= 3 else "ORTA", mechanism="eşzamansız kapanış: ABD/FX kapanışı BIST'ten sonra → BIST açılış gap'inde fiyatlanır",
            notes="İŞLENEMEZ (açılıştan önce pozisyon alınamaz; VİOP akşam seansı hariç). TR-ayna/FX mekanik." if dr in ("TUR", "TRY=X") else "İŞLENEMEZ (açılış gap'i)")
# (G) rejim
MK = pd.read_csv(os.path.join(CACHE, "market_level.csv"))
for _, x in MK.iterrows():
    row(stock="XU100", driver_yahoo="EEM (+10 makro)", driver_desc="USD bazlı XU100 ~ EEM Dimson beta (lag0+lag1); R2 10 makro", tv_ticker="AMEX:EEM", relation="regime", lag="0+1",
        corr_full=x.get("corr0_USD_EEM"), beta=x.get("beta_dimson_USD_EEM"), n=int(x.n), confidence="DÜŞÜK" if x.n < 120 else "ORTA", mechanism="küresel EM risk iştahı / yabancı payı",
        notes=f"{x['dönem']}: R2 sync TL={x.R2_sync_XU100:.3f}, USD={x.R2_sync_XU100_USD:.3f}, yalnız EEM={x.R2_sync_XU100_yalnızEEM:.3f}; ABD lag1->gap R2={x.R2_ABDlag1_gap:.3f}, ->intra R2={x.R2_ABDlag1_intra:.3f}; β_USD~^GSPC={x['beta_dimson_USD_^GSPC']:.2f}")
FD = pd.DataFrame(rows)
for c in ["corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr", "bt_oos_sharpe", "bt_oos_mean_bps"]:
    FD[c] = pd.to_numeric(FD[c], errors="coerce").round(4)
FD.to_csv(os.path.join(OUT, "f_tarama.csv"), index=False)
s = FD[FD.relation == "sync"]
print("satır:", len(FD), FD.relation.value_counts().to_dict()); print("sync güven:", s.confidence.value_counts().to_dict())
print("SAĞLAM blok:", int(s.notes.str.contains("SAĞLAM").sum()), "| YÜKSEK:", "; ".join(f"{a}-{b}" for a, b in zip(s[s.confidence == 'YÜKSEK'].stock, s[s.confidence == 'YÜKSEK'].driver_yahoo)))
print("ORTA (ilk 40):", "; ".join(f"{a}-{b}" for a, b in list(zip(s[s.confidence == 'ORTA'].stock, s[s.confidence == 'ORTA'].driver_yahoo))[:40]))
