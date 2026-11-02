"""s6: Plasebo / dış geçerlilik — aynı Yahoo 'o/c' ayrıştırması diğer ülke endekslerinde (2014–2026).
Desen (gap>0, gün-içi<0) her yerde varsa: ya küresel 'gece-gündüz' olgusu ya da Yahoo endeks açılışı artefaktı.
Açılışı bayat olan seriler (o==önceki c payı yüksek) ayrıca işaretlenir."""
import sys, glob, os; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_v_G3_b")
import numpy as np, pandas as pd, bc
L = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); L.append(s)
syms = ["^GSPC", "^IXIC", "^RUT", "^GDAXI", "^FTSE", "^FCHI", "^IBEX", "^AEX", "^SSMI", "^STOXX50E", "^OMX", "^ATX", "^BFX", "^N225", "^KS11", "^TWII",
        "^HSI", "^AXJO", "^NZ50", "^STI", "^BSESN", "^NSEI", "^JKSE", "^KLSE", "^SET.BK", "^BVSP", "^MXX", "^MERV", "^GSPTSE", "^J203.JO",
        "^TA125.TA", "^TASI.SR", "^CASE30", "^BUX.BD", "WIG20.WA", "XU030.IS", "XU100.IS"]
rows = []
for s in syms:
    p = f"{bc.D}/daily/{s}.parquet"
    if not os.path.exists(p): continue
    d = bc.decomp(s, start="2014-01-01")
    d = d[d.v.notna()]
    so = d.stale_open.mean()
    yi = d.intra.groupby(d.index.year).mean(); yg = d.gap.groupby(d.index.year).mean()
    st_i = bc.st(-d.intra); st_g = bc.st(d.gap)
    rows.append(dict(sym=s, n=st_i["n"], stale_open=so, gap=st_g["mean"], gap_t=st_g["t"], aqs=st_i["mean"], aqs_t=st_i["t"],
                     yrs_intra_neg=int((yi < 0).sum()), yrs=len(yi), yrs_gap_pos=int((yg > 0).sum()),
                     aqs_1420=bc.st(-d.intra.loc[:"2020"])["mean"], aqs_2126=bc.st(-d.intra.loc["2021":])["mean"]))
R = pd.DataFrame(rows).sort_values("aqs_t", ascending=False)
R.to_csv(f"{bc.RES}/s6_intl.csv", index=False)
P(R.round(2).to_string(index=False))
ok = R[(R.stale_open < 0.05) & ~R.sym.str.contains("XU")]
P(f"\nBayat-açılışsız {len(ok)} yabancı endeks: aç-sat t>2: {int((ok.aqs_t>2).sum())}, t<-2: {int((ok.aqs_t<-2).sum())}; medyan aç-sat {ok.aqs.median():.1f} bps; "
  f"gap>0 & gün-içi<0 (yıl çoğunluğu): {int(((ok.yrs_gap_pos>ok.yrs/2)&(ok.yrs_intra_neg>ok.yrs/2)).sum())}")
open(f"{bc.RES}/s6_intl.log", "w").write("\n".join(L))
