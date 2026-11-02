"""v1: Günlük (2014–2026) açılış gap fade yeniden üretimi — giriş E0 = açılış müzayedesi fiyatı (iyimser), çıkış = kapanış.
pos = −sign(gap) (|gap|>eşik), PnL = intra = ln(C/O). Hisse bazında ve eşit ağırlıklı portföy. IS 2014–2020, OOS 2021–2026.
Ek: likit/illikit (statik: son 250 gün spot ciro; dinamik: geçmiş 250 gün ciro sırası), asimetri (gap-up short vs gap-down long),
gün-içi sürüklenme arındırması (geçmiş 250 gün ortalama intra çıkarılmış), 2016+ IS, eşik duyarlılığı, yıllar.
Çıktı: res/v1_stock.csv, res/v1_port.csv, res/v1_years.csv
"""
import numpy as np, pandas as pd, vc
TG = vc.VIOP
D = {s: vc.decomp(s) for s in TG + ["XU030"]}
idx = vc.cal(); idx = idx[idx >= "2014-01-01"]
G = pd.DataFrame({s: D[s]["gap"] for s in TG}).reindex(idx)
GR = pd.DataFrame({s: D[s]["gap_raw"] for s in TG}).reindex(idx)
I = pd.DataFrame({s: D[s]["intra"] for s in TG}).reindex(idx)
TURN = pd.DataFrame({s: D[s]["turn"] for s in TG}).reindex(idx)
I = I.where(G.notna())

# likidite
last = TURN[TURN.index >= idx[-250]].median()
rank = last.rank(ascending=False)
LIQ = list(rank[rank <= 23].index); ILL = list(rank[rank > 23].index)
dyn = TURN.rolling(250, min_periods=120).median().shift(1)
dynrank = dyn.rank(axis=1, ascending=False, pct=True)
pd.DataFrame({"turn_med_250_mnTL": last / 1e6, "rank": rank}).sort_values("rank").to_csv(vc.RES + "/v1_liq.csv")

PER = {"IS14-20": (idx < vc.SPLIT), "OOS21-26": (idx >= vc.SPLIT), "ALL": np.ones(len(idx), bool),
       "IS16-20": (idx >= "2016-01-01") & (idx < vc.SPLIT), "2024+": idx >= "2024-01-01"}

def fade_pos(g, thr):
    return (-np.sign(g)).where(g.abs() > thr, 0.0).fillna(0.0)

rows = []
for thr in [0.005, 0.01, 0.02]:
    P = fade_pos(G, thr)
    R = (P * I).where(P != 0)
    for s in TG:
        o = dict(stock=s, thr=thr)
        for pn, m in PER.items():
            x = R[s][m].dropna()
            mm, t, n = vc.nw_mean(x.values, 5)
            o[f"{pn}_n"] = n; o[f"{pn}_bps"] = 1e4 * mm; o[f"{pn}_t"] = t
        rows.append(o)
S = pd.DataFrame(rows)
for thr, g in S.groupby("thr"):
    for pn in ["ALL", "OOS21-26"]:
        rej, padj = vc.bh(vc.t2p(g[f"{pn}_t"].values)); S.loc[g.index, f"fdr_{pn}"] = rej
S["liq"] = S["stock"].map(lambda s: "likit" if s in LIQ else "illikit")
S.to_csv(vc.RES + "/v1_stock.csv", index=False)

print("=== HİSSE BAZINDA (E0) ===")
for thr, g in S.groupby("thr"):
    print(f"thr {thr:.1%}: medyan IS {g['IS14-20_bps'].median():.1f}  OOS {g['OOS21-26_bps'].median():.1f}  IS16-20 {g['IS16-20_bps'].median():.1f}  2024+ {g['2024+_bps'].median():.1f} | OOS>0 {np.mean(g['OOS21-26_bps']>0):.0%} | FDR(all) {int(g['fdr_ALL'].sum())}  FDR(OOS) {int(g['fdr_OOS21-26'].sum())} | OOS n toplam {int(g['OOS21-26_n'].sum())}")
g = S[S.thr == 0.01].set_index("stock")
print(g.loc[["CIMSA", "OYAKC", "ALARK", "GARAN", "AKBNK", "THYAO"], ["IS14-20_bps", "IS14-20_t", "OOS21-26_bps", "OOS21-26_t", "OOS21-26_n", "ALL_t", "fdr_ALL", "fdr_OOS21-26"]].round(2).to_string())
print("FDR(all) geçenler 1%:", list(g.index[g["fdr_ALL"].astype(bool)]))
print("FDR(OOS) geçenler 1%:", list(g.index[g["fdr_OOS21-26"].astype(bool)]))

