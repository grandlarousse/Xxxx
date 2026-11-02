"""s2: İş Yatırım saatlik (2015–2026) ile spot gün-içinin saat saat ayrıştırılması -> açılış müzayedesi artefaktı testi
(2023 öncesi için h1 Yahoo verisi yok; İş Yatırım saatlik serisi bunu 2015'e kadar uzatıyor)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_b")
import numpy as np, pandas as pd, bc
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
L = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)


def build(code, ysym):
    x = bc.isy_h1(code)
    # değer zamanı = etiket + 1 saat (UTC) -> İstanbul yerel saati
    vt = (x.index + pd.Timedelta(hours=1)).tz_localize("UTC").tz_convert("Europe/Istanbul")
    df = pd.DataFrame({"px": x.values, "day": vt.tz_localize(None).normalize(), "hh": vt.hour + vt.minute / 60.0})
    d = bc.decomp(ysym, start="2015-01-01")
    piv = df.pivot_table(index="day", columns="hh", values="px", aggfunc="last")
    first = df.groupby("day").px.first(); last = df.groupby("day").px.last()
    first_h = df.groupby("day").hh.first()
    out = pd.DataFrame(index=d.index)
    out["o"] = d.o; out["c"] = d.c; out["intra"] = d.intra; out["gap"] = d.gap
    out["first"] = first.reindex(out.index); out["first_h"] = first_h.reindex(out.index)
    out["last"] = last.reindex(out.index)
    for h in range(10, 19):
        if h in piv.columns:
            out[f"p{h}"] = piv[h].reindex(out.index)
    out["close_match"] = np.abs(np.log(out["last"] / out.c)) < 2e-4
    out["s_o_first"] = np.log(out["first"] / out.o)           # açılış -> ilk saatlik değer (2017+: 11:00)
    out["s_first_c"] = np.log(out.c / out["first"])           # ilk saatlik -> kapanış
    if "p18" in out:
        out["s_18_c"] = np.log(out.c / out["p18"])              # sürekli seans sonu (18:00) -> kapanış müzayedesi
        out["s_first_18"] = np.log(out["p18"] / out["first"])
    if "p12" in out:
        out["s_o_12"] = np.log(out["p12"] / out.o); out["s_12_c"] = np.log(out.c / out["p12"])
    ok = out.intra.notna() & out.close_match & out["first"].notna()
    return out[ok]


for code, ysym in [("XU030", "XU030.IS"), ("XU100", "XU100.IS")]:
    o = build(code, ysym)
    P(f"\n===== {code}: n={len(o)}  (kapanış eşleşmesi zorunlu); ilk saatlik değer yerel saat dağılımı: {o.first_h.value_counts().head(4).to_dict()}")
    cols = ["intra", "s_o_first", "s_first_c", "s_first_18", "s_18_c"]
    yt = bc.by_year(o, cols)
    P(yt[[c for c in yt.columns if not c.endswith('_t')] + [c + '_t' for c in cols]].round(2).to_string())
    for nm, a, b in [("2015-2026", "2015", "2026"), ("2015-2016", "2015", "2016"), ("2017-2022", "2017", "2022"), ("2017-03..2023", "2017-03-06", "2023"),
                     ("2021-2022", "2021", "2022"), ("2023-2026", "2023", "2026"), ("2024-2026", "2024", "2026")]:
        x = o.loc[a:b]
        P(f"{nm:14s} aç-sat {bc.st(-x.intra)['mean']:6.2f} (t {bc.st(-x.intra)['t']:.2f}) | -[açılış->ilk saat] {bc.st(-x.s_o_first)['mean']:6.2f} (t {bc.st(-x.s_o_first)['t']:.2f})"
          f" | -[ilk saat->kapanış] {bc.st(-x.s_first_c)['mean']:6.2f} (t {bc.st(-x.s_first_c)['t']:.2f}) | -[ilk->18:00] {bc.st(-x.s_first_18)['mean']:6.2f} (t {bc.st(-x.s_first_18)['t']:.2f})"
          f" | -[18:00->kapanış] {bc.st(-x.s_18_c)['mean']:6.2f} (t {bc.st(-x.s_18_c)['t']:.2f})")
    # saat saat (2017+ ızgara: 11..18)
    hrs = [h for h in range(11, 19) if f"p{h}" in o]
    seg = {}
    seg["o->11"] = np.log(o["p11"] / o.o) if "p11" in o else None
    for a, b in zip(hrs[:-1], hrs[1:]):
        seg[f"{a}->{b}"] = np.log(o[f"p{b}"] / o[f"p{a}"])
    seg["18->c"] = np.log(o.c / o["p18"])
    sg = pd.DataFrame(seg)
    for nm, a, b in [("2017-2022", "2017", "2022"), ("2023-2026", "2023", "2026")]:
        x = sg.loc[a:b]
        P(f"saat segmentleri {nm} (bps, t): " + "; ".join(f"{c} {bc.st(x[c])['mean']:.1f} ({bc.st(x[c])['t']:.1f})" for c in sg.columns))
    o.to_parquet(f"{bc.RES}/s2_{code}.parquet"); yt.to_csv(f"{bc.RES}/s2_years_{code}.csv")

# 47 hisse: açılış->ilk saat vs ilk saat->kapanış
rows = []
for s in bc.STOCKS:
    try:
        o = build(s, s + ".IS")
    except Exception as e:
        P(s, "hata", e); continue
    for nm, a, b in [("2015-2022", "2015", "2022"), ("2023-2026", "2023", "2026")]:
        x = o.loc[a:b]
        if len(x) < 100: continue
        rows.append(dict(stock=s, per=nm, n=len(x), intra=bc.st(x.intra)["mean"], o_first=bc.st(x.s_o_first)["mean"],
                         o_first_t=bc.st(x.s_o_first)["t"], first_c=bc.st(x.s_first_c)["mean"], first_c_t=bc.st(x.s_first_c)["t"]))
R = pd.DataFrame(rows); R.to_csv(f"{bc.RES}/s2_stocks.csv", index=False)
for nm, g in R.groupby("per"):
    P(f"\n47 hisse {nm}: hisse sayısı {len(g)}; medyan intra {g.intra.median():.1f}; medyan açılış->ilk saat {g.o_first.median():.1f} "
      f"(negatif {int((g.o_first<0).sum())}, t<-2 {int((g.o_first_t<-2).sum())}); medyan ilk saat->kapanış {g.first_c.median():.1f} "
      f"(negatif {int((g.first_c<0).sum())}, t<-2 {int((g.first_c_t<-2).sum())})")
open(f"{bc.RES}/s2_isy.log", "w").write("\n".join(L))
