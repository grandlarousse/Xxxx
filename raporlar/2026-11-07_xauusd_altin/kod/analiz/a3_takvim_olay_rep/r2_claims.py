"""Bağımsız yeniden üretim — 6 iddia. Girdi: base.parquet (r0), spot_daily.parquet + cal_*.csv (r1). lib_altin / analist kodu KULLANILMADI."""
import json, numpy as np, pandas as pd
from rlib import *
S = "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad"
O = f"{S}/out/a3_takvim_olay_rep"
B = pd.read_parquet(f"{O}/base.parquet"); V = B.index; r = B.ret
SP = pd.read_parquet(f"{O}/spot_daily.parquet"); SPI = SP.index
Y = {h: B[f"fwd{h}"] for h in (1, 3, 5)}
NFP = pd.DatetimeIndex(pd.to_datetime(pd.read_csv(f"{O}/cal_nfp.csv").date))
OG = pd.read_csv(f"{O}/cal_og.csv", parse_dates=["og", "d4", "alt"])
BY = pd.read_csv(f"{O}/cal_bayram.csv", parse_dates=["start", "arife"])
HALF = set(pd.to_datetime(pd.read_csv(f"{O}/cal_halfdays.csv").date))
RES = {}
OUTL = lambda idx: ((idx >= "2020-03-01") & (idx <= "2020-03-31")) | ((idx >= "2026-01-01") & (idx <= "2026-02-28"))
roll = (B.code != B.code.shift()).astype(float); roll.iloc[0] = 0
def touches_roll(h): return sum(roll.shift(-k).fillna(0) for k in range(1, h + 1)) > 0
def ser(idx, mask): return pd.Series(np.asarray(mask, float), index=idx)
def tde_tdm(idx):
    g = pd.Series(np.arange(len(idx)), index=idx).groupby([idx.year, idx.month])
    tdm = g.cumcount() + 1; n = g.transform("size"); return (n - tdm).values, tdm.values
def P(o, keys): print("   ", fmt(o, keys))
def ev_of(D, y): e = pd.concat([D.rename("D"), y.rename("y")], axis=1); return e[e.D == 1].y

print("Al-tut Sharpe (VİOP v_ret): tam %.2f  IS %.2f  OOS %.2f" % tuple(r[m].mean() / r[m].std() * np.sqrt(252) for m in [np.ones(len(r), bool), V <= IS_END, V > IS_END]))

# =========================== 1) QEND_TDE1_h3 ===========================
print("\n==== A3_QEND_h3 ====")
tde, tdm = tde_tdm(V); qm = np.isin(V.month, [3, 6, 9, 12])
D = ser(V, qm & (tde == 1))
evd = D[D == 1].index
print("  olay sayısı", len(evd), " ilk/son", evd[0].date(), evd[-1].date())
o = dummy_test(D, Y[3], 3, "QEND_TDE1_h3"); RES["QEND"] = o
P(o, ["n_ev", "ev_mean_full", "non_mean_full", "diff_full", "diff_is", "diff_oos", "t_full", "t_is", "t_oos", "ic_full", "hit", "yrs_same"])
print("    yıllık fark:", o["by_year"])
bt = bt_block(D, r, 3); RES["QEND_bt"] = bt
P(bt, ["sh_full", "sh_is", "sh_oos", "sh_oos_dm", "sh_oos_10", "sh_oos_0", "bh_oos", "bh_full", "long_oos", "trades_per_year"])
# sağlamlık
keep = ~OUTL(V); print("    uç dönem hariç t:", round(reg_t(D[keep], Y[3][keep], 5)[0], 2))
keep = ~touches_roll(3).values; print("    roll içeren pencereler hariç t:", round(reg_t(D[keep], Y[3][keep], 5)[0], 2))
print("    Spearman (rank y) t:", round(reg_t(D, Y[3].rank(), 5)[0], 2))
print("    Aralık hariç:", fmt(dummy_test(ser(V, np.isin(V.month, [3, 6, 9]) & (tde == 1)), Y[3], 3), ["n_ev", "diff_full", "t_full"]))
print("    çeyrek dışı ay sonu TDE1 h3:", fmt(dummy_test(ser(V, ~qm & (tde == 1)), Y[3], 3), ["n_ev", "diff_full", "t_full", "t_is", "t_oos"]))
for lab, c, h in [("TDE0_h3", qm & (tde == 0), 3), ("TDE2_h3", qm & (tde == 2), 3), ("TDE2_h5", qm & (tde == 2), 5), ("TDE1_h1", qm & (tde == 1), 1), ("TDE1_h5", qm & (tde == 1), 5)]:
    print(f"    komşu {lab}:", fmt(dummy_test(ser(V, c), Y[h], h), ["n_ev", "diff_full", "t_full", "t_is", "t_oos"]))
