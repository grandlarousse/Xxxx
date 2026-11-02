"""A6: Ek analizler (tam kapsam).
 A. FMG.AX (ASX kapanışı 05-06 UTC, BIST açılışından önce) lag0 -> BIST gün-içi: bağımsız kontrol + artımsal regresyon
 B. SHFE HC/RB, DCE I: KENDİ roll'suz serim (her gün açık pozisyonu en yüksek kontrat; getiri = t-1'de baskın kontratın kendi getirisi)
    Zamanlama: SHFE gün seansı 15:00 Pekin = 07:00 UTC kapanır = BIST sürekli işlem açılışı (sınırda işlenebilir). lag1 versiyonu da.
 C. TIO=F ay-sonu sorunu (aylık ortalama kontrat): ayın iş günü kovalarına göre oynaklık ve korelasyon
 D. Aylık frekans: illikit HRC=F/BUS=F ve BRSAN-boru sürücüleri
 E. SSRM/EGO Türkiye faktörü + TRALT ile ortak 'Türk altın madencisi' faktörü; Çöpler olayı
 F. BRSAN/EREGL Section 232 olayları
 G. m5 ile 30 dakikalık TAM hizalı gün-içi lead-lag (h1 :30/:00 artefaktını düzeltir)
 H. Saatlik gece altın sinyali ile TRALT backtestleri (2024-06+)
Çıktılar res/x*.csv"""
import sys, os, glob, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mh, ll, pandas as pd, numpy as np
import statsmodels.api as sm
SINA = os.path.join(mh.SCR, "data_cin", "sina")
OUTP = lambda n: os.path.join(mh.RES, n)

def nz(r): return r.where(r != 0)
def btsum(sig, tgt, label, modes=(("sign", 0.0), ("z", 1.0)), costs=(8, 15)):
    rows = []
    for mode, thr in modes:
        for c in costs:
            res, pnl = ll.backtest(sig.reindex(tgt.index), tgt, cost_bps=c, mode=mode, thr=thr)
            r = {"test": label, "mode": f"{mode}{thr}", "cost": c}
            for k in ("IS", "OOS", "ALL"):
                for f in ("n", "mean_bps", "t", "sharpe", "hit"): r[f"{k}_{f}"] = res[k].get(f, np.nan)
            yb = res["by_year_bps"]; r["yrs_pos"] = f"{sum(v > 0 for v in yb.values())}/{len(yb)}"; r["by_year"] = ";".join(f"{k}:{v}" for k, v in yb.items())
            rows.append(r)
    return rows
def hedged(stock):
    a = mh.D(stock)["intra"]; m = mh.D("XU100")["intra"]
    df = pd.concat([a, m], axis=1).dropna(); b = np.polyfit(df.iloc[:, 1], df.iloc[:, 0], 1)[0]
    return a - b * m
def lead_row(stock, sig, name):
    d = mh.D(stock); i = d["intra"]; g = d["gap"]
    c, t, n = mh.corr_t(i, sig); cI, tI, _ = mh.corr_t(i[i.index < mh.SPLIT], sig); cO, tO, _ = mh.corr_t(i[i.index >= mh.SPLIT], sig)
    cg, tg, _ = mh.corr_t(g, sig); ch, th, _ = mh.corr_t(hedged(stock) if stock != "XU100" else i, sig)
    df = pd.concat([i.rename("i"), sig.rename("s")], axis=1).dropna()
    yr = df.groupby(df.index.year).apply(lambda x: x["i"].corr(x["s"]) if len(x) > 40 else np.nan).dropna()
    return {"stock": stock, "signal": name, "c_intra": c, "t_intra": t, "n": n, "t_IS": tI, "t_OOS": tO, "c_IS": cI, "c_OOS": cO, "c_gap": cg, "t_gap": tg,
            "c_hedged": ch, "t_hedged": th, "yr_pos_share": float((yr > 0).mean()), "yr": ";".join(f"{k}:{v:.2f}" for k, v in yr.items())}

