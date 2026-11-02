"""s10: VİOP pay vadelisi (09:30 TSİ = 06:30 UTC açılış) üzerinde, likit dönemde (2021+) ve 06:30 UTC'de BİLİNEN sinyallerle test.
Vadeli açılışı 06:30 UTC'de => SSE/SHFE kapanışı (07:00) 30 dk, HK kapanışı 100 dk örtüşür. Temiz sinyal: 06:30 anlık fiyat (h1) veya önceki gün."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
exec(open(sys.path[0] + "/s09_viop_test.py").read().split("OUT = []")[0])  # active() tanımı
def snap_loc(sym, hhmm):
    h = raw(sym, "h1").copy(); h["ld"] = pd.to_datetime(h["ldate"]); h["end"] = h.index + pd.Timedelta(minutes=60)
    hh, mm = map(int, hhmm.split(":")); lim = h.index.normalize() + pd.Timedelta(hours=hh, minutes=mm)
    return h[h["end"] <= lim].groupby("ld")["c"].last()
def preopen(sym, hhmm="06:30"):
    p = snap_loc(sym, hhmm); pc = daily_local(sym)["c"].shift(1); return to_bist(np.log(p / pc.reindex(p.index)), "zero")
# SHFE HC 60m (Sina, v_C4C5_a'nın indirdiği ham dosyalar; kendi ayrıştırmam): 14:15 Pekin (06:15 UTC) anlık / önceki gün 15:00
import json, glob
def sina60(prod):
    fr = []
    for f in sorted(glob.glob(S + f"/dl_v_C4C5a/sina60/{prod}*.txt")):
        t = open(f).read()
        try: j = json.loads(t[t.index("(") + 1:t.rindex(")")])
        except Exception: continue
        d = pd.DataFrame(j); d["d"] = pd.to_datetime(d["d"]); d["c"] = pd.to_numeric(d["c"]); d["ctr"] = os.path.basename(f)[:-4]; fr.append(d)
    return pd.concat(fr)
H = sina60("HC"); R = sina_roll("HC")
H["hm"] = H.d.dt.strftime("%H:%M"); H["day"] = H.d.dt.normalize()
piv = H.pivot_table(index=["ctr", "day"], columns="hm", values="c", aggfunc="last")
rows = []
for d, ctr in R["ctr"].items():
    if (ctr, d) in piv.index:
        x = piv.loc[(ctr, d)]
        # önceki işlem günü aynı kontrat 15:00 kapanışı
        prev = [k for k in piv.loc[ctr].index if k < d]
        if not prev: continue
        p0 = piv.loc[(ctr, prev[-1])].get("15:00", np.nan)
        rows.append(dict(d=d, pre0615=np.log(x.get("14:15", np.nan) / p0), full=np.log(x.get("15:00", np.nan) / p0)))
HC60 = pd.DataFrame(rows).set_index("d")
print("HC 60dk kapsama:", HC60.dropna().index.min(), HC60.dropna().index.max(), len(HC60.dropna()))
for und, sigs in [("TRALT", {"600547 cc(07:00)": to_bist(loc_ret("600547.SS", "adj"), "zero"), "600547 P06:30": preopen("600547.SS"), "2899 P06:30": preopen("2899.HK"), "1787 P06:30": preopen("1787.HK"), "1787 cc(08:10)": to_bist(loc_ret("1787.HK", "adj"), "zero")}),
                  ("KRDMD", {"HC cc(07:00)": to_bist(R["cc"], "zero"), "HC 60dk full": to_bist(HC60["full"], "zero"), "HC P06:15": to_bist(HC60["pre0615"], "zero"), "HC gapD (13:00 t-1)": to_bist(R["gapD"], "zero")})]:
    a = active(und); sp = bist_dec(und + ".IS")
    for st in ["2021-01-01", "2023-11-01", "2024-09-01"]:
        aa = a[a.index >= st]
        for nm, s in sigs.items():
            s = s.reindex(aa.index)
            if s.notna().sum() < 100 or (s.fillna(0) != 0).sum() < 100: continue
            b, t, n = nw_t(aa.fint, s); bs, ts, _ = nw_t(sp.intra.reindex(aa.index), s)
            r10, _, _ = bt(s, aa.fint, 10); r15, _, _ = bt(s, aa.fint, 15)
            print(f"{und} {st[:7]}+ {nm:20s} VİOP r={b:+.3f} t={t:+.2f} n={n} | spot r={bs:+.3f} t={ts:+.2f} | VİOP net10 {r10['ALL'].get('bps',np.nan):+.1f} (t {r10['ALL'].get('t',np.nan):+.2f}, Sh {r10['ALL'].get('sh',np.nan):.2f}) net15 {r15['ALL'].get('bps',np.nan):+.1f}")