# portföy
prow = []; YR = {}
def port(P, Y, cols):
    R = (P[cols] * Y[cols]).where(P[cols] != 0)
    return R.mean(axis=1), (P[cols] != 0).sum(axis=1)
def rec(name, pp, ntr):
    o = dict(spec=name)
    for pn, m in PER.items():
        x = pp[m].dropna(); mm, t, n = vc.nw_mean(x.values, 5)
        o[f"{pn}_bps"] = 1e4 * mm; o[f"{pn}_t"] = t; o[f"{pn}_days"] = n; o[f"{pn}_trades"] = int(ntr[m].sum())
    prow.append(o)
for thr in [0.005, 0.01, 0.02]:
    P = fade_pos(G, thr)
    for uni, cols in [("47", TG), ("likit23", LIQ), ("illikit24", ILL)]:
        pp, nt = port(P, I, cols); rec(f"E0 |gap|>{thr:.1%} {uni}", pp, nt)
        if thr == 0.01: YR[f"E0_1%_{uni}"] = 1e4 * pp.groupby(pp.index.year).mean()
    # dinamik likidite (o günkü geçmiş 250g ciro sırası; look-ahead yok)
    for lab, msk in [("dinamik-likit-yarı", dynrank <= 0.5), ("dinamik-illikit-yarı", dynrank > 0.5)]:
        Pm = P.where(msk.fillna(False), 0.0)
        pp, nt = port(Pm, I, TG); rec(f"E0 |gap|>{thr:.1%} {lab}", pp, nt)
    # ham gap tanımı (temettü düzeltmesiz)
    Pr = fade_pos(GR.where(G.notna()), thr); pp, nt = port(Pr, I, TG); rec(f"E0 |gap_raw|>{thr:.1%} 47", pp, nt)
P = fade_pos(G, 0.01)
# asimetri
pp, nt = port(P.where(G > 0, 0.0), I, TG); rec("E0 1% yalnız gap-UP short", pp, nt)
pp, nt = port(P.where(G < 0, 0.0), I, TG); rec("E0 1% yalnız gap-DOWN long", pp, nt)
# sürüklenme arındırma: intra - geçmiş 250g ortalama intra
mu = I.rolling(250, min_periods=60).mean().shift(1)
pp, nt = port(P, I - mu, TG); rec("E0 1% 47, intra − geçmiş ort (sürüklenme arındırılmış)", pp, nt)
# koşulsuz 'hep short gün-içi' benchmark ve net short eğilimi
pp, nt = port(pd.DataFrame(-1.0, index=idx, columns=TG).where(G.abs() > 0.01, 0.0), I, TG); rec("BENCH: |gap|>1% günlerde hep short gün-içi", pp, nt)
# o==c günleri hariç (2014-15 veri kusuru duyarlılığı; sonuca göre koşullama içerdiği için yalnız bilgi amaçlı)
OC = pd.DataFrame({s: D[s]["oc_eq"] for s in TG}).reindex(idx).fillna(False).astype(bool)
pp, nt = port(P.where(~OC, 0.0), I, TG); rec("E0 1% 47, o==c günleri hariç (bilgi)", pp, nt)
# piyasa gap günleri
gm = D["XU030"]["gap"].reindex(idx)
big = (gm.abs() > 0.01).values
pp, nt = port(P.where(pd.DataFrame(np.repeat(big[:, None], len(TG), 1), index=idx, columns=TG), 0.0), I, TG); rec("E0 1% 47, |XU030 gap|>1% günleri", pp, nt)
pp, nt = port(P.where(pd.DataFrame(np.repeat(~big[:, None], len(TG), 1), index=idx, columns=TG), 0.0), I, TG); rec("E0 1% 47, diğer günler", pp, nt)

PT = pd.DataFrame(prow); PT.to_csv(vc.RES + "/v1_port.csv", index=False)
pd.set_option("display.width", 250)
print("\n=== PORTFÖY (eşit ağırlık, günlük ortalama işlem getirisi, NW5 t) ===")
cols = ["spec"] + [f"{p}_{k}" for p in ["IS14-20", "OOS21-26", "IS16-20", "2024+"] for k in ["bps", "t"]] + ["OOS21-26_trades"]
print(PT[cols].round(2).to_string())
Y = pd.DataFrame(YR); Y.to_csv(vc.RES + "/v1_years.csv")
print("\n=== YILLAR (E0 1%, bps) ==="); print(Y.round(1).to_string())
print("net short oranı (|gap|>1% işlemlerde gap>0 payı):", float((G > 0.01).sum().sum() / (G.abs() > 0.01).sum().sum()))
print("likit23:", LIQ); print("illikit24:", ILL)
