"""GÖREV 2: 5 dk lead-lag (son ~60 gün). corr(BIST_t, D_{t-k}), k=-6..6 (k>0: sürücü önde). Pencereler: tüm gün, ABD öncesi (07:00-13:25 UTC),
ABD nakit açılışı örtüşmesi (13:30-14:55 UTC; m5 örnekleminin tamamında ABD yaz saati -> açılış 13:30 UTC).
Getiri ızgarası: BIST gününün 07:00..14:55 bar başlangıçları; r_t = log(c_t/c_{t-1}); 07:00 barı 06:55 açılış müzayedesine göre. 15:00 kapanış müzayedesi hariç.
Backtest: |ES_{t-1}| > z·σ (σ önceki günlerden) ise sign(ES_{t-1}) yönünde t..t+h-1 boyunca pozisyon; örtüşmeyen işlemler.
Çalıştır: python t2_m5_leadlag.py
"""
import numpy as np, pandas as pd, g_common as g
SYMS = g.IDX + g.VIOP
DRV = ["ES=F", "NQ=F", "BZ=F", "TRY=X", "GC=F", "^GDAXI"]

def m5_close(sym):
    d = g.load(sym, "m5"); d = d[~d.index.duplicated(keep="last")].sort_index()
    return d["c"].where(d["c"] > 0)

# ızgara: XU030 m5 günleri, 06:55..14:55
xu = g.load("XU030", "m5"); bdays = pd.DatetimeIndex(xu.index.tz_convert(None).normalize().unique())
grid = []
for d in bdays:
    t = pd.date_range(d + pd.Timedelta("06:55:00"), d + pd.Timedelta("14:55:00"), freq="5min", tz="UTC"); grid.append(t)
grid = grid[0].append(grid[1:])
def on_grid(sym, ffill_lim=None):
    c = m5_close(sym)
    s = c.reindex(c.index.union(grid)).ffill(limit=ffill_lim).reindex(grid) if ffill_lim else c.reindex(c.index.union(grid)).ffill().reindex(grid)
    # gün içi getiri, 06:55 barının kendisi (gece) hariç
    r = np.log(s).diff(); day = grid.tz_convert(None).normalize()
    first = pd.Series(day, index=grid).diff().dt.days.fillna(1).ne(0).values
    r[first] = np.nan
    return r
R = {s: on_grid(s) for s in SYMS}
DR = {}
for d in DRV:
    try: DR[d] = on_grid(d, ffill_lim=12)
    except Exception as e: print("skip", d, e)
# sürücü verisinin olmadığı günleri at (ES m5 2026-08-21'den başlar)
hm = grid.hour * 100 + grid.minute
day = grid.tz_convert(None).normalize()
W = {"all": (hm >= 700) & (hm <= 1455), "preUS": (hm >= 700) & (hm < 1330), "USopen": (hm >= 1330) & (hm <= 1455), "US30": (hm >= 1330) & (hm < 1400)}

def lagged(x, k):
    """x_{t-k} gün içinde (gün sınırını geçmez)."""
    xs = x.shift(k); dd = pd.Series(day, index=grid); same = dd.shift(k) == dd
    return xs.where(same.values)

rows = []
for s in SYMS:
    y = R[s]
    for d, x in DR.items():
        for wn, msk in W.items():
            for k in range(-6, 7):
                xl = lagged(x, k)
                df = pd.concat([y.rename("y"), xl.rename("x")], axis=1)[msk].dropna()
                df = df[(df["x"] != 0) | (df["y"] != 0)]
                if len(df) < 200: continue
                c = df["y"].corr(df["x"]); n = len(df)
                rows.append(dict(stock=s, driver=d, window=wn, lag=k, corr=c, n=n, t=c * np.sqrt(n), ndays=df.index.tz_convert(None).normalize().nunique()))
CC = pd.DataFrame(rows); CC.to_csv(g.RES + "/t2_ccf.csv", index=False)

