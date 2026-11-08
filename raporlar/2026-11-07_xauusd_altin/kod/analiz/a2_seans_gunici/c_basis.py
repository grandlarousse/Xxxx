"""(c) VİOP'a özgü fiyatlama hatası: excess_basis = log(v_settle/xau_p15) - r*dte/365, r = ust_nom3m/100 (t-1 değeri).
BİLGİ ZAMANI: v_settle gün t 15:10 UTC -> eb_t 'kapanışta hesaplanan'. Temiz sürüm: eb_{t-1} (t-1 15:10'da bilinir).
Ölçüm gürültüsü: xau_p15 (15:00) ile uzlaşma VWAP'ı (15:05-15:15) arasındaki ~10 dk; dakikalık örnekle ölçülür.
Hedefler: VİOP fwd{h} (işlem görebilir) ve rel{h} = sum_{k=1..h}(v_ret - s_ret15) = basis_{t+h} - basis_t (VİOP - spot göreli)."""
from a2_common import *
reset_families(["c_basis"])
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
v = load_viop()
carry = v.ust_nom3m / 100 * v.v_dte / 365
braw = np.log(v.v_settle / v.xau_p15)
eb = braw - carry
s15 = np.log(v.xau_p15 / v.xau_p15_prev)
relret = v.v_ret - s15            # gün t: VİOP getirisi - spot 15:00->15:00 getirisi (roll günlerinde v_ret aynı kontrat içi)
rel = {h: fwd(relret, h) for h in (1, 3, 5)}
# ---------- 1) dakikalık kalibrasyon: uzlaşma vs spot 15:00 / 15:10 / VWAP 15:05-15:15
m = pd.read_parquet(f"{P}/duka_min_XAUUSD.parquet")
m.index = pd.to_datetime(m.index)
# minute index = bar başlangıcı varsayımı kontrol: saatlik 15:00 fiyatı (14:00 barının kapanışı) ile 14:59 dakika barı kapanışı
cal = []
for d, g in m.groupby(m.index.date):
    d = pd.Timestamp(d)
    if d not in v.index: continue
    def px(hh, mm):
        t = d + pd.Timedelta(hours=hh, minutes=mm); x = g.c[g.index <= t]
        return x.iloc[-1] if len(x) and (t - x.index[-1]) <= pd.Timedelta(minutes=3) else np.nan
    w = g[(g.index >= d + pd.Timedelta(hours=15, minutes=5)) & (g.index < d + pd.Timedelta(hours=15, minutes=15))]
    vw = (w.c * w.v).sum() / w.v.sum() if len(w) and w.v.sum() > 0 else np.nan
    cal.append(dict(date=d, p1459=px(14, 59), p1500=px(15, 0), p1509=px(15, 9), p1510=px(15, 10), p1514=px(15, 14), vwap=vw, p1520=px(15, 20)))
C = pd.DataFrame(cal).set_index("date")
C = C.join(v[["v_settle", "xau_p15", "v_dte", "ust_nom3m", "v_close"]], how="inner")
cr = C.ust_nom3m / 100 * C.v_dte / 365
out = {}
out["check_p1459_vs_panel_p15_MAD_bps"] = float((np.log(C.p1459 / C.xau_p15)).abs().median() * 1e4)
out["check_p1500_vs_panel_p15_MAD_bps"] = float((np.log(C.p1500 / C.xau_p15)).abs().median() * 1e4)
ref = "p1459" if out["check_p1459_vs_panel_p15_MAD_bps"] <= out["check_p1500_vs_panel_p15_MAD_bps"] else "p1500"
out["minute_ref_for_15:00"] = ref
for nm in ["xau_p15", "p1509", "vwap", "p1514", "p1520"]:
    d = (np.log(C.v_settle / C[nm]) - cr) * 1e4
    out[f"settle_vs_{nm}: median_bps"] = round(float(d.median()), 2); out[f"settle_vs_{nm}: MAD_bps"] = round(float((d - d.median()).abs().median()), 2); out[f"settle_vs_{nm}: std_bps"] = round(float(d.std()), 2)
