"""Görev 2: zamanlama / hizalama / NaN kontrolleri."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from ortak import *
from leadlag_sweep import build_panel   # yalnız karşılaştırma için

spy = px("SPY").index
X = leaders(spy)
R0, X0 = build_panel()
print("== 1) Benim öncü panelim vs build_panel: sütunlar ve max fark")
print("sütun farkı:", set(X.columns) ^ set(X0.columns))
for L in X.columns:
    a, b = X[L], X0[L].reindex(X.index)
    both = a.notna() & b.notna()
    print(f"{L:10s} max|fark|={np.nanmax(np.abs(a[both]-b[both])) if both.any() else np.nan:.2e}  NaN farkı={int((a.isna()!=b.isna()).sum())}")

print("\n== 2) Tarih hizalaması: öncü(t) ile referans ETF getirisi(t+lag) korelasyonu; en büyük |corr| lag=0'da olmalı")
def r(sym): return np.log(px(sym)["c"]).diff().reindex(spy)
ref = {"VIX_dlog": "SPY", "VIXTS_d": "SPY", "VVIX_dlog": "SPY", "OVX_dlog": "USO", "GVZ_dlog": "GLD",
       "BTC_16ET": "IBIT", "ETH_16ET": "ETHA", "DGS10_d": "IEF", "DGS2_d": "SHY", "DGS30_d": "TLT", "DFII10_d": "TIP", "T10YIE_d": "TIP", "TLT": "IEF"}
rows = []
for L, E in ref.items():
    y = r(E); x = X[L]
    cs = {lag: x.corr(y.shift(-lag)) for lag in (-2, -1, 0, 1, 2)}
    rows.append({"öncü": L, "ref": E, **{f"lag{k:+d}": round(v, 3) for k, v in cs.items()}})
print(pd.DataFrame(rows).to_string(index=False))

print("\n== 3) BTC saat seçimi: IBIT/BITO kapanış getirisi ile farklı ET saatlerinde başlayan mumun kapanışı arasındaki corr")
h = pd.read_parquet(os.path.join(DATA, "crypto", "BTC-USD_h1.parquet"))
idx = h.index.tz_convert("America/New_York")
for E in ("IBIT", "BITO"):
    y = r(E)
    out = {}
    for hr in (13, 14, 15, 16, 17):
        m = pd.Series(h["c"].values, index=idx); m = m[m.index.hour == hr]
        m.index = m.index.tz_localize(None).normalize(); m = m[~m.index.duplicated(keep="last")]
        x = np.log(m.reindex(spy)).diff()
        out[f"{hr}:00 başl."] = round(x.corr(y), 4)
    print(E, out)

print("\n== 4) VIX 16:15 sızıntısı: VIX_dlog(t) ile SPY t+1 gece boşluğu (açılış t+1 / kapanış t) korelasyonu")
s = px("SPY"); gap = np.log(s["o"] / s["c"].shift(1)).reindex(spy)
spyr = r("SPY")
for nm, x in (("VIX_dlog", X["VIX_dlog"]), ("VVIX_dlog", X["VVIX_dlog"]), ("VIXTS_d", X["VIXTS_d"]), ("SPY ret(t) [16:00]", spyr), ("TLT", X["TLT"])):
    print(f"  {nm:20s} corr(x_t, gap_t+1)={x.corr(gap.shift(-1)):+.3f}   corr(x_t, SPY ret_t+1)={x.corr(spyr.shift(-1)):+.3f}")
# VIX'in SPY'den bağımsız kısmı (16:00-16:15 bilgisi + gürültü): VIX_dlog - b*SPY
d = pd.DataFrame({"v": X["VIX_dlog"], "s": spyr, "g": gap.shift(-1)}).dropna()
b = np.polyfit(d.s, d.v, 1)[0]; e = d.v - b * d.s
print(f"  VIX kalıntısı (SPY'ye göre) ile ertesi gece boşluğu corr={e.corr(d.g):+.3f}  (n={len(d)})")

print("\n== 5) z-skoru NaN oranı (öncünün ilk geçerli gününden 80 gün sonrası itibarıyla, SPY takviminde)")
rows = []
for L in X.columns:
    x = X[L]; z = zsc(x)
    fv = x.first_valid_index()
    if fv is None: continue
    start = spy[min(spy.get_loc(fv) + 80, len(spy) - 1)]
    zz = z[z.index >= start]
    rows.append({"öncü": L, "başlangıç": str(start.date()), "gün": len(zz), "z_NaN_oranı": round(zz.isna().mean(), 3),
                 "z>=2": int((zz >= 2).sum()), "z<=-2": int((zz <= -2).sum())})
nn = pd.DataFrame(rows).sort_values("z_NaN_oranı", ascending=False)
print(nn.to_string(index=False))
nn.to_csv(os.path.join(HERE, "d2_z_nan.csv"), index=False)

print("\n== 6) Hazine tatilleri (Columbus/Veterans) NaN etkisi: min_periods=40 ile olay sayısı")
for L in ["DGS10_d", "DGS2_d", "DGS30_d", "DFII10_d", "T10YIE_d"]:
    x = X[L]; z1 = zsc(x); z2 = x / x.rolling(60, min_periods=40).std().shift(1)
    m = x.index >= "2017-03-01"
    print(f"  {L:9s} z<=-2: {int((z1[m] <= -2).sum())} -> {int((z2[m] <= -2).sum())} ; z>=2: {int((z1[m] >= 2).sum())} -> {int((z2[m] >= 2).sum())}")

print("\n== 7) TLT L_UP olay günleri örnek (TLT getirisi, z, SPY getirisi)")
z = zsc(X["TLT"]); ev = z[z >= 2].index
print(pd.DataFrame({"TLT_bp": (X["TLT"][ev] * 1e4).round(0), "z": z[ev].round(2), "SPY_bp": (spyr[ev] * 1e4).round(0)}).head(8).to_string())
print("TLT z>=2 günlerinde SPY getirisi: ortalama %.0f bp, medyan %.0f bp, SPY<0 oranı %.2f, SPY z<=-1 oranı %.2f" % (
    spyr[ev].mean() * 1e4, spyr[ev].median() * 1e4, (spyr[ev] < 0).mean(), (zsc(spyr)[ev] <= -1).mean()))

print("\n== 8) CSV kontrolleri")
res = pd.read_csv(os.path.join(ROOT, "sonuclar", "c0_leadlag.csv"))
print("max|brüt-net-maliyet|:", (res.gross_bp - res.net_bp - res.cost_bp).abs().max())
print("NaN t:", int(res.t.isna().sum()), " n<30:", int((res.n < 30).sum()))
print("min p1:", res.p1.min(), " BH %10 için 1. sıranın eşiği 0.1/m =", 0.1 / len(res), "  en iyi p ile geçebilecek en büyük aile m =", int(0.1 / res.p1.min()))
from scipy import stats as st
for thr in (2.0, 2.5, 3.0, 3.5):
    exp = (st.t.sf(thr, res.n - 1)).sum()
    print(f"  t>{thr}: gözlenen {int((res.t > thr).sum())}, bağımsız-null beklenen ~{exp:.0f};  t<-{thr}: {int((res.t < -thr).sum())}")
