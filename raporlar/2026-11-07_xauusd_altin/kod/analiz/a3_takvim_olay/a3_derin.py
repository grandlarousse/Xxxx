"""a3_takvim_olay — ana taramada öne çıkan adaylar için derin kontroller (a3_analiz.py'den SONRA çalıştır; registry'ye ekler).
Adaylar: NFP koşullu momentum, çeyrek sonu ay dönümü, bayram sonrası, OG vade günü, Ocak etkisi; kontrol testleri (tüm günler, Cuma, CPI) dahil.
"""
import os, sys, json, warnings
warnings.filterwarnings("ignore")
O = os.path.dirname(os.path.abspath(__file__)); S = os.path.abspath(f"{O}/../..")
sys.path.insert(0, f"{S}/code"); sys.path.insert(0, O); sys.path.insert(0, f"{O}/pylib")
from lib_altin import *
import importlib.util
AG = "a3_takvim_olay"
# a3_analiz'in yardımcılarını yeniden tanımlamadan kullanmak için modülü test kaydı yapmadan içe aktarmak yerine burada yeniden kuruyoruz
d = load_viop(); s = load_spot(); V = d.index; r_v = d.v_ret
s_all = s; SPA = s.index
s_e = s[s.index < "2017-03-06"]; SPE = s_e.index
OUT = []
def first_ge(idx, dates, strict=False):
    a = idx.values; q = pd.DatetimeIndex(pd.to_datetime(pd.Series(dates)).dropna()).values
    p = np.searchsorted(a, q, side="right" if strict else "left"); return np.unique(p[p < len(idx)])
def dummy(idx, p, shift=0):
    p = np.asarray(p, int) + shift; p = p[(p >= 0) & (p < len(idx))]; D = pd.Series(0.0, index=idx); D.iloc[np.unique(p)] = 1.0; return D
def on_events(series, idx, p):
    x = pd.Series(np.nan, index=idx); p = p[(p >= 0) & (p < len(idx))]; x.iloc[p] = series.iloc[p].values; return x
def cal_pos(idx):
    g = pd.Series(np.arange(len(idx)), index=idx).groupby([idx.year, idx.month]); tdm = g.cumcount() + 1; n = g.transform("size"); return tdm.values, (n - tdm).values
def yearly(x, y, dummy_mode):
    dd = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna(); o = {}
    for yy, g in dd.groupby(dd.index.year):
        if dummy_mode:
            if (g.x == 1).sum() >= 1 and (g.x == 0).sum() >= 5: o[int(yy)] = round((g.y[g.x == 1].mean() - g.y[g.x == 0].mean()) * 1e4, 1)
        else:
            if len(g) >= 4: o[int(yy)] = round((np.sign(g.x) * g.y).mean() * 1e4, 1)
    return o
def st(x, y, h, dummy_mode, tag, family="derin", reg=True, desc=""):
    L = max(h, 5); f = ic(x, y, L, "pearson"); m = x.index <= IS_END
    a = ic(x[m], y[m], L, "pearson"); b = ic(x[~m], y[~m], L, "pearson"); yr = yearly(x, y, dummy_mode)
    sg = np.sign(f["ic"]); ys = sum(1 for v in yr.values() if np.sign(v) == sg)
    dd = pd.concat([x.rename("x"), y.rename("y")], axis=1).dropna()
    eff = ((dd.y[dd.x == 1].mean() - dd.y[dd.x == 0].mean()) if dummy_mode else (np.sign(dd.x) * dd.y).mean()) * 1e4
    o = dict(tag=tag, ic=f["ic"], t=f["t"], n=f["n"], t_is=a["t"], t_oos=b["t"], ic_oos=b["ic"], eff_bps=eff, yrs_same_sign=ys, yrs=len(yr), by_year=yr)
    if reg: register(AG, family, tag, desc or tag, h, o, note=json.dumps(dict(eff_bps=round(eff, 1), by_year=yr)))
    OUT.append(o); return o
