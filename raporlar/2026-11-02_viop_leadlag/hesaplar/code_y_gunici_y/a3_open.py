"""GÖREV 3: AÇILIŞ.
A) Gap fade (47 hisse, sistematik): pozisyon = -sign(gap) (|gap|>eşik), çıkış = günlük kapanış (kapanış müzayedesi).
   Giriş varyantları:  E0 = açılış müzayedesi fiyatı (iyimser; günlük 2014+ ve h1 2023-12+),
                       E2 = ilk 30 dk VWAP vekili = h1 06:30 barının (h+l+c)/3 (2023-12+),
                       E3 = 07:30 fiyatı (2023-12+),
                       E1 = ilk 5 dk (07:00 barı) (h+l+c)/3, E1b = 07:00-07:15 hacim ağırlıklı tipik fiyat (m5, 60 gün).
   Eşikler: |gap| > 0 / 0,5% / 1% / 2% ve z>1 (önceki 60 günün gap std'sine göre, kaydırılmış). Maliyet 0/8/15 bps.
   IS 2014–2020 / OOS 2021–2026 (günlük); h1 için ilk yarı / ikinci yarı. BH-FDR 47 hisse üzerinden.
   Ayrıca havuzlanmış regresyon: intra_i,t = a + b*gap_i,t (+ piyasa gap'i ayrıştırması: hisseye özgü gap vs XU030 gap), gün kümelenmiş SE.
B) Sektör içi gap yayılımı: y (açılış sonrası getiri) ~ own gap + sektör (kendisi hariç akran ortalaması) gap + XU030 gap.
   b(sektör)>0 => hisse açılışta sektörünü eksik yansıttı, sonra yetişiyor (gecikmeli yayılım).
C) Açılışta kim önce hareket ediyor (m5): O->07:30 hareketinin ilk 5/10/15 dk'da gerçekleşen payı (ağırlıklı fiyat katkısı, WPC),
   ve açılış penceresinde (07:05-07:30 hedef barlar) XU030 -> hisse lag-1 katsayısı.
Çıktı: res/a3_fade_daily.csv, res/a3_fade_h1.csv, res/a3_fade_m5.csv, res/a3_pooled.csv, res/a3_sector.csv, res/a3_wpc.csv
"""
import numpy as np, pandas as pd, c_common as c
ll = c.ll; TG = c.VIOP
COSTS = [0, 8, 15]

def fade_stats(sig_gap, y, thr, zthr=None, split="2021-01-01", gapstd=None):
    df = pd.concat([sig_gap.rename("g"), y.rename("y")], axis=1).dropna()
    if zthr is not None:
        sd = gapstd.reindex(df.index)
        pos = -np.sign(df["g"]).where((df["g"].abs() / sd) > zthr, 0.0).fillna(0.0)
    else:
        pos = -np.sign(df["g"]).where(df["g"].abs() > thr, 0.0)
    out = {}
    sp = pd.Timestamp(split)
    for per, m in [("all", np.ones(len(df), bool)), ("is", df.index < sp), ("oos", df.index >= sp)]:
        p = pos[m]; yy = df["y"][m]; act = p != 0; n = int(act.sum()); out[f"{per}_n"] = n
        if n < 15: continue
        g = (p * yy)[act]
        mm, t, _ = ll.nw_t(g.reset_index(drop=True), None, 5)
        out[f"{per}_bps"] = 1e4 * mm; out[f"{per}_t"] = t; out[f"{per}_hit"] = float((g > 0).mean())
        for cst in COSTS[1:]: out[f"{per}_net{cst}"] = 1e4 * mm - cst
        dailypnl = (p * yy - 8e-4 * p.abs())
        out[f"{per}_sharpe8"] = dailypnl.mean() / dailypnl.std() * np.sqrt(252) if dailypnl.std() > 0 else np.nan
    return out

# ---------------- A1: günlük uzun örneklem (E0)
rows = []; DEC = {}
for s in TG + ["XU030"]:
    d = ll.decomp(s); d = d[d.index >= "2014-01-01"]; DEC[s] = d
