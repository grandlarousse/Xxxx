"""(d) LBMA Gold Price PM (15:00 Londra) çevresi. Fiks saati UTC: kış (GMT) 15:00, yaz (BST) 14:00.
Fiks fiyatı yerine Dukascopy spot o saatteki fiyatı (vekil; IBA verisi indirilemedi - Cloudflare).
r_pre = log(P_fix / P_fix-1h): bilgi zamanı = fiks anı <= 15:00 UTC -> gün t sinyali olabilir.
r_post = log(P_fix+1h / P_fix): kışın 15->16 UTC (cutoff SONRASI) -> yalnız gün içi tanımlayıcı."""
from a2_common import *
reset_families(["d_fix"])
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
v = load_viop(); s = load_spot(); px = price_series()
def snap_ts(ts):
    i = px.index.searchsorted(ts, side="right") - 1
    ok = (i >= 0)
    val = np.where(ok, px.values[np.clip(i, 0, None)], np.nan)
    st = (ts - px.index[np.clip(i, 0, None)]) / pd.Timedelta(hours=1)
    return np.where(st <= 1, val, np.nan)
def fixframe(days):
    days = pd.DatetimeIndex(days)
    fixl = pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("Europe/London") + pd.Timedelta(hours=15) for d in days]).tz_convert("UTC")
    fh = fixl.hour
    o = pd.DataFrame(index=days)
    o["fix_hour_utc"] = fh
    pf = snap_ts(fixl); pm1 = snap_ts(fixl - pd.Timedelta(hours=1)); pp1 = snap_ts(fixl + pd.Timedelta(hours=1)); pm2 = snap_ts(fixl - pd.Timedelta(hours=2))
    o["r_pre"] = np.log(pf / pm1); o["r_pre2"] = np.log(pm1 / pm2); o["r_post"] = np.log(pp1 / pf)
    p15 = snap_ts(pd.DatetimeIndex([pd.Timestamp(d.date()).tz_localize("UTC") + pd.Timedelta(hours=15) for d in days]))
    o["r_fix_to_15"] = np.where(fh == 14, np.log(p15 / pf), np.nan)  # yalnız yaz: fiks (14:00) -> 15:00 UTC (cutoff'tan önce)
    return o
F = fixframe(v.index); Fs = fixframe(s.index)
print("fiks saati dağılımı (VİOP günleri):", F.fix_hour_utc.value_counts().to_dict())
rows = []
for h in (1, 3, 5):
    y = v[f"fwd{h}"]
    rows.append(test("d_fix", f"d_rpre_h{h}", "r_pre (fiks-1s->fiks)", F.r_pre, y, h, "<=15:00 UTC"))
    rows.append(test("d_fix", f"d_fix_to_15_summer_h{h}", "yaz: fiks(14)->15:00", F.r_fix_to_15, y, h, "yalnız BST günleri"))
for nm, msk in [("kis", F.fix_hour_utc == 15), ("yaz", F.fix_hour_utc == 14)]:
    rows.append(test("d_fix", f"d_rpre_{nm}_h1", f"r_pre {nm}", F.r_pre.where(msk), v.fwd1, 1, "DST alt örneklem"))
# gün içi fiks dönüşü (kapanıştan kapanışa değil): r_pre -> r_post, spot panel 2010-2026
st = split_stats(Fs.r_pre, Fs.r_post, 1); register(AGENT, "d_fix", "d_rpre_to_rpost_intraday", "r_pre->r_post", 0, st, "gün içi, spot 2010-26")
rows.append(dict(family="d_fix", test_id="d_rpre_to_rpost_intraday", predictor="r_pre->r_post (gün içi)", h=0, n=st["n"], ic=round(st["ic"], 4), t=round(st["t"], 2),
                 ic_is=round(st["ic_is"], 4), t_is=round(st["t_is"], 2), ic_oos=round(st["ic_oos"], 4), t_oos=round(st["t_oos"], 2), yrs=f'{st["yrs_same_sign"]}/{st["yrs"]}'))
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/d_fix_ic.csv", index=False); print(R.drop(columns=["family", "test_id", "note"], errors="ignore").to_string())
# ortalama getiriler: fiks öncesi/sonrası saat, yıl yıl (bps)
yr = Fs.index.year
T = pd.DataFrame({"pre2(fiks-2->-1)": Fs.r_pre2.groupby(yr).mean(), "pre(fiks-1->fiks)": Fs.r_pre.groupby(yr).mean(), "post(fiks->+1)": Fs.r_post.groupby(yr).mean()}) * 1e4
T = T.round(2); T.to_csv(f"{OUT}/d_fix_hour_means_by_year_bps.csv"); print("\nFiks çevresi saatlik ortalama (bps):\n", T.to_string())
for c in ["r_pre", "r_post", "r_pre2"]:
    x = Fs[c]; fm = mean_test(x); ys = x.groupby(yr).mean()
    ism = mean_test(x[(x.index >= "2017-03-01") & (x.index <= IS_END)]); oom = mean_test(x[x.index > IS_END]); e = mean_test(x[x.index < "2017-01-01"])
    register(AGENT, "d_fix", f"d_mean_{c}", c, 0, dict(ic=fm["mean"], t=fm["t"], n=fm["n"], t_is=ism["t"], t_oos=oom["t"], ic_oos=oom["mean"],
             yrs_same_sign=int((np.sign(ys) == np.sign(fm["mean"])).sum()), yrs=len(ys)), "ortalama saatlik getiri")
    print(c, "ort bps", round(fm["mean"] * 1e4, 2), "t", round(fm["t"], 2), "| 2010-16", round(e["mean"] * 1e4, 2), round(e["t"], 2), "| IS", round(ism["mean"] * 1e4, 2), round(ism["t"], 2), "| OOS", round(oom["mean"] * 1e4, 2), round(oom["t"], 2), "| yıllar aynı işaret", int((np.sign(ys) == np.sign(fm["mean"])).sum()), "/", len(ys))
# kış/yaz: 15:00 -> 15:10 spot (uzlaşma gürültüsü) ve uzlaşma-spot farkı (dakikalık örnek)
m = pd.read_parquet(f"{P}/duka_min_XAUUSD.parquet"); m.index = pd.to_datetime(m.index)
rr = []
for d, g in m.groupby(m.index.date):
    d = pd.Timestamp(d)
    a = g.c[g.index <= d + pd.Timedelta(hours=14, minutes=59)]; b = g.c[g.index <= d + pd.Timedelta(hours=15, minutes=9)]
    if len(a) and len(b): rr.append(dict(date=d, r_1500_1510=np.log(b.iloc[-1] / a.iloc[-1])))
RR = pd.DataFrame(rr).set_index("date"); RR = RR.join(fixframe(RR.index)[["fix_hour_utc"]])
print("\n15:00->15:10 spot getirisi (bps) kış/yaz (dakikalık örnek):\n", (RR.groupby("fix_hour_utc").r_1500_1510.agg(["mean", "std", "count"]) * [1e4, 1e4, 1]).round(2).to_string())
# VİOP vade sonu (son işlem günü uzlaşması = LBMA PM): aktif seride kaç gün vade sonu
print("aktif seride dte<=0 gün sayısı:", int((v.v_dte <= 0).sum()), " dte<=2:", int((v.v_dte <= 2).sum()))
