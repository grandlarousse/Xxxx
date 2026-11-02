"""S5: Seçim yanlılığı.
 (a) Kaynak ajanın bileşenleri 2014-2026 TAM örneklem taramasından (intra0_preopen, FDR) seçildi -> OOS kirli.
     Dürüst prosedür: aynı 72 açılış-öncesi Asya evreninde YALNIZ IS (2014-2020) korelasyonuna göre ilk-5'i seç, OOS'ta değerlendir.
 (b) Rastgele 5'li kompozit null dağılımı (aynı evren, 2000 çekiliş) -> JP_AU kompozitinin persentili.
Çıktı: res_s5_*.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v, numpy as np, pandas as pd
pd.set_option("display.width", 250)
UNI = ['000270.KS', '000660.KS', '004020.KS', '005380.KS', '005490.KS', '005930.KS', '006260.KS', '010120.KS', '010950.KS', '011170.KS', '012450.KS',
       '015760.KS', '034220.KS', '047810.KS', '051910.KS', '055550.KS', '064350.KS', '066570.KS', '079550.KS', '096770.KS', '103590.KS', '105560.KS',
       '2502.T', '2503.T', '267260.KS', '298040.KS', '3402.T', '4005.T', '5108.T', '5201.T', '5202.T', '5401.T', '5411.T', '6301.T', '6501.T', '6503.T',
       '6504.T', '6752.T', '6758.T', '7011.T', '7012.T', '7013.T', '7201.T', '7203.T', '7211.T', '7261.T', '7267.T', '7269.T', '7270.T', '8306.T',
       '8316.T', '8411.T', '9201.T', '9202.T', '9432.T', '9434.T', '9501.T', 'BHP.AX', 'CIA.AX', 'FMG.AX', 'IGO.AX', 'MIN.AX', 'NHC.AX', 'NIC.AX',
       'NUF.AX', 'RIO.AX', 'S32.AX', 'WHC.AX', 'YAL.AX', '^AXJO', '^KS11', '^N225']
JP_AU = ["5411.T", "5401.T", "6301.T", "FMG.AX", "BHP.AX"]
ST = ["EREGL.IS", "KRDMD.IS"]
Z = {}
for s in UNI:
    try: Z[s] = v.zpast(v.ret(s))
    except Exception as e: print("atla", s, e)
Z = pd.DataFrame(Z)
D = {s: v.decomp(s)["intra"] for s in ST}

def fast_bt(sig, y, cost=15.0, thr=1.0):
    df = pd.concat([sig.rename("s"), y.rename("y")], axis=1).dropna()
    z = v.zpast(df["s"]); pos = np.sign(z).where(z.abs() > thr, 0.0).fillna(0)
    p = pos * df["y"] - cost / 1e4 * pos.abs(); a = pos != 0
    o = {}
    for k, m in [("IS", (df.index < v.SPLIT) & (df.index >= "2014-01-01")), ("OOS", df.index >= v.SPLIT)]:
        x = p[a & m]; o[k] = 1e4 * x.mean() if len(x) else np.nan
        o[k + "_t"] = v.nw_mean_t(x)[1] if len(x) > 20 else np.nan
    return o

rows = []
for st in ST:
    y = D[st]
    # (a) yalnız-IS seçim
    isc = {}
    for s in Z.columns:
        df = pd.concat([y.rename("y"), Z[s].rename("x")], axis=1).dropna(); df = df[(df.index < v.SPLIT)]
        isc[s] = df["y"].corr(df["x"]) if len(df) > 250 else np.nan
    isc = pd.Series(isc).sort_values(ascending=False)
    print(st, "IS-only sıralama ilk 10:", isc.head(10).round(3).to_dict())
    for k in (3, 5, 8, 10):
        sel = list(isc.index[:k]); sig = Z[sel].mean(axis=1, skipna=True)
        r = fast_bt(sig, y); rows.append({"stock": st, "procedure": f"IS-only top{k}", "members": ",".join(sel), **r})
    r = fast_bt(Z[JP_AU].mean(axis=1, skipna=True), y); rows.append({"stock": st, "procedure": "kaynak JP_AU (tam-örneklem seçimi)", "members": ",".join(JP_AU), **r})
    r = fast_bt(Z.mean(axis=1, skipna=True), y); rows.append({"stock": st, "procedure": "tüm 72 eşit ağırlık", "members": "ALL", **r})
S = pd.DataFrame(rows); S.to_csv(os.path.join(v.OUT, "res_s5_is_selection.csv"), index=False)
print(S.drop(columns="members").round(2).to_string(index=False))

# (b) rastgele 5'li null
rng = np.random.default_rng(42); N = 2000; cols = list(Z.columns)
null = {st: [] for st in ST}
for i in range(N):
    sel = list(rng.choice(cols, 5, replace=False)); sig = Z[sel].mean(axis=1, skipna=True)
    for st in ST:
        r = fast_bt(sig, D[st]); null[st].append((r["IS"], r["OOS"], r["OOS_t"]))
out = []
for st in ST:
    a = np.array(null[st]); base = fast_bt(Z[JP_AU].mean(axis=1, skipna=True), D[st])
    pct_oos = (a[:, 1] < base["OOS"]).mean(); pct_is = (a[:, 0] < base["IS"]).mean()
    out.append({"stock": st, "null_OOS_mean": np.nanmean(a[:, 1]), "null_OOS_p50": np.nanmedian(a[:, 1]), "null_OOS_p95": np.nanpercentile(a[:, 1], 95),
                "null_OOS_share_pos": np.mean(a[:, 1] > 0), "null_OOS_t_p95": np.nanpercentile(a[:, 2], 95),
                "JP_AU_OOS": base["OOS"], "JP_AU_OOS_pctile": pct_oos, "JP_AU_IS": base["IS"], "JP_AU_IS_pctile": pct_is,
                "null_IS_mean": np.nanmean(a[:, 0])})
    np.save(os.path.join(v.OUT, f"res_s5_null_{st}.npy"), a)
O = pd.DataFrame(out); O.to_csv(os.path.join(v.OUT, "res_s5_null.csv"), index=False)
print(O.round(3).T.to_string())
