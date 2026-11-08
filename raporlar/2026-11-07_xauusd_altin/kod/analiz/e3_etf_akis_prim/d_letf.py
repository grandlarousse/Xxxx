"""(d) Kaldıraçlı ETF dengelemesi.
Mekanizma (Cheng–Madhavan 2009; Shum vd. 2016): günlük kaldıraç sabitleyen L× ETF'ler kapanışa yakın L(L−1)·AUM·r_t kadar
günün yönünde alım/satım yapar -> son saatte momentum, ertesi gün kısmi dönüş. Ters ETF'lerde de L(L−1)>0, aynı yön.
Testler:
 (1) Gerçekleşen kaldıraç ve aşınma (1/3/5 gün).
 (2) Mekanizma tanısı (İŞLEM DIŞI: gün t kapanış getirisi): |r_t|>2σ sonrası t+1 işaretli getiri; kaldıraçlı ürün ÖNCESİ
     (GLD 2004-11..2008-11; GDX 2006-05..2010-11; GDXJ 2009-11..2013-09) ve SONRASI.
 (3) Uygulanabilir: gün t'de 15:00 ET'ye kadarki hareket m_t = ln(xau_cut_t / xau_close_{t-1}) (spot, Dukascopy; bilgi anı 15:00 ET)
     büyükse (|m|>2σ, σ geçmiş 60 gün) -> GLD/GDX/GDXJ t kapanışından t+h'ye işaretli getiri.
     Ayrıca gün t-1 tam kapanış hareketi (bilgi anı t-1 16:00 ET).
 (4) Son saat momentumu: corr(m_t, ln(xau_close/xau_cut)) uzun dönem; saatlik GLD/GDX/NUGT (2 yıl) ve 5 dk (60 gün) son 30 dk.
"""
from common import *
import warnings; warnings.filterwarnings("ignore")
d = load_etf()
rows = []

def ylong(t):
    x = pd.read_parquet(f"{P}/yahoo/{t}.parquet"); x.index = pd.to_datetime(x.index); return x

# ---------------- (1) gerçekleşen kaldıraç
lev_rows = []
pairs = [("GLL", "GLD", -2), ("UGL", "GLD", 2), ("NUGT", "GDX", None), ("DUST", "GDX", None), ("JNUG", "GDXJ", None), ("JDST", "GDXJ", None),
         ("ZSL", "SLV", -2), ("AGQ", "SLV", 2), ("GDXU", "GDX", 3)]
for le, un, nom in pairs:
    if f"c_{le}" not in d: continue
    rl = lr(d[f"c_{le}"]); ru = lr(d[f"c_{un}"])
    for per, a, b in [("2010-2019", "2008-12-01", "2020-03-31"), ("2020-04+", "2020-04-01", "2026-12-31")]:
        for h in HS:
            y = rl.rolling(h).sum()[a:b]; x = ru.rolling(h).sum()[a:b]
            dd = pd.concat([y.rename("y"), x.rename("x")], axis=1).dropna()
            dd = dd.iloc[::h]   # örtüşmesiz
            if len(dd) < 50: continue
            beta = np.polyfit(dd.x, dd.y, 1)[0]
            decay = (dd.y - beta * dd.x).mean() * 252 / h
            lev_rows.append(dict(etf=le, under=un, period=per, h=h, beta=round(beta, 3), drag_ann_pct=round(decay * 100, 2), n=len(dd)))
lev = pd.DataFrame(lev_rows); lev.to_csv(f"{OUT}/d_realized_leverage.csv", index=False)
print(lev.pivot_table(index=["etf", "period"], columns="h", values="beta").round(2))

