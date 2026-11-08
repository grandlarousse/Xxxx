"""(1) FOMC öncesi/sonrası faize duyarlı sektörler (önceden tanımlı 6 test).
(2) Bu ajanın TÜM kendi testleri üzerinde BH-FDR (q=0.10): havuz_genel (297) + tests_hipotez (630) + leadlag_ek (102)
    + leadlag_kural (225) + fomc (6) + xme_copx_kural (24) + S1 satırları (18). Çıktı: sonuclar/aile_sektor_tematik/fdr_tum_testler.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from havuz import *

f = pd.read_csv(os.path.join(lib.DATA, "events", "fomc.csv"), parse_dates=["date"])
dec = pd.DatetimeIndex(f[f.event == "FOMC_karar"].date)
idx = D("SPY").index
pre = pd.Series(False, index=idx)
pos = idx.searchsorted(dec)
for p, d in zip(pos, dec):
    if p < len(idx) and idx[p] == d and p > 0: pre.iloc[p - 1] = True   # karar gününden bir önceki işlem günü
RATE = ["KRE", "XLF", "ITB", "VNQ", "XLU", "KIE"]
rows = []
for nm, uni in (("REPS37", REPS), ("faize_duyarli6", RATE)):
    for mode, lab in (("C0", "karar oncesi kapanis->karar gunu kapanis"), ("O1", "karar gunu acilis->kapanis"), ("C1", "karar gunu kapanis->ertesi kapanis")):
        tr = pd.concat([run_sym(s, pre, 1, mode) for s in uni], ignore_index=True)
        r = summarize(tr, f"FOMC {nm} {mode} ({lab})"); r.update({"grup": "FOMC", "h": 1, "mode": mode}); rows.append(r)
fo = pd.DataFrame(rows); fo.to_csv(os.path.join(OUT, "fomc_sektor.csv"), index=False)
pd.set_option("display.width", 250)
print(fo[["label", "n", "mean_gross_bp", "mean_net_bp", "t_cl", "is_net_bp", "oos_net_bp", "years_pos_frac", "mean_hedged_bp", "t_hedged_cl"]].round(2).to_string())

# ---- FDR ----
P = []
a = pd.read_csv(os.path.join(OUT, "havuz_genel.csv"))
P += [("havuz_genel", f"{r.sig} {r['mode']} h{r.h} {r.exit}", r.p_cl, r.mean_net_bp, r.t_cl) for _, r in a.iterrows()]
b = pd.read_csv(os.path.join(OUT, "tests_hipotez.csv"))
for _, r in b.iterrows():
    n = r.n_weeks if np.isfinite(r.get("n_weeks", np.nan)) else r.n
    P.append(("hipotez_" + r.grup, r.label, lib.t_to_p(r.t_cl, n) if np.isfinite(r.t_cl) else np.nan, r.mean_net_bp, r.t_cl))
c = pd.read_csv(os.path.join(OUT, "leadlag_ek.csv"))
for _, r in c.iterrows():
    P.append(("leadlag_ek", f"{r.leader}->{r.target} h1", r.p_h1, r.lag_bp_per_sd_h1, r.lag_t_h1))
    P.append(("leadlag_ek", f"{r.leader}->{r.target} h3", r.p_h3, r.lag_bp_per_sd_h3, r.lag_t_h3))
d = pd.read_csv(os.path.join(OUT, "leadlag_kural.csv"))
P += [("leadlag_kural", f"{r.label} {r['mode']} h{r.h}", r.p, r.mean_net_bp, r.t_naive) for _, r in d.iterrows()]
for _, r in fo.iterrows():
    P.append(("fomc", r.label, lib.t_to_p(r.t_cl, r.n_weeks), r.mean_net_bp, r.t_cl))
xm = os.path.join(OUT, "xme_copx_kural.csv")
if os.path.exists(xm):
    for _, r in pd.read_csv(xm).iterrows():
        P.append(("xme_copx_kural", f"{r.label} {r['mode']} h{r.h}", lib.t_to_p(r.t_naive, r.n), r.mean_net_bp, r.t_naive))
# S1 (SMH IBS<0.2 -> SMH) ve SOXX kopyası: 3 mod x 3 h
for sg in ("SMH", "SOXX"):
    for mode in ("C0", "O1", "C1"):
        for h in (1, 2, 3):
            s_, _ = lib.evaluate(D(sg), lib.ibs(D(sg)) < 0.2, h, mode, cost_for(D(sg), 2500.0))
            P.append(("strateji_S1", f"{sg} IBS<0.2 -> {sg} {mode} h{h}", lib.t_to_p(s_["t"], s_["n"]), s_["mean_net_bp"], s_["t"]))
F = pd.DataFrame(P, columns=["kaynak", "test", "p", "etki_bp", "t"])
F["fdr10"] = lib.bh_fdr(F.p.values, 0.10)
F.to_csv(os.path.join(OUT, "fdr_tum_testler.csv"), index=False)
print("\nTOPLAM KENDİ TEST SAYISI:", len(F), " BH-FDR q=0.10 geçen:", int(F.fdr10.sum()),
      " bunlardan pozitif etki:", int((F.fdr10 & (F.t > 0)).sum()))
print(F[F.fdr10].sort_values("t", ascending=False).to_string())
