"""s11: VİOP vadeli açılışı (06:30 UTC) bayat mı? Vadeli gün-içi fazlası (fint - sint) sinyalle tahmin ediliyor mu?
Ayrıca daha erken HK anlık fiyatları (04:00, 05:30) ve gece altını (GC 15:00 t-1 -> 06:30 t) ile kontrol."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
exec(open(sys.path[0] + "/s09_viop_test.py").read().split("OUT = []")[0])
exec(open(sys.path[0] + "/s10_viop_clean.py").read().split("# SHFE HC 60m")[0].split("exec(")[0])
def snap_loc(sym, hhmm):
    h = raw(sym, "h1").copy(); h["ld"] = pd.to_datetime(h["ldate"]); h["end"] = h.index + pd.Timedelta(minutes=60)
    hh, mm = map(int, hhmm.split(":")); lim = h.index.normalize() + pd.Timedelta(hours=hh, minutes=mm)
    return h[h["end"] <= lim].groupby("ld")["c"].last()
def preopen(sym, hhmm="06:30"):
    p = snap_loc(sym, hhmm); pc = daily_local(sym)["c"].shift(1); return to_bist(np.log(p / pc.reindex(p.index)), "zero")
a = active("TRALT"); sp = bist_dec("TRALT.IS"); a = a[a.index >= "2024-09-01"]
# vadeli 'gap': önceki gün vadeli kapanışından vadeli açılışa (aynı kontrat varsayımı yaklaşık; roll günleri hariç)
same = a.ser == a.ser.shift(1)
fgap = np.log(a.o / a.c.shift(1)).where(same)
df = pd.DataFrame({"fint": a.fint, "sint": sp.intra.reindex(a.index), "sgap": sp.gap.reindex(a.index), "fgap": fgap})
df["excess"] = df.fint - df.sint
# GC gece (s06 mantığı)
h = raw("GC=F", "h1").copy(); h["end"] = h.index + pd.Timedelta(minutes=60)
ends = h["end"].dt.tz_localize(None).values if hasattr(h["end"], "dt") else h["end"].values
def gsnap(d, hh, mm):
    lim = np.datetime64(pd.Timestamp(d) + pd.Timedelta(hours=hh, minutes=mm)); i = np.searchsorted(ends, lim, side="right") - 1
    return h["c"].values[i] if i >= 0 else np.nan
cal = df.index; prevd = pd.Series(cal[:-1], index=cal[1:]).reindex(cal)
g0630 = pd.Series([gsnap(d, 6, 30) for d in cal], index=cal); g1500p = pd.Series([gsnap(p, 15, 0) if pd.notna(p) else np.nan for p in prevd], index=cal)
df["GCn"] = np.log(g0630 / g1500p)
for hm in ["04:00", "05:30", "06:30"]:
    df[f"2899_{hm}"] = preopen("2899.HK", hm).reindex(cal); df[f"1787_{hm}"] = preopen("1787.HK", hm).reindex(cal)
df["600547_0630"] = preopen("600547.SS", "06:30").reindex(cal)
print("n", len(df.dropna()))
print("vadeli gap ile spot gap korelasyonu:", round(df.fgap.corr(df.sgap), 3), "| fint ort", round(1e4*df.fint.mean(), 1), "sint ort", round(1e4*df.sint.mean(), 1))
print("\nsinyal | -> VİOP fint | -> spot sint | -> fazla (fint-sint) | -> spot gap | -> vadeli gap")
for c in ["GCn", "2899_04:00", "2899_05:30", "2899_06:30", "1787_04:00", "1787_05:30", "1787_06:30", "600547_0630"]:
    o = [nw_t(df[k], df[c]) for k in ["fint", "sint", "excess", "sgap", "fgap"]]
    print(f"{c:12s} " + " | ".join(f"r={b:+.3f} t={t:+.2f}" for b, t, n in o))
r, n = ols_nw(df.fint, df[["2899_06:30", "GCn"]]); print("\nVİOP fint ~ 2899 + GCn:", r.round(3).to_dict())
r, n = ols_nw(df.fint, df[["2899_06:30", "GCn", "fgap"]]); print("VİOP fint ~ 2899 + GCn + vadeli gap:", r.round(3).to_dict())
for c in ["2899_04:00", "2899_05:30", "2899_06:30", "GCn"]:
    r10, _, _ = bt(df[c], df.fint, 10); r15, _, _ = bt(df[c], df.fint, 15)
    print(f"BT {c}: VİOP net10 {r10['ALL'].get('bps'):+.1f} (t {r10['ALL'].get('t'):+.2f}, Sh {r10['ALL'].get('sh'):.2f}) net15 {r15['ALL'].get('bps'):+.1f}")
# yarıyıllar ve uç değer, 2899 06:30 -> VİOP
d = df[["2899_06:30", "fint"]].dropna()
print("yarıyıllar r:", {k: round(g["2899_06:30"].corr(g.fint), 3) for k, g in d.groupby(d.index.year.astype(str) + np.where(d.index.month <= 6, "H1", "H2"))})
from scipy.stats import spearmanr
print("Spearman", round(spearmanr(d["2899_06:30"], d.fint)[0], 3), "| Eyl-Eki 2026 hariç r", round(d[d.index < "2026-09-01"].corr().iloc[0, 1], 3), "t", round(nw_t(d.fint[d.index < "2026-09-01"], d["2899_06:30"][d.index < "2026-09-01"])[1], 2))
r10, pnl, pos = bt(d["2899_06:30"], d.fint, 10); a_ = pnl[pos != 0].sort_values(ascending=False)
print("en iyi 10 işlem atılınca net10:", round(1e4 * a_.iloc[10:].mean(), 1), "| en iyi 10:", [(str(i.date()), round(1e4*v)) for i, v in a_.head(10).items()])