# ---------------- (2) mekanizma tanısı: ön/arka kaldıraçlı ürün
def event_rev(r, label, pre_end, sub=None):
    sig = r.rolling(60, min_periods=40).std().shift(1)
    big = (r.abs() > 2 * sig)
    y1 = r.shift(-1) * np.sign(r)          # işaretli ertesi gün getiri (pozitif = devam, negatif = dönüş)
    out = []
    for per, msk in [("pre", r.index <= pre_end), ("post", r.index > pre_end)]:
        e = y1[big & msk].dropna(); allv = (r.shift(-1) * np.sign(r))[msk].dropna()
        if len(e) < 10: continue
        tt = e.mean() / (e.std() / np.sqrt(len(e)))
        b = nw_ols(r.shift(-1)[msk], r[msk], lags=5)
        out.append(dict(series=label, period=per, n_big=len(e), signed_next_bps=round(e.mean() * 1e4, 1), t=round(tt, 2),
                        beta_next_on_r=round(b["b"], 3), t_beta=round(b["t"], 2), start=str(r[msk].dropna().index[0].date())))
    return out

diag = []
gl = ylong("GLD"); gd = ylong("GDX"); gj = ylong("GDXJ")
for nm, px, pe in [("GLD", gl.adjclose, "2008-11-30"), ("GDX", gd.adjclose, "2010-11-30"), ("GDXJ", gj.adjclose, "2013-09-30")]:
    diag += event_rev(np.log(px).diff(), nm, pd.Timestamp(pe))
diag = pd.DataFrame(diag); diag.to_csv(f"{OUT}/d_prepost_letf.csv", index=False)
print(diag.to_string())
for _, rr in diag.iterrows():
    register(AGENT, "d_letf_diag", f"d_prepost_{rr.series}_{rr.period}", f"{rr.series} |r_t|>2σ -> işaretli r_t+1 (tanı, işlem dışı)", 1,
             dict(ic=rr.signed_next_bps, t=rr.t, n=rr.n_big), note="tanı; gün t kapanış getirisi cutoff'ta bilinmez")

# ---------------- (3) uygulanabilir: 15:00 ET'ye kadarki spot hareketi ve t-1 hareketi
m = np.log(d.xau_cut / d.xau_close.shift(1))
sm_ = m.rolling(60, min_periods=40).std().shift(1)
zm = m / sm_
lasth = np.log(d.xau_close / d.xau_cut)
print("corr(m_t, son saat spot getirisi):", round(m.corr(lasth), 3), {y: round(m[str(y)].corr(lasth[str(y)]), 3) for y in range(2008, 2027)})
rows.append(test("d_letf_lasthour", "d_m_to_lasthour_spot", "m_t (15:00 ET'ye kadar) -> son saat spot (15->16 ET)", m, lasth.shift(-1).shift(1), 1, note="tanı: son saat momentumu"))
# büyük hareket olayı (işaretli)
big = (zm.abs() > 2).astype(float).where(zm.notna())
for tgt in ["GLD", "GDX", "GDXJ", "SLV"]:
    r = lr(d[f"c_{tgt}"])
    for h in HS:
        y = fwd(r, h)
        rows.append(test("d_letf_cut", f"d_zm_{tgt}_h{h}", f"z(m_t) spot 15:00 ET hareketi -> {tgt}", zm, y, h))
        ys = y * np.sign(m)
        rows.append(mean_diff_test("d_letf_cut_big", f"d_bigm_{tgt}_h{h}", f"|z(m_t)|>2 -> işaretli {tgt}", big, ys, h))
# t-1 tam gün hareketi (bilgi t-1 16:00 ET)
for tgt in ["GLD", "GDX", "GDXJ"]:
    r = lr(d[f"c_{tgt}"])
    zr = r / r.rolling(60, min_periods=40).std().shift(1)
    bg = (zr.abs() > 2).astype(float).where(zr.notna())
    for h in HS:
        y = fwd(r, h)
        rows.append(test("d_letf_l1", f"d_zr_l1_{tgt}_h{h}", f"z(r_t-1) {tgt} -> {tgt}", zr.shift(1), y, h))
        rows.append(mean_diff_test("d_letf_l1_big", f"d_bigr_l1_{tgt}_h{h}", f"|z(r_t-1)|>2 -> işaretli {tgt}", bg.shift(1), y * np.sign(r.shift(1)), h))
