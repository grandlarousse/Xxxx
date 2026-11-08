"""(c) Kapalı uçlu / fiziki tröst fonlar: PHYS (altın), PSLV (gümüş), CEF (altın+gümüş).
NAV verisi yok. NAV ≈ ons/birim × spot; ons/birim yalnız yavaş değişir (gider, ek ihraç). Bu yüzden aynı anda (16:00 ET) kapanan
referans ETF ile oran kullanılır: ln(PHYS/GLD), ln(PSLV/SLV). CEF için referans = geçmiş 250 gün yuvarlanan OLS ile r_CEF ~ r_GLD + r_SLV
artığı. Sapma = ln oran − geçmiş k günün medyanı; z = sapma / geçmiş 250 gün std.
Bilgi zamanı: t-1 kapanışları (16:00 ET t-1 = 20:00/21:00 UTC t-1) -> gün t 15:00 ET'de bilinir. Gün-içi sürüm: 14:30 ET (saatlik, ~2 yıl).
"""
from common import *
from common import _stagger
import warnings; warnings.filterwarnings("ignore")
d = load_etf()
rows = []; srows = []

def rolling_beta_resid(y, X, win=250):
    """Geçmişe dayalı yuvarlanan OLS (t-1'e kadar); artık e_t = y_t − b_{t-1}·X_t."""
    dd = pd.concat([y.rename("y"), X], axis=1).dropna()
    out = pd.Series(np.nan, index=dd.index)
    Y = dd.y.values; XX = np.column_stack([np.ones(len(dd)), dd.iloc[:, 1:].values])
    for i in range(win, len(dd)):
        b = np.linalg.lstsq(XX[i - win:i], Y[i - win:i], rcond=None)[0]
        out.iloc[i] = Y[i] - XX[i, 1:] @ b[1:]
    return out

pairs = {}
rP = lr(d.c_PHYS); rG = lr(d.c_GLD); rPS = lr(d.c_PSLV); rSL = lr(d.c_SLV); rC = lr(d.c_CEF)
pairs["PHYS-GLD"] = dict(lvl=np.log(d.c_PHYS / d.c_GLD), sp=rP - rG, a="PHYS", b="GLD")
pairs["PSLV-SLV"] = dict(lvl=np.log(d.c_PSLV / d.c_SLV), sp=rPS - rSL, a="PSLV", b="SLV")
eC = rolling_beta_resid(rC, pd.concat([rG.rename("g"), rSL.rename("s")], axis=1))
pairs["CEF-mix"] = dict(lvl=eC.reindex(d.index).fillna(0).cumsum().where(eC.reindex(d.index).notna()), sp=eC.reindex(d.index), a="CEF", b="GLD")