# olay başına gerçek işlem: tam pozisyon, net 5 bps
e3 = ev_of(D, Y[3]) * 1e4
print("    olay başına (tam pozisyon) ort brüt %.1f, net(5bps) %.1f bps; OOS net %.1f; medyan %.1f; en iyi 3 olay hariç ort %.1f" % (
    e3.mean(), e3.mean() - 5, e3[e3.index > IS_END].mean() - 5, e3.median(), e3.drop(e3.sort_values().index[-3:]).mean()))
print("    t (olay getirileri, sabit ortalama=0, h3 çakışmasız):", round(mean_t(e3, 0), 2), "| olay ort - koşulsuz ort:", round(e3.mean() - Y[3].mean() * 1e4, 1))
# 2026 hariç
k = V < "2026-01-01"; print("    2026 hariç:", fmt(dummy_test(D[k], Y[3][k], 3), ["n_ev", "diff_full", "t_full"]))
# spot uzun örneklem (kendi spot takvimim)
tde_s, _ = tde_tdm(SPI); Ds = ser(SPI, np.isin(SPI.month, [3, 6, 9, 12]) & (tde_s == 1))
for lo, hi in [("2010-01-01", "2016-12-31"), ("2010-01-01", "2017-03-05"), ("2017-03-06", "2021-12-31"), ("2022-01-01", "2026-12-31"), ("2010-01-01", "2026-12-31")]:
    m = (SPI >= lo) & (SPI <= hi); oo = dummy_test(Ds[m], SP.sfwd3[m], 3)
    print(f"    spot {lo[:7]}..{hi[:7]}:", fmt(oo, ["n_ev", "diff_full", "t_full", "yrs_same"]))
# VİOP döneminde spot hedefle (aynı olay günleri)
sp_on_v = SP.sfwd3.reindex(V)
print("    VİOP olay günlerinde spot 15:00 hedef:", fmt(dummy_test(D, sp_on_v, 3), ["n_ev", "diff_full", "t_full", "t_is", "t_oos"]))

# =========================== 2-3) NFP_MOM h1 / h3 ===========================
print("\n==== A3_NFP_MOM ====")
ev = [d for d in NFP if d in set(V)]
ev_ok = [d for d in ev if d not in HALF]
print("  NFP yayımı (VİOP dönemi):", len([d for d in NFP if V[0] <= d <= V[-1]]), " VİOP açık:", len(ev), " yarım gün dışı:", len(ev_ok), " yarım gün olan:", sorted(set(ev) - set(ev_ok)))
x = pd.Series(np.nan, index=V); x.loc[ev_ok] = np.log(B.p15 / B.p12).reindex(ev_ok).values
print("  x NaN (spot eksik):", int(x.loc[ev_ok].isna().sum()), " geçerli olay:", int(x.notna().sum()))
for h in (1, 3):
    o = cond_test(x, Y[h], h, f"NFP_h{h}"); RES[f"NFP_h{h}"] = o
    print(f"  h={h}:"); P(o, ["n_full", "ic_full", "tIC_full", "tIC_is", "tIC_oos", "sgn_mean_full", "sgn_mean_is", "sgn_mean_oos", "t_sgnmean_full", "t_sgnmean_is", "t_sgnmean_oos",
                            "t_sgnreg_full", "t_sgnreg_is", "t_sgnreg_oos", "hit_full", "hit_is", "hit_oos", "yrs_same_ic", "yrs_same_sgnmean"])
    print("    yıllık ort(sign·y):", o["by_year_sgnmean"])
    pos = np.sign(x).fillna(0)
    bt = bt_block(pos, r, h); RES[f"NFP_bt_h{h}"] = bt
    P(bt, ["sh_full", "sh_is", "sh_oos", "sh_oos_dm", "sh_oos_10", "sh_oos_0", "bh_oos", "long_oos", "short_oos", "long_oos_dm", "short_oos_dm", "trades_per_year"])
    pnl = (np.sign(x) * Y[h]).dropna() * 1e4
    top = pnl.abs().sort_values(ascending=False).index[:5]
    tr = pnl.drop(top); print("    en büyük |katkı| 5 olay hariç: ort %.1f bps, t %.2f, n %d; en büyük 5:" % (tr.mean(), mean_t(tr, 0), len(tr)), pnl.loc[top].round(0).to_dict())
    best = pnl.sort_values().index[-5:]; tb = pnl.drop(best); print("    en KÂRLI 5 olay hariç: ort %.1f bps, t %.2f" % (tb.mean(), mean_t(tb, 0)))
    for sg in (1, -1):
        q = pnl[np.sign(x.reindex(pnl.index)) == sg] * sg
        print(f"    x={sg:+d}: n={len(q)} ort fwd{h}={q.mean():.1f} bps (IS {q[q.index <= IS_END].mean():.1f}, OOS {q[q.index > IS_END].mean():.1f})")