def show(o): print(f"{o['tag']:<48} n={o['n']:>5} eff={o['eff_bps']:7.1f}bps t={o['t']:5.2f} IS={o['t_is']:5.2f} OOS={o['t_oos']:5.2f} yrs={o['yrs_same_sign']}/{o['yrs']}  {o['by_year']}")

tr_half = set(pd.read_csv(f"{O}/events_tr_bayram.csv", parse_dates=["arife"]).arife) | set(pd.Timestamp(y, 10, 28) for y in range(2009, 2027))
half_v = pd.Series(V.isin(list(tr_half)), index=V)
r1_v = np.log(d.xau_p15 / d.xau_p12).where(~half_v); r1_s = np.log(s_e.xau_p15 / s_e.xau_p12); r1_sa = np.log(s_all.xau_p15 / s_all.xau_p12)

print("=" * 30, "A) NFP koşullu momentum: spot 12->15 UTC işareti", "=" * 30)
nfp = pd.read_csv(f"{O}/events_us_nfp.csv", parse_dates=["date"]); cpi = pd.read_csv(f"{O}/events_us_cpi.csv", parse_dates=["date"])
E = first_ge(V, nfp.date); E = E[np.isin(V[E], nfp.date.values)]
Ec = first_ge(V, cpi.date); Ec = Ec[np.isin(V[Ec], cpi.date.values)]
for h in (1, 3, 5):
    show(st(on_events(r1_v, V, E), d[f"fwd{h}"], h, False, f"NFP_cond12to15_recheck_h{h}", reg=False))
# kontrol 1: aynı sinyal TÜM günlerde ve NFP DIŞI günlerde
allx = r1_v.copy(); nonev = r1_v.copy(); nonev.iloc[E] = np.nan; nonev.iloc[Ec] = np.nan
fri = r1_v.where(V.dayofweek == 4); fri_non = fri.copy(); fri_non.iloc[E] = np.nan
for h in (1, 3):
    show(st(np.sign(allx), d[f"fwd{h}"], h, False, f"CTRL_12to15_alldays_h{h}", "kontrol", desc="spot 12->15 işareti, tüm günler"))
    show(st(np.sign(nonev), d[f"fwd{h}"], h, False, f"CTRL_12to15_nonevent_h{h}", "kontrol", desc="spot 12->15 işareti, NFP/CPI dışı günler"))
    show(st(np.sign(fri_non), d[f"fwd{h}"], h, False, f"CTRL_12to15_friday_nonNFP_h{h}", "kontrol", desc="spot 12->15 işareti, NFP olmayan Cumalar"))
# sürekli tepki IC (işaret değil büyüklük) ve büyük tepkiler
xe = on_events(r1_v, V, E)
o = ic(xe, d.fwd1, 5, "spearman"); print("NFP sürekli Spearman IC h1:", round(o["ic"], 3), "t", round(o["t"], 2))
big = xe.where(xe.abs() > xe[xe.index <= IS_END].abs().median())
show(st(big, d.fwd1, 1, False, "NFP_cond12to15_bigIS-median_h1", "cpi_nfp", desc="NFP tepkisi |r|>IS medyanı olanlar"))
# en büyük 5 olay katkısı
ee = pd.concat([np.sign(xe).rename("s"), d.fwd1.rename("y")], axis=1).dropna(); ee["pnl"] = ee.s * ee.y * 1e4
print("en büyük katkılar:\n", ee.reindex(ee.pnl.abs().sort_values(ascending=False).index).head(8).round(1))
trim = ee.drop(ee.pnl.abs().sort_values(ascending=False).index[:5])
print("en büyük 5 hariç ort. %.1f bps, t(basit)=%.2f, n=%d" % (trim.pnl.mean(), trim.pnl.mean() / trim.pnl.std() * np.sqrt(len(trim)), len(trim)))
print("isabet: tüm %.2f  IS %.2f  OOS %.2f" % ((ee.pnl > 0).mean(), (ee.pnl[ee.index <= IS_END] > 0).mean(), (ee.pnl[ee.index > IS_END] > 0).mean()))
# spot uzun örneklem 2010-2026 (spot hedef)
Es = first_ge(SPA, nfp.date); Es = Es[np.isin(SPA[Es], nfp.date.values)]
xs = on_events(r1_sa, SPA, Es)
for lo, hi in [("2010", "2016-12-31"), ("2017", "2021-12-31"), ("2022", "2026-12-31")]:
    m = (SPA >= lo) & (SPA <= hi); o = ic(xs[m], s_all.sfwd1[m], 5, "pearson"); pnl = (np.sign(xs[m]) * s_all.sfwd1[m]).dropna()
    print(f"spot NFP 12->15 sinyal {lo}-{hi[:4]}: IC={o['ic']:.3f} t={o['t']:.2f} n={o['n']} ort={pnl.mean()*1e4:.1f}bps")