print("placebo zm -> GLD:", placebo_lead(zm, lr(d.c_GLD), 1))

# ---------------- (4) saatlik (2 yıl) ve 5 dk (60 gün) son saat / son 30 dk momentumu
def hb(t):
    g = pd.read_parquet(f"{P}/yahoo_h/{t}.parquet"); g.index = g.index.tz_convert("America/New_York"); return g
intr = []
for t in ["GLD", "GDX", "GDXJ", "NUGT", "SLV", "IAU", "DUST", "GLL", "UGL"]:
    try: g = hb(t)
    except Exception: continue
    c1430 = g[(g.index.hour == 13) & (g.index.minute == 30)]["close"]; c1430.index = pd.to_datetime(c1430.index.date)
    cc = ylong(t)["close"].reindex(d.index)   # temettü düzeltmesiz (saatlik veriyle aynı ölçek)
    a = np.log(c1430.reindex(d.index) / cc.shift(1)); b_ = np.log(cc / c1430.reindex(d.index)); nxt = lr(d[f"c_{t}"]).shift(-1)
    dd = pd.concat([a.rename("a"), b_.rename("b"), nxt.rename("n")], axis=1).dropna()
    if len(dd) < 50: continue
    r1 = nw_ols(dd.b, dd.a, lags=5); r2 = nw_ols(dd.n, dd.a, lags=5)
    intr.append(dict(etf=t, freq="1h", n=len(dd), corr_to1430_last90=round(dd.a.corr(dd.b), 3), t1=round(r1["t"], 2),
                     corr_to1430_next=round(dd.a.corr(dd.n), 3), t2=round(r2["t"], 2)))
    register(AGENT, "d_letf_intraday", f"d_h1_{t}_lastseg", f"{t} t-1 kapanış->14:30 ET -> 14:30->16:00", 1, dict(ic=dd.a.corr(dd.b), t=r1["t"], n=len(dd)), note="tanı; 2 yıl")
    rows.append(test("d_letf_intraday", f"d_h1_{t}_next_h1", f"{t} t-1 kapanış->14:30 ET hareketi -> {t} t->t+1", a, fwd(lr(d[f"c_{t}"]), 1), 1, note="2023-12+; tamamı OOS"))
for t in ["GLD", "GDX", "GDXJ", "NUGT", "SLV", "IAU"]:
    g = pd.read_parquet(f"{P}/yahoo_5m/{t}.parquet"); g.index = g.index.tz_convert("America/New_York")
    g = g.between_time("09:30", "15:55")
    c1525 = g[(g.index.hour == 15) & (g.index.minute == 25)]["close"]; c1525.index = pd.to_datetime(c1525.index.date)
    cc = ylong(t)["close"].reindex(d.index)
    a = np.log(c1525.reindex(d.index) / cc.shift(1)); b_ = np.log(cc / c1525.reindex(d.index))
    dd = pd.concat([a.rename("a"), b_.rename("b")], axis=1).dropna()
    r1 = nw_ols(dd.b, dd.a, lags=2)
    intr.append(dict(etf=t, freq="5m", n=len(dd), corr_to1530_last30=round(dd.a.corr(dd.b), 3), t1=round(r1["t"], 2)))
    register(AGENT, "d_letf_intraday", f"d_5m_{t}_last30", f"{t} t-1 kapanış->15:30 ET -> son 30 dk", 1, dict(ic=dd.a.corr(dd.b), t=r1["t"], n=len(dd)), note="tanı; 60 gün")
intr = pd.DataFrame(intr); intr.to_csv(f"{OUT}/d_intraday_lastseg.csv", index=False)
print(intr.to_string())

res = pd.DataFrame(rows)
res.drop(columns=["by_year"], errors="ignore").to_csv(f"{OUT}/d_letf_tests.csv", index=False)
pd.set_option("display.width", 250)
print(res[["test_id", "h", "n", "ic", "t", "t_is", "t_oos", "t_22", "yrs_same_sign", "yrs"]].round(3).to_string())