# kontroller
x_all = np.log(B.p15 / B.p12).where(~V.isin(list(HALF)))
xn = x_all.copy(); xn.loc[ev] = np.nan
fri = x_all.where(V.dayofweek == 4); fri.loc[ev] = np.nan
for lab, xx in [("tüm günler", x_all), ("NFP dışı günler", xn), ("NFP olmayan Cumalar", fri)]:
    o = cond_test(np.sign(xx), Y[1], 1); print(f"  kontrol {lab} h1:", fmt(o, ["n_full", "sgn_mean_full", "tIC_full", "t_sgnmean_full"]))
pl = pd.Series(np.nan, index=V); pl.loc[ev_ok] = np.log(B.p12 / B.p07).reindex(ev_ok).values
print("  placebo 07->12 h1:", fmt(cond_test(pl, Y[1], 1), ["n_full", "tIC_full", "sgn_mean_full", "t_sgnmean_full"]))
# uzlaşma hizası (ileriye bakma kontrolü): NFP günlerinde uzlaşma 15:00 sonrası fiyatı mı yansıtıyor?
g = B.ret - np.log(B.p15 / B.p15.shift(1))
gg = pd.concat([g.rename("g"), x.rename("x")], axis=1).dropna()
print("  NFP günü: (v_ret - spot 15->15) ile x korelasyonu: %.3f (negatifse uzlaşma bayat -> ileriye bakma riski)  medyan |g| %.1f bps" % (gg.g.corr(gg.x), gg.g.abs().median() * 1e4))
e15 = (B.ret - np.log(B.p15 / B.p15.shift(1))).abs(); e10 = (B.ret - np.log(B.p10 / B.p15.shift(1))).abs()
sus = [d for d in ev_ok if e10[d] < 0.5 * e15[d] and e15[d] > 15e-4]
print("  şüpheli (uzlaşma 10:00'a daha yakın) NFP günleri:", [d.date().isoformat() for d in sus])
x2 = x.copy(); x2.loc[sus] = np.nan
for h in (1, 3): print(f"  şüpheliler hariç h{h}:", fmt(cond_test(x2, Y[h], h), ["n_full", "tIC_full", "sgn_mean_full", "t_sgnmean_full", "t_sgnmean_oos"]))
# spot hedefle aynı olaylar (VİOP dönemi) ve erken spot
for h in (1, 3):
    print(f"  VİOP olaylarında spot hedef sfwd{h}:", fmt(cond_test(x, SP[f"sfwd{h}"].reindex(V), h), ["n_full", "tIC_full", "tIC_is", "tIC_oos", "sgn_mean_full", "sgn_mean_oos"]))
evs = [d for d in NFP if d in set(SPI)]
xs = pd.Series(np.nan, index=SPI); xs.loc[evs] = np.log(SP.p15 / SP.p12).reindex(evs).values
for lo, hi in [("2010-01-01", "2016-12-31"), ("2010-01-01", "2017-03-05"), ("2017-03-06", "2021-12-31"), ("2022-01-01", "2026-12-31")]:
    m = (SPI >= lo) & (SPI <= hi)
    for h in (1, 3):
        oo = cond_test(xs[m], SP[f"sfwd{h}"][m], h)
        print(f"  spot {lo[:7]}..{hi[:7]} h{h}:", fmt(oo, ["n_full", "ic_full", "tIC_full", "sgn_mean_full", "t_sgnmean_full", "t_sgnreg_full"]))