noise = np.log(C.vwap / C.xau_p15) * 1e4
out["spot_vwap15:05-15_minus_p15000: std_bps"] = round(float(noise.std()), 2); out["...: MAD_bps"] = round(float(noise.abs().median()), 2)
out["n_minute_days"] = int(len(C))
# eb'nin gürültü dışı (kalıcı) varyans payı: eb(p15) ile eb(vwap) varyansları
eb_p15 = (np.log(C.v_settle / C.xau_p15) - cr) * 1e4; eb_vw = (np.log(C.v_settle / C.vwap) - cr) * 1e4
out["std eb(p15) bps (örnek günler)"] = round(float(eb_p15.std()), 2); out["std eb(vwap) bps"] = round(float(eb_vw.std()), 2)
out["corr eb(p15), eb(vwap)"] = round(float(eb_p15.corr(eb_vw)), 3)
pd.Series(out).to_csv(f"{OUT}/c_minute_calibration.csv")
print("Dakikalık kalibrasyon:\n", pd.Series(out).to_string())
# ---------- 2) eb tanımlayıcı
print("\neb (bps) yıl yıl:\n", (eb * 1e4).groupby(v.index.year).agg(["mean", "std", "median"]).round(1).to_string())
print("AC1", round(eb.autocorr(1), 3), "AC5", round(eb.autocorr(5), 3))
# dte ile büyüyen kısım: IS'te eb ~ dte regresyonu (IS'te tahmin, tüm döneme uygulanır)
isd = pd.concat([eb, v.v_dte], axis=1).dropna(); isd = isd[isd.index <= IS_END]
b = np.polyfit(isd.iloc[:, 1], isd.iloc[:, 0], 1)
ebr = eb - (b[0] * v.v_dte + b[1])
print("IS eb~dte: slope bps/gün", round(b[0] * 1e4, 3), "const bps", round(b[1] * 1e4, 2), " -> ima edilen ek faiz %/yıl", round(b[0] * 365 * 100, 2))
# ---------- 3) testler
rows = []
for h in (1, 3, 5):
    y = v[f"fwd{h}"]
    rows.append(test("c_basis", f"c_eb_t_fwd_h{h}", "eb_t (kapanışta)", eb, y, h, "KAPANIŞTA HESAPLANAN (15:10 UTC)"))
    rows.append(test("c_basis", f"c_eb_tm1_fwd_h{h}", "eb_t-1", eb.shift(1), y, h, "t-1 15:10 UTC"))
    rows.append(test("c_basis", f"c_ebr_tm1_fwd_h{h}", "ebres_t-1 (dte-düz.)", ebr.shift(1), y, h, "t-1; dte eğimi IS'te"))
    rows.append(test("c_basis", f"c_eb_tm1_rel_h{h}", "eb_t-1 -> VİOP-spot", eb.shift(1), rel[h], h, "göreli hedef; t-1 gürültüsü hedeften bağımsız"))
    rows.append(test("c_basis", f"c_ebr_tm1_rel_h{h}", "ebres_t-1 -> VİOP-spot", ebr.shift(1), rel[h], h, "göreli hedef"))
    rows.append(test("c_basis", f"c_eb_t_rel_h{h}", "eb_t -> VİOP-spot (mekanik)", eb, rel[h], h, "MEKANİK: eb_t gürültüsü hedefte -eb_t olarak var"))
R = pd.DataFrame(rows); R.to_csv(f"{OUT}/c_basis_ic.csv", index=False)
print("\n", R.drop(columns=["family", "test_id", "note"]).to_string())
# OLS katsayısı: rel_h ~ eb_{t-1} (yarı ömür) ve eb_t (mekanik)
for h in (1, 5):
    r1 = nw_ols(rel[h], eb.shift(1), lags=max(h, 5)); r0 = nw_ols(rel[h], eb, lags=max(h, 5))
    print(f"h={h}: rel ~ eb_t-1 b={r1['b']:.3f} t={r1['t']:.2f} | rel ~ eb_t b={r0['b']:.3f} t={r0['t']:.2f}")
