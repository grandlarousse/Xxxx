"""v_A4_a / v0: Ham parquet'ten zamanlama doğrulaması (ll.py import EDİLMEZ).
1) Sürücü günlük kapanışı (c) == aynı ldate'in son saatlik barının kapanışı mı? (kapanış anını kanıtlar)
2) BIST günlük açılış (o) == saatlik ilk bar (06:30 UTC) açılışı mı? == 5dk açılış müzayedesi barı mı?
3) BIST günlük kapanış (c) == saatlik 15:00 kapanış seansı barı mı?
4) o == önceki c oranı (bayat açılış şüphesi) yıllara göre."""
import pandas as pd, numpy as np, sys
S = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad"
def rd(kind, s):
    d = pd.read_parquet(f"{S}/data/{kind}/{s}.parquet"); return d
out = []
for s in ["DAL", "UAL", "AAL", "TUR", "^GSPC", "LHA.DE", "AF.PA", "IAG.L", "^STOXX"]:
    d = rd("daily", s); h = rd("h1", s)
    d = d.set_index("ldate")
    h["end"] = h.index + pd.Timedelta(hours=1)
    last = h.groupby("ldate").agg(c=("c", "last"), end=("end", "max"))
    j = d[["c"]].join(last, rsuffix="_h", how="inner")
    rel = (j["c_h"] / j["c"] - 1).abs()
    out.append((s, len(j), float((rel < 1e-3).mean()), float(rel.median()), j["end"].dt.strftime("%H:%M").value_counts().head(3).to_dict()))
print("SÜRÜCÜ: (sym, n, |c_h1/c_d-1|<10bp oranı, medyan fark, son bar bitiş saatleri UTC)")
for o in out: print(o)
print()
for s in ["THYAO.IS", "PGSUS.IS", "TAVHL.IS", "XU100.IS"]:
    d = rd("daily", s).set_index("ldate"); h = rd("h1", s)
    h["hm"] = h.index.strftime("%H:%M")
    fb = h[h.hm == "06:30"].groupby("ldate").agg(o1=("o", "first"), c1=("c", "first"))
    cb = h[h.hm == "15:00"].groupby("ldate").agg(c15=("c", "last"))
    j = d[["o", "c"]].join(fb, how="inner").join(cb, how="left")
    r_o = (j.o1 / j.o - 1).abs(); r_c = (j.c15 / j.c - 1).abs()
    print(s, "n", len(j), "daily_o==h1_06:30_open (<5bp):", round(float((r_o < 5e-4).mean()), 3), "medyan", float(r_o.median()),
          "| daily_c==h1_15:00 close (<5bp):", round(float((r_c < 5e-4).mean()), 3), "n15", int(j.c15.notna().sum()))
    try:
        m = rd("m5", s); m["hm"] = m.index.strftime("%H:%M")
        fm = m.groupby("ldate").apply(lambda g: pd.Series({"first_hm": g.hm.iloc[0], "o5": g.o.iloc[0], "v5": g.v.iloc[0]}))
        jj = d[["o"]].join(fm, how="inner")
        print("   m5: ilk bar saatleri", jj.first_hm.value_counts().to_dict(), "daily_o==m5 ilk bar open (<5bp):", round(float(((jj.o5.astype(float) / jj.o - 1).abs() < 5e-4).mean()), 3), "n", len(jj))
    except Exception as e:
        print("  m5 yok", e)
    dd = rd("daily", s).set_index("ldate"); dd = dd[dd.v.fillna(0) > 0] if s != "XU100.IS" else dd
    eq = (dd.o == dd.c.shift(1)); flat = (dd.h == dd.l)
    yr = pd.DataFrame({"o_eq_prevc": eq, "o_eq_prevc_and_h_eq_l": eq & flat, "o_eq_h_or_l": (dd.o == dd.h) | (dd.o == dd.l)}).groupby(dd.index.year).mean().round(3)
    print(yr.loc[2012:].T.to_string())