# =========================== 4) OG vade günü ===========================
print("\n==== A3_OG_EXPIRY_DAY ====")
def og_dummy(dates, idx, require_open=False):
    p = np.searchsorted(idx.values, pd.DatetimeIndex(dates).values, side="left")
    ok = (p > 0) & (p < len(idx))
    p = p[ok]; dd = pd.DatetimeIndex(dates)[ok]
    if require_open: m = idx[p] == dd; p = p[m]
    D = pd.Series(0.0, index=idx); D.iloc[np.unique(p - 1)] = 1.0; return D, p
og_in = OG.og[(OG.og >= V[0]) & (OG.og <= V[-1])]
Dog, p = og_dummy(og_in, V)
nopen = int((V[p] != pd.DatetimeIndex(og_in)[: len(p)]).sum())
print("  OE tarihleri (VİOP dönemi):", len(og_in), " olay:", int(Dog.sum()), " OE günü VİOP kapalı (sonraki güne kayan):", nopen)
o = dummy_test(Dog, Y[1], 1); RES["OG"] = o
P(o, ["n_ev", "ev_mean_full", "non_mean_full", "diff_full", "diff_is", "diff_oos", "t_full", "t_is", "t_oos", "hit", "yrs_same"]); print("    yıllık:", o["by_year"])
bt = bt_block(-Dog, r, 1); RES["OG_bt"] = bt
P(bt, ["sh_full", "sh_is", "sh_oos", "sh_oos_dm", "sh_oos_10", "bh_oos", "short_oos", "short_oos_dm", "trades_per_year"])
Dog2, _ = og_dummy(og_in, V, require_open=True); print("  yalnız OE günü VİOP açık:", fmt(dummy_test(Dog2, Y[1], 1), ["n_ev", "diff_full", "t_full", "t_is", "t_oos"]))
# alternatif: 5. son iş günü (Cuma kuralı yok) ve d4 (düzeltmesiz 4. son iş günü)
for col in ["alt", "d4"]:
    dts = OG[col][(OG[col] >= V[0]) & (OG[col] <= V[-1])]
    print(f"  alternatif tarih {col}:", fmt(dummy_test(og_dummy(dts, V)[0], Y[1], 1), ["n_ev", "diff_full", "t_full", "t_is", "t_oos"]))
keep = ~OUTL(V); print("  uç dönem hariç t:", round(reg_t(Dog[keep], Y[1][keep], 5)[0], 2))
k = V < "2026-01-01"; print("  2026 hariç:", fmt(dummy_test(Dog[k], Y[1][k], 1), ["n_ev", "diff_full", "t_full", "t_oos"]))
Dsog, _ = og_dummy(OG.og[(OG.og >= SPI[0]) & (OG.og <= SPI[-1])], SPI)
for lo, hi in [("2010-01-01", "2016-12-31"), ("2017-03-06", "2021-12-31"), ("2022-01-01", "2026-12-31")]:
    m = (SPI >= lo) & (SPI <= hi); print(f"  spot {lo[:7]}..{hi[:7]}:", fmt(dummy_test(Dsog[m], SP.sfwd1[m], 1), ["n_ev", "diff_full", "t_full"]))

# =========================== 5) Bayram sonrası ===========================
print("\n==== A3_BAYRAM_POST ====")
byv = BY[(BY.start >= V[0]) & (BY.start <= V[-1])]
post = [V[V > s][0] for s in byv.start]
Db = pd.Series(0.0, index=V); Db.loc[post] = 1.0
print("  olay sayısı (doğru):", int(Db.sum()), [d.date().isoformat() for d in post])
o = dummy_test(Db, Y[5], 5); RES["BAY"] = o
P(o, ["n_ev", "ev_mean_full", "non_mean_full", "diff_full", "diff_is", "diff_oos", "t_full", "t_is", "t_oos", "hit", "yrs_same"]); print("    yıllık:", o["by_year"])
bt = bt_block(-Db, r, 5); RES["BAY_bt"] = bt
P(bt, ["sh_full", "sh_is", "sh_oos", "sh_oos_dm", "sh_oos_10", "bh_oos", "short_oos", "trades_per_year"])
print("    olay fwd5 (bps):", (ev_of(Db, Y[5]) * 1e4).round(0).to_dict())
# analistin 21 olaylı sürümü: 2017-03-06 (panel ilk günü) sahte olay dahil
Db21 = Db.copy(); Db21.iloc[0] = 1.0
o21 = dummy_test(Db21, Y[5], 5); print("  + 2017-03-06 sahte olay (analist sürümü):", fmt(o21, ["n_ev", "ev_mean_full", "diff_full", "t_full", "t_is", "t_oos", "hit", "yrs_same"]))
print("    2017-03-06 fwd5 = %.0f bps" % (Y[5].iloc[0] * 1e4))
bt21 = bt_block(-Db21, r, 5); P(bt21, ["sh_full", "sh_is", "sh_oos", "sh_oos_dm"])
keep = ~touches_roll(5).values; print("  roll hariç t (doğru):", round(reg_t(Db[keep], Y[5][keep], 5)[0], 2))
# erken spot: bayram bitişinden sonraki ilk spot günü
bys = BY[(BY.start >= "2010-01-01")]
ends = bys.start + pd.to_timedelta(bys.ndays, unit="D")
ps = [SPI[SPI >= e][0] for e in ends if e <= SPI[-1]]
Dbs = pd.Series(0.0, index=SPI); Dbs.loc[ps] = 1.0
for lo, hi in [("2010-01-01", "2016-12-31"), ("2017-03-06", "2026-12-31")]:
    m = (SPI >= lo) & (SPI <= hi); print(f"  spot {lo[:7]}..{hi[:7]}:", fmt(dummy_test(Dbs[m], SP.sfwd5[m], 5), ["n_ev", "diff_full", "t_full", "yrs_same"]))
