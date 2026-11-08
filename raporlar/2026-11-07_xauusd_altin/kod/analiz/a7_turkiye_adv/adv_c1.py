"""Hakem: C1 (USDTRY carry zamanlaması) ve C2 (USDTRY sürüklenme tahmini) saldırıları."""
import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/code")
import numpy as np, pandas as pd
import lib_altin as L
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
p = L.load_viop()
isx = p.index <= L.IS_END
lfx = np.log(p.dk_USDTRY_p15)
ur = p.vo_usdtry_ret
dte = p.vo_usdtry_dte

def make_sig(w=20, coef=1.4, clip=3, lag=1, mindte=0):
    bpd = np.log(p.vo_usdtry_settle / p.dk_USDTRY_p15) / dte.clip(lower=clip)
    if mindte > 0:
        bpd = bpd.where(dte >= mindte)
    s = lfx.diff().rolling(w).mean() - bpd * coef
    return s.shift(lag)

sig = make_sig()
pos = np.sign(sig).fillna(0)
print("=== C1 yeniden üretim ===")
for h in (1, 3, 5):
    st = L.split_stats(sig, L.fwd(ur, h), h)
    print(f"h={h} IC {st['ic']:+.3f} t {st['t']:+.2f} IS t {st['t_is']:+.2f} OOS t {st['t_oos']:+.2f} yrs {st['yrs_same_sign']}/{st['yrs']}")
bs = L.bt_summary(pos, ur, 1, 5)
print("bt h=1 5bps:", {k: (v['sharpe'], v['sharpe_demeaned']) for k, v in bs.items() if isinstance(v, dict)})

# --- 1) İleriye bakma: sinyalin gelecek kaydırması, dk vs vo zaman uyumu ---
print("\n=== (1) ileriye bakma ===")
print("placebo (shift<0 = gelecek):", L.placebo_lead(sig, ur, 1))
# Dukascopy 15:00 ile VİOP uzlaşma getirisi korelasyonu, gecikmeler
d_dk = lfx.diff()
for k in (-1, 0, 1):
    print(f"corr(vo_usdtry_ret_t, dlnS_(t+{k})) = {ur.corr(d_dk.shift(-k)):+.3f}")
# 2 gün gecikmeli sinyal (daha da muhafazakâr)
for lag in (1, 2, 3):
    s_ = make_sig(lag=lag)
    a = L.backtest(np.sign(s_).fillna(0), ur, 1, 5)
    st = L.ic(s_, L.fwd(ur, 1), 5)
    print(f"lag={lag}: IC {st['ic']:+.3f} t {st['t']:+.2f} | Sharpe {a['sharpe']:+.2f} t_daily {a['t_daily']:+.2f}")

# --- 2) uç değer / PnL yoğunlaşması ---
print("\n=== (2) uç değerler / PnL yoğunlaşması ===")
a = L.backtest(pos, ur, 1, 5)
pnl = a["pnl"]
top = pnl.abs().sort_values(ascending=False).head(12)
print("en büyük |PnL| günleri:")
print(pd.DataFrame({"pnl%": pnl[top.index] * 100, "pos": pos.shift(1)[top.index], "ret%": ur[top.index] * 100}).round(2))
print(f"toplam PnL {pnl.sum()*100:.1f}% ; en iyi 10 gün hariç {pnl.drop(pnl.sort_values().index[-10:]).sum()*100:.1f}% ; en iyi 20 hariç {pnl.drop(pnl.sort_values().index[-20:]).sum()*100:.1f}%")
for nm, m in [("2018-08 hariç", ~((p.index >= "2018-08-01") & (p.index <= "2018-09-30"))),
              ("2021-11..2022-01 hariç", ~((p.index >= "2021-11-01") & (p.index <= "2022-01-31"))),
              ("ikisi + 2023-06..08 hariç", ~(((p.index >= "2018-08-01") & (p.index <= "2018-09-30")) | ((p.index >= "2021-11-01") & (p.index <= "2022-01-31")) | ((p.index >= "2023-06-01") & (p.index <= "2023-08-31")))),
              ("|ret|>5% günler hariç", ~(ur.abs() > 0.05))]:
    b = L.backtest(pos[m], ur[m], 1, 5); q = L.ic(sig[m], L.fwd(ur, 1)[m], 5)
    print(f"  {nm:28s}: Sharpe {b['sharpe']:+.2f} (t {b['t_daily']:+.2f}) | IC {q['ic']:+.3f} t {q['t']:+.2f}")
