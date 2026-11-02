"""GÖREV 6: BACKTESTLER (look-ahead yok; maliyet duyarlılığı; IS/OOS; işlem sayısı).
BT1  5 dk lead-lag: lider bar t getirisi |z|>z0 (z: önceki günlerin slot std'si) -> hedefte sign yönünde pozisyon, giriş C_t (ideal) veya O_{t+1} (ilk işlem, gerçekçi),
     çıkış C_{t+h}. Örtüşmesiz. IS = ilk 30 gün, OOS = son 30 gün; IS'te seçilen hedefler OOS'ta.
BT2  Gap fade portföyü: |gap|>1% olan hisselerde -sign(gap), eşit ağırlık; giriş E0 açılış / E2 ilk-30dk VWAP vekili / E3 07:30; çıkış kapanış.
BT3  Sektör gap yetişmesi: s = akran gap ort. - kendi gap; |s|>1% -> sign(s); E0->kapanış (2014+), E0->07:30, E2->C, E3->C (h1).
BT4  Gün-içi momentum XU030 (VİOP endeks vadelisi vekili): 14:30'da sign(r1 = O->07:30) veya sign(r_first), çıkış kapanış; yıllık kırılım.
BT5  Kapanış müzayedesi dönüşü: -sign(CA_t) |CA|>eşik, giriş C_t (spot 'kapanış fiyatından işlemler' seansı varsayımı), çıkış O_{t+1} veya 07:30_{t+1}.
Çıktı: res/a6_bt.csv (tek tablo), res/a6_bt_years.csv
"""
import numpy as np, pandas as pd, c_common as c
ll = c.ll; TG = c.VIOP
OUT = []; YRS = []
def rec(name, variant, per, pnl_daily, ntr, cost_list=(0, 8, 15), note="", per_trade=None, ppy=252):
    """pnl_daily: gün bazında brüt ortalama işlem getirisi (portföy) — maliyet işlem başına düşülür."""
    x = pnl_daily.dropna()
    if len(x) < 10: return
    m, t, _ = ll.nw_t(x.reset_index(drop=True), None, 5)
    o = dict(bt=name, variant=variant, period=per, n_days=len(x), n_trades=int(ntr), gross_bps=1e4 * m, t=t, hit=float((x > 0).mean()), note=note)
    for cst in cost_list:
        net = x - cst / 1e4
        o[f"net{cst}_bps"] = 1e4 * net.mean(); o[f"sharpe{cst}"] = net.mean() / net.std() * np.sqrt(ppy) if net.std() > 0 else np.nan
    if per_trade is not None: o["gross_per_trade_bps"] = 1e4 * np.nanmean(per_trade)
    OUT.append(o)

# ============ BT1: 5 dk lead-lag
R = {s: c.m5_ret(s) for s in set(TG) | set(c.LEADERS)}
PAN = {s: c.m5_panel(s) for s in TG}
nd = R["XU030"].shape[0]
def zsig(L):
    X = R[L]; Z = np.full_like(X, np.nan)
    for d in range(10, nd):
        sd = np.nanstd(X[:d], axis=0); Z[d] = X[d] / np.where(sd > 0, sd, np.nan)
    return Z
ZC = {}
def bt1(L, Y, z0, h, sgn=1.0, entry="o"):
    if L not in ZC: ZC[L] = zsig(L)
    Z = ZC[L]; P = PAN[Y]; C = P["C"][:, 1:]; O = P["O"][:, 1:]
    trades = []  # (day, pnl)
    for d in range(10, nd):
        t = 0
        while t < C.shape[1] - h - 1:
            z = Z[d, t]
            if np.isnan(z) or abs(z) <= z0: t += 1; continue
            px_in = O[d, t + 1] if entry == "o" else C[d, t]
            px_out = C[d, t + h] if entry == "c" else C[d, t + h]
            if entry == "o": px_out = C[d, t + h]  # giriş t+1 barının ilk işlemi, çıkış t+h barının kapanışı (h>=1)
            if np.isnan(px_in) or np.isnan(px_out): t += 1; continue
            trades.append((d, sgn * np.sign(z) * np.log(px_out / px_in))); t += h + 1
    return pd.DataFrame(trades, columns=["d", "pnl"])

pairs = [("XU030", y, 1.0) for y in TG] + [("XBANK", "GARAN", 1.0), ("AKBNK", "GARAN", 1.0), ("ISCTR", "GARAN", 1.0), ("XBANK", "AKBNK", 1.0), ("BIMAS", "MGROS", 1.0), ("TUPRS", "THYAO", -1.0), ("AKBNK", "THYAO", 1.0)]
rows = []
for L, Y, sg in pairs:
    for z0 in [1.5, 2.5]:
        for h in [1, 3]:
            for en in ["c", "o"]:
                T = bt1(L, Y, z0, h, sg, en)
                if len(T) < 20: continue
                for per, m in [("IS", T.d < 30), ("OOS", T.d >= 30)]:
                    x = T[m]["pnl"]
                    if len(x) < 10: continue
                    mm, tt, _ = ll.nw_t(x.reset_index(drop=True), None, 3)
                    rows.append(dict(leader=L, target=Y, z0=z0, h=h, entry=en, period=per, n=len(x), gross_bps=1e4 * mm, t=tt, hit=float((x > 0).mean())))
