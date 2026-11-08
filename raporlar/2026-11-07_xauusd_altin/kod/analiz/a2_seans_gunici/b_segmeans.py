"""(b) 'Gece/Asya pozitif, NY negatif' anomalisi: segment ortalama getirileri yıl yıl (2010-2026, spot panel),
saat-saat ortalama, drift-düzeltilmiş segment fazlası, ve VİOP akşam seansıyla uygulanabilir alternatif giriş/çıkış saatleri (maliyetli).
Bu stratejiler kapanıştan kapanışa DEĞİL; ayrı raporlanır."""
from a2_common import *
reset_families(["b_segmean", "b_segexcess", "b_altentry"])
s = load_spot(); ss = segments(s)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_rows", 300)
seg = ss[SEGS].dropna()
day = seg.sum(axis=1)
yr = seg.index.year
# --- yıl yıl ortalama (bps/gün)
tab = (seg.groupby(yr).mean() * 1e4).round(2)
tab["DAY"] = (day.groupby(yr).mean() * 1e4).round(2)
tab["n"] = seg.groupby(yr).size()
tab.to_csv(f"{OUT}/b_segment_mean_by_year_bps.csv")
print("Segment ortalama getirisi (bps/gün), spot 2010-2026:\n", tab.to_string())
# segment volatilitesi (bps)
vt = (seg.groupby(yr).std() * 1e4).round(1); vt.to_csv(f"{OUT}/b_segment_std_by_year_bps.csv")
print("\nSegment std (bps):\n", vt.to_string())
# --- testler: ortalama + drift-düzeltilmiş fazla
per = {"2010-16": seg.index < "2017-01-01", "IS17-21": (seg.index >= "2017-03-01") & (seg.index <= IS_END), "OOS22-26": seg.index > IS_END, "full": np.ones(len(seg), bool)}
rows = []
for c in SEGS:
    # drift payı: segment varyans payı x günlük ortalama (her yıl içinde), fazla = segment - pay
    share = seg[c].groupby(yr).transform("var") / day.groupby(yr).transform("var")
    exc = seg[c] - share * day.groupby(yr).transform("mean")
    for nm, x in [("mean", seg[c]), ("excess", exc)]:
        r = dict(seg=c, kind=nm)
        for p, m in per.items():
            mt = mean_test(x[m]); r[f"{p}_bps"] = round(mt["mean"] * 1e4, 2); r[f"{p}_t"] = round(mt["t"], 2)
        ys = x.groupby(yr).mean(); r["yrs_pos"] = f"{int((ys > 0).sum())}/{len(ys)}"
        rows.append(r)
        fm = mean_test(x); ism = mean_test(x[per["IS17-21"]]); oom = mean_test(x[per["OOS22-26"]])
        register(AGENT, "b_segmean" if nm == "mean" else "b_segexcess", f"b_{nm}_{c}", c, 0,
                 dict(ic=fm["mean"], t=fm["t"], n=fm["n"], t_is=ism["t"], t_oos=oom["t"], ic_oos=oom["mean"],
                      yrs_same_sign=int((np.sign(ys) == np.sign(fm["mean"])).sum()), yrs=len(ys)), "ortalama segment getirisi (ic sütunu=ortalama)")
M = pd.DataFrame(rows); M.to_csv(f"{OUT}/b_segment_tests.csv", index=False)
print("\nSegment ortalama ve drift-düzeltilmiş fazla testleri:\n", M.to_string())

# --- saat-saat ortalama getiri (UTC), dönem grupları
px = price_series(); lr = np.log(px).diff()
gap = px.index.to_series().diff() != pd.Timedelta(hours=1)
lr = lr[~gap.values]  # yalnız ardışık saatler (hafta sonu boşluğu hariç)
hr = lr.index.hour  # fiyat anı saati: (H-1 -> H) getirisi
grp = pd.cut(lr.index.year, [2009, 2016, 2021, 2026], labels=["2010-16", "2017-21", "2022-26"])
m10 = lr.index.year >= 2010
H = pd.DataFrame({"r": lr.values, "h": hr, "g": grp})[m10]
HT = (H.groupby(["h", "g"]).r.mean().unstack() * 1e4).round(2)
HT["t_all"] = H.groupby("h").r.apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x)))).round(2)
HT.index = [f"{(h-1)%24:02d}->{h:02d}" for h in HT.index]
HT.to_csv(f"{OUT}/b_hourly_mean_bps.csv"); print("\nSaatlik ortalama getiri (bps), UTC:\n", HT.to_string())