for s in TG:
    d = DEC[s]; gsd = d["gap"].rolling(60, min_periods=30).std().shift(1)
    for thr, z in [(0, None), (0.005, None), (0.01, None), (0.02, None), (None, 1.0), (None, 2.0)]:
        o = fade_stats(d["gap"], d["intra"], thr, z, gapstd=gsd); o.update(stock=s, thr=thr if z is None else f"z{z}")
        rows.append(o)
A1 = pd.DataFrame(rows)
for th, g in A1.groupby("thr"):
    p = ll.t_to_p(g["all_t"].values); rej, padj = ll.fdr(p); A1.loc[g.index, "fdr"] = rej; A1.loc[g.index, "padj"] = padj
A1.to_csv(c.RES + "/a3_fade_daily.csv", index=False)

# havuzlanmış regresyon: intra ~ idio gap + piyasa gap
pool = []
gm = DEC["XU030"]["gap"]
for s in TG:
    d = DEC[s].copy(); d["gm"] = gm.reindex(d.index); d["stock"] = s; pool.append(d)
PO = pd.concat(pool).dropna(subset=["gap", "intra", "gm"])
PO["date"] = PO.index
rows = []
for per, m in [("all", PO.index >= "2014-01-01"), ("is", PO.index < "2021-01-01"), ("oos", PO.index >= "2021-01-01"), ("2024+", PO.index >= "2024-01-01")]:
    x = PO[m]
    # hisse başı beta ile idio gap (genişleyen değil, tam dönem beta — yalnız ayrıştırma amaçlı)
    beta = x.groupby("stock").apply(lambda g: np.cov(g["gap"], g["gm"])[0, 1] / np.var(g["gm"]))
    idio = x["gap"] - x["stock"].map(beta) * x["gm"]
    for nm, X in [("gap", x[["gap"]].values), ("idio+mkt", np.column_stack([idio, x["gm"]]))]:
        b, se, cov, r2, n = c.ols_cl(x["intra"].values, X, x["date"].values)
        rows.append(dict(period=per, spec=nm, b1=b[1], t1=b[1] / se[1], b2=b[2] if len(b) > 2 else np.nan, t2=b[2] / se[2] if len(b) > 2 else np.nan, r2=r2, n=n))
pd.DataFrame(rows).to_csv(c.RES + "/a3_pooled.csv", index=False)
print(pd.DataFrame(rows).round(4).to_string())

