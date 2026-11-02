"""Ek: ES=F/BZ=F günlük kapanışının saatlik eşleşen saati; VİOP vadeli açılış fiyatının zamanı (spot açılış vs 10:30 ile karşılaştırma)."""
import numpy as np, pandas as pd
import vlib as V
out = []
def P(*a):
    s = " ".join(str(x) for x in a); out.append(s); print(s, flush=True)
for s in ["ES=F", "BZ=F", "VLO"]:
    h = V.raw(s, "h1"); d = V.by_ldate(s)
    hend = h.index + pd.Timedelta(minutes=60)
    hs = pd.Series(h.c.values, index=hend)
    res = {}
    for d0, c in d.c[d.index >= "2024-01-01"].items():
        day = hs[(hs.index >= pd.Timestamp(d0).tz_localize("UTC") + pd.Timedelta(hours=10)) & (hs.index <= pd.Timestamp(d0).tz_localize("UTC") + pd.Timedelta(hours=23))]
        if day.empty: continue
        m = day[(day / c - 1).abs() < 2e-4]
        if len(m): res[d0] = m.index[0].strftime("%H:%M")
    vc = pd.Series(res).value_counts()
    P(f"{s}: günlük c'nin eşleştiği ilk saatlik bar BİTİŞ saati (UTC), 2024+: {vc.head(6).to_dict()} | eşleşen gün={len(res)}")
F = pd.read_csv(V.RES + "/viop_tuprs_front.csv", index_col=0, parse_dates=True)
H = pd.read_parquet(V.RES + "/hourly_entries.parquet")
J = F.join(H[["o", "E1", "c", "r0", "r1"]], how="inner", rsuffix="_s")
J["basis_o"] = np.log(J.o / J.o_s); J["basis_E1"] = np.log(J.o / J.E1); J["basis_c"] = np.log(J.c / J.c_s)
P(f"VİOP x saatlik ortak gün={len(J)} | log(F_açılış/S_açılış) sd={1e4*J.basis_o.std():.1f} bps | log(F_açılış/S_10:30) sd={1e4*J.basis_E1.std():.1f} bps | log(F_kapanış/S_kapanış) sd={1e4*J.basis_c.std():.1f} bps")
P(f"corr(F o->c, S o->c)={J.r_fc.corr(J.r0):.3f} | corr(F o->c, S 10:30->c)={J.r_fc.corr(J.r1):.3f}")
P(f"ACILIS SEANSI fiyatı olan gün oranı={float(F.acs.notna().mean()):.2f}; medyan |F_açılış/ACS-1|={1e4*(F.o/F.acs-1).abs().median():.1f} bps")
open(V.RES + "/04_misc.txt", "w").write("\n".join(out))
