"""Adim 6: (c) TRALT en iyi SHFE altiniyla mi aciklaniyor? Haftalik (Cuma-Cuma, BIST takvimi) ORTAK orneklemde
SHFE AU (Sina, roll-duzeltilmis, CNY) vs COMEX GC=F (USD) vs GC*USDTRY (TL altin) vs GLD; XU100 ve XU100+USDTRY kontrollu kismi korelasyon,
yillara gore, IS/OOS, blok-bootstrap fark testi, zamanlama kaydirmasi (SHFE haftasi Pazartesi 07:00 UTC'ye kadar uzatilmis).
Ek: (a) icin 1787.HK CLOSE'un 600547.SS CLOSE (07:00 UTC) otesinde katkisi (tum donem)."""
import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a")
import vlib as V, numpy as np, pandas as pd
from s02_hk_timing import signals
pd.set_option("display.width", 250)
OUT = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_a/"
C = V.cal()
TR = V.bist_daily("TRALT.IS"); XU = V.bist_daily("XU100.IS"); TM = V.bist_daily("TRMET.IS")
def lvl_on_cal(r_local):
    lp = r_local.fillna(0).cumsum(); lv, fr = V.on_cal(lp, C); return lv
au = V.shfe_main("AU"); au_lv = lvl_on_cal(au["r_cc"])
def ylv(sym):
    s = np.log(V.local_px(sym)); lv, _ = V.on_cal(s, C); return lv
L = pd.DataFrame({"AU": au_lv, "GC": ylv("GC=F"), "GLD": ylv("GLD"), "TRY": ylv("TRY=X"), "CNY": ylv("CNY=X")})
L["GC_TL"] = L["GC"] + L["TRY"]; L["AU_USD"] = L["AU"] - L["CNY"]; L["AU_TL"] = L["AU_USD"] + L["TRY"]
# BIST: kumulatif log fiyat (temizlenmis cc ile)
L["TRALT"] = TR["cc"].reindex(C).fillna(0).cumsum(); L["XU100"] = XU["cc"].reindex(C).fillna(0).cumsum(); L["TRMET"] = TM["cc"].reindex(C).fillna(0).cumsum()
L = L[L.index >= "2018-11-12"]
# AU kaydirmali: BIST gunu t icin SHFE seviyesi = t+1 SHFE kapanisi (07:00 UTC t+1) -> BIST t seansini tamamen icerir
L["AU_fwd1"] = L["AU"].shift(-1)
def weekly(Lv, cols):
    W = Lv[cols].resample("W-FRI").last().diff().dropna(how="all"); return W
cols = ["TRALT", "TRMET", "XU100", "AU", "AU_fwd1", "AU_USD", "AU_TL", "GC", "GC_TL", "GLD", "TRY"]
W = weekly(L, cols).dropna()
def pc(df, a, b, ctrl):
    X = np.column_stack([np.ones(len(df))] + [df[c].values for c in ctrl])
    ra = df[a].values - X @ np.linalg.lstsq(X, df[a].values, rcond=None)[0]; rb = df[b].values - X @ np.linalg.lstsq(X, df[b].values, rcond=None)[0]
    return np.corrcoef(ra, rb)[0, 1]
rows = []
for stock in ["TRALT", "TRMET"]:
    for d in ["AU", "AU_fwd1", "AU_USD", "AU_TL", "GC", "GC_TL", "GLD"]:
        df = W[[stock, d, "XU100", "TRY"]].dropna()
        r = {"hisse": stock, "surucu": d, "n_hafta": len(df), "r": df[stock].corr(df[d]), "pc_xu": pc(df, stock, d, ["XU100"]), "pc_xu_try": pc(df, stock, d, ["XU100", "TRY"])}
        for lab, g in [("IS<2021", df[df.index < "2021-01-01"]), ("OOS>=2021", df[df.index >= "2021-01-01"]), ("son3y", df[df.index >= "2023-10-30"])]:
            r["pc_xu_" + lab] = pc(g, stock, d, ["XU100"])
        yc = df.groupby(df.index.year).apply(lambda g: pc(g, stock, d, ["XU100"]) if len(g) > 25 else np.nan).dropna()
        r["yil_pc>0"] = f"{int((yc > 0).sum())}/{len(yc)}"; r["yil_pc"] = "; ".join(f"{k}:{v:.2f}" for k, v in yc.items())
        rows.append(r)
R = pd.DataFrame(rows); R.round(3).to_csv(OUT + "s06_weekly_gold.csv", index=False)
print("Haftalik (Cuma-Cuma), ortak orneklem", W.index[0].date(), "->", W.index[-1].date()); print(R.drop(columns=["yil_pc"]).round(3).to_string())
print(R[["hisse", "surucu", "yil_pc"]].to_string())
# blok bootstrap: pc(TRALT,AU|XU) - pc(TRALT,GC|XU)
rng = np.random.default_rng(11); df = W[["TRALT", "AU", "GC", "GC_TL", "XU100", "TRY"]].dropna(); B = 8; nb = len(df) // B; diffs = []; diffs2 = []
for _ in range(2000):
    idx = np.concatenate([np.arange(b * B, b * B + B) for b in rng.integers(0, nb, nb)]); g = df.iloc[idx]
    diffs.append(pc(g, "TRALT", "AU", ["XU100"]) - pc(g, "TRALT", "GC", ["XU100"])); diffs2.append(pc(g, "TRALT", "AU", ["XU100", "TRY"]) - pc(g, "TRALT", "GC_TL", ["XU100", "TRY"]))
