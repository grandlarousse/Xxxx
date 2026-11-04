"""Adım 2: Pratik kuralın backtest'i (VİOP uzlaşma fiyatlarıyla).
Sinyal varyantları: V0 araştırma (VİOP XAUUSD uzlaşma değişimi), V18 = 18:00 TSİ (15:00 UTC) GC=F anlık, V17 = 17:00 TSİ, m5 17:55/17:45.
Uygulama varyantları: E0 araştırma getirisi; E1 aynı kontrat + vadeli beta; E2 aynı kontrat + spot (Yahoo) beta; E3 E2 + tam sayı kontrat (1 XU030 + N TRALT);
E4 E3 + limit kilidi kuralları."""
import pl, numpy as np, pandas as pd, json
cl, ev = pl.cl, pl.ev
pl.install_panel()
c = cl.cal(); LAST = c[-1]
OUT = pl.R + "/sonuc"
print("takvim son günü", LAST.date(), "gün", len(c))
# ---------------- sinyaller
g0 = ev.R("XAUUSD"); sd0 = g0.rolling(250, min_periods=100).std().shift(1); z0 = g0 / sd0
r18raw = pl.snap_ret(pl.snap("GC=F", "h1", 15, 0)); r17raw = pl.snap_ret(pl.snap("GC=F", "h1", 14, 0))
r18, f18 = pl.yahoo_roll_fix(r18raw, g0); r17, f17 = pl.yahoo_roll_fix(r17raw, g0)
print("Yahoo GC=F vade geçiş düzeltmesi (18:00):", [(str(a.date()), b) for a, b in f18])
print("Yahoo GC=F vade geçiş düzeltmesi (17:00):", [(str(a.date()), b) for a, b in f17])
r1755 = pl.snap_ret(pl.snap("GC=F", "m5", 14, 55)); r1745 = pl.snap_ret(pl.snap("GC=F", "m5", 14, 45))
# sigma alternatifleri
gcd = pl.ydaily("GC=F"); rg = np.log(gcd["c"].where(gcd["c"] > 0)).diff(); rg_b = cl.to_bist(rg, "after")
sd_gcd = rg_b.rolling(250, min_periods=100).std().shift(1)
sd_snap = r18.rolling(250, min_periods=100).std().shift(1)
sd_script = r18raw.rolling(250, min_periods=100).std().shift(1)      # sinyal_altin.py ile aynı: Yahoo GC=F 15:00 UTC ham anlık değişimlerinin std'si
sd_script = sd_script.where(sd_script.notna(), sd0)
cmp_ = pd.concat([sd0.rename("sd_uzlasma"), sd_gcd.rename("sd_GCgunluk"), sd_snap.rename("sd_anlik18")], axis=1).dropna()
print("sigma oranları (anlık18 mevcut dönem):", (cmp_["sd_GCgunluk"] / cmp_["sd_uzlasma"]).describe()[["mean", "min", "max"]].round(3).to_dict(),
      (cmp_["sd_anlik18"] / cmp_["sd_uzlasma"]).describe()[["mean", "min", "max"]].round(3).to_dict())
s_all = pd.concat([sd0.rename("u"), sd_gcd.rename("g")], axis=1).dropna(); s_all = s_all[s_all.index >= "2018-12-17"]
print("sigma GC günlük / uzlaşma 2018-12+:", (s_all.g / s_all.u).describe()[["mean", "min", "max"]].round(3).to_dict())
Z = {"V0_uzlasma": z0, "V18_1800": r18 / sd0, "V18_ham_yahoo": r18raw / sd0, "V17_1700": r17 / sd0,
     "V18_sigmaGC": r18 / sd_gcd, "V18_sigmaBetik": r18 / sd_script, "V0_sigmaGC": g0 / sd_gcd, "m5_1755": r1755 / sd0, "m5_1745": r1745 / sd0}
