"""cin - Adım 7: bist_pairs.csv -> f_cin.csv (BRIEF formatı) + orijinal-vs-alternatif BIST temsil karşılaştırması.
FDR (BH, q=0,05): senkron ve gün-içi öncülük testleri AYRI aileler. Güven: BRIEF ölçeği (mekanizma: listelenen tüm çiftler için makul kabul edildi)."""
import sys; sys.path.insert(0, "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/code_cin")
import cin_lib as C, numpy as np, pandas as pd
from pairs_def import ORIG, ALT
ll = C.ll; OUT = "/tmp/claude-0/-home-user-Xxxx/210cb6c1-ba48-587d-972a-9ce1d37b6259/scratchpad/out/"
B = pd.read_csv(OUT + "code_cin/bist_pairs.csv")
B["p_sync"] = ll.t_to_p(B.t_sync); B["p_intra"] = ll.t_to_p(B.intra_t)
B["fdr_sync"], _ = ll.fdr(B.p_sync.values); B["fdr_intra"], _ = ll.fdr(B.p_intra.values)
A = pd.read_csv(OUT + "cin_alternatifler.csv")
def best_alt(o):
    x = A[(A.orijinal == o) & ~A.alternatif_tv.astype(str).str.contains("HKEX|AÇILMIYOR|HSI:", regex=True)].sort_values("corr_weekly", ascending=False)
    return f"{x.iloc[0].alternatif_tv} (haftalık r={x.iloc[0].corr_weekly:.2f})" if len(x) else "?"
def desc(d): return ORIG.get(d, ALT.get(d, ("", "", "")))[0]
def tv(d):
    if d in ORIG and not (d in ALT and "HKEX" not in ALT[d][1]):
        return "Çin borsası-AÇILMIYOR -> alt: " + best_alt(d) if "HKEX" not in ORIG[d][1] and "HSI" not in ORIG[d][1] and "FX:" not in ORIG[d][1] else ORIG[d][1] + " | alt: " + best_alt(d)
    return ALT.get(d, ("", "?", ""))[1]
def ysym(d):
    if d.startswith("FUT:"): return f"SINA:{d[4:]}(roll-düz.,tekil kontrat)"
    if d.startswith("SIDX:"): return f"SINA:{d[5:]}"
    return d
def conf_sync(r):
    sig = r.fdr_sync; big = abs(r.corr_full) >= 0.30 or abs(r.pcorr_xu100 if pd.notna(r.pcorr_xu100) else 0) >= 0.15
    same = np.sign(r.corr_is) == np.sign(r.corr_full) if pd.notna(r.corr_is) else True
    oos_ok = np.sign(r.corr_oos) == np.sign(r.corr_full) and abs(r.corr_oos) > 2 / np.sqrt(max(r.n, 1) * 0.6)
    if sig and big and r.yr_same_sign >= 0.75 and same and oos_ok and r.n >= 750: return "YÜKSEK"
    if sig and oos_ok: return "ORTA"
    if r.n < 500: return "DÜŞÜK"
    return "DÜŞÜK" if abs(r.corr_full) > 0.05 or (pd.notna(r.corr_w) and abs(r.corr_w) > 0.1) else "ÇOK DÜŞÜK"
def conf_lead(r):
    if r.fdr_intra and abs(r.intra_t) >= 3 and r.bt_oos_sharpe > 0 and r.bt_is_sharpe > 0: return "YÜKSEK"
    if r.fdr_intra and r.bt_oos_sharpe > 0: return "ORTA"
    if abs(r.intra_t) >= 2: return "DÜŞÜK"
    return "ÇOK DÜŞÜK"