# winsorize getiri
wr = ur.clip(ur.quantile(0.01), ur.quantile(0.99))
b = L.backtest(pos, wr, 1, 5); print(f"  getiri %1-%99 winsorize: Sharpe {b['sharpe']:+.2f} (t {b['t_daily']:+.2f})")
# vol-normalize getiri (her gün 60g vol ile)
vol = ur.rolling(60, min_periods=20).std().shift(1)
nr = ur / vol
b = L.backtest(pos, nr, 1, 0); print(f"  vol-ölçekli getiri (risk paritesi): Sharpe {b['sharpe']:+.2f} (t {b['t_daily']:+.2f})")
for seg, m in [("IS", isx), ("OOS", ~isx)]:
    b = L.backtest(pos[m], nr[m], 1, 0); print(f"     {seg}: Sharpe {b['sharpe']:+.2f} (t {b['t_daily']:+.2f})")

# --- 3) drift: dönem-içi demean, uzun/kısa ---
print("\n=== (3) drift: alt dönem içinde demeaned ===")
PER = {"2017-19": ("2017", "2019"), "2020-21": ("2020", "2021"), "2022-23": ("2022", "2023"), "2024-26": ("2024", "2026"),
       "2023-06+": ("2023-06", "2026")}
rows = []
for nm, (s0, s1) in PER.items():
    m = (p.index >= s0) & (p.index <= pd.Timestamp(s1) + pd.offsets.YearEnd(0)) if len(s1) == 4 else (p.index >= s0)
    rr = ur[m]; pp = pos[m]
    raw = L.backtest(pp, rr, 1, 5); dm = L.backtest(pp, rr, 1, 5, demean=True)
    lo = L.backtest(pp.clip(lower=0), rr, 1, 5); sh = L.backtest(pp.clip(upper=0), rr, 1, 5)
    ash = L.backtest(pd.Series(-1.0, index=rr.index), rr, 1, 0)
    q = L.ic(sig[m], L.fwd(ur, 1)[m], 5); q5 = L.ic(sig[m], L.fwd(ur, 5)[m], 5)
    rows.append(dict(per=nm, n=m.sum(), frac_short=(pp < 0).mean(), sh_raw=raw["sharpe"], t_raw=raw["t_daily"], sh_dm=dm["sharpe"], t_dm=dm["t_daily"],
                     long=lo and lo["sharpe"], short=sh and sh["sharpe"], always_short=ash["sharpe"], ic1=q["ic"], t_ic1=q["t"], ic5=q5["ic"], t_ic5=q5["t"]))
print(pd.DataFrame(rows).round(2).to_string(index=False))
# yıl içi demean edilmiş hedefle havuzlanmış IC (zamanlama, yıl düzeyi carry'den bağımsız)
for h in (1, 5):
    y = L.fwd(ur, h)
    ydm = y - y.groupby(y.index.year).transform("mean")
    q = L.ic(sig, ydm, max(h, 5))
    # yıl içi sinyal de demean
    sdm = sig - sig.groupby(sig.index.year).transform("mean")
    q2 = L.ic(sdm, ydm, max(h, 5))
    print(f"h={h}: hedef yıl-içi demeaned IC {q['ic']:+.3f} t {q['t']:+.2f} | sinyal+hedef yıl-içi demeaned IC {q2['ic']:+.3f} t {q2['t']:+.2f}")
    for seg, m in [("IS", isx), ("OOS", ~isx)]:
        q3 = L.ic(sdm[m], ydm[m], max(h, 5)); print(f"     {seg}: {q3['ic']:+.3f} t {q3['t']:+.2f}")