print("placebo_lead (NFP 12->15 işaret, h=1):", placebo_lead(np.sign(xe), r_v, 1))
bs = bt_summary(np.sign(xe).fillna(0), r_v, 1); print("backtest h1:", json.dumps(bs))
bs3 = bt_summary(np.sign(xe).fillna(0), r_v, 3); print("backtest h3:", json.dumps(bs3))
for lab, p in [("uzun bacak", np.sign(xe).clip(lower=0).fillna(0)), ("kısa bacak", np.sign(xe).clip(upper=0).fillna(0))]:
    b = bt_summary(p, r_v, 1); print(lab, "OOS sh", b["oos"]["sharpe"], "dm", b["oos"]["sharpe_demeaned"], "full", b["full"]["sharpe"])
oos = V > IS_END; b10 = backtest(np.sign(xe).fillna(0)[oos], r_v[oos], 1, 10); print("OOS 10bps sh", round(b10["sharpe"], 2))
# uzun-kısa bacak isabet/ortalama
for sg in (1, -1):
    q = ee[ee.s == sg]; print("x=%+d: n=%d ort fwd1=%.1f bps (IS %.1f, OOS %.1f)" % (sg, len(q), q.y.mean() * 1e4, q.y[q.index <= IS_END].mean() * 1e4, q.y[q.index > IS_END].mean() * 1e4))

print("=" * 30, "B) Çeyrek sonu ay dönümü", "=" * 30)
tdm, tde = cal_pos(V); tdm_s, tde_s = cal_pos(SPA)
qm = np.isin(V.month, [3, 6, 9, 12]); qm_s = np.isin(SPA.month, [3, 6, 9, 12])
nq = np.isin(V.month, [1, 2, 4, 5, 7, 8, 10, 11])
show(st(pd.Series((qm & (tde == 1)).astype(float), index=V), d.fwd3, 3, True, "QEND_TDE1_h3_recheck", reg=False))
show(st(pd.Series((np.isin(V.month, [3, 6, 9]) & (tde == 1)).astype(float), index=V), d.fwd3, 3, True, "QEND_exDec_TDE1_h3", "ceyrek_yil", desc="çeyrek sonu Aralık hariç"))
show(st(pd.Series((nq & (tde == 1)).astype(float), index=V), d.fwd3, 3, True, "MEND_nonQ_TDE1_h3", "ceyrek_yil", desc="çeyrek sonu OLMAYAN ay sonları TDE1 h3"))
# ayrıştırma: çeyrek son günü / yeni çeyrek 1. ve 2. gün tek tek (h=1)
for lab, c in [("Qlast_day", qm & (tde == 1)), ("Qnew_day1", qm & (tde == 0)), ("Qnew_day2", np.isin(V.month, [1, 4, 7, 10]) & (tdm == 1))]:
    show(st(pd.Series(c.astype(float), index=V), d.fwd1, 1, True, f"QDECOMP_{lab}_h1", "ceyrek_yil", desc=f"çeyrek dönümü ayrıştırma {lab}"))