# ---------- B: SHFE/DCE kendi serim ----------
def dominant_ret(code):
    C, P = {}, {}
    for f in sorted(glob.glob(os.path.join(SINA, f"{code}[0-9][0-9][0-9][0-9].json"))):
        nm = os.path.basename(f)[:-5]; d = pd.DataFrame(json.load(open(f)))
        if not len(d): continue
        d.index = pd.to_datetime(d["d"]); d = d[~d.index.duplicated(keep="last")]
        C[nm] = pd.to_numeric(d["c"], errors="coerce"); P[nm] = pd.to_numeric(d["p"], errors="coerce")
    C = pd.DataFrame(C).sort_index(); P = pd.DataFrame(P).sort_index()
    C = C.where(C > 0); dom = P.fillna(-1).idxmax(axis=1)
    lr = np.log(C).diff()
    domprev = dom.shift(1)
    r = pd.Series([lr.at[t, k] if isinstance(k, str) else np.nan for t, k in zip(lr.index, domprev)], index=lr.index)
    return r.dropna(), dom

def to_bist(r_local):
    """yerel tarih t getirisi -> BIST günü t (yerel tarihi <= t olan son kapanış). Çin tatillerinde birikmiş getiri ilk açılış gününe."""
    cal = ll.bist_cal(); lvl = np.exp(r_local.cumsum())
    s = lvl.reindex(lvl.index.union(cal)).ffill().reindex(cal)
    return nz(np.log(s).diff())