d0 = pc(df, "TRALT", "AU", ["XU100"]) - pc(df, "TRALT", "GC", ["XU100"])
print(f"\nFark pc(AU)-pc(GC) | XU100: {d0:+.3f}  %95 GA [{np.percentile(diffs, 2.5):+.3f}, {np.percentile(diffs, 97.5):+.3f}]  P(fark<=0)={np.mean(np.array(diffs) <= 0):.3f}")
print(f"Fark pc(AU)-pc(GC_TL) | XU100+TRY: GA [{np.percentile(diffs2, 2.5):+.3f}, {np.percentile(diffs2, 97.5):+.3f}]")
# yaris regresyonu (standartlastirilmis, NW)
z = lambda s: (s - s.mean()) / s.std()
for ctrl in [["XU100"], ["XU100", "TRY"]]:
    X = pd.DataFrame({"AU": z(df.AU), "GC": z(df.GC), **{c: z(df[c]) for c in ctrl}}); p, t, n = V.nw(z(df.TRALT), X, 4)
    print("Yaris TRALT_w ~ AU + GC +", ctrl, ":", " ".join(f"{k}={p[k]:+.3f}(t={t[k]:+.2f})" for k in X.columns), "n", n)
# Gunluk zamanlama: TRALT cc_t ile AU_t (07:00 t-1 -> 07:00 t) vs AU_{t+1} (07:00 t -> 07:00 t+1) vs GC_t
Dd = L[["TRALT", "XU100", "AU", "AU_fwd1", "GC", "GC_TL"]].diff().dropna()
print("\nGunluk korelasyon (2018-11+): ", {k: round(Dd.TRALT.corr(Dd[k]), 3) for k in ["AU", "AU_fwd1", "GC", "GC_TL"]},
      " kismi|XU:", {k: round(pc(Dd, "TRALT", k, ["XU100"]), 3) for k in ["AU", "AU_fwd1", "GC", "GC_TL"]})
D2 = L[["TRALT", "XU100", "AU", "AU_fwd1", "GC", "GC_TL"]].iloc[::2].diff().dropna()
print("2 gunluk ortusmeyen:", {k: round(D2.TRALT.corr(D2[k]), 3) for k in ["AU", "AU_fwd1", "GC", "GC_TL"]}, " kismi|XU:", {k: round(pc(D2, "TRALT", k, ["XU100"]), 3) for k in ["AU", "AU_fwd1", "GC", "GC_TL"]})
# Haftalik oncu: SHFE AU / GC haftasi t -> TRALT haftasi t+1
for d in ["AU", "GC"]:
    g = pd.concat([W.TRALT, W[d].shift(1).rename("lag"), W.XU100], axis=1).dropna()
    p, t, n = V.nw(z(g.TRALT), pd.DataFrame({"lag": z(g.lag), "XU": z(g.XU100)}), 4)
    print(f"Haftalik oncu {d}_(w-1) -> TRALT_w: beta={p['lag']:+.3f} t={t['lag']:+.2f} n={n}")
# (a) ek: 1787.HK CLOSE 600547.SS CLOSE otesinde ne katiyor (tum donem)
S1 = signals("1787.HK"); S3 = signals("600547.SS")
F = pd.concat([TR["intra"].rename("y"), S1["CLOSE"].rename("hk"), S3["CLOSE"].rename("ss"), S1["OPEN"].rename("hk_open")], axis=1).dropna()
F = F[F.index >= "2018-10-01"]
for lab, X in [("ss", ["ss"]), ("hk", ["hk"]), ("ss+hk", ["ss", "hk"]), ("ss+hk_open", ["ss", "hk_open"])]:
    p, t, n = V.nw(z(F.y), pd.DataFrame({c: z(F[c]) for c in X}))
    print(f"(a) TRALT oc ~ {lab:12s}: " + " ".join(f"{c}={p[c]:+.3f}(t={t[c]:+.2f})" for c in X), "n", n)
F["hk_res"] = F.hk - np.polyval(np.polyfit(F.ss, F.hk, 1), F.ss)
for lab, s in [("hk_res (1787 CLOSE'un 600547'ye dik kismi)", F.hk_res)]:
    r, _ = V.bt(s, F.y, 10); print(lab, "BT10:", {k: (round(r[k].get('mean_bps', np.nan), 1), round(r[k].get('sharpe', np.nan), 2)) for k in ['ALL', 'IS', 'OOS']})
