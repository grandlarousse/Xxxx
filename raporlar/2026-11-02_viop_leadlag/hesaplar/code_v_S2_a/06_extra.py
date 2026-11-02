"""06: (i) FX ileriye-bakma testi yıl yıl, (ii) yıllara göre regresyon (ham ve piyasa-nötr), (iii) kapanış seansı gürültüsü (h1),
(iv) 5 dk: açılış seansı fiyatı vs 07:00/07:05/07:15 sürekli işlem fiyatı (son ~60 gün), (v) iki bacaklı (TCELL - β·XU030) backtest."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_S2_a")
from vs import *
pd.set_option("display.width", 250)
df = pd.read_parquet(OUT + "/02_daily.parquet")
q = df[(df.index >= "2014-01-01")].copy(); q = q[q.D.abs() < 0.15]
q["U"] = q.D - q.gap1
print("=== (i) FX bar(t+1) BIST t+1 seansına taşıyor mu? corr(dfx_t [k0->k1 kur değişimi], X_{t+1}) yıl yıl ===")
print("    pozitif kontrol: corr(dfx_{t+1}, X_{t+1}) (t+1 günü kur değişimi; t+1 seansını İÇERİR)")
q["dfx_next"] = q.dfx_day.shift(-1)
rows = []
for y, z in q.groupby(q.index.year):
    rows.append(dict(yil=y, c_dfx_xuintra1=z.dfx_day.corr(z.xu_intra1), c_dfx_xugap1=z.dfx_day.corr(z.xu_gap1), c_dfx_tcintra1=z.dfx_day.corr(z.intra1),
                     poz_kontrol_c_dfxnext_xuintra1=z.dfx_next.corr(z.xu_intra1), c_dfxnext_xugap1=z.dfx_next.corr(z.xu_gap1), n=len(z)))
F = pd.DataFrame(rows).round(3); print(F.to_string(index=False)); F.to_csv(OUT + "/06_fx_lookahead.csv", index=False)
print("\n=== (ii) Yıllara göre: intra1 ~ D + gap1 ve piyasa-nötr (TCELL - β XU100) ===")
b = (q.intra1.rolling(250, min_periods=100).cov(q.xu_intra1) / q.xu_intra1.rolling(250, min_periods=100).var()).shift(1)
q["ab1"] = q.intra1 - b * q.xu_intra1
rows = []
for y, z in q.groupby(q.index.year):
    m, n = nw(z.intra1, z[["D", "gap1"]]); m2, n2 = nw(z.ab1, z[["D", "gap1"]])
    r = bt(z.U, z.intra1, 8, 0.005); rd = bt(z.D, z.intra1, 8, 0.005); rd0 = bt(z.D, z.intra1, 8, 0.0)
    rows.append(dict(yil=y, b_D=m.params["D"], t_D=m.tvalues["D"], b_D_nötr=m2.params["D"], t_D_nötr=m2.tvalues["D"], sdD_bps=1e4 * z.D.std(),
                     BT_U50_net=r["mean_bps"], BT_D50_net=rd["mean_bps"], BT_D0_net=rd0["mean_bps"], n=n))
Y = pd.DataFrame(rows).round(2); print(Y.to_string(index=False)); Y.to_csv(OUT + "/06_by_year.csv", index=False)
print("  pozitif b_D yıl oranı:", (Y.b_D > 0).mean().round(2), "| nötr:", (Y.b_D_nötr > 0).mean().round(2), "| BT_U50>0:", (Y.BT_U50_net > 0).mean().round(2), "| BT_D0>0:", (Y.BT_D0_net > 0).mean().round(2))
print("\n=== (v) İki bacaklı: sign(D) × (TCELL intra - β XU030 intra), maliyet TCELL 8 + XU030 vadeli 3 bps ===")
b30 = (q.intra1.rolling(250, min_periods=100).cov(q.x30_intra1) / q.x30_intra1.rolling(250, min_periods=100).var()).shift(1)
q["hedged"] = q.intra1 - b30 * q.x30_intra1
for nm, sig in [("D", q.D), ("U", q.U)]:
    for thr in [0, 0.005, 0.01]:
        out = []
        for lab, s, e in [("IS", "2014-01-01", "2020-12-31"), ("OOS", "2021-01-01", "2026-12-31")]:
            r = bt(sig, q.hedged, 8 + 3 * float(b30.mean()), thr, s, e); out.append(f"{lab} n {r['n']} {r['mean_bps']:.1f} bps t {r['t']:.2f} Sh {r['sharpe']:.2f}")
        print(f"  {nm} |>{thr*1e4:.0f}|: " + " | ".join(out))
print("\n=== (iii) Kapanış seansı gürültüsü (2023-12+): cs = ln(c_t / p_15:00 sürekli) ===")
H = pd.read_parquet(OUT + "/05_hourly.parquet")
h = rawd("TCELL.IS", "h1"); h = h[~h.index.duplicated(keep="last")]
last = pd.Series(h["c"].values, index=pd.DatetimeIndex(h["ldate"].values)).groupby(level=0).last()  # son saatlik bar kapanışı ≈ 15:00 UTC sürekli fiyat
H["cs"] = np.log(H.tcC / last.reindex(H.index))
z = H.dropna(subset=["cs", "D", "intra1", "gap1"]); z = z[z.cs.abs() < 0.05]
print("  sd(cs) bps", round(1e4 * z.cs.std(), 1), "corr(cs, D)", round(z.cs.corr(z.D), 3))
for y in ["gap1", "intra1", "y_730"]:
    zz = z.dropna(subset=[y]); m, n = nw(zz[y], zz[["D", "cs"]]); print(f"  {y} ~ D + cs: D b {m.params['D']:.3f} t {m.tvalues['D']:.2f} | cs b {m.params['cs']:.3f} t {m.tvalues['cs']:.2f} n {n}")
print("\n=== (iv) 5 dk (son ~60 gün): açılış seansı fiyatı (günlük o) vs sürekli işlem fiyatları ===")
m5 = rawd("TCELL.IS", "m5"); m5 = m5[~m5.index.duplicated(keep="last")]
dly = bist_decomp("TCELL.IS")
rows = []
for d, g in m5.groupby(pd.DatetimeIndex(m5["ldate"].values)):
    if d not in dly.index: continue
    o = dly.loc[d, "o"]
    def p_end(hhmm):
        t = pd.Timestamp(f"{d.date()} {hhmm}", tz="UTC") - pd.Timedelta(minutes=5)  # bu anda biten bar
        return g["c"].get(t, np.nan)
    a0655 = g["o"].get(pd.Timestamp(f"{d.date()} 06:55", tz="UTC"), np.nan)
    rows.append(dict(d=d, o=o, auc=a0655, p0705=p_end("07:05"), p0715=p_end("07:15"), p0730=p_end("07:30"), first_cont_open=g["o"].get(pd.Timestamp(f"{d.date()} 07:00", tz="UTC"), np.nan)))
M = pd.DataFrame(rows).set_index("d")
print("  n gün", len(M), "| günlük o == 06:55 barı açılışı oranı:", round((np.abs(np.log(M.o / M.auc)) < 1e-4).mean(), 3))
for c in ["first_cont_open", "p0705", "p0715", "p0730"]:
    r = np.log(M[c] / M.o) * 1e4; print(f"  ln({c}/o): ort {r.mean():.1f} bps, medyan |.| {r.abs().median():.1f} bps, sd {r.std():.1f}")
# sinyal koşullu kayma
M = M.join(q[["U", "D"]].shift(1).rename(columns={"U": "U_prev_def", "D": "Dsig"}), how="left")  # D_{t-1} sinyali gün t için
# U for day t = D_{t-1} - gap_t
gap_t = dly.gap.reindex(M.index); M["Usig"] = M.Dsig - gap_t
for sgn_nm in ["Usig", "Dsig"]:
    s = np.sign(M[sgn_nm]).where(M[sgn_nm].abs() > 0.005, 0)
    for c in ["p0705", "p0730"]:
        k = (s * np.log(M[c] / M.o))[s != 0] * 1e4
        print(f"  |{sgn_nm}|>50 günlerinde yönlü kayma açılış->{c}: ort {k.mean():.1f} bps (n {len(k)})")