# ---------------- (3b) m_t -> madenci dönüşü: kaldıraçlı ürün öncesi/sonrası ve yıl yıl
sub = []
for tgt, launch in [("GDX", "2010-12-08"), ("GDXJ", "2013-10-03"), ("GLD", "2008-12-03"), ("SLV", "2008-12-03")]:
    r = lr(d[f"c_{tgt}"]); y = fwd(r, 1)
    for per, a_, b_ in [("oncesi", "2008-01-01", launch), ("sonrasi", launch, "2026-12-31"), ("2013-2016", "2013-01-01", "2016-12-31"),
                        ("2017-2019", "2017-01-01", "2019-12-31"), ("2020-2021", "2020-01-01", "2021-12-31"), ("2022+", "2022-01-01", "2026-12-31")]:
        x_ = zm[a_:b_]; y_ = y[a_:b_]
        if x_.notna().sum() < 100: continue
        q = ic(x_, y_, 5)
        b = nw_ols(y_, m[a_:b_], lags=5)
        sub.append(dict(target=tgt, period=per, n=q["n"], ic=round(q["ic"], 3), t=round(q["t"], 2), beta_r_on_m=round(b["b"], 3), t_beta=round(b["t"], 2)))
sub = pd.DataFrame(sub); sub.to_csv(f"{OUT}/d_m_miner_subperiods.csv", index=False); print(sub.to_string())
# madencinin kendi gün-t getirisini kontrol et (işlem dışı tanı): m_t etkisi kendi dönüşünden mi?
for tgt in ["GDX", "GDXJ"]:
    r = lr(d[f"c_{tgt}"]); X = pd.concat([m.rename("m"), r.rename("r_t"), (r - m * nw_ols(r, m)["b"]).rename("idio_t")], axis=1)
    b1 = nw_ols(r.shift(-1), X[["m", "idio_t"]], lags=5)["model"]
    print(tgt, "r_t+1 ~ m_t + idio_t (tanı):", dict(zip(b1.params.index, [f"{p:.3f} (t={t:.1f})" for p, t in zip(b1.params, b1.tvalues)])))

# ---------------- Strateji: IS'te en güçlü uygulanabilir kural (|t_is|) -> eşik ve h IS'te -> OOS bir kez
cand = res[res.family.isin(["d_letf_cut", "d_letf_cut_big", "d_letf_l1", "d_letf_l1_big"])].copy()
cand["abs_t_is"] = cand.t_is.abs()
b = cand.sort_values("abs_t_is", ascending=False).iloc[0]
print("IS en güçlü test:", b.test_id, "t_is", round(b.t_is, 2), "t_oos", round(b.t_oos, 2))
json.dump({"is_best": b.test_id, "t_is": float(b.t_is), "t_oos": float(b.t_oos)}, open(f"{OUT}/d_is_choice.json", "w"))

def lev_series(inv, idx):
    if inv in ("DUST", "JDST"):
        return pd.Series(np.where(idx < pd.Timestamp("2020-04-01"), 3.0, 2.0), index=idx)
    return pd.Series(2.0, index=idx)

