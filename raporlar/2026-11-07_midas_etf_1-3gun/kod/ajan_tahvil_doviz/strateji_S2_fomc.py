"""ADAY S2 — FOMC karar günü uzun vade tahvil getirisi (Hillenbrand 2025; Pan & Peng: FOMC çevresinde uzun vadeli getiri düşüşü).
Kural: D = planlı FOMC karar günü (federalreserve.gov takvimi; 14:00 ET açıklama). D-1 KAPANIŞINDA TMF (3x TLT) ya da TLT al,
       D KAPANIŞINDA sat (1 işlem günü; karar günü tutulur).
Çalıştır: python3 -I kod/ajan_tahvil_doviz/strateji_S2_fomc.py
Basılanlar: ana sonuç (TMF, TLT, EDV), C0/O1/C1, maliyet duyarlılığı, aile içi, komşu pencereler, plasebo, yıllar."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import td, lib

pd.set_option("display.width", 250); pd.set_option("display.max_rows", 200)
IDX = lib.load("SPY").index
fomc = td.events("fomc", ["FOMC_karar"])
S = td.ev_on_idx(fomc, IDX, -1)
COLS = ["sym", "mode", "h", "n", "mean_gross_bp", "t_gross", "mean_net_bp", "net_bp_1000", "net_bp_10000", "win", "pf", "t", "is_net_bp", "is_t",
        "oos_net_bp", "oos_t", "years_pos_frac", "maxdd", "worst_bp", "cost_bp"]
print("=== S2 ana kural: FOMC D-1 kapanış -> D kapanış ===")
main = []; trs = {}
for sym in ["TMF", "TLT", "EDV", "UBT"]:
    for m in ("C0", "O1", "C1"):
        s, tr = td.full_eval(td.load(sym), S, 1, m, sym=sym, warm=0)
        main.append(td.row(s)); trs[(sym, m)] = tr
main = pd.DataFrame(main)
print(main[COLS].round(2).to_string(index=False))
main.to_csv(os.path.join(td.OUT, "S2_ana.csv"), index=False)

print("\n=== Aile içi (C0, brüt) ===")
fam = []
for sym in ["TLT", "EDV", "ZROZ", "TLH", "IEF", "IEI", "GOVT", "AGG", "LQD", "TIP", "MUB", "SHY", "HYG", "EMB", "TMF", "TMV", "TBT", "UUP", "FXE", "FXY"]:
    s, _ = td.full_eval(td.load(sym), S, 1, "C0", sym=sym, warm=0); fam.append(td.row(s))
fam = pd.DataFrame(fam)
print(fam[["sym", "n", "mean_gross_bp", "t_gross", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))
fam.to_csv(os.path.join(td.OUT, "S2_aile.csv"), index=False)

print("\n=== Komşu pencereler ve plasebo (TLT brüt, TMF net) ===")
nb = []
for lab, k, h in [("D-3->D-2", 3, 1), ("D-2->D-1", 2, 1), ("D-1->D ANA", 1, 1), ("D->D+1", 0, 1), ("D-2->D+1 (TD03 birincil)", 2, 3),
                  ("D-1->D+1", 1, 2), ("plasebo D-6->D-5", 6, 1), ("plasebo D+4->D+5", -4, 1)]:
    sg = td.ev_on_idx(fomc, IDX, -k)
    for sym in ("TLT", "TMF"):
        s, _ = td.full_eval(td.load(sym), sg, h, "C0", sym=sym, warm=0)
        nb.append(td.row(s, {"pencere": lab}))
nb = pd.DataFrame(nb)
print(nb[["pencere", "sym", "n", "mean_gross_bp", "t_gross", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))
nb.to_csv(os.path.join(td.OUT, "S2_komsu.csv"), index=False)

tm = trs[("TMF", "C0")]; tl = trs[("TLT", "C0")]
print("\n=== Yıllara göre ===")
yy = pd.DataFrame({"TMF_net_bp": tm.groupby(tm.sig_date.dt.year).net.mean() * 1e4, "n": tm.groupby(tm.sig_date.dt.year).size(),
                   "TLT_brut_bp": tl.groupby(tl.sig_date.dt.year).gross.mean() * 1e4})
print(yy.round(1).to_string())
yy.to_csv(os.path.join(td.OUT, "S2_yillar.csv"))
print("\nEn kötü 5 TMF işlemi:")
print(tm.sort_values("net").head(5).assign(net_bp=lambda d: d.net * 1e4)[["sig_date", "exit_date", "net_bp"]].to_string(index=False))
for ex in (2020, 2022):
    m = tm.sig_date.dt.year != ex
    print(f"{ex} hariç TMF net: {tm[m].net.mean()*1e4:.1f} bp, t={td._t(tm[m].net.values):.2f}")
tm.to_csv(os.path.join(td.OUT, "S2_islemler_TMF_C0.csv"), index=False)
print("Sıradaki FOMC: 2026-12-09 (Çar) -> giriş 2026-12-08 kapanış, çıkış 2026-12-09 kapanış")
