"""(a) Segment getirilerinin ve kombinasyonların VİOP fwd1/3/5'i öngörüsü (Spearman IC, NW lag>=max(h,5)).
Erken dönem tekrarı: spot panel 2010-2016, hedef sfwd{h} (15:00->15:00 spot)."""
from a2_common import *
reset_families(["a_segment", "a_segment_cum5", "a_early", "a_segment_cum20", "a_bigmove"])
v = load_viop(); s = load_spot()
sv = segments(v); ss = segments(s)
PRED = SEGS + ["C_full", "C_post", "C_night", "C_on", "C_day", "C_pre", "D_asia_ny"]
CUM = ["S1_eve", "C_night", "S4_lon", "S5_nyam"]
rows = []; early = []
for h in (1, 3, 5):
    y = v[f"fwd{h}"]; ys = s[f"sfwd{h}"]
    for p in PRED:
        rows.append(test("a_segment", f"a_{p}_h{h}", p, sv[p], y, h, "bilgi zamanı <= t 15:00 UTC"))
    for p in CUM:
        x = sv[p].rolling(5).sum(); xs = ss[p].rolling(5).sum()
        rows.append(test("a_segment_cum5", f"a_{p}_cum5_h{h}", p + "_cum5", x, y, h, "5 günlük toplam"))
    # erken dönem (2010-2016) tekrar, spot panel
    for p in PRED + [c + "_cum5" for c in CUM]:
        x = ss[p] if p in ss else ss[p.replace("_cum5", "")].rolling(5).sum()
        m = (x.index < "2017-01-01")
        st = ic(x[m], ys[m], max(h, 5))
        d = pd.concat([x[m].rename("x"), ys[m].rename("y")], axis=1).dropna()
        yr = d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y, method="spearman"))
        st.update(yrs_same_sign=int((np.sign(yr) == np.sign(st["ic"])).sum()), yrs=int(yr.notna().sum()))
        register(AGENT, "a_early", f"a_early_{p}_h{h}", p, h, st, "spot panel 2010-2016, sfwd")
        # aynı tanım spot panel 2017+ (VİOP yerine spot hedef) — tutarlılık için, kaydedilmez (aynı hipotez)
        m2 = x.index >= "2017-03-01"
        st2 = ic(x[m2], ys[m2], max(h, 5))
        early.append(dict(predictor=p, h=h, ic_1016=round(st["ic"], 4), t_1016=round(st["t"], 2), yrs_1016=f'{st["yrs_same_sign"]}/{st["yrs"]}',
                          ic_spot17=round(st2["ic"], 4), t_spot17=round(st2["t"], 2)))
# 20 günlük gece (C_on) / gündüz (C_day) toplamları ("tug of war", Lou-Polk-Skouras 2019) ve büyük NY-sabahı (ABD veri saati) hareketleri
for h in (1, 3, 5):
    y = v[f"fwd{h}"]
    ys = s[f"sfwd{h}"]; me = s.index < "2017-01-01"
    def early_rep(nm, xs_):
        st = ic(xs_[me], ys[me], max(h, 5)); d = pd.concat([xs_[me].rename("x"), ys[me].rename("y")], axis=1).dropna()
        yr = d.groupby(d.index.year).apply(lambda g: g.x.corr(g.y, method="spearman") if len(g) > 20 else np.nan)
        st.update(yrs_same_sign=int((np.sign(yr) == np.sign(st["ic"])).sum()), yrs=int(yr.notna().sum()))
        register(AGENT, "a_early", f"a_early_{nm}_h{h}", nm, h, st, "spot panel 2010-2016, sfwd")
        early.append(dict(predictor=nm, h=h, ic_1016=round(st["ic"], 4), t_1016=round(st["t"], 2), yrs_1016=f'{st["yrs_same_sign"]}/{st["yrs"]}', ic_spot17=np.nan, t_spot17=np.nan))
    for p in ("C_on", "C_day"):
        rows.append(test("a_segment_cum20", f"a_{p}_cum20_h{h}", p + "_cum20", sv[p].rolling(20, min_periods=15).sum(), y, h, "20 günlük toplam"))
        early_rep(p + "_cum20", ss[p].rolling(20, min_periods=15).sum())
    thr = sv.S5_nyam[sv.index <= IS_END].abs().quantile(0.9)   # eşik IS'te
    big = sv.S5_nyam.where(sv.S5_nyam.abs() > thr)
    rows.append(test("a_bigmove", f"a_S5big_h{h}", "S5_nyam |>q90_IS|", big, y, h, "yalnız büyük hareket günleri"))
    thr_e = ss.S5_nyam[me].abs().quantile(0.9)  # erken dönem kendi eşiği (o dönemin ilk yarısı yerine tüm 2010-16; tanımlayıcı)
    early_rep("S5_nyam |>q90_IS|", ss.S5_nyam.where(ss.S5_nyam.abs() > thr_e))
R = pd.DataFrame(rows); E = pd.DataFrame(early)
R = R.merge(E, on=["predictor", "h"], how="left")
R.to_csv(f"{OUT}/a_segments_ic.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30); pd.set_option("display.max_rows", 200)
print(R.drop(columns=["note", "family", "test_id"]).to_string())