# spot uzun örneklem
for lo, hi in [("2010", "2016-12-31"), ("2017", "2021-12-31"), ("2022", "2026-12-31")]:
    m = (SPA >= lo) & (SPA <= hi); x = pd.Series((qm_s & (tde_s == 1)).astype(float), index=SPA)[m]; y = s_all.sfwd3[m]
    o = ic(x, y, 5, "pearson"); print(f"spot çeyrek sonu TDE1 h3 {lo}-{hi[:4]}: t={o['t']:.2f} fark={(y[x==1].mean()-y[x==0].mean())*1e4:.1f}bps n_ev={int(x.sum())}")
pq = pd.Series((qm & (tde == 1)).astype(float), index=V)
bs = bt_summary(pq, r_v, 3); print("backtest QEND h3:", json.dumps(bs))
oos = V > IS_END; b10 = backtest(pq[oos], r_v[oos], 3, 10); print("OOS 10bps", round(b10["sharpe"], 2))
ev = pd.concat([pq.rename("x"), d.fwd3.rename("y")], axis=1); ev = ev[ev.x == 1]; print("olay bazında fwd3 (bps):", (ev.y * 1e4).round(0).to_dict())
print("placebo_lead:", placebo_lead(pq, r_v, 3))

print("=" * 30, "C) Bayram sonrası", "=" * 30)
bay = pd.read_csv(f"{O}/events_tr_bayram.csv", parse_dates=["start", "arife"])
post_b = np.searchsorted(V.values, bay.start.values); post_b = post_b[post_b < len(V)]
pb = dummy(V, post_b)
ev = pd.concat([pb.rename("x"), d.fwd5.rename("y"), d.v_code.rename("c")], axis=1); ev = ev[ev.x == 1]; print("olaylar fwd5 bps:\n", (ev.y * 1e4).round(0).to_string())
# spot: bayram sonrası ilk VİOP gününe denk gelen spot gün, 2010-2016 ve tam dönem
ends = []
for _, b in bay.iterrows():
    e = b.start + pd.Timedelta(days=int(b.days)); ends.append(e)
Ps = first_ge(SPA, ends)
for lo, hi in [("2010", "2016-12-31"), ("2017", "2026-12-31")]:
    m = (SPA >= lo) & (SPA <= hi); x = dummy(SPA, Ps)[m]; y = s_all.sfwd5[m]; o = ic(x, y, 5, "pearson")
    print(f"spot bayram sonrası h5 {lo}-{hi[:4]}: t={o['t']:.2f} fark={(y[x==1].mean()-y[x==0].mean())*1e4:.1f} n_ev={int(x.sum())}")
show(st(dummy(SPE, first_ge(SPE, ends)), s_e.sfwd5, 5, True, "BAYRAM_post_h5_spot_early", "tatil", desc="bayram sonrası 5 gün, spot 2010-2016"))
bs = bt_summary(-pb, r_v, 5); print("backtest kısa bayram sonrası h5:", json.dumps(bs))

print("=" * 30, "D) OG vade günü ve alternatif kural", "=" * 30)
cx = pd.read_csv(f"{O}/events_comex.csv", parse_dates=["og_expiry", "og_alt"])
for col in ["og_expiry", "og_alt"]:
    p = first_ge(V, cx[col]); show(st(dummy(V, p, -1), d.fwd1, 1, True, f"OGday_{col}_h1", "comex_vade" if col == "og_alt" else "derin", reg=(col == "og_alt"), desc="OG vade günü getirisi alternatif tarih"))
    ps = first_ge(SPA, cx[col])
    for lo, hi in [("2010", "2016-12-31"), ("2017", "2021-12-31"), ("2022", "2026-12-31")]:
        m = (SPA >= lo) & (SPA <= hi); x = dummy(SPA, ps, -1)[m]; y = s_all.sfwd1[m]; o = ic(x, y, 5, "pearson")
        print(f"   spot {col} {lo}-{hi[:4]}: t={o['t']:.2f} fark={(y[x==1].mean()-y[x==0].mean())*1e4:.1f}bps n={int(x.sum())}")