# Ay içi demean (rejim çok hızlı değişiyorsa)
y = L.fwd(ur, 1); per = y.index.to_period("Q")
ydm = y - y.groupby(per).transform("mean"); sdm = sig - sig.groupby(per).transform("mean")
q = L.ic(sdm, ydm, 5); print(f"h=1 çeyrek-içi demeaned IC {q['ic']:+.3f} t {q['t']:+.2f}")
# yıl içi demeaned getiride strateji
ydm1 = ur - ur.groupby(ur.index.year).transform("mean")
for seg, m in [("tam", slice(None)), ("IS", isx), ("OOS", ~isx)]:
    rr = ydm1 if isinstance(m, slice) else ydm1[m]
    b = L.backtest(pos.reindex(rr.index), rr, 1, 5); print(f"  strateji, yıl-içi demeaned getiri {seg}: Sharpe {b['sharpe']:+.2f} t {b['t_daily']:+.2f}")
yr = {}
for y_, g in ydm1.groupby(ydm1.index.year):
    b = L.backtest(pos.reindex(g.index), g, 1, 5); yr[y_] = round(b["sharpe"], 2)
print("  yıl yıl yıl-içi demeaned Sharpe:", yr)

# --- 5) parametre duyarlılığı ---
print("\n=== (5) parametre duyarlılığı (h=1, 5bps) ===")
rows = []
for w in (5, 10, 20, 40, 60, 120):
    for coef in (0.7, 1.0, 1.4, 2.0, 3.0):
        s_ = make_sig(w=w, coef=coef)
        pp = np.sign(s_).fillna(0)
        a = L.backtest(pp, ur, 1, 5); ai = L.backtest(pp[isx], ur[isx], 1, 5); ao = L.backtest(pp[~isx], ur[~isx], 1, 5)
        q = L.split_stats(s_, L.fwd(ur, 1), 1)
        rows.append(dict(w=w, coef=coef, ic=q["ic"], t=q["t"], t_is=q["t_is"], t_oos=q["t_oos"], sh=a["sharpe"], sh_is=ai["sharpe"], sh_oos=ao["sharpe"]))
R = pd.DataFrame(rows); print(R.round(2).to_string(index=False))
print("\nclip / mindte duyarlılığı:")
for clip, md in [(1, 0), (3, 0), (5, 0), (3, 5), (3, 10)]:
    s_ = make_sig(clip=clip, mindte=md); pp = np.sign(s_).fillna(0)
    a = L.backtest(pp, ur, 1, 5); ao = L.backtest(pp[~isx], ur[~isx], 1, 5); q = L.ic(s_, L.fwd(ur, 1), 5)
    print(f"  clip={clip} mindte={md}: IC {q['ic']:+.3f} t {q['t']:+.2f} | Sharpe {a['sharpe']:+.2f} OOS {ao['sharpe']:+.2f}")

# --- 6) maliyet ---
print("\n=== (6) maliyet ===")
for c in (5, 10, 20):
    a = L.backtest(pos, ur, 1, c); ao = L.backtest(pos[~isx], ur[~isx], 1, c); ad = L.backtest(pos[~isx], ur[~isx], 1, c, demean=True)
    print(f"  {c} bps: tam {a['sharpe']:+.2f} OOS {ao['sharpe']:+.2f} OOS dm {ad['sharpe']:+.2f}")

