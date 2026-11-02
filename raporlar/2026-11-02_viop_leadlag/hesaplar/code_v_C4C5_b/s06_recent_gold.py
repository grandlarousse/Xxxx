"""s06: 2024-09+ temiz HK/SSE sinyali (06:30 UTC anlık) -> TRALT gün-içi: ortak faktör (altın), trend/drift ve yön ayrımı.
 - GC=F saatlik (2024-06+): gece altını GC(06:30)/GC(15:00 t-1) ve Asya seansı altını GC(06:30)/GC(01:30).
 - Sinyalin GC'nin BIST seansı getirisini (07:00->15:00) tahmin edip etmediği (altının kendi momentumu mu?).
 - Uzun-yalnız benchmark, long/short bacak ayrımı, ortalamadan arındırılmış sinyal.
 - TRALT h1 (2025-11+): açılış->07:30 ve 07:30->kapanış ayrımı."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
tr = bist_dec("TRALT.IS"); y = tr.intra; xu = bist_dec("XU100.IS")
def h1(sym):
    h = raw(sym, "h1").copy(); h["end"] = h.index + pd.Timedelta(minutes=60); return h
def snap_utc(sym, hhmm, date_index):
    """UTC günü (BIST günü) için hhmm UTC'ye kadar kapanan son bar kapanışı (24 saat işlem gören GC için)."""
    h = h1(sym); hh, mm = map(int, hhmm.split(":"))
    out = {}
    ends = h["end"].values; cl = h["c"].values
    for d in date_index:
        lim = np.datetime64((pd.Timestamp(d).tz_localize("UTC") + pd.Timedelta(hours=hh, minutes=mm)).tz_localize(None))
        i = np.searchsorted(ends.astype("datetime64[ns]"), lim, side="right") - 1
        out[d] = cl[i] if i >= 0 and (lim - ends[i].astype("datetime64[ns]")) < np.timedelta64(3, "h") else np.nan
    return pd.Series(out)
def snap_loc(sym, hhmm):
    h = raw(sym, "h1").copy(); h["ld"] = pd.to_datetime(h["ldate"]); h["end"] = h.index + pd.Timedelta(minutes=60)
    hh, mm = map(int, hhmm.split(":")); lim = h.index.normalize() + pd.Timedelta(hours=hh, minutes=mm)
    return h[h["end"] <= lim].groupby("ld")["c"].last()
ST = "2024-09-01"
idx = y.index[y.index >= ST]
gc_tm1_1500 = snap_utc("GC=F", "15:00", idx - pd.Timedelta(days=0))  # aynı gün 15:00
gcs = pd.DataFrame({"g1500": gc_tm1_1500, "g0630": snap_utc("GC=F", "06:30", idx), "g0130": snap_utc("GC=F", "01:30", idx), "g0700": snap_utc("GC=F", "07:00", idx)})
cal = y.index
prev = pd.Series(cal[:-1], index=cal[1:])
gcs["g1500_prev"] = gcs["g1500"].reindex(prev.reindex(idx).values).values
GC_night = np.log(gcs.g0630 / gcs.g1500_prev)          # BIST t-1 kapanışı -> 06:30 t (açılış öncesi biliniyor)
GC_asia = np.log(gcs.g0630 / gcs.g0130)                 # Asya seansı altın
GC_day = np.log(gcs.g1500 / gcs.g0700)                  # BIST seansı altın (eşzamanlı, işlenemez)
sig = {}
for s in ["2899.HK", "1787.HK", "600547.SS"]:
    p = snap_loc(s, "06:30"); pc = daily_local(s)["c"].shift(1)
    sig[s] = to_bist(np.log(p / pc.reindex(p.index)), "zero").reindex(idx)
    po = daily_local(s)["o"]; sig[s + "_asia"] = to_bist(np.log(p / po.reindex(p.index)), "zero").reindex(idx)  # 01:30->06:30