rows = []
for _, r in B.iterrows():
    base = {"stock": r.stock, "driver_yahoo": ysym(r.driver), "driver_desc": desc(r.driver) + (" [orijinal]" if r.role == "orig" else f" [alternatif -> {r.maps_to}]"),
            "tv_ticker": tv(r.driver), "n": int(r.n), "mechanism": r.group}
    note_s = f"haftalık r={r.corr_w:.2f} (kısmi|XU100 {r.pcorr_w_xu100:.2f}); USD bazlı r={r.corr_usd:.2f}; IS={r.corr_is:.2f} OOS={r.corr_oos:.2f}; yıl-işaret={r.yr_same_sign:.2f}; başlangıç {r.start}"
    note_s += "; Asya kapanışı: D_t penceresi BIST t-1 seansını da içerir" if r.asia_close else "; ABD/Avrupa kapanışlı: A_t BIST kapanışından sonrasını da içerir"
    rows.append({**base, "relation": "sync", "lag": 0, "corr_full": r.corr_full, "corr_3y": r.corr_3y, "corr_1y": r.corr_1y, "pcorr_xu100": r.pcorr_xu100, "beta": r.beta,
                 "t_stat": r.t_sync, "gap_corr": r.gap_corr, "intra_corr": r.intra_corr, "is_oos": f"{r.corr_is:.2f}/{r.corr_oos:.2f}", "bt_oos_sharpe": np.nan,
                 "bt_oos_mean_bps": np.nan, "confidence": conf_sync(r), "notes": note_s + f"; FDR={'geçti' if r.fdr_sync else 'kaldı'}"})
    lag = 0 if r.asia_close else 1
    rows.append({**base, "relation": "lead_intra", "lag": lag, "corr_full": r.intra_corr, "corr_3y": np.nan, "corr_1y": np.nan, "pcorr_xu100": np.nan, "beta": np.nan,
                 "t_stat": r.intra_t, "gap_corr": r.gap_corr, "intra_corr": r.intra_corr, "is_oos": f"BT Sharpe IS={r.bt_is_sharpe:.2f}/OOS={r.bt_oos_sharpe:.2f}",
                 "bt_oos_sharpe": r.bt_oos_sharpe, "bt_oos_mean_bps": r.bt_oos_mean_bps, "confidence": conf_lead(r),
                 "notes": (f"sinyal D_t (Asya kapanışı ~BIST açılışı) -> BIST gün-içi t" if r.asia_close else "sinyal A_{t-1} -> BIST gün-içi t") +
                          f"; brüt OOS {r.bt_oos_mean_bps_gross:.1f} bps, net(10bps) {r.bt_oos_mean_bps:.1f}; gap r={r.gap_corr:.2f} (t={r.gap_t:.1f}, işlenemez); ters yön r={r.rev_corr:.2f} (t={r.rev_t:.1f}); FDR={'geçti' if r.fdr_intra else 'kaldı'}"})
F = pd.DataFrame(rows)
cols = ["stock", "driver_yahoo", "driver_desc", "tv_ticker", "relation", "lag", "corr_full", "corr_3y", "corr_1y", "pcorr_xu100", "beta", "t_stat", "gap_corr", "intra_corr",
        "is_oos", "bt_oos_sharpe", "bt_oos_mean_bps", "n", "confidence", "mechanism", "notes"]
F[cols].round(3).to_csv(OUT + "f_cin.csv", index=False)
# orijinal vs alternatif: aynı hisse için eşlenen orijinalin korelasyonu ile alternatifinki
O = B[B.role == "orig"].set_index(["stock", "driver"]); rows = []
for _, r in B[B.role == "alt"].iterrows():
    k = (r.stock, r.maps_to)
    if k not in O.index: continue
    o = O.loc[k]
    rows.append({"stock": r.stock, "orijinal": r.maps_to, "alternatif": r.driver, "orig_sync": o.corr_full, "alt_sync": r.corr_full, "orig_w": o.corr_w, "alt_w": r.corr_w,
                 "orig_pc": o.pcorr_xu100, "alt_pc": r.pcorr_xu100, "orig_pcw": o.pcorr_w_xu100, "alt_pcw": r.pcorr_w_xu100, "orig_gap": o.gap_corr, "alt_gap(lag1)": r.gap_corr,
                 "orig_intra_t": o.intra_t, "alt_intra_t": r.intra_t, "n_orig": o.n, "n_alt": r.n, "ratio_w": r.corr_w / o.corr_w if abs(o.corr_w) > 0.03 else np.nan})
V = pd.DataFrame(rows); V.round(3).to_csv(OUT + "code_cin/orig_vs_alt_bist.csv", index=False)
print("testler: senkron", len(B), "FDR geçen", int(B.fdr_sync.sum()), "| gün-içi öncülük", len(B), "FDR geçen", int(B.fdr_intra.sum()))
print(F.confidence[F.relation == "sync"].value_counts().to_dict(), F.confidence[F.relation == "lead_intra"].value_counts().to_dict())
