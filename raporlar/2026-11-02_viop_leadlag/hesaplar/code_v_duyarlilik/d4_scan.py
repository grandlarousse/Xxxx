"""(a) Gap fade IS varyantı: v4 ama |gap|>%10,5 işlemler hariç (açılış müzayedesinde dolum gerçekçi değil; devre kesici günleri)
(b) Genel tarama: f_y_hisse.csv 'sync' çiftleri (hisse ajanının yöntemi: ll.decomp cc, BIST takvimi, 2014+) — v3 vs v4 kısmi korelasyon (XU100),
    IS/OOS; |pc|>=0.15 eşiğini geçen/kaybeden çiftler ve en çok değişenler."""
import vers, numpy as np, pandas as pd, statsmodels.api as sm
L = vers.L; STK = vers.VIOP
def nw_mean(x, lags=5):
    x = pd.Series(x).dropna(); m = sm.OLS(x.values, np.ones(len(x))).fit(cov_type="HAC", cov_kwds={"maxlags": lags}); return float(m.params[0]), float(m.tvalues[0]), len(x)
rows = []
for v in ["v3", "v4"]:
    D = {s: L[v].decomp(s + ".IS") for s in STK}
    gaps = pd.DataFrame({s: D[s]["gap"] for s in STK}); gaps = gaps[(gaps.index >= "2014-01-01") & (gaps.index < "2021-01-01")]
    intra = pd.DataFrame({s: D[s]["intra"] for s in STK}).reindex(gaps.index)
    for lab, cap in [("tümü", 9), ("|gap|<=%10,5", np.log(1.105))]:
        pos = -np.sign(gaps).where((gaps.abs() > 0.01) & (gaps.abs() <= cap), 0.0)
        g = (pos * intra).where((pos != 0) & intra.notna()); m, t, n = nw_mean(g.mean(axis=1))
        med = float(np.nanmedian([1e4 * g[s].mean() for s in STK]))
        rows.append(dict(ver=v, variant=lab, IS_port_bps=1e4 * m, IS_port_t=t, IS_median_stock_bps=med, n_trades=int(g.notna().sum().sum())))
FA = pd.DataFrame(rows); FA.to_csv(vers.RES + "/d4_fade_IS_variants.csv", index=False); print(FA.round(2).to_string())
# ---------------- (b) çift taraması
H = pd.read_csv(vers.OUT + "/f_y_hisse.csv"); H = H[H.relation == "sync"].copy()
H["drv"] = H["driver_yahoo"].astype(str).str.replace(".IS", "", regex=False)
H = H[H["drv"].str.fullmatch(r"[A-Z0-9]+")]
syms = sorted(set(H["stock"]) | set(H["drv"]) | {"XU100"})
CAL = L["v4"].bist_cal(); CAL = CAL[CAL >= "2014-01-01"]
CC = {}
for v in ["v3", "v4"]:
    d = {}
    for s in syms:
        try: d[s] = L[v].decomp(s + ".IS")["cc"].reindex(CAL)
        except Exception as e: pass
    CC[v] = pd.DataFrame(d)
def pcv(a, b, m):
    df = pd.concat([a, b, m], axis=1).dropna()
    if len(df) < 60: return np.nan
    X = np.column_stack([np.ones(len(df)), df.iloc[:, 2].values])
    ra = df.iloc[:, 0].values - X @ np.linalg.lstsq(X, df.iloc[:, 0].values, rcond=None)[0]; rb = df.iloc[:, 1].values - X @ np.linalg.lstsq(X, df.iloc[:, 1].values, rcond=None)[0]
    return float(np.corrcoef(ra, rb)[0, 1])
out = []
for _, r in H.iterrows():
    a, b = r["stock"], r["drv"]
    if a not in CC["v4"] or b not in CC["v4"]: continue
    o = dict(stock=a, driver=b, agent_pc=r["pcorr_xu100"], agent_conf=r["confidence"])
    for v in ["v3", "v4"]:
        C = CC[v]
        for per, m in [("full", C.index >= "2014-01-01"), ("IS", C.index < "2021-01-01"), ("OOS", C.index >= "2021-01-01"), ("1y", C.index >= C.index[-1] - pd.DateOffset(years=1))]:
            o[f"pc_{per}_{v}"] = pcv(C.loc[m, a], C.loc[m, b], C.loc[m, "XU100"])
        o[f"corr_1y_{v}"] = C.loc[C.index >= C.index[-1] - pd.DateOffset(years=1), [a, b]].dropna().corr().iloc[0, 1]
    out.append(o)
S = pd.DataFrame(out).drop_duplicates(["stock", "driver"])
for per in ["full", "IS", "OOS", "1y"]: S[f"d_{per}"] = S[f"pc_{per}_v4"] - S[f"pc_{per}_v3"]
S["d_corr_1y"] = S["corr_1y_v4"] - S["corr_1y_v3"]
S["cross015_full"] = (S["pc_full_v3"].abs() >= 0.15) != (S["pc_full_v4"].abs() >= 0.15)
S["cross015_IS"] = (S["pc_IS_v3"].abs() >= 0.15) != (S["pc_IS_v4"].abs() >= 0.15)
S["sign_flip_IS"] = np.sign(S["pc_IS_v3"]) != np.sign(S["pc_IS_v4"])
S.to_csv(vers.RES + "/d4_pair_scan.csv", index=False)
pd.set_option("display.width", 250)
print("çift sayısı", len(S), " v3 rekonstrüksiyonu ajan pc ile |fark|<0.005:", float(((S.pc_full_v3 - S.agent_pc).abs() < 0.005).mean()))
print(S[["d_full", "d_IS", "d_OOS", "d_1y", "d_corr_1y"]].abs().describe().round(4).to_string())
print("eşik 0.15 geçişi (full):", int(S.cross015_full.sum()), " (IS):", int(S.cross015_IS.sum()), " IS işaret dönüşü:", int(S.sign_flip_IS.sum()))
cols = ["stock", "driver", "agent_pc", "agent_conf", "pc_full_v3", "pc_full_v4", "pc_IS_v3", "pc_IS_v4", "pc_1y_v3", "pc_1y_v4", "corr_1y_v3", "corr_1y_v4"]
S["maxd"] = S[["d_full", "d_IS", "d_1y", "d_corr_1y"]].abs().max(axis=1)
print(S.sort_values("maxd", ascending=False)[cols].head(25).round(3).to_string())
print(S[S.cross015_full | S.cross015_IS][cols].round(3).to_string())
