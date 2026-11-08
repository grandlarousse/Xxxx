"""Aday derin inceleme yardımcıları: tam istatistik, mod sağlamlığı, maliyet duyarlılığı, yıl yıl, aykırı değer etkisi,
ailedeki diğer ETF'ler. Aday betikleri (aday_*.py) bunu kullanır."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak as O, lib

def ozet(trade_sym, sig, h, mode, exit_sig=None):
    s, tr = O.full(trade_sym, sig, h, mode, exit_sig)
    return s, tr

def yil_tablosu(tr):
    g = tr.groupby(tr["sig_date"].dt.year)
    return pd.DataFrame({"n": g.size(), "brut_ort_bp": g["gross"].mean() * 1e4, "net_ort_bp": g["net"].mean() * 1e4,
                         "net_toplam_pct": g["net"].sum() * 100, "kazanma": g["net"].apply(lambda x: (x > 0).mean())})

def aykiri(tr):
    g = tr["gross"].values * 1e4
    q1, q99 = np.percentile(g, [1, 99])
    srt = np.sort(g)
    k = max(1, int(round(0.05 * len(g))))
    return {"medyan_brut_bp": float(np.median(g)), "kirpilmis_1_99_brut_bp": float(g[(g >= q1) & (g <= q99)].mean()),
            "en_iyi_%5_haric_brut_bp": float(srt[:-k].mean()), "en_iyi_islem_bp": float(srt[-1]), "en_kotu_islem_bp": float(srt[0])}

def rapor(baslik, trade_sym, sig, h, mode, diger=(), exit_sig=None, sig_for=None):
    """sig_for: diğer ETF'ler için sinyal üretici (sym -> Seri); verilmezse aynı sinyal kullanılır."""
    print("=" * 100); print(baslik); print("=" * 100)
    s, tr = ozet(trade_sym, sig, h, mode, exit_sig)
    keys = ["n", "mean_gross_bp", "mean_net_bp", "median_net_bp", "win", "pf", "t", "t_gross", "is_n", "is_net_bp", "is_t", "oos_n", "oos_net_bp",
            "oos_t", "years_pos_frac", "n_years", "maxdd", "worst_bp", "uncond_bp", "edge_bp", "t_edge", "cost_bp", "net_bp_1000", "net_bp_2500", "net_bp_10000"]
    print(f"[{trade_sym} {mode} h={h}]  " + "  ".join(f"{k}={s.get(k):.3f}" if isinstance(s.get(k), float) else f"{k}={s.get(k)}" for k in keys))
    print("\n-- Mod sağlamlığı (aynı ETF, h=1..3)")
    rows = []
    for m in ("C0", "O1", "C1"):
        for hh in (1, 2, 3):
            ss, _ = ozet(trade_sym, sig, hh, m, exit_sig)
            rows.append({"mode": m, "h": hh, **{k: ss.get(k) for k in ["n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac", "edge_bp"]}})
    print(pd.DataFrame(rows).round(2).to_string(index=False))
    print("\n-- Yıl yıl"); print(yil_tablosu(tr).round(2).to_string())
    print("\n-- Aykırı değer etkisi"); print({k: round(v, 1) for k, v in aykiri(tr).items()})
    if diger:
        print("\n-- Ailedeki diğer ETF'lerde aynı kural (aynı mod/h)")
        rows = []
        for d in diger:
            sg = sig if sig_for is None else sig_for(d)
            ss, _ = ozet(d, sg, h, mode, exit_sig)
            rows.append({"sym": d, "ptp": O.PTP.get(d), **{k: ss.get(k) for k in ["n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac", "cost_bp"]}})
        print(pd.DataFrame(rows).round(2).to_string(index=False))
    return s, tr
