"""sinyal_tuprs.compute() ile araştırma z'sinin (cl_t.signal_z, VİOP takvimi) karşılaştırması — yerel parquet verisiyle."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np, pandas as pd, cl_t as cl, sinyal_tuprs as st
def load(sym):
    d = cl.dly(sym) if not sym.endswith(".IS") else cl.dly(sym)
    return d[["c", "adj"]]
data = {s: load(s) for s in st.MEM + [st.MKT, "TUPRS.IS"]}
now = pd.Timestamp("2026-11-04 08:53", tz="UTC")
zr, Pb, P, df = cl.signal_z()
res = []
for tgt in [pd.Timestamp("2026-11-04")]:
    R = st.compute(data, tgt, now)
    z = R["z"]; j = zr.reindex(z.index); m = z.notna() & j.notna() & (z.index >= "2024-01-01")
    print("hedef", tgt.date(), "ortak gün (2024+)", int(m.sum()), "maks |fark|", float((z[m] - j[m]).abs().max()))
    print("işaret/eşik uyumu (|z|>1):", float(((z[m].abs() > 1) == (j[m].abs() > 1)).mean()))
    only = z.index[(z.index >= "2024-01-01") & (z.notna() != j.notna())]; print("yalnız birinde dolu gün:", [str(d.date()) for d in only][:20])
    print(z.tail(6).round(3).to_string()); print("araştırma:", zr.tail(5).round(3).to_dict())
    pos, left, ent, ev = st.state_machine(z.iloc[:-1]); print("durum", pos, left, ent, ev[-3:])
