"""Aile (b): Türkiye altın fiyatı (gram altın TL) — ayrıştırma, kur sürüklenmesi öngörüsü, prim dönüşü, gram vadeli tahmin modeli."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/7162e4a1-8b83-5632-8869-8b60f6d4bda9/scratchpad/out/a7_turkiye")
from a7_common import *
import statsmodels.api as sm
FAM = "b_trgold"
reset_family(FAM)
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
p, f = build()
MAN = pd.Timestamp("2023-06-01")  # yönetilen kur dönemi başlangıcı (Haziran 2023 politika dönüşü)

# ---------------- B1: ayrıştırma ----------------
g = p.vo_xautry_ret; x = p.v_ret; u = p.vo_usdtry_ret
res = g - x - u
D = pd.DataFrame({"g": g, "x": x, "u": u, "res": res}).dropna()
print("B1. VİOP gram vadeli günlük getirisi = ons vadeli + USDTRY vadeli + kalıntı (prim değişimi + vade uyumsuzluğu)")
print("kalıntı std (bps):", round(D.res.std() * 1e4, 1), " Δprem std:", round(p.tr_prem_matched.diff().std() * 1e4, 1),
      " corr(res, Δprem):", round(D.res.corr(p.tr_prem_matched.diff().reindex(D.index)), 3))

def cov_shares(df, h):
    z = df.rolling(h).sum().iloc[h - 1::h].dropna()
    vg = z.g.var()
    return dict(n=len(z), sd_g=z.g.std() * 100, ons=z.x.cov(z.g) / vg * 100, kur=z.u.cov(z.g) / vg * 100, prim=z.res.cov(z.g) / vg * 100, corr_ons_kur=z.x.corr(z.u))

rows = []
for y, d in D.groupby(D.index.year):
    for h in (1, 5):
        r = cov_shares(d, h); r.update(yil=y, h=h); rows.append(r)
for nm, (a, b) in {"2017-2021": ("2017", "2021"), "2022-2026": ("2022", "2026"), "2023-06+ (yönetilen)": ("2023-06", "2026")}.items():
    for h in (1, 5):
        r = cov_shares(D.loc[a:b], h); r.update(yil=nm, h=h); rows.append(r)
B1 = pd.DataFrame(rows).set_index(["yil", "h"]).round(1)
print("\nVaryans payları (kovaryans tabanlı, toplam=100): ons / kur / prim+kalıntı — VİOP vadeli getirileri")
print(B1.to_string()); B1.to_csv(f"{OUT}/b1_var_shares_futures.csv")
# spot sürüm
sx = np.log(p.xau_p15).diff(); su = np.log(p.dk_USDTRY_p15).diff()
SP = pd.DataFrame({"x": sx, "u": su}).dropna(); SP["g"] = SP.x + SP.u; SP["res"] = 0.0
rows = []
for y, d in SP.groupby(SP.index.year):
    for h in (1, 5):
        r = cov_shares(d, h); r.update(yil=y, h=h); rows.append(r)
B1s = pd.DataFrame(rows).set_index(["yil", "h"]).drop(columns=["prim"]).round(1)
print("\nSpot gram altın (ons 15:00 × USDTRY 15:00) varyans payları"); print(B1s.to_string()); B1s.to_csv(f"{OUT}/b1_var_shares_spot.csv")
yr = SP.groupby(SP.index.year)[["x", "u", "g"]].sum() * 100
yr.columns = ["ons_logret%", "kur_logret%", "gram_logret%"]
yr["kur_payi_%"] = yr["kur_logret%"] / yr["gram_logret%"] * 100
print("\nYıllık getiri katkısı (spot, log %)"); print(yr.round(1).to_string()); yr.round(2).to_csv(f"{OUT}/b1_annual_contrib.csv")

# ---------------- B2: USDTRY sürüklenmesi öngörüsü ----------------
print("\nB2. USDTRY spot (15:00 UTC) h-gün değişimi öngörüsü: RW vs geçmiş sürüklenme vs VİOP USDTRY bazı")
lfx = np.log(p.dk_USDTRY_p15)
dte = p.vo_usdtry_dte.clip(lower=3)
basis_pd = np.log(p.vo_usdtry_settle / p.dk_USDTRY_p15) / dte          # takvim günü başına ima kayma (t, K)
cal = pd.Series(p.index, index=p.index)
out = []
for h in (1, 3, 5):
    y = lfx.shift(-h) - lfx
    caldays = (cal.shift(-h) - cal).dt.days
    fc = {"RW": pd.Series(0.0, index=p.index),
          "trail20": lfx.diff().rolling(20).mean() * h,
          "trail60": lfx.diff().rolling(60).mean() * h,
          "basis_K": basis_pd * caldays,
          "basis_l1": basis_pd.shift(1) * caldays}
    for reg_nm, m in [("2017-03..2023-05", (p.index < MAN)), ("2023-06+ yönetilen", (p.index >= MAN)), ("2023-06..2025-02", (p.index >= MAN) & (p.index < "2025-03-01")), ("2025-04+", p.index >= "2025-04-01")]:
        yy = y[m]
        mse0 = (yy ** 2).mean()
        for k, v in fc.items():
            e = (yy - v[m]).dropna()
            r2 = 1 - (e ** 2).mean() / (yy.reindex(e.index) ** 2).mean()
            out.append(dict(h=h, donem=reg_nm, model=k, rmse_bps=np.sqrt((e ** 2).mean()) * 1e4, R2_vs_RW=r2 * 100, n=len(e),
                            mean_real_bps=yy.mean() * 1e4, mean_fc_bps=v[m].mean() * 1e4))
B2 = pd.DataFrame(out)
print(B2.round(2).to_string(index=False)); B2.round(3).to_csv(f"{OUT}/b2_fx_drift_forecast.csv", index=False)
# kayıt: yönetilen dönemde basis_l1 ve trail20 (IC)
for h in (1, 3, 5):
    y = lfx.shift(-h) - lfx
    caldays = (cal.shift(-h) - cal).dt.days
    m = p.index >= MAN
    for nm, v in [("fx_basis_l1->usdtry_h(man)", basis_pd.shift(1) * caldays), ("fx_trail20->usdtry_h(man)", lfx.diff().rolling(20).mean())]:
        st = L.split_stats(v[m], y[m], h)
        # IS/OOS bölümü bu dönemde anlamsız (hepsi OOS); n ve t raporlanır
        L.register(AG, FAM, nm, nm, h, st, "yönetilen kur dönemi 2023-06+, USDTRY spot hedef")
        print(nm, h, fmt(st))
# USDTRY vadeli getirisinin (carry trade) ortalaması — dönem bazında
uf = {h: fwd(p.vo_usdtry_ret, h) for h in (1, 5)}
print("\nUSDTRY vadeli ortalama getiri (uzun USDTRY vadeli; negatif = TL carry kazancı), yıllık %:")
for nm, m in [("2017-2021", p.index <= "2021-12-31"), ("2022-01..2023-05", (p.index >= "2022-01-01") & (p.index < MAN)), ("2023-06+", p.index >= MAN), ("2023-06..2025-02", (p.index >= MAN) & (p.index < "2025-03-01")), ("2025-03..", p.index >= "2025-03-01")]:
    r = p.vo_usdtry_ret[m]
    print(f"  {nm:18s} ort {r.mean()*252*100:+.1f}%/yıl, vol {r.std()*np.sqrt(252)*100:.1f}%, Sharpe(kısa) {-r.mean()/r.std()*np.sqrt(252):.2f}, en kötü gün {r.max()*100:+.2f}%")
# carry trade zamanlaması: (geçmiş sürüklenme - ima kayma) USDTRY vadeli getirisini öngörüyor mu?
sig = lfx.diff().rolling(20).mean() - basis_pd * 1.4  # iş günü başına (≈1,4 takvim günü)
for h in (1, 5):
    st = test(FAM, "fx_carry_timing(trail20-basis)->usdtry_fut", sig, fwd(p.vo_usdtry_ret, h), h, note="sinyal t 15:10 K")
    print("carry zamanlama", h, fmt(st))

# ---------------- B3: prim ortalamaya dönüşü ----------------
print("\nB3. Gram altın sentetik primi (tr_prem_matched) ortalamaya dönüş")
pr = p.tr_prem_matched
def ar1(s):
    d = pd.DataFrame({"y": s, "x": s.shift(1)}).dropna()
    m = sm.OLS(d.y, sm.add_constant(d.x)).fit(cov_type="HAC", cov_kwds={"maxlags": 5})
    phi = m.params["x"]; return phi, (np.log(0.5) / np.log(phi) if 0 < phi < 1 else np.nan), m.params["const"] / (1 - phi), len(d)
def ark(s, k):
    d = pd.DataFrame({"y": s, "x": s.shift(k)}).dropna()
    phi = np.polyfit(d.x, d.y, 1)[0]
    return phi ** (1 / k) if phi > 0 else np.nan
rows = []
for y, s in [(str(y), pr[pr.index.year == y]) for y in sorted(set(pr.index.year))] + [("IS", pr[:L.IS_END]), ("OOS", pr[L.IS_END + pd.Timedelta(days=1):]), ("tam", pr), ("tam |prem|<2%", pr.where(pr.abs() < 0.02))]:
    phi, hl, mu, n = ar1(s)
    phi5 = ark(s, 5)
    rows.append(dict(donem=y, phi1=phi, yari_omur_gun=hl, phi_from_lag5=phi5, yari_omur_lag5=np.log(0.5) / np.log(phi5) if phi5 and 0 < phi5 < 1 else np.nan,
                     ort_bps=mu * 1e4, sd_bps=s.std() * 1e4, sd_dprem_bps=s.diff().std() * 1e4, n=n))
B3 = pd.DataFrame(rows); print(B3.round(3).to_string(index=False)); B3.round(4).to_csv(f"{OUT}/b3_prem_ar.csv", index=False)
# hangi bacak düzeltiyor?
print("\nPrim sapması (prem - 60g ort, t-1) ile ileri h-gün getiriler (hangi bacak düzeltiyor):")
dev = (pr - pr.rolling(60, min_periods=20).mean())
for h in (1, 3, 5):
    for nm, tgt in [("gram", fwd(g, h)), ("ons", fwd(x, h)), ("usdtry", fwd(u, h)), ("Δprem", pr.shift(-h) - pr)]:
        r = nw_ols(tgt, dev.shift(1).rename("dev"), lags=max(h, 5))
        print(f"  h={h} {nm:7s} b={r['b']:+.3f} t={r['t']:+.2f} R2={r['r2']*100:.2f}%")
    st = test(FAM, "prem_dev_l1->gram_fwd", dev.shift(1), fwd(g, h), h, note="t-1 bilgi; gram vadeli hedef")
    st = test(FAM, "prem_dev_l1->dprem_fwd", dev.shift(1), pr.shift(-h) - pr, h, note="t-1 bilgi; prim değişimi hedef (sentetik RV)")
    print("   ", h, fmt(st))

# ---------------- B4: gram vadeli tahmin modeli ----------------
print("\nB4. Gram vadeli h-gün getirisi tahmini: bileşenler (ons=0) + kur vadeli beklenen getiri + prim dönüşü; kıyas 0 (ons×kur RW)")
isx = p.index <= L.IS_END
res_rows = []
for h in (1, 3, 5):
    y = fwd(g, h)
    # IS'te prim dönüş katsayısı (t-1 bilgisi ile)
    Xd = pd.DataFrame({"y": y, "dev": dev.shift(1)}).dropna()
    bi = np.polyfit(Xd.loc[Xd.index <= L.IS_END, "dev"], Xd.loc[Xd.index <= L.IS_END, "y"], 1)[0]
    cal_h = (cal.shift(-h) - cal).dt.days
    fx_exp = (lfx.diff().rolling(20).mean().shift(1) * h - basis_pd.shift(1) * cal_h)  # t-1 bilgisi: beklenen USDTRY vadeli getirisi
    comps = {"0 (RW)": pd.Series(0.0, index=p.index), "prim": bi * dev.shift(1), "kur_vadeli": fx_exp, "prim+kur": bi * dev.shift(1) + fx_exp}
    for seg, m in [("IS", isx), ("OOS", ~isx), ("OOS 2023-06+", p.index >= MAN)]:
        yy = y[m]
        for k, v in comps.items():
            e = (yy - v[m]).dropna(); base = yy.reindex(e.index)
            r2 = 1 - (e ** 2).sum() / (base ** 2).sum()
            ic_ = pd.concat([v[m], yy], axis=1).dropna().corr(method="spearman").iloc[0, 1] if k != "0 (RW)" else np.nan
            res_rows.append(dict(h=h, seg=seg, model=k, R2_vs_0=r2 * 100, ic=ic_, n=len(e), b_prem_IS=bi))
    for k in ("prim", "kur_vadeli", "prim+kur"):
        st = test(FAM, f"gram_model_{k}", comps[k], y, h, note="t-1 bilgi; prim katsayısı IS")
        print(f"  h={h} {k:10s}", fmt(st))
B4 = pd.DataFrame(res_rows); print(B4.round(3).to_string(index=False)); B4.round(4).to_csv(f"{OUT}/b4_gram_model.csv", index=False)

# ---------------- B5: prim RV stratejisi (sentetik — gram) ----------------
print("\nB5. Göreli değer: prim z(t-1)>k ise gram kısa + (ons+USDTRY) uzun (Δprem'in tersi kazanılır). 3 bacak maliyet = 3×5 bps")
spread_ret = -(pr.diff())  # prim düşerse kısa-prim pozisyonu kazanır (≈ -(g - x - u))
spread_ret2 = -(res)       # gerçek bacak getirileriyle
z = zs(pr, 60)
for k in (0.5, 1.0, 1.5, 2.0):
    pos = -(z.shift(1) > k).astype(float) + (z.shift(1) < -k).astype(float)   # pos>0: prim uzun ( gram uzun, sentetik kısa )
    for h in (1, 3, 5):
        a = L.backtest(pos, res.fillna(0), h, cost_bps=15)
        isb = L.backtest(pos[isx], res.fillna(0)[isx], h, cost_bps=15); oob = L.backtest(pos[~isx], res.fillna(0)[~isx], h, cost_bps=15)
        print(f"  k={k} h={h}: tam Sharpe {a['sharpe']:+.2f} (yıllık {a['ann_ret']*100:+.2f}%), IS {isb['sharpe']:+.2f}, OOS {oob['sharpe']:+.2f}, maruz {a['exposure']:.2f}, devir/yıl {a['turnover_per_yr']:.0f}")
        if k == 1.0:
            L.register(AG, FAM, f"prem_RV_z1_h{h}", "prem z(t-1)>1 RV", h, dict(ic=np.nan, t=a["t_daily"], n=a["n_days"], t_is=isb["t_daily"], t_oos=oob["t_daily"]), "3 bacak 15 bps")

# ---------------- B5b: prim RV — KAPANIŞTA (prem_t) sürümü, brüt ve net ----------------
print("\nB5b. Prim RV, sinyal t 15:10 KAPANIŞTA (z_t), brüt (0 bps) ve net (15 bps)")
for k in (1.0, 2.0):
    pos = -(z > k).astype(float) + (z < -k).astype(float)
    for h in (1, 3, 5):
        g0 = L.backtest(pos, res.fillna(0), h, cost_bps=0); n15 = L.backtest(pos, res.fillna(0), h, cost_bps=15)
        oo = L.backtest(pos[~isx], res.fillna(0)[~isx], h, cost_bps=15)
        print(f"  K k={k} h={h}: brüt Sharpe {g0['sharpe']:+.2f} ({g0['ann_ret']*100:+.2f}%/yıl), net15 {n15['sharpe']:+.2f}, OOS net15 {oo['sharpe']:+.2f}, maruz {g0['exposure']:.2f}")
        if k == 1.0:
            L.register(AG, FAM, f"prem_RV_K_z1_h{h}", "prem z_t>1 RV (K)", h, dict(ic=np.nan, t=n15["t_daily"], n=n15["n_days"], t_oos=oo["t_daily"]), "K; 3 bacak 15 bps")
for k in (1.0,):
    pos = -(z.shift(1) > k).astype(float) + (z.shift(1) < -k).astype(float)
    for h in (1, 3, 5):
        g0 = L.backtest(pos, res.fillna(0), h, cost_bps=0)
        print(f"  t-1 k={k} h={h}: brüt Sharpe {g0['sharpe']:+.2f} ({g0['ann_ret']*100:+.2f}%/yıl)")

# ---------------- B2b: USDTRY carry zamanlaması — temiz t-1 sürümü + strateji ----------------
print("\nB2b. USDTRY vadeli getirisi: (geçmiş 20g sürüklenme - ima kayma) sinyali, t-1 sürümü (temiz)")
sig1 = (lfx.diff().rolling(20).mean() - basis_pd * 1.4).shift(1)
for h in (1, 3, 5):
    st = test(FAM, "fx_carry_timing_l1->usdtry_fut", sig1, fwd(p.vo_usdtry_ret, h), h, note="t-1 bilgi")
    print("   ", h, fmt(st))
ur = p.vo_usdtry_ret
always_short = pd.Series(-1.0, index=p.index)
timing = np.sign(sig1).fillna(0)          # sinyal>0 (sürüklenme > taşıma) ise USDTRY uzun, aksi kısa
timing_flat = (-(sig1 < 0)).astype(float)  # yalnız taşıma > sürüklenme iken kısa, diğer zaman nakit
for nm, pos in [("hep kısa USDTRY (TL carry)", always_short), ("zamanlama ±1", timing), ("zamanlama kısa/nakit", timing_flat)]:
    for h in (1, 5):
        out = {}
        for seg, m in [("tam", slice(None)), ("IS", isx), ("OOS", ~isx), ("2023-06+", p.index >= MAN)]:
            rr = ur if isinstance(m, slice) else ur[m]
            a = L.backtest(pos.reindex(rr.index), rr, h, 5)
            out[seg] = f"{a['sharpe']:+.2f} ({a['ann_ret']*100:+.1f}%)"
        print(f"   {nm:24s} h={h}: " + "  ".join(f"{k} {v}" for k, v in out.items()))

# ---------------- B6: spot gram altın (ons × kur) yönü: kur sürüklenmesinin katkısı ----------------
print("\nB6. Spot gram altın (xau_p15 × USDTRY 15:00) h-gün log getirisi: RW(0) vs geçmiş 20g kur sürüklenmesi")
lg = np.log(p.xau_p15) + lfx
for h in (1, 3, 5):
    y = lg.shift(-h) - lg
    fc = lfx.diff().rolling(20).mean() * h
    for seg, m in [("2017-03..2023-05", p.index < MAN), ("2023-06+", p.index >= MAN)]:
        e = (y[m] - fc[m]).dropna(); b0 = y[m].reindex(e.index)
        print(f"   h={h} {seg}: R2 vs 0 = {(1-(e**2).sum()/(b0**2).sum())*100:+.2f}%  (kur sürüklenmesi ort {fc[m].mean()*1e4:.1f} bps, gram ort {y[m].mean()*1e4:.1f} bps)")