def strat_eval_tv(name, pos, tgt, h, inv):
    """strat_eval'in zamanla değişen ters ETF kaldıraçlı sürümü (DUST/JDST 2020-04 öncesi −3x)."""
    r = lr(d[f"c_{tgt}"]); ri = lr(d[f"c_{inv}"])
    out = []
    for mode in ["long_only", "inverse"]:
        rr = r if mode == "long_only" else r[ri.reindex(r.index).notna()]
        L = lev_series(inv, rr.index)
        for cname, cl, ci in [("base", 10.0, 20.0), ("stress", 20.0, 40.0)]:
            net, wl, ws = bt(pos, rr, h, cl, ri, L, ci, mode=mode)
            dm, _, _ = bt(pos, rr, h, cl, ri, L, ci, demean=True, mode=mode)
            nl, _, _ = bt(pos.clip(lower=0), rr, h, 0.0, mode="long_only")
            row = dict(strategy=name, target=tgt, h=h, mode=mode, cost=cname, exposure_long=round(wl.mean(), 3), exposure_short=round((ws * L).mean(), 3),
                       turnover_yr=round(((wl.diff().abs() + ws.diff().abs()).sum() / len(rr)) * 252, 1), start=str(rr.dropna().index[0].date()))
            for sg, v in segs(net).items(): row[f"sh_{sg}"] = v["sharpe"]; row[f"ann_{sg}"] = v["ann"]; row[f"t_{sg}"] = v["t"]
            for sg, v in segs(dm).items(): row[f"shdm_{sg}"] = v["sharpe"]
            for sg, v in segs(np.expm1(rr).dropna()).items(): row[f"bh_{sg}"] = v["sharpe"]
            row["leg_long_sh_oos"] = perf(nl[nl.index > IS_END])["sharpe"]
            if mode == "inverse":
                ns, _, _ = bt(pos.clip(upper=0), rr, h, 0.0, ri, L, 0.0, mode="inverse")
                row["leg_short_sh_oos"] = perf(ns[ns.index > IS_END])["sharpe"]; row["leg_short_ann_full"] = perf(ns)["ann"]
            for k_, (x0, x1) in EXTREMES.items(): row[f"x_{k_}"] = round(net[x0:x1].sum() * 100, 2) if len(net[x0:x1]) else np.nan
            msk = pd.Series(True, index=net.index)
            for x0, x1 in EXTREMES.values(): msk[x0:x1] = False
            row["sh_full_ex_extremes"] = perf(net[msk])["sharpe"]
            yr = net.groupby(net.index.year).sum(); row["yrs_pos"] = f"{int((yr > 0).sum())}/{len(yr)}"
            out.append(row)
    return out

srows = []
for tgt, inv in [("GDXJ", "JDST"), ("GDX", "DUST"), ("GLD", "GLL")]:
    for thr in (0.0, 1.0, 1.5, 2.0):
        for h in HS:
            pos = (-np.sign(zm) * (zm.abs() > thr)).fillna(0)
            for rr_ in strat_eval_tv(f"m_kontra_{tgt}_thr{thr}", pos, tgt, h, inv):
                rr_["thr"] = thr; srows.append(rr_)
sr = pd.DataFrame(srows); sr.to_csv(f"{OUT}/d_letf_strategies.csv", index=False)
for tgt in ["GDXJ", "GDX", "GLD"]:
    g = sr[(sr.target == tgt) & (sr["mode"] == "long_only") & (sr.cost == "base")]
    pk = g.sort_values("shdm_is", ascending=False).iloc[0]
    print(f"{tgt} IS seçimi (yalnız uzun, demeaned IS Sharpe): thr={pk.thr} h={pk.h} shdm_is={pk.shdm_is} -> sh_oos={pk.sh_oos} shdm_oos={pk.shdm_oos} bh_oos={pk.bh_oos}")
    gi = sr[(sr.target == tgt) & (sr["mode"] == "inverse") & (sr.cost == "base")]
    pki = gi.sort_values("sh_is", ascending=False).iloc[0]
    print(f"{tgt} IS seçimi (ters ETF'li): thr={pki.thr} h={pki.h} sh_is={pki.sh_is} -> sh_oos={pki.sh_oos} sh_22={pki.sh_22}")
cols = ["strategy", "h", "mode", "cost", "sh_is", "sh_oos", "sh_22", "shdm_is", "shdm_oos", "bh_is", "bh_oos", "exposure_long", "exposure_short", "turnover_yr", "leg_long_sh_oos", "leg_short_sh_oos", "sh_full_ex_extremes", "yrs_pos"]
print(sr[sr.cost == "base"][cols].to_string())