B1 = pd.DataFrame(rows); B1.to_csv(c.RES + "/a6_bt1_m5.csv", index=False)
# özet: XU030 -> 47 (medyan), IS seçilmiş -> OOS
for z0 in [1.5, 2.5]:
    for h in [1, 3]:
        for en in ["c", "o"]:
            g = B1[(B1.leader == "XU030") & (B1.z0 == z0) & (B1.h == h) & (B1.entry == en)]
            gi = g[g.period == "IS"].set_index("target"); go = g[g.period == "OOS"].set_index("target")
            sel = gi[(gi.t > 2)].index
            o = dict(bt="BT1_m5_XU030->47", variant=f"z>{z0},h={h},giris={'C_t(ideal)' if en=='c' else 'O_t+1(ilk islem)'}", period="IS/OOS",
                     n_trades=int(go["n"].sum()), gross_bps=go["gross_bps"].median(), t=np.nan, note=f"medyan hisse OOS brüt; IS medyan {gi['gross_bps'].median():.2f}; IS t>2 seçilen {len(sel)} hisse OOS ort {go.loc[go.index.intersection(sel),'gross_bps'].mean():.2f} bps (n={int(go.loc[go.index.intersection(sel),'n'].sum())})")
            for cst in [0, 3, 8, 15]: o[f"net{cst}_bps"] = go["gross_bps"].median() - cst
            OUT.append(o)

# ============ BT2: gap fade portföyü
DEC = {s: ll.decomp(s) for s in TG + ["XU030"]}
gaps = pd.DataFrame({s: DEC[s]["gap"] for s in TG}); gaps = gaps[gaps.index >= "2014-01-01"]
intra = pd.DataFrame({s: DEC[s]["intra"] for s in TG}).reindex(gaps.index)
LQ = pd.read_csv(c.RES + "/a0_liq.csv").set_index("stock"); liquid = LQ.index[LQ["liq_rank"] <= 23]; illiq = LQ.index[LQ["liq_rank"] > 23]
def port(pos, y):
    g = (pos * y).where(pos != 0)
    return g.mean(axis=1), int((pos != 0).sum().sum()), g
for thr in [0.01, 0.02]:
    pos = -np.sign(gaps).where(gaps.abs() > thr, 0.0)
    for uni, cols in [("47", TG), ("likit23", list(liquid)), ("illikit24", list(illiq))]:
        pp, ntr, g = port(pos[cols], intra[cols])
        for per, m in [("IS2014-20", pp.index < "2021-01-01"), ("OOS2021-26", pp.index >= "2021-01-01")]:
            rec("BT2_gapfade_E0_open", f"|gap|>{thr:.0%},{uni}", per, pp[m], (pos[cols][m] != 0).sum().sum())
        if uni == "47":
            yr = (1e4 * pp.groupby(pp.index.year).mean()).round(1); YRS.append(pd.Series(yr, name=f"BT2_E0_|gap|>{thr:.0%}_47"))
    # IS seçimi -> OOS
    isr = (pos * intra).where(pos != 0)[gaps.index < "2021-01-01"]
    tt = isr.mean() / isr.std() * np.sqrt(isr.count())
    sel = list(tt[tt > 2].index)
    pp, ntr, g = port(pos[sel], intra[sel]); m = pp.index >= "2021-01-01"
    rec("BT2_gapfade_E0_open", f"|gap|>{thr:.0%},IS t>2 secilen {len(sel)}: {','.join(sel)}", "OOS2021-26", pp[m], (pos[sel][m] != 0).sum().sum())