print("=" * 30, "E) Ocak etkisi", "=" * 30)
nm = pd.Series(np.r_[V.month[1:], [np.nan]], index=V)
x = (nm == 1).astype(float)
show(st(x[V < "2026-01-01"], d.fwd1[V < "2026-01-01"], 1, True, "MONTH_Oca_ex2026_h1", "ay_mevsim", desc="Ocak etkisi 2026 hariç"))
nms = pd.Series(np.r_[SPA.month[1:], [np.nan]], index=SPA)
for lo, hi in [("2010", "2016-12-31"), ("2017", "2026-12-31")]:
    m = (SPA >= lo) & (SPA <= hi); xx = (nms == 1).astype(float)[m]; y = s_all.sfwd1[m]; o = ic(xx, y, 5, "pearson")
    print(f"spot Ocak {lo}-{hi[:4]}: t={o['t']:.2f} fark={(y[xx==1].mean()-y[xx==0].mean())*1e4:.1f}bps/gün")


print("=" * 30, "F) NFP duyarlılık: tepki penceresi ve ayrıştırma", "=" * 30)
for a_, b_ in [("12", "14"), ("13", "15"), ("14", "15"), ("07", "12")]:
    rr = np.log(d[f"xau_p{b_}"] / d[f"xau_p{a_}"]).where(~half_v)
    lab = "placebo_önce" if a_ == "07" else "pencere"
    for h in (1, 3):
        show(st(on_events(rr, V, E), d[f"fwd{h}"], h, False, f"NFP_cond_{a_}to{b_}_h{h}", "cpi_nfp", desc=f"NFP {lab} spot {a_}:00->{b_}:00 UTC işareti"))
# ayrıştırma (yalnız tanı amaçlı, 15:10 sonrası veri kullanır -> sinyal değil): A = aynı gün 15->20 UTC, B = 20 UTC -> ertesi gün 15 UTC (spot)
sg = np.sign(on_events(r1_v, V, E)).dropna()
p15n = d.xau_p15.shift(-1)
A = (np.log(d.xau_p20 / d.xau_p15)).reindex(sg.index) * sg; B = (np.log(p15n / d.xau_p20)).reindex(sg.index) * sg
for lo, hi in [("2017", "2021-12-31"), ("2022", "2026-12-31")]:
    m = (sg.index >= lo) & (sg.index <= hi)
    print(f"NFP ayrıştırma {lo}-{hi[:4]}: aynı gün 15->20 UTC {A[m].mean()*1e4:.1f}bps (t={A[m].mean()/A[m].std()*np.sqrt(m.sum()):.2f}), 20 UTC->ertesi 15 UTC {B[m].mean()*1e4:.1f}bps (t={B[m].mean()/B[m].std()*np.sqrt(m.sum()):.2f}), n={m.sum()}")
# NFP sürpriz büyüklüğü vekili: |tepki| üst yarı / alt yarı OOS
xe2 = on_events(r1_v, V, E); dd = pd.concat([xe2.rename("x"), d.fwd1.rename("y")], axis=1).dropna(); dd["pnl"] = np.sign(dd.x) * dd.y
medi = dd.x.abs()[dd.index <= IS_END].median()
for nm_, q in [("büyük tepki", dd[dd.x.abs() > medi]), ("küçük tepki", dd[dd.x.abs() <= medi])]:
    print(f"  {nm_}: n={len(q)} ort={q.pnl.mean()*1e4:.1f}bps  IS={q.pnl[q.index<=IS_END].mean()*1e4:.1f} OOS={q.pnl[q.index>IS_END].mean()*1e4:.1f}")