# ---------------- A2: h1 örneklemi (E0 / E2 / E3)
rows = []
for s in TG:
    H = c.h1_panel(s)
    raw = ll.raw(ll.T(s), "h1"); raw = raw[~raw.index.duplicated(keep="last")]
    fb = raw[(raw.index.hour == 6) & (raw.index.minute == 30)].copy(); fb.index = pd.DatetimeIndex(fb.index.tz_convert(None).normalize())
    tp = ((fb["h"] + fb["l"] + fb["c"]) / 3).reindex(H.index)
    ok = ~H["intra"].isna()
    y0 = H["intra"].where(ok); y2 = np.log(H["C"] / tp).where(ok); y3 = np.log(H["C"] / H["P0730"]).where(ok)
    gsd = DEC[s]["gap"].rolling(60, min_periods=30).std().shift(1)
    split = str(H.index[len(H) // 2].date())
    for thr, z in [(0, None), (0.01, None), (0.02, None), (None, 1.0), (None, 2.0)]:
        for en, y in [("E0_open", y0), ("E2_vwap30", y2), ("E3_0730", y3)]:
            o = fade_stats(H["gap"], y, thr, z, split=split, gapstd=gsd); o.update(stock=s, thr=thr if z is None else f"z{z}", entry=en); rows.append(o)
    # ilk 30 dk'nın kendisi (O->07:30) fade'in ne kadarını taşıyor
A2 = pd.DataFrame(rows); A2.to_csv(c.RES + "/a3_fade_h1.csv", index=False)

# ---------------- A3: m5 örneklemi (E0 / E1 / E1b / E4=07:05)
rows = []
for s in TG:
    P = c.m5_panel(s); days = P["days"]
    O = pd.Series(P["dO"], days); C = pd.Series(P["dC"], days)
    tp1 = pd.Series((P["H"][:, 1] + P["L"][:, 1] + P["C"][:, 1]) / 3, days)
    tpm = (P["H"][:, 1:4] + P["L"][:, 1:4] + P["C"][:, 1:4]) / 3; vv = P["V"][:, 1:4]
    tp15 = pd.Series(np.nansum(tpm * vv, axis=1) / np.nansum(vv, axis=1), days)
    p0705 = pd.Series(P["C"][:, 1], days)
    gap = DEC[s]["gap"].reindex(days)
    gsd = DEC[s]["gap"].rolling(60, min_periods=30).std().shift(1)
    for thr, z in [(0, None), (0.01, None), (None, 1.0)]:
        for en, px in [("E0_open", O), ("E1_tp5", tp1), ("E1b_vwap15", tp15), ("E4_0705", p0705)]:
            y = np.log(C / px)
            o = fade_stats(gap, y, thr, z, split=str(days[len(days) // 2].date()), gapstd=gsd); o.update(stock=s, thr=thr if z is None else f"z{z}", entry=en); rows.append(o)
pd.DataFrame(rows).to_csv(c.RES + "/a3_fade_m5.csv", index=False)

# ---------------- B: sektör içi gap yayılımı
gaps = pd.DataFrame({s: DEC[s]["gap"] for s in TG})
intra = pd.DataFrame({s: DEC[s]["intra"] for s in TG})
H1 = {s: c.h1_panel(s) for s in TG}
r30 = pd.DataFrame({s: H1[s]["r1"] for s in TG}); rest = pd.DataFrame({s: np.log(H1[s]["C"] / H1[s]["P0730"]) for s in TG})
rows = []
for sec, mem in c.SECTOR.items():
    for s in mem:
        peers = [p for p in mem if p != s]
        gs = gaps[peers].mean(axis=1) if peers else gm
        for ynm, Y, start in [("intra_2014+", intra[s], "2014-01-01"), ("intra_2021+", intra[s], "2021-01-01"), ("O-0730_h1", r30[s], "2023-12-01"), ("0730-C_h1", rest[s], "2023-12-01")]:
            df = pd.concat([Y.rename("y"), gaps[s].rename("own"), gs.rename("sec"), gm.rename("mkt")], axis=1).dropna()
            df = df[df.index >= start]
            if len(df) < 200: continue
            b, se, cov, r2, n = c.ols_cl(df["y"].values, df[["own", "sec", "mkt"]].values, np.arange(len(df)))
            rows.append(dict(stock=s, sector=sec, y=ynm, b_own=b[1], t_own=b[1] / se[1], b_sec=b[2], t_sec=b[2] / se[2], b_mkt=b[3], t_mkt=b[3] / se[3], n=n, npeers=len(peers)))
SB = pd.DataFrame(rows)
for y, g in SB.groupby("y"):
    rej, padj = ll.fdr(ll.t_to_p(g["t_sec"].values)); SB.loc[g.index, "fdr_sec"] = rej
SB.to_csv(c.RES + "/a3_sector.csv", index=False)

# ---------------- C: açılışta hız (m5): WPC
rows = []
for s in TG + c.IDXL:
    P = c.m5_panel(s); C = P["C"]; O = C[:, 0]
    tot = np.log(C[:, 6] / O)  # O -> 07:30 (slot 6 = 07:25 barı kapanışı)
    w = np.abs(tot) / np.nansum(np.abs(tot))
    out = dict(stock=s)
    for k, lab in [(1, "07:05"), (2, "07:10"), (3, "07:15"), (4, "07:20")]:
        part = np.log(C[:, k] / O)
        ok = (np.abs(tot) > 1e-4) & ~np.isnan(part) & ~np.isnan(tot)
        out[f"wpc_{lab}"] = np.nansum((w * part / np.where(tot == 0, np.nan, tot))[ok]) / np.nansum(w[ok])
    rows.append(out)
pd.DataFrame(rows).to_csv(c.RES + "/a3_wpc.csv", index=False)
print("bitti")
