"""s02: Yahoo BIST günlük açılışı gerçek açılış müzayedesi fiyatı mı? (h1 06:30 barı açılışı, m5 06:55 barı ile karşılaştırma)
+ bayat açılış göstergeleri 2014–2026 (o == önceki c oranı)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_C4C5_b")
from vb import *
for sym in ["TRALT.IS", "KRDMD.IS", "EREGL.IS", "XU100.IS"]:
    d = daily_local(sym)
    h = raw(sym, "h1").copy(); h["ld"] = pd.to_datetime(h["ldate"]); h["hm"] = h.index.strftime("%H:%M")
    f = h[h.hm == "06:30"].set_index("ld")
    j = pd.concat([d["o"].rename("od"), f["o"].rename("oh"), d["c"].shift(1).rename("pc"), f["c"].rename("c0730")], axis=1).dropna()
    rel = np.log(j.od / j.oh)
    print(f"{sym}: h1 ortak gün {len(j)}; |od/oh-1|<1bp oranı {(rel.abs() < 1e-4).mean():.3f}; medyan |fark| {1e4*rel.abs().median():.1f}bps; o==önceki c oranı {(np.abs(np.log(j.od/j.pc))<1e-5).mean():.3f}")
    try:
        m = raw(sym, "m5").copy(); m["ld"] = pd.to_datetime(m["ldate"]); m["hm"] = m.index.strftime("%H:%M")
        f5 = m[m.hm == "06:55"].set_index("ld"); f7 = m[m.hm == "07:00"].set_index("ld")
        j5 = pd.concat([d["o"].rename("od"), f5["o"].rename("o655"), f5["c"].rename("c655"), f7["o"].rename("o700"), f7["c"].rename("c705"), f5["v"].rename("v655")], axis=1).dropna()
        print(f"   m5 ortak {len(j5)}: od==o655 {(np.abs(np.log(j5.od/j5.o655))<1e-4).mean():.2f}; od==c655 {(np.abs(np.log(j5.od/j5.c655))<1e-4).mean():.2f}; 06:55 barı h==l? ; medyan|od/c705| {1e4*np.abs(np.log(j5.od/j5.c705)).median():.1f}bps")
    except FileNotFoundError:
        pass
# uzun dönem bayat açılış: o == önceki c (h!=l olsa bile) oranı, yıllara göre
for sym in ["TRALT.IS", "KRDMD.IS"]:
    d = daily_local(sym); d = d[d.index >= "2014-01-01"]
    same = (np.abs(np.log(d.o / d.c.shift(1))) < 1e-6)
    oeqh = (d.o == d.h) | (d.o == d.l)
    print(sym, "o==önceki c oranı yıllara göre:", same.groupby(d.index.year).mean().round(3).to_dict())
    print(sym, "o==h veya o==l oranı:", oeqh.groupby(d.index.year).mean().round(2).to_dict())