# ---------------- getiriler
L = ev.legs("TRALT"); y_res = cl.fwd(L["hedged"], 2)
yT, cT, pT = pl.same_contract_fwd("TRALT", 2); yX, cX, pX = pl.same_contract_fwd("XU030", 2)
b_fut = cl.roll_beta(ev.R("TRALT"), ev.R("XU030"), 250, 100); b_sp = pl.spot_beta()
print("beta: vadeli vs spot korelasyon", round(pd.concat([b_fut, b_sp], axis=1).dropna().corr().iloc[0, 1], 3),
      "ort fark", round((b_sp - b_fut).dropna().mean(), 3), "son", round(b_fut.dropna().iloc[-1], 3), round(b_sp.dropna().iloc[-1], 3))
multX = pd.Series(np.where(c < pd.Timestamp("2020-07-27"), 100.0, 10.0), index=c)
nX = pX * multX; nT = pT * 100.0
NT = (nX / (b_sp * nT)).round().clip(lower=1); b_eff = nX / (NT * nT)
y_E1 = yT - b_fut * yX; y_E2 = yT - b_sp * yX; y_E3 = yT - b_eff * yX
print("tam sayı yuvarlama: |b_eff/b - 1| ort", round(((b_eff / b_sp) - 1).abs()[c >= "2018-12-17"].dropna().mean(), 3), "son NT", NT.dropna().iloc[-1])
tickX = np.where(pX < 1000, 0.025, 1.0)
cost_tick = (2 * 0.01 / pT * 1e4 + 4.2) + b_sp.clip(lower=0) * (2 * tickX / pX * 1e4 + 4.2)
cost_tick = pd.Series(cost_tick, index=c)
START = "2018-12-17"
def cut(y, a=START, b=None):
    y = y[y.index >= a]; return y[y.index <= b] if b else y
rows = []
def rep(lab, z, y, a=START, b=None, costs=(("8+3", 11.0), ("15+3", 18.0), ("tik", cost_tick)), keep=False):
    tr = pl.run_trades(z, cut(y, a, b), 2, 1.0)
    out = {}
    for cn, cv in costs:
        s = pl.stats(tr, cv); s.update(var=lab, cost=cn, start=a); rows.append(s); out[cn] = s
    return tr, out
# A) tam dönem: araştırma -> pratik uygulama zinciri (V0 sinyali)
trA0, _ = rep("A0 araştırma getirisi (front-geçişli, vadeli beta)", z0, y_res)
trA1, _ = rep("A1 aynı kontrat + vadeli beta", z0, y_E1)
trA2, _ = rep("A2 aynı kontrat + spot beta (Yahoo)", z0, y_E2)
trA3, _ = rep("A3 + tam sayı kontrat (1 XU030 + N TRALT)", z0, y_E3)
trAr, _ = rep("Araw hedge'siz TRALT (aynı kontrat)", z0, yT)
trAg, _ = rep("A0' sigma=GC günlük", g0 / sd_gcd, y_E3)
# B) 2024-07+ zamanlama karşılaştırması (aynı uygulama E3)
B0 = "2024-07-01"
for k in ["V0_uzlasma", "V18_1800", "V18_ham_yahoo", "V17_1700", "V18_sigmaGC", "V18_sigmaBetik"]:
    rep("B " + k, Z[k], y_E3, a=B0)
for k in ["V0_uzlasma", "m5_1755", "m5_1745"]:
    rep("C " + k, Z[k], y_E3, a="2026-08-27")
# uyum
def agree(za, zb, a):
    m = (za.index >= a) & za.notna() & zb.notna()
    A = za[m]; Bz = zb[m]; s1 = A.abs() > 1; s2 = Bz.abs() > 1
    return dict(n_gun=int(m.sum()), corr=round(np.corrcoef(A, Bz)[0, 1], 3), n_sinyal_ref=int(s1.sum()), n_sinyal_alt=int(s2.sum()),
                ikisinde=int((s1 & s2 & (np.sign(A) == np.sign(Bz))).sum()), ters_isaret=int((s1 & s2 & (np.sign(A) != np.sign(Bz))).sum()),
                isaret_uyumu_refsinyal=round(float((np.sign(A[s1]) == np.sign(Bz[s1])).mean()), 3))