print("=" * 30, "G) Çeyrek sonu parametre komşuluğu ve uzun spot örneklem", "=" * 30)
for lab_, cond_, h in [("TDE2_h3", qm & (tde == 2), 3), ("TDE0_h3", qm & (tde == 0), 3), ("TDE2_h5", qm & (tde == 2), 5), ("TDE0_h1", qm & (tde == 0), 1)]:
    show(st(pd.Series(cond_.astype(float), index=V), d[f"fwd{h}"], h, True, f"QEND_{lab_}", "ceyrek_yil", desc=f"çeyrek sonu komşu pencere {lab_}"))
x = pd.Series((qm_s & (tde_s == 1)).astype(float), index=SPA); o = ic(x, s_all.sfwd3, 5, "pearson")
print(f"spot 2010-2026 çeyrek sonu TDE1 h3: t={o['t']:.2f} fark={(s_all.sfwd3[x==1].mean()-s_all.sfwd3[x==0].mean())*1e4:.1f}bps n_ev={int(x.sum())}")
yr_s = {}
for yy in range(2010, 2027):
    m = SPA.year == yy; xx = x[m]; yv = s_all.sfwd3[m]
    if xx.sum() > 0: yr_s[yy] = round((yv[xx == 1].mean() - yv[xx == 0].mean()) * 1e4, 0)
print("spot yıllık fark (bps):", yr_s, " pozitif yıl:", sum(v > 0 for v in yr_s.values()), "/", len(yr_s))
# Haziran/Aralık (VİOP vade ayları) ve Mart/Eylül ayrı
for lab_, mm_ in [("Mar+Eyl", [3, 9]), ("Haz+Ara", [6, 12])]:
    c_ = np.isin(V.month, mm_) & (tde == 1); dd_ = d.fwd3[c_]
    print(f"  {lab_}: n={c_.sum()} ort fwd3={dd_.mean()*1e4:.1f}bps (koşulsuz {d.fwd3.mean()*1e4:.1f})")

print("=" * 30, "H) NFP pencere duyarlılığı erken spot; çeyrek sonu dolar kanalı", "=" * 30)
Ese = first_ge(SPE, nfp.date); Ese = Ese[np.isin(SPE[Ese], nfp.date.values)]
for a_, b_ in [("13", "15"), ("14", "15")]:
    rr = np.log(s_e[f"xau_p{b_}"] / s_e[f"xau_p{a_}"])
    for h in (1, 3):
        show(st(on_events(rr, SPE, Ese), s_e[f"sfwd{h}"], h, False, f"NFP_cond_{a_}to{b_}_h{h}_spotearly", "cpi_nfp", desc=f"NFP {a_}->{b_} spot 2010-2016"))
# dolar kanalı (tanı): çeyrek sonu TDE1 girişinde EURUSD ve DXY'nin sonraki 3 günlük 15:00 UTC değişimi
for sym in ["EURUSD", "DOLLARIDXUSD"]:
    c = f"dk_{sym}_p15"
    if c in d.columns:
        px = d[c]; f3 = np.log(px.shift(-3) / px)
        x = pd.Series((qm & (tde == 1)).astype(float), index=V)
        o = ic(x, f3, 5, "pearson"); print(f"  {sym} fwd3 çeyrek sonu: t={o['t']:.2f} fark={(f3[x==1].mean()-f3[x==0].mean())*1e4:.1f}bps n={o['n']}")
        x2 = pd.Series((nq & (tde == 1)).astype(float), index=V); o2 = ic(x2, f3, 5, "pearson")
        print(f"  {sym} fwd3 çeyrek-dışı ay sonu: t={o2['t']:.2f} fark={(f3[x2==1].mean()-f3[x2==0].mean())*1e4:.1f}bps")

pd.DataFrame(OUT).to_csv(f"{O}/results_derin.csv", index=False)
print("registry toplam satır:", len(pd.read_csv(f"{REG_DIR}/{AG}.csv")))