# h1 dönemi girişler
H1 = {s: c.h1_panel(s) for s in TG + ["XU030"]}
days = H1["XU030"].index; half = days[len(days) // 2]
def h1df(f): return pd.DataFrame({s: f(s) for s in TG})
TP = {}
for s in TG:
    raw = ll.raw(ll.T(s), "h1"); raw = raw[~raw.index.duplicated(keep="last")]
    fb = raw[(raw.index.hour == 6) & (raw.index.minute == 30)].copy(); fb.index = pd.DatetimeIndex(fb.index.tz_convert(None).normalize())
    TP[s] = ((fb["h"] + fb["l"] + fb["c"]) / 3).reindex(days)
okm = h1df(lambda s: H1[s]["intra"].notna())
gH = h1df(lambda s: H1[s]["gap"]).where(okm)
Y0 = h1df(lambda s: H1[s]["intra"]); Y2 = h1df(lambda s: np.log(H1[s]["C"] / TP[s])).where(okm); Y3 = h1df(lambda s: np.log(H1[s]["C"] / H1[s]["P0730"])).where(okm)
for thr in [0.01, 0.02]:
    pos = -np.sign(gH).where(gH.abs() > thr, 0.0).fillna(0.0)
    for en, Y in [("E0_open", Y0), ("E2_vwap30", Y2), ("E3_0730", Y3)]:
        for uni, cols in [("47", TG), ("illikit24", list(illiq))]:
            pp, ntr, g = port(pos[cols], Y[cols])
            for per, m in [("IS(1.yarı)", pp.index < half), ("OOS(2.yarı)", pp.index >= half)]:
                rec(f"BT2_gapfade_{en}", f"|gap|>{thr:.0%},{uni},h1 2023-12+", per, pp[m], (pos[cols][m] != 0).sum().sum())

# ============ BT3: sektör gap yetişmesi
secg = {}
for sec, mem in c.SECTOR.items():
    for s in mem:
        peers = [p for p in mem if p != s]
        secg[s] = gaps[peers].mean(axis=1) if peers else DEC["XU030"]["gap"].reindex(gaps.index)
S_ = pd.DataFrame({s: secg[s] - gaps[s] for s in TG})
for thr in [0.01, 0.02]:
    pos = np.sign(S_).where(S_.abs() > thr, 0.0).fillna(0.0)
    pp, ntr, g = port(pos, intra)
    for per, m in [("IS2014-20", pp.index < "2021-01-01"), ("OOS2021-26", pp.index >= "2021-01-01")]:
        rec("BT3_sektor_yetisme_E0->C", f"|s|>{thr:.0%}", per, pp[m], (pos[m] != 0).sum().sum())
    YRS.append(pd.Series((1e4 * pp.groupby(pp.index.year).mean()).round(1), name=f"BT3_E0_|s|>{thr:.0%}"))
    posH = pos.reindex(days).fillna(0.0)
    for en, Y in [("E0->07:30", h1df(lambda s: H1[s]["r1"])), ("E0->C", Y0), ("E2->C", Y2), ("E3->C", Y3)]:
        pp, ntr, g = port(posH, Y)
        for per, m in [("IS(1.yarı)", pp.index < half), ("OOS(2.yarı)", pp.index >= half)]:
            rec(f"BT3_sektor_yetisme_{en}", f"|s|>{thr:.0%},h1 2023-12+", per, pp[m], (posH[m] != 0).sum().sum())

# ============ BT4: XU030 gün-içi momentum
X = H1["XU030"]; gX = DEC["XU030"]["gap"].reindex(days)
for sig_name, sig in [("sign(r1:O->07:30)", np.sign(X["r1"])), ("sign(r_first:Cprev->07:30)", np.sign(gX + X["r1"]))]:
    y = X["r9"]; pos = sig.where(y.notna()); pnl = pos * y
    for per, m in [("IS(1.yarı)", days < half), ("OOS(2.yarı)", days >= half)]:
        rec("BT4_XU030_gunici_momentum_14:30->C", sig_name, per, pnl[m], (pos[m] != 0).sum(), cost_list=(0, 2, 4, 8))
    YRS.append(pd.Series((1e4 * pnl.groupby(pnl.index.year).mean()).round(1), name=f"BT4_{sig_name}"))

# ============ BT5: kapanış müzayedesi dönüşü
CA = h1df(lambda s: H1[s]["ca"])
nO = h1df(lambda s: H1[s]["gap"].shift(-1))  # C_t -> O_{t+1}
n730 = h1df(lambda s: (H1[s]["gap"] + H1[s]["r1"]).shift(-1))
for thr in [0.0, 0.0025, 0.005]:
    pos = -np.sign(CA).where(CA.abs() > thr, 0.0).fillna(0.0)
    for ex, Y in [("->O_t+1", nO), ("->07:30_t+1", n730)]:
        pp, ntr, g = port(pos, Y)
        for per, m in [("IS(1.yarı)", pp.index < half), ("OOS(2.yarı)", pp.index >= half)]:
            rec("BT5_kapanis_muzayede_donusu", f"|CA|>{thr*1e4:.0f}bps,C_t{ex},yaz günleri", per, pp[m], (pos[m] != 0).sum().sum())

BT = pd.DataFrame(OUT); BT.to_csv(c.RES + "/a6_bt.csv", index=False)
pd.concat(YRS, axis=1).to_csv(c.RES + "/a6_bt_years.csv")
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 70)
print(BT.drop(columns=[x for x in BT.columns if x.startswith("sharpe")]).round(2).to_string())
print(pd.concat(YRS, axis=1).to_string())
