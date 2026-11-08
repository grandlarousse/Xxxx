"""r1: sinyalleri ham tablolardan kur + her sinyal bileseninin bilgi anini ham zaman damgasiyla dogrula.
Karar ani (cutoff) = NYSE gunu t 15:00 America/New_York. Giris = t 16:00 ET adjclose.
"""
import sys, json
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/e2_etf_leadlag_rep")
from rep_lib import *

cal = nyse_calendar()
cut = at_local(cal, 15, 0, NY)                         # gun t cutoff UTC
close_ny = at_local(cal, 16, 0, NY)                    # gun t ABD kapanisi UTC
cut_s = pd.Series(cut, index=cal)
prev = pd.Series(cal, index=cal).shift(1)              # bir onceki NYSE gunu

# ---------- ABD ETF'leri (adjclose, NYSE takvimi) ----------
US = ["GLD", "GDX", "GDXJ", "SPY", "GLL", "DUST", "JDST"]
LP = {}
for tk in US:
    s = yahoo(tk)
    LP[tk] = np.log(s.reindex(cal))
R = {tk: LP[tk].diff() for tk in US}                   # gun t getirisi (t-1 -> t kapanis); hedef/giris icindir

viol = {}
# ---------- madenci artiklari (GLD+SPY, 250 gun, beta_{t-1}) ----------
SIG = {}
X = pd.concat([R["GLD"], R["SPY"]], axis=1); X.columns = ["GLD", "SPY"]
RES = {}
for und in ("GDX", "GDXJ"):
    for minp in (60, 250):
        B = roll_ols(R[und], X, 250, minp)                # t dahil pencere
        Bl = B.shift(1)                                   # beta_{t-1}
        e = R[und] - Bl["GLD"] * R["GLD"] - Bl["SPY"] * R["SPY"]   # e_t: t-1 -> t kapanis getirileri
        RES[(und, minp)] = e
        for k in (1, 3, 5, 10):
            x = e.rolling(k, min_periods=k).sum().shift(1)          # gun t'de: e_{t-1}+...+e_{t-k}
            SIG[(f"{und}res", k, minp)] = x
# bilgi ani: x_t'nin kullandigi en gec ABD kapanisi = onceki NYSE gunu 16:00 ET
info_us = at_local(prev.dropna().values, 16, 0, NY)
info_us = pd.Series(info_us, index=prev.dropna().index)
# x_t'yi gercekten t-1 verisinden mi kuruyoruz? Kontrol: x_t'yi yalniz t-1'e kadar kesilmis veriyle yeniden hesapla (rastgele 40 gun)
rng = np.random.default_rng(0)
chk_days = rng.choice(np.arange(400, len(cal) - 5), 40, replace=False)
mx = 0.0
for i in chk_days:
    t = cal[i]
    Rc = {tk: R[tk][R[tk].index <= cal[i - 1]] for tk in ("GDXJ", "GLD", "SPY")}
    Xc = pd.concat([Rc["GLD"], Rc["SPY"]], axis=1); Xc.columns = ["GLD", "SPY"]
    Bc = roll_ols(Rc["GDXJ"].iloc[-260:], Xc.iloc[-260:], 250, 60)
    e_last = Rc["GDXJ"].iloc[-1] - Bc["GLD"].iloc[-2] * Rc["GLD"].iloc[-1] - Bc["SPY"].iloc[-2] * Rc["SPY"].iloc[-1]
    v = SIG[("GDXJres", 1, 60)].loc[t]
    if np.isfinite(v) and np.isfinite(e_last): mx = max(mx, abs(v - e_last))
viol["C2j_truncation_recompute_maxabsdiff"] = mx
viol["US_close_t-1_before_cutoff_min_margin_h"] = float(((cut_s.loc[info_us.index] - info_us).dt.total_seconds() / 3600).min())
viol["US_close_t-1_before_cutoff_max_margin_h"] = float(((cut_s.loc[info_us.index] - info_us).dt.total_seconds() / 3600).max())
viol["US_close_t_after_cutoff_h"] = float(((pd.Series(close_ny, index=cal) - cut_s).dt.total_seconds() / 3600).min())

# ---------- Platin (PL=F), t-1 kapanisi (17:00 ET varsayimi) ----------
pl = yahoo("PL_F"); pl = pl[pl.index >= "2007-06-01"]
# NY gunu t icin: tarihi < t olan son PL kapanisi
ipos = pl.index.searchsorted(cal, side="left") - 1
pl_asof = pd.Series(pl.values[ipos], index=cal); pl_date = pd.Series(pl.index[ipos], index=cal)
pl_info = pd.Series(at_local(pl_date.values, 17, 0, NY), index=cal)
viol["PL_info_before_cutoff_violations"] = int((pl_info >= cut_s).sum())
viol["PL_min_margin_h"] = float(((cut_s - pl_info).dt.total_seconds() / 3600).min())
viol["PL_stale_days_gt4"] = int(((cal - pl_date.values).days > 4).sum())
lpl = np.log(pl_asof)
SIG["PL_d5"] = lpl - lpl.shift(5)
SIG["PL_d1"] = lpl - lpl.shift(1)
# Yahoo PL=F daily bar ts_utc: seans/bar anlami
pl_raw = pd.read_parquet(f"{P}/yahoo/PL_F.parquet")
viol["PL_ts_local_hours"] = pl_raw.ts_utc.dt.tz_convert(NY).dt.strftime("%H:%M").value_counts().head(3).to_dict()

