"""H4: mekanizma ayrıştırması.
 (1) Emsal sepet artığının kendi otokorelasyonu (küresel sektör momentumu): corr(X(t), X(t+1)).
 (2) Avrupa emsalleri: y_h(t) ~ z_EU(t) [öncül, t-1 seansı] + z_EU(t+1) [t seansı = BIST t ile eşzamanlı]. Öncül katsayı kalıyorsa -> BIST'e özgü gecikme.
 (3) ABD emsalleri: y_h(t) ~ z_AM(t) + z_AM(t+1) (örtüşme yalnız 13:30/14:30–15:00 UTC).
 (4) Saatlik zaman profili (2023-12+): her saatlik bar için hedge'li bar getirisi ~ z_res.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import vh
from peers import PEERS
L = lambda k: pd.read_parquet(vh.RES + f"/{k}.parquet").loc[vh.START:vh.END]
Y_h = L("Y_h"); Y_raw = L("Y_raw"); XU = L("XU")
STOCKS = list(PEERS.keys()); idx = Y_h.index
txt = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); txt.append(s)
Xr = {k: L(k) for k in ["X_res", "X_res_EU", "X_res_AM", "X_res_ASIA"]}
# (1) otokorelasyon (geleceğe kaydırmak için tam paneli kullan)
Lfull = lambda k: pd.read_parquet(vh.RES + f"/{k}.parquet")
P("== (1) Emsal sepet artığı otokorelasyonu corr(X_t, X_t+1) (hisse sepetleri ortalaması / medyan) ==")
for k in Xr:
    A = Lfull(k).loc["2013-06-01":]
    cs = [A[s].corr(A[s].shift(-1)) for s in STOCKS if A[s].notna().sum() > 500]
    P(f"  {k}: ort {np.nanmean(cs):.3f}, medyan {np.nanmedian(cs):.3f}, n={len(cs)}")
# (2)(3)
P("\n== (2)(3) Öncül + eşzamanlı (aynı bölge t seansı) birlikte; hedge'li gün-içi ==")
rows = []
for reg in ["X_res_EU", "X_res_AM"]:
    F = Lfull(reg)
    z_lead = F.apply(vh.zscore).loc[vh.START:vh.END]
    z_sync = F.apply(vh.zscore).shift(-1).loc[vh.START:vh.END]   # t+1'e atanmış pencere = yerel tarih t seansı
    cols = [s for s in STOCKS if z_lead[s].notna().sum() > 500]
    for per in ["ALL", "IS", "OOS"]:
        m = vh.period_mask(idx, per)
        r1 = vh.pooled_dk(Y_h.loc[m, cols], [z_lead.loc[m, cols]])
        r2 = vh.pooled_dk(Y_h.loc[m, cols], [z_lead.loc[m, cols], z_sync.loc[m, cols]])
        rows.append({"bolge": reg, "per": per, "b_öncül_yalnız": 1e4 * r1["b"][0], "t_öncül_yalnız": r1["t_dk"][0],
                     "b_öncül|eşz": 1e4 * r2["b"][0], "t_öncül|eşz": r2["t_dk"][0], "b_eşzamanlı": 1e4 * r2["b"][1], "t_eşzamanlı": r2["t_dk"][1]})
M = pd.DataFrame(rows); M.to_csv(vh.RES + "/h4_lead_vs_sync.csv", index=False); P(M.round(2).to_string(index=False))

# (4) saatlik profil
P("\n== (4) Saatlik profil (2023-12+): bar bazında hedge'li getiri ~ z_res (bps/1σ) ==")
H1 = vh.SCR + "/data/h1/"
def bars(sym):
    d = pd.read_parquet(H1 + sym + ".parquet"); d["hh"] = d.index.strftime("%H:%M"); d["day"] = pd.to_datetime(d["ldate"]).dt.normalize()
    d = d[~d.index.duplicated(keep="last")]
    piv = d.pivot_table(index="day", columns="hh", values="c", aggfunc="last")
    return piv
xb = bars("XU100.IS"); xr = vh.raw("XU100.IS")
order = ["06:30", "07:30", "08:30", "09:30", "10:30", "11:30", "12:30", "13:30", "14:30"]
mm = idx >= pd.Timestamp("2023-12-01")
Zres = Xr["X_res"].apply(vh.zscore)
segs = {}
for s in STOCKS:
    p = H1 + s + ".IS.parquet"
    if not os.path.exists(p): continue
    b = bars(s + ".IS"); d = vh.raw(s + ".IS")
    o = d["o"]; c = d["c"]
    prev = o
    xprev = xr["o"]
    for hh in order:
        if hh not in b.columns: continue
        cur = b[hh]; xcur = xb[hh] if hh in xb.columns else None
        if xcur is None: continue
        rr = (np.log(cur / prev.reindex(cur.index)) - np.log(xcur / xprev.reindex(xcur.index)))
        segs.setdefault(hh, {})[s] = rr.reindex(idx)
        prev = cur; xprev = xcur
    # son: son bar kapanışı -> günlük kapanış (kapanış seansı)
    last = b[order].ffill(axis=1).iloc[:, -1]; xlast = xb[order].ffill(axis=1).iloc[:, -1]
    segs.setdefault("son->kapanış", {})[s] = (np.log(c.reindex(last.index) / last) - np.log(xr["c"].reindex(xlast.index) / xlast)).reindex(idx)
rows = []
for hh, dct in segs.items():
    Y = pd.DataFrame(dct); cols = [s for s in Y.columns if Y[s].loc["2023-12-01":].notna().sum() > 200]
    Y = Y.where(Y.abs() < 0.08)
    r = vh.pooled_dk(Y.loc[mm, cols], [Zres.loc[mm, cols]])
    lab = {"06:30": "açılış->07:30 (açılış seansı+ilk 30dk)"}.get(hh, f"bar bitişi {hh}+1sa" if hh != "son->kapanış" else hh)
    rows.append({"segment": hh, "aciklama": lab, "b_bps": 1e4 * r["b"][0], "t_dk": r["t_dk"][0], "nobs": r["nobs"]})
H = pd.DataFrame(rows); H["kumulatif_b"] = H.b_bps.cumsum(); H.to_csv(vh.RES + "/h4_hourly_profile.csv", index=False); P(H.round(2).to_string(index=False))
open(vh.RES + "/h4_summary.txt", "w").write("\n".join(txt))