Dbs15 = Dbs.copy(); Dbs15.iloc[0] = 1.0; m = (SPI <= "2016-12-31")
print("  spot 2010-2016 + 2010-01-04 sahte olay (analist):", fmt(dummy_test(Dbs15[m], SP.sfwd5[m], 5), ["n_ev", "diff_full", "t_full"]))

# =========================== 6) Ocak ===========================
print("\n==== A3_JANUARY ====")
nm = pd.Series(np.r_[V.month[1:], [0]], index=V)
Dj = (nm == 1).astype(float)
o = dummy_test(Dj, Y[1], 1); RES["JAN"] = o
P(o, ["n_ev", "ev_mean_full", "non_mean_full", "diff_full", "diff_is", "diff_oos", "t_full", "t_is", "t_oos", "ic_full", "hit", "yrs_same"]); print("    yıllık:", o["by_year"])
bt = bt_block(Dj, r, 1); RES["JAN_bt"] = bt
P(bt, ["sh_full", "sh_is", "sh_oos", "sh_oos_dm", "sh_oos_10", "bh_oos", "long_oos", "trades_per_year"])
k = V < "2026-01-01"; print("  2026 hariç:", fmt(dummy_test(Dj[k], Y[1][k], 1), ["n_ev", "diff_full", "t_full", "t_is", "t_oos"]))
keep = ~OUTL(V); print("  uç dönem hariç t:", round(reg_t(Dj[keep], Y[1][keep], 5)[0], 2))
# Ocak ortalaması 2026 Ocak'a ne kadar bağlı
jr = ev_of(Dj, Y[1]); print("  Ocak günlük ort (bps): tümü %.1f, 2026 hariç %.1f, Ocak 2026 %.1f (n=%d)" % (jr.mean() * 1e4, jr[jr.index < "2026-01-01"].mean() * 1e4, jr[jr.index >= "2026-01-01"].mean() * 1e4, (jr.index >= "2026-01-01").sum()))
nms = pd.Series(np.r_[SPI.month[1:], [0]], index=SPI); Djs = (nms == 1).astype(float)
for lo, hi in [("2010-01-01", "2016-12-31"), ("2010-01-01", "2017-03-05"), ("2017-03-06", "2026-12-31")]:
    m = (SPI >= lo) & (SPI <= hi); print(f"  spot {lo[:7]}..{hi[:7]}:", fmt(dummy_test(Djs[m], SP.sfwd1[m], 1), ["n_ev", "diff_full", "t_full"]))
# 12 ay çoklu test bağlamı: kendi hesabımla 12 ayın t'leri
ts = {mm_: round(dummy_test((nm == mm_).astype(float), Y[1], 1)["t_full"], 2) for mm_ in range(1, 13)}
print("  12 ayın t'leri:", ts)

json.dump({k: {kk: (vv if not isinstance(vv, (np.floating, np.integer)) else float(vv)) for kk, vv in v.items()} for k, v in RES.items()},
          open(f"{O}/results_rep.json", "w"), indent=1, default=str, ensure_ascii=False)
print("\nyazıldı:", f"{O}/results_rep.json")
