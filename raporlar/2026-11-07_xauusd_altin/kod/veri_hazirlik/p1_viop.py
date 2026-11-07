"""VİOP bültenlerinden (filtreli) uzun tablo + XAUUSD/XAUTRY/XAGUSD/USDTRY/XU030 sürekli seriler.
Aktif kontrat: bir önceki iş günü açık pozisyonu en yüksek olan vade (ileriye bakma yok). Günlük getiri = aynı kontratın UZLASMA/ONCEKI_UZLASMA - 1."""
import glob, pandas as pd, numpy as np, sys
S = sys.argv[1]
cols = ["date","code","name","market","segment","itype","iclass","under","expiry","settle","prev_settle","chg_pct","open","low","high","close","vwap","value","premium","volume","trades","oi","oi_chg","os_price","os_value","os_prem","os_volume","os_trades"]
recs = []
for f in sorted(glob.glob(f"{S}/data/viop_f/viop_*.csv")):
    L = open(f).read().splitlines()[2:]
    for l in L:
        p = l.split(";")
        if len(p) < 23: continue
        p = (p + [""] * 28)[:28]
        recs.append(p)
df = pd.DataFrame(recs, columns=cols)
for c in cols[9:]:
    df[c] = pd.to_numeric(df[c].str.replace(",", "."), errors="coerce")
df["date"] = pd.to_datetime(df["date"]); df["expiry"] = pd.to_datetime(df["expiry"], errors="coerce")
df["root"] = df["code"].str.replace(r"^F_", "", regex=True).str.replace(r"\d{4}$", "", regex=True)
df.to_parquet(f"{S}/panel/viop_long.parquet")
print(df.groupby("root").size().sort_values(ascending=False).head(40))
def continuous(root):
    d = df[(df.root == root)].copy().sort_values(["date", "expiry"])
    by = {k: g.set_index("code") for k, g in d.groupby("date")}
    dates = sorted(by)
    out = []; oi_prev = None
    for t in dates:
        dt_ = by[t]
        if oi_prev is None or oi_prev.empty:
            act = dt_["volume"].idxmax()
        else:
            cand = oi_prev[oi_prev.index.isin(dt_.index)]
            act = cand.idxmax() if len(cand) and cand.max() > 0 else dt_["volume"].idxmax()
        r = dt_.loc[act]
        nxt = dt_[dt_.expiry > r.expiry].sort_values("expiry")
        out.append(dict(date=t, code=act, expiry=r.expiry, settle=r.settle, prev_settle=r.prev_settle,
                        ret=np.log(r.settle / r.prev_settle) if r.prev_settle and r.prev_settle > 0 and r.settle > 0 else np.nan,
                        close=r.close, open=r.open, high=r.high, low=r.low, vwap=r.vwap, volume=r.volume, trades=r.trades, oi=r.oi,
                        os_price=r.os_price, value=r.value,
                        tot_volume=dt_.volume.sum(), tot_oi=dt_.oi.sum(),
                        next_code=nxt.index[0] if len(nxt) else None, next_settle=nxt.settle.iloc[0] if len(nxt) else np.nan,
                        dte=(r.expiry - t).days))
        oi_prev = dt_["oi"]
    return pd.DataFrame(out).set_index("date")
for root in ["XAUUSD", "XAUTRYM", "XAGUSD", "USDTRY", "XU030", "EURUSD", "XAUTRY"]:
    if (df.root == root).any():
        c = continuous(root); c.to_parquet(f"{S}/panel/viop_{root}.parquet")
        print(root, c.index.min().date(), c.index.max().date(), len(c), "ret std", round(c.ret.std() * 100, 3), "zero-vol days", int((c.volume == 0).sum()))