# kümülatif dağıtılmış gecikme regresyonu: y_t = sum_k b_k x_{t-k}, k=0..6 (ES ve TRY)
import statsmodels.api as sm
rows2 = []
for s in SYMS:
    for d in ["ES=F", "NQ=F", "BZ=F", "TRY=X"]:
        if d not in DR: continue
        for wn, msk in W.items():
            Xl = pd.concat([lagged(DR[d], k).rename(f"l{k}") for k in range(0, 7)], axis=1)
            df = pd.concat([R[s].rename("y"), Xl], axis=1)[msk].dropna()
            if len(df) < 300: continue
            m = sm.OLS(df["y"], sm.add_constant(df.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
            b = m.params[1:].values; t = m.tvalues[1:].values
            L = np.zeros(7); L[1:] = 1; cov = m.cov_params().values[1:, 1:]
            sl = b[1:].sum(); tsl = sl / np.sqrt(L @ cov @ L)
            rows2.append(dict(stock=s, driver=d, window=wn, b0=b[0], t0=t[0], b1=b[1], t1=t[1], sum_b1_6=sl, t_sum_b1_6=tsl,
                              delayed_share=sl / (b.sum()) if b.sum() != 0 else np.nan, r2=m.rsquared, n=len(df)))
DL = pd.DataFrame(rows2); DL.to_csv(g.RES + "/t2_distlag.csv", index=False)

# backtest: ES_{t-1} şoku -> BIST t..t+h-1
rows3 = []
x = DR["ES=F"]; xl1 = lagged(x, 1)
dd = pd.Series(day, index=grid)
# σ: önceki günlerin ES 5dk std'si (genişleyen, gün bazında kaydırılmış)
dstd = x[W["all"]].groupby(day[W["all"]]).std()
sig_prev = dstd.expanding(5).mean().shift(1)
sig = pd.Series(sig_prev.reindex(day).values, index=grid)
alld = pd.DatetimeIndex(sorted(set(day[x.notna().values])))
mid = alld[len(alld) // 2]
for s in SYMS:
    y = R[s]
    for h in [1, 3, 6]:
        fwd = sum(lagged(y, -j).fillna(0) for j in range(h))  # y_t + ... + y_{t+h-1} (aynı gün)
        valid_end = lagged(y, -(h - 1)).notna()
        for z in [1.0, 2.0, 3.0]:
            for wn in ["all", "USopen", "preUS"]:
                cand = (xl1.abs() > z * sig) & W[wn] & valid_end & y.notna()
                idx = np.where(cand.values)[0]
                take = []; last = -10 ** 9
                for i in idx:
                    if i - last >= h: take.append(i); last = i
                if len(take) < 15: continue
                pos = np.sign(xl1.values[take]); pnl = pos * fwd.values[take]
                tdays = day[take]
                for per, m in [("ALL", np.ones(len(take), bool)), ("H1", tdays < mid), ("H2", tdays >= mid)]:
                    p = pnl[m]
                    if len(p) < 10: continue
                    rows3.append(dict(stock=s, h=h, z=z, window=wn, period=per, n=len(p), gross_bps=1e4 * p.mean(),
                                      t=p.mean() / (p.std(ddof=1) / np.sqrt(len(p))), hit=(p > 0).mean(),
                                      net_3bps=1e4 * p.mean() - 3, net_8bps=1e4 * p.mean() - 8, net_15bps=1e4 * p.mean() - 15))
BT = pd.DataFrame(rows3); BT.to_csv(g.RES + "/t2_bt.csv", index=False)
# 5dk getiri oynaklığı (maliyet karşılaştırması için)
vol = pd.DataFrame({s: [1e4 * R[s][W["all"]].std(), 1e4 * R[s][W["USopen"]].std()] for s in SYMS}, index=["sd5m_all_bps", "sd5m_USopen_bps"]).T
vol.to_csv(g.RES + "/t2_vol.csv")
print("days", len(bdays), "ES days", len(alld), "mid", mid.date())