for nm, pr in pairs.items():
    lvl, spr = pr["lvl"], pr["sp"]
    print(nm, "spread günlük std bps", round(spr.std() * 1e4, 1), "AC1", round(spr.autocorr(1), 3), "AC2", round(spr.autocorr(2), 3))
    for k in (20, 60):
        dev = lvl - lvl.rolling(k, min_periods=k // 2).median()
        z = dev / dev.rolling(250, min_periods=120).std()
        z_l1 = z.shift(1)  # uygulanabilir: t-1 kapanışı
        for h in HS:
            rows.append(test("c_cef", f"c_{nm}_z{k}_l1_spread_h{h}", f"{nm} sapma z (k={k}, t-1) -> spread", z_l1, fwd(spr, h), h))
            rows.append(test("c_cef", f"c_{nm}_z{k}_l1_{pr['a']}_h{h}", f"{nm} sapma z (k={k}, t-1) -> {pr['a']}", z_l1, fwd(lr(d['c_' + pr['a']]), h), h))
        if k == 20:
            rows.append(test("c_cef_diag", f"c_{nm}_z{k}_t_spread_h1", f"{nm} sapma z (t kapanışı; ulaşılamaz tanı) -> spread", z, fwd(spr, 1), 1, note="tanı"))
        pr[f"z{k}"] = z
    print(nm, "placebo z20:", placebo_lead(pr["z20"].shift(1), spr, 1))

# gün-içi (14:30 ET) PHYS/GLD
def h1430(t):
    g = pd.read_parquet(f"{P}/yahoo_h/{t}.parquet"); g.index = g.index.tz_convert("America/New_York")
    b = g[(g.index.hour == 13) & (g.index.minute == 30)]["close"]; b.index = pd.to_datetime(b.index.date); return b
lv_cut = np.log(h1430("PHYS") / h1430("GLD")).reindex(d.index)
lvl = pairs["PHYS-GLD"]["lvl"]
dev_cut = lv_cut - lvl.shift(1).rolling(20, min_periods=10).median()
z_cut = dev_cut / (lvl - lvl.rolling(20, min_periods=10).median()).rolling(250, min_periods=120).std().shift(1)
# ayrıca t-1 kapanışından 14:30'a spread hareketi
mv_cut = lv_cut - lvl.shift(1)
for h in HS:
    rows.append(test("c_cef_intraday", f"c_PHYS-GLD_zcut1430_spread_h{h}", "PHYS/GLD sapma z 14:30 ET (saatlik) -> spread", z_cut, fwd(pairs['PHYS-GLD']['sp'], h), h, note="2023-12+; tamamı OOS"))
    rows.append(test("c_cef_intraday", f"c_PHYS-GLD_mvcut1430_spread_h{h}", "PHYS/GLD spread hareketi t-1 kapanış->14:30 ET -> spread", mv_cut, fwd(pairs['PHYS-GLD']['sp'], h), h, note="2023-12+; tamamı OOS"))

res = pd.DataFrame(rows)
res.drop(columns=["by_year"], errors="ignore").to_csv(f"{OUT}/c_cef_tests.csv", index=False)
pd.set_option("display.width", 250)
print(res[["test_id", "h", "n", "ic", "t", "t_is", "t_oos", "t_22", "yrs_same_sign", "yrs"]].round(3).to_string())

# ---------------- Stratejiler
def switch_bt(w, exr, h, cost_rt):
    """Varsayılan referansı (GLD / SLV / GLD+SLV beta karması) tut; w=1 iken fona (PHYS/PSLV/CEF) geç.
    exr = fon − referans BASİT getiri farkı. Fazla getiri = eff·exr − |Δeff| × cost_rt/2 (bir geçiş = sat+al, iki bacak)."""
    idx = exr.dropna().index
    eff = _stagger(w.reindex(idx).fillna(0), h)
    ex = eff.shift(1) * exr.reindex(idx) - (eff - eff.shift(1).fillna(0)).abs().shift(1).fillna(0) * cost_rt / 2e4
    return ex.dropna(), eff

EXR = {"PHYS-GLD": np.expm1(rP) - np.expm1(rG), "PSLV-SLV": np.expm1(rPS) - np.expm1(rSL), "CEF-mix": eC.reindex(d.index)}
REF = {"PHYS-GLD": np.expm1(rG), "PSLV-SLV": np.expm1(rSL), "CEF-mix": None}
for nm in ["PHYS-GLD", "PSLV-SLV", "CEF-mix"]:
    pr = pairs[nm]; a = pr["a"]; exr = EXR[nm]
    cand = []
    for k in (20, 60):
        for thr in (1.0, 1.5, 2.0):
            for h in HS:
                w = (pr[f"z{k}"].shift(1) < -thr).astype(float)
                ex0, eff = switch_bt(w, exr, h, 0.0)
                ex, _ = switch_bt(w, exr, h, 20.0)    # 10+10 bps temel
                exs, _ = switch_bt(w, exr, h, 40.0)   # stres
                row = dict(strategy=f"arac_degistir_{nm}_k{k}_thr{thr}", pair=nm, k=k, thr=thr, h=h, frac_in_fund=round(eff.mean(), 3),
                           switches_yr=round(eff.diff().abs().sum() / len(eff) * 252, 1))
                for sg, v in segs(ex0).items(): row[f"IRgross_{sg}"] = v["sharpe"]
                for sg, v in segs(ex).items(): row[f"IR_{sg}"] = v["sharpe"]; row[f"ex_ann_{sg}"] = v["ann"]; row[f"t_{sg}"] = v["t"]
                for sg, v in segs(exs).items(): row[f"IRstress_{sg}"] = v["sharpe"]
                if REF[nm] is not None:
                    tot = (REF[nm] + ex.reindex(REF[nm].index)).dropna()
                    for sg, v in segs(tot).items(): row[f"sh_{sg}"] = v["sharpe"]
                    for sg, v in segs(REF[nm].dropna()[REF[nm].dropna().index >= ex.index[0]]).items(): row[f"bh_ref_{sg}"] = v["sharpe"]
                for kk, (x0, x1) in EXTREMES.items(): row[f"x_{kk}"] = round(ex[x0:x1].sum() * 100, 2) if len(ex[x0:x1]) else np.nan
                msk = pd.Series(True, index=ex.index)
                for x0, x1 in EXTREMES.values(): msk[x0:x1] = False
                row["IR_full_ex_extremes"] = perf(ex[msk])["sharpe"]
                yr = ex.groupby(ex.index.year).sum(); row["yrs_pos"] = f"{int((yr > 0).sum())}/{len(yr)}"
                cand.append(row)
    cdf = pd.DataFrame(cand)
    pick = cdf.sort_values("IR_is", ascending=False).iloc[0]
    print(f"{nm} IS seçimi: k={pick.k} thr={pick.thr} h={pick.h} IR_is={pick.IR_is} -> IR_oos={pick.IR_oos} IR_22={pick.IR_22} (stres OOS {pick.IRstress_oos}, brüt OOS {pick.IRgross_oos})")
    cdf["is_pick"] = (cdf.strategy == pick.strategy) & (cdf.h == pick.h)
    srows.append(cdf)
    # register: seçilen geçiş kuralı (fazla getiri günlük t'si)
    for _, rr_ in cdf.iterrows():
        register(AGENT, "c_cef_switch", f"{rr_.strategy}_h{rr_.h}", f"{nm} z<-thr iken fona geç", int(rr_.h),
                 dict(ic=rr_.ex_ann_full, t=rr_.t_full, n=None, t_is=rr_.t_is, t_oos=rr_.t_oos), note="strateji ızgarası; ic=yıllık fazla getiri %")
    if nm == "CEF-mix":
        continue
    # yönlü: fonu yalnız uzun (ucuzken), ters ETF (pahalıyken) — gereklilik 5 için
    pos = (-np.sign(pr[f"z{int(pick.k)}"].shift(1)) * (pr[f"z{int(pick.k)}"].shift(1).abs() > pick.thr)).fillna(0)
    inv = "GLL" if a == "PHYS" else "ZSL"
    yr_ = strat_eval(f"yonlu_{nm}", pos, a, int(pick.h), d, inv=inv)
    pd.DataFrame(yr_).to_csv(f"{OUT}/c_cef_directional_{nm}.csv", index=False)
    print(pd.DataFrame(yr_)[["strategy", "mode", "cost", "sh_is", "sh_oos", "sh_22", "shdm_is", "shdm_oos", "bh_oos"]].to_string())

out = pd.concat(srows)
out.to_csv(f"{OUT}/c_cef_switch_strategies.csv", index=False)
print(out[["strategy", "h", "frac_in_fund", "switches_yr", "IRgross_is", "IRgross_oos", "IR_is", "IR_oos", "IR_22", "IRstress_oos", "ex_ann_oos", "IR_full_ex_extremes", "yrs_pos"]].to_string())
print(out[out.is_pick].T.to_string())

# ---------------- Ekonomik büyüklük: z dilimlerine göre ileri spread (bps) ve brüt/net piyasa-nötr kuramsal getiri
mag = []
for nm in ["PHYS-GLD", "PSLV-SLV", "CEF-mix"]:
    pr = pairs[nm]
    for k in (20, 60):
        z1 = pr[f"z{k}"].shift(1)
        for h in HS:
            y = fwd(pr["sp"], h)
            dd = pd.concat([z1.rename("z"), y.rename("y")], axis=1).dropna()
            for seg, m in [("is", dd.index <= IS_END), ("oos", dd.index > IS_END)]:
                g = dd[m]
                b = pd.cut(g.z, [-np.inf, -2, -1, 1, 2, np.inf])
                mm = g.groupby(b).y.agg(["mean", "count"])
                mag.append(dict(pair=nm, k=k, h=h, seg=seg, **{f"bps_{str(i)}": round(v * 1e4, 1) for i, v in mm["mean"].items()},
                                **{f"n_{str(i)}": int(v) for i, v in mm["count"].items()}))
mag = pd.DataFrame(mag); mag.to_csv(f"{OUT}/c_cef_magnitude.csv", index=False)
print(mag[[c for c in mag.columns if not c.startswith("n_")]].to_string())
