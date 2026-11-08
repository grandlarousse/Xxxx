"""IBS dönüşü: bölge (eşzamansızlık) ve oynaklık/maliyet oranı ile ayrıştırma + EWY ayrıntısı.
Soru: genel_tum'da FDR'den geçen EWY IBS sonucu seçim yanlılığı mı, yoksa ilkesel bir nedeni (yüksek oynaklık / düşük maliyet,
Asya eşzamansızlığı) var mı? Kurallar strategies.LIB'den (değiştirilmeden): MR_ibs_lt02, MR_ibs_lt01_dusus; h=1.
Çalıştır: python3 -I kod/ajan_uluslararasi/a5_ibs_bolge.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import ortak, lib
import strategies as S

def main():
    scr = ortak.screen()
    ind = ortak.independent(10)
    rows, pools = [], []
    for sig in ["MR_ibs_lt02", "MR_ibs_lt01_dusus"]:
        for mode in ("C0", "O1", "C1"):
            by_reg = {}
            for s in ind:
                df = lib.load(s)
                sg = S.LIB[sig](df, None).reindex(df.index).fillna(False).astype(bool); sg.iloc[:200] = False
                st, tr = ortak.full_stats(df, sg, 1, mode, label=sig, sym=s)
                vol = np.log(df["c"]).diff().std() * 1e4
                st.update({"sig": sig, "reg": ortak.REGION.get(s), "vol_bp_tum": vol, "gross_per_vol": st["mean_gross_bp"] / vol,
                           "cost_over_vol": lib.cost_bp(df) / vol})
                rows.append(st)
                if len(tr): tr["sym"] = s; by_reg.setdefault(ortak.REGION.get(s), []).append(tr)
            for reg, lst in by_reg.items():
                r = ortak.pooled(pd.concat(lst, ignore_index=True), 1); r.update({"sig": sig, "mode": mode, "reg": reg}); pools.append(r)
    E = pd.DataFrame(rows); P = pd.DataFrame(pools)
    E.to_csv(os.path.join(ortak.OUT, "ibs_bolge_etf.csv"), index=False); P.to_csv(os.path.join(ortak.OUT, "ibs_bolge_havuz.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 300)
    print(P[["sig", "mode", "reg", "k_etf", "n_dates", "mean_gross_bp", "mean_net_bp", "t_nw", "is_net_bp", "oos_net_bp", "years_pos_frac"]].round(2).to_string(index=False))
    e = E[(E["mode"] == "C0")]
    for sig in e["sig"].unique():
        x = e[e["sig"] == sig]
        print(sig, "C0 h1: corr(brut/vol, 1) vs maliyet/vol:", round(x["gross_per_vol"].corr(x["cost_over_vol"]), 2),
              "| corr(net, maliyet/vol):", round(x["mean_net_bp"].corr(x["cost_over_vol"]), 2),
              "| ort. brüt/vol:", round(x["gross_per_vol"].mean(), 3))
        print(x.sort_values("cost_over_vol")[["sym", "reg", "n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "gross_per_vol", "cost_over_vol"]].round(3).head(10).to_string(index=False))
    # EWY: kendi gecikmesi (otokorelasyon) IS/OOS ve KORU'ya EWY sinyaliyle uygulama
    ewy = lib.load("EWY"); r = np.log(ewy["c"]).diff()
    for nm, m in (("IS", r.index <= lib.IS_END), ("OOS", r.index > lib.IS_END)):
        x = r[m]; print("EWY 1g otokorelasyon", nm, round(x.autocorr(1), 3), "n", len(x))
    on = ewy["o"] / ewy["c"].shift(1) - 1; intra = ewy["c"] / ewy["o"] - 1
    for nm, m in (("IS", r.index <= lib.IS_END), ("OOS", r.index > lib.IS_END)):
        print("EWY corr(gün içi t, gece t+1)", nm, round(intra[m].corr(on.shift(-1)[m]), 3))
    koru = lib.load("KORU")
    for sig in ["MR_ibs_lt01_dusus", "MR_ibs_lt02"]:
        sg = S.LIB[sig](ewy, None).reindex(ewy.index).fillna(False).astype(bool); sg.iloc[:200] = False
        for mode in ("C0", "O1", "C1"):
            st, tr = ortak.full_stats(koru, sg.reindex(koru.index).fillna(False), 1, mode, label=sig, sym="KORU")
            print("KORU <- EWY", sig, mode, {k: round(st[k], 2) for k in ["n", "mean_gross_bp", "mean_net_bp", "t", "is_net_bp", "oos_net_bp", "years_pos_frac", "worst_bp"]})

if __name__ == "__main__":
    main()
