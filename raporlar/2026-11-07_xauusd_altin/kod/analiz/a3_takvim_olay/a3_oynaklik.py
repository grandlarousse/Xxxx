"""a3_takvim_olay — olay günlerinde oynaklık (yön değil): |getiri| olay/olmayan oranı. a3_analiz.py ve a3_derin.py'den SONRA çalıştır (registry'ye ekler)."""
import os, sys, json
O = os.path.dirname(os.path.abspath(__file__)); S = os.path.abspath(f"{O}/../.."); sys.path.insert(0, f"{S}/code")
from lib_altin import *
d = load_viop(); V = d.index; a = d.v_ret.abs()
def fg(dates, strict=False):
    p = np.searchsorted(V.values, pd.to_datetime(dates).values, side="right" if strict else "left"); return np.unique(p[p < len(V)])
fomc = pd.read_csv(f"{O}/events_fomc.csv", parse_dates=["date"]); fomc = fomc[fomc.scheduled]
ev = {"FOMC (F+1 getirisi)": fg(fomc.date, True), "CPI günü": fg(pd.read_csv(f"{O}/events_us_cpi.csv").date),
      "NFP günü": fg(pd.read_csv(f"{O}/events_us_nfp.csv").date)}
cx = pd.read_csv(f"{O}/events_comex.csv"); ev["OG vade günü"] = fg(cx.og_expiry)
for k, p in ev.items():
    D = pd.Series(0.0, index=V); D.iloc[p] = 1
    r = nw_ols(a * 1e4, D, lags=5)
    ratio = a[D == 1].mean() / a[D == 0].mean()
    o = dict(ic=ratio, t=r["t"], n=r["n"]); register("a3_takvim_olay", "oynaklik", f"VOL_{k.split()[0]}", f"|v_ret| {k} vs diğer", 1, o, note=json.dumps(dict(ratio=round(ratio, 2))))
    print(f"{k:<22} ort|r| olay {a[D==1].mean()*1e4:.0f} bps, diğer {a[D==0].mean()*1e4:.0f} bps, oran {ratio:.2f}, NW t {r['t']:.2f}, n_olay {int(D.sum())}")
print("registry:", len(pd.read_csv(f"{REG_DIR}/a3_takvim_olay.csv")))