# ---------- 4) işlem kuralı (yalnız eb_{t-1}, IS tercilleri) VİOP çıplak pozisyon
q = eb[eb.index <= IS_END].quantile([1 / 3, 2 / 3]).values
bt_rows = []
for h in (1, 3, 5):
    pos = pd.Series(np.where(eb.shift(1) > q[1], -1.0, np.where(eb.shift(1) < q[0], 1.0, 0.0)), index=v.index)
    L = legs(pos, v.v_ret, h); df = fmt_legs(L); df["h"] = h; bt_rows.append(df)
BT = pd.concat(bt_rows); BT.to_csv(f"{OUT}/c_basis_backtest.csv", index=False)
print("\nTercil kuralı (eb_t-1 yüksek -> kısa, düşük -> uzun), VİOP v_ret:\n", BT[BT.leg == "both"].to_string())
print("Buy&hold Sharpe:", bh_stats(v.v_ret))
# ---------- 5) Göreli değer (VİOP - spot hedge) kuralı: eb_{t-1} IS tercilleri; hedef relret (iki bacak; maliyet 2x)
rv = []
for h in (1, 3, 5):
    pos = pd.Series(np.where(eb.shift(1) > q[1], -1.0, np.where(eb.shift(1) < q[0], 1.0, 0.0)), index=v.index)
    for cost in (10, 20):
        b = bt_summary(pos, relret.dropna(), h, cost)
        rv.append(dict(h=h, cost_bps_2leg=cost, **{f"{p}_sharpe": b[p]["sharpe"] for p in ("full", "is", "oos")}, **{f"{p}_ann_pct": b[p]["ann"] for p in ("full", "is", "oos")}, turn=b["full"]["turnover"]))
RV = pd.DataFrame(rv); RV.to_csv(f"{OUT}/c_relative_value_bt.csv", index=False)
print("\nGöreli değer (VİOP kısa/spot uzun eb yüksekken), relret, 2 bacak maliyet:\n", RV.to_string())
# brüt (maliyetsiz) getiri büyüklüğü
for h in (1, 5):
    pos = pd.Series(np.where(eb.shift(1) > q[1], -1.0, np.where(eb.shift(1) < q[0], 1.0, 0.0)), index=v.index)
    b0 = backtest(pos, relret.dropna(), h, 0)
    print(f"h={h} brüt yıllık %{b0['ann_ret']*100:.2f}, vol %{b0['ann_vol']*100:.2f}, gün başı ort bps {b0['pnl'].mean()*1e4:.2f}")
# ---------- 6) sağlamlık: roll penceresi hariç, uç dönem hariç, winsor
rb = []
for h in (3, 5):
    for nm, x, y in [("eb_t-1->rel", eb.shift(1), rel[h]), ("eb_t-1->fwd", eb.shift(1), v[f"fwd{h}"])]:
        for cond, msk in [("hepsi", pd.Series(True, index=v.index)), ("roll_haric", roll_window_mask(v, h)), ("uc_haric", extreme_mask(v.index)),
                          ("dte>5", v.v_dte.shift(1) > 5)]:
            xx = x[msk]; st = ic(xx, y[msk], max(h, 5))
            rb.append(dict(test=nm, h=h, cond=cond, ic=round(st["ic"], 4), t=round(st["t"], 2), n=st["n"]))
        xw = x.clip(x.quantile(0.01), x.quantile(0.99)); st = ic(xw, y, max(h, 5), method="pearson")
        rb.append(dict(test=nm, h=h, cond="winsor1-99_pearson", ic=round(st["ic"], 4), t=round(st["t"], 2), n=st["n"]))
RB = pd.DataFrame(rb); RB.to_csv(f"{OUT}/c_basis_robust.csv", index=False); print("\nSağlamlık:\n", RB.to_string())
print("placebo eb->fwd1:", placebo_lead(eb, v.v_ret, 1))