AG = {k: agree(z0, Z[k], B0 if not k.startswith("m5") else "2026-08-27") for k in ["V18_1800", "V18_ham_yahoo", "V17_1700", "V18_sigmaGC", "V18_sigmaBetik", "m5_1755", "m5_1745"]}
print("uyum (referans V0):"); [print(" ", k, v) for k, v in AG.items()]
# D) hibrit pratik seri: 18:00 anlık (2024-07+) yoksa uzlaşma
zH = Z["V18_1800"].where(Z["V18_1800"].notna() & (c >= pd.Timestamp(B0)), z0)
trH, _ = rep("D hibrit (2024-07+ 18:00 anlık, öncesi uzlaşma) + E3", zH, y_E3)
# E) limit kilidi kuralları + aynı yönde devam maliyet tasarrufu (hibrit sinyal, E3)
FL = {"vadeli": pl.fut_lock_flags("TRALT"), "spot": pl.limit_flags("TRALT.IS")}
def simulate(z, thr=1.0, h=2, lock=True, start=START, maxext=3, fl=FL["vadeli"]):
    tT, _ = pl.code_ret("TRALT"); tX, _ = pl.code_ret("XU030")
    zz = z.reindex(c).values; n = len(c); i = int(np.searchsorted(c.values, np.datetime64(pd.Timestamp(start))))
    rows_ = []; prev_exit = None; prev_dir = 0; skipped = 0; extended = 0
    while i < n - h:
        if np.isfinite(zz[i]) and abs(zz[i]) > thr and isinstance(cT.iloc[i], str) and np.isfinite(b_eff.iloc[i]):
            d = np.sign(zz[i])
            if lock and fl.iloc[i] == d:            # alış yönünde tavan / satış yönünde taban kilidi -> giriş yapılamaz
                skipped += 1; i += 1; continue
            H = h
            if lock:
                while i + H < n - 1 and fl.iloc[i + H] == -d and H < h + maxext: H += 1
                extended += int(H > h)
            if i + H >= n: break
            segT = tT[cT.iloc[i]].values[i + 1:i + H + 1]; segX = tX[cX.iloc[i]].values[i + 1:i + H + 1]
            if not (np.all(np.isfinite(segT)) and np.all(np.isfinite(segX))): i += 1; continue
            gr = d * (segT.sum() - b_eff.iloc[i] * segX.sum())
            cont = (prev_exit == i) and (prev_dir == d)
            rows_.append((c[i], d, gr, zz[i], H, cont, cost_tick.iloc[i], NT.iloc[i], nT.iloc[i], nX.iloc[i], c[i + H]))
            prev_exit = i + H; prev_dir = d; i += H
        else:
            i += 1
    T = pd.DataFrame(rows_, columns=["date", "dir", "gross", "z", "hold", "devam", "cost_tick", "N_TRALT", "notional_TRALT", "notional_XU030", "exit"]).set_index("date")
    return T, skipped, extended
zHs = Z["V18_sigmaBetik"].where(Z["V18_sigmaBetik"].notna() & (c >= pd.Timestamp(B0)), z0)
zH17 = Z["V17_1700"].where(Z["V17_1700"].notna() & (c >= pd.Timestamp(B0)), z0)
for lab, zz, fk in (("E0 uzlaşma sinyali + E3 + vadeli kilit kuralı", z0, "vadeli"), ("E0s uzlaşma sinyali + E3 + spot kilit kuralı", z0, "spot"),
                    ("E17 hibrit 17:00 + E3 + vadeli kilit", zH17, "vadeli"), ("E18 hibrit 18:00 (sigma uzlaşma) + E3 + vadeli kilit", zH, "vadeli"),
                    ("P PRATİK KURAL: hibrit 18:00 (betik sigması) + E3 + vadeli kilit", zHs, "vadeli")):
    TE, sk, ex = simulate(zz, fl=FL[fk])
    print(lab, "| atlanan giriş", sk, "uzatılan çıkış", ex, "aynı yönde devam", int(TE["devam"].sum()), "ort tutma", round(TE["hold"].mean(), 2))
    for cn, cv in (("8+3", 11.0), ("15+3", 18.0), ("tik", TE["cost_tick"])):
        s = pl.stats(TE[["dir", "gross"]], cv); s.update(var=lab, cost=cn, start=START); rows.append(s)
    cs = pd.Series(np.where(TE["devam"], 0.0, 11.0), index=TE.index)
    s = pl.stats(TE[["dir", "gross"]], cs); s.update(var=lab + " (+devamda işlem yok)", cost="8+3", start=START); rows.append(s)
    if lab.startswith("P "): TP = TE.copy()