df = pd.DataFrame({"y": y.reindex(idx), "gap": tr.gap.reindex(idx), "GCn": GC_night, "GCa": GC_asia, "GCd": GC_day, "xu": xu.intra.reindex(idx), **sig})
print("n", df.dropna().shape[0])
print("== Basit korelasyonlar (NW t) hedef TRALT intra ==")
for c in ["GCn", "GCa", "2899.HK", "1787.HK", "600547.SS", "2899.HK_asia", "1787.HK_asia", "600547.SS_asia"]:
    b, t, n = nw_t(df.y, df[c]); print(f"  {c:14s} r={b:+.3f} t={t:+.2f} n={n}")
print("  [eşzamanlı] GCd r={:+.3f} t={:+.2f}".format(*nw_t(df.y, df.GCd)[:2]))
print("== Sinyal -> GC BIST-seansı getirisi (altının kendi öncülüğü?) ==")
for c in ["2899.HK", "1787.HK", "600547.SS", "GCn", "GCa"]:
    b, t, n = nw_t(df.GCd, df[c]); print(f"  {c:10s} -> GC 07-15: r={b:+.3f} t={t:+.2f}")
print("== Çoklu regresyon ==")
for cols in [["2899.HK", "GCn"], ["2899.HK", "GCn", "gap"], ["2899.HK", "GCn", "gap", "GCd"], ["1787.HK", "GCn", "gap", "GCd"], ["600547.SS", "GCn", "gap", "GCd"], ["2899.HK", "1787.HK", "600547.SS"]]:
    r, n = ols_nw(df.y, df[cols]); print(f"  n={n} " + " | ".join(f"{i}: {v.b:+.3f} (t {v.t:+.2f})" for i, v in r.iterrows()))
print("== Trend/drift: uzun-yalnız TRALT gün-içi, sinyal pozitif oranı, bacaklar ==")
print(f"  TRALT gün-içi ort (2024-09+): {1e4*df.y.mean():+.1f} bps/gün, t {nw_t(df.y.dropna().values)[1]:+.2f}")
for c in ["2899.HK", "1787.HK", "600547.SS"]:
    d = df[[c, "y"]].dropna(); d = d[d[c] != 0]
    L = d.y[d[c] > 0]; Sx = -d.y[d[c] < 0]
    dm = d[c] - d[c].expanding(60).mean().shift(1)
    r_dm, _, _ = bt(dm, d.y, 10)
    print(f"  {c:10s} pozitif oran {(d[c]>0).mean():.2f} | LONG bacak brüt {1e4*L.mean():+.1f} bps (n {len(L)}) | SHORT bacak brüt {1e4*Sx.mean():+.1f} bps (n {len(Sx)}) | genişleyen-ortalamadan arındırılmış sinyal net10: {r_dm['ALL'].get('bps', np.nan):+.1f} (t {r_dm['ALL'].get('t', np.nan):+.2f})")
# yarıyıllık istikrar
print("== Altı aylık dilimler (2899 06:30 -> TRALT intra) ==")
d = df[["2899.HK", "y"]].dropna()
for k, g in d.groupby(d.index.to_period("Q").astype(str).str[:4] + np.where(d.index.month <= 6, "H1", "H2")):
    print(f"  {k}: r={g['2899.HK'].corr(g.y):+.3f} n={len(g)}")
# TRALT h1: açılış->07:30 vs 07:30->kapanış
h = raw("TRALT.IS", "h1").copy(); h["ld"] = pd.to_datetime(h["ldate"]); h["hm"] = h.index.strftime("%H:%M")
f = h[h.hm == "06:30"].set_index("ld"); dd = daily_local("TRALT.IS")
A = np.log(f["c"] / dd["o"].reindex(f.index)); B = np.log(dd["c"].reindex(f.index) / f["c"])
for c in ["2899.HK", "1787.HK", "600547.SS", "GCn"]:
    s_ = df[c]
    b1, t1, n1 = nw_t(A, s_); b2, t2, n2 = nw_t(B, s_)
    r2, _, _ = bt(s_, B, 10)
    print(f"  TRALT h1 (2025-11+): {c:10s} -> açılış->07:30 r={b1:+.3f} t={t1:+.2f} | 07:30->kapanış r={b2:+.3f} t={t2:+.2f} n={n2} net10(07:30 giriş) {r2['ALL'].get('bps', np.nan):+.1f}")