if __name__ == "__main__":
    LEAD, BT = [], []
    # A. FMG.AX
    fmg = nz(mh.R("FMG.AX"))
    for st in ["EREGL", "KRDMD", "BRSAN", "TRALT", "TRMET", "XU100"]:
        LEAD.append(lead_row(st, fmg, "FMG.AX lag0"))
    for st in ["EREGL", "KRDMD", "BRSAN"]:
        BT += btsum(fmg, mh.D(st)["intra"], f"A FMG.AX(t) -> {st} intra"); BT += btsum(fmg, hedged(st), f"A FMG.AX(t) -> {st} intra hedged")
    # artımsal regresyon: intra_t ~ FMG_t + SLX_{t-1} + ES_{t-1} + MT.AS_{t-1} + gap_t
    REG = []
    for st in ["EREGL", "KRDMD", "BRSAN"]:
        d = mh.D(st)
        X = pd.concat([fmg.rename("FMG_t"), nz(mh.R("SLX")).shift(1).rename("SLX_t1"), nz(mh.R("ES=F")).shift(1).rename("ES_t1"),
                       nz(mh.R("MT.AS")).shift(1).rename("MTAS_t1"), d["gap"].rename("gap_t")], axis=1)
        df = pd.concat([d["intra"].rename("y"), X], axis=1).dropna(); df = (df - df.mean()) / df.std()
        m = sm.OLS(df["y"], sm.add_constant(df.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
        REG.append({"stock": st, **{f"b_{k}": v for k, v in m.params.items()}, **{f"t_{k}": v for k, v in m.tvalues.items()}, "n": int(m.nobs)})
    # B. SHFE/DCE
    for code, nm in [("HC", "SHFE HRC"), ("RB", "SHFE inşaat demiri"), ("I", "DCE demir cevheri")]:
        try:
            rl, dom = dominant_ret(code)
        except Exception as e:
            print("SINA ERR", code, e); continue
        rb = to_bist(rl)
        pd.DataFrame({"r": rl, "dom": dom.reindex(rl.index)}).to_csv(OUTP(f"x_{code}_dominant.csv"))
        for st in ["EREGL", "KRDMD", "BRSAN", "XU100"]:
            LEAD.append(lead_row(st, rb, f"{nm} lag0 (07:00 UTC, sınırda)")); LEAD.append(lead_row(st, rb.shift(1), f"{nm} lag1"))
        for st in ["EREGL", "KRDMD"]:
            BT += btsum(rb, mh.D(st)["intra"], f"B {nm}(t) -> {st} intra"); BT += btsum(rb, hedged(st), f"B {nm}(t) -> {st} intra hedged")
        # senkron/haftalık
        for st in ["EREGL", "KRDMD"]:
            a = mh.R(st); c, t, n = mh.corr_t(a, rb); pc, _ = ll.partial_corr(a, rb, [mh.R("XU100")])
            wa, wb = mh.weekly(a), mh.weekly(rb); cw, _, _ = mh.corr_t(wa, wb); pcw, _ = ll.partial_corr(wa, wb, [mh.weekly(mh.R("XU100"))])
            REG.append({"stock": st, "signal": nm + " sync", "c": c, "pc": pc, "cw": cw, "pcw": pcw, "n": n})
    # FMG + SHFE birlikte (hangisi baskın?)
    try:
        hc = to_bist(dominant_ret("HC")[0])
        for st in ["EREGL", "KRDMD"]:
            d = mh.D(st)
            df = pd.concat([d["intra"].rename("y"), fmg.rename("FMG_t"), hc.rename("HC_t"), d["gap"].rename("gap_t")], axis=1).dropna(); df = (df - df.mean()) / df.std()
            m = sm.OLS(df["y"], sm.add_constant(df.drop(columns="y"))).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
            REG.append({"stock": st, "signal": "FMG+HC birlikte", **{f"b_{k}": v for k, v in m.params.items()}, **{f"t_{k}": v for k, v in m.tvalues.items()}, "n": int(m.nobs)})
        cmb = pd.concat([mh.R("FMG.AX").pipe(nz).pipe(lambda x: (x - x.rolling(250, min_periods=60).mean().shift(1)) / x.rolling(250, min_periods=60).std().shift(1)),
                         hc.pipe(lambda x: (x - x.rolling(250, min_periods=60).mean().shift(1)) / x.rolling(250, min_periods=60).std().shift(1))], axis=1).mean(axis=1)
        for st in ["EREGL", "KRDMD"]:
            BT += btsum(cmb, mh.D(st)["intra"], f"B2 FMG+SHFE HRC z-ort(t) -> {st} intra")
    except Exception as e: print("cmb err", e)
    pd.DataFrame(LEAD).to_csv(OUTP("x_lead.csv"), index=False); pd.DataFrame(REG).to_csv(OUTP("x_reg.csv"), index=False)
    # C. TIO=F ay-sonu
    tio = nz(ll.ret("TIO=F", on_bist_cal=False)); vale = nz(ll.ret("VALE", on_bist_cal=False)); fm = nz(ll.ret("FMG.AX", on_bist_cal=False))
    df = pd.concat([tio.rename("tio"), vale.rename("vale"), fm.shift(-1).rename("fmg_next")], axis=1).dropna(subset=["tio"])
    bdm = df.groupby([df.index.year, df.index.month]).cumcount() + 1; nmo = df.groupby([df.index.year, df.index.month])["tio"].transform("size")
    left = nmo - bdm
    df["kova"] = np.select([bdm <= 2, left <= 2, left <= 6], ["ay ilk 2 gün (roll)", "ay son 3 gün", "ay son 4-7 gün"], "ay ortası")
    er = mh.R("EREGL"); df["eregl_next"] = er.reindex(df.index + pd.Timedelta(days=1)).values  # yaklaşık: ertesi takvim günü BIST
    C = df.groupby("kova").apply(lambda x: pd.Series({"n": len(x), "sd_bps": 1e4 * x["tio"].std(), "corr_vale": x["tio"].corr(x["vale"]), "corr_fmg_next": x["tio"].corr(x["fmg_next"]),
                                                       "abs_gt_4sd": float((x["tio"].abs() > 4 * df["tio"].std()).mean())}))
    C.to_csv(OUTP("x_tio_month.csv"))
    # D. Aylık
    def mon(r): return r.resample("ME").sum(min_count=5)
    MON = []
    drvs = ["HRC=F", "BUS=F", "TIO=F", "HG=F", "ALI=F", "GC=F", "SI=F", "TS", "OIH", "XOP", "CL=F", "NUE", "STLD", "CMC", "MT.AS", "SLX", "VALE", "FMG.AX", "TRY=X", "^GSPC"]
    xm = mon(mh.R("XU100")); xmu = mon(mh.R("XU100", usd=True))
    for st in mh.STOCKS:
        for usd in (False, True):
            a = mon(mh.R(st, usd=usd)); ctrl = xmu if usd else xm
            for d in drvs + ["ONS_TL"]:
                b = mon(mh.onsTL()) if d == "ONS_TL" else mon(mh.R(d))
                x = pd.concat([a.rename("a"), b.rename("b"), ctrl.rename("m")], axis=1).dropna(); x = x[x.index >= "2008-01-01"]
                if len(x) < 36: continue
                c = x["a"].corr(x["b"]); pc, _ = ll.partial_corr(x["a"], x["b"], [x["m"]])
                cI = x[x.index < mh.SPLIT]; cO = x[x.index >= mh.SPLIT]
                MON.append({"stock": st, "usd": usd, "driver": d, "c_m": c, "pc_m": pc, "t_pc": pc * np.sqrt((len(x) - 3) / (1 - pc ** 2)), "n_m": len(x),
                            "c_IS": cI["a"].corr(cI["b"]), "c_OOS": cO["a"].corr(cO["b"]), "beta_m": np.cov(x["a"], x["b"])[0, 1] / x["b"].var()})
    pd.DataFrame(MON).to_csv(OUTP("x_monthly.csv"), index=False)
    # E. SSRM/EGO Türkiye faktörü (ABD seansı senkron, günlük) + TRALT ile haftalık ortak faktör
    EF = []
    for s in ["EGO", "SSRM", "NEM", "AEM", "KGC"]:
        df = pd.concat([nz(mh.R(s)).rename("y"), nz(mh.R("GDX")).rename("GDX"), nz(mh.R("TUR")).rename("TUR"), nz(mh.R("^GSPC")).rename("SPX")], axis=1).dropna()
        for lab, x in [("ALL", df), ("IS", df[df.index < mh.SPLIT]), ("OOS", df[df.index >= mh.SPLIT])]:
            m = sm.OLS(x["y"], sm.add_constant(x[["GDX", "TUR", "SPX"]])).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
            EF.append({"stock": s, "sample": lab, "b_GDX": m.params["GDX"], "b_TUR": m.params["TUR"], "t_TUR": m.tvalues["TUR"], "n": int(m.nobs)})
    w = lambda s: mh.weekly(s)
    for s in ["EGO", "SSRM", "NEM"]:
        a = w(mh.R("TRALT", usd=True)); b = w(nz(mh.R(s)))
        pc, n = ll.partial_corr(a, b, [w(nz(mh.R("GC=F"))), w(mh.R("XU100", usd=True))])
        pc2, _ = ll.partial_corr(a, b, [w(nz(mh.R("GC=F"))), w(mh.R("XU100", usd=True)), w(nz(mh.R("GDX")))])
        EF.append({"stock": "TRALT(USD,haftalık)", "sample": f"pc vs {s} | GC,XU100usd", "b_GDX": pc, "b_TUR": pc2, "t_TUR": pc2 * np.sqrt((n - 5) / (1 - pc2 ** 2)), "n": n})
    pd.DataFrame(EF).to_csv(OUTP("x_turkey_miners.csv"), index=False)
    # E2/F. Olaylar
    EVS = [("Çöpler heyelanı (SSRM)", "2024-02-13", ["TRALT", "TRMET", "SSRM", "EGO"]),
           ("ABD 232 çelik vergisi duyurusu", "2018-03-01", ["BRSAN", "EREGL", "KRDMD"]), ("ABD Türkiye çeliği %50 (kur krizi)", "2018-08-10", ["BRSAN", "EREGL", "KRDMD"]),
           ("ABD Türkiye çeliği %25'e indi", "2019-05-16", ["BRSAN", "EREGL", "KRDMD"]), ("ABD seçimi (Trump)", "2024-11-06", ["BRSAN", "EREGL", "KRDMD"]),
           ("232 muafiyetleri kaldırıldı %25", "2025-02-10", ["BRSAN", "EREGL", "KRDMD"]), ("232 %50'ye çıktı", "2025-06-02", ["BRSAN", "EREGL", "KRDMD"])]
    ER = []
    for ev, dt, sts in EVS:
        for st in sts:
            a = mh.R(st); bench = mh.R("XU100") if ll.is_bist(ll.T(st)) else nz(mh.R("GDX"))
            ab = (a - bench).dropna(); i0 = ab.index.searchsorted(pd.Timestamp(dt))
            if i0 >= len(ab) or i0 < 260: continue
            sd = ab.iloc[i0 - 260:i0 - 10].std()
            w1 = ab.iloc[i0 - 1:i0 + 2].sum(); w10 = ab.iloc[i0:i0 + 11].sum()
            ER.append({"event": ev, "date": str(ab.index[i0].date()), "stock": st, "bench": "XU100" if ll.is_bist(ll.T(st)) else "GDX", "car_m1p1_pct": 100 * w1, "car_0_10_pct": 100 * w10,
                       "z_m1p1": w1 / (sd * np.sqrt(3)), "z_0_10": w10 / (sd * np.sqrt(11))})
    pd.DataFrame(ER).to_csv(OUTP("x_events2.csv"), index=False)
    # G. m5 30-dk tam hizalı gün-içi lead-lag
    def grid30(sym):
        d = ll.raw(sym, "m5"); s = pd.Series(d["c"].values, index=d.index + pd.Timedelta(minutes=5)).sort_index(); s = s[~s.index.duplicated()]
        days = s.index.normalize().unique(); G = []
        for dd in days:
            G.append(pd.date_range(dd + pd.Timedelta(hours=7), dd + pd.Timedelta(hours=15), freq="30min"))
        g = G[0].append(G[1:]) if len(G) > 1 else G[0]
        lastt = pd.Series(s.index, index=s.index)
        px = s.reindex(s.index.union(g)).ffill().reindex(g); tt = lastt.reindex(lastt.index.union(g)).ffill().reindex(g)
        px[(g - pd.DatetimeIndex(tt.values).tz_localize("UTC")) > pd.Timedelta(minutes=30)] = np.nan
        return px
    GL = []
    pairs = [("TRALT.IS", "GC=F"), ("TRALT.IS", "SI=F"), ("TRMET.IS", "GC=F"), ("EREGL.IS", "TKA.DE"), ("EREGL.IS", "SZG.DE"), ("EREGL.IS", "MT"), ("EREGL.IS", "SLX"), ("EREGL.IS", "HG=F"),
             ("KRDMD.IS", "TKA.DE"), ("KRDMD.IS", "SZG.DE"), ("KRDMD.IS", "HG=F"), ("BRSAN.IS", "TS"), ("XU100.IS", "GC=F"), ("XU100.IS", "TKA.DE")]
    cache = {}
    for a, b in pairs:
        for s_ in (a, b):
            if s_ not in cache:
                try: cache[s_] = grid30(s_)
                except Exception as e: cache[s_] = None; print("m5 err", s_, e)
        if cache[a] is None or cache[b] is None: continue
        pa, pb = cache[a], cache[b]; idx = pa.index.intersection(pb.index); pa, pb = pa.reindex(idx), pb.reindex(idx)
        day = idx.normalize()
        ra = np.log(pa).groupby(day).diff(); rb_ = nz(np.log(pb).groupby(day).diff())
        rbl = rb_.groupby(day).shift(1); ral = ra.groupby(day).shift(1)
        c0, t0, n0 = mh.corr_t(ra, rb_); c1, t1, n1 = mh.corr_t(ra, rbl); cr, tr, nr = mh.corr_t(rb_, ral)
        GL.append({"stock": a, "driver": b, "c_sync30": c0, "t_sync30": t0, "c_drv_lead30": c1, "t_drv_lead30": t1, "c_stk_lead30": cr, "t_stk_lead30": tr, "n": n0,
                   "days": int(pd.Series(day).nunique())})
    pd.DataFrame(GL).to_csv(OUTP("x_m5_leadlag.csv"), index=False)
    # H. Gece altın sinyali (saatlik) -> TRALT/TRMET gün-içi; gap-artık geri dönüşü
    p15 = ll.snap_daily("GC=F", "15:00"); p07 = ll.snap_daily("GC=F", "06:55")
    HB = []
    for st in ["TRALT", "TRMET"]:
        d = mh.D(st).dropna(subset=["intra"]); d = d[d.index >= "2024-06-10"]
        prev = pd.Series(d.index[:-1], index=d.index[1:])
        night = pd.Series(np.log(p07.reindex(prev.index).values / p15.reindex(prev.values).values), index=prev.index)
        x = pd.concat([d, night.rename("night")], axis=1).dropna()
        # genişleyen beta (geçmiş), artık
        betas = [np.nan] * len(x)
        for k in range(60, len(x)):
            h = x.iloc[:k]; betas[k] = np.cov(h["gap"], h["night"])[0, 1] / h["night"].var()
        x["beta"] = betas; x["resid"] = x["gap"] - x["beta"] * x["night"]
        sdr = x["resid"].rolling(250, min_periods=60).std().shift(1); sdg = x["gap"].rolling(250, min_periods=60).std().shift(1)
        sigs = {"night_gold": x["night"], "gap_resid_reversal": -x["resid"].where(x["resid"].abs() > sdr), "gap_reversal_baseline": -x["gap"].where(x["gap"].abs() > sdg)}
        for k, s in sigs.items():
            for c in (8, 15):
                res, pnl = ll.backtest(s.fillna(0), x["intra"], cost_bps=c, mode="sign", split="2025-08-01")
                HB.append({"stock": st, "signal": k, "cost": c, **{f"{a}_{f}": res[a].get(f, np.nan) for a in ("IS", "OOS", "ALL") for f in ("n", "mean_bps", "t", "sharpe")},
                           "beta_last": x["beta"].iloc[-1]})
    pd.DataFrame(HB).to_csv(OUTP("x_night_bt.csv"), index=False)
    pd.DataFrame(BT).to_csv(OUTP("x_bt.csv"), index=False)
    print("done", len(LEAD), len(BT), len(MON), len(GL), len(HB))
