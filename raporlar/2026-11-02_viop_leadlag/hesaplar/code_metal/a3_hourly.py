"""A3: Saatlik veri ile kesin hizalama (2023-11+; TRALT/TRMET saatlik 2025-11-24+).
(1) Gece hareketi ayrıştırması: BIST günü t-1 kapanışı (15:00 UTC) -> sürücü
     post  = log(P_d(t-1, 22:30) / P_d(t-1, 15:00))   [BIST kapanışından ABD kapanışına]
     pre   = log(P_d(t, 06:55)  / P_d(t-1, 22:30))    [ABD kapanışından BIST açılışına (Asya seansı)]
     night = post + pre
   Hedef: gap_t, intra_t (ll.decomp), ayrıca intra_t'nin ilk saati (açılış->08:30 UTC bar sonu) ve geri kalanı.
(2) Saatlik lead-lag (gün-içi): BIST saatlik bar k getirisi vs sürücünün aynı bar ve bir önceki bar getirisi.
Çıktı: res/hourly_night.csv, res/hourly_leadlag.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mh, ll, pandas as pd, numpy as np

DRV = ["GC=F", "SI=F", "HG=F", "ALI=F", "HRC=F", "TRY=X", "MT", "NUE", "STLD", "CLF", "CMC", "SLX", "VALE", "BHP", "RIO", "TKA.DE", "SZG.DE", "VOE.VI",
       "TS", "TEN.MI", "OIH", "CL=F", "GDX", "GDXJ", "NEM", "AEM", "B", "KGC", "SSRM", "EGO", "PKX", "FMG.AX", "AUDUSD=X", "ES=F", "FXI", "ASHR"]

def bist_days(stock):
    d = mh.D(stock).dropna(subset=["intra"]); return d

EU = (".DE", ".VI", ".MI", ".AS", ".PA", ".L", ".ST", ".HE", ".SW", ".OL")
def night_table(drv):
    """24 saat işlem gören vadeli/FX: post (15:00->22:30) + pre (22:30->06:55). Hisse/ETF: sadece post (yerel kapanışa kadar), pre=0."""
    p15 = ll.snap_daily(drv, "15:00")
    if "=" in drv:
        pUS = ll.snap_daily(drv, "22:30"); p07 = ll.snap_daily(drv, "06:55")
    else:
        pUS = ll.snap_daily(drv, "17:00" if drv.endswith(EU) else "22:30"); p07 = None
    return p15, pUS, p07

def first_hour_split(stock):
    """BIST saatlik: açılış (daily o) -> 07:30 UTC bar sonu (06:30 barının kapanışı), ve 07:30 -> kapanış."""
    h = ll.raw(stock + ".IS", "h1")
    s = h["c"].copy(); s.index = s.index  # bar başlangıcı
    c0630 = s[(s.index.hour == 6) & (s.index.minute == 30)]
    c0630.index = c0630.index.tz_convert(None).normalize()
    dd = ll.raw(stock + ".IS"); dd = dd.set_index(pd.DatetimeIndex(dd["ldate"].values))
    o = dd["o"]; c = dd["c"]
    df = pd.DataFrame({"o": o, "c": c, "h1": c0630}).dropna()
    df["first"] = np.log(df["h1"] / df["o"]); df["rest"] = np.log(df["c"] / df["h1"])
    return df[["first", "rest"]]

if __name__ == "__main__":
    rows = []
    cache = {d: night_table(d) for d in DRV}
    for s in mh.STOCKS:
        dd = bist_days(s); dd = dd[dd.index >= "2023-11-01"]
        try: fh = first_hour_split(s)
        except Exception: fh = pd.DataFrame(columns=["first", "rest"])
        days = dd.index
        prev = pd.Series(days[:-1], index=days[1:])
        for d in DRV:
            p15, pUS, p07 = cache[d]
            tp = prev.values; t = prev.index
            a15 = p15.reindex(tp).values; aUS = pUS.reindex(tp).values; a07 = p07.reindex(t).values if p07 is not None else aUS
            X = pd.DataFrame({"post": np.log(aUS / a15), "pre": np.log(a07 / aUS), "night": np.log(a07 / a15)}, index=t)
            Y = dd[["gap", "intra"]].join(fh, how="left")
            xg = mh.D("XU100").reindex(Y.index)
            Y["gap_res"] = Y["gap"] - np.polyfit(*pd.concat([xg["gap"], Y["gap"]], axis=1).dropna().values.T[::1], 1)[0] * xg["gap"]
            Y["intra_res"] = Y["intra"] - np.polyfit(*pd.concat([xg["intra"], Y["intra"]], axis=1).dropna().values.T[::1], 1)[0] * xg["intra"]
            for xc in ["post", "pre", "night"]:
                for yc in ["gap", "intra", "first", "rest", "gap_res", "intra_res"]:
                    c, tt, n = mh.corr_t(Y[yc], X[xc])
                    rows.append({"stock": s, "driver": d, "x": xc, "y": yc, "corr": c, "t": tt, "n": n})
    N = pd.DataFrame(rows); N.to_csv(os.path.join(mh.RES, "hourly_night.csv"), index=False)
    # (2) saatlik gün-içi lead-lag: BIST bar sonu zamanlarında sürücü fiyatı (asof), aynı pencere getirileri
    rows = []
    for s in mh.STOCKS:
        h = ll.raw(s + ".IS", "h1"); st_ = h.index
        e = st_ + pd.Timedelta(minutes=60)
        e = e.where(~((st_.hour == 14) & (st_.minute == 30)), st_ + pd.Timedelta(minutes=30))
        e = e.where(~((st_.hour == 15) & (st_.minute == 0)), st_ + pd.Timedelta(minutes=10))
        bs = pd.Series(h["c"].values, index=e).sort_index(); bs = bs[~bs.index.duplicated()]
        day = bs.index.tz_convert(None).normalize()
        rs = np.log(bs).groupby(day).diff()
        for d in DRV:
            try: hd = ll.raw(d, "h1")
            except Exception: continue
            ds = pd.Series(hd["c"].values, index=hd.index + pd.Timedelta(minutes=60)).sort_index(); ds = ds[~ds.index.duplicated()]
            lastt = pd.Series(ds.index, index=ds.index)
            pa = ds.reindex(ds.index.union(bs.index)).ffill().reindex(bs.index)
            ta = lastt.reindex(lastt.index.union(bs.index)).ffill().reindex(bs.index)
            pa[(bs.index - pd.DatetimeIndex(ta.values).tz_localize("UTC") if pd.DatetimeIndex(ta.values).tz is None else bs.index - pd.DatetimeIndex(ta.values)) > pd.Timedelta(hours=2)] = np.nan
            rd = np.log(pa).groupby(day).diff(); rd = rd.where(rd != 0)
            rdl = rd.groupby(day).shift(1); rsl = rs.groupby(day).shift(1)
            c0, t0, n0 = mh.corr_t(rs, rd); c1, t1, n1 = mh.corr_t(rs, rdl); cr, tr, nr = mh.corr_t(rd, rsl)
            rows.append({"stock": s, "driver": d, "c_sync": c0, "t_sync": t0, "c_lead1h": c1, "t_lead1h": t1, "n_lead": n1, "c_rev1h": cr, "t_rev1h": tr, "n": n0})
    L = pd.DataFrame(rows); L.to_csv(os.path.join(mh.RES, "hourly_leadlag.csv"), index=False)
    print("night rows", len(N), "leadlag rows", len(L))