TE = TP; TE.to_csv(OUT + "/pratik_islemler.csv")
G = pd.DataFrame(rows); cols = ["var", "cost", "start", "n", "per_yr", "gross", "net", "t", "hit", "IS", "IS_t", "OOS", "OOS_t", "y2024_26", "drop_top10", "maxdd_bps", "worst", "worst_date", "by_year"]
G[cols].to_csv(OUT + "/backtest_ozet.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 120)
print(G[cols[:-1]].to_string())
print(G[["var", "cost", "by_year"]][G.cost == "8+3"].to_string())
# risk / TL
_, sT = pl.code_ret("TRALT"); _, sX = pl.code_ret("XU030")
pT_now = float(sT[cT.iloc[-1]].iloc[-1]); pX_now = float(sX[cX.iloc[-1]].iloc[-1])
now = dict(date=str(LAST.date()), code_T=cT.iloc[-1], code_X=cX.iloc[-1], TRALT=pT_now, XU030=pX_now, beta_spot=float(b_sp.dropna().iloc[-1]), beta_fut=float(b_fut.dropna().iloc[-1]),
           NT=int(round(10 * pX_now / (float(b_sp.dropna().iloc[-1]) * pT_now * 100))))
now["notional_T"] = now["NT"] * 100 * now["TRALT"]; now["notional_X"] = 10 * now["XU030"]
sdg = TE["gross"].std() * 1e4; sdg24 = TE["gross"][TE.index >= "2024-01-01"].std() * 1e4
now["sd_trade_bps_all"] = round(sdg, 0); now["sd_trade_bps_2024"] = round(sdg24, 0)
now["sd_trade_TL_unit"] = round(sdg24 / 1e4 * now["notional_T"], 0)
net = TE["gross"] * 1e4 - 11
now["mean_net_TL_unit"] = round(net.mean() / 1e4 * now["notional_T"], 0); now["worst_TL_unit"] = round(net.min() / 1e4 * now["notional_T"], 0)
cum = net.cumsum(); now["maxdd_bps"] = round((cum - cum.cummax()).min(), 0); now["maxdd_TL_unit"] = round(now["maxdd_bps"] / 1e4 * now["notional_T"], 0)
now["p5_bps"] = round(np.percentile(net, 5), 0); now["p5_TL_unit"] = round(now["p5_bps"] / 1e4 * now["notional_T"], 0)
print("birim (güncel fiyat):", json.dumps(now, ensure_ascii=False))
json.dump(dict(now=now, agree=AG, roll_flags18=[(str(a.date()), b) for a, b in f18]), open(OUT + "/backtest_meta.json", "w"), ensure_ascii=False, indent=1, default=str)
# z serileri (güncel durum için)
pd.concat([g0.rename("g_uzlasma"), sd0.rename("sd_uzlasma"), z0.rename("z_uzlasma"), r18.rename("g_1800"), Z["V18_1800"].rename("z_1800"),
           r1755.rename("g_1755"), Z["m5_1755"].rename("z_1755"), b_sp.rename("beta_spot"), b_fut.rename("beta_vadeli"), NT.rename("N_TRALT_birim")], axis=1).to_csv(OUT + "/seriler.csv")