# ---------- Spot altin ----------
ph, pm = gold_price_series()
xcut, xcut_ts = price_at(ph, pm, cut)
xclose, xclose_ts = price_at(ph, pm, close_ny)
xcut = pd.Series(xcut.values, index=cal); xclose = pd.Series(xclose.values, index=cal)
viol["xau_cut_stamp_after_cutoff"] = int((pd.Series(xcut_ts, index=cal) > cut_s).sum())
viol["xau_cut_missing"] = int(xcut.isna().sum())
viol["xau_cut_stale_gt1h"] = int(((cut_s - pd.Series(xcut_ts, index=cal)).dt.total_seconds() > 3600).sum())
gi = np.log(xcut) - np.log(xclose).shift(1)            # [t-1 16:00 ET -> t 15:00 ET]
SIG["gi"] = gi
# panel ile karsilastirma (yalniz kontrol)
pan = pd.read_parquet(f"{P}/panel_etf.parquet"); pan.index = pd.to_datetime(pan.index)
viol["xau_cut_vs_panel_maxreldiff"] = float((xcut / pan["xau_cut"] - 1).abs().max())
viol["xau_close_vs_panel_maxreldiff"] = float((xclose / pan["xau_close"] - 1).abs().max())
viol["c_GDXJ_vs_panel_maxreldiff"] = float((np.exp(LP["GDXJ"]) / pan["c_GDXJ"] - 1).abs().max())

# ---------- Asya madencileri: kendi yerel takvimlerinde ----------
x07_ts = None
ASIA = [("2899.HK", "_HSI", "Asia/Hong_Kong", (16, 10)), ("1818.HK", "_HSI", "Asia/Hong_Kong", (16, 10)), ("600547.SS", "000001.SS", "Asia/Shanghai", (15, 0))]
EA = {}
asia_info = {}
for stk, idx, tz, (hh, mm) in ASIA:
    ps = yahoo(stk); pi = yahoo(idx)
    ps = ps[ps.index >= "2006-01-01"].dropna(); pi = pi.reindex(ps.index)
    D = ps.index
    t07 = at_local(D, 7, 0, "UTC") if False else pd.DatetimeIndex(D).tz_localize("UTC") + pd.Timedelta(hours=7)
    g07, g07ts = price_at(ph, pm, t07)
    g07 = pd.Series(g07.values, index=D)
    rs = np.log(ps).diff(); rm = np.log(pi).diff(); rg = np.log(g07).diff()
    XX = pd.concat([rg.rename("g"), rm.rename("m")], axis=1)
    B = roll_ols(rs, XX, 250, 120).shift(1)            # beta_{D-1}
    e = rs - B["g"] * rg - B["m"] * rm
    EA[stk] = e
    loc_close = at_local(D, hh, mm, tz)
    asia_info[stk] = pd.Series(loc_close, index=D)
    # gold 07 UTC < yerel kapanis? (HK: 07:00 < 08:10; SS: 07:00 = 07:00)
# NY gunu t ile ayni takvim tarihli yerel gun
E = pd.concat({k: v.reindex(cal) for k, v in EA.items()}, axis=1)
comp = E.mean(axis=1, skipna=True)
SIG["asia1"] = comp
SIG["asia5"] = comp.fillna(0).rolling(5, min_periods=1).sum()
SIG["asia5"][comp.rolling(5, min_periods=1).count() == 0] = np.nan
# bilgi ani kontrolu: kullanilan yerel kapanis (tarih t) UTC < cutoff t
mviol = 0; mmin = 1e9
for stk in EA:
    inf = asia_info[stk].reindex(cal)
    ok = E[stk].notna()
    dd = (cut_s[ok] - inf[ok]).dt.total_seconds() / 3600
    mviol += int((dd <= 0).sum()); mmin = min(mmin, float(dd.min()))
viol["ASIA_violations"] = mviol; viol["ASIA_min_margin_h"] = mmin
viol["ASIA_coverage_first"] = str(E.dropna(how="all").index.min().date())
viol["ASIA_days_with_any"] = int(comp.notna().sum())

# ---------- ters ETF agirligi (1/|beta60|, t-1'e kadar) ----------
W = {}
for und, inv in (("GLD", "GLL"), ("GDX", "DUST"), ("GDXJ", "JDST")):
    cv = R[inv].rolling(60, min_periods=40).cov(R[und]); vr = R[und].rolling(60, min_periods=40).var()
    W[inv] = (1 / (cv / vr).abs()).clip(0.2, 1.0).shift(1)

pd.to_pickle(dict(SIG=SIG, R=R, LP=LP, W=W, cal=cal, RES=RES, E=E), f"{OUT}/r1_signals.pkl")
json.dump(viol, open(f"{OUT}/r1_zaman_denetimi.json", "w"), indent=1, default=str)
print(json.dumps(viol, indent=1, default=str))
# ters ETF veri kalitesi: uc gunluk getiriler
for und, inv in (("GLD", "GLL"), ("GDX", "DUST"), ("GDXJ", "JDST")):
    rr = pd.concat([R[inv], R[und]], axis=1).dropna(); rr.columns = ["inv", "und"]
    ratio = rr.inv / rr.und
    bad = rr[(rr.inv.abs() > 0.3) | ((rr.und.abs() > 0.01) & ((ratio > 0) | (ratio < -4.5)))]
    print(inv, "supheli gun:", len(bad)); print(bad.head(8).round(4).to_string())
