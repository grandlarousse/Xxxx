import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_E3_b")
"""10: Mekanizma — VLO (ve XLE) t-1 getirisini (i) önceki ABD kapanışı -> 14:30 UTC t-1 (BIST seansı içinde bilinen) ve
(ii) 14:30 UTC t-1 -> ABD kapanışı t-1 (BIST kapanışından sonra) olarak böl. Hedef: TUPRS hedge'li gap_t ve gün-içi_t."""
import vb, numpy as np, pandas as pd
F = pd.read_parquet(vb.RES + "/F.parquet")
cal = F.index
out = []
for sym in ["VLO", "XLE"]:
    h = vb.raw(sym, "h1").copy(); h.index = pd.DatetimeIndex(h.index).tz_convert("UTC")
    h["d"] = h.index.tz_localize(None).normalize(); h["hm"] = h.index.strftime("%H:%M")
    a = h[h.hm == "13:30"]; pa = pd.Series(a.c.values, index=a.d.values)       # 14:30 UTC kapanış (yaz)
    b = h[h.hm == "14:30"]; pb = pd.Series(b.o.values, index=b.d.values)       # 14:30 UTC açılış (kış)
    p1430 = pa.combine_first(pb)
    d = vb.raw(sym); c = d.c.astype(float)
    df = pd.DataFrame({"c": c, "p": p1430.reindex(c.index)}); df["pc"] = df.c.shift(1)
    df["i"] = np.log(df.p / df.pc); df["ii"] = np.log(df.c / df.p)
    df = df.dropna()
    # BIST günü t için: ABD günü = t'den önceki son ABD günü (strict) ve bu gün BIST t-1 ile aynı tarih olmalı (tatil kayması yok)
    idx = np.searchsorted(df.index.values, cal.values, side="left") - 1
    ok = idx >= 0
    us_day = pd.Series(pd.NaT, index=cal); us_day[ok] = df.index.values[idx[ok]]
    prev_bist = pd.Series(cal, index=cal).shift(1)
    same = us_day == prev_bist
    X = pd.DataFrame({"i": np.where(ok, df.i.values[np.clip(idx, 0, None)], np.nan), "ii": np.where(ok, df.ii.values[np.clip(idx, 0, None)], np.nan)}, index=cal)
    X[~same.values] = np.nan
    G = F.join(X, how="left"); G = G[G.index >= "2023-12-05"].dropna(subset=["i", "ii", "y_h"])
    for tgt, nm in [("y_h", "hedge'li gün-içi"), ("y_raw", "ham gün-içi"), ("tu_gap", "ham gap")]:
        yy = G[tgt] if tgt != "tu_gap" else G.tu_gap
        p, t, n = vb.nw(yy, G[["i", "ii"]])
        out.append(dict(sym=sym, hedef=nm, b_i=p["i"], t_i=t["i"], b_ii=p["ii"], t_ii=t["ii"], n=n))
    G["hg"] = G.tu_gap - G.xu_gap
    p, t, n = vb.nw(G.hg, G[["i", "ii"]]); out.append(dict(sym=sym, hedef="hedge'li gap", b_i=p["i"], t_i=t["i"], b_ii=p["ii"], t_ii=t["ii"], n=n))
    print(sym, "örneklem", G.index.min().date(), G.index.max().date(), "sd(i)", round(G.i.std(), 4), "sd(ii)", round(G.ii.std(), 4))
print(pd.DataFrame(out).round(3).to_string())