# --- Basit kıyas kuralları: carry-only (pos = -1 if basis>0), drift-only ---
print("\n=== kıyas: bileşenler ve basit rejim kuralları ===")
bpd = np.log(p.vo_usdtry_settle / p.dk_USDTRY_p15) / dte.clip(lower=3)
for nm, s_ in [("yalnız drift20 (uzun hep)", (lfx.diff().rolling(20).mean()).shift(1)),
               ("yalnız -taşıma (hep kısa)", (-bpd).shift(1)),
               ("60g momentum işareti USDTRY vadeli", ur.rolling(60).sum().shift(1)),
               ("20g momentum işareti USDTRY vadeli", ur.rolling(20).sum().shift(1)),
               ("C1", sig)]:
    pp = np.sign(s_).fillna(0)
    a = L.backtest(pp, ur, 1, 5); ai = L.backtest(pp[isx], ur[isx], 1, 5); ao = L.backtest(pp[~isx], ur[~isx], 1, 5)
    print(f"  {nm:38s}: tam {a['sharpe']:+.2f} IS {ai['sharpe']:+.2f} OOS {ao['sharpe']:+.2f} kısa oranı {(pp<0).mean():.2f}")
# Vadeli kendi momentumu = drift - carry ile hemen hemen aynı şey mi?
mom20 = ur.rolling(20).mean().shift(1)
print("corr(C1 sig, vadeli 20g momentum):", round(sig.corr(mom20), 3), " sign agreement:", round((np.sign(sig) == np.sign(mom20)).mean(), 3))

# --- C2: sürüklenme tahmini ---
print("\n\n=== C2: USDTRY spot sürüklenmesi (yönetilen rejim) ===")
MAN = pd.Timestamp("2023-06-01")
cal = pd.Series(p.index, index=p.index)
for h in (1, 3, 5):
    y = lfx.shift(-h) - lfx
    fcs = {"RW0": pd.Series(0.0, index=p.index), "trail20": lfx.diff().rolling(20).mean() * h,
           "trail60": lfx.diff().rolling(60).mean() * h, "trail250": lfx.diff().rolling(250).mean() * h,
           "expanding_since_MAN": lfx.diff().where(p.index >= MAN).expanding(min_periods=20).mean() * h}
    for reg, m in [("2023-06+", p.index >= MAN), ("2023-06..2024-05", (p.index >= MAN) & (p.index < "2024-06-01")), ("2024-06+", p.index >= "2024-06-01"),
                   ("2023-09+", p.index >= "2023-09-01"), ("2024-01+", p.index >= "2024-01-01")]:
        yy = y[m]
        out = []
        for k, v in fcs.items():
            e = (yy - v[m]).dropna(); b0 = yy.reindex(e.index)
            out.append(f"{k} {100*(1-(e**2).mean()/(b0**2).mean()):+.1f}")
        # trail20 vs trail250 karşılaştırması (aynı örneklem)
        e20 = (yy - fcs["trail20"][m]); e250 = (yy - fcs["trail250"][m]); d = pd.concat([e20, e250], axis=1).dropna()
        r2rel = 1 - (d.iloc[:, 0] ** 2).mean() / (d.iloc[:, 1] ** 2).mean()
        print(f"h={h} {reg:18s} R2 vs RW0: " + " | ".join(out) + f" || trail20 vs trail250 göreli R2 {r2rel*100:+.1f}%")
    m = p.index >= MAN
    st = L.split_stats(lfx.diff().rolling(20).mean()[m], y[m], h)
    print(f"    IC (2023-06+): {st['ic']:+.3f} t {st['t']:+.2f} n {st['n']} yıllar {st['by_year']}")
    for yy_ in (2023, 2024, 2025, 2026):
        mm = m & (p.index.year == yy_)
        q = L.ic(lfx.diff().rolling(20).mean()[mm], y[mm], max(h, 5))
        print(f"       {yy_}: IC {q['ic']:+.3f} t {q['t']:+.2f} n {q['n']}")
    # hiçbir rejim seçimi olmadan, tam dönem
    st = L.split_stats(lfx.diff().rolling(20).mean(), y, h)
    print(f"    IC tam dönem 2017+: {st['ic']:+.3f} t {st['t']:+.2f} | <2023-06: ", end="")
    q = L.ic(lfx.diff().rolling(20).mean()[~m], y[~m], max(h, 5)); print(f"{q['ic']:+.3f} t {q['t']:+.2f}")
