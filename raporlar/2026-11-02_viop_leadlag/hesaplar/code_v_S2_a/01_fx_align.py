"""01: USDTRY zaman damgası denetimi (bağımsız).
(a) 2024+: günlük TRY=X 'c' (ldate D) hangi UTC saatindeki saatlik fiyata eşit?
(b) 2008-2026 yıl yıl: parite P = ln(TKC_c * FX / (2.5 * TCELL_c)) günlük değişim varyansı, FX = (k=0) ldate<=t son bar, (k=1) ldate>t ilk bar, (k=2) ikinci bar.
    TKC kapanışı ~20/21 UTC t. Doğru hizalama varyansı en küçük yapar."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_a")
from vs import *
# (a)
fxd = dser("TRY=X", "c")
h = rawd("TRY=X", "h1"); h = h[~h.index.duplicated(keep="last")]
hc = pd.Series(h["c"].values, index=h.index + pd.Timedelta(hours=1))  # bar kapanış anı
hc = hc.sort_index()
rows = []
for off_h in range(-30, 25, 1):
    tgt = pd.DatetimeIndex(fxd.index).tz_localize("UTC") + pd.Timedelta(hours=off_h)
    pos = hc.index.searchsorted(tgt, side="right") - 1
    ok = pos >= 0
    v = pd.Series(np.where(ok, hc.values[np.clip(pos, 0, None)], np.nan), index=fxd.index)
    age = (tgt - hc.index[np.clip(pos, 0, None)]).total_seconds() / 3600
    v[(age > 3) | ~ok] = np.nan
    z = pd.concat([fxd, v], axis=1).dropna(); z = z[z.index >= "2024-02-01"]
    d = (np.log(z.iloc[:, 0] / z.iloc[:, 1])).abs() * 1e4
    rows.append((off_h, round(d.median(), 2), round(d.mean(), 2), len(z)))
A = pd.DataFrame(rows, columns=["saat_ofseti_ldate00UTC", "medyan_abs_fark_bps", "ort_abs_fark_bps", "n"])
print("(a) Günlük c(ldate D) vs saatlik fiyat (D 00:00 UTC + ofset saat):")
print(A[A.medyan_abs_fark_bps <= A.medyan_abs_fark_bps.min() * 4 + 5].to_string(index=False))
print("en iyi:", A.loc[A.medyan_abs_fark_bps.idxmin()].to_dict())
A.to_csv(OUT + "/01a_fx_hour_match.csv", index=False)
def hpx(off_h):
    tgt = pd.DatetimeIndex(fxd.index).tz_localize("UTC") + pd.Timedelta(hours=off_h)
    pos = hc.index.searchsorted(tgt, side="right") - 1
    v = pd.Series(np.where(pos >= 0, hc.values[np.clip(pos, 0, None)], np.nan), index=fxd.index)
    age = (tgt - hc.index[np.clip(pos, 0, None)]).total_seconds() / 3600
    v[(age > 3) | (pos < 0)] = np.nan
    return v
cands = {o: hpx(o) for o in [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]}
C = pd.DataFrame(cands); C["d"] = fxd; C = C[C.index >= "2024-02-01"].dropna()
mv = np.log(C[6] / C[0]).abs() * 1e4
for lo in [10, 20, 40]:
    q = C[mv > lo]
    err = {o: round(float((np.log(q.d / q[o]).abs() * 1e4).median()), 1) for o in cands}
    print(f"00->06 UTC hareketi >{lo} bps olan günler (n={len(q)}): medyan |c - saatlik(ofset)| bps:", err)
mv2 = np.log(C[0] / C[-3]).abs() * 1e4
q = C[mv2 > 10]
print("21->00 UTC hareketi >10 bps günler (n=%d):" % len(q), {o: round(float((np.log(q.d / q[o]).abs() * 1e4).median()), 1) for o in cands})

# (b) parite varyansı
tk = dser("TKC", "c", drop_zero_vol=True); tc = dser("TCELL.IS", "c", drop_zero_vol=True)
dates = tc.index.intersection(tk.index)
fxi = fxd.index
def fx_k(k):
    if k == 0:
        pos = fxi.searchsorted(dates, side="right") - 1
    else:
        pos = fxi.searchsorted(dates, side="right") + (k - 1)
    ok = (pos >= 0) & (pos < len(fxi))
    vals = np.where(ok, fxd.values[np.clip(pos, 0, len(fxi) - 1)], np.nan)
    gapd = np.where(ok, (fxi[np.clip(pos, 0, len(fxi) - 1)] - dates).days, 999)
    s = pd.Series(vals, index=dates); s[np.abs(gapd) > 6] = np.nan
    return s
res = {}
for k in [0, 1, 2]:
    P = np.log(tk.reindex(dates) * fx_k(k) / (2.5 * tc.reindex(dates)))
    dP = P.diff()
    dP = dP[dP.abs() < 0.2]
    res[f"k{k}"] = (dP.groupby(dP.index.year).std() * 1e4)
R = pd.DataFrame(res).round(1).dropna(how="all"); R["en_iyi"] = R[["k0","k1","k2"]].idxmin(axis=1)
print("\n(b) yıllık std(ΔP) bps; k0=ldate<=t bar, k1=ldate>t ilk bar, k2=ikinci bar")
print(R.to_string())
R.to_csv(OUT + "/01b_parity_var_by_k.csv")
# (c) TCELL günlük kapanış vs saatlik son bar; TKC günlük kapanış vs saatlik son bar
for sym in ["TCELL.IS", "TKC"]:
    d = dser(sym, "c"); hh = rawd(sym, "h1"); hh = hh[~hh.index.duplicated(keep="last")]
    last = pd.Series(hh["c"].values, index=pd.DatetimeIndex(hh["ldate"].values)).groupby(level=0).last()
    z = pd.concat([d, last], axis=1).dropna()
    dd = (np.log(z.iloc[:, 0] / z.iloc[:, 1])).abs() * 1e4
    print(sym, "günlük c vs saatlik son bar c: medyan |fark| bps", round(dd.median(), 2), "oran >5bps", round((dd > 5).mean(), 3), "n", len(z))
    print(" saatlik bar saatleri (UTC) dağılımı:", pd.Series(hh.index.strftime("%H:%M")).value_counts().sort_index().to_dict())
