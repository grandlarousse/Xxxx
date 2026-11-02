"""A8: tamamlayıcı analizler (önceki raporda 'yapılmadı' olanlar).
(1) 250g kayan korelasyon istatistikleri (XU100 artıkları) — ana çiftler.
(2) Gap-fade gerçekçi dolum: açılış yerine ilk saatlik bar kapanışında (07:30 UTC) / ikinci bar (08:30 UTC) giriş (h1, 2023-11+).
(3) Saatlik küme-içi öncülük: x_{h-1} -> y_h aynı gün içinde (çimento, gübre, taahhüt kümeleri), XU100 saatlik kontrollü; BH-FDR.
(4) Saatlik testlere (a6) BH-FDR.
(5) HEKTS bireysel yatırımcı vekili: anormal hacim x önceki gün getirisi -> ertesi gün (momentum hacimde mi yoğunlaşıyor?), tavan/taban sonrası.
(6) OYAK'ın Tekfen'i devralması (KAP 09.06.2026 görüşme, 24.07.2026 devir): olay CAR + TKFEN-OYAKC/HEKTS korelasyon rejimi.
(7) Backtest yıllık kırılım özeti (res_bt_years / res_selfbt).
Çıktı: res_extra_*.csv"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kc import *
from kc import _corr
HERE = os.path.dirname(os.path.abspath(__file__))
m = R("XU100")
pd.set_option("display.width", 250)

# (1) kayan korelasyon
PAIRS = [("CIMSA", "OYAKC"), ("CIMSA", "AKCNS.IS"), ("GUBRF", "BAGFS.IS"), ("GUBRF", "HEKTS"), ("TKFEN", "ENKAI"), ("SISE", "XBANK"), ("HEKTS", "OYAKC"),
         ("GUBRF", "CF"), ("SISE", "SGO.PA"), ("CIMSA", "HEI.DE"), ("SISE", "TTF=F"), ("SISE", "TRY=X"), ("TKFEN", "OYAKC"), ("TKFEN", "HEKTS")]
rr = []
for a, b in PAIRS:
    ra = resid(R(a), [m]); rb = resid(R(b), [m])
    rc = rolling_corr = pd.concat([ra, rb], axis=1).dropna()
    rc = rc[rc.index >= "2010-01-01"]
    x = rc.iloc[:, 0].rolling(250).corr(rc.iloc[:, 1]).dropna()
    raw = pd.concat([R(a), R(b)], axis=1).dropna(); raw = raw[raw.index >= "2010-01-01"]
    xr = raw.iloc[:, 0].rolling(250).corr(raw.iloc[:, 1]).dropna()
    rr.append({"stock": a, "driver": b, "pc250_min": x.min(), "pc250_med": x.median(), "pc250_max": x.max(), "pc250_frac_pos": (x > 0).mean(), "pc250_last": x.iloc[-1],
               "c250_min": xr.min(), "c250_med": xr.median(), "c250_max": xr.max(), "c250_last": xr.iloc[-1]})
RR = pd.DataFrame(rr); RR.to_csv(os.path.join(HERE, "res_extra_rolling.csv"), index=False)
print("== (1) 250g kayan (XU100 artığı pc ve ham c)"); print(RR.round(2).to_string(index=False))


# (2) gap-fade gecikmeli giriş
def h1px(sym, hhmm):
    d = ll.intraday(ll.T(sym), "h1"); d = d.copy(); d["d"] = d.index.tz_convert(None).normalize()
    h, mi = map(int, hhmm.split(":"))
    x = d[(d.index.hour == h) & (d.index.minute == mi)]
    return x.set_index("d")["c"]


gf = []
for s in ["CIMSA", "OYAKC", "GUBRF", "HEKTS", "TKFEN", "SISE", "AKCNS.IS", "NUHCM.IS", "AFYON.IS"]:
    dd = DEC(s); dl = ll.daily(ll.T(s), field="c", on_bist_cal=False)
    o = ll.raw(ll.T(s)).copy(); o.index = pd.DatetimeIndex(o["ldate"].values); o = o[~o.index.duplicated(keep="last")]
    gap = dd["gap"]
    for lab, hh in [("open", None), ("0730UTC", "06:30"), ("0830UTC", "07:30")]:
        if hh is None:
            tgt = dd["intra"]
        else:
            p = h1px(s, hh); tgt = np.log(dl.reindex(p.index) / p)
        df = pd.concat([gap.rename("g"), tgt.rename("y")], axis=1).dropna(); df = df[df.index >= "2023-12-01"]
        for thr in [0.01, 0.02]:
            pos = -np.sign(df.g).where(df.g.abs() > thr, 0.0)
            for cost in [0, 10, 15]:
                pnl = pos * df.y - cost / 1e4 * pos.abs(); act = pos != 0
                if act.sum() < 20: continue
                mm, t, _ = ll.nw_t(pnl[act])
                gf.append({"stock": s, "entry": lab, "thr": thr, "cost": cost, "n": int(act.sum()), "mean_bps": 1e4 * mm, "t": t, "hit": float((pnl[act] > 0).mean())})
GF = pd.DataFrame(gf); GF.to_csv(os.path.join(HERE, "res_extra_gapfade_h1.csv"), index=False)
print("== (2) gap-fade 2023-12+ (|gap|>1%), 10bps"); print(GF[(GF.cost == 10) & (GF.thr == 0.01)].pivot(index="stock", columns="entry", values="mean_bps").round(1).join(
    GF[(GF.cost == 10) & (GF.thr == 0.01)].pivot(index="stock", columns="entry", values="t").round(1).add_suffix("_t")).join(
    GF[(GF.cost == 10) & (GF.thr == 0.01) & (GF.entry == "open")].set_index("stock").n).to_string())

# (3) saatlik küme-içi öncülük
CL = {"cimento": ["CIMSA", "OYAKC", "AKCNS.IS", "NUHCM.IS", "AFYON.IS"], "gubre": ["GUBRF", "HEKTS", "BAGFS.IS", "EGGUB.IS"], "taahhut": ["TKFEN", "ENKAI"],
      "oyak": ["TKFEN", "HEKTS", "OYAKC"]}


def hret(sym):
    d = ll.intraday(ll.T(sym), "h1").copy()
    d = d[(d.index.hour * 100 + d.index.minute).isin([630, 730, 830, 930, 1030, 1130, 1230, 1330])]
    r = np.log(d["c"] / d["o"])  # bar-içi getiri (gece boşluğu yok)
    r[r.abs() > 0.08] = np.nan
    return r


XH = hret("XU100.IS")
hl = []
for cl, mem in CL.items():
    for y in mem:
        for x in mem:
            if x == y: continue
            ry = hret(y); rx = hret(x)
            df = pd.concat([ry.rename("y"), rx.rename("x"), XH.rename("m")], axis=1)
            df["d"] = df.index.tz_convert(None).normalize()
            df["xl"] = df.groupby("d")["x"].shift(1); df["ml"] = df.groupby("d")["m"].shift(1)
            df = df.dropna()
            if len(df) < 500: continue
            c = df.y.corr(df.xl); t = nwt_corr(df.y, df.xl)
            p_, _ = pc(df.y, df.xl, [df.m, df.ml])
            # backtest: x_{h-1} işareti -> y_h, |x|>0.5%
            pos = np.sign(df.xl).where(df.xl.abs() > 0.005, 0.0); pnl = pos * df.y; act = pos != 0
            mm = 1e4 * pnl[act].mean() if act.sum() > 20 else np.nan
            hl.append({"cluster": cl, "stock": y, "leader": x, "c": c, "t": t, "pc_xu": p_, "n": len(df), "bt_gross_bps": mm, "bt_n": int(act.sum())})
HL = pd.DataFrame(hl).drop_duplicates(["stock", "leader"])
HL["p"] = ll.t_to_p(HL.t); HL["fdr"] = ll.fdr(HL.p.values)[0]
HL.to_csv(os.path.join(HERE, "res_extra_hourly_leadlag.csv"), index=False)
print("== (3) saatlik küme-içi öncülük (x_{h-1} -> y_h), test sayısı", len(HL)); print(HL.sort_values("t", key=abs, ascending=False).round(3).head(14).to_string(index=False))

# (4) a6 saatlik testlere FDR
I = pd.read_csv(os.path.join(HERE, "res_intraday.csv"))
tc = [c for c in ["t_sync_snap", "t_after_gap1", "t_after_intra1"] if c in I]
ts = I[tc].values.ravel(); ok = ~np.isnan(ts)
rej = np.zeros(len(ts), bool); rej[ok] = ll.fdr(ll.t_to_p(ts[ok]))[0]
I_f = pd.DataFrame(rej.reshape(len(I), len(tc)), columns=[c + "_fdr" for c in tc]); I2 = pd.concat([I, I_f], axis=1)
I2.to_csv(os.path.join(HERE, "res_intraday_fdr.csv"), index=False)
print("== (4) a6 FDR: test sayısı", int(ok.sum())); print(I2[I2.c_sync_snap.notna()][["stock", "driver", "t_sync_snap", "t_sync_snap_fdr", "t_after_intra1", "t_after_intra1_fdr"]].round(2).to_string(index=False))

# (5) HEKTS bireysel vekili: anormal hacim
hv = []
for s in STOCKS:
    d = ll.raw(ll.T(s)).copy(); d.index = pd.DatetimeIndex(d["ldate"].values); d = d[~d.index.duplicated(keep="last")]
    v = (d["v"] * d["c"]).replace(0, np.nan)  # TL hacim
    av = np.log(v / v.rolling(20).mean().shift(1))
    r = R(s); dd = DEC(s)
    df = pd.concat([r.rename("r"), r.shift(1).rename("rl"), av.shift(1).rename("avl"), dd["intra"].rename("intra")], axis=1).dropna()
    df = df[df.index >= "2014-01-01"]
    q = df.avl.rank(pct=True)
    for lab, msk in [("hacim_düşük", q < 1 / 3), ("hacim_orta", (q >= 1 / 3) & (q < 2 / 3)), ("hacim_yüksek", q >= 2 / 3)]:
        x = df[msk]
        mm, t, n = ll.nw_t(np.sign(x.rl) * x.r)
        hv.append({"stock": s, "bucket": lab, "mom_bps": 1e4 * mm, "t": t, "n": n, "ac1": x.r.corr(x.rl)})
    lim = df[df.rl.abs() > 0.095]
    mm, t, n = ll.nw_t(np.sign(lim.rl) * lim.r)
    hv.append({"stock": s, "bucket": "tavan/taban_ertesi(cc)", "mom_bps": 1e4 * mm, "t": t, "n": n, "ac1": np.nan})
    mm, t, n = ll.nw_t(np.sign(lim.rl) * lim.intra)
    hv.append({"stock": s, "bucket": "tavan/taban_ertesi(intra)", "mom_bps": 1e4 * mm, "t": t, "n": n, "ac1": np.nan})
HV = pd.DataFrame(hv); HV.to_csv(os.path.join(HERE, "res_extra_volume.csv"), index=False)
print("== (5) momentum (sign r_{t-1} * r_t, brüt bps) hacim tercillerine göre"); print(HV.pivot(index="stock", columns="bucket", values="mom_bps").round(1).join(HV.pivot(index="stock", columns="bucket", values="t").round(1).add_suffix("_t")).to_string())

# (6) OYAK-Tekfen
def car(stock, date, win=(0, 5), est=(-250, -20)):  # a5_events.car ile aynı (import yan etkisinden kaçınmak için kopya)
    df = pd.concat([R(stock).rename("a"), m.rename("m")], axis=1).dropna()
    pos = df.index.searchsorted(pd.Timestamp(date))
    if pos >= len(df): return np.nan, np.nan
    e = df.iloc[max(0, pos + est[0]):pos + est[1]]
    b, a0 = np.polyfit(e.m, e.a, 1)
    ar = df.a - (a0 + b * df.m); sd = ar.iloc[max(0, pos + est[0]):pos + est[1]].std()
    w = ar.iloc[pos + win[0]:pos + win[1] + 1]
    return float(w.sum()), float(w.sum() / (sd * np.sqrt(len(w))))


ev = []
for d, lab in [("2026-06-10", "OYAK görüşme KAP (09.06 18:59)"), ("2026-07-27", "Pay devri tamam KAP (24.07 Cuma 20:28)")]:
    for s in ["TKFEN", "HEKTS", "OYAKC", "ENKAI", "GUBRF"]:
        for w in [(0, 0), (0, 2), (0, 10)]:
            c, z = car(s, d, w); ev.append({"event": lab, "stock": s, "win": str(w), "CAR_pct": 100 * c, "z": z})
EVT = pd.DataFrame(ev); EVT.to_csv(os.path.join(HERE, "res_extra_oyak_tekfen.csv"), index=False)
print("== (6) OYAK-Tekfen olayı"); print(EVT.pivot_table(index=["event", "stock"], columns="win", values=["CAR_pct", "z"]).round(1).to_string())
for a, b in [("TKFEN", "OYAKC"), ("TKFEN", "HEKTS"), ("TKFEN", "ENKAI"), ("TKFEN", "GUBRF")]:
    pre, n1 = pc(R(a), R(b), [m], "2025-06-01", "2026-06-10", min_n=40); post, n2 = pc(R(a), R(b), [m], "2026-06-10", None, min_n=40)
    print(f"  {a}-{b}: pc 2025-06..2026-06-09 = {pre:+.2f} (n{n1}) | 2026-06-10.. = {post:+.2f} (n{n2})")

# (7) backtest yıllık kırılım özeti
Y = pd.read_csv(os.path.join(HERE, "res_bt_years.csv")).set_index("spec")
yrs = [c for c in Y.columns]
iscols = [c for c in yrs if int(float(c)) < 2021]; oocols = [c for c in yrs if int(float(c)) >= 2021]
Ysum = pd.DataFrame({"IS_pos_years": (Y[iscols] > 0).sum(1), "IS_years": Y[iscols].notna().sum(1), "OOS_pos_years": (Y[oocols] > 0).sum(1), "OOS_years": Y[oocols].notna().sum(1)})
Ysum.to_csv(os.path.join(HERE, "res_extra_bt_years_summary.csv"))
print("== (7) backtest (10bps net) pozitif yıl sayısı"); print(Ysum.to_string())
