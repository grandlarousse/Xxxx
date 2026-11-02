"""v5: veri madenciliği (spesifikasyon eğrisi), uç değer testinin null kalibrasyonu, TUR/COMBO, gün etkisi,
ES gece kontrolü (saatlik dönem)."""
import sys, itertools; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_A4_b")
from core import *
pd.set_option("display.width", 250)
SG = pd.read_parquet(RES + "/signals.parquet"); AIR = SG.AIR_C
TGT = ["THYAO", "PGSUS", "TAVHL"]
D = {st: bist_day(st + ".IS") for st in TGT}
rng = np.random.default_rng(7)

# ---------- (1) spesifikasyon eğrisi
REU = {s: ret_own(s) for s in EU_AIR}; RUS = {s: ret_own(s) for s in US_AIR}
sx = ret_own("^STOXX"); sp = ret_own("^GSPC")
def leg(R, ix, resid, wb, wz):
    X = pd.concat(R, axis=1); b = X.mean(1).where(X.notna().sum(1) >= 2).dropna()
    x = rresid(b, ix, wb) if resid else b
    return to_bist(zs(x, wz, min(60, wz // 2)).clip(-3, 3))
rows = []
cache = {}
for resid, wb, wz in itertools.product([True, False], [120, 250, 500], [120, 250, 500]):
    if not resid and wb != 250: continue
    e = leg(REU, sx, resid, wb, wz); u = leg(RUS, sp, resid, wb, wz)
    for legs in ["EU+US", "EU", "US"]:
        s = e + u if legs == "EU+US" else (e if legs == "EU" else u)
        for thr in [0.0, 0.5, 1.0, 1.5]:
            for st in TGT:
                r = bt_periods(s, D[st].intra, 8, thr, ("IS", "OOS"))
                rows.append({"resid": resid, "wb": wb, "wz": wz, "legs": legs, "thr": thr, "tgt": st,
                             "IS_bps": r["IS"]["bps"], "IS_t": r["IS"]["t"], "OOS_bps": r["OOS"]["bps"], "OOS_t": r["OOS"]["t"], "OOS_gross": r["OOS"]["gross"]})
SC = pd.DataFrame(rows); SC.to_csv(RES + "/v5_speccurve.csv", index=False)
print("== (1) Spesifikasyon eğrisi: %d varyant x 3 hisse ==" % (len(SC) // 3))
for st in TGT:
    x = SC[SC.tgt == st]
    print(f"{st}: OOS net>0 oranı {(x.OOS_bps > 0).mean():.2f}; OOS t>2 oranı {(x.OOS_t > 2).mean():.2f}; IS t>2 oranı {(x.IS_t > 2).mean():.2f}; "
          f"OOS net medyan {x.OOS_bps.median():.1f} bps (t medyan {x.OOS_t.median():.2f}); IS&OOS ikisi de t>1,5: {((x.IS_t > 1.5) & (x.OOS_t > 1.5)).mean():.2f}")
    # IS'te en iyi varyantı seç -> OOS (gerçek seçim simülasyonu)
    best = x.sort_values("IS_t", ascending=False).iloc[0]
    print(f"   IS'te en iyi varyant: resid={best.resid} wb={best.wb} wz={best.wz} legs={best.legs} thr={best.thr} IS t {best.IS_t:.2f} -> OOS {best.OOS_bps:.1f} bps (t {best.OOS_t:.2f})")
    top5 = x.sort_values("IS_t", ascending=False).head(5)
    print(f"   IS en iyi 5 varyantın OOS ort.: {top5.OOS_bps.mean():.1f} bps (t ort {top5.OOS_t.mean():.2f})")
print(SC.groupby(["legs", "resid", "thr"])[["IS_t", "OOS_t"]].median().round(2).unstack("thr").to_string())

# ---------- (2) uç değer testinin null kalibrasyonu (rastgele işaret, aynı işlem günleri)
print("\n== (2) 'En iyi 10/20 günü çıkar' — rastgele işaret null'unda aynı işlem (OOS) ==")
for st in TGT:
    df = pd.concat([AIR.rename("s"), D[st].intra.rename("y")], axis=1).dropna(); df = df[(df.s.abs() > 1) & (df.index >= SPLIT)]
    g = np.sign(df.s.values) * df.y.values
    def stat(x, k): return np.sort(x)[::-1][k:].mean()
    obs10, obs20 = stat(g, 10), stat(g, 20)
    nul10, nul20 = [], []
    for i in range(2000):
        sh = rng.permutation(np.sign(df.s.values)) * df.y.values
        nul10.append(stat(sh, 10)); nul20.append(stat(sh, 20))
    nul10, nul20 = np.array(nul10), np.array(nul20)
    print(f"{st}: brüt, en iyi 10 çıkar: gözlenen {1e4*obs10:.1f} vs null medyan {1e4*np.median(nul10):.1f} (p {np.mean(nul10>=obs10):.3f}); "
          f"en iyi 20 çıkar: {1e4*obs20:.1f} vs null {1e4*np.median(nul20):.1f} (p {np.mean(nul20>=obs20):.3f})")

# ---------- (3) TUR bacağı ve COMBO (hizalama C)
print("\n== (3) TUR_{t-1} -> gün-içi ve COMBO (C hizalaması) ==")
TURr = to_bist(ret_own("TUR"))
for st in TGT:
    y = D[st].intra
    df = pd.concat([TURr.rename("x"), y.rename("y")], axis=1).dropna(); df = df[df.index >= "2014-01-01"]
    r, n = ols_nw(df.y, df[["x"]])
    cy = df.groupby(df.index.year).apply(lambda g: g.x.corr(g.y)).round(2)
    combo = AIR - SG.zTUR_C
    rb = bt_periods(combo, y, 8, 1.0, ("IS", "OOS", "24-26")); ra = bt_periods(AIR, y, 8, 1.0, ("IS", "OOS", "24-26"))
    rt = bt_periods(-SG.zTUR_C, y, 8, 1.0, ("IS", "OOS", "24-26"))
    print(f"{st}: corr {df.x.corr(df.y):.3f} (NW t {r.loc['x','t']:.2f}); yıllar {cy.to_dict()}")
    print(f"   COMBO {[(p, round(v['bps'],1), round(v['t'],2)) for p, v in rb.items()]} | AIR {[(p, round(v['bps'],1), round(v['t'],2)) for p, v in ra.items()]} | -TUR {[(p, round(v['bps'],1), round(v['t'],2)) for p, v in rt.items()]}")

# ---------- (4) haftanın günü
print("\n== (4) Haftanın günü (C, brüt bps/işlem, ALL) ==")
for st in TGT:
    g, _ = pnl_series(AIR, D[st].intra); g = g[g.index >= "2014-01-01"]
    print(st, (1e4 * g.groupby(g.index.dayofweek).mean()).round(1).to_dict(), g.groupby(g.index.dayofweek).size().to_dict())

# ---------- (5) saatlik dönem: ES gece hareketi (BIST kapanışı 15:00 -> 06:30 UTC) ve AB havayolu BIST-kapanış-sonrası kısmı
print("\n== (5) Saatlik dönem (2023-11+): gece ES ve AB havayolu kapanış-sonrası kontrolü ==")
def snap(sym, hhmm):
    h = raw(sym, "h1")
    if h is None: return None
    h = h[h.index.strftime("%H:%M") <= hhmm]
    s = h.groupby(pd.DatetimeIndex(h.ldate).normalize()).c.last()
    return s
es = raw("ES=F", "h1"); esc = es.c
cal = bist_cal(); cal = cal[cal >= "2023-12-01"]
ov = []
for t in cal:
    t0 = pd.Timestamp(t.date(), tz="UTC")
    a = esc[esc.index <= t0 - pd.Timedelta(days=1) + pd.Timedelta(hours=14, minutes=59)]
    b = esc[esc.index <= t0 + pd.Timedelta(hours=6, minutes=30)]
    if len(a) and len(b): ov.append((t, np.log(b.iloc[-1] / a.iloc[-1])))
ESov = pd.Series(dict(ov))
# AB havayolları: BIST kapanışından (15:00 UTC) AB kapanışına kalan parça (LHA, AF, IAG h1)
parts = []
for s in ["LHA.DE", "AF.PA", "IAG.L"]:
    h = raw(s, "h1"); d = pd.DatetimeIndex(h.ldate).normalize()
    pre = h[h.index.hour < 15].groupby(d[h.index.hour < 15]).c.last(); full = h.groupby(d).c.last()
    parts.append(np.log(full / pre).rename(s))
EUpost = pd.concat(parts, axis=1).mean(1)
EUpost_b = to_bist(EUpost)
for st in TGT:
    d = D[st]; y = d.intra[d.index >= "2023-12-01"]
    M = pd.DataFrame({"AIR": AIR, "ES_overnight": ESov, "EU_post15": EUpost_b, "own_gap": d.gap})
    for cols in [["AIR"], ["AIR", "ES_overnight", "own_gap"], ["AIR", "EU_post15"], ["EU_post15"]]:
        r, n = ols_nw(y, M[cols])
        print(st, cols, " | ".join(f"{c} {r.loc[c,'coef']:.3f} (t {r.loc[c,'t']:.2f})" for c in cols), "n", n)