# --- alternatif giriş/çıkış stratejileri (spot vekil; VİOP akşam seansı 18.09.2020+)
alt = pd.DataFrame(index=seg.index)
alt["ALT_eve_long"] = seg.S1_eve            # uzlaşmada (≈15:10) al -> 20:00 akşam seansı sonunda sat
alt["ALT_night_long"] = seg.S2_late + seg.S3_asia   # 20:00 al -> ertesi 06:30/07:00 sabah açılışında sat
alt["ALT_day_long"] = seg.S4_lon + seg.S5_nyam      # 07:00 al -> 15:10 uzlaşmada sat
alt["ALT_20_to_settle"] = seg.S2_late + seg.S3_asia + seg.S4_lon + seg.S5_nyam   # 20:00 al -> ertesi uzlaşmada sat
alt["ALT_LN_SD"] = (seg.S2_late + seg.S3_asia) - (seg.S4_lon + seg.S5_nyam)  # gece uzun + gündüz kısa (2 gidiş-dönüş)
ntr = {"ALT_eve_long": 1, "ALT_night_long": 1, "ALT_day_long": 1, "ALT_20_to_settle": 1, "ALT_LN_SD": 2}
alt["BH_15_15"] = day
rows = []
for c in alt.columns:
    for cost in (0, 5, 10):
        k = ntr.get(c, 0)
        net = alt[c] - k * cost / 1e4 if c != "BH_15_15" else alt[c]
        for p, m in {"2010-16": alt.index < "2017-01-01", "IS17-21": (alt.index >= "2017-03-01") & (alt.index <= IS_END),
                     "OOS22-26": alt.index > IS_END, "VIOPeve20.09+": alt.index >= "2020-09-18"}.items():
            x = net[m].dropna()
            rows.append(dict(strat=c, cost=cost, per=p, ann_pct=round(x.mean() * 252 * 100, 2), sharpe=round(x.mean() / x.std() * np.sqrt(252), 2),
                             t=round(mean_test(x)["t"], 2), hit=round((x > 0).mean(), 3), n=len(x)))
        if cost == 5 and c != "BH_15_15":
            x = net.dropna(); ys = x.groupby(x.index.year).mean()
            fm = mean_test(x); ism = mean_test(x[(x.index >= "2017-03-01") & (x.index <= IS_END)]); oom = mean_test(x[x.index > IS_END])
            register(AGENT, "b_altentry", f"b_{c}", c, 0, dict(ic=fm["mean"], t=fm["t"], n=fm["n"], t_is=ism["t"], t_oos=oom["t"], ic_oos=oom["mean"],
                     yrs_same_sign=int((np.sign(ys) == np.sign(fm["mean"])).sum()), yrs=len(ys)), "5bps net günlük getiri, 2010-2026")
A = pd.DataFrame(rows); A.to_csv(f"{OUT}/b_alt_entry.csv", index=False)
print("\nAlternatif giriş/çıkış (spot vekil):\n", A.pivot_table(index=["strat", "cost"], columns="per", values=["sharpe", "ann_pct"]).to_string())
# yıl yıl, 5 bps net, yıllık %
YY = pd.DataFrame({c: ((alt[c] - ntr.get(c, 0) * 5 / 1e4).groupby(alt.index.year).mean() * 252 * 100).round(1) for c in alt.columns})
YY.to_csv(f"{OUT}/b_alt_by_year_net5.csv"); print("\nYıl yıl yıllık getiri % (5 bps net):\n", YY.to_string())
